============================================================
===== templates/base.html =====
============================================================

<!DOCTYPE html>
<html lang="pt-br">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>DrinkMetrics — Global Alcohol Intelligence</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@500;600;700&family=Inter:wght@300;400;500;600&family=JetBrains+Mono:wght@300;400&display=swap" rel="stylesheet">
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
<script src="https://cdn.plot.ly/plotly-2.35.2.min.js"></script>
<style>
:root {
  --navy:       #080C18;
  --navy2:      #0B1020;
  --navy3:      #0E1528;
  --navy4:      #131C34;
  --cream:      #F0E8D5;
  --cream2:     #E8DEC8;
  --gold:       #C9A84C;
  --gold-light: #E8D080;
  --gold-dim:   #A07828;
  --gold-faint: rgba(201,168,76,.08);
  --text:       #E4D4A2;
  --text2:      #C0A868;
  --text3:      #8A7040;
  --border:     rgba(201,168,76,.1);
  --border2:    rgba(201,168,76,.2);
  --radius:     4px;
  --trans:      .28s cubic-bezier(.4,0,.2,1);
}

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html { scroll-behavior: smooth; }

body {
  background: var(--navy);
  color: var(--text);
  font-family: 'Inter', sans-serif;
  min-height: 100vh;
  overflow-x: hidden;
  -webkit-font-smoothing: antialiased;
  cursor: none;
}
a, button, [onclick], th { cursor: none; }

/* ── CURSOR ── */
#cur-dot {
  position: fixed; width: 7px; height: 7px; border-radius: 50%;
  background: var(--gold); pointer-events: none; z-index: 9999;
  transform: translate(-50%,-50%);
  box-shadow: 0 0 12px rgba(201,168,76,.9);
  transition: width .18s, height .18s, opacity .2s;
}
#cur-ring {
  position: fixed; width: 32px; height: 32px; border-radius: 50%;
  border: 1px solid rgba(201,168,76,.45); pointer-events: none; z-index: 9998;
  transform: translate(-50%,-50%);
  transition: width .3s, height .3s, border-color .3s;
}
body.ch #cur-dot  { width: 11px; height: 11px; box-shadow: 0 0 20px rgba(201,168,76,1); }
body.ch #cur-ring { width: 46px; height: 46px; border-color: rgba(201,168,76,.7); }
body.cc #cur-dot  { background: #fff; width: 5px; height: 5px; }

