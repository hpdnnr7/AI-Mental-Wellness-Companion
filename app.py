import streamlit as st
from textblob import TextBlob
import random

st.set_page_config(page_title="AI Mental Wellness Companion 💬", page_icon="💖")

st.title("💖 AI Mental Wellness Companion")
st.write("I'm here to listen and offer gentle support. Tell me how you're feeling today.")

# Function to analyze mood
def get_mood(text):
    polarity = TextBlob(text).sentiment.polarity
    if polarity > 0.3:
        return "positive"
    elif polarity < -0.3:
        return "negative"
    else:
        return "neutral"

# Function to generate responses
def get_response(mood):
    responses = {
        "positive": [
            "I'm happy to hear that! 🌞 What made you feel good today?",
            "That’s wonderful — keep holding onto that energy!",
            "It’s great to feel positive. Anything exciting happening soon?"
        ],
        "negative": [
            "I'm sorry you’re feeling this way 💛 Want to talk about what’s been tough?",
            "That sounds hard. Remember, it’s okay to rest and take care of yourself.",
            "You’re doing your best, and that’s enough. Try to take things one step at a time."
        ],
        "neutral": [
            "Thanks for sharing. How’s your day been overall?",
            "Sometimes it’s okay to just feel ‘meh’. Want to reflect on what might help your mood?",
            "I’m here to listen, even if you’re not sure how you feel yet."
        ]
    }
    return random.choice(responses[mood])

# Chat session state
if "history" not in st.session_state:
    st.session_state.history = []

user_input = st.text_input("You:", "")

if st.button("Send"):
    if user_input.strip():
        mood = get_mood(user_input)
        bot_response = get_response(mood)
        st.session_state.history.append(("You", user_input))
        st.session_state.history.append(("AI", bot_response))
        st.text_input("You:", "", key="new_input")

# Display conversation
for sender, message in st.session_state.history:
    if sender == "You":
        st.markdown(f"**🧍 You:** {message}")
    else:
        st.markdown(f"**🤖 AI:** {message}")
