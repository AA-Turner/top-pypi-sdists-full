"use strict";(globalThis.webpackChunksuperset=globalThis.webpackChunksuperset||[]).push([[6738],{51848:(e,t,n)=>{n.d(t,{U:()=>x});var l=n(17437),i=n(96453),r=n(95579),o=n(15595),s=n(96540),a=n(19129),d=n(98250),c=n(2445);const u=e=>l.AH`
  display: flex;
  font-size: ${e.typography.sizes.xl}px;
  font-weight: ${e.typography.weights.bold};
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;

  & .dynamic-title,
  & .dynamic-title-input {
    display: inline-block;
    max-width: 100%;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  & .dynamic-title {
    cursor: default;
  }
  & .dynamic-title-input {
    border: none;
    padding: 0;
    outline: none;

    &::placeholder {
      color: ${e.colors.grayscale.light1};
    }
  }

  & .input-sizer {
    position: absolute;
    left: -9999px;
    display: inline-block;
    white-space: pre;
  }
`,h=(0,s.memo)((({title:e,placeholder:t,onSave:n,canEdit:i,label:o})=>{const[h,p]=(0,s.useState)(!1),[g,f]=(0,s.useState)(e||""),m=(0,s.useRef)(null),[v,b]=(0,s.useState)(!1),{width:w,ref:y}=(0,d.uZ)(),{width:x,ref:D}=(0,d.uZ)({refreshMode:"debounce"});(0,s.useEffect)((()=>{f(e)}),[e]),(0,s.useEffect)((()=>{if(h&&null!=m&&m.current&&(m.current.focus(),m.current.setSelectionRange)){const{length:e}=m.current.value;m.current.setSelectionRange(e,e),m.current.scrollLeft=m.current.scrollWidth}}),[h]),(0,s.useLayoutEffect)((()=>{null!=y&&y.current&&(y.current.textContent=g||t)}),[g,t,y]),(0,s.useEffect)((()=>{m.current&&m.current.scrollWidth>m.current.clientWidth?b(!0):b(!1)}),[w,x]);const C=(0,s.useCallback)((()=>{i&&!h&&p(!0)}),[i,h]),S=(0,s.useCallback)((()=>{if(!i)return;const t=g.trim();f(t),e!==t&&n(t),p(!1)}),[i,g,n,e]),E=(0,s.useCallback)((e=>{i&&h&&f(e.target.value)}),[i,h]),R=(0,s.useCallback)((e=>{var t;i&&"Enter"===e.key&&(e.preventDefault(),null==(t=m.current)||t.blur())}),[i]);return(0,c.FD)("div",{css:u,ref:D,children:[(0,c.Y)(a.m_,{id:"title-tooltip",title:v&&g&&!h?g:null,children:i?(0,c.Y)("input",{className:"dynamic-title-input","aria-label":null!=o?o:(0,r.t)("Title"),ref:m,onChange:E,onBlur:S,onClick:C,onKeyPress:R,placeholder:t,value:g,css:l.AH`
                cursor: ${h?"text":"pointer"};

                ${w&&w>0&&l.AH`
                  width: ${w+1}px;
                `}
              `}):(0,c.Y)("span",{className:"dynamic-title","aria-label":null!=o?o:(0,r.t)("Title"),ref:m,children:g})}),(0,c.Y)("span",{ref:y,className:"input-sizer","aria-hidden":!0,tabIndex:-1})]})}));var p=n(58132),g=n(94704),f=n(12249),m=n(46920);const v=e=>l.AH`
  width: ${8*e.gridUnit}px;
  height: ${8*e.gridUnit}px;
  padding: 0;
  border: 1px solid ${e.colors.primary.dark2};

  &.antd5-btn > span.anticon {
    line-height: 0;
    transition: inherit;
  }

  &:hover:not(:focus) > span.anticon {
    color: ${e.colors.primary.light1};
  }
  &:focus-visible {
    outline: 2px solid ${e.colors.primary.dark2};
  }
`,b=e=>l.AH`
  display: flex;
  flex-direction: row;
  align-items: center;
  flex-wrap: nowrap;
  justify-content: space-between;
  background-color: ${e.colors.grayscale.light5};
  height: ${16*e.gridUnit}px;
  padding: 0 ${4*e.gridUnit}px;

  .editable-title {
    overflow: hidden;

    & > input[type='button'],
    & > span {
      overflow: hidden;
      text-overflow: ellipsis;
      max-width: 100%;
      white-space: nowrap;
    }
  }

  span[role='button'] {
    display: flex;
    height: 100%;
  }

  .title-panel {
    display: flex;
    align-items: center;
    min-width: 0;
    margin-right: ${12*e.gridUnit}px;
  }

  .right-button-panel {
    display: flex;
    align-items: center;
  }
`,w=e=>l.AH`
  display: flex;
  align-items: center;
  padding-left: ${2*e.gridUnit}px;

  & .fave-unfave-icon {
    padding: 0 ${e.gridUnit}px;

    &:first-of-type {
      padding-left: 0;
    }
  }
`,y=e=>l.AH`
  margin-left: ${2*e.gridUnit}px;
`,x=({editableTitleProps:e,showTitlePanelItems:t,certificatiedBadgeProps:n,showFaveStar:l,faveStarProps:s,titlePanelAdditionalItems:a,rightPanelAdditionalItems:d,additionalActionsMenu:u,menuDropdownProps:x,showMenuDropdown:D=!0,tooltipProps:C})=>{const S=(0,i.DP)();return(0,c.FD)("div",{css:b,className:"header-with-actions",children:[(0,c.FD)("div",{className:"title-panel",children:[(0,c.Y)(h,{...e}),t&&(0,c.FD)("div",{css:w,children:[(null==n?void 0:n.certifiedBy)&&(0,c.Y)(p.A,{...n}),l&&(0,c.Y)(g.A,{...s}),a]})]}),(0,c.FD)("div",{className:"right-button-panel",children:[d,(0,c.Y)("div",{css:y,children:D&&(0,c.Y)(o.rM,{trigger:["click"],overlay:u,...x,children:(0,c.Y)(m.A,{css:v,buttonStyle:"tertiary","aria-label":(0,r.t)("Menu actions trigger"),tooltip:null==C?void 0:C.text,placement:null==C?void 0:C.placement,children:(0,c.Y)(f.A.MoreHoriz,{iconColor:S.colors.primary.dark2,iconSize:"l"})})})})]})]})}},51003:(e,t,n)=>{n.d(t,{Kn:()=>x,un:()=>w,QS:()=>D,Ay:()=>A});var l=n(96540),i=n(58609),r=n(96453),o=n(95579),s=n(5362),a=n(17444);const d=(e,t,n)=>{let l=!1;const i=t-e;return i>0&&i<=n&&(l=!0),l};class c{constructor(e,t,n){this.tableRef=void 0,this.columnRef=void 0,this.setDerivedColumns=void 0,this.isDragging=void 0,this.resizable=void 0,this.reorderable=void 0,this.derivedColumns=void 0,this.RESIZE_INDICATOR_THRESHOLD=void 0,this.clearListeners=()=>{document.removeEventListener("mouseup",this.handleMouseup),this.initializeResizableColumns(!1,this.tableRef),this.initializeDragDropColumns(!1,this.tableRef)},this.setTableRef=e=>{this.tableRef=e},this.getColumnIndex=()=>{var e;let t=-1;const n=null==(e=this.columnRef)?void 0:e.parentNode;return n&&(t=Array.prototype.indexOf.call(n.children,this.columnRef)),t},this.handleColumnDragStart=e=>{var t;const n=null==e?void 0:e.currentTarget;n&&(this.columnRef=n),this.isDragging=!0;const l=this.getColumnIndex(),i={index:l,columnData:this.derivedColumns[l]};null==e||null==(t=e.dataTransfer)||t.setData(w,JSON.stringify(i))},this.handleDragDrop=e=>{var t;if(null==(t=e.dataTransfer)||null==t.getData?void 0:t.getData(w)){var n;e.preventDefault();const t=null==(n=e.currentTarget)?void 0:n.parentNode,l=Array.prototype.indexOf.call(t.children,e.currentTarget),i=this.getColumnIndex(),r=[...this.derivedColumns],o=r.slice(i,i+1);r.splice(i,1),r.splice(l,0,o[0]),this.derivedColumns=[...r],this.setDerivedColumns(r)}},this.allowDrop=e=>{e.preventDefault()},this.handleMouseDown=e=>{const t=null==e?void 0:e.currentTarget;t&&(this.columnRef=t,e&&d(e.offsetX,t.offsetWidth,this.RESIZE_INDICATOR_THRESHOLD)?(t.mouseDown=!0,t.oldX=e.x,t.oldWidth=t.offsetWidth,t.draggable=!1):this.reorderable&&(t.draggable=!0))},this.handleMouseMove=e=>{if(!0===this.resizable&&!this.isDragging){const t=e.currentTarget;e&&d(e.offsetX,t.offsetWidth,this.RESIZE_INDICATOR_THRESHOLD)?t.style.cursor="col-resize":t.style.cursor="default";const n=this.columnRef;if(null!=n&&n.mouseDown){let t=n.oldWidth;const l=e.x-n.oldX;n.oldWidth+(e.x-n.oldX)>0&&(t=n.oldWidth+l);const i=this.getColumnIndex();if(!Number.isNaN(i)){const e={...this.derivedColumns[i]};e.width=t,this.derivedColumns[i]=e,this.setDerivedColumns([...this.derivedColumns])}}}},this.handleMouseup=()=>{this.columnRef&&(this.columnRef.mouseDown=!1,this.columnRef.style.cursor="default",this.columnRef.draggable=!1),this.isDragging=!1},this.initializeResizableColumns=(e=!1,t)=>{var n,l;this.tableRef=t;const i=null==(n=this.tableRef)||null==(l=n.rows)?void 0:l[0];if(i){const{cells:t}=i,n=t.length;for(let l=0;l<n;l+=1){const n=t[l];!0===e?(this.resizable=!0,n.addEventListener("mousedown",this.handleMouseDown),n.addEventListener("mousemove",this.handleMouseMove,!0)):(this.resizable=!1,n.removeEventListener("mousedown",this.handleMouseDown),n.removeEventListener("mousemove",this.handleMouseMove,!0))}}},this.initializeDragDropColumns=(e=!1,t)=>{var n,l;this.tableRef=t;const i=null==(n=this.tableRef)||null==(l=n.rows)?void 0:l[0];if(i){const{cells:t}=i,n=t.length;for(let l=0;l<n;l+=1){const n=t[l];!0===e?(this.reorderable=!0,n.addEventListener("mousedown",this.handleMouseDown),n.addEventListener("dragover",this.allowDrop),n.addEventListener("dragstart",this.handleColumnDragStart),n.addEventListener("drop",this.handleDragDrop)):(this.reorderable=!1,n.draggable=!1,n.removeEventListener("mousedown",this.handleMouseDown),n.removeEventListener("dragover",this.allowDrop),n.removeEventListener("dragstart",this.handleColumnDragStart),n.removeEventListener("drop",this.handleDragDrop))}}},this.setDerivedColumns=n,this.tableRef=e,this.isDragging=!1,this.RESIZE_INDICATOR_THRESHOLD=8,this.resizable=!1,this.reorderable=!1,this.derivedColumns=[...t],document.addEventListener("mouseup",this.handleMouseup)}}var u=n(46942),h=n.n(u),p=n(98250),g=n(5373),f=n(58642),m=n(2445);const v=(0,r.I4)("div")((({theme:e,height:t})=>`\n  white-space: nowrap;\n  overflow: hidden;\n  text-overflow: ellipsis;\n  padding-left: ${2*e.gridUnit}px;\n  padding-right: ${e.gridUnit}px;\n  border-bottom: 1px solid ${e.colors.grayscale.light3};\n  transition: background 0.3s;\n  line-height: ${t}px;\n  box-sizing: border-box;\n`)),b=(0,r.I4)(i.A)((({theme:e})=>`\n    th.ant-table-cell {\n      font-weight: ${e.typography.weights.bold};\n      color: ${e.colors.grayscale.dark1};\n      white-space: nowrap;\n      overflow: hidden;\n      text-overflow: ellipsis;\n    }\n\n    .ant-pagination-item-active {\n      border-color: ${e.colors.primary.base};\n      }\n    }\n    .ant-table.ant-table-small {\n      font-size: ${e.typography.sizes.s}px;\n    }\n`)),w="superset/table-column";var y,x,D;!function(e){e.Disabled="disabled",e.Single="single",e.Multi="multi"}(y||(y={})),function(e){e.Paginate="paginate",e.Sort="sort",e.Filter="filter"}(x||(x={})),function(e){e.Small="small",e.Middle="middle"}(D||(D={}));const C=[],S=(0,r.I4)(i.A)((({theme:e,height:t})=>`\n    .ant-table-body {\n      overflow: auto;\n      height: ${t?`${t}px`:void 0};\n    }\n\n    th.ant-table-cell {\n      font-weight: ${e.typography.weights.bold};\n      color: ${e.colors.grayscale.dark1};\n      white-space: nowrap;\n      overflow: hidden;\n      text-overflow: ellipsis;\n    }\n\n    .ant-table-tbody > tr > td {\n      white-space: nowrap;\n      overflow: hidden;\n      text-overflow: ellipsis;\n      border-bottom: 1px solid ${e.colors.grayscale.light3};\n    }\n\n    .ant-pagination-item-active {\n      border-color: ${e.colors.primary.base};\n    }\n\n    .ant-table.ant-table-small {\n      font-size: ${e.typography.sizes.s}px;\n    }\n  `)),E=(0,r.I4)((e=>{var t;const{columns:n,pagination:i,onChange:o,height:s,scroll:a,size:d,allowHTML:c=!1}=e,[u,w]=(0,l.useState)(0),y=(0,l.useCallback)((e=>{w(e)}),[]),{ref:C}=(0,p.uZ)({onResize:y}),S=(0,r.DP)(),E=37*(null==S?void 0:S.gridUnit)||150,R=n.filter((({width:e})=>!e)).length;let T=0;null==n||n.forEach((e=>{e.width&&(T+=e.width)}));let z=0;const A=Math.max(Math.floor((u-T)/R),50),L=null!=(t=null==n||null==n.map?void 0:n.map((e=>{const t={...e};return e.width||(t.width=A),z+=t.width,t})))?t:[];if(z<u){const e=L[L.length-1];e.width=e.width+Math.floor(u-z)}const $=(0,l.useRef)(),[I]=(0,l.useState)((()=>{const e={};return Object.defineProperty(e,"scrollLeft",{get:()=>{var e,t;return $.current?null==(e=$.current)||null==(t=e.state)?void 0:t.scrollLeft:null},set:e=>{$.current&&$.current.scrollTo({scrollLeft:e})}}),e})),M=()=>{var e;null==(e=$.current)||e.resetAfterIndices({columnIndex:0,shouldForceUpdate:!0})};(0,l.useEffect)((()=>M),[u,n,d]);const N={...i,onChange:(e,t)=>{var n;null==(n=$.current)||null==n.scrollTo||n.scrollTo({scrollTop:0}),null==o||o({...i,current:e,pageSize:t},{},{},{action:x.Paginate,currentDataSource:[]})}};return(0,m.Y)("div",{ref:C,children:(0,m.Y)(b,{...e,sticky:!1,className:"virtual-table",columns:L,components:{body:(e,{ref:t,onScroll:n})=>{t.current=I;const l=d===D.Middle?47:39;return(0,m.Y)(g.cB,{ref:$,className:"virtual-grid",columnCount:L.length,columnWidth:e=>{const{width:t=E}=L[e];return t},height:s||a.y,rowCount:e.length,rowHeight:()=>l,width:u,onScroll:({scrollLeft:e})=>{n({scrollLeft:e})},children:({columnIndex:t,rowIndex:n,style:i})=>{var r,o;const s=null==e?void 0:e[n];let a=null==s?void 0:s[null==L||null==(r=L[t])?void 0:r.dataIndex];const d=null==(o=L[t])?void 0:o.render;return"function"==typeof d&&(a=d(a,s,n)),c&&"string"==typeof a&&(a=(0,f.nn)(a)),(0,m.Y)(v,{className:h()("virtual-table-cell",{"virtual-table-cell-last":t===L.length-1}),style:i,title:"string"==typeof a?a:void 0,theme:S,height:l,children:a})}})}},pagination:!!i&&N})})}))((({theme:e})=>`\n  .virtual-table .ant-table-container:before,\n  .virtual-table .ant-table-container:after {\n    display: none;\n  }\n  .virtual-table-cell {\n    box-sizing: border-box;\n    padding: ${4*e.gridUnit}px;\n    white-space: nowrap;\n    overflow: hidden;\n    text-overflow: ellipsis;\n  }\n`)),R={filterTitle:(0,o.t)("Filter menu"),filterConfirm:(0,o.t)("OK"),filterReset:(0,o.t)("Reset"),filterEmptyText:(0,o.t)("No filters"),filterCheckall:(0,o.t)("Select all items"),filterSearchPlaceholder:(0,o.t)("Search in filters"),emptyText:(0,o.t)("No data"),selectAll:(0,o.t)("Select current page"),selectInvert:(0,o.t)("Invert current page"),selectNone:(0,o.t)("Clear all data"),selectionAll:(0,o.t)("Select all data"),sortTitle:(0,o.t)("Sort"),expand:(0,o.t)("Expand row"),collapse:(0,o.t)("Collapse row"),triggerDesc:(0,o.t)("Click to sort descending"),triggerAsc:(0,o.t)("Click to sort ascending"),cancelSort:(0,o.t)("Click to cancel sorting")},T={[y.Multi]:"checkbox",[y.Single]:"radio",[y.Disabled]:null},z=()=>{},A=function(e){const{data:t,bordered:n,columns:i,selectedRows:o=C,handleRowSelection:d,size:u=D.Small,selectionType:h=y.Disabled,sticky:p=!0,loading:g=!1,resizable:f=!1,reorderable:v=!1,usePagination:b=!0,defaultPageSize:w=15,pageSizeOptions:x=["5","15","25","50","100"],hideData:A=!1,locale:L,height:$,virtualize:I=!1,onChange:M=z,recordCount:N,onRow:k,allowHTML:P=!1,childrenColumnName:H}=e,O=(0,l.useRef)(null),[Y,U]=(0,l.useState)(i),[F,W]=(0,l.useState)(w),[_,B]=(0,l.useState)({...R}),[X,Z]=(0,l.useState)(o),K=(0,l.useRef)(null),j=T[h],J={type:T[h],selectedRowKeys:X,onChange:e=>{Z(e),null==d||d(e)}};(0,l.useEffect)((()=>{!0===v&&s.A.warn('EXPERIMENTAL FEATURE ENABLED: The "reorderable" prop of Table is experimental and NOT recommended for use in production deployments.'),!0===f&&s.A.warn('EXPERIMENTAL FEATURE ENABLED: The "resizable" prop of Table is experimental and NOT recommended for use in production deployments.')}),[v,f]),(0,l.useEffect)((()=>{let e;e=L?{...R,...L}:{...R},B(e)}),[L]),(0,l.useEffect)((()=>U(i)),[i]),(0,l.useEffect)((()=>{var e,t;K.current&&(null==(t=K.current)||t.clearListeners());const n=null==(e=O.current)?void 0:e.getElementsByTagName("table")[0];var l,i;n&&(K.current=new c(n,Y,U),v&&(null==K||null==(l=K.current)||l.initializeDragDropColumns(v,n)),f&&(null==K||null==(i=K.current)||i.initializeResizableColumns(f,n)));return()=>{var e;null==K||null==(e=K.current)||null==e.clearListeners||e.clearListeners()}}),[O,v,f,I,K]);const Q=(0,r.DP)(),q=!!b&&{hideOnSinglePage:!0,pageSize:F,pageSizeOptions:x,onShowSizeChange:(e,t)=>W(t)};q&&N&&(q.total=N);let G=$;G&&(G-=68,b&&N&&N>F&&(G-=40));const V={loading:{spinning:null!=g&&g,indicator:(0,m.Y)(a.A,{})},hasData:!A&&t,columns:Y,dataSource:A?void 0:t,size:u,pagination:q,locale:_,showSorterTooltip:!1,onChange:M,onRow:k,theme:Q,height:G,bordered:n,expandable:{childrenColumnName:H}};return(0,m.FD)("div",{ref:O,children:[!I&&(0,m.Y)(S,{...V,rowSelection:null!==j?J:void 0,sticky:p}),I&&(0,m.Y)(E,{...V,scroll:{y:300,x:"100vw"},allowHTML:P})]})}}}]);