import { K as h, L as tick, N as g } from './2-CiIvreWi.js';
import { p } from './statustracker-Bm114cyu.js';
import { n } from './src3-BZUAlyHf.js';
import { r } from './Index7-CurGKs-t.js';
import './async-Cv1-GZGV.js';
import { d as derived, s as spread_props, a as attr_class, e as escape_html, b as attr_style, c as bind_props } from './renderer-RGQlaTg4.js';
import './environment-LXawilJQ.js';
import './chunk-B3kRsjbd.js';
import 'node:module';
import './server-03g46sDD.js';
import './html-CfyvkLET.js';

function s(e,t){e.component(e=>{let{open:n=true,label:r=``,height:i,max_height:a,onexpand:s,oncollapse:c,children:l}=t;e.push(`<button${attr_class(`label-wrap svelte-e5lyqv`,void 0,{open:n})}><span class="svelte-e5lyqv">${escape_html(r)}</span> <span class="icon svelte-e5lyqv"${attr_style(``,{transform:n?`rotate(0)`:`rotate(90deg)`})}>▼</span></button> <div data-testid="accordion-content"${attr_class(`svelte-e5lyqv`,void 0,{scrollable:i||a})}${attr_style(``,{display:n?`block`:`none`,height:i,"max-height":a})}>`),l?.(e),e.push(`<!----></div>`),bind_props(t,{open:n});});}function c(c,l){c.component(c=>{let{$$slots:u,$$events:d,...f}=l;let p$1 = class p extends h{set_data(e){let t=this.props.open;super.set_data(e),`open`in e&&e.open!==t&&(e.open?(this.dispatch(`expand`),tick().then(()=>this.dispatch(`gradio_expand`))):this.dispatch(`collapse`)),this.shared.loading_status.status=`complete`;}};let m=new p$1(f),h$1=derived(()=>m.shared.label||``),g$1=derived(()=>[...m.shared.elem_classes||[],`gr-accordion`]),_=derived(()=>m.shared.visible===true?true:`hidden`);n(c,{elem_id:m.shared.elem_id,elem_classes:g$1(),visible:_(),children:t=>{m.shared.loading_status?(t.push(`<!--[0-->`),p(t,spread_props([{autoscroll:m.shared.autoscroll,i18n:m.i18n},m.shared.loading_status]))):t.push(`<!--[-1-->`),t.push(`<!--]--> `),s(t,{label:h$1(),open:m.props.open,height:m.props.height==null?void 0:g(m.props.height),max_height:m.props.max_height==null?void 0:g(m.props.max_height),onexpand:()=>{m.dispatch(`expand`),m.dispatch(`gradio_expand`);},oncollapse:()=>m.dispatch(`collapse`),children:e=>{r(e,{children:e=>{f.children?.(e),e.push(`<!---->`);},$$slots:{default:true}});},$$slots:{default:true}}),t.push(`<!---->`);},$$slots:{default:true}});});}

export { c as default };
//# sourceMappingURL=Index9-B_42zdfz.js.map
