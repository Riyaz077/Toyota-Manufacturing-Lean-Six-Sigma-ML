# Toyota Manufacturing Process Improvement Using Lean Six Sigma and Machine Learning

An educational manufacturing-quality analytics project combining DMAIC, statistical process analysis, and machine learning to explore process variation and defect risk.

> **Important data note:** This package uses a synthetic manufacturing dataset generator. It is NOT Toyota production data and must not be presented as a real Toyota factory study. Company-specific findings, savings, defect reductions, or process improvements require authorized, traceable factory data and independent validation.

## DMAIC workflow
- **Define:** problem statement, scope, CTQs, stakeholders, SIPOC and project charter.
- **Measure:** data validation, operational defect definition, baseline defect rate and process distributions.
- **Analyze:** Pareto, stratification, correlation, assumption-checked statistical tests and predictive patterns.
- **Improve:** validated countermeasures, approved pilot and before/after evaluation.
- **Control:** KPI owners, control charts, standard work, audits and reaction plan.

## Capabilities
- Manufacturing data validation and feature preparation
- Baseline quality KPIs and Pareto analysis
- Random Forest defect-risk classification
- Daily defect-rate monitoring (illustrative p-chart calculations)
- Streamlit dashboard and CSV outputs
- Notebook, report, methodology, architecture and presentation

## Quick start
```bash
pip install -r requirements.txt
python -m src.pipeline --generate-demo
streamlit run app.py
```

## Repository layout
```text
config/ data/ docs/ models/ notebooks/ presentation/ results/ screenshots/ src/ tests/
app.py  README.md  requirements.txt  LICENSE  .gitignore
```

## Demo data fields
date, shift, line, machine_id, operator_experience_months, temperature_c, pressure_bar, cycle_time_sec, vibration_mm_s, tool_wear_hours, material_batch, defect.

The simulated process relationships are illustrative and do not describe Toyota's actual operating parameters.

## Evaluation
Classification: precision, recall, F1, ROC-AUC and confusion matrix. Statistical process analysis: baseline defect rate, Pareto and subgroup defect-rate monitoring. Capability indices such as Cp/Cpk require valid specification limits and a stable process; do not calculate them from arbitrary demo limits.

## Responsible interpretation
Prediction and feature importance do not prove causation. Validate root causes with manufacturing engineers and quality specialists. Do not change safety-critical process settings based solely on model output.

Author: Mohamed Riyaz S. | VIT Chennai
