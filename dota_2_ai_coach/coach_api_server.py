"""
This is the coach API server.

It is ready to run as a cloudfroundry deployment, 
just change the "run_locally" variable to "False". 

The response messages are all formated in JSON.

The API endpoints are following routes:
    / :              
        a welcome message
    /match_ids : 
        returns all available match IDs
    /first_blood/<match_id> : 
        returns the first blood event of the given match_id
    /kill_sequences/<match_id> :
        returns all kill sequences of the given match_id
    /intensity/<match_id> :
        returns the intensity series of the given match_id
    /match_duration/<match_id> :
        returns the match duration of the given match_id
"""

import identify_kill_sequences
from flask import Flask, make_response
import os
import json

import pandas as pd
import hana_connector

import identify_first_blood
from coach import query_intensity


# If this api is not deployed on cloudfoundry make sure that run_locally is
# set to True, it will run on localhost:5000
run_locally = True

# Create the application instance
app = Flask(__name__)

if run_locally:
    port = 5000
else:
    port = int(os.getenv("PORT"))


# Create a URL route in our application for "/"
@app.route('/')
def home():
    """
    This function just responds to the root URL
    Return:  
        JSON HANA welcome Message
    """
    hana = hana_connector.HanaConnector()
    hana.connect()
    data_set, columns = hana.execute("SELECT 'Hello Python World' FROM DUMMY")
    response = make_response(json.dumps(data_set), 200)
    return response


@app.route('/pandas_example')
def pandas_example():
    """
    This Example function just responds to the URL
    host/pandas_example
    Returns: 
        an example Pandas Dataframe to Json
    """
    welcome = pd.DataFrame(["Hello", "World"])
    response = make_response(welcome.to_json(orient="values"), 200)
    return response


@app.route('/first_blood/<match_id>')
def get_first_blood(match_id):
    """
    Finds the first blood event in a given match_id
    Responds for example to localhost:5000/first_blood/4074440208
    Args:
        match_id: id of a match in database
    Returns:
        JSON records with scene start, end time, attacker and target
        if match_id can't be found returns JSON with "match_id Not Found"
    """
    first_blood_df = identify_first_blood.first_blood(match_id)
    if not first_blood_df.empty:
        response = make_response(first_blood_df.to_json(orient="records"), 200)
    else:
        response = make_response("{match_id Not Found}", 404)
    return response


@app.route('/kill_sequences/<match_id>')
def get_kill_sequences(match_id):
    """
    Finds the kill sequencs where at least 3 heroes were killed in 18 seconds
    Responds for example to  localhost:5000/kill_sequences/4074440208
    Args:
        match_id: id of a match in database
    Returns:
        JSON records of scene start, end time,
        if match_id can't be found returns JSON with "match_id Not Found"
    """
    kill_sequences = identify_kill_sequences.get_kill_sequences(match_id)
    if not kill_sequences.empty:
        response = make_response(kill_sequences.to_json(orient="records"), 200)
    else:
        response = make_response("{match_id Not Found}", 404)
    return response


@app.route("/intensity/<match_id>")
def get_intensity(match_id):
    """
    Aggregates all meaningful match events into a match intensity time series
    Args:
        match_id: id of a match in database
    Returns:
        JSON records of Radiant and Dire and the time intervals
        if match_id can't be found returns JSON with "match_id Not Found"
    """
    intensity = query_intensity(match_id)
    if not intensity.empty:
        intensity_radiant = {
            "name": "Radiant",
            "objects": list(intensity[intensity["team_name"] == "Radiant"]["intensity_smoothed"])
        }
        intensity_dire = {
            "name": "Dire",
            "objects": list(intensity[intensity["team_name"] == "Dire"]["intensity_smoothed"])
        }
        seconds_interval = list(
            pd.Series(pd.unique(intensity["seconds_interval"])).sort_values())
        response = {
            "intensity_radiant": intensity_radiant,
            "intensity_dire": intensity_dire,
            "seconds_interval": seconds_interval
        }
        response = make_response(json.dumps(response), 200)
        response.headers.add('Access-Control-Allow-Origin', '*')
    else:
        response = make_response("{match_id Not Found}", 404)
    return response


@app.route("/match_duration/<match_id>")
def get_match_duration(match_id):
    """
    Gets the duration of the match
    Args:
        match_id: id of a match in database
    returns:
        JSON record of the match duration,
        if match_id can't be found returns JSON with "match_id Not Found"
    """
    hana = hana_connector.HanaConnector()
    connection = hana.connect()
    duration = pd.read_sql("""
    SELECT
        "duration"
    FROM
        "DOTA2_TI8"."matches"
    WHERE
        "match_id" = {match_id}
    """.format(match_id=match_id), connection)
    if not duration.empty:
        response = make_response(duration.to_json(orient="records"), 200)
    else:
        response = make_response("{match_id Not Found}", 404)
    return response


@app.route("/match_ids")
def get_match_ids():
    """
    Finds all available match_ids available in the database
    Returns:
        JSON array of all available match_ids,
        if no match can be found returns JSON with "No matches found"
    """
    hana = hana_connector.HanaConnector()
    connection = hana.connect()
    ids = pd.read_sql("""
    SELECT
        "match_id"
    FROM
        "DOTA2_TI8"."matches"
    ORDER BY
        "match_id"
        ASC
    """, connection)
    if not ids.empty:
        response = make_response(ids["match_id"].to_json(orient="values"), 200)
    else:
        response = make_response("{No Matches Found}", 404)
    return response


# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    if run_locally:
        app.run(debug=True)
    else:
        app.run(host='0.0.0.0', port=port, debug=False)
