# AI Mental Wellness Companion 💬

A mood-aware chatbot designed to listen, respond empathetically, and track your emotional state over time.
Built with Streamlit, TextBlob, and Matplotlib for real-time mood visualization and session tracking.

## Features

Conversational AI: Chat naturally with the bot, which responds based on mood and intent.

Mood Analysis: Detects positive, neutral, or negative moods, including nuanced contrast statements.

Mood Visualization: Tracks your mood throughout the session and shows trends in a graph.

Session Tracking: Save conversations and mood stats to mood_history.txt.

Positive Streaks: Highlights your current positive streak messages for motivation.

Reset & Save: Easily reset the chat or save the session at any time.

## Installation

Clone the repository:

git clone https://github.com/hpdnnr7/AI-Mental-Wellness-Companion.git
cd AI-Mental-Wellness-Companion


Create a virtual environment (optional but recommended):

python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows


Install dependencies:

<pre>pip install -r requirements.txt</pre>


Run the app locally:

streamlit run app.py


If running on a restricted network (like a company network), the local app may not display due to firewall/proxy restrictions. In that case, you can test via the deployed Streamlit Cloud app.

## Usage

Type your message in the input box and press Send.

The bot will respond with empathetic messages based on your mood.

Reset Chat clears the session (but saves it automatically if messages exist).

Save Session writes the current conversation and mood stats to mood_history.txt.

Mood trends and streaks are displayed in an interactive graph for easy tracking.

## Screenshots

Chat interface with AI responses


Mood trend visualization for the current session

## Deployment

The app is deployed on Streamlit Cloud:
Live App Link

Any updates pushed to GitHub will automatically reflect on the deployed app.

## Saved Sessions

All sessions are saved in mood_history.txt in the following format:

Session - 2025-11-14T10:48:00
Messages: 10
Moods: positive, negative, neutral, ...
Summary: 4 positive, 3 neutral, 3 negative
------------------------------------------------------------
