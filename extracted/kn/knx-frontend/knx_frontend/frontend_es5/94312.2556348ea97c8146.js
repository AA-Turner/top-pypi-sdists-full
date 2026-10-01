"use strict";(self.rspackChunkknx_frontend=self.rspackChunkknx_frontend||[]).push([[94312],{75334(t,e,a){var o=a(97058),i=(a(16280),a(79537));const n=(0,a(37264).n)(t=>{(0,i.zd)({scrollPosition:t})},300);function s(t){return(e,a)=>{if("object"==typeof a)throw new Error("This decorator does not support this compilation type.");const s=e.connectedCallback;e.connectedCallback=function(){s.call(this);const e=this[a];e&&this.updateComplete.then(()=>{const a=this.renderRoot.querySelector(t);a&&setTimeout(()=>{a.scrollTop=e},0)})};const r=Object.getOwnPropertyDescriptor(e,a);let l;if(void 0===r)l={get(){var t;return this[`__${String(a)}`]||(null===(t=(0,i.GL)())||void 0===t?void 0:t.scrollPosition)},set(t){n(t),this[`__${String(a)}`]=t},configurable:!0,enumerable:!0};else{const t=r.set;l=(0,o.A)((0,o.A)({},r),{},{set(e){n(e),this[`__${String(a)}`]=e,null==t||t.call(this,e)}})}Object.defineProperty(e,a,l)}}a.d(e,{a:()=>s})},85058(t,e,a){a(23792),a(18111),a(20116),a(27495),a(62953),a(3296),a(27208),a(48408),a(14603),a(47566),a(98721);a.d(e,{},{d:(t,e=!0)=>{if(t.defaultPrevented||0!==t.button||t.metaKey||t.ctrlKey||t.shiftKey)return;const a=t.composedPath().find(t=>"A"===t.tagName);if(!a||a.target||a.hasAttribute("download")||"external"===a.getAttribute("rel"))return;let o;try{o=new URL(a.href)}catch(t){return}return o.origin===window.location.origin?(e&&t.preventDefault(),o.pathname+o.search+o.hash):void 0}})},91230(t,e,a){a(3362);var o=a(76108);a.d(e,{},{l:async(t,e)=>{var a;if(navigator.clipboard)try{return void await navigator.clipboard.writeText(t)}catch(t){}const i=e||(null===(a=(0,o.n)())||void 0===a?void 0:a.getRootNode())||document.body,n=i.nodeType===Node.DOCUMENT_NODE?document.body:i,s=document.createElement("textarea");s.value=t,s.setAttribute("readonly",""),s.style.position="fixed",s.style.top="0",s.style.left="0",s.style.opacity="0",n.appendChild(s),s.select(),document.execCommand("copy"),n.removeChild(s)}})},37264(t,e,a){a(23792),a(62953);a.d(e,{},{n:(t,e,a=!0,o=!0)=>{let i,n=0;const s=(...s)=>{const r=()=>{n=!1===a?0:Date.now(),i=void 0,t(...s)},l=Date.now();n||!1!==a||(n=l);const c=e-(l-n);c<=0||c>e?(i&&(clearTimeout(i),i=void 0),n=l,t(...s)):i||!1===o||(i=window.setTimeout(r,c))};return s.cancel=()=>{clearTimeout(i),i=void 0,n=0},s}})},22575(t,e,a){var o=a(85058),i=a(79537),n=a(70855);a.d(e,{},{E:(t,e,a)=>{const s=(0,n.H)(e);s&&!(0,o.d)(t)||(a?a():(0,i.OE)(s))}})},11602(t,e,a){a.a(t,async function(t,e){try{a(23792),a(62953);var o=a(15697),i=a(57527),n=a(51209),s=a(48612),r=a(75334),l=a(79537),c=a(70855),h=a(22575),d=a(99628),p=a(11010),x=a(97651),y=t([d,p]);[d,p]=y.then?(await y)():y;let u,g,v,b,m=t=>t;class f extends i.WF{render(){var t;const e=(0,c.H)(this.backPath);return(0,i.qy)(u||(u=m` <div class="toolbar ${0}"> <div class="toolbar-content"> ${0} <div class="main-title"> <slot name="header">${0}</slot> </div> <slot name="toolbar-icon"></slot> </div> </div> <div class=${0} @scroll=${0}> <slot></slot> </div> <div id="fab"> <slot name="fab"></slot> </div> `),(0,s.H)({narrow:this.narrow}),this.mainPage||!e&&null!==(t=(0,l.GL)())&&void 0!==t&&t.root?(0,i.qy)(g||(g=m`<ha-menu-button></ha-menu-button>`)):(0,i.qy)(v||(v=m` <ha-icon-button-arrow-prev .href=${0} @click=${0}></ha-icon-button-arrow-prev> `),e,this._backTapped),this.header,(0,s.H)({content:!0,"ha-scrollbar":this.scrollable,"not-scrollable":!this.scrollable}),this._saveScrollPos)}_saveScrollPos(t){this._savedScrollPos=t.target.scrollTop}_backTapped(t){(0,h.E)(t,this.backPath,this.backCallback)}static get styles(){return[x.dp,(0,i.AH)(b||(b=m`:host{background-color:var(--primary-background-color);height:100%;display:block;position:relative;overflow:hidden}:host([narrow]){width:100%;position:fixed}.toolbar{background-color:var(--app-header-background-color);padding-top:var(--safe-area-inset-top);padding-right:var(--safe-area-inset-right)}:host([narrow]) .toolbar{padding-left:var(--safe-area-inset-left)}.toolbar-content{font-size:var(--ha-font-size-xl);height:var(--header-height);font-weight:var(--ha-font-weight-normal);color:var(--app-header-text-color,white);border-bottom:var(--app-header-border-bottom,none);box-sizing:border-box;align-items:center;padding:8px 12px;display:flex}.toolbar a{color:var(--sidebar-text-color);text-decoration:none}ha-menu-button,ha-icon-button-arrow-prev,::slotted([slot=toolbar-icon]){pointer-events:auto;color:var(--sidebar-icon-color);align-items:center;display:flex}.main-title{line-height:var(--ha-line-height-normal);overflow-wrap:break-word;-webkit-line-clamp:2;text-overflow:ellipsis;-webkit-box-orient:vertical;flex-grow:1;min-width:0;margin-inline-start:var(--ha-space-6);display:-webkit-box;overflow:hidden}.narrow .main-title{margin-inline-start:var(--ha-space-2)}.content{width:calc(100% - var(--safe-area-inset-right,0px));height:calc(100% - 1px - var(--header-height,0px) - var(--safe-area-inset-top,0px) - var(--safe-area-inset-bottom,0px));padding-bottom:var(--safe-area-inset-bottom,0px);margin-right:var(--safe-area-inset-right);-webkit-overflow-scrolling:touch;position:relative;overflow:auto}.content.not-scrollable{flex-direction:column;display:flex;overflow:hidden}:host([narrow]) .content{width:calc(100% - var(--safe-area-inset-left,0px) - var(--safe-area-inset-right,0px));margin-left:var(--safe-area-inset-left)}#fab{right:calc(16px + var(--safe-area-inset-right,0px));inset-inline-start:initial;inset-inline-end:calc(16px + var(--safe-area-inset-right,0px));bottom:calc(16px + var(--safe-area-inset-bottom,0px));z-index:1;justify-content:flex-end;gap:var(--ha-space-2);--ha-button-box-shadow:var(--ha-box-shadow-l);flex-wrap:wrap;display:flex;position:absolute}:host([narrow]) #fab.tabs{bottom:calc(84px + var(--safe-area-inset-bottom,0px))}#fab[is-wide]{bottom:calc(24px + var(--safe-area-inset-bottom,0px));right:calc(24px + var(--safe-area-inset-right,0px));inset-inline-start:initial;inset-inline-end:calc(24px + var(--safe-area-inset-right,0px))}`))]}constructor(...t){super(...t),this.mainPage=!1,this.narrow=!1,this.scrollable=!0}}(0,o.Cg)([(0,n.MZ)({attribute:!1})],f.prototype,"hass",void 0),(0,o.Cg)([(0,n.MZ)()],f.prototype,"header",void 0),(0,o.Cg)([(0,n.MZ)({type:Boolean,attribute:"main-page"})],f.prototype,"mainPage",void 0),(0,o.Cg)([(0,n.MZ)({type:String,attribute:"back-path"})],f.prototype,"backPath",void 0),(0,o.Cg)([(0,n.MZ)({attribute:!1})],f.prototype,"backCallback",void 0),(0,o.Cg)([(0,n.MZ)({type:Boolean,reflect:!0})],f.prototype,"narrow",void 0),(0,o.Cg)([(0,n.MZ)({type:Boolean})],f.prototype,"scrollable",void 0),(0,o.Cg)([(0,r.a)(".content")],f.prototype,"_savedScrollPos",void 0),(0,o.Cg)([(0,n.Ls)({passive:!0})],f.prototype,"_saveScrollPos",null),f=(0,o.Cg)([(0,n.EM)("hass-subpage")],f),e()}catch(t){e(t)}})},74054(t,e,a){a(23792),a(44114),a(18111),a(22489),a(62953);var o=a(15697),i=a(57527),n=a(51209),s=a(54497),r=a(67811),l=a(97168);a(18107),a(46449),a(78350),a(26910),a(93514),a(30237),a(30531),a(7588),a(61701),a(45367),a(92731),a(53921),a(67357);const c=.1,h=1.3,d=.2,p=224,x=240,y=[84,154,224],u=.03,g=.12,v=.24,b=.05,m=.45,f=.6,k={cycle:24,bursts:[[.6],[4.4,4.7],[9.2],[12.6,13],[16.9],[19.4,19.8]]},w={flight:c+h+d,blink:u+v,blinkDelays:y.map(t=>c+t/p*h-u),noAck:f-b,noAckDelay:c+h+d+b},$=[.04,.08],_=12,M=26,C=48,T=.24,j=.75,A=.9,z={hit:Object.fromEntries(y.map((t,e)=>[e+1,c+t/p*h])),flight:{},flash:A+.03};for(const t of[1,2,3])z.flight[t]=z.hit[t]+A;const Z={cycle:15.5,sends:[{at:.5,device:2},{at:3,device:1},{at:5.6,device:3},{at:8.2,device:3},{at:10.7,device:1},{at:13,device:2}]},P=t=>Math.max(...t.bursts.map(t=>t.length)),E=t=>{const e=Array.from({length:P(t)},()=>[]);for(const a of t.bursts)a.forEach((t,a)=>e[a].push(t));return e},H=(t,e,a)=>{const o=new Map;for(const[t,i]of a)o.set(Math.min(Math.max(t,0),e),i);const i=[...o.entries()].sort(([t],[e])=>t-e).map(([t,a])=>`    ${((t,e)=>`${Number((t/e*100).toFixed(3))}%`)(t,e)} {\n${a.map(t=>`      ${t};`).join("\n")}\n    }`).join("\n");return`@keyframes ${t} {\n${i}\n  }`},S=(t,e)=>[`transform: translateX(${t}px)`,`opacity: ${e}`],q=["fill: var(--knx-bus-scene-line)","opacity: 0.3"],W=["fill: var(--knx-bus-scene-reject)","opacity: 1"],D=["stroke: var(--knx-bus-scene-line)","stroke-opacity: 0.6"],N=["stroke: var(--knx-bus-scene-reject)","stroke-opacity: 1"],B=["opacity: 0"],J=["opacity: 1"],U=t=>{return[...E(t).map((e,a)=>((t,e,a)=>H(t,a,[[0,S(0,0)],...e.flatMap(t=>[[t,S(0,0)],[t+c,S(0,1)],[t+c+h,S(p,1)],[t+w.flight,S(x,0)],[t+w.flight+.02,S(0,0)]]),[a,S(0,0)]]))(`knx-send-${a}`,e,t.cycle)),...y.map((e,a)=>((t,e,a,o)=>H(t,o,[[0,q],...e.flatMap(t=>{const e=t+c+a/p*h;return[[e-u,q],[e,W],[e+g,W],[e+v,q]]}),[o,q]]))(`knx-blink-${a+1}`,t.bursts.flat(),e,t.cycle)),(e="knx-no-ack",a=t.bursts,o=t.cycle,H(e,o,[[0,B],...a.flatMap(t=>{const e=Math.max(...t)+w.flight;return[[e,B],[e+b,J],[e+m,J],[e+f,B]]}),[o,B]]))].join("\n\n  ");var e,a,o},F=(t,e)=>{const a=y[e-1],o=t+z.hit[e];return[[t,S(0,0)],[t+c,S(0,1)],[o,S(a-_,1)],[o+T,S(a-M,1)],[o+j,S(a-C,0)],[o+j+.02,S(0,0)]]},O=(t,e,a,o,i,n=0)=>H(t,e,[[0,o],...a.flatMap(t=>((t,e,a,o=0)=>[[t-.03,e],[t+o,a],[t+.55+o,a],[t+A,e]])(t,o,i,n)),[e,o]]),K=(t=Z)=>{const{cycle:e}=t,a=e=>t.sends.filter(t=>t.device===e).map(t=>t.at+z.hit[e]);return[...[1,2,3].flatMap(o=>[H(`knx-reject-${o}`,e,[[0,S(0,0)],...t.sends.filter(t=>t.device===o).flatMap(t=>F(t.at,t.device)),[e,S(0,0)]]),O(`knx-nak-body-${o}`,e,a(o),D,N),O(`knx-nak-led-${o}`,e,a(o),q,W),O(`knx-nak-text-${o}`,e,a(o),B,J,.06)])].join("\n\n  ")},L=(t,e)=>`${t} {\n      ${e}\n    }`;let R,V,X,G,I,Q,Y=t=>t;const tt=(0,i.JW)(R||(R=Y` <svg class="ha-logo" viewBox="0 0 240 240" x="21" y="40" width="30" height="30"> <path class="house" d="M240 224.762a15 15 0 0 1-15 15H15a15 15 0 0 1-15-15v-90c0-8.25 4.77-19.769 10.61-25.609l98.78-98.7805c5.83-5.83 15.38-5.83 21.21 0l98.79 98.7895c5.83 5.83 10.61 17.36 10.61 25.61v90-.01Z"/> <path class="tree" d="m107.27 239.762-40.63-40.63c-2.09.72-4.32 1.13-6.64 1.13-11.3 0-20.5-9.2-20.5-20.5s9.2-20.5 20.5-20.5 20.5 9.2 20.5 20.5c0 2.33-.41 4.56-1.13 6.65l31.63 31.63v-115.88c-6.8-3.3395-11.5-10.3195-11.5-18.3895 0-11.3 9.2-20.5 20.5-20.5s20.5 9.2 20.5 20.5c0 8.07-4.7 15.05-11.5 18.3895v81.27l31.46-31.46c-.62-1.96-.96-4.04-.96-6.2 0-11.3 9.2-20.5 20.5-20.5s20.5 9.2 20.5 20.5-9.2 20.5-20.5 20.5c-2.5 0-4.88-.47-7.09-1.29L129 208.892v30.88z"/> </svg> `)),et=[t=>(0,i.JW)(V||(V=Y` <rect class="glyph fill" x=${0} y="53" width="12" height="3" rx="1.5"/> <rect class="glyph fill" x=${0} y="60" width="12" height="3" rx="1.5"/> `),t-11,t-11),t=>(0,i.JW)(X||(X=Y` <circle class="glyph line" cx=${0} cy="58" r="5.5"/> <line class="glyph line" x1=${0} y1="58" x2=${0} y2="54.5"/> `),t-5,t-5,t-2),t=>(0,i.JW)(G||(G=Y` <circle class="glyph fill" cx=${0} cy="63" r="1.6"/> <path class="glyph line" d="M ${0} 58.5 A 4.5 4.5 0 0 1 ${0} 63"/> <path class="glyph line" d="M ${0} 54 A 9 9 0 0 1 ${0} 63"/> `),t-10,t-10,t-5.5,t-10,t-1)],at=(t,e)=>(0,i.JW)(I||(I=Y` <g class="device device-${0}"> <line class="drop" x1=${0} y1="70" x2=${0} y2="84"/> <rect class="body" x=${0} y="46" width="34" height="24" rx="5"/> ${0} <circle class="led" cx=${0} cy="53" r="2.5"/> </g> `),e,t,t,t-17,et[e-1](t),t+10),ot=(t,e)=>(0,i.JW)(Q||(Q=Y` <g class="ghost ghost-2 ${0}"><circle cx="36" cy="84" r="2.5"/></g> <g class="ghost ghost-1 ${0}"><circle cx="36" cy="84" r="3.2"/></g> <g class="telegram ${0}"> <circle class="halo" cx="36" cy="84" r="9"/> <circle class="dot" cx="36" cy="84" r="4"/> <rect class="badge" x="19" y="94" width="34" height="14" rx="7"/> <text x="36" y="104" text-anchor="middle">${0}</text> </g> `),t,t,t,e);let it,nt,st,rt,lt,ct,ht=t=>t;const dt=P(k),pt={1:120,2:190,3:260},xt="4/0/4",yt={1:"4/0/3",2:"5/0/0",3:"5/0/3"},ut=1e3,gt=2,vt=6,bt=100;class mt extends i.WF{render(){return(0,i.qy)(it||(it=ht` <svg viewBox="0 0 320 118" xmlns="http://www.w3.org/2000/svg"> <line class="bus" x1="12" y1="84" x2="308" y2="84"/> <line class="bus bus-shadow" x1="12" y1="87" x2="308" y2="87"/> <line class="bus-load" x1="12" y1="84" x2="308" y2="84"/> <g class="rate"> <text class="rate-value" x="308" y="27" text-anchor="end">${0}</text> <text class="rate-unit" x="308" y="37" text-anchor="end">${0}</text> </g> <g class="sender"> <line class="drop" x1="36" y1="70" x2="36" y2="84"/> ${0} ${0} </g> ${0} ${0} ${0} <text class="no-ack" x="308" y="79" text-anchor="end">no ACK</text> ${0} ${0} ${0} </svg> `),this._rate,this.rateUnit,(0,s.u)(this._sent,t=>t.id,()=>(0,i.JW)(nt||(nt=ht`<circle class="ripple" cx="36" cy="55" r="16"/>`))),tt,at(pt[1],1),at(pt[2],2),at(pt[3],3),[1,2,3].map(t=>(0,i.JW)(st||(st=ht`<text class="nak nak-${0}" x=${0} y="38" text-anchor="middle">NAK</text>`),t,pt[t])),"error"===this.variant?[1,2,3].map(t=>ot(`scheduled reject-lane-${t}`,yt[t])):Array.from({length:dt},(t,e)=>ot(`scheduled lane-${e}`,xt)),(0,s.u)(this._sent,t=>t.id,this._renderShot))}fire(){if((0,r.r)(l.G,"haptic","light"),this._tapTimes.push(Date.now()),this._updateRate(),this._holdSchedule(),"function"==typeof window.matchMedia&&window.matchMedia("(prefers-reduced-motion: reduce)").matches)return;const t="error"===this.variant?1+Math.floor(3*Math.random()):void 0;this._sent=[...this._sent,{id:this._nextId++,device:t}]}_holdSchedule(){this.busy=!0,window.clearTimeout(this._quietTimer),this._quietTimer=window.setTimeout(()=>{this._quietTimer=void 0,this.busy=!1},1500)}_updateRate(){const t=Date.now()-ut;this._tapTimes=this._tapTimes.filter(e=>e>t),this._rate=this._tapTimes.length;const e=(this._rate-gt)/(vt-gt);this.style.setProperty("--knx-bus-scene-load",String(Math.min(Math.max(e,0),1))),this._tapTimes.length&&void 0===this._rateTick&&(this._rateTick=window.setTimeout(()=>{this._rateTick=void 0,this._updateRate()},bt))}firstUpdated(){this.setAttribute("aria-hidden","true")}disconnectedCallback(){super.disconnectedCallback(),window.clearTimeout(this._rateTick),window.clearTimeout(this._quietTimer),this._rateTick=this._quietTimer=void 0,this.busy=!1}constructor(...t){super(...t),this.variant="not-found",this.busy=!1,this.rateUnit="telegrams/s",this._rate=0,this._sent=[],this._nextId=0,this._tapTimes=[],this._renderShot=({id:t,device:e})=>{if(e){const a=pt[e];return(0,i.JW)(rt||(rt=ht` <g class="shot reject-${0}" data-id=${0} @animationend=${0}> ${0} <rect class="body-echo" x=${0} y="46" width="34" height="24" rx="5"/> <circle class="led-echo" cx=${0} cy="53" r="2.5"/> <text class="nak-echo" x=${0} y="38" text-anchor="middle">NAK</text> </g> `),e,t,this._shotEnded,ot("",yt[e]),a-17,a+10,a)}return(0,i.JW)(lt||(lt=ht` <g class="shot" data-id=${0} @animationend=${0}> ${0} <circle class="led-echo led-echo-1" cx="130" cy="53" r="2.5"/> <circle class="led-echo led-echo-2" cx="200" cy="53" r="2.5"/> <circle class="led-echo led-echo-3" cx="270" cy="53" r="2.5"/> <text class="shot-no-ack" x="308" y="79" text-anchor="end">no ACK</text> </g> `),t,this._shotEnded,ot("",xt))},this._shotEnded=t=>{if("knx-shot-no-ack"!==t.animationName&&"knx-shot-nak"!==t.animationName)return;const e=Number(t.currentTarget.dataset.id);this._sent=this._sent.filter(t=>t.id!==e)}}}mt.styles=(0,i.AH)(ct||(ct=ht`
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
    ${0}

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
  `),(0,i.iz)(((t=k)=>{const e=`${t.cycle}s linear infinite`,a=`${Z.cycle}s linear infinite`,o=t=>`:host([variant="not-found"]) ${t}`,i=t=>`:host([variant="error"]) ${t}`,n=[1,2,3];return[...E(t).map((t,a)=>L(o(`.lane-${a}`),`animation: knx-send-${a} ${e};`)),...n.map(t=>L(o(`.device-${t} .led`),`animation: knx-blink-${t} ${e};`)),L(o(".no-ack"),`animation: knx-no-ack ${e};`),...n.flatMap(t=>[L(i(`.reject-lane-${t}`),`animation: knx-reject-${t} ${a};`),L(i(`.device-${t} .body`),`animation: knx-nak-body-${t} ${a};`),L(i(`.device-${t} .led`),`animation: knx-nak-led-${t} ${a};`),L(i(`.nak-${t}`),`animation: knx-nak-text-${t} ${a};`)]),L(":host([busy]) .scheduled,\n    :host([busy]) .device .led,\n    :host([busy]) .device .body,\n    :host([busy]) .no-ack,\n    :host([busy]) .nak","animation: none;"),L(".shot .telegram,\n    .shot .ghost",`animation: knx-shot ${w.flight}s linear;`),L(".shot .led-echo",`animation: knx-shot-blink ${w.blink}s linear;`),...w.blinkDelays.map((t,e)=>L(`.shot .led-echo-${e+1}`,`animation-delay: ${t.toFixed(3)}s;`)),L(".shot .shot-no-ack",`animation: knx-shot-no-ack ${w.noAck}s linear ${w.noAckDelay}s;`),...n.flatMap(t=>{const e=`${(z.hit[t]-.03).toFixed(3)}s`;return[L(`.shot.reject-${t} .telegram,\n    .shot.reject-${t} .ghost`,`animation: knx-shot-reject-${t} ${z.flight[t].toFixed(3)}s linear;`),L(`.shot.reject-${t} .body-echo`,`animation: knx-shot-nak-body ${z.flash}s linear ${e};`),L(`.shot.reject-${t} .led-echo`,`animation: knx-shot-nak-led ${z.flash}s linear ${e};`),L(`.shot.reject-${t} .nak-echo`,`animation: knx-shot-nak ${z.flash}s linear ${e};`)]}),...$.map((t,e)=>L(`:host .ghost.ghost-${e+1}`,`animation-delay: ${t}s;`)),U(t),[H("knx-shot",w.flight,[[0,S(0,0)],[c,S(0,1)],[c+h,S(p,1)],[w.flight,S(x,0)]]),H("knx-shot-blink",w.blink,[[0,q],[u,W],[u+g,W],[w.blink,q]]),H("knx-shot-no-ack",w.noAck,[[0,J],[m-b,J],[w.noAck,B]])].join("\n\n  "),[...[1,2,3].map(t=>H(`knx-shot-reject-${t}`,z.flight[t],[...F(0,t).slice(0,-1),[z.flight[t],S(0,0)]])),O("knx-shot-nak-body",z.flash,[.03],["stroke-opacity: 0"],["stroke-opacity: 1"]),O("knx-shot-nak-led",z.flash,[.03],B,W),O("knx-shot-nak",z.flash,[.03],B,J,.06)].join("\n\n  "),K()].join("\n\n    ")})())),(0,o.Cg)([(0,n.MZ)({reflect:!0})],mt.prototype,"variant",void 0),(0,o.Cg)([(0,n.MZ)({type:Boolean,reflect:!0})],mt.prototype,"busy",void 0),(0,o.Cg)([(0,n.MZ)({attribute:"rate-unit"})],mt.prototype,"rateUnit",void 0),(0,o.Cg)([(0,n.wk)()],mt.prototype,"_rate",void 0),(0,o.Cg)([(0,n.wk)()],mt.prototype,"_sent",void 0),mt=(0,o.Cg)([(0,n.EM)("knx-bus-scene")],mt)},55565(t,e,a){a.a(t,async function(t,e){try{a(89463),a(23792),a(18111),a(13579),a(3362),a(17642),a(58004),a(33853),a(45876),a(32475),a(15024),a(31698),a(62953);var o=a(15697),i=a(57527),n=a(51209),s=a(22472),r=a(11602),l=a(91230),c=a(77671),h=(a(74054),t([s,r]));[s,r]=h.then?(await h)():h;let d,p,x,y,u,g,v=t=>t;const b="M19,21H8V7H19M19,5H8A2,2 0 0,0 6,7V21A2,2 0 0,0 8,23H19A2,2 0 0,0 21,21V7A2,2 0 0,0 19,5M16,1H4A2,2 0 0,0 2,3V17H4V3H16V1Z",m=new Set(["ha-button","ha-icon-button","button","a","input","select","textarea"]);class f extends i.WF{render(){return(0,i.qy)(d||(d=v` <hass-subpage .hass=${0} .narrow=${0} .header=${0}> <div class="content" @pointerdown=${0}> <knx-bus-scene .variant=${0} .rateUnit=${0}></knx-bus-scene> <h1> ${0} <span class="headline">${0}</span> </h1> ${0} ${0} <div class="actions"><slot></slot></div> </div> </hass-subpage> `),this.hass,this.narrow,this.header,this._tap,this.variant,this.rateUnit,this.eyebrow?(0,i.qy)(p||(p=v`<span class="eyebrow">${0}</span>`),this.eyebrow):i.s6,this.headline,this.description?(0,i.qy)(x||(x=v`<p class="description">${0}</p>`),this.description):i.s6,this.detail?(0,i.qy)(y||(y=v`<div class="detail"> <span class="detail-label">${0}</span> <div class="detail-body"> <code>${0}</code> ${0} </div> </div>`),this.detailLabel,this.detail,this.copyable?(0,i.qy)(u||(u=v`<ha-icon-button .path=${0} label=${0} @click=${0}></ha-icon-button>`),b,this.hass.localize("ui.common.copy"),this._copy):i.s6):i.s6)}_tap(t){if(0!==t.button)return;var e;t.composedPath().some(t=>t instanceof Element&&m.has(t.localName))||(null===(e=this._scene)||void 0===e||e.fire())}async _copy(){await(0,l.l)(this.detail),(0,c.P)(this,{message:this.hass.localize("ui.common.copied_clipboard")})}constructor(...t){super(...t),this.narrow=!1,this.copyable=!1,this.variant="not-found",this.rateUnit="telegrams/s"}}f.styles=(0,i.AH)(g||(g=v`:host{height:100%;display:block}.content{-webkit-tap-highlight-color:transparent;-webkit-touch-callout:none;touch-action:manipulation;user-select:none;box-sizing:border-box;text-align:center;max-width:520px;min-height:100%;color:var(--primary-text-color);flex-direction:column;justify-content:center;align-items:center;margin:0 auto;padding:24px 16px 14vh;display:flex}knx-bus-scene{margin-bottom:28px}h1{font:inherit;margin:0 0 12px}.eyebrow{color:var(--secondary-text-color);font-size:var(--ha-font-size-s,12px);font-weight:var(--ha-font-weight-medium,500);letter-spacing:.14em;text-transform:uppercase;margin:0 0 6px;display:block}.headline{font-family:var(--knx-status-page-headline-font,var(--ha-font-family-body,inherit));font-size:var(--knx-status-page-headline-size,var(--ha-font-size-3xl,28px));font-weight:var(--ha-font-weight-medium,500);line-height:var(--ha-line-height-condensed,1.2);display:block}.description{max-width:42ch;color:var(--secondary-text-color);font-size:var(--ha-font-size-l,16px);line-height:var(--ha-line-height-normal,1.6);margin:0}.detail{text-align:left;width:100%;margin-top:24px}.detail-label{color:var(--secondary-text-color);font-size:var(--ha-font-size-s,12px);font-weight:var(--ha-font-weight-medium,500);letter-spacing:.14em;text-transform:uppercase;margin:0 0 6px 2px;display:block}.detail-body{border-radius:var(--ha-border-radius-md,12px);background:var(--secondary-background-color);align-items:flex-start;gap:4px;padding:8px 6px 8px 14px;display:flex}.detail-body code{font-family:var(--ha-font-family-code,monospace);font-size:var(--ha-font-size-s,12px);line-height:var(--ha-line-height-normal,1.6);color:var(--primary-text-color);overflow-wrap:anywhere;user-select:text;flex:1;padding:6px 0}.detail-body ha-icon-button{--mdc-icon-button-size:36px;--mdc-icon-size:18px;color:var(--secondary-text-color);margin:-2px 0}.actions{flex-wrap:wrap;justify-content:center;gap:8px;margin-top:28px;display:flex}`)),(0,o.Cg)([(0,n.MZ)({attribute:!1})],f.prototype,"hass",void 0),(0,o.Cg)([(0,n.MZ)({type:Boolean})],f.prototype,"narrow",void 0),(0,o.Cg)([(0,n.MZ)()],f.prototype,"header",void 0),(0,o.Cg)([(0,n.MZ)()],f.prototype,"eyebrow",void 0),(0,o.Cg)([(0,n.MZ)()],f.prototype,"headline",void 0),(0,o.Cg)([(0,n.MZ)()],f.prototype,"description",void 0),(0,o.Cg)([(0,n.MZ)({attribute:"detail-label"})],f.prototype,"detailLabel",void 0),(0,o.Cg)([(0,n.MZ)()],f.prototype,"detail",void 0),(0,o.Cg)([(0,n.MZ)({type:Boolean})],f.prototype,"copyable",void 0),(0,o.Cg)([(0,n.MZ)({reflect:!0})],f.prototype,"variant",void 0),(0,o.Cg)([(0,n.MZ)({attribute:"rate-unit"})],f.prototype,"rateUnit",void 0),(0,o.Cg)([(0,n.P)("knx-bus-scene")],f.prototype,"_scene",void 0),f=(0,o.Cg)([(0,n.EM)("knx-status-page")],f),e()}catch(t){e(t)}})},36859(t,e,a){a.a(t,async function(t,o){try{a(23792),a(62953);var i=a(15697),n=a(57527),s=a(51209),r=a(89274),l=a(79537),c=a(55565),h=(a(19465),t([r,c]));[r,c]=h.then?(await h)():h;let d,p=t=>t;class x extends n.WF{_goBack(){(0,l.OE)("/knx")}_goToDashboard(){(0,l.oo)("/knx")}constructor(...t){super(...t),this.narrow=!1}}x.styles=(0,n.AH)(d||(d=p`:host{height:100%;display:block}`)),(0,i.Cg)([(0,s.MZ)({attribute:!1})],x.prototype,"hass",void 0),(0,i.Cg)([(0,s.MZ)({attribute:!1})],x.prototype,"knx",void 0),(0,i.Cg)([(0,s.MZ)({type:Boolean})],x.prototype,"narrow",void 0),(0,i.Cg)([(0,s.MZ)({attribute:!1})],x.prototype,"route",void 0),a.d(e,{F:()=>x}),o()}catch(t){o(t)}})}}]);
//# sourceMappingURL=94312.2556348ea97c8146.js.map