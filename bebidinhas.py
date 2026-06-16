# ===== bebidinhas/app.py =====
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from flask import Flask, render_template
from api.routes import api
from services.data_loader import carregar_dados

app = Flask(__name__)
app.register_blueprint(api)

@app.route("/")
def dashboard():
    df = carregar_dados()
    return render_template(
        "dashboard.html",
        total=len(df),
        media=round(float(df["LitrosAlcool"].mean()), 2),
        max_country=df.loc[df["TotalBebidas"].idxmax()]["Pais"],
        max_value=int(df["TotalBebidas"].max()),
    )

@app.route("/insights")
def insights_page():
    return render_template("insights.html")

@app.route("/paises")
def paises_page():
    return render_template("paises.html")

@app.route("/comparar")
def comparar_page():
    return render_template("comparar.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)


# ===== bebidinhas/requirements.txt =====
Flask
pandas
numpy
gunicorn


# ===== bebidinhas/api/__init__.py =====


# ===== bebidinhas/api/routes.py =====
from flask import Blueprint, jsonify
from services.data_loader import carregar_dados
from services.analytics import gerar_insights

api = Blueprint("api", __name__)

@api.route("/api/dashboard")
def dashboard_api():
    df = carregar_dados()
    return jsonify({
        "total_paises": len(df),
        "media_alcool": round(float(df["LitrosAlcool"].mean()), 2),
        "top_country": df.loc[df["TotalBebidas"].idxmax()]["Pais"],
        "top_value": int(df["TotalBebidas"].max()),
        "nivel_alto": int((df["Nivel"] == "Alto").sum()),
        "nivel_baixo": int((df["Nivel"] == "Baixo").sum()),
    })

@api.route("/api/top10")
def top10():
    df = carregar_dados()
    top = df.nlargest(10, "Cerveja")
    return jsonify(top[["Pais", "Cerveja"]].to_dict(orient="records"))

@api.route("/api/top10-alcool")
def top10_alcool():
    df = carregar_dados()
    top = df.nlargest(10, "LitrosAlcool")
    return jsonify(top[["Pais", "LitrosAlcool", "TotalBebidas"]].to_dict(orient="records"))

@api.route("/api/paises")
def paises():
    df = carregar_dados()
    return jsonify(df[["Pais", "Cerveja", "Destilados", "Vinho", "LitrosAlcool", "TotalBebidas", "Nivel"]].to_dict(orient="records"))

@api.route("/api/insights")
def insights_api():
    df = carregar_dados()
    return jsonify({"insights": gerar_insights(df)})


# ===== bebidinhas/services/__init__.py =====


# ===== bebidinhas/services/data_loader.py =====
import pandas as pd
import numpy as np
import os

def carregar_dados():
    path = os.path.join(os.path.dirname(__file__), "..", "data", "drinks.csv")
    df = pd.read_csv(path)
    df.columns = ["Pais", "Cerveja", "Destilados", "Vinho", "LitrosAlcool"]
    df["TotalBebidas"] = df["Cerveja"] + df["Destilados"] + df["Vinho"]
    df["Nivel"] = np.where(df["LitrosAlcool"] > df["LitrosAlcool"].mean(), "Alto", "Baixo")
    return df


# ===== bebidinhas/services/analytics.py =====
def gerar_insights(df):
    insights = []
    media = df["LitrosAlcool"].mean()
    acima = len(df[df["LitrosAlcool"] > media])
    insights.append(f"{acima} países acima da média global")
    top = df.loc[df["TotalBebidas"].idxmax()]
    insights.append(f"Maior consumidor: {top['Pais']}")
    corr = df["Cerveja"].corr(df["LitrosAlcool"])
    insights.append(f"Correlação cerveja vs álcool: {corr:.2f}")
    baixo = len(df[df["LitrosAlcool"] == 0])
    insights.append(f"{baixo} países sem consumo registrado")
    top3 = df.nlargest(3, "LitrosAlcool")[["Pais", "LitrosAlcool"]].values
    insights.append(f"Top 3 em álcool puro: {', '.join([f'{p} ({v}L)' for p, v in top3])}")
    return insights


# ===== bebidinhas/templates/base.html =====
<!DOCTYPE html>
<html lang="pt-br">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Bebidinhas SaaS</title>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400&display=swap" rel="stylesheet">
<script src="https://cdn.plot.ly/plotly-2.35.2.min.js"></script>
<style>
  :root {
    --gold: #c9a84c;
    --gold-light: #e0b85a;
    --gold-dim: #a07830;
    --gold-faint: rgba(201,168,76,.08);
    --bg: #080604;
    --surface: #0f0a05;
    --surface2: #160f07;
    --border: #2a1e0e;
    --border-hover: #4a3820;
    --text: #c9a84c;
    --text-dim: #8a6828;
  }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  html { scroll-behavior: smooth; }

  body {
    background: var(--bg);
    color: var(--text);
    font-family: 'Segoe UI', Arial, sans-serif;
    min-height: 100vh;
  }

  .bg-grid { display: none; }

  /* Glow blob */
  .bg-glow {
    position: fixed; top: -20vh; right: -10vw; z-index: -1;
    width: 60vw; height: 60vw; border-radius: 50%;
    background: radial-gradient(ellipse, rgba(201,168,76,.06) 0%, transparent 70%);
    pointer-events: none;
  }

  /* Navbar */
  nav {
    position: sticky; top: 0; z-index: 100;
    background: rgba(8,6,4,.92);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border-bottom: 1px solid var(--border);
    padding: 0 28px;
    display: flex;
    align-items: center;
    height: 56px;
    gap: 8px;
  }
  .nav-brand {
    display: flex; align-items: center; gap: 10px;
    font-size: 1.05rem; font-weight: 700;
    color: var(--gold-light); text-decoration: none;
    margin-right: 20px;
    letter-spacing: .02em;
  }
  .nav-brand svg { flex-shrink: 0; }
  .nav-link-item {
    display: flex; align-items: center; gap: 6px;
    color: var(--text-dim); text-decoration: none;
    font-size: 0.85rem; padding: 6px 12px; border-radius: 6px;
    transition: color .2s, background .2s;
    white-space: nowrap;
  }
  .nav-link-item:hover { color: var(--gold-light); background: var(--gold-faint); }
  .nav-link-item.active { color: var(--gold-light); background: rgba(201,168,76,.12); }
  .nav-spacer { flex: 1; }
  .nav-badge {
    font-size: .7rem; background: rgba(201,168,76,.15);
    border: 1px solid var(--border); color: var(--gold-dim);
    padding: 2px 8px; border-radius: 20px; letter-spacing: .05em;
  }

  /* Cards */
  .card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 14px;
    transition: border-color .25s, transform .2s, box-shadow .25s;
  }
  .card:hover { border-color: var(--border-hover); box-shadow: 0 4px 32px rgba(201,168,76,.06); }
  .card-body { padding: 22px; }

  /* KPI cards */
  .kpi-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 22px;
    position: relative;
    overflow: hidden;
    transition: border-color .25s, transform .2s, box-shadow .25s;
  }
  .kpi-card::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, transparent, var(--gold), transparent);
    opacity: 0; transition: opacity .3s;
  }
  .kpi-card:hover { border-color: var(--border-hover); transform: translateY(-2px); box-shadow: 0 8px 32px rgba(201,168,76,.08); }
  .kpi-card:hover::before { opacity: 1; }
  .kpi-icon { margin-bottom: 14px; opacity: .7; }
  .kpi-label { font-size: .72rem; text-transform: uppercase; letter-spacing: .1em; color: var(--text-dim); margin-bottom: 6px; }
  .kpi-value { font-size: 2rem; font-weight: 700; color: var(--gold-light); line-height: 1; }
  .kpi-sub { font-size: .75rem; color: var(--text-dim); margin-top: 6px; }

  /* Section title */
  .section-title {
    font-size: .7rem; text-transform: uppercase; letter-spacing: .12em;
    color: var(--text-dim); margin-bottom: 16px;
    display: flex; align-items: center; gap: 8px;
  }
  .section-title::after {
    content: ''; flex: 1; height: 1px; background: var(--border);
  }

  /* Chart container */
  .chart-wrap { padding: 20px; }

  /* Live ticker */
  .live-ticker {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 12px 18px;
    font-size: .78rem; color: var(--text-dim);
    display: flex; align-items: center; gap: 12px;
  }
  .live-dot {
    width: 7px; height: 7px; border-radius: 50%;
    background: var(--gold); flex-shrink: 0;
    animation: pulse 2s ease-in-out infinite;
  }
  @keyframes pulse {
    0%,100% { opacity: 1; transform: scale(1); }
    50% { opacity: .4; transform: scale(.8); }
  }

  /* Badge */
  .badge-alto {
    background: rgba(201,168,76,.15); color: var(--gold-light);
    padding: 3px 9px; border-radius: 20px; font-size: .72rem;
    border: 1px solid rgba(201,168,76,.25);
  }
  .badge-baixo {
    background: rgba(42,30,14,.5); color: var(--text-dim);
    padding: 3px 9px; border-radius: 20px; font-size: .72rem;
    border: 1px solid var(--border);
  }

  /* Table */
  .data-table { width: 100%; border-collapse: collapse; font-size: .84rem; }
  .data-table th {
    padding: 10px 14px; color: var(--text-dim);
    font-size: .7rem; text-transform: uppercase; letter-spacing: .08em;
    border-bottom: 1px solid var(--border); cursor: pointer;
    user-select: none; white-space: nowrap;
    transition: color .2s;
  }
  .data-table th:hover { color: var(--gold-light); }
  .data-table td { padding: 9px 14px; border-bottom: 1px solid rgba(42,30,14,.7); }
  .data-table tbody tr { transition: background .15s; }
  .data-table tbody tr:hover { background: var(--gold-faint); }

  /* Search input */
  .search-input {
    background: var(--surface2); border: 1px solid var(--border);
    color: var(--text); padding: 10px 16px 10px 42px; border-radius: 8px;
    width: 100%; font-size: .9rem; outline: none;
    transition: border-color .2s, box-shadow .2s;
  }
  .search-input:focus { border-color: var(--border-hover); box-shadow: 0 0 0 3px rgba(201,168,76,.07); }
  .search-input::placeholder { color: var(--text-dim); }
  .search-wrap { position: relative; }
  .search-icon { position: absolute; left: 14px; top: 50%; transform: translateY(-50%); }

  /* Insight items */
  .insight-item {
    display: flex; gap: 14px; align-items: flex-start;
    padding: 14px 0; border-bottom: 1px solid var(--border);
    animation: fade-in .4s ease both;
  }
  .insight-item:last-child { border-bottom: none; }
  .insight-num {
    width: 26px; height: 26px; border-radius: 50%;
    background: rgba(201,168,76,.12); border: 1px solid rgba(201,168,76,.2);
    display: flex; align-items: center; justify-content: center;
    font-size: .72rem; font-weight: 700; color: var(--gold-light);
    flex-shrink: 0;
  }
  @keyframes fade-in {
    from { opacity: 0; transform: translateY(8px); }
    to { opacity: 1; transform: translateY(0); }
  }

  /* Country selector tags */
  .country-tag {
    display: inline-flex; align-items: center; gap: 6px;
    background: rgba(201,168,76,.12); border: 1px solid rgba(201,168,76,.25);
    color: var(--gold-light); border-radius: 20px;
    padding: 4px 10px; font-size: .8rem; cursor: pointer;
    transition: background .2s; margin: 3px;
  }
  .country-tag:hover, .country-tag.selected { background: rgba(201,168,76,.25); }
  .country-tag .remove { color: var(--gold-dim); font-size: .9rem; }

  /* Select dropdown */
  select.styled {
    background: var(--surface2); border: 1px solid var(--border);
    color: var(--text); padding: 9px 12px; border-radius: 8px;
    font-size: .85rem; outline: none; cursor: pointer;
    transition: border-color .2s;
  }
  select.styled:focus { border-color: var(--border-hover); }

  /* Progress bar */
  .progress-bar-custom {
    height: 4px; border-radius: 2px;
    background: linear-gradient(90deg, var(--gold-dim), var(--gold-light));
    transition: width .6s ease;
  }
  .progress-track { background: var(--surface2); border-radius: 2px; overflow: hidden; }

  /* Scrollbar */
  ::-webkit-scrollbar { width: 6px; height: 6px; }
  ::-webkit-scrollbar-track { background: var(--bg); }
  ::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
  ::-webkit-scrollbar-thumb:hover { background: var(--border-hover); }

  /* Tooltip override */
  [data-bs-toggle="tooltip"] { cursor: help; }

  /* Code rain */
  .code-rain {
    position: fixed; inset: 0; z-index: 0;
    pointer-events: none; overflow: hidden;
    opacity: .13;
  }
  .code-rain span {
    position: absolute;
    top: -120px;
    color: #c9a84c;
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    font-weight: 300;
    white-space: nowrap;
    animation: code-fall linear infinite;
    text-shadow: 0 0 6px rgba(201,168,76,.4);
  }
  @keyframes code-fall {
    0%   { transform: translateY(-120px); opacity: 0; }
    8%   { opacity: 1; }
    92%  { opacity: .7; }
    100% { transform: translateY(110vh); opacity: 0; }
  }
