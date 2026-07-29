import{Fo as e,Mo as t,No as n,Po as r,z as i,zr as a}from"./vendor-streamdown-CYxShiF9.js";import{a as o,aa as s,c,n as l,o as u}from"./toolPartTypes-BH4-RrRK.js";import{c as d,l as f}from"./vendor-shiki-CRwTrkVg.js";var p=e(),m=a`
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
`;function h(e){let i=(0,p.c)(22),{part:a,pending:o,snapshotToText:s,fileName:d,renderHeader:f,preparingLabel:h,preparingText:_,staleSessionMessage:v,showPreparing:y}=e,b;i[0]!==d||i[1]!==o||i[2]!==f||i[3]!==s||i[4]!==v?(b=o==null?null:n(g,{pending:o,snapshotToText:s,fileName:d,renderHeader:f,staleSessionMessage:v}),i[0]=d,i[1]=o,i[2]=f,i[3]=s,i[4]=v,i[5]=b):b=i[5];let x;i[6]!==a.output||i[7]!==a.state?(x=a.state===`output-available`?r(t,{children:[n(c,{children:`Result`}),n(u,{children:l(a.output)})]}):null,i[6]=a.output,i[7]=a.state,i[8]=x):x=i[8];let S;i[9]!==a.errorText||i[10]!==a.state?(S=a.state===`output-error`?r(t,{children:[n(c,{variant:`danger`,children:`Error`}),n(u,{children:a.errorText??``})]}):null,i[9]=a.errorText,i[10]=a.state,i[11]=S):S=i[11];let C;i[12]!==o||i[13]!==h||i[14]!==_||i[15]!==y?(C=o==null&&y?r(t,{children:[n(c,{children:h}),n(u,{children:_})]}):null,i[12]=o,i[13]=h,i[14]=_,i[15]=y,i[16]=C):C=i[16];let w;return i[17]!==b||i[18]!==x||i[19]!==S||i[20]!==C?(w=r(`div`,{className:`tool-part__body`,css:m,children:[b,x,S,C]}),i[17]=b,i[18]=x,i[19]=S,i[20]=C,i[21]=w):w=i[21],w}function g(e){let t=(0,p.c)(28),{pending:a,snapshotToText:c,fileName:l,renderHeader:u,staleSessionMessage:m}=e,{theme:h}=s(),g=!!(a.accept&&a.reject),_;t[0]!==l||t[1]!==a.after||t[2]!==a.before||t[3]!==c?(_=f({name:l,contents:c(a.before)},{name:l,contents:c(a.after)}),t[0]=l,t[1]=a.after,t[2]=a.before,t[3]=c,t[4]=_):_=t[4];let v=_,y;t[5]!==a||t[6]!==u?(y=u(a),t[5]=a,t[6]=u,t[7]=y):y=t[7];let b;t[8]===y?b=t[9]:(b=n(`div`,{className:`diff-accept-reject__header`,children:y}),t[8]=y,t[9]=b);let x;t[10]===Symbol.for(`react.memo_cache_sentinel`)?(x={light:`pierre-light`,dark:`pierre-dark`},t[10]=x):x=t[10];let S;t[11]===h?S=t[12]:(S={diffStyle:`unified`,disableFileHeader:!0,theme:x,themeType:h,unsafeCSS:`
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
            `},t[11]=h,t[12]=S);let C;t[13]!==v||t[14]!==S?(C=n(`div`,{className:`diff-accept-reject__diff`,children:n(d,{fileDiff:v,"data-background":`transparent`,options:S})}),t[13]=v,t[14]=S,t[15]=C):C=t[15];let w,T;t[16]===a?(w=t[17],T=t[18]):(w=()=>void a.accept?.(),T=()=>void a.reject?.(),t[16]=a,t[17]=w,t[18]=T);let E=!g,D;t[19]!==m||t[20]!==w||t[21]!==T||t[22]!==E?(D=n(o,{onAccept:w,onReject:T,isDisabled:E,staleMessage:m}),t[19]=m,t[20]=w,t[21]=T,t[22]=E,t[23]=D):D=t[23];let O;return t[24]!==D||t[25]!==b||t[26]!==C?(O=r(i,{direction:`column`,gap:`size-100`,children:[b,C,D]}),t[24]=D,t[25]=b,t[26]=C,t[27]=O):O=t[27],O}export{h as DiffAcceptRejectToolDetails};