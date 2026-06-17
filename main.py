from flask import Flask, request, jsonify, render_template_string
import pandas as pd
import sqlite3
import os
import plotly.graph_objs as go
from dash import Dash, html, dcc
import numpy as np
import config
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


#      ___                       ___                 
#     /\__\          ___        /\__\          ___   
#    /:/  /         /\  \      /::|  |        /\  \  
#   /:/  /          \:\  \    /:|:|  |        \:\  \ 
#  /:/__/  ___      /::\__\  /:/|:|  |__      /::\__\
#  |:|  | /\__\  __/:/\/__/ /:/ |:| /\__\  __/:/\/__/
#  |:|  |/:/  / /\/:/  /    \/__|:|/:/  / /\/:/  /   
#  |:|__/:/  /  \::/__/         |:/:/  /  \::/__/    
#   \::::/__/    \:\__\         |::/  /    \:\__\    
#    ~~~~         \/__/         /:/  /      \/__/    
#                               \/__/                
#
#
# AUTOR: Vinicius Soares Brandão
# VERSÃO: 0.0.1 [Beta]
# LICENÇA: Creative Commons

app = Flask(__name__)
DB_PATH = config.DB_PATH

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS inadimplencia (
                mes TEXT PRIMARY KEY,
                inadimplencia REAL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS selic (
                mes TEXT PRIMARY KEY,
                selic REAL
            )
        ''')
        conn.commit()

vazio = 0

BASE_STYLE = """
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:ital,wght@0,100..800;1,100..800&family=Playfair+Display:ital,wght@0,400..900;1,400..900&display=swap" rel="stylesheet">
<style>
  :root {
    --gold:  #c9a84c;
    --gold2: #a8864a;
    --gold3: #7a6535;
    --gold4: #4a3c20;
    --gold5: #2a2010;
    --bg:    #000000;
    --text:  #e8d9b0;
    --muted: #8a7a55;
    --border: rgba(120,90,40,.22);
    --border-hover: rgba(180,140,60,.4);
  }
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

  body {
    background: var(--bg);
    color: var(--text);
    font-family: 'JetBrains Mono', monospace;
    min-height: 100vh;
    overflow-x: hidden;
    position: relative;
  }

  /* ── Code Rain ── */
  #rain-canvas {
    position: fixed;
    top: 0; left: 0;
    width: 100%; height: 100%;
    pointer-events: none;
    z-index: 0;
    opacity: .13;
  }

  /* ── Glow orbs ── */
  .glow {
    position: fixed;
    width: 600px; height: 600px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(201,168,76,.18) 0%, transparent 70%);
    pointer-events: none;
    z-index: 0;
    top: -180px; left: -180px;
    animation: float 8s ease-in-out infinite;
  }
  .glow2 {
    position: fixed;
    width: 500px; height: 500px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(168,134,74,.13) 0%, transparent 70%);
    pointer-events: none;
    z-index: 0;
    bottom: -150px; right: -150px;
    animation: float2 10s ease-in-out infinite;
  }
  @keyframes float  { 0%,100%{transform:translateY(0) scale(1)} 50%{transform:translateY(30px) scale(1.05)} }
  @keyframes float2 { 0%,100%{transform:translateY(0) scale(1)} 50%{transform:translateY(-25px) scale(1.04)} }

  /* ── Layout ── */
  .page-wrap {
    position: relative;
    z-index: 1;
    max-width: 960px;
    margin: 0 auto;
    padding: 48px 24px 80px;
  }

  /* ── Header / Brand ── */
  .vsb-header {
    display: flex;
    align-items: center;
    gap: 16px;
    margin-bottom: 48px;
    animation: fadeInDown .6s ease both;
  }
  .vsb-logo {
    width: 48px; height: 48px;
    border: 1.5px solid var(--gold3);
    border-radius: 4px;
    display: flex; align-items: center; justify-content: center;
    font-family: 'Playfair Display', serif;
    font-size: 18px;
    color: var(--gold);
    letter-spacing: 1px;
    flex-shrink: 0;
    animation: logo-pulse 3.5s ease-in-out infinite;
  }
  .vsb-title-block { display: flex; flex-direction: column; gap: 2px; }
  .vsb-title {
    font-family: 'Playfair Display', serif;
    font-size: clamp(20px, 4vw, 28px);
    color: var(--gold);
    letter-spacing: .5px;
  }
  .vsb-subtitle {
    font-size: 11px;
    color: var(--muted);
    letter-spacing: 2px;
    text-transform: uppercase;
  }

  /* ── Section headings ── */
  .section-tag {
    font-size: 10px;
    color: var(--gold3);
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-bottom: 8px;
    animation: fadeIn .5s ease both;
  }
  .section-tag::after {
    content: '|';
    margin-left: 3px;
    animation: blink 1.1s step-end infinite;
    color: var(--gold3);
  }
  h1.page-heading {
    font-family: 'Playfair Display', serif;
    font-size: clamp(22px, 5vw, 36px);
    margin-bottom: 32px;
    line-height: 1.2;
    animation: fadeIn .6s ease both;
    background: linear-gradient(120deg, #c9a84c 0%, #f0dfa0 38%, #c9a84c 55%, #a8864a 80%, #c9a84c 100%);
    background-size: 250% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: fadeIn .6s ease both, gold-shine 5s linear infinite;
  }
  h2.sub-heading {
    font-size: 13px;
    color: var(--gold2);
    letter-spacing: 1px;
    margin-bottom: 16px;
    text-transform: uppercase;
  }

  /* ── Cards / Panels ── */
  .card {
    background: rgba(10,8,4,.7);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 28px 32px;
    margin-bottom: 20px;
    transition: border-color .3s, box-shadow .3s;
    animation: fadeIn .7s ease both;
    backdrop-filter: blur(4px);
  }
  .card:hover { border-color: var(--border-hover); box-shadow: 0 0 24px rgba(201,168,76,.06); }

  .nav-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
    gap: 14px;
    margin-top: 8px;
  }
  .nav-card {
    background: rgba(10,8,4,.7);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 20px 22px;
    text-decoration: none;
    display: flex;
    align-items: center;
    gap: 14px;
    transition: border-color .3s, box-shadow .3s, transform .2s;
    animation: fadeIn .8s ease both;
    backdrop-filter: blur(4px);
    cursor: pointer;
    position: relative;
    overflow: hidden;
  }
  .nav-card::before {
    content: '';
    position: absolute;
    top: 0; left: -75%;
    width: 50%; height: 100%;
    background: linear-gradient(90deg, transparent, rgba(201,168,76,.07), transparent);
    transform: skewX(-12deg);
    pointer-events: none;
  }
  .nav-card:hover::before { animation: shimmer .55s ease forwards; }
  .nav-card:hover {
    border-color: var(--border-hover);
    box-shadow: 0 0 22px rgba(201,168,76,.1), inset 0 0 20px rgba(201,168,76,.03);
    transform: translateY(-2px);
  }
  .nav-card:nth-child(1){animation-delay:.04s}
  .nav-card:nth-child(2){animation-delay:.09s}
  .nav-card:nth-child(3){animation-delay:.14s}
  .nav-card:nth-child(4){animation-delay:.19s}
  .nav-card:nth-child(5){animation-delay:.24s}
  .nav-card:nth-child(6){animation-delay:.29s}
  .nav-card-icon {
    width: 36px; height: 36px;
    border: 1px solid var(--gold4);
    border-radius: 4px;
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0;
    transition: border-color .3s, box-shadow .3s;
  }
  .nav-card:hover .nav-card-icon {
    border-color: var(--gold3);
    box-shadow: 0 0 8px rgba(201,168,76,.15);
  }
  .nav-card-icon svg { width: 18px; height: 18px; stroke: var(--gold); fill: none; stroke-width: 1.5; stroke-linecap: round; stroke-linejoin: round; }
  .nav-card-text { display: flex; flex-direction: column; gap: 2px; }
  .nav-card-label { font-size: 13px; color: var(--gold); letter-spacing: .4px; }
  .nav-card-desc  { font-size: 10px; color: var(--muted); letter-spacing: .5px; }

  /* ── Forms ── */
  .vsb-form { display: flex; flex-direction: column; gap: 18px; }
  .form-group { display: flex; flex-direction: column; gap: 6px; }
  .form-label {
    font-size: 10px;
    color: var(--gold3);
    letter-spacing: 2px;
    text-transform: uppercase;
  }
  .form-input, .form-select {
    background: rgba(20,15,5,.8);
    border: 1px solid var(--border);
    border-radius: 4px;
    color: var(--text);
    font-family: 'JetBrains Mono', monospace;
    font-size: 13px;
    padding: 10px 14px;
    outline: none;
    transition: border-color .25s, box-shadow .25s;
    width: 100%;
  }
  .form-input:focus, .form-select:focus {
    border-color: var(--gold3);
    box-shadow: 0 0 0 2px rgba(122,101,53,.18);
  }
  .form-select option { background: #0a0800; }
  input[type="file"].form-input { padding: 8px 14px; cursor: pointer; }
  input[type="file"].form-input::-webkit-file-upload-button {
    background: transparent;
    border: 1px solid var(--gold4);
    color: var(--gold2);
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    padding: 4px 10px;
    border-radius: 3px;
    cursor: pointer;
    margin-right: 10px;
    transition: border-color .2s;
  }
  input[type="file"].form-input::-webkit-file-upload-button:hover { border-color: var(--gold); color: var(--gold); }

  /* ── Buttons ── */
  .vsb-btn {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: transparent;
    border: 1px solid var(--gold3);
    color: var(--gold);
    font-family: 'JetBrains Mono', monospace;
    font-size: 12px;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    padding: 11px 24px;
    border-radius: 4px;
    cursor: pointer;
    transition: border-color .25s, background .25s, box-shadow .25s, color .25s;
    text-decoration: none;
    align-self: flex-start;
  }
  .vsb-btn:hover {
    border-color: var(--gold);
    background: rgba(201,168,76,.06);
    box-shadow: 0 0 16px rgba(201,168,76,.12);
    color: var(--gold);
  }
  .vsb-btn svg { width: 14px; height: 14px; stroke: currentColor; fill: none; stroke-width: 1.5; stroke-linecap: round; stroke-linejoin: round; }

  /* ── Back link ── */
  .back-link {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    font-size: 11px;
    color: var(--muted);
    text-decoration: none;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-top: 32px;
    transition: color .2s;
  }
  .back-link:hover { color: var(--gold); }
  .back-link svg { width: 13px; height: 13px; stroke: currentColor; fill: none; stroke-width: 1.5; stroke-linecap: round; stroke-linejoin: round; }

  /* ── Divider ── */
  .vsb-divider {
    border: none;
    border-top: 1px solid var(--border);
    margin: 32px 0;
  }

  /* ── Data table ── */
  .data-table-wrap { overflow-x: auto; border-radius: 6px; border: 1px solid var(--border); }
  table { width: 100%; border-collapse: collapse; font-size: 12px; }
  thead tr { background: rgba(74,60,32,.25); }
  thead th { padding: 10px 14px; text-align: left; color: var(--gold2); letter-spacing: 1px; font-size: 10px; text-transform: uppercase; border-bottom: 1px solid var(--border); }
  tbody tr { border-bottom: 1px solid rgba(120,90,40,.1); transition: background .2s; }
  tbody tr:last-child { border-bottom: none; }
  tbody tr:hover { background: rgba(201,168,76,.04); }
  tbody td { padding: 9px 14px; color: var(--text); }

  /* ── Graph container ── */
  .graph-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
  @media(max-width:680px){ .graph-grid{ grid-template-columns: 1fr; } }
  .graph-panel {
    background: rgba(10,8,4,.7);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 4px;
    overflow: hidden;
  }

  /* ── Footer ── */
  .vsb-footer {
    position: fixed;
    bottom: 0; left: 0; right: 0;
    border-top: 1px solid var(--border);
    background: rgba(0,0,0,.85);
    backdrop-filter: blur(6px);
    padding: 10px 24px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    z-index: 10;
  }
  .vsb-footer-left { font-size: 10px; color: var(--gold3); letter-spacing: 2px; text-transform: uppercase; }
  .vsb-footer-right { font-size: 10px; color: var(--muted); letter-spacing: 1.5px; }

  /* ── Animations ── */
  @keyframes fadeIn     { from{opacity:0;transform:translateY(12px)} to{opacity:1;transform:translateY(0)} }
  @keyframes fadeInDown { from{opacity:0;transform:translateY(-10px)} to{opacity:1;transform:translateY(0)} }
  @keyframes blink      { 0%,100%{opacity:1} 50%{opacity:0} }
  @keyframes shimmer    { 0%{left:-75%} 100%{left:125%} }
  @keyframes logo-pulse { 0%,100%{box-shadow:0 0 0 rgba(201,168,76,0);border-color:var(--gold3)} 50%{box-shadow:0 0 14px rgba(201,168,76,.22);border-color:var(--gold2)} }
  @keyframes gold-shine { 0%{background-position:200% center} 100%{background-position:-200% center} }

  /* ── Status badges ── */
  .badge {
    display: inline-block;
    font-size: 9px;
    letter-spacing: 2px;
    text-transform: uppercase;
    padding: 3px 8px;
    border-radius: 3px;
    border: 1px solid var(--gold4);
    color: var(--gold3);
    vertical-align: middle;
    margin-left: 8px;
  }
  .badge.success { border-color: rgba(60,120,60,.4); color: #7ab87a; }
  .badge.error   { border-color: rgba(120,60,60,.4); color: #c07070; }

  /* ── Scanlines CRT overlay ── */
  .scanlines {
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    pointer-events: none;
    z-index: 3;
    background: repeating-linear-gradient(
      0deg,
      transparent,
      transparent 3px,
      rgba(0,0,0,.04) 3px,
      rgba(0,0,0,.04) 4px
    );
  }

  /* ── Gold top accent bar ── */
  .top-bar {
    position: fixed;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, var(--gold3) 20%, var(--gold) 50%, var(--gold3) 80%, transparent);
    z-index: 20;
    pointer-events: none;
  }

  /* ── Plotly override for dark gold theme ── */
  .js-plotly-plot .plotly .bg { fill: transparent !important; }
</style>
"""

BASE_SCRIPTS = """
<canvas id="rain-canvas"></canvas>
<div class="glow"></div>
<div class="glow2"></div>
<div class="scanlines"></div>
<div class="top-bar"></div>
<script>
// ── Code Rain ──
(function(){
  const canvas = document.getElementById('rain-canvas');
  const ctx = canvas.getContext('2d');
  let cols, drops;
  const FONT_SIZE = 14;
  const CHARS = 'アイウエオカキクケコサシスセソタチツテトナニヌネノ0123456789ABCDEF∑∏∫∂∆';
  function resize(){
    canvas.width  = window.innerWidth;
    canvas.height = window.innerHeight;
    cols  = Math.floor(canvas.width / FONT_SIZE);
    drops = Array(cols).fill(1);
  }
  function draw(){
    ctx.fillStyle = 'rgba(0,0,0,0.05)';
    ctx.fillRect(0,0,canvas.width,canvas.height);
    ctx.fillStyle = '#7a6535';
    ctx.font = FONT_SIZE + 'px JetBrains Mono, monospace';
    drops.forEach((y,i)=>{
      const ch = CHARS[Math.floor(Math.random()*CHARS.length)];
      ctx.fillText(ch, i*FONT_SIZE, y*FONT_SIZE);
      if(y*FONT_SIZE > canvas.height && Math.random() > 0.975) drops[i] = 0;
      drops[i]++;
    });
  }
  window.addEventListener('resize', resize);
  resize();
  setInterval(draw, 150);
})();

// ── Typewriter on h1 ──
(function(){
  const h1 = document.querySelector('h1.page-heading');
  if(!h1) return;
  const full = h1.textContent.trim();
  h1.textContent = '';
  h1.style.minHeight = '1.3em';
  let i = 0;
  const tick = setInterval(()=>{
    h1.textContent += full[i];
    i++;
    if(i >= full.length) clearInterval(tick);
  }, 32);
})();
</script>
"""

FOOTER_HTML = """
<footer class="vsb-footer">
  <span class="vsb-footer-left">VSB &mdash; Vinicius Soares Brandão</span>
  <span class="vsb-footer-right">Dados Econômicos &bull; v0.0.1 Beta</span>
</footer>
"""

NEGRONI_FAVICON = (
  "data:image/svg+xml,"
  "%3Csvg width='32' height='32' viewBox='0 0 20 24' fill='none' xmlns='http://www.w3.org/2000/svg'%3E"
  "%3Crect width='20' height='24' rx='3' fill='%23000'/%3E"
  "%3Cpath d='M2 3.5 L18 3.5 L15.5 18 L4.5 18 Z' stroke='%23c9a84c' stroke-width='1.2' stroke-linejoin='round'/%3E"
  "%3Cline x1='2' y1='3.5' x2='18' y2='3.5' stroke='%23e0b85a' stroke-width='1.5' stroke-linecap='round'/%3E"
  "%3Cline x1='4.5' y1='18' x2='15.5' y2='18' stroke='%23c9a84c' stroke-width='1.5' stroke-linecap='round'/%3E"
  "%3Cline x1='3.5' y1='20' x2='16.5' y2='20' stroke='%23a07830' stroke-width='1' stroke-linecap='round'/%3E"
  "%3Crect x='7.5' y='9' width='5' height='5' rx='1' stroke='%23c9a84c' stroke-width='.9' opacity='.7'/%3E"
  "%3Cline x1='4.9' y1='13.5' x2='15.1' y2='13.5' stroke='%23a07830' stroke-width='.8' stroke-dasharray='2 1.5' opacity='.6'/%3E"
  "%3Cpath d='M14.5 2.5 Q17.5 0 16.5 3.5' stroke='%23c9a84c' stroke-width='1.1' stroke-linecap='round'/%3E"
  "%3C/svg%3E"
)

def base_html(title, content, extra_head=""):
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <title>{title} — VSB</title>
  <link rel="icon" type="image/svg+xml" href="{NEGRONI_FAVICON}">
  {BASE_STYLE}
  {extra_head}
</head>
<body>
  {BASE_SCRIPTS}

  <div class="page-wrap">
    <header class="vsb-header">
      <div class="vsb-logo">VSB</div>
      <div class="vsb-title-block">
        <span class="vsb-title">Dados Econômicos</span>
        <span class="vsb-subtitle">Análise · Correlação · Insights 3D</span>
      </div>
    </header>

    {content}
  </div>

  {FOOTER_HTML}
</body>
</html>"""


# ─────────────────────────────────────────────
#  SVG ICONS
# ─────────────────────────────────────────────
def icon(name):
    icons = {
        "upload":   '<polyline points="16 16 12 12 8 16"/><line x1="12" y1="12" x2="12" y2="21"/><path d="M20.39 18.39A5 5 0 0 0 18 9h-1.26A8 8 0 1 0 3 16.3"/>',
        "table":    '<rect x="3" y="3" width="18" height="18" rx="2" ry="2"/><line x1="3" y1="9" x2="21" y2="9"/><line x1="3" y1="15" x2="21" y2="15"/><line x1="9" y1="3" x2="9" y2="21"/><line x1="15" y1="3" x2="15" y2="21"/>',
        "chart":    '<line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/><line x1="2" y1="20" x2="22" y2="20"/>',
        "edit":     '<path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>',
        "percent":  '<line x1="19" y1="5" x2="5" y2="19"/><circle cx="6.5" cy="6.5" r="2.5"/><circle cx="17.5" cy="17.5" r="2.5"/>',
        "scatter":  '<circle cx="8" cy="16" r="2"/><circle cx="16" cy="8" r="2"/><circle cx="12" cy="12" r="2"/><circle cx="5" cy="10" r="2"/><circle cx="18" cy="15" r="2"/>',
        "cube":     '<path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/><polyline points="3.27 6.96 12 12.01 20.73 6.96"/><line x1="12" y1="22.08" x2="12" y2="12"/>',
        "arrow-left": '<line x1="19" y1="12" x2="5" y2="12"/><polyline points="12 19 5 12 12 5"/>',
        "send":     '<line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/>',
        "refresh":  '<polyline points="23 4 23 10 17 10"/><path d="M20.49 15a9 9 0 1 1-2.12-9.36L23 10"/>',
    }
    paths = icons.get(name, "")
    return f'<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">{paths}</svg>'


# ─────────────────────────────────────────────
#  ROUTES
# ─────────────────────────────────────────────

@app.route('/')
def index():
    content = f"""
    <div class="section-tag">// repositório</div>
    <h1 class="page-heading">Upload de Dados Econômicos</h1>

    <div class="card">
      <h2 class="sub-heading">Enviar Arquivos CSV</h2>
      <form action='/upload' method='POST' enctype='multipart/form-data' class="vsb-form">
        <div class="form-group">
          <label class="form-label">Arquivo de Inadimplência (.csv)</label>
          <input name='campo_inadimplencia' type='file' accept='.csv' required class="form-input">
        </div>
        <div class="form-group">
          <label class="form-label">Arquivo da Taxa Selic (.csv)</label>
          <input name='campo_selic' type='file' accept='.csv' required class="form-input">
        </div>
        <button type='submit' class="vsb-btn">
          {icon('upload')}
          Fazer Upload
        </button>
      </form>
    </div>

    <hr class="vsb-divider">
    <div class="section-tag">// navegação</div>
    <div class="nav-grid">
      <a href='/consultar' class="nav-card">
        <div class="nav-card-icon">{icon('table')}</div>
        <div class="nav-card-text">
          <span class="nav-card-label">Consultar Dados</span>
          <span class="nav-card-desc">Visualizar tabelas do banco</span>
        </div>
      </a>
      <a href='/graficos' class="nav-card">
        <div class="nav-card-icon">{icon('chart')}</div>
        <div class="nav-card-text">
          <span class="nav-card-label">Gráficos</span>
          <span class="nav-card-desc">Evolução temporal das séries</span>
        </div>
      </a>
      <a href='/editar_inadimplencia' class="nav-card">
        <div class="nav-card-icon">{icon('edit')}</div>
        <div class="nav-card-text">
          <span class="nav-card-label">Editar Inadimplência</span>
          <span class="nav-card-desc">Atualizar valores mensais</span>
        </div>
      </a>
      <a href='/editar_selic' class="nav-card">
        <div class="nav-card-icon">{icon('percent')}</div>
        <div class="nav-card-text">
          <span class="nav-card-label">Editar Selic</span>
          <span class="nav-card-desc">Atualizar taxa mensal</span>
        </div>
      </a>
      <a href='/correlacao' class="nav-card">
        <div class="nav-card-icon">{icon('scatter')}</div>
        <div class="nav-card-text">
          <span class="nav-card-label">Correlação</span>
          <span class="nav-card-desc">SELIC × Inadimplência</span>
        </div>
      </a>
      <a href='/insights_3d' class="nav-card">
        <div class="nav-card-icon">{icon('cube')}</div>
        <div class="nav-card-text">
          <span class="nav-card-label">Insights 3D</span>
          <span class="nav-card-desc">Clusters e regressão espacial</span>
        </div>
      </a>
    </div>
    """
    return base_html("Início", content)


@app.route('/upload', methods=['POST', 'GET'])
def upload():
    inad_file = request.files.get('campo_inadimplencia')
    selic_file = request.files.get('campo_selic')

    if not inad_file or not selic_file:
        content = f"""
        <div class="section-tag">// upload</div>
        <h1 class="page-heading">Erro no Upload</h1>
        <div class="card">
          <p style="color:#c07070;font-size:13px;">Ambos os arquivos devem ser enviados.</p>
        </div>
        <a href='/' class="back-link">{icon('arrow-left')} Voltar</a>
        """
        return base_html("Upload — Erro", content), 400

    inad_df = pd.read_csv(inad_file, sep=";", names=['data', 'inadimplencia'], header=0)
    selic_df = pd.read_csv(selic_file, sep=";", names=['data', 'selic_diaria'], header=0)
    inad_df['data']  = pd.to_datetime(inad_df['data'],  format="%d/%m/%Y")
    selic_df['data'] = pd.to_datetime(selic_df['data'], format="%d/%m/%Y")
    inad_df['mes']  = inad_df['data'].dt.to_period('M').astype(str)
    selic_df['mes'] = selic_df['data'].dt.to_period('M').astype(str)
    inad_mensal  = inad_df[['mes','inadimplencia']].drop_duplicates()
    selic_mensal = selic_df.groupby('mes')['selic_diaria'].mean().reset_index()

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS inadimplencia")
        cursor.execute("DROP TABLE IF EXISTS selic")
        inad_mensal.to_sql('inadimplencia',  conn, if_exists='replace', index=False)
        selic_mensal.to_sql('selic', conn, if_exists='replace', index=False)

    content = f"""
    <div class="section-tag">// upload</div>
    <h1 class="page-heading">Upload Concluído</h1>
    <div class="card">
      <p style="font-size:13px;color:#7ab87a;margin-bottom:16px;">
        Dados armazenados com sucesso no banco de dados. <span class="badge success">OK</span>
      </p>
      <div style="font-size:11px;color:var(--muted);display:flex;flex-direction:column;gap:4px;">
        <span>&#x2022; inadimplência: {len(inad_mensal)} registros mensais</span>
        <span>&#x2022; selic: {len(selic_mensal)} registros mensais</span>
      </div>
    </div>
    <a href='/' class="back-link">{icon('arrow-left')} Voltar ao início</a>
    """
    return base_html("Upload", content)


@app.route('/consultar', methods=['POST', 'GET'])
def consultar():
    table_html = ""
    if request.method == 'POST':
        tabela = request.form.get('campo_tabela')
        if tabela not in ['inadimplencia', 'selic']:
            content = f"""
            <div class="section-tag">// consulta</div>
            <h1 class="page-heading">Acesso Negado</h1>
            <div class="card">
              <p style="color:#c07070;font-size:13px;">Tabela inválida. <span class="badge error">403</span></p>
            </div>
            <a href='/' class="back-link">{icon('arrow-left')} Voltar</a>
            """
            return base_html("Consulta — Erro", content), 400

        with sqlite3.connect(DB_PATH) as conn:
            df = pd.read_sql_query(f"SELECT * FROM {tabela}", conn)

        rows_html = "".join(
            f"<tr>{''.join(f'<td>{v}</td>' for v in row)}</tr>"
            for row in df.values
        )
        headers_html = "".join(f"<th>{c}</th>" for c in df.columns)
        table_html = f"""
        <div class="data-table-wrap" style="margin-top:20px;">
          <table>
            <thead><tr>{headers_html}</tr></thead>
            <tbody>{rows_html}</tbody>
          </table>
        </div>
        """

    content = f"""
    <div class="section-tag">// banco de dados</div>
    <h1 class="page-heading">Consultar Tabelas</h1>
    <div class="card">
      <h2 class="sub-heading">Selecionar Tabela</h2>
      <form method='POST' class="vsb-form">
        <div class="form-group">
          <label class="form-label">Tabela</label>
          <select name='campo_tabela' class="form-select">
            <option value='inadimplencia'>Inadimplência</option>
            <option value='selic'>Taxa Selic</option>
          </select>
        </div>
        <button type='submit' class="vsb-btn">
          {icon('table')}
          Consultar
        </button>
      </form>
    </div>
    {table_html}
    <a href='/' class="back-link">{icon('arrow-left')} Voltar ao início</a>
    """
    return base_html("Consultar", content)


@app.route('/graficos')
def graficos():
    with sqlite3.connect(DB_PATH) as conn:
        inad_df  = pd.read_sql_query("SELECT * FROM inadimplencia", conn)
        selic_df = pd.read_sql_query("SELECT * FROM selic", conn)

    gold_color  = '#c9a84c'
    gold2_color = '#a8864a'

    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(
        x=inad_df['mes'], y=inad_df['inadimplencia'],
        mode='lines+markers', name='Inadimplência',
        line=dict(color=gold_color, width=2),
        marker=dict(color=gold_color, size=6, line=dict(color='#000', width=1)),
        hovertemplate='%{x}<br>Inadimplência: %{y:.2f}%<extra></extra>'
    ))
    fig1.update_layout(
        title=dict(text='Evolução da Inadimplência', font=dict(color=gold_color, size=15, family='JetBrains Mono')),
        xaxis_title='Mês', yaxis_title='%',
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(10,8,4,.6)',
        font=dict(family='JetBrains Mono', color='#8a7a55', size=11),
        margin=dict(l=40, r=20, t=50, b=40),
        xaxis=dict(gridcolor='rgba(120,90,40,.12)', linecolor='rgba(120,90,40,.3)'),
        yaxis=dict(gridcolor='rgba(120,90,40,.12)', linecolor='rgba(120,90,40,.3)'),
    )

    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(
        x=selic_df['mes'], y=selic_df['selic_diaria'],
        mode='lines+markers', name='Selic',
        line=dict(color=gold2_color, width=2),
        marker=dict(color=gold2_color, size=6, line=dict(color='#000', width=1)),
        hovertemplate='%{x}<br>Selic Média: %{y:.4f}<extra></extra>'
    ))
    fig2.update_layout(
        title=dict(text='Média Mensal da SELIC', font=dict(color=gold_color, size=15, family='JetBrains Mono')),
        xaxis_title='Mês', yaxis_title='Taxa',
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(10,8,4,.6)',
        font=dict(family='JetBrains Mono', color='#8a7a55', size=11),
        margin=dict(l=40, r=20, t=50, b=40),
        xaxis=dict(gridcolor='rgba(120,90,40,.12)', linecolor='rgba(120,90,40,.3)'),
        yaxis=dict(gridcolor='rgba(120,90,40,.12)', linecolor='rgba(120,90,40,.3)'),
    )

    g1 = fig1.to_html(full_html=False, include_plotlyjs='cdn')
    g2 = fig2.to_html(full_html=False, include_plotlyjs=False)

    content = f"""
    <div class="section-tag">// visualização</div>
    <h1 class="page-heading">Gráficos Econômicos</h1>
    <div class="graph-grid">
      <div class="graph-panel">{g1}</div>
      <div class="graph-panel">{g2}</div>
    </div>
    <a href='/' class="back-link">{icon('arrow-left')} Voltar ao início</a>
    """
    return base_html("Gráficos", content)


@app.route('/editar_inadimplencia', methods=['POST', 'GET'])
def editar_inadimplencia():
    msg_html = ""
    if request.method == 'POST':
        mes       = request.form.get('campo_mes')
        novo_valor = request.form.get('campo_valor')
        try:
            novo_valor = float(novo_valor)
        except:
            msg_html = '<p style="color:#c07070;font-size:12px;margin-top:12px;">Valor inválido. Use um número decimal. <span class="badge error">ERRO</span></p>'
        else:
            with sqlite3.connect(DB_PATH) as conn:
                cursor = conn.cursor()
                cursor.execute('UPDATE inadimplencia SET inadimplencia = ? WHERE mes = ?', (novo_valor, mes))
                conn.commit()
            msg_html = f'<p style="color:#7ab87a;font-size:12px;margin-top:12px;">Inadimplência atualizada para <strong>{mes}</strong> → {novo_valor:.4f} <span class="badge success">OK</span></p>'

    content = f"""
    <div class="section-tag">// edição</div>
    <h1 class="page-heading">Editar Inadimplência</h1>
    <div class="card">
      <h2 class="sub-heading">Atualizar Registro</h2>
      <form method='POST' class="vsb-form">
        <div class="form-group">
          <label class="form-label">Mês (AAAA-MM)</label>
          <input type='text' name='campo_mes' placeholder='ex: 2024-01' class="form-input" required>
        </div>
        <div class="form-group">
          <label class="form-label">Novo Valor de Inadimplência</label>
          <input type='text' name='campo_valor' placeholder='ex: 3.45' class="form-input" required>
        </div>
        <button type='submit' class="vsb-btn">
          {icon('send')}
          Atualizar
        </button>
      </form>
      {msg_html}
    </div>
    <a href='/' class="back-link">{icon('arrow-left')} Voltar ao início</a>
    """
    return base_html("Editar Inadimplência", content)


@app.route('/editar_selic', methods=['GET', 'POST'])
def editar_selic():
    msg_html = ""
    if request.method == 'POST':
        mes       = request.form.get('campo_mes')
        novo_valor = request.form.get('campo_valor')
        try:
            novo_valor = float(novo_valor)
        except:
            msg_html = '<p style="color:#c07070;font-size:12px;margin-top:12px;">Valor inválido. Use um número decimal. <span class="badge error">ERRO</span></p>'
        else:
            with sqlite3.connect(DB_PATH) as conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE selic SET selic_diaria = ? WHERE mes = ?", (novo_valor, mes))
                conn.commit()
            msg_html = f'<p style="color:#7ab87a;font-size:12px;margin-top:12px;">SELIC atualizada para <strong>{mes}</strong> → {novo_valor:.6f} <span class="badge success">OK</span></p>'

    content = f"""
    <div class="section-tag">// edição</div>
    <h1 class="page-heading">Editar Taxa SELIC</h1>
    <div class="card">
      <h2 class="sub-heading">Atualizar Registro</h2>
      <form method='POST' class="vsb-form">
        <div class="form-group">
          <label class="form-label">Mês (AAAA-MM)</label>
          <input type='text' name='campo_mes' placeholder='ex: 2024-01' class="form-input" required>
        </div>
        <div class="form-group">
          <label class="form-label">Nova Taxa SELIC</label>
          <input type='text' name='campo_valor' placeholder='ex: 0.001234' class="form-input" required>
        </div>
        <button type='submit' class="vsb-btn">
          {icon('send')}
          Atualizar
        </button>
      </form>
      {msg_html}
    </div>
    <a href='/' class="back-link">{icon('arrow-left')} Voltar ao início</a>
    """
    return base_html("Editar SELIC", content)


@app.route('/correlacao')
def correlacao():
    with sqlite3.connect(DB_PATH) as conn:
        inad_df  = pd.read_sql_query("SELECT * FROM inadimplencia", conn)
        selic_df = pd.read_sql_query("SELECT * FROM selic", conn)

    merged = pd.merge(inad_df, selic_df, on='mes')
    correl = merged['inadimplencia'].corr(merged['selic_diaria'])
    x = merged['selic_diaria']
    y = merged['inadimplencia']
    m, b = np.polyfit(x, y, 1)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x, y=y, mode='markers',
        name='Inadimplência × SELIC',
        marker=dict(color='rgba(201,168,76,0.85)', size=10,
                    line=dict(width=1, color='rgba(201,168,76,0.3)'), symbol='circle'),
        hovertemplate='SELIC: %{x:.4f}<br>Inadimplência: %{y:.2f}%<extra></extra>'
    ))
    fig.add_trace(go.Scatter(
        x=x, y=m*x+b, mode='lines',
        name='Linha de Tendência',
        line=dict(color='rgba(168,100,60,0.9)', width=3, dash='dot')
    ))
    fig.update_layout(
        title=dict(
            text=f'<b>Correlação SELIC × Inadimplência</b><br>'
                 f'<span style="font-size:13px;color:#8a7a55;">Coeficiente r = {correl:.4f}</span>',
            font=dict(color='#c9a84c', family='JetBrains Mono', size=15),
            x=0.5, xanchor='center', y=0.97, yanchor='top'
        ),
        xaxis_title=dict(text='SELIC Média Mensal', font=dict(color='#8a7a55', size=12, family='JetBrains Mono')),
        yaxis_title=dict(text='Inadimplência (%)',  font=dict(color='#8a7a55', size=12, family='JetBrains Mono')),
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(10,8,4,.6)',
        font=dict(family='JetBrains Mono', color='#8a7a55', size=11),
        xaxis=dict(gridcolor='rgba(120,90,40,.12)', linecolor='rgba(120,90,40,.3)', tickfont=dict(color='#8a7a55')),
        yaxis=dict(gridcolor='rgba(120,90,40,.12)', linecolor='rgba(120,90,40,.3)', tickfont=dict(color='#8a7a55')),
        legend=dict(orientation='h', bgcolor='rgba(0,0,0,0)', borderwidth=0, y=1.06, x=0.5, xanchor='center', yanchor='bottom', font=dict(color='#8a7a55')),
        margin=dict(l=50, r=30, t=100, b=50),
        height=520,
    )
    grafico = fig.to_html(full_html=False, include_plotlyjs='cdn')

    correl_badge = "Forte" if abs(correl) > 0.7 else "Moderada" if abs(correl) > 0.4 else "Fraca"
    correl_dir   = "positiva" if correl >= 0 else "negativa"

    content = f"""
    <div class="section-tag">// análise estatística</div>
    <h1 class="page-heading">Correlação SELIC × Inadimplência</h1>

    <div class="card" style="margin-bottom:20px;">
      <div style="display:flex;gap:32px;flex-wrap:wrap;">
        <div>
          <div class="form-label" style="margin-bottom:4px;">Coeficiente de Correlação</div>
          <div style="font-family:'Playfair Display',serif;font-size:28px;color:var(--gold);">{correl:.4f}</div>
        </div>
        <div>
          <div class="form-label" style="margin-bottom:4px;">Intensidade</div>
          <div style="font-size:15px;color:var(--gold2);">{correl_badge} <span style="color:var(--muted);font-size:11px;">/ {correl_dir}</span></div>
        </div>
        <div>
          <div class="form-label" style="margin-bottom:4px;">Inclinação da Reta</div>
          <div style="font-size:15px;color:var(--gold2);">{m:.4f}</div>
        </div>
      </div>
    </div>

    <div class="graph-panel" style="padding:8px;">{grafico}</div>
    <a href='/' class="back-link">{icon('arrow-left')} Voltar ao início</a>
    """
    return base_html("Correlação", content)


@app.route('/insights_3d')
def insights3d():
    with sqlite3.connect(DB_PATH) as conn:
        inad_df  = pd.read_sql_query("SELECT * FROM inadimplencia", conn)
        selic_df = pd.read_sql_query("SELECT * FROM selic", conn)

    merged = pd.merge(inad_df, selic_df, on='mes').sort_values('mes')
    merged['mes_idx'] = range(len(merged))
    merged['tend_inad'] = merged['inadimplencia'].diff().fillna(0)
    trend_color = ['subiu' if x > 0 else 'caiu' if x < 0 else 'estável' for x in merged['tend_inad']]
    merged['var_inad']  = merged['inadimplencia'].diff().fillna(0)
    merged['var_selic'] = merged['selic_diaria'].diff().fillna(0)

    features       = merged[['selic_diaria', 'inadimplencia']].copy()
    scaler         = StandardScaler()
    scaled_features = scaler.fit_transform(features)
    kmeans         = KMeans(n_clusters=3, random_state=42, n_init=10)
    merged['cluster'] = kmeans.fit_predict(scaled_features)

    x_mat = merged[['mes_idx', 'selic_diaria']].values
    y_vec = merged['inadimplencia'].values
    a     = np.c_[x_mat, np.ones(x_mat.shape[0])]
    coeffs, _, _, _ = np.linalg.lstsq(a, y_vec, rcond=None)

    xi = np.linspace(merged['mes_idx'].min(), merged['mes_idx'].max(), 30)
    yi = np.linspace(merged['selic_diaria'].min(), merged['selic_diaria'].max(), 30)
    xi, yi = np.meshgrid(xi, yi)
    zi = coeffs[0]*xi + coeffs[1]*yi + coeffs[2]

    # Cluster colours: gold / teal / red-orange — vivid and distinct on dark bg
    cluster_palette = {0: '#c9a84c', 1: '#4fc3c3', 2: '#e05a3a'}
    cluster_names   = {0: 'Cluster A — Alta Selic / Alta Inad',
                       1: 'Cluster B — Baixa Selic / Baixa Inad',
                       2: 'Cluster C — Transição / Volatilidade'}

    traces = []

    # ── Regression surface (rendered first, behind points) ──
    surface = go.Surface(
        x=xi, y=yi, z=zi,
        showscale=False,
        colorscale=[
            [0.0, 'rgba(20,14,4,0.55)'],
            [0.5, 'rgba(90,65,20,0.45)'],
            [1.0, 'rgba(201,168,76,0.38)'],
        ],
        opacity=0.5,
        name='Plano de Regressão',
        hoverinfo='skip',
        contours=dict(
            x=dict(show=True, color='rgba(201,168,76,0.12)', width=1),
            y=dict(show=True, color='rgba(201,168,76,0.12)', width=1),
            z=dict(show=False),
        ),
    )
    traces.append(surface)

    # ── Chronological path line ──
    path = go.Scatter3d(
        x=merged['mes_idx'],
        y=merged['selic_diaria'],
        z=merged['inadimplencia'],
        mode='lines',
        name='Trajetória Temporal',
        line=dict(color='rgba(201,168,76,0.25)', width=2),
        hoverinfo='skip',
        showlegend=True,
    )
    traces.append(path)

    # ── One scatter trace per cluster (for proper legend) ──
    for cid in sorted(merged['cluster'].unique()):
        mask = merged['cluster'] == cid
        sub  = merged[mask]
        tc   = [trend_color[i] for i in sub.index]
        col  = cluster_palette[cid]

        hover_texts = [
            f"<b>{m}</b><br>"
            f"Inadimplência: <b>{z:.2f}%</b><br>"
            f"SELIC média: {s:.5f}<br>"
            f"ΔInad: {vi:+.2f} | ΔSelic: {vs:+.5f}<br>"
            f"Tendência: {t}"
            for m, z, s, vi, vs, t in zip(
                sub['mes'], sub['inadimplencia'], sub['selic_diaria'],
                sub['var_inad'], sub['var_selic'], tc
            )
        ]
        traces.append(go.Scatter3d(
            x=sub['mes_idx'],
            y=sub['selic_diaria'],
            z=sub['inadimplencia'],
            mode='markers',
            name=cluster_names[cid],
            marker=dict(
                size=9,
                color=col,
                opacity=0.92,
                line=dict(color='rgba(0,0,0,0.55)', width=0.8),
                symbol='circle',
            ),
            text=hover_texts,
            hovertemplate='%{text}<extra></extra>',
        ))

    # ── First / last point labels ──
    label_idx = [0, len(merged)-1]
    for i in label_idx:
        row = merged.iloc[i]
        traces.append(go.Scatter3d(
            x=[row['mes_idx']], y=[row['selic_diaria']], z=[row['inadimplencia']],
            mode='text',
            text=[row['mes']],
            textfont=dict(color='#c9a84c', size=9, family='JetBrains Mono'),
            showlegend=False,
            hoverinfo='skip',
        ))

    fig = go.Figure(data=traces)
    fig.update_layout(
        scene=dict(
            xaxis=dict(
                title=dict(text='Tempo (meses)', font=dict(size=11, color='#8a7a55')),
                gridcolor='rgba(120,90,40,.18)',
                backgroundcolor='rgba(8,6,2,0.7)',
                color='#8a7a55',
                tickfont=dict(size=9, color='#6a5a3a'),
                showbackground=True,
                zerolinecolor='rgba(120,90,40,.3)',
            ),
            yaxis=dict(
                title=dict(text='SELIC (%)', font=dict(size=11, color='#8a7a55')),
                gridcolor='rgba(120,90,40,.18)',
                backgroundcolor='rgba(5,4,2,0.7)',
                color='#8a7a55',
                tickfont=dict(size=9, color='#6a5a3a'),
                showbackground=True,
                zerolinecolor='rgba(120,90,40,.3)',
            ),
            zaxis=dict(
                title=dict(text='Inadimplência (%)', font=dict(size=11, color='#8a7a55')),
                gridcolor='rgba(120,90,40,.18)',
                backgroundcolor='rgba(6,4,1,0.7)',
                color='#8a7a55',
                tickfont=dict(size=9, color='#6a5a3a'),
                showbackground=True,
                zerolinecolor='rgba(120,90,40,.3)',
            ),
            bgcolor='rgba(0,0,0,0)',
            camera=dict(
                eye=dict(x=1.55, y=-1.7, z=0.85),
                up=dict(x=0, y=0, z=1),
                center=dict(x=0, y=0, z=-0.1),
            ),
            aspectmode='manual',
            aspectratio=dict(x=1.6, y=1.1, z=0.8),
        ),
        title=dict(
            text='<b>Insights 3D</b>  <span style="font-size:12px;color:#8a7a55;">Tendência · Derivadas · K-Means Clusters</span>',
            font=dict(color='#c9a84c', family='JetBrains Mono', size=15),
            x=0.5, xanchor='center',
        ),
        legend=dict(
            font=dict(color='#8a7a55', family='JetBrains Mono', size=10),
            bgcolor='rgba(10,8,4,0.75)',
            bordercolor='rgba(120,90,40,.3)',
            borderwidth=1,
            x=0.01, y=0.99,
            xanchor='left', yanchor='top',
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='JetBrains Mono', color='#8a7a55', size=11),
        margin=dict(l=0, r=0, t=55, b=0),
        height=680,
    )
    grafico3d = fig.to_html(full_html=False, include_plotlyjs='cdn')

    content = f"""
    <div class="section-tag">// machine learning · 3D</div>
    <h1 class="page-heading">Insights Econômicos 3D</h1>

    <div class="card" style="margin-bottom:20px;">
      <div style="display:flex;gap:32px;flex-wrap:wrap;font-size:11px;color:var(--muted);">
        <span>&#x2022; K-Means com 3 clusters (StandardScaler)</span>
        <span>&#x2022; Plano de regressão por mínimos quadrados</span>
        <span>&#x2022; Derivadas discretas mensais (Δ Inad, Δ SELIC)</span>
        <span>&#x2022; {len(merged)} observações</span>
      </div>
    </div>

    <div class="graph-panel" style="padding:4px;">{grafico3d}</div>
    <a href='/' class="back-link">{icon('arrow-left')} Voltar ao início</a>
    """
    return base_html("Insights 3D", content)


if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
