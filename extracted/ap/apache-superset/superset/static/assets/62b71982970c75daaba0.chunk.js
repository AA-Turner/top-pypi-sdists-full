"use strict";(globalThis.webpackChunksuperset=globalThis.webpackChunksuperset||[]).push([[8568],{45418:(e,t,i)=>{i.d(t,{A:()=>g});var n=i(96540),r=i(46942),o=i.n(r),l=i(22553),a=i(6311),d=i(1051),s=i(96424),c=i(14277);const h=e=>{const{componentCls:t,sizePaddingEdgeHorizontal:i,colorSplit:n,lineWidth:r,textPaddingInline:o,orientationMargin:l,verticalMarginInline:s}=e;return{[t]:Object.assign(Object.assign({},(0,d.dF)(e)),{borderBlockStart:`${(0,a.unit)(r)} solid ${n}`,"&-vertical":{position:"relative",top:"-0.06em",display:"inline-block",height:"0.9em",marginInline:s,marginBlock:0,verticalAlign:"middle",borderTop:0,borderInlineStart:`${(0,a.unit)(r)} solid ${n}`},"&-horizontal":{display:"flex",clear:"both",width:"100%",minWidth:"100%",margin:`${(0,a.unit)(e.dividerHorizontalGutterMargin)} 0`},[`&-horizontal${t}-with-text`]:{display:"flex",alignItems:"center",margin:`${(0,a.unit)(e.dividerHorizontalWithTextGutterMargin)} 0`,color:e.colorTextHeading,fontWeight:500,fontSize:e.fontSizeLG,whiteSpace:"nowrap",textAlign:"center",borderBlockStart:`0 ${n}`,"&::before, &::after":{position:"relative",width:"50%",borderBlockStart:`${(0,a.unit)(r)} solid transparent`,borderBlockStartColor:"inherit",borderBlockEnd:0,transform:"translateY(50%)",content:"''"}},[`&-horizontal${t}-with-text-left`]:{"&::before":{width:`calc(${l} * 100%)`},"&::after":{width:`calc(100% - ${l} * 100%)`}},[`&-horizontal${t}-with-text-right`]:{"&::before":{width:`calc(100% - ${l} * 100%)`},"&::after":{width:`calc(${l} * 100%)`}},[`${t}-inner-text`]:{display:"inline-block",paddingBlock:0,paddingInline:o},"&-dashed":{background:"none",borderColor:n,borderStyle:"dashed",borderWidth:`${(0,a.unit)(r)} 0 0`},[`&-horizontal${t}-with-text${t}-dashed`]:{"&::before, &::after":{borderStyle:"dashed none none"}},[`&-vertical${t}-dashed`]:{borderInlineStartWidth:r,borderInlineEnd:0,borderBlockStart:0,borderBlockEnd:0},"&-dotted":{background:"none",borderColor:n,borderStyle:"dotted",borderWidth:`${(0,a.unit)(r)} 0 0`},[`&-horizontal${t}-with-text${t}-dotted`]:{"&::before, &::after":{borderStyle:"dotted none none"}},[`&-vertical${t}-dotted`]:{borderInlineStartWidth:r,borderInlineEnd:0,borderBlockStart:0,borderBlockEnd:0},[`&-plain${t}-with-text`]:{color:e.colorText,fontWeight:"normal",fontSize:e.fontSize},[`&-horizontal${t}-with-text-left${t}-no-default-orientation-margin-left`]:{"&::before":{width:0},"&::after":{width:"100%"},[`${t}-inner-text`]:{paddingInlineStart:i}},[`&-horizontal${t}-with-text-right${t}-no-default-orientation-margin-right`]:{"&::before":{width:"100%"},"&::after":{width:0},[`${t}-inner-text`]:{paddingInlineEnd:i}}})}},p=(0,s.OF)("Divider",(e=>{const t=(0,c.mergeToken)(e,{dividerHorizontalWithTextGutterMargin:e.margin,dividerHorizontalGutterMargin:e.marginLG,sizePaddingEdgeHorizontal:0});return[h(t)]}),(e=>({textPaddingInline:"1em",orientationMargin:.05,verticalMarginInline:e.marginXS})),{unitless:{orientationMargin:!0}});const g=e=>{const{getPrefixCls:t,direction:i,divider:r}=n.useContext(l.QO),{prefixCls:a,type:d="horizontal",orientation:s="center",orientationMargin:c,className:h,rootClassName:g,children:m,dashed:u,variant:b="solid",plain:f,style:v}=e,$=function(e,t){var i={};for(var n in e)Object.prototype.hasOwnProperty.call(e,n)&&t.indexOf(n)<0&&(i[n]=e[n]);if(null!=e&&"function"==typeof Object.getOwnPropertySymbols){var r=0;for(n=Object.getOwnPropertySymbols(e);r<n.length;r++)t.indexOf(n[r])<0&&Object.prototype.propertyIsEnumerable.call(e,n[r])&&(i[n[r]]=e[n[r]])}return i}(e,["prefixCls","type","orientation","orientationMargin","className","rootClassName","children","dashed","variant","plain","style"]),x=t("divider",a),[w,y,S]=p(x),k=!!m,A="left"===s&&null!=c,I="right"===s&&null!=c,Y=o()(x,null==r?void 0:r.className,y,S,`${x}-${d}`,{[`${x}-with-text`]:k,[`${x}-with-text-${s}`]:k,[`${x}-dashed`]:!!u,[`${x}-${b}`]:"solid"!==b,[`${x}-plain`]:!!f,[`${x}-rtl`]:"rtl"===i,[`${x}-no-default-orientation-margin-left`]:A,[`${x}-no-default-orientation-margin-right`]:I},h,g),z=n.useMemo((()=>"number"==typeof c?c:/^\d+$/.test(c)?Number(c):c),[c]),C=Object.assign(Object.assign({},A&&{marginLeft:z}),I&&{marginRight:z});return w(n.createElement("div",Object.assign({className:Y,style:Object.assign(Object.assign({},null==r?void 0:r.style),v)},$,{role:"separator"}),m&&"vertical"!==d&&n.createElement("span",{className:`${x}-inner-text`,style:C},m)))}},40458:(e,t,i)=>{i.d(t,{A:()=>a});var n=i(96453),r=i(2445);const o=n.I4.label`
  font-size: ${({theme:e})=>e.typography.sizes.s}px;
  color: ${({theme:e})=>e.colors.grayscale.base};
  margin-bottom: ${({theme:e})=>e.gridUnit}px;
`,l=n.I4.label`
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
`;function a({children:e,htmlFor:t,required:i=!1,className:n}){const a=i?l:o;return(0,r.Y)(a,{htmlFor:t,className:n,children:e})}},97987:(e,t,i)=>{i.d(t,{A:()=>A});var n,r=i(96453),o=i(17437),l=i(95579),a=i(19129),d=i(90868),s=i(31641),c=i(12249),h=i(46920),p=i(96540);function g(){return g=Object.assign?Object.assign.bind():function(e){for(var t=1;t<arguments.length;t++){var i=arguments[t];for(var n in i)({}).hasOwnProperty.call(i,n)&&(e[n]=i[n])}return e},g.apply(null,arguments)}const m=({title:e,titleId:t,...i},r)=>p.createElement("svg",g({xmlns:"http://www.w3.org/2000/svg",width:24,height:24,fill:"none",ref:r,"aria-labelledby":t},i),e?p.createElement("title",{id:t},e):null,n||(n=p.createElement("path",{fill:"currentColor",fillRule:"evenodd",d:"M12 7a1 1 0 0 0-1 1v4a1 1 0 1 0 2 0V8a1 1 0 0 0-1-1m0 8a1 1 0 1 0 0 2 1 1 0 0 0 0-2m9.71-7.44-5.27-5.27a1.05 1.05 0 0 0-.71-.29H8.27a1.05 1.05 0 0 0-.71.29L2.29 7.56a1.05 1.05 0 0 0-.29.71v7.46c.004.265.107.518.29.71l5.27 5.27c.192.183.445.286.71.29h7.46a1.05 1.05 0 0 0 .71-.29l5.27-5.27a1.05 1.05 0 0 0 .29-.71V8.27a1.05 1.05 0 0 0-.29-.71M20 15.31 15.31 20H8.69L4 15.31V8.69L8.69 4h6.62L20 8.69z",clipRule:"evenodd"}))),u=(0,p.forwardRef)(m);var b=i(86523),f=i(40458),v=i(2445);const $=(0,r.I4)(d.pd)`
  margin: ${({theme:e})=>`${e.gridUnit}px 0 ${2*e.gridUnit}px`};
`,x=(0,r.I4)(d.pd.Password)`
  margin: ${({theme:e})=>`${e.gridUnit}px 0 ${2*e.gridUnit}px`};
`,w=(0,r.I4)("div")`
  input::-webkit-outer-spin-button,
  input::-webkit-inner-spin-button {
    -webkit-appearance: none;
    margin: 0;
  }
  margin-bottom: ${({theme:e})=>3*e.gridUnit}px;
  .ant-form-item {
    margin-bottom: 0;
  }
`,y=r.I4.div`
  display: flex;
  align-items: center;
`,S=(0,r.I4)(f.A)`
  margin-bottom: 0;
`,k=o.AH`
  &.anticon > * {
    line-height: 0;
  }
`,A=({label:e,validationMethods:t,errorMessage:i,helpText:n,required:r=!1,hasTooltip:d=!1,tooltipText:p,id:g,className:m,visibilityToggle:f,get_url:A,description:I,...Y})=>(0,v.FD)(w,{className:m,children:[(0,v.FD)(y,{children:[(0,v.Y)(S,{htmlFor:g,required:r,children:e}),d&&(0,v.Y)(s.A,{tooltip:`${p}`})]}),(0,v.FD)(b.A,{css:e=>((e,t)=>o.AH`
  .ant-form-item-children-icon {
    display: none;
  }
  ${t&&`.ant-form-item-control-input-content {\n      position: relative;\n      &:after {\n        content: ' ';\n        display: inline-block;\n        background: ${e.colors.error.base};\n        mask: url(${u});\n        mask-size: cover;\n        width: ${4*e.gridUnit}px;\n        height: ${4*e.gridUnit}px;\n        position: absolute;\n        right: ${1.25*e.gridUnit}px;\n        top: ${2.75*e.gridUnit}px;\n      }\n    }`}
`)(e,!!i),validateTrigger:Object.keys(t),validateStatus:i?"error":"success",help:i||n,hasFeedback:!!i,children:[f||"password"===Y.name?(0,v.Y)(x,{...Y,...t,iconRender:e=>e?(0,v.Y)(a.m_,{title:(0,l.t)("Hide password."),children:(0,v.Y)(c.A.EyeInvisibleOutlined,{iconSize:"m",css:k})}):(0,v.Y)(a.m_,{title:(0,l.t)("Show password."),children:(0,v.Y)(c.A.EyeOutlined,{iconSize:"m",css:k})}),role:"textbox"}):(0,v.Y)($,{...Y,...t}),A&&I?(0,v.FD)(h.A,{type:"link",htmlType:"button",buttonStyle:"default",onClick:()=>(window.open(A),!0),children:["Get ",I]}):(0,v.Y)("br",{})]})]})},40563:(e,t,i)=>{i.d(t,{lV:()=>a,eI:()=>d.A,lR:()=>s.A,MA:()=>c.A});var n=i(77925),r=i(96453),o=i(2445);const l=(0,r.I4)(n.A)`
  &.ant-form label {
    font-size: ${({theme:e})=>e.typography.sizes.s}px;
  }
  .ant-form-item {
    margin-bottom: ${({theme:e})=>4*e.gridUnit}px;
  }
`;function a(e){return(0,o.Y)(l,{...e})}var d=i(86523),s=i(40458),c=i(97987)},31641:(e,t,i)=>{i.d(t,{A:()=>h});var n=i(96453),r=i(19129),o=i(12249),l=i(2445);const a=(0,n.I4)(r.m_)`
  cursor: pointer;
`,d=n.I4.span`
  display: -webkit-box;
  -webkit-line-clamp: 20;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
`,s={fontSize:"12px",lineHeight:"16px"},c="rgba(0,0,0,0.9)";function h({tooltip:e,iconStyle:t={},placement:i="right",trigger:r="hover",overlayStyle:h=s,bgColor:p=c,viewBox:g="0 -1 24 24"}){const m=(0,n.DP)(),u={...t,color:t.color||m.colors.grayscale.base};return(0,l.Y)(a,{title:(0,l.Y)(d,{children:e}),placement:i,trigger:r,overlayStyle:h,color:p,children:(0,l.Y)(o.A.InfoSolidSmall,{style:u,viewBox:g})})}},90868:(e,t,i)=>{i.d(t,{YI:()=>l,fs:()=>a,pd:()=>o});var n=i(63786),r=i(80566);const o=n.A,l=r.A,{TextArea:a}=n.A},69193:(e,t,i)=>{i.d(t,{s:()=>a});var n=i(75160),r=i(89516),o=i(2445);function l(e){return(0,o.Y)(r.A,{...e})}const a=Object.assign(n.Ay,{GroupWrapper:({spaceConfig:e,options:t,...i})=>{const n=t.map((e=>(0,o.Y)(a,{value:e.value,children:e.label},e.value)));return(0,o.Y)(a.Group,{...i,children:e?(0,o.Y)(l,{...e,children:n}):n})},Button:n.Ay.Button})},50317:(e,t,i)=>{i.d(t,{A:()=>g});var n=i(96540),r=i(17437),o=i(96453),l=i(95579),a=i(66537),d=i(19129),s=i(40563),c=i(12249),h=i(2445);const p=r.AH`
  &.anticon {
    font-size: unset;
    .anticon {
      line-height: unset;
      vertical-align: unset;
    }
  }
`,g=({name:e,label:t,description:i,validationErrors:g=[],renderTrigger:m=!1,rightNode:u,leftNode:b,onClick:f,hovered:v=!1,tooltipOnClick:$=()=>{},warning:x,danger:w})=>{const{gridUnit:y,colors:S}=(0,o.DP)(),k=(0,n.useRef)(!1),A=(0,n.useMemo)((()=>(g.length||(k.current=!0),k.current?g.length?S.error.base:"unset":S.warning.base)),[S.error.base,S.warning.base,g.length]);return t?(0,h.FD)("div",{className:"ControlHeader",children:[(0,h.Y)("div",{className:"pull-left",children:(0,h.FD)(s.lR,{css:e=>r.AH`
            margin-bottom: ${.5*e.gridUnit}px;
            position: relative;
          `,children:[b&&(0,h.Y)("span",{children:b}),(0,h.Y)("span",{role:"button",tabIndex:0,onClick:f,style:{cursor:f?"pointer":""},children:t})," ",x&&(0,h.FD)("span",{children:[(0,h.Y)(d.m_,{id:"error-tooltip",placement:"top",title:x,children:(0,h.Y)(c.A.AlertSolid,{iconColor:S.warning.base,iconSize:"s"})})," "]}),w&&(0,h.FD)("span",{children:[(0,h.Y)(d.m_,{id:"error-tooltip",placement:"top",title:w,children:(0,h.Y)(c.A.ErrorSolid,{iconColor:S.error.base,iconSize:"s"})})," "]}),(null==g?void 0:g.length)>0&&(0,h.FD)("span",{children:[(0,h.Y)(d.m_,{id:"error-tooltip",placement:"top",title:null==g?void 0:g.join(" "),children:(0,h.Y)(c.A.ExclamationCircleOutlined,{css:r.AH`
                    ${p};
                    color: ${A};
                  `})})," "]}),v?(0,h.FD)("span",{css:()=>r.AH`
          position: absolute;
          top: 50%;
          right: 0;
          padding-left: ${y}px;
          transform: translate(100%, -50%);
          white-space: nowrap;
        `,children:[i&&(0,h.FD)("span",{children:[(0,h.Y)(d.m_,{id:"description-tooltip",title:i,placement:"top",children:(0,h.Y)(c.A.InfoCircleOutlined,{css:p,onClick:$})})," "]}),m&&(0,h.FD)("span",{children:[(0,h.Y)(a.W,{label:(0,l.t)("bolt"),tooltip:(0,l.t)("Changing this control takes effect instantly"),placement:"top",icon:"bolt"})," "]})]}):null]})}),u&&(0,h.Y)("div",{className:"pull-right",children:u}),(0,h.Y)("div",{className:"clearfix"})]}):null}},87615:(e,t,i)=>{i.r(t),i.d(t,{default:()=>h});var n=i(96453),r=i(96627),o=i(96540),l=i(39074),a=i(67874),d=i(2445);const s=(0,n.I4)(a.j3)`
  display: flex;
  align-items: center;
  overflow-x: auto;

  & .ant-tag {
    margin-right: 0;
  }
`,c=n.I4.div`
  display: flex;
  height: 100%;
  max-width: 100%;
  width: 100%;
  & > div,
  & > div:hover {
    ${({validateStatus:e,theme:t})=>{var i;return e&&`border-color: ${null==(i=t.colors[e])?void 0:i.base}`}}
  }
`;function h(e){var t;const{setDataMask:i,setHoveredFilter:n,unsetHoveredFilter:a,setFocusedFilter:h,unsetFocusedFilter:p,setFilterActive:g,width:m,height:u,filterState:b,inputRef:f,isOverflowingFilterBar:v=!1}=e,$=(0,o.useCallback)((e=>{const t=e&&e!==r.WC;i({extraFormData:t?{time_range:e}:{},filterState:{value:t?e:void 0}})}),[i]);return(0,o.useEffect)((()=>{$(b.value)}),[b.value]),null!=(t=e.formData)&&t.inView?(0,d.Y)(s,{width:m,height:u,children:(0,d.Y)(c,{ref:f,validateStatus:b.validateStatus,onFocus:h,onBlur:p,onMouseEnter:n,onMouseLeave:a,children:(0,d.Y)(l.Ay,{value:b.value||r.WC,name:e.formData.nativeFilterId||"time_range",onChange:$,onOpenPopover:()=>g(!0),onClosePopover:()=>{g(!1),a(),p()},isOverflowingFilterBar:v})})}):null}},67874:(e,t,i)=>{i.d(t,{JF:()=>a,Mo:()=>d,YH:()=>o,j3:()=>l});var n=i(96453),r=i(86523);const o=0,l=n.I4.div`
  min-height: ${({height:e})=>e}px;
  width: ${({width:e})=>e===o?"100%":`${e}px`};
`,a=(0,n.I4)(r.A)`
  &.ant-row.ant-form-item {
    margin: 0;
  }
`,d=n.I4.div`
  color: ${({theme:e,status:t="error"})=>{var i;return null==(i=e.colors[t])?void 0:i.base}};
`}}]);