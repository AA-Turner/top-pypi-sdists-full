export const __webpack_ids__=["9494"];export const __webpack_modules__={26274:function(e,t,s){s.r(t),s.d(t,{HaBackupLocationSelector:()=>m});var o=s(73742),a=s(59048),i=s(7616),r=s(28105),u=s(42822),n=s(29740),h=s(41806),l=s(92949),d=function(e){return e.BIND="bind",e.CIFS="cifs",e.NFS="nfs",e}({}),p=function(e){return e.BACKUP="backup",e.MEDIA="media",e.SHARE="share",e}({});s(22543),s(93795),s(29490);const c="/backup";class _ extends a.oi{firstUpdated(){this._getMounts()}render(){if(this._error)return a.dy`<ha-alert alert-type="error">${this._error}</ha-alert>`;if(!this._mounts)return a.Ld;const e=a.dy`<ha-list-item
      graphic="icon"
      .value=${c}
    >
      <span>
        ${this.hass.localize("ui.components.mount-picker.use_datadisk")||"Use data disk for backup"}
      </span>
      <ha-svg-icon slot="graphic" .path=${"M6,2H18A2,2 0 0,1 20,4V20A2,2 0 0,1 18,22H6A2,2 0 0,1 4,20V4A2,2 0 0,1 6,2M12,4A6,6 0 0,0 6,10C6,13.31 8.69,16 12.1,16L11.22,13.77C10.95,13.29 11.11,12.68 11.59,12.4L12.45,11.9C12.93,11.63 13.54,11.79 13.82,12.27L15.74,14.69C17.12,13.59 18,11.9 18,10A6,6 0 0,0 12,4M12,9A1,1 0 0,1 13,10A1,1 0 0,1 12,11A1,1 0 0,1 11,10A1,1 0 0,1 12,9M7,18A1,1 0 0,0 6,19A1,1 0 0,0 7,20A1,1 0 0,0 8,19A1,1 0 0,0 7,18M12.09,13.27L14.58,19.58L17.17,18.08L12.95,12.77L12.09,13.27Z"}></ha-svg-icon>
    </ha-list-item>`;return a.dy`
      <ha-select
        .label=${void 0===this.label&&this.hass?this.hass.localize("ui.components.mount-picker.mount"):this.label}
        .value=${this._value}
        .required=${this.required}
        .disabled=${this.disabled}
        .helper=${this.helper}
        @selected=${this._mountChanged}
        @closed=${h.U}
        fixedMenuPosition
        naturalMenuWidth
      >
        ${this.usage!==p.BACKUP||this._mounts.default_backup_mount&&this._mounts.default_backup_mount!==c?a.Ld:e}
        ${this._filterMounts(this._mounts,this.usage).map((e=>a.dy`<ha-list-item twoline graphic="icon" .value=${e.name}>
              <span>${e.name}</span>
              <span slot="secondary"
                >${e.server}${e.port?`:${e.port}`:a.Ld}${e.type===d.NFS?e.path:`:${e.share}`}</span
              >
              <ha-svg-icon
                slot="graphic"
                .path=${e.usage===p.MEDIA?"M19 3H5C3.89 3 3 3.89 3 5V19C3 20.1 3.9 21 5 21H19C20.1 21 21 20.1 21 19V5C21 3.89 20.1 3 19 3M10 16V8L15 12":e.usage===p.SHARE?"M10,4H4C2.89,4 2,4.89 2,6V18A2,2 0 0,0 4,20H20A2,2 0 0,0 22,18V8C22,6.89 21.1,6 20,6H12L10,4Z":"M12,3A9,9 0 0,0 3,12H0L4,16L8,12H5A7,7 0 0,1 12,5A7,7 0 0,1 19,12A7,7 0 0,1 12,19C10.5,19 9.09,18.5 7.94,17.7L6.5,19.14C8.04,20.3 9.94,21 12,21A9,9 0 0,0 21,12A9,9 0 0,0 12,3M14,12A2,2 0 0,0 12,10A2,2 0 0,0 10,12A2,2 0 0,0 12,14A2,2 0 0,0 14,12Z"}
              ></ha-svg-icon>
            </ha-list-item>`))}
        ${this.usage===p.BACKUP&&this._mounts.default_backup_mount?e:a.Ld}
      </ha-select>
    `}async _getMounts(){try{(0,u.p)(this.hass,"hassio")?(this._mounts=await(async e=>e.callWS({type:"supervisor/api",endpoint:"/mounts",method:"get",timeout:null}))(this.hass),this.usage!==p.BACKUP||this.value||(this.value=this._mounts.default_backup_mount||c)):this._error=this.hass.localize("ui.components.mount-picker.error.no_supervisor")}catch(e){this._error=this.hass.localize("ui.components.mount-picker.error.fetch_mounts")}}get _value(){return this.value||""}_mountChanged(e){e.stopPropagation();const t=e.target.value;t!==this._value&&this._setValue(t)}_setValue(e){this.value=e,setTimeout((()=>{(0,n.B)(this,"value-changed",{value:e}),(0,n.B)(this,"change")}),0)}static get styles(){return[a.iv`
        ha-select {
          width: 100%;
        }
      `]}constructor(...e){super(...e),this.disabled=!1,this.required=!1,this._filterMounts=(0,r.Z)(((e,t)=>{let s=e.mounts.filter((e=>[d.CIFS,d.NFS].includes(e.type)));return t&&(s=e.mounts.filter((e=>e.usage===t))),s.sort(((t,s)=>t.name===e.default_backup_mount?-1:s.name===e.default_backup_mount?1:(0,l.fe)(t.name,s.name,this.hass.locale.language)))}))}}(0,o.__decorate)([(0,i.Cb)()],_.prototype,"label",void 0),(0,o.__decorate)([(0,i.Cb)()],_.prototype,"value",void 0),(0,o.__decorate)([(0,i.Cb)()],_.prototype,"helper",void 0),(0,o.__decorate)([(0,i.Cb)({type:Boolean})],_.prototype,"disabled",void 0),(0,o.__decorate)([(0,i.Cb)({type:Boolean})],_.prototype,"required",void 0),(0,o.__decorate)([(0,i.Cb)()],_.prototype,"usage",void 0),(0,o.__decorate)([(0,i.SB)()],_.prototype,"_mounts",void 0),(0,o.__decorate)([(0,i.SB)()],_.prototype,"_error",void 0),_=(0,o.__decorate)([(0,i.Mo)("ha-mount-picker")],_);class m extends a.oi{render(){return a.dy`<ha-mount-picker
      .hass=${this.hass}
      .value=${this.value}
      .label=${this.label}
      .helper=${this.helper}
      .disabled=${this.disabled}
      .required=${this.required}
      usage="backup"
    ></ha-mount-picker>`}constructor(...e){super(...e),this.disabled=!1,this.required=!0}}m.styles=a.iv`
    ha-mount-picker {
      width: 100%;
    }
  `,(0,o.__decorate)([(0,i.Cb)({attribute:!1})],m.prototype,"hass",void 0),(0,o.__decorate)([(0,i.Cb)({attribute:!1})],m.prototype,"selector",void 0),(0,o.__decorate)([(0,i.Cb)()],m.prototype,"value",void 0),(0,o.__decorate)([(0,i.Cb)()],m.prototype,"label",void 0),(0,o.__decorate)([(0,i.Cb)()],m.prototype,"helper",void 0),(0,o.__decorate)([(0,i.Cb)({type:Boolean})],m.prototype,"disabled",void 0),(0,o.__decorate)([(0,i.Cb)({type:Boolean})],m.prototype,"required",void 0),m=(0,o.__decorate)([(0,i.Mo)("ha-selector-backup_location")],m)}};
//# sourceMappingURL=9494.849d709cabeb195d.js.map