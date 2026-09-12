import{Jo as e,U as t,Xo as n,Xr as r,Yo as i,qo as a}from"./vendor-streamdown-D_OE4pRm.js";import{i as o,n as s,r as c,t as l}from"./index-6Gu5huqS.js";import{ToolPartDiffView as u}from"./ToolPartPierreViews-C76zj9wo.js";var d=n(),f=r`
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
`;function p(t){let n=(0,d.c)(22),{part:r,pending:s,snapshotToText:u,fileName:p,renderHeader:h,preparingLabel:g,preparingText:_,staleSessionMessage:v,showPreparing:y}=t,b;n[0]!==p||n[1]!==s||n[2]!==h||n[3]!==u||n[4]!==v?(b=s==null?null:e(m,{pending:s,snapshotToText:u,fileName:p,renderHeader:h,staleSessionMessage:v}),n[0]=p,n[1]=s,n[2]=h,n[3]=u,n[4]=v,n[5]=b):b=n[5];let x;n[6]!==r.output||n[7]!==r.state?(x=r.state===`output-available`?i(a,{children:[e(o,{children:`Result`}),e(c,{children:l(r.output)})]}):null,n[6]=r.output,n[7]=r.state,n[8]=x):x=n[8];let S;n[9]!==r.errorText||n[10]!==r.state?(S=r.state===`output-error`?i(a,{children:[e(o,{variant:`danger`,children:`Error`}),e(c,{children:r.errorText??``})]}):null,n[9]=r.errorText,n[10]=r.state,n[11]=S):S=n[11];let C;n[12]!==s||n[13]!==g||n[14]!==_||n[15]!==y?(C=s==null&&y?i(a,{children:[e(o,{children:g}),e(c,{children:_})]}):null,n[12]=s,n[13]=g,n[14]=_,n[15]=y,n[16]=C):C=n[16];let w;return n[17]!==b||n[18]!==x||n[19]!==S||n[20]!==C?(w=i(`div`,{className:`tool-part__body`,css:f,children:[b,x,S,C]}),n[17]=b,n[18]=x,n[19]=S,n[20]=C,n[21]=w):w=n[21],w}function m(n){let r=(0,d.c)(27),{pending:a,snapshotToText:o,fileName:c,renderHeader:l,staleSessionMessage:f}=n,p=!!(a.accept&&a.reject),m;r[0]!==a||r[1]!==l?(m=l(a),r[0]=a,r[1]=l,r[2]=m):m=r[2];let h;r[3]===m?h=r[4]:(h=e(`div`,{className:`diff-accept-reject__header`,children:m}),r[3]=m,r[4]=h);let g;r[5]!==a.before||r[6]!==o?(g=o(a.before),r[5]=a.before,r[6]=o,r[7]=g):g=r[7];let _;r[8]!==a.after||r[9]!==o?(_=o(a.after),r[8]=a.after,r[9]=o,r[10]=_):_=r[10];let v;r[11]!==c||r[12]!==g||r[13]!==_?(v=e(u,{fileName:c,before:g,after:_}),r[11]=c,r[12]=g,r[13]=_,r[14]=v):v=r[14];let y,b;r[15]===a?(y=r[16],b=r[17]):(y=()=>void a.accept?.(),b=()=>void a.reject?.(),r[15]=a,r[16]=y,r[17]=b);let x=!p,S;r[18]!==f||r[19]!==y||r[20]!==b||r[21]!==x?(S=e(s,{onAccept:y,onReject:b,isDisabled:x,staleMessage:f}),r[18]=f,r[19]=y,r[20]=b,r[21]=x,r[22]=S):S=r[22];let C;return r[23]!==h||r[24]!==v||r[25]!==S?(C=i(t,{direction:`column`,gap:`size-100`,children:[h,v,S]}),r[23]=h,r[24]=v,r[25]=S,r[26]=C):C=r[26],C}export{p as DiffAcceptRejectToolDetails};