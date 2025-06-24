"use strict";(globalThis.webpackChunksuperset=globalThis.webpackChunksuperset||[]).push([[4923],{54923:(e,t,a)=>{a.r(t),a.d(t,{default:()=>h});var l=a(62952),n=a(87903),s=a(95579),r=a(96540),o=a(15595),i=a(67874),u=a(2445);function h(e){const{data:t,formData:a,height:h,width:d,setDataMask:c,setHoveredFilter:v,unsetHoveredFilter:g,setFocusedFilter:f,unsetFocusedFilter:p,setFilterActive:m,filterState:F,inputRef:w}=e,{defaultValue:b}=a,[S,M]=(0,r.useState)(null!=b?b:[]),k=e=>{const t=(0,l.A)(e);M(t);const a={};t.length&&(a.granularity_sqla=t[0]),c({extraFormData:a,filterState:{value:t.length?t:null}})};(0,r.useEffect)((()=>{k(null!=b?b:null)}),[JSON.stringify(b)]),(0,r.useEffect)((()=>{var e;k(null!=(e=F.value)?e:null)}),[JSON.stringify(F.value)]);const C=(t||[]).filter((e=>e.dtype===n.s.Temporal)),Y=0===C.length?(0,s.t)("No time columns"):(0,s.tn)("%s option","%s options",C.length,C.length),x={};F.validateMessage&&(x.extra=(0,u.Y)(i.Mo,{status:F.validateStatus,children:F.validateMessage}));const y=C.map((e=>{const{column_name:t,verbose_name:a}=e;return{label:null!=a?a:t,value:t}}));return(0,u.Y)(i.j3,{height:h,width:d,children:(0,u.Y)(i.JF,{validateStatus:F.validateStatus,...x,children:(0,u.Y)(o.l6,{name:a.nativeFilterId,allowClear:!0,value:S,placeholder:Y,onChange:k,onBlur:p,onFocus:f,onMouseEnter:v,onMouseLeave:g,ref:w,options:y,onDropdownVisibleChange:m})})})}},67874:(e,t,a)=>{a.d(t,{JF:()=>o,Mo:()=>i,YH:()=>s,j3:()=>r});var l=a(96453),n=a(86523);const s=0,r=l.I4.div`
  min-height: ${({height:e})=>e}px;
  width: ${({width:e})=>e===s?"100%":`${e}px`};
`,o=(0,l.I4)(n.A)`
  &.ant-row.ant-form-item {
    margin: 0;
  }
`,i=l.I4.div`
  color: ${({theme:e,status:t="error"})=>{var a;return null==(a=e.colors[t])?void 0:a.base}};
`}}]);