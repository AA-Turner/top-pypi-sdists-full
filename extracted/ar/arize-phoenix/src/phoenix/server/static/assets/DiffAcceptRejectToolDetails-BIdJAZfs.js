import{Ao as e,Do as t,Ir as n,Oo as r,ko as i,z as a}from"./vendor-streamdown-BgNSPjUw.js";import{c as o,l as s}from"./vendor-shiki-CUwxbC9g.js";import{a as c,i as l,n as u,r as d,t as f}from"./index-BL1tnrKI.js";var p=e(),m=n`
  .diff-accept-reject__header {
    display: flex;
    align-items: center;
    min-width: 0;
    gap: var(--global-dimension-size-100);
    padding: var(--global-dimension-size-100) var(--global-dimension-size-250)
      var(--global-dimension-size-50);
  }

  .diff-accept-reject__header-icon {
    flex-shrink: 0;
  }

  .diff-accept-reject__header-label {
    min-width: 0;
    color: var(--tool-call-secondary-color);
    text-transform: uppercase;
    font-size: var(--global-font-size-xs);
    letter-spacing: 0.05em;
    user-select: none;
  }

  .diff-accept-reject__diff {
    font-family: var(--ac-global-font-family-sans);
    white-space: normal;
  }
`;function h(e){let n=(0,p.c)(22),{part:a,pending:o,snapshotToText:s,fileName:c,renderHeader:u,preparingLabel:h,preparingText:_,staleSessionMessage:v,showPreparing:y}=e,b;n[0]!==c||n[1]!==o||n[2]!==u||n[3]!==s||n[4]!==v?(b=o==null?null:r(g,{pending:o,snapshotToText:s,fileName:c,renderHeader:u,staleSessionMessage:v}),n[0]=c,n[1]=o,n[2]=u,n[3]=s,n[4]=v,n[5]=b):b=n[5];let x;n[6]!==a.output||n[7]!==a.state?(x=a.state===`output-available`?i(t,{children:[r(l,{children:`Result`}),r(d,{children:f(a.output)})]}):null,n[6]=a.output,n[7]=a.state,n[8]=x):x=n[8];let S;n[9]!==a.errorText||n[10]!==a.state?(S=a.state===`output-error`?i(t,{children:[r(l,{variant:`danger`,children:`Error`}),r(d,{children:a.errorText??``})]}):null,n[9]=a.errorText,n[10]=a.state,n[11]=S):S=n[11];let C;n[12]!==o||n[13]!==h||n[14]!==_||n[15]!==y?(C=o==null&&y?i(t,{children:[r(l,{children:h}),r(d,{children:_})]}):null,n[12]=o,n[13]=h,n[14]=_,n[15]=y,n[16]=C):C=n[16];let w;return n[17]!==b||n[18]!==x||n[19]!==S||n[20]!==C?(w=i(`div`,{className:`tool-part__body`,css:m,children:[b,x,S,C]}),n[17]=b,n[18]=x,n[19]=S,n[20]=C,n[21]=w):w=n[21],w}function g(e){let t=(0,p.c)(28),{pending:n,snapshotToText:l,fileName:d,renderHeader:f,staleSessionMessage:m}=e,{theme:h}=c(),g=!!(n.accept&&n.reject),_;t[0]!==d||t[1]!==n.after||t[2]!==n.before||t[3]!==l?(_=s({name:d,contents:l(n.before)},{name:d,contents:l(n.after)}),t[0]=d,t[1]=n.after,t[2]=n.before,t[3]=l,t[4]=_):_=t[4];let v=_,y;t[5]!==n||t[6]!==f?(y=f(n),t[5]=n,t[6]=f,t[7]=y):y=t[7];let b;t[8]===y?b=t[9]:(b=r(`div`,{className:`diff-accept-reject__header`,children:y}),t[8]=y,t[9]=b);let x;t[10]===Symbol.for(`react.memo_cache_sentinel`)?(x={light:`pierre-light`,dark:`pierre-dark`},t[10]=x):x=t[10];let S;t[11]===h?S=t[12]:(S={diffStyle:`unified`,disableFileHeader:!0,theme:x,themeType:h,unsafeCSS:`
            pre, pre code, [data-line-type=context], [data-gutter], svg {
              background: var(--tool-call-body-background-color);
              stroke: unset;
              fill: unset;
            }

            [data-line-type] {
              border-right: none;
            }

            [data-code] {
              padding: 0;
              padding-bottom: var(--global-dimension-static-size-100)
            }

            [data-column-number] {
              padding-left: 1.5ch;
            }
            `},t[11]=h,t[12]=S);let C;t[13]!==v||t[14]!==S?(C=r(`div`,{className:`diff-accept-reject__diff`,children:r(o,{fileDiff:v,"data-background":`transparent`,options:S})}),t[13]=v,t[14]=S,t[15]=C):C=t[15];let w,T;t[16]===n?(w=t[17],T=t[18]):(w=()=>void n.accept?.(),T=()=>void n.reject?.(),t[16]=n,t[17]=w,t[18]=T);let E=!g,D;t[19]!==m||t[20]!==w||t[21]!==T||t[22]!==E?(D=r(u,{onAccept:w,onReject:T,isDisabled:E,staleMessage:m}),t[19]=m,t[20]=w,t[21]=T,t[22]=E,t[23]=D):D=t[23];let O;return t[24]!==D||t[25]!==b||t[26]!==C?(O=i(a,{direction:`column`,gap:`size-100`,children:[b,C,D]}),t[24]=D,t[25]=b,t[26]=C,t[27]=O):O=t[27],O}export{h as DiffAcceptRejectToolDetails};