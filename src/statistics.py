import numpy as np
import pandas as pd
def baseline_kpis(df):
    n=len(df);d=int(df.defect.sum())
    return pd.DataFrame([{"records":n,"defects":d,"defect_rate":d/n if n else np.nan,
      "average_cycle_time_sec":df.cycle_time_sec.mean(),"average_vibration_mm_s":df.vibration_mm_s.mean(),
      "average_temperature_c":df.temperature_c.mean()}])
def pareto_by(df,category="machine_id"):
    x=df.groupby(category).defect.agg(defects="sum",records="count").reset_index().sort_values("defects",ascending=False)
    x["defect_rate"]=x.defects/x.records;x["cumulative_defect_share"]=x.defects.cumsum()/max(x.defects.sum(),1)
    return x
def subgroup_control_data(df,freq="D"):
    x=df.set_index("date").sort_index().resample(freq).defect.agg(defects="sum",samples="count").dropna()
    x["defect_rate"]=x.defects/x.samples.replace(0,np.nan);pbar=df.defect.mean()
    se=np.sqrt(pbar*(1-pbar)/x.samples.clip(lower=1))
    x["center_line"]=pbar;x["ucl"]=(pbar+3*se).clip(upper=1);x["lcl"]=(pbar-3*se).clip(lower=0)
    return x.reset_index()
