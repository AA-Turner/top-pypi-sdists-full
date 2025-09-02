"use strict";(self.webpackChunkknx_frontend=self.webpackChunkknx_frontend||[]).push([["3188"],{35859:function(e,t,i){i.d(t,{I:function(){return o}});i(39710),i(26847),i(56389),i(27530);const o=(e,t,i,o)=>{const[a,r,n]=e.split(".",3);return Number(a)>t||Number(a)===t&&(void 0===o?Number(r)>=i:Number(r)>i)||void 0!==o&&Number(a)===t&&Number(r)===i&&Number(n)>=o}},35505:function(e,t,i){i.d(t,{K:function(){return o}});const o=e=>{switch(e.language){case"cs":case"de":case"fi":case"fr":case"sk":case"sv":return" ";default:return""}}},30337:function(e,t,i){i.a(e,(async function(e,t){try{i(26847),i(27530),i(11807);var o=i(73742),a=i(71328),r=i(59048),n=i(7616),l=i(63871),d=e([a]);a=(d.then?(await d)():d)[0];let s,c=e=>e;class p extends a.Z{attachInternals(){const e=super.attachInternals();return Object.defineProperty(e,"states",{value:new l.C(this,e.states)}),e}static get styles(){return[a.Z.styles,(0,r.iv)(s||(s=c`
        .button {
          /* set theme vars */
          --wa-form-control-padding-inline: 16px;
          --wa-font-weight-action: var(--ha-font-weight-medium);
          --wa-border-radius-pill: 9999px;
          --wa-form-control-border-radius: var(
            --ha-button-radius,
            var(--wa-border-radius-pill)
          );

          --wa-form-control-height: var(
            --ha-button-height,
            var(--button-height, 40px)
          );

          font-size: var(--ha-font-size-m);
          line-height: 1;
        }

        :host([size="small"]) .button {
          --wa-form-control-height: var(
            --ha-button-height,
            var(--button-height, 32px)
          );
          font-size: var(--wa-font-size-s, var(--ha-font-size-m));
        }

        :host([variant="brand"]) {
          --color-fill-normal-active: var(--color-fill-primary-normal-active);
          --color-fill-normal-hover: var(--color-fill-primary-normal-hover);
          --color-fill-loud-active: var(--color-fill-primary-loud-active);
          --color-fill-loud-hover: var(--color-fill-primary-loud-hover);
        }

        :host([variant="neutral"]) {
          --color-fill-normal-active: var(--color-fill-neutral-normal-active);
          --color-fill-normal-hover: var(--color-fill-neutral-normal-hover);
          --color-fill-loud-active: var(--color-fill-neutral-loud-active);
          --color-fill-loud-hover: var(--color-fill-neutral-loud-hover);
        }

        :host([variant="success"]) {
          --color-fill-normal-active: var(--color-fill-success-normal-active);
          --color-fill-normal-hover: var(--color-fill-success-normal-hover);
          --color-fill-loud-active: var(--color-fill-success-loud-active);
          --color-fill-loud-hover: var(--color-fill-success-loud-hover);
        }

        :host([variant="warning"]) {
          --color-fill-normal-active: var(--color-fill-warning-normal-active);
          --color-fill-normal-hover: var(--color-fill-warning-normal-hover);
          --color-fill-loud-active: var(--color-fill-warning-loud-active);
          --color-fill-loud-hover: var(--color-fill-warning-loud-hover);
        }

        :host([variant="danger"]) {
          --color-fill-normal-active: var(--color-fill-danger-normal-active);
          --color-fill-normal-hover: var(--color-fill-danger-normal-hover);
          --color-fill-loud-active: var(--color-fill-danger-loud-active);
          --color-fill-loud-hover: var(--color-fill-danger-loud-hover);
        }

        :host([appearance~="plain"]) .button {
          color: var(--wa-color-on-normal);
        }
        :host([appearance~="plain"]) .button.disabled {
          background-color: var(--transparent-none);
          color: var(--color-on-disabled-quiet);
        }

        :host([appearance~="outlined"]) .button.disabled {
          background-color: var(--transparent-none);
          color: var(--color-on-disabled-quiet);
        }

        @media (hover: hover) {
          :host([appearance~="filled"])
            .button:not(.disabled):not(.loading):hover {
            background-color: var(--color-fill-normal-hover);
          }
          :host([appearance~="accent"])
            .button:not(.disabled):not(.loading):hover {
            background-color: var(--color-fill-loud-hover);
          }
          :host([appearance~="plain"])
            .button:not(.disabled):not(.loading):hover {
            color: var(--wa-color-on-normal);
          }
        }
        :host([appearance~="filled"])
          .button:not(.disabled):not(.loading):active {
          background-color: var(--color-fill-normal-active);
        }
        :host([appearance~="filled"]) .button.disabled {
          background-color: var(--color-fill-disabled-normal-resting);
          color: var(--color-on-disabled-normal);
        }

        :host([appearance~="accent"]) .button {
          background-color: var(
            --wa-color-fill-loud,
            var(--wa-color-neutral-fill-loud)
          );
        }
        :host([appearance~="accent"])
          .button:not(.disabled):not(.loading):active {
          background-color: var(--color-fill-loud-active);
        }
        :host([appearance~="accent"]) .button.disabled {
          background-color: var(--color-fill-disabled-loud-resting);
          color: var(--color-on-disabled-loud);
        }

        :host([loading]) {
          pointer-events: none;
        }

        .button.disabled {
          opacity: 1;
        }
      `))]}constructor(...e){super(...e),this.variant="brand"}}p=(0,o.__decorate)([(0,n.Mo)("ha-button")],p),t()}catch(s){t(s)}}))},34998:function(e,t,i){i.a(e,(async function(e,t){try{i(26847),i(81738),i(6989),i(27530);var o=i(73742),a=i(61611),r=i(59048),n=i(7616),l=i(31733),d=i(29740),s=i(30337),c=(i(78645),i(35505)),p=i(74608),h=i(57874),u=e([a,s]);[a,s]=u.then?(await u)():u;let v,f,g,x,m,b,_,y,k=e=>e;const w="M19,4H15.5L14.5,3H9.5L8.5,4H5V6H19M6,19A2,2 0 0,0 8,21H16A2,2 0 0,0 18,19V7H6V19Z",$="M14,2H6A2,2 0 0,0 4,4V20A2,2 0 0,0 6,22H18A2,2 0 0,0 20,20V8L14,2M13.5,16V19H10.5V16H8L12,12L16,16H13.5M13,9V3.5L18.5,9H13Z";class j extends r.oi{firstUpdated(e){super.firstUpdated(e),this.autoOpenFileDialog&&this._openFilePicker()}get _name(){if(void 0===this.value)return"";if("string"==typeof this.value)return this.value;return(this.value instanceof FileList?Array.from(this.value):(0,p.r)(this.value)).map((e=>e.name)).join(", ")}render(){const e=this.localize||this.hass.localize;return(0,r.dy)(v||(v=k`
      ${0}
    `),this.uploading?(0,r.dy)(f||(f=k`<div class="container">
            <div class="uploading">
              <span class="header"
                >${0}</span
              >
              ${0}
            </div>
            <mwc-linear-progress
              .indeterminate=${0}
              .progress=${0}
            ></mwc-linear-progress>
          </div>`),this.uploadingLabel||(this.value?e("ui.components.file-upload.uploading_name",{name:this._name}):e("ui.components.file-upload.uploading")),this.progress?(0,r.dy)(g||(g=k`<div class="progress">
                    ${0}${0}%
                  </div>`),this.progress,this.hass&&(0,c.K)(this.hass.locale)):r.Ld,!this.progress,this.progress?this.progress/100:void 0):(0,r.dy)(x||(x=k`<label
            for=${0}
            class="container ${0}"
            @drop=${0}
            @dragenter=${0}
            @dragover=${0}
            @dragleave=${0}
            @dragend=${0}
            >${0}
            <input
              id="input"
              type="file"
              class="file"
              .accept=${0}
              .multiple=${0}
              @change=${0}
          /></label>`),this.value?"":"input",(0,l.$)({dragged:this._drag,multiple:this.multiple,value:Boolean(this.value)}),this._handleDrop,this._handleDragStart,this._handleDragStart,this._handleDragEnd,this._handleDragEnd,this.value?"string"==typeof this.value?(0,r.dy)(b||(b=k`<div class="row">
                    <div class="value" @click=${0}>
                      <ha-svg-icon
                        .path=${0}
                      ></ha-svg-icon>
                      ${0}
                    </div>
                    <ha-icon-button
                      @click=${0}
                      .label=${0}
                      .path=${0}
                    ></ha-icon-button>
                  </div>`),this._openFilePicker,this.icon||$,this.value,this._clearValue,this.deleteLabel||e("ui.common.delete"),w):(this.value instanceof FileList?Array.from(this.value):(0,p.r)(this.value)).map((t=>(0,r.dy)(_||(_=k`<div class="row">
                        <div class="value" @click=${0}>
                          <ha-svg-icon
                            .path=${0}
                          ></ha-svg-icon>
                          ${0} - ${0}
                        </div>
                        <ha-icon-button
                          @click=${0}
                          .label=${0}
                          .path=${0}
                        ></ha-icon-button>
                      </div>`),this._openFilePicker,this.icon||$,t.name,(0,h.d)(t.size),this._clearValue,this.deleteLabel||e("ui.common.delete"),w))):(0,r.dy)(m||(m=k`<ha-button
                    size="small"
                    appearance="filled"
                    @click=${0}
                  >
                    <ha-svg-icon
                      slot="start"
                      .path=${0}
                    ></ha-svg-icon>
                    ${0}
                  </ha-button>
                  <span class="secondary"
                    >${0}</span
                  >
                  <span class="supports">${0}</span>`),this._openFilePicker,this.icon||$,this.label||e("ui.components.file-upload.label"),this.secondary||e("ui.components.file-upload.secondary"),this.supports),this.accept,this.multiple,this._handleFilePicked))}_openFilePicker(){var e;null===(e=this._input)||void 0===e||e.click()}_handleDrop(e){var t;e.preventDefault(),e.stopPropagation(),null!==(t=e.dataTransfer)&&void 0!==t&&t.files&&(0,d.B)(this,"file-picked",{files:this.multiple||1===e.dataTransfer.files.length?Array.from(e.dataTransfer.files):[e.dataTransfer.files[0]]}),this._drag=!1}_handleDragStart(e){e.preventDefault(),e.stopPropagation(),this._drag=!0}_handleDragEnd(e){e.preventDefault(),e.stopPropagation(),this._drag=!1}_handleFilePicked(e){0!==e.target.files.length&&(this.value=e.target.files,(0,d.B)(this,"file-picked",{files:e.target.files}))}_clearValue(e){e.preventDefault(),this._input.value="",this.value=void 0,(0,d.B)(this,"change"),(0,d.B)(this,"files-cleared")}constructor(...e){super(...e),this.multiple=!1,this.disabled=!1,this.uploading=!1,this.autoOpenFileDialog=!1,this._drag=!1}}j.styles=(0,r.iv)(y||(y=k`
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
  `)),(0,o.__decorate)([(0,n.Cb)({attribute:!1})],j.prototype,"hass",void 0),(0,o.__decorate)([(0,n.Cb)({attribute:!1})],j.prototype,"localize",void 0),(0,o.__decorate)([(0,n.Cb)()],j.prototype,"accept",void 0),(0,o.__decorate)([(0,n.Cb)()],j.prototype,"icon",void 0),(0,o.__decorate)([(0,n.Cb)()],j.prototype,"label",void 0),(0,o.__decorate)([(0,n.Cb)()],j.prototype,"secondary",void 0),(0,o.__decorate)([(0,n.Cb)({attribute:"uploading-label"})],j.prototype,"uploadingLabel",void 0),(0,o.__decorate)([(0,n.Cb)({attribute:"delete-label"})],j.prototype,"deleteLabel",void 0),(0,o.__decorate)([(0,n.Cb)()],j.prototype,"supports",void 0),(0,o.__decorate)([(0,n.Cb)({type:Object})],j.prototype,"value",void 0),(0,o.__decorate)([(0,n.Cb)({type:Boolean})],j.prototype,"multiple",void 0),(0,o.__decorate)([(0,n.Cb)({type:Boolean,reflect:!0})],j.prototype,"disabled",void 0),(0,o.__decorate)([(0,n.Cb)({type:Boolean})],j.prototype,"uploading",void 0),(0,o.__decorate)([(0,n.Cb)({type:Number})],j.prototype,"progress",void 0),(0,o.__decorate)([(0,n.Cb)({type:Boolean,attribute:"auto-open-file-dialog"})],j.prototype,"autoOpenFileDialog",void 0),(0,o.__decorate)([(0,n.SB)()],j.prototype,"_drag",void 0),(0,o.__decorate)([(0,n.IO)("#input")],j.prototype,"_input",void 0),j=(0,o.__decorate)([(0,n.Mo)("ha-file-upload")],j),t()}catch(v){t(v)}}))},38573:function(e,t,i){i.d(t,{f:function(){return v}});i(26847),i(27530);var o=i(73742),a=i(94068),r=i(16880),n=i(59048),l=i(7616),d=i(51597);let s,c,p,h,u=e=>e;class v extends a.P{updated(e){super.updated(e),(e.has("invalid")||e.has("errorMessage"))&&(this.setCustomValidity(this.invalid?this.errorMessage||this.validationMessage||"Invalid":""),(this.invalid||this.validateOnInitialRender||e.has("invalid")&&void 0!==e.get("invalid"))&&this.reportValidity()),e.has("autocomplete")&&(this.autocomplete?this.formElement.setAttribute("autocomplete",this.autocomplete):this.formElement.removeAttribute("autocomplete")),e.has("autocorrect")&&(this.autocorrect?this.formElement.setAttribute("autocorrect",this.autocorrect):this.formElement.removeAttribute("autocorrect")),e.has("inputSpellcheck")&&(this.inputSpellcheck?this.formElement.setAttribute("spellcheck",this.inputSpellcheck):this.formElement.removeAttribute("spellcheck"))}renderIcon(e,t=!1){const i=t?"trailing":"leading";return(0,n.dy)(s||(s=u`
      <span
        class="mdc-text-field__icon mdc-text-field__icon--${0}"
        tabindex=${0}
      >
        <slot name="${0}Icon"></slot>
      </span>
    `),i,t?1:-1,i)}constructor(...e){super(...e),this.icon=!1,this.iconTrailing=!1}}v.styles=[r.W,(0,n.iv)(c||(c=u`
      .mdc-text-field__input {
        width: var(--ha-textfield-input-width, 100%);
      }
      .mdc-text-field:not(.mdc-text-field--with-leading-icon) {
        padding: var(--text-field-padding, 0px 16px);
      }
      .mdc-text-field__affix--suffix {
        padding-left: var(--text-field-suffix-padding-left, 12px);
        padding-right: var(--text-field-suffix-padding-right, 0px);
        padding-inline-start: var(--text-field-suffix-padding-left, 12px);
        padding-inline-end: var(--text-field-suffix-padding-right, 0px);
        direction: ltr;
      }
      .mdc-text-field--with-leading-icon {
        padding-inline-start: var(--text-field-suffix-padding-left, 0px);
        padding-inline-end: var(--text-field-suffix-padding-right, 16px);
        direction: var(--direction);
      }

      .mdc-text-field--with-leading-icon.mdc-text-field--with-trailing-icon {
        padding-left: var(--text-field-suffix-padding-left, 0px);
        padding-right: var(--text-field-suffix-padding-right, 0px);
        padding-inline-start: var(--text-field-suffix-padding-left, 0px);
        padding-inline-end: var(--text-field-suffix-padding-right, 0px);
      }
      .mdc-text-field:not(.mdc-text-field--disabled)
        .mdc-text-field__affix--suffix {
        color: var(--secondary-text-color);
      }

      .mdc-text-field:not(.mdc-text-field--disabled) .mdc-text-field__icon {
        color: var(--secondary-text-color);
      }

      .mdc-text-field__icon--leading {
        margin-inline-start: 16px;
        margin-inline-end: 8px;
        direction: var(--direction);
      }

      .mdc-text-field__icon--trailing {
        padding: var(--textfield-icon-trailing-padding, 12px);
      }

      .mdc-floating-label:not(.mdc-floating-label--float-above) {
        max-width: calc(100% - 16px);
      }

      .mdc-floating-label--float-above {
        max-width: calc((100% - 16px) / 0.75);
        transition: none;
      }

      input {
        text-align: var(--text-field-text-align, start);
      }

      input[type="color"] {
        height: 20px;
      }

      /* Edge, hide reveal password icon */
      ::-ms-reveal {
        display: none;
      }

      /* Chrome, Safari, Edge, Opera */
      :host([no-spinner]) input::-webkit-outer-spin-button,
      :host([no-spinner]) input::-webkit-inner-spin-button {
        -webkit-appearance: none;
        margin: 0;
      }

      input[type="color"]::-webkit-color-swatch-wrapper {
        padding: 0;
      }

      /* Firefox */
      :host([no-spinner]) input[type="number"] {
        -moz-appearance: textfield;
      }

      .mdc-text-field__ripple {
        overflow: hidden;
      }

      .mdc-text-field {
        overflow: var(--text-field-overflow);
      }

      .mdc-floating-label {
        padding-inline-end: 16px;
        padding-inline-start: initial;
        inset-inline-start: 16px !important;
        inset-inline-end: initial !important;
        transform-origin: var(--float-start);
        direction: var(--direction);
        text-align: var(--float-start);
        box-sizing: border-box;
        text-overflow: ellipsis;
      }

      .mdc-text-field--with-leading-icon.mdc-text-field--filled
        .mdc-floating-label {
        max-width: calc(
          100% - 48px - var(--text-field-suffix-padding-left, 0px)
        );
        inset-inline-start: calc(
          48px + var(--text-field-suffix-padding-left, 0px)
        ) !important;
        inset-inline-end: initial !important;
        direction: var(--direction);
      }

      .mdc-text-field__input[type="number"] {
        direction: var(--direction);
      }
      .mdc-text-field__affix--prefix {
        padding-right: var(--text-field-prefix-padding-right, 2px);
        padding-inline-end: var(--text-field-prefix-padding-right, 2px);
        padding-inline-start: initial;
      }

      .mdc-text-field:not(.mdc-text-field--disabled)
        .mdc-text-field__affix--prefix {
        color: var(--mdc-text-field-label-ink-color);
      }
      #helper-text ha-markdown {
        display: inline-block;
      }
    `)),"rtl"===d.E.document.dir?(0,n.iv)(p||(p=u`
          .mdc-text-field--with-leading-icon,
          .mdc-text-field__icon--leading,
          .mdc-floating-label,
          .mdc-text-field--with-leading-icon.mdc-text-field--filled
            .mdc-floating-label,
          .mdc-text-field__input[type="number"] {
            direction: rtl;
            --direction: rtl;
          }
        `)):(0,n.iv)(h||(h=u``))],(0,o.__decorate)([(0,l.Cb)({type:Boolean})],v.prototype,"invalid",void 0),(0,o.__decorate)([(0,l.Cb)({attribute:"error-message"})],v.prototype,"errorMessage",void 0),(0,o.__decorate)([(0,l.Cb)({type:Boolean})],v.prototype,"icon",void 0),(0,o.__decorate)([(0,l.Cb)({type:Boolean})],v.prototype,"iconTrailing",void 0),(0,o.__decorate)([(0,l.Cb)()],v.prototype,"autocomplete",void 0),(0,o.__decorate)([(0,l.Cb)()],v.prototype,"autocorrect",void 0),(0,o.__decorate)([(0,l.Cb)({attribute:"input-spellcheck"})],v.prototype,"inputSpellcheck",void 0),(0,o.__decorate)([(0,l.IO)("input")],v.prototype,"formElement",void 0),v=(0,o.__decorate)([(0,l.Mo)("ha-textfield")],v)},71268:function(e,t,i){i.d(t,{Y:function(){return a},c:function(){return o}});i(40777),i(1455);const o=async(e,t)=>{const i=new FormData;i.append("file",t);const o=await e.fetchWithAuth("/api/file_upload",{method:"POST",body:i});if(413===o.status)throw new Error(`Uploaded file is too large (${t.name})`);if(200!==o.status)throw new Error("Unknown error");return(await o.json()).file_id},a=async(e,t)=>e.callApi("DELETE","file_upload",{file_id:t})},10840:function(e,t,i){i.d(t,{js:function(){return a},rY:function(){return o}});i(39710),i(26847),i(1455),i(67886),i(65451),i(46015),i(38334),i(94880),i(75643),i(29761),i(56389),i(27530),i(35859);const o=e=>e.data,a=e=>"object"==typeof e?"object"==typeof e.body?e.body.message||"Unknown error, see supervisor logs":e.body||e.message||"Unknown error, see supervisor logs":e;new Set([502,503,504])},81665:function(e,t,i){i.d(t,{D9:function(){return d},Ys:function(){return n},g7:function(){return l}});i(26847),i(87799),i(1455),i(27530);var o=i(29740);const a=()=>Promise.all([i.e("2179"),i.e("5055"),i.e("5177")]).then(i.bind(i,36765)),r=(e,t,i)=>new Promise((r=>{const n=t.cancel,l=t.confirm;(0,o.B)(e,"show-dialog",{dialogTag:"dialog-box",dialogImport:a,dialogParams:Object.assign(Object.assign(Object.assign({},t),i),{},{cancel:()=>{r(!(null==i||!i.prompt)&&null),n&&n()},confirm:e=>{r(null==i||!i.prompt||e),l&&l(e)}})})})),n=(e,t)=>r(e,t),l=(e,t)=>r(e,t,{confirmation:!0}),d=(e,t)=>r(e,t,{prompt:!0})},52128:function(e,t,i){i.a(e,(async function(e,t){try{i(26847),i(1455),i(27530);var o=i(52128),a=e([o]);o=(a.then?(await a)():a)[0],"function"!=typeof window.ResizeObserver&&(window.ResizeObserver=(await i.e("9931").then(i.bind(i,11860))).default),t()}catch(r){t(r)}}),1)},63871:function(e,t,i){i.d(t,{C:function(){return o}});i(26847),i(64455),i(67886),i(65451),i(46015),i(38334),i(94880),i(75643),i(29761),i(6202),i(27530);class o extends Set{add(e){super.add(e);const t=this._existing;if(t)try{t.add(e)}catch(i){t.add(`--${e}`)}else this._el.setAttribute(`state-${e}`,"");return this}delete(e){super.delete(e);const t=this._existing;return t?(t.delete(e),t.delete(`--${e}`)):this._el.removeAttribute(`state-${e}`),!0}has(e){return super.has(e)}clear(){for(const e of this)this.delete(e)}constructor(e,t=null){super(),this._existing=null,this._el=e,this._existing=t}}const a=CSSStyleSheet.prototype.replaceSync;Object.defineProperty(CSSStyleSheet.prototype,"replaceSync",{value:function(e){e=e.replace(/:state\(([^)]+)\)/g,":where(:state($1), :--$1, [state-$1])"),a.call(this,e)}})},57874:function(e,t,i){i.d(t,{d:function(){return o}});i(25718),i(15519);const o=(e=0,t=2)=>{if(0===e)return"0 Bytes";t=t<0?0:t;const i=Math.floor(Math.log(e)/Math.log(1024));return`${parseFloat((e/1024**i).toFixed(t))} ${["Bytes","KB","MB","GB","TB","PB","EB","ZB","YB"][i]}`}},26014:function(e,t,i){i.d(t,{q:function(){return o}});const o="2025.8.24.205840"},75681:function(e,t,i){i.a(e,(async function(e,o){try{i.r(t),i.d(t,{KNXInfo:function(){return z}});i(26847),i(1455),i(27530);var a=i(73742),r=i(59048),n=i(7616),l=i(29740),d=(i(13965),i(62790),i(30337)),s=i(34998),c=i(10667),p=i(71268),h=i(10840),u=i(81665),v=i(63279),f=i(38059),g=i(26014),x=e([d,s,c]);[d,s,c]=x.then?(await x)():x;let m,b,_,y,k,w=e=>e;const $="M14,2H6A2,2 0 0,0 4,4V20A2,2 0 0,0 6,22H18A2,2 0 0,0 20,20V8L14,2M13.5,16V19H10.5V16H8L12,12L16,16H13.5M13,9V3.5L18.5,9H13Z",j=new f.r("info");class z extends r.oi{render(){return(0,r.dy)(m||(m=w`
      <hass-tabs-subpage
        .hass=${0}
        .narrow=${0}
        .route=${0}
        .tabs=${0}
        .localizeFunc=${0}
      >
        <div class="columns">
          ${0}
          ${0}
          ${0}
        </div>
      </hass-tabs-subpage>
    `),this.hass,this.narrow,this.route,this.tabs,this.knx.localize,this._renderInfoCard(),this.knx.projectInfo?this._renderProjectDataCard(this.knx.projectInfo):r.Ld,this._renderProjectUploadCard())}_renderInfoCard(){return(0,r.dy)(b||(b=w` <ha-card class="knx-info">
      <div class="card-content knx-info-section">
        <div class="knx-content-row header">${0}</div>

        <div class="knx-content-row">
          <div>XKNX Version</div>
          <div>${0}</div>
        </div>

        <div class="knx-content-row">
          <div>KNX-Frontend Version</div>
          <div>${0}</div>
        </div>

        <div class="knx-content-row">
          <div>${0}</div>
          <div>
            ${0}
          </div>
        </div>

        <div class="knx-content-row">
          <div>${0}</div>
          <div>${0}</div>
        </div>

        <div class="knx-bug-report">
          ${0}
          <a href="https://github.com/XKNX/knx-integration" target="_blank">xknx/knx-integration</a>
        </div>

        <div class="knx-bug-report">
          ${0}
          <a href="https://my.knx.org" target="_blank">my.knx.org</a>
        </div>
      </div>
    </ha-card>`),this.knx.localize("info_information_header"),this.knx.connectionInfo.version,g.q,this.knx.localize("info_connected_to_bus"),this.hass.localize(this.knx.connectionInfo.connected?"ui.common.yes":"ui.common.no"),this.knx.localize("info_individual_address"),this.knx.connectionInfo.current_address,this.knx.localize("info_issue_tracker"),this.knx.localize("info_my_knx"))}_renderProjectDataCard(e){return(0,r.dy)(_||(_=w`
      <ha-card class="knx-info">
          <div class="card-content knx-content">
            <div class="header knx-content-row">
              ${0}
            </div>
            <div class="knx-content-row">
              <div>${0}</div>
              <div>${0}</div>
            </div>
            <div class="knx-content-row">
              <div>${0}</div>
              <div>${0}</div>
            </div>
            <div class="knx-content-row">
              <div>${0}</div>
              <div>${0}</div>
            </div>
            <div class="knx-content-row">
              <div>${0}</div>
              <div>${0}</div>
            </div>
            <div class="knx-button-row">
              <ha-button
                class="knx-warning push-right"
                @click=${0}
                .disabled=${0}
                >
                ${0}
              </ha-button>
            </div>
          </div>
        </div>
      </ha-card>
    `),this.knx.localize("info_project_data_header"),this.knx.localize("info_project_data_name"),e.name,this.knx.localize("info_project_data_last_modified"),new Date(e.last_modified).toUTCString(),this.knx.localize("info_project_data_tool_version"),e.tool_version,this.knx.localize("info_project_data_xknxproject_version"),e.xknxproject_version,this._removeProject,this._uploading||!this.knx.projectInfo,this.knx.localize("info_project_delete"))}_renderProjectUploadCard(){var e;return(0,r.dy)(y||(y=w` <ha-card class="knx-info">
      <div class="card-content knx-content">
        <div class="knx-content-row header">${0}</div>
        <div class="knx-content-row">${0}</div>
        <div class="knx-content-row">
          <ha-file-upload
            .hass=${0}
            accept=".knxproj, .knxprojarchive"
            .icon=${0}
            .label=${0}
            .value=${0}
            .uploading=${0}
            @file-picked=${0}
          ></ha-file-upload>
        </div>
        <div class="knx-content-row">
          <ha-selector-text
            .hass=${0}
            .value=${0}
            .label=${0}
            .selector=${0}
            .required=${0}
            @value-changed=${0}
          >
          </ha-selector-text>
        </div>
        <div class="knx-button-row">
          <ha-button
            class="push-right"
            @click=${0}
            .disabled=${0}
            >${0}</ha-button
          >
        </div>
      </div>
    </ha-card>`),this.knx.localize("info_project_file_header"),this.knx.localize("info_project_upload_description"),this.hass,$,this.knx.localize("info_project_file"),null===(e=this._projectFile)||void 0===e?void 0:e.name,this._uploading,this._filePicked,this.hass,this._projectPassword||"",this.hass.localize("ui.login-form.password"),{text:{multiline:!1,type:"password"}},!1,this._passwordChanged,this._uploadFile,this._uploading||!this._projectFile,this.hass.localize("ui.common.submit"))}_filePicked(e){this._projectFile=e.detail.files[0]}_passwordChanged(e){this._projectPassword=e.detail.value}async _uploadFile(e){const t=this._projectFile;if(void 0===t)return;let i;this._uploading=!0;try{const e=await(0,p.c)(this.hass,t);await(0,v.cO)(this.hass,e,this._projectPassword||"")}catch(o){i=o,(0,u.Ys)(this,{title:"Upload failed",text:(0,h.js)(o)})}finally{i||(this._projectFile=void 0,this._projectPassword=void 0),this._uploading=!1,(0,l.B)(this,"knx-reload")}}async _removeProject(e){if(await(0,u.g7)(this,{text:this.knx.localize("info_project_delete")}))try{await(0,v.Hk)(this.hass)}catch(t){(0,u.Ys)(this,{title:"Deletion failed",text:(0,h.js)(t)})}finally{(0,l.B)(this,"knx-reload")}else j.debug("User cancelled deletion")}constructor(...e){super(...e),this._uploading=!1}}z.styles=(0,r.iv)(k||(k=w`
    .columns {
      display: flex;
      justify-content: center;
    }

    @media screen and (max-width: 1232px) {
      .columns {
        flex-direction: column;
      }

      .knx-button-row {
        margin-top: 20px;
      }

      .knx-info {
        margin-right: 8px;
      }
    }

    @media screen and (min-width: 1233px) {
      .knx-button-row {
        margin-top: auto;
      }

      .knx-info {
        width: 400px;
      }
    }

    .knx-info {
      margin-left: 8px;
      margin-top: 8px;
    }

    .knx-content {
      display: flex;
      flex-direction: column;
      height: 100%;
      box-sizing: border-box;
    }

    .knx-content-row {
      display: flex;
      flex-direction: row;
      justify-content: space-between;
    }

    .knx-content-row > div:nth-child(2) {
      margin-left: 1rem;
    }

    .knx-button-row {
      display: flex;
      flex-direction: row;
      vertical-align: bottom;
      padding-top: 16px;
    }

    .push-left {
      margin-right: auto;
    }

    .push-right {
      margin-left: auto;
    }

    .knx-warning {
      --mdc-theme-primary: var(--error-color);
    }

    .knx-project-description {
      margin-top: -8px;
      padding: 0px 16px 16px;
    }

    .knx-delete-project-button {
      position: absolute;
      bottom: 0;
      right: 0;
    }

    .knx-bug-report {
      margin-top: 20px;

      a {
        text-decoration: none;
      }
    }

    .header {
      color: var(--ha-card-header-color, --primary-text-color);
      font-family: var(--ha-card-header-font-family, inherit);
      font-size: var(--ha-card-header-font-size, 24px);
      letter-spacing: -0.012em;
      line-height: 48px;
      padding: -4px 16px 16px;
      display: inline-block;
      margin-block-start: 0px;
      margin-block-end: 4px;
      font-weight: normal;
    }

    ha-file-upload,
    ha-selector-text {
      width: 100%;
      margin-top: 8px;
    }
  `)),(0,a.__decorate)([(0,n.Cb)({type:Object})],z.prototype,"hass",void 0),(0,a.__decorate)([(0,n.Cb)({attribute:!1})],z.prototype,"knx",void 0),(0,a.__decorate)([(0,n.Cb)({type:Boolean,reflect:!0})],z.prototype,"narrow",void 0),(0,a.__decorate)([(0,n.Cb)({type:Object})],z.prototype,"route",void 0),(0,a.__decorate)([(0,n.Cb)({type:Array,reflect:!1})],z.prototype,"tabs",void 0),(0,a.__decorate)([(0,n.SB)()],z.prototype,"_projectPassword",void 0),(0,a.__decorate)([(0,n.SB)()],z.prototype,"_uploading",void 0),(0,a.__decorate)([(0,n.SB)()],z.prototype,"_projectFile",void 0),z=(0,a.__decorate)([(0,n.Mo)("knx-info")],z),o()}catch(m){o(m)}}))}}]);
//# sourceMappingURL=3188.0e938cf6a7a89fd1.js.map