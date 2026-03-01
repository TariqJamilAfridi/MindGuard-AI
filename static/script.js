/* ═══════════════════════════════════════════════════════════
   MINDGUARD — script.js  v3
   Canvas mood animations · Voice input · Auth modals
   Registration nudge · Charts · Streak · Export
═══════════════════════════════════════════════════════════ */

// ── State ──────────────────────────────────────────────────
let allEntries  = [];
let chartObjs   = {};
let recognition = null;
let isListening = false;
let currentUser = null;
let animFrame   = null;   // requestAnimationFrame id

// Chart defaults
Chart.defaults.color       = '#5a5550';
Chart.defaults.font.family = "'Outfit', sans-serif";
Chart.defaults.font.size   = 11;
Chart.defaults.plugins.legend.display = false;


// ════════════════════════════════════════════════════════════
//  CANVAS MOOD ANIMATIONS
//  Each sentiment triggers a full-screen particle system
// ════════════════════════════════════════════════════════════
const canvas  = document.getElementById('moodCanvas');
const ctx2d   = canvas.getContext('2d');
let particles = [];
let animMode  = null;   // 'happy' | 'sad' | 'anxious' | 'exhausted' | null

function resizeCanvas() {
  canvas.width  = window.innerWidth;
  canvas.height = window.innerHeight;
}
window.addEventListener('resize', resizeCanvas);
resizeCanvas();

// ─── HAPPY — confetti burst + floating stars ───────────────
function spawnHappy() {
  particles = [];
  const colors = ['#c9a96e','#82b09a','#e8c98a','#c97a62','#fff9e6','#a8d5c2'];
  for (let i = 0; i < 160; i++) {
    const angle = Math.random() * Math.PI * 2;
    const speed = 2 + Math.random() * 6;
    particles.push({
      type:   'confetti',
      x:      canvas.width  * (.2 + Math.random() * .6),
      y:      canvas.height * (.3 + Math.random() * .4),
      vx:     Math.cos(angle) * speed,
      vy:     Math.sin(angle) * speed - 3,
      rot:    Math.random() * 360,
      rotV:   (Math.random() - .5) * 8,
      w:      6 + Math.random() * 9,
      h:      3 + Math.random() * 5,
      color:  colors[Math.floor(Math.random() * colors.length)],
      alpha:  1,
      life:   1,
    });
  }
  // Floating stars
  for (let i = 0; i < 40; i++) {
    particles.push({
      type:  'star',
      x:     Math.random() * canvas.width,
      y:     canvas.height + 30,
      vy:    -(0.5 + Math.random() * 1.5),
      size:  4 + Math.random() * 12,
      alpha: 0,
      pulse: Math.random() * Math.PI * 2,
    });
  }
}

// ─── SAD — rain drops + dark ripple ───────────────────────
function spawnSad() {
  particles = [];
  for (let i = 0; i < 120; i++) {
    particles.push({
      type:  'rain',
      x:     Math.random() * canvas.width,
      y:     -Math.random() * canvas.height,
      vy:    4 + Math.random() * 6,
      vx:    -1 + Math.random() * .5,
      len:   14 + Math.random() * 22,
      alpha: .1 + Math.random() * .35,
    });
  }
  // Ripples from bottom
  for (let i = 0; i < 6; i++) {
    particles.push({
      type:  'ripple',
      x:     canvas.width  * (.1 + Math.random() * .8),
      y:     canvas.height * (.6 + Math.random() * .35),
      r:     0,
      maxR:  80 + Math.random() * 120,
      alpha: .4,
      speed: 0.7 + Math.random() * .5,
    });
  }
}

// ─── ANXIOUS — electric pulse rings ───────────────────────
function spawnAnxious() {
  particles = [];
  const cx = canvas.width  / 2;
  const cy = canvas.height / 2;
  for (let i = 0; i < 12; i++) {
    particles.push({
      type:  'pulse',
      x: cx, y: cy,
      r:     i * 30,
      maxR:  Math.max(canvas.width, canvas.height) * .8,
      alpha: .6,
      speed: 3 + i * .4,
      color: i % 2 === 0 ? '#c97a62' : '#c9a96e',
    });
  }
  // Jitter sparks
  for (let i = 0; i < 50; i++) {
    const angle = Math.random() * Math.PI * 2;
    particles.push({
      type:  'spark',
      x:  cx + Math.cos(angle) * (40 + Math.random() * 80),
      y:  cy + Math.sin(angle) * (40 + Math.random() * 80),
      vx: (Math.random() - .5) * 4,
      vy: (Math.random() - .5) * 4,
      alpha: .8,
      size:  1 + Math.random() * 2,
    });
  }
}

