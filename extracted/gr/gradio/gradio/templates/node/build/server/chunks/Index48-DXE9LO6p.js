import './async-Mo2Ia14K.js';
import { b as spread_props, f as attr_class, a as attr, d as attr_style, g as stringify, i as slot, c as bind_props } from './index-D1Ptw7Az.js';
import { g, a as U, d as b } from './2-B89dC7Mi.js';
import './index5-BoOEKc6P.js';
import './dev-fallback-Bc5Ork7Y.js';
import 'path';
import 'url';
import 'fs';
import './spring-DE8vsW2o.js';

function B(h,i){h.component(n=>{let {open:_=true,width:d,position:a="left",elem_classes:e=[],elem_id:r="",onexpand:u=()=>{},oncollapse:b=()=>{}}=i,o=false,g=typeof d=="number"?`${d}px`:d,f=false;let w=e?.join(" ")||"";n.push(`<div${attr_class(`sidebar ${stringify(w)}`,"svelte-1uruprb",{open:o,right:a==="right","reduce-motion":f})}${attr("id",r)}${attr_style(`width: ${stringify(g)}; ${stringify(a)}: calc(${stringify(g)} * -1)`)}><button class="toggle-button svelte-1uruprb" aria-label="Toggle Sidebar"><div class="chevron svelte-1uruprb"><span class="chevron-left svelte-1uruprb"></span></div></button> <div class="sidebar-content svelte-1uruprb"><!--[-->`),slot(n,i,"default",{},null),n.push("<!--]--></div></div>"),bind_props(i,{open:_,position:a});});}function T(h,i){h.component(n=>{const{$$slots:_,$$events:d,...a}=i,e=new g(a);let r=true,u;function b$1(o){U(o,spread_props([{autoscroll:e.shared.autoscroll,i18n:e.i18n},e.shared.loading_status])),o.push("<!----> "),e.shared.visible?(o.push("<!--[-->"),B(o,{width:e.props.width,onexpand:()=>e.dispatch("expand"),oncollapse:()=>e.dispatch("collapse"),elem_classes:e.shared.elem_classes,elem_id:e.shared.elem_id,get open(){return e.props.open},set open(s){e.props.open=s,r=false;},get position(){return e.props.position},set position(s){e.props.position=s,r=false;},children:s$1=>{b(s$1,{children:l=>{l.push("<!--[-->"),slot(l,i,"default",{},null),l.push("<!--]-->");},$$slots:{default:true}});},$$slots:{default:true}})):o.push("<!--[!-->"),o.push("<!--]-->");}do r=true,u=n.copy(),b$1(u);while(!r);n.subsume(u);});}

export { T as default };
//# sourceMappingURL=Index48-DXE9LO6p.js.map
