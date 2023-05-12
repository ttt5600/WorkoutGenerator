# AI Personalized workout generator - connect with Strava app!

Just access the website, connect your strava permission, and off you go!

## If you'd like to run this locally: 
1. Clone this repo

2. Navigate into the project directory

   ```bash
   $ cd openai-quickstart-python
   ```

3. Create a new virtual environment

   ```bash
   $ python -m venv venv
   $ . venv/bin/activate
   ```

4. Install the requirements

   ```bash
   $ pip install -r requirements.txt
   ```

5. Make a copy of the example environment variables file

   ```bash
   $ cp .env.example .env
   ```

6. Add your [API key](https://beta.openai.com/account/api-keys) to the newly created `.env` file.

7. Run the app

   ```bash
   $ flask run
   ```

You'll need to create your own conversations/conversation.json file for security purposes and all. Also requires python 3.8-3.10
