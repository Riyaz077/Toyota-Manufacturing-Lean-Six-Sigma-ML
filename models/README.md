# Model artifacts
The training pipeline generates `defect_risk_model.joblib` locally after fitting. No fake pretrained model is included. Record feature schema, target definition, data version, split, metrics, package versions and training date. Never load untrusted joblib/pickle files. Consider Git LFS for large artifacts.