// ─── EXHAUSTED — slow drooping particles ──────────────────
function spawnExhausted() {
  particles = [];
  for (let i = 0; i < 60; i++) {
    particles.push({
      type:  'droop',
      x:     Math.random() * canvas.width,
      y:     -20 - Math.random() * canvas.height * .5,
      vy:    0.2 + Math.random() * .5,
      vx:    (Math.random() - .5) * .3,
      r:     3 + Math.random() * 9,
      alpha: .08 + Math.random() * .18,
      color: Math.random() > .5 ? '#5a5550' : '#1e252c',
      wobble: Math.random() * Math.PI * 2,
    });
  }
}

// ─── ANIMATION LOOP ───────────────────────────────────────
function animLoop() {
  ctx2d.clearRect(0, 0, canvas.width, canvas.height);

  if (animMode === 'happy')    drawHappy();
  if (animMode === 'sad')      drawSad();
  if (animMode === 'anxious')  drawAnxious();
  if (animMode === 'exhausted') drawExhausted();

  animFrame = requestAnimationFrame(animLoop);
}

function drawHappy() {
  particles.forEach(p => {
    if (p.type === 'confetti') {
      p.vy    += 0.12;           // gravity
      p.x     += p.vx;
      p.y     += p.vy;
      p.rot   += p.rotV;
      p.alpha -= 0.004;
      if (p.alpha <= 0) resetConfetti(p);
      ctx2d.save();
      ctx2d.globalAlpha = Math.max(0, p.alpha);
      ctx2d.translate(p.x, p.y);
      ctx2d.rotate(p.rot * Math.PI / 180);
      ctx2d.fillStyle = p.color;
      ctx2d.fillRect(-p.w/2, -p.h/2, p.w, p.h);
      ctx2d.restore();
    }
    if (p.type === 'star') {
      p.y     += p.vy;
      p.pulse += 0.04;
      p.alpha  = Math.min(.7, p.alpha + .01) * (0.6 + 0.4 * Math.sin(p.pulse));
      if (p.y < -30) resetStar(p);
      const sz = p.size;
      ctx2d.save();
      ctx2d.globalAlpha = p.alpha;
      ctx2d.fillStyle   = '#e8c98a';
      ctx2d.font        = `${sz}px serif`;
      ctx2d.fillText('✦', p.x, p.y);
      ctx2d.restore();
    }
  });
}

function resetConfetti(p) {
  const colors = ['#c9a96e','#82b09a','#e8c98a','#c97a62','#fff9e6'];
  p.x     = canvas.width  * (.1 + Math.random() * .8);
  p.y     = canvas.height * (.2 + Math.random() * .3);
  const angle = Math.random() * Math.PI * 2;
  const speed = 2 + Math.random() * 5;
  p.vx    = Math.cos(angle) * speed;
  p.vy    = Math.sin(angle) * speed - 2;
  p.alpha = .9;
  p.color = colors[Math.floor(Math.random() * colors.length)];
}

function resetStar(p) {
  p.x = Math.random() * canvas.width;
  p.y = canvas.height + 20;
  p.alpha = 0;
}

