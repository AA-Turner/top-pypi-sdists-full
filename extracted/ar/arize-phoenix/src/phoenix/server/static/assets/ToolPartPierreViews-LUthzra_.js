import{Cs as e,Ts as t,ii as n}from"./vendor-streamdown-6L0QmST3.js";import{F as r,I as i,Yt as a}from"./vendor-CZKEknT1.js";import{I as o}from"./contexts-CHfLnjjx.js";var s=t(),c=`
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
`,l=n`
  font-family: var(--global-font-family-sans);
  white-space: normal;
`,u={light:`pierre-light`,dark:`pierre-dark`};function d(t){let n=(0,s.c)(8),{fileName:r,contents:a}=t,{theme:d}=o(),f;n[0]!==a||n[1]!==r?(f={name:r,contents:a},n[0]=a,n[1]=r,n[2]=f):f=n[2];let p;n[3]===d?p=n[4]:(p={disableFileHeader:!0,theme:u,themeType:d,unsafeCSS:c},n[3]=d,n[4]=p);let m;return n[5]!==f||n[6]!==p?(m=e(`div`,{className:`tool-part-pierre-view`,css:l,children:e(i,{file:f,options:p})}),n[5]=f,n[6]=p,n[7]=m):m=n[7],m}function f(t){let n=(0,s.c)(9),{fileName:i,before:d,after:f}=t,{theme:p}=o(),m;n[0]!==f||n[1]!==d||n[2]!==i?(m=a({name:i,contents:d},{name:i,contents:f}),n[0]=f,n[1]=d,n[2]=i,n[3]=m):m=n[3];let h=m,g;n[4]===p?g=n[5]:(g={diffStyle:`unified`,disableFileHeader:!0,theme:u,themeType:p,unsafeCSS:c},n[4]=p,n[5]=g);let _;return n[6]!==h||n[7]!==g?(_=e(`div`,{className:`tool-part-pierre-view`,css:l,children:e(r,{fileDiff:h,"data-background":`transparent`,options:g})}),n[6]=h,n[7]=g,n[8]=_):_=n[8],_}export{f as ToolPartDiffView,d as ToolPartFileView};