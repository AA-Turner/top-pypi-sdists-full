export const __webpack_ids__=["9641"];export const __webpack_modules__={61145:function(e,t,i){var o={"./ha-icon-prev":["16274","1624"],"./ha-alert":["22543"],"./ha-icon-button-toggle":["80712","2558"],"./ha-svg-icon.ts":["40830"],"./ha-alert.ts":["22543"],"./ha-icon":["3847"],"./ha-icon-next.ts":["65266"],"./ha-qr-code.ts":["23493","6892","8278"],"./ha-icon-overflow-menu.ts":["83379","4458","2092","760"],"./ha-icon-button-toggle.ts":["80712","2558"],"./ha-icon-button-group":["55575","2715"],"./ha-svg-icon":["40830"],"./ha-icon-button-prev":["74683","1809"],"./ha-icon-button.ts":["78645"],"./ha-icon-overflow-menu":["83379","4458","2092","760"],"./ha-icon-button-arrow-next":["44339","2267"],"./ha-icon-button-prev.ts":["74683","1809"],"./ha-icon-picker":["49590","8018"],"./ha-icon-picker.ts":["49590","8018"],"./ha-icon-button-arrow-prev.ts":["64218"],"./ha-icon-button-next":["24696","3315"],"./ha-icon-next":["65266"],"./ha-icon-prev.ts":["16274","1624"],"./ha-icon-button-arrow-prev":["64218"],"./ha-icon-button-next.ts":["24696","3315"],"./ha-icon.ts":["3847"],"./ha-qr-code":["23493","6892","8278"],"./ha-icon-button":["78645"],"./ha-icon-button-group.ts":["55575","2715"],"./ha-icon-button-arrow-next.ts":["44339","2267"]};function s(e){if(!i.o(o,e))return Promise.resolve().then((function(){var t=new Error("Cannot find module '"+e+"'");throw t.code="MODULE_NOT_FOUND",t}));var t=o[e],s=t[0];return Promise.all(t.slice(1).map(i.e)).then((function(){return i(s)}))}s.keys=()=>Object.keys(o),s.id=61145,e.exports=s},2292:function(e,t,i){var o={"./flow-preview-generic.ts":["78375","9392","1066","8167","9338","6103"],"./flow-preview-template":["69220","9392","1066","8167","9338","6146"],"./flow-preview-generic_camera":["70269","9392","1066","8167","9338","6728"],"./flow-preview-generic_camera.ts":["70269","9392","1066","8167","9338","6728"],"./flow-preview-generic":["78375","9392","1066","8167","9338","6103"],"./flow-preview-template.ts":["69220","9392","1066","8167","9338","6146"]};function s(e){if(!i.o(o,e))return Promise.resolve().then((function(){var t=new Error("Cannot find module '"+e+"'");throw t.code="MODULE_NOT_FOUND",t}));var t=o[e],s=t[0];return Promise.all(t.slice(1).map(i.e)).then((function(){return i(s)}))}s.keys=()=>Object.keys(o),s.id=2292,e.exports=s},66766:function(e,t,i){i.d(t,{J:()=>o});const o=(e,t=!0)=>{if(e.defaultPrevented||0!==e.button||e.metaKey||e.ctrlKey||e.shiftKey)return;const i=e.composedPath().find((e=>"A"===e.tagName));if(!i||i.target||i.hasAttribute("download")||"external"===i.getAttribute("rel"))return;let o=i.href;if(!o||-1!==o.indexOf("mailto:"))return;const s=window.location,a=s.origin||s.protocol+"//"+s.host;return 0===o.indexOf(a)&&(o=o.substr(a.length),"#"!==o)?(t&&e.preventDefault(),o):void 0}},85163:function(e,t,i){i.d(t,{wZ:()=>r,jL:()=>a});var o=i(28105),s=i(31298);const a=e=>(e.name_by_user||e.name)?.trim(),r=(e,t,i)=>a(e)||i&&n(t,i)||t.localize("ui.panel.config.devices.unnamed_device",{type:t.localize(`ui.panel.config.devices.type.${e.entry_type||"device"}`)}),n=(e,t)=>{for(const i of t||[]){const t="string"==typeof i?i:i.entity_id,o=e.states[t];if(o)return(0,s.C)(o)}};(0,o.Z)((e=>function(e){const t=new Set,i=new Set;for(const o of e)i.has(o)?t.add(o):i.add(o);return t}(Object.values(e).map((e=>a(e))).filter((e=>void 0!==e)))))},35505:function(e,t,i){i.d(t,{K:()=>o});const o=e=>{switch(e.language){case"cs":case"de":case"fi":case"fr":case"sk":case"sv":return" ";default:return""}}},76528:function(e,t,i){var o=i(73742),s=i(59048),a=i(7616);class r extends s.oi{render(){return s.dy`
      <header class="header">
        <div class="header-bar">
          <section class="header-navigation-icon">
            <slot name="navigationIcon"></slot>
          </section>
          <section class="header-content">
            <div class="header-title">
              <slot name="title"></slot>
            </div>
            <div class="header-subtitle">
              <slot name="subtitle"></slot>
            </div>
          </section>
          <section class="header-action-items">
            <slot name="actionItems"></slot>
          </section>
        </div>
        <slot></slot>
      </header>
    `}static get styles(){return[s.iv`
        :host {
          display: block;
        }
        :host([show-border]) {
          border-bottom: 1px solid
            var(--mdc-dialog-scroll-divider-color, rgba(0, 0, 0, 0.12));
        }
        .header-bar {
          display: flex;
          flex-direction: row;
          align-items: flex-start;
          padding: 4px;
          box-sizing: border-box;
        }
        .header-content {
          flex: 1;
          padding: 10px 4px;
          min-width: 0;
          overflow: hidden;
          text-overflow: ellipsis;
          white-space: nowrap;
        }
        .header-title {
          font-size: var(--ha-font-size-xl);
          line-height: var(--ha-line-height-condensed);
          font-weight: var(--ha-font-weight-normal);
        }
        .header-subtitle {
          font-size: var(--ha-font-size-m);
          line-height: 20px;
          color: var(--secondary-text-color);
        }
        @media all and (min-width: 450px) and (min-height: 500px) {
          .header-bar {
            padding: 16px;
          }
        }
        .header-navigation-icon {
          flex: none;
          min-width: 8px;
          height: 100%;
          display: flex;
          flex-direction: row;
        }
        .header-action-items {
          flex: none;
          min-width: 8px;
          height: 100%;
          display: flex;
          flex-direction: row;
        }
      `]}}r=(0,o.__decorate)([(0,a.Mo)("ha-dialog-header")],r)},42523:function(e,t,i){i.d(t,{x:()=>o});const o=e=>{const t={};return e.forEach((e=>{if(void 0!==e.description?.suggested_value&&null!==e.description?.suggested_value)t[e.name]=e.description.suggested_value;else if("default"in e)t[e.name]=e.default;else if("expandable"===e.type){const i=o(e.schema);(e.required||Object.keys(i).length)&&(t[e.name]=i)}else if(e.required){if("boolean"===e.type)t[e.name]=!1;else if("string"===e.type)t[e.name]="";else if("integer"===e.type)t[e.name]="valueMin"in e?e.valueMin:0;else if("constant"===e.type)t[e.name]=e.value;else if("float"===e.type)t[e.name]=0;else if("select"===e.type){if(e.options.length){const i=e.options[0];t[e.name]=Array.isArray(i)?i[0]:i}}else if("positive_time_period_dict"===e.type)t[e.name]={hours:0,minutes:0,seconds:0};else if("selector"in e){const i=e.selector;if("device"in i)t[e.name]=i.device?.multiple?[]:"";else if("entity"in i)t[e.name]=i.entity?.multiple?[]:"";else if("area"in i)t[e.name]=i.area?.multiple?[]:"";else if("label"in i)t[e.name]=i.label?.multiple?[]:"";else if("boolean"in i)t[e.name]=!1;else if("addon"in i||"attribute"in i||"file"in i||"icon"in i||"template"in i||"text"in i||"theme"in i||"object"in i)t[e.name]="";else if("number"in i)t[e.name]=i.number?.min??0;else if("select"in i){if(i.select?.options.length){const o=i.select.options[0],s="string"==typeof o?o:o.value;t[e.name]=i.select.multiple?[s]:s}}else if("country"in i)i.country?.countries?.length&&(t[e.name]=i.country.countries[0]);else if("language"in i)i.language?.languages?.length&&(t[e.name]=i.language.languages[0]);else if("duration"in i)t[e.name]={hours:0,minutes:0,seconds:0};else if("time"in i)t[e.name]="00:00:00";else if("date"in i||"datetime"in i){const i=(new Date).toISOString().slice(0,10);t[e.name]=`${i}T00:00:00`}else if("color_rgb"in i)t[e.name]=[0,0,0];else if("color_temp"in i)t[e.name]=i.color_temp?.min_mireds??153;else if("action"in i||"trigger"in i||"condition"in i)t[e.name]=[];else{if(!("media"in i)&&!("target"in i))throw new Error(`Selector ${Object.keys(i)[0]} not supported in initial form data`);t[e.name]={}}}}else;})),t}},91337:function(e,t,i){var o=i(73742),s=i(59048),a=i(7616),r=i(69342),n=i(29740);i(22543),i(32986);const l={boolean:()=>i.e("4852").then(i.bind(i,60751)),constant:()=>i.e("177").then(i.bind(i,85184)),float:()=>i.e("2369").then(i.bind(i,94980)),grid:()=>i.e("9219").then(i.bind(i,79998)),expandable:()=>i.e("4020").then(i.bind(i,71781)),integer:()=>i.e("3703").then(i.bind(i,12960)),multi_select:()=>Promise.all([i.e("4458"),i.e("514")]).then(i.bind(i,79298)),positive_time_period_dict:()=>i.e("2010").then(i.bind(i,49058)),select:()=>i.e("3162").then(i.bind(i,64324)),string:()=>i.e("2529").then(i.bind(i,72609)),optional_actions:()=>i.e("1601").then(i.bind(i,67552))},d=(e,t)=>e?!t.name||t.flatten?e:e[t.name]:null;class c extends s.oi{getFormProperties(){return{}}async focus(){await this.updateComplete;const e=this.renderRoot.querySelector(".root");if(e)for(const t of e.children)if("HA-ALERT"!==t.tagName){t instanceof s.fl&&await t.updateComplete,t.focus();break}}willUpdate(e){e.has("schema")&&this.schema&&this.schema.forEach((e=>{"selector"in e||l[e.type]?.()}))}render(){return s.dy`
      <div class="root" part="root">
        ${this.error&&this.error.base?s.dy`
              <ha-alert alert-type="error">
                ${this._computeError(this.error.base,this.schema)}
              </ha-alert>
            `:""}
        ${this.schema.map((e=>{const t=((e,t)=>e&&t.name?e[t.name]:null)(this.error,e),i=((e,t)=>e&&t.name?e[t.name]:null)(this.warning,e);return s.dy`
            ${t?s.dy`
                  <ha-alert own-margin alert-type="error">
                    ${this._computeError(t,e)}
                  </ha-alert>
                `:i?s.dy`
                    <ha-alert own-margin alert-type="warning">
                      ${this._computeWarning(i,e)}
                    </ha-alert>
                  `:""}
            ${"selector"in e?s.dy`<ha-selector
                  .schema=${e}
                  .hass=${this.hass}
                  .narrow=${this.narrow}
                  .name=${e.name}
                  .selector=${e.selector}
                  .value=${d(this.data,e)}
                  .label=${this._computeLabel(e,this.data)}
                  .disabled=${e.disabled||this.disabled||!1}
                  .placeholder=${e.required?"":e.default}
                  .helper=${this._computeHelper(e)}
                  .localizeValue=${this.localizeValue}
                  .required=${e.required||!1}
                  .context=${this._generateContext(e)}
                ></ha-selector>`:(0,r.h)(this.fieldElementName(e.type),{schema:e,data:d(this.data,e),label:this._computeLabel(e,this.data),helper:this._computeHelper(e),disabled:this.disabled||e.disabled||!1,hass:this.hass,localize:this.hass?.localize,computeLabel:this.computeLabel,computeHelper:this.computeHelper,localizeValue:this.localizeValue,context:this._generateContext(e),...this.getFormProperties()})}
          `}))}
      </div>
    `}fieldElementName(e){return`ha-form-${e}`}_generateContext(e){if(!e.context)return;const t={};for(const[i,o]of Object.entries(e.context))t[i]=this.data[o];return t}createRenderRoot(){const e=super.createRenderRoot();return this.addValueChangedListener(e),e}addValueChangedListener(e){e.addEventListener("value-changed",(e=>{e.stopPropagation();const t=e.target.schema;if(e.target===this)return;const i=!t.name||"flatten"in t&&t.flatten?e.detail.value:{[t.name]:e.detail.value};this.data={...this.data,...i},(0,n.B)(this,"value-changed",{value:this.data})}))}_computeLabel(e,t){return this.computeLabel?this.computeLabel(e,t):e?e.name:""}_computeHelper(e){return this.computeHelper?this.computeHelper(e):""}_computeError(e,t){return Array.isArray(e)?s.dy`<ul>
        ${e.map((e=>s.dy`<li>
              ${this.computeError?this.computeError(e,t):e}
            </li>`))}
      </ul>`:this.computeError?this.computeError(e,t):e}_computeWarning(e,t){return this.computeWarning?this.computeWarning(e,t):e}constructor(...e){super(...e),this.narrow=!1,this.disabled=!1}}c.styles=s.iv`
    .root > * {
      display: block;
    }
    .root > *:not([own-margin]):not(:last-child) {
      margin-bottom: 24px;
    }
    ha-alert[own-margin] {
      margin-bottom: 4px;
    }
  `,(0,o.__decorate)([(0,a.Cb)({attribute:!1})],c.prototype,"hass",void 0),(0,o.__decorate)([(0,a.Cb)({type:Boolean})],c.prototype,"narrow",void 0),(0,o.__decorate)([(0,a.Cb)({attribute:!1})],c.prototype,"data",void 0),(0,o.__decorate)([(0,a.Cb)({attribute:!1})],c.prototype,"schema",void 0),(0,o.__decorate)([(0,a.Cb)({attribute:!1})],c.prototype,"error",void 0),(0,o.__decorate)([(0,a.Cb)({attribute:!1})],c.prototype,"warning",void 0),(0,o.__decorate)([(0,a.Cb)({type:Boolean})],c.prototype,"disabled",void 0),(0,o.__decorate)([(0,a.Cb)({attribute:!1})],c.prototype,"computeError",void 0),(0,o.__decorate)([(0,a.Cb)({attribute:!1})],c.prototype,"computeWarning",void 0),(0,o.__decorate)([(0,a.Cb)({attribute:!1})],c.prototype,"computeLabel",void 0),(0,o.__decorate)([(0,a.Cb)({attribute:!1})],c.prototype,"computeHelper",void 0),(0,o.__decorate)([(0,a.Cb)({attribute:!1})],c.prototype,"localizeValue",void 0),c=(0,o.__decorate)([(0,a.Mo)("ha-form")],c)},24083:function(e,t,i){var o=i(73742),s=i(59048),a=i(7616),r=i(82040),n=i.n(r),l=i(29740),d=i(86190);let c;const h=new class{get(e){return this._cache.get(e)}set(e,t){this._cache.set(e,t),this._expiration&&window.setTimeout((()=>this._cache.delete(e)),this._expiration)}has(e){return this._cache.has(e)}constructor(e){this._cache=new Map,this._expiration=e}}(1e3),p={reType:/(?<input>(\[!(?<type>caution|important|note|tip|warning)\])(?:\s|\\n)?)/i,typeToHaAlert:{caution:"error",important:"info",note:"info",tip:"success",warning:"warning"}};class _ extends s.fl{disconnectedCallback(){if(super.disconnectedCallback(),this.cache){const e=this._computeCacheKey();h.set(e,this.innerHTML)}}createRenderRoot(){return this}update(e){super.update(e),void 0!==this.content&&this._render()}willUpdate(e){if(!this.innerHTML&&this.cache){const e=this._computeCacheKey();h.has(e)&&(this.innerHTML=h.get(e),this._resize())}}_computeCacheKey(){return n()({content:this.content,allowSvg:this.allowSvg,allowDataUrl:this.allowDataUrl,breaks:this.breaks})}async _render(){this.innerHTML=await(async(e,t,o)=>(c||(c=(0,d.Ud)(new Worker(new URL(i.p+i.u("5845"),i.b)))),c.renderMarkdown(e,t,o)))(String(this.content),{breaks:this.breaks,gfm:!0},{allowSvg:this.allowSvg,allowDataUrl:this.allowDataUrl}),this._resize();const e=document.createTreeWalker(this,NodeFilter.SHOW_ELEMENT,null);for(;e.nextNode();){const t=e.currentNode;if(t instanceof HTMLAnchorElement&&t.host!==document.location.host)t.target="_blank",t.rel="noreferrer noopener";else if(t instanceof HTMLImageElement)this.lazyImages&&(t.loading="lazy"),t.addEventListener("load",this._resize);else if(t instanceof HTMLQuoteElement){const i=t.firstElementChild?.firstChild?.textContent&&p.reType.exec(t.firstElementChild.firstChild.textContent);if(i){const{type:o}=i.groups,s=document.createElement("ha-alert");s.alertType=p.typeToHaAlert[o.toLowerCase()],s.append(...Array.from(t.childNodes).map((e=>{const t=Array.from(e.childNodes);if(!this.breaks&&t.length){const e=t[0];e.nodeType===Node.TEXT_NODE&&e.textContent===i.input&&e.textContent?.includes("\n")&&(e.textContent=e.textContent.split("\n").slice(1).join("\n"))}return t})).reduce(((e,t)=>e.concat(t)),[]).filter((e=>e.textContent&&e.textContent!==i.input))),e.parentNode().replaceChild(s,t)}}else t instanceof HTMLElement&&["ha-alert","ha-qr-code","ha-icon","ha-svg-icon"].includes(t.localName)&&i(61145)(`./${t.localName}`)}}constructor(...e){super(...e),this.allowSvg=!1,this.allowDataUrl=!1,this.breaks=!1,this.lazyImages=!1,this.cache=!1,this._resize=()=>(0,l.B)(this,"content-resize")}}(0,o.__decorate)([(0,a.Cb)()],_.prototype,"content",void 0),(0,o.__decorate)([(0,a.Cb)({attribute:"allow-svg",type:Boolean})],_.prototype,"allowSvg",void 0),(0,o.__decorate)([(0,a.Cb)({attribute:"allow-data-url",type:Boolean})],_.prototype,"allowDataUrl",void 0),(0,o.__decorate)([(0,a.Cb)({type:Boolean})],_.prototype,"breaks",void 0),(0,o.__decorate)([(0,a.Cb)({type:Boolean,attribute:"lazy-images"})],_.prototype,"lazyImages",void 0),(0,o.__decorate)([(0,a.Cb)({type:Boolean})],_.prototype,"cache",void 0),_=(0,o.__decorate)([(0,a.Mo)("ha-markdown-element")],_);class u extends s.oi{render(){return this.content?s.dy`<ha-markdown-element
      .content=${this.content}
      .allowSvg=${this.allowSvg}
      .allowDataUrl=${this.allowDataUrl}
      .breaks=${this.breaks}
      .lazyImages=${this.lazyImages}
      .cache=${this.cache}
    ></ha-markdown-element>`:s.Ld}constructor(...e){super(...e),this.allowSvg=!1,this.allowDataUrl=!1,this.breaks=!1,this.lazyImages=!1,this.cache=!1}}u.styles=s.iv`
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
      margin: 4px 0;
    }
    a {
      color: var(--primary-color);
    }
    img {
      max-width: 100%;
    }
    code,
    pre {
      background-color: var(--markdown-code-background-color, none);
      border-radius: 3px;
    }
    svg {
      background-color: var(--markdown-svg-background-color, none);
      color: var(--markdown-svg-color, none);
    }
    code {
      font-size: var(--ha-font-size-s);
      padding: 0.2em 0.4em;
    }
    pre code {
      padding: 0;
    }
    pre {
      padding: 16px;
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
      margin: 16px 0;
    }
  `,(0,o.__decorate)([(0,a.Cb)()],u.prototype,"content",void 0),(0,o.__decorate)([(0,a.Cb)({attribute:"allow-svg",type:Boolean})],u.prototype,"allowSvg",void 0),(0,o.__decorate)([(0,a.Cb)({attribute:"allow-data-url",type:Boolean})],u.prototype,"allowDataUrl",void 0),(0,o.__decorate)([(0,a.Cb)({type:Boolean})],u.prototype,"breaks",void 0),(0,o.__decorate)([(0,a.Cb)({type:Boolean,attribute:"lazy-images"})],u.prototype,"lazyImages",void 0),(0,o.__decorate)([(0,a.Cb)({type:Boolean})],u.prototype,"cache",void 0),u=(0,o.__decorate)([(0,a.Mo)("ha-markdown")],u)},21349:function(e,t,i){i.a(e,(async function(e,t){try{var o=i(73742),s=i(30033),a=i(12191),r=i(59048),n=i(7616),l=e([s]);s=(l.then?(await l)():l)[0];class d extends s.Z{updated(e){if(super.updated(e),e.has("size"))switch(this.size){case"tiny":this.style.setProperty("--ha-progress-ring-size","16px");break;case"small":this.style.setProperty("--ha-progress-ring-size","28px");break;case"medium":this.style.setProperty("--ha-progress-ring-size","48px");break;case"large":this.style.setProperty("--ha-progress-ring-size","68px");break;case void 0:this.style.removeProperty("--ha-progress-ring-size")}}}d.styles=[a.Z,r.iv`
      :host {
        --indicator-color: var(
          --ha-progress-ring-indicator-color,
          var(--primary-color)
        );
        --track-color: var(
          --ha-progress-ring-divider-color,
          var(--divider-color)
        );
        --track-width: 4px;
        --speed: 3.5s;
        --size: var(--ha-progress-ring-size, 48px);
      }
    `],(0,o.__decorate)([(0,n.Cb)()],d.prototype,"size",void 0),d=(0,o.__decorate)([(0,n.Mo)("ha-progress-ring")],d),t()}catch(d){t(d)}}))},89275:function(e,t,i){i.d(t,{Bg:()=>c,DT:()=>d,SY:()=>n,aJ:()=>a,cz:()=>r,ko:()=>l});var o=i(75012),s=i(64930);const a=(e,t,i)=>e.connection.subscribeMessage(i,{type:"assist_satellite/intercept_wake_word",entity_id:t}),r=(e,t)=>e.callWS({type:"assist_satellite/test_connection",entity_id:t}),n=(e,t,i)=>e.callService("assist_satellite","announce",i,{entity_id:t}),l=(e,t)=>e.callWS({type:"assist_satellite/get_configuration",entity_id:t}),d=(e,t,i)=>e.callWS({type:"assist_satellite/set_wake_words",entity_id:t,wake_word_ids:i}),c=e=>e&&e.state!==s.nZ&&(0,o.e)(e,1)},39929:function(e,t,i){i.d(t,{iI:()=>s,oT:()=>o});const o=e=>e.map((e=>{if("string"!==e.type)return e;switch(e.name){case"username":return{...e,autocomplete:"username",autofocus:!0};case"password":return{...e,autocomplete:"current-password"};case"code":return{...e,autocomplete:"one-time-code",autofocus:!0};default:return e}})),s=(e,t)=>e.callWS({type:"auth/sign_path",path:t})},39286:function(e,t,i){i.d(t,{D4:()=>a,D7:()=>d,Ky:()=>s,XO:()=>r,d4:()=>l,oi:()=>n});const o={"HA-Frontend-Base":`${location.protocol}//${location.host}`},s=(e,t,i)=>e.callApi("POST","config/config_entries/flow",{handler:t,show_advanced_options:Boolean(e.userData?.showAdvanced),entry_id:i},o),a=(e,t)=>e.callApi("GET",`config/config_entries/flow/${t}`,void 0,o),r=(e,t,i)=>e.callApi("POST",`config/config_entries/flow/${t}`,i,o),n=(e,t)=>e.callApi("DELETE",`config/config_entries/flow/${t}`),l=(e,t)=>e.callApi("GET","config/config_entries/flow_handlers"+(t?`?type=${t}`:"")),d=e=>e.sendMessagePromise({type:"config_entries/flow/progress"})},46660:function(e,t,i){i.d(t,{S:()=>s,X:()=>o});const o=(e,t)=>e.subscribeEvents(t,"data_entry_flow_progressed"),s=(e,t)=>e.subscribeEvents(t,"data_entry_flow_progress_update")},64930:function(e,t,i){i.d(t,{ON:()=>r,PX:()=>n,V_:()=>l,lz:()=>a,nZ:()=>s,rk:()=>c});var o=i(13228);const s="unavailable",a="unknown",r="on",n="off",l=[s,a],d=[s,a,n],c=(0,o.z)(l);(0,o.z)(d)},28203:function(e,t,i){i.d(t,{CL:()=>f,Iq:()=>d,L3:()=>l,LM:()=>_,Mw:()=>g,Nv:()=>c,vA:()=>n,w1:()=>u});var o=i(88865),s=i(28105),a=i(31298),r=(i(92949),i(16811));const n=(e,t)=>{if(t.name)return t.name;const i=e.states[t.entity_id];return i?(0,a.C)(i):t.original_name?t.original_name:t.entity_id},l=(e,t)=>e.callWS({type:"config/entity_registry/get",entity_id:t}),d=(e,t)=>e.callWS({type:"config/entity_registry/get_entries",entity_ids:t}),c=(e,t,i)=>e.callWS({type:"config/entity_registry/update",entity_id:t,...i}),h=e=>e.sendMessagePromise({type:"config/entity_registry/list"}),p=(e,t)=>e.subscribeEvents((0,r.D)((()=>h(e).then((e=>t.setState(e,!0)))),500,!0),"entity_registry_updated"),_=(e,t)=>(0,o.B)("_entityRegistry",h,p,e,t),u=(0,s.Z)((e=>{const t={};for(const i of e)t[i.entity_id]=i;return t})),g=(0,s.Z)((e=>{const t={};for(const i of e)t[i.id]=i;return t})),f=(e,t)=>e.callWS({type:"config/entity_registry/get_automatic_entity_ids",entity_ids:t})},47893:function(e,t,i){i.d(t,{H:()=>s,O:()=>a});const o=["generic_camera","template"],s=(e,t,i,o,s,a)=>e.connection.subscribeMessage(a,{type:`${t}/start_preview`,flow_id:i,flow_type:o,user_input:s}),a=e=>o.includes(e)?e:"generic"},14723:function(e,t,i){i.a(e,(async function(e,o){try{i.r(t);var s=i(73742),a=i(59048),r=i(7616),n=i(28105),l=i(29740),d=(i(99298),i(76528),i(78645),i(46660)),c=i(77204),h=i(47584),p=i(81665),_=i(86336),u=i(47060),g=i(34386),f=i(32362),m=i(26298),v=(i(56931),i(513)),y=e([_,u,g,f,m,v]);[_,u,g,f,m,v]=y.then?(await y)():y;const w="M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z",b="M15.07,11.25L14.17,12.17C13.45,12.89 13,13.5 13,15H11V14.5C11,13.39 11.45,12.39 12.17,11.67L13.41,10.41C13.78,10.05 14,9.55 14,9C14,7.89 13.1,7 12,7A2,2 0 0,0 10,9H8A4,4 0 0,1 12,5A4,4 0 0,1 16,9C16,9.88 15.64,10.67 15.07,11.25M13,19H11V17H13M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12C22,6.47 17.5,2 12,2Z";let $=0;class x extends a.oi{async showDialog(e){this._params=e,this._instance=$++;const t=this._instance;let i;if(e.startFlowHandler){this._loading="loading_flow",this._handler=e.startFlowHandler;try{i=await this._params.flowConfig.createFlow(this.hass,e.startFlowHandler)}catch(o){this.closeDialog();let e=o.message||o.body||"Unknown error";return"string"!=typeof e&&(e=JSON.stringify(e)),void(0,p.Ys)(this,{title:this.hass.localize("ui.panel.config.integrations.config_flow.error"),text:`${this.hass.localize("ui.panel.config.integrations.config_flow.could_not_load")}: ${e}`})}if(t!==this._instance)return}else{if(!e.continueFlowId)return;this._loading="loading_flow";try{i=await e.flowConfig.fetchFlow(this.hass,e.continueFlowId)}catch(o){this.closeDialog();let e=o.message||o.body||"Unknown error";return"string"!=typeof e&&(e=JSON.stringify(e)),void(0,p.Ys)(this,{title:this.hass.localize("ui.panel.config.integrations.config_flow.error"),text:`${this.hass.localize("ui.panel.config.integrations.config_flow.could_not_load")}: ${e}`})}}t===this._instance&&(this._processStep(i),this._loading=void 0)}closeDialog(){if(!this._params)return;const e=Boolean(this._step&&["create_entry","abort"].includes(this._step.type));!this._step||e||this._params.continueFlowId||this._params.flowConfig.deleteFlow(this.hass,this._step.flow_id),this._step&&this._params.dialogClosedCallback&&this._params.dialogClosedCallback({flowFinished:e,entryId:"result"in this._step?this._step.result?.entry_id:void 0}),this._loading=void 0,this._step=void 0,this._params=void 0,this._handler=void 0,this._unsubDataEntryFlowProgress&&(this._unsubDataEntryFlowProgress(),this._unsubDataEntryFlowProgress=void 0),(0,l.B)(this,"dialog-closed",{dialog:this.localName})}_getDialogTitle(){if(this._loading||!this._step||!this._params)return"";switch(this._step.type){case"form":return this._params.flowConfig.renderShowFormStepHeader(this.hass,this._step);case"abort":return this._params.flowConfig.renderAbortHeader?this._params.flowConfig.renderAbortHeader(this.hass,this._step):this.hass.localize(`component.${this._params.domain??this._step.handler}.title`);case"progress":return this._params.flowConfig.renderShowFormProgressHeader(this.hass,this._step);case"menu":return this._params.flowConfig.renderMenuHeader(this.hass,this._step);case"create_entry":{const e=this._devices(this._params.flowConfig.showDevices,Object.values(this.hass.devices),this._step.result?.entry_id).length;return this.hass.localize("ui.panel.config.integrations.config_flow."+(e?"device_created":"success"),{number:e})}default:return""}}_getDialogSubtitle(){if(this._loading||!this._step||!this._params)return"";switch(this._step.type){case"form":return this._params.flowConfig.renderShowFormStepSubheader?.(this.hass,this._step);case"abort":return this._params.flowConfig.renderAbortSubheader?.(this.hass,this._step);case"progress":return this._params.flowConfig.renderShowFormProgressSubheader?.(this.hass,this._step);case"menu":return this._params.flowConfig.renderMenuSubheader?.(this.hass,this._step);default:return""}}render(){if(!this._params)return a.Ld;const e=["form","menu","external","progress","data_entry_flow_progressed"].includes(this._step?.type)&&this._params.manifest?.is_built_in||!!this._params.manifest?.documentation,t=this._getDialogTitle(),i=this._getDialogSubtitle();return a.dy`
      <ha-dialog
        open
        @closed=${this.closeDialog}
        scrimClickAction
        escapeKeyAction
        hideActions
        .heading=${t||!0}
      >
        <ha-dialog-header slot="heading">
          <ha-icon-button
            .label=${this.hass.localize("ui.common.close")}
            .path=${w}
            dialogAction="close"
            slot="navigationIcon"
          ></ha-icon-button>

          <div
            slot="title"
            class="dialog-title${"form"===this._step?.type?" form":""}"
            title=${t}
          >
            ${t}
          </div>

          ${i?a.dy` <div slot="subtitle">${i}</div>`:a.Ld}
          ${e&&!this._loading&&this._step?a.dy`
                <a
                  slot="actionItems"
                  class="help"
                  href=${this._params.manifest.is_built_in?(0,h.R)(this.hass,`/integrations/${this._params.manifest.domain}`):this._params.manifest.documentation}
                  target="_blank"
                  rel="noreferrer noopener"
                >
                  <ha-icon-button
                    .label=${this.hass.localize("ui.common.help")}
                    .path=${b}
                  >
                  </ha-icon-button
                ></a>
              `:a.Ld}
        </ha-dialog-header>
        <div>
          ${this._loading||null===this._step?a.dy`
                <step-flow-loading
                  .flowConfig=${this._params.flowConfig}
                  .hass=${this.hass}
                  .loadingReason=${this._loading}
                  .handler=${this._handler}
                  .step=${this._step}
                ></step-flow-loading>
              `:void 0===this._step?a.Ld:a.dy`
                  ${"form"===this._step.type?a.dy`
                        <step-flow-form
                          narrow
                          .flowConfig=${this._params.flowConfig}
                          .step=${this._step}
                          .hass=${this.hass}
                        ></step-flow-form>
                      `:"external"===this._step.type?a.dy`
                          <step-flow-external
                            .flowConfig=${this._params.flowConfig}
                            .step=${this._step}
                            .hass=${this.hass}
                          ></step-flow-external>
                        `:"abort"===this._step.type?a.dy`
                            <step-flow-abort
                              .params=${this._params}
                              .step=${this._step}
                              .hass=${this.hass}
                              .handler=${this._step.handler}
                              .domain=${this._params.domain??this._step.handler}
                            ></step-flow-abort>
                          `:"progress"===this._step.type?a.dy`
                              <step-flow-progress
                                .flowConfig=${this._params.flowConfig}
                                .step=${this._step}
                                .hass=${this.hass}
                                .progress=${this._progress}
                              ></step-flow-progress>
                            `:"menu"===this._step.type?a.dy`
                                <step-flow-menu
                                  .flowConfig=${this._params.flowConfig}
                                  .step=${this._step}
                                  .hass=${this.hass}
                                ></step-flow-menu>
                              `:a.dy`
                                <step-flow-create-entry
                                  .flowConfig=${this._params.flowConfig}
                                  .step=${this._step}
                                  .hass=${this.hass}
                                  .navigateToResult=${this._params.navigateToResult??!1}
                                  .devices=${this._devices(this._params.flowConfig.showDevices,Object.values(this.hass.devices),this._step.result?.entry_id)}
                                ></step-flow-create-entry>
                              `}
                `}
        </div>
      </ha-dialog>
    `}firstUpdated(e){super.firstUpdated(e),this.addEventListener("flow-update",(e=>{const{step:t,stepPromise:i}=e.detail;this._processStep(t||i)}))}willUpdate(e){super.willUpdate(e),e.has("_step")&&this._step&&["external","progress"].includes(this._step.type)&&this._subscribeDataEntryFlowProgressed()}async _processStep(e){if(void 0===e)return void this.closeDialog();const t=setTimeout((()=>{this._loading="loading_step"}),250);let i;try{i=await e}catch(o){return this.closeDialog(),void(0,p.Ys)(this,{title:this.hass.localize("ui.panel.config.integrations.config_flow.error"),text:o?.body?.message})}finally{clearTimeout(t),this._loading=void 0}this._step=void 0,await this.updateComplete,this._step=i}async _subscribeDataEntryFlowProgressed(){if(this._unsubDataEntryFlowProgress)return;this._progress=void 0;const e=[(0,d.X)(this.hass.connection,(e=>{e.data.flow_id===this._step?.flow_id&&(this._processStep(this._params.flowConfig.fetchFlow(this.hass,this._step.flow_id)),this._progress=void 0)})),(0,d.S)(this.hass.connection,(e=>{this._progress=Math.ceil(100*e.data.progress)}))];this._unsubDataEntryFlowProgress=async()=>{(await Promise.all(e)).map((e=>e()))}}static get styles(){return[c.yu,a.iv`
        ha-dialog {
          --dialog-content-padding: 0;
        }
        .dialog-title {
          overflow: hidden;
          text-overflow: ellipsis;
        }
        .dialog-title.form {
          white-space: normal;
        }
        .help {
          color: var(--secondary-text-color);
        }
      `]}constructor(...e){super(...e),this._instance=$,this._devices=(0,n.Z)(((e,t,i)=>e&&i?t.filter((e=>e.config_entries.includes(i))):[]))}}(0,s.__decorate)([(0,r.Cb)({attribute:!1})],x.prototype,"hass",void 0),(0,s.__decorate)([(0,r.SB)()],x.prototype,"_params",void 0),(0,s.__decorate)([(0,r.SB)()],x.prototype,"_loading",void 0),(0,s.__decorate)([(0,r.SB)()],x.prototype,"_progress",void 0),(0,s.__decorate)([(0,r.SB)()],x.prototype,"_step",void 0),(0,s.__decorate)([(0,r.SB)()],x.prototype,"_handler",void 0),x=(0,s.__decorate)([(0,r.Mo)("dialog-data-entry-flow")],x),o()}catch(w){o(w)}}))},68603:function(e,t,i){i.d(t,{t:()=>n});var o=i(59048),s=i(39286),a=i(47469),r=i(90558);const n=(e,t)=>(0,r.w)(e,t,{flowType:"config_flow",showDevices:!0,createFlow:async(e,i)=>{const[o]=await Promise.all([(0,s.Ky)(e,i,t.entryId),e.loadFragmentTranslation("config"),e.loadBackendTranslation("config",i),e.loadBackendTranslation("selector",i),e.loadBackendTranslation("title",i)]);return o},fetchFlow:async(e,t)=>{const[i]=await Promise.all([(0,s.D4)(e,t),e.loadFragmentTranslation("config")]);return await Promise.all([e.loadBackendTranslation("config",i.handler),e.loadBackendTranslation("selector",i.handler),e.loadBackendTranslation("title",i.handler)]),i},handleFlowStep:s.XO,deleteFlow:s.oi,renderAbortDescription(e,t){const i=e.localize(`component.${t.translation_domain||t.handler}.config.abort.${t.reason}`,t.description_placeholders);return i?o.dy`
            <ha-markdown allow-svg breaks .content=${i}></ha-markdown>
          `:t.reason},renderShowFormStepHeader(e,t){return e.localize(`component.${t.translation_domain||t.handler}.config.step.${t.step_id}.title`,t.description_placeholders)||e.localize(`component.${t.handler}.title`)},renderShowFormStepDescription(e,t){const i=e.localize(`component.${t.translation_domain||t.handler}.config.step.${t.step_id}.description`,t.description_placeholders);return i?o.dy`
            <ha-markdown
              .allowDataUrl=${"zwave_js"===t.handler}
              allow-svg
              breaks
              .content=${i}
            ></ha-markdown>
          `:""},renderShowFormStepFieldLabel(e,t,i,o){if("expandable"===i.type)return e.localize(`component.${t.handler}.config.step.${t.step_id}.sections.${i.name}.name`,t.description_placeholders);const s=o?.path?.[0]?`sections.${o.path[0]}.`:"";return e.localize(`component.${t.handler}.config.step.${t.step_id}.${s}data.${i.name}`,t.description_placeholders)||i.name},renderShowFormStepFieldHelper(e,t,i,s){if("expandable"===i.type)return e.localize(`component.${t.translation_domain||t.handler}.config.step.${t.step_id}.sections.${i.name}.description`,t.description_placeholders);const a=s?.path?.[0]?`sections.${s.path[0]}.`:"",r=e.localize(`component.${t.translation_domain||t.handler}.config.step.${t.step_id}.${a}data_description.${i.name}`,t.description_placeholders);return r?o.dy`<ha-markdown breaks .content=${r}></ha-markdown>`:""},renderShowFormStepFieldError(e,t,i){return e.localize(`component.${t.translation_domain||t.translation_domain||t.handler}.config.error.${i}`,t.description_placeholders)||i},renderShowFormStepFieldLocalizeValue(e,t,i){return e.localize(`component.${t.handler}.selector.${i}`)},renderShowFormStepSubmitButton(e,t){return e.localize(`component.${t.handler}.config.step.${t.step_id}.submit`)||e.localize("ui.panel.config.integrations.config_flow."+(!1===t.last_step?"next":"submit"))},renderExternalStepHeader(e,t){return e.localize(`component.${t.handler}.config.step.${t.step_id}.title`)||e.localize("ui.panel.config.integrations.config_flow.external_step.open_site")},renderExternalStepDescription(e,t){const i=e.localize(`component.${t.translation_domain||t.handler}.config.${t.step_id}.description`,t.description_placeholders);return o.dy`
        <p>
          ${e.localize("ui.panel.config.integrations.config_flow.external_step.description")}
        </p>
        ${i?o.dy`
              <ha-markdown
                allow-svg
                breaks
                .content=${i}
              ></ha-markdown>
            `:""}
      `},renderCreateEntryDescription(e,t){const i=e.localize(`component.${t.translation_domain||t.handler}.config.create_entry.${t.description||"default"}`,t.description_placeholders);return o.dy`
        ${i?o.dy`
              <ha-markdown
                allow-svg
                breaks
                .content=${i}
              ></ha-markdown>
            `:o.Ld}
      `},renderShowFormProgressHeader(e,t){return e.localize(`component.${t.handler}.config.step.${t.step_id}.title`)||e.localize(`component.${t.handler}.title`)},renderShowFormProgressDescription(e,t){const i=e.localize(`component.${t.translation_domain||t.handler}.config.progress.${t.progress_action}`,t.description_placeholders);return i?o.dy`
            <ha-markdown allow-svg breaks .content=${i}></ha-markdown>
          `:""},renderMenuHeader(e,t){return e.localize(`component.${t.handler}.config.step.${t.step_id}.title`)||e.localize(`component.${t.handler}.title`)},renderMenuDescription(e,t){const i=e.localize(`component.${t.translation_domain||t.handler}.config.step.${t.step_id}.description`,t.description_placeholders);return i?o.dy`
            <ha-markdown allow-svg breaks .content=${i}></ha-markdown>
          `:""},renderMenuOption(e,t,i){return e.localize(`component.${t.translation_domain||t.handler}.config.step.${t.step_id}.menu_options.${i}`,t.description_placeholders)},renderLoadingDescription(e,t,i,o){if("loading_flow"!==t&&"loading_step"!==t)return"";const s=o?.handler||i;return e.localize(`ui.panel.config.integrations.config_flow.loading.${t}`,{integration:s?(0,a.Lh)(e.localize,s):e.localize("ui.panel.config.integrations.config_flow.loading.fallback_title")})}})},86336:function(e,t,i){i.a(e,(async function(e,t){try{var o=i(73742),s=i(59048),a=i(7616),r=i(29740),n=i(35355),l=i(68603),d=i(3567),c=i(30337),h=e([c]);c=(h.then?(await h)():h)[0];class p extends s.oi{firstUpdated(e){super.firstUpdated(e),"missing_credentials"===this.step.reason&&this._handleMissingCreds()}render(){return"missing_credentials"===this.step.reason?s.Ld:s.dy`
      <div class="content">
        ${this.params.flowConfig.renderAbortDescription(this.hass,this.step)}
      </div>
      <div class="buttons">
        <ha-button appearance="plain" @click=${this._flowDone}
          >${this.hass.localize("ui.panel.config.integrations.config_flow.close")}</ha-button
        >
      </div>
    `}async _handleMissingCreds(){(0,n.L)(this.params.dialogParentElement,{selectedDomain:this.domain,manifest:this.params.manifest,applicationCredentialAddedCallback:()=>{(0,l.t)(this.params.dialogParentElement,{dialogClosedCallback:this.params.dialogClosedCallback,startFlowHandler:this.handler,showAdvanced:this.hass.userData?.showAdvanced,navigateToResult:this.params.navigateToResult})}}),this._flowDone()}_flowDone(){(0,r.B)(this,"flow-update",{step:void 0})}static get styles(){return d.i}}(0,o.__decorate)([(0,a.Cb)({attribute:!1})],p.prototype,"params",void 0),(0,o.__decorate)([(0,a.Cb)({attribute:!1})],p.prototype,"hass",void 0),(0,o.__decorate)([(0,a.Cb)({attribute:!1})],p.prototype,"step",void 0),(0,o.__decorate)([(0,a.Cb)({attribute:!1})],p.prototype,"domain",void 0),(0,o.__decorate)([(0,a.Cb)({attribute:!1})],p.prototype,"handler",void 0),p=(0,o.__decorate)([(0,a.Mo)("step-flow-abort")],p),t()}catch(p){t(p)}}))},47060:function(e,t,i){i.a(e,(async function(e,t){try{var o=i(73742),s=i(59048),a=i(7616),r=i(28105),n=i(29740),l=i(85163),d=i(76151),c=i(29173),h=(i(99495),i(30337)),p=i(89275),_=i(51729),u=i(28203),g=i(47469),f=i(37198),m=i(81665),v=i(21570),y=i(3567),w=e([h]);h=(w.then?(await w)():w)[0];class b extends s.oi{willUpdate(e){if(!e.has("devices")&&!e.has("hass"))return;if(1!==this.devices.length||this.devices[0].primary_config_entry!==this.step.result?.entry_id||"voip"===this.step.result.domain)return;const t=this._deviceEntities(this.devices[0].id,Object.values(this.hass.entities),"assist_satellite");t.length&&t.some((e=>(0,p.Bg)(this.hass.states[e.entity_id])))&&(this.navigateToResult=!1,this._flowDone(),(0,v.k)(this,{deviceId:this.devices[0].id}))}render(){const e=this.hass.localize;return s.dy`
      <div class="content">
        ${this.flowConfig.renderCreateEntryDescription(this.hass,this.step)}
        ${"not_loaded"===this.step.result?.state?s.dy`<span class="error"
              >${e("ui.panel.config.integrations.config_flow.not_loaded")}</span
            >`:s.Ld}
        ${0===this.devices.length&&["options_flow","repair_flow"].includes(this.flowConfig.flowType)?s.Ld:0===this.devices.length?s.dy`<p>
                ${e("ui.panel.config.integrations.config_flow.created_config",{name:this.step.title})}
              </p>`:s.dy`
                <div class="devices">
                  ${this.devices.map((t=>s.dy`
                      <div class="device">
                        <div class="device-info">
                          ${this.step.result?.domain?s.dy`<img
                                slot="graphic"
                                alt=${(0,g.Lh)(this.hass.localize,this.step.result.domain)}
                                src=${(0,f.X1)({domain:this.step.result.domain,type:"icon",darkOptimized:this.hass.themes?.darkMode})}
                                crossorigin="anonymous"
                                referrerpolicy="no-referrer"
                              />`:s.Ld}
                          <div class="device-info-details">
                            <span>${t.model||t.manufacturer}</span>
                            ${t.model?s.dy`<span class="secondary">
                                  ${t.manufacturer}
                                </span>`:s.Ld}
                          </div>
                        </div>
                        <ha-textfield
                          .label=${e("ui.panel.config.integrations.config_flow.device_name")}
                          .placeholder=${(0,l.wZ)(t,this.hass)}
                          .value=${this._deviceUpdate[t.id]?.name??(0,l.jL)(t)}
                          @change=${this._deviceNameChanged}
                          .device=${t.id}
                        ></ha-textfield>
                        <ha-area-picker
                          .hass=${this.hass}
                          .device=${t.id}
                          .value=${this._deviceUpdate[t.id]?.area??t.area_id??void 0}
                          @value-changed=${this._areaPicked}
                        ></ha-area-picker>
                      </div>
                    `))}
                </div>
              `}
      </div>
      <div class="buttons">
        <ha-button @click=${this._flowDone}
          >${e("ui.panel.config.integrations.config_flow."+(!this.devices.length||Object.keys(this._deviceUpdate).length?"finish":"finish_skip"))}</ha-button
        >
      </div>
    `}async _flowDone(){if(Object.keys(this._deviceUpdate).length){const e=[],t=Object.entries(this._deviceUpdate).map((([t,i])=>(i.name&&e.push(t),(0,_.t1)(this.hass,t,{name_by_user:i.name,area_id:i.area}).catch((e=>{(0,m.Ys)(this,{text:this.hass.localize("ui.panel.config.integrations.config_flow.error_saving_device",{error:e.message})})})))));await Promise.allSettled(t);const i=[],o=[];e.forEach((e=>{const t=this._deviceEntities(e,Object.values(this.hass.entities));o.push(...t.map((e=>e.entity_id)))}));const s=await(0,u.CL)(this.hass,o);Object.entries(s).forEach((([e,t])=>{t&&i.push((0,u.Nv)(this.hass,e,{new_entity_id:t}).catch((e=>(0,m.Ys)(this,{text:this.hass.localize("ui.panel.config.integrations.config_flow.error_saving_entity",{error:e.message})}))))})),await Promise.allSettled(i)}(0,n.B)(this,"flow-update",{step:void 0}),this.step.result&&this.navigateToResult&&(1===this.devices.length?(0,c.c)(`/config/devices/device/${this.devices[0].id}`):(0,c.c)(`/config/integrations/integration/${this.step.result.domain}#config_entry=${this.step.result.entry_id}`))}async _areaPicked(e){const t=e.currentTarget.device,i=e.detail.value;t in this._deviceUpdate||(this._deviceUpdate[t]={}),this._deviceUpdate[t].area=i,this.requestUpdate("_deviceUpdate")}_deviceNameChanged(e){const t=e.currentTarget,i=t.device,o=t.value;i in this._deviceUpdate||(this._deviceUpdate[i]={}),this._deviceUpdate[i].name=o,this.requestUpdate("_deviceUpdate")}static get styles(){return[y.i,s.iv`
        .devices {
          display: flex;
          margin: -4px;
          max-height: 600px;
          overflow-y: auto;
          flex-direction: column;
        }
        @media all and (max-width: 450px), all and (max-height: 500px) {
          .devices {
            /* header - margin content - footer */
            max-height: calc(100vh - 52px - 20px - 52px);
          }
        }
        .device {
          border: 1px solid var(--divider-color);
          padding: 6px;
          border-radius: 4px;
          margin: 4px;
          display: inline-block;
        }
        .device-info {
          display: flex;
          align-items: center;
          gap: 8px;
        }
        .device-info img {
          width: 40px;
          height: 40px;
        }
        .device-info-details {
          display: flex;
          flex-direction: column;
          justify-content: center;
        }
        .secondary {
          color: var(--secondary-text-color);
        }
        ha-textfield,
        ha-area-picker {
          display: block;
        }
        ha-textfield {
          margin: 8px 0;
        }
        .buttons > *:last-child {
          margin-left: auto;
          margin-inline-start: auto;
          margin-inline-end: initial;
        }
        .error {
          color: var(--error-color);
        }
      `]}constructor(...e){super(...e),this.navigateToResult=!1,this._deviceUpdate={},this._deviceEntities=(0,r.Z)(((e,t,i)=>t.filter((t=>t.device_id===e&&(!i||(0,d.M)(t.entity_id)===i)))))}}(0,o.__decorate)([(0,a.Cb)({attribute:!1})],b.prototype,"flowConfig",void 0),(0,o.__decorate)([(0,a.Cb)({attribute:!1})],b.prototype,"hass",void 0),(0,o.__decorate)([(0,a.Cb)({attribute:!1})],b.prototype,"step",void 0),(0,o.__decorate)([(0,a.Cb)({attribute:!1})],b.prototype,"devices",void 0),(0,o.__decorate)([(0,a.SB)()],b.prototype,"_deviceUpdate",void 0),b=(0,o.__decorate)([(0,a.Mo)("step-flow-create-entry")],b),t()}catch(b){t(b)}}))},34386:function(e,t,i){i.a(e,(async function(e,t){try{var o=i(73742),s=i(59048),a=i(7616),r=i(3567),n=i(30337),l=e([n]);n=(l.then?(await l)():l)[0];class d extends s.oi{render(){const e=this.hass.localize;return s.dy`
      <div class="content">
        ${this.flowConfig.renderExternalStepDescription(this.hass,this.step)}
        <div class="open-button">
          <ha-button href=${this.step.url} target="_blank" rel="noreferrer">
            ${e("ui.panel.config.integrations.config_flow.external_step.open_site")}
          </ha-button>
        </div>
      </div>
    `}firstUpdated(e){super.firstUpdated(e),window.open(this.step.url)}static get styles(){return[r.i,s.iv`
        .open-button {
          text-align: center;
          padding: 24px 0;
        }
        .open-button a {
          text-decoration: none;
        }
      `]}}(0,o.__decorate)([(0,a.Cb)({attribute:!1})],d.prototype,"flowConfig",void 0),(0,o.__decorate)([(0,a.Cb)({attribute:!1})],d.prototype,"hass",void 0),(0,o.__decorate)([(0,a.Cb)({attribute:!1})],d.prototype,"step",void 0),d=(0,o.__decorate)([(0,a.Mo)("step-flow-external")],d),t()}catch(d){t(d)}}))},32362:function(e,t,i){i.a(e,(async function(e,t){try{var o=i(73742),s=i(59048),a=i(7616),r=i(28105),n=i(69342),l=i(29740),d=i(66766),c=i(30337),h=(i(22543),i(42523)),p=(i(91337),i(24083),i(97862)),_=i(39929),u=i(47893),g=i(77204),f=i(3567),m=e([c,p]);[c,p]=m.then?(await m)():m;class v extends s.oi{disconnectedCallback(){super.disconnectedCallback(),this.removeEventListener("keydown",this._handleKeyDown)}render(){const e=this.step,t=this._stepDataProcessed;return s.dy`
      <div class="content" @click=${this._clickHandler}>
        ${this.flowConfig.renderShowFormStepDescription(this.hass,this.step)}
        ${this._errorMsg?s.dy`<ha-alert alert-type="error">${this._errorMsg}</ha-alert>`:""}
        <ha-form
          .hass=${this.hass}
          .narrow=${this.narrow}
          .data=${t}
          .disabled=${this._loading}
          @value-changed=${this._stepDataChanged}
          .schema=${(0,_.oT)(this.handleReadOnlyFields(e.data_schema))}
          .error=${this._errors}
          .computeLabel=${this._labelCallback}
          .computeHelper=${this._helperCallback}
          .computeError=${this._errorCallback}
          .localizeValue=${this._localizeValueCallback}
        ></ha-form>
      </div>
      ${e.preview?s.dy`<div class="preview" @set-flow-errors=${this._setError}>
            <h3>
              ${this.hass.localize("ui.panel.config.integrations.config_flow.preview")}:
            </h3>
            ${(0,n.h)(`flow-preview-${(0,u.O)(e.preview)}`,{hass:this.hass,domain:e.preview,flowType:this.flowConfig.flowType,handler:e.handler,stepId:e.step_id,flowId:e.flow_id,stepData:t})}
          </div>`:s.Ld}
      <div class="buttons">
        <ha-button @click=${this._submitStep} .loading=${this._loading}>
          ${this.flowConfig.renderShowFormStepSubmitButton(this.hass,this.step)}
        </ha-button>
      </div>
    `}_setError(e){this._previewErrors=e.detail}firstUpdated(e){super.firstUpdated(e),setTimeout((()=>this.shadowRoot.querySelector("ha-form").focus()),0),this.addEventListener("keydown",this._handleKeyDown)}willUpdate(e){super.willUpdate(e),e.has("step")&&this.step?.preview&&i(2292)(`./flow-preview-${(0,u.O)(this.step.preview)}`),(e.has("step")||e.has("_previewErrors")||e.has("_submitErrors"))&&(this._errors=this.step.errors||this._previewErrors||this._submitErrors?{...this.step.errors,...this._previewErrors,...this._submitErrors}:void 0)}_clickHandler(e){(0,d.J)(e,!1)&&(0,l.B)(this,"flow-update",{step:void 0})}get _stepDataProcessed(){return void 0!==this._stepData||(this._stepData=(0,h.x)(this.step.data_schema)),this._stepData}async _submitStep(){const e=this._stepData||{},t=(e,i)=>e.every((e=>(!e.required||!["",void 0].includes(i[e.name]))&&("expandable"!==e.type||!e.required&&void 0===i[e.name]||t(e.schema,i[e.name]))));if(!(void 0===e?void 0===this.step.data_schema.find((e=>e.required)):t(this.step.data_schema,e)))return void(this._errorMsg=this.hass.localize("ui.panel.config.integrations.config_flow.not_all_required_fields"));this._loading=!0,this._errorMsg=void 0,this._submitErrors=void 0;const i=this.step.flow_id,o={};Object.keys(e).forEach((t=>{const i=e[t],s=[void 0,""].includes(i),a=this.step.data_schema?.find((e=>e.name===t)),r=a?.selector??{},n=Object.values(r)[0]?.read_only;s||n||(o[t]=i)}));try{const e=await this.flowConfig.handleFlowStep(this.hass,this.step.flow_id,o);if(!this.step||i!==this.step.flow_id)return;this._previewErrors=void 0,(0,l.B)(this,"flow-update",{step:e})}catch(s){s&&s.body?(s.body.message&&(this._errorMsg=s.body.message),s.body.errors&&(this._submitErrors=s.body.errors),s.body.message||s.body.errors||(this._errorMsg="Unknown error occurred")):this._errorMsg="Unknown error occurred"}finally{this._loading=!1}}_stepDataChanged(e){this._stepData=e.detail.value}static get styles(){return[g.Qx,f.i,s.iv`
        .error {
          color: red;
        }

        ha-alert,
        ha-form {
          margin-top: 24px;
          display: block;
        }

        .buttons {
          padding: 16px;
        }
      `]}constructor(...e){super(...e),this.narrow=!1,this._loading=!1,this.handleReadOnlyFields=(0,r.Z)((e=>e?.map((e=>({...e,...Object.values(e?.selector??{})[0]?.read_only?{disabled:!0}:{}}))))),this._handleKeyDown=e=>{"Enter"===e.key&&this._submitStep()},this._labelCallback=(e,t,i)=>this.flowConfig.renderShowFormStepFieldLabel(this.hass,this.step,e,i),this._helperCallback=(e,t)=>this.flowConfig.renderShowFormStepFieldHelper(this.hass,this.step,e,t),this._errorCallback=e=>this.flowConfig.renderShowFormStepFieldError(this.hass,this.step,e),this._localizeValueCallback=e=>this.flowConfig.renderShowFormStepFieldLocalizeValue(this.hass,this.step,e)}}(0,o.__decorate)([(0,a.Cb)({attribute:!1})],v.prototype,"flowConfig",void 0),(0,o.__decorate)([(0,a.Cb)({type:Boolean})],v.prototype,"narrow",void 0),(0,o.__decorate)([(0,a.Cb)({attribute:!1})],v.prototype,"step",void 0),(0,o.__decorate)([(0,a.Cb)({attribute:!1})],v.prototype,"hass",void 0),(0,o.__decorate)([(0,a.SB)()],v.prototype,"_loading",void 0),(0,o.__decorate)([(0,a.SB)()],v.prototype,"_stepData",void 0),(0,o.__decorate)([(0,a.SB)()],v.prototype,"_previewErrors",void 0),(0,o.__decorate)([(0,a.SB)()],v.prototype,"_submitErrors",void 0),(0,o.__decorate)([(0,a.SB)()],v.prototype,"_errorMsg",void 0),v=(0,o.__decorate)([(0,a.Mo)("step-flow-form")],v),t()}catch(v){t(v)}}))},26298:function(e,t,i){i.a(e,(async function(e,t){try{var o=i(73742),s=i(59048),a=i(7616),r=i(97862),n=e([r]);r=(n.then?(await n)():n)[0];class l extends s.oi{render(){const e=this.flowConfig.renderLoadingDescription(this.hass,this.loadingReason,this.handler,this.step);return s.dy`
      <div class="init-spinner">
        ${e?s.dy`<div>${e}</div>`:""}
        <ha-spinner></ha-spinner>
      </div>
    `}}l.styles=s.iv`
    .init-spinner {
      padding: 50px 100px;
      text-align: center;
    }
    ha-spinner {
      margin-top: 16px;
    }
  `,(0,o.__decorate)([(0,a.Cb)({attribute:!1})],l.prototype,"flowConfig",void 0),(0,o.__decorate)([(0,a.Cb)({attribute:!1})],l.prototype,"hass",void 0),(0,o.__decorate)([(0,a.Cb)({attribute:!1})],l.prototype,"loadingReason",void 0),(0,o.__decorate)([(0,a.Cb)()],l.prototype,"handler",void 0),(0,o.__decorate)([(0,a.Cb)({attribute:!1})],l.prototype,"step",void 0),l=(0,o.__decorate)([(0,a.Mo)("step-flow-loading")],l),t()}catch(l){t(l)}}))},56931:function(e,t,i){var o=i(73742),s=i(59048),a=i(7616),r=i(29740),n=(i(65266),i(93795),i(3567));class l extends s.oi{render(){let e,t;if(Array.isArray(this.step.menu_options)){e=this.step.menu_options,t={};for(const i of e)t[i]=this.flowConfig.renderMenuOption(this.hass,this.step,i)}else e=Object.keys(this.step.menu_options),t=this.step.menu_options;const i=this.flowConfig.renderMenuDescription(this.hass,this.step);return s.dy`
      ${i?s.dy`<div class="content">${i}</div>`:""}
      <div class="options">
        ${e.map((e=>s.dy`
            <ha-list-item hasMeta .step=${e} @click=${this._handleStep}>
              <span>${t[e]}</span>
              <ha-icon-next slot="meta"></ha-icon-next>
            </ha-list-item>
          `))}
      </div>
    `}_handleStep(e){(0,r.B)(this,"flow-update",{stepPromise:this.flowConfig.handleFlowStep(this.hass,this.step.flow_id,{next_step_id:e.currentTarget.step})})}}l.styles=[n.i,s.iv`
      .options {
        margin-top: 20px;
        margin-bottom: 8px;
      }
      .content {
        padding-bottom: 16px;
        border-bottom: 1px solid var(--divider-color);
      }
      .content + .options {
        margin-top: 8px;
      }
      ha-list-item {
        --mdc-list-side-padding: 24px;
      }
    `],(0,o.__decorate)([(0,a.Cb)({attribute:!1})],l.prototype,"flowConfig",void 0),(0,o.__decorate)([(0,a.Cb)({attribute:!1})],l.prototype,"hass",void 0),(0,o.__decorate)([(0,a.Cb)({attribute:!1})],l.prototype,"step",void 0),l=(0,o.__decorate)([(0,a.Mo)("step-flow-menu")],l)},513:function(e,t,i){i.a(e,(async function(e,t){try{var o=i(73742),s=i(59048),a=i(7616),r=i(35505),n=i(21349),l=i(97862),d=i(3567),c=e([n,l]);[n,l]=c.then?(await c)():c;class h extends s.oi{render(){return s.dy`
      <div class="content">
        ${this.progress?s.dy`
              <ha-progress-ring .value=${this.progress} size="large"
                >${this.progress}${(0,r.K)(this.hass.locale)}%</ha-progress-ring
              >
            `:s.dy` <ha-spinner size="large"></ha-spinner> `}
        ${this.flowConfig.renderShowFormProgressDescription(this.hass,this.step)}
      </div>
    `}static get styles(){return[d.i,s.iv`
        .content {
          padding: 50px 100px;
          text-align: center;
        }
        ha-spinner {
          margin-bottom: 16px;
        }
      `]}}(0,o.__decorate)([(0,a.Cb)({attribute:!1})],h.prototype,"flowConfig",void 0),(0,o.__decorate)([(0,a.Cb)({attribute:!1})],h.prototype,"hass",void 0),(0,o.__decorate)([(0,a.Cb)({attribute:!1})],h.prototype,"step",void 0),(0,o.__decorate)([(0,a.Cb)({type:Number})],h.prototype,"progress",void 0),h=(0,o.__decorate)([(0,a.Mo)("step-flow-progress")],h),t()}catch(h){t(h)}}))},3567:function(e,t,i){i.d(t,{i:()=>o});const o=i(59048).iv`
  h2 {
    margin: 24px 38px 0 0;
    margin-inline-start: 0px;
    margin-inline-end: 38px;
    padding: 0 24px;
    padding-inline-start: 24px;
    padding-inline-end: 24px;
    -moz-osx-font-smoothing: var(--ha-moz-osx-font-smoothing);
    -webkit-font-smoothing: var(--ha-font-smoothing);
    font-family: var(
      --mdc-typography-headline6-font-family,
      var(--mdc-typography-font-family, var(--ha-font-family-body))
    );
    font-size: var(--mdc-typography-headline6-font-size, var(--ha-font-size-l));
    line-height: var(--mdc-typography-headline6-line-height, 2rem);
    font-weight: var(
      --mdc-typography-headline6-font-weight,
      var(--ha-font-weight-medium)
    );
    letter-spacing: var(--mdc-typography-headline6-letter-spacing, 0.0125em);
    text-decoration: var(--mdc-typography-headline6-text-decoration, inherit);
    text-transform: var(--mdc-typography-headline6-text-transform, inherit);
    box-sizing: border-box;
  }

  .content,
  .preview {
    margin-top: 20px;
    padding: 0 24px;
  }

  .buttons {
    position: relative;
    padding: 16px;
    margin: 8px 0 0;
    color: var(--primary-color);
    display: flex;
    justify-content: flex-end;
  }

  ha-markdown {
    overflow-wrap: break-word;
  }
  ha-markdown a {
    color: var(--primary-color);
  }
  ha-markdown img:first-child:last-child {
    display: block;
    margin: 0 auto;
  }
`},21570:function(e,t,i){i.d(t,{k:()=>a});var o=i(29740);const s=()=>Promise.all([i.e("4458"),i.e("9392"),i.e("8167"),i.e("9548")]).then(i.bind(i,52398)),a=(e,t)=>{(0,o.B)(e,"show-dialog",{dialogTag:"ha-voice-assistant-setup-dialog",dialogImport:s,dialogParams:t})}},35355:function(e,t,i){i.d(t,{L:()=>a});var o=i(29740);const s=()=>i.e("5881").then(i.bind(i,78818)),a=(e,t)=>{(0,o.B)(e,"show-dialog",{dialogTag:"dialog-add-application-credential",dialogImport:s,dialogParams:t})}},37198:function(e,t,i){i.d(t,{X1:()=>o,u4:()=>s,zC:()=>a});const o=e=>`https://brands.home-assistant.io/${e.brand?"brands/":""}${e.useFallback?"_/":""}${e.domain}/${e.darkOptimized?"dark_":""}${e.type}.png`,s=e=>e.split("/")[4],a=e=>e.startsWith("https://brands.home-assistant.io/")},47584:function(e,t,i){i.d(t,{R:()=>o});const o=(e,t)=>`https://${e.config.version.includes("b")?"rc":e.config.version.includes("dev")?"next":"www"}.home-assistant.io${t}`}};
//# sourceMappingURL=9641.d96cdbba6f5f5f9c.js.map