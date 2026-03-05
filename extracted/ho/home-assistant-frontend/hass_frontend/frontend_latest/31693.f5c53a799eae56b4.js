export const __rspack_esm_id="31693";export const __rspack_esm_ids=["31693"];export const __webpack_modules__={50248(a,t,e){e.d(t,{n:()=>o});const o=(a=document)=>a.activeElement?.shadowRoot?.activeElement?o(a.activeElement.shadowRoot):a.activeElement},91926(a,t,e){e.d(t,{O:()=>l,o:()=>s});var o=e(22444),i=e(1087),r=e(63091);const n=async a=>{const{history:t}=r.G;if(!t.state?.dialog||Date.now()-a>=500)return!0;return await(0,o.Jh)()?(await new Promise(a=>{setTimeout(a)}),n(a)):(console.warn("Navigation blocked, because dialog refused to close"),!1)},s=async(a,t)=>{if(!await n(Date.now()))return!1;const e=t?.replace||!1;return e?r.G.history.replaceState(r.G.history.state?.root?{root:!0}:t?.data??null,"",a):r.G.history.pushState(t?.data??null,"",a),(0,i.r)(r.G,"location-changed",{replace:e}),!0},l=async a=>{if(!await n(Date.now()))return;const{history:t}=r.G;if(t.length>1)return void t.back();s(a||"/",{replace:!0})}},12587(a,t,e){e.d(t,{E:()=>i,m:()=>o});const o=a=>{requestAnimationFrame(()=>setTimeout(a,0))},i=()=>new Promise(a=>{o(a)})},2846(a,t,e){e.d(t,{G:()=>d,J:()=>l});var o=e(62826),i=e(12415),r=e(82553),n=e(96196),s=e(97735);e(54276);const l=[r.R,n.AH`:host{--ha-icon-display:block;--md-sys-color-primary:var(--primary-text-color);--md-sys-color-secondary:var(--secondary-text-color);--md-sys-color-surface:var(--card-background-color);--md-sys-color-on-surface:var(--primary-text-color);--md-sys-color-on-surface-variant:var(--secondary-text-color)}md-item{overflow:var(--md-item-overflow,hidden);align-items:var(--md-item-align-items,center);gap:var(--ha-md-list-item-gap,16px)}`];class d extends i.n{renderRipple(){return"text"===this.type?n.s6:n.qy`<ha-ripple part="ripple" for="item" ?disabled="${this.disabled&&"link"!==this.type}"></ha-ripple>`}}d.styles=l,d=(0,o.Cg)([(0,s.EM)("ha-md-list-item")],d)},54276(a,t,e){var o=e(62826),i=e(76482),r=e(91382),n=e(96245),s=e(96196),l=e(97735);class d extends r.n{attach(a){super.attach(a),this.attachableTouchController.attach(a)}disconnectedCallback(){super.disconnectedCallback(),this.hovered=!1,this.pressed=!1}detach(){super.detach(),this.attachableTouchController.detach()}_onTouchControlChange(a,t){a?.removeEventListener("touchend",this._handleTouchEnd),t?.addEventListener("touchend",this._handleTouchEnd)}constructor(...a){super(...a),this.attachableTouchController=new i.i(this,this._onTouchControlChange.bind(this)),this._handleTouchEnd=()=>{this.disabled||super.endPressAnimation()}}}d.styles=[n.R,s.AH`:host{--md-ripple-hover-opacity:var(--ha-ripple-hover-opacity, 0.08);--md-ripple-pressed-opacity:var(--ha-ripple-pressed-opacity, 0.12);--md-ripple-hover-color:var(
          --ha-ripple-hover-color,
          var(--ha-ripple-color, var(--secondary-text-color))
        );--md-ripple-pressed-color:var(
          --ha-ripple-pressed-color,
          var(--ha-ripple-color, var(--secondary-text-color))
        )}`],d=(0,o.Cg)([(0,l.EM)("ha-ripple")],d)},59241(a,t,e){e.d(t,{BM:()=>T,Bz:()=>w,DW:()=>h,Er:()=>c,G3:()=>p,G_:()=>f,Ox:()=>_,P9:()=>k,RP:()=>y,bg:()=>v,jh:()=>g,n4:()=>b,v:()=>m});e(18111),e(22489),e(20116);var o=e(35518),i=e(22786),r=e(71727),n=e(28978),s=e(52220),l=e(9899);const d=["sensor","binary_sensor"],c=(a,t)=>{const e=t.filter(t=>a.states[t.entity_id]&&"battery"===a.states[t.entity_id].attributes.device_class&&d.includes((0,r.m)(t.entity_id))).sort((a,t)=>d.indexOf((0,r.m)(a.entity_id))-d.indexOf((0,r.m)(t.entity_id)));if(e.length>0)return e[0]},h=(a,t)=>t.find(t=>a.states[t.entity_id]&&"battery_charging"===a.states[t.entity_id].attributes.device_class),g=(a,t)=>{if(t.name)return t.name;const e=a.states[t.entity_id];return e?(0,n.u)(e):t.original_name?t.original_name:t.entity_id},m=(a,t)=>a.callWS({type:"config/entity_registry/get",entity_id:t}),p=(a,t)=>a.callWS({type:"config/entity_registry/get_entries",entity_ids:t}),f=(a,t,e)=>a.callWS({type:"config/entity_registry/update",entity_id:t,...e}),v=(a,t)=>a.callWS({type:"config/entity_registry/remove",entity_id:t}),u=a=>a.sendMessagePromise({type:"config/entity_registry/list"}),y=a=>a.sendMessagePromise({type:"config/entity_registry/list_for_display"}),x=(a,t)=>a.subscribeEvents((0,l.s)(()=>u(a).then(a=>t.setState(a,!0)),500,!0),"entity_registry_updated"),w=(a,t)=>(0,o.N)("_entityRegistry",u,x,a,t),b=(a,t)=>a.sort((a,e)=>(0,s.SH)(a.name||"",e.name||"",t)),_=(0,i.A)(a=>{const t={};for(const e of a)t[e.entity_id]=e;return t}),k=(0,i.A)(a=>{const t={};for(const e of a)t[e.id]=e;return t}),T=(a,t)=>a.callWS({type:"config/entity_registry/get_automatic_entity_ids",entity_ids:t})},65063(a,t,e){e.d(t,{an:()=>l,dk:()=>s,showAlertDialog:()=>n});var o=e(1087);const i=()=>Promise.all([e.e("31065"),e.e("79064"),e.e("84776")]).then(e.bind(e,26683)),r=(a,t,e)=>new Promise(r=>{const n=t.cancel,s=t.confirm;(0,o.r)(a,"show-dialog",{dialogTag:"dialog-box",dialogImport:i,dialogParams:{...t,...e,cancel:()=>{r(!!e?.prompt&&null),n&&n()},confirm:a=>{r(!e?.prompt||a),s&&s(a)}}})}),n=(a,t)=>r(a,t),s=(a,t)=>r(a,t,{confirmation:!0}),l=(a,t)=>r(a,t,{prompt:!0})},22444(a,t,e){e.d(t,{oO:()=>f,t3:()=>g,zU:()=>h,Jh:()=>m,ui:()=>c});e(44114),e(17642),e(58004),e(33853),e(45876),e(32475),e(15024),e(31698);const o=(a,t,e=true)=>{if(!a||a===document.body)return null;if((a=a.assignedSlot??a).parentElement)a=a.parentElement;else{const t=a.getRootNode();a=t instanceof ShadowRoot?t.host:null}return(e?Object.prototype.hasOwnProperty.call(a,t):a&&t in a)?a:o(a,t,e)};if(66649!=e.j)var i=e(50248);var r=e(63091);if(66649!=e.j)var n=e(12587);const s={},l=[],d=Symbol.for("HA focus target"),c=async(a,t,e,n,h,g=!0)=>{if(!(e in s)){if(!h)return!1;s[e]={element:h().then(()=>{const t=document.createElement(e);return a.provideHass(t),t.addEventListener("dialog-closed",p),t.addEventListener("dialog-closed",v),t})}}if(g){const{history:o}=r.G;if(o.state?.dialog&&!l.length)return await new Promise(a=>{setTimeout(a)}),c(a,t,e,n,h,g);const i=l.findIndex(a=>a.dialogTag===e);-1!==i&&l.splice(i,1),l.push({element:a,root:t,dialogTag:e,dialogParams:n,dialogImport:h,addHistory:g});const s={dialog:e};o.state?.dialog?o.replaceState(s,""):(o.replaceState({...o.state,opensDialog:!0},""),o.pushState(s,""))}s[e].closedFocusTargets=((a,t,e=!0)=>{const i=new Set;for(;a;)i.add(a),a=o(a,t,e);return i})((0,i.n)(),d);const m=await s[e].element;return t.appendChild(m),m.showDialog(n),!0},h=async(a,t)=>{if(!(a in s))return!0;const e=await s[a].element;return!e.closeDialog||!1!==e.closeDialog(t)},g=async a=>{if(l.length){const t=l.pop(),e=await h(t.dialogTag,a);return e?l.length&&r.G.history.state?.opensDialog&&r.G.history.pushState({dialog:l[l.length-1].dialogTag},""):l.push(t),e}return!0},m=async()=>{for(let a=l.length-1;a>=0;a--){if(!(!l[a]||await h(l[a].dialogTag)))return!1}return!0},p=a=>{const t=l.findIndex(t=>t.dialogTag===a.detail.dialog);-1!==t&&l.splice(t,1),r.G.history.state?.dialog===a.detail.dialog&&(l.length?r.G.history.replaceState({dialog:l[l.length-1].dialogTag},""):-1!==t&&r.G.history.back())},f=(a,t)=>{a.addEventListener("show-dialog",e=>{const{dialogTag:o,dialogImport:i,dialogParams:r,addHistory:n}=e.detail;c(a,t,o,r,i,n)})},v=async a=>{if(!s[a.detail.dialog])return;const t=s[a.detail.dialog].closedFocusTargets;if(delete s[a.detail.dialog].closedFocusTargets,!t)return;let e=(0,i.n)();e instanceof HTMLElement&&e.blur(),await(0,n.E)();for(const a of t)if(a instanceof HTMLElement&&(a.focus(),e=(0,i.n)(),e&&e!==document.body))return}},14503(a,t,e){e.d(t,{RF:()=>r,dp:()=>l,kO:()=>s,nA:()=>n,og:()=>i});var o=e(96196);const i=o.AH`button.link{background:0 0;color:inherit;border:none;padding:0;font:inherit;text-align:left;text-decoration:underline;cursor:pointer;outline:0}`,r=o.AH`:host{font-family:var(--ha-font-family-body);-webkit-font-smoothing:var(--ha-font-smoothing);-moz-osx-font-smoothing:var(--ha-moz-osx-font-smoothing);font-size:var(--ha-font-size-m);font-weight:var(--ha-font-weight-normal);line-height:var(--ha-line-height-normal)}app-header div[sticky]{height:48px}app-toolbar [main-title]{margin-left:20px;margin-inline-start:20px;margin-inline-end:initial}.header{transition:box-shadow .2s linear,width var(--ha-animation-duration-normal) ease,padding-left var(--ha-animation-duration-normal) ease,padding-right var(--ha-animation-duration-normal) ease}@media (prefers-reduced-motion:reduce){.header{transition:box-shadow .2s linear}}h1{font-family:var(--ha-font-family-heading);-webkit-font-smoothing:var(--ha-font-smoothing);-moz-osx-font-smoothing:var(--ha-moz-osx-font-smoothing);font-size:var(--ha-font-size-2xl);font-weight:var(--ha-font-weight-normal);line-height:var(--ha-line-height-condensed)}h2{font-family:var(--ha-font-family-body);-webkit-font-smoothing:var(--ha-font-smoothing);-moz-osx-font-smoothing:var(--ha-moz-osx-font-smoothing);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;font-size:var(--ha-font-size-xl);font-weight:var(--ha-font-weight-medium);line-height:var(--ha-line-height-normal)}h3{font-family:var(--ha-font-family-body);-webkit-font-smoothing:var(--ha-font-smoothing);-moz-osx-font-smoothing:var(--ha-moz-osx-font-smoothing);font-size:var(--ha-font-size-l);font-weight:var(--ha-font-weight-normal);line-height:var(--ha-line-height-normal)}a{color:var(--primary-color)}.secondary{color:var(--secondary-text-color)}.error{color:var(--error-color)}.warning{color:var(--error-color)}${i} .card-actions a{text-decoration:none}.card-actions .warning{--mdc-theme-primary:var(--error-color)}.layout.horizontal,.layout.vertical{display:flex}.layout.inline{display:inline-flex}.layout.horizontal{flex-direction:row}.layout.vertical{flex-direction:column}.layout.wrap{flex-wrap:wrap}.layout.no-wrap{flex-wrap:nowrap}.layout.center,.layout.center-center{align-items:center}.layout.bottom{align-items:flex-end}.layout.center-center,.layout.center-justified{justify-content:center}.flex{flex:1;flex-basis:0.000000001px}.flex-auto{flex:1 1 auto}.flex-none{flex:none}.layout.justified{justify-content:space-between}`,n=o.AH`
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
`,s=o.AH`ha-adaptive-dialog,ha-dialog{--vertical-align-dialog:flex-start;--dialog-surface-margin-top:var(--ha-space-10);--mdc-dialog-max-height:calc(
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
    )}@media all and (max-width:450px),all and (max-height:500px){ha-adaptive-dialog,ha-dialog{--dialog-surface-margin-top:0px;--mdc-dialog-min-height:100vh;--mdc-dialog-min-height:100svh;--mdc-dialog-max-height:100vh;--mdc-dialog-max-height:100svh;--ha-dialog-max-height:100vh;--ha-dialog-max-height:100svh}}`,l=o.AH`.ha-scrollbar::-webkit-scrollbar{width:.4rem;height:.4rem}.ha-scrollbar::-webkit-scrollbar-thumb{border-radius:var(--ha-border-radius-sm);background:var(--scrollbar-thumb-color)}.ha-scrollbar{overflow-y:auto;scrollbar-color:var(--scrollbar-thumb-color) transparent;scrollbar-width:thin}`;o.AH`body{background-color:var(--primary-background-color);color:var(--primary-text-color);height:calc(100vh - 32px);width:100vw}`},44144(a,t,e){e.d(t,{Cv:()=>n,MR:()=>c,QR:()=>h,_c:()=>d,a_:()=>m,bg:()=>p,yM:()=>g});e(18111),e(22489),e(14603),e(47566),e(98721);let o,i;const r=66649!=e.j?18e5:null,n=a=>s(a).then(()=>l(a),()=>{}),s=async a=>{const t=await a.callWS({type:"brands/access_token"});o=t.token},l=a=>{d(),i=setInterval(()=>{s(a).catch(()=>{})},r)},d=()=>{i&&(clearInterval(i),i=void 0)},c=(a,t)=>{t=t??location.origin;const e=`/api/brands/integration/${a.domain}/${a.darkOptimized?"dark_":""}${a.type}.png`,i=new URL(e,t);return o&&i.searchParams.set("token",o),i.toString()},h=(a,t)=>{t=t??location.origin;const e=`/api/brands/hardware/${a.category}/${a.darkOptimized?"dark_":""}${a.manufacturer}${a.model?`_${a.model}`:""}.png`,i=new URL(e,t);return o&&i.searchParams.set("token",o),i.toString()},g=(a,t)=>{if(t=t??location.origin,!o)return a;try{const e=new URL(a,t);return e.pathname.startsWith("/api/brands/")?(e.searchParams.set("token",o),e.toString()):a}catch{return a}},m=a=>{const t=new URL(a,location.origin);if(t.pathname.startsWith("/api/brands/"))return t.pathname.split("/")[4];const e=t.pathname.split("/").filter(a=>a.length>0),o=e.indexOf("_");return-1!==o&&o+1<e.length?e[o+1]:e[1]??""},p=a=>{try{return new URL(a,location.origin).pathname.startsWith("/api/brands/")||a.startsWith("https://brands.home-assistant.io/")}catch{return!1}}}};
//# sourceMappingURL=31693.f5c53a799eae56b4.js.map