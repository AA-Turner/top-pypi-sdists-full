"use strict";(globalThis.webpackChunksuperset=globalThis.webpackChunksuperset||[]).push([[1419],{1419:(e,t,a)=>{a.r(t),a.d(t,{default:()=>u});var l=a(62952),n=a(95579),i=a(96540),s=a(15595),r=a(67874),o=a(2445);function u(e){const{data:t,formData:a,height:u,width:d,setDataMask:h,setHoveredFilter:c,unsetHoveredFilter:v,setFocusedFilter:g,unsetFocusedFilter:f,setFilterActive:p,filterState:m,inputRef:F}=e,{defaultValue:w}=a,[S,b]=(0,i.useState)(null!=w?w:[]),M=(0,i.useMemo)((()=>t.reduce(((e,{duration:t,name:a})=>({...e,[t]:a})),{})),[JSON.stringify(t)]),k=e=>{const t=(0,l.A)(e),[a]=t,n=a?M[a]:void 0,i={};a&&(i.time_grain_sqla=a),b(t),h({extraFormData:i,filterState:{label:n,value:t.length?t:null}})};(0,i.useEffect)((()=>{k(null!=w?w:[])}),[JSON.stringify(w)]),(0,i.useEffect)((()=>{var e;k(null!=(e=m.value)?e:[])}),[JSON.stringify(m.value)]);const C=0===(t||[]).length?(0,n.t)("No data"):(0,n.tn)("%s option","%s options",t.length,t.length),J={};m.validateMessage&&(J.extra=(0,o.Y)(r.Mo,{status:m.validateStatus,children:m.validateMessage}));const Y=(t||[]).map((e=>{const{name:t,duration:a}=e;return{label:t,value:a}}));return(0,o.Y)(r.j3,{height:u,width:d,children:(0,o.Y)(r.JF,{validateStatus:m.validateStatus,...J,children:(0,o.Y)(s.l6,{name:a.nativeFilterId,allowClear:!0,value:S,placeholder:C,onChange:k,onBlur:f,onFocus:g,onMouseEnter:c,onMouseLeave:v,ref:F,options:Y,onDropdownVisibleChange:p})})})}},67874:(e,t,a)=>{a.d(t,{JF:()=>r,Mo:()=>o,YH:()=>i,j3:()=>s});var l=a(96453),n=a(86523);const i=0,s=l.I4.div`
  min-height: ${({height:e})=>e}px;
  width: ${({width:e})=>e===i?"100%":`${e}px`};
`,r=(0,l.I4)(n.A)`
  &.ant-row.ant-form-item {
    margin: 0;
  }
`,o=l.I4.div`
  color: ${({theme:e,status:t="error"})=>{var a;return null==(a=e.colors[t])?void 0:a.base}};
`}}]);