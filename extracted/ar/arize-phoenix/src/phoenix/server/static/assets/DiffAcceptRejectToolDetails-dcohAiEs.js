import{$r as e,U as t,_s as n,bs as r,vs as i,ys as a}from"./vendor-streamdown-BT0fJ3A3.js";import{i as o,n as s,r as c,t as l}from"./index-BeUAedO-.js";import{ToolPartDiffView as u}from"./ToolPartPierreViews-DrGsI4gh.js";var d=r(),f=e`
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
`;function p(e){let t=(0,d.c)(22),{part:r,pending:s,snapshotToText:u,fileName:p,renderHeader:h,preparingLabel:g,preparingText:_,staleSessionMessage:v,showPreparing:y}=e,b;t[0]!==p||t[1]!==s||t[2]!==h||t[3]!==u||t[4]!==v?(b=s==null?null:i(m,{pending:s,snapshotToText:u,fileName:p,renderHeader:h,staleSessionMessage:v}),t[0]=p,t[1]=s,t[2]=h,t[3]=u,t[4]=v,t[5]=b):b=t[5];let x;t[6]!==r.output||t[7]!==r.state?(x=r.state===`output-available`?a(n,{children:[i(o,{children:`Result`}),i(c,{children:l(r.output)})]}):null,t[6]=r.output,t[7]=r.state,t[8]=x):x=t[8];let S;t[9]!==r.errorText||t[10]!==r.state?(S=r.state===`output-error`?a(n,{children:[i(o,{variant:`danger`,children:`Error`}),i(c,{children:r.errorText??``})]}):null,t[9]=r.errorText,t[10]=r.state,t[11]=S):S=t[11];let C;t[12]!==s||t[13]!==g||t[14]!==_||t[15]!==y?(C=s==null&&y?a(n,{children:[i(o,{children:g}),i(c,{children:_})]}):null,t[12]=s,t[13]=g,t[14]=_,t[15]=y,t[16]=C):C=t[16];let w;return t[17]!==b||t[18]!==x||t[19]!==S||t[20]!==C?(w=a(`div`,{className:`tool-part__body`,css:f,children:[b,x,S,C]}),t[17]=b,t[18]=x,t[19]=S,t[20]=C,t[21]=w):w=t[21],w}function m(e){let n=(0,d.c)(27),{pending:r,snapshotToText:o,fileName:c,renderHeader:l,staleSessionMessage:f}=e,p=!!(r.accept&&r.reject),m;n[0]!==r||n[1]!==l?(m=l(r),n[0]=r,n[1]=l,n[2]=m):m=n[2];let h;n[3]===m?h=n[4]:(h=i(`div`,{className:`diff-accept-reject__header`,children:m}),n[3]=m,n[4]=h);let g;n[5]!==r.before||n[6]!==o?(g=o(r.before),n[5]=r.before,n[6]=o,n[7]=g):g=n[7];let _;n[8]!==r.after||n[9]!==o?(_=o(r.after),n[8]=r.after,n[9]=o,n[10]=_):_=n[10];let v;n[11]!==c||n[12]!==g||n[13]!==_?(v=i(u,{fileName:c,before:g,after:_}),n[11]=c,n[12]=g,n[13]=_,n[14]=v):v=n[14];let y,b;n[15]===r?(y=n[16],b=n[17]):(y=()=>void r.accept?.(),b=()=>void r.reject?.(),n[15]=r,n[16]=y,n[17]=b);let x=!p,S;n[18]!==f||n[19]!==y||n[20]!==b||n[21]!==x?(S=i(s,{onAccept:y,onReject:b,isDisabled:x,staleMessage:f}),n[18]=f,n[19]=y,n[20]=b,n[21]=x,n[22]=S):S=n[22];let C;return n[23]!==h||n[24]!==v||n[25]!==S?(C=a(t,{direction:`column`,gap:`size-100`,children:[h,v,S]}),n[23]=h,n[24]=v,n[25]=S,n[26]=C):C=n[26],C}export{p as DiffAcceptRejectToolDetails};