</style>
</head>
<body>
<div class="bg-grid"></div>
<div class="bg-glow"></div>
<div class="code-rain" id="code-rain"></div>

<nav>
  <a class="nav-brand" href="/">
    <!-- Negroni glass — golden line art only -->
    <svg width="20" height="24" viewBox="0 0 20 24" fill="none" xmlns="http://www.w3.org/2000/svg">
      <!-- glass body outline -->
      <path d="M2 3.5 L18 3.5 L15.5 18 L4.5 18 Z"
            stroke="#c9a84c" stroke-width="1.2" stroke-linejoin="round"/>
      <!-- rim top bar -->
      <line x1="2" y1="3.5" x2="18" y2="3.5" stroke="#e0b85a" stroke-width="1.5" stroke-linecap="round"/>
      <!-- base platform -->
      <line x1="4.5" y1="18" x2="15.5" y2="18" stroke="#c9a84c" stroke-width="1.5" stroke-linecap="round"/>
      <!-- coaster -->
      <line x1="3.5" y1="20" x2="16.5" y2="20" stroke="#a07830" stroke-width="1" stroke-linecap="round"/>
      <!-- ice cube outline -->
      <rect x="7.5" y="9" width="5" height="5" rx="1" stroke="#c9a84c" stroke-width=".9" opacity=".7"/>
      <!-- liquid level line -->
      <line x1="4.9" y1="13.5" x2="15.1" y2="13.5" stroke="#a07830" stroke-width=".8" stroke-dasharray="2 1.5" opacity=".6"/>
      <!-- orange peel swirl -->
      <path d="M14.5 2.5 Q17.5 0 16.5 3.5" stroke="#c9a84c" stroke-width="1.1" stroke-linecap="round"/>
    </svg>
    Bebidinhas SaaS
  </a>

  <a href="/" class="nav-link-item {% if request.endpoint == 'dashboard' %}active{% endif %}">
    <svg width="14" height="14" viewBox="0 0 14 14" fill="none"><rect x="1" y="7" width="3" height="6" rx="1" fill="currentColor"/><rect x="5.5" y="4" width="3" height="9" rx="1" fill="currentColor"/><rect x="10" y="1" width="3" height="12" rx="1" fill="currentColor"/></svg>
    Dashboard
  </a>
  <a href="/insights" class="nav-link-item {% if request.endpoint == 'insights_page' %}active{% endif %}">
    <svg width="14" height="14" viewBox="0 0 14 14" fill="none"><circle cx="7" cy="7" r="5.5" stroke="currentColor" stroke-width="1.3"/><path d="M7 4.5v3l2 1.2" stroke="currentColor" stroke-width="1.3" stroke-linecap="round"/></svg>
    Insights
  </a>
  <a href="/paises" class="nav-link-item {% if request.endpoint == 'paises_page' %}active{% endif %}">
    <svg width="14" height="14" viewBox="0 0 14 14" fill="none"><rect x="1" y="2" width="12" height="1.5" rx=".75" fill="currentColor"/><rect x="1" y="6" width="12" height="1.5" rx=".75" fill="currentColor"/><rect x="1" y="10" width="8" height="1.5" rx=".75" fill="currentColor"/></svg>
    Países
  </a>
  <a href="/comparar" class="nav-link-item {% if request.endpoint == 'comparar_page' %}active{% endif %}">
    <svg width="14" height="14" viewBox="0 0 14 14" fill="none"><polygon points="7,1 13,11 1,11" stroke="currentColor" stroke-width="1.3" fill="none" stroke-linejoin="round"/></svg>
    Comparar
  </a>

  <div class="nav-spacer"></div>
  <span class="nav-badge">193 países</span>
