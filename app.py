import streamlit as st
from textblob import TextBlob
import matplotlib.pyplot as plt
import random
from datetime import datetime
import os

st.set_page_config(page_title="Mood-Aware Chatbot 💬", page_icon="💖")

st.title("Mood-Aware Chatbot 💬")
st.write(
    "I'm here to listen and offer gentle support. Tell me how you're feeling today."
)

# File path for persistent storage
MOOD_DATA_FILE = "mood_history.txt"


def save_session_to_txt(session_data):
    """Append session to TXT file"""
    # Check if file exists to determine if we need a header
    file_exists = os.path.exists(MOOD_DATA_FILE)

    with open(MOOD_DATA_FILE, 'a') as f:  # 'a' = append mode
        if not file_exists:
            f.write("=" * 60 + "\n")
            f.write("MOOD HISTORY - SAVED SESSIONS\n")
            f.write("=" * 60 + "\n\n")

        f.write(f"Session - {session_data['timestamp']}\n")
        f.write(f"Messages: {session_data['message_count']}\n")
        f.write(f"Moods: {', '.join(session_data['moods'])}\n")

        # Calculate session statistics
        mood_counts = {"positive": 0, "neutral": 0, "negative": 0}
        for mood in session_data['moods']:
            mood_counts[mood] += 1

        f.write(f"Summary: {mood_counts['positive']} positive, "
                f"{mood_counts['neutral']} neutral, "
                f"{mood_counts['negative']} negative\n")
        f.write("-" * 60 + "\n\n")


def calculate_streak(moods):
    """Calculate current positive mood streak"""
    if not moods:
        return 0

    streak = 0
    for mood in reversed(moods):
        if mood == "positive":
            streak += 1
        else:
            break
    return streak


def detect_intent(text):
    text = text.lower().strip().strip('"').strip("'")
    words = text.split()

    greetings = [
        "hi", "hello", "hey", "yo", "sup", "good morning", "good afternoon",
        "good evening"
    ]
    thanks = ["thank", "thanks", "appreciate", "grateful"]
    bye = ["bye", "goodbye", "see you", "talk later"]

    if any(greet in text for greet in [
            "hi ", "hi!", "hello", "hey ", "hey!", "yo ", "yo!", "sup ", "sup!"
    ]) or text in greetings:
        return "greeting"
    elif any(word in words for word in thanks):
        return "thanks"
    elif any(phrase in text for phrase in bye):
        return "farewell"
    else:
        return "general"


def analyze_sentiment_structure(text):
    """
    Analyzes if message has a contrast structure and detects sentiment of each part
    Returns: (has_contrast, topics_before, mood_before, topics_after, mood_after)
    """
    text_lower = text.lower()
    contrast_words = [" but ", " though ", " however ", " yet "]

    for contrast in contrast_words:
        if contrast in text_lower:
            parts = text_lower.split(contrast, 1)
            before = parts[0]
            after = parts[1] if len(parts) > 1 else ""

            before_topics = detect_topic(before)
            after_topics = detect_topic(after)
            before_mood = get_mood(before)
            after_mood = get_mood(after)

            return (True, before_topics, before_mood, after_topics, after_mood)

    return (False, [], None, [], None)


def get_mood(text):
    """Improved mood detection with word boundary checking"""
    text_lower = text.lower()
    words = set(
        text_lower.replace(',', ' ').replace('.', ' ').replace('!',
                                                               ' ').split())

    negative_cues = {
        "sad", "sadness", "tired", "tiredness", "stressed", "stressful",
        "anxious", "anxiety", "worried", "worry", "angry", "depressed",
        "lonely", "overwhelmed", "burnout", "exhausted", "exhausting",
        "exhaustion", "terrible", "awful", "horrible", "struggling", "bad",
        "worse", "worst", "devastated", "dreading", "dread", "hate", "hating",
        "terrified", "scared", "fearful", "fear", "afraid", "upset",
        "frustrated", "frustration", "disappointed", "irritated", "jealous",
        "insecure", "guilty", "ashamed", "hurt", "drained", "lost", "confused"
    }
    positive_cues = {
        "happy", "excited", "grateful", "thankful", "love", "joyful",
        "content", "amazing", "great", "wonderful", "fantastic", "blessed",
        "sweet", "awesome", "excellent", "brilliant", "surprised", "proud",
        "accomplished", "thrilled", "delighted", "well", "relieved", "relief",
        "calm", "peaceful", "peace", "relaxed", "relaxing", "relaxation",
        "relax", "chill", "chilled", "chilling", "chillax", "motivated",
        "inspired", "optimistic", "hopeful", "confident", "cheerful",
        "energized"
    }
    neutral_cues = {
        "okay", "fine", "alright", "so-so", "good", "decent", "ok", "neutral",
        "indifferent", "meh", "unsure", "bored", "numb"
    }

    found_negative = bool(negative_cues & words)
    found_positive = bool(positive_cues & words)
    found_neutral = bool(neutral_cues & words)

    if found_negative:
        return "negative"
    if found_positive:
        return "positive"
    if found_neutral:
        return "neutral"

    polarity = TextBlob(text).sentiment.polarity
    if polarity > 0.15:
        return "positive"
    elif polarity < -0.15:
        return "negative"
    else:
        return "neutral"


