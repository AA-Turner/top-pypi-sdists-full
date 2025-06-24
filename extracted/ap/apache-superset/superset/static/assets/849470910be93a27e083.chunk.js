"use strict";(globalThis.webpackChunksuperset=globalThis.webpackChunksuperset||[]).push([[2246],{17613:(e,t,n)=>{var a=n(24994).default;Object.defineProperty(t,"__esModule",{value:!0}),t.default=function e(t){var n=arguments.length>1&&void 0!==arguments[1]?arguments[1]:{},a=[];return r.default.Children.forEach(t,(function(t){(null!=t||n.keepEmpty)&&(Array.isArray(t)?a=a.concat(e(t)):(0,i.default)(t)&&t.props?a=a.concat(e(t.props.children,n)):a.push(t))})),a};var i=a(n(13077)),r=a(n(96540))},14773:(e,t,n)=>{var a=n(6305).default;Object.defineProperty(t,"__esModule",{value:!0}),t.default=function(e){var t=i.useRef();return t.current=e,i.useCallback((function(){for(var e,n=arguments.length,a=new Array(n),i=0;i<n;i++)a[i]=arguments[i];return null===(e=t.current)||void 0===e?void 0:e.call.apply(e,[t].concat(a))}),[])};var i=a(n(96540))},34482:(e,t,n)=>{var a=n(24994).default,i=n(6305).default;Object.defineProperty(t,"__esModule",{value:!0}),t.useLayoutUpdateEffect=t.default=void 0;var r=i(n(96540)),l=(0,a(n(83477)).default)()?r.useLayoutEffect:r.useEffect,o=function(e,t){var n=r.useRef(!0);l((function(){return e(n.current)}),t),l((function(){return n.current=!1,function(){n.current=!0}}),[])};t.useLayoutUpdateEffect=function(e,t){o((function(t){if(!t)return e()}),t)},t.default=o},96680:(e,t,n)=>{var a=n(24994).default;Object.defineProperty(t,"__esModule",{value:!0}),t.default=function(e,t){var n=t||{},a=n.defaultValue,d=n.value,c=n.onChange,u=n.postState,h=(0,o.default)((function(){return s(d)?d:s(a)?"function"==typeof a?a():a:"function"==typeof e?e():e})),g=(0,i.default)(h,2),p=g[0],m=g[1],f=void 0!==d?d:p,b=u?u(f):f,v=(0,r.default)(c),y=(0,o.default)([f]),x=(0,i.default)(y,2),$=x[0],w=x[1];return(0,l.useLayoutUpdateEffect)((function(){var e=$[0];p!==e&&v(p,e)}),[$]),(0,l.useLayoutUpdateEffect)((function(){s(d)||m(d)}),[d]),[b,(0,r.default)((function(e,t){m(e,t),w([f],t)}))]};var i=a(n(85715)),r=a(n(14773)),l=n(34482),o=a(n(43312));function s(e){return void 0!==e}},43312:(e,t,n)=>{var a=n(6305).default,i=n(24994).default;Object.defineProperty(t,"__esModule",{value:!0}),t.default=function(e){var t=l.useRef(!1),n=l.useState(e),a=(0,r.default)(n,2),i=a[0],o=a[1];return l.useEffect((function(){return t.current=!1,function(){t.current=!0}}),[]),[i,function(e,n){n&&t.current||o(e)}]};var r=i(n(85715)),l=a(n(96540))},47163:(e,t,n)=>{n.d(t,{A:()=>i});var a=n(96540);const i=()=>{const[e,t]=(0,a.useState)(0),[n,i]=(0,a.useState)(!1),r=(0,a.useRef)(null),l=(0,a.useRef)(null);return(0,a.useLayoutEffect)((()=>{var e;const n=()=>{const e=r.current;if(!e)return;const n=l.current,{scrollWidth:a,clientWidth:o,childNodes:s}=e;if(a>o){const e=6,a=(null==n?void 0:n.offsetWidth)||0,r=o-e,l=s.length;let d=0,c=0;for(let e=0;e<l;e+=1)r-d-a<=0&&(c+=1),d+=s[e].offsetWidth;l>1&&c?(i(!0),t(c)):(i(!1),t(1))}else i(!1),t(0)},a=new ResizeObserver(n),o=null==(e=r.current)?void 0:e.parentElement;return o&&a.observe(o),n(),()=>{a.disconnect()}}),[l.current]),[r,l,e,n]}},41621:(e,t,n)=>{n.d(t,{A:()=>d});var a=n(33149),i=n(96453),r=n(96540),l=n(62221),o=n(2445);const s=i.I4.div`
  position: absolute;
  height: 100%;

  :hover .sidebar-resizer::after {
    background-color: ${({theme:e})=>e.colors.primary.base};
  }

  .sidebar-resizer {
    // @z-index-above-sticky-header (100) + 1 = 101
    z-index: 101;
  }

  .sidebar-resizer::after {
    display: block;
    content: '';
    width: 1px;
    height: 100%;
    margin: 0 auto;
  }
`,d=({id:e,initialWidth:t,minWidth:n,maxWidth:i,enable:d,children:c})=>{const[u,h]=function(e,t){const n=(0,r.useRef)(),[a,i]=(0,r.useState)(t);return(0,r.useEffect)((()=>{var t;n.current=null!=(t=n.current)?t:(0,l.Gq)(l.Hh.CommonResizableSidebarWidths,{}),n.current[e]&&i(n.current[e])}),[e]),[a,function(t){i(t),(0,l.SO)(l.Hh.CommonResizableSidebarWidths,{...n.current,[e]:t})}]}(e,t);return(0,o.FD)(o.FK,{children:[(0,o.Y)(s,{children:(0,o.Y)(a.c,{enable:{right:d},handleClasses:{right:"sidebar-resizer",bottom:"hidden",bottomRight:"hidden",bottomLeft:"hidden"},size:{width:u,height:"100%"},minWidth:n,maxWidth:i,onResizeStop:(e,t,n,a)=>h(u+a.width)})}),c(u)]})}},78704:(e,t,n)=>{n.d(t,{A:()=>d});var a=n(17437),i=n(96453),r=n(16784),l=n(12249),o=n(19129),s=n(2445);const d=function({warningMarkdown:e,size:t,marginRight:n}){const d=(0,i.DP)();return(0,s.Y)(o.m_,{id:"warning-tooltip",title:(0,s.Y)(r.A,{source:e}),children:(0,s.Y)(l.A.AlertSolid,{iconColor:d.colors.warning.base,iconSize:t,css:(0,a.AH)({marginRight:null!=n?n:2*d.gridUnit},"","")})})}},29130:(e,t,n)=>{n.r(t),n.d(t,{datasetReducer:()=>rt,default:()=>ot});var a=n(96540),i=n(61574),r=n(35742),l=n(95579),o=n(5362),s=n(58561),d=n.n(s),c=n(95272);const u=(e,t)=>{const[n,i]=(0,a.useState)([]),s=t?encodeURIComponent(t):void 0,u=(0,a.useCallback)((async e=>{let t,n=[],a=0;for(;void 0===t||n.length<t;){const i=d().encode_uri({filters:e,page:a});try{const e=await r.A.get({endpoint:`/api/v1/dataset/?q=${i}`});({count:t}=e.json);const{json:{result:l}}=e;n=[...n,...l],a+=1}catch(e){(0,c.iB)((0,l.t)("There was an error fetching dataset")),o.A.error((0,l.t)("There was an error fetching dataset"),e)}}i(n)}),[]);(0,a.useEffect)((()=>{const n=[{col:"database",opr:"rel_o_m",value:null==e?void 0:e.id},{col:"schema",opr:"eq",value:s},{col:"sql",opr:"dataset_is_null_or_empty",value:!0}];t&&u(n)}),[null==e?void 0:e.id,t,s,u]);const h=(0,a.useMemo)((()=>null==n?void 0:n.map((e=>e.table_name))),[n]);return{datasets:n,datasetNames:h}};var h,g=n(51848),p=n(46920),m=n(12249),f=n(6749);!function(e){e[e.SelectDatabase=0]="SelectDatabase",e[e.SelectCatalog=1]="SelectCatalog",e[e.SelectSchema=2]="SelectSchema",e[e.SelectTable=3]="SelectTable",e[e.ChangeDataset=4]="ChangeDataset"}(h||(h={}));var b=n(96453),v=n(17437);const y=b.I4.div`
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  background-color: ${({theme:e})=>e.colors.grayscale.light5};
`,x=b.I4.div`
  width: ${({theme:e,width:t})=>null!=t?t:80*e.gridUnit}px;
  max-width: ${({theme:e,width:t})=>null!=t?t:80*e.gridUnit}px;
  flex-direction: column;
  flex: 1 0 auto;
`,$=b.I4.div`
  display: flex;
  flex-direction: column;
  flex-grow: 1;
`,w=b.I4.div`
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: row;
`,_=(0,b.I4)(w)`
  flex: 1 0 auto;
  position: relative;
`,S=(0,b.I4)(w)`
  flex: 1 0 auto;
  height: auto;
`,U=(0,b.I4)(w)`
  flex: 0 0 auto;
  height: ${({theme:e})=>16*e.gridUnit}px;
  z-index: 0;
`,Y=b.I4.div`
  ${({theme:e})=>`\n  flex: 0 0 auto;\n  height: ${16*e.gridUnit}px;\n  border-bottom: 2px solid ${e.colors.grayscale.light2};\n\n  .header-with-actions {\n    height: ${15.5*e.gridUnit}px;\n  }\n  `}
`,I=b.I4.div`
  ${({theme:e})=>`\n  margin: ${4*e.gridUnit}px;\n  font-size: ${e.typography.sizes.xl}px;\n  font-weight: ${e.typography.weights.bold};\n  `}
`,C=b.I4.div`
  ${({theme:e})=>`\n  height: 100%;\n  border-right: 1px solid ${e.colors.grayscale.light2};\n  `}
`,T=b.I4.div`
  width: 100%;
  position: relative;
`,A=b.I4.div`
  ${({theme:e})=>`\n  border-left: 1px solid ${e.colors.grayscale.light2};\n  color: ${e.colors.success.base};\n  `}
`,D=b.I4.div`
  ${({theme:e})=>`\n  height: ${16*e.gridUnit}px;\n  width: 100%;\n  border-top: 1px solid ${e.colors.grayscale.light2};\n  border-bottom: 1px solid ${e.colors.grayscale.light2};\n  color: ${e.colors.info.base};\n  border-top: ${e.gridUnit/4}px solid\n    ${e.colors.grayscale.light2};\n  padding: ${4*e.gridUnit}px;\n  display: flex;\n  justify-content: flex-end;\n  background-color: ${e.colors.grayscale.light5};\n  z-index: ${e.zIndex.max}\n  `}
`,k=b.I4.div`
  .antd5-btn {
    span {
      margin-right: 0;
    }

    &:disabled {
      svg {
        color: ${({theme:e})=>e.colors.grayscale.light1};
      }
    }
  }
`,E=e=>v.AH`
  width: ${21.5*e.gridUnit}px;

  &:disabled {
    background-color: ${e.colors.grayscale.light3};
    color: ${e.colors.grayscale.light1};
  }
`;var z=n(2445);const F=(0,l.t)("New dataset"),P={text:(0,l.t)("Select a database table and create dataset"),placement:"bottomRight"},N=()=>(0,z.FD)(p.A,{buttonStyle:"primary",tooltip:null==P?void 0:P.text,placement:null==P?void 0:P.placement,disabled:!0,css:E,children:[(0,z.Y)(m.A.Save,{iconSize:"m"}),(0,l.t)("Save")]}),R=()=>(0,z.FD)(f.W1,{children:[(0,z.Y)(f.W1.Item,{children:(0,l.t)("Settings")}),(0,z.Y)(f.W1.Item,{children:(0,l.t)("Delete")})]});function L({setDataset:e,title:t=F,editing:n=!1}){const a={title:null!=t?t:F,placeholder:F,onSave:t=>{e({type:h.ChangeDataset,payload:{name:"dataset_name",value:t}})},canEdit:!1,label:(0,l.t)("dataset name")};return(0,z.Y)(k,{children:n?(0,z.Y)(g.U,{editableTitleProps:a,showTitlePanelItems:!1,showFaveStar:!1,faveStarProps:{itemId:1,saveFaveStar:()=>{}},titlePanelAdditionalItems:(0,z.Y)(z.FK,{}),rightPanelAdditionalItems:N(),additionalActionsMenu:R(),menuDropdownProps:{disabled:!0},tooltipProps:P}):(0,z.Y)(I,{children:t||F})})}var j=n(69945),M=n(48327),O=n(71519),W=n(62952),K=n(51003),q=n(50455),H=n(46e3),B=n(5261),V=n(50500),X=n(39854),Q=n(7089),G=n(47163),J=n(19129);const Z=b.I4.div`
  & > span {
    width: 100%;
    display: flex;

    .antd5-tooltip-open {
      display: inline;
    }
  }
`,ee=b.I4.span`
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  display: inline-block;
  width: 100%;
  vertical-align: bottom;
`,te=b.I4.span`
  &:not(:last-child)::after {
    content: ', ';
  }
`,ne=b.I4.div`
  .link {
    color: ${({theme:e})=>e.colors.grayscale.light5};
    display: block;
    text-decoration: underline;
  }
`,ae=b.I4.span`
  ${({theme:e})=>`\n  cursor: pointer;\n  color: ${e.colors.primary.dark1};\n  font-weight: ${e.typography.weights.normal};\n  `}
`;function ie({items:e,renderVisibleItem:t=e=>e,renderTooltipItem:n=e=>e,getKey:i=e=>e,maxLinks:r=20}){const[o,s,d,c]=(0,G.A)(),u=(0,a.useMemo)((()=>e.length>r?e.length-r:void 0),[e,r]),h=(0,a.useMemo)((()=>(0,z.Y)(ee,{ref:o,children:e.map((e=>(0,z.Y)(te,{children:t(e)},i(e))))})),[i,e,t]),g=(0,a.useMemo)((()=>e.slice(0,r).map((e=>(0,z.Y)(ne,{children:n(e)},i(e))))),[i,e,r,n]);return(0,z.Y)(Z,{children:(0,z.FD)(J.m_,{placement:"top",title:d?(0,z.FD)(z.FK,{children:[g,u&&(0,z.Y)("span",{children:(0,l.t)("+ %s more",u)})]}):null,children:[h,c&&(0,z.FD)(ae,{ref:s,children:["+",d]})]})})}const re=e=>({key:e.id,to:`/superset/dashboard/${e.id}`,target:"_blank",rel:"noreferer noopener",children:e.dashboard_title}),le=e=>v.AH`
  color: ${e.colors.grayscale.light5};
  text-decoration: underline;
  &:hover {
    color: inherit;
  }
`,oe=[{key:"slice_name",title:(0,l.t)("Chart"),width:"320px",sorter:!0,render:(e,t)=>(0,z.Y)(O.N_,{to:t.url,children:t.slice_name})},{key:"owners",title:(0,l.t)("Chart owners"),width:"242px",render:(e,t)=>{var n,a;return(0,z.Y)(ie,{items:null!=(n=null==(a=t.owners)?void 0:a.map((e=>`${e.first_name} ${e.last_name}`)))?n:[]})}},{key:"last_saved_at",title:(0,l.t)("Chart last modified"),width:"209px",sorter:!0,defaultSortOrder:"descend",render:(e,t)=>t.last_saved_at?Q.XV.utc(t.last_saved_at).fromNow():null},{key:"last_saved_by.first_name",title:(0,l.t)("Chart last modified by"),width:"216px",sorter:!0,render:(e,t)=>t.last_saved_by?`${t.last_saved_by.first_name} ${t.last_saved_by.last_name}`:null},{key:"dashboards",title:(0,l.t)("Dashboard usage"),width:"420px",render:(e,t)=>(0,z.Y)(ie,{items:t.dashboards,renderVisibleItem:e=>(0,z.Y)(O.N_,{...re(e)}),renderTooltipItem:e=>(0,z.Y)(O.N_,{...re(e),css:le}),getKey:e=>e.id})}],se=e=>v.AH`
  && th.ant-table-cell {
    color: ${e.colors.grayscale.light1};
  }

  .ant-table-placeholder {
    display: none;
  }
`,de=(0,z.FD)(z.FK,{children:[(0,z.Y)(m.A.PlusOutlined,{iconSize:"m",css:v.AH`
        & > .anticon {
          line-height: 0;
        }
      `}),(0,l.t)("Create chart with dataset")]}),ce=(0,b.I4)(q.p)`
  margin: ${({theme:e})=>13*e.gridUnit}px 0;
`,ue=({datasetId:e})=>{const{loading:t,recordCount:n,data:i,onChange:r}=(e=>{const{addDangerToast:t}=(0,B.Yf)(),n=(0,a.useMemo)((()=>[{id:"datasource_id",operator:X.t.Equals,value:e}]),[e]),{state:{loading:i,resourceCount:r,resourceCollection:o},fetchData:s}=(0,V.RU)("chart",(0,l.t)("chart"),t,!0,[],n),d=(0,a.useMemo)((()=>o.map((e=>({...e,key:e.id})))),[o]),c=(0,a.useCallback)(((e,t,n)=>{var a,i;const r=(null!=(a=e.current)?a:1)-1,l=null!=(i=e.pageSize)?i:0,o=(0,W.A)(n).filter((({columnKey:e})=>"string"==typeof e)).map((({columnKey:e,order:t})=>({id:e,desc:"descend"===t})));s({pageIndex:r,pageSize:l,sortBy:o,filters:[]})}),[s]);return(0,a.useEffect)((()=>{s({pageIndex:0,pageSize:25,sortBy:[{id:"last_saved_at",desc:!0}],filters:[]})}),[s]),{loading:i,recordCount:r,data:d,onChange:c}})(e),o=(0,a.useCallback)((()=>window.open(`/explore/?dataset_type=table&dataset_id=${e}`,"_blank")),[e]);return(0,z.FD)("div",{css:i.length?null:se,children:[(0,z.Y)(K.Ay,{columns:oe,data:i,size:K.QS.Middle,defaultPageSize:25,recordCount:n,loading:t,onChange:r}),i.length||t?null:(0,z.Y)(ce,{image:(0,z.Y)(H.A,{}),size:"large",title:(0,l.t)("No charts"),description:(0,l.t)("This dataset is not used to power any charts."),buttonText:de,buttonAction:o})]})},he=(0,b.I4)(M.Ay)`
  ${({theme:e})=>`\n  margin-top: ${8.5*e.gridUnit}px;\n  padding-left: ${4*e.gridUnit}px;\n  padding-right: ${4*e.gridUnit}px;\n\n  .ant-tabs-top > .ant-tabs-nav::before {\n    width: ${50*e.gridUnit}px;\n  }\n  `}
`,ge=b.I4.div`
  ${({theme:e})=>`\n  .ant-badge {\n    width: ${8*e.gridUnit}px;\n    margin-left: ${2.5*e.gridUnit}px;\n  }\n  `}
`,pe={USAGE_TEXT:(0,l.t)("Usage"),COLUMNS_TEXT:(0,l.t)("Columns"),METRICS_TEXT:(0,l.t)("Metrics")},me=({id:e})=>{const{usageCount:t}=(e=>{const[t,n]=(0,a.useState)(0),i=(0,a.useCallback)((()=>r.A.get({endpoint:`/api/v1/dataset/${e}/related_objects`}).then((({json:e})=>{n(null==e?void 0:e.charts.count)})).catch((e=>{(0,c.iB)((0,l.t)("There was an error fetching dataset's related objects")),o.A.error(e)}))),[e]);return(0,a.useEffect)((()=>{e&&i()}),[e,i]),{usageCount:t}})(e),n=(0,z.FD)(ge,{children:[(0,z.Y)("span",{children:pe.USAGE_TEXT}),t>0&&(0,z.Y)(j.A,{count:t})]});return(0,z.FD)(he,{moreIcon:null,fullWidth:!1,children:[(0,z.Y)(M.Ay.TabPane,{tab:pe.COLUMNS_TEXT},"1"),(0,z.Y)(M.Ay.TabPane,{tab:pe.METRICS_TEXT},"2"),(0,z.Y)(M.Ay.TabPane,{tab:n,children:(0,z.Y)(ue,{datasetId:e})},"3")]})};var fe=n(32132),be=n(25946),ve=n(39197);const ye=b.I4.div`
  padding: ${({theme:e})=>8*e.gridUnit}px
    ${({theme:e})=>6*e.gridUnit}px;

  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
`,xe=(0,b.I4)(q.p)`
  max-width: 50%;

  p {
    width: ${({theme:e})=>115*e.gridUnit}px;
  }
`,$e=(0,l.t)("Datasets can be created from database tables or SQL queries. Select a database table to the left or "),we=(0,l.t)("create dataset from SQL query"),_e=(0,l.t)(" to open SQL Lab. From there you can save the query as a dataset."),Se=(0,l.t)("Select dataset source"),Ue=(0,l.t)("No table columns"),Ye=(0,l.t)("This database table does not contain any data. Please select a different table."),Ie=(0,l.t)("An Error Occurred"),Ce=(0,l.t)("Unable to load columns for the selected table. Please select a different table."),Te=e=>{const{hasError:t,tableName:n,hasColumns:a}=e;let i="empty-dataset.svg",r=Se,l=(0,z.FD)(z.FK,{children:[$e,(0,z.Y)(O.N_,{to:"/sqllab",children:(0,z.Y)("span",{role:"button",tabIndex:0,children:we})}),_e]});return t?(r=Ie,l=(0,z.Y)(z.FK,{children:Ce}),i=void 0):n&&!a&&(i="no-columns.svg",r=Ue,l=(0,z.Y)(z.FK,{children:Ye})),(0,z.Y)(ye,{children:(0,z.Y)(xe,{image:i,size:"large",title:r,description:l})})};var Ae;!function(e){e.ABSOLUTE="absolute",e.RELATIVE="relative"}(Ae||(Ae={}));const De=b.I4.div`
  ${({theme:e,position:t})=>`\n  position: ${t};\n  margin: ${4*e.gridUnit}px\n    ${3*e.gridUnit}px\n    ${3*e.gridUnit}px\n    ${6*e.gridUnit}px;\n  font-size: ${6*e.gridUnit}px;\n  font-weight: ${e.typography.weights.medium};\n  padding-bottom: ${3*e.gridUnit}px;\n\n  white-space: nowrap;\n  overflow: hidden;\n  text-overflow: ellipsis;\n\n  .anticon:first-of-type {\n    margin-right: ${4*e.gridUnit}px;\n  }\n\n  .anticon:nth-of-type(2) {\n    margin-left: ${4*e.gridUnit}px;\n  `}
`,ke=b.I4.div`
  ${({theme:e})=>`\n  margin-left: ${6*e.gridUnit}px;\n  margin-bottom: ${3*e.gridUnit}px;\n  font-weight: ${e.typography.weights.bold};\n  `}
`,Ee=b.I4.div`
  ${({theme:e})=>`\n  padding: ${8*e.gridUnit}px\n    ${6*e.gridUnit}px;\n  box-sizing: border-box;\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  height: 100%;\n  position: absolute;\n  top: 0;\n  bottom: 0;\n  left: 0;\n  right: 0;\n  `}
`,ze=b.I4.div`
  ${({theme:e})=>`\n  max-width: 50%;\n  width: 200px;\n\n  img {\n    width: 120px;\n    margin-left: 40px;\n  }\n\n  div {\n    width: 100%;\n    margin-top: ${3*e.gridUnit}px;\n    text-align: center;\n    font-weight: ${e.typography.weights.normal};\n    font-size: ${e.typography.sizes.l}px;\n    color: ${e.colors.grayscale.light1};\n  }\n  `}
`,Fe=b.I4.div`
  ${({theme:e})=>`\n  position: relative;\n  margin: ${3*e.gridUnit}px;\n  margin-left: ${6*e.gridUnit}px;\n  height: calc(100% - ${60*e.gridUnit}px);\n  overflow: auto;\n  `}
`,Pe=b.I4.div`
  ${({theme:e})=>`\n  position: relative;\n  margin: ${3*e.gridUnit}px;\n  margin-left: ${6*e.gridUnit}px;\n  height: calc(100% - ${30*e.gridUnit}px);\n  overflow: auto;\n  `}
`,Ne=b.I4.div`
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  right: 0;
`,Re=(0,b.I4)(be.A)`
  ${({theme:e})=>`\n  border: 1px solid ${e.colors.info.base};\n  padding: ${4*e.gridUnit}px;\n  margin: ${6*e.gridUnit}px ${6*e.gridUnit}px\n    ${8*e.gridUnit}px;\n  .view-dataset-button {\n    position: absolute;\n    top: ${4*e.gridUnit}px;\n    right: ${4*e.gridUnit}px;\n    font-weight: ${e.typography.weights.normal};\n\n    &:hover {\n      color: ${e.colors.secondary.dark3};\n      text-decoration: underline;\n    }\n  }\n  `}
`,Le=(0,l.t)("Refreshing columns"),je=(0,l.t)("Table columns"),Me=(0,l.t)("Loading"),Oe=["5","10","15","25"],We=[{title:"Column Name",dataIndex:"name",key:"name",sorter:(e,t)=>e.name.localeCompare(t.name)},{title:"Datatype",dataIndex:"type",key:"type",width:"100px",sorter:(e,t)=>e.name.localeCompare(t.name)}],Ke=(0,l.t)("This table already has a dataset associated with it. You can only associate one dataset with a table.\n"),qe=(0,l.t)("View Dataset"),He=({tableName:e,columnList:t,loading:n,hasError:a,datasets:i})=>{const r=(0,b.DP)(),o=Boolean((null==t?void 0:t.length)>0),s=null==i?void 0:i.map((e=>e.table_name)),d=null==i?void 0:i.find((t=>t.table_name===e));let c,u;return n&&(u=(0,z.Y)(Ee,{children:(0,z.FD)(ze,{children:[(0,z.Y)("img",{alt:Me,src:ve}),(0,z.Y)("div",{children:Le})]})})),n||(c=!n&&e&&o&&!a?(0,z.FD)(z.FK,{children:[(0,z.Y)(ke,{children:je}),d?(0,z.Y)(Fe,{children:(0,z.Y)(Ne,{children:(0,z.Y)(K.Ay,{loading:n,size:K.QS.Small,columns:We,data:t,pageSizeOptions:Oe,defaultPageSize:25})})}):(0,z.Y)(Pe,{children:(0,z.Y)(Ne,{children:(0,z.Y)(K.Ay,{loading:n,size:K.QS.Small,columns:We,data:t,pageSizeOptions:Oe,defaultPageSize:25})})})]}):(0,z.Y)(Te,{hasColumns:o,hasError:a,tableName:e})),(0,z.FD)(z.FK,{children:[e&&(0,z.FD)(z.FK,{children:[(null==s?void 0:s.includes(e))&&(h=d,(0,z.Y)(Re,{closable:!1,type:"info",showIcon:!0,message:(0,l.t)("This table already has a dataset"),description:(0,z.FD)(z.FK,{children:[Ke,(0,z.Y)("span",{role:"button",onClick:()=>{window.open(null==h?void 0:h.explore_url,"_blank","noreferrer noopener popup=false")},tabIndex:0,className:"view-dataset-button",children:qe})]})})),(0,z.FD)(De,{position:!n&&o?Ae.RELATIVE:Ae.ABSOLUTE,title:e||"",children:[e&&(0,z.Y)(m.A.Table,{iconColor:r.colors.grayscale.base}),e]})]}),c,u]});var h},Be=({tableName:e,dbId:t,catalog:n,schema:i,setHasColumns:s,datasets:d})=>{const[u,h]=(0,a.useState)([]),[g,p]=(0,a.useState)(!1),[m,f]=(0,a.useState)(!1),b=(0,a.useRef)(e);return(0,a.useEffect)((()=>{b.current=e,e&&i&&t&&(async e=>{const{dbId:t,tableName:a,schema:i}=e;p(!0),null==s||s(!1);const d=`/api/v1/database/${t}/table_metadata/${(0,fe.zJ)({name:a,catalog:n,schema:i})}`;try{const e=await r.A.get({endpoint:d});if((e=>{let t=!0;if("string"!=typeof(null==e?void 0:e.name)&&(t=!1),t&&!Array.isArray(e.columns)&&(t=!1),t&&e.columns.length>0){const n=e.columns.some(((e,t)=>{const n=(e=>{let t=!0;const n="The object provided to isITableColumn does match the interface.";return"string"!=typeof(null==e?void 0:e.name)&&(t=!1,console.error(`${n} The property 'name' is required and must be a string`)),t&&"string"!=typeof(null==e?void 0:e.type)&&(t=!1,console.error(`${n} The property 'type' is required and must be a string`)),t})(e);return n||console.error(`The provided object does not match the IDatabaseTable interface. columns[${t}] is invalid and does not match the ITableColumn interface`),!n}));t=!n}return t})(null==e?void 0:e.json)){const t=e.json;t.name===b.current&&(h(t.columns),null==s||s(t.columns.length>0),f(!1))}else h([]),null==s||s(!1),f(!0),(0,c.iB)((0,l.t)("The API response from %s does not match the IDatabaseTable interface.",d)),o.A.error((0,l.t)("The API response from %s does not match the IDatabaseTable interface.",d))}catch(e){h([]),null==s||s(!1),f(!0)}finally{p(!1)}})({tableName:e,dbId:t,schema:i})}),[e,t,i]),(0,z.Y)(He,{columnList:u,hasError:m,loading:g,tableName:e,datasets:d})};var Ve=n(8791),Xe=n(62221);const Qe=b.I4.div`
  ${({theme:e})=>`\n    padding: ${4*e.gridUnit}px;\n    height: 100%;\n    background-color: ${e.colors.grayscale.light5};\n    position: relative;\n    .emptystate {\n      height: auto;\n      margin-top: ${17.5*e.gridUnit}px;\n    }\n    .section-title {\n      margin-top: ${5.5*e.gridUnit}px;\n      margin-bottom: ${11*e.gridUnit}px;\n      font-weight: ${e.typography.weights.bold};\n    }\n    .table-title {\n      margin-top: ${11*e.gridUnit}px;\n      margin-bottom: ${6*e.gridUnit}px;\n      font-weight: ${e.typography.weights.bold};\n    }\n    .options-list {\n      overflow: auto;\n      position: absolute;\n      bottom: 0;\n      top: ${92.25*e.gridUnit}px;\n      left: ${3.25*e.gridUnit}px;\n      right: 0;\n\n      .no-scrollbar {\n        margin-right: ${4*e.gridUnit}px;\n      }\n\n      .options {\n        cursor: pointer;\n        padding: ${1.75*e.gridUnit}px;\n        border-radius: ${e.borderRadius}px;\n        :hover {\n          background-color: ${e.colors.grayscale.light4}\n        }\n      }\n\n      .options-highlighted {\n        cursor: pointer;\n        padding: ${1.75*e.gridUnit}px;\n        border-radius: ${e.borderRadius}px;\n        background-color: ${e.colors.primary.dark1};\n        color: ${e.colors.grayscale.light5};\n      }\n\n      .options, .options-highlighted {\n        display: flex;\n        align-items: center;\n        justify-content: space-between;\n      }\n    }\n    form > span[aria-label="refresh"] {\n      position: absolute;\n      top: ${69*e.gridUnit}px;\n      left: ${42.75*e.gridUnit}px;\n      font-size: ${4.25*e.gridUnit}px;\n    }\n    .table-form {\n      margin-bottom: ${8*e.gridUnit}px;\n    }\n    .loading-container {\n      position: absolute;\n      top: ${89.75*e.gridUnit}px;\n      left: 0;\n      right: 0;\n      text-align: center;\n      img {\n        width: ${20*e.gridUnit}px;\n        margin-bottom: ${2.5*e.gridUnit}px;\n      }\n      p {\n        color: ${e.colors.grayscale.light1};\n      }\n    }\n`}
`;function Ge({setDataset:e,dataset:t,datasetNames:n}){const{addDangerToast:i}=(0,B.Yf)(),r=(0,a.useCallback)((t=>{e({type:h.SelectDatabase,payload:{db:t}})}),[e]);(0,a.useEffect)((()=>{const e=(0,Xe.Gq)(Xe.Hh.Database,null);e&&r(e)}),[r]);const o=(0,a.useCallback)((e=>(0,z.Y)(Ve.cs,{table:null!=n&&n.includes(e.value)?{...e,extra:{warning_markdown:(0,l.t)("This table already has a dataset")}}:e})),[n]);return(0,z.Y)(Qe,{children:(0,z.Y)(Ve.Ay,{database:null==t?void 0:t.db,handleError:i,emptyState:(0,z.Y)(q.p,{image:"empty.svg",title:(0,l.t)("No databases available"),description:(0,z.FD)("span",{children:[(0,l.t)("Manage your databases")," ",(0,z.Y)("a",{href:"/databaseview/list",children:(0,l.t)("here")})]}),size:"small"}),onDbChange:r,onCatalogChange:t=>{t&&e({type:h.SelectCatalog,payload:{name:"catalog",value:t}})},onSchemaChange:t=>{t&&e({type:h.SelectSchema,payload:{name:"schema",value:t}})},onTableSelectChange:t=>{e({type:h.SelectTable,payload:{name:"table_name",value:t}})},sqlLabMode:!1,customTableOptionLabelRenderer:o,...(null==t?void 0:t.catalog)&&{catalog:t.catalog},...(null==t?void 0:t.schema)&&{schema:t.schema}})})}var Je=n(7735),Ze=n(35700);const et=["db","schema","table_name"],tt=[Ze.ci,Ze.q0,Ze.ar,Ze.R2],nt=(0,B.Ay)((function({datasetObject:e,addDangerToast:t,hasColumns:n=!1,datasets:a}){const r=(0,i.W6)(),{createResource:o}=(0,V.fn)("dataset",(0,l.t)("dataset"),t),s=(0,l.t)("Select a database table."),d=(0,l.t)("Create dataset and create chart"),c=!(null!=e&&e.table_name)||!n||(null==a?void 0:a.includes(null==e?void 0:e.table_name));return(0,z.FD)(z.FK,{children:[(0,z.Y)(p.A,{onClick:()=>{if(e){const t=(e=>{let t=0;const n=Object.keys(e).reduce(((n,a)=>(et.includes(a)&&e[a]&&(t+=1),t)),0);return tt[n]})(e);(0,Je.logEvent)(t,e)}else(0,Je.logEvent)(Ze.ci,{});r.goBack()},children:(0,l.t)("Cancel")}),(0,z.Y)(p.A,{buttonStyle:"primary",disabled:c,tooltip:null!=e&&e.table_name?void 0:s,onClick:()=>{if(e){var t;const n={database:null==(t=e.db)?void 0:t.id,catalog:e.catalog,schema:e.schema,table_name:e.table_name};o(n).then((t=>{t&&"number"==typeof t&&((0,Je.logEvent)(Ze.oA,e),r.push(`/chart/add/?dataset=${e.table_name}`))}))}},children:d})]})}));var at=n(41621);function it({header:e,leftPanel:t,datasetPanel:n,rightPanel:a,footer:i}){const r=(0,b.DP)();return(0,z.FD)(y,{children:[e&&(0,z.Y)(Y,{children:e}),(0,z.FD)(_,{children:[t&&(0,z.Y)(at.A,{id:"dataset",initialWidth:80*r.gridUnit,minWidth:80*r.gridUnit,enable:!0,children:e=>(0,z.Y)(x,{width:e,children:(0,z.Y)(C,{children:t})})}),(0,z.FD)($,{children:[(0,z.FD)(S,{children:[n&&(0,z.Y)(T,{children:n}),a&&(0,z.Y)(A,{children:a})]}),(0,z.Y)(U,{children:i&&(0,z.Y)(D,{children:i})})]})]})]})}function rt(e,t){const n={...e||{}};switch(t.type){case h.SelectDatabase:return{...n,...t.payload,catalog:null,schema:null,table_name:null};case h.SelectCatalog:return{...n,[t.payload.name]:t.payload.value,schema:null,table_name:null};case h.SelectSchema:return{...n,[t.payload.name]:t.payload.value,table_name:null};case h.SelectTable:return{...n,[t.payload.name]:t.payload.value};case h.ChangeDataset:return{...n,[t.payload.name]:t.payload.value};default:return null}}const lt="/tablemodelview/list/?pageIndex=0&sortColumn=changed_on_delta_humanized&sortOrder=desc";function ot(){const[e,t]=(0,a.useReducer)(rt,null),[n,r]=(0,a.useState)(!1),[l,o]=(0,a.useState)(!1),{datasets:s,datasetNames:d}=u(null==e?void 0:e.db,null==e?void 0:e.schema),{datasetId:c}=(0,i.g)();return(0,a.useEffect)((()=>{Number.isNaN(parseInt(c,10))||o(!0)}),[c]),(0,z.Y)(it,{header:(0,z.Y)(L,{setDataset:t,title:null==e?void 0:e.table_name}),leftPanel:l?null:(0,z.Y)(Ge,{setDataset:t,dataset:e,datasetNames:d}),datasetPanel:l?(0,z.Y)(me,{id:c}):(0,z.Y)(Be,{tableName:null==e?void 0:e.table_name,dbId:null==e||null==(h=e.db)?void 0:h.id,catalog:null==e?void 0:e.catalog,schema:null==e?void 0:e.schema,setHasColumns:r,datasets:s}),footer:(0,z.Y)(nt,{url:lt,datasetObject:e,hasColumns:n,datasets:d})});var h}}}]);