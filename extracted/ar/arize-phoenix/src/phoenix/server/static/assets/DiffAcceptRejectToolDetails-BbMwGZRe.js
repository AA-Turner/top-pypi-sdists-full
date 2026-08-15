import{Fo as e,Io as t,Lo as n,Ro as r,Vr as i,z as a}from"./vendor-streamdown-BLV5_fPs.js";import{a as o,c as s,n as c,o as l,po as u}from"./toolPartTypes-GJ7YWL-e.js";import{a as d,i as f}from"./vendor-shiki-D42C0yEl.js";var p=r(),m=i`
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
`;function h(r){let i=(0,p.c)(22),{part:a,pending:o,snapshotToText:u,fileName:d,renderHeader:f,preparingLabel:h,preparingText:_,staleSessionMessage:v,showPreparing:y}=r,b;i[0]!==d||i[1]!==o||i[2]!==f||i[3]!==u||i[4]!==v?(b=o==null?null:t(g,{pending:o,snapshotToText:u,fileName:d,renderHeader:f,staleSessionMessage:v}),i[0]=d,i[1]=o,i[2]=f,i[3]=u,i[4]=v,i[5]=b):b=i[5];let x;i[6]!==a.output||i[7]!==a.state?(x=a.state===`output-available`?n(e,{children:[t(s,{children:`Result`}),t(l,{children:c(a.output)})]}):null,i[6]=a.output,i[7]=a.state,i[8]=x):x=i[8];let S;i[9]!==a.errorText||i[10]!==a.state?(S=a.state===`output-error`?n(e,{children:[t(s,{variant:`danger`,children:`Error`}),t(l,{children:a.errorText??``})]}):null,i[9]=a.errorText,i[10]=a.state,i[11]=S):S=i[11];let C;i[12]!==o||i[13]!==h||i[14]!==_||i[15]!==y?(C=o==null&&y?n(e,{children:[t(s,{children:h}),t(l,{children:_})]}):null,i[12]=o,i[13]=h,i[14]=_,i[15]=y,i[16]=C):C=i[16];let w;return i[17]!==b||i[18]!==x||i[19]!==S||i[20]!==C?(w=n(`div`,{className:`tool-part__body`,css:m,children:[b,x,S,C]}),i[17]=b,i[18]=x,i[19]=S,i[20]=C,i[21]=w):w=i[21],w}function g(e){let r=(0,p.c)(28),{pending:i,snapshotToText:s,fileName:c,renderHeader:l,staleSessionMessage:m}=e,{theme:h}=u(),g=!!(i.accept&&i.reject),_;r[0]!==c||r[1]!==i.after||r[2]!==i.before||r[3]!==s?(_=d({name:c,contents:s(i.before)},{name:c,contents:s(i.after)}),r[0]=c,r[1]=i.after,r[2]=i.before,r[3]=s,r[4]=_):_=r[4];let v=_,y;r[5]!==i||r[6]!==l?(y=l(i),r[5]=i,r[6]=l,r[7]=y):y=r[7];let b;r[8]===y?b=r[9]:(b=t(`div`,{className:`diff-accept-reject__header`,children:y}),r[8]=y,r[9]=b);let x;r[10]===Symbol.for(`react.memo_cache_sentinel`)?(x={light:`pierre-light`,dark:`pierre-dark`},r[10]=x):x=r[10];let S;r[11]===h?S=r[12]:(S={diffStyle:`unified`,disableFileHeader:!0,theme:x,themeType:h,unsafeCSS:`
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
              padding-bottom: var(--global-dimension-size-100)
            }

            [data-column-number] {
              padding-left: 1.5ch;
            }
            `},r[11]=h,r[12]=S);let C;r[13]!==v||r[14]!==S?(C=t(`div`,{className:`diff-accept-reject__diff`,children:t(f,{fileDiff:v,"data-background":`transparent`,options:S})}),r[13]=v,r[14]=S,r[15]=C):C=r[15];let w,T;r[16]===i?(w=r[17],T=r[18]):(w=()=>void i.accept?.(),T=()=>void i.reject?.(),r[16]=i,r[17]=w,r[18]=T);let E=!g,D;r[19]!==m||r[20]!==w||r[21]!==T||r[22]!==E?(D=t(o,{onAccept:w,onReject:T,isDisabled:E,staleMessage:m}),r[19]=m,r[20]=w,r[21]=T,r[22]=E,r[23]=D):D=r[23];let O;return r[24]!==D||r[25]!==b||r[26]!==C?(O=n(a,{direction:`column`,gap:`size-100`,children:[b,C,D]}),r[24]=D,r[25]=b,r[26]=C,r[27]=O):O=r[27],O}export{h as DiffAcceptRejectToolDetails};