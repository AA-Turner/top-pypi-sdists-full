"""bingo/web/server.py — FastAPI + WebSocket real-time dashboard."""
from __future__ import annotations
import socket, threading, queue
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .event_bus import EventBus


def _is_wsl2() -> bool:
    try:
        with open("/proc/version") as f:
            return "microsoft" in f.read().lower()
    except Exception:
        return False


def _find_free_port(start: int = 17890) -> int:
    for p in range(start, start + 20):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                s.bind(("", p))
                return p
        except OSError:
            continue
    return start


_HTML = """\
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>BINGO · Recon Dashboard</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;500;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box;}
:root{
  --bg:#030712;
  --surface:rgba(9,12,30,0.80);
  --border:rgba(255,255,255,0.07);
  --txt:#e2e8f0;
  --txt-dim:#64748b;
  --conf:#f59e0b;
  --prob:#8b5cf6;
  --pot:#38bdf8;
  --blk:#6b7280;
  --emerald:#10b981;
  --rose:#fb7185;
  --orange:#fb923c;
}
body{font:14px/1.6 'Space Grotesk',sans-serif;background:var(--bg);color:var(--txt);overflow:hidden;position:relative;}
#bg{position:fixed;top:0;left:0;width:100%;height:100%;z-index:0;pointer-events:none;}
.app{position:relative;z-index:1;display:flex;flex-direction:column;height:100vh;}
header{display:flex;align-items:center;gap:20px;padding:0 24px;height:52px;background:var(--surface);border-bottom:1px solid var(--border);backdrop-filter:blur(12px);position:relative;overflow:hidden;}
header::before{content:'';position:absolute;inset:0;background:linear-gradient(90deg,transparent 0%,rgba(167,139,250,0.08) 50%,transparent 100%);background-size:200% 100%;animation:shimmer 4s linear infinite;pointer-events:none;}
@keyframes shimmer{0%{background-position:200% 0;}100%{background-position:-200% 0;}}
#h-logo{font-weight:700;color:var(--emerald);font-size:18px;letter-spacing:-0.5px;}
#h-dot{width:10px;height:10px;border-radius:50%;background:var(--emerald);animation:breathe 2.4s infinite;}
@keyframes breathe{0%,100%{box-shadow:0 0 0 0 rgba(16,185,129,0.6),0 0 0 0 rgba(16,185,129,0.3);}50%{box-shadow:0 0 0 6px rgba(16,185,129,0),0 0 0 12px rgba(16,185,129,0);}}
#h-target{font-family:'JetBrains Mono',monospace;color:var(--prob);flex:1;font-size:13px;font-weight:500;}
#h-lnum{color:var(--conf);font-weight:500;}
#h-ws{color:var(--rose);font-size:12px;}
.grid{display:flex;flex:1;overflow:hidden;}
.panel{background:var(--surface);backdrop-filter:blur(20px);border-right:1px solid var(--border);overflow:auto;padding:16px;}
.left-panel{width:300px;}
.center-panel{flex:1;display:flex;flex-direction:column;padding:0;}
.right-panel{width:260px;}
.panel-title{font-size:11px;text-transform:uppercase;color:var(--txt-dim);margin-bottom:12px;letter-spacing:1px;font-weight:500;}
.tabs{display:flex;gap:8px;margin-bottom:12px;}
.tab{padding:6px 12px;border-radius:6px;font-size:12px;cursor:pointer;background:rgba(255,255,255,0.03);color:var(--txt-dim);transition:all 0.2s;font-weight:500;}
.tab.active{background:var(--prob);color:#fff;}
.find-list{display:none;}
.find-list.active{display:block;}
.card{background:rgba(0,0,0,0.4);border:1px solid var(--border);border-radius:8px;padding:12px;margin-bottom:10px;cursor:pointer;animation:cardMagic 500ms cubic-bezier(0.34,1.56,0.64,1);transition:all 0.3s;}
@keyframes cardMagic{0%{transform:translateY(16px) scale(0.94);opacity:0;filter:brightness(2.5);}55%{transform:translateY(-3px) scale(1.02);opacity:1;filter:brightness(1.4);}100%{transform:translateY(0) scale(1);opacity:1;filter:brightness(1);}}
.card:hover{border-color:rgba(255,255,255,0.2);transform:translateY(-2px);box-shadow:0 8px 24px rgba(0,0,0,0.3);}
.card.conf{border-left:3px solid var(--conf);}
.card.prob{border-left:3px solid var(--prob);}
.card.pot{border-left:3px solid var(--pot);}
.card-top{display:flex;justify-content:space-between;margin-bottom:6px;}
.card-type{font-weight:700;font-size:13px;color:var(--txt);}
.card-conf-badge{font-size:10px;padding:2px 8px;border-radius:4px;font-weight:700;letter-spacing:0.5px;}
.conf .card-conf-badge{background:var(--conf);color:#000;}
.prob .card-conf-badge{background:var(--prob);color:#fff;}
.pot .card-conf-badge{background:var(--pot);color:#000;}
.card-url{font-family:'JetBrains Mono',monospace;font-size:11px;color:var(--txt-dim);margin-bottom:4px;word-break:break-all;}
.card-payload{font-family:'JetBrains Mono',monospace;font-size:11px;background:rgba(0,0,0,0.5);padding:6px;border-radius:4px;margin-top:6px;color:var(--orange);max-height:40px;overflow:hidden;}
.card-ev{font-family:'JetBrains Mono',monospace;font-size:10px;color:var(--txt-dim);margin-top:6px;max-height:60px;overflow:hidden;line-height:1.4;}
.card.open .card-payload,.card.open .card-ev{max-height:none;}
#stream-header{padding:16px;border-bottom:1px solid var(--border);display:flex;justify-content:space-between;align-items:center;}
#scroll-pin{cursor:pointer;font-size:12px;padding:4px 10px;border-radius:4px;background:rgba(255,255,255,0.05);transition:all 0.2s;}
#scroll-pin:hover{background:rgba(255,255,255,0.1);}
#stream-body{flex:1;overflow-y:auto;padding:12px 16px;}
.stream-entry{padding:6px 10px;margin-bottom:4px;border-radius:4px;font-family:'JetBrains Mono',monospace;font-size:12px;line-height:1.5;animation:streamIn 220ms;word-break:break-word;}
@keyframes streamIn{0%{transform:translateX(-8px);opacity:0;}100%{transform:translateX(0);opacity:1;}}
.stream-entry.chunk{color:var(--txt-dim);}
.stream-entry.tool{color:var(--emerald);background:rgba(16,185,129,0.08);}
.stream-entry.hal{color:var(--rose);background:rgba(251,113,133,0.08);}
.stream-entry.nudge{color:var(--orange);background:rgba(251,146,60,0.08);}
.stream-entry.done{color:var(--conf);background:rgba(245,158,11,0.08);font-weight:500;}
.stat-ring{margin-bottom:20px;}
.ring-wrap{position:relative;width:80px;height:80px;margin:0 auto 8px;}
.ring-wrap svg{transform:rotate(-90deg);}
.ring-bg{fill:none;stroke:rgba(255,255,255,0.05);stroke-width:6;}
.ring-fill{fill:none;stroke-width:6;transition:stroke-dashoffset 600ms;stroke-linecap:round;}
.ring-fill.conf{stroke:var(--conf);}
.ring-fill.prob{stroke:var(--prob);}
.ring-fill.pot{stroke:var(--pot);}
.ring-fill.blk{stroke:var(--blk);}
.ring-label{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-size:20px;font-weight:700;}
.ring-name{text-align:center;font-size:11px;color:var(--txt-dim);text-transform:uppercase;letter-spacing:0.5px;}
#elapsed{margin-top:12px;padding:12px;background:rgba(0,0,0,0.3);border-radius:8px;text-align:center;font-family:'JetBrains Mono',monospace;font-size:13px;color:var(--txt-dim);}
#domain-list{margin-top:12px;max-height:200px;overflow-y:auto;}
.domain-item{padding:6px 10px;margin-bottom:4px;background:rgba(0,0,0,0.3);border-radius:4px;font-family:'JetBrains Mono',monospace;font-size:11px;color:var(--txt-dim);}
.hint-bar{display:flex;gap:8px;padding:12px 16px;background:var(--surface);backdrop-filter:blur(12px);border-top:1px solid var(--border);align-items:center;}
.hint-bar::before{content:'✦';margin-right:4px;color:var(--prob);font-size:16px;}
#hint-input{flex:1;background:rgba(0,0,0,0.4);border:1px solid var(--border);border-radius:6px;padding:8px 12px;color:var(--txt);font-family:'JetBrains Mono',monospace;font-size:13px;outline:none;transition:all 0.3s;}
#hint-input:focus{border-color:var(--prob);box-shadow:0 0 0 2px rgba(139,92,246,0.2);}
#hint-btn{padding:8px 16px;background:var(--prob);color:#fff;border:none;border-radius:6px;cursor:pointer;font-weight:500;transition:all 0.2s;font-size:13px;}
#hint-btn:hover{background:rgba(139,92,246,0.8);transform:scale(0.98);}
#hint-sent{margin-left:8px;font-size:12px;color:var(--emerald);opacity:0;transition:opacity 0.3s;}
#confetti-layer{position:fixed;inset:0;z-index:9999;pointer-events:none;}
.confetti{position:absolute;width:8px;height:8px;border-radius:50%;}
</style>
</head>
<body>
<canvas id="bg"></canvas>
<div class="app">
  <header>
    <span id="h-logo">BINGO</span>
    <span id="h-dot"></span>
    <span id="h-target">—</span>
    <span id="h-lnum">0</span>
    <span id="h-ws">●</span>
  </header>
  <main class="grid">
    <section class="panel left-panel">
      <div class="panel-title">Findings</div>
      <div class="tabs">
        <div class="tab active" onclick="switchTab(this,'conf')">Confirmed <span id="n-conf">0</span></div>
        <div class="tab" onclick="switchTab(this,'prob')">Probable <span id="n-prob">0</span></div>
        <div class="tab" onclick="switchTab(this,'pot')">Possible <span id="n-pot">0</span></div>
      </div>
      <div id="list-conf" class="find-list active"></div>
      <div id="list-prob" class="find-list"></div>
      <div id="list-pot" class="find-list"></div>
    </section>
    <section class="panel center-panel">
      <div id="stream-header">
        <div class="panel-title" style="margin:0;">Live Activity</div>
        <button id="scroll-pin">⏬ AUTO</button>
      </div>
      <div id="stream-body"></div>
    </section>
    <section class="panel right-panel">
      <div class="panel-title">Statistics</div>
      <div class="stat-ring">
        <div class="ring-wrap">
          <svg width="80" height="80"><circle class="ring-bg" cx="40" cy="40" r="18"/><circle id="ring-conf" class="ring-fill conf" cx="40" cy="40" r="18" stroke-dasharray="113.1" stroke-dashoffset="113.1"/></svg>
          <div class="ring-label" id="sn-conf">0</div>
        </div>
        <div class="ring-name">Confirmed</div>
      </div>
      <div class="stat-ring">
        <div class="ring-wrap">
          <svg width="80" height="80"><circle class="ring-bg" cx="40" cy="40" r="18"/><circle id="ring-prob" class="ring-fill prob" cx="40" cy="40" r="18" stroke-dasharray="113.1" stroke-dashoffset="113.1"/></svg>
          <div class="ring-label" id="sn-prob">0</div>
        </div>
        <div class="ring-name">Probable</div>
      </div>
      <div class="stat-ring">
        <div class="ring-wrap">
          <svg width="80" height="80"><circle class="ring-bg" cx="40" cy="40" r="18"/><circle id="ring-pot" class="ring-fill pot" cx="40" cy="40" r="18" stroke-dasharray="113.1" stroke-dashoffset="113.1"/></svg>
          <div class="ring-label" id="sn-pot">0</div>
        </div>
        <div class="ring-name">Possible</div>
      </div>
      <div class="stat-ring">
        <div class="ring-wrap">
          <svg width="80" height="80"><circle class="ring-bg" cx="40" cy="40" r="18"/><circle id="ring-blk" class="ring-fill blk" cx="40" cy="40" r="18" stroke-dasharray="113.1" stroke-dashoffset="113.1"/></svg>
          <div class="ring-label" id="sn-blk">0</div>
        </div>
        <div class="ring-name">Blocked</div>
      </div>
      <div id="elapsed">00:00</div>
      <div class="panel-title" style="margin-top:20px;">Domains <span id="n-dom">0</span></div>
      <div id="domain-list"></div>
    </section>
  </main>
  <div class="hint-bar">
    <input id="hint-input" placeholder="Inject hint or guidance...">
    <button id="hint-btn">Send</button>
    <span id="hint-sent">✓ Sent</span>
  </div>
</div>
<div id="confetti-layer"></div>
<script>
const $=id=>document.getElementById(id);
let ws,autoScroll=true,cnts={conf:0,prob:0,pot:0,blk:0},domains=new Set(),startTime=Date.now();

// Canvas particles
const canvas=$('bg'),ctx=canvas.getContext('2d');
canvas.width=window.innerWidth;canvas.height=window.innerHeight;
const particles=Array.from({length:70},()=>({x:Math.random()*canvas.width,y:Math.random()*canvas.height,vx:(Math.random()-0.5)*0.4,vy:(Math.random()-0.5)*0.4,r:1+Math.random()*2}));
let burstParticles=[];
function drawParticles(){
  ctx.clearRect(0,0,canvas.width,canvas.height);
  particles.forEach(p=>{
    p.x+=p.vx;p.y+=p.vy;
    if(p.x<0||p.x>canvas.width)p.vx*=-1;
    if(p.y<0||p.y>canvas.height)p.vy*=-1;
    ctx.fillStyle='rgba(167,139,250,0.4)';
    ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill();
  });
  particles.forEach((p,i)=>{
    particles.slice(i+1).forEach(q=>{
      const dx=q.x-p.x,dy=q.y-p.y,d=Math.sqrt(dx*dx+dy*dy);
      if(d<120){
        ctx.strokeStyle=`rgba(167,139,250,${0.15*(1-d/120)})`;
        ctx.lineWidth=0.5;
        ctx.beginPath();ctx.moveTo(p.x,p.y);ctx.lineTo(q.x,q.y);ctx.stroke();
      }
    });
  });
  burstParticles=burstParticles.filter(b=>{
    b.y+=b.vy;b.vy+=0.4;b.life--;
    if(b.life<=0)return false;
    ctx.fillStyle=b.color;
    ctx.beginPath();ctx.arc(b.x,b.y,3,0,Math.PI*2);ctx.fill();
    return true;
  });
  requestAnimationFrame(drawParticles);
}
drawParticles();
window.addEventListener('resize',()=>{canvas.width=window.innerWidth;canvas.height=window.innerHeight;});

function burstConfetti(){
  const layer=$('confetti-layer');
  const panel=document.querySelector('.left-panel');
  const pr=panel?panel.getBoundingClientRect():{left:0,top:0,width:300,height:400};
  const ox=pr.left+Math.min(pr.width*0.6,250);
  const oy=pr.top+Math.min(pr.height*0.35,180);
  const colors=['#f59e0b','#8b5cf6','#38bdf8'];
  for(let i=0;i<30;i++){
    const span=document.createElement('span');
    span.className='confetti';
    span.style.left=ox+'px';
    span.style.top=oy+'px';
    span.style.background=colors[Math.floor(Math.random()*colors.length)];
    const dx=(Math.random()-0.5)*400;
    const dy=-100-Math.random()*200;
    const rot=(Math.random()-0.5)*720;
    span.style.animation=`confettiFly 1.2s ease-in forwards`;
    span.style.setProperty('--dx',dx+'px');
    span.style.setProperty('--dy',dy+'px');
    span.style.setProperty('--rot',rot+'deg');
    layer.appendChild(span);
    setTimeout(()=>span.remove(),1200);
  }
  for(let i=0;i<18;i++){
    burstParticles.push({x:300,y:200,vy:-3-Math.random()*5,life:60,color:'#f59e0b'});
  }
}
const style=document.createElement('style');
style.textContent='@keyframes confettiFly{0%{transform:translate(0,0) rotate(0deg);opacity:1;}100%{transform:translate(var(--dx),300px) rotate(var(--rot));opacity:0;}}';
document.head.appendChild(style);

function switchTab(el,name){
  document.querySelectorAll('.tab').forEach(t=>t.classList.remove('active'));
  document.querySelectorAll('.find-list').forEach(l=>l.classList.remove('active'));
  el.classList.add('active');
  $('list-'+name).classList.add('active');
}

function connect(){
  const wsUrl='ws://'+location.host+'/ws';
  ws=new WebSocket(wsUrl);
  ws.onopen=()=>{
    $('h-ws').textContent='● ON';$('h-ws').style.color='var(--emerald)';
    cnts={conf:0,prob:0,pot:0,blk:0};
    domains=new Set();
    ['list-conf','list-prob','list-pot'].forEach(id=>{$(id).innerHTML='';});
    $('domain-list').innerHTML='';
    refreshCounts();
  };
  ws.onerror=()=>{$('h-ws').textContent='● ERR';$('h-ws').style.color='var(--rose)';};
  ws.onclose=(e)=>{$('h-ws').textContent='● OFF';$('h-ws').style.color='var(--rose)';setTimeout(connect,2000);};
  ws.onmessage=e=>route(JSON.parse(e.data));
}
connect();

function route(msg){
  const d=msg.data||{};
  if(msg.type==='stream_chunk')addStream('chunk',d.text||'');
  else if(msg.type==='tool_result'){
    const label=d.name?('['+d.name+'] '):'';
    const body=d.error||d.preview||'(empty)';
    addStream('tool',label+body);
  }
  else if(msg.type==='finding'){addFinding(d);if(d.confidence==='confirmed')burstConfetti();}
  else if(msg.type==='stats')updateStats(d);
  else if(msg.type==='loop_start'){
    if(typeof d.loop==='number')$('h-lnum').textContent=d.loop;
    if(d.target)$('h-target').textContent=d.target.replace('https://','').replace('http://','').slice(0,50);
  }
  else if(msg.type==='hal_event'){
    const reason=d.reason||'unknown';
    const txt=d.blocked?('🚫 HAL blocked: '+reason):('⚠ HAL warned: '+reason);
    addStream('hal',txt);
    if(d.blocked){cnts.blk++;refreshCounts();}
  }
  else if(msg.type==='depth_nudge'){
    addStream('nudge','🔍 Depth nudge — '+(d.vuln_type||'finding')+' (loop '+(d.loop||'?')+')');
  }
  else if(msg.type==='session_done'){
    addStream('done','✅ Done — confirmed:'+(d.confirmed||0)+' probable:'+(d.probable||0)+' potential:'+(d.potential||0));
    updateStats(d);
  }
}

function addStream(cls,text){
  const b=$('stream-body');
  // Accumulate consecutive chunk tokens into the same line
  if(cls==='chunk'){
    const last=b.lastElementChild;
    if(last&&last.classList.contains('chunk')){
      last.textContent+=text;
      if(autoScroll)b.scrollTop=b.scrollHeight;
      return;
    }
  }
  const el=document.createElement('div');
  el.className='stream-entry '+cls;
  el.textContent=text;
  b.appendChild(el);
  if(b.children.length>2000)b.removeChild(b.firstChild);
  if(autoScroll)b.scrollTop=b.scrollHeight;
}

$('scroll-pin').onclick=()=>{
  autoScroll=!autoScroll;
  $('scroll-pin').textContent=autoScroll?'⏬ AUTO':'⏫ MANUAL';
  if(autoScroll)$('stream-body').scrollTop=$('stream-body').scrollHeight;
};
$('stream-body').onscroll=()=>{
  const b=$('stream-body');
  if(b.scrollTop+b.clientHeight<b.scrollHeight-30)autoScroll=false;
};

function addFinding(d){
  const conf=d.confidence||'potential';
  const cls=conf==='confirmed'?'conf':conf==='probable'?'prob':'pot';
  const list=$('list-'+cls);
  const card=document.createElement('div');
  card.className='card '+cls;
  card.innerHTML='<div class="card-top"><span class="card-type">'+esc(d.vuln_type||'unknown')+'</span><span class="card-conf-badge">'+conf.toUpperCase()+'</span></div>'
    +'<div class="card-url">'+esc((d.target||'').replace('https://','').replace('http://','').slice(0,60))+'</div>'
    +(d.payload?'<div class="card-payload">'+esc(d.payload.slice(0,80))+'</div>':'')
    +(d.evidence?'<div class="card-ev">'+esc(d.evidence.slice(0,400))+'</div>':'');
  card.onclick=()=>card.classList.toggle('open');
  list.prepend(card);
  cnts[cls]++;
  refreshCounts();
  if(d.target){
    $('h-target').textContent=d.target.replace('https://','').replace('http://','').slice(0,50);
    try{domains.add(new URL(d.target).hostname);}catch(e){}
    renderDomains();
  }
}

function updateStats(d){
  if(d.target)$('h-target').textContent=d.target.replace('https://','').replace('http://','').slice(0,50);
  if(typeof d.loop==='number')$('h-lnum').textContent=d.loop;
  if(typeof d.confirmed==='number')cnts.conf=d.confirmed;
  if(typeof d.probable==='number')cnts.prob=d.probable;
  if(typeof d.potential==='number')cnts.pot=d.potential;
  if(typeof d.blocked==='number')cnts.blk=d.blocked;
  refreshCounts();
}

function refreshCounts(){
  const total=cnts.conf+cnts.prob+cnts.pot;
  const max=Math.max(total,cnts.blk,1);
  $('n-conf').textContent=cnts.conf;
  $('n-prob').textContent=cnts.prob;
  $('n-pot').textContent=cnts.pot;
  $('sn-conf').textContent=cnts.conf;
  $('sn-prob').textContent=cnts.prob;
  $('sn-pot').textContent=cnts.pot;
  $('sn-blk').textContent=cnts.blk;
  const circ=113.1;
  $('ring-conf').style.strokeDashoffset=circ-(cnts.conf/max*circ);
  $('ring-prob').style.strokeDashoffset=circ-(cnts.prob/max*circ);
  $('ring-pot').style.strokeDashoffset=circ-(cnts.pot/max*circ);
  $('ring-blk').style.strokeDashoffset=circ-(cnts.blk/max*circ);
}

function renderDomains(){
  const dl=$('domain-list');
  dl.innerHTML='';
  $('n-dom').textContent=domains.size;
  [...domains].slice(0,30).forEach(d=>{
    const el=document.createElement('div');
    el.className='domain-item';
    el.textContent=d;
    dl.appendChild(el);
  });
}

function esc(s){
  return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
}

$('hint-btn').onclick=sendHint;
$('hint-input').onkeydown=e=>{if(e.key==='Enter')sendHint();};
function sendHint(){
  const v=$('hint-input').value.trim();
  if(!v)return;
  fetch('/api/hint',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({text:v})})
    .then(()=>{
      $('hint-input').value='';
      $('hint-sent').style.opacity='1';
      setTimeout(()=>$('hint-sent').style.opacity='0',2000);
      addStream('nudge','💉 Hint injected: '+v.slice(0,60));
    }).catch(()=>{});
}

fetch('/api/findings').then(r=>r.json()).then(findings=>{findings.forEach(addFinding);}).catch(()=>{});

setInterval(()=>{
  const sec=Math.floor((Date.now()-startTime)/1000);
  const m=Math.floor(sec/60),s=sec%60;
  $('elapsed').textContent=(m<10?'0':'')+m+':'+(s<10?'0':'')+s;
},1000);
</script>
</body>
</html>

"""


