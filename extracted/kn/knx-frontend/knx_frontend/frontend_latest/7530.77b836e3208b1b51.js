export const __webpack_ids__=["7530"];export const __webpack_modules__={35505:function(e,t,i){i.d(t,{K:()=>a});const a=e=>{switch(e.language){case"cs":case"de":case"fi":case"fr":case"sk":case"sv":return" ";default:return""}}},34998:function(e,t,i){i.a(e,(async function(e,t){try{var a=i(73742),o=(i(1051),i(59048)),s=i(7616),r=i(31733),l=i(29740),n=i(30337),d=(i(78645),i(35505)),c=i(74608),p=i(57874),h=e([n]);n=(h.then?(await h)():h)[0];const u="M19,4H15.5L14.5,3H9.5L8.5,4H5V6H19M6,19A2,2 0 0,0 8,21H16A2,2 0 0,0 18,19V7H6V19Z",g="M14,2H6A2,2 0 0,0 4,4V20A2,2 0 0,0 6,22H18A2,2 0 0,0 20,20V8L14,2M13.5,16V19H10.5V16H8L12,12L16,16H13.5M13,9V3.5L18.5,9H13Z";class v extends o.oi{firstUpdated(e){super.firstUpdated(e),this.autoOpenFileDialog&&this._openFilePicker()}get _name(){if(void 0===this.value)return"";if("string"==typeof this.value)return this.value;return(this.value instanceof FileList?Array.from(this.value):(0,c.r)(this.value)).map((e=>e.name)).join(", ")}render(){const e=this.localize||this.hass.localize;return o.dy`
      ${this.uploading?o.dy`<div class="container">
            <div class="uploading">
              <span class="header"
                >${this.uploadingLabel||(this.value?e("ui.components.file-upload.uploading_name",{name:this._name}):e("ui.components.file-upload.uploading"))}</span
              >
              ${this.progress?o.dy`<div class="progress">
                    ${this.progress}${this.hass&&(0,d.K)(this.hass.locale)}%
                  </div>`:o.Ld}
            </div>
            <mwc-linear-progress
              .indeterminate=${!this.progress}
              .progress=${this.progress?this.progress/100:void 0}
            ></mwc-linear-progress>
          </div>`:o.dy`<label
            for=${this.value?"":"input"}
            class="container ${(0,r.$)({dragged:this._drag,multiple:this.multiple,value:Boolean(this.value)})}"
            @drop=${this._handleDrop}
            @dragenter=${this._handleDragStart}
            @dragover=${this._handleDragStart}
            @dragleave=${this._handleDragEnd}
            @dragend=${this._handleDragEnd}
            >${this.value?"string"==typeof this.value?o.dy`<div class="row">
                    <div class="value" @click=${this._openFilePicker}>
                      <ha-svg-icon
                        .path=${this.icon||g}
                      ></ha-svg-icon>
                      ${this.value}
                    </div>
                    <ha-icon-button
                      @click=${this._clearValue}
                      .label=${this.deleteLabel||e("ui.common.delete")}
                      .path=${u}
                    ></ha-icon-button>
                  </div>`:(this.value instanceof FileList?Array.from(this.value):(0,c.r)(this.value)).map((t=>o.dy`<div class="row">
                        <div class="value" @click=${this._openFilePicker}>
                          <ha-svg-icon
                            .path=${this.icon||g}
                          ></ha-svg-icon>
                          ${t.name} - ${(0,p.d)(t.size)}
                        </div>
                        <ha-icon-button
                          @click=${this._clearValue}
                          .label=${this.deleteLabel||e("ui.common.delete")}
                          .path=${u}
                        ></ha-icon-button>
                      </div>`)):o.dy`<ha-button
                    size="small"
                    appearance="filled"
                    @click=${this._openFilePicker}
                  >
                    <ha-svg-icon
                      slot="start"
                      .path=${this.icon||g}
                    ></ha-svg-icon>
                    ${this.label||e("ui.components.file-upload.label")}
                  </ha-button>
                  <span class="secondary"
                    >${this.secondary||e("ui.components.file-upload.secondary")}</span
                  >
                  <span class="supports">${this.supports}</span>`}
            <input
              id="input"
              type="file"
              class="file"
              .accept=${this.accept}
              .multiple=${this.multiple}
              @change=${this._handleFilePicked}
          /></label>`}
    `}_openFilePicker(){this._input?.click()}_handleDrop(e){e.preventDefault(),e.stopPropagation(),e.dataTransfer?.files&&(0,l.B)(this,"file-picked",{files:this.multiple||1===e.dataTransfer.files.length?Array.from(e.dataTransfer.files):[e.dataTransfer.files[0]]}),this._drag=!1}_handleDragStart(e){e.preventDefault(),e.stopPropagation(),this._drag=!0}_handleDragEnd(e){e.preventDefault(),e.stopPropagation(),this._drag=!1}_handleFilePicked(e){0!==e.target.files.length&&(this.value=e.target.files,(0,l.B)(this,"file-picked",{files:e.target.files}))}_clearValue(e){e.preventDefault(),this._input.value="",this.value=void 0,(0,l.B)(this,"change"),(0,l.B)(this,"files-cleared")}constructor(...e){super(...e),this.multiple=!1,this.disabled=!1,this.uploading=!1,this.autoOpenFileDialog=!1,this._drag=!1}}v.styles=o.iv`
    :host {
      display: block;
      height: 240px;
    }
    :host([disabled]) {
      pointer-events: none;
      color: var(--disabled-text-color);
    }
    .container {
      position: relative;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      border: solid 1px
        var(--mdc-text-field-idle-line-color, rgba(0, 0, 0, 0.42));
      border-radius: var(--mdc-shape-small, 4px);
      height: 100%;
    }
    .row {
      display: flex;
      align-items: center;
    }
    label.container {
      border: dashed 1px
        var(--mdc-text-field-idle-line-color, rgba(0, 0, 0, 0.42));
      cursor: pointer;
    }
    .container .uploading {
      display: flex;
      flex-direction: column;
      width: 100%;
      align-items: flex-start;
      padding: 0 32px;
      box-sizing: border-box;
    }
    :host([disabled]) .container {
      border-color: var(--disabled-color);
    }
    label:hover,
    label.dragged {
      border-style: solid;
    }
    label.dragged {
      border-color: var(--primary-color);
    }
    .dragged:before {
      position: absolute;
      top: 0;
      right: 0;
      bottom: 0;
      left: 0;
      background-color: var(--primary-color);
      content: "";
      opacity: var(--dark-divider-opacity);
      pointer-events: none;
      border-radius: var(--mdc-shape-small, 4px);
    }
    label.value {
      cursor: default;
    }
    label.value.multiple {
      justify-content: unset;
      overflow: auto;
    }
    .highlight {
      color: var(--primary-color);
    }
    ha-button {
      margin-bottom: 8px;
    }
    .supports {
      color: var(--secondary-text-color);
      font-size: var(--ha-font-size-s);
    }
    :host([disabled]) .secondary {
      color: var(--disabled-text-color);
    }
    input.file {
      display: none;
    }
    .value {
      cursor: pointer;
    }
    .value ha-svg-icon {
      margin-right: 8px;
      margin-inline-end: 8px;
      margin-inline-start: initial;
    }
    ha-button {
      --mdc-button-outline-color: var(--primary-color);
      --mdc-icon-button-size: 24px;
    }
    mwc-linear-progress {
      width: 100%;
      padding: 8px 32px;
      box-sizing: border-box;
    }
    .header {
      font-weight: var(--ha-font-weight-medium);
    }
    .progress {
      color: var(--secondary-text-color);
    }
    button.link {
      background: none;
      border: none;
      padding: 0;
      font-size: var(--ha-font-size-m);
      color: var(--primary-color);
      text-decoration: underline;
      cursor: pointer;
    }
  `,(0,a.__decorate)([(0,s.Cb)({attribute:!1})],v.prototype,"hass",void 0),(0,a.__decorate)([(0,s.Cb)({attribute:!1})],v.prototype,"localize",void 0),(0,a.__decorate)([(0,s.Cb)()],v.prototype,"accept",void 0),(0,a.__decorate)([(0,s.Cb)()],v.prototype,"icon",void 0),(0,a.__decorate)([(0,s.Cb)()],v.prototype,"label",void 0),(0,a.__decorate)([(0,s.Cb)()],v.prototype,"secondary",void 0),(0,a.__decorate)([(0,s.Cb)({attribute:"uploading-label"})],v.prototype,"uploadingLabel",void 0),(0,a.__decorate)([(0,s.Cb)({attribute:"delete-label"})],v.prototype,"deleteLabel",void 0),(0,a.__decorate)([(0,s.Cb)()],v.prototype,"supports",void 0),(0,a.__decorate)([(0,s.Cb)({type:Object})],v.prototype,"value",void 0),(0,a.__decorate)([(0,s.Cb)({type:Boolean})],v.prototype,"multiple",void 0),(0,a.__decorate)([(0,s.Cb)({type:Boolean,reflect:!0})],v.prototype,"disabled",void 0),(0,a.__decorate)([(0,s.Cb)({type:Boolean})],v.prototype,"uploading",void 0),(0,a.__decorate)([(0,s.Cb)({type:Number})],v.prototype,"progress",void 0),(0,a.__decorate)([(0,s.Cb)({type:Boolean,attribute:"auto-open-file-dialog"})],v.prototype,"autoOpenFileDialog",void 0),(0,a.__decorate)([(0,s.SB)()],v.prototype,"_drag",void 0),(0,a.__decorate)([(0,s.IO)("#input")],v.prototype,"_input",void 0),v=(0,a.__decorate)([(0,s.Mo)("ha-file-upload")],v),t()}catch(u){t(u)}}))},73186:function(e,t,i){i.a(e,(async function(e,t){try{var a=i(73742),o=i(59048),s=i(7616),r=i(29740),l=i(77204),n=i(93881),d=i(81665),c=i(62521),p=i(30337),h=i(34998),u=i(91268),g=e([p,h]);[p,h]=g.then?(await g)():g;const v="M18 15V18H15V20H18V23H20V20H23V18H20V15H18M13.3 21H5C3.9 21 3 20.1 3 19V5C3 3.9 3.9 3 5 3H19C20.1 3 21 3.9 21 5V13.3C20.4 13.1 19.7 13 19 13C17.9 13 16.8 13.3 15.9 13.9L14.5 12L11 16.5L8.5 13.5L5 18H13.1C13 18.3 13 18.7 13 19C13 19.7 13.1 20.4 13.3 21Z";class _ extends o.oi{render(){if(!this.value){const e=this.secondary||(this.selectMedia?o.dy`${this.hass.localize("ui.components.picture-upload.secondary",{select_media:o.dy`<button
                  class="link"
                  @click=${this._chooseMedia}
                >
                  ${this.hass.localize("ui.components.picture-upload.select_media")}
                </button>`})}`:void 0);return o.dy`
        <ha-file-upload
          .hass=${this.hass}
          .icon=${v}
          .label=${this.label||this.hass.localize("ui.components.picture-upload.label")}
          .secondary=${e}
          .supports=${this.supports||this.hass.localize("ui.components.picture-upload.supported_formats")}
          .uploading=${this._uploading}
          @file-picked=${this._handleFilePicked}
          @change=${this._handleFileCleared}
          accept="image/png, image/jpeg, image/gif"
        ></ha-file-upload>
      `}return o.dy`<div class="center-vertical">
      <div class="value">
        <img
          .src=${this.value}
          alt=${this.currentImageAltText||this.hass.localize("ui.components.picture-upload.current_image_alt")}
        />
        <div>
          <ha-button
            appearance="plain"
            size="small"
            variant="danger"
            @click=${this._handleChangeClick}
          >
            ${this.hass.localize("ui.components.picture-upload.clear_picture")}
          </ha-button>
        </div>
      </div>
    </div>`}_handleChangeClick(){this.value=null,(0,r.B)(this,"change")}async _handleFilePicked(e){const t=e.detail.files[0];this.crop?this._cropFile(t):this._uploadFile(t)}async _handleFileCleared(){this.value=null}async _cropFile(e,t){["image/png","image/jpeg","image/gif"].includes(e.type)?(0,c.E)(this,{file:e,options:this.cropOptions||{round:!1,aspectRatio:NaN},croppedCallback:i=>{t&&i===e?(this.value=(0,n.p6)(t,this.size,this.original),(0,r.B)(this,"change")):this._uploadFile(i)}}):(0,d.Ys)(this,{text:this.hass.localize("ui.components.picture-upload.unsupported_format")})}async _uploadFile(e){if(["image/png","image/jpeg","image/gif"].includes(e.type)){this._uploading=!0;try{const t=await(0,n.Bi)(this.hass,e);this.value=(0,n.p6)(t.id,this.size,this.original),(0,r.B)(this,"change")}catch(t){(0,d.Ys)(this,{text:t.toString()})}finally{this._uploading=!1}}else(0,d.Ys)(this,{text:this.hass.localize("ui.components.picture-upload.unsupported_format")})}static get styles(){return[l.Qx,o.iv`
        :host {
          display: block;
          height: 240px;
        }
        ha-file-upload {
          height: 100%;
        }
        .center-vertical {
          display: flex;
          align-items: center;
          height: 100%;
        }
        .value {
          width: 100%;
          display: flex;
          flex-direction: column;
          align-items: center;
        }
        img {
          max-width: 100%;
          max-height: 200px;
          margin-bottom: 4px;
          border-radius: var(--file-upload-image-border-radius);
          transition: opacity 0.3s;
          opacity: var(--picture-opacity, 1);
        }
        img:hover {
          opacity: 1;
        }
      `]}constructor(...e){super(...e),this.value=null,this.crop=!1,this.selectMedia=!1,this.original=!1,this.size=512,this._uploading=!1,this._chooseMedia=()=>{(0,u.B)(this,{action:"pick",entityId:"browser",navigateIds:[{media_content_id:void 0,media_content_type:void 0},{media_content_id:n.dg,media_content_type:"app"}],minimumNavigateLevel:2,mediaPickedCallback:async e=>{const t=(0,n.TT)(e.item.media_content_id);if(t)if(this.crop){const a=(0,n.p6)(t,void 0,!0);let o;try{o=await(0,n.n$)(this.hass,a)}catch(i){return void(0,d.Ys)(this,{text:i.toString()})}const s={type:e.item.media_content_type},r=new File([o],e.item.title,s);this._cropFile(r,t)}else this.value=(0,n.p6)(t,this.size,this.original),(0,r.B)(this,"change")}})}}}(0,a.__decorate)([(0,s.Cb)()],_.prototype,"value",void 0),(0,a.__decorate)([(0,s.Cb)()],_.prototype,"label",void 0),(0,a.__decorate)([(0,s.Cb)()],_.prototype,"secondary",void 0),(0,a.__decorate)([(0,s.Cb)()],_.prototype,"supports",void 0),(0,a.__decorate)([(0,s.Cb)({attribute:!1})],_.prototype,"currentImageAltText",void 0),(0,a.__decorate)([(0,s.Cb)({type:Boolean})],_.prototype,"crop",void 0),(0,a.__decorate)([(0,s.Cb)({type:Boolean,attribute:"select-media"})],_.prototype,"selectMedia",void 0),(0,a.__decorate)([(0,s.Cb)({attribute:!1})],_.prototype,"cropOptions",void 0),(0,a.__decorate)([(0,s.Cb)({type:Boolean})],_.prototype,"original",void 0),(0,a.__decorate)([(0,s.Cb)({type:Number})],_.prototype,"size",void 0),(0,a.__decorate)([(0,s.SB)()],_.prototype,"_uploading",void 0),_=(0,a.__decorate)([(0,s.Mo)("ha-picture-upload")],_),t()}catch(v){t(v)}}))},91268:function(e,t,i){i.d(t,{B:()=>o});var a=i(29740);const o=(e,t)=>{(0,a.B)(e,"show-dialog",{dialogTag:"dialog-media-player-browse",dialogImport:()=>Promise.all([i.e("2092"),i.e("5593"),i.e("8167"),i.e("3982"),i.e("9442")]).then(i.bind(i,50555)),dialogParams:t})}},93881:function(e,t,i){i.d(t,{Bi:()=>l,JS:()=>a,TT:()=>s,ao:()=>n,dg:()=>o,n$:()=>d,p6:()=>r});const a="/api/image/serve/",o="media-source://image_upload",s=e=>{let t;if(e.startsWith(a)){t=e.substring(a.length);const i=t.indexOf("/");i>=0&&(t=t.substring(0,i))}else e.startsWith(o)&&(t=e.substring(o.length+1));return t},r=(e,t,i=!1)=>{if(!i&&!t)throw new Error("Size must be provided if original is false");return i?`/api/image/serve/${e}/original`:`/api/image/serve/${e}/${t}x${t}`},l=async(e,t)=>{const i=new FormData;i.append("file",t);const a=await e.fetchWithAuth("/api/image/upload",{method:"POST",body:i});if(413===a.status)throw new Error(`Uploaded image is too large (${t.name})`);if(200!==a.status)throw new Error("Unknown error");return a.json()},n=(e,t)=>e.callWS({type:"image/delete",image_id:t}),d=async(e,t)=>{const i=await fetch(e.hassUrl(t));if(!i.ok)throw new Error(`Failed to fetch image: ${i.statusText?i.statusText:i.status}`);return i.blob()}},62521:function(e,t,i){i.d(t,{E:()=>s});var a=i(29740);const o=()=>Promise.all([i.e("8807"),i.e("6570")]).then(i.bind(i,72199)),s=(e,t)=>{(0,a.B)(e,"show-dialog",{dialogTag:"image-cropper-dialog",dialogImport:o,dialogParams:t})}},57874:function(e,t,i){i.d(t,{d:()=>a});const a=(e=0,t=2)=>{if(0===e)return"0 Bytes";t=t<0?0:t;const i=Math.floor(Math.log(e)/Math.log(1024));return`${parseFloat((e/1024**i).toFixed(t))} ${["Bytes","KB","MB","GB","TB","PB","EB","ZB","YB"][i]}`}}};
//# sourceMappingURL=7530.77b836e3208b1b51.js.map