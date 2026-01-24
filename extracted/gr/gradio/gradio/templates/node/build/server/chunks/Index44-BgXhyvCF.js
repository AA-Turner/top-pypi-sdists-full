import { e as escape_html } from './async-Mo2Ia14K.js';
import { b as spread_props, f as attr_class, d as attr_style, i as slot, c as bind_props } from './index-D1Ptw7Az.js';
import { g, c as G, a as U, d as b } from './2-B89dC7Mi.js';
import './index5-BoOEKc6P.js';
import './dev-fallback-Bc5Ork7Y.js';
import 'path';
import 'url';
import 'fs';
import './spring-DE8vsW2o.js';

function v(p,l){p.component(a=>{let{open:e=true,label:n="",onexpand:d,oncollapse:s$1}=l;a.push(`<button${attr_class("label-wrap svelte-e5lyqv",void 0,{open:e})}><span class="svelte-e5lyqv">${escape_html(n)}</span> <span class="icon svelte-e5lyqv"${attr_style("",{transform:e?"rotate(0)":"rotate(90deg)"})}>▼</span></button> <div${attr_style("",{display:e?"block":"none"})}><!--[-->`),slot(a,l,"default",{},null),a.push("<!--]--></div>"),bind_props(l,{open:e});});}function C(p,l){p.component(a=>{let{$$slots:e,$$events:n,...d}=l;const s$1=new g(d);let u=s$1.shared.label||"";G(a,{elem_id:s$1.shared.elem_id,elem_classes:s$1.shared.elem_classes,visible:s$1.shared.visible,children:o=>{s$1.shared.loading_status?(o.push("<!--[-->"),U(o,spread_props([{autoscroll:s$1.shared.autoscroll,i18n:s$1.i18n},s$1.shared.loading_status]))):o.push("<!--[!-->"),o.push("<!--]--> "),v(o,{label:u,open:s$1.props.open,onexpand:()=>{s$1.dispatch("expand"),s$1.dispatch("gradio_expand");},oncollapse:()=>s$1.dispatch("collapse"),children:c=>{b(c,{children:i=>{i.push("<!--[-->"),slot(i,l,"default",{},null),i.push("<!--]-->");},$$slots:{default:true}});},$$slots:{default:true}}),o.push("<!---->");},$$slots:{default:true}});});}

export { C as default };
//# sourceMappingURL=Index44-BgXhyvCF.js.map
