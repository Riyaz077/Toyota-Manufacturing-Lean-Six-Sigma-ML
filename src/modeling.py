from pathlib import Path
import joblib
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder,StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score,precision_score,recall_score,f1_score,roc_auc_score,confusion_matrix
NUM=["operator_experience_months","temperature_c","pressure_bar","cycle_time_sec","vibration_mm_s","tool_wear_hours","hour","day_of_week","month"]
CAT=["shift","line","machine_id"]
def train_model(df,random_state=42):
    x=df.copy()
    if "hour" not in x:x["hour"]=x.date.dt.hour;x["day_of_week"]=x.date.dt.dayofweek;x["month"]=x.date.dt.month
    features=NUM+CAT;X=x[features];y=x.defect.astype(int)
    if y.nunique()<2:raise ValueError("Need both defect classes.")
    num=Pipeline([("imputer",SimpleImputer(strategy="median")),("scale",StandardScaler())])
    cat=Pipeline([("imputer",SimpleImputer(strategy="most_frequent")),("onehot",OneHotEncoder(handle_unknown="ignore"))])
    prep=ColumnTransformer([("num",num,NUM),("cat",cat,CAT)])
    pipe=Pipeline([("prep",prep),("rf",RandomForestClassifier(n_estimators=250,min_samples_leaf=3,class_weight="balanced",random_state=random_state,n_jobs=-1))])
    Xtr,Xte,ytr,yte=train_test_split(X,y,test_size=.25,random_state=random_state,stratify=y)
    pipe.fit(Xtr,ytr);pred=pipe.predict(Xte);proba=pipe.predict_proba(Xte)[:,1]
    metrics={"accuracy":accuracy_score(yte,pred),"precision":precision_score(yte,pred,zero_division=0),"recall":recall_score(yte,pred,zero_division=0),"f1":f1_score(yte,pred,zero_division=0),"roc_auc":roc_auc_score(yte,proba)}
    return pipe,metrics,confusion_matrix(yte,pred).tolist(),features
def save_model(model,features,path="models/defect_risk_model.joblib"):
    Path(path).parent.mkdir(parents=True,exist_ok=True);joblib.dump({"pipeline":model,"features":features},path)
