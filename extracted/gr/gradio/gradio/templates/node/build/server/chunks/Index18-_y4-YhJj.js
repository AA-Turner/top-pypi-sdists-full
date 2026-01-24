import './async-Mo2Ia14K.js';
import { b as spread_props } from './index-D1Ptw7Az.js';
import { g, c as G, e as y, a as U } from './2-B89dC7Mi.js';
import { a, P as u } from './Plot-DB-BsHV0.js';
import { k } from './BlockLabel-qrJKniS-.js';
import { v } from './FullscreenButton-Dv8H9Qim.js';
import './index5-BoOEKc6P.js';
import './dev-fallback-Bc5Ork7Y.js';
import 'path';
import 'url';
import 'fs';
import './spring-DE8vsW2o.js';
import './Empty-DPmCPCDI.js';
import './Maximize-CwvDIx8B.js';

function E(i,n){i.component(p=>{let{$$slots:B,$$events:k$1,...u$1}=n;const s$1=new g(u$1);let l=false,e=true,a$1;function r(c){G(c,{padding:false,elem_id:s$1.shared.elem_id,elem_classes:s$1.shared.elem_classes,visible:s$1.shared.visible,container:s$1.shared.container,scale:s$1.shared.scale,min_width:s$1.shared.min_width,allow_overflow:false,get fullscreen(){return l},set fullscreen(o){l=o,e=false;},children:o=>{k(o,{show_label:s$1.shared.show_label,label:s$1.shared.label||s$1.i18n("plot.plot"),Icon:u}),o.push("<!----> "),s$1.props.buttons&&s$1.props.buttons.length>0||s$1.props.show_fullscreen_button?(o.push("<!--[-->"),y(o,{buttons:s$1.props.buttons??[],on_custom_button_click:t=>{s$1.dispatch("custom_button_click",{id:t});},children:t=>{s$1.props.show_fullscreen_button?(t.push("<!--[-->"),v(t,{fullscreen:l})):t.push("<!--[!-->"),t.push("<!--]-->");}})):o.push("<!--[!-->"),o.push("<!--]--> "),U(o,spread_props([{autoscroll:s$1.shared.autoscroll,i18n:s$1.i18n},s$1.shared.loading_status,{on_clear_status:()=>s$1.dispatch("clear_status",s$1.shared.loading_status)}])),o.push("<!----> "),a(o,{value:s$1.props.value,theme_mode:s$1.props.theme_mode,show_label:s$1.shared.show_label,caption:s$1.props.caption,bokeh_version:s$1.props.bokeh_version,show_actions_button:s$1.props.show_actions_button,_selectable:s$1.props._selectable,x_lim:s$1.props.x_lim,show_fullscreen_button:s$1.props.show_fullscreen_button,on_change:()=>s$1.dispatch("change")}),o.push("<!---->");},$$slots:{default:true}});}do e=true,a$1=p.copy(),r(a$1);while(!e);p.subsume(a$1);});}

export { a as BasePlot, E as default };
//# sourceMappingURL=Index18-_y4-YhJj.js.map
