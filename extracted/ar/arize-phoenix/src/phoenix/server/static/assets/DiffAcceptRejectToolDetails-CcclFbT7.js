import{Br as e,Fo as t,Mo as n,No as r,Po as i,z as a}from"./vendor-streamdown-B9i_QIkL.js";import{c as o,l as s}from"./vendor-shiki-DErOVhO6.js";import{a as c,i as l,n as u,r as d,t as f}from"./index-Btpaqypv.js";var p=t(),m=e`
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
`;function h(e){let t=(0,p.c)(22),{part:a,pending:o,snapshotToText:s,fileName:c,renderHeader:u,preparingLabel:h,preparingText:_,staleSessionMessage:v,showPreparing:y}=e,b;t[0]!==c||t[1]!==o||t[2]!==u||t[3]!==s||t[4]!==v?(b=o==null?null:r(g,{pending:o,snapshotToText:s,fileName:c,renderHeader:u,staleSessionMessage:v}),t[0]=c,t[1]=o,t[2]=u,t[3]=s,t[4]=v,t[5]=b):b=t[5];let x;t[6]!==a.output||t[7]!==a.state?(x=a.state===`output-available`?i(n,{children:[r(l,{children:`Result`}),r(d,{children:f(a.output)})]}):null,t[6]=a.output,t[7]=a.state,t[8]=x):x=t[8];let S;t[9]!==a.errorText||t[10]!==a.state?(S=a.state===`output-error`?i(n,{children:[r(l,{variant:`danger`,children:`Error`}),r(d,{children:a.errorText??``})]}):null,t[9]=a.errorText,t[10]=a.state,t[11]=S):S=t[11];let C;t[12]!==o||t[13]!==h||t[14]!==_||t[15]!==y?(C=o==null&&y?i(n,{children:[r(l,{children:h}),r(d,{children:_})]}):null,t[12]=o,t[13]=h,t[14]=_,t[15]=y,t[16]=C):C=t[16];let w;return t[17]!==b||t[18]!==x||t[19]!==S||t[20]!==C?(w=i(`div`,{className:`tool-part__body`,css:m,children:[b,x,S,C]}),t[17]=b,t[18]=x,t[19]=S,t[20]=C,t[21]=w):w=t[21],w}function g(e){let t=(0,p.c)(28),{pending:n,snapshotToText:l,fileName:d,renderHeader:f,staleSessionMessage:m}=e,{theme:h}=c(),g=!!(n.accept&&n.reject),_;t[0]!==d||t[1]!==n.after||t[2]!==n.before||t[3]!==l?(_=s({name:d,contents:l(n.before)},{name:d,contents:l(n.after)}),t[0]=d,t[1]=n.after,t[2]=n.before,t[3]=l,t[4]=_):_=t[4];let v=_,y;t[5]!==n||t[6]!==f?(y=f(n),t[5]=n,t[6]=f,t[7]=y):y=t[7];let b;t[8]===y?b=t[9]:(b=r(`div`,{className:`diff-accept-reject__header`,children:y}),t[8]=y,t[9]=b);let x;t[10]===Symbol.for(`react.memo_cache_sentinel`)?(x={light:`pierre-light`,dark:`pierre-dark`},t[10]=x):x=t[10];let S;t[11]===h?S=t[12]:(S={diffStyle:`unified`,disableFileHeader:!0,theme:x,themeType:h,unsafeCSS:`
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