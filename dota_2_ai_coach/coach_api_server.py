import identify_kill_sequences
from flask import Flask, make_response
import os
import json

import pandas as pd
import hana_connector

import identify_first_blood

"""
if this api should be run not on  cloudfoundry make sure that run_localy is
set to True, it will run on localhost:5000
"""
run_localy = False

# Create the application instance
app = Flask(__name__)

if run_localy:
    port = 5000
else:
    port = int(os.getenv("PORT"))


# Create a URL route in our application for "/"
@app.route('/')
def home():
    """
    This function just responds to the root URL
    return:  json HANA welcome Message
    """
    hana = hana_connector.HanaConnector()
    hana.connect()
    data_set, columns = hana.execute("SELECT 'Hello Python World' FROM DUMMY")
    hana.close()
    response = make_response(json.dumps(data_set), 200)
    return response


@app.route('/pandas_example')
def pandas_example():
    """
    This Example function just responds to the URL
    localhost:5000/pandas_example
    return: an example Pandas Dataframe to Json
    """
    welcome = pd.DataFrame(["Hello", "World"])
    response = make_response(welcome.to_json(orient="values"), 200)
    return response


@app.route('/first_blood/<matchID>')
def get_first_blood(matchID):
    """
    Finds the first blood event in a given matchID 
    Responds for example to  localhost:5000/first_blood/4074440208
    returns: 
        a record of with a scene start, end time, attacker and target
        if matchID can't be found returns Json with "MatchID Not Found"
    """
    first_blood_df = identify_first_blood.first_blood(matchID)
    if not first_blood_df.empty:
        response = make_response(first_blood_df.to_json(orient="records"), 200)
    else:
        response = make_response("{MatchID Not Found}", 404)
    return response


@app.route('/kill_sequences/<matchID>')
def get_kill_sequences(matchID):
    """
    Finds the kill sequencs where at least 3 heroes were kille in 18 seconds 
    Responds for example to  localhost:5000/kill_sequences/4074440208
    returns: 
        a record of with a scene start, end time,
        if matchID can't be found returns Json with "MatchID Not Found"
    """
    kill_sequences = identify_kill_sequences.get_kill_sequences(matchID)
    if not kill_sequences.empty:
        response = make_response(kill_sequences.to_json(orient="records"), 200)
    else:
        response = make_response("{MatchID Not Found}", 404)
    return response


# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    if run_localy:
        app.run(debug=True)
    else:
        app.run(host='0.0.0.0', port=port, debug=False)
