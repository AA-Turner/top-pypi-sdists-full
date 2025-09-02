"use strict";(self.webpackChunkinsteon_frontend_home_assistant=self.webpackChunkinsteon_frontend_home_assistant||[]).push([[1501],{81501:(e,t,i)=>{i.a(e,(async(e,a)=>{try{i.r(t),i.d(t,{HaTriggerSelector:()=>n});var r=i(73958),o=i(9644),s=i(36924),d=i(41848),l=e([d]);d=(l.then?(await l)():l)[0];let n=(0,r.Z)([(0,s.Mo)("ha-selector-trigger")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,s.Cb)()],key:"hass",value:void 0},{kind:"field",decorators:[(0,s.Cb)()],key:"selector",value:void 0},{kind:"field",decorators:[(0,s.Cb)()],key:"value",value:void 0},{kind:"field",decorators:[(0,s.Cb)()],key:"label",value:void 0},{kind:"field",decorators:[(0,s.Cb)({type:Boolean,reflect:!0})],key:"disabled",value(){return!1}},{kind:"method",key:"render",value:function(){var e,t;return o.dy`
      ${this.label?o.dy`<label>${this.label}</label>`:o.Ld}
      <ha-automation-trigger
        .disabled=${this.disabled}
        .triggers=${this.value||[]}
        .hass=${this.hass}
        .nested=${null===(e=this.selector.trigger)||void 0===e?void 0:e.nested}
        .reOrderMode=${null===(t=this.selector.trigger)||void 0===t?void 0:t.reorder_mode}
      ></ha-automation-trigger>
    `}},{kind:"get",static:!0,key:"styles",value:function(){return o.iv`
      ha-automation-trigger {
        display: block;
        margin-bottom: 16px;
      }
      :host([disabled]) ha-automation-trigger {
        opacity: var(--light-disabled-opacity);
        pointer-events: none;
      }
      label {
        display: block;
        margin-bottom: 4px;
        font-weight: 500;
      }
    `}}]}}),o.oi);a()}catch(n){a(n)}}))}}]);
//# sourceMappingURL=4eda827d.js.map