function drawSad() {
  particles.forEach(p => {
    if (p.type === 'rain') {
      p.x += p.vx;
      p.y += p.vy;
      if (p.y > canvas.height + p.len) { p.y = -p.len; p.x = Math.random() * canvas.width; }
      ctx2d.save();
      ctx2d.globalAlpha = p.alpha;
      ctx2d.strokeStyle = '#4a7a9a';
      ctx2d.lineWidth   = 1.2;
      ctx2d.beginPath();
      ctx2d.moveTo(p.x, p.y);
      ctx2d.lineTo(p.x + p.vx * 2, p.y + p.len);
      ctx2d.stroke();
      ctx2d.restore();
    }
    if (p.type === 'ripple') {
      p.r     += p.speed;
      p.alpha -= 0.004;
      if (p.alpha <= 0) { p.r = 0; p.alpha = .4; p.x = canvas.width * (.1 + Math.random() * .8); }
      ctx2d.save();
      ctx2d.globalAlpha = p.alpha;
      ctx2d.strokeStyle = '#3a5a7a';
      ctx2d.lineWidth   = 1;
      ctx2d.beginPath();
      ctx2d.arc(p.x, p.y, p.r, 0, Math.PI * 2);
      ctx2d.stroke();
      ctx2d.restore();
    }
  });
}

function drawAnxious() {
  particles.forEach(p => {
    if (p.type === 'pulse') {
      p.r     += p.speed;
      p.alpha -= 0.006;
      if (p.r > p.maxR) { p.r = 0; p.alpha = .5; }
      ctx2d.save();
      ctx2d.globalAlpha = Math.max(0, p.alpha);
      ctx2d.strokeStyle = p.color;
      ctx2d.lineWidth   = 1.5;
      ctx2d.beginPath();
      ctx2d.arc(p.x, p.y, p.r, 0, Math.PI * 2);
      ctx2d.stroke();
      ctx2d.restore();
    }
    if (p.type === 'spark') {
      p.x    += p.vx + (Math.random()-.5) * .5;
      p.y    += p.vy + (Math.random()-.5) * .5;
      p.alpha = .5 + Math.random() * .5;
      ctx2d.save();
      ctx2d.globalAlpha = p.alpha;
      ctx2d.fillStyle   = '#c97a62';
      ctx2d.beginPath();
      ctx2d.arc(p.x, p.y, p.size, 0, Math.PI * 2);
      ctx2d.fill();
      ctx2d.restore();
    }
  });
}

function drawExhausted() {
  particles.forEach(p => {
    p.wobble += 0.02;
    p.x += p.vx + Math.sin(p.wobble) * .3;
    p.y += p.vy;
    if (p.y > canvas.height + 20) { p.y = -20; p.x = Math.random() * canvas.width; }
    ctx2d.save();
    ctx2d.globalAlpha = p.alpha;
    ctx2d.fillStyle   = p.color;
    ctx2d.beginPath();
    ctx2d.arc(p.x, p.y, p.r, 0, Math.PI * 2);
    ctx2d.fill();
    ctx2d.restore();
  });
}

// ─── Trigger animation based on sentiment / emotion ───────
function triggerAnimation(sentiment, emotions) {
  if (animFrame) cancelAnimationFrame(animFrame);

  const primary = (emotions[0] || '').toLowerCase();

  if (sentiment === 'Positive' || ['joy','pride','hope','gratitude'].includes(primary)) {
    animMode = 'happy';
    spawnHappy();
  } else if (['anxiety','anxious','confusion','anger'].includes(primary)) {
    animMode = 'anxious';
    spawnAnxious();
  } else if (['exhaustion','loneliness'].includes(primary)) {
    animMode = 'exhausted';
    spawnExhausted();
  } else if (sentiment === 'Negative') {
    animMode = 'sad';
    spawnSad();
  } else {
    animMode = null;
    canvas.classList.remove('visible');
    return;
  }

  canvas.classList.add('visible');
  animLoop();

  // Auto-fade after 6 seconds
  setTimeout(() => {
    canvas.style.transition = 'opacity 2s ease';
    canvas.style.opacity = '0';
    setTimeout(() => {
      canvas.classList.remove('visible');
      canvas.style.opacity = '';
      canvas.style.transition = '';
      if (animFrame) cancelAnimationFrame(animFrame);
      animFrame = null;
    }, 2000);
  }, 6000);
}


// ════════════════════════════════════════════════════════════
//  INIT
// ════════════════════════════════════════════════════════════
document.addEventListener('DOMContentLoaded', () => {
  setGreeting();
  loadStreak();
  setupNav();
  setupTextarea();
  setupEmojiStrip();
  initVoice();
  checkAuthStatus();
});

