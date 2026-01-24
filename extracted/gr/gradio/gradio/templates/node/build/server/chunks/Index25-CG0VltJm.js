import { e as escape_html } from './async-Mo2Ia14K.js';
import { b as spread_props, a as attr, e as ensure_array_like, f as attr_class } from './index-D1Ptw7Az.js';
import { g, c as G, a as U, e as y, C as c } from './2-B89dC7Mi.js';
import './index5-BoOEKc6P.js';
import './dev-fallback-Bc5Ork7Y.js';
import 'path';
import 'url';
import 'fs';
import './spring-DE8vsW2o.js';

function z(p,h){p.component(u=>{let{$$slots:f,$$events:x,...r}=h,t=new g(r),c$1=(()=>{const e=t.props.choices.map(([,a])=>a);return t.props.value.length===0?"unchecked":t.props.value.length===e.length?"checked":"indeterminate"})(),i=!t.shared.interactive;t.props.value,G(u,{visible:t.shared.visible,elem_id:t.shared.elem_id,elem_classes:t.shared.elem_classes,type:"fieldset",container:t.shared.container,scale:t.shared.scale,min_width:t.shared.min_width,children:e=>{U(e,spread_props([{autoscroll:t.shared.autoscroll,i18n:t.i18n},t.shared.loading_status,{on_clear_status:()=>t.dispatch("clear_status",t.shared.loading_status)}])),e.push("<!----> "),t.shared.show_label&&t.props.buttons&&t.props.buttons.length>0?(e.push("<!--[-->"),y(e,{buttons:t.props.buttons,on_custom_button_click:s=>{t.dispatch("custom_button_click",{id:s});}})):e.push("<!--[!-->"),e.push("<!--]--> "),c(e,{show_label:t.shared.show_label||t.props.show_select_all&&t.shared.interactive,info:t.props.info,children:s$1=>{t.props.show_select_all&&t.shared.interactive?(s$1.push("<!--[-->"),s$1.push(`<div class="select-all-container svelte-yb2gcx"><label class="select-all-label svelte-yb2gcx"><input class="select-all-checkbox svelte-yb2gcx"${attr("checked",c$1==="checked",true)}${attr("indeterminate",c$1==="indeterminate",true)} type="checkbox" title="Select/Deselect All"/></label> <button type="button" class="label-text svelte-yb2gcx">${escape_html(t.shared.show_label?t.shared.label:"Select All")}</button></div>`)):(s$1.push("<!--[!-->"),t.shared.show_label?(s$1.push("<!--[-->"),s$1.push(`${escape_html(t.shared.label||t.i18n("checkbox.checkbox_group"))}`)):s$1.push("<!--[!-->"),s$1.push("<!--]-->")),s$1.push("<!--]-->");},$$slots:{default:true}}),e.push('<!----> <div class="wrap svelte-yb2gcx" data-testid="checkbox-group"><!--[-->');const a=ensure_array_like(t.props.choices);for(let s$1=0,n=a.length;s$1<n;s$1++){let[d,o]=a[s$1];e.push(`<label${attr_class("svelte-yb2gcx",void 0,{disabled:i,selected:t.props.value.includes(o)})}><input${attr("disabled",i,true)}${attr("checked",t.props.value.includes(o),true)} type="checkbox"${attr("name",o?.toString())}${attr("title",o?.toString())} class="svelte-yb2gcx"/> <span class="ml-2 svelte-yb2gcx">${escape_html(d)}</span></label>`);}e.push("<!--]--></div>");},$$slots:{default:true}});});}

export { z as default };
//# sourceMappingURL=Index25-CG0VltJm.js.map
