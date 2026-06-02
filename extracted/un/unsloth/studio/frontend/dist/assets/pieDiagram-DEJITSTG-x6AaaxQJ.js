import{n as e}from"./ordinal-d3qmLxvs.js";import{n as t}from"./path-CA7JeXbM.js";import{p as n}from"./math-DKrkx0go.js";import{t as r}from"./arc-BNgZxx4h.js";import{t as i}from"./array-xS8TccZC.js";import{Dr as a,Er as o,Hr as s,Qt as c,Vr as l,dr as u,fr as d,gr as f,hr as p,kn as m,kr as h,lr as g,or as _,pr as v,rn as y}from"./index-CsXMiQwf.js";import{t as b}from"./chunk-4BX2VUAB-BC0Dbbgo.js";import{t as x}from"./mermaid-parser.core-BHilnCTB.js";function S(e,t){return t<e?-1:t>e?1:t>=e?0:NaN}function C(e){return e}function w(){var e=C,r=S,a=null,o=t(0),s=t(n),c=t(0);function l(t){var l,u=(t=i(t)).length,d,f,p=0,m=Array(u),h=Array(u),g=+o.apply(this,arguments),_=Math.min(n,Math.max(-n,s.apply(this,arguments)-g)),v,y=Math.min(Math.abs(_)/u,c.apply(this,arguments)),b=y*(_<0?-1:1),x;for(l=0;l<u;++l)(x=h[m[l]=l]=+e(t[l],l,t))>0&&(p+=x);for(r==null?a!=null&&m.sort(function(e,n){return a(t[e],t[n])}):m.sort(function(e,t){return r(h[e],h[t])}),l=0,f=p?(_-u*b)/p:0;l<u;++l,g=v)d=m[l],x=h[d],v=g+(x>0?x*f:0)+b,h[d]={data:t[d],index:l,value:x,startAngle:g,endAngle:v,padAngle:y};return h}return l.value=function(n){return arguments.length?(e=typeof n==`function`?n:t(+n),l):e},l.sortValues=function(e){return arguments.length?(r=e,a=null,l):r},l.sort=function(e){return arguments.length?(a=e,r=null,l):a},l.startAngle=function(e){return arguments.length?(o=typeof e==`function`?e:t(+e),l):o},l.endAngle=function(e){return arguments.length?(s=typeof e==`function`?e:t(+e),l):s},l.padAngle=function(e){return arguments.length?(c=typeof e==`function`?e:t(+e),l):c},l}var T=u.pie,E={sections:new Map,showData:!1,config:T},D=E.sections,O=E.showData,k=structuredClone(T),A={getConfig:l(()=>structuredClone(k),`getConfig`),clear:l(()=>{D=new Map,O=E.showData,_()},`clear`),setDiagramTitle:h,getDiagramTitle:f,setAccTitle:a,getAccTitle:v,setAccDescription:o,getAccDescription:d,addSection:l(({label:e,value:t})=>{if(t<0)throw Error(`"${e}" has invalid value: ${t}. Negative values are not allowed in pie charts. All slice values must be >= 0.`);D.has(e)||(D.set(e,t),s.debug(`added new section: ${e}, with value: ${t}`))},`addSection`),getSections:l(()=>D,`getSections`),setShowData:l(e=>{O=e},`setShowData`),getShowData:l(()=>O,`getShowData`)},j=l((e,t)=>{b(e,t),t.setShowData(e.showData),e.sections.map(t.addSection)},`populateDb`),M={parse:l(async e=>{let t=await x(`pie`,e);s.debug(t),j(t,A)},`parse`)},N=l(e=>`
  .pieCircle{
    stroke: ${e.pieStrokeColor};
    stroke-width : ${e.pieStrokeWidth};
    opacity : ${e.pieOpacity};
  }
  .pieOuterCircle{
    stroke: ${e.pieOuterStrokeColor};
    stroke-width: ${e.pieOuterStrokeWidth};
    fill: none;
  }
  .pieTitleText {
    text-anchor: middle;
    font-size: ${e.pieTitleTextSize};
    fill: ${e.pieTitleTextColor};
    font-family: ${e.fontFamily};
  }
  .slice {
    font-family: ${e.fontFamily};
    fill: ${e.pieSectionTextColor};
    font-size:${e.pieSectionTextSize};
    // fill: white;
  }
  .legend text {
    fill: ${e.pieLegendTextColor};
    font-family: ${e.fontFamily};
    font-size: ${e.pieLegendTextSize};
  }
`,`getStyles`),P=l(e=>{let t=[...e.values()].reduce((e,t)=>e+t,0),n=[...e.entries()].map(([e,t])=>({label:e,value:t})).filter(e=>e.value/t*100>=1);return w().value(e=>e.value).sort(null)(n)},`createPieArcs`),F={parser:M,db:A,renderer:{draw:l((t,n,i,a)=>{s.debug(`rendering pie chart
`+t);let o=a.db,l=p(),u=c(o.getConfig(),l.pie),d=m(n),f=d.append(`g`);f.attr(`transform`,`translate(225,225)`);let{themeVariables:h}=l,[_]=y(h.pieOuterStrokeWidth);_??=2;let v=u.textPosition,b=r().innerRadius(0).outerRadius(185),x=r().innerRadius(185*v).outerRadius(185*v);f.append(`circle`).attr(`cx`,0).attr(`cy`,0).attr(`r`,185+_/2).attr(`class`,`pieOuterCircle`);let S=o.getSections(),C=P(S),w=[h.pie1,h.pie2,h.pie3,h.pie4,h.pie5,h.pie6,h.pie7,h.pie8,h.pie9,h.pie10,h.pie11,h.pie12],T=0;S.forEach(e=>{T+=e});let E=C.filter(e=>(e.data.value/T*100).toFixed(0)!==`0`),D=e(w).domain([...S.keys()]);f.selectAll(`mySlices`).data(E).enter().append(`path`).attr(`d`,b).attr(`fill`,e=>D(e.data.label)).attr(`class`,`pieCircle`),f.selectAll(`mySlices`).data(E).enter().append(`text`).text(e=>(e.data.value/T*100).toFixed(0)+`%`).attr(`transform`,e=>`translate(`+x.centroid(e)+`)`).style(`text-anchor`,`middle`).attr(`class`,`slice`);let O=f.append(`text`).text(o.getDiagramTitle()).attr(`x`,0).attr(`y`,-400/2).attr(`class`,`pieTitleText`),k=[...S.entries()].map(([e,t])=>({label:e,value:t})),A=f.selectAll(`.legend`).data(k).enter().append(`g`).attr(`class`,`legend`).attr(`transform`,(e,t)=>{let n=22*k.length/2;return`translate(216,`+(t*22-n)+`)`});A.append(`rect`).attr(`width`,18).attr(`height`,18).style(`fill`,e=>D(e.label)).style(`stroke`,e=>D(e.label)),A.append(`text`).attr(`x`,22).attr(`y`,14).text(e=>o.getShowData()?`${e.label} [${e.value}]`:e.label);let j=512+Math.max(...A.selectAll(`text`).nodes().map(e=>e?.getBoundingClientRect().width??0)),M=O.node()?.getBoundingClientRect().width??0,N=450/2-M/2,F=450/2+M/2,I=Math.min(0,N),L=Math.max(j,F)-I;d.attr(`viewBox`,`${I} 0 ${L} 450`),g(d,450,L,u.useMaxWidth)},`draw`)},styles:N};export{F as diagram};