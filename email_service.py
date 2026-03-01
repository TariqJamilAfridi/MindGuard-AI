import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text      import MIMEText
from datetime             import datetime

# ── CONFIG — fill these in before running ─────────────────
# Go to Gmail → Settings → Security → App Passwords → Create
# Use that 16-char app password here (NOT your Gmail login password)
GMAIL_USER     = "tariq347146@gmail.com"     # <-- change this
GMAIL_PASSWORD = "rcxh yxif sump mdtp"   # <-- change this
APP_NAME       = "MindGuard"


def send_welcome_email(user_name: str, user_email: str) -> bool:
    """Sent immediately after registration."""
    subject = f"Welcome to MindGuard, {user_name} 🧠✨"
    html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8"/>
<style>
  body   {{ font-family:'Segoe UI',Arial,sans-serif; background:#080b0e; margin:0; padding:0; }}
  .wrap  {{ max-width:560px; margin:40px auto; background:#0f1317;
             border:1px solid rgba(255,255,255,0.07); border-radius:16px; overflow:hidden; }}
  .hero  {{ background:linear-gradient(135deg,#1a1208,#0a1510);
             padding:44px 40px 36px; text-align:center; border-bottom:1px solid rgba(255,255,255,0.06); }}
  .orb   {{ width:64px;height:64px;border-radius:50%;
             background:conic-gradient(#c9a96e,#82b09a,#c97a62,#c9a96e);
             margin:0 auto 18px; }}
  h1     {{ font-family:Georgia,serif; color:#e9e4dc; font-size:1.9rem;
             font-weight:400; margin:0 0 8px; }}
  .sub   {{ color:#a09890; font-size:.9rem; margin:0; }}
  .body  {{ padding:36px 40px; }}
  p      {{ color:#a09890; line-height:1.75; font-size:.92rem; margin:0 0 18px; }}
  .hi    {{ color:#e9e4dc; font-family:Georgia,serif; font-size:1.2rem;
             font-style:italic; margin-bottom:20px; }}
  .cta   {{ display:block; width:fit-content; margin:28px auto 0;
             background:linear-gradient(135deg,#c9a96e,#b8924a);
             color:#080b0e; text-decoration:none;
             padding:13px 32px; border-radius:8px;
             font-weight:600; font-size:.88rem; letter-spacing:.05em;
             text-transform:uppercase; }}
  .features {{ display:flex; gap:16px; margin:28px 0; }}
  .feat  {{ flex:1; background:#171c21; border:1px solid rgba(255,255,255,0.06);
             border-radius:10px; padding:16px; text-align:center; }}
  .feat .icon {{ font-size:1.4rem; margin-bottom:8px; }}
  .feat .name {{ color:#c9a96e; font-size:.78rem; font-weight:600;
                 letter-spacing:.06em; text-transform:uppercase; }}
  .foot  {{ padding:20px 40px; border-top:1px solid rgba(255,255,255,0.06);
             text-align:center; }}
  .foot p{{ color:#5a5550; font-size:.75rem; margin:0; }}
</style>
</head>
<body>
<div class="wrap">
  <div class="hero">
    <div class="orb"></div>
    <h1>Welcome to MindGuard</h1>
    <p class="sub">Your quiet corner for emotional clarity</p>
  </div>
  <div class="body">
    <p class="hi">Hello, {user_name} —</p>
    <p>You've just taken a meaningful step toward understanding yourself better.
       MindGuard is your private, judgment-free space to check in with how you're
       really feeling — every single day.</p>
    <p>Here's what you can do:</p>
    <div class="features">
      <div class="feat">
        <div class="icon">✍️</div>
        <div class="name">Journal</div>
      </div>
      <div class="feat">
        <div class="icon">📊</div>
        <div class="name">Track</div>
      </div>
      <div class="feat">
        <div class="icon">🎙️</div>
        <div class="name">Speak</div>
      </div>
      <div class="feat">
        <div class="icon">🔥</div>
        <div class="name">Streak</div>
      </div>
    </div>
    <p>Write your first entry today. Even just a few sentences. Your future self will
       thank you for starting now.</p>
    <a class="cta" href="http://127.0.0.1:5000">Open MindGuard →</a>
  </div>
  <div class="foot">
    <p>MindGuard is a personal wellness companion, not a clinical tool.<br>
       If you're struggling, please reach out to a mental health professional.</p>
  </div>
</div>
</body>
</html>
"""
    return _send(user_email, subject, html)


def send_weekly_digest(user_name: str, user_email: str,
                       total: int, positive: int, negative: int,
                       top_emotion: str, streak: int,
                       insight: str) -> bool:
    """Weekly mood summary digest."""
    subject = f"Your MindGuard Weekly Digest 📊 — {datetime.now().strftime('%b %d')}"

    pct = round((positive / total * 100)) if total else 0
    mood_color = "#82b09a" if pct >= 60 else "#c97a62" if pct < 40 else "#c9a96e"

    html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8"/>
<style>
  body   {{ font-family:'Segoe UI',Arial,sans-serif; background:#080b0e; margin:0; padding:0; }}
  .wrap  {{ max-width:560px; margin:40px auto; background:#0f1317;
             border:1px solid rgba(255,255,255,0.07); border-radius:16px; overflow:hidden; }}
  .hero  {{ padding:36px 40px 28px; background:#0f1317;
             border-bottom:1px solid rgba(255,255,255,0.06); }}
  .week  {{ color:#5a5550; font-size:.72rem; letter-spacing:.1em;
             text-transform:uppercase; margin-bottom:8px; }}
  h1     {{ font-family:Georgia,serif; color:#e9e4dc; font-size:1.7rem;
             font-weight:400; margin:0; }}
  .body  {{ padding:32px 40px; }}
  .stats {{ display:grid; grid-template-columns:1fr 1fr 1fr; gap:12px; margin-bottom:28px; }}
  .stat  {{ background:#171c21; border:1px solid rgba(255,255,255,0.06);
             border-radius:10px; padding:18px 14px; text-align:center; }}
  .sv    {{ font-family:Georgia,serif; font-size:1.8rem; font-weight:600;
             color:#c9a96e; line-height:1; margin-bottom:4px; }}
  .sl    {{ color:#5a5550; font-size:.68rem; text-transform:uppercase; letter-spacing:.08em; }}
  .bar-wrap {{ background:#171c21; border-radius:10px; padding:20px; margin-bottom:20px; }}
  .bar-label {{ color:#a09890; font-size:.8rem; margin-bottom:10px; }}
  .bar-outer {{ background:#1e252c; border-radius:4px; height:8px; }}
  .bar-inner {{ height:8px; border-radius:4px; background:{mood_color};
                width:{pct}%; transition:width .8s ease; }}
  .bar-pct   {{ color:{mood_color}; font-size:.85rem; font-weight:600; margin-top:8px; }}
  .insight-box {{ background:rgba(130,176,154,0.07);
                  border-left:3px solid #82b09a; border-radius:0 8px 8px 0;
                  padding:16px 18px; margin-bottom:20px; }}
  .insight-box p {{ color:#a09890; font-size:.88rem; line-height:1.65;
                    font-style:italic; margin:0; }}
  p    {{ color:#a09890; line-height:1.75; font-size:.9rem; margin:0 0 16px; }}
  .cta {{ display:block; width:fit-content; margin:24px auto 0;
           background:linear-gradient(135deg,#c9a96e,#b8924a);
           color:#080b0e; text-decoration:none;
           padding:12px 28px; border-radius:8px;
           font-weight:600; font-size:.85rem; letter-spacing:.05em;
           text-transform:uppercase; }}
  .foot  {{ padding:18px 40px; border-top:1px solid rgba(255,255,255,0.06);
             text-align:center; }}
  .foot p{{ color:#5a5550; font-size:.72rem; margin:0; }}
</style>
</head>
<body>
<div class="wrap">
  <div class="hero">
    <div class="week">Weekly Digest — {datetime.now().strftime('%B %d, %Y')}</div>
    <h1>Here's how your week looked, {user_name}</h1>
  </div>
  <div class="body">
    <div class="stats">
      <div class="stat"><div class="sv">{total}</div><div class="sl">Entries</div></div>
      <div class="stat"><div class="sv" style="color:#82b09a">{positive}</div><div class="sl">Positive</div></div>
      <div class="stat"><div class="sv" style="color:#c97a62">{negative}</div><div class="sl">Challenging</div></div>
    </div>

    <div class="bar-wrap">
      <div class="bar-label">Positive mood rate this week</div>
      <div class="bar-outer"><div class="bar-inner"></div></div>
      <div class="bar-pct">{pct}% positive</div>
    </div>

    <div class="insight-box">
      <p>✨ {insight}</p>
    </div>

    <p>Your most felt emotion this week was <strong style="color:#c9a96e">{top_emotion}</strong>.
       {"You've been keeping up a " + str(streak) + "-day streak 🔥 — that's remarkable consistency." if streak >= 3 else "Keep showing up — even one entry a day builds something powerful over time."}</p>

    <p>Every entry you write is data about yourself — and the more you write, the clearer your
       patterns become. Your journal is waiting.</p>

    <a class="cta" href="http://127.0.0.1:5000">Open My Journal →</a>
  </div>
  <div class="foot">
    <p>MindGuard · Personal Wellness Companion · Not a clinical tool<br>
       You're receiving this because you registered at MindGuard.</p>
  </div>
</div>
</body>
</html>
"""
    return _send(user_email, subject, html)


def _send(to_email: str, subject: str, html: str) -> bool:
    """Internal helper — sends HTML email via Gmail SMTP."""
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"]    = f"{APP_NAME} <{GMAIL_USER}>"
        msg["To"]      = to_email
        msg.attach(MIMEText(html, "html"))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(GMAIL_USER, GMAIL_PASSWORD)
            server.sendmail(GMAIL_USER, to_email, msg.as_string())
        print(f"✅ Email sent to {to_email}")
        return True
    except Exception as e:
        print(f"❌ Email failed: {e}")
        return False
