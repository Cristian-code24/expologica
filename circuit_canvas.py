"""Renderizador Canvas para circuitos lógicos interactivos en Streamlit."""

import json
from typing import Mapping

import streamlit.components.v1 as components

from boolean_logic import evaluate_gates


def render_circuit(
    circuit: Mapping[str, object],
    input_values: Mapping[str, int],
    autoplay: bool = False,
    height: int = 540,
) -> int:
    """Muestra el circuito animado y devuelve el valor de salida calculado."""
    variables = list(circuit["variables"])
    gates = list(circuit["gates"])
    output = str(circuit["output"])
    signals = evaluate_gates(input_values, gates)
    result = signals[output]
    payload = json.dumps(
        {
            "variables": variables,
            "inputs": dict(input_values),
            "gates": gates,
            "output": output,
            "expression": str(circuit.get("expression", "")),
            "autoplay": autoplay,
        },
        ensure_ascii=True,
    ).replace("</", "<\\/")
    component_html = _CANVAS_HTML.replace("__CIRCUIT_DATA__", payload)
    components.html(component_html, height=height, scrolling=False)
    return result


_CANVAS_HTML = r"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
* { box-sizing: border-box; }
html, body { margin: 0; width: 100%; background: transparent; color: #e7f2f7;
  font: 13px/1.4 Inter, ui-sans-serif, system-ui, -apple-system, "Segoe UI", sans-serif; }
.frame { border: 1px solid rgba(131, 175, 194, .17); border-radius: 18px;
  background: linear-gradient(145deg, rgba(13, 30, 43, .97), rgba(8, 18, 30, .98));
  overflow: hidden; box-shadow: 0 16px 48px rgba(0,0,0,.2); }
