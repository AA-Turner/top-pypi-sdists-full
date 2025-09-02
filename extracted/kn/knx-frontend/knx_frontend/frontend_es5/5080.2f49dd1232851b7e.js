"use strict";(self.webpackChunkknx_frontend=self.webpackChunkknx_frontend||[]).push([["5080"],{74608:function(e,t,i){function o(e){return null==e||Array.isArray(e)?e:[e]}i.d(t,{r:function(){return o}})},13228:function(e,t,i){i.d(t,{z:function(){return o}});i(39710),i(56389);const o=e=>(t,i)=>e.includes(t,i)},42822:function(e,t,i){i.d(t,{p:function(){return o}});i(39710),i(56389);const o=(e,t)=>e&&e.config.components.includes(t)},40985:function(e,t,i){i.d(t,{i:function(){return a}});i(40777),i(87799);const o=(0,i(48112).P)((e=>{history.replaceState({scrollPosition:e},"")}),300);function a(e){return(t,i)=>{if("object"==typeof i)throw new Error("This decorator does not support this compilation type.");const a=t.connectedCallback;t.connectedCallback=function(){a.call(this);const t=this[i];t&&this.updateComplete.then((()=>{const i=this.renderRoot.querySelector(e);i&&setTimeout((()=>{i.scrollTop=t}),0)}))};const r=Object.getOwnPropertyDescriptor(t,i);let s;if(void 0===r)s={get(){var e;return this[`__${String(i)}`]||(null===(e=history.state)||void 0===e?void 0:e.scrollPosition)},set(e){o(e),this[`__${String(i)}`]=e},configurable:!0,enumerable:!0};else{const e=r.set;s=Object.assign(Object.assign({},r),{},{set(t){o(t),this[`__${String(i)}`]=t,null==e||e.call(this,t)}})}Object.defineProperty(t,i,s)}}},69342:function(e,t,i){i.d(t,{h:function(){return r}});i(40777),i(26847),i(81738),i(22960),i(27530);var o=i(59048),a=i(79104);const r=(0,a.XM)(class extends a.Xe{update(e,[t,i]){return this._element&&this._element.localName===t?(i&&Object.entries(i).forEach((([e,t])=>{this._element[e]=t})),o.Jb):this.render(t,i)}render(e,t){return this._element=document.createElement(e),t&&Object.entries(t).forEach((([e,t])=>{this._element[e]=t})),this._element}constructor(e){if(super(e),e.type!==a.pX.CHILD)throw new Error("dynamicElementDirective can only be used in content bindings")}})},41806:function(e,t,i){i.d(t,{U:function(){return o}});const o=e=>e.stopPropagation()},71188:function(e,t,i){i.d(t,{D:function(){return o}});i(20655);const o=e=>{var t;return null===(t=e.name)||void 0===t?void 0:t.trim()}},41099:function(e,t,i){i.d(t,{r:function(){return o}});i(20655);const o=e=>{var t;return null===(t=e.name)||void 0===t?void 0:t.trim()}},31298:function(e,t,i){i.d(t,{C:function(){return a}});i(64455),i(56303),i(6202);var o=i(93318);const a=e=>{return t=e.entity_id,void 0===(i=e.attributes).friendly_name?(0,o.p)(t).replace(/_/g," "):(null!==(a=i.friendly_name)&&void 0!==a?a:"").toString();var t,i,a}},8028:function(e,t,i){i.d(t,{C:function(){return o}});const o=(e,t)=>{const i=e.floor_id;return{area:e,floor:(i?t.floors[i]:void 0)||null}}},39186:function(e,t,i){i.d(t,{q:function(){return m}});i(26847),i(18574),i(81738),i(94814),i(6989),i(27530),i(64455),i(6202);const o=e=>e.normalize("NFD").replace(/[\u0300-\u036F]/g,"");i(40777),i(2394),i(56303);var a=function(e){return e[e.Null=0]="Null",e[e.Backspace=8]="Backspace",e[e.Tab=9]="Tab",e[e.LineFeed=10]="LineFeed",e[e.CarriageReturn=13]="CarriageReturn",e[e.Space=32]="Space",e[e.ExclamationMark=33]="ExclamationMark",e[e.DoubleQuote=34]="DoubleQuote",e[e.Hash=35]="Hash",e[e.DollarSign=36]="DollarSign",e[e.PercentSign=37]="PercentSign",e[e.Ampersand=38]="Ampersand",e[e.SingleQuote=39]="SingleQuote",e[e.OpenParen=40]="OpenParen",e[e.CloseParen=41]="CloseParen",e[e.Asterisk=42]="Asterisk",e[e.Plus=43]="Plus",e[e.Comma=44]="Comma",e[e.Dash=45]="Dash",e[e.Period=46]="Period",e[e.Slash=47]="Slash",e[e.Digit0=48]="Digit0",e[e.Digit1=49]="Digit1",e[e.Digit2=50]="Digit2",e[e.Digit3=51]="Digit3",e[e.Digit4=52]="Digit4",e[e.Digit5=53]="Digit5",e[e.Digit6=54]="Digit6",e[e.Digit7=55]="Digit7",e[e.Digit8=56]="Digit8",e[e.Digit9=57]="Digit9",e[e.Colon=58]="Colon",e[e.Semicolon=59]="Semicolon",e[e.LessThan=60]="LessThan",e[e.Equals=61]="Equals",e[e.GreaterThan=62]="GreaterThan",e[e.QuestionMark=63]="QuestionMark",e[e.AtSign=64]="AtSign",e[e.A=65]="A",e[e.B=66]="B",e[e.C=67]="C",e[e.D=68]="D",e[e.E=69]="E",e[e.F=70]="F",e[e.G=71]="G",e[e.H=72]="H",e[e.I=73]="I",e[e.J=74]="J",e[e.K=75]="K",e[e.L=76]="L",e[e.M=77]="M",e[e.N=78]="N",e[e.O=79]="O",e[e.P=80]="P",e[e.Q=81]="Q",e[e.R=82]="R",e[e.S=83]="S",e[e.T=84]="T",e[e.U=85]="U",e[e.V=86]="V",e[e.W=87]="W",e[e.X=88]="X",e[e.Y=89]="Y",e[e.Z=90]="Z",e[e.OpenSquareBracket=91]="OpenSquareBracket",e[e.Backslash=92]="Backslash",e[e.CloseSquareBracket=93]="CloseSquareBracket",e[e.Caret=94]="Caret",e[e.Underline=95]="Underline",e[e.BackTick=96]="BackTick",e[e.a=97]="a",e[e.b=98]="b",e[e.c=99]="c",e[e.d=100]="d",e[e.e=101]="e",e[e.f=102]="f",e[e.g=103]="g",e[e.h=104]="h",e[e.i=105]="i",e[e.j=106]="j",e[e.k=107]="k",e[e.l=108]="l",e[e.m=109]="m",e[e.n=110]="n",e[e.o=111]="o",e[e.p=112]="p",e[e.q=113]="q",e[e.r=114]="r",e[e.s=115]="s",e[e.t=116]="t",e[e.u=117]="u",e[e.v=118]="v",e[e.w=119]="w",e[e.x=120]="x",e[e.y=121]="y",e[e.z=122]="z",e[e.OpenCurlyBrace=123]="OpenCurlyBrace",e[e.Pipe=124]="Pipe",e[e.CloseCurlyBrace=125]="CloseCurlyBrace",e[e.Tilde=126]="Tilde",e}({});const r=128;function s(){const e=[],t=[];for(let i=0;i<=r;i++)t[i]=0;for(let i=0;i<=r;i++)e.push(t.slice(0));return e}function n(e,t){if(t<0||t>=e.length)return!1;const i=e.codePointAt(t);switch(i){case a.Underline:case a.Dash:case a.Period:case a.Space:case a.Slash:case a.Backslash:case a.SingleQuote:case a.DoubleQuote:case a.Colon:case a.DollarSign:case a.LessThan:case a.OpenParen:case a.OpenSquareBracket:return!0;case void 0:return!1;default:return(o=i)>=127462&&o<=127487||8986===o||8987===o||9200===o||9203===o||o>=9728&&o<=10175||11088===o||11093===o||o>=127744&&o<=128591||o>=128640&&o<=128764||o>=128992&&o<=129003||o>=129280&&o<=129535||o>=129648&&o<=129750?!0:!1}var o}function l(e,t){if(t<0||t>=e.length)return!1;switch(e.charCodeAt(t)){case a.Space:case a.Tab:return!0;default:return!1}}function d(e,t,i){return t[e]!==i[e]}function c(e,t,i,o,a,s,n){const l=e.length>r?r:e.length,c=o.length>r?r:o.length;if(i>=l||s>=c||l-i>c-s)return;if(!function(e,t,i,o,a,r,s=!1){for(;t<i&&a<r;)e[t]===o[a]&&(s&&(p[t]=a),t+=1),a+=1;return t===i}(t,i,l,a,s,c,!0))return;let g;!function(e,t,i,o,a,r){let s=e-1,n=t-1;for(;s>=i&&n>=o;)a[s]===r[n]&&(u[s]=n,s--),n--}(l,c,i,s,t,a);let m,y,f=1;const x=[!1];for(g=1,m=i;m<l;g++,m++){const r=p[m],n=u[m],d=m+1<l?u[m+1]:c;for(f=r-s+1,y=r;y<d;f++,y++){let l=Number.MIN_SAFE_INTEGER,d=!1;y<=n&&(l=h(e,t,m,i,o,a,y,c,s,0===v[g-1][f-1],x));let p=0;l!==Number.MAX_SAFE_INTEGER&&(d=!0,p=l+b[g-1][f-1]);const u=y>r,$=u?b[g][f-1]+(v[g][f-1]>0?-5:0):0,w=y>r+1&&v[g][f-1]>0,C=w?b[g][f-2]+(v[g][f-2]>0?-5:0):0;if(w&&(!u||C>=$)&&(!d||C>=p))b[g][f]=C,_[g][f]=3,v[g][f]=0;else if(u&&(!d||$>=p))b[g][f]=$,_[g][f]=2,v[g][f]=0;else{if(!d)throw new Error("not possible");b[g][f]=p,_[g][f]=1,v[g][f]=v[g-1][f-1]+1}}}if(!x[0]&&!n)return;g--,f--;const $=[b[g][f],s];let w=0,C=0;for(;g>=1;){let e=f;do{const t=_[g][e];if(3===t)e-=2;else{if(2!==t)break;e-=1}}while(e>=1);w>1&&t[i+g-1]===a[s+f-1]&&!d(e+s-1,o,a)&&w+1>v[g][e]&&(e=f),e===f?w++:w=1,C||(C=e),g--,f=e-1,$.push(f)}c===l&&($[0]+=2);const k=C-l;return $[0]-=k,$}function h(e,t,i,o,a,r,s,c,h,p,u){if(t[i]!==r[s])return Number.MIN_SAFE_INTEGER;let v=1,b=!1;return s===i-o?v=e[i]===a[s]?7:5:!d(s,a,r)||0!==s&&d(s-1,a,r)?!n(r,s)||0!==s&&n(r,s-1)?(n(r,s-1)||l(r,s-1))&&(v=5,b=!0):v=5:(v=e[i]===a[s]?7:5,b=!0),v>1&&i===o&&(u[0]=!0),b||(b=d(s,a,r)||n(r,s-1)||l(r,s-1)),i===o?s>h&&(v-=b?3:5):v+=p?b?2:0:b?0:1,s+1===c&&(v-=b?3:5),v}const p=g(256),u=g(256),v=s(),b=s(),_=s();function g(e){const t=[];for(let i=0;i<=e;i++)t[i]=0;return t}const m=(e,t)=>t.map((t=>(t.score=((e,t)=>{let i=Number.NEGATIVE_INFINITY;for(const a of t.strings){const t=c(e,o(e.toLowerCase()),0,a,o(a.toLowerCase()),0,!0);if(!t)continue;const r=0===t[0]?1:t[0];r>i&&(i=r)}if(i!==Number.NEGATIVE_INFINITY)return i})(e,t),t))).filter((e=>void 0!==e.score)).sort((({score:e=0},{score:t=0})=>e>t?-1:e<t?1:0))},48112:function(e,t,i){i.d(t,{P:function(){return o}});i(26847),i(27530);const o=(e,t,i=!0,o=!0)=>{let a,r=0;const s=(...s)=>{const n=()=>{r=!1===i?0:Date.now(),a=void 0,e(...s)},l=Date.now();r||!1!==i||(r=l);const d=t-(l-r);d<=0||d>t?(a&&(clearTimeout(a),a=void 0),r=l,e(...s)):a||!1===o||(a=window.setTimeout(n,d))};return s.cancel=()=>{clearTimeout(a),a=void 0,r=0},s}},2414:function(e,t,i){var o=i(73742),a=i(38438),r=i(7616);class s extends a.l{}s=(0,o.__decorate)([(0,r.Mo)("ha-chip-set")],s)},91572:function(e,t,i){var o=i(73742),a=i(57714),r=i(52732),s=i(98939),n=i(23533),l=i(40621),d=i(59048),c=i(7616);let h;class p extends a.W{}p.styles=[n.W,l.W,s.W,r.W,(0,d.iv)(h||(h=(e=>e)`
      :host {
        --md-sys-color-primary: var(--primary-text-color);
        --md-sys-color-on-surface: var(--primary-text-color);
        --md-sys-color-on-surface-variant: var(--primary-text-color);
        --md-sys-color-on-secondary-container: var(--primary-text-color);
        --md-input-chip-container-shape: 16px;
        --md-input-chip-outline-color: var(--outline-color);
        --md-input-chip-selected-container-color: rgba(
          var(--rgb-primary-text-color),
          0.15
        );
        --ha-input-chip-selected-container-opacity: 1;
        --md-input-chip-label-text-font: Roboto, sans-serif;
      }
      /** Set the size of mdc icons **/
      ::slotted([slot="icon"]) {
        display: flex;
        --mdc-icon-size: var(--md-input-chip-icon-size, 18px);
      }
      .selected::before {
        opacity: var(--ha-input-chip-selected-container-opacity);
      }
    `))],p=(0,o.__decorate)([(0,c.Mo)("ha-input-chip")],p)},99495:function(e,t,i){i.a(e,(async function(e,t){try{i(39710),i(26847),i(81738),i(33480),i(94814),i(6989),i(72489),i(1455),i(56389),i(44261),i(27530);var o=i(73742),a=i(59048),r=i(7616),s=i(28105),n=i(29740),l=i(71188),d=i(76151),c=i(41099),h=i(8028),p=i(57108),u=i(57774),v=i(81665),b=i(95846),_=(i(57264),i(33321)),g=(i(78645),i(40830),e([_]));_=(g.then?(await g)():g)[0];let m,y,f,x,$,w,C=e=>e;const k="M19,13H13V19H11V13H5V11H11V5H13V11H19V13Z",V="M20 2H4C2.9 2 2 2.9 2 4V20C2 21.11 2.9 22 4 22H20C21.11 22 22 21.11 22 20V4C22 2.9 21.11 2 20 2M4 6L6 4H10.9L4 10.9V6M4 13.7L13.7 4H18.6L4 18.6V13.7M20 18L18 20H13.1L20 13.1V18M20 10.3L10.3 20H5.4L20 5.4V10.3Z",L="___ADD_NEW___";class S extends a.oi{async open(){var e;await this.updateComplete,await(null===(e=this._picker)||void 0===e?void 0:e.open())}render(){var e;const t=null!==(e=this.placeholder)&&void 0!==e?e:this.hass.localize("ui.components.area-picker.area"),i=this._computeValueRenderer(this.hass.areas);return(0,a.dy)(m||(m=C`
      <ha-generic-picker
        .hass=${0}
        .autofocus=${0}
        .label=${0}
        .helper=${0}
        .notFoundLabel=${0}
        .placeholder=${0}
        .value=${0}
        .getItems=${0}
        .getAdditionalItems=${0}
        .valueRenderer=${0}
        @value-changed=${0}
      >
      </ha-generic-picker>
    `),this.hass,this.autofocus,this.label,this.helper,this.hass.localize("ui.components.area-picker.no_match"),t,this.value,this._getItems,this._getAdditionalItems,i,this._valueChanged)}_valueChanged(e){e.stopPropagation();const t=e.detail.value;if(t)if(t.startsWith(L)){this.hass.loadFragmentTranslation("config");const e=t.substring(L.length);(0,b.E)(this,{suggestedName:e,createEntry:async e=>{try{const t=await(0,p.Lo)(this.hass,e);this._setValue(t.area_id)}catch(t){(0,v.Ys)(this,{title:this.hass.localize("ui.components.area-picker.failed_create_area"),text:t.message})}}})}else this._setValue(t);else this._setValue(void 0)}_setValue(e){this.value=e,(0,n.B)(this,"value-changed",{value:e}),(0,n.B)(this,"change")}constructor(...e){super(...e),this.noAdd=!1,this.disabled=!1,this.required=!1,this._computeValueRenderer=(0,s.Z)((e=>e=>{const t=this.hass.areas[e];if(!t)return(0,a.dy)(y||(y=C`
            <ha-svg-icon slot="start" .path=${0}></ha-svg-icon>
            <span slot="headline">${0}</span>
          `),V,t);const{floor:i}=(0,h.C)(t,this.hass),o=t?(0,l.D)(t):void 0,r=i?(0,c.r)(i):void 0,s=t.icon;return(0,a.dy)(f||(f=C`
          ${0}
          <span slot="headline">${0}</span>
          ${0}
        `),s?(0,a.dy)(x||(x=C`<ha-icon slot="start" .icon=${0}></ha-icon>`),s):(0,a.dy)($||($=C`<ha-svg-icon
                slot="start"
                .path=${0}
              ></ha-svg-icon>`),V),o,r?(0,a.dy)(w||(w=C`<span slot="supporting-text">${0}</span>`),r):a.Ld)})),this._getAreas=(0,s.Z)(((e,t,i,o,a,r,s,n,p)=>{let v,b,_={};const g=Object.values(e),m=Object.values(t),y=Object.values(i);(o||a||r||s||n)&&(_=(0,u.R6)(y),v=m,b=y.filter((e=>e.area_id)),o&&(v=v.filter((e=>{const t=_[e.id];return!(!t||!t.length)&&_[e.id].some((e=>o.includes((0,d.M)(e.entity_id))))})),b=b.filter((e=>o.includes((0,d.M)(e.entity_id))))),a&&(v=v.filter((e=>{const t=_[e.id];return!t||!t.length||y.every((e=>!a.includes((0,d.M)(e.entity_id))))})),b=b.filter((e=>!a.includes((0,d.M)(e.entity_id))))),r&&(v=v.filter((e=>{const t=_[e.id];return!(!t||!t.length)&&_[e.id].some((e=>{const t=this.hass.states[e.entity_id];return!!t&&(t.attributes.device_class&&r.includes(t.attributes.device_class))}))})),b=b.filter((e=>{const t=this.hass.states[e.entity_id];return t.attributes.device_class&&r.includes(t.attributes.device_class)}))),s&&(v=v.filter((e=>s(e)))),n&&(v=v.filter((e=>{const t=_[e.id];return!(!t||!t.length)&&_[e.id].some((e=>{const t=this.hass.states[e.entity_id];return!!t&&n(t)}))})),b=b.filter((e=>{const t=this.hass.states[e.entity_id];return!!t&&n(t)}))));let f,x=g;v&&(f=v.filter((e=>e.area_id)).map((e=>e.area_id))),b&&(f=(null!=f?f:[]).concat(b.filter((e=>e.area_id)).map((e=>e.area_id)))),f&&(x=x.filter((e=>f.includes(e.area_id)))),p&&(x=x.filter((e=>!p.includes(e.area_id))));return x.map((e=>{const{floor:t}=(0,h.C)(e,this.hass),i=t?(0,c.r)(t):void 0,o=(0,l.D)(e);return{id:e.area_id,primary:o||e.area_id,secondary:i,icon:e.icon||void 0,icon_path:e.icon?void 0:V,sorting_label:o,search_labels:[o,i,e.area_id,...e.aliases].filter((e=>Boolean(e)))}}))})),this._getItems=()=>this._getAreas(this.hass.areas,this.hass.devices,this.hass.entities,this.includeDomains,this.excludeDomains,this.includeDeviceClasses,this.deviceFilter,this.entityFilter,this.excludeAreas),this._allAreaNames=(0,s.Z)((e=>Object.values(e).map((e=>{var t;return null===(t=(0,l.D)(e))||void 0===t?void 0:t.toLowerCase()})).filter(Boolean))),this._getAdditionalItems=e=>{if(this.noAdd)return[];const t=this._allAreaNames(this.hass.areas);return e&&!t.includes(e.toLowerCase())?[{id:L+e,primary:this.hass.localize("ui.components.area-picker.add_new_sugestion",{name:e}),icon_path:k}]:[{id:L,primary:this.hass.localize("ui.components.area-picker.add_new"),icon_path:k}]}}}(0,o.__decorate)([(0,r.Cb)({attribute:!1})],S.prototype,"hass",void 0),(0,o.__decorate)([(0,r.Cb)()],S.prototype,"label",void 0),(0,o.__decorate)([(0,r.Cb)()],S.prototype,"value",void 0),(0,o.__decorate)([(0,r.Cb)()],S.prototype,"helper",void 0),(0,o.__decorate)([(0,r.Cb)()],S.prototype,"placeholder",void 0),(0,o.__decorate)([(0,r.Cb)({type:Boolean,attribute:"no-add"})],S.prototype,"noAdd",void 0),(0,o.__decorate)([(0,r.Cb)({type:Array,attribute:"include-domains"})],S.prototype,"includeDomains",void 0),(0,o.__decorate)([(0,r.Cb)({type:Array,attribute:"exclude-domains"})],S.prototype,"excludeDomains",void 0),(0,o.__decorate)([(0,r.Cb)({type:Array,attribute:"include-device-classes"})],S.prototype,"includeDeviceClasses",void 0),(0,o.__decorate)([(0,r.Cb)({type:Array,attribute:"exclude-areas"})],S.prototype,"excludeAreas",void 0),(0,o.__decorate)([(0,r.Cb)({attribute:!1})],S.prototype,"deviceFilter",void 0),(0,o.__decorate)([(0,r.Cb)({attribute:!1})],S.prototype,"entityFilter",void 0),(0,o.__decorate)([(0,r.Cb)({type:Boolean})],S.prototype,"disabled",void 0),(0,o.__decorate)([(0,r.Cb)({type:Boolean})],S.prototype,"required",void 0),(0,o.__decorate)([(0,r.IO)("ha-generic-picker")],S.prototype,"_picker",void 0),S=(0,o.__decorate)([(0,r.Mo)("ha-area-picker")],S),t()}catch(m){t(m)}}))},57264:function(e,t,i){i(26847),i(27530);var o=i(73742),a=i(59048),r=i(7616),s=i(78067);let n;class l extends s.t{constructor(...e){super(...e),this.borderTop=!1}}l.styles=[...s.C,(0,a.iv)(n||(n=(e=>e)`
      :host {
        --md-list-item-one-line-container-height: 48px;
        --md-list-item-two-line-container-height: 64px;
      }
      :host([border-top]) md-item {
        border-top: 1px solid var(--divider-color);
      }
      [slot="start"] {
        --state-icon-color: var(--secondary-text-color);
      }
      [slot="headline"] {
        line-height: var(--ha-line-height-normal);
        font-size: var(--ha-font-size-m);
        white-space: nowrap;
      }
      [slot="supporting-text"] {
        line-height: var(--ha-line-height-normal);
        font-size: var(--ha-font-size-s);
        white-space: nowrap;
      }
      ::slotted(state-badge),
      ::slotted(img) {
        width: 32px;
        height: 32px;
      }
      ::slotted(.code) {
        font-family: var(--ha-font-family-code);
        font-size: var(--ha-font-size-xs);
      }
      ::slotted(.domain) {
        font-size: var(--ha-font-size-s);
        font-weight: var(--ha-font-weight-normal);
        line-height: var(--ha-line-height-normal);
        align-self: flex-end;
        max-width: 30%;
        text-overflow: ellipsis;
        overflow: hidden;
        white-space: nowrap;
      }
    `))],(0,o.__decorate)([(0,r.Cb)({type:Boolean,reflect:!0,attribute:"border-top"})],l.prototype,"borderTop",void 0),l=(0,o.__decorate)([(0,r.Mo)("ha-combo-box-item")],l)},10471:function(e,t,i){i(26847),i(27530);var o=i(73742),a=i(7616),r=i(38573);class s extends r.f{willUpdate(e){super.willUpdate(e),e.has("value")&&this.disableSetValue&&(this.value=e.get("value"))}constructor(...e){super(...e),this.disableSetValue=!1}}(0,o.__decorate)([(0,a.Cb)({type:Boolean,attribute:"disable-set-value"})],s.prototype,"disableSetValue",void 0),s=(0,o.__decorate)([(0,a.Mo)("ha-combo-box-textfield")],s)},54693:function(e,t,i){i.a(e,(async function(e,t){try{i(26847),i(81738),i(22960),i(1455),i(27530);var o=i(73742),a=i(4816),r=i(5335),s=i(18464),n=i(59048),l=i(7616),d=i(25191),c=i(29740),h=(i(57264),i(10471),i(78645),i(42592),i(38573),e([r]));r=(h.then?(await h)():h)[0];let p,u,v,b,_,g,m,y=e=>e;const f="M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z",x="M7,10L12,15L17,10H7Z",$="M7,15L12,10L17,15H7Z";(0,s.hC)("vaadin-combo-box-item",(0,n.iv)(p||(p=y`
    :host {
      padding: 0 !important;
    }
    :host([focused]:not([disabled])) {
      background-color: rgba(var(--rgb-primary-text-color, 0, 0, 0), 0.12);
    }
    :host([selected]:not([disabled])) {
      background-color: transparent;
      color: var(--mdc-theme-primary);
      --mdc-ripple-color: var(--mdc-theme-primary);
      --mdc-theme-text-primary-on-background: var(--mdc-theme-primary);
    }
    :host([selected]:not([disabled])):before {
      background-color: var(--mdc-theme-primary);
      opacity: 0.12;
      content: "";
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
    }
    :host([selected][focused]:not([disabled])):before {
      opacity: 0.24;
    }
    :host(:hover:not([disabled])) {
      background-color: transparent;
    }
    [part="content"] {
      width: 100%;
    }
    [part="checkmark"] {
      display: none;
    }
  `)));class w extends n.oi{async open(){var e;await this.updateComplete,null===(e=this._comboBox)||void 0===e||e.open()}async focus(){var e,t;await this.updateComplete,await(null===(e=this._inputElement)||void 0===e?void 0:e.updateComplete),null===(t=this._inputElement)||void 0===t||t.focus()}disconnectedCallback(){super.disconnectedCallback(),this._overlayMutationObserver&&(this._overlayMutationObserver.disconnect(),this._overlayMutationObserver=void 0),this._bodyMutationObserver&&(this._bodyMutationObserver.disconnect(),this._bodyMutationObserver=void 0)}get selectedItem(){return this._comboBox.selectedItem}setInputValue(e){this._comboBox.value=e}setTextFieldValue(e){this._inputElement.value=e}render(){var e;return(0,n.dy)(u||(u=y`
      <!-- @ts-ignore Tag definition is not included in theme folder -->
      <vaadin-combo-box-light
        .itemValuePath=${0}
        .itemIdPath=${0}
        .itemLabelPath=${0}
        .items=${0}
        .value=${0}
        .filteredItems=${0}
        .dataProvider=${0}
        .allowCustomValue=${0}
        .disabled=${0}
        .required=${0}
        ${0}
        @opened-changed=${0}
        @filter-changed=${0}
        @value-changed=${0}
        attr-for-value="value"
      >
        <ha-combo-box-textfield
          label=${0}
          placeholder=${0}
          ?disabled=${0}
          ?required=${0}
          validationMessage=${0}
          .errorMessage=${0}
          class="input"
          autocapitalize="none"
          autocomplete="off"
          autocorrect="off"
          input-spellcheck="false"
          .suffix=${0}
          .icon=${0}
          .invalid=${0}
          .disableSetValue=${0}
        >
          <slot name="icon" slot="leadingIcon"></slot>
        </ha-combo-box-textfield>
        ${0}
        <ha-svg-icon
          role="button"
          tabindex="-1"
          aria-label=${0}
          aria-expanded=${0}
          class=${0}
          .path=${0}
          ?disabled=${0}
          @click=${0}
        ></ha-svg-icon>
      </vaadin-combo-box-light>
      ${0}
    `),this.itemValuePath,this.itemIdPath,this.itemLabelPath,this.items,this.value||"",this.filteredItems,this.dataProvider,this.allowCustomValue,this.disabled,this.required,(0,a.t)(this.renderer||this._defaultRowRenderer),this._openedChanged,this._filterChanged,this._valueChanged,(0,d.o)(this.label),(0,d.o)(this.placeholder),this.disabled,this.required,(0,d.o)(this.validationMessage),this.errorMessage,(0,n.dy)(v||(v=y`<div
            style="width: 28px;"
            role="none presentation"
          ></div>`)),this.icon,this.invalid,this._disableSetValue,this.value&&!this.hideClearIcon?(0,n.dy)(b||(b=y`<ha-svg-icon
              role="button"
              tabindex="-1"
              aria-label=${0}
              class=${0}
              .path=${0}
              @click=${0}
            ></ha-svg-icon>`),(0,d.o)(null===(e=this.hass)||void 0===e?void 0:e.localize("ui.common.clear")),"clear-button "+(this.label?"":"no-label"),f,this._clearValue):"",(0,d.o)(this.label),this.opened?"true":"false","toggle-button "+(this.label?"":"no-label"),this.opened?$:x,this.disabled,this._toggleOpen,this._renderHelper())}_renderHelper(){return this.helper?(0,n.dy)(_||(_=y`<ha-input-helper-text .disabled=${0}
          >${0}</ha-input-helper-text
        >`),this.disabled,this.helper):""}_clearValue(e){e.stopPropagation(),(0,c.B)(this,"value-changed",{value:void 0})}_toggleOpen(e){var t,i;this.opened?(null===(t=this._comboBox)||void 0===t||t.close(),e.stopPropagation()):null===(i=this._comboBox)||void 0===i||i.inputElement.focus()}_openedChanged(e){e.stopPropagation();const t=e.detail.value;if(setTimeout((()=>{this.opened=t,(0,c.B)(this,"opened-changed",{value:e.detail.value})}),0),this.clearInitialValue&&(this.setTextFieldValue(""),t?setTimeout((()=>{this._disableSetValue=!1}),100):this._disableSetValue=!0),t){const e=document.querySelector("vaadin-combo-box-overlay");e&&this._removeInert(e),this._observeBody()}else{var i;null===(i=this._bodyMutationObserver)||void 0===i||i.disconnect(),this._bodyMutationObserver=void 0}}_observeBody(){"MutationObserver"in window&&!this._bodyMutationObserver&&(this._bodyMutationObserver=new MutationObserver((e=>{e.forEach((e=>{e.addedNodes.forEach((e=>{"VAADIN-COMBO-BOX-OVERLAY"===e.nodeName&&this._removeInert(e)})),e.removedNodes.forEach((e=>{var t;"VAADIN-COMBO-BOX-OVERLAY"===e.nodeName&&(null===(t=this._overlayMutationObserver)||void 0===t||t.disconnect(),this._overlayMutationObserver=void 0)}))}))})),this._bodyMutationObserver.observe(document.body,{childList:!0}))}_removeInert(e){var t;if(e.inert)return e.inert=!1,null===(t=this._overlayMutationObserver)||void 0===t||t.disconnect(),void(this._overlayMutationObserver=void 0);"MutationObserver"in window&&!this._overlayMutationObserver&&(this._overlayMutationObserver=new MutationObserver((e=>{e.forEach((e=>{if("inert"===e.attributeName){const i=e.target;var t;if(i.inert)null===(t=this._overlayMutationObserver)||void 0===t||t.disconnect(),this._overlayMutationObserver=void 0,i.inert=!1}}))})),this._overlayMutationObserver.observe(e,{attributes:!0}))}_filterChanged(e){e.stopPropagation(),(0,c.B)(this,"filter-changed",{value:e.detail.value})}_valueChanged(e){if(e.stopPropagation(),this.allowCustomValue||(this._comboBox._closeOnBlurIsPrevented=!0),!this.opened)return;const t=e.detail.value;t!==this.value&&(0,c.B)(this,"value-changed",{value:t||void 0})}constructor(...e){super(...e),this.invalid=!1,this.icon=!1,this.allowCustomValue=!1,this.itemValuePath="value",this.itemLabelPath="label",this.disabled=!1,this.required=!1,this.opened=!1,this.hideClearIcon=!1,this.clearInitialValue=!1,this._disableSetValue=!1,this._defaultRowRenderer=e=>(0,n.dy)(g||(g=y`
    <ha-combo-box-item type="button">
      ${0}
    </ha-combo-box-item>
  `),this.itemLabelPath?e[this.itemLabelPath]:e)}}w.styles=(0,n.iv)(m||(m=y`
    :host {
      display: block;
      width: 100%;
    }
    vaadin-combo-box-light {
      position: relative;
    }
    ha-combo-box-textfield {
      width: 100%;
    }
    ha-combo-box-textfield > ha-icon-button {
      --mdc-icon-button-size: 24px;
      padding: 2px;
      color: var(--secondary-text-color);
    }
    ha-svg-icon {
      color: var(--input-dropdown-icon-color);
      position: absolute;
      cursor: pointer;
    }
    .toggle-button {
      right: 12px;
      top: -10px;
      inset-inline-start: initial;
      inset-inline-end: 12px;
      direction: var(--direction);
    }
    :host([opened]) .toggle-button {
      color: var(--primary-color);
    }
    .toggle-button[disabled] {
      color: var(--disabled-text-color);
      pointer-events: none;
    }
    .toggle-button.no-label {
      top: -3px;
    }
    .clear-button {
      --mdc-icon-size: 20px;
      top: -7px;
      right: 36px;
      inset-inline-start: initial;
      inset-inline-end: 36px;
      direction: var(--direction);
    }
    .clear-button.no-label {
      top: 0;
    }
    ha-input-helper-text {
      margin-top: 4px;
    }
  `)),(0,o.__decorate)([(0,l.Cb)({attribute:!1})],w.prototype,"hass",void 0),(0,o.__decorate)([(0,l.Cb)()],w.prototype,"label",void 0),(0,o.__decorate)([(0,l.Cb)()],w.prototype,"value",void 0),(0,o.__decorate)([(0,l.Cb)()],w.prototype,"placeholder",void 0),(0,o.__decorate)([(0,l.Cb)({attribute:!1})],w.prototype,"validationMessage",void 0),(0,o.__decorate)([(0,l.Cb)()],w.prototype,"helper",void 0),(0,o.__decorate)([(0,l.Cb)({attribute:"error-message"})],w.prototype,"errorMessage",void 0),(0,o.__decorate)([(0,l.Cb)({type:Boolean})],w.prototype,"invalid",void 0),(0,o.__decorate)([(0,l.Cb)({type:Boolean})],w.prototype,"icon",void 0),(0,o.__decorate)([(0,l.Cb)({attribute:!1})],w.prototype,"items",void 0),(0,o.__decorate)([(0,l.Cb)({attribute:!1})],w.prototype,"filteredItems",void 0),(0,o.__decorate)([(0,l.Cb)({attribute:!1})],w.prototype,"dataProvider",void 0),(0,o.__decorate)([(0,l.Cb)({attribute:"allow-custom-value",type:Boolean})],w.prototype,"allowCustomValue",void 0),(0,o.__decorate)([(0,l.Cb)({attribute:"item-value-path"})],w.prototype,"itemValuePath",void 0),(0,o.__decorate)([(0,l.Cb)({attribute:"item-label-path"})],w.prototype,"itemLabelPath",void 0),(0,o.__decorate)([(0,l.Cb)({attribute:"item-id-path"})],w.prototype,"itemIdPath",void 0),(0,o.__decorate)([(0,l.Cb)({attribute:!1})],w.prototype,"renderer",void 0),(0,o.__decorate)([(0,l.Cb)({type:Boolean})],w.prototype,"disabled",void 0),(0,o.__decorate)([(0,l.Cb)({type:Boolean})],w.prototype,"required",void 0),(0,o.__decorate)([(0,l.Cb)({type:Boolean,reflect:!0})],w.prototype,"opened",void 0),(0,o.__decorate)([(0,l.Cb)({type:Boolean,attribute:"hide-clear-icon"})],w.prototype,"hideClearIcon",void 0),(0,o.__decorate)([(0,l.Cb)({type:Boolean,attribute:"clear-initial-value"})],w.prototype,"clearInitialValue",void 0),(0,o.__decorate)([(0,l.IO)("vaadin-combo-box-light",!0)],w.prototype,"_comboBox",void 0),(0,o.__decorate)([(0,l.IO)("ha-combo-box-textfield",!0)],w.prototype,"_inputElement",void 0),(0,o.__decorate)([(0,l.SB)({type:Boolean})],w.prototype,"_disableSetValue",void 0),w=(0,o.__decorate)([(0,l.Mo)("ha-combo-box")],w),t()}catch(p){t(p)}}))},91577:function(e,t,i){i(26847),i(27530);var o=i(73742),a=i(59048),r=i(7616),s=i(31733),n=i(25191),l=i(88245),d=i(29740);i(3847),i(40830);let c,h,p,u,v,b=e=>e;class _ extends a.oi{_handleFocus(e){if(!this.disabled&&this.options&&e.target===e.currentTarget){const e=null!=this.value?this.options.findIndex((e=>e.value===this.value)):-1,t=-1!==e?e:0;this._focusOption(t)}}_focusOption(e){this._activeIndex=e,this.requestUpdate(),this.updateComplete.then((()=>{var t;const i=null===(t=this.shadowRoot)||void 0===t?void 0:t.querySelector(`#option-${this.options[e].value}`);null==i||i.focus()}))}_handleBlur(e){this.contains(e.relatedTarget)||(this._activeIndex=void 0)}_handleKeydown(e){var t;if(!this.options||this.disabled)return;let i=null!==(t=this._activeIndex)&&void 0!==t?t:0;switch(e.key){case" ":case"Enter":if(null!=this._activeIndex){const e=this.options[this._activeIndex].value;this.value=e,(0,d.B)(this,"value-changed",{value:e})}break;case"ArrowUp":case"ArrowLeft":i=i<=0?this.options.length-1:i-1,this._focusOption(i);break;case"ArrowDown":case"ArrowRight":i=(i+1)%this.options.length,this._focusOption(i);break;default:return}e.preventDefault()}_handleOptionClick(e){if(this.disabled)return;const t=e.target.value;this.value=t,(0,d.B)(this,"value-changed",{value:t})}_handleOptionMouseDown(e){var t;if(this.disabled)return;e.preventDefault();const i=e.target.value;this._activeIndex=null===(t=this.options)||void 0===t?void 0:t.findIndex((e=>e.value===i))}_handleOptionMouseUp(e){e.preventDefault()}_handleOptionFocus(e){var t;if(this.disabled)return;const i=e.target.value;this._activeIndex=null===(t=this.options)||void 0===t?void 0:t.findIndex((e=>e.value===i))}render(){return(0,a.dy)(c||(c=b`
      <div
        class="container"
        role="radiogroup"
        aria-label=${0}
        @focus=${0}
        @blur=${0}
        @keydown=${0}
        ?disabled=${0}
      >
        ${0}
      </div>
    `),(0,n.o)(this.label),this._handleFocus,this._handleBlur,this._handleKeydown,this.disabled,this.options?(0,l.r)(this.options,(e=>e.value),(e=>this._renderOption(e))):a.Ld)}_renderOption(e){const t=this.value===e.value;return(0,a.dy)(h||(h=b`
      <div
        id=${0}
        class=${0}
        role="radio"
        tabindex=${0}
        .value=${0}
        aria-checked=${0}
        aria-label=${0}
        title=${0}
        @click=${0}
        @focus=${0}
        @mousedown=${0}
        @mouseup=${0}
      >
        <div class="content">
          ${0}
          ${0}
        </div>
      </div>
    `),`option-${e.value}`,(0,s.$)({option:!0,selected:t}),t?"0":"-1",e.value,t?"true":"false",(0,n.o)(e.label),(0,n.o)(e.label),this._handleOptionClick,this._handleOptionFocus,this._handleOptionMouseDown,this._handleOptionMouseUp,e.path?(0,a.dy)(p||(p=b`<ha-svg-icon .path=${0}></ha-svg-icon>`),e.path):e.icon||a.Ld,e.label&&!this.hideOptionLabel?(0,a.dy)(u||(u=b`<span>${0}</span>`),e.label):a.Ld)}constructor(...e){super(...e),this.disabled=!1,this.vertical=!1,this.hideOptionLabel=!1}}_.styles=(0,a.iv)(v||(v=b`
    :host {
      display: block;
      --control-select-color: var(--primary-color);
      --control-select-focused-opacity: 0.2;
      --control-select-selected-opacity: 1;
      --control-select-background: var(--disabled-color);
      --control-select-background-opacity: 0.2;
      --control-select-thickness: 40px;
      --control-select-border-radius: 10px;
      --control-select-padding: 4px;
      --control-select-button-border-radius: calc(
        var(--control-select-border-radius) - var(--control-select-padding)
      );
      --mdc-icon-size: 20px;
      height: var(--control-select-thickness);
      width: 100%;
      font-style: normal;
      font-weight: var(--ha-font-weight-medium);
      color: var(--primary-text-color);
      user-select: none;
      -webkit-tap-highlight-color: transparent;
    }
    :host([vertical]) {
      width: var(--control-select-thickness);
      height: 100%;
    }
    .container {
      position: relative;
      height: 100%;
      width: 100%;
      border-radius: var(--control-select-border-radius);
      transform: translateZ(0);
      display: flex;
      flex-direction: row;
      padding: var(--control-select-padding);
      box-sizing: border-box;
      outline: none;
      transition: box-shadow 180ms ease-in-out;
    }
    .container::before {
      position: absolute;
      content: "";
      top: 0;
      left: 0;
      height: 100%;
      width: 100%;
      background: var(--control-select-background);
      opacity: var(--control-select-background-opacity);
      border-radius: var(--control-select-border-radius);
    }

    .container > *:not(:last-child) {
      margin-right: var(--control-select-padding);
      margin-inline-end: var(--control-select-padding);
      margin-inline-start: initial;
      direction: var(--direction);
    }
    .container[disabled] {
      --control-select-color: var(--disabled-color);
      --control-select-focused-opacity: 0;
      color: var(--disabled-color);
    }

    .container[disabled] .option {
      cursor: not-allowed;
    }

    .option {
      cursor: pointer;
      position: relative;
      flex: 1;
      height: 100%;
      width: 100%;
      display: flex;
      align-items: center;
      justify-content: center;
      border-radius: var(--control-select-button-border-radius);
      /* For safari border-radius overflow */
      z-index: 0;
      outline: none;
      transition: box-shadow 180ms ease-in-out;
    }
    .option:focus-visible {
      box-shadow: 0 0 0 2px var(--control-select-color);
    }
    .content > *:not(:last-child) {
      margin-bottom: 4px;
    }
    .option::before {
      position: absolute;
      content: "";
      top: 0;
      left: 0;
      height: 100%;
      width: 100%;
      background-color: var(--control-select-color);
      opacity: 0;
      border-radius: var(--control-select-button-border-radius);
      transition:
        background-color ease-in-out 180ms,
        opacity ease-in-out 80ms;
    }
    .option:hover::before {
      opacity: var(--control-select-focused-opacity);
    }
    .option.selected {
      color: white;
    }
    .option.selected::before {
      opacity: var(--control-select-selected-opacity);
    }
    .option .content {
      position: relative;
      pointer-events: none;
      display: flex;
      align-items: center;
      justify-content: center;
      flex-direction: column;
      text-align: center;
      padding: 2px;
      width: 100%;
      box-sizing: border-box;
    }
    .option .content span {
      display: block;
      width: 100%;
      -webkit-hyphens: auto;
      -moz-hyphens: auto;
      hyphens: auto;
    }
    :host([vertical]) {
      width: var(--control-select-thickness);
      height: auto;
    }
    :host([vertical]) .container {
      flex-direction: column;
    }
    :host([vertical]) .container > *:not(:last-child) {
      margin-right: initial;
      margin-inline-end: initial;
      margin-bottom: var(--control-select-padding);
    }
  `)),(0,o.__decorate)([(0,r.Cb)({type:Boolean})],_.prototype,"disabled",void 0),(0,o.__decorate)([(0,r.Cb)({attribute:!1})],_.prototype,"options",void 0),(0,o.__decorate)([(0,r.Cb)()],_.prototype,"value",void 0),(0,o.__decorate)([(0,r.Cb)({type:Boolean,reflect:!0})],_.prototype,"vertical",void 0),(0,o.__decorate)([(0,r.Cb)({type:Boolean,attribute:"hide-option-label"})],_.prototype,"hideOptionLabel",void 0),(0,o.__decorate)([(0,r.Cb)({type:String})],_.prototype,"label",void 0),(0,o.__decorate)([(0,r.SB)()],_.prototype,"_activeIndex",void 0),_=(0,o.__decorate)([(0,r.Mo)("ha-control-select")],_)},74207:function(e,t,i){i(26847),i(27530);var o=i(73742),a=i(3416),r=i(24196),s=i(59048),n=i(7616),l=i(31733),d=i(29740);let c,h,p=e=>e;class u extends a.a{render(){const e={"mdc-form-field--align-end":this.alignEnd,"mdc-form-field--space-between":this.spaceBetween,"mdc-form-field--nowrap":this.nowrap};return(0,s.dy)(c||(c=p` <div class="mdc-form-field ${0}">
      <slot></slot>
      <label class="mdc-label" @click=${0}>
        <slot name="label">${0}</slot>
      </label>
    </div>`),(0,l.$)(e),this._labelClick,this.label)}_labelClick(){const e=this.input;if(e&&(e.focus(),!e.disabled))switch(e.tagName){case"HA-CHECKBOX":e.checked=!e.checked,(0,d.B)(e,"change");break;case"HA-RADIO":e.checked=!0,(0,d.B)(e,"change");break;default:e.click()}}constructor(...e){super(...e),this.disabled=!1}}u.styles=[r.W,(0,s.iv)(h||(h=p`
      :host(:not([alignEnd])) ::slotted(ha-switch) {
        margin-right: 10px;
        margin-inline-end: 10px;
        margin-inline-start: inline;
      }
      .mdc-form-field {
        align-items: var(--ha-formfield-align-items, center);
        gap: 4px;
      }
      .mdc-form-field > label {
        direction: var(--direction);
        margin-inline-start: 0;
        margin-inline-end: auto;
        padding: 0;
      }
      :host([disabled]) label {
        color: var(--disabled-text-color);
      }
    `))],(0,o.__decorate)([(0,n.Cb)({type:Boolean,reflect:!0})],u.prototype,"disabled",void 0),u=(0,o.__decorate)([(0,n.Mo)("ha-formfield")],u)},33321:function(e,t,i){i.a(e,(async function(e,t){try{i(26847),i(1455),i(27530);var o=i(73742),a=i(59048),r=i(7616),s=i(25191),n=i(29740),l=(i(57264),i(78645),i(42592),i(64149)),d=(i(54164),i(40830),e([l]));l=(d.then?(await d)():d)[0];let c,h,p,u,v,b,_=e=>e;class g extends a.oi{render(){var e;return(0,a.dy)(c||(c=_`
      ${0}
      <div class="container">
        ${0}
      </div>
      ${0}
    `),this.label?(0,a.dy)(h||(h=_`<label ?disabled=${0}>${0}</label>`),this.disabled,this.label):a.Ld,this._opened?(0,a.dy)(u||(u=_`
              <ha-picker-combo-box
                .hass=${0}
                .autofocus=${0}
                .allowCustomValue=${0}
                .label=${0}
                .value=${0}
                hide-clear-icon
                @opened-changed=${0}
                @value-changed=${0}
                .rowRenderer=${0}
                .notFoundLabel=${0}
                .getItems=${0}
                .getAdditionalItems=${0}
                .searchFn=${0}
              ></ha-picker-combo-box>
            `),this.hass,this.autofocus,this.allowCustomValue,null!==(e=this.searchLabel)&&void 0!==e?e:this.hass.localize("ui.common.search"),this.value,this._openedChanged,this._valueChanged,this.rowRenderer,this.notFoundLabel,this.getItems,this.getAdditionalItems,this.searchFn):(0,a.dy)(p||(p=_`
              <ha-picker-field
                type="button"
                compact
                aria-label=${0}
                @click=${0}
                @clear=${0}
                .placeholder=${0}
                .value=${0}
                .required=${0}
                .disabled=${0}
                .hideClearIcon=${0}
                .valueRenderer=${0}
              >
              </ha-picker-field>
            `),(0,s.o)(this.label),this.open,this._clear,this.placeholder,this.value,this.required,this.disabled,this.hideClearIcon,this.valueRenderer),this._renderHelper())}_renderHelper(){return this.helper?(0,a.dy)(v||(v=_`<ha-input-helper-text .disabled=${0}
          >${0}</ha-input-helper-text
        >`),this.disabled,this.helper):a.Ld}_valueChanged(e){e.stopPropagation();const t=e.detail.value;t&&(0,n.B)(this,"value-changed",{value:t})}_clear(e){e.stopPropagation(),this._setValue(void 0)}_setValue(e){this.value=e,(0,n.B)(this,"value-changed",{value:e})}async open(){var e,t;this.disabled||(this._opened=!0,await this.updateComplete,null===(e=this._comboBox)||void 0===e||e.focus(),null===(t=this._comboBox)||void 0===t||t.open())}async _openedChanged(e){const t=e.detail.value;var i;this._opened&&!t&&(this._opened=!1,await this.updateComplete,null===(i=this._field)||void 0===i||i.focus())}static get styles(){return[(0,a.iv)(b||(b=_`
        .container {
          position: relative;
          display: block;
        }
        label[disabled] {
          color: var(--mdc-text-field-disabled-ink-color, rgba(0, 0, 0, 0.6));
        }
        label {
          display: block;
          margin: 0 0 8px;
        }
        ha-input-helper-text {
          display: block;
          margin: 8px 0 0;
        }
      `))]}constructor(...e){super(...e),this.autofocus=!1,this.disabled=!1,this.required=!1,this.hideClearIcon=!1,this._opened=!1}}(0,o.__decorate)([(0,r.Cb)({attribute:!1})],g.prototype,"hass",void 0),(0,o.__decorate)([(0,r.Cb)({type:Boolean})],g.prototype,"autofocus",void 0),(0,o.__decorate)([(0,r.Cb)({type:Boolean})],g.prototype,"disabled",void 0),(0,o.__decorate)([(0,r.Cb)({type:Boolean})],g.prototype,"required",void 0),(0,o.__decorate)([(0,r.Cb)({type:Boolean,attribute:"allow-custom-value"})],g.prototype,"allowCustomValue",void 0),(0,o.__decorate)([(0,r.Cb)()],g.prototype,"label",void 0),(0,o.__decorate)([(0,r.Cb)()],g.prototype,"value",void 0),(0,o.__decorate)([(0,r.Cb)()],g.prototype,"helper",void 0),(0,o.__decorate)([(0,r.Cb)()],g.prototype,"placeholder",void 0),(0,o.__decorate)([(0,r.Cb)({type:String,attribute:"search-label"})],g.prototype,"searchLabel",void 0),(0,o.__decorate)([(0,r.Cb)({attribute:"hide-clear-icon",type:Boolean})],g.prototype,"hideClearIcon",void 0),(0,o.__decorate)([(0,r.Cb)({attribute:!1,type:Array})],g.prototype,"getItems",void 0),(0,o.__decorate)([(0,r.Cb)({attribute:!1,type:Array})],g.prototype,"getAdditionalItems",void 0),(0,o.__decorate)([(0,r.Cb)({attribute:!1})],g.prototype,"rowRenderer",void 0),(0,o.__decorate)([(0,r.Cb)({attribute:!1})],g.prototype,"valueRenderer",void 0),(0,o.__decorate)([(0,r.Cb)({attribute:!1})],g.prototype,"searchFn",void 0),(0,o.__decorate)([(0,r.Cb)({attribute:"not-found-label",type:String})],g.prototype,"notFoundLabel",void 0),(0,o.__decorate)([(0,r.IO)("ha-picker-field")],g.prototype,"_field",void 0),(0,o.__decorate)([(0,r.IO)("ha-picker-combo-box")],g.prototype,"_comboBox",void 0),(0,o.__decorate)([(0,r.SB)()],g.prototype,"_opened",void 0),g=(0,o.__decorate)([(0,r.Mo)("ha-generic-picker")],g),t()}catch(c){t(c)}}))},64218:function(e,t,i){i.r(t),i.d(t,{HaIconButtonArrowPrev:function(){return d}});i(26847),i(27530);var o=i(73742),a=i(59048),r=i(7616),s=i(51597);i(78645);let n,l=e=>e;class d extends a.oi{render(){var e;return(0,a.dy)(n||(n=l`
      <ha-icon-button
        .disabled=${0}
        .label=${0}
        .path=${0}
      ></ha-icon-button>
    `),this.disabled,this.label||(null===(e=this.hass)||void 0===e?void 0:e.localize("ui.common.back"))||"Back",this._icon)}constructor(...e){super(...e),this.disabled=!1,this._icon="rtl"===s.E.document.dir?"M4,11V13H16L10.5,18.5L11.92,19.92L19.84,12L11.92,4.08L10.5,5.5L16,11H4Z":"M20,11V13H8L13.5,18.5L12.08,19.92L4.16,12L12.08,4.08L13.5,5.5L8,11H20Z"}}(0,o.__decorate)([(0,r.Cb)({attribute:!1})],d.prototype,"hass",void 0),(0,o.__decorate)([(0,r.Cb)({type:Boolean})],d.prototype,"disabled",void 0),(0,o.__decorate)([(0,r.Cb)()],d.prototype,"label",void 0),(0,o.__decorate)([(0,r.SB)()],d.prototype,"_icon",void 0),d=(0,o.__decorate)([(0,r.Mo)("ha-icon-button-arrow-prev")],d)},78645:function(e,t,i){i.r(t),i.d(t,{HaIconButton:function(){return p}});i(26847),i(27530);var o=i(73742),a=(i(1023),i(59048)),r=i(7616),s=i(25191);i(40830);let n,l,d,c,h=e=>e;class p extends a.oi{focus(){var e;null===(e=this._button)||void 0===e||e.focus()}render(){return(0,a.dy)(n||(n=h`
      <mwc-icon-button
        aria-label=${0}
        title=${0}
        aria-haspopup=${0}
        .disabled=${0}
      >
        ${0}
      </mwc-icon-button>
    `),(0,s.o)(this.label),(0,s.o)(this.hideTitle?void 0:this.label),(0,s.o)(this.ariaHasPopup),this.disabled,this.path?(0,a.dy)(l||(l=h`<ha-svg-icon .path=${0}></ha-svg-icon>`),this.path):(0,a.dy)(d||(d=h`<slot></slot>`)))}constructor(...e){super(...e),this.disabled=!1,this.hideTitle=!1}}p.shadowRootOptions={mode:"open",delegatesFocus:!0},p.styles=(0,a.iv)(c||(c=h`
    :host {
      display: inline-block;
      outline: none;
    }
    :host([disabled]) {
      pointer-events: none;
    }
    mwc-icon-button {
      --mdc-theme-on-primary: currentColor;
      --mdc-theme-text-disabled-on-light: var(--disabled-text-color);
    }
  `)),(0,o.__decorate)([(0,r.Cb)({type:Boolean,reflect:!0})],p.prototype,"disabled",void 0),(0,o.__decorate)([(0,r.Cb)({type:String})],p.prototype,"path",void 0),(0,o.__decorate)([(0,r.Cb)({type:String})],p.prototype,"label",void 0),(0,o.__decorate)([(0,r.Cb)({type:String,attribute:"aria-haspopup"})],p.prototype,"ariaHasPopup",void 0),(0,o.__decorate)([(0,r.Cb)({attribute:"hide-title",type:Boolean})],p.prototype,"hideTitle",void 0),(0,o.__decorate)([(0,r.IO)("mwc-icon-button",!0)],p.prototype,"_button",void 0),p=(0,o.__decorate)([(0,r.Mo)("ha-icon-button")],p)},65266:function(e,t,i){i.r(t),i.d(t,{HaIconNext:function(){return n}});i(26847),i(27530);var o=i(73742),a=i(7616),r=i(51597),s=i(40830);class n extends s.HaSvgIcon{constructor(...e){super(...e),this.path="rtl"===r.E.document.dir?"M15.41,16.58L10.83,12L15.41,7.41L14,6L8,12L14,18L15.41,16.58Z":"M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z"}}(0,o.__decorate)([(0,a.Cb)()],n.prototype,"path",void 0),n=(0,o.__decorate)([(0,a.Mo)("ha-icon-next")],n)},78067:function(e,t,i){i.d(t,{C:function(){return d},t:function(){return c}});var o=i(73742),a=i(74789),r=i(62693),s=i(59048),n=i(7616);let l;const d=[r.W,(0,s.iv)(l||(l=(e=>e)`
    :host {
      --ha-icon-display: block;
      --md-sys-color-primary: var(--primary-text-color);
      --md-sys-color-secondary: var(--secondary-text-color);
      --md-sys-color-surface: var(--card-background-color);
      --md-sys-color-on-surface: var(--primary-text-color);
      --md-sys-color-on-surface-variant: var(--secondary-text-color);
    }
    md-item {
      overflow: var(--md-item-overflow, hidden);
      align-items: var(--md-item-align-items, center);
      gap: var(--ha-md-list-item-gap, 16px);
    }
  `))];class c extends a.d{}c.styles=d,c=(0,o.__decorate)([(0,n.Mo)("ha-md-list-item")],c)},89429:function(e,t,i){var o=i(73742),a=i(10067),r=i(30187),s=i(59048),n=i(7616);let l;class d extends a.a{}d.styles=[r.W,(0,s.iv)(l||(l=(e=>e)`
      :host {
        --md-sys-color-surface: var(--card-background-color);
      }
    `))],d=(0,o.__decorate)([(0,n.Mo)("ha-md-list")],d)},38098:function(e,t,i){i(40777),i(26847),i(27530);var o=i(73742),a=i(59048),r=i(7616),s=i(29740);i(87799);class n{processMessage(e){if("removed"===e.type)for(const t of Object.keys(e.notifications))delete this.notifications[t];else this.notifications=Object.assign(Object.assign({},this.notifications),e.notifications);return Object.values(this.notifications)}constructor(){this.notifications={}}}i(78645);let l,d,c,h=e=>e;class p extends a.oi{connectedCallback(){super.connectedCallback(),this._attachNotifOnConnect&&(this._attachNotifOnConnect=!1,this._subscribeNotifications())}disconnectedCallback(){super.disconnectedCallback(),this._unsubNotifications&&(this._attachNotifOnConnect=!0,this._unsubNotifications(),this._unsubNotifications=void 0)}render(){if(!this._show)return a.Ld;const e=this._hasNotifications&&(this.narrow||"always_hidden"===this.hass.dockedSidebar);return(0,a.dy)(l||(l=h`
      <ha-icon-button
        .label=${0}
        .path=${0}
        @click=${0}
      ></ha-icon-button>
      ${0}
    `),this.hass.localize("ui.sidebar.sidebar_toggle"),"M3,6H21V8H3V6M3,11H21V13H3V11M3,16H21V18H3V16Z",this._toggleMenu,e?(0,a.dy)(d||(d=h`<div class="dot"></div>`)):"")}firstUpdated(e){super.firstUpdated(e),this.hassio&&(this._alwaysVisible=(Number(window.parent.frontendVersion)||0)<20190710)}willUpdate(e){if(super.willUpdate(e),!e.has("narrow")&&!e.has("hass"))return;const t=e.has("hass")?e.get("hass"):this.hass,i=(e.has("narrow")?e.get("narrow"):this.narrow)||"always_hidden"===(null==t?void 0:t.dockedSidebar),o=this.narrow||"always_hidden"===this.hass.dockedSidebar;this.hasUpdated&&i===o||(this._show=o||this._alwaysVisible,o?this._subscribeNotifications():this._unsubNotifications&&(this._unsubNotifications(),this._unsubNotifications=void 0))}_subscribeNotifications(){if(this._unsubNotifications)throw new Error("Already subscribed");this._unsubNotifications=((e,t)=>{const i=new n,o=e.subscribeMessage((e=>t(i.processMessage(e))),{type:"persistent_notification/subscribe"});return()=>{o.then((e=>null==e?void 0:e()))}})(this.hass.connection,(e=>{this._hasNotifications=e.length>0}))}_toggleMenu(){(0,s.B)(this,"hass-toggle-menu")}constructor(...e){super(...e),this.hassio=!1,this.narrow=!1,this._hasNotifications=!1,this._show=!1,this._alwaysVisible=!1,this._attachNotifOnConnect=!1}}p.styles=(0,a.iv)(c||(c=h`
    :host {
      position: relative;
    }
    .dot {
      pointer-events: none;
      position: absolute;
      background-color: var(--accent-color);
      width: 12px;
      height: 12px;
      top: 9px;
      right: 7px;
      inset-inline-end: 7px;
      inset-inline-start: initial;
      border-radius: 50%;
      border: 2px solid var(--app-header-background-color);
    }
  `)),(0,o.__decorate)([(0,r.Cb)({type:Boolean})],p.prototype,"hassio",void 0),(0,o.__decorate)([(0,r.Cb)({type:Boolean})],p.prototype,"narrow",void 0),(0,o.__decorate)([(0,r.Cb)({attribute:!1})],p.prototype,"hass",void 0),(0,o.__decorate)([(0,r.SB)()],p.prototype,"_hasNotifications",void 0),(0,o.__decorate)([(0,r.SB)()],p.prototype,"_show",void 0),p=(0,o.__decorate)([(0,r.Mo)("ha-menu-button")],p)},56884:function(e,t,i){i(84730),i(26847),i(81738),i(6989),i(26086),i(27530);var o=i(73742),a=i(59048),r=i(7616),s=i(25191);i(65266),i(40830),i(89429),i(78067);let n,l,d,c,h,p=e=>e;class u extends a.oi{render(){return(0,a.dy)(n||(n=p`
      <ha-md-list
        innerRole="menu"
        itemRoles="menuitem"
        innerAriaLabel=${0}
      >
        ${0}
      </ha-md-list>
    `),(0,s.o)(this.label),this.pages.map((e=>{const t=e.path.endsWith("#external-app-configuration");return(0,a.dy)(l||(l=p`
            <ha-md-list-item
              .type=${0}
              .href=${0}
              @click=${0}
            >
              <div
                slot="start"
                class=${0}
                .style="background-color: ${0}"
              >
                <ha-svg-icon .path=${0}></ha-svg-icon>
              </div>
              <span slot="headline">${0}</span>
              ${0}
              ${0}
            </ha-md-list-item>
          `),t?"button":"link",t?void 0:e.path,t?this._handleExternalApp:void 0,e.iconColor?"icon-background":"",e.iconColor||"undefined",e.iconPath,e.name,this.hasSecondary?(0,a.dy)(d||(d=p`<span slot="supporting-text">${0}</span>`),e.description):"",this.narrow?"":(0,a.dy)(c||(c=p`<ha-icon-next slot="end"></ha-icon-next>`)))})))}_handleExternalApp(){this.hass.auth.external.fireMessage({type:"config_screen/show"})}constructor(...e){super(...e),this.narrow=!1,this.hasSecondary=!1}}u.styles=(0,a.iv)(h||(h=p`
    ha-svg-icon,
    ha-icon-next {
      color: var(--secondary-text-color);
      height: 24px;
      width: 24px;
      display: block;
    }
    ha-svg-icon {
      padding: 8px;
    }
    .icon-background {
      border-radius: 50%;
    }
    .icon-background ha-svg-icon {
      color: #fff;
    }
    ha-md-list-item {
      font-size: var(--navigation-list-item-title-font-size);
    }
  `)),(0,o.__decorate)([(0,r.Cb)({attribute:!1})],u.prototype,"hass",void 0),(0,o.__decorate)([(0,r.Cb)({type:Boolean})],u.prototype,"narrow",void 0),(0,o.__decorate)([(0,r.Cb)({attribute:!1})],u.prototype,"pages",void 0),(0,o.__decorate)([(0,r.Cb)({attribute:"has-secondary",type:Boolean})],u.prototype,"hasSecondary",void 0),(0,o.__decorate)([(0,r.Cb)()],u.prototype,"label",void 0),u=(0,o.__decorate)([(0,r.Mo)("ha-navigation-list")],u)},64149:function(e,t,i){i.a(e,(async function(e,t){try{i(26847),i(2394),i(18574),i(81738),i(6989),i(87799),i(1455),i(20655),i(27530);var o=i(73742),a=i(39230),r=i(59048),s=i(7616),n=i(28105),l=i(29740),d=i(92949),c=i(93117),h=i(54693),p=(i(57264),i(3847),e([h]));h=(p.then?(await p)():p)[0];let u,v,b,_,g,m=e=>e;const y="M9.5,3A6.5,6.5 0 0,1 16,9.5C16,11.11 15.41,12.59 14.44,13.73L14.71,14H15.5L20.5,19L19,20.5L14,15.5V14.71L13.73,14.44C12.59,15.41 11.11,16 9.5,16A6.5,6.5 0 0,1 3,9.5A6.5,6.5 0 0,1 9.5,3M9.5,5C7,5 5,7 5,9.5C5,12 7,14 9.5,14C12,14 14,12 14,9.5C14,7 12,5 9.5,5Z",f="___no_matching_items_found___",x=e=>(0,r.dy)(u||(u=m`
  <ha-combo-box-item type="button" compact>
    ${0}
    <span slot="headline">${0}</span>
    ${0}
  </ha-combo-box-item>
`),e.icon?(0,r.dy)(v||(v=m`<ha-icon slot="start" .icon=${0}></ha-icon>`),e.icon):e.icon_path?(0,r.dy)(b||(b=m`<ha-svg-icon slot="start" .path=${0}></ha-svg-icon>`),e.icon_path):r.Ld,e.primary,e.secondary?(0,r.dy)(_||(_=m`<span slot="supporting-text">${0}</span>`),e.secondary):r.Ld);class $ extends r.oi{async open(){var e;await this.updateComplete,await(null===(e=this.comboBox)||void 0===e?void 0:e.open())}async focus(){var e;await this.updateComplete,await(null===(e=this.comboBox)||void 0===e?void 0:e.focus())}shouldUpdate(e){return!!(e.has("value")||e.has("label")||e.has("disabled"))||!(!e.has("_opened")&&this._opened)}willUpdate(e){e.has("_opened")&&this._opened&&(this._items=this._getItems(),this._initialItems&&(this.comboBox.filteredItems=this._items),this._initialItems=!0)}render(){return(0,r.dy)(g||(g=m`
      <ha-combo-box
        item-id-path="id"
        item-value-path="id"
        item-label-path="a11y_label"
        clear-initial-value
        .hass=${0}
        .value=${0}
        .label=${0}
        .helper=${0}
        .allowCustomValue=${0}
        .filteredItems=${0}
        .renderer=${0}
        .required=${0}
        .disabled=${0}
        .hideClearIcon=${0}
        @opened-changed=${0}
        @value-changed=${0}
        @filter-changed=${0}
      >
      </ha-combo-box>
    `),this.hass,this._value,this.label,this.helper,this.allowCustomValue,this._items,this.rowRenderer||x,this.required,this.disabled,this.hideClearIcon,this._openedChanged,this._valueChanged,this._filterChanged)}get _value(){return this.value||""}_openedChanged(e){e.stopPropagation(),e.detail.value!==this._opened&&(this._opened=e.detail.value,(0,l.B)(this,"opened-changed",{value:this._opened}))}_valueChanged(e){var t;e.stopPropagation(),this.comboBox.setTextFieldValue("");const i=null===(t=e.detail.value)||void 0===t?void 0:t.trim();i!==f&&i!==this._value&&this._setValue(i)}_filterChanged(e){if(!this._opened)return;const t=e.target,i=e.detail.value.trim(),o=this._fuseIndex(this._items),a=new c.J(this._items,{shouldSort:!1},o).multiTermsSearch(i);let r=this._items;if(a){const e=a.map((e=>e.item));0===e.length&&e.push(this._defaultNotFoundItem(this.notFoundLabel,this.hass.localize));const t=this._getAdditionalItems(i);e.push(...t),r=e}this.searchFn&&(r=this.searchFn(i,r,this._items)),t.filteredItems=r}_setValue(e){setTimeout((()=>{(0,l.B)(this,"value-changed",{value:e})}),0)}constructor(...e){super(...e),this.autofocus=!1,this.disabled=!1,this.required=!1,this.hideClearIcon=!1,this._opened=!1,this._initialItems=!1,this._items=[],this._defaultNotFoundItem=(0,n.Z)(((e,t)=>({id:f,primary:e||t("ui.components.combo-box.no_match"),icon_path:y,a11y_label:e||t("ui.components.combo-box.no_match")}))),this._getAdditionalItems=e=>{var t;return((null===(t=this.getAdditionalItems)||void 0===t?void 0:t.call(this,e))||[]).map((e=>Object.assign(Object.assign({},e),{},{a11y_label:e.a11y_label||e.primary})))},this._getItems=()=>{const e=(this.getItems?this.getItems():[]).map((e=>Object.assign(Object.assign({},e),{},{a11y_label:e.a11y_label||e.primary}))).sort(((e,t)=>(0,d.fe)(e.sorting_label,t.sorting_label,this.hass.locale.language)));e.length||e.push(this._defaultNotFoundItem(this.notFoundLabel,this.hass.localize));const t=this._getAdditionalItems();return e.push(...t),e},this._fuseIndex=(0,n.Z)((e=>a.Z.createIndex(["search_labels"],e)))}}(0,o.__decorate)([(0,s.Cb)({attribute:!1})],$.prototype,"hass",void 0),(0,o.__decorate)([(0,s.Cb)({type:Boolean})],$.prototype,"autofocus",void 0),(0,o.__decorate)([(0,s.Cb)({type:Boolean})],$.prototype,"disabled",void 0),(0,o.__decorate)([(0,s.Cb)({type:Boolean})],$.prototype,"required",void 0),(0,o.__decorate)([(0,s.Cb)({type:Boolean,attribute:"allow-custom-value"})],$.prototype,"allowCustomValue",void 0),(0,o.__decorate)([(0,s.Cb)()],$.prototype,"label",void 0),(0,o.__decorate)([(0,s.Cb)()],$.prototype,"value",void 0),(0,o.__decorate)([(0,s.Cb)()],$.prototype,"helper",void 0),(0,o.__decorate)([(0,s.Cb)({attribute:!1,type:Array})],$.prototype,"getItems",void 0),(0,o.__decorate)([(0,s.Cb)({attribute:!1,type:Array})],$.prototype,"getAdditionalItems",void 0),(0,o.__decorate)([(0,s.Cb)({attribute:!1})],$.prototype,"rowRenderer",void 0),(0,o.__decorate)([(0,s.Cb)({attribute:"hide-clear-icon",type:Boolean})],$.prototype,"hideClearIcon",void 0),(0,o.__decorate)([(0,s.Cb)({attribute:"not-found-label",type:String})],$.prototype,"notFoundLabel",void 0),(0,o.__decorate)([(0,s.Cb)({attribute:!1})],$.prototype,"searchFn",void 0),(0,o.__decorate)([(0,s.SB)()],$.prototype,"_opened",void 0),(0,o.__decorate)([(0,s.IO)("ha-combo-box",!0)],$.prototype,"comboBox",void 0),$=(0,o.__decorate)([(0,s.Mo)("ha-picker-combo-box")],$),t()}catch(u){t(u)}}))},54164:function(e,t,i){i(26847),i(1455),i(27530);var o=i(73742),a=i(59048),r=i(7616),s=i(29740);i(57264),i(78645);let n,l,d,c,h,p=e=>e;class u extends a.oi{async focus(){var e;await this.updateComplete,await(null===(e=this.item)||void 0===e?void 0:e.focus())}render(){const e=!(!this.value||this.required||this.disabled||this.hideClearIcon);return(0,a.dy)(n||(n=p`
      <ha-combo-box-item .disabled=${0} type="button" compact>
        ${0}
        ${0}
        <ha-svg-icon
          class="arrow"
          slot="end"
          .path=${0}
        ></ha-svg-icon>
      </ha-combo-box-item>
    `),this.disabled,this.value?this.valueRenderer?this.valueRenderer(this.value):(0,a.dy)(l||(l=p`<slot name="headline">${0}</slot>`),this.value):(0,a.dy)(d||(d=p`
              <span slot="headline" class="placeholder">
                ${0}
              </span>
            `),this.placeholder),e?(0,a.dy)(c||(c=p`
              <ha-icon-button
                class="clear"
                slot="end"
                @click=${0}
                .path=${0}
              ></ha-icon-button>
            `),this._clear,"M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z"):a.Ld,"M7,10L12,15L17,10H7Z")}_clear(e){e.stopPropagation(),(0,s.B)(this,"clear")}static get styles(){return[(0,a.iv)(h||(h=p`
        ha-combo-box-item[disabled] {
          background-color: var(
            --mdc-text-field-disabled-fill-color,
            whitesmoke
          );
        }
        ha-combo-box-item {
          background-color: var(--mdc-text-field-fill-color, whitesmoke);
          border-radius: 4px;
          border-end-end-radius: 0;
          border-end-start-radius: 0;
          --md-list-item-one-line-container-height: 56px;
          --md-list-item-two-line-container-height: 56px;
          --md-list-item-top-space: 0px;
          --md-list-item-bottom-space: 0px;
          --md-list-item-leading-space: 8px;
          --md-list-item-trailing-space: 8px;
          --ha-md-list-item-gap: 8px;
          /* Remove the default focus ring */
          --md-focus-ring-width: 0px;
          --md-focus-ring-duration: 0s;
        }

        /* Add Similar focus style as the text field */
        ha-combo-box-item[disabled]:after {
          background-color: var(
            --mdc-text-field-disabled-line-color,
            rgba(0, 0, 0, 0.42)
          );
        }
        ha-combo-box-item:after {
          display: block;
          content: "";
          position: absolute;
          pointer-events: none;
          bottom: 0;
          left: 0;
          right: 0;
          height: 1px;
          width: 100%;
          background-color: var(
            --mdc-text-field-idle-line-color,
            rgba(0, 0, 0, 0.42)
          );
          transform:
            height 180ms ease-in-out,
            background-color 180ms ease-in-out;
        }

        ha-combo-box-item:focus:after {
          height: 2px;
          background-color: var(--mdc-theme-primary);
        }

        .clear {
          margin: 0 -8px;
          --mdc-icon-button-size: 32px;
          --mdc-icon-size: 20px;
        }
        .arrow {
          --mdc-icon-size: 20px;
          width: 32px;
        }

        .placeholder {
          color: var(--secondary-text-color);
          padding: 0 8px;
        }
      `))]}constructor(...e){super(...e),this.disabled=!1,this.required=!1,this.hideClearIcon=!1}}(0,o.__decorate)([(0,r.Cb)({type:Boolean})],u.prototype,"disabled",void 0),(0,o.__decorate)([(0,r.Cb)({type:Boolean})],u.prototype,"required",void 0),(0,o.__decorate)([(0,r.Cb)()],u.prototype,"value",void 0),(0,o.__decorate)([(0,r.Cb)()],u.prototype,"helper",void 0),(0,o.__decorate)([(0,r.Cb)()],u.prototype,"placeholder",void 0),(0,o.__decorate)([(0,r.Cb)({attribute:"hide-clear-icon",type:Boolean})],u.prototype,"hideClearIcon",void 0),(0,o.__decorate)([(0,r.Cb)({attribute:!1})],u.prototype,"valueRenderer",void 0),(0,o.__decorate)([(0,r.IO)("ha-combo-box-item",!0)],u.prototype,"item",void 0),u=(0,o.__decorate)([(0,r.Mo)("ha-picker-field")],u)},71308:function(e,t,i){var o=i(73742),a=i(94626),r=i(89994),s=i(59048),n=i(7616);let l;class d extends a.J{}d.styles=[r.W,(0,s.iv)(l||(l=(e=>e)`
      :host {
        --mdc-theme-secondary: var(--primary-color);
      }
    `))],d=(0,o.__decorate)([(0,n.Mo)("ha-radio")],d)},77307:function(e,t,i){i(84730),i(26847),i(81738),i(6989),i(27530);var o=i(73742),a=i(7616),r=i(59048),s=(i(71308),i(31733)),n=i(20480),l=i(29740),d=i(80913),c=i(41806);let h,p,u,v,b,_=e=>e;class g extends r.oi{render(){var e;const t=null!==(e=this.maxColumns)&&void 0!==e?e:3,i=Math.min(t,this.options.length);return(0,r.dy)(h||(h=_`
      <div class="list" style=${0}>
        ${0}
      </div>
    `),(0,n.V)({"--columns":i}),this.options.map((e=>this._renderOption(e))))}_renderOption(e){var t;const i=1===this.maxColumns,o=e.disabled||this.disabled||!1,a=e.value===this.value,n=(null===(t=this.hass)||void 0===t?void 0:t.themes.darkMode)||!1,l=!!this.hass&&(0,d.HE)(this.hass),h="object"==typeof e.image?n&&e.image.src_dark||e.image.src:e.image,b="object"==typeof e.image&&(l&&e.image.flip_rtl);return(0,r.dy)(p||(p=_`
      <label
        class="option ${0}"
        ?disabled=${0}
        @click=${0}
      >
        <div class="content">
          <ha-radio
            .checked=${0}
            .value=${0}
            .disabled=${0}
            @change=${0}
            @click=${0}
          ></ha-radio>
          <div class="text">
            <span class="label">${0}</span>
            ${0}
          </div>
        </div>
        ${0}
      </label>
    `),(0,s.$)({horizontal:i,selected:a}),o,this._labelClick,e.value===this.value,e.value,o,this._radioChanged,c.U,e.label,e.description?(0,r.dy)(u||(u=_`<span class="description">${0}</span>`),e.description):r.Ld,h?(0,r.dy)(v||(v=_`
              <img class=${0} alt="" src=${0} />
            `),b?"flipped":"",h):r.Ld)}_labelClick(e){var t;e.stopPropagation(),null===(t=e.currentTarget.querySelector("ha-radio"))||void 0===t||t.click()}_radioChanged(e){var t;e.stopPropagation();const i=e.currentTarget.value;this.disabled||void 0===i||i===(null!==(t=this.value)&&void 0!==t?t:"")||(0,l.B)(this,"value-changed",{value:i})}constructor(...e){super(...e),this.options=[]}}g.styles=(0,r.iv)(b||(b=_`
    .list {
      display: grid;
      grid-template-columns: repeat(var(--columns, 1), minmax(0, 1fr));
      gap: 12px;
    }
    .option {
      position: relative;
      display: block;
      border: 1px solid var(--divider-color);
      border-radius: var(--ha-card-border-radius, 12px);
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: space-between;
      padding: 12px;
      gap: 8px;
      overflow: hidden;
      cursor: pointer;
    }

    .option .content {
      position: relative;
      display: flex;
      flex-direction: row;
      gap: 8px;
      min-width: 0;
      width: 100%;
    }
    .option .content ha-radio {
      margin: -12px;
      flex: none;
    }
    .option .content .text {
      display: flex;
      flex-direction: column;
      gap: 4px;
      min-width: 0;
      flex: 1;
    }
    .option .content .text .label {
      color: var(--primary-text-color);
      font-size: var(--ha-font-size-m);
      font-weight: var(--ha-font-weight-normal);
      line-height: var(--ha-line-height-condensed);
      overflow: hidden;
      white-space: nowrap;
      text-overflow: ellipsis;
    }
    .option .content .text .description {
      color: var(--secondary-text-color);
      font-size: var(--ha-font-size-s);
      font-weight: var(--ha-font-weight-normal);
      line-height: var(--ha-line-height-condensed);
    }
    img {
      position: relative;
      max-width: var(--ha-select-box-image-size, 96px);
      max-height: var(--ha-select-box-image-size, 96px);
      margin: auto;
    }

    .flipped {
      transform: scaleX(-1);
    }

    .option.horizontal {
      flex-direction: row;
      align-items: flex-start;
    }

    .option.horizontal img {
      margin: 0;
    }

    .option:before {
      content: "";
      display: block;
      inset: 0;
      position: absolute;
      background-color: transparent;
      pointer-events: none;
      opacity: 0.2;
      transition:
        background-color 180ms ease-in-out,
        opacity 180ms ease-in-out;
    }
    .option:hover:before {
      background-color: var(--divider-color);
    }
    .option.selected:before {
      background-color: var(--primary-color);
    }
    .option[disabled] {
      cursor: not-allowed;
    }
    .option[disabled] .content,
    .option[disabled] img {
      opacity: 0.5;
    }
    .option[disabled]:before {
      background-color: var(--disabled-color);
      opacity: 0.05;
    }
  `)),(0,o.__decorate)([(0,a.Cb)({attribute:!1})],g.prototype,"hass",void 0),(0,o.__decorate)([(0,a.Cb)({attribute:!1})],g.prototype,"options",void 0),(0,o.__decorate)([(0,a.Cb)({attribute:!1})],g.prototype,"value",void 0),(0,o.__decorate)([(0,a.Cb)({type:Boolean})],g.prototype,"disabled",void 0),(0,o.__decorate)([(0,a.Cb)({type:Number,attribute:"max_columns"})],g.prototype,"maxColumns",void 0),g=(0,o.__decorate)([(0,a.Mo)("ha-select-box")],g)},29490:function(e,t,i){i(26847),i(1455),i(27530);var o=i(73742),a=i(77740),r=i(32609),s=i(59048),n=i(7616),l=i(31733),d=i(16811),c=i(98012);i(78645),i(59462);let h,p,u,v,b,_=e=>e;class g extends a.K{render(){return(0,s.dy)(h||(h=_`
      ${0}
      ${0}
    `),super.render(),this.clearable&&!this.required&&!this.disabled&&this.value?(0,s.dy)(p||(p=_`<ha-icon-button
            label="clear"
            @click=${0}
            .path=${0}
          ></ha-icon-button>`),this._clearValue,"M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z"):s.Ld)}renderMenu(){const e=this.getMenuClasses();return(0,s.dy)(u||(u=_`<ha-menu
      innerRole="listbox"
      wrapFocus
      class=${0}
      activatable
      .fullwidth=${0}
      .open=${0}
      .anchor=${0}
      .fixed=${0}
      @selected=${0}
      @opened=${0}
      @closed=${0}
      @items-updated=${0}
      @keydown=${0}
    >
      ${0}
    </ha-menu>`),(0,l.$)(e),!this.fixedMenuPosition&&!this.naturalMenuWidth,this.menuOpen,this.anchorElement,this.fixedMenuPosition,this.onSelected,this.onOpened,this.onClosed,this.onItemsUpdated,this.handleTypeahead,this.renderMenuContent())}renderLeadingIcon(){return this.icon?(0,s.dy)(v||(v=_`<span class="mdc-select__icon"
      ><slot name="icon"></slot
    ></span>`)):s.Ld}connectedCallback(){super.connectedCallback(),window.addEventListener("translations-updated",this._translationsUpdated)}async firstUpdated(){var e;(super.firstUpdated(),this.inlineArrow)&&(null===(e=this.shadowRoot)||void 0===e||null===(e=e.querySelector(".mdc-select__selected-text-container"))||void 0===e||e.classList.add("inline-arrow"))}updated(e){if(super.updated(e),e.has("inlineArrow")){var t;const e=null===(t=this.shadowRoot)||void 0===t?void 0:t.querySelector(".mdc-select__selected-text-container");this.inlineArrow?null==e||e.classList.add("inline-arrow"):null==e||e.classList.remove("inline-arrow")}e.get("options")&&(this.layoutOptions(),this.selectByValue(this.value))}disconnectedCallback(){super.disconnectedCallback(),window.removeEventListener("translations-updated",this._translationsUpdated)}_clearValue(){!this.disabled&&this.value&&(this.valueSetDirectly=!0,this.select(-1),this.mdcFoundation.handleChange())}constructor(...e){super(...e),this.icon=!1,this.clearable=!1,this.inlineArrow=!1,this._translationsUpdated=(0,d.D)((async()=>{await(0,c.y)(),this.layoutOptions()}),500)}}g.styles=[r.W,(0,s.iv)(b||(b=_`
      :host([clearable]) {
        position: relative;
      }
      .mdc-select:not(.mdc-select--disabled) .mdc-select__icon {
        color: var(--secondary-text-color);
      }
      .mdc-select__anchor {
        width: var(--ha-select-min-width, 200px);
      }
      .mdc-select--filled .mdc-select__anchor {
        height: var(--ha-select-height, 56px);
      }
      .mdc-select--filled .mdc-floating-label {
        inset-inline-start: 12px;
        inset-inline-end: initial;
        direction: var(--direction);
      }
      .mdc-select--filled.mdc-select--with-leading-icon .mdc-floating-label {
        inset-inline-start: 48px;
        inset-inline-end: initial;
        direction: var(--direction);
      }
      .mdc-select .mdc-select__anchor {
        padding-inline-start: 12px;
        padding-inline-end: 0px;
        direction: var(--direction);
      }
      .mdc-select__anchor .mdc-floating-label--float-above {
        transform-origin: var(--float-start);
      }
      .mdc-select__selected-text-container {
        padding-inline-end: var(--select-selected-text-padding-end, 0px);
      }
      :host([clearable]) .mdc-select__selected-text-container {
        padding-inline-end: var(--select-selected-text-padding-end, 12px);
      }
      ha-icon-button {
        position: absolute;
        top: 10px;
        right: 28px;
        --mdc-icon-button-size: 36px;
        --mdc-icon-size: 20px;
        color: var(--secondary-text-color);
        inset-inline-start: initial;
        inset-inline-end: 28px;
        direction: var(--direction);
      }
      .inline-arrow {
        flex-grow: 0;
      }
    `))],(0,o.__decorate)([(0,n.Cb)({type:Boolean})],g.prototype,"icon",void 0),(0,o.__decorate)([(0,n.Cb)({type:Boolean,reflect:!0})],g.prototype,"clearable",void 0),(0,o.__decorate)([(0,n.Cb)({attribute:"inline-arrow",type:Boolean})],g.prototype,"inlineArrow",void 0),(0,o.__decorate)([(0,n.Cb)()],g.prototype,"options",void 0),g=(0,o.__decorate)([(0,n.Mo)("ha-select")],g)},69028:function(e,t,i){i.r(t),i.d(t,{HaNumberSelector:function(){return v}});i(26847),i(56303),i(27530);var o=i(73742),a=i(59048),r=i(7616),s=i(31733),n=i(29740);i(42592),i(57275),i(38573);let l,d,c,h,p,u=e=>e;class v extends a.oi{willUpdate(e){e.has("value")&&(""!==this._valueStr&&this.value===Number(this._valueStr)||(this._valueStr=null==this.value||isNaN(this.value)?"":this.value.toString()))}render(){var e,t,i,o,r,n,p,v,b,_,g,m,y,f,x;const $="box"===(null===(e=this.selector.number)||void 0===e?void 0:e.mode)||void 0===(null===(t=this.selector.number)||void 0===t?void 0:t.min)||void 0===(null===(i=this.selector.number)||void 0===i?void 0:i.max);let w;var C;if(!$&&(w=null!==(C=this.selector.number.step)&&void 0!==C?C:1,"any"===w)){w=1;const e=(this.selector.number.max-this.selector.number.min)/100;for(;w>e;)w/=10}const k=null===(o=this.selector.number)||void 0===o?void 0:o.translation_key;let V=null===(r=this.selector.number)||void 0===r?void 0:r.unit_of_measurement;return $&&V&&this.localizeValue&&k&&(V=this.localizeValue(`${k}.unit_of_measurement.${V}`)||V),(0,a.dy)(l||(l=u`
      ${0}
      <div class="input">
        ${0}
        <ha-textfield
          .inputMode=${0}
          .label=${0}
          .placeholder=${0}
          class=${0}
          .min=${0}
          .max=${0}
          .value=${0}
          .step=${0}
          helperPersistent
          .helper=${0}
          .disabled=${0}
          .required=${0}
          .suffix=${0}
          type="number"
          autoValidate
          ?no-spinner=${0}
          @input=${0}
        >
        </ha-textfield>
      </div>
      ${0}
    `),this.label&&!$?(0,a.dy)(d||(d=u`${0}${0}`),this.label,this.required?"*":""):a.Ld,$?a.Ld:(0,a.dy)(c||(c=u`
              <ha-slider
                labeled
                .min=${0}
                .max=${0}
                .value=${0}
                .step=${0}
                .disabled=${0}
                .required=${0}
                @change=${0}
                .ticks=${0}
              >
              </ha-slider>
            `),this.selector.number.min,this.selector.number.max,null!==(n=this.value)&&void 0!==n?n:"",w,this.disabled,this.required,this._handleSliderChange,null===(p=this.selector.number)||void 0===p?void 0:p.slider_ticks),"any"===(null===(v=this.selector.number)||void 0===v?void 0:v.step)||(null!==(b=null===(_=this.selector.number)||void 0===_?void 0:_.step)&&void 0!==b?b:1)%1!=0?"decimal":"numeric",$?this.label:void 0,this.placeholder,(0,s.$)({single:$}),null===(g=this.selector.number)||void 0===g?void 0:g.min,null===(m=this.selector.number)||void 0===m?void 0:m.max,null!==(y=this._valueStr)&&void 0!==y?y:"",null!==(f=null===(x=this.selector.number)||void 0===x?void 0:x.step)&&void 0!==f?f:1,$?this.helper:void 0,this.disabled,this.required,V,!$,this._handleInputChange,!$&&this.helper?(0,a.dy)(h||(h=u`<ha-input-helper-text .disabled=${0}
            >${0}</ha-input-helper-text
          >`),this.disabled,this.helper):a.Ld)}_handleInputChange(e){e.stopPropagation(),this._valueStr=e.target.value;const t=""===e.target.value||isNaN(e.target.value)?void 0:Number(e.target.value);this.value!==t&&(0,n.B)(this,"value-changed",{value:t})}_handleSliderChange(e){e.stopPropagation();const t=Number(e.target.value);this.value!==t&&(0,n.B)(this,"value-changed",{value:t})}constructor(...e){super(...e),this.required=!0,this.disabled=!1,this._valueStr=""}}v.styles=(0,a.iv)(p||(p=u`
    .input {
      display: flex;
      justify-content: space-between;
      align-items: center;
      direction: ltr;
    }
    ha-slider {
      flex: 1;
      margin-right: 16px;
      margin-inline-end: 16px;
      margin-inline-start: 0;
    }
    ha-textfield {
      --ha-textfield-input-width: 40px;
    }
    .single {
      --ha-textfield-input-width: unset;
      flex: 1;
    }
  `)),(0,o.__decorate)([(0,r.Cb)({attribute:!1})],v.prototype,"hass",void 0),(0,o.__decorate)([(0,r.Cb)({attribute:!1})],v.prototype,"selector",void 0),(0,o.__decorate)([(0,r.Cb)({type:Number})],v.prototype,"value",void 0),(0,o.__decorate)([(0,r.Cb)({type:Number})],v.prototype,"placeholder",void 0),(0,o.__decorate)([(0,r.Cb)()],v.prototype,"label",void 0),(0,o.__decorate)([(0,r.Cb)()],v.prototype,"helper",void 0),(0,o.__decorate)([(0,r.Cb)({attribute:!1})],v.prototype,"localizeValue",void 0),(0,o.__decorate)([(0,r.Cb)({type:Boolean})],v.prototype,"required",void 0),(0,o.__decorate)([(0,r.Cb)({type:Boolean})],v.prototype,"disabled",void 0),v=(0,o.__decorate)([(0,r.Mo)("ha-selector-number")],v)},24085:function(e,t,i){i.a(e,(async function(e,o){try{i.r(t),i.d(t,{HaSelectSelector:function(){return M}});i(39710),i(26847),i(18574),i(73042),i(81738),i(94814),i(29981),i(22960),i(6989),i(72489),i(1455),i(56389),i(27530);var a=i(73742),r=i(59048),s=i(7616),n=i(88245),l=i(74608),d=i(29740),c=i(41806),h=i(92949),p=(i(2414),i(91572),i(86776),i(54693)),u=(i(74207),i(42592),i(93795),i(71308),i(29490),i(77307),i(48374),e([p]));p=(u.then?(await u)():u)[0];let v,b,_,g,m,y,f,x,$,w,C,k,V,L,S,B=e=>e;const O="M7,19V17H9V19H7M11,19V17H13V19H11M15,19V17H17V19H15M7,15V13H9V15H7M11,15V13H13V15H11M15,15V13H17V15H15M7,11V9H9V11H7M11,11V9H13V11H11M15,11V9H17V11H15M7,7V5H9V7H7M11,7V5H13V7H11M15,7V5H17V7H15Z";class M extends r.oi{_itemMoved(e){e.stopPropagation();const{oldIndex:t,newIndex:i}=e.detail;this._move(t,i)}_move(e,t){const i=this.value.concat(),o=i.splice(e,1)[0];i.splice(t,0,o),this.value=i,(0,d.B)(this,"value-changed",{value:i})}render(){var e,t,i,o,a,s,d,p,u,L,S,M,H;const P=(null===(e=this.selector.select)||void 0===e||null===(e=e.options)||void 0===e?void 0:e.map((e=>"object"==typeof e?e:{value:e,label:e})))||[],D=null===(t=this.selector.select)||void 0===t?void 0:t.translation_key;var I;if(this.localizeValue&&D&&P.forEach((e=>{const t=this.localizeValue(`${D}.options.${e.value}`);t&&(e.label=t)})),null!==(i=this.selector.select)&&void 0!==i&&i.sort&&P.sort(((e,t)=>(0,h.fe)(e.label,t.label,this.hass.locale.language))),!(null!==(o=this.selector.select)&&void 0!==o&&o.multiple||null!==(a=this.selector.select)&&void 0!==a&&a.reorder||null!==(s=this.selector.select)&&void 0!==s&&s.custom_value||"box"!==this._mode))return(0,r.dy)(v||(v=B`
        ${0}
        <ha-select-box
          .options=${0}
          .value=${0}
          @value-changed=${0}
          .maxColumns=${0}
          .hass=${0}
        ></ha-select-box>
        ${0}
      `),this.label?(0,r.dy)(b||(b=B`<span class="label">${0}</span>`),this.label):r.Ld,P,this.value,this._valueChanged,null===(I=this.selector.select)||void 0===I?void 0:I.box_max_columns,this.hass,this._renderHelper());if(!(null!==(d=this.selector.select)&&void 0!==d&&d.custom_value||null!==(p=this.selector.select)&&void 0!==p&&p.reorder||"list"!==this._mode)){var z;if(null===(z=this.selector.select)||void 0===z||!z.multiple)return(0,r.dy)(_||(_=B`
          <div>
            ${0}
            ${0}
          </div>
          ${0}
        `),this.label,P.map((e=>(0,r.dy)(g||(g=B`
                <ha-formfield
                  .label=${0}
                  .disabled=${0}
                >
                  <ha-radio
                    .checked=${0}
                    .value=${0}
                    .disabled=${0}
                    @change=${0}
                  ></ha-radio>
                </ha-formfield>
              `),e.label,e.disabled||this.disabled,e.value===this.value,e.value,e.disabled||this.disabled,this._valueChanged))),this._renderHelper());const e=this.value&&""!==this.value?(0,l.r)(this.value):[];return(0,r.dy)(m||(m=B`
        <div>
          ${0}
          ${0}
        </div>
        ${0}
      `),this.label,P.map((t=>(0,r.dy)(y||(y=B`
              <ha-formfield .label=${0}>
                <ha-checkbox
                  .checked=${0}
                  .value=${0}
                  .disabled=${0}
                  @change=${0}
                ></ha-checkbox>
              </ha-formfield>
            `),t.label,e.includes(t.value),t.value,t.disabled||this.disabled,this._checkboxChanged))),this._renderHelper())}if(null!==(u=this.selector.select)&&void 0!==u&&u.multiple){var A;const e=this.value&&""!==this.value?(0,l.r)(this.value):[],t=P.filter((t=>!(t.disabled||null!=e&&e.includes(t.value))));return(0,r.dy)(f||(f=B`
        ${0}

        <ha-combo-box
          item-value-path="value"
          item-label-path="label"
          .hass=${0}
          .label=${0}
          .helper=${0}
          .disabled=${0}
          .required=${0}
          .value=${0}
          .items=${0}
          .allowCustomValue=${0}
          @filter-changed=${0}
          @value-changed=${0}
          @opened-changed=${0}
        ></ha-combo-box>
      `),null!=e&&e.length?(0,r.dy)(x||(x=B`
              <ha-sortable
                no-style
                .disabled=${0}
                @item-moved=${0}
                handle-selector="button.primary.action"
              >
                <ha-chip-set>
                  ${0}
                </ha-chip-set>
              </ha-sortable>
            `),!this.selector.select.reorder,this._itemMoved,(0,n.r)(e,(e=>e),((e,t)=>{var i,o,a;const s=(null===(i=P.find((t=>t.value===e)))||void 0===i?void 0:i.label)||e;return(0,r.dy)($||($=B`
                        <ha-input-chip
                          .idx=${0}
                          @remove=${0}
                          .label=${0}
                          selected
                        >
                          ${0}
                          ${0}
                        </ha-input-chip>
                      `),t,this._removeItem,s,null!==(o=this.selector.select)&&void 0!==o&&o.reorder?(0,r.dy)(w||(w=B`
                                <ha-svg-icon
                                  slot="icon"
                                  .path=${0}
                                ></ha-svg-icon>
                              `),O):r.Ld,(null===(a=P.find((t=>t.value===e)))||void 0===a?void 0:a.label)||e)}))):r.Ld,this.hass,this.label,this.helper,this.disabled,this.required&&!e.length,"",t,null!==(A=this.selector.select.custom_value)&&void 0!==A&&A,this._filterChanged,this._comboBoxValueChanged,this._openedChanged)}if(null!==(L=this.selector.select)&&void 0!==L&&L.custom_value){void 0===this.value||Array.isArray(this.value)||P.find((e=>e.value===this.value))||P.unshift({value:this.value,label:this.value});const e=P.filter((e=>!e.disabled));return(0,r.dy)(C||(C=B`
        <ha-combo-box
          item-value-path="value"
          item-label-path="label"
          .hass=${0}
          .label=${0}
          .helper=${0}
          .disabled=${0}
          .required=${0}
          .items=${0}
          .value=${0}
          @filter-changed=${0}
          @value-changed=${0}
          @opened-changed=${0}
        ></ha-combo-box>
      `),this.hass,this.label,this.helper,this.disabled,this.required,e,this.value,this._filterChanged,this._comboBoxValueChanged,this._openedChanged)}return(0,r.dy)(k||(k=B`
      <ha-select
        fixedMenuPosition
        naturalMenuWidth
        .label=${0}
        .value=${0}
        .helper=${0}
        .disabled=${0}
        .required=${0}
        clearable
        @closed=${0}
        @selected=${0}
      >
        ${0}
      </ha-select>
    `),null!==(S=this.label)&&void 0!==S?S:"",null!==(M=this.value)&&void 0!==M?M:"",null!==(H=this.helper)&&void 0!==H?H:"",this.disabled,this.required,c.U,this._valueChanged,P.map((e=>(0,r.dy)(V||(V=B`
            <ha-list-item .value=${0} .disabled=${0}
              >${0}</ha-list-item
            >
          `),e.value,e.disabled,e.label))))}_renderHelper(){return this.helper?(0,r.dy)(L||(L=B`<ha-input-helper-text .disabled=${0}
          >${0}</ha-input-helper-text
        >`),this.disabled,this.helper):""}get _mode(){var e,t;return(null===(e=this.selector.select)||void 0===e?void 0:e.mode)||(((null===(t=this.selector.select)||void 0===t||null===(t=t.options)||void 0===t?void 0:t.length)||0)<6?"list":"dropdown")}_valueChanged(e){var t,i,o;if(e.stopPropagation(),-1===(null===(t=e.detail)||void 0===t?void 0:t.index)&&void 0!==this.value)return void(0,d.B)(this,"value-changed",{value:void 0});const a=(null===(i=e.detail)||void 0===i?void 0:i.value)||e.target.value;this.disabled||void 0===a||a===(null!==(o=this.value)&&void 0!==o?o:"")||(0,d.B)(this,"value-changed",{value:a})}_checkboxChanged(e){if(e.stopPropagation(),this.disabled)return;let t;const i=e.target.value,o=e.target.checked,a=this.value&&""!==this.value?(0,l.r)(this.value):[];if(o){if(a.includes(i))return;t=[...a,i]}else{if(null==a||!a.includes(i))return;t=a.filter((e=>e!==i))}(0,d.B)(this,"value-changed",{value:t})}async _removeItem(e){e.stopPropagation();const t=[...(0,l.r)(this.value)];t.splice(e.target.idx,1),(0,d.B)(this,"value-changed",{value:t}),await this.updateComplete,this._filterChanged()}_comboBoxValueChanged(e){var t;e.stopPropagation();const i=e.detail.value;if(this.disabled||""===i)return;if(null===(t=this.selector.select)||void 0===t||!t.multiple)return void(0,d.B)(this,"value-changed",{value:i});const o=this.value&&""!==this.value?(0,l.r)(this.value):[];void 0!==i&&o.includes(i)||(setTimeout((()=>{this._filterChanged(),this.comboBox.setInputValue("")}),0),(0,d.B)(this,"value-changed",{value:[...o,i]}))}_openedChanged(e){null!=e&&e.detail.value&&this._filterChanged()}_filterChanged(e){var t,i;this._filter=(null==e?void 0:e.detail.value)||"";const o=null===(t=this.comboBox.items)||void 0===t?void 0:t.filter((e=>{var t;return(e.label||e.value).toLowerCase().includes(null===(t=this._filter)||void 0===t?void 0:t.toLowerCase())}));this._filter&&null!==(i=this.selector.select)&&void 0!==i&&i.custom_value&&o&&!o.some((e=>(e.label||e.value)===this._filter))&&o.unshift({label:this._filter,value:this._filter}),this.comboBox.filteredItems=o}constructor(...e){super(...e),this.disabled=!1,this.required=!0,this._filter=""}}M.styles=(0,r.iv)(S||(S=B`
    :host {
      position: relative;
    }
    ha-select,
    ha-formfield {
      display: block;
    }
    ha-list-item[disabled] {
      --mdc-theme-text-primary-on-background: var(--disabled-text-color);
    }
    ha-chip-set {
      padding: 8px 0;
    }

    .label {
      display: block;
      margin: 0 0 8px;
    }

    ha-select-box + ha-input-helper-text {
      margin-top: 4px;
    }

    .sortable-fallback {
      display: none;
      opacity: 0;
    }

    .sortable-ghost {
      opacity: 0.4;
    }

    .sortable-drag {
      cursor: grabbing;
    }
  `)),(0,a.__decorate)([(0,s.Cb)({attribute:!1})],M.prototype,"hass",void 0),(0,a.__decorate)([(0,s.Cb)({attribute:!1})],M.prototype,"selector",void 0),(0,a.__decorate)([(0,s.Cb)()],M.prototype,"value",void 0),(0,a.__decorate)([(0,s.Cb)()],M.prototype,"label",void 0),(0,a.__decorate)([(0,s.Cb)()],M.prototype,"helper",void 0),(0,a.__decorate)([(0,s.Cb)({attribute:!1})],M.prototype,"localizeValue",void 0),(0,a.__decorate)([(0,s.Cb)({type:Boolean})],M.prototype,"disabled",void 0),(0,a.__decorate)([(0,s.Cb)({type:Boolean})],M.prototype,"required",void 0),(0,a.__decorate)([(0,s.IO)("ha-combo-box",!0)],M.prototype,"comboBox",void 0),M=(0,a.__decorate)([(0,s.Mo)("ha-selector-select")],M),o()}catch(v){o(v)}}))},32986:function(e,t,i){i(26847),i(1455),i(64455),i(67886),i(65451),i(46015),i(38334),i(94880),i(75643),i(29761),i(6202),i(27530);var o=i(73742),a=i(59048),r=i(7616),s=i(28105),n=i(69342),l=i(45103);let d,c=e=>e;const h={action:()=>Promise.all([i.e("4458"),i.e("2092"),i.e("1645"),i.e("8167"),i.e("133"),i.e("2335"),i.e("8193"),i.e("2571"),i.e("8461"),i.e("3348"),i.e("2795")]).then(i.bind(i,36112)),addon:()=>i.e("1697").then(i.bind(i,38245)),area:()=>i.e("7665").then(i.bind(i,97034)),areas_display:()=>i.e("4598").then(i.bind(i,77046)),attribute:()=>i.e("8552").then(i.bind(i,58558)),assist_pipeline:()=>i.e("5047").then(i.bind(i,83019)),boolean:()=>i.e("6734").then(i.bind(i,96382)),color_rgb:()=>i.e("6381").then(i.bind(i,15464)),condition:()=>Promise.all([i.e("4458"),i.e("1645"),i.e("8167"),i.e("133"),i.e("2335"),i.e("8193"),i.e("8461"),i.e("7920")]).then(i.bind(i,98731)),config_entry:()=>i.e("4751").then(i.bind(i,33301)),conversation_agent:()=>i.e("5033").then(i.bind(i,88381)),constant:()=>i.e("9054").then(i.bind(i,50582)),country:()=>i.e("6083").then(i.bind(i,51576)),date:()=>i.e("5112").then(i.bind(i,72135)),datetime:()=>i.e("2691").then(i.bind(i,39280)),device:()=>i.e("6477").then(i.bind(i,12840)),duration:()=>i.e("297").then(i.bind(i,30093)),entity:()=>Promise.all([i.e("8167"),i.e("133"),i.e("1345")]).then(i.bind(i,87393)),statistic:()=>Promise.all([i.e("8167"),i.e("3419")]).then(i.bind(i,76641)),file:()=>i.e("816").then(i.bind(i,97258)),floor:()=>i.e("9961").then(i.bind(i,28086)),label:()=>Promise.all([i.e("9204"),i.e("5600")]).then(i.bind(i,45917)),image:()=>Promise.all([i.e("7530"),i.e("5737")]).then(i.bind(i,62464)),background:()=>Promise.all([i.e("7530"),i.e("5875")]).then(i.bind(i,51323)),language:()=>i.e("1316").then(i.bind(i,50736)),navigation:()=>i.e("5799").then(i.bind(i,53306)),number:()=>Promise.resolve().then(i.bind(i,69028)),object:()=>Promise.all([i.e("2335"),i.e("5792")]).then(i.bind(i,57612)),qr_code:()=>Promise.all([i.e("6892"),i.e("9462")]).then(i.bind(i,68011)),select:()=>Promise.resolve().then(i.bind(i,24085)),selector:()=>i.e("6470").then(i.bind(i,69933)),state:()=>i.e("6254").then(i.bind(i,76983)),backup_location:()=>i.e("9494").then(i.bind(i,26274)),stt:()=>i.e("2102").then(i.bind(i,30441)),target:()=>Promise.all([i.e("2092"),i.e("3459"),i.e("8167"),i.e("133"),i.e("4444")]).then(i.bind(i,66495)),template:()=>i.e("4394").then(i.bind(i,88011)),text:()=>Promise.resolve().then(i.bind(i,10667)),time:()=>i.e("9672").then(i.bind(i,8633)),icon:()=>i.e("3254").then(i.bind(i,37339)),media:()=>i.e("9902").then(i.bind(i,76609)),theme:()=>i.e("4538").then(i.bind(i,10066)),button_toggle:()=>i.e("8376").then(i.bind(i,2702)),trigger:()=>Promise.all([i.e("4458"),i.e("1645"),i.e("8167"),i.e("133"),i.e("2335"),i.e("8193"),i.e("2571"),i.e("2775")]).then(i.bind(i,98515)),tts:()=>i.e("8183").then(i.bind(i,55983)),tts_voice:()=>i.e("6369").then(i.bind(i,24684)),location:()=>Promise.all([i.e("1506"),i.e("9656")]).then(i.bind(i,4830)),color_temp:()=>Promise.all([i.e("7717"),i.e("9114")]).then(i.bind(i,19451)),ui_action:()=>Promise.all([i.e("2092"),i.e("2335"),i.e("3348"),i.e("5171")]).then(i.bind(i,53179)),ui_color:()=>i.e("2304").then(i.bind(i,22104)),ui_state_content:()=>Promise.all([i.e("9392"),i.e("6979"),i.e("4463")]).then(i.bind(i,42981))},p=new Set(["ui-action","ui-color"]);class u extends a.oi{async focus(){var e;await this.updateComplete,null===(e=this.renderRoot.querySelector("#selector"))||void 0===e||e.focus()}get _type(){const e=Object.keys(this.selector)[0];return p.has(e)?e.replace("-","_"):e}willUpdate(e){var t;e.has("selector")&&this.selector&&(null===(t=h[this._type])||void 0===t||t.call(h))}render(){return(0,a.dy)(d||(d=c`
      ${0}
    `),(0,n.h)(`ha-selector-${this._type}`,{hass:this.hass,narrow:this.narrow,name:this.name,selector:this._handleLegacySelector(this.selector),value:this.value,label:this.label,placeholder:this.placeholder,disabled:this.disabled,required:this.required,helper:this.helper,context:this.context,localizeValue:this.localizeValue,id:"selector"}))}constructor(...e){super(...e),this.narrow=!1,this.disabled=!1,this.required=!0,this._handleLegacySelector=(0,s.Z)((e=>{if("entity"in e)return(0,l.CM)(e);if("device"in e)return(0,l.c9)(e);const t=Object.keys(this.selector)[0];return p.has(t)?{[t.replace("-","_")]:e[t]}:e}))}}(0,o.__decorate)([(0,r.Cb)({attribute:!1})],u.prototype,"hass",void 0),(0,o.__decorate)([(0,r.Cb)({type:Boolean})],u.prototype,"narrow",void 0),(0,o.__decorate)([(0,r.Cb)()],u.prototype,"name",void 0),(0,o.__decorate)([(0,r.Cb)({attribute:!1})],u.prototype,"selector",void 0),(0,o.__decorate)([(0,r.Cb)()],u.prototype,"value",void 0),(0,o.__decorate)([(0,r.Cb)()],u.prototype,"label",void 0),(0,o.__decorate)([(0,r.Cb)()],u.prototype,"helper",void 0),(0,o.__decorate)([(0,r.Cb)({attribute:!1})],u.prototype,"localizeValue",void 0),(0,o.__decorate)([(0,r.Cb)()],u.prototype,"placeholder",void 0),(0,o.__decorate)([(0,r.Cb)({type:Boolean})],u.prototype,"disabled",void 0),(0,o.__decorate)([(0,r.Cb)({type:Boolean})],u.prototype,"required",void 0),(0,o.__decorate)([(0,r.Cb)({attribute:!1})],u.prototype,"context",void 0),u=(0,o.__decorate)([(0,r.Mo)("ha-selector")],u)},14891:function(e,t,i){i(26847),i(27530);var o=i(73742),a=i(59048),r=i(7616);let s,n,l=e=>e;class d extends a.oi{render(){return(0,a.dy)(s||(s=l`
      <div class="prefix-wrap">
        <slot name="prefix"></slot>
        <div
          class="body"
          ?two-line=${0}
          ?three-line=${0}
        >
          <slot name="heading"></slot>
          <div class="secondary"><slot name="description"></slot></div>
        </div>
      </div>
      <div class="content"><slot></slot></div>
    `),!this.threeLine,this.threeLine)}constructor(...e){super(...e),this.narrow=!1,this.slim=!1,this.threeLine=!1,this.wrapHeading=!1}}d.styles=(0,a.iv)(n||(n=l`
    :host {
      display: flex;
      padding: 0 16px;
      align-content: normal;
      align-self: auto;
      align-items: center;
    }
    .body {
      padding-top: 8px;
      padding-bottom: 8px;
      padding-left: 0;
      padding-inline-start: 0;
      padding-right: 16px;
      padding-inline-end: 16px;
      overflow: hidden;
      display: var(--layout-vertical_-_display, flex);
      flex-direction: var(--layout-vertical_-_flex-direction, column);
      justify-content: var(--layout-center-justified_-_justify-content, center);
      flex: var(--layout-flex_-_flex, 1);
      flex-basis: var(--layout-flex_-_flex-basis, 0.000000001px);
    }
    .body[three-line] {
      min-height: 88px;
    }
    :host(:not([wrap-heading])) body > * {
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }
    .body > .secondary {
      display: block;
      padding-top: 4px;
      font-family: var(
        --mdc-typography-body2-font-family,
        var(--mdc-typography-font-family, var(--ha-font-family-body))
      );
      font-size: var(--mdc-typography-body2-font-size, var(--ha-font-size-s));
      -webkit-font-smoothing: var(--ha-font-smoothing);
      -moz-osx-font-smoothing: var(--ha-moz-osx-font-smoothing);
      font-weight: var(
        --mdc-typography-body2-font-weight,
        var(--ha-font-weight-normal)
      );
      line-height: normal;
      color: var(--secondary-text-color);
    }
    .body[two-line] {
      min-height: calc(72px - 16px);
      flex: 1;
    }
    .content {
      display: contents;
    }
    :host(:not([narrow])) .content {
      display: var(--settings-row-content-display, flex);
      justify-content: flex-end;
      flex: 1;
      min-width: 0;
      padding: 16px 0;
    }
    .content ::slotted(*) {
      width: var(--settings-row-content-width);
    }
    :host([narrow]) {
      align-items: normal;
      flex-direction: column;
      border-top: 1px solid var(--divider-color);
      padding-bottom: 8px;
    }
    ::slotted(ha-switch) {
      padding: 16px 0;
    }
    .secondary {
      white-space: normal;
    }
    .prefix-wrap {
      display: var(--settings-row-prefix-display);
    }
    :host([narrow]) .prefix-wrap {
      display: flex;
      align-items: center;
    }
    :host([slim]),
    :host([slim]) .content,
    :host([slim]) ::slotted(ha-switch) {
      padding: 0;
    }
    :host([slim]) .body {
      min-height: 0;
    }
  `)),(0,o.__decorate)([(0,r.Cb)({type:Boolean,reflect:!0})],d.prototype,"narrow",void 0),(0,o.__decorate)([(0,r.Cb)({type:Boolean,reflect:!0})],d.prototype,"slim",void 0),(0,o.__decorate)([(0,r.Cb)({type:Boolean,attribute:"three-line"})],d.prototype,"threeLine",void 0),(0,o.__decorate)([(0,r.Cb)({type:Boolean,attribute:"wrap-heading",reflect:!0})],d.prototype,"wrapHeading",void 0),d=(0,o.__decorate)([(0,r.Mo)("ha-settings-row")],d)},57275:function(e,t,i){var o=i(73742),a=i(8851),r=i(57905),s=i(59048),n=i(7616),l=i(51597);let d;class c extends a.i{connectedCallback(){super.connectedCallback(),this.dir=l.E.document.dir}}c.styles=[r.W,(0,s.iv)(d||(d=(e=>e)`
      :host {
        --md-sys-color-primary: var(--primary-color);
        --md-sys-color-on-primary: var(--text-primary-color);
        --md-sys-color-outline: var(--outline-color);
        --md-sys-color-on-surface: var(--primary-text-color);
        --md-slider-handle-width: 14px;
        --md-slider-handle-height: 14px;
        --md-slider-state-layer-size: 24px;
        min-width: 100px;
        min-inline-size: 100px;
        width: 200px;
      }
    `))],c=(0,o.__decorate)([(0,n.Mo)("ha-slider")],c)},48374:function(e,t,i){i(26847),i(81738),i(94814),i(87799),i(1455),i(40589),i(27530);var o=i(73742),a=i(59048),r=i(7616),s=i(29740);let n,l=e=>e;class d extends a.oi{updated(e){e.has("disabled")&&(this.disabled?this._destroySortable():this._createSortable())}disconnectedCallback(){super.disconnectedCallback(),this._shouldBeDestroy=!0,setTimeout((()=>{this._shouldBeDestroy&&(this._destroySortable(),this._shouldBeDestroy=!1)}),1)}connectedCallback(){super.connectedCallback(),this._shouldBeDestroy=!1,this.hasUpdated&&!this.disabled&&this._createSortable()}createRenderRoot(){return this}render(){return this.noStyle?a.Ld:(0,a.dy)(n||(n=l`
      <style>
        .sortable-fallback {
          display: none !important;
        }

        .sortable-ghost {
          box-shadow: 0 0 0 2px var(--primary-color);
          background: rgba(var(--rgb-primary-color), 0.25);
          border-radius: 4px;
          opacity: 0.4;
        }

        .sortable-drag {
          border-radius: 4px;
          opacity: 1;
          background: var(--card-background-color);
          box-shadow: 0px 4px 8px 3px #00000026;
          cursor: grabbing;
        }
      </style>
    `))}async _createSortable(){if(this._sortable)return;const e=this.children[0];if(!e)return;const t=(await Promise.all([i.e("7597"),i.e("9600")]).then(i.bind(i,72764))).default,o=Object.assign(Object.assign({scroll:!0,forceAutoScrollFallback:!0,scrollSpeed:20,animation:150},this.options),{},{onChoose:this._handleChoose,onStart:this._handleStart,onEnd:this._handleEnd,onUpdate:this._handleUpdate,onAdd:this._handleAdd,onRemove:this._handleRemove});this.draggableSelector&&(o.draggable=this.draggableSelector),this.handleSelector&&(o.handle=this.handleSelector),void 0!==this.invertSwap&&(o.invertSwap=this.invertSwap),this.group&&(o.group=this.group),this.filter&&(o.filter=this.filter),this._sortable=new t(e,o)}_destroySortable(){this._sortable&&(this._sortable.destroy(),this._sortable=void 0)}constructor(...e){super(...e),this.disabled=!1,this.noStyle=!1,this.invertSwap=!1,this.rollback=!0,this._shouldBeDestroy=!1,this._handleUpdate=e=>{(0,s.B)(this,"item-moved",{newIndex:e.newIndex,oldIndex:e.oldIndex})},this._handleAdd=e=>{(0,s.B)(this,"item-added",{index:e.newIndex,data:e.item.sortableData})},this._handleRemove=e=>{(0,s.B)(this,"item-removed",{index:e.oldIndex})},this._handleEnd=async e=>{(0,s.B)(this,"drag-end"),this.rollback&&e.item.placeholder&&(e.item.placeholder.replaceWith(e.item),delete e.item.placeholder)},this._handleStart=()=>{(0,s.B)(this,"drag-start")},this._handleChoose=e=>{this.rollback&&(e.item.placeholder=document.createComment("sort-placeholder"),e.item.after(e.item.placeholder))}}}(0,o.__decorate)([(0,r.Cb)({type:Boolean})],d.prototype,"disabled",void 0),(0,o.__decorate)([(0,r.Cb)({type:Boolean,attribute:"no-style"})],d.prototype,"noStyle",void 0),(0,o.__decorate)([(0,r.Cb)({type:String,attribute:"draggable-selector"})],d.prototype,"draggableSelector",void 0),(0,o.__decorate)([(0,r.Cb)({type:String,attribute:"handle-selector"})],d.prototype,"handleSelector",void 0),(0,o.__decorate)([(0,r.Cb)({type:String,attribute:"filter"})],d.prototype,"filter",void 0),(0,o.__decorate)([(0,r.Cb)({type:String})],d.prototype,"group",void 0),(0,o.__decorate)([(0,r.Cb)({type:Boolean,attribute:"invert-swap"})],d.prototype,"invertSwap",void 0),(0,o.__decorate)([(0,r.Cb)({attribute:!1})],d.prototype,"options",void 0),(0,o.__decorate)([(0,r.Cb)({type:Boolean})],d.prototype,"rollback",void 0),d=(0,o.__decorate)([(0,r.Mo)("ha-sortable")],d)},40830:function(e,t,i){i.r(t),i.d(t,{HaSvgIcon:function(){return h}});var o=i(73742),a=i(59048),r=i(7616);let s,n,l,d,c=e=>e;class h extends a.oi{render(){return(0,a.YP)(s||(s=c`
    <svg
      viewBox=${0}
      preserveAspectRatio="xMidYMid meet"
      focusable="false"
      role="img"
      aria-hidden="true"
    >
      <g>
        ${0}
        ${0}
      </g>
    </svg>`),this.viewBox||"0 0 24 24",this.path?(0,a.YP)(n||(n=c`<path class="primary-path" d=${0}></path>`),this.path):a.Ld,this.secondaryPath?(0,a.YP)(l||(l=c`<path class="secondary-path" d=${0}></path>`),this.secondaryPath):a.Ld)}}h.styles=(0,a.iv)(d||(d=c`
    :host {
      display: var(--ha-icon-display, inline-flex);
      align-items: center;
      justify-content: center;
      position: relative;
      vertical-align: middle;
      fill: var(--icon-primary-color, currentcolor);
      width: var(--mdc-icon-size, 24px);
      height: var(--mdc-icon-size, 24px);
    }
    svg {
      width: 100%;
      height: 100%;
      pointer-events: none;
      display: block;
    }
    path.primary-path {
      opacity: var(--icon-primary-opactity, 1);
    }
    path.secondary-path {
      fill: var(--icon-secondary-color, currentcolor);
      opacity: var(--icon-secondary-opactity, 0.5);
    }
  `)),(0,o.__decorate)([(0,r.Cb)()],h.prototype,"path",void 0),(0,o.__decorate)([(0,r.Cb)({attribute:!1})],h.prototype,"secondaryPath",void 0),(0,o.__decorate)([(0,r.Cb)({attribute:!1})],h.prototype,"viewBox",void 0),h=(0,o.__decorate)([(0,r.Mo)("ha-svg-icon")],h)},57108:function(e,t,i){i.d(t,{IO:function(){return r},Lo:function(){return a},a:function(){return n},qv:function(){return s}});i(26847),i(2394),i(87799),i(27530);var o=i(92949);i(96110);const a=(e,t)=>e.callWS(Object.assign({type:"config/area_registry/create"},t)),r=(e,t,i)=>e.callWS(Object.assign({type:"config/area_registry/update",area_id:t},i)),s=(e,t)=>e.callWS({type:"config/area_registry/delete",area_id:t}),n=(e,t)=>(i,a)=>{const r=t?t.indexOf(i):-1,s=t?t.indexOf(a):-1;if(-1===r&&-1===s){var n,l,d,c;const t=null!==(n=null==e||null===(l=e[i])||void 0===l?void 0:l.name)&&void 0!==n?n:i,r=null!==(d=null==e||null===(c=e[a])||void 0===c?void 0:c.name)&&void 0!==d?d:a;return(0,o.$K)(t,r)}return-1===r?1:-1===s?-1:r-s}},57774:function(e,t,i){i.d(t,{HP:function(){return r},t1:function(){return o},R6:function(){return a}});i(26847),i(2394),i(18574),i(81738),i(94814),i(29981),i(87799),i(67886),i(65451),i(46015),i(38334),i(94880),i(75643),i(29761),i(27530),i(31298),i(92949),i(16811);const o=(e,t,i)=>e.callWS(Object.assign({type:"config/device_registry/update",device_id:t},i)),a=e=>{const t={};for(const i of e)i.device_id&&(i.device_id in t||(t[i.device_id]=[]),t[i.device_id].push(i));return t},r=(e,t,i,o)=>{const a={};for(const r of t){const t=e[r.entity_id];null!=t&&t.domain&&null!==r.device_id&&(a[r.device_id]=a[r.device_id]||new Set,a[r.device_id].add(t.domain))}if(i&&o)for(const r of i)for(const e of r.config_entries){const t=o.find((t=>t.entry_id===e));null!=t&&t.domain&&(a[r.id]=a[r.id]||new Set,a[r.id].add(t.domain))}return a}},45103:function(e,t,i){i.d(t,{CM:function(){return f},QQ:function(){return g},aV:function(){return v},bq:function(){return $},c9:function(){return x},lE:function(){return m},lV:function(){return y},o1:function(){return h},qJ:function(){return _},qR:function(){return p},vI:function(){return b},xO:function(){return u}});var o=i(47817),a=(i(81315),i(39710),i(26847),i(2394),i(78152),i(81738),i(94814),i(55770),i(22960),i(72489),i(87799),i(67886),i(65451),i(46015),i(38334),i(94880),i(75643),i(29761),i(56389),i(27530),i(74608)),r=i(18088),s=i(75012),n=i(56845),l=i(57774);const d=["domain","integration","device_class"],c=["integration","manufacturer","model"],h=(e,t,i,o,a,r,s)=>{const n=[],l=[],d=[];return Object.values(i).forEach((i=>{i.labels.includes(t)&&b(e,a,o,i.area_id,r,s)&&d.push(i.area_id)})),Object.values(o).forEach((i=>{i.labels.includes(t)&&_(e,Object.values(a),i,r,s)&&l.push(i.id)})),Object.values(a).forEach((i=>{i.labels.includes(t)&&g(e.states[i.entity_id],r,s)&&n.push(i.entity_id)})),{areas:d,devices:l,entities:n}},p=(e,t,i,o,a)=>{const r=[];return Object.values(i).forEach((i=>{i.floor_id===t&&b(e,e.entities,e.devices,i.area_id,o,a)&&r.push(i.area_id)})),{areas:r}},u=(e,t,i,o,a,r)=>{const s=[],n=[];return Object.values(i).forEach((i=>{i.area_id===t&&_(e,Object.values(o),i,a,r)&&n.push(i.id)})),Object.values(o).forEach((i=>{i.area_id===t&&g(e.states[i.entity_id],a,r)&&s.push(i.entity_id)})),{devices:n,entities:s}},v=(e,t,i,o,a)=>{const r=[];return Object.values(i).forEach((i=>{i.device_id===t&&g(e.states[i.entity_id],o,a)&&r.push(i.entity_id)})),{entities:r}},b=(e,t,i,o,a,r)=>!!Object.values(i).some((i=>!(i.area_id!==o||!_(e,Object.values(t),i,a,r))))||Object.values(t).some((t=>!(t.area_id!==o||!g(e.states[t.entity_id],a,r)))),_=(e,t,i,o,r)=>{var s,n;const d=r?(0,l.HP)(r,t):void 0;if(null!==(s=o.target)&&void 0!==s&&s.device&&!(0,a.r)(o.target.device).some((e=>m(e,i,d))))return!1;if(null!==(n=o.target)&&void 0!==n&&n.entity){return t.filter((e=>e.device_id===i.id)).some((t=>{const i=e.states[t.entity_id];return g(i,o,r)}))}return!0},g=(e,t,i)=>{var o;return!!e&&(null===(o=t.target)||void 0===o||!o.entity||(0,a.r)(t.target.entity).some((t=>y(t,e,i))))},m=(e,t,i)=>{const{manufacturer:o,model:a,model_id:r,integration:s}=e;if(o&&t.manufacturer!==o)return!1;if(a&&t.model!==a)return!1;if(r&&t.model_id!==r)return!1;var n;if(s&&i&&(null==i||null===(n=i[t.id])||void 0===n||!n.has(s)))return!1;return!0},y=(e,t,i)=>{var o;const{domain:n,device_class:l,supported_features:d,integration:c}=e;if(n){const e=(0,r.N)(t);if(Array.isArray(n)?!n.includes(e):e!==n)return!1}if(l){const e=t.attributes.device_class;if(e&&Array.isArray(l)?!l.includes(e):e!==l)return!1}return!(d&&!(0,a.r)(d).some((e=>(0,s.e)(t,e))))&&(!c||(null==i||null===(o=i[t.entity_id])||void 0===o?void 0:o.domain)===c)},f=e=>{if(!e.entity)return{entity:null};if("filter"in e.entity)return e;const t=e.entity,{domain:i,integration:a,device_class:r}=t,s=(0,o.Z)(t,d);return i||a||r?{entity:Object.assign(Object.assign({},s),{},{filter:{domain:i,integration:a,device_class:r}})}:{entity:s}},x=e=>{if(!e.device)return{device:null};if("filter"in e.device)return e;const t=e.device,{integration:i,manufacturer:a,model:r}=t,s=(0,o.Z)(t,c);return i||a||r?{device:Object.assign(Object.assign({},s),{},{filter:{integration:i,manufacturer:a,model:r}})}:{device:s}},$=e=>{let t;var i;if("target"in e)t=(0,a.r)(null===(i=e.target)||void 0===i?void 0:i.entity);else if("entity"in e){var o,r;if(null!==(o=e.entity)&&void 0!==o&&o.include_entities)return;t=(0,a.r)(null===(r=e.entity)||void 0===r?void 0:r.filter)}if(!t)return;const s=t.flatMap((e=>e.integration||e.device_class||e.supported_features||!e.domain?[]:(0,a.r)(e.domain).filter((e=>(0,n.X)(e)))));return[...new Set(s)]}},96110:function(e,t,i){i(18574),i(92949),i(16811)},56165:function(e,t,i){i(26847),i(27530);var o=i(73742),a=i(59048),r=i(7616),s=i(40985),n=(i(64218),i(38098),i(77204));let l,d,c,h,p,u=e=>e;class v extends a.oi{render(){var e;return(0,a.dy)(l||(l=u`
      <div class="toolbar">
        ${0}

        <div class="main-title"><slot name="header">${0}</slot></div>
        <slot name="toolbar-icon"></slot>
      </div>
      <div class="content ha-scrollbar" @scroll=${0}>
        <slot></slot>
      </div>
      <div id="fab">
        <slot name="fab"></slot>
      </div>
    `),this.mainPage||null!==(e=history.state)&&void 0!==e&&e.root?(0,a.dy)(d||(d=u`
              <ha-menu-button
                .hassio=${0}
                .hass=${0}
                .narrow=${0}
              ></ha-menu-button>
            `),this.supervisor,this.hass,this.narrow):this.backPath?(0,a.dy)(c||(c=u`
                <a href=${0}>
                  <ha-icon-button-arrow-prev
                    .hass=${0}
                  ></ha-icon-button-arrow-prev>
                </a>
              `),this.backPath,this.hass):(0,a.dy)(h||(h=u`
                <ha-icon-button-arrow-prev
                  .hass=${0}
                  @click=${0}
                ></ha-icon-button-arrow-prev>
              `),this.hass,this._backTapped),this.header,this._saveScrollPos)}_saveScrollPos(e){this._savedScrollPos=e.target.scrollTop}_backTapped(){this.backCallback?this.backCallback():history.back()}static get styles(){return[n.$c,(0,a.iv)(p||(p=u`
        :host {
          display: block;
          height: 100%;
          background-color: var(--primary-background-color);
          overflow: hidden;
          position: relative;
        }

        :host([narrow]) {
          width: 100%;
          position: fixed;
        }

        .toolbar {
          display: flex;
          align-items: center;
          font-size: var(--ha-font-size-xl);
          height: var(--header-height);
          padding: 8px 12px;
          background-color: var(--app-header-background-color);
          font-weight: var(--ha-font-weight-normal);
          color: var(--app-header-text-color, white);
          border-bottom: var(--app-header-border-bottom, none);
          box-sizing: border-box;
        }
        @media (max-width: 599px) {
          .toolbar {
            padding: 4px;
          }
        }
        .toolbar a {
          color: var(--sidebar-text-color);
          text-decoration: none;
        }

        ha-menu-button,
        ha-icon-button-arrow-prev,
        ::slotted([slot="toolbar-icon"]) {
          pointer-events: auto;
          color: var(--sidebar-icon-color);
        }

        .main-title {
          margin: var(--margin-title);
          line-height: var(--ha-line-height-normal);
          min-width: 0;
          flex-grow: 1;
          overflow-wrap: break-word;
          display: -webkit-box;
          -webkit-line-clamp: 2;
          -webkit-box-orient: vertical;
          overflow: hidden;
          text-overflow: ellipsis;
          padding-bottom: 1px;
        }

        .content {
          position: relative;
          width: 100%;
          height: calc(100% - 1px - var(--header-height));
          overflow-y: auto;
          overflow: auto;
          -webkit-overflow-scrolling: touch;
        }

        #fab {
          position: absolute;
          right: calc(16px + var(--safe-area-inset-right));
          inset-inline-end: calc(16px + var(--safe-area-inset-right));
          inset-inline-start: initial;
          bottom: calc(16px + var(--safe-area-inset-bottom));
          z-index: 1;
          display: flex;
          flex-wrap: wrap;
          justify-content: flex-end;
          gap: 8px;
        }
        :host([narrow]) #fab.tabs {
          bottom: calc(84px + var(--safe-area-inset-bottom));
        }
        #fab[is-wide] {
          bottom: 24px;
          right: 24px;
          inset-inline-end: 24px;
          inset-inline-start: initial;
        }
      `))]}constructor(...e){super(...e),this.mainPage=!1,this.narrow=!1,this.supervisor=!1}}(0,o.__decorate)([(0,r.Cb)({attribute:!1})],v.prototype,"hass",void 0),(0,o.__decorate)([(0,r.Cb)()],v.prototype,"header",void 0),(0,o.__decorate)([(0,r.Cb)({type:Boolean,attribute:"main-page"})],v.prototype,"mainPage",void 0),(0,o.__decorate)([(0,r.Cb)({type:String,attribute:"back-path"})],v.prototype,"backPath",void 0),(0,o.__decorate)([(0,r.Cb)({attribute:!1})],v.prototype,"backCallback",void 0),(0,o.__decorate)([(0,r.Cb)({type:Boolean,reflect:!0})],v.prototype,"narrow",void 0),(0,o.__decorate)([(0,r.Cb)({type:Boolean})],v.prototype,"supervisor",void 0),(0,o.__decorate)([(0,s.i)(".content")],v.prototype,"_savedScrollPos",void 0),(0,o.__decorate)([(0,r.hO)({passive:!0})],v.prototype,"_saveScrollPos",null),v=(0,o.__decorate)([(0,r.Mo)("hass-subpage")],v)},95846:function(e,t,i){i.d(t,{E:function(){return r}});i(26847),i(1455),i(27530);var o=i(29740);const a=()=>Promise.all([i.e("2154"),i.e("8167"),i.e("133"),i.e("7530"),i.e("9204"),i.e("1278")]).then(i.bind(i,2460)),r=(e,t)=>{(0,o.B)(e,"show-dialog",{dialogTag:"dialog-area-registry-detail",dialogImport:a,dialogParams:t})}},56845:function(e,t,i){i.d(t,{X:function(){return o}});const o=(0,i(13228).z)(["input_boolean","input_button","input_text","input_number","input_datetime","input_select","counter","timer","schedule"])},93117:function(e,t,i){i.d(t,{J:function(){return r}});i(26847),i(81738),i(94814),i(6989),i(87799),i(64455),i(41381),i(27530);var o=i(39230);const a={ignoreDiacritics:!0,isCaseSensitive:!1,threshold:.3,minMatchCharLength:2};class r extends o.Z{multiTermsSearch(e,t){const i=e.toLowerCase().split(" "),{minMatchCharLength:o}=this.options,a=o?i.filter((e=>e.length>=o)):i;if(0===a.length)return null;const r=this.getIndex().toJSON().keys,s={$and:a.map((e=>({$or:r.map((t=>({$path:t.path,$val:e})))})))};return this.search(s,t)}constructor(e,t,i){super(e,Object.assign(Object.assign({},a),t),i)}}},77204:function(e,t,i){i.d(t,{$c:function(){return u},Qx:function(){return h},k1:function(){return c},yu:function(){return p}});var o=i(59048);let a,r,s,n,l,d=e=>e;const c=(0,o.iv)(a||(a=d`
  button.link {
    background: none;
    color: inherit;
    border: none;
    padding: 0;
    font: inherit;
    text-align: left;
    text-decoration: underline;
    cursor: pointer;
    outline: none;
  }
`)),h=(0,o.iv)(r||(r=d`
  :host {
    font-family: var(--ha-font-family-body);
    -webkit-font-smoothing: var(--ha-font-smoothing);
    -moz-osx-font-smoothing: var(--ha-moz-osx-font-smoothing);
    font-size: var(--ha-font-size-m);
    font-weight: var(--ha-font-weight-normal);
    line-height: var(--ha-line-height-normal);
  }

  app-header div[sticky] {
    height: 48px;
  }

  app-toolbar [main-title] {
    margin-left: 20px;
    margin-inline-start: 20px;
    margin-inline-end: initial;
  }

  h1 {
    font-family: var(--ha-font-family-heading);
    -webkit-font-smoothing: var(--ha-font-smoothing);
    -moz-osx-font-smoothing: var(--ha-moz-osx-font-smoothing);
    font-size: var(--ha-font-size-2xl);
    font-weight: var(--ha-font-weight-normal);
    line-height: var(--ha-line-height-condensed);
  }

  h2 {
    font-family: var(--ha-font-family-body);
    -webkit-font-smoothing: var(--ha-font-smoothing);
    -moz-osx-font-smoothing: var(--ha-moz-osx-font-smoothing);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    font-size: var(--ha-font-size-xl);
    font-weight: var(--ha-font-weight-medium);
    line-height: var(--ha-line-height-normal);
  }

  h3 {
    font-family: var(--ha-font-family-body);
    -webkit-font-smoothing: var(--ha-font-smoothing);
    -moz-osx-font-smoothing: var(--ha-moz-osx-font-smoothing);
    font-size: var(--ha-font-size-l);
    font-weight: var(--ha-font-weight-normal);
    line-height: var(--ha-line-height-normal);
  }

  a {
    color: var(--primary-color);
  }

  .secondary {
    color: var(--secondary-text-color);
  }

  .error {
    color: var(--error-color);
  }

  .warning {
    color: var(--error-color);
  }

  ${0}

  .card-actions a {
    text-decoration: none;
  }

  .card-actions .warning {
    --mdc-theme-primary: var(--error-color);
  }

  .layout.horizontal,
  .layout.vertical {
    display: flex;
  }
  .layout.inline {
    display: inline-flex;
  }
  .layout.horizontal {
    flex-direction: row;
  }
  .layout.vertical {
    flex-direction: column;
  }
  .layout.wrap {
    flex-wrap: wrap;
  }
  .layout.no-wrap {
    flex-wrap: nowrap;
  }
  .layout.center,
  .layout.center-center {
    align-items: center;
  }
  .layout.bottom {
    align-items: flex-end;
  }
  .layout.center-justified,
  .layout.center-center {
    justify-content: center;
  }
  .flex {
    flex: 1;
    flex-basis: 0.000000001px;
  }
  .flex-auto {
    flex: 1 1 auto;
  }
  .flex-none {
    flex: none;
  }
  .layout.justified {
    justify-content: space-between;
  }
`),c),p=(0,o.iv)(s||(s=d`
  /* mwc-dialog (ha-dialog) styles */
  ha-dialog {
    --mdc-dialog-min-width: 400px;
    --mdc-dialog-max-width: 600px;
    --mdc-dialog-max-width: min(600px, 95vw);
    --justify-action-buttons: space-between;
  }

  ha-dialog .form {
    color: var(--primary-text-color);
  }

  a {
    color: var(--primary-color);
  }

  /* make dialog fullscreen on small screens */
  @media all and (max-width: 450px), all and (max-height: 500px) {
    ha-dialog {
      --mdc-dialog-min-width: calc(
        100vw - var(--safe-area-inset-right) - var(--safe-area-inset-left)
      );
      --mdc-dialog-max-width: calc(
        100vw - var(--safe-area-inset-right) - var(--safe-area-inset-left)
      );
      --mdc-dialog-min-height: 100%;
      --mdc-dialog-max-height: 100%;
      --vertical-align-dialog: flex-end;
      --ha-dialog-border-radius: 0;
    }
  }
  .error {
    color: var(--error-color);
  }
`)),u=(0,o.iv)(n||(n=d`
  .ha-scrollbar::-webkit-scrollbar {
    width: 0.4rem;
    height: 0.4rem;
  }

  .ha-scrollbar::-webkit-scrollbar-thumb {
    -webkit-border-radius: 4px;
    border-radius: 4px;
    background: var(--scrollbar-thumb-color);
  }

  .ha-scrollbar {
    overflow-y: auto;
    scrollbar-color: var(--scrollbar-thumb-color) transparent;
    scrollbar-width: thin;
  }
`));(0,o.iv)(l||(l=d`
  body {
    background-color: var(--primary-background-color);
    color: var(--primary-text-color);
    height: calc(100vh - 32px);
    width: 100vw;
  }
`))},46919:function(e,t,i){i.a(e,(async function(e,o){try{i.d(t,{I:function(){return v}});var a=i(59048),r=(i(22543),i(13965),i(86932),i(24085)),s=i(10667),n=i(95409),l=i(22076),d=i(14511),c=e([r,s,n]);[r,s,n]=c.then?(await c)():c;let h,p,u=e=>e;const v=(e,t,i,o,r=e=>e)=>{var s,n;const c=t.device_info?(0,l.Q8)(e,t.device_info):void 0,v=c?null!==(s=c.name_by_user)&&void 0!==s?s:c.name:"",b=(0,d.T)(o);return(0,a.dy)(h||(h=u`
    <ha-card outlined>
      <h1 class="card-header">${0}</h1>
      <p class="card-content">${0}</p>
      ${0}
      <ha-expansion-panel
        header=${0}
        secondary=${0}
        expanded
        .noCollapse=${0}
      >
        <knx-device-picker
          .hass=${0}
          .key=${0}
          .helper=${0}
          .value=${0}
          @value-changed=${0}
        ></knx-device-picker>
        <ha-selector-text
          .hass=${0}
          label=${0}
          helper=${0}
          .required=${0}
          .selector=${0}
          .key=${0}
          .value=${0}
          @value-changed=${0}
        ></ha-selector-text>
      </ha-expansion-panel>
      <ha-expansion-panel .header=${0} outlined>
        <ha-selector-select
          .hass=${0}
          .label=${0}
          .helper=${0}
          .required=${0}
          .selector=${0}
          .key=${0}
          .value=${0}
          @value-changed=${0}
        ></ha-selector-select>
      </ha-expansion-panel>
    </ha-card>
  `),r("entity.title"),r("entity.description"),o&&b?(0,a.dy)(p||(p=u`<ha-alert
              .alertType=${0}
              .title=${0}
            ></ha-alert>`),"error",b.error_message):a.Ld,r("entity.name_title"),r("entity.name_description"),!0,e,"entity.device_info",r("entity.device_description"),null!==(n=t.device_info)&&void 0!==n?n:void 0,i,e,r("entity.entity_label"),r("entity.entity_description"),!c,{text:{type:"text",prefix:v}},"entity.name",t.name,i,r("entity.entity_category_title"),e,r("entity.entity_category_title"),r("entity.entity_category_description"),!1,{select:{multiple:!1,custom_value:!1,mode:"dropdown",options:[{value:"config",label:e.localize("ui.panel.config.devices.entities.config")},{value:"diagnostic",label:e.localize("ui.panel.config.devices.entities.diagnostic")}]}},"entity.entity_category",t.entity_category,i)};o()}catch(h){o(h)}}))},25121:function(e,t,i){i.a(e,(async function(e,t){try{i(39710),i(26847),i(2394),i(81738),i(33480),i(22960),i(6989),i(72489),i(18514),i(70820),i(64455),i(56303),i(41381),i(27530),i(73249),i(36330),i(38221),i(75863);var o=i(73742),a=i(59048),r=i(7616),s=i(20480),n=(i(22543),i(13965),i(91577),i(40830),i(86932),i(32986),i(14891),i(51597)),l=i(29740),d=i(74037),c=(i(30702),i(11675)),h=i(46919),p=i(38059),u=i(91447),v=i(14511),b=i(67388),_=e([d,c,b,h]);[d,c,b,h]=_.then?(await _)():_;let g,m,y,f,x,$,w,C,k,V,L,S=e=>e;const B=new p.r("knx-configure-entity");class O extends a.oi{connectedCallback(){if(super.connectedCallback(),this.platformStyle=(0,b.s)(this.platform),!this.config){this.config={entity:{},knx:{}};const e=new URLSearchParams(n.E.location.search),t=Object.fromEntries(e.entries());for(const[i,o]of Object.entries(t))(0,u.Q)(this.config,i,o,B),(0,l.B)(this,"knx-entity-configuration-changed",this.config)}}render(){var e;const t=(0,v._)(this.validationErrors,"data"),i=(0,v._)(t,"knx"),o=(0,v.T)(i);return(0,a.dy)(g||(g=S`
      <div class="header">
        <h1>
          <ha-svg-icon
            .path=${0}
            style=${0}
          ></ha-svg-icon>
          ${0}
        </h1>
        <p>${0}</p>
      </div>
      <slot name="knx-validation-error"></slot>
      <ha-card outlined>
        <h1 class="card-header">${0}</h1>
        ${0}
        ${0}
      </ha-card>
      ${0}
    `),this.platformStyle.iconPath,(0,s.V)({"background-color":this.platformStyle.color}),this.hass.localize(`component.${this.platform}.title`)||this.platform,this._backendLocalize("description"),this._backendLocalize("knx.title"),o?(0,a.dy)(m||(m=S`<ha-alert .alertType=${0} .title=${0}></ha-alert>`),"error",o.error_message):a.Ld,this.generateRootGroups(this.schema,i),(0,h.I)(this.hass,null!==(e=this.config.entity)&&void 0!==e?e:{},this._updateConfig,(0,v._)(t,"entity"),this._backendLocalize))}generateRootGroups(e,t){return this._generateItems(e,"knx",t)}_generateSection(e,t,i){const o=(0,v.T)(i);return(0,a.dy)(y||(y=S` <ha-expansion-panel
      .header=${0}
      .secondary=${0}
      .expanded=${0}
      .noCollapse=${0}
      .outlined=${0}
    >
      ${0}
      ${0}
    </ha-expansion-panel>`),this._backendLocalize(`${t}.title`),this._backendLocalize(`${t}.description`),!e.collapsible||this._groupHasGroupAddressInConfig(e,t),!e.collapsible,!!e.collapsible,o?(0,a.dy)(f||(f=S` <ha-alert .alertType=${0} .title=${0}>
            ${0}
          </ha-alert>`),"error","Validation error",o.error_message):a.Ld,this._generateItems(e.schema,t,i))}_generateGroupSelect(e,t,i){t in this._selectedGroupSelectOptions||(this._selectedGroupSelectOptions[t]=this._getOptionIndex(e,t));const o=this._selectedGroupSelectOptions[t],r=e.schema[o];void 0===r&&B.error("No option for index",o,e.schema);const s=e.schema.map(((e,i)=>({value:i.toString(),label:this._backendLocalize(`${t}.options.${e.translation_key}.label`)})));return(0,a.dy)(x||(x=S` <ha-expansion-panel
      .header=${0}
      .secondary=${0}
      .expanded=${0}
      .noCollapse=${0}
      .outlined=${0}
    >
      <ha-control-select
        .options=${0}
        .value=${0}
        .key=${0}
        @value-changed=${0}
      ></ha-control-select>
      ${0}
    </ha-expansion-panel>`),this._backendLocalize(`${t}.title`),this._backendLocalize(`${t}.description`),!e.collapsible||this._groupHasGroupAddressInConfig(e,t),!e.collapsible,!!e.collapsible,s,o.toString(),t,this._updateGroupSelectOption,r?(0,a.dy)($||($=S` <p class="group-description">
              ${0}
            </p>
            <div class="group-selection">
              ${0}
            </div>`),this._backendLocalize(`${t}.options.${r.translation_key}.description`),this._generateItems(r.schema,t,i)):a.Ld)}_generateItems(e,t,i){const o=[];let r,s=[];const n=()=>{if(0===s.length||void 0===r)return;const e=t+"."+r.name,n=!r.collapsible||s.some((e=>"knx_group_address"===e.type&&this._hasGroupAddressInConfig(e,t)));o.push((0,a.dy)(w||(w=S`<ha-expansion-panel
          .header=${0}
          .secondary=${0}
          .expanded=${0}
          .noCollapse=${0}
          .outlined=${0}
        >
          ${0}
        </ha-expansion-panel> `),this._backendLocalize(`${e}.title`),this._backendLocalize(`${e}.description`),n,!r.collapsible,!!r.collapsible,s.map((e=>this._generateItem(e,t,i))))),s=[]};for(const a of e)"knx_section_flat"!==a.type?(["knx_section","knx_group_select","knx_sync_state"].includes(a.type)&&(n(),r=void 0),void 0===r?o.push(this._generateItem(a,t,i)):s.push(a)):(n(),r=a);return n(),o}_generateItem(e,t,i){var o,r;const s=t+"."+e.name,n=(0,v._)(i,e.name);switch(e.type){case"knx_section":return this._generateSection(e,s,n);case"knx_group_select":return this._generateGroupSelect(e,s,n);case"knx_group_address":return(0,a.dy)(C||(C=S`
          <knx-group-address-selector
            .hass=${0}
            .knx=${0}
            .key=${0}
            .label=${0}
            .config=${0}
            .options=${0}
            .validationErrors=${0}
            .localizeFunction=${0}
            @value-changed=${0}
          ></knx-group-address-selector>
        `),this.hass,this.knx,s,this._backendLocalize(`${s}.label`),null!==(o=(0,u.q)(this.config,s))&&void 0!==o?o:{},e.options,n,this._backendLocalize,this._updateConfig);case"knx_sync_state":return(0,a.dy)(k||(k=S`
          <ha-expansion-panel
            .header=${0}
            .secondary=${0}
            .outlined=${0}
          >
            <knx-sync-state-selector-row
              .hass=${0}
              .key=${0}
              .value=${0}
              .allowFalse=${0}
              .localizeFunction=${0}
              @value-changed=${0}
            ></knx-sync-state-selector-row>
          </ha-expansion-panel>
        `),this._backendLocalize(`${s}.title`),this._backendLocalize(`${s}.description`),!0,this.hass,s,null===(r=(0,u.q)(this.config,s))||void 0===r||r,e.allow_false,this._backendLocalize,this._updateConfig);case"ha_selector":return(0,a.dy)(V||(V=S`
          <knx-selector-row
            .hass=${0}
            .key=${0}
            .selector=${0}
            .value=${0}
            .validationErrors=${0}
            .localizeFunction=${0}
            @value-changed=${0}
          ></knx-selector-row>
        `),this.hass,s,e,(0,u.q)(this.config,s),n,this._backendLocalize,this._updateConfig);default:return B.error("Unknown selector type",e),a.Ld}}_groupHasGroupAddressInConfig(e,t){return void 0!==this.config&&("knx_group_select"===e.type?!!(0,u.q)(this.config,t):e.schema.some((e=>{if("knx_group_address"===e.type)return this._hasGroupAddressInConfig(e,t);if("knx_section"===e.type||"knx_group_select"===e.type){const i=t+"."+e.name;return this._groupHasGroupAddressInConfig(e,i)}return!1})))}_hasGroupAddressInConfig(e,t){var i;const o=(0,u.q)(this.config,t+"."+e.name);return!!o&&(void 0!==o.write||(void 0!==o.state||!(null===(i=o.passive)||void 0===i||!i.length)))}_getRequiredKeys(e){const t=[];return e.forEach((e=>{"knx_section"!==e.type?("knx_group_address"===e.type&&e.required||"ha_selector"===e.type&&e.required)&&t.push(e.name):t.push(...this._getRequiredKeys(e.schema))})),t}_getOptionIndex(e,t){const i=(0,u.q)(this.config,t);if(void 0===i)return B.debug("No config found for group select",t),0;const o=e.schema.findIndex((e=>{const o=this._getRequiredKeys(e.schema);return 0===o.length?(B.warn("No required keys for GroupSelect option",t,e),!1):o.every((e=>e in i))}));return-1===o?(B.debug("No valid option found for group select",t,i),0):o}_updateGroupSelectOption(e){e.stopPropagation();const t=e.target.key,i=parseInt(e.detail.value,10);(0,u.Q)(this.config,t,void 0,B),this._selectedGroupSelectOptions[t]=i,(0,l.B)(this,"knx-entity-configuration-changed",this.config),this.requestUpdate()}_updateConfig(e){e.stopPropagation();const t=e.target.key,i=e.detail.value;(0,u.Q)(this.config,t,i,B),(0,l.B)(this,"knx-entity-configuration-changed",this.config),this.requestUpdate()}constructor(...e){super(...e),this._selectedGroupSelectOptions={},this._backendLocalize=e=>this.hass.localize(`component.knx.config_panel.entities.create.${this.platform}.${e}`)||this.hass.localize(`component.knx.config_panel.entities.create._.${e}`)}}O.styles=(0,a.iv)(L||(L=S`
    p {
      color: var(--secondary-text-color);
    }

    .header {
      color: var(--ha-card-header-color, --primary-text-color);
      font-family: var(--ha-card-header-font-family, inherit);
      padding: 0 16px 16px;

      & h1 {
        display: inline-flex;
        align-items: center;
        font-size: 26px;
        letter-spacing: -0.012em;
        line-height: 48px;
        font-weight: normal;
        margin-bottom: 14px;

        & ha-svg-icon {
          color: var(--text-primary-color);
          padding: 8px;
          background-color: var(--blue-color);
          border-radius: 50%;
          margin-right: 8px;
        }
      }

      & p {
        margin-top: -8px;
        line-height: 24px;
      }
    }

    ::slotted(ha-alert) {
      margin-top: 0 !important;
    }

    ha-card {
      margin-bottom: 24px;
      padding: 16px;

      & .card-header {
        display: inline-flex;
        align-items: center;
      }
    }

    ha-expansion-panel {
      margin-bottom: 16px;
    }
    ha-expansion-panel > :first-child:not(ha-settings-row) {
      margin-top: 16px; /* ha-settings-row has this margin internally */
    }
    ha-expansion-panel > ha-settings-row:first-child,
    ha-expansion-panel > knx-selector-row:first-child {
      border: 0;
    }
    ha-expansion-panel > * {
      margin-left: 8px;
      margin-right: 8px;
    }

    ha-settings-row {
      margin-bottom: 8px;
      padding: 0;
    }
    ha-control-select {
      padding: 0;
      margin-left: 0;
      margin-right: 0;
      margin-bottom: 16px;
    }

    .group-description {
      align-items: center;
      margin-top: -8px;
      padding-left: 8px;
      padding-bottom: 8px;
    }

    .group-selection {
      padding-left: 8px;
      padding-right: 8px;
      & ha-settings-row:first-child {
        border-top: 0;
      }
    }

    knx-group-address-selector,
    ha-selector,
    ha-selector-text,
    ha-selector-select,
    knx-sync-state-selector-row,
    knx-device-picker {
      display: block;
      margin-bottom: 16px;
    }

    ha-alert {
      display: block;
      margin: 20px auto;
      max-width: 720px;

      & summary {
        padding: 10px;
      }
    }
  `)),(0,o.__decorate)([(0,r.Cb)({attribute:!1})],O.prototype,"hass",void 0),(0,o.__decorate)([(0,r.Cb)({attribute:!1})],O.prototype,"knx",void 0),(0,o.__decorate)([(0,r.Cb)({attribute:!1})],O.prototype,"platform",void 0),(0,o.__decorate)([(0,r.Cb)({attribute:!1})],O.prototype,"config",void 0),(0,o.__decorate)([(0,r.Cb)({attribute:!1})],O.prototype,"schema",void 0),(0,o.__decorate)([(0,r.Cb)({attribute:!1})],O.prototype,"validationErrors",void 0),(0,o.__decorate)([(0,r.SB)()],O.prototype,"_selectedGroupSelectOptions",void 0),O=(0,o.__decorate)([(0,r.Mo)("knx-configure-entity")],O),t()}catch(g){t(g)}}))},95409:function(e,t,i){i.a(e,(async function(e,t){try{i(39710),i(26847),i(18574),i(81738),i(29981),i(6989),i(1455),i(27530);var o=i(73742),a=i(59048),r=i(7616),s=i(31733),n=i(28105),l=i(54693),d=(i(93795),i(65894)),c=i(29740),h=i(39186),p=i(92949),u=i(22076),v=e([l,d]);[l,d]=v.then?(await v)():v;let b,_,g,m=e=>e;const y=e=>(0,a.dy)(b||(b=m`<ha-list-item
    class=${0}
    .twoline=${0}
  >
    <span>${0}</span>
    <span slot="secondary">${0}</span>
  </ha-list-item>`),(0,s.$)({"add-new":"add_new"===e.id}),!!e.area,e.name,e.area);class f extends a.oi{async _addDevice(e){const t=[...(0,u.kc)(this.hass),e],i=this._getDevices(t,this.hass.areas);this.comboBox.items=i,this.comboBox.filteredItems=i,await this.updateComplete,await this.comboBox.updateComplete}async open(){var e;await this.updateComplete,await(null===(e=this.comboBox)||void 0===e?void 0:e.open())}async focus(){var e;await this.updateComplete,await(null===(e=this.comboBox)||void 0===e?void 0:e.focus())}updated(e){if(!this._init&&this.hass||this._init&&e.has("_opened")&&this._opened){var t;this._init=!0;const e=this._getDevices((0,u.kc)(this.hass),this.hass.areas),i=this.value?null===(t=e.find((e=>e.identifier===this.value)))||void 0===t?void 0:t.id:void 0;this.comboBox.value=i,this._deviceId=i,this.comboBox.items=e,this.comboBox.filteredItems=e}}render(){return(0,a.dy)(_||(_=m`
      <ha-combo-box
        .hass=${0}
        .label=${0}
        .helper=${0}
        .value=${0}
        .renderer=${0}
        item-id-path="id"
        item-value-path="id"
        item-label-path="name"
        @filter-changed=${0}
        @opened-changed=${0}
        @value-changed=${0}
      ></ha-combo-box>
      ${0}
    `),this.hass,void 0===this.label&&this.hass?this.hass.localize("ui.components.device-picker.device"):this.label,this.helper,this._deviceId,y,this._filterChanged,this._openedChanged,this._deviceChanged,this._showCreateDeviceDialog?this._renderCreateDeviceDialog():a.Ld)}_filterChanged(e){const t=e.target,i=e.detail.value;if(!i)return void(this.comboBox.filteredItems=this.comboBox.items);const o=(0,h.q)(i,t.items||[]);this._suggestion=i,this.comboBox.filteredItems=[...o,{id:"add_new_suggestion",name:`Add new device '${this._suggestion}'`}]}_openedChanged(e){this._opened=e.detail.value}_deviceChanged(e){e.stopPropagation();let t=e.detail.value;"no_devices"===t&&(t=""),["add_new_suggestion","add_new"].includes(t)?(e.target.value=this._deviceId,this._openCreateDeviceDialog()):t!==this._deviceId&&this._setValue(t)}_setValue(e){const t=this.comboBox.items.find((t=>t.id===e)),i=null==t?void 0:t.identifier;this.value=i,this._deviceId=null==t?void 0:t.id,setTimeout((()=>{(0,c.B)(this,"value-changed",{value:i}),(0,c.B)(this,"change")}),0)}_renderCreateDeviceDialog(){return(0,a.dy)(g||(g=m`
      <knx-device-create-dialog
        .hass=${0}
        @create-device-dialog-closed=${0}
        .deviceName=${0}
      ></knx-device-create-dialog>
    `),this.hass,this._closeCreateDeviceDialog,this._suggestion)}_openCreateDeviceDialog(){this._showCreateDeviceDialog=!0}async _closeCreateDeviceDialog(e){const t=e.detail.newDevice;t?await this._addDevice(t):this.comboBox.setInputValue(""),this._setValue(null==t?void 0:t.id),this._suggestion=void 0,this._showCreateDeviceDialog=!1}constructor(...e){super(...e),this._showCreateDeviceDialog=!1,this._init=!1,this._getDevices=(0,n.Z)(((e,t)=>[{id:"add_new",name:"Add new device…",area:"",strings:[]},...e.map((e=>{var i,o;const a=null!==(i=null!==(o=e.name_by_user)&&void 0!==o?o:e.name)&&void 0!==i?i:"";return{id:e.id,identifier:(0,u.cG)(e),name:a,area:e.area_id&&t[e.area_id]?t[e.area_id].name:this.hass.localize("ui.components.device-picker.no_area"),strings:[a||""]}})).sort(((e,t)=>(0,p.$K)(e.name||"",t.name||"",this.hass.locale.language)))]))}}(0,o.__decorate)([(0,r.Cb)({attribute:!1})],f.prototype,"hass",void 0),(0,o.__decorate)([(0,r.Cb)()],f.prototype,"label",void 0),(0,o.__decorate)([(0,r.Cb)()],f.prototype,"helper",void 0),(0,o.__decorate)([(0,r.Cb)()],f.prototype,"value",void 0),(0,o.__decorate)([(0,r.SB)()],f.prototype,"_opened",void 0),(0,o.__decorate)([(0,r.IO)("ha-combo-box",!0)],f.prototype,"comboBox",void 0),(0,o.__decorate)([(0,r.SB)()],f.prototype,"_showCreateDeviceDialog",void 0),f=(0,o.__decorate)([(0,r.Mo)("knx-device-picker")],f),t()}catch(b){t(b)}}))},63840:function(e,t,i){i(26847),i(81738),i(6989),i(27530);var o=i(73742),a=i(59048),r=i(7616),s=(i(74207),i(71308),i(29740));let n,l,d,c,h=e=>e;class p extends a.oi{render(){var e;return(0,a.dy)(n||(n=h`
      <div>
        ${0}
        ${0}
        ${0}
      </div>
    `),null!==(e=this.label)&&void 0!==e?e:a.Ld,this.options.map((e=>(0,a.dy)(l||(l=h`
            <div class="formfield">
              <ha-radio
                .checked=${0}
                .value=${0}
                .disabled=${0}
                @change=${0}
              ></ha-radio>
              <label .value=${0} @click=${0}>
                <p>
                  ${0}
                </p>
                <p class="secondary">DPT ${0}</p>
              </label>
            </div>
          `),e.value===this.value,e.value,this.disabled,this._valueChanged,e.value,this._valueChanged,this.localizeValue(this.translation_key+".options."+e.translation_key),e.value))),this.invalidMessage?(0,a.dy)(d||(d=h`<p class="invalid-message">${0}</p>`),this.invalidMessage):a.Ld)}_valueChanged(e){var t;e.stopPropagation();const i=e.target.value;this.disabled||void 0===i||i===(null!==(t=this.value)&&void 0!==t?t:"")||(0,s.B)(this,"value-changed",{value:i})}constructor(...e){super(...e),this.disabled=!1,this.invalid=!1,this.localizeValue=e=>e}}p.styles=[(0,a.iv)(c||(c=h`
      :host([invalid]) div {
        color: var(--error-color);
      }

      .formfield {
        display: flex;
        align-items: center;
      }

      label {
        min-width: 200px; /* to make it easier to click */
      }

      p {
        pointer-events: none;
        color: var(--primary-text-color);
        margin: 0px;
      }

      .secondary {
        padding-top: 4px;
        font-family: var(
          --mdc-typography-body2-font-family,
          var(--mdc-typography-font-family, Roboto, sans-serif)
        );
        -webkit-font-smoothing: antialiased;
        font-size: var(--mdc-typography-body2-font-size, 0.875rem);
        font-weight: var(--mdc-typography-body2-font-weight, 400);
        line-height: normal;
        color: var(--secondary-text-color);
      }

      .invalid-message {
        font-size: 0.75rem;
        color: var(--error-color);
        padding-left: 16px;
      }
    `))],(0,o.__decorate)([(0,r.Cb)({type:Array})],p.prototype,"options",void 0),(0,o.__decorate)([(0,r.Cb)()],p.prototype,"value",void 0),(0,o.__decorate)([(0,r.Cb)()],p.prototype,"label",void 0),(0,o.__decorate)([(0,r.Cb)({type:Boolean})],p.prototype,"disabled",void 0),(0,o.__decorate)([(0,r.Cb)({type:Boolean,reflect:!0})],p.prototype,"invalid",void 0),(0,o.__decorate)([(0,r.Cb)({attribute:!1})],p.prototype,"invalidMessage",void 0),(0,o.__decorate)([(0,r.Cb)({attribute:!1})],p.prototype,"localizeValue",void 0),(0,o.__decorate)([(0,r.Cb)({type:String})],p.prototype,"translation_key",void 0),p=(0,o.__decorate)([(0,r.Mo)("knx-dpt-selector")],p)},74037:function(e,t,i){i.a(e,(async function(e,t){try{i(39710),i(26847),i(81738),i(33480),i(94814),i(29981),i(22960),i(6989),i(87799),i(1455),i(56389),i(27530);var o=i(73742),a=i(59048),r=i(7616),s=i(31733),n=i(72644),l=i(28105),d=(i(93795),i(24085)),c=(i(78645),i(29740)),h=(i(63840),i(46350)),p=i(86662),u=i(14511),v=i(65793),b=e([d]);d=(b.then?(await b)():b)[0];let _,g,m,y,f,x,$,w=e=>e;const C="M7.41,8.58L12,13.17L16.59,8.58L18,10L12,16L6,10L7.41,8.58Z",k="M7.41,15.41L12,10.83L16.59,15.41L18,14L12,8L6,14L7.41,15.41Z",V="M11,15H13V17H11V15M11,7H13V13H11V7M12,2C6.47,2 2,6.5 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M12,20A8,8 0 0,1 4,12A8,8 0 0,1 12,4A8,8 0 0,1 20,12A8,8 0 0,1 12,20Z",L=e=>e.map((e=>({value:e.address,label:`${e.address} - ${e.name}`})));class S extends a.oi{getValidGroupAddresses(e){return this.knx.projectData?Object.values(this.knx.projectData.group_addresses).filter((t=>!!t.dpt&&(0,p.nK)(t.dpt,e))):[]}getDptOptionByValue(e){var t;return e?null===(t=this.options.dptSelect)||void 0===t?void 0:t.find((t=>t.value===e)):void 0}connectedCallback(){var e,t,i;super.connectedCallback(),this.validGroupAddresses=this.getValidGroupAddresses(null!==(e=null!==(t=this.options.validDPTs)&&void 0!==t?t:null===(i=this.options.dptSelect)||void 0===i?void 0:i.map((e=>e.dpt)))&&void 0!==e?e:[]),this.filteredGroupAddresses=this.validGroupAddresses,this.addressOptions=L(this.filteredGroupAddresses)}shouldUpdate(e){return!(1===e.size&&e.has("hass"))}willUpdate(e){var t;if(e.has("config")){var i,o;this._selectedDPTValue=null!==(i=this.config.dpt)&&void 0!==i?i:this._selectedDPTValue;const e=null===(o=this.getDptOptionByValue(this._selectedDPTValue))||void 0===o?void 0:o.dpt;if(this.setFilteredGroupAddresses(e),e&&this.knx.projectData){var a;const t=[this.config.write,this.config.state,...null!==(a=this.config.passive)&&void 0!==a?a:[]].filter((e=>null!=e));this.dptSelectorDisabled=t.length>0&&t.every((t=>{var i;const o=null===(i=this.knx.projectData.group_addresses[t])||void 0===i?void 0:i.dpt;return!!o&&(0,p.nK)(o,[e])}))}else this.dptSelectorDisabled=!1}this._validGADropTarget=null!==(t=this._dragDropContext)&&void 0!==t&&t.groupAddress?this.filteredGroupAddresses.includes(this._dragDropContext.groupAddress):void 0}updated(e){e.has("validationErrors")&&this._gaSelectors.forEach((async e=>{await e.updateComplete;const t=(0,u.T)(this.validationErrors,e.key);e.comboBox.errorMessage=null==t?void 0:t.error_message,e.comboBox.invalid=!!t}))}render(){const e=this.config.passive&&this.config.passive.length>0,t=!0===this._validGADropTarget,i=!1===this._validGADropTarget,o=(0,u.T)(this.validationErrors);return(0,a.dy)(_||(_=w`
      ${0}
      <div class="main">
        <div class="selectors">
          ${0}
          ${0}
        </div>
        <div class="options">
          <ha-icon-button
            .disabled=${0}
            .path=${0}
            .label=${0}
            @click=${0}
          ></ha-icon-button>
        </div>
      </div>
      <div
        class="passive ${0}"
        @transitionend=${0}
      >
        <ha-selector-select
          class=${0}
          .hass=${0}
          .label=${0}
          .required=${0}
          .selector=${0}
          .key=${0}
          .value=${0}
          @value-changed=${0}
          @dragover=${0}
          @drop=${0}
        ></ha-selector-select>
      </div>
      ${0}
      ${0}
    `),o?(0,a.dy)(g||(g=w`<p class="error">
            <ha-svg-icon .path=${0}></ha-svg-icon>
            <b>Validation error:</b>
            ${0}
          </p>`),V,o.error_message):a.Ld,this.options.write?(0,a.dy)(m||(m=w`<ha-selector-select
                class=${0}
                .hass=${0}
                .label=${0}
                .required=${0}
                .selector=${0}
                .key=${0}
                .value=${0}
                @value-changed=${0}
                @dragover=${0}
                @drop=${0}
              ></ha-selector-select>`),(0,s.$)({"valid-drop-zone":t,"invalid-drop-zone":i}),this.hass,this._baseTranslation("send_address")+(this.label?` - ${this.label}`:""),this.options.write.required,{select:{multiple:!1,custom_value:!0,options:this.addressOptions}},"write",this.config.write,this._updateConfig,this._dragOverHandler,this._dropHandler):a.Ld,this.options.state?(0,a.dy)(y||(y=w`<ha-selector-select
                class=${0}
                .hass=${0}
                .label=${0}
                .required=${0}
                .selector=${0}
                .key=${0}
                .value=${0}
                @value-changed=${0}
                @dragover=${0}
                @drop=${0}
              ></ha-selector-select>`),(0,s.$)({"valid-drop-zone":t,"invalid-drop-zone":i}),this.hass,this._baseTranslation("state_address")+(this.label?` - ${this.label}`:""),this.options.state.required,{select:{multiple:!1,custom_value:!0,options:this.addressOptions}},"state",this.config.state,this._updateConfig,this._dragOverHandler,this._dropHandler):a.Ld,!!e,this._showPassive?k:C,"Toggle passive address visibility",this._togglePassiveVisibility,(0,s.$)({expanded:e||this._showPassive}),this._handleTransitionEnd,(0,s.$)({"valid-drop-zone":t,"invalid-drop-zone":i}),this.hass,this._baseTranslation("passive_addresses")+(this.label?` - ${this.label}`:""),!1,{select:{multiple:!0,custom_value:!0,options:this.addressOptions}},"passive",this.config.passive,this._updateConfig,this._dragOverHandler,this._dropHandler,this.options.validDPTs?(0,a.dy)(f||(f=w`<p class="valid-dpts">
            ${0}:
            ${0}
          </p>`),this._baseTranslation("valid_dpts"),this.options.validDPTs.map((e=>(0,v.Wl)(e))).join(", ")):a.Ld,this.options.dptSelect?this._renderDptSelector():a.Ld)}_renderDptSelector(){const e=(0,u.T)(this.validationErrors,"dpt");return(0,a.dy)(x||(x=w`<knx-dpt-selector
      .key=${0}
      .label=${0}
      .options=${0}
      .value=${0}
      .disabled=${0}
      .invalid=${0}
      .invalidMessage=${0}
      .localizeValue=${0}
      .translation_key=${0}
      @value-changed=${0}
    >
    </knx-dpt-selector>`),"dpt",this._baseTranslation("dpt"),this.options.dptSelect,this._selectedDPTValue,this.dptSelectorDisabled,!!e,null==e?void 0:e.error_message,this.localizeFunction,this.key,this._updateConfig)}_updateConfig(e){var t;e.stopPropagation();const i=e.target,o=e.detail.value,a=Object.assign(Object.assign({},this.config),{},{[i.key]:o}),r=!!(a.write||a.state||null!==(t=a.passive)&&void 0!==t&&t.length);this._updateDptSelector(i.key,a,r),this.config=a;const s=r?a:void 0;(0,c.B)(this,"value-changed",{value:s}),this.requestUpdate()}_updateDptSelector(e,t,i){var o,a;if(!this.options.dptSelect)return;if("dpt"===e)this._selectedDPTValue=t.dpt;else{if(!i)return t.dpt=void 0,void(this._selectedDPTValue=void 0);t.dpt=this._selectedDPTValue}if(!this.knx.projectData)return;const r=this._getAddedGroupAddress(e,t);if(!r||void 0!==this._selectedDPTValue)return;const s=null===(o=this.validGroupAddresses.find((e=>e.address===r)))||void 0===o?void 0:o.dpt;if(!s)return;const n=this.options.dptSelect.find((e=>e.dpt.main===s.main&&e.dpt.sub===s.sub));t.dpt=n?n.value:null===(a=this.options.dptSelect.find((e=>(0,p.nK)(s,[e.dpt]))))||void 0===a?void 0:a.value}_getAddedGroupAddress(e,t){return"write"===e||"state"===e?t[e]:"passive"===e?null===(i=t.passive)||void 0===i?void 0:i.find((e=>{var t;return!(null!==(t=this.config.passive)&&void 0!==t&&t.includes(e))})):void 0;var i}_togglePassiveVisibility(e){e.stopPropagation(),e.preventDefault();const t=!this._showPassive;this._passiveContainer.style.overflow="hidden";const i=this._passiveContainer.scrollHeight;this._passiveContainer.style.height=`${i}px`,t||setTimeout((()=>{this._passiveContainer.style.height="0px"}),0),this._showPassive=t}_handleTransitionEnd(){this._passiveContainer.style.removeProperty("height"),this._passiveContainer.style.overflow=this._showPassive?"initial":"hidden"}_dragOverHandler(e){if(![...e.dataTransfer.types].includes("text/group-address"))return;e.preventDefault(),e.dataTransfer.dropEffect="move";const t=e.target;this._dragOverTimeout[t.key]?clearTimeout(this._dragOverTimeout[t.key]):t.classList.add("active-drop-zone"),this._dragOverTimeout[t.key]=setTimeout((()=>{delete this._dragOverTimeout[t.key],t.classList.remove("active-drop-zone")}),100)}_dropHandler(e){const t=e.dataTransfer.getData("text/group-address");if(!t)return;e.stopPropagation(),e.preventDefault();const i=e.target,o=Object.assign({},this.config);if(i.selector.select.multiple){var a;const e=[...null!==(a=this.config[i.key])&&void 0!==a?a:[],t];o[i.key]=e}else o[i.key]=t;this._updateDptSelector(i.key,o),(0,c.B)(this,"value-changed",{value:o}),setTimeout((()=>i.comboBox._inputElement.blur()))}constructor(...e){super(...e),this.config={},this.localizeFunction=e=>e,this._showPassive=!1,this.validGroupAddresses=[],this.filteredGroupAddresses=[],this.addressOptions=[],this.dptSelectorDisabled=!1,this._dragOverTimeout={},this._baseTranslation=e=>this.hass.localize(`component.knx.config_panel.entities.create._.knx.knx_group_address.${e}`),this.setFilteredGroupAddresses=(0,l.Z)((e=>{this.filteredGroupAddresses=e?this.getValidGroupAddresses([e]):this.validGroupAddresses,this.addressOptions=L(this.filteredGroupAddresses)}))}}S.styles=(0,a.iv)($||($=w`
    .main {
      display: flex;
      flex-direction: row;
    }

    .selectors {
      flex: 1;
      padding-right: 16px;
    }

    .options {
      width: 48px;
      display: flex;
      flex-direction: column-reverse;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 16px;
    }

    .passive {
      overflow: hidden;
      transition: height 150ms cubic-bezier(0.4, 0, 0.2, 1);
      height: 0px;
      margin-right: 64px; /* compensate for .options */
    }

    .passive.expanded {
      height: auto;
    }

    .valid-dpts {
      margin-top: 0;
      margin-left: 16px;
      margin-right: 64px;
      color: var(--secondary-text-color);
      font-size: var(--ha-font-size-s);
      font-weight: var(--ha-font-weight-medium);
    }

    ha-selector-select {
      display: block;
      margin-bottom: 16px;
      transition:
        box-shadow 250ms,
        opacity 250ms;
    }

    .valid-drop-zone {
      box-shadow: 0px 0px 5px 2px rgba(var(--rgb-primary-color), 0.5);
    }

    .valid-drop-zone.active-drop-zone {
      box-shadow: 0px 0px 5px 2px var(--primary-color);
    }

    .invalid-drop-zone {
      opacity: 0.5;
    }

    .invalid-drop-zone.active-drop-zone {
      box-shadow: 0px 0px 5px 2px var(--error-color);
    }

    .error {
      color: var(--error-color);
    }
  `)),(0,o.__decorate)([(0,n.F_)({context:h.R,subscribe:!0})],S.prototype,"_dragDropContext",void 0),(0,o.__decorate)([(0,r.Cb)({attribute:!1})],S.prototype,"hass",void 0),(0,o.__decorate)([(0,r.Cb)({attribute:!1})],S.prototype,"knx",void 0),(0,o.__decorate)([(0,r.Cb)()],S.prototype,"label",void 0),(0,o.__decorate)([(0,r.Cb)({attribute:!1})],S.prototype,"config",void 0),(0,o.__decorate)([(0,r.Cb)({attribute:!1})],S.prototype,"options",void 0),(0,o.__decorate)([(0,r.Cb)({reflect:!0})],S.prototype,"key",void 0),(0,o.__decorate)([(0,r.Cb)({attribute:!1})],S.prototype,"validationErrors",void 0),(0,o.__decorate)([(0,r.Cb)({attribute:!1})],S.prototype,"localizeFunction",void 0),(0,o.__decorate)([(0,r.SB)()],S.prototype,"_showPassive",void 0),(0,o.__decorate)([(0,r.IO)(".passive")],S.prototype,"_passiveContainer",void 0),(0,o.__decorate)([(0,r.Kt)("ha-selector-select")],S.prototype,"_gaSelectors",void 0),S=(0,o.__decorate)([(0,r.Mo)("knx-group-address-selector")],S),t()}catch(_){t(_)}}))},93341:function(e,t,i){i(84730),i(26847),i(2394),i(44438),i(81738),i(94814),i(6989),i(93190),i(18514),i(64455),i(60142),i(38465),i(27530);var o=i(73742),a=i(59048),r=i(7616),s=i(88245),n=i(72644),l=(i(22543),i(40830),i(38059)),d=i(46350),c=i(86662),h=i(65793);let p,u,v,b,_,g,m,y,f,x,$,w,C,k,V=e=>e;const L=new l.r("knx-project-device-tree");class S extends a.oi{connectedCallback(){var e;super.connectedCallback();const t=null!==(e=this.validDPTs)&&void 0!==e&&e.length?(0,c.OJ)(this.data,this.validDPTs):this.data.communication_objects,i=Object.values(this.data.devices).map((e=>{const i=[],o=Object.fromEntries(Object.entries(e.channels).map((([e,t])=>[e,{name:t.name,comObjects:[]}])));for(const r of e.communication_object_ids){if(!(r in t))continue;const e=t[r];e.channel&&e.channel in o?o[e.channel].comObjects.push(e):i.push(e)}const a=Object.entries(o).reduce(((e,[t,i])=>(i.comObjects.length&&(e[t]=i),e)),{});return{ia:e.individual_address,name:e.name,manufacturer:e.manufacturer_name,description:e.description.split(/[\r\n]/,1)[0],noChannelComObjects:i,channels:a}}));this.deviceTree=i.filter((e=>!!e.noChannelComObjects.length||!!Object.keys(e.channels).length))}render(){return(0,a.dy)(p||(p=V`<div class="device-tree-view">
      ${0}
    </div>`),this._selectedDevice?this._renderSelectedDevice(this._selectedDevice):this._renderDevices())}_renderDevices(){return this.deviceTree.length?(0,a.dy)(v||(v=V`<ul class="devices">
      ${0}
    </ul>`),(0,s.r)(this.deviceTree,(e=>e.ia),(e=>(0,a.dy)(b||(b=V`<li class="clickable" @click=${0} .device=${0}>
            ${0}
          </li>`),this._selectDevice,e,this._renderDevice(e))))):(0,a.dy)(u||(u=V`<ha-alert alert-type="info">No suitable device found in project data.</ha-alert>`))}_renderDevice(e){return(0,a.dy)(_||(_=V`<div class="item">
      <span class="icon ia">
        <ha-svg-icon .path=${0}></ha-svg-icon>
        <span>${0}</span>
      </span>
      <div class="description">
        <p>${0}</p>
        <p>${0}</p>
        ${0}
      </div>
    </div>`),"M15,20A1,1 0 0,0 14,19H13V17H17A2,2 0 0,0 19,15V5A2,2 0 0,0 17,3H7A2,2 0 0,0 5,5V15A2,2 0 0,0 7,17H11V19H10A1,1 0 0,0 9,20H2V22H9A1,1 0 0,0 10,23H14A1,1 0 0,0 15,22H22V20H15M7,15V5H17V15H7Z",e.ia,e.manufacturer,e.name,e.description?(0,a.dy)(g||(g=V`<p>${0}</p>`),e.description):a.Ld)}_renderSelectedDevice(e){return(0,a.dy)(m||(m=V`<ul class="selected-device">
      <li class="back-item clickable" @click=${0}>
        <div class="item">
          <ha-svg-icon class="back-icon" .path=${0}></ha-svg-icon>
          ${0}
        </div>
      </li>
      ${0}
    </ul>`),this._selectDevice,"M20,11V13H8L13.5,18.5L12.08,19.92L4.16,12L12.08,4.08L13.5,5.5L8,11H20Z",this._renderDevice(e),this._renderChannels(e))}_renderChannels(e){return(0,a.dy)(y||(y=V`${0}
    ${0} `),this._renderComObjects(e.noChannelComObjects),(0,s.r)(Object.entries(e.channels),(([t,i])=>`${e.ia}_ch_${t}`),(([e,t])=>t.comObjects.length?(0,a.dy)(f||(f=V`<li class="channel">${0}</li>
              ${0}`),t.name,this._renderComObjects(t.comObjects)):a.Ld)))}_renderComObjects(e){return(0,a.dy)(x||(x=V`${0} `),(0,s.r)(e,(e=>`${e.device_address}_co_${e.number}`),(e=>{return(0,a.dy)($||($=V`<li class="com-object">
          <div class="item">
            <span class="icon co"
              ><ha-svg-icon .path=${0}></ha-svg-icon
              ><span>${0}</span></span
            >
            <div class="description">
              <p>
                ${0}${0}
              </p>
              <p class="co-info">${0}</p>
            </div>
          </div>
          <ul class="group-addresses">
            ${0}
          </ul>
        </li>`),"M22 12C22 6.5 17.5 2 12 2S2 6.5 2 12 6.5 22 12 22 22 17.5 22 12M15 6.5L18.5 10L15 13.5V11H11V9H15V6.5M9 17.5L5.5 14L9 10.5V13H13V15H9V17.5Z",e.number,e.text,e.function_text?" - "+e.function_text:"",`${(t=e.flags).read?"R":"–"} ${t.write?"W":"–"} ${t.transmit?"T":"–"} ${t.update?"U":"–"}`,this._renderGroupAddresses(e.group_address_links));var t})))}_renderGroupAddresses(e){const t=e.map((e=>this.data.group_addresses[e]));return(0,a.dy)(w||(w=V`${0} `),(0,s.r)(t,(e=>e.identifier),(e=>{var t,i,o,r,s,n;return(0,a.dy)(C||(C=V`<li
          draggable="true"
          @dragstart=${0}
          @dragend=${0}
          @mouseover=${0}
          @focus=${0}
          @mouseout=${0}
          @blur=${0}
          .ga=${0}
        >
          <div class="item">
            <ha-svg-icon
              class="drag-icon"
              .path=${0}
              .viewBox=${0}
            ></ha-svg-icon>
            <span class="icon ga">
              <span>${0}</span>
            </span>
            <div class="description">
              <p>${0}</p>
              <p class="ga-info">${0}</p>
            </div>
          </div>
        </li>`),null===(t=this._dragDropContext)||void 0===t?void 0:t.gaDragStartHandler,null===(i=this._dragDropContext)||void 0===i?void 0:i.gaDragEndHandler,null===(o=this._dragDropContext)||void 0===o?void 0:o.gaDragIndicatorStartHandler,null===(r=this._dragDropContext)||void 0===r?void 0:r.gaDragIndicatorStartHandler,null===(s=this._dragDropContext)||void 0===s?void 0:s.gaDragIndicatorEndHandler,null===(n=this._dragDropContext)||void 0===n?void 0:n.gaDragIndicatorEndHandler,e,"M9,3H11V5H9V3M13,3H15V5H13V3M9,7H11V9H9V7M13,7H15V9H13V7M9,11H11V13H9V11M13,11H15V13H13V11M9,15H11V17H9V15M13,15H15V17H13V15M9,19H11V21H9V19M13,19H15V21H13V19Z","4 0 16 24",e.address,e.name,(e=>{const t=(0,h.Wl)(e.dpt);return t?`DPT ${t}`:""})(e))})))}_selectDevice(e){const t=e.target.device;L.debug("select device",t),this._selectedDevice=t,this.scrollTop=0}constructor(...e){super(...e),this.deviceTree=[]}}S.styles=(0,a.iv)(k||(k=V`
    :host {
      display: block;
      box-sizing: border-box;
      margin: 0;
      height: 100%;
      overflow-y: scroll;
      overflow-x: hidden;
      background-color: var(--sidebar-background-color);
      color: var(--sidebar-menu-button-text-color, --primary-text-color);
      margin-right: env(safe-area-inset-right);
      border-left: 1px solid var(--divider-color);
      padding-left: 8px;
    }

    ha-alert {
      display: block;
      margin-right: 8px;
      margin-top: 8px;
    }

    ul {
      list-style-type: none;
      padding: 0;
      margin-block-start: 8px;
    }

    li {
      display: block;
      margin-bottom: 4px;
      & div.item {
        /* icon and text */
        display: flex;
        align-items: center;
        pointer-events: none;
        & > div {
          /* optional container for multiple paragraphs */
          min-width: 0;
          width: 100%;
        }
      }
    }

    li p {
      margin: 0;
      overflow: hidden;
      white-space: nowrap;
      text-overflow: ellipsis;
    }

    span.icon {
      flex: 0 0 auto;
      display: inline-flex;
      /* align-self: stretch; */
      align-items: center;

      color: var(--text-primary-color);
      font-size: 1rem;
      font-weight: 700;
      border-radius: 12px;
      padding: 3px 6px;
      margin-right: 4px;

      & > ha-svg-icon {
        float: left;
        width: 16px;
        height: 16px;
        margin-right: 4px;
      }

      & > span {
        /* icon text */
        flex: 1;
        text-align: center;
      }
    }

    span.ia {
      flex-basis: 70px;
      background-color: var(--label-badge-grey);
      & > ha-svg-icon {
        transform: rotate(90deg);
      }
    }

    span.co {
      flex-basis: 44px;
      background-color: var(--amber-color);
    }

    span.ga {
      flex-basis: 54px;
      background-color: var(--knx-green);
    }

    .description {
      margin-top: 4px;
      margin-bottom: 4px;
    }

    p.co-info,
    p.ga-info {
      font-size: 0.85rem;
      font-weight: 300;
    }

    .back-item {
      margin-left: -8px; /* revert host padding to have gapless border */
      padding-left: 8px;
      margin-top: -8px; /* revert ul margin-block-start to have gapless hover effect */
      padding-top: 8px;
      padding-bottom: 8px;
      border-bottom: 1px solid var(--divider-color);
      margin-bottom: 8px;
    }

    .back-icon {
      margin-right: 8px;
      color: var(--label-badge-grey);
    }

    li.channel {
      border-top: 1px solid var(--divider-color);
      border-bottom: 1px solid var(--divider-color);
      padding: 4px 16px;
      font-weight: 500;
    }

    li.clickable {
      cursor: pointer;
    }
    li.clickable:hover {
      background-color: rgba(var(--rgb-primary-text-color), 0.04);
    }

    li[draggable="true"] {
      cursor: grab;
    }
    li[draggable="true"]:hover {
      border-radius: 12px;
      background-color: rgba(var(--rgb-primary-color), 0.2);
    }

    ul.group-addresses {
      margin-top: 0;
      margin-bottom: 8px;

      & > li:not(:first-child) {
        /* passive addresses for this com-object */
        opacity: 0.8;
      }
    }
  `)),(0,o.__decorate)([(0,n.F_)({context:d.R})],S.prototype,"_dragDropContext",void 0),(0,o.__decorate)([(0,r.Cb)({attribute:!1})],S.prototype,"data",void 0),(0,o.__decorate)([(0,r.Cb)({attribute:!1})],S.prototype,"validDPTs",void 0),(0,o.__decorate)([(0,r.SB)()],S.prototype,"_selectedDevice",void 0),S=(0,o.__decorate)([(0,r.Mo)("knx-project-device-tree")],S)},30702:function(e,t,i){i(26847),i(27530);var o=i(73742),a=i(59048),r=i(7616),s=i(31733),n=i(29740),l=(i(86776),i(32986),i(4820),i(14511));let d,c,h,p,u,v=e=>e;class b extends a.oi{connectedCallback(){var e,t;super.connectedCallback(),this._disabled=!this.selector.required&&void 0===this.value,this._haSelectorValue=null!==(e=null!==(t=this.value)&&void 0!==t?t:this.selector.default)&&void 0!==e?e:null;const i="boolean"in this.selector.selector,o=i||"number"in this.selector.selector;this._inlineSelector=!!this.selector.required&&o,this._optionalBooleanSelector=!this.selector.required&&i,this._optionalBooleanSelector&&(this._haSelectorValue=!0)}render(){const e=(0,l.T)(this.validationErrors),t=this._optionalBooleanSelector?a.Ld:(0,a.dy)(d||(d=v`<ha-selector
          class=${0}
          .hass=${0}
          .selector=${0}
          .disabled=${0}
          .value=${0}
          @value-changed=${0}
        ></ha-selector>`),(0,s.$)({"newline-selector":!this._inlineSelector}),this.hass,this.selector.selector,this._disabled,this._haSelectorValue,this._valueChange);return(0,a.dy)(c||(c=v`
      <div class="body">
        <div class="text">
          <p class="heading ${0}">
            ${0}
          </p>
          <p class="description">${0}</p>
        </div>
        ${0}
        ${0}
      </div>
      ${0}
      ${0}
    `),(0,s.$)({invalid:!!e}),this.localizeFunction(`${this.key}.label`),this.localizeFunction(`${this.key}.description`),this.selector.required?a.Ld:(0,a.dy)(h||(h=v`<ha-selector
              class="optional-switch"
              .selector=${0}
              .value=${0}
              @value-changed=${0}
            ></ha-selector>`),{boolean:{}},!this._disabled,this._toggleDisabled),this._inlineSelector?t:a.Ld,this._inlineSelector?a.Ld:t,e?(0,a.dy)(p||(p=v`<p class="invalid-message">${0}</p>`),e.error_message):a.Ld)}_toggleDisabled(e){e.stopPropagation(),this._disabled=!this._disabled,this._propagateValue()}_valueChange(e){e.stopPropagation(),this._haSelectorValue=e.detail.value,this._propagateValue()}_propagateValue(){(0,n.B)(this,"value-changed",{value:this._disabled?void 0:this._haSelectorValue})}constructor(...e){super(...e),this.localizeFunction=e=>e,this._disabled=!1,this._haSelectorValue=null,this._inlineSelector=!1,this._optionalBooleanSelector=!1}}b.styles=(0,a.iv)(u||(u=v`
    :host {
      display: block;
      padding: 8px 16px 8px 0;
      border-top: 1px solid var(--divider-color);
    }
    .newline-selector {
      display: block;
      padding-top: 8px;
    }
    .body {
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      row-gap: 8px;
    }
    .body > * {
      flex-grow: 1;
    }
    .text {
      flex-basis: 260px; /* min size of text - if inline selector is too big it will be pushed to next row */
    }
    .heading {
      margin: 0;
    }
    .description {
      margin: 0;
      display: block;
      padding-top: 4px;
      font-family: var(
        --mdc-typography-body2-font-family,
        var(--mdc-typography-font-family, Roboto, sans-serif)
      );
      -webkit-font-smoothing: antialiased;
      font-size: var(--mdc-typography-body2-font-size, 0.875rem);
      font-weight: var(--mdc-typography-body2-font-weight, 400);
      line-height: normal;
      color: var(--secondary-text-color);
    }

    .invalid {
      color: var(--error-color);
    }
    .invalid-message {
      font-size: 0.75rem;
      color: var(--error-color);
      padding-left: 16px;
    }
  `)),(0,o.__decorate)([(0,r.Cb)({attribute:!1})],b.prototype,"hass",void 0),(0,o.__decorate)([(0,r.Cb)()],b.prototype,"key",void 0),(0,o.__decorate)([(0,r.Cb)({attribute:!1})],b.prototype,"selector",void 0),(0,o.__decorate)([(0,r.Cb)()],b.prototype,"value",void 0),(0,o.__decorate)([(0,r.Cb)({attribute:!1})],b.prototype,"validationErrors",void 0),(0,o.__decorate)([(0,r.Cb)({attribute:!1})],b.prototype,"localizeFunction",void 0),(0,o.__decorate)([(0,r.SB)()],b.prototype,"_disabled",void 0),b=(0,o.__decorate)([(0,r.Mo)("knx-selector-row")],b)},11675:function(e,t,i){i.a(e,(async function(e,t){try{i(26847),i(27530);var o=i(73742),a=i(59048),r=i(7616),s=i(29740),n=(i(69028),i(24085)),l=e([n]);n=(l.then?(await l)():l)[0];let d,c,h=e=>e;class p extends a.oi{get _options(){return this.allowFalse?[!0,"init","expire","every",!1]:[!0,"init","expire","every"]}_hasMinutes(e){return"expire"===e||"every"===e}willUpdate(){if("boolean"==typeof this.value)return void(this._strategy=this.value);const[e,t]=this.value.split(" ");this._strategy=e,+t&&(this._minutes=+t)}render(){return(0,a.dy)(d||(d=h` <div class="inline">
      <ha-selector-select
        .hass=${0}
        .label=${0}
        .localizeValue=${0}
        .selector=${0}
        .key=${0}
        .value=${0}
        @value-changed=${0}
      >
      </ha-selector-select>
      <ha-selector-number
        .hass=${0}
        .disabled=${0}
        .selector=${0}
        .key=${0}
        .value=${0}
        @value-changed=${0}
      >
      </ha-selector-number>
    </div>`),this.hass,this.localizeFunction(`${this.key}.title`),this.localizeFunction,{select:{translation_key:this.key,multiple:!1,custom_value:!1,mode:"dropdown",options:this._options}},"strategy",this._strategy,this._handleChange,this.hass,!this._hasMinutes(this._strategy),{number:{min:2,max:1440,step:1,unit_of_measurement:"minutes"}},"minutes",this._minutes,this._handleChange)}_handleChange(e){let t,i;e.stopPropagation(),"strategy"===e.target.key?(t=e.detail.value,i=this._minutes):(t=this._strategy,i=e.detail.value);const o=this._hasMinutes(t)?`${t} ${i}`:t;(0,s.B)(this,"value-changed",{value:o})}constructor(...e){super(...e),this.value=!0,this.key="sync_state",this.allowFalse=!1,this.localizeFunction=e=>e,this._strategy=!0,this._minutes=60}}p.styles=(0,a.iv)(c||(c=h`
    .description {
      margin: 0;
      display: block;
      padding-top: 4px;
      padding-bottom: 8px;
      font-family: var(
        --mdc-typography-body2-font-family,
        var(--mdc-typography-font-family, Roboto, sans-serif)
      );
      -webkit-font-smoothing: antialiased;
      font-size: var(--mdc-typography-body2-font-size, 0.875rem);
      font-weight: var(--mdc-typography-body2-font-weight, 400);
      line-height: normal;
      color: var(--secondary-text-color);
    }
    .inline {
      width: 100%;
      display: inline-flex;
      flex-flow: row wrap;
      gap: 16px;
      justify-content: space-between;
    }
    .inline > * {
      flex: 1;
      width: 100%; /* to not overflow when wrapped */
    }
  `)),(0,o.__decorate)([(0,r.Cb)({attribute:!1})],p.prototype,"hass",void 0),(0,o.__decorate)([(0,r.Cb)()],p.prototype,"value",void 0),(0,o.__decorate)([(0,r.Cb)()],p.prototype,"key",void 0),(0,o.__decorate)([(0,r.Cb)({attribute:!1})],p.prototype,"allowFalse",void 0),(0,o.__decorate)([(0,r.Cb)({attribute:!1})],p.prototype,"localizeFunction",void 0),p=(0,o.__decorate)([(0,r.Mo)("knx-sync-state-selector-row")],p),t()}catch(d){t(d)}}))},65894:function(e,t,i){i.a(e,(async function(e,t){try{i(1455),i(67496);var o=i(73742),a=i(59048),r=i(7616),s=i(29173),n=i(99495),l=(i(99298),i(30337)),d=i(10667),c=i(29740),h=i(77204),p=i(63279),u=i(38059),v=e([n,l,d]);[n,l,d]=v.then?(await v)():v;let b,_,g=e=>e;const m=new u.r("create_device_dialog");class y extends a.oi{closeDialog(e){(0,c.B)(this,"create-device-dialog-closed",{newDevice:this._deviceEntry},{bubbles:!1})}_createDevice(){(0,p.fM)(this.hass,{name:this.deviceName,area_id:this.area}).then((e=>{this._deviceEntry=e})).catch((e=>{m.error("getGroupMonitorInfo",e),(0,s.c)("/knx/error",{replace:!0,data:e})})).finally((()=>{this.closeDialog(void 0)}))}render(){return(0,a.dy)(b||(b=g`<ha-dialog
      open
      .heading=${0}
      scrimClickAction
      escapeKeyAction
      defaultAction="ignore"
    >
      <ha-selector-text
        .hass=${0}
        .label=${0}
        .required=${0}
        .selector=${0}
        .key=${0}
        .value=${0}
        @value-changed=${0}
      ></ha-selector-text>
      <ha-area-picker
        .hass=${0}
        .label=${0}
        .key=${0}
        .value=${0}
        @value-changed=${0}
      >
      </ha-area-picker>
      <ha-button slot="secondaryAction" @click=${0}>
        ${0}
      </ha-button>
      <ha-button slot="primaryAction" @click=${0}>
        ${0}
      </ha-button>
    </ha-dialog>`),"Create new device",this.hass,"Name",!0,{text:{}},"deviceName",this.deviceName,this._valueChanged,this.hass,"Area","area",this.area,this._valueChanged,this.closeDialog,this.hass.localize("ui.common.cancel"),this._createDevice,this.hass.localize("ui.common.add"))}_valueChanged(e){e.stopPropagation();const t=e.target;null!=t&&t.key&&(this[t.key]=e.detail.value)}static get styles(){return[h.yu,(0,a.iv)(_||(_=g`
        @media all and (min-width: 600px) {
          ha-dialog {
            --mdc-dialog-min-width: 480px;
          }
        }
      `))]}}(0,o.__decorate)([(0,r.Cb)({attribute:!1})],y.prototype,"hass",void 0),(0,o.__decorate)([(0,r.Cb)({attribute:!1})],y.prototype,"deviceName",void 0),(0,o.__decorate)([(0,r.SB)()],y.prototype,"area",void 0),y=(0,o.__decorate)([(0,r.Mo)("knx-device-create-dialog")],y),t()}catch(b){t(b)}}))},67388:function(e,t,i){i.a(e,(async function(e,o){try{i.d(t,{s:function(){return l}});i(87799);var a=i(54974),r=e([a]);a=(r.then?(await r)():r)[0];const n={binary_sensor:{iconPath:"M12 2C6.5 2 2 6.5 2 12S6.5 22 12 22 22 17.5 22 12 17.5 2 12 2M10 17L5 12L6.41 10.59L10 14.17L17.59 6.58L19 8L10 17Z",color:"var(--green-color)"},button:{iconPath:"M20 20.5C20 21.3 19.3 22 18.5 22H13C12.6 22 12.3 21.9 12 21.6L8 17.4L8.7 16.6C8.9 16.4 9.2 16.3 9.5 16.3H9.7L12 18V9C12 8.4 12.4 8 13 8S14 8.4 14 9V13.5L15.2 13.6L19.1 15.8C19.6 16 20 16.6 20 17.1V20.5M20 2H4C2.9 2 2 2.9 2 4V12C2 13.1 2.9 14 4 14H8V12H4V4H20V12H18V14H20C21.1 14 22 13.1 22 12V4C22 2.9 21.1 2 20 2Z",color:"var(--purple-color)"},climate:{color:"var(--red-color)"},cover:{iconPath:"M3 4H21V8H19V20H17V8H7V20H5V8H3V4M8 9H16V11H8V9M8 12H16V14H8V12M8 15H16V17H8V15M8 18H16V20H8V18Z",color:"var(--cyan-color)"},date:{color:"var(--lime-color)"},event:{iconPath:"M13 11H11V5H13M13 15H11V13H13M20 2H4C2.9 2 2 2.9 2 4V22L6 18H20C21.1 18 22 17.1 22 16V4C22 2.9 21.1 2 20 2Z",color:"var(--deep-orange-color)"},fan:{iconPath:"M12,11A1,1 0 0,0 11,12A1,1 0 0,0 12,13A1,1 0 0,0 13,12A1,1 0 0,0 12,11M12.5,2C17,2 17.11,5.57 14.75,6.75C13.76,7.24 13.32,8.29 13.13,9.22C13.61,9.42 14.03,9.73 14.35,10.13C18.05,8.13 22.03,8.92 22.03,12.5C22.03,17 18.46,17.1 17.28,14.73C16.78,13.74 15.72,13.3 14.79,13.11C14.59,13.59 14.28,14 13.88,14.34C15.87,18.03 15.08,22 11.5,22C7,22 6.91,18.42 9.27,17.24C10.25,16.75 10.69,15.71 10.89,14.79C10.4,14.59 9.97,14.27 9.65,13.87C5.96,15.85 2,15.07 2,11.5C2,7 5.56,6.89 6.74,9.26C7.24,10.25 8.29,10.68 9.22,10.87C9.41,10.39 9.73,9.97 10.14,9.65C8.15,5.96 8.94,2 12.5,2Z",color:"var(--light-grey-color)"},light:{color:"var(--amber-color)"},notify:{color:"var(--pink-color)"},number:{color:"var(--teal-color)"},scene:{color:"var(--deep-purple-color)"},select:{color:"var(--indigo-color)"},sensor:{color:"var(--orange-color)"},switch:{iconPath:"M18.4 1.6C18 1.2 17.5 1 17 1H7C6.5 1 6 1.2 5.6 1.6C5.2 2 5 2.5 5 3V21C5 21.5 5.2 22 5.6 22.4C6 22.8 6.5 23 7 23H17C17.5 23 18 22.8 18.4 22.4C18.8 22 19 21.5 19 21V3C19 2.5 18.8 2 18.4 1.6M16 7C16 7.6 15.6 8 15 8H9C8.4 8 8 7.6 8 7V5C8 4.4 8.4 4 9 4H15C15.6 4 16 4.4 16 5V7Z",color:"var(--blue-color)"},text:{color:"var(--brown-color)"},time:{color:"var(--light-green-color)"},valve:{iconPath:"M4 22H2V2H4M22 2H20V22H22M17.24 5.34L13.24 9.34A3 3 0 0 0 9.24 13.34L5.24 17.34L6.66 18.76L10.66 14.76A3 3 0 0 0 14.66 10.76L18.66 6.76Z",color:"var(--light-blue-color)"},weather:{color:"var(--yellow-color)"}};function l(e){return Object.assign({iconPath:a.Ls[e],color:"var(--dark-grey-color)"},n[e])}o()}catch(s){o(s)}}))},91447:function(e,t,i){i.d(t,{Q:function(){return o},q:function(){return a}});i(26847),i(27530);function o(e,t,i,a){const r=t.split("."),s=r.pop();if(!s)return;let n=e;for(const o of r){if(!(o in n)){if(void 0===i)return;n[o]={}}n=n[o]}void 0===i?(a&&a.debug(`remove ${s} at ${t}`),delete n[s],!Object.keys(n).length&&r.length>0&&o(e,r.join("."),void 0)):(a&&a.debug(`update ${s} at ${t} with value`,i),n[s]=i)}function a(e,t){const i=t.split(".");let o=e;for(const a of i){if(!(a in o))return;o=o[a]}return o}},22076:function(e,t,i){i.d(t,{Q8:function(){return s},cG:function(){return n},kc:function(){return r}});i(81738),i(94814),i(29981),i(72489);const o=e=>"knx"===e[0],a=e=>e.identifiers.some(o),r=e=>Object.values(e.devices).filter(a),s=(e,t)=>Object.values(e.devices).find((e=>e.identifiers.find((e=>o(e)&&e[1]===t)))),n=e=>{const t=e.identifiers.find(o);return t?t[1]:void 0}},86662:function(e,t,i){i.d(t,{OJ:function(){return r},nK:function(){return a},ts:function(){return n}});i(26847),i(2394),i(44438),i(81738),i(22960),i(6989),i(93190),i(72489),i(27530);var o=i(28105);const a=(e,t)=>t.some((t=>e.main===t.main&&(!t.sub||e.sub===t.sub))),r=(e,t)=>{const i=((e,t)=>Object.entries(e.group_addresses).reduce(((e,[i,o])=>(o.dpt&&a(o.dpt,t)&&(e[i]=o),e)),{}))(e,t);return Object.entries(e.communication_objects).reduce(((e,[t,o])=>(o.group_address_links.some((e=>e in i))&&(e[t]=o),e)),{})};function s(e){const t=[];return e.forEach((e=>{"knx_group_address"!==e.type?"schema"in e&&t.push(...s(e.schema)):e.options.validDPTs?t.push(...e.options.validDPTs):e.options.dptSelect&&t.push(...e.options.dptSelect.map((e=>e.dpt)))})),t}const n=(0,o.Z)((e=>s(e).reduce(((e,t)=>e.some((e=>{return o=t,(i=e).main===o.main&&i.sub===o.sub;var i,o}))?e:e.concat([t])),[])))},46350:function(e,t,i){i.d(t,{R:function(){return n},Z:function(){return s}});i(84730);var o=i(72644);const a=new(i(38059).r)("knx-drag-drop-context"),r=Symbol("drag-drop-context");class s{get groupAddress(){return this._groupAddress}constructor(e){this.gaDragStartHandler=e=>{var t;const i=e.target,o=i.ga;o?(this._groupAddress=o,a.debug("dragstart",o.address,this),null===(t=e.dataTransfer)||void 0===t||t.setData("text/group-address",o.address),this._updateObservers()):a.warn("dragstart: no 'ga' property found",i)},this.gaDragEndHandler=e=>{a.debug("dragend",this),this._groupAddress=void 0,this._updateObservers()},this.gaDragIndicatorStartHandler=e=>{const t=e.target.ga;t&&(this._groupAddress=t,a.debug("drag indicator start",t.address,this),this._updateObservers())},this.gaDragIndicatorEndHandler=e=>{a.debug("drag indicator end",this),this._groupAddress=void 0,this._updateObservers()},this._updateObservers=e}}const n=(0,o.kr)(r)},14511:function(e,t,i){i.d(t,{T:function(){return a},_:function(){return o}});i(26847),i(2394),i(81738),i(29981),i(87799),i(27530);const o=(e,t)=>{if(!e)return;const i=[];for(const o of e)if(o.path){const[e,...a]=o.path;e===t&&i.push(Object.assign(Object.assign({},o),{},{path:a}))}return i.length?i:void 0},a=(e,t=void 0)=>{var i;return t&&(e=o(e,t)),null===(i=e)||void 0===i?void 0:i.find((e=>{var t;return 0===(null===(t=e.path)||void 0===t?void 0:t.length)}))}},16931:function(e,t,i){i.a(e,(async function(e,o){try{i.r(t),i.d(t,{KNXCreateEntity:function(){return q}});i(40777),i(55619),i(39710),i(26847),i(81738),i(6989),i(1455),i(5458),i(56389),i(27530);var a=i(73742),r=i(59048),s=i(7616),n=i(72644),l=i(66842),d=i(86829),c=(i(56165),i(22543),i(13965),i(45222),i(40830),i(56884),i(29173)),h=i(51597),p=i(29740),u=i(48112),v=i(25121),b=(i(93341),i(63279)),_=i(67388),g=i(86662),m=i(46350),y=i(38059),f=e([d,v,_]);[d,v,_]=f.then?(await f)():f;let x,$,w,C,k,V,L,S,B,O,M,H,P,D,I,z,A=e=>e;const E="M19,13H13V19H11V13H5V11H11V5H13V11H19V13Z",j="M5,3A2,2 0 0,0 3,5V19A2,2 0 0,0 5,21H19A2,2 0 0,0 21,19V5.5L18.5,3H17V9A1,1 0 0,1 16,10H8A1,1 0 0,1 7,9V3H5M12,4V9H15V4H12M7,12H17A1,1 0 0,1 18,13V19H6V13A1,1 0 0,1 7,12Z",T=new y.r("knx-create-entity");class q extends r.oi{willUpdate(e){if(e.has("route")){const e=this.route.prefix.split("/").at(-1);if("create"!==e&&"edit"!==e)return T.error("Unknown intent",e),void(this._intent=void 0);this._intent=e,this._config=void 0,this._validationErrors=void 0,this._validationBaseError=void 0,"create"===e?(this.entityId=void 0,this.entityPlatform=this.route.path.split("/")[1]):"edit"===e&&(this.entityId=this.route.path.split("/")[1])}}render(){return this.hass&&this._intent?this._projectLoadTask.render({initial:()=>(0,r.dy)($||($=A`
        <hass-loading-screen .message=${0}></hass-loading-screen>
      `),"Waiting to fetch project data."),pending:()=>(0,r.dy)(w||(w=A`
        <hass-loading-screen .message=${0}></hass-loading-screen>
      `),"Loading KNX project data."),error:e=>this._renderError("Error loading KNX project",e),complete:()=>"edit"===this._intent?this._renderEdit():this._renderCreate()}):(0,r.dy)(x||(x=A` <hass-loading-screen></hass-loading-screen> `))}_renderCreate(){return this.entityPlatform?this.knx.supportedPlatforms.includes(this.entityPlatform)?this._renderLoadSchema():(T.error("Unknown platform",this.entityPlatform),this._renderTypeSelection()):this._renderTypeSelection()}_renderEdit(){return this._entityConfigLoadTask.render({initial:()=>(0,r.dy)(C||(C=A`
        <hass-loading-screen .message=${0}></hass-loading-screen>
      `),"Waiting to fetch entity data."),pending:()=>(0,r.dy)(k||(k=A`
        <hass-loading-screen .message=${0}></hass-loading-screen>
      `),"Loading entity data."),error:e=>this._renderError((0,r.dy)(V||(V=A`${0}:
            <code>${0}</code>`),this.hass.localize("ui.card.common.entity_not_found"),this.entityId),e),complete:()=>this.entityPlatform?this.knx.supportedPlatforms.includes(this.entityPlatform)?this._renderLoadSchema():this._renderError("Unsupported platform","Unsupported platform: "+this.entityPlatform):this._renderError((0,r.dy)(L||(L=A`${0}:
              <code>${0}</code>`),this.hass.localize("ui.card.common.entity_not_found"),this.entityId),new Error("Entity platform unknown"))})}_renderLoadSchema(){return this._schemaLoadTask.render({initial:()=>(0,r.dy)(S||(S=A`
        <hass-loading-screen .message=${0}></hass-loading-screen>
      `),"Waiting to fetch schema."),pending:()=>(0,r.dy)(B||(B=A`
        <hass-loading-screen .message=${0}></hass-loading-screen>
      `),"Loading entity platform schema."),error:e=>this._renderError("Error loading schema",e),complete:()=>this._renderEntityConfig(this.entityPlatform)})}_renderError(e,t){return T.error("Error in create/edit entity",t),(0,r.dy)(O||(O=A`
      <hass-subpage
        .hass=${0}
        .narrow=${0}
        .back-path=${0}
        .header=${0}
      >
        <div class="content">
          <ha-alert alert-type="error"> ${0} </ha-alert>
        </div>
      </hass-subpage>
    `),this.hass,this.narrow,this.backPath,this.hass.localize("ui.panel.config.integrations.config_flow.error"),e)}_renderTypeSelection(){return(0,r.dy)(M||(M=A`
      <hass-subpage
        .hass=${0}
        .narrow=${0}
        .back-path=${0}
        .header=${0}
      >
        <div class="type-selection">
          <ha-card
            outlined
            .header=${0}
          >
            <!-- <p>Some help text</p> -->
            <ha-navigation-list
              .hass=${0}
              .narrow=${0}
              .pages=${0}
              has-secondary
              .label=${0}
            ></ha-navigation-list>
          </ha-card>
        </div>
      </hass-subpage>
    `),this.hass,this.narrow,this.backPath,this.hass.localize("component.knx.config_panel.entities.create.type_selection.title"),this.hass.localize("component.knx.config_panel.entities.create.type_selection.header"),this.hass,this.narrow,this.knx.supportedPlatforms.map((e=>{const t=(0,_.s)(e);return{name:`${this.hass.localize(`component.${e}.title`)}`,description:`${this.hass.localize(`component.knx.config_panel.entities.create.${e}.description`)}`,iconPath:t.iconPath,iconColor:t.color,path:`/knx/entities/create/${e}`}})),this.hass.localize("component.knx.config_panel.entities.create.type_selection.title"))}_renderEntityConfig(e){var t,i;const o="create"===this._intent,a=this.knx.schema[e];return(0,r.dy)(H||(H=A`<hass-subpage
      .hass=${0}
      .narrow=${0}
      .back-path=${0}
      .header=${0}
    >
      <div class="content">
        <div class="entity-config">
          <knx-configure-entity
            .hass=${0}
            .knx=${0}
            .platform=${0}
            .config=${0}
            .schema=${0}
            .validationErrors=${0}
            @knx-entity-configuration-changed=${0}
          >
            ${0}
          </knx-configure-entity>
          <ha-fab
            .label=${0}
            extended
            @click=${0}
            ?disabled=${0}
          >
            <ha-svg-icon slot="icon" .path=${0}></ha-svg-icon>
          </ha-fab>
        </div>
        ${0}
      </div>
    </hass-subpage>`),this.hass,this.narrow,this.backPath,o?this.hass.localize("component.knx.config_panel.entities.create.header"):`${this.hass.localize("ui.common.edit")}: ${this.entityId}`,this.hass,this.knx,e,this._config,a,this._validationErrors,this._configChanged,this._validationBaseError?(0,r.dy)(P||(P=A`<ha-alert slot="knx-validation-error" alert-type="error">
                  <details>
                    <summary><b>Validation error</b></summary>
                    <p>Base error: ${0}</p>
                    ${0}
                  </details>
                </ha-alert>`),this._validationBaseError,null!==(t=null===(i=this._validationErrors)||void 0===i?void 0:i.map((e=>{var t;return(0,r.dy)(D||(D=A`<p>
                          ${0}: ${0} in ${0}
                        </p>`),e.error_class,e.error_message,null===(t=e.path)||void 0===t?void 0:t.join(" / "))})))&&void 0!==t?t:r.Ld):r.Ld,o?this.hass.localize("ui.common.create"):this.hass.localize("ui.common.save"),o?this._entityCreate:this._entityUpdate,void 0===this._config,o?E:j,this.knx.projectData?(0,r.dy)(I||(I=A` <div class="panel">
              <knx-project-device-tree
                .data=${0}
                .validDPTs=${0}
              ></knx-project-device-tree>
            </div>`),this.knx.projectData,(0,g.ts)(a)):r.Ld)}_configChanged(e){e.stopPropagation(),T.debug("configChanged",e.detail),this._config=e.detail,this._validationErrors&&this._entityValidate()}_entityCreate(e){e.stopPropagation(),void 0!==this._config&&void 0!==this.entityPlatform?(0,b.JP)(this.hass,{platform:this.entityPlatform,data:this._config}).then((e=>{this._handleValidationError(e,!0)||(T.debug("Successfully created entity",e.entity_id),(0,c.c)("/knx/entities",{replace:!0}),e.entity_id?this._entityMoreInfoSettings(e.entity_id):T.error("entity_id not found after creation."))})).catch((e=>{T.error("Error creating entity",e),(0,c.c)("/knx/error",{replace:!0,data:e})})):T.error("No config found.")}_entityUpdate(e){e.stopPropagation(),void 0!==this._config&&void 0!==this.entityId&&void 0!==this.entityPlatform?(0,b.i8)(this.hass,{platform:this.entityPlatform,entity_id:this.entityId,data:this._config}).then((e=>{this._handleValidationError(e,!0)||(T.debug("Successfully updated entity",this.entityId),(0,c.c)("/knx/entities",{replace:!0}))})).catch((e=>{T.error("Error updating entity",e),(0,c.c)("/knx/error",{replace:!0,data:e})})):T.error("No config found.")}_handleValidationError(e,t){return!1===e.success?(T.warn("Validation error",e),this._validationErrors=e.errors,this._validationBaseError=e.error_base,t&&setTimeout((()=>this._alertElement.scrollIntoView({behavior:"smooth"}))),!0):(this._validationErrors=void 0,this._validationBaseError=void 0,T.debug("Validation passed",e.entity_id),!1)}_entityMoreInfoSettings(e){(0,p.B)(h.E.document.querySelector("home-assistant"),"hass-more-info",{entityId:e,view:"settings"})}constructor(...e){super(...e),this._projectLoadTask=new l.iQ(this,{args:()=>[],task:async()=>{this.knx.projectInfo&&(this.knx.projectData||await this.knx.loadProject())}}),this._schemaLoadTask=new l.iQ(this,{args:()=>[this.entityPlatform],task:async([e])=>{e&&await this.knx.loadSchema(e)}}),this._entityConfigLoadTask=new l.iQ(this,{args:()=>[this.entityId],task:async([e])=>{if(!e)return;const{platform:t,data:i}=await(0,b.IK)(this.hass,e);this.entityPlatform=t,this._config=i}}),this._dragDropContextProvider=new n.HQ(this,{context:m.R,initialValue:new m.Z((()=>{this._dragDropContextProvider.updateObservers()}))}),this._entityValidate=(0,u.P)((()=>{T.debug("validate",this._config),void 0!==this._config&&void 0!==this.entityPlatform&&(0,b.W4)(this.hass,{platform:this.entityPlatform,data:this._config}).then((e=>{this._handleValidationError(e,!1)})).catch((e=>{T.error("validateEntity",e),(0,c.c)("/knx/error",{replace:!0,data:e})}))}),250)}}q.styles=(0,r.iv)(z||(z=A`
    hass-loading-screen {
      --app-header-background-color: var(--sidebar-background-color);
      --app-header-text-color: var(--sidebar-text-color);
    }

    .type-selection {
      margin: 20px auto 80px;
      max-width: 720px;
    }

    @media screen and (max-width: 600px) {
      .panel {
        display: none;
      }
    }

    .content {
      display: flex;
      flex-direction: row;
      height: 100%;
      width: 100%;

      & > .entity-config {
        flex-grow: 1;
        flex-shrink: 1;
        height: 100%;
        overflow-y: scroll;
      }

      & > .panel {
        flex-grow: 0;
        flex-shrink: 3;
        width: 480px;
        min-width: 280px;
      }
    }

    knx-configure-entity {
      display: block;
      margin: 20px auto 40px; /* leave 80px space for fab */
      max-width: 720px;
    }

    ha-alert {
      display: block;
      margin: 20px auto;
      max-width: 720px;

      & summary {
        padding: 10px;
      }
    }

    ha-fab {
      /* not slot="fab" to move out of panel */
      float: right;
      margin-right: calc(16px + env(safe-area-inset-right));
      margin-bottom: 40px;
      z-index: 1;
    }
  `)),(0,a.__decorate)([(0,s.Cb)({type:Object})],q.prototype,"hass",void 0),(0,a.__decorate)([(0,s.Cb)({attribute:!1})],q.prototype,"knx",void 0),(0,a.__decorate)([(0,s.Cb)({type:Object})],q.prototype,"route",void 0),(0,a.__decorate)([(0,s.Cb)({type:Boolean,reflect:!0})],q.prototype,"narrow",void 0),(0,a.__decorate)([(0,s.Cb)({type:String,attribute:"back-path"})],q.prototype,"backPath",void 0),(0,a.__decorate)([(0,s.SB)()],q.prototype,"_config",void 0),(0,a.__decorate)([(0,s.SB)()],q.prototype,"_validationErrors",void 0),(0,a.__decorate)([(0,s.SB)()],q.prototype,"_validationBaseError",void 0),(0,a.__decorate)([(0,s.IO)("ha-alert")],q.prototype,"_alertElement",void 0),q=(0,a.__decorate)([(0,s.Mo)("knx-create-entity")],q),o()}catch(x){o(x)}}))}}]);
//# sourceMappingURL=5080.2f49dd1232851b7e.js.map