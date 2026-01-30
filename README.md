# Criteo Marketing Uplift Modeling  
## A/B Testing + Causal Uplift Learners

This project analyzes causal impact in digital marketing using the **Criteo Uplift Prediction Dataset** (randomized treatment-control experiment).

It combines:

- **Population-level impact measurement (A/B testing)**
- **Individual-level treatment effect estimation (uplift modeling)**

The objective is to build a targeting model that ranks users by **incremental conversion effect**, enabling budget-efficient campaign prioritization.

---

# 1️⃣ Part I — A/B Testing (Average Treatment Effect)

## Power Analysis

Power analysis indicates that detecting the minimum detectable effect (MDE) at:

- α = 0.05  
- Power = 0.80  

requires approximately **0.85M users per arm**.

The dataset contains:

- 11.88M treated users  
- 2.10M control users  

Both exceed the required sample size, indicating that the hypothesis tests are well-powered.

---

## Statistical Validation

### Two-Sample Z-Test
- Null hypothesis: Equal conversion rates  
- Result: p < 0.05  
- Z-statistic > 0 (p₁ > p₀)  

Conclusion: The treatment significantly increases conversion rate.

---

### Permutation Test (Non-parametric Robustness)

- Treatment labels shuffled repeatedly while preserving group sizes  
- Empirical p-value ≈ 0.00  

Conclusion: The result remains statistically significant without relying on parametric assumptions.

---

### Bootstrap Confidence Interval

- 95% percentile confidence interval computed via resampling within each arm  
- Confidence interval entirely positive  

Conclusion: The treatment effect is statistically significant at the 5% level.

---

## Practical Significance

- Lower bound of 95% CI: **0.001085**
- Absolute MDE: **0.00019376**

Since the lower bound exceeds the MDE, the lift is both:

- Statistically significant  
- Practically meaningful  

---

# 2️⃣ Part II — Uplift Modeling (Treatment Effect Heterogeneity)

While A/B testing measures average treatment effect (ATE), uplift modeling estimates:

\[
\tau(x) = \mathbb{E}[Y \mid X=x, T=1] - \mathbb{E}[Y \mid X=x, T=0]
\]

An end-to-end uplift workflow was implemented:

- Data preprocessing  
- Model training  
- Model comparison  
- Ranking-based evaluation  
- Visualization  

---

## Implemented Uplift Learners

- **S-Learner**
- **T-Learner**
- **DR-Learner (Doubly Robust)**
- **X-Learner**
- **R-Learner**

These span standard meta-learners and residualized/doubly-robust causal estimators.

---

# Evaluation Metrics

## Uplift Curve + AUUC

Measures cumulative incremental outcomes when targeting users ranked by predicted uplift.

Metric reported:
- **Normalized AUUC (`uplift_auc_score`)**

---

## Qini Curve + Qini Coefficient

Measures incremental gain relative to a random targeting baseline.

Metric reported:
- **Normalized Qini AUC (`qini_auc_score`)**

---

# Results (Normalized Metrics)

| Model       | AUUC    | Qini Coefficient |
|------------|---------|------------------|
| S-Learner  | 0.00074 | 0.076            |
| T-Learner  | 0.00156 | 0.156            |
| DR-Learner | 0.00093 | 0.099            |
| X-Learner  | 0.00159 | 0.165            |
| R-Learner  | 0.00146 | 0.152            |

---

# Key Insights

- **X-Learner and T-Learner** achieved the strongest uplift ranking performance.
- R-Learner performed competitively.
- Strong early lift (top 10–20%) indicates effective identification of high-impact users.
- Models are particularly useful under **budget-constrained targeting scenarios**.

---

# Business Interpretation

If only the top 20% of users (ranked by predicted uplift) are targeted:

- Campaign focuses on users with highest incremental effect.
- Marketing budget is allocated efficiently.
- Reduces treatment of users unlikely to respond.

This demonstrates how causal modeling improves decision-making beyond average treatment effect estimation.

---

# Dataset

**Criteo Uplift Prediction Dataset**

Randomized marketing experiment with:

- `X` → user features  
- `T` → treatment indicator (0 = control, 1 = treated)  
- `Y` → conversion outcome  

---

# Repository Structure


Includes:

- Power analysis  
- Two-sample Z-test  
- Permutation test  
- Bootstrap confidence intervals  
- Implementation of S / T / DR / X / R learners  
- Uplift and Qini curves  
- Normalized AUUC and Qini reporting  

---

# Project Focus

- Causal inference  
- Treatment effect estimation  
- Uplift modeling  
- Ranking-based targeting  
- Statistical validation  
- Marketing optimization  

---

# Author

Rahul Bharti  
M.Tech Data Analytics
