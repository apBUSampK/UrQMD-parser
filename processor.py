import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import gc

pr14 = str(input("Enter f14 prefix:"))
pr15 = str(input("Enter f15 prefix:"))
pr_save = str(input("Enter prefix for saved .parquet files:"))
df14 = pd.read_csv(pr14 + '_1_reduced.csv', sep=' ', names=['t', 'x', 'y', 'z', 'p0', 'px', 'py', 'pz', 'm', 'ityp',
                                                            'di3', 'ch', 'pcn', 'ncoll', 'ppt', 'eta', 'nev'], dtype=str)

data14 = pd.DataFrame(columns=df14.columns)
tottime = float(df14.iloc[5, 7])
dtime = float(df14.iloc[5, 9])
mass = int(df14.iloc[1, 3]) + int(df14.iloc[1, 8])
time = dtime

seps = df14[df14['y'].isna()].index
nev = 1

# Parse events

for sep in seps:
    eSlice: pd.DataFrame = df14.iloc[sep + 2 : sep + 2 + int(df14.iloc[sep]['t'])]
    eSlice = eSlice.astype(float)
    p = np.sqrt(np.square(eSlice['px']) + np.square(eSlice['py']) + np.square(eSlice['pz']))
    eSlice['eta'] = np.log((p + eSlice['pz']) / (p - eSlice['pz']))
    eSlice['nev'] = nev
    data14 = pd.concat((data14, eSlice), ignore_index=True)
    time += dtime
    if time > tottime:
        time = dtime
        nev += 1
    if nev > 1:
        break

del df14
d1 = data14[1 == data14['nev']]
del data14
time_arr = d1['t'].unique()
d1.to_parquet(f"{pr_save}1event.parquet")
del d1
gc.collect()

df15 = pd.read_csv(pr15 + '_1_reduced.csv', sep=' ', names=['id', 't', 'x', 'y', 'z', 'p0', 'px', 'py', 'pz', 'm',
                                                    'ityp', 'di3', 'ch', 'pcn', 'ncoll', 's', 'debug'],
                   usecols=['id', 't', 'x', 'y', 'z', 'p0', 'px', 'py', 'pz', 'ityp', 'pcn', 'debug'], dtype=float).rename(columns={'debug' : 'nev'})

seps15 = df15[df15['id'] == -1].index
df15 = df15[df15['id'] != -1]
for i in range(len(seps15) - 1):
    df15.loc[seps15[i]:seps15[i+1], 'nev'] = i + 1
df15.loc[seps15[-1]:, 'nev'] = len(seps15)

npart = pd.DataFrame(columns=['time', 'elastic', 'inelastic', 'sum', 'ncoll'], index=[0])

for nev in df15['nev'].unique():
    eSlice = df15[df15['nev'] == nev]
    heads = eSlice[eSlice['pcn'].isna()]
    eSlice = eSlice.dropna()
    eSlice = eSlice[eSlice['id'] <= mass]
    el = 0
    inel = 0
    ncoll = 0
    ncoll_i = 0
    for time in time_arr:
        teSlice = eSlice.loc[lambda df: df['t'] < time].loc[lambda df: df['t'] > time - dtime]
        hSlice = heads.loc[(heads['z'] < time) & (heads['z'] > time - dtime), 'x']
        hSlice = ~((hSlice == 13) | (hSlice == 17) | (hSlice == 19) | (hSlice == 22) | (hSlice == 26) | (hSlice == 35))
        for id in teSlice['id'].unique():
            type = 0
            for event in teSlice.loc[teSlice['id'] == id].index:
                if hSlice.loc[:event].size:
                    if hSlice.loc[:event].iat[-1]:
                        type = 1
                        break
            eSlice.drop(eSlice[eSlice['id'] == id].index, inplace=True) #erase this nucleon, so we don't count it in next [t; t + dt]
            inel += type
            el += (1 - type)
        ncoll += hSlice.size
        ncoll_i += hSlice.sum()
        npart = pd.concat((npart, pd.Series({'time' : time, 'elastic' : el, 'inelastic' : inel, 'sum' : el + inel, 'ncoll' : ncoll, 'ncoll_i' : ncoll_i}).to_frame().T), ignore_index=True)

npart = npart.groupby(['time']).mean()

npart.to_parquet(f"{pr_save}npart.parquet")