def should_include_secondary(primary_topic, secondary_topic, mood):
    """Determines if secondary topic should be included to avoid awkward repetition"""
    redundant_pairs = [("work", "general"), ("school", "general"),
                       ("relationship", "general"), ("travel", "general")]

    if (primary_topic, secondary_topic) in redundant_pairs:
        return False
    return True


def detect_topic(text):
    text = text.lower()
    topics = {
        "travel": [
            "travel", "trip", "vacation", "flight", "journey", "airport",
            "brazil", "europe", "asia"
        ],
        "relationship": [
            "love", "boyfriend", "girlfriend", "relationship", "partner",
            "dating", "crush"
        ],
        "school": [
            "school", "class", "study", "homework", "exam", "college",
            "professor", "assignment"
        ],
        "work": ["work", "job", "boss", "career", "office", "meeting"],
    }

    detected = [
        t for t, kws in topics.items() if any(word in text for word in kws)
    ]
    if not detected:
        detected = ["general"]

    priority_order = ["travel", "relationship", "school", "work", "general"]
    detected_sorted = sorted(detected,
                             key=lambda x: priority_order.index(x)
                             if x in priority_order else len(priority_order))

    return detected_sorted[:2]


def get_response(mood, user_message):
    intent = detect_intent(user_message)

    if intent == "greeting":
        return random.choice([
            "Hey there! 👋 How are you feeling today?",
            "Hi! It's good to see you again 😊",
            "Hey! What's on your mind right now?"
        ])
    elif intent == "thanks":
        return random.choice([
            "Aww, you're welcome 💖", "Happy to help anytime 🌸",
            "You're sweet — I'm here for you always 💕"
        ])
    elif intent == "farewell":
        return random.choice([
            "Take care, okay? 🌿", "Talk soon — sending good vibes your way 💫",
            "Bye for now! 💌"
        ])

    has_contrast, before_topics, before_mood, after_topics, after_mood = analyze_sentiment_structure(
        user_message)

    topic_responses = {
        "travel": {
            "positive":
            "That sounds so exciting! ✈️ Traveling can be such a great way to reset and find joy.",
            "neutral":
            "Travel plans always bring mixed feelings — are you feeling ready for it?",
            "negative":
            "Travel can be stressful with all the planning 💛 But it'll be worth it once you're there!"
        },
        "work": {
            "positive":
            "That's awesome about work! 💼 Keep that momentum going!",
            "neutral":
            "Work can be tricky to balance — are you feeling productive or a bit drained?",
            "negative":
            "Work stress is real 😞 Remember to give yourself credit for showing up and doing your best."
        },
        "relationship": {
            "positive":
            "Love and connection can feel so beautiful 💖 I'm happy for you!",
            "neutral":
            "Relationships can be complex — how are things between you two lately?",
            "negative":
            "Matters of the heart can really weigh on you 💔 I'm here if you want to unpack it."
        },
        "school": {
            "positive":
            "Nice! 📚 Sounds like things are going well with school!",
            "neutral":
            "School can be a lot to juggle — are you managing okay?",
            "negative":
            "That sounds exhausting 💛 Try not to be too hard on yourself — learning takes time."
        },
        "general": {
            "positive":
            "I love hearing good news like that 🌞 What's been lifting your mood?",
            "neutral":
            "Thanks for sharing — how's your day feeling overall?",
            "negative":
            "That sounds rough 💛 Take a deep breath — you're doing your best."
        }
    }

    if has_contrast and before_topics and after_topics and before_mood and after_mood:
        first_topic = before_topics[0]
        second_topic = after_topics[0]
        first_response = topic_responses[first_topic][before_mood]
        second_response = topic_responses[second_topic][after_mood]
        second_response = second_response[0].lower() + second_response[1:]
        return f"{first_response} Also, {second_response}"

    topics = detect_topic(user_message)
    primary_topic = topics[0]
    primary_response = topic_responses[primary_topic][mood]

    if len(topics) > 1 and topics[1] != primary_topic:
        secondary_topic = topics[1]
        if should_include_secondary(primary_topic, secondary_topic, mood):
            secondary_response = topic_responses[secondary_topic][mood]
            connectors = ["Also, ", "And ", "Plus, ", "On another note, "]
            connector = random.choice(connectors)
            secondary_response = secondary_response[0].lower(
            ) + secondary_response[1:]
            return f"{primary_response} {connector}{secondary_response}"

    return primary_response


