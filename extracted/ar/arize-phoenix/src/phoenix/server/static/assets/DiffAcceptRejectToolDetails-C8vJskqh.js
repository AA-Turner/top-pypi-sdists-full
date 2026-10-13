import{U as e,Xr as t,_s as n,gs as r,hs as i,ms as a}from"./vendor-streamdown-CsHvRwzJ.js";import{i as o,n as s,r as c,t as l}from"./index-C9MXKM6e.js";import{ToolPartDiffView as u}from"./ToolPartPierreViews-5vXNAv_1.js";var d=n(),f=t`
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
`;function p(e){let t=(0,d.c)(22),{part:n,pending:s,snapshotToText:u,fileName:p,renderHeader:h,preparingLabel:g,preparingText:_,staleSessionMessage:v,showPreparing:y}=e,b;t[0]!==p||t[1]!==s||t[2]!==h||t[3]!==u||t[4]!==v?(b=s==null?null:i(m,{pending:s,snapshotToText:u,fileName:p,renderHeader:h,staleSessionMessage:v}),t[0]=p,t[1]=s,t[2]=h,t[3]=u,t[4]=v,t[5]=b):b=t[5];let x;t[6]!==n.output||t[7]!==n.state?(x=n.state===`output-available`?r(a,{children:[i(o,{children:`Result`}),i(c,{children:l(n.output)})]}):null,t[6]=n.output,t[7]=n.state,t[8]=x):x=t[8];let S;t[9]!==n.errorText||t[10]!==n.state?(S=n.state===`output-error`?r(a,{children:[i(o,{variant:`danger`,children:`Error`}),i(c,{children:n.errorText??``})]}):null,t[9]=n.errorText,t[10]=n.state,t[11]=S):S=t[11];let C;t[12]!==s||t[13]!==g||t[14]!==_||t[15]!==y?(C=s==null&&y?r(a,{children:[i(o,{children:g}),i(c,{children:_})]}):null,t[12]=s,t[13]=g,t[14]=_,t[15]=y,t[16]=C):C=t[16];let w;return t[17]!==b||t[18]!==x||t[19]!==S||t[20]!==C?(w=r(`div`,{className:`tool-part__body`,css:f,children:[b,x,S,C]}),t[17]=b,t[18]=x,t[19]=S,t[20]=C,t[21]=w):w=t[21],w}function m(t){let n=(0,d.c)(27),{pending:a,snapshotToText:o,fileName:c,renderHeader:l,staleSessionMessage:f}=t,p=!!(a.accept&&a.reject),m;n[0]!==a||n[1]!==l?(m=l(a),n[0]=a,n[1]=l,n[2]=m):m=n[2];let h;n[3]===m?h=n[4]:(h=i(`div`,{className:`diff-accept-reject__header`,children:m}),n[3]=m,n[4]=h);let g;n[5]!==a.before||n[6]!==o?(g=o(a.before),n[5]=a.before,n[6]=o,n[7]=g):g=n[7];let _;n[8]!==a.after||n[9]!==o?(_=o(a.after),n[8]=a.after,n[9]=o,n[10]=_):_=n[10];let v;n[11]!==c||n[12]!==g||n[13]!==_?(v=i(u,{fileName:c,before:g,after:_}),n[11]=c,n[12]=g,n[13]=_,n[14]=v):v=n[14];let y,b;n[15]===a?(y=n[16],b=n[17]):(y=()=>void a.accept?.(),b=()=>void a.reject?.(),n[15]=a,n[16]=y,n[17]=b);let x=!p,S;n[18]!==f||n[19]!==y||n[20]!==b||n[21]!==x?(S=i(s,{onAccept:y,onReject:b,isDisabled:x,staleMessage:f}),n[18]=f,n[19]=y,n[20]=b,n[21]=x,n[22]=S):S=n[22];let C;return n[23]!==h||n[24]!==v||n[25]!==S?(C=r(e,{direction:`column`,gap:`size-100`,children:[h,v,S]}),n[23]=h,n[24]=v,n[25]=S,n[26]=C):C=n[26],C}export{p as DiffAcceptRejectToolDetails};