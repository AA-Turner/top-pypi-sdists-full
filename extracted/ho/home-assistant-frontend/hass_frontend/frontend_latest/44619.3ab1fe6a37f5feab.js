/*! For license information please see 44619.3ab1fe6a37f5feab.js.LICENSE.txt */
export const __rspack_esm_id="44619";export const __rspack_esm_ids=["44619"];export const __webpack_modules__={69709(e,t,n){n(18111),n(22489),n(61701),n(18237);var o=n(62826),r=n(96196),a=n(44457),i=n(1420),s=n(30015),l=n.n(s),c=n(1087),h=(n(14603),n(47566),n(98721),n(2209));let d;var p=n(996);const u=e=>r.qy`${e}`,g=new p.G(1e3),m={reType:/(?<input>(\[!(?<type>caution|important|note|tip|warning)\])(?:\s|\\n)?)/i,typeToHaAlert:{caution:"error",important:"info",note:"info",tip:"success",warning:"warning"}};class w extends r.mN{disconnectedCallback(){if(super.disconnectedCallback(),this.cache){const e=this._computeCacheKey();g.set(e,this.innerHTML)}}createRenderRoot(){return this}update(e){super.update(e),void 0!==this.content&&(this._renderPromise=this._render())}async getUpdateComplete(){return await super.getUpdateComplete(),await this._renderPromise,!0}willUpdate(e){if(!this.innerHTML&&this.cache){const e=this._computeCacheKey();g.has(e)&&((0,r.XX)(u((0,i._)(g.get(e))),this.renderRoot),this._resize())}}_computeCacheKey(){return l()({content:this.content,allowSvg:this.allowSvg,allowDataUrl:this.allowDataUrl,breaks:this.breaks})}async _render(){const e=await(async(e,t,o)=>(d||(d=(0,h.LV)(new Worker(new URL(n.p+n.u("55640"),n.b)))),d.renderMarkdown(e,t,o)))(String(this.content),{breaks:this.breaks,gfm:!0},{allowSvg:this.allowSvg,allowDataUrl:this.allowDataUrl});(0,r.XX)(u((0,i._)(e.join(""))),this.renderRoot),this._resize();const t=document.createTreeWalker(this,NodeFilter.SHOW_ELEMENT,null);for(;t.nextNode();){const e=t.currentNode;if(e instanceof HTMLAnchorElement&&e.host!==document.location.host)e.target="_blank",e.rel="noreferrer noopener";else if(e instanceof HTMLImageElement)this.lazyImages&&(e.loading="lazy"),e.addEventListener("load",this._resize);else if(e instanceof HTMLQuoteElement){const n=e.firstElementChild?.firstChild?.textContent&&m.reType.exec(e.firstElementChild.firstChild.textContent);if(n){const{type:o}=n.groups,r=document.createElement("ha-alert");r.alertType=m.typeToHaAlert[o.toLowerCase()],r.append(...Array.from(e.childNodes).map(e=>{const t=Array.from(e.childNodes);if(!this.breaks&&t.length){const e=t[0];e.nodeType===Node.TEXT_NODE&&e.textContent===n.input&&e.textContent?.includes("\n")&&(e.textContent=e.textContent.split("\n").slice(1).join("\n"))}return t}).reduce((e,t)=>e.concat(t),[]).filter(e=>e.textContent&&e.textContent!==n.input)),t.parentNode().replaceChild(r,e)}}else e instanceof HTMLElement&&["ha-alert","ha-qr-code","ha-icon","ha-svg-icon"].includes(e.localName)&&n(96175)(`./${e.localName}`)}}constructor(...e){super(...e),this.allowSvg=!1,this.allowDataUrl=!1,this.breaks=!1,this.lazyImages=!1,this.cache=!1,this._renderPromise=Promise.resolve(),this._resize=()=>(0,c.r)(this,"content-resize")}}(0,o.Cg)([(0,a.MZ)()],w.prototype,"content",void 0),(0,o.Cg)([(0,a.MZ)({attribute:"allow-svg",type:Boolean})],w.prototype,"allowSvg",void 0),(0,o.Cg)([(0,a.MZ)({attribute:"allow-data-url",type:Boolean})],w.prototype,"allowDataUrl",void 0),(0,o.Cg)([(0,a.MZ)({type:Boolean})],w.prototype,"breaks",void 0),(0,o.Cg)([(0,a.MZ)({type:Boolean,attribute:"lazy-images"})],w.prototype,"lazyImages",void 0),(0,o.Cg)([(0,a.MZ)({type:Boolean})],w.prototype,"cache",void 0),w=(0,o.Cg)([(0,a.EM)("ha-markdown-element")],w)},3587(e,t,n){var o=n(62826),r=n(96196),a=n(44457);n(69709);class i extends r.WF{async getUpdateComplete(){const e=await super.getUpdateComplete();return await(this._markdownElement?.updateComplete),e}render(){return this.content?r.qy`<ha-markdown-element .content="${this.content}" .allowSvg="${this.allowSvg}" .allowDataUrl="${this.allowDataUrl}" .breaks="${this.breaks}" .lazyImages="${this.lazyImages}" .cache="${this.cache}"></ha-markdown-element>`:r.s6}constructor(...e){super(...e),this.allowSvg=!1,this.allowDataUrl=!1,this.breaks=!1,this.lazyImages=!1,this.cache=!1}}i.styles=r.AH`
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
  `,(0,o.Cg)([(0,a.MZ)()],i.prototype,"content",void 0),(0,o.Cg)([(0,a.MZ)({attribute:"allow-svg",type:Boolean})],i.prototype,"allowSvg",void 0),(0,o.Cg)([(0,a.MZ)({attribute:"allow-data-url",type:Boolean})],i.prototype,"allowDataUrl",void 0),(0,o.Cg)([(0,a.MZ)({type:Boolean})],i.prototype,"breaks",void 0),(0,o.Cg)([(0,a.MZ)({type:Boolean,attribute:"lazy-images"})],i.prototype,"lazyImages",void 0),(0,o.Cg)([(0,a.MZ)({type:Boolean})],i.prototype,"cache",void 0),(0,o.Cg)([(0,a.P)("ha-markdown-element")],i.prototype,"_markdownElement",void 0),i=(0,o.Cg)([(0,a.EM)("ha-markdown")],i)},84334(e,t,n){n.d(t,{H:()=>r,R:()=>o});const o=(e,t,n)=>e.subscribeMessage(e=>t(e),{type:"render_template",...n}),r=(e,t,n,o,r)=>e.connection.subscribeMessage(r,{type:"template/start_preview",flow_id:t,flow_type:n,user_input:o})},67334(e,t,n){n.r(t),n.d(t,{HuiMarkdownCard:()=>u});var o=n(62826),r=n(96196),a=n(44457),i=n(94333),s=n(30015),l=n.n(s),c=n(42372),h=n(1087),d=(n(38962),n(76776),n(3587),n(84334));const p=new(n(996).G)(1e3);class u extends r.WF{static async getConfigElement(){return await n.e("90742").then(n.bind(n,4757)),document.createElement("hui-markdown-card-editor")}static getStubConfig(){return{type:"markdown",content:"The **Markdown** card allows you to write any text. You can style it **bold**, *italicized*, ~strikethrough~ etc. You can do images, links, and more.\n\nFor more information see the [Markdown Cheatsheet](https://commonmark.org/help)."}}getCardSize(){return void 0===this._config?3:void 0===this._config.card_size?Math.round(this._config.content.split("\n").length/2)+(this._config.title?1:0):this._config.card_size}setConfig(e){if(!e.content)throw new Error("Content required");this._config?.content!==e.content&&this._tryDisconnect(),this._config=e}connectedCallback(){super.connectedCallback(),this._tryConnect()}_computeCacheKey(){return l()(this._config)}disconnectedCallback(){if(super.disconnectedCallback(),this._tryDisconnect(),this._config&&this._templateResult){const e=this._computeCacheKey();p.set(e,this._templateResult)}}willUpdate(e){if(super.willUpdate(e),this._config&&!this._templateResult){const e=this._computeCacheKey();p.has(e)&&(this._templateResult=p.get(e))}}render(){return this._config?r.qy` ${this._error?r.qy` <ha-alert .alertType="${this._errorLevel?.toLowerCase()||"error"}"> ${this._error} </ha-alert> `:r.s6} <ha-card .header="${this._config.text_only?void 0:this._config.title}" class="${(0,i.H)({"with-header":!!this._config.title,"text-only":this._config.text_only??!1})}"> <ha-markdown cache breaks .content="${this._templateResult?.result}"></ha-markdown> </ha-card> `:r.s6}updated(e){if(super.updated(e),!this._config||!this.hass)return;e.has("_config")&&this._tryConnect();const t=!!this._templateResult&&!1===this._config.show_empty&&0===this._templateResult.result.length;t!==this.hidden&&(this.style.display=t?"none":"",this.toggleAttribute("hidden",t),(0,h.r)(this,"card-visibility-changed",{value:!t}));const n=e.get("hass"),o=e.get("_config");n&&o&&n.themes===this.hass.themes&&o.theme===this._config.theme||(0,c.Q)(this,this.hass.themes,this._config.theme)}async _tryConnect(){if(void 0===this._unsubRenderTemplate&&this.hass&&this._config){this._error=void 0,this._errorLevel=void 0;try{this._unsubRenderTemplate=(0,d.R)(this.hass.connection,e=>{"error"in e?"ERROR"!==e.level&&"ERROR"===this._errorLevel||(this._error=e.error,this._errorLevel=e.level):this._templateResult=e},{template:this._config.content,entity_ids:this._config.entity_id,variables:{config:this._config,user:this.hass.user.name},strict:!0,report_errors:this.preview}),await this._unsubRenderTemplate}catch(e){this.preview&&(this._error=e.message,this._errorLevel=void 0),this._templateResult={result:this._config.content,listeners:{all:!1,domains:[],entities:[],time:!1}},this._unsubRenderTemplate=void 0}}}async _tryDisconnect(){this._unsubRenderTemplate&&(this._unsubRenderTemplate.then(e=>e()).catch(),this._unsubRenderTemplate=void 0,this._error=void 0,this._errorLevel=void 0)}constructor(...e){super(...e),this.preview=!1}}u.styles=r.AH`ha-card{height:100%;overflow-y:auto}ha-alert{margin-bottom:8px}ha-markdown{padding:16px;word-wrap:break-word;text-align:var(--card-text-align,inherit)}.with-header ha-markdown{padding:0 16px 16px}.text-only{background:0 0;box-shadow:none;border:none}.text-only ha-markdown{padding:2px 4px}`,(0,o.Cg)([(0,a.MZ)({attribute:!1})],u.prototype,"hass",void 0),(0,o.Cg)([(0,a.MZ)({type:Boolean})],u.prototype,"preview",void 0),(0,o.Cg)([(0,a.wk)()],u.prototype,"_config",void 0),(0,o.Cg)([(0,a.wk)()],u.prototype,"_error",void 0),(0,o.Cg)([(0,a.wk)()],u.prototype,"_errorLevel",void 0),(0,o.Cg)([(0,a.wk)()],u.prototype,"_templateResult",void 0),u=(0,o.Cg)([(0,a.EM)("hui-markdown-card")],u)},996(e,t,n){n.d(t,{G:()=>o});class o{get(e){return this._cache.get(e)}set(e,t){this._cache.set(e,t),this._expiration&&window.setTimeout(()=>this._cache.delete(e),this._expiration)}has(e){return this._cache.has(e)}constructor(e){this._cache=new Map,this._expiration=e}}},96175(e,t,n){var o={"./ha-icon-prev":["89133","61982"],"./ha-icon-button-toolbar":["9882","52074","76775"],"./ha-alert":["38962","19695"],"./ha-icon-button-toggle":["62501","77254"],"./ha-svg-icon.ts":["67094"],"./ha-alert.ts":["38962","19695"],"./ha-icon":["88945","51146"],"./ha-icon-next.ts":["43661","63902"],"./ha-qr-code.ts":["60543","51343","62740"],"./ha-icon-overflow-menu.ts":["75248","46095","52074","22016","29499","56297"],"./ha-icon-button-toggle.ts":["62501","77254"],"./ha-icon-button-group":["39826","13647"],"./ha-svg-icon":["67094"],"./ha-icon-button-prev":["45100","99197"],"./ha-icon-button.ts":["26300"],"./ha-icon-overflow-menu":["75248","46095","52074","22016","29499","56297"],"./ha-icon-button-arrow-next":["99028","54101"],"./ha-icon-button-prev.ts":["45100","99197"],"./ha-icon-picker":["64138","44533","7199","46095","92769","52074","44966","80445","87234"],"./ha-icon-button-toolbar.ts":["9882","52074","76775"],"./ha-icon-button-arrow-prev.ts":["90248","17041"],"./ha-icon-button-next":["25440","81049"],"./ha-icon-next":["43661","63902"],"./ha-icon-picker.ts":["64138","44533","7199","46095","92769","52074","44966","80445","87234"],"./ha-icon-prev.ts":["89133","61982"],"./ha-icon-button-arrow-prev":["90248","17041"],"./ha-icon-button-next.ts":["25440","81049"],"./ha-icon.ts":["88945","51146"],"./ha-qr-code":["60543","51343","62740"],"./ha-icon-button":["26300"],"./ha-icon-button-group.ts":["39826","13647"],"./ha-icon-button-arrow-next.ts":["99028","54101"]};function r(e){if(!n.o(o,e))return Promise.resolve().then(function(){var t=new Error("Cannot find module '"+e+"'");throw t.code="MODULE_NOT_FOUND",t});var t=o[e],r=t[0];return Promise.all(t.slice(1).map(n.e)).then(function(){return n(r)})}r.keys=()=>Object.keys(o),r.id=96175,e.exports=r},2209(e,t,n){n.d(t,{LV:()=>p});n(18111),n(61701),n(18237);const o=Symbol("Comlink.proxy"),r=Symbol("Comlink.endpoint"),a=Symbol("Comlink.releaseProxy"),i=Symbol("Comlink.finalizer"),s=Symbol("Comlink.thrown"),l=e=>"object"==typeof e&&null!==e||"function"==typeof e,c=new Map([["proxy",{canHandle:e=>l(e)&&e[o],serialize(e){const{port1:t,port2:n}=new MessageChannel;return h(e,t),[n,[n]]},deserialize:e=>(e.start(),p(e))}],["throw",{canHandle:e=>l(e)&&s in e,serialize({value:e}){let t;return t=e instanceof Error?{isError:!0,value:{message:e.message,name:e.name,stack:e.stack}}:{isError:!1,value:e},[t,[]]},deserialize(e){if(e.isError)throw Object.assign(new Error(e.value.message),e.value);throw e.value}}]]);function h(e,t=globalThis,n=["*"]){t.addEventListener("message",function r(a){if(!a||!a.data)return;if(!function(e,t){for(const n of e){if(t===n||"*"===n)return!0;if(n instanceof RegExp&&n.test(t))return!0}return!1}(n,a.origin))return void console.warn(`Invalid origin '${a.origin}' for comlink proxy`);const{id:l,type:c,path:p}=Object.assign({path:[]},a.data),u=(a.data.argumentList||[]).map(_);let g;try{const t=p.slice(0,-1).reduce((e,t)=>e[t],e),n=p.reduce((e,t)=>e[t],e);switch(c){case"GET":g=n;break;case"SET":t[p.slice(-1)[0]]=_(a.data.value),g=!0;break;case"APPLY":g=n.apply(t,u);break;case"CONSTRUCT":g=function(e){return Object.assign(e,{[o]:!0})}(new n(...u));break;case"ENDPOINT":{const{port1:t,port2:n}=new MessageChannel;h(e,n),g=function(e,t){return y.set(e,t),e}(t,[t])}break;case"RELEASE":g=void 0;break;default:return}}catch(e){g={value:e,[s]:0}}Promise.resolve(g).catch(e=>({value:e,[s]:0})).then(n=>{const[o,a]=f(n);t.postMessage(Object.assign(Object.assign({},o),{id:l}),a),"RELEASE"===c&&(t.removeEventListener("message",r),d(t),i in e&&"function"==typeof e[i]&&e[i]())}).catch(e=>{const[n,o]=f({value:new TypeError("Unserializable return value"),[s]:0});t.postMessage(Object.assign(Object.assign({},n),{id:l}),o)})}),t.start&&t.start()}function d(e){(function(e){return"MessagePort"===e.constructor.name})(e)&&e.close()}function p(e,t){const n=new Map;return e.addEventListener("message",function(e){const{data:t}=e;if(!t||!t.id)return;const o=n.get(t.id);if(o)try{o(t)}finally{n.delete(t.id)}}),v(e,n,[],t)}function u(e){if(e)throw new Error("Proxy has been released and is not useable")}function g(e){return k(e,new Map,{type:"RELEASE"}).then(()=>{d(e)})}const m=new WeakMap,w="FinalizationRegistry"in globalThis&&new FinalizationRegistry(e=>{const t=(m.get(e)||0)-1;m.set(e,t),0===t&&g(e)});function v(e,t,n=[],o=function(){}){let i=!1;const s=new Proxy(o,{get(o,r){if(u(i),r===a)return()=>{!function(e){w&&w.unregister(e)}(s),g(e),t.clear(),i=!0};if("then"===r){if(0===n.length)return{then:()=>s};const o=k(e,t,{type:"GET",path:n.map(e=>e.toString())}).then(_);return o.then.bind(o)}return v(e,t,[...n,r])},set(o,r,a){u(i);const[s,l]=f(a);return k(e,t,{type:"SET",path:[...n,r].map(e=>e.toString()),value:s},l).then(_)},apply(o,a,s){u(i);const l=n[n.length-1];if(l===r)return k(e,t,{type:"ENDPOINT"}).then(_);if("bind"===l)return v(e,t,n.slice(0,-1));const[c,h]=b(s);return k(e,t,{type:"APPLY",path:n.map(e=>e.toString()),argumentList:c},h).then(_)},construct(o,r){u(i);const[a,s]=b(r);return k(e,t,{type:"CONSTRUCT",path:n.map(e=>e.toString()),argumentList:a},s).then(_)}});return function(e,t){const n=(m.get(t)||0)+1;m.set(t,n),w&&w.register(e,t,e)}(s,e),s}function b(e){const t=e.map(f);return[t.map(e=>e[0]),(n=t.map(e=>e[1]),Array.prototype.concat.apply([],n))];var n}const y=new WeakMap;function f(e){for(const[t,n]of c)if(n.canHandle(e)){const[o,r]=n.serialize(e);return[{type:"HANDLER",name:t,value:o},r]}return[{type:"RAW",value:e},y.get(e)||[]]}function _(e){switch(e.type){case"HANDLER":return c.get(e.name).deserialize(e.value);case"RAW":return e.value}}function k(e,t,n,o){return new Promise(r=>{const a=new Array(4).fill(0).map(()=>Math.floor(Math.random()*Number.MAX_SAFE_INTEGER).toString(16)).join("-");t.set(a,r),e.start&&e.start(),e.postMessage(Object.assign({id:a},n),o)})}}};
//# sourceMappingURL=44619.3ab1fe6a37f5feab.js.map