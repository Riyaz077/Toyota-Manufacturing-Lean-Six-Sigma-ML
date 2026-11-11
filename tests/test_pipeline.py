from src.data_generator import generate_demo_data
from src.preprocessing import clean_data,add_time_features
from src.statistics import baseline_kpis,pareto_by
from src.modeling import train_model
def test_smoke():
    df=clean_data(generate_demo_data(n=800,seed=11));feat=add_time_features(df)
    assert 0<=baseline_kpis(df).defect_rate.iloc[0]<=1
    assert not pareto_by(df).empty
    model,metrics,cm,features=train_model(feat)
    assert "f1" in metrics and features