/* ── BACKGROUND ── */
.bg-layer {
  position: fixed; inset: 0; z-index: 0; pointer-events: none;
  background:
    radial-gradient(ellipse 80% 55% at 12% 8%, rgba(201,168,76,.055) 0%, transparent 55%),
    radial-gradient(ellipse 55% 45% at 88% 92%, rgba(20,45,130,.14) 0%, transparent 55%),
    linear-gradient(155deg, #080C18 0%, #0B1020 100%);
}
.bg-noise {
  position: fixed; inset: 0; z-index: 1; pointer-events: none; opacity: .016;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
  background-size: 200px;
}
.bg-rain {
  position: fixed; inset: 0; z-index: 2; pointer-events: none; opacity: .09;
}
.bg-rain span {
  position: absolute; top: -120px;
  color: #B89030; font-family: 'JetBrains Mono', monospace;
  font-size: 10px; white-space: nowrap;
  animation: rain-fall linear infinite;
}
@keyframes rain-fall {
  0%   { transform: translateY(-120px); opacity: 0; }
  8%   { opacity: 1; }
  92%  { opacity: .6; }
  100% { transform: translateY(110vh); opacity: 0; }
}

/* ── TOP ACCENT BAR ── */
.top-bar {
  position: fixed; top: 0; left: 0; right: 0; height: 2px; z-index: 300;
  background: linear-gradient(90deg, transparent 0%, var(--gold-dim) 25%, var(--gold) 50%, var(--gold-dim) 75%, transparent 100%);
  pointer-events: none;
}

/* ── NAV ── */
nav {
  position: fixed; top: 2px; left: 0; right: 0; z-index: 200;
  height: 62px;
  display: flex; align-items: center; justify-content: space-between;
  padding: 0 48px;
  background: rgba(8,12,24,.88);
  backdrop-filter: blur(20px) saturate(1.5);
  border-bottom: 1px solid var(--border);
}
.nav-brand {
  display: flex; align-items: center; gap: 10px;
  text-decoration: none;
  font-family: 'Playfair Display', serif;
  font-size: 1.05rem; font-weight: 600;
  color: var(--gold); letter-spacing: 2px;
}
.nav-brand-icon {
  width: 28px; height: 28px; flex-shrink: 0;
}
.nav-links { display: flex; gap: 6px; align-items: center; }
.nav-link {
  display: flex; align-items: center; gap: 6px;
  text-decoration: none; color: var(--text3);
  font-size: .68rem; letter-spacing: 2px; text-transform: uppercase;
  font-weight: 500; padding: 7px 14px; border-radius: var(--radius);
  transition: color var(--trans), background var(--trans);
  position: relative;
}
.nav-link:hover  { color: var(--gold); background: var(--gold-faint); }
.nav-link.active { color: var(--gold-light); background: rgba(201,168,76,.1); }
.nav-link svg { width: 12px; height: 12px; stroke: currentColor; fill: none; stroke-width: 1.5; flex-shrink: 0; }
.nav-right { display: flex; align-items: center; gap: 12px; }
.nav-pill {
  font-size: .62rem; letter-spacing: 2px; text-transform: uppercase;
  color: var(--text3); background: rgba(201,168,76,.06);
  border: 1px solid var(--border); padding: 4px 12px; border-radius: 20px;
}

/* ── PAGE SHELL ── */
.page {
  position: relative; z-index: 10;
  max-width: 1200px; margin: 0 auto;
  padding: 88px 32px 80px;
}

/* ── PAGE HEADER ── */
.page-eyebrow {
  font-size: .58rem; letter-spacing: 4px; text-transform: uppercase;
  color: var(--gold); font-weight: 500; margin-bottom: 8px;
  display: flex; align-items: center; gap: 12px;
}
.page-eyebrow::before, .page-eyebrow::after {
  content: ''; display: block; width: 32px; height: 1px;
  background: linear-gradient(to right, transparent, rgba(201,168,76,.4), transparent);
}
.page-title {
  font-family: 'Playfair Display', serif;
  font-size: clamp(1.6rem, 4vw, 2.4rem); font-weight: 600;
  color: var(--text); margin-bottom: 4px; line-height: 1.2;
}
.page-title .accent {
  background: linear-gradient(135deg, var(--gold) 0%, var(--gold-light) 60%, var(--gold-dim) 100%);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
}
.page-sub { font-size: .8rem; color: var(--text3); letter-spacing: .3px; }
.page-header { margin-bottom: 40px; }

/* ── DIVIDER ── */
.rule {
  border: none; border-top: 1px solid var(--border);
  margin: 0;
}

/* ── KPI CARDS ── */
.kpi-grid { display: grid; grid-template-columns: repeat(4,1fr); gap: 16px; margin-bottom: 32px; }
@media(max-width:900px){ .kpi-grid{ grid-template-columns: repeat(2,1fr); } }
@media(max-width:540px){ .kpi-grid{ grid-template-columns: 1fr 1fr; } }

.kpi {
  background: var(--navy3);
  border: 1px solid var(--border);
  border-radius: 8px; padding: 24px 22px;
  position: relative; overflow: hidden;
  transition: border-color var(--trans), transform var(--trans), box-shadow var(--trans);
}
.kpi::before {
  content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px;
  background: linear-gradient(90deg, transparent, var(--gold), transparent);
  opacity: 0; transition: opacity var(--trans);
}
.kpi:hover { border-color: var(--border2); transform: translateY(-3px); box-shadow: 0 12px 40px rgba(0,0,0,.35); }
.kpi:hover::before { opacity: 1; }
.kpi-icon { margin-bottom: 16px; }
.kpi-icon svg { width: 22px; height: 22px; stroke: var(--gold); fill: none; stroke-width: 1.4; opacity: .75; }
.kpi-label { font-size: .6rem; letter-spacing: 2.5px; text-transform: uppercase; color: var(--text3); margin-bottom: 8px; }
.kpi-value { font-size: 1.9rem; font-weight: 700; color: var(--gold-light); line-height: 1; font-family: 'Playfair Display', serif; }
.kpi-sub { font-size: .7rem; color: var(--text3); margin-top: 8px; font-family: 'JetBrains Mono', monospace; }

/* ── CARDS ── */
.card {
  background: var(--navy3);
  border: 1px solid var(--border);
  border-radius: 8px;
  transition: border-color var(--trans), box-shadow var(--trans);
  overflow: hidden;
}
.card:hover { border-color: rgba(201,168,76,.22); box-shadow: 0 6px 32px rgba(0,0,0,.3); }
.card-inner { padding: 24px; }

/* ── SECTION LABEL ── */
.sec-label {
  font-size: .6rem; letter-spacing: 3px; text-transform: uppercase;
  color: var(--text3); margin-bottom: 18px;
  display: flex; align-items: center; gap: 10px;
}
.sec-label svg { width: 12px; height: 12px; stroke: var(--gold-dim); fill: none; stroke-width: 1.5; flex-shrink: 0; }
.sec-label::after { content: ''; flex: 1; height: 1px; background: var(--border); }

/* ── CHART PANEL ── */
.chart-panel { padding: 20px 20px 8px; }

/* ── LIVE TICKER ── */
.live-ticker {
  display: flex; align-items: center; gap: 10px;
  background: var(--navy4); border: 1px solid var(--border);
  border-radius: 6px; padding: 10px 16px;
  font-size: .72rem; color: var(--text3);
  font-family: 'JetBrains Mono', monospace;
}
.live-dot {
  width: 6px; height: 6px; border-radius: 50%;
  background: var(--gold); flex-shrink: 0;
  box-shadow: 0 0 6px rgba(201,168,76,.8);
  animation: pulse 2.2s ease-in-out infinite;
}
@keyframes pulse { 0%,100%{opacity:1;transform:scale(1);} 50%{opacity:.35;transform:scale(.75);} }

/* ── BADGES ── */
.badge-alto {
  background: rgba(201,168,76,.12); color: var(--gold-light);
  padding: 3px 10px; border-radius: 20px; font-size: .68rem;
  border: 1px solid rgba(201,168,76,.25); font-weight: 500;
}
.badge-baixo {
  background: rgba(20,30,60,.5); color: var(--text3);
  padding: 3px 10px; border-radius: 20px; font-size: .68rem;
  border: 1px solid rgba(201,168,76,.08);
}

/* ── DATA TABLE ── */
.data-table { width: 100%; border-collapse: collapse; font-size: .82rem; }
.data-table th {
  padding: 11px 14px; color: var(--text3);
  font-size: .62rem; letter-spacing: 2px; text-transform: uppercase;
  border-bottom: 1px solid var(--border); cursor: pointer;
  user-select: none; white-space: nowrap; font-weight: 500;
  transition: color var(--trans); background: var(--navy4);
}
.data-table th:hover { color: var(--gold-light); }
.data-table td { padding: 10px 14px; border-bottom: 1px solid rgba(201,168,76,.05); vertical-align: middle; }
.data-table tbody tr { transition: background var(--trans); }
.data-table tbody tr:hover { background: var(--gold-faint); }
.data-table tbody tr:last-child td { border-bottom: none; }

/* ── SEARCH ── */
.search-wrap { position: relative; }
.search-icon { position: absolute; left: 14px; top: 50%; transform: translateY(-50%); }
.search-icon svg { width: 14px; height: 14px; stroke: var(--text3); fill: none; stroke-width: 1.5; }
.search-input {
  width: 100%; padding: 10px 16px 10px 42px;
  background: var(--navy4); border: 1px solid var(--border);
  border-radius: 6px; color: var(--text);
  font-size: .85rem; outline: none;
  transition: border-color var(--trans), box-shadow var(--trans);
  font-family: 'Inter', sans-serif;
}
.search-input:focus { border-color: var(--border2); box-shadow: 0 0 0 3px rgba(201,168,76,.06); }
.search-input::placeholder { color: var(--text3); }

/* ── MINI BAR ── */
.mini-bar { display: flex; align-items: center; gap: 8px; justify-content: flex-end; }
.mini-bar-track { width: 52px; height: 3px; background: rgba(201,168,76,.08); border-radius: 2px; overflow: hidden; flex-shrink: 0; }
.mini-bar-fill { height: 100%; border-radius: 2px; }

/* ── INSIGHT ITEM ── */
.insight-item {
  display: flex; gap: 16px; align-items: flex-start;
  padding: 16px 0; border-bottom: 1px solid var(--border);
}
.insight-item:last-child { border-bottom: none; }
.insight-num {
  width: 28px; height: 28px; border-radius: 50%; flex-shrink: 0;
  background: rgba(201,168,76,.1); border: 1px solid rgba(201,168,76,.2);
  display: flex; align-items: center; justify-content: center;
  font-size: .7rem; font-weight: 700; color: var(--gold-light);
  font-family: 'JetBrains Mono', monospace;
}
@keyframes fade-up { from{opacity:0;transform:translateY(10px);} to{opacity:1;transform:translateY(0);} }

/* ── COUNTRY TAG ── */
.ctag {
  display: inline-flex; align-items: center; gap: 6px;
  background: rgba(201,168,76,.1); border: 1px solid rgba(201,168,76,.22);
  color: var(--gold-light); border-radius: 20px;
  padding: 5px 12px; font-size: .78rem; cursor: pointer;
  transition: background var(--trans), transform var(--trans); margin: 3px;
}
.ctag:hover { background: rgba(201,168,76,.2); transform: translateY(-1px); }

/* ── PROGRESS TRACK ── */
.prog-track { background: rgba(201,168,76,.07); border-radius: 3px; overflow: hidden; }
.prog-fill {
  height: 4px; border-radius: 3px;
  background: linear-gradient(90deg, var(--gold-dim), var(--gold-light));
  transition: width .7s ease;
}

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: var(--navy); }
::-webkit-scrollbar-thumb { background: rgba(201,168,76,.2); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: rgba(201,168,76,.35); }

/* ── RESPONSIVE ── */
@media(max-width:768px){
  nav { padding: 0 20px; }
  .page { padding: 80px 16px 72px; }
  .nav-links .nav-link span { display: none; }
}
</style>
</head>
<body>
<div class="bg-layer"></div>
<div class="bg-noise"></div>
<div class="bg-rain" id="bg-rain"></div>
<div class="top-bar"></div>
<div id="cur-dot"></div>
<div id="cur-ring"></div>

<nav>
  <a class="nav-brand" href="/">
    <svg class="nav-brand-icon" viewBox="0 0 28 32" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path d="M3 4.5L25 4.5L22 22L6 22Z" stroke="#C9A84C" stroke-width="1.4" stroke-linejoin="round"/>
      <line x1="3" y1="4.5" x2="25" y2="4.5" stroke="#E0B85A" stroke-width="1.8" stroke-linecap="round"/>
      <line x1="6" y1="22" x2="22" y2="22" stroke="#C9A84C" stroke-width="1.8" stroke-linecap="round"/>
      <line x1="5" y1="25" x2="23" y2="25" stroke="#A07828" stroke-width="1.2" stroke-linecap="round"/>
      <rect x="10" y="11" width="8" height="7" rx="1.5" stroke="#C9A84C" stroke-width="1.1" opacity=".7"/>
      <line x1="7" y1="17" x2="21" y2="17" stroke="#A07828" stroke-width="1" stroke-dasharray="2 1.5" opacity=".55"/>
      <path d="M20 3.5 Q23.5 1 22.5 4.5" stroke="#C9A84C" stroke-width="1.3" stroke-linecap="round"/>
    </svg>
    DrinkMetrics
  </a>

  <div class="nav-links">
    <a href="/" class="nav-link {% if request.endpoint == 'dashboard' %}active{% endif %}">
      <svg viewBox="0 0 14 14"><rect x="1" y="8" width="3" height="5" rx=".8"/><rect x="5.5" y="5" width="3" height="8" rx=".8"/><rect x="10" y="2" width="3" height="11" rx=".8"/></svg>
      <span>Dashboard</span>
    </a>
    <a href="/insights" class="nav-link {% if request.endpoint == 'insights_page' %}active{% endif %}">
      <svg viewBox="0 0 14 14"><circle cx="7" cy="7" r="5.5" stroke-width="1.3"/><path d="M7 4.5v3l2 1.2" stroke-width="1.3" stroke-linecap="round"/></svg>
      <span>Insights</span>
    </a>
    <a href="/paises" class="nav-link {% if request.endpoint == 'paises_page' %}active{% endif %}">
      <svg viewBox="0 0 14 14"><rect x="1" y="2.5" width="12" height="1.5" rx=".75"/><rect x="1" y="6.5" width="12" height="1.5" rx=".75"/><rect x="1" y="10.5" width="8" height="1.5" rx=".75"/></svg>
      <span>Países</span>
    </a>
    <a href="/comparar" class="nav-link {% if request.endpoint == 'comparar_page' %}active{% endif %}">
      <svg viewBox="0 0 14 14"><polygon points="7,1 13,12 1,12" stroke-width="1.3" fill="none" stroke-linejoin="round"/></svg>
      <span>Comparar</span>
    </a>
  </div>

  <div class="nav-right">
    <span class="nav-pill">193 países</span>
  </div>
