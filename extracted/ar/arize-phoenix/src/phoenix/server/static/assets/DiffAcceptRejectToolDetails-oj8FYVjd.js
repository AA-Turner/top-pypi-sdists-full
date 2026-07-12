import{Br as e,Mo as t,No as n,Po as r,jo as i,z as a}from"./vendor-streamdown-FRYh_TMF.js";import{c as o,l as s}from"./vendor-shiki-DQhfHv7h.js";import{a as c,i as l,n as u,r as d,t as f}from"./index-DxDQCD84.js";var p=r(),m=e`
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
`;function h(e){let r=(0,p.c)(22),{part:a,pending:o,snapshotToText:s,fileName:c,renderHeader:u,preparingLabel:h,preparingText:_,staleSessionMessage:v,showPreparing:y}=e,b;r[0]!==c||r[1]!==o||r[2]!==u||r[3]!==s||r[4]!==v?(b=o==null?null:t(g,{pending:o,snapshotToText:s,fileName:c,renderHeader:u,staleSessionMessage:v}),r[0]=c,r[1]=o,r[2]=u,r[3]=s,r[4]=v,r[5]=b):b=r[5];let x;r[6]!==a.output||r[7]!==a.state?(x=a.state===`output-available`?n(i,{children:[t(l,{children:`Result`}),t(d,{children:f(a.output)})]}):null,r[6]=a.output,r[7]=a.state,r[8]=x):x=r[8];let S;r[9]!==a.errorText||r[10]!==a.state?(S=a.state===`output-error`?n(i,{children:[t(l,{variant:`danger`,children:`Error`}),t(d,{children:a.errorText??``})]}):null,r[9]=a.errorText,r[10]=a.state,r[11]=S):S=r[11];let C;r[12]!==o||r[13]!==h||r[14]!==_||r[15]!==y?(C=o==null&&y?n(i,{children:[t(l,{children:h}),t(d,{children:_})]}):null,r[12]=o,r[13]=h,r[14]=_,r[15]=y,r[16]=C):C=r[16];let w;return r[17]!==b||r[18]!==x||r[19]!==S||r[20]!==C?(w=n(`div`,{className:`tool-part__body`,css:m,children:[b,x,S,C]}),r[17]=b,r[18]=x,r[19]=S,r[20]=C,r[21]=w):w=r[21],w}function g(e){let r=(0,p.c)(28),{pending:i,snapshotToText:l,fileName:d,renderHeader:f,staleSessionMessage:m}=e,{theme:h}=c(),g=!!(i.accept&&i.reject),_;r[0]!==d||r[1]!==i.after||r[2]!==i.before||r[3]!==l?(_=s({name:d,contents:l(i.before)},{name:d,contents:l(i.after)}),r[0]=d,r[1]=i.after,r[2]=i.before,r[3]=l,r[4]=_):_=r[4];let v=_,y;r[5]!==i||r[6]!==f?(y=f(i),r[5]=i,r[6]=f,r[7]=y):y=r[7];let b;r[8]===y?b=r[9]:(b=t(`div`,{className:`diff-accept-reject__header`,children:y}),r[8]=y,r[9]=b);let x;r[10]===Symbol.for(`react.memo_cache_sentinel`)?(x={light:`pierre-light`,dark:`pierre-dark`},r[10]=x):x=r[10];let S;r[11]===h?S=r[12]:(S={diffStyle:`unified`,disableFileHeader:!0,theme:x,themeType:h,unsafeCSS:`
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
            `},r[11]=h,r[12]=S);let C;r[13]!==v||r[14]!==S?(C=t(`div`,{className:`diff-accept-reject__diff`,children:t(o,{fileDiff:v,"data-background":`transparent`,options:S})}),r[13]=v,r[14]=S,r[15]=C):C=r[15];let w,T;r[16]===i?(w=r[17],T=r[18]):(w=()=>void i.accept?.(),T=()=>void i.reject?.(),r[16]=i,r[17]=w,r[18]=T);let E=!g,D;r[19]!==m||r[20]!==w||r[21]!==T||r[22]!==E?(D=t(u,{onAccept:w,onReject:T,isDisabled:E,staleMessage:m}),r[19]=m,r[20]=w,r[21]=T,r[22]=E,r[23]=D):D=r[23];let O;return r[24]!==D||r[25]!==b||r[26]!==C?(O=n(a,{direction:`column`,gap:`size-100`,children:[b,C,D]}),r[24]=D,r[25]=b,r[26]=C,r[27]=O):O=r[27],O}export{h as DiffAcceptRejectToolDetails};