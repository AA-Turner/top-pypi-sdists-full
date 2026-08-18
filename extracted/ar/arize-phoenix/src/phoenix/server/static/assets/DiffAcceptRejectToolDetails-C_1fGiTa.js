import{Bo as e,H as t,Ho as n,Vo as r,Wr as i,zo as a}from"./vendor-streamdown-f8ZsYTf7.js";import{a as o,c as s,ho as c,n as l,o as u}from"./toolPartTypes-BnTzjNNX.js";import{a as d,i as f}from"./vendor-shiki-CiB61Vc_.js";var p=n(),m=i`
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
`;function h(t){let n=(0,p.c)(22),{part:i,pending:o,snapshotToText:c,fileName:d,renderHeader:f,preparingLabel:h,preparingText:_,staleSessionMessage:v,showPreparing:y}=t,b;n[0]!==d||n[1]!==o||n[2]!==f||n[3]!==c||n[4]!==v?(b=o==null?null:e(g,{pending:o,snapshotToText:c,fileName:d,renderHeader:f,staleSessionMessage:v}),n[0]=d,n[1]=o,n[2]=f,n[3]=c,n[4]=v,n[5]=b):b=n[5];let x;n[6]!==i.output||n[7]!==i.state?(x=i.state===`output-available`?r(a,{children:[e(s,{children:`Result`}),e(u,{children:l(i.output)})]}):null,n[6]=i.output,n[7]=i.state,n[8]=x):x=n[8];let S;n[9]!==i.errorText||n[10]!==i.state?(S=i.state===`output-error`?r(a,{children:[e(s,{variant:`danger`,children:`Error`}),e(u,{children:i.errorText??``})]}):null,n[9]=i.errorText,n[10]=i.state,n[11]=S):S=n[11];let C;n[12]!==o||n[13]!==h||n[14]!==_||n[15]!==y?(C=o==null&&y?r(a,{children:[e(s,{children:h}),e(u,{children:_})]}):null,n[12]=o,n[13]=h,n[14]=_,n[15]=y,n[16]=C):C=n[16];let w;return n[17]!==b||n[18]!==x||n[19]!==S||n[20]!==C?(w=r(`div`,{className:`tool-part__body`,css:m,children:[b,x,S,C]}),n[17]=b,n[18]=x,n[19]=S,n[20]=C,n[21]=w):w=n[21],w}function g(n){let i=(0,p.c)(28),{pending:a,snapshotToText:s,fileName:l,renderHeader:u,staleSessionMessage:m}=n,{theme:h}=c(),g=!!(a.accept&&a.reject),_;i[0]!==l||i[1]!==a.after||i[2]!==a.before||i[3]!==s?(_=d({name:l,contents:s(a.before)},{name:l,contents:s(a.after)}),i[0]=l,i[1]=a.after,i[2]=a.before,i[3]=s,i[4]=_):_=i[4];let v=_,y;i[5]!==a||i[6]!==u?(y=u(a),i[5]=a,i[6]=u,i[7]=y):y=i[7];let b;i[8]===y?b=i[9]:(b=e(`div`,{className:`diff-accept-reject__header`,children:y}),i[8]=y,i[9]=b);let x;i[10]===Symbol.for(`react.memo_cache_sentinel`)?(x={light:`pierre-light`,dark:`pierre-dark`},i[10]=x):x=i[10];let S;i[11]===h?S=i[12]:(S={diffStyle:`unified`,disableFileHeader:!0,theme:x,themeType:h,unsafeCSS:`
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
            `},i[11]=h,i[12]=S);let C;i[13]!==v||i[14]!==S?(C=e(`div`,{className:`diff-accept-reject__diff`,children:e(f,{fileDiff:v,"data-background":`transparent`,options:S})}),i[13]=v,i[14]=S,i[15]=C):C=i[15];let w,T;i[16]===a?(w=i[17],T=i[18]):(w=()=>void a.accept?.(),T=()=>void a.reject?.(),i[16]=a,i[17]=w,i[18]=T);let E=!g,D;i[19]!==m||i[20]!==w||i[21]!==T||i[22]!==E?(D=e(o,{onAccept:w,onReject:T,isDisabled:E,staleMessage:m}),i[19]=m,i[20]=w,i[21]=T,i[22]=E,i[23]=D):D=i[23];let O;return i[24]!==D||i[25]!==b||i[26]!==C?(O=r(t,{direction:`column`,gap:`size-100`,children:[b,C,D]}),i[24]=D,i[25]=b,i[26]=C,i[27]=O):O=i[27],O}export{h as DiffAcceptRejectToolDetails};