</nav>

<div class="container-fluid py-4 px-4" style="max-width:1400px;margin:0 auto">
{% block content %}{% endblock %}
</div>

<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>

<script>
// ── Code Rain ────────────────────────────────────────────────
(function () {
  const SNIPPETS = [
    'import flask', 'import pandas as pd', 'import numpy as np',
    '@api.route("/top10")', '@app.route("/")', 'def carregar_dados():',
    'return jsonify(data)', 'df.groupby("Pais")', 'df.nlargest(10)',
    'pd.read_csv(path)', 'df["LitrosAlcool"].mean()', 'np.where(cond, "Alto", "Baixo")',
    'Blueprint("api", __name__)', 'render_template("dashboard.html")',
    'SELECT * FROM drinks', 'GROUP BY country', 'ORDER BY total DESC',
    'df.columns = ["Pais","Cerveja"]', 'corr = df["Cerveja"].corr(df["LitrosAlcool"])',
    'app.register_blueprint(api)', 'gunicorn app:app', 'PORT=5000',
    'from flask import jsonify', 'df.loc[df["TotalBebidas"].idxmax()]',
    '{ "total_paises": 193 }', '"media_alcool": 4.72',
    'df["TotalBebidas"] = df.sum()', 'os.environ.get("PORT")',
    'fetch("/api/dashboard")', 'Plotly.newPlot("chart")',
    '.then(r => r.json())', 'async function load()',
    '#!/usr/bin/env python3', '# -*- coding: utf-8 -*-',
    'for pais in df.itertuples():', 'if __name__ == "__main__":',
    '>>> df.describe()', '>>> df.shape', '(193, 6)',
    '{}', '[]', '()', '=>', '//', '--', '**', '&&', '||',
    '0x1A', '0xFF', '#!/bin', 'null', 'true', 'false',
  ];

  const container = document.getElementById('code-rain');
  const COUNT = 28;

  for (let i = 0; i < COUNT; i++) {
    const span = document.createElement('span');
    const left = Math.random() * 100;
    const duration = 10 + Math.random() * 18;   // 10–28 s
    const delay = -(Math.random() * duration);   // start at random point in cycle
    const txt = SNIPPETS[Math.floor(Math.random() * SNIPPETS.length)];

    span.textContent = txt;
    span.style.left = left + 'vw';
    span.style.animationDuration = duration + 's';
    span.style.animationDelay = delay + 's';
    // Vary opacity per column for depth
    span.style.opacity = (0.4 + Math.random() * 0.6).toString();

    container.appendChild(span);
  }
})();
</script>

<script>
(function () {
  let ctx = null;

  function getCtx() {
    if (!ctx) ctx = new (window.AudioContext || window.webkitAudioContext)();
    return ctx;
  }

  // Clean, subtle tick — fires only once per element entry (mouseenter)
  function playTick() {
    try {
      const ac = getCtx();
      if (ac.state === 'suspended') ac.resume();
      const now = ac.currentTime;

      // Very short noise burst — tight bandpass around 1.8 kHz
      const len = Math.floor(ac.sampleRate * 0.012);
      const buf = ac.createBuffer(1, len, ac.sampleRate);
      const d = buf.getChannelData(0);
      for (let i = 0; i < len; i++) {
        d[i] = (Math.random() * 2 - 1) * Math.exp(-i / len * 10);
      }
      const src = ac.createBufferSource();
      src.buffer = buf;

      const bp = ac.createBiquadFilter();
      bp.type = 'bandpass';
      bp.frequency.value = 1800;
      bp.Q.value = 2.8;

      const gain = ac.createGain();
      gain.gain.setValueAtTime(0.28, now);
      gain.gain.exponentialRampToValueAtTime(0.0001, now + 0.012);

      src.connect(bp); bp.connect(gain); gain.connect(ac.destination);
      src.start(now); src.stop(now + 0.015);
    } catch (e) {}
  }

  const HOVER_SEL = [
    'a', 'button', '[onclick]', 'th[onclick]',
    '.nav-link-item', '.country-tag', '.kpi-card',
    'input[type="text"]', 'input[type="search"]',
    'select'
  ].join(',');

  // mouseenter fires once when cursor enters — does not repeat while inside
  document.addEventListener('mouseenter', function (e) {
    if (e.target.closest && e.target.closest(HOVER_SEL)) playTick();
  }, { passive: true, capture: true });

  document.addEventListener('click', function () {
    if (ctx && ctx.state === 'suspended') ctx.resume();
  }, { once: true, passive: true });
})();
</script>
</body>
</html>


# ===== bebidinhas/templates/dashboard.html =====
{% extends 'base.html' %}
{% block content %}

<div class="d-flex align-items-center justify-content-between mb-4">
  <div>
    <h1 style="font-size:1.4rem;font-weight:700;color:var(--gold-light)">Visão Global</h1>
    <p style="font-size:.82rem;color:var(--text-dim);margin-top:2px">Consumo de bebidas alcoólicas por país</p>
  </div>
  <div class="live-ticker">
    <span class="live-dot"></span>
    <span id="live-text">Atualizando...</span>
  </div>
</div>

