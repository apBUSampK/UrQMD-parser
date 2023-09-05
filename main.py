import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


if __name__ == "__main__":
    df = pd.read_csv(input("Enter filename: "), sep=' ', names=['t', 'x', 'y', 'z', 'p0', 'px', 'py', 'pz', 'm', 'ityp',
                                                                'di3', 'ch', 'pcn', 'ncoll', 'ppt', 'eta', 'nev'])
    data = pd.DataFrame(columns=df.columns)
    tottime = float(df.iloc[5, 7])
    dtime = float(df.iloc[5, 9])
    time = dtime

    seps = df[df['y'].isna()].index
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