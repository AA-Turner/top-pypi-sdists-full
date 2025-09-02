"use strict";(self.webpackChunkknx_frontend=self.webpackChunkknx_frontend||[]).push([["3956"],{32780:function(e,t,a){a(39710),a(26847),a(2394),a(44438),a(18574),a(81738),a(94814),a(29981),a(22960),a(6989),a(93190),a(72489),a(1455),a(56389),a(20655),a(40589),a(27530);var o=a(73742),l=a(1521),i=a(59048),r=a(7616),d=a(31733),s=a(25191),c=a(20480),n=a(28105),h=a(40985),_=a(29740),u=a(92949),p=a(16811);const m=(e,t)=>{const a={};for(const o of e){const e=t(o);e in a?a[e].push(o):a[e]=[o]}return a};var b=a(77204),f=a(65682),v=(a(86776),a(40830),a(40850),a(41465),a(34845),a(73249),a(36330),a(38221),a(75863),a(86190));let g;const w=()=>(g||(g=(0,v.Ud)(new Worker(new URL(a.p+a.u("1358"),a.b)))),g);var y=a(98012);let x,k,C,$,R,L,S,D,z,O,I,B,T,G,H,F,W,M=e=>e;const A="zzzzz_undefined";class E extends i.oi{clearSelection(){this._checkedRows=[],this._lastSelectedRowId=null,this._checkedRowsChanged()}selectAll(){this._checkedRows=this._filteredData.filter((e=>!1!==e.selectable)).map((e=>e[this.id])),this._lastSelectedRowId=null,this._checkedRowsChanged()}select(e,t){t&&(this._checkedRows=[]),e.forEach((e=>{const t=this._filteredData.find((t=>t[this.id]===e));!1===(null==t?void 0:t.selectable)||this._checkedRows.includes(e)||this._checkedRows.push(e)})),this._lastSelectedRowId=null,this._checkedRowsChanged()}unselect(e){e.forEach((e=>{const t=this._checkedRows.indexOf(e);t>-1&&this._checkedRows.splice(t,1)})),this._lastSelectedRowId=null,this._checkedRowsChanged()}connectedCallback(){super.connectedCallback(),this._filteredData.length&&(this._filteredData=[...this._filteredData])}firstUpdated(){this.updateComplete.then((()=>this._calcTableHeight()))}updated(){const e=this.renderRoot.querySelector(".mdc-data-table__header-row");e&&(e.scrollWidth>e.clientWidth?this.style.setProperty("--table-row-width",`${e.scrollWidth}px`):this.style.removeProperty("--table-row-width"))}willUpdate(e){if(super.willUpdate(e),this.hasUpdated||(0,f.o)(),e.has("columns")){if(this._filterable=Object.values(this.columns).some((e=>e.filterable)),!this.sortColumn)for(const t in this.columns)if(this.columns[t].direction){this.sortDirection=this.columns[t].direction,this.sortColumn=t,this._lastSelectedRowId=null,(0,_.B)(this,"sorting-changed",{column:t,direction:this.sortDirection});break}const e=(0,l.Z)(this.columns);Object.values(e).forEach((e=>{delete e.title,delete e.template,delete e.extraTemplate})),this._sortColumns=e}e.has("filter")&&(this._debounceSearch(this.filter),this._lastSelectedRowId=null),e.has("data")&&(this._checkableRowsCount=this.data.filter((e=>!1!==e.selectable)).length),!this.hasUpdated&&this.initialCollapsedGroups?(this._collapsedGroups=this.initialCollapsedGroups,this._lastSelectedRowId=null,(0,_.B)(this,"collapsed-changed",{value:this._collapsedGroups})):e.has("groupColumn")&&(this._collapsedGroups=[],this._lastSelectedRowId=null,(0,_.B)(this,"collapsed-changed",{value:this._collapsedGroups})),(e.has("data")||e.has("columns")||e.has("_filter")||e.has("sortColumn")||e.has("sortDirection"))&&this._sortFilterData(),(e.has("_filter")||e.has("sortColumn")||e.has("sortDirection"))&&(this._lastSelectedRowId=null),(e.has("selectable")||e.has("hiddenColumns"))&&(this._filteredData=[...this._filteredData])}render(){const e=this.localizeFunc||this.hass.localize,t=this._sortedColumns(this.columns,this.columnOrder);return(0,i.dy)(x||(x=M`
      <div class="mdc-data-table">
        <slot name="header" @slotchange=${0}>
          ${0}
        </slot>
        <div
          class="mdc-data-table__table ${0}"
          role="table"
          aria-rowcount=${0}
          style=${0}
        >
          <div
            class="mdc-data-table__header-row"
            role="row"
            aria-rowindex="1"
            @scroll=${0}
          >
            <slot name="header-row">
              ${0}
              ${0}
            </slot>
          </div>
          ${0}
        </div>
      </div>
    `),this._calcTableHeight,this._filterable?(0,i.dy)(k||(k=M`
                <div class="table-header">
                  <search-input
                    .hass=${0}
                    @value-changed=${0}
                    .label=${0}
                    .noLabelFloat=${0}
                  ></search-input>
                </div>
              `),this.hass,this._handleSearchChange,this.searchLabel,this.noLabelFloat):"",(0,d.$)({"auto-height":this.autoHeight}),this._filteredData.length+1,(0,c.V)({height:this.autoHeight?53*(this._filteredData.length||1)+53+"px":`calc(100% - ${this._headerHeight}px)`}),this._scrollContent,this.selectable?(0,i.dy)(C||(C=M`
                    <div
                      class="mdc-data-table__header-cell mdc-data-table__header-cell--checkbox"
                      role="columnheader"
                    >
                      <ha-checkbox
                        class="mdc-data-table__row-checkbox"
                        @change=${0}
                        .indeterminate=${0}
                        .checked=${0}
                      >
                      </ha-checkbox>
                    </div>
                  `),this._handleHeaderRowCheckboxClick,this._checkedRows.length&&this._checkedRows.length!==this._checkableRowsCount,this._checkedRows.length&&this._checkedRows.length===this._checkableRowsCount):"",Object.entries(t).map((([e,t])=>{var a,o;if(t.hidden||(this.columnOrder&&this.columnOrder.includes(e)&&null!==(a=null===(o=this.hiddenColumns)||void 0===o?void 0:o.includes(e))&&void 0!==a?a:t.defaultHidden))return i.Ld;const l=e===this.sortColumn,r={"mdc-data-table__header-cell--numeric":"numeric"===t.type,"mdc-data-table__header-cell--icon":"icon"===t.type,"mdc-data-table__header-cell--icon-button":"icon-button"===t.type,"mdc-data-table__header-cell--overflow-menu":"overflow-menu"===t.type,"mdc-data-table__header-cell--overflow":"overflow"===t.type,sortable:Boolean(t.sortable),"not-sorted":Boolean(t.sortable&&!l)};return(0,i.dy)($||($=M`
                  <div
                    aria-label=${0}
                    class="mdc-data-table__header-cell ${0}"
                    style=${0}
                    role="columnheader"
                    aria-sort=${0}
                    @click=${0}
                    .columnId=${0}
                    title=${0}
                  >
                    ${0}
                    <span>${0}</span>
                  </div>
                `),(0,s.o)(t.label),(0,d.$)(r),(0,c.V)({minWidth:t.minWidth,maxWidth:t.maxWidth,flex:t.flex||1}),(0,s.o)(l?"desc"===this.sortDirection?"descending":"ascending":void 0),this._handleHeaderClick,e,(0,s.o)(t.title),t.sortable?(0,i.dy)(R||(R=M`
                          <ha-svg-icon
                            .path=${0}
                          ></ha-svg-icon>
                        `),l&&"desc"===this.sortDirection?"M11,4H13V16L18.5,10.5L19.92,11.92L12,19.84L4.08,11.92L5.5,10.5L11,16V4Z":"M13,20H11V8L5.5,13.5L4.08,12.08L12,4.16L19.92,12.08L18.5,13.5L13,8V20Z"):"",t.title)})),this._filteredData.length?(0,i.dy)(S||(S=M`
                <lit-virtualizer
                  scroller
                  class="mdc-data-table__content scroller ha-scrollbar"
                  @scroll=${0}
                  .items=${0}
                  .keyFunction=${0}
                  .renderItem=${0}
                ></lit-virtualizer>
              `),this._saveScrollPos,this._groupData(this._filteredData,e,this.appendRow,this.hasFab,this.groupColumn,this.groupOrder,this._collapsedGroups,this.sortColumn,this.sortDirection),this._keyFunction,((e,a)=>this._renderRow(t,this.narrow,e,a))):(0,i.dy)(L||(L=M`
                <div class="mdc-data-table__content">
                  <div class="mdc-data-table__row" role="row">
                    <div class="mdc-data-table__cell grows center" role="cell">
                      ${0}
                    </div>
                  </div>
                </div>
              `),this.noDataText||e("ui.components.data-table.no-data")))}async _sortFilterData(){const e=(new Date).getTime(),t=e-this._lastUpdate,a=e-this._curRequest;this._curRequest=e;const o=!this._lastUpdate||t>500&&a<500;let l=this.data;if(this._filter&&(l=await this._memFilterData(this.data,this._sortColumns,this._filter.trim())),!o&&this._curRequest!==e)return;const i=this.sortColumn&&this._sortColumns[this.sortColumn]?((e,t,a,o,l)=>w().sortData(e,t,a,o,l))(l,this._sortColumns[this.sortColumn],this.sortDirection,this.sortColumn,this.hass.locale.language):l,[r]=await Promise.all([i,y.y]),d=(new Date).getTime()-e;d<100&&await new Promise((e=>{setTimeout(e,100-d)})),(o||this._curRequest===e)&&(this._lastUpdate=e,this._filteredData=r)}_handleHeaderClick(e){const t=e.currentTarget.columnId;this.columns[t].sortable&&(this.sortDirection&&this.sortColumn===t?"asc"===this.sortDirection?this.sortDirection="desc":this.sortDirection=null:this.sortDirection="asc",this.sortColumn=null===this.sortDirection?void 0:t,(0,_.B)(this,"sorting-changed",{column:t,direction:this.sortDirection}))}_handleHeaderRowCheckboxClick(e){e.target.checked?this.selectAll():(this._checkedRows=[],this._checkedRowsChanged()),this._lastSelectedRowId=null}_selectRange(e,t,a){const o=Math.min(t,a),l=Math.max(t,a),i=[];for(let r=o;r<=l;r++){const t=e[r];t&&!1!==t.selectable&&!this._checkedRows.includes(t[this.id])&&i.push(t[this.id])}return i}_setTitle(e){const t=e.currentTarget;t.scrollWidth>t.offsetWidth&&t.setAttribute("title",t.innerText)}_checkedRowsChanged(){this._filteredData.length&&(this._filteredData=[...this._filteredData]),(0,_.B)(this,"selection-changed",{value:this._checkedRows})}_handleSearchChange(e){this.filter||(this._lastSelectedRowId=null,this._debounceSearch(e.detail.value))}async _calcTableHeight(){this.autoHeight||(await this.updateComplete,this._headerHeight=this._header.clientHeight)}_saveScrollPos(e){this._savedScrollPos=e.target.scrollTop,this.renderRoot.querySelector(".mdc-data-table__header-row").scrollLeft=e.target.scrollLeft}_scrollContent(e){this.renderRoot.querySelector("lit-virtualizer").scrollLeft=e.target.scrollLeft}expandAllGroups(){this._collapsedGroups=[],this._lastSelectedRowId=null,(0,_.B)(this,"collapsed-changed",{value:this._collapsedGroups})}collapseAllGroups(){if(!this.groupColumn||!this.data.some((e=>e[this.groupColumn])))return;const e=m(this.data,(e=>e[this.groupColumn]));e.undefined&&(e[A]=e.undefined,delete e.undefined),this._collapsedGroups=Object.keys(e),this._lastSelectedRowId=null,(0,_.B)(this,"collapsed-changed",{value:this._collapsedGroups})}static get styles(){return[b.$c,(0,i.iv)(D||(D=M`
        /* default mdc styles, colors changed, without checkbox styles */
        :host {
          height: 100%;
        }
        .mdc-data-table__content {
          font-family: var(--ha-font-family-body);
          -moz-osx-font-smoothing: var(--ha-moz-osx-font-smoothing);
          -webkit-font-smoothing: var(--ha-font-smoothing);
          font-size: 0.875rem;
          line-height: var(--ha-line-height-condensed);
          font-weight: var(--ha-font-weight-normal);
          letter-spacing: 0.0178571429em;
          text-decoration: inherit;
          text-transform: inherit;
        }

        .mdc-data-table {
          background-color: var(--data-table-background-color);
          border-radius: 4px;
          border-width: 1px;
          border-style: solid;
          border-color: var(--divider-color);
          display: inline-flex;
          flex-direction: column;
          box-sizing: border-box;
          overflow: hidden;
        }

        .mdc-data-table__row--selected {
          background-color: rgba(var(--rgb-primary-color), 0.04);
        }

        .mdc-data-table__row {
          display: flex;
          height: var(--data-table-row-height, 52px);
          width: var(--table-row-width, 100%);
        }

        .mdc-data-table__row.empty-row {
          height: var(
            --data-table-empty-row-height,
            var(--data-table-row-height, 52px)
          );
        }

        .mdc-data-table__row ~ .mdc-data-table__row {
          border-top: 1px solid var(--divider-color);
        }

        .mdc-data-table__row.clickable:not(
            .mdc-data-table__row--selected
          ):hover {
          background-color: rgba(var(--rgb-primary-text-color), 0.04);
        }

        .mdc-data-table__header-cell {
          color: var(--primary-text-color);
        }

        .mdc-data-table__cell {
          color: var(--primary-text-color);
        }

        .mdc-data-table__header-row {
          height: 56px;
          display: flex;
          border-bottom: 1px solid var(--divider-color);
          overflow: auto;
        }

        /* Hide scrollbar for Chrome, Safari and Opera */
        .mdc-data-table__header-row::-webkit-scrollbar {
          display: none;
        }

        /* Hide scrollbar for IE, Edge and Firefox */
        .mdc-data-table__header-row {
          -ms-overflow-style: none; /* IE and Edge */
          scrollbar-width: none; /* Firefox */
        }

        .mdc-data-table__cell,
        .mdc-data-table__header-cell {
          padding-right: 16px;
          padding-left: 16px;
          min-width: 150px;
          align-self: center;
          overflow: hidden;
          text-overflow: ellipsis;
          flex-shrink: 0;
          box-sizing: border-box;
        }

        .mdc-data-table__cell.mdc-data-table__cell--flex {
          display: flex;
          overflow: initial;
        }

        .mdc-data-table__cell.mdc-data-table__cell--icon {
          overflow: initial;
        }

        .mdc-data-table__header-cell--checkbox,
        .mdc-data-table__cell--checkbox {
          /* @noflip */
          padding-left: 16px;
          /* @noflip */
          padding-right: 0;
          /* @noflip */
          padding-inline-start: 16px;
          /* @noflip */
          padding-inline-end: initial;
          width: 60px;
          min-width: 60px;
        }

        .mdc-data-table__table {
          height: 100%;
          width: 100%;
          border: 0;
          white-space: nowrap;
          position: relative;
        }

        .mdc-data-table__cell {
          font-family: var(--ha-font-family-body);
          -moz-osx-font-smoothing: var(--ha-moz-osx-font-smoothing);
          -webkit-font-smoothing: var(--ha-font-smoothing);
          font-size: 0.875rem;
          line-height: var(--ha-line-height-condensed);
          font-weight: var(--ha-font-weight-normal);
          letter-spacing: 0.0178571429em;
          text-decoration: inherit;
          text-transform: inherit;
          flex-grow: 0;
          flex-shrink: 0;
        }

        .mdc-data-table__cell a {
          color: inherit;
          text-decoration: none;
        }

        .mdc-data-table__cell--numeric {
          text-align: var(--float-end);
        }

        .mdc-data-table__cell--icon {
          color: var(--secondary-text-color);
          text-align: center;
        }

        .mdc-data-table__header-cell--icon,
        .mdc-data-table__cell--icon {
          min-width: 64px;
          flex: 0 0 64px !important;
        }

        .mdc-data-table__cell--icon img {
          width: 24px;
          height: 24px;
        }

        .mdc-data-table__header-cell.mdc-data-table__header-cell--icon {
          text-align: center;
        }

        .mdc-data-table__header-cell.sortable.mdc-data-table__header-cell--icon:hover,
        .mdc-data-table__header-cell.sortable.mdc-data-table__header-cell--icon:not(
            .not-sorted
          ) {
          text-align: var(--float-start);
        }

        .mdc-data-table__cell--icon:first-child img,
        .mdc-data-table__cell--icon:first-child ha-icon,
        .mdc-data-table__cell--icon:first-child ha-svg-icon,
        .mdc-data-table__cell--icon:first-child ha-state-icon,
        .mdc-data-table__cell--icon:first-child ha-domain-icon,
        .mdc-data-table__cell--icon:first-child ha-service-icon {
          margin-left: 8px;
          margin-inline-start: 8px;
          margin-inline-end: initial;
        }

        .mdc-data-table__cell--icon:first-child state-badge {
          margin-right: -8px;
          margin-inline-end: -8px;
          margin-inline-start: initial;
        }

        .mdc-data-table__cell--overflow-menu,
        .mdc-data-table__header-cell--overflow-menu,
        .mdc-data-table__header-cell--icon-button,
        .mdc-data-table__cell--icon-button {
          min-width: 64px;
          flex: 0 0 64px !important;
          padding: 8px;
        }

        .mdc-data-table__header-cell--icon-button,
        .mdc-data-table__cell--icon-button {
          min-width: 56px;
          width: 56px;
        }

        .mdc-data-table__cell--overflow-menu,
        .mdc-data-table__cell--icon-button {
          color: var(--secondary-text-color);
          text-overflow: clip;
        }

        .mdc-data-table__header-cell--icon-button:first-child,
        .mdc-data-table__cell--icon-button:first-child,
        .mdc-data-table__header-cell--icon-button:last-child,
        .mdc-data-table__cell--icon-button:last-child {
          width: 64px;
        }

        .mdc-data-table__cell--overflow-menu:first-child,
        .mdc-data-table__header-cell--overflow-menu:first-child,
        .mdc-data-table__header-cell--icon-button:first-child,
        .mdc-data-table__cell--icon-button:first-child {
          padding-left: 16px;
          padding-inline-start: 16px;
          padding-inline-end: initial;
        }

        .mdc-data-table__cell--overflow-menu:last-child,
        .mdc-data-table__header-cell--overflow-menu:last-child,
        .mdc-data-table__header-cell--icon-button:last-child,
        .mdc-data-table__cell--icon-button:last-child {
          padding-right: 16px;
          padding-inline-end: 16px;
          padding-inline-start: initial;
        }
        .mdc-data-table__cell--overflow-menu,
        .mdc-data-table__cell--overflow,
        .mdc-data-table__header-cell--overflow-menu,
        .mdc-data-table__header-cell--overflow {
          overflow: initial;
        }
        .mdc-data-table__cell--icon-button a {
          color: var(--secondary-text-color);
        }

        .mdc-data-table__header-cell {
          font-family: var(--ha-font-family-body);
          -moz-osx-font-smoothing: var(--ha-moz-osx-font-smoothing);
          -webkit-font-smoothing: var(--ha-font-smoothing);
          font-size: var(--ha-font-size-s);
          line-height: var(--ha-line-height-normal);
          font-weight: var(--ha-font-weight-medium);
          letter-spacing: 0.0071428571em;
          text-decoration: inherit;
          text-transform: inherit;
          text-align: var(--float-start);
        }

        .mdc-data-table__header-cell--numeric {
          text-align: var(--float-end);
        }
        .mdc-data-table__header-cell--numeric.sortable:hover,
        .mdc-data-table__header-cell--numeric.sortable:not(.not-sorted) {
          text-align: var(--float-start);
        }

        /* custom from here */

        .group-header {
          padding-top: 12px;
          height: var(--data-table-row-height, 52px);
          padding-left: 12px;
          padding-inline-start: 12px;
          padding-inline-end: initial;
          width: 100%;
          font-weight: var(--ha-font-weight-medium);
          display: flex;
          align-items: center;
          cursor: pointer;
          background-color: var(--primary-background-color);
        }

        .group-header ha-icon-button {
          transition: transform 0.2s ease;
        }

        .group-header ha-icon-button.collapsed {
          transform: rotate(180deg);
        }

        :host {
          display: block;
        }

        .mdc-data-table {
          display: block;
          border-width: var(--data-table-border-width, 1px);
          height: 100%;
        }
        .mdc-data-table__header-cell {
          overflow: hidden;
          position: relative;
        }
        .mdc-data-table__header-cell span {
          position: relative;
          left: 0px;
          inset-inline-start: 0px;
          inset-inline-end: initial;
        }

        .mdc-data-table__header-cell.sortable {
          cursor: pointer;
        }
        .mdc-data-table__header-cell > * {
          transition: var(--float-start) 0.2s ease;
        }
        .mdc-data-table__header-cell ha-svg-icon {
          top: -3px;
          position: absolute;
        }
        .mdc-data-table__header-cell.not-sorted ha-svg-icon {
          left: -20px;
          inset-inline-start: -20px;
          inset-inline-end: initial;
        }
        .mdc-data-table__header-cell.sortable:not(.not-sorted) span,
        .mdc-data-table__header-cell.sortable.not-sorted:hover span {
          left: 24px;
          inset-inline-start: 24px;
          inset-inline-end: initial;
        }
        .mdc-data-table__header-cell.sortable:not(.not-sorted) ha-svg-icon,
        .mdc-data-table__header-cell.sortable:hover.not-sorted ha-svg-icon {
          left: 12px;
          inset-inline-start: 12px;
          inset-inline-end: initial;
        }
        .table-header {
          border-bottom: 1px solid var(--divider-color);
        }
        search-input {
          display: block;
          flex: 1;
          --mdc-text-field-fill-color: var(--sidebar-background-color);
          --mdc-text-field-idle-line-color: transparent;
        }
        slot[name="header"] {
          display: block;
        }
        .center {
          text-align: center;
        }
        .secondary {
          color: var(--secondary-text-color);
        }
        .scroller {
          height: calc(100% - 57px);
          overflow: overlay !important;
        }

        .mdc-data-table__table.auto-height .scroller {
          overflow-y: hidden !important;
        }
        .grows {
          flex-grow: 1;
          flex-shrink: 1;
        }
        .forceLTR {
          direction: ltr;
        }
        .clickable {
          cursor: pointer;
        }
        lit-virtualizer {
          contain: size layout !important;
          overscroll-behavior: contain;
        }
      `))]}constructor(...e){super(...e),this.narrow=!1,this.columns={},this.data=[],this.selectable=!1,this.clickable=!1,this.hasFab=!1,this.autoHeight=!1,this.id="id",this.noLabelFloat=!1,this.filter="",this.sortDirection=null,this._filterable=!1,this._filter="",this._filteredData=[],this._headerHeight=0,this._collapsedGroups=[],this._lastSelectedRowId=null,this._checkedRows=[],this._sortColumns={},this._curRequest=0,this._lastUpdate=0,this._debounceSearch=(0,p.D)((e=>{this._filter=e}),100,!1),this._sortedColumns=(0,n.Z)(((e,t)=>t&&t.length?Object.keys(e).sort(((e,a)=>{const o=t.indexOf(e),l=t.indexOf(a);if(o!==l){if(-1===o)return 1;if(-1===l)return-1}return o-l})).reduce(((t,a)=>(t[a]=e[a],t)),{}):e)),this._keyFunction=e=>(null==e?void 0:e[this.id])||e,this._renderRow=(e,t,a,o)=>a?a.append?(0,i.dy)(z||(z=M`<div class="mdc-data-table__row">${0}</div>`),a.content):a.empty?(0,i.dy)(O||(O=M`<div class="mdc-data-table__row empty-row"></div>`)):(0,i.dy)(I||(I=M`
      <div
        aria-rowindex=${0}
        role="row"
        .rowId=${0}
        @click=${0}
        class="mdc-data-table__row ${0}"
        aria-selected=${0}
        .selectable=${0}
      >
        ${0}
        ${0}
      </div>
    `),o+2,a[this.id],this._handleRowClick,(0,d.$)({"mdc-data-table__row--selected":this._checkedRows.includes(String(a[this.id])),clickable:this.clickable}),(0,s.o)(!!this._checkedRows.includes(String(a[this.id]))||void 0),!1!==a.selectable,this.selectable?(0,i.dy)(B||(B=M`
              <div
                class="mdc-data-table__cell mdc-data-table__cell--checkbox"
                role="cell"
              >
                <ha-checkbox
                  class="mdc-data-table__row-checkbox"
                  @click=${0}
                  .rowId=${0}
                  .disabled=${0}
                  .checked=${0}
                >
                </ha-checkbox>
              </div>
            `),this._handleRowCheckboxClicked,a[this.id],!1===a.selectable,this._checkedRows.includes(String(a[this.id]))):"",Object.entries(e).map((([o,l])=>{var r,s;return t&&!l.main&&!l.showNarrow||l.hidden||(this.columnOrder&&this.columnOrder.includes(o)&&null!==(r=null===(s=this.hiddenColumns)||void 0===s?void 0:s.includes(o))&&void 0!==r?r:l.defaultHidden)?i.Ld:(0,i.dy)(T||(T=M`
            <div
              @mouseover=${0}
              @focus=${0}
              role=${0}
              class="mdc-data-table__cell ${0}"
              style=${0}
            >
              ${0}
            </div>
          `),this._setTitle,this._setTitle,l.main?"rowheader":"cell",(0,d.$)({"mdc-data-table__cell--flex":"flex"===l.type,"mdc-data-table__cell--numeric":"numeric"===l.type,"mdc-data-table__cell--icon":"icon"===l.type,"mdc-data-table__cell--icon-button":"icon-button"===l.type,"mdc-data-table__cell--overflow-menu":"overflow-menu"===l.type,"mdc-data-table__cell--overflow":"overflow"===l.type,forceLTR:Boolean(l.forceLTR)}),(0,c.V)({minWidth:l.minWidth,maxWidth:l.maxWidth,flex:l.flex||1}),l.template?l.template(a):t&&l.main?(0,i.dy)(G||(G=M`<div class="primary">${0}</div>
                      <div class="secondary">
                        ${0}
                      </div>
                      ${0}`),a[o],Object.entries(e).filter((([e,t])=>{var a,o;return!(t.hidden||t.main||t.showNarrow||(this.columnOrder&&this.columnOrder.includes(e)&&null!==(a=null===(o=this.hiddenColumns)||void 0===o?void 0:o.includes(e))&&void 0!==a?a:t.defaultHidden))})).map((([e,t],o)=>(0,i.dy)(H||(H=M`${0}${0}`),0!==o?" · ":i.Ld,t.template?t.template(a):a[e]))),l.extraTemplate?l.extraTemplate(a):i.Ld):(0,i.dy)(F||(F=M`${0}${0}`),a[o],l.extraTemplate?l.extraTemplate(a):i.Ld))}))):i.Ld,this._groupData=(0,n.Z)(((e,t,a,o,l,r,d,s,c)=>{if(a||o||l){let n=[...e];if(l){const e=s===l,a=m(n,(e=>e[l]));a.undefined&&(a[A]=a.undefined,delete a.undefined);const o=Object.keys(a).sort(((t,a)=>{var o,l;if(!r&&e){const e=(0,u.$K)(t,a,this.hass.locale.language);return"asc"===c?e:-1*e}const i=null!==(o=null==r?void 0:r.indexOf(t))&&void 0!==o?o:-1,d=null!==(l=null==r?void 0:r.indexOf(a))&&void 0!==l?l:-1;return i!==d?-1===i?1:-1===d?-1:i-d:(0,u.$K)(["","-","—"].includes(t)?"zzz":t,["","-","—"].includes(a)?"zzz":a,this.hass.locale.language)})).reduce(((e,t)=>{const o=[t,a[t]];return e.push(o),e}),[]),h=[];o.forEach((([e,a])=>{const o=d.includes(e);h.push({append:!0,selectable:!1,content:(0,i.dy)(W||(W=M`<div
                class="mdc-data-table__cell group-header"
                role="cell"
                .group=${0}
                @click=${0}
              >
                <ha-icon-button
                  .path=${0}
                  .label=${0}
                  class=${0}
                >
                </ha-icon-button>
                ${0}
              </div>`),e,this._collapseGroup,"M7.41,15.41L12,10.83L16.59,15.41L18,14L12,8L6,14L7.41,15.41Z",this.hass.localize("ui.components.data-table."+(o?"expand":"collapse")),o?"collapsed":"",e===A?t("ui.components.data-table.ungrouped"):e||"")}),d.includes(e)||h.push(...a)})),n=h}return a&&n.push({append:!0,selectable:!1,content:a}),o&&n.push({empty:!0}),n}return e})),this._memFilterData=(0,n.Z)(((e,t,a)=>((e,t,a)=>w().filterData(e,t,a))(e,t,a))),this._handleRowCheckboxClicked=e=>{var t;const a=e.currentTarget,o=a.rowId,l=this._groupData(this._filteredData,this.localizeFunc||this.hass.localize,this.appendRow,this.hasFab,this.groupColumn,this.groupOrder,this._collapsedGroups,this.sortColumn,this.sortDirection);if(!1===(null===(t=l.find((e=>e[this.id]===o)))||void 0===t?void 0:t.selectable))return;const i=l.findIndex((e=>e[this.id]===o));if(e instanceof MouseEvent&&e.shiftKey&&null!==this._lastSelectedRowId){const e=l.findIndex((e=>e[this.id]===this._lastSelectedRowId));e>-1&&i>-1&&(this._checkedRows=[...this._checkedRows,...this._selectRange(l,e,i)])}else a.checked?this._checkedRows=this._checkedRows.filter((e=>e!==o)):this._checkedRows.includes(o)||(this._checkedRows=[...this._checkedRows,o]);i>-1&&(this._lastSelectedRowId=o),this._checkedRowsChanged()},this._handleRowClick=e=>{if(e.composedPath().find((e=>["ha-checkbox","ha-button","ha-button","ha-icon-button","ha-assist-chip"].includes(e.localName))))return;const t=e.currentTarget.rowId;(0,_.B)(this,"row-click",{id:t},{bubbles:!1})},this._collapseGroup=e=>{const t=e.currentTarget.group;this._collapsedGroups.includes(t)?this._collapsedGroups=this._collapsedGroups.filter((e=>e!==t)):this._collapsedGroups=[...this._collapsedGroups,t],this._lastSelectedRowId=null,(0,_.B)(this,"collapsed-changed",{value:this._collapsedGroups})}}}(0,o.__decorate)([(0,r.Cb)({attribute:!1})],E.prototype,"hass",void 0),(0,o.__decorate)([(0,r.Cb)({attribute:!1})],E.prototype,"localizeFunc",void 0),(0,o.__decorate)([(0,r.Cb)({type:Boolean})],E.prototype,"narrow",void 0),(0,o.__decorate)([(0,r.Cb)({type:Object})],E.prototype,"columns",void 0),(0,o.__decorate)([(0,r.Cb)({type:Array})],E.prototype,"data",void 0),(0,o.__decorate)([(0,r.Cb)({type:Boolean})],E.prototype,"selectable",void 0),(0,o.__decorate)([(0,r.Cb)({type:Boolean})],E.prototype,"clickable",void 0),(0,o.__decorate)([(0,r.Cb)({attribute:"has-fab",type:Boolean})],E.prototype,"hasFab",void 0),(0,o.__decorate)([(0,r.Cb)({attribute:!1})],E.prototype,"appendRow",void 0),(0,o.__decorate)([(0,r.Cb)({type:Boolean,attribute:"auto-height"})],E.prototype,"autoHeight",void 0),(0,o.__decorate)([(0,r.Cb)({type:String})],E.prototype,"id",void 0),(0,o.__decorate)([(0,r.Cb)({attribute:!1,type:String})],E.prototype,"noDataText",void 0),(0,o.__decorate)([(0,r.Cb)({attribute:!1,type:String})],E.prototype,"searchLabel",void 0),(0,o.__decorate)([(0,r.Cb)({type:Boolean,attribute:"no-label-float"})],E.prototype,"noLabelFloat",void 0),(0,o.__decorate)([(0,r.Cb)({type:String})],E.prototype,"filter",void 0),(0,o.__decorate)([(0,r.Cb)({attribute:!1})],E.prototype,"groupColumn",void 0),(0,o.__decorate)([(0,r.Cb)({attribute:!1})],E.prototype,"groupOrder",void 0),(0,o.__decorate)([(0,r.Cb)({attribute:!1})],E.prototype,"sortColumn",void 0),(0,o.__decorate)([(0,r.Cb)({attribute:!1})],E.prototype,"sortDirection",void 0),(0,o.__decorate)([(0,r.Cb)({attribute:!1})],E.prototype,"initialCollapsedGroups",void 0),(0,o.__decorate)([(0,r.Cb)({attribute:!1})],E.prototype,"hiddenColumns",void 0),(0,o.__decorate)([(0,r.Cb)({attribute:!1})],E.prototype,"columnOrder",void 0),(0,o.__decorate)([(0,r.SB)()],E.prototype,"_filterable",void 0),(0,o.__decorate)([(0,r.SB)()],E.prototype,"_filter",void 0),(0,o.__decorate)([(0,r.SB)()],E.prototype,"_filteredData",void 0),(0,o.__decorate)([(0,r.SB)()],E.prototype,"_headerHeight",void 0),(0,o.__decorate)([(0,r.IO)("slot[name='header']")],E.prototype,"_header",void 0),(0,o.__decorate)([(0,r.SB)()],E.prototype,"_collapsedGroups",void 0),(0,o.__decorate)([(0,r.SB)()],E.prototype,"_lastSelectedRowId",void 0),(0,o.__decorate)([(0,h.i)(".scroller")],E.prototype,"_savedScrollPos",void 0),(0,o.__decorate)([(0,r.hO)({passive:!0})],E.prototype,"_saveScrollPos",null),(0,o.__decorate)([(0,r.hO)({passive:!0})],E.prototype,"_scrollContent",null),E=(0,o.__decorate)([(0,r.Mo)("ha-data-table")],E)},51431:function(e,t,a){a(26847),a(27530);var o=a(73742),l=a(59048),i=a(7616),r=a(29740),d=(a(90380),a(10051)),s=a(91646),c=a(67419);let n;class h extends d.v2{connectedCallback(){super.connectedCallback(),this.addEventListener("close-menu",this._handleCloseMenu)}_handleCloseMenu(e){var t,a;e.detail.reason.kind===c.GB.KEYDOWN&&e.detail.reason.key===c.KC.ESCAPE||null===(t=(a=e.detail.initiator).clickAction)||void 0===t||t.call(a,e.detail.initiator)}}h.styles=[s.W,(0,l.iv)(n||(n=(e=>e)`
      :host {
        --md-sys-color-surface-container: var(--card-background-color);
      }
    `))],h=(0,o.__decorate)([(0,i.Mo)("ha-md-menu")],h);let _,u,p=e=>e;class m extends l.oi{get items(){return this._menu.items}focus(){var e;this._menu.open?this._menu.focus():null===(e=this._triggerButton)||void 0===e||e.focus()}render(){return(0,l.dy)(_||(_=p`
      <div @click=${0}>
        <slot name="trigger" @slotchange=${0}></slot>
      </div>
      <ha-md-menu
        .positioning=${0}
        .hasOverflow=${0}
        @opening=${0}
        @closing=${0}
      >
        <slot></slot>
      </ha-md-menu>
    `),this._handleClick,this._setTriggerAria,this.positioning,this.hasOverflow,this._handleOpening,this._handleClosing)}_handleOpening(){(0,r.B)(this,"opening",void 0,{composed:!1})}_handleClosing(){(0,r.B)(this,"closing",void 0,{composed:!1})}_handleClick(){this.disabled||(this._menu.anchorElement=this,this._menu.open?this._menu.close():this._menu.show())}get _triggerButton(){return this.querySelector('ha-icon-button[slot="trigger"], ha-button[slot="trigger"], ha-assist-chip[slot="trigger"]')}_setTriggerAria(){this._triggerButton&&(this._triggerButton.ariaHasPopup="menu")}constructor(...e){super(...e),this.disabled=!1,this.hasOverflow=!1}}m.styles=(0,l.iv)(u||(u=p`
    :host {
      display: inline-block;
      position: relative;
    }
    ::slotted([disabled]) {
      color: var(--disabled-text-color);
    }
  `)),(0,o.__decorate)([(0,i.Cb)({type:Boolean})],m.prototype,"disabled",void 0),(0,o.__decorate)([(0,i.Cb)()],m.prototype,"positioning",void 0),(0,o.__decorate)([(0,i.Cb)({type:Boolean,attribute:"has-overflow"})],m.prototype,"hasOverflow",void 0),(0,o.__decorate)([(0,i.IO)("ha-md-menu",!0)],m.prototype,"_menu",void 0),m=(0,o.__decorate)([(0,i.Mo)("ha-md-button-menu")],m)},1963:function(e,t,a){var o=a(73742),l=a(66923),i=a(93952),r=a(59048),d=a(7616);let s;class c extends l.i{}c.styles=[i.W,(0,r.iv)(s||(s=(e=>e)`
      :host {
        --md-divider-color: var(--divider-color);
      }
    `))],c=(0,o.__decorate)([(0,d.Mo)("ha-md-divider")],c)},72633:function(e,t,a){var o=a(73742),l=a(94598),i=a(15215),r=a(59048),d=a(7616);let s;class c extends l.${}c.styles=[i.W,(0,r.iv)(s||(s=(e=>e)`
      :host {
        --ha-icon-display: block;
        --md-sys-color-primary: var(--primary-text-color);
        --md-sys-color-on-primary: var(--primary-text-color);
        --md-sys-color-secondary: var(--secondary-text-color);
        --md-sys-color-surface: var(--card-background-color);
        --md-sys-color-on-surface: var(--primary-text-color);
        --md-sys-color-on-surface-variant: var(--secondary-text-color);
        --md-sys-color-secondary-container: rgba(
          var(--rgb-primary-color),
          0.15
        );
        --md-sys-color-on-secondary-container: var(--text-primary-color);
        --mdc-icon-size: 16px;

        --md-sys-color-on-primary-container: var(--primary-text-color);
        --md-sys-color-on-secondary-container: var(--primary-text-color);
        --md-menu-item-label-text-font: Roboto, sans-serif;
      }
      :host(.warning) {
        --md-menu-item-label-text-color: var(--error-color);
        --md-menu-item-leading-icon-color: var(--error-color);
      }
      ::slotted([slot="headline"]) {
        text-wrap: nowrap;
      }
    `))],(0,o.__decorate)([(0,d.Cb)({attribute:!1})],c.prototype,"clickAction",void 0),c=(0,o.__decorate)([(0,d.Mo)("ha-md-menu-item")],c)},40850:function(e,t,a){a(26847),a(81738),a(94814),a(1455),a(27530);var o=a(73742),l=a(59048),i=a(7616),r=(a(78645),a(40830),a(38573),a(29740));let d,s,c,n=e=>e;class h extends l.oi{focus(){var e;null===(e=this._input)||void 0===e||e.focus()}render(){return(0,l.dy)(d||(d=n`
      <ha-textfield
        .autofocus=${0}
        .label=${0}
        .value=${0}
        icon
        .iconTrailing=${0}
        @input=${0}
      >
        <slot name="prefix" slot="leadingIcon">
          <ha-svg-icon
            tabindex="-1"
            class="prefix"
            .path=${0}
          ></ha-svg-icon>
        </slot>
        <div class="trailing" slot="trailingIcon">
          ${0}
          <slot name="suffix"></slot>
        </div>
      </ha-textfield>
    `),this.autofocus,this.label||this.hass.localize("ui.common.search"),this.filter||"",this.filter||this.suffix,this._filterInputChanged,"M9.5,3A6.5,6.5 0 0,1 16,9.5C16,11.11 15.41,12.59 14.44,13.73L14.71,14H15.5L20.5,19L19,20.5L14,15.5V14.71L13.73,14.44C12.59,15.41 11.11,16 9.5,16A6.5,6.5 0 0,1 3,9.5A6.5,6.5 0 0,1 9.5,3M9.5,5C7,5 5,7 5,9.5C5,12 7,14 9.5,14C12,14 14,12 14,9.5C14,7 12,5 9.5,5Z",this.filter&&(0,l.dy)(s||(s=n`
            <ha-icon-button
              @click=${0}
              .label=${0}
              .path=${0}
              class="clear-button"
            ></ha-icon-button>
          `),this._clearSearch,this.hass.localize("ui.common.clear"),"M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z"))}async _filterChanged(e){(0,r.B)(this,"value-changed",{value:String(e)})}async _filterInputChanged(e){this._filterChanged(e.target.value)}async _clearSearch(){this._filterChanged("")}constructor(...e){super(...e),this.suffix=!1,this.autofocus=!1}}h.styles=(0,l.iv)(c||(c=n`
    :host {
      display: inline-flex;
    }
    ha-svg-icon,
    ha-icon-button {
      color: var(--primary-text-color);
    }
    ha-svg-icon {
      outline: none;
    }
    .clear-button {
      --mdc-icon-size: 20px;
    }
    ha-textfield {
      display: inherit;
    }
    .trailing {
      display: flex;
      align-items: center;
    }
  `)),(0,o.__decorate)([(0,i.Cb)({attribute:!1})],h.prototype,"hass",void 0),(0,o.__decorate)([(0,i.Cb)()],h.prototype,"filter",void 0),(0,o.__decorate)([(0,i.Cb)({type:Boolean})],h.prototype,"suffix",void 0),(0,o.__decorate)([(0,i.Cb)({type:Boolean})],h.prototype,"autofocus",void 0),(0,o.__decorate)([(0,i.Cb)({type:String})],h.prototype,"label",void 0),(0,o.__decorate)([(0,i.IO)("ha-textfield",!0)],h.prototype,"_input",void 0),h=(0,o.__decorate)([(0,i.Mo)("search-input")],h)},65682:function(e,t,a){a.d(t,{o:function(){return o}});a(26847),a(1455),a(27530);const o=async()=>{await a.e("9323").then(a.bind(a,23684))}}}]);
//# sourceMappingURL=3956.d1a31602e071a9be.js.map