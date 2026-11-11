import pandas as pd
REQUIRED=["date","shift","line","machine_id","temperature_c","pressure_bar","cycle_time_sec","vibration_mm_s","tool_wear_hours","defect"]
NUMERIC=["operator_experience_months","temperature_c","pressure_bar","cycle_time_sec","vibration_mm_s","tool_wear_hours","defect"]
def clean_data(df):
    missing=[c for c in REQUIRED if c not in df]
    if missing: raise ValueError(f"Missing columns: {missing}")
    x=df.copy();x["date"]=pd.to_datetime(x["date"],errors="coerce")
    for c in NUMERIC:
        if c in x:x[c]=pd.to_numeric(x[c],errors="coerce")
    x=x.dropna(subset=REQUIRED).drop_duplicates().sort_values("date").reset_index(drop=True)
    x["defect"]=x["defect"].astype(int)
    if not set(x.defect.unique()).issubset({0,1}): raise ValueError("defect must be binary 0/1")
    return x
def add_time_features(df):
    x=df.copy();x["hour"]=x.date.dt.hour;x["day_of_week"]=x.date.dt.dayofweek;x["month"]=x.date.dt.month
    return x
