export const __rspack_esm_id="7901";export const __rspack_esm_ids=["7901"];export const __webpack_modules__={80785(e,t,a){function o(e){return!!e&&(e instanceof Date&&!isNaN(e.valueOf()))}a.d(t,{A:()=>o})},72487(e,t,a){a.a(e,async function(e,o){try{a.d(t,{CA:()=>k,Pm:()=>w,Wq:()=>y,Yq:()=>d,fr:()=>v,gu:()=>S,kz:()=>h,sl:()=>g,zB:()=>p});a(18111),a(20116);var i=a(74487),r=a(22786),n=a(46927),l=a(8480),s=e([i,l]);[i,l]=s.then?(await s)():s;(0,r.A)((e,t)=>new Intl.DateTimeFormat(e.language,{weekday:"long",month:"long",day:"numeric",timeZone:(0,l.w)(e.time_zone,t)}));const d=(e,t,a)=>c(t,a.time_zone).format(e),c=(0,r.A)((e,t)=>new Intl.DateTimeFormat(e.language,{year:"numeric",month:"long",day:"numeric",timeZone:(0,l.w)(e.time_zone,t)})),h=(e,t,a)=>u(t,a.time_zone).format(e),u=(0,r.A)((e,t)=>new Intl.DateTimeFormat(e.language,{year:"numeric",month:"short",day:"numeric",timeZone:(0,l.w)(e.time_zone,t)})),p=(e,t,a)=>{const o=m(t,a.time_zone);if(t.date_format===n.ow.language||t.date_format===n.ow.system)return o.format(e);const i=o.formatToParts(e),r=i.find(e=>"literal"===e.type)?.value,l=i.find(e=>"day"===e.type)?.value,s=i.find(e=>"month"===e.type)?.value,d=i.find(e=>"year"===e.type)?.value,c=i[i.length-1];let h="literal"===c?.type?c?.value:"";"bg"===t.language&&t.date_format===n.ow.YMD&&(h="");return{[n.ow.DMY]:`${l}${r}${s}${r}${d}${h}`,[n.ow.MDY]:`${s}${r}${l}${r}${d}${h}`,[n.ow.YMD]:`${d}${r}${s}${r}${l}${h}`}[t.date_format]},m=(0,r.A)((e,t)=>{const a=e.date_format===n.ow.system?void 0:e.language;return e.date_format===n.ow.language||(e.date_format,n.ow.system),new Intl.DateTimeFormat(a,{year:"numeric",month:"numeric",day:"numeric",timeZone:(0,l.w)(e.time_zone,t)})}),g=(e,t,a)=>f(t,a.time_zone).format(e),f=(0,r.A)((e,t)=>new Intl.DateTimeFormat(e.language,{day:"numeric",month:"short",timeZone:(0,l.w)(e.time_zone,t)})),v=(e,t,a)=>b(t,a.time_zone).format(e),b=(0,r.A)((e,t)=>new Intl.DateTimeFormat(e.language,{month:"long",year:"numeric",timeZone:(0,l.w)(e.time_zone,t)})),y=(e,t,a)=>_(t,a.time_zone).format(e),_=(0,r.A)((e,t)=>new Intl.DateTimeFormat(e.language,{month:"long",timeZone:(0,l.w)(e.time_zone,t)})),w=(e,t,a)=>x(t,a.time_zone).format(e),x=(0,r.A)((e,t)=>new Intl.DateTimeFormat(e.language,{year:"numeric",timeZone:(0,l.w)(e.time_zone,t)})),k=(e,t,a)=>C(t,a.time_zone).format(e),C=(0,r.A)((e,t)=>new Intl.DateTimeFormat(e.language,{weekday:"long",timeZone:(0,l.w)(e.time_zone,t)})),S=(e,t,a)=>$(t,a.time_zone).format(e),$=(0,r.A)((e,t)=>new Intl.DateTimeFormat(e.language,{weekday:"short",timeZone:(0,l.w)(e.time_zone,t)}));o()}catch(e){o(e)}})},95747(e,t,a){a.a(e,async function(e,o){try{a.d(t,{CL:()=>y,GH:()=>x,Rl:()=>p,ZS:()=>v,aQ:()=>g,r6:()=>h,yg:()=>_});var i=a(74487),r=a(22786),n=a(72487),l=a(30162),s=a(8480),d=a(69543),c=e([i,s,n,l]);[i,s,n,l]=c.then?(await c)():c;const h=(e,t,a)=>u(t,a.time_zone).format(e),u=(0,r.A)((e,t)=>new Intl.DateTimeFormat(e.language,{year:"numeric",month:"long",day:"numeric",hour:(0,d.J)(e)?"numeric":"2-digit",minute:"2-digit",hourCycle:(0,d.J)(e)?"h12":"h23",timeZone:(0,s.w)(e.time_zone,t)})),p=e=>m().format(e),m=(0,r.A)(()=>new Intl.DateTimeFormat(void 0,{year:"numeric",month:"long",day:"numeric",hour:"2-digit",minute:"2-digit"})),g=(e,t,a)=>f(t,a.time_zone).format(e),f=(0,r.A)((e,t)=>new Intl.DateTimeFormat(e.language,{year:"numeric",month:"short",day:"numeric",hour:(0,d.J)(e)?"numeric":"2-digit",minute:"2-digit",hourCycle:(0,d.J)(e)?"h12":"h23",timeZone:(0,s.w)(e.time_zone,t)})),v=(e,t,a)=>b(t,a.time_zone).format(e),b=(0,r.A)((e,t)=>new Intl.DateTimeFormat(e.language,{month:"short",day:"numeric",hour:(0,d.J)(e)?"numeric":"2-digit",minute:"2-digit",hourCycle:(0,d.J)(e)?"h12":"h23",timeZone:(0,s.w)(e.time_zone,t)})),y=(e,t,a)=>(new Date).getFullYear()===e.getFullYear()?v(e,t,a):g(e,t,a),_=(e,t,a)=>w(t,a.time_zone).format(e),w=(0,r.A)((e,t)=>new Intl.DateTimeFormat(e.language,{year:"numeric",month:"long",day:"numeric",hour:(0,d.J)(e)?"numeric":"2-digit",minute:"2-digit",second:"2-digit",hourCycle:(0,d.J)(e)?"h12":"h23",timeZone:(0,s.w)(e.time_zone,t)})),x=(e,t,a)=>`${(0,n.zB)(e,t,a)}, ${(0,l.fU)(e,t,a)}`;o()}catch(e){o(e)}})},30162(e,t,a){a.a(e,async function(e,o){try{a.d(t,{LW:()=>g,Xs:()=>p,fU:()=>d,ie:()=>h});var i=a(74487),r=a(22786),n=a(8480),l=a(69543),s=e([i,n]);[i,n]=s.then?(await s)():s;const d=(e,t,a)=>c(t,a.time_zone).format(e),c=(0,r.A)((e,t)=>new Intl.DateTimeFormat(e.language,{hour:"numeric",minute:"2-digit",hourCycle:(0,l.J)(e)?"h12":"h23",timeZone:(0,n.w)(e.time_zone,t)})),h=(e,t,a)=>u(t,a.time_zone).format(e),u=(0,r.A)((e,t)=>new Intl.DateTimeFormat(e.language,{hour:(0,l.J)(e)?"numeric":"2-digit",minute:"2-digit",second:"2-digit",hourCycle:(0,l.J)(e)?"h12":"h23",timeZone:(0,n.w)(e.time_zone,t)})),p=(e,t,a)=>m(t,a.time_zone).format(e),m=(0,r.A)((e,t)=>new Intl.DateTimeFormat(e.language,{weekday:"long",hour:(0,l.J)(e)?"numeric":"2-digit",minute:"2-digit",hourCycle:(0,l.J)(e)?"h12":"h23",timeZone:(0,n.w)(e.time_zone,t)})),g=(e,t,a)=>f(t,a.time_zone).format(e),f=(0,r.A)((e,t)=>new Intl.DateTimeFormat("en-GB",{hour:"numeric",minute:"2-digit",hour12:!1,timeZone:(0,n.w)(e.time_zone,t)}));o()}catch(e){o(e)}})},98975(e,t,a){a.a(e,async function(e,o){try{a.d(t,{K:()=>d});var i=a(74487),r=a(22786),n=a(63927),l=e([i,n]);[i,n]=l.then?(await l)():l;const s=(0,r.A)(e=>new Intl.RelativeTimeFormat(e.language,{numeric:"auto"})),d=(e,t,a,o=!0)=>{const i=(0,n.x)(e,a,t);return o?s(t).format(i.value,i.unit):Intl.NumberFormat(t.language,{style:"unit",unit:i.unit,unitDisplay:"long"}).format(Math.abs(i.value))};o()}catch(e){o(e)}})},8480(e,t,a){a.a(e,async function(e,o){try{a.d(t,{n:()=>s,w:()=>d});var i=a(74487),r=a(46927),n=e([i]);i=(n.then?(await n)():n)[0];const l=Intl.DateTimeFormat?.().resolvedOptions?.().timeZone,s=l??"UTC",d=(e,t)=>e===r.Wj.local&&l?s:t;o()}catch(e){o(e)}})},69543(e,t,a){a.d(t,{J:()=>r});var o=a(22786),i=a(46927);const r=(0,o.A)(e=>{if(e.time_format===i.Hg.language||e.time_format===i.Hg.system){const t=e.time_format===i.Hg.language?e.language:void 0;return new Date("January 1, 2023 22:00:00").toLocaleString(t).includes("10")}return e.time_format===i.Hg.am_pm})},63927(e,t,a){a.a(e,async function(e,o){try{a.d(t,{x:()=>h});var i=a(6946),r=a(52640),n=a(38684),l=a(380);const s=1e3,d=60,c=60*d;function h(e,t=Date.now(),a,o={}){const h={...u,...o||{}},p=(+e-+t)/s;if(Math.abs(p)<h.second)return{value:Math.round(p),unit:"second"};const m=p/d;if(Math.abs(m)<h.minute)return{value:Math.round(m),unit:"minute"};const g=p/c;if(Math.abs(g)<h.hour)return{value:Math.round(g),unit:"hour"};const f=new Date(e),v=new Date(t);f.setHours(0,0,0,0),v.setHours(0,0,0,0);const b=(0,i.c)(f,v);if(0===b)return{value:Math.round(g),unit:"hour"};if(Math.abs(b)<h.day)return{value:b,unit:"day"};const y=(0,l.P)(a),_=(0,r.k)(f,{weekStartsOn:y}),w=(0,r.k)(v,{weekStartsOn:y}),x=(0,n.I)(_,w);if(0===x)return{value:b,unit:"day"};if(Math.abs(x)<h.week)return{value:x,unit:"week"};const k=f.getFullYear()-v.getFullYear(),C=12*k+f.getMonth()-v.getMonth();return 0===C?{value:x,unit:"week"}:Math.abs(C)<h.month||0===k?{value:C,unit:"month"}:{value:Math.round(k),unit:"year"}}const u={second:59,minute:59,hour:22,day:5,week:4,month:11};o()}catch(p){o(p)}})},93444(e,t,a){var o=a(62826),i=a(96196),r=a(44457);class n extends i.WF{render(){return i.qy` <footer> <slot name="secondaryAction"></slot> <slot name="primaryAction"></slot> </footer> `}static get styles(){return[i.AH`footer{display:flex;gap:var(--ha-space-3);justify-content:flex-end;align-items:center;width:100%}`]}}n=(0,o.Cg)([(0,r.EM)("ha-dialog-footer")],n)},76538(e,t,a){var o=a(62826),i=a(96196),r=a(44457);class n extends i.WF{render(){const e=i.qy`<div class="header-title"> <slot name="title"></slot> </div>`,t=i.qy`<div class="header-subtitle"> <slot name="subtitle"></slot> </div>`;return i.qy` <header class="header"> <div class="header-bar"> <section class="header-navigation-icon"> <slot name="navigationIcon"></slot> </section> <section class="header-content"> ${"above"===this.subtitlePosition?i.qy`${t}${e}`:i.qy`${e}${t}`} </section> <section class="header-action-items"> <slot name="actionItems"></slot> </section> </div> <slot></slot> </header> `}static get styles(){return[i.AH`:host{display:block}:host([show-border]){border-bottom:1px solid var(--mdc-dialog-scroll-divider-color,rgba(0,0,0,.12))}.header-bar{display:flex;flex-direction:row;align-items:center;padding:0 var(--ha-space-1);box-sizing:border-box}.header-content{flex:1;padding:10px var(--ha-space-1);display:flex;flex-direction:column;justify-content:center;min-height:var(--ha-space-12);min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.header-title{height:var(--ha-dialog-header-title-height,calc(var(--ha-font-size-xl) + var(--ha-space-1)));font-size:var(--ha-font-size-xl);line-height:var(--ha-line-height-condensed);font-weight:var(--ha-font-weight-medium);color:var(--ha-dialog-header-title-color,var(--primary-text-color))}.header-subtitle{font-size:var(--ha-font-size-m);line-height:var(--ha-line-height-normal);color:var(--ha-dialog-header-subtitle-color,var(--secondary-text-color))}@media all and (min-width:450px) and (min-height:500px){.header-bar{padding:0 var(--ha-space-2)}}.header-navigation-icon{flex:none;min-width:var(--ha-space-2);height:100%;display:flex;flex-direction:row}.header-action-items{flex:none;min-width:var(--ha-space-2);height:100%;display:flex;flex-direction:row}`]}constructor(...e){super(...e),this.subtitlePosition="below",this.showBorder=!1}}(0,o.Cg)([(0,r.MZ)({type:String,attribute:"subtitle-position"})],n.prototype,"subtitlePosition",void 0),(0,o.Cg)([(0,r.MZ)({type:Boolean,reflect:!0,attribute:"show-border"})],n.prototype,"showBorder",void 0),n=(0,o.Cg)([(0,r.EM)("ha-dialog-header")],n)},2846(e,t,a){a.d(t,{G:()=>d,J:()=>s});var o=a(62826),i=a(97154),r=a(82553),n=a(96196),l=a(44457);a(54276);const s=[r.R,n.AH`:host{--ha-icon-display:block;--md-sys-color-primary:var(--primary-text-color);--md-sys-color-secondary:var(--secondary-text-color);--md-sys-color-surface:var(--card-background-color);--md-sys-color-on-surface:var(--primary-text-color);--md-sys-color-on-surface-variant:var(--secondary-text-color)}md-item{overflow:var(--md-item-overflow,hidden);align-items:var(--md-item-align-items,center);gap:var(--ha-md-list-item-gap,16px)}`];class d extends i.n{renderRipple(){return"text"===this.type?n.s6:n.qy`<ha-ripple part="ripple" for="item" ?disabled="${this.disabled&&"link"!==this.type}"></ha-ripple>`}}d.styles=s,d=(0,o.Cg)([(0,l.EM)("ha-md-list-item")],d)},17308(e,t,a){var o=a(62826),i=a(49838),r=a(11245),n=a(96196),l=a(44457);class s extends i.B{}s.styles=[r.R,n.AH`:host{--md-sys-color-surface:var(--card-background-color)}`],s=(0,o.Cg)([(0,l.EM)("ha-md-list")],s)},54276(e,t,a){var o=a(62826),i=a(76482),r=a(91382),n=a(96245),l=a(96196),s=a(44457);class d extends r.n{attach(e){super.attach(e),this.attachableTouchController.attach(e)}disconnectedCallback(){super.disconnectedCallback(),this.hovered=!1,this.pressed=!1}detach(){super.detach(),this.attachableTouchController.detach()}_onTouchControlChange(e,t){e?.removeEventListener("touchend",this._handleTouchEnd),t?.addEventListener("touchend",this._handleTouchEnd)}constructor(...e){super(...e),this.attachableTouchController=new i.i(this,this._onTouchControlChange.bind(this)),this._handleTouchEnd=()=>{this.disabled||super.endPressAnimation()}}}d.styles=[n.R,l.AH`:host{--md-ripple-hover-opacity:var(--ha-ripple-hover-opacity, 0.08);--md-ripple-pressed-opacity:var(--ha-ripple-pressed-opacity, 0.12);--md-ripple-hover-color:var(
          --ha-ripple-hover-color,
          var(--ha-ripple-color, var(--secondary-text-color))
        );--md-ripple-pressed-color:var(
          --ha-ripple-pressed-color,
          var(--ha-ripple-color, var(--secondary-text-color))
        )}`],d=(0,o.Cg)([(0,s.EM)("ha-ripple")],d)},45331(e,t,a){a.a(e,async function(e,t){try{var o=a(62826),i=a(93900),r=a(96196),n=a(44457),l=a(32288),s=a(1087),d=a(59992),c=a(14503),h=(a(76538),a(26300),e([i]));i=(h.then?(await h)():h)[0];const u="M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z";class p extends((0,d.V)(r.WF)){get scrollableElement(){return this.bodyContainer}updated(e){super.updated(e),e.has("open")&&(this._open=this.open)}render(){return r.qy` <wa-dialog .open="${this._open}" .lightDismiss="${!this.preventScrimClose}" without-header aria-labelledby="${(0,l.J)(this.ariaLabelledBy||(void 0!==this.headerTitle?"ha-wa-dialog-title":void 0))}" aria-describedby="${(0,l.J)(this.ariaDescribedBy)}" @wa-show="${this._handleShow}" @wa-after-show="${this._handleAfterShow}" @wa-after-hide="${this._handleAfterHide}"> <slot name="header"> <ha-dialog-header .subtitlePosition="${this.headerSubtitlePosition}" .showBorder="${this._bodyScrolled}"> <slot name="headerNavigationIcon" slot="navigationIcon"> <ha-icon-button data-dialog="close" .label="${this.hass?.localize("ui.common.close")??"Close"}" .path="${u}"></ha-icon-button> </slot> ${void 0!==this.headerTitle?r.qy`<span slot="title" class="title" id="ha-wa-dialog-title"> ${this.headerTitle} </span>`:r.qy`<slot name="headerTitle" slot="title"></slot>`} ${void 0!==this.headerSubtitle?r.qy`<span slot="subtitle">${this.headerSubtitle}</span>`:r.qy`<slot name="headerSubtitle" slot="subtitle"></slot>`} <slot name="headerActionItems" slot="actionItems"></slot> </ha-dialog-header> </slot> <div class="content-wrapper"> <div class="body ha-scrollbar" @scroll="${this._handleBodyScroll}"> <slot></slot> </div> ${this.renderScrollableFades()} </div> <slot name="footer" slot="footer"></slot> </wa-dialog> `}disconnectedCallback(){super.disconnectedCallback(),this._open=!1}_handleBodyScroll(e){this._bodyScrolled=e.target.scrollTop>0}static get styles(){return[...super.styles,c.dp,r.AH`
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
      `]}constructor(...e){super(...e),this.open=!1,this.type="standard",this.width="medium",this.preventScrimClose=!1,this.headerSubtitlePosition="below",this.flexContent=!1,this._open=!1,this._bodyScrolled=!1,this._handleShow=async()=>{this._open=!0,(0,s.r)(this,"opened"),await this.updateComplete,requestAnimationFrame(()=>{this.querySelector("[autofocus]")?.focus()})},this._handleAfterShow=()=>{(0,s.r)(this,"after-show")},this._handleAfterHide=()=>{this._open=!1,(0,s.r)(this,"closed")}}}(0,o.Cg)([(0,n.MZ)({attribute:!1})],p.prototype,"hass",void 0),(0,o.Cg)([(0,n.MZ)({attribute:"aria-labelledby"})],p.prototype,"ariaLabelledBy",void 0),(0,o.Cg)([(0,n.MZ)({attribute:"aria-describedby"})],p.prototype,"ariaDescribedBy",void 0),(0,o.Cg)([(0,n.MZ)({type:Boolean,reflect:!0})],p.prototype,"open",void 0),(0,o.Cg)([(0,n.MZ)({reflect:!0})],p.prototype,"type",void 0),(0,o.Cg)([(0,n.MZ)({type:String,reflect:!0,attribute:"width"})],p.prototype,"width",void 0),(0,o.Cg)([(0,n.MZ)({type:Boolean,reflect:!0,attribute:"prevent-scrim-close"})],p.prototype,"preventScrimClose",void 0),(0,o.Cg)([(0,n.MZ)({attribute:"header-title"})],p.prototype,"headerTitle",void 0),(0,o.Cg)([(0,n.MZ)({attribute:"header-subtitle"})],p.prototype,"headerSubtitle",void 0),(0,o.Cg)([(0,n.MZ)({type:String,attribute:"header-subtitle-position"})],p.prototype,"headerSubtitlePosition",void 0),(0,o.Cg)([(0,n.MZ)({type:Boolean,reflect:!0,attribute:"flexcontent"})],p.prototype,"flexContent",void 0),(0,o.Cg)([(0,n.wk)()],p.prototype,"_open",void 0),(0,o.Cg)([(0,n.P)(".body")],p.prototype,"bodyContainer",void 0),(0,o.Cg)([(0,n.wk)()],p.prototype,"_bodyScrolled",void 0),(0,o.Cg)([(0,n.Ls)({passive:!0})],p.prototype,"_handleBodyScroll",null),p=(0,o.Cg)([(0,n.EM)("ha-wa-dialog")],p),t()}catch(e){t(e)}})},31420(e,t,a){a.a(e,async function(e,o){try{a.d(t,{Bi:()=>L,Dt:()=>X,EB:()=>D,IW:()=>z,P_:()=>C,SG:()=>$,Sx:()=>Y,T2:()=>v,Xm:()=>y,Ye:()=>b,Zm:()=>M,cq:()=>J,dH:()=>A,en:()=>V,gb:()=>_,gv:()=>E,jU:()=>Z,kI:()=>T,mF:()=>F,mu:()=>S,oJ:()=>B,pI:()=>x,pL:()=>j,q5:()=>P,q7:()=>I,qk:()=>f,sp:()=>U,uM:()=>N,v3:()=>q,xN:()=>G,yL:()=>w,yj:()=>W,zZ:()=>k});a(16573),a(78100),a(77936),a(18111),a(22489),a(20116),a(7588),a(61701),a(37467),a(44732),a(79577),a(41549),a(49797),a(49631),a(35623),a(14603),a(47566),a(98721);var i=a(22711),r=a(97732),n=a(6226),l=a(22786),s=a(80785),d=a(95747),c=a(30162),h=a(36918),u=a(30039),p=a(39889),m=a(95350),g=e([i,d,c]);[i,d,c]=g.then?(await g)():g;var f=function(e){return e.NEVER="never",e.DAILY="daily",e.CUSTOM_DAYS="custom_days",e}({});const v=["mon","tue","wed","thu","fri","sat","sun"],b=e=>e.sort((e,t)=>v.indexOf(e)-v.indexOf(t)),y=e=>e.callWS({type:"backup/config/info"}),_=(e,t)=>e.callWS({type:"backup/config/update",...t}),w=(e,t,a)=>`/api/backup/download/${e}?agent_id=${t}${a?`&password=${a}`:""}`,x=e=>e.callWS({type:"backup/info"}),k=(e,t)=>e.callWS({type:"backup/details",backup_id:t}),C=e=>e.callWS({type:"backup/agents/info"}),S=(e,t)=>e.callWS({type:"backup/delete",backup_id:t}),$=(e,t)=>e.callWS({type:"backup/generate",...t}),z=e=>e.callWS({type:"backup/generate_with_automatic_settings"}),A=(e,t)=>e.callWS({type:"backup/restore",...t}),T=async(e,t,a)=>{const o=new FormData;o.append("file",t);const i=new URLSearchParams;return a.forEach(e=>{i.append("agent_id",e)}),(0,p.QE)(e.fetchWithAuth(`/api/backup/upload?${i.toString()}`,{method:"POST",body:o}))},D=e=>{const t=e.find(L);if(t)return t;const a=e.find(Z);return a||e[0]},M=(e,t,a,o)=>e.callWS({type:"backup/can_decrypt_on_download",backup_id:t,agent_id:a,password:o}),E="backup.local",F="hassio.local",B="cloud.cloud",L=e=>[E,F].includes(e),Z=e=>{const[t,a]=e.split(".");return"hassio"===t&&"local"!==a},I=(e,t,a)=>{if(L(t))return e("ui.panel.config.backup.agents.local_agent");const o=a.find(e=>e.agent_id===t),i=t.split(".")[0],r=o?o.name:t.split(".")[1];if(Z(t))return r;const n=(0,m.p$)(e,i);return a.filter(e=>e.agent_id.split(".")[0]===i).length>1?`${n}: ${r}`:n},q=e=>Math.max(...Object.values(e.agents).map(e=>e.size)),H=["automatic","addon_update","manual"],P=(0,i.z)(e=>e?H:H.filter(e=>"addon_update"!==e)),U=(e,t)=>e.with_automatic_settings?"automatic":t&&null!=e.extra_metadata?.["supervisor.addon_update"]?"addon_update":"manual",W=(e,t)=>{const a=L(e),o=L(t),i=Z(e),r=Z(t),n=(e,t)=>e?1:t?2:3,l=n(a,i),s=n(o,r);return l!==s?l-s:e.localeCompare(t)},J=()=>{const e="ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",t="xxxx-xxxx-xxxx-xxxx-xxxx-xxxx-xxxx";let a="";const o=new Uint8Array(34);return crypto.getRandomValues(o),o.forEach((o,i)=>{a+="-"===t[i]?"-":e[o%36]}),a},R=(e,t)=>"data:text/plain;charset=utf-8,"+encodeURIComponent(`${e.localize("ui.panel.config.backup.emergency_kit_file.title")}\n\n${e.localize("ui.panel.config.backup.emergency_kit_file.description")}\n\n${e.localize("ui.panel.config.backup.emergency_kit_file.date")} ${(0,d.r6)(new Date,e.locale,e.config)}\n\n${e.localize("ui.panel.config.backup.emergency_kit_file.instance")}\n${e.config.location_name}\n\n${e.localize("ui.panel.config.backup.emergency_kit_file.url")}\n${e.auth.data.hassUrl}\n\n${e.localize("ui.panel.config.backup.emergency_kit_file.encryption_key")}\n${t}\n\n${e.localize("ui.panel.config.backup.emergency_kit_file.more_info",{link:(0,h.o)(e,"/more-info/backup-emergency-kit")})}`),O=(e,t)=>`home_assistant_backup_emergency_kit_${t?`${t}_`:""}${(0,d.GH)(new Date,e.locale,e.config).replace(",","").replace(" ","_")}.txt`,Y=(e,t,a)=>(0,u.R)(R(e,t),O(e,a)),N=(0,r.g)((0,n.a)(new Date,4),45),j=(0,r.g)((0,n.a)(new Date,5),45),V=(0,l.A)((e,t,a)=>{if((0,s.A)(a))return(0,c.fU)(a,e,t);if("string"==typeof a&&a){const o=a.split(":"),i=(0,r.g)((0,n.a)(new Date,parseInt(o[0])),parseInt(o[1]));return(0,c.fU)(i,e,t)}return`${(0,c.fU)(N,e,t)} - ${(0,c.fU)(j,e,t)}`}),G="application/x-tar",X={file:void 0};o()}catch(e){o(e)}})},26581(e,t,a){a.d(t,{r:()=>i,y:()=>o});const o=async e=>e.callWS({type:"hassio/update/config/info"}),i=async(e,t)=>e.callWS({type:"hassio/update/config/update",...t})},59992(e,t,a){a.d(t,{V:()=>s});var o=a(62826),i=a(88696),r=a(96196),n=a(94333),l=a(44457);const s=e=>{class t extends e{get scrollableElement(){return t.DEFAULT_SCROLLABLE_ELEMENT}firstUpdated(e){super.firstUpdated?.(e),this.scrollableElement&&this._updateScrollableState(this.scrollableElement),this._attachScrollableElement()}updated(e){super.updated?.(e),this._attachScrollableElement()}disconnectedCallback(){this._detachScrollableElement(),this._contentScrolled=!1,this._contentScrollable=!1,super.disconnectedCallback()}renderScrollableFades(e=!1){return r.qy` <div class="${(0,n.H)({"fade-top":!0,rounded:e,visible:this._contentScrolled})}"></div> <div class="${(0,n.H)({"fade-bottom":!0,rounded:e,visible:this._contentScrollable})}"></div> `}static get styles(){const e=Object.getPrototypeOf(this);var t;return[...void 0===(t=e?.styles??[])?[]:Array.isArray(t)?t:[t],r.AH`.fade-bottom,.fade-top{position:absolute;left:0;right:0;height:var(--ha-space-2);pointer-events:none;transition:opacity 180ms ease-in-out;border-radius:var(--ha-border-radius-square);opacity:0;background:linear-gradient(to bottom,var(--ha-color-shadow-scrollable-fade),transparent)}.fade-top{top:0}.fade-bottom{bottom:0;transform:rotate(180deg)}.fade-bottom.visible,.fade-top.visible{opacity:1}.fade-bottom.rounded,.fade-top.rounded{border-radius:var(--ha-card-border-radius,var(--ha-border-radius-lg));border-bottom-left-radius:var(--ha-border-radius-square);border-bottom-right-radius:var(--ha-border-radius-square)}.fade-top.rounded{border-top-left-radius:var(--ha-border-radius-square);border-top-right-radius:var(--ha-border-radius-square)}.fade-bottom.rounded{border-bottom-left-radius:var(--ha-border-radius-square);border-bottom-right-radius:var(--ha-border-radius-square)}`]}_attachScrollableElement(){const e=this.scrollableElement;e!==this._scrollTarget&&(this._detachScrollableElement(),e&&(this._scrollTarget=e,e.addEventListener("scroll",this._onScroll,{passive:!0}),this._resize.observe(e),this._updateScrollableState(e)))}_detachScrollableElement(){this._scrollTarget&&(this._scrollTarget.removeEventListener("scroll",this._onScroll),this._resize.unobserve?.(this._scrollTarget),this._scrollTarget=void 0)}_updateScrollableState(e){const t=parseFloat(getComputedStyle(e).getPropertyValue("--safe-area-inset-bottom"))||0,{scrollHeight:a=0,clientHeight:o=0,scrollTop:i=0}=e;this._contentScrollable=a-o>i+t+this.scrollFadeSafeAreaPadding}constructor(...e){super(...e),this._contentScrolled=!1,this._contentScrollable=!1,this._onScroll=e=>{const t=e.currentTarget;this._contentScrolled=(t.scrollTop??0)>this.scrollFadeThreshold,this._updateScrollableState(t)},this._resize=new i.P(this,{target:null,callback:e=>{const t=e[0]?.target;t&&this._updateScrollableState(t)}}),this.scrollFadeSafeAreaPadding=4,this.scrollFadeThreshold=4}}return t.DEFAULT_SCROLLABLE_ELEMENT=null,(0,o.Cg)([(0,l.wk)()],t.prototype,"_contentScrolled",void 0),(0,o.Cg)([(0,l.wk)()],t.prototype,"_contentScrollable",void 0),t}},56588(e,t,a){a.a(e,async function(e,o){try{a.r(t),a.d(t,{DialogLabsPreviewFeatureEnable:()=>g});var i=a(62826),r=a(96196),n=a(44457),l=a(36312),s=a(98975),d=a(1087),c=a(18350),h=(a(93444),a(45331)),u=(a(17308),a(2846),a(59646),a(31420)),p=a(26581),m=e([c,h,u,s]);[c,h,u,s]=m.then?(await m)():m;class g extends r.WF{async showDialog(e){this._params=e,this._createBackup=!1,this._open=!0,this._fetchBackupConfig(),(0,l.x)(this.hass,"hassio")&&this._fetchUpdateBackupConfig()}closeDialog(){return this._open=!1,!0}_dialogClosed(){this._params=void 0,this._backupConfig=void 0,this._createBackup=!1,(0,d.r)(this,"dialog-closed",{dialog:this.localName})}async _fetchBackupConfig(){try{const{config:e}=await(0,u.Xm)(this.hass);this._backupConfig=e}catch(e){console.error(e)}}async _fetchUpdateBackupConfig(){try{const e=await(0,p.y)(this.hass);this._createBackup=e.core_backup_before_update}catch(e){console.error(e)}}_computeCreateBackupTexts(){if(!this._backupConfig||!this._backupConfig.automatic_backups_configured||!this._backupConfig.create_backup.password||0===this._backupConfig.create_backup.agent_ids.length)return{title:this.hass.localize("ui.panel.config.labs.create_backup.manual"),description:this.hass.localize("ui.panel.config.labs.create_backup.manual_description")};const e=this._backupConfig.last_completed_automatic_backup?new Date(this._backupConfig.last_completed_automatic_backup):null,t=new Date;return{title:this.hass.localize("ui.panel.config.labs.create_backup.automatic"),description:e?this.hass.localize("ui.panel.config.labs.create_backup.automatic_description_last",{relative_time:(0,s.K)(e,this.hass.locale,t,!0)}):this.hass.localize("ui.panel.config.labs.create_backup.automatic_description_none")}}_createBackupChanged(e){this._createBackup=e.target.checked}_handleCancel(){this.closeDialog()}_handleConfirm(){this._params&&this._params.onConfirm(this._createBackup),this.closeDialog()}render(){if(!this._params)return r.s6;const e=this._computeCreateBackupTexts();return r.qy` <ha-wa-dialog .hass="${this.hass}" .open="${this._open}" header-title="${this.hass.localize("ui.panel.config.labs.enable_title")}" @closed="${this._dialogClosed}"> <p> ${this.hass.localize(`component.${this._params.preview_feature.domain}.preview_features.${this._params.preview_feature.preview_feature}.enable_confirmation`)||this.hass.localize("ui.panel.config.labs.enable_confirmation")} </p> ${e?r.qy` <ha-md-list> <ha-md-list-item> <span slot="headline">${e.title}</span> ${e.description?r.qy` <span slot="supporting-text"> ${e.description} </span> `:r.s6} <ha-switch slot="end" .checked="${this._createBackup}" @change="${this._createBackupChanged}"></ha-switch> </ha-md-list-item> </ha-md-list> `:r.s6} <ha-dialog-footer slot="footer"> <ha-button slot="secondaryAction" appearance="plain" @click="${this._handleCancel}"> ${this.hass.localize("ui.common.cancel")} </ha-button> <ha-button slot="primaryAction" appearance="filled" variant="brand" @click="${this._handleConfirm}"> ${this.hass.localize("ui.panel.config.labs.enable")} </ha-button> </ha-dialog-footer> </ha-wa-dialog> `}constructor(...e){super(...e),this._createBackup=!1,this._open=!1}}g.styles=r.AH`ha-wa-dialog{--dialog-content-padding:0}p{margin:0 var(--ha-space-6) var(--ha-space-6);color:var(--secondary-text-color)}ha-md-list{background:0 0;--md-list-item-leading-space:var(--ha-space-6);--md-list-item-trailing-space:var(--ha-space-6);margin:0;padding:0;border-top:var(--ha-border-width-sm) solid var(--divider-color)}`,(0,i.Cg)([(0,n.MZ)({attribute:!1})],g.prototype,"hass",void 0),(0,i.Cg)([(0,n.wk)()],g.prototype,"_params",void 0),(0,i.Cg)([(0,n.wk)()],g.prototype,"_backupConfig",void 0),(0,i.Cg)([(0,n.wk)()],g.prototype,"_createBackup",void 0),(0,i.Cg)([(0,n.wk)()],g.prototype,"_open",void 0),g=(0,i.Cg)([(0,n.EM)("dialog-labs-preview-feature-enable")],g),o()}catch(e){o(e)}})},30039(e,t,a){a.d(t,{R:()=>i,h:()=>r});var o=a(22348);const i=(e,t="")=>{const a=document.createElement("a");a.target="_blank",a.href=e,a.download=t,a.style.display="none",document.body.appendChild(a),a.dispatchEvent(new MouseEvent("click")),document.body.removeChild(a)},r=e=>!(0,o.V)(e)||!!e.auth.external?.config.downloadFileSupported},22348(e,t,a){a.d(t,{V:()=>i});var o=a(37177);const i=e=>!!e.auth.external&&o.n},37177(e,t,a){a.d(t,{n:()=>o});const o=/^((?!chrome|android).)*safari/i.test(navigator.userAgent)}};
//# sourceMappingURL=7901.28d285d36f5c7144.js.map