<!-- KPI row -->
<div class="row g-3 mb-4">
  <div class="col-6 col-md-3">
    <div class="kpi-card">
      <div class="kpi-icon">
        <svg width="20" height="20" viewBox="0 0 20 20" fill="none"><circle cx="10" cy="10" r="8.5" stroke="#c9a84c" stroke-width="1.4"/><path d="M10 5.5v5l3 1.8" stroke="#c9a84c" stroke-width="1.4" stroke-linecap="round"/></svg>
      </div>
      <div class="kpi-label">Países analisados</div>
      <div class="kpi-value" id="kv-total">{{ total }}</div>
      <div class="kpi-sub">dataset global completo</div>
    </div>
  </div>
  <div class="col-6 col-md-3">
    <div class="kpi-card">
      <div class="kpi-icon">
        <svg width="20" height="20" viewBox="0 0 20 20" fill="none"><path d="M3 17 Q7 3 10 10 Q13 17 17 17" stroke="#c9a84c" stroke-width="1.5" fill="none" stroke-linecap="round"/><line x1="3" y1="17" x2="17" y2="17" stroke="#c9a84c" stroke-width="1.2" opacity=".4"/></svg>
      </div>
      <div class="kpi-label">Média álcool puro</div>
      <div class="kpi-value" id="kv-media">{{ media }}L</div>
      <div class="kpi-sub">litros per capita / ano</div>
    </div>
  </div>
  <div class="col-6 col-md-3">
    <div class="kpi-card">
      <div class="kpi-icon">
        <svg width="20" height="20" viewBox="0 0 20 20" fill="none"><polygon points="10,2 18,17 2,17" stroke="#c9a84c" stroke-width="1.4" fill="none" stroke-linejoin="round"/><line x1="10" y1="8" x2="10" y2="13" stroke="#c9a84c" stroke-width="1.4" stroke-linecap="round"/><circle cx="10" cy="15.5" r=".8" fill="#c9a84c"/></svg>
      </div>
      <div class="kpi-label">Maior consumidor</div>
      <div class="kpi-value" style="font-size:1.2rem;line-height:1.3" id="kv-top">{{ max_country }}</div>
      <div class="kpi-sub">total de servings combinados</div>
    </div>
  </div>
  <div class="col-6 col-md-3">
    <div class="kpi-card">
      <div class="kpi-icon">
        <svg width="20" height="20" viewBox="0 0 20 20" fill="none"><rect x="3" y="9" width="3" height="8" rx="1" fill="#c9a84c" opacity=".5"/><rect x="8.5" y="5" width="3" height="12" rx="1" fill="#c9a84c" opacity=".7"/><rect x="14" y="2" width="3" height="15" rx="1" fill="#c9a84c"/></svg>
      </div>
      <div class="kpi-label">Máx. servings totais</div>
      <div class="kpi-value" id="kv-max">{{ max_value }}</div>
      <div class="kpi-sub">combinado (cerveja+dest.+vinho)</div>
    </div>
  </div>
</div>

<!-- Charts row 1 -->
<div class="row g-3 mb-3">
  <div class="col-md-6">
    <div class="card">
      <div class="chart-wrap">
        <div class="section-title">
          <svg width="12" height="12" viewBox="0 0 12 12" fill="none"><rect x="1" y="4" width="2.5" height="7" rx=".8" fill="var(--gold-dim)"/><rect x="4.75" y="2" width="2.5" height="9" rx=".8" fill="var(--gold)"/><rect x="8.5" y="0" width="2.5" height="11" rx=".8" fill="var(--gold-light)"/></svg>
          Top 10 — Cerveja (servings)
        </div>
        <div id="chart-beer" style="height:300px"></div>
      </div>
    </div>
  </div>
  <div class="col-md-6">
    <div class="card">
      <div class="chart-wrap">
        <div class="section-title">
          <svg width="12" height="12" viewBox="0 0 12 12" fill="none"><circle cx="6" cy="6" r="4.5" stroke="var(--gold)" stroke-width="1.2"/><path d="M6 3.5v3l1.8 1.1" stroke="var(--gold)" stroke-width="1.2" stroke-linecap="round"/></svg>
          Top 10 — Álcool Puro (litros)
        </div>
        <div id="chart-alcool" style="height:300px"></div>
      </div>
    </div>
  </div>
</div>

<!-- Charts row 2 -->
<div class="row g-3 mb-3">
  <div class="col-md-8">
    <div class="card">
      <div class="chart-wrap">
        <div class="section-title">
          <svg width="12" height="12" viewBox="0 0 12 12" fill="none"><circle cx="3" cy="9" r="1.5" fill="var(--gold-dim)"/><circle cx="7" cy="5" r="1.5" fill="var(--gold)"/><circle cx="10" cy="2.5" r="1.5" fill="var(--gold-light)"/></svg>
          Dispersão — Servings vs Álcool Puro
        </div>
        <div id="chart-scatter" style="height:300px"></div>
      </div>
    </div>
  </div>
  <div class="col-md-4">
    <div class="card h-100">
      <div class="chart-wrap">
        <div class="section-title">
          <svg width="12" height="12" viewBox="0 0 12 12" fill="none"><circle cx="6" cy="6" r="5" stroke="var(--gold)" stroke-width="1.2"/><path d="M6 6 L6 1" stroke="var(--gold)" stroke-width="1.2"/><path d="M6 6 L10 9" stroke="var(--gold-dim)" stroke-width="1.2"/></svg>
          Distribuição — Nível
        </div>
        <div id="chart-donut" style="height:220px"></div>
        <div id="nivel-stats" style="margin-top:12px"></div>
      </div>
    </div>
  </div>
</div>

<script>
const PLOTLY_LAYOUT = {
  paper_bgcolor: 'transparent',
  plot_bgcolor: 'transparent',
  font: { color: '#a07830', size: 11, family: 'Segoe UI, Arial' },
  margin: { t: 8, b: 36, l: 0, r: 8 },
  xaxis: { gridcolor: '#1e1408', zerolinecolor: '#2a1e0e', tickfont: { color: '#a07830' } },
  yaxis: { gridcolor: '#1e1408', zerolinecolor: '#2a1e0e', tickfont: { color: '#a07830' } },
};
const CFG = { responsive: true, displayModeBar: false };

const GOLD_SCALE = [
  [0, '#1a1005'], [0.3, '#4a3010'], [0.6, '#a07830'], [1, '#e0b85a']
];

