import './async-DWBXLqlH.js';
import { b as spread_props, d as attr_class, g as attr_style } from './index-D1re1cuM.js';
import './2-D-BOeBbl.js';
import { S, T } from './utils.svelte-B6jnWCLi.js';
import pr from './HTML-Cjmao4Sd.js';
import { R } from './index3-D8K8hrsu.js';
import { i } from './Code-JPvLawBI.js';
import { G } from './Block-C1l7qmeM.js';
import './MarkdownCode.svelte_svelte_type_style_lang-LyYy_rma.js';
import { k } from './BlockLabel-B2_AkSr2.js';
import { y } from './IconButtonWrapper-BI5v6wo4.js';
export { default as BaseExample } from './Example18-Cul-0cb7.js';
import './escaping-CBnpiEl5.js';
import './context-BZS6UlnY.js';
import './uneval-ZBzcyJ66.js';
import './clone-CubQhOZi.js';
import './index5-BoOEKc6P.js';
import './dev-fallback-Bc5Ork7Y.js';
import './_commonjs-dynamic-modules-DX_xVkta.js';
import 'fs';
import './spring-D6sHki8W.js';
import './IconButton-C2_XRZp7.js';
import './Clear-CTfKb9Id.js';
import './prism-python-AN_bsBrU.js';

function W(p,i$1){p.component(r=>{let{$$slots:g,$$events:v,...e}=i$1,h=e.children;const s$1=new S(e);let n={value:s$1.props.value||"",label:s$1.shared.label,visible:s$1.shared.visible,...s$1.props.props};s$1.props.value,G(r,{visible:s$1.shared.visible,elem_id:s$1.shared.elem_id,elem_classes:s$1.shared.elem_classes,container:s$1.shared.container,padding:s$1.props.padding!==false,overflow_behavior:"visible",children:a=>{s$1.shared.show_label&&s$1.props.buttons&&s$1.props.buttons.length>0?(a.push("<!--[-->"),y(a,{buttons:s$1.props.buttons,on_custom_button_click:o=>{s$1.dispatch("custom_button_click",{id:o});}})):a.push("<!--[!-->"),a.push("<!--]--> "),s$1.shared.show_label?(a.push("<!--[-->"),k(a,{Icon:i,show_label:s$1.shared.show_label,label:s$1.shared.label,float:true})):a.push("<!--[!-->"),a.push("<!--]--> "),R(a,spread_props([{autoscroll:s$1.shared.autoscroll,i18n:s$1.i18n},s$1.shared.loading_status,{variant:"center",on_clear_status:()=>s$1.dispatch("clear_status",loading_status)}])),a.push(`<!----> <div${attr_class("html-container svelte-1jts93g",void 0,{pending:s$1.shared.loading_status?.status==="pending"&&s$1.shared.loading_status?.show_progress!=="hidden","label-padding":s$1.shared.show_label??void 0})}${attr_style("",{"min-height":s$1.props.min_height&&s$1.shared.loading_status?.status!=="pending"?T(s$1.props.min_height):void 0,"max-height":s$1.props.max_height?T(s$1.props.max_height):void 0,"overflow-y":s$1.props.max_height?"auto":void 0})}>`),pr(a,{props:n,html_template:s$1.props.html_template,css_template:s$1.props.css_template,js_on_load:s$1.props.js_on_load,elem_classes:s$1.shared.elem_classes,visible:s$1.shared.visible,autoscroll:s$1.shared.autoscroll,apply_default_css:s$1.props.apply_default_css,component_class_name:s$1.props.component_class_name,server:s$1.shared.server,children:o=>{h?.(o);}}),a.push("<!----></div>");},$$slots:{default:true}});});}

export { pr as BaseHTML, W as default };
//# sourceMappingURL=Index28-DbuGBQ5p.js.map