</nav>

<div class="page">
{% block content %}{% endblock %}
</div>

<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
<script>
/* ── CURSOR ── */
const dot = document.getElementById('cur-dot');
const ring = document.getElementById('cur-ring');
let mx = 0, my = 0, rx = 0, ry = 0;
document.addEventListener('mousemove', e => {
  mx = e.clientX; my = e.clientY;
  dot.style.left = mx + 'px'; dot.style.top = my + 'px';
});
(function loop(){ rx += (mx-rx)*.11; ry += (my-ry)*.11;
  ring.style.left = rx+'px'; ring.style.top = ry+'px'; requestAnimationFrame(loop); })();
const HS = 'a,button,[onclick],th,.kpi,.ctag,.nav-link,.search-input,select';
document.querySelectorAll(HS).forEach(el => {
  el.addEventListener('mouseenter', () => document.body.classList.add('ch'));
  el.addEventListener('mouseleave', () => document.body.classList.remove('ch'));
});
document.addEventListener('mousedown', () => document.body.classList.add('cc'));
document.addEventListener('mouseup',   () => document.body.classList.remove('cc'));

/* ── CODE RAIN ── */
(function(){
  const c = document.getElementById('bg-rain');
  const words = ['import pandas','df.groupby','SELECT *','def analyze','KMeans(3)','df.corr()','plt.show()','df.describe()','df.nlargest','pd.read_csv','np.where','df.merge','ORDER BY','GROUP BY','df.dropna','model.fit','StandardScaler','df.to_csv','df.head()','sns.heatmap'];
  for(let i=0;i<22;i++){
    const s=document.createElement('span');
    const dur=9+Math.random()*16;
    s.textContent=words[i%words.length];
    s.style.cssText=`left:${Math.random()*100}vw;animation-duration:${dur}s;animation-delay:-${Math.random()*dur}s;opacity:${.35+Math.random()*.55}`;
    c.appendChild(s);
  }
})();

/* ── HOVER TICK SOUND ── */
(function(){
  let ctx;
  function getCtx(){ if(!ctx) ctx=new(window.AudioContext||window.webkitAudioContext)(); return ctx; }
  function tick(){
    try{
      const ac=getCtx(); if(ac.state==='suspended') ac.resume();
      const now=ac.currentTime;
      const len=Math.floor(ac.sampleRate*.008);
      const buf=ac.createBuffer(1,len,ac.sampleRate);
      const d=buf.getChannelData(0);
      for(let i=0;i<len;i++) d[i]=(Math.random()*2-1)*Math.exp(-i/len*12);
      const src=ac.createBufferSource(); src.buffer=buf;
      const bp=ac.createBiquadFilter(); bp.type='bandpass'; bp.frequency.value=2200; bp.Q.value=3;
      const g=ac.createGain(); g.gain.setValueAtTime(.12,now); g.gain.exponentialRampToValueAtTime(.0001,now+.01);
      src.connect(bp); bp.connect(g); g.connect(ac.destination);
      src.start(now); src.stop(now+.012);
    }catch(e){}
  }
  document.addEventListener('mouseenter',e=>{ if(e.target.closest&&e.target.closest(HS)) tick(); },{capture:true,passive:true});
  document.addEventListener('click',()=>{ if(ctx&&ctx.state==='suspended') ctx.resume(); },{once:true,passive:true});
})();
</script>
</body>
</html>




============================================================
===== templates/dashboard.html =====
============================================================

{% extends 'base.html' %}
{% block content %}

<!-- Page Header -->
<div class="d-flex align-items-start justify-content-between mb-5 flex-wrap gap-3">
  <div>
    <div class="page-eyebrow">// visão global</div>
    <h1 class="page-title"><span class="accent">Consumo</span> de Bebidas</h1>
    <p class="page-sub">Inteligência global sobre consumo de bebidas alcoólicas por país</p>
  </div>
  <div class="live-ticker mt-2">
    <span class="live-dot"></span>
    <span id="live-text" style="color:var(--text2)">Carregando...</span>
  </div>
</div>

<!-- KPI Grid -->
<div class="kpi-grid">
  <div class="kpi">
    <div class="kpi-icon"><svg viewBox="0 0 22 22" stroke="currentColor" fill="none" stroke-width="1.4"><circle cx="11" cy="11" r="9"/><path d="M11 6v5.5l3.5 2" stroke-linecap="round"/></svg></div>
    <div class="kpi-label">Países analisados</div>
    <div class="kpi-value" id="kv-total">{{ total }}</div>
    <div class="kpi-sub">dataset global completo</div>
  </div>
  <div class="kpi">
    <div class="kpi-icon"><svg viewBox="0 0 22 22" stroke="currentColor" fill="none" stroke-width="1.5"><path d="M3 19 Q7 4 11 11 Q15 18 19 19" stroke-linecap="round"/><line x1="3" y1="19" x2="19" y2="19" stroke-width="1.1" opacity=".35"/></svg></div>
    <div class="kpi-label">Média álcool puro</div>
    <div class="kpi-value" id="kv-media">{{ media }}L</div>
    <div class="kpi-sub">litros per capita / ano</div>
  </div>
  <div class="kpi">
    <div class="kpi-icon"><svg viewBox="0 0 22 22" stroke="currentColor" fill="none" stroke-width="1.4"><polygon points="11,2 20,18 2,18" stroke-linejoin="round"/><line x1="11" y1="9" x2="11" y2="14" stroke-linecap="round"/><circle cx="11" cy="16.5" r=".9" fill="currentColor" stroke="none"/></svg></div>
    <div class="kpi-label">Maior consumidor</div>
    <div class="kpi-value" id="kv-top" style="font-size:1.25rem;line-height:1.3">{{ max_country }}</div>
    <div class="kpi-sub">total de servings combinados</div>
  </div>
  <div class="kpi">
    <div class="kpi-icon"><svg viewBox="0 0 22 22" fill="currentColor" stroke="none"><rect x="3" y="11" width="4" height="9" rx="1.2" opacity=".4"/><rect x="9" y="7" width="4" height="13" rx="1.2" opacity=".65"/><rect x="15" y="3" width="4" height="17" rx="1.2"/></svg></div>
    <div class="kpi-label">Máx. servings totais</div>
    <div class="kpi-value" id="kv-max">{{ max_value }}</div>
    <div class="kpi-sub">cerveja + dest. + vinho</div>
  </div>
</div>

<!-- World Map -->
<div class="card mb-3">
  <div class="chart-panel">
    <div class="sec-label">
      <svg viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="1.2"><circle cx="6" cy="6" r="5"/><ellipse cx="6" cy="6" rx="2.5" ry="5"/><line x1="1" y1="6" x2="11" y2="6"/></svg>
      Mapa-múndi — Álcool puro per capita (L/ano)
    </div>
    <div id="chart-map" style="height:400px"></div>
  </div>
