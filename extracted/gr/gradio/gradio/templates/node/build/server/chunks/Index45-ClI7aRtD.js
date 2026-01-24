import { e as escape_html } from './async-Mo2Ia14K.js';
import { a as attr } from './index-D1Ptw7Az.js';
import { B as B$1, g } from './2-B89dC7Mi.js';
import './index5-BoOEKc6P.js';
import './dev-fallback-Bc5Ork7Y.js';
import 'path';
import 'url';
import 'fs';
import './spring-DE8vsW2o.js';

function B(o,t){o.component(a=>{let{elem_id:d="",elem_classes:u=[],visible:n=true,variant:i="secondary",size:c="lg",value:e,icon:m,disabled:f=false,scale:_=null,min_width:v=void 0,on_click:b,children:h}=t;function w(){if(b?.(),!e?.url)return;let s;if(!e.orig_name&&e.url){const r=e.url.split("/");s=r[r.length-1],s=s.split("?")[0].split("#")[0];}else s=e.orig_name;const l=document.createElement("a");l.href=e.url,l.download=s||"file",document.body.appendChild(l),l.click(),document.body.removeChild(l);}B$1(a,{size:c,variant:i,elem_id:d,elem_classes:u,visible:n,onclick:w,scale:_,min_width:v,disabled:f,children:s$1=>{m?(s$1.push("<!--[-->"),s$1.push(`<img class="button-icon svelte-4ac0fl"${attr("src",m.url)}${attr("alt",`${e} icon`)}/>`)):s$1.push("<!--[!-->"),s$1.push("<!--]--> "),h?(s$1.push("<!--[-->"),h(s$1),s$1.push("<!---->")):s$1.push("<!--[!-->"),s$1.push("<!--]-->");}});});}function D(o,t){o.component(a=>{const{$$slots:d,$$events:u,...n}=t,i=new g(n);B(a,{value:i.props.value,variant:i.props.variant,elem_id:i.shared.elem_id,elem_classes:i.shared.elem_classes,size:i.props.size,scale:i.shared.scale,icon:i.props.icon,min_width:i.shared.min_width,visible:i.shared.visible,disabled:!i.shared.interactive,on_click:()=>i.dispatch("click"),children:c=>{c.push(`<!---->${escape_html(i.shared.label??"")}`);}});});}

export { B as BaseButton, D as default };
//# sourceMappingURL=Index45-ClI7aRtD.js.map
