import sys

if (len(sys.argv) != 2):
    sys.stderr.write("Wrong number of arguments!\n")
    sys.exit(1)
fname = sys.argv[1]
with open(fname) as fr, open(fname[:-4] + "_reduced.csv", 'w') as fw:
    for line in fr:
        fw.write(" ".join(line.split()) + '\n')