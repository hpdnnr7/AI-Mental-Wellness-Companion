import streamlit as st
from textblob import TextBlob
import matplotlib.pyplot as plt
import random

st.set_page_config(page_title="Mood-Aware Chatbot 💬", page_icon="💖")

st.title(" Mood-Aware Chatbot 💬")
st.write(
    "I'm here to listen and offer gentle support. Tell me how you're feeling today."
)


def detect_intent(text):
    text = text.lower().strip()
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
            parts = text_lower.split(contrast,
                                     1)  # Split only on first occurrence
            before = parts[0]
            after = parts[1] if len(parts) > 1 else ""

            # Detect topics AND mood in each part
            before_topics = detect_topic(before)
            after_topics = detect_topic(after)

            before_mood = get_mood(before)
            after_mood = get_mood(after)

            return (True, before_topics, before_mood, after_topics, after_mood)

    return (False, [], None, [], None)


def get_mood(text):
    """
    Improved mood detection with word boundary checking
    """
    text_lower = text.lower()

    # Split into words for exact matching
    words = set(
        text_lower.replace(',', ' ').replace('.', ' ').replace('!',
                                                               ' ').split())
    # print(f"DEBUG MOOD: words = {words}")

    negative_cues = {
        "sad", "sadness", "tired", "tiredness", "stressed", "stressful",
        "anxious", "anxiety", "worried", "worry", "angry", "depressed",
        "lonely", "overwhelmed", "burnout", "exhausted", "exhausting",
        "exhaustion", "terrible", "awful", "horrible", "struggling", "bad",
        "worse", "worst"
    }
    positive_cues = {
        "happy", "excited", "grateful", "thankful", "love", "joyful",
        "content", "amazing", "great", "wonderful", "fantastic", "blessed",
        "sweet", "awesome", "excellent", "brilliant", "surprised", "proud",
        "accomplished", "thrilled", "delighted"
    }
    neutral_cues = {
        "okay", "fine", "alright", "so-so", "meh", "good", "decent", "ok"
    }

    # Check for exact word matches using set intersection
    found_negative = bool(negative_cues & words)
    found_positive = bool(positive_cues & words)
    found_neutral = bool(neutral_cues & words)

    # print(f"DEBUG MOOD: found_negative={found_negative}, found_positive={found_positive}, found_neutral={found_neutral}")

    # Priority: Strong emotions override neutral words
    if found_negative:
        return "negative"
    if found_positive:
        return "positive"
    if found_neutral:
        return "neutral"

    # Fallback: use TextBlob polarity
    polarity = TextBlob(text).sentiment.polarity
    if polarity > 0.15:
        return "positive"
    elif polarity < -0.15:
        return "negative"
    else:
        return "neutral"


def should_include_secondary(primary_topic, secondary_topic, mood):
    """
    Determines if secondary topic should be included to avoid awkward repetition
    """
    # Don't include secondary if topics would give redundant responses
    redundant_pairs = [("work", "general"), ("school", "general"),
                       ("relationship", "general"), ("travel", "general")]

    # Check if this combination would be redundant
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

    # Sort by priority
    priority_order = ["travel", "relationship", "school", "work", "general"]
    detected_sorted = sorted(detected,
                             key=lambda x: priority_order.index(x)
                             if x in priority_order else len(priority_order))

    return detected_sorted[:2]  # Limit to 2 topics


