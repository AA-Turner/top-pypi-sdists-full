export const __webpack_id__="1817";export const __webpack_ids__=["1817"];export const __webpack_modules__={92209:function(t,e,a){a.d(e,{x:()=>i});const i=(t,e)=>t&&t.config.components.includes(e)},25749:function(t,e,a){a.d(e,{SH:()=>s,u1:()=>n,xL:()=>d});var i=a(22786);const o=(0,i.A)(t=>new Intl.Collator(t,{numeric:!0})),l=(0,i.A)(t=>new Intl.Collator(t,{sensitivity:"accent",numeric:!0})),r=(t,e)=>t<e?-1:t>e?1:0,d=(t,e,a=void 0)=>Intl?.Collator?o(a).compare(t,e):r(t,e),s=(t,e,a=void 0)=>Intl?.Collator?l(a).compare(t,e):r(t.toLowerCase(),e.toLowerCase()),n=t=>(e,a)=>{const i=t.indexOf(e),o=t.indexOf(a);return i===o?0:-1===i?1:-1===o?-1:i-o}},40404:function(t,e,a){a.d(e,{s:()=>i});const i=(t,e,a=!1)=>{let i;const o=(...o)=>{const l=a&&!i;clearTimeout(i),i=window.setTimeout(()=>{i=void 0,t(...o)},e),l&&t(...o)};return o.cancel=()=>{clearTimeout(i)},o}},37445:function(t,e,a){var i=a(62826),o=a(34271),l=a(96196),r=a(77845),d=a(94333),s=a(32288),n=a(29485),c=a(22786),h=a(39501),p=a(92542),_=a(25749),b=a(40404);const u=(t,e)=>{const a={};for(const i of t){const t=e(i);t in a?a[t].push(i):a[t]=[i]}return a};var m=a(39396),f=a(84183),v=(a(70524),a(60961),a(17262),a(2209));let g;const x=()=>(g||(g=(0,v.LV)(new Worker(new URL(a.p+a.u("4346"),a.b)))),g);var w=a(99034);const y="zzzzz_undefined";class k extends l.WF{clearSelection(){this._checkedRows=[],this._lastSelectedRowId=null,this._checkedRowsChanged()}selectAll(){this._checkedRows=this._filteredData.filter(t=>!1!==t.selectable).map(t=>t[this.id]),this._lastSelectedRowId=null,this._checkedRowsChanged()}select(t,e){e&&(this._checkedRows=[]),t.forEach(t=>{const e=this._filteredData.find(e=>e[this.id]===t);!1===e?.selectable||this._checkedRows.includes(t)||this._checkedRows.push(t)}),this._lastSelectedRowId=null,this._checkedRowsChanged()}unselect(t){t.forEach(t=>{const e=this._checkedRows.indexOf(t);e>-1&&this._checkedRows.splice(e,1)}),this._lastSelectedRowId=null,this._checkedRowsChanged()}connectedCallback(){super.connectedCallback(),this._filteredData.length&&(this._filteredData=[...this._filteredData])}firstUpdated(){this.updateComplete.then(()=>this._calcTableHeight())}updated(){const t=this.renderRoot.querySelector(".mdc-data-table__header-row");t&&(t.scrollWidth>t.clientWidth?this.style.setProperty("--table-row-width",`${t.scrollWidth}px`):this.style.removeProperty("--table-row-width"))}willUpdate(t){if(super.willUpdate(t),this.hasUpdated||(0,f.i)(),t.has("columns")){if(this._filterable=Object.values(this.columns).some(t=>t.filterable),!this.sortColumn)for(const e in this.columns)if(this.columns[e].direction){this.sortDirection=this.columns[e].direction,this.sortColumn=e,this._lastSelectedRowId=null,(0,p.r)(this,"sorting-changed",{column:e,direction:this.sortDirection});break}const t=(0,o.A)(this.columns);Object.values(t).forEach(t=>{delete t.title,delete t.template,delete t.extraTemplate}),this._sortColumns=t}if(t.has("filter")&&(this._debounceSearch(this.filter),this._lastSelectedRowId=null),t.has("data")){if(this._checkedRows.length){const t=new Set(this.data.map(t=>String(t[this.id]))),e=this._checkedRows.filter(e=>t.has(e));e.length!==this._checkedRows.length&&(this._checkedRows=e,this._checkedRowsChanged())}this._checkableRowsCount=this.data.filter(t=>!1!==t.selectable).length}!this.hasUpdated&&this.initialCollapsedGroups?(this._collapsedGroups=this.initialCollapsedGroups,this._lastSelectedRowId=null,(0,p.r)(this,"collapsed-changed",{value:this._collapsedGroups})):t.has("groupColumn")&&(this._collapsedGroups=[],this._lastSelectedRowId=null,(0,p.r)(this,"collapsed-changed",{value:this._collapsedGroups})),(t.has("data")||t.has("columns")||t.has("_filter")||t.has("sortColumn")||t.has("sortDirection"))&&this._sortFilterData(),(t.has("_filter")||t.has("sortColumn")||t.has("sortDirection"))&&(this._lastSelectedRowId=null),(t.has("selectable")||t.has("hiddenColumns"))&&(this._filteredData=[...this._filteredData])}render(){const t=this.localizeFunc||this.hass.localize,e=this._sortedColumns(this.columns,this.columnOrder);return l.qy`
      <div class="mdc-data-table">
        <slot name="header" @slotchange=${this._calcTableHeight}>
          ${this._filterable?l.qy`
                <div class="table-header">
                  <search-input
                    .hass=${this.hass}
                    @value-changed=${this._handleSearchChange}
                    .label=${this.searchLabel}
                    .noLabelFloat=${this.noLabelFloat}
                  ></search-input>
                </div>
              `:""}
        </slot>
        <div
          class="mdc-data-table__table ${(0,d.H)({"auto-height":this.autoHeight})}"
          role="table"
          aria-rowcount=${this._filteredData.length+1}
          style=${(0,n.W)({height:this.autoHeight?53*(this._filteredData.length||1)+53+"px":`calc(100% - ${this._headerHeight}px)`})}
        >
          <div
            class="mdc-data-table__header-row"
            role="row"
            aria-rowindex="1"
            @scroll=${this._scrollContent}
          >
            <slot name="header-row">
              ${this.selectable?l.qy`
                    <div
                      class="mdc-data-table__header-cell mdc-data-table__header-cell--checkbox"
                      role="columnheader"
                    >
                      <ha-checkbox
                        class="mdc-data-table__row-checkbox"
                        @change=${this._handleHeaderRowCheckboxClick}
                        .indeterminate=${this._checkedRows.length&&this._checkedRows.length!==this._checkableRowsCount}
                        .checked=${this._checkedRows.length&&this._checkedRows.length===this._checkableRowsCount}
                      >
                      </ha-checkbox>
                    </div>
                  `:""}
              ${Object.entries(e).map(([t,e])=>{if(e.hidden||(this.columnOrder&&this.columnOrder.includes(t)?this.hiddenColumns?.includes(t)??e.defaultHidden:e.defaultHidden))return l.s6;const a=t===this.sortColumn,i={"mdc-data-table__header-cell--numeric":"numeric"===e.type,"mdc-data-table__header-cell--icon":"icon"===e.type,"mdc-data-table__header-cell--icon-button":"icon-button"===e.type,"mdc-data-table__header-cell--overflow-menu":"overflow-menu"===e.type,"mdc-data-table__header-cell--overflow":"overflow"===e.type,sortable:Boolean(e.sortable),"not-sorted":Boolean(e.sortable&&!a)};return l.qy`
                  <div
                    aria-label=${(0,s.J)(e.label)}
                    class="mdc-data-table__header-cell ${(0,d.H)(i)}"
                    style=${(0,n.W)({minWidth:e.minWidth,maxWidth:e.maxWidth,flex:e.flex||1})}
                    role="columnheader"
                    aria-sort=${(0,s.J)(a?"desc"===this.sortDirection?"descending":"ascending":void 0)}
                    @click=${this._handleHeaderClick}
                    .columnId=${t}
                    title=${(0,s.J)(e.title)}
                  >
                    ${e.sortable?l.qy`
                          <ha-svg-icon
                            .path=${a&&"desc"===this.sortDirection?"M11,4H13V16L18.5,10.5L19.92,11.92L12,19.84L4.08,11.92L5.5,10.5L11,16V4Z":"M13,20H11V8L5.5,13.5L4.08,12.08L12,4.16L19.92,12.08L18.5,13.5L13,8V20Z"}
                          ></ha-svg-icon>
                        `:""}
                    <span>${e.title}</span>
                  </div>
                `})}
            </slot>
          </div>
          ${this._filteredData.length?l.qy`
                <lit-virtualizer
                  scroller
                  class="mdc-data-table__content scroller ha-scrollbar"
                  @scroll=${this._saveScrollPos}
                  .items=${this._groupData(this._filteredData,t,this.appendRow,this.hasFab,this.groupColumn,this.groupOrder,this._collapsedGroups,this.sortColumn,this.sortDirection)}
                  .keyFunction=${this._keyFunction}
                  .renderItem=${(t,a)=>this._renderRow(e,this.narrow,t,a)}
                ></lit-virtualizer>
              `:l.qy`
                <div class="mdc-data-table__content">
                  <div class="mdc-data-table__row" role="row">
                    <div class="mdc-data-table__cell grows center" role="cell">
                      ${this.noDataText||t("ui.components.data-table.no-data")}
                    </div>
                  </div>
                </div>
              `}
        </div>
      </div>
    `}async _sortFilterData(){const t=(new Date).getTime(),e=t-this._lastUpdate,a=t-this._curRequest;this._curRequest=t;const i=!this._lastUpdate||e>500&&a<500;let o=this.data;if(this._filter&&(o=await this._memFilterData(this.data,this._sortColumns,this._filter.trim())),!i&&this._curRequest!==t)return;const l=this.sortColumn&&this._sortColumns[this.sortColumn]?((t,e,a,i,o)=>x().sortData(t,e,a,i,o))(o,this._sortColumns[this.sortColumn],this.sortDirection,this.sortColumn,this.hass.locale.language):o,[r]=await Promise.all([l,w.E]),d=(new Date).getTime()-t;d<100&&await new Promise(t=>{setTimeout(t,100-d)}),(i||this._curRequest===t)&&(this._lastUpdate=t,this._filteredData=r)}_handleHeaderClick(t){const e=t.currentTarget.columnId;this.columns[e].sortable&&(this.sortDirection&&this.sortColumn===e?"asc"===this.sortDirection?this.sortDirection="desc":this.sortDirection=null:this.sortDirection="asc",this.sortColumn=null===this.sortDirection?void 0:e,(0,p.r)(this,"sorting-changed",{column:e,direction:this.sortDirection}))}_handleHeaderRowCheckboxClick(t){t.target.checked?this.selectAll():(this._checkedRows=[],this._checkedRowsChanged()),this._lastSelectedRowId=null}_selectRange(t,e,a){const i=Math.min(e,a),o=Math.max(e,a),l=[];for(let r=i;r<=o;r++){const e=t[r];e&&!1!==e.selectable&&!this._checkedRows.includes(e[this.id])&&l.push(e[this.id])}return l}_setTitle(t){const e=t.currentTarget;e.scrollWidth>e.offsetWidth&&e.setAttribute("title",e.innerText)}_checkedRowsChanged(){this._filteredData.length&&(this._filteredData=[...this._filteredData]),(0,p.r)(this,"selection-changed",{value:this._checkedRows})}_handleSearchChange(t){this.filter||(this._lastSelectedRowId=null,this._debounceSearch(t.detail.value))}async _calcTableHeight(){this.autoHeight||(await this.updateComplete,this._headerHeight=this._header.clientHeight)}_saveScrollPos(t){this._savedScrollPos=t.target.scrollTop,this.renderRoot.querySelector(".mdc-data-table__header-row").scrollLeft=t.target.scrollLeft}_scrollContent(t){this.renderRoot.querySelector("lit-virtualizer").scrollLeft=t.target.scrollLeft}expandAllGroups(){this._collapsedGroups=[],this._lastSelectedRowId=null,(0,p.r)(this,"collapsed-changed",{value:this._collapsedGroups})}collapseAllGroups(){if(!this.groupColumn||!this.data.some(t=>t[this.groupColumn]))return;const t=u(this.data,t=>t[this.groupColumn]);t.undefined&&(t[y]=t.undefined,delete t.undefined),this._collapsedGroups=Object.keys(t),this._lastSelectedRowId=null,(0,p.r)(this,"collapsed-changed",{value:this._collapsedGroups})}static get styles(){return[m.dp,l.AH`
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
          border-radius: var(--ha-border-radius-sm);
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
      `]}constructor(...t){super(...t),this.narrow=!1,this.columns={},this.data=[],this.selectable=!1,this.clickable=!1,this.hasFab=!1,this.autoHeight=!1,this.id="id",this.noLabelFloat=!1,this.filter="",this.sortDirection=null,this._filterable=!1,this._filter="",this._filteredData=[],this._headerHeight=0,this._collapsedGroups=[],this._lastSelectedRowId=null,this._checkedRows=[],this._sortColumns={},this._curRequest=0,this._lastUpdate=0,this._debounceSearch=(0,b.s)(t=>{this._filter=t},100,!1),this._sortedColumns=(0,c.A)((t,e)=>e&&e.length?Object.keys(t).sort((t,a)=>{const i=e.indexOf(t),o=e.indexOf(a);if(i!==o){if(-1===i)return 1;if(-1===o)return-1}return i-o}).reduce((e,a)=>(e[a]=t[a],e),{}):t),this._keyFunction=t=>t?.[this.id]||t,this._renderRow=(t,e,a,i)=>a?a.append?l.qy`<div class="mdc-data-table__row">${a.content}</div>`:a.empty?l.qy`<div class="mdc-data-table__row empty-row"></div>`:l.qy`
      <div
        aria-rowindex=${i+2}
        role="row"
        .rowId=${a[this.id]}
        @click=${this._handleRowClick}
        class="mdc-data-table__row ${(0,d.H)({"mdc-data-table__row--selected":this._checkedRows.includes(String(a[this.id])),clickable:this.clickable})}"
        aria-selected=${(0,s.J)(!!this._checkedRows.includes(String(a[this.id]))||void 0)}
        .selectable=${!1!==a.selectable}
      >
        ${this.selectable?l.qy`
              <div
                class="mdc-data-table__cell mdc-data-table__cell--checkbox"
                role="cell"
              >
                <ha-checkbox
                  class="mdc-data-table__row-checkbox"
                  @click=${this._handleRowCheckboxClicked}
                  .rowId=${a[this.id]}
                  .disabled=${!1===a.selectable}
                  .checked=${this._checkedRows.includes(String(a[this.id]))}
                >
                </ha-checkbox>
              </div>
            `:""}
        ${Object.entries(t).map(([i,o])=>e&&!o.main&&!o.showNarrow||o.hidden||(this.columnOrder&&this.columnOrder.includes(i)?this.hiddenColumns?.includes(i)??o.defaultHidden:o.defaultHidden)?l.s6:l.qy`
            <div
              @mouseover=${this._setTitle}
              @focus=${this._setTitle}
              role=${o.main?"rowheader":"cell"}
              class="mdc-data-table__cell ${(0,d.H)({"mdc-data-table__cell--flex":"flex"===o.type,"mdc-data-table__cell--numeric":"numeric"===o.type,"mdc-data-table__cell--icon":"icon"===o.type,"mdc-data-table__cell--icon-button":"icon-button"===o.type,"mdc-data-table__cell--overflow-menu":"overflow-menu"===o.type,"mdc-data-table__cell--overflow":"overflow"===o.type,forceLTR:Boolean(o.forceLTR)})}"
              style=${(0,n.W)({minWidth:o.minWidth,maxWidth:o.maxWidth,flex:o.flex||1})}
            >
              ${o.template?o.template(a):e&&o.main?l.qy`<div class="primary">${a[i]}</div>
                      <div class="secondary">
                        ${Object.entries(t).filter(([t,e])=>!(e.hidden||e.main||e.showNarrow||(this.columnOrder&&this.columnOrder.includes(t)?this.hiddenColumns?.includes(t)??e.defaultHidden:e.defaultHidden))).map(([t,e],i)=>l.qy`${0!==i?" · ":l.s6}${e.template?e.template(a):a[t]}`)}
                      </div>
                      ${o.extraTemplate?o.extraTemplate(a):l.s6}`:l.qy`${a[i]}${o.extraTemplate?o.extraTemplate(a):l.s6}`}
            </div>
          `)}
      </div>
    `:l.s6,this._groupData=(0,c.A)((t,e,a,i,o,r,d,s,n)=>{if(a||i||o){let c=[...t];if(o){const t=s===o,a=u(c,t=>t[o]);a.undefined&&(a[y]=a.undefined,delete a.undefined);const i=Object.keys(a).sort((e,a)=>{if(!r&&t){const t=(0,_.xL)(e,a,this.hass.locale.language);return"asc"===n?t:-1*t}const i=r?.indexOf(e)??-1,o=r?.indexOf(a)??-1;return i!==o?-1===i?1:-1===o?-1:i-o:(0,_.xL)(["","-","—"].includes(e)?"zzz":e,["","-","—"].includes(a)?"zzz":a,this.hass.locale.language)}).reduce((t,e)=>{const i=[e,a[e]];return t.push(i),t},[]),h=[];i.forEach(([t,a])=>{const i=d.includes(t);h.push({append:!0,selectable:!1,content:l.qy`<div
                class="mdc-data-table__cell group-header"
                role="cell"
                .group=${t}
                @click=${this._collapseGroup}
              >
                <ha-icon-button
                  .path=${"M7.41,15.41L12,10.83L16.59,15.41L18,14L12,8L6,14L7.41,15.41Z"}
                  .label=${this.hass.localize("ui.components.data-table."+(i?"expand":"collapse"))}
                  class=${i?"collapsed":""}
                >
                </ha-icon-button>
                ${t===y?e("ui.components.data-table.ungrouped"):t||""}
              </div>`}),d.includes(t)||h.push(...a)}),c=h}return a&&c.push({append:!0,selectable:!1,content:a}),i&&c.push({empty:!0}),c}return t}),this._memFilterData=(0,c.A)((t,e,a)=>((t,e,a)=>x().filterData(t,e,a))(t,e,a)),this._handleRowCheckboxClicked=t=>{const e=t.currentTarget,a=e.rowId,i=this._groupData(this._filteredData,this.localizeFunc||this.hass.localize,this.appendRow,this.hasFab,this.groupColumn,this.groupOrder,this._collapsedGroups,this.sortColumn,this.sortDirection);if(!1===i.find(t=>t[this.id]===a)?.selectable)return;const o=i.findIndex(t=>t[this.id]===a);if(t instanceof MouseEvent&&t.shiftKey&&null!==this._lastSelectedRowId){const t=i.findIndex(t=>t[this.id]===this._lastSelectedRowId);t>-1&&o>-1&&(this._checkedRows=[...this._checkedRows,...this._selectRange(i,t,o)])}else e.checked?this._checkedRows=this._checkedRows.filter(t=>t!==a):this._checkedRows.includes(a)||(this._checkedRows=[...this._checkedRows,a]);o>-1&&(this._lastSelectedRowId=a),this._checkedRowsChanged()},this._handleRowClick=t=>{if(t.composedPath().find(t=>["ha-checkbox","ha-button","ha-button","ha-icon-button","ha-assist-chip"].includes(t.localName)))return;const e=t.currentTarget.rowId;(0,p.r)(this,"row-click",{id:e},{bubbles:!1})},this._collapseGroup=t=>{const e=t.currentTarget.group;this._collapsedGroups.includes(e)?this._collapsedGroups=this._collapsedGroups.filter(t=>t!==e):this._collapsedGroups=[...this._collapsedGroups,e],this._lastSelectedRowId=null,(0,p.r)(this,"collapsed-changed",{value:this._collapsedGroups})}}}(0,i.__decorate)([(0,r.MZ)({attribute:!1})],k.prototype,"hass",void 0),(0,i.__decorate)([(0,r.MZ)({attribute:!1})],k.prototype,"localizeFunc",void 0),(0,i.__decorate)([(0,r.MZ)({type:Boolean})],k.prototype,"narrow",void 0),(0,i.__decorate)([(0,r.MZ)({type:Object})],k.prototype,"columns",void 0),(0,i.__decorate)([(0,r.MZ)({type:Array})],k.prototype,"data",void 0),(0,i.__decorate)([(0,r.MZ)({type:Boolean})],k.prototype,"selectable",void 0),(0,i.__decorate)([(0,r.MZ)({type:Boolean})],k.prototype,"clickable",void 0),(0,i.__decorate)([(0,r.MZ)({attribute:"has-fab",type:Boolean})],k.prototype,"hasFab",void 0),(0,i.__decorate)([(0,r.MZ)({attribute:!1})],k.prototype,"appendRow",void 0),(0,i.__decorate)([(0,r.MZ)({type:Boolean,attribute:"auto-height"})],k.prototype,"autoHeight",void 0),(0,i.__decorate)([(0,r.MZ)({type:String})],k.prototype,"id",void 0),(0,i.__decorate)([(0,r.MZ)({attribute:!1,type:String})],k.prototype,"noDataText",void 0),(0,i.__decorate)([(0,r.MZ)({attribute:!1,type:String})],k.prototype,"searchLabel",void 0),(0,i.__decorate)([(0,r.MZ)({type:Boolean,attribute:"no-label-float"})],k.prototype,"noLabelFloat",void 0),(0,i.__decorate)([(0,r.MZ)({type:String})],k.prototype,"filter",void 0),(0,i.__decorate)([(0,r.MZ)({attribute:!1})],k.prototype,"groupColumn",void 0),(0,i.__decorate)([(0,r.MZ)({attribute:!1})],k.prototype,"groupOrder",void 0),(0,i.__decorate)([(0,r.MZ)({attribute:!1})],k.prototype,"sortColumn",void 0),(0,i.__decorate)([(0,r.MZ)({attribute:!1})],k.prototype,"sortDirection",void 0),(0,i.__decorate)([(0,r.MZ)({attribute:!1})],k.prototype,"initialCollapsedGroups",void 0),(0,i.__decorate)([(0,r.MZ)({attribute:!1})],k.prototype,"hiddenColumns",void 0),(0,i.__decorate)([(0,r.MZ)({attribute:!1})],k.prototype,"columnOrder",void 0),(0,i.__decorate)([(0,r.wk)()],k.prototype,"_filterable",void 0),(0,i.__decorate)([(0,r.wk)()],k.prototype,"_filter",void 0),(0,i.__decorate)([(0,r.wk)()],k.prototype,"_filteredData",void 0),(0,i.__decorate)([(0,r.wk)()],k.prototype,"_headerHeight",void 0),(0,i.__decorate)([(0,r.P)("slot[name='header']")],k.prototype,"_header",void 0),(0,i.__decorate)([(0,r.wk)()],k.prototype,"_collapsedGroups",void 0),(0,i.__decorate)([(0,r.wk)()],k.prototype,"_lastSelectedRowId",void 0),(0,i.__decorate)([(0,h.a)(".scroller")],k.prototype,"_savedScrollPos",void 0),(0,i.__decorate)([(0,r.Ls)({passive:!0})],k.prototype,"_saveScrollPos",null),(0,i.__decorate)([(0,r.Ls)({passive:!0})],k.prototype,"_scrollContent",null),k=(0,i.__decorate)([(0,r.EM)("ha-data-table")],k)},70524:function(t,e,a){var i=a(62826),o=a(69162),l=a(47191),r=a(96196),d=a(77845);class s extends o.L{}s.styles=[l.R,r.AH`
      :host {
        --mdc-theme-secondary: var(--primary-color);
      }
    `],s=(0,i.__decorate)([(0,d.EM)("ha-checkbox")],s)},78740:function(t,e,a){a.d(e,{h:()=>n});var i=a(62826),o=a(68846),l=a(92347),r=a(96196),d=a(77845),s=a(76679);class n extends o.J{updated(t){super.updated(t),(t.has("invalid")||t.has("errorMessage"))&&(this.setCustomValidity(this.invalid?this.errorMessage||this.validationMessage||"Invalid":""),(this.invalid||this.validateOnInitialRender||t.has("invalid")&&void 0!==t.get("invalid"))&&this.reportValidity()),t.has("autocomplete")&&(this.autocomplete?this.formElement.setAttribute("autocomplete",this.autocomplete):this.formElement.removeAttribute("autocomplete")),t.has("autocorrect")&&(!1===this.autocorrect?this.formElement.setAttribute("autocorrect","off"):this.formElement.removeAttribute("autocorrect")),t.has("inputSpellcheck")&&(this.inputSpellcheck?this.formElement.setAttribute("spellcheck",this.inputSpellcheck):this.formElement.removeAttribute("spellcheck"))}renderIcon(t,e=!1){const a=e?"trailing":"leading";return r.qy`
      <span
        class="mdc-text-field__icon mdc-text-field__icon--${a}"
        tabindex=${e?1:-1}
      >
        <slot name="${a}Icon"></slot>
      </span>
    `}constructor(...t){super(...t),this.icon=!1,this.iconTrailing=!1,this.autocorrect=!0}}n.styles=[l.R,r.AH`
      .mdc-text-field__input {
        width: var(--ha-textfield-input-width, 100%);
      }
      .mdc-text-field:not(.mdc-text-field--with-leading-icon) {
        padding: var(--text-field-padding, 0px 16px);
      }
      .mdc-text-field__affix--suffix {
        padding-left: var(--text-field-suffix-padding-left, 12px);
        padding-right: var(--text-field-suffix-padding-right, 0px);
        padding-inline-start: var(--text-field-suffix-padding-left, 12px);
        padding-inline-end: var(--text-field-suffix-padding-right, 0px);
        direction: ltr;
      }
      .mdc-text-field--with-leading-icon {
        padding-inline-start: var(--text-field-suffix-padding-left, 0px);
        padding-inline-end: var(--text-field-suffix-padding-right, 16px);
        direction: var(--direction);
      }

      .mdc-text-field--with-leading-icon.mdc-text-field--with-trailing-icon {
        padding-left: var(--text-field-suffix-padding-left, 0px);
        padding-right: var(--text-field-suffix-padding-right, 0px);
        padding-inline-start: var(--text-field-suffix-padding-left, 0px);
        padding-inline-end: var(--text-field-suffix-padding-right, 0px);
      }
      .mdc-text-field:not(.mdc-text-field--disabled)
        .mdc-text-field__affix--suffix {
        color: var(--secondary-text-color);
      }

      .mdc-text-field:not(.mdc-text-field--disabled) .mdc-text-field__icon {
        color: var(--secondary-text-color);
      }

      .mdc-text-field__icon--leading {
        margin-inline-start: 16px;
        margin-inline-end: 8px;
        direction: var(--direction);
      }

      .mdc-text-field__icon--trailing {
        padding: var(--textfield-icon-trailing-padding, 12px);
      }

      .mdc-floating-label:not(.mdc-floating-label--float-above) {
        max-width: calc(100% - 16px);
      }

      .mdc-floating-label--float-above {
        max-width: calc((100% - 16px) / 0.75);
        transition: none;
      }

      input {
        text-align: var(--text-field-text-align, start);
      }

      input[type="color"] {
        height: 20px;
      }

      /* Edge, hide reveal password icon */
      ::-ms-reveal {
        display: none;
      }

      /* Chrome, Safari, Edge, Opera */
      :host([no-spinner]) input::-webkit-outer-spin-button,
      :host([no-spinner]) input::-webkit-inner-spin-button {
        -webkit-appearance: none;
        margin: 0;
      }

      input[type="color"]::-webkit-color-swatch-wrapper {
        padding: 0;
      }

      /* Firefox */
      :host([no-spinner]) input[type="number"] {
        -moz-appearance: textfield;
      }

      .mdc-text-field__ripple {
        overflow: hidden;
      }

      .mdc-text-field {
        overflow: var(--text-field-overflow);
      }

      .mdc-floating-label {
        padding-inline-end: 16px;
        padding-inline-start: initial;
        inset-inline-start: 16px !important;
        inset-inline-end: initial !important;
        transform-origin: var(--float-start);
        direction: var(--direction);
        text-align: var(--float-start);
        box-sizing: border-box;
        text-overflow: ellipsis;
      }

      .mdc-text-field--with-leading-icon.mdc-text-field--filled
        .mdc-floating-label {
        max-width: calc(
          100% - 48px - var(--text-field-suffix-padding-left, 0px)
        );
        inset-inline-start: calc(
          48px + var(--text-field-suffix-padding-left, 0px)
        ) !important;
        inset-inline-end: initial !important;
        direction: var(--direction);
      }

      .mdc-text-field__input[type="number"] {
        direction: var(--direction);
      }
      .mdc-text-field__affix--prefix {
        padding-right: var(--text-field-prefix-padding-right, 2px);
        padding-inline-end: var(--text-field-prefix-padding-right, 2px);
        padding-inline-start: initial;
      }

      .mdc-text-field:not(.mdc-text-field--disabled)
        .mdc-text-field__affix--prefix {
        color: var(--mdc-text-field-label-ink-color);
      }
      #helper-text ha-markdown {
        display: inline-block;
      }
    `,"rtl"===s.G.document.dir?r.AH`
          .mdc-text-field--with-leading-icon,
          .mdc-text-field__icon--leading,
          .mdc-floating-label,
          .mdc-text-field--with-leading-icon.mdc-text-field--filled
            .mdc-floating-label,
          .mdc-text-field__input[type="number"] {
            direction: rtl;
            --direction: rtl;
          }
        `:r.AH``],(0,i.__decorate)([(0,d.MZ)({type:Boolean})],n.prototype,"invalid",void 0),(0,i.__decorate)([(0,d.MZ)({attribute:"error-message"})],n.prototype,"errorMessage",void 0),(0,i.__decorate)([(0,d.MZ)({type:Boolean})],n.prototype,"icon",void 0),(0,i.__decorate)([(0,d.MZ)({type:Boolean})],n.prototype,"iconTrailing",void 0),(0,i.__decorate)([(0,d.MZ)()],n.prototype,"autocomplete",void 0),(0,i.__decorate)([(0,d.MZ)({type:Boolean})],n.prototype,"autocorrect",void 0),(0,i.__decorate)([(0,d.MZ)({attribute:"input-spellcheck"})],n.prototype,"inputSpellcheck",void 0),(0,i.__decorate)([(0,d.P)("input")],n.prototype,"formElement",void 0),n=(0,i.__decorate)([(0,d.EM)("ha-textfield")],n)},17262:function(t,e,a){var i=a(62826),o=a(96196),l=a(77845),r=(a(60733),a(60961),a(78740),a(92542));class d extends o.WF{focus(){this._input?.focus()}render(){return o.qy`
      <ha-textfield
        .autofocus=${this.autofocus}
        autocomplete="off"
        .label=${this.label||this.hass.localize("ui.common.search")}
        .value=${this.filter||""}
        icon
        .iconTrailing=${this.filter||this.suffix}
        @input=${this._filterInputChanged}
      >
        <slot name="prefix" slot="leadingIcon">
          <ha-svg-icon
            tabindex="-1"
            class="prefix"
            .path=${"M9.5,3A6.5,6.5 0 0,1 16,9.5C16,11.11 15.41,12.59 14.44,13.73L14.71,14H15.5L20.5,19L19,20.5L14,15.5V14.71L13.73,14.44C12.59,15.41 11.11,16 9.5,16A6.5,6.5 0 0,1 3,9.5A6.5,6.5 0 0,1 9.5,3M9.5,5C7,5 5,7 5,9.5C5,12 7,14 9.5,14C12,14 14,12 14,9.5C14,7 12,5 9.5,5Z"}
          ></ha-svg-icon>
        </slot>
        <div class="trailing" slot="trailingIcon">
          ${this.filter&&o.qy`
            <ha-icon-button
              @click=${this._clearSearch}
              .label=${this.hass.localize("ui.common.clear")}
              .path=${"M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z"}
              class="clear-button"
            ></ha-icon-button>
          `}
          <slot name="suffix"></slot>
        </div>
      </ha-textfield>
    `}async _filterChanged(t){(0,r.r)(this,"value-changed",{value:String(t)})}async _filterInputChanged(t){this._filterChanged(t.target.value)}async _clearSearch(){this._filterChanged("")}constructor(...t){super(...t),this.suffix=!1,this.autofocus=!1}}d.styles=o.AH`
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
  `,(0,i.__decorate)([(0,l.MZ)({attribute:!1})],d.prototype,"hass",void 0),(0,i.__decorate)([(0,l.MZ)()],d.prototype,"filter",void 0),(0,i.__decorate)([(0,l.MZ)({type:Boolean})],d.prototype,"suffix",void 0),(0,i.__decorate)([(0,l.MZ)({type:Boolean})],d.prototype,"autofocus",void 0),(0,i.__decorate)([(0,l.MZ)({type:String})],d.prototype,"label",void 0),(0,i.__decorate)([(0,l.P)("ha-textfield",!0)],d.prototype,"_input",void 0),d=(0,i.__decorate)([(0,l.EM)("search-input")],d)},84884:function(t,e,a){var i=a(62826),o=a(96196),l=a(77845),r=a(94333),d=a(22786),s=a(55376),n=a(92209);const c=(t,e)=>!e.component||(0,s.e)(e.component).some(e=>(0,n.x)(t,e)),h=(t,e)=>!e.not_component||!(0,s.e)(e.not_component).some(e=>(0,n.x)(t,e)),p=t=>t.core,_=(t,e)=>(t=>t.advancedOnly)(e)&&!(t=>t.userData?.showAdvanced)(t);var b=a(5871),u=a(39501),m=(a(371),a(45397),a(60961),a(32288));a(95591);class f extends o.WF{render(){return o.qy`
      <div
        tabindex="0"
        role="tab"
        aria-selected=${this.active}
        aria-label=${(0,m.J)(this.name)}
        @keydown=${this._handleKeyDown}
      >
        ${this.narrow?o.qy`<slot name="icon"></slot>`:""}
        <span class="name">${this.name}</span>
        <ha-ripple></ha-ripple>
      </div>
    `}_handleKeyDown(t){"Enter"===t.key&&t.target.click()}constructor(...t){super(...t),this.active=!1,this.narrow=!1}}f.styles=o.AH`
    div {
      padding: 0 32px;
      display: flex;
      flex-direction: column;
      text-align: center;
      box-sizing: border-box;
      align-items: center;
      justify-content: center;
      width: 100%;
      height: var(--header-height);
      cursor: pointer;
      position: relative;
      outline: none;
    }

    .name {
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      max-width: 100%;
    }

    :host([active]) {
      color: var(--primary-color);
    }

    :host(:not([narrow])[active]) div {
      border-bottom: 2px solid var(--primary-color);
    }

    :host([narrow]) {
      min-width: 0;
      display: flex;
      justify-content: center;
      overflow: hidden;
    }

    :host([narrow]) div {
      padding: 0 4px;
    }

    div:focus-visible:before {
      position: absolute;
      display: block;
      content: "";
      inset: 0;
      background-color: var(--secondary-text-color);
      opacity: 0.08;
    }
  `,(0,i.__decorate)([(0,l.MZ)({type:Boolean,reflect:!0})],f.prototype,"active",void 0),(0,i.__decorate)([(0,l.MZ)({type:Boolean,reflect:!0})],f.prototype,"narrow",void 0),(0,i.__decorate)([(0,l.MZ)()],f.prototype,"name",void 0),f=(0,i.__decorate)([(0,l.EM)("ha-tab")],f);var v=a(39396);class g extends o.WF{willUpdate(t){t.has("route")&&(this._activeTab=this.tabs.find(t=>`${this.route.prefix}${this.route.path}`.includes(t.path))),super.willUpdate(t)}render(){const t=this._getTabs(this.tabs,this._activeTab,this.hass.config.components,this.hass.language,this.hass.userData,this.narrow,this.localizeFunc||this.hass.localize),e=t.length>1;return o.qy`
      <div class="toolbar">
        <slot name="toolbar">
          <div class="toolbar-content">
            ${this.mainPage||!this.backPath&&history.state?.root?o.qy`
                  <ha-menu-button
                    .hassio=${this.supervisor}
                    .hass=${this.hass}
                    .narrow=${this.narrow}
                  ></ha-menu-button>
                `:this.backPath?o.qy`
                    <a href=${this.backPath}>
                      <ha-icon-button-arrow-prev
                        .hass=${this.hass}
                      ></ha-icon-button-arrow-prev>
                    </a>
                  `:o.qy`
                    <ha-icon-button-arrow-prev
                      .hass=${this.hass}
                      @click=${this._backTapped}
                    ></ha-icon-button-arrow-prev>
                  `}
            ${this.narrow||!e?o.qy`<div class="main-title">
                  <slot name="header">${e?"":t[0]}</slot>
                </div>`:""}
            ${e&&!this.narrow?o.qy`<div id="tabbar">${t}</div>`:""}
            <div id="toolbar-icon">
              <slot name="toolbar-icon"></slot>
            </div>
          </div>
        </slot>
        ${e&&this.narrow?o.qy`<div id="tabbar" class="bottom-bar">${t}</div>`:""}
      </div>
      <div
        class=${(0,r.H)({container:!0,tabs:e&&this.narrow})}
      >
        ${this.pane?o.qy`<div class="pane">
              <div class="shadow-container"></div>
              <div class="ha-scrollbar">
                <slot name="pane"></slot>
              </div>
            </div>`:o.s6}
        <div
          class="content ha-scrollbar ${(0,r.H)({tabs:e})}"
          @scroll=${this._saveScrollPos}
        >
          <slot></slot>
          ${this.hasFab?o.qy`<div class="fab-bottom-space"></div>`:o.s6}
        </div>
      </div>
      <div id="fab" class=${(0,r.H)({tabs:e})}>
        <slot name="fab"></slot>
      </div>
    `}_saveScrollPos(t){this._savedScrollPos=t.target.scrollTop}_backTapped(){this.backCallback?this.backCallback():(0,b.O)()}static get styles(){return[v.dp,o.AH`
        :host {
          display: block;
          height: 100%;
          background-color: var(--primary-background-color);
        }

        :host([narrow]) {
          width: 100%;
          position: fixed;
        }

        .container {
          display: flex;
          height: calc(
            100% - var(--header-height, 0px) - var(--safe-area-inset-top, 0px)
          );
        }

        ha-menu-button {
          margin-right: 24px;
          margin-inline-end: 24px;
          margin-inline-start: initial;
        }

        .toolbar {
          font-size: var(--ha-font-size-xl);
          height: calc(
            var(--header-height, 0px) + var(--safe-area-inset-top, 0px)
          );
          padding-top: var(--safe-area-inset-top);
          padding-right: var(--safe-area-inset-right);
          background-color: var(--sidebar-background-color);
          font-weight: var(--ha-font-weight-normal);
          border-bottom: 1px solid var(--divider-color);
          box-sizing: border-box;
        }
        :host([narrow]) .toolbar {
          padding-left: var(--safe-area-inset-left);
        }
        .toolbar-content {
          padding: 8px 12px;
          display: flex;
          align-items: center;
          height: 100%;
          box-sizing: border-box;
        }
        :host([narrow]) .toolbar-content {
          padding: 4px;
        }
        .toolbar a {
          color: var(--sidebar-text-color);
          text-decoration: none;
        }
        .bottom-bar a {
          width: 25%;
        }

        #tabbar {
          display: flex;
          font-size: var(--ha-font-size-m);
          overflow: hidden;
        }

        #tabbar > a {
          overflow: hidden;
          max-width: 45%;
        }

        #tabbar.bottom-bar {
          position: absolute;
          bottom: 0;
          left: 0;
          padding: 0 16px;
          box-sizing: border-box;
          background-color: var(--sidebar-background-color);
          border-top: 1px solid var(--divider-color);
          justify-content: space-around;
          z-index: 2;
          font-size: var(--ha-font-size-s);
          width: 100%;
          padding-bottom: var(--safe-area-inset-bottom);
        }

        #tabbar:not(.bottom-bar) {
          flex: 1;
          justify-content: center;
        }

        :host(:not([narrow])) #toolbar-icon {
          min-width: 40px;
        }

        ha-menu-button,
        ha-icon-button-arrow-prev,
        ::slotted([slot="toolbar-icon"]) {
          display: flex;
          flex-shrink: 0;
          pointer-events: auto;
          color: var(--sidebar-icon-color);
        }

        .main-title {
          flex: 1;
          max-height: var(--header-height);
          line-height: var(--ha-line-height-normal);
          color: var(--sidebar-text-color);
          margin: var(--main-title-margin, var(--margin-title));
        }

        .content {
          position: relative;
          width: 100%;
          margin-right: var(--safe-area-inset-right);
          margin-inline-end: var(--safe-area-inset-right);
          margin-bottom: var(--safe-area-inset-bottom);
          overflow: auto;
          -webkit-overflow-scrolling: touch;
        }
        :host([narrow]) .content {
          margin-left: var(--safe-area-inset-left);
          margin-inline-start: var(--safe-area-inset-left);
        }
        :host([narrow]) .content.tabs {
          /* Bottom bar reuses header height */
          margin-bottom: calc(
            var(--header-height, 0px) + var(--safe-area-inset-bottom, 0px)
          );
        }

        .content .fab-bottom-space {
          height: calc(64px + var(--safe-area-inset-bottom, 0px));
        }

        :host([narrow]) .content.tabs .fab-bottom-space {
          height: calc(80px + var(--safe-area-inset-bottom, 0px));
        }

        #fab {
          position: fixed;
          right: calc(16px + var(--safe-area-inset-right, 0px));
          inset-inline-end: calc(16px + var(--safe-area-inset-right));
          inset-inline-start: initial;
          bottom: calc(16px + var(--safe-area-inset-bottom, 0px));
          z-index: 1;
          display: flex;
          flex-wrap: wrap;
          justify-content: flex-end;
          gap: var(--ha-space-2);
        }
        :host([narrow]) #fab.tabs {
          bottom: calc(84px + var(--safe-area-inset-bottom, 0px));
        }
        #fab[is-wide] {
          bottom: 24px;
          right: 24px;
          inset-inline-end: 24px;
          inset-inline-start: initial;
        }

        .pane {
          border-right: 1px solid var(--divider-color);
          border-inline-end: 1px solid var(--divider-color);
          border-inline-start: initial;
          box-sizing: border-box;
          display: flex;
          flex: 0 0 var(--sidepane-width, 250px);
          width: var(--sidepane-width, 250px);
          flex-direction: column;
          position: relative;
        }
        .pane .ha-scrollbar {
          flex: 1;
        }
      `]}constructor(...t){super(...t),this.supervisor=!1,this.mainPage=!1,this.narrow=!1,this.isWide=!1,this.pane=!1,this.hasFab=!1,this._getTabs=(0,d.A)((t,e,a,i,l,r,d)=>{const s=t.filter(t=>((t,e)=>(p(e)||c(t,e))&&!_(t,e)&&h(t,e))(this.hass,t));if(s.length<2){if(1===s.length){const t=s[0];return[t.translationKey?d(t.translationKey):t.name]}return[""]}return s.map(t=>o.qy`
          <a href=${t.path}>
            <ha-tab
              .hass=${this.hass}
              .active=${t.path===e?.path}
              .narrow=${this.narrow}
              .name=${t.translationKey?d(t.translationKey):t.name}
            >
              ${t.iconPath?o.qy`<ha-svg-icon
                    slot="icon"
                    .path=${t.iconPath}
                  ></ha-svg-icon>`:""}
            </ha-tab>
          </a>
        `)})}}(0,i.__decorate)([(0,l.MZ)({attribute:!1})],g.prototype,"hass",void 0),(0,i.__decorate)([(0,l.MZ)({type:Boolean})],g.prototype,"supervisor",void 0),(0,i.__decorate)([(0,l.MZ)({attribute:!1})],g.prototype,"localizeFunc",void 0),(0,i.__decorate)([(0,l.MZ)({type:String,attribute:"back-path"})],g.prototype,"backPath",void 0),(0,i.__decorate)([(0,l.MZ)({attribute:!1})],g.prototype,"backCallback",void 0),(0,i.__decorate)([(0,l.MZ)({type:Boolean,attribute:"main-page"})],g.prototype,"mainPage",void 0),(0,i.__decorate)([(0,l.MZ)({attribute:!1})],g.prototype,"route",void 0),(0,i.__decorate)([(0,l.MZ)({attribute:!1})],g.prototype,"tabs",void 0),(0,i.__decorate)([(0,l.MZ)({type:Boolean,reflect:!0})],g.prototype,"narrow",void 0),(0,i.__decorate)([(0,l.MZ)({type:Boolean,reflect:!0,attribute:"is-wide"})],g.prototype,"isWide",void 0),(0,i.__decorate)([(0,l.MZ)({type:Boolean})],g.prototype,"pane",void 0),(0,i.__decorate)([(0,l.MZ)({type:Boolean,attribute:"has-fab"})],g.prototype,"hasFab",void 0),(0,i.__decorate)([(0,l.wk)()],g.prototype,"_activeTab",void 0),(0,i.__decorate)([(0,u.a)(".content")],g.prototype,"_savedScrollPos",void 0),(0,i.__decorate)([(0,l.Ls)({passive:!0})],g.prototype,"_saveScrollPos",null),g=(0,i.__decorate)([(0,l.EM)("hass-tabs-subpage")],g)},84183:function(t,e,a){a.d(e,{i:()=>i});const i=async()=>{await a.e("2564").then(a.bind(a,42735))}}};
//# sourceMappingURL=1817.dd37dc1ee5832b47.js.map