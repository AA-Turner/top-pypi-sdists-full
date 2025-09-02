"use strict";(self.webpackChunkknx_frontend=self.webpackChunkknx_frontend||[]).push([["4379"],{13539:function(e,t,a){a.a(e,(async function(e,i){try{a.d(t,{Bt:function(){return c}});a(39710);var o=a(57900),s=a(3574),n=a(43956),r=e([o]);o=(r.then?(await r)():r)[0];const l=["sunday","monday","tuesday","wednesday","thursday","friday","saturday"],c=e=>e.first_weekday===n.FS.language?"weekInfo"in Intl.Locale.prototype?new Intl.Locale(e.language).weekInfo.firstDay%7:(0,s.L)(e.language)%7:l.includes(e.first_weekday)?l.indexOf(e.first_weekday):1;i()}catch(l){i(l)}}))},9131:function(e,t,a){a.a(e,(async function(e,i){try{a.d(t,{Vu:function(){return h},Zs:function(){return v},mr:function(){return c},xO:function(){return p}});var o=a(57900),s=a(28105),n=a(36641),r=a(13819),l=e([o,n]);[o,n]=l.then?(await l)():l;const c=(e,t,a)=>d(t,a.time_zone).format(e),d=(0,s.Z)(((e,t)=>new Intl.DateTimeFormat(e.language,{hour:"numeric",minute:"2-digit",hourCycle:(0,r.y)(e)?"h12":"h23",timeZone:(0,n.f)(e.time_zone,t)}))),h=(e,t,a)=>u(t,a.time_zone).format(e),u=(0,s.Z)(((e,t)=>new Intl.DateTimeFormat(e.language,{hour:(0,r.y)(e)?"numeric":"2-digit",minute:"2-digit",second:"2-digit",hourCycle:(0,r.y)(e)?"h12":"h23",timeZone:(0,n.f)(e.time_zone,t)}))),p=(e,t,a)=>_(t,a.time_zone).format(e),_=(0,s.Z)(((e,t)=>new Intl.DateTimeFormat(e.language,{weekday:"long",hour:(0,r.y)(e)?"numeric":"2-digit",minute:"2-digit",hourCycle:(0,r.y)(e)?"h12":"h23",timeZone:(0,n.f)(e.time_zone,t)}))),v=(e,t,a)=>m(t,a.time_zone).format(e),m=(0,s.Z)(((e,t)=>new Intl.DateTimeFormat("en-GB",{hour:"numeric",minute:"2-digit",hour12:!1,timeZone:(0,n.f)(e.time_zone,t)})));i()}catch(c){i(c)}}))},36641:function(e,t,a){a.a(e,(async function(e,i){try{a.d(t,{f:function(){return u}});var o,s,n,r=a(57900),l=a(43956),c=e([r]);r=(c.then?(await c)():c)[0];const d=null===(o=Intl.DateTimeFormat)||void 0===o||null===(s=(n=o.call(Intl)).resolvedOptions)||void 0===s?void 0:s.call(n).timeZone,h=null!=d?d:"UTC",u=(e,t)=>e===l.c_.local&&d?h:t;i()}catch(d){i(d)}}))},13819:function(e,t,a){a.d(t,{y:function(){return s}});a(39710),a(56389);var i=a(28105),o=a(43956);const s=(0,i.Z)((e=>{if(e.time_format===o.zt.language||e.time_format===o.zt.system){const t=e.time_format===o.zt.language?e.language:void 0;return new Date("January 1, 2023 22:00:00").toLocaleString(t).includes("10")}return e.time_format===o.zt.am_pm}))},49590:function(e,t,a){a.a(e,(async function(e,i){try{a.r(t),a.d(t,{HaIconPicker:function(){return $}});a(39710),a(26847),a(2394),a(18574),a(81738),a(94814),a(22960),a(6989),a(72489),a(1455),a(67886),a(65451),a(46015),a(38334),a(94880),a(75643),a(29761),a(56389),a(27530);var o=a(73742),s=a(59048),n=a(7616),r=a(28105),l=a(29740),c=a(18610),d=a(54693),h=(a(3847),a(57264),e([d]));d=(h.then?(await h)():h)[0];let u,p,_,v,m,g=e=>e,y=[],f=!1;const b=async()=>{f=!0;const e=await a.e("4813").then(a.t.bind(a,81405,19));y=e.default.map((e=>({icon:`mdi:${e.name}`,parts:new Set(e.name.split("-")),keywords:e.keywords})));const t=[];Object.keys(c.g).forEach((e=>{t.push(w(e))})),(await Promise.all(t)).forEach((e=>{y.push(...e)}))},w=async e=>{try{const t=c.g[e].getIconList;if("function"!=typeof t)return[];const a=await t();return a.map((t=>{var a;return{icon:`${e}:${t.name}`,parts:new Set(t.name.split("-")),keywords:null!==(a=t.keywords)&&void 0!==a?a:[]}}))}catch(t){return console.warn(`Unable to load icon list for ${e} iconset`),[]}},k=e=>(0,s.dy)(u||(u=g`
  <ha-combo-box-item type="button">
    <ha-icon .icon=${0} slot="start"></ha-icon>
    ${0}
  </ha-combo-box-item>
`),e.icon,e.icon);class $ extends s.oi{render(){return(0,s.dy)(p||(p=g`
      <ha-combo-box
        .hass=${0}
        item-value-path="icon"
        item-label-path="icon"
        .value=${0}
        allow-custom-value
        .dataProvider=${0}
        .label=${0}
        .helper=${0}
        .disabled=${0}
        .required=${0}
        .placeholder=${0}
        .errorMessage=${0}
        .invalid=${0}
        .renderer=${0}
        icon
        @opened-changed=${0}
        @value-changed=${0}
      >
        ${0}
      </ha-combo-box>
    `),this.hass,this._value,f?this._iconProvider:void 0,this.label,this.helper,this.disabled,this.required,this.placeholder,this.errorMessage,this.invalid,k,this._openedChanged,this._valueChanged,this._value||this.placeholder?(0,s.dy)(_||(_=g`
              <ha-icon .icon=${0} slot="icon">
              </ha-icon>
            `),this._value||this.placeholder):(0,s.dy)(v||(v=g`<slot slot="icon" name="fallback"></slot>`)))}async _openedChanged(e){e.detail.value&&!f&&(await b(),this.requestUpdate())}_valueChanged(e){e.stopPropagation(),this._setValue(e.detail.value)}_setValue(e){this.value=e,(0,l.B)(this,"value-changed",{value:this._value},{bubbles:!1,composed:!1})}get _value(){return this.value||""}constructor(...e){super(...e),this.disabled=!1,this.required=!1,this.invalid=!1,this._filterIcons=(0,r.Z)(((e,t=y)=>{if(!e)return t;const a=[],i=(e,t)=>a.push({icon:e,rank:t});for(const o of t)o.parts.has(e)?i(o.icon,1):o.keywords.includes(e)?i(o.icon,2):o.icon.includes(e)?i(o.icon,3):o.keywords.some((t=>t.includes(e)))&&i(o.icon,4);return 0===a.length&&i(e,0),a.sort(((e,t)=>e.rank-t.rank))})),this._iconProvider=(e,t)=>{const a=this._filterIcons(e.filter.toLowerCase(),y),i=e.page*e.pageSize,o=i+e.pageSize;t(a.slice(i,o),a.length)}}}$.styles=(0,s.iv)(m||(m=g`
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
  `)),(0,o.__decorate)([(0,n.Cb)({attribute:!1})],$.prototype,"hass",void 0),(0,o.__decorate)([(0,n.Cb)()],$.prototype,"value",void 0),(0,o.__decorate)([(0,n.Cb)()],$.prototype,"label",void 0),(0,o.__decorate)([(0,n.Cb)()],$.prototype,"helper",void 0),(0,o.__decorate)([(0,n.Cb)()],$.prototype,"placeholder",void 0),(0,o.__decorate)([(0,n.Cb)({attribute:"error-message"})],$.prototype,"errorMessage",void 0),(0,o.__decorate)([(0,n.Cb)({type:Boolean})],$.prototype,"disabled",void 0),(0,o.__decorate)([(0,n.Cb)({type:Boolean})],$.prototype,"required",void 0),(0,o.__decorate)([(0,n.Cb)({type:Boolean})],$.prototype,"invalid",void 0),$=(0,o.__decorate)([(0,n.Mo)("ha-icon-picker")],$),i()}catch(u){i(u)}}))},44516:function(e,t,a){a.a(e,(async function(e,i){try{a.r(t);a(26847),a(2394),a(81738),a(22960),a(87799),a(70820),a(1455),a(27530);var o=a(73742),s=a(65650),n=a(77704),r=a(4939),l=a(50789),c=a(57766),d=a(68226),h=a(21343),u=a(31007),p=a(59048),_=a(7616),v=a(13539),m=a(9131),g=a(13819),y=a(29740),f=a(49590),b=(a(38573),a(9488)),w=a(43956),k=a(41631),$=a(77204),C=e([f,l,r,s,v,m]);[f,l,r,s,v,m]=C.then?(await C)():C;let B,x,S=e=>e;const O={plugins:[l.Z,r.ZP],headerToolbar:!1,initialView:"timeGridWeek",editable:!0,selectable:!0,selectMirror:!0,selectOverlap:!1,eventOverlap:!1,allDaySlot:!1,height:"parent",locales:n.Z,firstDay:1,dayHeaderFormat:{weekday:"short",month:void 0,day:void 0}};class I extends p.oi{set item(e){this._item=e,e?(this._name=e.name||"",this._icon=e.icon||"",this._monday=e.monday||[],this._tuesday=e.tuesday||[],this._wednesday=e.wednesday||[],this._thursday=e.thursday||[],this._friday=e.friday||[],this._saturday=e.saturday||[],this._sunday=e.sunday||[]):(this._name="",this._icon="",this._monday=[],this._tuesday=[],this._wednesday=[],this._thursday=[],this._friday=[],this._saturday=[],this._sunday=[])}disconnectedCallback(){var e,t;super.disconnectedCallback(),null===(e=this.calendar)||void 0===e||e.destroy(),this.calendar=void 0,null===(t=this.renderRoot.querySelector("style[data-fullcalendar]"))||void 0===t||t.remove()}connectedCallback(){super.connectedCallback(),this.hasUpdated&&!this.calendar&&this._setupCalendar()}focus(){this.updateComplete.then((()=>{var e;return null===(e=this.shadowRoot)||void 0===e||null===(e=e.querySelector("[dialogInitialFocus]"))||void 0===e?void 0:e.focus()}))}render(){return this.hass?(0,p.dy)(B||(B=S`
      <div class="form">
        <ha-textfield
          .value=${0}
          .configValue=${0}
          @input=${0}
          .label=${0}
          autoValidate
          required
          .validationMessage=${0}
          dialogInitialFocus
        ></ha-textfield>
        <ha-icon-picker
          .hass=${0}
          .value=${0}
          .configValue=${0}
          @value-changed=${0}
          .label=${0}
        ></ha-icon-picker>
        <div id="calendar"></div>
      </div>
    `),this._name,"name",this._valueChanged,this.hass.localize("ui.dialogs.helper_settings.generic.name"),this.hass.localize("ui.dialogs.helper_settings.required_error_msg"),this.hass,this._icon,"icon",this._valueChanged,this.hass.localize("ui.dialogs.helper_settings.generic.icon")):p.Ld}willUpdate(e){if(super.willUpdate(e),!this.calendar)return;(e.has("_sunday")||e.has("_monday")||e.has("_tuesday")||e.has("_wednesday")||e.has("_thursday")||e.has("_friday")||e.has("_saturday")||e.has("calendar"))&&(this.calendar.removeAllEventSources(),this.calendar.addEventSource(this._events));const t=e.get("hass");t&&t.language!==this.hass.language&&this.calendar.setOption("locale",this.hass.language)}firstUpdated(){this._setupCalendar()}_setupCalendar(){const e=Object.assign(Object.assign({},O),{},{locale:this.hass.language,firstDay:(0,v.Bt)(this.hass.locale),slotLabelFormat:{hour:"numeric",minute:void 0,hour12:(0,g.y)(this.hass.locale),meridiem:!!(0,g.y)(this.hass.locale)&&"narrow"},eventTimeFormat:{hour:(0,g.y)(this.hass.locale)?"numeric":"2-digit",minute:(0,g.y)(this.hass.locale)?"numeric":"2-digit",hour12:(0,g.y)(this.hass.locale),meridiem:!!(0,g.y)(this.hass.locale)&&"narrow"}});e.eventClick=e=>this._handleEventClick(e),e.select=e=>this._handleSelect(e),e.eventResize=e=>this._handleEventResize(e),e.eventDrop=e=>this._handleEventDrop(e),this.calendar=new s.f(this.shadowRoot.getElementById("calendar"),e),this.calendar.render()}get _events(){const e=[];for(const[t,a]of b.KY.entries())this[`_${a}`].length&&this[`_${a}`].forEach(((i,o)=>{let s=(0,c.O)(new Date,t);(0,d.x)(s,new Date,{weekStartsOn:(0,v.Bt)(this.hass.locale)})||(s=(0,h.E)(s,-7));const n=new Date(s),r=i.from.split(":");n.setHours(parseInt(r[0]),parseInt(r[1]),0,0);const l=new Date(s),u=i.to.split(":");l.setHours(parseInt(u[0]),parseInt(u[1]),0,0),e.push({id:`${a}-${o}`,start:n.toISOString(),end:l.toISOString()})}));return e}_handleSelect(e){const{start:t,end:a}=e,i=b.KY[t.getDay()],o=[...this[`_${i}`]],s=Object.assign({},this._item),n=(0,m.Zs)(a,Object.assign(Object.assign({},this.hass.locale),{},{time_zone:w.c_.local}),this.hass.config);o.push({from:(0,m.Zs)(t,Object.assign(Object.assign({},this.hass.locale),{},{time_zone:w.c_.local}),this.hass.config),to:(0,u.K)(t,a)&&"0:00"!==n?n:"24:00"}),s[i]=o,(0,y.B)(this,"value-changed",{value:s}),(0,u.K)(t,a)||this.calendar.unselect()}_handleEventResize(e){const{id:t,start:a,end:i}=e.event,[o,s]=t.split("-"),n=this[`_${o}`][parseInt(s)],r=Object.assign({},this._item),l=(0,m.Zs)(i,this.hass.locale,this.hass.config);r[o][s]=Object.assign(Object.assign({},r[o][s]),{},{from:n.from,to:(0,u.K)(a,i)&&"0:00"!==l?l:"24:00"}),(0,y.B)(this,"value-changed",{value:r}),(0,u.K)(a,i)||(this.requestUpdate(`_${o}`),e.revert())}_handleEventDrop(e){const{id:t,start:a,end:i}=e.event,[o,s]=t.split("-"),n=b.KY[a.getDay()],r=Object.assign({},this._item),l=(0,m.Zs)(i,this.hass.locale,this.hass.config),c=Object.assign(Object.assign({},r[o][s]),{},{from:(0,m.Zs)(a,this.hass.locale,this.hass.config),to:(0,u.K)(a,i)&&"0:00"!==l?l:"24:00"});if(n===o)r[o][s]=c;else{r[o].splice(s,1);const e=[...this[`_${n}`]];e.push(c),r[n]=e}(0,y.B)(this,"value-changed",{value:r}),(0,u.K)(a,i)||(this.requestUpdate(`_${o}`),e.revert())}async _handleEventClick(e){const[t,a]=e.event.id.split("-"),i=[...this[`_${t}`]][a];(0,k.F)(this,{block:i,updateBlock:e=>this._updateBlock(t,a,e),deleteBlock:()=>this._deleteBlock(t,a)})}_updateBlock(e,t,a){const[i,o,s]=a.from.split(":");a.from=`${i}:${o}`;const[n,r,l]=a.to.split(":");a.to=`${n}:${r}`,0===Number(n)&&0===Number(r)&&(a.to="24:00");const c=Object.assign({},this._item);c[e]=[...this._item[e]],c[e][t]=a,(0,y.B)(this,"value-changed",{value:c})}_deleteBlock(e,t){const a=[...this[`_${e}`]],i=Object.assign({},this._item);a.splice(parseInt(t),1),i[e]=a,(0,y.B)(this,"value-changed",{value:i})}_valueChanged(e){var t;if(!this.new&&!this._item)return;e.stopPropagation();const a=e.target.configValue,i=(null===(t=e.detail)||void 0===t?void 0:t.value)||e.target.value;if(this[`_${a}`]===i)return;const o=Object.assign({},this._item);i?o[a]=i:delete o[a],(0,y.B)(this,"value-changed",{value:o})}static get styles(){return[$.Qx,(0,p.iv)(x||(x=S`
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
      `))]}constructor(...e){super(...e),this.new=!1}}(0,o.__decorate)([(0,_.Cb)({attribute:!1})],I.prototype,"hass",void 0),(0,o.__decorate)([(0,_.Cb)({type:Boolean})],I.prototype,"new",void 0),(0,o.__decorate)([(0,_.SB)()],I.prototype,"_name",void 0),(0,o.__decorate)([(0,_.SB)()],I.prototype,"_icon",void 0),(0,o.__decorate)([(0,_.SB)()],I.prototype,"_monday",void 0),(0,o.__decorate)([(0,_.SB)()],I.prototype,"_tuesday",void 0),(0,o.__decorate)([(0,_.SB)()],I.prototype,"_wednesday",void 0),(0,o.__decorate)([(0,_.SB)()],I.prototype,"_thursday",void 0),(0,o.__decorate)([(0,_.SB)()],I.prototype,"_friday",void 0),(0,o.__decorate)([(0,_.SB)()],I.prototype,"_saturday",void 0),(0,o.__decorate)([(0,_.SB)()],I.prototype,"_sunday",void 0),(0,o.__decorate)([(0,_.SB)()],I.prototype,"calendar",void 0),I=(0,o.__decorate)([(0,_.Mo)("ha-schedule-form")],I),i()}catch(B){i(B)}}))},41631:function(e,t,a){a.d(t,{F:function(){return s}});a(26847),a(1455),a(27530);var i=a(29740);const o=()=>a.e("601").then(a.bind(a,74069)),s=(e,t)=>{(0,i.B)(e,"show-dialog",{dialogTag:"dialog-schedule-block-info",dialogImport:o,dialogParams:t})}}}]);
//# sourceMappingURL=4379.528032924a49c055.js.map