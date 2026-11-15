import numpy as np
import pandas as pd

df = pd.read_csv("data/processed/analytic.csv")
n = len(df)

df["SLEEP_CAT"] = np.select(
    [df["SLEEP_WEEK"] < 7, df["SLEEP_WEEK"] <= 9],
    ["short", "normal"],
    default="long",
)
df["A"] = df["SLEEP_WEEK"] < 7     # short sleep
df["B"] = df["SBP"] >= 130         # high measured SBP

print("n =", n)

# Task 2: marginal and joint
pA = df["A"].mean()
pB = df["B"].mean()
pAB = (df["A"] & df["B"]).mean()

print("\n=== Marginal and joint ===")
print(f"P(A)       = {pA:.4f}")
print(f"P(B)       = {pB:.4f}")
print(f"P(A and B) = {pAB:.4f}")

counts = pd.crosstab(df["A"], df["B"], margins=True)
props = pd.crosstab(df["A"], df["B"], margins=True, normalize="all")
print("\nCounts:\n", counts)
print("\nProportions:\n", props.round(4))

# Task 3: conditional
pB_A = pAB / pA
pB_notA = (~df["A"] & df["B"]).mean() / (1 - pA)
pA_B = pAB / pB

print("\n=== Conditional ===")
print(f"P(B | A)     = {pB_A:.4f}")
print(f"P(B | not A) = {pB_notA:.4f}")
print(f"P(A | B)     = {pA_B:.4f}")

by_sleep = df.groupby("SLEEP_CAT")["B"].agg(n="size", p_high_sbp="mean")
print("\nP(B | sleep category):\n", by_sleep.round(4))

# Task 4: independence check
print("\n=== Independence ===")
print(f"P(A)*P(B)  = {pA * pB:.4f}   vs   P(A and B) = {pAB:.4f}")
print(f"P(B | A)   = {pB_A:.4f}   vs   P(B)       = {pB:.4f}")

counts.to_csv("reports/phase2/table_AB_counts.csv")
props.to_csv("reports/phase2/table_AB_props.csv")
by_sleep.to_csv("reports/phase2/p_highsbp_by_sleep.csv")
# Task A.1: subgroups
df["AGE_GRP"] = pd.cut(df["RIDAGEYR"], bins=[19, 39, 59, 80],
                       labels=["20-39", "40-59", "60+"])
df["SEX"] = df["RIAGENDR"].map({1: "male", 2: "female"})

print("\n=== P(B | age group) ===")
by_age = df.groupby("AGE_GRP", observed=True)["B"].agg(n="size", p_high_sbp="mean")
by_age["share"] = by_age["n"] / n
print(by_age.round(4))

total = (by_age["p_high_sbp"] * by_age["share"]).sum()
print(f"Law of total probability: sum = {total:.4f}   vs   P(B) = {pB:.4f}")

print("\n=== P(B | sex) ===")
by_sex = df.groupby("SEX")["B"].agg(n="size", p_high_sbp="mean")
print(by_sex.round(4))

print("\n=== Mean age by sleep category ===")
print(df.groupby("SLEEP_CAT")["RIDAGEYR"].mean().round(1))

print("\n=== P(B | age group, sleep category) ===")
p_tab = df.pivot_table(index="AGE_GRP", columns="SLEEP_CAT", values="B",
                       aggfunc="mean", observed=True)
n_tab = df.pivot_table(index="AGE_GRP", columns="SLEEP_CAT", values="B",
                       aggfunc="size", observed=True)
print(p_tab.round(3))
print("\nCounts:\n", n_tab)

by_age.to_csv("reports/phase2/p_highsbp_by_age.csv")
by_sex.to_csv("reports/phase2/p_highsbp_by_sex.csv")
p_tab.to_csv("reports/phase2/p_highsbp_by_age_sleep.csv")
# Task 9: Bayes
print("\n=== Bayes: sleep ===")
pB_total = pB_A * pA + pB_notA * (1 - pA)
pA_B_bayes = pB_A * pA / pB_total
print(f"P(B) by total probability = {pB_total:.4f}")
print(f"P(A | B) by Bayes = {pA_B_bayes:.4f}   direct = {pA_B:.4f}")

print("\n=== Bayes: age 60+ given high SBP ===")
bayes_age = by_age[["share", "p_high_sbp"]].copy()
bayes_age.columns = ["prior", "likelihood"]
bayes_age["posterior"] = bayes_age["prior"] * bayes_age["likelihood"] / pB
print(bayes_age.round(4))
print("posterior sum =", round(bayes_age["posterior"].sum(), 4))

# Task A.4: weighted vs unweighted
w = df["WTMEC2YR"]

def wmean(x, wt):
    return (x * wt).sum() / wt.sum()

rows = {
    "P(A) short sleep":  (df["A"].mean(), wmean(df["A"], w)),
    "P(B) high SBP":     (pB, wmean(df["B"], w)),
    "P(B | A)":          (pB_A, wmean(df.loc[df["A"], "B"], w[df["A"]])),
    "P(B | not A)":      (pB_notA, wmean(df.loc[~df["A"], "B"], w[~df["A"]])),
}
for g in ["20-39", "40-59", "60+"]:
    is_g = df["AGE_GRP"] == g
    rows[f"P(age {g})"] = (is_g.mean(), wmean(is_g, w))

wt_tab = pd.DataFrame(rows, index=["unweighted", "weighted"]).T
wt_tab["diff"] = wt_tab["weighted"] - wt_tab["unweighted"]
print("\n=== Weighted vs unweighted ===")
print(wt_tab.round(4))

bayes_age.to_csv("reports/phase2/bayes_age.csv")
wt_tab.to_csv("reports/phase2/weighted_vs_unweighted.csv")