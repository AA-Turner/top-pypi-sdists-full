import { f as fallback, e as escape_html } from './async-Mo2Ia14K.js';
import { f as attr_class, e as ensure_array_like, a as attr, c as bind_props } from './index-D1Ptw7Az.js';
import { q as c } from './2-B89dC7Mi.js';
import { Q as Qu } from './Video2-BcnuCSWl.js';
import './index5-BoOEKc6P.js';
import './dev-fallback-Bc5Ork7Y.js';
import 'path';
import 'url';
import 'fs';
import './spring-DE8vsW2o.js';

function V(c$1,a){c$1.component(t=>{let i=fallback(a.value,()=>({text:"",files:[]}),true),p=a.type,o=fallback(a.selected,false);t.push(`<div${attr_class("container svelte-xz0m7l",void 0,{table:p==="table",gallery:p==="gallery",selected:o,border:i})}><p>${escape_html(i.text?i.text:"")}</p> <!--[-->`);const u=ensure_array_like(i.files);for(let e=0,m=u.length;e<m;e++){let l=u[e];l.mime_type&&l.mime_type.includes("image")?(t.push("<!--[-->"),c(t,{src:l.url})):(t.push("<!--[!-->"),l.mime_type&&l.mime_type.includes("video")?(t.push("<!--[-->"),Qu(t,{src:l.url,alt:"",loop:true,is_stream:false})):(t.push("<!--[!-->"),l.mime_type&&l.mime_type.includes("audio")?(t.push("<!--[-->"),t.push(`<audio${attr("src",l.url)} controls></audio>`)):(t.push("<!--[!-->"),t.push(`${escape_html(l.orig_name)}`)),t.push("<!--]-->")),t.push("<!--]-->")),t.push("<!--]-->");}t.push("<!--]--></div>"),bind_props(a,{value:i,type:p,selected:o});});}

export { V as default };
//# sourceMappingURL=Example23-tcbzMCSz.js.map
