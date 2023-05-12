import os

import openai
import requests
import secrets
import json
from prompt_utils import generate_prompt, generate_conversation_prompt
from utils import get_routes, get_athlete, get_athlete_stats, get_route_suggestions, get_athlete_activities, get_strava_access_token, clean_activity_json
from flask import Flask, redirect, render_template, request, url_for, session


app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")
app.secret_key = secrets.token_hex(16)

client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
# scope = 'read_all,activity:read_all'
redirect_uri = 'localhost:5000'
access_token = None


@app.route('/')
def index():
    redirect_uri = 'http://localhost:5000/exchange_token'
    scope = 'activity:read_all,read_all,profile:read_all'
    if access_token:
        return redirect(url_for('workout_index'))
    return redirect(f"http://www.strava.com/oauth/authorize?client_id={client_id}&response_type=code&redirect_uri={redirect_uri}&approval_prompt=force&scope={scope}")


@app.route('/exchange_token')
def strava_callback():
    try:
        # Get the authorization code from the query string
        code = request.args.get('code')

        # Use the code to obtain an access token
        access_token = get_strava_access_token(client_id, client_secret, redirect_uri, code)
        # NOT SECURE LOL

        session['access_token'] = access_token
        # Redirect the user to a new page
        return redirect(url_for('workout_index'))
    except Exception:
        return render_template("redirect_authorization.html")


@app.route("/workout_index", methods=("GET", "POST"))
def workout_index():
    access_token = session.get('access_token')
    if not access_token:
        # If the access token is missing, redirect the user to the authorization page
        return redirect('/')

    athlete_info = get_athlete(access_token)
    athleteId = athlete_info['id']

    athlete_stats = get_athlete_stats(athleteId, access_token)

    athlete_activities = clean_activity_json(get_athlete_activities(access_token))

    route_suggestions = get_route_suggestions(athlete_activities, access_token)

    # Load the previous conversation from a file
    try:
        with open('data.json', 'r') as file:
            conversation = json.load(file)
    except FileNotFoundError:
        print('Your conversation was lost.')

    if request.method == "POST":
        count = session.get('count')

        if count == 0:
            goal = request.form["goal"]
            prompt = generate_prompt(goal, athlete_stats, athlete_activities, route_suggestions)
            entry = {"role": "user", "content": prompt}
            conversation.append(entry)
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=conversation,
                temperature=0.6,
            )
            # Open the file in append mode
            with open('conversation/conversation.json', 'w') as file:
                json.dump(conversation, file)

            session['count'] += 1

            return redirect(url_for("workout_index", result=response.choices[0].text))
        else:
            question = request.form["Goal"]
            entry = {"role": "user", "content": question}
            conversation.append(entry)
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=conversation,
                temperature=0.6,
            )

            with open('conversation/conversation.json', 'w') as file:
                json.dump(conversation, file)


            return redirect(url_for("workout_index", result=response.choices[0].text))

    result = request.args.get("result")
    return render_template("index.html", result=result)
