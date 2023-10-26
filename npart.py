import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

d1 = pd.read_parquet(input("Enter path to parquet file:"))
suf = input("Enter suffix:")

if not os.path.isdir("pics"):
    os.makedirs("pics")

fig, ax1 = plt.subplots()

time = d1.index

lns1 = ax1.scatter(time, d1['elastic'], color='g', label="Elastic")
lns2 = ax1.scatter(time, d1['inelastic'], color='r', label="Inelastic")
lns3 = ax1.scatter(time, d1['sum'], color='b', label="Total")
lnsG = ax1.hlines(75.26, 5, 15, color='red', ls='--', lw=2, label='GlauberMC mean')
lnsP = ax1.vlines(7.096, 0, 135, color='k', ls='--')
ax1.set_title(r"$^{208}$Pb-$^{208}$Pb @ $\sqrt{s_{\mathrm{NN}}} = 4.5$ GeV, $b = 2$ fm")
ax1.set_xlabel(r"$\tau$, fm/c")
ax1.set_xticks(np.arange(0, 16))
ax1.tick_params(direction='in')
ax1.set_ylabel(r"$<N_{part}>$")

ax2 = ax1.twinx()
ax2.set_ylabel(r"$<N_{coll}>$")
lns4 = ax2.plot(time, d1['ncoll'], marker='.', color='m', label=r"$N_{coll}$")

lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax2.legend(lines + lines2, labels + labels2, loc='upper left')

plt.savefig(f"pics/npart{suf}.png", dpi=300)
