import pandas as pd

RAW = "data/raw"
files = ["DEMO_L", "BPXO_L", "BMX_L", "SLQ_L"]

d = {}
for f in files:
    d[f] = pd.read_sas(f"{RAW}/{f}.xpt", format="xport", encoding="infer")
for name, df in d.items():
    print(name, df.shape, "SEQN unique:", df["SEQN"].is_unique)