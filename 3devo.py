import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

d1 = pd.read_parquet(input("Enter path to parquet file:"))
suf = input("Enter suffix:")
fig = plt.figure()
ax = fig.add_subplot(projection="3d")
ax.view_init(0, 90, 90)
time_arr = d1['t'].unique()

if not os.path.isdir(f"pics/3d_evo{suf}"):
    os.makedirs(f"pics/3d_evo{suf}")

for time in time_arr:
    d1t = d1[d1['t'] == time]
    d1t['ityp'] = d1t['ityp'].abs()
    d1tsl = d1t.loc[d1t['ppt'] == 0].loc[d1t['pz'] > 0]
    d1tsr = d1t.loc[d1t['ppt'] == 0].loc[d1t['pz'] < 0]
    d1tp = d1t.loc[d1t['ppt'] != 0].loc[d1t['ityp'] < 100]
    d1tm = d1t[d1t['ityp'] > 100]
    ax.scatter3D(d1tsl['x'], d1tsl['y'], d1tsl['z'], marker='o', color='yellow')
    ax.scatter3D(d1tsr['x'], d1tsr['y'], d1tsr['z'], marker='o', color='dodgerblue')
    ax.scatter3D(d1tp['x'], d1tp['y'], d1tp['z'], marker='o', color='red')
    ax.scatter3D(d1tm['x'], d1tm['y'], d1tm['z'], marker='.', color='lime')
    ax.set_xlabel('$x$, fm')
    ax.set_ylabel('$y$, fm')
    ax.set_zlabel('$z$, fm')
    ax.set_xlim(-20, 20)
    ax.set_ylim(-20, 20)
    ax.set_zlim(-20, 20)
    ax.set_yticks([])
    ax.set_title(rf'$b = 10$ fm, $\tau = {time}$ fm/c')
    plt.savefig(f'./pics/3d_evo{suf}/{time}_fmc.png', dpi=300)
    ax.clear()
