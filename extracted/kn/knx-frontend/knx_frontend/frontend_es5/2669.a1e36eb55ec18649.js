/*! For license information please see 2669.a1e36eb55ec18649.js.LICENSE.txt */
"use strict";(self.webpackChunkknx_frontend=self.webpackChunkknx_frontend||[]).push([["2669"],{13539:function(t,e,r){r.a(t,(async function(t,a){try{r.d(e,{Bt:function(){return d}});r(39710);var o=r(57900),i=r(3574),n=r(43956),s=t([o]);o=(s.then?(await s)():s)[0];const l=["sunday","monday","tuesday","wednesday","thursday","friday","saturday"],d=t=>t.first_weekday===n.FS.language?"weekInfo"in Intl.Locale.prototype?new Intl.Locale(t.language).weekInfo.firstDay%7:(0,i.L)(t.language)%7:l.includes(t.first_weekday)?l.indexOf(t.first_weekday):1;a()}catch(l){a(l)}}))},60495:function(t,e,r){r.a(t,(async function(t,a){try{r.d(e,{G:function(){return d}});var o=r(57900),i=r(28105),n=r(58713),s=t([o,n]);[o,n]=s.then?(await s)():s;const l=(0,i.Z)((t=>new Intl.RelativeTimeFormat(t.language,{numeric:"auto"}))),d=(t,e,r,a=!0)=>{const o=(0,n.W)(t,r,e);return a?l(e).format(o.value,o.unit):Intl.NumberFormat(e.language,{style:"unit",unit:o.unit,unitDisplay:"long"}).format(Math.abs(o.value))};a()}catch(l){a(l)}}))},58713:function(t,e,r){r.a(t,(async function(t,a){try{r.d(e,{W:function(){return p}});r(87799);var o=r(7722),i=r(66233),n=r(41238),s=r(13539),l=t([s]);s=(l.then?(await l)():l)[0];const c=1e3,h=60,u=60*h;function p(t,e=Date.now(),r,a={}){const l=Object.assign(Object.assign({},g),a||{}),d=(+t-+e)/c;if(Math.abs(d)<l.second)return{value:Math.round(d),unit:"second"};const p=d/h;if(Math.abs(p)<l.minute)return{value:Math.round(p),unit:"minute"};const v=d/u;if(Math.abs(v)<l.hour)return{value:Math.round(v),unit:"hour"};const b=new Date(t),f=new Date(e);b.setHours(0,0,0,0),f.setHours(0,0,0,0);const y=(0,o.j)(b,f);if(0===y)return{value:Math.round(v),unit:"hour"};if(Math.abs(y)<l.day)return{value:y,unit:"day"};const m=(0,s.Bt)(r),_=(0,i.z)(b,{weekStartsOn:m}),x=(0,i.z)(f,{weekStartsOn:m}),w=(0,n.p)(_,x);if(0===w)return{value:y,unit:"day"};if(Math.abs(w)<l.week)return{value:w,unit:"week"};const k=b.getFullYear()-f.getFullYear(),$=12*k+b.getMonth()-f.getMonth();return 0===$?{value:w,unit:"week"}:Math.abs($)<l.month||0===k?{value:$,unit:"month"}:{value:Math.round(k),unit:"year"}}const g={second:45,minute:45,hour:22,day:5,week:4,month:11};a()}catch(d){a(d)}}))},22543:function(t,e,r){r.r(e);r(26847),r(27530);var a=r(73742),o=r(59048),i=r(7616),n=r(31733),s=r(29740);r(78645),r(40830);let l,d,c,h,u=t=>t;const p={info:"M11,9H13V7H11M12,20C7.59,20 4,16.41 4,12C4,7.59 7.59,4 12,4C16.41,4 20,7.59 20,12C20,16.41 16.41,20 12,20M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M11,17H13V11H11V17Z",warning:"M12,2L1,21H23M12,6L19.53,19H4.47M11,10V14H13V10M11,16V18H13V16",error:"M11,15H13V17H11V15M11,7H13V13H11V7M12,2C6.47,2 2,6.5 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M12,20A8,8 0 0,1 4,12A8,8 0 0,1 12,4A8,8 0 0,1 20,12A8,8 0 0,1 12,20Z",success:"M20,12A8,8 0 0,1 12,20A8,8 0 0,1 4,12A8,8 0 0,1 12,4C12.76,4 13.5,4.11 14.2,4.31L15.77,2.74C14.61,2.26 13.34,2 12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12M7.91,10.08L6.5,11.5L11,16L21,6L19.59,4.58L11,13.17L7.91,10.08Z"};class g extends o.oi{render(){return(0,o.dy)(l||(l=u`
      <div
        class="issue-type ${0}"
        role="alert"
      >
        <div class="icon ${0}">
          <slot name="icon">
            <ha-svg-icon .path=${0}></ha-svg-icon>
          </slot>
        </div>
        <div class=${0}>
          <div class="main-content">
            ${0}
            <slot></slot>
          </div>
          <div class="action">
            <slot name="action">
              ${0}
            </slot>
          </div>
        </div>
      </div>
    `),(0,n.$)({[this.alertType]:!0}),this.title?"":"no-title",p[this.alertType],(0,n.$)({content:!0,narrow:this.narrow}),this.title?(0,o.dy)(d||(d=u`<div class="title">${0}</div>`),this.title):o.Ld,this.dismissable?(0,o.dy)(c||(c=u`<ha-icon-button
                    @click=${0}
                    label="Dismiss alert"
                    .path=${0}
                  ></ha-icon-button>`),this._dismissClicked,"M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z"):o.Ld)}_dismissClicked(){(0,s.B)(this,"alert-dismissed-clicked")}constructor(...t){super(...t),this.title="",this.alertType="info",this.dismissable=!1,this.narrow=!1}}g.styles=(0,o.iv)(h||(h=u`
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
  `)),(0,a.__decorate)([(0,i.Cb)()],g.prototype,"title",void 0),(0,a.__decorate)([(0,i.Cb)({attribute:"alert-type"})],g.prototype,"alertType",void 0),(0,a.__decorate)([(0,i.Cb)({type:Boolean})],g.prototype,"dismissable",void 0),(0,a.__decorate)([(0,i.Cb)({type:Boolean})],g.prototype,"narrow",void 0),g=(0,a.__decorate)([(0,i.Mo)("ha-alert")],g)},13965:function(t,e,r){r(26847),r(27530);var a=r(73742),o=r(59048),i=r(7616);let n,s,l,d=t=>t;class c extends o.oi{render(){return(0,o.dy)(n||(n=d`
      ${0}
      <slot></slot>
    `),this.header?(0,o.dy)(s||(s=d`<h1 class="card-header">${0}</h1>`),this.header):o.Ld)}constructor(...t){super(...t),this.raised=!1}}c.styles=(0,o.iv)(l||(l=d`
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
  `)),(0,a.__decorate)([(0,i.Cb)()],c.prototype,"header",void 0),(0,a.__decorate)([(0,i.Cb)({type:Boolean,reflect:!0})],c.prototype,"raised",void 0),c=(0,a.__decorate)([(0,i.Mo)("ha-card")],c)},83379:function(t,e,r){r.a(t,(async function(t,a){try{r.r(e),r.d(e,{HaIconOverflowMenu:function(){return x}});r(26847),r(81738),r(6989),r(27530);var o=r(73742),i=r(59048),n=r(7616),s=r(31733),l=r(77204),d=(r(51431),r(78645),r(40830),r(27341)),c=(r(72633),r(1963),t([d]));d=(c.then?(await c)():c)[0];let h,u,p,g,v,b,f,y,m=t=>t;const _="M12,16A2,2 0 0,1 14,18A2,2 0 0,1 12,20A2,2 0 0,1 10,18A2,2 0 0,1 12,16M12,10A2,2 0 0,1 14,12A2,2 0 0,1 12,14A2,2 0 0,1 10,12A2,2 0 0,1 12,10M12,4A2,2 0 0,1 14,6A2,2 0 0,1 12,8A2,2 0 0,1 10,6A2,2 0 0,1 12,4Z";class x extends i.oi{render(){return(0,i.dy)(h||(h=m`
      ${0}
    `),this.narrow?(0,i.dy)(u||(u=m` <!-- Collapsed representation for small screens -->
            <ha-md-button-menu
              @click=${0}
              positioning="popover"
            >
              <ha-icon-button
                .label=${0}
                .path=${0}
                slot="trigger"
              ></ha-icon-button>

              ${0}
            </ha-md-button-menu>`),this._handleIconOverflowMenuOpened,this.hass.localize("ui.common.overflow_menu"),_,this.items.map((t=>t.divider?(0,i.dy)(p||(p=m`<ha-md-divider
                      role="separator"
                      tabindex="-1"
                    ></ha-md-divider>`)):(0,i.dy)(g||(g=m`<ha-md-menu-item
                      ?disabled=${0}
                      .clickAction=${0}
                      class=${0}
                    >
                      <ha-svg-icon
                        slot="start"
                        class=${0}
                        .path=${0}
                      ></ha-svg-icon>
                      ${0}
                    </ha-md-menu-item> `),t.disabled,t.action,(0,s.$)({warning:Boolean(t.warning)}),(0,s.$)({warning:Boolean(t.warning)}),t.path,t.label)))):(0,i.dy)(v||(v=m`
            <!-- Icon representation for big screens -->
            ${0}
          `),this.items.map((t=>{var e;return t.narrowOnly?i.Ld:t.divider?(0,i.dy)(b||(b=m`<div role="separator"></div>`)):(0,i.dy)(f||(f=m`<ha-tooltip
                      .disabled=${0}
                      .content=${0}
                    >
                      <ha-icon-button
                        @click=${0}
                        .label=${0}
                        .path=${0}
                        ?disabled=${0}
                      ></ha-icon-button>
                    </ha-tooltip>`),!t.tooltip,null!==(e=t.tooltip)&&void 0!==e?e:"",t.action,t.label,t.path,t.disabled)}))))}_handleIconOverflowMenuOpened(t){t.stopPropagation()}static get styles(){return[l.Qx,(0,i.iv)(y||(y=m`
        :host {
          display: flex;
          justify-content: flex-end;
        }
        div[role="separator"] {
          border-right: 1px solid var(--divider-color);
          width: 1px;
        }
      `))]}constructor(...t){super(...t),this.items=[],this.narrow=!1}}(0,o.__decorate)([(0,n.Cb)({attribute:!1})],x.prototype,"hass",void 0),(0,o.__decorate)([(0,n.Cb)({type:Array})],x.prototype,"items",void 0),(0,o.__decorate)([(0,n.Cb)({type:Boolean})],x.prototype,"narrow",void 0),x=(0,o.__decorate)([(0,n.Mo)("ha-icon-overflow-menu")],x),a()}catch(h){a(h)}}))},27341:function(t,e,r){r.a(t,(async function(t,e){try{var a=r(73742),o=r(52634),i=r(62685),n=r(59048),s=r(7616),l=r(75535),d=t([o]);o=(d.then?(await d)():d)[0];let c,h=t=>t;(0,l.jx)("tooltip.show",{keyframes:[{opacity:0},{opacity:1}],options:{duration:150,easing:"ease"}}),(0,l.jx)("tooltip.hide",{keyframes:[{opacity:1},{opacity:0}],options:{duration:400,easing:"ease"}});class u extends o.Z{}u.styles=[i.Z,(0,n.iv)(c||(c=h`
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
    `))],u=(0,a.__decorate)([(0,s.Mo)("ha-tooltip")],u),e()}catch(c){e(c)}}))},15724:function(t,e,r){r.d(e,{q:function(){return d}});r(40777),r(39710),r(56389),r(26847),r(70820),r(64455),r(40005),r(27530);const a=/^[v^~<>=]*?(\d+)(?:\.([x*]|\d+)(?:\.([x*]|\d+)(?:\.([x*]|\d+))?(?:-([\da-z\-]+(?:\.[\da-z\-]+)*))?(?:\+[\da-z\-]+(?:\.[\da-z\-]+)*)?)?)?$/i,o=t=>{if("string"!=typeof t)throw new TypeError("Invalid argument expected string");const e=t.match(a);if(!e)throw new Error(`Invalid argument not valid semver ('${t}' received)`);return e.shift(),e},i=t=>"*"===t||"x"===t||"X"===t,n=t=>{const e=parseInt(t,10);return isNaN(e)?t:e},s=(t,e)=>{if(i(t)||i(e))return 0;const[r,a]=((t,e)=>typeof t!=typeof e?[String(t),String(e)]:[t,e])(n(t),n(e));return r>a?1:r<a?-1:0},l=(t,e)=>{for(let r=0;r<Math.max(t.length,e.length);r++){const a=s(t[r]||"0",e[r]||"0");if(0!==a)return a}return 0},d=(t,e,r)=>{u(r);const a=((t,e)=>{const r=o(t),a=o(e),i=r.pop(),n=a.pop(),s=l(r,a);return 0!==s?s:i&&n?l(i.split("."),n.split(".")):i||n?i?-1:1:0})(t,e);return c[r].includes(a)},c={">":[1],">=":[0,1],"=":[0],"<=":[-1,0],"<":[-1],"!=":[-1,1]},h=Object.keys(c),u=t=>{if("string"!=typeof t)throw new TypeError("Invalid operator type, expected string but got "+typeof t);if(-1===h.indexOf(t))throw new Error(`Invalid operator, expected one of ${h.join("|")}`)}},92799:function(t,e,r){r(26847),r(44438),r(81738),r(22960),r(6989),r(93190),r(27530);var a=r(73742),o=r(59048),i=r(7616),n=r(31733),s=r(29740),l=r(38059);let d,c,h,u,p,g,v=t=>t;const b=new l.r("knx-project-tree-view");class f extends o.oi{connectedCallback(){super.connectedCallback();const t=e=>{Object.entries(e).forEach((([e,r])=>{r.group_addresses.length>0&&(this._selectableRanges[e]={selected:!1,groupAddresses:r.group_addresses}),t(r.group_ranges)}))};t(this.data.group_ranges),b.debug("ranges",this._selectableRanges)}render(){return(0,o.dy)(d||(d=v`<div class="ha-tree-view">${0}</div>`),this._recurseData(this.data.group_ranges))}_recurseData(t,e=0){const r=Object.entries(t).map((([t,r])=>{const a=Object.keys(r.group_ranges).length>0;if(!(a||r.group_addresses.length>0))return o.Ld;const i=t in this._selectableRanges,s=!!i&&this._selectableRanges[t].selected,l={"range-item":!0,"root-range":0===e,"sub-range":e>0,selectable:i,"selected-range":s,"non-selected-range":i&&!s},d=(0,o.dy)(c||(c=v`<div
        class=${0}
        toggle-range=${0}
        @click=${0}
      >
        <span class="range-key">${0}</span>
        <span class="range-text">${0}</span>
      </div>`),(0,n.$)(l),i?t:o.Ld,i?this.multiselect?this._selectionChangedMulti:this._selectionChangedSingle:o.Ld,t,r.name);if(a){const t={"root-group":0===e,"sub-group":0!==e};return(0,o.dy)(h||(h=v`<div class=${0}>
          ${0} ${0}
        </div>`),(0,n.$)(t),d,this._recurseData(r.group_ranges,e+1))}return(0,o.dy)(u||(u=v`${0}`),d)}));return(0,o.dy)(p||(p=v`${0}`),r)}_selectionChangedMulti(t){const e=t.target.getAttribute("toggle-range");this._selectableRanges[e].selected=!this._selectableRanges[e].selected,this._selectionUpdate(),this.requestUpdate()}_selectionChangedSingle(t){const e=t.target.getAttribute("toggle-range"),r=this._selectableRanges[e].selected;Object.values(this._selectableRanges).forEach((t=>{t.selected=!1})),this._selectableRanges[e].selected=!r,this._selectionUpdate(),this.requestUpdate()}_selectionUpdate(){const t=Object.values(this._selectableRanges).reduce(((t,e)=>e.selected?t.concat(e.groupAddresses):t),[]);b.debug("selection changed",t),(0,s.B)(this,"knx-group-range-selection-changed",{groupAddresses:t})}constructor(...t){super(...t),this.multiselect=!1,this._selectableRanges={}}}f.styles=(0,o.iv)(g||(g=v`
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
  `)),(0,a.__decorate)([(0,i.Cb)({attribute:!1})],f.prototype,"data",void 0),(0,a.__decorate)([(0,i.Cb)({attribute:!1})],f.prototype,"multiselect",void 0),(0,a.__decorate)([(0,i.SB)()],f.prototype,"_selectableRanges",void 0),f=(0,a.__decorate)([(0,i.Mo)("knx-project-tree-view")],f)},65793:function(t,e,r){r.d(e,{Am:function(){return l},Wl:function(){return i},Yh:function(){return n},f3:function(){return o},jQ:function(){return b},q$:function(){return s},tu:function(){return v}});r(44438),r(81738),r(93190),r(64455),r(56303),r(40005);var a=r(24110);const o={payload:t=>null==t.payload?"":Array.isArray(t.payload)?t.payload.reduce(((t,e)=>t+e.toString(16).padStart(2,"0")),"0x"):t.payload.toString(),valueWithUnit:t=>null==t.value?"":"number"==typeof t.value||"boolean"==typeof t.value||"string"==typeof t.value?t.value.toString()+(t.unit?" "+t.unit:""):(0,a.$w)(t.value),timeWithMilliseconds:t=>new Date(t.timestamp).toLocaleTimeString(["en-US"],{hour12:!1,hour:"2-digit",minute:"2-digit",second:"2-digit",fractionalSecondDigits:3}),dateWithMilliseconds:t=>new Date(t.timestamp).toLocaleTimeString([],{year:"numeric",month:"2-digit",day:"2-digit",hour:"2-digit",minute:"2-digit",second:"2-digit",fractionalSecondDigits:3}),dptNumber:t=>null==t.dpt_main?"":null==t.dpt_sub?t.dpt_main.toString():t.dpt_main.toString()+"."+t.dpt_sub.toString().padStart(3,"0"),dptNameNumber:t=>{const e=o.dptNumber(t);return null==t.dpt_name?`DPT ${e}`:e?`DPT ${e} ${t.dpt_name}`:t.dpt_name}},i=t=>null==t?"":t.main+(t.sub?"."+t.sub.toString().padStart(3,"0"):""),n=t=>t.toLocaleTimeString(void 0,{hour12:!1,hour:"2-digit",minute:"2-digit",second:"2-digit",fractionalSecondDigits:3}),s=t=>t.toLocaleDateString(void 0,{year:"numeric",month:"2-digit",day:"2-digit"})+", "+t.toLocaleTimeString(void 0,{hour12:!1,hour:"2-digit",minute:"2-digit",second:"2-digit",fractionalSecondDigits:3}),l=t=>{const e=new Date(t),r=t.match(/\.(\d{6})/),a=r?r[1]:"000000";return e.toLocaleDateString(void 0,{year:"numeric",month:"2-digit",day:"2-digit"})+", "+e.toLocaleTimeString(void 0,{hour12:!1,hour:"2-digit",minute:"2-digit",second:"2-digit"})+"."+a},d=1e3,c=1e3,h=60*c,u=60*h,p=2,g=3;function v(t){const e=t.indexOf(".");if(-1===e)return 1e3*Date.parse(t);let r=t.indexOf("Z",e);-1===r&&(r=t.indexOf("+",e),-1===r&&(r=t.indexOf("-",e))),-1===r&&(r=t.length);const a=t.slice(0,e)+t.slice(r),o=Date.parse(a);let i=t.slice(e+1,r);return i.length<6?i=i.padEnd(6,"0"):i.length>6&&(i=i.slice(0,6)),1e3*o+Number(i)}function b(t,e="milliseconds"){if(null==t)return"—";const r=t<0?"-":"",a=Math.abs(t),o="milliseconds"===e?Math.round(a/d):Math.floor(a/d),i="microseconds"===e?a%d:0,n=Math.floor(o/u),s=Math.floor(o%u/h),l=Math.floor(o%h/c),v=o%c,b=t=>t.toString().padStart(p,"0"),f=t=>t.toString().padStart(g,"0"),y="microseconds"===e?`.${f(v)}${f(i)}`:`.${f(v)}`,m=`${b(s)}:${b(l)}`;return`${r}${n>0?`${b(n)}:${m}`:m}${y}`}},18988:function(t,e,r){r.a(t,(async function(t,a){try{r.r(e),r.d(e,{KNXProjectView:function(){return I}});r(39710),r(26847),r(2394),r(44438),r(81738),r(93190),r(87799),r(1455),r(56303),r(56389),r(27530);var o=r(73742),i=r(59048),n=r(7616),s=r(66842),l=r(28105),d=r(29173),c=r(86829),h=(r(62790),r(22543),r(13965),r(78645),r(83379)),u=(r(32780),r(60495)),p=(r(92799),r(15724)),g=r(63279),v=r(38059),b=r(65793),f=t([c,h,u]);[c,h,u]=f.then?(await f)():f;let y,m,_,x,w,k,$,M,j,A,C,S,L,H,z,V=t=>t;const O="M6,13H18V11H6M3,6V8H21V6M10,18H14V16H10V18Z",D="M19,13H13V19H11V13H5V11H11V5H13V11H19V13Z",T="M18 7C16.9 7 16 7.9 16 9V15C16 16.1 16.9 17 18 17H20C21.1 17 22 16.1 22 15V11H20V15H18V9H22V7H18M2 7V17H8V15H4V7H2M11 7C9.9 7 9 7.9 9 9V15C9 16.1 9.9 17 11 17H13C14.1 17 15 16.1 15 15V9C15 7.9 14.1 7 13 7H11M11 9H13V15H11V9Z",R=new v.r("knx-project-view"),B="3.3.0";class I extends i.oi{disconnectedCallback(){super.disconnectedCallback(),this._subscribed&&(this._subscribed(),this._subscribed=void 0)}async firstUpdated(){(0,g.ze)(this.hass).then((t=>{this._lastTelegrams=t})).catch((t=>{R.error("getGroupTelegrams",t),(0,d.c)("/knx/error",{replace:!0,data:t})})),this._subscribed=await(0,g.IP)(this.hass,(t=>{this.telegram_callback(t)}))}_isGroupRangeAvailable(){var t,e;const r=null!==(t=null===(e=this.knx.projectData)||void 0===e?void 0:e.info.xknxproject_version)&&void 0!==t?t:"0.0.0";R.debug("project version: "+r),this._groupRangeAvailable=(0,p.q)(r,B,">=")}telegram_callback(t){this._lastTelegrams=Object.assign(Object.assign({},this._lastTelegrams),{},{[t.destination]:t})}_groupAddressMenu(t){var e;const r=[];return r.push({path:T,label:this.knx.localize("project_view_menu_view_telegrams"),action:()=>{(0,d.c)(`/knx/group_monitor?destination=${t.address}`)}}),1===(null===(e=t.dpt)||void 0===e?void 0:e.main)&&r.push({path:D,label:this.knx.localize("project_view_menu_create_binary_sensor"),action:()=>{(0,d.c)("/knx/entities/create/binary_sensor?knx.ga_sensor.state="+t.address)}}),(0,i.dy)(y||(y=V`
      <ha-icon-overflow-menu .hass=${0} narrow .items=${0}> </ha-icon-overflow-menu>
    `),this.hass,r)}_getRows(t){return t.length?Object.entries(this.knx.projectData.group_addresses).reduce(((e,[r,a])=>(t.includes(r)&&e.push(a),e)),[]):Object.values(this.knx.projectData.group_addresses)}_visibleAddressesChanged(t){this._visibleGroupAddresses=t.detail.groupAddresses}render(){return this.hass?(0,i.dy)(_||(_=V` <hass-tabs-subpage
      .hass=${0}
      .narrow=${0}
      .route=${0}
      .tabs=${0}
      .localizeFunc=${0}
    >
      ${0}
    </hass-tabs-subpage>`),this.hass,this.narrow,this.route,this.tabs,this.knx.localize,this._projectLoadTask.render({initial:()=>(0,i.dy)(x||(x=V`
          <hass-loading-screen .message=${0}></hass-loading-screen>
        `),"Waiting to fetch project data."),pending:()=>(0,i.dy)(w||(w=V`
          <hass-loading-screen .message=${0}></hass-loading-screen>
        `),"Loading KNX project data."),error:t=>(R.error("Error loading KNX project",t),(0,i.dy)(k||(k=V`<ha-alert alert-type="error">"Error loading KNX project"</ha-alert>`))),complete:()=>this.renderMain()})):(0,i.dy)(m||(m=V` <hass-loading-screen></hass-loading-screen> `))}renderMain(){const t=this._getRows(this._visibleGroupAddresses);return this.knx.projectData?(0,i.dy)($||($=V`${0}
          <div class="sections">
            ${0}
            <ha-data-table
              class="ga-table"
              .hass=${0}
              .columns=${0}
              .data=${0}
              .hasFab=${0}
              .searchLabel=${0}
              .clickable=${0}
            ></ha-data-table>
          </div>`),this.narrow&&this._groupRangeAvailable?(0,i.dy)(M||(M=V`<ha-icon-button
                slot="toolbar-icon"
                .label=${0}
                .path=${0}
                @click=${0}
              ></ha-icon-button>`),this.hass.localize("ui.components.related-filter-menu.filter"),O,this._toggleRangeSelector):i.Ld,this._groupRangeAvailable?(0,i.dy)(j||(j=V`
                  <knx-project-tree-view
                    .data=${0}
                    @knx-group-range-selection-changed=${0}
                  ></knx-project-tree-view>
                `),this.knx.projectData,this._visibleAddressesChanged):i.Ld,this.hass,this._columns(this.narrow,this.hass.language),t,!1,this.hass.localize("ui.components.data-table.search"),!1):(0,i.dy)(A||(A=V` <ha-card .header=${0}>
          <div class="card-content">
            <p>${0}</p>
          </div>
        </ha-card>`),this.knx.localize("attention"),this.knx.localize("project_view_upload"))}_toggleRangeSelector(){this.rangeSelectorHidden=!this.rangeSelectorHidden}constructor(...t){super(...t),this.rangeSelectorHidden=!0,this._visibleGroupAddresses=[],this._groupRangeAvailable=!1,this._lastTelegrams={},this._projectLoadTask=new s.iQ(this,{args:()=>[],task:async()=>{this.knx.projectInfo&&!this.knx.projectData&&await this.knx.loadProject(),this._isGroupRangeAvailable()}}),this._columns=(0,l.Z)(((t,e)=>({address:{filterable:!0,sortable:!0,title:this.knx.localize("project_view_table_address"),flex:1,minWidth:"100px"},name:{filterable:!0,sortable:!0,title:this.knx.localize("project_view_table_name"),flex:3},dpt:{sortable:!0,filterable:!0,title:this.knx.localize("project_view_table_dpt"),flex:1,minWidth:"82px",template:t=>t.dpt?(0,i.dy)(C||(C=V`<span style="display:inline-block;width:24px;text-align:right;"
                  >${0}</span
                >${0} `),t.dpt.main,t.dpt.sub?"."+t.dpt.sub.toString().padStart(3,"0"):""):""},lastValue:{filterable:!0,title:this.knx.localize("project_view_table_last_value"),flex:2,template:t=>{const e=this._lastTelegrams[t.address];if(!e)return"";const r=b.f3.payload(e);return null==e.value?(0,i.dy)(S||(S=V`<code>${0}</code>`),r):(0,i.dy)(L||(L=V`<div title=${0}>
            ${0}
          </div>`),r,b.f3.valueWithUnit(this._lastTelegrams[t.address]))}},updated:{title:this.knx.localize("project_view_table_updated"),flex:1,showNarrow:!1,template:t=>{const e=this._lastTelegrams[t.address];if(!e)return"";const r=`${b.f3.dateWithMilliseconds(e)}\n\n${e.source} ${e.source_name}`;return(0,i.dy)(H||(H=V`<div title=${0}>
            ${0}
          </div>`),r,(0,u.G)(new Date(e.timestamp),this.hass.locale))}},actions:{title:"",minWidth:"72px",type:"overflow-menu",template:t=>this._groupAddressMenu(t)}})))}}I.styles=(0,i.iv)(z||(z=V`
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
  `)),(0,o.__decorate)([(0,n.Cb)({type:Object})],I.prototype,"hass",void 0),(0,o.__decorate)([(0,n.Cb)({attribute:!1})],I.prototype,"knx",void 0),(0,o.__decorate)([(0,n.Cb)({type:Boolean,reflect:!0})],I.prototype,"narrow",void 0),(0,o.__decorate)([(0,n.Cb)({type:Object})],I.prototype,"route",void 0),(0,o.__decorate)([(0,n.Cb)({type:Array,reflect:!1})],I.prototype,"tabs",void 0),(0,o.__decorate)([(0,n.Cb)({type:Boolean,reflect:!0,attribute:"range-selector-hidden"})],I.prototype,"rangeSelectorHidden",void 0),(0,o.__decorate)([(0,n.SB)()],I.prototype,"_visibleGroupAddresses",void 0),(0,o.__decorate)([(0,n.SB)()],I.prototype,"_groupRangeAvailable",void 0),(0,o.__decorate)([(0,n.SB)()],I.prototype,"_subscribed",void 0),(0,o.__decorate)([(0,n.SB)()],I.prototype,"_lastTelegrams",void 0),I=(0,o.__decorate)([(0,n.Mo)("knx-project-view")],I),a()}catch(y){a(y)}}))},2503:function(t,e,r){var a=r(77341),o=r(30456),i=r(88018),n=r(65085),s=r(60968),l=r(81455),d=r(61360);a({global:!0,enumerable:!0,dontCallGetSet:!0,forced:l((function(){return d&&1!==Object.getOwnPropertyDescriptor(o,"queueMicrotask").value.length}))},{queueMicrotask:function(t){s(arguments.length,1),i(n(t))}})},66842:function(t,e,r){r.d(e,{iQ:function(){return i}});r(84730),r(40777),r(81738),r(33480),r(1455),r(2503);var a=r(87059);const o=Symbol();class i{get taskComplete(){return this.t||(1===this.i?this.t=new Promise(((t,e)=>{this.o=t,this.h=e})):3===this.i?this.t=Promise.reject(this.l):this.t=Promise.resolve(this.u)),this.t}hostUpdate(){!0===this.autoRun&&this.S()}hostUpdated(){"afterUpdate"===this.autoRun&&this.S()}T(){if(void 0===this.j)return;const t=this.j();if(!Array.isArray(t))throw Error("The args function must return an array");return t}async S(){const t=this.T(),e=this.O;this.O=t,t===e||void 0===t||void 0!==e&&this.m(e,t)||await this.run(t)}async run(t){var e;let r,a;null!=t||(t=this.T()),this.O=t,1===this.i?null===(e=this.q)||void 0===e||e.abort():(this.t=void 0,this.o=void 0,this.h=void 0),this.i=1,"afterUpdate"===this.autoRun?queueMicrotask((()=>this._.requestUpdate())):this._.requestUpdate();const i=++this.p;this.q=new AbortController;let n=!1;try{r=await this.v(t,{signal:this.q.signal})}catch(t){n=!0,a=t}if(this.p===i){if(r===o)this.i=0;else{if(!1===n){var s;try{var l;null===(l=this.k)||void 0===l||l.call(this,r)}catch(h){}this.i=2,null===(s=this.o)||void 0===s||s.call(this,r)}else{var d;try{var c;null===(c=this.A)||void 0===c||c.call(this,a)}catch(u){}this.i=3,null===(d=this.h)||void 0===d||d.call(this,a)}this.u=r,this.l=a}this._.requestUpdate()}}abort(t){var e;1===this.i&&(null===(e=this.q)||void 0===e||e.abort(t))}get value(){return this.u}get error(){return this.l}get status(){return this.i}render(t){var e,r,a,o;switch(this.i){case 0:return null===(e=t.initial)||void 0===e?void 0:e.call(t);case 1:return null===(r=t.pending)||void 0===r?void 0:r.call(t);case 2:return null===(a=t.complete)||void 0===a?void 0:a.call(t,this.value);case 3:return null===(o=t.error)||void 0===o?void 0:o.call(t,this.error);default:throw Error("Unexpected status: "+this.i)}}constructor(t,e,r){var a,o,i;this.p=0,this.i=0,(this._=t).addController(this);const s="object"==typeof e?e:{task:e,args:r};this.v=s.task,this.j=s.args,this.m=null!==(a=s.argsEqual)&&void 0!==a?a:n,this.k=s.onComplete,this.A=s.onError,this.autoRun=null===(o=s.autoRun)||void 0===o||o,"initialValue"in s&&(this.u=s.initialValue,this.i=2,this.O=null===(i=this.T)||void 0===i?void 0:i.call(this))}}const n=(t,e)=>t===e||t.length===e.length&&t.every(((t,r)=>!(0,a.Qu)(t,e[r])))}}]);
//# sourceMappingURL=2669.a1e36eb55ec18649.js.map