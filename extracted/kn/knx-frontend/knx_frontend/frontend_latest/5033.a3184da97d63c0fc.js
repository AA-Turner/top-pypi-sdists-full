export const __webpack_ids__=["5033"];export const __webpack_modules__={31298:function(e,t,o){o.d(t,{C:()=>i});var n=o(93318);const i=e=>{return t=e.entity_id,void 0===(o=e.attributes).friendly_name?(0,n.p)(t).replace(/_/g," "):(o.friendly_name??"").toString();var t,o}},88381:function(e,t,o){o.r(t),o.d(t,{HaConversationAgentSelector:()=>$});var n=o(73742),i=o(59048),a=o(7616),s=o(29740),r=o(41806),l=o(16811),d=o(51068),c=o(59753),p=o(47469);const u=(e,t)=>e.callApi("POST","config/config_entries/options/flow",{handler:t,show_advanced_options:Boolean(e.userData?.showAdvanced)}),h=(e,t)=>e.callApi("GET",`config/config_entries/options/flow/${t}`),_=(e,t,o)=>e.callApi("POST",`config/config_entries/options/flow/${t}`,o),g=(e,t)=>e.callApi("DELETE",`config/config_entries/options/flow/${t}`);var m=o(90558);o(93795),o(29490);var v=o(28203);const y="__NONE_OPTION__";class f extends i.oi{render(){if(!this._agents)return i.Ld;let e=this.value;if(!e&&this.required){for(const t of this._agents)if("conversation.home_assistant"===t.id&&t.supported_languages.includes(this.language)){e=t.id;break}if(!e)for(const t of this._agents)if("*"===t.supported_languages&&t.supported_languages.includes(this.language)){e=t.id;break}}return e||(e=y),i.dy`
      <ha-select
        .label=${this.label||this.hass.localize("ui.components.coversation-agent-picker.conversation_agent")}
        .value=${e}
        .required=${this.required}
        .disabled=${this.disabled}
        @selected=${this._changed}
        @closed=${r.U}
        fixedMenuPosition
        naturalMenuWidth
      >
        ${this.required?i.Ld:i.dy`<ha-list-item .value=${y}>
              ${this.hass.localize("ui.components.coversation-agent-picker.none")}
            </ha-list-item>`}
        ${this._agents.map((e=>i.dy`<ha-list-item
              .value=${e.id}
              .disabled=${"*"!==e.supported_languages&&0===e.supported_languages.length}
            >
              ${e.name}
            </ha-list-item>`))}</ha-select
      >${this._configEntry?.supports_options?i.dy`<ha-icon-button
            .path=${"M12,15.5A3.5,3.5 0 0,1 8.5,12A3.5,3.5 0 0,1 12,8.5A3.5,3.5 0 0,1 15.5,12A3.5,3.5 0 0,1 12,15.5M19.43,12.97C19.47,12.65 19.5,12.33 19.5,12C19.5,11.67 19.47,11.34 19.43,11L21.54,9.37C21.73,9.22 21.78,8.95 21.66,8.73L19.66,5.27C19.54,5.05 19.27,4.96 19.05,5.05L16.56,6.05C16.04,5.66 15.5,5.32 14.87,5.07L14.5,2.42C14.46,2.18 14.25,2 14,2H10C9.75,2 9.54,2.18 9.5,2.42L9.13,5.07C8.5,5.32 7.96,5.66 7.44,6.05L4.95,5.05C4.73,4.96 4.46,5.05 4.34,5.27L2.34,8.73C2.21,8.95 2.27,9.22 2.46,9.37L4.57,11C4.53,11.34 4.5,11.67 4.5,12C4.5,12.33 4.53,12.65 4.57,12.97L2.46,14.63C2.27,14.78 2.21,15.05 2.34,15.27L4.34,18.73C4.46,18.95 4.73,19.03 4.95,18.95L7.44,17.94C7.96,18.34 8.5,18.68 9.13,18.93L9.5,21.58C9.54,21.82 9.75,22 10,22H14C14.25,22 14.46,21.82 14.5,21.58L14.87,18.93C15.5,18.67 16.04,18.34 16.56,17.94L19.05,18.95C19.27,19.03 19.54,18.95 19.66,18.73L21.66,15.27C21.78,15.05 21.73,14.78 21.54,14.63L19.43,12.97Z"}
            @click=${this._openOptionsFlow}
          ></ha-icon-button>`:""}
    `}willUpdate(e){super.willUpdate(e),this.hasUpdated?e.has("language")&&this._debouncedUpdateAgents():this._updateAgents(),e.has("value")&&this._maybeFetchConfigEntry()}async _maybeFetchConfigEntry(){if(this.value&&this.value in this.hass.entities)try{const e=await(0,v.L3)(this.hass,this.value);if(!e.config_entry_id)return void(this._configEntry=void 0);this._configEntry=(await(0,d.RQ)(this.hass,e.config_entry_id)).config_entry}catch(e){this._configEntry=void 0}else this._configEntry=void 0}async _updateAgents(){const{agents:e}=await(0,c.rM)(this.hass,this.language,this.hass.config.country||void 0);if(this._agents=e,!this.value)return;const t=e.find((e=>e.id===this.value));(0,s.B)(this,"supported-languages-changed",{value:t?.supported_languages}),(!t||"*"!==t.supported_languages&&0===t.supported_languages.length)&&(this.value=void 0,(0,s.B)(this,"value-changed",{value:this.value}))}async _openOptionsFlow(){var e,t,o;this._configEntry&&(e=this,t=this._configEntry,o={manifest:await(0,p.t4)(this.hass,this._configEntry.domain)},(0,m.w)(e,{startFlowHandler:t.entry_id,domain:t.domain,...o},{flowType:"options_flow",showDevices:!1,createFlow:async(e,o)=>{const[n]=await Promise.all([u(e,o),e.loadFragmentTranslation("config"),e.loadBackendTranslation("options",t.domain),e.loadBackendTranslation("selector",t.domain)]);return n},fetchFlow:async(e,o)=>{const[n]=await Promise.all([h(e,o),e.loadFragmentTranslation("config"),e.loadBackendTranslation("options",t.domain),e.loadBackendTranslation("selector",t.domain)]);return n},handleFlowStep:_,deleteFlow:g,renderAbortDescription(e,o){const n=e.localize(`component.${o.translation_domain||t.domain}.options.abort.${o.reason}`,o.description_placeholders);return n?i.dy`
              <ha-markdown
                breaks
                allow-svg
                .content=${n}
              ></ha-markdown>
            `:o.reason},renderShowFormStepHeader(e,o){return e.localize(`component.${o.translation_domain||t.domain}.options.step.${o.step_id}.title`,o.description_placeholders)||e.localize("ui.dialogs.options_flow.form.header")},renderShowFormStepDescription(e,o){const n=e.localize(`component.${o.translation_domain||t.domain}.options.step.${o.step_id}.description`,o.description_placeholders);return n?i.dy`
              <ha-markdown
                allow-svg
                breaks
                .content=${n}
              ></ha-markdown>
            `:""},renderShowFormStepFieldLabel(e,o,n,i){if("expandable"===n.type)return e.localize(`component.${t.domain}.options.step.${o.step_id}.sections.${n.name}.name`,o.description_placeholders);const a=i?.path?.[0]?`sections.${i.path[0]}.`:"";return e.localize(`component.${t.domain}.options.step.${o.step_id}.${a}data.${n.name}`,o.description_placeholders)||n.name},renderShowFormStepFieldHelper(e,o,n,a){if("expandable"===n.type)return e.localize(`component.${o.translation_domain||t.domain}.options.step.${o.step_id}.sections.${n.name}.description`,o.description_placeholders);const s=a?.path?.[0]?`sections.${a.path[0]}.`:"",r=e.localize(`component.${o.translation_domain||t.domain}.options.step.${o.step_id}.${s}data_description.${n.name}`,o.description_placeholders);return r?i.dy`<ha-markdown breaks .content=${r}></ha-markdown>`:""},renderShowFormStepFieldError(e,o,n){return e.localize(`component.${o.translation_domain||t.domain}.options.error.${n}`,o.description_placeholders)||n},renderShowFormStepFieldLocalizeValue(e,o,n){return e.localize(`component.${t.domain}.selector.${n}`)},renderShowFormStepSubmitButton(e,o){return e.localize(`component.${t.domain}.options.step.${o.step_id}.submit`)||e.localize("ui.panel.config.integrations.config_flow."+(!1===o.last_step?"next":"submit"))},renderExternalStepHeader(e,t){return""},renderExternalStepDescription(e,t){return""},renderCreateEntryDescription(e,t){return i.dy`
          <p>${e.localize("ui.dialogs.options_flow.success.description")}</p>
        `},renderShowFormProgressHeader(e,o){return e.localize(`component.${t.domain}.options.step.${o.step_id}.title`)||e.localize(`component.${t.domain}.title`)},renderShowFormProgressDescription(e,o){const n=e.localize(`component.${o.translation_domain||t.domain}.options.progress.${o.progress_action}`,o.description_placeholders);return n?i.dy`
              <ha-markdown
                allow-svg
                breaks
                .content=${n}
              ></ha-markdown>
            `:""},renderMenuHeader(e,o){return e.localize(`component.${t.domain}.options.step.${o.step_id}.title`)||e.localize(`component.${t.domain}.title`)},renderMenuDescription(e,o){const n=e.localize(`component.${o.translation_domain||t.domain}.options.step.${o.step_id}.description`,o.description_placeholders);return n?i.dy`
              <ha-markdown
                allow-svg
                breaks
                .content=${n}
              ></ha-markdown>
            `:""},renderMenuOption(e,o,n){return e.localize(`component.${o.translation_domain||t.domain}.options.step.${o.step_id}.menu_options.${n}`,o.description_placeholders)},renderLoadingDescription(e,o){return e.localize(`component.${t.domain}.options.loading`)||("loading_flow"===o||"loading_step"===o?e.localize(`ui.dialogs.options_flow.loading.${o}`,{integration:(0,p.Lh)(e.localize,t.domain)}):"")}}))}_changed(e){const t=e.target;!this.hass||""===t.value||t.value===this.value||void 0===this.value&&t.value===y||(this.value=t.value===y?void 0:t.value,(0,s.B)(this,"value-changed",{value:this.value}),(0,s.B)(this,"supported-languages-changed",{value:this._agents.find((e=>e.id===this.value))?.supported_languages}))}constructor(...e){super(...e),this.disabled=!1,this.required=!1,this._debouncedUpdateAgents=(0,l.D)((()=>this._updateAgents()),500)}}f.styles=i.iv`
    :host {
      display: flex;
      align-items: center;
    }
    ha-select {
      width: 100%;
    }
    ha-icon-button {
      color: var(--secondary-text-color);
    }
  `,(0,n.__decorate)([(0,a.Cb)()],f.prototype,"value",void 0),(0,n.__decorate)([(0,a.Cb)()],f.prototype,"language",void 0),(0,n.__decorate)([(0,a.Cb)()],f.prototype,"label",void 0),(0,n.__decorate)([(0,a.Cb)({attribute:!1})],f.prototype,"hass",void 0),(0,n.__decorate)([(0,a.Cb)({type:Boolean,reflect:!0})],f.prototype,"disabled",void 0),(0,n.__decorate)([(0,a.Cb)({type:Boolean})],f.prototype,"required",void 0),(0,n.__decorate)([(0,a.SB)()],f.prototype,"_agents",void 0),(0,n.__decorate)([(0,a.SB)()],f.prototype,"_configEntry",void 0),f=(0,n.__decorate)([(0,a.Mo)("ha-conversation-agent-picker")],f);class $ extends i.oi{render(){return i.dy`<ha-conversation-agent-picker
      .hass=${this.hass}
      .value=${this.value}
      .language=${this.selector.conversation_agent?.language||this.context?.language}
      .label=${this.label}
      .helper=${this.helper}
      .disabled=${this.disabled}
      .required=${this.required}
    ></ha-conversation-agent-picker>`}constructor(...e){super(...e),this.disabled=!1,this.required=!0}}$.styles=i.iv`
    ha-conversation-agent-picker {
      width: 100%;
    }
  `,(0,n.__decorate)([(0,a.Cb)({attribute:!1})],$.prototype,"hass",void 0),(0,n.__decorate)([(0,a.Cb)({attribute:!1})],$.prototype,"selector",void 0),(0,n.__decorate)([(0,a.Cb)()],$.prototype,"value",void 0),(0,n.__decorate)([(0,a.Cb)()],$.prototype,"label",void 0),(0,n.__decorate)([(0,a.Cb)()],$.prototype,"helper",void 0),(0,n.__decorate)([(0,a.Cb)({type:Boolean})],$.prototype,"disabled",void 0),(0,n.__decorate)([(0,a.Cb)({type:Boolean})],$.prototype,"required",void 0),(0,n.__decorate)([(0,a.Cb)({attribute:!1})],$.prototype,"context",void 0),$=(0,n.__decorate)([(0,a.Mo)("ha-selector-conversation_agent")],$)},59753:function(e,t,o){o.d(t,{KH:()=>a,rM:()=>i,zt:()=>n});var n=function(e){return e[e.CONTROL=1]="CONTROL",e}({});const i=(e,t,o)=>e.callWS({type:"conversation/agent/list",language:t,country:o}),a=(e,t,o)=>e.callWS({type:"conversation/agent/homeassistant/language_scores",language:t,country:o})},28203:function(e,t,o){o.d(t,{CL:()=>m,Iq:()=>d,L3:()=>l,LM:()=>h,Mw:()=>g,Nv:()=>c,vA:()=>r,w1:()=>_});var n=o(88865),i=o(28105),a=o(31298),s=(o(92949),o(16811));const r=(e,t)=>{if(t.name)return t.name;const o=e.states[t.entity_id];return o?(0,a.C)(o):t.original_name?t.original_name:t.entity_id},l=(e,t)=>e.callWS({type:"config/entity_registry/get",entity_id:t}),d=(e,t)=>e.callWS({type:"config/entity_registry/get_entries",entity_ids:t}),c=(e,t,o)=>e.callWS({type:"config/entity_registry/update",entity_id:t,...o}),p=e=>e.sendMessagePromise({type:"config/entity_registry/list"}),u=(e,t)=>e.subscribeEvents((0,s.D)((()=>p(e).then((e=>t.setState(e,!0)))),500,!0),"entity_registry_updated"),h=(e,t)=>(0,n.B)("_entityRegistry",p,u,e,t),_=(0,i.Z)((e=>{const t={};for(const o of e)t[o.entity_id]=o;return t})),g=(0,i.Z)((e=>{const t={};for(const o of e)t[o.id]=o;return t})),m=(e,t)=>e.callWS({type:"config/entity_registry/get_automatic_entity_ids",entity_ids:t})},47469:function(e,t,o){o.d(t,{F3:()=>i,Lh:()=>n,t4:()=>a});const n=(e,t,o)=>e(`component.${t}.title`)||o?.name||t,i=(e,t)=>{const o={type:"manifest/list"};return t&&(o.integrations=t),e.callWS(o)},a=(e,t)=>e.callWS({type:"manifest/get",integration:t})},90558:function(e,t,o){o.d(t,{w:()=>a});var n=o(29740);const i=()=>Promise.all([o.e("1753"),o.e("9641")]).then(o.bind(o,14723)),a=(e,t,o)=>{(0,n.B)(e,"show-dialog",{dialogTag:"dialog-data-entry-flow",dialogImport:i,dialogParams:{...t,flowConfig:o,dialogParentElement:e}})}},88865:function(e,t,o){o.d(t,{B:()=>a});const n=e=>{let t=[];function o(o,n){e=n?o:Object.assign(Object.assign({},e),o);let i=t;for(let t=0;t<i.length;t++)i[t](e)}return{get state(){return e},action(t){function n(e){o(e,!1)}return function(){let o=[e];for(let e=0;e<arguments.length;e++)o.push(arguments[e]);let i=t.apply(this,o);if(null!=i)return i instanceof Promise?i.then(n):n(i)}},setState:o,clearState(){e=void 0},subscribe(e){return t.push(e),()=>{!function(e){let o=[];for(let n=0;n<t.length;n++)t[n]===e?e=null:o.push(t[n]);t=o}(e)}}}},i=(e,t,o,i,a={unsubGrace:!0})=>{if(e[t])return e[t];let s,r,l=0,d=n();const c=()=>{if(!o)throw new Error("Collection does not support refresh");return o(e).then((e=>d.setState(e,!0)))},p=()=>c().catch((t=>{if(e.connected)throw t})),u=()=>{r=void 0,s&&s.then((e=>{e()})),d.clearState(),e.removeEventListener("ready",c),e.removeEventListener("disconnected",h)},h=()=>{r&&(clearTimeout(r),u())};return e[t]={get state(){return d.state},refresh:c,subscribe(t){l++,1===l&&(()=>{if(void 0!==r)return clearTimeout(r),void(r=void 0);i&&(s=i(e,d)),o&&(e.addEventListener("ready",p),p()),e.addEventListener("disconnected",h)})();const n=d.subscribe(t);return void 0!==d.state&&setTimeout((()=>t(d.state)),0),()=>{n(),l--,l||(a.unsubGrace?r=setTimeout(u,5e3):u())}}},e[t]},a=(e,t,o,n,a)=>i(n,e,t,o).subscribe(a)}};
//# sourceMappingURL=5033.a3184da97d63c0fc.js.map