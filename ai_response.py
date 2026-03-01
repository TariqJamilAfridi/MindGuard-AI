import random

# ═══════════════════════════════════════════════════════════════════
#  MINDGUARD — ai_response.py
#  Expanded response library: 13 unique responses per emotion
#  Written in warm, literary, human-feeling language.
#  Every call to generate_response() will feel fresh and personal.
# ═══════════════════════════════════════════════════════════════════

RESPONSES = {

    # ──────────────────────────────────────────────
    ("Positive", "Joy"): [
        "There's something quietly magical about a day that genuinely feels good — hold this one close, because you've earned it.",
        "Joy like this doesn't need a reason. It just needs to be felt fully, without apology.",
        "The way you're feeling right now? That's not luck. That's you aligned with something true.",
        "Happiness looks good on you. Let it stay as long as it wants.",
        "Days like this are worth remembering — not just living through. Savour every corner of it.",
        "Your joy today is its own kind of medicine. Let it spill over into everything you do.",
        "Something about the way you wrote this feels like sunshine through a window. Beautiful.",
        "Not every day sparkles — but this one clearly does. You deserve this brightness.",
        "This is the kind of day that makes the harder ones worth enduring. Soak it in completely.",
        "Joy is contagious, even in writing. I can feel the lightness in your words.",
        "There's real power in noticing when things are good. That awareness is a gift you give yourself.",
        "Whatever opened today's door to happiness — remember it. It's worth finding again.",
        "Some days just fit right. This sounds like one of them. Keep going exactly as you are.",
    ],

    ("Positive", "Hope"): [
        "Hope is one of the bravest things a person can hold onto — especially when it hasn't been proven yet.",
        "The fact that you're looking forward says everything about your strength. Keep that vision alive.",
        "Something is opening up for you, and you can feel it. Trust that instinct completely.",
        "Hope isn't naive — it's a decision. And you've made a really good one today.",
        "That spark you're feeling? Protect it. Not every day will fan it, but today it's burning bright.",
        "When you look ahead with this kind of light in your eyes, the path has a way of appearing.",
        "You're not just wishing — you're believing. There's a difference, and you've crossed it.",
        "Whatever you're moving toward, this feeling is your compass. Follow it.",
        "Hope that comes from within is unshakeable. What you're carrying today is real.",
        "Even the smallest seed of optimism, well-tended, can become something extraordinary.",
        "You're standing at a beginning and you know it. That clarity is rare. Honour it.",
        "The world needs more people who still believe in what's possible. You're one of them.",
        "This kind of forward-looking energy is the foundation every good chapter is built on.",
    ],

    ("Positive", "Gratitude"): [
        "Gratitude is the quiet art of finding gold in ordinary days — and you've mastered it today.",
        "There's something profound about pausing long enough to notice what's good. You just did that.",
        "A thankful heart isn't a passive one — it's one that pays close attention. Yours clearly does.",
        "The things you're appreciating today have always been there. Today you finally saw them fully.",
        "Gratitude rewires us. What you're practising right now is one of the most powerful things a person can do.",
        "Every 'thank you' you carry inside you makes the world fractionally warmer. Yours counts.",
        "You didn't have to notice the good things — but you did. That choice matters more than you know.",
        "This kind of awareness is rare. Most people walk past the beautiful things. You stopped.",
        "What you're feeling is the softest, strongest emotion there is. Let it settle into you.",
        "Counting blessings isn't a cliché when you truly mean it — and it's clear that you do.",
        "The fact that you feel grateful means something went right today, and you noticed. Perfect.",
        "Gratitude doesn't make hard things disappear — it just reminds you there's also this. And this is good.",
        "You've found something worth holding. Don't let the busyness of tomorrow make you forget it.",
    ],

    ("Positive", "Pride"): [
        "You did that. No one else. Take a breath and let yourself actually feel how far you've come.",
        "Pride only feels this good when it's earned — and yours clearly is.",
        "This moment is the payoff for every quiet hour you put in that nobody saw.",
        "Don't rush past this feeling. You worked for it. You deserve to sit in it for a while.",
        "Achievement has a particular weight when it comes from persistence. What you're feeling is real.",
        "The version of you from a few months ago would be so proud of where you are right now.",
        "You built this. Brick by brick, choice by choice, day by day. Look at it.",
        "Not everyone would have kept going when it got hard. But you did. That's the whole story.",
        "This kind of accomplishment doesn't fade — it becomes part of who you are permanently.",
        "Wear this pride gently but fully. You've become someone today who wasn't there before.",
        "Every milestone you reach makes the next one more believable. You've just made something possible.",
        "Celebrate this properly. Not tomorrow — right now, today, exactly as it is.",
        "There are people who wish for what you just did. And you actually went and did it.",
    ],

    ("Negative", "Sadness"): [
        "Sadness doesn't mean something went wrong — sometimes it just means you loved something deeply.",
        "You don't have to explain this feeling or fix it right now. Just let it be what it is.",
        "There's a strange kind of courage in sitting with sadness rather than running from it. You're doing that.",
        "The heaviness you're carrying today is real, and it's okay that it's heavy. You don't have to pretend otherwise.",
        "Grief, in all its forms, deserves to be felt — not rushed through. Take all the time you need.",
        "It's okay to cry. It's okay to feel hollow. It's okay to not be okay today.",
        "Some days the weight is just there, and that's not your fault and it's not a failure.",
        "You came here and wrote this down instead of carrying it silently. That took something real.",
        "The fact that you feel this deeply says something beautiful about how much you care.",
        "Sadness is not permanent, even when it feels like the only landscape you've ever known.",
        "Be very gentle with yourself today. Treat yourself the way you'd treat someone you love who's hurting.",
        "Even on the darkest days, you are not alone in this — and tomorrow doesn't have to look like today.",
        "Whatever made your heart heavy today — it matters, because you matter.",
        "You're allowed to be sad. Fully, completely, without apology. That's not weakness. That's humanity.",
    ],

    ("Negative", "Anger"): [
        "Your anger makes complete sense. Something crossed a line, and you felt it clearly.",
        "Frustration this real usually means something that matters to you was treated like it didn't.",
        "It's okay to be angry. The important thing is you're here, naming it, rather than letting it fester alone.",
        "There's information in this feeling — it's pointing at something that needs to change.",
        "You're allowed to be furious. Just don't let it make decisions for you before you've had a breath.",
        "Anger is often love in a different outfit — protection of something or someone that matters.",
        "The fire in what you wrote tells me you care deeply. That's not a flaw. That's integrity.",
        "Let yourself feel this fully, and then gently ask: what does this anger want me to know?",
        "You don't need to perform calm right now. The frustration is valid. Just breathe when you can.",
        "Strong emotion means strong investment. You care. That's never the wrong thing.",
        "This feeling has a message for you if you listen to it carefully enough. What is it really saying?",
        "Even the sharpest anger softens with time. You won't feel this exact intensity forever.",
        "What happened to you today was real and your reaction to it is completely understandable.",
        "Sometimes the world genuinely deserves the frustration we give it. Today might be one of those times.",
    ],

    ("Negative", "Anxiety"): [
        "Your mind is running fast right now, and that's exhausting. You're safe here. Slow it down a little.",
        "Anxiety lies to you about how permanent and total the danger is. Most of what it predicts never arrives.",
        "You have survived every difficult day that came before this one. That's a perfect record.",
        "The weight of worry you're carrying didn't appear overnight — be patient with yourself as it lifts.",
        "Breathe first. The thoughts will still be there in two minutes, but your body will be calmer.",
        "One breath. One moment. One tiny step. That's all that's being asked of you right now.",
        "Your nervous system is trying to protect you. It's just a little over-eager today. That's okay.",
        "The spiral is loud, but it's not the truth. Come back to what's real: the floor, the air, this moment.",
        "Everything doesn't have to be solved tonight. Some things will resolve themselves without your help.",
        "Anxiety makes the future feel certain and terrible. But the future is neither — it's still open.",
        "You've worried before and made it through. Your track record of surviving difficult days is 100%.",
        "The thoughts rushing through you are clouds, not the sky. Let them pass without chasing them.",
        "Right now, in this exact second, you are okay. Hold just that — just this second.",
        "You are not your anxiety. You are the one who notices it. That distance is everything.",
    ],

    ("Negative", "Exhaustion"): [
        "You've been giving so much for so long. The tiredness you feel is the receipt — proof you showed up.",
        "Rest is not laziness. Rest is the thing that makes everything else possible. You need it and deserve it.",
        "Your body is speaking clearly right now. It's saying: enough for today. Please listen.",
        "The kind of tired you're describing doesn't come from doing nothing. It comes from caring too much, too long.",
        "It's okay to stop pushing today. The world will still be there tomorrow — and so will you.",
        "Sometimes the most productive thing you can do is genuinely, completely rest. This is that time.",
        "Exhaustion is your nervous system asking — very firmly — to be taken care of. Honour that ask.",
        "You can't pour from an empty cup. Before you do anything else, fill yours.",
        "The fatigue in your words is real. Please don't push through this one — rest through it instead.",
        "Everyone around you may keep going, but your pace is yours alone. And your pace says: slow down.",
        "There's a difference between giving up and knowing when to stop. This is you knowing. That's wisdom.",
        "Being this tired means you've been incredibly present and giving. Now be that present with yourself.",
        "Put down whatever you're carrying that isn't essential tonight. Tomorrow you'll carry it better rested.",
        "Your mind and body are one conversation, and right now they're both saying the same thing: rest.",
    ],

    ("Negative", "Loneliness"): [
        "Loneliness is the ache of connection deferred — it means you have real love to give. Don't forget that.",
        "Feeling unseen doesn't mean you are unseen. It means the right eyes haven't landed on you yet today.",
        "You reached out here, and that matters. Even this small act says: I want to be known. That's brave.",
        "The silence around you right now is not a verdict on your worth. It's just quiet. It will shift.",
        "You are not as alone in this as the loneliness wants you to believe. That feeling lies about its scale.",
        "Some of the most connected people in the world have written from the exact place you're writing from.",
        "Being lonely doesn't mean unloved — it means the love around you isn't visible enough right now.",
        "Your presence matters, even when no one is reflecting that back to you. Especially then.",
        "Connection starts with being honest about the lack of it. You just did something really hard.",
        "Whatever has created this distance — it is not permanent, and it is not your fault.",
        "The world is full of people who would be deeply glad to know you. They just haven't found you yet.",
        "You deserve warmth and company and people who get it. You haven't had enough of that lately.",
        "Writing down the loneliness shrinks it, just a little. Keep writing. Keep naming it.",
    ],

    ("Negative", "Confusion"): [
        "Not knowing is its own kind of discomfort — but it also means the next chapter hasn't been written yet.",
        "Confusion often arrives just before clarity. You may be closer to understanding than it feels.",
        "You don't have to have the answer today. Sitting in the question is valid and important.",
        "The messiness you're feeling in your head right now isn't permanent — it's a process.",
        "Most great decisions started exactly here: in the tangled, unclear middle. You're in good company.",
        "It's okay to not know. It's okay to say 'I don't understand this yet.' That honesty is a foundation.",
        "Uncertainty isn't failure — it's the accurate description of a situation that's genuinely complex.",
        "Your mind is working hard to make sense of something that doesn't quite make sense yet. Give it time.",
        "Sometimes the fog has to thicken before it lifts completely. You might be right at that turning point.",
        "Being lost is always temporary. Direction always eventually appears — but it rarely appears on demand.",
        "What you're feeling is the sensation of being between two knowings. That space is real and valid.",
        "You don't need the full map. You just need to know the next one step. Start there.",
        "Confusion is the mind asking for gentleness. Be generous with yourself while it finds its footing.",
    ],

    ("Neutral", "Neutral"): [
        "Not every day has a headline. Some are just steady — and steady is quietly wonderful.",
        "Ordinary days are the texture of a good life. Today sounds like one worth living.",
        "There's a particular kind of peace in an unremarkable day. You may be sitting in it right now.",
        "Checking in with yourself, even on a quiet day, is its own kind of practice. Well done.",
        "Not up, not down — just here. That's perfectly fine. Sometimes presence is the whole point.",
        "A calm day is a day your nervous system got to breathe. That's not nothing — that's recovery.",
        "Some days just pass without drama, and the next morning you realise they were exactly what you needed.",
        "The fact that you showed up to write today, even without a big feeling — that consistency matters.",
        "Equanimity is underrated. The groundedness you're feeling is a strength, not a lack of something.",
        "Balance doesn't always announce itself. Sometimes it's just this — a day that asked little and gave enough.",
        "There's wisdom in being able to say 'today was just okay' without needing it to be more.",
        "A quiet day well-lived is still a day well-lived. You showed up. That counts.",
    ],

    ("Neutral", "Calm"): [
        "Calm is not the absence of feeling — it's the presence of peace. You're there right now.",
        "This stillness you're carrying is earned. Let yourself rest inside it.",
        "A calm mind is a clear mind. Whatever you think through today, you'll think through well.",
        "There's enormous strength in this steadiness. Not everyone finds it, and you have it today.",
        "Calm like this is a gift to everyone around you, not just yourself.",
        "The world moves fast and loud. The fact that you've found quiet today is precious.",
        "Savour this equilibrium — not because it's rare, but because it's real and it's yours.",
        "When the storm comes again — and storms always do — remember today. This is what centre feels like.",
        "You are grounded. That is one of the best things a person can be.",
        "The peace in your words today is its own kind of medicine.",
        "Calm is the foundation everything else is built on. You're standing on solid ground.",
        "Today you gave your mind permission to be still. That's rare and that's beautiful.",
    ],

    ("Neutral", "Unease"): [
        "Something feels off and you can't quite name it — that vagueness is its own kind of uncomfortable.",
        "When the feeling has no clear source, it's often the body noticing before the mind catches up.",
        "Unease is your intuition asking to be listened to. Sit with it — it may have something to tell you.",
        "You don't have to fix this right now. Just notice it without judgment for a moment.",
        "Sometimes the unsettled feeling is a signal that something needs your attention — but gently.",
        "The fact that you noticed this and wrote it down is already a step toward understanding it.",
        "Vague discomfort is still discomfort. It deserves to be taken seriously, not dismissed.",
        "Try not to chase this feeling into a spiral. Let it be present without making it larger than it is.",
        "Whatever is beneath this unease, you're capable of facing it when it surfaces clearly.",
        "There may be something your mind is processing that it hasn't finished yet. Let it work.",
        "Unease before clarity is a known and normal thing. You may just be in the in-between.",
        "Trust that this fog will lift. It always does. You've seen it clear before.",
    ],
}

