"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([["54074"],{20058:function(a,t,e){e.a(a,async function(a,o){try{e.d(t,{QL:function(){return d},ZQ:function(){return p},ZV:function(){return c},ty:function(){return l},x:function(){return s}});var i=e(74487),r=(e(74423),e(18111),e(61701),e(46927)),n=a([i]);i=(n.then?(await n)():n)[0];const s=a=>l(a.attributes),l=(a,t)=>!!a.unit_of_measurement||!!a.state_class||(t||[]).includes(a.device_class||""),h=a=>{switch(a.number_format){case r.jG.comma_decimal:return["en-US","en"];case r.jG.decimal_comma:return["de","es","it"];case r.jG.space_comma:return["fr","sv","cs"];case r.jG.quote_decimal:return["de-CH"];case r.jG.system:return;default:return a.language}},c=(a,t,e)=>d(a,t,e).map(a=>a.value).join(""),d=(a,t,e)=>{const o=t?h(t):void 0;return Number.isNaN=Number.isNaN||function a(t){return"number"==typeof t&&a(t)},(null==t?void 0:t.number_format)===r.jG.none||Number.isNaN(Number(a))?Number.isNaN(Number(a))||""===a||(null==t?void 0:t.number_format)!==r.jG.none?[{type:"literal",value:a}]:new Intl.NumberFormat("en-US",m(a,Object.assign(Object.assign({},e),{},{useGrouping:!1}))).formatToParts(Number(a)):new Intl.NumberFormat(o,m(a,e)).formatToParts(Number(a))},p=(a,t)=>{var e;const o=null==t?void 0:t.display_precision;return null!=o?{maximumFractionDigits:o,minimumFractionDigits:o}:Number.isInteger(Number(null==a||null===(e=a.attributes)||void 0===e?void 0:e.step))&&Number.isInteger(Number(null==a?void 0:a.state))?{maximumFractionDigits:0}:void 0},m=(a,t)=>{const e=Object.assign({maximumFractionDigits:2},t);if("string"!=typeof a)return e;if(!t||void 0===t.minimumFractionDigits&&void 0===t.maximumFractionDigits){const t=a.indexOf(".")>-1?a.split(".")[1].length:0;e.minimumFractionDigits=t,e.maximumFractionDigits=t}return e};o()}catch(s){o(s)}})},26300:function(a,t,e){e.a(a,async function(a,o){try{e.r(t),e.d(t,{HaIconButton:function(){return g}});e(62953);var i=e(40445),r=e(96196),n=e(77845),s=e(32288),l=e(18350),h=(e(67094),a([l]));l=(h.then?(await h)():h)[0];let c,d,p,m,u=a=>a;class g extends r.WF{render(){return(0,r.qy)(c||(c=u` <ha-button appearance="plain" variant="neutral" aria-label="${0}" title="${0}" aria-haspopup="${0}" .disabled="${0}" .iconTag="${0}" .href="${0}" .target="${0}" .rel="${0}" .download="${0}"> ${0} </ha-button> `),(0,s.J)(this.label),(0,s.J)(this.hideTitle?void 0:this.label),(0,s.J)(this.ariaHasPopup),this.disabled,this.path?"ha-svg-icon":"span",this.href,this.target,this.rel,this.download,this.path?(0,r.qy)(d||(d=u`<ha-svg-icon .path="${0}"></ha-svg-icon>`),this.path):(0,r.qy)(p||(p=u`<span><slot></slot></span>`)))}constructor(...a){super(...a),this.disabled=!1,this.hideTitle=!1,this.selected=!1}}g.shadowRootOptions={mode:"open",delegatesFocus:!0},g.styles=(0,r.AH)(m||(m=u`:host{display:inline-block;outline:0;--ha-button-height:var(--ha-icon-button-size, 48px)}ha-button{position:relative;isolation:isolate;--wa-form-control-padding-inline:var(
        --ha-icon-button-padding-inline,
        --ha-space-2
      );--wa-color-on-normal:currentColor;--wa-color-fill-quiet:transparent;--ha-button-label-overflow:visible}ha-button::after{content:"";position:absolute;inset:0;z-index:-1;border-radius:50%;background-color:currentColor;opacity:0;pointer-events:none}ha-button::part(base){width:var(--wa-form-control-height);aspect-ratio:1;outline-offset:-4px}ha-button::part(label){display:flex}:host([selected]) ha-button::after{opacity:.1}@media (hover:hover){:host(:hover:not([disabled])) ha-button::after{opacity:.1}}`)),(0,i.Cg)([(0,n.MZ)({type:Boolean,reflect:!0})],g.prototype,"disabled",void 0),(0,i.Cg)([(0,n.MZ)({type:String})],g.prototype,"path",void 0),(0,i.Cg)([(0,n.MZ)({type:String})],g.prototype,"label",void 0),(0,i.Cg)([(0,n.MZ)({type:String,attribute:"aria-haspopup"})],g.prototype,"ariaHasPopup",void 0),(0,i.Cg)([(0,n.MZ)({attribute:"hide-title",type:Boolean})],g.prototype,"hideTitle",void 0),(0,i.Cg)([(0,n.MZ)({type:Boolean,reflect:!0})],g.prototype,"selected",void 0),(0,i.Cg)([(0,n.MZ)()],g.prototype,"href",void 0),(0,i.Cg)([(0,n.MZ)()],g.prototype,"target",void 0),(0,i.Cg)([(0,n.MZ)()],g.prototype,"rel",void 0),(0,i.Cg)([(0,n.MZ)()],g.prototype,"download",void 0),g=(0,i.Cg)([(0,n.EM)("ha-icon-button")],g),o()}catch(c){o(c)}})},2846:function(a,t,e){e.d(t,{G:function(){return p},J:function(){return d}});var o=e(40445),i=e(12415),r=e(82553),n=e(96196),s=e(77845);e(54276);let l,h,c=a=>a;const d=[r.R,(0,n.AH)(l||(l=c`:host{--ha-icon-display:block;--md-sys-color-primary:var(--primary-text-color);--md-sys-color-secondary:var(--secondary-text-color);--md-sys-color-surface:var(--card-background-color);--md-sys-color-on-surface:var(--primary-text-color);--md-sys-color-on-surface-variant:var(--secondary-text-color)}md-item{overflow:var(--md-item-overflow,hidden);align-items:var(--md-item-align-items,center);gap:var(--ha-md-list-item-gap,16px)}`))];class p extends i.n{renderRipple(){return"text"===this.type?n.s6:(0,n.qy)(h||(h=c`<ha-ripple part="ripple" for="item" ?disabled="${0}"></ha-ripple>`),this.disabled&&"link"!==this.type)}}p.styles=d,p=(0,o.Cg)([(0,s.EM)("ha-md-list-item")],p)},17308:function(a,t,e){var o=e(40445),i=e(49838),r=e(11245),n=e(96196),s=e(77845);let l;class h extends i.B{}h.styles=[r.R,(0,n.AH)(l||(l=(a=>a)`:host{--md-sys-color-surface:var(--card-background-color)}`))],h=(0,o.Cg)([(0,s.EM)("ha-md-list")],h)},54276:function(a,t,e){e(62953);var o=e(40445),i=e(76482),r=e(91382),n=e(96245),s=e(96196),l=e(77845);let h;class c extends r.n{attach(a){super.attach(a),this.attachableTouchController.attach(a)}disconnectedCallback(){super.disconnectedCallback(),this.hovered=!1,this.pressed=!1}detach(){super.detach(),this.attachableTouchController.detach()}_onTouchControlChange(a,t){null==a||a.removeEventListener("touchend",this._handleTouchEnd),null==t||t.addEventListener("touchend",this._handleTouchEnd)}constructor(...a){super(...a),this.attachableTouchController=new i.i(this,this._onTouchControlChange.bind(this)),this._handleTouchEnd=()=>{this.disabled||super.endPressAnimation()}}}c.styles=[n.R,(0,s.AH)(h||(h=(a=>a)`:host{--md-ripple-hover-opacity:var(--ha-ripple-hover-opacity, 0.08);--md-ripple-pressed-opacity:var(--ha-ripple-pressed-opacity, 0.12);--md-ripple-hover-color:var(
          --ha-ripple-hover-color,
          var(--ha-ripple-color, var(--secondary-text-color))
        );--md-ripple-pressed-color:var(
          --ha-ripple-pressed-color,
          var(--ha-ripple-color, var(--secondary-text-color))
        )}`))],c=(0,o.Cg)([(0,l.EM)("ha-ripple")],c)},67094:function(a,t,e){e.r(t),e.d(t,{HaSvgIcon:function(){return d}});var o=e(40445),i=e(96196),r=e(77845);let n,s,l,h,c=a=>a;class d extends i.WF{render(){return(0,i.JW)(n||(n=c` <svg viewBox="${0}" preserveAspectRatio="xMidYMid meet" focusable="false" role="img" aria-hidden="true"> <g> ${0} ${0} </g> </svg>`),this.viewBox||"0 0 24 24",this.path?(0,i.JW)(s||(s=c`<path class="primary-path" d="${0}"></path>`),this.path):i.s6,this.secondaryPath?(0,i.JW)(l||(l=c`<path class="secondary-path" d="${0}"></path>`),this.secondaryPath):i.s6)}}d.styles=(0,i.AH)(h||(h=c`:host{display:var(--ha-icon-display,inline-flex);align-items:center;justify-content:center;position:relative;vertical-align:middle;fill:var(--icon-primary-color,currentcolor);width:var(--mdc-icon-size,24px);height:var(--mdc-icon-size,24px)}svg{width:100%;height:100%;pointer-events:none;display:block}path.primary-path{opacity:var(--icon-primary-opactity, 1)}path.secondary-path{fill:var(--icon-secondary-color,currentcolor);opacity:var(--icon-secondary-opactity, .5)}`)),(0,o.Cg)([(0,r.MZ)()],d.prototype,"path",void 0),(0,o.Cg)([(0,r.MZ)({attribute:!1})],d.prototype,"secondaryPath",void 0),(0,o.Cg)([(0,r.MZ)({attribute:!1})],d.prototype,"viewBox",void 0),d=(0,o.Cg)([(0,r.EM)("ha-svg-icon")],d)},44249:function(a,t,e){e.d(t,{V:function(){return o}});e(62953);const o=(a,t)=>{const e=new i,o=a.subscribeMessage(a=>t(e.processMessage(a)),{type:"persistent_notification/subscribe"});return()=>{o.then(a=>null==a?void 0:a())}};class i{processMessage(a){if("removed"===a.type)for(const t of Object.keys(a.notifications))delete this.notifications[t];else this.notifications=Object.assign(Object.assign({},this.notifications),a.notifications);return Object.values(this.notifications)}constructor(){this.notifications={}}}},68302:function(a,t,e){e.d(t,{w:function(){return r}});e(3362),e(62953);var o=e(1087);const i=()=>Promise.all([e.e("87272"),e.e("30628"),e.e("34995"),e.e("46995"),e.e("66878"),e.e("33337"),e.e("11345")]).then(e.bind(e,93576)),r=a=>{(0,o.r)(a,"show-dialog",{dialogTag:"dialog-edit-sidebar",dialogImport:i,dialogParams:{}})}},69235:function(a,t,e){e.a(a,async function(a,t){try{e(3362),e(62953);"function"!=typeof window.ResizeObserver&&(window.ResizeObserver=(await e.e("71055").then(e.bind(e,52370))).default),t()}catch(o){t(o)}},1)},14503:function(a,t,e){e.d(t,{RF:function(){return p},dp:function(){return g},kO:function(){return u},nA:function(){return m},og:function(){return d}});var o=e(96196);let i,r,n,s,l,h,c=a=>a;const d=(0,o.AH)(i||(i=c`button.link{background:0 0;color:inherit;border:none;padding:0;font:inherit;text-align:left;text-decoration:underline;cursor:pointer;outline:0}`)),p=(0,o.AH)(r||(r=c`:host{font-family:var(--ha-font-family-body);-webkit-font-smoothing:var(--ha-font-smoothing);-moz-osx-font-smoothing:var(--ha-moz-osx-font-smoothing);font-size:var(--ha-font-size-m);font-weight:var(--ha-font-weight-normal);line-height:var(--ha-line-height-normal)}app-header div[sticky]{height:48px}app-toolbar [main-title]{margin-left:20px;margin-inline-start:20px;margin-inline-end:initial}.header{transition:box-shadow .2s linear,width var(--ha-animation-duration-normal) ease,padding-left var(--ha-animation-duration-normal) ease,padding-right var(--ha-animation-duration-normal) ease}@media (prefers-reduced-motion:reduce){.header{transition:box-shadow .2s linear}}h1{font-family:var(--ha-font-family-heading);-webkit-font-smoothing:var(--ha-font-smoothing);-moz-osx-font-smoothing:var(--ha-moz-osx-font-smoothing);font-size:var(--ha-font-size-2xl);font-weight:var(--ha-font-weight-normal);line-height:var(--ha-line-height-condensed)}h2{font-family:var(--ha-font-family-body);-webkit-font-smoothing:var(--ha-font-smoothing);-moz-osx-font-smoothing:var(--ha-moz-osx-font-smoothing);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;font-size:var(--ha-font-size-xl);font-weight:var(--ha-font-weight-medium);line-height:var(--ha-line-height-normal)}h3{font-family:var(--ha-font-family-body);-webkit-font-smoothing:var(--ha-font-smoothing);-moz-osx-font-smoothing:var(--ha-moz-osx-font-smoothing);font-size:var(--ha-font-size-l);font-weight:var(--ha-font-weight-normal);line-height:var(--ha-line-height-normal)}a{color:var(--primary-color)}.secondary{color:var(--secondary-text-color)}.error{color:var(--error-color)}.warning{color:var(--error-color)}${0} .card-actions a{text-decoration:none}.card-actions .warning{--mdc-theme-primary:var(--error-color)}.layout.horizontal,.layout.vertical{display:flex}.layout.inline{display:inline-flex}.layout.horizontal{flex-direction:row}.layout.vertical{flex-direction:column}.layout.wrap{flex-wrap:wrap}.layout.no-wrap{flex-wrap:nowrap}.layout.center,.layout.center-center{align-items:center}.layout.bottom{align-items:flex-end}.layout.center-center,.layout.center-justified{justify-content:center}.flex{flex:1;flex-basis:0.000000001px}.flex-auto{flex:1 1 auto}.flex-none{flex:none}.layout.justified{justify-content:space-between}`),d),m=(0,o.AH)(n||(n=c`
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
`)),u=(0,o.AH)(s||(s=c`ha-adaptive-dialog,ha-dialog{--vertical-align-dialog:flex-start;--dialog-surface-margin-top:var(--ha-space-10);--mdc-dialog-max-height:calc(
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
    )}@media all and (max-width:450px),all and (max-height:500px){ha-adaptive-dialog,ha-dialog{--dialog-surface-margin-top:0px;--mdc-dialog-min-height:100vh;--mdc-dialog-min-height:100svh;--mdc-dialog-max-height:100vh;--mdc-dialog-max-height:100svh;--ha-dialog-max-height:100vh;--ha-dialog-max-height:100svh}}`)),g=(0,o.AH)(l||(l=c`.ha-scrollbar::-webkit-scrollbar{width:.4rem;height:.4rem}.ha-scrollbar::-webkit-scrollbar-thumb{border-radius:var(--ha-border-radius-sm);background:var(--scrollbar-thumb-color)}.ha-scrollbar{overflow-y:auto;scrollbar-color:var(--scrollbar-thumb-color) transparent;scrollbar-width:thin}`));(0,o.AH)(h||(h=c`body{background-color:var(--primary-background-color);color:var(--primary-text-color);height:calc(100vh - 32px);width:100vw}`))},88438:function(a,t,e){e.d(t,{C:function(){return o}});const o="ontouchstart"in window||navigator.maxTouchPoints>0||navigator.msMaxTouchPoints>0}}]);
//# sourceMappingURL=54074.11aa33c37794474e.js.map