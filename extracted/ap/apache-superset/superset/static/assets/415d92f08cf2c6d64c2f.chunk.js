"use strict";(globalThis.webpackChunksuperset=globalThis.webpackChunksuperset||[]).push([[9915],{10044:(e,t,r)=>{r.d(t,{A:()=>i});var a=r(28073),s=r(2445);const i=e=>(0,s.Y)(a.A,{...e})},93514:(e,t,r)=>{r.d(t,{F:()=>s});var a=r(95579);const s={name:(0,a.t)("SQL"),tabs:[{name:"Saved queries",label:(0,a.t)("Saved queries"),url:"/savedqueryview/list/",usesRouter:!0},{name:"Query history",label:(0,a.t)("Query history"),url:"/sqllab/history/",usesRouter:!0}]}},11188:(e,t,r)=>{r.d(t,{A:()=>m});var a=r(96453),s=r(95579),i=r(78360),l=r(69633),o=r(8143),n=r(69172),c=r(10286),d=r(45738),u=r(12249),h=r(73135),g=r(2445);d.A.registerLanguage("sql",i.A),d.A.registerLanguage("markdown",o.A),d.A.registerLanguage("html",l.A),d.A.registerLanguage("json",n.A);const p=a.I4.div`
  margin-top: -24px;

  &:hover {
    svg {
      visibility: visible;
    }
  }

  svg {
    position: relative;
    top: 40px;
    left: 512px;
    visibility: hidden;
    margin: -4px;
    color: ${({theme:e})=>e.colors.grayscale.base};
  }
`;function m({addDangerToast:e,addSuccessToast:t,children:r,...a}){return(0,g.FD)(p,{children:[(0,g.Y)(u.A.Copy,{tabIndex:0,role:"button",onClick:a=>{var i;a.preventDefault(),a.currentTarget.blur(),i=r,(0,h.A)((()=>Promise.resolve(i))).then((()=>{t&&t((0,s.t)("SQL Copied!"))})).catch((()=>{e&&e((0,s.t)("Sorry, your browser does not support copying."))}))}}),(0,g.Y)(d.A,{style:c.A,...a,children:r})]})}},14318:(e,t,r)=>{r.d(t,{A:()=>s});var a=r(96540);function s({queries:e,fetchData:t,currentQueryId:r}){const s=e.findIndex((e=>e.id===r)),[i,l]=(0,a.useState)(s),[o,n]=(0,a.useState)(!1),[c,d]=(0,a.useState)(!1);function u(){n(0===i),d(i===e.length-1)}function h(r){const a=i+(r?-1:1);a>=0&&a<e.length&&(t(e[a].id),l(a),u())}return(0,a.useEffect)((()=>{u()})),{handleKeyPress:function(t){i>=0&&i<e.length&&("ArrowDown"===t.key||"k"===t.key?(t.preventDefault(),h(!1)):"ArrowUp"!==t.key&&"j"!==t.key||(t.preventDefault(),h(!0)))},handleDataChange:h,disablePrevious:o,disableNext:c}}},52825:(e,t,r)=>{r.r(t),r.d(t,{default:()=>E});var a=r(96540),s=r(61574),i=r(71519),l=r(96453),o=r(95579),n=r(35742),c=r(69108),d=r(30703),u=r(5261),h=r(50500),g=r(35768),p=r(51713),m=r(10044),y=r(93514),b=r(39854),v=r(19129),f=r(45738),A=r(78360),x=r(10286),S=r(27023),q=r(23193),k=r(12249),w=r(85861),C=r(46942),Y=r.n(C),D=r(46920),H=r(11188),$=r(14318),F=r(2445);const T=l.I4.div`
  color: ${({theme:e})=>e.colors.secondary.light2};
  font-size: ${({theme:e})=>e.typography.sizes.s}px;
  margin-bottom: 0;
`,I=l.I4.div`
  color: ${({theme:e})=>e.colors.grayscale.dark2};
  font-size: ${({theme:e})=>e.typography.sizes.m}px;
  padding: 4px 0 24px 0;
`,z=l.I4.div`
  margin: 0 0 ${({theme:e})=>6*e.gridUnit}px 0;
`,L=l.I4.div`
  display: inline;
  font-size: ${({theme:e})=>e.typography.sizes.s}px;
  padding: ${({theme:e})=>2*e.gridUnit}px
    ${({theme:e})=>4*e.gridUnit}px;
  margin-right: ${({theme:e})=>4*e.gridUnit}px;
  color: ${({theme:e})=>e.colors.secondary.dark1};

  &.active,
  &:focus,
  &:hover {
    background: ${({theme:e})=>e.colors.secondary.light4};
    border-bottom: none;
    border-radius: ${({theme:e})=>e.borderRadius}px;
    margin-bottom: ${({theme:e})=>2*e.gridUnit}px;
  }

  &:hover:not(.active) {
    background: ${({theme:e})=>e.colors.secondary.light5};
  }
`,U=(0,l.I4)(w.Ay)`
  .antd5-modal-body {
    padding: ${({theme:e})=>6*e.gridUnit}px;
  }

  pre {
    font-size: ${({theme:e})=>e.typography.sizes.xs}px;
    font-weight: ${({theme:e})=>e.typography.weights.normal};
    line-height: ${({theme:e})=>e.typography.sizes.l}px;
    height: 375px;
    border: none;
  }
`,Q=(0,u.Ay)((function({onHide:e,openInSqlLab:t,queries:r,query:s,fetchData:i,show:l,addDangerToast:n,addSuccessToast:c}){const{handleKeyPress:d,handleDataChange:u,disablePrevious:h,disableNext:g}=(0,$.A)({queries:r,currentQueryId:s.id,fetchData:i}),[p,m]=(0,a.useState)("user"),{id:y,sql:b,executed_sql:v}=s;return(0,F.Y)("div",{role:"none",onKeyUp:d,children:(0,F.FD)(U,{onHide:e,show:l,title:(0,o.t)("Query preview"),footer:(0,F.FD)(F.FK,{children:[(0,F.Y)(D.A,{disabled:h,onClick:()=>u(!0),children:(0,o.t)("Previous")},"previous-query"),(0,F.Y)(D.A,{disabled:g,onClick:()=>u(!1),children:(0,o.t)("Next")},"next-query"),(0,F.Y)(D.A,{buttonStyle:"primary",onClick:()=>t(y),children:(0,o.t)("Open in SQL Lab")},"open-in-sql-lab")]}),children:[(0,F.Y)(T,{children:(0,o.t)("Tab name")}),(0,F.Y)(I,{children:s.tab_name}),(0,F.FD)(z,{children:[(0,F.Y)(L,{role:"button",className:Y()({active:"user"===p}),onClick:()=>m("user"),children:(0,o.t)("User query")}),(0,F.Y)(L,{role:"button",className:Y()({active:"executed"===p}),onClick:()=>m("executed"),children:(0,o.t)("Executed query")})]}),(0,F.Y)(H.A,{addDangerToast:n,addSuccessToast:c,language:"sql",children:("user"===p?b:v)||""})]})})}));var R=r(95272),_=r(25106),N=r(7089);const Z=(0,l.I4)(b.A)`
  table .table-cell {
    vertical-align: top;
  }
`;f.A.registerLanguage("sql",A.A);const P=(0,l.I4)(f.A)`
  height: ${({theme:e})=>26*e.gridUnit}px;
  overflow: hidden !important; /* needed to override inline styles */
  text-overflow: ellipsis;
  white-space: nowrap;
`,K=l.I4.div`
  .count {
    margin-left: 5px;
    color: ${({theme:e})=>e.colors.primary.base};
    text-decoration: underline;
    cursor: pointer;
  }
`,O=l.I4.div`
  color: ${({theme:e})=>e.colors.grayscale.dark2};
`,B=(0,l.I4)(g.Ay)`
  text-align: left;
  font-family: ${({theme:e})=>e.typography.families.monospace};
`,E=(0,u.Ay)((function({addDangerToast:e}){const{state:{loading:t,resourceCount:r,resourceCollection:u},fetchData:g}=(0,h.RU)("query",(0,o.t)("Query history"),e,!1),[f,A]=(0,a.useState)(),w=(0,l.DP)(),C=(0,s.W6)(),Y=(0,a.useCallback)((t=>{n.A.get({endpoint:`/api/v1/query/${t}`}).then((({json:e={}})=>{A({...e.result})}),(0,d.JF)((t=>e((0,o.t)("There was an issue previewing the selected query. %s",t)))))}),[e]),D={activeChild:"Query history",...y.F},H=[{id:q.H.StartTime,desc:!0}],$=(0,a.useMemo)((()=>[{Cell:({row:{original:{status:e}}})=>{const t={name:null,label:""};return e===c.kZ.Success?(t.name=(0,F.Y)(k.A.Check,{iconColor:w.colors.success.base}),t.label=(0,o.t)("Success")):e===c.kZ.Failed||e===c.kZ.Stopped?(t.name=(0,F.Y)(k.A.XSmall,{iconColor:e===c.kZ.Failed?w.colors.error.base:w.colors.grayscale.base}),t.label=(0,o.t)("Failed")):e===c.kZ.Running?(t.name=(0,F.Y)(k.A.Running,{iconColor:w.colors.primary.base}),t.label=(0,o.t)("Running")):e===c.kZ.TimedOut?(t.name=(0,F.Y)(k.A.Offline,{iconColor:w.colors.grayscale.light1}),t.label=(0,o.t)("Offline")):e!==c.kZ.Scheduled&&e!==c.kZ.Pending||(t.name=(0,F.Y)(k.A.Queued,{iconColor:w.colors.grayscale.base}),t.label=(0,o.t)("Scheduled")),(0,F.Y)(v.m_,{title:t.label,placement:"bottom",children:(0,F.Y)("span",{children:t.name})})},accessor:q.H.Status,size:"xs",disableSortBy:!0},{accessor:q.H.StartTime,Header:(0,o.t)("Time"),size:"xl",Cell:({row:{original:{start_time:e}}})=>{const t=N.XV.utc(e).local().format(S.QU).split(" ");return(0,F.FD)(F.FK,{children:[t[0]," ",(0,F.Y)("br",{}),t[1]]})}},{Header:(0,o.t)("Duration"),size:"xl",Cell:({row:{original:{status:e,start_time:t,end_time:r}}})=>{const a=e===c.kZ.Failed?"danger":e,s=r?(0,N.XV)(N.XV.utc(r-t)).format(S.os):"00:00:00.000";return(0,F.Y)(B,{type:a,role:"timer",children:s})}},{accessor:q.H.TabName,Header:(0,o.t)("Tab name"),size:"xl"},{accessor:q.H.DatabaseName,Header:(0,o.t)("Database"),size:"xl"},{accessor:q.H.Database,hidden:!0},{accessor:q.H.Schema,Header:(0,o.t)("Schema"),size:"xl"},{Cell:({row:{original:{sql_tables:e=[]}}})=>{const t=e.map((e=>e.table)),r=t.length>0?t.shift():"";return t.length?(0,F.FD)(K,{children:[(0,F.Y)("span",{children:r}),(0,F.Y)(m.A,{placement:"right",title:(0,o.t)("TABLES"),trigger:"click",content:(0,F.Y)(F.FK,{children:t.map((e=>(0,F.Y)(O,{children:e},e)))}),children:(0,F.FD)("span",{className:"count",children:["(+",t.length,")"]})})]}):r},accessor:q.H.SqlTables,Header:(0,o.t)("Tables"),size:"xl",disableSortBy:!0},{accessor:q.H.UserFirstName,Header:(0,o.t)("User"),size:"xl",Cell:({row:{original:{user:e}}})=>(0,_.A)(e)},{accessor:q.H.User,hidden:!0},{accessor:q.H.Rows,Header:(0,o.t)("Rows"),size:"md"},{accessor:q.H.Sql,Header:(0,o.t)("SQL"),Cell:({row:{original:e,id:t}})=>(0,F.Y)("div",{tabIndex:0,role:"button",onClick:()=>A(e),children:(0,F.Y)(P,{language:"sql",style:x.A,children:(0,d.s4)(e.sql,4)})})},{Header:(0,o.t)("Actions"),id:"actions",disableSortBy:!0,Cell:({row:{original:{id:e}}})=>(0,F.Y)(v.m_,{title:(0,o.t)("Open query in SQL Lab"),placement:"bottom",children:(0,F.Y)(i.N_,{to:`/sqllab?queryId=${e}`,children:(0,F.Y)(k.A.Full,{iconColor:w.colors.grayscale.base})})})}]),[]),T=(0,a.useMemo)((()=>[{Header:(0,o.t)("Database"),key:"database",id:"database",input:"select",operator:b.t.RelationOneMany,unfilteredLabel:(0,o.t)("All"),fetchSelects:(0,d.u1)("query","database",(0,d.JF)((t=>e((0,o.t)("An error occurred while fetching database values: %s",t))))),paginate:!0},{Header:(0,o.t)("State"),key:"state",id:"status",input:"select",operator:b.t.Equals,unfilteredLabel:"All",fetchSelects:(0,d.$C)("query","status",(0,d.JF)((t=>e((0,o.t)("An error occurred while fetching schema values: %s",t))))),paginate:!0},{Header:(0,o.t)("User"),key:"user",id:"user",input:"select",operator:b.t.RelationOneMany,unfilteredLabel:"All",fetchSelects:(0,d.u1)("query","user",(0,d.JF)((t=>e((0,o.t)("An error occurred while fetching user values: %s",t))))),paginate:!0},{Header:(0,o.t)("Time range"),key:"start_time",id:"start_time",input:"datetime_range",operator:b.t.Between},{Header:(0,o.t)("Search by query text"),key:"sql",id:"sql",input:"search",operator:b.t.Contains}]),[e]);return(0,F.FD)(F.FK,{children:[(0,F.Y)(p.A,{...D}),f&&(0,F.Y)(Q,{onHide:()=>A(void 0),query:f,queries:u,fetchData:Y,openInSqlLab:e=>C.push(`/sqllab?queryId=${e}`),show:!0}),(0,F.Y)(Z,{className:"query-history-list-view",columns:$,count:r,data:u,fetchData:g,filters:T,initialSort:H,loading:t,pageSize:25,highlightRowId:null==f?void 0:f.id,refreshData:()=>{},addDangerToast:e,addSuccessToast:R.WR})]})}))}}]);