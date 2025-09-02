export const __webpack_ids__=["4379"];export const __webpack_modules__={13539:function(e,t,a){a.d(t,{Bt:()=>r});var o=a(3574),i=a(1066);const s=["sunday","monday","tuesday","wednesday","thursday","friday","saturday"],r=e=>e.first_weekday===i.FS.language?"weekInfo"in Intl.Locale.prototype?new Intl.Locale(e.language).weekInfo.firstDay%7:(0,o.L)(e.language)%7:s.includes(e.first_weekday)?s.indexOf(e.first_weekday):1},9131:function(e,t,a){a.a(e,(async function(e,o){try{a.d(t,{Vu:()=>h,Zs:()=>m,mr:()=>d,xO:()=>_});var i=a(57900),s=a(28105),r=a(36641),n=a(13819),l=e([i,r]);[i,r]=l.then?(await l)():l;const d=(e,t,a)=>c(t,a.time_zone).format(e),c=(0,s.Z)(((e,t)=>new Intl.DateTimeFormat(e.language,{hour:"numeric",minute:"2-digit",hourCycle:(0,n.y)(e)?"h12":"h23",timeZone:(0,r.f)(e.time_zone,t)}))),h=(e,t,a)=>u(t,a.time_zone).format(e),u=(0,s.Z)(((e,t)=>new Intl.DateTimeFormat(e.language,{hour:(0,n.y)(e)?"numeric":"2-digit",minute:"2-digit",second:"2-digit",hourCycle:(0,n.y)(e)?"h12":"h23",timeZone:(0,r.f)(e.time_zone,t)}))),_=(e,t,a)=>p(t,a.time_zone).format(e),p=(0,s.Z)(((e,t)=>new Intl.DateTimeFormat(e.language,{weekday:"long",hour:(0,n.y)(e)?"numeric":"2-digit",minute:"2-digit",hourCycle:(0,n.y)(e)?"h12":"h23",timeZone:(0,r.f)(e.time_zone,t)}))),m=(e,t,a)=>y(t,a.time_zone).format(e),y=(0,s.Z)(((e,t)=>new Intl.DateTimeFormat("en-GB",{hour:"numeric",minute:"2-digit",hour12:!1,timeZone:(0,r.f)(e.time_zone,t)})));o()}catch(d){o(d)}}))},36641:function(e,t,a){a.a(e,(async function(e,o){try{a.d(t,{f:()=>d});var i=a(57900),s=a(1066),r=e([i]);i=(r.then?(await r)():r)[0];const n=Intl.DateTimeFormat?.().resolvedOptions?.().timeZone,l=n??"UTC",d=(e,t)=>e===s.c_.local&&n?l:t;o()}catch(n){o(n)}}))},13819:function(e,t,a){a.d(t,{y:()=>s});var o=a(28105),i=a(1066);const s=(0,o.Z)((e=>{if(e.time_format===i.zt.language||e.time_format===i.zt.system){const t=e.time_format===i.zt.language?e.language:void 0;return new Date("January 1, 2023 22:00:00").toLocaleString(t).includes("10")}return e.time_format===i.zt.am_pm}))},49590:function(e,t,a){a.r(t),a.d(t,{HaIconPicker:()=>_});var o=a(73742),i=a(59048),s=a(7616),r=a(28105),n=a(29740),l=a(18610);a(90256),a(3847),a(57264);let d=[],c=!1;const h=async e=>{try{const t=l.g[e].getIconList;if("function"!=typeof t)return[];const a=await t();return a.map((t=>({icon:`${e}:${t.name}`,parts:new Set(t.name.split("-")),keywords:t.keywords??[]})))}catch(t){return console.warn(`Unable to load icon list for ${e} iconset`),[]}},u=e=>i.dy`
  <ha-combo-box-item type="button">
    <ha-icon .icon=${e.icon} slot="start"></ha-icon>
    ${e.icon}
  </ha-combo-box-item>
`;class _ extends i.oi{render(){return i.dy`
      <ha-combo-box
        .hass=${this.hass}
        item-value-path="icon"
        item-label-path="icon"
        .value=${this._value}
        allow-custom-value
        .dataProvider=${c?this._iconProvider:void 0}
        .label=${this.label}
        .helper=${this.helper}
        .disabled=${this.disabled}
        .required=${this.required}
        .placeholder=${this.placeholder}
        .errorMessage=${this.errorMessage}
        .invalid=${this.invalid}
        .renderer=${u}
        icon
        @opened-changed=${this._openedChanged}
        @value-changed=${this._valueChanged}
      >
        ${this._value||this.placeholder?i.dy`
              <ha-icon .icon=${this._value||this.placeholder} slot="icon">
              </ha-icon>
            `:i.dy`<slot slot="icon" name="fallback"></slot>`}
      </ha-combo-box>
    `}async _openedChanged(e){e.detail.value&&!c&&(await(async()=>{c=!0;const e=await a.e("4813").then(a.t.bind(a,81405,19));d=e.default.map((e=>({icon:`mdi:${e.name}`,parts:new Set(e.name.split("-")),keywords:e.keywords})));const t=[];Object.keys(l.g).forEach((e=>{t.push(h(e))})),(await Promise.all(t)).forEach((e=>{d.push(...e)}))})(),this.requestUpdate())}_valueChanged(e){e.stopPropagation(),this._setValue(e.detail.value)}_setValue(e){this.value=e,(0,n.B)(this,"value-changed",{value:this._value},{bubbles:!1,composed:!1})}get _value(){return this.value||""}constructor(...e){super(...e),this.disabled=!1,this.required=!1,this.invalid=!1,this._filterIcons=(0,r.Z)(((e,t=d)=>{if(!e)return t;const a=[],o=(e,t)=>a.push({icon:e,rank:t});for(const i of t)i.parts.has(e)?o(i.icon,1):i.keywords.includes(e)?o(i.icon,2):i.icon.includes(e)?o(i.icon,3):i.keywords.some((t=>t.includes(e)))&&o(i.icon,4);return 0===a.length&&o(e,0),a.sort(((e,t)=>e.rank-t.rank))})),this._iconProvider=(e,t)=>{const a=this._filterIcons(e.filter.toLowerCase(),d),o=e.page*e.pageSize,i=o+e.pageSize;t(a.slice(o,i),a.length)}}}_.styles=i.iv`
    *[slot="icon"] {
      color: var(--primary-text-color);
      position: relative;
      bottom: 2px;
    }
    *[slot="prefix"] {
      margin-right: 8px;
      margin-inline-end: 8px;
      margin-inline-start: initial;
    }
  `,(0,o.__decorate)([(0,s.Cb)({attribute:!1})],_.prototype,"hass",void 0),(0,o.__decorate)([(0,s.Cb)()],_.prototype,"value",void 0),(0,o.__decorate)([(0,s.Cb)()],_.prototype,"label",void 0),(0,o.__decorate)([(0,s.Cb)()],_.prototype,"helper",void 0),(0,o.__decorate)([(0,s.Cb)()],_.prototype,"placeholder",void 0),(0,o.__decorate)([(0,s.Cb)({attribute:"error-message"})],_.prototype,"errorMessage",void 0),(0,o.__decorate)([(0,s.Cb)({type:Boolean})],_.prototype,"disabled",void 0),(0,o.__decorate)([(0,s.Cb)({type:Boolean})],_.prototype,"required",void 0),(0,o.__decorate)([(0,s.Cb)({type:Boolean})],_.prototype,"invalid",void 0),_=(0,o.__decorate)([(0,s.Mo)("ha-icon-picker")],_)},44516:function(e,t,a){a.a(e,(async function(e,o){try{a.r(t);var i=a(73742),s=a(65650),r=a(77704),n=a(4939),l=a(50789),d=a(57766),c=a(68226),h=a(21343),u=a(31007),_=a(59048),p=a(7616),m=a(13539),y=a(9131),v=a(13819),g=a(29740),f=(a(49590),a(38573),a(9488)),b=a(1066),w=a(41631),k=a(77204),$=e([l,n,s,y]);[l,n,s,y]=$.then?(await $)():$;const C={plugins:[l.Z,n.ZP],headerToolbar:!1,initialView:"timeGridWeek",editable:!0,selectable:!0,selectMirror:!0,selectOverlap:!1,eventOverlap:!1,allDaySlot:!1,height:"parent",locales:r.Z,firstDay:1,dayHeaderFormat:{weekday:"short",month:void 0,day:void 0}};class B extends _.oi{set item(e){this._item=e,e?(this._name=e.name||"",this._icon=e.icon||"",this._monday=e.monday||[],this._tuesday=e.tuesday||[],this._wednesday=e.wednesday||[],this._thursday=e.thursday||[],this._friday=e.friday||[],this._saturday=e.saturday||[],this._sunday=e.sunday||[]):(this._name="",this._icon="",this._monday=[],this._tuesday=[],this._wednesday=[],this._thursday=[],this._friday=[],this._saturday=[],this._sunday=[])}disconnectedCallback(){super.disconnectedCallback(),this.calendar?.destroy(),this.calendar=void 0,this.renderRoot.querySelector("style[data-fullcalendar]")?.remove()}connectedCallback(){super.connectedCallback(),this.hasUpdated&&!this.calendar&&this._setupCalendar()}focus(){this.updateComplete.then((()=>this.shadowRoot?.querySelector("[dialogInitialFocus]")?.focus()))}render(){return this.hass?_.dy`
      <div class="form">
        <ha-textfield
          .value=${this._name}
          .configValue=${"name"}
          @input=${this._valueChanged}
          .label=${this.hass.localize("ui.dialogs.helper_settings.generic.name")}
          autoValidate
          required
          .validationMessage=${this.hass.localize("ui.dialogs.helper_settings.required_error_msg")}
          dialogInitialFocus
        ></ha-textfield>
        <ha-icon-picker
          .hass=${this.hass}
          .value=${this._icon}
          .configValue=${"icon"}
          @value-changed=${this._valueChanged}
          .label=${this.hass.localize("ui.dialogs.helper_settings.generic.icon")}
        ></ha-icon-picker>
        <div id="calendar"></div>
      </div>
    `:_.Ld}willUpdate(e){if(super.willUpdate(e),!this.calendar)return;(e.has("_sunday")||e.has("_monday")||e.has("_tuesday")||e.has("_wednesday")||e.has("_thursday")||e.has("_friday")||e.has("_saturday")||e.has("calendar"))&&(this.calendar.removeAllEventSources(),this.calendar.addEventSource(this._events));const t=e.get("hass");t&&t.language!==this.hass.language&&this.calendar.setOption("locale",this.hass.language)}firstUpdated(){this._setupCalendar()}_setupCalendar(){const e={...C,locale:this.hass.language,firstDay:(0,m.Bt)(this.hass.locale),slotLabelFormat:{hour:"numeric",minute:void 0,hour12:(0,v.y)(this.hass.locale),meridiem:!!(0,v.y)(this.hass.locale)&&"narrow"},eventTimeFormat:{hour:(0,v.y)(this.hass.locale)?"numeric":"2-digit",minute:(0,v.y)(this.hass.locale)?"numeric":"2-digit",hour12:(0,v.y)(this.hass.locale),meridiem:!!(0,v.y)(this.hass.locale)&&"narrow"}};e.eventClick=e=>this._handleEventClick(e),e.select=e=>this._handleSelect(e),e.eventResize=e=>this._handleEventResize(e),e.eventDrop=e=>this._handleEventDrop(e),this.calendar=new s.f(this.shadowRoot.getElementById("calendar"),e),this.calendar.render()}get _events(){const e=[];for(const[t,a]of f.KY.entries())this[`_${a}`].length&&this[`_${a}`].forEach(((o,i)=>{let s=(0,d.O)(new Date,t);(0,c.x)(s,new Date,{weekStartsOn:(0,m.Bt)(this.hass.locale)})||(s=(0,h.E)(s,-7));const r=new Date(s),n=o.from.split(":");r.setHours(parseInt(n[0]),parseInt(n[1]),0,0);const l=new Date(s),u=o.to.split(":");l.setHours(parseInt(u[0]),parseInt(u[1]),0,0),e.push({id:`${a}-${i}`,start:r.toISOString(),end:l.toISOString()})}));return e}_handleSelect(e){const{start:t,end:a}=e,o=f.KY[t.getDay()],i=[...this[`_${o}`]],s={...this._item},r=(0,y.Zs)(a,{...this.hass.locale,time_zone:b.c_.local},this.hass.config);i.push({from:(0,y.Zs)(t,{...this.hass.locale,time_zone:b.c_.local},this.hass.config),to:(0,u.K)(t,a)&&"0:00"!==r?r:"24:00"}),s[o]=i,(0,g.B)(this,"value-changed",{value:s}),(0,u.K)(t,a)||this.calendar.unselect()}_handleEventResize(e){const{id:t,start:a,end:o}=e.event,[i,s]=t.split("-"),r=this[`_${i}`][parseInt(s)],n={...this._item},l=(0,y.Zs)(o,this.hass.locale,this.hass.config);n[i][s]={...n[i][s],from:r.from,to:(0,u.K)(a,o)&&"0:00"!==l?l:"24:00"},(0,g.B)(this,"value-changed",{value:n}),(0,u.K)(a,o)||(this.requestUpdate(`_${i}`),e.revert())}_handleEventDrop(e){const{id:t,start:a,end:o}=e.event,[i,s]=t.split("-"),r=f.KY[a.getDay()],n={...this._item},l=(0,y.Zs)(o,this.hass.locale,this.hass.config),d={...n[i][s],from:(0,y.Zs)(a,this.hass.locale,this.hass.config),to:(0,u.K)(a,o)&&"0:00"!==l?l:"24:00"};if(r===i)n[i][s]=d;else{n[i].splice(s,1);const e=[...this[`_${r}`]];e.push(d),n[r]=e}(0,g.B)(this,"value-changed",{value:n}),(0,u.K)(a,o)||(this.requestUpdate(`_${i}`),e.revert())}async _handleEventClick(e){const[t,a]=e.event.id.split("-"),o=[...this[`_${t}`]][a];(0,w.F)(this,{block:o,updateBlock:e=>this._updateBlock(t,a,e),deleteBlock:()=>this._deleteBlock(t,a)})}_updateBlock(e,t,a){const[o,i,s]=a.from.split(":");a.from=`${o}:${i}`;const[r,n,l]=a.to.split(":");a.to=`${r}:${n}`,0===Number(r)&&0===Number(n)&&(a.to="24:00");const d={...this._item};d[e]=[...this._item[e]],d[e][t]=a,(0,g.B)(this,"value-changed",{value:d})}_deleteBlock(e,t){const a=[...this[`_${e}`]],o={...this._item};a.splice(parseInt(t),1),o[e]=a,(0,g.B)(this,"value-changed",{value:o})}_valueChanged(e){if(!this.new&&!this._item)return;e.stopPropagation();const t=e.target.configValue,a=e.detail?.value||e.target.value;if(this[`_${t}`]===a)return;const o={...this._item};a?o[t]=a:delete o[t],(0,g.B)(this,"value-changed",{value:o})}static get styles(){return[k.Qx,_.iv`
        .form {
          color: var(--primary-text-color);
        }

        ha-textfield {
          display: block;
          margin: 8px 0;
        }

        #calendar {
          margin: 8px 0;
          height: 450px;
          width: 100%;
          -webkit-user-select: none;
          -ms-user-select: none;
          user-select: none;
          --fc-border-color: var(--divider-color);
          --fc-event-border-color: var(--divider-color);
        }

        .fc-v-event .fc-event-time {
          white-space: inherit;
        }
        .fc-theme-standard .fc-scrollgrid {
          border: 1px solid var(--divider-color);
          border-radius: var(--mdc-shape-small, 4px);
        }

        .fc-scrollgrid-section-header td {
          border: none;
        }
        :host([narrow]) .fc-scrollgrid-sync-table {
          overflow: hidden;
        }
        table.fc-scrollgrid-sync-table
          tbody
          tr:first-child
          .fc-daygrid-day-top {
          padding-top: 0;
        }
        .fc-scroller::-webkit-scrollbar {
          width: 0.4rem;
          height: 0.4rem;
        }
        .fc-scroller::-webkit-scrollbar-thumb {
          -webkit-border-radius: 4px;
          border-radius: 4px;
          background: var(--scrollbar-thumb-color);
        }
        .fc-scroller {
          overflow-y: auto;
          scrollbar-color: var(--scrollbar-thumb-color) transparent;
          scrollbar-width: thin;
        }

        .fc-timegrid-event-short .fc-event-time:after {
          content: ""; /* prevent trailing dash in half hour events since we do not have event titles */
        }

        a {
          color: inherit !important;
        }

        th.fc-col-header-cell.fc-day {
          background-color: var(--table-header-background-color);
          color: var(--primary-text-color);
          font-size: var(--ha-font-size-xs);
          font-weight: var(--ha-font-weight-bold);
          text-transform: uppercase;
        }
      `]}constructor(...e){super(...e),this.new=!1}}(0,i.__decorate)([(0,p.Cb)({attribute:!1})],B.prototype,"hass",void 0),(0,i.__decorate)([(0,p.Cb)({type:Boolean})],B.prototype,"new",void 0),(0,i.__decorate)([(0,p.SB)()],B.prototype,"_name",void 0),(0,i.__decorate)([(0,p.SB)()],B.prototype,"_icon",void 0),(0,i.__decorate)([(0,p.SB)()],B.prototype,"_monday",void 0),(0,i.__decorate)([(0,p.SB)()],B.prototype,"_tuesday",void 0),(0,i.__decorate)([(0,p.SB)()],B.prototype,"_wednesday",void 0),(0,i.__decorate)([(0,p.SB)()],B.prototype,"_thursday",void 0),(0,i.__decorate)([(0,p.SB)()],B.prototype,"_friday",void 0),(0,i.__decorate)([(0,p.SB)()],B.prototype,"_saturday",void 0),(0,i.__decorate)([(0,p.SB)()],B.prototype,"_sunday",void 0),(0,i.__decorate)([(0,p.SB)()],B.prototype,"calendar",void 0),B=(0,i.__decorate)([(0,p.Mo)("ha-schedule-form")],B),o()}catch(C){o(C)}}))},41631:function(e,t,a){a.d(t,{F:()=>s});var o=a(29740);const i=()=>a.e("601").then(a.bind(a,74069)),s=(e,t)=>{(0,o.B)(e,"show-dialog",{dialogTag:"dialog-schedule-block-info",dialogImport:i,dialogParams:t})}}};
//# sourceMappingURL=4379.6b1b1a0b96242f2c.js.map