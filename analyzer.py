from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Create the analyzer once — reuse it for every entry (faster)
vader = SentimentIntensityAnalyzer()

# ─────────────────────────────────────────────────────────────
# EMOTION KEYWORD MAP
# Each emotion maps to a list of words/phrases that suggest it.
# We check if any of these words appear in the user's text.
# ─────────────────────────────────────────────────────────────
EMOTION_KEYWORDS = {
    "Joy":        ["happy", "joyful", "excited", "amazing", "great", "wonderful",
                   "love", "fantastic", "grateful", "blessed", "thrilled", "delighted",
                   "cheerful", "elated", "content", "glad", "pleased", "smile", "laugh"],

    "Sadness":    ["sad", "unhappy", "cry", "cried", "tears", "depressed", "miserable",
                   "heartbroken", "lonely", "alone", "grief", "sorrow", "hopeless",
                   "empty", "lost", "gloomy", "down", "blue", "upset"],

    "Anger":      ["angry", "furious", "rage", "hate", "annoyed", "frustrated",
                   "irritated", "mad", "outraged", "livid", "resentful", "bitter",
                   "hostile", "agitated", "infuriated"],

    "Anxiety":    ["anxious", "worried", "nervous", "stressed", "overwhelmed", "panic",
                   "scared", "fear", "dread", "tense", "uneasy", "restless",
                   "apprehensive", "on edge", "cant stop thinking", "overthinking"],

    "Exhaustion": ["tired", "exhausted", "drained", "burnt out", "burnout", "sleepy",
                   "fatigue", "fatigued", "worn out", "no energy", "exhausting",
                   "weary", "sluggish", "lethargic", "spent"],

    "Confusion":  ["confused", "lost", "unsure", "dont know", "uncertain", "unclear",
                   "bewildered", "puzzled", "overwhelmed", "cant focus", "scattered"],

    "Hope":       ["hope", "hopeful", "optimistic", "looking forward", "excited about",
                   "better tomorrow", "things will improve", "positive", "believe",
                   "motivated", "inspired", "determined", "ready"],

    "Gratitude":  ["grateful", "thankful", "appreciate", "blessed", "fortunate",
                   "lucky", "thankfulness", "gratitude"],

    "Loneliness": ["lonely", "alone", "isolated", "no one", "nobody", "left out",
                   "disconnected", "invisible", "ignored", "forgotten"],

    "Pride":      ["proud", "accomplished", "achieved", "did it", "succeeded",
                   "proud of", "milestone", "victory", "win", "earned"],
}


def analyze(text: str) -> dict:
    """
    Main function — takes raw journal text, returns a results dict with:
      - sentiment  : "Positive" / "Neutral" / "Negative"
      - score      : float between -1.0 and 1.0
      - emotions   : list of detected emotion labels
    """
    text_lower = text.lower()

    # ── 1. Sentiment via VADER ──────────────────────────────────
    scores    = vader.polarity_scores(text)
    compound  = scores["compound"]        # ranges from -1 (very negative) to +1 (very positive)

    if compound >= 0.05:
        sentiment = "Positive"
    elif compound <= -0.05:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"

    # ── 2. Emotion Detection via keywords ──────────────────────
    detected_emotions = []
    for emotion, keywords in EMOTION_KEYWORDS.items():
        for keyword in keywords:
            if keyword in text_lower:
                detected_emotions.append(emotion)
                break   # found this emotion — no need to check more keywords for it

    # If no emotion keyword matched, fall back to a sentiment-based default
    if not detected_emotions:
        if sentiment == "Positive":
            detected_emotions = ["Calm"]
        elif sentiment == "Negative":
            detected_emotions = ["Unease"]
        else:
            detected_emotions = ["Neutral"]

    return {
        "sentiment": sentiment,
        "score":     round(compound, 3),
        "emotions":  detected_emotions,
    }