function setGreeting() {
  const h = new Date().getHours();
  document.getElementById('greetingText').textContent =
    h < 5 ? 'Up late, are we?' : h < 12 ? 'Good morning' :
    h < 17 ? 'Good afternoon' : h < 21 ? 'Good evening' : 'Good night';
  document.getElementById('headerDate').innerHTML =
    new Date().toLocaleDateString('en-US',{weekday:'long',day:'numeric',month:'long',year:'numeric'}).replace(',','<br>');
}

function setupTextarea() {
  const ta = document.getElementById('journalInput');
  ta.addEventListener('input', () => {
    document.getElementById('charCount').textContent = ta.value.length;
  });
}

function setupEmojiStrip() {
  document.querySelectorAll('.emj').forEach(b => {
    b.addEventListener('click', () => {
      document.querySelectorAll('.emj').forEach(x => x.classList.remove('selected'));
      b.classList.add('selected');
    });
  });
}


// ════════════════════════════════════════════════════════════
//  NAVIGATION
// ════════════════════════════════════════════════════════════
function setupNav() {
  document.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', e => {
      e.preventDefault();
      navigate(link.dataset.section);
      document.getElementById('sidebar').classList.remove('open');
      document.getElementById('sidebarOverlay').classList.remove('visible');
      document.getElementById('hamburger').classList.remove('open');
    });
  });
}

function navigate(section) {
  document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
  document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
  document.getElementById(`section-${section}`).classList.add('active');
  document.querySelector(`[data-section="${section}"]`).classList.add('active');
  if (section === 'dashboard') initDashboard();
  if (section === 'history')   loadHistory();
}

function toggleSidebar() {
  const sb = document.getElementById('sidebar');
  const ov = document.getElementById('sidebarOverlay');
  const hb = document.getElementById('hamburger');
  const open = sb.classList.toggle('open');
  ov.classList.toggle('visible', open);
  hb.classList.toggle('open', open);
}


// ════════════════════════════════════════════════════════════
//  VOICE INPUT
// ════════════════════════════════════════════════════════════
function initVoice() {
  const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!SR) { const b = document.getElementById('micBtn'); if(b) b.style.display='none'; return; }

  recognition = new SR();
  recognition.lang = 'en-US';
  recognition.continuous    = true;
  recognition.interimResults = true;

  recognition.onresult = e => {
    let final = '', interim = '';
    for (let i = 0; i < e.results.length; i++) {
      e.results[i].isFinal ? (final += e.results[i][0].transcript + ' ')
                           : (interim += e.results[i][0].transcript);
    }
    const ta = document.getElementById('journalInput');
    ta.value = (final + interim).trim();
    document.getElementById('charCount').textContent = ta.value.length;
  };

  recognition.onerror = e => {
    document.getElementById('voiceStatusText').textContent =
      e.error === 'not-allowed' ? 'Microphone permission denied.' : 'Could not hear audio. Try again.';
    setTimeout(stopVoice, 2000);
  };

  recognition.onend = () => { if (isListening) { try { recognition.start(); } catch(e){} } };
}

function toggleVoice() {
  isListening ? stopVoice() : startVoice();
}

function startVoice() {
  if (!recognition) { alert('Voice input requires Chrome or Edge browser.'); return; }
  isListening = true;
  recognition.start();
  document.getElementById('micBtn').classList.add('listening');
  document.getElementById('voiceStatus').style.display = 'flex';
  document.getElementById('voiceStatusText').textContent = 'Listening… speak your entry';
}

function stopVoice() {
  isListening = false;
  if (recognition) recognition.stop();
  document.getElementById('micBtn').classList.remove('listening');
  document.getElementById('voiceStatus').style.display = 'none';
}


