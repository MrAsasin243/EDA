# EDA Research Report — template

> Purpose: produce an analytical artifact that can be reviewed and reproduced by someone who did not write the notebook. Replace every bracketed instruction. Delete sections only when you explain why they are not applicable.

## 1. Executive summary

- **Research question:** [one precise question]
- **Decision or downstream action:** [what the analysis may inform]
- **Main findings:** [three to five evidence-backed statements]
- **Critical caveats:** [the most consequential limitations]
- **Recommendation / next step:** [what should happen next]

## 2. Context and data provenance

- Source, URL, DOI and access date:
- Data owner / collector:
- Original purpose of collection:
- Population and geography:
- Observation period:
- License and usage restrictions:
- Data transformations already applied by the source:
- Known exclusions and selection mechanisms:

## 3. Unit of observation and data model

- What does one row represent?
- Candidate key / primary key:
- Is the key unique? Evidence:
- Is the dataset event-level, user-level, transaction-level, panel, snapshot or aggregate?
- Which entities and tables exist?
- What joins are required? Can joins multiply rows?
- Are repeated observations expected or erroneous?

## 4. Prediction-time contract (for ML tasks)

- Prediction moment:
- Target definition:
- Target horizon / label window:
- Label maturation delay:
- Feature availability at prediction moment:
- Group boundary (user, account, device, session, etc.):
- Temporal ordering and split strategy:
- Potential leakage paths:

## 5. Data dictionary

Attach the completed `EDA_Data_Dictionary_Template.csv` or an equivalent table. For each variable describe semantic meaning, physical type, unit, valid range, missing-value encoding, role and availability time.

## 6. Data quality audit

Report, with counts and denominators:

- Schema and type inconsistencies.
- Missing values and possible MCAR/MAR/MNAR mechanisms.
- Duplicate rows and duplicate keys.
- Invalid ranges and logical contradictions.
- Sentinel values and special codes.
- Category drift / rare levels.
- Date gaps, timezone assumptions and ordering.
- Join integrity and row multiplication.

For every issue state: **evidence → interpretation → proposed treatment → risk of treatment**. Do not silently clean data during EDA.

## 7. Univariate analysis

For each important variable:

- Distribution and summary statistics.
- Quantiles and robust measures.
- Skew, tails, zero mass and outliers.
- Category frequencies and cardinality.
- Confidence intervals / sampling uncertainty where meaningful.

## 8. Bivariate and multivariate analysis

- Research question for each comparison.
- Conditional distributions and segment sizes.
- Effect size and uncertainty.
- Nonlinear relationships and interactions.
- Confounding / Simpson's paradox risks.
- Multiple-comparison strategy.
- Alternative explanations.

## 9. Time, cohorts and repeated observations

- Time granularity and timezone.
- Trends, seasonality, autocorrelation and structural breaks.
- Cohort definitions and censoring.
- Repeated-measure or cluster structure.
- Whether IID assumptions are reasonable.

## 10. ML-oriented analysis (when applicable)

- Target distribution and label quality.
- Train/test overlap and distribution shift.
- Leakage audit.
- Validation split and why it matches deployment.
- Baseline definition and metrics.
- Error analysis by segment.
- Feature hypotheses (not yet proven improvements).
- Robustness / stability checks.

## 11. Findings register

| Finding | Evidence | Alternative explanation | Risk / limitation | Next test | Decision |
|---|---|---|---|---|---|
| [Finding 1] | [table / figure / statistic] | [alternative] | [risk] | [test] | [decision] |

## 12. Limitations and responsible interpretation

Discuss selection bias, measurement error, data age, external validity, confounding, fairness concerns, missing context, sample size and privacy/usage restrictions. Separate descriptive facts, predictive hypotheses and causal claims.

## 13. Conclusions and next steps

- What is supported by the evidence?
- What remains uncertain?
- What data or experiment would reduce uncertainty?
- What should not be concluded?

## 14. Reproducibility appendix

- Python version:
- Package versions / lockfile:
- Notebook and script versions:
- Random seeds:
- Data file checksums:
- Exact run instructions:
- Output artifacts:

## 15. References

List original dataset citation, data page, papers and documentation. Preserve required attribution and license notices.
