from pathlib import Path
import numpy as np
import pandas as pd

def generate_demo_data(n=5000, seed=42):
    rng=np.random.default_rng(seed)
    dates=pd.date_range("2025-01-01",periods=n,freq="15min")
    shift=rng.choice(["A","B","C"],n); line=rng.choice(["Line-1","Line-2","Line-3"],n)
    machine=rng.choice(["M-01","M-02","M-03","M-04"],n)
    exp=rng.integers(1,121,n); temp=rng.normal(185,8,n); pressure=rng.normal(6,.55,n)
    cycle=rng.normal(54,6,n)+(line=="Line-3")*2
    vibration=np.abs(rng.normal(3.1,1.2,n)); wear=np.clip(rng.normal(120,55,n),0,300)
    logit=-3.2+.018*np.abs(temp-185)+.48*np.maximum(pressure-6.6,0)+.075*np.maximum(vibration-4,0)+.004*np.maximum(wear-150,0)+.008*np.maximum(cycle-60,0)-.003*np.minimum(exp,60)
    prob=1/(1+np.exp(-logit)); defect=rng.binomial(1,prob)
    idx=rng.choice(n,size=max(10,n//100),replace=False); vibration[idx]=rng.uniform(8,13,len(idx)); defect[idx]=1
    return pd.DataFrame({"date":dates,"shift":shift,"line":line,"machine_id":machine,
      "operator_experience_months":exp,"temperature_c":temp.round(2),"pressure_bar":pressure.round(2),
      "cycle_time_sec":cycle.round(2),"vibration_mm_s":vibration.round(2),"tool_wear_hours":wear.round(1),
      "material_batch":[f"B{x:04d}" for x in rng.integers(1,300,n)],"defect":defect,"synthetic_data":True})

def save_demo_data(path="data/generated/manufacturing_demo.csv",**kwargs):
    p=Path(path);p.parent.mkdir(parents=True,exist_ok=True);df=generate_demo_data(**kwargs);df.to_csv(p,index=False);return df