def get_response(mood, user_message):
    # print(f"DEBUG 1: Input mood = {mood}")
    # print(f"DEBUG 2: User message = {user_message}")
    intent = detect_intent(user_message)

    # Quick intent responses
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

    # Check for contrast structure (negative BUT positive)
    has_contrast, before_topics, before_mood, after_topics, after_mood = analyze_sentiment_structure(
        user_message)
    # print(f"DEBUG 3: has_contrast = {has_contrast}")
    # print(
    #     f"DEBUG 4: before_topics = {before_topics}, before_mood = {before_mood}"
    # )
    # print(f"DEBUG 5: after_topics = {after_topics}, after_mood = {after_mood}")

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

    # Handle contrast structure with DYNAMIC mood detection
    if has_contrast and before_topics and after_topics and before_mood and after_mood:
        # print("DEBUG 6: Using CONTRAST structure")
        first_topic = before_topics[0]
        second_topic = after_topics[0]

        # Use the ACTUAL detected mood for each part
        first_response = topic_responses[first_topic][before_mood]
        second_response = topic_responses[second_topic][after_mood]

        # Make second response flow naturally
        second_response = second_response[0].lower() + second_response[1:]
        return f"{first_response} Also, {second_response}"

    # Regular single-mood response (no contrast structure)
    topics = detect_topic(user_message)
    # print(f"DEBUG 7: Regular topics = {topics}")
    primary_topic = topics[0]
    primary_response = topic_responses[primary_topic][mood]
    # print(f"DEBUG 8: Primary topic = {primary_topic}, mood = {mood}")
    # print(f"DEBUG 9: Primary response = {primary_response}")

    # Only add secondary topic if it's meaningfully different and adds value
    if len(topics) > 1 and topics[1] != primary_topic:
        secondary_topic = topics[1]

        if should_include_secondary(primary_topic, secondary_topic, mood):
            secondary_response = topic_responses[secondary_topic][mood]

            # Use varied connectors instead of always "Also,"
            connectors = ["Also, ", "And ", "Plus, ", "On another note, "]
            connector = random.choice(connectors)

            # Make it flow naturally
            secondary_response = secondary_response[0].lower(
            ) + secondary_response[1:]
            return f"{primary_response} {connector}{secondary_response}"

    return primary_response


# Chat session state
if "history" not in st.session_state:
    st.session_state.history = []

if "user_input" not in st.session_state:
    st.session_state.user_input = ""

if "last_mood" not in st.session_state:
    st.session_state.last_mood = None

if "moods" not in st.session_state:
    st.session_state.moods = []

# Create text input with persistent state
st.session_state.user_input = st.text_input("You:",
                                            st.session_state.user_input,
                                            key="input_box")

# Handle Send button
if st.button("Send"):
    if st.session_state.user_input.strip():
        # Analyze mood
        mood = get_mood(st.session_state.user_input)

        # If new mood is neutral but we have a previous one, keep the last mood
        # if mood == "neutral" and st.session_state.last_mood is not None:
        #     mood = st.session_state.last_mood
        # else:
        #     st.session_state.last_mood = mood

        # Generate bot response
        bot_response = get_response(mood, st.session_state.user_input)
        # Check if this was a contrast/mixed emotion message
        has_contrast, before_topics, before_mood, after_topics, after_mood = analyze_sentiment_structure(
            st.session_state.user_input)
        # For the graph: track mixed emotions as neutral
        if has_contrast and before_mood and after_mood and before_mood != after_mood:
            graph_mood = "neutral"  # Mixed emotions
        else:
            graph_mood = mood

        # Track moods for the chart
        st.session_state.moods.append(graph_mood)

        # Append messages to history
        st.session_state.history.append(("You", st.session_state.user_input))
        st.session_state.history.append(("AI", bot_response))

        # Clear input
        st.session_state.user_input = ""

# Display conversation
for sender, message in st.session_state.history:
    if sender == "You":
        st.markdown(f"**🧍 You:** {message}")
    else:
        st.markdown(f"**🤖 AI:** {message}")

# st.subheader("🌈 Mood Trend Over Time")
# --- Mood Trend Visualization ---
if "moods" in st.session_state and len(st.session_state.moods) > 0:
    st.write("### 🌈 Mood Trend Over Time")
    st.markdown("---")
    mood_map = {"negative": -1, "neutral": 0, "positive": 1}
    mood_values = [mood_map[m] for m in st.session_state.moods]

    fig, ax = plt.subplots()
    ax.plot(range(1,
                  len(mood_values) + 1),
            mood_values,
            marker="o",
            linestyle="-")
    ax.set_xlabel("Message #")
    ax.set_ylabel("Mood Level")
    ax.set_title("Your Mood Pattern During Chat")
    ax.set_yticks([-1, 0, 1])
    ax.set_yticklabels(["Negative", "Neutral", "Positive"])

    st.pyplot(fig)

if st.button("🔄 Reset Chat"):
    st.session_state.history = []
    st.session_state.moods = []
    st.session_state.last_mood = None
