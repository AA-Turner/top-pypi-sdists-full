"use strict";(self.webpackChunkknx_frontend=self.webpackChunkknx_frontend||[]).push([["5792"],{85163:function(e,t,i){i.d(t,{wZ:function(){return a},jL:function(){return r}});i(26847),i(81738),i(94814),i(6989),i(20655),i(27530);var o=i(28105),n=i(31298);i(67886),i(65451),i(46015),i(38334),i(94880),i(75643),i(29761);const r=e=>{var t;return null===(t=e.name_by_user||e.name)||void 0===t?void 0:t.trim()},a=(e,t,i)=>r(e)||i&&s(t,i)||t.localize("ui.panel.config.devices.unnamed_device",{type:t.localize(`ui.panel.config.devices.type.${e.entry_type||"device"}`)}),s=(e,t)=>{for(const i of t||[]){const t="string"==typeof i?i:i.entity_id,o=e.states[t];if(o)return(0,n.C)(o)}};(0,o.Z)((e=>function(e){const t=new Set,i=new Set;for(const o of e)i.has(o)?t.add(o):i.add(o);return t}(Object.values(e).map((e=>r(e))).filter((e=>void 0!==e)))))},10996:function(e,t,i){i.d(t,{K:function(){return s}});var o=i(85163),n=i(31298);i(26847),i(44261),i(27530);const r=[" ",": "," - "],a=e=>e.toLowerCase()!==e,s=(e,t)=>{const i=t.entities[e.entity_id];return i?l(i,t):(0,n.C)(e)},l=(e,t)=>{const i=e.name||("original_name"in e?e.original_name:void 0),s=e.device_id?t.devices[e.device_id]:void 0;if(!s){if(i)return i;const o=t.states[e.entity_id];return o?(0,n.C)(o):void 0}const l=(0,o.jL)(s);if(l!==i)return l&&i&&((e,t)=>{const i=e.toLowerCase(),o=t.toLowerCase();for(const n of r){const t=`${o}${n}`;if(i.startsWith(t)){const i=e.substring(t.length);if(i.length)return a(i.substr(0,i.indexOf(" ")))?i:i[0].toUpperCase()+i.slice(1)}}})(i,l)||i}},66027:function(e,t,i){i.d(t,{U:function(){return o}});const o=(e,t)=>{const i=t.entities[e.entity_id];return i?n(i,t):{entity:null,device:null,area:null,floor:null}},n=(e,t)=>{const i=t.entities[e.entity_id],o=null==e?void 0:e.device_id,n=o?t.devices[o]:void 0,r=(null==e?void 0:e.area_id)||(null==n?void 0:n.area_id),a=r?t.areas[r]:void 0,s=null==a?void 0:a.floor_id;return{entity:i,device:n||null,area:a||null,floor:(s?t.floors[s]:void 0)||null}}},35505:function(e,t,i){i.d(t,{K:function(){return o}});const o=e=>{switch(e.language){case"cs":case"de":case"fi":case"fr":case"sk":case"sv":return" ";default:return""}}},85310:function(e,t,i){i.d(t,{L:function(){return n}});var o=i(35505);const n=(e,t)=>"°"===e?"":t&&"%"===e?(0,o.K)(t):" "},74002:function(e,t,i){i.d(t,{v:function(){return o}});i(26847),i(65640),i(28660),i(64455),i(60142),i(56303),i(67886),i(65451),i(46015),i(38334),i(94880),i(75643),i(29761),i(27530);const o=(e,t)=>{if(e===t)return!0;if(e&&t&&"object"==typeof e&&"object"==typeof t){if(e.constructor!==t.constructor)return!1;let i,n;if(Array.isArray(e)){if(n=e.length,n!==t.length)return!1;for(i=n;0!=i--;)if(!o(e[i],t[i]))return!1;return!0}if(e instanceof Map&&t instanceof Map){if(e.size!==t.size)return!1;for(i of e.entries())if(!t.has(i[0]))return!1;for(i of e.entries())if(!o(i[1],t.get(i[0])))return!1;return!0}if(e instanceof Set&&t instanceof Set){if(e.size!==t.size)return!1;for(i of e.entries())if(!t.has(i[0]))return!1;return!0}if(ArrayBuffer.isView(e)&&ArrayBuffer.isView(t)){if(n=e.length,n!==t.length)return!1;for(i=n;0!=i--;)if(e[i]!==t[i])return!1;return!0}if(e.constructor===RegExp)return e.source===t.source&&e.flags===t.flags;if(e.valueOf!==Object.prototype.valueOf)return e.valueOf()===t.valueOf();if(e.toString!==Object.prototype.toString)return e.toString()===t.toString();const r=Object.keys(e);if(n=r.length,n!==Object.keys(t).length)return!1;for(i=n;0!=i--;)if(!Object.prototype.hasOwnProperty.call(t,r[i]))return!1;for(i=n;0!=i--;){const n=r[i];if(!o(e[n],t[n]))return!1}return!0}return e!=e&&t!=t}},57612:function(e,t,i){i.a(e,(async function(e,o){try{i.r(t),i.d(t,{HaObjectSelector:function(){return k}});i(26847),i(2394),i(81738),i(6989),i(1455),i(27530);var n=i(73742),r=i(59048),a=i(7616),s=i(28105),l=i(74608),c=i(29740),d=i(73123),u=i(88561),h=(i(42592),i(89429),i(78067),i(48374),i(36344)),f=i(74002),v=e([h]);h=(v.then?(await v)():v)[0];let m,p,b,g,_,y,$,j,L,V,H,x,C=e=>e;const w="M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z",M="M19,4H15.5L14.5,3H9.5L8.5,4H5V6H19M6,19A2,2 0 0,0 8,21H16A2,2 0 0,0 18,19V7H6V19Z",z="M7,19V17H9V19H7M11,19V17H13V19H11M15,19V17H17V19H15M7,15V13H9V15H7M11,15V13H13V15H11M15,15V13H17V15H15M7,11V9H9V11H7M11,11V9H13V11H11M15,11V9H17V11H15M7,7V5H9V7H7M11,7V5H13V7H11M15,7V5H17V7H15Z",O="M20.71,7.04C21.1,6.65 21.1,6 20.71,5.63L18.37,3.29C18,2.9 17.35,2.9 16.96,3.29L15.12,5.12L18.87,8.87M3,17.25V21H6.75L17.81,9.93L14.06,6.18L3,17.25Z";class k extends r.oi{_renderItem(e,t){const i=this.selector.object.label_field||Object.keys(this.selector.object.fields)[0],o=this.selector.object.fields[i].selector,n=o?(0,d.z)(this.hass,e[i],o):"";let a="";const s=this.selector.object.description_field;if(s){const t=this.selector.object.fields[s].selector;a=t?(0,d.z)(this.hass,e[s],t):""}const l=this.selector.object.multiple||!1,c=this.selector.object.multiple||!1;return(0,r.dy)(m||(m=C`
      <ha-md-list-item class="item">
        ${0}
        <div slot="headline" class="label">${0}</div>
        ${0}
        <ha-icon-button
          slot="end"
          .item=${0}
          .index=${0}
          .label=${0}
          .path=${0}
          @click=${0}
        ></ha-icon-button>
        <ha-icon-button
          slot="end"
          .index=${0}
          .label=${0}
          .path=${0}
          @click=${0}
        ></ha-icon-button>
      </ha-md-list-item>
    `),l?(0,r.dy)(p||(p=C`
              <ha-svg-icon
                class="handle"
                .path=${0}
                slot="start"
              ></ha-svg-icon>
            `),z):r.Ld,n,a?(0,r.dy)(b||(b=C`<div slot="supporting-text" class="description">
              ${0}
            </div>`),a):r.Ld,e,t,this.hass.localize("ui.common.edit"),O,this._editItem,t,this.hass.localize("ui.common.delete"),c?M:w,this._deleteItem)}render(){var e;if(null!==(e=this.selector.object)&&void 0!==e&&e.fields){if(this.selector.object.multiple){var t;const e=(0,l.r)(null!==(t=this.value)&&void 0!==t?t:[]);return(0,r.dy)(g||(g=C`
          ${0}
          <div class="items-container">
            <ha-sortable
              handle-selector=".handle"
              draggable-selector=".item"
              @item-moved=${0}
            >
              <ha-md-list>
                ${0}
              </ha-md-list>
            </ha-sortable>
            <ha-button appearance="filled" @click=${0}>
              ${0}
            </ha-button>
          </div>
        `),this.label?(0,r.dy)(_||(_=C`<label>${0}</label>`),this.label):r.Ld,this._itemMoved,e.map(((e,t)=>this._renderItem(e,t))),this._addItem,this.hass.localize("ui.common.add"))}return(0,r.dy)(y||(y=C`
        ${0}
        <div class="items-container">
          ${0}
        </div>
      `),this.label?(0,r.dy)($||($=C`<label>${0}</label>`),this.label):r.Ld,this.value?(0,r.dy)(j||(j=C`<ha-md-list>
                ${0}
              </ha-md-list>`),this._renderItem(this.value,0)):(0,r.dy)(L||(L=C`
                <ha-button appearance="filled" @click=${0}>
                  ${0}
                </ha-button>
              `),this._addItem,this.hass.localize("ui.common.add")))}return(0,r.dy)(V||(V=C`<ha-yaml-editor
        .hass=${0}
        .readonly=${0}
        .label=${0}
        .required=${0}
        .placeholder=${0}
        .defaultValue=${0}
        @value-changed=${0}
      ></ha-yaml-editor>
      ${0} `),this.hass,this.disabled,this.label,this.required,this.placeholder,this.value,this._handleChange,this.helper?(0,r.dy)(H||(H=C`<ha-input-helper-text .disabled=${0}
            >${0}</ha-input-helper-text
          >`),this.disabled,this.helper):"")}_itemMoved(e){var t;e.stopPropagation();const i=e.detail.newIndex,o=e.detail.oldIndex;if(!this.selector.object.multiple)return;const n=(0,l.r)(null!==(t=this.value)&&void 0!==t?t:[]).concat(),r=n.splice(o,1)[0];n.splice(i,0,r),(0,c.B)(this,"value-changed",{value:n})}async _addItem(e){var t;e.stopPropagation();const i=await(0,u.v)(this,{title:this.hass.localize("ui.common.add"),schema:this._schema(this.selector),data:{},computeLabel:this._computeLabel,submitText:this.hass.localize("ui.common.add")});if(null===i)return;if(!this.selector.object.multiple)return void(0,c.B)(this,"value-changed",{value:i});const o=(0,l.r)(null!==(t=this.value)&&void 0!==t?t:[]).concat();o.push(i),(0,c.B)(this,"value-changed",{value:o})}async _editItem(e){var t;e.stopPropagation();const i=e.currentTarget.item,o=e.currentTarget.index,n=await(0,u.v)(this,{title:this.hass.localize("ui.common.edit"),schema:this._schema(this.selector),data:i,computeLabel:this._computeLabel,submitText:this.hass.localize("ui.common.save")});if(null===n)return;if(!this.selector.object.multiple)return void(0,c.B)(this,"value-changed",{value:n});const r=(0,l.r)(null!==(t=this.value)&&void 0!==t?t:[]).concat();r[o]=n,(0,c.B)(this,"value-changed",{value:r})}_deleteItem(e){var t;e.stopPropagation();const i=e.currentTarget.index;if(!this.selector.object.multiple)return void(0,c.B)(this,"value-changed",{value:void 0});const o=(0,l.r)(null!==(t=this.value)&&void 0!==t?t:[]).concat();o.splice(i,1),(0,c.B)(this,"value-changed",{value:o})}updated(e){super.updated(e),e.has("value")&&!this._valueChangedFromChild&&this._yamlEditor&&!(0,f.v)(this.value,e.get("value"))&&this._yamlEditor.setValue(this.value),this._valueChangedFromChild=!1}_handleChange(e){e.stopPropagation(),this._valueChangedFromChild=!0;const t=e.target.value;e.target.isValid&&this.value!==t&&(0,c.B)(this,"value-changed",{value:t})}static get styles(){return[(0,r.iv)(x||(x=C`
        ha-md-list {
          gap: 8px;
        }
        ha-md-list-item {
          border: 1px solid var(--divider-color);
          border-radius: 8px;
          --ha-md-list-item-gap: 0;
          --md-list-item-top-space: 0;
          --md-list-item-bottom-space: 0;
          --md-list-item-leading-space: 12px;
          --md-list-item-trailing-space: 4px;
          --md-list-item-two-line-container-height: 48px;
          --md-list-item-one-line-container-height: 48px;
        }
        .handle {
          cursor: move;
          padding: 8px;
          margin-inline-start: -8px;
        }
        label {
          margin-bottom: 8px;
          display: block;
        }
        ha-md-list-item .label,
        ha-md-list-item .description {
          text-overflow: ellipsis;
          overflow: hidden;
          white-space: nowrap;
        }
      `))]}constructor(...e){super(...e),this.disabled=!1,this.required=!0,this._valueChangedFromChild=!1,this._computeLabel=e=>{var t,i;const o=null===(t=this.selector.object)||void 0===t?void 0:t.translation_key;if(this.localizeValue&&o){const t=this.localizeValue(`${o}.fields.${e.name}`);if(t)return t}return(null===(i=this.selector.object)||void 0===i||null===(i=i.fields)||void 0===i||null===(i=i[e.name])||void 0===i?void 0:i.label)||e.name},this._schema=(0,s.Z)((e=>e.object&&e.object.fields?Object.entries(e.object.fields).map((([e,t])=>{var i;return{name:e,selector:t.selector,required:null!==(i=t.required)&&void 0!==i&&i}})):[]))}}(0,n.__decorate)([(0,a.Cb)({attribute:!1})],k.prototype,"hass",void 0),(0,n.__decorate)([(0,a.Cb)({attribute:!1})],k.prototype,"selector",void 0),(0,n.__decorate)([(0,a.Cb)()],k.prototype,"value",void 0),(0,n.__decorate)([(0,a.Cb)()],k.prototype,"label",void 0),(0,n.__decorate)([(0,a.Cb)()],k.prototype,"helper",void 0),(0,n.__decorate)([(0,a.Cb)()],k.prototype,"placeholder",void 0),(0,n.__decorate)([(0,a.Cb)({type:Boolean})],k.prototype,"disabled",void 0),(0,n.__decorate)([(0,a.Cb)({type:Boolean})],k.prototype,"required",void 0),(0,n.__decorate)([(0,a.Cb)({attribute:!1})],k.prototype,"localizeValue",void 0),(0,n.__decorate)([(0,a.IO)("ha-yaml-editor",!0)],k.prototype,"_yamlEditor",void 0),k=(0,n.__decorate)([(0,a.Mo)("ha-selector-object")],k),o()}catch(m){o(m)}}))},73123:function(e,t,i){i.d(t,{z:function(){return c}});i(81738),i(6989),i(56303);var o=i(74608),n=i(71188),r=i(85163),a=i(10996),s=i(66027),l=i(85310);const c=(e,t,i)=>{if(null==t)return"";if(!i)return(0,o.r)(t).join(", ");if("text"in i){const{prefix:e,suffix:n}=i.text||{};return(0,o.r)(t).map((t=>`${e||""}${t}${n||""}`)).join(", ")}if("number"in i){const{unit_of_measurement:n}=i.number||{};return(0,o.r)(t).map((t=>{const i=Number(t);return isNaN(i)?t:n?`${i}${(0,l.L)(n,e.locale)}${n}`:i.toString()})).join(", ")}if("floor"in i){return(0,o.r)(t).map((t=>{const i=e.floors[t];return i&&i.name||t})).join(", ")}if("area"in i){return(0,o.r)(t).map((t=>{const i=e.areas[t];return i?(0,n.D)(i):t})).join(", ")}if("entity"in i){return(0,o.r)(t).map((t=>{const i=e.states[t];if(!i)return t;const{device:o}=(0,s.U)(i,e);return[o?(0,r.jL)(o):void 0,(0,a.K)(i,e)].filter(Boolean).join(" ")||t})).join(", ")}if("device"in i){return(0,o.r)(t).map((t=>{const i=e.devices[t];return i&&i.name||t})).join(", ")}return(0,o.r)(t).join(", ")}},88561:function(e,t,i){i.d(t,{v:function(){return n}});i(26847),i(87799),i(1455),i(27530);var o=i(29740);const n=(e,t)=>new Promise((n=>{const r=t.cancel,a=t.submit;(0,o.B)(e,"show-dialog",{dialogTag:"dialog-form",dialogImport:()=>i.e("4477").then(i.bind(i,13021)),dialogParams:Object.assign(Object.assign({},t),{},{cancel:()=>{n(null),r&&r()},submit:e=>{n(e),a&&a(e)}})})}))},15606:function(e,t,i){i.d(t,{C:function(){return n}});var o=i(29740);const n=(e,t)=>(0,o.B)(e,"hass-notification",t)}}]);
//# sourceMappingURL=5792.86dce4745f9f169b.js.map