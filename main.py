import pandas as pd
import numpy as np


if __name__ == "__main__":
    df = pd.read_csv(input("Enter filename: "), sep=' ', names=['t', 'x', 'y', 'z', 'p0', 'px', 'py', 'pz', 'm', 'ityp',
                                                                'di3', 'ch', 'pcn', 'ncoll', 'ppt', 'eta', 'nev'], low_memory=False)
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
