import os

import requests
import urllib.parse
import datetime
import json
from urllib.parse import urlencode


def get_strava_access_token(client_id, client_secret, redirect_uri, code):
    """
    Gets an access token for the authenticated Strava user using the OAuth 2.0 authorization flow.
    """
    # Exchange the authorization code for an access token
    response = requests.post('https://www.strava.com/oauth/token', data={
    'client_id': client_id,
    'client_secret': client_secret,
    'code': code,
    'grant_type': 'authorization_code',
    'redirect_uri': redirect_uri
    })

    if response.status_code == 200:
        # Return the access token
        return response.json()['access_token']
    else:
        # Something went wrong
        raise Exception('Failed to obtain Strava access token')


def clean_activity_json(activities):
    for act in activities:
        del act['resource_state']
        del act['athlete']
        del act['workout_type']
        del act['id']
        del act['trainer']
        del act['map']
        del act['utc_offset']
        del act['location_city']
        del act['location_state']
        del act['location_country']
        del act['kudos_count']
        del act['comment_count']
        del act['photo_count']
        del act['commute']
        del act['private']
        del act['visibility']
        del act['gear_id']
        del act['upload_id']
        del act['upload_id_str']
        del act['external_id']
        del act['total_photo_count']
        del act['has_kudoed']
        del act['from_accepted_tag']
        del act['end_latlng']
        del act['display_hide_heartrate_option']

    return activities


# Get Athlete
def get_athlete(access_token):
    headers = {'Authorization': f'Bearer {access_token}'}

    # Make a GET request to the Strava athlete info endpoint
    response = requests.get('https://www.strava.com/api/v3/athlete', headers=headers)

    # Raise an exception if the request fails
    response.raise_for_status()

    # Parse the response data as JSON
    return response.json()


def get_athlete_stats(athleteId, access_token):
    headers = {'Authorization': f'Bearer {access_token}'}

    # Make a GET request to the Strava athlete info endpoint
    response = requests.get(f"https://www.strava.com/api/v3/athletes/{athleteId}/stats", headers=headers)

    # Raise an exception if the request fails
    response.raise_for_status()

    # Parse the response data as JSON
    return response.json()



def get_athlete_activities(access_token):
    headers = {'Authorization': f'Bearer {access_token}'}

    # Calculate the start date for the activities (two weeks ago from today)
    start_date = int((datetime.datetime.now() - datetime.timedelta(days=14)).timestamp())

    # Make a GET request to the Strava activities endpoint
    response = requests.get('https://www.strava.com/api/v3/athlete/activities', headers=headers, params={'after': start_date})

    # Raise an exception if the request fails
    response.raise_for_status()

    # Parse the response data as JSON
    activities = response.json()

    return activities


def get_route_suggestions(activity_list, access_token):

    suggestions = set()
    suggestions_stats = dict()

    for activity in activity_list:
        lat, long = activity['start_latlng']
        routes = get_routes(lat, long, access_token)
        for route in routes['segments']:
            suggestions.add(route['name'])
            if route['name'] not in suggestions:
                suggestions_stats[route['name']] = [route['avg_grade'], route['elev_difference'], route['distance']]

    return suggestions_stats


def get_routes(lat, long, access_token):
    headers = {'Authorization': f'Bearer {access_token}'}

    bounds = [lat - 0.03,long - 0.03,lat + 0.03,long + 0.03]

    payload = {'bounds': str(bounds).strip('[]'), 'activity_type': 'running'}

    # Convert the bounds list to a URL-encoded string
    params = urlencode(payload, quote_via=urllib.parse.quote)

    try:
        # Make a GET request to the Strava segments endpoint
        response = requests.get('https://www.strava.com/api/v3/segments/explore', headers=headers, params=params)

        # Raise an exception if the request fails
        response.raise_for_status()
    except requests.exceptions.HTTPError as error:
        return []

    # Parse the response data as JSON
    activities = response.json()

    return activities
