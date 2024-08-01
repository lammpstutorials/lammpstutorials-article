import numpy as np
import re
import yaml

# Import the data from the yaml file
pattern = r"^(keywords:.*$|data:$|---$|\.\.\.$|  - \[.*\]$)"
docs = ""
with open("log.yaml") as f:
    for line in f:
        m = re.search(pattern, line)
        if m:
            docs += m.group(0) + "\n"
thermo = list(yaml.load_all(docs, Loader=yaml.CSafeLoader))

# Read basic information
print("Number of runs: ", len(thermo))
print("All info:", thermo[1]['keywords'])

# Read the data from the second run, and save it. 
F_vs_L = []
for line in thermo[1]["data"]:
    _, _, _, _, L, F = line
    F_vs_L.append([L, F])
np.savetxt("F_vs_L.dat", F_vs_L)