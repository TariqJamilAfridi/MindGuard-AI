import random

# ═══════════════════════════════════════════════════════════════
#  MINDGUARD — ai_response.py
#
#  Philosophy: Responses must sound like a kind, calm friend
#  talking to you — not a therapist, not a robot, not a book.
#  Simple words. Short sentences. Real warmth. Always specific
#  to the emotion so it feels personally heard.
#
#  13–14 responses per emotion category.
#  5 coping tips per emotion — practical, doable, specific.
# ═══════════════════════════════════════════════════════════════

RESPONSES = {

    # ── JOY ──────────────────────────────────────────────────
    ("Positive", "Joy"): [
        "This honestly made me smile reading it. You sound really happy today, and that is wonderful.",
        "Good days like this one are worth holding onto. I am really glad you are feeling this way.",
        "You know what? Not every day feels like this. Enjoy every bit of it, you deserve it.",
        "That kind of happiness is contagious, even through words. Keep riding this feeling.",
        "I love hearing this. You sound light today, and that matters more than you probably realize.",
        "This is the kind of day you will look back on and smile. Make the most of it.",
        "Something is clearly going right for you today, and I am genuinely happy for you.",
        "Days like this remind you why the harder ones are worth getting through. Soak it all in.",
        "You sound so alive in this entry. That energy is a gift. Do not waste a drop of it.",
        "Reading this felt like a breath of fresh air. You are in a really good place right now.",
        "That joy you are feeling is real and it is yours. Nobody can take that away from you.",
        "It is rare to feel this good, so sit with it a little longer before the day moves on.",
        "Whatever happened today, it worked. You are glowing through your words.",
    ],

    # ── HOPE ─────────────────────────────────────────────────
    ("Positive", "Hope"): [
        "I can hear the hope in what you wrote, and honestly, that is one of the most powerful things a person can carry.",
        "You are looking forward to something and believing it will happen. That takes real courage.",
        "This is what a good mindset looks like. Hold onto this feeling tight.",
        "Something is shifting for you and you can feel it. Trust that instinct.",
        "The fact that you feel hopeful right now says a lot about your strength.",
        "Hope is not wishful thinking. It is a choice. And you are choosing it right now.",
        "Whatever you are looking forward to, I really hope it works out exactly the way you imagine.",
        "You sound motivated today. That energy is going to carry you a long way.",
        "Reading this felt uplifting. You are in a good headspace and that matters.",
        "Keep feeding that spark. Not every day will feel like this, so use today well.",
        "You are not just hoping blindly. You are believing in yourself, and that is different.",
        "This kind of forward-thinking energy is exactly what sets people apart.",
        "I believe in what you are hoping for. Now make sure you believe in it too.",
    ],

    # ── GRATITUDE ────────────────────────────────────────────
    ("Positive", "Gratitude"): [
        "The fact that you noticed the good things today means you are paying attention to what really matters.",
        "Gratitude is honestly one of the hardest things to practise, and you are doing it naturally. That is special.",
        "You could have written about anything, but you chose to notice what is good. I love that.",
        "There is something really grounding about feeling thankful. You sound settled and at peace.",
        "Not many people stop to appreciate what they have. You just did, and that says a lot about you.",
        "That kind of thankfulness tends to multiply. The more you notice the good, the more good you find.",
        "Reading this felt peaceful. You are in a beautiful headspace right now.",
        "The things you are grateful for are clearly meaningful to you. That is not nothing.",
        "Gratitude like this has a way of softening even the hard edges of a day. You feel it.",
        "You sound happy in a quiet, deep kind of way. That is actually better than excited happy.",
        "Whatever you are thankful for today, it clearly meant something real to you.",
        "This kind of reflection is good for the soul. You should do this more often.",
        "I am glad you wrote this. It is a good reminder that there is always something worth noticing.",
    ],

    # ── PRIDE ────────────────────────────────────────────────
    ("Positive", "Pride"): [
        "You earned this. Every single bit of it. Stop and let yourself actually feel proud for once.",
        "Do not rush past this moment. You did something worth celebrating, so celebrate it properly.",
        "That feeling you have right now? That is what hard work looks like when it pays off.",
        "I am genuinely proud of you reading this. You put in the effort and it showed.",
        "Moments like this do not just happen. You made this happen. Remember that.",
        "This is what real accomplishment feels like. Not luck, not chance. You.",
        "You worked for this. Nobody handed it to you. Own it completely.",
        "The version of you from before would be really proud of who you are right now.",
        "You did it, and now you need to actually believe that you did it.",
        "Achievement feels best when you know exactly what it cost you. You know.",
        "Take a proper moment with this. Not a quick glance. A full, real pause to appreciate it.",
        "This is the kind of thing you write down and look back at when things get hard.",
        "Well done. And I mean that simply, without any extra words needed.",
    ],

    # ── SADNESS ──────────────────────────────────────────────
    ("Negative", "Sadness"): [
        "That sounds really painful and I am sorry you are going through it. You do not have to be okay right now.",
        "It makes complete sense that you feel this way. What you are carrying is heavy and real.",
        "You do not have to explain or justify how you feel. Sad is sad, and that is enough.",
        "I hear you. Some days are just genuinely hard and today sounds like one of them.",
        "You came here and wrote this instead of keeping it locked inside. That took something. I respect that.",
        "Sadness like this usually means you care deeply about something. That is not a flaw.",
        "Please be gentle with yourself today. You deserve the same kindness you would give a friend.",
        "You are not weak for feeling this. You are human, and this is what being human sometimes looks like.",
        "Whatever is making you sad right now is real and valid. Do not let anyone tell you otherwise.",
        "Some days the weight just shows up and you did not ask for it. That is not your fault.",
        "Cry if you need to. Rest if you need to. There is no correct way to get through a sad day.",
        "Tomorrow does not have to look like today. But for now, just let today be what it is.",
        "You matter, even on the days when everything feels heavy and nothing feels right.",
        "I am glad you wrote this down. Sadness named is sadness that starts to shrink, just a little.",
    ],

    # ── ANGER ────────────────────────────────────────────────
    ("Negative", "Anger"): [
        "Yeah, that sounds genuinely frustrating. Your anger makes complete sense here.",
        "Something crossed a line for you today and you felt it clearly. That reaction is fair.",
        "I am not going to tell you to calm down. What you are feeling is real and it is valid.",
        "Anger like this usually points at something that really matters to you. What is it protecting?",
        "You are allowed to be furious. The important thing is you wrote it here instead of letting it eat you.",
        "Whatever happened today was enough to make you feel this way, and that tells me it was serious.",
        "That frustration in your words is completely understandable. Anyone in your position would feel the same.",
        "Strong reactions come from strong caring. You care a lot about this. That is not a bad thing.",
        "It is okay to be angry. Just try not to let it make any big decisions for you tonight.",
        "Writing this out was a smart move. Anger needs somewhere to go and paper is a good place.",
        "You are not wrong for feeling this. The question is what you want to do with it now.",
        "Let it out here. All of it. That is exactly what this space is for.",
        "The fire in what you wrote is real. Just give it a little time before you act on it.",
        "Sometimes things genuinely deserve our anger. Today might be one of those times.",
    ],

    # ── ANXIETY ──────────────────────────────────────────────
    ("Negative", "Anxiety"): [
        "Your mind is spinning right now and that is exhausting. Let me just say, you are safe in this moment.",
        "Anxiety lies to you. It makes things feel more certain and more dangerous than they actually are.",
        "You have gotten through every hard day you have ever had. That is a perfect record.",
        "I know the worry feels very real and very loud right now. Try to come back to just this minute.",
        "You do not have to solve everything tonight. Some things will sort themselves out without you touching them.",
        "That feeling of being overwhelmed is so uncomfortable. Take one breath before you do anything else.",
        "Your brain is trying to protect you by thinking ahead. It is just being a little too enthusiastic about it.",
        "Most of what anxiety predicts never actually arrives. The future is still open, not decided.",
        "One small step. Just one. You do not owe anyone a perfect solution right now.",
        "The thoughts are loud but they are not facts. Come back to what is actually real around you right now.",
        "You have survived every difficult moment in your life so far. This one is no different.",
        "Put down everything except this single moment. Just this breath. Just right now.",
        "You are not your anxiety. You are the person noticing the anxiety. That distance matters.",
        "It is okay to not be okay. It is okay to feel this. It will not feel like this forever.",
    ],

    # ── EXHAUSTION ───────────────────────────────────────────
    ("Negative", "Exhaustion"): [
        "You sound tired in a way that goes deeper than just needing sleep. Please rest, properly.",
        "You have been giving a lot of yourself lately. It makes complete sense that you are running low.",
        "Rest is not giving up. Rest is what makes it possible to keep going tomorrow.",
        "Your body is telling you something very clearly right now. It would be worth listening.",
        "There is no prize for running yourself into the ground. Please take care of yourself.",
        "That kind of exhaustion does not come from doing nothing. You have been working really hard.",
        "You are allowed to stop. Actually stop, not just slow down slightly. Give yourself that.",
        "The world will still be here tomorrow. Your responsibilities will still be there. But so will you, rested.",
        "Being this tired means you have been showing up consistently for a long time. That counts.",
        "You cannot pour anything from an empty container. Fill yours first, please.",
        "It takes courage to admit you are running out of steam. You just did that. Now act on it.",
        "Even one small act of rest today will make tomorrow slightly more manageable.",
        "Please do not push through this one. Rest through it instead.",
        "You have been doing a lot. It is time to do a little less, just for today.",
    ],

    # ── LONELINESS ───────────────────────────────────────────
    ("Negative", "Loneliness"): [
        "That feeling of being disconnected from everyone is one of the hardest things a person can feel.",
        "Feeling invisible is painful and real. I want you to know that you are seen, at least right here.",
        "Loneliness does not mean you are unlikeable. It means the right connection has not shown up yet today.",
        "The fact that you wrote this means some part of you is reaching out. That is a healthy instinct.",
        "You deserve people who see you and appreciate you. Not having that right now is genuinely hard.",
        "Being surrounded by people and still feeling alone is sometimes the loneliest kind of lonely.",
        "This feeling is temporary even when it does not feel that way. People find their people.",
        "You are not invisible even when everything makes you feel like you are.",
        "Writing here instead of sitting alone with it was a good choice. Always a good choice.",
        "Whatever distance exists between you and others right now, it is not permanent.",
        "You have something real to offer the world. The right people will see that.",
        "Connection often starts with honesty about needing it. You just did that. That is a start.",
        "I am sorry today felt lonely. You deserved better company than you got.",
    ],

    # ── CONFUSION ────────────────────────────────────────────
    ("Negative", "Confusion"): [
        "Not knowing what you think or feel is its own kind of uncomfortable. That is completely normal.",
        "You do not have to have this figured out today. Give yourself permission to not know yet.",
        "Confusion often shows up right before clarity does. You might be closer than you think.",
        "The fact that things feel tangled right now does not mean they will stay that way.",
        "It is okay to say I do not know. In fact it is one of the most honest things you can say.",
        "Your brain is working through something complicated. Give it the time it is asking for.",
        "Most good decisions were made from exactly this messy, unclear place you are in right now.",
        "You do not need the full picture. Just the next single step. Start there and only there.",
        "Uncertainty is uncomfortable but it is also honest. You are being real with yourself.",
        "The fog does lift. It always does. You just cannot usually see that from inside it.",
        "Writing about confusion, even if it sounds messy, is still a step toward making sense of it.",
        "Take the pressure off yourself to have the answer. Sometimes sitting with the question is the work.",
        "You are between two knowings right now. That space is uncomfortable but it is temporary.",
    ],

    # ── NEUTRAL ──────────────────────────────────────────────
    ("Neutral", "Neutral"): [
        "Not every day has a big headline. Steady and ordinary is actually a pretty good day.",
        "An even keel is honestly underrated. You sound balanced and that is worth something.",
        "Some days just are. Not good, not bad, just Tuesday. And that is perfectly fine.",
        "You checked in with yourself today even when nothing dramatic was happening. That habit matters.",
        "Ordinary days are the foundation of a life. You are building yours quietly. That counts.",
        "There is real peace in a day that does not demand too much from you.",
        "Balanced is not boring. Balanced is grounded, and grounded is strong.",
        "Nothing remarkable to report is sometimes exactly the kind of day your nervous system needed.",
        "You showed up for this, even on a quiet day. The consistency is the whole point.",
        "Some days you ride the wave. Some days you just float. Both are fine.",
        "A calm day is a day where nothing bad won. That is always a small win.",
        "Equanimity is a skill. You are practising it without even trying.",
    ],

    ("Neutral", "Calm"): [
        "You sound settled today. That kind of inner quiet is something a lot of people are chasing.",
        "Calm is not the absence of anything. It is its own kind of fullness. Enjoy it.",
        "There is real strength in this steadiness. Not everyone finds it.",
        "Whatever you tackle today, you will tackle it with a clear head. That is a good starting position.",
        "This kind of peace tends to spill over into everything you do. Let it.",
        "Calm days are the best days to make good decisions. Use this one well.",
        "You have found a quiet today that a lot of people spend years looking for.",
        "That stillness in your words feels earned. Rest in it a little.",
        "Grounded is one of the best things a person can be. You are there today.",
        "When the harder days come back around, remember this is also what you are capable of feeling.",
        "The world is loud. The fact that you found quiet in it today is genuinely good.",
        "Savour this. Not every day hands you this kind of peace.",
    ],

    ("Neutral", "Unease"): [
        "Something feels off and you cannot quite put your finger on it. That vague feeling is real and worth noticing.",
        "Your gut is picking something up before your brain has caught up. That is worth paying attention to.",
        "Not every uncomfortable feeling has a clear name. Sometimes it is just a signal asking for attention.",
        "You noticed something was off instead of pushing past it. That awareness is a good thing.",
        "Vague discomfort is still discomfort. It does not need a label to be taken seriously.",
        "Sometimes the body knows before the mind does. Try to listen without forcing an answer.",
        "You do not need to solve this right now. Just noticing it is already doing something useful.",
        "That unsettled feeling often means something is trying to surface. Let it come up in its own time.",
        "It is okay to sit with an unclear feeling for a while. Clarity usually comes, just not on demand.",
        "There might be something you have been putting off thinking about. This might be its way of knocking.",
        "The fog has a way of lifting when you stop trying to blow it away.",
        "Whatever this is, you are more capable of handling it than you feel right now.",
    ],
}

