import './async-Mo2Ia14K.js';
import { b as spread_props, f as attr_class, d as attr_style } from './index-D1Ptw7Az.js';
import { g, c as G, e as y, a as U, H as b } from './2-B89dC7Mi.js';
import pr from './HTML-Dc8oCSHH.js';
import { i } from './Code-DrWuNqT0.js';
import { k } from './BlockLabel-qrJKniS-.js';
export { default as BaseExample } from './Example18-2bBU3g9W.js';
import './index5-BoOEKc6P.js';
import './dev-fallback-Bc5Ork7Y.js';
import 'path';
import 'url';
import 'fs';
import './spring-DE8vsW2o.js';
import './_commonjs-dynamic-modules-DX_xVkta.js';

function E(e,l){e.component(p=>{let{$$slots:f,$$events:g$1,...i$1}=l;const s$1=new g(i$1);let r={value:s$1.props.value||"",label:s$1.shared.label,visible:s$1.shared.visible,...s$1.props.props};s$1.props.value,G(p,{visible:s$1.shared.visible,elem_id:s$1.shared.elem_id,elem_classes:s$1.shared.elem_classes,container:s$1.shared.container,padding:s$1.props.padding!==false,overflow_behavior:"visible",children:a=>{s$1.shared.show_label&&s$1.props.buttons&&s$1.props.buttons.length>0?(a.push("<!--[-->"),y(a,{buttons:s$1.props.buttons,on_custom_button_click:h=>{s$1.dispatch("custom_button_click",{id:h});}})):a.push("<!--[!-->"),a.push("<!--]--> "),s$1.shared.show_label?(a.push("<!--[-->"),k(a,{Icon:i,show_label:s$1.shared.show_label,label:s$1.shared.label,float:true})):a.push("<!--[!-->"),a.push("<!--]--> "),U(a,spread_props([{autoscroll:s$1.shared.autoscroll,i18n:s$1.i18n},s$1.shared.loading_status,{variant:"center",on_clear_status:()=>s$1.dispatch("clear_status",loading_status)}])),a.push(`<!----> <div${attr_class("html-container svelte-1jts93g",void 0,{pending:s$1.shared.loading_status?.status==="pending"&&s$1.shared.loading_status?.show_progress!=="hidden","label-padding":s$1.shared.show_label??void 0})}${attr_style("",{"min-height":s$1.props.min_height&&s$1.shared.loading_status?.status!=="pending"?b(s$1.props.min_height):void 0,"max-height":s$1.props.max_height?b(s$1.props.max_height):void 0,"overflow-y":s$1.props.max_height?"auto":void 0})}>`),pr(a,{props:r,html_template:s$1.props.html_template,css_template:s$1.props.css_template,js_on_load:s$1.props.js_on_load,elem_classes:s$1.shared.elem_classes,visible:s$1.shared.visible,autoscroll:s$1.shared.autoscroll,apply_default_css:s$1.props.apply_default_css,component_class_name:s$1.props.component_class_name}),a.push("<!----></div>");},$$slots:{default:true}});});}

export { pr as BaseHTML, E as default };
//# sourceMappingURL=Index29-Brf1TYj-.js.map
