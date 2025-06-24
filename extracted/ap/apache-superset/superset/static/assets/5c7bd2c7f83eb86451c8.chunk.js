"use strict";(globalThis.webpackChunksuperset=globalThis.webpackChunksuperset||[]).push([[1285],{45418:(e,t,i)=>{i.d(t,{A:()=>u});var n=i(96540),a=i(46942),r=i.n(a),o=i(22553),l=i(6311),d=i(1051),s=i(96424),c=i(14277);const h=e=>{const{componentCls:t,sizePaddingEdgeHorizontal:i,colorSplit:n,lineWidth:a,textPaddingInline:r,orientationMargin:o,verticalMarginInline:s}=e;return{[t]:Object.assign(Object.assign({},(0,d.dF)(e)),{borderBlockStart:`${(0,l.unit)(a)} solid ${n}`,"&-vertical":{position:"relative",top:"-0.06em",display:"inline-block",height:"0.9em",marginInline:s,marginBlock:0,verticalAlign:"middle",borderTop:0,borderInlineStart:`${(0,l.unit)(a)} solid ${n}`},"&-horizontal":{display:"flex",clear:"both",width:"100%",minWidth:"100%",margin:`${(0,l.unit)(e.dividerHorizontalGutterMargin)} 0`},[`&-horizontal${t}-with-text`]:{display:"flex",alignItems:"center",margin:`${(0,l.unit)(e.dividerHorizontalWithTextGutterMargin)} 0`,color:e.colorTextHeading,fontWeight:500,fontSize:e.fontSizeLG,whiteSpace:"nowrap",textAlign:"center",borderBlockStart:`0 ${n}`,"&::before, &::after":{position:"relative",width:"50%",borderBlockStart:`${(0,l.unit)(a)} solid transparent`,borderBlockStartColor:"inherit",borderBlockEnd:0,transform:"translateY(50%)",content:"''"}},[`&-horizontal${t}-with-text-left`]:{"&::before":{width:`calc(${o} * 100%)`},"&::after":{width:`calc(100% - ${o} * 100%)`}},[`&-horizontal${t}-with-text-right`]:{"&::before":{width:`calc(100% - ${o} * 100%)`},"&::after":{width:`calc(${o} * 100%)`}},[`${t}-inner-text`]:{display:"inline-block",paddingBlock:0,paddingInline:r},"&-dashed":{background:"none",borderColor:n,borderStyle:"dashed",borderWidth:`${(0,l.unit)(a)} 0 0`},[`&-horizontal${t}-with-text${t}-dashed`]:{"&::before, &::after":{borderStyle:"dashed none none"}},[`&-vertical${t}-dashed`]:{borderInlineStartWidth:a,borderInlineEnd:0,borderBlockStart:0,borderBlockEnd:0},"&-dotted":{background:"none",borderColor:n,borderStyle:"dotted",borderWidth:`${(0,l.unit)(a)} 0 0`},[`&-horizontal${t}-with-text${t}-dotted`]:{"&::before, &::after":{borderStyle:"dotted none none"}},[`&-vertical${t}-dotted`]:{borderInlineStartWidth:a,borderInlineEnd:0,borderBlockStart:0,borderBlockEnd:0},[`&-plain${t}-with-text`]:{color:e.colorText,fontWeight:"normal",fontSize:e.fontSize},[`&-horizontal${t}-with-text-left${t}-no-default-orientation-margin-left`]:{"&::before":{width:0},"&::after":{width:"100%"},[`${t}-inner-text`]:{paddingInlineStart:i}},[`&-horizontal${t}-with-text-right${t}-no-default-orientation-margin-right`]:{"&::before":{width:"100%"},"&::after":{width:0},[`${t}-inner-text`]:{paddingInlineEnd:i}}})}},p=(0,s.OF)("Divider",(e=>{const t=(0,c.mergeToken)(e,{dividerHorizontalWithTextGutterMargin:e.margin,dividerHorizontalGutterMargin:e.marginLG,sizePaddingEdgeHorizontal:0});return[h(t)]}),(e=>({textPaddingInline:"1em",orientationMargin:.05,verticalMarginInline:e.marginXS})),{unitless:{orientationMargin:!0}});const u=e=>{const{getPrefixCls:t,direction:i,divider:a}=n.useContext(o.QO),{prefixCls:l,type:d="horizontal",orientation:s="center",orientationMargin:c,className:h,rootClassName:u,children:g,dashed:m,variant:b="solid",plain:f,style:y}=e,v=function(e,t){var i={};for(var n in e)Object.prototype.hasOwnProperty.call(e,n)&&t.indexOf(n)<0&&(i[n]=e[n]);if(null!=e&&"function"==typeof Object.getOwnPropertySymbols){var a=0;for(n=Object.getOwnPropertySymbols(e);a<n.length;a++)t.indexOf(n[a])<0&&Object.prototype.propertyIsEnumerable.call(e,n[a])&&(i[n[a]]=e[n[a]])}return i}(e,["prefixCls","type","orientation","orientationMargin","className","rootClassName","children","dashed","variant","plain","style"]),w=t("divider",l),[x,$,S]=p(w),Y=!!g,A="left"===s&&null!=c,T="right"===s&&null!=c,k=r()(w,null==a?void 0:a.className,$,S,`${w}-${d}`,{[`${w}-with-text`]:Y,[`${w}-with-text-${s}`]:Y,[`${w}-dashed`]:!!m,[`${w}-${b}`]:"solid"!==b,[`${w}-plain`]:!!f,[`${w}-rtl`]:"rtl"===i,[`${w}-no-default-orientation-margin-left`]:A,[`${w}-no-default-orientation-margin-right`]:T},h,u),C=n.useMemo((()=>"number"==typeof c?c:/^\d+$/.test(c)?Number(c):c),[c]),D=Object.assign(Object.assign({},A&&{marginLeft:C}),T&&{marginRight:C});return x(n.createElement("div",Object.assign({className:k,style:Object.assign(Object.assign({},null==a?void 0:a.style),y)},v,{role:"separator"}),g&&"vertical"!==d&&n.createElement("span",{className:`${w}-inner-text`,style:D},g)))}},85955:(e,t,i)=>{i.d(t,{c:()=>r});var n=i(45418),a=i(2445);function r(e){return(0,a.Y)(n.A,{...e})}},70175:(e,t,i)=>{var n;i.d(t,{Q:()=>n}),function(e){e.Dashboards="dashboards",e.Description="description",e.LastModified="lastModified",e.Owner="owner",e.Rows="rows",e.Sql="sql",e.Table="table",e.Tags="tags"}(n||(n={}))},14693:(e,t,i)=>{i.d(t,{QD:()=>x.Q,Ay:()=>$});var n=i(9063),a=i.n(n),r=i(96540),o=i(98250),l=i(96453),d=i(19129),s=i(62952),c=i(95579),h=i(12249),p=i(2445);const u=l.I4.div`
  font-weight: ${({theme:e})=>e.typography.weights.bold};
`,g=({text:e,header:t})=>{const i=(0,s.A)(e);return(0,p.FD)(p.FK,{children:[t&&(0,p.Y)(u,{children:t}),i.map((e=>(0,p.Y)("div",{children:e},e)))]})},m=16,b={dashboards:0,table:1,sql:2,rows:3,tags:4,description:5,owner:6,lastModified:7},f=l.I4.div`
  ${({theme:e,count:t})=>`\n    display: flex;\n    align-items: center;\n    padding: 8px 12px;\n    background-color: ${e.colors.grayscale.light4};\n    color: ${e.colors.grayscale.base};\n    font-size: ${e.typography.sizes.s}px;\n    min-width: ${24+32*t-m}px;\n    border-radius: ${e.borderRadius}px;\n    line-height: 1;\n  `}
`,y=l.I4.div`
  ${({theme:e,collapsed:t,last:i,onClick:n})=>`\n    display: flex;\n    align-items: center;\n    max-width: ${174+(i?0:m)}px;\n    min-width: ${t?16+(i?0:m):94+(i?0:m)}px;\n    padding-right: ${i?0:m}px;\n    cursor: ${n?"pointer":"default"};\n    & .metadata-icon {\n      color: ${n&&t?e.colors.primary.base:e.colors.grayscale.base};\n      padding-right: ${t?0:8}px;\n      & .anticon {\n        line-height: 0;\n      }\n    }\n    & .metadata-text {\n      min-width: 70px;\n      overflow: hidden;\n      text-overflow: ${t?"unset":"ellipsis"};\n      white-space: nowrap;\n      text-decoration: ${n?"underline":"none"};\n      line-height: 1.4;\n    }\n  `}
`,v=l.I4.div`
  display: -webkit-box;
  -webkit-line-clamp: 20;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
`,w=({barWidth:e,contentType:t,collapsed:i,last:n=!1,tooltipPlacement:a})=>{const{icon:o,title:l,tooltip:s=l}=(e=>{const{type:t}=e;switch(t){case x.Q.Dashboards:return{icon:h.A.FundProjectionScreenOutlined,title:e.title,tooltip:e.description?(0,p.Y)("div",{children:(0,p.Y)(g,{header:e.title,text:e.description})}):void 0};case x.Q.Description:return{icon:h.A.BookOutlined,title:e.value};case x.Q.LastModified:return{icon:h.A.EditOutlined,title:e.value,tooltip:(0,p.FD)("div",{children:[(0,p.Y)(g,{header:(0,c.t)("Last modified"),text:e.value}),(0,p.Y)(g,{header:(0,c.t)("Modified by"),text:e.modifiedBy})]})};case x.Q.Owner:return{icon:h.A.UserOutlined,title:e.createdBy,tooltip:(0,p.FD)("div",{children:[(0,p.Y)(g,{header:(0,c.t)("Created by"),text:e.createdBy}),!!e.owners&&(0,p.Y)(g,{header:(0,c.t)("Owners"),text:e.owners}),(0,p.Y)(g,{header:(0,c.t)("Created on"),text:e.createdOn})]})};case x.Q.Rows:return{icon:h.A.InsertRowBelowOutlined,title:e.title,tooltip:e.title};case x.Q.Sql:return{icon:h.A.ConsoleSqlOutlined,title:e.title,tooltip:e.title};case x.Q.Table:return{icon:h.A.Table,title:e.title,tooltip:e.title};case x.Q.Tags:return{icon:h.A.TagsOutlined,title:e.values.join(", "),tooltip:(0,p.Y)("div",{children:(0,p.Y)(g,{header:(0,c.t)("Tags"),text:e.values})})};default:throw Error(`Invalid type provided: ${t}`)}})(t),[u,m]=(0,r.useState)(!1),b=(0,r.useRef)(null),f=o,{type:w,onClick:$}=t;(0,r.useEffect)((()=>{m(!!b.current&&b.current.scrollWidth>b.current.clientWidth)}),[e,m,t]);const S=(0,p.FD)(y,{collapsed:i,last:n,onClick:$?()=>$(w):void 0,role:$?"button":void 0,children:[(0,p.Y)(f,{iconSize:"l",className:"metadata-icon"}),!i&&(0,p.Y)("span",{ref:b,className:"metadata-text",children:l})]});return u||i||s&&s!==l?(0,p.Y)(d.m_,{placement:a,title:(0,p.Y)(v,{children:s}),children:S}):S};var x=i(70175);const $=({items:e,tooltipPlacement:t="top"})=>{const[i,n]=(0,r.useState)(),[l,d]=(0,r.useState)(!1),s=a()(e,((e,t)=>e.type===t.type)).sort(((e,t)=>b[e.type]-b[t.type])),c=s.length;if(c<2)throw Error("The minimum number of items for the metadata bar is 2.");if(c>6)throw Error("The maximum number of items for the metadata bar is 6.");const h=(0,r.useCallback)((e=>{const t=110*c-m;n(e),d(Boolean(e&&e<t))}),[c]),{ref:u}=(0,o.uZ)({onResize:h});return(0,p.Y)(f,{ref:u,count:c,children:s.map(((e,n)=>(0,p.Y)(w,{barWidth:i,contentType:e,collapsed:l,last:n===c-1,tooltipPlacement:t},n)))})}},51848:(e,t,i)=>{i.d(t,{U:()=>x});var n=i(17437),a=i(96453),r=i(95579),o=i(15595),l=i(96540),d=i(19129),s=i(98250),c=i(2445);const h=e=>n.AH`
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
`,p=(0,l.memo)((({title:e,placeholder:t,onSave:i,canEdit:a,label:o})=>{const[p,u]=(0,l.useState)(!1),[g,m]=(0,l.useState)(e||""),b=(0,l.useRef)(null),[f,y]=(0,l.useState)(!1),{width:v,ref:w}=(0,s.uZ)(),{width:x,ref:$}=(0,s.uZ)({refreshMode:"debounce"});(0,l.useEffect)((()=>{m(e)}),[e]),(0,l.useEffect)((()=>{if(p&&null!=b&&b.current&&(b.current.focus(),b.current.setSelectionRange)){const{length:e}=b.current.value;b.current.setSelectionRange(e,e),b.current.scrollLeft=b.current.scrollWidth}}),[p]),(0,l.useLayoutEffect)((()=>{null!=w&&w.current&&(w.current.textContent=g||t)}),[g,t,w]),(0,l.useEffect)((()=>{b.current&&b.current.scrollWidth>b.current.clientWidth?y(!0):y(!1)}),[v,x]);const S=(0,l.useCallback)((()=>{a&&!p&&u(!0)}),[a,p]),Y=(0,l.useCallback)((()=>{if(!a)return;const t=g.trim();m(t),e!==t&&i(t),u(!1)}),[a,g,i,e]),A=(0,l.useCallback)((e=>{a&&p&&m(e.target.value)}),[a,p]),T=(0,l.useCallback)((e=>{var t;a&&"Enter"===e.key&&(e.preventDefault(),null==(t=b.current)||t.blur())}),[a]);return(0,c.FD)("div",{css:h,ref:$,children:[(0,c.Y)(d.m_,{id:"title-tooltip",title:f&&g&&!p?g:null,children:a?(0,c.Y)("input",{className:"dynamic-title-input","aria-label":null!=o?o:(0,r.t)("Title"),ref:b,onChange:A,onBlur:Y,onClick:S,onKeyPress:T,placeholder:t,value:g,css:n.AH`
                cursor: ${p?"text":"pointer"};

                ${v&&v>0&&n.AH`
                  width: ${v+1}px;
                `}
              `}):(0,c.Y)("span",{className:"dynamic-title","aria-label":null!=o?o:(0,r.t)("Title"),ref:b,children:g})}),(0,c.Y)("span",{ref:w,className:"input-sizer","aria-hidden":!0,tabIndex:-1})]})}));var u=i(58132),g=i(94704),m=i(12249),b=i(46920);const f=e=>n.AH`
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
`,y=e=>n.AH`
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
`,v=e=>n.AH`
  display: flex;
  align-items: center;
  padding-left: ${2*e.gridUnit}px;

  & .fave-unfave-icon {
    padding: 0 ${e.gridUnit}px;

    &:first-of-type {
      padding-left: 0;
    }
  }
`,w=e=>n.AH`
  margin-left: ${2*e.gridUnit}px;
`,x=({editableTitleProps:e,showTitlePanelItems:t,certificatiedBadgeProps:i,showFaveStar:n,faveStarProps:l,titlePanelAdditionalItems:d,rightPanelAdditionalItems:s,additionalActionsMenu:h,menuDropdownProps:x,showMenuDropdown:$=!0,tooltipProps:S})=>{const Y=(0,a.DP)();return(0,c.FD)("div",{css:y,className:"header-with-actions",children:[(0,c.FD)("div",{className:"title-panel",children:[(0,c.Y)(p,{...e}),t&&(0,c.FD)("div",{css:v,children:[(null==i?void 0:i.certifiedBy)&&(0,c.Y)(u.A,{...i}),n&&(0,c.Y)(g.A,{...l}),d]})]}),(0,c.FD)("div",{className:"right-button-panel",children:[s,(0,c.Y)("div",{css:w,children:$&&(0,c.Y)(o.rM,{trigger:["click"],overlay:h,...x,children:(0,c.Y)(b.A,{css:f,buttonStyle:"tertiary","aria-label":(0,r.t)("Menu actions trigger"),tooltip:null==S?void 0:S.text,placement:null==S?void 0:S.placement,children:(0,c.Y)(m.A.MoreHoriz,{iconColor:Y.colors.primary.dark2,iconSize:"l"})})})})]})]})}},25143:(e,t,i)=>{i.d(t,{S:()=>n.A});var n=i(46740);i(16707)},20473:(e,t,i)=>{i.d(t,{A:()=>v});var n=i(96540),a=i(58561),r=i.n(a),o=i(85861),l=i(49756),d=i(40563),s=i(96453),c=i(35742),h=i(95579),p=i(36255),u=i(85955),g=i(46920),m=i(97567),b=i(2445);const f=s.I4.div`
  .ant-select-dropdown {
    max-height: ${({theme:e})=>40*e.gridUnit}px;
  }
  .tag-input {
    margin-bottom: ${({theme:e})=>3*e.gridUnit}px;
  }
`;var y;!function(e){e.Chart="chart",e.Dashboard="dashboard",e.SavedQuery="query"}(y||(y={}));const v=({show:e,onHide:t,editTag:i,refreshData:a,addSuccessToast:s,addDangerToast:v,clearOnHide:w=!1})=>{const[x,$]=(0,n.useState)([]),[S,Y]=(0,n.useState)([]),[A,T]=(0,n.useState)([]),[k,C]=(0,n.useState)(""),[D,z]=(0,n.useState)(""),E=!!i,I=E?"Edit Tag":"Create Tag",O=()=>{C(""),z(""),$([]),Y([]),T([])};(0,n.useEffect)((()=>{const e={[y.Dashboard]:[],[y.Chart]:[],[y.SavedQuery]:[]},t=({id:t,name:i,type:n})=>{const a=e[n];a&&a.push({value:t,label:i,key:t})};$([]),Y([]),T([]),E&&((0,m.Ik)({tagIds:[i.id],types:null},(i=>{i.forEach(t),$(e[y.Dashboard]),Y(e[y.Chart]),T(e[y.SavedQuery])}),(e=>{v("Error Fetching Tagged Objects")})),C(i.name),z(i.description))}),[i]);const F=async(e,t,i,n,a,o,l)=>{const d=r().encode({columns:n,filters:[{col:a,opr:"ct",value:e}],page:t,order_column:o}),{json:s}=await c.A.get({endpoint:`/api/v1/${l}/?q=${d}`}),{result:h,count:p}=s;return{data:h.map((e=>({value:e.id,label:e[a]}))),totalCount:p}},P=(e,t)=>{e===y.Dashboard?$(t):e===y.Chart?Y(t):e===y.SavedQuery&&T(t)};return(0,b.Y)(o.Ay,{title:I,onHide:()=>{w&&O(),t()},show:e,footer:(0,b.FD)("div",{children:[(0,b.Y)(g.A,{buttonStyle:"secondary",onClick:t,children:(0,h.t)("Cancel")}),(0,b.Y)(g.A,{buttonStyle:"primary",onClick:()=>{const e=x.map((e=>["dashboard",e.value])),n=S.map((e=>["chart",e.value])),r=A.map((e=>["query",e.value]));E?c.A.put({endpoint:`/api/v1/tag/${i.id}`,jsonPayload:{description:D,name:k,objects_to_tag:[...e,...n,...r]}}).then((({json:e={}})=>{a(),O(),s((0,h.t)("Tag updated")),t()})).catch((e=>{v(e.message||"Error Updating Tag")})):c.A.post({endpoint:"/api/v1/tag/",jsonPayload:{description:D,name:k,objects_to_tag:[...e,...n,...r]}}).then((({json:e={}})=>{a(),O(),s((0,h.t)("Tag created")),t()})).catch((e=>v(e.message||"Error Creating Tag")))},children:(0,h.t)("Save")})]}),children:(0,b.FD)(f,{children:[(0,b.Y)(d.lR,{children:(0,h.t)("Tag name")}),(0,b.Y)(p.A,{className:"tag-input",onChange:e=>C(e.target.value),placeholder:(0,h.t)("Name of your tag"),value:k}),(0,b.Y)(d.lR,{children:(0,h.t)("Description")}),(0,b.Y)(p.A,{className:"tag-input",onChange:e=>z(e.target.value),placeholder:(0,h.t)("Add description of your tag"),value:D}),(0,b.Y)(u.c,{}),(0,b.Y)(l.A,{className:"tag-input",ariaLabel:(0,h.t)("Select dashboards"),mode:"multiple",name:"dashboards",value:x,options:async(e,t,i)=>F(e,t,0,["id","dashboard_title"],"dashboard_title","dashboard_title","dashboard"),onChange:e=>P(y.Dashboard,e),header:(0,b.Y)(d.lR,{children:(0,h.t)("Dashboards")}),allowClear:!0}),(0,b.Y)(l.A,{className:"tag-input",ariaLabel:(0,h.t)("Select charts"),mode:"multiple",name:"charts",value:S,options:async(e,t,i)=>F(e,t,0,["id","slice_name"],"slice_name","slice_name","chart"),onChange:e=>P(y.Chart,e),header:(0,b.Y)(d.lR,{children:(0,h.t)("Charts")}),allowClear:!0}),(0,b.Y)(l.A,{className:"tag-input",ariaLabel:(0,h.t)("Select saved queries"),mode:"multiple",name:"savedQueries",value:A,options:async(e,t,i)=>F(e,t,0,["id","label"],"label","label","saved_query"),onChange:e=>P(y.SavedQuery,e),header:(0,b.Y)(d.lR,{children:(0,h.t)("Saved queries")}),allowClear:!0})]})})}},86014:(e,t,i)=>{i.r(t),i.d(t,{default:()=>D});var n=i(96540),a=i(17437),r=i(96453),o=i(95579),l=i(33231),d=i(7089),s=i(50217),c=i(25143),h=i(75841),p=i(50455),u=i(2445);const g=r.I4.div`
  text-align: left;
  border-radius: ${({theme:e})=>1*e.gridUnit}px 0;
  .table {
    table-layout: fixed;
  }
  .td {
    width: 33%;
  }
  .entity-title {
    font-family: Inter;
    font-size: ${({theme:e})=>e.typography.sizes.m}px;
    font-weight: ${({theme:e})=>e.typography.weights.medium};
    line-height: 17px;
    letter-spacing: 0px;
    text-align: left;
    margin: ${({theme:e})=>4*e.gridUnit}px 0;
  }
`;function m({search:e="",setShowTagModal:t,objects:i,canEditTag:n}){const[a]=(0,l.pE)("id",l.hc),r=i.dashboard.length>0,m=i.chart.length>0,b=i.query.length>0,f=r||m||b,y=e=>{const t=i[e].map((t=>({[e]:(0,u.Y)("a",{href:t.url,children:t.name}),modified:d.XV.utc(t.changed_on).fromNow(),tags:t.tags,owners:t.owners})));return(0,u.Y)(s.A,{className:"table-condensed",emptyWrapperType:s.V.Small,data:t,pageSize:10,columns:[{accessor:e,Header:"Title"},{Cell:({row:{original:{tags:e=[]}}})=>(0,u.Y)(c.S,{tags:e.filter((e=>void 0!==e.type&&["TagType.custom",1].includes(e.type)&&e.id!==a)),maxTags:3}),Header:(0,o.t)("Tags"),accessor:"tags",disableSortBy:!0},{Cell:({row:{original:{owners:e=[]}}})=>(0,u.Y)(h.A,{users:e}),Header:(0,o.t)("Owners"),accessor:"owners",disableSortBy:!0,size:"xl"}]})};return(0,u.Y)(g,{children:f?(0,u.FD)(u.FK,{children:[r&&(0,u.FD)(u.FK,{children:[(0,u.Y)("div",{className:"entity-title",children:(0,o.t)("Dashboards")}),y("dashboard")]}),m&&(0,u.FD)(u.FK,{children:[(0,u.Y)("div",{className:"entity-title",children:(0,o.t)("Charts")}),y("chart")]}),b&&(0,u.FD)(u.FK,{children:[(0,u.Y)("div",{className:"entity-title",children:(0,o.t)("Queries")}),y("query")]})]}):(0,u.Y)(p.p,{image:"dashboard.svg",size:"large",title:(0,o.t)("No entities have this tag currently assigned"),...n&&{buttonAction:()=>t(!0),buttonText:(0,o.t)("Add tag to entities")}})})}var b=i(46920),f=i(14693),y=i(51848),v=i(20473),w=i(5261),x=i(97567),$=i(17444),S=i(25106),Y=i(84666),A=i(61225);const T=e=>a.AH`
  display: flex;
  align-items: center;
  margin-left: ${e.gridUnit}px;
  & > span {
    margin-right: ${3*e.gridUnit}px;
  }
`,k=r.I4.div`
  ${({theme:e})=>`\n  background-color: ${e.colors.grayscale.light4};\n  .select-control {\n    margin-left: ${4*e.gridUnit}px;\n    margin-right: ${4*e.gridUnit}px;\n    margin-bottom: ${2*e.gridUnit}px;\n  }\n  .select-control-label {\n    font-size: ${3*e.gridUnit}px;\n    color: ${e.colors.grayscale.base};\n    margin-bottom: ${1*e.gridUnit}px;\n  }\n  .entities {\n    margin: ${6*e.gridUnit}px; 0px;\n  }\n  .pagination-container {\n    background-color: transparent;\n  }\n  `}
`,C=r.I4.div`
  ${({theme:e})=>`\n  height: ${12.5*e.gridUnit}px;\n  background-color: ${e.colors.grayscale.light5};\n  margin-bottom: ${4*e.gridUnit}px;\n  .navbar-brand {\n    margin-left: ${2*e.gridUnit}px;\n    font-weight: ${e.typography.weights.bold};\n  }\n  .header {\n    font-weight: ${e.typography.weights.bold};\n    margin-right:  ${3*e.gridUnit}px;\n    text-align: left;\n    font-size: ${4.5*e.gridUnit}px;\n    padding: ${3*e.gridUnit}px;\n    display: inline-block;\n    line-height: ${9*e.gridUnit}px;\n  }\n  `};
`,D=(0,w.Ay)((function(){const[e]=(0,l.pE)("id",l.hc),[t,i]=(0,n.useState)(null),[a,r]=(0,n.useState)(!1),{addSuccessToast:d,addDangerToast:s}=(0,w.Yf)(),[c,h]=(0,n.useState)(!1),[p,g]=(0,n.useState)({dashboard:[],chart:[],query:[]}),D=(0,A.d4)((e=>{var t;return(0,Y.L)("can_write","Tag",null==(t=e.user)?void 0:t.roles)})),z={title:(null==t?void 0:t.name)||"",placeholder:"testing",onSave:e=>{},canEdit:!1,label:(0,o.t)("dataset name")},E=[];if(null!=t&&t.description){const e={type:f.QD.Description,value:(null==t?void 0:t.description)||""};E.push(e)}const I={type:f.QD.Owner,createdBy:(0,S.A)(null==t?void 0:t.created_by),createdOn:(null==t?void 0:t.created_on_delta_humanized)||""};E.push(I);const O={type:f.QD.LastModified,value:(null==t?void 0:t.changed_on_delta_humanized)||"",modifiedBy:(0,S.A)(null==t?void 0:t.changed_by)};E.push(O);const F=()=>{h(!0),t?(0,x.Ik)({tagIds:void 0!==(null==t?void 0:t.id)?[t.id]:"",types:null},(e=>{const t={dashboard:[],chart:[],query:[]};e.forEach((function(e){const i=e.type;t[i].push(e)})),g(t),h(!1)}),(e=>{s("Error Fetching Tagged Objects"),h(!1)})):s("Error tag object is not referenced!")},P=e=>{(0,x.FA)(e,(e=>{i(e),h(!1)}),(e=>{s((0,o.t)("Error Fetching Tagged Objects")),h(!1)}))};return(0,n.useEffect)((()=>{e&&(h(!0),P(e))}),[e]),(0,n.useEffect)((()=>{t&&F()}),[t]),c?(0,u.Y)($.A,{}):(0,u.FD)(k,{children:[(0,u.Y)(v.A,{show:a,onHide:()=>{r(!1)},editTag:t,addSuccessToast:d,addDangerToast:s,refreshData:()=>{F(),e&&P(e)}}),(0,u.Y)(C,{children:(0,u.Y)(y.U,{additionalActionsMenu:(0,u.Y)(u.FK,{}),editableTitleProps:z,faveStarProps:{itemId:1,saveFaveStar:()=>{}},showFaveStar:!1,showTitlePanelItems:!0,titlePanelAdditionalItems:(0,u.Y)("div",{css:T,children:(0,u.Y)(f.Ay,{items:E,tooltipPlacement:"bottom"})}),rightPanelAdditionalItems:(0,u.Y)(u.FK,{children:D&&(0,u.FD)(b.A,{buttonStyle:"secondary",onClick:()=>r(!0),showMarginRight:!1,children:[(0,o.t)("Edit tag")," "]})}),menuDropdownProps:{disabled:!0},showMenuDropdown:!1})}),(0,u.Y)("div",{className:"entities",children:(0,u.Y)(m,{search:(null==t?void 0:t.name)||"",setShowTagModal:r,objects:p,canEditTag:D})})]})}))}}]);