# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
#imports
import joblib
from flask import render_template, redirect, request, url_for, render_template, jsonify
import requests
import plotly.graph_objects as go
import glob
import os
import json
import pandas as pd
import matplotlib.pyplot as plt
from flask_login import (
    current_user,
    login_user,
    logout_user
)
from flask_dance.contrib.github import github
from sympy.physics.optics import deviation
from apps import db, login_manager
from apps.authentication import blueprint
from apps.authentication.forms import LoginForm, CreateAccountForm
from apps.authentication.models import Users
from apps.authentication.util import verify_pass


@blueprint.route('/')
def route_default():
    return redirect(url_for('authentication_blueprint.login'))

# Login & Registration

@blueprint.route("/github")
def login_github():
    """ Github login """
    if not github.authorized:
        return redirect(url_for("github.login"))

    res = github.get("/user")
    return redirect(url_for('home_blueprint.index'))
    
@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm(request.form)
    if 'login' in request.form:

        # read form data
        username = request.form['username']
        password = request.form['password']

        # Locate user
        user = Users.query.filter_by(username=username).first()

        # Check the password
        if user and verify_pass(password, user.password):

            login_user(user)
            return redirect(url_for('authentication_blueprint.route_default'))

        # Something (user or pass) is not ok
        return render_template('accounts/login.html',
                               msg='Wrong user or password',
                               form=login_form)

    if not current_user.is_authenticated:
        return render_template('accounts/login.html',
                               form=login_form)
    return redirect(url_for('home_blueprint.index'))


@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    create_account_form = CreateAccountForm(request.form)
    if 'register' in request.form:

        username = request.form['username']
        email = request.form['email']

        # Check usename exists
        user = Users.query.filter_by(username=username).first()
        if user:
            return render_template('accounts/register.html',
                                   msg='Username already registered',
                                   success=False,
                                   form=create_account_form)

        # Check email exists
        user = Users.query.filter_by(email=email).first()
        if user:
            return render_template('accounts/register.html',
                                   msg='Email already registered',
                                   success=False,
                                   form=create_account_form)

        # else we can create the user
        user = Users(**request.form)
        db.session.add(user)
        db.session.commit()

        # Delete user from session
        logout_user()
        
        return render_template('accounts/register.html',
                               msg='Account created successfully.',
                               success=True,
                               form=create_account_form)

    else:
        return render_template('accounts/register.html', form=create_account_form)

#dataframe display function
@blueprint.route('/data')
def display_data():
    data_folder = os.path.dirname(os.path.abspath(__file__))
    filename = 'flask_data_no_encoder.csv'
    file_path = os.path.join(data_folder, filename)

    # Read the CSV file into a Pandas DataFrame
    df = pd.read_csv(file_path)

    # Convert the DataFrame to an HTML table
    table_html = df.to_html(classes='table table-striped table-bordered')

    return render_template('DataFrame/DisplayDataFrame.html', table_html=table_html)

#logout function
@blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('authentication_blueprint.login'))


#display blogs function
@blueprint.route('/blogs')
def get_blogs():
    topic = "Automotive Industry"

    try:
        wikipedia_api = f"https://en.wikipedia.org/w/api.php?action=query&format=json&list=search&srsearch={topic}&utf8="
        response = requests.get(wikipedia_api)
        response.raise_for_status()

        data = response.json()
        blog_data = data['query']['search'][:5]  # Limit to first 5 search results

        blogs = []
        for item in blog_data:
            title = item['title']
            url = f"https://en.wikipedia.org/wiki/{title}"

            # Fetch snippet from the Wikipedia API for each Blogs
            snippet_api = f"https://en.wikipedia.org/w/api.php?action=query&format=json&prop=extracts&exintro&explaintext&titles={title}&utf8="
            snippet_response = requests.get(snippet_api)
            snippet_response.raise_for_status()

            snippet_data = snippet_response.json()
            page_id = list(snippet_data['query']['pages'].keys())[0]
            snippet = snippet_data['query']['pages'][page_id]['extract']

            blogs.append({
                'title': title,
                'url': url,
                'snippet': snippet
            })

        return render_template('Blogs/Blogs.html', blogs=blogs)
    except requests.exceptions.RequestException as e:
        return jsonify(error='Failed to fetch blogs'), 500

