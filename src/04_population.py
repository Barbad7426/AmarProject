import numpy as np
import pandas as pd

m = pd.read_csv("data/processed/merged.csv")

m["SBP"] = m[["BPXOSY1", "BPXOSY2", "BPXOSY3"]].mean(axis=1)
m["DBP"] = m[["BPXODI1", "BPXODI2", "BPXODI3"]].mean(axis=1)
m["SLEEP_WEEK"] = (5 * m["SLD012"] + 2 * m["SLD013"]) / 7
m["DMDEDUC2"] = m["DMDEDUC2"].replace(9, np.nan)   # 9 = Don't know

steps = [
    ("Age >= 20",            m["RIDAGEYR"] >= 20),
    ("Examined at MEC",      m["RIDSTATR"] == 2),
    ("Has SBP",              m["SBP"].notna()),
    ("Has weekly sleep",     m["SLEEP_WEEK"].notna()),
    ("Has BMI",              m["BMXBMI"].notna()),
]

flow = [("All participants", len(m), 0)]
df = m.copy()
for label, condition in steps:
    before = len(df)
    df = df[condition.loc[df.index]]
    flow.append((label, len(df), before - len(df)))

flow = pd.DataFrame(flow, columns=["Step", "Remaining", "Excluded"])
print(flow.to_string(index=False))

df.to_csv("data/processed/analytic.csv", index=False)
flow.to_csv("reports/phase1/flow_table.csv", index=False)
print("\nFinal analytic sample:", len(df))