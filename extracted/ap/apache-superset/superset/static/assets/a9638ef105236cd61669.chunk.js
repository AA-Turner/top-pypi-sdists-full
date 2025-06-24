"use strict";(globalThis.webpackChunksuperset=globalThis.webpackChunksuperset||[]).push([[9074],{13686:(e,t,n)=>{n.d(t,{t:()=>m});var a=n(77189);const i=String.raw`\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(?:\.\d+)?(?:(?:[+-]\d\d:\d\d)|Z)?`,l=String.raw`(?:TODAY|NOW)`,r=String.raw`[+-]?[1-9][0-9]*`,o=String.raw`YEAR|QUARTER|MONTH|WEEK|DAY|HOUR|MINUTE|SECOND`,d=RegExp(String.raw`^DATEADD\(DATETIME\("(${i}|${l})"\),\s(${r}),\s(${o})\)$`,"i"),c=RegExp(String.raw`^${i}$|^${l}$`,"i"),s=["now","today"],u=new Date;u.setHours(0,0,0,0);const h=new Date;h.setHours(0,0,0,0);const p={sinceDatetime:u.setDate(u.getDate()-7).toString(),sinceMode:"relative",sinceGrain:"day",sinceGrainValue:-7,untilDatetime:h.toString(),untilMode:"specific",untilGrain:"day",untilGrainValue:7,anchorMode:"now",anchorValue:"now"},m=e=>{const t=e.split(a.wv);if(2===t.length){const[e,n]=t;if(c.test(e)&&c.test(n)){const t=s.includes(e)?e:"specific",a=s.includes(n)?n:"specific";return{customRange:{...p,sinceDatetime:e,untilDatetime:n,sinceMode:t,untilMode:a},matchedFlag:!0}}const a=e.match(d);if(a&&c.test(n)&&e.includes(n)){const[e,t,i]=a.slice(1),l=s.includes(n)?n:"specific";return{customRange:{...p,sinceGrain:i,sinceGrainValue:parseInt(t,10),sinceDatetime:e,untilDatetime:e,sinceMode:"relative",untilMode:l},matchedFlag:!0}}const i=n.match(d);if(c.test(e)&&i&&n.includes(e)){const[t,n,a]=[...i.slice(1)],l=s.includes(e)?e:"specific";return{customRange:{...p,untilGrain:a,untilGrainValue:parseInt(n,10),sinceDatetime:t,untilDatetime:t,untilMode:"relative",sinceMode:l},matchedFlag:!0}}if(a&&i){const[e,t,n]=[...a.slice(1)],[l,r,o]=[...i.slice(1)];if(e===l)return{customRange:{...p,sinceGrain:n,sinceGrainValue:parseInt(t,10),sinceDatetime:e,untilGrain:o,untilGrainValue:parseInt(r,10),untilDatetime:l,anchorValue:e,sinceMode:"relative",untilMode:"relative",anchorMode:"now"===e?"now":"specific"},matchedFlag:!0}}}return{customRange:p,matchedFlag:!1}}},77189:(e,t,n)=>{n.d(t,{wv:()=>s,x9:()=>m});var a=n(62193),i=n.n(a),l=n(58561),r=n.n(l),o=n(62952),d=n(35742),c=n(51436);const s=" : ",u=(e,t)=>`${e}${s}${t}`,h=(e,t)=>e.replace("T00:00:00","")||(t?"-∞":"∞"),p=(e,t="col")=>{const n=e.split(s);return 1===n.length?e:`${h(n[0],!0)} ≤ ${t} < ${h(n[1])}`},m=async(e,t="col",n)=>{let a,l;if(i()(n))a=r().encode_uri(e),l=`/api/v1/time_range/?q=${a}`;else{const t=(0,o.A)(n).map((t=>({timeRange:e,shift:t})));a=r().encode_uri([{timeRange:e},...t]),l=`/api/v1/time_range/?q=${a}`}try{var m;const e=await d.A.get({endpoint:l});if(i()(n)){var v,g,f,b;const n=u((null==e||null==(v=e.json)||null==(g=v.result[0])?void 0:g.since)||"",(null==e||null==(f=e.json)||null==(b=f.result[0])?void 0:b.until)||"");return{value:p(n,t)}}const a=null==e||null==(m=e.json)?void 0:m.result.map((e=>u(e.since,e.until)));return{value:a.slice(1).map((e=>((e,t,n="col")=>{const a=e.split(s),i=t.split(s);return`${n}: ${h(a[0],!0)} to ${h(a[1])} vs\n  ${h(i[0],!0)} to ${h(i[1])}`})(a[0],e,t)))}}catch(e){const t=await(0,c.h4)(e);return{error:t.message||t.error||e.statusText}}}},6094:(e,t,n)=>{n.d(t,{c:()=>o,l:()=>r});var a=n(85973),i=n(17437),l=n(2445);const r=e=>(0,l.Y)(a.A,{css:i.AH`
      width: 100%;
    `,...e}),o=a.A.RangePicker},85955:(e,t,n)=>{n.d(t,{c:()=>l});var a=n(45418),i=n(2445);function l(e){return(0,i.Y)(a.A,{...e})}},10044:(e,t,n)=>{n.d(t,{A:()=>l});var a=n(28073),i=n(2445);const l=e=>(0,i.Y)(a.A,{...e})},22533:(e,t,n)=>{n.d(t,{A:()=>d,v:()=>r});var a=n(96540),i=n(10044),l=n(2445);const r=()=>{var e;return null==(e=document.getElementById("controlSections"))?void 0:e.lastElementChild},o=e=>{var t,n;const a=null==(t=window)?void 0:t.innerHeight,i=null==e||null==(n=e.getBoundingClientRect())?void 0:n.top;return a&&i?i/a:0},d=({getPopupContainer:e,getVisibilityRatio:t=o,visible:n,destroyTooltipOnHide:d=!1,...c})=>{const s=(0,a.useRef)(),[u,h]=(0,a.useState)(void 0===n?c.defaultVisible:n),[p,m]=a.useState("right"),v=(0,a.useCallback)((()=>{const e=t(s.current);m(e<.35&&"rightTop"!==p?"rightTop":e>.65&&"rightBottom"!==p?"rightBottom":"right")}),[t]),g=(0,a.useCallback)((e=>{const t=r();t&&t.style.setProperty("overflow-y",e?"hidden":"auto","important")}),[v]),f=(0,a.useCallback)((t=>(s.current=t,(null==e?void 0:e(t))||document.body)),[v,e]),b=(0,a.useCallback)((e=>{void 0===e&&g(e),h(!!e),null==c.onVisibleChange||c.onVisibleChange(!!e)}),[c,g]),y=(0,a.useCallback)((e=>{"Escape"===e.key&&(h(!1),null==c.onVisibleChange||c.onVisibleChange(!1))}),[c]);return(0,a.useEffect)((()=>{void 0!==n&&h(!!n)}),[n]),(0,a.useEffect)((()=>{void 0!==u&&g(u)}),[u,g]),(0,a.useEffect)((()=>(u&&document.addEventListener("keydown",y),()=>{document.removeEventListener("keydown",y)})),[y,u]),(0,a.useEffect)((()=>{u&&v()}),[u,v]),(0,l.Y)(i.A,{...c,visible:u,arrowPointAtCenter:!0,placement:p,onVisibleChange:b,getPopupContainer:f,destroyTooltipOnHide:d})}},45267:(e,t,n)=>{n.d(t,{A:()=>Z});var a=n(96540),i=n(96453),l=n(17437),r=n(37827),o=n(96627),d=n(77189),c=n(95579),s=n(46920),u=n(50317),h=n(85861),p=n(85955),m=n(12249),v=n(28990),g=n(19129),f=n(85183),b=n(27023),y=n(15151),Y=n(22533),C=n(39942),w=n(69193),D=n(2445);function A(e){let t="Last week";return C.Be.has(e.value)?t=e.value:e.onChange(t),(0,D.FD)(D.FK,{children:[(0,D.Y)("div",{className:"section-title",children:(0,c.t)("Configure Time Range: Last...")}),(0,D.Y)(w.s.GroupWrapper,{spaceConfig:{direction:"vertical",size:15,align:"start",wrap:!1},size:"large",value:t,onChange:t=>e.onChange(t.target.value),options:C.z6})]})}var $=n(7987);function E({onChange:e,value:t}){return(0,a.useEffect)((()=>{C.oo.has(t)||e($.sw)}),[e,t]),C.oo.has(t)?(0,D.FD)(D.FK,{children:[(0,D.Y)("div",{className:"section-title",children:(0,c.t)("Configure Time Range: Previous...")}),(0,D.Y)(w.s.GroupWrapper,{spaceConfig:{direction:"vertical",size:15,align:"start",wrap:!1},size:"large",value:t,onChange:t=>e(t.target.value),options:C.cn})]}):null}function x({onChange:e,value:t}){return(0,a.useEffect)((()=>{C.yI.has(t)||e($.ke)}),[t]),C.yI.has(t)?(0,D.FD)(D.FK,{children:[(0,D.Y)("div",{className:"section-title",children:(0,c.t)("Configure Time Range: Current...")}),(0,D.Y)(w.s.GroupWrapper,{spaceConfig:{direction:"vertical",size:15,align:"start",wrap:!0},size:"large",onChange:t=>{let n=t.target.value;n=n.trim(),""!==n&&e(n)},options:C.ZC})]}):null}var S=n(13686),T=n(66537),F=n(15595),N=n(90868),I=n(6094),V=n(17444),k=n(23807),M=n(28532);function R(e){const{customRange:t,matchedFlag:n}=(0,S.t)(e.value),a=(0,M.Y)();n||e.onChange((0,C.IS)(t));const{sinceDatetime:i,sinceMode:l,sinceGrain:r,sinceGrainValue:o,untilDatetime:d,untilMode:s,untilGrain:u,untilGrainValue:h,anchorValue:p,anchorMode:m}={...t};function g(n,a){e.onChange((0,C.IS)({...t,[n]:a}))}function f(n,a){"number"==typeof a&&Number.isInteger(a)&&a>0&&e.onChange((0,C.IS)({...t,[n]:a}))}return null===a?(0,D.Y)(V.A,{position:"inline-centered"}):(0,D.Y)(k.Q,{locale:a,children:(0,D.FD)("div",{children:[(0,D.Y)("div",{className:"section-title",children:(0,c.t)("Configure custom time range")}),(0,D.FD)(F.fI,{gutter:24,children:[(0,D.FD)(F.fv,{span:12,children:[(0,D.FD)("div",{className:"control-label",children:[(0,c.t)("START (INCLUSIVE)")," ",(0,D.Y)(T.W,{tooltip:(0,c.t)("Start date included in time range"),placement:"right"})]}),(0,D.Y)(v.A,{ariaLabel:(0,c.t)("START (INCLUSIVE)"),options:C.Wm,value:l,onChange:e=>g("sinceMode",e)}),"specific"===l&&(0,D.Y)(F.fI,{children:(0,D.Y)(I.l,{showTime:!0,defaultValue:(0,C.Ab)(i),onChange:e=>g("sinceDatetime",e.format(C.c1)),allowClear:!1,getPopupContainer:t=>e.isOverflowingFilterBar?t.parentNode:document.body})}),"relative"===l&&(0,D.FD)(F.fI,{gutter:8,children:[(0,D.Y)(F.fv,{span:11,children:(0,D.Y)(N.YI,{placeholder:(0,c.t)("Relative quantity"),value:Math.abs(o),min:1,defaultValue:1,onChange:e=>f("sinceGrainValue",e||1),onStep:e=>f("sinceGrainValue",e||1)})}),(0,D.Y)(F.fv,{span:13,children:(0,D.Y)(v.A,{ariaLabel:(0,c.t)("Relative period"),options:C.IZ,value:r,onChange:e=>g("sinceGrain",e)})})]})]}),(0,D.FD)(F.fv,{span:12,children:[(0,D.FD)("div",{className:"control-label",children:[(0,c.t)("END (EXCLUSIVE)")," ",(0,D.Y)(T.W,{tooltip:(0,c.t)("End date excluded from time range"),placement:"right"})]}),(0,D.Y)(v.A,{ariaLabel:(0,c.t)("END (EXCLUSIVE)"),options:C.OP,value:s,onChange:e=>g("untilMode",e)}),"specific"===s&&(0,D.Y)(F.fI,{children:(0,D.Y)(I.l,{showTime:!0,defaultValue:(0,C.Ab)(d),onChange:e=>g("untilDatetime",e.format(C.c1)),allowClear:!1,getPopupContainer:t=>e.isOverflowingFilterBar?t.parentNode:document.body})}),"relative"===s&&(0,D.FD)(F.fI,{gutter:8,children:[(0,D.Y)(F.fv,{span:11,children:(0,D.Y)(N.YI,{placeholder:(0,c.t)("Relative quantity"),value:h,min:1,defaultValue:1,onChange:e=>f("untilGrainValue",e||1),onStep:e=>f("untilGrainValue",e||1)})}),(0,D.Y)(F.fv,{span:13,children:(0,D.Y)(v.A,{ariaLabel:(0,c.t)("Relative period"),options:C.s6,value:u,onChange:e=>g("untilGrain",e)})})]})]})]}),"relative"===l&&"relative"===s&&(0,D.FD)("div",{className:"control-anchor-to",children:[(0,D.Y)("div",{className:"control-label",children:(0,c.t)("Anchor to")}),(0,D.FD)(F.fI,{align:"middle",children:[(0,D.Y)(F.fv,{children:(0,D.Y)(w.s.GroupWrapper,{options:[{value:"now",label:(0,c.t)("Now")},{value:"specific",label:(0,c.t)("Date/Time")}],onChange:function(n){const a=n.target.value;"now"===a?e.onChange((0,C.IS)({...t,anchorValue:"now",anchorMode:a})):e.onChange((0,C.IS)({...t,anchorValue:C.bd,anchorMode:a}))},defaultValue:"now",value:m})}),"now"!==m&&(0,D.Y)(F.fv,{children:(0,D.Y)(I.l,{showTime:!0,defaultValue:(0,C.Ab)(p),onChange:e=>g("anchorValue",e.format(C.c1)),allowClear:!1,className:"control-anchor-to-datetime",getPopupContainer:t=>e.isOverflowingFilterBar?t.parentNode:document.body})})]})]})]})})}const L=(0,D.FD)(D.FK,{children:[(0,D.FD)("div",{children:[(0,D.Y)("h3",{children:"DATETIME"}),(0,D.Y)("p",{children:(0,c.t)("Return to specific datetime.")}),(0,D.Y)("h4",{children:(0,c.t)("Syntax")}),(0,D.Y)("pre",{children:(0,D.Y)("code",{children:"datetime([string])"})}),(0,D.Y)("h4",{children:(0,c.t)("Example")}),(0,D.Y)("pre",{children:(0,D.Y)("code",{children:'datetime("2020-03-01 12:00:00")\ndatetime("now")\ndatetime("last year")'})})]}),(0,D.FD)("div",{children:[(0,D.Y)("h3",{children:"DATEADD"}),(0,D.Y)("p",{children:(0,c.t)("Moves the given set of dates by a specified interval.")}),(0,D.Y)("h4",{children:(0,c.t)("Syntax")}),(0,D.Y)("pre",{children:(0,D.Y)("code",{children:"dateadd([datetime], [integer], [dateunit])\ndateunit = (year | quarter | month | week | day | hour | minute | second)"})}),(0,D.Y)("h4",{children:(0,c.t)("Example")}),(0,D.Y)("pre",{children:(0,D.Y)("code",{children:'dateadd(datetime("today"), -13, day)\ndateadd(datetime("2020-03-01"), 2, day)'})})]}),(0,D.FD)("div",{children:[(0,D.Y)("h3",{children:"DATETRUNC"}),(0,D.Y)("p",{children:(0,c.t)("Truncates the specified date to the accuracy specified by the date unit.")}),(0,D.Y)("h4",{children:(0,c.t)("Syntax")}),(0,D.Y)("pre",{children:(0,D.Y)("code",{children:"datetrunc([datetime], [dateunit])\ndateunit = (year | quarter | month | week)"})}),(0,D.Y)("h4",{children:(0,c.t)("Example")}),(0,D.Y)("pre",{children:(0,D.Y)("code",{children:'datetrunc(datetime("2020-03-01"), week)\ndatetrunc(datetime("2020-03-01"), month)'})})]}),(0,D.FD)("div",{children:[(0,D.Y)("h3",{children:"LASTDAY"}),(0,D.Y)("p",{children:(0,c.t)("Get the last date by the date unit.")}),(0,D.Y)("h4",{children:(0,c.t)("Syntax")}),(0,D.Y)("pre",{children:(0,D.Y)("code",{children:"lastday([datetime], [dateunit])\ndateunit = (year | month | week)"})}),(0,D.Y)("h4",{children:(0,c.t)("Example")}),(0,D.Y)("pre",{children:(0,D.Y)("code",{children:'lastday(datetime("today"), month)'})})]}),(0,D.FD)("div",{children:[(0,D.Y)("h3",{children:"HOLIDAY"}),(0,D.Y)("p",{children:(0,c.t)("Get the specify date for the holiday")}),(0,D.Y)("h4",{children:(0,c.t)("Syntax")}),(0,D.Y)("pre",{children:(0,D.Y)("code",{children:"holiday([string])\nholiday([holiday string], [datetime])\nholiday([holiday string], [datetime], [country name])"})}),(0,D.Y)("h4",{children:(0,c.t)("Example")}),(0,D.Y)("pre",{children:(0,D.Y)("code",{children:'holiday("new year")\nholiday("christmas", datetime("2019"))\nholiday("christmas", dateadd(datetime("2019"), 1, year))\nholiday("christmas", datetime("2 years ago"))\nholiday("Easter Monday", datetime("2019"), "UK")'})})]})]}),G=e=>{const t=(0,i.DP)();return(0,D.Y)(l.Z2,{children:({css:n})=>(0,D.Y)(g.m_,{overlayClassName:n`
            .antd5-tooltip-content {
              min-width: ${125*t.gridUnit}px;
              max-height: 410px;
              overflow-y: scroll;

              .antd5-tooltip-inner {
                max-width: ${125*t.gridUnit}px;
                h3 {
                  font-size: ${t.typography.sizes.m}px;
                  font-weight: ${t.typography.weights.bold};
                }
                h4 {
                  font-size: ${t.typography.sizes.m}px;
                  font-weight: ${t.typography.weights.bold};
                }
                pre {
                  border: none;
                  text-align: left;
                  word-break: break-word;
                  font-size: ${t.typography.sizes.s}px;
                }
              }
            }
          `,...e})})};function O(e){return(0,D.Y)(G,{title:L,...e})}function P(e){return e.includes(d.wv)?e:e.startsWith("Last")?[e,""].join(d.wv):e.startsWith("Next")?["",e].join(d.wv):d.wv}function W(e){const t=P(e.value||""),[n,a]=t.split(d.wv);function i(t,i){"since"===t?e.onChange(`${i}${d.wv}${a}`):e.onChange(`${n}${d.wv}${i}`)}return t!==e.value&&e.onChange(P(e.value||"")),(0,D.FD)(D.FK,{children:[(0,D.FD)("div",{className:"section-title",children:[(0,c.t)("Configure Advanced Time Range "),(0,D.Y)(O,{placement:"rightBottom",children:(0,D.Y)("i",{className:"fa fa-info-circle text-muted"})})]}),(0,D.FD)("div",{className:"control-label",children:[(0,c.t)("START (INCLUSIVE)")," ",(0,D.Y)(T.W,{tooltip:(0,c.t)("Start date included in time range"),placement:"right"})]}),(0,D.Y)(N.pd,{value:n,onChange:e=>i("since",e.target.value)},"since"),(0,D.FD)("div",{className:"control-label",children:[(0,c.t)("END (EXCLUSIVE)")," ",(0,D.Y)(T.W,{tooltip:(0,c.t)("End date excluded from time range"),placement:"right"})]}),(0,D.Y)(N.pd,{value:a,onChange:e=>i("until",e.target.value)},"until")]})}const z="#45BED6",B=i.I4.div`
  ${({theme:e,isActive:t,isPlaceholder:n})=>l.AH`
    width: 100%;
    height: ${8*e.gridUnit}px;

    display: flex;
    align-items: center;
    flex-wrap: nowrap;

    padding: 0 ${3*e.gridUnit}px;

    background-color: ${e.colors.grayscale.light5};

    border: 1px solid
      ${t?z:e.colors.grayscale.light2};
    border-radius: ${e.borderRadius}px;

    cursor: pointer;

    transition: border-color 0.3s cubic-bezier(0.65, 0.05, 0.36, 1);
    :hover,
    :focus {
      border-color: ${z};
    }

    .date-label-content {
      color: ${n?e.colors.grayscale.light1:e.colors.grayscale.dark1};
      overflow: hidden;
      text-overflow: ellipsis;
      min-width: 0;
      flex-shrink: 1;
      white-space: nowrap;
    }

    span[role='img'] {
      margin-left: auto;
      padding-left: ${e.gridUnit}px;

      & > span[role='img'] {
        line-height: 0;
      }
    }
  `}
`,U=(0,a.forwardRef)(((e,t)=>{const n=(0,i.DP)();return(0,D.FD)(B,{...e,tabIndex:0,role:"button",children:[(0,D.Y)("span",{id:`date-label-${e.name}`,className:"date-label-content",ref:t,children:"string"==typeof e.label?(0,c.t)(e.label):e.label}),(0,D.Y)(m.A.CalendarOutlined,{iconSize:"s",iconColor:n.colors.grayscale.base})]})})),H=(0,i.I4)(v.A)`
  width: 272px;
`,_=i.I4.div`
  ${({theme:e})=>l.AH`
    .ant-row {
      margin-top: 8px;
    }

    .antd5-input-number {
      width: 100%;
    }

    .ant-picker {
      padding: 4px 17px 4px;
      border-radius: 4px;
      width: 100%;
    }

    .antd5-divider-horizontal {
      margin: 16px 0;
    }

    .control-label {
      font-size: 11px;
      font-weight: ${e.typography.weights.medium};
      color: ${e.colors.grayscale.light2};
      line-height: 16px;
      margin: 8px 0;
    }

    .section-title {
      font-style: normal;
      font-weight: ${e.typography.weights.bold};
      font-size: 15px;
      line-height: 24px;
      margin-bottom: 8px;
    }

    .control-anchor-to {
      margin-top: 16px;
    }

    .control-anchor-to-datetime {
      width: 217px;
    }

    .footer {
      text-align: right;
    }
  `}
`,q=i.I4.span`
  span {
    margin-right: ${({theme:e})=>2*e.gridUnit}px;
    vertical-align: middle;
  }
  .text {
    vertical-align: middle;
  }
  .error {
    color: ${({theme:e})=>e.colors.error.base};
  }
`,K=(e,t,n)=>e?(0,D.FD)("div",{children:[t&&(0,D.Y)("strong",{children:t}),n&&(0,D.Y)("div",{css:e=>l.AH`
            margin-top: ${e.gridUnit}px;
          `,children:n})]}):n||null;function Z(e){var t;const{name:n,onChange:l,onOpenPopover:v=y.fZ,onClosePopover:w=y.fZ,overlayStyle:$="Popover",isOverflowingFilterBar:S=!1}=e,T=(0,C.IM)(),F=null!=(t=e.value)?t:T,[N,I]=(0,a.useState)(F),[V,k]=(0,a.useState)(!1),M=(0,a.useMemo)((()=>(0,C.J5)(F)),[F]),[L,G]=(0,a.useState)(M),[O,P]=(0,a.useState)(F),[z,B]=(0,a.useState)(F),[Z,X]=(0,a.useState)(!1),[J,j]=(0,a.useState)(F),[Q,ee]=(0,a.useState)(F),te=(0,i.DP)(),[ne,ae]=(0,r.A)();function ie(){B(F),G(M),k(!1),w()}(0,a.useEffect)((()=>{if(F===o.WC)return I(o.WC),ee(null),void X(!0);(0,d.x9)(F).then((({value:e,error:t})=>{t?(j(t||""),X(!1),ee(F||null)):("Common"===M||"Calendar"===M||"Current"===M||"No filter"===M?(I(F),ee(K(ae,F,e))):(I(e||""),ee(K(ae,e,F))),X(!0)),P(F),j(e||F)}))}),[M,ae,ne,F]),(0,f.sv)((()=>{if(z===o.WC)return j(o.WC),P(o.WC),void X(!0);O!==z&&(0,d.x9)(z).then((({value:e,error:t})=>{t?(j(t||""),X(!1)):(j(e||""),X(!0)),P(z)}))}),b.Qs,[z]);const le=()=>{V?ie():(B(F),G(M),k(!0),v())},re=(0,D.FD)(_,{children:[(0,D.Y)("div",{className:"control-label",children:(0,c.t)("RANGE TYPE")}),(0,D.Y)(H,{ariaLabel:(0,c.t)("RANGE TYPE"),options:C.BJ,value:L,onChange:function(e){e===o.WC&&B(o.WC),G(e)}}),"No filter"!==L&&(0,D.Y)(p.c,{}),"Common"===L&&(0,D.Y)(A,{value:z,onChange:B}),"Calendar"===L&&(0,D.Y)(E,{value:z,onChange:B}),"Current"===L&&(0,D.Y)(x,{value:z,onChange:B}),"Advanced"===L&&(0,D.Y)(W,{value:z,onChange:B}),"Custom"===L&&(0,D.Y)(R,{value:z,onChange:B,isOverflowingFilterBar:S}),"No filter"===L&&(0,D.Y)("div",{}),(0,D.Y)(p.c,{}),(0,D.FD)("div",{children:[(0,D.Y)("div",{className:"section-title",children:(0,c.t)("Actual time range")}),Z&&(0,D.Y)("div",{children:"No filter"===J?(0,c.t)("No filter"):J}),!Z&&(0,D.FD)(q,{className:"warning",children:[(0,D.Y)(m.A.ErrorSolidSmall,{iconColor:te.colors.error.base}),(0,D.Y)("span",{className:"text error",children:J})]})]}),(0,D.Y)(p.c,{}),(0,D.FD)("div",{className:"footer",children:[(0,D.Y)(s.A,{buttonStyle:"secondary",cta:!0,onClick:ie,children:(0,c.t)("CANCEL")},"cancel"),(0,D.Y)(s.A,{buttonStyle:"primary",cta:!0,disabled:!Z,onClick:function(){l(z),k(!1),w()},children:(0,c.t)("APPLY")},"apply")]})]}),oe=(0,D.FD)(q,{children:[(0,D.Y)(m.A.EditAlt,{iconColor:te.colors.grayscale.base}),(0,D.Y)("span",{className:"text",children:(0,c.t)("Edit time range")})]}),de=(0,D.Y)(Y.A,{placement:"right",trigger:"click",content:re,title:oe,defaultVisible:V,visible:V,onVisibleChange:le,overlayStyle:{width:"600px"},getPopupContainer:e=>S?e.parentNode:document.body,destroyTooltipOnHide:!0,children:(0,D.Y)(g.m_,{placement:"top",title:Q,children:(0,D.Y)(U,{name:n,"aria-labelledby":`filter-name-${e.name}`,"aria-describedby":`date-label-${e.name}`,label:N,isActive:V,isPlaceholder:N===o.WC,ref:ne})})}),ce=(0,D.FD)(D.FK,{children:[(0,D.Y)(g.m_,{placement:"top",title:Q,children:(0,D.Y)(U,{name:n,"aria-labelledby":`filter-name-${e.name}`,"aria-describedby":`date-label-${e.name}`,onClick:le,label:N,isActive:V,isPlaceholder:N===o.WC,ref:ne})}),(0,D.Y)(h.Ay,{title:oe,show:V,onHide:le,width:"600px",hideFooter:!0,zIndex:1030,children:re})]});return(0,D.FD)(D.FK,{children:[(0,D.Y)(u.A,{...e}),"Modal"===$?ce:de]})}},39074:(e,t,n)=>{n.d(t,{Ay:()=>a.A});var a=n(45267);n(39942)},7987:(e,t,n)=>{n.d(t,{RV:()=>s,be:()=>r,cJ:()=>c,ke:()=>d,kw:()=>u,o6:()=>l,oF:()=>i,sw:()=>a,u_:()=>o});const a="previous calendar week",i="previous calendar month",l="previous calendar quarter",r="previous calendar year",o="Current day",d="Current week",c="Current month",s="Current year",u="Current quarter"},39942:(e,t,n)=>{n.d(t,{cn:()=>c,oo:()=>y,nS:()=>s,z6:()=>o,Be:()=>b,OL:()=>d,yI:()=>Y,ZC:()=>u,Ex:()=>h,c1:()=>C,BJ:()=>r,bd:()=>w,IZ:()=>m,Wm:()=>g,s6:()=>v,OP:()=>f,IS:()=>T,Ab:()=>x,J5:()=>V,IM:()=>k});var a=n(7089),i=n(95579),l=n(7987);const r=[{value:"Common",label:(0,i.t)("Last")},{value:"Calendar",label:(0,i.t)("Previous")},{value:"Current",label:(0,i.t)("Current")},{value:"Custom",label:(0,i.t)("Custom")},{value:"Advanced",label:(0,i.t)("Advanced")},{value:"No filter",label:(0,i.t)("No filter")}],o=[{value:"Last day",label:(0,i.t)("Last day")},{value:"Last week",label:(0,i.t)("Last week")},{value:"Last month",label:(0,i.t)("Last month")},{value:"Last quarter",label:(0,i.t)("Last quarter")},{value:"Last year",label:(0,i.t)("Last year")}],d=new Set(o.map((e=>e.value))),c=[{value:l.sw,label:(0,i.t)("previous calendar week")},{value:l.oF,label:(0,i.t)("previous calendar month")},{value:l.o6,label:(0,i.t)("previous calendar quarter")},{value:l.be,label:(0,i.t)("previous calendar year")}],s=new Set(c.map((e=>e.value))),u=[{value:l.u_,label:(0,i.t)("Current day")},{value:l.ke,label:(0,i.t)("Current week")},{value:l.cJ,label:(0,i.t)("Current month")},{value:l.kw,label:(0,i.t)("Current quarter")},{value:l.RV,label:(0,i.t)("Current year")}],h=new Set(u.map((e=>e.value))),p=[{value:"second",label:e=>(0,i.t)("Seconds %s",e)},{value:"minute",label:e=>(0,i.t)("Minutes %s",e)},{value:"hour",label:e=>(0,i.t)("Hours %s",e)},{value:"day",label:e=>(0,i.t)("Days %s",e)},{value:"week",label:e=>(0,i.t)("Weeks %s",e)},{value:"month",label:e=>(0,i.t)("Months %s",e)},{value:"quarter",label:e=>(0,i.t)("Quarters %s",e)},{value:"year",label:e=>(0,i.t)("Years %s",e)}],m=p.map((e=>({value:e.value,label:e.label((0,i.t)("Before"))}))),v=p.map((e=>({value:e.value,label:e.label((0,i.t)("After"))}))),g=[{value:"specific",label:(0,i.t)("Specific Date/Time")},{value:"relative",label:(0,i.t)("Relative Date/Time")},{value:"now",label:(0,i.t)("Now")},{value:"today",label:(0,i.t)("Midnight")}],f=g.slice(),b=new Set(["Last day","Last week","Last month","Last quarter","Last year"]),y=new Set([l.sw,l.oF,l.o6,l.be]),Y=new Set([l.u_,l.ke,l.cJ,l.kw,l.RV]),C="YYYY-MM-DD[T]HH:mm:ss",w=((0,a.XV)().utc().startOf("day").subtract(7,"days").format(C),(0,a.XV)().utc().startOf("day").format(C));var D;!function(e){e.CommonFrame="common-frame",e.ModalOverlay="modal-overlay",e.PopoverOverlay="time-range-trigger",e.NoFilter="no-filter",e.CancelButton="cancel-button",e.ApplyButton="date-filter-control__apply-button"}(D||(D={}));const A=String.raw`\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(?:\.\d+)?(?:(?:[+-]\d\d:\d\d)|Z)?`,$=String.raw`(?:TODAY|NOW)`,E=(RegExp(String.raw`^${A}$|^${$}$`,"i"),["specific","today","now"]),x=e=>"now"===e?(0,a.XV)().utc().startOf("second"):"today"===e?(0,a.XV)().utc().startOf("day"):(0,a.XV)(e),S=e=>x(e).format(C),T=e=>{const{sinceDatetime:t,sinceMode:n,sinceGrain:a,sinceGrainValue:i,untilDatetime:l,untilMode:r,untilGrain:o,untilGrainValue:d,anchorValue:c}={...e};if(E.includes(n)&&E.includes(r))return`${"specific"===n?S(t):n} : ${"specific"===r?S(l):r}`;if(E.includes(n)&&"relative"===r){const e="specific"===n?S(t):n;return`${e} : DATEADD(DATETIME("${e}"), ${d}, ${o})`}if("relative"===n&&E.includes(r)){const e="specific"===r?S(l):r;return`DATEADD(DATETIME("${e}"), ${-Math.abs(i)}, ${a}) : ${e}`}return`DATEADD(DATETIME("${c}"), ${-Math.abs(i)}, ${a}) : DATEADD(DATETIME("${c}"), ${d}, ${o})`};var F=n(96627),N=n(13686),I=n(61225);const V=e=>d.has(e)?"Common":s.has(e)?"Calendar":h.has(e)?"Current":e===F.WC?"No filter":(0,N.t)(e).matchedFlag?"Custom":"Advanced";function k(){var e;return null!=(e=(0,I.d4)((e=>{var t,n;return null==e||null==(t=e.common)||null==(n=t.conf)?void 0:n.DEFAULT_TIME_FILTER})))?e:F.WC}},28532:(e,t,n)=>{n.d(t,{Y:()=>d});var a=n(74353),i=n.n(a),l=n(96540),r=n(61225);n(65826),n(813),n(47317),n(33900),n(16033),n(50952),n(50494),n(72369),n(92218),n(62796),n(88003),n(46847),n(39998),n(69423);const o={en:()=>n.e(5543).then(n.bind(n,75543)),fr:()=>n.e(6930).then(n.bind(n,26930)),es:()=>n.e(254).then(n.bind(n,70254)),it:()=>n.e(2432).then(n.bind(n,32432)),zh:()=>n.e(2441).then(n.bind(n,32441)),ja:()=>n.e(2963).then(n.bind(n,72963)),de:()=>n.e(5700).then(n.bind(n,5700)),pt:()=>n.e(126).then(n.bind(n,40126)),pt_BR:()=>n.e(3898).then(n.bind(n,3898)),ru:()=>n.e(12).then(n.bind(n,10012)),ko:()=>n.e(9605).then(n.bind(n,39605)),sk:()=>n.e(3266).then(n.bind(n,3266)),sl:()=>n.e(1271).then(n.bind(n,41271)),nl:()=>n.e(9414).then(n.bind(n,9414))},d=()=>{const[e,t]=(0,l.useState)(null),n=(0,r.d4)((e=>{var t;return null==e||null==(t=e.common)?void 0:t.locale}));return(0,l.useEffect)((()=>{null===e&&(n&&o[n]?o[n]().then((e=>{t(e.default),i().locale(n)})).catch((()=>t(void 0))):t(void 0))}),[e,n]),e}}}]);