import{n as e}from"./ordinal-d3qmLxvs.js";import{n as t}from"./path-CA7JeXbM.js";import{p as n}from"./math-DKrkx0go.js";import{t as r}from"./arc-BNgZxx4h.js";import{t as i}from"./array-xS8TccZC.js";import{Ci as a,Fi as o,Li as s,Lr as c,Pi as l,Qn as u,Xi as d,Yi as f,_i as p,bi as m,mi as h,rr as g,wi as _,xi as v,yi as y}from"./index-DyCK0vtI.js";import{t as b}from"./chunk-4BX2VUAB-DEx_QEwp.js";import{t as x}from"./mermaid-parser.core-BLQn6l-D.js";function S(e,t){return t<e?-1:t>e?1:t>=e?0:NaN}function C(e){return e}function w(){var e=C,r=S,a=null,o=t(0),s=t(n),c=t(0);function l(t){var l,u=(t=i(t)).length,d,f,p=0,m=Array(u),h=Array(u),g=+o.apply(this,arguments),_=Math.min(n,Math.max(-n,s.apply(this,arguments)-g)),v,y=Math.min(Math.abs(_)/u,c.apply(this,arguments)),b=y*(_<0?-1:1),x;for(l=0;l<u;++l)(x=h[m[l]=l]=+e(t[l],l,t))>0&&(p+=x);for(r==null?a!=null&&m.sort(function(e,n){return a(t[e],t[n])}):m.sort(function(e,t){return r(h[e],h[t])}),l=0,f=p?(_-u*b)/p:0;l<u;++l,g=v)d=m[l],x=h[d],v=g+(x>0?x*f:0)+b,h[d]={data:t[d],index:l,value:x,startAngle:g,endAngle:v,padAngle:y};return h}return l.value=function(n){return arguments.length?(e=typeof n==`function`?n:t(+n),l):e},l.sortValues=function(e){return arguments.length?(r=e,a=null,l):r},l.sort=function(e){return arguments.length?(a=e,r=null,l):a},l.startAngle=function(e){return arguments.length?(o=typeof e==`function`?e:t(+e),l):o},l.endAngle=function(e){return arguments.length?(s=typeof e==`function`?e:t(+e),l):s},l.padAngle=function(e){return arguments.length?(c=typeof e==`function`?e:t(+e),l):c},l}var T=y.pie,E={sections:new Map,showData:!1,config:T},D=E.sections,O=E.showData,k=structuredClone(T),A={getConfig:f(()=>structuredClone(k),`getConfig`),clear:f(()=>{D=new Map,O=E.showData,h()},`clear`),setDiagramTitle:s,getDiagramTitle:_,setAccTitle:o,getAccTitle:v,setAccDescription:l,getAccDescription:m,addSection:f(({label:e,value:t})=>{if(t<0)throw Error(`"${e}" has invalid value: ${t}. Negative values are not allowed in pie charts. All slice values must be >= 0.`);D.has(e)||(D.set(e,t),d.debug(`added new section: ${e}, with value: ${t}`))},`addSection`),getSections:f(()=>D,`getSections`),setShowData:f(e=>{O=e},`setShowData`),getShowData:f(()=>O,`getShowData`)},j=f((e,t)=>{b(e,t),t.setShowData(e.showData),e.sections.map(t.addSection)},`populateDb`),M={parse:f(async e=>{let t=await x(`pie`,e);d.debug(t),j(t,A)},`parse`)},N=f(e=>`
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
`,`getStyles`),P=f(e=>{let t=[...e.values()].reduce((e,t)=>e+t,0),n=[...e.entries()].map(([e,t])=>({label:e,value:t})).filter(e=>e.value/t*100>=1);return w().value(e=>e.value).sort(null)(n)},`createPieArcs`),F={parser:M,db:A,renderer:{draw:f((t,n,i,o)=>{d.debug(`rendering pie chart
`+t);let s=o.db,l=a(),f=u(s.getConfig(),l.pie),m=c(n),h=m.append(`g`);h.attr(`transform`,`translate(225,225)`);let{themeVariables:_}=l,[v]=g(_.pieOuterStrokeWidth);v??=2;let y=f.textPosition,b=r().innerRadius(0).outerRadius(185),x=r().innerRadius(185*y).outerRadius(185*y);h.append(`circle`).attr(`cx`,0).attr(`cy`,0).attr(`r`,185+v/2).attr(`class`,`pieOuterCircle`);let S=s.getSections(),C=P(S),w=[_.pie1,_.pie2,_.pie3,_.pie4,_.pie5,_.pie6,_.pie7,_.pie8,_.pie9,_.pie10,_.pie11,_.pie12],T=0;S.forEach(e=>{T+=e});let E=C.filter(e=>(e.data.value/T*100).toFixed(0)!==`0`),D=e(w).domain([...S.keys()]);h.selectAll(`mySlices`).data(E).enter().append(`path`).attr(`d`,b).attr(`fill`,e=>D(e.data.label)).attr(`class`,`pieCircle`),h.selectAll(`mySlices`).data(E).enter().append(`text`).text(e=>(e.data.value/T*100).toFixed(0)+`%`).attr(`transform`,e=>`translate(`+x.centroid(e)+`)`).style(`text-anchor`,`middle`).attr(`class`,`slice`);let O=h.append(`text`).text(s.getDiagramTitle()).attr(`x`,0).attr(`y`,-400/2).attr(`class`,`pieTitleText`),k=[...S.entries()].map(([e,t])=>({label:e,value:t})),A=h.selectAll(`.legend`).data(k).enter().append(`g`).attr(`class`,`legend`).attr(`transform`,(e,t)=>{let n=22*k.length/2;return`translate(216,`+(t*22-n)+`)`});A.append(`rect`).attr(`width`,18).attr(`height`,18).style(`fill`,e=>D(e.label)).style(`stroke`,e=>D(e.label)),A.append(`text`).attr(`x`,22).attr(`y`,14).text(e=>s.getShowData()?`${e.label} [${e.value}]`:e.label);let j=512+Math.max(...A.selectAll(`text`).nodes().map(e=>e?.getBoundingClientRect().width??0)),M=O.node()?.getBoundingClientRect().width??0,N=450/2-M/2,F=450/2+M/2,I=Math.min(0,N),L=Math.max(j,F)-I;m.attr(`viewBox`,`${I} 0 ${L} 450`),p(m,450,L,f.useMaxWidth)},`draw`)},styles:N};export{F as diagram};