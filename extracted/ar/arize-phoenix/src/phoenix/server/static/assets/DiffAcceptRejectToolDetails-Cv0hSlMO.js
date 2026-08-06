import{Fo as e,Io as t,No as n,Po as r,z as i,zr as a}from"./vendor-streamdown-DicArkC7.js";import{a as o,c as s,do as c,n as l,o as u}from"./toolPartTypes-BqDby3SE.js";import{a as d,i as f}from"./vendor-shiki-Dq6QPeNt.js";var p=t(),m=a`
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
`;function h(t){let i=(0,p.c)(22),{part:a,pending:o,snapshotToText:c,fileName:d,renderHeader:f,preparingLabel:h,preparingText:_,staleSessionMessage:v,showPreparing:y}=t,b;i[0]!==d||i[1]!==o||i[2]!==f||i[3]!==c||i[4]!==v?(b=o==null?null:r(g,{pending:o,snapshotToText:c,fileName:d,renderHeader:f,staleSessionMessage:v}),i[0]=d,i[1]=o,i[2]=f,i[3]=c,i[4]=v,i[5]=b):b=i[5];let x;i[6]!==a.output||i[7]!==a.state?(x=a.state===`output-available`?e(n,{children:[r(s,{children:`Result`}),r(u,{children:l(a.output)})]}):null,i[6]=a.output,i[7]=a.state,i[8]=x):x=i[8];let S;i[9]!==a.errorText||i[10]!==a.state?(S=a.state===`output-error`?e(n,{children:[r(s,{variant:`danger`,children:`Error`}),r(u,{children:a.errorText??``})]}):null,i[9]=a.errorText,i[10]=a.state,i[11]=S):S=i[11];let C;i[12]!==o||i[13]!==h||i[14]!==_||i[15]!==y?(C=o==null&&y?e(n,{children:[r(s,{children:h}),r(u,{children:_})]}):null,i[12]=o,i[13]=h,i[14]=_,i[15]=y,i[16]=C):C=i[16];let w;return i[17]!==b||i[18]!==x||i[19]!==S||i[20]!==C?(w=e(`div`,{className:`tool-part__body`,css:m,children:[b,x,S,C]}),i[17]=b,i[18]=x,i[19]=S,i[20]=C,i[21]=w):w=i[21],w}function g(t){let n=(0,p.c)(28),{pending:a,snapshotToText:s,fileName:l,renderHeader:u,staleSessionMessage:m}=t,{theme:h}=c(),g=!!(a.accept&&a.reject),_;n[0]!==l||n[1]!==a.after||n[2]!==a.before||n[3]!==s?(_=d({name:l,contents:s(a.before)},{name:l,contents:s(a.after)}),n[0]=l,n[1]=a.after,n[2]=a.before,n[3]=s,n[4]=_):_=n[4];let v=_,y;n[5]!==a||n[6]!==u?(y=u(a),n[5]=a,n[6]=u,n[7]=y):y=n[7];let b;n[8]===y?b=n[9]:(b=r(`div`,{className:`diff-accept-reject__header`,children:y}),n[8]=y,n[9]=b);let x;n[10]===Symbol.for(`react.memo_cache_sentinel`)?(x={light:`pierre-light`,dark:`pierre-dark`},n[10]=x):x=n[10];let S;n[11]===h?S=n[12]:(S={diffStyle:`unified`,disableFileHeader:!0,theme:x,themeType:h,unsafeCSS:`
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
            `},n[11]=h,n[12]=S);let C;n[13]!==v||n[14]!==S?(C=r(`div`,{className:`diff-accept-reject__diff`,children:r(f,{fileDiff:v,"data-background":`transparent`,options:S})}),n[13]=v,n[14]=S,n[15]=C):C=n[15];let w,T;n[16]===a?(w=n[17],T=n[18]):(w=()=>void a.accept?.(),T=()=>void a.reject?.(),n[16]=a,n[17]=w,n[18]=T);let E=!g,D;n[19]!==m||n[20]!==w||n[21]!==T||n[22]!==E?(D=r(o,{onAccept:w,onReject:T,isDisabled:E,staleMessage:m}),n[19]=m,n[20]=w,n[21]=T,n[22]=E,n[23]=D):D=n[23];let O;return n[24]!==D||n[25]!==b||n[26]!==C?(O=e(i,{direction:`column`,gap:`size-100`,children:[b,C,D]}),n[24]=D,n[25]=b,n[26]=C,n[27]=O):O=n[27],O}export{h as DiffAcceptRejectToolDetails};