# Initialize session state
if "history" not in st.session_state:
    st.session_state.history = []

if "user_input" not in st.session_state:
    st.session_state.user_input = ""

if "moods" not in st.session_state:
    st.session_state.moods = []

if "session_start" not in st.session_state:
    st.session_state.session_start = datetime.now().isoformat()

# Create text input
st.session_state.user_input = st.text_input(
    "You:", key="input_box", placeholder="Type your message here...")

# Handle Send button
if st.button("Send"):
    if st.session_state.user_input.strip():
        mood = get_mood(st.session_state.user_input)
        bot_response = get_response(mood, st.session_state.user_input)

        has_contrast, before_topics, before_mood, after_topics, after_mood = analyze_sentiment_structure(
            st.session_state.user_input)

        if has_contrast and before_mood and after_mood and before_mood != after_mood:
            graph_mood = "neutral"
        else:
            graph_mood = mood

        st.session_state.moods.append(graph_mood)
        st.session_state.history.append(("You", st.session_state.user_input))
        st.session_state.history.append(("AI", bot_response))
        st.session_state.user_input = ""

# Display conversation
for sender, message in st.session_state.history:
    if sender == "You":
        st.markdown(f"**🧍 You:** {message}")
    else:
        st.markdown(f"**🤖 AI:** {message}")

# Mood visualization and analytics
if "moods" in st.session_state and len(st.session_state.moods) > 0:
    st.write("### 🌈 Mood Trend Over Time")
    st.markdown("---")

    # Calculate analytics
    current_streak = calculate_streak(st.session_state.moods)

    # Display analytics cards (only 2 columns now)
    col1, col2 = st.columns(2)

    with col1:
        st.metric("Current Positive Streak 🔥", f"{current_streak} messages")

    with col2:
        # Current session mood percentage
        mood_counts = {"positive": 0, "neutral": 0, "negative": 0}
        for mood in st.session_state.moods:
            mood_counts[mood] += 1

        dominant_mood = max(mood_counts, key=mood_counts.get)
        mood_emoji = {"positive": "😊", "neutral": "😐", "negative": "😔"}
        st.metric("Current Session Mood",
                  f"{dominant_mood.title()} {mood_emoji[dominant_mood]}")

    # Plot current session
    mood_map = {"negative": -1, "neutral": 0, "positive": 1}
    mood_values = [mood_map[m] for m in st.session_state.moods]

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(range(1,
                  len(mood_values) + 1),
            mood_values,
            marker="o",
            linestyle="-",
            linewidth=2,
            markersize=8)
    ax.set_xlabel("Message #")
    ax.set_ylabel("Mood Level")
    ax.set_title("Your Mood Pattern (Current Session)")
    ax.set_yticks([-1, 0, 1])
    ax.set_yticklabels(["Negative", "Neutral", "Positive"])
    ax.grid(True, alpha=0.3)

    st.pyplot(fig)

# Reset and Save buttons
col1, col2 = st.columns(2)

with col1:
    if st.button("🔄 Reset Chat"):
        # Reset session (no automatic saving)
        for key in ["history", "moods", "user_input"]:
            if key in st.session_state:
                del st.session_state[key]
        st.session_state.session_start = datetime.now().isoformat()
        st.rerun()

with col2:
    if st.button("⬇️ Download Current Session"):
        if st.session_state.moods:
            # Count moods to determine dominant/current session mood
            mood_counts = {"positive": 0, "neutral": 0, "negative": 0}
            for mood in st.session_state.moods:
                mood_counts[mood] += 1

            dominant_mood = max(mood_counts, key=mood_counts.get)

            # Create current session string for download
            current_session_txt = "=" * 60 + "\n"
            current_session_txt += "CURRENT SESSION\n"
            current_session_txt += "=" * 60 + "\n\n"
            current_session_txt += f"Session - {st.session_state.session_start}\n"
            current_session_txt += f"Messages: {len(st.session_state.history)//2}\n"
            current_session_txt += f"Moods: {', '.join(st.session_state.moods)}\n"
            current_session_txt += f"Current Session Mood: {dominant_mood.title()}\n"
            current_session_txt += "=" * 60 + "\n"

# Provide download button
    st.download_button(
    "⬇️ Download Current Session", 
    current_session_txt, 
    file_name=f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    )
