"use strict";(self.webpackChunkinsteon_frontend_home_assistant=self.webpackChunkinsteon_frontend_home_assistant||[]).push([[7765],{52996:(e,i,t)=>{t.d(i,{p:()=>a});const a=(e,i)=>e&&e.config.components.includes(i)},92295:(e,i,t)=>{var a=t(73958),n=t(30437),s=t(9644),o=t(36924),l=t(3712);(0,a.Z)([(0,o.Mo)("ha-button")],(function(e,i){return{F:class extends i{constructor(...i){super(...i),e(this)}},d:[{kind:"field",static:!0,key:"styles",value(){return[l.W,s.iv`
      ::slotted([slot="icon"]) {
        margin-inline-start: 0px;
        margin-inline-end: 8px;
        direction: var(--direction);
        display: block;
      }
      .mdc-button {
        height: var(--button-height, 36px);
      }
      .trailing-icon {
        display: flex;
      }
      .slot-container {
        overflow: var(--button-slot-container-overflow, visible);
      }
    `]}}]}}),n.z)},41911:(e,i,t)=>{var a=t(73958),n=t(9644),s=t(28111),o=t(21270),l=t(96762),d=t(36924);(0,a.Z)([(0,d.Mo)("ha-check-list-item")],(function(e,i){return{F:class extends i{constructor(...i){super(...i),e(this)}},d:[{kind:"field",static:!0,key:"styles",value(){return[l.W,o.W,n.iv`
      :host {
        --mdc-theme-secondary: var(--primary-color);
      }

      :host([graphic="avatar"]) .mdc-deprecated-list-item__graphic,
      :host([graphic="medium"]) .mdc-deprecated-list-item__graphic,
      :host([graphic="large"]) .mdc-deprecated-list-item__graphic,
      :host([graphic="control"]) .mdc-deprecated-list-item__graphic {
        margin-inline-end: var(--mdc-list-item-graphic-margin, 16px);
        margin-inline-start: 0px;
        direction: var(--direction);
      }
    `]}}]}}),s.F)},29708:(e,i,t)=>{var a=t(73958),n=t(9644),s=t(36924);t(37662);(0,a.Z)([(0,s.Mo)("ha-tip")],(function(e,i){return{F:class extends i{constructor(...i){super(...i),e(this)}},d:[{kind:"field",decorators:[(0,s.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"method",key:"render",value:function(){return this.hass?n.dy`
      <ha-svg-icon .path=${"M12,2A7,7 0 0,1 19,9C19,11.38 17.81,13.47 16,14.74V17A1,1 0 0,1 15,18H9A1,1 0 0,1 8,17V14.74C6.19,13.47 5,11.38 5,9A7,7 0 0,1 12,2M9,21V20H15V21A1,1 0 0,1 14,22H10A1,1 0 0,1 9,21M12,4A5,5 0 0,0 7,9C7,11.05 8.23,12.81 10,13.58V16H14V13.58C15.77,12.81 17,11.05 17,9A5,5 0 0,0 12,4Z"}></ha-svg-icon>
      <span class="prefix"
        >${this.hass.localize("ui.panel.config.tips.tip")}</span
      >
      <span class="text"><slot></slot></span>
    `:n.Ld}},{kind:"field",static:!0,key:"styles",value(){return n.iv`
    :host {
      display: block;
      text-align: center;
    }

    .text {
      direction: var(--direction);
      margin-left: 2px;
      margin-inline-start: 2px;
      margin-inline-end: initial;
      color: var(--secondary-text-color);
    }

    .prefix {
      font-weight: 500;
    }
  `}}]}}),n.oi)},77765:(e,i,t)=>{t.a(e,(async(e,a)=>{try{t.r(i);var n=t(73958),s=t(64801),o=(t(24103),t(44577),t(9644)),l=t(36924),d=t(86230),r=t(18394),c=t(51750),h=t(78889),u=t(23469),m=t(11285),p=t(29950),g=(t(92295),t(41911),t(7006),t(9828),t(78680),t(37662),t(29708),t(15758)),_=(t(86986),t(52996)),v=e([g]);g=(v.then?(await v)():v)[0];const f="M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z",y="M19,4H15.5L14.5,3H9.5L8.5,4H5V6H19M6,19A2,2 0 0,0 8,21H16A2,2 0 0,0 18,19V7H6V19Z";(0,n.Z)([(0,l.Mo)("dialog-media-manage")],(function(e,i){return{F:class extends i{constructor(...i){super(...i),e(this)}},d:[{kind:"field",decorators:[(0,l.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,l.SB)()],key:"_currentItem",value:void 0},{kind:"field",decorators:[(0,l.SB)()],key:"_params",value:void 0},{kind:"field",decorators:[(0,l.SB)()],key:"_uploading",value(){return!1}},{kind:"field",decorators:[(0,l.SB)()],key:"_deleting",value(){return!1}},{kind:"field",decorators:[(0,l.SB)()],key:"_selected",value(){return new Set}},{kind:"field",key:"_filesChanged",value(){return!1}},{kind:"method",key:"showDialog",value:function(e){this._params=e,this._refreshMedia()}},{kind:"method",key:"closeDialog",value:function(){this._filesChanged&&this._params.onClose&&this._params.onClose(),this._params=void 0,this._currentItem=void 0,this._uploading=!1,this._deleting=!1,this._filesChanged=!1,(0,r.B)(this,"dialog-closed",{dialog:this.localName})}},{kind:"method",key:"render",value:function(){var e,i;if(!this._params)return o.Ld;const t=(null===(e=this._currentItem)||void 0===e||null===(e=e.children)||void 0===e?void 0:e.filter((e=>!e.can_expand)))||[];let a=0;return o.dy`
      <ha-dialog
        open
        scrimClickAction
        escapeKeyAction
        hideActions
        flexContent
        .heading=${this._params.currentItem.title}
        @closed=${this.closeDialog}
      >
        <ha-dialog-header slot="heading">
          ${0===this._selected.size?o.dy`
                <span slot="title">
                  ${this.hass.localize("ui.components.media-browser.file_management.title")}
                </span>

                <ha-media-upload-button
                  .disabled=${this._deleting}
                  .hass=${this.hass}
                  .currentItem=${this._params.currentItem}
                  @uploading=${this._startUploading}
                  @media-refresh=${this._doneUploading}
                  slot="actionItems"
                ></ha-media-upload-button>
                ${this._uploading?"":o.dy`
                      <ha-icon-button
                        .label=${this.hass.localize("ui.dialogs.generic.close")}
                        .path=${f}
                        dialogAction="close"
                        slot="navigationIcon"
                        dir=${(0,c.Zu)(this.hass)}
                      ></ha-icon-button>
                    `}
              `:o.dy`
                <ha-button
                  class="danger"
                  slot="title"
                  .disabled=${this._deleting}
                  .label=${this.hass.localize("ui.components.media-browser.file_management."+(this._deleting?"deleting":"delete"),{count:this._selected.size})}
                  @click=${this._handleDelete}
                >
                  <ha-svg-icon .path=${y} slot="icon"></ha-svg-icon>
                </ha-button>

                ${this._deleting?"":o.dy`
                      <ha-button
                        slot="actionItems"
                        .label=${"Deselect all"}
                        @click=${this._handleDeselectAll}
                      >
                        <ha-svg-icon
                          .path=${f}
                          slot="icon"
                        ></ha-svg-icon>
                      </ha-button>
                    `}
              `}
        </ha-dialog-header>
        ${this._currentItem?t.length?o.dy`
                <mwc-list multi @selected=${this._handleSelected}>
                  ${(0,d.r)(t,(e=>e.media_content_id),(e=>{const i=o.dy`
                        <ha-svg-icon
                          slot="graphic"
                          .path=${h.Fn["directory"===e.media_class&&e.children_media_class||e.media_class].icon}
                        ></ha-svg-icon>
                      `;return o.dy`
                        <ha-check-list-item
                          ${(0,s.jt)({id:e.media_content_id,skipInitial:!0})}
                          graphic="icon"
                          .disabled=${this._uploading||this._deleting}
                          .selected=${this._selected.has(a++)}
                          .item=${e}
                        >
                          ${i} ${e.title}
                        </ha-check-list-item>
                      `}))}
                </mwc-list>
              `:o.dy`<div class="no-items">
                <p>
                  ${this.hass.localize("ui.components.media-browser.file_management.no_items")}
                </p>
                ${null!==(i=this._currentItem)&&void 0!==i&&null!==(i=i.children)&&void 0!==i&&i.length?o.dy`<span class="folders"
                      >${this.hass.localize("ui.components.media-browser.file_management.folders_not_supported")}</span
                    >`:""}
              </div>`:o.dy`
              <div class="refresh">
                <ha-circular-progress indeterminate></ha-circular-progress>
              </div>
            `}
        ${(0,_.p)(this.hass,"hassio")?o.dy`<ha-tip .hass=${this.hass}>
              ${this.hass.localize("ui.components.media-browser.file_management.tip_media_storage",{storage:o.dy`<a
                    href="/config/storage"
                    @click=${this.closeDialog}
                  >
                    ${this.hass.localize("ui.components.media-browser.file_management.tip_storage_panel").toLowerCase()}
                  </a>`})}
            </ha-tip>`:o.Ld}
      </ha-dialog>
    `}},{kind:"method",key:"_handleSelected",value:function(e){this._selected=e.detail.index}},{kind:"method",key:"_startUploading",value:function(){this._uploading=!0,this._filesChanged=!0}},{kind:"method",key:"_doneUploading",value:function(){this._uploading=!1,this._refreshMedia()}},{kind:"method",key:"_handleDeselectAll",value:function(){this._selected.size&&(this._selected=new Set)}},{kind:"method",key:"_handleDelete",value:async function(){if(!(await(0,m.g7)(this,{text:this.hass.localize("ui.components.media-browser.file_management.confirm_delete",{count:this._selected.size}),warning:!0})))return;this._filesChanged=!0,this._deleting=!0;const e=[];let i=0;this._currentItem.children.forEach((t=>{t.can_expand||this._selected.has(i++)&&e.push(t)}));try{await Promise.all(e.map((async e=>{await(0,u.Qr)(this.hass,e.media_content_id),this._currentItem={...this._currentItem,children:this._currentItem.children.filter((i=>i!==e))}})))}finally{this._deleting=!1,this._selected=new Set}}},{kind:"method",key:"_refreshMedia",value:async function(){this._selected=new Set,this._currentItem=void 0,this._currentItem=await(0,u.b)(this.hass,this._params.currentItem.media_content_id)}},{kind:"get",static:!0,key:"styles",value:function(){return[p.yu,o.iv`
        ha-dialog {
          --dialog-z-index: 9;
          --dialog-content-padding: 0;
        }

        @media (min-width: 800px) {
          ha-dialog {
            --mdc-dialog-max-width: 800px;
            --dialog-surface-position: fixed;
            --dialog-surface-top: 40px;
            --mdc-dialog-max-height: calc(100vh - 72px);
          }
        }

        ha-dialog-header ha-media-upload-button,
        ha-dialog-header ha-button {
          --mdc-theme-primary: var(--primary-text-color);
          margin: 6px;
          display: block;
        }

        mwc-list {
          direction: ltr;
        }

        .danger {
          --mdc-theme-primary: var(--error-color);
        }

        ha-svg-icon[slot="icon"] {
          vertical-align: middle;
        }

        ha-tip {
          margin: 16px;
        }

        ha-svg-icon[slot="icon"] {
          margin-inline-start: 0px !important;
          margin-inline-end: 8px !important;
          direction: var(--direction);
        }

        .refresh {
          display: flex;
          height: 200px;
          justify-content: center;
          align-items: center;
        }

        .no-items {
          text-align: center;
          padding: 16px;
        }
        .folders {
          color: var(--secondary-text-color);
          font-style: italic;
        }
      `]}}]}}),o.oi);a()}catch(f){a(f)}}))},86986:(e,i,t)=>{var a=t(73958),n=(t(30437),t(9644)),s=t(36924),o=t(18394),l=t(23469),d=t(11285);t(7006),t(37662);(0,a.Z)([(0,s.Mo)("ha-media-upload-button")],(function(e,i){return{F:class extends i{constructor(...i){super(...i),e(this)}},d:[{kind:"field",decorators:[(0,s.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,s.Cb)()],key:"currentItem",value:void 0},{kind:"field",decorators:[(0,s.SB)()],key:"_uploading",value(){return 0}},{kind:"method",key:"render",value:function(){return this.currentItem&&(0,l.aV)(this.currentItem.media_content_id||"")?n.dy`
      <mwc-button
        .label=${this._uploading>0?this.hass.localize("ui.components.media-browser.file_management.uploading",{count:this._uploading}):this.hass.localize("ui.components.media-browser.file_management.add_media")}
        .disabled=${this._uploading>0}
        @click=${this._startUpload}
      >
        ${this._uploading>0?n.dy`
              <ha-circular-progress
                size="tiny"
                indeterminate
                area-label="Uploading"
                slot="icon"
              ></ha-circular-progress>
            `:n.dy` <ha-svg-icon .path=${"M9,16V10H5L12,3L19,10H15V16H9M5,20V18H19V20H5Z"} slot="icon"></ha-svg-icon> `}
      </mwc-button>
    `:n.Ld}},{kind:"method",key:"_startUpload",value:async function(){if(this._uploading>0)return;const e=document.createElement("input");e.type="file",e.accept="audio/*,video/*,image/*",e.multiple=!0,e.addEventListener("change",(async()=>{(0,o.B)(this,"uploading");const i=e.files;document.body.removeChild(e);const t=this.currentItem.media_content_id;for(let e=0;e<i.length;e++){this._uploading=i.length-e;try{await(0,l.oE)(this.hass,t,i[e])}catch(a){(0,d.Ys)(this,{text:this.hass.localize("ui.components.media-browser.file_management.upload_failed",{reason:a.message||a})});break}}this._uploading=0,(0,o.B)(this,"media-refresh")}),{once:!0}),e.style.display="none",document.body.append(e),e.click()}},{kind:"field",static:!0,key:"styles",value(){return n.iv`
    mwc-button {
      /* We use icon + text to show disabled state */
      --mdc-button-disabled-ink-color: --mdc-theme-primary;
    }

    ha-svg-icon[slot="icon"],
    ha-circular-progress[slot="icon"] {
      vertical-align: middle;
    }

    ha-svg-icon[slot="icon"] {
      margin-inline-start: 0px;
      margin-inline-end: 8px;
      direction: var(--direction);
    }
  `}}]}}),n.oi)}}]);
//# sourceMappingURL=e3717bf7.js.map