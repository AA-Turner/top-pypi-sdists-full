export const __rspack_esm_id="27465";export const __rspack_esm_ids=["27465"];export const __webpack_modules__={69093(e,t,a){a.d(t,{t:()=>i});var o=a(71727);const i=e=>(0,o.m)(e.entity_id)},82286(e,t,a){a.d(t,{$:()=>o});const o=(e,t)=>i(e.attributes,t),i=(e,t)=>0!==(e.supported_features&t)},38962(e,t,a){a.r(t);var o=a(62826),i=a(96196),r=a(44457),s=a(94333),l=a(1087);a(26300),a(67094);const n={info:"M11,9H13V7H11M12,20C7.59,20 4,16.41 4,12C4,7.59 7.59,4 12,4C16.41,4 20,7.59 20,12C20,16.41 16.41,20 12,20M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M11,17H13V11H11V17Z",warning:"M12,2L1,21H23M12,6L19.53,19H4.47M11,10V14H13V10M11,16V18H13V16",error:"M11,15H13V17H11V15M11,7H13V13H11V7M12,2C6.47,2 2,6.5 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M12,20A8,8 0 0,1 4,12A8,8 0 0,1 12,4A8,8 0 0,1 20,12A8,8 0 0,1 12,20Z",success:"M20,12A8,8 0 0,1 12,20A8,8 0 0,1 4,12A8,8 0 0,1 12,4C12.76,4 13.5,4.11 14.2,4.31L15.77,2.74C14.61,2.26 13.34,2 12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12M7.91,10.08L6.5,11.5L11,16L21,6L19.59,4.58L11,13.17L7.91,10.08Z"};class d extends i.WF{render(){return i.qy` <div class="issue-type ${(0,s.H)({[this.alertType]:!0})}" role="alert"> <div class="icon ${this.title?"":"no-title"}"> <slot name="icon"> <ha-svg-icon .path="${n[this.alertType]}"></ha-svg-icon> </slot> </div> <div class="${(0,s.H)({content:!0,narrow:this.narrow})}"> <div class="main-content"> ${this.title?i.qy`<div class="title">${this.title}</div>`:i.s6} <slot></slot> </div> <div class="action"> <slot name="action"> ${this.dismissable?i.qy`<ha-icon-button @click="${this._dismissClicked}" label="Dismiss alert" .path="${"M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z"}"></ha-icon-button>`:i.s6} </slot> </div> </div> </div> `}_dismissClicked(){(0,l.r)(this,"alert-dismissed-clicked")}constructor(...e){super(...e),this.title="",this.alertType="info",this.dismissable=!1,this.narrow=!1}}d.styles=i.AH`.issue-type{position:relative;padding:8px;display:flex}.icon{height:var(--ha-alert-icon-size,24px);width:var(--ha-alert-icon-size,24px)}.issue-type::after{position:absolute;top:0;right:0;bottom:0;left:0;opacity:.12;pointer-events:none;content:"";border-radius:var(--ha-border-radius-sm)}.icon.no-title{align-self:center}.content{display:flex;justify-content:space-between;align-items:center;width:100%;text-align:var(--float-start)}.content.narrow{flex-direction:column;align-items:flex-end}.action{z-index:1;width:min-content;--mdc-theme-primary:var(--primary-text-color)}.main-content{overflow-wrap:anywhere;word-break:break-word;line-height:normal;margin-left:8px;margin-right:0;margin-inline-start:8px;margin-inline-end:8px}.title{margin-top:2px;font-weight:var(--ha-font-weight-bold)}.action ha-icon-button{--mdc-theme-primary:var(--primary-text-color);--mdc-icon-button-size:36px}.issue-type.info>.icon{color:var(--info-color)}.issue-type.info::after{background-color:var(--info-color)}.issue-type.warning>.icon{color:var(--warning-color)}.issue-type.warning::after{background-color:var(--warning-color)}.issue-type.error>.icon{color:var(--error-color)}.issue-type.error::after{background-color:var(--error-color)}.issue-type.success>.icon{color:var(--success-color)}.issue-type.success::after{background-color:var(--success-color)}:host ::slotted(ul){margin:0;padding-inline-start:20px}`,(0,o.Cg)([(0,r.MZ)()],d.prototype,"title",void 0),(0,o.Cg)([(0,r.MZ)({attribute:"alert-type"})],d.prototype,"alertType",void 0),(0,o.Cg)([(0,r.MZ)({type:Boolean})],d.prototype,"dismissable",void 0),(0,o.Cg)([(0,r.MZ)({type:Boolean})],d.prototype,"narrow",void 0),d=(0,o.Cg)([(0,r.EM)("ha-alert")],d)},93444(e,t,a){var o=a(62826),i=a(96196),r=a(44457);class s extends i.WF{render(){return i.qy` <footer> <slot name="secondaryAction"></slot> <slot name="primaryAction"></slot> </footer> `}static get styles(){return[i.AH`footer{display:flex;gap:var(--ha-space-3);justify-content:flex-end;align-items:center;width:100%}`]}}s=(0,o.Cg)([(0,r.EM)("ha-dialog-footer")],s)},45331(e,t,a){a.a(e,async function(e,t){try{var o=a(62826),i=a(93900),r=a(96196),s=a(44457),l=a(32288),n=a(1087),d=a(59992),c=a(14503),h=(a(76538),a(26300),e([i]));i=(h.then?(await h)():h)[0];const p="M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z";class u extends((0,d.V)(r.WF)){get scrollableElement(){return this.bodyContainer}updated(e){super.updated(e),e.has("open")&&(this._open=this.open)}render(){return r.qy` <wa-dialog .open="${this._open}" .lightDismiss="${!this.preventScrimClose}" without-header aria-labelledby="${(0,l.J)(this.ariaLabelledBy||(void 0!==this.headerTitle?"ha-wa-dialog-title":void 0))}" aria-describedby="${(0,l.J)(this.ariaDescribedBy)}" @wa-show="${this._handleShow}" @wa-after-show="${this._handleAfterShow}" @wa-after-hide="${this._handleAfterHide}"> <slot name="header"> <ha-dialog-header .subtitlePosition="${this.headerSubtitlePosition}" .showBorder="${this._bodyScrolled}"> <slot name="headerNavigationIcon" slot="navigationIcon"> <ha-icon-button data-dialog="close" .label="${this.hass?.localize("ui.common.close")??"Close"}" .path="${p}"></ha-icon-button> </slot> ${void 0!==this.headerTitle?r.qy`<span slot="title" class="title" id="ha-wa-dialog-title"> ${this.headerTitle} </span>`:r.qy`<slot name="headerTitle" slot="title"></slot>`} ${void 0!==this.headerSubtitle?r.qy`<span slot="subtitle">${this.headerSubtitle}</span>`:r.qy`<slot name="headerSubtitle" slot="subtitle"></slot>`} <slot name="headerActionItems" slot="actionItems"></slot> </ha-dialog-header> </slot> <div class="content-wrapper"> <div class="body ha-scrollbar" @scroll="${this._handleBodyScroll}"> <slot></slot> </div> ${this.renderScrollableFades()} </div> <slot name="footer" slot="footer"></slot> </wa-dialog> `}disconnectedCallback(){super.disconnectedCallback(),this._open=!1}_handleBodyScroll(e){this._bodyScrolled=e.target.scrollTop>0}static get styles(){return[...super.styles,c.dp,r.AH`
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
      `]}constructor(...e){super(...e),this.open=!1,this.type="standard",this.width="medium",this.preventScrimClose=!1,this.headerSubtitlePosition="below",this.flexContent=!1,this._open=!1,this._bodyScrolled=!1,this._handleShow=async()=>{this._open=!0,(0,n.r)(this,"opened"),await this.updateComplete,requestAnimationFrame(()=>{this.querySelector("[autofocus]")?.focus()})},this._handleAfterShow=()=>{(0,n.r)(this,"after-show")},this._handleAfterHide=()=>{this._open=!1,(0,n.r)(this,"closed")}}}(0,o.Cg)([(0,s.MZ)({attribute:!1})],u.prototype,"hass",void 0),(0,o.Cg)([(0,s.MZ)({attribute:"aria-labelledby"})],u.prototype,"ariaLabelledBy",void 0),(0,o.Cg)([(0,s.MZ)({attribute:"aria-describedby"})],u.prototype,"ariaDescribedBy",void 0),(0,o.Cg)([(0,s.MZ)({type:Boolean,reflect:!0})],u.prototype,"open",void 0),(0,o.Cg)([(0,s.MZ)({reflect:!0})],u.prototype,"type",void 0),(0,o.Cg)([(0,s.MZ)({type:String,reflect:!0,attribute:"width"})],u.prototype,"width",void 0),(0,o.Cg)([(0,s.MZ)({type:Boolean,reflect:!0,attribute:"prevent-scrim-close"})],u.prototype,"preventScrimClose",void 0),(0,o.Cg)([(0,s.MZ)({attribute:"header-title"})],u.prototype,"headerTitle",void 0),(0,o.Cg)([(0,s.MZ)({attribute:"header-subtitle"})],u.prototype,"headerSubtitle",void 0),(0,o.Cg)([(0,s.MZ)({type:String,attribute:"header-subtitle-position"})],u.prototype,"headerSubtitlePosition",void 0),(0,o.Cg)([(0,s.MZ)({type:Boolean,reflect:!0,attribute:"flexcontent"})],u.prototype,"flexContent",void 0),(0,o.Cg)([(0,s.wk)()],u.prototype,"_open",void 0),(0,o.Cg)([(0,s.P)(".body")],u.prototype,"bodyContainer",void 0),(0,o.Cg)([(0,s.wk)()],u.prototype,"_bodyScrolled",void 0),(0,o.Cg)([(0,s.Ls)({passive:!0})],u.prototype,"_handleBodyScroll",null),u=(0,o.Cg)([(0,s.EM)("ha-wa-dialog")],u),t()}catch(e){t(e)}})},59992(e,t,a){a.d(t,{V:()=>n});var o=a(62826),i=a(88696),r=a(96196),s=a(94333),l=a(44457);const n=e=>{class t extends e{get scrollableElement(){return t.DEFAULT_SCROLLABLE_ELEMENT}firstUpdated(e){super.firstUpdated?.(e),this.scrollableElement&&this._updateScrollableState(this.scrollableElement),this._attachScrollableElement()}updated(e){super.updated?.(e),this._attachScrollableElement()}disconnectedCallback(){this._detachScrollableElement(),this._contentScrolled=!1,this._contentScrollable=!1,super.disconnectedCallback()}renderScrollableFades(e=!1){return r.qy` <div class="${(0,s.H)({"fade-top":!0,rounded:e,visible:this._contentScrolled})}"></div> <div class="${(0,s.H)({"fade-bottom":!0,rounded:e,visible:this._contentScrollable})}"></div> `}static get styles(){const e=Object.getPrototypeOf(this);var t;return[...void 0===(t=e?.styles??[])?[]:Array.isArray(t)?t:[t],r.AH`.fade-bottom,.fade-top{position:absolute;left:0;right:0;height:var(--ha-space-2);pointer-events:none;transition:opacity 180ms ease-in-out;border-radius:var(--ha-border-radius-square);opacity:0;background:linear-gradient(to bottom,var(--ha-color-shadow-scrollable-fade),transparent)}.fade-top{top:0}.fade-bottom{bottom:0;transform:rotate(180deg)}.fade-bottom.visible,.fade-top.visible{opacity:1}.fade-bottom.rounded,.fade-top.rounded{border-radius:var(--ha-card-border-radius,var(--ha-border-radius-lg));border-bottom-left-radius:var(--ha-border-radius-square);border-bottom-right-radius:var(--ha-border-radius-square)}.fade-top.rounded{border-top-left-radius:var(--ha-border-radius-square);border-top-right-radius:var(--ha-border-radius-square)}.fade-bottom.rounded{border-bottom-left-radius:var(--ha-border-radius-square);border-bottom-right-radius:var(--ha-border-radius-square)}`]}_attachScrollableElement(){const e=this.scrollableElement;e!==this._scrollTarget&&(this._detachScrollableElement(),e&&(this._scrollTarget=e,e.addEventListener("scroll",this._onScroll,{passive:!0}),this._resize.observe(e),this._updateScrollableState(e)))}_detachScrollableElement(){this._scrollTarget&&(this._scrollTarget.removeEventListener("scroll",this._onScroll),this._resize.unobserve?.(this._scrollTarget),this._scrollTarget=void 0)}_updateScrollableState(e){const t=parseFloat(getComputedStyle(e).getPropertyValue("--safe-area-inset-bottom"))||0,{scrollHeight:a=0,clientHeight:o=0,scrollTop:i=0}=e;this._contentScrollable=a-o>i+t+this.scrollFadeSafeAreaPadding}constructor(...e){super(...e),this._contentScrolled=!1,this._contentScrollable=!1,this._onScroll=e=>{const t=e.currentTarget;this._contentScrolled=(t.scrollTop??0)>this.scrollFadeThreshold,this._updateScrollableState(t)},this._resize=new i.P(this,{target:null,callback:e=>{const t=e[0]?.target;t&&this._updateScrollableState(t)}}),this.scrollFadeSafeAreaPadding=4,this.scrollFadeThreshold=4}}return t.DEFAULT_SCROLLABLE_ELEMENT=null,(0,o.Cg)([(0,l.wk)()],t.prototype,"_contentScrolled",void 0),(0,o.Cg)([(0,l.wk)()],t.prototype,"_contentScrollable",void 0),t}},24367(e,t,a){a.d(t,{L:()=>i,z:()=>r});var o=a(23832);const i=["input_boolean","input_button","input_text","input_number","input_datetime","input_select","counter","timer","schedule"],r=(0,o.g)(i)},84309(e,t,a){a.a(e,async function(e,o){try{a.r(t),a.d(t,{DialogLovelaceResourceDetail:()=>u});var i=a(62826),r=a(96196),s=a(44457),l=a(22786),n=a(1087),d=a(45331),c=(a(93444),a(38962),a(52763),a(18350)),h=e([d,c]);[d,c]=h.then?(await h)():h;const p=e=>{if(!e)return;const t=e.split(".").pop()||"";return"css"===t?"css":"js"===t?"module":void 0};class u extends r.WF{showDialog(e){this._params=e,this._error=void 0,this._params.resource?this._data={url:this._params.resource.url,res_type:this._params.resource.type}:this._data={url:""},this._open=!0}closeDialog(){this._open=!1}_dialogClosed(){this._params=void 0,(0,n.r)(this,"dialog-closed",{dialog:this.localName})}render(){if(!this._params)return r.s6;const e=!this._data?.url||""===this._data.url.trim(),t=this._params.resource?.url||this.hass.localize("ui.panel.config.lovelace.resources.detail.new_resource");return r.qy` <ha-wa-dialog .hass="${this.hass}" .open="${this._open}" prevent-scrim-close header-title="${t}" @closed="${this._dialogClosed}"> <ha-alert alert-type="warning" .title="${this.hass.localize("ui.panel.config.lovelace.resources.detail.warning_header")}"> ${this.hass.localize("ui.panel.config.lovelace.resources.detail.warning_text")} </ha-alert> <ha-form autofocus .schema="${this._schema(this._data)}" .data="${this._data}" .hass="${this.hass}" .error="${this._error}" .computeLabel="${this._computeLabel}" @value-changed="${this._valueChanged}"></ha-form> <ha-dialog-footer slot="footer"> <ha-button appearance="plain" slot="secondaryAction" @click="${this.closeDialog}"> ${this.hass.localize("ui.common.cancel")} </ha-button> <ha-button slot="primaryAction" @click="${this._updateResource}" .disabled="${e||!this._data?.res_type||this._submitting}"> ${this._params.resource?this.hass.localize("ui.panel.config.lovelace.resources.detail.update"):this.hass.localize("ui.panel.config.lovelace.resources.detail.create")} </ha-button> </ha-dialog-footer> </ha-wa-dialog> `}_valueChanged(e){if(this._data=e.detail.value,!this._data.res_type){const e=p(this._data.url);if(!e)return;this._data={...this._data,res_type:e}}}async _updateResource(){if(this._data?.res_type){this._submitting=!0;try{this._params.resource?await this._params.updateResource(this._data):await this._params.createResource(this._data),this._params=void 0}catch(e){this._error={base:e?.message||"Unknown error"}}finally{this._submitting=!1}}}constructor(...e){super(...e),this._submitting=!1,this._open=!1,this._schema=(0,l.A)(e=>[{name:"url",required:!0,selector:{text:{}}},{name:"res_type",required:!0,selector:{select:{options:[{value:"module",label:this.hass.localize("ui.panel.config.lovelace.resources.types.module")},{value:"css",label:this.hass.localize("ui.panel.config.lovelace.resources.types.css")},..."js"===e.type?[{value:"js",label:this.hass.localize("ui.panel.config.lovelace.resources.types.js")}]:[],..."html"===e.type?[{value:"html",label:this.hass.localize("ui.panel.config.lovelace.resources.types.html")}]:[]]}}}]),this._computeLabel=e=>this.hass.localize(`ui.panel.config.lovelace.resources.detail.${"res_type"===e.name?"type":e.name}`)}}(0,i.Cg)([(0,s.MZ)({attribute:!1})],u.prototype,"hass",void 0),(0,i.Cg)([(0,s.wk)()],u.prototype,"_params",void 0),(0,i.Cg)([(0,s.wk)()],u.prototype,"_data",void 0),(0,i.Cg)([(0,s.wk)()],u.prototype,"_error",void 0),(0,i.Cg)([(0,s.wk)()],u.prototype,"_submitting",void 0),(0,i.Cg)([(0,s.wk)()],u.prototype,"_open",void 0),u=(0,i.Cg)([(0,s.EM)("dialog-lovelace-resource-detail")],u),o()}catch(e){o(e)}})},48646(e,t,a){var o=a(69565),i=a(28551),r=a(1767),s=a(50851);e.exports=function(e,t){t&&"string"==typeof e||i(e);var a=s(e);return r(i(void 0!==a?o(a,e):e))}},30531(e,t,a){var o=a(46518),i=a(69565),r=a(79306),s=a(28551),l=a(1767),n=a(48646),d=a(19462),c=a(9539),h=a(96395),p=a(30684),u=a(84549),g=!h&&!p("flatMap",function(){}),f=!h&&!g&&u("flatMap",TypeError),m=h||g||f,v=d(function(){for(var e,t,a=this.iterator,o=this.mapper;;){if(t=this.inner)try{if(!(e=s(i(t.next,t.iterator))).done)return e.value;this.inner=null}catch(e){c(a,"throw",e)}if(e=s(i(this.next,a)),this.done=!!e.done)return;try{this.inner=n(o(e.value,this.counter++),!1)}catch(e){c(a,"throw",e)}}});o({target:"Iterator",proto:!0,real:!0,forced:m},{flatMap:function(e){s(this);try{r(e)}catch(e){c(this,"throw",e)}return f?i(f,this,e):new v(l(this),{mapper:e,inner:null})}})},99793(e,t,a){a.d(t,{A:()=>o});const o=a(96196).AH`:host{--width:31rem;--spacing:var(--wa-space-l);--show-duration:200ms;--hide-duration:200ms;display:none}:host([open]){display:block}.dialog{display:flex;flex-direction:column;top:0;right:0;bottom:0;left:0;width:var(--width);max-width:calc(100% - var(--wa-space-2xl));max-height:calc(100% - var(--wa-space-2xl));background-color:var(--wa-color-surface-raised);border-radius:var(--wa-panel-border-radius);border:none;box-shadow:var(--wa-shadow-l);padding:0;margin:auto}.dialog.show{animation:show-dialog var(--show-duration) ease}.dialog.show::backdrop{animation:show-backdrop var(--show-duration,200ms) ease}.dialog.hide{animation:show-dialog var(--hide-duration) ease reverse}.dialog.hide::backdrop{animation:show-backdrop var(--hide-duration,200ms) ease reverse}.dialog.pulse{animation:pulse 250ms ease}.dialog:focus{outline:0}@media screen and (max-width:420px){.dialog{max-height:80vh}}.open{display:flex;opacity:1}.header{flex:0 0 auto;display:flex;flex-wrap:nowrap;padding-inline-start:var(--spacing);padding-block-end:0;padding-inline-end:calc(var(--spacing) - var(--wa-form-control-padding-block));padding-block-start:calc(var(--spacing) - var(--wa-form-control-padding-block))}.title{align-self:center;flex:1 1 auto;font-family:inherit;font-size:var(--wa-font-size-l);font-weight:var(--wa-font-weight-heading);line-height:var(--wa-line-height-condensed);margin:0}.header-actions{align-self:start;display:flex;flex-shrink:0;flex-wrap:wrap;justify-content:end;gap:var(--wa-space-2xs);padding-inline-start:var(--spacing)}.header-actions ::slotted(wa-button),.header-actions wa-button{flex:0 0 auto;display:flex;align-items:center}.body{flex:1 1 auto;display:block;padding:var(--spacing);overflow:auto;-webkit-overflow-scrolling:touch}.body:focus{outline:0}.body:focus-visible{outline:var(--wa-focus-ring);outline-offset:var(--wa-focus-ring-offset)}.footer{flex:0 0 auto;display:flex;flex-wrap:wrap;gap:var(--wa-space-xs);justify-content:end;padding:var(--spacing);padding-block-start:0}.footer ::slotted(wa-button:not(:first-of-type)){margin-inline-start:var(--wa-spacing-xs)}.dialog::backdrop{background-color:var(--wa-color-overlay-modal,rgb(0 0 0 / .25))}@keyframes pulse{0%{scale:1}50%{scale:1.02}100%{scale:1}}@keyframes show-dialog{from{opacity:0;scale:0.8}to{opacity:1;scale:1}}@keyframes show-backdrop{from{opacity:0}to{opacity:1}}@media (forced-colors:active){.dialog{border:solid 1px #fff}}`},93900(e,t,a){a.a(e,async function(e,t){try{var o=a(96196),i=a(44457),r=a(94333),s=a(32288),l=a(17051),n=a(42462),d=a(28438),c=a(98779),h=a(27259),p=a(31247),u=a(97039),g=a(92070),f=a(9395),m=a(32510),v=a(17060),b=a(88496),w=a(99793),y=e([b,v]);[b,v]=y.then?(await y)():y;var _=Object.defineProperty,x=Object.getOwnPropertyDescriptor,C=(e,t,a,o)=>{for(var i,r=o>1?void 0:o?x(t,a):t,s=e.length-1;s>=0;s--)(i=e[s])&&(r=(o?i(t,a,r):i(r))||r);return o&&r&&_(t,a,r),r};let L=class extends m.A{firstUpdated(){this.open&&(this.addOpenListeners(),this.dialog.showModal(),(0,u.JG)(this))}disconnectedCallback(){super.disconnectedCallback(),(0,u.I7)(this),this.removeOpenListeners()}async requestClose(e){const t=new d.L({source:e});if(this.dispatchEvent(t),t.defaultPrevented)return this.open=!0,void(0,h.Ud)(this.dialog,"pulse");this.removeOpenListeners(),await(0,h.Ud)(this.dialog,"hide"),this.open=!1,this.dialog.close(),(0,u.I7)(this);const a=this.originalTrigger;"function"==typeof a?.focus&&setTimeout(()=>a.focus()),this.dispatchEvent(new l.Z)}addOpenListeners(){document.addEventListener("keydown",this.handleDocumentKeyDown)}removeOpenListeners(){document.removeEventListener("keydown",this.handleDocumentKeyDown)}handleDialogCancel(e){e.preventDefault(),this.dialog.classList.contains("hide")||e.target!==this.dialog||this.requestClose(this.dialog)}handleDialogClick(e){const t=e.target.closest('[data-dialog="close"]');t&&(e.stopPropagation(),this.requestClose(t))}async handleDialogPointerDown(e){e.target===this.dialog&&(this.lightDismiss?this.requestClose(this.dialog):await(0,h.Ud)(this.dialog,"pulse"))}handleOpenChange(){this.open&&!this.dialog.open?this.show():!this.open&&this.dialog.open&&(this.open=!0,this.requestClose(this.dialog))}async show(){const e=new c.k;this.dispatchEvent(e),e.defaultPrevented?this.open=!1:(this.addOpenListeners(),this.originalTrigger=document.activeElement,this.open=!0,this.dialog.showModal(),(0,u.JG)(this),requestAnimationFrame(()=>{const e=this.querySelector("[autofocus]");e&&"function"==typeof e.focus?e.focus():this.dialog.focus()}),await(0,h.Ud)(this.dialog,"show"),this.dispatchEvent(new n.q))}render(){const e=!this.withoutHeader,t=this.hasSlotController.test("footer");return o.qy` <dialog aria-labelledby="${this.ariaLabelledby??"title"}" aria-describedby="${(0,s.J)(this.ariaDescribedby)}" part="dialog" class="${(0,r.H)({dialog:!0,open:this.open})}" @cancel="${this.handleDialogCancel}" @click="${this.handleDialogClick}" @pointerdown="${this.handleDialogPointerDown}"> ${e?o.qy` <header part="header" class="header"> <h2 part="title" class="title" id="title"> <slot name="label"> ${this.label.length>0?this.label:String.fromCharCode(8203)} </slot> </h2> <div part="header-actions" class="header-actions"> <slot name="header-actions"></slot> <wa-button part="close-button" exportparts="base:close-button__base" class="close" appearance="plain" @click="${e=>this.requestClose(e.target)}"> <wa-icon name="xmark" label="${this.localize.term("close")}" library="system" variant="solid"></wa-icon> </wa-button> </div> </header> `:""} <div part="body" class="body"><slot></slot></div> ${t?o.qy` <footer part="footer" class="footer"> <slot name="footer"></slot> </footer> `:""} </dialog> `}constructor(){super(...arguments),this.localize=new v.c(this),this.hasSlotController=new g.X(this,"footer","header-actions","label"),this.open=!1,this.label="",this.withoutHeader=!1,this.lightDismiss=!1,this.handleDocumentKeyDown=e=>{"Escape"===e.key&&this.open&&(e.preventDefault(),e.stopPropagation(),this.requestClose(this.dialog))}}};L.css=w.A,C([(0,i.P)(".dialog")],L.prototype,"dialog",2),C([(0,i.MZ)({type:Boolean,reflect:!0})],L.prototype,"open",2),C([(0,i.MZ)({reflect:!0})],L.prototype,"label",2),C([(0,i.MZ)({attribute:"without-header",type:Boolean,reflect:!0})],L.prototype,"withoutHeader",2),C([(0,i.MZ)({attribute:"light-dismiss",type:Boolean})],L.prototype,"lightDismiss",2),C([(0,i.MZ)({attribute:"aria-labelledby"})],L.prototype,"ariaLabelledby",2),C([(0,i.MZ)({attribute:"aria-describedby"})],L.prototype,"ariaDescribedby",2),C([(0,f.w)("open",{waitUntilFirstUpdate:!0})],L.prototype,"handleOpenChange",1),L=C([(0,i.EM)("wa-dialog")],L),document.addEventListener("click",e=>{const t=e.target.closest("[data-dialog]");if(t instanceof Element){const[e,a]=(0,p.v)(t.getAttribute("data-dialog")||"");if("open"===e&&a?.length){const e=t.getRootNode().getElementById(a);"wa-dialog"===e?.localName?e.open=!0:console.warn(`A dialog with an ID of "${a}" could not be found in this document.`)}}}),o.S$||document.addEventListener("pointerdown",()=>{}),t()}catch(e){t(e)}})},17051(e,t,a){a.d(t,{Z:()=>o});class o extends Event{constructor(){super("wa-after-hide",{bubbles:!0,cancelable:!1,composed:!0})}}},42462(e,t,a){a.d(t,{q:()=>o});class o extends Event{constructor(){super("wa-after-show",{bubbles:!0,cancelable:!1,composed:!0})}}},28438(e,t,a){a.d(t,{L:()=>o});class o extends Event{constructor(e){super("wa-hide",{bubbles:!0,cancelable:!0,composed:!0}),this.detail=e}}},98779(e,t,a){a.d(t,{k:()=>o});class o extends Event{constructor(){super("wa-show",{bubbles:!0,cancelable:!0,composed:!0})}}},27259(e,t,a){async function o(e,t,a){return e.animate(t,a).finished.catch(()=>{})}function i(e,t){return new Promise(a=>{const o=new AbortController,{signal:i}=o;if(e.classList.contains(t))return;e.classList.remove(t),e.classList.add(t);let r=()=>{e.classList.remove(t),a(),o.abort()};e.addEventListener("animationend",r,{once:!0,signal:i}),e.addEventListener("animationcancel",r,{once:!0,signal:i})})}function r(e){return(e=e.toString().toLowerCase()).indexOf("ms")>-1?parseFloat(e)||0:e.indexOf("s")>-1?1e3*(parseFloat(e)||0):parseFloat(e)||0}a.d(t,{E9:()=>r,Ud:()=>i,i0:()=>o})},91081(e,t,a){function o(e,t){return{top:Math.round(e.getBoundingClientRect().top-t.getBoundingClientRect().top),left:Math.round(e.getBoundingClientRect().left-t.getBoundingClientRect().left)}}a.d(t,{A:()=>o})},31247(e,t,a){a.d(t,{v:()=>o});a(18111),a(22489),a(61701);function o(e){return e.split(" ").map(e=>e.trim()).filter(e=>""!==e)}},97039(e,t,a){a.d(t,{I7:()=>s,JG:()=>r,Rt:()=>l});a(17642),a(58004),a(33853),a(45876),a(32475),a(15024),a(31698);var o=a(91081);const i=new Set;function r(e){if(i.add(e),!document.documentElement.classList.contains("wa-scroll-lock")){const e=function(){const e=document.documentElement.clientWidth;return Math.abs(window.innerWidth-e)}()+function(){const e=Number(getComputedStyle(document.body).paddingRight.replace(/px/,""));return isNaN(e)||!e?0:e}();let t=getComputedStyle(document.documentElement).scrollbarGutter;t&&"auto"!==t||(t="stable"),e<2&&(t=""),document.documentElement.style.setProperty("--wa-scroll-lock-gutter",t),document.documentElement.classList.add("wa-scroll-lock"),document.documentElement.style.setProperty("--wa-scroll-lock-size",`${e}px`)}}function s(e){i.delete(e),0===i.size&&(document.documentElement.classList.remove("wa-scroll-lock"),document.documentElement.style.removeProperty("--wa-scroll-lock-size"))}function l(e,t,a="vertical",i="smooth"){const r=(0,o.A)(e,t),s=r.top+t.scrollTop,l=r.left+t.scrollLeft,n=t.scrollLeft,d=t.scrollLeft+t.offsetWidth,c=t.scrollTop,h=t.scrollTop+t.offsetHeight;"horizontal"!==a&&"both"!==a||(l<n?t.scrollTo({left:l,behavior:i}):l+e.clientWidth>d&&t.scrollTo({left:l-t.offsetWidth+e.clientWidth,behavior:i})),"vertical"!==a&&"both"!==a||(s<c?t.scrollTo({top:s,behavior:i}):s+e.clientHeight>h&&t.scrollTo({top:s-t.offsetHeight+e.clientHeight,behavior:i}))}}};
//# sourceMappingURL=27465.38df6aa28f786d3c.js.map