#Prediction function
@blueprint.route('/predict', methods=['GET','POST'])
def input_form():
    if request.method == 'POST':
        # Get the form data
        Deviation = int(request.form['Deviation'])
        Maneuver = int(request.form['Maneuver'])
        WeatherCondition = int(request.form['WeatherCondition'])
        ParkingGarage = int(request.form['ParkingGarage'])
        ArtificialLight = int(request.form['ArtificialLight'])
        DynamicObjects = int(request.form['DynamicObjects'])
        DirectionChange = int(request.form['DirectionChange'])
        LightCondition = int(request.form['LightCondition'])
        ParkingManeuver = int(request.form['ParkingManeuver'])
        Seasons = int(request.form['Seasons'])
        StaticObjects = int(request.form['StaticObjects'])
        Location = int(request.form['Location'])
        VID_START_FRAME = int(request.form['VID_START_FRAME'])
        VID_START_ELV = float(request.form['VID_START_ELV'])
        VID_START_LAT = float(request.form['VID_START_LAT'])
        VID_START_LNG = float(request.form['VID_START_LNG'])
        VID_START_TSTMP = int(request.form['VID_START_TSTMP'])
        SCN_START_FRAME = int(request.form['SCN_START_FRAME'])
        SCN_START_ELV = float(request.form['SCN_START_ELV'])
        SCN_START_LAT = float(request.form['SCN_START_LAT'])
        SCN_START_LNG = float(request.form['SCN_START_LNG'])
        SCN_START_TSTMP = int(request.form['SCN_START_TSTMP'])
        VID_END_FRAME = int(request.form['VID_END_FRAME'])
        VID_END_ELV = float(request.form['VID_END_ELV'])
        VID_END_LAT = float(request.form['VID_END_LAT'])
        VID_END_LNG = float(request.form['VID_END_LNG'])
        VID_END_TSTMP = int(request.form['VID_END_TSTMP'])
        SCN_END_FRAME = int(request.form['SCN_END_FRAME'])
        SCN_END_ELV = float(request.form['SCN_END_ELV'])
        SCN_END_LAT = float(request.form['SCN_END_LAT'])
        SCN_END_LNG = float(request.form['SCN_END_LNG'])
        SCN_END_TSTMP = int(request.form['SCN_END_TSTMP'])

        input_data = pd.DataFrame({
            'Deviation': [Deviation],
            'Maneuver': [Maneuver],
            'WeatherCondition': [WeatherCondition],
            'ParkingGarage': [ParkingGarage],
            'ArtificialLight': [ArtificialLight],
            'DynamicObjects': [DynamicObjects],
            'DirectionChange': [DirectionChange],
            'LightCondition': [LightCondition],
            'ParkingManeuver': [ParkingManeuver],
            'Seasons': [Seasons],
            'StaticObjects': [StaticObjects],
            'Location': [Location],
            'VID_START_FRAME': [VID_START_FRAME],
            'VID_START_ELV': [VID_START_ELV],
            'VID_START_LAT': [VID_START_LAT],
            'VID_START_LNG': [VID_START_LNG],
            'VID_START_TSTMP': [VID_START_TSTMP],
            'SCN_START_FRAME': [SCN_START_FRAME],
            'SCN_START_ELV': [SCN_START_ELV],
            'SCN_START_LAT': [SCN_START_LAT],
            'SCN_START_LNG': [SCN_START_LNG],
            'SCN_START_TSTMP': [SCN_START_TSTMP],
            'VID_END_FRAME': [VID_END_FRAME],
            'VID_END_ELV': [VID_END_ELV],
            'VID_END_LAT': [VID_END_LAT],
            'VID_END_LNG': [VID_END_LNG],
            'VID_END_TSTMP': [VID_END_TSTMP],
            'SCN_END_FRAME': [SCN_END_FRAME],
            'SCN_END_ELV': [SCN_END_ELV],
            'SCN_END_LAT': [SCN_END_LAT],
            'SCN_END_LNG': [SCN_END_LNG],
            'SCN_END_TSTMP': [SCN_END_TSTMP],

        })

        rf_model = joblib.load(r'apps/authentication/model_RandomForest.pkl')
        rf_prediction = rf_model.predict(input_data)
        print("Random Forest prediction:", rf_prediction)
        return render_template('Prediction/PredictionResult.html', rf_prediction=rf_prediction)

    # If the request method is GET, render the input form
    return render_template('Prediction/PredictionFeatures.html')


#Statistics usng the Clips folder function
@blueprint.route('/stats')
def generate_statistics():
    # Perform analysis and generate data for the bar chart
    directory_path = 'Clips'  # Replace with the actual path to your Clips folder

    # Get a list of subdirectories within the Clips folder
    subdirectories = [name for name in os.listdir(directory_path) if os.path.isdir(os.path.join(directory_path, name))]

    # Initialize counts for folders with and without JSON files
    count_with_json = 0
    count_without_json = 0

    # Iterate over the subdirectories and count the folders with and without JSON files
    for subdir in subdirectories:
        subdir_path = os.path.join(directory_path, subdir)
        json_files = glob.glob(os.path.join(subdir_path, '*.json'))
        if json_files:
            count_with_json += 1
        else:
            count_without_json += 1

    # Create a Plotly pie chart figure
    fig = go.Figure(data=[go.Pie(labels=['Folders containing JSON', 'Folders without JSON'], values=[count_with_json, count_without_json])])

    # Set the title for the pie chart
    fig.update_layout(title="Json Files Statistics")

    # Convert the figure to JSON
    chart_json = fig.to_json()

    # Render the template with the chart data
    return render_template('Statistics/PythonStatistics.html', chart_json=chart_json)


# Errors

@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('home/page-403.html'), 403


@blueprint.errorhandler(403)
def access_forbidden(error):
    return render_template('home/page-403.html'), 403


@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template('home/page-404.html'), 404


@blueprint.errorhandler(500)
def internal_error(error):
    return render_template('home/page-500.html'), 500