# ─────────────────────────────────────────────────────────────
#  COPING TIPS — practical, simple, actually doable
# ─────────────────────────────────────────────────────────────
COPING_TIPS = {
    "Joy": [
        "Write down exactly what made today feel this way. Future you will want to remember this.",
        "Send a message to one person you care about and share something good. Shared joy doubles.",
        "Do one spontaneous thing that matches how you feel — dance, go outside, call someone.",
        "Take a photo of something beautiful around you right now, just to mark the moment.",
        "Tell one person out loud about something good that happened today.",
    ],
    "Hope": [
        "Write down three small actions you can take this week toward what you are looking forward to.",
        "Share your optimism with someone who could use it today.",
        "Take one tiny step toward what you are hoping for. Even five minutes is a real beginning.",
        "Write a short paragraph about what life looks like when this hope comes true.",
        "Spend time today with people who believe in you and what you are working toward.",
    ],
    "Gratitude": [
        "Write a real thank-you message to someone who helped you recently, even if you never send it.",
        "Start a simple note in your phone called tiny good things and add one thing to it right now.",
        "Tell one person today specifically why you appreciate them.",
        "Spend ten quiet minutes appreciating something you usually take completely for granted.",
        "Put your phone down for a bit and just experience something you are grateful for.",
    ],
    "Pride": [
        "Write down exactly what you did to get here, step by step. Save it somewhere you will find it.",
        "Tell one person about what you achieved today. Say it out loud.",
        "Do something small to mark this moment — write it down, buy yourself something, take a picture.",
        "Sit with this feeling for five whole minutes before moving on to the next thing.",
        "Think about who helped or inspired you to reach this and find a way to thank them.",
    ],
    "Sadness": [
        "Name five things you can physically see right now. It helps bring you back to the present.",
        "Put on one song that fits exactly how you feel and let yourself feel it for three full minutes.",
        "Reach out to one person — you do not need to explain anything, just say you need some company.",
        "Make something warm for yourself right now, a drink, a blanket. Let the physical comfort come first.",
        "Write a letter to the sadness and ask it what it needs from you today.",
    ],
    "Anger": [
        "Try this before doing anything: breathe in for four counts, hold four, out for four, hold four. Repeat.",
        "Write everything you want to say to whoever sparked this — uncensored. You never have to send it.",
        "Move your body. Walk fast, do push-ups, stretch. Anger lives in the muscles and needs an exit.",
        "Give yourself a twenty-minute pause before acting on anything. Not to suppress it, to channel it better.",
        "Ask yourself what boundary was crossed and what you actually need here.",
    ],
    "Anxiety": [
        "Write every anxious thought down on paper, then close the notebook. Tell yourself you will come back to it later.",
        "Put both feet flat on the floor. Name five things you can physically touch right now.",
        "Ask yourself: is this thought a fact or a prediction? Most anxiety lives in predictions.",
        "Set a ten-minute worry time. Worry hard during it. Then stop and do something else.",
        "Call or text one person right now. Connection is the fastest antidote to anxious isolation.",
    ],
    "Exhaustion": [
        "Give yourself permission to cancel one non-essential thing today. Rest is a real priority.",
        "Try twenty minutes of lying down with no screen, in a dark room. Not sleep, just stillness.",
        "Write down five things you can take off your plate this week, even temporarily.",
        "Drink a full glass of water and eat something small. Exhaustion is often partly physical.",
        "Say no to one thing today without any explanation or apology. Just: I cannot right now.",
    ],
    "Loneliness": [
        "Send one genuine message to someone you have not spoken to in a while. Keep it simple.",
        "Spend thirty minutes somewhere with people around even if you do not talk to anyone.",
        "Write about the kind of connection you are really craving. Getting specific helps.",
        "Call one person on the phone instead of texting. The voice makes a real difference.",
        "Look for one community around something you love, online or local, and just look today.",
    ],
    "Confusion": [
        "Write everything in your head for ten minutes with no filter. Then read it back.",
        "Talk to someone you trust, not for advice, just to think out loud. Clarity often comes through speaking.",
        "Break whatever is confusing you into the smallest possible question you could answer today.",
        "Step away from it for a few hours. Your brain keeps working even when you stop pushing.",
        "Draw the confusion out on paper, boxes, arrows, anything. Sometimes the eyes see what the mind cannot.",
    ],
    "Neutral": [
        "Use this calm window for something you have been putting off. Steady days are good for quiet progress.",
        "Take a fifteen-minute walk without your phone and let your mind go wherever it wants.",
        "Write about something you are curious about lately and follow that thread.",
        "Do one small thing today that makes tomorrow a little easier.",
        "Check in with someone who might be having a harder day than you.",
    ],
    "Calm": [
        "Use this stillness to do something creative. Calm is the best state for making things.",
        "Read something slowly today, a book, a poem, something that rewards a quiet mind.",
        "Plan something you have been meaning to organise. This clear head is a good time for it.",
        "Share this calm energy with someone who is struggling today.",
        "Try five minutes of just sitting quietly. No task, no phone, just being.",
    ],
    "Unease": [
        "Sit quietly and ask yourself where in your body you feel this. What does it feel like physically?",
        "Write freely for ten minutes about everything that has been on your mind. No editing.",
        "Check the basics first. Have you slept, eaten, moved, connected with someone recently?",
        "Try to give this feeling a more specific name than just off. Naming it often shrinks it.",
        "Do one small thing today that feels like taking care of yourself. Anything counts.",
    ],
}

