(globalThis.webpackChunksuperset=globalThis.webpackChunksuperset||[]).push([[9897],{19593:e=>{const t=[null];e.exports=t.length<=1?t[0]:t},9450:(e,t,n)=>{"use strict";n.d(t,{E:()=>a});class r{constructor(e){if(this.cache=void 0,this.capacity=void 0,e<1)throw new Error("The capacity in LRU must be greater than 0.");this.capacity=e,this.cache=new Map}has(e){return this.cache.has(e)}get(e){if("string"!=typeof e)throw new TypeError("The LRUCache key must be string.");if(this.cache.has(e)){const t=this.cache.get(e);return this.cache.delete(e),this.cache.set(e,t),t}}set(e,t){if("string"!=typeof e)throw new TypeError("The LRUCache key must be string.");this.cache.size>=this.capacity&&this.cache.delete(this.cache.keys().next().value),this.cache.set(e,t)}clear(){this.cache.clear()}get size(){return this.cache.size}values(){return[...this.cache.values()]}}function a(e=100){return new r(e)}},24976:(e,t,n)=>{"use strict";n.d(t,{_p:()=>w,rN:()=>v,pw:()=>b,iN:()=>x,nt:()=>f,YU:()=>g,S9:()=>y,jS:()=>u});var r=n(96540),a=n(49262),o=n(86963),i=n(96453),s=n(17437),l=n(2445),d=n(37057),c=n(15595);const p=({title:e,icon:t,body:n,meta:r,footer:a})=>(0,l.FD)("div",{className:"tooltip-detail",children:[(0,l.FD)("div",{className:"tooltip-detail-head",children:[(0,l.FD)("div",{className:"tooltip-detail-title",children:[t,e]}),r&&(0,l.Y)("span",{className:"tooltip-detail-meta",children:(0,l.Y)(c.vw,{color:"default",children:r})})]}),n&&(0,l.Y)("div",{className:"tooltip-detail-body",children:null!=n?n:e}),a&&(0,l.Y)("div",{className:"tooltip-detail-footer",children:a})]}),u=e=>`${(0,d.renderToStaticMarkup)((0,l.Y)(p,{...e}))}`,h={"mode/sql":()=>n.e(2514).then(n.t.bind(n,32514,23)),"mode/markdown":()=>Promise.all([n.e(7472),n.e(9620),n.e(9846),n.e(7613)]).then(n.t.bind(n,7613,23)),"mode/css":()=>Promise.all([n.e(9620),n.e(9994)]).then(n.t.bind(n,29994,23)),"mode/json":()=>n.e(9118).then(n.t.bind(n,59118,23)),"mode/yaml":()=>n.e(7215).then(n.t.bind(n,97215,23)),"mode/html":()=>Promise.all([n.e(7472),n.e(9620),n.e(9846),n.e(6861)]).then(n.t.bind(n,56861,23)),"mode/javascript":()=>Promise.all([n.e(7472),n.e(8263)]).then(n.t.bind(n,8263,23)),"theme/textmate":()=>n.e(2694).then(n.t.bind(n,52694,23)),"theme/github":()=>n.e(3139).then(n.t.bind(n,83139,23)),"ext/language_tools":()=>n.e(6464).then(n.t.bind(n,6464,23)),"ext/searchbox":()=>n.e(8949).then(n.t.bind(n,88949,23))};function m(e,{defaultMode:t,defaultTheme:d,defaultTabSize:c=2,fontFamily:p="Menlo, Consolas, Courier New, Ubuntu Mono, source-code-pro, Lucida Console, monospace",placeholder:u}={}){return(0,a.A)((async()=>{var a,u;const m=Promise.all([n.e(8096),n.e(952),n.e(1541)]).then(n.bind(n,70470)),g=n.e(952).then(n.t.bind(n,80952,23)),b=n.e(61).then(n.t.bind(n,70061,17)),f=n.e(4987).then(n.t.bind(n,34987,23)),[{default:y},{config:v},{default:x},{acequire:w}]=await Promise.all([m,g,b,f]);v.setModuleUrl("ace/mode/css_worker",x),await Promise.all(e.map((e=>h[e]())));const $=t||(null==(a=e.find((e=>e.startsWith("mode/"))))?void 0:a.replace("mode/","")),_=d||(null==(u=e.find((e=>e.startsWith("theme/"))))?void 0:u.replace("theme/",""));return(0,r.forwardRef)((function({keywords:e,mode:t=$,theme:n=_,tabSize:a=c,defaultValue:d="",...u},h){const m=(0,i.DP)(),g=w("ace/ext/language_tools"),b=(0,o.A)((e=>{const n={getCompletions:(n,r,a,o,i)=>{Number.isNaN(parseInt(o,10))&&r.getMode().$id===`ace/mode/${t}`&&i(null,e)}};g.setCompleters([n])}));return(0,r.useEffect)((()=>{e&&b(e)}),[e,b]),(0,l.FD)(l.FK,{children:[(0,l.Y)(s.mL,{styles:s.AH`
                .ace_tooltip {
                  margin-left: ${2*m.gridUnit}px;
                  padding: 0px;
                  border: 1px solid ${m.colors.grayscale.light1};
                }

                & .tooltip-detail {
                  background-color: ${m.colors.grayscale.light5};
                  white-space: pre-wrap;
                  word-break: break-all;
                  min-width: ${50*m.gridUnit}px;
                  max-width: ${100*m.gridUnit}px;
                  & .tooltip-detail-head {
                    background-color: ${m.colors.grayscale.light4};
                    color: ${m.colors.grayscale.dark1};
                    display: flex;
                    column-gap: ${m.gridUnit}px;
                    align-items: baseline;
                    justify-content: space-between;
                  }
                  & .tooltip-detail-title {
                    display: flex;
                    column-gap: ${m.gridUnit}px;
                  }
                  & .tooltip-detail-body {
                    word-break: break-word;
                  }
                  & .tooltip-detail-head,
                  & .tooltip-detail-body {
                    padding: ${m.gridUnit}px
                      ${2*m.gridUnit}px;
                  }
                  & .tooltip-detail-footer {
                    border-top: 1px ${m.colors.grayscale.light2}
                      solid;
                    padding: 0 ${2*m.gridUnit}px;
                    color: ${m.colors.grayscale.dark1};
                    font-size: ${m.typography.sizes.xs}px;
                  }
                  & .tooltip-detail-meta {
                    & > .ant-tag {
                      margin-right: 0px;
                    }
                  }
                }
              `}),(0,l.Y)(y,{ref:h,mode:t,theme:n,tabSize:a,defaultValue:d,setOptions:{fontFamily:p},...u})]})}))}),u)}const g=m(["mode/sql","theme/github","ext/language_tools","ext/searchbox"]),b=m(["mode/sql","theme/github","ext/language_tools","ext/searchbox"],{placeholder:()=>(0,l.FD)("div",{style:{height:"100%"},children:[(0,l.Y)("div",{style:{width:41,height:"100%",background:"#e8e8e8"}}),(0,l.Y)("div",{className:"ace_content"})]})}),f=m(["mode/markdown","theme/textmate"]),y=m(["mode/markdown","mode/sql","mode/json","mode/html","mode/javascript","theme/textmate"]),v=m(["mode/css","theme/github"]),x=m(["mode/json","theme/github"]),w=m(["mode/json","mode/yaml","theme/github"])},49262:(e,t,n)=>{"use strict";n.d(t,{A:()=>s});var r=n(96540),a=n(17444),o=n(2445);function i({width:e,height:t,showLoadingForImport:n=!1,placeholderStyle:r}){return t&&(0,o.Y)("div",{style:{width:e,height:t,...r},children:n&&(0,o.Y)(a.A,{position:"floating"})},"async-asm-placeholder")||null}function s(e,t=i){let n,a;function s(){return n||(n=e instanceof Promise?e:e()),a||n.then((e=>{a=e.default||e})),n}const l=(0,r.forwardRef)((function(e,n){const[i,l]=(0,r.useState)(void 0!==a);(0,r.useEffect)((()=>{let e=!0;return i||s().then((()=>{e&&l(!0)})),()=>{e=!1}}));const d=a||t;return d?(0,o.Y)(d,{ref:d===a?n:null,...e}):null}));return l.preload=s,l}},61693:(e,t,n)=>{"use strict";n.d(t,{A:()=>i});var r=n(96453),a=n(38510),o=n(2445);const i=Object.assign((0,r.I4)((({light:e,bigger:t,bold:n,animateArrows:r,...i})=>(0,o.Y)(a.A,{...i})))`
    .ant-collapse-item {
      .ant-collapse-header {
        font-weight: ${({bold:e,theme:t})=>e?t.typography.weights.bold:t.typography.weights.normal};
        font-size: ${({bigger:e,theme:t})=>e?4*t.gridUnit+"px":"inherit"};

        .ant-collapse-arrow svg {
          transition: ${({animateArrows:e})=>e?"transform 0.24s":"none"};
        }

        ${({expandIconPosition:e})=>e&&"right"===e&&"\n            .anticon.anticon-right.ant-collapse-arrow > svg {\n              transform: rotate(90deg) !important;\n            }\n          "}

        ${({light:e,theme:t})=>e&&`\n            color: ${t.colors.grayscale.light4};\n            .ant-collapse-arrow svg {\n              color: ${t.colors.grayscale.light4};\n            }\n          `}

        ${({ghost:e,bordered:t,theme:n})=>e&&t&&`\n            border-bottom: 1px solid ${n.colors.grayscale.light3};\n          `}
      }
      .ant-collapse-content {
        .ant-collapse-content-box {
          .loading.inline {
            margin: ${({theme:e})=>12*e.gridUnit}px auto;
            display: block;
          }
        }
      }
    }
    .ant-collapse-item-active {
      .ant-collapse-header {
        ${({expandIconPosition:e})=>e&&"right"===e&&"\n            .anticon.anticon-right.ant-collapse-arrow > svg {\n              transform: rotate(-90deg) !important;\n            }\n          "}
      }
    }
  `,{Panel:a.A.Panel})},79427:(e,t,n)=>{"use strict";n.d(t,{A:()=>l});var r=n(95579),a=n(42498),o=n(58999),i=n(2445);const s=(0,r.t)("Unexpected error");function l({title:e=s,error:t,subtitle:n,link:l,stackTrace:d,source:c,description:p,descriptionDetails:u,fallback:h,compact:m}){if(t){const e=(0,a.A)().get(t.error_type);if(e)return(0,i.Y)(e,{compact:m,error:t,source:c,subtitle:n})}if(h)return(0,i.Y)(i.FK,{children:h});const g=u||(l||d?(0,i.FD)(i.FK,{children:[l&&(0,i.Y)("a",{href:l,target:"_blank",rel:"noopener noreferrer",children:(0,r.t)("Request Access")}),(0,i.Y)("br",{}),d&&(0,i.Y)("pre",{children:d})]}):void 0);return(0,i.Y)(o.A,{type:"error",errorType:e,message:n,description:p,descriptionDetails:g,compact:m})}},42498:(e,t,n)=>{"use strict";n.d(t,{A:()=>i});var r=n(25373),a=n(70360);class o extends r.A{constructor(){super({name:"ErrorMessageComponent",overwritePolicy:r.m.Allow})}}const i=(0,a.A)(o)},40458:(e,t,n)=>{"use strict";n.d(t,{A:()=>s});var r=n(96453),a=n(2445);const o=r.I4.label`
  font-size: ${({theme:e})=>e.typography.sizes.s}px;
  color: ${({theme:e})=>e.colors.grayscale.base};
  margin-bottom: ${({theme:e})=>e.gridUnit}px;
`,i=r.I4.label`
  font-size: ${({theme:e})=>e.typography.sizes.s}px;
  color: ${({theme:e})=>e.colors.grayscale.base};
  margin-bottom: ${({theme:e})=>e.gridUnit}px;
  &::after {
    display: inline-block;
    margin-left: ${({theme:e})=>e.gridUnit}px;
    color: ${({theme:e})=>e.colors.error.base};
    font-size: ${({theme:e})=>e.typography.sizes.m}px;
    content: '*';
  }
`;function s({children:e,htmlFor:t,required:n=!1,className:r}){const s=n?i:o;return(0,a.Y)(s,{htmlFor:t,className:r,children:e})}},97987:(e,t,n)=>{"use strict";n.d(t,{A:()=>k});var r,a=n(96453),o=n(17437),i=n(95579),s=n(19129),l=n(90868),d=n(31641),c=n(12249),p=n(46920),u=n(96540);function h(){return h=Object.assign?Object.assign.bind():function(e){for(var t=1;t<arguments.length;t++){var n=arguments[t];for(var r in n)({}).hasOwnProperty.call(n,r)&&(e[r]=n[r])}return e},h.apply(null,arguments)}const m=({title:e,titleId:t,...n},a)=>u.createElement("svg",h({xmlns:"http://www.w3.org/2000/svg",width:24,height:24,fill:"none",ref:a,"aria-labelledby":t},n),e?u.createElement("title",{id:t},e):null,r||(r=u.createElement("path",{fill:"currentColor",fillRule:"evenodd",d:"M12 7a1 1 0 0 0-1 1v4a1 1 0 1 0 2 0V8a1 1 0 0 0-1-1m0 8a1 1 0 1 0 0 2 1 1 0 0 0 0-2m9.71-7.44-5.27-5.27a1.05 1.05 0 0 0-.71-.29H8.27a1.05 1.05 0 0 0-.71.29L2.29 7.56a1.05 1.05 0 0 0-.29.71v7.46c.004.265.107.518.29.71l5.27 5.27c.192.183.445.286.71.29h7.46a1.05 1.05 0 0 0 .71-.29l5.27-5.27a1.05 1.05 0 0 0 .29-.71V8.27a1.05 1.05 0 0 0-.29-.71M20 15.31 15.31 20H8.69L4 15.31V8.69L8.69 4h6.62L20 8.69z",clipRule:"evenodd"}))),g=(0,u.forwardRef)(m);var b=n(86523),f=n(40458),y=n(2445);const v=(0,a.I4)(l.pd)`
  margin: ${({theme:e})=>`${e.gridUnit}px 0 ${2*e.gridUnit}px`};
`,x=(0,a.I4)(l.pd.Password)`
  margin: ${({theme:e})=>`${e.gridUnit}px 0 ${2*e.gridUnit}px`};
`,w=(0,a.I4)("div")`
  input::-webkit-outer-spin-button,
  input::-webkit-inner-spin-button {
    -webkit-appearance: none;
    margin: 0;
  }
  margin-bottom: ${({theme:e})=>3*e.gridUnit}px;
  .ant-form-item {
    margin-bottom: 0;
  }
`,$=a.I4.div`
  display: flex;
  align-items: center;
`,_=(0,a.I4)(f.A)`
  margin-bottom: 0;
`,A=o.AH`
  &.anticon > * {
    line-height: 0;
  }
`,k=({label:e,validationMethods:t,errorMessage:n,helpText:r,required:a=!1,hasTooltip:l=!1,tooltipText:u,id:h,className:m,visibilityToggle:f,get_url:k,description:S,...C})=>(0,y.FD)(w,{className:m,children:[(0,y.FD)($,{children:[(0,y.Y)(_,{htmlFor:h,required:a,children:e}),l&&(0,y.Y)(d.A,{tooltip:`${u}`})]}),(0,y.FD)(b.A,{css:e=>((e,t)=>o.AH`
  .ant-form-item-children-icon {
    display: none;
  }
  ${t&&`.ant-form-item-control-input-content {\n      position: relative;\n      &:after {\n        content: ' ';\n        display: inline-block;\n        background: ${e.colors.error.base};\n        mask: url(${g});\n        mask-size: cover;\n        width: ${4*e.gridUnit}px;\n        height: ${4*e.gridUnit}px;\n        position: absolute;\n        right: ${1.25*e.gridUnit}px;\n        top: ${2.75*e.gridUnit}px;\n      }\n    }`}
`)(e,!!n),validateTrigger:Object.keys(t),validateStatus:n?"error":"success",help:n||r,hasFeedback:!!n,children:[f||"password"===C.name?(0,y.Y)(x,{...C,...t,iconRender:e=>e?(0,y.Y)(s.m_,{title:(0,i.t)("Hide password."),children:(0,y.Y)(c.A.EyeInvisibleOutlined,{iconSize:"m",css:A})}):(0,y.Y)(s.m_,{title:(0,i.t)("Show password."),children:(0,y.Y)(c.A.EyeOutlined,{iconSize:"m",css:A})}),role:"textbox"}):(0,y.Y)(v,{...C,...t}),k&&S?(0,y.FD)(p.A,{type:"link",htmlType:"button",buttonStyle:"default",onClick:()=>(window.open(k),!0),children:["Get ",S]}):(0,y.Y)("br",{})]})]})},40563:(e,t,n)=>{"use strict";n.d(t,{lV:()=>s,eI:()=>l.A,lR:()=>d.A,MA:()=>c.A});var r=n(77925),a=n(96453),o=n(2445);const i=(0,a.I4)(r.A)`
  &.ant-form label {
    font-size: ${({theme:e})=>e.typography.sizes.s}px;
  }
  .ant-form-item {
    margin-bottom: ${({theme:e})=>4*e.gridUnit}px;
  }
`;function s(e){return(0,o.Y)(i,{...e})}var l=n(86523),d=n(40458),c=n(97987)},78532:(e,t,n)=>{"use strict";n.d(t,{K:()=>i});var r=n(71519),a=n(32132),o=n(2445);const i=({to:e,component:t,replace:n,innerRef:i,children:s,...l})=>"string"==typeof e&&(0,a.JE)(e)?(0,o.Y)("a",{href:(0,a.Dl)(e),...l,children:s}):(0,o.Y)(r.N_,{to:e,component:t,replace:n,innerRef:i,...l,children:s})},31641:(e,t,n)=>{"use strict";n.d(t,{A:()=>p});var r=n(96453),a=n(19129),o=n(12249),i=n(2445);const s=(0,r.I4)(a.m_)`
  cursor: pointer;
`,l=r.I4.span`
  display: -webkit-box;
  -webkit-line-clamp: 20;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
`,d={fontSize:"12px",lineHeight:"16px"},c="rgba(0,0,0,0.9)";function p({tooltip:e,iconStyle:t={},placement:n="right",trigger:a="hover",overlayStyle:p=d,bgColor:u=c,viewBox:h="0 -1 24 24"}){const m=(0,r.DP)(),g={...t,color:t.color||m.colors.grayscale.base};return(0,i.Y)(s,{title:(0,i.Y)(l,{children:e}),placement:n,trigger:a,overlayStyle:p,color:u,children:(0,i.Y)(o.A.InfoSolidSmall,{style:g,viewBox:h})})}},90868:(e,t,n)=>{"use strict";n.d(t,{YI:()=>i,fs:()=>s,pd:()=>o});var r=n(63786),a=n(80566);const o=r.A,i=a.A,{TextArea:s}=r.A},35768:(e,t,n)=>{"use strict";n.d(t,{DQ:()=>l,xI:()=>d,Ay:()=>c});var r=n(15595),a=n(96453),o=n(12249),i=n(95579),s=n(2445);const l=({datasetType:e})=>{const t="physical"===e?(0,i.t)("Physical"):(0,i.t)("Virtual"),n="physical"===e?(0,s.Y)(o.A.Table,{iconSize:"s"}):(0,s.Y)(o.A.ConsoleSqlOutlined,{iconSize:"s"}),r="physical"===e?"primary":"secondary";return(0,s.Y)(c,{icon:n,type:r,children:t})},d=({isPublished:e,onClick:t})=>{const n=e?(0,i.t)("Published"):(0,i.t)("Draft"),r=e?(0,s.Y)(o.A.CircleCheck,{iconSize:"s"}):(0,s.Y)(o.A.Minus,{iconSize:"s"}),a=e?"primary":"secondary";return(0,s.Y)(c,{type:a,icon:r,onClick:t,children:n})};function c(e){const t=(0,a.DP)(),{colors:n,transitionTiming:o}=t,{type:i="default",monospace:l=!1,style:d,onClick:c,children:p,icon:u,...h}=e,{primary:m,secondary:g,grayscale:b,success:f,warning:y,error:v,info:x}=n;let w;w="primary"===i?m:"secondary"===i?g:"success"===i?f:"warning"===i?y:"danger"===i?v:"info"===i?x:b;const $=w.dark2;let _=w.light1,A=w.light2;["default","primary","secondary"].includes(i)&&(A=w.light4,_=w.light2);const k=c?w.light1:A,S=c?w.base:_;"default"===i&&(A=b.light3);const C={transition:`background-color ${o}s`,whiteSpace:"nowrap",cursor:c?"pointer":"default",overflow:"hidden",textOverflow:"ellipsis",backgroundColor:A,borderRadius:8,borderColor:_,padding:"0.35em 0.8em",lineHeight:1,color:$,display:"inline-flex",verticalAlign:"middle",alignItems:"center",maxWidth:"100%","&:hover":{backgroundColor:k,borderColor:S,opacity:1},...l?{"font-family":t.typography.families.monospace}:{}};return(0,s.Y)(r.vw,{onClick:c,role:c?"button":void 0,style:d,icon:u,...h,css:C,children:p})}},6749:(e,t,n)=>{"use strict";n.d(t,{NG:()=>u,W1:()=>p});var r,a=n(96453),o=n(39472),i=n(36180);!function(e){e.MenuItem="menu-item",e.SubMenu="submenu",e.SubMenuItem="submenu-item"}(r||(r={}));const s=(0,a.I4)(i.A.Item)`
  a {
    text-decoration: none;
  }
  &.antd5-menu-item {
    div {
      display: flex;
      align-items: center;
      justify-content: space-between;
    }
    a {
      transition: background-color ${({theme:e})=>e.transitionTiming}s;
      &:after {
        content: '';
        position: absolute;
        bottom: -2px;
        left: 50%;
        width: 0;
        height: 3px;
        opacity: 0;
        transform: translateX(-50%);
        transition: all ${({theme:e})=>e.transitionTiming}s;
        background-color: ${({theme:e})=>e.colors.primary.base};
      }
      &:focus {
        @media (max-width: 767px) {
          background-color: ${({theme:e})=>e.colors.primary.light5};
        }
      }
    }
  }
`,l=(0,a.I4)(i.A)`
  ${({theme:e})=>`\n    &.antd5-menu-horizontal {\n      background-color: inherit;\n      border-bottom: 1px solid transparent;\n    }\n    &.antd5-menu-vertical,\n    &.ant-dropdown-menu {\n      box-shadow:\n        0 3px 6px -4px ${(0,o.o3)(e.colors.grayscale.dark2,.12)},\n        0 6px 16px 0\n      ${(0,o.o3)(e.colors.grayscale.dark2,.08)},\n        0 9px 28px 8px\n      ${(0,o.o3)(e.colors.grayscale.dark2,.05)};\n    }\n    `}
`,d=(0,a.I4)(i.A)`
  display: flex;
  align-items: center;
  height: 100%;
  gap: 0;
  &.antd5-menu-horizontal > .antd5-menu-item {
    height: 100%;
    display: flex;
    align-items: center;
    margin: 0;
    border-bottom: 2px solid transparent;
    padding: ${({theme:e})=>2*e.gridUnit}px
      ${({theme:e})=>4*e.gridUnit}px;
    &:hover {
      background-color: ${({theme:e})=>e.colors.primary.light5};
      border-bottom: 2px solid transparent;
      & a:after {
        opacity: 1;
        width: 100%;
      }
    }
  }
  &.antd5-menu-horizontal > .antd5-menu-item-selected {
    box-sizing: border-box;
    border-bottom: 2px solid ${({theme:e})=>e.colors.primary.base};
  }
`,c=(0,a.I4)(i.A.SubMenu)`
  .antd5-menu-submenu-open,
  .antd5-menu-submenu-active {
    .antd5-menu-submenu-title {
      &:after {
        opacity: 1;
        width: calc(100% - 1);
      }
    }
  }
  .antd5-menu-submenu-title {
    display: flex;
    flex-direction: row-reverse;
    &:after {
      content: '';
      position: absolute;
      bottom: -3px;
      left: 50%;
      width: 0;
      height: 3px;
      opacity: 0;
      transform: translateX(-50%);
      transition: all ${({theme:e})=>e.transitionTiming}s;
    }
  }

  .ant-dropdown-menu-submenu-arrow:before,
  .ant-dropdown-menu-submenu-arrow:after {
    content: none !important;
  }
`,p=Object.assign(l,{Item:s,SubMenu:c,Divider:i.A.Divider,ItemGroup:i.A.ItemGroup}),u=Object.assign(d,{Item:s,SubMenu:c,Divider:i.A.Divider,ItemGroup:i.A.ItemGroup})},69193:(e,t,n)=>{"use strict";n.d(t,{s:()=>s});var r=n(75160),a=n(89516),o=n(2445);function i(e){return(0,o.Y)(a.A,{...e})}const s=Object.assign(r.Ay,{GroupWrapper:({spaceConfig:e,options:t,...n})=>{const r=t.map((e=>(0,o.Y)(s,{value:e.value,children:e.label},e.value)));return(0,o.Y)(s.Group,{...n,children:e?(0,o.Y)(i,{...e,children:r}):r})},Button:r.Ay.Button})},75488:(e,t,n)=>{"use strict";n.d(t,{d:()=>o});var r=n(96102),a=n(2445);const o=e=>(0,a.Y)(r.A,{...e})},48327:(e,t,n)=>{"use strict";n.d(t,{fn:()=>h,pX:()=>g,Ay:()=>b});var r=n(17437),a=n(96453),o=n(80899),i=n(12249),s=n(2445);const l=({animated:e=!1,fullWidth:t=!0,allowOverflow:n=!0,...a})=>(0,s.Y)(o.A,{animated:e,...a,css:e=>r.AH`
      overflow: ${n?"visible":"hidden"};

      .ant-tabs-content-holder {
        overflow: ${n?"visible":"auto"};
      }
      .ant-tabs-tab {
        flex: 1 1 auto;
        &.ant-tabs-tab-active .ant-tabs-tab-btn {
          color: inherit;
        }
        &:hover {
          .anchor-link-container {
            cursor: pointer;
            .fa.fa-link {
              visibility: visible;
            }
          }
        }
        .short-link-trigger.btn {
          padding: 0 ${e.gridUnit}px;
          & > .fa.fa-link {
            top: 0;
          }
        }
      }
      ${t&&r.AH`
        .ant-tabs-nav-list {
          width: 100%;
        }
      `};

      .ant-tabs-tab-btn {
        display: flex;
        flex: 1 1 auto;
        align-items: center;
        justify-content: center;
        font-size: ${e.typography.sizes.s}px;
        text-align: center;
        user-select: none;
        .required {
          margin-left: ${e.gridUnit/2}px;
          color: ${e.colors.error.base};
        }
      }
      .ant-tabs-ink-bar {
        background: ${e.colors.secondary.base};
      }
    `}),d=(0,a.I4)(o.A.TabPane)``,c=Object.assign(l,{TabPane:d}),p=(0,a.I4)(l)`
  ${({theme:e,fullWidth:t})=>`\n    .ant-tabs-content-holder {\n      background: ${e.colors.grayscale.light5};\n    }\n\n    & > .ant-tabs-nav {\n      margin-bottom: 0;\n    }\n\n    .ant-tabs-tab-remove {\n      padding-top: 0;\n      padding-bottom: 0;\n      height: ${6*e.gridUnit}px;\n    }\n\n    ${t?r.AH`
            .ant-tabs-nav-list {
              width: 100%;
            }
          `:""}\n  `}
`,u=(0,a.I4)(i.A.CancelX)`
  color: ${({theme:e})=>e.colors.grayscale.base};
`,h=Object.assign(p,{TabPane:d});h.defaultProps={type:"editable-card",fullWidth:!1,animated:{inkBar:!0,tabPane:!1}},h.TabPane.defaultProps={closeIcon:(0,s.Y)(u,{role:"button",tabIndex:0})};const m=(0,a.I4)(h)`
  &.ant-tabs-card > .ant-tabs-nav .ant-tabs-tab {
    margin: 0 ${({theme:e})=>4*e.gridUnit}px;
    padding: ${({theme:e})=>`${3*e.gridUnit}px ${e.gridUnit}px`};
    background: transparent;
    border: none;
  }

  &.ant-tabs-card > .ant-tabs-nav .ant-tabs-ink-bar {
    visibility: visible;
  }

  .ant-tabs-tab-btn {
    font-size: ${({theme:e})=>e.typography.sizes.m}px;
  }

  .ant-tabs-tab-remove {
    margin-left: 0;
    padding-right: 0;
  }

  .ant-tabs-nav-add {
    min-width: unset !important;
    background: transparent !important;
    border: none !important;
  }
`,g=Object.assign(m,{TabPane:d}),b=c},28292:(e,t,n)=>{"use strict";n.d(t,{B:()=>a});var r=n(61225);function a(){return(0,r.d4)((e=>{var t;return null==e||null==(t=e.common)?void 0:t.conf}))}},3139:(e,t,n)=>{"use strict";var r,a;n.d(t,{$:()=>a,N:()=>r}),function(e){e.Charts="CHARTS",e.Dashboards="DASHBOARDS",e.Recents="RECENTS",e.SavedQueries="SAVED_QUERIES"}(r||(r={})),function(e){e.GoogleSheets="gsheets",e.DbConnection="dbconnection",e.DatasetCreation="datasetCreation",e.CSVUpload="csvUpload",e.ExcelUpload="excelUpload",e.ColumnarUpload="columnarUpload"}(a||(a={}))},73135:(e,t,n)=>{"use strict";n.d(t,{A:()=>a});var r=n(15151);const a=e=>(async e=>{if((0,r.nr)())try{const t=new ClipboardItem({"text/plain":e()});await navigator.clipboard.write([t])}catch{const t=await e();await navigator.clipboard.writeText(t)}else{const t=await e();await navigator.clipboard.writeText(t)}})(e).catch((()=>e().then((e=>new Promise(((t,n)=>{const r=document.getSelection();if(r){r.removeAllRanges();const t=document.createRange(),a=document.createElement("span");a.textContent=e,a.style.position="fixed",a.style.top="0",a.style.clip="rect(0, 0, 0, 0)",a.style.whiteSpace="pre",document.body.appendChild(a),t.selectNode(a),r.addRange(t);try{document.execCommand("copy")||n()}catch(e){n()}document.body.removeChild(a),r.removeRange?r.removeRange(t):r.removeAllRanges()}t()}))))))},27588:(e,t,n)=>{"use strict";n.d(t,{A:()=>r});const r=(()=>{try{return n(19593)||{}}catch(e){return{}}})()},50500:(e,t,n)=>{"use strict";n.d(t,{Fp:()=>$,RU:()=>m,Y8:()=>C,bN:()=>b,bR:()=>v,d5:()=>k,fn:()=>g,g9:()=>w,oG:()=>y,oi:()=>N,q4:()=>x,xK:()=>_,ym:()=>A});var r=n(58561),a=n.n(r),o=n(96540),i=n(35742),s=n(95579),l=n(51436),d=n(93505),c=n(30703),p=n(73135),u=n(27588);const h=e=>"string"==typeof e?e:Object.entries(e).map((([e,t])=>Array.isArray(t)?`(${e}) ${t.join(", ")}`:`(${e}) ${t}`)).join("\n");function m(e,t,n,r=!0,l=[],d,p=!0,u){const[h,m]=(0,o.useState)({count:0,collection:l,loading:p,lastFetchDataConfig:null,permissions:[],bulkSelectEnabled:!1});function g(e){m((t=>({...t,...e})))}(0,o.useEffect)((()=>{r&&i.A.get({endpoint:`/api/v1/${e}/_info?q=${a().encode({keys:["permissions"]})}`}).then((({json:e={}})=>{g({permissions:e.permissions})}),(0,c.JF)((e=>n((0,s.t)("An error occurred while fetching %s info: %s",t,e)))))}),[]);const b=(0,o.useCallback)((({pageIndex:r,pageSize:o,sortBy:l,filters:p})=>{g({lastFetchDataConfig:{filters:p,pageIndex:r,pageSize:o,sortBy:l},loading:!0});const h=(d||[]).concat(p).map((({id:e,operator:t,value:n})=>({col:e,opr:t,value:n&&"object"==typeof n&&"value"in n?n.value:n}))),m=a().encode_uri({order_column:l[0].id,order_direction:l[0].desc?"desc":"asc",page:r,page_size:o,...h.length?{filters:h}:{},...null!=u&&u.length?{select_columns:u}:{}});return i.A.get({endpoint:`/api/v1/${e}/?q=${m}`}).then((({json:e={}})=>{g({collection:e.result,count:e.count,lastFetched:(new Date).toISOString()})}),(0,c.JF)((e=>n((0,s.t)("An error occurred while fetching %ss: %s",t,e))))).finally((()=>{g({loading:!1})}))}),[d]);return{state:{loading:h.loading,resourceCount:h.count,resourceCollection:h.collection,bulkSelectEnabled:h.bulkSelectEnabled,lastFetched:h.lastFetched},setResourceCollection:e=>g({collection:e}),hasPerm:function(e){return!!h.permissions.length&&Boolean(h.permissions.find((t=>t===e)))},fetchData:b,toggleBulkSelect:function(){g({bulkSelectEnabled:!h.bulkSelectEnabled})},refreshData:e=>h.lastFetchDataConfig?b(h.lastFetchDataConfig):e?b(e):null}}function g(e,t,n,r=""){const[a,l]=(0,o.useState)({loading:!1,resource:null,error:null});function d(e){l((t=>({...t,...e})))}return{state:a,setResource:e=>d({resource:e}),fetchResource:(0,o.useCallback)((a=>{d({loading:!0});const o=`/api/v1/${e}/${a}`,l=""!==r?`${o}/${r}`:o;return i.A.get({endpoint:l}).then((({json:e={}})=>(d({resource:e.result,error:null}),e.result)),(0,c.JF)((e=>{n((0,s.t)("An error occurred while fetching %ss: %s",t,h(e))),d({error:e})}))).finally((()=>{d({loading:!1})}))}),[n,e,t]),createResource:(0,o.useCallback)(((r,a=!1)=>(d({loading:!0}),i.A.post({endpoint:`/api/v1/${e}/`,body:JSON.stringify(r),headers:{"Content-Type":"application/json"}}).then((({json:e={}})=>(d({resource:{id:e.id,...e.result},error:null}),e.id)),(0,c.JF)((e=>{a||n((0,s.t)("An error occurred while creating %ss: %s",t,h(e))),d({error:e})}))).finally((()=>{d({loading:!1})})))),[n,e,t]),updateResource:(0,o.useCallback)(((r,a,o=!1,l=!0)=>(l&&d({loading:!0}),i.A.put({endpoint:`/api/v1/${e}/${r}`,body:JSON.stringify(a),headers:{"Content-Type":"application/json"}}).then((({json:e={}})=>(d({resource:{...e.result,id:e.id},error:null}),e.result)),(0,c.JF)((e=>(o||n((0,s.t)("An error occurred while fetching %ss: %s",t,JSON.stringify(e))),d({error:e}),e)))).finally((()=>{l&&d({loading:!1})})))),[n,e,t]),clearError:()=>d({error:null})}}function b(e,t,n){const[r,a]=(0,o.useState)({loading:!1,passwordsNeeded:[],alreadyExists:[],sshPasswordNeeded:[],sshPrivateKeyNeeded:[],sshPrivateKeyPasswordNeeded:[],failed:!1});function d(e){a((t=>({...t,...e})))}return{state:r,importResource:(0,o.useCallback)(((r,a={},o={},p={},u={},h=!1)=>{d({loading:!0,failed:!1});const m=new FormData;m.append("formData",r);const g=(0,s.t)("Please re-export your file and try importing again");return a&&m.append("passwords",JSON.stringify(a)),h&&m.append("overwrite","true"),o&&m.append("ssh_tunnel_passwords",JSON.stringify(o)),p&&m.append("ssh_tunnel_private_keys",JSON.stringify(p)),u&&m.append("ssh_tunnel_private_key_passwords",JSON.stringify(u)),i.A.post({endpoint:`/api/v1/${e}/import/`,body:m,headers:{Accept:"application/json"}}).then((()=>(d({passwordsNeeded:[],alreadyExists:[],sshPasswordNeeded:[],sshPrivateKeyNeeded:[],sshPrivateKeyPasswordNeeded:[],failed:!1}),!0))).catch((e=>(0,l.h4)(e).then((e=>(d({failed:!0}),e.errors?((0,c.ec)(e.errors)?n((0,s.t)("An error occurred while importing %s: %s",t,[...e.errors.map((e=>e.message)),g].join(".\n"))):d({passwordsNeeded:(0,c.uN)(e.errors),sshPasswordNeeded:(0,c.Um)(e.errors),sshPrivateKeyNeeded:(0,c.dl)(e.errors),sshPrivateKeyPasswordNeeded:(0,c.I7)(e.errors),alreadyExists:(0,c.Xh)(e.errors)}),!1):(n((0,s.t)("An error occurred while importing %s: %s",t,e.message||e.error)),!1)))))).finally((()=>{d({loading:!1})}))}),[])}}const f={chart:(0,d.A)({requestType:"rison",method:"GET",endpoint:"/api/v1/chart/favorite_status/"}),dashboard:(0,d.A)({requestType:"rison",method:"GET",endpoint:"/api/v1/dashboard/favorite_status/"}),tag:(0,d.A)({requestType:"rison",method:"GET",endpoint:"/api/v1/tag/favorite_status/"})};function y(e,t,n){const[r,a]=(0,o.useState)({}),l=e=>a((t=>({...t,...e})));return(0,o.useEffect)((()=>{t.length&&f[e](t).then((({result:e})=>{const t=e.reduce(((e,t)=>(e[t.id]=t.value,e)),{});l(t)}),(0,c.JF)((e=>n((0,s.t)("There was an error fetching the favorite status: %s",e)))))}),[t,e,n]),[(0,o.useCallback)(((t,r)=>{const a=`/api/v1/${e}/${t}/favorites/`;(r?i.A.delete({endpoint:a}):i.A.post({endpoint:a})).then((()=>{l({[t]:!r})}),(0,c.JF)((e=>n((0,s.t)("There was an error saving the favorite status: %s",e)))))}),[e]),r]}const v=(e,t)=>{const[n,r]=(0,o.useState)(null);return{sliceCurrentlyEditing:n,handleChartUpdated:function(n){const r=t.map((e=>e.id===n.id?{...e,...n}:e));e(r)},openChartEditModal:function(e){r({slice_id:e.id,slice_name:e.slice_name,description:e.description,cache_timeout:e.cache_timeout,certified_by:e.certified_by,certification_details:e.certification_details,is_managed_externally:e.is_managed_externally})},closeChartEditModal:function(){r(null)}}},x=(e,t,n)=>{(0,p.A)((()=>Promise.resolve(`${window.location.origin}/sqllab?savedQueryId=${e}`))).then((()=>{n((0,s.t)("Link Copied!"))})).catch((()=>{t((0,s.t)("Sorry, your browser does not support copying."))}))},w=()=>u.A.DB_IMAGES,$=()=>u.A.DB_CONNECTION_ALERTS,_=()=>u.A.DB_CONNECTION_DOC_LINKS,A=(e,t,n)=>{i.A.post({endpoint:"api/v1/database/test_connection/",body:JSON.stringify(e),headers:{"Content-Type":"application/json"}}).then((()=>{n((0,s.t)("Connection looks good!"))}),(0,c.JF)((e=>{t((0,s.t)("ERROR: %s",h(e)))})))};function k(){const[e,t]=(0,o.useState)(null);return[e,(0,o.useCallback)((()=>{i.A.get({endpoint:"/api/v1/database/available/"}).then((({json:e})=>{t(e)}))}),[t])]}const S=e=>e&&Array.isArray(null==e?void 0:e.catalog)?{...e,catalog:Object.assign({},...e.catalog.map((e=>({[e.name]:e.value}))))}:e;function C(){const[e,t]=(0,o.useState)(null);return[e,(0,o.useCallback)(((e,n=!1)=>{var r;return null!=e&&null!=(r=e.parameters)&&r.ssh?(t(null),[]):i.A.post({endpoint:"/api/v1/database/validate_parameters/",body:JSON.stringify(S(e)),headers:{"Content-Type":"application/json"}}).then((()=>{t(null)})).catch((e=>{if("function"==typeof e.json)return e.json().then((({errors:e=[]})=>{const r=e.filter((e=>!["CONNECTION_MISSING_PARAMETERS_ERROR","CONNECTION_ACCESS_DENIED_ERROR"].includes(e.error_type)||n)).reduce(((e,{error_type:t,extra:n,message:r})=>{var a,o;return n.catalog?n.catalog.name?{...e,error_type:t,[n.catalog.idx]:{name:r}}:n.catalog.url?{...e,error_type:t,[n.catalog.idx]:{url:r}}:{...e,error_type:t,[n.catalog.idx]:{name:r,url:r}}:n.invalid?{...e,[n.invalid[0]]:r,error_type:t}:n.missing?{...e,error_type:t,...Object.assign({},...n.missing.map((e=>({[e]:"This is a required field"}))))}:null!=(a=n.issue_codes)&&a.length?{...e,error_type:t,description:r||(null==(o=n.issue_codes[0])?void 0:o.message)}:e}),{});return t(r),r}));console.error(e)}))}),[t]),t]}const N=(e,t,n)=>{var r;return n?null==(r=e.reports[t])?void 0:r[n]:null}},23193:(e,t,n)=>{"use strict";var r,a;n.d(t,{G:()=>r,H:()=>a}),function(e){e.Favorite="Favorite",e.Mine="Mine",e.Other="Other",e.Viewed="Viewed",e.Created="Created",e.Edited="Edited"}(r||(r={})),function(e){e.Id="id",e.ChangedOn="changed_on",e.ChangedBy="changed_by",e.Database="database",e.DatabaseName="database.database_name",e.Schema="schema",e.Sql="sql",e.ExecutedSql="executed_sql",e.SqlTables="sql_tables",e.Status="status",e.TabName="tab_name",e.User="user",e.UserFirstName="user.first_name",e.StartTime="start_time",e.EndTime="end_time",e.Rows="rows",e.TmpTableName="tmp_table_name",e.TrackingUrl="tracking_url"}(a||(a={}))},30703:(e,t,n)=>{"use strict";n.d(t,{$C:()=>S,Af:()=>T,En:()=>y,GP:()=>N,I7:()=>J,J7:()=>A,JF:()=>C,ND:()=>K,Q_:()=>j,Um:()=>q,VY:()=>R,Xh:()=>B,c8:()=>V,dl:()=>G,ec:()=>H,lH:()=>_,md:()=>x,mq:()=>U,oE:()=>$,s4:()=>I,u1:()=>k,uN:()=>M,vE:()=>O,yT:()=>E});var r=n(5287),a=n.n(r),o=n(96453),i=n(35742),s=n(95579),l=n(9450),d=n(51436),c=n(5362),p=n(17437),u=n(58561),h=n.n(u),m=n(27588),g=n(84666),b=n(3139),f=n(23193);(()=>{const e=h(),t=[];for(let e=0;e<16;e+=1)for(let n=0;n<16;n+=1){if(e+n===0)continue;const r=String.fromCharCode(16*e+n);/\w|[-_./~]/.test(r)||t.push(`\\u00${e.toString(16)}${n.toString(16)}`)}e.not_idchar=t.join(""),e.not_idstart="-0123456789";const n=`[^${e.not_idstart}${e.not_idchar}][^${e.not_idchar}]*`;e.id_ok=new RegExp(`^${n}$`),e.next_id=new RegExp(n,"g")})();const y=o.I4.div`
  color: ${({theme:e})=>e.colors.grayscale.base};
`,v=e=>(t,n,r,a)=>async(r="",o,s)=>{var l;const d=`/api/v1/${t}/${e}/${n}`,c=h().encode_uri({filter:r,page:o,page_size:s}),{json:p={}}=await i.A.get({endpoint:`${d}?q=${c}`});let u=!1;const m=a?{label:`${a.firstName} ${a.lastName}`,value:a.userId}:void 0,g=[];return null==p||null==(l=p.result)||l.filter((({text:e})=>e.trim().length>0)).forEach((({text:e,value:t})=>{m&&t===m.value&&e===m.label?u=!0:g.push({label:e,value:t})})),!m||r&&!u||g.unshift(m),{data:g,totalCount:null==p?void 0:p.count}},x=5,w=(e,t)=>{const n={order_column:"changed_on_delta_humanized",order_direction:"desc",page:0,page_size:x,filters:e,select_columns:t};return e||delete n.filters,t||delete n.select_columns,h().encode(n)},$=e=>{const t={edited:[{col:"changed_by",opr:"rel_o_m",value:`${e}`}]},n=[i.A.get({endpoint:`/api/v1/dashboard/?q=${w(t.edited)}`}),i.A.get({endpoint:`/api/v1/chart/?q=${w(t.edited)}`})];return Promise.all(n).then((([e,t])=>{var n,r;return{editedDash:null==(n=t.json)?void 0:n.result.slice(0,3),editedChart:null==(r=e.json)?void 0:r.result.slice(0,3)}})).catch((e=>e))},_=(e,t,n=[{col:"owners",opr:"rel_m_m",value:`${e}`}],r)=>i.A.get({endpoint:`/api/v1/${t}/?q=${w(n,r)}`}).then((e=>{var t;return null==(t=e.json)?void 0:t.result})),A=(e,t,n,r)=>i.A.get({endpoint:t}).then((e=>{const t={},a=(0,l.E)(6);return e.json.result.reverse().forEach((e=>{a.set(e.item_url,e)})),((e,t)=>{const n=[i.A.get({endpoint:`/api/v1/chart/?q=${w(t,void 0)}`}),i.A.get({endpoint:`/api/v1/dashboard/?q=${w(t,void 0)}`})];return Promise.all(n).then((([e,t])=>({other:[...e.json.result,...t.json.result]}))).catch((t=>(e((0,s.t)("There was an error fetching the filtered charts and dashboards:"),t),{other:[]})))})(n,r).then((({other:e})=>(t.other=e,t.viewed=a.values().reverse(),t)))})),k=v("related"),S=v("distinct");function C(e){return async t=>{const n=await(0,d.h4)(t),r=null==n?void 0:n.errors,a=await m.A;null!=r&&r.length&&null!=a&&a.ERRORS&&r[0].error_type in a.ERRORS&&(n.message=a.ERRORS[r[0].error_type]),c.A.error(t),e(n.message||n.error)}}function N({id:e,slice_name:t},n,r,a,o,l){const d={pageIndex:0,pageSize:x,sortBy:[{id:"changed_on_delta_humanized",desc:!0}],filters:[{id:"created_by",operator:"rel_o_m",value:`${l}`}]};i.A.delete({endpoint:`/api/v1/chart/${e}`}).then((()=>{"Mine"===o?a(d):a(),n((0,s.t)("Deleted: %s",t))}),(()=>{r((0,s.t)("There was an issue deleting: %s",t))}))}function E({id:e,dashboard_title:t},n,r,a,o,l){return i.A.delete({endpoint:`/api/v1/dashboard/${e}`}).then((()=>{"Mine"===o?n({pageIndex:0,pageSize:x,sortBy:[{id:"changed_on_delta_humanized",desc:!0}],filters:[{id:"owners",operator:"rel_m_m",value:`${l}`}]}):n(),r((0,s.t)("Deleted: %s",t))}),C((e=>a((0,s.t)("There was an issue deleting %s: %s",t,e)))))}function I(e,t){let n=e.split("\n");return n.length>=t&&(n=n.slice(0,t),n.push("...")),n.join("\n")}const T=5,U=[576,768,992,1200].map((e=>`@media (max-width: ${e}px)`)),j=o.I4.div`
  ${({showThumbnails:e,theme:t})=>`\n    overflow: hidden;\n    display: grid;\n    grid-gap: ${12*t.gridUnit}px ${4*t.gridUnit}px;\n    grid-template-columns: repeat(auto-fit, 300px);\n    max-height: ${e?"314":"148"}px;\n    margin-top: ${-6*t.gridUnit}px;\n    padding: ${e?`${8*t.gridUnit+3}px ${9*t.gridUnit}px`:`${8*t.gridUnit+1}px ${9*t.gridUnit}px`};\n  `}
`,R=o.I4.div`
  cursor: pointer;
  a {
    text-decoration: none;
  }
  .antd5-card-cover > div {
    /* Height is calculated based on 300px width, to keep the same aspect ratio as the 800*450 thumbnails */
    height: 168px;
  }
`,O=e=>p.AH`
  margin: auto ${2*e.gridUnit}px auto 0;
  color: ${e.colors.grayscale.base};
`,D=e=>{var t;return"object"==typeof e&&Array.isArray(e._schema)&&!(null==(t=e._schema)||!t.find((e=>"Must provide a password for the database"===e)))},Y=e=>{var t;return"object"==typeof e&&Array.isArray(e._schema)&&!(null==(t=e._schema)||!t.find((e=>"Must provide a password for the ssh tunnel"===e)))},P=e=>{var t;return"object"==typeof e&&Array.isArray(e._schema)&&!(null==(t=e._schema)||!t.find((e=>"Must provide a private key for the ssh tunnel"===e)))},z=e=>{var t;return"object"==typeof e&&Array.isArray(e._schema)&&!(null==(t=e._schema)||!t.find((e=>"Must provide a private key password for the ssh tunnel"===e)))},F=e=>"string"==typeof e&&e.includes("already exists and `overwrite=true` was not passed"),M=e=>e.map((e=>Object.entries(e.extra).filter((([,e])=>D(e))).map((([e])=>e)))).flat(),q=e=>e.map((e=>Object.entries(e.extra).filter((([,e])=>Y(e))).map((([e])=>e)))).flat(),G=e=>e.map((e=>Object.entries(e.extra).filter((([,e])=>P(e))).map((([e])=>e)))).flat(),J=e=>e.map((e=>Object.entries(e.extra).filter((([,e])=>z(e))).map((([e])=>e)))).flat(),B=e=>e.map((e=>Object.entries(e.extra).filter((([,e])=>F(e))).map((([e])=>e)))).flat(),H=e=>e.some((e=>{const t=Object.entries(e.extra).filter((([e])=>"issue_codes"!==e));return 0===t.length||!t.every((([,e])=>D(e)||F(e)||Y(e)||P(e)||z(e)))})),L=(e,t)=>void 0!==e&&a()(e,t).length>0,V=(e,t,n,r,a)=>{const o=(0,g.L)("can_upload","Database",e)&&L(t,a),i=L(n,a)&&(0,g.L)("can_upload","Database",e),s=L(r,a)&&(0,g.L)("can_upload","Database",e);return{canUploadCSV:o,canUploadColumnar:i,canUploadExcel:s,canUploadData:o||i||s}};function K(e,t,n,r){return e===f.G.Created||t===b.N.SavedQueries&&e===f.G.Mine?[{id:"created_by",operator:"rel_o_m",value:`${null==n?void 0:n.userId}`}]:t===b.N.SavedQueries&&e===f.G.Favorite?[{id:"id",operator:"saved_query_is_fav",value:!0}]:e===f.G.Mine&&n?[{id:"owners",operator:"rel_m_m",value:`${n.userId}`}]:e===f.G.Favorite&&[b.N.Dashboards,b.N.Charts].includes(t)?[{id:"id",operator:t===b.N.Dashboards?"dashboard_is_favorite":"chart_is_favorite",value:!0}]:e===f.G.Other?(r||[]).map((e=>({id:e.col,operator:e.opr,value:e.value}))):[]}}}]);