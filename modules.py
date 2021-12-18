import pickle
import pandas as pd

# functions to be used by the routes

# retrieve all the names from the dataset and put them into a list
def get_names(source):
    names = []
    for row in source:
        # lowercase all the names for better searching
        name = row["name"].lower()
        names.append(name)
    return sorted(names)

# find the row that matches the id in the URL, retrieve name and photo
def get_actor(source, id):
    for row in source:
        if id == str( row["id"] ):
            name = row["name"]
            photo = row["photo"]
            # change number to string
            id = str(id)
            # return these if id is valid
            return id, name, photo
    # return these if id is not valid - not a great solution, but simple
    return "Unknown", "Unknown", ""

# find the row that matches the name in the form and retrieve matching id
def get_id(source, name):
    for row in source:
        # lower() makes the string all lowercase
        if name.lower() == row["name"].lower():
            id = row["id"]
            # change number to string
            id = str(id)
            # return id if name is valid
            return id
    # return these if id is not valid - not a great solution, but simple
    return "Unknown"


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