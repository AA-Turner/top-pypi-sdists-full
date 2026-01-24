import { f as fallback } from './async-Mo2Ia14K.js';
import { f as attr_class, c as bind_props } from './index-D1Ptw7Az.js';
import { e as y, q as c, l as w, j as w$1 } from './2-B89dC7Mi.js';
import { k } from './BlockLabel-qrJKniS-.js';
import { u } from './DownloadLink-CHK0Lliu.js';
import { p } from './Empty-DPmCPCDI.js';
import { y as y$1 } from './ShareButton-BgNheG3R.js';
import { l } from './Download-CXUtRxuu.js';
import { i } from './Image2-rnCO69bR.js';
import { v } from './FullscreenButton-Dv8H9Qim.js';
import './index5-BoOEKc6P.js';
import './dev-fallback-Bc5Ork7Y.js';
import 'path';
import 'url';
import 'fs';
import './spring-DE8vsW2o.js';
import './Maximize-CwvDIx8B.js';

/* empty css                                          */function Q(g,o){g.component(a=>{let u$1=o.value,e=fallback(o.label,void 0),c$1=o.show_label,i$1=fallback(o.buttons,()=>[],true),f=fallback(o.on_custom_button_click,null),n=fallback(o.selectable,false),m=o.i18n,p$1=fallback(o.display_icon_button_wrapper_top_corner,false),b=fallback(o.fullscreen,false),_=fallback(o.show_button_background,true);k(a,{show_label:c$1,Icon:i,label:c$1?e||m("image.image"):""}),a.push("<!----> "),u$1==null||!u$1?.url?(a.push("<!--[-->"),p(a,{unpadded_box:true,size:"large",children:l=>{i(l);},$$slots:{default:true}})):(a.push("<!--[!-->"),a.push('<div class="image-container svelte-12vrxzd">'),y(a,{display_top_corner:p$1,show_background:_,buttons:i$1,on_custom_button_click:f,children:l$1=>{i$1.some(t=>typeof t=="string"&&t==="fullscreen")?(l$1.push("<!--[-->"),v(l$1,{fullscreen:b})):l$1.push("<!--[!-->"),l$1.push("<!--]--> "),i$1.some(t=>typeof t=="string"&&t==="download")?(l$1.push("<!--[-->"),u(l$1,{href:u$1.url,download:u$1.orig_name||"image",children:t=>{w(t,{Icon:l,label:m("common.download")});},$$slots:{default:true}})):l$1.push("<!--[!-->"),l$1.push("<!--]--> "),i$1.some(t=>typeof t=="string"&&t==="share")?(l$1.push("<!--[-->"),y$1(l$1,{i18n:m,formatter:async t=>t?`<img src="${await w$1(t)}" />`:"",value:u$1})):l$1.push("<!--[!-->"),l$1.push("<!--]-->");}}),a.push(`<!----> <button class="svelte-12vrxzd"><div${attr_class("image-frame svelte-12vrxzd",void 0,{selectable:n})}>`),c(a,{src:u$1.url,restProps:{loading:"lazy",alt:""}}),a.push("<!----></div></button></div>")),a.push("<!--]-->"),bind_props(o,{value:u$1,label:e,show_label:c$1,buttons:i$1,on_custom_button_click:f,selectable:n,i18n:m,display_icon_button_wrapper_top_corner:p$1,fullscreen:b,show_button_background:_});});}

export { Q as default };
//# sourceMappingURL=ImagePreview-DZORK30D.js.map
