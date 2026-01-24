import { e as escape_html } from './async-Mo2Ia14K.js';
import { a as attr, d as attr_style, c as bind_props, b as spread_props } from './index-D1Ptw7Az.js';
import { C as c, g, c as G, a as U } from './2-B89dC7Mi.js';
import { s } from './tinycolor-DfhFic3A.js';
export { default as BaseExample } from './Example14-vkLMcQAb.js';
import './index5-BoOEKc6P.js';
import './dev-fallback-Bc5Ork7Y.js';
import 'path';
import 'url';
import 'fs';
import './spring-DE8vsW2o.js';

function w(e,a){return s(e).toHexString()}function B(e,a){e.component(t=>{let{value:i=void 0,label:c$1,info:u,disabled:o,show_label:p,on_input:r=()=>{},on_submit:n=()=>{},on_blur:d=()=>{},on_focus:m=()=>{}}=a;w(i),c(t,{show_label:p,info:u,children:s$1=>{s$1.push(`<!---->${escape_html(c$1)}`);},$$slots:{default:true}}),t.push(`<!----> <button class="dialog-button svelte-nbn1m9"${attr("disabled",o,true)}${attr_style("",{background:i})}></button> `),t.push("<!--[!-->"),t.push("<!--]-->"),bind_props(a,{value:i});});}function q(e,a){e.component(t=>{let{$$slots:i,$$events:c,...u}=a;const o=new g(u,{value:"#000000"});o.props.value;let p=o.shared.label||o.i18n("color_picker.color_picker"),r=true,n;function d(m){G(m,{visible:o.shared.visible,elem_id:o.shared.elem_id,elem_classes:o.shared.elem_classes,container:o.shared.container,scale:o.shared.scale,min_width:o.shared.min_width,children:s$1=>{U(s$1,spread_props([{autoscroll:o.shared.autoscroll,i18n:o.i18n},o.shared.loading_status,{on_clear_status:()=>o.dispatch("clear_status",o.shared.loading_status)}])),s$1.push("<!----> "),B(s$1,{label:p,info:o.props.info,show_label:o.shared.show_label,disabled:!o.shared.interactive,on_input:()=>o.dispatch("input"),on_submit:()=>o.dispatch("submit"),on_blur:()=>o.dispatch("blur"),on_focus:()=>o.dispatch("focus"),get value(){return o.props.value},set value(h){o.props.value=h,r=false;}}),s$1.push("<!---->");},$$slots:{default:true}});}do r=true,n=t.copy(),d(n);while(!r);t.subsume(n);});}

export { B as BaseColorPicker, q as default };
//# sourceMappingURL=Index52-B32t5vuK.js.map
