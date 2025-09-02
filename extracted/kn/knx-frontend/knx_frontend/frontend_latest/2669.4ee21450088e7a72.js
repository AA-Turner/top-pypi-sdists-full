/*! For license information please see 2669.4ee21450088e7a72.js.LICENSE.txt */
export const __webpack_ids__=["2669"];export const __webpack_modules__={13539:function(e,t,r){r.d(t,{Bt:()=>s});var a=r(3574),o=r(1066);const i=["sunday","monday","tuesday","wednesday","thursday","friday","saturday"],s=e=>e.first_weekday===o.FS.language?"weekInfo"in Intl.Locale.prototype?new Intl.Locale(e.language).weekInfo.firstDay%7:(0,a.L)(e.language)%7:i.includes(e.first_weekday)?i.indexOf(e.first_weekday):1},60495:function(e,t,r){r.a(e,(async function(e,a){try{r.d(t,{G:()=>d});var o=r(57900),i=r(28105),s=r(58713),n=e([o,s]);[o,s]=n.then?(await n)():n;const l=(0,i.Z)((e=>new Intl.RelativeTimeFormat(e.language,{numeric:"auto"}))),d=(e,t,r,a=!0)=>{const o=(0,s.W)(e,r,t);return a?l(t).format(o.value,o.unit):Intl.NumberFormat(t.language,{style:"unit",unit:o.unit,unitDisplay:"long"}).format(Math.abs(o.value))};a()}catch(l){a(l)}}))},58713:function(e,t,r){r.a(e,(async function(e,a){try{r.d(t,{W:()=>p});var o=r(7722),i=r(66233),s=r(41238),n=r(13539);const d=1e3,c=60,h=60*c;function p(e,t=Date.now(),r,a={}){const l={...u,...a||{}},p=(+e-+t)/d;if(Math.abs(p)<l.second)return{value:Math.round(p),unit:"second"};const g=p/c;if(Math.abs(g)<l.minute)return{value:Math.round(g),unit:"minute"};const b=p/h;if(Math.abs(b)<l.hour)return{value:Math.round(b),unit:"hour"};const v=new Date(e),m=new Date(t);v.setHours(0,0,0,0),m.setHours(0,0,0,0);const y=(0,o.j)(v,m);if(0===y)return{value:Math.round(b),unit:"hour"};if(Math.abs(y)<l.day)return{value:y,unit:"day"};const f=(0,n.Bt)(r),_=(0,i.z)(v,{weekStartsOn:f}),x=(0,i.z)(m,{weekStartsOn:f}),w=(0,s.p)(_,x);if(0===w)return{value:y,unit:"day"};if(Math.abs(w)<l.week)return{value:w,unit:"week"};const k=v.getFullYear()-m.getFullYear(),$=12*k+v.getMonth()-m.getMonth();return 0===$?{value:w,unit:"week"}:Math.abs($)<l.month||0===k?{value:$,unit:"month"}:{value:Math.round(k),unit:"year"}}const u={second:45,minute:45,hour:22,day:5,week:4,month:11};a()}catch(l){a(l)}}))},22543:function(e,t,r){r.r(t);var a=r(73742),o=r(59048),i=r(7616),s=r(31733),n=r(29740);r(78645),r(40830);const l={info:"M11,9H13V7H11M12,20C7.59,20 4,16.41 4,12C4,7.59 7.59,4 12,4C16.41,4 20,7.59 20,12C20,16.41 16.41,20 12,20M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M11,17H13V11H11V17Z",warning:"M12,2L1,21H23M12,6L19.53,19H4.47M11,10V14H13V10M11,16V18H13V16",error:"M11,15H13V17H11V15M11,7H13V13H11V7M12,2C6.47,2 2,6.5 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M12,20A8,8 0 0,1 4,12A8,8 0 0,1 12,4A8,8 0 0,1 20,12A8,8 0 0,1 12,20Z",success:"M20,12A8,8 0 0,1 12,20A8,8 0 0,1 4,12A8,8 0 0,1 12,4C12.76,4 13.5,4.11 14.2,4.31L15.77,2.74C14.61,2.26 13.34,2 12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12M7.91,10.08L6.5,11.5L11,16L21,6L19.59,4.58L11,13.17L7.91,10.08Z"};class d extends o.oi{render(){return o.dy`
      <div
        class="issue-type ${(0,s.$)({[this.alertType]:!0})}"
        role="alert"
      >
        <div class="icon ${this.title?"":"no-title"}">
          <slot name="icon">
            <ha-svg-icon .path=${l[this.alertType]}></ha-svg-icon>
          </slot>
        </div>
        <div class=${(0,s.$)({content:!0,narrow:this.narrow})}>
          <div class="main-content">
            ${this.title?o.dy`<div class="title">${this.title}</div>`:o.Ld}
            <slot></slot>
          </div>
          <div class="action">
            <slot name="action">
              ${this.dismissable?o.dy`<ha-icon-button
                    @click=${this._dismissClicked}
                    label="Dismiss alert"
                    .path=${"M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z"}
                  ></ha-icon-button>`:o.Ld}
            </slot>
          </div>
        </div>
      </div>
    `}_dismissClicked(){(0,n.B)(this,"alert-dismissed-clicked")}constructor(...e){super(...e),this.title="",this.alertType="info",this.dismissable=!1,this.narrow=!1}}d.styles=o.iv`
    .issue-type {
      position: relative;
      padding: 8px;
      display: flex;
    }
    .issue-type::after {
      position: absolute;
      top: 0;
      right: 0;
      bottom: 0;
      left: 0;
      opacity: 0.12;
      pointer-events: none;
      content: "";
      border-radius: 4px;
    }
    .icon {
      z-index: 1;
    }
    .icon.no-title {
      align-self: center;
    }
    .content {
      display: flex;
      justify-content: space-between;
      align-items: center;
      width: 100%;
      text-align: var(--float-start);
    }
    .content.narrow {
      flex-direction: column;
      align-items: flex-end;
    }
    .action {
      z-index: 1;
      width: min-content;
      --mdc-theme-primary: var(--primary-text-color);
    }
    .main-content {
      overflow-wrap: anywhere;
      word-break: break-word;
      margin-left: 8px;
      margin-right: 0;
      margin-inline-start: 8px;
      margin-inline-end: 0;
    }
    .title {
      margin-top: 2px;
      font-weight: var(--ha-font-weight-bold);
    }
    .action ha-icon-button {
      --mdc-theme-primary: var(--primary-text-color);
      --mdc-icon-button-size: 36px;
    }
    .issue-type.info > .icon {
      color: var(--info-color);
    }
    .issue-type.info::after {
      background-color: var(--info-color);
    }

    .issue-type.warning > .icon {
      color: var(--warning-color);
    }
    .issue-type.warning::after {
      background-color: var(--warning-color);
    }

    .issue-type.error > .icon {
      color: var(--error-color);
    }
    .issue-type.error::after {
      background-color: var(--error-color);
    }

    .issue-type.success > .icon {
      color: var(--success-color);
    }
    .issue-type.success::after {
      background-color: var(--success-color);
    }
    :host ::slotted(ul) {
      margin: 0;
      padding-inline-start: 20px;
    }
  `,(0,a.__decorate)([(0,i.Cb)()],d.prototype,"title",void 0),(0,a.__decorate)([(0,i.Cb)({attribute:"alert-type"})],d.prototype,"alertType",void 0),(0,a.__decorate)([(0,i.Cb)({type:Boolean})],d.prototype,"dismissable",void 0),(0,a.__decorate)([(0,i.Cb)({type:Boolean})],d.prototype,"narrow",void 0),d=(0,a.__decorate)([(0,i.Mo)("ha-alert")],d)},13965:function(e,t,r){var a=r(73742),o=r(59048),i=r(7616);class s extends o.oi{render(){return o.dy`
      ${this.header?o.dy`<h1 class="card-header">${this.header}</h1>`:o.Ld}
      <slot></slot>
    `}constructor(...e){super(...e),this.raised=!1}}s.styles=o.iv`
    :host {
      background: var(
        --ha-card-background,
        var(--card-background-color, white)
      );
      -webkit-backdrop-filter: var(--ha-card-backdrop-filter, none);
      backdrop-filter: var(--ha-card-backdrop-filter, none);
      box-shadow: var(--ha-card-box-shadow, none);
      box-sizing: border-box;
      border-radius: var(--ha-card-border-radius, 12px);
      border-width: var(--ha-card-border-width, 1px);
      border-style: solid;
      border-color: var(--ha-card-border-color, var(--divider-color, #e0e0e0));
      color: var(--primary-text-color);
      display: block;
      transition: all 0.3s ease-out;
      position: relative;
    }

    :host([raised]) {
      border: none;
      box-shadow: var(
        --ha-card-box-shadow,
        0px 2px 1px -1px rgba(0, 0, 0, 0.2),
        0px 1px 1px 0px rgba(0, 0, 0, 0.14),
        0px 1px 3px 0px rgba(0, 0, 0, 0.12)
      );
    }

    .card-header,
    :host ::slotted(.card-header) {
      color: var(--ha-card-header-color, var(--primary-text-color));
      font-family: var(--ha-card-header-font-family, inherit);
      font-size: var(--ha-card-header-font-size, var(--ha-font-size-2xl));
      letter-spacing: -0.012em;
      line-height: var(--ha-line-height-expanded);
      padding: 12px 16px 16px;
      display: block;
      margin-block-start: 0px;
      margin-block-end: 0px;
      font-weight: var(--ha-font-weight-normal);
    }

    :host ::slotted(.card-content:not(:first-child)),
    slot:not(:first-child)::slotted(.card-content) {
      padding-top: 0px;
      margin-top: -8px;
    }

    :host ::slotted(.card-content) {
      padding: 16px;
    }

    :host ::slotted(.card-actions) {
      border-top: 1px solid var(--divider-color, #e8e8e8);
      padding: 8px;
    }
  `,(0,a.__decorate)([(0,i.Cb)()],s.prototype,"header",void 0),(0,a.__decorate)([(0,i.Cb)({type:Boolean,reflect:!0})],s.prototype,"raised",void 0),s=(0,a.__decorate)([(0,i.Mo)("ha-card")],s)},83379:function(e,t,r){r.a(e,(async function(e,a){try{r.r(t),r.d(t,{HaIconOverflowMenu:()=>p});var o=r(73742),i=r(59048),s=r(7616),n=r(31733),l=r(77204),d=(r(51431),r(78645),r(40830),r(27341)),c=(r(72633),r(1963),e([d]));d=(c.then?(await c)():c)[0];const h="M12,16A2,2 0 0,1 14,18A2,2 0 0,1 12,20A2,2 0 0,1 10,18A2,2 0 0,1 12,16M12,10A2,2 0 0,1 14,12A2,2 0 0,1 12,14A2,2 0 0,1 10,12A2,2 0 0,1 12,10M12,4A2,2 0 0,1 14,6A2,2 0 0,1 12,8A2,2 0 0,1 10,6A2,2 0 0,1 12,4Z";class p extends i.oi{render(){return i.dy`
      ${this.narrow?i.dy` <!-- Collapsed representation for small screens -->
            <ha-md-button-menu
              @click=${this._handleIconOverflowMenuOpened}
              positioning="popover"
            >
              <ha-icon-button
                .label=${this.hass.localize("ui.common.overflow_menu")}
                .path=${h}
                slot="trigger"
              ></ha-icon-button>

              ${this.items.map((e=>e.divider?i.dy`<ha-md-divider
                      role="separator"
                      tabindex="-1"
                    ></ha-md-divider>`:i.dy`<ha-md-menu-item
                      ?disabled=${e.disabled}
                      .clickAction=${e.action}
                      class=${(0,n.$)({warning:Boolean(e.warning)})}
                    >
                      <ha-svg-icon
                        slot="start"
                        class=${(0,n.$)({warning:Boolean(e.warning)})}
                        .path=${e.path}
                      ></ha-svg-icon>
                      ${e.label}
                    </ha-md-menu-item> `))}
            </ha-md-button-menu>`:i.dy`
            <!-- Icon representation for big screens -->
            ${this.items.map((e=>e.narrowOnly?i.Ld:e.divider?i.dy`<div role="separator"></div>`:i.dy`<ha-tooltip
                      .disabled=${!e.tooltip}
                      .content=${e.tooltip??""}
                    >
                      <ha-icon-button
                        @click=${e.action}
                        .label=${e.label}
                        .path=${e.path}
                        ?disabled=${e.disabled}
                      ></ha-icon-button>
                    </ha-tooltip>`))}
          `}
    `}_handleIconOverflowMenuOpened(e){e.stopPropagation()}static get styles(){return[l.Qx,i.iv`
        :host {
          display: flex;
          justify-content: flex-end;
        }
        div[role="separator"] {
          border-right: 1px solid var(--divider-color);
          width: 1px;
        }
      `]}constructor(...e){super(...e),this.items=[],this.narrow=!1}}(0,o.__decorate)([(0,s.Cb)({attribute:!1})],p.prototype,"hass",void 0),(0,o.__decorate)([(0,s.Cb)({type:Array})],p.prototype,"items",void 0),(0,o.__decorate)([(0,s.Cb)({type:Boolean})],p.prototype,"narrow",void 0),p=(0,o.__decorate)([(0,s.Mo)("ha-icon-overflow-menu")],p),a()}catch(h){a(h)}}))},27341:function(e,t,r){r.a(e,(async function(e,t){try{var a=r(73742),o=r(52634),i=r(62685),s=r(59048),n=r(7616),l=r(75535),d=e([o]);o=(d.then?(await d)():d)[0],(0,l.jx)("tooltip.show",{keyframes:[{opacity:0},{opacity:1}],options:{duration:150,easing:"ease"}}),(0,l.jx)("tooltip.hide",{keyframes:[{opacity:1},{opacity:0}],options:{duration:400,easing:"ease"}});class c extends o.Z{}c.styles=[i.Z,s.iv`
      :host {
        --sl-tooltip-background-color: var(--secondary-background-color);
        --sl-tooltip-color: var(--primary-text-color);
        --sl-tooltip-font-family: var(
          --ha-tooltip-font-family,
          var(--ha-font-family-body)
        );
        --sl-tooltip-font-size: var(
          --ha-tooltip-font-size,
          var(--ha-font-size-s)
        );
        --sl-tooltip-font-weight: var(
          --ha-tooltip-font-weight,
          var(--ha-font-weight-normal)
        );
        --sl-tooltip-line-height: var(
          --ha-tooltip-line-height,
          var(--ha-line-height-condensed)
        );
        --sl-tooltip-padding: 8px;
        --sl-tooltip-border-radius: var(--ha-tooltip-border-radius, 4px);
        --sl-tooltip-arrow-size: var(--ha-tooltip-arrow-size, 8px);
        --sl-z-index-tooltip: var(--ha-tooltip-z-index, 1000);
      }
    `],c=(0,a.__decorate)([(0,n.Mo)("ha-tooltip")],c),t()}catch(c){t(c)}}))},15724:function(e,t,r){r.d(t,{q:()=>d});const a=/^[v^~<>=]*?(\d+)(?:\.([x*]|\d+)(?:\.([x*]|\d+)(?:\.([x*]|\d+))?(?:-([\da-z\-]+(?:\.[\da-z\-]+)*))?(?:\+[\da-z\-]+(?:\.[\da-z\-]+)*)?)?)?$/i,o=e=>{if("string"!=typeof e)throw new TypeError("Invalid argument expected string");const t=e.match(a);if(!t)throw new Error(`Invalid argument not valid semver ('${e}' received)`);return t.shift(),t},i=e=>"*"===e||"x"===e||"X"===e,s=e=>{const t=parseInt(e,10);return isNaN(t)?e:t},n=(e,t)=>{if(i(e)||i(t))return 0;const[r,a]=((e,t)=>typeof e!=typeof t?[String(e),String(t)]:[e,t])(s(e),s(t));return r>a?1:r<a?-1:0},l=(e,t)=>{for(let r=0;r<Math.max(e.length,t.length);r++){const a=n(e[r]||"0",t[r]||"0");if(0!==a)return a}return 0},d=(e,t,r)=>{p(r);const a=((e,t)=>{const r=o(e),a=o(t),i=r.pop(),s=a.pop(),n=l(r,a);return 0!==n?n:i&&s?l(i.split("."),s.split(".")):i||s?i?-1:1:0})(e,t);return c[r].includes(a)},c={">":[1],">=":[0,1],"=":[0],"<=":[-1,0],"<":[-1],"!=":[-1,1]},h=Object.keys(c),p=e=>{if("string"!=typeof e)throw new TypeError("Invalid operator type, expected string but got "+typeof e);if(-1===h.indexOf(e))throw new Error(`Invalid operator, expected one of ${h.join("|")}`)}},92799:function(e,t,r){var a=r(73742),o=r(59048),i=r(7616),s=r(31733),n=r(29740);const l=new(r(38059).r)("knx-project-tree-view");class d extends o.oi{connectedCallback(){super.connectedCallback();const e=t=>{Object.entries(t).forEach((([t,r])=>{r.group_addresses.length>0&&(this._selectableRanges[t]={selected:!1,groupAddresses:r.group_addresses}),e(r.group_ranges)}))};e(this.data.group_ranges),l.debug("ranges",this._selectableRanges)}render(){return o.dy`<div class="ha-tree-view">${this._recurseData(this.data.group_ranges)}</div>`}_recurseData(e,t=0){const r=Object.entries(e).map((([e,r])=>{const a=Object.keys(r.group_ranges).length>0;if(!(a||r.group_addresses.length>0))return o.Ld;const i=e in this._selectableRanges,n=!!i&&this._selectableRanges[e].selected,l={"range-item":!0,"root-range":0===t,"sub-range":t>0,selectable:i,"selected-range":n,"non-selected-range":i&&!n},d=o.dy`<div
        class=${(0,s.$)(l)}
        toggle-range=${i?e:o.Ld}
        @click=${i?this.multiselect?this._selectionChangedMulti:this._selectionChangedSingle:o.Ld}
      >
        <span class="range-key">${e}</span>
        <span class="range-text">${r.name}</span>
      </div>`;if(a){const e={"root-group":0===t,"sub-group":0!==t};return o.dy`<div class=${(0,s.$)(e)}>
          ${d} ${this._recurseData(r.group_ranges,t+1)}
        </div>`}return o.dy`${d}`}));return o.dy`${r}`}_selectionChangedMulti(e){const t=e.target.getAttribute("toggle-range");this._selectableRanges[t].selected=!this._selectableRanges[t].selected,this._selectionUpdate(),this.requestUpdate()}_selectionChangedSingle(e){const t=e.target.getAttribute("toggle-range"),r=this._selectableRanges[t].selected;Object.values(this._selectableRanges).forEach((e=>{e.selected=!1})),this._selectableRanges[t].selected=!r,this._selectionUpdate(),this.requestUpdate()}_selectionUpdate(){const e=Object.values(this._selectableRanges).reduce(((e,t)=>t.selected?e.concat(t.groupAddresses):e),[]);l.debug("selection changed",e),(0,n.B)(this,"knx-group-range-selection-changed",{groupAddresses:e})}constructor(...e){super(...e),this.multiselect=!1,this._selectableRanges={}}}d.styles=o.iv`
    :host {
      margin: 0;
      height: 100%;
      overflow-y: scroll;
      overflow-x: hidden;
      background-color: var(--card-background-color);
    }

    .ha-tree-view {
      cursor: default;
    }

    .root-group {
      margin-bottom: 8px;
    }

    .root-group > * {
      padding-top: 5px;
      padding-bottom: 5px;
    }

    .range-item {
      display: block;
      overflow: hidden;
      white-space: nowrap;
      text-overflow: ellipsis;
      font-size: 0.875rem;
    }

    .range-item > * {
      vertical-align: middle;
      pointer-events: none;
    }

    .range-key {
      color: var(--text-primary-color);
      font-size: 0.75rem;
      font-weight: 700;
      background-color: var(--label-badge-grey);
      border-radius: 4px;
      padding: 1px 4px;
      margin-right: 2px;
    }

    .root-range {
      padding-left: 8px;
      font-weight: 500;
      background-color: var(--secondary-background-color);

      & .range-key {
        color: var(--primary-text-color);
        background-color: var(--card-background-color);
      }
    }

    .sub-range {
      padding-left: 13px;
    }

    .selectable {
      cursor: pointer;
    }

    .selectable:hover {
      background-color: rgba(var(--rgb-primary-text-color), 0.04);
    }

    .selected-range {
      background-color: rgba(var(--rgb-primary-color), 0.12);

      & .range-key {
        background-color: var(--primary-color);
      }
    }

    .selected-range:hover {
      background-color: rgba(var(--rgb-primary-color), 0.07);
    }

    .non-selected-range {
      background-color: var(--card-background-color);
    }
  `,(0,a.__decorate)([(0,i.Cb)({attribute:!1})],d.prototype,"data",void 0),(0,a.__decorate)([(0,i.Cb)({attribute:!1})],d.prototype,"multiselect",void 0),(0,a.__decorate)([(0,i.SB)()],d.prototype,"_selectableRanges",void 0),d=(0,a.__decorate)([(0,i.Mo)("knx-project-tree-view")],d)},65793:function(e,t,r){r.d(t,{Am:()=>l,Wl:()=>i,Yh:()=>s,f3:()=>o,jQ:()=>v,q$:()=>n,tu:()=>b});var a=r(24110);const o={payload:e=>null==e.payload?"":Array.isArray(e.payload)?e.payload.reduce(((e,t)=>e+t.toString(16).padStart(2,"0")),"0x"):e.payload.toString(),valueWithUnit:e=>null==e.value?"":"number"==typeof e.value||"boolean"==typeof e.value||"string"==typeof e.value?e.value.toString()+(e.unit?" "+e.unit:""):(0,a.$w)(e.value),timeWithMilliseconds:e=>new Date(e.timestamp).toLocaleTimeString(["en-US"],{hour12:!1,hour:"2-digit",minute:"2-digit",second:"2-digit",fractionalSecondDigits:3}),dateWithMilliseconds:e=>new Date(e.timestamp).toLocaleTimeString([],{year:"numeric",month:"2-digit",day:"2-digit",hour:"2-digit",minute:"2-digit",second:"2-digit",fractionalSecondDigits:3}),dptNumber:e=>null==e.dpt_main?"":null==e.dpt_sub?e.dpt_main.toString():e.dpt_main.toString()+"."+e.dpt_sub.toString().padStart(3,"0"),dptNameNumber:e=>{const t=o.dptNumber(e);return null==e.dpt_name?`DPT ${t}`:t?`DPT ${t} ${e.dpt_name}`:e.dpt_name}},i=e=>null==e?"":e.main+(e.sub?"."+e.sub.toString().padStart(3,"0"):""),s=e=>e.toLocaleTimeString(void 0,{hour12:!1,hour:"2-digit",minute:"2-digit",second:"2-digit",fractionalSecondDigits:3}),n=e=>e.toLocaleDateString(void 0,{year:"numeric",month:"2-digit",day:"2-digit"})+", "+e.toLocaleTimeString(void 0,{hour12:!1,hour:"2-digit",minute:"2-digit",second:"2-digit",fractionalSecondDigits:3}),l=e=>{const t=new Date(e),r=e.match(/\.(\d{6})/),a=r?r[1]:"000000";return t.toLocaleDateString(void 0,{year:"numeric",month:"2-digit",day:"2-digit"})+", "+t.toLocaleTimeString(void 0,{hour12:!1,hour:"2-digit",minute:"2-digit",second:"2-digit"})+"."+a},d=1e3,c=1e3,h=60*c,p=60*h,u=2,g=3;function b(e){const t=e.indexOf(".");if(-1===t)return 1e3*Date.parse(e);let r=e.indexOf("Z",t);-1===r&&(r=e.indexOf("+",t),-1===r&&(r=e.indexOf("-",t))),-1===r&&(r=e.length);const a=e.slice(0,t)+e.slice(r),o=Date.parse(a);let i=e.slice(t+1,r);return i.length<6?i=i.padEnd(6,"0"):i.length>6&&(i=i.slice(0,6)),1e3*o+Number(i)}function v(e,t="milliseconds"){if(null==e)return"—";const r=e<0?"-":"",a=Math.abs(e),o="milliseconds"===t?Math.round(a/d):Math.floor(a/d),i="microseconds"===t?a%d:0,s=Math.floor(o/p),n=Math.floor(o%p/h),l=Math.floor(o%h/c),b=o%c,v=e=>e.toString().padStart(u,"0"),m=e=>e.toString().padStart(g,"0"),y="microseconds"===t?`.${m(b)}${m(i)}`:`.${m(b)}`,f=`${v(n)}:${v(l)}`;return`${r}${s>0?`${v(s)}:${f}`:f}${y}`}},18988:function(e,t,r){r.a(e,(async function(e,a){try{r.r(t),r.d(t,{KNXProjectView:()=>k});var o=r(73742),i=r(59048),s=r(7616),n=r(66842),l=r(28105),d=r(29173),c=r(86829),h=(r(62790),r(22543),r(13965),r(78645),r(83379)),p=(r(32780),r(60495)),u=(r(92799),r(15724)),g=r(63279),b=r(38059),v=r(65793),m=e([c,h,p]);[c,h,p]=m.then?(await m)():m;const y="M6,13H18V11H6M3,6V8H21V6M10,18H14V16H10V18Z",f="M19,13H13V19H11V13H5V11H11V5H13V11H19V13Z",_="M18 7C16.9 7 16 7.9 16 9V15C16 16.1 16.9 17 18 17H20C21.1 17 22 16.1 22 15V11H20V15H18V9H22V7H18M2 7V17H8V15H4V7H2M11 7C9.9 7 9 7.9 9 9V15C9 16.1 9.9 17 11 17H13C14.1 17 15 16.1 15 15V9C15 7.9 14.1 7 13 7H11M11 9H13V15H11V9Z",x=new b.r("knx-project-view"),w="3.3.0";class k extends i.oi{disconnectedCallback(){super.disconnectedCallback(),this._subscribed&&(this._subscribed(),this._subscribed=void 0)}async firstUpdated(){(0,g.ze)(this.hass).then((e=>{this._lastTelegrams=e})).catch((e=>{x.error("getGroupTelegrams",e),(0,d.c)("/knx/error",{replace:!0,data:e})})),this._subscribed=await(0,g.IP)(this.hass,(e=>{this.telegram_callback(e)}))}_isGroupRangeAvailable(){const e=this.knx.projectData?.info.xknxproject_version??"0.0.0";x.debug("project version: "+e),this._groupRangeAvailable=(0,u.q)(e,w,">=")}telegram_callback(e){this._lastTelegrams={...this._lastTelegrams,[e.destination]:e}}_groupAddressMenu(e){const t=[];return t.push({path:_,label:this.knx.localize("project_view_menu_view_telegrams"),action:()=>{(0,d.c)(`/knx/group_monitor?destination=${e.address}`)}}),1===e.dpt?.main&&t.push({path:f,label:this.knx.localize("project_view_menu_create_binary_sensor"),action:()=>{(0,d.c)("/knx/entities/create/binary_sensor?knx.ga_sensor.state="+e.address)}}),i.dy`
      <ha-icon-overflow-menu .hass=${this.hass} narrow .items=${t}> </ha-icon-overflow-menu>
    `}_getRows(e){return e.length?Object.entries(this.knx.projectData.group_addresses).reduce(((t,[r,a])=>(e.includes(r)&&t.push(a),t)),[]):Object.values(this.knx.projectData.group_addresses)}_visibleAddressesChanged(e){this._visibleGroupAddresses=e.detail.groupAddresses}render(){return this.hass?i.dy` <hass-tabs-subpage
      .hass=${this.hass}
      .narrow=${this.narrow}
      .route=${this.route}
      .tabs=${this.tabs}
      .localizeFunc=${this.knx.localize}
    >
      ${this._projectLoadTask.render({initial:()=>i.dy`
          <hass-loading-screen .message=${"Waiting to fetch project data."}></hass-loading-screen>
        `,pending:()=>i.dy`
          <hass-loading-screen .message=${"Loading KNX project data."}></hass-loading-screen>
        `,error:e=>(x.error("Error loading KNX project",e),i.dy`<ha-alert alert-type="error">"Error loading KNX project"</ha-alert>`),complete:()=>this.renderMain()})}
    </hass-tabs-subpage>`:i.dy` <hass-loading-screen></hass-loading-screen> `}renderMain(){const e=this._getRows(this._visibleGroupAddresses);return this.knx.projectData?i.dy`${this.narrow&&this._groupRangeAvailable?i.dy`<ha-icon-button
                slot="toolbar-icon"
                .label=${this.hass.localize("ui.components.related-filter-menu.filter")}
                .path=${y}
                @click=${this._toggleRangeSelector}
              ></ha-icon-button>`:i.Ld}
          <div class="sections">
            ${this._groupRangeAvailable?i.dy`
                  <knx-project-tree-view
                    .data=${this.knx.projectData}
                    @knx-group-range-selection-changed=${this._visibleAddressesChanged}
                  ></knx-project-tree-view>
                `:i.Ld}
            <ha-data-table
              class="ga-table"
              .hass=${this.hass}
              .columns=${this._columns(this.narrow,this.hass.language)}
              .data=${e}
              .hasFab=${!1}
              .searchLabel=${this.hass.localize("ui.components.data-table.search")}
              .clickable=${!1}
            ></ha-data-table>
          </div>`:i.dy` <ha-card .header=${this.knx.localize("attention")}>
          <div class="card-content">
            <p>${this.knx.localize("project_view_upload")}</p>
          </div>
        </ha-card>`}_toggleRangeSelector(){this.rangeSelectorHidden=!this.rangeSelectorHidden}constructor(...e){super(...e),this.rangeSelectorHidden=!0,this._visibleGroupAddresses=[],this._groupRangeAvailable=!1,this._lastTelegrams={},this._projectLoadTask=new n.iQ(this,{args:()=>[],task:async()=>{this.knx.projectInfo&&!this.knx.projectData&&await this.knx.loadProject(),this._isGroupRangeAvailable()}}),this._columns=(0,l.Z)(((e,t)=>({address:{filterable:!0,sortable:!0,title:this.knx.localize("project_view_table_address"),flex:1,minWidth:"100px"},name:{filterable:!0,sortable:!0,title:this.knx.localize("project_view_table_name"),flex:3},dpt:{sortable:!0,filterable:!0,title:this.knx.localize("project_view_table_dpt"),flex:1,minWidth:"82px",template:e=>e.dpt?i.dy`<span style="display:inline-block;width:24px;text-align:right;"
                  >${e.dpt.main}</span
                >${e.dpt.sub?"."+e.dpt.sub.toString().padStart(3,"0"):""} `:""},lastValue:{filterable:!0,title:this.knx.localize("project_view_table_last_value"),flex:2,template:e=>{const t=this._lastTelegrams[e.address];if(!t)return"";const r=v.f3.payload(t);return null==t.value?i.dy`<code>${r}</code>`:i.dy`<div title=${r}>
            ${v.f3.valueWithUnit(this._lastTelegrams[e.address])}
          </div>`}},updated:{title:this.knx.localize("project_view_table_updated"),flex:1,showNarrow:!1,template:e=>{const t=this._lastTelegrams[e.address];if(!t)return"";const r=`${v.f3.dateWithMilliseconds(t)}\n\n${t.source} ${t.source_name}`;return i.dy`<div title=${r}>
            ${(0,p.G)(new Date(t.timestamp),this.hass.locale)}
          </div>`}},actions:{title:"",minWidth:"72px",type:"overflow-menu",template:e=>this._groupAddressMenu(e)}})))}}k.styles=i.iv`
    hass-loading-screen {
      --app-header-background-color: var(--sidebar-background-color);
      --app-header-text-color: var(--sidebar-text-color);
    }
    .sections {
      display: flex;
      flex-direction: row;
      height: 100%;
    }

    :host([narrow]) knx-project-tree-view {
      position: absolute;
      max-width: calc(100% - 60px); /* 100% -> max 871px before not narrow */
      z-index: 1;
      right: 0;
      transition: 0.5s;
      border-left: 1px solid var(--divider-color);
    }

    :host([narrow][range-selector-hidden]) knx-project-tree-view {
      width: 0;
    }

    :host(:not([narrow])) knx-project-tree-view {
      max-width: 255px; /* min 616px - 816px for tree-view + ga-table (depending on side menu) */
    }

    .ga-table {
      flex: 1;
    }
  `,(0,o.__decorate)([(0,s.Cb)({type:Object})],k.prototype,"hass",void 0),(0,o.__decorate)([(0,s.Cb)({attribute:!1})],k.prototype,"knx",void 0),(0,o.__decorate)([(0,s.Cb)({type:Boolean,reflect:!0})],k.prototype,"narrow",void 0),(0,o.__decorate)([(0,s.Cb)({type:Object})],k.prototype,"route",void 0),(0,o.__decorate)([(0,s.Cb)({type:Array,reflect:!1})],k.prototype,"tabs",void 0),(0,o.__decorate)([(0,s.Cb)({type:Boolean,reflect:!0,attribute:"range-selector-hidden"})],k.prototype,"rangeSelectorHidden",void 0),(0,o.__decorate)([(0,s.SB)()],k.prototype,"_visibleGroupAddresses",void 0),(0,o.__decorate)([(0,s.SB)()],k.prototype,"_groupRangeAvailable",void 0),(0,o.__decorate)([(0,s.SB)()],k.prototype,"_subscribed",void 0),(0,o.__decorate)([(0,s.SB)()],k.prototype,"_lastTelegrams",void 0),k=(0,o.__decorate)([(0,s.Mo)("knx-project-view")],k),a()}catch(y){a(y)}}))},66842:function(e,t,r){r.d(t,{iQ:()=>i});var a=r(87059);const o=Symbol();class i{get taskComplete(){return this.t||(1===this.i?this.t=new Promise(((e,t)=>{this.o=e,this.h=t})):3===this.i?this.t=Promise.reject(this.l):this.t=Promise.resolve(this.u)),this.t}hostUpdate(){!0===this.autoRun&&this.S()}hostUpdated(){"afterUpdate"===this.autoRun&&this.S()}T(){if(void 0===this.j)return;const e=this.j();if(!Array.isArray(e))throw Error("The args function must return an array");return e}async S(){const e=this.T(),t=this.O;this.O=e,e===t||void 0===e||void 0!==t&&this.m(t,e)||await this.run(e)}async run(e){let t,r;e??=this.T(),this.O=e,1===this.i?this.q?.abort():(this.t=void 0,this.o=void 0,this.h=void 0),this.i=1,"afterUpdate"===this.autoRun?queueMicrotask((()=>this._.requestUpdate())):this._.requestUpdate();const a=++this.p;this.q=new AbortController;let i=!1;try{t=await this.v(e,{signal:this.q.signal})}catch(e){i=!0,r=e}if(this.p===a){if(t===o)this.i=0;else{if(!1===i){try{this.k?.(t)}catch{}this.i=2,this.o?.(t)}else{try{this.A?.(r)}catch{}this.i=3,this.h?.(r)}this.u=t,this.l=r}this._.requestUpdate()}}abort(e){1===this.i&&this.q?.abort(e)}get value(){return this.u}get error(){return this.l}get status(){return this.i}render(e){switch(this.i){case 0:return e.initial?.();case 1:return e.pending?.();case 2:return e.complete?.(this.value);case 3:return e.error?.(this.error);default:throw Error("Unexpected status: "+this.i)}}constructor(e,t,r){this.p=0,this.i=0,(this._=e).addController(this);const a="object"==typeof t?t:{task:t,args:r};this.v=a.task,this.j=a.args,this.m=a.argsEqual??s,this.k=a.onComplete,this.A=a.onError,this.autoRun=a.autoRun??!0,"initialValue"in a&&(this.u=a.initialValue,this.i=2,this.O=this.T?.())}}const s=(e,t)=>e===t||e.length===t.length&&e.every(((e,r)=>!(0,a.Qu)(e,t[r])))}};
//# sourceMappingURL=2669.4ee21450088e7a72.js.map