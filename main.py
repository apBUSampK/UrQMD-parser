import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

pr14 = str(input("Enter f14 prefix:"))
pr15 = str(input("Enter f15 prefix:"))
df14 = pd.read_csv(pr14 + '_1.csv', sep=' ', names=['t', 'x', 'y', 'z', 'p0', 'px', 'py', 'pz', 'm', 'ityp',
                                                            'di3', 'ch', 'pcn', 'ncoll', 'ppt', 'eta', 'nev'],
                   usecols=['t', 'x', 'y', 'z', 'p0', 'px', 'py', 'pz', 'ityp', 'pcn', 'ppt', 'eta', 'nev'], dtype=str)
df15 = pd.read_csv(pr15 + '_1.csv', sep=' ', names=['id', 't', 'x', 'y', 'z', 'p0', 'px', 'py', 'pz', 'm',
                                                    'ityp', 'di3', 'ch', 'pcn', 'ncoll', 's', 'debug'],
                   usecols=['t', 'x', 'y', 'z', 'p0', 'px', 'py', 'pz', 'ityp', 'pcn', 'debug'], dtype=float).rename(columns={'debug' : 'nev'})

data14 = pd.DataFrame(columns=df14.columns)
data15 = pd.DataFrame(columns=df15.columns)
tottime = float(df14.iloc[5, 7])
dtime = float(df14.iloc[5, 9])
time = dtime

seps = df14[df14['y'].isna()].index
nev = 1

# Parse events

    for sep in seps:
        eSlice: pd.DataFrame = df.iloc[sep + 2 : sep + 2 + int(df.iloc[sep]['t'])]
        eSlice = eSlice.astype(float)
        p = np.sqrt(np.square(eSlice['px']) + np.square(eSlice['py']) + np.square(eSlice['pz']))
        eSlice['eta'] = np.log((p + eSlice['pz']) / (p - eSlice['pz']))
        eSlice['nev'] = nev
        data = pd.concat((data, eSlice), ignore_index=True)
        time += dtime
        if time > tottime:
            time = dtime
            nev += 1

    # Some plots

    fig : plt.Figure = plt.figure()
    ax = fig.add_subplot(projection='3d')

    d1 = data[1 == data['nev']]
    for time in d1['t'].unique():
        d1t = d1[d1['t'] == time]
        ax.scatter3D(d1t['x'], d1t['y'], d1t['z'], marker='o')
        plt.savefig(f'./pics/passing_{time}_fmc.png', dpi=300)
        ax.clear()