async function loadAll() {
  const [top10, top10a, paises] = await Promise.all([
    fetch('/api/top10').then(r => r.json()),
    fetch('/api/top10-alcool').then(r => r.json()),
    fetch('/api/paises').then(r => r.json()),
  ]);

  // Beer chart
  Plotly.newPlot('chart-beer', [{
    type: 'bar', orientation: 'h',
    x: top10.map(d => d.Cerveja).reverse(),
    y: top10.map(d => d.Pais).reverse(),
    marker: {
      color: top10.map(d => d.Cerveja).reverse(),
      colorscale: GOLD_SCALE,
      line: { color: 'rgba(201,168,76,.2)', width: 1 }
    },
    hovertemplate: '<b>%{y}</b><br>%{x} servings<extra></extra>',
  }], { ...PLOTLY_LAYOUT, yaxis: { ...PLOTLY_LAYOUT.yaxis, automargin: true } }, CFG);

  // Alcohol chart
  Plotly.newPlot('chart-alcool', [{
    type: 'bar', orientation: 'h',
    x: top10a.map(d => d.LitrosAlcool).reverse(),
    y: top10a.map(d => d.Pais).reverse(),
    marker: {
      color: top10a.map(d => d.LitrosAlcool).reverse(),
      colorscale: [[0,'#120e1a'],[0.4,'#4a3870'],[0.75,'#7b6ab0'],[1,'#b8a8e8']],
      line: { color: 'rgba(184,168,232,.18)', width: 1 }
    },
    hovertemplate: '<b>%{y}</b><br>%{x}L álcool puro<extra></extra>',
  }], { ...PLOTLY_LAYOUT, yaxis: { ...PLOTLY_LAYOUT.yaxis, automargin: true } }, CFG);

  // Scatter
  Plotly.newPlot('chart-scatter', [{
    type: 'scatter', mode: 'markers',
    x: paises.map(d => d.TotalBebidas),
    y: paises.map(d => d.LitrosAlcool),
    text: paises.map(d => d.Pais),
    hovertemplate: '<b>%{text}</b><br>Servings totais: %{x}<br>Álcool puro: %{y}L<extra></extra>',
    marker: {
      color: paises.map(d => d.LitrosAlcool),
      colorscale: GOLD_SCALE,
      size: 8, opacity: .82,
      line: { color: 'rgba(201,168,76,.3)', width: .5 }
    },
  }], {
    ...PLOTLY_LAYOUT,
    margin: { t: 8, b: 40, l: 50, r: 8 },
    xaxis: { ...PLOTLY_LAYOUT.xaxis, title: { text: 'Total Servings', font: { size: 10, color: '#5a4020' } } },
    yaxis: { ...PLOTLY_LAYOUT.yaxis, title: { text: 'Litros Álcool Puro', font: { size: 10, color: '#5a4020' } } },
  }, CFG);

  // Donut
  const alto = paises.filter(d => d.Nivel === 'Alto').length;
  const baixo = paises.length - alto;
  Plotly.newPlot('chart-donut', [{
    type: 'pie',
    labels: ['Nível Alto', 'Nível Baixo'],
    values: [alto, baixo],
    hole: .6,
    marker: { colors: ['#c9a84c', '#2a1e0e'], line: { color: '#0f0a05', width: 2 } },
    textinfo: 'none',
    hovertemplate: '<b>%{label}</b><br>%{value} países (%{percent})<extra></extra>',
  }], {
    ...PLOTLY_LAYOUT,
    margin: { t: 0, b: 0, l: 0, r: 0 },
    showlegend: false,
    annotations: [{
      text: `<b>${alto}</b>`,
      x: .5, y: .55, xref: 'paper', yref: 'paper',
      showarrow: false,
      font: { size: 22, color: '#e0b85a', family: 'Segoe UI' }
    },{
      text: 'alto',
      x: .5, y: .35, xref: 'paper', yref: 'paper',
      showarrow: false,
      font: { size: 10, color: '#a07830', family: 'Segoe UI' }
    }]
  }, CFG);

  document.getElementById('nivel-stats').innerHTML = `
    <div style="display:flex;justify-content:space-between;margin-bottom:8px">
      <span style="font-size:.75rem;color:var(--text-dim)">Nível Alto</span>
      <span style="font-size:.75rem;color:var(--gold-light)">${alto} países</span>
    </div>
    <div class="progress-track mb-2"><div class="progress-bar-custom" style="width:${(alto/paises.length*100).toFixed(1)}%"></div></div>
    <div style="display:flex;justify-content:space-between;margin-bottom:8px">
      <span style="font-size:.75rem;color:var(--text-dim)">Nível Baixo</span>
      <span style="font-size:.75rem;color:var(--text-dim)">${baixo} países</span>
    </div>
    <div class="progress-track"><div style="height:4px;border-radius:2px;background:var(--border);width:${(baixo/paises.length*100).toFixed(1)}%"></div></div>
  `;
}

async function livePoll() {
  try {
    const d = await fetch('/api/dashboard').then(r => r.json());
    document.getElementById('kv-total').textContent = d.total_paises;
    document.getElementById('kv-media').textContent = d.media_alcool + 'L';
    document.getElementById('kv-top').textContent = d.top_country;
    document.getElementById('kv-max').textContent = d.top_value;
    const now = new Date().toLocaleTimeString('pt-BR');
    document.getElementById('live-text').textContent = `Atualizado às ${now} · ${d.nivel_alto} alto · ${d.nivel_baixo} baixo`;
  } catch(e) {}
}

loadAll();
livePoll();
setInterval(livePoll, 6000);
</script>
{% endblock %}


# ===== bebidinhas/templates/insights.html =====
{% extends 'base.html' %}
{% block content %}

<div class="mb-4">
  <h1 style="font-size:1.4rem;font-weight:700;color:var(--gold-light)">Insights Analíticos</h1>
  <p style="font-size:.82rem;color:var(--text-dim);margin-top:2px">Padrões e correlações extraídas automaticamente</p>
</div>

<div class="row g-3 mb-3">
  <!-- Insights list -->
  <div class="col-md-7">
    <div class="card">
      <div class="chart-wrap">
        <div class="section-title">
          <svg width="12" height="12" viewBox="0 0 12 12" fill="none"><path d="M6 1a5 5 0 100 10A5 5 0 006 1zm0 3v3.5" stroke="var(--gold)" stroke-width="1.3" stroke-linecap="round"/><circle cx="6" cy="9" r=".6" fill="var(--gold)"/></svg>
          Destaques automáticos
        </div>
        <div id="insights-list">
          <div style="color:var(--text-dim);font-size:.85rem">Carregando...</div>
        </div>
      </div>
    </div>
  </div>
  <!-- Donut -->
  <div class="col-md-5">
    <div class="card h-100">
      <div class="chart-wrap">
        <div class="section-title">
          <svg width="12" height="12" viewBox="0 0 12 12" fill="none"><circle cx="6" cy="6" r="5" stroke="var(--gold)" stroke-width="1.2"/><path d="M6 6 L6 1" stroke="var(--gold)" stroke-width="1.2"/><path d="M6 6 L10 9" stroke="var(--gold-dim)" stroke-width="1.2"/></svg>
          Distribuição por nível
        </div>
        <div id="chart-nivel" style="height:220px"></div>
      </div>
    </div>
  </div>
</div>

<div class="row g-3">
  <!-- Correlation -->
  <div class="col-md-6">
    <div class="card">
      <div class="chart-wrap">
        <div class="section-title">
          <svg width="12" height="12" viewBox="0 0 12 12" fill="none"><circle cx="2.5" cy="9" r="1.5" fill="var(--gold-dim)"/><circle cx="6" cy="5.5" r="1.5" fill="var(--gold)"/><circle cx="9.5" cy="2.5" r="1.5" fill="var(--gold-light)"/><line x1="2" y1="9" x2="10" y2="2" stroke="var(--gold)" stroke-width=".8" stroke-dasharray="1.5 1.5" opacity=".5"/></svg>
          Cerveja vs Álcool — Correlação
        </div>
        <div id="chart-corr" style="height:280px"></div>
      </div>
    </div>
  </div>
  <!-- Composition -->
  <div class="col-md-6">
    <div class="card">
      <div class="chart-wrap">
        <div class="section-title">
          <svg width="12" height="12" viewBox="0 0 12 12" fill="none"><rect x="1" y="4" width="2.5" height="7" rx=".8" fill="#c9a84c" opacity=".5"/><rect x="4.75" y="2" width="2.5" height="9" rx=".8" fill="#c9a84c" opacity=".7"/><rect x="8.5" y="0" width="2.5" height="11" rx=".8" fill="#c9a84c"/></svg>
          Composição média global
        </div>
        <div id="chart-comp" style="height:280px"></div>
      </div>
    </div>
  </div>
</div>

<script>
const PLOTLY_LAYOUT = {
  paper_bgcolor: 'transparent', plot_bgcolor: 'transparent',
  font: { color: '#a07830', size: 11, family: 'Segoe UI, Arial' },
  margin: { t: 8, b: 40, l: 50, r: 8 },
  xaxis: { gridcolor: '#1e1408', zerolinecolor: '#2a1e0e', tickfont: { color: '#a07830' } },
  yaxis: { gridcolor: '#1e1408', zerolinecolor: '#2a1e0e', tickfont: { color: '#a07830' } },
};
const CFG = { responsive: true, displayModeBar: false };

