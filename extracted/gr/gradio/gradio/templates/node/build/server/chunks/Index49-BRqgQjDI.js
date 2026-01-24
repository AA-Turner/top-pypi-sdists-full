import { f as fallback, g as getContext } from './async-Mo2Ia14K.js';
import { s as store_get, a as attr, f as attr_class, d as attr_style, g as stringify, i as slot, u as unsubscribe_stores, c as bind_props } from './index-D1Ptw7Az.js';
import { d as b, g } from './2-B89dC7Mi.js';
import { t as tick, c as createEventDispatcher } from './spring-DE8vsW2o.js';
import { O } from './Walkthrough.svelte_svelte_type_style_lang-Cbiyy8Wd.js';
import './index5-BoOEKc6P.js';
import './dev-fallback-Bc5Ork7Y.js';
import 'path';
import 'url';
import 'fs';

function N(d,e){d.component(n=>{var r;let m,i=fallback(e.elem_id,""),l=fallback(e.elem_classes,()=>[],true),s$1=e.label,c=fallback(e.id,()=>({}),true),_=e.visible,f=e.interactive,u=e.order,o=e.scale,p=e.component_id;const h=createEventDispatcher(),{register_tab:v,unregister_tab:g,selected_tab:x,selected_tab_index:k}=getContext(O);let b$1;function y(a,B){return a=JSON.parse(a),v(a,B)}m=JSON.stringify({label:s$1,id:c,elem_id:i,visible:_,interactive:f,scale:o,component_id:p}),b$1=y(m,u),store_get(r??={},"$selected_tab_index",k)===b$1&&tick().then(()=>h("select",{value:s$1,index:b$1})),n.push(`<div${attr("id",i)}${attr_class(`tabitem ${stringify(l.join(" "))}`,"svelte-dmtrd3",{"grow-children":o>=1})} role="tabpanel"${attr_style("",{display:store_get(r??={},"$selected_tab",x)===c&&_!==false?"flex":"none","flex-grow":o})}>`),b(n,{scale:o>=1?o:null,children:a=>{a.push("<!--[-->"),slot(a,e,"default",{},null),a.push("<!--]-->");},$$slots:{default:true}}),n.push("<!----></div>"),r&&unsubscribe_stores(r),bind_props(e,{elem_id:i,elem_classes:l,label:s$1,id:c,visible:_,interactive:f,order:u,scale:o,component_id:p});});}function z(d,e){d.component(n=>{let{$$slots:r,$$events:m,...i}=e;const l=new g(i);N(n,{elem_id:l.shared.elem_id,elem_classes:l.shared.elem_classes,label:l.shared.label,visible:l.shared.visible,interactive:l.shared.interactive,id:l.props.id,order:l.props.order,scale:l.props.scale,component_id:l.props.component_id,children:s$1=>{s$1.push("<!--[-->"),slot(s$1,e,"default",{},null),s$1.push("<!--]-->");},$$slots:{default:true}});});}

export { N as BaseTabItem, z as default };
//# sourceMappingURL=Index49-BRqgQjDI.js.map
