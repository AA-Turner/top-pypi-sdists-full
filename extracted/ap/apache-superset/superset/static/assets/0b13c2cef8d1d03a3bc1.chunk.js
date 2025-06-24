"use strict";(globalThis.webpackChunksuperset=globalThis.webpackChunksuperset||[]).push([[217],{47251:(n,e,l)=>{l.d(e,{A:()=>p});var i=l(96453),o=l(46942),a=l.n(o),t=l(2445);const r=i.I4.ul`
  display: inline-block;
  margin: 16px 0;
  padding: 0;

  li {
    display: inline;
    margin: 0 4px;

    span {
      padding: 8px 12px;
      text-decoration: none;
      background-color: ${({theme:n})=>n.colors.grayscale.light5};
      border-radius: ${({theme:n})=>n.borderRadius}px;

      &:hover,
      &:focus {
        z-index: 2;
        color: ${({theme:n})=>n.colors.grayscale.dark1};
        background-color: ${({theme:n})=>n.colors.grayscale.light3};
      }
    }

    &.disabled {
      span {
        background-color: transparent;
        cursor: default;

        &:focus {
          outline: none;
        }
      }
    }
    &.active {
      span {
        z-index: 3;
        color: ${({theme:n})=>n.colors.grayscale.light5};
        cursor: default;
        background-color: ${({theme:n})=>n.colors.primary.base};

        &:focus {
          outline: none;
        }
      }
    }
  }
`;function s({children:n}){return(0,t.Y)(r,{role:"navigation",children:n})}s.Next=function({disabled:n,onClick:e}){return(0,t.Y)("li",{className:a()({disabled:n}),children:(0,t.Y)("span",{role:"button",tabIndex:n?-1:0,onClick:l=>{l.preventDefault(),n||e(l)},children:"»"})})},s.Prev=function({disabled:n,onClick:e}){return(0,t.Y)("li",{className:a()({disabled:n}),children:(0,t.Y)("span",{role:"button",tabIndex:n?-1:0,onClick:l=>{l.preventDefault(),n||e(l)},children:"«"})})},s.Item=function({active:n,children:e,onClick:l}){return(0,t.Y)("li",{className:a()({active:n}),children:(0,t.Y)("span",{role:"button",tabIndex:n?-1:0,onClick:e=>{e.preventDefault(),n||l(e)},children:e})})},s.Ellipsis=function({disabled:n,onClick:e}){return(0,t.Y)("li",{className:a()({disabled:n}),children:(0,t.Y)("span",{role:"button",tabIndex:n?-1:0,onClick:l=>{l.preventDefault(),n||e(l)},children:"…"})})};const c=s;var d=l(18575);const p=(0,d.uv)({WrapperComponent:c,itemTypeToComponent:{[d.w$.PAGE]:({value:n,isActive:e,onClick:l})=>(0,t.Y)(c.Item,{active:e,onClick:l,children:n}),[d.w$.ELLIPSIS]:({isActive:n,onClick:e})=>(0,t.Y)(c.Ellipsis,{disabled:n,onClick:e}),[d.w$.PREVIOUS_PAGE_LINK]:({isActive:n,onClick:e})=>(0,t.Y)(c.Prev,{disabled:n,onClick:e}),[d.w$.NEXT_PAGE_LINK]:({isActive:n,onClick:e})=>(0,t.Y)(c.Next,{disabled:n,onClick:e}),[d.w$.FIRST_PAGE_LINK]:()=>null,[d.w$.LAST_PAGE_LINK]:()=>null}})},73204:(n,e,l)=>{l.d(e,{A:()=>d});var i=l(96540),o=l(46942),a=l.n(o),t=l(96453),r=l(12249),s=l(2445);const c=t.I4.table`
  ${({theme:n})=>`\n    background-color: ${n.colors.grayscale.light5};\n    border-collapse: separate;\n    border-radius: ${n.borderRadius}px;\n\n    thead > tr > th {\n      border: 0;\n    }\n\n    tbody {\n      tr:first-of-type > td {\n        border-top: 0;\n      }\n    }\n    th {\n      background: ${n.colors.grayscale.light5};\n      position: sticky;\n      top: 0;\n\n      &:first-of-type {\n        padding-left: ${4*n.gridUnit}px;\n      }\n\n      &.xs {\n        min-width: 25px;\n      }\n      &.sm {\n        min-width: 50px;\n      }\n      &.md {\n        min-width: 75px;\n      }\n      &.lg {\n        min-width: 100px;\n      }\n      &.xl {\n        min-width: 150px;\n      }\n      &.xxl {\n        min-width: 200px;\n      }\n\n      span {\n        white-space: nowrap;\n        display: flex;\n        align-items: center;\n        line-height: 2;\n      }\n\n      svg {\n        display: inline-block;\n        position: relative;\n      }\n    }\n\n    td {\n      &.xs {\n        width: 25px;\n      }\n      &.sm {\n        width: 50px;\n      }\n      &.md {\n        width: 75px;\n      }\n      &.lg {\n        width: 100px;\n      }\n      &.xl {\n        width: 150px;\n      }\n      &.xxl {\n        width: 200px;\n      }\n    }\n\n    .table-cell-loader {\n      position: relative;\n\n      .loading-bar {\n        background-color: ${n.colors.secondary.light4};\n        border-radius: 7px;\n\n        span {\n          visibility: hidden;\n        }\n      }\n\n      .empty-loading-bar {\n        display: inline-block;\n        width: 100%;\n        height: 1.2em;\n      }\n    }\n\n    .actions {\n      white-space: nowrap;\n      min-width: 100px;\n\n      svg,\n      i {\n        margin-right: 8px;\n\n        &:hover {\n          path {\n            fill: ${n.colors.primary.base};\n          }\n        }\n      }\n    }\n\n    .table-row {\n      .actions {\n        opacity: 0;\n        font-size: ${n.typography.sizes.xl}px;\n        display: flex;\n      }\n\n      &:hover {\n        background-color: ${n.colors.secondary.light5};\n\n        .actions {\n          opacity: 1;\n          transition: opacity ease-in ${n.transitionTiming}s;\n        }\n      }\n    }\n\n    .table-row-selected {\n      background-color: ${n.colors.secondary.light4};\n\n      &:hover {\n        background-color: ${n.colors.secondary.light4};\n      }\n    }\n\n    .table-cell {\n      font-feature-settings: 'tnum' 1;\n      text-overflow: ellipsis;\n      overflow: hidden;\n      max-width: 320px;\n      line-height: 1;\n      vertical-align: middle;\n      &:first-of-type {\n        padding-left: ${4*n.gridUnit}px;\n      }\n      &__wrap {\n        white-space: normal;\n      }\n      &__nowrap {\n        white-space: nowrap;\n      }\n    }\n\n    @keyframes loading-shimmer {\n      40% {\n        background-position: 100% 0;\n      }\n\n      100% {\n        background-position: 100% 0;\n      }\n    }\n  `}
`;c.displayName="table";const d=(0,i.memo)((({getTableProps:n,getTableBodyProps:e,prepareRow:l,headerGroups:i,columns:o,rows:t,loading:d,highlightRowId:p,columnsForWrapText:g})=>(0,s.FD)(c,{...n(),className:"table table-hover",children:[(0,s.Y)("thead",{children:i.map((n=>(0,s.Y)("tr",{...n.getHeaderGroupProps(),children:n.headers.map((n=>{let e=(0,s.Y)(r.A.Sort,{});return n.isSorted&&n.isSortedDesc?e=(0,s.Y)(r.A.SortDesc,{}):n.isSorted&&!n.isSortedDesc&&(e=(0,s.Y)(r.A.SortAsc,{})),n.hidden?null:(0,s.Y)("th",{...n.getHeaderProps(n.canSort?n.getSortByToggleProps():{}),className:a()({[n.size||""]:n.size}),children:(0,s.FD)("span",{children:[n.render("Header"),n.canSort&&e]})})}))})))}),(0,s.FD)("tbody",{...e(),children:[d&&0===t.length&&[...new Array(12)].map(((n,e)=>(0,s.Y)("tr",{children:o.map(((n,e)=>n.hidden?null:(0,s.Y)("td",{className:a()("table-cell",{"table-cell-loader":d}),children:(0,s.Y)("span",{className:"loading-bar empty-loading-bar",role:"progressbar","aria-label":"loading"})},e)))},e))),t.length>0&&t.map((n=>{l(n);const e=n.original.id;return(0,s.Y)("tr",{...n.getRowProps(),className:a()("table-row",{"table-row-selected":n.isSelected||void 0!==e&&e===p}),children:n.cells.map((n=>{if(n.column.hidden)return null;const e=n.column.cellProps||{},l=null==g?void 0:g.includes(n.column.Header);return(0,s.Y)("td",{className:a()("table-cell table-cell__"+(l?"wrap":"nowrap"),{"table-cell-loader":d,[n.column.size||""]:n.column.size}),...n.getCellProps(),...e,children:(0,s.Y)("span",{className:a()({"loading-bar":d}),role:d?"progressbar":void 0,children:(0,s.Y)("span",{children:n.render("Cell")})})})}))})}))]})]})))},54016:(n,e,l)=>{l.d(e,{A:()=>y,V:()=>i});var i,o=l(2404),a=l.n(o),t=l(96540),r=l(96453),s=l(95579),c=l(32885),d=l(641),p=l(47251),g=l(73204),h=l(2445);!function(n){n.Default="Default",n.Small="Small"}(i||(i={}));const u=r.I4.div`
  margin: ${({theme:n})=>40*n.gridUnit}px 0;
`,m=r.I4.div`
  ${({scrollTable:n,theme:e})=>n&&`\n    flex: 1 1 auto;\n    margin-bottom: ${4*e.gridUnit}px;\n    overflow: auto;\n  `}

  .table-row {
    ${({theme:n,small:e})=>!e&&`height: ${11*n.gridUnit-1}px;`}

    .table-cell {
      ${({theme:n,small:e})=>e&&`\n        padding-top: ${n.gridUnit+1}px;\n        padding-bottom: ${n.gridUnit+1}px;\n        line-height: 1.45;\n      `}
    }
  }

  th[role='columnheader'] {
    z-index: 1;
    border-bottom: ${({theme:n})=>`${n.gridUnit-2}px solid ${n.colors.grayscale.light2}`};
    ${({small:n})=>n&&"padding-bottom: 0;"}
  }
`,b=r.I4.div`
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background-color: ${({theme:n})=>n.colors.grayscale.light5};

  ${({isPaginationSticky:n})=>n&&"\n        position: sticky;\n        bottom: 0;\n        left: 0;\n    "};

  .row-count-container {
    margin-top: ${({theme:n})=>2*n.gridUnit}px;
    color: ${({theme:n})=>n.colors.grayscale.base};
  }
`,x=({columns:n,data:e,pageSize:l,totalCount:o=e.length,initialPageIndex:r,initialSortBy:x=[],loading:y=!1,withPagination:w=!0,emptyWrapperType:f=i.Default,noDataText:v,showRowCount:k=!0,serverPagination:$=!1,columnsForWrapText:P,onServerPagination:S=()=>{},scrollTopOnPagination:Y=!1,...I})=>{const C={pageSize:null!=l?l:10,pageIndex:null!=r?r:0,sortBy:x},{getTableProps:A,getTableBodyProps:T,headerGroups:N,page:E,rows:D,prepareRow:_,pageCount:F,gotoPage:z,state:{pageIndex:R,pageSize:B,sortBy:G}}=(0,c.useTable)({columns:n,data:e,initialState:C,manualPagination:$,manualSortBy:$,pageCount:Math.ceil(o/C.pageSize)},c.useFilters,c.useSortBy,c.usePagination),L=w?E:D;let U;switch(f){case i.Small:U=({children:n})=>(0,h.Y)(h.FK,{children:n});break;case i.Default:default:U=({children:n})=>(0,h.Y)(u,{children:n})}const K=!y&&0===L.length,M=F>1&&w,W=(0,t.useRef)(null);return(0,t.useEffect)((()=>{$&&R!==C.pageIndex&&S({pageIndex:R})}),[R]),(0,t.useEffect)((()=>{$&&!a()(G,C.sortBy)&&S({pageIndex:0,sortBy:G})}),[G]),(0,h.FD)(h.FK,{children:[(0,h.FD)(m,{...I,ref:W,children:[(0,h.Y)(g.A,{getTableProps:A,getTableBodyProps:T,prepareRow:_,headerGroups:N,rows:L,columns:n,loading:y,columnsForWrapText:P}),K&&(0,h.Y)(U,{children:v?(0,h.Y)(d.S,{image:d.S.PRESENTED_IMAGE_SIMPLE,description:v}):(0,h.Y)(d.S,{image:d.S.PRESENTED_IMAGE_SIMPLE})})]}),M&&(0,h.FD)(b,{className:"pagination-container",isPaginationSticky:I.isPaginationSticky,children:[(0,h.Y)(p.A,{totalPages:F||0,currentPage:F?R+1:0,onChange:n=>(n=>{var e;Y&&(null==W||null==(e=W.current)||e.scroll(0,0)),z(n)})(n-1),hideFirstAndLastPageLinks:!0}),k&&(0,h.Y)("div",{className:"row-count-container",children:!y&&(0,s.t)("%s-%s of %s",B*R+(E.length&&1),B*R+E.length,o)})]})]})},y=(0,t.memo)(x)},50217:(n,e,l)=>{l.d(e,{A:()=>i.A,V:()=>i.V});var i=l(54016)}}]);