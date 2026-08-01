import{j as n,L as T,m as I,n as L,R as m,o as w,D as _,q as H,t as B,s as M,v as V,w as z,x as G,y as f,C as O,z as K,A as N,B as U,E as W,F as X,G as Y,H as Z,I as q,S as J}from"./index-Dc58E4ij.js";import{r as h,B as Q,X as tt,Y as et,T as st,a as nt}from"./recharts-BXZtEhpB.js";import"./plotly-CrTaWLEP.js";const at=f.div`
  overflow-y: hidden;
  overflow-x: auto;
  width: 100%;
  flex: 1;

  ${G}
`,ot=200,rt=({title:e,count:t})=>n.jsxs(O,{children:[n.jsx(K,{children:e}),"Count: ",t]}),it=(e,t)=>class extends h.PureComponent{render(){const{x:o,y:a,payload:d,fill:x}=this.props,r=d.value;return n.jsx("g",{transform:`translate(${o},${a})`,children:n.jsx("text",{x:0,y:0,dy:16,textAnchor:"end",fill:x,transform:"rotate(-80)",children:e&&typeof r!="string"?N(r,t):U(r)?r.toFixed(3):r.length>24?r.slice(0,21)+"...":r})})}},lt=f.div`
  font-weight: bold;
  font-size: 1rem;
  line-height: 2rem;
  margin-left: 1rem;
`,ct=e=>{const t=[];for(let s=0;s<e.length;s+=Math.max(Math.floor(e.length/4),1))t.push(e[s].key);return t},dt=e=>{const t=m(z(e));switch(t.__typename){case"BoolCountValuesResponse":return{data:t.values.map(({value:s,bool:o})=>({key:o,count:s,ticks:null})),ticks:null};case"DatetimeHistogramValuesResponse":return v(t.counts,t.datetimes);case"FloatHistogramValuesResponse":return v(t.counts,t.floats);case"IntHistogramValuesResponse":return v(t.counts,t.ints);case"StrCountValuesResponse":return{data:t.values.map(({value:s,str:o})=>({key:o,count:s})),ticks:null};default:throw new Error("invalid")}},v=(e,t)=>{if(e.length<2)return{data:[],ticks:null};const s=e.map((o,a)=>({count:o,key:(t[a+1]-t[a])/2+t[a],edges:[t[a],t[a+1]]}));return{data:s,ticks:ct(s)}},ut=({path:e})=>{const[t,{height:s}]=I(),o=L(),{data:a,ticks:d}=dt(e),x=a.length>=ot,r=24,g=o.text.secondary,C=g,p=m(w({path:e,ftype:_})),u=m(w({path:e,ftype:H})),b=m(B),S=a.map(({key:l,...i})=>({...i,key:p||u?l:M(l)})),y=S.reduce((l,i)=>({...l,[i.key]:i.edges}),{}),F=it(p||u,u?"UTC":b),$=d===null?{interval:0}:{ticks:d};return h.useLayoutEffect(()=>{document.getElementById(`histogram-${e}`)?.dispatchEvent(new CustomEvent(`histogram-${e}`,{bubbles:!0}))},[e,t]),a.length?n.jsxs(at,{id:`histogram-${e}`,ref:t,children:[x&&n.jsx(lt,{children:`First ${a?.length} results`}),n.jsx("div",{style:{display:"flex",justifyContent:"center"},children:n.jsxs(Q,{height:s-37,width:a.length*(r+4)+50,barCategoryGap:"4px",data:S,margin:{top:0,left:0,bottom:5,right:5},children:[n.jsx(tt,{dataKey:"key",height:.2*s,axisLine:!1,tick:n.jsx(F,{fill:C}),tickLine:{stroke:g},...$}),n.jsx(et,{dataKey:"count",axisLine:!1,tick:{fill:C},tickLine:{stroke:g}}),n.jsx(st,{cursor:!1,content:l=>{const i=l?.payload[0]?.payload?.key,D=l?.payload[0]?.payload?.count;if(typeof D!="number")return null;let j=`Value: ${i}`;if(y[i])if(p||u){const[c,P]=y[i],{common:A,diff:E}=V(u?"UTC":b,c,P);let k=E.formatRange(c,P);E.resolvedOptions().fractionalSecondDigits===3&&(k=k.replaceAll(",",".")),j=`Range: ${A?A.format(c):""} ${k}`}else j=`Range: [${y[i].map(c=>Number.isInteger(c)?c:c.toFixed(3)).join(", ")})`;return n.jsx(rt,{title:j,count:D})},contentStyle:{background:"hsl(210, 20%, 23%)",borderColor:"rgb(255, 109, 4)"}}),n.jsx(nt,{dataKey:"count",fill:"rgb(255, 109, 4)",barCategoryGap:0,barSize:r,isAnimationActive:!1})]})})]}):n.jsx(T,{children:"No Data"})},mt=({path:e})=>n.jsx(h.Suspense,{fallback:n.jsx(T,{ellipsisAnimation:!0,children:"Loading"}),children:n.jsx(ut,{path:e},e)}),ht=f.div`
  position: relative;
  display: flex;
  flex-direction: column;
  height: 100%;
  width: 100%;
  max-height: 100%;
  overflow-x: auto;
  overflow-y: hidden;
`,ft=f.div`
  display: flex;
  gap: 1rem;
  margin: 1rem;
`;function R(){const e=m(Z),[t,s]=q("path",e[0]);return h.useEffect(()=>{e.includes(t)||s(e[0])},[t,e,s]),{path:t,setPath:s,paths:e}}const xt=()=>{const{path:e,setPath:t,paths:s}=R();return n.jsx(J,{component:({value:o})=>n.jsx(n.Fragment,{children:o}),containerStyle:{position:"relative"},onSelect:t,overflow:!0,resultsPlacement:"bottom-start",placeholder:"Select field",useSearch:o=>({values:s.filter(d=>d.includes(o)),total:s.length}),value:e||"",cy:"histograms"})};function kt(){const[e,t]=W(),{path:s}=R();return h.useEffect(()=>{t(s)},[s]),n.jsxs(ht,{"data-cy":"histograms-container",children:[n.jsxs(ft,{children:[n.jsx(xt,{}),n.jsx(X,{place:Y.HISTOGRAM_ACTIONS})]}),s?n.jsx(mt,{path:s},s):n.jsx(T,{children:"Select a field"})]})}export{kt as default};
