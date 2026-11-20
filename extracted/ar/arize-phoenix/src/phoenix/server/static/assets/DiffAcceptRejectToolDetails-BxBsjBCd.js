import{Cs as e,Ss as t,Ts as n,U as r,ii as i,ws as a}from"./vendor-streamdown-6L0QmST3.js";import{i as o,n as s,r as c,t as l}from"./index-B-eKduXe.js";import{ToolPartDiffView as u}from"./ToolPartPierreViews-LUthzra_.js";var d=n(),f=i`
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
`;function p(n){let r=(0,d.c)(22),{part:i,pending:s,snapshotToText:u,fileName:p,renderHeader:h,preparingLabel:g,preparingText:_,staleSessionMessage:v,showPreparing:y}=n,b;r[0]!==p||r[1]!==s||r[2]!==h||r[3]!==u||r[4]!==v?(b=s==null?null:e(m,{pending:s,snapshotToText:u,fileName:p,renderHeader:h,staleSessionMessage:v}),r[0]=p,r[1]=s,r[2]=h,r[3]=u,r[4]=v,r[5]=b):b=r[5];let x;r[6]!==i.output||r[7]!==i.state?(x=i.state===`output-available`?a(t,{children:[e(o,{children:`Result`}),e(c,{children:l(i.output)})]}):null,r[6]=i.output,r[7]=i.state,r[8]=x):x=r[8];let S;r[9]!==i.errorText||r[10]!==i.state?(S=i.state===`output-error`?a(t,{children:[e(o,{variant:`danger`,children:`Error`}),e(c,{children:i.errorText??``})]}):null,r[9]=i.errorText,r[10]=i.state,r[11]=S):S=r[11];let C;r[12]!==s||r[13]!==g||r[14]!==_||r[15]!==y?(C=s==null&&y?a(t,{children:[e(o,{children:g}),e(c,{children:_})]}):null,r[12]=s,r[13]=g,r[14]=_,r[15]=y,r[16]=C):C=r[16];let w;return r[17]!==b||r[18]!==x||r[19]!==S||r[20]!==C?(w=a(`div`,{className:`tool-part__body`,css:f,children:[b,x,S,C]}),r[17]=b,r[18]=x,r[19]=S,r[20]=C,r[21]=w):w=r[21],w}function m(t){let n=(0,d.c)(27),{pending:i,snapshotToText:o,fileName:c,renderHeader:l,staleSessionMessage:f}=t,p=!!(i.accept&&i.reject),m;n[0]!==i||n[1]!==l?(m=l(i),n[0]=i,n[1]=l,n[2]=m):m=n[2];let h;n[3]===m?h=n[4]:(h=e(`div`,{className:`diff-accept-reject__header`,children:m}),n[3]=m,n[4]=h);let g;n[5]!==i.before||n[6]!==o?(g=o(i.before),n[5]=i.before,n[6]=o,n[7]=g):g=n[7];let _;n[8]!==i.after||n[9]!==o?(_=o(i.after),n[8]=i.after,n[9]=o,n[10]=_):_=n[10];let v;n[11]!==c||n[12]!==g||n[13]!==_?(v=e(u,{fileName:c,before:g,after:_}),n[11]=c,n[12]=g,n[13]=_,n[14]=v):v=n[14];let y,b;n[15]===i?(y=n[16],b=n[17]):(y=()=>void i.accept?.(),b=()=>void i.reject?.(),n[15]=i,n[16]=y,n[17]=b);let x=!p,S;n[18]!==f||n[19]!==y||n[20]!==b||n[21]!==x?(S=e(s,{onAccept:y,onReject:b,isDisabled:x,staleMessage:f}),n[18]=f,n[19]=y,n[20]=b,n[21]=x,n[22]=S):S=n[22];let C;return n[23]!==h||n[24]!==v||n[25]!==S?(C=a(r,{direction:`column`,gap:`size-100`,children:[h,v,S]}),n[23]=h,n[24]=v,n[25]=S,n[26]=C):C=n[26],C}export{p as DiffAcceptRejectToolDetails};