# ═══════════════════════════════════════════════════════════════════
#  COPING TIPS — 5 per emotion, randomly selected
# ═══════════════════════════════════════════════════════════════════
COPING_TIPS = {
    "Joy": [
        "Call or message someone you love and share something good that happened today — shared joy doubles.",
        "Write down exactly what made today feel this way. Future-you will want to read this.",
        "Do one spontaneous, joyful thing right now — dance, step outside, sing. Let the body join in.",
        "Take a photo of something beautiful around you right now. Not for anyone else — just to mark this moment.",
        "Give this feeling to someone else by doing one small, unexpected kind thing today.",
    ],
    "Hope": [
        "Write down three concrete small actions you can take this week toward what you're looking forward to.",
        "Share your optimism with someone who needs it — hope is contagious and costs nothing to give.",
        "Create a 'vision note': one paragraph describing what life looks like when this hope is fulfilled.",
        "Take one tiny step toward what you're hopeful about today. Even five minutes counts as a beginning.",
        "Protect your energy today — surround yourself with people and things that match this frequency.",
    ],
    "Gratitude": [
        "Write a genuine thank-you to someone who helped you recently — even an unsent letter counts.",
        "Start a 'tiny gold moments' list in your notes app. Add to it every day for one week.",
        "Tell someone in person today that you appreciate them. Be specific about exactly why.",
        "Spend five minutes writing about one thing you normally take for granted but couldn't live without.",
        "Put your phone down for 20 minutes and simply experience something you're grateful for, without documenting it.",
    ],
    "Pride": [
        "Write a detailed account of exactly what you did to get here — every hard step. Save it somewhere.",
        "Tell one person about your achievement today. Saying it out loud makes it truly real.",
        "Mark this milestone physically — write it down, buy yourself something small, take a picture.",
        "Sit with this feeling for at least five uninterrupted minutes before moving on to the next thing.",
        "Think about who inspired or helped you reach this point and find a way to acknowledge them.",
    ],
    "Sadness": [
        "Try 5-4-3-2-1 grounding: name 5 things you see, 4 you can touch, 3 you hear, 2 you smell, 1 you taste.",
        "Put on one song that matches exactly how you feel — let it carry you for three minutes without resistance.",
        "Write an uncensored letter to the sadness itself. Ask it what it needs from you.",
        "Reach out to one person — not to explain anything, just to say: I need some company today.",
        "Make something warm for yourself — a drink, a blanket, a bath — let physical comfort start there.",
    ],
    "Anger": [
        "Try box breathing before acting on anything: inhale 4s, hold 4s, exhale 4s, hold 4s. Four times.",
        "Write a letter you'll never send to whoever sparked this — uncensored, full strength, completely honest.",
        "Move your body: walk fast, do push-ups, stretch. Anger lives in the muscles — let it out physically.",
        "Ask yourself: what boundary was crossed? What do I actually need here? Let those answers guide you.",
        "Give yourself a 20-minute pause before acting — not to suppress the feeling, but to channel it well.",
    ],
    "Anxiety": [
        "Try 'worry containment': write every anxious thought down, close the notebook, say 'I'll return to you later'.",
        "Place both feet flat on the floor. Name five things you can physically feel right now. Return to the body.",
        "Ask yourself: 'Is this thought a fact or a prediction?' Most anxiety lives in predictions, not facts.",
        "Set a 10-minute worry timer. Worry intensely during it — then stop. Anxiety shrinks when given a container.",
        "Call or text one person right now. Connection is the fastest antidote to anxious isolation.",
    ],
    "Exhaustion": [
        "Give yourself permission to cancel one non-essential thing today. Rest is a legitimate priority.",
        "Try a 20-minute rest with no screens, in a dark room. Not sleep — just stillness. You'll feel the difference.",
        "Write a list of five things you can take off your plate this week, even temporarily.",
        "Drink a full glass of water and eat something — exhaustion is often partly physical depletion.",
        "Say no to one thing today without explanation. Just: 'I can't take that on right now.'",
    ],
    "Loneliness": [
        "Send one genuine message to someone you haven't spoken to in a while. Keep it simple: 'Thinking of you.'",
        "Find a community around something you love — a forum, a local club, an online group. Just look today.",
        "Spend 30 minutes somewhere with ambient human presence: a café, a library, a park. You don't have to talk.",
        "Write about the kind of connection you're really craving. Getting specific makes it easier to find.",
        "Call someone on the phone — not a text. The sound of a voice does something a message cannot.",
    ],
    "Confusion": [
        "Try a 'brain dump': write every thought for 10 minutes, no filter, no structure. Then read it back.",
        "Talk to someone who knows you well — not for advice, just to think out loud. Clarity often comes through voice.",
        "Break your biggest confusion into the smallest possible question you could answer today.",
        "Step away from the problem for a few hours. Your subconscious will keep working even when you stop.",
        "Draw or map the confusion visually — boxes, arrows, whatever feels right. Sometimes eyes see what the mind can't.",
    ],
    "Neutral": [
        "Use this calm window for something you've been putting off — steady days are made for quiet progress.",
        "Take a 15-minute walk without your phone. Let your mind wander without destination.",
        "Write about something you're curious about lately — follow the thread, see where it leads.",
        "Do one small thing today that makes tomorrow easier: prep, tidy, plan, or simply sleep early.",
        "Use this evenness to check in with someone who might be having a harder time than you right now.",
    ],
    "Calm": [
        "Use this stillness to meditate for even 5 minutes — calm days are the best ones to build that practice.",
        "Create something while you have this peace: write, draw, cook, build something that reflects this clarity.",
        "Read something slow and beautiful today — poetry, a novel, something that rewards stillness.",
        "Plan something you've been meaning to organise — the clear head you have today is a gift.",
        "Share your calm with someone who is struggling. Stability is contagious in the best way.",
    ],
    "Unease": [
        "Sit quietly for five minutes and ask your body: where do you feel this? What does it want to tell you?",
        "Write freely for 10 minutes about everything on your mind lately — unsorted, unedited, uncensored.",
        "Check the basics: have you slept enough, eaten, moved, connected with someone recently? Start there.",
        "Name the vague feeling as precisely as you can. 'Unease' becomes smaller when it has a real name.",
        "Do one thing today that feels like taking care of yourself — even something very small counts.",
    ],
}

