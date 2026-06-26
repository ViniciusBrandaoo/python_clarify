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
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,500;0,600;0,700;1,500&family=Inter:wght@300;400;500;600&family=JetBrains+Mono:wght@300;400&display=swap" rel="stylesheet">
<style>
/* ── RESET & ROOT ── */
*{margin:0;padding:0;box-sizing:border-box;}
:root{
  --s-black:   #080C18;
  --s-dark:    #0B1020;
  --s-dark2:   #0E1528;
  --s-dark3:   #131C34;
  --s-cream:   #F0E8D5;
  --s-gold:    #C9A84C;
  --s-gold2:   #B8962E;
  --s-gold3:   #A07828;
  --s-gold4:   #6B5020;
  --s-gold5:   #3A2C10;
  --s-text:    #E4D4A2;
  --s-text2:   #C0A868;
  --s-text3:   #8A7040;
  --s-text-cr: #1C1408;
  --s-text-cr2:#3A2E18;
  --s-text-cr3:#6A5A30;
  --radius: 2px;
  --transition: .32s cubic-bezier(.4,0,.2,1);
}
html{scroll-behavior:smooth;}
body{
  background:var(--s-black);
  color:var(--s-text);
  font-family:'Inter',sans-serif;
  overflow-x:hidden;
  -webkit-font-smoothing:antialiased;
  cursor:none;
}
a,button,[onclick]{cursor:none;}

/* ── CUSTOM CURSOR ── */
#cursor-dot{
  position:fixed;width:8px;height:8px;border-radius:50%;
  background:var(--s-gold);
  pointer-events:none;z-index:9999;
  transform:translate(-50%,-50%);
  transition:width .2s,height .2s,background .2s,opacity .2s;
  box-shadow:0 0 10px rgba(201,168,76,.8),0 0 20px rgba(201,168,76,.3);
}
#cursor-ring{
  position:fixed;width:36px;height:36px;border-radius:50%;
  border:1px solid rgba(201,168,76,.5);
  pointer-events:none;z-index:9998;
  transform:translate(-50%,-50%);
  transition:width .35s ease,height .35s ease,border-color .35s,opacity .3s;
}
body.cursor-hover #cursor-dot{width:12px;height:12px;box-shadow:0 0 18px rgba(201,168,76,1),0 0 36px rgba(201,168,76,.4);}
body.cursor-hover #cursor-ring{width:52px;height:52px;border-color:rgba(201,168,76,.8);}
body.cursor-click #cursor-dot{width:6px;height:6px;background:#fff;}
body.cursor-click #cursor-ring{width:24px;height:24px;border-color:var(--s-gold);}

