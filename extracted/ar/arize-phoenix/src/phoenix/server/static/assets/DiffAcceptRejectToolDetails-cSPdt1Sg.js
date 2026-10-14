import{U as e,Zr as t,_s as n,gs as r,hs as i,vs as a}from"./vendor-streamdown-DSE3r0AP.js";import{i as o,n as s,r as c,t as l}from"./index-Dsvb4FMm.js";import{ToolPartDiffView as u}from"./ToolPartPierreViews-BXoTiE0e.js";var d=a(),f=t`
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
`;function p(e){let t=(0,d.c)(22),{part:a,pending:s,snapshotToText:u,fileName:p,renderHeader:h,preparingLabel:g,preparingText:_,staleSessionMessage:v,showPreparing:y}=e,b;t[0]!==p||t[1]!==s||t[2]!==h||t[3]!==u||t[4]!==v?(b=s==null?null:r(m,{pending:s,snapshotToText:u,fileName:p,renderHeader:h,staleSessionMessage:v}),t[0]=p,t[1]=s,t[2]=h,t[3]=u,t[4]=v,t[5]=b):b=t[5];let x;t[6]!==a.output||t[7]!==a.state?(x=a.state===`output-available`?n(i,{children:[r(o,{children:`Result`}),r(c,{children:l(a.output)})]}):null,t[6]=a.output,t[7]=a.state,t[8]=x):x=t[8];let S;t[9]!==a.errorText||t[10]!==a.state?(S=a.state===`output-error`?n(i,{children:[r(o,{variant:`danger`,children:`Error`}),r(c,{children:a.errorText??``})]}):null,t[9]=a.errorText,t[10]=a.state,t[11]=S):S=t[11];let C;t[12]!==s||t[13]!==g||t[14]!==_||t[15]!==y?(C=s==null&&y?n(i,{children:[r(o,{children:g}),r(c,{children:_})]}):null,t[12]=s,t[13]=g,t[14]=_,t[15]=y,t[16]=C):C=t[16];let w;return t[17]!==b||t[18]!==x||t[19]!==S||t[20]!==C?(w=n(`div`,{className:`tool-part__body`,css:f,children:[b,x,S,C]}),t[17]=b,t[18]=x,t[19]=S,t[20]=C,t[21]=w):w=t[21],w}function m(t){let i=(0,d.c)(27),{pending:a,snapshotToText:o,fileName:c,renderHeader:l,staleSessionMessage:f}=t,p=!!(a.accept&&a.reject),m;i[0]!==a||i[1]!==l?(m=l(a),i[0]=a,i[1]=l,i[2]=m):m=i[2];let h;i[3]===m?h=i[4]:(h=r(`div`,{className:`diff-accept-reject__header`,children:m}),i[3]=m,i[4]=h);let g;i[5]!==a.before||i[6]!==o?(g=o(a.before),i[5]=a.before,i[6]=o,i[7]=g):g=i[7];let _;i[8]!==a.after||i[9]!==o?(_=o(a.after),i[8]=a.after,i[9]=o,i[10]=_):_=i[10];let v;i[11]!==c||i[12]!==g||i[13]!==_?(v=r(u,{fileName:c,before:g,after:_}),i[11]=c,i[12]=g,i[13]=_,i[14]=v):v=i[14];let y,b;i[15]===a?(y=i[16],b=i[17]):(y=()=>void a.accept?.(),b=()=>void a.reject?.(),i[15]=a,i[16]=y,i[17]=b);let x=!p,S;i[18]!==f||i[19]!==y||i[20]!==b||i[21]!==x?(S=r(s,{onAccept:y,onReject:b,isDisabled:x,staleMessage:f}),i[18]=f,i[19]=y,i[20]=b,i[21]=x,i[22]=S):S=i[22];let C;return i[23]!==h||i[24]!==v||i[25]!==S?(C=n(e,{direction:`column`,gap:`size-100`,children:[h,v,S]}),i[23]=h,i[24]=v,i[25]=S,i[26]=C):C=i[26],C}export{p as DiffAcceptRejectToolDetails};