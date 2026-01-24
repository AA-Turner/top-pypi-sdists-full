import { f as fallback, e as escape_html } from './async-Mo2Ia14K.js';
import { f as attr_class, e as ensure_array_like, c as bind_props } from './index-D1Ptw7Az.js';

function f(p,t){p.component(l=>{let a=t.value,e=t.type,i=fallback(t.selected,false);if(l.push(`<ul${attr_class("svelte-14aa7hi",void 0,{table:e==="table",gallery:e==="gallery",selected:i})}>`),a){l.push("<!--[-->"),l.push("<!--[-->");const u=ensure_array_like(Array.isArray(a)?a.slice(0,3):[a]);for(let h=0,c=u.length;h<c;h++){let o=u[h];l.push(`<li><code>./${escape_html(o)}</code></li>`);}l.push("<!--]--> "),Array.isArray(a)&&a.length>3?(l.push("<!--[-->"),l.push('<li class="extra svelte-14aa7hi">...</li>')):l.push("<!--[!-->"),l.push("<!--]-->");}else l.push("<!--[!-->");l.push("<!--]--></ul>"),bind_props(t,{value:a,type:e,selected:i});});}

export { f as default };
//# sourceMappingURL=Example17--6WHhLSK.js.map
