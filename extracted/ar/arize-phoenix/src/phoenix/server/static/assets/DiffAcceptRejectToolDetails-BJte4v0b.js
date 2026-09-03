import{Go as e,Jo as t,Ko as n,U as r,Xr as i,qo as a}from"./vendor-streamdown-B3oVlV66.js";import{i as o,n as s,r as c,t as l}from"./index-Cueqbr_a.js";import{ToolPartDiffView as u}from"./ToolPartPierreViews-D-l0I5Y2.js";var d=t(),f=i`
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
`;function p(t){let r=(0,d.c)(22),{part:i,pending:s,snapshotToText:u,fileName:p,renderHeader:h,preparingLabel:g,preparingText:_,staleSessionMessage:v,showPreparing:y}=t,b;r[0]!==p||r[1]!==s||r[2]!==h||r[3]!==u||r[4]!==v?(b=s==null?null:n(m,{pending:s,snapshotToText:u,fileName:p,renderHeader:h,staleSessionMessage:v}),r[0]=p,r[1]=s,r[2]=h,r[3]=u,r[4]=v,r[5]=b):b=r[5];let x;r[6]!==i.output||r[7]!==i.state?(x=i.state===`output-available`?a(e,{children:[n(o,{children:`Result`}),n(c,{children:l(i.output)})]}):null,r[6]=i.output,r[7]=i.state,r[8]=x):x=r[8];let S;r[9]!==i.errorText||r[10]!==i.state?(S=i.state===`output-error`?a(e,{children:[n(o,{variant:`danger`,children:`Error`}),n(c,{children:i.errorText??``})]}):null,r[9]=i.errorText,r[10]=i.state,r[11]=S):S=r[11];let C;r[12]!==s||r[13]!==g||r[14]!==_||r[15]!==y?(C=s==null&&y?a(e,{children:[n(o,{children:g}),n(c,{children:_})]}):null,r[12]=s,r[13]=g,r[14]=_,r[15]=y,r[16]=C):C=r[16];let w;return r[17]!==b||r[18]!==x||r[19]!==S||r[20]!==C?(w=a(`div`,{className:`tool-part__body`,css:f,children:[b,x,S,C]}),r[17]=b,r[18]=x,r[19]=S,r[20]=C,r[21]=w):w=r[21],w}function m(e){let t=(0,d.c)(27),{pending:i,snapshotToText:o,fileName:c,renderHeader:l,staleSessionMessage:f}=e,p=!!(i.accept&&i.reject),m;t[0]!==i||t[1]!==l?(m=l(i),t[0]=i,t[1]=l,t[2]=m):m=t[2];let h;t[3]===m?h=t[4]:(h=n(`div`,{className:`diff-accept-reject__header`,children:m}),t[3]=m,t[4]=h);let g;t[5]!==i.before||t[6]!==o?(g=o(i.before),t[5]=i.before,t[6]=o,t[7]=g):g=t[7];let _;t[8]!==i.after||t[9]!==o?(_=o(i.after),t[8]=i.after,t[9]=o,t[10]=_):_=t[10];let v;t[11]!==c||t[12]!==g||t[13]!==_?(v=n(u,{fileName:c,before:g,after:_}),t[11]=c,t[12]=g,t[13]=_,t[14]=v):v=t[14];let y,b;t[15]===i?(y=t[16],b=t[17]):(y=()=>void i.accept?.(),b=()=>void i.reject?.(),t[15]=i,t[16]=y,t[17]=b);let x=!p,S;t[18]!==f||t[19]!==y||t[20]!==b||t[21]!==x?(S=n(s,{onAccept:y,onReject:b,isDisabled:x,staleMessage:f}),t[18]=f,t[19]=y,t[20]=b,t[21]=x,t[22]=S):S=t[22];let C;return t[23]!==h||t[24]!==v||t[25]!==S?(C=a(r,{direction:`column`,gap:`size-100`,children:[h,v,S]}),t[23]=h,t[24]=v,t[25]=S,t[26]=C):C=t[26],C}export{p as DiffAcceptRejectToolDetails};