FALLBACK_RESPONSES = [
    "Whatever you are carrying today, you showed up and wrote it down. That is not nothing.",
    "Your feelings are real and they matter, even if they are hard to name right now.",
    "Every time you check in honestly with yourself you are doing something most people never do.",
    "Thank you for writing this. The act of putting it into words already does something useful.",
    "You deserve support exactly as you are, not after you have figured everything out.",
]

FALLBACK_TIPS = [
    "Take three slow breaths right now. In for four counts, out for six. Just start there.",
    "Drink some water and step outside for five minutes. Reorient yourself physically first.",
    "Write two more sentences about how you are feeling. The second layer often holds the real answer.",
    "Reach out to one person today, even just a small message. Connection helps.",
    "Do one small thing that makes your immediate environment more comfortable.",
]

def generate_response(sentiment: str, emotions: list) -> dict:
    primary = emotions[0] if emotions else "Neutral"
    key     = (sentiment, primary)

    if key in RESPONSES:
        response = random.choice(RESPONSES[key])
    else:
        fallback_key = (sentiment, "Neutral")
        response = random.choice(RESPONSES.get(fallback_key, FALLBACK_RESPONSES))

    tip_pool = COPING_TIPS.get(primary, COPING_TIPS.get("Neutral", FALLBACK_TIPS))
    tip      = random.choice(tip_pool)

    return {"response": response, "tip": tip}
