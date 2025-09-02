"use strict";(self.webpackChunkinsteon_frontend_home_assistant=self.webpackChunkinsteon_frontend_home_assistant||[]).push([[1880],{21880:(e,t,i)=>{i.r(t),i.d(t,{HaFormGrid:()=>n});var a=i(73958),o=i(565),r=i(47838),d=(i(39663),i(9644)),s=i(36924);let n=(0,a.Z)([(0,s.Mo)("ha-form-grid")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,s.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,s.Cb)({attribute:!1})],key:"data",value:void 0},{kind:"field",decorators:[(0,s.Cb)({attribute:!1})],key:"schema",value:void 0},{kind:"field",decorators:[(0,s.Cb)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,s.Cb)()],key:"computeLabel",value:void 0},{kind:"field",decorators:[(0,s.Cb)()],key:"computeHelper",value:void 0},{kind:"method",key:"focus",value:async function(){var e;await this.updateComplete,null===(e=this.renderRoot.querySelector("ha-form"))||void 0===e||e.focus()}},{kind:"method",key:"updated",value:function(e){(0,o.Z)((0,r.Z)(i.prototype),"updated",this).call(this,e),e.has("schema")&&(this.schema.column_min_width?this.style.setProperty("--form-grid-min-width",this.schema.column_min_width):this.style.setProperty("--form-grid-min-width",""))}},{kind:"method",key:"render",value:function(){return d.dy`
      ${this.schema.schema.map((e=>d.dy`
          <ha-form
            .hass=${this.hass}
            .data=${this.data}
            .schema=${[e]}
            .disabled=${this.disabled}
            .computeLabel=${this.computeLabel}
            .computeHelper=${this.computeHelper}
          ></ha-form>
        `))}
    `}},{kind:"get",static:!0,key:"styles",value:function(){return d.iv`
      :host {
        display: grid !important;
        grid-template-columns: repeat(
          var(--form-grid-column-count, auto-fit),
          minmax(var(--form-grid-min-width, 200px), 1fr)
        );
        grid-column-gap: 8px;
        grid-row-gap: 24px;
      }
      :host > ha-form {
        display: block;
      }
    `}}]}}),d.oi)}}]);
//# sourceMappingURL=c2b65f42.js.map