/*! For license information please see 5171.807f06e7eeb8c486.js.LICENSE.txt */
"use strict";(self.webpackChunkknx_frontend=self.webpackChunkknx_frontend||[]).push([["5171"],{75972:function(t,e,i){i.a(t,(async function(t,a){try{i.d(e,{u:function(){return r}});var s=i(57900),o=i(28105),n=t([s]);s=(n.then?(await n)():n)[0];const r=(t,e)=>{try{var i,a;return null!==(i=null===(a=l(e))||void 0===a?void 0:a.of(t))&&void 0!==i?i:t}catch(s){return t}},l=(0,o.Z)((t=>new Intl.DisplayNames(t.language,{type:"language",fallback:"code"})));a()}catch(r){a(r)}}))},89395:function(t,e,i){i.d(e,{J:function(){return s},_:function(){return o}});i(81738),i(72489),i(64455),i(32192);const a=/{%|{{/,s=t=>a.test(t),o=t=>{if(!t)return!1;if("string"==typeof t)return s(t);if("object"==typeof t){return(Array.isArray(t)?t:Object.values(t)).some((t=>t&&o(t)))}return!1}},1893:function(t,e,i){i.d(e,{Q:function(){return a}});i(64455),i(6202);const a=t=>t.replace(/^_*(.)|_+(.)/g,((t,e,i)=>e?e.toUpperCase():" "+i.toUpperCase()))},69187:function(t,e,i){i.a(t,(async function(t,e){try{i(26847),i(81738),i(29981),i(6989),i(27530);var a=i(73742),s=i(59048),o=i(7616),n=i(29740),r=i(41806),l=i(75972),c=i(32518),d=(i(93795),i(29490),t([l]));l=(d.then?(await d)():d)[0];let h,u,p,v,_=t=>t;const g="preferred",b="last_used";class f extends s.oi{get _default(){return this.includeLastUsed?b:g}render(){var t,e;if(!this._pipelines)return s.Ld;const i=null!==(t=this.value)&&void 0!==t?t:this._default;return(0,s.dy)(h||(h=_`
      <ha-select
        .label=${0}
        .value=${0}
        .required=${0}
        .disabled=${0}
        @selected=${0}
        @closed=${0}
        fixedMenuPosition
        naturalMenuWidth
      >
        ${0}
        <ha-list-item .value=${0}>
          ${0}
        </ha-list-item>
        ${0}
      </ha-select>
    `),this.label||this.hass.localize("ui.components.pipeline-picker.pipeline"),i,this.required,this.disabled,this._changed,r.U,this.includeLastUsed?(0,s.dy)(u||(u=_`
              <ha-list-item .value=${0}>
                ${0}
              </ha-list-item>
            `),b,this.hass.localize("ui.components.pipeline-picker.last_used")):null,g,this.hass.localize("ui.components.pipeline-picker.preferred",{preferred:null===(e=this._pipelines.find((t=>t.id===this._preferredPipeline)))||void 0===e?void 0:e.name}),this._pipelines.map((t=>(0,s.dy)(p||(p=_`<ha-list-item .value=${0}>
              ${0}
              (${0})
            </ha-list-item>`),t.id,t.name,(0,l.u)(t.language,this.hass.locale)))))}firstUpdated(t){super.firstUpdated(t),(0,c.SC)(this.hass).then((t=>{this._pipelines=t.pipelines,this._preferredPipeline=t.preferred_pipeline}))}_changed(t){const e=t.target;!this.hass||""===e.value||e.value===this.value||void 0===this.value&&e.value===this._default||(this.value=e.value===this._default?void 0:e.value,(0,n.B)(this,"value-changed",{value:this.value}))}constructor(...t){super(...t),this.disabled=!1,this.required=!1,this.includeLastUsed=!1,this._preferredPipeline=null}}f.styles=(0,s.iv)(v||(v=_`
    ha-select {
      width: 100%;
    }
  `)),(0,a.__decorate)([(0,o.Cb)()],f.prototype,"value",void 0),(0,a.__decorate)([(0,o.Cb)()],f.prototype,"label",void 0),(0,a.__decorate)([(0,o.Cb)({attribute:!1})],f.prototype,"hass",void 0),(0,a.__decorate)([(0,o.Cb)({type:Boolean,reflect:!0})],f.prototype,"disabled",void 0),(0,a.__decorate)([(0,o.Cb)({type:Boolean})],f.prototype,"required",void 0),(0,a.__decorate)([(0,o.Cb)({attribute:!1})],f.prototype,"includeLastUsed",void 0),(0,a.__decorate)([(0,o.SB)()],f.prototype,"_pipelines",void 0),(0,a.__decorate)([(0,o.SB)()],f.prototype,"_preferredPipeline",void 0),f=(0,a.__decorate)([(0,o.Mo)("ha-assist-pipeline-picker")],f),e()}catch(h){e(h)}}))},57027:function(t,e,i){i.a(t,(async function(t,e){try{i(26847),i(27530);var a=i(73742),s=i(59048),o=i(7616),n=(i(40830),i(27341)),r=t([n]);n=(r.then?(await r)():r)[0];let l,c,d=t=>t;const h="M15.07,11.25L14.17,12.17C13.45,12.89 13,13.5 13,15H11V14.5C11,13.39 11.45,12.39 12.17,11.67L13.41,10.41C13.78,10.05 14,9.55 14,9C14,7.89 13.1,7 12,7A2,2 0 0,0 10,9H8A4,4 0 0,1 12,5A4,4 0 0,1 16,9C16,9.88 15.64,10.67 15.07,11.25M13,19H11V17H13M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12C22,6.47 17.5,2 12,2Z";class u extends s.oi{render(){return(0,s.dy)(l||(l=d`
      <ha-tooltip .placement=${0} .content=${0}>
        <ha-svg-icon .path=${0}></ha-svg-icon>
      </ha-tooltip>
    `),this.position,this.label,h)}constructor(...t){super(...t),this.position="top"}}u.styles=(0,s.iv)(c||(c=d`
    ha-svg-icon {
      --mdc-icon-size: var(--ha-help-tooltip-size, 14px);
      color: var(--ha-help-tooltip-color, var(--disabled-text-color));
    }
  `)),(0,a.__decorate)([(0,o.Cb)()],u.prototype,"label",void 0),(0,a.__decorate)([(0,o.Cb)()],u.prototype,"position",void 0),u=(0,a.__decorate)([(0,o.Mo)("ha-help-tooltip")],u),e()}catch(l){e(l)}}))},20797:function(t,e,i){i.a(t,(async function(t,e){try{i(39710),i(26847),i(2394),i(81738),i(94814),i(22960),i(6989),i(87799),i(1455),i(56389),i(27530);var a=i(73742),s=i(59048),o=i(7616),n=i(29740),r=i(1893),l=i(8265),c=i(54693),d=(i(57264),i(3847),t([c]));c=(d.then?(await d)():d)[0];let h,u,p,v,_=t=>t;const g=[],b=t=>(0,s.dy)(h||(h=_`
  <ha-combo-box-item type="button">
    <ha-icon .icon=${0} slot="start"></ha-icon>
    <span slot="headline">${0}</span>
    ${0}
  </ha-combo-box-item>
`),t.icon,t.title||t.path,t.title?(0,s.dy)(u||(u=_`<span slot="supporting-text">${0}</span>`),t.path):s.Ld),f=(t,e,i)=>{var a,s,o;return{path:`/${t}/${null!==(a=e.path)&&void 0!==a?a:i}`,icon:null!==(s=e.icon)&&void 0!==s?s:"mdi:view-compact",title:null!==(o=e.title)&&void 0!==o?o:e.path?(0,r.Q)(e.path):`${i}`}},m=(t,e)=>{var i;return{path:`/${e.url_path}`,icon:null!==(i=e.icon)&&void 0!==i?i:"mdi:view-dashboard",title:e.url_path===t.defaultPanel?t.localize("panel.states"):t.localize(`panel.${e.title}`)||e.title||(e.url_path?(0,r.Q)(e.url_path):"")}};class y extends s.oi{render(){return(0,s.dy)(p||(p=_`
      <ha-combo-box
        .hass=${0}
        item-value-path="path"
        item-label-path="path"
        .value=${0}
        allow-custom-value
        .filteredItems=${0}
        .label=${0}
        .helper=${0}
        .disabled=${0}
        .required=${0}
        .renderer=${0}
        @opened-changed=${0}
        @value-changed=${0}
        @filter-changed=${0}
      >
      </ha-combo-box>
    `),this.hass,this._value,this.navigationItems,this.label,this.helper,this.disabled,this.required,b,this._openedChanged,this._valueChanged,this._filterChanged)}async _openedChanged(t){this._opened=t.detail.value,this._opened&&!this.navigationItemsLoaded&&this._loadNavigationItems()}async _loadNavigationItems(){this.navigationItemsLoaded=!0;const t=Object.entries(this.hass.panels).map((([t,e])=>Object.assign({id:t},e))),e=t.filter((t=>"lovelace"===t.component_name)),i=await Promise.all(e.map((t=>(0,l.Q2)(this.hass.connection,"lovelace"===t.url_path?null:t.url_path,!0).then((e=>[t.id,e])).catch((e=>[t.id,void 0]))))),a=new Map(i);this.navigationItems=[];for(const s of t){this.navigationItems.push(m(this.hass,s));const t=a.get(s.id);t&&"views"in t&&t.views.forEach(((t,e)=>this.navigationItems.push(f(s.url_path,t,e))))}this.comboBox.filteredItems=this.navigationItems}shouldUpdate(t){return!this._opened||t.has("_opened")}_valueChanged(t){t.stopPropagation(),this._setValue(t.detail.value)}_setValue(t){this.value=t,(0,n.B)(this,"value-changed",{value:this._value},{bubbles:!1,composed:!1})}_filterChanged(t){const e=t.detail.value.toLowerCase();if(e.length>=2){const t=[];this.navigationItems.forEach((i=>{(i.path.toLowerCase().includes(e)||i.title.toLowerCase().includes(e))&&t.push(i)})),t.length>0?this.comboBox.filteredItems=t:this.comboBox.filteredItems=[]}else this.comboBox.filteredItems=this.navigationItems}get _value(){return this.value||""}constructor(...t){super(...t),this.disabled=!1,this.required=!1,this._opened=!1,this.navigationItemsLoaded=!1,this.navigationItems=g}}y.styles=(0,s.iv)(v||(v=_`
    ha-icon,
    ha-svg-icon {
      color: var(--primary-text-color);
      position: relative;
      bottom: 0px;
    }
    *[slot="prefix"] {
      margin-right: 8px;
      margin-inline-end: 8px;
      margin-inline-start: initial;
    }
  `)),(0,a.__decorate)([(0,o.Cb)({attribute:!1})],y.prototype,"hass",void 0),(0,a.__decorate)([(0,o.Cb)()],y.prototype,"label",void 0),(0,a.__decorate)([(0,o.Cb)()],y.prototype,"value",void 0),(0,a.__decorate)([(0,o.Cb)()],y.prototype,"helper",void 0),(0,a.__decorate)([(0,o.Cb)({type:Boolean})],y.prototype,"disabled",void 0),(0,a.__decorate)([(0,o.Cb)({type:Boolean})],y.prototype,"required",void 0),(0,a.__decorate)([(0,o.SB)()],y.prototype,"_opened",void 0),(0,a.__decorate)([(0,o.IO)("ha-combo-box",!0)],y.prototype,"comboBox",void 0),y=(0,a.__decorate)([(0,o.Mo)("ha-navigation-picker")],y),e()}catch(h){e(h)}}))},53179:function(t,e,i){i.a(t,(async function(t,a){try{i.r(e),i.d(e,{HaSelectorUiAction:function(){return u}});var s=i(73742),o=i(59048),n=i(7616),r=i(29740),l=i(18234),c=t([l]);l=(c.then?(await c)():c)[0];let d,h=t=>t;class u extends o.oi{render(){var t,e;return(0,o.dy)(d||(d=h`
      <hui-action-editor
        .label=${0}
        .hass=${0}
        .config=${0}
        .actions=${0}
        .defaultAction=${0}
        .tooltipText=${0}
        @value-changed=${0}
      ></hui-action-editor>
    `),this.label,this.hass,this.value,null===(t=this.selector.ui_action)||void 0===t?void 0:t.actions,null===(e=this.selector.ui_action)||void 0===e?void 0:e.default_action,this.helper,this._valueChanged)}_valueChanged(t){t.stopPropagation(),(0,r.B)(this,"value-changed",{value:t.detail.value})}}(0,s.__decorate)([(0,n.Cb)({attribute:!1})],u.prototype,"hass",void 0),(0,s.__decorate)([(0,n.Cb)({attribute:!1})],u.prototype,"selector",void 0),(0,s.__decorate)([(0,n.Cb)({attribute:!1})],u.prototype,"value",void 0),(0,s.__decorate)([(0,n.Cb)()],u.prototype,"label",void 0),(0,s.__decorate)([(0,n.Cb)()],u.prototype,"helper",void 0),u=(0,s.__decorate)([(0,n.Mo)("ha-selector-ui_action")],u),a()}catch(d){a(d)}}))},32518:function(t,e,i){i.d(e,{Dy:function(){return c},PA:function(){return n},SC:function(){return o},Xp:function(){return s},af:function(){return l},eP:function(){return a},jZ:function(){return r}});i(26847),i(87799),i(27530);const a=(t,e,i)=>"run-start"===e.type?t={init_options:i,stage:"ready",run:e.data,events:[e]}:t?((t="wake_word-start"===e.type?Object.assign(Object.assign({},t),{},{stage:"wake_word",wake_word:Object.assign(Object.assign({},e.data),{},{done:!1})}):"wake_word-end"===e.type?Object.assign(Object.assign({},t),{},{wake_word:Object.assign(Object.assign(Object.assign({},t.wake_word),e.data),{},{done:!0})}):"stt-start"===e.type?Object.assign(Object.assign({},t),{},{stage:"stt",stt:Object.assign(Object.assign({},e.data),{},{done:!1})}):"stt-end"===e.type?Object.assign(Object.assign({},t),{},{stt:Object.assign(Object.assign(Object.assign({},t.stt),e.data),{},{done:!0})}):"intent-start"===e.type?Object.assign(Object.assign({},t),{},{stage:"intent",intent:Object.assign(Object.assign({},e.data),{},{done:!1})}):"intent-end"===e.type?Object.assign(Object.assign({},t),{},{intent:Object.assign(Object.assign(Object.assign({},t.intent),e.data),{},{done:!0})}):"tts-start"===e.type?Object.assign(Object.assign({},t),{},{stage:"tts",tts:Object.assign(Object.assign({},e.data),{},{done:!1})}):"tts-end"===e.type?Object.assign(Object.assign({},t),{},{tts:Object.assign(Object.assign(Object.assign({},t.tts),e.data),{},{done:!0})}):"run-end"===e.type?Object.assign(Object.assign({},t),{},{stage:"done"}):"error"===e.type?Object.assign(Object.assign({},t),{},{stage:"error",error:e.data}):Object.assign({},t)).events=[...t.events,e],t):void console.warn("Received unexpected event before receiving session",e),s=(t,e,i)=>t.connection.subscribeMessage(e,Object.assign(Object.assign({},i),{},{type:"assist_pipeline/run"})),o=t=>t.callWS({type:"assist_pipeline/pipeline/list"}),n=(t,e)=>t.callWS({type:"assist_pipeline/pipeline/get",pipeline_id:e}),r=(t,e)=>t.callWS(Object.assign({type:"assist_pipeline/pipeline/create"},e)),l=(t,e,i)=>t.callWS(Object.assign({type:"assist_pipeline/pipeline/update",pipeline_id:e},i)),c=t=>t.callWS({type:"assist_pipeline/language/list"})},47469:function(t,e,i){i.d(e,{F3:function(){return s},Lh:function(){return a},t4:function(){return o}});i(16811);const a=(t,e,i)=>t(`component.${e}.title`)||(null==i?void 0:i.name)||e,s=(t,e)=>{const i={type:"manifest/list"};return e&&(i.integrations=e),t.callWS(i)},o=(t,e)=>t.callWS({type:"manifest/get",integration:e})},8265:function(t,e,i){i.d(e,{Q2:function(){return a}});const a=(t,e,i)=>t.sendMessagePromise({type:"lovelace/config",url_path:e,force:i})},18234:function(t,e,i){i.a(t,(async function(t,e){try{i(26847),i(81738),i(6989),i(87799),i(27530);var a=i(73742),s=i(59048),o=i(7616),n=i(28105),r=i(29740),l=i(41806),c=i(69187),d=i(57027),h=(i(93795),i(20797)),u=i(45618),p=t([c,d,h,u]);[c,d,h,u]=p.then?(await p)():p;let v,_,g,b,f,m,y,$,C=t=>t;const O=["more-info","toggle","navigate","url","perform-action","assist","none"],j=[{name:"navigation_path",selector:{navigation:{}}}],w=[{type:"grid",name:"",schema:[{name:"pipeline_id",selector:{assist_pipeline:{include_last_used:!0}}},{name:"start_listening",selector:{boolean:{}}}]}];class x extends s.oi{get _navigation_path(){const t=this.config;return(null==t?void 0:t.navigation_path)||""}get _url_path(){const t=this.config;return(null==t?void 0:t.url_path)||""}get _service(){const t=this.config;return(null==t?void 0:t.perform_action)||(null==t?void 0:t.service)||""}updated(t){super.updated(t),t.has("defaultAction")&&t.get("defaultAction")!==this.defaultAction&&this._select.layoutOptions()}render(){var t,e,i,a,o,n,r,c;if(!this.hass)return s.Ld;const d=null!==(t=this.actions)&&void 0!==t?t:O;let h=(null===(e=this.config)||void 0===e?void 0:e.action)||"default";return"call-service"===h&&(h="perform-action"),(0,s.dy)(v||(v=C`
      <div class="dropdown">
        <ha-select
          .label=${0}
          .configValue=${0}
          @selected=${0}
          .value=${0}
          @closed=${0}
          fixedMenuPosition
          naturalMenuWidth
        >
          <ha-list-item value="default">
            ${0}
            ${0}
          </ha-list-item>
          ${0}
        </ha-select>
        ${0}
      </div>
      ${0}
      ${0}
      ${0}
      ${0}
    `),this.label,"action",this._actionPicked,h,l.U,this.hass.localize("ui.panel.lovelace.editor.action-editor.actions.default_action"),this.defaultAction?` (${this.hass.localize(`ui.panel.lovelace.editor.action-editor.actions.${this.defaultAction}`).toLowerCase()})`:s.Ld,d.map((t=>(0,s.dy)(_||(_=C`
              <ha-list-item .value=${0}>
                ${0}
              </ha-list-item>
            `),t,this.hass.localize(`ui.panel.lovelace.editor.action-editor.actions.${t}`)))),this.tooltipText?(0,s.dy)(g||(g=C`
              <ha-help-tooltip .label=${0}></ha-help-tooltip>
            `),this.tooltipText):s.Ld,"navigate"===(null===(i=this.config)||void 0===i?void 0:i.action)?(0,s.dy)(b||(b=C`
            <ha-form
              .hass=${0}
              .schema=${0}
              .data=${0}
              .computeLabel=${0}
              @value-changed=${0}
            >
            </ha-form>
          `),this.hass,j,this.config,this._computeFormLabel,this._formValueChanged):s.Ld,"url"===(null===(a=this.config)||void 0===a?void 0:a.action)?(0,s.dy)(f||(f=C`
            <ha-textfield
              .label=${0}
              .value=${0}
              .configValue=${0}
              @input=${0}
            ></ha-textfield>
          `),this.hass.localize("ui.panel.lovelace.editor.action-editor.url_path"),this._url_path,"url_path",this._valueChanged):s.Ld,"call-service"===(null===(o=this.config)||void 0===o?void 0:o.action)||"perform-action"===(null===(n=this.config)||void 0===n?void 0:n.action)?(0,s.dy)(m||(m=C`
            <ha-service-control
              .hass=${0}
              .value=${0}
              .showAdvanced=${0}
              narrow
              @value-changed=${0}
            ></ha-service-control>
          `),this.hass,this._serviceAction(this.config),null===(r=this.hass.userData)||void 0===r?void 0:r.showAdvanced,this._serviceValueChanged):s.Ld,"assist"===(null===(c=this.config)||void 0===c?void 0:c.action)?(0,s.dy)(y||(y=C`
            <ha-form
              .hass=${0}
              .schema=${0}
              .data=${0}
              .computeLabel=${0}
              @value-changed=${0}
            >
            </ha-form>
          `),this.hass,w,this.config,this._computeFormLabel,this._formValueChanged):s.Ld)}_actionPicked(t){var e;if(t.stopPropagation(),!this.hass)return;let i=null===(e=this.config)||void 0===e?void 0:e.action;"call-service"===i&&(i="perform-action");const a=t.target.value;if(i===a)return;if("default"===a)return void(0,r.B)(this,"value-changed",{value:void 0});let s;switch(a){case"url":s={url_path:this._url_path};break;case"perform-action":s={perform_action:this._service};break;case"navigate":s={navigation_path:this._navigation_path}}(0,r.B)(this,"value-changed",{value:Object.assign({action:a},s)})}_valueChanged(t){var e;if(t.stopPropagation(),!this.hass)return;const i=t.target,a=null!==(e=t.target.value)&&void 0!==e?e:t.target.checked;this[`_${i.configValue}`]!==a&&i.configValue&&(0,r.B)(this,"value-changed",{value:Object.assign(Object.assign({},this.config),{},{[i.configValue]:a})})}_formValueChanged(t){t.stopPropagation();const e=t.detail.value;(0,r.B)(this,"value-changed",{value:e})}_computeFormLabel(t){var e;return null===(e=this.hass)||void 0===e?void 0:e.localize(`ui.panel.lovelace.editor.action-editor.${t.name}`)}_serviceValueChanged(t){t.stopPropagation();const e=Object.assign(Object.assign({},this.config),{},{action:"perform-action",perform_action:t.detail.value.action||"",data:t.detail.value.data,target:t.detail.value.target||{}});t.detail.value.data||delete e.data,"service_data"in e&&delete e.service_data,"service"in e&&delete e.service,(0,r.B)(this,"value-changed",{value:e})}constructor(...t){super(...t),this._serviceAction=(0,n.Z)((t=>{var e;return Object.assign(Object.assign({action:this._service},t.data||t.service_data?{data:null!==(e=t.data)&&void 0!==e?e:t.service_data}:null),{},{target:t.target})}))}}x.styles=(0,s.iv)($||($=C`
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
  `)),(0,a.__decorate)([(0,o.Cb)({attribute:!1})],x.prototype,"config",void 0),(0,a.__decorate)([(0,o.Cb)({attribute:!1})],x.prototype,"label",void 0),(0,a.__decorate)([(0,o.Cb)({attribute:!1})],x.prototype,"actions",void 0),(0,a.__decorate)([(0,o.Cb)({attribute:!1})],x.prototype,"defaultAction",void 0),(0,a.__decorate)([(0,o.Cb)({attribute:!1})],x.prototype,"tooltipText",void 0),(0,a.__decorate)([(0,o.Cb)({attribute:!1})],x.prototype,"hass",void 0),(0,a.__decorate)([(0,o.IO)("ha-select")],x.prototype,"_select",void 0),x=(0,a.__decorate)([(0,o.Mo)("hui-action-editor")],x),e()}catch(v){e(v)}}))},15606:function(t,e,i){i.d(e,{C:function(){return s}});var a=i(29740);const s=(t,e)=>(0,a.B)(t,"hass-notification",e)},28177:function(t,e,i){i.d(e,{C:function(){return u}});i(26847),i(81738),i(29981),i(1455),i(27530);var a=i(35340),s=i(5277),o=i(93847);i(84730),i(15411),i(40777);class n{disconnect(){this.G=void 0}reconnect(t){this.G=t}deref(){return this.G}constructor(t){this.G=t}}class r{get(){return this.Y}pause(){var t;null!==(t=this.Y)&&void 0!==t||(this.Y=new Promise((t=>this.Z=t)))}resume(){var t;null!==(t=this.Z)&&void 0!==t&&t.call(this),this.Y=this.Z=void 0}constructor(){this.Y=void 0,this.Z=void 0}}var l=i(83522);const c=t=>!(0,s.pt)(t)&&"function"==typeof t.then,d=1073741823;class h extends o.sR{render(...t){var e;return null!==(e=t.find((t=>!c(t))))&&void 0!==e?e:a.Jb}update(t,e){const i=this._$Cbt;let s=i.length;this._$Cbt=e;const o=this._$CK,n=this._$CX;this.isConnected||this.disconnected();for(let a=0;a<e.length&&!(a>this._$Cwt);a++){const t=e[a];if(!c(t))return this._$Cwt=a,t;a<s&&t===i[a]||(this._$Cwt=d,s=0,Promise.resolve(t).then((async e=>{for(;n.get();)await n.get();const i=o.deref();if(void 0!==i){const a=i._$Cbt.indexOf(t);a>-1&&a<i._$Cwt&&(i._$Cwt=a,i.setValue(e))}})))}return a.Jb}disconnected(){this._$CK.disconnect(),this._$CX.pause()}reconnected(){this._$CK.reconnect(this),this._$CX.resume()}constructor(){super(...arguments),this._$Cwt=d,this._$Cbt=[],this._$CK=new n(this),this._$CX=new r}}const u=(0,l.XM)(h)}}]);
//# sourceMappingURL=5171.807f06e7eeb8c486.js.map