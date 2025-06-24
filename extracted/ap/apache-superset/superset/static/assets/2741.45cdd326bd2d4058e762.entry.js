"use strict";(globalThis.webpackChunksuperset=globalThis.webpackChunksuperset||[]).push([[2741],{31383:(e,a,t)=>{t.d(a,{A:()=>c});var n=t(95579),l=t(50500),r=t(25946),i=t(17437),o=t(2445);const s=(0,l.xK)(),d=s?s.support:"https://superset.apache.org/docs/databases/installing-database-drivers",c=({errorMessage:e,showDbInstallInstructions:a})=>(0,o.Y)(r.A,{closable:!1,css:e=>(e=>i.AH`
  margin: ${4*e.gridUnit}px 0;

  .antd5-alert-message {
    margin: 0;
  }
`)(e),type:"error",showIcon:!0,message:e,description:a?(0,o.FD)(o.FK,{children:[(0,o.Y)("br",{}),(0,n.t)("Database driver for importing maybe not installed. Visit the Superset documentation page for installation instructions: "),(0,o.Y)("a",{href:d,target:"_blank",rel:"noopener noreferrer",className:"additional-fields-alert-description",children:(0,n.t)("here")}),"."]}):""})},85994:(e,a,t)=>{t.d(a,{A:()=>u});var n=t(96540),l=t(96453),r=t(12249),i=t(2445);const o=l.I4.label`
  cursor: pointer;
  display: inline-block;
  margin-bottom: 0;
`,s=(0,l.I4)(r.A.CheckboxHalf)`
  color: ${({theme:e})=>e.colors.primary.base};
  cursor: pointer;
`,d=(0,l.I4)(r.A.CheckboxOff)`
  color: ${({theme:e})=>e.colors.grayscale.base};
  cursor: pointer;
`,c=(0,l.I4)(r.A.CheckboxOn)`
  color: ${({theme:e})=>e.colors.primary.base};
  cursor: pointer;
`,h=l.I4.input`
  &[type='checkbox'] {
    cursor: pointer;
    opacity: 0;
    position: absolute;
    left: 3px;
    margin: 0;
    top: 4px;
  }
`,p=l.I4.div`
  cursor: pointer;
  display: inline-block;
  position: relative;
`,u=(0,n.forwardRef)((({indeterminate:e,id:a,checked:t,onChange:l,title:r="",labelText:u="",...m},g)=>{const b=(0,n.useRef)(),v=g||b;return(0,n.useEffect)((()=>{v.current.indeterminate=e}),[v,e]),(0,i.FD)(i.FK,{children:[(0,i.FD)(p,{children:[e&&(0,i.Y)(s,{}),!e&&t&&(0,i.Y)(c,{}),!e&&!t&&(0,i.Y)(d,{}),(0,i.Y)(h,{name:a,id:a,type:"checkbox",ref:v,checked:t,onChange:l,...m})]}),(0,i.Y)(o,{title:r,htmlFor:a,children:u})]})}))},46740:(e,a,t)=>{t.d(a,{A:()=>s});var n=t(96540),l=t(96453),r=t(16707),i=t(2445);const o=l.I4.div`
  max-width: 100%;
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
`,s=({tags:e,editable:a=!1,onDelete:t,maxTags:l})=>{const[s,d]=(0,n.useState)(l),c=e=>{null==t||t(e)},h=(0,n.useMemo)((()=>s?e.length>s:null),[e.length,s]),p=(0,n.useMemo)((()=>"number"==typeof s?e.length-s+1:null),[h,e.length,s]);return(0,i.Y)(o,{className:"tag-list",children:h&&"number"==typeof s?(0,i.FD)(i.FK,{children:[e.slice(0,s-1).map(((e,t)=>(0,i.Y)(r.A,{id:e.id,name:e.name,index:t,onDelete:c,editable:a},e.id))),e.length>s?(0,i.Y)(r.A,{name:`+${p}...`,onClick:()=>d(void 0),toolTipTitle:e.map((e=>e.name)).join(", ")}):null]}):(0,i.FD)(i.FK,{children:[e.map(((e,t)=>(0,i.Y)(r.A,{id:e.id,name:e.name,index:t,onDelete:c,editable:a},e.id))),l&&e.length>l?(0,i.Y)(r.A,{name:"...",onClick:()=>d(l)}):null]})})}},76617:(e,a,t)=>{t.d(a,{hT:()=>oa,Ay:()=>ca});var n=t(44383),l=t.n(n),r=t(62193),i=t.n(r),o=t(72391),s=t(96453),d=t(95579),c=t(96540),h=t(61574),p=t(62221),u=t(48327),m=t(15595),g=t(25946),b=t(85861),v=t(46920),f=t(12249);function y(){return y=Object.assign?Object.assign.bind():function(e){for(var a=1;a<arguments.length;a++){var t=arguments[a];for(var n in t)Object.prototype.hasOwnProperty.call(t,n)&&(e[n]=t[n])}return e},y.apply(this,arguments)}const _={position:"absolute",bottom:0,left:0,height:0,overflow:"hidden","padding-top":0,"padding-bottom":0,border:"none"},x=["box-sizing","width","font-size","font-weight","font-family","font-style","letter-spacing","text-indent","white-space","word-break","overflow-wrap","padding-left","padding-right"],Y=["component","ellipsis","trimRight","className"];function w(e,a){for(;e&&a--;)e=e.previousElementSibling;return e}const C={basedOn:void 0,className:"",component:"div",ellipsis:"…",maxLine:1,onReflow(){},text:"",trimRight:!0,winWidth:void 0},S=Object.keys(C);class A extends c.Component{constructor(e){super(e),this.state={text:e.text,clamped:!1},this.units=[],this.maxLine=0,this.canvas=null}componentDidMount(){this.initCanvas(),this.reflow(this.props)}componentDidUpdate(e){e.winWidth!==this.props.winWidth&&this.copyStyleToCanvas(),this.props!==e&&this.reflow(this.props)}componentWillUnmount(){this.canvas&&(this.canvas.parentNode.removeChild(this.canvas),this.canvas=null)}setState(e,a){return void 0!==e.clamped&&(this.clamped=e.clamped),super.setState(e,a)}initCanvas(){if(this.canvas)return;const e=this.canvas=document.createElement("div");e.className=`LinesEllipsis-canvas ${this.props.className}`,e.setAttribute("aria-hidden","true"),this.copyStyleToCanvas(),Object.keys(_).forEach((a=>{e.style[a]=_[a]})),document.body.appendChild(e)}copyStyleToCanvas(){const e=window.getComputedStyle(this.target);x.forEach((a=>{this.canvas.style[a]=e[a]}))}reflow(e){const a=e.basedOn||(/^[\x00-\x7F]+$/.test(e.text)?"words":"letters");switch(a){case"words":this.units=e.text.split(/\b|(?=\W)/);break;case"letters":this.units=Array.from(e.text);break;default:throw new Error(`Unsupported options basedOn: ${a}`)}this.maxLine=+e.maxLine||1,this.canvas.innerHTML=this.units.map((e=>`<span class='LinesEllipsis-unit'>${e}</span>`)).join("");const t=this.putEllipsis(this.calcIndexes()),n=t>-1,l={clamped:n,text:n?this.units.slice(0,t).join(""):e.text};this.setState(l,e.onReflow.bind(this,l))}calcIndexes(){const e=[0];let a=this.canvas.firstElementChild;if(!a)return e;let t=0,n=1,l=a.offsetTop;for(;(a=a.nextElementSibling)&&(a.offsetTop>l&&(n++,e.push(t),l=a.offsetTop),t++,!(n>this.maxLine)););return e}putEllipsis(e){if(e.length<=this.maxLine)return-1;const a=e[this.maxLine],t=this.units.slice(0,a),n=this.canvas.children[a].offsetTop;this.canvas.innerHTML=t.map(((e,a)=>`<span class='LinesEllipsis-unit'>${e}</span>`)).join("")+`<wbr><span class='LinesEllipsis-ellipsis'>${this.props.ellipsis}</span>`;const l=this.canvas.lastElementChild;let r=w(l,2);for(;r&&(l.offsetTop>n||l.offsetHeight>r.offsetHeight||l.offsetTop>r.offsetTop);)this.canvas.removeChild(r),r=w(l,2),t.pop();return t.length}isClamped(){return this.clamped}render(){const{text:e,clamped:a}=this.state,t=this.props,{component:n,ellipsis:l,trimRight:r,className:i}=t,o=function(e,a){if(null==e)return{};var t,n,l={},r=Object.keys(e);for(n=0;n<r.length;n++)t=r[n],a.indexOf(t)>=0||(l[t]=e[t]);return l}(t,Y);return c.createElement(n,y({className:`LinesEllipsis ${a?"LinesEllipsis--clamped":""} ${i}`,ref:e=>this.target=e},function(e,a){if(!e||"object"!=typeof e)return e;const t={};return Object.keys(e).forEach((n=>{a.indexOf(n)>-1||(t[n]=e[n])})),t}(o,S)),a&&r?e.replace(/[\s\uFEFF\xA0]+$/,""):e,c.createElement("wbr",null),a&&c.createElement("span",{className:"LinesEllipsis-ellipsis"},l))}}A.defaultProps=C;var D=t(2445);const F=(0,s.I4)(v.A)`
  height: auto;
  display: flex;
  flex-direction: column;
  padding: 0;
`,N=s.I4.div`
  padding: ${({theme:e})=>4*e.gridUnit}px;
  height: ${({theme:e})=>18*e.gridUnit}px;
  margin: ${({theme:e})=>3*e.gridUnit}px 0;

  .default-db-icon {
    font-size: 36px;
    color: ${({theme:e})=>e.colors.grayscale.base};
    margin-right: 0;
    span:first-of-type {
      margin-right: 0;
    }
  }

  &:first-of-type {
    margin-right: 0;
  }

  img {
    width: ${({theme:e})=>10*e.gridUnit}px;
    height: ${({theme:e})=>10*e.gridUnit}px;
    margin: 0;
    &:first-of-type {
      margin-right: 0;
    }
  }
  svg {
    &:first-of-type {
      margin-right: 0;
    }
  }
`,E=s.I4.div`
  max-height: calc(1.5em * 2);
  white-space: break-spaces;

  &:first-of-type {
    margin-right: 0;
  }

  .LinesEllipsis {
    &:first-of-type {
      margin-right: 0;
    }
  }
`,$=s.I4.div`
  padding: ${({theme:e})=>4*e.gridUnit}px 0;
  border-radius: 0 0 ${({theme:e})=>e.borderRadius}px
    ${({theme:e})=>e.borderRadius}px;
  background-color: ${({theme:e})=>e.colors.grayscale.light4};
  width: 100%;
  line-height: 1.5em;
  overflow: hidden;
  white-space: no-wrap;
  text-overflow: ellipsis;

  &:first-of-type {
    margin-right: 0;
  }
`,k=(0,s.I4)((({icon:e,altText:a,buttonText:t,...n})=>(0,D.FD)(F,{...n,children:[(0,D.FD)(N,{children:[e&&(0,D.Y)("img",{src:e,alt:a}),!e&&(0,D.Y)(f.A.DatabaseOutlined,{className:"default-db-icon","aria-label":"default-icon"})]}),(0,D.Y)($,{children:(0,D.Y)(E,{children:(0,D.Y)(A,{text:t,maxLine:"2",basedOn:"words",trimRight:!0})})})]})))`
  text-transform: none;
  background-color: ${({theme:e})=>e.colors.grayscale.light5};
  font-weight: ${({theme:e})=>e.typography.weights.normal};
  color: ${({theme:e})=>e.colors.grayscale.dark2};
  border: 1px solid ${({theme:e})=>e.colors.grayscale.light2};
  margin: 0;
  width: 100%;

  &:hover,
  &:focus {
    background-color: ${({theme:e})=>e.colors.grayscale.light5};
    color: ${({theme:e})=>e.colors.grayscale.dark2};
    border: 1px solid ${({theme:e})=>e.colors.grayscale.light2};
    box-shadow: 4px 4px 20px ${({theme:e})=>e.colors.grayscale.light2};
  }
`;var I,T,U=t(31641),P=t(5261),q=t(97987),L=t(79427),O=t(31383),M=t(50500),R=t(28292),H=t(17444);!function(e){e.SqlalchemyUri="sqlalchemy_form",e.DynamicForm="dynamic_form"}(I||(I={})),function(e){e.GSheet="gsheets",e.BigQuery="bigquery",e.Snowflake="snowflake"}(T||(T={}));var j=t(17437),z=t(46942),B=t.n(z),V=t(27366),W=t(85994),K=t(61693),J=t(24976);const Q=j.AH`
  margin-bottom: 0;
`,G=s.I4.header`
  padding: ${({theme:e})=>2*e.gridUnit}px
    ${({theme:e})=>4*e.gridUnit}px;
  line-height: ${({theme:e})=>6*e.gridUnit}px;

  .helper-top {
    padding-bottom: 0;
    color: ${({theme:e})=>e.colors.grayscale.base};
    font-size: ${({theme:e})=>e.typography.sizes.s}px;
    margin: 0;
  }

  .subheader-text {
    line-height: ${({theme:e})=>4.25*e.gridUnit}px;
  }

  .helper-bottom {
    padding-top: 0;
    color: ${({theme:e})=>e.colors.grayscale.base};
    font-size: ${({theme:e})=>e.typography.sizes.s}px;
    margin: 0;
  }

  h4 {
    color: ${({theme:e})=>e.colors.grayscale.dark2};
    font-size: ${({theme:e})=>e.typography.sizes.l}px;
    margin: 0;
    padding: 0;
    line-height: ${({theme:e})=>8*e.gridUnit}px;
  }

  .select-db {
    padding-bottom: ${({theme:e})=>2*e.gridUnit}px;
    .helper {
      margin: 0;
    }

    h4 {
      margin: 0 0 ${({theme:e})=>4*e.gridUnit}px;
    }
  }
`,X=j.AH`
  .ant-tabs-top {
    margin-top: 0;
  }
  .ant-tabs-top > .ant-tabs-nav {
    margin-bottom: 0;
  }
  .ant-tabs-tab {
    margin-right: 0;
  }
`,Z=j.AH`
  .antd5-modal-body {
    padding-left: 0;
    padding-right: 0;
    padding-top: 0;
  }
`,ee=e=>j.AH`
  margin-bottom: ${5*e.gridUnit}px;
  svg {
    margin-bottom: ${.25*e.gridUnit}px;
  }
`,ae=e=>j.AH`
  padding-left: ${2*e.gridUnit}px;
`,te=e=>j.AH`
  padding: ${4*e.gridUnit}px ${4*e.gridUnit}px 0;
`,ne=e=>j.AH`
  .ant-select-dropdown {
    height: ${40*e.gridUnit}px;
  }

  .antd5-modal-header {
    padding: ${4.5*e.gridUnit}px ${4*e.gridUnit}px
      ${4*e.gridUnit}px;
  }

  .antd5-modal-close-x .close {
    opacity: 1;
  }

  .antd5-modal-body {
    height: ${180.5*e.gridUnit}px;
  }

  .antd5-modal-footer {
    height: ${16.25*e.gridUnit}px;
  }
`,le=e=>j.AH`
  margin: ${4*e.gridUnit}px 0;
`,re=s.I4.div`
  ${({theme:e})=>j.AH`
    margin: 0 ${4*e.gridUnit}px ${4*e.gridUnit}px;
  `}
`,ie=e=>j.AH`
  .required {
    margin-left: ${e.gridUnit/2}px;
    color: ${e.colors.error.base};
  }

  .helper {
    display: block;
    padding: ${e.gridUnit}px 0;
    color: ${e.colors.grayscale.light1};
    font-size: ${e.typography.sizes.s}px;
    text-align: left;
  }
`,oe=e=>j.AH`
  .form-group {
    margin-bottom: ${4*e.gridUnit}px;
    &-w-50 {
      display: inline-block;
      width: ${`calc(50% - ${4*e.gridUnit}px)`};
      & + .form-group-w-50 {
        margin-left: ${8*e.gridUnit}px;
      }
    }
  }
  .control-label {
    color: ${e.colors.grayscale.dark1};
    font-size: ${e.typography.sizes.s}px;
  }
  .helper {
    color: ${e.colors.grayscale.light1};
    font-size: ${e.typography.sizes.s}px;
    margin-top: ${1.5*e.gridUnit}px;
  }
  .ant-tabs-content-holder {
    overflow: auto;
    max-height: 480px;
  }
`,se=e=>j.AH`
  label {
    color: ${e.colors.grayscale.dark1};
    font-size: ${e.typography.sizes.s}px;
    margin-bottom: 0;
  }
`,de=s.I4.div`
  ${({theme:e})=>j.AH`
    margin-bottom: ${6*e.gridUnit}px;
    &.mb-0 {
      margin-bottom: 0;
    }
    &.mb-8 {
      margin-bottom: ${2*e.gridUnit}px;
    }

    .control-label {
      color: ${e.colors.grayscale.dark1};
      font-size: ${e.typography.sizes.s}px;
      margin-bottom: ${2*e.gridUnit}px;
    }

    &.extra-container {
      padding-top: ${2*e.gridUnit}px;
    }

    .input-container {
      display: flex;
      align-items: top;

      label {
        display: flex;
        margin-left: ${2*e.gridUnit}px;
        margin-top: ${.75*e.gridUnit}px;
        font-family: ${e.typography.families.sansSerif};
        font-size: ${e.typography.sizes.m}px;
      }

      i {
        margin: 0 ${e.gridUnit}px;
      }
    }

    input,
    textarea {
      flex: 1 1 auto;
    }

    textarea {
      height: 160px;
      resize: none;
    }

    input::placeholder,
    textarea::placeholder {
      color: ${e.colors.grayscale.light1};
    }

    textarea,
    input[type='text'],
    input[type='number'] {
      padding: ${1.5*e.gridUnit}px ${2*e.gridUnit}px;
      border-style: none;
      border: 1px solid ${e.colors.grayscale.light2};
      border-radius: ${e.gridUnit}px;

      &[name='name'] {
        flex: 0 1 auto;
        width: 40%;
      }
    }
    &.expandable {
      height: 0;
      overflow: hidden;
      transition: height 0.25s;
      margin-left: ${8*e.gridUnit}px;
      margin-bottom: 0;
      padding: 0;
      .control-label {
        margin-bottom: 0;
      }
      &.open {
        height: ${108}px;
        padding-right: ${5*e.gridUnit}px;
      }
    }
  `}
`,ce=(0,s.I4)(J.iN)`
  flex: 1 1 auto;
  border: 1px solid ${({theme:e})=>e.colors.grayscale.light2};
  border-radius: ${({theme:e})=>e.gridUnit}px;
`,he=s.I4.div`
  padding-top: ${({theme:e})=>e.gridUnit}px;
  .input-container {
    padding-top: ${({theme:e})=>e.gridUnit}px;
    padding-bottom: ${({theme:e})=>e.gridUnit}px;
  }
  &.expandable {
    height: 0;
    overflow: hidden;
    transition: height 0.25s;
    margin-left: ${({theme:e})=>7*e.gridUnit}px;
    &.open {
      height: ${261}px;
      &.ctas-open {
        height: ${363}px;
      }
    }
  }
`,pe=s.I4.div`
  padding: 0 ${({theme:e})=>4*e.gridUnit}px;
  margin-top: ${({theme:e})=>6*e.gridUnit}px;
`,ue=e=>j.AH`
  font-weight: ${e.typography.weights.normal};
  text-transform: initial;
  padding-right: ${2*e.gridUnit}px;
`,me=e=>j.AH`
  font-size: ${3.5*e.gridUnit}px;
  font-weight: ${e.typography.weights.normal};
  text-transform: initial;
  padding-right: ${2*e.gridUnit}px;
`,ge=s.I4.div`
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: 0px;

  .helper {
    color: ${({theme:e})=>e.colors.grayscale.base};
    font-size: ${({theme:e})=>e.typography.sizes.s}px;
    margin: 0px;
  }
`,be=(s.I4.div`
  color: ${({theme:e})=>e.colors.grayscale.dark2};
  font-weight: ${({theme:e})=>e.typography.weights.bold};
  font-size: ${({theme:e})=>e.typography.sizes.m}px;
`,s.I4.div`
  color: ${({theme:e})=>e.colors.grayscale.dark1};
  font-size: ${({theme:e})=>e.typography.sizes.s}px;
`,s.I4.div`
  color: ${({theme:e})=>e.colors.grayscale.light1};
  font-size: ${({theme:e})=>e.typography.sizes.s}px;
`),ve=s.I4.div`
  color: ${({theme:e})=>e.colors.grayscale.dark1};
  font-size: ${({theme:e})=>e.typography.sizes.l}px;
  font-weight: ${({theme:e})=>e.typography.weights.bold};
`,fe=s.I4.div`
  .catalog-type-select {
    margin: 0 0 20px;
  }

  .label-select {
    color: ${({theme:e})=>e.colors.grayscale.dark1};
    font-size: 11px;
    margin: 0 5px ${({theme:e})=>2*e.gridUnit}px;
  }

  .label-paste {
    color: ${({theme:e})=>e.colors.grayscale.light1};
    font-size: 11px;
    line-height: 16px;
  }

  .input-container {
    margin: ${({theme:e})=>7*e.gridUnit}px 0;
    display: flex;
    flex-direction: column;
}
  }
  .input-form {
    height: 100px;
    width: 100%;
    border: 1px solid ${({theme:e})=>e.colors.grayscale.light2};
    border-radius: ${({theme:e})=>e.gridUnit}px;
    resize: vertical;
    padding: ${({theme:e})=>1.5*e.gridUnit}px
      ${({theme:e})=>2*e.gridUnit}px;
    &::placeholder {
      color: ${({theme:e})=>e.colors.grayscale.light1};
    }
  }

  .input-container {
    .input-upload {
      display: none !important;
    }
    .input-upload-current {
      display: flex;
      justify-content: space-between;
    }
    .input-upload-btn {
      width: ${({theme:e})=>32*e.gridUnit}px
    }
  }`,ye=s.I4.div`
  .preferred {
    .superset-button {
      margin-left: 0;
    }
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    margin: ${({theme:e})=>4*e.gridUnit}px;
  }

  .preferred-item {
    width: 32%;
    margin-bottom: ${({theme:e})=>2.5*e.gridUnit}px;
  }

  .available {
    margin: ${({theme:e})=>4*e.gridUnit}px;
    .available-label {
      font-size: ${({theme:e})=>e.typography.sizes.l}px;
      font-weight: ${({theme:e})=>e.typography.weights.bold};
      margin: ${({theme:e})=>6*e.gridUnit}px 0;
    }
    .available-select {
      width: 100%;
    }
  }

  .label-available-select {
    font-size: ${({theme:e})=>e.typography.sizes.s}px;
  }

  .control-label {
    color: ${({theme:e})=>e.colors.grayscale.dark1};
    font-size: ${({theme:e})=>e.typography.sizes.s}px;
    margin-bottom: ${({theme:e})=>2*e.gridUnit}px;
  }
`,_e=(0,s.I4)(v.A)`
  width: ${({theme:e})=>40*e.gridUnit}px;
`,xe=s.I4.div`
  position: sticky;
  top: 0;
  z-index: ${({theme:e})=>e.zIndex.max};
  background: ${({theme:e})=>e.colors.grayscale.light5};
  height: auto;
`,Ye=s.I4.div`
  margin-bottom: 16px;

  .catalog-type-select {
    margin: 0 0 20px;
  }

  .gsheet-title {
    font-size: ${({theme:e})=>e.typography.sizes.l}px;
    font-weight: ${({theme:e})=>e.typography.weights.bold};
    margin: ${({theme:e})=>10*e.gridUnit}px 0 16px;
  }

  .catalog-label {
    margin: 0 0 7px;
  }

  .catalog-name {
    display: flex;
    .catalog-name-input {
      width: 95%;
      margin-bottom: 0px;
    }
  }

  .catalog-name-url {
    margin: 4px 0;
    width: 95%;
  }

  .catalog-add-btn {
    width: 95%;
  }
`,we=s.I4.div`
  .ant-progress-inner {
    display: none;
  }

  .ant-upload-list-item-card-actions {
    display: none;
  }
`,Ce=({db:e,onInputChange:a,onTextChange:t,onEditorChange:n,onExtraInputChange:l,onExtraEditorChange:r,extraExtension:i})=>{var o,c,h,p,u;const m=!(null==e||!e.expose_in_sqllab),g=!!(null!=e&&e.allow_ctas||null!=e&&e.allow_cvas),b=null==e||null==(o=e.engine_information)?void 0:o.supports_file_upload,v=null==e||null==(c=e.engine_information)?void 0:c.supports_dynamic_catalog,f=JSON.parse((null==e?void 0:e.extra)||"{}",((e,a)=>"engine_params"===e&&"object"==typeof a?JSON.stringify(a):a)),y=(0,s.DP)(),_=null==i?void 0:i.component,x=null==i?void 0:i.logo,Y=null==i?void 0:i.description,w=!!(0,V.G7)(V.TO.ForceSqlLabRunAsync)||!(null==e||!e.allow_run_async),C=(0,V.G7)(V.TO.ForceSqlLabRunAsync);return(0,D.FD)(K.A,{expandIconPosition:"right",accordion:!0,css:e=>(e=>j.AH`
  .ant-collapse-header {
    padding-top: ${3.5*e.gridUnit}px;
    padding-bottom: ${2.5*e.gridUnit}px;

    .anticon.ant-collapse-arrow {
      top: calc(50% - ${6}px);
    }
    .helper {
      color: ${e.colors.grayscale.base};
    }
  }
  h4 {
    font-size: 16px;
    margin-top: 0;
    margin-bottom: ${e.gridUnit}px;
  }
  p.helper {
    margin-bottom: 0;
    padding: 0;
  }
`)(e),children:[(0,D.Y)(K.A.Panel,{header:(0,D.FD)("div",{children:[(0,D.Y)("h4",{children:(0,d.t)("SQL Lab")}),(0,D.Y)("p",{className:"helper",children:(0,d.t)("Adjust how this database will interact with SQL Lab.")})]}),children:(0,D.FD)(de,{css:Q,children:[(0,D.FD)("div",{className:"input-container",children:[(0,D.Y)(W.A,{id:"expose_in_sqllab",indeterminate:!1,checked:!(null==e||!e.expose_in_sqllab),onChange:a,labelText:(0,d.t)("Expose database in SQL Lab")}),(0,D.Y)(U.A,{tooltip:(0,d.t)("Allow this database to be queried in SQL Lab")})]}),(0,D.FD)(he,{className:B()("expandable",{open:m,"ctas-open":g}),children:[(0,D.Y)(de,{css:Q,children:(0,D.FD)("div",{className:"input-container",children:[(0,D.Y)(W.A,{id:"allow_ctas",indeterminate:!1,checked:!(null==e||!e.allow_ctas),onChange:a,labelText:(0,d.t)("Allow CREATE TABLE AS")}),(0,D.Y)(U.A,{tooltip:(0,d.t)("Allow creation of new tables based on queries")})]})}),(0,D.FD)(de,{css:Q,children:[(0,D.FD)("div",{className:"input-container",children:[(0,D.Y)(W.A,{id:"allow_cvas",indeterminate:!1,checked:!(null==e||!e.allow_cvas),onChange:a,labelText:(0,d.t)("Allow CREATE VIEW AS")}),(0,D.Y)(U.A,{tooltip:(0,d.t)("Allow creation of new views based on queries")})]}),(0,D.FD)(de,{className:B()("expandable",{open:g}),children:[(0,D.Y)("div",{className:"control-label",children:(0,d.t)("CTAS & CVAS SCHEMA")}),(0,D.Y)("div",{className:"input-container",children:(0,D.Y)("input",{type:"text",name:"force_ctas_schema",placeholder:(0,d.t)("Create or select schema..."),onChange:a,value:(null==e?void 0:e.force_ctas_schema)||""})}),(0,D.Y)("div",{className:"helper",children:(0,d.t)("Force all tables and views to be created in this schema when clicking CTAS or CVAS in SQL Lab.")})]})]}),(0,D.Y)(de,{css:Q,children:(0,D.FD)("div",{className:"input-container",children:[(0,D.Y)(W.A,{id:"allow_dml",indeterminate:!1,checked:!(null==e||!e.allow_dml),onChange:a,labelText:(0,d.t)("Allow DDL and DML")}),(0,D.Y)(U.A,{tooltip:(0,d.t)("Allow the execution of DDL (Data Definition Language: CREATE, DROP, TRUNCATE, etc.) and DML (Data Modification Language: INSERT, UPDATE, DELETE, etc)")})]})}),(0,D.Y)(de,{css:Q,children:(0,D.FD)("div",{className:"input-container",children:[(0,D.Y)(W.A,{id:"cost_estimate_enabled",indeterminate:!1,checked:!(null==f||!f.cost_estimate_enabled),onChange:l,labelText:(0,d.t)("Enable query cost estimation")}),(0,D.Y)(U.A,{tooltip:(0,d.t)("For Bigquery, Presto and Postgres, shows a button to compute cost before running a query.")})]})}),(0,D.Y)(de,{css:Q,children:(0,D.FD)("div",{className:"input-container",children:[(0,D.Y)(W.A,{id:"allows_virtual_table_explore",indeterminate:!1,checked:!1!==(null==f?void 0:f.allows_virtual_table_explore),onChange:l,labelText:(0,d.t)("Allow this database to be explored")}),(0,D.Y)(U.A,{tooltip:(0,d.t)("When enabled, users are able to visualize SQL Lab results in Explore.")})]})}),(0,D.Y)(de,{css:Q,children:(0,D.FD)("div",{className:"input-container",children:[(0,D.Y)(W.A,{id:"disable_data_preview",indeterminate:!1,checked:!(null==f||!f.disable_data_preview),onChange:l,labelText:(0,d.t)("Disable SQL Lab data preview queries")}),(0,D.Y)(U.A,{tooltip:(0,d.t)("Disable data preview when fetching table metadata in SQL Lab.  Useful to avoid browser performance issues when using  databases with very wide tables.")})]})}),(0,D.Y)(de,{children:(0,D.FD)("div",{className:"input-container",children:[(0,D.Y)(W.A,{id:"expand_rows",indeterminate:!1,checked:!(null==f||null==(h=f.schema_options)||!h.expand_rows),onChange:l,labelText:(0,d.t)("Enable row expansion in schemas")}),(0,D.Y)(U.A,{tooltip:(0,d.t)("For Trino, describe full schemas of nested ROW types, expanding them with dotted paths")})]})})]})]})},"1"),(0,D.FD)(K.A.Panel,{header:(0,D.FD)("div",{children:[(0,D.Y)("h4",{children:(0,d.t)("Performance")}),(0,D.Y)("p",{className:"helper",children:(0,d.t)("Adjust performance settings of this database.")})]}),children:[(0,D.FD)(de,{className:"mb-8",children:[(0,D.Y)("div",{className:"control-label",children:(0,d.t)("Chart cache timeout")}),(0,D.Y)("div",{className:"input-container",children:(0,D.Y)("input",{type:"number",name:"cache_timeout",value:(null==e?void 0:e.cache_timeout)||"",placeholder:(0,d.t)("Enter duration in seconds"),onChange:a})}),(0,D.Y)("div",{className:"helper",children:(0,d.t)("Duration (in seconds) of the caching timeout for charts of this database. A timeout of 0 indicates that the cache never expires, and -1 bypasses the cache. Note this defaults to the global timeout if undefined.")})]}),(0,D.FD)(de,{children:[(0,D.Y)("div",{className:"control-label",children:(0,d.t)("Schema cache timeout")}),(0,D.Y)("div",{className:"input-container",children:(0,D.Y)("input",{type:"number",name:"schema_cache_timeout",value:(null==f||null==(p=f.metadata_cache_timeout)?void 0:p.schema_cache_timeout)||"",placeholder:(0,d.t)("Enter duration in seconds"),onChange:l})}),(0,D.Y)("div",{className:"helper",children:(0,d.t)("Duration (in seconds) of the metadata caching timeout for schemas of this database. If left unset, the cache never expires.")})]}),(0,D.FD)(de,{children:[(0,D.Y)("div",{className:"control-label",children:(0,d.t)("Table cache timeout")}),(0,D.Y)("div",{className:"input-container",children:(0,D.Y)("input",{type:"number",name:"table_cache_timeout",value:(null==f||null==(u=f.metadata_cache_timeout)?void 0:u.table_cache_timeout)||"",placeholder:(0,d.t)("Enter duration in seconds"),onChange:l})}),(0,D.Y)("div",{className:"helper",children:(0,d.t)("Duration (in seconds) of the metadata caching timeout for tables of this database. If left unset, the cache never expires. ")})]}),(0,D.Y)(de,{css:(0,j.AH)({no_margin_bottom:Q},"",""),children:(0,D.FD)("div",{className:"input-container",children:[(0,D.Y)(W.A,{id:"allow_run_async",indeterminate:!1,checked:w,onChange:a,labelText:(0,d.t)("Asynchronous query execution")}),(0,D.Y)(U.A,{tooltip:(0,d.t)("Operate the database in asynchronous mode, meaning that the queries are executed on remote workers as opposed to on the web server itself. This assumes that you have a Celery worker setup as well as a results backend. Refer to the installation docs for more information.")}),C&&(0,D.Y)(U.A,{iconStyle:{color:y.colors.error.base},tooltip:(0,d.t)("This option has been disabled by the administrator.")})]})}),(0,D.Y)(de,{css:(0,j.AH)({no_margin_bottom:Q},"",""),children:(0,D.FD)("div",{className:"input-container",children:[(0,D.Y)(W.A,{id:"cancel_query_on_windows_unload",indeterminate:!1,checked:!(null==f||!f.cancel_query_on_windows_unload),onChange:l,labelText:(0,d.t)("Cancel query on window unload event")}),(0,D.Y)(U.A,{tooltip:(0,d.t)("Terminate running queries when browser window closed or navigated to another page. Available for Presto, Hive, MySQL, Postgres and Snowflake databases.")})]})})]},"2"),(0,D.FD)(K.A.Panel,{header:(0,D.FD)("div",{children:[(0,D.Y)("h4",{children:(0,d.t)("Security")}),(0,D.Y)("p",{className:"helper",children:(0,d.t)("Add extra connection information.")})]}),children:[(0,D.FD)(de,{children:[(0,D.Y)("div",{className:"control-label",children:(0,d.t)("Secure extra")}),(0,D.Y)("div",{className:"input-container",children:(0,D.Y)(ce,{name:"masked_encrypted_extra",value:(null==e?void 0:e.masked_encrypted_extra)||"",placeholder:(0,d.t)("Secure extra"),onChange:e=>n({json:e,name:"masked_encrypted_extra"}),width:"100%",height:"160px"})}),(0,D.Y)("div",{className:"helper",children:(0,D.Y)("div",{children:(0,d.t)("JSON string containing additional connection configuration. This is used to provide connection information for systems like Hive, Presto and BigQuery which do not conform to the username:password syntax normally used by SQLAlchemy.")})})]}),(0,D.FD)(de,{children:[(0,D.Y)("div",{className:"control-label",children:(0,d.t)("Root certificate")}),(0,D.Y)("div",{className:"input-container",children:(0,D.Y)("textarea",{name:"server_cert",value:(null==e?void 0:e.server_cert)||"",placeholder:(0,d.t)("Enter CA_BUNDLE"),onChange:t})}),(0,D.Y)("div",{className:"helper",children:(0,d.t)("Optional CA_BUNDLE contents to validate HTTPS requests. Only available on certain database engines.")})]}),(0,D.Y)(de,{css:b?{}:Q,children:(0,D.FD)("div",{className:"input-container",children:[(0,D.Y)(W.A,{id:"impersonate_user",indeterminate:!1,checked:!(null==e||!e.impersonate_user),onChange:a,labelText:(0,d.t)("Impersonate logged in user (Presto, Trino, Drill, Hive, and GSheets)")}),(0,D.Y)(U.A,{tooltip:(0,d.t)("If Presto or Trino, all the queries in SQL Lab are going to be executed as the currently logged on user who must have permission to run them. If Hive and hive.server2.enable.doAs is enabled, will run the queries as service account, but impersonate the currently logged on user via hive.server2.proxy.user property.")})]})}),b&&(0,D.Y)(de,{css:null!=e&&e.allow_file_upload?{}:Q,children:(0,D.Y)("div",{className:"input-container",children:(0,D.Y)(W.A,{id:"allow_file_upload",indeterminate:!1,checked:!(null==e||!e.allow_file_upload),onChange:a,labelText:(0,d.t)("Allow file uploads to database")})})}),b&&!(null==e||!e.allow_file_upload)&&(0,D.FD)(de,{css:Q,children:[(0,D.Y)("div",{className:"control-label",children:(0,d.t)("Schemas allowed for File upload")}),(0,D.Y)("div",{className:"input-container",children:(0,D.Y)("input",{type:"text",name:"schemas_allowed_for_file_upload",value:((null==f?void 0:f.schemas_allowed_for_file_upload)||[]).join(","),placeholder:"schema1,schema2",onChange:l})}),(0,D.Y)("div",{className:"helper",children:(0,d.t)("A comma-separated list of schemas that files are allowed to upload to.")})]})]},"3"),i&&_&&Y&&(0,D.Y)(K.A.Panel,{header:(0,D.FD)("div",{children:[x&&(0,D.Y)(x,{}),(0,D.Y)("span",{css:e=>({fontSize:e.typography.sizes.l,fontWeight:e.typography.weights.bold}),children:null==i?void 0:i.title}),(0,D.Y)("p",{className:"helper",children:(0,D.Y)(Y,{})})]}),collapsible:null!=i.enabled&&i.enabled()?"icon":"disabled",children:(0,D.Y)(de,{css:Q,children:(0,D.Y)(_,{db:e,onEdit:i.onEdit})})},null==i?void 0:i.title),(0,D.FD)(K.A.Panel,{header:(0,D.FD)("div",{children:[(0,D.Y)("h4",{children:(0,d.t)("Other")}),(0,D.Y)("p",{className:"helper",children:(0,d.t)("Additional settings.")})]}),children:[(0,D.FD)(de,{children:[(0,D.Y)("div",{className:"control-label",children:(0,d.t)("Metadata Parameters")}),(0,D.Y)("div",{className:"input-container",children:(0,D.Y)(ce,{name:"metadata_params",placeholder:(0,d.t)("Metadata Parameters"),onChange:e=>r({json:e,name:"metadata_params"}),width:"100%",height:"160px",value:Object.keys((null==f?void 0:f.metadata_params)||{}).length?"string"==typeof(null==f?void 0:f.metadata_params)?null==f?void 0:f.metadata_params:JSON.stringify(null==f?void 0:f.metadata_params):""})}),(0,D.Y)("div",{className:"helper",children:(0,D.Y)("div",{children:(0,d.t)("The metadata_params object gets unpacked into the sqlalchemy.MetaData call.")})})]}),(0,D.FD)(de,{children:[(0,D.Y)("div",{className:"control-label",children:(0,d.t)("Engine Parameters")}),(0,D.Y)("div",{className:"input-container",children:(0,D.Y)(ce,{name:"engine_params",placeholder:(0,d.t)("Engine Parameters"),onChange:e=>r({json:e,name:"engine_params"}),width:"100%",height:"160px",value:Object.keys((null==f?void 0:f.engine_params)||{}).length?null==f?void 0:f.engine_params:""})}),(0,D.Y)("div",{className:"helper",children:(0,D.Y)("div",{children:(0,d.t)("The engine_params object gets unpacked into the sqlalchemy.create_engine call.")})})]}),(0,D.FD)(de,{children:[(0,D.Y)("div",{className:"control-label",children:(0,d.t)("Version")}),(0,D.Y)("div",{className:"input-container",children:(0,D.Y)("input",{type:"text",name:"version",placeholder:(0,d.t)("Version number"),onChange:l,value:(null==f?void 0:f.version)||""})}),(0,D.Y)("div",{className:"helper",children:(0,d.t)("Specify the database version. This is used with Presto for query cost estimation, and Dremio for syntax changes, among others.")})]}),(0,D.Y)(de,{css:Q,children:(0,D.FD)("div",{className:"input-container",children:[(0,D.Y)(W.A,{id:"disable_drill_to_detail",indeterminate:!1,checked:!(null==f||!f.disable_drill_to_detail),onChange:l,labelText:(0,d.t)("Disable drill to detail")}),(0,D.Y)(U.A,{tooltip:(0,d.t)("Disables the drill to detail feature for this database.")})]})}),v&&(0,D.Y)(de,{css:Q,children:(0,D.FD)("div",{className:"input-container",children:[(0,D.Y)(W.A,{id:"allow_multi_catalog",indeterminate:!1,checked:!(null==f||!f.allow_multi_catalog),onChange:l,labelText:(0,d.t)("Allow changing catalogs")}),(0,D.Y)(U.A,{tooltip:(0,d.t)("Give access to multiple catalogs in a single database connection.")})]})})]},"4")]})};var Se=t(27588);const Ae=({db:e,onInputChange:a,testConnection:t,conf:n,testInProgress:l=!1,children:r})=>{var i,o;const s=(null==Se.A||null==(i=Se.A.DB_MODAL_SQLALCHEMY_FORM)?void 0:i.SQLALCHEMY_DOCS_URL)||"https://docs.sqlalchemy.org/en/13/core/engines.html",c=(null==Se.A||null==(o=Se.A.DB_MODAL_SQLALCHEMY_FORM)?void 0:o.SQLALCHEMY_DISPLAY_TEXT)||"SQLAlchemy docs";return(0,D.FD)(D.FK,{children:[(0,D.FD)(de,{children:[(0,D.FD)("div",{className:"control-label",children:[(0,d.t)("Display Name"),(0,D.Y)("span",{className:"required",children:"*"})]}),(0,D.Y)("div",{className:"input-container",children:(0,D.Y)("input",{type:"text",name:"database_name",value:(null==e?void 0:e.database_name)||"",placeholder:(0,d.t)("Name your database"),onChange:a})}),(0,D.Y)("div",{className:"helper",children:(0,d.t)("Pick a name to help you identify this database.")})]}),(0,D.FD)(de,{children:[(0,D.FD)("div",{className:"control-label",children:[(0,d.t)("SQLAlchemy URI"),(0,D.Y)("span",{className:"required",children:"*"})]}),(0,D.Y)("div",{className:"input-container",children:(0,D.Y)("input",{type:"text",name:"sqlalchemy_uri",value:(null==e?void 0:e.sqlalchemy_uri)||"",autoComplete:"off",placeholder:(null==e?void 0:e.sqlalchemy_uri_placeholder)||(0,d.t)("dialect+driver://username:password@host:port/database"),onChange:a})}),(0,D.FD)("div",{className:"helper",children:[(0,d.t)("Refer to the")," ",(0,D.Y)("a",{href:s||(null==n?void 0:n.SQLALCHEMY_DOCS_URL)||"",target:"_blank",rel:"noopener noreferrer",children:c||(null==n?void 0:n.SQLALCHEMY_DISPLAY_TEXT)||""})," ",(0,d.t)("for more information on how to structure your URI.")]})]}),r,(0,D.Y)(v.A,{onClick:t,loading:l,cta:!0,buttonStyle:"link",css:e=>(e=>j.AH`
  width: 100%;
  border: 1px solid ${e.colors.primary.dark2};
  color: ${e.colors.primary.dark2};
  &:hover,
  &:focus {
    border: 1px solid ${e.colors.primary.dark1};
    color: ${e.colors.primary.dark1};
  }
`)(e),children:(0,d.t)("Test connection")})]})};var De=t(40563),Fe=t(75488),Ne=t(90868);const Ee={account:{label:"Account",helpText:(0,d.t)("Copy the identifier of the account you are trying to connect to."),placeholder:(0,d.t)("e.g. xy12345.us-east-2.aws")},warehouse:{label:"Warehouse",placeholder:(0,d.t)("e.g. compute_wh"),className:"form-group-w-50"},role:{label:"Role",placeholder:(0,d.t)("e.g. AccountAdmin"),className:"form-group-w-50"}},$e=({required:e,changeMethods:a,getValidation:t,validationErrors:n,db:l,field:r})=>{var i,o;return(0,D.Y)(q.A,{id:r,name:r,required:e,value:null==l||null==(i=l.parameters)?void 0:i[r],validationMethods:{onBlur:t},errorMessage:null==n?void 0:n[r],placeholder:Ee[r].placeholder,helpText:null==(o=Ee[r])?void 0:o.helpText,label:Ee[r].label||r,onChange:a.onParametersChange,className:Ee[r].className||r})};var ke,Ie=t(40458);!function(e){e[e.JsonUpload=0]="JsonUpload",e[e.CopyPaste=1]="CopyPaste"}(ke||(ke={}));const Te={gsheets:"service_account_info",bigquery:"credentials_info"};var Ue={name:"s5xdrg",styles:"display:flex;align-items:center"};const Pe=({changeMethods:e,isEditMode:a,db:t,editNewDb:n})=>{var l;const r=(0,c.useRef)(null),[i,o]=(0,c.useState)(ke.JsonUpload.valueOf()),[s,h]=(0,c.useState)(null),[p,u]=(0,c.useState)(!0),g="gsheets"===(null==t?void 0:t.engine)?!a&&!p:!a,b=a&&"{}"!==(null==t?void 0:t.masked_encrypted_extra),v=(null==t?void 0:t.engine)&&Te[t.engine],y=null==t||null==(l=t.parameters)?void 0:l[v],_=y&&"object"==typeof y?JSON.stringify(y):y;return(0,D.FD)(fe,{children:["gsheets"===(null==t?void 0:t.engine)&&(0,D.FD)("div",{className:"catalog-type-select",children:[(0,D.Y)(Ie.A,{css:e=>(e=>j.AH`
  margin-bottom: ${2*e.gridUnit}px;
`)(e),required:!0,children:(0,d.t)("Type of Google Sheets allowed")}),(0,D.FD)(m._P,{style:{width:"100%"},defaultValue:b?"false":"true",onChange:e=>u("true"===e),children:[(0,D.Y)(m._P.Option,{value:"true",children:(0,d.t)("Publicly shared sheets only")},1),(0,D.Y)(m._P.Option,{value:"false",children:(0,d.t)("Public and privately shared sheets")},2)]})]}),g&&(0,D.FD)(D.FK,{children:[(0,D.Y)(Ie.A,{required:!0,children:(0,d.t)("How do you want to enter service account credentials?")}),(0,D.FD)(m._P,{defaultValue:i,style:{width:"100%"},onChange:e=>o(e),children:[(0,D.Y)(m._P.Option,{value:ke.JsonUpload,children:(0,d.t)("Upload JSON file")}),(0,D.Y)(m._P.Option,{value:ke.CopyPaste,children:(0,d.t)("Copy and Paste JSON credentials")})]})]}),i===ke.CopyPaste||a||n?(0,D.FD)("div",{className:"input-container",children:[(0,D.Y)(Ie.A,{required:!0,children:(0,d.t)("Service Account")}),(0,D.Y)("textarea",{className:"input-form",name:v,value:"boolean"==typeof _?String(_):_,onChange:e.onParametersChange,placeholder:(0,d.t)("Paste content of service credentials JSON file here")}),(0,D.Y)("span",{className:"label-paste",children:(0,d.t)("Copy and paste the entire service account .json file here")})]}):g&&(0,D.FD)("div",{className:"input-container",css:e=>ee(e),children:[(0,D.FD)("div",{css:Ue,children:[(0,D.Y)(Ie.A,{required:!0,children:(0,d.t)("Upload Credentials")}),(0,D.Y)(U.A,{tooltip:(0,d.t)("Use the JSON file you automatically downloaded when creating your service account."),viewBox:"0 0 24 24"})]}),!s&&(0,D.Y)(m.$n,{className:"input-upload-btn",onClick:()=>{var e;return null==(e=r.current)?void 0:e.click()},children:(0,d.t)("Choose File")}),s&&(0,D.FD)("div",{className:"input-upload-current",children:[s,(0,D.Y)(f.A.DeleteFilled,{iconSize:"m",onClick:()=>{h(null),e.onParametersChange({target:{name:v,value:""}})}})]}),(0,D.Y)("input",{ref:r,id:"selectedFile",accept:".json",className:"input-upload",type:"file",onChange:async a=>{var t,n;let l;a.target.files&&(l=a.target.files[0]),h(null==(t=l)?void 0:t.name),e.onParametersChange({target:{type:null,name:v,value:await(null==(n=l)?void 0:n.text()),checked:!1}}),r.current&&(r.current.value=null)}})]})]})},qe=({clearValidationErrors:e,changeMethods:a,db:t,dbModel:n})=>{var l,r,o;const[s,h]=(0,c.useState)(!1),p=(0,V.G7)(V.TO.SshTunneling),u=(null==n||null==(l=n.engine_information)?void 0:l.disable_ssh_tunneling)||!1,m=p&&!u;return(0,c.useEffect)((()=>{var e;m&&void 0!==(null==t||null==(e=t.parameters)?void 0:e.ssh)&&h(t.parameters.ssh)}),[null==t||null==(r=t.parameters)?void 0:r.ssh,m]),(0,c.useEffect)((()=>{var e;m&&void 0===(null==t||null==(e=t.parameters)?void 0:e.ssh)&&!i()(null==t?void 0:t.ssh_tunnel)&&a.onParametersChange({target:{type:"toggle",name:"ssh",checked:!0,value:!0}})}),[a,null==t||null==(o=t.parameters)?void 0:o.ssh,null==t?void 0:t.ssh_tunnel,m]),m?(0,D.FD)("div",{css:e=>ee(e),children:[(0,D.Y)(Fe.d,{checked:s,onChange:t=>{h(t),a.onParametersChange({target:{type:"toggle",name:"ssh",checked:!0,value:t}}),e()}}),(0,D.Y)("span",{css:ae,children:(0,d.t)("SSH Tunnel")}),(0,D.Y)(U.A,{tooltip:(0,d.t)("SSH Tunnel configuration parameters"),placement:"right",viewBox:"0 -5 24 24"})]}):null};var Le;const Oe=["host","port","database","default_catalog","default_schema","username","password","access_token","http_path","http_path_field","database_name","project_id","credentials_info","service_account_info","catalog","query","encryption","account","warehouse","role","ssh","oauth2_client"],Me={host:({required:e,changeMethods:a,getValidation:t,validationErrors:n,db:l})=>{var r;return(0,D.Y)(q.A,{id:"host",name:"host",value:null==l||null==(r=l.parameters)?void 0:r.host,required:e,hasTooltip:!0,tooltipText:(0,d.t)("This can be either an IP address (e.g. 127.0.0.1) or a domain name (e.g. mydatabase.com)."),validationMethods:{onBlur:t},errorMessage:null==n?void 0:n.host,placeholder:(0,d.t)("e.g. 127.0.0.1"),className:"form-group-w-50",label:(0,d.t)("Host"),onChange:a.onParametersChange})},http_path:({required:e,changeMethods:a,getValidation:t,validationErrors:n,db:l})=>{var r,i;const o=JSON.parse((null==l?void 0:l.extra)||"{}");return(0,D.Y)(q.A,{id:"http_path",name:"http_path",required:e,value:null==(r=o.engine_params)||null==(i=r.connect_args)?void 0:i.http_path,validationMethods:{onBlur:t},errorMessage:null==n?void 0:n.http_path,placeholder:(0,d.t)("e.g. sql/protocolv1/o/12345"),label:"HTTP Path",onChange:a.onExtraInputChange,helpText:(0,d.t)("Copy the name of the HTTP Path of your cluster.")})},http_path_field:({required:e,changeMethods:a,getValidation:t,validationErrors:n,db:l})=>{var r;return(0,D.Y)(q.A,{id:"http_path_field",name:"http_path_field",required:e,value:null==l||null==(r=l.parameters)?void 0:r.http_path_field,validationMethods:{onBlur:t},errorMessage:null==n?void 0:n.http_path,placeholder:(0,d.t)("e.g. sql/protocolv1/o/12345"),label:"HTTP Path",onChange:a.onParametersChange,helpText:(0,d.t)("Copy the name of the HTTP Path of your cluster.")})},port:({required:e,changeMethods:a,getValidation:t,validationErrors:n,db:l})=>{var r;return(0,D.Y)(D.FK,{children:(0,D.Y)(q.A,{id:"port",name:"port",type:"number",required:e,value:null==l||null==(r=l.parameters)?void 0:r.port,validationMethods:{onBlur:t},errorMessage:null==n?void 0:n.port,placeholder:(0,d.t)("e.g. 5432"),className:"form-group-w-50",label:(0,d.t)("Port"),onChange:a.onParametersChange})})},database:({required:e,changeMethods:a,getValidation:t,validationErrors:n,placeholder:l,db:r})=>{var i;return(0,D.Y)(q.A,{id:"database",name:"database",required:e,value:null==r||null==(i=r.parameters)?void 0:i.database,validationMethods:{onBlur:t},errorMessage:null==n?void 0:n.database,placeholder:null!=l?l:(0,d.t)("e.g. world_population"),label:(0,d.t)("Database name"),onChange:a.onParametersChange,helpText:(0,d.t)("Copy the name of the database you are trying to connect to.")})},default_catalog:({required:e,changeMethods:a,getValidation:t,validationErrors:n,db:l})=>{var r;return(0,D.Y)(q.A,{id:"default_catalog",name:"default_catalog",required:e,value:null==l||null==(r=l.parameters)?void 0:r.default_catalog,validationMethods:{onBlur:t},errorMessage:null==n?void 0:n.default_catalog,placeholder:(0,d.t)("e.g. hive_metastore"),label:(0,d.t)("Default Catalog"),onChange:a.onParametersChange,helpText:(0,d.t)("The default catalog that should be used for the connection.")})},default_schema:({required:e,changeMethods:a,getValidation:t,validationErrors:n,db:l})=>{var r;return(0,D.Y)(q.A,{id:"default_schema",name:"default_schema",required:e,value:null==l||null==(r=l.parameters)?void 0:r.default_schema,validationMethods:{onBlur:t},errorMessage:null==n?void 0:n.default_schema,placeholder:(0,d.t)("e.g. default"),label:(0,d.t)("Default Schema"),onChange:a.onParametersChange,helpText:(0,d.t)("The default schema that should be used for the connection.")})},username:({required:e,changeMethods:a,getValidation:t,validationErrors:n,db:l})=>{var r;return(0,D.Y)(q.A,{id:"username",name:"username",required:e,value:null==l||null==(r=l.parameters)?void 0:r.username,validationMethods:{onBlur:t},errorMessage:null==n?void 0:n.username,placeholder:(0,d.t)("e.g. Analytics"),label:(0,d.t)("Username"),onChange:a.onParametersChange})},password:({required:e,changeMethods:a,getValidation:t,validationErrors:n,db:l,isEditMode:r})=>{var i;return(0,D.Y)(q.A,{id:"password",name:"password",required:e,visibilityToggle:!r,value:null==l||null==(i=l.parameters)?void 0:i.password,validationMethods:{onBlur:t},errorMessage:null==n?void 0:n.password,placeholder:(0,d.t)("e.g. ********"),label:(0,d.t)("Password"),onChange:a.onParametersChange})},oauth2_client:({changeMethods:e,db:a})=>{var t,n,l,r,i;const o=JSON.parse((null==a?void 0:a.masked_encrypted_extra)||"{}"),[s,d]=(0,c.useState)({id:(null==(t=o.oauth2_client_info)?void 0:t.id)||"",secret:(null==(n=o.oauth2_client_info)?void 0:n.secret)||"",authorization_request_uri:(null==(l=o.oauth2_client_info)?void 0:l.authorization_request_uri)||"",token_request_uri:(null==(r=o.oauth2_client_info)?void 0:r.token_request_uri)||"",scope:(null==(i=o.oauth2_client_info)?void 0:i.scope)||""}),h=a=>t=>{const n={...s,[a]:t.target.value};d(n);const l={target:{name:"oauth2_client_info",value:n}};e.onEncryptedExtraInputChange(l)};return(0,D.Y)(K.A,{children:(0,D.FD)(K.A.Panel,{header:"OAuth2 client information",children:[(0,D.Y)(De.eI,{label:"Client ID",children:(0,D.Y)(Ne.pd,{value:s.id,onChange:h("id")})}),(0,D.Y)(De.eI,{label:"Client Secret",children:(0,D.Y)(Ne.pd,{type:"password",value:s.secret,onChange:h("secret")})}),(0,D.Y)(De.eI,{label:"Authorization Request URI",children:(0,D.Y)(Ne.pd,{placeholder:"https://",value:s.authorization_request_uri,onChange:h("authorization_request_uri")})}),(0,D.Y)(De.eI,{label:"Token Request URI",children:(0,D.Y)(Ne.pd,{placeholder:"https://",value:s.token_request_uri,onChange:h("token_request_uri")})}),(0,D.Y)(De.eI,{label:"Scope",children:(0,D.Y)(Ne.pd,{value:s.scope,onChange:h("scope")})})]},"1")})},access_token:({required:e,changeMethods:a,getValidation:t,validationErrors:n,db:l,isEditMode:r,default_value:i,description:o})=>{var s;return(0,D.Y)(q.A,{id:"access_token",name:"access_token",required:e,visibilityToggle:!r,value:null==l||null==(s=l.parameters)?void 0:s.access_token,validationMethods:{onBlur:t},errorMessage:null==n?void 0:n.access_token,placeholder:(0,d.t)("Paste your access token here"),get_url:"string"==typeof i&&i.includes("https://")?i:null,description:o,label:(0,d.t)("Access token"),onChange:a.onParametersChange})},database_name:({changeMethods:e,getValidation:a,validationErrors:t,db:n})=>(0,D.Y)(D.FK,{children:(0,D.Y)(q.A,{id:"database_name",name:"database_name",required:!0,value:null==n?void 0:n.database_name,validationMethods:{onBlur:a},errorMessage:null==t?void 0:t.database_name,placeholder:"",label:(0,d.t)("Display Name"),onChange:e.onChange,helpText:(0,d.t)("Pick a nickname for how the database will display in Superset.")})}),query:({required:e,changeMethods:a,getValidation:t,validationErrors:n,db:l})=>(0,D.Y)(q.A,{id:"query_input",name:"query_input",required:e,value:(null==l?void 0:l.query_input)||"",validationMethods:{onBlur:t},errorMessage:null==n?void 0:n.query,placeholder:(0,d.t)("e.g. param1=value1&param2=value2"),label:(0,d.t)("Additional Parameters"),onChange:a.onQueryChange,helpText:(0,d.t)("Add additional custom parameters")}),encryption:({isEditMode:e,changeMethods:a,db:t,sslForced:n})=>{var l;return(0,D.FD)("div",{css:e=>ee(e),children:[(0,D.Y)(Fe.d,{disabled:n&&!e,checked:(null==t||null==(l=t.parameters)?void 0:l.encryption)||n,onChange:e=>{a.onParametersChange({target:{type:"toggle",name:"encryption",checked:!0,value:e}})}}),(0,D.Y)("span",{css:ae,children:"SSL"}),(0,D.Y)(U.A,{tooltip:(0,d.t)('SSL Mode "require" will be used.'),placement:"right",viewBox:"0 -5 24 24"})]})},credentials_info:Pe,service_account_info:Pe,catalog:({required:e,changeMethods:a,getValidation:t,validationErrors:n,db:l})=>{const r=(null==l?void 0:l.catalog)||[],i=n||{};return(0,D.FD)(Ye,{children:[(0,D.Y)("h4",{className:"gsheet-title",children:(0,d.t)("Connect Google Sheets as tables to this database")}),(0,D.FD)("div",{children:[null==r?void 0:r.map(((n,l)=>{var o,s;return(0,D.FD)(D.FK,{children:[(0,D.Y)(Ie.A,{className:"catalog-label",required:!0,children:(0,d.t)("Google Sheet Name and URL")}),(0,D.FD)("div",{className:"catalog-name",children:[(0,D.Y)(q.A,{className:"catalog-name-input",required:e,validationMethods:{onBlur:t},errorMessage:null==(o=i[l])?void 0:o.name,placeholder:(0,d.t)("Enter a name for this sheet"),onChange:e=>{a.onParametersChange({target:{type:`catalog-${l}`,name:"name",value:e.target.value}})},value:n.name}),(null==r?void 0:r.length)>1&&(0,D.Y)(f.A.CloseOutlined,{css:e=>j.AH`
                    align-self: center;
                    background: ${e.colors.grayscale.light4};
                    margin: 5px 5px 8px 5px;

                    &.anticon > * {
                      line-height: 0;
                    }
                  `,iconSize:"m",onClick:()=>a.onRemoveTableCatalog(l)})]}),(0,D.Y)(q.A,{className:"catalog-name-url",required:e,validationMethods:{onBlur:t},errorMessage:null==(s=i[l])?void 0:s.url,placeholder:(0,d.t)("Paste the shareable Google Sheet URL here"),onChange:e=>a.onParametersChange({target:{type:`catalog-${l}`,name:"value",value:e.target.value}}),value:n.value})]})})),(0,D.FD)(_e,{className:"catalog-add-btn",onClick:()=>{a.onAddTableCatalog()},children:["+ ",(0,d.t)("Add sheet")]})]})]})},warehouse:$e,role:$e,account:$e,ssh:null!=(Le=(0,o.a)().get("ssh_tunnel.form.switch"))?Le:qe,project_id:({changeMethods:e,getValidation:a,validationErrors:t,db:n})=>{var l;return(0,D.Y)(D.FK,{children:(0,D.Y)(q.A,{id:"project_id",name:"project_id",required:!0,value:null==n||null==(l=n.parameters)?void 0:l.project_id,validationMethods:{onBlur:a},errorMessage:null==t?void 0:t.project_id,placeholder:"your-project-1234-a1",label:(0,d.t)("Project Id"),onChange:e.onParametersChange,helpText:(0,d.t)("Enter the unique project id for your database.")})})}},Re=({dbModel:e,db:a,editNewDb:t,getPlaceholder:n,getValidation:l,isEditMode:r=!1,onAddTableCatalog:i,onChange:o,onExtraInputChange:s,onEncryptedExtraInputChange:d,onParametersChange:c,onParametersUploadFileChange:h,onQueryChange:p,onRemoveTableCatalog:u,sslForced:m,validationErrors:g,clearValidationErrors:b})=>{const v=null==e?void 0:e.parameters;return(0,D.Y)(De.lV,{children:(0,D.Y)("div",{css:e=>[te,se(e)],children:v&&Oe.filter((e=>Object.keys(v.properties).includes(e)||"database_name"===e)).map((e=>{var f,y,_;return Me[e]({required:null==(f=v.required)?void 0:f.includes(e),changeMethods:{onParametersChange:c,onChange:o,onQueryChange:p,onParametersUploadFileChange:h,onAddTableCatalog:i,onRemoveTableCatalog:u,onExtraInputChange:s,onEncryptedExtraInputChange:d},validationErrors:g,getValidation:l,clearValidationErrors:b,db:a,key:e,field:e,default_value:null==(y=v.properties[e])?void 0:y.default,description:null==(_=v.properties[e])?void 0:_.description,isEditMode:r,sslForced:m,editNewDb:t,placeholder:n?n(e):void 0})}))})})},He=(0,M.xK)(),je=He?He.support:"https://superset.apache.org/docs/configuration/databases#installing-database-drivers",ze={postgresql:"https://superset.apache.org",mssql:"https://superset.apache.org/docs/databases/sql-server",gsheets:"https://superset.apache.org/docs/databases/google-sheets"},Be=({isLoading:e,isEditMode:a,useSqlAlchemyForm:t,hasConnectedDb:n,db:l,dbName:r,dbModel:i,editNewDb:o,fileList:s})=>{const c=s&&(null==s?void 0:s.length)>0,h=(0,D.FD)(G,{children:[(0,D.Y)(be,{children:null==l?void 0:l.backend}),(0,D.Y)(ve,{children:r})]}),p=(0,D.FD)(G,{children:[(0,D.Y)("p",{className:"helper-top",children:(0,d.t)("STEP %(stepCurr)s OF %(stepLast)s",{stepCurr:2,stepLast:2})}),(0,D.Y)("h4",{children:(0,d.t)("Enter Primary Credentials")}),(0,D.FD)("p",{className:"helper-bottom",children:[(0,d.t)("Need help? Learn how to connect your database")," ",(0,D.Y)("a",{href:(null==He?void 0:He.default)||je,target:"_blank",rel:"noopener noreferrer",children:(0,d.t)("here")}),"."]})]}),u=(0,D.Y)(xe,{children:(0,D.FD)(G,{children:[(0,D.Y)("p",{className:"helper-top",children:(0,d.t)("STEP %(stepCurr)s OF %(stepLast)s",{stepCurr:3,stepLast:3})}),(0,D.Y)("h4",{className:"step-3-text",children:(0,d.t)("Database connected")}),(0,D.Y)("p",{className:"subheader-text",children:(0,d.t)("Create a dataset to begin visualizing your data as a chart or go to\n          SQL Lab to query your data.")})]})}),m=(0,D.Y)(xe,{children:(0,D.FD)(G,{children:[(0,D.Y)("p",{className:"helper-top",children:(0,d.t)("STEP %(stepCurr)s OF %(stepLast)s",{stepCurr:2,stepLast:3})}),(0,D.Y)("h4",{children:(0,d.t)("Enter the required %(dbModelName)s credentials",{dbModelName:i.name})}),(0,D.FD)("p",{className:"helper-bottom",children:[(0,d.t)("Need help? Learn more about")," ",(0,D.FD)("a",{href:(g=null==l?void 0:l.engine,g?He?He[g]||He.default:ze[g]?ze[g]:`https://superset.apache.org/docs/databases/${g}`:null),target:"_blank",rel:"noopener noreferrer",children:[(0,d.t)("connecting to %(dbModelName)s",{dbModelName:i.name}),"."]})]})]})});var g;const b=(0,D.Y)(G,{children:(0,D.FD)("div",{className:"select-db",children:[(0,D.Y)("p",{className:"helper-top",children:(0,d.t)("STEP %(stepCurr)s OF %(stepLast)s",{stepCurr:1,stepLast:3})}),(0,D.Y)("h4",{children:(0,d.t)("Select a database to connect")})]})}),v=(0,D.Y)(xe,{children:(0,D.FD)(G,{children:[(0,D.Y)("p",{className:"helper-top",children:(0,d.t)("STEP %(stepCurr)s OF %(stepLast)s",{stepCurr:2,stepLast:2})}),(0,D.Y)("h4",{children:(0,d.t)("Enter the required %(dbModelName)s credentials",{dbModelName:i.name})}),(0,D.Y)("p",{className:"helper-bottom",children:c?s[0].name:""})]})});return c?v:e?(0,D.Y)(D.FK,{}):a?h:t?p:n&&!o?u:l||o?m:b};var Ve=t(69193),We=t(36255),Ke=t(27236);const Je=s.I4.div`
  padding-top: ${({theme:e})=>2*e.gridUnit}px;
  label {
    color: ${({theme:e})=>e.colors.grayscale.base};
    margin-bottom: ${({theme:e})=>2*e.gridUnit}px;
  }
`,Qe=(0,s.I4)(m.fI)`
  padding-bottom: ${({theme:e})=>2*e.gridUnit}px;
`,Ge=(0,s.I4)(m.Wq.Item)`
  margin-bottom: 0 !important;
`,Xe=(0,s.I4)(We.A.Password)`
  margin: ${({theme:e})=>`${e.gridUnit}px 0 ${2*e.gridUnit}px`};
`,Ze=({db:e,onSSHTunnelParametersChange:a,setSSHTunnelLoginMethod:t})=>{var n,l,r,i,o,s;const[h,p]=(0,c.useState)(oa.Password);return(0,D.FD)(De.lV,{children:[(0,D.FD)(Qe,{gutter:16,children:[(0,D.Y)(m.fv,{xs:24,md:12,children:(0,D.FD)(Je,{children:[(0,D.Y)(De.lR,{htmlFor:"server_address",required:!0,children:(0,d.t)("SSH Host")}),(0,D.Y)(Ne.pd,{name:"server_address",type:"text",placeholder:(0,d.t)("e.g. 127.0.0.1"),value:(null==e||null==(n=e.ssh_tunnel)?void 0:n.server_address)||"",onChange:a})]})}),(0,D.Y)(m.fv,{xs:24,md:12,children:(0,D.FD)(Je,{children:[(0,D.Y)(De.lR,{htmlFor:"server_port",required:!0,children:(0,d.t)("SSH Port")}),(0,D.Y)(Ne.pd,{name:"server_port",placeholder:(0,d.t)("22"),type:"number",value:null==e||null==(l=e.ssh_tunnel)?void 0:l.server_port,onChange:a})]})})]}),(0,D.Y)(Qe,{gutter:16,children:(0,D.Y)(m.fv,{xs:24,children:(0,D.FD)(Je,{children:[(0,D.Y)(De.lR,{htmlFor:"username",required:!0,children:(0,d.t)("Username")}),(0,D.Y)(Ne.pd,{name:"username",type:"text",placeholder:(0,d.t)("e.g. Analytics"),value:(null==e||null==(r=e.ssh_tunnel)?void 0:r.username)||"",onChange:a})]})})}),(0,D.Y)(Qe,{gutter:16,children:(0,D.Y)(m.fv,{xs:24,children:(0,D.FD)(Je,{children:[(0,D.Y)(De.lR,{htmlFor:"use_password",required:!0,children:(0,d.t)("Login with")}),(0,D.Y)(Ge,{name:"use_password",initialValue:h,children:(0,D.FD)(Ve.s.Group,{onChange:({target:{value:e}})=>{p(e),t(e)},children:[(0,D.Y)(Ve.s,{value:oa.Password,children:(0,d.t)("Password")}),(0,D.Y)(Ve.s,{value:oa.PrivateKey,children:(0,d.t)("Private Key & Password")})]})})]})})}),h===oa.Password&&(0,D.Y)(Qe,{gutter:16,children:(0,D.Y)(m.fv,{xs:24,children:(0,D.FD)(Je,{children:[(0,D.Y)(De.lR,{htmlFor:"password",required:!0,children:(0,d.t)("SSH Password")}),(0,D.Y)(Xe,{name:"password",placeholder:(0,d.t)("e.g. ********"),value:(null==e||null==(i=e.ssh_tunnel)?void 0:i.password)||"",onChange:a,iconRender:e=>e?(0,D.Y)(Ke.A,{title:"Hide password.",children:(0,D.Y)(f.A.EyeInvisibleOutlined,{})}):(0,D.Y)(Ke.A,{title:"Show password.",children:(0,D.Y)(f.A.EyeOutlined,{})}),role:"textbox"})]})})}),h===oa.PrivateKey&&(0,D.FD)(D.FK,{children:[(0,D.Y)(Qe,{gutter:16,children:(0,D.Y)(m.fv,{xs:24,children:(0,D.FD)(Je,{children:[(0,D.Y)(De.lR,{htmlFor:"private_key",required:!0,children:(0,d.t)("Private Key")}),(0,D.Y)(Ne.fs,{name:"private_key",placeholder:(0,d.t)("Paste Private Key here"),value:(null==e||null==(o=e.ssh_tunnel)?void 0:o.private_key)||"",onChange:a,rows:4})]})})}),(0,D.Y)(Qe,{gutter:16,children:(0,D.Y)(m.fv,{xs:24,children:(0,D.FD)(Je,{children:[(0,D.Y)(De.lR,{htmlFor:"private_key_password",required:!0,children:(0,d.t)("Private Key Password")}),(0,D.Y)(Xe,{name:"private_key_password",placeholder:(0,d.t)("e.g. ********"),value:(null==e||null==(s=e.ssh_tunnel)?void 0:s.private_key_password)||"",onChange:a,iconRender:e=>e?(0,D.Y)(Ke.A,{title:"Hide password.",children:(0,D.Y)(f.A.EyeInvisibleOutlined,{})}):(0,D.Y)(Ke.A,{title:"Show password.",children:(0,D.Y)(f.A.EyeOutlined,{})}),role:"textbox"})]})})})]})]})},ea=(0,o.a)(),aa=JSON.stringify({allows_virtual_table_explore:!0}),ta={[T.GSheet]:{message:"Why do I need to create a database?",description:"To begin using your Google Sheets, you need to create a database first. Databases are used as a way to identify your data so that it can be queried and visualized. This database will hold all of your individual Google Sheets you choose to connect here."}},na=(0,s.I4)(u.Ay)`
  .ant-tabs-content {
    display: flex;
    width: 100%;
    overflow: inherit;

    & > .ant-tabs-tabpane {
      position: relative;
    }
  }
`,la=s.I4.div`
  ${({theme:e})=>`\n    margin: ${8*e.gridUnit}px ${4*e.gridUnit}px;\n  `};
`,ra=s.I4.div`
  ${({theme:e})=>`\n    padding: 0px ${4*e.gridUnit}px;\n  `};
`;var ia,oa;!function(e){e[e.AddTableCatalogSheet=0]="AddTableCatalogSheet",e[e.ConfigMethodChange=1]="ConfigMethodChange",e[e.DbSelected=2]="DbSelected",e[e.EditorChange=3]="EditorChange",e[e.ExtraEditorChange=4]="ExtraEditorChange",e[e.ExtraInputChange=5]="ExtraInputChange",e[e.EncryptedExtraInputChange=6]="EncryptedExtraInputChange",e[e.Fetched=7]="Fetched",e[e.InputChange=8]="InputChange",e[e.ParametersChange=9]="ParametersChange",e[e.QueryChange=10]="QueryChange",e[e.RemoveTableCatalogSheet=11]="RemoveTableCatalogSheet",e[e.Reset=12]="Reset",e[e.TextChange=13]="TextChange",e[e.ParametersSSHTunnelChange=14]="ParametersSSHTunnelChange",e[e.SetSSHTunnelLoginMethod=15]="SetSSHTunnelLoginMethod",e[e.RemoveSSHTunnelConfig=16]="RemoveSSHTunnelConfig"}(ia||(ia={})),function(e){e[e.Password=0]="Password",e[e.PrivateKey=1]="PrivateKey"}(oa||(oa={}));const sa=s.I4.div`
  margin-bottom: ${({theme:e})=>3*e.gridUnit}px;
  margin-left: ${({theme:e})=>3*e.gridUnit}px;
`;function da(e,a){var t,n,r,i;const o={...e||{}};let s,d,c={},h="";const p=JSON.parse(o.extra||"{}");switch(a.type){case ia.ExtraEditorChange:try{d=JSON.parse(a.payload.json||"{}")}catch(e){d=a.payload.json}return{...o,extra:JSON.stringify({...p,[a.payload.name]:d})};case ia.EncryptedExtraInputChange:return{...o,masked_encrypted_extra:JSON.stringify({...JSON.parse(o.masked_encrypted_extra||"{}"),[a.payload.name]:a.payload.value})};case ia.ExtraInputChange:return"schema_cache_timeout"===a.payload.name||"table_cache_timeout"===a.payload.name?{...o,extra:JSON.stringify({...p,metadata_cache_timeout:{...null==p?void 0:p.metadata_cache_timeout,[a.payload.name]:a.payload.value}})}:"schemas_allowed_for_file_upload"===a.payload.name?{...o,extra:JSON.stringify({...p,schemas_allowed_for_file_upload:(a.payload.value||"").split(",").filter((e=>""!==e))})}:"http_path"===a.payload.name?{...o,extra:JSON.stringify({...p,engine_params:{connect_args:{[a.payload.name]:null==(u=a.payload.value)?void 0:u.trim()}}})}:"expand_rows"===a.payload.name?{...o,extra:JSON.stringify({...p,schema_options:{...null==p?void 0:p.schema_options,[a.payload.name]:!!a.payload.value}})}:{...o,extra:JSON.stringify({...p,[a.payload.name]:"checkbox"===a.payload.type?a.payload.checked:a.payload.value})};var u;case ia.InputChange:return"checkbox"===a.payload.type?{...o,[a.payload.name]:a.payload.checked}:{...o,[a.payload.name]:a.payload.value};case ia.ParametersChange:if(null!=(t=a.payload.type)&&t.startsWith("catalog")&&void 0!==o.catalog){var m;const e=[...o.catalog],t=null==(m=a.payload.type)?void 0:m.split("-")[1],n=e[parseInt(t,10)]||{};return void 0!==a.payload.value&&(n[a.payload.name]=a.payload.value),e.splice(parseInt(t,10),1,n),s=e.reduce(((e,a)=>{const t={...e};return t[a.name]=a.value,t}),{}),{...o,catalog:e,parameters:{...o.parameters,catalog:s}}}return{...o,parameters:{...o.parameters,[a.payload.name]:a.payload.value}};case ia.ParametersSSHTunnelChange:return{...o,ssh_tunnel:{...o.ssh_tunnel,[a.payload.name]:a.payload.value}};case ia.SetSSHTunnelLoginMethod:{let e={};var g,b,v;return null!=o&&o.ssh_tunnel&&(e=l()(o.ssh_tunnel,["id","server_address","server_port","username"])),a.payload.login_method===oa.PrivateKey?{...o,ssh_tunnel:{private_key:null==o||null==(g=o.ssh_tunnel)?void 0:g.private_key,private_key_password:null==o||null==(b=o.ssh_tunnel)?void 0:b.private_key_password,...e}}:a.payload.login_method===oa.Password?{...o,ssh_tunnel:{password:null==o||null==(v=o.ssh_tunnel)?void 0:v.password,...e}}:{...o}}case ia.RemoveSSHTunnelConfig:return{...o,ssh_tunnel:void 0};case ia.AddTableCatalogSheet:return void 0!==o.catalog?{...o,catalog:[...o.catalog,{name:"",value:""}]}:{...o,catalog:[{name:"",value:""}]};case ia.RemoveTableCatalogSheet:return null==(n=o.catalog)||n.splice(a.payload.indexToDelete,1),{...o};case ia.EditorChange:return{...o,[a.payload.name]:a.payload.json};case ia.QueryChange:return{...o,parameters:{...o.parameters,query:Object.fromEntries(new URLSearchParams(a.payload.value))},query_input:a.payload.value};case ia.TextChange:return{...o,[a.payload.name]:a.payload.value};case ia.Fetched:if(c=(null==(r=a.payload)||null==(i=r.parameters)?void 0:i.query)||{},h=Object.entries(c).map((([e,a])=>`${e}=${a}`)).join("&"),a.payload.masked_encrypted_extra&&a.payload.configuration_method===I.DynamicForm){var f;const e=null==(f={...JSON.parse(a.payload.extra||"{}")}.engine_params)?void 0:f.catalog,t=Object.entries(e||{}).map((([e,a])=>({name:e,value:a})));return{...a.payload,engine:a.payload.backend||o.engine,configuration_method:a.payload.configuration_method,catalog:t,parameters:{...a.payload.parameters||o.parameters,catalog:e},query_input:h}}return{...a.payload,masked_encrypted_extra:a.payload.masked_encrypted_extra||"",engine:a.payload.backend||o.engine,configuration_method:a.payload.configuration_method,parameters:a.payload.parameters||o.parameters,ssh_tunnel:a.payload.ssh_tunnel||o.ssh_tunnel,query_input:h};case ia.DbSelected:return{...a.payload,extra:aa,expose_in_sqllab:!0};case ia.ConfigMethodChange:return{...a.payload};case ia.Reset:default:return null}}const ca=(0,P.Ay)((({addDangerToast:e,addSuccessToast:a,onDatabaseAdd:t,onHide:n,show:l,databaseId:r,dbEngine:o})=>{var s,f,y,_;const[x,Y]=(0,c.useReducer)(da,null),{state:{loading:w,resource:C,error:S},fetchResource:A,createResource:F,updateResource:N,clearError:E}=(0,M.fn)("database",(0,d.t)("database"),e,"connection"),[$,P]=(0,c.useState)("1"),[z,B]=(0,M.d5)(),[V,W,K]=(0,M.Y8)(),[J,Q]=(0,c.useState)(!1),[G,ae]=(0,c.useState)(!1),[se,de]=(0,c.useState)(""),[ce,he]=(0,c.useState)(!1),[be,ve]=(0,c.useState)(!1),[fe,Ye]=(0,c.useState)(!1),[Se,De]=(0,c.useState)({}),[Fe,Ne]=(0,c.useState)({}),[Ee,$e]=(0,c.useState)({}),[ke,Ie]=(0,c.useState)({}),[Te,Ue]=(0,c.useState)(!1),[Pe,Le]=(0,c.useState)([]),[Oe,Me]=(0,c.useState)(!1),[He,ze]=(0,c.useState)(),[Ve,We]=(0,c.useState)([]),[Ke,Je]=(0,c.useState)([]),[Qe,Ge]=(0,c.useState)([]),[Xe,aa]=(0,c.useState)([]),[oa,ca]=(0,c.useState)({}),ha=null!=(s=ea.get("ssh_tunnel.form.switch"))?s:qe,[pa,ua]=(0,c.useState)(void 0);let ma=ea.get("databaseconnection.extraOption");ma&&(ma={...ma,onEdit:e=>{ca({...oa,...e})}});const ga=(0,R.B)(),ba=(0,M.g9)(),va=(0,M.Fp)(),fa=!!r,ya=va||!(null==x||!x.engine||!ta[x.engine]),_a=(null==x?void 0:x.configuration_method)===I.SqlalchemyUri,xa=fa||_a,Ya=V||S,wa=(0,h.W6)(),Ca=(null==z||null==(f=z.databases)?void 0:f.find((e=>e.engine===(fa?null==x?void 0:x.backend:null==x?void 0:x.engine)&&e.default_driver===(null==x?void 0:x.driver))))||(null==z||null==(y=z.databases)?void 0:y.find((e=>e.engine===(fa?null==x?void 0:x.backend:null==x?void 0:x.engine))))||{},Sa=e=>{if("database"===e)return(0,d.t)("e.g. world_population")},Aa=(0,c.useCallback)(((e,a)=>{Y({type:e,payload:a})}),[]),Da=(0,c.useCallback)((()=>{K(null)}),[K]),Fa=(0,c.useCallback)((({target:e})=>{Aa(ia.ParametersChange,{type:e.type,name:e.name,checked:e.checked,value:e.value})}),[Aa]),Na=()=>{Y({type:ia.Reset}),Q(!1),Da(),E(),he(!1),Le([]),Me(!1),ze(""),We([]),Je([]),Ge([]),aa([]),De({}),Ne({}),$e({}),Ie({}),Ue(!1),ua(void 0),n()},Ea=e=>{wa.push(e)},{state:{alreadyExists:$a,passwordsNeeded:ka,sshPasswordNeeded:Ia,sshPrivateKeyNeeded:Ta,sshPrivateKeyPasswordNeeded:Ua,loading:Pa,failed:qa},importResource:La}=(0,M.bN)("database",(0,d.t)("database"),(e=>{ze(e)})),Oa=async()=>{var n,l;let r;if(ve(!0),null==(n=ma)||n.onSave(oa,x).then((({error:a})=>{a&&(r=a,e(a))})),r)return void ve(!1);const o={...x||{}};if(o.configuration_method===I.DynamicForm){var s,c;null!=o&&null!=(s=o.parameters)&&s.catalog&&(o.extra=JSON.stringify({...JSON.parse(o.extra||"{}"),engine_params:{catalog:o.parameters.catalog}}));const a=await W(o,!0);if(!i()(V)||null!=a&&a.length)return e((0,d.t)("Connection failed, please check your connection settings.")),void ve(!1);const t=fa?null==(c=o.parameters_schema)?void 0:c.properties:null==Ca?void 0:Ca.parameters.properties,n=JSON.parse(o.masked_encrypted_extra||"{}");Object.keys(t||{}).forEach((e=>{var a,l,r,i;t[e]["x-encrypted-extra"]&&null!=(a=o.parameters)&&a[e]&&("object"==typeof(null==(l=o.parameters)?void 0:l[e])?(n[e]=null==(r=o.parameters)?void 0:r[e],o.parameters[e]=JSON.stringify(o.parameters[e])):n[e]=JSON.parse((null==(i=o.parameters)?void 0:i[e])||"{}"))})),o.masked_encrypted_extra=JSON.stringify(n),o.engine===T.GSheet&&(o.impersonate_user=!0)}if(null!=o&&null!=(l=o.parameters)&&l.catalog&&(o.extra=JSON.stringify({...JSON.parse(o.extra||"{}"),engine_params:{catalog:o.parameters.catalog}})),!1===pa&&(o.ssh_tunnel=null),null!=x&&x.id){if(await N(x.id,o,o.configuration_method===I.DynamicForm)){var h;if(t&&t(),null==(h=ma)||h.onSave(oa,x).then((({error:a})=>{a&&(r=a,e(a))})),r)return void ve(!1);ce||(Na(),a((0,d.t)("Database settings updated")))}}else if(x){if(await F(o,o.configuration_method===I.DynamicForm)){var p;if(Q(!0),t&&t(),null==(p=ma)||p.onSave(oa,x).then((({error:a})=>{a&&(r=a,e(a))})),r)return void ve(!1);xa&&(Na(),a((0,d.t)("Database connected")))}}else{if(Me(!0),!(Pe[0].originFileObj instanceof File))return;await La(Pe[0].originFileObj,Se,Fe,Ee,ke,Te)&&(t&&t(),Na(),a((0,d.t)("Database connected")))}ae(!0),he(!1),ve(!1)},Ma=e=>{if("Other"===e)Y({type:ia.DbSelected,payload:{database_name:e,configuration_method:I.SqlalchemyUri,engine:void 0,engine_information:{supports_file_upload:!0}}});else{const a=null==z?void 0:z.databases.filter((a=>a.name===e))[0],{engine:t,parameters:n,engine_information:l,default_driver:r,sqlalchemy_uri_placeholder:i}=a,o=void 0!==n;Y({type:ia.DbSelected,payload:{database_name:e,engine:t,configuration_method:o?I.DynamicForm:I.SqlalchemyUri,engine_information:l,driver:r,sqlalchemy_uri_placeholder:i}}),t===T.GSheet&&Y({type:ia.AddTableCatalogSheet})}},Ra=()=>{C&&A(C.id),ae(!1),he(!0)},Ha=()=>{ce&&Q(!1),Oe&&Me(!1),qa&&(Me(!1),ze(""),We([]),Je([]),Ge([]),aa([]),De({}),Ne({}),$e({}),Ie({})),Y({type:ia.Reset}),Le([])},ja=()=>x?!J||ce?(0,D.FD)(D.FK,{children:[(0,D.Y)(_e,{onClick:Ha,children:(0,d.t)("Back")},"back"),(0,D.Y)(_e,{buttonStyle:"primary",onClick:Oa,loading:be,children:(0,d.t)("Connect")},"submit")]}):(0,D.FD)(D.FK,{children:[(0,D.Y)(_e,{onClick:Ra,children:(0,d.t)("Back")},"back"),(0,D.Y)(_e,{buttonStyle:"primary",onClick:Oa,loading:be,children:(0,d.t)("Finish")},"submit")]}):Oe?(0,D.FD)(D.FK,{children:[(0,D.Y)(_e,{onClick:Ha,children:(0,d.t)("Back")},"back"),(0,D.Y)(_e,{buttonStyle:"primary",onClick:Oa,disabled:!!(Pa||$a.length&&!Te||ka.length&&"{}"===JSON.stringify(Se)||Ia.length&&"{}"===JSON.stringify(Fe)||Ta.length&&"{}"===JSON.stringify(Ee)||Ua.length&&"{}"===JSON.stringify(ke)),loading:be,children:(0,d.t)("Connect")},"submit")]}):(0,D.Y)(D.FK,{}),za=(0,c.useRef)(!0);(0,c.useEffect)((()=>{za.current?za.current=!1:Pa||$a.length||ka.length||Ia.length||Ta.length||Ua.length||be||qa||(Na(),a((0,d.t)("Database connected")))}),[$a,ka,Pa,qa,Ia,Ta,Ua]),(0,c.useEffect)((()=>{l&&(P("1"),ve(!0),B()),r&&l&&fa&&r&&(w||A(r).catch((a=>e((0,d.t)("Sorry there was an error fetching database information: %s",a.message)))))}),[l,r]),(0,c.useEffect)((()=>{C&&(Y({type:ia.Fetched,payload:C}),de(C.database_name))}),[C]),(0,c.useEffect)((()=>{be&&ve(!1),z&&o&&Ma(o)}),[z]),(0,c.useEffect)((()=>{var e;Oe&&(null==(e=document)||e.getElementsByClassName("ant-upload-list-item-name")[0].scrollIntoView())}),[Oe]),(0,c.useEffect)((()=>{We([...ka])}),[ka]),(0,c.useEffect)((()=>{Je([...Ia])}),[Ia]),(0,c.useEffect)((()=>{Ge([...Ta])}),[Ta]),(0,c.useEffect)((()=>{aa([...Ua])}),[Ua]),(0,c.useEffect)((()=>{var e;void 0!==(null==x||null==(e=x.parameters)?void 0:e.ssh)&&ua(x.parameters.ssh)}),[null==x||null==(_=x.parameters)?void 0:_.ssh]);const Ba=()=>He?(0,D.Y)(re,{children:(0,D.Y)(O.A,{errorMessage:He,showDbInstallInstructions:Ve.length>0})}):null,Va=e=>{var a,t;const n=null!=(a=null==(t=e.currentTarget)?void 0:t.value)?a:"";Ue(n.toUpperCase()===(0,d.t)("OVERWRITE"))},Wa=()=>{let e=[];var a;return i()(S)?i()(V)||"GENERIC_DB_ENGINE_ERROR"!==(null==V?void 0:V.error_type)||(e=[(null==V?void 0:V.description)||(null==V?void 0:V.message)]):e="object"==typeof S?Object.values(S):"string"==typeof S?[S]:[],e.length?(0,D.Y)(la,{children:(0,D.Y)(L.A,{title:(0,d.t)("Database Creation Error"),description:(0,d.t)('We are unable to connect to your database. Click "See more" for database-provided information that may help troubleshoot the issue.'),descriptionDetails:(null==(a=e)?void 0:a[0])||(null==V?void 0:V.description)})}):(0,D.Y)(D.FK,{})},Ka=()=>{ve(!0),A(null==C?void 0:C.id).then((e=>{(0,p.SO)(p.Hh.Database,e)}))},Ja=()=>(0,D.Y)(Ze,{db:x,onSSHTunnelParametersChange:({target:e})=>{Aa(ia.ParametersSSHTunnelChange,{type:e.type,name:e.name,value:e.value}),Da()},setSSHTunnelLoginMethod:e=>Y({type:ia.SetSSHTunnelLoginMethod,payload:{login_method:e}})}),Qa=()=>(0,D.FD)(D.FK,{children:[(0,D.Y)(Re,{isEditMode:fa,db:x,sslForced:!1,dbModel:Ca,onAddTableCatalog:()=>{Y({type:ia.AddTableCatalogSheet})},onQueryChange:({target:e})=>Aa(ia.QueryChange,{name:e.name,value:e.value}),onExtraInputChange:({target:e})=>Aa(ia.ExtraInputChange,{name:e.name,value:e.value}),onEncryptedExtraInputChange:({target:e})=>Aa(ia.EncryptedExtraInputChange,{name:e.name,value:e.value}),onRemoveTableCatalog:e=>{Y({type:ia.RemoveTableCatalogSheet,payload:{indexToDelete:e}})},onParametersChange:Fa,onChange:({target:e})=>Aa(ia.TextChange,{name:e.name,value:e.value}),getValidation:()=>W(x),validationErrors:V,getPlaceholder:Sa,clearValidationErrors:Da}),pa&&(0,D.Y)(ra,{children:Ja()})]});if(Pe.length>0&&($a.length||Ve.length||Ke.length||Qe.length||Xe.length))return(0,D.FD)(b.Ay,{centered:!0,css:e=>[Z,ne(e),ie(e),oe(e)],footer:ja(),maskClosable:!1,name:"database",onHide:Na,onHandledPrimaryAction:Oa,primaryButtonName:(0,d.t)("Connect"),show:l,title:(0,D.Y)("h4",{children:(0,d.t)("Connect a database")}),width:"500px",children:[(0,D.Y)(Be,{db:x,dbName:se,dbModel:Ca,fileList:Pe,hasConnectedDb:J,isEditMode:fa,isLoading:be,useSqlAlchemyForm:_a}),$a.length?(0,D.FD)(D.FK,{children:[(0,D.Y)(re,{children:(0,D.Y)(g.A,{closable:!1,css:e=>(e=>j.AH`
  margin: ${4*e.gridUnit}px 0;

  .antd5-alert-message {
    margin: 0;
  }
`)(e),type:"warning",showIcon:!0,message:"",description:(0,d.t)("You are importing one or more databases that already exist. Overwriting might cause you to lose some of your work. Are you sure you want to overwrite?")})}),(0,D.Y)(q.A,{id:"confirm_overwrite",name:"confirm_overwrite",required:!0,validationMethods:{onBlur:()=>{}},errorMessage:null==V?void 0:V.confirm_overwrite,label:(0,d.t)('Type "%s" to confirm',(0,d.t)("OVERWRITE")),onChange:Va,css:te})]}):null,Ba(),Ve.length||Ke.length||Qe.length||Xe.length?[...new Set([...Ve,...Ke,...Qe,...Xe])].map((e=>(0,D.FD)(D.FK,{children:[(0,D.Y)(re,{children:(0,D.Y)(g.A,{closable:!1,css:e=>le(e),type:"info",showIcon:!0,message:"Database passwords",description:(0,d.t)('The passwords for the databases below are needed in order to import them. Please note that the "Secure Extra" and "Certificate" sections of the database configuration are not present in explore files and should be added manually after the import if they are needed.')})}),(null==Ve?void 0:Ve.indexOf(e))>=0&&(0,D.Y)(q.A,{id:"password_needed",name:"password_needed",required:!0,value:Se[e],onChange:a=>De({...Se,[e]:a.target.value}),validationMethods:{onBlur:()=>{}},errorMessage:null==V?void 0:V.password_needed,label:(0,d.t)("%s PASSWORD",e.slice(10)),css:te}),(null==Ke?void 0:Ke.indexOf(e))>=0&&(0,D.Y)(q.A,{id:"ssh_tunnel_password_needed",name:"ssh_tunnel_password_needed",required:!0,value:Fe[e],onChange:a=>Ne({...Fe,[e]:a.target.value}),validationMethods:{onBlur:()=>{}},errorMessage:null==V?void 0:V.ssh_tunnel_password_needed,label:(0,d.t)("%s SSH TUNNEL PASSWORD",e.slice(10)),css:te}),(null==Qe?void 0:Qe.indexOf(e))>=0&&(0,D.Y)(q.A,{id:"ssh_tunnel_private_key_needed",name:"ssh_tunnel_private_key_needed",required:!0,value:Ee[e],onChange:a=>$e({...Ee,[e]:a.target.value}),validationMethods:{onBlur:()=>{}},errorMessage:null==V?void 0:V.ssh_tunnel_private_key_needed,label:(0,d.t)("%s SSH TUNNEL PRIVATE KEY",e.slice(10)),css:te}),(null==Xe?void 0:Xe.indexOf(e))>=0&&(0,D.Y)(q.A,{id:"ssh_tunnel_private_key_password_needed",name:"ssh_tunnel_private_key_password_needed",required:!0,value:ke[e],onChange:a=>Ie({...ke,[e]:a.target.value}),validationMethods:{onBlur:()=>{}},errorMessage:null==V?void 0:V.ssh_tunnel_private_key_password_needed,label:(0,d.t)("%s SSH TUNNEL PRIVATE KEY PASSWORD",e.slice(10)),css:te})]}))):null]});const Ga=fa?(e=>(0,D.FD)(D.FK,{children:[(0,D.Y)(_e,{onClick:Na,children:(0,d.t)("Close")},"close"),(0,D.Y)(_e,{buttonStyle:"primary",onClick:Oa,disabled:null==e?void 0:e.is_managed_externally,loading:be,tooltip:null!=e&&e.is_managed_externally?(0,d.t)("This database is managed externally, and can't be edited in Superset"):"",children:(0,d.t)("Finish")},"submit")]}))(x):ja();return xa?(0,D.FD)(b.Ay,{css:e=>[X,Z,ne(e),ie(e),oe(e)],name:"database",onHandledPrimaryAction:Oa,onHide:Na,primaryButtonName:fa?(0,d.t)("Save"):(0,d.t)("Connect"),width:"500px",centered:!0,show:l,title:(0,D.Y)("h4",{children:fa?(0,d.t)("Edit database"):(0,d.t)("Connect a database")}),footer:Ga,maskClosable:!1,children:[(0,D.Y)(xe,{children:(0,D.Y)(ge,{children:(0,D.Y)(Be,{isLoading:be,isEditMode:fa,useSqlAlchemyForm:_a,hasConnectedDb:J,db:x,dbName:se,dbModel:Ca})})}),(0,D.FD)(na,{defaultActiveKey:"1",activeKey:$,onTabClick:e=>P(e),animated:{inkBar:!0,tabPane:!0},children:[(0,D.FD)(u.Ay.TabPane,{tab:(0,D.Y)("span",{children:(0,d.t)("Basic")}),children:[_a?(0,D.FD)(pe,{children:[(0,D.FD)(Ae,{db:x,onInputChange:({target:e})=>Aa(ia.InputChange,{type:e.type,name:e.name,checked:e.checked,value:e.value}),conf:ga,testConnection:()=>{var t;if(null==x||!x.sqlalchemy_uri)return void e((0,d.t)("Please enter a SQLAlchemy URI to test"));const n={sqlalchemy_uri:(null==x?void 0:x.sqlalchemy_uri)||"",database_name:(null==x||null==(t=x.database_name)?void 0:t.trim())||void 0,impersonate_user:(null==x?void 0:x.impersonate_user)||void 0,extra:null==x?void 0:x.extra,masked_encrypted_extra:(null==x?void 0:x.masked_encrypted_extra)||"",server_cert:(null==x?void 0:x.server_cert)||void 0,ssh_tunnel:!i()(null==x?void 0:x.ssh_tunnel)&&pa?{...x.ssh_tunnel,server_port:Number(x.ssh_tunnel.server_port)}:void 0};Ye(!0),(0,M.ym)(n,(a=>{Ye(!1),e(a)}),(e=>{Ye(!1),a(e)}))},testInProgress:fe,children:[(0,D.Y)(ha,{dbModel:Ca,db:x,changeMethods:{onParametersChange:Fa},clearValidationErrors:Da}),pa&&Ja()]}),(Za=(null==x?void 0:x.backend)||(null==x?void 0:x.engine),void 0!==(null==z||null==(et=z.databases)||null==(at=et.find((e=>e.backend===Za||e.engine===Za)))?void 0:at.parameters)&&!fa&&(0,D.FD)("div",{css:e=>ee(e),children:[(0,D.Y)(v.A,{buttonStyle:"link",onClick:()=>Y({type:ia.ConfigMethodChange,payload:{database_name:null==x?void 0:x.database_name,configuration_method:I.DynamicForm,engine:null==x?void 0:x.engine}}),css:e=>(e=>j.AH`
  font-weight: ${e.typography.weights.normal};
  text-transform: initial;
  padding: ${8*e.gridUnit}px 0 0;
  margin-left: 0px;
`)(e),children:(0,d.t)("Connect this database using the dynamic form instead")}),(0,D.Y)(U.A,{tooltip:(0,d.t)("Click this link to switch to an alternate form that exposes only the required fields needed to connect this database."),viewBox:"0 -6 24 24"})]}))]}):Qa(),!fa&&(0,D.Y)(re,{children:(0,D.Y)(g.A,{closable:!1,css:e=>le(e),message:(0,d.t)("Additional fields may be required"),showIcon:!0,description:(0,D.FD)(D.FK,{children:[(0,d.t)("Select databases require additional fields to be completed in the Advanced tab to successfully connect the database. Learn what requirements your databases has "),(0,D.Y)("a",{href:je,target:"_blank",rel:"noopener noreferrer",className:"additional-fields-alert-description",children:(0,d.t)("here")}),"."]}),type:"info"})}),Ya&&Wa()]},"1"),(0,D.Y)(u.Ay.TabPane,{tab:(0,D.Y)("span",{children:(0,d.t)("Advanced")}),children:(0,D.Y)(Ce,{extraExtension:ma,db:x,onInputChange:({target:e})=>Aa(ia.InputChange,{type:e.type,name:e.name,checked:e.checked,value:e.value}),onTextChange:({target:e})=>Aa(ia.TextChange,{name:e.name,value:e.value}),onEditorChange:e=>Aa(ia.EditorChange,e),onExtraInputChange:({target:e})=>{Aa(ia.ExtraInputChange,{type:e.type,name:e.name,checked:e.checked,value:e.value})},onExtraEditorChange:e=>{Aa(ia.ExtraEditorChange,e)}})},"2")]})]}):(0,D.FD)(b.Ay,{css:e=>[Z,ne(e),ie(e),oe(e)],name:"database",onHandledPrimaryAction:Oa,onHide:Na,primaryButtonName:J?(0,d.t)("Finish"):(0,d.t)("Connect"),width:"500px",centered:!0,show:l,title:(0,D.Y)("h4",{children:(0,d.t)("Connect a database")}),footer:ja(),maskClosable:!1,children:[!be&&J?(0,D.FD)(D.FK,{children:[(0,D.Y)(Be,{isLoading:be,isEditMode:fa,useSqlAlchemyForm:_a,hasConnectedDb:J,db:x,dbName:se,dbModel:Ca,editNewDb:ce}),G&&(0,D.FD)(sa,{children:[(0,D.Y)(v.A,{buttonStyle:"secondary",onClick:()=>{ve(!0),Ka(),Ea("/dataset/add/")},children:(0,d.t)("CREATE DATASET")}),(0,D.Y)(v.A,{buttonStyle:"secondary",onClick:()=>{ve(!0),Ka(),Ea("/sqllab?db=true")},children:(0,d.t)("QUERY DATA IN SQL LAB")})]}),ce?Qa():(0,D.Y)(Ce,{extraExtension:ma,db:x,onInputChange:({target:e})=>Aa(ia.InputChange,{type:e.type,name:e.name,checked:e.checked,value:e.value}),onTextChange:({target:e})=>Aa(ia.TextChange,{name:e.name,value:e.value}),onEditorChange:e=>Aa(ia.EditorChange,e),onExtraInputChange:({target:e})=>{Aa(ia.ExtraInputChange,{type:e.type,name:e.name,checked:e.checked,value:e.value})},onExtraEditorChange:e=>Aa(ia.ExtraEditorChange,e)})]}):(0,D.Y)(D.FK,{children:!be&&(x?(0,D.FD)(D.FK,{children:[(0,D.Y)(Be,{isLoading:be,isEditMode:fa,useSqlAlchemyForm:_a,hasConnectedDb:J,db:x,dbName:se,dbModel:Ca}),ya&&(()=>{var e,a,t,n,l;const{hostname:r}=window.location;let i=(null==va||null==(e=va.REGIONAL_IPS)?void 0:e.default)||"";const o=(null==va?void 0:va.REGIONAL_IPS)||{};return Object.entries(o).forEach((([e,a])=>{const t=new RegExp(e);r.match(t)&&(i=a)})),(null==x?void 0:x.engine)&&(0,D.Y)(re,{children:(0,D.Y)(g.A,{closable:!1,css:e=>le(e),type:"info",showIcon:!0,message:(null==(a=ta[x.engine])?void 0:a.message)||(null==va||null==(t=va.DEFAULT)?void 0:t.message),description:(null==(n=ta[x.engine])?void 0:n.description)||(null==va||null==(l=va.DEFAULT)?void 0:l.description)+i})})})(),Qa(),(0,D.Y)("div",{css:e=>ee(e),children:Ca.engine!==T.GSheet&&(0,D.FD)(D.FK,{children:[(0,D.Y)(v.A,{buttonStyle:"link",onClick:()=>Y({type:ia.ConfigMethodChange,payload:{engine:x.engine,configuration_method:I.SqlalchemyUri,database_name:x.database_name}}),css:ue,children:(0,d.t)("Connect this database with a SQLAlchemy URI string instead")}),(0,D.Y)(U.A,{tooltip:(0,d.t)("Click this link to switch to an alternate form that allows you to input the SQLAlchemy URL for this database manually."),viewBox:"0 -6 24 24"})]})}),Ya&&Wa()]}):(0,D.FD)(ye,{children:[(0,D.Y)(Be,{isLoading:be,isEditMode:fa,useSqlAlchemyForm:_a,hasConnectedDb:J,db:x,dbName:se,dbModel:Ca}),(0,D.Y)("div",{className:"preferred",children:null==z||null==(Xa=z.databases)?void 0:Xa.filter((e=>e.preferred)).map((e=>(0,D.Y)(k,{className:"preferred-item",onClick:()=>Ma(e.name),buttonText:e.name,icon:null==ba?void 0:ba[e.engine]},`${e.name}`)))}),(()=>{var e,a;return(0,D.FD)("div",{className:"available",children:[(0,D.Y)("h4",{className:"available-label",children:(0,d.t)("Or choose from a list of other databases we support:")}),(0,D.Y)("div",{className:"control-label",children:(0,d.t)("Supported databases")}),(0,D.FD)(m._P,{className:"available-select",onChange:Ma,placeholder:(0,d.t)("Choose a database..."),showSearch:!0,children:[null==(e=[...(null==z?void 0:z.databases)||[]])?void 0:e.sort(((e,a)=>e.name.localeCompare(a.name))).map(((e,a)=>(0,D.Y)(m._P.Option,{value:e.name,children:e.name},`database-${a}`))),(0,D.Y)(m._P.Option,{value:"Other",children:(0,d.t)("Other")},"Other")]}),(0,D.Y)(g.A,{showIcon:!0,closable:!1,css:e=>le(e),type:"info",message:(null==va||null==(a=va.ADD_DATABASE)?void 0:a.message)||(0,d.t)("Want to add a new database?"),description:null!=va&&va.ADD_DATABASE?(0,D.FD)(D.FK,{children:[(0,d.t)("Any databases that allow connections via SQL Alchemy URIs can be added. "),(0,D.Y)("a",{href:null==va?void 0:va.ADD_DATABASE.contact_link,target:"_blank",rel:"noopener noreferrer",children:null==va?void 0:va.ADD_DATABASE.contact_description_link})," ",null==va?void 0:va.ADD_DATABASE.description]}):(0,D.FD)(D.FK,{children:[(0,d.t)("Any databases that allow connections via SQL Alchemy URIs can be added. Learn about how to connect a database driver "),(0,D.Y)("a",{href:je,target:"_blank",rel:"noopener noreferrer",children:(0,d.t)("here")}),"."]})})]})})(),(0,D.Y)(we,{children:(0,D.Y)(m._O,{name:"databaseFile",id:"databaseFile",accept:".yaml,.json,.yml,.zip",customRequest:()=>{},onChange:async e=>{ze(""),We([]),Je([]),Ge([]),aa([]),De({}),Ne({}),$e({}),Ie({}),Me(!0),Le([{...e.file,status:"done"}]),e.file.originFileObj instanceof File&&await La(e.file.originFileObj,Se,Fe,Ee,ke,Te)&&(null==t||t())},onRemove:e=>(Le(Pe.filter((a=>a.uid!==e.uid))),!1),children:(0,D.Y)(v.A,{buttonStyle:"link",type:"link",css:me,children:(0,d.t)("Import database from file")})})}),Ba()]}))}),be&&(0,D.Y)(H.A,{})]});var Xa,Za,et,at}))},19980:(e,a,t)=>{t.d(a,{A:()=>H});var n=t(96540),l=t(35742),r=t(51436),i=t(95579),o=t(85861),s=t(46920),d=t(75488),c=t(61693),h=t(15595),p=t(77028),u=t(90868),m=t(58561),g=t.n(m),b=t(5261),v=t(40563),f=t(96453),y=t(17437);const _=(0,f.I4)(v.eI)`
  ${({theme:e})=>y.AH`
    flex: 1;
    margin-top: 0;
    margin-bottom: ${2.5*e.gridUnit}px;
  }
  `}
`,x=f.I4.div`
  display: flex;
  align-items: center;
  margin-top: 0;
`,Y=y.AH`
  .antd5-modal-body {
    padding-left: 0;
    padding-right: 0;
    padding-top: 0;
  }
`,w=e=>y.AH`
  .switch-label {
    color: ${e.colors.grayscale.base};
    margin-left: ${4*e.gridUnit}px;
  }
`,C=e=>y.AH`
  .antd5-modal-header {
    padding: ${4.5*e.gridUnit}px ${4*e.gridUnit}px
      ${4*e.gridUnit}px;
  }

  .antd5-modal-close-x .close {
    opacity: 1;
  }

  .antd5-modal-body {
    height: ${180.5*e.gridUnit}px;
  }

  .antd5-modal-footer {
    height: ${16.25*e.gridUnit}px;
  }

  .info-solid-small {
    vertical-align: bottom;
  }
`;var S=t(46740),A=t(2445);const D=f.I4.div`
  //margin-top: 10px;
  //margin-bottom: 10px;
`,F=({columns:e,maxColumnsToShow:a=4})=>{const t=e.map((e=>({name:e})));return(0,A.FD)(D,{children:[(0,A.Y)(h.o5.Text,{type:"secondary",children:"Columns:"}),0===e.length?(0,A.Y)("p",{className:"help-block",children:(0,i.t)("Upload file to preview columns")}):(0,A.Y)(S.A,{tags:t,maxTags:a})]})};var N=t(31641);const E=({label:e,tip:a,children:t,name:n,rules:l})=>(0,A.Y)(_,{label:(0,A.FD)("div",{children:[e,(0,A.Y)(N.A,{tooltip:a})]}),name:n,rules:l,children:t}),$=["delimiter","skip_initial_space","skip_blank_lines","day_first","column_data_types","column_dates","decimal_character","null_values","index_column","header_row","rows_to_read","skip_rows"],k=["sheet_name","column_dates","decimal_character","null_values","index_column","header_row","rows_to_read","skip_rows"],I=[],T=["rows_to_read","index_column"],U=[...$,...k,...I],P={csv:$,excel:k,columnar:I},q=(e,a)=>P[a].includes(e),L={table_name:"",schema:"",sheet_name:void 0,delimiter:",",already_exists:"fail",skip_initial_space:!1,skip_blank_lines:!1,day_first:!1,decimal_character:".",null_values:[],header_row:"0",rows_to_read:null,skip_rows:"0",column_dates:[],index_column:null,dataframe_index:!1,index_label:"",columns_read:[],column_data_types:""},O={csv:".csv, .tsv",excel:".xls, .xlsx",columnar:".parquet, .zip"},M={csv:"CSV",excel:"Excel",columnar:"Columnar"},R=({label:e,dataTest:a,children:t,...n})=>(0,A.FD)(x,{children:[(0,A.Y)(d.d,{...n}),(0,A.Y)("div",{className:"switch-label",children:e}),t]}),H=(0,b.Ay)((({addDangerToast:e,addSuccessToast:a,onHide:t,show:d,allowedExtensions:m,type:b="csv"})=>{const[v]=h.Wq.useForm(),[f,x]=(0,n.useState)(0),[S,D]=(0,n.useState)([]),[N,$]=(0,n.useState)([]),[k,I]=(0,n.useState)([]),[H,j]=(0,n.useState)({}),[z,B]=(0,n.useState)(","),[V,W]=(0,n.useState)(!1),[K,J]=(0,n.useState)(),[Q,G]=(0,n.useState)(!1),[X,Z]=(0,n.useState)(!0),[ee,ae]=(0,n.useState)(!1),te=(0,n.useMemo)((()=>(e="",a,t)=>{const n=g().encode_uri({filters:[{col:"allow_file_upload",opr:"eq",value:!0}],page:a,page_size:t});return l.A.get({endpoint:`/api/v1/database/?q=${n}`}).then((e=>({data:e.json.result.map((e=>({value:e.id,label:e.database_name}))),totalCount:e.json.count})))}),[]),ne=(0,n.useMemo)((()=>(e="",a,t)=>f?l.A.get({endpoint:`/api/v1/database/${f}/schemas/`}).then((e=>({data:e.json.result.map((e=>({value:e,label:e}))),totalCount:e.json.count}))):Promise.resolve({data:[],totalCount:0})),[f]),le=a=>{const t=v.getFieldsValue(),n={...L,...t},i=new FormData;return i.append("file",a),"csv"===b&&i.append("delimiter",n.delimiter),i.append("type",b),ae(!0),l.A.post({endpoint:"/api/v1/database/upload_metadata/",body:i,headers:{Accept:"application/json"}}).then((e=>{const{items:a}=e.json.result;if(a&&"excel"!==b)$(a[0].column_names);else{const{allSheetNames:e,sheetColumnNamesMap:t}=a.reduce(((e,a)=>(e.allSheetNames.push(a.sheet_name),e.sheetColumnNamesMap[a.sheet_name]=a.column_names,e)),{allSheetNames:[],sheetColumnNamesMap:{}});$(a[0].column_names),I(e),v.setFieldsValue({sheet_name:e[0]}),j(t)}})).catch((a=>(0,r.h4)(a).then((a=>{e(a.error||"Error"),$([]),v.setFieldsValue({sheet_name:void 0}),I([])})))).finally((()=>{ae(!1)}))},re=()=>{D([]),$([]),J(""),x(0),I([]),W(!1),B(","),Z(!0),ae(!1),j({}),v.resetFields(),t()},ie=()=>N.map((e=>({value:e,label:e})));(0,n.useEffect)((()=>{if(N.length>0&&S[0].originFileObj&&S[0].originFileObj instanceof File){if(!X)return;le(S[0].originFileObj).then((e=>e))}}),[z]);const oe={csv:(0,i.t)("CSV upload"),excel:(0,i.t)("Excel upload"),columnar:(0,i.t)("Columnar upload")};return(0,A.Y)(o.Ay,{css:e=>[Y,C(e),w(e)],primaryButtonLoading:V,name:"database",onHandledPrimaryAction:v.submit,onHide:re,width:"500px",primaryButtonName:"Upload",centered:!0,show:d,title:(0,A.Y)((()=>{const e=oe[b]||(0,i.t)("Upload");return(0,A.Y)("h4",{children:e})}),{}),children:(0,A.Y)(h.Wq,{form:v,onFinish:()=>{var t;const n=v.getFieldsValue();delete n.database,n.schema=K;const o={...L,...n},s=new FormData,d=null==(t=S[0])?void 0:t.originFileObj;d&&s.append("file",d),((e,a)=>{const t=(()=>{const e=P[b]||[];return[...U].filter((a=>!e.includes(a)))})();Object.entries(a).forEach((([a,n])=>{t.includes(a)||T.includes(a)&&null==n||e.append(a,n)}))})(s,o),W(!0);const c=`/api/v1/database/${f}/upload/`;return s.append("type",b),l.A.post({endpoint:c,body:s,headers:{Accept:"application/json"}}).then((()=>{a((0,i.t)("Data imported")),W(!1),re()})).catch((a=>(0,r.h4)(a).then((a=>{e(a.error||"Error")})))).finally((()=>{W(!1)}))},layout:"vertical",initialValues:L,children:(0,A.FD)(c.A,{expandIconPosition:"right",accordion:!0,defaultActiveKey:"general",css:e=>(e=>y.AH`
  .ant-collapse-header {
    padding-top: ${3.5*e.gridUnit}px;
    padding-bottom: ${2.5*e.gridUnit}px;
    .anticon.ant-collapse-arrow {
      top: calc(50% - ${6}px);
    }
    .helper {
      color: ${e.colors.grayscale.base};
      font-size: ${e.typography.sizes.s}px;
    }
  }
  h4 {
    font-size: ${e.typography.sizes.l}px;
    margin-top: 0;
    margin-bottom: ${e.gridUnit}px;
  }
  p.helper {
    margin-bottom: 0;
    padding: 0;
  }
`)(e),children:[(0,A.FD)(c.A.Panel,{header:(0,A.FD)("div",{children:[(0,A.Y)("h4",{children:(0,i.t)("General information")}),(0,A.Y)("p",{className:"helper",children:(0,i.t)("Upload a file to a database.")})]}),children:[(0,A.Y)(h.fI,{children:(0,A.Y)(h.fv,{span:24,children:(0,A.Y)(_,{label:(0,i.t)("%(label)s file",{label:M[b]}),name:"file",required:!0,rules:[{validator:(e,a)=>0===S.length?Promise.reject((0,i.t)("Uploading a file is required")):((e,a)=>{const t=e.name.match(/.+\.([^.]+)$/);if(!t)return!1;const n=t[1].toLowerCase();return a.map((e=>e.toLowerCase())).includes(n)})(S[0],m)?Promise.resolve():Promise.reject((0,i.t)("Upload a file with a valid extension. Valid: [%s]",m.join(",")))}],children:(0,A.Y)(h._O,{name:"modelFile",id:"modelFile",accept:O[b],fileList:S,onChange:async e=>{D([{...e.file,status:"done"}]),X&&await le(e.file.originFileObj)},onRemove:e=>(D(S.filter((a=>a.uid!==e.uid))),$([]),I([]),v.setFieldsValue({sheet_name:void 0}),!1),customRequest:()=>{},children:(0,A.Y)(s.A,{"aria-label":(0,i.t)("Select"),icon:(0,A.Y)(p.A,{}),loading:ee,children:(0,i.t)("Select")})})})})}),(0,A.Y)(h.fI,{children:(0,A.Y)(h.fv,{span:24,children:(0,A.Y)(_,{children:(0,A.Y)(R,{label:(0,i.t)("Preview uploaded file"),dataTest:"previewUploadedFile",onChange:e=>{Z(e)},checked:X})})})}),X&&(0,A.Y)(h.fI,{children:(0,A.Y)(h.fv,{span:24,children:(0,A.Y)(F,{columns:N})})}),(0,A.Y)(h.fI,{children:(0,A.Y)(h.fv,{span:24,children:(0,A.Y)(_,{label:(0,i.t)("Database"),required:!0,name:"database",rules:[{validator:(e,a)=>f?Promise.resolve():Promise.reject((0,i.t)("Selecting a database is required"))}],children:(0,A.Y)(h.DW,{ariaLabel:(0,i.t)("Select a database"),options:te,onChange:e=>{x(null==e?void 0:e.value),J(void 0),v.setFieldsValue({schema:void 0})},allowClear:!0,placeholder:(0,i.t)("Select a database to upload the file to")})})})}),(0,A.Y)(h.fI,{children:(0,A.Y)(h.fv,{span:24,children:(0,A.Y)(_,{label:(0,i.t)("Schema"),name:"schema",children:(0,A.Y)(h.DW,{ariaLabel:(0,i.t)("Select a schema"),options:ne,onChange:e=>{J(null==e?void 0:e.value)},allowClear:!0,placeholder:(0,i.t)("Select a schema if the database supports this")})})})}),(0,A.Y)(h.fI,{children:(0,A.Y)(h.fv,{span:24,children:(0,A.Y)(_,{label:(0,i.t)("Table name"),name:"table_name",required:!0,rules:[{required:!0,message:"Table name is required"}],children:(0,A.Y)(u.pd,{"aria-label":(0,i.t)("Table Name"),name:"table_name",type:"text",placeholder:(0,i.t)("Name of table to be created")})})})}),q("delimiter",b)&&(0,A.Y)(h.fI,{children:(0,A.Y)(h.fv,{span:24,children:(0,A.Y)(E,{label:(0,i.t)("Delimiter"),tip:(0,i.t)("Select a delimiter for this data"),name:"delimiter",children:(0,A.Y)(h.l6,{ariaLabel:(0,i.t)("Choose a delimiter"),options:[{value:",",label:'Comma ","'},{value:";",label:'Semicolon ";"'},{value:"\t",label:'Tab "\\t"'},{value:"|",label:"Pipe"}],onChange:e=>{B(e)},allowNewOptions:!0})})})}),q("sheet_name",b)&&(0,A.Y)(h.fI,{children:(0,A.Y)(h.fv,{span:24,children:(0,A.Y)(_,{label:(0,i.t)("Sheet name"),name:"sheet_name",children:(0,A.Y)(h.l6,{ariaLabel:(0,i.t)("Choose sheet name"),options:k.map((e=>({value:e,label:e}))),onChange:e=>{var a;$(null!=(a=H[e])?a:[])},allowNewOptions:!0,placeholder:(0,i.t)("Select a sheet name from the uploaded file")})})})})]},"general"),(0,A.FD)(c.A.Panel,{header:(0,A.FD)("div",{children:[(0,A.Y)("h4",{children:(0,i.t)("File settings")}),(0,A.Y)("p",{className:"helper",children:(0,i.t)("Adjust how spaces, blank lines, null values are handled and other file wide settings.")})]}),children:[(0,A.Y)(h.fI,{children:(0,A.Y)(h.fv,{span:24,children:(0,A.Y)(E,{label:(0,i.t)("If table already exists"),tip:(0,i.t)("What should happen if the table already exists"),name:"already_exists",children:(0,A.Y)(h.l6,{ariaLabel:(0,i.t)("Choose already exists"),options:[{value:"fail",label:"Fail"},{value:"replace",label:"Replace"},{value:"append",label:"Append"}],onChange:()=>{}})})})}),q("column_dates",b)&&(0,A.Y)(h.fI,{children:(0,A.Y)(h.fv,{span:24,children:(0,A.Y)(_,{label:(0,i.t)("Columns to be parsed as dates"),name:"column_dates",children:(0,A.Y)(h.l6,{ariaLabel:(0,i.t)("Choose columns to be parsed as dates"),mode:"multiple",options:ie(),allowClear:!0,allowNewOptions:!0,placeholder:(0,i.t)("Select column names from a dropdown list that should be parsed as dates.")})})})}),q("decimal_character",b)&&(0,A.Y)(h.fI,{children:(0,A.Y)(h.fv,{span:24,children:(0,A.Y)(E,{label:(0,i.t)("Decimal character"),tip:(0,i.t)("Character to interpret as decimal point"),name:"decimal_character",children:(0,A.Y)(u.pd,{type:"text"})})})}),q("null_values",b)&&(0,A.Y)(h.fI,{children:(0,A.Y)(h.fv,{span:24,children:(0,A.Y)(E,{label:(0,i.t)("Null Values"),tip:(0,i.t)("Choose values that should be treated as null. Warning: Hive database supports only a single value"),name:"null_values",children:(0,A.Y)(h.l6,{mode:"multiple",options:[{value:'""',label:'Empty Strings ""'},{value:"None",label:"None"},{value:"nan",label:"nan"},{value:"null",label:"null"},{value:"N/A",label:"N/A"}],allowClear:!0,allowNewOptions:!0})})})}),q("skip_initial_space",b)&&(0,A.Y)(h.fI,{children:(0,A.Y)(h.fv,{span:24,children:(0,A.Y)(_,{name:"skip_initial_space",children:(0,A.Y)(R,{label:(0,i.t)("Skip spaces after delimiter"),dataTest:"skipInitialSpace"})})})}),q("skip_blank_lines",b)&&(0,A.Y)(h.fI,{children:(0,A.Y)(h.fv,{span:24,children:(0,A.Y)(_,{name:"skip_blank_lines",children:(0,A.Y)(R,{label:(0,i.t)("Skip blank lines rather than interpreting them as Not A Number values"),dataTest:"skipBlankLines"})})})}),q("day_first",b)&&(0,A.Y)(h.fI,{children:(0,A.Y)(h.fv,{span:24,children:(0,A.Y)(_,{name:"day_first",children:(0,A.Y)(R,{label:(0,i.t)("DD/MM format dates, international and European format"),dataTest:"dayFirst"})})})})]},"2"),(0,A.FD)(c.A.Panel,{header:(0,A.FD)("div",{children:[(0,A.Y)("h4",{children:(0,i.t)("Columns")}),(0,A.Y)("p",{className:"helper",children:(0,i.t)("Adjust column settings such as specifying the columns to read, how duplicates are handled, column data types, and more.")})]}),children:[(0,A.Y)(h.fI,{children:(0,A.Y)(h.fv,{span:24,children:(0,A.Y)(_,{label:(0,i.t)("Columns to read"),name:"columns_read",children:(0,A.Y)(h.l6,{ariaLabel:(0,i.t)("Choose columns to read"),mode:"multiple",options:ie(),allowClear:!0,allowNewOptions:!0,placeholder:(0,i.t)("List of the column names that should be read")})})})}),q("column_data_types",b)&&(0,A.Y)(h.fI,{children:(0,A.Y)(h.fv,{span:24,children:(0,A.Y)(E,{label:(0,i.t)("Column data types"),tip:(0,i.t)('A dictionary with column names and their data types if you need to change the defaults. Example: {"user_id":"int"}. Check Python\'s Pandas library for supported data types.'),name:"column_data_types",children:(0,A.Y)(u.pd,{"aria-label":(0,i.t)("Column data types"),type:"text"})})})}),(0,A.Y)(h.fI,{children:(0,A.Y)(h.fv,{span:24,children:(0,A.Y)(_,{name:"dataframe_index",children:(0,A.Y)(R,{label:(0,i.t)("Create dataframe index"),dataTest:"dataFrameIndex",onChange:G})})})}),Q&&q("index_column",b)&&(0,A.Y)(h.fI,{children:(0,A.Y)(h.fv,{span:24,children:(0,A.Y)(E,{label:(0,i.t)("Index column"),tip:(0,i.t)("Column to use as the index of the dataframe. If None is given, Index label is used."),name:"index_column",children:(0,A.Y)(h.l6,{ariaLabel:(0,i.t)("Choose index column"),options:N.map((e=>({value:e,label:e}))),allowClear:!0,allowNewOptions:!0})})})}),Q&&(0,A.Y)(h.fI,{children:(0,A.Y)(h.fv,{span:24,children:(0,A.Y)(E,{label:(0,i.t)("Index label"),tip:(0,i.t)("Label for the index column. Don't use an existing column name."),name:"index_label",children:(0,A.Y)(u.pd,{"aria-label":(0,i.t)("Index label"),type:"text"})})})})]},"3"),q("header_row",b)&&q("rows_to_read",b)&&q("skip_rows",b)&&(0,A.Y)(c.A.Panel,{header:(0,A.FD)("div",{children:[(0,A.Y)("h4",{children:(0,i.t)("Rows")}),(0,A.Y)("p",{className:"helper",children:(0,i.t)("Set header rows and the number of rows to read or skip.")})]}),children:(0,A.FD)(h.fI,{children:[(0,A.Y)(h.fv,{span:8,children:(0,A.Y)(E,{label:(0,i.t)("Header row"),tip:(0,i.t)("Row containing the headers to use as column names (0 is first line of data)."),name:"header_row",rules:[{required:!0,message:"Header row is required"}],children:(0,A.Y)(u.YI,{"aria-label":(0,i.t)("Header row"),type:"text",min:0})})}),(0,A.Y)(h.fv,{span:8,children:(0,A.Y)(E,{label:(0,i.t)("Rows to read"),tip:(0,i.t)("Number of rows of file to read. Leave empty (default) to read all rows"),name:"rows_to_read",children:(0,A.Y)(u.YI,{"aria-label":(0,i.t)("Rows to read"),min:1})})}),(0,A.Y)(h.fv,{span:8,children:(0,A.Y)(E,{label:(0,i.t)("Skip rows"),tip:(0,i.t)("Number of rows to skip at start of file."),name:"skip_rows",rules:[{required:!0,message:"Skip rows is required"}],children:(0,A.Y)(u.YI,{"aria-label":(0,i.t)("Skip rows"),min:0})})})]})},"4")]})})})}))},82741:(e,a,t)=>{t.d(a,{A:()=>se});var n=t(38221),l=t.n(n),r=t(96540),i=t(96453),o=t(32132),s=t(15595),d=t(6749),c=t(19129),h=t(61574),p=t(71519),u=t(78532),m=t(12249),g=t(35837),b=t(27023),v=t(17437),f=t(62193),y=t.n(f),_=t(58156),x=t.n(_),Y=t(58561),w=t.n(Y),C=t(61225),S=t(33231),A=t(72391),D=t(95579),F=t(35742),N=t(35768),E=t(84666),$=t(65256),k=t(76617),I=t(19980),T=t(30703),U=t(2445);const P=({version:e="unknownVersion",sha:a="unknownSHA",build:t="unknownBuild"})=>{const n=`https://apachesuperset.gateway.scarf.sh/pixel/0d3461e1-abb1-4691-a0aa-5ed50de66af0/${e}/${a}/${t}`;return(0,U.Y)("img",{referrerPolicy:"no-referrer-when-downgrade",src:n,width:0,height:0,alt:""})},{SubMenu:q}=d.NG,L=i.I4.div`
  display: flex;
  align-items: center;

  & i {
    margin-right: ${({theme:e})=>2*e.gridUnit}px;
  }

  & a {
    display: block;
    width: 150px;
    word-wrap: break-word;
    text-decoration: none;
  }
`,O=i.I4.i`
  margin-top: 2px;
`;function M(e){const{locale:a,languages:t,...n}=e;return(0,U.Y)(q,{"aria-label":"Languages",title:(0,U.Y)("div",{className:"f16",children:(0,U.Y)(O,{className:`flag ${t[a].flag}`})}),icon:(0,U.Y)(m.A.TriangleDown,{}),...n,children:Object.keys(t).map((e=>(0,U.Y)(d.NG.Item,{style:{whiteSpace:"normal",height:"auto"},children:(0,U.FD)(L,{className:"f16",children:[(0,U.Y)("i",{className:`flag ${t[e].flag}`}),(0,U.Y)("a",{href:t[e].url,children:t[e].name})]})},e)))})}var R=t(3139);const H=(0,A.a)(),j=e=>v.AH`
  padding: ${1.5*e.gridUnit}px ${4*e.gridUnit}px
    ${4*e.gridUnit}px ${7*e.gridUnit}px;
  color: ${e.colors.grayscale.base};
  font-size: ${e.typography.sizes.xs}px;
  white-space: nowrap;
`,z=i.I4.div`
  color: ${({theme:e})=>e.colors.primary.dark1};
`,B=e=>v.AH`
  color: ${e.colors.grayscale.light1};
`,V=i.I4.div`
  display: flex;
  height: 100%;
  flex-direction: row;
  justify-content: ${({align:e})=>e};
  align-items: center;
  margin-right: ${({theme:e})=>e.gridUnit}px;
`,W=i.I4.div`
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
`,K=i.I4.a`
  padding-right: ${({theme:e})=>e.gridUnit}px;
  padding-left: ${({theme:e})=>e.gridUnit}px;
`,J=e=>v.AH`
  color: ${e.colors.grayscale.light5};
`,Q=e=>v.AH`
  &:hover {
    color: ${e.colors.primary.base} !important;
    cursor: pointer !important;
  }
`,{SubMenu:G}=d.W1,X=(0,i.I4)(G)`
  &.antd5-menu-submenu-active {
    .antd5-menu-title-content {
      color: ${({theme:e})=>e.colors.primary.base};
    }
  }
`,Z=({align:e,settings:a,navbarRight:t,isFrontendRoute:n,environmentTag:l,setQuery:o})=>{const s=(0,C.d4)((e=>e.user)),h=(0,C.d4)((e=>{var a;return null==(a=e.dashboardInfo)?void 0:a.id})),u=s||{},{roles:g}=u,{CSV_EXTENSIONS:b,COLUMNAR_EXTENSIONS:f,EXCEL_EXTENSIONS:_,ALLOWED_EXTENSIONS:Y,HAS_GSHEETS_INSTALLED:S}=(0,C.d4)((e=>e.common.conf)),[A,q]=(0,r.useState)(!1),[L,O]=(0,r.useState)(!1),[G,Z]=(0,r.useState)(!1),[ee,ae]=(0,r.useState)(!1),[te,ne]=(0,r.useState)(""),le=(0,E.L)("can_sqllab","Superset",g),re=(0,E.L)("can_write","Dashboard",g),ie=(0,E.L)("can_write","Chart",g),oe=(0,E.L)("can_write","Database",g),se=(0,E.L)("can_write","Dataset",g),{canUploadData:de,canUploadCSV:ce,canUploadColumnar:he,canUploadExcel:pe}=(0,T.c8)(g,b,f,_,Y),ue=le||ie||re,[me,ge]=(0,r.useState)(!1),[be,ve]=(0,r.useState)(!1),fe=(0,$.N6)(s),ye=me||fe,_e=[{label:(0,D.t)("Data"),icon:"fa-database",childs:[{label:(0,D.t)("Connect database"),name:R.$.DbConnection,perm:oe&&!be},{label:(0,D.t)("Create dataset"),name:R.$.DatasetCreation,url:"/dataset/add/",perm:se&&be},{label:(0,D.t)("Connect Google Sheet"),name:R.$.GoogleSheets,perm:oe&&S},{label:(0,D.t)("Upload CSV to database"),name:R.$.CSVUpload,perm:ce&&ye,disable:fe&&!me},{label:(0,D.t)("Upload Excel to database"),name:R.$.ExcelUpload,perm:pe&&ye,disable:fe&&!me},{label:(0,D.t)("Upload Columnar file to database"),name:R.$.ColumnarUpload,perm:he&&ye,disable:fe&&!me}]},{label:(0,D.t)("SQL query"),url:"/sqllab?new=true",icon:"fa-fw fa-search",perm:"can_sqllab",view:"Superset"},{label:(0,D.t)("Chart"),url:Number.isInteger(h)?`/chart/add?dashboard_id=${h}`:"/chart/add",icon:"fa-fw fa-bar-chart",perm:"can_write",view:"Chart"},{label:(0,D.t)("Dashboard"),url:"/dashboard/new",icon:"fa-fw fa-dashboard",perm:"can_write",view:"Dashboard"}],xe=()=>{F.A.get({endpoint:`/api/v1/database/?q=${w().encode({filters:[{col:"allow_file_upload",opr:"upload_is_enabled",value:!0}]})}`}).then((({json:e})=>{var a;const t=(null==e||null==(a=e.result)?void 0:a.filter((e=>{var a;return null==e||null==(a=e.engine_information)?void 0:a.supports_file_upload})))||[];ge((null==t?void 0:t.length)>=1)}))},Ye=()=>{F.A.get({endpoint:`/api/v1/database/?q=${w().encode({filters:[{col:"database_name",opr:"neq",value:"examples"}]})}`}).then((({json:e})=>{ve(e.count>=1)}))};(0,r.useEffect)((()=>{de&&xe()}),[de]),(0,r.useEffect)((()=>{(oe||se)&&Ye()}),[oe,se]);const we=e=>(0,U.Y)("i",{className:`fa ${e.icon}`}),Ce=(0,D.t)("Enable 'Allow file uploads to database' in any database's settings"),Se=e=>e.disable?(0,U.Y)(d.W1.Item,{css:B,disabled:!0,children:(0,U.Y)(c.m_,{placement:"top",title:Ce,children:e.label})},e.name):(0,U.Y)(d.W1.Item,{css:Q,children:e.url?(0,U.FD)("a",{href:e.url,children:[" ",e.label," "]}):e.label},e.name),Ae=H.get("navbar.right"),De=H.get("navbar.right-menu.item.icon"),Fe=(0,i.DP)();return(0,U.FD)(V,{align:e,children:[oe&&(0,U.Y)(k.Ay,{onHide:()=>{ne(""),q(!1)},show:A,dbEngine:te,onDatabaseAdd:()=>o({databaseAdded:!0})}),ce&&(0,U.Y)(I.A,{onHide:()=>O(!1),show:L,allowedExtensions:b,type:"csv"}),pe&&(0,U.Y)(I.A,{onHide:()=>Z(!1),show:G,allowedExtensions:_,type:"excel"}),he&&(0,U.Y)(I.A,{onHide:()=>ae(!1),show:ee,allowedExtensions:f,type:"columnar"}),(null==l?void 0:l.text)&&(0,U.Y)(N.Ay,{css:(0,v.AH)({borderRadius:125*Fe.gridUnit+"px"},"",""),color:/^#(?:[0-9a-f]{3}){1,2}$/i.test(l.color)?l.color:x()(Fe.colors,l.color),children:(0,U.Y)("span",{css:J,children:l.text})}),(0,U.FD)(d.W1,{selectable:!1,mode:"horizontal",onClick:e=>{e.key===R.$.DbConnection?q(!0):e.key===R.$.GoogleSheets?(q(!0),ne("Google Sheets")):e.key===R.$.CSVUpload?O(!0):e.key===R.$.ExcelUpload?Z(!0):e.key===R.$.ColumnarUpload&&ae(!0)},onOpenChange:e=>(e.length>1&&!y()(null==e?void 0:e.filter((e=>{var a;return e.includes(`sub2_${null==_e||null==(a=_e[0])?void 0:a.label}`)})))&&(de&&xe(),(oe||se)&&Ye()),null),disabledOverflow:!0,children:[Ae&&(0,U.Y)(Ae,{}),!t.user_is_anonymous&&ue&&(0,U.Y)(X,{title:(0,U.Y)(z,{className:"fa fa-plus"}),icon:(0,U.Y)(m.A.TriangleDown,{}),children:null==_e||null==_e.map?void 0:_e.map((e=>{var a;const t=null==(a=e.childs)?void 0:a.some((e=>"object"==typeof e&&!!e.perm));if(e.childs){var l;if(t)return(0,U.Y)(X,{className:"data-menu",title:e.label,icon:we(e),children:null==e||null==(l=e.childs)||null==l.map?void 0:l.map(((e,a)=>"string"!=typeof e&&e.name&&e.perm?(0,U.FD)(r.Fragment,{children:[3===a&&(0,U.Y)(d.W1.Divider,{}),Se(e)]},e.name):null))},`sub2_${e.label}`);if(!e.url)return null}return(0,E.L)(e.perm,e.view,g)&&(0,U.Y)(d.W1.Item,{children:n(e.url)?(0,U.FD)(p.N_,{to:e.url||"",children:[(0,U.Y)("i",{className:`fa ${e.icon}`})," ",e.label]}):(0,U.FD)("a",{href:e.url,children:[(0,U.Y)("i",{className:`fa ${e.icon}`})," ",e.label]})},e.label)}))}),(0,U.FD)(X,{title:(0,D.t)("Settings"),icon:(0,U.Y)(m.A.TriangleDown,{iconSize:"xl"}),children:[null==a||null==a.map?void 0:a.map(((e,t)=>{var l;return[(0,U.Y)(d.W1.ItemGroup,{title:e.label,children:null==e||null==(l=e.childs)||null==l.map?void 0:l.map((e=>{if("string"!=typeof e){const a=De?(0,U.FD)(W,{children:[e.label,(0,U.Y)(De,{menuChild:e})]}):e.label;return(0,U.Y)(d.W1.Item,{children:n(e.url)?(0,U.Y)(p.N_,{to:e.url||"",children:a}):(0,U.Y)("a",{href:e.url,children:a})},`${e.label}`)}return null}))},`${e.label}`),t<a.length-1&&(0,U.Y)(d.W1.Divider,{},`divider_${t}`)]})),!t.user_is_anonymous&&[(0,U.Y)(d.W1.Divider,{},"user-divider"),(0,U.FD)(d.W1.ItemGroup,{title:(0,D.t)("User"),children:[t.user_info_url&&(0,U.Y)(d.W1.Item,{children:(0,U.Y)("a",{href:t.user_info_url,children:(0,D.t)("Info")})},"info"),(0,U.Y)(d.W1.Item,{onClick:()=>{localStorage.removeItem("redux")},children:(0,U.Y)("a",{href:t.user_logout_url,children:(0,D.t)("Logout")})},"logout")]},"user-section")],(t.version_string||t.version_sha)&&[(0,U.Y)(d.W1.Divider,{},"version-info-divider"),(0,U.Y)(d.W1.ItemGroup,{title:(0,D.t)("About"),children:(0,U.FD)("div",{className:"about-section",children:[t.show_watermark&&(0,U.Y)("div",{css:j,children:(0,D.t)("Powered by Apache Superset")}),t.version_string&&(0,U.FD)("div",{css:j,children:[(0,D.t)("Version"),": ",t.version_string]}),t.version_sha&&(0,U.FD)("div",{css:j,children:[(0,D.t)("SHA"),": ",t.version_sha]}),t.build_number&&(0,U.FD)("div",{css:j,children:[(0,D.t)("Build"),": ",t.build_number]})]})},"about-section")]]}),t.show_language_picker&&(0,U.Y)(M,{locale:t.locale,languages:t.languages})]}),t.documentation_url&&(0,U.FD)(U.FK,{children:[(0,U.Y)(K,{href:t.documentation_url,target:"_blank",rel:"noreferrer",title:t.documentation_text||(0,D.t)("Documentation"),children:t.documentation_icon?(0,U.Y)("i",{className:t.documentation_icon}):(0,U.Y)("i",{className:"fa fa-question"})}),(0,U.Y)("span",{children:" "})]}),t.bug_report_url&&(0,U.FD)(U.FK,{children:[(0,U.Y)(K,{href:t.bug_report_url,target:"_blank",rel:"noreferrer",title:t.bug_report_text||(0,D.t)("Report a bug"),children:t.bug_report_icon?(0,U.Y)("i",{className:t.bug_report_icon}):(0,U.Y)("i",{className:"fa fa-bug"})}),(0,U.Y)("span",{children:" "})]}),t.user_is_anonymous&&(0,U.FD)(K,{href:t.user_login_url,children:[(0,U.Y)("i",{className:"fa fa-fw fa-sign-in"}),(0,D.t)("Login")]}),(0,U.Y)(P,{version:t.version_string,sha:t.version_sha,build:t.build_number})]})},ee=e=>{const[,a]=(0,S.sq)({databaseAdded:S.sJ,datasetAdded:S.sJ});return(0,U.Y)(Z,{setQuery:a,...e})};class ae extends r.PureComponent{constructor(...e){super(...e),this.state={hasError:!1},this.noop=()=>{}}static getDerivedStateFromError(){return{hasError:!0}}render(){return this.state.hasError?(0,U.Y)(Z,{setQuery:this.noop,...this.props}):this.props.children}}const te=e=>(0,U.Y)(ae,{...e,children:(0,U.Y)(ee,{...e})}),ne=i.I4.header`
  ${({theme:e})=>`\n      background-color: ${e.colors.grayscale.light5};\n      margin-bottom: 2px;\n      z-index: 10;\n\n      &:nth-last-of-type(2) nav {\n        margin-bottom: 2px;\n      }\n      .caret {\n        display: none;\n      }\n      .navbar-brand {\n        display: flex;\n        flex-direction: column;\n        justify-content: center;\n        /* must be exactly the height of the Antd navbar */\n        min-height: 50px;\n        padding: ${e.gridUnit}px\n          ${2*e.gridUnit}px\n          ${e.gridUnit}px\n          ${4*e.gridUnit}px;\n        max-width: ${e.gridUnit*e.brandIconMaxWidth}px;\n        img {\n          height: 100%;\n          object-fit: contain;\n        }\n        &:focus {\n          border-color: transparent;\n        }\n        &:focus-visible {\n          border-color: ${e.colors.primary.dark1};\n        }\n      }\n      .navbar-brand-text {\n        border-left: 1px solid ${e.colors.grayscale.light2};\n        border-right: 1px solid ${e.colors.grayscale.light2};\n        height: 100%;\n        color: ${e.colors.grayscale.dark1};\n        padding-left: ${4*e.gridUnit}px;\n        padding-right: ${4*e.gridUnit}px;\n        margin-right: ${6*e.gridUnit}px;\n        font-size: ${4*e.gridUnit}px;\n        float: left;\n        display: flex;\n        flex-direction: column;\n        justify-content: center;\n\n        span {\n          max-width: ${58*e.gridUnit}px;\n          white-space: nowrap;\n          overflow: hidden;\n          text-overflow: ellipsis;\n        }\n        @media (max-width: 1127px) {\n          display: none;\n        }\n      }\n      @media (max-width: 767px) {\n        .navbar-brand {\n          float: none;\n        }\n      }\n      @media (max-width: 767px) {\n        .antd5-menu-item {\n          padding: 0 ${6*e.gridUnit}px 0\n            ${3*e.gridUnit}px !important;\n        }\n        .antd5-menu > .antd5-menu-item > span > a {\n          padding: 0px;\n        }\n        .main-nav .antd5-menu-submenu-title > svg:nth-of-type(1) {\n          display: none;\n        }\n      }\n  `}
`,{SubMenu:le}=d.NG,re=(0,i.I4)(le)`
  &.antd5-menu-submenu-active {
    .antd5-menu-title-content {
      color: ${({theme:e})=>e.colors.primary.base};
    }
  }
`,{useBreakpoint:ie}=s.xA;function oe({data:{menu:e,brand:a,navbar_right:t,settings:n,environment_tag:i},isFrontendRoute:v=()=>!1}){const[f,y]=(0,r.useState)("horizontal"),_=ie(),x=(0,g.Q1)();let Y;(0,r.useEffect)((()=>{function e(){window.innerWidth<=767?y("inline"):y("horizontal")}e();const a=l()((()=>e()),10);return window.addEventListener("resize",a),()=>window.removeEventListener("resize",a)}),[]),function(e){e.Explore="/explore",e.Dashboard="/dashboard",e.Chart="/chart",e.Datasets="/tablemodelview"}(Y||(Y={}));const w=[],[C,S]=(0,r.useState)(w),A=(0,h.zy)();return(0,r.useEffect)((()=>{const e=A.pathname;switch(!0){case e.startsWith(Y.Dashboard):S(["Dashboards"]);break;case e.startsWith(Y.Chart)||e.startsWith(Y.Explore):S(["Charts"]);break;case e.startsWith(Y.Datasets):S(["Datasets"]);break;default:S(w)}}),[A.pathname]),(0,o.P3)(b.vX.standalone)||x.hideNav?(0,U.Y)(U.FK,{}):(0,U.Y)(ne,{className:"top",id:"main-menu",role:"navigation",children:(0,U.FD)(s.fI,{children:[(0,U.FD)(s.fv,{md:16,xs:24,children:[(0,U.Y)(c.m_,{id:"brand-tooltip",placement:"bottomLeft",title:a.tooltip,arrow:{pointAtCenter:!0},children:v(window.location.pathname)?(0,U.Y)(u.K,{className:"navbar-brand",to:a.path,children:(0,U.Y)("img",{src:a.icon,alt:a.alt})}):(0,U.Y)("a",{className:"navbar-brand",href:a.path,tabIndex:-1,children:(0,U.Y)("img",{src:a.icon,alt:a.alt})})}),a.text&&(0,U.Y)("div",{className:"navbar-brand-text",children:(0,U.Y)("span",{children:a.text})}),(0,U.Y)(d.NG,{mode:f,className:"main-nav",selectedKeys:C,disabledOverflow:!0,children:e.map(((e,a)=>{var t;return(({label:e,childs:a,url:t,index:n,isFrontendRoute:l})=>t&&l?(0,U.Y)(d.NG.Item,{role:"presentation",children:(0,U.Y)(p.k2,{role:"button",to:t,activeClassName:"is-active",children:e})},e):t?(0,U.Y)(d.NG.Item,{children:(0,U.Y)("a",{href:t,children:e})},e):(0,U.Y)(re,{title:e,icon:"inline"===f?(0,U.Y)(U.FK,{}):(0,U.Y)(m.A.TriangleDown,{}),children:null==a?void 0:a.map(((a,t)=>"string"==typeof a&&"-"===a&&"Data"!==e?(0,U.Y)(d.NG.Divider,{},`$${t}`):"string"!=typeof a?(0,U.Y)(d.NG.Item,{children:a.isFrontendRoute?(0,U.Y)(p.k2,{to:a.url||"",exact:!0,activeClassName:"is-active",children:a.label}):(0,U.Y)("a",{href:a.url,children:a.label})},`${a.label}`):null))},n))({index:a,...e,isFrontendRoute:v(e.url),childs:null==(t=e.childs)?void 0:t.map((e=>"string"==typeof e?e:{...e,isFrontendRoute:v(e.url)}))})}))})]}),(0,U.Y)(s.fv,{md:8,xs:24,children:(0,U.Y)(te,{align:_.md?"flex-end":"flex-start",settings:n,navbarRight:t,isFrontendRoute:v,environmentTag:i})})]})})}function se({data:e,...a}){const t={...e},n={Data:!0,Security:!0,Manage:!0},l=[],r=[];return t.menu.forEach((e=>{if(!e)return;const a=[],t={...e};e.childs&&(e.childs.forEach((e=>{("string"==typeof e||e.label)&&a.push(e)})),t.childs=a),n.hasOwnProperty(e.name)?r.push(t):l.push(t)})),t.menu=l,t.settings=r,(0,U.Y)(oe,{data:t,...a})}},62221:(e,a,t)=>{var n;function l(e,a){try{const t=localStorage.getItem(e);return null===t?a:JSON.parse(t)}catch{return a}}function r(e,a){try{localStorage.setItem(e,JSON.stringify(a))}catch{}}function i(e,a){return l(e,a)}function o(e,a){r(e,a)}t.d(a,{Gq:()=>i,Hh:()=>n,SO:()=>o,SX:()=>l,Wr:()=>r}),function(e){e.Database="db",e.ChartSplitSizes="chart_split_sizes",e.ControlsWidth="controls_width",e.DatasourceWidth="datasource_width",e.IsDatapanelOpen="is_datapanel_open",e.HomepageChartFilter="homepage_chart_filter",e.HomepageDashboardFilter="homepage_dashboard_filter",e.HomepageCollapseState="homepage_collapse_state",e.HomepageActivityFilter="homepage_activity_filter",e.DatasetnameSetSuccessful="datasetname_set_successful",e.SqllabIsAutocompleteEnabled="sqllab__is_autocomplete_enabled",e.SqllabIsRenderHtmlEnabled="sqllab__is_render_html_enabled",e.ExploreDataTableOriginalFormattedTimeColumns="explore__data_table_original_formatted_time_columns",e.DashboardCustomFilterBarWidths="dashboard__custom_filter_bar_widths",e.DashboardExploreContext="dashboard__explore_context",e.DashboardEditorShowOnlyMyCharts="dashboard__editor_show_only_my_charts",e.CommonResizableSidebarWidths="common__resizable_sidebar_widths"}(n||(n={}))}}]);