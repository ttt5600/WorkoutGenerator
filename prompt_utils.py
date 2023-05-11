import json


def generate_prompt(goal, athlete_stats, athlete_activities, route_suggestions):

    prompt = """You are an athletic coach. You are discussing with an athlete who's has some athletic goal. Suggest a workout plan for today, this week, and general advice for the goal based on the athlete's previous stats, and activities.

Here's an example response:
Goal: run a half-marathon at 1:20 pace.
Workout for today: 15 x 400m, 100m jog (8M total) at 5k pace, 60 minutes total, 8/10 intensity.
Workout for this week:
    Mon: 4 miles, 7:45 min/mile pace, 31 mins total, 3/10 intensity.
    Tue: 15 x 400m, 100m jog (8M total), at 5K pace, 60 mins total, 8/10 intensity.
    Wed: Steady	10M, 7:00 min/mile pace, 70 mins totoal, 5/10 intensity.
    Thu: 8 miles (inc 4M Threshold), 1/2 marathon pace, 55 mins total (25 mins THR), 7/10 intensity.
    Fri: 4 miles, 7:30 min/mile pace, 30 mins total, 3/10 intensity.
    Sat: 8 miles (12 x 200m hill), Mile pace on the hills, 65 mins total, 6/10 intensity.
    Sun: 15 miles, 7:15 min/mile pace, 1hr 50min total, 9/10 intensity.

For the general advice, just give any words of motivation, length of training needed, sleeping schedule, healthy habits, cross training, lifting, diet tips, and anything else that is relevant.

Here are athlete stats in JSON format. Distances are in meters and times are in total seconds: {}
Here are recent activities in the past 2 weeks in JSON format. Distances are in meters and times are in total seconds. Speeds are in meters/second. Pay attention to personal records and flagged activities (flagged may not be an accurate representation of athletic ability): {}
If applicable, suggest some routes for the workout today based on the following dict: key = name (which should be returned), values = 3 columns: average grade, elevation difference, and distance respectively: {}
Goal: {}.
Include athlete stats and judgement of training progress and athletic ability from the activities in the past 2 weeks in your response. Mention specific times and evidence and provide reasoning. If the athlete should already be able to achieve the goal, suggest something faster/longer. Take the information as truth (do not say e.g. "based on your information, ..."), and if needed provide the source as Strava.
Remember, you are a friendly coach talking to the athlete you are training.""".format(json.dumps(athlete_stats), json.dumps(athlete_activities), json.dumps(route_suggestions), goal)

    return prompt


def generate_conversation_prompt(question, athlete_stats, athlete_activities, conversation):

    prompt = """Pretend you are an athletic traininer and coach. You are discussing with and training an athlete.

Here are some athlete stats in JSON format. Distances are in meters and times are in total seconds: {}
Here are some recent activities in the past 2 weeks in JSON format. Distances are in meters and times are in total seconds. Speeds are in meters/second and pay attention to if it is a personal record and if it is a flagged activity (it might not be an accurate activity or representation of athletic ability): {}
Here are the previous answers you provided, take this into account in your conversation: {}

The athlete gives you the following prompt.
Prompt: {}.
Make sure to include the athlete stats and your judgement of the training progress and athletic ability over the activities in the past 2 weeks in your response and reasoning. Do not mention JSON in your response.
Remember, you are a tough but friendly coach talking to the athlete you are training in your response.""".format(json.dumps(athlete_stats), json.dumps(athlete_activities), conversation, question)

    return prompt
