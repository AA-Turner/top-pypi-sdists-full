export const __rspack_esm_id="24901";export const __rspack_esm_ids=["24901"];export const __webpack_modules__={93444(e,t,a){var o=a(62826),i=a(96196),r=a(44457);class l extends i.WF{render(){return i.qy` <footer> <slot name="secondaryAction"></slot> <slot name="primaryAction"></slot> </footer> `}static get styles(){return[i.AH`footer{display:flex;gap:var(--ha-space-3);justify-content:flex-end;align-items:center;width:100%}`]}}l=(0,o.Cg)([(0,r.EM)("ha-dialog-footer")],l)},41060(e,t,a){a.a(e,async function(e,t){try{a(18111),a(61701);var o=a(62826),i=(a(63687),a(96196)),r=a(44457),l=a(94333),s=a(1087),d=a(18350),n=(a(26300),a(67258)),h=a(44537),c=a(46187),p=e([d]);d=(p.then?(await p)():p)[0];const u="M19,4H15.5L14.5,3H9.5L8.5,4H5V6H19M6,19A2,2 0 0,0 8,21H16A2,2 0 0,0 18,19V7H6V19Z",g="M14,2H6A2,2 0 0,0 4,4V20A2,2 0 0,0 6,22H18A2,2 0 0,0 20,20V8L14,2M13.5,16V19H10.5V16H8L12,12L16,16H13.5M13,9V3.5L18.5,9H13Z";class v extends i.WF{firstUpdated(e){super.firstUpdated(e),this.autoOpenFileDialog&&this._openFilePicker()}get _name(){if(void 0===this.value)return"";if("string"==typeof this.value)return this.value;return(this.value instanceof FileList?Array.from(this.value):(0,h.e)(this.value)).map(e=>e.name).join(", ")}render(){const e=this.localize||this.hass.localize;return i.qy` ${this.uploading?i.qy`<div class="container"> <div class="uploading"> <span class="header">${this.uploadingLabel||(this.value?e("ui.components.file-upload.uploading_name",{name:this._name}):e("ui.components.file-upload.uploading"))}</span> ${this.progress?i.qy`<div class="progress"> ${this.progress}${this.hass&&(0,n.d)(this.hass.locale)}% </div>`:i.s6} </div> <mwc-linear-progress .indeterminate="${!this.progress}" .progress="${this.progress?this.progress/100:void 0}"></mwc-linear-progress> </div>`:i.qy`<label for="${this.value?"":"input"}" class="container ${(0,l.H)({dragged:this._drag,multiple:this.multiple,value:Boolean(this.value)})}" @drop="${this._handleDrop}" @dragenter="${this._handleDragStart}" @dragover="${this._handleDragStart}" @dragleave="${this._handleDragEnd}" @dragend="${this._handleDragEnd}">${this.value?"string"==typeof this.value?i.qy`<div class="row"> <div class="value" @click="${this._openFilePicker}"> <ha-svg-icon .path="${this.icon||g}"></ha-svg-icon> ${this.value} </div> <ha-icon-button @click="${this._clearValue}" .label="${this.deleteLabel||e("ui.common.delete")}" .path="${u}"></ha-icon-button> </div>`:(this.value instanceof FileList?Array.from(this.value):(0,h.e)(this.value)).map(t=>i.qy`<div class="row"> <div class="value" @click="${this._openFilePicker}"> <ha-svg-icon .path="${this.icon||g}"></ha-svg-icon> ${t.name} - ${(0,c.A)(t.size)} </div> <ha-icon-button @click="${this._clearValue}" .label="${this.deleteLabel||e("ui.common.delete")}" .path="${u}"></ha-icon-button> </div>`):i.qy`<ha-button size="small" appearance="filled" @click="${this._openFilePicker}"> <ha-svg-icon slot="start" .path="${this.icon||g}"></ha-svg-icon> ${this.label||e("ui.components.file-upload.label")} </ha-button> <span class="secondary">${this.secondary||e("ui.components.file-upload.secondary")}</span> <span class="supports">${this.supports}</span>`} <input id="input" type="file" class="file" .accept="${this.accept}" .multiple="${this.multiple}" @change="${this._handleFilePicked}"></label>`} `}_openFilePicker(){this._input?.click()}_handleDrop(e){e.preventDefault(),e.stopPropagation(),e.dataTransfer?.files&&(0,s.r)(this,"file-picked",{files:this.multiple||1===e.dataTransfer.files.length?Array.from(e.dataTransfer.files):[e.dataTransfer.files[0]]}),this._drag=!1}_handleDragStart(e){e.preventDefault(),e.stopPropagation(),this._drag=!0}_handleDragEnd(e){e.preventDefault(),e.stopPropagation(),this._drag=!1}_handleFilePicked(e){0!==e.target.files.length&&(this.value=e.target.files,(0,s.r)(this,"file-picked",{files:e.target.files}))}_clearValue(e){e.preventDefault(),this._input.value="",this.value=void 0,(0,s.r)(this,"change"),(0,s.r)(this,"files-cleared")}constructor(...e){super(...e),this.multiple=!1,this.disabled=!1,this.uploading=!1,this.autoOpenFileDialog=!1,this._drag=!1}}v.styles=i.AH`:host{display:block;height:240px}:host([disabled]){pointer-events:none;color:var(--disabled-text-color)}.container{position:relative;display:flex;flex-direction:column;justify-content:center;align-items:center;border:solid 1px var(--mdc-text-field-idle-line-color,rgba(0,0,0,.42));border-radius:var(--mdc-shape-small,var(--ha-border-radius-sm));height:100%}.row{display:flex;align-items:center}label.container{border:dashed 1px var(--mdc-text-field-idle-line-color,rgba(0,0,0,.42));cursor:pointer}.container .uploading{display:flex;flex-direction:column;width:100%;align-items:flex-start;padding:0 32px;box-sizing:border-box}:host([disabled]) .container{border-color:var(--disabled-color)}label.dragged,label:hover{border-style:solid}label.dragged{border-color:var(--primary-color)}.dragged:before{position:absolute;top:0;right:0;bottom:0;left:0;background-color:var(--primary-color);content:"";opacity:var(--dark-divider-opacity);pointer-events:none;border-radius:var(--mdc-shape-small,4px)}label.value{cursor:default}label.value.multiple{justify-content:unset;overflow:auto}.highlight{color:var(--primary-color)}ha-button{margin-bottom:8px}.supports{color:var(--secondary-text-color);font-size:var(--ha-font-size-s)}:host([disabled]) .secondary{color:var(--disabled-text-color)}input.file{display:none}.value{cursor:pointer}.value ha-svg-icon{margin-right:8px;margin-inline-end:8px;margin-inline-start:initial}ha-button{--mdc-button-outline-color:var(--primary-color);--mdc-icon-button-size:24px}mwc-linear-progress{width:100%;padding:8px 32px;box-sizing:border-box}.header{font-weight:var(--ha-font-weight-medium)}.progress{color:var(--secondary-text-color)}button.link{background:0 0;border:none;padding:0;font-size:var(--ha-font-size-m);color:var(--primary-color);text-decoration:underline;cursor:pointer}`,(0,o.Cg)([(0,r.MZ)({attribute:!1})],v.prototype,"hass",void 0),(0,o.Cg)([(0,r.MZ)({attribute:!1})],v.prototype,"localize",void 0),(0,o.Cg)([(0,r.MZ)()],v.prototype,"accept",void 0),(0,o.Cg)([(0,r.MZ)()],v.prototype,"icon",void 0),(0,o.Cg)([(0,r.MZ)()],v.prototype,"label",void 0),(0,o.Cg)([(0,r.MZ)()],v.prototype,"secondary",void 0),(0,o.Cg)([(0,r.MZ)({attribute:"uploading-label"})],v.prototype,"uploadingLabel",void 0),(0,o.Cg)([(0,r.MZ)({attribute:"delete-label"})],v.prototype,"deleteLabel",void 0),(0,o.Cg)([(0,r.MZ)()],v.prototype,"supports",void 0),(0,o.Cg)([(0,r.MZ)({type:Object})],v.prototype,"value",void 0),(0,o.Cg)([(0,r.MZ)({type:Boolean})],v.prototype,"multiple",void 0),(0,o.Cg)([(0,r.MZ)({type:Boolean,reflect:!0})],v.prototype,"disabled",void 0),(0,o.Cg)([(0,r.MZ)({type:Boolean})],v.prototype,"uploading",void 0),(0,o.Cg)([(0,r.MZ)({type:Number})],v.prototype,"progress",void 0),(0,o.Cg)([(0,r.MZ)({type:Boolean,attribute:"auto-open-file-dialog"})],v.prototype,"autoOpenFileDialog",void 0),(0,o.Cg)([(0,r.wk)()],v.prototype,"_drag",void 0),(0,o.Cg)([(0,r.P)("#input")],v.prototype,"_input",void 0),v=(0,o.Cg)([(0,r.EM)("ha-file-upload")],v),t()}catch(e){t(e)}})},45331(e,t,a){a.a(e,async function(e,t){try{var o=a(62826),i=a(93900),r=a(96196),l=a(44457),s=a(32288),d=a(1087),n=a(59992),h=a(14503),c=(a(76538),a(26300),e([i]));i=(c.then?(await c)():c)[0];const p="M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z";class u extends((0,n.V)(r.WF)){get scrollableElement(){return this.bodyContainer}updated(e){super.updated(e),e.has("open")&&(this._open=this.open)}render(){return r.qy` <wa-dialog .open="${this._open}" .lightDismiss="${!this.preventScrimClose}" without-header aria-labelledby="${(0,s.J)(this.ariaLabelledBy||(void 0!==this.headerTitle?"ha-wa-dialog-title":void 0))}" aria-describedby="${(0,s.J)(this.ariaDescribedBy)}" @wa-show="${this._handleShow}" @wa-after-show="${this._handleAfterShow}" @wa-after-hide="${this._handleAfterHide}"> <slot name="header"> <ha-dialog-header .subtitlePosition="${this.headerSubtitlePosition}" .showBorder="${this._bodyScrolled}"> <slot name="headerNavigationIcon" slot="navigationIcon"> <ha-icon-button data-dialog="close" .label="${this.hass?.localize("ui.common.close")??"Close"}" .path="${p}"></ha-icon-button> </slot> ${void 0!==this.headerTitle?r.qy`<span slot="title" class="title" id="ha-wa-dialog-title"> ${this.headerTitle} </span>`:r.qy`<slot name="headerTitle" slot="title"></slot>`} ${void 0!==this.headerSubtitle?r.qy`<span slot="subtitle">${this.headerSubtitle}</span>`:r.qy`<slot name="headerSubtitle" slot="subtitle"></slot>`} <slot name="headerActionItems" slot="actionItems"></slot> </ha-dialog-header> </slot> <div class="content-wrapper"> <div class="body ha-scrollbar" @scroll="${this._handleBodyScroll}"> <slot></slot> </div> ${this.renderScrollableFades()} </div> <slot name="footer" slot="footer"></slot> </wa-dialog> `}disconnectedCallback(){super.disconnectedCallback(),this._open=!1}_handleBodyScroll(e){this._bodyScrolled=e.target.scrollTop>0}static get styles(){return[...super.styles,h.dp,r.AH`
        wa-dialog {
          --full-width: var(
            --ha-dialog-width-full,
            min(95vw, var(--safe-width))
          );
          --width: min(var(--ha-dialog-width-md, 580px), var(--full-width));
          --spacing: var(--dialog-content-padding, var(--ha-space-6));
          --show-duration: var(--ha-dialog-show-duration, 200ms);
          --hide-duration: var(--ha-dialog-hide-duration, 200ms);
          --ha-dialog-surface-background: var(
            --card-background-color,
            var(--ha-color-surface-default)
          );
          --wa-color-surface-raised: var(
            --ha-dialog-surface-background,
            var(--card-background-color, var(--ha-color-surface-default))
          );
          --wa-panel-border-radius: var(
            --ha-dialog-border-radius,
            var(--ha-border-radius-3xl)
          );
          max-width: var(--ha-dialog-max-width, var(--safe-width));
        }
        @media (prefers-reduced-motion: reduce) {
          wa-dialog {
            --show-duration: 0ms;
            --hide-duration: 0ms;
          }
        }

        :host([width="small"]) wa-dialog {
          --width: min(var(--ha-dialog-width-sm, 320px), var(--full-width));
        }

        :host([width="large"]) wa-dialog {
          --width: min(var(--ha-dialog-width-lg, 1024px), var(--full-width));
        }

        :host([width="full"]) wa-dialog {
          --width: var(--full-width);
        }

        wa-dialog::part(dialog) {
          min-width: var(--width, var(--full-width));
          max-width: var(--width, var(--full-width));
          max-height: var(
            --ha-dialog-max-height,
            calc(var(--safe-height) - var(--ha-space-20))
          );
          min-height: var(--ha-dialog-min-height);
          margin-top: var(--dialog-surface-margin-top, auto);
          /* Used to offset the dialog from the safe areas when space is limited */
          transform: translate(
            calc(
              var(--safe-area-offset-left, 0px) - var(
                  --safe-area-offset-right,
                  0px
                )
            ),
            calc(
              var(--safe-area-offset-top, 0px) - var(
                  --safe-area-offset-bottom,
                  0px
                )
            )
          );
          display: flex;
          flex-direction: column;
          overflow: hidden;
        }

        @media all and (max-width: 450px), all and (max-height: 500px) {
          :host([type="standard"]) {
            --ha-dialog-border-radius: 0;

            wa-dialog {
              /* Make the container fill the whole screen width and not the safe width */
              --full-width: var(--ha-dialog-width-full, 100vw);
              --width: var(--full-width);
            }

            wa-dialog::part(dialog) {
              /* Make the dialog fill the whole screen height and not the safe height */
              min-height: var(--ha-dialog-min-height, 100vh);
              min-height: var(--ha-dialog-min-height, 100dvh);
              max-height: var(--ha-dialog-max-height, 100vh);
              max-height: var(--ha-dialog-max-height, 100dvh);
              margin-top: 0;
              margin-bottom: 0;
              /* Use safe area as padding instead of the container size */
              padding-top: var(--safe-area-inset-top);
              padding-bottom: var(--safe-area-inset-bottom);
              padding-left: var(--safe-area-inset-left);
              padding-right: var(--safe-area-inset-right);
              /* Reset the transform to center the dialog */
              transform: none;
            }
          }
        }

        .header-title-container {
          display: flex;
          align-items: center;
        }

        .header-title {
          margin: 0;
          margin-bottom: 0;
          color: var(--ha-dialog-header-title-color, var(--primary-text-color));
          font-size: var(
            --ha-dialog-header-title-font-size,
            var(--ha-font-size-2xl)
          );
          line-height: var(
            --ha-dialog-header-title-line-height,
            var(--ha-line-height-condensed)
          );
          font-weight: var(
            --ha-dialog-header-title-font-weight,
            var(--ha-font-weight-normal)
          );
          overflow: hidden;
          text-overflow: ellipsis;
          white-space: nowrap;
          margin-right: var(--ha-space-3);
        }

        wa-dialog::part(body) {
          padding: 0;
          display: flex;
          flex-direction: column;
          max-width: 100%;
          overflow: hidden;
        }

        .content-wrapper {
          position: relative;
          flex: 1;
          display: flex;
          flex-direction: column;
          min-height: 0;
        }

        .body {
          position: var(--dialog-content-position, relative);
          padding: var(
            --dialog-content-padding,
            0 var(--ha-space-6) var(--ha-space-6) var(--ha-space-6)
          );
          overflow: auto;
          flex-grow: 1;
        }
        :host([flexcontent]) .body {
          max-width: 100%;
          flex: 1;
          display: flex;
          flex-direction: column;
        }

        wa-dialog::part(footer) {
          padding: 0;
        }

        ::slotted([slot="footer"]) {
          display: flex;
          padding: var(--ha-space-3) var(--ha-space-4) var(--ha-space-4)
            var(--ha-space-4);
          gap: var(--ha-space-3);
          justify-content: flex-end;
          align-items: center;
          width: 100%;
        }
      `]}constructor(...e){super(...e),this.open=!1,this.type="standard",this.width="medium",this.preventScrimClose=!1,this.headerSubtitlePosition="below",this.flexContent=!1,this._open=!1,this._bodyScrolled=!1,this._handleShow=async()=>{this._open=!0,(0,d.r)(this,"opened"),await this.updateComplete,requestAnimationFrame(()=>{this.querySelector("[autofocus]")?.focus()})},this._handleAfterShow=()=>{(0,d.r)(this,"after-show")},this._handleAfterHide=()=>{this._open=!1,(0,d.r)(this,"closed")}}}(0,o.Cg)([(0,l.MZ)({attribute:!1})],u.prototype,"hass",void 0),(0,o.Cg)([(0,l.MZ)({attribute:"aria-labelledby"})],u.prototype,"ariaLabelledBy",void 0),(0,o.Cg)([(0,l.MZ)({attribute:"aria-describedby"})],u.prototype,"ariaDescribedBy",void 0),(0,o.Cg)([(0,l.MZ)({type:Boolean,reflect:!0})],u.prototype,"open",void 0),(0,o.Cg)([(0,l.MZ)({reflect:!0})],u.prototype,"type",void 0),(0,o.Cg)([(0,l.MZ)({type:String,reflect:!0,attribute:"width"})],u.prototype,"width",void 0),(0,o.Cg)([(0,l.MZ)({type:Boolean,reflect:!0,attribute:"prevent-scrim-close"})],u.prototype,"preventScrimClose",void 0),(0,o.Cg)([(0,l.MZ)({attribute:"header-title"})],u.prototype,"headerTitle",void 0),(0,o.Cg)([(0,l.MZ)({attribute:"header-subtitle"})],u.prototype,"headerSubtitle",void 0),(0,o.Cg)([(0,l.MZ)({type:String,attribute:"header-subtitle-position"})],u.prototype,"headerSubtitlePosition",void 0),(0,o.Cg)([(0,l.MZ)({type:Boolean,reflect:!0,attribute:"flexcontent"})],u.prototype,"flexContent",void 0),(0,o.Cg)([(0,l.wk)()],u.prototype,"_open",void 0),(0,o.Cg)([(0,l.P)(".body")],u.prototype,"bodyContainer",void 0),(0,o.Cg)([(0,l.wk)()],u.prototype,"_bodyScrolled",void 0),(0,o.Cg)([(0,l.Ls)({passive:!0})],u.prototype,"_handleBodyScroll",null),u=(0,o.Cg)([(0,l.EM)("ha-wa-dialog")],u),t()}catch(e){t(e)}})},59992(e,t,a){a.d(t,{V:()=>d});var o=a(62826),i=a(88696),r=a(96196),l=a(94333),s=a(44457);const d=e=>{class t extends e{get scrollableElement(){return t.DEFAULT_SCROLLABLE_ELEMENT}firstUpdated(e){super.firstUpdated?.(e),this.scrollableElement&&this._updateScrollableState(this.scrollableElement),this._attachScrollableElement()}updated(e){super.updated?.(e),this._attachScrollableElement()}disconnectedCallback(){this._detachScrollableElement(),this._contentScrolled=!1,this._contentScrollable=!1,super.disconnectedCallback()}renderScrollableFades(e=!1){return r.qy` <div class="${(0,l.H)({"fade-top":!0,rounded:e,visible:this._contentScrolled})}"></div> <div class="${(0,l.H)({"fade-bottom":!0,rounded:e,visible:this._contentScrollable})}"></div> `}static get styles(){const e=Object.getPrototypeOf(this);var t;return[...void 0===(t=e?.styles??[])?[]:Array.isArray(t)?t:[t],r.AH`.fade-bottom,.fade-top{position:absolute;left:0;right:0;height:var(--ha-space-2);pointer-events:none;transition:opacity 180ms ease-in-out;border-radius:var(--ha-border-radius-square);opacity:0;background:linear-gradient(to bottom,var(--ha-color-shadow-scrollable-fade),transparent)}.fade-top{top:0}.fade-bottom{bottom:0;transform:rotate(180deg)}.fade-bottom.visible,.fade-top.visible{opacity:1}.fade-bottom.rounded,.fade-top.rounded{border-radius:var(--ha-card-border-radius,var(--ha-border-radius-lg));border-bottom-left-radius:var(--ha-border-radius-square);border-bottom-right-radius:var(--ha-border-radius-square)}.fade-top.rounded{border-top-left-radius:var(--ha-border-radius-square);border-top-right-radius:var(--ha-border-radius-square)}.fade-bottom.rounded{border-bottom-left-radius:var(--ha-border-radius-square);border-bottom-right-radius:var(--ha-border-radius-square)}`]}_attachScrollableElement(){const e=this.scrollableElement;e!==this._scrollTarget&&(this._detachScrollableElement(),e&&(this._scrollTarget=e,e.addEventListener("scroll",this._onScroll,{passive:!0}),this._resize.observe(e),this._updateScrollableState(e)))}_detachScrollableElement(){this._scrollTarget&&(this._scrollTarget.removeEventListener("scroll",this._onScroll),this._resize.unobserve?.(this._scrollTarget),this._scrollTarget=void 0)}_updateScrollableState(e){const t=parseFloat(getComputedStyle(e).getPropertyValue("--safe-area-inset-bottom"))||0,{scrollHeight:a=0,clientHeight:o=0,scrollTop:i=0}=e;this._contentScrollable=a-o>i+t+this.scrollFadeSafeAreaPadding}constructor(...e){super(...e),this._contentScrolled=!1,this._contentScrollable=!1,this._onScroll=e=>{const t=e.currentTarget;this._contentScrolled=(t.scrollTop??0)>this.scrollFadeThreshold,this._updateScrollableState(t)},this._resize=new i.P(this,{target:null,callback:e=>{const t=e[0]?.target;t&&this._updateScrollableState(t)}}),this.scrollFadeSafeAreaPadding=4,this.scrollFadeThreshold=4}}return t.DEFAULT_SCROLLABLE_ELEMENT=null,(0,o.Cg)([(0,s.wk)()],t.prototype,"_contentScrolled",void 0),(0,o.Cg)([(0,s.wk)()],t.prototype,"_contentScrollable",void 0),t}},62468(e,t,a){a.a(e,async function(e,o){try{a.r(t),a.d(t,{DialogUploadBackup:()=>b});var i=a(62826),r=a(96196),l=a(44457),s=a(36312),d=a(1087),n=(a(38962),a(18350)),h=(a(93444),a(41060)),c=a(45331),p=a(31420),u=a(14503),g=a(33963),v=e([n,h,c,g,p]);[n,h,c,g,p]=v.then?(await v)():v;const f="M20,6A2,2 0 0,1 22,8V18A2,2 0 0,1 20,20H4A2,2 0 0,1 2,18V6A2,2 0 0,1 4,4H10L12,6H20M10.75,13H14V17H16V13H19.25L15,8.75";class b extends r.WF{async showDialog(e){this._params=e,this._formData=p.Dt,this._open=!0}_dialogClosed(){this._params.cancel&&this._params.cancel(),this._formData=void 0,this._params=void 0,this._open=!1,(0,d.r)(this,"dialog-closed",{dialog:this.localName})}closeDialog(){return this._open=!1,!0}_formValid(){return void 0!==this._formData?.file}render(){return this._params&&this._formData?r.qy` <ha-wa-dialog .hass="${this.hass}" .open="${this._open}" header-title="${this.hass.localize("ui.panel.config.backup.dialogs.upload.title")}" ?prevent-scrim-close="${this._uploading}" @closed="${this._dialogClosed}"> ${this._error?r.qy`<ha-alert alert-type="error">${this._error}</ha-alert>`:r.s6} <ha-file-upload .hass="${this.hass}" .uploading="${this._uploading}" .icon="${f}" .accept="${p.xN}" .localize="${this.hass.localize}" .label="${this.hass.localize("ui.panel.config.backup.dialogs.upload.input_label")}" .supports="${this.hass.localize("ui.panel.config.backup.dialogs.upload.supports_tar")}" @file-picked="${this._filePicked}" @files-cleared="${this._filesCleared}"></ha-file-upload> <ha-dialog-footer slot="footer"> <ha-button slot="secondaryAction" appearance="plain" @click="${this.closeDialog}" .disabled="${this._uploading}"> ${this.hass.localize("ui.common.cancel")} </ha-button> <ha-button slot="primaryAction" @click="${this._upload}" .disabled="${!this._formValid()||this._uploading}"> ${this.hass.localize("ui.panel.config.backup.dialogs.upload.action")} </ha-button> </ha-dialog-footer> </ha-wa-dialog> `:r.s6}_filePicked(e){this._error=void 0;const t=e.detail.files[0];this._formData={...this._formData,file:t}}_filesCleared(){this._error=void 0,this._formData=p.Dt}async _upload(){const{file:e}=this._formData;if(!e||e.type!==p.xN)return void(0,g.showAlertDialog)(this,{title:this.hass.localize("ui.panel.config.backup.dialogs.upload.unsupported.title"),text:this.hass.localize("ui.panel.config.backup.dialogs.upload.unsupported.text"),confirmText:this.hass.localize("ui.common.ok")});const t=(0,s.x)(this.hass,"hassio")?[p.mF]:[p.gv];this._uploading=!0;try{await(0,p.kI)(this.hass,e,t),this._params.submit?.(),this.closeDialog()}catch(e){this._error=e.message}finally{this._uploading=!1}}static get styles(){return[u.RF,u.nA,r.AH`ha-alert{display:block;margin-bottom:var(--ha-space-4)}`]}constructor(...e){super(...e),this._uploading=!1,this._open=!1}}(0,i.Cg)([(0,l.MZ)({attribute:!1})],b.prototype,"hass",void 0),(0,i.Cg)([(0,l.wk)()],b.prototype,"_params",void 0),(0,i.Cg)([(0,l.wk)()],b.prototype,"_uploading",void 0),(0,i.Cg)([(0,l.wk)()],b.prototype,"_error",void 0),(0,i.Cg)([(0,l.wk)()],b.prototype,"_formData",void 0),(0,i.Cg)([(0,l.wk)()],b.prototype,"_open",void 0),b=(0,i.Cg)([(0,l.EM)("ha-dialog-upload-backup")],b),o()}catch(e){o(e)}})}};
//# sourceMappingURL=24901.62678be36335b502.js.map