// ════════════════════════════════════════════════════════════
//  SUBMIT ENTRY
// ════════════════════════════════════════════════════════════
async function submitEntry() {
  if (isListening) stopVoice();
  const text = document.getElementById('journalInput').value.trim();
  if (!text || text.length < 8) { shakeEl(document.getElementById('journalInput')); return; }

  showLoading(true);
  try {
    const res  = await fetch('/api/entry', {
      method:'POST', headers:{'Content-Type':'application/json'},
      body: JSON.stringify({ text })
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || 'Error');

    renderResult(data);
    triggerAnimation(data.sentiment, data.emotions);
    updateStreak();
    allEntries = [];

    // Show registration nudge if backend says so
    if (data.show_nudge && !currentUser) {
      setTimeout(showNudge, 1200);
    }

  } catch (err) { alert('Error: ' + err.message); }
  finally { showLoading(false); }
}

function renderResult(data) {
  setOrb(data.sentiment);
  const card = document.getElementById('resultCard');
  card.style.display = 'block';
  setTimeout(() => card.scrollIntoView({behavior:'smooth', block:'nearest'}), 100);

  const pill = document.getElementById('sentimentPill');
  pill.textContent = data.sentiment;
  pill.className   = `sentiment-pill pill-${data.sentiment}`;

  const pct = ((data.score + 1) / 2) * 100;
  const bar = document.getElementById('scoreBar');
  bar.style.width      = `${pct}%`;
  bar.style.background = scoreColor(data.sentiment);
  document.getElementById('scoreValue').textContent = (data.score > 0 ? '+' : '') + data.score;

  document.getElementById('emotionsWrap').innerHTML =
    data.emotions.map(e => `<span class="etag">${emEmoji(e)}&nbsp;${e}</span>`).join('');

  document.getElementById('responseQuote').textContent = data.response;
  document.getElementById('tipBlock').innerHTML = `<strong>💡 Try this:</strong> ${data.tip}`;
}

// ─── Orb ──────────────────────────────────────────────────
function setOrb(sentiment) {
  const orb   = document.getElementById('moodOrb');
  const emoji = document.getElementById('orbEmoji');
  const label = document.getElementById('orbLabel');
  const map   = { Positive:['✦','Positive'], Neutral:['◉','Balanced'], Negative:['◌','Low'] };
  orb.className = `orb ${sentiment.toLowerCase()}`;
  [emoji.textContent, label.textContent] = map[sentiment] || ['✦','—'];
}


// ════════════════════════════════════════════════════════════
//  REGISTRATION NUDGE
// ════════════════════════════════════════════════════════════
function showNudge() {
  if (currentUser) return;
  document.getElementById('nudgeBanner').style.display = 'block';
}

function dismissNudge() {
  document.getElementById('nudgeBanner').style.display = 'none';
}


// ════════════════════════════════════════════════════════════
//  MODALS
// ════════════════════════════════════════════════════════════
function openModal(type) {
  dismissNudge();
  document.getElementById('modalBackdrop').classList.add('visible');
  document.getElementById('registerModal').classList.remove('visible');
  document.getElementById('loginModal').classList.remove('visible');
  document.getElementById(`${type}Modal`).classList.add('visible');
  // Clear errors
  document.getElementById('regError').textContent   = '';
  document.getElementById('loginError').textContent = '';
}

function closeModal() {
  document.getElementById('modalBackdrop').classList.remove('visible');
  document.getElementById('registerModal').classList.remove('visible');
  document.getElementById('loginModal').classList.remove('visible');
}

// Close on Escape
document.addEventListener('keydown', e => { if (e.key === 'Escape') closeModal(); });


// ════════════════════════════════════════════════════════════
//  AUTH — Register / Login / Logout
// ════════════════════════════════════════════════════════════
async function doRegister() {
  const name     = document.getElementById('regName').value.trim();
  const email    = document.getElementById('regEmail').value.trim();
  const password = document.getElementById('regPassword').value;
  const errEl    = document.getElementById('regError');

  errEl.textContent = '';

  if (!name || !email || !password) {
    errEl.textContent = 'Please fill in all fields.'; return;
  }

  try {
    const res  = await fetch('/api/register', {
      method:'POST', headers:{'Content-Type':'application/json'},
      body: JSON.stringify({ name, email, password })
    });
    const data = await res.json();
    if (!res.ok) { errEl.textContent = data.error; return; }

    setCurrentUser(data.user);
    closeModal();
    showToast(`Welcome, ${data.user.name}! 🎉 Check your email for a welcome message.`);
    allEntries = [];

  } catch (e) { errEl.textContent = 'Something went wrong. Please try again.'; }
}

async function doLogin() {
  const email    = document.getElementById('loginEmail').value.trim();
  const password = document.getElementById('loginPassword').value;
  const errEl    = document.getElementById('loginError');

  errEl.textContent = '';

  try {
    const res  = await fetch('/api/login', {
      method:'POST', headers:{'Content-Type':'application/json'},
      body: JSON.stringify({ email, password })
    });
    const data = await res.json();
    if (!res.ok) { errEl.textContent = data.error; return; }

    setCurrentUser(data.user);
    closeModal();
    showToast(`Welcome back, ${data.user.name}! ✦`);
    allEntries = [];

  } catch (e) { errEl.textContent = 'Something went wrong. Please try again.'; }
}

async function doLogout() {
  await fetch('/api/logout', { method:'POST' });
  currentUser = null;
  document.getElementById('userPill').style.display  = 'none';
  document.getElementById('authBtns').style.display  = 'flex';
  allEntries = [];
  showToast('Signed out. See you soon 👋');
}

async function checkAuthStatus() {
  try {
    const res  = await fetch('/api/me');
    const data = await res.json();
    if (data.user) setCurrentUser(data.user);
  } catch (e) {}
}

function setCurrentUser(user) {
  currentUser = user;
  document.getElementById('userPill').style.display  = 'flex';
  document.getElementById('authBtns').style.display  = 'none';
  document.getElementById('userName').textContent    = user.name;
  document.getElementById('userEmail').textContent   = user.email;
  document.getElementById('userAvatar').textContent  = user.name.charAt(0).toUpperCase();
}

// Toast notification
function showToast(msg) {
  const existing = document.getElementById('toast');
  if (existing) existing.remove();

  const t = document.createElement('div');
  t.id = 'toast';
  t.textContent = msg;
  Object.assign(t.style, {
    position:'fixed', bottom:'80px', left:'50%', transform:'translateX(-50%)',
    background:'#171c21', border:'1px solid rgba(201,169,110,.35)',
    color:'#e9e4dc', borderRadius:'10px', padding:'12px 24px',
    fontSize:'.85rem', zIndex:'900', whiteSpace:'nowrap',
    boxShadow:'0 8px 28px rgba(0,0,0,.4)',
    animation:'slideUp .35s ease',
  });
  document.body.appendChild(t);
  setTimeout(() => { t.style.opacity = '0'; t.style.transition = 'opacity .5s'; setTimeout(() => t.remove(), 500); }, 3500);
}


// ════════════════════════════════════════════════════════════
//  DASHBOARD
// ════════════════════════════════════════════════════════════
async function initDashboard() {
  await Promise.all([
    loadMoodChart(7, document.querySelector('.rtbtn.active')),
    loadEmotionChart(),
    loadSentimentChart(),
    loadStats(),
    checkTrend(),
    generateInsight(),
  ]);
}

async function loadStats() {
  const res     = await fetch('/api/entries');
  const entries = await res.json();
  let pos = 0, neg = 0;
  entries.forEach(e => { if(e.sentiment==='Positive') pos++; else if(e.sentiment==='Negative') neg++; });
  document.getElementById('statTotal').textContent    = entries.length;
  document.getElementById('statPositive').textContent = pos;
  document.getElementById('statNegative').textContent = neg;
  document.getElementById('statStreak').textContent   = localStorage.getItem('mg_streak') || 0;
}

async function loadMoodChart(days, btn) {
  document.querySelectorAll('.rtbtn').forEach(b => b.classList.remove('active'));
  if (btn) btn.classList.add('active');

  const data   = await fetch(`/api/chart?days=${days}`).then(r=>r.json());
  const labels = data.map(d => fmtShort(d.day));
  const scores = data.map(d => parseFloat(d.avg_score.toFixed(2)));
  const colors = scores.map(s => s>=.05 ? 'rgba(130,176,154,.75)' : s<=-.05 ? 'rgba(201,122,98,.75)' : 'rgba(201,169,110,.75)');

  if (chartObjs.mood) chartObjs.mood.destroy();
  chartObjs.mood = new Chart(document.getElementById('moodChart').getContext('2d'), {
    type:'bar',
    data:{ labels, datasets:[{ data:scores, backgroundColor:colors, borderRadius:6, borderWidth:0 }] },
    options:{
      responsive:true,
      plugins:{ tooltip:{ callbacks:{ label:c=>` Score: ${c.parsed.y>0?'+':''}${c.parsed.y}` }}},
      scales:{
        y:{ min:-1, max:1, grid:{color:'rgba(255,255,255,.04)'}, ticks:{ callback:v=>v===0?'0':v>0?`+${v}`:v, stepSize:.5 } },
        x:{ grid:{ display:false } }
      }
    }
  });
}

async function loadEmotionChart() {
  const counts = await fetch('/api/emotions').then(r=>r.json());
  const labels = Object.keys(counts).slice(0,7);
  const values = Object.values(counts).slice(0,7);
  const palette = ['rgba(201,169,110,.8)','rgba(130,176,154,.8)','rgba(201,122,98,.8)','rgba(122,158,201,.8)','rgba(190,150,180,.8)','rgba(160,190,140,.8)','rgba(201,190,110,.8)'];
  if (chartObjs.emotion) chartObjs.emotion.destroy();
  chartObjs.emotion = new Chart(document.getElementById('emotionChart').getContext('2d'), {
    type:'doughnut',
    data:{ labels, datasets:[{ data:values, backgroundColor:palette, borderWidth:0, hoverOffset:8 }] },
    options:{ responsive:true, cutout:'58%', plugins:{ legend:{ display:true, position:'bottom', labels:{padding:13,boxWidth:9,font:{size:10}} }}}
  });
}

async function loadSentimentChart() {
  const entries = await fetch('/api/entries').then(r=>r.json());
  let pos=0,neu=0,neg=0;
  entries.forEach(e=>{ if(e.sentiment==='Positive')pos++; else if(e.sentiment==='Neutral')neu++; else neg++; });
  if (chartObjs.sentiment) chartObjs.sentiment.destroy();
  chartObjs.sentiment = new Chart(document.getElementById('sentimentChart').getContext('2d'), {
    type:'pie',
    data:{ labels:['Positive','Neutral','Negative'], datasets:[{ data:[pos,neu,neg], backgroundColor:['rgba(130,176,154,.8)','rgba(201,169,110,.8)','rgba(201,122,98,.8)'], borderWidth:0, hoverOffset:8 }] },
    options:{ responsive:true, plugins:{ legend:{ display:true, position:'bottom', labels:{padding:13,boxWidth:9,font:{size:10}} }}}
  });
}

async function checkTrend() {
  const entries = await fetch('/api/entries').then(r=>r.json());
  const bad = entries.length >= 3 && entries.slice(0,3).every(e=>e.sentiment==='Negative');
  document.getElementById('alertCard').style.display = bad ? 'flex' : 'none';
}

async function generateInsight() {
  const entries = await fetch('/api/entries').then(r=>r.json());
  if (entries.length < 3) { document.getElementById('insightCard').style.display='none'; return; }

  const counts = {Positive:0,Neutral:0,Negative:0};
  const ef = {};
  entries.forEach(e => {
    counts[e.sentiment]++;
    e.emotions.split(', ').forEach(em => { em=em.trim(); ef[em]=(ef[em]||0)+1; });
  });

  const dom  = Object.keys(counts).sort((a,b)=>counts[b]-counts[a])[0];
  const topE = Object.keys(ef).sort((a,b)=>ef[b]-ef[a])[0];
  const tail = dom==='Positive' ? "You've been carrying real brightness lately. ✨"
             : dom==='Negative' ? "You've been going through a lot. Reaching out for support is always an option."
             : "Your mood has been steady and balanced — quiet strength.";

  document.getElementById('insightCard').style.display = 'flex';
  document.getElementById('insightText').innerHTML =
    `Across your <strong>${entries.length}</strong> journal ${entries.length===1?'entry':'entries'}, your most common mood has been <strong>${dom.toLowerCase()}</strong>. The emotion showing up most is <strong>${topE}</strong>. ${tail}`;
}


// ════════════════════════════════════════════════════════════
//  HISTORY
// ════════════════════════════════════════════════════════════
async function loadHistory() {
  if (!allEntries.length) { const r=await fetch('/api/entries'); allEntries=await r.json(); }
  renderHistory(allEntries);
}

function renderHistory(entries) {
  const list = document.getElementById('historyList');
  if (!entries.length) {
    list.innerHTML = '<div class="empty-state"><div class="empty-icon">📖</div><p>No entries yet. Write your first one!</p></div>';
    return;
  }
  list.innerHTML = entries.map(e => `
    <div class="h-entry">
      <div class="h-top">
        <span class="sentiment-pill pill-${e.sentiment}" style="font-size:.67rem;padding:3px 11px">${e.sentiment}</span>
        <span class="h-date">${fmtDT(e.created_at)}</span>
      </div>
      <p class="h-text">${escH(e.text)}</p>
      <div class="h-tags">${e.emotions.split(', ').map(em=>`<span class="h-tag">${emEmoji(em.trim())} ${em.trim()}</span>`).join('')}</div>
    </div>
  `).join('');
}

function filterHistory() {
  const q = document.getElementById('searchBox').value.toLowerCase();
  renderHistory(allEntries.filter(e => e.text.toLowerCase().includes(q) || e.emotions.toLowerCase().includes(q) || e.sentiment.toLowerCase().includes(q)));
}

async function exportCSV() {
  if (!allEntries.length) { const r=await fetch('/api/entries'); allEntries=await r.json(); }
  if (!allEntries.length) { alert('No entries to export yet.'); return; }
  const csv = [['Date','Sentiment','Score','Emotions','Text'],
    ...allEntries.map(e=>[ e.created_at, e.sentiment, e.score, `"${e.emotions}"`, `"${e.text.replace(/"/g,'""')}"` ])
  ].map(r=>r.join(',')).join('\n');
  const a = Object.assign(document.createElement('a'), {
    href:     URL.createObjectURL(new Blob([csv],{type:'text/csv'})),
    download: `mindguard-${new Date().toISOString().slice(0,10)}.csv`
  });
  a.click();
}


// ════════════════════════════════════════════════════════════
//  STREAK
// ════════════════════════════════════════════════════════════
function updateStreak() {
  const today = new Date().toISOString().slice(0,10);
  const last  = localStorage.getItem('mg_last') || '';
  const yest  = new Date(Date.now()-86400000).toISOString().slice(0,10);
  let s = parseInt(localStorage.getItem('mg_streak')||'0');
  if (last===today) {} else if (last===yest) s++; else s=1;
  localStorage.setItem('mg_last',today); localStorage.setItem('mg_streak',s);
  document.getElementById('streakCount').textContent = s;
}

function loadStreak() {
  document.getElementById('streakCount').textContent = localStorage.getItem('mg_streak')||'0';
}


// ════════════════════════════════════════════════════════════
//  HELPERS
// ════════════════════════════════════════════════════════════
function scoreColor(s) {
  return s==='Positive'?'#82b09a':s==='Negative'?'#c97a62':'#c9a96e';
}
function emEmoji(e) {
  return {Joy:'😊',Sadness:'😢',Anger:'😠',Anxiety:'😰',Exhaustion:'😴',Confusion:'😕',Hope:'🌱',Gratitude:'🙏',Loneliness:'🫂',Pride:'🌟',Neutral:'😐',Calm:'🌊',Unease:'😶'}[e]||'💭';
}
function fmtShort(d) { return new Date(d).toLocaleDateString('en-US',{month:'short',day:'numeric'}); }
function fmtDT(d)    { return new Date(d).toLocaleDateString('en-US',{month:'short',day:'numeric',year:'numeric',hour:'2-digit',minute:'2-digit'}); }
function escH(s)     { return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;'); }
function shakeEl(el) { el.style.animation=''; void el.offsetWidth; el.style.animation='shake .35s ease'; setTimeout(()=>el.style.animation='',400); }
function showLoading(v) { document.getElementById('loadingOverlay').style.display=v?'flex':'none'; }

// Inject shake animation
const ss = document.createElement('style');
ss.textContent = `@keyframes shake{0%,100%{transform:translateX(0)}20%,60%{transform:translateX(-7px)}40%,80%{transform:translateX(7px)}}`;
document.head.appendChild(ss);
