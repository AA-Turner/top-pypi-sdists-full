/*! For license information please see 94312.62756e72ab74d83a.js.LICENSE.txt */
export const __rspack_esm_id=94312;export const __rspack_esm_ids=[94312];export const __webpack_modules__={75334(t,e,a){var o=a(79537);const i=(0,a(37264).n)(t=>{(0,o.zd)({scrollPosition:t})},300);function n(t){return(e,a)=>{if("object"==typeof a)throw new Error("This decorator does not support this compilation type.");const n=e.connectedCallback;e.connectedCallback=function(){n.call(this);const e=this[a];e&&this.updateComplete.then(()=>{const a=this.renderRoot.querySelector(t);a&&setTimeout(()=>{a.scrollTop=e},0)})};const r=Object.getOwnPropertyDescriptor(e,a);let s;if(void 0===r)s={get(){return this[`__${String(a)}`]||(0,o.GL)()?.scrollPosition},set(t){i(t),this[`__${String(a)}`]=t},configurable:!0,enumerable:!0};else{const t=r.set;s={...r,set(e){i(e),this[`__${String(a)}`]=e,t?.call(this,e)}}}Object.defineProperty(e,a,s)}}a.d(e,{a:()=>n})},85058(t,e,a){a(18111),a(20116);a.d(e,{},{d:(t,e=!0)=>{if(t.defaultPrevented||0!==t.button||t.metaKey||t.ctrlKey||t.shiftKey)return;const a=t.composedPath().find(t=>"A"===t.tagName);if(!a||a.target||a.hasAttribute("download")||"external"===a.getAttribute("rel"))return;let o;try{o=new URL(a.href)}catch{return}return o.origin===window.location.origin?(e&&t.preventDefault(),o.pathname+o.search+o.hash):void 0}})},91230(t,e,a){var o=a(76108);a.d(e,{},{l:async(t,e)=>{if(navigator.clipboard)try{return void await navigator.clipboard.writeText(t)}catch{}const a=e||(0,o.n)()?.getRootNode()||document.body,i=a.nodeType===Node.DOCUMENT_NODE?document.body:a,n=document.createElement("textarea");n.value=t,n.setAttribute("readonly",""),n.style.position="fixed",n.style.top="0",n.style.left="0",n.style.opacity="0",i.appendChild(n),n.select(),document.execCommand("copy"),i.removeChild(n)}})},37264(t,e,a){a.d(e,{},{n:(t,e,a=!0,o=!0)=>{let i,n=0;const r=(...r)=>{const s=()=>{n=!1===a?0:Date.now(),i=void 0,t(...r)},l=Date.now();n||!1!==a||(n=l);const c=e-(l-n);c<=0||c>e?(i&&(clearTimeout(i),i=void 0),n=l,t(...r)):i||!1===o||(i=window.setTimeout(s,c))};return r.cancel=()=>{clearTimeout(i),i=void 0,n=0},r}})},22575(t,e,a){var o=a(85058),i=a(79537),n=a(70855);a.d(e,{},{E:(t,e,a)=>{const r=(0,n.H)(e);r&&!(0,o.d)(t)||(a?a():(0,i.OE)(r))}})},11602(t,e,a){a.a(t,async function(t,e){try{var o=a(15697),i=a(57527),n=a(8399),r=a(97901),s=a(75334),l=a(79537),c=a(70855),h=a(22575),d=a(99628),p=a(11010),u=a(97651),x=t([d,p]);[d,p]=x.then?(await x)():x;class y extends i.WF{render(){const t=(0,c.H)(this.backPath);return i.qy` <div class="toolbar ${(0,r.H)({narrow:this.narrow})}"> <div class="toolbar-content"> ${this.mainPage||!t&&(0,l.GL)()?.root?i.qy`<ha-menu-button></ha-menu-button>`:i.qy` <ha-icon-button-arrow-prev .href=${t} @click=${this._backTapped}></ha-icon-button-arrow-prev> `} <div class="main-title"> <slot name="header">${this.header}</slot> </div> <slot name="toolbar-icon"></slot> </div> </div> <div class=${(0,r.H)({content:!0,"ha-scrollbar":this.scrollable,"not-scrollable":!this.scrollable})} @scroll=${this._saveScrollPos}> <slot></slot> </div> <div id="fab"> <slot name="fab"></slot> </div> `}_saveScrollPos(t){this._savedScrollPos=t.target.scrollTop}_backTapped(t){(0,h.E)(t,this.backPath,this.backCallback)}static get styles(){return[u.dp,i.AH`:host{background-color:var(--primary-background-color);height:100%;display:block;position:relative;overflow:hidden}:host([narrow]){width:100%;position:fixed}.toolbar{background-color:var(--app-header-background-color);padding-top:var(--safe-area-inset-top);padding-right:var(--safe-area-inset-right)}:host([narrow]) .toolbar{padding-left:var(--safe-area-inset-left)}.toolbar-content{font-size:var(--ha-font-size-xl);height:var(--header-height);font-weight:var(--ha-font-weight-normal);color:var(--app-header-text-color,white);border-bottom:var(--app-header-border-bottom,none);box-sizing:border-box;align-items:center;padding:8px 12px;display:flex}.toolbar a{color:var(--sidebar-text-color);text-decoration:none}ha-menu-button,ha-icon-button-arrow-prev,::slotted([slot=toolbar-icon]){pointer-events:auto;color:var(--sidebar-icon-color);align-items:center;display:flex}.main-title{line-height:var(--ha-line-height-normal);overflow-wrap:break-word;-webkit-line-clamp:2;text-overflow:ellipsis;-webkit-box-orient:vertical;flex-grow:1;min-width:0;margin-inline-start:var(--ha-space-6);display:-webkit-box;overflow:hidden}.narrow .main-title{margin-inline-start:var(--ha-space-2)}.content{width:calc(100% - var(--safe-area-inset-right,0px));height:calc(100% - 1px - var(--header-height,0px) - var(--safe-area-inset-top,0px) - var(--safe-area-inset-bottom,0px));padding-bottom:var(--safe-area-inset-bottom,0px);margin-right:var(--safe-area-inset-right);-webkit-overflow-scrolling:touch;position:relative;overflow:auto}.content.not-scrollable{flex-direction:column;display:flex;overflow:hidden}:host([narrow]) .content{width:calc(100% - var(--safe-area-inset-left,0px) - var(--safe-area-inset-right,0px));margin-left:var(--safe-area-inset-left)}#fab{right:calc(16px + var(--safe-area-inset-right,0px));inset-inline-start:initial;inset-inline-end:calc(16px + var(--safe-area-inset-right,0px));bottom:calc(16px + var(--safe-area-inset-bottom,0px));z-index:1;justify-content:flex-end;gap:var(--ha-space-2);--ha-button-box-shadow:var(--ha-box-shadow-l);flex-wrap:wrap;display:flex;position:absolute}:host([narrow]) #fab.tabs{bottom:calc(84px + var(--safe-area-inset-bottom,0px))}#fab[is-wide]{bottom:calc(24px + var(--safe-area-inset-bottom,0px));right:calc(24px + var(--safe-area-inset-right,0px));inset-inline-start:initial;inset-inline-end:calc(24px + var(--safe-area-inset-right,0px))}`]}constructor(...t){super(...t),this.mainPage=!1,this.narrow=!1,this.scrollable=!0}}(0,o.Cg)([(0,n.MZ)({attribute:!1})],y.prototype,"hass",void 0),(0,o.Cg)([(0,n.MZ)()],y.prototype,"header",void 0),(0,o.Cg)([(0,n.MZ)({type:Boolean,attribute:"main-page"})],y.prototype,"mainPage",void 0),(0,o.Cg)([(0,n.MZ)({type:String,attribute:"back-path"})],y.prototype,"backPath",void 0),(0,o.Cg)([(0,n.MZ)({attribute:!1})],y.prototype,"backCallback",void 0),(0,o.Cg)([(0,n.MZ)({type:Boolean,reflect:!0})],y.prototype,"narrow",void 0),(0,o.Cg)([(0,n.MZ)({type:Boolean})],y.prototype,"scrollable",void 0),(0,o.Cg)([(0,s.a)(".content")],y.prototype,"_savedScrollPos",void 0),(0,o.Cg)([(0,n.Ls)({passive:!0})],y.prototype,"_saveScrollPos",null),y=(0,o.Cg)([(0,n.EM)("hass-subpage")],y),e()}catch(t){e(t)}})},74054(t,e,a){a(18111),a(22489);var o=a(15697),i=a(57527),n=a(8399),r=a(64820),s=a(67811),l=a(97168);a(30531),a(7588),a(61701),a(45367),a(92731);const c=.1,h=1.3,d=.2,p=224,u=240,x=[84,154,224],y=.03,f=.12,g=.24,v=.05,m=.45,b=.6,k={cycle:24,bursts:[[.6],[4.4,4.7],[9.2],[12.6,13],[16.9],[19.4,19.8]]},w={flight:c+h+d,blink:y+g,blinkDelays:x.map(t=>c+t/p*h-y),noAck:b-v,noAckDelay:c+h+d+v},$=[.04,.08],_=12,M=26,C=48,T=.24,j=.75,A=.9,z={hit:Object.fromEntries(x.map((t,e)=>[e+1,c+t/p*h])),flight:{},flash:A+.03};for(const t of[1,2,3])z.flight[t]=z.hit[t]+A;const Z={cycle:15.5,sends:[{at:.5,device:2},{at:3,device:1},{at:5.6,device:3},{at:8.2,device:3},{at:10.7,device:1},{at:13,device:2}]},P=t=>Math.max(...t.bursts.map(t=>t.length)),D=t=>{const e=Array.from({length:P(t)},()=>[]);for(const a of t.bursts)a.forEach((t,a)=>e[a].push(t));return e},E=(t,e,a)=>{const o=new Map;for(const[t,i]of a)o.set(Math.min(Math.max(t,0),e),i);const i=[...o.entries()].sort(([t],[e])=>t-e).map(([t,a])=>`    ${((t,e)=>`${Number((t/e*100).toFixed(3))}%`)(t,e)} {\n${a.map(t=>`      ${t};`).join("\n")}\n    }`).join("\n");return`@keyframes ${t} {\n${i}\n  }`},H=(t,e)=>[`transform: translateX(${t}px)`,`opacity: ${e}`],S=["fill: var(--knx-bus-scene-line)","opacity: 0.3"],q=["fill: var(--knx-bus-scene-reject)","opacity: 1"],W=["stroke: var(--knx-bus-scene-line)","stroke-opacity: 0.6"],N=["stroke: var(--knx-bus-scene-reject)","stroke-opacity: 1"],O=["opacity: 0"],K=["opacity: 1"],B=t=>{return[...D(t).map((e,a)=>((t,e,a)=>E(t,a,[[0,H(0,0)],...e.flatMap(t=>[[t,H(0,0)],[t+c,H(0,1)],[t+c+h,H(p,1)],[t+w.flight,H(u,0)],[t+w.flight+.02,H(0,0)]]),[a,H(0,0)]]))(`knx-send-${a}`,e,t.cycle)),...x.map((e,a)=>((t,e,a,o)=>E(t,o,[[0,S],...e.flatMap(t=>{const e=t+c+a/p*h;return[[e-y,S],[e,q],[e+f,q],[e+g,S]]}),[o,S]]))(`knx-blink-${a+1}`,t.bursts.flat(),e,t.cycle)),(e="knx-no-ack",a=t.bursts,o=t.cycle,E(e,o,[[0,O],...a.flatMap(t=>{const e=Math.max(...t)+w.flight;return[[e,O],[e+v,K],[e+m,K],[e+b,O]]}),[o,O]]))].join("\n\n  ");var e,a,o},J=(t,e)=>{const a=x[e-1],o=t+z.hit[e];return[[t,H(0,0)],[t+c,H(0,1)],[o,H(a-_,1)],[o+T,H(a-M,1)],[o+j,H(a-C,0)],[o+j+.02,H(0,0)]]},U=(t,e,a,o,i,n=0)=>E(t,e,[[0,o],...a.flatMap(t=>((t,e,a,o=0)=>[[t-.03,e],[t+o,a],[t+.55+o,a],[t+A,e]])(t,o,i,n)),[e,o]]),F=(t=Z)=>{const{cycle:e}=t,a=e=>t.sends.filter(t=>t.device===e).map(t=>t.at+z.hit[e]);return[...[1,2,3].flatMap(o=>[E(`knx-reject-${o}`,e,[[0,H(0,0)],...t.sends.filter(t=>t.device===o).flatMap(t=>J(t.at,t.device)),[e,H(0,0)]]),U(`knx-nak-body-${o}`,e,a(o),W,N),U(`knx-nak-led-${o}`,e,a(o),S,q),U(`knx-nak-text-${o}`,e,a(o),O,K,.06)])].join("\n\n  ")},L=(t,e)=>`${t} {\n      ${e}\n    }`,R=i.JW` <svg class="ha-logo" viewBox="0 0 240 240" x="21" y="40" width="30" height="30"> <path class="house" d="M240 224.762a15 15 0 0 1-15 15H15a15 15 0 0 1-15-15v-90c0-8.25 4.77-19.769 10.61-25.609l98.78-98.7805c5.83-5.83 15.38-5.83 21.21 0l98.79 98.7895c5.83 5.83 10.61 17.36 10.61 25.61v90-.01Z"/> <path class="tree" d="m107.27 239.762-40.63-40.63c-2.09.72-4.32 1.13-6.64 1.13-11.3 0-20.5-9.2-20.5-20.5s9.2-20.5 20.5-20.5 20.5 9.2 20.5 20.5c0 2.33-.41 4.56-1.13 6.65l31.63 31.63v-115.88c-6.8-3.3395-11.5-10.3195-11.5-18.3895 0-11.3 9.2-20.5 20.5-20.5s20.5 9.2 20.5 20.5c0 8.07-4.7 15.05-11.5 18.3895v81.27l31.46-31.46c-.62-1.96-.96-4.04-.96-6.2 0-11.3 9.2-20.5 20.5-20.5s20.5 9.2 20.5 20.5-9.2 20.5-20.5 20.5c-2.5 0-4.88-.47-7.09-1.29L129 208.892v30.88z"/> </svg> `,V=[t=>i.JW` <rect class="glyph fill" x=${t-11} y="53" width="12" height="3" rx="1.5"/> <rect class="glyph fill" x=${t-11} y="60" width="12" height="3" rx="1.5"/> `,t=>i.JW` <circle class="glyph line" cx=${t-5} cy="58" r="5.5"/> <line class="glyph line" x1=${t-5} y1="58" x2=${t-2} y2="54.5"/> `,t=>i.JW` <circle class="glyph fill" cx=${t-10} cy="63" r="1.6"/> <path class="glyph line" d="M ${t-10} 58.5 A 4.5 4.5 0 0 1 ${t-5.5} 63"/> <path class="glyph line" d="M ${t-10} 54 A 9 9 0 0 1 ${t-1} 63"/> `],I=(t,e)=>i.JW` <g class="device device-${e}"> <line class="drop" x1=${t} y1="70" x2=${t} y2="84"/> <rect class="body" x=${t-17} y="46" width="34" height="24" rx="5"/> ${V[e-1](t)} <circle class="led" cx=${t+10} cy="53" r="2.5"/> </g> `,X=(t,e)=>i.JW` <g class="ghost ghost-2 ${t}"><circle cx="36" cy="84" r="2.5"/></g> <g class="ghost ghost-1 ${t}"><circle cx="36" cy="84" r="3.2"/></g> <g class="telegram ${t}"> <circle class="halo" cx="36" cy="84" r="9"/> <circle class="dot" cx="36" cy="84" r="4"/> <rect class="badge" x="19" y="94" width="34" height="14" rx="7"/> <text x="36" y="104" text-anchor="middle">${e}</text> </g> `,G=P(k),Y={1:120,2:190,3:260},Q="4/0/4",tt={1:"4/0/3",2:"5/0/0",3:"5/0/3"},et=1e3,at=2,ot=6,it=100;class nt extends i.WF{render(){return i.qy` <svg viewBox="0 0 320 118" xmlns="http://www.w3.org/2000/svg"> <line class="bus" x1="12" y1="84" x2="308" y2="84"/> <line class="bus bus-shadow" x1="12" y1="87" x2="308" y2="87"/> <line class="bus-load" x1="12" y1="84" x2="308" y2="84"/> <g class="rate"> <text class="rate-value" x="308" y="27" text-anchor="end">${this._rate}</text> <text class="rate-unit" x="308" y="37" text-anchor="end">${this.rateUnit}</text> </g> <g class="sender"> <line class="drop" x1="36" y1="70" x2="36" y2="84"/> ${(0,r.u)(this._sent,t=>t.id,()=>i.JW`<circle class="ripple" cx="36" cy="55" r="16"/>`)} ${R} </g> ${I(Y[1],1)} ${I(Y[2],2)} ${I(Y[3],3)} <text class="no-ack" x="308" y="79" text-anchor="end">no ACK</text> ${[1,2,3].map(t=>i.JW`<text class="nak nak-${t}" x=${Y[t]} y="38" text-anchor="middle">NAK</text>`)} ${"error"===this.variant?[1,2,3].map(t=>X(`scheduled reject-lane-${t}`,tt[t])):Array.from({length:G},(t,e)=>X(`scheduled lane-${e}`,Q))} ${(0,r.u)(this._sent,t=>t.id,this._renderShot)} </svg> `}fire(){if((0,s.r)(l.G,"haptic","light"),this._tapTimes.push(Date.now()),this._updateRate(),this._holdSchedule(),"function"==typeof window.matchMedia&&window.matchMedia("(prefers-reduced-motion: reduce)").matches)return;const t="error"===this.variant?1+Math.floor(3*Math.random()):void 0;this._sent=[...this._sent,{id:this._nextId++,device:t}]}_holdSchedule(){this.busy=!0,window.clearTimeout(this._quietTimer),this._quietTimer=window.setTimeout(()=>{this._quietTimer=void 0,this.busy=!1},1500)}_updateRate(){const t=Date.now()-et;this._tapTimes=this._tapTimes.filter(e=>e>t),this._rate=this._tapTimes.length;const e=(this._rate-at)/(ot-at);this.style.setProperty("--knx-bus-scene-load",String(Math.min(Math.max(e,0),1))),this._tapTimes.length&&void 0===this._rateTick&&(this._rateTick=window.setTimeout(()=>{this._rateTick=void 0,this._updateRate()},it))}firstUpdated(){this.setAttribute("aria-hidden","true")}disconnectedCallback(){super.disconnectedCallback(),window.clearTimeout(this._rateTick),window.clearTimeout(this._quietTimer),this._rateTick=this._quietTimer=void 0,this.busy=!1}constructor(...t){super(...t),this.variant="not-found",this.busy=!1,this.rateUnit="telegrams/s",this._rate=0,this._sent=[],this._nextId=0,this._tapTimes=[],this._renderShot=({id:t,device:e})=>{if(e){const a=Y[e];return i.JW` <g class="shot reject-${e}" data-id=${t} @animationend=${this._shotEnded}> ${X("",tt[e])} <rect class="body-echo" x=${a-17} y="46" width="34" height="24" rx="5"/> <circle class="led-echo" cx=${a+10} cy="53" r="2.5"/> <text class="nak-echo" x=${a} y="38" text-anchor="middle">NAK</text> </g> `}return i.JW` <g class="shot" data-id=${t} @animationend=${this._shotEnded}> ${X("",Q)} <circle class="led-echo led-echo-1" cx="130" cy="53" r="2.5"/> <circle class="led-echo led-echo-2" cx="200" cy="53" r="2.5"/> <circle class="led-echo led-echo-3" cx="270" cy="53" r="2.5"/> <text class="shot-no-ack" x="308" y="79" text-anchor="end">no ACK</text> </g> `},this._shotEnded=t=>{if("knx-shot-no-ack"!==t.animationName&&"knx-shot-nak"!==t.animationName)return;const e=Number(t.currentTarget.dataset.id);this._sent=this._sent.filter(t=>t.id!==e)}}}nt.styles=i.AH`
    :host {
      display: block;
      width: 100%;
      max-width: 400px;
      --knx-bus-scene-line: var(--secondary-text-color);
      --knx-bus-scene-device: var(--card-background-color);
      /* same fill + white text as the "Outgoing" badge in the group monitor */
      --knx-bus-scene-telegram: var(--knx-blue, var(--primary-color));
      --knx-bus-scene-on-telegram: var(--text-primary-color, #fff);
      --knx-bus-scene-reject: var(--error-color);
      /* --knx-bus-scene-load (0..1) is set inline by _updateRate */
    }

    svg {
      display: block;
      width: 100%;
      height: auto;
      overflow: visible;
    }

    .bus,
    .drop {
      stroke: var(--knx-bus-scene-line);
      stroke-width: 1.5;
      stroke-linecap: round;
      opacity: 0.55;
    }

    .bus-shadow {
      opacity: 0.2;
    }

    .drop {
      opacity: 0.4;
    }

    /* bus load: the line fills with KNX blue as the rate climbs */
    .bus-load {
      stroke: var(--knx-bus-scene-telegram);
      stroke-width: 2.2;
      stroke-linecap: round;
      opacity: calc(var(--knx-bus-scene-load, 0) * 0.85);
      transition: opacity 250ms ease;
    }

    .rate {
      opacity: var(--knx-bus-scene-load, 0);
      transition: opacity 250ms ease;
    }

    .rate-value {
      font-family: var(--ha-font-family-code, monospace);
      font-size: 24px;
      font-weight: var(--ha-font-weight-medium, 500);
      font-variant-numeric: tabular-nums;
      fill: var(--primary-text-color);
    }

    .rate-unit {
      font-size: 6.5px;
      font-weight: var(--ha-font-weight-medium, 500);
      letter-spacing: 0.14em;
      text-transform: uppercase;
      fill: var(--secondary-text-color);
    }

    /* brand colours as in ha-logo-svg, readable on light and dark themes */
    .sender .house,
    .sender .ripple {
      fill: #18bcf2;
    }

    .sender .tree {
      fill: #f2f4f9;
    }

    /* one ripple per tap, spreading out behind the logo, each on its own */
    .sender .ripple {
      opacity: 0;
      transform-box: fill-box;
      transform-origin: center;
      animation: knx-ripple 550ms ease-out;
    }

    @keyframes knx-ripple {
      0% {
        transform: scale(0.6);
        opacity: 0.4;
      }
      100% {
        transform: scale(2.4);
        opacity: 0;
      }
    }

    .device .body {
      fill: var(--knx-bus-scene-device);
      stroke: var(--knx-bus-scene-line);
      stroke-width: 1.5;
      stroke-opacity: 0.6;
    }

    .device .glyph {
      opacity: 0.4;
    }

    .device .glyph.fill {
      fill: var(--knx-bus-scene-line);
    }

    .device .glyph.line {
      fill: none;
      stroke: var(--knx-bus-scene-line);
      stroke-width: 1.5;
      stroke-linecap: round;
    }

    .device .led,
    .shot .led-echo {
      fill: var(--knx-bus-scene-line);
      opacity: 0.3;
    }

    .shot .led-echo {
      opacity: 0;
    }

    .shot .body-echo {
      fill: none;
      stroke: var(--knx-bus-scene-reject);
      stroke-width: 1.5;
      stroke-opacity: 0;
    }

    /* telegrams are invisible until their keyframes bring them onto the bus */
    .telegram,
    .ghost {
      opacity: 0;
    }

    .telegram .dot {
      fill: var(--knx-bus-scene-telegram);
      stroke: var(--primary-background-color);
      stroke-width: 1.5;
    }

    .telegram .halo,
    .telegram .badge,
    .ghost circle {
      fill: var(--knx-bus-scene-telegram);
    }

    .telegram .halo {
      opacity: 0.25;
    }

    .ghost-1 circle {
      opacity: 0.35;
    }

    .ghost-2 circle {
      opacity: 0.16;
    }

    .telegram text {
      font-family: var(--ha-font-family-code, monospace);
      font-size: 9px;
      fill: var(--knx-bus-scene-on-telegram);
    }

    .no-ack,
    .shot-no-ack,
    .nak,
    .nak-echo {
      font-family: var(--ha-font-family-code, monospace);
      font-size: 8px;
      letter-spacing: 0.08em;
      fill: var(--knx-bus-scene-reject);
      opacity: 0;
    }

    /* all animation bindings and keyframes, see knx-bus-scene-animations.ts */
    ${(0,i.iz)(((t=k)=>{const e=`${t.cycle}s linear infinite`,a=`${Z.cycle}s linear infinite`,o=t=>`:host([variant="not-found"]) ${t}`,i=t=>`:host([variant="error"]) ${t}`,n=[1,2,3];return[...D(t).map((t,a)=>L(o(`.lane-${a}`),`animation: knx-send-${a} ${e};`)),...n.map(t=>L(o(`.device-${t} .led`),`animation: knx-blink-${t} ${e};`)),L(o(".no-ack"),`animation: knx-no-ack ${e};`),...n.flatMap(t=>[L(i(`.reject-lane-${t}`),`animation: knx-reject-${t} ${a};`),L(i(`.device-${t} .body`),`animation: knx-nak-body-${t} ${a};`),L(i(`.device-${t} .led`),`animation: knx-nak-led-${t} ${a};`),L(i(`.nak-${t}`),`animation: knx-nak-text-${t} ${a};`)]),L(":host([busy]) .scheduled,\n    :host([busy]) .device .led,\n    :host([busy]) .device .body,\n    :host([busy]) .no-ack,\n    :host([busy]) .nak","animation: none;"),L(".shot .telegram,\n    .shot .ghost",`animation: knx-shot ${w.flight}s linear;`),L(".shot .led-echo",`animation: knx-shot-blink ${w.blink}s linear;`),...w.blinkDelays.map((t,e)=>L(`.shot .led-echo-${e+1}`,`animation-delay: ${t.toFixed(3)}s;`)),L(".shot .shot-no-ack",`animation: knx-shot-no-ack ${w.noAck}s linear ${w.noAckDelay}s;`),...n.flatMap(t=>{const e=`${(z.hit[t]-.03).toFixed(3)}s`;return[L(`.shot.reject-${t} .telegram,\n    .shot.reject-${t} .ghost`,`animation: knx-shot-reject-${t} ${z.flight[t].toFixed(3)}s linear;`),L(`.shot.reject-${t} .body-echo`,`animation: knx-shot-nak-body ${z.flash}s linear ${e};`),L(`.shot.reject-${t} .led-echo`,`animation: knx-shot-nak-led ${z.flash}s linear ${e};`),L(`.shot.reject-${t} .nak-echo`,`animation: knx-shot-nak ${z.flash}s linear ${e};`)]}),...$.map((t,e)=>L(`:host .ghost.ghost-${e+1}`,`animation-delay: ${t}s;`)),B(t),[E("knx-shot",w.flight,[[0,H(0,0)],[c,H(0,1)],[c+h,H(p,1)],[w.flight,H(u,0)]]),E("knx-shot-blink",w.blink,[[0,S],[y,q],[y+f,q],[w.blink,S]]),E("knx-shot-no-ack",w.noAck,[[0,K],[m-v,K],[w.noAck,O]])].join("\n\n  "),[...[1,2,3].map(t=>E(`knx-shot-reject-${t}`,z.flight[t],[...J(0,t).slice(0,-1),[z.flight[t],H(0,0)]])),U("knx-shot-nak-body",z.flash,[.03],["stroke-opacity: 0"],["stroke-opacity: 1"]),U("knx-shot-nak-led",z.flash,[.03],O,q),U("knx-shot-nak",z.flash,[.03],O,K,.06)].join("\n\n  "),F()].join("\n\n    ")})())}

    /* ---- reduced motion: show the end of the story instead ------------- */
    @media (prefers-reduced-motion: reduce) {
      .telegram,
      .device .led,
      .device .body,
      .no-ack,
      .nak {
        animation: none !important;
      }

      .ghost,
      .shot,
      .sender .ripple {
        display: none;
      }

      :host([variant="not-found"]) .telegram.lane-0 {
        transform: translateX(224px);
        opacity: 0.6;
      }

      :host([variant="not-found"]) .no-ack,
      :host([variant="error"]) .nak-1 {
        opacity: 1;
      }

      :host([variant="error"]) .telegram.reject-lane-1 {
        transform: translateX(58px);
        opacity: 1;
      }

      :host([variant="error"]) .device-1 .body {
        stroke: var(--knx-bus-scene-reject);
        stroke-opacity: 1;
      }

      :host([variant="error"]) .device-1 .led {
        fill: var(--knx-bus-scene-reject);
        opacity: 1;
      }
    }
  `,(0,o.Cg)([(0,n.MZ)({reflect:!0})],nt.prototype,"variant",void 0),(0,o.Cg)([(0,n.MZ)({type:Boolean,reflect:!0})],nt.prototype,"busy",void 0),(0,o.Cg)([(0,n.MZ)({attribute:"rate-unit"})],nt.prototype,"rateUnit",void 0),(0,o.Cg)([(0,n.wk)()],nt.prototype,"_rate",void 0),(0,o.Cg)([(0,n.wk)()],nt.prototype,"_sent",void 0),nt=(0,o.Cg)([(0,n.EM)("knx-bus-scene")],nt)},55565(t,e,a){a.a(t,async function(t,e){try{a(18111),a(13579),a(17642),a(15024),a(31698);var o=a(15697),i=a(57527),n=a(8399),r=a(22472),s=a(11602),l=a(91230),c=a(77671),h=(a(74054),t([r,s]));[r,s]=h.then?(await h)():h;const d="M19,21H8V7H19M19,5H8A2,2 0 0,0 6,7V21A2,2 0 0,0 8,23H19A2,2 0 0,0 21,21V7A2,2 0 0,0 19,5M16,1H4A2,2 0 0,0 2,3V17H4V3H16V1Z",p=new Set(["ha-button","ha-icon-button","button","a","input","select","textarea"]);class u extends i.WF{render(){return i.qy` <hass-subpage .hass=${this.hass} .narrow=${this.narrow} .header=${this.header}> <div class="content" @pointerdown=${this._tap}> <knx-bus-scene .variant=${this.variant} .rateUnit=${this.rateUnit}></knx-bus-scene> <h1> ${this.eyebrow?i.qy`<span class="eyebrow">${this.eyebrow}</span>`:i.s6} <span class="headline">${this.headline}</span> </h1> ${this.description?i.qy`<p class="description">${this.description}</p>`:i.s6} ${this.detail?i.qy`<div class="detail"> <span class="detail-label">${this.detailLabel}</span> <div class="detail-body"> <code>${this.detail}</code> ${this.copyable?i.qy`<ha-icon-button .path=${d} label=${this.hass.localize("ui.common.copy")} @click=${this._copy}></ha-icon-button>`:i.s6} </div> </div>`:i.s6} <div class="actions"><slot></slot></div> </div> </hass-subpage> `}_tap(t){if(0!==t.button)return;t.composedPath().some(t=>t instanceof Element&&p.has(t.localName))||this._scene?.fire()}async _copy(){await(0,l.l)(this.detail),(0,c.P)(this,{message:this.hass.localize("ui.common.copied_clipboard")})}constructor(...t){super(...t),this.narrow=!1,this.copyable=!1,this.variant="not-found",this.rateUnit="telegrams/s"}}u.styles=i.AH`:host{height:100%;display:block}.content{-webkit-tap-highlight-color:transparent;-webkit-touch-callout:none;touch-action:manipulation;user-select:none;box-sizing:border-box;text-align:center;max-width:520px;min-height:100%;color:var(--primary-text-color);flex-direction:column;justify-content:center;align-items:center;margin:0 auto;padding:24px 16px 14vh;display:flex}knx-bus-scene{margin-bottom:28px}h1{font:inherit;margin:0 0 12px}.eyebrow{color:var(--secondary-text-color);font-size:var(--ha-font-size-s,12px);font-weight:var(--ha-font-weight-medium,500);letter-spacing:.14em;text-transform:uppercase;margin:0 0 6px;display:block}.headline{font-family:var(--knx-status-page-headline-font,var(--ha-font-family-body,inherit));font-size:var(--knx-status-page-headline-size,var(--ha-font-size-3xl,28px));font-weight:var(--ha-font-weight-medium,500);line-height:var(--ha-line-height-condensed,1.2);display:block}.description{max-width:42ch;color:var(--secondary-text-color);font-size:var(--ha-font-size-l,16px);line-height:var(--ha-line-height-normal,1.6);margin:0}.detail{text-align:left;width:100%;margin-top:24px}.detail-label{color:var(--secondary-text-color);font-size:var(--ha-font-size-s,12px);font-weight:var(--ha-font-weight-medium,500);letter-spacing:.14em;text-transform:uppercase;margin:0 0 6px 2px;display:block}.detail-body{border-radius:var(--ha-border-radius-md,12px);background:var(--secondary-background-color);align-items:flex-start;gap:4px;padding:8px 6px 8px 14px;display:flex}.detail-body code{font-family:var(--ha-font-family-code,monospace);font-size:var(--ha-font-size-s,12px);line-height:var(--ha-line-height-normal,1.6);color:var(--primary-text-color);overflow-wrap:anywhere;user-select:text;flex:1;padding:6px 0}.detail-body ha-icon-button{--mdc-icon-button-size:36px;--mdc-icon-size:18px;color:var(--secondary-text-color);margin:-2px 0}.actions{flex-wrap:wrap;justify-content:center;gap:8px;margin-top:28px;display:flex}`,(0,o.Cg)([(0,n.MZ)({attribute:!1})],u.prototype,"hass",void 0),(0,o.Cg)([(0,n.MZ)({type:Boolean})],u.prototype,"narrow",void 0),(0,o.Cg)([(0,n.MZ)()],u.prototype,"header",void 0),(0,o.Cg)([(0,n.MZ)()],u.prototype,"eyebrow",void 0),(0,o.Cg)([(0,n.MZ)()],u.prototype,"headline",void 0),(0,o.Cg)([(0,n.MZ)()],u.prototype,"description",void 0),(0,o.Cg)([(0,n.MZ)({attribute:"detail-label"})],u.prototype,"detailLabel",void 0),(0,o.Cg)([(0,n.MZ)()],u.prototype,"detail",void 0),(0,o.Cg)([(0,n.MZ)({type:Boolean})],u.prototype,"copyable",void 0),(0,o.Cg)([(0,n.MZ)({reflect:!0})],u.prototype,"variant",void 0),(0,o.Cg)([(0,n.MZ)({attribute:"rate-unit"})],u.prototype,"rateUnit",void 0),(0,o.Cg)([(0,n.P)("knx-bus-scene")],u.prototype,"_scene",void 0),u=(0,o.Cg)([(0,n.EM)("knx-status-page")],u),e()}catch(t){e(t)}})},36859(t,e,a){a.a(t,async function(t,o){try{var i=a(15697),n=a(57527),r=a(8399),s=a(89274),l=a(79537),c=a(55565),h=(a(19465),t([s,c]));[s,c]=h.then?(await h)():h;class d extends n.WF{_goBack(){(0,l.OE)("/knx")}_goToDashboard(){(0,l.oo)("/knx")}constructor(...t){super(...t),this.narrow=!1}}d.styles=n.AH`:host{height:100%;display:block}`,(0,i.Cg)([(0,r.MZ)({attribute:!1})],d.prototype,"hass",void 0),(0,i.Cg)([(0,r.MZ)({attribute:!1})],d.prototype,"knx",void 0),(0,i.Cg)([(0,r.MZ)({type:Boolean})],d.prototype,"narrow",void 0),(0,i.Cg)([(0,r.MZ)({attribute:!1})],d.prototype,"route",void 0),a.d(e,{F:()=>d}),o()}catch(t){o(t)}})},48646(t,e,a){var o=a(69565),i=a(28551),n=a(1767),r=a(63085);t.exports=function(t,e){e&&"string"==typeof t||i(t);var a=r(t);return n(i(void 0!==a?o(a,t):t))}},30531(t,e,a){var o=a(46518),i=a(69565),n=a(79306),r=a(28551),s=a(1767),l=a(48646),c=a(19462),h=a(9539),d=a(79039),p=a(96395),u=a(30684),x=a(84549),y=!p&&d(function(){return 1!==[1].values().flatMap(function(){return[1]}).find(function(){return!0})}),f=!p&&!y&&!u("flatMap",function(){}),g=!p&&!y&&!f&&x("flatMap",TypeError),v=p||y||f||g,m=c(function(){for(var t,e,a=this.iterator,o=this.mapper;;){if(e=this.inner)try{if(!(t=r(i(e.next,e.iterator))).done)return t.value;this.inner=null}catch(t){h(a,"throw",t)}if(t=r(i(this.next,a)),this.done=!!t.done)return;try{this.inner=l(o(t.value,this.counter++),!1)}catch(t){h(a,"throw",t)}}});o({target:"Iterator",proto:!0,real:!0,forced:v},{flatMap:function(t){r(this);try{n(t)}catch(t){h(this,"throw",t)}return g?i(g,this,t):new m(s(this),{mapper:t,inner:null})}})},64820(t,e,a){a.d(e,{u:()=>s});a(45367),a(92731);var o=a(64238),i=a(67034),n=a(13246);const r=(t,e,a)=>{const o=new Map;for(let i=e;i<=a;i++)o.set(t[i],i);return o},s=(0,i.u$)(class extends i.WL{dt(t,e,a){let o;void 0===a?a=e:void 0!==e&&(o=e);const i=[],n=[];let r=0;for(const e of t)i[r]=o?o(e,r):r,n[r]=a(e,r),r++;return{values:n,keys:i}}render(t,e,a){return this.dt(t,e,a).values}update(t,[e,a,i]){const s=(0,n.cN)(t),{values:l,keys:c}=this.dt(e,a,i);if(!Array.isArray(s))return this.ut=c,l;const h=this.ut??=[],d=[];let p,u,x=0,y=s.length-1,f=0,g=l.length-1;for(;x<=y&&f<=g;)if(null===s[x])x++;else if(null===s[y])y--;else if(h[x]===c[f])d[f]=(0,n.lx)(s[x],l[f]),x++,f++;else if(h[y]===c[g])d[g]=(0,n.lx)(s[y],l[g]),y--,g--;else if(h[x]===c[g])d[g]=(0,n.lx)(s[x],l[g]),(0,n.Dx)(t,d[g+1],s[x]),x++,g--;else if(h[y]===c[f])d[f]=(0,n.lx)(s[y],l[f]),(0,n.Dx)(t,s[x],s[y]),y--,f++;else if(void 0===p&&(p=r(c,f,g),u=r(h,x,y)),p.has(h[x]))if(p.has(h[y])){const e=u.get(c[f]),a=void 0!==e?s[e]:null;if(null===a){const e=(0,n.Dx)(t,s[x]);(0,n.lx)(e,l[f]),d[f]=e}else d[f]=(0,n.lx)(a,l[f]),(0,n.Dx)(t,s[x],a),s[e]=null;f++}else(0,n.KO)(s[y]),y--;else(0,n.KO)(s[x]),x++;for(;f<=g;){const e=(0,n.Dx)(t,d[g+1]);(0,n.lx)(e,l[f]),d[f++]=e}for(;x<=y;){const t=s[x++];null!==t&&(0,n.KO)(t)}return this.ut=c,(0,n.mY)(t,d),o.c0}constructor(t){if(super(t),t.type!==i.OA.CHILD)throw Error("repeat() can only be used in text expressions")}})}};
//# sourceMappingURL=94312.62756e72ab74d83a.js.map