</div>

<!-- Charts Row 1 -->
<div class="row g-3 mb-3">
  <div class="col-md-6">
    <div class="card h-100">
      <div class="chart-panel">
        <div class="sec-label">
          <svg viewBox="0 0 12 12" fill="currentColor" stroke="none"><rect x="1" y="4" width="2.5" height="7" rx=".5" opacity=".45"/><rect x="4.75" y="2" width="2.5" height="9" rx=".5" opacity=".7"/><rect x="8.5" y="0" width="2.5" height="11" rx=".5"/></svg>
          Top 10 — Cerveja (servings)
        </div>
        <div id="chart-beer" style="height:320px"></div>
      </div>
    </div>
  </div>
  <div class="col-md-6">
    <div class="card h-100">
      <div class="chart-panel">
        <div class="sec-label">
          <svg viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="1.2"><path d="M6 1C6 1 2.5 4.5 2.5 7a3.5 3.5 0 007 0C9.5 4.5 6 1 6 1z" stroke-linecap="round"/></svg>
          Top 10 — Álcool Puro (litros)
        </div>
        <div id="chart-alcool" style="height:320px"></div>
      </div>
    </div>
  </div>
</div>

<!-- Charts Row 2 -->
<div class="row g-3 mb-3">
  <div class="col-md-8">
    <div class="card h-100">
      <div class="chart-panel">
        <div class="sec-label">
          <svg viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="1.2"><circle cx="2.8" cy="9" r="1.3"/><circle cx="6.5" cy="5.5" r="1.3"/><circle cx="9.8" cy="2.5" r="1.3"/></svg>
          Dispersão — Servings Totais vs Álcool Puro
        </div>
        <div id="chart-scatter" style="height:310px"></div>
      </div>
    </div>
  </div>
  <div class="col-md-4">
    <div class="card h-100">
      <div class="chart-panel">
        <div class="sec-label">
          <svg viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="1.2"><circle cx="6" cy="6" r="5"/><path d="M6 6L6 1"/><path d="M6 6L10 9" opacity=".6"/></svg>
          Distribuição por Nível
        </div>
        <div id="chart-donut" style="height:190px"></div>
        <div id="nivel-stats" style="margin-top:12px;padding-top:12px;border-top:1px solid var(--border)"></div>
      </div>
    </div>
  </div>
</div>

<!-- Row 3 — Cerveja/Dest/Vinho médias -->
<div class="card">
  <div class="chart-panel">
    <div class="sec-label">
      <svg viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="1.2"><polyline points="1,10 4,5 7,8 10,3 11,3" stroke-linecap="round" stroke-linejoin="round"/></svg>
      Consumo médio global por categoria
    </div>
    <div id="chart-cats" style="height:220px"></div>
  </div>
</div>

<script>
const BL={
  paper_bgcolor:'transparent',plot_bgcolor:'transparent',
  font:{color:'#8A7040',size:11,family:'Inter,sans-serif'},
};
const AX={
  xaxis:{gridcolor:'rgba(201,168,76,.07)',zerolinecolor:'rgba(201,168,76,.12)',tickfont:{color:'#8A7040',size:10}},
  yaxis:{gridcolor:'rgba(201,168,76,.07)',zerolinecolor:'rgba(201,168,76,.12)',tickfont:{color:'#8A7040',size:10}},
};
const CFG={responsive:true,displayModeBar:false};
const GS_GOLD=[[0,'#0d0a04'],[.28,'#3a2808'],[.6,'#9a7020'],[1,'#e8d080']];
const GS_PUR=[[0,'#0e0c18'],[.35,'#2c2458'],[.7,'#6050a0'],[1,'#b0a0e0']];

async function loadAll(){
  const [t10,t10a,paises]=await Promise.all([
    fetch('/api/top10').then(r=>r.json()),
    fetch('/api/top10-alcool').then(r=>r.json()),
    fetch('/api/paises').then(r=>r.json()),
  ]);

  /* ── WORLD MAP ── */
  Plotly.newPlot('chart-map',[{
    type:'choropleth',locationmode:'country names',
    locations:paises.map(d=>d.Pais),
    z:paises.map(d=>d.LitrosAlcool),
    text:paises.map(d=>`<b>${d.Pais}</b><br>Álcool: ${d.LitrosAlcool}L<br>Total: ${d.TotalBebidas} servings`),
    hovertemplate:'%{text}<extra></extra>',
    colorscale:[[0,'#080C18'],[.15,'#1a1408'],[.35,'#4a3010'],[.6,'#9a7020'],[.85,'#c9a84c'],[1,'#f0d060']],
    zmin:0,zmax:15,
    colorbar:{
      thickness:10,len:.8,x:1.01,
      title:{text:'Litros',font:{size:9,color:'#8A7040'},side:'right'},
      tickfont:{color:'#8A7040',size:9},
      tickcolor:'rgba(201,168,76,.2)',outlinecolor:'transparent',
      bgcolor:'rgba(8,12,24,.4)',
    },
    marker:{line:{color:'rgba(201,168,76,.12)',width:.5}},
  }],{
    ...BL,
    geo:{
      showframe:false,showcoastlines:true,
      coastlinecolor:'rgba(201,168,76,.18)',coastlinewidth:.7,
      showland:true,landcolor:'#0E1528',
      showocean:true,oceancolor:'#080C18',
      showlakes:false,
      showcountries:true,countrycolor:'rgba(201,168,76,.1)',countrywidth:.4,
      showgraticules:true,graticulecolor:'rgba(201,168,76,.04)',
      bgcolor:'transparent',
      projection:{type:'natural earth'},
    },
    margin:{t:0,b:0,l:0,r:60},
  },CFG);

  /* ── BEER TOP10 ── */
  const beerVals=t10.map(d=>d.Cerveja).reverse();
  const beerLabs=t10.map(d=>d.Pais).reverse();
  Plotly.newPlot('chart-beer',[{
    type:'bar',orientation:'h',
    x:beerVals,y:beerLabs,
    text:beerVals.map(v=>v),textposition:'outside',
    textfont:{color:'#C0A868',size:10},
    marker:{
      color:beerVals,colorscale:GS_GOLD,
      line:{color:'rgba(201,168,76,.15)',width:.8},
    },
    hovertemplate:'<b>%{y}</b><br>%{x} servings<extra></extra>',
  }],{
    ...BL,...AX,
    margin:{t:8,b:16,l:0,r:52},
    yaxis:{...AX.yaxis,automargin:true},
    xaxis:{...AX.xaxis,showgrid:true},
  },CFG);

  /* ── ALCOOL TOP10 ── */
  const alcVals=t10a.map(d=>d.LitrosAlcool).reverse();
  const alcLabs=t10a.map(d=>d.Pais).reverse();
  Plotly.newPlot('chart-alcool',[{
    type:'bar',orientation:'h',
    x:alcVals,y:alcLabs,
    text:alcVals.map(v=>v+'L'),textposition:'outside',
    textfont:{color:'#9090C0',size:10},
    marker:{
      color:alcVals,colorscale:GS_PUR,
      line:{color:'rgba(130,110,200,.15)',width:.8},
    },
    hovertemplate:'<b>%{y}</b><br>%{x}L álcool puro<extra></extra>',
  }],{
    ...BL,...AX,
    margin:{t:8,b:16,l:0,r:48},
    yaxis:{...AX.yaxis,automargin:true},
  },CFG);

  /* ── SCATTER ── */
  const highlight=paises.filter(d=>d.LitrosAlcool>10||d.TotalBebidas>500);
  Plotly.newPlot('chart-scatter',[
    {
      type:'scatter',mode:'markers',
      x:paises.map(d=>d.TotalBebidas),y:paises.map(d=>d.LitrosAlcool),
      text:paises.map(d=>d.Pais),
      hovertemplate:'<b>%{text}</b><br>Total servings: %{x}<br>Álcool: %{y}L<extra></extra>',
      marker:{color:paises.map(d=>d.LitrosAlcool),colorscale:GS_GOLD,size:6.5,opacity:.82,line:{color:'rgba(201,168,76,.2)',width:.5}},
      name:'Países',
    },{
      type:'scatter',mode:'markers+text',
      x:highlight.map(d=>d.TotalBebidas),y:highlight.map(d=>d.LitrosAlcool),
      text:highlight.map(d=>d.Pais),textposition:'top center',
      textfont:{color:'#C0A868',size:9},
      hovertemplate:'<b>%{text}</b><br>%{x} servings · %{y}L<extra></extra>',
      marker:{color:'rgba(201,168,76,.0)',size:0},
      showlegend:false,
    },
  ],{
    ...BL,...AX,
    margin:{t:8,b:44,l:52,r:8},
    xaxis:{...AX.xaxis,title:{text:'Total Servings',font:{size:10,color:'#6A5A30'}}},
    yaxis:{...AX.yaxis,title:{text:'Litros Álcool Puro',font:{size:10,color:'#6A5A30'}}},
    showlegend:false,
  },CFG);

  /* ── DONUT ── */
  const alto=paises.filter(d=>d.Nivel==='Alto').length;
  const baixo=paises.length-alto;
  Plotly.newPlot('chart-donut',[{
    type:'pie',labels:['Alto','Baixo'],values:[alto,baixo],hole:.6,
    marker:{colors:['#C9A84C','#1C2840'],line:{color:'#080C18',width:2}},
    textinfo:'none',
    hovertemplate:'<b>%{label}</b><br>%{value} países · %{percent}<extra></extra>',
    pull:[.04,0],
  }],{
    ...BL,
    margin:{t:0,b:0,l:0,r:0},showlegend:false,
    annotations:[
      {text:`<b style="font-size:20px">${alto}</b>`,x:.5,y:.6,xref:'paper',yref:'paper',showarrow:false,font:{size:20,color:'#E8D080',family:'Playfair Display,serif'}},
      {text:'alto',x:.5,y:.38,xref:'paper',yref:'paper',showarrow:false,font:{size:10,color:'#8A7040',family:'Inter'}},
    ]
  },CFG);

  document.getElementById('nivel-stats').innerHTML=`
    <div class="d-flex justify-content-between mb-2">
      <span style="font-size:.7rem;color:var(--text3)">Alto consumo</span>
      <span style="font-size:.7rem;color:var(--gold-light);font-family:'JetBrains Mono',monospace">${alto} países</span>
    </div>
    <div class="prog-track mb-3"><div class="prog-fill" style="width:${(alto/paises.length*100).toFixed(1)}%"></div></div>
    <div class="d-flex justify-content-between mb-2">
      <span style="font-size:.7rem;color:var(--text3)">Baixo consumo</span>
      <span style="font-size:.7rem;color:var(--text3);font-family:'JetBrains Mono',monospace">${baixo} países</span>
    </div>
    <div class="prog-track"><div style="height:4px;border-radius:3px;background:rgba(201,168,76,.18);width:${(baixo/paises.length*100).toFixed(1)}%"></div></div>
  `;

  /* ── CATEGORIES AVG ── */
  const cats=['Cerveja','Destilados','Vinho'];
  const n=paises.length;
  const avgs=cats.map(k=>+(paises.reduce((s,d)=>s+d[k],0)/n).toFixed(1));
  const catColors=['#C9A84C','#C46E4A','#7060A8'];
  Plotly.newPlot('chart-cats',[{
    type:'bar',x:cats,y:avgs,
    text:avgs.map(v=>v+' srv'),textposition:'outside',
    textfont:{size:11,color:'#C0A868'},
    marker:{color:catColors,opacity:.88,line:{color:catColors.map(c=>c+'44'),width:1}},
    hovertemplate:'<b>%{x}</b><br>Média: %{y} servings/país<extra></extra>',
    width:[.4,.4,.4],
  }],{
    ...BL,...AX,
    margin:{t:12,b:28,l:44,r:8},
    yaxis:{...AX.yaxis,title:{text:'Servings médios',font:{size:10,color:'#6A5A30'}}},
    xaxis:{...AX.xaxis,showgrid:false,tickfont:{color:'#C0A868',size:12}},
    bargap:.5,
  },CFG);
}

