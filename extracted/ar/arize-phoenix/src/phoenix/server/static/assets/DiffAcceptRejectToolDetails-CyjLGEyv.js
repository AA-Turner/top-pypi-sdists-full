import{Do as e,Eo as t,Fr as n,Oo as r,ko as i,z as a}from"./vendor-streamdown-Iyezjedh.js";import{c as o,l as s}from"./vendor-shiki-BSMFiH_P.js";import{a as c,i as l,n as u,r as d,t as f}from"./index-CwlX1Huf.js";var p=i(),m=n`
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
`;function h(n){let i=(0,p.c)(22),{part:a,pending:o,snapshotToText:s,fileName:c,renderHeader:u,preparingLabel:h,preparingText:_,staleSessionMessage:v,showPreparing:y}=n,b;i[0]!==c||i[1]!==o||i[2]!==u||i[3]!==s||i[4]!==v?(b=o==null?null:e(g,{pending:o,snapshotToText:s,fileName:c,renderHeader:u,staleSessionMessage:v}),i[0]=c,i[1]=o,i[2]=u,i[3]=s,i[4]=v,i[5]=b):b=i[5];let x;i[6]!==a.output||i[7]!==a.state?(x=a.state===`output-available`?r(t,{children:[e(l,{children:`Result`}),e(d,{children:f(a.output)})]}):null,i[6]=a.output,i[7]=a.state,i[8]=x):x=i[8];let S;i[9]!==a.errorText||i[10]!==a.state?(S=a.state===`output-error`?r(t,{children:[e(l,{variant:`danger`,children:`Error`}),e(d,{children:a.errorText??``})]}):null,i[9]=a.errorText,i[10]=a.state,i[11]=S):S=i[11];let C;i[12]!==o||i[13]!==h||i[14]!==_||i[15]!==y?(C=o==null&&y?r(t,{children:[e(l,{children:h}),e(d,{children:_})]}):null,i[12]=o,i[13]=h,i[14]=_,i[15]=y,i[16]=C):C=i[16];let w;return i[17]!==b||i[18]!==x||i[19]!==S||i[20]!==C?(w=r(`div`,{className:`tool-part__body`,css:m,children:[b,x,S,C]}),i[17]=b,i[18]=x,i[19]=S,i[20]=C,i[21]=w):w=i[21],w}function g(t){let n=(0,p.c)(28),{pending:i,snapshotToText:l,fileName:d,renderHeader:f,staleSessionMessage:m}=t,{theme:h}=c(),g=!!(i.accept&&i.reject),_;n[0]!==d||n[1]!==i.after||n[2]!==i.before||n[3]!==l?(_=s({name:d,contents:l(i.before)},{name:d,contents:l(i.after)}),n[0]=d,n[1]=i.after,n[2]=i.before,n[3]=l,n[4]=_):_=n[4];let v=_,y;n[5]!==i||n[6]!==f?(y=f(i),n[5]=i,n[6]=f,n[7]=y):y=n[7];let b;n[8]===y?b=n[9]:(b=e(`div`,{className:`diff-accept-reject__header`,children:y}),n[8]=y,n[9]=b);let x;n[10]===Symbol.for(`react.memo_cache_sentinel`)?(x={light:`pierre-light`,dark:`pierre-dark`},n[10]=x):x=n[10];let S;n[11]===h?S=n[12]:(S={diffStyle:`unified`,disableFileHeader:!0,theme:x,themeType:h,unsafeCSS:`
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
            `},n[11]=h,n[12]=S);let C;n[13]!==v||n[14]!==S?(C=e(`div`,{className:`diff-accept-reject__diff`,children:e(o,{fileDiff:v,"data-background":`transparent`,options:S})}),n[13]=v,n[14]=S,n[15]=C):C=n[15];let w,T;n[16]===i?(w=n[17],T=n[18]):(w=()=>void i.accept?.(),T=()=>void i.reject?.(),n[16]=i,n[17]=w,n[18]=T);let E=!g,D;n[19]!==m||n[20]!==w||n[21]!==T||n[22]!==E?(D=e(u,{onAccept:w,onReject:T,isDisabled:E,staleMessage:m}),n[19]=m,n[20]=w,n[21]=T,n[22]=E,n[23]=D):D=n[23];let O;return n[24]!==D||n[25]!==b||n[26]!==C?(O=r(a,{direction:`column`,gap:`size-100`,children:[b,C,D]}),n[24]=D,n[25]=b,n[26]=C,n[27]=O):O=n[27],O}export{h as DiffAcceptRejectToolDetails};