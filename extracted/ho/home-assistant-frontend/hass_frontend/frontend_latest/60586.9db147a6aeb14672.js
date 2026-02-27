export const __rspack_esm_id="60586";export const __rspack_esm_ids=["60586"];export const __webpack_modules__={26218(t,e,a){a.d(e,{a:()=>i});const o=(0,a(77796).n)(t=>{history.replaceState({scrollPosition:t},"")},300);function i(t){return(e,a)=>{if("object"==typeof a)throw new Error("This decorator does not support this compilation type.");const i=e.connectedCallback;e.connectedCallback=function(){i.call(this);const e=this[a];e&&this.updateComplete.then(()=>{const a=this.renderRoot.querySelector(t);a&&setTimeout(()=>{a.scrollTop=e},0)})};const s=Object.getOwnPropertyDescriptor(e,a);let r;if(void 0===s)r={get(){return this[`__${String(a)}`]||history.state?.scrollPosition},set(t){o(t),this[`__${String(a)}`]=t},configurable:!0,enumerable:!0};else{const t=s.set;r={...s,set(e){o(e),this[`__${String(a)}`]=e,t?.call(this,e)}}}Object.defineProperty(e,a,r)}}},77796(t,e,a){a.d(e,{n:()=>o});const o=(t,e,a=!0,o=!0)=>{let i,s=0;const r=(...r)=>{const l=()=>{s=!1===a?0:Date.now(),i=void 0,t(...r)},n=Date.now();s||!1!==a||(s=n);const d=e-(n-s);d<=0||d>e?(i&&(clearTimeout(i),i=void 0),s=n,t(...r)):i||!1===o||(i=window.setTimeout(l,d))};return r.cancel=()=>{clearTimeout(i),i=void 0,s=0},r}},93444(t,e,a){var o=a(62826),i=a(96196),s=a(97735);class r extends i.WF{render(){return i.qy` <footer> <slot name="secondaryAction"></slot> <slot name="primaryAction"></slot> </footer> `}static get styles(){return[i.AH`footer{display:flex;gap:var(--ha-space-3);justify-content:flex-end;align-items:center;width:100%}`]}}r=(0,o.Cg)([(0,s.EM)("ha-dialog-footer")],r)},76538(t,e,a){var o=a(62826),i=a(96196),s=a(97735);class r extends i.WF{render(){const t=i.qy`<div class="header-title"> <slot name="title"></slot> </div>`,e=i.qy`<div class="header-subtitle"> <slot name="subtitle"></slot> </div>`;return i.qy` <header class="header"> <div class="header-bar"> <section class="header-navigation-icon"> <slot name="navigationIcon"></slot> </section> <section class="header-content"> ${"above"===this.subtitlePosition?i.qy`${e}${t}`:i.qy`${t}${e}`} </section> <section class="header-action-items"> <slot name="actionItems"></slot> </section> </div> <slot></slot> </header> `}static get styles(){return[i.AH`:host{display:block}:host([show-border]){border-bottom:1px solid var(--mdc-dialog-scroll-divider-color,rgba(0,0,0,.12))}.header-bar{display:flex;flex-direction:row;align-items:center;padding:0 var(--ha-space-1);box-sizing:border-box}.header-content{flex:1;padding:10px var(--ha-space-1);display:flex;flex-direction:column;justify-content:center;min-height:var(--ha-space-12);min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.header-title{height:var(--ha-dialog-header-title-height,calc(var(--ha-font-size-xl) + var(--ha-space-1)));font-size:var(--ha-font-size-xl);line-height:var(--ha-line-height-condensed);font-weight:var(--ha-font-weight-medium);color:var(--ha-dialog-header-title-color,var(--primary-text-color))}.header-subtitle{font-size:var(--ha-font-size-m);line-height:var(--ha-line-height-normal);color:var(--ha-dialog-header-subtitle-color,var(--secondary-text-color))}@media all and (min-width:450px) and (min-height:500px){.header-bar{padding:0 var(--ha-space-2)}}.header-navigation-icon{flex:none;min-width:var(--ha-space-2);height:100%;display:flex;flex-direction:row}.header-action-items{flex:none;min-width:var(--ha-space-2);height:100%;display:flex;flex-direction:row}`]}constructor(...t){super(...t),this.subtitlePosition="below",this.showBorder=!1}}(0,o.Cg)([(0,s.MZ)({type:String,attribute:"subtitle-position"})],r.prototype,"subtitlePosition",void 0),(0,o.Cg)([(0,s.MZ)({type:Boolean,reflect:!0,attribute:"show-border"})],r.prototype,"showBorder",void 0),r=(0,o.Cg)([(0,s.EM)("ha-dialog-header")],r)},72554(t,e,a){a.a(t,async function(t,e){try{var o=a(62826),i=a(93900),s=a(96196),r=a(97735),l=a(32288),n=a(1087),d=a(59992),h=a(14503),c=a(22348),p=(a(76538),a(26300)),g=t([i,p]);[i,p]=g.then?(await g)():g;const v="M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z";class u extends((0,d.V)(s.WF)){get scrollableElement(){return this.bodyContainer}updated(t){super.updated(t),t.has("open")&&(this._open=this.open)}render(){return s.qy` <wa-dialog .open="${this._open}" .lightDismiss="${!this.preventScrimClose}" without-header aria-labelledby="${(0,l.J)(this.ariaLabelledBy||(void 0!==this.headerTitle?"ha-dialog-title":void 0))}" aria-describedby="${(0,l.J)(this.ariaDescribedBy)}" @keydown="${this._handleKeyDown}" @wa-hide="${this._handleHide}" @wa-show="${this._handleShow}" @wa-after-show="${this._handleAfterShow}" @wa-after-hide="${this._handleAfterHide}"> ${this.withoutHeader?s.s6:s.qy` <slot name="header"> <ha-dialog-header .subtitlePosition="${this.headerSubtitlePosition}" .showBorder="${this._bodyScrolled}"> <slot name="headerNavigationIcon" slot="navigationIcon"> <ha-icon-button data-dialog="close" .label="${this.hass?.localize("ui.common.close")??"Close"}" .path="${v}"></ha-icon-button> </slot> ${void 0!==this.headerTitle?s.qy`<span slot="title" class="title" id="ha-dialog-title"> ${this.headerTitle} </span>`:s.qy`<slot name="headerTitle" slot="title"></slot>`} ${void 0!==this.headerSubtitle?s.qy`<span slot="subtitle">${this.headerSubtitle}</span>`:s.qy`<slot name="headerSubtitle" slot="subtitle"></slot>`} <slot name="headerActionItems" slot="actionItems"></slot> </ha-dialog-header> </slot>`} <div class="content-wrapper"> <div class="body ha-scrollbar" @scroll="${this._handleBodyScroll}"> <slot></slot> </div> ${this.renderScrollableFades()} </div> <slot name="footer" slot="footer"></slot> </wa-dialog> `}disconnectedCallback(){super.disconnectedCallback(),this._open=!1}_handleBodyScroll(t){this._bodyScrolled=t.target.scrollTop>0}_handleKeyDown(t){"Escape"===t.key&&(this._escapePressed=!0,this.preventScrimClose&&t.preventDefault(),t.stopPropagation(),t.currentTarget.open=!1)}_handleHide(t){const e=t.detail?.source===t.target.dialog;this.preventScrimClose&&this._escapePressed&&e&&t.preventDefault(),this._escapePressed=!1}static get styles(){return[...super.styles,h.dp,s.AH`
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

        :host([width="full"]) wa-dialog {
          --width: var(--full-width);
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
      `]}constructor(...t){super(...t),this.open=!1,this.type="standard",this.width="medium",this.preventScrimClose=!1,this.headerSubtitlePosition="below",this.flexContent=!1,this.withoutHeader=!1,this._open=!1,this._bodyScrolled=!1,this._escapePressed=!1,this._handleShow=async()=>{this._open=!0,(0,n.r)(this,"opened"),await this.updateComplete,requestAnimationFrame(()=>{if(this.hass&&(0,c.V)(this.hass)){const t=this.querySelector("[autofocus]");return void(null!==t&&(t.id||(t.id="ha-dialog-autofocus"),this.hass?.auth.external?.fireMessage({type:"focus_element",payload:{element_id:t.id}})))}this.querySelector("[autofocus]")?.focus()})},this._handleAfterShow=()=>{(0,n.r)(this,"after-show")},this._handleAfterHide=t=>{t.eventPhase===Event.AT_TARGET&&(this._open=!1,(0,n.r)(this,"closed"))}}}(0,o.Cg)([(0,r.MZ)({attribute:!1})],u.prototype,"hass",void 0),(0,o.Cg)([(0,r.MZ)({attribute:"aria-labelledby"})],u.prototype,"ariaLabelledBy",void 0),(0,o.Cg)([(0,r.MZ)({attribute:"aria-describedby"})],u.prototype,"ariaDescribedBy",void 0),(0,o.Cg)([(0,r.MZ)({type:Boolean,reflect:!0})],u.prototype,"open",void 0),(0,o.Cg)([(0,r.MZ)({reflect:!0})],u.prototype,"type",void 0),(0,o.Cg)([(0,r.MZ)({type:String,reflect:!0,attribute:"width"})],u.prototype,"width",void 0),(0,o.Cg)([(0,r.MZ)({type:Boolean,reflect:!0,attribute:"prevent-scrim-close"})],u.prototype,"preventScrimClose",void 0),(0,o.Cg)([(0,r.MZ)({attribute:"header-title"})],u.prototype,"headerTitle",void 0),(0,o.Cg)([(0,r.MZ)({attribute:"header-subtitle"})],u.prototype,"headerSubtitle",void 0),(0,o.Cg)([(0,r.MZ)({type:String,attribute:"header-subtitle-position"})],u.prototype,"headerSubtitlePosition",void 0),(0,o.Cg)([(0,r.MZ)({type:Boolean,reflect:!0,attribute:"flexcontent"})],u.prototype,"flexContent",void 0),(0,o.Cg)([(0,r.MZ)({type:Boolean,attribute:"without-header"})],u.prototype,"withoutHeader",void 0),(0,o.Cg)([(0,r.wk)()],u.prototype,"_open",void 0),(0,o.Cg)([(0,r.P)(".body")],u.prototype,"bodyContainer",void 0),(0,o.Cg)([(0,r.wk)()],u.prototype,"_bodyScrolled",void 0),(0,o.Cg)([(0,r.Ls)({passive:!0})],u.prototype,"_handleBodyScroll",null),u=(0,o.Cg)([(0,r.EM)("ha-dialog")],u),e()}catch(t){e(t)}})},90248(t,e,a){a.a(t,async function(t,o){try{a.r(e),a.d(e,{HaIconButtonArrowPrev:()=>p});var i=a(62826),s=a(96196),r=a(97735),l=a(63091),n=a(26300),d=t([n]);n=(d.then?(await d)():d)[0];const h="M20,11V13H8L13.5,18.5L12.08,19.92L4.16,12L12.08,4.08L13.5,5.5L8,11H20Z",c="M4,11V13H16L10.5,18.5L11.92,19.92L19.84,12L11.92,4.08L10.5,5.5L16,11H4Z";class p extends s.WF{render(){return s.qy` <ha-icon-button .disabled="${this.disabled}" .label="${this.label||this.hass?.localize("ui.common.back")||"Back"}" .path="${this._icon}" .href="${this.href}" .target="${this.target}" .rel="${this.rel}" .download="${this.download}"></ha-icon-button> `}constructor(...t){super(...t),this.disabled=!1,this._icon="rtl"===l.G.document.dir?c:h}}(0,i.Cg)([(0,r.MZ)({attribute:!1})],p.prototype,"hass",void 0),(0,i.Cg)([(0,r.MZ)({type:Boolean})],p.prototype,"disabled",void 0),(0,i.Cg)([(0,r.MZ)()],p.prototype,"label",void 0),(0,i.Cg)([(0,r.MZ)()],p.prototype,"href",void 0),(0,i.Cg)([(0,r.MZ)()],p.prototype,"target",void 0),(0,i.Cg)([(0,r.MZ)()],p.prototype,"rel",void 0),(0,i.Cg)([(0,r.MZ)()],p.prototype,"download",void 0),(0,i.Cg)([(0,r.wk)()],p.prototype,"_icon",void 0),p=(0,i.Cg)([(0,r.EM)("ha-icon-button-arrow-prev")],p),o()}catch(t){o(t)}})},47351(t,e,a){a.d(e,{PS:()=>i,Tv:()=>l,VR:()=>s,lE:()=>n});a(17642),a(58004),a(33853),a(45876),a(32475),a(15024),a(31698);var o=a(62384);const i=t=>t.data,s=t=>"object"==typeof t?"object"==typeof t.body?t.body.message||"Unknown error, see supervisor logs":t.body||t.message||"Unknown error, see supervisor logs":t,r=new Set([502,503,504]),l=t=>!!(t&&t.status_code&&r.has(t.status_code))||!(!t||!t.message||!t.message.includes("ERR_CONNECTION_CLOSED")&&!t.message.includes("ERR_CONNECTION_RESET")),n=async(t,e)=>(0,o.v)(t.config.version,2021,2,4)?t.callWS({type:"supervisor/api",endpoint:`/${e}/stats`,method:"get"}):i(await t.callApi("GET",`hassio/${e}/stats`))},90600(t,e,a){a.d(e,{GM:()=>r,IK:()=>d,MU:()=>l,OV:()=>s,RE:()=>h,Vo:()=>g,Yd:()=>v,h$:()=>n,w9:()=>u,xL:()=>p,y0:()=>c});var o=a(62384),i=a(47351);const s=async t=>{(0,o.v)(t.config.version,2021,2,4)?await t.callWS({type:"supervisor/api",endpoint:"/supervisor/reload",method:"post"}):await t.callApi("POST","hassio/supervisor/reload")},r=async t=>(0,o.v)(t.config.version,2021,2,4)?t.callWS({type:"supervisor/api",endpoint:"/supervisor/info",method:"get"}):(0,i.PS)(await t.callApi("GET","hassio/supervisor/info")),l=async t=>(0,o.v)(t.config.version,2021,2,4)?t.callWS({type:"supervisor/api",endpoint:"/info",method:"get"}):(0,i.PS)(await t.callApi("GET","hassio/info")),n=async t=>t.callApi("GET","hassio/host/logs/boots"),d=async(t,e)=>t.callApi("GET",`hassio/${e.includes("_")?`addons/${e}`:e}/logs`),h=async(t,e,a,o=0)=>t.callApiRaw("GET",`hassio/${e.includes("_")?`addons/${e}`:e}/logs${0!==o?`/boots/${o}`:""}`,void 0,a?{Range:a}:void 0),c=async(t,e,a,o=100,i=0)=>t.callApiRaw("GET",`hassio/${e.includes("_")?`addons/${e}`:e}/logs${0!==i?`/boots/${i}`:""}/follow?lines=${o}`,void 0,void 0,a),p=async(t,e,a,o,i,s=100,r=0)=>t.callApiRaw("GET",`hassio/${e.includes("_")?`addons/${e}`:e}/logs${0!==r?`/boots/${r}`:""}/follow`,void 0,{Range:`entries=${o}:${i}:${s}`},a),g=t=>`/api/hassio/${t.includes("_")?`addons/${t}`:t}/logs`,v=(t,e,a=0)=>`/api/hassio/${t.includes("_")?`addons/${t}`:t}/logs${0!==a?`/boots/${a}`:""}?lines=${e}`,u=async(t,e)=>{(0,o.v)(t.config.version,2021,2,4)?await t.callWS({type:"supervisor/api",endpoint:"/supervisor/options",method:"post",data:e}):await t.callApi("POST","hassio/supervisor/options",e)}},81310(t,e,a){a.a(t,async function(t,e){try{var o=a(62826),i=a(96196),s=a(97735),r=a(94333),l=a(26218),n=a(91926),d=a(90248),h=a(2054),c=a(14503),p=t([d,h]);[d,h]=p.then?(await p)():p;class g extends i.WF{render(){return i.qy` <div class="toolbar ${(0,r.H)({narrow:this.narrow})}"> <div class="toolbar-content"> ${this.mainPage||history.state?.root?i.qy` <ha-menu-button .hass="${this.hass}" .narrow="${this.narrow}"></ha-menu-button> `:this.backPath?i.qy` <ha-icon-button-arrow-prev href="${this.backPath}" .hass="${this.hass}"></ha-icon-button-arrow-prev> `:i.qy` <ha-icon-button-arrow-prev .hass="${this.hass}" @click="${this._backTapped}"></ha-icon-button-arrow-prev> `} <div class="main-title"> <slot name="header">${this.header}</slot> </div> <slot name="toolbar-icon"></slot> </div> </div> <div class="content ha-scrollbar" @scroll="${this._saveScrollPos}"> <slot></slot> </div> <div id="fab"> <slot name="fab"></slot> </div> `}_saveScrollPos(t){this._savedScrollPos=t.target.scrollTop}_backTapped(){this.backCallback?this.backCallback():(0,n.O)()}static get styles(){return[c.dp,i.AH`:host{display:block;height:100%;background-color:var(--primary-background-color);overflow:hidden;position:relative}:host([narrow]){width:100%;position:fixed}.toolbar{background-color:var(--app-header-background-color);padding-top:var(--safe-area-inset-top);padding-right:var(--safe-area-inset-right)}:host([narrow]) .toolbar{padding-left:var(--safe-area-inset-left)}.toolbar-content{display:flex;align-items:center;font-size:var(--ha-font-size-xl);height:var(--header-height);font-weight:var(--ha-font-weight-normal);color:var(--app-header-text-color,#fff);border-bottom:var(--app-header-border-bottom,none);box-sizing:border-box;padding:8px 12px}.toolbar a{color:var(--sidebar-text-color);text-decoration:none}::slotted([slot=toolbar-icon]),ha-icon-button-arrow-prev,ha-menu-button{display:flex;align-items:center;pointer-events:auto;color:var(--sidebar-icon-color)}.main-title{margin-inline-start:var(--ha-space-6);line-height:var(--ha-line-height-normal);min-width:0;flex-grow:1;overflow-wrap:break-word;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;text-overflow:ellipsis}.narrow .main-title{margin-inline-start:var(--ha-space-2)}.content{position:relative;width:calc(100% - var(--safe-area-inset-right,0px));height:calc(100% - 1px - var(--header-height,0px) - var(--safe-area-inset-top,0px) - var(--safe-area-inset-bottom,0px));padding-bottom:var(--safe-area-inset-bottom,0px);margin-right:var(--safe-area-inset-right);overflow-y:auto;overflow:auto;-webkit-overflow-scrolling:touch}:host([narrow]) .content{width:calc(100% - var(--safe-area-inset-left,0px) - var(--safe-area-inset-right,0px));margin-left:var(--safe-area-inset-left)}#fab{position:absolute;right:calc(16px + var(--safe-area-inset-right,0px));inset-inline-end:calc(16px + var(--safe-area-inset-right,0px));inset-inline-start:initial;bottom:calc(16px + var(--safe-area-inset-bottom,0px));z-index:1;display:flex;flex-wrap:wrap;justify-content:flex-end;gap:var(--ha-space-2)}:host([narrow]) #fab.tabs{bottom:calc(84px + var(--safe-area-inset-bottom,0px))}#fab[is-wide]{bottom:calc(24px + var(--safe-area-inset-bottom,0px));right:calc(24px + var(--safe-area-inset-right,0px));inset-inline-end:calc(24px + var(--safe-area-inset-right,0px));inset-inline-start:initial}`]}constructor(...t){super(...t),this.mainPage=!1,this.narrow=!1}}(0,o.Cg)([(0,s.MZ)({attribute:!1})],g.prototype,"hass",void 0),(0,o.Cg)([(0,s.MZ)()],g.prototype,"header",void 0),(0,o.Cg)([(0,s.MZ)({type:Boolean,attribute:"main-page"})],g.prototype,"mainPage",void 0),(0,o.Cg)([(0,s.MZ)({type:String,attribute:"back-path"})],g.prototype,"backPath",void 0),(0,o.Cg)([(0,s.MZ)({attribute:!1})],g.prototype,"backCallback",void 0),(0,o.Cg)([(0,s.MZ)({type:Boolean,reflect:!0})],g.prototype,"narrow",void 0),(0,o.Cg)([(0,l.a)(".content")],g.prototype,"_savedScrollPos",void 0),(0,o.Cg)([(0,s.Ls)({passive:!0})],g.prototype,"_saveScrollPos",null),g=(0,o.Cg)([(0,s.EM)("hass-subpage")],g),e()}catch(t){e(t)}})},59992(t,e,a){a.d(e,{V:()=>n});var o=a(62826),i=a(88696),s=a(96196),r=a(94333),l=a(97735);const n=t=>{class e extends t{get scrollableElement(){return e.DEFAULT_SCROLLABLE_ELEMENT}firstUpdated(t){super.firstUpdated?.(t),this.scrollableElement&&this._updateScrollableState(this.scrollableElement),this._attachScrollableElement()}updated(t){super.updated?.(t),this._attachScrollableElement()}disconnectedCallback(){this._detachScrollableElement(),this._contentScrolled=!1,this._contentScrollable=!1,super.disconnectedCallback()}renderScrollableFades(t=!1){return s.qy` <div class="${(0,r.H)({"fade-top":!0,rounded:t,visible:this._contentScrolled})}"></div> <div class="${(0,r.H)({"fade-bottom":!0,rounded:t,visible:this._contentScrollable})}"></div> `}static get styles(){const t=Object.getPrototypeOf(this);var e;return[...void 0===(e=t?.styles??[])?[]:Array.isArray(e)?e:[e],s.AH`.fade-bottom,.fade-top{position:absolute;left:0;right:0;height:var(--ha-space-2);pointer-events:none;transition:opacity 180ms ease-in-out;border-radius:var(--ha-border-radius-square);opacity:0;background:linear-gradient(to bottom,var(--ha-color-shadow-scrollable-fade),transparent)}.fade-top{top:0}.fade-bottom{bottom:0;transform:rotate(180deg)}.fade-bottom.visible,.fade-top.visible{opacity:1}.fade-bottom.rounded,.fade-top.rounded{border-radius:var(--ha-card-border-radius,var(--ha-border-radius-lg));border-bottom-left-radius:var(--ha-border-radius-square);border-bottom-right-radius:var(--ha-border-radius-square)}.fade-top.rounded{border-top-left-radius:var(--ha-border-radius-square);border-top-right-radius:var(--ha-border-radius-square)}.fade-bottom.rounded{border-bottom-left-radius:var(--ha-border-radius-square);border-bottom-right-radius:var(--ha-border-radius-square)}`]}_attachScrollableElement(){const t=this.scrollableElement;t!==this._scrollTarget&&(this._detachScrollableElement(),t&&(this._scrollTarget=t,t.addEventListener("scroll",this._onScroll,{passive:!0}),this._resize.observe(t),this._updateScrollableState(t)))}_detachScrollableElement(){this._scrollTarget&&(this._scrollTarget.removeEventListener("scroll",this._onScroll),this._resize.unobserve?.(this._scrollTarget),this._scrollTarget=void 0)}_updateScrollableState(t){const e=parseFloat(getComputedStyle(t).getPropertyValue("--safe-area-inset-bottom"))||0,{scrollHeight:a=0,clientHeight:o=0,scrollTop:i=0}=t;this._contentScrollable=a-o>i+e+this.scrollFadeSafeAreaPadding}constructor(...t){super(...t),this._contentScrolled=!1,this._contentScrollable=!1,this._onScroll=t=>{const e=t.currentTarget;this._contentScrolled=(e.scrollTop??0)>this.scrollFadeThreshold,this._updateScrollableState(e)},this._resize=new i.P(this,{target:null,callback:t=>{const e=t[0]?.target;e&&this._updateScrollableState(e)}}),this.scrollFadeSafeAreaPadding=4,this.scrollFadeThreshold=4}}return e.DEFAULT_SCROLLABLE_ELEMENT=null,(0,o.Cg)([(0,l.wk)()],e.prototype,"_contentScrolled",void 0),(0,o.Cg)([(0,l.wk)()],e.prototype,"_contentScrollable",void 0),e}},89905(t,e,a){a.a(t,async function(t,o){try{a.r(e);a(14603),a(47566),a(98721);var i=a(62826),s=a(96196),r=a(97735),l=a(22786),n=a(36312),d=(a(76776),a(47351)),h=a(90600),c=a(24247),p=a(65063),g=a(81310),v=a(87842),u=a(96897),b=a(29823),f=(a(70947),a(71786),t([g,v,b,u,c]));[g,v,b,u,c]=f.then?(await f)():f;const w="M12,16A2,2 0 0,1 14,18A2,2 0 0,1 12,20A2,2 0 0,1 10,18A2,2 0 0,1 12,16M12,10A2,2 0 0,1 14,12A2,2 0 0,1 12,14A2,2 0 0,1 10,12A2,2 0 0,1 12,10M12,4A2,2 0 0,1 14,6A2,2 0 0,1 12,8A2,2 0 0,1 10,6A2,2 0 0,1 12,4Z",m="M14 12L10 8V11H2V13H10V16M22 12A10 10 0 0 1 2.46 15H4.59A8 8 0 1 0 4.59 9H2.46A10 10 0 0 1 22 12Z",y="M22 12L18 8V11H10V13H18V16M20 18A10 10 0 1 1 20 6H17.27A8 8 0 1 0 17.27 18Z",_="M17.65,6.35C16.2,4.9 14.21,4 12,4A8,8 0 0,0 4,12A8,8 0 0,0 12,20C15.73,20 18.84,17.45 19.73,14H17.65C16.83,16.33 14.61,18 12,18A6,6 0 0,1 6,12A6,6 0 0,1 12,6C13.66,6 15.14,6.69 16.22,7.78L13,11H20V4L17.65,6.35Z";class x extends s.WF{firstUpdated(t){super.firstUpdated(t),(0,n.x)(this.hass,"hassio")&&this._refreshSupervisorInfo()}render(){const t=this._filterInstallableUpdateEntities(this.hass.states,this._showSkipped),e=this._filterNotInstallableUpdateEntities(this.hass.states,this._showSkipped);return s.qy` <hass-subpage .backPath="${this._searchParms.has("historyBack")?void 0:"/config/system"}" .hass="${this.hass}" .narrow="${this.narrow}" .header="${this.hass.localize("ui.panel.config.updates.caption")}"> <div slot="toolbar-icon"> <ha-icon-button .label="${this.hass.localize("ui.panel.config.updates.check_updates")}" .path="${_}" @click="${this._checkUpdates}"></ha-icon-button> <ha-dropdown @wa-select="${this._handleOverflowAction}"> <ha-icon-button slot="trigger" .label="${this.hass.localize("ui.common.menu")}" .path="${w}"></ha-icon-button> <ha-dropdown-item type="checkbox" .checked="${this._showSkipped}" value="show_skipped"> ${this.hass.localize("ui.panel.config.updates.show_skipped")} </ha-dropdown-item> ${this._supervisorInfo?s.qy` <wa-divider></wa-divider> <ha-dropdown-item value="toggle_beta" .disabled="${"dev"===this._supervisorInfo.channel}"> <ha-svg-icon .path="${"stable"===this._supervisorInfo.channel?m:y}" slot="icon"></ha-svg-icon> ${this.hass.localize(`ui.panel.config.updates.${"stable"===this._supervisorInfo.channel?"join":"leave"}_beta`)} </ha-dropdown-item> `:s.s6} </ha-dropdown> </div> <div class="content"> ${t.length?s.qy` <ha-card outlined> <div class="card-content"> <ha-config-updates .hass="${this.hass}" .narrow="${this.narrow}" .updateEntities="${t}" .isInstallable="${!0}" showAll></ha-config-updates> </div> </ha-card> `:s.s6} ${e.length?s.qy` <ha-card outlined> <div class="card-content"> <ha-config-updates .hass="${this.hass}" .narrow="${this.narrow}" .updateEntities="${e}" .isInstallable="${!1}" showAll></ha-config-updates> </div> </ha-card> `:s.s6} ${t.length+e.length?s.s6:s.qy` <ha-card outlined> <div class="no-updates"> ${this.hass.localize("ui.panel.config.updates.no_updates")} </div> </ha-card> `} </div> </hass-subpage> `}async _refreshSupervisorInfo(){this._supervisorInfo=await(0,h.GM)(this.hass)}_handleOverflowAction(t){"toggle_beta"===t.detail.item.value?"stable"===this._supervisorInfo.channel?(0,u.U)(this,{join:()=>this._setChannel("beta")}):this._setChannel("stable"):"show_skipped"===t.detail.item.value&&(this._showSkipped=!this._showSkipped)}async _setChannel(t){try{await(0,h.w9)(this.hass,{channel:t}),await(0,h.OV)(this.hass),await this._refreshSupervisorInfo()}catch(t){(0,p.showAlertDialog)(this,{text:(0,d.VR)(t)})}}async _checkUpdates(){(0,c.nD)(this,this.hass)}constructor(...t){super(...t),this.narrow=!1,this._searchParms=new URLSearchParams(window.location.search),this._showSkipped=!1,this._filterInstallableUpdateEntities=(0,l.A)((t,e)=>(0,c.id)(t,e,!1)),this._filterNotInstallableUpdateEntities=(0,l.A)((t,e)=>(0,c.id)(t,e,!0))}}x.styles=s.AH`.content{padding:28px 20px 0;max-width:1040px;margin:0 auto}ha-card{max-width:600px;margin:0 auto;height:100%;justify-content:space-between;flex-direction:column;display:flex;margin-bottom:max(24px,var(--safe-area-inset-bottom))}ha-config-updates{margin-bottom:8px}.card-content{display:flex;justify-content:space-between;flex-direction:column;padding:0}.no-updates{padding:16px}li[divider]{border-bottom-color:var(--divider-color)}`,(0,i.Cg)([(0,r.MZ)({attribute:!1})],x.prototype,"hass",void 0),(0,i.Cg)([(0,r.MZ)({type:Boolean})],x.prototype,"narrow",void 0),(0,i.Cg)([(0,r.wk)()],x.prototype,"_searchParms",void 0),(0,i.Cg)([(0,r.wk)()],x.prototype,"_showSkipped",void 0),(0,i.Cg)([(0,r.wk)()],x.prototype,"_supervisorInfo",void 0),x=(0,i.Cg)([(0,r.EM)("ha-config-section-updates")],x),o()}catch(t){o(t)}})},15685(t,e,a){a.a(t,async function(t,o){try{a.r(e),a.d(e,{DialogJoinBeta:()=>u});var i=a(62826),s=a(96196),r=a(97735),l=a(1087),n=a(38962),d=a(18350),h=(a(93444),a(72554)),c=a(14503),p=a(36918),g=t([n,d,h]);[n,d,h]=g.then?(await g)():g;const v="M14,3V5H17.59L7.76,14.83L9.17,16.24L19,6.41V10H21V3M19,19H5V5H12V3H5C3.89,3 3,3.9 3,5V19A2,2 0 0,0 5,21H19A2,2 0 0,0 21,19V12H19V19Z";class u extends s.WF{showDialog(t){this._dialogParams=t,this._open=!0}closeDialog(){return this._open=!1,!0}_dialogClosed(){this._dialogParams=void 0,(0,l.r)(this,"dialog-closed",{dialog:this.localName})}render(){return this._dialogParams?s.qy` <ha-dialog .hass="${this.hass}" .open="${this._open}" header-title="${this.hass.localize("ui.dialogs.join_beta_channel.title")}" @closed="${this._dialogClosed}"> <ha-alert alert-type="warning"> ${this.hass.localize("ui.dialogs.join_beta_channel.backup")} </ha-alert> <p> ${this.hass.localize("ui.dialogs.join_beta_channel.warning")}.<br> ${this.hass.localize("ui.dialogs.join_beta_channel.release_items")} </p> <ul> <li>Home Assistant Core</li> <li>Home Assistant Supervisor</li> <li>Home Assistant Operating System</li> </ul> <a href="${(0,p.o)(this.hass,"/faq/release/")}" target="_blank" rel="noreferrer"> ${this.hass.localize("ui.dialogs.join_beta_channel.view_documentation")} <ha-svg-icon .path="${v}"></ha-svg-icon> </a> <ha-dialog-footer slot="footer"> <ha-button slot="secondaryAction" appearance="plain" @click="${this._cancel}"> ${this.hass.localize("ui.common.cancel")} </ha-button> <ha-button slot="primaryAction" @click="${this._join}"> ${this.hass.localize("ui.dialogs.join_beta_channel.join")} </ha-button> </ha-dialog-footer> </ha-dialog> `:s.s6}_cancel(){this._dialogParams?.cancel?.(),this.closeDialog()}_join(){this._dialogParams?.join?.(),this.closeDialog()}static get styles(){return[c.nA,s.AH`a{text-decoration:none}a ha-svg-icon{--mdc-icon-size:16px}`]}constructor(...t){super(...t),this._open=!1}}(0,i.Cg)([(0,r.MZ)({attribute:!1})],u.prototype,"hass",void 0),(0,i.Cg)([(0,r.wk)()],u.prototype,"_dialogParams",void 0),(0,i.Cg)([(0,r.wk)()],u.prototype,"_open",void 0),u=(0,i.Cg)([(0,r.EM)("dialog-join-beta")],u),o()}catch(t){o(t)}})},96897(t,e,a){a.a(t,async function(t,o){try{a.d(e,{U:()=>l});var i=a(1087),s=a(15685),r=t([s]);s=(r.then?(await r)():r)[0];const l=(t,e)=>{(0,i.r)(t,"show-dialog",{dialogTag:"dialog-join-beta",dialogImport:()=>Promise.resolve().then(a.bind(a,15685)),dialogParams:e})};o()}catch(t){o(t)}})},22348(t,e,a){a.d(e,{V:()=>i});var o=a(37177);const i=t=>!!t.auth.external&&o.n},37177(t,e,a){a.d(e,{n:()=>o});const o=/^((?!chrome|android).)*safari/i.test(navigator.userAgent)}};
//# sourceMappingURL=60586.9db147a6aeb14672.js.map