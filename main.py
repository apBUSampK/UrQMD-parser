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

if __name__ == "__main__":
    df = pd.read_csv(input("Enter filename: "), sep=' ', names=['t', 'x', 'y', 'z', 'p0', 'px', 'py', 'pz', 'm', 'ityp',
                                                                'di3', 'ch', 'pcn', 'ncoll', 'ppt', 'eta', 'nev'], low_memory=False)
    data = pd.DataFrame(columns=df.columns)
    tottime = float(df.iloc[5, 7])
    dtime = float(df.iloc[5, 9])
    mass = int(df.iloc[1, 3]) + int(df.iloc[1, 8])
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
        d1ts = d1t[d1t['ppt'] == 0]
        d1tp = d1t[d1t['ppt'] != 0]
        ax.scatter3D(d1ts['x'], d1ts['y'], d1ts['z'], marker='o', color='b')
        ax.scatter3D(d1tp['x'], d1tp['y'], d1tp['z'], marker='o', color='r')
        ax.set_xlabel('$x$, fm')
        ax.set_ylabel('$y$, fm')
        ax.set_zlabel('$z$, fm')
        ax.set_xlim(-20, 20)
        ax.set_ylim(-20, 20)
        ax.set_zlim(-20, 20)
        ax.set_title(rf'$b = 2 fm, \tau = {time} fm / c$')
        plt.savefig(f'./pics/3d_evo/{time}_fmc.png', dpi=300)
        ax.clear()

    fig.clear()
    ax = fig.add_subplot()

    npart = []

    #nucleons only now
    data = data[data['ityp'] == 1]

    for time in d1['t'].unique():
        dt = data[data['t'] == time]
        ax.hist(dt['eta'], histtype='step', edgecolor='k', density=True, bins=50)
        ax.set_xlabel(r'$\eta$')
        ax.set_ylabel(r'$<P(\eta)>$')
        ax.set_title(rf'$b = 2 fm, \tau = {time} fm / c$')
        plt.savefig(f'./pics/eta/{time}_fmc.png', dpi=300)
        ax.clear()
        npart.append((mass - dt[dt['ppt'] == 0].shape[0]) / nev)

    ax.scatter(np.arange(dtime, tottime + dtime/2, dtime), npart)
    ax.grid()
    ax.set_xlabel(r'$\tau, fm$')
    ax.set_ylabel(r'$<N_{part}>$')
    plt.savefig('./pics/npart.png', dpi=300)