.topline { display:flex; align-items:center; justify-content:space-between; padding: 13px 17px 9px; }
.tag { color:#8da8b7; font-size:10px; text-transform:uppercase; letter-spacing:.16em; }
.expr { color:#e4f2f4; font-weight:650; letter-spacing:.025em; }
canvas { display:block; width:100%; height:470px; }
.legend { display:flex; gap:18px; padding:0 17px 13px; color:#91a9b5; font-size:10px; }
.dot { display:inline-block; width:7px; height:7px; border-radius:50%; margin-right:6px; }
.live { color:#7ee9cc; }
@media(max-width:600px) { canvas { height:390px; } .legend { gap:9px; font-size:9px; } }
</style>
</head>
<body>
<div class="frame">
  <div class="topline"><span class="tag">Simulación de circuito</span><span class="expr"></span></div>
  <canvas id="circuit"></canvas>
  <div class="legend"><span><i class="dot" style="background:#46e3c1"></i>señal 1</span>
    <span><i class="dot" style="background:#d6a86a"></i>señal 0</span>
    <span class="live" id="readout"></span></div>
</div>
<script>
(() => {
  const data = __CIRCUIT_DATA__;
  document.querySelector(".expr").textContent = "Flujo de señales 0/1";
  const canvas = document.getElementById("circuit");
  const ctx = canvas.getContext("2d");
  const W = 960, H = 500;
  const inputYs = data.variables.map((_, i) => 105 + i * (290 / Math.max(data.variables.length - 1, 1)));
  const values = {...data.inputs};
  const colors = {1:"#48e5c4", 0:"#d7a96d"};
  const signals = {};
  const gateValues = {};
  const gateFns = {
    NOT: a => 1-a, AND: (...a) => Number(a.every(Boolean)),
    OR: (...a) => Number(a.some(Boolean)), NAND: (...a) => 1-Number(a.every(Boolean)),
    NOR: (...a) => 1-Number(a.some(Boolean)), XOR: (...a) => a.reduce((x,y)=>x^y,0),
    XNOR: (...a) => 1-a.reduce((x,y)=>x^y,0)
  };
  const positions = {};
  data.variables.forEach((name, i) => positions[name] = {x:116, y:inputYs[i]});
  data.gates.forEach(g => positions[g.output] = {x:g.x+51, y:g.y});
  const wires = [];
  data.gates.forEach(g => g.inputs.forEach((source, i) => {
    const from = positions[source], pinY = g.y + (i-(g.inputs.length-1)/2)*27;
    const to = {x:g.x-47, y:pinY};
    const midX = Math.max(from.x+22, (from.x+to.x)/2);
    wires.push({source, points:[from, {x:midX,y:from.y}, {x:midX,y:to.y}, to]});
  }));
  const outY = 250, finalFrom = positions[data.output];
  wires.push({source:data.output, points:[finalFrom, {x:Math.max(finalFrom.x+25,865),y:finalFrom.y},
    {x:Math.max(finalFrom.x+25,865),y:outY}, {x:910,y:outY}]});
  function evaluate() {
    Object.assign(signals, values);
    data.gates.forEach(g => {
      signals[g.output] = gateFns[g.kind](...g.inputs.map(name => signals[name]));
      gateValues[g.id] = signals[g.output];
    });
  }
  function fit() {
    const rect = canvas.getBoundingClientRect(), dpr = Math.min(window.devicePixelRatio || 1, 2);
    canvas.width = Math.round(rect.width*dpr); canvas.height = Math.round(rect.height*dpr);
    ctx.setTransform(canvas.width/W, 0, 0, canvas.height/H, 0, 0);
  }
  function path(points) {
    ctx.beginPath(); ctx.moveTo(points[0].x, points[0].y);
    points.slice(1).forEach(p => ctx.lineTo(p.x,p.y));
  }
  function pointAt(points, progress) {
    const lengths = [], total = points.slice(1).reduce((sum,p,i) => {
      const a=points[i], len=Math.hypot(p.x-a.x,p.y-a.y); lengths.push(len); return sum+len;
    },0);
    let remaining = progress*total;
    for (let i=0;i<lengths.length;i++) {
      if (remaining <= lengths[i]) {
        const a=points[i], b=points[i+1], t=lengths[i] ? remaining/lengths[i] : 0;
        return {x:a.x+(b.x-a.x)*t,y:a.y+(b.y-a.y)*t};
      }
      remaining -= lengths[i];
    }
    return points[points.length-1];
  }
  function drawGate(g, time) {
    const v=signals[g.output], c=colors[v], x=g.x, y=g.y;
    const pulse=(Math.sin(time/155 + g.x*.03)+1)/2;
    g.inputs.forEach((source,i) => {
      const pinY=y+(i-(g.inputs.length-1)/2)*27;
      ctx.beginPath(); ctx.moveTo(x-47,pinY); ctx.lineTo(x-32,pinY);
      ctx.strokeStyle=colors[signals[source]]; ctx.lineWidth=2; ctx.stroke();
    });
    ctx.save(); ctx.shadowColor=c; ctx.shadowBlur=5+pulse*12;
    ctx.strokeStyle=c; ctx.fillStyle="rgba(13,31,43,.98)"; ctx.lineWidth=2;
    const kind=g.kind.replace(" ×3","");
    if (kind==="NOT") {
      ctx.beginPath(); ctx.moveTo(x-31,y-25); ctx.lineTo(x+20,y); ctx.lineTo(x-31,y+25); ctx.closePath();
      ctx.fill(); ctx.stroke();
      ctx.beginPath(); ctx.arc(x+26,y,6,0,Math.PI*2); ctx.fill(); ctx.stroke();
    } else if (kind==="AND" || kind==="NAND") {
      ctx.beginPath(); ctx.moveTo(x-32,y-28); ctx.lineTo(x,y-28);
      ctx.arc(x,y,28,-Math.PI/2,Math.PI/2); ctx.lineTo(x-32,y+28); ctx.closePath();
      ctx.fill(); ctx.stroke();
      if(kind==="NAND") { ctx.beginPath(); ctx.arc(x+35,y,5,0,Math.PI*2); ctx.fill(); ctx.stroke(); }
    } else {
      ctx.beginPath(); ctx.moveTo(x-32,y-28);
      ctx.quadraticCurveTo(x-6,y-28,x+5,y-20); ctx.quadraticCurveTo(x+20,y-12,x+31,y);
      ctx.quadraticCurveTo(x+20,y+12,x+5,y+20); ctx.quadraticCurveTo(x-6,y+28,x-32,y+28);
      ctx.quadraticCurveTo(x-11,y,x-32,y-28); ctx.closePath(); ctx.fill(); ctx.stroke();
      if(kind==="XOR" || kind==="XNOR") {
        ctx.beginPath(); ctx.moveTo(x-41,y-28); ctx.quadraticCurveTo(x-20,y,x-41,y+28); ctx.stroke();
      }
      if(kind==="NOR" || kind==="XNOR") { ctx.beginPath(); ctx.arc(x+37,y,5,0,Math.PI*2); ctx.fill(); ctx.stroke(); }
    }
    const outputStart=kind==="AND" ? 28 : kind==="NAND" ? 40 : kind==="NOR" || kind==="XNOR" ? 42 : kind==="NOT" ? 32 : 31;
    ctx.beginPath(); ctx.moveTo(x+outputStart,y); ctx.lineTo(x+51,y);
    ctx.strokeStyle=c; ctx.lineWidth=2; ctx.stroke();
    ctx.shadowBlur=0; ctx.fillStyle="#d8e9ee"; ctx.font="600 10px system-ui";
    ctx.textAlign="center"; ctx.textBaseline="middle"; ctx.fillText(g.label,x-4,y);
    ctx.restore();
  }
  function draw(time) {
    evaluate();
    ctx.clearRect(0,0,W,H);
    ctx.fillStyle="rgba(120,165,184,.07)";
    for(let x=28;x<W;x+=32) for(let y=22;y<H;y+=32) {ctx.beginPath();ctx.arc(x,y,.8,0,7);ctx.fill();}
    wires.forEach((wire, wi) => {
      const bit=signals[wire.source], color=colors[bit];
      path(wire.points); ctx.strokeStyle=bit ? "rgba(72,229,196,.35)" : "rgba(215,169,109,.27)";
      ctx.lineWidth=bit ? 2.3 : 1.7; ctx.shadowColor=color; ctx.shadowBlur=bit ? 8 : 3; ctx.stroke(); ctx.shadowBlur=0;
      for(let p=0;p<2;p++) {
        const progress=((time*.000085 + wi*.153 + p*.48)%1);
        const pt=pointAt(wire.points,progress);
        ctx.beginPath(); ctx.arc(pt.x,pt.y,9,0,Math.PI*2);
        ctx.fillStyle=bit ? "rgba(16,53,54,.96)" : "rgba(48,42,37,.96)";
        ctx.shadowColor=color; ctx.shadowBlur=10; ctx.fill(); ctx.shadowBlur=0;
        ctx.strokeStyle=color; ctx.lineWidth=1; ctx.stroke();
        ctx.fillStyle=color; ctx.font="700 10px ui-monospace,monospace";
        ctx.textAlign="center"; ctx.textBaseline="middle"; ctx.fillText(String(bit),pt.x,pt.y+.5);
      }
    });
    data.variables.forEach((name,i) => {
      const y=inputYs[i], bit=values[name];
      ctx.fillStyle="rgba(22,42,54,.95)"; ctx.strokeStyle=colors[bit]; ctx.lineWidth=1.5;
      ctx.beginPath(); ctx.roundRect(35,y-17,54,34,10); ctx.fill(); ctx.stroke();
      ctx.fillStyle="#9bb2bd"; ctx.font="600 11px system-ui"; ctx.textAlign="left"; ctx.fillText(name,45,y-1);
      ctx.fillStyle=colors[bit]; ctx.font="700 15px ui-monospace,monospace"; ctx.textAlign="right"; ctx.fillText(String(bit),79,y+1);
    });
    data.gates.forEach(g=>drawGate(g,time));
    const result=signals[data.output], color=colors[result];
    ctx.fillStyle="rgba(19,43,51,.98)"; ctx.strokeStyle=color; ctx.lineWidth=2;
    ctx.shadowColor=color; ctx.shadowBlur=13; ctx.beginPath(); ctx.roundRect(906,outY-21,42,42,12); ctx.fill(); ctx.stroke(); ctx.shadowBlur=0;
    ctx.fillStyle="#d4e5e9"; ctx.font="600 10px system-ui"; ctx.textAlign="center"; ctx.fillText("F",927,outY-8);
    ctx.fillStyle=color; ctx.font="700 17px ui-monospace,monospace"; ctx.fillText(String(result),927,outY+11);
    document.getElementById("readout").textContent="F = "+result+(data.autoplay ? " · reproducción activa" : "");
    requestAnimationFrame(draw);
  }
  let started=performance.now();
  if(data.autoplay) {
    const combinations=[];
    for(let n=0;n<Math.pow(2,data.variables.length);n++) {
      const row={};
      data.variables.forEach((name,i)=>row[name]=(n>>(data.variables.length-1-i))&1);
      combinations.push(row);
    }
    setInterval(()=>Object.assign(values,combinations[Math.floor((performance.now()-started)/1450)%combinations.length]),1450);
  }
  new ResizeObserver(fit).observe(canvas); fit(); requestAnimationFrame(draw);
})();
</script>
</body>
</html>"""