async function livePoll(){
  try{
    const d=await fetch('/api/dashboard').then(r=>r.json());
    document.getElementById('kv-total').textContent=d.total_paises;
    document.getElementById('kv-media').textContent=d.media_alcool+'L';
    document.getElementById('kv-top').textContent=d.top_country;
    document.getElementById('kv-max').textContent=d.top_value;
    const t=new Date().toLocaleTimeString('pt-BR',{hour:'2-digit',minute:'2-digit'});
    document.getElementById('live-text').textContent=`Atualizado ${t} · ${d.nivel_alto} alto · ${d.nivel_baixo} baixo`;
  }catch(e){}
}

loadAll(); livePoll(); setInterval(livePoll,8000);
</script>
{% endblock %}




============================================================
===== templates/insights.html =====
============================================================

{% extends 'base.html' %}
{% block content %}

<div class="page-header">
  <div class="page-eyebrow">// análise automatizada</div>
  <h1 class="page-title"><span class="accent">Insights</span> Analíticos</h1>
  <p class="page-sub">Padrões e correlações extraídas automaticamente do dataset global</p>
</div>

<div class="row g-3 mb-3">
  <div class="col-md-7">
    <div class="card h-100">
      <div class="card-inner">
        <div class="sec-label">
          <svg viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="1.3" stroke-linecap="round"><path d="M6 1a5 5 0 100 10A5 5 0 006 1zm0 3v3"/><circle cx="6" cy="9" r=".6" fill="currentColor" stroke="none"/></svg>
          Destaques automáticos
        </div>
        <div id="insights-list"><p style="color:var(--text3);font-size:.85rem">Carregando...</p></div>
      </div>
    </div>
  </div>
  <div class="col-md-5">
    <div class="card h-100">
      <div class="chart-panel">
        <div class="sec-label">
          <svg viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="1.2"><circle cx="6" cy="6" r="5"/><path d="M6 6L6 1"/><path d="M6 6L10 9" opacity=".6"/></svg>
          Distribuição por nível
        </div>
        <div id="chart-nivel" style="height:220px"></div>
      </div>
    </div>
  </div>
</div>

<div class="row g-3">
  <div class="col-md-6">
    <div class="card h-100">
      <div class="chart-panel">
        <div class="sec-label">
          <svg viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="1.2"><circle cx="2.5" cy="9" r="1.4"/><circle cx="6" cy="5.5" r="1.4"/><circle cx="9.5" cy="2.5" r="1.4"/><line x1="2" y1="9" x2="10" y2="2" stroke-dasharray="1.5 1.5" opacity=".5"/></svg>
          Cerveja vs Álcool — Correlação
        </div>
        <div id="chart-corr" style="height:290px"></div>
      </div>
    </div>
  </div>
  <div class="col-md-6">
    <div class="card h-100">
      <div class="chart-panel">
        <div class="sec-label">
          <svg viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="1.2"><rect x="1" y="4" width="2.5" height="7" rx=".7" opacity=".5"/><rect x="4.75" y="2" width="2.5" height="9" rx=".7" opacity=".75"/><rect x="8.5" y="0" width="2.5" height="11" rx=".7"/></svg>
          Composição média global
        </div>
        <div id="chart-comp" style="height:290px"></div>
      </div>
    </div>
  </div>
</div>

<script>
const L={
  paper_bgcolor:'transparent',plot_bgcolor:'transparent',
  font:{color:'#8A7040',size:11,family:'Inter,sans-serif'},
  margin:{t:8,b:44,l:52,r:8},
  xaxis:{gridcolor:'rgba(201,168,76,.07)',zerolinecolor:'rgba(201,168,76,.12)',tickfont:{color:'#8A7040',size:10}},
  yaxis:{gridcolor:'rgba(201,168,76,.07)',zerolinecolor:'rgba(201,168,76,.12)',tickfont:{color:'#8A7040',size:10}},
};
const CFG={responsive:true,displayModeBar:false};

