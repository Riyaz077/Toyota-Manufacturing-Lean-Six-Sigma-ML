from pathlib import Path
import pandas as pd
import streamlit as st
import plotly.express as px
st.set_page_config(page_title="Lean Six Sigma Manufacturing Analytics",page_icon="🏭",layout="wide")
st.title("Toyota Manufacturing Process Improvement")
st.caption("Lean Six Sigma DMAIC • Statistical quality analysis • Defect-risk modeling")
up=st.sidebar.file_uploader("Upload authorized manufacturing CSV",type=["csv"]);p=Path("results/scored_manufacturing_records.csv")
if up:df=pd.read_csv(up)
elif p.exists():df=pd.read_csv(p)
else:st.info("Run `python -m src.pipeline --generate-demo` first.");st.stop()
need={"date","machine_id","defect","cycle_time_sec","vibration_mm_s","predicted_defect_probability"}
if not need.issubset(df.columns):st.error(f"Missing columns: {need-set(df.columns)}");st.stop()
df["date"]=pd.to_datetime(df.date,errors="coerce");st.sidebar.warning("Bundled demo data is synthetic.")
machines=["All"]+sorted(df.machine_id.dropna().unique());m=st.sidebar.selectbox("Machine",machines);v=df if m=="All" else df[df.machine_id==m]
a,b,c,d=st.columns(4);a.metric("Records",f"{len(v):,}");b.metric("Defect rate",f"{v.defect.mean()*100:.2f}%");c.metric("Avg cycle time",f"{v.cycle_time_sec.mean():.1f} sec");d.metric("High predicted risk",int((v.predicted_defect_probability>=.5).sum()))
t1,t2,t3,t4=st.tabs(["Overview","DMAIC & Pareto","Defect prediction","Process control"])
with t1:
    metric=st.selectbox("Process metric",["cycle_time_sec","temperature_c","pressure_bar","vibration_mm_s"])
    st.plotly_chart(px.line(v.sort_values("date"),x="date",y=metric,color="line"),use_container_width=True)
with t2:
    p=v.groupby("machine_id").defect.agg(["sum","count"]).reset_index().rename(columns={"sum":"defects","count":"records"}).sort_values("defects",ascending=False)
    st.plotly_chart(px.bar(p,x="machine_id",y="defects",title="Defects by machine"),use_container_width=True)
    st.write("Define CTQ → Measure baseline → Analyze validated causes → Improve with an approved pilot → Control with KPI ownership.")
with t3:
    st.plotly_chart(px.histogram(v,x="predicted_defect_probability",color="defect",nbins=30),use_container_width=True)
    st.dataframe(v.sort_values("predicted_defect_probability",ascending=False).head(100),use_container_width=True)
with t4:
    cp=Path("results/control_chart_data.csv")
    if cp.exists():
        z=pd.read_csv(cp);z["date"]=pd.to_datetime(z.date)
        st.plotly_chart(px.line(z,x="date",y=["defect_rate","center_line","ucl","lcl"]),use_container_width=True)
    else:st.info("Run pipeline first.")
st.download_button("Download data CSV",v.to_csv(index=False).encode(),file_name="manufacturing_analysis.csv")
st.caption("Synthetic educational case study. Prediction is not causal proof.")