FALLBACK_RESPONSES = [
    "Whatever you're carrying today — you showed up anyway. That matters more than you know.",
    "Every time you check in with yourself honestly, you're doing something most people never do.",
    "Your feelings are valid, complex, and worth paying attention to. Thank you for writing them down.",
    "The simple act of putting words to how you feel is more powerful than it appears. Keep doing it.",
    "You don't have to have it all figured out to deserve support. You deserve it exactly as you are.",
    "Something in you reached out today instead of staying silent. Hold onto that instinct — it's a good one.",
]

FALLBACK_TIPS = [
    "Take three slow deep breaths right now — in for four counts, out for six. Start there.",
    "Drink a glass of water and step outside for five minutes. Reorient yourself physically.",
    "Write two more sentences about how you're feeling — sometimes the second layer holds the real answer.",
    "Reach out to one person today, even just a simple message. Connection is always the right direction.",
    "Do one small thing that makes your immediate environment more comfortable or beautiful.",
]


def generate_response(sentiment: str, emotions: list) -> dict:
    primary = emotions[0] if emotions else "Neutral"
    key = (sentiment, primary)

    if key in RESPONSES:
        response = random.choice(RESPONSES[key])
    else:
        fallback_key = (sentiment, "Neutral")
        response = random.choice(RESPONSES.get(fallback_key, FALLBACK_RESPONSES))

    tip_pool = COPING_TIPS.get(primary, COPING_TIPS.get("Neutral", FALLBACK_TIPS))
    tip = random.choice(tip_pool)

    return {"response": response, "tip": tip}
