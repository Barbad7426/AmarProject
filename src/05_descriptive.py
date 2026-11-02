import os
import numpy as np
import pandas as pd

df = pd.read_csv("data/processed/analytic.csv")
OUT = "reports/phase1/tables"
os.makedirs(OUT, exist_ok=True)

df["SEX"] = df["RIAGENDR"].map({1: "Male", 2: "Female"})

df["SLEEP_CAT"] = np.select(
    [df["SLEEP_WEEK"] < 7, df["SLEEP_WEEK"] <= 9],
    ["Short (<7h)", "Normal (7-9h)"],
    default="Long (>9h)",
)
df["AGE_GRP"] = pd.cut(df["RIDAGEYR"], bins=[19, 39, 59, 80],
                       labels=["20-39", "40-59", "60+"])

for col in ["SEX", "AGE_GRP", "SLEEP_CAT"]:
    t = df[col].value_counts().to_frame("n")
    t["pct"] = (t["n"] / len(df) * 100).round(1)
    print(f"\n=== {col} ===\n{t}")
    t.to_csv(f"{OUT}/freq_{col}.csv")

num = ["RIDAGEYR", "SBP", "DBP", "BMXBMI", "SLEEP_WEEK"]
s = df[num].describe().T
s["median"] = df[num].median()
s["IQR"] = s["75%"] - s["25%"]
s = s[["count", "mean", "median", "std", "25%", "75%", "IQR", "min", "max"]].round(2)
print("\n=== Numeric summary ===\n", s)
s.to_csv(f"{OUT}/numeric_summary.csv")

w = df["WTMEC2YR"]
raw_sbp = df["SBP"].mean()
wtd_sbp = np.average(df["SBP"], weights=w)
short = (df["SLEEP_CAT"] == "Short (<7h)").astype(int)
raw_short = short.mean()
wtd_short = np.average(short, weights=w)
cmp = pd.DataFrame({
    "unweighted": [raw_sbp, raw_short * 100],
    "weighted":   [wtd_sbp, wtd_short * 100],
}, index=["Mean SBP (mmHg)", "Short sleep (%)"]).round(2)
print("\n=== Unweighted vs weighted ===\n", cmp)
cmp.to_csv(f"{OUT}/weighted_vs_unweighted.csv")

g = (df.groupby("SLEEP_CAT")["SBP"]
       .agg(["count", "mean", "median", "std"])
       .reindex(["Short (<7h)", "Normal (7-9h)", "Long (>9h)"])
       .round(2))
print("\n=== SBP by sleep category ===\n", g)
g.to_csv(f"{OUT}/sbp_by_sleep.csv")

df.to_csv("data/processed/analytic.csv", index=False)