/* ── BACKGROUND LAYERS ── */
.bg-gradient{
  position:fixed;inset:0;z-index:0;pointer-events:none;
  background:
    radial-gradient(ellipse 80% 60% at 10% 5%, rgba(201,168,76,.06) 0%, transparent 55%),
    radial-gradient(ellipse 60% 50% at 90% 90%, rgba(20,40,120,.15) 0%, transparent 50%),
    linear-gradient(160deg, #080C18 0%, #0B1020 100%);
}
.code-rain-dark{position:fixed;inset:0;z-index:1;pointer-events:none;opacity:.11;mix-blend-mode:screen;}
.code-rain-dark span{position:absolute;top:-100px;color:#B89030;font-family:'JetBrains Mono',monospace;font-size:11px;animation:rain-fall linear infinite;}
.noise{
  position:fixed;inset:0;z-index:2;pointer-events:none;opacity:.018;
  background-image:url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
  background-size:200px 200px;
}
@keyframes rain-fall{
  0%{transform:translateY(-100px);opacity:0;}
  8%{opacity:1;}
  100%{transform:translateY(110vh);opacity:0;}
}

/* ── TOP BAR ── */
.top-bar{
  position:fixed;top:0;left:0;right:0;height:2px;
  background:linear-gradient(90deg,transparent,var(--s-gold3) 20%,var(--s-gold) 50%,var(--s-gold3) 80%,transparent);
  z-index:200;pointer-events:none;
}

/* ── NAVIGATION ── */
nav{
  position:fixed;top:2px;left:0;right:0;z-index:199;
  display:flex;justify-content:space-between;align-items:center;
  padding:0 48px;height:62px;
  background:rgba(8,12,24,.85);
  backdrop-filter:blur(20px) saturate(1.4);
  border-bottom:1px solid rgba(201,168,76,.08);
}
.nav-logo{
  font-family:'Playfair Display',serif;
  font-size:1.1rem;font-weight:600;
  color:var(--s-gold);letter-spacing:3px;
  text-decoration:none;
}
.nav-logo span{color:var(--s-text3);font-weight:400;}
.nav-links{display:flex;gap:28px;align-items:center;}
.nav-links a{
  color:var(--s-text3);text-decoration:none;
  font-size:.68rem;letter-spacing:2.5px;text-transform:uppercase;
  font-weight:500;transition:color var(--transition);
  position:relative;padding-bottom:2px;
}
.nav-links a::after{
  content:'';position:absolute;bottom:0;left:0;right:0;height:1px;
  background:var(--s-gold);transform:scaleX(0);transform-origin:left;
  transition:transform var(--transition);
}
.nav-links a:hover{color:var(--s-gold);}
.nav-links a:hover::after{transform:scaleX(1);}

/* ── LAYOUT ── */
.page-wrap{
  position:relative;z-index:10;
  max-width:920px;margin:0 auto;
  padding:100px 32px 96px;
}

/* ── SECTION HEADERS ── */
.section-tag{
  font-size:.58rem;letter-spacing:4px;text-transform:uppercase;
  color:var(--s-gold);font-weight:500;margin-bottom:10px;
  display:flex;align-items:center;gap:12px;
}
.section-tag::before,.section-tag::after{
  content:'';display:block;width:36px;height:1px;
  background:linear-gradient(to right,transparent,rgba(201,168,76,.4),transparent);
}
.section-tag::after{transform:rotate(180deg);}

/* ── PAGE HEADING ── */
h1.page-heading{
  font-family:'Playfair Display',serif;
  font-size:clamp(22px,5vw,36px);
  margin-bottom:36px;line-height:1.2;
  background:linear-gradient(135deg,var(--s-gold) 0%,#E8D080 50%,var(--s-gold2) 100%);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
}
h2.sub-heading{
  font-size:.68rem;letter-spacing:2px;text-transform:uppercase;
  color:var(--s-text2);margin-bottom:18px;font-weight:500;
}

/* ── CARDS ── */
.card{
  background:rgba(255,255,255,.02);
  border:1px solid rgba(201,168,76,.1);
  border-radius:2px;padding:28px 32px;margin-bottom:20px;
  transition:border-color var(--transition),box-shadow var(--transition),background var(--transition);
  position:relative;overflow:hidden;
  backdrop-filter:blur(4px);
}
.card::before{
  content:'';position:absolute;top:0;left:0;right:0;height:1px;
  background:linear-gradient(to right,transparent,var(--s-gold),transparent);
  opacity:0;transition:opacity var(--transition);
}
.card:hover{border-color:rgba(201,168,76,.28);background:rgba(201,168,76,.03);}
.card:hover::before{opacity:1;}

/* ── NAV GRID ── */
.nav-grid{
  display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));
  gap:14px;margin-top:8px;
}
.nav-card{
  background:rgba(255,255,255,.02);
  border:1px solid rgba(201,168,76,.1);
  border-radius:2px;padding:20px 22px;
  text-decoration:none;display:flex;align-items:center;gap:14px;
  transition:all var(--transition);
  position:relative;overflow:hidden;
}
.nav-card::before{
  content:'';position:absolute;top:0;left:0;right:0;height:1px;
  background:linear-gradient(to right,transparent,var(--s-gold),transparent);
  opacity:0;transition:opacity var(--transition);
}
.nav-card:hover{
  border-color:rgba(201,168,76,.3);
  background:rgba(201,168,76,.04);
  transform:translateY(-3px);
  box-shadow:0 12px 32px rgba(0,0,0,.4);
}
.nav-card:hover::before{opacity:1;}
.nav-card-icon{
  width:36px;height:36px;
  border:1px solid rgba(201,168,76,.2);border-radius:2px;
  display:flex;align-items:center;justify-content:center;
  flex-shrink:0;transition:border-color var(--transition),box-shadow var(--transition);
}
.nav-card:hover .nav-card-icon{border-color:var(--s-gold3);box-shadow:0 0 8px rgba(201,168,76,.15);}
.nav-card-icon svg{width:18px;height:18px;stroke:var(--s-gold);fill:none;stroke-width:1.5;stroke-linecap:round;stroke-linejoin:round;}
.nav-card-text{display:flex;flex-direction:column;gap:2px;}
.nav-card-label{font-size:.78rem;color:var(--s-text2);letter-spacing:.4px;font-weight:500;}
.nav-card-desc{font-size:.62rem;color:var(--s-text3);letter-spacing:.5px;}

/* ── FORMS ── */
.vsb-form{display:flex;flex-direction:column;gap:18px;}
.form-group{display:flex;flex-direction:column;gap:6px;}
.form-label{
  font-size:.58rem;letter-spacing:2.5px;text-transform:uppercase;
  color:var(--s-text3);font-weight:500;
}
.form-input,.form-select{
  background:rgba(8,12,24,.8);
  border:1px solid rgba(201,168,76,.12);
  border-radius:2px;color:var(--s-text);
  font-family:'JetBrains Mono',monospace;font-size:.82rem;
  padding:10px 14px;outline:none;
  transition:border-color var(--transition),box-shadow var(--transition);
  width:100%;
}
.form-input:focus,.form-select:focus{
  border-color:var(--s-gold3);
  box-shadow:0 0 0 2px rgba(160,120,40,.15);
}
.form-select option{background:#080C18;}
input[type="file"].form-input{padding:8px 14px;cursor:pointer;}
input[type="file"].form-input::-webkit-file-upload-button{
  background:transparent;border:1px solid rgba(201,168,76,.2);
  color:var(--s-text2);font-family:'Inter',sans-serif;
  font-size:.62rem;letter-spacing:1.5px;text-transform:uppercase;
  padding:4px 12px;border-radius:2px;cursor:pointer;
  margin-right:10px;transition:border-color var(--transition);
}
input[type="file"].form-input::-webkit-file-upload-button:hover{border-color:var(--s-gold);color:var(--s-gold);}

/* ── BUTTONS ── */
.vsb-btn{
  display:inline-flex;align-items:center;gap:8px;
  border:1px solid rgba(201,168,76,.3);color:var(--s-text2);
  background:transparent;
  font-family:'Inter',sans-serif;font-size:.65rem;
  letter-spacing:2.5px;text-transform:uppercase;font-weight:600;
  padding:10px 26px;border-radius:2px;cursor:pointer;
  transition:all var(--transition);text-decoration:none;align-self:flex-start;
}
.vsb-btn:hover{
  border-color:var(--s-gold);color:var(--s-gold);
  background:rgba(201,168,76,.06);
  transform:translateY(-2px);
  box-shadow:0 8px 24px rgba(201,168,76,.15);
}
.vsb-btn.primary{
  background:var(--s-gold);color:var(--s-black);border-color:var(--s-gold);
}
.vsb-btn.primary:hover{background:var(--s-text);border-color:var(--s-text);color:var(--s-black);}
.vsb-btn svg{width:14px;height:14px;stroke:currentColor;fill:none;stroke-width:1.5;stroke-linecap:round;stroke-linejoin:round;}

/* ── BACK LINK ── */
.back-link{
  display:inline-flex;align-items:center;gap:7px;
  font-size:.6rem;color:var(--s-text3);text-decoration:none;
  letter-spacing:2px;text-transform:uppercase;font-weight:500;
  margin-top:32px;transition:color var(--transition);
}
.back-link:hover{color:var(--s-gold);}
.back-link svg{width:13px;height:13px;stroke:currentColor;fill:none;stroke-width:1.5;stroke-linecap:round;stroke-linejoin:round;}

/* ── DIVIDER ── */
.vsb-divider{border:none;border-top:1px solid rgba(201,168,76,.1);margin:32px 0;}

/* ── DATA TABLE ── */
.data-table-wrap{overflow-x:auto;border-radius:2px;border:1px solid rgba(201,168,76,.1);}
table{width:100%;border-collapse:collapse;font-size:.75rem;}
thead tr{background:rgba(201,168,76,.05);}
thead th{padding:10px 14px;text-align:left;color:var(--s-text2);letter-spacing:1.5px;font-size:.58rem;text-transform:uppercase;border-bottom:1px solid rgba(201,168,76,.1);}
tbody tr{border-bottom:1px solid rgba(201,168,76,.05);transition:background var(--transition);}
tbody tr:last-child{border-bottom:none;}
tbody tr:hover{background:rgba(201,168,76,.04);}
tbody td{padding:9px 14px;color:var(--s-text);}

/* ── GRAPH ── */
.graph-grid{display:grid;grid-template-columns:1fr 1fr;gap:20px;}
@media(max-width:680px){.graph-grid{grid-template-columns:1fr;}}
.graph-panel{
  background:rgba(255,255,255,.02);
  border:1px solid rgba(201,168,76,.1);border-radius:2px;
  padding:4px;overflow:hidden;
}

/* ── FOOTER ── */
.vsb-footer{
  position:fixed;bottom:0;left:0;right:0;
  border-top:1px solid rgba(201,168,76,.08);
  background:rgba(8,12,24,.9);backdrop-filter:blur(12px);
  padding:10px 48px;
  display:flex;align-items:center;justify-content:space-between;z-index:10;
}
.vsb-footer-left{font-size:.58rem;letter-spacing:2px;color:var(--s-text3);text-transform:uppercase;}
.vsb-footer-right{font-size:.58rem;letter-spacing:2px;color:var(--s-gold4);font-family:'JetBrains Mono',monospace;}

/* ── STATUS BADGES ── */
.badge{
  display:inline-block;font-size:.5rem;letter-spacing:2px;text-transform:uppercase;
  padding:3px 8px;border-radius:2px;
  border:1px solid rgba(201,168,76,.2);color:var(--s-text3);vertical-align:middle;margin-left:8px;
}
.badge.success{border-color:rgba(60,120,60,.4);color:#7ab87a;}
.badge.error{border-color:rgba(120,60,60,.4);color:#c07070;}

/* ── ANIMATIONS ── */
@keyframes fadeIn{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:translateY(0)}}
@keyframes fadeInDown{from{opacity:0;transform:translateY(-10px)}to{opacity:1;transform:translateY(0)}}

/* ── PLOTLY DARK OVERRIDE ── */
.js-plotly-plot .plotly .bg{fill:transparent !important;}

/* ── RESPONSIVE ── */
@media(max-width:700px){
  nav{padding:0 20px;}
  .page-wrap{padding:88px 20px 80px;}
  .vsb-footer{padding:10px 20px;}
}
</style>"""

BASE_SCRIPTS = """
<div id="cursor-dot"></div>
<div id="cursor-ring"></div>
<div class="bg-gradient"></div>
<div class="code-rain-dark"></div>
<div class="noise"></div>
<div class="top-bar"></div>
<script>
/* ── CODE RAIN ── */
const rainDark=document.querySelector(".code-rain-dark");
const drops=["import pandas as pd","df.groupby('região')","SELECT * FROM dados","plt.show()","def analyze(df):","return df.describe()","df.dropna()","WHERE receita > 0","df['kpi'].mean()","JOIN vendas ON id","model.fit(X_train)","df.corr().round(2)","sns.heatmap(corr)","ORDER BY data DESC","df.merge(left,right)","df.to_csv('output')","print(df.head())","GROUP BY mes","ax.set_xlabel('Data')","KMeans(n_clusters=3)"];
function makeRainSpan(){
  const text=drops[Math.floor(Math.random()*drops.length)];
  const left=Math.random()*100;const dur=Math.random()*7+6;
  const s=document.createElement("span");s.innerText=text;
  s.style.cssText=`left:${left}vw;animation-duration:${dur}s;font-size:${Math.random()>.5?'10px':'12px'}`;
  rainDark.appendChild(s);setTimeout(()=>s.remove(),14000);
}
setInterval(makeRainSpan,180);

/* ── CURSOR ── */
const dot=document.getElementById('cursor-dot');
const ring=document.getElementById('cursor-ring');
let mx=0,my=0,rx=0,ry=0;
document.addEventListener('mousemove',e=>{mx=e.clientX;my=e.clientY;dot.style.left=mx+'px';dot.style.top=my+'px';});
(function animRing(){rx+=(mx-rx)*.12;ry+=(my-ry)*.12;ring.style.left=rx+'px';ring.style.top=ry+'px';requestAnimationFrame(animRing);})();
const hoverSels='a,button,[onclick],.card,.nav-card,.vsb-btn';
document.querySelectorAll(hoverSels).forEach(el=>{
  el.addEventListener('mouseenter',()=>document.body.classList.add('cursor-hover'));
  el.addEventListener('mouseleave',()=>document.body.classList.remove('cursor-hover'));
});
document.addEventListener('mousedown',()=>document.body.classList.add('cursor-click'));
document.addEventListener('mouseup',()=>document.body.classList.remove('cursor-click'));
document.addEventListener('mouseleave',()=>{dot.style.opacity='0';ring.style.opacity='0';});
document.addEventListener('mouseenter',()=>{dot.style.opacity='1';ring.style.opacity='1';});

/* ── TYPEWRITER on h1 ── */
(function(){
  const h1=document.querySelector('h1.page-heading');
  if(!h1) return;
  const full=h1.textContent.trim();
  h1.textContent='';h1.style.minHeight='1.3em';
  let i=0;
  const tick=setInterval(()=>{h1.textContent+=full[i];i++;if(i>=full.length)clearInterval(tick);},30);
})();
</script>
"""

FOOTER_HTML = """
<footer class="vsb-footer">
  <span class="vsb-footer-left">VSB &mdash; Vinicius Soares Brandão</span>
  <span class="vsb-footer-right">data &rarr; insights &rarr; decisions</span>
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

  <nav>
    <a class="nav-logo" href="/">VSB<span>.</span></a>
    <div class="nav-links">
      <a href="/consultar">Consultar</a>
      <a href="/graficos">Gráficos</a>
      <a href="/editar_inadimplencia">Editar</a>
      <a href="/insights3d">Insights 3D</a>
    </div>
  </nav>

  <div class="page-wrap">
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
