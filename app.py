from flask      import Flask, request, jsonify, render_template, session, redirect, url_for, abort
from flask_cors import CORS

from database    import (init_db, save_entry, get_all_entries,
                          get_recent_entries, get_emotion_counts,
                          register_user, login_user, get_user_by_id,
                          get_all_users, get_user_stats)
from analyzer    import analyze
from ai_response import generate_response

app = Flask(__name__)
app.secret_key = "mindguard_secret_2026"
CORS(app)
init_db()

# ── Admin credentials (change before production) ───────────
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "mindguard2026"

# ─────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────
def current_user():
    uid = session.get("user_id")
    return get_user_by_id(uid) if uid else None

def is_admin():
    return session.get("is_admin", False)

# ─────────────────────────────────────────────────────────────
# USER ROUTES
# ─────────────────────────────────────────────────────────────
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/register", methods=["POST"])
def api_register():
    d = request.get_json()
    user, err = register_user(d.get("name",""), d.get("email",""), d.get("password",""))
    if err:
        return jsonify({"error": err}), 400
    session["user_id"] = user["id"]
    try:
        from email_service import send_welcome_email
        send_welcome_email(user["name"], user["email"])
    except Exception as e:
        print(f"Welcome email skipped: {e}")
    return jsonify({"user": {"id": user["id"], "name": user["name"], "email": user["email"]}}), 201

@app.route("/api/login", methods=["POST"])
def api_login():
    d    = request.get_json()
    user = login_user(d.get("email",""), d.get("password",""))
    if not user:
        return jsonify({"error": "Invalid email or password."}), 401
    session["user_id"] = user["id"]
    return jsonify({"user": {"id": user["id"], "name": user["name"], "email": user["email"]}})

@app.route("/api/logout", methods=["POST"])
def api_logout():
    session.clear()
    return jsonify({"ok": True})

@app.route("/api/me")
def api_me():
    user = current_user()
    if user:
        return jsonify({"user": {"id": user["id"], "name": user["name"], "email": user["email"]}})
    return jsonify({"user": None})

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

    anon_count = session.get("anon_count", 0) + 1
    session["anon_count"] = anon_count

    return jsonify({
        "id":         eid,
        "text":       text,
        "sentiment":  analysis["sentiment"],
        "score":      analysis["score"],
        "emotions":   analysis["emotions"],
        "response":   ai["response"],
        "tip":        ai["tip"],
        "anon_count": anon_count,
        "show_nudge": (not user) and (anon_count >= 2),
    }), 201

@app.route("/api/entries")
def get_entries():
    user = current_user()
    return jsonify(get_all_entries(user["id"] if user else None))

@app.route("/api/chart")
def get_chart():
    days = request.args.get("days", 7, type=int)
    user = current_user()
    return jsonify(get_recent_entries(days, user["id"] if user else None))

@app.route("/api/emotions")
def get_emotions():
    user = current_user()
    return jsonify(get_emotion_counts(user["id"] if user else None))

# ─────────────────────────────────────────────────────────────
# ADMIN ROUTES
# ─────────────────────────────────────────────────────────────
@app.route("/admin")
def admin_panel():
    if not is_admin():
        return redirect(url_for("admin_login"))
    return render_template("admin.html")

@app.route("/admin/login", methods=["GET","POST"])
def admin_login():
    error = None
    if request.method == "POST":
        u = request.form.get("username","")
        p = request.form.get("password","")
        if u == ADMIN_USERNAME and p == ADMIN_PASSWORD:
            session["is_admin"] = True
            return redirect(url_for("admin_panel"))
        error = "Invalid credentials."
    return render_template("admin_login.html", error=error)

@app.route("/admin/logout")
def admin_logout():
    session.pop("is_admin", None)
    return redirect(url_for("admin_login"))

# ── Admin API ─────────────────────────────────────────────
@app.route("/api/admin/users")
def api_admin_users():
    if not is_admin(): return jsonify({"error":"Unauthorized"}), 403
    return jsonify(get_all_users())

@app.route("/api/admin/user/<int:uid>/entries")
def api_admin_user_entries(uid):
    if not is_admin(): return jsonify({"error":"Unauthorized"}), 403
    return jsonify(get_all_entries(uid))

@app.route("/api/admin/stats")
def api_admin_stats():
    if not is_admin(): return jsonify({"error":"Unauthorized"}), 403
    return jsonify(get_user_stats())

@app.route("/api/admin/entries/all")
def api_admin_all_entries():
    if not is_admin(): return jsonify({"error":"Unauthorized"}), 403
    return jsonify(get_all_entries())   # no user_id = all entries

if __name__ == "__main__":
    print("🧠 MindGuard → http://127.0.0.1:5000")
    print("🔐 Admin Panel → http://127.0.0.1:5000/admin")
    app.run(debug=True)
