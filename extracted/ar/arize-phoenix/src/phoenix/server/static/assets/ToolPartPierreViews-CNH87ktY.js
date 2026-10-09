import{Xr as e,_s as t,hs as n}from"./vendor-streamdown-D5f7746Z.js";import{F as r}from"./contexts-DjI8XCgv.js";import{a as i,i as a,u as o}from"./vendor-shiki-CzKUVjZc.js";var s=t(),c=`
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
`,l=e`
  font-family: var(--global-font-family-sans);
  white-space: normal;
`,u={light:`pierre-light`,dark:`pierre-dark`};function d(e){let t=(0,s.c)(8),{fileName:a,contents:o}=e,{theme:d}=r(),f;t[0]!==o||t[1]!==a?(f={name:a,contents:o},t[0]=o,t[1]=a,t[2]=f):f=t[2];let p;t[3]===d?p=t[4]:(p={disableFileHeader:!0,theme:u,themeType:d,unsafeCSS:c},t[3]=d,t[4]=p);let m;return t[5]!==f||t[6]!==p?(m=n(`div`,{className:`tool-part-pierre-view`,css:l,children:n(i,{file:f,options:p})}),t[5]=f,t[6]=p,t[7]=m):m=t[7],m}function f(e){let t=(0,s.c)(9),{fileName:i,before:d,after:f}=e,{theme:p}=r(),m;t[0]!==f||t[1]!==d||t[2]!==i?(m=o({name:i,contents:d},{name:i,contents:f}),t[0]=f,t[1]=d,t[2]=i,t[3]=m):m=t[3];let h=m,g;t[4]===p?g=t[5]:(g={diffStyle:`unified`,disableFileHeader:!0,theme:u,themeType:p,unsafeCSS:c},t[4]=p,t[5]=g);let _;return t[6]!==h||t[7]!==g?(_=n(`div`,{className:`tool-part-pierre-view`,css:l,children:n(a,{fileDiff:h,"data-background":`transparent`,options:g})}),t[6]=h,t[7]=g,t[8]=_):_=t[8],_}export{f as ToolPartDiffView,d as ToolPartFileView};