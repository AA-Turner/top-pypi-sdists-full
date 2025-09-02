"use strict";(self.webpackChunkinsteon_frontend_home_assistant=self.webpackChunkinsteon_frontend_home_assistant||[]).push([[8874],{48874:(e,a,i)=>{i.r(a),i.d(a,{HaFormExpendable:()=>s});var t=i(73958),o=i(9644),n=i(36924);i(39663);let s=(0,t.Z)([(0,n.Mo)("ha-form-expandable")],(function(e,a){return{F:class extends a{constructor(...a){super(...a),e(this)}},d:[{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"data",value:void 0},{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"schema",value:void 0},{kind:"field",decorators:[(0,n.Cb)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,n.Cb)()],key:"computeLabel",value:void 0},{kind:"field",decorators:[(0,n.Cb)()],key:"computeHelper",value:void 0},{kind:"method",key:"render",value:function(){var e,a;return o.dy`
      <ha-expansion-panel outlined .expanded=${Boolean(this.schema.expanded)}>
        <div
          slot="header"
          role="heading"
          aria-level=${null!==(e=null===(a=this.schema.headingLevel)||void 0===a?void 0:a.toString())&&void 0!==e?e:"3"}
        >
          ${this.schema.icon?o.dy` <ha-icon .icon=${this.schema.icon}></ha-icon> `:this.schema.iconPath?o.dy`
                  <ha-svg-icon .path=${this.schema.iconPath}></ha-svg-icon>
                `:o.Ld}
          ${this.schema.title}
        </div>
        <div class="content">
          <ha-form
            .hass=${this.hass}
            .data=${this.data}
            .schema=${this.schema.schema}
            .disabled=${this.disabled}
            .computeLabel=${this.computeLabel}
            .computeHelper=${this.computeHelper}
          ></ha-form>
        </div>
      </ha-expansion-panel>
    `}},{kind:"get",static:!0,key:"styles",value:function(){return o.iv`
      :host {
        display: flex !important;
        flex-direction: column;
      }
      :host ha-form {
        display: block;
      }
      .content {
        padding: 12px;
      }
      ha-expansion-panel {
        display: block;
        --expansion-panel-content-padding: 0;
        border-radius: 6px;
        --ha-card-border-radius: 6px;
      }
      ha-svg-icon,
      ha-icon {
        color: var(--secondary-text-color);
      }
    `}}]}}),o.oi)}}]);
//# sourceMappingURL=9ecc2c0c.js.map