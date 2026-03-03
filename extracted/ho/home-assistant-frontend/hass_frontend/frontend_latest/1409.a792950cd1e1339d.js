export const __rspack_esm_id="1409";export const __rspack_esm_ids=["1409"];export const __webpack_modules__={26218(e,a,t){t.d(a,{a:()=>r});const o=(0,t(77796).n)(e=>{history.replaceState({scrollPosition:e},"")},300);function r(e){return(a,t)=>{if("object"==typeof t)throw new Error("This decorator does not support this compilation type.");const r=a.connectedCallback;a.connectedCallback=function(){r.call(this);const a=this[t];a&&this.updateComplete.then(()=>{const t=this.renderRoot.querySelector(e);t&&setTimeout(()=>{t.scrollTop=a},0)})};const i=Object.getOwnPropertyDescriptor(a,t);let n;if(void 0===i)n={get(){return this[`__${String(t)}`]||history.state?.scrollPosition},set(e){o(e),this[`__${String(t)}`]=e},configurable:!0,enumerable:!0};else{const e=i.set;n={...i,set(a){o(a),this[`__${String(t)}`]=a,e?.call(this,a)}}}Object.defineProperty(a,t,n)}}},77796(e,a,t){t.d(a,{n:()=>o});const o=(e,a,t=!0,o=!0)=>{let r,i=0;const n=(...n)=>{const s=()=>{i=!1===t?0:Date.now(),r=void 0,e(...n)},l=Date.now();i||!1!==t||(i=l);const c=a-(l-i);c<=0||c>a?(r&&(clearTimeout(r),r=void 0),i=l,e(...n)):r||!1===o||(r=window.setTimeout(s,c))};return n.cancel=()=>{clearTimeout(r),r=void 0,i=0},n}},38962(e,a,t){t.a(e,async function(e,o){try{t.r(a);var r=t(62826),i=t(96196),n=t(97735),s=t(94333),l=t(1087),c=t(26300),h=(t(67094),e([c]));c=(h.then?(await h)():h)[0];const d="M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z",p={info:"M11,9H13V7H11M12,20C7.59,20 4,16.41 4,12C4,7.59 7.59,4 12,4C16.41,4 20,7.59 20,12C20,16.41 16.41,20 12,20M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M11,17H13V11H11V17Z",warning:"M12,2L1,21H23M12,6L19.53,19H4.47M11,10V14H13V10M11,16V18H13V16",error:"M11,15H13V17H11V15M11,7H13V13H11V7M12,2C6.47,2 2,6.5 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M12,20A8,8 0 0,1 4,12A8,8 0 0,1 12,4A8,8 0 0,1 20,12A8,8 0 0,1 12,20Z",success:"M20,12A8,8 0 0,1 12,20A8,8 0 0,1 4,12A8,8 0 0,1 12,4C12.76,4 13.5,4.11 14.2,4.31L15.77,2.74C14.61,2.26 13.34,2 12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12M7.91,10.08L6.5,11.5L11,16L21,6L19.59,4.58L11,13.17L7.91,10.08Z"};class g extends i.WF{render(){return i.qy` <div class="issue-type ${(0,s.H)({[this.alertType]:!0})}" role="alert"> <div class="icon ${this.title?"":"no-title"}"> <slot name="icon"> <ha-svg-icon .path="${p[this.alertType]}"></ha-svg-icon> </slot> </div> <div class="${(0,s.H)({content:!0,narrow:this.narrow})}"> <div class="main-content"> ${this.title?i.qy`<div class="title">${this.title}</div>`:i.s6} <slot></slot> </div> <div class="action"> <slot name="action"> ${this.dismissable?i.qy`<ha-icon-button @click="${this._dismissClicked}" label="Dismiss alert" .path="${d}"></ha-icon-button>`:i.s6} </slot> </div> </div> </div> `}_dismissClicked(){(0,l.r)(this,"alert-dismissed-clicked")}constructor(...e){super(...e),this.title="",this.alertType="info",this.dismissable=!1,this.narrow=!1}}g.styles=i.AH`.issue-type{position:relative;padding:8px;display:flex}.icon{height:var(--ha-alert-icon-size,24px);width:var(--ha-alert-icon-size,24px)}.issue-type::after{position:absolute;top:0;right:0;bottom:0;left:0;opacity:.12;pointer-events:none;content:"";border-radius:var(--ha-border-radius-sm)}.icon.no-title{align-self:center}.content{display:flex;justify-content:space-between;align-items:center;width:100%;text-align:var(--float-start)}.content.narrow{flex-direction:column;align-items:flex-end}.action{z-index:1;width:min-content;--mdc-theme-primary:var(--primary-text-color)}.main-content{overflow-wrap:anywhere;word-break:break-word;line-height:normal;margin-left:8px;margin-right:0;margin-inline-start:8px;margin-inline-end:8px}.title{margin-top:2px;font-weight:var(--ha-font-weight-bold)}.action ha-icon-button{--mdc-theme-primary:var(--primary-text-color);--ha-icon-button-size:36px}.issue-type.info>.icon{color:var(--info-color)}.issue-type.info::after{background-color:var(--info-color)}.issue-type.warning>.icon{color:var(--warning-color)}.issue-type.warning::after{background-color:var(--warning-color)}.issue-type.error>.icon{color:var(--error-color)}.issue-type.error::after{background-color:var(--error-color)}.issue-type.success>.icon{color:var(--success-color)}.issue-type.success::after{background-color:var(--success-color)}:host ::slotted(ul){margin:0;padding-inline-start:20px}`,(0,r.Cg)([(0,n.MZ)()],g.prototype,"title",void 0),(0,r.Cg)([(0,n.MZ)({attribute:"alert-type"})],g.prototype,"alertType",void 0),(0,r.Cg)([(0,n.MZ)({type:Boolean})],g.prototype,"dismissable",void 0),(0,r.Cg)([(0,n.MZ)({type:Boolean})],g.prototype,"narrow",void 0),g=(0,r.Cg)([(0,n.EM)("ha-alert")],g),o()}catch(e){o(e)}})},76776(e,a,t){var o=t(62826),r=t(96196),i=t(97735);class n extends r.WF{render(){return r.qy` ${this.header?r.qy`<h1 class="card-header">${this.header}</h1>`:r.s6} <slot></slot> `}constructor(...e){super(...e),this.raised=!1}}n.styles=r.AH`:host{background:var(--ha-card-background,var(--card-background-color,#fff));-webkit-backdrop-filter:var(--ha-card-backdrop-filter,none);backdrop-filter:var(--ha-card-backdrop-filter,none);box-shadow:var(--ha-card-box-shadow,none);box-sizing:border-box;border-radius:var(--ha-card-border-radius,var(--ha-border-radius-lg));border-width:var(--ha-card-border-width,1px);border-style:solid;border-color:var(--ha-card-border-color,var(--divider-color,#e0e0e0));color:var(--primary-text-color);display:block;transition:all .3s ease-out;position:relative}:host([raised]){border:none;box-shadow:var(--ha-card-box-shadow,0px 2px 1px -1px rgba(0,0,0,.2),0px 1px 1px 0px rgba(0,0,0,.14),0px 1px 3px 0px rgba(0,0,0,.12))}.card-header,:host ::slotted(.card-header){color:var(--ha-card-header-color,var(--primary-text-color));font-family:var(--ha-card-header-font-family, inherit);font-size:var(--ha-card-header-font-size, var(--ha-font-size-2xl));letter-spacing:-.012em;line-height:var(--ha-line-height-expanded);padding:var(--ha-space-3) var(--ha-space-4) var(--ha-space-4);display:block;margin-block-start:0;margin-block-end:0;font-weight:var(--ha-font-weight-normal)}
    :host
      ::slotted(
        .card-content:not(:nth-child(1 of .card-content, .card-header))
      ),
    slot:not(:first-child)::slotted(.card-content) {
      padding-top: 0;
      margin-top: calc(var(--ha-space-2) * -1);
    }
    :host ::slotted(.card-content){padding:var(--ha-space-4)}:host ::slotted(.card-actions){border-top:1px solid var(--divider-color,#e8e8e8);padding:var(--ha-space-2)}`,(0,o.Cg)([(0,i.MZ)()],n.prototype,"header",void 0),(0,o.Cg)([(0,i.MZ)({type:Boolean,reflect:!0})],n.prototype,"raised",void 0),n=(0,o.Cg)([(0,i.EM)("ha-card")],n)},90248(e,a,t){t.a(e,async function(e,o){try{t.r(a),t.d(a,{HaIconButtonArrowPrev:()=>p});var r=t(62826),i=t(96196),n=t(97735),s=t(63091),l=t(26300),c=e([l]);l=(c.then?(await c)():c)[0];const h="M20,11V13H8L13.5,18.5L12.08,19.92L4.16,12L12.08,4.08L13.5,5.5L8,11H20Z",d="M4,11V13H16L10.5,18.5L11.92,19.92L19.84,12L11.92,4.08L10.5,5.5L16,11H4Z";class p extends i.WF{render(){return i.qy` <ha-icon-button .disabled="${this.disabled}" .label="${this.label||this.hass?.localize("ui.common.back")||"Back"}" .path="${this._icon}" .href="${this.href}" .target="${this.target}" .rel="${this.rel}" .download="${this.download}"></ha-icon-button> `}constructor(...e){super(...e),this.disabled=!1,this._icon="rtl"===s.G.document.dir?d:h}}(0,r.Cg)([(0,n.MZ)({attribute:!1})],p.prototype,"hass",void 0),(0,r.Cg)([(0,n.MZ)({type:Boolean})],p.prototype,"disabled",void 0),(0,r.Cg)([(0,n.MZ)()],p.prototype,"label",void 0),(0,r.Cg)([(0,n.MZ)()],p.prototype,"href",void 0),(0,r.Cg)([(0,n.MZ)()],p.prototype,"target",void 0),(0,r.Cg)([(0,n.MZ)()],p.prototype,"rel",void 0),(0,r.Cg)([(0,n.MZ)()],p.prototype,"download",void 0),(0,r.Cg)([(0,n.wk)()],p.prototype,"_icon",void 0),p=(0,r.Cg)([(0,n.EM)("ha-icon-button-arrow-prev")],p),o()}catch(e){o(e)}})},26300(e,a,t){t.a(e,async function(e,o){try{t.r(a),t.d(a,{HaIconButton:()=>h});var r=t(62826),i=t(96196),n=t(97735),s=t(32288),l=t(18350),c=(t(67094),e([l]));l=(c.then?(await c)():c)[0];class h extends i.WF{render(){return i.qy` <ha-button appearance="plain" variant="neutral" aria-label="${(0,s.J)(this.label)}" title="${(0,s.J)(this.hideTitle?void 0:this.label)}" aria-haspopup="${(0,s.J)(this.ariaHasPopup)}" .disabled="${this.disabled}" .iconTag="${this.path?"ha-svg-icon":"span"}" .href="${this.href}" .target="${this.target}" .rel="${this.rel}" .download="${this.download}"> ${this.path?i.qy`<ha-svg-icon .path="${this.path}"></ha-svg-icon>`:i.qy`<span><slot></slot></span>`} </ha-button> `}constructor(...e){super(...e),this.disabled=!1,this.hideTitle=!1,this.selected=!1}}h.shadowRootOptions={mode:"open",delegatesFocus:!0},h.styles=i.AH`:host{display:inline-block;outline:0;--ha-button-height:var(--ha-icon-button-size, 48px)}ha-button{position:relative;isolation:isolate;--wa-form-control-padding-inline:var(
        --ha-icon-button-padding-inline,
        --ha-space-2
      );--wa-color-on-normal:currentColor;--wa-color-fill-quiet:transparent;--ha-button-label-overflow:visible}ha-button::after{content:"";position:absolute;inset:0;z-index:-1;border-radius:50%;background-color:currentColor;opacity:0;pointer-events:none}ha-button::part(base){width:var(--wa-form-control-height);aspect-ratio:1;outline-offset:-4px}ha-button::part(label){display:flex}:host([selected]) ha-button::after{opacity:.1}@media (hover:hover){:host(:hover:not([disabled])) ha-button::after{opacity:.1}}`,(0,r.Cg)([(0,n.MZ)({type:Boolean,reflect:!0})],h.prototype,"disabled",void 0),(0,r.Cg)([(0,n.MZ)({type:String})],h.prototype,"path",void 0),(0,r.Cg)([(0,n.MZ)({type:String})],h.prototype,"label",void 0),(0,r.Cg)([(0,n.MZ)({type:String,attribute:"aria-haspopup"})],h.prototype,"ariaHasPopup",void 0),(0,r.Cg)([(0,n.MZ)({attribute:"hide-title",type:Boolean})],h.prototype,"hideTitle",void 0),(0,r.Cg)([(0,n.MZ)({type:Boolean,reflect:!0})],h.prototype,"selected",void 0),(0,r.Cg)([(0,n.MZ)()],h.prototype,"href",void 0),(0,r.Cg)([(0,n.MZ)()],h.prototype,"target",void 0),(0,r.Cg)([(0,n.MZ)()],h.prototype,"rel",void 0),(0,r.Cg)([(0,n.MZ)()],h.prototype,"download",void 0),h=(0,r.Cg)([(0,n.EM)("ha-icon-button")],h),o()}catch(e){o(e)}})},69709(e,a,t){t(18111),t(22489),t(61701),t(18237);var o=t(62826),r=t(96196),i=t(97735),n=t(1420),s=t(30015),l=t.n(s),c=t(1087),h=(t(14603),t(47566),t(98721),t(2209));let d;var p=t(996);const g=e=>r.qy`${e}`,v=new p.G(1e3),b={reType:/(?<input>(\[!(?<type>caution|important|note|tip|warning)\])(?:\s|\\n)?)/i,typeToHaAlert:{caution:"error",important:"info",note:"info",tip:"success",warning:"warning"}};class m extends r.mN{disconnectedCallback(){if(super.disconnectedCallback(),this.cache){const e=this._computeCacheKey();v.set(e,this.innerHTML)}}createRenderRoot(){return this}update(e){super.update(e),void 0!==this.content&&(this._renderPromise=this._render())}async getUpdateComplete(){return await super.getUpdateComplete(),await this._renderPromise,!0}willUpdate(e){if(!this.innerHTML&&this.cache){const e=this._computeCacheKey();v.has(e)&&((0,r.XX)(g((0,n._)(v.get(e))),this.renderRoot),this._resize())}}_computeCacheKey(){return l()({content:this.content,allowSvg:this.allowSvg,allowDataUrl:this.allowDataUrl,breaks:this.breaks})}async _render(){const e=await(async(e,a,o)=>(d||(d=(0,h.LV)(new Worker(new URL(t.p+t.u("55640"),t.b)))),d.renderMarkdown(e,a,o)))(String(this.content),{breaks:this.breaks,gfm:!0},{allowSvg:this.allowSvg,allowDataUrl:this.allowDataUrl});(0,r.XX)(g((0,n._)(e.join(""))),this.renderRoot),this._resize();const a=document.createTreeWalker(this,NodeFilter.SHOW_ELEMENT,null);for(;a.nextNode();){const e=a.currentNode;if(e instanceof HTMLAnchorElement&&e.host!==document.location.host)e.target="_blank",e.rel="noreferrer noopener";else if(e instanceof HTMLImageElement)this.lazyImages&&(e.loading="lazy"),e.addEventListener("load",this._resize);else if(e instanceof HTMLQuoteElement){const t=e.firstElementChild?.firstChild?.textContent&&b.reType.exec(e.firstElementChild.firstChild.textContent);if(t){const{type:o}=t.groups,r=document.createElement("ha-alert");r.alertType=b.typeToHaAlert[o.toLowerCase()],r.append(...Array.from(e.childNodes).map(e=>{const a=Array.from(e.childNodes);if(!this.breaks&&a.length){const e=a[0];e.nodeType===Node.TEXT_NODE&&e.textContent===t.input&&e.textContent?.includes("\n")&&(e.textContent=e.textContent.split("\n").slice(1).join("\n"))}return a}).reduce((e,a)=>e.concat(a),[]).filter(e=>e.textContent&&e.textContent!==t.input)),a.parentNode().replaceChild(r,e)}}else e instanceof HTMLElement&&["ha-alert","ha-qr-code","ha-icon","ha-svg-icon"].includes(e.localName)&&t(96175)(`./${e.localName}`)}}constructor(...e){super(...e),this.allowSvg=!1,this.allowDataUrl=!1,this.breaks=!1,this.lazyImages=!1,this.cache=!1,this._renderPromise=Promise.resolve(),this._resize=()=>(0,c.r)(this,"content-resize")}}(0,o.Cg)([(0,i.MZ)()],m.prototype,"content",void 0),(0,o.Cg)([(0,i.MZ)({attribute:"allow-svg",type:Boolean})],m.prototype,"allowSvg",void 0),(0,o.Cg)([(0,i.MZ)({attribute:"allow-data-url",type:Boolean})],m.prototype,"allowDataUrl",void 0),(0,o.Cg)([(0,i.MZ)({type:Boolean})],m.prototype,"breaks",void 0),(0,o.Cg)([(0,i.MZ)({type:Boolean,attribute:"lazy-images"})],m.prototype,"lazyImages",void 0),(0,o.Cg)([(0,i.MZ)({type:Boolean})],m.prototype,"cache",void 0),m=(0,o.Cg)([(0,i.EM)("ha-markdown-element")],m)},3587(e,a,t){var o=t(62826),r=t(96196),i=t(97735);t(69709);class n extends r.WF{async getUpdateComplete(){const e=await super.getUpdateComplete();return await(this._markdownElement?.updateComplete),e}render(){return this.content?r.qy`<ha-markdown-element .content="${this.content}" .allowSvg="${this.allowSvg}" .allowDataUrl="${this.allowDataUrl}" .breaks="${this.breaks}" .lazyImages="${this.lazyImages}" .cache="${this.cache}"></ha-markdown-element>`:r.s6}constructor(...e){super(...e),this.allowSvg=!1,this.allowDataUrl=!1,this.breaks=!1,this.lazyImages=!1,this.cache=!1}}n.styles=r.AH`
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
  `,(0,o.Cg)([(0,i.MZ)()],n.prototype,"content",void 0),(0,o.Cg)([(0,i.MZ)({attribute:"allow-svg",type:Boolean})],n.prototype,"allowSvg",void 0),(0,o.Cg)([(0,i.MZ)({attribute:"allow-data-url",type:Boolean})],n.prototype,"allowDataUrl",void 0),(0,o.Cg)([(0,i.MZ)({type:Boolean})],n.prototype,"breaks",void 0),(0,o.Cg)([(0,i.MZ)({type:Boolean,attribute:"lazy-images"})],n.prototype,"lazyImages",void 0),(0,o.Cg)([(0,i.MZ)({type:Boolean})],n.prototype,"cache",void 0),(0,o.Cg)([(0,i.P)("ha-markdown-element")],n.prototype,"_markdownElement",void 0),n=(0,o.Cg)([(0,i.EM)("ha-markdown")],n)},2054(e,a,t){t.a(e,async function(e,a){try{var o=t(62826),r=t(96196),i=t(97735),n=t(1087),s=t(44249),l=t(26300),c=e([l]);l=(c.then?(await c)():c)[0];const h="M3,6H21V8H3V6M3,11H21V13H3V11M3,16H21V18H3V16Z";class d extends r.WF{connectedCallback(){super.connectedCallback(),this._attachNotifOnConnect&&(this._attachNotifOnConnect=!1,this._subscribeNotifications())}disconnectedCallback(){super.disconnectedCallback(),this._unsubNotifications&&(this._attachNotifOnConnect=!0,this._unsubNotifications(),this._unsubNotifications=void 0)}render(){if(!this._show)return r.s6;const e=this._hasNotifications&&(this.narrow||"always_hidden"===this.hass.dockedSidebar);return r.qy` <ha-icon-button .label="${this.hass.localize("ui.sidebar.sidebar_toggle")}" .path="${h}" @click="${this._toggleMenu}"></ha-icon-button> ${e?r.qy`<div class="dot"></div>`:""} `}willUpdate(e){if(super.willUpdate(e),!e.has("narrow")&&!e.has("hass"))return;const a=e.has("hass")?e.get("hass"):this.hass,t=e.has("narrow")?e.get("narrow"):this.narrow,o=!1===a?.kioskMode&&(t||"always_hidden"===a?.dockedSidebar),r=!1===this.hass.kioskMode&&(this.narrow||"always_hidden"===this.hass.dockedSidebar);this.hasUpdated&&o===r||(this._show=r||this._alwaysVisible,r?this._subscribeNotifications():this._unsubNotifications&&(this._unsubNotifications(),this._unsubNotifications=void 0))}_subscribeNotifications(){if(this._unsubNotifications)throw new Error("Already subscribed");this._unsubNotifications=(0,s.V)(this.hass.connection,e=>{this._hasNotifications=e.length>0})}_toggleMenu(){(0,n.r)(this,"hass-toggle-menu")}constructor(...e){super(...e),this.narrow=!1,this._hasNotifications=!1,this._show=!1,this._alwaysVisible=!1,this._attachNotifOnConnect=!1}}d.styles=r.AH`:host{position:relative}.dot{pointer-events:none;position:absolute;background-color:var(--accent-color);width:12px;height:12px;top:9px;right:7px;inset-inline-end:7px;inset-inline-start:initial;border-radius:var(--ha-border-radius-circle);border:2px solid var(--app-header-background-color)}`,(0,o.Cg)([(0,i.MZ)({type:Boolean})],d.prototype,"narrow",void 0),(0,o.Cg)([(0,i.MZ)({attribute:!1})],d.prototype,"hass",void 0),(0,o.Cg)([(0,i.wk)()],d.prototype,"_hasNotifications",void 0),(0,o.Cg)([(0,i.wk)()],d.prototype,"_show",void 0),d=(0,o.Cg)([(0,i.EM)("ha-menu-button")],d),a()}catch(e){a(e)}})},67094(e,a,t){t.r(a),t.d(a,{HaSvgIcon:()=>n});var o=t(62826),r=t(96196),i=t(97735);class n extends r.WF{render(){return r.JW` <svg viewBox="${this.viewBox||"0 0 24 24"}" preserveAspectRatio="xMidYMid meet" focusable="false" role="img" aria-hidden="true"> <g> ${this.path?r.JW`<path class="primary-path" d="${this.path}"></path>`:r.s6} ${this.secondaryPath?r.JW`<path class="secondary-path" d="${this.secondaryPath}"></path>`:r.s6} </g> </svg>`}}n.styles=r.AH`:host{display:var(--ha-icon-display,inline-flex);align-items:center;justify-content:center;position:relative;vertical-align:middle;fill:var(--icon-primary-color,currentcolor);width:var(--mdc-icon-size,24px);height:var(--mdc-icon-size,24px)}svg{width:100%;height:100%;pointer-events:none;display:block}path.primary-path{opacity:var(--icon-primary-opactity, 1)}path.secondary-path{fill:var(--icon-secondary-color,currentcolor);opacity:var(--icon-secondary-opactity, .5)}`,(0,o.Cg)([(0,i.MZ)()],n.prototype,"path",void 0),(0,o.Cg)([(0,i.MZ)({attribute:!1})],n.prototype,"secondaryPath",void 0),(0,o.Cg)([(0,i.MZ)({attribute:!1})],n.prototype,"viewBox",void 0),n=(0,o.Cg)([(0,i.EM)("ha-svg-icon")],n)},59646(e,a,t){var o=t(62826),r=t(4845),i=t(49065),n=t(96196),s=t(97735),l=t(88360);class c extends r.U{firstUpdated(){super.firstUpdated(),this.addEventListener("change",()=>{this.haptic&&(0,l.j)(this,"light")})}constructor(...e){super(...e),this.haptic=!1}}c.styles=[i.R,n.AH`:host{--mdc-theme-secondary:var(--switch-checked-color)}.mdc-switch.mdc-switch--checked .mdc-switch__thumb{background-color:var(--switch-checked-button-color);border-color:var(--switch-checked-button-color)}.mdc-switch.mdc-switch--checked .mdc-switch__track{background-color:var(--switch-checked-track-color);border-color:var(--switch-checked-track-color)}.mdc-switch:not(.mdc-switch--checked) .mdc-switch__thumb{background-color:var(--switch-unchecked-button-color);border-color:var(--switch-unchecked-button-color)}.mdc-switch:not(.mdc-switch--checked) .mdc-switch__track{background-color:var(--switch-unchecked-track-color);border-color:var(--switch-unchecked-track-color)}`],(0,o.Cg)([(0,s.MZ)({type:Boolean})],c.prototype,"haptic",void 0),c=(0,o.Cg)([(0,s.EM)("ha-switch")],c)},93758(e,a,t){t.d(a,{CO:()=>h,NS:()=>c,f$:()=>i,ok:()=>n});var o=t(35518),r=t(9899);const i=async e=>(await e.callWS({type:"labs/list"})).features,n=(e,a,t,o,r)=>e.callWS({type:"labs/update",domain:a,preview_feature:t,enabled:o,...void 0!==r&&{create_backup:r}}),s=e=>e.sendMessagePromise({type:"labs/list"}).then(e=>e.features),l=(e,a)=>e.subscribeEvents((0,r.s)(()=>s(e).then(e=>a.setState(e,!0)),500,!0),"labs_updated"),c=(e,a)=>(0,o.N)("_labFeatures",s,l,e,a),h=(e,a,t,o)=>e.subscribeMessage(o,{type:"labs/subscribe",domain:a,preview_feature:t})},44249(e,a,t){t.d(a,{V:()=>o});const o=(e,a)=>{const t=new r,o=e.subscribeMessage(e=>a(t.processMessage(e)),{type:"persistent_notification/subscribe"});return()=>{o.then(e=>e?.())}};class r{processMessage(e){if("removed"===e.type)for(const a of Object.keys(e.notifications))delete this.notifications[a];else this.notifications={...this.notifications,...e.notifications};return Object.values(this.notifications)}constructor(){this.notifications={}}}},81310(e,a,t){t.a(e,async function(e,a){try{var o=t(62826),r=t(96196),i=t(97735),n=t(94333),s=t(26218),l=t(91926),c=t(90248),h=t(2054),d=t(14503),p=e([c,h]);[c,h]=p.then?(await p)():p;class g extends r.WF{render(){return r.qy` <div class="toolbar ${(0,n.H)({narrow:this.narrow})}"> <div class="toolbar-content"> ${this.mainPage||history.state?.root?r.qy` <ha-menu-button .hass="${this.hass}" .narrow="${this.narrow}"></ha-menu-button> `:this.backPath?r.qy` <ha-icon-button-arrow-prev href="${this.backPath}" .hass="${this.hass}"></ha-icon-button-arrow-prev> `:r.qy` <ha-icon-button-arrow-prev .hass="${this.hass}" @click="${this._backTapped}"></ha-icon-button-arrow-prev> `} <div class="main-title"> <slot name="header">${this.header}</slot> </div> <slot name="toolbar-icon"></slot> </div> </div> <div class="content ha-scrollbar" @scroll="${this._saveScrollPos}"> <slot></slot> </div> <div id="fab"> <slot name="fab"></slot> </div> `}_saveScrollPos(e){this._savedScrollPos=e.target.scrollTop}_backTapped(){this.backCallback?this.backCallback():(0,l.O)()}static get styles(){return[d.dp,r.AH`:host{display:block;height:100%;background-color:var(--primary-background-color);overflow:hidden;position:relative}:host([narrow]){width:100%;position:fixed}.toolbar{background-color:var(--app-header-background-color);padding-top:var(--safe-area-inset-top);padding-right:var(--safe-area-inset-right)}:host([narrow]) .toolbar{padding-left:var(--safe-area-inset-left)}.toolbar-content{display:flex;align-items:center;font-size:var(--ha-font-size-xl);height:var(--header-height);font-weight:var(--ha-font-weight-normal);color:var(--app-header-text-color,#fff);border-bottom:var(--app-header-border-bottom,none);box-sizing:border-box;padding:8px 12px}.toolbar a{color:var(--sidebar-text-color);text-decoration:none}::slotted([slot=toolbar-icon]),ha-icon-button-arrow-prev,ha-menu-button{display:flex;align-items:center;pointer-events:auto;color:var(--sidebar-icon-color)}.main-title{margin-inline-start:var(--ha-space-6);line-height:var(--ha-line-height-normal);min-width:0;flex-grow:1;overflow-wrap:break-word;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;text-overflow:ellipsis}.narrow .main-title{margin-inline-start:var(--ha-space-2)}.content{position:relative;width:calc(100% - var(--safe-area-inset-right,0px));height:calc(100% - 1px - var(--header-height,0px) - var(--safe-area-inset-top,0px) - var(--safe-area-inset-bottom,0px));padding-bottom:var(--safe-area-inset-bottom,0px);margin-right:var(--safe-area-inset-right);overflow-y:auto;overflow:auto;-webkit-overflow-scrolling:touch}:host([narrow]) .content{width:calc(100% - var(--safe-area-inset-left,0px) - var(--safe-area-inset-right,0px));margin-left:var(--safe-area-inset-left)}#fab{position:absolute;right:calc(16px + var(--safe-area-inset-right,0px));inset-inline-end:calc(16px + var(--safe-area-inset-right,0px));inset-inline-start:initial;bottom:calc(16px + var(--safe-area-inset-bottom,0px));z-index:1;display:flex;flex-wrap:wrap;justify-content:flex-end;gap:var(--ha-space-2)}:host([narrow]) #fab.tabs{bottom:calc(84px + var(--safe-area-inset-bottom,0px))}#fab[is-wide]{bottom:calc(24px + var(--safe-area-inset-bottom,0px));right:calc(24px + var(--safe-area-inset-right,0px));inset-inline-end:calc(24px + var(--safe-area-inset-right,0px));inset-inline-start:initial}`]}constructor(...e){super(...e),this.mainPage=!1,this.narrow=!1}}(0,o.Cg)([(0,i.MZ)({attribute:!1})],g.prototype,"hass",void 0),(0,o.Cg)([(0,i.MZ)()],g.prototype,"header",void 0),(0,o.Cg)([(0,i.MZ)({type:Boolean,attribute:"main-page"})],g.prototype,"mainPage",void 0),(0,o.Cg)([(0,i.MZ)({type:String,attribute:"back-path"})],g.prototype,"backPath",void 0),(0,o.Cg)([(0,i.MZ)({attribute:!1})],g.prototype,"backCallback",void 0),(0,o.Cg)([(0,i.MZ)({type:Boolean,reflect:!0})],g.prototype,"narrow",void 0),(0,o.Cg)([(0,s.a)(".content")],g.prototype,"_savedScrollPos",void 0),(0,o.Cg)([(0,i.Ls)({passive:!0})],g.prototype,"_saveScrollPos",null),g=(0,o.Cg)([(0,i.EM)("hass-subpage")],g),a()}catch(e){a(e)}})},78040(e,a,t){t.a(e,async function(e,o){try{t.r(a);t(18111),t(61701),t(17642),t(58004),t(33853),t(45876),t(32475),t(15024),t(31698);var r=t(62826),i=t(96196),n=t(97735),s=t(22786),l=t(6030),c=t(38962),h=t(18350),d=(t(76776),t(26300)),p=(t(3587),t(59646),t(95350)),g=t(93758),v=t(65063),b=t(81310),m=t(54706),u=t(14503),f=t(44144),w=t(36918),y=t(81619),x=t(56072),k=t(32854),_=e([c,h,d,b]);[c,h,d,b]=_.then?(await _)():_;const C="M6,22A3,3 0 0,1 3,19C3,18.4 3.18,17.84 3.5,17.37L9,7.81V6A1,1 0 0,1 8,5V4A2,2 0 0,1 10,2H14A2,2 0 0,1 16,4V5A1,1 0 0,1 15,6V7.81L20.5,17.37C20.82,17.84 21,18.4 21,19A3,3 0 0,1 18,22H6M5,19A1,1 0 0,0 6,20H18A1,1 0 0,0 19,19C19,18.79 18.93,18.59 18.82,18.43L16.53,14.47L14,17L8.93,11.93L5.18,18.43C5.07,18.59 5,18.79 5,19M13,10A1,1 0 0,0 12,11A1,1 0 0,0 13,12A1,1 0 0,0 14,11A1,1 0 0,0 13,10Z",$="M11,18H13V16H11V18M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M12,20C7.59,20 4,16.41 4,12C4,7.59 7.59,4 12,4C16.41,4 20,7.59 20,12C20,16.41 16.41,20 12,20M12,6A4,4 0 0,0 8,10H10A2,2 0 0,1 12,8A2,2 0 0,1 14,10C14,12 11,11.75 11,15H13C13,12.75 16,12.5 16,10A4,4 0 0,0 12,6Z",M="M14,3V5H17.59L7.76,14.83L9.17,16.24L19,6.41V10H21V3M19,19H5V5H12V3H5C3.89,3 3,3.9 3,5V19A2,2 0 0,0 5,21H19A2,2 0 0,0 21,19V12H19V19Z";class z extends((0,m.E)(i.WF)){hassSubscribe(){return[(0,g.NS)(this.hass.connection,e=>{const a=[...new Set(e.map(e=>e.domain))];this.hass.loadBackendTranslation("title",a),this.hass.loadBackendTranslation("preview_features",a),this._preview_features=e})]}firstUpdated(e){super.firstUpdated(e),this.hass.loadBackendTranslation("preview_features"),this._handleUrlParams()}_handleUrlParams(){const e=(0,l.p9)("domain"),a=(0,l.p9)("preview_feature");if(e&&a){const t=`${e}.${a}`;this._highlightedPreviewFeature=t,this.updateComplete.then(()=>{this._scrollToPreviewFeature(t)})}}render(){const e=this._sortedPreviewFeatures(this.hass.localize,this._preview_features);return i.qy` <hass-subpage .hass="${this.hass}" .narrow="${this.narrow}" back-path="/config/system" .header="${this.hass.localize("ui.panel.config.labs.caption")}"> ${e.length?i.qy` <ha-icon-button slot="toolbar-icon" .href="${(0,w.o)(this.hass,"/integrations/labs/")}" target="_blank" rel="noopener noreferrer" .title="${this.hass.localize("ui.common.help")}" .label="${this.hass.localize("ui.common.help")}" .path="${$}"></ha-icon-button> `:i.s6} <div class="content"> ${e.length?i.qy` <ha-card outlined> <div class="card-content intro-card"> <h1> ${this.hass.localize("ui.panel.config.labs.intro_title")} </h1> <p class="intro-text"> ${this.hass.localize("ui.panel.config.labs.intro_description")} </p> <ha-alert alert-type="warning"> ${this.hass.localize("ui.panel.config.labs.intro_warning")} </ha-alert> </div> </ha-card> ${e.map(e=>this._renderPreviewFeature(e))} `:i.qy` <div class="empty"> <ha-svg-icon .path="${C}"></ha-svg-icon> <h1> ${this.hass.localize("ui.panel.config.labs.empty.title")} </h1> ${this.hass.localize("ui.panel.config.labs.empty.description")} <a href="${(0,w.o)(this.hass,"/integrations/labs/")}" target="_blank" rel="noopener noreferrer"> ${this.hass.localize("ui.panel.config.labs.learn_more")} <ha-svg-icon .path="${M}"></ha-svg-icon> </a> </div> `} </div> </hass-subpage> `}_renderPreviewFeature(e){const a=`${e.domain}.${e.preview_feature}`,t=this.hass.localize(`component.${e.domain}.preview_features.${e.preview_feature}.name`),o=this.hass.localize(`component.${e.domain}.preview_features.${e.preview_feature}.description`),r=(0,p.p$)(this.hass.localize,e.domain),n=e.is_built_in?r:`${r} • ${this.hass.localize("ui.panel.config.labs.custom_integration")}`,s=this._highlightedPreviewFeature===a,l=e.learn_more_url?`${o}\n\n[${this.hass.localize("ui.panel.config.labs.learn_more")}](${e.learn_more_url})`:o;return i.qy` <ha-card outlined data-feature-id="${a}" class="${s?"highlighted":""}"> <div class="card-content"> <div class="card-header"> <img alt="" src="${(0,f.MR)({domain:e.domain,type:"icon",darkOptimized:this.hass.themes?.darkMode})}" crossorigin="anonymous" referrerpolicy="no-referrer"> <div class="feature-title"> <span class="integration-name">${n}</span> <h2>${t}</h2> </div> </div> <ha-markdown .content="${l}" breaks></ha-markdown> </div> <div class="card-actions"> <div> ${e.feedback_url?i.qy` <ha-button appearance="plain" href="${e.feedback_url}" target="_blank" rel="noopener noreferrer"> ${this.hass.localize("ui.panel.config.labs.provide_feedback")} </ha-button> `:i.s6} ${e.report_issue_url?i.qy` <ha-button appearance="plain" href="${e.report_issue_url}" target="_blank" rel="noopener noreferrer"> ${this.hass.localize("ui.panel.config.labs.report_issue")} </ha-button> `:i.s6} </div> <ha-button appearance="filled" .variant="${e.enabled?"danger":"brand"}" @click="${this._handleToggle}" .preview_feature="${e}"> ${this.hass.localize(e.enabled?"ui.panel.config.labs.disable":"ui.panel.config.labs.enable")} </ha-button> </div> </ha-card> `}_scrollToPreviewFeature(e){const a=this.shadowRoot?.querySelector(`[data-feature-id="${e}"]`);a&&(a.scrollIntoView({behavior:"smooth",block:"center"}),setTimeout(()=>{this._highlightedPreviewFeature=void 0},3e3))}async _handleToggle(e){const a=e.currentTarget.preview_feature,t=!a.enabled,o=`${a.domain}.${a.preview_feature}`;if(t)return void(0,x.R)(this,{preview_feature:a,previewFeatureId:o,onConfirm:async e=>{await this._performToggle(o,t,e)}});await(0,v.dk)(this,{title:this.hass.localize("ui.panel.config.labs.disable_title"),text:this.hass.localize(`component.${a.domain}.preview_features.${a.preview_feature}.disable_confirmation`)||this.hass.localize("ui.panel.config.labs.disable_confirmation"),confirmText:this.hass.localize("ui.panel.config.labs.disable"),dismissText:this.hass.localize("ui.common.cancel"),destructive:!0})&&await this._performToggle(o,t,!1)}async _performToggle(e,a,t){t&&(0,k.xX)(this,{enabled:a});const o=e.split(".",2);if(2!==o.length)return void(0,y.P)(this,{message:this.hass.localize("ui.common.unknown_error")});const[r,i]=o;try{await(0,g.ok)(this.hass,r,i,a,t)}catch(e){t&&(0,k.MD)();const o=e?.message||this.hass.localize("ui.common.unknown_error");return void(0,y.P)(this,{message:this.hass.localize(a?"ui.panel.config.labs.enable_failed":"ui.panel.config.labs.disable_failed",{error:o})})}t&&(0,k.MD)(),(0,y.P)(this,{message:this.hass.localize(a?"ui.panel.config.labs.enabled_success":"ui.panel.config.labs.disabled_success")})}constructor(...e){super(...e),this.narrow=!1,this._preview_features=[],this._sortedPreviewFeatures=(0,s.A)((e,a)=>[...a].sort((a,t)=>"frontend"===a.domain&&"winter_mode"===a.preview_feature?1:"frontend"===t.domain&&"winter_mode"===t.preview_feature?-1:(0,p.p$)(e,a.domain).localeCompare((0,p.p$)(e,t.domain))))}}z.styles=[u.RF,i.AH`:host{display:block;height:100%}ha-icon-button[slot=toolbar-icon]{color:var(--sidebar-icon-color)}.content{max-width:800px;margin:0 auto;padding:var(--ha-space-4);display:flex;flex-direction:column}.content:has(.empty){justify-content:center}ha-card{margin-bottom:var(--ha-space-4);position:relative;transition:box-shadow .3s ease}ha-card.highlighted{animation:highlight-fade 2.5s ease-out forwards}@keyframes highlight-fade{0%{box-shadow:0 0 0 var(--ha-border-width-md) var(--primary-color),0 0 var(--ha-shadow-blur-lg) rgba(var(--rgb-primary-color),.4)}100%{box-shadow:0 0 0 var(--ha-border-width-md) transparent,0 0 0 transparent}}.intro-card{display:flex;flex-direction:column;gap:var(--ha-space-4)}.intro-card h1{margin:0}.intro-text{margin:0 0 var(--ha-space-3)}.card-content{padding:var(--ha-space-4)}.card-header{display:flex;gap:var(--ha-space-3);margin-bottom:var(--ha-space-4);align-items:flex-start}.card-header img{width:38px;height:38px;flex-shrink:0;margin-top:2px}.feature-title{flex:1;min-width:0}.feature-title h2{margin:0;line-height:1.3}.integration-name{display:block;margin-bottom:2px;font-size:14px;color:var(--secondary-text-color)}.empty{max-width:500px;margin:0 auto;padding:var(--ha-space-12) var(--ha-space-4);text-align:center}.empty ha-svg-icon{width:120px;height:120px;color:var(--secondary-text-color);opacity:.3}.empty h1{margin:var(--ha-space-6) 0 var(--ha-space-4)}.empty p{margin:0 0 var(--ha-space-6);font-size:16px;line-height:24px;color:var(--secondary-text-color)}.empty a{display:inline-flex;align-items:center;gap:var(--ha-space-1);color:var(--primary-color);text-decoration:none;font-weight:500}.empty a:hover{text-decoration:underline}.empty a:focus-visible{outline:var(--ha-border-width-md) solid var(--primary-color);outline-offset:2px;border-radius:var(--ha-border-radius-sm)}.empty a ha-svg-icon{width:16px;height:16px;opacity:1}.card-actions{display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:var(--ha-space-2);padding:var(--ha-space-2);border-top:var(--ha-border-width-sm) solid var(--divider-color)}.card-actions>div{display:flex;flex-wrap:wrap;gap:var(--ha-space-2)}`],(0,r.Cg)([(0,n.MZ)({attribute:!1})],z.prototype,"hass",void 0),(0,r.Cg)([(0,n.MZ)({type:Boolean})],z.prototype,"narrow",void 0),(0,r.Cg)([(0,n.wk)()],z.prototype,"_preview_features",void 0),(0,r.Cg)([(0,n.wk)()],z.prototype,"_highlightedPreviewFeature",void 0),z=(0,r.Cg)([(0,n.EM)("ha-config-labs")],z),o()}catch(e){o(e)}})},56072(e,a,t){t.d(a,{R:()=>i});var o=t(1087);const r=()=>Promise.all([t.e("46095"),t.e("79996"),t.e("5967"),t.e("7901")]).then(t.bind(t,56588)),i=(e,a)=>{(0,o.r)(e,"show-dialog",{dialogTag:"dialog-labs-preview-feature-enable",dialogImport:r,dialogParams:a})}},32854(e,a,t){t.d(a,{MD:()=>s,xX:()=>n});var o=t(1087),r=t(22444);const i=()=>Promise.all([t.e("11921"),t.e("10167")]).then(t.bind(t,95338)),n=(e,a)=>{(0,o.r)(e,"show-dialog",{dialogTag:"dialog-labs-progress",dialogImport:i,dialogParams:a})},s=()=>(0,r.zU)("dialog-labs-progress")},14503(e,a,t){t.d(a,{RF:()=>i,dp:()=>l,kO:()=>s,nA:()=>n,og:()=>r});var o=t(96196);const r=o.AH`button.link{background:0 0;color:inherit;border:none;padding:0;font:inherit;text-align:left;text-decoration:underline;cursor:pointer;outline:0}`,i=o.AH`:host{font-family:var(--ha-font-family-body);-webkit-font-smoothing:var(--ha-font-smoothing);-moz-osx-font-smoothing:var(--ha-moz-osx-font-smoothing);font-size:var(--ha-font-size-m);font-weight:var(--ha-font-weight-normal);line-height:var(--ha-line-height-normal)}app-header div[sticky]{height:48px}app-toolbar [main-title]{margin-left:20px;margin-inline-start:20px;margin-inline-end:initial}.header{transition:box-shadow .2s linear,width var(--ha-animation-duration-normal) ease,padding-left var(--ha-animation-duration-normal) ease,padding-right var(--ha-animation-duration-normal) ease}@media (prefers-reduced-motion:reduce){.header{transition:box-shadow .2s linear}}h1{font-family:var(--ha-font-family-heading);-webkit-font-smoothing:var(--ha-font-smoothing);-moz-osx-font-smoothing:var(--ha-moz-osx-font-smoothing);font-size:var(--ha-font-size-2xl);font-weight:var(--ha-font-weight-normal);line-height:var(--ha-line-height-condensed)}h2{font-family:var(--ha-font-family-body);-webkit-font-smoothing:var(--ha-font-smoothing);-moz-osx-font-smoothing:var(--ha-moz-osx-font-smoothing);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;font-size:var(--ha-font-size-xl);font-weight:var(--ha-font-weight-medium);line-height:var(--ha-line-height-normal)}h3{font-family:var(--ha-font-family-body);-webkit-font-smoothing:var(--ha-font-smoothing);-moz-osx-font-smoothing:var(--ha-moz-osx-font-smoothing);font-size:var(--ha-font-size-l);font-weight:var(--ha-font-weight-normal);line-height:var(--ha-line-height-normal)}a{color:var(--primary-color)}.secondary{color:var(--secondary-text-color)}.error{color:var(--error-color)}.warning{color:var(--error-color)}${r} .card-actions a{text-decoration:none}.card-actions .warning{--mdc-theme-primary:var(--error-color)}.layout.horizontal,.layout.vertical{display:flex}.layout.inline{display:inline-flex}.layout.horizontal{flex-direction:row}.layout.vertical{flex-direction:column}.layout.wrap{flex-wrap:wrap}.layout.no-wrap{flex-wrap:nowrap}.layout.center,.layout.center-center{align-items:center}.layout.bottom{align-items:flex-end}.layout.center-center,.layout.center-justified{justify-content:center}.flex{flex:1;flex-basis:0.000000001px}.flex-auto{flex:1 1 auto}.flex-none{flex:none}.layout.justified{justify-content:space-between}`,n=o.AH`
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
    )}@media all and (max-width:450px),all and (max-height:500px){ha-adaptive-dialog,ha-dialog{--dialog-surface-margin-top:0px;--mdc-dialog-min-height:100vh;--mdc-dialog-min-height:100svh;--mdc-dialog-max-height:100vh;--mdc-dialog-max-height:100svh;--ha-dialog-max-height:100vh;--ha-dialog-max-height:100svh}}`,l=o.AH`.ha-scrollbar::-webkit-scrollbar{width:.4rem;height:.4rem}.ha-scrollbar::-webkit-scrollbar-thumb{border-radius:var(--ha-border-radius-sm);background:var(--scrollbar-thumb-color)}.ha-scrollbar{overflow-y:auto;scrollbar-color:var(--scrollbar-thumb-color) transparent;scrollbar-width:thin}`;o.AH`body{background-color:var(--primary-background-color);color:var(--primary-text-color);height:calc(100vh - 32px);width:100vw}`},996(e,a,t){t.d(a,{G:()=>o});t(45367),t(92731);class o{get(e){return this._cache.get(e)}set(e,a){this._cache.set(e,a),this._expiration&&window.setTimeout(()=>this._cache.delete(e),this._expiration)}has(e){return this._cache.has(e)}constructor(e){this._cache=new Map,this._expiration=e}}},36918(e,a,t){t.d(a,{o:()=>o});const o=(e,a)=>`https://${e.config.version.includes("b")?"rc":e.config.version.includes("dev")?"next":"www"}.home-assistant.io${a}`},96175(e,a,t){var o={"./ha-icon-prev":["89133","61982"],"./ha-icon-button-toolbar":["9882","30628","76775"],"./ha-alert":["38962","19695"],"./ha-icon-button-toggle":["62501","77254"],"./ha-svg-icon.ts":["67094"],"./ha-alert.ts":["38962","19695"],"./ha-icon":["88945","51146"],"./ha-icon-next.ts":["43661","63902"],"./ha-qr-code.ts":["60543","51343","62740"],"./ha-icon-overflow-menu.ts":["75248","30628","34995","85545"],"./ha-icon-button-toggle.ts":["62501","77254"],"./ha-icon-button-group":["39826","13647"],"./ha-svg-icon":["67094"],"./ha-icon-button-prev":["45100","99197"],"./ha-icon-button.ts":["26300"],"./ha-icon-overflow-menu":["75248","30628","34995","85545"],"./ha-icon-button-arrow-next":["99028","54101"],"./ha-icon-button-prev.ts":["45100","99197"],"./ha-icon-picker":["64138","46095","31065","30628","92769","62453","78398","70744"],"./ha-icon-button-toolbar.ts":["9882","30628","76775"],"./ha-icon-button-arrow-prev.ts":["90248","17041"],"./ha-icon-button-next":["25440","81049"],"./ha-icon-next":["43661","63902"],"./ha-icon-picker.ts":["64138","46095","31065","30628","92769","62453","78398","70744"],"./ha-icon-prev.ts":["89133","61982"],"./ha-icon-button-arrow-prev":["90248","17041"],"./ha-icon-button-next.ts":["25440","81049"],"./ha-icon.ts":["88945","51146"],"./ha-qr-code":["60543","51343","62740"],"./ha-icon-button":["26300"],"./ha-icon-button-group.ts":["39826","13647"],"./ha-icon-button-arrow-next.ts":["99028","54101"]};function r(e){if(!t.o(o,e))return Promise.resolve().then(function(){var a=new Error("Cannot find module '"+e+"'");throw a.code="MODULE_NOT_FOUND",a});var a=o[e],r=a[0];return Promise.all(a.slice(1).map(t.e)).then(function(){return t(r)})}r.keys=()=>Object.keys(o),r.id=96175,e.exports=r}};
//# sourceMappingURL=1409.a792950cd1e1339d.js.map