async function load() {
  const [ins, paises, dash] = await Promise.all([
    fetch('/api/insights').then(r => r.json()),
    fetch('/api/paises').then(r => r.json()),
    fetch('/api/dashboard').then(r => r.json()),
  ]);

  // Insights list
  const icons = ['📊','🏆','🔗','🚫','⭐'];
  document.getElementById('insights-list').innerHTML = ins.insights.map((txt, i) => `
    <div class="insight-item" style="animation-delay:${i*80}ms">
      <span class="insight-num">${i+1}</span>
      <span style="font-size:.87rem;color:var(--text);line-height:1.5">${txt}</span>
    </div>
  `).join('');

  // Donut
  Plotly.newPlot('chart-nivel', [{
    type: 'pie',
    labels: ['Nível Alto', 'Nível Baixo'],
    values: [dash.nivel_alto, dash.nivel_baixo],
    hole: .55,
    marker: { colors: ['#c9a84c', '#2a1e0e'], line: { color: '#0f0a05', width: 2 } },
    textinfo: 'label+percent',
    textfont: { size: 11, color: '#c9a84c' },
    hovertemplate: '<b>%{label}</b><br>%{value} países<extra></extra>',
  }], { ...PLOTLY_LAYOUT, margin: { t: 8, b: 8, l: 8, r: 8 }, showlegend: false }, CFG);

  // Correlation scatter
  Plotly.newPlot('chart-corr', [{
    type: 'scatter', mode: 'markers',
    x: paises.map(d => d.Cerveja),
    y: paises.map(d => d.LitrosAlcool),
    text: paises.map(d => d.Pais),
    hovertemplate: '<b>%{text}</b><br>Cerveja: %{x}<br>Álcool: %{y}L<extra></extra>',
    marker: {
      color: paises.map(d => d.LitrosAlcool),
      colorscale: [[0,'#1a1005'],[0.5,'#a07830'],[1,'#e0b85a']],
      size: 7, opacity: .8,
      line: { color: 'rgba(201,168,76,.25)', width: .5 }
    },
  }], {
    ...PLOTLY_LAYOUT,
    xaxis: { ...PLOTLY_LAYOUT.xaxis, title: { text: 'Servings de Cerveja', font: { size: 10, color: '#5a4020' } } },
    yaxis: { ...PLOTLY_LAYOUT.yaxis, title: { text: 'Litros de Álcool Puro', font: { size: 10, color: '#5a4020' } } },
  }, CFG);

  // Composition bar
  const avg = k => paises.reduce((s, d) => s + d[k], 0) / paises.length;
  const cats = ['Cerveja', 'Destilados', 'Vinho'];
  const vals = cats.map(k => +avg(k).toFixed(1));
  Plotly.newPlot('chart-comp', [{
    type: 'bar',
    x: cats,
    y: vals,
    marker: {
      color: ['#d4a843', '#c46e4a', '#7b6ab0'],
      opacity: .88,
      line: { color: ['rgba(212,168,67,.25)','rgba(196,110,74,.25)','rgba(123,106,176,.25)'], width: 1 }
    },
    text: vals.map(v => v.toFixed(1)),
    textposition: 'outside',
    textfont: { color: '#a07830', size: 11 },
    hovertemplate: '<b>%{x}</b><br>Média: %{y} servings<extra></extra>',
  }], {
    ...PLOTLY_LAYOUT,
    yaxis: { ...PLOTLY_LAYOUT.yaxis, title: { text: 'Média de Servings', font: { size: 10, color: '#5a4020' } } },
  }, CFG);
}

load();
</script>
{% endblock %}


# ===== bebidinhas/templates/paises.html =====
{% extends 'base.html' %}
{% block content %}

<div class="d-flex align-items-center justify-content-between mb-4">
  <div>
    <h1 style="font-size:1.4rem;font-weight:700;color:var(--gold-light)">Todos os Países</h1>
    <p style="font-size:.82rem;color:var(--text-dim);margin-top:2px">Dados completos de consumo por categoria</p>
  </div>
  <span id="count-badge" style="font-size:.75rem;color:var(--text-dim);background:var(--surface);border:1px solid var(--border);padding:5px 12px;border-radius:20px"></span>
</div>

<div class="card mb-3">
  <div class="card-body" style="padding:14px 16px">
    <div class="search-wrap">
      <svg class="search-icon" width="14" height="14" viewBox="0 0 14 14" fill="none">
        <circle cx="6" cy="6" r="4.5" stroke="#5a4020" stroke-width="1.3"/>
        <line x1="9.5" y1="9.5" x2="12.5" y2="12.5" stroke="#5a4020" stroke-width="1.3" stroke-linecap="round"/>
      </svg>
      <input type="text" id="search" class="search-input" placeholder="Buscar país...">
    </div>
  </div>
</div>

<div class="card" style="overflow-x:auto">
  <table class="data-table">
    <thead>
      <tr>
        <th onclick="sortBy('Pais')">
          <span style="display:inline-flex;align-items:center;gap:5px">
            <svg width="10" height="10" viewBox="0 0 10 10" fill="none"><circle cx="5" cy="5" r="4" stroke="currentColor" stroke-width="1"/></svg>
            País <span id="sort-Pais"></span>
          </span>
        </th>
        <th onclick="sortBy('Cerveja')" style="text-align:right">
          <span style="display:inline-flex;align-items:center;gap:5px">
            <svg width="10" height="10" viewBox="0 0 10 10" fill="none"><rect x="2" y="2" width="6" height="7" rx="1" stroke="currentColor" stroke-width="1"/><path d="M8 4h1.5" stroke="currentColor" stroke-width="1" stroke-linecap="round"/></svg>
            Cerveja <span id="sort-Cerveja"></span>
          </span>
        </th>
        <th onclick="sortBy('Destilados')" style="text-align:right">
          <span style="display:inline-flex;align-items:center;gap:5px">
            <svg width="10" height="10" viewBox="0 0 10 10" fill="none"><path d="M4 1h2v3l2 3H2L4 4V1z" stroke="currentColor" stroke-width="1" fill="none"/></svg>
            Destilados <span id="sort-Destilados"></span>
          </span>
        </th>
        <th onclick="sortBy('Vinho')" style="text-align:right">
          <span style="display:inline-flex;align-items:center;gap:5px">
            <svg width="10" height="10" viewBox="0 0 10 10" fill="none"><path d="M3 1h4v4a2 2 0 01-4 0V1z" stroke="currentColor" stroke-width="1" fill="none"/><line x1="5" y1="7" x2="5" y2="9.5" stroke="currentColor" stroke-width="1" stroke-linecap="round"/></svg>
            Vinho <span id="sort-Vinho"></span>
          </span>
        </th>
        <th onclick="sortBy('LitrosAlcool')" style="text-align:right">
          <span style="display:inline-flex;align-items:center;gap:5px">
            <svg width="10" height="10" viewBox="0 0 10 10" fill="none"><path d="M5 1C5 1 2 4 2 6.5a3 3 0 006 0C8 4 5 1 5 1z" stroke="currentColor" stroke-width="1" fill="none"/></svg>
            Álcool (L) <span id="sort-LitrosAlcool"></span>
          </span>
        </th>
        <th onclick="sortBy('TotalBebidas')" style="text-align:right">
          <span style="display:inline-flex;align-items:center;gap:5px">
            <svg width="10" height="10" viewBox="0 0 10 10" fill="none"><rect x="1.5" y="5" width="2" height="4" rx=".5" fill="currentColor" opacity=".5"/><rect x="4" y="3" width="2" height="6" rx=".5" fill="currentColor" opacity=".7"/><rect x="6.5" y="1" width="2" height="8" rx=".5" fill="currentColor"/></svg>
            Total <span id="sort-TotalBebidas"></span>
          </span>
        </th>
        <th>Nível</th>
      </tr>
    </thead>
    <tbody id="tbody"></tbody>
  </table>
</div>

<script>
let data = [], sortKey = 'TotalBebidas', sortAsc = false;

