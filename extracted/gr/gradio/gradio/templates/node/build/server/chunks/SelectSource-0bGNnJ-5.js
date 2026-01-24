import './async-Mo2Ia14K.js';
import { f as attr_class, c as bind_props } from './index-D1Ptw7Az.js';
import { o } from './UploadText-Cj3NP7gm.js';
import { i as i$1 } from './Microphone-C7JgPGGY.js';
import { i } from './Upload-DAOKtkC7.js';

function h(t){t.push('<svg xmlns="http://www.w3.org/2000/svg" width="100%" height="100%" viewBox="0 0 24 24"><path fill="currentColor" d="M12 2c-4.963 0-9 4.038-9 9c0 3.328 1.82 6.232 4.513 7.79l-2.067 1.378A1 1 0 0 0 6 22h12a1 1 0 0 0 .555-1.832l-2.067-1.378C19.18 17.232 21 14.328 21 11c0-4.962-4.037-9-9-9zm0 16c-3.859 0-7-3.141-7-7c0-3.86 3.141-7 7-7s7 3.14 7 7c0 3.859-3.141 7-7 7z"></path><path fill="currentColor" d="M12 6c-2.757 0-5 2.243-5 5s2.243 5 5 5s5-2.243 5-5s-2.243-5-5-5zm0 8c-1.654 0-3-1.346-3-3s1.346-3 3-3s3 1.346 3 3s-1.346 3-3 3z"></path></svg>');}

function k(l,u){l.component(s$1=>{let{sources:t,active_source:o$1=void 0,handle_clear:m=()=>{},handle_select:b=()=>{}}=u;[...new Set(t)].length>1?(s$1.push("<!--[-->"),s$1.push('<span class="source-selection svelte-exvkcd" data-testid="source-select">'),t.includes("upload")?(s$1.push("<!--[-->"),s$1.push(`<button${attr_class("icon svelte-exvkcd",void 0,{selected:o$1==="upload"||!o$1})} aria-label="Upload file">`),i(s$1),s$1.push("<!----></button>")):s$1.push("<!--[!-->"),s$1.push("<!--]--> "),t.includes("microphone")?(s$1.push("<!--[-->"),s$1.push(`<button${attr_class("icon svelte-exvkcd",void 0,{selected:o$1==="microphone"})} aria-label="Record audio">`),i$1(s$1),s$1.push("<!----></button>")):s$1.push("<!--[!-->"),s$1.push("<!--]--> "),t.includes("webcam")?(s$1.push("<!--[-->"),s$1.push(`<button${attr_class("icon svelte-exvkcd",void 0,{selected:o$1==="webcam"})} aria-label="Capture from camera">`),h(s$1),s$1.push("<!----></button>")):s$1.push("<!--[!-->"),s$1.push("<!--]--> "),t.includes("clipboard")?(s$1.push("<!--[-->"),s$1.push(`<button${attr_class("icon svelte-exvkcd",void 0,{selected:o$1==="clipboard"})} aria-label="Paste from clipboard">`),o(s$1),s$1.push("<!----></button>")):s$1.push("<!--[!-->"),s$1.push("<!--]--></span>")):s$1.push("<!--[!-->"),s$1.push("<!--]-->"),bind_props(u,{active_source:o$1});});}

export { h, k };
//# sourceMappingURL=SelectSource-0bGNnJ-5.js.map
