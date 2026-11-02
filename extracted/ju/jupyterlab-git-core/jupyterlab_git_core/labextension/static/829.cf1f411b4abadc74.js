"use strict";(self.rspackChunk_jupyterlab_git=self.rspackChunk_jupyterlab_git||[]).push([[829],{2720(e,t,n){function r(e){if(void 0===e)throw ReferenceError("this hasn't been initialised - super() hasn't been called");return e}n.d(t,{A:()=>r})},5108(e,t,n){n.d(t,{A:()=>U});var r=n(5285),i=n(644),o=n(5524),l=n.n(o),u=n(8919),a=n(5659),s=n(9360),c=n(8201),p=n(6852),d=n(3034),h=n(8851),f=n(2720),m=n(7874),b=n(7241);function v(e,t){var n=Object.create(null);return e&&o.Children.map(e,function(e){return e}).forEach(function(e){n[e.key]=t&&(0,o.isValidElement)(e)?t(e):e}),n}function g(e,t,n){return null!=n[t]?n[t]:e.props[t]}var y=Object.values||function(e){return Object.keys(e).map(function(t){return e[t]})},A=function(e){function t(t,n){var r=e.call(this,t,n)||this,i=r.handleExited.bind((0,f.A)(r));return r.state={contextValue:{isMounting:!0},handleExited:i,firstRender:!0},r}(0,m.A)(t,e);var n=t.prototype;return n.componentDidMount=function(){this.mounted=!0,this.setState({contextValue:{isMounting:!1}})},n.componentWillUnmount=function(){this.mounted=!1},t.getDerivedStateFromProps=function(e,t){var n,r,i=t.children,l=t.handleExited;return{children:t.firstRender?v(e.children,function(t){return(0,o.cloneElement)(t,{onExited:l.bind(null,t),in:!0,appear:g(t,"appear",e),enter:g(t,"enter",e),exit:g(t,"exit",e)})}):(Object.keys(r=function(e,t){function n(n){return n in t?t[n]:e[n]}e=e||{},t=t||{};var r,i=Object.create(null),o=[];for(var l in e)l in t?o.length&&(i[l]=o,o=[]):o.push(l);var u={};for(var a in t){if(i[a])for(r=0;r<i[a].length;r++){var s=i[a][r];u[i[a][r]]=n(s)}u[a]=n(a)}for(r=0;r<o.length;r++)u[o[r]]=n(o[r]);return u}(i,n=v(e.children))).forEach(function(t){var u=r[t];if((0,o.isValidElement)(u)){var a=t in i,s=t in n,c=i[t],p=(0,o.isValidElement)(c)&&!c.props.in;s&&(!a||p)?r[t]=(0,o.cloneElement)(u,{onExited:l.bind(null,u),in:!0,exit:g(u,"exit",e),enter:g(u,"enter",e)}):s||!a||p?s&&a&&(0,o.isValidElement)(c)&&(r[t]=(0,o.cloneElement)(u,{onExited:l.bind(null,u),in:c.props.in,exit:g(u,"exit",e),enter:g(u,"enter",e)})):r[t]=(0,o.cloneElement)(u,{in:!1})}}),r),firstRender:!1}},n.handleExited=function(e,t){var n=v(this.props.children);e.key in n||(e.props.onExited&&e.props.onExited(t),this.mounted&&this.setState(function(t){var n=(0,r.A)({},t.children);return delete n[e.key],{children:n}}))},n.render=function(){var e=this.props,t=e.component,n=e.childFactory,r=(0,i.A)(e,["component","childFactory"]),o=this.state.contextValue,u=y(this.state.children).map(n);return(delete r.appear,delete r.enter,delete r.exit,null===t)?l().createElement(b.A.Provider,{value:o},u):l().createElement(b.A.Provider,{value:o},l().createElement(t,r,u))},t}(l().Component);A.propTypes={},A.defaultProps={component:"div",childFactory:function(e){return e}};var x=n(5125),E=n(4848),R=n(8413);let M=(0,R.A)("MuiTouchRipple",["root","ripple","rippleVisible","ripplePulsate","child","childLeaving","childPulsate"]),k=["center","classes","className"],T=e=>e,C,P,V,j,$=(0,x.keyframes)(C||(C=T`
  0% {
    transform: scale(0);
    opacity: 0.1;
  }

  100% {
    transform: scale(1);
    opacity: 0.3;
  }
`)),w=(0,x.keyframes)(P||(P=T`
  0% {
    opacity: 1;
  }

  100% {
    opacity: 0;
  }
`)),S=(0,x.keyframes)(V||(V=T`
  0% {
    transform: scale(1);
  }

  50% {
    transform: scale(0.92);
  }

  100% {
    transform: scale(1);
  }
`)),B=(0,s.Ay)("span",{name:"MuiTouchRipple",slot:"Root"})({overflow:"hidden",pointerEvents:"none",position:"absolute",zIndex:0,top:0,right:0,bottom:0,left:0,borderRadius:"inherit"}),D=(0,s.Ay)(function(e){let{className:t,classes:n,pulsate:r=!1,rippleX:i,rippleY:l,rippleSize:a,in:s,onExited:c,timeout:p}=e,[d,h]=o.useState(!1),f=(0,u.A)(t,n.ripple,n.rippleVisible,r&&n.ripplePulsate),m=(0,u.A)(n.child,d&&n.childLeaving,r&&n.childPulsate);return s||d||h(!0),o.useEffect(()=>{if(!s&&null!=c){let e=setTimeout(c,p);return()=>{clearTimeout(e)}}},[c,s,p]),(0,E.jsx)("span",{className:f,style:{width:a,height:a,top:-(a/2)+l,left:-(a/2)+i},children:(0,E.jsx)("span",{className:m})})},{name:"MuiTouchRipple",slot:"Ripple"})(j||(j=T`
  opacity: 0;
  position: absolute;

  &.${0} {
    opacity: 0.3;
    transform: scale(1);
    animation-name: ${0};
    animation-duration: ${0}ms;
    animation-timing-function: ${0};
  }

  &.${0} {
    animation-duration: ${0}ms;
  }

  & .${0} {
    opacity: 1;
    display: block;
    width: 100%;
    height: 100%;
    border-radius: 50%;
    background-color: currentColor;
  }

  & .${0} {
    opacity: 0;
    animation-name: ${0};
    animation-duration: ${0}ms;
    animation-timing-function: ${0};
  }

  & .${0} {
    position: absolute;
    /* @noflip */
    left: 0px;
    top: 0;
    animation-name: ${0};
    animation-duration: 2500ms;
    animation-timing-function: ${0};
    animation-iteration-count: infinite;
    animation-delay: 200ms;
  }
`),M.rippleVisible,$,550,({theme:e})=>e.transitions.easing.easeInOut,M.ripplePulsate,({theme:e})=>e.transitions.duration.shorter,M.child,M.childLeaving,w,550,({theme:e})=>e.transitions.easing.easeInOut,M.childPulsate,S,({theme:e})=>e.transitions.easing.easeInOut),L=o.forwardRef(function(e,t){let n=(0,c.A)({props:e,name:"MuiTouchRipple"}),{center:l=!1,classes:a={},className:s}=n,p=(0,i.A)(n,k),[d,h]=o.useState([]),f=o.useRef(0),m=o.useRef(null);o.useEffect(()=>{m.current&&(m.current(),m.current=null)},[d]);let b=o.useRef(!1),v=o.useRef(0),g=o.useRef(null),y=o.useRef(null);o.useEffect(()=>()=>{v.current&&clearTimeout(v.current)},[]);let x=o.useCallback(e=>{let{pulsate:t,rippleX:n,rippleY:r,rippleSize:i,cb:o}=e;h(e=>[...e,(0,E.jsx)(D,{classes:{ripple:(0,u.A)(a.ripple,M.ripple),rippleVisible:(0,u.A)(a.rippleVisible,M.rippleVisible),ripplePulsate:(0,u.A)(a.ripplePulsate,M.ripplePulsate),child:(0,u.A)(a.child,M.child),childLeaving:(0,u.A)(a.childLeaving,M.childLeaving),childPulsate:(0,u.A)(a.childPulsate,M.childPulsate)},timeout:550,pulsate:t,rippleX:n,rippleY:r,rippleSize:i},f.current)]),f.current+=1,m.current=o},[a]),R=o.useCallback((e={},t={},n=()=>{})=>{let r,i,o,{pulsate:u=!1,center:a=l||t.pulsate,fakeElement:s=!1}=t;if((null==e?void 0:e.type)==="mousedown"&&b.current){b.current=!1;return}(null==e?void 0:e.type)==="touchstart"&&(b.current=!0);let c=s?null:y.current,p=c?c.getBoundingClientRect():{width:0,height:0,left:0,top:0};if(!a&&void 0!==e&&(0!==e.clientX||0!==e.clientY)&&(e.clientX||e.touches)){let{clientX:t,clientY:n}=e.touches&&e.touches.length>0?e.touches[0]:e;r=Math.round(t-p.left),i=Math.round(n-p.top)}else r=Math.round(p.width/2),i=Math.round(p.height/2);a?(o=Math.sqrt((2*p.width**2+p.height**2)/3))%2==0&&(o+=1):o=Math.sqrt((2*Math.max(Math.abs((c?c.clientWidth:0)-r),r)+2)**2+(2*Math.max(Math.abs((c?c.clientHeight:0)-i),i)+2)**2),null!=e&&e.touches?null===g.current&&(g.current=()=>{x({pulsate:u,rippleX:r,rippleY:i,rippleSize:o,cb:n})},v.current=setTimeout(()=>{g.current&&(g.current(),g.current=null)},80)):x({pulsate:u,rippleX:r,rippleY:i,rippleSize:o,cb:n})},[l,x]),T=o.useCallback(()=>{R({},{pulsate:!0})},[R]),C=o.useCallback((e,t)=>{if(clearTimeout(v.current),(null==e?void 0:e.type)==="touchend"&&g.current){g.current(),g.current=null,v.current=setTimeout(()=>{C(e,t)});return}g.current=null,h(e=>e.length>0?e.slice(1):e),m.current=t},[]);return o.useImperativeHandle(t,()=>({pulsate:T,start:R,stop:C}),[T,R,C]),(0,E.jsx)(B,(0,r.A)({className:(0,u.A)(M.root,a.root,s),ref:y},p,{children:(0,E.jsx)(A,{component:null,exit:!0,children:d})}))});var I=n(1609);function F(e){return(0,I.A)("MuiButtonBase",e)}let N=(0,R.A)("MuiButtonBase",["root","disabled","focusVisible"]),O=["action","centerRipple","children","className","component","disabled","disableRipple","disableTouchRipple","focusRipple","focusVisibleClassName","LinkComponent","onBlur","onClick","onContextMenu","onDragLeave","onFocus","onFocusVisible","onKeyDown","onKeyUp","onMouseDown","onMouseLeave","onMouseUp","onTouchEnd","onTouchMove","onTouchStart","tabIndex","TouchRippleProps","touchRippleRef","type"],z=(0,s.Ay)("button",{name:"MuiButtonBase",slot:"Root",overridesResolver:(e,t)=>t.root})({display:"inline-flex",alignItems:"center",justifyContent:"center",position:"relative",boxSizing:"border-box",WebkitTapHighlightColor:"transparent",backgroundColor:"transparent",outline:0,border:0,margin:0,borderRadius:0,padding:0,cursor:"pointer",userSelect:"none",verticalAlign:"middle",MozAppearance:"none",WebkitAppearance:"none",textDecoration:"none",color:"inherit","&::-moz-focus-inner":{borderStyle:"none"},[`&.${N.disabled}`]:{pointerEvents:"none",cursor:"default"},"@media print":{colorAdjust:"exact"}}),U=o.forwardRef(function(e,t){let n=(0,c.A)({props:e,name:"MuiButtonBase"}),{action:l,centerRipple:s=!1,children:f,className:m,component:b="button",disabled:v=!1,disableRipple:g=!1,disableTouchRipple:y=!1,focusRipple:A=!1,LinkComponent:x="a",onBlur:R,onClick:M,onContextMenu:k,onDragLeave:T,onFocus:C,onFocusVisible:P,onKeyDown:V,onKeyUp:j,onMouseDown:$,onMouseLeave:w,onMouseUp:S,onTouchEnd:B,onTouchMove:D,onTouchStart:I,tabIndex:N=0,TouchRippleProps:U,touchRippleRef:H,type:K}=n,W=(0,i.A)(n,O),_=o.useRef(null),X=o.useRef(null),q=(0,p.A)(X,H),{isFocusVisibleRef:Y,onFocus:G,onBlur:J,ref:Q}=(0,h.A)(),[Z,ee]=o.useState(!1);v&&Z&&ee(!1),o.useImperativeHandle(l,()=>({focusVisible:()=>{ee(!0),_.current.focus()}}),[]);let[et,en]=o.useState(!1);o.useEffect(()=>{en(!0)},[]);let er=et&&!g&&!v;function ei(e,t,n=y){return(0,d.A)(r=>(t&&t(r),!n&&X.current&&X.current[e](r),!0))}o.useEffect(()=>{Z&&A&&!g&&et&&X.current.pulsate()},[g,A,Z,et]);let eo=ei("start",$),el=ei("stop",k),eu=ei("stop",T),ea=ei("stop",S),es=ei("stop",e=>{Z&&e.preventDefault(),w&&w(e)}),ec=ei("start",I),ep=ei("stop",B),ed=ei("stop",D),eh=ei("stop",e=>{J(e),!1===Y.current&&ee(!1),R&&R(e)},!1),ef=(0,d.A)(e=>{_.current||(_.current=e.currentTarget),G(e),!0===Y.current&&(ee(!0),P&&P(e)),C&&C(e)}),em=()=>{let e=_.current;return b&&"button"!==b&&!("A"===e.tagName&&e.href)},eb=o.useRef(!1),ev=(0,d.A)(e=>{A&&!eb.current&&Z&&X.current&&" "===e.key&&(eb.current=!0,X.current.stop(e,()=>{X.current.start(e)})),e.target===e.currentTarget&&em()&&" "===e.key&&e.preventDefault(),V&&V(e),e.target===e.currentTarget&&em()&&"Enter"===e.key&&!v&&(e.preventDefault(),M&&M(e))}),eg=(0,d.A)(e=>{A&&" "===e.key&&X.current&&Z&&!e.defaultPrevented&&(eb.current=!1,X.current.stop(e,()=>{X.current.pulsate(e)})),j&&j(e),M&&e.target===e.currentTarget&&em()&&" "===e.key&&!e.defaultPrevented&&M(e)}),ey=b;"button"===ey&&(W.href||W.to)&&(ey=x);let eA={};"button"===ey?(eA.type=void 0===K?"button":K,eA.disabled=v):(W.href||W.to||(eA.role="button"),v&&(eA["aria-disabled"]=v));let ex=(0,p.A)(t,Q,_),eE=(0,r.A)({},n,{centerRipple:s,component:b,disabled:v,disableRipple:g,disableTouchRipple:y,focusRipple:A,tabIndex:N,focusVisible:Z}),eR=(e=>{let{disabled:t,focusVisible:n,focusVisibleClassName:r,classes:i}=e,o=(0,a.A)({root:["root",t&&"disabled",n&&"focusVisible"]},F,i);return n&&r&&(o.root+=` ${r}`),o})(eE);return(0,E.jsxs)(z,(0,r.A)({as:ey,className:(0,u.A)(eR.root,m),ownerState:eE,onBlur:eh,onClick:M,onContextMenu:el,onFocus:ef,onKeyDown:ev,onKeyUp:eg,onMouseDown:eo,onMouseLeave:es,onMouseUp:ea,onDragLeave:eu,onTouchEnd:ep,onTouchMove:ed,onTouchStart:ec,ref:ex,tabIndex:v?-1:N,type:K},eA,W,{children:[f,er?(0,E.jsx)(L,(0,r.A)({ref:q,center:s},U)):null]}))})}}]);