export const __webpack_ids__=["1316"];export const __webpack_modules__={75972:function(e,t,a){a.a(e,(async function(e,s){try{a.d(t,{u:()=>n});var i=a(57900),o=a(28105),l=e([i]);i=(l.then?(await l)():l)[0];const n=(e,t)=>{try{return r(t)?.of(e)??e}catch{return e}},r=(0,o.Z)((e=>new Intl.DisplayNames(e.language,{type:"language",fallback:"code"})));s()}catch(n){s(n)}}))},86352:function(e,t,a){a.a(e,(async function(e,s){try{a.d(t,{C:()=>_});var i=a(57900),o=a(73742),l=a(59048),n=a(7616),r=a(28105),u=a(29740),d=a(41806),h=a(75972),c=a(92949),g=a(18447),p=(a(93795),a(29490),e([i,h]));[i,h]=p.then?(await p)():p;const _=(e,t,a,s)=>{let i=[];if(t){const t=g.o.translations;i=e.map((e=>{let a=t[e]?.nativeName;if(!a)try{a=new Intl.DisplayNames(e,{type:"language",fallback:"code"}).of(e)}catch(s){a=e}return{value:e,label:a}}))}else s&&(i=e.map((e=>({value:e,label:(0,h.u)(e,s)}))));return!a&&s&&i.sort(((e,t)=>(0,c.fe)(e.label,t.label,s.language))),i};class v extends l.oi{firstUpdated(e){super.firstUpdated(e),this._computeDefaultLanguageOptions()}updated(e){super.updated(e);const t=e.has("hass")&&this.hass&&e.get("hass")&&e.get("hass").locale.language!==this.hass.locale.language;if(e.has("languages")||e.has("value")||t){if(this._select.layoutOptions(),this.disabled||this._select.value===this.value||(0,u.B)(this,"value-changed",{value:this._select.value}),!this.value)return;const e=this._getLanguagesOptions(this.languages??this._defaultLanguages,this.nativeName,this.noSort,this.hass?.locale).findIndex((e=>e.value===this.value));-1===e&&(this.value=void 0),t&&this._select.select(e)}}_computeDefaultLanguageOptions(){this._defaultLanguages=Object.keys(g.o.translations)}render(){const e=this._getLanguagesOptions(this.languages??this._defaultLanguages,this.nativeName,this.noSort,this.hass?.locale),t=this.value??(this.required&&!this.disabled?e[0]?.value:this.value);return l.dy`
      <ha-select
        .label=${this.label??(this.hass?.localize("ui.components.language-picker.language")||"Language")}
        .value=${t||""}
        .required=${this.required}
        .disabled=${this.disabled}
        @selected=${this._changed}
        @closed=${d.U}
        fixedMenuPosition
        naturalMenuWidth
        .inlineArrow=${this.inlineArrow}
      >
        ${0===e.length?l.dy`<ha-list-item value=""
              >${this.hass?.localize("ui.components.language-picker.no_languages")||"No languages"}</ha-list-item
            >`:e.map((e=>l.dy`
                <ha-list-item .value=${e.value}
                  >${e.label}</ha-list-item
                >
              `))}
      </ha-select>
    `}_changed(e){const t=e.target;this.disabled||""===t.value||t.value===this.value||(this.value=t.value,(0,u.B)(this,"value-changed",{value:this.value}))}constructor(...e){super(...e),this.disabled=!1,this.required=!1,this.nativeName=!1,this.noSort=!1,this.inlineArrow=!1,this._defaultLanguages=[],this._getLanguagesOptions=(0,r.Z)(_)}}v.styles=l.iv`
    ha-select {
      width: 100%;
    }
  `,(0,o.__decorate)([(0,n.Cb)()],v.prototype,"value",void 0),(0,o.__decorate)([(0,n.Cb)()],v.prototype,"label",void 0),(0,o.__decorate)([(0,n.Cb)({type:Array})],v.prototype,"languages",void 0),(0,o.__decorate)([(0,n.Cb)({attribute:!1})],v.prototype,"hass",void 0),(0,o.__decorate)([(0,n.Cb)({type:Boolean,reflect:!0})],v.prototype,"disabled",void 0),(0,o.__decorate)([(0,n.Cb)({type:Boolean})],v.prototype,"required",void 0),(0,o.__decorate)([(0,n.Cb)({attribute:"native-name",type:Boolean})],v.prototype,"nativeName",void 0),(0,o.__decorate)([(0,n.Cb)({attribute:"no-sort",type:Boolean})],v.prototype,"noSort",void 0),(0,o.__decorate)([(0,n.Cb)({attribute:"inline-arrow",type:Boolean})],v.prototype,"inlineArrow",void 0),(0,o.__decorate)([(0,n.SB)()],v.prototype,"_defaultLanguages",void 0),(0,o.__decorate)([(0,n.IO)("ha-select")],v.prototype,"_select",void 0),v=(0,o.__decorate)([(0,n.Mo)("ha-language-picker")],v),s()}catch(_){s(_)}}))},50736:function(e,t,a){a.a(e,(async function(e,s){try{a.r(t),a.d(t,{HaLanguageSelector:()=>u});var i=a(73742),o=a(59048),l=a(7616),n=a(86352),r=e([n]);n=(r.then?(await r)():r)[0];class u extends o.oi{render(){return o.dy`
      <ha-language-picker
        .hass=${this.hass}
        .value=${this.value}
        .label=${this.label}
        .helper=${this.helper}
        .languages=${this.selector.language?.languages}
        .nativeName=${Boolean(this.selector?.language?.native_name)}
        .noSort=${Boolean(this.selector?.language?.no_sort)}
        .disabled=${this.disabled}
        .required=${this.required}
      ></ha-language-picker>
    `}constructor(...e){super(...e),this.disabled=!1,this.required=!0}}u.styles=o.iv`
    ha-language-picker {
      width: 100%;
    }
  `,(0,i.__decorate)([(0,l.Cb)({attribute:!1})],u.prototype,"hass",void 0),(0,i.__decorate)([(0,l.Cb)({attribute:!1})],u.prototype,"selector",void 0),(0,i.__decorate)([(0,l.Cb)()],u.prototype,"value",void 0),(0,i.__decorate)([(0,l.Cb)()],u.prototype,"label",void 0),(0,i.__decorate)([(0,l.Cb)()],u.prototype,"helper",void 0),(0,i.__decorate)([(0,l.Cb)({type:Boolean})],u.prototype,"disabled",void 0),(0,i.__decorate)([(0,l.Cb)({type:Boolean})],u.prototype,"required",void 0),u=(0,i.__decorate)([(0,l.Mo)("ha-selector-language")],u),s()}catch(u){s(u)}}))}};
//# sourceMappingURL=1316.4dc2847c0634cf1b.js.map