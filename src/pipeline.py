import argparse
from pathlib import Path
import pandas as pd
from src.data_generator import save_demo_data
from src.preprocessing import clean_data,add_time_features
from src.statistics import baseline_kpis,pareto_by,subgroup_control_data
from src.modeling import train_model,save_model
def run(input_path="data/generated/manufacturing_demo.csv",generate_demo=False):
    if generate_demo or not Path(input_path).exists():save_demo_data(input_path)
    clean=clean_data(pd.read_csv(input_path));feat=add_time_features(clean)
    model,metrics,cm,features=train_model(feat);save_model(model,features)
    feat["predicted_defect_probability"]=model.predict_proba(feat[features])[:,1]
    feat["predicted_defect"]=model.predict(feat[features])
    Path("results").mkdir(exist_ok=True)
    baseline_kpis(clean).to_csv("results/baseline_kpis.csv",index=False)
    pareto_by(clean).to_csv("results/pareto_defects.csv",index=False)
    pd.DataFrame([metrics]).to_csv("results/model_metrics.csv",index=False)
    feat.to_csv("results/scored_manufacturing_records.csv",index=False)
    subgroup_control_data(clean).to_csv("results/control_chart_data.csv",index=False)
    print("Pipeline complete. Metrics:",metrics,"\nSynthetic demonstration only.")
    return clean,feat,metrics,cm
if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--generate-demo",action="store_true");p.add_argument("--input",default="data/generated/manufacturing_demo.csv");a=p.parse_args();run(a.input,a.generate_demo)
