"use strict";(self.webpackChunkknx_frontend=self.webpackChunkknx_frontend||[]).push([["9607"],{49590:function(e,t,i){i.a(e,(async function(e,o){try{i.r(t),i.d(t,{HaIconPicker:function(){return V}});i(39710),i(26847),i(2394),i(18574),i(81738),i(94814),i(22960),i(6989),i(72489),i(1455),i(67886),i(65451),i(46015),i(38334),i(94880),i(75643),i(29761),i(56389),i(27530);var a=i(73742),s=i(59048),n=i(7616),l=i(28105),r=i(29740),c=i(18610),d=i(54693),h=(i(3847),i(57264),e([d]));d=(h.then?(await h)():h)[0];let p,u,_,v,g,m=e=>e,b=[],y=!1;const f=async()=>{y=!0;const e=await i.e("4813").then(i.t.bind(i,81405,19));b=e.default.map((e=>({icon:`mdi:${e.name}`,parts:new Set(e.name.split("-")),keywords:e.keywords})));const t=[];Object.keys(c.g).forEach((e=>{t.push($(e))})),(await Promise.all(t)).forEach((e=>{b.push(...e)}))},$=async e=>{try{const t=c.g[e].getIconList;if("function"!=typeof t)return[];const i=await t();return i.map((t=>{var i;return{icon:`${e}:${t.name}`,parts:new Set(t.name.split("-")),keywords:null!==(i=t.keywords)&&void 0!==i?i:[]}}))}catch(t){return console.warn(`Unable to load icon list for ${e} iconset`),[]}},x=e=>(0,s.dy)(p||(p=m`
  <ha-combo-box-item type="button">
    <ha-icon .icon=${0} slot="start"></ha-icon>
    ${0}
  </ha-combo-box-item>
`),e.icon,e.icon);class V extends s.oi{render(){return(0,s.dy)(u||(u=m`
      <ha-combo-box
        .hass=${0}
        item-value-path="icon"
        item-label-path="icon"
        .value=${0}
        allow-custom-value
        .dataProvider=${0}
        .label=${0}
        .helper=${0}
        .disabled=${0}
        .required=${0}
        .placeholder=${0}
        .errorMessage=${0}
        .invalid=${0}
        .renderer=${0}
        icon
        @opened-changed=${0}
        @value-changed=${0}
      >
        ${0}
      </ha-combo-box>
    `),this.hass,this._value,y?this._iconProvider:void 0,this.label,this.helper,this.disabled,this.required,this.placeholder,this.errorMessage,this.invalid,x,this._openedChanged,this._valueChanged,this._value||this.placeholder?(0,s.dy)(_||(_=m`
              <ha-icon .icon=${0} slot="icon">
              </ha-icon>
            `),this._value||this.placeholder):(0,s.dy)(v||(v=m`<slot slot="icon" name="fallback"></slot>`)))}async _openedChanged(e){e.detail.value&&!y&&(await f(),this.requestUpdate())}_valueChanged(e){e.stopPropagation(),this._setValue(e.detail.value)}_setValue(e){this.value=e,(0,r.B)(this,"value-changed",{value:this._value},{bubbles:!1,composed:!1})}get _value(){return this.value||""}constructor(...e){super(...e),this.disabled=!1,this.required=!1,this.invalid=!1,this._filterIcons=(0,l.Z)(((e,t=b)=>{if(!e)return t;const i=[],o=(e,t)=>i.push({icon:e,rank:t});for(const a of t)a.parts.has(e)?o(a.icon,1):a.keywords.includes(e)?o(a.icon,2):a.icon.includes(e)?o(a.icon,3):a.keywords.some((t=>t.includes(e)))&&o(a.icon,4);return 0===i.length&&o(e,0),i.sort(((e,t)=>e.rank-t.rank))})),this._iconProvider=(e,t)=>{const i=this._filterIcons(e.filter.toLowerCase(),b),o=e.page*e.pageSize,a=o+e.pageSize;t(i.slice(o,a),i.length)}}}V.styles=(0,s.iv)(g||(g=m`
    *[slot="icon"] {
      color: var(--primary-text-color);
      position: relative;
      bottom: 2px;
    }
    *[slot="prefix"] {
      margin-right: 8px;
      margin-inline-end: 8px;
      margin-inline-start: initial;
    }
  `)),(0,a.__decorate)([(0,n.Cb)({attribute:!1})],V.prototype,"hass",void 0),(0,a.__decorate)([(0,n.Cb)()],V.prototype,"value",void 0),(0,a.__decorate)([(0,n.Cb)()],V.prototype,"label",void 0),(0,a.__decorate)([(0,n.Cb)()],V.prototype,"helper",void 0),(0,a.__decorate)([(0,n.Cb)()],V.prototype,"placeholder",void 0),(0,a.__decorate)([(0,n.Cb)({attribute:"error-message"})],V.prototype,"errorMessage",void 0),(0,a.__decorate)([(0,n.Cb)({type:Boolean})],V.prototype,"disabled",void 0),(0,a.__decorate)([(0,n.Cb)({type:Boolean})],V.prototype,"required",void 0),(0,a.__decorate)([(0,n.Cb)({type:Boolean})],V.prototype,"invalid",void 0),V=(0,a.__decorate)([(0,n.Mo)("ha-icon-picker")],V),o()}catch(p){o(p)}}))},1166:function(e,t,i){i.a(e,(async function(e,o){try{i.r(t);i(26847),i(87799),i(1455),i(27530);var a=i(73742),s=i(59048),n=i(7616),l=i(88245),r=i(29740),c=i(30337),d=(i(78645),i(49590)),h=(i(39651),i(93795),i(48374),i(38573),i(81665)),p=i(77204),u=e([c,d]);[c,d]=u.then?(await u)():u;let _,v,g,m,b=e=>e;const y="M19,4H15.5L14.5,3H9.5L8.5,4H5V6H19M6,19A2,2 0 0,0 8,21H16A2,2 0 0,0 18,19V7H6V19Z",f="M7,19V17H9V19H7M11,19V17H13V19H11M15,19V17H17V19H15M7,15V13H9V15H7M11,15V13H13V15H11M15,15V13H17V15H15M7,11V9H9V11H7M11,11V9H13V11H11M15,11V9H17V11H15M7,7V5H9V7H7M11,7V5H13V7H11M15,7V5H17V7H15Z";class $ extends s.oi{_optionMoved(e){e.stopPropagation();const{oldIndex:t,newIndex:i}=e.detail,o=this._options.concat(),a=o.splice(t,1)[0];o.splice(i,0,a),(0,r.B)(this,"value-changed",{value:Object.assign(Object.assign({},this._item),{},{options:o})})}set item(e){this._item=e,e?(this._name=e.name||"",this._icon=e.icon||"",this._options=e.options||[]):(this._name="",this._icon="",this._options=[])}focus(){this.updateComplete.then((()=>{var e;return null===(e=this.shadowRoot)||void 0===e||null===(e=e.querySelector("[dialogInitialFocus]"))||void 0===e?void 0:e.focus()}))}render(){return this.hass?(0,s.dy)(_||(_=b`
      <div class="form">
        <ha-textfield
          dialogInitialFocus
          autoValidate
          required
          .validationMessage=${0}
          .value=${0}
          .label=${0}
          .configValue=${0}
          @input=${0}
        ></ha-textfield>
        <ha-icon-picker
          .hass=${0}
          .value=${0}
          .configValue=${0}
          @value-changed=${0}
          .label=${0}
        ></ha-icon-picker>
        <div class="header">
          ${0}:
        </div>
        <ha-sortable @item-moved=${0} handle-selector=".handle">
          <ha-list class="options">
            ${0}
          </ha-list>
        </ha-sortable>
        <div class="layout horizontal center">
          <ha-textfield
            class="flex-auto"
            id="option_input"
            .label=${0}
            @keydown=${0}
          ></ha-textfield>
          <ha-button size="small" appearance="plain" @click=${0}
            >${0}</ha-button
          >
        </div>
      </div>
    `),this.hass.localize("ui.dialogs.helper_settings.required_error_msg"),this._name,this.hass.localize("ui.dialogs.helper_settings.generic.name"),"name",this._valueChanged,this.hass,this._icon,"icon",this._valueChanged,this.hass.localize("ui.dialogs.helper_settings.generic.icon"),this.hass.localize("ui.dialogs.helper_settings.input_select.options"),this._optionMoved,this._options.length?(0,l.r)(this._options,(e=>e),((e,t)=>(0,s.dy)(v||(v=b`
                    <ha-list-item class="option" hasMeta>
                      <div class="optioncontent">
                        <div class="handle">
                          <ha-svg-icon .path=${0}></ha-svg-icon>
                        </div>
                        ${0}
                      </div>
                      <ha-icon-button
                        slot="meta"
                        .index=${0}
                        .label=${0}
                        @click=${0}
                        .path=${0}
                      ></ha-icon-button>
                    </ha-list-item>
                  `),f,e,t,this.hass.localize("ui.dialogs.helper_settings.input_select.remove_option"),this._removeOption,y))):(0,s.dy)(g||(g=b`
                  <ha-list-item noninteractive>
                    ${0}
                  </ha-list-item>
                `),this.hass.localize("ui.dialogs.helper_settings.input_select.no_options")),this.hass.localize("ui.dialogs.helper_settings.input_select.add_option"),this._handleKeyAdd,this._addOption,this.hass.localize("ui.dialogs.helper_settings.input_select.add")):s.Ld}_handleKeyAdd(e){e.stopPropagation(),"Enter"===e.key&&this._addOption()}_addOption(){const e=this._optionInput;null!=e&&e.value&&((0,r.B)(this,"value-changed",{value:Object.assign(Object.assign({},this._item),{},{options:[...this._options,e.value]})}),e.value="")}async _removeOption(e){const t=e.target.index;if(!(await(0,h.g7)(this,{title:this.hass.localize("ui.dialogs.helper_settings.input_select.confirm_delete.delete"),text:this.hass.localize("ui.dialogs.helper_settings.input_select.confirm_delete.prompt"),destructive:!0})))return;const i=[...this._options];i.splice(t,1),(0,r.B)(this,"value-changed",{value:Object.assign(Object.assign({},this._item),{},{options:i})})}_valueChanged(e){var t;if(!this.new&&!this._item)return;e.stopPropagation();const i=e.target.configValue,o=(null===(t=e.detail)||void 0===t?void 0:t.value)||e.target.value;if(this[`_${i}`]===o)return;const a=Object.assign({},this._item);o?a[i]=o:delete a[i],(0,r.B)(this,"value-changed",{value:a})}static get styles(){return[p.Qx,(0,s.iv)(m||(m=b`
        .form {
          color: var(--primary-text-color);
        }
        .option {
          border: 1px solid var(--divider-color);
          border-radius: 4px;
          margin-top: 4px;
          --mdc-icon-button-size: 24px;
          --mdc-ripple-color: transparent;
          --mdc-list-side-padding: 16px;
          cursor: default;
          background-color: var(--card-background-color);
        }
        ha-textfield {
          display: block;
          margin-bottom: 8px;
        }
        #option_input {
          margin-top: 8px;
        }
        .header {
          margin-top: 8px;
          margin-bottom: 8px;
        }
        .handle {
          cursor: move; /* fallback if grab cursor is unsupported */
          cursor: grab;
          padding-right: 12px;
          padding-inline-end: 12px;
          padding-inline-start: initial;
        }
        .handle ha-svg-icon {
          pointer-events: none;
          height: 24px;
        }
        .optioncontent {
          display: flex;
          align-items: center;
        }
      `))]}constructor(...e){super(...e),this.new=!1,this._options=[]}}(0,a.__decorate)([(0,n.Cb)({attribute:!1})],$.prototype,"hass",void 0),(0,a.__decorate)([(0,n.Cb)({type:Boolean})],$.prototype,"new",void 0),(0,a.__decorate)([(0,n.SB)()],$.prototype,"_name",void 0),(0,a.__decorate)([(0,n.SB)()],$.prototype,"_icon",void 0),(0,a.__decorate)([(0,n.SB)()],$.prototype,"_options",void 0),(0,a.__decorate)([(0,n.IO)("#option_input",!0)],$.prototype,"_optionInput",void 0),$=(0,a.__decorate)([(0,n.Mo)("ha-input_select-form")],$),o()}catch(_){o(_)}}))}}]);
//# sourceMappingURL=9607.b637fa90684812d3.js.map