async function load(){
  const [ins,paises,dash]=await Promise.all([
    fetch('/api/insights').then(r=>r.json()),
    fetch('/api/paises').then(r=>r.json()),
    fetch('/api/dashboard').then(r=>r.json()),
  ]);

  document.getElementById('insights-list').innerHTML=ins.insights.map((txt,i)=>`
    <div class="insight-item" style="animation:fade-up .45s ${i*90}ms both">
      <span class="insight-num">${i+1}</span>
      <span style="font-size:.85rem;color:var(--text2);line-height:1.6">${txt}</span>
    </div>
  `).join('');

  Plotly.newPlot('chart-nivel',[{
    type:'pie',labels:['Alto','Baixo'],values:[dash.nivel_alto,dash.nivel_baixo],hole:.58,
    marker:{colors:['#C9A84C','#1C2840'],line:{color:'#080C18',width:2}},
    textinfo:'label+percent',textfont:{size:11,color:'#C9A84C'},
    hovertemplate:'<b>%{label}</b><br>%{value} países<extra></extra>',
  }],{...L,margin:{t:8,b:8,l:8,r:8},showlegend:false},CFG);

  Plotly.newPlot('chart-corr',[{
    type:'scatter',mode:'markers',
    x:paises.map(d=>d.Cerveja),y:paises.map(d=>d.LitrosAlcool),
    text:paises.map(d=>d.Pais),
    hovertemplate:'<b>%{text}</b><br>Cerveja: %{x}<br>Álcool: %{y}L<extra></extra>',
    marker:{color:paises.map(d=>d.LitrosAlcool),colorscale:[[0,'#0d0a04'],[.5,'#9a7020'],[1,'#e8d080']],size:7,opacity:.82,line:{color:'rgba(201,168,76,.2)',width:.5}},
  }],{...L,
    xaxis:{...L.xaxis,title:{text:'Servings de Cerveja',font:{size:10,color:'#6A5A30'}}},
    yaxis:{...L.yaxis,title:{text:'Litros Álcool Puro',font:{size:10,color:'#6A5A30'}}},
  },CFG);

  const avg=k=>paises.reduce((s,d)=>s+d[k],0)/paises.length;
  const cats=['Cerveja','Destilados','Vinho'];
  const vals=cats.map(k=>+avg(k).toFixed(1));
  Plotly.newPlot('chart-comp',[{
    type:'bar',x:cats,y:vals,
    marker:{color:['#C9A84C','#C46E4A','#7060A8'],opacity:.88,line:{color:['rgba(201,168,76,.25)','rgba(196,110,74,.25)','rgba(112,96,168,.25)'],width:1}},
    text:vals.map(v=>v.toFixed(1)),textposition:'outside',textfont:{color:'#C0A868',size:11},
    hovertemplate:'<b>%{x}</b><br>Média: %{y} servings<extra></extra>',
  }],{...L,
    yaxis:{...L.yaxis,title:{text:'Média de Servings',font:{size:10,color:'#6A5A30'}}},
  },CFG);
}
load();
</script>
{% endblock %}




============================================================
===== templates/paises.html =====
============================================================

{% extends 'base.html' %}
{% block content %}

<div class="d-flex align-items-start justify-content-between mb-5 flex-wrap gap-3">
  <div>
    <div class="page-eyebrow">// dados completos</div>
    <h1 class="page-title">Todos os <span class="accent">Países</span></h1>
    <p class="page-sub">Consumo detalhado por categoria — ordenável e pesquisável</p>
  </div>
  <div class="mt-2">
    <span id="count-badge" style="font-size:.72rem;color:var(--text3);background:var(--navy3);border:1px solid var(--border);padding:6px 16px;border-radius:20px;font-family:'JetBrains Mono',monospace"></span>
  </div>
</div>

<!-- Search -->
<div class="card mb-3">
  <div class="card-inner" style="padding:14px 18px">
    <div class="search-wrap">
      <span class="search-icon"><svg viewBox="0 0 14 14" fill="none"><circle cx="6" cy="6" r="4.5" stroke-width="1.4"/><line x1="9.5" y1="9.5" x2="13" y2="13" stroke-width="1.4" stroke-linecap="round"/></svg></span>
      <input type="text" id="search" class="search-input" placeholder="Buscar país...">
    </div>
  </div>
</div>

<!-- Table -->
<div class="card" style="overflow-x:auto">
  <table class="data-table">
    <thead>
      <tr>
        <th onclick="sortBy('Pais')">
          <span style="display:inline-flex;align-items:center;gap:6px">
            <svg width="10" height="10" viewBox="0 0 10 10" fill="none" stroke="currentColor" stroke-width="1.2"><circle cx="5" cy="5" r="4"/></svg>
            País <span id="sort-Pais" style="color:var(--gold)"></span>
          </span>
        </th>
        <th onclick="sortBy('Cerveja')" style="text-align:right">
          <span style="display:inline-flex;align-items:center;gap:6px;justify-content:flex-end">
            Cerveja <span id="sort-Cerveja" style="color:var(--gold)"></span>
          </span>
        </th>
        <th onclick="sortBy('Destilados')" style="text-align:right">
          <span style="display:inline-flex;align-items:center;gap:6px;justify-content:flex-end">
            Destilados <span id="sort-Destilados" style="color:var(--gold)"></span>
          </span>
        </th>
        <th onclick="sortBy('Vinho')" style="text-align:right">
          <span style="display:inline-flex;align-items:center;gap:6px;justify-content:flex-end">
            Vinho <span id="sort-Vinho" style="color:var(--gold)"></span>
          </span>
        </th>
        <th onclick="sortBy('LitrosAlcool')" style="text-align:right">
          <span style="display:inline-flex;align-items:center;gap:6px;justify-content:flex-end">
            Álcool (L) <span id="sort-LitrosAlcool" style="color:var(--gold)"></span>
          </span>
        </th>
        <th onclick="sortBy('TotalBebidas')" style="text-align:right">
          <span style="display:inline-flex;align-items:center;gap:6px;justify-content:flex-end">
            Total <span id="sort-TotalBebidas" style="color:var(--gold)"></span>
          </span>
        </th>
        <th>Nível</th>
      </tr>
    </thead>
    <tbody id="tbody"></tbody>
  </table>
</div>

<script>
let data=[],sortKey='TotalBebidas',sortAsc=false;

async function load(){
  data=await fetch('/api/paises').then(r=>r.json());
  render();
}

function bar(val,max,color){
  const pct=Math.round(val/max*100);
  return `<div class="mini-bar">
    <span style="color:var(--text2);font-family:'JetBrains Mono',monospace;font-size:.78rem">${val}</span>
    <div class="mini-bar-track"><div class="mini-bar-fill" style="width:${pct}%;background:${color}"></div></div>
  </div>`;
}

function render(){
  const q=document.getElementById('search').value.toLowerCase();
  let rows=data.filter(d=>d.Pais.toLowerCase().includes(q));
  if(sortKey){
    rows.sort((a,b)=>{
      const av=a[sortKey],bv=b[sortKey];
      if(typeof av==='string') return sortAsc?av.localeCompare(bv):bv.localeCompare(av);
      return sortAsc?av-bv:bv-av;
    });
  }
  const maxC=Math.max(...data.map(d=>d.Cerveja));
  const maxD=Math.max(...data.map(d=>d.Destilados));
  const maxV=Math.max(...data.map(d=>d.Vinho));
  const maxA=Math.max(...data.map(d=>d.LitrosAlcool));
  const maxT=Math.max(...data.map(d=>d.TotalBebidas));
  document.getElementById('tbody').innerHTML=rows.map(d=>`
    <tr>
      <td style="font-weight:500;color:var(--text2)">${d.Pais}</td>
      <td>${bar(d.Cerveja,maxC,'#C9A84C')}</td>
      <td>${bar(d.Destilados,maxD,'#C46E4A')}</td>
      <td>${bar(d.Vinho,maxV,'#7060A8')}</td>
      <td>${bar(d.LitrosAlcool,maxA,'#4A9E8E')}</td>
      <td>${bar(d.TotalBebidas,maxT,'#A07828')}</td>
      <td><span class="badge-${d.Nivel.toLowerCase()}">${d.Nivel}</span></td>
    </tr>
  `).join('');
  const keys=['Pais','Cerveja','Destilados','Vinho','LitrosAlcool','TotalBebidas'];
  keys.forEach(k=>{
    const el=document.getElementById(`sort-${k}`);
    if(el) el.textContent=sortKey===k?(sortAsc?'↑':'↓'):'';
  });
  document.getElementById('count-badge').textContent=`${rows.length} / ${data.length} países`;
}

