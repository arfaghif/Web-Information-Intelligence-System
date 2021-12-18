import pickle
import pandas as pd

# functions to be used by the routes

def get_desc_cluster(num_label):
    df = pd.read_csv("desc_cluster.csv")
    return round(df.iloc[num_label]["days_since_last_purchase"],1), round(df.iloc[num_label]["frequency"],1), round(df.iloc[num_label]["amount"],1), df.iloc[num_label]["TotalCustomer"], df.iloc[num_label]["label"]

def predict_cluster(normalized_data):
    # load the model from disk
    seg_cluster = pickle.load(open("seg_cluster.sav", 'rb'))
    # predict
    result = seg_cluster.predict(normalized_data)
    return result

def minmax_scaler(days, freq, amount):
    # load the model from disk
    scaler = pickle.load(open("minmax_scaler.sav", 'rb'))
    # predict
    data = [[days, freq, amount]]
    data = scaler.transform(data)
    return data

def search(name):
    a_set = set()
    df = pd.read_csv("rules_fp.csv")
    df_match = df.loc[df['antecedents'].str.contains(name, case=False)]
    for i in range(len(df_match)):
        a_set.add(df_match.iloc[i]['antecedents'])
        a_set.add(df_match.iloc[i]['consequents'])
    return list(a_set)
