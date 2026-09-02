import{Go as e,Uo as t,qr as n}from"./vendor-streamdown-CXxPfHvi.js";import{N as r}from"./contexts-BP9urAJJ.js";import{a as i,i as a,u as o}from"./vendor-shiki-DWNyMZ4k.js";var s=e(),c=`
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
`,u={light:`pierre-light`,dark:`pierre-dark`};function d(e){let n=(0,s.c)(8),{fileName:a,contents:o}=e,{theme:d}=r(),f;n[0]!==o||n[1]!==a?(f={name:a,contents:o},n[0]=o,n[1]=a,n[2]=f):f=n[2];let p;n[3]===d?p=n[4]:(p={disableFileHeader:!0,theme:u,themeType:d,unsafeCSS:c},n[3]=d,n[4]=p);let m;return n[5]!==f||n[6]!==p?(m=t(`div`,{className:`tool-part-pierre-view`,css:l,children:t(i,{file:f,options:p})}),n[5]=f,n[6]=p,n[7]=m):m=n[7],m}function f(e){let n=(0,s.c)(9),{fileName:i,before:d,after:f}=e,{theme:p}=r(),m;n[0]!==f||n[1]!==d||n[2]!==i?(m=o({name:i,contents:d},{name:i,contents:f}),n[0]=f,n[1]=d,n[2]=i,n[3]=m):m=n[3];let h=m,g;n[4]===p?g=n[5]:(g={diffStyle:`unified`,disableFileHeader:!0,theme:u,themeType:p,unsafeCSS:c},n[4]=p,n[5]=g);let _;return n[6]!==h||n[7]!==g?(_=t(`div`,{className:`tool-part-pierre-view`,css:l,children:t(a,{fileDiff:h,"data-background":`transparent`,options:g})}),n[6]=h,n[7]=g,n[8]=_):_=n[8],_}export{f as ToolPartDiffView,d as ToolPartFileView};