# ── FastAPI app ───────────────────────────────────────────────────────────────

def _make_app(event_bus: "EventBus"):
    from fastapi import FastAPI, WebSocket, WebSocketDisconnect
    from fastapi.responses import HTMLResponse, JSONResponse
    from fastapi.middleware.cors import CORSMiddleware
    from pydantic import BaseModel

    app = FastAPI(docs_url=None, redoc_url=None)
    # Starlette 1.2+ added WebSocket CSRF origin checks — allow all origins
    # so the browser can connect from any host/port (local pentest tool, not a public API)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/")
    async def index():
        return HTMLResponse(_HTML)

    @app.get("/api/findings")
    async def get_findings():
        return JSONResponse(event_bus.get_findings())

    @app.get("/api/stats")
    async def get_stats():
        return JSONResponse(event_bus.get_stats())

    class HintBody(BaseModel):
        text: str

    @app.post("/api/hint")
    async def post_hint(body: HintBody):
        event_bus.push_hint(body.text.strip())
        return {"ok": True}

    # Use add_websocket_route (plain Starlette WebSocketRoute) instead of
    # @app.websocket() to bypass FastAPI's APIWebSocketRoute dependency-injection
    # layer, which throws WebSocketRequestValidationError → code=1008 → uvicorn 403
    # when there are no declared dependencies but the FastAPI dep-solver still runs.
    async def ws_endpoint(websocket: WebSocket):
        import asyncio, json as _j, time as _t
        try:
            await websocket.accept()
        except Exception:
            return
        q = event_bus.subscribe()
        last_ping = _t.monotonic()
        try:
            # Replay existing state to newly connected client
            for f in event_bus.get_findings():
                await websocket.send_text(_j.dumps({"type": "finding", "data": f}))
            s = event_bus.get_stats()
            if s:
                await websocket.send_text(_j.dumps({"type": "stats", "data": s}))
            while True:
                try:
                    msg = q.get_nowait()
                    await websocket.send_text(msg)
                    last_ping = _t.monotonic()
                except queue.Empty:
                    await asyncio.sleep(0.02)
                    # Heartbeat every 5 s: keeps proxies/browsers from dropping idle WS
                    if _t.monotonic() - last_ping > 5:
                        await websocket.send_text(_j.dumps({"type": "ping"}))
                        last_ping = _t.monotonic()
        except Exception:
            # Catch ALL disconnect/reset variants, not only WebSocketDisconnect,
            # so the finally-unsubscribe always runs and the loop never dies silently.
            pass
        finally:
            event_bus.unsubscribe(q)

    # app.router is the plain Starlette Router — add_websocket_route here
    # registers a raw WebSocketRoute, no FastAPI dep-injection
    app.router.add_websocket_route("/ws", ws_endpoint)
    return app


# ── Server start ──────────────────────────────────────────────────────────────

def start_web_server(event_bus: "EventBus") -> int:
    """Start uvicorn in a daemon thread. Returns the bound port."""
    port = _find_free_port(17890)
    host = "0.0.0.0"  # 0.0.0.0 lets WSL2 Windows browser reach via localhost

    app = _make_app(event_bus)

    def _run():
        import uvicorn
        uvicorn.run(app, host=host, port=port, log_level="error", access_log=False)

    t = threading.Thread(target=_run, daemon=True)
    t.start()

    import time; time.sleep(0.8)  # wait for bind
    return port
