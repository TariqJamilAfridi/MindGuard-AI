from flask       import Flask, request, jsonify, render_template, session
from flask_cors  import CORS

from database    import (init_db, save_entry, get_all_entries,
                          get_recent_entries, get_emotion_counts,
                          register_user, login_user, get_user_by_id)
from analyzer    import analyze
from ai_response import generate_response

app = Flask(__name__)
app.secret_key = "mindguard_secret_2026"   # change in production
CORS(app)
init_db()


# ── Helper ─────────────────────────────────────────────────
def current_user():
    uid = session.get("user_id")
    return get_user_by_id(uid) if uid else None


# ── Pages ──────────────────────────────────────────────────
@app.route("/")
def index():
    return render_template("index.html")


# ── Auth: Register ─────────────────────────────────────────
@app.route("/api/register", methods=["POST"])
def api_register():
    d = request.get_json()
    user, err = register_user(d.get("name",""), d.get("email",""), d.get("password",""))
    if err:
        return jsonify({"error": err}), 400

    session["user_id"] = user["id"]

    # Send welcome email in background (don't block response)
    try:
        from email_service import send_welcome_email
        send_welcome_email(user["name"], user["email"])
    except Exception as e:
        print(f"Welcome email skipped: {e}")

    return jsonify({"user": {"id": user["id"], "name": user["name"], "email": user["email"]}}), 201


# ── Auth: Login ────────────────────────────────────────────
@app.route("/api/login", methods=["POST"])
def api_login():
    d = request.get_json()
    user = login_user(d.get("email",""), d.get("password",""))
    if not user:
        return jsonify({"error": "Invalid email or password."}), 401
    session["user_id"] = user["id"]
    return jsonify({"user": {"id": user["id"], "name": user["name"], "email": user["email"]}})


# ── Auth: Logout ───────────────────────────────────────────
@app.route("/api/logout", methods=["POST"])
def api_logout():
    session.clear()
    return jsonify({"ok": True})


# ── Auth: Status ───────────────────────────────────────────
@app.route("/api/me")
def api_me():
    user = current_user()
    if user:
        return jsonify({"user": {"id": user["id"], "name": user["name"], "email": user["email"]}})
    return jsonify({"user": None})


# ── Journal Entry ──────────────────────────────────────────
@app.route("/api/entry", methods=["POST"])
def submit_entry():
    d = request.get_json()
    if not d or not d.get("text","").strip():
        return jsonify({"error": "Entry text required."}), 400

    text     = d["text"].strip()
    analysis = analyze(text)
    ai       = generate_response(analysis["sentiment"], analysis["emotions"])

    user    = current_user()
    user_id = user["id"] if user else None

    eid = save_entry(text, analysis["sentiment"], analysis["score"],
                     analysis["emotions"], ai["response"], ai["tip"], user_id)

    # Count anonymous sessions for registration nudge
    anon_count = session.get("anon_count", 0) + 1
    session["anon_count"] = anon_count

    return jsonify({
        "id":          eid,
        "text":        text,
        "sentiment":   analysis["sentiment"],
        "score":       analysis["score"],
        "emotions":    analysis["emotions"],
        "response":    ai["response"],
        "tip":         ai["tip"],
        "anon_count":  anon_count,          # frontend uses this to show register nudge
        "show_nudge":  (not user) and (anon_count >= 2),
    }), 201


# ── Entries history ────────────────────────────────────────
@app.route("/api/entries")
def get_entries():
    user = current_user()
    return jsonify(get_all_entries(user["id"] if user else None))


# ── Chart data ─────────────────────────────────────────────
@app.route("/api/chart")
def get_chart():
    days = request.args.get("days", 7, type=int)
    user = current_user()
    return jsonify(get_recent_entries(days, user["id"] if user else None))


# ── Emotion counts ─────────────────────────────────────────
@app.route("/api/emotions")
def get_emotions():
    user = current_user()
    return jsonify(get_emotion_counts(user["id"] if user else None))


# ── Manual digest trigger (for demo purposes) ──────────────
@app.route("/api/send-digest", methods=["POST"])
def send_digest():
    """Call this endpoint to trigger digest emails for all eligible users."""
    try:
        from email_service import send_weekly_digest
        from database      import get_users_for_digest, mark_email_sent, get_all_entries, get_emotion_counts
    except ImportError as e:
        return jsonify({"error": str(e)}), 500

    from database import get_users_for_digest, mark_email_sent
    users = get_users_for_digest()
    sent  = 0

    for u in users:
        entries = get_all_entries(u["id"])
        if not entries:
            continue

        total    = len(entries)
        positive = sum(1 for e in entries if e["sentiment"] == "Positive")
        negative = sum(1 for e in entries if e["sentiment"] == "Negative")
        ec       = get_emotion_counts(u["id"])
        top_em   = list(ec.keys())[0] if ec else "varied"
        streak   = 0  # simplified for demo

        dominant = "Positive" if positive > negative else ("Negative" if negative > positive else "Neutral")
        insight  = (
            f"You had {positive} positive and {negative} challenging days this week. "
            + ("Keep this momentum — you're doing really well." if dominant == "Positive"
               else "Remember: asking for support is strength. You don't have to carry this alone."
               if dominant == "Negative"
               else "Your mood stayed balanced this week — that kind of steadiness is quietly powerful.")
        )

        ok = send_weekly_digest(u["name"], u["email"], total, positive, negative, top_em, streak, insight)
        if ok:
            mark_email_sent(u["id"])
            sent += 1

    return jsonify({"sent": sent, "eligible": len(users)})


if __name__ == "__main__":
    print("🧠 MindGuard starting on http://127.0.0.1:5000")
    app.run(debug=True)
