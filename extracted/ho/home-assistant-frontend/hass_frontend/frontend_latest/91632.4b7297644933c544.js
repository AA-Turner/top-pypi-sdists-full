export const __rspack_esm_id="91632";export const __rspack_esm_ids=["91632"];export const __webpack_modules__={93905(e,t,a){a.d(t,{I:()=>r});a(44114),a(18111),a(7588),a(69112),a(33110);class i{addFromStorage(e){if(!this._storage[e]){const t=this.storage.getItem(e);t&&(this._storage[e]=JSON.parse(t))}}subscribeChanges(e,t){return this._listeners[e]?this._listeners[e].push(t):this._listeners[e]=[t],()=>{this.unsubscribeChanges(e,t)}}unsubscribeChanges(e,t){if(!(e in this._listeners))return;const a=this._listeners[e].indexOf(t);-1!==a&&this._listeners[e].splice(a,1)}hasKey(e){return e in this._storage}getValue(e){return this._storage[e]}setValue(e,t){const a=this._storage[e];this._storage[e]=t;try{void 0===t?this.storage.removeItem(e):this.storage.setItem(e,JSON.stringify(t))}catch(e){}finally{this._listeners[e]&&this._listeners[e].forEach(e=>e(a,t))}}constructor(e=window.localStorage){this._storage={},this._listeners={},this.storage=e,this.storage===window.localStorage&&window.addEventListener("storage",e=>{e.key&&this.hasKey(e.key)&&(this._storage[e.key]=e.newValue?JSON.parse(e.newValue):e.newValue,this._listeners[e.key]&&this._listeners[e.key].forEach(t=>t(e.oldValue?JSON.parse(e.oldValue):e.oldValue,this._storage[e.key])))})}}const o={};function r(e){return(t,a)=>{if("object"==typeof a)throw new Error("This decorator does not support this compilation type.");const r=e.storage||"localStorage";let n;r&&r in o?n=o[r]:(n=new i(window[r]),o[r]=n);const s=e.key||String(a);n.addFromStorage(s);const l=!1!==e.subscribe?e=>n.subscribeChanges(s,(t,i)=>{e.requestUpdate(a,t)}):void 0,d=()=>n.hasKey(s)?e.deserializer?e.deserializer(n.getValue(s)):n.getValue(s):void 0,h=(t,i)=>{let o;e.state&&(o=d()),n.setValue(s,e.serializer?e.serializer(i):i),e.state&&t.requestUpdate(a,o)},c=t.performUpdate;if(t.performUpdate=function(){this.__initialized=!0,c.call(this)},e.subscribe){const e=t.connectedCallback,a=t.disconnectedCallback;t.connectedCallback=function(){e.call(this);const t=this;t.__unbsubLocalStorage||(t.__unbsubLocalStorage=l?.(this))},t.disconnectedCallback=function(){a.call(this);this.__unbsubLocalStorage?.(),this.__unbsubLocalStorage=void 0}}const p=Object.getOwnPropertyDescriptor(t,a);let g;if(void 0===p)g={get:()=>d(),set(e){(this.__initialized||void 0===d())&&h(this,e)},configurable:!0,enumerable:!0};else{const e=p.set;g={...p,get:()=>d(),set(t){(this.__initialized||void 0===d())&&h(this,t),e?.call(this,t)}}}Object.defineProperty(t,a,g)}}},57237(e,t,a){a.d(t,{d:()=>i});const i=e=>e.stopPropagation()},82286(e,t,a){a.d(t,{$:()=>i});const i=(e,t)=>o(e.attributes,t),o=(e,t)=>0!==(e.supported_features&t)},64481(e,t,a){a.d(t,{D:()=>o,J:()=>r});let i=!1;try{i="true"===window.localStorage.getItem("disableViewTransition")}catch{}const o=e=>{i=e},r=e=>{if(!document.startViewTransition||i)return e(!1),Promise.resolve();let t=!1;try{return document.startViewTransition(()=>{t=!0,e(!0)}).finished}catch(a){return console.warn("View transition failed, falling back to direct execution.",a),t?Promise.reject(a):(e(!1),Promise.resolve())}}},38962(e,t,a){a.a(e,async function(e,i){try{a.r(t);var o=a(62826),r=a(96196),n=a(97735),s=a(94333),l=a(1087),d=a(26300),h=(a(67094),e([d]));d=(h.then?(await h)():h)[0];const c="M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z",p={info:"M11,9H13V7H11M12,20C7.59,20 4,16.41 4,12C4,7.59 7.59,4 12,4C16.41,4 20,7.59 20,12C20,16.41 16.41,20 12,20M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M11,17H13V11H11V17Z",warning:"M12,2L1,21H23M12,6L19.53,19H4.47M11,10V14H13V10M11,16V18H13V16",error:"M11,15H13V17H11V15M11,7H13V13H11V7M12,2C6.47,2 2,6.5 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M12,20A8,8 0 0,1 4,12A8,8 0 0,1 12,4A8,8 0 0,1 20,12A8,8 0 0,1 12,20Z",success:"M20,12A8,8 0 0,1 12,20A8,8 0 0,1 4,12A8,8 0 0,1 12,4C12.76,4 13.5,4.11 14.2,4.31L15.77,2.74C14.61,2.26 13.34,2 12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12M7.91,10.08L6.5,11.5L11,16L21,6L19.59,4.58L11,13.17L7.91,10.08Z"};class g extends r.WF{render(){return r.qy` <div class="issue-type ${(0,s.H)({[this.alertType]:!0})}" role="alert"> <div class="icon ${this.title?"":"no-title"}"> <slot name="icon"> <ha-svg-icon .path="${p[this.alertType]}"></ha-svg-icon> </slot> </div> <div class="${(0,s.H)({content:!0,narrow:this.narrow})}"> <div class="main-content"> ${this.title?r.qy`<div class="title">${this.title}</div>`:r.s6} <slot></slot> </div> <div class="action"> <slot name="action"> ${this.dismissable?r.qy`<ha-icon-button @click="${this._dismissClicked}" label="Dismiss alert" .path="${c}"></ha-icon-button>`:r.s6} </slot> </div> </div> </div> `}_dismissClicked(){(0,l.r)(this,"alert-dismissed-clicked")}constructor(...e){super(...e),this.title="",this.alertType="info",this.dismissable=!1,this.narrow=!1}}g.styles=r.AH`.issue-type{position:relative;padding:8px;display:flex}.icon{height:var(--ha-alert-icon-size,24px);width:var(--ha-alert-icon-size,24px)}.issue-type::after{position:absolute;top:0;right:0;bottom:0;left:0;opacity:.12;pointer-events:none;content:"";border-radius:var(--ha-border-radius-sm)}.icon.no-title{align-self:center}.content{display:flex;justify-content:space-between;align-items:center;width:100%;text-align:var(--float-start)}.content.narrow{flex-direction:column;align-items:flex-end}.action{z-index:1;width:min-content;--mdc-theme-primary:var(--primary-text-color)}.main-content{overflow-wrap:anywhere;word-break:break-word;line-height:normal;margin-left:8px;margin-right:0;margin-inline-start:8px;margin-inline-end:8px}.title{margin-top:2px;font-weight:var(--ha-font-weight-bold)}.action ha-icon-button{--mdc-theme-primary:var(--primary-text-color);--ha-icon-button-size:36px}.issue-type.info>.icon{color:var(--info-color)}.issue-type.info::after{background-color:var(--info-color)}.issue-type.warning>.icon{color:var(--warning-color)}.issue-type.warning::after{background-color:var(--warning-color)}.issue-type.error>.icon{color:var(--error-color)}.issue-type.error::after{background-color:var(--error-color)}.issue-type.success>.icon{color:var(--success-color)}.issue-type.success::after{background-color:var(--success-color)}:host ::slotted(ul){margin:0;padding-inline-start:20px}`,(0,o.Cg)([(0,n.MZ)()],g.prototype,"title",void 0),(0,o.Cg)([(0,n.MZ)({attribute:"alert-type"})],g.prototype,"alertType",void 0),(0,o.Cg)([(0,n.MZ)({type:Boolean})],g.prototype,"dismissable",void 0),(0,o.Cg)([(0,n.MZ)({type:Boolean})],g.prototype,"narrow",void 0),g=(0,o.Cg)([(0,n.EM)("ha-alert")],g),i()}catch(e){i(e)}})},76538(e,t,a){var i=a(62826),o=a(96196),r=a(97735);class n extends o.WF{render(){const e=o.qy`<div class="header-title"> <slot name="title"></slot> </div>`,t=o.qy`<div class="header-subtitle"> <slot name="subtitle"></slot> </div>`;return o.qy` <header class="header"> <div class="header-bar"> <section class="header-navigation-icon"> <slot name="navigationIcon"></slot> </section> <section class="header-content"> ${"above"===this.subtitlePosition?o.qy`${t}${e}`:o.qy`${e}${t}`} </section> <section class="header-action-items"> <slot name="actionItems"></slot> </section> </div> <slot></slot> </header> `}static get styles(){return[o.AH`:host{display:block}:host([show-border]){border-bottom:1px solid var(--mdc-dialog-scroll-divider-color,rgba(0,0,0,.12))}.header-bar{display:flex;flex-direction:row;align-items:center;padding:0 var(--ha-space-1);box-sizing:border-box}.header-content{flex:1;padding:10px var(--ha-space-1);display:flex;flex-direction:column;justify-content:center;min-height:var(--ha-space-12);min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.header-title{height:var(--ha-dialog-header-title-height,calc(var(--ha-font-size-xl) + var(--ha-space-1)));font-size:var(--ha-font-size-xl);line-height:var(--ha-line-height-condensed);font-weight:var(--ha-font-weight-medium);color:var(--ha-dialog-header-title-color,var(--primary-text-color))}.header-subtitle{font-size:var(--ha-font-size-m);line-height:var(--ha-line-height-normal);color:var(--ha-dialog-header-subtitle-color,var(--secondary-text-color))}@media all and (min-width:450px) and (min-height:500px){.header-bar{padding:0 var(--ha-space-2)}}.header-navigation-icon{flex:none;min-width:var(--ha-space-2);height:100%;display:flex;flex-direction:row}.header-action-items{flex:none;min-width:var(--ha-space-2);height:100%;display:flex;flex-direction:row}`]}constructor(...e){super(...e),this.subtitlePosition="below",this.showBorder=!1}}(0,i.Cg)([(0,r.MZ)({type:String,attribute:"subtitle-position"})],n.prototype,"subtitlePosition",void 0),(0,i.Cg)([(0,r.MZ)({type:Boolean,reflect:!0,attribute:"show-border"})],n.prototype,"showBorder",void 0),n=(0,i.Cg)([(0,r.EM)("ha-dialog-header")],n)},72554(e,t,a){a.a(e,async function(e,t){try{var i=a(62826),o=a(93900),r=a(96196),n=a(97735),s=a(32288),l=a(1087),d=a(64481),h=a(59992),c=a(14503),p=a(22348),g=(a(76538),a(26300)),v=e([o,g]);[o,g]=v.then?(await v)():v;const m="M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z";class u extends((0,h.V)(r.WF)){connectedCallback(){super.connectedCallback(),this.addEventListener("dialog-set-fullscreen",this._handleFullscreenChanged)}get scrollableElement(){return this.bodyContainer}updated(e){super.updated(e),e.has("open")&&(this._open=this.open)}render(){return r.qy` <wa-dialog .open="${this._open}" .lightDismiss="${!this.preventScrimClose}" without-header aria-labelledby="${(0,s.J)(this.ariaLabelledBy||(void 0!==this.headerTitle?"ha-dialog-title":void 0))}" aria-describedby="${(0,s.J)(this.ariaDescribedBy)}" @keydown="${this._handleKeyDown}" @wa-hide="${this._handleHide}" @wa-show="${this._handleShow}" @wa-after-show="${this._handleAfterShow}" @wa-after-hide="${this._handleAfterHide}"> ${this.withoutHeader?r.s6:r.qy` <slot name="header"> <ha-dialog-header .subtitlePosition="${this.headerSubtitlePosition}" .showBorder="${this._bodyScrolled}"> <slot name="headerNavigationIcon" slot="navigationIcon"> <ha-icon-button data-dialog="close" .label="${this.hass?.localize("ui.common.close")??"Close"}" .path="${m}"></ha-icon-button> </slot> ${void 0!==this.headerTitle?r.qy`<span slot="title" class="title" id="ha-dialog-title"> ${this.headerTitle} </span>`:r.qy`<slot name="headerTitle" slot="title"></slot>`} ${void 0!==this.headerSubtitle?r.qy`<span slot="subtitle">${this.headerSubtitle}</span>`:r.qy`<slot name="headerSubtitle" slot="subtitle"></slot>`} <slot name="headerActionItems" slot="actionItems"></slot> </ha-dialog-header> </slot>`} <div class="content-wrapper"> <div class="body ha-scrollbar" @scroll="${this._handleBodyScroll}"> <slot></slot> </div> ${this.renderScrollableFades()} </div> <slot name="footer" slot="footer"></slot> </wa-dialog> `}disconnectedCallback(){this.removeEventListener("dialog-set-fullscreen",this._handleFullscreenChanged),this._setFullscreen(!1),super.disconnectedCallback(),this._open=!1}_handleFullscreenChanged(e){this._open?(0,d.J)(()=>{this._setFullscreen(e.detail)}):this._setFullscreen(e.detail)}_setFullscreen(e){this.toggleAttribute("fullscreen",e)}_handleBodyScroll(e){this._bodyScrolled=e.target.scrollTop>0}_handleKeyDown(e){"Escape"===e.key&&(this._escapePressed=!0,this.preventScrimClose&&e.preventDefault(),e.stopPropagation(),e.currentTarget.open=!1)}_handleHide(e){const t=e.detail?.source===e.target.dialog;this.preventScrimClose&&this._escapePressed&&t&&e.preventDefault(),this._escapePressed=!1}static get styles(){return[...super.styles,c.dp,r.AH`
        wa-dialog {
          --full-width: var(
            --ha-dialog-width-full,
            min(95vw, var(--safe-width))
          );
          --width: min(var(--ha-dialog-width-md, 580px), var(--full-width));
          --spacing: var(--dialog-content-padding, var(--ha-space-6));
          --show-duration: var(--ha-dialog-show-duration, 200ms);
          --hide-duration: var(--ha-dialog-hide-duration, 200ms);
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

        :host([width="full"]) wa-dialog,
        :host([fullscreen]) wa-dialog {
          --width: var(--full-width);
        }

        :host([fullscreen]) wa-dialog::part(dialog) {
          min-height: var(--safe-height);
          max-height: var(--safe-height);
          margin-top: 0;
          transform: none;
        }

        :host([fullscreen]) .content-wrapper {
          overflow: hidden;
        }

        :host([fullscreen]) .body {
          overflow: hidden;
          padding: 0;
        }

        wa-dialog::part(dialog) {
          -webkit-backdrop-filter: var(
            --ha-dialog-surface-backdrop-filter,
            none
          );
          backdrop-filter: var(--ha-dialog-surface-backdrop-filter, none);
          box-shadow: var(--dialog-box-shadow, var(--wa-shadow-l));
          color: var(--primary-text-color);
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

        wa-dialog::part(dialog)::backdrop {
          -webkit-backdrop-filter: var(
            --ha-dialog-scrim-backdrop-filter,
            var(--dialog-backdrop-filter, none)
          );
          backdrop-filter: var(
            --ha-dialog-scrim-backdrop-filter,
            var(--dialog-backdrop-filter, none)
          );
          background-color: var(--mdc-dialog-scrim-color, none);
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
      `]}constructor(...e){super(...e),this.open=!1,this.type="standard",this.width="medium",this.preventScrimClose=!1,this.headerSubtitlePosition="below",this.flexContent=!1,this.withoutHeader=!1,this._open=!1,this._bodyScrolled=!1,this._escapePressed=!1,this._handleShow=async e=>{e.eventPhase===Event.AT_TARGET&&(this._open=!0,(0,l.r)(this,"opened"),await this.updateComplete,requestAnimationFrame(()=>{if(this.hass&&(0,p.V)(this.hass)){const e=this.querySelector("[autofocus]");return void(null!==e&&(e.id||(e.id="ha-dialog-autofocus"),this.hass?.auth.external?.fireMessage({type:"focus_element",payload:{element_id:e.id}})))}this.querySelector("[autofocus]")?.focus()}))},this._handleAfterShow=e=>{e.eventPhase===Event.AT_TARGET&&(0,l.r)(this,"after-show")},this._handleAfterHide=e=>{e.eventPhase===Event.AT_TARGET&&(this._open=!1,this._setFullscreen(!1),(0,l.r)(this,"closed"))}}}(0,i.Cg)([(0,n.MZ)({attribute:!1})],u.prototype,"hass",void 0),(0,i.Cg)([(0,n.MZ)({attribute:"aria-labelledby"})],u.prototype,"ariaLabelledBy",void 0),(0,i.Cg)([(0,n.MZ)({attribute:"aria-describedby"})],u.prototype,"ariaDescribedBy",void 0),(0,i.Cg)([(0,n.MZ)({type:Boolean,reflect:!0})],u.prototype,"open",void 0),(0,i.Cg)([(0,n.MZ)({reflect:!0})],u.prototype,"type",void 0),(0,i.Cg)([(0,n.MZ)({type:String,reflect:!0,attribute:"width"})],u.prototype,"width",void 0),(0,i.Cg)([(0,n.MZ)({type:Boolean,reflect:!0,attribute:"prevent-scrim-close"})],u.prototype,"preventScrimClose",void 0),(0,i.Cg)([(0,n.MZ)({attribute:"header-title"})],u.prototype,"headerTitle",void 0),(0,i.Cg)([(0,n.MZ)({attribute:"header-subtitle"})],u.prototype,"headerSubtitle",void 0),(0,i.Cg)([(0,n.MZ)({type:String,attribute:"header-subtitle-position"})],u.prototype,"headerSubtitlePosition",void 0),(0,i.Cg)([(0,n.MZ)({type:Boolean,reflect:!0,attribute:"flexcontent"})],u.prototype,"flexContent",void 0),(0,i.Cg)([(0,n.MZ)({type:Boolean,attribute:"without-header"})],u.prototype,"withoutHeader",void 0),(0,i.Cg)([(0,n.wk)()],u.prototype,"_open",void 0),(0,i.Cg)([(0,n.P)(".body")],u.prototype,"bodyContainer",void 0),(0,i.Cg)([(0,n.wk)()],u.prototype,"_bodyScrolled",void 0),(0,i.Cg)([(0,n.Ls)({passive:!0})],u.prototype,"_handleBodyScroll",null),u=(0,i.Cg)([(0,n.EM)("ha-dialog")],u),t()}catch(e){t(e)}})},70947(e,t,a){var i=a(62826),o=a(90075),r=(a(43776),a(96196)),n=a(97735);a(67094);class s extends o.A{renderCheckboxIcon(){return r.qy` <ha-svg-icon id="check" part="checkmark" .path="${this.checked?"M10,17L5,12L6.41,10.58L10,14.17L17.59,6.58L19,8M19,3H5C3.89,3 3,3.89 3,5V19A2,2 0 0,0 5,21H19A2,2 0 0,0 21,19V5C21,3.89 20.1,3 19,3Z":"M19,3H5C3.89,3 3,3.89 3,5V19A2,2 0 0,0 5,21H19A2,2 0 0,0 21,19V5C21,3.89 20.1,3 19,3M19,5V19H5V5H19Z"}"></ha-svg-icon> `}static get styles(){return[o.A.styles,r.AH`:host{min-height:var(--ha-space-10)}#check{visibility:visible;flex-shrink:0}#icon ::slotted(*){color:var(--ha-color-on-neutral-normal)}:host([variant=danger]) #icon ::slotted(*){color:var(--ha-color-on-danger-quiet)}:host([selected]){font-weight:var(--ha-font-weight-medium);color:var(--primary-color);background-color:var(--ha-color-fill-primary-quiet-resting);--icon-primary-color:var(--primary-color)}:host([selected]:hover){background-color:var(--ha-color-fill-primary-quiet-hover)}`]}constructor(...e){super(...e),this.selected=!1}}(0,i.Cg)([(0,n.MZ)({type:Boolean,reflect:!0})],s.prototype,"selected",void 0),s=(0,i.Cg)([(0,n.EM)("ha-dropdown-item")],s)},29823(e,t,a){a.a(e,async function(e,t){try{var i=a(62826),o=a(52254),r=a(96196),n=a(97735),s=e([o]);o=(s.then?(await s)():s)[0];class l extends o.A{get anchorElement(){return this.popup?.anchor}set anchorElement(e){this.popup&&(this.popup.anchor&&"ha-icon-button"===this.popup.anchor.localName&&(this.popup.anchor.selected=!1),this.popup.anchor=e)}getTrigger(){return this.anchorElement?this.anchorElement:super.getTrigger()}async showMenu(){await super.showMenu();const e=this.getTrigger();e&&"ha-icon-button"===e.localName&&(e.selected=!0)}async hideMenu(){const e=this.getTrigger();e&&"ha-icon-button"===e.localName&&(e.selected=!1),await super.hideMenu()}static get styles(){return[o.A.styles,r.AH`:host{font-size:var(--ha-dropdown-font-size, var(--ha-font-size-m));--wa-color-surface-raised:var(
            --card-background-color,
            var(--ha-dialog-surface-background, var(--mdc-theme-surface, #fff)),
          )}#menu{padding:var(--ha-space-1)}`]}constructor(...e){super(...e),this.dropdownTag="ha-dropdown",this.dropdownItemTag="ha-dropdown-item"}}(0,i.Cg)([(0,n.MZ)({attribute:!1})],l.prototype,"dropdownTag",void 0),(0,i.Cg)([(0,n.MZ)({attribute:!1})],l.prototype,"dropdownItemTag",void 0),l=(0,i.Cg)([(0,n.EM)("ha-dropdown")],l),t()}catch(e){t(e)}})},26300(e,t,a){a.a(e,async function(e,i){try{a.r(t),a.d(t,{HaIconButton:()=>h});var o=a(62826),r=a(96196),n=a(97735),s=a(32288),l=a(18350),d=(a(67094),e([l]));l=(d.then?(await d)():d)[0];class h extends r.WF{render(){return r.qy` <ha-button appearance="plain" variant="neutral" aria-label="${(0,s.J)(this.label)}" title="${(0,s.J)(this.hideTitle?void 0:this.label)}" aria-haspopup="${(0,s.J)(this.ariaHasPopup)}" .disabled="${this.disabled}" .iconTag="${this.path?"ha-svg-icon":"span"}" .href="${this.href}" .target="${this.target}" .rel="${this.rel}" .download="${this.download}"> ${this.path?r.qy`<ha-svg-icon .path="${this.path}"></ha-svg-icon>`:r.qy`<span><slot></slot></span>`} </ha-button> `}constructor(...e){super(...e),this.disabled=!1,this.hideTitle=!1,this.selected=!1}}h.shadowRootOptions={mode:"open",delegatesFocus:!0},h.styles=r.AH`:host{display:inline-block;outline:0;--ha-button-height:var(--ha-icon-button-size, 48px)}ha-button{position:relative;isolation:isolate;--wa-form-control-padding-inline:var(
        --ha-icon-button-padding-inline,
        --ha-space-2
      );--wa-color-on-normal:currentColor;--wa-color-fill-quiet:transparent;--ha-button-label-overflow:visible}ha-button::after{content:"";position:absolute;inset:0;z-index:-1;border-radius:50%;background-color:currentColor;opacity:0;pointer-events:none}ha-button::part(base){width:var(--wa-form-control-height);aspect-ratio:1;outline-offset:-4px}ha-button::part(label){display:flex}:host([selected]) ha-button::after{opacity:.1}@media (hover:hover){:host(:hover:not([disabled])) ha-button::after{opacity:.1}}`,(0,o.Cg)([(0,n.MZ)({type:Boolean,reflect:!0})],h.prototype,"disabled",void 0),(0,o.Cg)([(0,n.MZ)({type:String})],h.prototype,"path",void 0),(0,o.Cg)([(0,n.MZ)({type:String})],h.prototype,"label",void 0),(0,o.Cg)([(0,n.MZ)({type:String,attribute:"aria-haspopup"})],h.prototype,"ariaHasPopup",void 0),(0,o.Cg)([(0,n.MZ)({attribute:"hide-title",type:Boolean})],h.prototype,"hideTitle",void 0),(0,o.Cg)([(0,n.MZ)({type:Boolean,reflect:!0})],h.prototype,"selected",void 0),(0,o.Cg)([(0,n.MZ)()],h.prototype,"href",void 0),(0,o.Cg)([(0,n.MZ)()],h.prototype,"target",void 0),(0,o.Cg)([(0,n.MZ)()],h.prototype,"rel",void 0),(0,o.Cg)([(0,n.MZ)()],h.prototype,"download",void 0),h=(0,o.Cg)([(0,n.EM)("ha-icon-button")],h),i()}catch(e){i(e)}})},43661(e,t,a){a.r(t),a.d(t,{HaIconNext:()=>s});var i=a(62826),o=a(97735),r=a(63091),n=a(67094);class s extends n.HaSvgIcon{constructor(...e){super(...e),this.path="rtl"===r.G.document.dir?"M15.41,16.58L10.83,12L15.41,7.41L14,6L8,12L14,18L15.41,16.58Z":"M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z"}}(0,i.Cg)([(0,o.MZ)()],s.prototype,"path",void 0),s=(0,i.Cg)([(0,o.EM)("ha-icon-next")],s)},69709(e,t,a){a(18111),a(22489),a(61701),a(18237);var i=a(62826),o=a(96196),r=a(97735),n=a(1420),s=a(30015),l=a.n(s),d=a(1087),h=(a(14603),a(47566),a(98721),a(2209));let c;var p=a(996);const g=e=>o.qy`${e}`,v=new p.G(1e3),m={reType:/(?<input>(\[!(?<type>caution|important|note|tip|warning)\])(?:\s|\\n)?)/i,typeToHaAlert:{caution:"error",important:"info",note:"info",tip:"success",warning:"warning"}};class u extends o.mN{disconnectedCallback(){if(super.disconnectedCallback(),this.cache){const e=this._computeCacheKey();v.set(e,this.innerHTML)}}createRenderRoot(){return this}update(e){super.update(e),void 0!==this.content&&(this._renderPromise=this._render())}async getUpdateComplete(){return await super.getUpdateComplete(),await this._renderPromise,!0}willUpdate(e){if(!this.innerHTML&&this.cache){const e=this._computeCacheKey();v.has(e)&&((0,o.XX)(g((0,n._)(v.get(e))),this.renderRoot),this._resize())}}_computeCacheKey(){return l()({content:this.content,allowSvg:this.allowSvg,allowDataUrl:this.allowDataUrl,breaks:this.breaks})}async _render(){const e=await(async(e,t,i)=>(c||(c=(0,h.LV)(new Worker(new URL(a.p+a.u("55640"),a.b)))),c.renderMarkdown(e,t,i)))(String(this.content),{breaks:this.breaks,gfm:!0},{allowSvg:this.allowSvg,allowDataUrl:this.allowDataUrl});(0,o.XX)(g((0,n._)(e.join(""))),this.renderRoot),this._resize();const t=document.createTreeWalker(this,NodeFilter.SHOW_ELEMENT,null);for(;t.nextNode();){const e=t.currentNode;if(e instanceof HTMLAnchorElement&&e.host!==document.location.host)e.target="_blank",e.rel="noreferrer noopener";else if(e instanceof HTMLImageElement)this.lazyImages&&(e.loading="lazy"),e.addEventListener("load",this._resize);else if(e instanceof HTMLQuoteElement){const a=e.firstElementChild?.firstChild?.textContent&&m.reType.exec(e.firstElementChild.firstChild.textContent);if(a){const{type:i}=a.groups,o=document.createElement("ha-alert");o.alertType=m.typeToHaAlert[i.toLowerCase()],o.append(...Array.from(e.childNodes).map(e=>{const t=Array.from(e.childNodes);if(!this.breaks&&t.length){const e=t[0];e.nodeType===Node.TEXT_NODE&&e.textContent===a.input&&e.textContent?.includes("\n")&&(e.textContent=e.textContent.split("\n").slice(1).join("\n"))}return t}).reduce((e,t)=>e.concat(t),[]).filter(e=>e.textContent&&e.textContent!==a.input)),t.parentNode().replaceChild(o,e)}}else e instanceof HTMLElement&&["ha-alert","ha-qr-code","ha-icon","ha-svg-icon"].includes(e.localName)&&a(96175)(`./${e.localName}`)}}constructor(...e){super(...e),this.allowSvg=!1,this.allowDataUrl=!1,this.breaks=!1,this.lazyImages=!1,this.cache=!1,this._renderPromise=Promise.resolve(),this._resize=()=>(0,d.r)(this,"content-resize")}}(0,i.Cg)([(0,r.MZ)()],u.prototype,"content",void 0),(0,i.Cg)([(0,r.MZ)({attribute:"allow-svg",type:Boolean})],u.prototype,"allowSvg",void 0),(0,i.Cg)([(0,r.MZ)({attribute:"allow-data-url",type:Boolean})],u.prototype,"allowDataUrl",void 0),(0,i.Cg)([(0,r.MZ)({type:Boolean})],u.prototype,"breaks",void 0),(0,i.Cg)([(0,r.MZ)({type:Boolean,attribute:"lazy-images"})],u.prototype,"lazyImages",void 0),(0,i.Cg)([(0,r.MZ)({type:Boolean})],u.prototype,"cache",void 0),u=(0,i.Cg)([(0,r.EM)("ha-markdown-element")],u)},3587(e,t,a){var i=a(62826),o=a(96196),r=a(97735);a(69709);class n extends o.WF{async getUpdateComplete(){const e=await super.getUpdateComplete();return await(this._markdownElement?.updateComplete),e}render(){return this.content?o.qy`<ha-markdown-element .content="${this.content}" .allowSvg="${this.allowSvg}" .allowDataUrl="${this.allowDataUrl}" .breaks="${this.breaks}" .lazyImages="${this.lazyImages}" .cache="${this.cache}"></ha-markdown-element>`:o.s6}constructor(...e){super(...e),this.allowSvg=!1,this.allowDataUrl=!1,this.breaks=!1,this.lazyImages=!1,this.cache=!1}}n.styles=o.AH`
    :host {
      display: block;
    }
    ha-markdown-element {
      -ms-user-select: text;
      -webkit-user-select: text;
      -moz-user-select: text;
    }
    ha-markdown-element > *:first-child {
      margin-top: 0;
    }
    ha-markdown-element > *:last-child {
      margin-bottom: 0;
    }
    ha-alert {
      display: block;
      margin: var(--ha-space-1) 0;
    }
    a {
      color: var(--markdown-link-color, var(--primary-color));
    }
    img {
      background-color: var(--markdown-image-background-color);
      border-radius: var(--markdown-image-border-radius);
      max-width: 100%;
    }
    p:first-child > img:first-child {
      vertical-align: top;
    }
    p:first-child > img:last-child {
      vertical-align: top;
    }
    ha-markdown-element > :is(ol, ul) {
      padding-inline-start: var(--markdown-list-indent, revert);
    }
    li {
      &:has(input[type="checkbox"]) {
        list-style: none;
        & > input[type="checkbox"] {
          margin-left: 0;
        }
      }
    }
    svg {
      background-color: var(--markdown-svg-background-color, none);
      color: var(--markdown-svg-color, none);
    }
    code,
    pre {
      background-color: var(--markdown-code-background-color, none);
      border-radius: var(--ha-border-radius-sm);
      color: var(--markdown-code-text-color, inherit);
    }
    code {
      font-size: var(--ha-font-size-s);
      padding: 0.2em 0.4em;
    }
    pre code {
      padding: 0;
    }
    pre {
      padding: var(--ha-space-4);
      overflow: auto;
      line-height: var(--ha-line-height-condensed);
      font-family: var(--ha-font-family-code);
    }
    h1,
    h2,
    h3,
    h4,
    h5,
    h6 {
      line-height: initial;
    }
    h2 {
      font-size: var(--ha-font-size-xl);
      font-weight: var(--ha-font-weight-bold);
    }
    hr {
      border-color: var(--divider-color);
      border-bottom: none;
      margin: var(--ha-space-4) 0;
    }
    table[role="presentation"] {
      --markdown-table-border-collapse: separate;
      --markdown-table-border-width: 0;
      --markdown-table-padding-inline: 0;
      --markdown-table-padding-block: 0;
      th,
      td {
        vertical-align: middle;
      }
    }
    table[role="presentation"] td[valign="top"],
    table[role="presentation"] th[valign="top"] {
      vertical-align: top;
    }
    table[role="presentation"] td[valign="middle"],
    table[role="presentation"] th[valign="middle"] {
      vertical-align: middle;
    }
    table[role="presentation"] td[valign="bottom"],
    table[role="presentation"] th[valign="bottom"] {
      vertical-align: bottom;
    }
    table[role="presentation"] td[valign="baseline"],
    table[role="presentation"] th[valign="baseline"] {
      vertical-align: baseline;
    }
    @supports (border-width: attr(border px, 0)) {
      table[role="presentation"] {
        --markdown-table-border-width: attr(border px, 0);
      }
      table[role="presentation"] th,
      table[role="presentation"] td {
        vertical-align: attr(valign, middle);
      }
    }
    table[role="presentation"][border="0"] {
      --markdown-table-border-width: 0;
    }
    table[role="presentation"][border="1"] {
      --markdown-table-border-width: 1px;
    }
    table[role="presentation"][border="2"] {
      --markdown-table-border-width: 2px;
    }
    table[role="presentation"][border="3"] {
      --markdown-table-border-width: 3px;
    }
    table {
      border-collapse: var(--markdown-table-border-collapse, collapse);
    }
    div:has(> table) {
      overflow: auto;
    }
    th {
      text-align: var(--markdown-table-text-align, start);
    }
    td,
    th {
      border-width: var(--markdown-table-border-width, 1px);
      border-style: var(--markdown-table-border-style, solid);
      border-color: var(--markdown-table-border-color, var(--divider-color));
      padding-inline: var(--markdown-table-padding-inline, 0.5em);
      padding-block: var(--markdown-table-padding-block, 0.25em);
    }
    blockquote {
      border-left: 4px solid var(--divider-color);
      margin-inline: 0;
      padding-inline: 1em;
    }
  `,(0,i.Cg)([(0,r.MZ)()],n.prototype,"content",void 0),(0,i.Cg)([(0,r.MZ)({attribute:"allow-svg",type:Boolean})],n.prototype,"allowSvg",void 0),(0,i.Cg)([(0,r.MZ)({attribute:"allow-data-url",type:Boolean})],n.prototype,"allowDataUrl",void 0),(0,i.Cg)([(0,r.MZ)({type:Boolean})],n.prototype,"breaks",void 0),(0,i.Cg)([(0,r.MZ)({type:Boolean,attribute:"lazy-images"})],n.prototype,"lazyImages",void 0),(0,i.Cg)([(0,r.MZ)({type:Boolean})],n.prototype,"cache",void 0),(0,i.Cg)([(0,r.P)("ha-markdown-element")],n.prototype,"_markdownElement",void 0),n=(0,i.Cg)([(0,r.EM)("ha-markdown")],n)},65829(e,t,a){a.a(e,async function(e,i){try{a.r(t),a.d(t,{HaSpinner:()=>d});var o=a(62826),r=a(55262),n=a(96196),s=a(97735),l=e([r]);r=(l.then?(await l)():l)[0];class d extends r.A{updated(e){if(super.updated(e),e.has("size"))switch(this.size){case"tiny":this.style.setProperty("--ha-spinner-size","16px");break;case"small":this.style.setProperty("--ha-spinner-size","28px");break;case"medium":this.style.setProperty("--ha-spinner-size","48px");break;case"large":this.style.setProperty("--ha-spinner-size","68px");break;case void 0:this.style.removeProperty("--ha-progress-ring-size")}}static get styles(){return[r.A.styles,n.AH`:host{--indicator-color:var(
            --ha-spinner-indicator-color,
            var(--primary-color)
          );--track-color:var(--ha-spinner-divider-color, var(--divider-color));--track-width:4px;--speed:3.5s;font-size:var(--ha-spinner-size, 48px)}`]}}(0,o.Cg)([(0,s.MZ)()],d.prototype,"size",void 0),d=(0,o.Cg)([(0,s.EM)("ha-spinner")],d),i()}catch(e){i(e)}})},67094(e,t,a){a.r(t),a.d(t,{HaSvgIcon:()=>n});var i=a(62826),o=a(96196),r=a(97735);class n extends o.WF{render(){return o.JW` <svg viewBox="${this.viewBox||"0 0 24 24"}" preserveAspectRatio="xMidYMid meet" focusable="false" role="img" aria-hidden="true"> <g> ${this.path?o.JW`<path class="primary-path" d="${this.path}"></path>`:o.s6} ${this.secondaryPath?o.JW`<path class="secondary-path" d="${this.secondaryPath}"></path>`:o.s6} </g> </svg>`}}n.styles=o.AH`:host{display:var(--ha-icon-display,inline-flex);align-items:center;justify-content:center;position:relative;vertical-align:middle;fill:var(--icon-primary-color,currentcolor);width:var(--mdc-icon-size,24px);height:var(--mdc-icon-size,24px)}svg{width:100%;height:100%;pointer-events:none;display:block}path.primary-path{opacity:var(--icon-primary-opactity, 1)}path.secondary-path{fill:var(--icon-secondary-color,currentcolor);opacity:var(--icon-secondary-opactity, .5)}`,(0,i.Cg)([(0,r.MZ)()],n.prototype,"path",void 0),(0,i.Cg)([(0,r.MZ)({attribute:!1})],n.prototype,"secondaryPath",void 0),(0,i.Cg)([(0,r.MZ)({attribute:!1})],n.prototype,"viewBox",void 0),n=(0,i.Cg)([(0,r.EM)("ha-svg-icon")],n)},75709(e,t,a){a.d(t,{h:()=>d});var i=a(62826),o=a(71714),r=a(92347),n=a(96196),s=a(97735),l=a(63091);class d extends o.J{updated(e){super.updated(e),(e.has("invalid")||e.has("errorMessage"))&&(this.setCustomValidity(this.invalid?this.errorMessage||this.validationMessage||"Invalid":""),(this.invalid||this.validateOnInitialRender||e.has("invalid")&&void 0!==e.get("invalid"))&&this.reportValidity()),e.has("autocomplete")&&(this.autocomplete?this.formElement.setAttribute("autocomplete",this.autocomplete):this.formElement.removeAttribute("autocomplete")),e.has("autocorrect")&&(!1===this.autocorrect?this.formElement.setAttribute("autocorrect","off"):this.formElement.removeAttribute("autocorrect")),e.has("inputSpellcheck")&&(this.inputSpellcheck?this.formElement.setAttribute("spellcheck",this.inputSpellcheck):this.formElement.removeAttribute("spellcheck"))}renderIcon(e,t=!1){const a=t?"trailing":"leading";return n.qy` <span class="mdc-text-field__icon mdc-text-field__icon--${a}" tabindex="${t?1:-1}"> <slot name="${a}Icon"></slot> </span> `}constructor(...e){super(...e),this.icon=!1,this.iconTrailing=!1,this.autocorrect=!0}}d.styles=[r.R,n.AH`.mdc-text-field__input{width:var(--ha-textfield-input-width,100%)}.mdc-text-field:not(.mdc-text-field--with-leading-icon){padding:var(--text-field-padding,0px 16px)}.mdc-text-field__affix--suffix{padding-left:var(--text-field-suffix-padding-left,12px);padding-right:var(--text-field-suffix-padding-right,0px);padding-inline-start:var(--text-field-suffix-padding-left,12px);padding-inline-end:var(--text-field-suffix-padding-right,0px);direction:ltr}.mdc-text-field--with-leading-icon{padding-inline-start:var(--text-field-suffix-padding-left,0px);padding-inline-end:var(--text-field-suffix-padding-right,16px);direction:var(--direction)}.mdc-text-field--with-leading-icon.mdc-text-field--with-trailing-icon{padding-left:var(--text-field-suffix-padding-left,0px);padding-right:var(--text-field-suffix-padding-right,0px);padding-inline-start:var(--text-field-suffix-padding-left,0px);padding-inline-end:var(--text-field-suffix-padding-right,0px)}.mdc-text-field:not(.mdc-text-field--disabled) .mdc-text-field__affix--suffix{color:var(--secondary-text-color)}.mdc-text-field:not(.mdc-text-field--disabled) .mdc-text-field__icon{color:var(--secondary-text-color)}.mdc-text-field__icon--leading{margin-inline-start:16px;margin-inline-end:8px;direction:var(--direction)}.mdc-text-field__icon--trailing{padding:var(--textfield-icon-trailing-padding,12px)}.mdc-floating-label:not(.mdc-floating-label--float-above){max-width:calc(100% - 16px)}.mdc-floating-label--float-above{max-width:calc((100% - 16px)/ .75);transition:none}input{text-align:var(--text-field-text-align,start)}input[type=color]{height:20px}::-ms-reveal{display:none}:host([no-spinner]) input::-webkit-inner-spin-button,:host([no-spinner]) input::-webkit-outer-spin-button{-webkit-appearance:none;margin:0}input[type=color]::-webkit-color-swatch-wrapper{padding:0}:host([no-spinner]) input[type=number]{-moz-appearance:textfield}.mdc-text-field__ripple{overflow:hidden}.mdc-text-field{overflow:var(--text-field-overflow)}.mdc-floating-label{padding-inline-end:16px;padding-inline-start:initial;inset-inline-start:16px!important;inset-inline-end:initial!important;transform-origin:var(--float-start);direction:var(--direction);text-align:var(--float-start);box-sizing:border-box;text-overflow:ellipsis}.mdc-text-field--with-leading-icon.mdc-text-field--filled .mdc-floating-label{max-width:calc(100% - 48px - var(--text-field-suffix-padding-left,0px));inset-inline-start:calc(48px + var(--text-field-suffix-padding-left,0px))!important;inset-inline-end:initial!important;direction:var(--direction)}.mdc-text-field__input[type=number]{direction:var(--direction)}.mdc-text-field__affix--prefix{padding-right:var(--text-field-prefix-padding-right,2px);padding-inline-end:var(--text-field-prefix-padding-right,2px);padding-inline-start:initial}.mdc-text-field:not(.mdc-text-field--disabled) .mdc-text-field__affix--prefix{color:var(--mdc-text-field-label-ink-color)}#helper-text ha-markdown{display:inline-block}`,"rtl"===l.G.document.dir?n.AH`.mdc-floating-label,.mdc-text-field--with-leading-icon,.mdc-text-field--with-leading-icon.mdc-text-field--filled .mdc-floating-label,.mdc-text-field__icon--leading,.mdc-text-field__input[type=number]{direction:rtl;--direction:rtl}`:n.AH``],(0,i.Cg)([(0,s.MZ)({type:Boolean})],d.prototype,"invalid",void 0),(0,i.Cg)([(0,s.MZ)({attribute:"error-message"})],d.prototype,"errorMessage",void 0),(0,i.Cg)([(0,s.MZ)({type:Boolean})],d.prototype,"icon",void 0),(0,i.Cg)([(0,s.MZ)({type:Boolean})],d.prototype,"iconTrailing",void 0),(0,i.Cg)([(0,s.MZ)()],d.prototype,"autocomplete",void 0),(0,i.Cg)([(0,s.MZ)({type:Boolean})],d.prototype,"autocorrect",void 0),(0,i.Cg)([(0,s.MZ)({attribute:"input-spellcheck"})],d.prototype,"inputSpellcheck",void 0),(0,i.Cg)([(0,s.P)("input")],d.prototype,"formElement",void 0),d=(0,i.Cg)([(0,s.EM)("ha-textfield")],d)},69150(e,t,a){a.d(t,{$$:()=>m,AH:()=>o,NH:()=>p,QC:()=>i,Uc:()=>n,Zr:()=>g,ds:()=>v,hJ:()=>s,mp:()=>d,nx:()=>l,u6:()=>h,vU:()=>r,zn:()=>c});const i=(e,t,a)=>"run-start"===t.type?e={init_options:a,stage:"ready",run:t.data,events:[t],started:new Date(t.timestamp)}:e?((e="wake_word-start"===t.type?{...e,stage:"wake_word",wake_word:{...t.data,done:!1}}:"wake_word-end"===t.type?{...e,wake_word:{...e.wake_word,...t.data,done:!0}}:"stt-start"===t.type?{...e,stage:"stt",stt:{...t.data,done:!1}}:"stt-end"===t.type?{...e,stt:{...e.stt,...t.data,done:!0}}:"intent-start"===t.type?{...e,stage:"intent",intent:{...t.data,done:!1}}:"intent-end"===t.type?{...e,intent:{...e.intent,...t.data,done:!0}}:"tts-start"===t.type?{...e,stage:"tts",tts:{...t.data,done:!1}}:"tts-end"===t.type?{...e,tts:{...e.tts,...t.data,done:!0}}:"run-end"===t.type?{...e,finished:new Date(t.timestamp),stage:"done"}:"error"===t.type?{...e,finished:new Date(t.timestamp),stage:"error",error:t.data}:{...e}).events=[...e.events,t],e):void console.warn("Received unexpected event before receiving session",t),o=(e,t,a)=>{let o;const n=r(e,e=>{o=i(o,e,a),"run-end"!==e.type&&"error"!==e.type||n.then(e=>e()),o&&t(o)},a);return n},r=(e,t,a)=>e.connection.subscribeMessage(t,{...a,type:"assist_pipeline/run"}),n=(e,t)=>e.callWS({type:"assist_pipeline/pipeline_debug/list",pipeline_id:t}),s=(e,t,a)=>e.callWS({type:"assist_pipeline/pipeline_debug/get",pipeline_id:t,pipeline_run_id:a}),l=e=>e.callWS({type:"assist_pipeline/pipeline/list"}),d=(e,t)=>e.callWS({type:"assist_pipeline/pipeline/get",pipeline_id:t}),h=(e,t)=>e.callWS({type:"assist_pipeline/pipeline/create",...t}),c=(e,t,a)=>e.callWS({type:"assist_pipeline/pipeline/update",pipeline_id:t,...a}),p=(e,t)=>e.callWS({type:"assist_pipeline/pipeline/set_preferred",pipeline_id:t}),g=(e,t)=>e.callWS({type:"assist_pipeline/pipeline/delete",pipeline_id:t}),v=e=>e.callWS({type:"assist_pipeline/language/list"}),m=e=>e.callWS({type:"assist_pipeline/device/list"})},24524(e,t,a){a.a(e,async function(e,i){try{a.r(t),a.d(t,{HaVoiceCommandDialog:()=>M});a(18111),a(61701);var o=a(62826),r=(a(71786),a(96196)),n=a(97735),s=a(93905),l=a(1087),d=a(57237),h=a(38962),c=a(85404),p=a(18350),g=a(72554),v=(a(76538),a(29823)),m=(a(70947),a(26300)),u=(a(43661),a(65829)),f=a(69150),b=a(14503),y=a(36918),w=e([h,c,p,g,v,m,u]);[h,c,p,g,v,m,u]=w.then?(await w)():w;const x="M7.41,8.58L12,13.17L16.59,8.58L18,10L12,16L6,10L7.41,8.58Z",_="M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z",k="M11,18H13V16H11V18M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M12,20C7.59,20 4,16.41 4,12C4,7.59 7.59,4 12,4C16.41,4 20,7.59 20,12C20,16.41 16.41,20 12,20M12,6A4,4 0 0,0 8,10H10A2,2 0 0,1 12,8A2,2 0 0,1 14,10C14,12 11,11.75 11,15H13C13,12.75 16,12.5 16,10A4,4 0 0,0 12,6Z",C="M12,17.27L18.18,21L16.54,13.97L22,9.24L14.81,8.62L12,2L9.19,8.62L2,9.24L7.45,13.97L5.82,21L12,17.27Z";class M extends r.WF{async showDialog(e){await this._loadPipelines();const t=this._pipelines?.map(e=>e.id)||[];"preferred"===e.pipeline_id||"last_used"===e.pipeline_id&&!this._pipelineId?this._pipelineId=this._preferredPipeline:["last_used","preferred"].includes(e.pipeline_id)||(this._pipelineId=e.pipeline_id),this._pipelineId&&!t.includes(this._pipelineId)&&(this._pipelineId=this._preferredPipeline),this._startListening=e.start_listening,this._dialogOpen=!0,this._open=!0}closeDialog(){this._open=!1}_dialogClosed(){this._dialogOpen=!1,this._pipelines=void 0,(0,l.r)(this,"dialog-closed",{dialog:this.localName})}render(){return this._dialogOpen?r.qy` <ha-dialog .hass="${this.hass}" .open="${this._open}" @closed="${this._dialogClosed}" flexcontent> <ha-dialog-header slot="header"> <ha-icon-button slot="navigationIcon" data-dialog="close" .label="${this.hass.localize("ui.common.close")}" .path="${_}"></ha-icon-button> <div slot="title"> ${this.hass.localize("ui.dialogs.voice_command.title")} <ha-dropdown @opened="${this._loadPipelines}" @closed="${d.d}" @wa-select="${this._selectPipeline}"> <ha-button slot="trigger" appearance="plain" variant="neutral" size="small" .loading="${!this._pipelines}"> ${this._pipeline?.name} <ha-svg-icon slot="end" .path="${x}"></ha-svg-icon> </ha-button> ${this._pipelines?this._pipelines?.map(e=>r.qy`<ha-dropdown-item ?selected="${e.id===this._pipelineId||!this._pipelineId&&e.id===this._preferredPipeline}" .value="${e.id}"> ${e.name}${e.id===this._preferredPipeline?r.qy` <ha-svg-icon slot="details" .path="${C}"></ha-svg-icon> `:r.s6} </ha-dropdown-item>`):r.s6} ${this.hass.user?.is_admin?r.qy`<wa-divider></wa-divider> <a href="/config/voice-assistants/assistants"><ha-dropdown-item>${this.hass.localize("ui.dialogs.voice_command.manage_assistants")} <ha-icon-next slot="details"></ha-icon-next></ha-dropdown-item></a>`:r.s6} </ha-dropdown> </div> <ha-icon-button .label="${this.hass.localize("ui.common.help")}" .path="${k}" href="${(0,y.o)(this.hass,"/docs/assist/")}" slot="actionItems" target="_blank" rel="noopener noreferrer"></ha-icon-button> </ha-dialog-header> ${this._errorLoadAssist?r.qy`<ha-alert alert-type="error"> ${this.hass.localize(`ui.dialogs.voice_command.${this._errorLoadAssist}_error_load_assist`)} </ha-alert>`:this._pipeline?r.qy` <ha-assist-chat .hass="${this.hass}" .pipeline="${this._pipeline}" .startListening="${this._startListening}"> </ha-assist-chat> `:r.qy`<div class="pipelines-loading"> <ha-spinner size="large"></ha-spinner> </div>`} </ha-dialog> `:r.s6}willUpdate(e){(e.has("_pipelineId")||e.has("_open")&&!0===this._open&&this._pipelineId)&&this._getPipeline()}async _loadPipelines(){if(this._pipelines)return;const{pipelines:e,preferred_pipeline:t}=await(0,f.nx)(this.hass);this._pipelines=e,this._preferredPipeline=t||void 0}async _selectPipeline(e){const t=e.detail?.item?.value;t&&(this._pipelineId=t,await this.updateComplete)}async _getPipeline(){this._pipeline=void 0,this._errorLoadAssist=void 0;const e=this._pipelineId;try{const t=await(0,f.mp)(this.hass,e);e===this._pipelineId&&(this._pipeline=t)}catch(t){if(e!==this._pipelineId)return;"not_found"===t.code?this._errorLoadAssist="not_found":(this._errorLoadAssist="unknown",console.error(t))}}static get styles(){return[b.nA,r.AH`ha-dialog{--dialog-content-padding:0}ha-dialog-header a{color:var(--primary-text-color)}div[slot=title]{display:flex;flex-direction:column;margin:-4px 0}ha-dropdown{display:flex;--mdc-theme-on-primary:var(--text-primary-color);--mdc-theme-primary:var(--primary-color);margin-top:-4px;margin-bottom:0;margin-right:0;margin-inline-end:0;margin-left:-9px;margin-inline-start:-9px}ha-dropdown ha-button{--ha-button-height:var(--ha-space-5)}ha-dropdown ha-button::part(base){margin-left:5px;padding:0}@media (prefers-color-scheme:dark){ha-dropdown ha-button{--ha-button-theme-lighter-color:rgba(255, 255, 255, 0.1)}}ha-dropdown ha-button ha-svg-icon{height:var(--ha-space-7);margin-left:var(--ha-space-1);margin-inline-start:var(--ha-space-1);margin-inline-end:initial;direction:var(--direction)}ha-dropdown-item ha-svg-icon{margin-left:var(--ha-space-1);margin-inline-start:var(--ha-space-1);margin-inline-end:initial;direction:var(--direction);display:block}ha-dropdown a{text-decoration:none}.pipelines-loading{display:flex;justify-content:center}`]}constructor(...e){super(...e),this._open=!1,this._dialogOpen=!1,this._startListening=!1}}(0,o.Cg)([(0,n.MZ)({attribute:!1})],M.prototype,"hass",void 0),(0,o.Cg)([(0,n.wk)()],M.prototype,"_open",void 0),(0,o.Cg)([(0,n.wk)()],M.prototype,"_dialogOpen",void 0),(0,o.Cg)([(0,n.wk)(),(0,s.I)({key:"AssistPipelineId",state:!0,subscribe:!1})],M.prototype,"_pipelineId",void 0),(0,o.Cg)([(0,n.wk)()],M.prototype,"_pipeline",void 0),(0,o.Cg)([(0,n.wk)()],M.prototype,"_pipelines",void 0),(0,o.Cg)([(0,n.wk)()],M.prototype,"_preferredPipeline",void 0),(0,o.Cg)([(0,n.wk)()],M.prototype,"_errorLoadAssist",void 0),M=(0,o.Cg)([(0,n.EM)("ha-voice-command-dialog")],M),i()}catch(e){i(e)}})},59992(e,t,a){a.d(t,{V:()=>l});var i=a(62826),o=a(88696),r=a(96196),n=a(94333),s=a(97735);const l=e=>{class t extends e{get scrollableElement(){return t.DEFAULT_SCROLLABLE_ELEMENT}firstUpdated(e){super.firstUpdated?.(e),this.scrollableElement&&this._updateScrollableState(this.scrollableElement),this._attachScrollableElement()}updated(e){super.updated?.(e),this._attachScrollableElement()}disconnectedCallback(){this._detachScrollableElement(),this._contentScrolled=!1,this._contentScrollable=!1,super.disconnectedCallback()}renderScrollableFades(e=!1){return r.qy` <div class="${(0,n.H)({"fade-top":!0,rounded:e,visible:this._contentScrolled})}"></div> <div class="${(0,n.H)({"fade-bottom":!0,rounded:e,visible:this._contentScrollable})}"></div> `}static get styles(){const e=Object.getPrototypeOf(this);var t;return[...void 0===(t=e?.styles??[])?[]:Array.isArray(t)?t:[t],r.AH`.fade-bottom,.fade-top{position:absolute;left:0;right:0;height:var(--ha-space-2);pointer-events:none;transition:opacity 180ms ease-in-out;border-radius:var(--ha-border-radius-square);opacity:0;background:linear-gradient(to bottom,var(--ha-color-shadow-scrollable-fade),transparent)}.fade-top{top:0}.fade-bottom{bottom:0;transform:rotate(180deg)}.fade-bottom.visible,.fade-top.visible{opacity:1}.fade-bottom.rounded,.fade-top.rounded{border-radius:var(--ha-card-border-radius,var(--ha-border-radius-lg));border-bottom-left-radius:var(--ha-border-radius-square);border-bottom-right-radius:var(--ha-border-radius-square)}.fade-top.rounded{border-top-left-radius:var(--ha-border-radius-square);border-top-right-radius:var(--ha-border-radius-square)}.fade-bottom.rounded{border-bottom-left-radius:var(--ha-border-radius-square);border-bottom-right-radius:var(--ha-border-radius-square)}`]}_attachScrollableElement(){const e=this.scrollableElement;e!==this._scrollTarget&&(this._detachScrollableElement(),e&&(this._scrollTarget=e,e.addEventListener("scroll",this._onScroll,{passive:!0}),this._resize.observe(e),this._updateScrollableState(e)))}_detachScrollableElement(){this._scrollTarget&&(this._scrollTarget.removeEventListener("scroll",this._onScroll),this._resize.unobserve?.(this._scrollTarget),this._scrollTarget=void 0)}_updateScrollableState(e){const t=parseFloat(getComputedStyle(e).getPropertyValue("--safe-area-inset-bottom"))||0,{scrollHeight:a=0,clientHeight:i=0,scrollTop:o=0}=e;this._contentScrollable=a-i>o+t+this.scrollFadeSafeAreaPadding}constructor(...e){super(...e),this._contentScrolled=!1,this._contentScrollable=!1,this._onScroll=e=>{const t=e.currentTarget;this._contentScrolled=(t.scrollTop??0)>this.scrollFadeThreshold,this._updateScrollableState(t)},this._resize=new o.P(this,{target:null,callback:e=>{const t=e[0]?.target;t&&this._updateScrollableState(t)}}),this.scrollFadeSafeAreaPadding=4,this.scrollFadeThreshold=4}}return t.DEFAULT_SCROLLABLE_ELEMENT=null,(0,i.Cg)([(0,s.wk)()],t.prototype,"_contentScrolled",void 0),(0,i.Cg)([(0,s.wk)()],t.prototype,"_contentScrollable",void 0),t}},14503(e,t,a){a.d(t,{RF:()=>r,dp:()=>l,kO:()=>s,nA:()=>n,og:()=>o});var i=a(96196);const o=i.AH`button.link{background:0 0;color:inherit;border:none;padding:0;font:inherit;text-align:left;text-decoration:underline;cursor:pointer;outline:0}`,r=i.AH`:host{font-family:var(--ha-font-family-body);-webkit-font-smoothing:var(--ha-font-smoothing);-moz-osx-font-smoothing:var(--ha-moz-osx-font-smoothing);font-size:var(--ha-font-size-m);font-weight:var(--ha-font-weight-normal);line-height:var(--ha-line-height-normal)}app-header div[sticky]{height:48px}app-toolbar [main-title]{margin-left:20px;margin-inline-start:20px;margin-inline-end:initial}.header{transition:box-shadow .2s linear,width var(--ha-animation-duration-normal) ease,padding-left var(--ha-animation-duration-normal) ease,padding-right var(--ha-animation-duration-normal) ease}@media (prefers-reduced-motion:reduce){.header{transition:box-shadow .2s linear}}h1{font-family:var(--ha-font-family-heading);-webkit-font-smoothing:var(--ha-font-smoothing);-moz-osx-font-smoothing:var(--ha-moz-osx-font-smoothing);font-size:var(--ha-font-size-2xl);font-weight:var(--ha-font-weight-normal);line-height:var(--ha-line-height-condensed)}h2{font-family:var(--ha-font-family-body);-webkit-font-smoothing:var(--ha-font-smoothing);-moz-osx-font-smoothing:var(--ha-moz-osx-font-smoothing);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;font-size:var(--ha-font-size-xl);font-weight:var(--ha-font-weight-medium);line-height:var(--ha-line-height-normal)}h3{font-family:var(--ha-font-family-body);-webkit-font-smoothing:var(--ha-font-smoothing);-moz-osx-font-smoothing:var(--ha-moz-osx-font-smoothing);font-size:var(--ha-font-size-l);font-weight:var(--ha-font-weight-normal);line-height:var(--ha-line-height-normal)}a{color:var(--primary-color)}.secondary{color:var(--secondary-text-color)}.error{color:var(--error-color)}.warning{color:var(--error-color)}${o} .card-actions a{text-decoration:none}.card-actions .warning{--mdc-theme-primary:var(--error-color)}.layout.horizontal,.layout.vertical{display:flex}.layout.inline{display:inline-flex}.layout.horizontal{flex-direction:row}.layout.vertical{flex-direction:column}.layout.wrap{flex-wrap:wrap}.layout.no-wrap{flex-wrap:nowrap}.layout.center,.layout.center-center{align-items:center}.layout.bottom{align-items:flex-end}.layout.center-center,.layout.center-justified{justify-content:center}.flex{flex:1;flex-basis:0.000000001px}.flex-auto{flex:1 1 auto}.flex-none{flex:none}.layout.justified{justify-content:space-between}`,n=i.AH`
  ha-dialog,
  ha-adaptive-dialog {
    --mdc-dialog-min-width: 400px;
    --mdc-dialog-max-width: 600px;
    --mdc-dialog-max-width: min(600px, 95vw);
    --justify-action-buttons: space-between;
    --dialog-container-padding: var(--safe-area-inset-top, 0)
      var(--safe-area-inset-right, 0) var(--safe-area-inset-bottom, 0)
      var(--safe-area-inset-left, 0);
    --dialog-surface-padding: 0px;
  }

  ha-dialog .form,
  ha-adaptive-dialog .form {
    color: var(--primary-text-color);
  }

  a {
    color: var(--primary-color);
  }

  /* make dialog fullscreen on small screens */
  @media all and (max-width: 450px), all and (max-height: 500px) {
    ha-dialog,
    ha-adaptive-dialog {
      --mdc-dialog-min-width: 100vw;
      --mdc-dialog-max-width: 100vw;
      --mdc-dialog-min-height: 100vh;
      --mdc-dialog-min-height: 100svh;
      --mdc-dialog-max-height: 100vh;
      --mdc-dialog-max-height: 100svh;
      --dialog-container-padding: 0px;
      --dialog-surface-padding: var(--safe-area-inset-top, 0)
        var(--safe-area-inset-right, 0) var(--safe-area-inset-bottom, 0)
        var(--safe-area-inset-left, 0);
      --vertical-align-dialog: flex-end;
      --ha-dialog-border-radius: var(--ha-border-radius-square);
    ha-dialog,
    ha-adaptive-dialog {
     --mdc-dialog-min-width: 100vw;
     --mdc-dialog-max-width: 100vw;
     --mdc-dialog-min-height: 100vh;
     --mdc-dialog-min-height: 100svh;
     --mdc-dialog-max-height: 100vh;
     --mdc-dialog-max-height: 100svh;
     --dialog-container-padding: 0px;
     --dialog-surface-padding: var(--safe-area-inset-top, 0)
       var(--safe-area-inset-right, 0) var(--safe-area-inset-bottom, 0)
       var(--safe-area-inset-left, 0);
     --vertical-align-dialog: flex-end;
   }
   ha-dialog {
      --ha-dialog-border-radius: var(--ha-border-radius-square);
   }
  }
  .error {
    color: var(--error-color);
  }
`,s=i.AH`ha-adaptive-dialog,ha-dialog{--vertical-align-dialog:flex-start;--dialog-surface-margin-top:var(--ha-space-10);--mdc-dialog-max-height:calc(
      100vh - var(--dialog-surface-margin-top) - var(--ha-space-2) - var(
          --safe-area-inset-y,
          0px
        )
    );--mdc-dialog-max-height:calc(
      100svh - var(--dialog-surface-margin-top) - var(--ha-space-2) - var(
          --safe-area-inset-y,
          0px
        )
    );--ha-dialog-max-height:calc(
      100vh - var(--dialog-surface-margin-top) - var(--ha-space-2) - var(
          --safe-area-inset-y,
          0px
        )
    );--ha-dialog-max-height:calc(
      100svh - var(--dialog-surface-margin-top) - var(--ha-space-2) - var(
          --safe-area-inset-y,
          0px
        )
    )}@media all and (max-width:450px),all and (max-height:500px){ha-adaptive-dialog,ha-dialog{--dialog-surface-margin-top:0px;--mdc-dialog-min-height:100vh;--mdc-dialog-min-height:100svh;--mdc-dialog-max-height:100vh;--mdc-dialog-max-height:100svh;--ha-dialog-max-height:100vh;--ha-dialog-max-height:100svh}}`,l=i.AH`.ha-scrollbar::-webkit-scrollbar{width:.4rem;height:.4rem}.ha-scrollbar::-webkit-scrollbar-thumb{border-radius:var(--ha-border-radius-sm);background:var(--scrollbar-thumb-color)}.ha-scrollbar{overflow-y:auto;scrollbar-color:var(--scrollbar-thumb-color) transparent;scrollbar-width:thin}`;i.AH`body{background-color:var(--primary-background-color);color:var(--primary-text-color);height:calc(100vh - 32px);width:100vw}`},996(e,t,a){a.d(t,{G:()=>i});a(45367),a(92731);class i{get(e){return this._cache.get(e)}set(e,t){this._cache.set(e,t),this._expiration&&window.setTimeout(()=>this._cache.delete(e),this._expiration)}has(e){return this._cache.has(e)}constructor(e){this._cache=new Map,this._expiration=e}}},36918(e,t,a){a.d(t,{o:()=>i});const i=(e,t)=>`https://${e.config.version.includes("b")?"rc":e.config.version.includes("dev")?"next":"www"}.home-assistant.io${t}`},22348(e,t,a){a.d(t,{V:()=>o});var i=a(37177);const o=e=>!!e.auth.external&&i.n},37177(e,t,a){a.d(t,{n:()=>i});const i=/^((?!chrome|android).)*safari/i.test(navigator.userAgent)},96175(e,t,a){var i={"./ha-icon-prev":["89133","61982"],"./ha-icon-button-toolbar":["9882","30628","76775"],"./ha-alert":["38962","19695"],"./ha-icon-button-toggle":["62501","77254"],"./ha-svg-icon.ts":["67094"],"./ha-alert.ts":["38962","19695"],"./ha-icon":["88945","51146"],"./ha-icon-next.ts":["43661","63902"],"./ha-qr-code.ts":["60543","51343","62740"],"./ha-icon-overflow-menu.ts":["75248","30628","34995","85545"],"./ha-icon-button-toggle.ts":["62501","77254"],"./ha-icon-button-group":["39826","13647"],"./ha-svg-icon":["67094"],"./ha-icon-button-prev":["45100","99197"],"./ha-icon-button.ts":["26300"],"./ha-icon-overflow-menu":["75248","30628","34995","85545"],"./ha-icon-button-arrow-next":["99028","54101"],"./ha-icon-button-prev.ts":["45100","99197"],"./ha-icon-picker":["64138","46095","31065","30628","92769","62453","78398","70744"],"./ha-icon-button-toolbar.ts":["9882","30628","76775"],"./ha-icon-button-arrow-prev.ts":["90248","17041"],"./ha-icon-button-next":["25440","81049"],"./ha-icon-next":["43661","63902"],"./ha-icon-picker.ts":["64138","46095","31065","30628","92769","62453","78398","70744"],"./ha-icon-prev.ts":["89133","61982"],"./ha-icon-button-arrow-prev":["90248","17041"],"./ha-icon-button-next.ts":["25440","81049"],"./ha-icon.ts":["88945","51146"],"./ha-qr-code":["60543","51343","62740"],"./ha-icon-button":["26300"],"./ha-icon-button-group.ts":["39826","13647"],"./ha-icon-button-arrow-next.ts":["99028","54101"]};function o(e){if(!a.o(i,e))return Promise.resolve().then(function(){var t=new Error("Cannot find module '"+e+"'");throw t.code="MODULE_NOT_FOUND",t});var t=i[e],o=t[0];return Promise.all(t.slice(1).map(a.e)).then(function(){return a(o)})}o.keys=()=>Object.keys(i),o.id=96175,e.exports=o}};
//# sourceMappingURL=91632.4b7297644933c544.js.map