import sys
import os
import shutil
import time
import traceback
import pickle
from pathlib import Path

from flask import Flask, request, jsonify, render_template
import pandas as pd

app = Flask(__name__)

# inputs
training_data = "data/titanic.csv"
include = ["Age", "Sex", "Embarked", "Survived"]
dependent_variable = include[-1]

model_filename = "model/titanic_model.pkl"
model_columns_filename = "model/titanic_model_columns.pkl"

# These will be populated at training time
model_columns = None
clf = None


@app.route("/")
def index():
    """Index for the app, this will be at the root of the API
    """
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    """Endpoint for the prediction of the model
    
    To make a prediction, the user needs to pass a json object
    """
    if clf:
        try:
            json_ = request.json
            query = pd.get_dummies(pd.DataFrame(json_))

            query = query.reindex(columns=model_columns, fill_value=0)

            prediction = list(clf.predict(query))

            # Converting to int from int64
            return jsonify({"prediction": list(map(int, prediction))})

        except Exception as e:

            return jsonify({"error": str(e), "trace": traceback.format_exc()})
    else:
        print("Please make sure you have trained your model")
        return "no model here"


@app.route("/train", methods=["GET"])
def train():
    """ 
    Endpoint used to train the model, this is only one way to do this, 
    a more common approach is that you might need to traqin your model and then 
    serialise it or persist it somewhere else"""

    # using random forest as an example
    # can do the training separately and just update the pickles
    from sklearn.ensemble import RandomForestClassifier as rf

    df = pd.read_csv(training_data)
    df_ = df[include]

    categoricals = []  # going to one-hot encode categorical variables

    for col, col_type in df_.dtypes.items():
        if col_type == "O":
            categoricals.append(col)
        else:
            df_[col].fillna(
                0, inplace=True
            )  # fill NA's with 0 for ints/floats, too generic

    # get_dummies effectively creates one-hot encoded variables
    df_ohe = pd.get_dummies(df_, columns=categoricals, dummy_na=True)

    x = df_ohe[df_ohe.columns.difference([dependent_variable])]
    y = df_ohe[dependent_variable]

    # capture a list of columns that will be used for prediction
    global model_columns
    model_columns = list(x.columns)
    with open(model_columns_filename, "wb") as f:
        pickle.dump(model_columns, f)

    global clf
    clf = rf()
    start = time.time()
    clf.fit(x, y)

    with open(model_filename, "wb") as f:
        pickle.dump(clf, f)

    message1 = f"Trained in {time.time()-start} seconds"
    message2 = f"Model training score: {clf.score(x,y)}"
    return_message = "Success. \n{0}. \n{1}.".format(message1, message2)
    return return_message


@app.route("/wipe", methods=["GET"])
def wipe():
    """ Endpoint to delete the pickle files for the model and the column names"""
    try:
        shutil.rmtree(model_path)
        os.makedirs(model_path)
        return "Model wiped"

    except Exception as e:
        print(str(e))
        return "Could not remove and recreate the model directory"


if __name__ == "__main__":
    try:
        port = int(sys.argv[1])
    except Exception as e:
        port = 80

    try:
        clf = pickle.load(model_filename)
        print("Model loaded")
        model_columns = pickle.load(model_columns_filename)
        print("Model columns loaded")

    except Exception as e:
        print("Oops! No model here")
        print("Please train your model first")
        print(str(e))
        clf = None

    app.run(host="0.0.0.0", port=port, debug=True)

