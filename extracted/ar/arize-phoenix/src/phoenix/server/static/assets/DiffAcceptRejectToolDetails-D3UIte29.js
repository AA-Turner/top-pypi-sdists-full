import{Go as e,Ho as t,U as n,Uo as r,Wo as i,qr as a}from"./vendor-streamdown-CoKIfNf_.js";import{i as o,n as s,r as c,t as l}from"./index-DD-6nw4p.js";import{ToolPartDiffView as u}from"./ToolPartPierreViews-SV62_s94.js";var d=e(),f=a`
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
`;function p(e){let n=(0,d.c)(22),{part:a,pending:s,snapshotToText:u,fileName:p,renderHeader:h,preparingLabel:g,preparingText:_,staleSessionMessage:v,showPreparing:y}=e,b;n[0]!==p||n[1]!==s||n[2]!==h||n[3]!==u||n[4]!==v?(b=s==null?null:r(m,{pending:s,snapshotToText:u,fileName:p,renderHeader:h,staleSessionMessage:v}),n[0]=p,n[1]=s,n[2]=h,n[3]=u,n[4]=v,n[5]=b):b=n[5];let x;n[6]!==a.output||n[7]!==a.state?(x=a.state===`output-available`?i(t,{children:[r(o,{children:`Result`}),r(c,{children:l(a.output)})]}):null,n[6]=a.output,n[7]=a.state,n[8]=x):x=n[8];let S;n[9]!==a.errorText||n[10]!==a.state?(S=a.state===`output-error`?i(t,{children:[r(o,{variant:`danger`,children:`Error`}),r(c,{children:a.errorText??``})]}):null,n[9]=a.errorText,n[10]=a.state,n[11]=S):S=n[11];let C;n[12]!==s||n[13]!==g||n[14]!==_||n[15]!==y?(C=s==null&&y?i(t,{children:[r(o,{children:g}),r(c,{children:_})]}):null,n[12]=s,n[13]=g,n[14]=_,n[15]=y,n[16]=C):C=n[16];let w;return n[17]!==b||n[18]!==x||n[19]!==S||n[20]!==C?(w=i(`div`,{className:`tool-part__body`,css:f,children:[b,x,S,C]}),n[17]=b,n[18]=x,n[19]=S,n[20]=C,n[21]=w):w=n[21],w}function m(e){let t=(0,d.c)(27),{pending:a,snapshotToText:o,fileName:c,renderHeader:l,staleSessionMessage:f}=e,p=!!(a.accept&&a.reject),m;t[0]!==a||t[1]!==l?(m=l(a),t[0]=a,t[1]=l,t[2]=m):m=t[2];let h;t[3]===m?h=t[4]:(h=r(`div`,{className:`diff-accept-reject__header`,children:m}),t[3]=m,t[4]=h);let g;t[5]!==a.before||t[6]!==o?(g=o(a.before),t[5]=a.before,t[6]=o,t[7]=g):g=t[7];let _;t[8]!==a.after||t[9]!==o?(_=o(a.after),t[8]=a.after,t[9]=o,t[10]=_):_=t[10];let v;t[11]!==c||t[12]!==g||t[13]!==_?(v=r(u,{fileName:c,before:g,after:_}),t[11]=c,t[12]=g,t[13]=_,t[14]=v):v=t[14];let y,b;t[15]===a?(y=t[16],b=t[17]):(y=()=>void a.accept?.(),b=()=>void a.reject?.(),t[15]=a,t[16]=y,t[17]=b);let x=!p,S;t[18]!==f||t[19]!==y||t[20]!==b||t[21]!==x?(S=r(s,{onAccept:y,onReject:b,isDisabled:x,staleMessage:f}),t[18]=f,t[19]=y,t[20]=b,t[21]=x,t[22]=S):S=t[22];let C;return t[23]!==h||t[24]!==v||t[25]!==S?(C=i(n,{direction:`column`,gap:`size-100`,children:[h,v,S]}),t[23]=h,t[24]=v,t[25]=S,t[26]=C):C=t[26],C}export{p as DiffAcceptRejectToolDetails};