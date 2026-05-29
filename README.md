# Credit Scoring Business Understanding

## Basel II and Model Interpretability

The Basel II Accord emphasizes effective credit risk measurement and regulatory transparency within financial institutions. As a result, credit scoring models must be interpretable, well-documented, and auditable. Financial institutions need to clearly explain how predictions are generated, which variables influence risk decisions, and why borrowers are classified as high or low risk.

Interpretable models such as Logistic Regression with Weight of Evidence (WoE) are widely preferred because they support regulatory compliance, model governance, fairness assessment, and risk validation.

---

## Proxy Variables and Business Risks

In many real-world credit datasets, a direct default label is unavailable. Therefore, proxy variables such as severe delinquency, missed payments, or write-offs are used to approximate default behavior for supervised learning.

Although proxy variables enable model development, they introduce several business risks, including:

* inaccurate labeling,
* customer misclassification,
* regulatory concerns,
* biased predictions,
* poor lending decisions.

For this reason, proxy variables must be carefully designed, validated, and documented.

---

## Interpretable vs High-Performance Models

Credit scoring models involve a trade-off between interpretability and predictive performance.

### Interpretable Models

Examples:

* Logistic Regression
* Weight of Evidence (WoE)

Advantages:

* easy to explain,
* regulatory friendly,
* easier auditing and validation.

Limitations:

* lower predictive power for complex patterns.

### High-Performance Models

Examples:

* Gradient Boosting,
* XGBoost,
* Random Forest.

Advantages:

* higher predictive accuracy,
* better handling of nonlinear relationships.

Limitations:

* reduced transparency,
* difficult explainability,
* increased regulatory scrutiny.

In practice, financial institutions balance predictive performance with explainability, compliance, fairness, and operational risk requirements.
