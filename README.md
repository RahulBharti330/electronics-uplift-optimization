# Criteo Marketing Uplift Modeling (A/B Testing + Uplift Learners)

This project explores **causal impact measurement** in marketing using the **Criteo Uplift Prediction dataset**. It combines:

1) **A/B testing** to quantify the average treatment effect (ATE) on conversion rate, and  
2) **uplift modeling** to predict *who benefits most* from treatment (heterogeneous / individual treatment effects).

The end goal is to build a targeting model that ranks users by **incremental effect**, so a marketing campaign can prioritize the users most likely to be influenced by the intervention.

---

## Project Highlights

### Part 1 — A/B Testing (Conversion Lift)

**Power analysis**
- Power analysis indicates that if the true conversion lift is at least the **minimum detectable effect (MDE)**, then we need approximately **0.85M users per arm** to achieve **α = 0.05** and **power = 0.80**.
- The dataset contains **11.88M treated users** and **2.10M control users**, exceeding the minimum required in both groups. Therefore, the hypothesis test is **well powered**.

**Hypothesis tests and uncertainty quantification**
- **Two-sample Z-test (conversion rates)**
  - With **p < 0.05**, we reject the null hypothesis of equal conversion rates.
  - The Z-statistic is positive (**p₁ > p₀**), implying a higher conversion rate in the treatment group.
- **Permutation test (non-parametric robustness check)**
  - Treatment labels were repeatedly shuffled (keeping group sizes fixed), recomputing the conversion-rate difference each time.
  - The permutation p-value is the fraction of permuted differences at least as extreme as the observed difference.
  - Since **p ≈ 0.00 < 0.05**, the lift is statistically significant and consistent with the Z-test conclusion.
- **Bootstrap confidence interval**
  - Computed a **95% bootstrap percentile CI** for the conversion-rate lift by resampling users with replacement within each arm and recomputing **p₁ − p₀** across *B* replicates.
  - Since **0 is not contained in the CI**, the lift is statistically significant at the 5% level.
  - The interval is entirely positive, reinforcing that the treatment group’s conversion rate is higher.

**Practical significance**
- The **lower bound of the CI** is **0.001085**, which exceeds the absolute **MDE = 0.00019376**.
- Therefore, the observed lift is not only statistically significant but also **practically meaningful**.

**Summary**
- The Z-test, permutation test, and bootstrap CI provide **consistent evidence** that treatment increases conversion rate.
- The lift also passes a **practical significance** threshold based on the MDE.

---

### Part 2 — Uplift Modeling (Who to Target)

- Implemented an end-to-end uplift modeling workflow: data preparation, model training, evaluation, and visualization.
- Trained and compared multiple uplift learners:
  - **S-Learner**
  - **T-Learner**
  - **DR-Learner (Doubly Robust)**
  - **X-Learner**
  - **R-Learner**
- Evaluated models using uplift-specific ranking metrics:
  - **AUUC** (normalized Area Under the Uplift Curve)
  - **Qini coefficient** (normalized Area Under the Qini Curve)
- Across models, the uplift/Qini curves generally show a **steep initial slope in the top 10–20%** of ranked users, indicating strong ability to identify a high-treatment-effect segment. This is particularly valuable in budget-constrained targeting where only a small fraction of users can be treated.

---

## Dataset

- **Criteo Uplift Prediction Dataset** (randomized marketing treatment/control experiment)
- Typical fields:
  - `X`: user features  
  - `T`: treatment indicator (0 = control, 1 = treated)  
  - `Y`: outcome (conversion)

---

## Methodology

### 1) A/B Testing (Population-Level Impact)
- Estimated the **Average Treatment Effect (ATE)** on conversion rate:
  \[
  \text{ATE} = \mathbb{E}[Y \mid T=1] - \mathbb{E}[Y \mid T=0]
  \]
- Validated statistical significance using:
  - two-sample Z-test for difference in proportions
  - permutation test for a distribution-free robustness check
  - bootstrap confidence interval for uncertainty estimation
- Assessed **practical significance** by comparing the CI to the **MDE**.

### 2) Uplift Modeling (Individual / Segment-Level Impact)

Trained multiple uplift learners to estimate treatment effect heterogeneity:

- **S-Learner**: one model predicts `Y` using `(X, T)`, uplift is the difference between predicted outcomes under `T=1` vs `T=0`.
- **T-Learner**: two outcome models `m₁(X)` and `m₀(X)` trained separately on treated and control groups.
- **DR-Learner**: combines outcome models and propensity estimates to form a doubly robust uplift signal.
- **X-Learner**: uses imputed treatment effects and two uplift regressors, often effective under imbalance or low treatment signal.
- **R-Learner**: residualizes both outcome and treatment using nuisance models, then fits a weighted regression to estimate uplift.

---

## Evaluation Metrics

### Uplift Curve + AUUC
- Measures cumulative incremental outcomes as we target users from highest predicted uplift to lowest.
- **AUUC** is reported as **normalized AUUC** (`uplift_auc_score`).

### Qini Curve + Qini Coefficient
- Measures incremental gain relative to a random targeting baseline.
- **Qini coefficient** is reported as **normalized Qini AUC** (`qini_auc_score`).

---

## Results (Normalized AUUC and Qini)

| Model       | AUUC     | Qini Coef. |
|------------|----------:|-----------:|
| S-Learner  | 0.00074   | 0.076      |
| T-Learner  | 0.00156   | 0.156      |
| DR-Learner | 0.00093   | 0.099      |
| X-Learner  | 0.00159   | 0.165      |
| R-Learner  | 0.00146   | 0.152      |

**Key takeaways**
- **X-Learner and T-Learner** achieved the strongest overall uplift ranking performance, with **R-Learner** close behind.
- **DR-Learner** improved over the S-Learner baseline but did not match the top performers in this run.
- The consistently strong early lift (top 10–20%) suggests the models are effective for **prioritized targeting** under limited campaign budget.

---

## Repository Structure

- `uplift_model.ipynb` — main notebook containing:
  - dataset preparation
  - A/B testing analysis (power analysis, Z-test, permutation test, bootstrap CI, practical significance)
  - uplift model training (S / T / DR / X / R learners)
  - evaluation plots (uplift curve, Qini curve)
  - normalized AUUC / Qini reporting