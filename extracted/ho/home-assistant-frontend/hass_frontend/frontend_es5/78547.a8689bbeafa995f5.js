"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([["78547"],{50248:function(t,a,e){e.d(a,{n:function(){return n}});const n=(t=document)=>{var a;return null!==(a=t.activeElement)&&void 0!==a&&null!==(a=a.shadowRoot)&&void 0!==a&&a.activeElement?n(t.activeElement.shadowRoot):t.activeElement}},91926:function(t,a,e){e.d(a,{O:function(){return s},o:function(){return l}});e(3362),e(27495),e(25440);var n=e(22444),o=e(1087),i=e(63091);const r=async t=>{var a;const{history:e}=i.G;if(null===(a=e.state)||void 0===a||!a.dialog||Date.now()-t>=500)return!0;return await(0,n.Jh)()?(await new Promise(t=>{setTimeout(t)}),r(t)):(console.warn("Navigation blocked, because dialog refused to close"),!1)},l=async(t,a)=>{if(!(await r(Date.now())))return!1;const e=(null==a?void 0:a.replace)||!1;var n,l,s;return e?i.G.history.replaceState(null!==(n=i.G.history.state)&&void 0!==n&&n.root?{root:!0}:null!==(l=null==a?void 0:a.data)&&void 0!==l?l:null,"",t):i.G.history.pushState(null!==(s=null==a?void 0:a.data)&&void 0!==s?s:null,"",t),(0,o.r)(i.G,"location-changed",{replace:e}),!0},s=async t=>{if(!(await r(Date.now())))return;const{history:a}=i.G;if(a.length>1)return void a.back();l(t||"/",{replace:!0})}},12587:function(t,a,e){e.d(a,{E:function(){return o},m:function(){return n}});e(3362);const n=t=>{requestAnimationFrame(()=>setTimeout(t,0))},o=()=>new Promise(t=>{n(t)})},2846:function(t,a,e){e.d(a,{G:function(){return u},J:function(){return h}});var n=e(40445),o=e(12415),i=e(82553),r=e(96196),l=e(77845);e(54276);let s,d,c=t=>t;const h=[i.R,(0,r.AH)(s||(s=c`:host{--ha-icon-display:block;--md-sys-color-primary:var(--primary-text-color);--md-sys-color-secondary:var(--secondary-text-color);--md-sys-color-surface:var(--card-background-color);--md-sys-color-on-surface:var(--primary-text-color);--md-sys-color-on-surface-variant:var(--secondary-text-color)}md-item{overflow:var(--md-item-overflow,hidden);align-items:var(--md-item-align-items,center);gap:var(--ha-md-list-item-gap,16px)}`))];class u extends o.n{renderRipple(){return"text"===this.type?r.s6:(0,r.qy)(d||(d=c`<ha-ripple part="ripple" for="item" ?disabled="${0}"></ha-ripple>`),this.disabled&&"link"!==this.type)}}u.styles=h,u=(0,n.Cg)([(0,l.EM)("ha-md-list-item")],u)},54276:function(t,a,e){e(62953);var n=e(40445),o=e(76482),i=e(91382),r=e(96245),l=e(96196),s=e(77845);let d;class c extends i.n{attach(t){super.attach(t),this.attachableTouchController.attach(t)}disconnectedCallback(){super.disconnectedCallback(),this.hovered=!1,this.pressed=!1}detach(){super.detach(),this.attachableTouchController.detach()}_onTouchControlChange(t,a){null==t||t.removeEventListener("touchend",this._handleTouchEnd),null==a||a.addEventListener("touchend",this._handleTouchEnd)}constructor(...t){super(...t),this.attachableTouchController=new o.i(this,this._onTouchControlChange.bind(this)),this._handleTouchEnd=()=>{this.disabled||super.endPressAnimation()}}}c.styles=[r.R,(0,l.AH)(d||(d=(t=>t)`:host{--md-ripple-hover-opacity:var(--ha-ripple-hover-opacity, 0.08);--md-ripple-pressed-opacity:var(--ha-ripple-pressed-opacity, 0.12);--md-ripple-hover-color:var(
          --ha-ripple-hover-color,
          var(--ha-ripple-color, var(--secondary-text-color))
        );--md-ripple-pressed-color:var(
          --ha-ripple-pressed-color,
          var(--ha-ripple-color, var(--secondary-text-color))
        )}`))],c=(0,n.Cg)([(0,s.EM)("ha-ripple")],c)},59241:function(t,a,e){e.d(a,{BM:function(){return T},Bz:function(){return b},DW:function(){return h},Er:function(){return c},G3:function(){return m},G_:function(){return f},Ox:function(){return _},P9:function(){return k},RP:function(){return y},bg:function(){return p},jh:function(){return u},n4:function(){return x},v:function(){return g}});e(74423),e(26910),e(18111),e(22489),e(20116),e(62953);var n=e(70570),o=e(22786),i=e(71727),r=e(28978),l=e(52220),s=e(9899);const d=["sensor","binary_sensor"],c=(t,a)=>{const e=a.filter(a=>t.states[a.entity_id]&&"battery"===t.states[a.entity_id].attributes.device_class&&d.includes((0,i.m)(a.entity_id))).sort((t,a)=>d.indexOf((0,i.m)(t.entity_id))-d.indexOf((0,i.m)(a.entity_id)));if(e.length>0)return e[0]},h=(t,a)=>a.find(a=>t.states[a.entity_id]&&"battery_charging"===t.states[a.entity_id].attributes.device_class),u=(t,a)=>{if(a.name)return a.name;const e=t.states[a.entity_id];return e?(0,r.u)(e):a.original_name?a.original_name:a.entity_id},g=(t,a)=>t.callWS({type:"config/entity_registry/get",entity_id:a}),m=(t,a)=>t.callWS({type:"config/entity_registry/get_entries",entity_ids:a}),f=(t,a,e)=>t.callWS(Object.assign({type:"config/entity_registry/update",entity_id:a},e)),p=(t,a)=>t.callWS({type:"config/entity_registry/remove",entity_id:a}),v=t=>t.sendMessagePromise({type:"config/entity_registry/list"}),y=t=>t.sendMessagePromise({type:"config/entity_registry/list_for_display"}),w=(t,a)=>t.subscribeEvents((0,s.s)(()=>v(t).then(t=>a.setState(t,!0)),500,!0),"entity_registry_updated"),b=(t,a)=>(0,n.N)("_entityRegistry",v,w,t,a),x=(t,a)=>t.sort((t,e)=>(0,l.SH)(t.name||"",e.name||"",a)),_=(0,o.A)(t=>{const a={};for(const e of t)a[e.entity_id]=e;return a}),k=(0,o.A)(t=>{const a={};for(const e of t)a[e.id]=e;return a}),T=(t,a)=>t.callWS({type:"config/entity_registry/get_automatic_entity_ids",entity_ids:a})},65063:function(t,a,e){e.d(a,{an:function(){return s},dk:function(){return l},showAlertDialog:function(){return r}});e(3362),e(62953);var n=e(1087);const o=()=>Promise.all([e.e("31065"),e.e("93754"),e.e("42310")]).then(e.bind(e,26683)),i=(t,a,e)=>new Promise(i=>{const r=a.cancel,l=a.confirm;(0,n.r)(t,"show-dialog",{dialogTag:"dialog-box",dialogImport:o,dialogParams:Object.assign(Object.assign(Object.assign({},a),e),{},{cancel:()=>{i(!(null==e||!e.prompt)&&null),r&&r()},confirm:t=>{i(null==e||!e.prompt||t),l&&l(t)}})})}),r=(t,a)=>i(t,a),l=(t,a)=>i(t,a,{confirmation:!0}),s=(t,a)=>i(t,a,{prompt:!0})},22444:function(t,a,e){e.d(a,{oO:function(){return f},t3:function(){return u},zU:function(){return h},Jh:function(){return g},ui:function(){return c}});e(44114),e(3362),e(62953),e(17642),e(58004),e(33853),e(45876),e(32475),e(15024),e(31698);const n=(t,a,e=true)=>{var o;if(!t||t===document.body)return null;if((t=null!==(o=t.assignedSlot)&&void 0!==o?o:t).parentElement)t=t.parentElement;else{const a=t.getRootNode();t=a instanceof ShadowRoot?a.host:null}return(e?Object.prototype.hasOwnProperty.call(t,a):t&&a in t)?t:n(t,a,e)};if(66649!=e.j)var o=e(50248);var i=e(63091),r=e(12587);const l={},s=[],d=Symbol.for("HA focus target"),c=async(t,a,e,r,h,u=!0)=>{if(!(e in l)){if(!h)return!1;l[e]={element:h().then(()=>{const a=document.createElement(e);return t.provideHass(a),a.addEventListener("dialog-closed",m),a.addEventListener("dialog-closed",p),a})}}if(u){var g,f;const{history:n}=i.G;if(null!==(g=n.state)&&void 0!==g&&g.dialog&&!s.length)return await new Promise(t=>{setTimeout(t)}),c(t,a,e,r,h,u);const o=s.findIndex(t=>t.dialogTag===e);-1!==o&&s.splice(o,1),s.push({element:t,root:a,dialogTag:e,dialogParams:r,dialogImport:h,addHistory:u});const l={dialog:e};null!==(f=n.state)&&void 0!==f&&f.dialog?n.replaceState(l,""):(n.replaceState(Object.assign(Object.assign({},n.state),{},{opensDialog:!0}),""),n.pushState(l,""))}l[e].closedFocusTargets=((t,a,e=!0)=>{const o=new Set;for(;t;)o.add(t),t=n(t,a,e);return o})((0,o.n)(),d);const v=await l[e].element;return a.appendChild(v),v.showDialog(r),!0},h=async(t,a)=>{if(!(t in l))return!0;const e=await l[t].element;return!e.closeDialog||!1!==e.closeDialog(a)},u=async t=>{if(s.length){var a;const e=s.pop(),n=await h(e.dialogTag,t);return n?s.length&&null!==(a=i.G.history.state)&&void 0!==a&&a.opensDialog&&i.G.history.pushState({dialog:s[s.length-1].dialogTag},""):s.push(e),n}return!0},g=async()=>{for(let t=s.length-1;t>=0;t--){if(!(!s[t]||await h(s[t].dialogTag)))return!1}return!0},m=t=>{var a;const e=s.findIndex(a=>a.dialogTag===t.detail.dialog);-1!==e&&s.splice(e,1),(null===(a=i.G.history.state)||void 0===a?void 0:a.dialog)===t.detail.dialog&&(s.length?i.G.history.replaceState({dialog:s[s.length-1].dialogTag},""):-1!==e&&i.G.history.back())},f=(t,a)=>{t.addEventListener("show-dialog",e=>{const{dialogTag:n,dialogImport:o,dialogParams:i,addHistory:r}=e.detail;c(t,a,n,i,o,r)})},p=async t=>{if(!l[t.detail.dialog])return;const a=l[t.detail.dialog].closedFocusTargets;if(delete l[t.detail.dialog].closedFocusTargets,!a)return;let e=(0,o.n)();e instanceof HTMLElement&&e.blur(),await(0,r.E)();for(const n of a)if(n instanceof HTMLElement&&(n.focus(),e=(0,o.n)(),e&&e!==document.body))return}},69235:function(t,a,e){e.a(t,async function(t,a){try{e(3362),e(62953);"function"!=typeof window.ResizeObserver&&(window.ResizeObserver=(await e.e("71055").then(e.bind(e,52370))).default),a()}catch(n){a(n)}},1)},14503:function(t,a,e){e.d(a,{RF:function(){return u},dp:function(){return f},kO:function(){return m},nA:function(){return g},og:function(){return h}});var n=e(96196);let o,i,r,l,s,d,c=t=>t;const h=(0,n.AH)(o||(o=c`button.link{background:0 0;color:inherit;border:none;padding:0;font:inherit;text-align:left;text-decoration:underline;cursor:pointer;outline:0}`)),u=(0,n.AH)(i||(i=c`:host{font-family:var(--ha-font-family-body);-webkit-font-smoothing:var(--ha-font-smoothing);-moz-osx-font-smoothing:var(--ha-moz-osx-font-smoothing);font-size:var(--ha-font-size-m);font-weight:var(--ha-font-weight-normal);line-height:var(--ha-line-height-normal)}app-header div[sticky]{height:48px}app-toolbar [main-title]{margin-left:20px;margin-inline-start:20px;margin-inline-end:initial}.header{transition:box-shadow .2s linear,width var(--ha-animation-duration-normal) ease,padding-left var(--ha-animation-duration-normal) ease,padding-right var(--ha-animation-duration-normal) ease}@media (prefers-reduced-motion:reduce){.header{transition:box-shadow .2s linear}}h1{font-family:var(--ha-font-family-heading);-webkit-font-smoothing:var(--ha-font-smoothing);-moz-osx-font-smoothing:var(--ha-moz-osx-font-smoothing);font-size:var(--ha-font-size-2xl);font-weight:var(--ha-font-weight-normal);line-height:var(--ha-line-height-condensed)}h2{font-family:var(--ha-font-family-body);-webkit-font-smoothing:var(--ha-font-smoothing);-moz-osx-font-smoothing:var(--ha-moz-osx-font-smoothing);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;font-size:var(--ha-font-size-xl);font-weight:var(--ha-font-weight-medium);line-height:var(--ha-line-height-normal)}h3{font-family:var(--ha-font-family-body);-webkit-font-smoothing:var(--ha-font-smoothing);-moz-osx-font-smoothing:var(--ha-moz-osx-font-smoothing);font-size:var(--ha-font-size-l);font-weight:var(--ha-font-weight-normal);line-height:var(--ha-line-height-normal)}a{color:var(--primary-color)}.secondary{color:var(--secondary-text-color)}.error{color:var(--error-color)}.warning{color:var(--error-color)}${0} .card-actions a{text-decoration:none}.card-actions .warning{--mdc-theme-primary:var(--error-color)}.layout.horizontal,.layout.vertical{display:flex}.layout.inline{display:inline-flex}.layout.horizontal{flex-direction:row}.layout.vertical{flex-direction:column}.layout.wrap{flex-wrap:wrap}.layout.no-wrap{flex-wrap:nowrap}.layout.center,.layout.center-center{align-items:center}.layout.bottom{align-items:flex-end}.layout.center-center,.layout.center-justified{justify-content:center}.flex{flex:1;flex-basis:0.000000001px}.flex-auto{flex:1 1 auto}.flex-none{flex:none}.layout.justified{justify-content:space-between}`),h),g=(0,n.AH)(r||(r=c`
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
`)),m=(0,n.AH)(l||(l=c`ha-adaptive-dialog,ha-dialog{--vertical-align-dialog:flex-start;--dialog-surface-margin-top:var(--ha-space-10);--mdc-dialog-max-height:calc(
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
    )}@media all and (max-width:450px),all and (max-height:500px){ha-adaptive-dialog,ha-dialog{--dialog-surface-margin-top:0px;--mdc-dialog-min-height:100vh;--mdc-dialog-min-height:100svh;--mdc-dialog-max-height:100vh;--mdc-dialog-max-height:100svh;--ha-dialog-max-height:100vh;--ha-dialog-max-height:100svh}}`)),f=(0,n.AH)(s||(s=c`.ha-scrollbar::-webkit-scrollbar{width:.4rem;height:.4rem}.ha-scrollbar::-webkit-scrollbar-thumb{border-radius:var(--ha-border-radius-sm);background:var(--scrollbar-thumb-color)}.ha-scrollbar{overflow-y:auto;scrollbar-color:var(--scrollbar-thumb-color) transparent;scrollbar-width:thin}`));(0,n.AH)(d||(d=c`body{background-color:var(--primary-background-color);color:var(--primary-text-color);height:calc(100vh - 32px);width:100vw}`))},44144:function(t,a,e){e.d(a,{Cv:function(){return r},MR:function(){return c},QR:function(){return h},_c:function(){return d},a_:function(){return g},bg:function(){return m},yM:function(){return u}});e(18111),e(22489),e(3362),e(62953),e(3296),e(27208),e(48408),e(14603),e(47566),e(98721);let n,o;const i=66649!=e.j?18e5:null,r=t=>l(t).then(()=>s(t),()=>{}),l=async t=>{const a=await t.callWS({type:"brands/access_token"});n=a.token},s=t=>{d(),o=setInterval(()=>{l(t).catch(()=>{})},i)},d=()=>{o&&(clearInterval(o),o=void 0)},c=(t,a)=>{a=null!=a?a:location.origin;const e=`/api/brands/integration/${t.domain}/${t.darkOptimized?"dark_":""}${t.type}.png`,o=new URL(e,a);return n&&o.searchParams.set("token",n),o.toString()},h=(t,a)=>{a=null!=a?a:location.origin;const e=`/api/brands/hardware/${t.category}/${t.darkOptimized?"dark_":""}${t.manufacturer}${t.model?`_${t.model}`:""}.png`,o=new URL(e,a);return n&&o.searchParams.set("token",n),o.toString()},u=(t,a)=>{if(a=null!=a?a:location.origin,!n)return t;try{const e=new URL(t,a);return e.pathname.startsWith("/api/brands/")?(e.searchParams.set("token",n),e.toString()):t}catch(e){return t}},g=t=>{var a;const e=new URL(t,location.origin);if(e.pathname.startsWith("/api/brands/"))return e.pathname.split("/")[4];const n=e.pathname.split("/").filter(t=>t.length>0),o=n.indexOf("_");return-1!==o&&o+1<n.length?n[o+1]:null!==(a=n[1])&&void 0!==a?a:""},m=t=>{try{return new URL(t,location.origin).pathname.startsWith("/api/brands/")||t.startsWith("https://brands.home-assistant.io/")}catch(a){return!1}}}}]);
//# sourceMappingURL=78547.a8689bbeafa995f5.js.map