async function load() {
  data = await fetch('/api/paises').then(r => r.json());
  render();
}

function bar(val, max, color='#c9a84c') {
  const pct = Math.round(val / max * 100);
  return `<div style="display:flex;align-items:center;gap:8px;justify-content:flex-end">
    <span>${val}</span>
    <div style="width:50px;height:3px;background:var(--surface2);border-radius:1.5px;overflow:hidden">
      <div style="width:${pct}%;height:100%;background:${color};border-radius:1.5px"></div>
    </div>
  </div>`;
}

function render() {
  const q = document.getElementById('search').value.toLowerCase();
  let rows = data.filter(d => d.Pais.toLowerCase().includes(q));
  if (sortKey) {
    rows.sort((a, b) => {
      const av = a[sortKey], bv = b[sortKey];
      if (typeof av === 'string') return sortAsc ? av.localeCompare(bv) : bv.localeCompare(av);
      return sortAsc ? av - bv : bv - av;
    });
  }

  const maxC = Math.max(...data.map(d => d.Cerveja));
  const maxD = Math.max(...data.map(d => d.Destilados));
  const maxV = Math.max(...data.map(d => d.Vinho));
  const maxA = Math.max(...data.map(d => d.LitrosAlcool));
  const maxT = Math.max(...data.map(d => d.TotalBebidas));

  document.getElementById('tbody').innerHTML = rows.map(d => `
    <tr>
      <td style="font-weight:500;color:var(--gold-light)">${d.Pais}</td>
      <td style="text-align:right;font-size:.82rem">${bar(d.Cerveja, maxC, '#d4a843')}</td>
      <td style="text-align:right;font-size:.82rem">${bar(d.Destilados, maxD, '#c46e4a')}</td>
      <td style="text-align:right;font-size:.82rem">${bar(d.Vinho, maxV, '#7b6ab0')}</td>
      <td style="text-align:right;font-size:.82rem">${bar(d.LitrosAlcool, maxA, '#4a9e8e')}</td>
      <td style="text-align:right;font-size:.82rem;color:var(--text)">${bar(d.TotalBebidas, maxT, '#a07830')}</td>
      <td><span class="badge-${d.Nivel.toLowerCase()}">${d.Nivel}</span></td>
    </tr>
  `).join('');

  const sortIds = ['Pais','Cerveja','Destilados','Vinho','LitrosAlcool','TotalBebidas'];
  sortIds.forEach(k => {
    const el = document.getElementById(`sort-${k}`);
    if (el) el.textContent = sortKey === k ? (sortAsc ? '↑' : '↓') : '';
  });

  document.getElementById('count-badge').textContent = `${rows.length} de ${data.length} países`;
}

function sortBy(key) {
  if (sortKey === key) sortAsc = !sortAsc;
  else { sortKey = key; sortAsc = false; }
  render();
}

document.getElementById('search').addEventListener('input', render);
load();
</script>
{% endblock %}


# ===== bebidinhas/templates/comparar.html =====
{% extends 'base.html' %}
{% block content %}

<div class="mb-4">
  <h1 style="font-size:1.4rem;font-weight:700;color:var(--gold-light)">Comparar Países</h1>
  <p style="font-size:.82rem;color:var(--text-dim);margin-top:2px">Selecione 2 a 5 países para comparação lado a lado</p>
</div>

<div class="row g-3 mb-3">
  <!-- Selector -->
  <div class="col-md-4">
    <div class="card h-100">
      <div class="chart-wrap">
        <div class="section-title">
          <svg width="12" height="12" viewBox="0 0 12 12" fill="none"><circle cx="6" cy="4" r="2.5" stroke="var(--gold)" stroke-width="1.2"/><path d="M2 11c0-2.2 1.8-4 4-4s4 1.8 4 4" stroke="var(--gold)" stroke-width="1.2" stroke-linecap="round" fill="none"/></svg>
          Selecionar países
        </div>

        <div class="search-wrap mb-3">
          <svg class="search-icon" width="13" height="13" viewBox="0 0 14 14" fill="none">
            <circle cx="6" cy="6" r="4.5" stroke="#5a4020" stroke-width="1.3"/>
            <line x1="9.5" y1="9.5" x2="12.5" y2="12.5" stroke="#5a4020" stroke-width="1.3" stroke-linecap="round"/>
          </svg>
          <input id="country-search" class="search-input" placeholder="Buscar país..." style="padding-left:38px;font-size:.83rem">
        </div>

        <div id="country-list" style="max-height:320px;overflow-y:auto;display:flex;flex-direction:column;gap:2px"></div>

        <div style="margin-top:16px;padding-top:12px;border-top:1px solid var(--border)">
          <div class="section-title" style="margin-bottom:10px">
            <svg width="12" height="12" viewBox="0 0 12 12" fill="none"><rect x="1" y="5" width="10" height="1.5" rx=".75" fill="var(--gold-dim)"/><rect x="4" y="2" width="1.5" height="8" rx=".75" fill="var(--gold-dim)"/></svg>
            Selecionados
          </div>
          <div id="selected-tags" style="min-height:32px"></div>
          <div id="select-hint" style="font-size:.75rem;color:var(--text-dim);margin-top:8px">Selecione entre 2 e 5 países</div>
        </div>
      </div>
    </div>
  </div>

  <!-- Radar + Bar -->
  <div class="col-md-8">
    <div class="card mb-3">
      <div class="chart-wrap">
        <div class="section-title">
          <svg width="12" height="12" viewBox="0 0 12 12" fill="none"><polygon points="6,1 11,4 11,8 6,11 1,8 1,4" stroke="var(--gold)" stroke-width="1.1" fill="none"/></svg>
          Radar — Perfil de consumo
        </div>
        <div id="chart-radar" style="height:340px;display:flex;align-items:center;justify-content:center">
          <span style="color:var(--text-dim);font-size:.85rem">Selecione países para visualizar</span>
        </div>
      </div>
    </div>
    <div class="card">
      <div class="chart-wrap">
        <div class="section-title">
          <svg width="12" height="12" viewBox="0 0 12 12" fill="none"><rect x="1" y="4" width="2.5" height="7" rx=".8" fill="var(--gold-dim)"/><rect x="4.75" y="2" width="2.5" height="9" rx=".8" fill="var(--gold)"/><rect x="8.5" y="0" width="2.5" height="11" rx=".8" fill="var(--gold-light)"/></svg>
          Comparativo — Álcool puro & Total servings
        </div>
        <div id="chart-bar" style="height:220px;display:flex;align-items:center;justify-content:center">
          <span style="color:var(--text-dim);font-size:.85rem">Selecione países para visualizar</span>
        </div>
      </div>
    </div>
  </div>
</div>

<!-- Stats table -->
<div class="card" id="stats-table-wrap" style="display:none">
  <div class="chart-wrap">
    <div class="section-title">
      <svg width="12" height="12" viewBox="0 0 12 12" fill="none"><rect x="1" y="2" width="10" height="1.3" rx=".65" fill="var(--gold-dim)"/><rect x="1" y="5.4" width="10" height="1.3" rx=".65" fill="var(--gold-dim)"/><rect x="1" y="8.8" width="7" height="1.3" rx=".65" fill="var(--gold-dim)"/></svg>
      Dados tabulares
    </div>
    <div style="overflow-x:auto">
      <table class="data-table" id="stats-table">
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

<script>
const PALETTE = ['#c9a84c','#e07840','#6090d0','#80c060','#c060a0'];
const CFG = { responsive: true, displayModeBar: false };
const BASE_LAYOUT = {
  paper_bgcolor: 'transparent', plot_bgcolor: 'transparent',
  font: { color: '#a07830', size: 11, family: 'Segoe UI, Arial' },
  legend: { bgcolor: 'transparent', font: { color: '#c9a84c', size: 11 } },
};

