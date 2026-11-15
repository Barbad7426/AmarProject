# Project Card

## Dataset and subset
Path A: NHANES August 2021–August 2023 (CDC/NCHS), public-use files:
- `DEMO_L`: demographics, sampling weights, and survey design variables
- `BPXO_L`: blood pressure (three oscillometric readings)
- `BMX_L`: body measures, including BMI
- `SLQ_L`: sleep questionnaire
Files are merged on the participant identifier `SEQN`.

## Working title
Sleep duration and systolic blood pressure in U.S. adults

## Main statistical question
How is sleep duration related to systolic blood pressure among
U.S. adults aged 20 and older?

## Unit of observation and population
Each row represents one participant (`SEQN` is unique in every file).
Unweighted results describe the analytic sample (n = 5,726);
weighted results (using `WTMEC2YR`) are interpretable for the U.S.
civilian non-institutionalized adult population aged 20+.
## Main variables and scales
| Variable | Description | Type |
|---
| `SBP` | Mean of up to three systolic BP readings (mmHg) | Quantitative, continuous |
| `SLEEP_WEEK` | Weekly average sleep: (5 × weekday + 2 × weekend) / 7 (hours) | Quantitative, continuous |
| `SLEEP_CAT` | Short (<7h), Normal (7–9h), Long (>9h) | Ordinal |
| `RIAGENDR` | Sex (male / female) | Binary |
| `RIDAGEYR` | Age in completed years (top-coded at 80) | Quantitative, discrete |
| `BMXBMI` | Body mass index (kg/m²) | Quantitative, continuous |

## Role of variables
- Response: `SBP`
- Main explanatory: `SLEEP_WEEK` (and its categorized form `SLEEP_CAT`)
- Covariates: age, sex, BMI

## Initial hypothesis
Shorter sleep duration is associated with higher systolic blood
pressure in U.S. adults.
## Type of question
Associational: the aim is to examine whether sleep duration is
related to systolic blood pressure, not to predict BP for new
individuals.

## Initial limitations
1. **Self-reported sleep:** sleep duration comes from a questionnaire,
   so it is subject to recall and reporting error.
2. **Observational data:** NHANES is not an experiment, so an
   association cannot be interpreted as a causal effect of sleep on BP.
3. **Unmeasured confounding:** age, sex, and BMI are available and will
   be adjusted for, but factors such as stress and physical activity
   are not included in the analysis files.
4. **Selection:** 1,745 adults who were interviewed but not examined
   were excluded; if they differ systematically from examined
   participants, the sample may not fully represent the population.
5. **Coding limits:** age is top-coded at 80, and sleep hours are
   recorded within a bounded range.