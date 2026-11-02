import os
import pandas as pd

RAW = "data/raw"

def load(name):
    return pd.read_sas(f"{RAW}/{name}.xpt", format="xport", encoding="infer")

demo = load("DEMO_L")
bp = load("BPXO_L")
bmx = load("BMX_L")
slq = load("SLQ_L")

print("DEMO participants:", len(demo))
for name, df in [("BPXO", bp), ("BMX", bmx), ("SLQ", slq)]:
    found = df["SEQN"].isin(demo["SEQN"]).sum()
    print(f"{name}: {len(df)} rows, {found} found in DEMO")

merged = (
    demo.merge(bp, on="SEQN", how="left", validate="one_to_one")
        .merge(bmx, on="SEQN", how="left", validate="one_to_one")
        .merge(slq, on="SEQN", how="left", validate="one_to_one")
)
print("Merged shape:", merged.shape)

in_all = (demo["SEQN"].isin(bp["SEQN"])
          & demo["SEQN"].isin(bmx["SEQN"])
          & demo["SEQN"].isin(slq["SEQN"]))
print("Present in all 4 files:", in_all.sum())

os.makedirs("data/processed", exist_ok=True)
merged.to_csv("data/processed/merged.csv", index=False)
print("Saved data/processed/merged.csv")