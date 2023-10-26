import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

d1 = pd.read_parquet(input("Enter path to parquet file:"))
suf = input("Enter suffix:")
func_t = input("Enter fit type (d for default or s for STAR):")
f = float(input("Enter f:"))

match func_t:
    case "d":
        func = lambda x, y: f * x + (1 - f) * y
    case "s":
        func = lambda x, y: (1 - f) / 2 * x + f * y
    case _:
        exit(1)

if not os.path.isdir("pics"):
    os.makedirs("pics")

fig, ax1 = plt.subplots()

time = d1.index

lns1 = ax1.scatter(time, d1['sum'], color='b', label=r"$\mathrm{N}_{part}$")
lns2 = ax1.scatter(time, func(d1['sum'], d1['ncoll']), color='k', label=r"$\mathrm{N}_{anc.}$, $f = " + str(f) + r"$, "
                                                                        + ("default" if func_t == 'd' else "star"))
ax1.set_title(r"$^{208}$Pb-$^{208}$Pb @ $\sqrt{s_{\mathrm{NN}}} = 4.5$ GeV, $b = 10$ fm")
ax1.set_xlabel(r"$\tau$, fm/c")
ax1.set_xticks(np.arange(0, 16))
ax1.tick_params(direction='in')
ax1.set_ylabel(r"$<N_{part}>$")

ax2 = ax1.twinx()
ax2.set_ylabel(r"$<N_{coll}>$")
lns3 = ax2.plot(time, d1['ncoll'], marker='.', color='m', label=r"$\mathrm{N}_{coll}$")

lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax2.legend(lines + lines2, labels + labels2, loc='upper left')

plt.savefig(f"pics/npart{suf}.png", dpi=300)
