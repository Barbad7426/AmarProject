# Data

Raw data files are not stored in this repository.

## Source
NHANES August 2021–August 2023, CDC / National Center for Health
Statistics. Public-use files:
https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/DataFiles/

## Files used
| File | Content |
|---|---|
| `DEMO_L.xpt` | Demographics, sampling weights, design variables |
| `BPXO_L.xpt` | Oscillometric blood pressure |
| `BMX_L.xpt` | Body measures |
| `SLQ_L.xpt` | Sleep questionnaire |

Date downloaded: 2026-11-02

## How to rebuild the analytic dataset
From the project root:

```bash
for f in DEMO_L BPXO_L BMX_L SLQ_L; do
  curl -L -o data/raw/$f.xpt https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/DataFiles/$f.xpt
done
python src/02_merge.py
python src/04_population.py
python src/05_descriptive.py
python src/06_plots.py
```

Intermediate files are written to `data/processed/` (not tracked).