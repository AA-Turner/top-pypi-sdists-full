export const __rspack_esm_id="87772";export const __rspack_esm_ids=["87772"];export const __webpack_modules__={5745(e,t,a){var i=a(62826),o=a(4720),r=a(44457);class s extends o.Y{}s=(0,i.Cg)([(0,r.EM)("ha-chip-set")],s)},38962(e,t,a){a.r(t);var i=a(62826),o=a(96196),r=a(44457),s=a(94333),n=a(1087);a(26300),a(67094);const l={info:"M11,9H13V7H11M12,20C7.59,20 4,16.41 4,12C4,7.59 7.59,4 12,4C16.41,4 20,7.59 20,12C20,16.41 16.41,20 12,20M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M11,17H13V11H11V17Z",warning:"M12,2L1,21H23M12,6L19.53,19H4.47M11,10V14H13V10M11,16V18H13V16",error:"M11,15H13V17H11V15M11,7H13V13H11V7M12,2C6.47,2 2,6.5 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M12,20A8,8 0 0,1 4,12A8,8 0 0,1 12,4A8,8 0 0,1 20,12A8,8 0 0,1 12,20Z",success:"M20,12A8,8 0 0,1 12,20A8,8 0 0,1 4,12A8,8 0 0,1 12,4C12.76,4 13.5,4.11 14.2,4.31L15.77,2.74C14.61,2.26 13.34,2 12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12M7.91,10.08L6.5,11.5L11,16L21,6L19.59,4.58L11,13.17L7.91,10.08Z"};class d extends o.WF{render(){return o.qy` <div class="issue-type ${(0,s.H)({[this.alertType]:!0})}" role="alert"> <div class="icon ${this.title?"":"no-title"}"> <slot name="icon"> <ha-svg-icon .path="${l[this.alertType]}"></ha-svg-icon> </slot> </div> <div class="${(0,s.H)({content:!0,narrow:this.narrow})}"> <div class="main-content"> ${this.title?o.qy`<div class="title">${this.title}</div>`:o.s6} <slot></slot> </div> <div class="action"> <slot name="action"> ${this.dismissable?o.qy`<ha-icon-button @click="${this._dismissClicked}" label="Dismiss alert" .path="${"M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z"}"></ha-icon-button>`:o.s6} </slot> </div> </div> </div> `}_dismissClicked(){(0,n.r)(this,"alert-dismissed-clicked")}constructor(...e){super(...e),this.title="",this.alertType="info",this.dismissable=!1,this.narrow=!1}}d.styles=o.AH`.issue-type{position:relative;padding:8px;display:flex}.icon{height:var(--ha-alert-icon-size,24px);width:var(--ha-alert-icon-size,24px)}.issue-type::after{position:absolute;top:0;right:0;bottom:0;left:0;opacity:.12;pointer-events:none;content:"";border-radius:var(--ha-border-radius-sm)}.icon.no-title{align-self:center}.content{display:flex;justify-content:space-between;align-items:center;width:100%;text-align:var(--float-start)}.content.narrow{flex-direction:column;align-items:flex-end}.action{z-index:1;width:min-content;--mdc-theme-primary:var(--primary-text-color)}.main-content{overflow-wrap:anywhere;word-break:break-word;line-height:normal;margin-left:8px;margin-right:0;margin-inline-start:8px;margin-inline-end:8px}.title{margin-top:2px;font-weight:var(--ha-font-weight-bold)}.action ha-icon-button{--mdc-theme-primary:var(--primary-text-color);--mdc-icon-button-size:36px}.issue-type.info>.icon{color:var(--info-color)}.issue-type.info::after{background-color:var(--info-color)}.issue-type.warning>.icon{color:var(--warning-color)}.issue-type.warning::after{background-color:var(--warning-color)}.issue-type.error>.icon{color:var(--error-color)}.issue-type.error::after{background-color:var(--error-color)}.issue-type.success>.icon{color:var(--success-color)}.issue-type.success::after{background-color:var(--success-color)}:host ::slotted(ul){margin:0;padding-inline-start:20px}`,(0,i.Cg)([(0,r.MZ)()],d.prototype,"title",void 0),(0,i.Cg)([(0,r.MZ)({attribute:"alert-type"})],d.prototype,"alertType",void 0),(0,i.Cg)([(0,r.MZ)({type:Boolean})],d.prototype,"dismissable",void 0),(0,i.Cg)([(0,r.MZ)({type:Boolean})],d.prototype,"narrow",void 0),d=(0,i.Cg)([(0,r.EM)("ha-alert")],d)},99611(e,t,a){a.a(e,async function(e,i){try{a.d(t,{r:()=>p});var o=a(62826),r=a(1126),s=a(96196),n=a(44457),l=a(60353),d=a(59992),c=a(14503),h=e([r]);r=(h.then?(await h)():h)[0];const p=300;class g extends((0,d.V)(s.WF)){get scrollableElement(){return this._bodyElement}_handleAfterHide(e){e.stopPropagation(),this.open=!1;const t=new Event("closed",{bubbles:!0,composed:!0});this.dispatchEvent(t)}updated(e){super.updated(e),e.has("open")&&(this._drawerOpen=this.open)}render(){return s.qy` <wa-drawer id="drawer" placement="bottom" .open="${this._drawerOpen}" @wa-after-hide="${this._handleAfterHide}" without-header @touchstart="${this._handleTouchStart}"> <slot name="header"></slot> <div class="content-wrapper"> <div id="body" class="body ha-scrollbar"> <slot></slot> </div> ${this.renderScrollableFades()} </div> <slot name="footer"></slot> </wa-drawer> `}_startResizing(e){document.addEventListener("touchmove",this._handleTouchMove,{passive:!1}),document.addEventListener("touchend",this._handleTouchEnd),document.addEventListener("touchcancel",this._handleTouchEnd),this._gestureRecognizer.start(e)}_animateSnapBack(){this.style.setProperty("--dialog-transition",`transform ${p}ms ease-out`),this.style.removeProperty("--dialog-transform"),setTimeout(()=>{this.style.removeProperty("--dialog-transition")},p)}disconnectedCallback(){super.disconnectedCallback(),this._unregisterResizeHandlers(),this._isDragging=!1}static get styles(){return[...super.styles,c.dp,s.AH`wa-drawer{--wa-color-surface-raised:transparent;--spacing:0;--size:var(--ha-bottom-sheet-height, auto);--show-duration:${p}ms;--hide-duration:${p}ms}wa-drawer::part(dialog){max-height:var(--ha-bottom-sheet-max-height,90vh);align-items:center;transform:var(--dialog-transform);transition:var(--dialog-transition)}wa-drawer::part(body){max-width:var(--ha-bottom-sheet-max-width);width:100%;border-top-left-radius:var(--ha-bottom-sheet-border-radius,var(--ha-dialog-border-radius,var(--ha-border-radius-2xl)));border-top-right-radius:var(--ha-bottom-sheet-border-radius,var(--ha-dialog-border-radius,var(--ha-border-radius-2xl)));background-color:var(--ha-bottom-sheet-surface-background,var(--ha-dialog-surface-background,var(--mdc-theme-surface,#fff)));padding:var(--ha-bottom-sheet-padding,0 var(--safe-area-inset-right) var(--safe-area-inset-bottom) var(--safe-area-inset-left))}:host([flexcontent]) wa-drawer::part(body){display:flex;flex-direction:column}.content-wrapper{position:relative;flex:1;display:flex;flex-direction:column;min-height:0}:host([flexcontent]) .body{flex:1;max-width:100%;display:flex;flex-direction:column;padding:var(--ha-bottom-sheet-padding,0 var(--safe-area-inset-right) var(--safe-area-inset-bottom) var(--safe-area-inset-left))}slot[name=footer]{display:block;padding:0}::slotted([slot=footer]){display:flex;padding:var(--ha-space-3) var(--ha-space-4) var(--ha-space-4) var(--ha-space-4);gap:var(--ha-space-3);justify-content:flex-end;align-items:center;width:100%;box-sizing:border-box}:host([flexcontent]) slot[name=footer]{flex-shrink:0}`]}constructor(...e){super(...e),this.open=!1,this.flexContent=!1,this._drawerOpen=!1,this._gestureRecognizer=new l.u,this._isDragging=!1,this._handleTouchStart=e=>{for(const t of e.composedPath()){const e=t;if(e===this._drawer)break;if(e.scrollTop>0)return}this._startResizing(e.touches[0].clientY)},this._handleTouchMove=e=>{const t=e.touches[0].clientY,a=this._gestureRecognizer.move(t);a<0&&(e.preventDefault(),this._isDragging=!0,requestAnimationFrame(()=>{this._isDragging&&this.style.setProperty("--dialog-transform",`translateY(${-1*a}px)`)}))},this._handleTouchEnd=()=>{this._unregisterResizeHandlers(),this._isDragging=!1;const e=this._gestureRecognizer.end();if(e.isSwipe)return void(e.isDownwardSwipe?this._drawerOpen=!1:this._animateSnapBack());const t=this._drawer.shadowRoot?.querySelector('[part="body"]'),a=t?.offsetHeight||0;a>0&&e.delta<0&&Math.abs(e.delta)>.5*a?this._drawerOpen=!1:this._animateSnapBack()},this._unregisterResizeHandlers=()=>{document.removeEventListener("touchmove",this._handleTouchMove),document.removeEventListener("touchend",this._handleTouchEnd),document.removeEventListener("touchcancel",this._handleTouchEnd)}}}(0,o.Cg)([(0,n.MZ)({type:Boolean})],g.prototype,"open",void 0),(0,o.Cg)([(0,n.MZ)({type:Boolean,reflect:!0,attribute:"flexcontent"})],g.prototype,"flexContent",void 0),(0,o.Cg)([(0,n.wk)()],g.prototype,"_drawerOpen",void 0),(0,o.Cg)([(0,n.P)("#drawer")],g.prototype,"_drawer",void 0),(0,o.Cg)([(0,n.P)("#body")],g.prototype,"_bodyElement",void 0),g=(0,o.Cg)([(0,n.EM)("ha-bottom-sheet")],g),i()}catch(e){i(e)}})},93444(e,t,a){var i=a(62826),o=a(96196),r=a(44457);class s extends o.WF{render(){return o.qy` <footer> <slot name="secondaryAction"></slot> <slot name="primaryAction"></slot> </footer> `}static get styles(){return[o.AH`footer{display:flex;gap:var(--ha-space-3);justify-content:flex-end;align-items:center;width:100%}`]}}s=(0,i.Cg)([(0,r.EM)("ha-dialog-footer")],s)},44010(e,t,a){var i=a(62826),o=a(4042),r=a(44457);class s extends o.A{constructor(...e){super(...e),this.name="fadeIn",this.fill="both",this.play=!0,this.iterations=1}}(0,i.Cg)([(0,r.MZ)()],s.prototype,"name",void 0),(0,i.Cg)([(0,r.MZ)()],s.prototype,"fill",void 0),(0,i.Cg)([(0,r.MZ)({type:Boolean})],s.prototype,"play",void 0),(0,i.Cg)([(0,r.MZ)({type:Number})],s.prototype,"iterations",void 0),s=(0,i.Cg)([(0,r.EM)("ha-fade-in")],s)},88945(e,t,a){a.r(t),a.d(t,{HaIcon:()=>w});var i=a(62826),o=a(96196),r=a(44457),s=a(1087),n=a(9899),l=a(57769),d=(a(44114),a(18111),a(7588),a(95192)),c=a(22786),h=a(7553);const p=JSON.parse('{"version":"7.4.47","parts":[{"file":"7a7139d465f1f41cb26ab851a17caa21a9331234"},{"start":"account-supervisor-circle-","file":"9561286c4c1021d46b9006596812178190a7cc1c"},{"start":"alpha-r-c","file":"eb466b7087fb2b4d23376ea9bc86693c45c500fa"},{"start":"arrow-decision-o","file":"4b3c01b7e0723b702940c5ac46fb9e555646972b"},{"start":"baby-f","file":"2611401d85450b95ab448ad1d02c1a432b409ed2"},{"start":"battery-hi","file":"89bcd31855b34cd9d31ac693fb073277e74f1f6a"},{"start":"blur-r","file":"373709cd5d7e688c2addc9a6c5d26c2d57c02c48"},{"start":"briefcase-account-","file":"a75956cf812ee90ee4f656274426aafac81e1053"},{"start":"calendar-question-","file":"3253f2529b5ebdd110b411917bacfacb5b7063e6"},{"start":"car-lig","file":"74566af3501ad6ae58ad13a8b6921b3cc2ef879d"},{"start":"cellphone-co","file":"7677f1cfb2dd4f5562a2aa6d3ae43a2e6997b21a"},{"start":"circle-slice-2","file":"70d08c50ec4522dd75d11338db57846588263ee2"},{"start":"cloud-co","file":"141d2bfa55ca4c83f4bae2812a5da59a84fec4ff"},{"start":"cog-s","file":"5a640365f8e47c609005d5e098e0e8104286d120"},{"start":"cookie-l","file":"dd85b8eb8581b176d3acf75d1bd82e61ca1ba2fc"},{"start":"currency-eur-","file":"15362279f4ebfc3620ae55f79d2830ad86d5213e"},{"start":"delete-o","file":"239434ab8df61237277d7599ebe066c55806c274"},{"start":"draw-","file":"5605918a592070803ba2ad05a5aba06263da0d70"},{"start":"emoticon-po","file":"a838cfcec34323946237a9f18e66945f55260f78"},{"start":"fan","file":"effd56103b37a8c7f332e22de8e4d67a69b70db7"},{"start":"file-question-","file":"b2424b50bd465ae192593f1c3d086c5eec893af8"},{"start":"flask-off-","file":"3b76295cde006a18f0301dd98eed8c57e1d5a425"},{"start":"food-s","file":"1c6941474cbeb1755faaaf5771440577f4f1f9c6"},{"start":"gamepad-u","file":"c6efe18db6bc9654ae3540c7dee83218a5450263"},{"start":"google-f","file":"df341afe6ad4437457cf188499cb8d2df8ac7b9e"},{"start":"head-c","file":"282121c9e45ed67f033edcc1eafd279334c00f46"},{"start":"home-pl","file":"27e8e38fc7adcacf2a210802f27d841b49c8c508"},{"start":"inbox-","file":"0f0316ec7b1b7f7ce3eaabce26c9ef619b5a1694"},{"start":"key-v","file":"ea33462be7b953ff1eafc5dac2d166b210685a60"},{"start":"leaf-circle-","file":"33db9bbd66ce48a2db3e987fdbd37fb0482145a4"},{"start":"lock-p","file":"b89e27ed39e9d10c44259362a4b57f3c579d3ec8"},{"start":"message-s","file":"7b5ab5a5cadbe06e3113ec148f044aa701eac53a"},{"start":"moti","file":"01024d78c248d36805b565e343dd98033cc3bcaf"},{"start":"newspaper-variant-o","file":"22a6ec4a4fdd0a7c0acaf805f6127b38723c9189"},{"start":"on","file":"c73d55b412f394e64632e2011a59aa05e5a1f50d"},{"start":"paw-ou","file":"3f669bf26d16752dc4a9ea349492df93a13dcfbf"},{"start":"pigg","file":"0c24edb27eb1c90b6e33fc05f34ef3118fa94256"},{"start":"printer-pos-sy","file":"41a55cda866f90b99a64395c3bb18c14983dcf0a"},{"start":"read","file":"c7ed91552a3a64c9be88c85e807404cf705b7edf"},{"start":"robot-vacuum-variant-o","file":"917d2a35d7268c0ea9ad9ecab2778060e19d90e0"},{"start":"sees","file":"6e82d9861d8fac30102bafa212021b819f303bdb"},{"start":"shoe-f","file":"e2fe7ce02b5472301418cc90a0e631f187b9f238"},{"start":"snowflake-m","file":"a28ba9f5309090c8b49a27ca20ff582a944f6e71"},{"start":"st","file":"7e92d03f095ec27e137b708b879dfd273bd735ab"},{"start":"su","file":"61c74913720f9de59a379bdca37f1d2f0dc1f9db"},{"start":"tag-plus-","file":"8f3184156a4f38549cf4c4fffba73a6a941166ae"},{"start":"timer-a","file":"baab470d11cfb3a3cd3b063ee6503a77d12a80d0"},{"start":"transit-d","file":"8561c0d9b1ac03fab360fd8fe9729c96e8693239"},{"start":"vector-arrange-b","file":"c9a3439257d4bab33d3355f1f2e11842e8171141"},{"start":"water-ou","file":"02dbccfb8ca35f39b99f5a085b095fc1275005a0"},{"start":"webc","file":"57bafd4b97341f4f2ac20a609d023719f23a619c"},{"start":"zip","file":"65ae094e8263236fa50486584a08c03497a38d93"}]}'),g=(0,c.A)(async()=>{const e=(0,d.y$)("hass-icon-db","mdi-icon-store");{const t=await(0,d.Jt)("_version",e);t?t!==p.version&&(await(0,d.IU)(e),(0,d.hZ)("_version",p.version,e)):(0,d.hZ)("_version",p.version,e)}return e}),f=["mdi","hass","hassio","hademo"];let u=[];a(67094);const m={},v={},b=(0,n.s)(()=>(async e=>{const t=Object.keys(e),a=await Promise.all(Object.values(e));(await g())("readwrite",i=>{a.forEach((a,o)=>{Object.entries(a).forEach(([e,t])=>{i.put(t,e)}),delete e[t[o]]})})})(v),2e3),y={};class w extends o.WF{willUpdate(e){super.willUpdate(e),e.has("icon")&&(this._path=void 0,this._secondaryPath=void 0,this._viewBox=void 0,this._loadIcon())}render(){return this.icon?this._legacy?o.qy` <iron-icon .icon="${this.icon}"></iron-icon>`:o.qy`<ha-svg-icon .path="${this._path}" .secondaryPath="${this._secondaryPath}" .viewBox="${this._viewBox}"></ha-svg-icon>`:o.s6}async _loadIcon(){if(!this.icon)return;const e=this.icon,[t,i]=this.icon.split(":",2);let o,r=i;if(!t||!r)return;if(!f.includes(t)){const a=l.y[t];return a?void(a&&"function"==typeof a.getIcon&&this._setCustomPath(a.getIcon(r),e)):void(this._legacy=!0)}if(this._legacy=!1,r in m){const e=m[r];let a;e.newName?(a=`Icon ${t}:${r} was renamed to ${t}:${e.newName}, please change your config, it will be removed in version ${e.removeIn}.`,r=e.newName):a=`Icon ${t}:${r} was removed from MDI, please replace this icon with an other icon in your config, it will be removed in version ${e.removeIn}.`,console.warn(a),(0,s.r)(this,"write_log",{level:"warning",message:a})}if(r in y)return void(this._path=y[r]);if("home-assistant"===r){const t=(await a.e("58781").then(a.bind(a,53580))).mdiHomeAssistant;return this.icon===e&&(this._path=t),void(y[r]=t)}try{o=await(e=>new Promise((t,a)=>{if(u.push([e,t,a]),u.length>1)return;const i=g();(0,h.h)(1e3,(async()=>{(await i)("readonly",e=>{for(const[t,a,i]of u)(0,d.Yd)(e.get(t)).then(e=>a(e)).catch(e=>i(e));u=[]})})()).catch(e=>{for(const[,,t]of u)t(e);u=[]})}))(r)}catch(e){o=void 0}if(o)return this.icon===e&&(this._path=o),void(y[r]=o);const n=(e=>{let t;for(const a of p.parts){if(void 0!==a.start&&e<a.start)break;t=a}return t.file})(r);if(n in v)return void this._setPath(v[n],r,e);const c=fetch(`/static/mdi/${n}.json`).then(e=>e.json());v[n]=c,this._setPath(c,r,e),b()}async _setCustomPath(e,t){const a=await e;this.icon===t&&(this._path=a.path,this._secondaryPath=a.secondaryPath,this._viewBox=a.viewBox)}async _setPath(e,t,a){const i=await e;this.icon===a&&(this._path=i[t]),y[t]=i[t]}constructor(...e){super(...e),this._legacy=!1}}w.styles=o.AH`:host{fill:currentcolor}`,(0,i.Cg)([(0,r.MZ)()],w.prototype,"icon",void 0),(0,i.Cg)([(0,r.wk)()],w.prototype,"_path",void 0),(0,i.Cg)([(0,r.wk)()],w.prototype,"_secondaryPath",void 0),(0,i.Cg)([(0,r.wk)()],w.prototype,"_viewBox",void 0),(0,i.Cg)([(0,r.wk)()],w.prototype,"_legacy",void 0),w=(0,i.Cg)([(0,r.EM)("ha-icon")],w)},69709(e,t,a){a(18111),a(22489),a(61701),a(18237);var i=a(62826),o=a(96196),r=a(44457),s=a(1420),n=a(30015),l=a.n(n),d=a(1087),c=(a(14603),a(47566),a(98721),a(2209));let h;var p=a(996);const g=e=>o.qy`${e}`,f=new p.G(1e3),u={reType:/(?<input>(\[!(?<type>caution|important|note|tip|warning)\])(?:\s|\\n)?)/i,typeToHaAlert:{caution:"error",important:"info",note:"info",tip:"success",warning:"warning"}};class m extends o.mN{disconnectedCallback(){if(super.disconnectedCallback(),this.cache){const e=this._computeCacheKey();f.set(e,this.innerHTML)}}createRenderRoot(){return this}update(e){super.update(e),void 0!==this.content&&(this._renderPromise=this._render())}async getUpdateComplete(){return await super.getUpdateComplete(),await this._renderPromise,!0}willUpdate(e){if(!this.innerHTML&&this.cache){const e=this._computeCacheKey();f.has(e)&&((0,o.XX)(g((0,s._)(f.get(e))),this.renderRoot),this._resize())}}_computeCacheKey(){return l()({content:this.content,allowSvg:this.allowSvg,allowDataUrl:this.allowDataUrl,breaks:this.breaks})}async _render(){const e=await(async(e,t,i)=>(h||(h=(0,c.LV)(new Worker(new URL(a.p+a.u("55640"),a.b)))),h.renderMarkdown(e,t,i)))(String(this.content),{breaks:this.breaks,gfm:!0},{allowSvg:this.allowSvg,allowDataUrl:this.allowDataUrl});(0,o.XX)(g((0,s._)(e.join(""))),this.renderRoot),this._resize();const t=document.createTreeWalker(this,NodeFilter.SHOW_ELEMENT,null);for(;t.nextNode();){const e=t.currentNode;if(e instanceof HTMLAnchorElement&&e.host!==document.location.host)e.target="_blank",e.rel="noreferrer noopener";else if(e instanceof HTMLImageElement)this.lazyImages&&(e.loading="lazy"),e.addEventListener("load",this._resize);else if(e instanceof HTMLQuoteElement){const a=e.firstElementChild?.firstChild?.textContent&&u.reType.exec(e.firstElementChild.firstChild.textContent);if(a){const{type:i}=a.groups,o=document.createElement("ha-alert");o.alertType=u.typeToHaAlert[i.toLowerCase()],o.append(...Array.from(e.childNodes).map(e=>{const t=Array.from(e.childNodes);if(!this.breaks&&t.length){const e=t[0];e.nodeType===Node.TEXT_NODE&&e.textContent===a.input&&e.textContent?.includes("\n")&&(e.textContent=e.textContent.split("\n").slice(1).join("\n"))}return t}).reduce((e,t)=>e.concat(t),[]).filter(e=>e.textContent&&e.textContent!==a.input)),t.parentNode().replaceChild(o,e)}}else e instanceof HTMLElement&&["ha-alert","ha-qr-code","ha-icon","ha-svg-icon"].includes(e.localName)&&a(96175)(`./${e.localName}`)}}constructor(...e){super(...e),this.allowSvg=!1,this.allowDataUrl=!1,this.breaks=!1,this.lazyImages=!1,this.cache=!1,this._renderPromise=Promise.resolve(),this._resize=()=>(0,d.r)(this,"content-resize")}}(0,i.Cg)([(0,r.MZ)()],m.prototype,"content",void 0),(0,i.Cg)([(0,r.MZ)({attribute:"allow-svg",type:Boolean})],m.prototype,"allowSvg",void 0),(0,i.Cg)([(0,r.MZ)({attribute:"allow-data-url",type:Boolean})],m.prototype,"allowDataUrl",void 0),(0,i.Cg)([(0,r.MZ)({type:Boolean})],m.prototype,"breaks",void 0),(0,i.Cg)([(0,r.MZ)({type:Boolean,attribute:"lazy-images"})],m.prototype,"lazyImages",void 0),(0,i.Cg)([(0,r.MZ)({type:Boolean})],m.prototype,"cache",void 0),m=(0,i.Cg)([(0,r.EM)("ha-markdown-element")],m)},3587(e,t,a){var i=a(62826),o=a(96196),r=a(44457);a(69709);class s extends o.WF{async getUpdateComplete(){const e=await super.getUpdateComplete();return await(this._markdownElement?.updateComplete),e}render(){return this.content?o.qy`<ha-markdown-element .content="${this.content}" .allowSvg="${this.allowSvg}" .allowDataUrl="${this.allowDataUrl}" .breaks="${this.breaks}" .lazyImages="${this.lazyImages}" .cache="${this.cache}"></ha-markdown-element>`:o.s6}constructor(...e){super(...e),this.allowSvg=!1,this.allowDataUrl=!1,this.breaks=!1,this.lazyImages=!1,this.cache=!1}}s.styles=o.AH`
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
      --markdown-table-border-width: attr(border, 0);
      --markdown-table-padding-inline: 0;
      --markdown-table-padding-block: 0;
      th {
        vertical-align: attr(align, center);
      }
      td {
        vertical-align: attr(align, left);
      }
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
  `,(0,i.Cg)([(0,r.MZ)()],s.prototype,"content",void 0),(0,i.Cg)([(0,r.MZ)({attribute:"allow-svg",type:Boolean})],s.prototype,"allowSvg",void 0),(0,i.Cg)([(0,r.MZ)({attribute:"allow-data-url",type:Boolean})],s.prototype,"allowDataUrl",void 0),(0,i.Cg)([(0,r.MZ)({type:Boolean})],s.prototype,"breaks",void 0),(0,i.Cg)([(0,r.MZ)({type:Boolean,attribute:"lazy-images"})],s.prototype,"lazyImages",void 0),(0,i.Cg)([(0,r.MZ)({type:Boolean})],s.prototype,"cache",void 0),(0,i.Cg)([(0,r.P)("ha-markdown-element")],s.prototype,"_markdownElement",void 0),s=(0,i.Cg)([(0,r.EM)("ha-markdown")],s)},2846(e,t,a){a.d(t,{G:()=>d,J:()=>l});var i=a(62826),o=a(97154),r=a(82553),s=a(96196),n=a(44457);a(54276);const l=[r.R,s.AH`:host{--ha-icon-display:block;--md-sys-color-primary:var(--primary-text-color);--md-sys-color-secondary:var(--secondary-text-color);--md-sys-color-surface:var(--card-background-color);--md-sys-color-on-surface:var(--primary-text-color);--md-sys-color-on-surface-variant:var(--secondary-text-color)}md-item{overflow:var(--md-item-overflow,hidden);align-items:var(--md-item-align-items,center);gap:var(--ha-md-list-item-gap,16px)}`];class d extends o.n{renderRipple(){return"text"===this.type?s.s6:s.qy`<ha-ripple part="ripple" for="item" ?disabled="${this.disabled&&"link"!==this.type}"></ha-ripple>`}}d.styles=l,d=(0,i.Cg)([(0,n.EM)("ha-md-list-item")],d)},71418(e,t,a){var i=a(62826),o=a(96196),r=a(44457);a(26300),a(75709);class s extends o.WF{render(){return o.qy`<ha-textfield .invalid="${this.invalid}" .errorMessage="${this.errorMessage}" .icon="${this.icon}" .iconTrailing="${this.iconTrailing}" .autocomplete="${this.autocomplete}" .autocorrect="${this.autocorrect}" .inputSpellcheck="${this.inputSpellcheck}" .value="${this.value}" .placeholder="${this.placeholder}" .label="${this.label}" .disabled="${this.disabled}" .required="${this.required}" .minLength="${this.minLength}" .maxLength="${this.maxLength}" .outlined="${this.outlined}" .helper="${this.helper}" .validateOnInitialRender="${this.validateOnInitialRender}" .validationMessage="${this.validationMessage}" .autoValidate="${this.autoValidate}" .pattern="${this.pattern}" .size="${this.size}" .helperPersistent="${this.helperPersistent}" .charCounter="${this.charCounter}" .endAligned="${this.endAligned}" .prefix="${this.prefix}" .name="${this.name}" .inputMode="${this.inputMode}" .readOnly="${this.readOnly}" .autocapitalize="${this.autocapitalize}" .type="${this._unmaskedPassword?"text":"password"}" .suffix="${o.qy`<div style="width:24px"></div>`}" @input="${this._handleInputEvent}" @change="${this._handleChangeEvent}"></ha-textfield> <ha-icon-button .label="${this.hass?.localize(this._unmaskedPassword?"ui.components.selectors.text.hide_password":"ui.components.selectors.text.show_password")||(this._unmaskedPassword?"Hide password":"Show password")}" @click="${this._toggleUnmaskedPassword}" .path="${this._unmaskedPassword?"M11.83,9L15,12.16C15,12.11 15,12.05 15,12A3,3 0 0,0 12,9C11.94,9 11.89,9 11.83,9M7.53,9.8L9.08,11.35C9.03,11.56 9,11.77 9,12A3,3 0 0,0 12,15C12.22,15 12.44,14.97 12.65,14.92L14.2,16.47C13.53,16.8 12.79,17 12,17A5,5 0 0,1 7,12C7,11.21 7.2,10.47 7.53,9.8M2,4.27L4.28,6.55L4.73,7C3.08,8.3 1.78,10 1,12C2.73,16.39 7,19.5 12,19.5C13.55,19.5 15.03,19.2 16.38,18.66L16.81,19.08L19.73,22L21,20.73L3.27,3M12,7A5,5 0 0,1 17,12C17,12.64 16.87,13.26 16.64,13.82L19.57,16.75C21.07,15.5 22.27,13.86 23,12C21.27,7.61 17,4.5 12,4.5C10.6,4.5 9.26,4.75 8,5.2L10.17,7.35C10.74,7.13 11.35,7 12,7Z":"M12,9A3,3 0 0,0 9,12A3,3 0 0,0 12,15A3,3 0 0,0 15,12A3,3 0 0,0 12,9M12,17A5,5 0 0,1 7,12A5,5 0 0,1 12,7A5,5 0 0,1 17,12A5,5 0 0,1 12,17M12,4.5C7,4.5 2.73,7.61 1,12C2.73,16.39 7,19.5 12,19.5C17,19.5 21.27,16.39 23,12C21.27,7.61 17,4.5 12,4.5Z"}"></ha-icon-button>`}focus(){this._textField.focus()}checkValidity(){return this._textField.checkValidity()}reportValidity(){return this._textField.reportValidity()}setCustomValidity(e){return this._textField.setCustomValidity(e)}layout(){return this._textField.layout()}_toggleUnmaskedPassword(){this._unmaskedPassword=!this._unmaskedPassword}_handleInputEvent(e){this.value=e.target.value}_handleChangeEvent(e){this.value=e.target.value,this._reDispatchEvent(e)}_reDispatchEvent(e){const t=new Event(e.type,e);this.dispatchEvent(t)}constructor(...e){super(...e),this.icon=!1,this.iconTrailing=!1,this.autocorrect=!0,this.value="",this.placeholder="",this.label="",this.disabled=!1,this.required=!1,this.minLength=-1,this.maxLength=-1,this.outlined=!1,this.helper="",this.validateOnInitialRender=!1,this.validationMessage="",this.autoValidate=!1,this.pattern="",this.size=null,this.helperPersistent=!1,this.charCounter=!1,this.endAligned=!1,this.prefix="",this.suffix="",this.name="",this.readOnly=!1,this.autocapitalize="",this._unmaskedPassword=!1}}s.styles=o.AH`:host{display:block;position:relative}ha-textfield{width:100%}ha-icon-button{position:absolute;top:8px;right:8px;inset-inline-start:initial;inset-inline-end:8px;--mdc-icon-button-size:40px;--mdc-icon-size:20px;color:var(--secondary-text-color);direction:var(--direction)}`,(0,i.Cg)([(0,r.MZ)({attribute:!1})],s.prototype,"hass",void 0),(0,i.Cg)([(0,r.MZ)({type:Boolean})],s.prototype,"invalid",void 0),(0,i.Cg)([(0,r.MZ)({attribute:"error-message"})],s.prototype,"errorMessage",void 0),(0,i.Cg)([(0,r.MZ)({type:Boolean})],s.prototype,"icon",void 0),(0,i.Cg)([(0,r.MZ)({type:Boolean})],s.prototype,"iconTrailing",void 0),(0,i.Cg)([(0,r.MZ)()],s.prototype,"autocomplete",void 0),(0,i.Cg)([(0,r.MZ)({type:Boolean})],s.prototype,"autocorrect",void 0),(0,i.Cg)([(0,r.MZ)({attribute:"input-spellcheck"})],s.prototype,"inputSpellcheck",void 0),(0,i.Cg)([(0,r.MZ)({type:String})],s.prototype,"value",void 0),(0,i.Cg)([(0,r.MZ)({type:String})],s.prototype,"placeholder",void 0),(0,i.Cg)([(0,r.MZ)({type:String})],s.prototype,"label",void 0),(0,i.Cg)([(0,r.MZ)({type:Boolean,reflect:!0})],s.prototype,"disabled",void 0),(0,i.Cg)([(0,r.MZ)({type:Boolean})],s.prototype,"required",void 0),(0,i.Cg)([(0,r.MZ)({type:Number})],s.prototype,"minLength",void 0),(0,i.Cg)([(0,r.MZ)({type:Number})],s.prototype,"maxLength",void 0),(0,i.Cg)([(0,r.MZ)({type:Boolean,reflect:!0})],s.prototype,"outlined",void 0),(0,i.Cg)([(0,r.MZ)({type:String})],s.prototype,"helper",void 0),(0,i.Cg)([(0,r.MZ)({type:Boolean})],s.prototype,"validateOnInitialRender",void 0),(0,i.Cg)([(0,r.MZ)({type:String})],s.prototype,"validationMessage",void 0),(0,i.Cg)([(0,r.MZ)({type:Boolean})],s.prototype,"autoValidate",void 0),(0,i.Cg)([(0,r.MZ)({type:String})],s.prototype,"pattern",void 0),(0,i.Cg)([(0,r.MZ)({type:Number})],s.prototype,"size",void 0),(0,i.Cg)([(0,r.MZ)({type:Boolean})],s.prototype,"helperPersistent",void 0),(0,i.Cg)([(0,r.MZ)({type:Boolean})],s.prototype,"charCounter",void 0),(0,i.Cg)([(0,r.MZ)({type:Boolean})],s.prototype,"endAligned",void 0),(0,i.Cg)([(0,r.MZ)({type:String})],s.prototype,"prefix",void 0),(0,i.Cg)([(0,r.MZ)({type:String})],s.prototype,"suffix",void 0),(0,i.Cg)([(0,r.MZ)({type:String})],s.prototype,"name",void 0),(0,i.Cg)([(0,r.MZ)({type:String,attribute:"input-mode"})],s.prototype,"inputMode",void 0),(0,i.Cg)([(0,r.MZ)({type:Boolean})],s.prototype,"readOnly",void 0),(0,i.Cg)([(0,r.MZ)({attribute:!1,type:String})],s.prototype,"autocapitalize",void 0),(0,i.Cg)([(0,r.wk)()],s.prototype,"_unmaskedPassword",void 0),(0,i.Cg)([(0,r.P)("ha-textfield")],s.prototype,"_textField",void 0),(0,i.Cg)([(0,r.Ls)({passive:!0})],s.prototype,"_handleInputEvent",null),(0,i.Cg)([(0,r.Ls)({passive:!0})],s.prototype,"_handleChangeEvent",null),s=(0,i.Cg)([(0,r.EM)("ha-password-field")],s)},45331(e,t,a){a.a(e,async function(e,t){try{var i=a(62826),o=a(93900),r=a(96196),s=a(44457),n=a(32288),l=a(1087),d=a(59992),c=a(14503),h=(a(76538),a(26300),e([o]));o=(h.then?(await h)():h)[0];const p="M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z";class g extends((0,d.V)(r.WF)){get scrollableElement(){return this.bodyContainer}updated(e){super.updated(e),e.has("open")&&(this._open=this.open)}render(){return r.qy` <wa-dialog .open="${this._open}" .lightDismiss="${!this.preventScrimClose}" without-header aria-labelledby="${(0,n.J)(this.ariaLabelledBy||(void 0!==this.headerTitle?"ha-wa-dialog-title":void 0))}" aria-describedby="${(0,n.J)(this.ariaDescribedBy)}" @wa-show="${this._handleShow}" @wa-after-show="${this._handleAfterShow}" @wa-after-hide="${this._handleAfterHide}"> <slot name="header"> <ha-dialog-header .subtitlePosition="${this.headerSubtitlePosition}" .showBorder="${this._bodyScrolled}"> <slot name="headerNavigationIcon" slot="navigationIcon"> <ha-icon-button data-dialog="close" .label="${this.hass?.localize("ui.common.close")??"Close"}" .path="${p}"></ha-icon-button> </slot> ${void 0!==this.headerTitle?r.qy`<span slot="title" class="title" id="ha-wa-dialog-title"> ${this.headerTitle} </span>`:r.qy`<slot name="headerTitle" slot="title"></slot>`} ${void 0!==this.headerSubtitle?r.qy`<span slot="subtitle">${this.headerSubtitle}</span>`:r.qy`<slot name="headerSubtitle" slot="subtitle"></slot>`} <slot name="headerActionItems" slot="actionItems"></slot> </ha-dialog-header> </slot> <div class="content-wrapper"> <div class="body ha-scrollbar" @scroll="${this._handleBodyScroll}"> <slot></slot> </div> ${this.renderScrollableFades()} </div> <slot name="footer" slot="footer"></slot> </wa-dialog> `}disconnectedCallback(){super.disconnectedCallback(),this._open=!1}_handleBodyScroll(e){this._bodyScrolled=e.target.scrollTop>0}static get styles(){return[...super.styles,c.dp,r.AH`
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
      `]}constructor(...e){super(...e),this.open=!1,this.type="standard",this.width="medium",this.preventScrimClose=!1,this.headerSubtitlePosition="below",this.flexContent=!1,this._open=!1,this._bodyScrolled=!1,this._handleShow=async()=>{this._open=!0,(0,l.r)(this,"opened"),await this.updateComplete,requestAnimationFrame(()=>{this.querySelector("[autofocus]")?.focus()})},this._handleAfterShow=()=>{(0,l.r)(this,"after-show")},this._handleAfterHide=()=>{this._open=!1,(0,l.r)(this,"closed")}}}(0,i.Cg)([(0,s.MZ)({attribute:!1})],g.prototype,"hass",void 0),(0,i.Cg)([(0,s.MZ)({attribute:"aria-labelledby"})],g.prototype,"ariaLabelledBy",void 0),(0,i.Cg)([(0,s.MZ)({attribute:"aria-describedby"})],g.prototype,"ariaDescribedBy",void 0),(0,i.Cg)([(0,s.MZ)({type:Boolean,reflect:!0})],g.prototype,"open",void 0),(0,i.Cg)([(0,s.MZ)({reflect:!0})],g.prototype,"type",void 0),(0,i.Cg)([(0,s.MZ)({type:String,reflect:!0,attribute:"width"})],g.prototype,"width",void 0),(0,i.Cg)([(0,s.MZ)({type:Boolean,reflect:!0,attribute:"prevent-scrim-close"})],g.prototype,"preventScrimClose",void 0),(0,i.Cg)([(0,s.MZ)({attribute:"header-title"})],g.prototype,"headerTitle",void 0),(0,i.Cg)([(0,s.MZ)({attribute:"header-subtitle"})],g.prototype,"headerSubtitle",void 0),(0,i.Cg)([(0,s.MZ)({type:String,attribute:"header-subtitle-position"})],g.prototype,"headerSubtitlePosition",void 0),(0,i.Cg)([(0,s.MZ)({type:Boolean,reflect:!0,attribute:"flexcontent"})],g.prototype,"flexContent",void 0),(0,i.Cg)([(0,s.wk)()],g.prototype,"_open",void 0),(0,i.Cg)([(0,s.P)(".body")],g.prototype,"bodyContainer",void 0),(0,i.Cg)([(0,s.wk)()],g.prototype,"_bodyScrolled",void 0),(0,i.Cg)([(0,s.Ls)({passive:!0})],g.prototype,"_handleBodyScroll",null),g=(0,i.Cg)([(0,s.EM)("ha-wa-dialog")],g),t()}catch(e){t(e)}})},76944(e,t,a){a.d(t,{MV:()=>s,VR:()=>r,d8:()=>i,jJ:()=>n,l3:()=>o});const i=async e=>e.callWS({type:"application_credentials/config"}),o=async(e,t)=>e.callWS({type:"application_credentials/config_entry",config_entry_id:t}),r=async e=>e.callWS({type:"application_credentials/list"}),s=async(e,t,a,i,o)=>e.callWS({type:"application_credentials/create",domain:t,client_id:a,client_secret:i,name:o}),n=async(e,t)=>e.callWS({type:"application_credentials/delete",application_credentials_id:t})},57769(e,t,a){a.d(t,{y:()=>s});const i=window;"customIconsets"in i||(i.customIconsets={});const o=i.customIconsets,r=window;"customIcons"in r||(r.customIcons={});const s=new Proxy(r.customIcons,{get:(e,t)=>e[t]??(o[t]?{getIcon:o[t]}:void 0)})},82196(e,t,a){a.a(e,async function(e,i){try{a.r(t),a.d(t,{DialogAddApplicationCredential:()=>b});a(18111),a(20116),a(61701);var o=a(62826),r=a(96196),s=a(44457),n=a(1087),l=(a(38962),a(18350)),d=(a(93444),a(44010),a(38508)),c=(a(3587),a(71418),a(65829)),h=(a(75709),a(45331)),p=a(76944),g=a(95350),f=a(14503),u=a(36918),m=e([l,d,c,h]);[l,d,c,h]=m.then?(await m)():m;const v="M14,3V5H17.59L7.76,14.83L9.17,16.24L19,6.41V10H21V3M19,19H5V5H12V3H5C3.89,3 3,3.9 3,5V19A2,2 0 0,0 5,21H19A2,2 0 0,0 21,19V12H19V19Z";class b extends r.WF{showDialog(e){this._params=e,this._domain=e.selectedDomain,this._manifest=e.manifest,this._name="",this._description="",this._clientId="",this._clientSecret="",this._error=void 0,this._loading=!1,this._open=!0,this._fetchConfig()}async _fetchConfig(){this._config=await(0,p.d8)(this.hass),this._domains=Object.keys(this._config.integrations).map(e=>({id:e,name:(0,g.p$)(this.hass.localize,e)})),await this.hass.loadBackendTranslation("application_credentials"),this._updateDescription()}render(){if(!this._params)return r.s6;const e=this._params.selectedDomain?(0,g.p$)(this.hass.localize,this._domain):"";return r.qy` <ha-wa-dialog .hass="${this.hass}" .open="${this._open}" @closed="${this._abortDialog}" .preventScrimClose="${!!(this._domain||this._name||this._clientId||this._clientSecret)}" .headerTitle="${this.hass.localize("ui.panel.config.application_credentials.editor.caption")}"> ${this._config?r.qy`<div> ${this._error?r.qy`<ha-alert alert-type="error">${this._error}</ha-alert> `:r.s6} ${this._params.selectedDomain&&!this._description?r.qy`<p> ${this.hass.localize("ui.panel.config.application_credentials.editor.missing_credentials",{integration:e})} ${this._manifest?.is_built_in||this._manifest?.documentation?r.qy`<a href="${this._manifest.is_built_in?(0,u.o)(this.hass,`/integrations/${this._domain}`):this._manifest.documentation}" target="_blank" rel="noreferrer"> ${this.hass.localize("ui.panel.config.application_credentials.editor.missing_credentials_domain_link",{integration:e})} <ha-svg-icon .path="${v}"></ha-svg-icon> </a>`:r.s6} </p>`:r.s6} ${this._params.selectedDomain&&this._description?r.s6:r.qy`<p> ${this.hass.localize("ui.panel.config.application_credentials.editor.description")} <a href="${(0,u.o)(this.hass,"/integrations/application_credentials")}" target="_blank" rel="noreferrer"> ${this.hass.localize("ui.panel.config.application_credentials.editor.view_documentation")} <ha-svg-icon .path="${v}"></ha-svg-icon> </a> </p>`} ${this._params.selectedDomain?r.s6:r.qy`<ha-generic-picker name="domain" .hass="${this.hass}" .label="${this.hass.localize("ui.panel.config.application_credentials.editor.domain")}" .value="${this._domain}" .invalid="${this._invalid&&!this._domain}" .getItems="${this._getDomainItems}" required .disabled="${!this._domains}" .valueRenderer="${this._domainRenderer}" @value-changed="${this._handleDomainPicked}" .errorMessage="${this.hass.localize("ui.common.error_required")}"></ha-generic-picker>`} ${this._description?r.qy`<ha-markdown breaks .content="${this._description}"></ha-markdown>`:r.s6} <ha-textfield class="name" name="name" .label="${this.hass.localize("ui.panel.config.application_credentials.editor.name")}" .value="${this._name}" .invalid="${this._invalid&&!this._name}" required @input="${this._handleValueChanged}" .errorMessage="${this.hass.localize("ui.common.error_required")}" dialogInitialFocus></ha-textfield> <ha-textfield class="clientId" name="clientId" .label="${this.hass.localize("ui.panel.config.application_credentials.editor.client_id")}" .value="${this._clientId}" .invalid="${this._invalid&&!this._clientId}" required @input="${this._handleValueChanged}" .errorMessage="${this.hass.localize("ui.common.error_required")}" dialogInitialFocus .helper="${this.hass.localize("ui.panel.config.application_credentials.editor.client_id_helper")}" helperPersistent></ha-textfield> <ha-password-field .label="${this.hass.localize("ui.panel.config.application_credentials.editor.client_secret")}" name="clientSecret" .value="${this._clientSecret}" .invalid="${this._invalid&&!this._clientSecret}" required @input="${this._handleValueChanged}" .errorMessage="${this.hass.localize("ui.common.error_required")}" .helper="${this.hass.localize("ui.panel.config.application_credentials.editor.client_secret_helper")}" helperPersistent></ha-password-field> </div> <ha-dialog-footer slot="footer"> <ha-button appearance="plain" slot="secondaryAction" @click="${this._closeDialog}" .disabled="${this._loading}"> ${this.hass.localize("ui.common.cancel")} </ha-button> <ha-button slot="primaryAction" @click="${this._addApplicationCredential}" .loading="${this._loading}"> ${this.hass.localize("ui.panel.config.application_credentials.editor.add")} </ha-button> </ha-dialog-footer>`:r.qy`<ha-fade-in .delay="${500}"> <ha-spinner size="large"></ha-spinner> </ha-fade-in>`} </ha-wa-dialog> `}_closeDialog(){this._open=!1}closeDialog(){this._params=void 0,this._domains=void 0,(0,n.r)(this,"dialog-closed",{dialog:this.localName})}_handleDomainPicked(e){e.stopPropagation(),this._domain=e.detail.value,this._updateDescription()}async _updateDescription(){if(!this._domain)return;await this.hass.loadBackendTranslation("application_credentials",this._domain);const e=this._config.integrations[this._domain];this._description=this.hass.localize(`component.${this._domain}.application_credentials.description`,e.description_placeholders)}_handleValueChanged(e){this._error=void 0;const t=e.target.name,a=e.target.value;this[`_${t}`]=a}_abortDialog(){this._params&&this._params.dialogAbortedCallback&&this._params.dialogAbortedCallback(),this.closeDialog()}async _addApplicationCredential(e){if(e.preventDefault(),!(this._domain&&this._name&&this._clientId&&this._clientSecret))return void(this._invalid=!0);let t;this._invalid=!1,this._loading=!0,this._error="";try{t=await(0,p.MV)(this.hass,this._domain,this._clientId,this._clientSecret,this._name)}catch(e){return this._loading=!1,void(this._error=e.message)}this._params.applicationCredentialAddedCallback(t),this.closeDialog()}static get styles(){return[f.nA,r.AH`ha-dialog{--mdc-dialog-max-width:500px;--dialog-z-index:10}.row{display:flex;padding:var(--ha-space-2) 0}ha-textfield{display:block;margin-top:var(--ha-space-4);margin-bottom:var(--ha-space-4)}a{text-decoration:none}a ha-svg-icon{--mdc-icon-size:16px}ha-markdown{margin-top:var(--ha-space-4);margin-bottom:var(--ha-space-4)}ha-fade-in{display:flex;width:100%;justify-content:center}`]}constructor(...e){super(...e),this._loading=!1,this._open=!1,this._invalid=!1,this._getDomainItems=()=>this._domains?.map(e=>({id:e.id,primary:e.name,sorting_label:e.name}))??[],this._domainRenderer=e=>{const t=this._domains?.find(t=>t.id===e);return r.qy`<span slot="headline">${t?t.name:e}</span>`}}}(0,o.Cg)([(0,s.MZ)({attribute:!1})],b.prototype,"hass",void 0),(0,o.Cg)([(0,s.wk)()],b.prototype,"_loading",void 0),(0,o.Cg)([(0,s.wk)()],b.prototype,"_error",void 0),(0,o.Cg)([(0,s.wk)()],b.prototype,"_params",void 0),(0,o.Cg)([(0,s.wk)()],b.prototype,"_domain",void 0),(0,o.Cg)([(0,s.wk)()],b.prototype,"_manifest",void 0),(0,o.Cg)([(0,s.wk)()],b.prototype,"_name",void 0),(0,o.Cg)([(0,s.wk)()],b.prototype,"_description",void 0),(0,o.Cg)([(0,s.wk)()],b.prototype,"_clientId",void 0),(0,o.Cg)([(0,s.wk)()],b.prototype,"_clientSecret",void 0),(0,o.Cg)([(0,s.wk)()],b.prototype,"_domains",void 0),(0,o.Cg)([(0,s.wk)()],b.prototype,"_config",void 0),(0,o.Cg)([(0,s.wk)()],b.prototype,"_open",void 0),(0,o.Cg)([(0,s.wk)()],b.prototype,"_invalid",void 0),b=(0,o.Cg)([(0,s.EM)("dialog-add-application-credential")],b),i()}catch(e){i(e)}})},996(e,t,a){a.d(t,{G:()=>i});class i{get(e){return this._cache.get(e)}set(e,t){this._cache.set(e,t),this._expiration&&window.setTimeout(()=>this._cache.delete(e),this._expiration)}has(e){return this._cache.has(e)}constructor(e){this._cache=new Map,this._expiration=e}}},36918(e,t,a){a.d(t,{o:()=>i});const i=(e,t)=>`https://${e.config.version.includes("b")?"rc":e.config.version.includes("dev")?"next":"www"}.home-assistant.io${t}`},22348(e,t,a){a.d(t,{V:()=>o});var i=a(37177);const o=e=>!!e.auth.external&&i.n},37177(e,t,a){a.d(t,{n:()=>i});const i=/^((?!chrome|android).)*safari/i.test(navigator.userAgent)},96175(e,t,a){var i={"./ha-icon-prev":["89133","61982"],"./ha-icon-button-toolbar":["9882","52074","76775"],"./ha-alert":["38962","19695"],"./ha-icon-button-toggle":["62501","77254"],"./ha-svg-icon.ts":["67094"],"./ha-alert.ts":["38962","19695"],"./ha-icon":["88945","51146"],"./ha-icon-next.ts":["43661","63902"],"./ha-qr-code.ts":["60543","51343","62740"],"./ha-icon-overflow-menu.ts":["75248","46095","52074","22016","29499","56297"],"./ha-icon-button-toggle.ts":["62501","77254"],"./ha-icon-button-group":["39826","13647"],"./ha-svg-icon":["67094"],"./ha-icon-button-prev":["45100","99197"],"./ha-icon-button.ts":["26300"],"./ha-icon-overflow-menu":["75248","46095","52074","22016","29499","56297"],"./ha-icon-button-arrow-next":["99028","54101"],"./ha-icon-button-prev.ts":["45100","99197"],"./ha-icon-picker":["64138","44533","7199","46095","92769","52074","44966","80445","87234"],"./ha-icon-button-toolbar.ts":["9882","52074","76775"],"./ha-icon-button-arrow-prev.ts":["90248","17041"],"./ha-icon-button-next":["25440","81049"],"./ha-icon-next":["43661","63902"],"./ha-icon-picker.ts":["64138","44533","7199","46095","92769","52074","44966","80445","87234"],"./ha-icon-prev.ts":["89133","61982"],"./ha-icon-button-arrow-prev":["90248","17041"],"./ha-icon-button-next.ts":["25440","81049"],"./ha-icon.ts":["88945","51146"],"./ha-qr-code":["60543","51343","62740"],"./ha-icon-button":["26300"],"./ha-icon-button-group.ts":["39826","13647"],"./ha-icon-button-arrow-next.ts":["99028","54101"]};function o(e){if(!a.o(i,e))return Promise.resolve().then(function(){var t=new Error("Cannot find module '"+e+"'");throw t.code="MODULE_NOT_FOUND",t});var t=i[e],o=t[0];return Promise.all(t.slice(1).map(a.e)).then(function(){return a(o)})}o.keys=()=>Object.keys(i),o.id=96175,e.exports=o}};
//# sourceMappingURL=87772.b939c426dd16bc13.js.map