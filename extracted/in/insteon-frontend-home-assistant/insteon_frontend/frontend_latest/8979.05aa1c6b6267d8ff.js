export const __webpack_id__="8979";export const __webpack_ids__=["8979"];export const __webpack_modules__={31747:function(e,t,i){i.a(e,async function(e,a){try{i.d(t,{T:()=>r});var s=i(22),o=i(22786),n=e([s]);s=(n.then?(await n)():n)[0];const r=(e,t)=>{try{return l(t)?.of(e)??e}catch{return e}},l=(0,o.A)(e=>new Intl.DisplayNames(e.language,{type:"language",fallback:"code"}));a()}catch(r){a(r)}})},56528:function(e,t,i){i.a(e,async function(e,t){try{var a=i(62826),s=i(96196),o=i(77845),n=i(92542),r=i(55124),l=i(31747),c=i(45369),d=(i(56565),i(69869),e([l]));l=(d.then?(await d)():d)[0];const p="preferred",h="last_used";class u extends s.WF{get _default(){return this.includeLastUsed?h:p}render(){if(!this._pipelines)return s.s6;const e=this.value??this._default;return s.qy`
      <ha-select
        .label=${this.label||this.hass.localize("ui.components.pipeline-picker.pipeline")}
        .value=${e}
        .required=${this.required}
        .disabled=${this.disabled}
        @selected=${this._changed}
        @closed=${r.d}
        fixedMenuPosition
        naturalMenuWidth
      >
        ${this.includeLastUsed?s.qy`
              <ha-list-item .value=${h}>
                ${this.hass.localize("ui.components.pipeline-picker.last_used")}
              </ha-list-item>
            `:null}
        <ha-list-item .value=${p}>
          ${this.hass.localize("ui.components.pipeline-picker.preferred",{preferred:this._pipelines.find(e=>e.id===this._preferredPipeline)?.name})}
        </ha-list-item>
        ${this._pipelines.map(e=>s.qy`<ha-list-item .value=${e.id}>
              ${e.name}
              (${(0,l.T)(e.language,this.hass.locale)})
            </ha-list-item>`)}
      </ha-select>
    `}firstUpdated(e){super.firstUpdated(e),(0,c.nx)(this.hass).then(e=>{this._pipelines=e.pipelines,this._preferredPipeline=e.preferred_pipeline})}_changed(e){const t=e.target;!this.hass||""===t.value||t.value===this.value||void 0===this.value&&t.value===this._default||(this.value=t.value===this._default?void 0:t.value,(0,n.r)(this,"value-changed",{value:this.value}))}constructor(...e){super(...e),this.disabled=!1,this.required=!1,this.includeLastUsed=!1,this._preferredPipeline=null}}u.styles=s.AH`
    ha-select {
      width: 100%;
    }
  `,(0,a.__decorate)([(0,o.MZ)()],u.prototype,"value",void 0),(0,a.__decorate)([(0,o.MZ)()],u.prototype,"label",void 0),(0,a.__decorate)([(0,o.MZ)({attribute:!1})],u.prototype,"hass",void 0),(0,a.__decorate)([(0,o.MZ)({type:Boolean,reflect:!0})],u.prototype,"disabled",void 0),(0,a.__decorate)([(0,o.MZ)({type:Boolean})],u.prototype,"required",void 0),(0,a.__decorate)([(0,o.MZ)({attribute:!1})],u.prototype,"includeLastUsed",void 0),(0,a.__decorate)([(0,o.wk)()],u.prototype,"_pipelines",void 0),(0,a.__decorate)([(0,o.wk)()],u.prototype,"_preferredPipeline",void 0),u=(0,a.__decorate)([(0,o.EM)("ha-assist-pipeline-picker")],u),t()}catch(p){t(p)}})},2076:function(e,t,i){i.a(e,async function(e,t){try{var a=i(62826),s=i(96196),o=i(77845),n=(i(60961),i(88422)),r=e([n]);n=(r.then?(await r)():r)[0];const l="M15.07,11.25L14.17,12.17C13.45,12.89 13,13.5 13,15H11V14.5C11,13.39 11.45,12.39 12.17,11.67L13.41,10.41C13.78,10.05 14,9.55 14,9C14,7.89 13.1,7 12,7A2,2 0 0,0 10,9H8A4,4 0 0,1 12,5A4,4 0 0,1 16,9C16,9.88 15.64,10.67 15.07,11.25M13,19H11V17H13M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12C22,6.47 17.5,2 12,2Z";class c extends s.WF{render(){return s.qy`
      <ha-svg-icon id="svg-icon" .path=${l}></ha-svg-icon>
      <ha-tooltip for="svg-icon" .placement=${this.position}>
        ${this.label}
      </ha-tooltip>
    `}constructor(...e){super(...e),this.position="top"}}c.styles=s.AH`
    ha-svg-icon {
      --mdc-icon-size: var(--ha-help-tooltip-size, 14px);
      color: var(--ha-help-tooltip-color, var(--disabled-text-color));
    }
  `,(0,a.__decorate)([(0,o.MZ)()],c.prototype,"label",void 0),(0,a.__decorate)([(0,o.MZ)()],c.prototype,"position",void 0),c=(0,a.__decorate)([(0,o.EM)("ha-help-tooltip")],c),t()}catch(l){t(l)}})},56565:function(e,t,i){var a=i(62826),s=i(27686),o=i(7731),n=i(96196),r=i(77845);class l extends s.J{renderRipple(){return this.noninteractive?"":super.renderRipple()}static get styles(){return[o.R,n.AH`
        :host {
          padding-left: var(
            --mdc-list-side-padding-left,
            var(--mdc-list-side-padding, 20px)
          );
          padding-inline-start: var(
            --mdc-list-side-padding-left,
            var(--mdc-list-side-padding, 20px)
          );
          padding-right: var(
            --mdc-list-side-padding-right,
            var(--mdc-list-side-padding, 20px)
          );
          padding-inline-end: var(
            --mdc-list-side-padding-right,
            var(--mdc-list-side-padding, 20px)
          );
        }
        :host([graphic="avatar"]:not([twoLine])),
        :host([graphic="icon"]:not([twoLine])) {
          height: 48px;
        }
        span.material-icons:first-of-type {
          margin-inline-start: 0px !important;
          margin-inline-end: var(
            --mdc-list-item-graphic-margin,
            16px
          ) !important;
          direction: var(--direction) !important;
        }
        span.material-icons:last-of-type {
          margin-inline-start: auto !important;
          margin-inline-end: 0px !important;
          direction: var(--direction) !important;
        }
        .mdc-deprecated-list-item__meta {
          display: var(--mdc-list-item-meta-display);
          align-items: center;
          flex-shrink: 0;
        }
        :host([graphic="icon"]:not([twoline]))
          .mdc-deprecated-list-item__graphic {
          margin-inline-end: var(
            --mdc-list-item-graphic-margin,
            20px
          ) !important;
        }
        :host([multiline-secondary]) {
          height: auto;
        }
        :host([multiline-secondary]) .mdc-deprecated-list-item__text {
          padding: 8px 0;
        }
        :host([multiline-secondary]) .mdc-deprecated-list-item__secondary-text {
          text-overflow: initial;
          white-space: normal;
          overflow: auto;
          display: inline-block;
          margin-top: 10px;
        }
        :host([multiline-secondary]) .mdc-deprecated-list-item__primary-text {
          margin-top: 10px;
        }
        :host([multiline-secondary])
          .mdc-deprecated-list-item__secondary-text::before {
          display: none;
        }
        :host([multiline-secondary])
          .mdc-deprecated-list-item__primary-text::before {
          display: none;
        }
        :host([disabled]) {
          color: var(--disabled-text-color);
        }
        :host([noninteractive]) {
          pointer-events: unset;
        }
      `,"rtl"===document.dir?n.AH`
            span.material-icons:first-of-type,
            span.material-icons:last-of-type {
              direction: rtl !important;
              --direction: rtl;
            }
          `:n.AH``]}}l=(0,a.__decorate)([(0,r.EM)("ha-list-item")],l)},28238:function(e,t,i){i.a(e,async function(e,a){try{i.r(t),i.d(t,{HaSelectorUiAction:()=>d});var s=i(62826),o=i(96196),n=i(77845),r=i(92542),l=i(38020),c=e([l]);l=(c.then?(await c)():c)[0];class d extends o.WF{render(){return o.qy`
      <hui-action-editor
        .label=${this.label}
        .hass=${this.hass}
        .config=${this.value}
        .actions=${this.selector.ui_action?.actions}
        .defaultAction=${this.selector.ui_action?.default_action}
        .tooltipText=${this.helper}
        @value-changed=${this._valueChanged}
      ></hui-action-editor>
    `}_valueChanged(e){e.stopPropagation(),(0,r.r)(this,"value-changed",{value:e.detail.value})}}(0,s.__decorate)([(0,n.MZ)({attribute:!1})],d.prototype,"hass",void 0),(0,s.__decorate)([(0,n.MZ)({attribute:!1})],d.prototype,"selector",void 0),(0,s.__decorate)([(0,n.MZ)({attribute:!1})],d.prototype,"value",void 0),(0,s.__decorate)([(0,n.MZ)()],d.prototype,"label",void 0),(0,s.__decorate)([(0,n.MZ)()],d.prototype,"helper",void 0),d=(0,s.__decorate)([(0,n.EM)("ha-selector-ui_action")],d),a()}catch(d){a(d)}})},45369:function(e,t,i){i.d(t,{QC:()=>a,ds:()=>c,mp:()=>n,nx:()=>o,u6:()=>r,vU:()=>s,zn:()=>l});const a=(e,t,i)=>"run-start"===t.type?e={init_options:i,stage:"ready",run:t.data,events:[t],started:new Date(t.timestamp)}:e?((e="wake_word-start"===t.type?{...e,stage:"wake_word",wake_word:{...t.data,done:!1}}:"wake_word-end"===t.type?{...e,wake_word:{...e.wake_word,...t.data,done:!0}}:"stt-start"===t.type?{...e,stage:"stt",stt:{...t.data,done:!1}}:"stt-end"===t.type?{...e,stt:{...e.stt,...t.data,done:!0}}:"intent-start"===t.type?{...e,stage:"intent",intent:{...t.data,done:!1}}:"intent-end"===t.type?{...e,intent:{...e.intent,...t.data,done:!0}}:"tts-start"===t.type?{...e,stage:"tts",tts:{...t.data,done:!1}}:"tts-end"===t.type?{...e,tts:{...e.tts,...t.data,done:!0}}:"run-end"===t.type?{...e,finished:new Date(t.timestamp),stage:"done"}:"error"===t.type?{...e,finished:new Date(t.timestamp),stage:"error",error:t.data}:{...e}).events=[...e.events,t],e):void console.warn("Received unexpected event before receiving session",t),s=(e,t,i)=>e.connection.subscribeMessage(t,{...i,type:"assist_pipeline/run"}),o=e=>e.callWS({type:"assist_pipeline/pipeline/list"}),n=(e,t)=>e.callWS({type:"assist_pipeline/pipeline/get",pipeline_id:t}),r=(e,t)=>e.callWS({type:"assist_pipeline/pipeline/create",...t}),l=(e,t,i)=>e.callWS({type:"assist_pipeline/pipeline/update",pipeline_id:t,...i}),c=e=>e.callWS({type:"assist_pipeline/language/list"})},38020:function(e,t,i){i.a(e,async function(e,t){try{var a=i(62826),s=i(96196),o=i(77845),n=i(22786),r=i(92542),l=i(55124),c=i(56528),d=i(2076),p=(i(56565),i(81657),i(39338)),h=e([c,d,p]);[c,d,p]=h.then?(await h)():h;const u=["more-info","toggle","navigate","url","perform-action","assist","none"],_=[{name:"navigation_path",selector:{navigation:{}}}],v=[{type:"grid",name:"",schema:[{name:"pipeline_id",selector:{assist_pipeline:{include_last_used:!0}}},{name:"start_listening",selector:{boolean:{}}}]}];class g extends s.WF{get _navigation_path(){const e=this.config;return e?.navigation_path||""}get _url_path(){const e=this.config;return e?.url_path||""}get _service(){const e=this.config;return e?.perform_action||e?.service||""}updated(e){super.updated(e),e.has("defaultAction")&&e.get("defaultAction")!==this.defaultAction&&this._select.layoutOptions()}render(){if(!this.hass)return s.s6;const e=this.actions??u;let t=this.config?.action||"default";return"call-service"===t&&(t="perform-action"),s.qy`
      <div class="dropdown">
        <ha-select
          .label=${this.label}
          .configValue=${"action"}
          @selected=${this._actionPicked}
          .value=${t}
          @closed=${l.d}
          fixedMenuPosition
          naturalMenuWidth
        >
          <ha-list-item value="default">
            ${this.hass.localize("ui.panel.lovelace.editor.action-editor.actions.default_action")}
            ${this.defaultAction?` (${this.hass.localize(`ui.panel.lovelace.editor.action-editor.actions.${this.defaultAction}`).toLowerCase()})`:s.s6}
          </ha-list-item>
          ${e.map(e=>s.qy`
              <ha-list-item .value=${e}>
                ${this.hass.localize(`ui.panel.lovelace.editor.action-editor.actions.${e}`)}
              </ha-list-item>
            `)}
        </ha-select>
        ${this.tooltipText?s.qy`
              <ha-help-tooltip .label=${this.tooltipText}></ha-help-tooltip>
            `:s.s6}
      </div>
      ${"navigate"===this.config?.action?s.qy`
            <ha-form
              .hass=${this.hass}
              .schema=${_}
              .data=${this.config}
              .computeLabel=${this._computeFormLabel}
              @value-changed=${this._formValueChanged}
            >
            </ha-form>
          `:s.s6}
      ${"url"===this.config?.action?s.qy`
            <ha-textfield
              .label=${this.hass.localize("ui.panel.lovelace.editor.action-editor.url_path")}
              .value=${this._url_path}
              .configValue=${"url_path"}
              @input=${this._valueChanged}
            ></ha-textfield>
          `:s.s6}
      ${"call-service"===this.config?.action||"perform-action"===this.config?.action?s.qy`
            <ha-service-control
              .hass=${this.hass}
              .value=${this._serviceAction(this.config)}
              .showAdvanced=${this.hass.userData?.showAdvanced}
              narrow
              @value-changed=${this._serviceValueChanged}
            ></ha-service-control>
          `:s.s6}
      ${"assist"===this.config?.action?s.qy`
            <ha-form
              .hass=${this.hass}
              .schema=${v}
              .data=${this.config}
              .computeLabel=${this._computeFormLabel}
              @value-changed=${this._formValueChanged}
            >
            </ha-form>
          `:s.s6}
    `}_actionPicked(e){if(e.stopPropagation(),!this.hass)return;let t=this.config?.action;"call-service"===t&&(t="perform-action");const i=e.target.value;if(t===i)return;if("default"===i)return void(0,r.r)(this,"value-changed",{value:void 0});let a;switch(i){case"url":a={url_path:this._url_path};break;case"perform-action":a={perform_action:this._service};break;case"navigate":a={navigation_path:this._navigation_path}}(0,r.r)(this,"value-changed",{value:{action:i,...a}})}_valueChanged(e){if(e.stopPropagation(),!this.hass)return;const t=e.target,i=e.target.value??e.target.checked;this[`_${t.configValue}`]!==i&&t.configValue&&(0,r.r)(this,"value-changed",{value:{...this.config,[t.configValue]:i}})}_formValueChanged(e){e.stopPropagation();const t=e.detail.value;(0,r.r)(this,"value-changed",{value:t})}_computeFormLabel(e){return this.hass?.localize(`ui.panel.lovelace.editor.action-editor.${e.name}`)}_serviceValueChanged(e){e.stopPropagation();const t={...this.config,action:"perform-action",perform_action:e.detail.value.action||"",data:e.detail.value.data,target:e.detail.value.target||{}};e.detail.value.data||delete t.data,"service_data"in t&&delete t.service_data,"service"in t&&delete t.service,(0,r.r)(this,"value-changed",{value:t})}constructor(...e){super(...e),this._serviceAction=(0,n.A)(e=>({action:this._service,...e.data||e.service_data?{data:e.data??e.service_data}:null,target:e.target}))}}g.styles=s.AH`
    .dropdown {
      position: relative;
    }
    ha-help-tooltip {
      position: absolute;
      right: 40px;
      top: 16px;
      inset-inline-start: initial;
      inset-inline-end: 40px;
      direction: var(--direction);
    }
    ha-select,
    ha-textfield {
      width: 100%;
    }
    ha-service-control,
    ha-navigation-picker,
    ha-form {
      display: block;
    }
    ha-textfield,
    ha-service-control,
    ha-navigation-picker,
    ha-form {
      margin-top: 8px;
    }
    ha-service-control {
      --service-control-padding: 0;
    }
  `,(0,a.__decorate)([(0,o.MZ)({attribute:!1})],g.prototype,"config",void 0),(0,a.__decorate)([(0,o.MZ)({attribute:!1})],g.prototype,"label",void 0),(0,a.__decorate)([(0,o.MZ)({attribute:!1})],g.prototype,"actions",void 0),(0,a.__decorate)([(0,o.MZ)({attribute:!1})],g.prototype,"defaultAction",void 0),(0,a.__decorate)([(0,o.MZ)({attribute:!1})],g.prototype,"tooltipText",void 0),(0,a.__decorate)([(0,o.MZ)({attribute:!1})],g.prototype,"hass",void 0),(0,a.__decorate)([(0,o.P)("ha-select")],g.prototype,"_select",void 0),g=(0,a.__decorate)([(0,o.EM)("hui-action-editor")],g),t()}catch(u){t(u)}})}};
//# sourceMappingURL=8979.05aa1c6b6267d8ff.js.map