let allData = [], selected = [];

async function init() {
  allData = await fetch('/api/paises').then(r => r.json());
  renderList('');
}

function renderList(q) {
  const filtered = allData.filter(d => d.Pais.toLowerCase().includes(q.toLowerCase()));
  document.getElementById('country-list').innerHTML = filtered.slice(0, 80).map(d => {
    const isSel = selected.includes(d.Pais);
    return `<div onclick="toggleCountry('${d.Pais.replace(/'/g,"\\'")}',this)"
      style="
        display:flex;align-items:center;justify-content:space-between;
        padding:7px 10px;border-radius:7px;cursor:pointer;font-size:.83rem;
        background:${isSel ? 'rgba(201,168,76,.12)' : 'transparent'};
        color:${isSel ? 'var(--gold-light)' : 'var(--text-dim)'};
        border:1px solid ${isSel ? 'rgba(201,168,76,.25)' : 'transparent'};
        transition:background .15s,color .15s,border-color .15s;
      "
      data-pais="${d.Pais}">
      <span>${d.Pais}</span>
      ${isSel ? `<svg width="12" height="12" viewBox="0 0 12 12" fill="none"><path d="M2 6l3 3 5-5" stroke="#c9a84c" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>` : ''}
    </div>`;
  }).join('');
}

function toggleCountry(pais) {
  const idx = selected.indexOf(pais);
  if (idx >= 0) {
    selected.splice(idx, 1);
  } else {
    if (selected.length >= 5) {
      selected.shift();
    }
    selected.push(pais);
  }
  renderList(document.getElementById('country-search').value);
  renderTags();
  updateCharts();
}

function renderTags() {
  document.getElementById('selected-tags').innerHTML = selected.map((p, i) => `
    <span class="country-tag" onclick="toggleCountry('${p.replace(/'/g,"\\'")}')"
      style="border-color:${PALETTE[i]}40;background:${PALETTE[i]}18;color:${PALETTE[i]}">
      ${p}
      <svg width="10" height="10" viewBox="0 0 10 10" fill="none" class="remove">
        <path d="M2 2l6 6M8 2l-6 6" stroke="${PALETTE[i]}" stroke-width="1.3" stroke-linecap="round"/>
      </svg>
    </span>
  `).join('');

  const hint = document.getElementById('select-hint');
  if (selected.length < 2) hint.textContent = `Selecione ${2 - selected.length} mais país${selected.length === 1 ? '' : 'es'}`;
  else if (selected.length >= 5) hint.textContent = 'Máximo de 5 países atingido';
  else hint.textContent = `${selected.length} países selecionados`;
}

function updateCharts() {
  if (selected.length < 2) {
    document.getElementById('chart-radar').innerHTML = '<span style="color:var(--text-dim);font-size:.85rem">Selecione pelo menos 2 países</span>';
    document.getElementById('chart-bar').innerHTML = '<span style="color:var(--text-dim);font-size:.85rem">Selecione pelo menos 2 países</span>';
    document.getElementById('stats-table-wrap').style.display = 'none';
    return;
  }

  const rows = selected.map(p => allData.find(d => d.Pais === p)).filter(Boolean);

  // Radar
  const cats = ['Cerveja', 'Destilados', 'Vinho', 'LitrosAlcool', 'TotalBebidas'];
  const catLabels = ['Cerveja', 'Destilados', 'Vinho', 'Álcool (L)', 'Total'];
  const maxes = cats.map(k => Math.max(...allData.map(d => d[k])));

  const radarTraces = rows.map((r, i) => ({
    type: 'scatterpolar',
    r: cats.map((k, ki) => r[k] / maxes[ki] * 100).concat([cats.map((k, ki) => r[k] / maxes[ki] * 100)[0]]),
    theta: catLabels.concat([catLabels[0]]),
    name: r.Pais,
    fill: 'toself',
    fillcolor: PALETTE[i] + '22',
    line: { color: PALETTE[i], width: 2 },
    hovertemplate: `<b>${r.Pais}</b><br>%{theta}: %{r:.1f}%<extra></extra>`,
  }));

  Plotly.newPlot('chart-radar', radarTraces, {
    ...BASE_LAYOUT,
    polar: {
      bgcolor: 'transparent',
      angularaxis: { color: '#3a2a10', gridcolor: '#2a1e0e', linecolor: '#2a1e0e', tickfont: { color: '#a07830', size: 10 } },
      radialaxis: { color: '#2a1e0e', gridcolor: '#2a1e0e', tickfont: { color: '#5a4020', size: 8 }, range: [0, 100], showticklabels: false },
    },
    margin: { t: 20, b: 20, l: 40, r: 40 },
    showlegend: true,
    legend: { ...BASE_LAYOUT.legend, orientation: 'h', y: -0.05 },
  }, CFG);

  // Bar comparison
  const barTraces = [
    {
      type: 'bar', name: 'Álcool puro (L)',
      x: rows.map(r => r.Pais),
      y: rows.map(r => r.LitrosAlcool),
      marker: { color: rows.map((_, i) => PALETTE[i]), opacity: .85 },
      hovertemplate: '<b>%{x}</b><br>Álcool: %{y}L<extra></extra>',
      yaxis: 'y',
    },
    {
      type: 'scatter', mode: 'markers+lines', name: 'Total servings',
      x: rows.map(r => r.Pais),
      y: rows.map(r => r.TotalBebidas),
      marker: { color: rows.map((_, i) => PALETTE[i]), size: 10, symbol: 'diamond', line: { color: '#0f0a05', width: 1 } },
      line: { color: '#a07830', width: 1, dash: 'dot' },
      hovertemplate: '<b>%{x}</b><br>Total: %{y} servings<extra></extra>',
      yaxis: 'y2',
    }
  ];

  Plotly.newPlot('chart-bar', barTraces, {
    ...BASE_LAYOUT,
    margin: { t: 8, b: 50, l: 50, r: 60 },
    xaxis: { gridcolor: '#1e1408', zerolinecolor: '#2a1e0e', tickfont: { color: '#a07830' } },
    yaxis: { gridcolor: '#1e1408', zerolinecolor: '#2a1e0e', tickfont: { color: '#a07830' }, title: { text: 'Álcool (L)', font: { size: 9, color: '#5a4020' } } },
    yaxis2: { overlaying: 'y', side: 'right', gridcolor: 'transparent', tickfont: { color: '#8a6050', size: 9 }, title: { text: 'Total servings', font: { size: 9, color: '#5a4020' } } },
    showlegend: true,
    legend: { ...BASE_LAYOUT.legend, x: 0, y: 1.05, orientation: 'h' },
    barmode: 'group',
  }, CFG);

  // Stats table
  document.getElementById('stats-table-wrap').style.display = '';
  document.getElementById('stats-tbody').innerHTML = rows.map((r, i) => `
    <tr>
      <td style="font-weight:500;color:${PALETTE[i]}">${r.Pais}</td>
      <td style="text-align:right">${r.Cerveja}</td>
      <td style="text-align:right">${r.Destilados}</td>
      <td style="text-align:right">${r.Vinho}</td>
      <td style="text-align:right;color:var(--gold-light)">${r.TotalBebidas}</td>
      <td style="text-align:right">${r.LitrosAlcool}</td>
      <td><span class="badge-${r.Nivel.toLowerCase()}">${r.Nivel}</span></td>
    </tr>
  `).join('');
}

document.getElementById('country-search').addEventListener('input', e => renderList(e.target.value));
init();
</script>
{% endblock %}
