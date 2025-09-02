"use strict";(self.webpackChunkknx_frontend=self.webpackChunkknx_frontend||[]).push([["8552"],{81758:function(t,e,o){o.a(t,(async function(t,e){try{o(39710),o(26847),o(2394),o(81738),o(94814),o(6989),o(67886),o(65451),o(46015),o(38334),o(94880),o(75643),o(29761),o(56389),o(27530);var i=o(73742),a=o(59048),r=o(7616),s=o(74608),d=o(29740),l=o(54693),u=t([l]);l=(u.then?(await u)():u)[0];let h,n=t=>t;class c extends a.oi{shouldUpdate(t){return!(!t.has("_opened")&&this._opened)}updated(t){if(t.has("_opened")&&this._opened||t.has("entityId")||t.has("attribute")){const t=(this.entityId?(0,s.r)(this.entityId):[]).map((t=>{const e=this.hass.states[t];if(!e)return[];return Object.keys(e.attributes).filter((t=>{var e;return!(null!==(e=this.hideAttributes)&&void 0!==e&&e.includes(t))})).map((t=>({value:t,label:this.hass.formatEntityAttributeName(e,t)})))})),e=[],o=new Set;for(const i of t)for(const t of i)o.has(t.value)||(o.add(t.value),e.push(t));this._comboBox.filteredItems=e}}render(){var t;return this.hass?(0,a.dy)(h||(h=n`
      <ha-combo-box
        .hass=${0}
        .value=${0}
        .autofocus=${0}
        .label=${0}
        .disabled=${0}
        .required=${0}
        .helper=${0}
        .allowCustomValue=${0}
        item-id-path="value"
        item-value-path="value"
        item-label-path="label"
        @opened-changed=${0}
        @value-changed=${0}
      >
      </ha-combo-box>
    `),this.hass,this.value,this.autofocus,null!==(t=this.label)&&void 0!==t?t:this.hass.localize("ui.components.entity.entity-attribute-picker.attribute"),this.disabled||!this.entityId,this.required,this.helper,this.allowCustomValue,this._openedChanged,this._valueChanged):a.Ld}get _value(){return this.value||""}_openedChanged(t){this._opened=t.detail.value}_valueChanged(t){t.stopPropagation();const e=t.detail.value;e!==this._value&&this._setValue(e)}_setValue(t){this.value=t,setTimeout((()=>{(0,d.B)(this,"value-changed",{value:t}),(0,d.B)(this,"change")}),0)}constructor(...t){super(...t),this.autofocus=!1,this.disabled=!1,this.required=!1,this._opened=!1}}(0,i.__decorate)([(0,r.Cb)({attribute:!1})],c.prototype,"hass",void 0),(0,i.__decorate)([(0,r.Cb)({attribute:!1})],c.prototype,"entityId",void 0),(0,i.__decorate)([(0,r.Cb)({type:Array,attribute:"hide-attributes"})],c.prototype,"hideAttributes",void 0),(0,i.__decorate)([(0,r.Cb)({type:Boolean})],c.prototype,"autofocus",void 0),(0,i.__decorate)([(0,r.Cb)({type:Boolean})],c.prototype,"disabled",void 0),(0,i.__decorate)([(0,r.Cb)({type:Boolean})],c.prototype,"required",void 0),(0,i.__decorate)([(0,r.Cb)({type:Boolean,attribute:"allow-custom-value"})],c.prototype,"allowCustomValue",void 0),(0,i.__decorate)([(0,r.Cb)()],c.prototype,"label",void 0),(0,i.__decorate)([(0,r.Cb)()],c.prototype,"value",void 0),(0,i.__decorate)([(0,r.Cb)()],c.prototype,"helper",void 0),(0,i.__decorate)([(0,r.SB)()],c.prototype,"_opened",void 0),(0,i.__decorate)([(0,r.IO)("ha-combo-box",!0)],c.prototype,"_comboBox",void 0),c=(0,i.__decorate)([(0,r.Mo)("ha-entity-attribute-picker")],c),e()}catch(h){e(h)}}))},58558:function(t,e,o){o.a(t,(async function(t,i){try{o.r(e),o.d(e,{HaSelectorAttribute:function(){return p}});o(26847),o(81738),o(72489),o(27530);var a=o(73742),r=o(59048),s=o(7616),d=o(29740),l=o(81758),u=o(74608),h=t([l]);l=(h.then?(await h)():h)[0];let n,c=t=>t;class p extends r.oi{render(){var t,e,o;return(0,r.dy)(n||(n=c`
      <ha-entity-attribute-picker
        .hass=${0}
        .entityId=${0}
        .hideAttributes=${0}
        .value=${0}
        .label=${0}
        .helper=${0}
        .disabled=${0}
        .required=${0}
        allow-custom-value
      ></ha-entity-attribute-picker>
    `),this.hass,(null===(t=this.selector.attribute)||void 0===t?void 0:t.entity_id)||(null===(e=this.context)||void 0===e?void 0:e.filter_entity),null===(o=this.selector.attribute)||void 0===o?void 0:o.hide_attributes,this.value,this.label,this.helper,this.disabled,this.required)}updated(t){var e;if(super.updated(t),!this.value||null!==(e=this.selector.attribute)&&void 0!==e&&e.entity_id||!t.has("context"))return;const o=t.get("context");if(!this.context||!o||o.filter_entity===this.context.filter_entity)return;let i=!1;if(this.context.filter_entity){i=!(0,u.r)(this.context.filter_entity).some((t=>{const e=this.hass.states[t];return e&&this.value in e.attributes&&void 0!==e.attributes[this.value]}))}else i=void 0!==this.value;i&&(0,d.B)(this,"value-changed",{value:void 0})}constructor(...t){super(...t),this.disabled=!1,this.required=!0}}(0,a.__decorate)([(0,s.Cb)({attribute:!1})],p.prototype,"hass",void 0),(0,a.__decorate)([(0,s.Cb)({attribute:!1})],p.prototype,"selector",void 0),(0,a.__decorate)([(0,s.Cb)()],p.prototype,"value",void 0),(0,a.__decorate)([(0,s.Cb)()],p.prototype,"label",void 0),(0,a.__decorate)([(0,s.Cb)()],p.prototype,"helper",void 0),(0,a.__decorate)([(0,s.Cb)({type:Boolean})],p.prototype,"disabled",void 0),(0,a.__decorate)([(0,s.Cb)({type:Boolean})],p.prototype,"required",void 0),(0,a.__decorate)([(0,s.Cb)({attribute:!1})],p.prototype,"context",void 0),p=(0,a.__decorate)([(0,s.Mo)("ha-selector-attribute")],p),i()}catch(n){i(n)}}))}}]);
//# sourceMappingURL=8552.2a6d43a6a5caa978.js.map