function sortBy(key){
  if(sortKey===key) sortAsc=!sortAsc;
  else{sortKey=key;sortAsc=false;}
  render();
}
document.getElementById('search').addEventListener('input',render);
load();
</script>
{% endblock %}




============================================================
===== templates/comparar.html =====
============================================================

{% extends 'base.html' %}
{% block content %}

<div class="page-header">
  <div class="page-eyebrow">// análise comparativa</div>
  <h1 class="page-title"><span class="accent">Comparar</span> Países</h1>
  <p class="page-sub">Selecione entre 1 e 5 países para comparação detalhada lado a lado</p>
</div>

<div class="row g-3">
  <!-- ── Selector Panel ── -->
  <div class="col-md-3">
    <div class="card h-100">
      <div class="card-inner" style="padding:18px">
        <div class="sec-label">
          <svg viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="1.2"><circle cx="6" cy="4" r="2.5"/><path d="M2 11c0-2.2 1.8-4 4-4s4 1.8 4 4" stroke-linecap="round"/></svg>
          Países
        </div>

        <div class="search-wrap mb-3">
          <span class="search-icon"><svg viewBox="0 0 14 14" fill="none"><circle cx="6" cy="6" r="4.5" stroke-width="1.4"/><line x1="9.5" y1="9.5" x2="13" y2="13" stroke-width="1.4" stroke-linecap="round"/></svg></span>
          <input id="country-search" class="search-input" placeholder="Buscar..." style="font-size:.8rem;padding:8px 12px 8px 38px">
        </div>

        <div id="country-list" style="max-height:340px;overflow-y:auto;display:flex;flex-direction:column;gap:2px;margin-bottom:16px"></div>

        <div style="padding-top:14px;border-top:1px solid var(--border)">
          <div class="sec-label" style="margin-bottom:8px">Selecionados</div>
          <div id="selected-tags" style="min-height:24px;display:flex;flex-wrap:wrap;gap:4px"></div>
          <p id="select-hint" style="font-size:.68rem;color:var(--text3);margin-top:10px;font-family:'JetBrains Mono',monospace;line-height:1.5">
            Clique para selecionar
          </p>
        </div>
      </div>
    </div>
  </div>

  <!-- ── Chart Area ── -->
  <div class="col-md-9">

    <!-- Empty state (shown until 1 country selected) -->
    <div id="empty-state" class="card" style="display:flex;align-items:center;justify-content:center;min-height:560px;flex-direction:column;gap:16px">
      <svg width="48" height="48" viewBox="0 0 48 48" fill="none" stroke="rgba(201,168,76,.3)" stroke-width="1.2"><polygon points="24,4 44,40 4,40" stroke-linejoin="round"/><line x1="24" y1="16" x2="24" y2="30" stroke-linecap="round"/><circle cx="24" cy="35" r="1.5" fill="rgba(201,168,76,.3)" stroke="none"/></svg>
      <p style="font-family:'JetBrains Mono',monospace;font-size:.8rem;color:var(--text3);text-align:center;line-height:1.8">
        Selecione ao menos um país<br>para visualizar os gráficos
      </p>
    </div>

    <!-- Charts (hidden until selection) -->
    <div id="charts-area" style="display:none">

      <!-- Radar -->
      <div class="card mb-3">
        <div class="chart-panel">
          <div class="sec-label">
            <svg viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="1.2"><polygon points="6,1 11,4 11,8 6,11 1,8 1,4"/></svg>
            Radar — Perfil de consumo normalizado
          </div>
          <div id="chart-radar" style="width:100%;height:350px"></div>
        </div>
      </div>

      <!-- Bar + Line -->
      <div class="card mb-3">
        <div class="chart-panel">
          <div class="sec-label">
            <svg viewBox="0 0 12 12" fill="currentColor" stroke="none"><rect x="1" y="4" width="2.5" height="7" rx=".5" opacity=".5"/><rect x="4.75" y="2" width="2.5" height="9" rx=".5" opacity=".75"/><rect x="8.5" y="0" width="2.5" height="11" rx=".5"/></svg>
            Álcool puro (L) &amp; Total servings
          </div>
          <div id="chart-bar" style="width:100%;height:230px"></div>
        </div>
      </div>

      <!-- Stacked -->
      <div class="card mb-3">
        <div class="chart-panel">
          <div class="sec-label">
            <svg viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="1.2"><rect x="1" y="1" width="10" height="10" rx="1"/><line x1="1" y1="4.5" x2="11" y2="4.5" opacity=".4"/><line x1="1" y1="7.5" x2="11" y2="7.5" opacity=".4"/></svg>
            Composição — Cerveja · Destilados · Vinho
          </div>
          <div id="chart-stack" style="width:100%;height:230px"></div>
        </div>
      </div>

      <!-- Table -->
      <div class="card">
        <div class="card-inner">
          <div class="sec-label">
            <svg viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="1.2"><rect x="1" y="2" width="10" height="1.5" rx=".75"/><rect x="1" y="5.5" width="10" height="1.5" rx=".75"/><rect x="1" y="9" width="7" height="1.5" rx=".75"/></svg>
            Dados tabulares
          </div>
          <div style="overflow-x:auto">
            <table class="data-table">
              <thead>
                <tr>
                  <th>País</th>
                  <th style="text-align:right">Cerveja</th>
                  <th style="text-align:right">Destilados</th>
                  <th style="text-align:right">Vinho</th>
                  <th style="text-align:right">Total</th>
                  <th style="text-align:right">Álcool (L)</th>
                  <th>Nível</th>
                </tr>
              </thead>
              <tbody id="stats-tbody"></tbody>
            </table>
          </div>
        </div>
      </div>

    </div><!-- /charts-area -->
  </div>
</div>

<script>
const PAL=['#C9A84C','#E07840','#6090D0','#80C060','#C060A0'];
const CFG={responsive:true,displayModeBar:false};
const BL={
  paper_bgcolor:'transparent',plot_bgcolor:'transparent',
  font:{color:'#8A7040',size:11,family:'Inter,sans-serif'},
};
const AX={
  xaxis:{gridcolor:'rgba(201,168,76,.07)',zerolinecolor:'rgba(201,168,76,.12)',tickfont:{color:'#8A7040',size:10}},
  yaxis:{gridcolor:'rgba(201,168,76,.07)',zerolinecolor:'rgba(201,168,76,.12)',tickfont:{color:'#8A7040',size:10}},
};

let all=[],sel=[];
let radarInit=false,barInit=false,stackInit=false;

async function init(){
  all=await fetch('/api/paises').then(r=>r.json());
  renderList('');
}

function renderList(q){
  const f=all.filter(d=>d.Pais.toLowerCase().includes(q.toLowerCase()));
  document.getElementById('country-list').innerHTML=f.slice(0,120).map(d=>{
    const on=sel.includes(d.Pais);
    const idx=sel.indexOf(d.Pais);
    const col=on?PAL[idx]:'';
    return `<div onclick="toggle('${d.Pais.replace(/\\/g,'\\\\').replace(/'/g,"\\'")}');" style="
      display:flex;align-items:center;justify-content:space-between;
      padding:7px 10px;border-radius:5px;font-size:.8rem;user-select:none;
      background:${on?col+'1A':'transparent'};
      color:${on?col:'var(--text3)'};
      border:1px solid ${on?col+'44':'transparent'};
      transition:.12s ease">
      <span>${d.Pais}</span>
      ${on?`<svg width="11" height="11" viewBox="0 0 12 12" fill="none" stroke="${col}" stroke-width="1.8" stroke-linecap="round"><path d="M2 6l3 3 5-5"/></svg>`:''}
    </div>`;
  }).join('');
}

function toggle(p){
  const i=sel.indexOf(p);
  if(i>=0) sel.splice(i,1);
  else{ if(sel.length>=5) return; sel.push(p); }
  renderList(document.getElementById('country-search').value);
  renderTags();
  updateCharts();
}

