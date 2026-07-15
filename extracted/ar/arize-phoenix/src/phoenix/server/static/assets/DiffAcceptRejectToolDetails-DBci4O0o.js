import{Mo as e,No as t,Po as n,jo as r,z as i,zr as a}from"./vendor-streamdown-DLAdUpKI.js";import{c as o,l as s}from"./vendor-shiki-CMMiReF1.js";import{a as c,i as l,n as u,r as d,t as f}from"./index-T629vnBw.js";var p=n(),m=a`
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
    font-family: var(--global-font-family-sans);
    white-space: normal;
  }
`;function h(n){let i=(0,p.c)(22),{part:a,pending:o,snapshotToText:s,fileName:c,renderHeader:u,preparingLabel:h,preparingText:_,staleSessionMessage:v,showPreparing:y}=n,b;i[0]!==c||i[1]!==o||i[2]!==u||i[3]!==s||i[4]!==v?(b=o==null?null:e(g,{pending:o,snapshotToText:s,fileName:c,renderHeader:u,staleSessionMessage:v}),i[0]=c,i[1]=o,i[2]=u,i[3]=s,i[4]=v,i[5]=b):b=i[5];let x;i[6]!==a.output||i[7]!==a.state?(x=a.state===`output-available`?t(r,{children:[e(l,{children:`Result`}),e(d,{children:f(a.output)})]}):null,i[6]=a.output,i[7]=a.state,i[8]=x):x=i[8];let S;i[9]!==a.errorText||i[10]!==a.state?(S=a.state===`output-error`?t(r,{children:[e(l,{variant:`danger`,children:`Error`}),e(d,{children:a.errorText??``})]}):null,i[9]=a.errorText,i[10]=a.state,i[11]=S):S=i[11];let C;i[12]!==o||i[13]!==h||i[14]!==_||i[15]!==y?(C=o==null&&y?t(r,{children:[e(l,{children:h}),e(d,{children:_})]}):null,i[12]=o,i[13]=h,i[14]=_,i[15]=y,i[16]=C):C=i[16];let w;return i[17]!==b||i[18]!==x||i[19]!==S||i[20]!==C?(w=t(`div`,{className:`tool-part__body`,css:m,children:[b,x,S,C]}),i[17]=b,i[18]=x,i[19]=S,i[20]=C,i[21]=w):w=i[21],w}function g(n){let r=(0,p.c)(28),{pending:a,snapshotToText:l,fileName:d,renderHeader:f,staleSessionMessage:m}=n,{theme:h}=c(),g=!!(a.accept&&a.reject),_;r[0]!==d||r[1]!==a.after||r[2]!==a.before||r[3]!==l?(_=s({name:d,contents:l(a.before)},{name:d,contents:l(a.after)}),r[0]=d,r[1]=a.after,r[2]=a.before,r[3]=l,r[4]=_):_=r[4];let v=_,y;r[5]!==a||r[6]!==f?(y=f(a),r[5]=a,r[6]=f,r[7]=y):y=r[7];let b;r[8]===y?b=r[9]:(b=e(`div`,{className:`diff-accept-reject__header`,children:y}),r[8]=y,r[9]=b);let x;r[10]===Symbol.for(`react.memo_cache_sentinel`)?(x={light:`pierre-light`,dark:`pierre-dark`},r[10]=x):x=r[10];let S;r[11]===h?S=r[12]:(S={diffStyle:`unified`,disableFileHeader:!0,theme:x,themeType:h,unsafeCSS:`
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
            `},r[11]=h,r[12]=S);let C;r[13]!==v||r[14]!==S?(C=e(`div`,{className:`diff-accept-reject__diff`,children:e(o,{fileDiff:v,"data-background":`transparent`,options:S})}),r[13]=v,r[14]=S,r[15]=C):C=r[15];let w,T;r[16]===a?(w=r[17],T=r[18]):(w=()=>void a.accept?.(),T=()=>void a.reject?.(),r[16]=a,r[17]=w,r[18]=T);let E=!g,D;r[19]!==m||r[20]!==w||r[21]!==T||r[22]!==E?(D=e(u,{onAccept:w,onReject:T,isDisabled:E,staleMessage:m}),r[19]=m,r[20]=w,r[21]=T,r[22]=E,r[23]=D):D=r[23];let O;return r[24]!==D||r[25]!==b||r[26]!==C?(O=t(i,{direction:`column`,gap:`size-100`,children:[b,C,D]}),r[24]=D,r[25]=b,r[26]=C,r[27]=O):O=r[27],O}export{h as DiffAcceptRejectToolDetails};