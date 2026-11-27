"use strict";(globalThis.rspackChunkesphome_frontend||=[]).push([[386],{1752(e,t,i){var r=i(9104),o=i(5077),a=i(9356),n=i(918),s=i(1556),l=i(5865),d=i(5660),c=i(3140),p=i(325),u=i(8283),h=i(3074),m=i(6910),f=i(2),g=i(2353),v=i(2497);let _=(0,o.AH)`
  esphome-base-dialog {
    --width: 560px;
  }
  esphome-base-dialog::part(body) {
    padding: var(--wa-space-l);
  }
  .field {
    display: flex;
    flex-direction: column;
    gap: var(--wa-space-2xs);
    margin-bottom: var(--wa-space-m);
  }
  .field-desc {
    font-size: var(--wa-font-size-2xs);
    color: var(--wa-color-text-quiet);
    line-height: 1.5;
    margin: 0;
  }
  .field-desc a {
    color: var(--wa-color-brand-fill-loud, #0b5cad);
  }
  .actions {
    display: flex;
    justify-content: flex-end;
    gap: var(--wa-space-s);
    margin-top: var(--wa-space-l);
  }

  .actions button {
    display: inline-flex;
    align-items: center;
    box-sizing: border-box;
    gap: 3px;
    padding: 7px 14px;
    border: var(--wa-border-width-s) solid transparent;
    border-radius: var(--wa-border-radius-m);
    cursor: pointer;
    font-size: var(--wa-font-size-xs);
    font-weight: var(--wa-font-weight-bold);
    font-family: inherit;
    line-height: 1;
    transition:
      background 0.12s,
      border-color 0.12s,
      box-shadow 0.12s,
      transform 0.12s;
  }
  .actions .primary {
    background: var(--esphome-primary);
    color: var(--esphome-on-primary);
    box-shadow: var(--esphome-primary-shadow);
  }
  .actions .primary:hover:not(:disabled) {
    background: var(--esphome-primary-hover);
    box-shadow: var(--esphome-primary-shadow-hover);
    transform: translateY(-1px);
  }
  .actions .primary:active:not(:disabled) {
    transform: translateY(0);
  }
  .actions .primary:disabled {
    background: color-mix(
      in srgb,
      var(--esphome-primary) 35%,
      var(--wa-color-surface-default)
    );
    color: color-mix(in srgb, var(--esphome-on-primary), transparent 30%);
    cursor: not-allowed;
    box-shadow: none;
    transform: none;
  }
  /* Interval-row pairing: matches the editor's inline
     TIME_PERIOD layout so the dialog reads as the same
     kind of compound input the user will see again in the
     section editor. */
  .interval-inputs {
    display: flex;
    align-items: center;
    gap: var(--wa-space-s);
  }
  .interval-inputs > input {
    flex: 1 1 auto;
    min-width: 0;
  }
  .interval-inputs > wa-select {
    flex: 0 0 auto;
    min-width: 6rem;
  }
`;var y=i(318),b=i(2311);i(9218),i(1687),i(4063),i(2522),i(9835);var w=i(6734),x=i(3330);let $=(0,o.AH)`
  .field {
    display: flex;
    flex-direction: column;
    gap: var(--wa-space-2xs);
    margin-bottom: var(--wa-space-m);
  }
  .field-label {
    font-size: var(--wa-font-size-s);
    font-weight: var(--wa-font-weight-semibold);
    color: var(--wa-color-text-normal);
  }
  .error {
    color: var(--esphome-error, #d92d20);
    font-size: var(--wa-font-size-2xs);
    margin-top: var(--wa-space-2xs);
  }
  .component-list {
    display: flex;
    flex-direction: column;
    gap: 2px;
    max-height: 280px;
    overflow-y: auto;
    border: var(--wa-border-width-s) solid var(--wa-color-surface-border);
    border-radius: var(--wa-border-radius-m);
    padding: var(--wa-space-2xs);
  }
  /* The role=group wrapper carries the same column gap as the list, with a
     left rule + indented rows so a group's members read as nested under its
     header and a following loose row (e.g. wifi) is clearly outside it. */
  .component-group-wrap {
    display: flex;
    flex-direction: column;
    gap: 2px;
    border-left: 2px solid var(--wa-color-surface-border);
    margin-left: var(--wa-space-2xs);
    padding-left: var(--wa-space-2xs);
  }
  .component-group-wrap .component-choice {
    padding-left: var(--wa-space-m);
  }
  .component-group {
    font-size: var(--wa-font-size-2xs);
    font-weight: var(--wa-font-weight-semibold);
    color: var(--wa-color-text-quiet);
    text-transform: uppercase;
    letter-spacing: 0.04em;
    margin: var(--wa-space-s) var(--wa-space-2xs) var(--wa-space-2xs);
  }
  /* Trim the leading gap only when a group is the very first row (each
     group now sits in its own wrap, so :first-child on the header would
     match every group). */
  .component-group-wrap:first-child .component-group {
    margin-top: var(--wa-space-2xs);
  }
  .component-group-id {
    text-transform: none;
    letter-spacing: normal;
    font-weight: var(--wa-font-weight-normal);
  }
  .component-choice {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: var(--wa-space-s);
    padding: var(--wa-space-xs) var(--wa-space-s);
    border-radius: var(--wa-border-radius-m);
    cursor: pointer;
    transition: background 0.12s;
  }
  .component-choice:hover,
  .component-choice:focus-visible {
    background: var(--wa-color-surface-lowered);
    outline: none;
  }
  .component-choice--selected {
    background: color-mix(
      in srgb,
      var(--esphome-primary) 14%,
      var(--wa-color-surface-default)
    );
  }
  .component-choice[aria-disabled="true"] {
    opacity: 0.55;
    cursor: default;
    pointer-events: none;
  }
  .component-choice-name {
    font-size: var(--wa-font-size-s);
    color: var(--wa-color-text-normal);
  }
  .component-domain {
    flex: 0 0 auto;
    font-size: var(--wa-font-size-2xs);
    color: var(--wa-color-text-quiet);
    background: var(--wa-color-surface-default);
    border: var(--wa-border-width-s) solid var(--wa-color-surface-border);
    border-radius: var(--wa-border-radius-s);
    padding: 1px 6px;
  }
`;function k(e,t,i,r){var o,a=arguments.length,n=a<3?t:null===r?r=Object.getOwnPropertyDescriptor(t,i):r;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)n=Reflect.decorate(e,t,i,r);else for(var s=e.length-1;s>=0;s--)(o=e[s])&&(n=(a<3?o(n):a>3?o(t,i,n):o(t,i))||n);return a>3&&n&&Object.defineProperty(t,i,n),n}let z={ArrowDown:1,ArrowRight:1,ArrowUp:-1,ArrowLeft:-1};class C extends o.WF{render(){let{plan:e,order:t}=this._plan();return 0===t.length?(0,o.qy)`<p class="error" role="status">
        ${this._localize("device.automation_target_no_components")}
      </p>`:(0,o.qy)`<div class="field">
      <label class="field-label" id="component-target-label">
        ${this._localize("device.automation_wizard_pick_component")}
      </label>
      <div
        class="component-list"
        role="radiogroup"
        aria-labelledby="component-target-label"
        @keydown=${e=>this._onKeydown(e,t)}
      >
        ${e.map(e=>{var i;if(!("header"in e))return this._renderChoice(e,t);let r=(i=e.header,`component-group-${i.id}`);return(0,o.qy)`<div
            class="component-group-wrap"
            role="group"
            aria-labelledby=${e.heading?r:o.s6}
            aria-label=${e.heading?o.s6:(0,y.zl)(e.header)}
          >
            ${e.heading?(0,o.qy)`<p class="component-group" id=${r}>
                    ${(0,y.zl)(e.header)}
                    <span class="component-group-id">(${e.header.component_id})</span>
                  </p>`:o.s6}
            ${e.subs.map(e=>this._renderChoice(e,t))}
          </div>`})}
      </div>
    </div>`}_plan(){let e=new Set(this.devices.filter(e=>e.is_entity_container).map(e=>e.id)),t=new Map;for(let i of this.devices){if(!i.parent_id||!e.has(i.parent_id))continue;let r=t.get(i.parent_id)??[];r.push(i),t.set(i.parent_id,r)}let i=[],r=[];for(let o of this.devices)if(o.is_entity_container){let e=t.get(o.id)??[],a=(0,y.e1)(o,this.triggers);if(a&&(i.push(o),r.push(o.id)),0===e.length)continue;i.push({header:o,subs:e,heading:!a}),r.push(...e.map(e=>e.id))}else o.parent_id&&e.has(o.parent_id)||(i.push(o),r.push(o.id));return{plan:i,order:r}}_renderChoice(e,t){let i=e.id===this.value,r=i||!t.includes(this.value)&&t[0]===e.id;return(0,o.qy)`<div
      class="component-choice ${i?"component-choice--selected":""}"
      role="radio"
      aria-checked=${i?"true":"false"}
      aria-disabled=${this.disabled?"true":"false"}
      data-id=${e.id}
      tabindex=${r?"0":"-1"}
      @click=${()=>this._select(e.id)}
    >
      <span class="component-choice-name truncate">${(0,y.zl)(e)}</span>
      <span class="component-domain">${e.component_id}</span>
    </div>`}_onKeydown(e,t){if(this.disabled||0===t.length)return;let i=e.target?.closest(".component-choice"),r=i?.dataset.id??null;if("Enter"===e.key||" "===e.key){r&&(e.preventDefault(),this._select(r));return}let o=z[e.key]??0;if(0===o)return;e.preventDefault();let a=r?t.indexOf(r):-1,n=t[(a+o+t.length)%t.length];this._select(n),this.updateComplete.then(()=>{let e=this.shadowRoot?.querySelector(`.component-choice[data-id="${n}"]`);e?.focus()})}_select(e){this.disabled||(0,x.r)(this,"component-change",{componentId:e})}constructor(...e){super(...e),this._localize=e=>e,this.devices=[],this.triggers=[],this.value="",this.disabled=!1}}function q(e,t,i,r){var o,a=arguments.length,n=a<3?t:null===r?r=Object.getOwnPropertyDescriptor(t,i):r;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)n=Reflect.decorate(e,t,i,r);else for(var s=e.length-1;s>=0;s--)(o=e[s])&&(n=(a<3?o(n):a>3?o(t,i,n):o(t,i))||n);return a>3&&n&&Object.defineProperty(t,i,n),n}C.styles=[c.G9,w.U,$],k([(0,r.Fg)({context:s.$F,subscribe:!0}),(0,a.wk)()],C.prototype,"_localize",void 0),k([(0,a.MZ)({attribute:!1})],C.prototype,"devices",void 0),k([(0,a.MZ)({attribute:!1})],C.prototype,"triggers",void 0),k([(0,a.MZ)()],C.prototype,"value",void 0),k([(0,a.MZ)({type:Boolean})],C.prototype,"disabled",void 0),C=k([(0,a.EM)("esphome-component-target-picker")],C);class S extends o.WF{open(e){this._prefilled=void 0!==e,this._kind=e?.kind??"device_on",this._componentId=e?.kind==="component_on"?e.componentId:"",this._prefillComponentId=this._componentId,this._triggerId=null,this._intervalValue="",this._intervalUnit="s",this._error="",this._dialog.open=!0,this._loadAvailable()}get _devices(){return this._available?.devices??[]}get _triggers(){return this._available?.triggers??[]}async _loadAvailable(){if(this._api&&this.configuration){this._loading=!0;try{this._available=await this._api.getAvailableAutomations(this.configuration,this.yaml);let e=this._prefillContainer();e&&(this._componentId=(0,y.Oj)((0,y.Fi)(this._devices,e),this._triggers)?.id??""),this._preselectUniqueTrigger()}catch(e){this._error=(0,u.u)(e)}finally{this._loading=!1}}}_prefillContainer(){if(!this._prefilled||"component_on"!==this._kind||!this._prefillComponentId)return;let e=this._available?.devices.find(e=>e.id===this._prefillComponentId);return e?.is_entity_container?e:void 0}render(){let e=this.boardName?this._localize("device.add_automation_dialog_title",{name:this.boardName}):this._localize("device.add_automation");return(0,o.qy)`<esphome-base-dialog
      ?open=${this._dialog.open}
      ?busy=${this._saving}
      .label=${e}
      .confirmOnEnter=${this._onContinue}
      @request-close=${this._dialog.onRequestClose}
    >
      ${this._loading&&!this._available?(0,o.qy)`<div style="text-align: center; padding: 32px;">
              <wa-spinner></wa-spinner>
            </div>`:this._renderForm()}
    </esphome-base-dialog>`}_renderForm(){let e=this._filteredTriggers(),t="interval"===this._kind,i=!this._prefilled,r=this._prefillContainer(),a="component_on"===this._kind&&(!this._prefilled||!!r),n=!!r&&!(0,y.Oj)((0,y.Fi)(this._devices,r),this._triggers);return(0,o.qy)`
      <p class="intro">
        ${(0,m.Gc)(this._localize("device.automation_header_description"))}
      </p>
      ${i?(0,o.qy)`<div class="field">
              <label class="field-label" id="kind-label">
                ${this._localize("device.automation_wizard_pick_target")}
              </label>
              <wa-select
                aria-labelledby="kind-label"
                value=${this._kind}
                ?disabled=${this._saving}
                @change=${e=>this._onKindChange(e.target.value)}
              >
                <wa-option value="device_on" ?selected=${"device_on"===this._kind}>
                  ${this._localize("device.automation_target_device")}
                </wa-option>
                <wa-option
                  value="component_on"
                  ?selected=${"component_on"===this._kind}
                >
                  ${this._localize("device.automation_target_component")}
                </wa-option>
                <wa-option value="interval" ?selected=${"interval"===this._kind}>
                  ${this._localize("device.automation_target_interval")}
                </wa-option>
              </wa-select>
            </div>`:o.s6}
      ${n?(0,o.qy)`<p class="field-desc">
              ${this._localize("device.automation_container_no_entities")}
            </p>`:(0,o.qy)`
              ${a?this._renderComponentRow(r):o.s6}
              ${"interval"===this._kind?this._renderIntervalRow():o.s6}
              ${!t?this._renderTriggerRow(e):o.s6}
            `}
      ${this._error?(0,o.qy)`<p class="error" role="alert">${this._error}</p>`:o.s6}
      <div class="actions">
        <button
          type="button"
          class="primary"
          ?disabled=${this._saving||!this._canContinue()}
          @click=${this._onContinue}
        >
          ${this._saving?this._localize("device.adding"):this._localize("device.add_automation_continue")}
        </button>
      </div>
    `}_renderComponentRow(e){let t=(0,y.Fi)(this._devices,e);return(0,o.qy)`<esphome-component-target-picker
      .devices=${t}
      .triggers=${this._triggers}
      .value=${this._componentId}
      ?disabled=${this._saving}
      @component-change=${e=>this._onComponentChange(e.detail.componentId)}
    ></esphome-component-target-picker>`}_renderIntervalRow(){return(0,o.qy)`<div class="field">
      <label class="field-label" id="interval-label">
        ${this._localize("device.automation_interval_label")}
      </label>
      <div class="interval-inputs">
        <input
          type="text"
          inputmode="decimal"
          aria-labelledby="interval-label"
          .value=${this._intervalValue}
          placeholder="0"
          ?disabled=${this._saving}
          @input=${e=>{this._intervalValue=e.target.value}}
        />
        <wa-select
          aria-label=${this._localize("device.automation_action_delay_unit")}
          ?disabled=${this._saving}
          @change=${e=>{this._intervalUnit=e.target.value}}
        >
          ${(0,f.ze)("ms",this._intervalUnit).map(e=>(0,o.qy)`<wa-option value=${e} ?selected=${e===this._intervalUnit}
                >${this._localize(`device.automation_action_delay_unit_${e}`)}</wa-option
              >`)}
        </wa-select>
      </div>
    </div>`}_renderTriggerRow(e){if(0===e.length)return(0,o.qy)`<p class="error">
        ${this._localize("device.automation_trigger_none_available")}
      </p>`;let t=e.find(e=>e.id===this._triggerId);return(0,o.qy)`<div class="field">
      <label class="field-label" id="trigger-label">
        ${this._localize("device.automation_wizard_pick_trigger")}
      </label>
      <wa-select
        aria-labelledby="trigger-label"
        value=${this._triggerId??""}
        ?disabled=${this._saving}
        @change=${e=>this._triggerId=e.target.value}
      >
        ${e.map(e=>(0,o.qy)`<wa-option value=${e.id} ?selected=${e.id===this._triggerId}>
              ${e.name}
            </wa-option>`)}
      </wa-select>
      ${t?.description?(0,o.qy)`<p class="field-desc">${(0,m.Gc)(t.description)}</p>`:o.s6}
    </div>`}_filteredTriggers(){let e=this._triggers;if("device_on"===this._kind){let t=this._existingDeviceTriggers();return e.filter(e=>e.is_device_level&&(!t.has(e.id)||e.supports_list))}if("component_on"===this._kind){let t=this._available?.devices.find(e=>e.id===this._componentId),i=this._existingComponentTriggers(this._componentId);return(0,y.mR)(e,t).filter(e=>!i.has((0,g.y1)(e.id))||e.supports_list)}return[]}_existingDeviceTriggers(){let e=new Set;for(let t of(0,v.vB)(this.yaml))"esphome"===t.parentKey&&t.eventKey&&e.add(t.eventKey);return e}_existingComponentTriggers(e){let t=new Set;for(let i of(0,v.vB)(this.yaml))i.id===e&&i.eventKey&&t.add(i.eventKey);return t}_onKindChange(e){this._kind=e,this._triggerId=null,"component_on"===e?this._componentId=(0,y.Oj)(this._devices,this._triggers)?.id??"":this._componentId="",this._preselectUniqueTrigger()}_onComponentChange(e){this._componentId=e,this._triggerId=null,this._preselectUniqueTrigger()}_preselectUniqueTrigger(){let e=this._filteredTriggers();1===e.length&&(this._triggerId=e[0].id)}_canContinue(){return"interval"===this._kind?""!==this._intervalValue.trim():!!this._triggerId&&("component_on"!==this._kind||!!this._componentId)}_buildLocation(){if("device_on"===this._kind){let e=this._available?.triggers.find(e=>e.id===this._triggerId);if(e?.supports_list){let e=(0,v.vB)(this.yaml).filter(e=>"esphome"===e.parentKey&&e.eventKey===this._triggerId).length;return{kind:"device_on",trigger:this._triggerId,index:e}}return{kind:"device_on",trigger:this._triggerId}}if("component_on"===this._kind){let e=(0,g.y1)(this._triggerId),t=this._available?.triggers.find(e=>e.id===this._triggerId);if(t?.supports_list){let t=(0,v.vB)(this.yaml).filter(t=>t.id===this._componentId&&t.eventKey===e).length;return{kind:"component_on",component_id:this._componentId,trigger:e,index:t}}return{kind:"component_on",component_id:this._componentId,trigger:e}}return{kind:"interval",index:(0,v.vB)(this.yaml).filter(e=>"interval"===e.parentKey).length}}_catalogTriggerId(e){return"interval"===e.kind?null:this._triggerId}constructor(...e){super(...e),this._localize=e=>e,this.boardName="",this.configuration="",this.yaml="",this.board=null,this._dialog=new p.T(this),this._kind="device_on",this._componentId="",this._prefillComponentId="",this._triggerId=null,this._prefilled=!1,this._intervalValue="",this._intervalUnit="s",this._available=null,this._loading=!0,this._saving=!1,this._error="",this._onContinue=async()=>{if(this._api&&this._canContinue()&&!this._saving){this._saving=!0,this._error="";try{let e=this._buildLocation(),t={trigger_id:this._catalogTriggerId(e),trigger_params:"interval"===this._kind?{interval:`${this._intervalValue.trim()}${this._intervalUnit}`}:{},actions:[]},i=this.configuration,r=this.yaml,{yaml_diff:o}=await this._api.upsertAutomation(i,t,e,r);(0,b.K)(this,i,r,e,o),this._dialog.open=!1}catch(t){let e=(0,h.K)(t,this._localize,"device.automation_save_error");this._error=e,(0,n.UG)(this._localize("device.automation_save_error"),{description:e})}finally{this._saving=!1}}}}}S.styles=[c.G9,d.z9,l.h,_],q([(0,r.Fg)({context:s.$F,subscribe:!0}),(0,a.wk)()],S.prototype,"_localize",void 0),q([(0,r.Fg)({context:s.Ie})],S.prototype,"_api",void 0),q([(0,a.MZ)()],S.prototype,"boardName",void 0),q([(0,a.MZ)()],S.prototype,"configuration",void 0),q([(0,a.MZ)()],S.prototype,"yaml",void 0),q([(0,a.MZ)({attribute:!1})],S.prototype,"board",void 0),q([(0,a.wk)()],S.prototype,"_kind",void 0),q([(0,a.wk)()],S.prototype,"_componentId",void 0),q([(0,a.wk)()],S.prototype,"_prefillComponentId",void 0),q([(0,a.wk)()],S.prototype,"_triggerId",void 0),q([(0,a.wk)()],S.prototype,"_prefilled",void 0),q([(0,a.wk)()],S.prototype,"_intervalValue",void 0),q([(0,a.wk)()],S.prototype,"_intervalUnit",void 0),q([(0,a.wk)()],S.prototype,"_available",void 0),q([(0,a.wk)()],S.prototype,"_loading",void 0),q([(0,a.wk)()],S.prototype,"_saving",void 0),q([(0,a.wk)()],S.prototype,"_error",void 0),q([(0,a.EM)("esphome-add-automation-dialog")],S)},7427(e,t,i){var r=i(9104),o=i(289),a=i(5077),n=i(9356),s=i(1556),l=i(6848),d=i(6016),c=i(3140),p=i(5413),u=i(2765),h=i(8310),m=i(4125),f=i(2497);let g={uart:{claims:{require_rx:"rx_pin",require_tx:"tx_pin"},settings:{baud_rate:null,data_bits:"8",parity:"NONE",stop_bits:"1"}}};function v(e){for(let t of e.dependencies??[]){if(!g[t])continue;let i=e.bus_constraints?.[t];if(i)return{domain:t,constraints:i}}return null}var _=i(6092),y=i(325),b=i(5795),w=i(3330),x=i(3074),$=i(2919),k=i(918),z=i(1093),C=i(2761),q=i(8851),S=i(5016),A=i(874),O=i(565),M=i(6670),E=i(6295),I=i(1254);function P(e,t){let i=e.config_entries;return(e.dependencies??[]).filter(e=>{let r=i.filter(t=>t.references_component===e);return 0===r.length||!r.every(e=>R(e,t,i))})}function R(e,t,i){let r=(0,O.Dw)(e,t,void 0,i);return null!=r&&!(0,O.zO)(e,r)}function L(e,t,i,r=[],o=(0,C.Cm)()){if(0===e.length)return[];let a=i??(0,q.Zn)(t),n=(0,q.u)(t),s=(0,$.H)(n,t,r),l=new Set;for(let e of n){let t=e.indexOf(".");-1!==t&&l.add(e.slice(t+1))}return e.filter(e=>!(0,S.p)(a,e)&&(e.includes(".")?!s.has(e):!(o&&!(0,I.Po)(o).has(e)&&l.has(e))))}async function F(e,t,i,r){let o=new Set,a=t.filter(e=>!e.includes("."));if(0===a.length)return o;let n=r.platform?(0,S.bk)(r.platform):void 0;return await Promise.all(a.map(async t=>{for(let a of(await (0,M.wI)(e,t,n,r.boardId??void 0)))if((0,S.p)(i,a)){o.add(t);break}})),o}function N(e,t,i,r,o){if(!o)return[];let a=new Set,n=e=>o.components.filter(t=>t.provides?.includes(e)).map(t=>(0,A.G_)(t,e));for(let s of e){let l=s.references_component;if(!l||!s.references_class||s.locked||!t.includes(l)||R(s,i,e)||a.has(l))continue;let d=(0,A.Zm)(r,l,n(l));(0,E.m)(r,d,s,o.byId).noneMatch&&a.add(l)}return[...a]}var D=i(1919),j=i(4008),T=i(7169),B=i(4117);function K(e){let t=e._detourStack[e._detourStack.length-1];return t?(e._detourStack=e._detourStack.slice(0,-1),e._selected=t.component,e._returnValues=t.values,e._depPrefill=t.values&&t.prefill?{...t.prefill,fields:{}}:t.prefill,t):null}async function V(e,t,i){let r=++e._selectionSeq,o=i??e.board?.id??void 0;try{let[i]=await Promise.all([(0,B.Sn)(e._api,t,e.platform||void 0,o),(0,C.ak)(e._api)]);if(r!==e._selectionSeq)return{kind:"stale"};if(!i)return{kind:"error",message:e._localize("device.add_component_load_failed")};return{kind:"ok",entry:i}}catch(t){if(r!==e._selectionSeq)return{kind:"stale"};return{kind:"error",message:(0,x.K)(t,e._localize,"device.add_component_error")}}}let U=(0,a.AH)`
  esphome-base-dialog {
    --width: 900px;
  }

  esphome-base-dialog.form-view {
    --width: 480px;
  }

  /* Primary header + 40x40 close + .back-button come from
     primaryHeaderDialogStyles (dialog-chrome.ts). */
  esphome-base-dialog::part(body) {
    padding: var(--wa-space-l);
  }

  /* Breadcrumb that shows up while the user is detoured into
     "add a dependency" mid-way through adding another component.
     Tells them we'll bring them back to the original after. */
  .return-banner {
    margin-bottom: var(--wa-space-m);
    padding: var(--wa-space-2xs) var(--wa-space-s);
    background: var(--esphome-tint);
    border-left: 3px solid var(--esphome-primary);
    border-radius: var(--wa-border-radius-s);
    font-size: var(--wa-font-size-xs);
    color: var(--wa-color-text-quiet);
  }

  .return-banner strong {
    color: var(--wa-color-text-normal);
    font-weight: var(--wa-font-weight-semibold);
  }

  .bundle-banner {
    display: flex;
    align-items: center;
    gap: var(--wa-space-xs);
    margin-bottom: var(--wa-space-m);
    padding: var(--wa-space-xs) var(--wa-space-s);
    background: var(--esphome-tint);
    border-left: 3px solid var(--esphome-primary);
    border-radius: var(--wa-border-radius-s);
    font-size: var(--wa-font-size-xs);
    color: var(--wa-color-text-normal);
  }

  .bundle-banner wa-icon {
    font-size: 14px;
    color: var(--esphome-primary);
  }

  /* Surfaces a hydrate / WS-transport failure on the catalog
     view; the form's own banner is unreachable when _selected
     is still null. */
  .catalog-error {
    margin-bottom: var(--wa-space-m);
    padding: var(--wa-space-xs) var(--wa-space-s);
    background: color-mix(in srgb, var(--wa-color-danger-60), transparent 88%);
    border-left: 3px solid var(--wa-color-danger-60);
    border-radius: var(--wa-border-radius-s);
    font-size: var(--wa-font-size-s);
    color: var(--wa-color-text-normal);
  }
`;var Z=i(2943),H=i(271),G=i(8175);function W(e,t){let i={};for(let r of e){if(r.hidden)continue;let e=t[r.key];if(r.type===j.Hh.NESTED){let t=r.config_entries??[];if(r.multi_value){let o=(0,G.ly)(e).map(e=>W(t,e)).filter(e=>Object.keys(e).length>0);o.length>0&&(i[r.key]=o);continue}let o=W(t,(0,G.qY)(e));Object.keys(o).length>0&&(i[r.key]=o);continue}if(void 0!==e){if(Array.isArray(e)){if(0===e.length)continue;i[r.key]=e;continue}if(""===e){r.required&&(i[r.key]=e);continue}r.type===j.Hh.INTEGER&&"hex"!==r.display_format?i[r.key]=(0,H.s)(e):r.type===j.Hh.FLOAT?i[r.key]="number"==typeof e&&Number.isFinite(e)?e:(0,Z.aY)(r,String(e)):r.type===j.Hh.BOOLEAN?i[r.key]="string"==typeof e?(0,Z.aY)(r,e):e:i[r.key]=e}}return i}var Y=i(3508),Q=i(1379);function J(e,t,i){return(0,Q.xx)({requiredOnly:!0,showAdvanced:!1,presentComponents:i,board:t,values:e})}var X=i(1150);function ee(e){return e.replace(/ /g,"_").toLowerCase().replace(/[^a-z0-9_-]/g,"_")}let et=new Set(["esphome","esp32_ble"]);var ei=i(9508);function er(e,t,i,r={}){for(let o of e){if(o.type===j.Hh.NESTED){let e=er(o.config_entries??[],t,[...i,o.key],r);if(e)return e;continue}if(o.references_component===t){let e=[...i,o.key];if(void 0!==(0,G.O6)(r,e))continue;return e}}return null}function eo(e){let{entries:t,component:i,board:r,yaml:o,prefillReference:a,prefillFields:n,restoredValues:s,localize:l}=e,d=function e(t,i,r,o=!1,a=null){let n={};for(let s of t){if(s.type===j.Hh.NESTED){let t=e(s.config_entries??[],i,r,o,a);s.required&&null!=s.platform_type&&void 0===t.name&&void 0===t.id&&(t.name=(0,ei.H)(s,r)),Object.keys(t).length>0&&(n[s.key]=t);continue}if(s.required||o&&s.from_preset){if(s.references_component&&!s.locked){let{candidates:e}=(0,E.m)(i,(0,A.Zm)(i,s.references_component,[]),s,a),t=o&&s.from_preset&&"string"==typeof s.default_value&&e.some(e=>e.id===s.default_value)?s.default_value:void 0,r=!!s.references_class&&!a,l=t??(r?void 0:(0,A.z)(e,i)?.id);void 0!==l?n[s.key]=s.multi_value?[l]:l:s.multi_value&&s.required&&(n[s.key]=[]);continue}null!=s.default_value?n[s.key]=s.multi_value?Array.isArray(s.default_value)?[...s.default_value]:[String(s.default_value)]:s.default_value:s.multi_value&&s.required&&(n[s.key]=[])}}return n}(t,o,l,(0,b.sO)(i.id),e.catalogById),c=d;if(t.find(e=>"id"===e.key&&e.type===j.Hh.ID)&&void 0===c.id){let e=(0,_.fW)(i.id,!0===i.multi_conf,(0,_.Y0)(o));null!==e&&(c={...c,id:e})}if(t.find(e=>"name"===e.key&&e.type===j.Hh.STRING)&&void 0===c.name){let e=function(e,t,i){var r,o;if((0,b.sO)(e)||et.has(e))return null;let a=t.trim();if(!a)return null;let n=(r=i,o=(0,A.iZ)(e).domain,(0,X.p)(r,"name",o)),s=new Set;for(let e of n){let t=ee(e);t&&s.add(t)}if(!s.has(ee(a)))return a;let l=2,d=`${a} ${l}`;for(;s.has(ee(d));)l++,d=`${a} ${l}`;return d}(i.id,i.name,o);null!==e&&(c={...c,name:e})}if(c=function(e,t,i,r,o){if(!i?.pins?.length||e.includes("."))return r;let a=r,n=new Set;for(let r of t){if(r.type!==j.Hh.PIN||void 0!==a[r.key])continue;let t=r.key.toLowerCase().replace(/_(pin|gpio)$/,""),s=`${e}_${t}`,l=i.pins.find(e=>e.features.includes(s)&&!o.has(e.gpio)&&!n.has(e.gpio));l&&(n.add(l.gpio),a={...a,[r.key]:l.gpio})}return a}(i.id,t,r,c,(0,A.zq)(o)),s&&(c={...c,...s}),a){let i=er(t,a.domain,[],d),r=i&&function e(t,i){let[r,...o]=i,a=t.find(e=>e.key===r);return o.length&&a?e(a.config_entries??[],o):a}(t,i),n=[{id:a.id}],s=!!r?.references_class&&!e.catalogById;i&&!s&&(!r||(0,E.m)(o,n,r,e.catalogById).candidates.length>0)&&(c=(0,G.Oe)(c,i,a.id))}return n&&(c={...c,...n}),c}let ea=new Set(["adc","dac","ota"]);function en(e){return e?"featured"===e?"Recommended":e.split("_").filter(e=>e.length>0).map(e=>ea.has(e.toLowerCase())?e.toUpperCase():e[0].toUpperCase()+e.slice(1)).join(" "):""}var es=i(7491);i(9218),i(2522),i(9835);var el=i(1502),ed=i(1404),ec=i(5660);class ep{hostConnected(){this._unsubscribe=(0,B.Ej)(()=>{this._host.requestUpdate()})}hostDisconnected(){this._unsubscribe?.(),this._unsubscribe=void 0}resolve(e){return(0,B.CQ)(e,this._getPlatform())?.name??e}kickoff(e){let t=this._getApi();if(!t)return;let i=this._getPlatform();for(let r of e)void 0===(0,B.CQ)(r,i)&&(0,B.Sn)(t,r,i).catch(()=>{})}constructor(e,t,i){this._host=e,this._getApi=t,this._getPlatform=i,e.addController(this)}}var eu=i(6185),eh=i(6910);let em={blocked:null,picker:null,reference:null};function ef(e,t){if(!t?.length)return e;let i=new Set(t);return e.map(e=>i.has(e.key)&&!e.required?{...e,required:!0}:e)}function eg(e,t){return t&&0!==Object.keys(t).length?e.map(e=>{let i=t[e.key];if(!i?.length||e.multi_value)return e;let r=new Map((e.options??[]).map(e=>[e.value,e]));return{...e,options:i.map(e=>r.get(String(e))??{label:String(e),value:String(e)}),default_value:e.type===j.Hh.STRING?String(i[0]):i[0]}}):e}let ev=(0,a.AH)`
  :host {
    display: block;
  }

  .form {
    display: flex;
    flex-direction: column;
    gap: var(--wa-space-m);
  }

  .form-desc {
    margin: 0 0 var(--wa-space-m);
    font-size: var(--wa-font-size-s);
    color: var(--wa-color-text-quiet);
  }

  .field {
    display: flex;
    flex-direction: column;
    gap: var(--wa-space-xs);
  }

  label {
    font-size: var(--wa-font-size-s);
    font-weight: var(--wa-font-weight-bold);
    color: var(--wa-color-text-normal);
  }

  label .required {
    color: var(--esphome-error);
    margin-left: 2px;
  }

  select {
    width: 100%;
    padding: 9px 14px;
    font-size: var(--wa-font-size-s);
    font-family: inherit;
    color: var(--wa-color-text-normal);
    background: var(--wa-color-surface-raised);
    border: var(--wa-border-width-s) solid var(--wa-color-surface-border);
    border-radius: var(--wa-border-radius-l);
    box-sizing: border-box;
    outline: none;
    transition:
      border-color 0.15s,
      box-shadow 0.15s;
  }

  select:focus {
    border-color: var(--esphome-primary);
    box-shadow: var(--esphome-focus-ring);
  }

  select.invalid {
    border-color: var(--esphome-error);
  }

  select:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }

  .field-error {
    color: var(--esphome-error);
    font-size: var(--wa-font-size-xs);
  }

  .array-row {
    display: flex;
    gap: var(--wa-space-xs);
  }

  .array-row input {
    flex: 1;
  }

  .array-btn {
    background: none;
    border: var(--wa-border-width-m) solid var(--wa-color-surface-border);
    border-radius: var(--wa-border-radius-m);
    padding: 0 var(--wa-space-s);
    cursor: pointer;
    font-family: inherit;
    color: var(--wa-color-text-normal);
  }

  .array-btn:hover:not(:disabled) {
    background: var(--wa-color-surface-lowered);
  }

  .array-btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }

  .yaml-preview {
    margin: 0;
    padding: var(--wa-space-s) var(--wa-space-m);
    background: var(--wa-color-surface-lowered);
    border: var(--wa-border-width-s) solid var(--wa-color-surface-border);
    border-radius: var(--wa-border-radius-m);
    font-family: var(--wa-font-family-code, monospace);
    font-size: var(--wa-font-size-xs);
    white-space: pre;
    overflow-x: auto;
    color: var(--wa-color-text-normal);
  }

  .toggle-link {
    background: none;
    border: none;
    padding: 0;
    color: var(--esphome-primary);
    cursor: pointer;
    font-size: var(--wa-font-size-xs);
    text-decoration: underline;
    align-self: flex-start;
  }

  .actions {
    display: flex;
    justify-content: flex-end;
    gap: var(--wa-space-s);
    padding-top: var(--wa-space-m);
  }

  /* Deltas over the shared .btn chrome (dialogActionButtonStyles,
     layered before this module in the host's static styles): icon +
     label sit inline-centred, disabled applies to every variant (this
     form's variants are .btn-primary / .btn-secondary, not the shared
     modifier classes), and the opacity change is animated. */
  .btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 6px;
    transition:
      background 0.12s,
      opacity 0.12s;
  }

  .btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }

  .btn-secondary {
    background: var(--wa-color-surface-lowered);
    color: var(--wa-color-text-normal);
    border: var(--wa-border-width-s) solid var(--wa-color-surface-border);
  }

  .btn-secondary:hover:not(:disabled) {
    background: var(--wa-color-surface-border);
  }

  .btn-primary {
    background: var(--esphome-primary);
    color: var(--esphome-on-primary);
  }

  .btn-primary:hover:not(:disabled) {
    background: var(--esphome-primary-hover);
  }

  .error {
    color: var(--esphome-error);
    font-size: var(--wa-font-size-s);
  }

  /* Banner shown when the component has unmet dependencies
     (e.g. a gpio light needs a configured output: first). */
  .deps-warning {
    display: flex;
    gap: var(--wa-space-s);
    padding: var(--wa-space-s) var(--wa-space-m);
    background: color-mix(in srgb, var(--esphome-warning, #d97706), transparent 88%);
    border: var(--wa-border-width-s) solid var(--esphome-warning, #d97706);
    border-radius: var(--wa-border-radius-m);
    color: var(--wa-color-text-normal);
    font-size: var(--wa-font-size-s);
    line-height: 1.45;
  }

  .deps-warning wa-icon {
    flex-shrink: 0;
    font-size: 20px;
    color: var(--esphome-warning, #d97706);
  }

  .deps-warning-body {
    display: flex;
    flex-direction: column;
    gap: var(--wa-space-2xs);
    flex: 1;
    min-width: 0;
  }

  .deps-warning-title {
    font-weight: var(--wa-font-weight-bold);
  }

  .deps-warning-actions {
    display: flex;
    flex-wrap: wrap;
    gap: var(--wa-space-2xs);
    margin-top: var(--wa-space-2xs);
  }

  .dep-button {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    padding: 4px 10px;
    background: var(--esphome-warning, #d97706);
    color: var(--esphome-on-primary, white);
    border: none;
    border-radius: var(--wa-border-radius-m);
    font-family: inherit;
    font-size: var(--wa-font-size-xs);
    font-weight: var(--wa-font-weight-bold);
    cursor: pointer;
    transition: opacity 0.12s;
  }

  .dep-button:hover {
    opacity: 0.9;
  }
`;var e_=i(7869);i(4355);var ey=i(2564);function eb(e,t,i,r){var o,a=arguments.length,n=a<3?t:null===r?r=Object.getOwnPropertyDescriptor(t,i):r;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)n=Reflect.decorate(e,t,i,r);else for(var s=e.length-1;s>=0;s--)(o=e[s])&&(n=(a<3?o(n):a>3?o(t,i,n):o(t,i))||n);return a>3&&n&&Object.defineProperty(t,i,n),n}(0,z.C)({"alert-circle-outline":o.mdiAlertCircleOutline});class ew extends a.WF{get currentValues(){return{...this._values}}requestSubmit(){this.submitting||this._onSubmit()}disconnectedCallback(){super.disconnectedCallback(),clearTimeout(this._liveValidateTimer)}get _entries(){return this._overlayOptions(this._overlayRequired(this.component.config_entries,this._mergedExtraRequired(this.extraRequired,this._busPickerKey)),this.optionOverrides)}willUpdate(e){super.willUpdate(e),(e.has("component")||!this._initialized)&&this.component&&(this._initialized=!0,clearTimeout(this._liveValidateTimer),this._busBlockedDep=null,this._busPickerKey=null,this._initValues(),this._localBlockMessage="",this._depResolver.kickoff(this.component.dependencies??[]));let t=e.has("component")||e.has("yaml")||e.has("board");(t||e.has("resolvedComponents")||e.has("resolvedPlatforms"))&&this._resolveProvidedDeps(),t&&this._resolveBusHostability()}_visibilityPresence(){return this._widenPresence(this.yaml,this.resolvedComponents)}_missingDeps(e){var t;let i,r,o,a,n,s;return r=L(i=P((t={component:this.component,entries:this._entries,values:this._values,yaml:this.yaml,present:e,resolvedPlatforms:this.resolvedPlatforms,provided:this._providedDeps,busBlocked:this._busBlockedDep,index:this._catalogIndex.index()}).component,t.values),t.yaml,t.present,t.resolvedPlatforms,t.index).filter(e=>!t.provided.has(e)),a=new Set(o=N(t.entries,i,t.values,t.yaml,t.index)),t.busBlocked&&i.includes(t.busBlocked)&&a.add(t.busBlocked),s=1===(n=[...r,...[...a].filter(e=>!r.includes(e))]).length&&n[0]===t.busBlocked?"device.bus_dependency_in_use":n.every(e=>o.includes(e))?"device.wrong_kind_dependency":"device.missing_dependencies",{deps:n,copy:s}}async _resolveProvidedDeps(){let e=++this._providesSeq;this._providedDeps.size&&(this._providedDeps=new Set);let t=this._api,i=this.component?.dependencies??[];if(!t||0===i.length)return;let r=this._visibilityPresence(),o=L(i,this.yaml,r,this.resolvedPlatforms);if(0!==o.length)try{let i=await F(t,o,r,{platform:this.board?.esphome.platform??null,boardId:this.board?.id??null});e===this._providesSeq&&(i.size||this._providedDeps.size)&&(this._providedDeps=i)}catch(e){console.warn("[add-component-form] provides lookup failed",e)}}async _resolveBusHostability(){let e=++this._busAssessSeq,t=this._api,i=t&&this.component?await async function(e,t,i,r){let o=v(t);if(!o||(0,A.eN)(i))return em;let a=await (0,C.ak)(e);if(0===a.byId.size)return em;let{busCount:n,compatibleIds:s}=function(e,t,i,r){let o=g[t],a=(0,m.MT)(e),n=(0,u.D)(e),s=e=>(e.parentKey??e.key)===t,l=a.filter(s).map(t=>{let i=(0,h.wz)(e,t.key,t.fromLine);return{id:t.id??null,values:i,readable:Object.keys(i).length>0&&!(0,m.tv)(n,t),claimed:new Set}});if(0===l.length)return{busCount:0,compatibleIds:[]};if(!o||a.some(e=>(e.parentKey??e.key)==="host"))return{busCount:l.length,compatibleIds:l.map(e=>e.id)};let d=`${t}_id`;for(let i of a){if(s(i))continue;let a=r((0,f.gU)(i))?.[t];if(!a)continue;let n=function(e,t,i,r){let o=(0,h.wz)(e,t.key,t.fromLine)[i];return void 0!==o?r.find(e=>e.id===String(o))??null:1===r.length?r[0]:null}(e,i,d,l);if(n)for(let[e,t]of Object.entries(o.claims))!0===a[e]&&n.claimed.add(t)}let c=l.filter(e=>(function(e,t,i){for(let[r,o]of Object.entries(i.claims))if(!0===t[r]&&(e.claimed.has(o)||e.readable&&!Object.prototype.hasOwnProperty.call(e.values,o)))return!1;if(!e.readable)return!0;for(let[r,o]of Object.entries(i.settings)){let i=t[r];if(null==i)continue;let a=function(e,t,i){let r=e.values[t];if(null==r)return i;let o=String(r);return(0,p.RB)(o)?null:o}(e,r,o);if(null===a)continue;let n=(Array.isArray(i)?i:[i]).filter(e=>"string"==typeof e||"number"==typeof e);if(0!==n.length&&!n.some(e=>a.toUpperCase()===String(e).toUpperCase()))return!1}return!0})(e,i,o)).map(e=>e.id);return{busCount:l.length,compatibleIds:c}}(i,o.domain,o.constraints,e=>a.byId.get(e)?.bus_constraints),l=n>1?s.filter(e=>null!==e):s;if(n>0&&0===l.length){let t=o.domain;try{let a=(0,q.Zn)(i);(await F(e,[o.domain],a,{platform:r?.esphome.platform??null,boardId:r?.id??null})).has(o.domain)&&(t=null)}catch(e){console.warn("[add-component-form] bus provider lookup failed",e)}return{...em,blocked:t}}if(1===l.length){let e=l[0];return null===e?em:{...em,reference:{domain:o.domain,id:e}}}if(l.length>1){let e=er(t.config_entries,o.domain,[]);if(e?.length===1)return{...em,picker:e[0]}}return em}(t,this.component,this.yaml,this.board):em;if(e===this._busAssessSeq&&(this._busBlockedDep!==i.blocked&&(this._busBlockedDep=i.blocked),this._busPickerKey!==i.picker&&(this._busPickerKey=i.picker),i.reference)){let e=er(this.component.config_entries,i.reference.domain,[],this._values);e&&(this._values=(0,G.Oe)(this._values,e,i.reference.id))}}_initValues(){this._values=eo({entries:this._entries,component:this.component,board:this.board,yaml:this.yaml,prefillReference:this.prefillReference,prefillFields:this.prefillFields,restoredValues:this.restoredValues,localize:this._localize,catalogById:(0,C.Cm)()?.byId})}render(){let e=this.submitting,t=this._visibilityPresence(),{deps:i,copy:r}=this._missingDeps(t),o=(0,O.JK)(this._entries,this._values,t,this.board?.esphome.platform??null),n=!this._hasRequiredErrors(o)&&!this._hasUnsatisfiedConstraint(t);return(0,a.qy)`
      <div class="form">
        <p class="form-desc">${(0,eh.Gc)(this.component.description)}</p>
        ${i.length>0?this._renderMissingDeps(i,r):a.s6}
        <esphome-config-entry-form
          .entries=${this._entries}
          .requiredGroups=${this.component.required_groups??[]}
          .values=${this._values}
          .errors=${this._errors}
          .board=${this.board}
          .yaml=${this.yaml}
          .sectionKey=${this._sectionKey}
          .presentComponents=${t}
          ?disabled=${e}
          ?required-only=${!0}
          @value-change=${this._onValueChange}
        ></esphome-config-entry-form>
        <button
          type="button"
          class="toggle-link"
          @click=${()=>{this._showYaml=!this._showYaml}}
        >
          ${this._showYaml?this._localize("device.yaml_preview_toggle"):this._localize("device.yaml_preview")}
        </button>
        ${this._showYaml?(0,a.qy)`<pre class="yaml-preview">${this._generateYamlPreview()}</pre>`:a.s6}
        ${this.submitError?(0,a.qy)`<p class="error">${this.submitError}</p>`:a.s6}
        ${this._localBlockMessage?(0,a.qy)`<p class="error">${this._localBlockMessage}</p>`:a.s6}
        <div class="actions">
          <button
            class="btn btn-secondary"
            ?disabled=${e}
            @click=${this._onCancel}
          >
            ${this._localize("wizard.back")}
          </button>
          <button
            class="btn btn-primary"
            ?disabled=${e||!n||i.length>0}
            @click=${this._onSubmit}
          >
            ${this.submitting?this._localize("device.adding"):this._localize("device.add_component_action")}
          </button>
        </div>
      </div>
    `}_depsBlockTitle(e){return this._localize(`${e}_title`,{name:this.component.name})}_renderMissingDeps(e,t){return(0,a.qy)`
      <div class="deps-warning" role="alert">
        <wa-icon library="mdi" name="alert-circle-outline"></wa-icon>
        <div class="deps-warning-body">
          <div class="deps-warning-title">${this._depsBlockTitle(t)}</div>
          <div>${this._localize(`${t}_body`)}</div>
          <div class="deps-warning-actions">
            ${e.map(e=>(0,a.qy)`<button
                  type="button"
                  class="dep-button"
                  @click=${()=>this._onAddDep(e)}
                >
                  ${this._localize("device.missing_dependencies_add",{domain:this._depResolver.resolve(e)})}
                </button>`)}
          </div>
        </div>
      </div>
    `}_onAddDep(e){(0,w.r)(this,"navigate-to-dep",{domain:e})}_hasRequiredErrors(e){for(let t of e.values())if("validation.required"===t.code)return!0;return!1}_labelForErrorKey(e){let t=(0,eu.vB)(this._entries,e.split("."));return t?(0,ey.HL)(t,this._localize):e}_hasUnsatisfiedConstraint(e){var t,i,r,o;return t=this._entries,i=this._values,r=this.component.required_groups??[],o=this.board,(0,Y.c4)(t,i,r,J(i,o,e)).unmet.some(e=>e.actionable)}_anyErrorIsVisible(e,t){var i,r,o,a;if(0===e.size)return!1;let n=(i=this._entries,r=this._values,o=this.component.required_groups??[],a=this.board,(0,Q.tX)(i,r,{...J(r,a,t),requiredGroups:o}));for(let t of e.keys())if(n.has(t))return!0;return!1}_onValueChange(e){let{path:t,value:i}=e.detail;this._values=(0,G.Oe)(this._values,t,i),clearTimeout(this._liveValidateTimer);let r=t.join("."),o=(0,O.bj)(this._entries,t,i),a=this._errors,n=(0,O.iL)(a,r);if(0===o.size)n&&(this._errors=n);else{let e=n??new Map(a),i=null!==n;for(let[t,r]of o)a.has(t)&&(e.set(t,r),i=!0);i&&(this._errors=e),this._liveValidateTimer=setTimeout(()=>{let e=(0,O.bj)(this._entries,t,(0,G.O6)(this._values,t)),i=(0,O.iL)(this._errors,r);if(!i&&!e.size)return;let o=i??new Map(this._errors);for(let[t,i]of e)o.set(t,i);this._errors=o},ew.LIVE_VALIDATE_DEBOUNCE_MS)}this._localBlockMessage&&(this._localBlockMessage="")}get _sectionKey(){return(0,b.Ze)(this.component.id,this.board)}_generateYamlPreview(){let e=[`${this._sectionKey}:`];return e.push(...(0,q.ym)(this._values,"  ")),e.join("\n")}_onCancel(){(0,w.r)(this,"form-cancel")}_onSubmit(){clearTimeout(this._liveValidateTimer),this._localBlockMessage="";let e=this._visibilityPresence(),{deps:t,copy:i}=this._missingDeps(e);if(t.length>0){this._localBlockMessage=`${this._depsBlockTitle(i)} (${t.join(", ")})`;return}if(this._hasUnsatisfiedConstraint(e))return;let r=(0,O.JK)(this._entries,this._values,e,this.board?.esphome.platform??null);if(r.size>0){if(this._errors=r,!this._anyErrorIsVisible(r,e)){let e=[...r.entries()].map(([e,t])=>`${this._labelForErrorKey(e)}: ${this._localize(t.code,t.params)}`).join("; ");this._localBlockMessage=`${this._localize("device.add_component_hidden_validation_error")} (${e})`}return}this._errors=new Map,this._localBlockMessage="";let o=W(this._entries,this._values);(0,w.r)(this,"form-submit",{fields:o})}constructor(...e){super(...e),this._localize=e=>e,this._catalogIndex=new e_.C(this,()=>this._api),this.board=null,this.yaml="",this.resolvedComponents=[],this.resolvedPlatforms=[],this.prefillReference=null,this.prefillFields=null,this.extraRequired=null,this.restoredValues=null,this.optionOverrides=null,this.submitting=!1,this.submitError="",this._values={},this._errors=new Map,this._localBlockMessage="",this._showYaml=!1,this._providedDeps=new Set,this._providesSeq=0,this._busBlockedDep=null,this._busPickerKey=null,this._busAssessSeq=0,this._depResolver=new ep(this,()=>this._api,()=>this.board?.esphome.platform||void 0),this._overlayRequired=(0,el.A)(ef),this._overlayOptions=(0,el.A)(eg),this._mergedExtraRequired=(0,el.A)((e,t)=>t?[...e??[],t]:e),this._initialized=!1,this._widenPresence=(0,el.A)((e,t)=>(0,$.H)((0,q.Zn)(e),e,t))}}ew.LIVE_VALIDATE_DEBOUNCE_MS=200,ew.styles=[c.G9,ec.z9,ed.V,ev],eb([(0,r.Fg)({context:s.$F,subscribe:!0}),(0,n.wk)()],ew.prototype,"_localize",void 0),eb([(0,r.Fg)({context:s.Ie})],ew.prototype,"_api",void 0),eb([(0,n.MZ)({attribute:!1})],ew.prototype,"component",void 0),eb([(0,n.MZ)({attribute:!1})],ew.prototype,"board",void 0),eb([(0,n.MZ)()],ew.prototype,"yaml",void 0),eb([(0,n.MZ)({attribute:!1})],ew.prototype,"resolvedComponents",void 0),eb([(0,n.MZ)({attribute:!1})],ew.prototype,"resolvedPlatforms",void 0),eb([(0,n.MZ)({attribute:!1})],ew.prototype,"prefillReference",void 0),eb([(0,n.MZ)({attribute:!1})],ew.prototype,"prefillFields",void 0),eb([(0,n.MZ)({attribute:!1})],ew.prototype,"extraRequired",void 0),eb([(0,n.MZ)({attribute:!1})],ew.prototype,"restoredValues",void 0),eb([(0,n.MZ)({attribute:!1})],ew.prototype,"optionOverrides",void 0),eb([(0,n.MZ)({type:Boolean})],ew.prototype,"submitting",void 0),eb([(0,n.MZ)()],ew.prototype,"submitError",void 0),eb([(0,n.wk)()],ew.prototype,"_values",void 0),eb([(0,n.wk)()],ew.prototype,"_errors",void 0),eb([(0,n.wk)()],ew.prototype,"_localBlockMessage",void 0),eb([(0,n.wk)()],ew.prototype,"_showYaml",void 0),eb([(0,n.wk)()],ew.prototype,"_providedDeps",void 0),eb([(0,n.wk)()],ew.prototype,"_busBlockedDep",void 0),eb([(0,n.wk)()],ew.prototype,"_busPickerKey",void 0),ew=eb([(0,n.EM)("esphome-add-component-form")],ew);var ex=i(8719),e$=i(6734),ek=i(4996),ez=i(9295),eC=i(1188),eq=i(1448);class eS{hostConnected(){this._observer.observe(this._host)}hostDisconnected(){this._observer.disconnect()}constructor(e,t){this._host=e,this._observer=new ResizeObserver(t),e.addController(this)}}var eA=i(2814),eO=i(2743),eM=i(1148);let eE=(0,el.A)(q.Zn),eI=(0,el.A)(q.u),eP=(0,el.A)(_.gO);function eR(e,t){let i=e.fields?.id?.value;return"string"==typeof i&&t.has(i)}function eL(e,t){return!!e.locked_pins&&(0,A.cN)(t,(0,A.iZ)(e.component_id).domain,e.locked_pins)}function eF(e){let t=eE(e.yaml),i=eI(e.yaml),r=e.lockedCategories.length>0,o=r?(0,$.H)(t,e.yaml,e.resolvedComponents):t,a=e._components.filter(t=>(0,O.Cs)(t.supported_platforms,e.platform)),n=r?new Set(a.map(e=>e.id)):null,s=new Map,l=e.board;if(l)for(let e of l.featured_components??[])s.set((0,b.m0)(l.id,e.id),e);let d=s.size?eP(e.yaml):new Set;return a.filter(r=>{let a=s.get(r.id);if(a&&(eR(a,d)||eL(a,e.yaml)))return!1;let l=a?.component_id??r.id;if(!r.multi_conf&&(0,S.by)(l,t,i))return!1;let c=r.dependencies??[];return(!(n&&r.id.includes("."))||!(c.length>0)||!!c.every(e=>n.has(e)||(0,S.p)(o,e)))&&!0})}let eN=(0,el.A)((e,t)=>{let i=e?.featured_bundles??[];if(!e||0===i.length)return new Set;let r=new Map;for(let t of e.featured_components??[]){let e=t.fields?.id?.value;"string"==typeof e&&r.set(t.id,e)}let o=eP(t),a=new Set;for(let e of i){let t=e.component_ids.map(e=>r.get(e)).filter(e=>void 0!==e);t.length>0&&t.every(e=>o.has(e))&&a.add(e.id)}return a});function eD(e){let t=eN(e.board,e.yaml);return(e.board?.featured_bundles??[]).filter(e=>!t.has(e.id))}function ej(e){let t=(e._search??"").trim();return eD(e).filter(e=>(0,eM.K)(t,e.name,e.description,e.id))}function eT(e,t){let i=e.board;if(!i)return 0;let r=i.featured_components??[],o=eE(e.yaml),a=eI(e.yaml),n=r.length?eP(e.yaml):new Set,s=t?.applyQuery??!0,l=s?(e._search??"").trim():"";return r.filter(t=>!eR(t,n)&&!eL(t,e.yaml)&&(!1!==t.multi_conf||!(0,S.by)(t.component_id,o,a))&&(0,eM.K)(l,t.name??void 0,t.description??void 0,t.id)).length+(s?ej(e):eD(e)).length}var eB=i(1020);function eK(e){let t=e.target;return!t?.closest("a, button")}function eV(e,t){return(0,a.qy)`<span
      id=${e}
      class="component-category-chip component-category-chip--recommended"
      tabindex=${t?"0":"-1"}
      >${en("featured")}</span
    >
    ${t?(0,a.qy)`<wa-tooltip for=${e}>${t}</wa-tooltip>`:a.s6}`}function eU(e,t){let i=e._expandedId===t;return(0,a.qy)`<button
    class="expand-button"
    type="button"
    aria-pressed=${i}
    aria-label=${e._localize("wizard.expand_board")}
    title=${e._localize("wizard.expand_board")}
    @click=${()=>e._onToggleExpand(t)}
  >
    ${(0,eB.R)(i?o.mdiArrowCollapseAll:o.mdiArrowExpandAll)}
  </button>`}let eZ=(0,a.AH)`
  :host {
    display: flex;
    height: 480px;
    gap: 0;
  }

  :host([hidden]) {
    display: none;
  }

  .sidebar {
    width: 160px;
    flex-shrink: 0;
    display: flex;
    flex-direction: column;
    gap: var(--wa-space-2xs);
    padding-right: var(--wa-space-m);
    border-right: 1px solid var(--wa-color-surface-border);
    overflow-y: auto;
  }

  .sidebar-label {
    font-size: var(--wa-font-size-xs);
    font-weight: var(--wa-font-weight-bold);
    color: var(--wa-color-text-subtle);
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin: 0 0 var(--wa-space-2xs);
    flex-shrink: 0;
  }

  .category-btn {
    border: none;
    background: none;
    cursor: pointer;
    text-align: left;
    padding: var(--wa-space-xs) var(--wa-space-s);
    border-radius: var(--wa-border-radius-m);
    font-size: var(--wa-font-size-s);
    font-weight: var(--wa-font-weight-semibold);
    color: var(--wa-color-text-normal);
    transition: background 0.1s;
    font-family: inherit;
    flex-shrink: 0;
  }

  .category-btn:hover {
    background: var(--esphome-tint);
    color: var(--esphome-primary);
  }

  .category-btn--active {
    background: var(--esphome-tint);
    color: var(--esphome-primary);
  }

  .category-btn-inner {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: var(--wa-space-xs);
  }

  .category-count {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    min-width: 18px;
    height: 18px;
    padding: 0 4px;
    border-radius: 9px;
    font-size: var(--wa-font-size-xs);
    font-weight: var(--wa-font-weight-bold);
    background: var(--wa-color-surface-raised);
    color: var(--wa-color-text-subtle);
    flex-shrink: 0;
    box-sizing: border-box;
  }

  .category-btn--active .category-count {
    background: var(--esphome-primary);
    color: var(--esphome-on-primary);
  }

  .main {
    flex: 1;
    min-width: 0;
    display: flex;
    flex-direction: column;
    gap: var(--wa-space-m);
    padding-left: var(--wa-space-m);
    padding-top: 3px;
    padding-right: 3px;
    overflow: hidden;
  }

  input[type="search"] {
    flex-shrink: 0;
  }

  .result-count {
    font-size: var(--wa-font-size-2xs);
    color: var(--wa-color-text-quiet);
    flex-shrink: 0;
    margin-top: -6px;
  }

  .grid-scroll {
    flex: 1;
    overflow-y: auto;
    overflow-x: hidden;
    padding-right: var(--wa-space-2xs);
  }

  /* auto-fill + minmax so the grid drops 2 → 1 column as soon as a card
     would shrink below ~340px — avoids hard viewport breakpoints. */
  .components-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
    gap: 8px;
    align-content: start;
  }

  /* Below the shared phone breakpoint (modal viewport on phones) collapse sidebar into a
     horizontal chip row above the grid. */
  @media (max-width: ${600}px) {
    /* The dialog hosting the catalog goes full-screen on phones, so fill the
       available height (the body's flex track) rather than capping at 70vh,
       which would leave the bottom of the screen empty. */
    :host {
      flex-direction: column;
      height: 100%;
    }

    .sidebar {
      width: 100%;
      flex-direction: row;
      gap: var(--wa-space-2xs);
      padding-right: 0;
      padding-bottom: var(--wa-space-s);
      margin-bottom: var(--wa-space-s);
      overflow-x: auto;
      overflow-y: hidden;
      border-right: none;
      border-bottom: 1px solid var(--wa-color-surface-border);
    }

    .sidebar-label {
      display: none;
    }

    .category-btn {
      flex-shrink: 0;
      white-space: nowrap;
    }

    .main {
      padding-left: 0;
      padding-right: 0;
    }

    /* Drop the desktop 340px column floor: in the full-screen mobile dialog
       the body is narrower than 340px on small phones (e.g. 375px − padding),
       and minmax(340px, …) would force a track wider than the viewport and
       clip the cards. A single minmax(0, 1fr) column shrinks to fit. */
    .components-grid {
      grid-template-columns: minmax(0, 1fr);
    }
  }

  .component-card {
    border-radius: var(--wa-border-radius-l);
    border: var(--wa-border-width-s) solid var(--wa-color-surface-border);
    background: var(--wa-color-surface-default);
    padding: var(--wa-space-s) var(--wa-space-m);
    box-sizing: border-box;
    min-width: 0;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    gap: 6px;
    cursor: pointer;
    transition:
      border-color var(--wa-transition-normal) var(--wa-transition-easing),
      background var(--wa-transition-normal) var(--wa-transition-easing);
  }

  .component-card:hover {
    border-color: var(--esphome-primary);
    background: var(--esphome-tint-faint);
  }

  .component-card:focus-within {
    border-color: var(--esphome-primary);
  }

  .component-card--expanded {
    grid-column: 1 / -1;
  }

  .expand-button {
    border: none;
    background: none;
    cursor: pointer;
    padding: 2px;
    border-radius: 4px;
    display: inline-flex;
    align-items: center;
    flex-shrink: 0;
    color: var(--esphome-primary);
    font-size: 15px;
  }

  .expand-button:focus-visible {
    outline: var(--esphome-focus-outline);
    outline-offset: 1px;
  }

  .component-card-header {
    display: flex;
    align-items: center;
    gap: 8px;
  }

  .component-image,
  .component-image--placeholder {
    width: 56px;
    height: 56px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: var(--wa-border-radius-m);
    background: var(--wa-color-surface-subtle);
    flex-shrink: 0;
    color: var(--esphome-primary);
    font-size: 28px;
    box-sizing: border-box;
  }

  .component-image {
    padding: 4px;
  }

  .component-image img {
    width: 100%;
    height: 100%;
    object-fit: contain;
  }

  /* ESPHome's monochrome SVG illustrations are black-on-transparent —
     invert + hue-rotate in dark mode (apply-theme.ts root var). Scoped
     to SVGs so JPGs/PNGs keep their original colours. */
  .component-image img[src$=".svg"] {
    filter: var(--esphome-svg-filter, none);
  }

  .component-card-header-text {
    flex: 1;
    min-width: 0;
  }

  .component-title {
    margin: 0;
    font-size: var(--wa-font-size-xs);
    font-weight: var(--wa-font-weight-bold);
    color: var(--wa-color-text-normal);
    line-height: 1.3;
  }

  /* Category chip disambiguates same-name catalog entries (sensor.debug
     vs text_sensor.debug). Only shown under "All" / "Featured" — see
     shouldShowCategoryChip. */
  .component-category-chip {
    display: inline-block;
    margin-top: 2px;
    padding: 0 6px;
    font-size: 9px;
    font-weight: var(--wa-font-weight-semibold);
    line-height: 1.6;
    color: var(--wa-color-text-quiet);
    background: var(--wa-color-surface-raised);
    border: 1px solid var(--wa-color-border);
    border-radius: 999px;
    text-transform: uppercase;
    letter-spacing: 0.04em;
  }

  /* Board-recommendation identity: same pill as its sibling chips so the
     row reads as one family, recolored primary so it stands out from the
     muted category chips (frontend #1220). */
  .component-category-chip--recommended {
    color: var(--esphome-primary);
    background: var(--esphome-tint);
    border-color: var(--esphome-primary);
    font-weight: var(--wa-font-weight-bold);
  }

  /* Focusable (tabindex) so keyboard users can raise the explainer
     tooltip; wa-tooltip's default trigger is hover+focus. */
  .component-category-chip--recommended:focus-visible {
    outline: none;
    box-shadow: var(--esphome-focus-ring-tight);
  }

  .component-description {
    margin: 0;
    font-size: var(--wa-font-size-2xs);
    color: var(--wa-color-text-quiet);
    line-height: 1.4;
  }

  .card-footer {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: var(--wa-space-xs);
    margin-top: auto;
  }

  .more-info {
    display: inline-flex;
    align-items: center;
    gap: 2px;
    font-size: var(--wa-font-size-2xs);
    color: var(--esphome-primary);
    text-decoration: none;
  }

  .more-info:hover {
    text-decoration: underline;
  }

  .more-info svg {
    font-size: 11px;
  }

  .select-component {
    display: flex;
    align-items: center;
    gap: 3px;
    border: none;
    background: none;
    padding: 0;
    border-radius: 4px;
    font-family: inherit;
    font-size: var(--wa-font-size-2xs);
    font-weight: var(--wa-font-weight-bold);
    color: var(--esphome-primary);
    cursor: pointer;
  }

  .select-component:focus-visible {
    outline: var(--esphome-focus-outline);
    outline-offset: 3px;
  }

  .empty {
    text-align: center;
    color: var(--wa-color-text-quiet);
    font-size: var(--wa-font-size-s);
    padding: var(--wa-space-xl);
    grid-column: 1 / -1;
  }

  .loading {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--wa-color-text-quiet);
    font-size: var(--wa-font-size-s);
  }

  /* Featured cards read as the curated set via a thicker edge in the same
     neutral border color — distinguished by weight, not hue, so it stays
     subtle. Drawn as an inset ring (box-shadow), not a wider border, so the
     box model — and thus the card size — matches the regular cards beside it. */
  .component-card--featured {
    --featured-ring: var(--wa-color-surface-border);
    box-shadow: inset 0 0 0 var(--wa-border-width-s) var(--featured-ring);
    /* transition doesn't accumulate across rules, so restate the base card's
       animated properties alongside the ring. */
    transition:
      border-color var(--wa-transition-normal) var(--wa-transition-easing),
      box-shadow var(--wa-transition-normal) var(--wa-transition-easing),
      background var(--wa-transition-normal) var(--wa-transition-easing);
  }

  /* Track the border's primary highlight on hover / focus so the ring doesn't
     stay a stale neutral while the border lights up. */
  .component-card--featured:hover,
  .component-card--featured:focus-within {
    --featured-ring: var(--esphome-primary);
  }

  .bundle-badge {
    display: inline-flex;
    align-items: center;
    gap: 2px;
    font-size: var(--wa-font-size-2xs);
    font-weight: var(--wa-font-weight-bold);
    color: var(--esphome-primary);
    background: var(--esphome-tint);
    border-radius: var(--wa-border-radius-s);
    padding: 1px 6px;
  }

  .bundle-badge svg {
    font-size: 11px;
  }
`;function eH(e,t,i,r){var o,a=arguments.length,n=a<3?t:null===r?r=Object.getOwnPropertyDescriptor(t,i):r;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)n=Reflect.decorate(e,t,i,r);else for(var s=e.length-1;s>=0;s--)(o=e[s])&&(n=(a<3?o(n):a>3?o(t,i,n):o(t,i))||n);return a>3&&n&&Object.defineProperty(t,i,n),n}i(1306);class eG extends a.WF{get _components(){return this._list.items}get _total(){return this._list.total}_prefersFeatured(){return 0===this.lockedCategories.length&&!!this.boardId&&eT(this,{applyQuery:!1})>0}_recommendationInclusive(){return this._category===D._.FEATURED||"all"===this._category}load(){this._provides="",this._prefersFeatured()?this._category=D._.FEATURED:this._category===D._.FEATURED&&(this._category="all"),this._fetchComponents()}filterByDomain(e){let t=(0,C.Cm)();null!==t&&(0,I.Po)(t).has(e)?(this._search="",this._provides="",this._category=e):(this._search=e,this._provides=e,this._category="all"),this._fetchComponents()}_fetchComponents(){let e=this._search.trim()||void 0,t=this.lockedCategories.length>0,i={category:t?this.lockedCategories:"all"!==this._category?this._category:void 0,exclude_category:!t&&this.excludeCategories.length>0?this.excludeCategories:void 0,platform:this.platform||void 0,board_id:this.boardId||void 0},r=this._provides;this._list.reset(async(t,o)=>{let a=r?await this._api.getComponents({...i,offset:t,limit:o,provides:r}):await this._api.getComponents({...i,offset:t,limit:o,query:e});return 0===t&&r&&0===a.components.length&&(this._provides="",r="",a=await this._api.getComponents({...i,offset:t,limit:o,query:e})),0===t&&(this._categories=a.categories),{items:a.components,total:a.total}})}firstUpdated(){document.fonts?.ready.then(()=>this._measureDescriptionOverflow())}updated(){this._measureDescriptionOverflow(),this._list.loading||0!==this.lockedCategories.length||this._category!==D._.FEATURED||this._provides||eF(this).length+ej(this).length!==0||(this._category="all",this._fetchComponents())}render(){var e;let t,i,r,n,s,l,d,c;if(this._list.loading&&!this._list.hasLoaded)return(0,a.qy)`<div class="loading">
        ${this._localize("device.loading_components")}
      </div>`;let p=(e=this._localize,t=new Set(this.excludeCategories),i=this._categories.filter(e=>!t.has(e.id)),r=this.lockedCategories.length?0:eT(this),n=i.filter(e=>e.id!==D._.FEATURED),s=t.size?n.reduce((e,t)=>e+t.count,0)+r:this._total,l=new Intl.Collator(void 0,{sensitivity:"base"}),d=n.map(e=>({id:e.id,label:en(e.id),count:e.count})).sort((e,t)=>l.compare(e.label,t.label)),c=[],r>0&&c.push({id:D._.FEATURED,label:e("device.component_category_featured"),count:r}),c.push({id:"all",label:e("device.component_category_all"),count:s}),c.push(...d),c),u=0===this.lockedCategories.length,h=this._recommendationInclusive()?ej(this):[],m=eF(this),f=function(e){let t=new Map;for(let i of e){let e=JSON.stringify([i.category,i.name]),r=t.get(e);r?r.push(i):t.set(e,[i])}let i=new Set;for(let e of t.values())if(e.length>1)for(let t of e)i.add(t.id);return i}(m);return(0,a.qy)`
      ${u?(0,a.qy)`<div class="sidebar">
              <p class="sidebar-label">
                ${this._localize("device.component_categories")}
              </p>
              ${p.map(({id:e,label:t,count:i})=>(0,a.qy)`
                  <button
                    class="category-btn ${this._category===e?"category-btn--active":""}"
                    type="button"
                    @click=${()=>{this._category=e,this._provides="",this._fetchComponents()}}
                  >
                    <span class="category-btn-inner">
                      <span>${t}</span>
                      <span class="category-count">${i}</span>
                    </span>
                  </button>
                `)}
            </div>`:a.s6}
      <div class="main">
        <input
          type="search"
          autocomplete="off"
          .value=${this._search}
          @input=${this._onSearchInput}
          placeholder=${this._localize("device.search_components_placeholder")}
        />
        ${!this._list.loading?(0,a.qy)`<span class="result-count"
                >${this._localize("device.components_count",{visible:m.length+h.length,total:this._total+h.length})}</span
              >`:a.s6}
        <div class="grid-scroll">
          <div class="components-grid">
            ${this._list.loading?(0,a.qy)`<p class="empty">
                    ${this._localize("device.loading_components")}
                  </p>`:m.length+h.length?(0,a.qy)`
                      ${h.map(e=>{var t;let i,r,n,s,l;return t=this,i=!!e.image_url&&!t._imageFailed.has(e.id),r=t.board?t._localize("device.recommended_chip_tooltip",{board:t.board.name}):"",n=`bundle.${e.id}`,l=(s=t._expandedId===n)||t._overflowingDescriptions.has(n),(0,a.qy)`
    <article
      class="component-card component-card--featured ${s?"component-card--expanded":""}"
      @click=${i=>{eK(i)&&t._onAddBundle(e)}}
    >
      <div class="component-card-header">
        ${i?(0,a.qy)`<div class="component-image">
                <img
                  src=${e.image_url}
                  alt=${e.name}
                  referrerpolicy="no-referrer"
                  loading="lazy"
                  @error=${()=>t._onImageError(e.id)}
                />
              </div>`:(0,a.qy)`<div class="component-image--placeholder">
                ${(0,eB.R)(o.mdiPackageVariantClosed)}
              </div>`}
        <div class="component-card-header-text">
          <h3 class="component-title truncate">${e.name}</h3>
          ${eV(`recommended-chip-bundle-${e.id}`,r)}
        </div>
        <span class="bundle-badge">
          ${(0,eB.R)(o.mdiPackageVariantClosed)}
          ${t._localize("device.featured_bundle_badge")}
        </span>
        ${l?eU(t,n):a.s6}
      </div>
      ${e.description?(0,a.qy)`<p
              class="component-description ${s?"":"component-description--clamp line-clamp-2"}"
              data-component-id=${n}
            >
              ${(0,eh.Gc)(e.description)}
            </p>`:a.s6}
      <div class="card-footer">
        <span></span>
        <button
          class="select-component"
          type="button"
          @click=${()=>t._onAddBundle(e)}
        >
          ${(0,eB.R)(o.mdiPlus)} ${t._localize("device.add_component_action")}
        </button>
      </div>
    </article>
  `})}
                      ${m.map(e=>(function(e,t,i,r,n,s=!1){var l,d;let c,p=!!t.image_url&&!e._imageFailed.has(t.id),u=i||e._overflowingDescriptions.has(t.id),h="all"===(l=e._category)||"featured"===l?en((r?t.underlying_category:t.category)??""):"",m=s?-1===(c=(d=t.id).indexOf("."))?"":d.slice(c+1).split("_").filter(e=>e.length>0).map(e=>e.toUpperCase()).join(" "):"",f=r&&e.board?n("device.recommended_chip_tooltip",{board:e.board.name}):"";return(0,a.qy)`
    <article
      class="component-card ${i?"component-card--expanded":""} ${r?"component-card--featured":""}"
      @click=${i=>{eK(i)&&e._onAdd(t)}}
    >
      <div class="component-card-header">
        ${p?(0,a.qy)`<div class="component-image">
                <img
                  src=${t.image_url}
                  alt=${t.name}
                  referrerpolicy="no-referrer"
                  loading="lazy"
                  @error=${()=>e._onImageError(t.id)}
                />
              </div>`:(0,a.qy)`<div class="component-image--placeholder">${(0,eB.R)(o.mdiMemory)}</div>`}
        <div class="component-card-header-text">
          <h3 class="component-title truncate">${t.name}</h3>
          ${r?eV(`recommended-chip-${t.id}`,f):a.s6}
          ${h?(0,a.qy)`<span class="component-category-chip">${h}</span>`:a.s6}
          ${m?(0,a.qy)`<span class="component-category-chip">${m}</span>`:a.s6}
        </div>
        ${u?eU(e,t.id):a.s6}
      </div>
      <p
        class="component-description ${i?"":"component-description--clamp line-clamp-2"}"
        data-component-id=${t.id}
      >
        ${(0,eh.Gc)(t.description)}
      </p>
      <div class="card-footer">
        ${(0,eh.RQ)(t.docs_url)?(0,a.qy)`<a
                class="more-info"
                href=${t.docs_url}
                target="_blank"
                rel="noopener noreferrer"
              >
                ${n("device.more_info")} ${(0,eB.R)(o.mdiOpenInNew)}
              </a>`:(0,a.qy)`<span></span>`}
        <button
          class="select-component"
          type="button"
          @click=${()=>e._onAdd(t)}
        >
          ${(0,eB.R)(o.mdiPlus)} ${n("device.add_component_action")}
        </button>
      </div>
    </article>
  `})(this,e,e.id===this._expandedId,(0,b.sO)(e.id),this._localize,f.has(e.id)))}
                    `:(0,a.qy)`<p class="empty">
                      ${this._localize(this._list.hasError?"device.components_load_error":"device.no_components_found")}
                    </p>`}
          </div>
          ${(0,eO.F)({loadingMore:this._list.loadingMore,error:this._list.hasError&&this._list.items.length>0,hasMore:this._list.hasMore,localize:this._localize,loadingLabelKey:"device.loading_components",errorLabelKey:"device.components_load_more_error",onRetry:()=>this._list.loadMore()})}
        </div>
      </div>
    `}_onToggleExpand(e){this._expandedId=this._expandedId===e?null:e}_measureDescriptionOverflow(){if(!(0,eC.z)(this))return;let e=function(e){let t=new Set;for(let i of e){let e=i.dataset.componentId;e&&i.scrollHeight>i.clientHeight&&t.add(e)}return t}(this._clampedDescriptions);this._expandedId&&e.add(this._expandedId),this._overflowingDescriptions=e}_onImageError(e){if(this._imageFailed.has(e))return;let t=new Set(this._imageFailed);t.add(e),this._imageFailed=t}_onAdd(e){(0,w.r)(this,"add-component",{component:e})}_onAddBundle(e){(0,w.r)(this,"add-bundle",{bundle:e,boardId:this.boardId})}constructor(...e){super(...e),this._localize=e=>e,this.platform="",this.boardId="",this.board=null,this.yaml="",this.resolvedComponents=[],this.lockedCategories=[],this.excludeCategories=[],this._list=new eq.S(this),this._categories=[],this._search="",this._category="all",this._provides="",this._expandedId=null,this._imageFailed=new Set,this._overflowingDescriptions=new Set,this._resize=new eS(this,()=>this._measureDescriptionOverflow()),this._intersection=new ez.Q(this,()=>this._list.loadMore()),this._debouncedSearch=(0,ek.s)(()=>this._fetchComponents(),300),this._onSearchInput=e=>{this._search=e.target.value,this._provides="",this._recommendationInclusive()&&this._prefersFeatured()&&(this._category=this._search.trim()?"all":D._.FEATURED),this._debouncedSearch()}}}function eW(e,t,i,r){var o,a=arguments.length,n=a<3?t:null===r?r=Object.getOwnPropertyDescriptor(t,i):r;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)n=Reflect.decorate(e,t,i,r);else for(var s=e.length-1;s>=0;s--)(o=e[s])&&(n=(a<3?o(n):a>3?o(t,i,n):o(t,i))||n);return a>3&&n&&Object.defineProperty(t,i,n),n}eG.styles=[c.G9,ec.z9,e$.U,eZ,ex.f],eH([(0,r.Fg)({context:s.$F,subscribe:!0}),(0,n.wk)()],eG.prototype,"_localize",void 0),eH([(0,r.Fg)({context:s.Ie})],eG.prototype,"_api",void 0),eH([(0,n.MZ)()],eG.prototype,"platform",void 0),eH([(0,n.MZ)({attribute:"board-id"})],eG.prototype,"boardId",void 0),eH([(0,n.MZ)({attribute:!1})],eG.prototype,"board",void 0),eH([(0,n.MZ)()],eG.prototype,"yaml",void 0),eH([(0,n.MZ)({attribute:!1})],eG.prototype,"resolvedComponents",void 0),eH([(0,n.MZ)({attribute:!1})],eG.prototype,"lockedCategories",void 0),eH([(0,n.MZ)({attribute:!1})],eG.prototype,"excludeCategories",void 0),eH([(0,n.wk)()],eG.prototype,"_categories",void 0),eH([(0,n.wk)()],eG.prototype,"_search",void 0),eH([(0,n.wk)()],eG.prototype,"_category",void 0),eH([(0,n.wk)()],eG.prototype,"_provides",void 0),eH([(0,n.wk)()],eG.prototype,"_expandedId",void 0),eH([(0,n.wk)()],eG.prototype,"_imageFailed",void 0),eH([(0,n.wk)({hasChanged:(e,t)=>!t||!(0,eA.c)(e,t)})],eG.prototype,"_overflowingDescriptions",void 0),eH([(0,n.YG)(".component-description--clamp[data-component-id]")],eG.prototype,"_clampedDescriptions",void 0),eG=eH([(0,n.EM)("esphome-component-catalog")],eG),(0,z.C)({close:o.mdiClose,"arrow-left":o.mdiArrowLeft,"package-variant-closed":o.mdiPackageVariantClosed});class eY extends a.WF{open(){this._resetDetourState(),this._selected=null,this._submitError="",this._submitting=!1,this._dialog.open=!0,(0,C.ak)(this._api),this.updateComplete.then(()=>this._catalog?.load())}openWithSearch(e){this._resetDetourState(),this._selected=null,this._submitError="",this._submitting=!1,this._dialog.open=!0;let t=this._depNavSeq;Promise.all([(0,C.ak)(this._api),this.updateComplete]).then(()=>{t===this._depNavSeq&&this._dialog.open&&this._catalog?.filterByDomain(e)})}_clearDetourFields(){this._detourStack=[],this._prefillReference=null,this._depPrefill=null,this._returnValues=null}_cancelPendingWork(){this._bundleQueue=[],this._bundleProgress=null,this._depNavSeq++,this._selectionSeq++}_resetDetourState(){this._clearDetourFields(),this._cancelPendingWork()}render(){var e;let t=null!==this._selected,i=this._detourStack[this._detourStack.length-1]?.component??null,r=this.lockedCategories.length>0,o=r?this.boardName?"device.add_config_dialog_title":"device.add_config":this.boardName?"device.add_component_dialog_title":"device.add_component",n=t?function(e,t,i){if(i.core)return e;let r=en(t);return r?`${e} \xb7 ${r}`:e}(this._selected.name,this._selected.category,{core:r}):this.boardName?this._localize(o,{name:this.boardName}):this._localize(o);return(0,a.qy)`
      <esphome-base-dialog
        class=${t?"form-view":""}
        ?open=${this._dialog.open}
        ?busy=${this._submitting}
        .label=${n}
        .confirmOnEnter=${t?this._onEnterSubmit:void 0}
        @request-close=${this._dialog.onRequestClose}
        @add-component=${this._onComponentSelected}
        @add-bundle=${this._onBundleSelected}
        @form-cancel=${this._onBack}
        @form-submit=${this._onFormSubmit}
        @navigate-to-dep=${this._onNavigateToDep}
        @request-add-component=${this._onNavigateToDep}
      >
        ${t?(0,a.qy)`<button
                slot="header-prefix"
                class="back-button"
                title=${this._localize("layout.back")}
                aria-label=${this._localize("layout.back")}
                @click=${this._onBack}
              >
                <wa-icon library="mdi" name="arrow-left"></wa-icon>
              </button>`:a.s6}
        ${i?(0,a.qy)`<div class="return-banner">
                ${this._localize("device.return_to_after_dep_prefix")}
                <strong>${i.name}</strong>
                ${this._localize("device.return_to_after_dep_suffix")}
              </div>`:a.s6}
        ${t&&this._bundleProgress?(0,a.qy)`<div class="bundle-banner">
                <wa-icon library="mdi" name="package-variant-closed"></wa-icon>
                <span
                  >${this._localize("device.bundle_step_progress",{current:this._bundleProgress.current,total:this._bundleProgress.total,name:this._bundleProgress.bundleName})}</span
                >
              </div>`:a.s6}
        ${!t&&this._submitError?(0,a.qy)`<div class="catalog-error" role="alert">${this._submitError}</div>`:a.s6}
        <esphome-component-catalog
          ?hidden=${t}
          .platform=${this.platform}
          .boardId=${this.board?.id??""}
          .board=${this.board}
          .yaml=${this.yaml}
          .resolvedComponents=${this._resolvedComponents}
          .lockedCategories=${this.lockedCategories}
          .excludeCategories=${(e={isCoreLocked:r,isInDepDetour:null!==i}).isCoreLocked||e.isInDepDetour?[]:D.b}
        ></esphome-component-catalog>
        ${t?(0,a.qy)`<esphome-add-component-form
                .component=${this._selected}
                .board=${this.board}
                .yaml=${this.yaml}
                .resolvedComponents=${this._resolvedComponents}
                .resolvedPlatforms=${this._resolvedPlatforms}
                .prefillReference=${this._prefillReference}
                .prefillFields=${this._depPrefill?.fields??null}
                .restoredValues=${this._returnValues}
                .extraRequired=${this._depPrefill?.required??null}
                .optionOverrides=${this._depPrefill?.optionOverrides??null}
                .submitting=${this._submitting}
                .submitError=${this._submitError}
              ></esphome-add-component-form>`:a.s6}
      </esphome-base-dialog>
    `}async _onComponentSelected(e){e.stopPropagation();let t=await V(this,e.detail.component.id);if("stale"===t.kind)return;if("error"===t.kind){this._submitError=t.message;return}let i=this._missingRequiredPrereqs(t.entry);if(i&&i.unresolved.length>0){this._submitError=this._localize("device.prereq_unresolved",{name:t.entry.name,ids:i.unresolved.join(", ")});return}if(i&&i.missing.length>0)return void await this._startFeaturedSequence([...i.missing,t.entry.id],i.boardId,this._localize("device.adding_prerequisites_for",{name:t.entry.name}));this._selected=t.entry,this._submitError="";let r=this._fastPathFields(t.entry);r&&await this._submitComponent(r,!0)}_missingRequiredPrereqs(e){let t=this.board;if(!t)return null;let i=t.featured_components??[],r=(0,b.Hz)(e.id,t);if(!r?.requires?.length)return null;let o=(0,_.gO)(this.yaml),a=[],n=[];for(let s of r.requires){let r=i.find(e=>e.id===s);if(!r){console.warn(`Featured component '${e.id}' requires '${s}', which is not in the board catalog.`),n.push(s);continue}let l=r.fields.id?.value;"string"==typeof l&&o.has(l)||a.push((0,b.m0)(t.id,s))}return{boardId:t.id,missing:a,unresolved:n}}async _startFeaturedSequence(e,t,i){let[r,...o]=e,a=await V(this,r,t);return"stale"!==a.kind&&("error"===a.kind?(this._submitError=a.message,!1):(this._clearDetourFields(),this._bundleQueue=o,this._bundleProgress={current:1,total:e.length,bundleName:i},this._selected=a.entry,this._submitError="",!0))}_fastPathFields(e){var t,i,r;let o;if(null!==this._prefillReference||null!==this._depPrefill||v(e))return null;let a=(0,$.H)((0,q.Zn)(this.yaml),this.yaml,this._resolvedComponents),n=eo({entries:e.config_entries,component:e,board:this.board,yaml:this.yaml,prefillReference:null,prefillFields:null,restoredValues:null,localize:this._localize,catalogById:(0,C.Cm)()?.byId}),s=P(e,n);return L(s,this.yaml,a,this._resolvedPlatforms).length>0||function(e,t,i,r,o=(0,C.Cm)()){return o?N(e,t,i,r,o).length>0:function e(t){return t.some(t=>!!(t.references_component&&t.references_class&&!t.locked)||e(t.config_entries??[]))}(e)}(e.config_entries,s,n,this.yaml)?null:(t=e.config_entries,i=e.required_groups??[],r=this.board,o=(0,Y.c4)(t,n,i,J(n,r,a)),(0,Y.qI)(o)||o.unmet.length>0)?null:W(e.config_entries,n)}async _onBundleSelected(e){if(e.stopPropagation(),this._submitting)return;let{bundle:t,boardId:i}=e.detail;if(!i||0===t.component_ids.length||!this.configuration)return;let r=this.configuration,o=this.yaml,a=this.board,n=t.component_ids.map(e=>(0,b.m0)(i,e));this._clearDetourFields(),this._submitting=!0,this._submitError="",this._depNavSeq++;let s=this.yaml||void 0,l=null,d=null,c=!1,p=()=>{c&&this._dispatchDraft({configuration:r,yaml:this.yaml,basedOn:o})},u=async e=>{p();let r=await this._startFeaturedSequence(n.slice(e),i,t.name);this._submitting=!1,r&&(l&&(this._prefillReference=l),this._bundleProgress={current:e+1,total:n.length,bundleName:t.name})},h=(0,_.gO)(this.yaml);try{for(let e=0;e<n.length;e++){let t=await V(this,n[e],i);if("stale"===t.kind)return void p();if("error"===t.kind){p(),this._submitError=t.message;return}let o=t.entry,a=this._fastPathFields(o);if(null===a)return void await u(e);let m="string"==typeof a.id?a.id:void 0;if(m&&h.has(m)){l=this._chainReference(o,a);continue}let{yaml:f}=await this._api.addComponent(r,{component_id:n[e],fields:a},s);s=f,c=!0,d={yaml:f,componentId:n[e],instanceId:m},m&&h.add(m),this.yaml=f,l=this._chainReference(o,a)}p(),this._selectAndClose(d,a);let e=c?this._localize("device.bundle_added",{name:t.name}):this._localize("device.bundle_already_present",{name:t.name});(0,k.VX)(e)}catch(e){p(),this._submitError=(0,x.K)(e,this._localize,"device.add_component_error"),(0,k.UG)(this._submitError)}finally{this._submitting=!1}}_selectAndClose(e,t){if(e){let i=(0,b.Ze)(e.componentId,t);(0,b.sO)(i)&&console.warn(`Board carries no featured entry for '${i}'; skipping the post-add jump.`);let r=(0,f.BB)(e.yaml,i,e.instanceId);if(r){let{sectionKey:e,fromLine:t,toLine:i}=r;(0,w.r)(this,"section-select",{sectionKey:e,fromLine:t}),(0,w.r)(this,"yaml-highlight",{range:{fromLine:t,toLine:i},scroll:!0})}}this._dialog.open=!1,this._selected=null,this._resetDetourState()}_dispatchDraft(e){(0,es.IL)(this,"yaml-draft",{...e,node:this})}_chainReference(e,t){let i=t.id;return"string"==typeof i&&e.category?{domain:e.category,id:i}:null}_onBack(){if(!this._submitting){if(K(this)){this._prefillReference=null,this._cancelPendingWork(),this._submitError="";return}this._resetDetourState(),this._selected=null,this._submitError=""}}_onNavigateToDep(e){e.stopPropagation();let t=this._form?.currentValues??null;return this._returnValues=null,async function(e,t,i=null){if(e._submitting)return;let r=e._selected;e._submitError="";let o=++e._depNavSeq,a=null;try{a=await (0,B.Sn)(e._api,t,e.platform||void 0,e.board?.id??void 0)}catch{a=null}if(o===e._depNavSeq){if(r&&(e._detourStack=[...e._detourStack,{component:r,depDomain:t,values:i,prefill:e._depPrefill}]),e._depPrefill=null,a){var n,s,l;let i,o=r?.bus_constraints?.[t],d=o?function(e,t){let i={},r=[],o={},a=t=>e.find(e=>e.key===t),n=null,s=null;for(let[e,l]of Object.entries(t)){if("min_frequency"===e){"number"==typeof l&&(n=l);continue}if("max_frequency"===e){"number"==typeof l&&(s=l);continue}if(e.startsWith("require_")){!0===l&&r.push(`${e.slice(8)}_pin`);continue}let t=a(e);if(!t)continue;if(Array.isArray(l)){let r=t.multi_value?[]:l.filter(e=>"string"==typeof e||"number"==typeof e);if(0===r.length)continue;o[e]=r;let a=r[0],n=t.default_value;(null==n||String(n)!==String(a))&&(i[e]=t.type===j.Hh.STRING?String(a):a);continue}let d=t.default_value;(null==d||String(d)!==String(l))&&(i[e]=t.type===j.Hh.STRING?String(l):l)}if(null!==n||null!==s){let e=a("frequency"),t=e?.unit_options?.length?e.unit_options:["Hz"],r=(0,T.D6)(e?.default_value,t),o=null;null===r?o=s??n:null!==s&&r>s?o=s:null!==n&&r<n&&(o=n),null!==o&&(i.frequency=(0,T.j1)(o,t))}if(0===Object.keys(i).length&&0===r.length&&0===Object.keys(o).length)return null;let l={fields:i,required:r};return Object.keys(o).length>0&&(l.optionOverrides=o),l}(a.config_entries,o):null,c=e.board?.featured_components?.find(e=>e.component_id===a.id);n=d,s=function(e){if(!e)return null;let t={};for(let[i,r]of Object.entries(e.fields))null!==r.value&&void 0!==r.value&&(t[i]=r.value);return Object.keys(t).length>0?{fields:t,required:[]}:null}(c),e._depPrefill=n?s?{fields:{...s.fields,...n.fields},required:[...n.required,...s.required],...n.optionOverrides?{optionOverrides:n.optionOverrides}:{}}:n:s,e._selected=c?(l=a,0===(i=new Set(Object.entries(c.fields).filter(([,e])=>e.locked).map(([e])=>e))).size?l:{...l,config_entries:l.config_entries.map(e=>i.has(e.key)?{...e,locked:!0}:e)}):a;return}e._selected=null,await e.updateComplete,o===e._depNavSeq&&e._catalog?.filterByDomain(t)}}(this,e.detail.domain,t)}_onFormSubmit(e){return e.stopPropagation(),this._submitComponent(e.detail.fields)}async _submitComponent(e,t=!1){if(!this._selected||!this.configuration||this._submitting)return;let i=this.configuration,r=this.yaml,o=this.board;this._submitting=!0,this._submitError="",this._depNavSeq++;try{let{yaml:n}=await this._api.addComponent(i,{component_id:this._selected.id,fields:e},r||void 0);this._dispatchDraft({configuration:i,yaml:n,basedOn:r});let s=this._selected,l=K(this);if(l){var a;let t=e.id;this._prefillReference="string"==typeof t&&(a=l.depDomain,s.id===a||s.category===a)?{domain:l.depDomain,id:t}:null}else if(this._bundleQueue.length>0&&this._bundleProgress){let t=this._bundleQueue[0],i=this._bundleQueue.slice(1),r=await V(this,t);if("stale"===r.kind)return;if("error"===r.kind){this._submitError=r.message;return}let o=r.entry;this._prefillReference=this._chainReference(this._selected,e),this._bundleQueue=i,this._bundleProgress={...this._bundleProgress,current:this._bundleProgress.current+1},this._returnValues=null,this._selected=o}else{let i=this._selected.name,r=e.id;this._selectAndClose({yaml:n,componentId:this._selected.id,instanceId:"string"==typeof r?r:void 0},o),t&&(0,k.VX)(this._localize("device.component_added",{name:i}))}}catch(e){this._submitError=(0,x.K)(e,this._localize,"device.add_component_error"),t&&(0,k.UG)(this._submitError)}finally{this._submitting=!1}}constructor(...e){super(...e),this._localize=e=>e,this.boardName="",this.configuration="",this.platform="",this.board=null,this.yaml="",this._resolvedComponents=[],this._resolvedPlatforms=[],this.lockedCategories=[],this._dialog=new y.T(this),this._returnValues=null,this._selected=null,this._submitting=!1,this._submitError="",this._detourStack=[],this._prefillReference=null,this._depPrefill=null,this._bundleQueue=[],this._bundleProgress=null,this._selectionSeq=0,this._depNavSeq=0,this._onEnterSubmit=e=>{e.repeat||this._submitting||this._form?.requestSubmit()}}}eY.styles=[c.G9,(0,d._)("esphome-base-dialog"),l.c4,U],eW([(0,r.Fg)({context:s.$F,subscribe:!0}),(0,n.wk)()],eY.prototype,"_localize",void 0),eW([(0,r.Fg)({context:s.Ie})],eY.prototype,"_api",void 0),eW([(0,n.MZ)()],eY.prototype,"boardName",void 0),eW([(0,n.MZ)()],eY.prototype,"configuration",void 0),eW([(0,n.MZ)()],eY.prototype,"platform",void 0),eW([(0,n.MZ)({attribute:!1})],eY.prototype,"board",void 0),eW([(0,n.MZ)()],eY.prototype,"yaml",void 0),eW([(0,r.Fg)({context:s.I9,subscribe:!0}),(0,n.wk)()],eY.prototype,"_resolvedComponents",void 0),eW([(0,r.Fg)({context:s.YY,subscribe:!0}),(0,n.wk)()],eY.prototype,"_resolvedPlatforms",void 0),eW([(0,n.MZ)({attribute:!1})],eY.prototype,"lockedCategories",void 0),eW([(0,n.P)("esphome-component-catalog")],eY.prototype,"_catalog",void 0),eW([(0,n.P)("esphome-add-component-form")],eY.prototype,"_form",void 0),eW([(0,n.wk)()],eY.prototype,"_returnValues",void 0),eW([(0,n.wk)()],eY.prototype,"_selected",void 0),eW([(0,n.wk)()],eY.prototype,"_submitting",void 0),eW([(0,n.wk)()],eY.prototype,"_submitError",void 0),eW([(0,n.wk)()],eY.prototype,"_detourStack",void 0),eW([(0,n.wk)()],eY.prototype,"_prefillReference",void 0),eW([(0,n.wk)()],eY.prototype,"_depPrefill",void 0),eW([(0,n.wk)()],eY.prototype,"_bundleQueue",void 0),eW([(0,n.wk)()],eY.prototype,"_bundleProgress",void 0),eW([(0,n.EM)("esphome-add-component-dialog")],eY)},318(e,t,i){var r=i(9995),o=i(874),a=i(2353),n=i(2761),s=i(2497);function l(e){return e.name?e.name:e.title?(0,s.Zt)((0,n.Cm)()).has(d(e.component_id))?(0,r.m)(e.title):e.title:e.id}function d(e){return(0,o.iZ)(e).domain}function c(e,t){if(!e.is_entity_container)return!0;let i=(0,a.PM)(e);return t.some(e=>(0,a.Qf)(e,i))}i.d(t,{},{Fi:function(e,t){return t?e.filter(e=>e.id===t.id||e.parent_id===t.id):e},I7:d,Oj:function(e,t){return e.find(e=>c(e,t))},TS:function(e,t){if(!t.has_explicit_id)return;let i=d(t.component_id),r=e.config_entries.find(e=>e.references_component===i);if(r)return{[r.key]:t.id}},_B:function(e){return!e.is_entity_container},e1:c,mR:function(e,t){if(!t)return[];let i=(0,a.PM)(t);return e.filter(e=>(0,a.Qf)(e,i))},vJ:function(e){let t=new Map(e.map(e=>[e.id,e]));return e=>{let i=e.parent_id?t.get(e.parent_id):void 0;return i?`${e.component_id} \xb7 ${l(i)}`:e.component_id}},zl:l})},8041(e,t,i){var r=i(8175);function o(){return{conditions:[],actions:[]}}function a(e){return(0,r.wr)(e)?Number(e):null}i.d(t,{},{Gi:function(e,t,i){return{action_id:e,params:{...i},children:{},conditions:[],...t?.has_branches?{branches:[o()]}:{}}},Ks:function(e){switch(e.kind){case"device_on":return void 0===e.index?`automation:device_on:${e.trigger}`:`automation:device_on:${e.trigger}:${e.index}`;case"component_on":return void 0===e.index?`automation:component_on:${e.component_id}:${e.trigger}`:`automation:component_on:${e.component_id}:${e.trigger}:${e.index}`;case"component_action":return`automation:component_action:${e.component_id}:${e.field}`;case"script":return`automation:script:${e.id}`;case"interval":return`automation:interval:${e.index}`;case"light_effect":return`automation:light_effect:${e.component_id}:${e.index}`;case"api_action":return`automation:api_action:${e.action_name}`}},LA:function(e){return{condition_id:e,params:{},children:[]}},Ly:o,Wq:function(e,t){if(t<0||t>=e.length)return e;let i=e.slice();return i.splice(t,1),i},_D:function(e,t,i){if(t<0||t>=e.length)return e;let r=e.slice();return r[t]=i,r},aG:function e(t,i,r){if(0===i.length)return r&&"object"==typeof r&&!Array.isArray(r)?{...r}:{};let[o,...a]=i;if(0===a.length){if(void 0===r||""===r){let e={...t};return delete e[o],e}return{...t,[o]:r}}let n=t[o]&&"object"==typeof t[o]&&!Array.isArray(t[o])?t[o]:{};return{...t,[o]:e(n,a,r)}},ac:function(e){if(!e.startsWith("automation:"))return null;let t=e.split(":");switch(t[1]){case"device_on":if(!t[2])return null;if(3===t.length)return{kind:"device_on",trigger:t[2]};if(4===t.length){let e=a(t[3]);return null===e?null:{kind:"device_on",trigger:t[2],index:e}}return null;case"component_on":if(!t[2]||!t[3])return null;if(4===t.length)return{kind:"component_on",component_id:t[2],trigger:t[3]};if(5===t.length){let e=a(t[4]);return null===e?null:{kind:"component_on",component_id:t[2],trigger:t[3],index:e}}return null;case"component_action":return 4===t.length&&t[2]&&t[3]?{kind:"component_action",component_id:t[2],field:t[3]}:null;case"script":return t[2]?{kind:"script",id:t[2]}:null;case"interval":{let e=Number(t[2]);return Number.isFinite(e)?{kind:"interval",index:e}:null}case"light_effect":{let e=Number(t[3]);return t[2]&&Number.isFinite(e)?{kind:"light_effect",component_id:t[2],index:e}:null}case"api_action":return t[2]?{kind:"api_action",action_name:t[2]}:null;default:return null}},lX:function(e,t){let i=e.split("\n"),r=t.fromLine-1,o=Math.max(0,t.toLine-t.fromLine+1),a=t.replacement.endsWith("\n")?t.replacement.slice(0,-1):t.replacement,n=""===a?[]:a.split("\n");return[...i.slice(0,r),...n,...i.slice(r+o)].join("\n")},rN:function(){return{trigger_id:null,trigger_params:{},actions:[]}},wg:function(e,t,i){if(t<0||i<0||t>=e.length||i>=e.length||t===i)return e;let r=e.slice();return[r[t],r[i]]=[r[i],r[t]],r}})},7869(e,t,i){var r=i(2761);i.d(t,{},{C:class{byId(){return this.index()?.byId??null}index(){let e=(0,r.Cm)(),t=this._api();if(!e&&t&&Date.now()>=this._retryAt){this._retryAt=1/0;let e=()=>{this._retryAt=Date.now()+3e4};(0,r.ak)(t).then(()=>{if(!(0,r.Cm)())return e();this._retryAt=0,this._host.requestUpdate()},e)}return e}constructor(e,t){this._host=e,this._api=t,this._retryAt=0}}})},2561(e,t,i){var r=i(4008),o=i(565),a=i(8851);function n(e,t=[]){let i=new Set;for(let t of e??[])("exactly_one"===t.kind||"at_least_one"===t.kind)&&t.keys.forEach(e=>i.add(e));let r=new Set(t.filter(e=>e.group&&i.has(e.key)).map(e=>e.group));for(let e of t)r.has(e.group)&&i.add(e.key);return i}function s(e,t){return(e.config_entries??[]).find(e=>e.type===r.Hh.ID&&!e.references_component&&(e.required||!t&&"id"===e.key))}function l(e,t){let i=e.config_entries??[];if(null!=e.platform_type&&(e.config_entries??[]).some(e=>"name"===e.key&&e.type===r.Hh.STRING))return{from:"name",key:"name"};let n=s(e,!1);if(n)return{from:"id",key:n.key};if(!d(e,t))return null;let l=i.find(e=>!e.hidden&&!e.locked&&!e.multi_value&&!e.references_component&&e.type!==r.Hh.NESTED&&e.type!==r.Hh.MAP&&(0,a.$z)(e.default_value)&&(0,o.VP)(e,{},t.presentComponents,t.targetPlatform,t.rootValues,i));return l?{from:"default",key:l.key,value:l.default_value}:null}function d(e,t){return!e.required&&void 0!==t.requiredGroups&&n(t.requiredGroups).has(e.key)}i.d(t,{},{Rj:s,Vn:n,p_:function(e,t){return d(e,t)&&null!=l(e,t)},x9:l})},3508(e,t,i){var r=i(6185),o=i(1734),a=i(1379),n=i(324),s=i(8329),l=i(2911);function d(e){return e.length>0&&e.every(e=>!!e.advanced)}function c(e,t){return e.some(e=>(0,o.P)(e,t))}i.d(t,{},{TP:c,_r:function(e,t,i){let r=function(e,t){let i=new Map,{clusters:r}=(0,s.Jz)(e,t);for(let e of r)for(let t of e.members)i.set(t.key,e.members);let o=new Map;for(let t of e){if(!t.exclusive_group)continue;let e=o.get(t.exclusive_group)??[];e.push(t),o.set(t.exclusive_group,e),i.set(t.key,e)}return e=>i.get(e)}(e,t);return e=>{let t=r(e);if(t)return d(t)&&!c(t,i)}},c4:function(e,t,i,o){let d={...o,requiredGroups:i},c=(0,l.$J)(e),{clusters:p,memberKeys:u}=(0,s.Jz)(e,i),h=p.map(i=>(0,s.Ci)(i,t,d,e)),m=new Map(h.map(e=>[e.cluster.members[0].key,e])),f=c.filter(e=>Array.isArray(e)).map(i=>(0,l.Bw)(i,t,d,e)),g=new Map(f.map(e=>[e.members,e])),v=e.filter(e=>!e.exclusive_group&&!u.has(e.key)),_=new Set((0,a.V5)(v,t,d)),y=new Map,b=e=>{for(let t of e)t.locked||y.set(t.key,t)};for(let{painted:e,mode:t}of(b([..._]),h))"radio"===t&&(0,r.es)(e)||b(e);for(let{options:e}of f)(0,r.es)(e)||b(e);let w=e=>e.some(e=>y.has(e)),x=(0,n.c)({entries:e,requiredGroups:i,values:t,opts:d},u).map(({kind:e,keys:t})=>({kind:e,keys:t,source:"banner",actionable:w(t)}));for(let{unmet:e}of h)e&&x.push({...e,source:"cluster",actionable:w(e.keys)});return{ordered:c,clusters:h,memberKeys:u,clusterByFirstKey:m,groupPaints:g,visible:_,settable:y,unmet:x}},gl:d,qI:function(e){return e.settable.size>0}})},4355(e,t,i){var r=i(9104),o=i(289),a=i(5077),n=i(9356),s=i(1502),l=i(4008),d=i(1556),c=i(6185),p=i(7181),u=i(5217),h=i(8283),m=i(5795),f=i(8175);let g=new WeakMap,v=new WeakMap,_=new WeakSet;var y=i(3330),b=i(1734),w=i(9582);let x=(0,i(7064).Y)({name:"pin-registry-modes",fetch:e=>e.getPinRegistryModes(),fallback:e=>(console.warn("pin-registry-modes fetch failed; Mode flags unscoped",e),Object.create(null))});function $(){return x.getCached()}function k(e){return x.subscribe(e)}function z(e){return x.fetch(e)}var C=i(6670),q=i(1093);function S(e){if(e.assignedSlot)return e.assignedSlot;if(e.parentElement)return e.parentElement;let t=e.getRootNode();return t instanceof ShadowRoot?t.host:null}class A{hostConnected(){this._unsubscribe=this._binding.subscribe(()=>this._host.requestUpdate())}hostDisconnected(){this._unsubscribe?.(),this._unsubscribe=void 0}hostUpdated(){if(this._kicked)return;let e=this._api();e&&(this._kicked=!0,this._binding.fetch(e))}get value(){return this._binding.getCached()}constructor(e,t,i){this._host=e,this._binding=t,this._api=i,this._kicked=!1,e.addController(this)}}var O=i(5413),M=i(7869),E=i(1379),I=i(2564),P=i(6910),R=i(3815),L=i(8851),F=i(2561),N=i(8329);function D(e,t,i){return 0===e.length?a.s6:e.map(({kind:e,keys:r})=>(0,a.qy)`
      <div class="warning-banner constraint-banner">
        <wa-icon library="mdi" name="alert-circle-outline"></wa-icon>
        <span>
          ${i.localize(`device.constraint_${e}`,{keys:(0,N.X7)(r,t,i)})}
        </span>
      </div>
    `)}var j=i(324);let T=e=>t=>t===e?null:t>e?t-1:t;function B(e,t){let i=[...e.entries()];for(let[r,o]of(e.clear(),i)){let i=t(r);null!==i&&(e instanceof Set?e.add(i):e.set(i,o))}}var K=i(6092);function V(e,t){let i=(0,K.Y0)(t.yaml);return(0,K.Fc)(t.getAt([]),i),(0,K.T6)(e.key,i)}let U=new WeakMap;function Z(e,t,i){let r=i.getAt(t);if(!e.multi_value&&(0,L.$z)(r)&&("string"==typeof r||"number"==typeof r||"boolean"==typeof r))return(0,a.qy)`
      <div class="field" data-field-key=${(0,I.DN)(t)}>
        ${(0,I.Lx)(e,i,{path:t})}
        <p class="field-description">
          ${i.localize("device.value_set_in_yaml",{value:String(r)})}
        </p>
        ${(0,I.FL)(t,i)}
      </div>
    `;let o=t.join("."),n=i.scopeValues(t),s=(0,L.$z)(r),d=(0,E.Ic)(e,r),c=i.filterRenderable(e.config_entries??[],n,d),p=c.length>0;p&&(e.required||s)&&i.seedNestedOpen(o);let u=i.nestedOpenSections.has(o),h=p&&u,m=null!=e.platform_type&&!e.required,g=(0,F.p_)(e,(0,I.I4)(i,t)),v=m||g,_=v&&s,y=(0,I.gt)(e,i),b=i.localize("device.enable_entity",{name:y}),w=(0,I.BT)(e,t,i),x=new Set(c.map(e=>e.key)),$=_?function(e,t,i,r){if(!(0,f.Qd)(t))return"";let o=new Map((e.config_entries??[]).map(e=>[e.key,e]));return Object.entries(t).filter(([e,t])=>!r.has(e)&&(0,f.k4)(t)&&(0,L.$z)(t)).map(([t,r])=>{var a,n,s,d;let c=o.get(t),p=(a=e.key,n=t,s=r,d=c,d?.type===l.Hh.SECURE_STRING||(0,R._s)(a,n)?"••••••":String(s).replace(G," "));return`${c?(0,I.gt)(c,i):t}: ${p}`}).join(", ")}(e,r,i,x):"",k=(0,a.qy)`<span class="nested-title">${y}</span>
    ${e.platform_type?(0,a.qy)`<span class="nested-platform">${e.platform_type}</span>`:a.s6}`;return(0,a.qy)`
    <div class="nested-group" data-field-key=${(0,I.DN)(t)}>
      <div class="nested-header">
        ${v?(0,a.qy)`<wa-switch
                class="nested-enable"
                .checked=${_}
                ?disabled=${(0,I.U)(e,i)}
                aria-label=${b}
                title=${b}
                @change=${r=>(function(e){let t,{entry:i,path:r,key:o,isOpen:a,checked:n,label:s,ctx:l}=e,d=((t=U.get(l.stashOwner))||(t=new Map,U.set(l.stashOwner,t)),t);if(n){var c,p,u,h;let e,t,n=d.get(o);n&&(0,L.$z)(n)?(d.delete(o),l.emitChange(r,n)):(c=i,p=r,u=s,h=l,e=(0,F.x9)(c,(0,I.I4)(h,p)),t=e?.from==="name"?u:e?.from==="id"?V(c,h):e?.value,e&&void 0!==t?h.emitChange([...p,e.key],t):h.emitChange(p,void 0)),a||l.toggleNested(o)}else{let e=l.getAt(r);(0,f.Qd)(e)&&(0,L.$z)(e)&&d.set(o,e),l.emitChange(r,void 0),a&&l.toggleNested(o)}})({entry:e,path:t,key:o,isOpen:u,checked:r.target.checked,label:y,ctx:i})}
              ></wa-switch>`:a.s6}
        ${p?(0,a.qy)`<button
                type="button"
                class="nested-toggle"
                aria-expanded=${h}
                @click=${()=>i.toggleNested(o)}
              >
                <wa-icon
                  library="mdi"
                  name=${h?"chevron-up":"chevron-down"}
                ></wa-icon>
                ${k}
              </button>`:(0,a.qy)`<span class="nested-toggle nested-toggle--static">${k}</span>`}
        ${(0,I.wm)(e,i)}
      </div>
      ${w?(0,a.qy)`<p class="nested-desc">${(0,P.Gc)(w)}</p>`:a.s6}
      ${$?(0,a.qy)`<p class="nested-desc">
              ${i.localize("device.enabled_block_sets",{values:$})}
            </p>`:a.s6}
      ${h?(0,a.qy)`<div class="nested-fields">
              ${s?D((0,j.c)({entries:e.config_entries??[],requiredGroups:d,values:n,opts:(0,I.I4)(i,t)},H),e.config_entries??[],i):a.s6}
              ${c.map(e=>i.renderEntry(e,[...t,e.key]))}
            </div>`:a.s6}
    </div>
  `}let H=new Set,G=/\s+/g;var W=i(8067),Y=i(6906),Q=i(9177),J=i(3013),X=i(596),ee=i(9732),et=i(6320),ei=i(2125),er=i(5343),eo=i(4256),ea=i(6250);function en(e,t,i,r){var o,a=arguments.length,n=a<3?t:null===r?r=Object.getOwnPropertyDescriptor(t,i):r;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)n=Reflect.decorate(e,t,i,r);else for(var s=e.length-1;s>=0;s--)(o=e[s])&&(n=(a<3?o(n):a>3?o(t,i,n):o(t,i))||n);return a>3&&n&&Object.defineProperty(t,i,n),n}let es=X.YH.define();class el extends ea.U{render(){return(0,a.qy)`<div class="cm-wrap ${this.invalid?"invalid":""}"></div>`}updated(e){if(this._view&&(e.has("_darkMode")&&this._view.dispatch({effects:this._themeCompartment.reconfigure((0,ei.P5)(this._darkMode))}),e.has("disabled")&&this._view.dispatch({effects:this._editableCompartment.reconfigure(ee.Lz.editable.of(!this.disabled))}),e.has("value"))){let e=this._view.state.doc.toString();e!==this.value&&this._view.dispatch({changes:{from:0,to:e.length,insert:this.value},annotations:es.of(!0)})}}_mountEditor(){this._mountView(this.value,[et.oQ,(0,eo.O)(this._localize),(0,Q.I)(),J.Xt.of("  "),ee.w4.of([Y.Yc]),this._editableCompartment.of(ee.Lz.editable.of(!this.disabled)),this._themeCompartment.of((0,ei.P5)(this._darkMode)),ei.gn,ee.Lz.updateListener.of(e=>{if(e.docChanged&&!e.transactions.some(e=>void 0!==e.annotation(es))){let t=e.state.doc.toString();(0,y.r)(this,"lambda-change",{value:t})}})])}constructor(...e){super(...e),this._darkMode=(0,er.yk)(),this._localize=e=>e,this.value="",this.disabled=!1,this.invalid=!1,this.placeholder="",this._themeCompartment=new X.xx,this._editableCompartment=new X.xx}}function ed(e,t,i){let r=i.getAt(t),o=(0,W.b)(r)?r._lambda:r instanceof L.ho?r.body:null==r?"":String(r),n=null!==i.errorAt(t),s=(0,I.U)(e,i),l=(0,W.b)(r)?r._tag:void 0;return(0,I.tj)(e,t,i,(0,a.qy)`<esphome-lambda-editor
      .value=${o}
      .invalid=${n}
      ?disabled=${s}
      placeholder=${String(e.default_value??"")}
      @lambda-change=${e=>i.emitChange(t,l?{_lambda:e.detail.value,_tag:l}:{_lambda:e.detail.value})}
    ></esphome-lambda-editor>`)}el.styles=(0,a.AH)`
    :host {
      display: block;
    }
    .cm-wrap {
      border: 1px solid var(--wa-color-neutral-border-quiet, #d1d5db);
      border-radius: 6px;
      overflow: hidden;
      min-height: 96px;
    }
    .cm-wrap.invalid {
      border-color: var(--wa-color-danger-fill-loud, #d92d20);
    }
    :host([disabled]) .cm-wrap {
      opacity: 0.6;
    }
    .cm-editor {
      font-family: "JetBrains Mono", "Fira Code", monospace;
      font-size: 13px;
      min-height: 96px;
      max-height: 320px;
    }
    .cm-editor .cm-scroller {
      overflow: auto;
    }
    .cm-editor.cm-focused {
      outline: 2px solid var(--wa-color-brand-fill-loud, #0b5cad);
      outline-offset: -1px;
    }
  `,en([(0,r.Fg)({context:d.B6,subscribe:!0}),(0,n.wk)()],el.prototype,"_darkMode",void 0),en([(0,r.Fg)({context:d.$F}),(0,n.wk)()],el.prototype,"_localize",void 0),en([(0,n.MZ)()],el.prototype,"value",void 0),en([(0,n.MZ)({type:Boolean,reflect:!0})],el.prototype,"disabled",void 0),en([(0,n.MZ)({type:Boolean})],el.prototype,"invalid",void 0),en([(0,n.MZ)()],el.prototype,"placeholder",void 0),el=en([(0,n.EM)("esphome-lambda-editor")],el);var ec=i(901);let ep=new WeakMap;class eu{clear(){this._units.clear(),this._magnitudes.clear()}constructor(e){this._host=e,this._units=new Map,this._magnitudes=new Map,this.stores=[this._units,this._magnitudes],this.ctx={getPendingUnit:e=>this._units.get(e.join(".")),setPendingUnit:(e,t)=>{this._units.set(e.join("."),t),this._host.requestUpdate()},getEditingMagnitude:e=>this._magnitudes.get(e.join(".")),setEditingMagnitude:(e,t)=>{this._magnitudes.set(e.join("."),t)},clearEditingMagnitude:e=>{this._magnitudes.delete(e.join("."))}}}}class eh{hostUpdated(){this._syncRadioGroups()}reset(){this._choices.clear(),this._stash.clear()}rekeyChoices(e){B(this._choices,e)}getChoice(e){return this._choices.get(e)}setChoice(e,t){this._choices.set(e,t),this._host.requestUpdate()}getStash(e,t){return this._stash.get(`${e} ${t}`)}setStash(e,t,i){this._stash.set(`${e} ${t}`,i)}clearStash(e,t){this._stash.delete(`${e} ${t}`)}async _syncRadioGroups(){let e=this._host.shadowRoot;if(!e)return;let t=[...e.querySelectorAll("wa-radio-group")];if(0!==t.length)for(let e of(await Promise.all(t.map(e=>e.updateComplete?.catch(()=>{}))),t))try{Promise.resolve(e.syncRadioElements?.()).catch(t=>this._warnSyncFailed(e,t))}catch(t){this._warnSyncFailed(e,t)}}_warnSyncFailed(e,t){this._warnedGroups.has(e)||(this._warnedGroups.add(e),console.warn("Radio group sync failed:",t))}constructor(e){this._host=e,this._choices=new Map,this._stash=new Map,this._warnedGroups=new WeakSet,e.addController(this)}}let em=["focusin","pointerdown","input","change"];class ef{hostConnected(){for(let e of em)this.host.addEventListener(e,this._onInteraction)}hostDisconnected(){for(let e of em)this.host.removeEventListener(e,this._onInteraction)}constructor(e){this.host=e,this._onInteraction=e=>{var t,i,r;let o=e.composedPath().find(e=>e instanceof HTMLElement&&e.hasAttribute("data-field-key"));if(!o)return;let a=o.getAttribute("data-field-key")??"";if(!a.startsWith("["))return;let n=(0,I.lt)(a);if(!n.length)return;let{emit:s,focusedKey:l}=(t=e.type,i=(0,I.DN)(n),r=this._focusedKey,"change"===t?{emit:i===r,focusedKey:r}:{emit:"focusin"===t||i!==r,focusedKey:i});this._focusedKey=l,s&&this.host.dispatchEvent(new CustomEvent("field-focus",{detail:{path:n},bubbles:!0,composed:!0}))},e.addController(this)}}var eg=i(2814),ev=i(6567);class e_{maybeScroll(e){let t=this.host.focusFieldPath,i=t?.length?(0,I.DN)(t):void 0,r=e.has("focusFieldPath")||e.has("entries")||e.has("values")||e.has("showAdvanced"),{gate:o,scroll:a}=function(e,t,i){let{scrolledKey:r,lastFocusKey:o,tries:a}=e;t!==o&&(o=t,r=void 0,a=0);let n=!!t&&r!==t&&a<3&&i;return n&&a++,{gate:{scrolledKey:r,lastFocusKey:o,tries:a},scroll:n}}({scrolledKey:this._scrolledKey,lastFocusKey:this._lastFocusKey,tries:this._tries},i,r);this._scrolledKey=o.scrolledKey,this._lastFocusKey=o.lastFocusKey,this._tries=o.tries,a&&t?.length&&i&&this._scrollTo(t,i)}async _scrollTo(e,t){var i;let{host:r}=this;if(!r.shadowRoot)return;for(let t=1;t<e.length;t++)r.openNested(e.slice(0,t).join("."));for(let t of(i=this._gatingDecls(r.shadowRoot),i.filter(t=>t.prefix.length>0&&t.prefix.length<=e.length&&t.prefix.every((t,i)=>t===e[i])).map(e=>e.key)))r.openNested(t);await r.updateComplete;let o=r.focusFieldPath;if(o&&(0,I.DN)(o)===t)for(let i=e.length;i>=1;i--){let o=this._find(r.shadowRoot,e.slice(0,i));if(!o)continue;o.scrollIntoView({block:"center"});let a=(0,I.DN)(e.slice(0,i)),n=Date.now();(a!==this._lastFlashKey||n-this._lastFlashAt>1e4)&&(this._lastFlashKey=a,this._lastFlashAt=n,(0,ev.rK)(o)),i===e.length&&(this._scrolledKey=t);return}}_gatingDecls(e){let t=[];for(let i of e.querySelectorAll("[data-reveal-for]")){let e=i.getAttribute("data-field-key");e&&t.push({prefix:(0,I.lt)(i.getAttribute("data-reveal-for")??""),key:e})}return t}_find(e,t){for(let i of e.querySelectorAll("[data-field-key]")){let e=(0,I.lt)(i.getAttribute("data-field-key")??"");if((0,eg.r)(e,t))return i}for(let i of e.querySelectorAll("*")){if(!i.localName.includes("-"))continue;let e=i.shadowRoot,r=e?this._find(e,t):null;if(r)return r}return null}constructor(e){this.host=e,this._lastFlashAt=0,this._tries=0}}let ey=":pin-advanced";i(8606),i(9218),i(1687),i(2542),i(269),i(4063),i(4350),i(1306);var eb=i(5660),ew=i(6734),ex=i(1959);let e$=(0,a.AH)`
  :host {
    display: block;
    position: relative;
  }

  /* Trigger — shaped like the project's standard input */
  .trigger {
    width: 100%;
    box-sizing: border-box;
    min-height: var(--wa-form-control-height);
    padding: 0 14px;
    font-size: var(--wa-font-size-s);
    font-family: inherit;
    line-height: var(--wa-form-control-value-line-height);
    color: var(--wa-color-text-normal);
    background: var(--wa-color-surface-raised);
    border: var(--wa-border-width-s) solid var(--wa-color-surface-border);
    border-radius: var(--wa-border-radius-m);
    outline: none;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 10px;
    text-align: left;
    transition:
      border-color 0.15s,
      box-shadow 0.15s;
  }

  .trigger:focus,
  :host([open]) .trigger {
    border-color: var(--esphome-primary);
    box-shadow: var(--esphome-focus-ring);
  }

  .trigger.invalid {
    border-color: var(--esphome-error);
  }

  .trigger.invalid:focus {
    box-shadow: 0 0 0 3px color-mix(in srgb, var(--esphome-error), transparent 80%);
  }

  .trigger:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }

  .trigger-icon {
    width: 22px;
    height: 22px;
    flex: 0 0 22px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    border-radius: var(--wa-border-radius-s);
    background: var(--esphome-tint);
    color: var(--esphome-primary);
  }

  .trigger-icon svg {
    width: 16px;
    height: 16px;
  }

  .trigger-icon--empty {
    background: var(--wa-color-surface-lowered);
    color: var(--wa-color-text-quiet);
  }

  .trigger-label {
    flex: 1;
    min-width: 0;
    font-family: var(--wa-font-family-code, monospace);
    font-size: var(--wa-font-size-s);
  }

  .trigger-label.placeholder {
    color: var(--wa-color-text-quiet);
    font-family: inherit;
  }

  .trigger-clear {
    background: none;
    border: none;
    padding: 4px;
    cursor: pointer;
    color: var(--wa-color-text-quiet);
    display: inline-flex;
    align-items: center;
    justify-content: center;
    border-radius: var(--wa-border-radius-s);
  }

  .trigger-clear:hover {
    background: var(--wa-color-surface-lowered);
    color: var(--wa-color-text-normal);
  }

  .trigger-chevron {
    width: 14px;
    height: 14px;
    color: var(--wa-color-text-quiet);
    flex: 0 0 14px;
    transition: transform 0.15s;
  }

  :host([open]) .trigger-chevron {
    transform: rotate(180deg);
  }

  /* Panel */
  .panel {
    position: absolute;
    top: calc(100% + 4px);
    left: 0;
    right: 0;
    z-index: 1000;
    display: flex;
    flex-direction: column;
    max-height: 380px;
    background: var(--wa-color-surface-raised);
    border: var(--wa-border-width-s) solid var(--wa-color-surface-border);
    border-radius: var(--wa-border-radius-m);
    box-shadow:
      0 8px 24px rgba(0, 0, 0, 0.12),
      0 2px 6px rgba(0, 0, 0, 0.06);
    overflow: hidden;
    animation: panelIn 0.12s ease-out;
  }

  @keyframes panelIn {
    from {
      opacity: 0;
      transform: translateY(-4px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }

  .search {
    position: relative;
    padding: 10px 12px;
    border-bottom: var(--wa-border-width-s) solid var(--wa-color-surface-border);
  }

  .search-icon {
    position: absolute;
    left: 22px;
    top: 50%;
    transform: translateY(-50%);
    width: 14px;
    height: 14px;
    color: var(--wa-color-text-quiet);
    pointer-events: none;
  }

  .search-input {
    width: 100%;
    box-sizing: border-box;
    padding: 7px 10px 7px 32px !important;
    min-height: 32px !important;
    font-size: var(--wa-font-size-s);
  }

  .grid-wrap {
    flex: 1;
    overflow-y: auto;
    padding: 8px;
  }

  .grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(40px, 1fr));
    gap: 4px;
  }

  .icon-cell {
    position: relative;
    aspect-ratio: 1;
    background: none;
    border: 1px solid transparent;
    border-radius: var(--wa-border-radius-s);
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--wa-color-text-normal);
    padding: 0;
    transition:
      background 0.1s,
      border-color 0.1s,
      color 0.1s,
      transform 0.08s;
  }

  .icon-cell svg {
    width: 20px;
    height: 20px;
  }

  .icon-cell:hover {
    background: var(--esphome-tint);
    color: var(--esphome-primary);
    border-color: var(--esphome-tint-border);
    transform: scale(1.06);
  }

  .icon-cell--selected {
    background: var(--esphome-primary);
    color: var(--esphome-on-primary);
  }

  .icon-cell--selected:hover {
    background: var(--esphome-primary);
    color: var(--esphome-on-primary);
    transform: scale(1.06);
  }

  .empty,
  .loading {
    padding: 24px 16px;
    text-align: center;
    color: var(--wa-color-text-quiet);
    font-size: var(--wa-font-size-s);
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 8px;
  }

  .footer {
    padding: 6px 12px;
    border-top: var(--wa-border-width-s) solid var(--wa-color-surface-border);
    font-size: var(--wa-font-size-xs);
    color: var(--wa-color-text-quiet);
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .footer-name {
    font-family: var(--wa-font-family-code, monospace);
    color: var(--wa-color-text-normal);
    font-size: var(--wa-font-size-xs);
  }
`;function ek(e,t,i,r){var o,a=arguments.length,n=a<3?t:null===r?r=Object.getOwnPropertyDescriptor(t,i):r;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)n=Reflect.decorate(e,t,i,r);else for(var s=e.length-1;s>=0;s--)(o=e[s])&&(n=(a<3?o(n):a>3?o(t,i,n):o(t,i))||n);return a>3&&n&&Object.defineProperty(t,i,n),n}(0,q.C)({close:o.mdiClose,magnify:o.mdiMagnify,palette:o.mdiPalette});let ez=null;function eC(e){return e?e.startsWith("mdi:")?e.slice(4):e:""}class eq extends a.WF{willUpdate(e){e.has("_open")&&this._dismiss.set(this._open),e.has("value")&&!this._loaded&&eC(this.value)&&this._ensureCatalogLoaded()}async _toggle(){this.disabled||(this._open?this._close():await this._openPanel())}async _openPanel(){this._open=!0,this.setAttribute("open",""),await this._ensureCatalogLoaded(),await this.updateComplete,this._searchInput?.focus()}async _ensureCatalogLoaded(){this._loaded||(this._catalog=await (ez||(ez=(async()=>{let e=await Promise.resolve().then(i.bind(i,289)),t=[];for(let[i,r]of Object.entries(e)){if(!i.startsWith("mdi")||"string"!=typeof r)continue;let e=i.slice(3);if(!e)continue;let o=e.replace(/^[A-Z]/,e=>e.toLowerCase()).replace(/([A-Z])/g,"-$1").replace(/_/g,"-").toLowerCase();t.push({name:o,path:r})}return t.sort((e,t)=>e.name.localeCompare(t.name)),t})().catch(e=>(console.error("[mdi-icon-picker] failed to load catalog:",e),ez=null,[])))),this._loaded=!0)}_close(){this._open=!1,this.removeAttribute("open"),this._query=""}_select(e){let t=`mdi:${e}`;this.value=t,(0,y.r)(this,"change",{value:t}),this._close()}_clear(e){e.stopPropagation(),this.value="",(0,y.r)(this,"change",{value:""})}_onSearchInput(e){this._query=e.target.value}_renderTriggerIcon(){let e=eC(this.value);if(!e)return(0,a.qy)`<span class="trigger-icon trigger-icon--empty">
        <svg viewBox="0 0 24 24" aria-hidden="true">
          <path fill="currentColor" d=${o.mdiPalette}></path>
        </svg>
      </span>`;let t=this._catalog.find(t=>t.name===e);return t?(0,a.qy)`<span class="trigger-icon">
        <svg viewBox="0 0 24 24" aria-hidden="true">
          <path fill="currentColor" d=${t.path}></path>
        </svg>
      </span>`:(0,a.qy)`<span class="trigger-icon">
      <wa-icon library="mdi" name=${e} style="font-size: 16px;"></wa-icon>
    </span>`}_renderPanel(){if(!this._loaded)return(0,a.qy)`<div class="panel" @click=${e=>e.stopPropagation()}>
        <div class="loading">Loading icons…</div>
      </div>`;let e=function(e,t){if(!t)return e.slice(0,400);let i=t.trim().toLowerCase().replace(/\s+/g,"-");if(!i)return e.slice(0,400);let r=[],o=[],a=[];for(let t of e)if(t.name===i?r.push(t):t.name.startsWith(i)?o.push(t):t.name.includes(i)&&a.push(t),r.length+o.length+a.length>=800)break;return[...r,...o,...a].slice(0,400)}(this._catalog,this._query),t=eC(this.value);return(0,a.qy)`
      <div class="panel" @click=${e=>e.stopPropagation()}>
        <div class="search">
          <svg class="search-icon" viewBox="0 0 24 24" aria-hidden="true">
            <path fill="currentColor" d=${o.mdiMagnify}></path>
          </svg>
          <input
            type="text"
            class="search-input"
            placeholder="Search ${this._catalog.length.toLocaleString()} icons…"
            .value=${this._query}
            @input=${this._onSearchInput}
            @keydown=${t=>{"Enter"===t.key&&e.length>0&&(t.preventDefault(),this._select(e[0].name))}}
          />
        </div>
        <div class="grid-wrap">
          ${0===e.length?(0,a.qy)`<div class="empty">
                  <wa-icon
                    library="mdi"
                    name="magnify"
                    style="font-size: 24px;"
                  ></wa-icon>
                  No icons match “${this._query}”
                </div>`:(0,a.qy)`<div class="grid">
                  ${e.map(e=>(0,a.qy)`
                      <button
                        type="button"
                        class=${e.name===t?"icon-cell icon-cell--selected":"icon-cell"}
                        title=${`mdi:${e.name}`}
                        @click=${()=>this._select(e.name)}
                      >
                        <svg viewBox="0 0 24 24" aria-hidden="true">
                          <path fill="currentColor" d=${e.path}></path>
                        </svg>
                      </button>
                    `)}
                </div>`}
        </div>
        <div class="footer">
          <span>
            ${0===e.length?"No matches":e.length>=400?`400+ of ${this._catalog.length.toLocaleString()}`:`${e.length} of ${this._catalog.length.toLocaleString()}`}
          </span>
          ${t?(0,a.qy)`<span class="footer-name">mdi:${t}</span>`:a.s6}
        </div>
      </div>
    `}render(){let e=eC(this.value),t=`trigger${this.invalid?" invalid":""}`;return(0,a.qy)`
      <button
        type="button"
        class=${t}
        ?disabled=${this.disabled}
        @click=${this._toggle}
      >
        ${this._renderTriggerIcon()}
        <span
          class=${e?"trigger-label truncate":"trigger-label placeholder truncate"}
        >
          ${e?`mdi:${e}`:this.placeholder}
        </span>
        ${e&&!this.disabled?(0,a.qy)`<span
                class="trigger-clear"
                role="button"
                tabindex="-1"
                title="Clear"
                @click=${this._clear}
              >
                <svg width="14" height="14" viewBox="0 0 24 24" aria-hidden="true">
                  <path fill="currentColor" d=${o.mdiClose}></path>
                </svg>
              </span>`:a.s6}
        <svg class="trigger-chevron" viewBox="0 0 24 24" aria-hidden="true">
          <path fill="currentColor" d="M7,10L12,15L17,10H7Z"></path>
        </svg>
      </button>
      ${this._open?this._renderPanel():a.s6}
    `}constructor(...e){super(...e),this.value="",this.placeholder="Choose an icon…",this.invalid=!1,this.disabled=!1,this._open=!1,this._catalog=[],this._query="",this._loaded=!1,this._dismiss=new ex.J(this,()=>this._close(),{escapeTarget:document,onEscape:e=>e.stopPropagation()})}}function eS(e,t,i){return t||i?(0,a.qy)`<span class="option-stack">
    <span class="option-label">${e}</span>
    ${t?(0,a.qy)`<small class="option-description-note">${t}</small>`:a.s6}
    ${i?(0,a.qy)`<small class="option-default-note">${i}</small>`:a.s6}
  </span>`:(0,a.qy)`<span class="option-label">${e}</span>`}eq.styles=[eb.z9,ew.U,e$],ek([(0,n.MZ)()],eq.prototype,"value",void 0),ek([(0,n.MZ)()],eq.prototype,"placeholder",void 0),ek([(0,n.MZ)({type:Boolean})],eq.prototype,"invalid",void 0),ek([(0,n.MZ)({type:Boolean})],eq.prototype,"disabled",void 0),ek([(0,n.wk)()],eq.prototype,"_open",void 0),ek([(0,n.wk)()],eq.prototype,"_catalog",void 0),ek([(0,n.wk)()],eq.prototype,"_query",void 0),ek([(0,n.wk)()],eq.prototype,"_loaded",void 0),ek([(0,n.P)(".search-input")],eq.prototype,"_searchInput",void 0),eq=ek([(0,n.EM)("esphome-mdi-icon-picker")],eq);let eA=(0,a.AH)`
  :host {
    display: block;
  }

  .control {
    position: relative;
    display: block;
  }

  /* Leave room for the chevron sitting over the input's right edge. */
  input {
    padding-right: 34px;
  }

  .chevron {
    position: absolute;
    top: 0;
    right: 0;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    height: 100%;
    width: 32px;
    padding: 0;
    background: transparent;
    border: 0;
    color: var(--wa-color-text-quiet);
    font-size: 18px;
    cursor: pointer;
  }

  .chevron:disabled {
    cursor: not-allowed;
    opacity: 0.5;
  }

  .listbox {
    max-height: 280px;
    overflow-y: auto;
    background: var(--wa-color-surface-raised);
    border: var(--wa-border-width-s) solid var(--wa-color-surface-border);
    border-radius: var(--wa-border-radius-m);
    box-shadow: var(--wa-shadow-m);
    padding: var(--wa-space-2xs);
  }

  .option {
    padding: var(--wa-space-2xs) var(--wa-space-s);
    border-radius: var(--wa-border-radius-s);
    font-size: var(--wa-font-size-s);
    color: var(--wa-color-text-normal);
    cursor: pointer;
  }

  .option--active {
    background: var(--esphome-tint, var(--wa-color-surface-border));
  }

  .option-label {
    display: block;
  }
`;function eO(e,t,i,r){var o,a=arguments.length,n=a<3?t:null===r?r=Object.getOwnPropertyDescriptor(t,i):r;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)n=Reflect.decorate(e,t,i,r);else for(var s=e.length-1;s>=0;s--)(o=e[s])&&(n=(a<3?o(n):a>3?o(t,i,n):o(t,i))||n);return a>3&&n&&Object.defineProperty(t,i,n),n}i(7816),(0,q.C)({"chevron-down":o.mdiChevronDown});class eM extends a.WF{render(){let e=this._filtered,t=this._open?this._query:this.value,i=this._open&&e.length>0,r=i&&this._active>=0&&this._active<e.length?`option-${this._active}`:a.s6;return(0,a.qy)`
      <wa-popup placement="bottom-start" sync="width" distance="4" ?active=${i}>
        <div slot="anchor" class="control">
          <input
            type="text"
            class=${this.invalid?"invalid":""}
            role="combobox"
            aria-autocomplete="list"
            aria-invalid=${this.invalid?"true":a.s6}
            aria-expanded=${i?"true":"false"}
            aria-controls=${i?"listbox":a.s6}
            aria-activedescendant=${r}
            aria-label=${this.label||a.s6}
            .value=${t}
            placeholder=${this.placeholder}
            ?disabled=${this.disabled}
            autocomplete="off"
            spellcheck="false"
            @focus=${this._open_}
            @input=${this._onInput}
            @keydown=${this._onKeyDown}
            @blur=${this._close}
          />
          <button
            class="chevron"
            type="button"
            tabindex="-1"
            ?disabled=${this.disabled}
            aria-hidden="true"
            @mousedown=${this._preventBlur}
            @click=${this._toggle}
          >
            <wa-icon library="mdi" name="chevron-down"></wa-icon>
          </button>
        </div>
        ${i?(0,a.qy)`<div
                id="listbox"
                class="listbox"
                role="listbox"
                @mousedown=${this._preventBlur}
              >
                ${e.map((e,t)=>(0,a.qy)`<div
                      id="option-${t}"
                      class="option truncate ${t===this._active?"option--active":""}"
                      role="option"
                      aria-selected=${e.value===this.value?"true":"false"}
                      @mousedown=${this._preventBlur}
                      @click=${()=>this._select(e)}
                      @mouseenter=${()=>this._active=t}
                    >
                      ${eS(e.label,e.description,this._isDefault(e)?this.defaultNote:void 0)}
                    </div>`)}
              </div>`:a.s6}
      </wa-popup>
    `}_isDefault(e){return""!==this.defaultNote&&""!==this.defaultValue&&e.value.toLowerCase()===this.defaultValue.toLowerCase()}get _filtered(){if(!this._dirty)return this.options;let e=this._query.trim().toLowerCase();return e?this.options.filter(t=>t.value.toLowerCase().includes(e)||t.label.toLowerCase().includes(e)||t.description?.toLowerCase().includes(e)):this.options}_select(e){this.value=e.value,this._query=e.value,this._emit(e.value),this._close()}_emit(e){this.dispatchEvent(new CustomEvent("options-combobox-change",{detail:{value:e},bubbles:!1,composed:!1}))}_scrollActiveIntoView(){this.updateComplete.then(()=>this._activeOption?.scrollIntoView({block:"nearest"}))}constructor(...e){super(...e),this.options=[],this.value="",this.placeholder="",this.disabled=!1,this.invalid=!1,this.label="",this.defaultValue="",this.defaultNote="",this._open=!1,this._query="",this._dirty=!1,this._active=-1,this._committed="",this._open_=()=>{this.disabled||this._open||(this._open=!0,this._committed=this.value,this._query=this.value,this._dirty=!1,this._active=this.options.findIndex(e=>e.value===this.value),this._active>=0&&this._scrollActiveIntoView())},this._close=()=>{this._open=!1,this._active=-1,this._dirty=!1},this._toggle=()=>{this.disabled||(this._open?this._close():(this._open_(),this._input?.focus()))},this._preventBlur=e=>e.preventDefault(),this._onInput=e=>{let t=e.target.value;this._query=t,this._dirty=!0,this._open=!0,this._active=-1,this._emit(t)},this._onKeyDown=e=>{let t=this._filtered;switch(e.key){case"ArrowDown":e.preventDefault(),this._open||this._open_(),t.length&&(this._active=this._active>=t.length-1?0:this._active+1,this._scrollActiveIntoView());break;case"ArrowUp":e.preventDefault(),this._open||this._open_(),t.length&&(this._active=this._active<=0?t.length-1:this._active-1,this._scrollActiveIntoView());break;case"Enter":this._open&&this._active>=0&&t[this._active]?(e.preventDefault(),this._select(t[this._active])):this._close();break;case"Escape":this._open&&(e.preventDefault(),e.stopPropagation(),this.value=this._committed,this._query=this._committed,this._emit(this._committed),this._close());break;case"Tab":this._close()}}}}eM.styles=[eb.z9,ew.U,eA],eO([(0,n.MZ)({attribute:!1})],eM.prototype,"options",void 0),eO([(0,n.MZ)()],eM.prototype,"value",void 0),eO([(0,n.MZ)()],eM.prototype,"placeholder",void 0),eO([(0,n.MZ)({type:Boolean})],eM.prototype,"disabled",void 0),eO([(0,n.MZ)({type:Boolean})],eM.prototype,"invalid",void 0),eO([(0,n.MZ)()],eM.prototype,"label",void 0),eO([(0,n.MZ)()],eM.prototype,"defaultValue",void 0),eO([(0,n.MZ)()],eM.prototype,"defaultNote",void 0),eO([(0,n.wk)()],eM.prototype,"_open",void 0),eO([(0,n.wk)()],eM.prototype,"_query",void 0),eO([(0,n.wk)()],eM.prototype,"_dirty",void 0),eO([(0,n.wk)()],eM.prototype,"_active",void 0),eO([(0,n.P)("input")],eM.prototype,"_input",void 0),eO([(0,n.P)(".option--active")],eM.prototype,"_activeOption",void 0),eM=eO([(0,n.EM)("esphome-options-combobox")],eM);var eE=i(3508),eI=i(874),eP=i(6295),eR=i(2748);(0,q.C)({plus:o.mdiPlus});let eL="__esphome_add_new__",eF="__esphome_auto__";var eN=i(6160),eD=i(4776),ej=i(8404),eT=i(1376),eB=i(9460),eK=i(1888),eV=i(5089),eU=i(2943),eZ=i(565),eH=i(721),eG=i(7288),eW=i(7169),eY=i(5490),eQ=i(271),eJ=i(2);function eX(e){return null==e||""===e?"":(0,eY.uS)(e)||String(e)}let e0=new WeakMap;function e1(e,t,i){let r=i.getAt(t),o=(0,I.BO)(e,t,i,r);if(o)return o;let n=(0,L.FY)(r);if(null===n&&(0,eZ.rf)(r))return(0,I.JF)(e,t,i,r);let s=(null==r?(0,L.FY)(e.default_value):n)===!0;return(0,a.qy)`
    <div class="switch-field" data-field-key=${(0,I.DN)(t)}>
      <div class="field-info">
        ${(0,I.Lx)(e,i,{includeHelpLink:!1,path:t})}
      </div>
      ${(0,I.wm)(e,i)}
      <wa-switch
        ?checked=${s}
        ?disabled=${(0,I.U)(e,i)}
        aria-label=${(0,I.gt)(e,i)}
        @change=${e=>i.emitChange(t,e.target.checked)}
      ></wa-switch>
    </div>
  `}function e2(e,t,i){if(!t)return e;let r=e.filter(e=>!e.variants?.length||e.variants.includes(t)||e.value===i);return r.length>0?r:e}function e6(e){let t=(0,eB.cV)(`/assets/pin-wiring/${e}.svg`);return(0,a.qy)`<span
    class="pin-wiring-diagram pin-wiring-diagram--mask"
    style="-webkit-mask-image: url('${t}'); mask-image: url('${t}')"
    aria-hidden="true"
  ></span>`}function e3(e,t,i){var r,o,a,n,s,d,c,p,u,h;let m,g,v,_,y,b,w;if("mode"!==e.key||e.type!==l.Hh.NESTED)return i.renderEntry(e,[...t,e.key]);let x=[...t,e.key],$=i.getAt(x),k=function(e,t){if(!t||!(0,f.Qd)(e))return null;for(let i of Object.keys(e))if(Object.prototype.hasOwnProperty.call(t,i)){let e=t[i];return e.length>0?e:null}return null}(i.getAt(t),i.pinRegistryModes),z=k?(o=e,a=k,n="string"==typeof(r=$)?Object.keys((0,eK.o)(r)??{}):(0,f.Qd)(r)?Object.keys(r):[],m=new Set([...a,...n]),g=(o.config_entries??[]).filter(e=>m.has(e.key)),{...o,config_entries:g}):e;return"string"!=typeof $||(0,O.R_)($)?i.renderEntry(z,x):(s=z,d=x,(_="string"==typeof(v=(c=i).getAt(d))?(0,eK.o)(v):null)?Z(s,d,(p=c,u=d,h=_,y=u.join("."),b=e=>e.length===u.length+1&&e.slice(0,u.length).join(".")===y?e[u.length]:null,(w={...p,getAt:e=>{if(e.join(".")===y)return h;let t=b(e);return null!==t?h[t]:p.getAt(e)},scopeValues:e=>e.join(".")===y?{...h}:p.scopeValues(e),emitChange:(e,t)=>{let i=b(e);if(null===i)return void p.emitChange(e,t);let r={...h};t?r[i]=!0:delete r[i],p.emitChange(u,r)}}).renderEntry=(e,t)=>e.type===l.Hh.BOOLEAN?e1(e,t,w):p.renderEntry(e,t),w)):Z(s,d,c))}function e5(e){let t,{entry:i,path:r,ctx:o,rawValue:n,boardPin:s,guarded:d}=e,c=(0,f.Qd)(n),p=(0,I.U)(i,o),u=(i.config_entries??[]).map(e=>{var t;let i;return eD.C8.has(e.key)?(t=e,(i=e9.get(t))||(i=e4(t,()=>({advanced:!1})),e9.set(t,i)),i):e}),h=o.scopeValues(r),m=o.filterRenderable(u,h);if(0===m.length)return a.s6;let g=c&&Object.keys(h).some(e=>"number"!==e&&void 0!==h[e]);if(i.locked&&!g)return a.s6;let v=m.find(e=>"mode"===e.key&&e.type===l.Hh.NESTED),_=c?n.mode:void 0,y=c?n.inverted:void 0,b=v&&o.sectionKey.endsWith(".gpio")&&!(0,eN.GV)(n)&&(0,eD.B$)(_,y)?(0,eD.Ms)(i.pin_mode):[],w=b.length>0,x={kind:"default"};if(w){let e="preset"===(x=(0,eD.hK)(b,_,y,i.pin_mode)).kind&&!0===x.implicit?x.preset:null,r="preset"!==x.kind||e?o.localize("custom"===x.kind?"device.pin_wiring_custom":"device.pin_wiring_default"):o.localize(`device.pin_wiring_${x.preset.id}`),a="preset"===x.kind?x.preset:null,n=(0,eD.gF)(_),s=a&&0===Object.keys(n).length?a.flags:n,l=(0,eD.Zw)(s,!e&&!0===(0,L.FY)(y));t=l?o.localize("device.pin_wiring_summary_with_tech",{value:r,tech:l}):o.localize("device.pin_wiring_summary",{value:r})}let $=`${r.join(".")}${ey}`;g&&(!w||"custom"===x.kind)&&o.seedNestedOpen($);let k=o.nestedOpenSections.has($),z=()=>{c||null==n||""===n||o.emitChange(r,{number:n})},C=!w||u.some(e=>!eD.C8.has(e.key)),q=d||p?{...o,disabled:!0,renderEntry:(e,t)=>{var i,r;let a,n;return o.renderEntry((i=e,(n=(a=(r=d)?e8:e7).get(i))||(n=e4(i,r?()=>({locked:!0,locked_reason_key:"device.pin_wiring_guard_tooltip"}):()=>({locked:!0})),a.set(i,n)),n),t)}}:o;return(0,a.qy)`
    <div class="pin-advanced" data-field-key="${$}">
      ${m.map(e=>(0,a.qy)`<span
              hidden
              data-reveal-for=${(0,I.DN)([...r,e.key])}
              data-field-key="${$}"
            ></span>`)}
      ${(0,eT.u)({open:k,onToggle:()=>{!p&&(o.toggleNested($),k||d||!C||z())},localize:o.localize,labelKey:"device.pin_advanced",labelText:t,variant:"quiet",iconBefore:!0,disabled:p,body:()=>(0,a.qy)`${d?(0,a.qy)`<div class="pin-wiring-guard">
          <wa-icon library="mdi" name="lock-outline"></wa-icon>
          <div class="pin-wiring-guard-text">
            <span class="field-label">${o.localize("device.pin_wiring_guard")}</span>
            <p class="field-description">
              ${o.localize("device.pin_wiring_guard_hint")}
            </p>
          </div>
        </div>`:a.s6}
          ${w?function(e){let{longFormFields:t,modeValue:i,path:r,ctx:o,presets:n,state:s,boardPin:d}=e,c=o.disabled,p=!0===(0,L.FY)(e.invertedValue),u=`${r.join(".")}:pin-wiring`,h=!(0,f.Qd)(e.rawValue)&&null!=e.rawValue&&""!==e.rawValue,m="custom"===s.kind||"custom"===o.getClusterChoice(u)&&!h,g=n.map(e=>(0,eD.sB)(e,d)),v=g.some(e=>null!==e)?o.localize("device.pin_wiring_unavailable_input_only",{pin:d.label}):"",_=v?(0,a.qy)`<div class="warning-banner pin-wiring-banner">
        ${o.localize(e.pinMode===l.l3.OUTPUT?"device.pin_wiring_input_only_banner_output":"device.pin_wiring_input_only_banner",{pin:d.label})}
      </div>`:a.s6,y=t.find(e=>"inverted"===e.key),b=t.filter(e=>!eD.C8.has(e.key)),w=m?n.length:"preset"===s.kind?n.indexOf(s.preset):-1,x=[...n.map((e,t)=>!c&&null===g[t]),!c],$=(0,ej.vB)(w,x);return(0,a.qy)`
    ${_}
    <div
      class="pin-wiring-grid"
      role="radiogroup"
      aria-label=${o.localize("device.pin_wiring_group_label")}
      @keydown=${ej.tK}
    >
      ${n.map((t,i)=>{var n,s,l,h,m,f,_,y,b;let x,k;return n=t,s=i===w,l=i===$,h=g[i]?v:"",m=i===w?p:t.invertedWrite??p,f=e.guardTooltip,_=c,y=()=>{i!==w&&!c&&null===(0,eD.sB)(t,d)&&(o.setClusterChoice(u,""),o.emitChange(r,(0,eD.YV)(t,e.rawValue)))},b=o,x=["pin-wiring-card",s?"pin-wiring-card--selected":""].filter(Boolean).join(" "),k=_||!!h,(0,a.qy)`<button
    type="button"
    class=${x}
    data-preset=${n.id}
    role="radio"
    aria-checked=${s?"true":"false"}
    tabindex=${l?"0":"-1"}
    title=${f||a.s6}
    aria-disabled=${k?"true":"false"}
    @click=${k?a.s6:y}
  >
    ${e6(n.id)}
    <span class="pin-wiring-card-title">
      ${b.localize(`device.pin_wiring_${n.id}`)}
      ${n.recommended&&!h?(0,a.qy)`<span class="pin-wiring-badge">
              ${b.localize("device.pin_wiring_recommended")}
            </span>`:a.s6}
    </span>
    <span
      class="pin-wiring-card-desc${h?" pin-wiring-card-desc--reason":""}"
    >
      ${h||b.localize(`device.pin_wiring_${n.id}_description`)}
    </span>
    <code class="pin-wiring-card-tech">
      ${(0,eD.Zw)(n.flags,m)}
    </code>
  </button>`})}
      <button
        type="button"
        class="pin-wiring-card${m?" pin-wiring-card--selected":""}"
        data-preset="custom"
        role="radio"
        aria-checked=${m?"true":"false"}
        tabindex=${$===n.length?"0":"-1"}
        title=${e.guardTooltip||a.s6}
        aria-disabled=${c?"true":"false"}
        @click=${c?a.s6:()=>{c||(e.promoteShortForm(),o.setClusterChoice(u,"custom"))}}
      >
        <span class="pin-wiring-diagram pin-wiring-diagram--icon" aria-hidden="true">
          <wa-icon library="mdi" name="tune"></wa-icon>
        </span>
        <span class="pin-wiring-card-title">
          ${o.localize("device.pin_wiring_custom")}
        </span>
        <span class="pin-wiring-card-desc">
          ${o.localize("device.pin_wiring_custom_description")}
        </span>
      </button>
    </div>
    ${m?function(e,t,i,r,o,n,s=!1,d=null){let c=(0,eD.gF)(o);if(null===c||Object.keys(c).some(e=>!eD.Q6.has(e)))return(0,a.qy)`<div class="pin-wiring-custom">
      ${e3(e,i,r)}
      ${t?e3(t,i,r):a.s6}
    </div>`;let p=d===l.l3.INPUT?"input":d===l.l3.OUTPUT?"output":null,u={...c};!p||u.input||u.output||(u[p]=!0);let h=u.input&&u.output?"both":u.output?"output":u.input?"input":"",m=u.pullup?"pullup":u.pulldown?"pulldown":"none",f=(e,t)=>s&&e!==t&&"input"!==e&&"none"!==e,g=e=>{if(n)return;let t={...u};for(let i of(e(t),Object.keys(t)))t[i]||delete t[i];let o=Object.keys(t),a=0===o.length||1===o.length&&null!==p&&t[p];r.emitChange([...i,"mode"],a?void 0:t)},v=`pin-wiring-${i.join("-")}`,_=(e,t,i,o)=>(0,a.qy)`
    <wa-radio-group
      class="pin-wiring-radios"
      aria-labelledby=${e}
      .value=${t}
      ?disabled=${n}
      @change=${e=>i(e.target.value)}
    >
      ${o.map(([e,i])=>(0,a.qy)`<wa-radio value=${e} ?disabled=${f(e,t)}>
            ${r.localize(i)}
          </wa-radio>`)}
    </wa-radio-group>
  `;return(0,a.qy)`
    <div class="pin-wiring-custom">
      <div class="pin-wiring-row">
        <span class="field-label" id="${v}-direction">
          ${r.localize("device.pin_wiring_direction")}
        </span>
        <p class="field-description">
          ${r.localize("device.pin_wiring_direction_description")}
        </p>
        ${e6("direction")}
        ${_(`${v}-direction`,h,e=>{"input"!==e&&"output"!==e&&"both"!==e||f(e,h)||g(t=>{delete t.input,delete t.output,("input"===e||"both"===e)&&(t.input=!0),("output"===e||"both"===e)&&(t.output=!0)})},[["input","device.pin_wiring_direction_input"],["output","device.pin_wiring_direction_output"],["both","device.pin_wiring_direction_both"]])}
      </div>
      <div class="pin-wiring-row">
        <span class="field-label" id="${v}-pull">
          ${r.localize("device.pin_wiring_pull")}
        </span>
        <p class="field-description">
          ${r.localize("device.pin_wiring_pull_description")}
        </p>
        ${e6("pull_resistor")}
        ${_(`${v}-pull`,m,e=>{"none"!==e&&"pullup"!==e&&"pulldown"!==e||f(e,m)||g(t=>{delete t.pullup,delete t.pulldown,"pullup"===e&&(t.pullup=!0),"pulldown"===e&&(t.pulldown=!0)})},[["none","device.pin_wiring_pull_none"],["pullup","device.pin_wiring_pull_up"],["pulldown","device.pin_wiring_pull_down"]])}
      </div>
      ${u.open_drain||"output"===h||"both"===h?(0,a.qy)`<div class="switch-field">
              <div class="field-info">
                <label class="field-label">
                  ${r.localize("device.pin_wiring_open_drain")}
                </label>
                <p class="field-description">
                  ${r.localize("device.pin_wiring_open_drain_description")}
                </p>
              </div>
              <wa-switch
                ?checked=${!!u.open_drain}
                ?disabled=${n||s&&!u.open_drain}
                aria-label=${r.localize("device.pin_wiring_open_drain")}
                @change=${e=>{let t=e.target.checked;t&&s||g(e=>{e.open_drain=t})}}
              ></wa-switch>
            </div>`:a.s6}
      ${t?e3(t,i,r):a.s6}
    </div>
  `}(e.modeChild,y,r,o,i,c,d?.features.includes(l.k6.INPUT_ONLY)??!1,e.pinMode):a.s6}
    ${b.map(e=>e3(e,r,o))}
  `}({longFormFields:m,modeChild:v,pinMode:i.pin_mode??null,modeValue:_,invertedValue:y,guardTooltip:d?o.localize("device.pin_wiring_guard_tooltip"):"",path:r,ctx:q,rawValue:n,presets:b,state:x,boardPin:s,promoteShortForm:z}):m.map(e=>e3(e,r,q))}`})}
    </div>
  `}function e4(e,t){return{...e,...t(e),config_entries:e.config_entries?.map(e=>e4(e,t))??e.config_entries}}(0,q.C)({tune:o.mdiTune});let e9=new WeakMap,e8=new WeakMap,e7=new WeakMap;function te(e,t){let i="string"==typeof e?e.trim():(0,f.Qd)(e)&&"string"==typeof e.number?e.number.trim():"";if(!i)return null;let r=i.toLowerCase(),o=t.find(e=>e.aliases?.some(e=>e.toLowerCase()===r));return o?o.gpio:null}function tt(e,t){return(0,eN.j8)(e)??te(e,t)}function ti(e,t){let i=t.join("."),r=[t[0],"value",...t.slice(1)],o=new Set,a=new Set,n=new Set;for(let t of e.board?.featured_components??[]){if(t.component_id!==e.sectionKey)continue;for(let[e,r]of Object.entries(t.locked_pins??{}))"number"==typeof r?(o.add(r),e===i&&a.add(r)):"string"==typeof r&&e===i&&n.add(r);let s=(0,f.O6)(t.fields??{},r);if(null==s)continue;let l=(0,eN.E7)(s)??te(s,e.board?.pins??[]);if("number"==typeof l)a.add(l);else if("string"==typeof l)n.add(l);else if("string"==typeof s)n.add(s);else{let e=(0,eN.Sn)(s),t=void 0!==e?(0,eN.eT)(s[e]):null;null!==t&&n.add(`${e}:${t}:*`)}}return{lockedGpios:o,gpios:a,tokens:n}}function tr(e,t){return e.has(t)||e.has(`${t.slice(0,t.lastIndexOf(":")+1)}*`)}function to(e,t){return(0,a.qy)`<wa-option
    class=${e.warn?"pin-option pin-option--warn":"pin-option"}
    value=${e.optValue}
    .label=${e.primary}
    ?selected=${e.optValue===t}
    ?disabled=${e.disabled}
    title=${e.titleText}
  >
    <span class="pin-option-stack">
      <span class="pin-option-primary">
        ${e.primary}
        ${e.warn?(0,a.qy)`<wa-icon
                class="pin-warn-icon"
                library="mdi"
                name="alert-circle-outline"
              ></wa-icon>`:a.s6}
      </span>
      ${e.secondary?(0,a.qy)`<span class="pin-option-secondary">${e.secondary}</span>`:a.s6}
    </span>
  </wa-option>`}var ta=i(1020),tn=i(9470);function ts(e,t){let i=e.getAt(t);return Array.isArray(i)?i:[]}function tl(e,t,i){return{addItem:()=>e.emitChange(t,[...ts(e,t),i()]),removeAt:i=>{e.rowsMoved(t,T(i)),e.emitChange(t,ts(e,t).filter((e,t)=>t!==i))}}}function td(e,t){return 0===e.length?(0,a.qy)`<p class="field-description">${t.localize("device.multi_value_empty")}</p>`:a.s6}function tc(e,t,i){return(0,a.qy)`
    <button
      type="button"
      class="multi-btn"
      ?disabled=${t}
      aria-label=${e.localize("device.multi_value_remove")}
      @click=${i}
    >
      ${(0,ta.R)(o.mdiClose)}
    </button>
  `}function tp(e,t,i){return(0,a.qy)`
    <button
      type="button"
      class="multi-btn multi-add"
      ?disabled=${t}
      @click=${i}
    >
      ${(0,ta.R)(o.mdiPlus)} ${e.localize("device.multi_value_add")}
    </button>
  `}var tu=i(5109),th=i(7219),tm=i(3336);function tf(e,t,i,r){var o,a=arguments.length,n=a<3?t:null===r?r=Object.getOwnPropertyDescriptor(t,i):r;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)n=Reflect.decorate(e,t,i,r);else for(var s=e.length-1;s>=0;s--)(o=e[s])&&(n=(a<3?o(n):a>3?o(t,i,n):o(t,i))||n);return a>3&&n&&Object.defineProperty(t,i,n),n}class tg extends a.WF{connectedCallback(){super.connectedCallback();let e=this._ops();if(null===e)return;this._unsubscribe=(0,tu.z2)(()=>{if(!this.isConnected)return;let e=this._ops();if(null===e)return;let t=e.cache();void 0!==t&&(this._catalog=t,this._fetchError=!1)});let t=e.cache();this._fetchError=!1,void 0!==t?this._catalog=t:this._kickFetch(e)}updated(){if(this._kickedFetch||null!==this._catalog||this._fetchError||!this._api)return;let e=this._ops();null!==e&&void 0===e.cache()&&this._kickFetch(e)}_kickFetch(e){this._api&&(this._kickedFetch=!0,e.fetch(this._api).catch(e=>{console.error("Failed to fetch registry catalog",e),this.isConnected&&(this._fetchError=!0)}))}_ops(){let e=this.entry?.registry??"";return th.Dh[e]??null}disconnectedCallback(){super.disconnectedCallback(),this._unsubscribe?.(),this._unsubscribe=void 0,this._kickedFetch=!1}render(){let e=this._ops();if(null===e)return(0,a.qy)`
        <div class="field" data-field-key=${(0,I.DN)(this.path)}>
          ${(0,I.Lx)(this.entry,this.ctx,{path:this.path})}
          <p class="registry-list-fallback">
            ${this.ctx.localize("device.registry_list_unsupported")}
          </p>
          ${(0,I.FL)(this.path,this.ctx)}
        </div>
      `;let t=this.ctx.getAt(this.path);if(t instanceof L.ho||void 0!==t&&!Array.isArray(t))return(0,a.qy)`
        <div class="field" data-field-key=${(0,I.DN)(this.path)}>
          ${(0,I.Lx)(this.entry,this.ctx,{path:this.path})}
          <p class="field-description">
            ${this.ctx.localize("device.multi_value_yaml_only")}
          </p>
          ${(0,I.FL)(this.path,this.ctx)}
        </div>
      `;let i=(0,th.DD)(t),{items:r,positions:o}=(0,th.Fj)(i),n=(0,I.U)(this.entry,this.ctx),s=this.ctx.sectionKey?e.parentToken(this.ctx.sectionKey):"",l=(this._catalog??[]).filter(e=>!s||!e.applies_to?.length||e.applies_to.includes(s)),d=null!==this._catalog&&0===this._catalog.length,c=this._fetchError?(0,a.qy)`<p class="registry-list-fallback">
          ${this.ctx.localize("device.registry_list_error")}
          ${this._api?(0,a.qy)`<button type="button" class="multi-btn" @click=${this._retryFetch}>
                  ${this.ctx.localize("device.registry_list_retry")}
                </button>`:a.s6}
        </p>`:null===this._catalog?(0,a.qy)`<p class="registry-list-fallback">
            ${this.ctx.localize("device.registry_list_loading")}
          </p>`:d?(0,a.qy)`<p class="registry-list-fallback">
              ${this.ctx.localize("device.registry_list_empty_catalog")}
            </p>`:0===l.length?(0,a.qy)`<p class="registry-list-fallback">
                ${this.ctx.localize("device.registry_list_no_applicable_options")}
              </p>`:a.s6,p=n||0===l.length;return(0,a.qy)`
      <div class="field" data-field-key=${(0,I.DN)(this.path)}>
        ${(0,I.Lx)(this.entry,this.ctx,{path:this.path})}
        ${td(r,this.ctx)} ${c}
        ${r.map((t,i)=>this._renderRow(t,i,o[i],l,r,n,e.dedupByTypeId))}
        ${tp(this.ctx,p,()=>this._addItem())}
        ${(0,I.FL)(this.path,this.ctx)}
      </div>
    `}_renderRow(e,t,i,r,o,n,s){let l=(0,th.XG)(e),d=new Set;s&&o.forEach((e,i)=>{if(i===t)return;let r=(0,th.XG)(e);r&&d.add(r)});let c=r.find(e=>e.id===l),p=void 0!==c,u=[...r].sort((e,t)=>e.id.localeCompare(t.id)),h=l?e[l]:null,m=null!==h&&"object"==typeof h&&!Array.isArray(h)&&!(0,W.b)(h)&&!(h instanceof L.ho),f=c?.config_entries,g=c?.value_type==="time_period"&&(m&&f?.length===0||(0,eJ.Hb)(h)&&!f?.some(e=>Object.prototype.hasOwnProperty.call(h,e.key))),v=m&&!g?null:this._scalarDispatchType(c,h),_=(null===h||m)&&f?f:[];return(0,a.qy)`
      <div class="registry-list-item" data-row-index=${t}>
        <div class="registry-list-row">
          <wa-select
            .value=${l}
            ?disabled=${n}
            placeholder=${this.ctx.localize("device.registry_list_select")}
            aria-label=${this.ctx.localize("device.registry_list_row_label",{index:String(t+1)})}
            @change=${e=>{let i=e.target.value;this._renameRow(t,i)}}
          >
            ${!p&&l?(0,a.qy)`<wa-option value=${l} selected
                    >${(0,th.Q$)(l)}</wa-option
                  >`:a.s6}
            ${u.filter(e=>e.id===l||!d.has(e.id)).map(e=>(0,a.qy)`<wa-option value=${e.id} ?selected=${e.id===l}
                    >${(0,th.Q$)(e.id)}</wa-option
                  >`)}
          </wa-select>
          ${tc(this.ctx,n,()=>this._removeAt(t))}
        </div>
        ${this._renderSubForm(i,l,v,_,c)}
      </div>
    `}_editable(){let e=(0,th.DD)(this.ctx.getAt(this.path));return{list:e,...(0,th.Fj)(e)}}_scalarDispatchType(e,t){let i=(0,tm.aj)(e);return null!==i?i:(0,eJ.QH)(t)?l.Hh.TIME_PERIOD:null}_renderSubForm(e,t,i,r,o){return null!==i?(0,a.qy)`<div class="registry-list-sub-form">
        ${this.ctx.renderEntry((0,tm.as)(i,o),[...this.path,String(e),t])}
      </div>`:r.length>0?(0,a.qy)`<div class="registry-list-sub-form">
        ${r.map(i=>this.ctx.renderEntry(i,[...this.path,String(e),t,i.key]))}
      </div>`:a.s6}_addItem(){let{list:e,positions:t}=this._editable();this.ctx.emitChange(this.path,(0,th.hC)(e,t,{}))}_removeAt(e){let{list:t,positions:i}=this._editable(),r=i[e];void 0!==r&&(this.ctx.rowsMoved(this.path,T(r)),this.ctx.emitChange(this.path,t.filter((e,t)=>t!==r)))}_renameRow(e,t){if(!t)return;let{list:i,items:r,positions:o}=this._editable(),a=r[e];if(!a||(0,th.XG)(a)===t)return;let n=o[e];this.ctx.rowsMoved(this.path,e=>e===n?null:e),this.ctx.emitChange(this.path,i.map((e,i)=>i===n?{[t]:null}:e))}constructor(...e){super(...e),this.path=[],this._catalog=null,this._fetchError=!1,this._kickedFetch=!1,this._retryFetch=()=>{if(!this._api)return;let e=this._ops();null!==e&&(this._fetchError=!1,e.fetch(this._api).catch(e=>{console.error("Failed to retry registry catalog fetch",e),this.isConnected&&(this._fetchError=!0)}))}}}tg.styles=[...I.M8,(0,a.AH)`
      :host {
        display: block;
      }
      .registry-list-item {
        margin-bottom: 1rem;
      }
      .registry-list-row {
        display: flex;
        gap: 0.5rem;
        align-items: center;
        margin-bottom: 0.5rem;
      }
      .registry-list-row wa-select {
        flex: 1;
      }
      .registry-list-sub-form {
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
        margin-left: 1rem;
        padding-left: 1rem;
        border-left: 2px solid var(--wa-color-surface-border);
      }
      .registry-list-fallback {
        color: var(--wa-color-neutral-fill-loud);
        font-size: 0.9rem;
      }
    `],tf([(0,r.Fg)({context:d.Ie})],tg.prototype,"_api",void 0),tf([(0,n.MZ)({attribute:!1})],tg.prototype,"entry",void 0),tf([(0,n.MZ)({attribute:!1})],tg.prototype,"path",void 0),tf([(0,n.MZ)({attribute:!1})],tg.prototype,"ctx",void 0),tf([(0,n.wk)()],tg.prototype,"_catalog",void 0),tf([(0,n.wk)()],tg.prototype,"_fetchError",void 0),tg=tf([(0,n.EM)("esphome-registry-list")],tg);var tv=i(2911);i(8944);var t_=i(918),ty=i(1209),tb=i(7228);async function tw(e,t,i,r,o){try{return await o(),(0,ty.ik)(e),!0}catch(e){return console.error(i,e),(0,t_.UG)(r(t)),!1}}function tx(e,t,i,r,o){return tw(e,o.errorKey,o.logLabel,r,async()=>{let{created:a}=await (0,tb.j)(e,t,i);t_.me[a?"success":"info"](r(a?o.createdKey:"device.secret_picker_linked",{key:t}))})}var t$=i(1529),tk=i(7967);i(1958),i(5910);var tz=i(8990),tC=i(9309);function tq(e,t,i,r){var o,a=arguments.length,n=a<3?t:null===r?r=Object.getOwnPropertyDescriptor(t,i):r;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)n=Reflect.decorate(e,t,i,r);else for(var s=e.length-1;s>=0;s--)(o=e[s])&&(n=(a<3?o(n):a>3?o(t,i,n):o(t,i))||n);return a>3&&n&&Object.defineProperty(t,i,n),n}i(8768),(0,q.C)({alert:o.mdiAlert,"content-copy":o.mdiContentCopy});class tS extends a.WF{willUpdate(e){(e.has("secretKey")||e.has("present"))&&(this._draftValue="",this._stored=null,this._busy=!1,this._loading=!1,this._loadError=!1,this._loadToken++,this._opToken++)}updated(){this.present&&this.secretKey&&this._api&&null===this._stored&&!this._loading&&!this._loadError&&this._loadStored()}render(){return this.present?this._renderEdit():this._renderCreate()}get _dirty(){return null!==this._stored&&this._draftValue!==this._stored}get _hasDraft(){return""!==this._draftValue.trim()}get _loadingStored(){return this.present&&null===this._stored}_renderEdit(){return this._loadError?this._renderLoadError():(0,a.qy)`<div class="row">
        ${this._renderInput()}
        <button
          class="copy"
          type="button"
          ?disabled=${this._busy||this._loadingStored}
          title=${this._localize("device.secret_reveal_copy")}
          aria-label=${this._localize("device.secret_reveal_copy")}
          @click=${this._copy}
        >
          <wa-icon library="mdi" name="content-copy"></wa-icon>
        </button>
        <button
          class="save"
          type="button"
          ?disabled=${this._busy||!this._dirty}
          @click=${this._save}
        >
          ${this._localize("device.secret_picker_save")}
        </button>
      </div>
      <esphome-confirm-dialog
        heading=${this._localize("device.secret_picker_shared_confirm_title")}
        confirm-label=${this._localize("device.secret_picker_save")}
        message=${this._localize("device.secret_picker_shared_confirm_message",{key:this.secretKey})}
        @confirm=${this._persist}
      ></esphome-confirm-dialog>`}_renderLoadError(){return(0,a.qy)`<div class="fix">
      <span class="msg" role="alert">
        <wa-icon library="mdi" name="alert"></wa-icon>
        ${this._localize("device.secret_picker_reveal_error")}
        <button class="retry link-button" type="button" @click=${this._retry}>
          ${this._localize("device.secret_picker_retry")}
        </button>
      </span>
    </div>`}_renderCreate(){return(0,a.qy)`<div class="fix">
      <span class="msg" role="alert">
        <wa-icon library="mdi" name="alert"></wa-icon>
        ${this._localize("device.secret_picker_missing",{key:this.secretKey})}
      </span>
      <div class="row">
        ${this._renderInput()}
        <button
          class="save"
          type="button"
          ?disabled=${this._busy||!this._hasDraft}
          @click=${this._create}
        >
          ${this._localize("device.secret_picker_missing_create")}
        </button>
      </div>
    </div>`}_renderInput(){return(0,a.qy)`<esphome-password-input
      class="value"
      .value=${this._draftValue}
      .disabled=${this._busy||this._loadingStored}
      .placeholder=${this._localize(this.present?"device.secret_picker_value":"device.secret_picker_missing_placeholder")}
      .label=${this._localize("device.secret_picker_value_label",{key:this.secretKey})}
      @password-input-change=${e=>{this._draftValue=e.detail.value}}
      @keydown=${e=>{"Enter"===e.key&&(e.preventDefault(),this.present?this._save():this._create())}}
    ></esphome-password-input>`}async _loadStored(){let e=++this._loadToken;this._loading=!0;let t=null,i=!1;try{let e=await this._api.getConfig(tk.R_);t=(0,tk.Tv)(e,this.secretKey)}catch{i=!0,(0,t_.UG)(this._localize("device.secret_picker_reveal_error"))}if(e===this._loadToken){if(this._loading=!1,i){this._loadError=!0;return}this._stored=t??"",this._draftValue=this._stored}}async _run(e,t){let i=this._api;if(!i||!this.secretKey||this._busy)return;let r=this._opToken;this._busy=!0;try{let o=await e(i);if(r!==this._opToken)return;o&&t()}finally{r===this._opToken&&(this._busy=!1)}}constructor(...e){super(...e),this._localize=e=>e,this.secretKey="",this.present=!1,this.deviceName="",this._draftValue="",this._stored=null,this._busy=!1,this._loadError=!1,this._loadToken=0,this._opToken=0,this._loading=!1,this._retry=()=>{this._loadError=!1},this._copy=async()=>{await (0,tC.l)(this._draftValue)&&(0,t_.VX)(this._localize("device.secret_reveal_copied"))},this._create=()=>{this._hasDraft&&this._run(e=>tx(e,this.secretKey,this._draftValue,this._localize,{createdKey:"device.secret_picker_missing_created",errorKey:"device.secret_picker_missing_error",logLabel:"Secret create failed"}),()=>{this._draftValue=""})},this._save=()=>{if(this._dirty){if((0,tk.e2)(this.secretKey,this.deviceName))return void this._confirmDialog?.open();this._persist()}},this._persist=()=>{this._run(e=>{var t,i,r,o;return t=this.secretKey,i=this._draftValue,r=this._localize,tw(e,(o={savedKey:"device.secret_picker_saved",errorKey:"device.secret_picker_save_error",logLabel:"Secret save failed"}).errorKey,o.logLabel,r,async()=>{await (0,tb.x)(e,t,i),(0,t_.VX)(r(o.savedKey,{key:t}))})},()=>{this._stored=this._draftValue})}}}function tA(e,t,i,r){var o,a=arguments.length,n=a<3?t:null===r?r=Object.getOwnPropertyDescriptor(t,i):r;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)n=Reflect.decorate(e,t,i,r);else for(var s=e.length-1;s>=0;s--)(o=e[s])&&(n=(a<3?o(n):a>3?o(t,i,n):o(t,i))||n);return a>3&&n&&Object.defineProperty(t,i,n),n}tS.styles=[tz.R,(0,a.AH)`
      :host {
        display: block;
      }

      .fix {
        display: flex;
        flex-direction: column;
        gap: var(--wa-space-2xs);
        padding-left: var(--wa-space-2xs);
      }

      .msg {
        display: flex;
        align-items: center;
        gap: var(--wa-space-2xs);
        font-size: var(--wa-font-size-xs);
        color: var(--wa-color-danger-border, var(--wa-color-danger-60));
      }

      .row {
        display: flex;
        align-items: center;
        gap: var(--wa-space-xs);
      }

      /* esphome-password-input is display:block; flex so it shares the row. */
      esphome-password-input {
        flex: 1;
        min-width: 0;
      }

      .copy {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 28px;
        height: 28px;
        flex-shrink: 0;
        padding: 0;
        border: none;
        border-radius: var(--wa-border-radius-m);
        background: transparent;
        color: var(--wa-color-text-quiet);
        cursor: pointer;
        transition:
          background 0.12s,
          color 0.12s;
      }

      .copy:hover:not(:disabled) {
        background: var(--wa-color-surface-border);
        color: var(--wa-color-text-normal);
      }

      .copy:disabled {
        opacity: 0.5;
        cursor: not-allowed;
      }

      .copy wa-icon {
        font-size: 15px;
      }

      .save {
        padding: 0 14px;
        min-height: var(--wa-form-control-height);
        box-sizing: border-box;
        flex-shrink: 0;
        border: var(--wa-border-width-s) solid var(--esphome-primary);
        border-radius: var(--wa-border-radius-m);
        background: var(--esphome-primary);
        color: var(--wa-color-surface-default);
        font-family: inherit;
        font-size: var(--wa-font-size-s);
        cursor: pointer;
        transition:
          opacity 0.12s,
          background 0.12s;
      }

      .save:hover:not(:disabled) {
        opacity: 0.9;
      }

      .save:disabled {
        opacity: 0.5;
        cursor: not-allowed;
      }
    `],tq([(0,r.Fg)({context:d.$F,subscribe:!0}),(0,n.wk)()],tS.prototype,"_localize",void 0),tq([(0,r.Fg)({context:d.Ie,subscribe:!0}),(0,n.wk)()],tS.prototype,"_api",void 0),tq([(0,n.MZ)({attribute:"secret-key"})],tS.prototype,"secretKey",void 0),tq([(0,n.MZ)({type:Boolean})],tS.prototype,"present",void 0),tq([(0,n.MZ)({attribute:"device-name"})],tS.prototype,"deviceName",void 0),tq([(0,n.P)("esphome-confirm-dialog")],tS.prototype,"_confirmDialog",void 0),tq([(0,n.wk)()],tS.prototype,"_draftValue",void 0),tq([(0,n.wk)()],tS.prototype,"_stored",void 0),tq([(0,n.wk)()],tS.prototype,"_busy",void 0),tq([(0,n.wk)()],tS.prototype,"_loadError",void 0),tS=tq([(0,n.EM)("esphome-secret-value")],tS),(0,q.C)({alert:o.mdiAlert,check:o.mdiCheck,"chevron-down":o.mdiChevronDown,"key-variant":o.mdiKeyVariant,plus:o.mdiPlus,"shield-key-outline":o.mdiShieldKeyOutline});class tO extends a.WF{get _keys(){return this._secretKeys.value}get _migrateTarget(){return this.recommendedKeys[0]??""}get _canMigrate(){return""===this.selectedKey&&""!==this.value&&""!==this._migrateTarget&&void 0!==this._keys&&!this._keys.includes(this._migrateTarget)}get _missing(){return""!==this.selectedKey&&void 0!==this._keys&&!this._keys.includes(this.selectedKey)}render(){let e=""!==this.selectedKey,t=this._missing,i=(0,tk.Jw)(this._keys??[],[...this.recommendedKeys,this.selectedKey],this.deviceName,this._devices.map(e=>e.name)),r=new Set(i),o=new Set(this.recommendedKeys),n=this.recommendedKeys.filter(e=>r.has(e)),s=i.filter(e=>!o.has(e));return(0,a.qy)`
      <wa-dropdown @wa-select=${this._onSelect}>
        <button
          slot="trigger"
          class=${t?"trigger missing":e?"trigger selected":"trigger"}
          type="button"
          ?disabled=${this.disabled}
          aria-label=${this._localize(t?"device.secret_picker_aria_missing":"device.secret_picker_aria",{field:this.fieldLabel})}
        >
          <wa-icon
            class="key"
            library="mdi"
            name=${t?"alert":"key-variant"}
          ></wa-icon>
          ${e?(0,a.qy)`<span class="label">${this.selectedKey}</span>`:(0,a.qy)`<span class="placeholder"
                  >${this._localize("device.secret_picker_label")}</span
                >`}
          <wa-icon class="chevron" library="mdi" name="chevron-down"></wa-icon>
        </button>
        ${this._canMigrate?(0,a.qy)`<wa-dropdown-item class="migrate" value=${"__esphome_migrate_secret__"}>
                  <wa-icon slot="icon" library="mdi" name="shield-key-outline"></wa-icon>
                  ${this._localize("device.secret_picker_migrate",{key:this._migrateTarget})}
                </wa-dropdown-item>
                <wa-divider role="separator"></wa-divider>`:a.s6}
        ${n.length?(0,a.qy)`<small class="group-label" aria-hidden="true"
                  >${this._localize("device.secret_picker_related")}</small
                >
                ${n.map(e=>this._renderKeyItem(e))}
                ${s.length?(0,a.qy)`<small class="group-label" aria-hidden="true"
                        >${this._localize("device.secret_picker_shared")}</small
                      >`:a.s6}`:a.s6}
        ${s.map(e=>this._renderKeyItem(e))}
        ${i.length?a.s6:(0,a.qy)`<wa-dropdown-item class="empty" disabled role="status"
                >${this._localize("device.secret_picker_empty")}</wa-dropdown-item
              >`}
        <wa-divider role="separator"></wa-divider>
        <wa-dropdown-item class="create" value=${"__esphome_create_secret__"}>
          <wa-icon slot="icon" library="mdi" name="plus"></wa-icon>
          ${this._localize("device.secret_picker_create")}
        </wa-dropdown-item>
        ${e?(0,a.qy)`<wa-dropdown-item class="manual" value=${"__esphome_manual_value__"}>
                ${this._localize("device.secret_picker_manual")}
              </wa-dropdown-item>`:a.s6}
      </wa-dropdown>
      ${e?(0,a.qy)`<esphome-secret-value
              secret-key=${this.selectedKey}
              ?present=${!t}
              device-name=${this.deviceName}
            ></esphome-secret-value>`:a.s6}
    `}_renderKeyItem(e){return(0,a.qy)`<wa-dropdown-item
      value=${e}
      aria-selected=${e===this.selectedKey?"true":"false"}
    >
      ${e===this.selectedKey?(0,a.qy)`<wa-icon slot="icon" class="check" library="mdi" name="check"></wa-icon>`:a.s6}
      ${e}
    </wa-dropdown-item>`}_onSelect(e){let t=e.detail.item,i=t.classList;if(i?.contains("create"))return void(0,t$.oo)("/secrets");if(i?.contains("migrate"))return void this._migrate();if(i?.contains("manual"))return void this._manual();let r=t.value??"";r&&this._emit(`!secret ${r}`)}async _manual(){if(!this._api||!this.selectedKey)return void this._emit("");try{let e=await this._api.getConfig(tk.R_);this._emit((0,tk.Tv)(e,this.selectedKey)??"")}catch{(0,t_.UG)(this._localize("device.secret_picker_manual_error"))}}_emit(e){this.dispatchEvent(new CustomEvent("secret-selected",{detail:{value:e},bubbles:!0,composed:!0}))}async _migrate(){let e=this._migrateTarget;this._api&&e&&this.value&&await tx(this._api,e,this.value,this._localize,{createdKey:"device.secret_picker_migrated",errorKey:"device.secret_picker_migrate_error",logLabel:"Secret migration failed"})&&this._emit(`!secret ${e}`)}constructor(...e){super(...e),this._localize=e=>e,this._devices=[],this.disabled=!1,this.deviceName="",this.full=!1,this.fieldLabel="",this.selectedKey="",this.value="",this.recommendedKeys=[],this._secretKeys=new A(this,{getCached:ty.BW,subscribe:ty.Ft,fetch:ty.RX},()=>this._api)}}function tM(e,t,i,r){var o,a=arguments.length,n=a<3?t:null===r?r=Object.getOwnPropertyDescriptor(t,i):r;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)n=Reflect.decorate(e,t,i,r);else for(var s=e.length-1;s>=0;s--)(o=e[s])&&(n=(a<3?o(n):a>3?o(t,i,n):o(t,i))||n);return a>3&&n&&Object.defineProperty(t,i,n),n}tO.styles=(0,a.AH)`
    :host {
      display: inline-flex;
    }

    :host([full]) {
      display: flex;
      flex-direction: column;
      align-items: stretch;
      gap: var(--wa-space-2xs);
      width: 100%;
    }

    :host([full]) wa-dropdown,
    :host([full]) .trigger {
      width: 100%;
    }

    :host([full]) .chevron {
      margin-left: auto;
    }

    .trigger {
      display: inline-flex;
      align-items: center;
      gap: 4px;
      padding: 0 10px;
      min-height: 34px;
      box-sizing: border-box;
      background: transparent;
      border: var(--wa-border-width-s) solid var(--wa-color-surface-border);
      border-radius: var(--wa-border-radius-m);
      color: var(--wa-color-text-quiet);
      font-family: inherit;
      font-size: var(--wa-font-size-xs);
      white-space: nowrap;
      cursor: pointer;
      transition:
        background 0.12s,
        border-color 0.12s,
        color 0.12s;
    }

    .trigger:hover:not(:disabled) {
      color: var(--esphome-primary);
      border-color: var(--esphome-primary);
      background: var(--esphome-tint);
    }

    /* Reads as a select that's already pointed at a secret. */
    .trigger.selected {
      color: var(--wa-color-text-normal);
      border-color: var(--esphome-primary);
    }

    /* Referenced secret is absent from secrets.yaml — flag it. */
    .trigger.missing {
      color: var(--wa-color-text-normal);
      border-color: var(--wa-color-danger-border, var(--wa-color-danger-60));
    }

    .trigger.missing .key {
      color: var(--wa-color-danger-border, var(--wa-color-danger-60));
    }

    .trigger:disabled {
      opacity: 0.5;
      cursor: not-allowed;
    }

    .trigger .key {
      font-size: 15px;
      color: var(--esphome-primary);
    }

    .trigger .label {
      /* flex + min-width:0 so a long key actually shrinks and ellipsizes
         inside the inline-flex trigger (notably in full / width:100% mode). */
      flex: 1;
      min-width: 0;
      font-family: ui-monospace, "SF Mono", Menlo, Consolas, monospace;
      overflow: hidden;
      text-overflow: ellipsis;
    }

    .trigger .placeholder {
      color: var(--wa-color-text-quiet);
    }

    .trigger .chevron {
      font-size: 14px;
    }

    /* Keep the menu inside the viewport on small screens and wrap long
       keys / the migrate label instead of overflowing off-screen. */
    wa-dropdown::part(menu) {
      max-width: min(92vw, 340px);
      box-sizing: border-box;
    }

    wa-dropdown-item {
      max-width: min(92vw, 340px);
      box-sizing: border-box;
    }

    wa-dropdown-item::part(label) {
      white-space: normal;
      overflow-wrap: anywhere;
    }

    .group-label {
      display: block;
      padding: var(--wa-space-2xs) var(--wa-space-s) 0;
      font-size: var(--wa-font-size-2xs);
      font-weight: var(--wa-font-weight-semibold);
      color: var(--wa-color-text-quiet);
      text-transform: uppercase;
    }

    .empty {
      color: var(--wa-color-text-quiet);
    }

    .check {
      font-size: 15px;
      color: var(--esphome-primary);
    }

    .create wa-icon,
    .migrate wa-icon {
      font-size: 15px;
    }
  `,tA([(0,r.Fg)({context:d.$F,subscribe:!0}),(0,n.wk)()],tO.prototype,"_localize",void 0),tA([(0,r.Fg)({context:d.Ie,subscribe:!0}),(0,n.wk)()],tO.prototype,"_api",void 0),tA([(0,r.Fg)({context:d.xJ,subscribe:!0}),(0,n.wk)()],tO.prototype,"_devices",void 0),tA([(0,n.MZ)({type:Boolean})],tO.prototype,"disabled",void 0),tA([(0,n.MZ)({attribute:"device-name"})],tO.prototype,"deviceName",void 0),tA([(0,n.MZ)({type:Boolean,reflect:!0})],tO.prototype,"full",void 0),tA([(0,n.MZ)({attribute:"field-label"})],tO.prototype,"fieldLabel",void 0),tA([(0,n.MZ)({attribute:"selected-key"})],tO.prototype,"selectedKey",void 0),tA([(0,n.MZ)()],tO.prototype,"value",void 0),tA([(0,n.MZ)({attribute:!1})],tO.prototype,"recommendedKeys",void 0),tO=tA([(0,n.EM)("esphome-secret-picker")],tO),(0,q.C)({"alert-circle-outline":o.mdiAlertCircleOutline,"chevron-down":o.mdiChevronDown,"chevron-up":o.mdiChevronUp,close:o.mdiClose,"open-in-new":o.mdiOpenInNew});class tE extends a.WF{render(){let e=this._buildCtx(),t=function(e,t,i,r){let o=(0,m.lb)(t,i,r.id);if(!o)return e;let a=!1,n=e.map(e=>{let t=o.fields[e.key];if(!t?.locked)return e;let i=function e(t,i,r){var o,a,n;let s;if(t.locked||t.type===l.Hh.PIN)return t;if((0,f.Qd)(i)){let o=t.config_entries;if(!o)return _.has(t)||(_.add(t),console.warn(`Board mapping preset for '${t.key}' has no nested schema entries; lock not applied`)),t;if(!(0,f.Qd)(r))return t;let a=!1,n=o.map(t=>{if(!(t.key in i))return t;let o=e(t,i[t.key],r[t.key]);return o!==t&&(a=!0),o});return a?function(e,t){let i=v.get(e);if(i&&t.every((e,t)=>e===i.config_entries[t]))return i;let r={...e,config_entries:t};return v.set(e,r),r}(t,n):t}return(o=r,a=i,null!=o&&null!==a&&(Array.isArray(a)||Array.isArray(o)?JSON.stringify(o)===JSON.stringify(a):"object"!=typeof a&&"object"!=typeof o&&String(o)===String(a)))?(n=t,(s=g.get(n))||(s={...n,locked:!0,locked_reason_key:"device.pin_wiring_guard_tooltip"},g.set(n,s)),s):t}(e,t.value,r[e.key]);return i!==e&&(a=!0),i});return a?n:e}(this.entries,this.board,this.sectionKey,this.values),i=this.requiredOnly?function(e){let t=new Map;for(let i of e)i.exclusive_group&&t.set(i.exclusive_group,(t.get(i.exclusive_group)??!1)||!!i.required);let i=e=>e.exclusive_group?t.get(e.exclusive_group):!!e.required;return[...e.filter(i),...e.filter(e=>!i(e))]}(t):t;return this.advancedSection?this._renderWithAdvancedSection(i,e):this._renderFlat(i,e)}_renderFlat(e,t){let i=(0,eE.c4)(e,this.values,this.requiredGroups,(0,E.xx)(this)),r=this._makeItemRenderer(i,t);return(0,a.qy)`${this._renderConstraintBanners(t,i)}${i.ordered.map(r)}`}_renderWithAdvancedSection(e,t){let i=(0,eE.c4)(e,this.values,this.requiredGroups,(0,E.xx)(this,{showAdvanced:!0})),r=this._makeItemRenderer(i,t),o=this._advancedUnitClassifier(i),n=new Set(i.clusters.filter(e=>"none"!==e.mode).map(e=>e.cluster.members[0].key)),s=i.ordered.filter(e=>!!Array.isArray(e)||(i.memberKeys.has(e.key)?n.has(e.key):i.visible.has(e))),l=s.filter(e=>!o(e)),d=s.filter(e=>o(e)),p=(0,c.RQ)(e),u=d.length>0&&0===l.length&&!this.forceAdvancedControl&&!this.gateAdvanced,h=[],m=d;if(this.gateAdvanced){let e=e=>{if(Array.isArray(e))return(0,eE.TP)(e,this.values);if(i.memberKeys.has(e.key)){let t=i.clusterByFirstKey.get(e.key);return!!t&&(0,eE.TP)(t.cluster.members,this.values)}return(0,b.P)(e,this.values)};for(let t of(m=[],d)){let i;if(this.showAdvanced){let r=Array.isArray(t)?t[0].key:t.key;i=this._openAdvancedPlacement.get(r)??e(t),this._openAdvancedPlacement.set(r,i)}else i=e(t);(i?h:m).push(t)}}let f=this._effectiveForceOpen(),g=this.showAdvanced||f||u,v=this.forceAdvancedControl||p&&!u,_=m.length+this.advancedExtraCount;return(0,a.qy)`${this._renderConstraintBanners(t,i)}${l.map(r)}${h.map(r)}${v?this._renderAdvancedControl(g,_,f):a.s6}${g?m.map(r):a.s6}`}_makeItemRenderer(e,t){return i=>{if(Array.isArray(i))return(0,tv.g_)(e.groupPaints.get(i),t);if(e.memberKeys.has(i.key)){let r=e.clusterByFirstKey.get(i.key);return r?(0,N.kB)(r,t):a.s6}return e.visible.has(i)?this._renderEntry(i,i.key?[i.key]:[],t):a.s6}}_advancedForceOpen(){return this.entries.some(e=>e.advanced&&(0,b.P)(e,this.values))}_effectiveForceOpen(){return!this.gateAdvanced&&this._advancedForceOpen()}_advancedUnitClassifier(e){let t=new Map;for(let{cluster:i}of e.clusters){let e=(0,eE.gl)(i.members);for(let r of i.members)t.set(r.key,e)}return i=>Array.isArray(i)?(0,eE.gl)(i):e.memberKeys.has(i.key)?t.get(i.key)??!1:!!i.advanced}_renderAdvancedControl(e,t,i){let r=t>0?this._localize("device.show_advanced_count",{count:t}):this._localize("device.show_advanced");return(0,a.qy)`<div class="advanced-toggle-row">
      <wa-switch
        size="small"
        ?disabled=${i}
        .checked=${e}
        @change=${e=>{let t=e.currentTarget,i=t.parentElement;i&&(this._advancedControlAnchor={top:i.getBoundingClientRect().top,at:performance.now()}),this._emitAdvancedToggle(t.checked)}}
      >
        ${r}
      </wa-switch>
    </div>`}_restoreAdvancedControlAnchor(e){let t=this._advancedControlAnchor;if(!t||!e.has("showAdvanced")||(this._advancedControlAnchor=void 0,performance.now()-t.at>2e3))return;let i=this.shadowRoot?.querySelector(".advanced-toggle-row");if(!i)return;let r=function(e){for(let t=S(e);t;t=S(t))if(t instanceof HTMLElement&&t.scrollHeight>t.clientHeight){let e=getComputedStyle(t).overflowY;if("auto"===e||"scroll"===e)return t}return null}(i);r&&(r.scrollTop+=i.getBoundingClientRect().top-t.top)}_emitAdvancedToggle(e){(0,y.r)(this,"advanced-toggle",{show:e})}_renderConstraintBanners(e,t){return D(t.unmet.filter(e=>"banner"===e.source),this.entries,e)}connectedCallback(){super.connectedCallback(),this._unsubscribeProviders=(0,C.y_)(()=>this.requestUpdate())}disconnectedCallback(){super.disconnectedCallback(),this._unsubscribeProviders?.(),this._unsubscribeProviders=void 0}willUpdate(e){var t;let i=e.get("entries"),r=e.has("entries")&&void 0!==i,o=e.has("valuesRead");(o||r&&(t=this.entries,!(i.length===t.length&&i.every((e,i)=>{var r,o;return(r=e)===(o=t[i])||!!r.config_entries&&r.config_entries===o.config_entries&&r.key===o.key&&r.type===o.type}))))&&(ep.delete(this),U.delete(this)),(o||r)&&(this._valueMemory.clear(),this._constraintClusters.reset()),o&&function(...e){for(let t of e)for(let e of[...t])e.endsWith(ey)&&t.delete(e)}(this._nestedOpenSections,this._seededNestedOpen),r&&(this._openAdvancedPlacement.clear(),this._expandedOptionFields.clear(),this._seededNestedOpen.clear()),e.has("showAdvanced")&&!this.showAdvanced&&this._openAdvancedPlacement.clear()}_pathOf(e){return(0,I.lt)(e.getAttribute("data-field-key")??"")}updated(e){super.updated(e),this._syncSelectValues(),this._fieldScroll.maybeScroll(e),this.advancedSection&&!this.showAdvanced&&this._effectiveForceOpen()&&this._emitAdvancedToggle(!0),this._maybeRevealForFocus(),this._restoreAdvancedControlAnchor(e)}_maybeRevealForFocus(){if(!this.advancedSection||this.showAdvanced||!this.focusFieldPath?.length||0===this.entries.length)return;let e=(0,I.DN)(this.focusFieldPath);if(e===this._focusRevealKey)return;let t=(0,eE._r)(this.entries,this.requiredGroups,this.values);(0,c.WG)(this.entries,this.focusFieldPath,this.values,t)&&(this._focusRevealKey=e,this._emitAdvancedToggle(!0))}async _syncSelectValues(){if(this.shadowRoot)for(let e of this.shadowRoot.querySelectorAll("[data-field-key]")){let t=e.querySelector("wa-select");if(!t)continue;if(t.hasAttribute("data-no-value-sync")){await this._syncSelectedAttr(t);continue}if(!t.hasUpdated&&t.updateComplete)try{await t.updateComplete}catch{}let i=this._pathOf(e);if(!i.length)continue;let r=(0,f.O6)(this.values,i);if(!(0,f.k4)(r)){""!==(Array.isArray(t.value)?t.value[0]??"":t.value??"")&&(t.value="");continue}let o=String(r??""),a=Array.isArray(t.value)?t.value[0]??"":t.value??"";if(a===o||null!==(0,w.O)(r,[a]))continue;let n=this._matchOptionValue(t,r)??o;a!==n&&(t.value=n)}}_matchOptionValue(e,t){let i=Array.from(e.querySelectorAll("wa-option"),e=>e.value??"");return(0,w.O)(t,i)}async _syncSelectedAttr(e){if(!e.hasUpdated&&e.updateComplete)try{await e.updateComplete}catch{}let t=e.querySelector("wa-option[selected]"),i=t?.value??"";(Array.isArray(e.value)?e.value[0]??"":e.value??"")!==i&&(e.value=i)}_renderEntry(e,t,i){try{return this._renderEntryUnsafe(e,t,i)}catch(r){console.error("esphome-config-entry-form: render failed for entry",{key:e.key,type:e.type,path:t},r);let i=(0,h.u)(r);return(0,a.qy)`<div class="render-error" role="alert">
        <wa-icon library="mdi" name="alert-circle-outline"></wa-icon>
        <div>
          <strong> ${this._localize("device.entry_render_error_title")} </strong>
          <code class="render-error-key"
            >${e.key||"(empty key)"} · ${e.type}</code
          >
          <pre class="render-error-message">${i}</pre>
        </div>
      </div>`}}_renderEntryUnsafe(e,t,i){if(e.templatable&&!(0,E.Hh)(e.type)){var r;let o,n,s,l,d,c,p;return r=()=>this._renderEntryLeaf(e,t,i),o=i.getAt(t),n=(0,W.b)(o),(s=ep.get(i.stashOwner))||(s=new Map,ep.set(i.stashOwner,s)),l=t.join("."),(d=s.get(l))||(d={},s.set(l,d)),c=d,p=(0,I.DN)(t),(0,a.qy)`
    <div class="templatable-field" data-field-key=${p}>
      ${(0,ec.L)({isLambda:n,disabled:i.disabled,localize:i.localize,onSwitch:e=>{e!==n&&(n?(c.lambda=(0,W.b)(o)?o._lambda:"",i.emitChange(t,c.literal??"")):(c.literal=o,i.emitChange(t,{_lambda:c.lambda??"",_tag:"!lambda"})))}})}
      ${n?ed(e,t,i):r()}
    </div>
  `}return this._renderEntryLeaf(e,t,i)}_renderEntryLeaf(e,t,i){let r=i.getAt(t),n=e.type===l.Hh.PIN&&!e.multi_value;if((0,O.zZ)(r)&&!n){let r=e.type===l.Hh.SECURE_STRING?"password":"text";return(0,I.Mf)(e,r,t,i)}if(e.type===l.Hh.DIVIDER)return(0,a.qy)`<wa-divider></wa-divider>`;if(e.type===l.Hh.LABEL)return(0,a.qy)`<p class="label-entry">${(0,I.gt)(e,i)}</p>`;if(e.type===l.Hh.ALERT)return(0,a.qy)`<div class="alert-entry">${(0,I.gt)(e,i)}</div>`;if(e.type===l.Hh.NESTED)return e.multi_value?function(e,t,i){let r=i.getAt(t);if(r instanceof L.ho)return(0,a.qy)`
      <div class="nested-list" data-field-key=${(0,I.DN)(t)}>
        ${(0,I.Lx)(e,i,{path:t})}
        <p class="field-description">${i.localize("device.multi_value_yaml_only")}</p>
        ${(0,I.FL)(t,i)}
      </div>
    `;let o=(0,f.ly)(r),n=(0,I.U)(e,i),{addItem:s,removeAt:l}=tl(i,t,()=>{let t;return(t=function(e,t,{requiredOnly:i=!1}={}){let r=(0,F.Rj)(e,i);return r?{key:r.key,id:V(e,t)}:null}(e,i,{requiredOnly:!0}))?{[t.key]:t.id}:{}}),d=(0,I.gt)(e,i),c=e.config_entries??[];return(0,a.qy)`
    <div class="nested-list" data-field-key=${(0,I.DN)(t)}>
      ${(0,I.Lx)(e,i,{path:t})} ${td(o,i)}
      ${o.map((e,r)=>{let o=[...t,String(r)],s=i.filterRenderable(c,e);return(0,a.qy)`
          <div class="nested-list-item" data-field-key=${(0,I.DN)(o)}>
            <div class="nested-list-item-header">
              <span class="nested-list-item-title"> ${d} ${r+1} </span>
              ${tc(i,n,()=>l(r))}
            </div>
            <div class="nested-fields">
              ${s.map(e=>i.renderEntry(e,[...o,e.key]))}
            </div>
          </div>
        `})}
      ${tp(i,n,s)} ${(0,I.FL)(t,i)}
    </div>
  `}(e,t,i):Z(e,t,i);if(e.type===l.Hh.MAP){let r,n,s,l,d,c;return r=(e.config_entries??[])[0],l=Object.keys(s=(n=i.getAt(t))&&"object"==typeof n&&!Array.isArray(n)?n:{}),d=(0,I.U)(e,i),c=()=>{let e=i.getAt(t);return e&&"object"==typeof e&&!Array.isArray(e)?Object.assign(Object.create(null),e):Object.create(null)},(0,a.qy)`
    <div class="field" data-field-key=${(0,I.DN)(t)}>
      ${(0,I.Lx)(e,i,{path:t})}
      ${0===l.length?(0,a.qy)`<p class="field-description">${i.localize("device.map_empty")}</p>`:a.s6}
      ${l.map(e=>{let n,l,p;return n=[...t,e],l=s[e],p=!(0,f.k4)(l)&&!(0,W.b)(l),(0,a.qy)`
      <div class="map-row" data-field-key=${(0,I.DN)(n)}>
        <input
          type="text"
          class="multi-input map-key-input"
          .value=${e}
          ?disabled=${d}
          @change=${r=>((e,r)=>{if(e===r||!r)return;let o=i.getAt(t);if(!o||"object"!=typeof o||Array.isArray(o)||r in o)return;let a=Object.create(null);for(let[t,i]of Object.entries(o))a[t===e?r:t]=i;i.emitChange(t,a)})(e,r.target.value)}
        />
        <div class="map-value">
          ${p?(0,a.qy)`<p class="map-value-yaml-only">
                  ${i.localize("device.map_value_edit_in_yaml")}
                </p>`:r?i.renderEntry(r,n):a.s6}
        </div>
        <button
          type="button"
          class="multi-btn"
          ?disabled=${d}
          aria-label=${i.localize("device.map_remove")}
          @click=${()=>{let r;e in(r=c())&&(delete r[e],i.emitChange(t,r))}}
        >
          ${(0,ta.R)(o.mdiClose)}
        </button>
      </div>
    `})}
      <button
        type="button"
        class="multi-btn multi-add"
        ?disabled=${d}
        @click=${()=>{let e=c(),r=1;for(;`new_${r}`in e;)r++;e[`new_${r}`]="",i.emitChange(t,e)}}
      >
        ${(0,ta.R)(o.mdiPlus)} ${i.localize("device.map_add")}
      </button>
      ${(0,I.FL)(t,i)}
    </div>
  `}if(e.type===l.Hh.REGISTRY_LIST)return(0,a.qy)`<esphome-registry-list
    .entry=${e}
    .path=${t}
    .ctx=${i}
  ></esphome-registry-list>`;if(e.multi_value)return function(e,t,i){let r=ts(i,t);if(r.some(e=>!(0,f.k4)(e)))return(0,I.YJ)(e,t,i);let o=(e.type===l.Hh.INTEGER||e.type===l.Hh.FLOAT)&&"hex"!==e.display_format,n=o&&e.type===l.Hh.INTEGER,s=o&&e.type===l.Hh.FLOAT,d=o?r.map(e=>String(e??"")):r.map(e=>(0,tn.hZ)(String(e))),c=(0,I.U)(e,i),{addItem:p,removeAt:u}=tl(i,t,()=>"");return(0,a.qy)`
    <div class="field" data-field-key=${(0,I.DN)(t)}>
      ${(0,I.Lx)(e,i,{path:t})} ${td(d,i)}
      ${d.map((l,d)=>{let p=s&&null!=r[d]&&""!==r[d]&&Number.isFinite(Number(String(r[d]))),h=[...t,String(d)],m=null!==i.errorAt(h),f=n?i.getEditingMagnitude(h)??l:l;return(0,a.qy)`
          <div class="multi-row">
            <div class="multi-value-cell">
              <input
                type=${p?"number":"text"}
                autocomplete="off"
                spellcheck="false"
                step=${p?"any":a.s6}
                class="multi-input ${m?"invalid":""}"
                .value=${f}
                ?disabled=${c}
                @input=${r=>{let a,s=r.target.value;n&&i.setEditingMagnitude(h,s),(a=[...ts(i,t)])[d]=o?(0,eU.aY)(e,s):(0,tn.iI)(s),i.emitChange(t,a)}}
                @blur=${()=>{n&&i.clearEditingMagnitude(h)}}
              />
              ${(0,I.Nk)(String(r[d]??""),i.substitutions,i.localize)}
              ${(0,I.FL)(h,i)}
            </div>
            ${tc(i,c,()=>u(d))}
          </div>
        `})}
      ${tp(i,c,p)} ${(0,I.FL)(t,i)}
    </div>
  `}(e,t,i);if(e.references_component)return function(e,t,i){let r=e.references_component||"",o=i.resolveInterfaceProviders(r),n=(0,eI.Zm)(i.yaml,r,o??[]),s=e.references_class?i.catalogById():null,l=(0,eP.m)(i.yaml,n,e,s),d=l.candidates,c=null!==o&&l.noneMatch,p=i.getAt(t),u=(0,I.BO)(e,t,i,p);if(u)return u;let h=String(p??""),m=null!==i.errorAt(t),f=""===h?(0,eI.z)(d,i.yaml):null,g=(e,t,i)=>(0,a.qy)`
    <wa-option
      class="id-option"
      value=${e}
      .label=${t}
      ?selected=${e===h}
    >
      <span class="id-option-stack">
        <span class="id-option-primary">${t}</span>
        <span class="id-option-secondary">${i}</span>
      </span>
    </wa-option>
  `,v=d.find(e=>e.id===h),_=""!==h&&!v,y=i.isOptionsExpanded(t)?d:v?[v]:[],b=_&&n.some(e=>e.id===h),w=_?g(h,h,i.localize(b?"device.id_reference_wrong_kind":"device.id_reference_unresolved",{domain:r})):a.s6,x=!m&&null!==o&&(0,eI.Ty)(h,n,i.yaml),$=!m&&b,k=x?(0,eR.O)(i.localize("device.id_reference_unknown_error",{id:h})):$?(0,eR.O)(i.localize("device.id_reference_wrong_kind",{domain:r})):a.s6,z=0===d.length&&!_,C=z&&!c&&!e.required&&(0,L.Zn)(i.yaml).has(r),q=e=>{let o=e.target,a=o.value;if(a===eL){o.value=h,i.requestAddComponent(r);return}i.emitChange(t,a===eF?"":a)},S=e.required||""===h||c?a.s6:g(eF,i.localize("device.id_reference_auto"),i.localize("device.id_reference_auto_detail",{domain:r})),A=(0,a.qy)`
    <wa-option
      class="id-option id-option-add ${z&&!C?"id-option-add--solo":""}"
      value=${eL}
    >
      <span class="id-option-stack">
        <span class="id-option-primary id-option-primary-add">
          <wa-icon library="mdi" name="plus"></wa-icon>
          ${i.localize("device.id_reference_add",{domain:r})}
        </span>
      </span>
    </wa-option>
  `;return z?(0,a.qy)`
      <div class="field" data-field-key=${(0,I.DN)(t)}>
        ${(0,I.Lx)(e,i,{path:t})}
        <wa-select
          class=${m?"invalid":""}
          ?disabled=${(0,I.U)(e,i)}
          placeholder=${i.localize(C?"device.id_reference_auto_configured":c?"device.id_reference_none_match":"device.id_reference_empty",{domain:r})}
          @change=${q}
        >
          ${C?g(eF,i.localize("device.id_reference_auto"),i.localize("device.id_reference_auto_detail",{domain:r})):a.s6}
          ${A}
        </wa-select>
        ${(0,I.FL)(t,i)}
      </div>
    `:(0,a.qy)`
    <div class="field" data-field-key=${(0,I.DN)(t)}>
      ${(0,I.Lx)(e,i,{path:t})}
      <wa-select
        class=${m||x||$?"invalid":""}
        ?disabled=${(0,I.U)(e,i)}
        placeholder=${f?(0,O.rq)(f.name,i.substitutions)||f.id:a.s6}
        @wa-show=${()=>i.expandOptions(t)}
        @change=${q}
      >
        ${S} ${w}
        ${y.map(e=>{let t=e.name?`${e.id} \xb7 ${r}`:r,o=(0,O.rq)(e.name,i.substitutions);return g(e.id,o||e.id,e===f?`${t} \xb7 ${i.localize("device.default_option_tag")}`:t)})}
        ${A}
      </wa-select>
      ${(0,I.FL)(t,i)}${k}
    </div>
  `}(e,t,i);if(e.options&&e.options.length>0)return function(e,t,i){let r,o,n=i.getAt(t),s=(0,I.BO)(e,t,i,n);if(s)return s;let l=String(n??""),d=null!==i.errorAt(t),c=(0,I.U)(e,i);if(e.suggestions&&e.suggestions.length>0)return(0,I.jT)(e,t,n,d,c,i);let p=(o=((r=String(i.getAt(["board"])??""))?(0,eV.S)(r):i.board?.esphome.variant??"").toLowerCase()).startsWith("esp32")?o:"";if(e.allow_custom_value&&e.options&&e.options.length>0){let r=(0,eZ.yz)(l,e.options);return(0,a.qy)`
      <div class="field" data-field-key=${(0,I.DN)(t)}>
        ${(0,I.Lx)(e,i,{path:t})}
        <esphome-options-combobox
          .options=${e2(e.options,p,(0,w.O)(n,e.options.map(e=>e.value)))}
          .value=${l}
          label=${e.label}
          placeholder=${String(e.default_value??"")}
          .defaultValue=${String(e.default_value??"")}
          .defaultNote=${i.localize("device.default_option_tag")}
          ?disabled=${c}
          ?invalid=${d}
          @options-combobox-change=${r=>i.emitChange(t,(0,eU.aY)(e,r.detail.value))}
        ></esphome-options-combobox>
        ${(0,I.FL)(t,i)}
        ${r?(0,a.qy)`<span class="field-warning" role="status"
                >${i.localize("validation.did_you_mean",{suggestion:r})}</span
              >`:a.s6}
      </div>
    `}let u=function(e,t,i){if(i&&"variant"===e.key&&"esp32"===t.sectionKey)return e.options?.some(e=>e.value.toLowerCase()===i)?i:void 0}(e,i,p)??(null!=e.default_value?String(e.default_value):""),h=u.toLowerCase(),m=e.options?.find(e=>e.value.toLowerCase()===h),f=m?.label??u,{clearable:g,visibleOptions:v}=function(e){let t=e0.get(e);if(!t){let i=e.options??[];t={clearable:i.some(e=>""===e.value),visibleOptions:i.filter(e=>""!==e.value)},e0.set(e,t)}return t}(e),_=(0,w.O)(n,v.map(e=>e.value)),y=e2(v,p,_);return(0,a.qy)`
    <div class="field" data-field-key=${(0,I.DN)(t)}>
      ${(0,I.Lx)(e,i,{path:t})}
      <wa-select
        class=${d?"invalid":""}
        ?disabled=${c}
        .withClear=${g}
        placeholder=${f}
        @change=${r=>i.emitChange(t,(0,eU.aY)(e,r.target.value))}
      >
        ${g?(0,a.qy)`<wa-icon slot="clear-icon" library="mdi" name="close"></wa-icon>`:a.s6}
        ${y.map(e=>{let t=e.value===_,r=""!==u&&e.value.toLowerCase()===h?i.localize("device.default_option_tag"):void 0;return r||e.description?(0,a.qy)`<wa-option
            value=${e.value}
            .label=${e.label}
            ?selected=${t}
          >
            ${eS(e.label,e.description,r)}
          </wa-option>`:(0,a.qy)`<wa-option value=${e.value} ?selected=${t}
              >${eS(e.label)}</wa-option
            >`})}
      </wa-select>
      ${(0,I.FL)(t,i)}
    </div>
  `}(e,t,i);switch(e.type){case l.Hh.BOOLEAN:return e1(e,t,i);case l.Hh.SELECT:return(0,I.Mf)(e,"text",t,i);case l.Hh.SECURE_STRING:return(0,I.Mf)(e,"password",t,i);case l.Hh.INTEGER:case l.Hh.FLOAT:return function(e,t,i){var r,o,n,s,d,c;if(e.suggestions&&e.suggestions.length>0)return(0,I.Mf)(e,"number",t,i);let p=i.getAt(t),u=(0,I.BO)(e,t,i,p);if(u)return u;if("hex"===e.display_format){let s,l,d,c,p;return r=e,o=t,s=(n=i).getAt(o),l=null!==n.errorAt(o),d=(0,I.U)(r,n),c=n.getEditingMagnitude(o)??eX(s),p=eX(r.default_value),(0,I.tj)(r,o,n,(0,a.qy)`<input
      type="text"
      autocomplete="off"
      spellcheck="false"
      class=${l?"invalid":""}
      .value=${c}
      ?disabled=${d}
      placeholder=${p}
      @input=${e=>{let t=e.target.value;(n.setEditingMagnitude(o,t),""===t)?n.emitChange(o,""):n.emitChange(o,(0,eY.uS)((0,eY.EG)(t))||t)}}
      @blur=${()=>n.clearEditingMagnitude(o)}
    />`)}if(e.type===l.Hh.INTEGER){let r,o,n;return s=e,d=t,r=(c=i).getEditingMagnitude(d)??String(c.getAt(d)??""),o=null!==c.errorAt(d),n=(0,I.U)(s,c),(0,I.tj)(s,d,c,(0,a.qy)`<input
      type="text"
      autocomplete="off"
      spellcheck="false"
      class=${o?"invalid":""}
      .value=${r}
      ?disabled=${n}
      placeholder=${String(s.default_value??"")}
      @input=${e=>{let t=e.target.value;c.setEditingMagnitude(d,t),c.emitChange(d,(0,eQ.s)(t))}}
      @blur=${()=>c.clearEditingMagnitude(d)}
    />`)}if(null!=p&&!Number.isFinite(Number(String(p))))return(0,I.JF)(e,t,i,p);let h=String(p??""),m=null!==i.errorAt(t),f=e.range?String(e.range[0]):void 0,g=e.range?String(e.range[1]):void 0,v=(0,I.U)(e,i);return(0,I.tj)(e,t,i,(0,a.qy)`<input
      type="number"
      class=${m?"invalid":""}
      .value=${h}
      ?disabled=${v}
      min=${f??""}
      max=${g??""}
      step="any"
      placeholder=${String(e.default_value??"")}
      @input=${r=>{let o=r.target.value;i.emitChange(t,(0,eU.aY)(e,o))}}
    />`)}(e,t,i);case l.Hh.FLOAT_WITH_UNIT:return function(e,t,i){let r=e.unit_options??[],o=r[0]??"",n=i.getAt(t),s=(0,I.BO)(e,t,i,n);if(s)return s;let l=(0,eW.Eb)(n,r),d=i.getEditingMagnitude(t);if(null===l.value&&null==d&&null!=n&&""!==String(n).trim())return(0,I.JF)(e,t,i,n);let c=d??(null===l.value?"":String(l.value)),p=(0,eW.E3)(n,e.default_value,i.getPendingUnit(t),r),u=(0,eW.hX)(r,e.range,[o,(0,eW.Ji)(e.default_value,r),p]),h=(0,eW.x9)(e.default_value,r),m=null!==i.errorAt(t),f=(0,I.U)(e,i),g=p===o,v=e.range&&g?String(e.range[0]):void 0,_=e.range&&g?String(e.range[1]):void 0,y=e=>i.emitChange(t,(0,eW.BR)(e));return(0,a.qy)`
    <div class="field float-with-unit" data-field-key=${(0,I.DN)(t)}>
      ${(0,I.Lx)(e,i,{path:t})}
      <div class="float-with-unit-inputs">
        <input
          type="number"
          class=${m?"invalid":""}
          .value=${c}
          ?disabled=${f}
          min=${(0,eG.J)(v)}
          max=${(0,eG.J)(_)}
          step="any"
          placeholder=${h}
          @input=${e=>{let r=e.target.value;i.setEditingMagnitude(t,r);let o=(0,eU.pz)(r);""===o?(i.setPendingUnit(t,p),y({value:null,unit:p})):"number"==typeof o?y({value:o,unit:p}):i.emitChange(t,o+p)}}
          @blur=${()=>i.clearEditingMagnitude(t)}
        />
        ${u.length>1?(0,a.qy)`
                <wa-select
                  data-no-value-sync
                  ?disabled=${f}
                  @change=${e=>{let r=e.target.value;null===l.value?i.setPendingUnit(t,r):y({value:l.value,unit:r})}}
                >
                  ${u.map(e=>(0,a.qy)`<wa-option value=${e} ?selected=${e===p}
                        >${e}</wa-option
                      >`)}
                </wa-select>
              `:(0,a.qy)`<span class="float-with-unit-suffix">${p}</span>`}
      </div>
      ${(0,I.FL)(t,i)}
    </div>
  `}(e,t,i);case l.Hh.TIME_PERIOD:return function(e,t,i){let r=i.getAt(t),o=(e.accepts_duration_mapping?(0,eJ.nh)(r):null)??r,n=(0,I.BO)(e,t,i,o);if(n)return n;let s=(0,eJ.gF)(o),l=null!==i.errorAt(t),d=(0,I.U)(e,i);if(!s.parseable)return(0,I.JF)(e,t,i,o);let c=void 0!==e.default_value&&null!==e.default_value?(0,eJ.gF)(e.default_value):null,p=c&&c.parseable?c.value:"",u=null!=o&&""!==o,h=u&&!s.unitless,m=(0,eJ.ze)(e.duration_min_unit),f=m.find(e=>e===i.getPendingUnit(t)),g=h?s.unit:f??(0,eJ.cU)(c?.parseable?c.unit:s.unit,e.duration_min_unit),v=u&&!h?null:g;return(0,a.qy)`
    <div class="field time-period" data-field-key=${(0,I.DN)(t)}>
      ${(0,I.Lx)(e,i,{path:t})}
      <div class="time-period-inputs">
        <input
          type="text"
          inputmode="decimal"
          class=${l?"invalid":""}
          .value=${s.value}
          ?disabled=${d}
          placeholder=${p}
          @input=${e=>{let r=e.target.value;i.emitChange(t,(0,eJ.n9)(r,g))}}
        />
        <wa-select
          data-no-value-sync
          aria-label=${i.localize("device.automation_action_delay_unit")}
          placeholder=${i.localize("device.automation_action_delay_unit")}
          ?disabled=${d}
          @change=${e=>{let r=e.target.value;i.setPendingUnit(t,r),u&&i.emitChange(t,(0,eJ.n9)(s.value,r))}}
        >
          ${(h?(0,eJ.ze)(e.duration_min_unit,g):m).map(e=>(0,a.qy)`<wa-option value=${e} ?selected=${e===v}
                >${i.localize(`device.automation_action_delay_unit_${e}`)}</wa-option
              >`)}
        </wa-select>
      </div>
      ${(0,I.FL)(t,i)}
    </div>
  `}(e,t,i);case l.Hh.PIN:return function(e,t,i){let r=i.getAt(t);if((0,O.zZ)(r)||(0,f.Qd)(r)&&(0,O.zZ)(r.number)){var o,n,s,d;let l,c,p,u,h,m,g,v,_,y,b;return o=e,n=t,s=i,d=r,c=(l=(0,f.Qd)(d)?d:null)?l.number:d,p=l?[...n,"number"]:n,u=null!==s.errorAt(p),h=(0,I.U)(o,s),m=s.board?.pins??[],g=(0,O.rq)(c,s.substitutions),v=(0,eN.E7)(l?{...l,number:g}:g)??((0,eN.GV)(d)?null:te(g,m)),_=ti(s,n),y=null!==v&&("number"==typeof v?_.gpios.has(v)||(o.suggestions??[]).some(e=>tt(e,m)===v):tr(_.tokens,v)||(o.suggestions??[]).some(e=>e===v)),b="number"==typeof v?m.find(e=>e.gpio===v)??null:null,(0,a.qy)`
    <div class="field" data-field-key=${(0,I.DN)(n)}>
      ${(0,I.Lx)(o,s,{path:n})}
      <!-- Deliberately not guard-locked: no manifest designates a pin via a
           substitution, so a \${var} landing on one is the user's own
           hand-authored setup, and this input edits the reference name, not
           the wiring the panel below guards. -->
      <input
        type="text"
        autocomplete="off"
        class=${u?"invalid":""}
        .value=${c}
        ?disabled=${h}
        @input=${e=>s.emitChange(p,e.target.value)}
      />
      ${(0,I.Nk)(c,s.substitutions,s.localize)}
      ${(0,I.FL)(p,s)}
      ${e5({entry:o,path:n,ctx:s,rawValue:d,boardPin:b,guarded:y&&!h})}
    </div>
  `}if(!i.board||0===i.board.pins.length)return(0,I.Mf)(e,"text",t,i);let c=(0,eN.E7)(function(e,t){let i=(0,eN.Sn)(e);if(void 0===i||!(0,f.Qd)(e))return e;let r=e[i];return"string"==typeof r?{...e,[i]:(0,O.rq)(r,t)}:(0,f.Qd)(r)&&"string"==typeof r.address?{...e,[i]:{...r,address:(0,O.rq)(r.address,t)}}:e}(r,i.substitutions));if("string"==typeof c||(0,eN.GV)(r)){let o="string"==typeof c?c:null,n=null!==o&&((e.suggestions??[]).some(e=>"string"==typeof e&&null===(0,eN.j8)(e)&&e===o)||tr(ti(i,t).tokens,o));return function(e,t,i,r,o,n){var s;let l,d,c,[p,u,h]=r?.split(":")??(s=o,l=(0,eN.Sn)(s)??"",d=s[l],c=(0,f.Qd)(d)?d.address:void 0,[l,"string"==typeof d?d:(0,O.zZ)(c)?`@${c}`:"",String(s.number??"")]),m=(0,eN.PE)(u),g=n&&!(0,I.U)(e,i);return(0,a.qy)`
    <div class="field" data-field-key=${(0,I.DN)(t)}>
      ${(0,I.Lx)(e,i,{path:t})}
      <input
        type="text"
        readonly
        .value=${""===u?i.localize("device.pin_on_expander_unresolved",{provider:p,channel:h}):null===m?i.localize("device.pin_on_expander",{provider:p,hub:u,channel:h}):i.localize("device.pin_on_expander_address",{provider:p,address:m,channel:h})}
      />
      ${(0,I.FL)(t,i)}
      ${e5({entry:e,path:t,ctx:i,rawValue:o,boardPin:null,guarded:g})}
    </div>
  `}(e,t,i,o,r,n)}let p=("number"==typeof c?c:null)??te(r,i.board.pins),u=i.board.esphome.platform,h=null!==p?(0,eN.m5)(p,u):(0,f.k4)(r)?String(r??""):"",m=null!==i.errorAt(t),g=null!=e.default_value?tt(e.default_value,i.board.pins):null,v=null!==g?i.board.pins.find(e=>e.gpio===g)?.label??(0,eN.m5)(g,u):"",_=i.board.pins,y=null!==p?i.board.pins.find(e=>e.gpio===p)??null:null,b=new Set((e.suggestions??[]).map(e=>tt(e,i.board.pins)).filter(e=>null!==e));if(b.size>0){let e=_.filter(e=>b.has(e.gpio));e.length>0&&(_=e)}y&&!_.some(e=>e.gpio===y.gpio)&&(_=[y,..._]);let w=(0,eI.zq)(i.yaml,i.fromLine,(0,eI.lz)(i.yaml,i.fromLine)),x=ti(i,t),$=x.lockedGpios,k=null!==p&&(x.gpios.has(p)||b.has(p));null!==p&&$.add(p);let z=(0,I.U)(e,i),C=k&&!z,q=C?{...e,locked:!0,locked_reason_key:"device.pin_wiring_guard_tooltip"}:e,S=(0,I.Gc)("pin-guard-tip",t),A=(0,f.Qd)(r);return(0,a.qy)`
    <div class="field" data-field-key=${(0,I.DN)(t)}>
      ${(0,I.Lx)(q,i,{path:t})}
      <!-- Keyed as the long form's number so the YAML cursor lands on the
           select itself (the whole-field fallback centers mid-panel once
           the wiring disclosure is open). Short form keeps the bare path:
           a number key would break the form-to-YAML pulse, which looks up
           a number line the YAML doesn't have. -->
      <wa-select
        data-no-value-sync
        data-field-key=${(0,I.DN)(A?[...t,"number"]:t)}
        id=${C?S:a.s6}
        class=${m?"invalid":""}
        placeholder=${v}
        ?disabled=${z||C}
        @change=${e=>{let r=e.target.value;A?i.emitChange([...t,"number"],r):i.emitChange(t,r)}}
      >
        ${function(e,t,i,r,o,n){let s=[],d=[],c=[];for(let o of e){let e=function(e,t,i,r,o){let a=(0,eN.m5)(e.gpio,o.board?.esphome.platform),n=e.label||a,s=e.occupied_by||"",d=i.get(e.gpio)||"",c=(t.pin_mode===l.l3.OUTPUT||t.pin_mode===l.l3.INPUT_OUTPUT)&&e.features.includes(l.k6.INPUT_ONLY),p=(t.pin_features??[]).every(t=>e.features.includes(t)),u=!1===e.available,h=u&&!r.has(e.gpio),m=!!(s||d),f=s?o.localize("device.pin_occupied_by",{name:s}):d?o.localize("device.pin_used_by",{name:d}):"",g=c?o.localize("device.pin_input_only"):"",v=e.notes||(u?o.localize("device.pin_unavailable"):""),_=[];return e.label&&e.label!==a&&_.push(a),f&&_.push(f),g&&_.push(g),v&&_.push(v),{optValue:a,primary:n,secondary:_.join(" • "),titleText:[f,g,v].filter(Boolean).join(" — "),warn:m||c,reserved:u,disabled:h,supported:p&&!c}}(o,t,i,r,n);(e.reserved?c:e.supported?s:d).push(e)}let p=s.length>0&&d.length>0,u=(t.pin_features??[]).map(e=>e.toUpperCase()).join(", "),h=(e,t)=>(0,a.qy)`${t?(0,a.qy)`<wa-divider class="pin-group-divider" aria-hidden="true"></wa-divider>`:a.s6} <small class="pin-group-label" aria-hidden="true">${e}</small>`;return(0,a.qy)`
    ${p&&u?h(n.localize("device.pin_group_supports",{features:u}),!1):a.s6}
    ${s.map(e=>to(e,o))}
    ${p?h(n.localize("device.pin_group_other"),!0):a.s6}
    ${d.map(e=>to(e,o))}
    ${c.length>0?h(n.localize("device.pin_group_reserved"),!0):a.s6}
    ${c.map(e=>to(e,o))}
  `}(_,e,w,$,h,i)}
      </wa-select>
      ${C?(0,a.qy)`<wa-tooltip for=${S}>
              ${i.localize("device.pin_wiring_guard_tooltip")}
            </wa-tooltip>`:a.s6}
      ${(0,I.FL)(t,i)}
      ${e5({entry:e,path:t,ctx:i,rawValue:r,boardPin:y,guarded:C})}
    </div>
  `}(e,t,i);case l.Hh.COLOR:let s;return s=i.getAt(t),(0,eZ.rf)(s)&&!(0,eH.fd)(String(s))?(0,I.JF)(e,t,i,s):(0,I.Mf)(e,"color",t,i);case l.Hh.MAC_ADDRESS:return(0,I.Mf)(e,"text",t,i);case l.Hh.LAMBDA:return ed(e,t,i);case l.Hh.JSON:return function(e,t,i){let r=i.getAt(t),o=r instanceof L.ho;if(!o){let o=(0,I.BO)(e,t,i,r);if(o)return o}let n=o?r.body:String(r??""),s=null!==i.errorAt(t);return(0,a.qy)`
    <div class="field" data-field-key=${(0,I.DN)(t)}>
      ${(0,I.Lx)(e,i,{path:t})}
      <textarea
        class="textarea-field ${s?"invalid":""}"
        rows="4"
        ?disabled=${(0,I.U)(e,i)}
        .value=${n}
        placeholder=${String(e.default_value??"")}
        @input=${e=>{let a=e.target.value;i.emitChange(t,o?L.ho.fromBodyText(a,r):a)}}
      ></textarea>
      ${(0,I.FL)(t,i)}
    </div>
  `}(e,t,i);case l.Hh.ICON:let d=i.getAt(t),c=(0,I.BO)(e,t,i,d);if(c)return c;let p=String(d??""),u=null!==i.errorAt(t);return(0,a.qy)`
    <div class="field" data-field-key=${(0,I.DN)(t)}>
      ${(0,I.Lx)(e,i,{path:t})}
      <esphome-mdi-icon-picker
        .value=${p}
        .invalid=${u}
        .disabled=${(0,I.U)(e,i)}
        .placeholder=${String(e.default_value??"Choose an icon…")}
        @change=${e=>i.emitChange(t,e.detail.value)}
      ></esphome-mdi-icon-picker>
      ${(0,I.FL)(t,i)}
    </div>
  `;case l.Hh.TRIGGER:return(0,a.qy)`<div class="field" data-field-key=${(0,I.DN)(t)}>
          ${(0,I.gt)(e,i)}
          <button
            type="button"
            class="edit-actions-button"
            ?disabled=${i.disabled}
            @click=${()=>this._emitEditActionField(t)}
          >
            ${i.localize("device.automation_action_field_edit")}
          </button>
        </div>`;case l.Hh.UNKNOWN:return(0,I.YJ)(e,t,i);default:return(0,I.Mf)(e,"text",t,i)}}_buildCtx(){var e,t,i,r;let o={localize:this._localize,disabled:this.disabled,yaml:this.yaml,substitutions:this._parseSubstitutions(this.yaml),fromLine:this.fromLine,sectionKey:this.sectionKey,deviceName:(0,u.k)(this._devices,this.configuration),board:this.board,pinRegistryModes:this._pinRegistryModes.value,requiredOnly:this.requiredOnly,showAdvanced:this.showAdvanced,presentComponents:this.presentComponents,reactiveConstraintPaths:this._constraintMemberPaths(this.entries,this.requiredGroups),entries:this.entries,nestedOpenSections:this._nestedOpenSections,getAt:e=>(0,f.O6)(this.values,e),errorAt:e=>this.errors.get(e.join("."))??null,emitChange:(e,t)=>this._emitChange(e,t),toggleNested:e=>this._toggleNested(e),seedNestedOpen:e=>this._seedNestedOpen(e),requestAddComponent:e=>this._requestAddComponent(e),resolveInterfaceProviders:e=>this._resolveInterfaceProviders(e),catalogById:()=>this._catalogIndex.byId(),isOptionsExpanded:e=>this._expandedOptionFields.has((0,I.DN)(e)),expandOptions:e=>{let t=(0,I.DN)(e);this._expandedOptionFields.has(t)||(this._expandedOptionFields.add(t),this.requestUpdate())},scopeValues:e=>this._scopeValues(e),filterRenderable:this._filterRenderable,requiredGroups:this.requiredGroups,...this._valueMemory.ctx,...(e=this,t=this._constraintClusters,i=this._expandedOptionFields,r=[...this._valueMemory.stores,this._nestedOpenSections,this._seededNestedOpen],{rowsMoved:(o,a)=>{let n,s,l,d=(n=`${o.join(".")}.`,e=>{if(!e.startsWith(n))return e;let t=e.slice(n.length),i=t.split(/[.:]/,1)[0];if(!(0,f.wr)(i))return e;let r=a(Number(i));return null===r?null:`${n}${r}${t.slice(i.length)}`});for(let e of(B(i,e=>{let t=(0,I.lt)(e),i=t?.[o.length];if(!t||void 0===i||!(0,f.wr)(i)||!o.every((e,i)=>t[i]===e))return e;let r=a(Number(i));return null===r?null:(0,I.DN)([...o,String(r),...t.slice(o.length+1)])}),r))B(e,d);(s=ep.get(e))&&B(s,d),(l=U.get(e))&&B(l,d),t.rekeyChoices(d)}}),getClusterChoice:e=>this._constraintClusters.getChoice(e),setClusterChoice:(e,t)=>this._constraintClusters.setChoice(e,t),getClusterStash:(e,t)=>this._constraintClusters.getStash(e,t),setClusterStash:(e,t,i)=>this._constraintClusters.setStash(e,t,i),clearClusterStash:(e,t)=>this._constraintClusters.clearStash(e,t),stashOwner:this,renderEntry:()=>a.s6};return o.renderEntry=(e,t)=>this._renderEntry(e,t,o),o}_scopeValues(e){let t=(0,f.O6)(this.values,e);return t&&"object"==typeof t&&!Array.isArray(t)?t:{}}_emitChange(e,t){this.dispatchEvent(new CustomEvent("value-change",{detail:{path:e,value:t},bubbles:!0,composed:!0}))}_emitEditActionField(e){this.dispatchEvent(new CustomEvent("edit-action-field",{detail:{path:e},bubbles:!0,composed:!0}))}_toggleNested(e){let t=new Set(this._nestedOpenSections);t.has(e)?t.delete(e):t.add(e),this._nestedOpenSections=t}openNested(e){if(this._nestedOpenSections.has(e))return;let t=new Set(this._nestedOpenSections);t.add(e),this._nestedOpenSections=t}_seedNestedOpen(e){this._seededNestedOpen.has(e)||(this._seededNestedOpen.add(e),this._nestedOpenSections.add(e))}_requestAddComponent(e){(0,y.r)(this,"request-add-component",{domain:e})}_resolveInterfaceProviders(e){if(!e)return[];let t=(0,C.Qk)(e);return t||(this._api&&(0,C.em)(this._api,e).catch(()=>{}),null)}constructor(...e){super(...e),this._localize=e=>e,this._devices=[],this._pinRegistryModes=new A(this,{getCached:$,subscribe:k,fetch:z},()=>this._api),this.entries=[],this.values={},this.requiredGroups=[],this.errors=new Map,this.board=null,this.disabled=!1,this.showAdvanced=!1,this.advancedSection=!1,this.forceAdvancedControl=!1,this.gateAdvanced=!1,this.advancedExtraCount=0,this.requiredOnly=!1,this.yaml="",this.sectionKey="",this.configuration="",this.presentComponents=new Set,this.valuesRead=0,this._nestedOpenSections=new Set,this._seededNestedOpen=new Set,this._expandedOptionFields=new Set,this._fieldScroll=new e_(this),this._fieldFocus=new ef(this),this._valueMemory=new eu(this),this._constraintClusters=new eh(this),this._catalogIndex=new M.C(this,()=>this._api),this._openAdvancedPlacement=new Map,this._filterRenderable=(e,t,i)=>(0,E.V5)(e,t,(0,E.xx)(this,{requiredGroups:i})),this._parseSubstitutions=(0,s.A)(O.Gr),this._constraintMemberPaths=(0,s.A)((e,t)=>(0,p.IT)(e,t))}}tE.styles=[I.M8,(0,a.AH)`
      /* "Show advanced settings" switch (advanced-section mode): sits at the
         basic/advanced boundary; flipping it on reveals the advanced fields
         rendered below it. */
      .advanced-toggle-row {
        display: flex;
        font-size: var(--wa-font-size-s);
      }

      .advanced-toggle-row wa-switch {
        font-weight: var(--wa-font-weight-semibold);
        color: var(--wa-color-text-quiet);
      }
    `],tM([(0,r.Fg)({context:d.$F,subscribe:!0}),(0,n.wk)()],tE.prototype,"_localize",void 0),tM([(0,r.Fg)({context:d.Ie,subscribe:!0}),(0,n.wk)()],tE.prototype,"_api",void 0),tM([(0,r.Fg)({context:d.xJ,subscribe:!0}),(0,n.wk)()],tE.prototype,"_devices",void 0),tM([(0,n.MZ)({attribute:!1})],tE.prototype,"entries",void 0),tM([(0,n.MZ)({attribute:!1})],tE.prototype,"values",void 0),tM([(0,n.MZ)({attribute:!1})],tE.prototype,"requiredGroups",void 0),tM([(0,n.MZ)({attribute:!1})],tE.prototype,"errors",void 0),tM([(0,n.MZ)({attribute:!1})],tE.prototype,"board",void 0),tM([(0,n.MZ)({type:Boolean})],tE.prototype,"disabled",void 0),tM([(0,n.MZ)({type:Boolean,attribute:"show-advanced"})],tE.prototype,"showAdvanced",void 0),tM([(0,n.MZ)({type:Boolean,attribute:"advanced-section"})],tE.prototype,"advancedSection",void 0),tM([(0,n.MZ)({type:Boolean,attribute:"force-advanced-control"})],tE.prototype,"forceAdvancedControl",void 0),tM([(0,n.MZ)({type:Boolean,attribute:"gate-advanced"})],tE.prototype,"gateAdvanced",void 0),tM([(0,n.MZ)({type:Number,attribute:"advanced-extra-count"})],tE.prototype,"advancedExtraCount",void 0),tM([(0,n.MZ)({type:Boolean,attribute:"required-only"})],tE.prototype,"requiredOnly",void 0),tM([(0,n.MZ)()],tE.prototype,"yaml",void 0),tM([(0,n.MZ)({type:Number,attribute:"from-line"})],tE.prototype,"fromLine",void 0),tM([(0,n.MZ)({attribute:"section-key"})],tE.prototype,"sectionKey",void 0),tM([(0,n.MZ)()],tE.prototype,"configuration",void 0),tM([(0,n.MZ)({attribute:!1})],tE.prototype,"presentComponents",void 0),tM([(0,r.Fg)({context:d.km,subscribe:!0}),(0,n.wk)()],tE.prototype,"valuesRead",void 0),tM([(0,n.MZ)({attribute:!1})],tE.prototype,"focusFieldPath",void 0),tM([(0,n.wk)()],tE.prototype,"_nestedOpenSections",void 0),tM([(0,n.EM)("esphome-config-entry-form")],tE)},1379(e,t,i){var r=i(4008),o=i(565),a=i(1734),n=i(8175),s=i(8851),l=i(2561);let d=new Set(["name"]);function c(e,t){return(0,s.$z)(t)?e.required_groups??[]:[]}function p(e,t,i){let r=c(t,i),o=r.length?r:void 0;return o||e.requiredGroups?{...e,requiredGroups:o}:e}function u(e,t,i){if(e.type!==r.Hh.NESTED||e.multi_value)return!1;let o=t[e.key];return!(("string"==typeof o||"number"==typeof o||"boolean"==typeof o)&&(0,s.$z)(o))&&0===h(e.config_entries??[],(0,n.qY)(o),p(i,e,o)).length&&!(0,l.p_)(e,i)}function h(e,t,i){let n=[],s=i.requiredGroups?(0,l.Vn)(i.requiredGroups,e):null;for(let l of e)if((0,o.VP)(l,t,i.presentComponents,i.targetPlatform,i.rootValues,e)&&!(!i.showAdvanced&&(0,a.w)(l,t))){if(l.type===r.Hh.NESTED){if(u(l,t,i))continue}else if(i.requiredOnly&&!l.required&&!d.has(l.key)&&!s?.has(l.key))continue;n.push(l)}return n}i.d(t,{},{Hh:function(e){return e===r.Hh.NESTED||e===r.Hh.MAP||e===r.Hh.DIVIDER||e===r.Hh.LABEL||e===r.Hh.ALERT},Ic:c,TU:function(e,t,i,r){return void 0!==t[e.key]||(0,o.VP)(e,t,i.presentComponents,i.targetPlatform,i.rootValues,r)},V5:h,tX:function e(t,i,o,a=[],s=new Set){for(let l of h(t,i,o)){if(l.type===r.Hh.NESTED){let t=l.config_entries??[];l.multi_value?(0,n.ly)(i[l.key]).forEach((i,r)=>{e(t,i,p(o,l,void 0),[...a,l.key,String(r)],s)}):e(t,(0,n.qY)(i[l.key]),p(o,l,i[l.key]),[...a,l.key],s),s.add([...a,l.key].join("."));continue}l.multi_value&&Array.isArray(i[l.key])&&i[l.key].forEach((e,t)=>{s.add([...a,l.key,String(t)].join("."))}),s.add([...a,l.key].join("."))}return s},xx:function(e,t={}){var i;let r,o={requiredOnly:e.requiredOnly,showAdvanced:e.showAdvanced,presentComponents:e.presentComponents,targetPlatform:e.board?.esphome.platform??null,rootValues:e.values,...t};return i=o.rootValues,o.rootValues=(r=e.board?.esphome)&&e.sectionKey===r.platform&&null!=r.variant?{variant:r.variant,...i}:i,o},z0:u})},2564(e,t,i){i.d(t,{BT:()=>D,U:()=>M,DN:()=>E,M8:()=>O,I4:()=>H,gt:()=>L,lt:()=>P,cu:()=>G,FL:()=>j,tj:()=>T,wm:()=>F,Lx:()=>N,Mf:()=>U,Nk:()=>R,jT:()=>Z,JF:()=>K,BO:()=>B,YJ:()=>V,HL:()=>u.H,Gc:()=>I});var r=i(289),o=i(5077),a=i(1262),n=i(1480),s=i(5660),l=i(3140),d=i(615),c=i(2943),p=i(7181),u=i(9508),h=i(6910),m=i(8175),f=i(9582),g=i(1093),v=i(2748),_=i(7967),y=i(355),b=i(5413),w=i(9470),x=i(8851);let $=(0,o.AH)`
  /* Per-entry render-error tile. A renderer that throws (or
     receives a malformed entry shape) would otherwise leave a
     silent gap in the form — the user can't tell whether their
     data is gone or the form just doesn't show that field. The
     tile makes the failure visible with the entry's key/type
     and the error message so a user can report the problem
     instead of silently losing their work. */
  .render-error {
    display: flex;
    gap: var(--wa-space-s);
    align-items: flex-start;
    padding: var(--wa-space-s);
    border: 1px solid var(--wa-color-danger-fill-loud, currentColor);
    border-radius: var(--wa-border-radius-m);
    background: var(--wa-color-danger-fill-quiet, transparent);
    color: var(--wa-color-danger-on-quiet, currentColor);
  }
  .render-error wa-icon {
    flex-shrink: 0;
    margin-top: 2px;
  }
  .render-error > div {
    display: flex;
    flex-direction: column;
    gap: var(--wa-space-2xs);
    min-width: 0;
  }
  .render-error-key {
    font-family: ui-monospace, "SF Mono", Menlo, Consolas, monospace;
    font-size: var(--wa-font-size-xs);
    opacity: 0.85;
  }
  .render-error-message {
    margin: 0;
    font-family: ui-monospace, "SF Mono", Menlo, Consolas, monospace;
    font-size: var(--wa-font-size-xs);
    white-space: pre-wrap;
    word-break: break-word;
  }

  .textarea-field {
    font-family: ui-monospace, "SF Mono", Menlo, Consolas, monospace;
    font-size: var(--wa-font-size-xs);
    padding: var(--wa-space-s);
    border-radius: var(--wa-border-radius-m);
    border: var(--wa-border-width-s) solid var(--wa-color-surface-border);
    background: var(--wa-color-surface-default);
    color: var(--wa-color-text-normal);
    resize: vertical;
    min-height: 80px;
  }

  .textarea-field.invalid {
    border-color: var(--esphome-error);
  }

  /* ─── Pin selector option layout ─────────────────────────── */
  .pin-option-stack {
    display: inline-flex;
    flex-direction: column;
    gap: 1px;
    line-height: 1.25;
  }

  .pin-option-primary {
    font-size: var(--wa-font-size-s);
    font-weight: var(--wa-font-weight-semibold);
    color: var(--wa-color-text-normal);
    display: inline-flex;
    align-items: center;
    gap: 4px;
  }

  .pin-option-secondary {
    font-size: var(--wa-font-size-2xs);
    color: var(--wa-color-text-quiet);
    font-style: italic;
  }

  .pin-option[disabled] .pin-option-primary,
  .pin-option[disabled] .pin-option-secondary {
    color: var(--wa-color-text-quiet);
  }

  .pin-warn-icon {
    color: var(--esphome-warning, #d97706);
    font-size: 14px;
    flex-shrink: 0;
  }

  .pin-option--warn .pin-option-secondary {
    color: var(--esphome-warning, #d97706);
    font-style: normal;
  }

  /* Section labels for the Recommended / Other pins groups in the GPIO
     picker (issue #1012). Presentational only — wa-select skips
     non-option children for selection / keyboard nav. */
  .pin-group-label {
    display: block;
    padding: var(--wa-space-2xs) var(--wa-space-s) 0;
    font-size: var(--wa-font-size-2xs);
    font-weight: var(--wa-font-weight-semibold);
    text-transform: uppercase;
    letter-spacing: 0.04em;
    color: var(--wa-color-text-quiet);
  }

  .pin-group-divider {
    margin: var(--wa-space-2xs) 0;
  }

  /* ─── Pin "Advanced" disclosure (long-form fields) ──────── */
  /* Compact toggle that opens the long-form pin fields (mode
     flags, inverted) attached by the catalog's
     _pin_long_form_extras helper. Visually subordinate to the
     primary GPIO picker — the user has to opt in to the
     advanced fields per pin. */
  .pin-advanced {
    margin-top: var(--wa-space-2xs);
  }

  /* Keep the toggle's original vertical hit area (the shared base is flush). */
  .pin-advanced .disclosure-toggle {
    padding: 2px 0;
  }

  /* The shared disclosure renders the quiet toggle + panel; the bordered indent
     rail for the long-form fields is pin-specific, scoped to this disclosure's
     panel so it overrides the shared margin-only default. */
  .pin-advanced .disclosure-panel {
    margin-top: var(--wa-space-xs);
    padding-left: var(--wa-space-s);
    border-left: 2px solid var(--wa-color-surface-border);
    display: flex;
    flex-direction: column;
    gap: var(--wa-space-s);
  }

  /* ─── Pin wiring presets ─────────────────────────────────── */
  .pin-wiring-banner {
    margin: 0;
  }

  .pin-wiring-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(190px, 1fr));
    gap: var(--wa-space-xs);
  }

  .pin-wiring-card {
    display: flex;
    flex-direction: column;
    gap: 2px;
    padding: var(--wa-space-xs) var(--wa-space-s);
    border: var(--wa-border-width-s) solid var(--wa-color-surface-border);
    border-radius: var(--wa-border-radius-m);
    background: none;
    text-align: left;
    cursor: pointer;
    font: inherit;
    color: var(--wa-color-text-normal);
  }

  .pin-wiring-card:hover:not([aria-disabled="true"]) {
    border-color: var(--wa-color-brand-border-loud);
  }

  .pin-wiring-card--selected {
    border-color: var(--wa-color-brand-border-loud);
    box-shadow: inset 0 0 0 1px var(--wa-color-brand-border-loud);
  }

  /* aria-disabled, not native disabled: the card stays hoverable (the
     guard tooltip must show) and reachable by keyboard/AT. */
  .pin-wiring-card[aria-disabled="true"] {
    opacity: 0.6;
    cursor: default;
  }

  .pin-wiring-card-title {
    display: flex;
    align-items: center;
    gap: var(--wa-space-2xs);
    font-size: var(--wa-font-size-s);
    font-weight: var(--wa-font-weight-semibold);
  }

  .pin-wiring-badge {
    font-size: var(--wa-font-size-2xs);
    font-weight: var(--wa-font-weight-normal);
    padding: 0 var(--wa-space-2xs);
    border-radius: var(--wa-border-radius-s);
    background: var(--wa-color-brand-fill-quiet);
    color: var(--wa-color-brand-text-quiet);
  }

  .pin-wiring-card-desc {
    font-size: var(--wa-font-size-2xs);
    color: var(--wa-color-text-quiet);
  }

  .pin-wiring-card-desc--reason {
    color: var(--esphome-warning, #d97706);
  }

  /* What the preset writes, in mode-flag vocabulary — the quick read
     for users who already know what a pull-up is. */
  .pin-wiring-card-tech {
    font-family: var(--wa-font-family-code);
    font-size: var(--wa-font-size-2xs);
    color: var(--wa-color-text-quiet);
  }

  .pin-wiring-diagram {
    height: 30px;
    align-self: flex-start;
    color: var(--wa-color-text-quiet);
  }

  /* The schematic SVGs ship as asset files and are applied as a mask so
     the drawing takes the theme's text color in light and dark mode. */
  .pin-wiring-diagram--mask {
    width: 140px;
    background-color: var(--wa-color-text-quiet);
    -webkit-mask-repeat: no-repeat;
    -webkit-mask-position: left center;
    -webkit-mask-size: contain;
    mask-repeat: no-repeat;
    mask-position: left center;
    mask-size: contain;
  }

  .pin-wiring-diagram--icon {
    display: flex;
    align-items: center;
    font-size: 22px;
  }

  .pin-wiring-custom {
    display: flex;
    flex-direction: column;
    gap: var(--wa-space-s);
  }

  .pin-wiring-row {
    display: flex;
    flex-direction: column;
    gap: var(--wa-space-2xs);
  }

  .pin-wiring-radios wa-radio {
    font-size: var(--wa-font-size-s);
  }

  /* wa-radio's checked dot is "fill: currentColor", and its
     ":host(:state(checked)) .control { color: ... }" rule ties on specificity
     with the default "color: transparent" — the attribute selector wins the
     tie, so the dot renders invisible. One generic rule for every form
     radio group (constraint clusters, pin wiring). */
  wa-radio[aria-checked="true"]::part(control) {
    color: var(--wa-form-control-activated-color) !important;
  }

  /* Board-preset wiring guard: the panel is view-only; changes go through the YAML. */
  .pin-wiring-guard {
    display: flex;
    align-items: center;
    gap: var(--wa-space-s);
    padding: var(--wa-space-xs) var(--wa-space-s);
    border: var(--wa-border-width-s) solid var(--wa-color-surface-border);
    border-radius: var(--wa-border-radius-m);
  }

  .pin-wiring-guard > wa-icon {
    flex-shrink: 0;
    color: var(--wa-color-text-quiet);
  }

  .pin-wiring-guard-text {
    flex: 1;
    min-width: 0;
  }

  .pin-wiring-guard-text .field-description {
    margin: 0;
  }

  /* ─── ID reference picker option layout ──────────────────── */
  .id-option-stack {
    display: inline-flex;
    flex-direction: column;
    gap: 1px;
    line-height: 1.25;
  }

  /* Visually distinguish the "Add new …" entry at the bottom of
     the dropdown — same pattern as Home Assistant's entity
     pickers. Coloured to read as an action, not a value. */
  .id-option-add {
    border-top: var(--wa-border-width-s) solid var(--wa-color-surface-border);
    margin-top: var(--wa-space-2xs);
  }

  .id-option-add--solo {
    border-top: none;
    margin-top: 0;
  }

  .id-option-primary-add {
    color: var(--esphome-primary);
    font-weight: var(--wa-font-weight-bold);
  }

  .id-option-primary-add wa-icon {
    font-size: 14px;
  }

  .id-option-primary {
    font-size: var(--wa-font-size-s);
    font-weight: var(--wa-font-weight-semibold);
    color: var(--wa-color-text-normal);
    display: inline-flex;
    align-items: center;
    gap: 4px;
  }

  .id-option-secondary {
    font-size: var(--wa-font-size-2xs);
    color: var(--wa-color-text-quiet);
    font-style: italic;
  }

  .alert-entry {
    padding: var(--wa-space-s) var(--wa-space-m);
    background: var(--wa-color-surface-lowered);
    border-radius: var(--wa-border-radius-m);
    font-size: var(--wa-font-size-xs);
    color: var(--wa-color-text-quiet);
    line-height: 1.5;
  }

  .label-entry {
    font-size: var(--wa-font-size-xs);
    color: var(--wa-color-text-subtle);
    font-style: italic;
  }

  .switch-field {
    display: grid;
    grid-template-columns: 1fr auto;
    column-gap: var(--wa-space-m);
    row-gap: var(--wa-space-2xs);
    align-items: center;
  }

  .switch-field .field-info {
    grid-column: 1;
    grid-row: 1 / span 2;
    display: flex;
    flex-direction: column;
    gap: 2px;
  }

  .switch-field > .help-button {
    grid-column: 2;
    grid-row: 1;
    margin-left: 0;
    align-self: start;
  }

  .switch-field > wa-switch {
    grid-column: 2;
    grid-row: 2;
    justify-self: end;
  }

  .switch-field:not(:has(> .help-button)) > wa-switch {
    grid-row: 1 / span 2;
  }

  wa-select {
    width: 100%;
  }

  .float-with-unit-inputs {
    display: flex;
    align-items: center;
    gap: var(--wa-space-s);
  }

  .float-with-unit-inputs > input[type="number"] {
    flex: 1 1 auto;
    min-width: 0;
  }

  .float-with-unit-inputs > wa-select {
    flex: 0 0 auto;
    width: auto;
    min-width: 6rem;
  }

  /* Time-period field: numeric input + unit picker. Same layout
     as float_with_unit so the eye reads them as the same kind of
     compound control. */
  .time-period-inputs {
    display: flex;
    align-items: center;
    gap: var(--wa-space-s);
  }

  .time-period-inputs > input {
    flex: 1 1 auto;
    min-width: 0;
  }

  .time-period-inputs > wa-select {
    flex: 0 0 auto;
    width: auto;
    min-width: 6rem;
  }

  .float-with-unit-suffix {
    flex: 0 0 auto;
    color: var(--wa-color-text-subtle);
    font-size: var(--wa-font-size-s);
  }

  /* Templatable field wrapper — column holding the literal/lambda tab
     strip (styled by literalLambdaToggleStyles) above the active
     body. */
  .templatable-field {
    display: flex;
    flex-direction: column;
    gap: var(--wa-space-2xs);
  }

  /* TRIGGER (action-list) field — a button that opens the automation
     editor for the field's bare action list (cover open_action, …),
     since the actions can't be edited inline as a single value. */
  .edit-actions-button {
    appearance: none;
    display: inline-flex;
    align-items: center;
    gap: var(--wa-space-2xs);
    padding: var(--wa-space-2xs) var(--wa-space-s);
    border: 1px solid var(--wa-color-surface-border);
    border-radius: var(--wa-border-radius-m);
    background: var(--wa-color-surface-raised, transparent);
    color: var(--wa-color-text-normal);
    font-family: inherit;
    font-size: var(--wa-font-size-s);
    cursor: pointer;
    transition: background 0.12s;
  }

  .edit-actions-button:hover:not(:disabled) {
    background: var(--wa-color-surface-lowered);
  }

  .edit-actions-button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
`,k=(0,o.AH)`
  :host {
    display: flex;
    flex-direction: column;
    gap: var(--wa-space-m);
  }

  .field {
    display: flex;
    flex-direction: column;
    gap: var(--wa-space-2xs);
    border-radius: var(--wa-border-radius-m);
  }

  .field-label {
    font-size: var(--wa-font-size-s);
    font-weight: var(--wa-font-weight-semibold);
    color: var(--wa-color-text-normal);
    display: flex;
    align-items: center;
    gap: var(--wa-space-2xs);
  }

  .field-label .required {
    color: var(--esphome-error);
  }

  /* Indicator on featured-component fields the board has pinned to a
     fixed value. Sits next to the help-link icon. */
  .field-label .lock-icon {
    font-size: 13px;
    color: var(--wa-color-text-quiet);
  }

  .field-error {
    color: var(--esphome-error);
    font-size: var(--wa-font-size-2xs);
    margin-top: var(--wa-space-2xs);
  }

  .field-warning {
    color: var(--esphome-warning, #d97706);
    font-size: var(--wa-font-size-2xs);
    margin-top: var(--wa-space-2xs);
  }

  .field-description {
    font-size: var(--wa-font-size-2xs);
    color: var(--wa-color-text-quiet);
    margin: 0;
  }

  .field-description + input,
  .field-description + textarea,
  .field-description + wa-select,
  /* Secret-eligible fields wrap the control in .field-input-row, or replace
     it with the picker in secret mode — keep the same post-description gap. */
  .field-description + .field-input-row,
  .field-description + esphome-secret-picker {
    margin-top: 8px;
  }

  /* Stacks a string/password input above its inline secret picker (only
     emitted for secret-eligible fields with a literal value). Stacked, not
     side-by-side, so the input keeps full width — a side-by-side picker
     squeezes the input and its value collides with the password reveal eye. */
  .field-input-row {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    gap: var(--wa-space-2xs);
  }

  .field-input-row > input,
  .field-input-row > esphome-password-input {
    align-self: stretch;
    min-width: 0;
  }

  /* Hint shown below a string/password input when the value is a
     !secret reference — clarifies that the field points into
     secrets.yaml instead of holding a literal value. */
  /* The .substitution-note chip styles live in substitution-note.styles.js
     (pulled into fieldRendererStyles) so the automation editor can share
     them; only .secret-note is here. */
  .secret-note {
    display: inline-flex;
    align-items: center;
    gap: var(--wa-space-2xs);
    margin-top: var(--wa-space-2xs);
    font-size: var(--wa-font-size-2xs);
    color: var(--wa-color-text-quiet);
  }

  .secret-note wa-icon {
    font-size: 14px;
    color: var(--esphome-primary);
  }

  .secret-note code {
    font-family: ui-monospace, "SF Mono", Menlo, Consolas, monospace;
    font-size: var(--wa-font-size-2xs);
    padding: 1px 4px;
    border-radius: var(--wa-border-radius-s);
    background: var(--wa-color-surface-lowered);
    color: var(--wa-color-text-normal);
  }

  .help-button {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    background: none;
    border: none;
    padding: 0;
    cursor: pointer;
    color: var(--wa-color-text-quiet);
    font-size: 16px;
    transition: color 0.12s;
    margin-left: auto;
  }

  .help-button:hover {
    color: var(--esphome-primary);
  }

  /* Inline "generate a key" action stacked under the API encryption-key
     input — a quiet link-style button, not a heavy form control. */
  .generate-key {
    display: inline-flex;
    align-items: center;
    gap: var(--wa-space-2xs);
    align-self: flex-start;
    background: none;
    border: none;
    padding: 0;
    cursor: pointer;
    color: var(--esphome-primary);
    font-size: var(--wa-font-size-2xs);
    transition: color 0.12s;
  }

  .generate-key:hover {
    text-decoration: underline;
  }

  .generate-key wa-icon {
    font-size: 14px;
  }

  /* ─── Nested group ──────────────────────────────────────── */
  .nested-group {
    display: flex;
    flex-direction: column;
    gap: var(--wa-space-s);
    padding: var(--wa-space-s) var(--wa-space-m);
    background: var(--wa-color-surface-lowered);
    border: var(--wa-border-width-s) solid var(--wa-color-surface-border);
    border-radius: var(--wa-border-radius-m);
  }

  .nested-header {
    display: flex;
    align-items: center;
    gap: var(--wa-space-2xs);
  }

  .nested-enable {
    flex-shrink: 0;
  }

  .nested-toggle {
    display: flex;
    flex: 1;
    min-width: 0;
    align-items: center;
    gap: var(--wa-space-2xs);
    background: none;
    border: none;
    padding: 0;
    font-family: inherit;
    font-size: var(--wa-font-size-s);
    font-weight: var(--wa-font-weight-bold);
    color: var(--wa-color-text-normal);
    cursor: pointer;
    text-align: left;
  }

  .nested-desc {
    font-size: var(--wa-font-size-2xs);
    color: var(--wa-color-text-quiet);
    margin: 0;
  }

  .nested-toggle:hover {
    color: var(--esphome-primary);
  }

  /* A block with no field to expand: a title, not a control. */
  .nested-toggle--static,
  .nested-toggle--static:hover {
    color: var(--wa-color-text-normal);
    cursor: default;
  }

  /* Hold the chevron's slot so the title does not shift when fields appear. */
  .nested-toggle--static {
    padding-left: calc(18px + var(--wa-space-2xs));
  }

  .nested-toggle wa-icon {
    font-size: 18px;
  }

  .nested-title {
    flex: 1;
    min-width: 0;
    overflow-wrap: anywhere;
  }

  .nested-platform {
    font-size: var(--wa-font-size-2xs);
    font-weight: var(--wa-font-weight-normal);
    color: var(--wa-color-text-quiet);
    background: var(--wa-color-surface-default);
    border: var(--wa-border-width-s) solid var(--wa-color-surface-border);
    border-radius: var(--wa-border-radius-s);
    padding: 1px 6px;
    margin-left: var(--wa-space-xs);
  }

  .nested-fields {
    display: flex;
    flex-direction: column;
    gap: var(--wa-space-m);
    padding-top: var(--wa-space-xs);
  }

  /* ─── nested list (repeatable nested mapping) ───────────── */
  .nested-list {
    display: flex;
    flex-direction: column;
    gap: var(--wa-space-s);
  }

  .nested-list-item {
    display: flex;
    flex-direction: column;
    gap: var(--wa-space-xs);
    padding: var(--wa-space-s) var(--wa-space-m);
    background: var(--wa-color-surface-lowered);
    border: var(--wa-border-width-s) solid var(--wa-color-surface-border);
    border-radius: var(--wa-border-radius-m);
  }

  .nested-list-item-header {
    display: flex;
    align-items: center;
    gap: var(--wa-space-2xs);
  }

  .nested-list-item-title {
    flex: 1;
    min-width: 0;
    overflow-wrap: anywhere;
    font-size: var(--wa-font-size-s);
    font-weight: var(--wa-font-weight-bold);
    color: var(--wa-color-text-normal);
  }

  /* ─── multi-value rows ──────────────────────────────────── */
  .multi-row {
    display: flex;
    align-items: center;
    gap: var(--wa-space-2xs);
  }

  .multi-row .multi-input {
    flex: 1;
    font-family: inherit;
    font-size: var(--wa-font-size-s);
    padding: 6px 12px;
    border-radius: var(--wa-border-radius-m);
    border: var(--wa-border-width-s) solid var(--wa-color-surface-border);
    background: var(--wa-color-surface-default);
    color: var(--wa-color-text-normal);
    outline: none;
    box-sizing: border-box;
    transition:
      border-color 0.12s,
      box-shadow 0.12s;
  }

  .multi-row .multi-input:focus {
    border-color: var(--esphome-primary);
    box-shadow: var(--esphome-focus-ring);
  }

  .multi-row .multi-input.invalid {
    border-color: var(--esphome-error);
  }

  .multi-row .multi-input:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }

  /* Stacks a row's input above its substitution hint while the remove
     button stays beside the input column. */
  .multi-row .multi-value-cell {
    flex: 1;
    min-width: 0;
    display: flex;
    flex-direction: column;
  }

  .combobox-input {
    font-family: inherit;
    font-size: var(--wa-font-size-s);
    padding: 6px 12px;
    border-radius: var(--wa-border-radius-m);
    border: var(--wa-border-width-s) solid var(--wa-color-surface-border);
    background: var(--wa-color-surface-default);
    color: var(--wa-color-text-normal);
    outline: none;
    box-sizing: border-box;
    transition:
      border-color 0.12s,
      box-shadow 0.12s;
  }

  .combobox-input:focus {
    border-color: var(--esphome-primary);
    box-shadow: var(--esphome-focus-ring);
  }

  .combobox-input.invalid {
    border-color: var(--esphome-error);
  }

  .combobox-input:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }

  .multi-btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 4px;
    padding: 4px 10px;
    background: transparent;
    border: var(--wa-border-width-s) solid var(--wa-color-surface-border);
    border-radius: var(--wa-border-radius-m);
    color: var(--wa-color-text-quiet);
    font-family: inherit;
    font-size: var(--wa-font-size-xs);
    cursor: pointer;
    transition:
      background 0.12s,
      border-color 0.12s,
      color 0.12s;
  }

  .multi-btn:hover {
    background: var(--wa-color-surface-lowered);
    color: var(--wa-color-text-normal);
  }

  .multi-btn svg {
    font-size: 14px;
  }

  .multi-add {
    align-self: flex-start;
    margin-top: var(--wa-space-2xs);
  }

  /* ─── Map (key/value) rows ──────────────────────────────── */
  .map-row {
    display: flex;
    align-items: flex-start;
    gap: var(--wa-space-2xs);
  }

  .map-row .map-key-input {
    flex: 1;
    min-width: 0;
  }

  .map-row .map-value {
    flex: 1.5;
    min-width: 0;
  }

  /* Inside a map row the value's label and description are
     redundant (the map itself has those at the top) — suppress
     them so each row stays compact. A templatable value (Value / λ
     Lambda toggle) nests its field one level deeper under
     .templatable-field, so match that too or the label re-appears
     and offsets the input. */
  .map-row .map-value > .field > label,
  .map-row .map-value > .field > p.field-description,
  .map-row .map-value > .templatable-field > .field > label,
  .map-row .map-value > .templatable-field > .field > p.field-description {
    display: none;
  }

  .map-row .map-value > .field,
  .map-row .map-value > .templatable-field > .field {
    gap: 0;
  }

  /* A templatable value stacks its Value / λ Lambda toggle above the input
     (a full-width field column). In a compact map row that drops the input
     below the toggle and out of line with the key; lay the toggle and input
     on one row instead so the value aligns with the key input. */
  .map-row .map-value > .templatable-field {
    flex-direction: row;
    align-items: center;
    gap: var(--wa-space-2xs);
  }

  .map-row .map-value > .templatable-field > .field {
    flex: 1;
    min-width: 0;
  }

  /* "Complex value — edit in YAML" placeholder for map rows whose
     value isn't a primitive (lists / dicts can't round-trip through
     a single text input). Quiet, italic, padded to vertically
     match the size of a wa-input so the row alignment is preserved. */
  .map-row .map-value-yaml-only {
    margin: 0;
    padding: var(--wa-space-2xs) var(--wa-space-s);
    color: var(--wa-color-text-quiet);
    font-style: italic;
    font-size: var(--wa-font-size-s);
    line-height: var(--wa-form-control-line-height, 1.5);
  }
`;var z=i(1379);let C=(0,o.AH)`
  /* Reactive prompt for an unsatisfied cross-field constraint group
     (e.g. "set exactly one of: chipset, manual timings"). Layers the
     icon+text row and spacing onto the shared .warning-banner shape;
     shown only while the group is unmet, so a satisfied group adds no
     noise. */
  .constraint-banner {
    display: flex;
    gap: var(--wa-space-s);
    align-items: center;
    margin-bottom: var(--wa-space-m);
  }
  .constraint-banner wa-icon {
    flex-shrink: 0;
  }

  /* Header of a folded either/or constraint cluster (the .nested-group box):
     a muted caption of the rule, warm-toned while the rule is unmet. */
  .constraint-cluster-header {
    display: flex;
    gap: var(--wa-space-s);
    align-items: center;
    font-size: var(--wa-font-size-s);
    color: var(--wa-color-text-quiet);
  }
  .constraint-cluster-header.unsatisfied {
    color: var(--wa-color-warning-on-quiet, currentColor);
  }
  .constraint-cluster-header wa-icon {
    flex-shrink: 0;
  }

  /* Radio chooser for an exactly-one cluster: small gap above the selected
     alternative's fields so the radios read as the box's control. */
  .constraint-cluster-radios {
    margin-bottom: var(--wa-space-2xs);
  }

  /* The checked-dot visibility fix lives once in
     config-entry-form-extra.styles.ts as a generic wa-radio rule. */
`;var q=i(901),S=i(4267),A=i(8144);let O=[l.G9,s.z9,a.X,k,$,n.a,q.N,C,S.h,A.s];function M(e,t){return t.disabled||!0===e.locked}(0,g.C)({"alert-circle-outline":r.mdiAlertCircleOutline,"auto-fix":r.mdiAutoFix,"code-braces":r.mdiCodeBraces,"key-variant":r.mdiKeyVariant,"lock-outline":r.mdiLockOutline});let E=e=>JSON.stringify(e),I=(e,t)=>`${e}-${encodeURIComponent(E(t))}`,P=e=>{try{let t=JSON.parse(e);if(Array.isArray(t))return t.map(String)}catch{}return e?e.split("."):[]};function R(e,t,i){if(!(0,b.RB)(e))return o.s6;let r=(0,b.rq)(e,t);if((0,b.RB)(r)){let e=i("device.substitution_unresolved_hint");return(0,o.qy)`<span
      class="substitution-note substitution-note--external"
      role="note"
      aria-label=${e}
      title=${e}
    >
      <wa-icon library="mdi" name="code-braces"></wa-icon>
      <wa-icon
        class="substitution-warn"
        library="mdi"
        name="alert-circle-outline"
      ></wa-icon>
      <span>${i("device.substitution_unresolved")}</span>
    </span>`}let a=i("device.substitution_resolves_to");return(0,o.qy)`<span
    class="substitution-note"
    role="note"
    aria-label=${`${a}: ${r}`}
    title=${a}
  >
    <wa-icon library="mdi" name="code-braces"></wa-icon>
    <code>${r}</code>
  </span>`}function L(e,t){return(0,u.H)(e,t.localize)}function F(e,t){return e.help_link?(0,o.qy)`<a
    class="help-button"
    href=${e.help_link}
    target="_blank"
    rel="noreferrer"
    title=${t.localize("device.docs")}
  >
    <wa-icon library="mdi" name="open-in-new"></wa-icon>
  </a>`:o.s6}function N(e,t,i){var r,a,n;let s,l,d,{includeHelpLink:c=!0,path:p}=i;return(0,o.qy)`
    <label class="field-label">
      ${L(e,t)}
      ${e.required?(0,o.qy)`<span class="required">*</span>`:o.s6}
      ${e.locked?(r=e,a=t,n=p,s=a.localize(r.locked_reason_key??"device.field_locked_by_board"),l=I("lock-tip",n),(0,o.qy)`<wa-icon
      id=${l}
      class="lock-icon"
      library="mdi"
      name="lock-outline"
      tabindex="0"
      role="img"
      aria-label=${s}
    ></wa-icon>
    <wa-tooltip for=${l}>${s}</wa-tooltip>`):o.s6}
      ${c&&e.help_link?F(e,t):o.s6}
    </label>
    ${(d=D(e,p,t))?(0,o.qy)`<p class="field-description">${(0,h.Gc)(d)}</p>`:o.s6}
  `}function D(e,t,i){let r=e.description??"";return i.reactiveConstraintPaths.has((0,p.Wy)(t))&&(1===t.length||(0,x.$z)(i.getAt(t.slice(0,-1))))?(0,p.PX)(r):r}function j(e,t){let i=t.errorAt(e);return(0,v.O)(i?t.localize(i.code,i.params):void 0)}function T(e,t,i,r,a=o.s6){return(0,o.qy)`
    <div class="field" data-field-key=${E(t)}>
      ${N(e,i,{path:t})} ${r} ${a}
      ${j(t,i)}
    </div>
  `}function B(e,t,i,r){return(0,m.k4)(r)?null:V(e,t,i)}function K(e,t,i,r){return"string"==typeof r?U(e,"text",t,i):V(e,t,i)}function V(e,t,i){return(0,o.qy)`
    <div class="field" data-field-key=${E(t)}>
      ${N(e,i,{path:t})}
      <p class="field-description">${i.localize("device.value_yaml_only")}</p>
      ${j(t,i)}
    </div>
  `}function U(e,t,i,r){let a,n=r.getAt(i),s=B(e,i,r,n);if(s)return s;let l=String(n??""),p=null!==r.errorAt(i),u=String(e.default_value??""),h=M(e,r),m="password"===t||(0,_.Un)(r.sectionKey,e.key),f=(0,y.D)(l),g=m&&null!==f,v=m?(0,_.WA)(r.sectionKey,e.key,r.deviceName??"","password"===t,i):[],x=m?(0,o.qy)`<esphome-secret-picker
        ?full=${g}
        .disabled=${h}
        .fieldLabel=${L(e,r)}
        .selectedKey=${f??""}
        .value=${l}
        .deviceName=${r.deviceName??""}
        .recommendedKeys=${v}
        @secret-selected=${e=>r.emitChange(i,e.detail.value)}
      ></esphome-secret-picker>`:o.s6,$=(0,d.hp)(r.sectionKey,i)&&!g&&!h&&!(0,b.R_)(l)&&!(0,d.lk)(l),k=$?(0,o.qy)`<button
        type="button"
        class="generate-key"
        @click=${()=>r.emitChange(i,(0,d.My)())}
      >
        <wa-icon library="mdi" name="auto-fix"></wa-icon>
        <span>${r.localize("device.generate_encryption_key")}</span>
      </button>`:o.s6,z=e=>g?x:m||$?(0,o.qy)`<div class="field-input-row">
            ${e}${x}${k}
          </div>`:e,C=x===o.s6?null===(a=(0,y.D)(l))?o.s6:(0,o.qy)`<span class="secret-note">
    <wa-icon library="mdi" name="key-variant"></wa-icon>
    <span>${r.localize("device.value_from_secret")}</span>
    <code>${a}</code>
  </span>`:o.s6,q="password"===t?o.s6:R(l,r.substitutions,r.localize);if(e.suggestions&&e.suggestions.length>0)return Z(e,i,n,p,h,r);if("password"===t){let t=(0,o.qy)`<esphome-password-input
      .value=${l}
      .invalid=${p}
      .disabled=${h}
      .placeholder=${u}
      @password-input-change=${e=>r.emitChange(i,e.detail.value)}
    ></esphome-password-input>`;return(0,o.qy)`
      <div class="field" data-field-key=${E(i)}>
        ${N(e,r,{path:i})} ${z(t)} ${C}
        ${j(i,r)}
      </div>
    `}let S=(0,w.td)(l),A=(0,o.qy)`<input
    type=${t}
    autocomplete="off"
    class=${p?"invalid":""}
    .value=${S?(0,w.kk)(l):l}
    ?disabled=${h}
    placeholder=${u}
    @input=${t=>{let o=t.target.value,a=S?(0,w.pV)(o):o;r.emitChange(i,(0,c.aY)(e,a))}}
  />`;return(0,o.qy)`
    <div class="field" data-field-key=${E(i)}>
      ${N(e,r,{path:i})} ${z(A)} ${C}
      ${q} ${j(i,r)}
    </div>
  `}function Z(e,t,i,r,a,n){let s=String(e.default_value??""),l=(e.suggestions??[]).map(String),d=(0,f.O)(i,l);return(0,o.qy)`
    <div class="field" data-field-key=${E(t)}>
      ${N(e,n,{path:t})}
      <wa-select
        class=${r?"invalid":""}
        ?disabled=${a}
        placeholder=${s}
        @change=${i=>n.emitChange(t,(0,c.aY)(e,i.target.value))}
      >
        ${l.map(e=>(0,o.qy)`<wa-option value=${e} ?selected=${e===d}>${e}</wa-option>`)}
      </wa-select>
      ${j(t,n)}
    </div>
  `}function H(e,t){return(0,z.xx)(e,{rootValues:e.scopeValues([]),requiredGroups:1===t.length?e.requiredGroups:void 0})}function G(e,t,i){return(0,z.V5)(e.config_entries??[],i.scopeValues(t),(0,z.xx)(i,{showAdvanced:!0,rootValues:i.scopeValues([])})).map(e=>i.renderEntry(e,[...t,e.key]))}},324(e,t,i){var r=i(7181),o=i(1379);i.d(t,{},{c:function(e,t){let{entries:i,requiredGroups:a,values:n,opts:s}=e;if(0===a.length&&!i.some(e=>e.group))return[];let l=[],d=new Map(i.map(e=>[e.key,e])),c=e=>{let t=d.get(e);return void 0!==t&&(0,o.TU)(t,n,s,i)},p=e=>e.some(c),u=(e,t)=>"all_or_none"===e||"none_or_all"===e?t:t.filter(c);for(let e of a)!e.keys.some(e=>t.has(e))&&p(e.keys)&&((0,r.$J)(e.kind,e.keys,n)||l.push({kind:e.kind,keys:u(e.kind,e.keys)}));let h=new Map;for(let e of i)e.group&&h.set(e.group,[...h.get(e.group)??[],e.key]);for(let e of h.values())!e.some(e=>t.has(e))&&p(e)&&((0,r.$J)("all_or_none",e,n)||l.push({kind:"all_or_none",keys:u("all_or_none",e)}));return l}})},8329(e,t,i){var r=i(5077),o=i(4008),a=i(6185),n=i(7181),s=i(1379),l=i(2564);function d(e,t,i){let r=new Map(t.map(e=>[e.key,e])),o=e=>{let t=r.get(e);return t?(0,l.gt)(t,i):e},a=new Set,n=[];for(let i of e){let e=r.get(i)?.group;if(!e){n.push(o(i));continue}if(a.has(e))continue;a.add(e);let s=t.filter(t=>t.group===e).map(e=>o(e.key));n.push(s.length>1?`(${s.join(", ")})`:s[0])}return n.join(", ")}function c(e){let t=new Map(e.members.map(e=>[e.key,e]));return(e.cardinality?.keys??[]).flatMap(i=>{let r=t.get(i);if(!r)return[];let o=r.group?e.members.filter(e=>e.group===r.group):[r];return[{id:o[0].key,members:o}]})}i.d(t,{},{Ci:function(e,t,i,r){let a=e.members.filter(e=>(0,s.TU)(e,t,i,r)&&!(0,s.z0)(e,t,i)),l=c(e).filter(e=>e.members.some(e=>a.includes(e))),d=0===a.length?"none":e.cardinality?.kind==="exactly_one"&&l.length>=2?"radio":"box",p="box"===d||"radio"===d&&a.some(e=>e.type===o.Hh.NESTED);return{cluster:e,painted:a,alternatives:l,mode:d,unmet:p?function(e,t){let{cardinality:i,inclusiveKeys:r}=e;return i&&!(0,n.$J)(i.kind,i.keys,t)?{kind:i.kind,keys:i.keys}:(0,n.$J)("all_or_none",r,t)?null:{kind:"all_or_none",keys:r}}(e,t):null}},Jz:function(e,t){let i=new Map(e.map(e=>[e.key,e])),r=new Map;for(let t of e)t.group&&!t.exclusive_group&&r.set(t.group,[...r.get(t.group)??[],t.key]);let o=[],a=new Set;for(let n of r.values()){let r=new Set(n),s=t.find(e=>e.keys.some(e=>r.has(e)));if(s)for(let e of s.keys)i.get(e)?.exclusive_group||r.add(e);let l=e.filter(e=>r.has(e.key));l.forEach(e=>a.add(e.key));let d=s?s.keys.filter(e=>l.some(t=>t.key===e)).length:0;o.push({members:l,cardinality:d>=2?s:void 0,inclusiveKeys:n})}return{clusters:o,memberKeys:a}},X7:d,kB:function(e,t){switch(e.mode){case"none":return r.s6;case"radio":return function(e,t){let{cluster:i,painted:o,alternatives:s}=e,d=i.members[0].key,p=t.getClusterChoice(d)??s.find(e=>e.members.some(e=>(0,n.VM)(t.getAt([e.key]))))?.id,u=s.find(e=>e.id===p),h=t.localize("device.constraint_exactly_one_radio"),m=`constraint-cluster-${d}`,f=(u?.members??[]).filter(e=>o.includes(e)),g=(0,a.es)(o);return(0,r.qy)`
    <div
      class="nested-group constraint-cluster"
      data-field-key=${(0,l.DN)([d])}
    >
      <div id=${m} class="constraint-cluster-header">
        <span>${h}</span>
      </div>
      <wa-radio-group
        class="constraint-cluster-radios"
        aria-labelledby=${m}
        .value=${p??""}
        ?disabled=${t.disabled||g}
        @change=${e=>(function(e,t,i){let r=e.members[0].key,o=c(e),a=o.find(e=>e.id===i);if(a){for(let e of o)if(e.id!==i)for(let{key:i}of e.members){let e=t.getAt([i]);void 0!==e&&(t.setClusterStash(r,i,e),t.emitChange([i],void 0))}for(let{key:e}of a.members){let i=t.getClusterStash(r,e);void 0!==i&&(t.emitChange([e],i),t.clearClusterStash(r,e))}t.setClusterChoice(r,i)}})(i,t,e.target.value)}
      >
        ${s.map(e=>(0,r.qy)`<wa-radio value=${e.id}
              >${e.members.map(e=>(0,l.gt)(e,t)).join(", ")}</wa-radio
            >`)}
      </wa-radio-group>
      ${f.length?(0,r.qy)`<div class="nested-fields">
              ${f.map(e=>t.renderEntry(e,[e.key]))}
            </div>`:r.s6}
    </div>
  `}(e,t);case"box":return function(e,t){let{cluster:i,painted:o,unmet:a}=e,n=a??{kind:i.cardinality?.kind??"all_or_none",keys:i.cardinality?.keys??i.inclusiveKeys},s=t.localize(`device.constraint_${n.kind}`,{keys:d(n.keys,t.entries,t)});return(0,r.qy)`
    <div
      class="nested-group constraint-cluster"
      data-field-key=${(0,l.DN)([i.members[0].key])}
    >
      <div class="constraint-cluster-header ${a?"unsatisfied":""}">
        ${a?(0,r.qy)`<wa-icon library="mdi" name="alert-circle-outline"></wa-icon>`:r.s6}
        <span>${s}</span>
      </div>
      <div class="nested-fields">${o.map(e=>t.renderEntry(e,[e.key]))}</div>
    </div>
  `}(e,t)}}})},2911(e,t,i){var r=i(5077),o=i(6185),a=i(1379),n=i(2564);let s="__none__";i.d(t,{},{$J:function(e){let t=new Map;for(let i of e)if(i.exclusive_group){let e=t.get(i.exclusive_group)??[];e.push(i),t.set(i.exclusive_group,e)}let i=new Set,r=[];for(let o of e)o.exclusive_group?i.has(o.exclusive_group)||(i.add(o.exclusive_group),r.push(t.get(o.exclusive_group))):r.push(o);return r},Bw:function(e,t,i,r){return{members:e,options:e.filter(e=>(0,a.TU)(e,t,i,r))}},g_:function(e,t){let{members:i,options:a}=e,l=i.filter(e=>void 0!==t.getAt([e.key])),d=l[0]?.key??"",c=i.find(e=>e.key===d),p=t.disabled||(0,o.es)(a),u=`exclusive-group-${i[0].key}`;return(0,r.qy)`
    <div class="field" data-field-key=${(0,n.DN)(c?[c.key]:[])}>
      <label class="field-label" id=${u}>
        ${t.localize("device.exclusive_group_label")}
        <span class="required">*</span>
      </label>
      <wa-select
        data-no-value-sync
        aria-labelledby=${u}
        ?disabled=${p}
        @change=${e=>{let r=e.target.value;var o=r===s?"":r;for(let e of i)e.key!==o&&void 0!==t.getAt([e.key])&&t.emitChange([e.key],void 0);o&&void 0===t.getAt([o])&&t.emitChange([o],{})}}
      >
        <wa-option value=${s} ?selected=${""===d}>
          ${t.localize("device.exclusive_group_placeholder")}
        </wa-option>
        ${a.map(e=>(0,r.qy)`<wa-option value=${e.key} ?selected=${e.key===d}
              >${(0,n.gt)(e,t)}</wa-option
            >`)}
      </wa-select>
      ${l.length>1?(0,r.qy)`<p class="field-description exclusive-group-conflict">
              ${t.localize("device.exclusive_group_conflict")}
            </p>`:r.s6}
      ${c?(0,r.qy)`<div class="nested-fields">
              ${(0,n.cu)(c,[c.key],t)}
            </div>`:r.s6}
    </div>
  `}})},901(e,t,i){var r=i(5077);let o=(0,r.AH)`
  .templatable-toggle {
    display: inline-flex;
    align-self: flex-start;
    border-radius: var(--wa-border-radius-s);
    background: var(--wa-color-surface-lowered);
    padding: 2px;
  }

  .templatable-toggle button {
    appearance: none;
    border: none;
    background: transparent;
    color: var(--wa-color-text-quiet);
    font-size: var(--wa-font-size-2xs);
    font-weight: var(--wa-font-weight-semibold);
    padding: 4px 10px;
    border-radius: var(--wa-border-radius-s);
    cursor: pointer;
  }

  .templatable-toggle button.active {
    background: var(--wa-color-surface-default);
    color: var(--wa-color-text-normal);
    box-shadow: var(--wa-shadow-xs);
  }

  .templatable-toggle button:disabled {
    cursor: not-allowed;
    opacity: 0.6;
  }
`;i.d(t,{},{L:function({isLambda:e,disabled:t,localize:i,onSwitch:o}){return(0,r.qy)`
    <div
      class="templatable-toggle"
      role="tablist"
      aria-label=${i("device.automation_literal")}
    >
      <button
        type="button"
        role="tab"
        class=${!e?"active":""}
        aria-selected=${!e}
        ?disabled=${t}
        @click=${()=>o(!1)}
      >
        ${i("device.automation_literal")}
      </button>
      <button
        type="button"
        role="tab"
        class=${e?"active":""}
        aria-selected=${e}
        ?disabled=${t}
        @click=${()=>o(!0)}
      >
        ${i("device.automation_lambda")}
      </button>
    </div>
  `},N:o})},7219(e,t,i){var r=i(4008),o=i(5109);let a={time_period:r.Hh.TIME_PERIOD,float:r.Hh.FLOAT,integer:r.Hh.INTEGER,string:r.Hh.STRING,lambda:r.Hh.LAMBDA};i.d(t,{},{DD:function(e){return Array.isArray(e)?e:[]},Dh:{light_effects:{cache:()=>(0,o.xB)(),fetch:e=>(0,o.VS)(e),parentToken:e=>e,dedupByTypeId:!0},filter:{cache:()=>(0,o.ac)(),fetch:e=>(0,o.cQ)(e),parentToken:e=>e.split(".",1)[0],dedupByTypeId:!1}},Fj:function(e){let t=[],i=[];return e.forEach((e,r)=>{!(null===e||"object"!=typeof e||Array.isArray(e))&&Object.keys(e).length<=1&&(t.push(e),i.push(r))}),{items:t,positions:i}},Q$:function(e){return e?e.replace(/_/g," ").replace(/\b\w/g,e=>e.toUpperCase()):""},XG:function(e){let t=Object.keys(e);return 1===t.length?t[0]:""},Z8:a,hC:function(e,t,i){let r=t.length>0?t[t.length-1]+1:e.length;return[...e.slice(0,r),i,...e.slice(r)]}})},3336(e,t,i){var r=i(4008),o=i(8339),a=i(7219);function n(e){let t=e?.value_type;return t&&Object.prototype.hasOwnProperty.call(a.Z8,t)?a.Z8[t]:null}function s(e,t,i={}){let a=(0,o.h)({type:e,templatable:t?.templatable??!1,...i});return e===r.Hh.TIME_PERIOD&&(a.accepts_duration_mapping=!0,t?.duration_min_unit&&(a.duration_min_unit=t.duration_min_unit)),a}let l=new WeakMap;i.d(t,{},{aj:n,as:s,rq:function(e){let t=e.config_entries.length>0?null:n(e);if(null===t)return e.config_entries;let i=l.get(e);return i||(i=[s(t,e,{key:"id",label:"Value",translation_key:"device.automation_action_delay_value",required:!0})],l.set(e,i)),i}})},8297(e,t,i){var r=i(9104),o=i(289),a=i(5077),n=i(9356),s=i(1502),l=i(1556),d=i(3140),c=i(6734),p=i(5109),u=i(2812),h=i(4117),m=i(3330),f=i(1093),g=i(2497),v=i(3425);class _{get tick(){return this._tick}hostConnected(){this._unsubscribes=this._subscribes.map(e=>e(()=>{this._tick++,this._host.requestUpdate()}))}hostDisconnected(){for(let e of this._unsubscribes)e();this._unsubscribes=[]}constructor(e,t){this._host=e,this._subscribes=t,this._tick=0,this._unsubscribes=[],e.addController(this)}}var y=i(7869);let b=(0,a.AH)`
  :host {
    display: contents;
  }

  .card {
    background: var(--wa-color-surface-default);
    border-radius: var(--navigator-border-radius, var(--wa-border-radius-l));
    border: var(
      --navigator-border,
      var(--wa-border-width-s) solid var(--wa-color-surface-border)
    );
    box-shadow: var(--navigator-shadow, var(--wa-elevation-02));
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }

  .card-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: var(--wa-space-2xs);
    padding: var(--wa-space-s) var(--wa-space-s) var(--wa-space-s) var(--wa-space-m);
    background: var(--esphome-tint);
    color: var(--esphome-primary);
    border-bottom: var(--wa-border-width-s) solid var(--wa-color-surface-border);
    flex-shrink: 0;
  }

  .card-title {
    margin: 0;
    font-size: var(--wa-font-size-s);
    font-weight: var(--wa-font-weight-bold);
    /* Match the editor header title's line-height so both header bars are the
       same height (their dividers line up) and the title baselines align.
       line-height 1 clipped the descender 'g' (#827) and left this header about
       0.4px shorter than the editor's, offsetting the divider by a pixel. */
    line-height: var(--wa-line-height-normal);
    min-width: 0;
  }

  .header-actions {
    display: inline-flex;
    align-items: center;
    gap: 0;
  }

  /* Box + hover come from .ghost-icon-btn (shared.ts). Both buttons swap
     the shared padding for a fixed width/height and add a hover
     transition; the icon size is per-site. */
  .collapse-btn,
  .search-btn {
    width: 30px;
    height: 22px;
    padding: 0;
    border-radius: var(--wa-border-radius-m);
    transition: background 0.12s;
  }

  /* Active search toggle gets a subtle tint, not the ghost-icon-btn filled
     state; reset the color too so the icon stays primary, not on-primary. */
  .search-btn[aria-pressed="true"] {
    background: color-mix(in srgb, var(--esphome-primary), transparent 88%);
    color: var(--esphome-primary);
  }

  .collapse-btn wa-icon,
  .search-btn wa-icon {
    font-size: 18px;
  }

  .card-body {
    flex: 1;
    min-height: 0;
    display: flex;
    flex-direction: column;
    overflow-y: auto;
  }

  .italic {
    font-style: italic;
    font-size: var(--wa-font-size-2xs);
    padding: 0 var(--wa-space-m);
    margin: var(--wa-space-xs) 0;
    flex-shrink: 0;
  }

  .separator {
    height: 1px;
    background: var(--wa-color-surface-border);
    margin: var(--wa-space-2xs) 0;
    flex-shrink: 0;
  }

  .nav-empty {
    padding: var(--wa-space-l) var(--wa-space-m);
    margin: 0;
    font-size: var(--wa-font-size-s);
    color: var(--wa-color-text-quiet);
    text-align: center;
  }

  .nav-content {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 var(--wa-space-m);
    cursor: pointer;
    user-select: none;
    flex-shrink: 0;
  }

  .nav-content-label {
    display: flex;
    align-items: center;
    gap: var(--wa-space-xs);
    min-width: 0;
  }

  .nav-content:hover p {
    color: var(--esphome-primary);
  }

  .nav-content p {
    margin: var(--wa-space-xs) 0;
    font-size: var(--wa-font-size-s);
    font-weight: var(--wa-font-weight-bold);
  }

  .nav-content-label wa-icon {
    font-size: var(--wa-font-size-l);
    color: var(--esphome-primary);
    flex-shrink: 0;
  }

  .nav-content-chevron {
    font-size: var(--wa-font-size-xl);
    color: var(--esphome-primary);
    flex-shrink: 0;
  }

  .nav-subgroup-header {
    display: flex;
    align-items: center;
    gap: var(--wa-space-xs);
    /* Match the flat rows' inter-block gap with margin-top (not vertical
       padding) so a header sits the same distance below the previous block
       as the rows do; the header-to-rows gap lives on .nav-items--grouped. */
    padding: 0 var(--wa-space-m);
    margin-top: var(--wa-space-2xs);
    cursor: pointer;
    user-select: none;
    flex-shrink: 0;
  }

  .nav-subgroup-header:not(.nav-subgroup-header--static):hover .nav-subgroup-title {
    color: var(--esphome-primary);
  }

  .nav-subgroup-header:focus-visible {
    outline: none;
    box-shadow: var(--esphome-focus-ring-tight);
    border-radius: var(--wa-border-radius-s);
  }

  /* While filtering the subgroup can't collapse, so it isn't interactive. */
  .nav-subgroup-header--static {
    cursor: default;
  }

  /* Muted leading domain glyph — on a domain subgroup header and on an
     ungrouped row (Core / Automations). Always visible. */
  .nav-subgroup-icon,
  .nav-item-icon {
    font-size: var(--wa-font-size-m);
    color: var(--wa-color-text-quiet);
    flex-shrink: 0;
  }

  .nav-subgroup-title {
    font-size: var(--wa-font-size-2xs);
    font-weight: var(--wa-font-weight-semibold);
    text-transform: uppercase;
    letter-spacing: 0.04em;
    color: var(--wa-color-text-quiet);
  }

  .nav-subgroup-count,
  .nav-item-error-badge {
    font-size: var(--wa-font-size-2xs);
    color: var(--wa-color-text-quiet);
    background: var(--wa-color-surface-raised);
    border-radius: 999px;
    padding: 0 var(--wa-space-xs);
    line-height: 1.5;
  }

  .nav-subgroup-chevron {
    margin-left: auto;
    font-size: var(--wa-font-size-l);
    color: var(--wa-color-text-quiet);
    flex-shrink: 0;
  }

  .nav-items {
    display: flex;
    flex-direction: column;
    /* Bordered rows need breathing room so adjacent boxes don't touch. */
    gap: var(--wa-space-2xs);
    /* var(--wa-space-m) horizontal inset lines the row boxes' left/right
       edges up under the section headers' content. */
    padding: var(--wa-space-xs) var(--wa-space-m);
  }

  /* Rows nested under a domain subgroup; the box edge keeps the shared
     var(--wa-space-m) inset. padding-top is the header-to-first-row gap;
     padding-bottom is 0 so the next block's own margin sets the gap. */
  .nav-items--grouped {
    padding-top: var(--wa-space-2xs);
    padding-bottom: 0;
  }

  /* A lone config-block domain (no "platform:", e.g. i2c / bluetooth_proxy)
     renders as one flat row in place of a header; platform components keep
     their header even with one item. Keep the shared box inset and only drop
     the vertical pad; margin-top carries the inter-block gap, since each
     single is its own one-row container. */
  .nav-items--single {
    padding-top: 0;
    padding-bottom: 0;
    margin-top: var(--wa-space-2xs);
  }

  .nav-item {
    padding: 0 var(--wa-space-2xs);
    border-radius: var(--wa-border-radius-m);
    border: var(--wa-border-width-s) solid var(--wa-color-surface-border);
    /* Uniform row height tracked off the type scale (two text lines plus the
       row's own breathing room) so a description-less row pads up to the same
       box as a title + description one instead of rendering shorter. */
    min-height: calc(2 * var(--wa-font-size-s) + var(--wa-space-m));
    display: flex;
    align-items: center;
    gap: var(--wa-space-xs);
    cursor: pointer;
    user-select: none;
    transition:
      background 0.1s,
      border-color 0.1s;
  }

  .nav-item:hover,
  .nav-item--hovered {
    background: var(--esphome-tint);
  }

  /* Selected adds the primary border so the open row stays distinct from a
     row that is merely hovered (which only tints the background). */
  .nav-item--selected {
    background: var(--esphome-tint);
    border-color: var(--esphome-primary);
  }

  .nav-item-content {
    display: flex;
    flex-direction: column;
    flex: 1 1 auto;
    min-width: 0;
    padding: var(--wa-space-2xs) 0;
  }

  .nav-item-content p {
    margin: 0;
    font-size: var(--wa-font-size-s);
    font-weight: var(--wa-font-weight-semibold);
  }

  .nav-item-subtitle {
    font-size: var(--wa-font-size-2xs);
    color: var(--wa-color-text-quiet);
    font-weight: normal;
    margin: 0;
    line-height: 1.2;
  }

  /* Error-count pill on a row (or a collapsed subgroup header) whose
     section carries backend validation errors. Shares the count pill's
     geometry above; only the color treatment differs. */
  .nav-item-error-badge {
    margin-left: auto;
    font-weight: var(--wa-font-weight-semibold);
    color: var(--esphome-error);
    background: color-mix(in srgb, var(--esphome-error), transparent 88%);
    flex-shrink: 0;
  }

  .nav-subgroup-header .nav-item-error-badge {
    margin-left: 0;
  }

  .nav-item-chevron {
    margin-left: auto;
    font-size: var(--wa-font-size-l);
    color: var(--esphome-primary);
    flex-shrink: 0;
  }

  /* The chevron yields the right edge when an error badge holds it. */
  .nav-item-error-badge ~ .nav-item-chevron {
    margin-left: 0;
  }

  /* Declutter the chevron only where hover exists; on touch (no hover)
     it stays visible so the "this row navigates" cue isn't lost. */
  @media (hover: hover) {
    .nav-item-chevron {
      opacity: 0;
      transition: opacity 0.1s;
    }

    .nav-item:hover .nav-item-chevron,
    .nav-item--hovered .nav-item-chevron,
    .nav-item--selected .nav-item-chevron {
      opacity: 1;
    }
  }

  .action-item {
    padding: 0 var(--wa-space-2xs);
    border-radius: var(--wa-border-radius-m);
    display: flex;
    align-items: center;
    background: var(--esphome-primary);
    color: var(--esphome-on-primary);
    justify-content: space-between;
    cursor: pointer;
    user-select: none;
    transition:
      background 0.1s,
      border-color 0.1s;
  }

  .action-item:hover,
  .action-item--hovered {
    opacity: 0.9;
  }

  .action-item p {
    margin: var(--wa-space-xs) 0;
    font-size: var(--wa-font-size-s);
    font-weight: var(--wa-font-weight-bold);
  }

  .action-item wa-icon {
    font-size: var(--wa-font-size-l);
  }

  .action-item div {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: var(--wa-space-2xs);
  }
`;var w=i(5413);function x(e,t){let{core:i,components:r,automations:o}=(0,g.uU)((0,g.MT)(e),t),a=(0,g.vB)(e);return{core:i,components:r,automations:[...o.filter(e=>"script"!==e.key&&"interval"!==e.key),...a].filter(e=>!e.key.startsWith("automation:light_effect:")&&!e.key.startsWith("automation:unscoped:")).sort((e,t)=>e.fromLine-t.fromLine),substitutions:(0,w.Gr)(e)}}function $(e){let t=[],i=new Map;for(let r of e){let e=r.item.key,o=i.get(e);o||(o=[],i.set(e,o),t.push(e)),o.push(r)}return t.map(e=>({key:e,rows:i.get(e)}))}var k=i(4323),z=i(9995),C=i(2353);function q(e,t,i){let r=(0,g.gU)(e);if("automation"===t)return function(e,t,i){if("script"===e.parentKey&&!e.eventKey){let r=i.localize("device.script_header_title_static"),o=(0,w.rq)(e.id??t,i.substitutions);return{primary:r,secondary:o!==r?o:void 0}}if("interval"===e.parentKey){let t=i.localize("device.automation_interval_label"),r=e.meta?.every;return{primary:t,secondary:r?i.localize("device.automation_interval_every_n",{time:r}):void 0}}if("esphome"===e.parentKey&&e.eventKey)return{primary:O(i.triggerCatalog.resolveName(["esphome"],e.eventKey,A(e.eventKey)))};if(e.parentKey&&e.eventKey){let t=O(i.triggerCatalog.resolveName((0,C.yZ)(e.parentKey,e.hostPlatform),e.eventKey,A(e.eventKey)));return{primary:t,secondary:S(e,i,t)}}if(e.parentKey&&e.actionField){let t=(0,k.t)(e.actionField,i.localize);return{primary:t,secondary:S(e,i,t)}}return{primary:e.displayLabel||t}}(e,r,i);let o=r,a=(0,h.CQ)(r,i.platform||void 0);a?.name&&(o=a.name),"core"===t&&(o=(0,z.m)(o));let n="core"===t&&"esphome"===e.key&&i.deviceName?i.deviceName:(0,w.rq)(e.name||e.id||"",i.substitutions)||void 0,s=n&&n!==o?n:void 0;return{primary:o,secondary:s}}function S(e,t,i){let r=e.name||e.id,o=r?(0,w.rq)(r,t.substitutions):M(e.parentKey??"");return o!==i?o:void 0}function A(e){return e.split("_").map(e=>e.charAt(0).toUpperCase()+e.slice(1)).join(" ")}function O(e){let t=e.lastIndexOf(" → ");return t>=0?e.slice(t+3):e}function M(e){let t=e.replace(/_/g," ");return t.charAt(0).toUpperCase()+t.slice(1)}var E=i(7288),I=i(9460),P=i(1020);i(5016);let R={esphome:o.mdiChip,wifi:o.mdiWifi,ethernet:o.mdiEthernet,mdns:o.mdiRadioTower,network:o.mdiLan,api:o.mdiApi,ota:o.mdiCloudUploadOutline,dashboard_import:o.mdiCloudUploadOutline,logger:o.mdiCardTextOutline,syslog:o.mdiCardTextOutline,web_server:o.mdiWeb,http_request:o.mdiWeb,captive_portal:o.mdiWifiLock,improv_serial:o.mdiWifiCog,improv_ble:o.mdiWifiCog,esp32_improv:o.mdiWifiCog,mqtt:o.mdiSwapHorizontal,wireguard:o.mdiVpn,socket:o.mdiConnection,udp:o.mdiConnection,async_tcp:o.mdiConnection,espnow:o.mdiConnection,serial_proxy:o.mdiConnection,sim800l:o.mdiConnection,prometheus:o.mdiChartLine,statsd:o.mdiChartLine,runtime_stats:o.mdiChartLine,time:o.mdiClockOutline,sntp:o.mdiClockOutline,interval:o.mdiClockOutline,script:o.mdiScriptTextOutline,uart:o.mdiSerialPort,i2c:o.mdiConnection,spi:o.mdiConnection,modbus:o.mdiConnection,modbus_controller:o.mdiConnection,modbus_server:o.mdiConnection,esp32:o.mdiCpu32Bit,esp8266:o.mdiCpu32Bit,rp2:o.mdiCpu32Bit,rp2040:o.mdiCpu32Bit,bk72xx:o.mdiCpu32Bit,rtl87xx:o.mdiCpu32Bit,ln882x:o.mdiCpu32Bit,libretiny:o.mdiCpu32Bit,nrf52:o.mdiCpu32Bit,host:o.mdiChip,esp32_hosted:o.mdiWifi,esp32_ble:o.mdiBluetooth,esp32_ble_tracker:o.mdiBluetooth,ble:o.mdiBluetooth,bluetooth_proxy:o.mdiBluetooth,ble_client:o.mdiBluetooth,ble_nus:o.mdiBluetooth,esp32_ble_beacon:o.mdiBluetooth,esp32_ble_server:o.mdiBluetooth,zephyr_ble_server:o.mdiBluetooth,rp2040_ble:o.mdiBluetooth,exposure_notifications:o.mdiBluetooth,airthings_ble:o.mdiBluetooth,bedjet:o.mdiBluetooth,mopeka_ble:o.mdiBluetooth,radon_eye_ble:o.mdiBluetooth,ruuvi_ble:o.mdiBluetooth,xiaomi_ble:o.mdiBluetooth,xiaomi_rtcgq02lm:o.mdiBluetooth,zwave_proxy:o.mdiZWave,zigbee:o.mdiZigbee,openthread:o.mdiZigbee,usb_host:o.mdiUsb,usb_uart:o.mdiUsb,usb_cdc_acm:o.mdiUsb,tinyusb:o.mdiUsb,psram:o.mdiMemory,preferences:o.mdiContentSaveCogOutline,power_supply:o.mdiPowerPlug,esp_ldo:o.mdiPowerPlug,sy6970:o.mdiPowerPlug,deep_sleep:o.mdiPowerSleep,status_led:o.mdiLedOn,safe_mode:o.mdiRestartAlert,factory_reset:o.mdiRestartAlert,debug:o.mdiBug,globals:o.mdiVariable,substitutions:o.mdiCodeBraces,packages:o.mdiPackageVariantClosed,external_components:o.mdiPuzzleOutline,mapping:o.mdiCog,json:o.mdiCodeJson,bytebuffer:o.mdiCodeArray,split_buffer:o.mdiCodeArray,sha256:o.mdiPoundBoxOutline,hmac_md5:o.mdiPoundBoxOutline,hmac_sha256:o.mdiPoundBoxOutline,remote_receiver:o.mdiRemote,remote_transmitter:o.mdiRemote,cc1101:o.mdiRemote,sx126x:o.mdiRemote,sx127x:o.mdiRemote,lightwaverf:o.mdiRemote,rf_bridge:o.mdiRemote,pn532:o.mdiNfcVariant,pn532_i2c:o.mdiNfcVariant,pn532_spi:o.mdiNfcVariant,pn7150_i2c:o.mdiNfcVariant,pn7160_i2c:o.mdiNfcVariant,pn7160_spi:o.mdiNfcVariant,rc522_i2c:o.mdiNfcVariant,rc522_spi:o.mdiNfcVariant,rdm6300:o.mdiNfcVariant,ld2410:o.mdiMotionSensor,ld2412:o.mdiMotionSensor,ld2420:o.mdiMotionSensor,ld2450:o.mdiMotionSensor,rd03d:o.mdiMotionSensor,at581x:o.mdiMotionSensor,dfrobot_sen0395:o.mdiMotionSensor,hlk_fm22x:o.mdiMotionSensor,seeed_mr24hpc1:o.mdiMotionSensor,seeed_mr60bha2:o.mdiMotionSensor,seeed_mr60fda2:o.mdiMotionSensor,esp32_touch:o.mdiGestureTapButton,cap1188:o.mdiGestureTapButton,mpr121:o.mdiGestureTapButton,ttp229_bsf:o.mdiGestureTapButton,ttp229_lsf:o.mdiGestureTapButton,matrix_keypad:o.mdiDialpad,wiegand:o.mdiDialpad,key_collector:o.mdiDialpad,fingerprint_grow:o.mdiFingerprint,i2s_audio:o.mdiVolumeHigh,audio:o.mdiVolumeHigh,audio_file:o.mdiVolumeHigh,microphone:o.mdiMicrophone,micro_wake_word:o.mdiMicrophone,voice_assistant:o.mdiMicrophoneMessage,speaker:o.mdiSpeaker,dfplayer:o.mdiSpeaker,rtttl:o.mdiSpeaker,adalight:o.mdiLightbulbOutline,wled:o.mdiLightbulbOutline,e131:o.mdiLightbulbOutline,my9231:o.mdiLightbulbOutline,sm16716:o.mdiLightbulbOutline,sm2135:o.mdiLightbulbOutline,sm2235:o.mdiLightbulbOutline,sm2335:o.mdiLightbulbOutline,bp1658cj:o.mdiLightbulbOutline,bp5758d:o.mdiLightbulbOutline,tlc59208f:o.mdiLightbulbOutline,tlc5947:o.mdiLightbulbOutline,tlc5971:o.mdiLightbulbOutline,tm1651:o.mdiLightbulbOutline,adc128s102:o.mdiGauge,ads1115:o.mdiGauge,ads1118:o.mdiGauge,mcp3008:o.mdiGauge,mcp3204:o.mdiGauge,as5600:o.mdiGauge,dac7678:o.mdiExportVariant,gp8403:o.mdiExportVariant,mcp4728:o.mdiExportVariant,mcp4461:o.mdiExportVariant,pca9685:o.mdiExportVariant,servo:o.mdiExportVariant,grove_tb6612fng:o.mdiExportVariant,mcp23008:o.mdiConnection,mcp23016:o.mdiConnection,mcp23017:o.mdiConnection,mcp23s08:o.mdiConnection,mcp23s17:o.mdiConnection,pca6416a:o.mdiConnection,pca9554:o.mdiConnection,pcf8574:o.mdiConnection,pi4ioe5v6408:o.mdiConnection,xl9535:o.mdiConnection,max6956:o.mdiConnection,sn74hc165:o.mdiConnection,sn74hc595:o.mdiConnection,cd74hc4067:o.mdiConnection,tca9548a:o.mdiConnection,tca9555:o.mdiConnection,ch422g:o.mdiConnection,ch423:o.mdiConnection,sx1509:o.mdiConnection,m5stack_8angle:o.mdiConnection,i2c_device:o.mdiConnection,spi_device:o.mdiConnection,vbus:o.mdiConnection,tuya:o.mdiConnection,wk2132_i2c:o.mdiSerialPort,wk2132_spi:o.mdiSerialPort,wk2168_i2c:o.mdiSerialPort,wk2168_spi:o.mdiSerialPort,wk2204_i2c:o.mdiSerialPort,wk2204_spi:o.mdiSerialPort,wk2212_i2c:o.mdiSerialPort,wk2212_spi:o.mdiSerialPort,apds9960:o.mdiGauge,as3935_i2c:o.mdiGauge,as3935_spi:o.mdiGauge,bme680_bsec:o.mdiGauge,bme68x_bsec2_i2c:o.mdiGauge,gdk101:o.mdiGauge,msa3xx:o.mdiGauge,ezo_pmp:o.mdiGauge,daly_bms:o.mdiGauge,pylontech:o.mdiGauge,pipsolar:o.mdiGauge,sun_gtil2:o.mdiGauge,sml:o.mdiGauge,dsmr:o.mdiGauge,teleinfo:o.mdiGauge,dlms_meter:o.mdiGauge,emontx:o.mdiGauge,emc2101:o.mdiFan,gps:o.mdiCrosshairsGps,sun:o.mdiWeatherSunny,opentherm:o.mdiThermostat,uponor_smatrix:o.mdiThermostat,micronova:o.mdiThermostat,sprinkler:o.mdiSprinklerVariant,sensor:o.mdiGauge,binary_sensor:o.mdiCheckboxMarkedCircleOutline,text_sensor:o.mdiTextBoxOutline,switch:o.mdiToggleSwitchOutline,light:o.mdiLightbulbOutline,output:o.mdiExportVariant,number:o.mdiNumeric,select:o.mdiFormDropdown,button:o.mdiGestureTapButton,fan:o.mdiFan,cover:o.mdiWindowShutter,climate:o.mdiThermostat,text:o.mdiFormTextbox,lock:o.mdiLockOutline,valve:o.mdiValve,media_player:o.mdiSpeaker,display:o.mdiMonitor,lvgl:o.mdiMonitor,graphical_display_menu:o.mdiMonitor,lcd_menu:o.mdiMonitor,datetime:o.mdiCalendarClock,camera:o.mdiCameraOutline,esp32_camera:o.mdiCameraOutline,esp32_camera_web_server:o.mdiCameraOutline,camera_encoder:o.mdiCameraOutline,event:o.mdiBellOutline,alarm_control_panel:o.mdiShieldHomeOutline,graph:o.mdiChartLine,color:o.mdiPalette,qr_code:o.mdiQrcode,font:o.mdiFormatFont,image:o.mdiImageOutline,online_image:o.mdiImageSyncOutline,animation:o.mdiImageMultipleOutline},L=o.mdiShapeOutline,F=(0,P.R)(o.mdiChevronRight,"nav-item-chevron"),N=(0,P.R)(o.mdiChevronUp,"nav-subgroup-chevron"),D=(0,P.R)(o.mdiChevronDown,"nav-subgroup-chevron");function j(e,t,i){var r;let{item:o,labels:n}=e,{primary:s,secondary:l}=n,d=o.parentKey??o.key,c=t.errorCount?.(o)??0;return(0,a.qy)`
    <div
      class="nav-item ${t.selectedLine===o.fromLine?"nav-item--selected":""} ${t.hoveredLine===o.fromLine?"nav-item--hovered":""}"
      ${(0,v.Wf)("esphome"===o.key&&t.tourAnchorId?`${t.tourAnchorId}-item`:void 0)}
      @mouseenter=${()=>t.onItemEnter(o)}
      @mouseleave=${()=>t.onItemLeave()}
      @click=${()=>t.onItemClick(o)}
    >
      ${i?"esphome"===(r=d)?(0,a.qy)`<wa-icon
      class="nav-item-icon"
      src=${(0,I.cV)("/assets/logo/esphome-mono-black.svg")}
      title="ESPHome"
    ></wa-icon>`:(0,P.R)(R[r]??L,"nav-item-icon",M(r)):a.s6}
      <div class="nav-item-content">
        <p class="truncate">${s}</p>
        ${l?(0,a.qy)`<span class="nav-item-subtitle truncate">${l}</span>`:a.s6}
      </div>
      ${c>0?T(c,t):a.s6} ${F}
    </div>
  `}function T(e,t){return(0,a.qy)`<span
    class="nav-item-error-badge"
    role="img"
    aria-label=${t.errorLabel(e)}
    >${e}</span
  >`}function B(e){("Enter"===e.key||" "===e.key)&&(e.preventDefault(),e.currentTarget.click())}class K{hostUpdated(){let{selectedLine:e,buckets:t,openSections:i,filtering:r}=this._read();if(null===e){this._scrolled=null,this._revealed=null;return}let o=t.core.some(t=>t.fromLine===e)?0:t.components.some(t=>t.fromLine===e)?1:t.automations.some(t=>t.fromLine===e)?2:-1,a=`${e}:${o}`;if(this._revealed!==a&&(this._revealed=null),this._scrolled===a)return;if(-1===o){this._scrolled=a;return}if(!r&&!i.has(o)&&this._revealed!==a){this._revealed=a,this._host.dispatchEvent(new CustomEvent("section-reveal",{detail:{index:o},bubbles:!0,composed:!0}));return}this._revealed=a;let n=this._host.renderRoot.querySelector(".nav-item--selected");n&&n.getClientRects().length>0&&(n.scrollIntoView({block:"nearest"}),this._scrolled=a)}constructor(e,t){this._host=e,this._read=t,this._scrolled=null,this._revealed=null,e.addController(this)}}var V=i(1148);i(9218),i(1752),i(7427);var U=i(1919);function Z(e,t,i,r){var o,a=arguments.length,n=a<3?t:null===r?r=Object.getOwnPropertyDescriptor(t,i):r;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)n=Reflect.decorate(e,t,i,r);else for(var s=e.length-1;s>=0;s--)(o=e[s])&&(n=(a<3?o(n):a>3?o(t,i,n):o(t,i))||n);return a>3&&n&&Object.defineProperty(t,i,n),n}class H extends a.WF{open(){this._inner.open()}render(){return(0,a.qy)`<esphome-add-component-dialog
      .lockedCategories=${U.b}
      .boardName=${this.boardName}
      .configuration=${this.configuration}
      .platform=${this.platform}
      .board=${this.board}
      .yaml=${this.yaml}
    ></esphome-add-component-dialog>`}constructor(...e){super(...e),this.boardName="",this.configuration="",this.platform="",this.board=null,this.yaml=""}}Z([(0,n.MZ)()],H.prototype,"boardName",void 0),Z([(0,n.MZ)()],H.prototype,"configuration",void 0),Z([(0,n.MZ)()],H.prototype,"platform",void 0),Z([(0,n.MZ)({attribute:!1})],H.prototype,"board",void 0),Z([(0,n.MZ)()],H.prototype,"yaml",void 0),Z([(0,n.P)("esphome-add-component-dialog")],H.prototype,"_inner",void 0),H=Z([(0,n.EM)("esphome-add-config-dialog")],H);var G=i(918),W=i(5865),Y=i(5660),Q=i(325),J=i(8283),X=i(664),ee=i(3074),et=i(6910),ei=i(2311);function er(e,t,i,r){var o,a=arguments.length,n=a<3?t:null===r?r=Object.getOwnPropertyDescriptor(t,i):r;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)n=Reflect.decorate(e,t,i,r);else for(var s=e.length-1;s>=0;s--)(o=e[s])&&(n=(a<3?o(n):a>3?o(t,i,n):o(t,i))||n);return a>3&&n&&Object.defineProperty(t,i,n),n}i(9835),(0,f.C)({close:o.mdiClose});class eo extends a.WF{open(){this._id="",this._error="",this._dialog.open=!0,this._loadAvailable()}async _loadAvailable(){if(this._api&&this.configuration)try{this._available=await this._api.getAvailableAutomations(this.configuration,this.yaml)}catch(e){this._error=(0,J.u)(e)}}render(){let e=this.boardName?this._localize("device.add_script_dialog_title",{name:this.boardName}):this._localize("device.add_script");return(0,a.qy)`<esphome-base-dialog
      ?open=${this._dialog.open}
      ?busy=${this._saving}
      .label=${e}
      .confirmOnEnter=${this._onContinue}
      @request-close=${this._dialog.onRequestClose}
    >
      <p class="intro">
        ${(0,et.Gc)(this._localize("device.script_header_description"))}
      </p>
      <div class="field">
        <label class="field-label" for="script-id-input">
          ${this._localize("device.automation_target_script_new_id_label")}
          <span class="required">*</span>
        </label>
        <input
          id="script-id-input"
          type="text"
          .value=${this._id}
          placeholder=${this._localize("device.automation_target_script_id_placeholder")}
          ?disabled=${this._saving}
          @input=${e=>{this._id=(0,X.e)(e.target.value),this._error=""}}
        />
      </div>
      ${this._error?(0,a.qy)`<p class="error" role="alert">${this._error}</p>`:a.s6}
      <div class="actions">
        <button
          type="button"
          class="primary"
          ?disabled=${this._saving||!this._canContinue()}
          @click=${this._onContinue}
        >
          ${this._saving?this._localize("device.adding"):this._localize("device.add_automation_continue")}
        </button>
      </div>
    </esphome-base-dialog>`}_canContinue(){return!!this._id&&!this._available?.scripts.some(e=>e.id===this._id)}constructor(...e){super(...e),this._localize=e=>e,this.boardName="",this.configuration="",this.yaml="",this.board=null,this._dialog=new Q.T(this),this._id="",this._available=null,this._saving=!1,this._error="",this._onContinue=async()=>{if(this._api&&this._canContinue()&&!this._saving){this._saving=!0,this._error="";try{let e={kind:"script",id:this._id},t=this.configuration,i=this.yaml,{yaml_diff:r}=await this._api.upsertAutomation(t,{trigger_id:null,trigger_params:{mode:"single"},actions:[]},e,i);(0,ei.K)(this,t,i,e,r),this._dialog.open=!1}catch(t){let e=(0,ee.K)(t,this._localize,"device.automation_save_error");this._error=e,(0,G.UG)(this._localize("device.automation_save_error"),{description:e})}finally{this._saving=!1}}}}}eo.styles=[d.G9,Y.z9,W.h,(0,a.AH)`
      esphome-base-dialog {
        --width: 480px;
      }
      esphome-base-dialog::part(body) {
        padding: var(--wa-space-l);
      }
      .intro code {
        font-family: ui-monospace, "SF Mono", Menlo, Consolas, monospace;
        font-size: var(--wa-font-size-2xs);
        padding: 1px 4px;
        border-radius: var(--wa-border-radius-s);
        background: var(--wa-color-surface-lowered);
      }
      .field {
        display: flex;
        flex-direction: column;
        gap: var(--wa-space-2xs);
      }
      .actions {
        display: flex;
        justify-content: flex-end;
        gap: var(--wa-space-s);
        margin-top: var(--wa-space-l);
      }

      .actions button {
        display: inline-flex;
        align-items: center;
        box-sizing: border-box;
        gap: 3px;
        padding: 7px 14px;
        border: var(--wa-border-width-s) solid transparent;
        border-radius: var(--wa-border-radius-m);
        cursor: pointer;
        font-size: var(--wa-font-size-xs);
        font-weight: var(--wa-font-weight-bold);
        font-family: inherit;
        line-height: 1;
        transition:
          background 0.12s,
          border-color 0.12s,
          box-shadow 0.12s,
          transform 0.12s;
      }
      .actions .primary {
        background: var(--esphome-primary);
        color: var(--esphome-on-primary);
        box-shadow: var(--esphome-primary-shadow);
      }
      .actions .primary:hover:not(:disabled) {
        background: var(--esphome-primary-hover);
        box-shadow: var(--esphome-primary-shadow-hover);
        transform: translateY(-1px);
      }
      .actions .primary:active:not(:disabled) {
        transform: translateY(0);
      }
      .actions .primary:disabled {
        background: color-mix(
          in srgb,
          var(--esphome-primary) 35%,
          var(--wa-color-surface-default)
        );
        color: color-mix(in srgb, var(--esphome-on-primary), transparent 30%);
        cursor: not-allowed;
        box-shadow: none;
        transform: none;
      }
    `],er([(0,r.Fg)({context:l.$F,subscribe:!0}),(0,n.wk)()],eo.prototype,"_localize",void 0),er([(0,r.Fg)({context:l.Ie})],eo.prototype,"_api",void 0),er([(0,n.MZ)()],eo.prototype,"boardName",void 0),er([(0,n.MZ)()],eo.prototype,"configuration",void 0),er([(0,n.MZ)()],eo.prototype,"yaml",void 0),er([(0,n.MZ)({attribute:!1})],eo.prototype,"board",void 0),er([(0,n.wk)()],eo.prototype,"_id",void 0),er([(0,n.wk)()],eo.prototype,"_available",void 0),er([(0,n.wk)()],eo.prototype,"_saving",void 0),er([(0,n.wk)()],eo.prototype,"_error",void 0),eo=er([(0,n.EM)("esphome-add-script-dialog")],eo);let ea=(0,a.AH)`
  :host {
    display: block;
  }

  :host([hidden]) {
    display: none;
  }

  .search {
    display: flex;
    align-items: center;
    gap: var(--wa-space-xs);
    margin: var(--wa-space-s) var(--wa-space-s) var(--wa-space-2xs);
    padding: 0 var(--wa-space-s);
    border: var(--wa-border-width-s) solid var(--wa-color-surface-border);
    border-radius: var(--wa-border-radius-m);
    background: var(--wa-color-surface-default);
    /* Wrapper draws the border, so it carries the shared control height. */
    ${Y.BJ}
  }

  .search:focus-within {
    ${Y.jq}
  }

  input {
    flex: 1;
    min-width: 0;
    border: none;
    background: transparent;
    color: var(--wa-color-text-normal);
    ${Y.xw}
    /* 16px floor avoids iOS focus-zoom in the mobile drawer (overrides the
       shared 14px); the wrapper holds the height, so this doesn't grow it. */
    font-size: max(16px, var(--wa-font-size-s));
    font-family: inherit;
    padding: 0;
    outline: none;
  }

  /* The native clear affordance duplicates our own ✕ button. */
  input::-webkit-search-cancel-button {
    display: none;
  }

  .search-clear {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    border: none;
    background: transparent;
    color: var(--wa-color-text-quiet);
    cursor: pointer;
    padding: 2px;
    border-radius: var(--wa-border-radius-s);
    flex-shrink: 0;
  }

  .search-clear:hover {
    color: var(--wa-color-text-normal);
  }

  .search-clear wa-icon {
    display: block;
    font-size: var(--wa-font-size-m);
  }

  .search-result {
    margin: var(--wa-space-2xs) var(--wa-space-s) var(--wa-space-xs);
    font-size: var(--wa-font-size-2xs);
    color: var(--wa-color-text-quiet);
  }
`;function en(e,t,i,r){var o,a=arguments.length,n=a<3?t:null===r?r=Object.getOwnPropertyDescriptor(t,i):r;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)n=Reflect.decorate(e,t,i,r);else for(var s=e.length-1;s>=0;s--)(o=e[s])&&(n=(a<3?o(n):a>3?o(t,i,n):o(t,i))||n);return a>3&&n&&Object.defineProperty(t,i,n),n}(0,f.C)({close:o.mdiClose});class es extends a.WF{focusInput(){this._input?.focus()}render(){let e=this._localize("device.navigator_search_placeholder");return(0,a.qy)`
      <div class="search">
        <input
          type="search"
          .value=${this.value}
          placeholder=${e}
          aria-label=${e}
          enterkeyhint="search"
          autocomplete="off"
          autocapitalize="off"
          autocorrect="off"
          spellcheck="false"
          @input=${this._onInput}
          @keydown=${this._onKeydown}
        />
        ${this.value?(0,a.qy)`<button
                type="button"
                class="search-clear"
                @click=${this._clear}
                title=${this._localize("device.navigator_search_clear")}
                aria-label=${this._localize("device.navigator_search_clear")}
              >
                <wa-icon library="mdi" name="close"></wa-icon>
              </button>`:a.s6}
      </div>
      ${this.value&&this.resultLabel?(0,a.qy)`<p class="search-result" role="status">${this.resultLabel}</p>`:a.s6}
    `}_emit(e){(0,m.r)(this,"navigator-search",{value:e})}constructor(...e){super(...e),this._localize=e=>e,this.value="",this.resultLabel="",this._onInput=e=>{this.value=e.target.value,this._emit(this.value)},this._onKeydown=e=>{"Escape"===e.key&&this._input?.value&&(e.stopPropagation(),this._clear())},this._clear=()=>{this.value="",this._emit(""),this._input?.focus()}}}es.styles=[d.G9,ea],en([(0,r.Fg)({context:l.$F,subscribe:!0}),(0,n.wk)()],es.prototype,"_localize",void 0),en([(0,n.MZ)()],es.prototype,"value",void 0),en([(0,n.MZ)()],es.prototype,"resultLabel",void 0),en([(0,n.P)("input")],es.prototype,"_input",void 0),es=en([(0,n.EM)("esphome-navigator-search")],es);var el=i(5494),ed=i(7297);function ec(e,t,i,r){var o,a=arguments.length,n=a<3?t:null===r?r=Object.getOwnPropertyDescriptor(t,i):r;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)n=Reflect.decorate(e,t,i,r);else for(var s=e.length-1;s>=0;s--)(o=e[s])&&(n=(a<3?o(n):a>3?o(t,i,n):o(t,i))||n);return a>3&&n&&Object.defineProperty(t,i,n),n}(0,f.C)({"chevron-down":o.mdiChevronDown,"chevron-up":o.mdiChevronUp,cog:o.mdiCog,magnify:o.mdiMagnify,menu:o.mdiMenu,"plus-circle-outline":o.mdiPlusCircleOutline,"script-text-outline":o.mdiScriptTextOutline});class ep extends a.WF{_buckets(){return this._deriveBuckets(this.yaml,(0,g.Zt)(this._catalogIndex.index()))}willUpdate(e){if((e.has("yaml")||e.has("platform")||e.has("platformReady"))&&this.yaml&&this.platformReady&&this._kickoffNameResolves(),(e.has("selectedKey")||e.has("yaml")||e.has("selectedFromLine"))&&this.yaml){if(!this.selectedKey){this._selectedLine=null,this._selectedRange=null;return}let e=[...(0,g.MT)(this.yaml),...(0,g.vB)(this.yaml)],t=(void 0!==this.selectedFromLine?e.find(e=>e.fromLine===this.selectedFromLine):void 0)??e.find(e=>(0,g.gU)(e)===this.selectedKey);t&&(this._selectedLine=t.fromLine,this._selectedRange={fromLine:t.fromLine,toLine:t.toLine})}}render(){let e=this._buckets(),{core:t,components:i,automations:r}=e,o=e=>!this._collapsedGroups.has(e),n=[{label:this._localize("device.section_core"),desc:this._localize("device.section_core_desc"),icon:el.I.core,items:t,category:"core",actions:[{label:this._localize("device.add_config"),icon:"cog",onClick:()=>this._addConfigDialog.open()}]},{label:this._localize("device.section_components"),desc:this._localize("device.section_components_desc"),icon:el.I.components,items:i,category:"component",actions:[{label:this._localize("device.add_component"),icon:el.I.components,onClick:()=>this._addComponentDialog.open()}]},{label:this._localize("device.section_automations"),desc:this._localize("device.section_automations_desc"),icon:el.I.automations,items:r,category:"automation",actions:[{label:this._localize("device.add_automation"),icon:el.I.automations,onClick:()=>this._addAutomationDialog.open()},{label:this._localize("device.add_script"),icon:"script-text-outline",onClick:()=>this._addScriptDialog.open()}]}];if(this.readonly)for(let e of n)Object.assign(e,{actions:[],desc:""});let s=this._resolveLabels(e,this._caches.tick,this.platform,this.deviceName,this._localize),l=this._query.trim(),d=l.length>0,c=d?s.map(e=>e.filter(({item:e,labels:t})=>(0,V.K)(l,t.primary,t.secondary,e.id,e.name))):null,p=n.reduce((e,t)=>e+t.items.length,0),h=this._expertMode&&(p>=15||this._searchOpen),m=this._expertMode&&(this._searchOpen||d),f=c?c.reduce((e,t)=>e+t.length,0):0,_=d&&f>0?this._localize("device.navigator_search_count",{count:f,total:p}):"";return(0,a.qy)`
      <section class="card" ${(0,v.Wf)(this.tourAnchorId)}>
        <esphome-add-config-dialog
          .boardName=${this.boardName}
          .configuration=${this.configuration}
          .platform=${this.platform}
          .board=${this.board}
          .yaml=${this.yaml}
        ></esphome-add-config-dialog>
        <esphome-add-component-dialog
          .boardName=${this.boardName}
          .configuration=${this.configuration}
          .platform=${this.platform}
          .board=${this.board}
          .yaml=${this.yaml}
        ></esphome-add-component-dialog>
        <esphome-add-automation-dialog
          .boardName=${this.boardName}
          .configuration=${this.configuration}
          .board=${this.board}
          .yaml=${this.yaml}
          @automation-added=${this._onAutomationAdded}
        ></esphome-add-automation-dialog>
        <esphome-add-script-dialog
          .boardName=${this.boardName}
          .configuration=${this.configuration}
          .board=${this.board}
          .yaml=${this.yaml}
          @automation-added=${this._onAutomationAdded}
        ></esphome-add-script-dialog>
        <header class="card-header">
          <h2 class="card-title truncate">
            ${this._localize(this.readonly?"device.navigator_title_file":"device.navigator_title")}
          </h2>
          <div class="header-actions">
            ${h?(0,a.qy)`<button
                    type="button"
                    class="ghost-icon-btn search-btn"
                    aria-pressed=${m}
                    @click=${this._toggleSearch}
                    title=${this._localize("device.navigator_search_toggle")}
                    aria-label=${this._localize("device.navigator_search_toggle")}
                  >
                    <wa-icon library="mdi" name="magnify"></wa-icon>
                  </button>`:a.s6}
            <button
              type="button"
              class="ghost-icon-btn collapse-btn"
              @click=${this._onCollapseClick}
              title=${this._localize("device.hide_navigator")}
              aria-label=${this._localize("device.hide_navigator")}
            >
              <wa-icon library="mdi" name="menu"></wa-icon>
            </button>
          </div>
        </header>
        <div class="card-body">
          <esphome-navigator-search
            ?hidden=${!m}
            .value=${this._query}
            .resultLabel=${_}
            @navigator-search=${this._onSearchChange}
          ></esphome-navigator-search>
          ${d?a.s6:(0,a.qy)`<p class="italic">
                  ${this._localize(this.readonly?"device.navigator_desc_file":"device.navigator_desc")}
                </p>`}
          <div class="separator"></div>
          ${d&&0===f?(0,a.qy)`<p class="nav-empty" role="status">
                  ${this._localize("device.navigator_search_none")}
                </p>`:n.map(({label:e,desc:t,icon:i,category:r,actions:n},l)=>{var p;let h=c?.[l]??s[l];return(p={label:e,desc:t,icon:i,actions:n,rows:h,groups:"component"===r?this._groupComponents(h):void 0,isGroupOpen:o,onSetGroupOpen:(e,t)=>this._setGroupOpen(e,t),open:!!d||this.openSections.has(l),filtering:d,selectedLine:this._selectedLine,hoveredLine:this._hoveredLine,tourAnchorId:0===l&&this.tourAnchorId?this.classList.contains("drawer-nav")?"nav-mobile-core":"nav-core":void 0,errorCount:this.errorCounts.size?e=>this.errorCounts.get((0,u.pA)((0,g.gU)(e),e.fromLine))??0:void 0,errorLabel:e=>this._localize("device.navigator_error_count",{count:e}),onToggle:()=>{d||this._toggleSection(l)},onItemEnter:e=>this._onItemHover(e.fromLine,e.fromLine,e.toLine),onItemLeave:()=>this._onItemLeave(),onItemClick:e=>this._onItemClick(e)}).filtering&&0===p.rows.length?a.s6:(0,a.qy)`
    <div
      class="nav-content"
      role=${(0,E.J)(p.filtering?void 0:"button")}
      tabindex=${(0,E.J)(p.filtering?void 0:"0")}
      aria-expanded=${(0,E.J)(p.filtering?void 0:p.open?"true":"false")}
      ${(0,v.Wf)(p.tourAnchorId)}
      @click=${p.filtering?void 0:p.onToggle}
      @keydown=${p.filtering?void 0:B}
    >
      <div class="nav-content-label">
        <wa-icon library="mdi" name=${p.icon}></wa-icon>
        <p>${p.label}</p>
      </div>
      ${p.filtering?a.s6:(0,a.qy)`<wa-icon
              class="nav-content-chevron"
              library="mdi"
              name=${p.open?"chevron-up":"chevron-down"}
            ></wa-icon>`}
    </div>
    ${p.open?(0,a.qy)`
            <div class="separator"></div>
            ${p.filtering||!p.desc?a.s6:(0,a.qy)`<p class="italic">${p.desc}</p>`}
            ${p.groups?p.groups.map(e=>{var t,i,r,o;let n,s,l,d,c,u;return(t=e.rows.length,i=e.rows[0].item,1!==t||i.platform)?(r=e,n=(o=p).filtering||o.isGroupOpen(r.key),s=!o.filtering,l=o.errorCount,d=!n&&l?r.rows.reduce((e,t)=>e+l(t.item),0):0,c=()=>{s&&o.onSetGroupOpen(r.key,!n)},u=`navgroup-${r.key}`,(0,a.qy)`
    <div
      class="nav-subgroup-header ${s?"":"nav-subgroup-header--static"}"
      role=${(0,E.J)(s?"button":void 0)}
      tabindex=${(0,E.J)(s?"0":void 0)}
      aria-expanded=${(0,E.J)(s?String(n):void 0)}
      aria-controls=${(0,E.J)(s?u:void 0)}
      @click=${c}
      @keydown=${e=>{s&&("Enter"===e.key||" "===e.key)&&(e.preventDefault(),c())}}
    >
      ${(0,P.R)(R[r.key]??L,"nav-subgroup-icon")}
      <span class="nav-subgroup-title">${M(r.key)}</span>
      <span class="nav-subgroup-count">${r.rows.length}</span>
      ${d>0?T(d,o):a.s6}
      ${s?n?N:D:a.s6}
    </div>
    ${n?(0,a.qy)`<div id=${u} class="nav-items nav-items--grouped">
            ${r.rows.map(e=>j(e,o,!1))}
          </div>`:a.s6}
  `):(0,a.qy)`<div class="nav-items nav-items--single">
    ${j(e.rows[0],p,!0)}
  </div>`}):p.rows.length>0?(0,a.qy)`<div class="nav-items">
                      ${p.rows.map(e=>j(e,p,!0))}
                    </div>`:a.s6}
            ${p.filtering?a.s6:(0,a.qy)`<div class="nav-items">
                    ${p.actions.map(e=>(0,a.qy)`<div class="action-item" @click=${()=>e.onClick()}>
    <div>
      <wa-icon library="mdi" name=${e.icon}></wa-icon>
      <p>${e.label}</p>
    </div>
    <wa-icon library="mdi" name="plus-circle-outline"></wa-icon>
  </div>`)}
                  </div>`}
          `:a.s6}
    <div class="separator"></div>
  `})}
        </div>
      </section>
    `}_toggleSection(e){(0,m.r)(this,"section-toggle",{index:e})}_setGroupOpen(e,t){let i=new Set(this._collapsedGroups);t?i.delete(e):i.add(e),this._collapsedGroups=i}_kickoffNameResolves(){if(!this._api)return;let{core:e,components:t}=this._buckets(),i=this.platform||void 0;for(let r of[...e,...t]){let e=(0,g.gU)(r);void 0===(0,h.CQ)(e,i)&&(0,h.Sn)(this._api,e,i).catch(()=>{})}this._triggerCatalog.ensure()}_onItemHover(e,t,i){this._hoveredLine=e,this._emitHighlight({fromLine:t,toLine:i},!1)}_onItemLeave(){this._hoveredLine=null,this._emitHighlight(this._selectedRange,!1)}_onItemClick(e){let{fromLine:t,toLine:i}=e,r=(0,g.gU)(e);this._selectedLine===t?(this.selectedKey=null,this._selectedLine=null,this._selectedRange=null,this._emitHighlight(this._hoveredLine===t?{fromLine:t,toLine:i}:null,!1),this._emitSectionSelect(null,void 0)):(this.selectedKey=r,this._selectedLine=t,this._selectedRange={fromLine:t,toLine:i},this._emitHighlight({fromLine:t,toLine:i},!0),this._emitSectionSelect(r,t))}_emitHighlight(e,t){(0,m.r)(this,"yaml-highlight",{range:e,scroll:t})}_emitSectionSelect(e,t){(0,m.r)(this,"section-select",{sectionKey:e,fromLine:t})}constructor(...e){super(...e),this._localize=e=>e,this._caches=new _(this,[h.Ej,p.z2]),this._triggerCatalog=new ed.Q(this,()=>({api:this._api,platform:this.platform||void 0,boardId:this.board?.id})),this._reveal=new K(this,()=>({selectedLine:this._selectedLine,buckets:this._buckets(),openSections:this.openSections,filtering:this._query.trim().length>0})),this.openSections=new Set,this.yaml="",this._deriveBuckets=(0,s.A)(x),this._catalogIndex=new y.C(this,()=>this._api),this._groupComponents=(0,s.A)($),this._resolveLabels=(0,s.A)((e,t,i,r,o)=>{var a;return a={triggerCatalog:this._triggerCatalog,platform:i,deviceName:r,localize:o,substitutions:e.substitutions},[e.core.map(e=>({item:e,labels:q(e,"core",a)})),e.components.map(e=>({item:e,labels:q(e,"component",a)})),e.automations.map(e=>({item:e,labels:q(e,"automation",a)}))]}),this.board=null,this.boardName="",this.configuration="",this.deviceName="",this.platform="",this.platformReady=!1,this.readonly=!1,this.selectedKey=null,this.errorCounts=new Map,this._selectedLine=null,this._selectedRange=null,this._hoveredLine=null,this._expertMode=!1,this._query="",this._searchOpen=!1,this._collapsedGroups=new Set,this._onSearchChange=e=>{this._query=e.detail.value},this._toggleSearch=()=>{if(this._searchOpen||this._query){this._searchOpen=!1,this._query="";return}this._searchOpen=!0,this.updateComplete.then(()=>this._search?.focusInput())},this._onCollapseClick=()=>{(0,m.r)(this,"nav-collapse")},this._onAutomationAdded=e=>{(e.stopPropagation(),e.detail.configuration!==this.configuration)?console.warn("Dropped automation-added for",e.detail.configuration,"while showing",this.configuration):this._emitSectionSelect(e.detail.sectionKey,void 0)}}}ep.styles=[d.G9,c.U,b],ec([(0,r.Fg)({context:l.$F,subscribe:!0}),(0,n.wk)()],ep.prototype,"_localize",void 0),ec([(0,r.Fg)({context:l.Ie})],ep.prototype,"_api",void 0),ec([(0,n.MZ)({attribute:!1})],ep.prototype,"openSections",void 0),ec([(0,n.MZ)({attribute:!1})],ep.prototype,"tourAnchorId",void 0),ec([(0,n.MZ)({attribute:!1})],ep.prototype,"yaml",void 0),ec([(0,n.MZ)({attribute:!1})],ep.prototype,"board",void 0),ec([(0,n.MZ)()],ep.prototype,"boardName",void 0),ec([(0,n.MZ)()],ep.prototype,"configuration",void 0),ec([(0,n.MZ)()],ep.prototype,"deviceName",void 0),ec([(0,n.MZ)()],ep.prototype,"platform",void 0),ec([(0,n.MZ)({type:Boolean})],ep.prototype,"platformReady",void 0),ec([(0,n.MZ)({type:Boolean})],ep.prototype,"readonly",void 0),ec([(0,n.P)("esphome-add-config-dialog")],ep.prototype,"_addConfigDialog",void 0),ec([(0,n.P)("esphome-add-component-dialog")],ep.prototype,"_addComponentDialog",void 0),ec([(0,n.P)("esphome-add-automation-dialog")],ep.prototype,"_addAutomationDialog",void 0),ec([(0,n.P)("esphome-add-script-dialog")],ep.prototype,"_addScriptDialog",void 0),ec([(0,n.P)("esphome-navigator-search")],ep.prototype,"_search",void 0),ec([(0,n.MZ)({attribute:!1})],ep.prototype,"selectedKey",void 0),ec([(0,n.MZ)({attribute:!1})],ep.prototype,"selectedFromLine",void 0),ec([(0,n.MZ)({attribute:!1})],ep.prototype,"errorCounts",void 0),ec([(0,n.wk)()],ep.prototype,"_selectedLine",void 0),ec([(0,n.wk)()],ep.prototype,"_selectedRange",void 0),ec([(0,n.wk)()],ep.prototype,"_hoveredLine",void 0),ec([(0,r.Fg)({context:l.Pt,subscribe:!0}),(0,n.wk)()],ep.prototype,"_expertMode",void 0),ec([(0,n.wk)()],ep.prototype,"_query",void 0),ec([(0,n.wk)()],ep.prototype,"_searchOpen",void 0),ec([(0,n.wk)()],ep.prototype,"_collapsedGroups",void 0),ec([(0,n.EM)("esphome-device-navigator")],ep)},2311(e,t,i){var r=i(8041),o=i(7491);i.d(t,{},{K:function(e,t,i,a,n){let s=(0,r.lX)(i,n);(0,o.IL)(e,"yaml-draft",{configuration:t,yaml:s,basedOn:i,node:e}),e.dispatchEvent(new CustomEvent("automation-added",{detail:{configuration:t,sectionKey:(0,r.Ks)(a)},bubbles:!0,composed:!0}))}})},4267(e,t,i){var r=i(5077);let o=(0,r.AH)`
  /* Brief glow when navigated to from the YAML cursor — mirrors the
     dashboard's just-added card flash. */
  .field--highlight {
    animation: field-highlight-glow 2s ease-out 1;
  }
  @keyframes field-highlight-glow {
    0% {
      box-shadow: 0 0 0 0 color-mix(in srgb, var(--esphome-primary), transparent 40%);
    }
    50% {
      box-shadow: 0 0 0 6px color-mix(in srgb, var(--esphome-primary), transparent 70%);
    }
    100% {
      box-shadow: 0 0 0 0 color-mix(in srgb, var(--esphome-primary), transparent 100%);
    }
  }
  @media (prefers-reduced-motion: reduce) {
    .field--highlight {
      animation: none;
    }
  }
`;i.d(t,{},{h:o})},6567(e,t,i){let r="field--highlight";function o(e){window.matchMedia?.("(prefers-reduced-motion: reduce)").matches||(e.classList.remove(r),e.offsetWidth,e.classList.add(r),e.addEventListener("animationend",()=>e.classList.remove(r),{once:!0}))}i.d(t,{},{rK:o,uJ:function(e){e.scrollIntoView({block:"center"}),o(e)}})},7491(e,t,i){var r=i(3330);function o(e,t,i){(0,r.r)(e,t,i)}i.d(t,{},{IL:o,fb:function(e,t,i){let r=e.parentNode??i??null;return(i,a)=>{let n=i?e:r;i||!r||r.isConnected||console.warn(`Dispatching ${t} on a detached anchor; it may go nowhere`),n&&o(n,t,a)}},y5:function(e){let t=e.parentNode;return o(e,"section-mount",{node:e}),()=>o(t??e,"section-unmount",{node:e})}})},5494(e,t,i){var r=i(289),o=i(1093);let a={core:"cog-outline",components:"memory",automations:"arrow-decision-outline"};(0,o.C)({[a.core]:r.mdiCogOutline,[a.components]:r.mdiMemory,[a.automations]:r.mdiArrowDecisionOutline}),i.d(t,{},{I:a})},8144(e,t,i){var r=i(5077);let o=(0,r.AH)`
  .substitution-note {
    display: inline-flex;
    align-items: center;
    gap: var(--wa-space-2xs);
    margin-top: var(--wa-space-2xs);
    font-size: var(--wa-font-size-2xs);
    color: var(--wa-color-text-quiet);
  }

  .substitution-note wa-icon {
    font-size: 14px;
    color: var(--esphome-primary);
  }

  /* The "defined elsewhere" marker is a quiet heads-up, not a positive
     resolve, so its braces icon and text stay muted. */
  .substitution-note--external {
    color: var(--wa-color-text-quiet);
  }

  .substitution-note--external wa-icon {
    color: var(--wa-color-text-quiet);
  }

  /* …except the warning glyph, which signals the unresolved reference. */
  .substitution-note--external wa-icon.substitution-warn {
    color: var(--wa-color-warning-fill-loud, #b8860b);
  }

  .substitution-note code {
    font-family: ui-monospace, "SF Mono", Menlo, Consolas, monospace;
    font-size: var(--wa-font-size-2xs);
    padding: 1px 4px;
    border-radius: var(--wa-border-radius-s);
    background: var(--wa-color-surface-lowered);
    color: var(--wa-color-text-normal);
  }
`;i.d(t,{},{s:o})},7297(e,t,i){var r=i(5109),o=i(2353);i.d(t,{},{Q:class{hostConnected(){this._unsubscribe=(0,r.z2)(()=>this._host.requestUpdate())}hostDisconnected(){this._unsubscribe?.(),this._unsubscribe=void 0}ensure(){let{api:e,platform:t,boardId:i}=this._context();e&&void 0===(0,r.vM)(t,i)&&(0,r.R8)(e,t,i).catch(()=>{})}resolveName(e,t,i){let{platform:a,boardId:n}=this._context(),s=(0,r.vM)(a,n);if(!s)return i;let l=e.includes("esphome")?s.find(e=>e.id===t):(0,o.$Z)(s,e,t);return l?.name||i}hasTriggersFor(e){let{platform:t,boardId:i}=this._context(),o=(0,r.vM)(t,i);return!o||o.some(t=>(t.applies_to??[]).some(t=>e.includes(t)))}constructor(e,t){this._host=e,this._context=t,e.addController(this)}}})},5865(e,t,i){var r=i(5077);let o=(0,r.AH)`
  .intro {
    font-size: var(--wa-font-size-s);
    color: var(--wa-color-text-quiet);
    margin: 0 0 var(--wa-space-m) 0;
    line-height: 1.5;
  }
  .field-label {
    font-size: var(--wa-font-size-s);
    font-weight: var(--wa-font-weight-semibold);
    color: var(--wa-color-text-normal);
  }
  .required {
    color: var(--esphome-error, #d92d20);
  }
  .error {
    color: var(--esphome-error, #d92d20);
    font-size: var(--wa-font-size-2xs);
    margin-top: var(--wa-space-2xs);
  }
`;i.d(t,{},{h:o})},4323(e,t,i){var r=i(1746);function o(e){let t=e.replace(/_/g," ").trim();return t?t[0].toUpperCase()+t.slice(1):""}i.d(t,{},{t:function(e,t){let i=(0,r.Y)(e),a=String(i[i.length-1]??e),n=[];for(let e of i.slice(0,-1))"number"==typeof e?n[n.length-1]=`${n[n.length-1]} #${e+1}`:n.push(o(e));let s=t("device.action_field_label",{name:o((a.endsWith("_action")?a.slice(0,-7):a)||a)||"Action"});return[...n,s].join(" → ")}})},5242(e,t,i){i.d(t,{FG:()=>n,SN:()=>a,P0:()=>s});let r=new(i(2741)).E({name:"automation-body-cache",bucketKey:()=>"",cacheMisses:!1,fetch:(e,t)=>{let i=t.map(e=>{let t=e.indexOf("/");return{type:e.slice(0,t),id:e.slice(t+1)}});return e.getAutomationBodies(i)}});function o(e,t,i){return r.fetch(e,`${t}/${i}`,void 0)}async function a(e,t,i,r=o){let n=await r(e,t,i.id);if(n&&"config_entries"in n)return i.config_entries=structuredClone(n.config_entries),"required_groups"in n&&(i.required_groups=structuredClone(n.required_groups)),"ok";let s=null===n?"no body returned":"body shape missing config_entries";return console.warn(`automation-body: ${t}/${i.id} ${s}; form will render empty`),null===n?"missingBody":"missingField"}function n(){return{succeeded:0,missingBody:0,missingField:0,rejected:0}}function s(e,t){e["ok"===t?"succeeded":t]++}},5109(e,t,i){var r=i(5242),o=i(7064);function a(e,t){return`${e??""}|${t??""}`}let n={triggers:(0,o.Y)({name:"automation-catalog-cache:triggers",key:a,fetch:(e,t,i)=>e.getAutomationTriggers(t,i)}),actions:(0,o.Y)({name:"automation-catalog-cache:actions",key:a,fetch:(e,t,i)=>e.getAutomationActions(t,i)}),conditions:(0,o.Y)({name:"automation-catalog-cache:conditions",key:a,fetch:(e,t,i)=>e.getAutomationConditions(t,i)}),light_effects:(0,o.Y)({name:"automation-catalog-cache:light_effects",key:a,fetch:(e,t,i)=>e.getLightEffects(t,i)}),filters:(0,o.Y)({name:"automation-catalog-cache:filters",key:a,fetch:(e,t,i)=>e.getFilters(t,i)})};async function s(e,t,i,r,o){if(0===(await o(r)).succeeded)return r;let a=[...r];return n[e].update(a,t,i),a}let l=new WeakSet;async function d(e,t,i){let o=(0,r.FG)(),a=i.filter(e=>!l.has(e));if(0===a.length)return o;for(let i of(await Promise.allSettled(a.map(async i=>{let a=await (0,r.SN)(e,t,i);"ok"===a&&l.add(i),(0,r.P0)(o,a)}))))"rejected"===i.status&&(o.rejected++,console.warn(`${t} hydration failed`,i.reason));let n=o.missingBody+o.missingField+o.rejected;return n>0&&console.warn(`${t} hydration: ${o.succeeded} ok, ${n} failed (missingBody=${o.missingBody}, missingField=${o.missingField}, rejected=${o.rejected})`),o}i.d(t,{},{R8:function(e,t,i){return n.triggers.fetch(e,t,i)},VS:async function(e,t,i){let r=await n.light_effects.fetch(e,t,i);return s("light_effects",t,i,r,t=>d(e,"light_effects",t))},ac:function(e,t){return n.filters.getCached(e,t)},cQ:async function(e,t,i){let r=await n.filters.fetch(e,t,i);return s("filters",t,i,r,t=>d(e,"filters",t))},vM:function(e,t){return n.triggers.getCached(e,t)},xB:function(e,t){return n.light_effects.getCached(e,t)},z2:function(e){let t=Object.values(n).map(t=>t.subscribe(e));return()=>{for(let e of t)e()}}})},2943(e,t,i){var r=i(4008),o=i(271),a=i(8851);function n(e){let t=e.trim();if(""===t)return"";let i=Number(t);return Number.isFinite(i)?i:t}i.d(t,{},{Ae:function(e,t){return"int"===e?(0,o.s)(t):"float"===e?n(t):t},aY:function(e,t){if(e.type===r.Hh.INTEGER)return(0,o.s)(t);if(e.type===r.Hh.FLOAT)return n(t);if(e.type===r.Hh.BOOLEAN){let e=t.trim();return""===e?"":(0,a.FY)(e)??e}return t},pz:n})},9995(e,t,i){i.d(t,{},{m:function(e){return e.replace(/ (Component|Configuration)$/,"")||e}})},7181(e,t,i){var r=i(565),o=i(8175),a=i(8851);let n=/^\*\*(Required —|Set at most one of:|Set together)/;function s(e){return(0,o.Qd)(e)?(0,a.$z)(e):(0,r.rf)(e)}i.d(t,{},{$J:function(e,t,i){let r=t.filter(e=>s(i[e])).length;switch(e){case"exactly_one":return 1===r;case"at_least_one":return r>=1;case"at_most_one":return r<=1;case"none_or_all":case"all_or_none":return 0===r||r===t.length}},IT:function e(t,i,r=[],o=!0,a=new Set){let n=new Set(i.flatMap(e=>e.keys));for(let i of t){let t=[...r,i.key];o&&(i.group||n.has(i.key))&&a.add(t.join("."));let s=i.config_entries;s?.length&&e(s,i.required_groups??[],t,!i.multi_value,a)}return a},PX:function(e){if(!e.startsWith("**"))return e;let t=e.split("\n\n"),i=0;for(;i<t.length&&n.test(t[i].trim());)i++;return t.slice(i).join("\n\n").trim()},VM:s,Wy:function(e){return e.filter(e=>!(0,o.wr)(e)).join(".")}})},6092(e,t,i){var r=i(664),o=i(5795),a=i(2765),n=i(1150),s=i(8851);let l=/^(?:[a-z0-9_]+_)?id$/,d=/^\s+(?:-\s+)?((?:[a-z0-9_]+_)?id):/;function c(e,t){let i=(0,r.e)(e.toLowerCase()),o=(0,r.t)(i)?i:`_${i}`,a=1;for(;t.has(`${o}_${a}`);)a++;return`${o}_${a}`}i.d(t,{},{Fc:function e(t,i){if(t&&"object"==typeof t&&!(t instanceof s.ho))for(let[r,o]of Object.entries(t))"string"==typeof o&&o&&l.test(r)&&i.add(o),e(o,i)},T6:function(e,t){return c(e,t)},Y0:function(e){let t=new Set;for(let i of(0,a.D)(e)){let e=i.match(d)?.[1];if(void 0===e)continue;let r=(0,n.K)(i,e);null!==r&&t.add(r)}return t},fW:function(e,t,i){return t||(0,o.K8)(e)?c(e,i):null},gO:function(e){return(0,n.p)(e,"id")}})},5217(e,t,i){i.d(t,{},{k:function(e,t){return t?e.find(e=>e.configuration===t)?.name??"":""}})},9508(e,t,i){i.d(t,{},{H:function(e,t){if(e.translation_key){let i=e.translation_params||void 0,r=t(e.translation_key,i);if(r&&r!==e.translation_key)return r}return e.label?e.label:e.key.split("_").map(e=>e?e[0].toUpperCase()+e.slice(1):e).join(" ")}})},2919(e,t,i){var r=i(874);i.d(t,{},{H:function(e,t,i){if(0===i.length||!(0,r.im)(t))return e;let o=new Set(e);for(let e of i)o.add(e);return o}})},6670(e,t,i){var r=i(874),o=i(2930),a=i(2342),n=i(7064);let s=new a.e,l=(0,n.Y)({name:"interface-providers",key:e=>e,fetch:(e,t)=>(0,o._)(e,{provides:t}).then(e=>e.map(e=>(0,r.G_)(e,t))).catch(e=>{throw console.warn("[provides-cache] provider fetch failed for",t,e),e})});i.d(t,{},{Qk:function(e){return l.getCached(e)},em:function(e,t){return l.fetch(e,t)},wI:function(e,t,i,r){let a=`${t}|${i??""}|${r??""}`;return s.fetch(a,()=>(0,o._)(e,{provides:t,platform:i??void 0,board_id:r??void 0}).then(e=>new Set(e.map(e=>e.id))))},y_:function(e){return l.subscribe(e)}})},7228(e,t,i){i.d(t,{},{j:async function(e,t,i){let{created:r}=await e.setSecret(t,i,!1);return r&&window.dispatchEvent(new CustomEvent("secrets-saved")),{created:r}},x:async function(e,t,i){await e.setSecret(t,i,!0),window.dispatchEvent(new CustomEvent("secrets-saved"))}})},2(e,t,i){var r=i(8175);let o=["us","ms","s","min","h","d"];function a(e,t){let i=o.indexOf(e);return i<=0?o:o.filter((e,r)=>r>=i||e===t)}let n={us:"us",µs:"us",microseconds:"us",ms:"ms",milliseconds:"ms",s:"s",sec:"s",seconds:"s",min:"min",minutes:"min",h:"h",hours:"h",d:"d",days:"d"},s=Object.keys(n).map(e=>e.replace(/[.*+?^${}()|[\]\\]/g,"\\$&")).join("|"),l=RegExp(`^(\\d+(?:\\.\\d+)?)\\s*(${s})?$`),d=RegExp(`^\\d+(?:\\.\\d+)?\\s*(?:${s})$`);function c(e){return"string"==typeof e&&d.test(e.trim())}let p={microseconds:"us",milliseconds:"ms",seconds:"s",minutes:"min",hours:"h",days:"d"};i.d(t,{},{Hb:function(e){if(!(0,r.Qd)(e))return!1;let t=Object.keys(e);return t.length>0&&t.every(e=>Object.prototype.hasOwnProperty.call(p,e))},QH:c,cU:function(e,t){return a(t).includes(e)?e:t},gF:function(e){if(null==e||""===e)return{value:"",unit:"s",parseable:!0,unitless:!1};let t=String(e).trim(),i=t.match(l);if(i){let[,e,t]=i;return{value:e,unit:t?n[t]:"s",parseable:!0,unitless:!t}}return{value:t,unit:"s",parseable:!1,unitless:!1}},n9:function(e,t){let i=e.trim();return""===i?"":`${i}${t}`},nh:function(e){if(!(0,r.Qd)(e))return null;let t=Object.keys(e);if(1!==t.length||!Object.prototype.hasOwnProperty.call(p,t[0]))return null;let i=e[t[0]];if("number"!=typeof i&&"string"!=typeof i)return null;let o=`${String(i).trim()}${p[t[0]]}`;return c(o)?o:null},ze:a})},2353(e,t,i){var r=i(874),o=i(4125);function a(e){return e.slice(e.lastIndexOf(".")+1)}function n(e,t){return!e.is_device_level&&(e.applies_to??[]).some(e=>t.includes(e))}i.d(t,{},{$Z:function(e,t,i){for(let r of t){let t=e.find(e=>a(e.id)===i&&n(e,[r]));if(t)return t}},PM:function(e){return e.is_entity_container?[e.component_id]:function(e){let{domain:t}=(0,r.iZ)(e);return t===e?[e]:[e,t]}(e.component_id)},Qf:n,y1:a,yZ:function(e,t){return t?[(0,o.T0)(e,t),e]:[e]}})}}]);
//# sourceMappingURL=386.72657005e71167d5.js.map