function renderTags(){
  document.getElementById('selected-tags').innerHTML=sel.map((p,i)=>`
    <span onclick="toggle('${p.replace(/\\/g,'\\\\').replace(/'/g,"\\'")}');" style="
      display:inline-flex;align-items:center;gap:5px;cursor:pointer;
      background:${PAL[i]}22;border:1px solid ${PAL[i]}55;color:${PAL[i]};
      border-radius:20px;padding:3px 10px;font-size:.72rem;line-height:1.4;
      transition:.12s ease">
      ${p}
      <svg width="8" height="8" viewBox="0 0 10 10" fill="none" stroke="${PAL[i]}" stroke-width="1.6" stroke-linecap="round"><path d="M2 2l6 6M8 2l-6 6"/></svg>
    </span>`).join('');
  const h=document.getElementById('select-hint');
  if(!sel.length) h.textContent='Clique para selecionar';
  else if(sel.length===1) h.textContent='Selecione mais 1 para comparar';
  else if(sel.length>=5) h.textContent='Máximo de 5 países';
  else h.textContent=`${sel.length} países selecionados`;
}

function updateCharts(){
  if(!sel.length){
    document.getElementById('empty-state').style.display='';
    document.getElementById('charts-area').style.display='none';
    return;
  }
  document.getElementById('empty-state').style.display='none';
  document.getElementById('charts-area').style.display='';

  const rows=sel.map(p=>all.find(d=>d.Pais===p)).filter(Boolean);
  const cats  =['Cerveja','Destilados','Vinho','LitrosAlcool','TotalBebidas'];
  const labs  =['Cerveja','Destilados','Vinho','Álcool (L)','Total'];
  const maxes=cats.map(k=>Math.max(...all.map(d=>d[k])));

  /* ── RADAR ── */
  const radarT=rows.map((r,i)=>{
    const vals=cats.map((k,ki)=>+(r[k]/maxes[ki]*100).toFixed(1));
    return {
      type:'scatterpolar',
      r:[...vals,vals[0]],
      theta:[...labs,labs[0]],
      name:r.Pais,fill:'toself',
      fillcolor:PAL[i]+'28',
      line:{color:PAL[i],width:2.2},
      marker:{color:PAL[i],size:5},
      hovertemplate:`<b>${r.Pais}</b><br>%{theta}: %{r:.1f}%<extra></extra>`,
    };
  });
  const radarLayout={
    ...BL,
    polar:{
      bgcolor:'rgba(14,21,40,.5)',
      angularaxis:{color:'rgba(201,168,76,.18)',gridcolor:'rgba(201,168,76,.1)',tickfont:{color:'#8A7040',size:10},linecolor:'rgba(201,168,76,.15)'},
      radialaxis:{color:'rgba(201,168,76,.1)',gridcolor:'rgba(201,168,76,.08)',range:[0,105],showticklabels:false,linecolor:'transparent'},
    },
    margin:{t:24,b:48,l:52,r:52},
    showlegend:true,
    legend:{bgcolor:'rgba(8,12,24,.5)',font:{color:'#C9A84C',size:11},orientation:'h',x:.5,xanchor:'center',y:-.1},
  };
  if(!radarInit){ Plotly.newPlot('chart-radar',radarT,radarLayout,CFG); radarInit=true; }
  else Plotly.react('chart-radar',radarT,radarLayout,CFG);

  /* ── BAR + LINE ── */
  const barT=[{
    type:'bar',name:'Álcool puro (L)',
    x:rows.map(r=>r.Pais),y:rows.map(r=>r.LitrosAlcool),
    marker:{color:rows.map((_,i)=>PAL[i]),opacity:.88,line:{color:'rgba(8,12,24,.4)',width:.8}},
    text:rows.map(r=>r.LitrosAlcool+'L'),textposition:'outside',textfont:{size:10,color:'#C0A868'},
    hovertemplate:'<b>%{x}</b><br>Álcool puro: %{y}L<extra></extra>',yaxis:'y',
  },{
    type:'scatter',mode:'markers+lines',name:'Total servings',
    x:rows.map(r=>r.Pais),y:rows.map(r=>r.TotalBebidas),
    marker:{color:rows.map((_,i)=>PAL[i]),size:11,symbol:'diamond',line:{color:'#080C18',width:1.5}},
    line:{color:'rgba(201,168,76,.35)',width:1.5,dash:'dot'},
    hovertemplate:'<b>%{x}</b><br>Total: %{y} servings<extra></extra>',yaxis:'y2',
  }];
  const barLayout={
    ...BL,...AX,
    margin:{t:16,b:48,l:48,r:56},barmode:'group',showlegend:true,
    legend:{bgcolor:'rgba(8,12,24,.5)',font:{color:'#C9A84C',size:11},orientation:'h',x:.5,xanchor:'center',y:1.1},
    yaxis:{...AX.yaxis,title:{text:'Álcool (L)',font:{size:9,color:'#6A5A30'}}},
    yaxis2:{overlaying:'y',side:'right',gridcolor:'transparent',tickfont:{color:'#8A7050',size:9},title:{text:'Total servings',font:{size:9,color:'#6A5A30'}},zeroline:false},
  };
  if(!barInit){ Plotly.newPlot('chart-bar',barT,barLayout,CFG); barInit=true; }
  else Plotly.react('chart-bar',barT,barLayout,CFG);

  /* ── STACKED BAR ── */
  const catKeys =['Cerveja','Destilados','Vinho'];
  const catCols =['#C9A84C','#C46E4A','#7060A8'];
  const catNames=['Cerveja','Destilados','Vinho'];
  const stackT=catKeys.map((k,ki)=>({
    type:'bar',name:catNames[ki],
    x:rows.map(r=>r.Pais),y:rows.map(r=>r[k]),
    marker:{color:catCols[ki],opacity:.85,line:{color:'rgba(8,12,24,.3)',width:.6}},
    hovertemplate:`<b>%{x}</b><br>${catNames[ki]}: %{y} servings<extra></extra>`,
  }));
  const stackLayout={
    ...BL,...AX,
    margin:{t:16,b:48,l:48,r:8},barmode:'stack',showlegend:true,
    legend:{bgcolor:'rgba(8,12,24,.5)',font:{color:'#C9A84C',size:11},orientation:'h',x:.5,xanchor:'center',y:1.1},
    yaxis:{...AX.yaxis,title:{text:'Servings',font:{size:9,color:'#6A5A30'}}},
  };
  if(!stackInit){ Plotly.newPlot('chart-stack',stackT,stackLayout,CFG); stackInit=true; }
  else Plotly.react('chart-stack',stackT,stackLayout,CFG);

  /* ── TABLE ── */
  document.getElementById('stats-tbody').innerHTML=rows.map((r,i)=>`
    <tr>
      <td style="font-weight:600;color:${PAL[i]}">${r.Pais}</td>
      <td style="text-align:right;font-family:'JetBrains Mono',monospace;font-size:.78rem;color:var(--text2)">${r.Cerveja}</td>
      <td style="text-align:right;font-family:'JetBrains Mono',monospace;font-size:.78rem;color:#C08060">${r.Destilados}</td>
      <td style="text-align:right;font-family:'JetBrains Mono',monospace;font-size:.78rem;color:#8878C0">${r.Vinho}</td>
      <td style="text-align:right;font-family:'JetBrains Mono',monospace;font-size:.78rem;color:var(--gold-light);font-weight:600">${r.TotalBebidas}</td>
      <td style="text-align:right;font-family:'JetBrains Mono',monospace;font-size:.78rem">${r.LitrosAlcool}L</td>
      <td><span class="badge-${r.Nivel.toLowerCase()}">${r.Nivel}</span></td>
    </tr>
  `).join('');

  /* force resize to ensure charts fill containers */
  setTimeout(()=>{ Plotly.Plots.resize('chart-radar'); Plotly.Plots.resize('chart-bar'); Plotly.Plots.resize('chart-stack'); },80);
}

document.getElementById('country-search').addEventListener('input',e=>renderList(e.target.value));
init();
</script>
{% endblock %}



