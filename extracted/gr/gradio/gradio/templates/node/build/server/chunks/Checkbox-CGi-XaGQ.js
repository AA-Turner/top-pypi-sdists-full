import { e as escape_html } from './async-Mo2Ia14K.js';
import { f as attr_class, a as attr, c as bind_props } from './index-D1Ptw7Az.js';

function x(c,s$1){c.component(t=>{let{label:o="Checkbox",value:a=void 0,interactive:p=true,show_label:i=true,on_change:b,on_input:h,on_select:n}=s$1,l=!p;t.push(`<label${attr_class("checkbox-container svelte-1q8xtp9",void 0,{disabled:l})}><input${attr("checked",a,true)}${attr("disabled",l,true)} type="checkbox" name="test" data-testid="checkbox" class="svelte-1q8xtp9"/> `),i?(t.push("<!--[-->"),t.push(`<span class="label-text svelte-1q8xtp9">${escape_html(o)}</span>`)):t.push("<!--[!-->"),t.push("<!--]--></label>"),bind_props(s$1,{value:a});});}

export { x };
//# sourceMappingURL=Checkbox-CGi-XaGQ.js.map
