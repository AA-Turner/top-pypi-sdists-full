import './async-Mo2Ia14K.js';
import { f as attr_class, a as attr, d as attr_style, g as stringify } from './index-D1Ptw7Az.js';
import { H as b, e as y, r as P, l as w, o as h, t as e } from './2-B89dC7Mi.js';

function K(m,r){m.component(t=>{let{elem_classes:c=[],visible:f=true,value:e$1,min_height:s$1=void 0,rtl:u=false,sanitize_html:d=true,line_breaks:h$1=false,latex_delimiters:_=[],header_links:g=false,height:n=void 0,show_copy_button:v=false,loading_status:y$1=void 0,theme_mode:k,onchange:z=()=>{},oncopy:b$1=l=>{}}=r,o=false,a;async function w$1(){"clipboard"in navigator&&(await navigator.clipboard.writeText(e$1),b$1({value:e$1}),C());}function C(){o=true,a&&clearTimeout(a),a=setTimeout(()=>{o=false;},1e3);}t.push(`<div${attr_class(`prose ${stringify(c?.join(" ")||"")}`,"svelte-1xjkzpp",{hide:!f})} data-testid="markdown"${attr("dir",u?"rtl":"ltr")}${attr_style(n?`max-height: ${b(n)}; overflow-y: auto;`:"",{"min-height":s$1&&y$1?.status!=="pending"?b(s$1):void 0})}>`),v?(t.push("<!--[-->"),y(t,{children:l=>{w(l,{Icon:o?e:h,onclick:w$1,label:o?"Copied conversation":"Copy conversation"});}})):t.push("<!--[!-->"),t.push("<!--]--> "),P(t,{message:e$1,latex_delimiters:_,sanitize_html:d,line_breaks:h$1,chatbot:false,header_links:g,theme_mode:k}),t.push("<!----></div>");});}

export { K };
//# sourceMappingURL=Index.svelte_svelte_type_style_lang2-e6yfyvxZ.js.map
