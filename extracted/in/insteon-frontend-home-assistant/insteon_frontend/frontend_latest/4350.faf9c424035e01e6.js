/*! For license information please see 4350.faf9c424035e01e6.js.LICENSE.txt */
export const __webpack_id__="4350";export const __webpack_ids__=["4350"];export const __webpack_modules__={43102:function(e,t,a){a.d(t,{K:()=>r,t:()=>i});var n=a(96196);const r=n.qy`<svg height="24" viewBox="0 0 24 24" width="24"><path d="M15.41 7.41L14 6l-6 6 6 6 1.41-1.41L10.83 12z"></path></svg>`,i=n.qy`<svg height="24" viewBox="0 0 24 24" width="24"><path d="M10 6L8.59 7.41 13.17 12l-4.58 4.59L10 18l6-6z"></path></svg>`},35769:function(e,t,a){a.a(e,async function(e,t){try{var n=a(52588),r=a(33143),i=a(12402),o=e([n,r]);[n,r]=o.then?(await o)():o,(0,i.U)(n.$4,r.t),t()}catch(s){t(s)}})},73095:function(e,t,a){a.d(t,{WA:()=>r,mm:()=>i});var n=a(96196);const r=n.AH`
button {
  -webkit-appearance: none;
  -moz-appearance: none;
  appearance: none;

  position: relative;
  display: block;
  margin: 0;
  padding: 0;
  background: none; /** NOTE: IE11 fix */
  color: inherit;
  border: none;
  font: inherit;
  text-align: left;
  text-transform: inherit;
  -webkit-tap-highlight-color: rgba(0, 0, 0, 0);
}
`,i=(n.AH`
a {
  -webkit-tap-highlight-color: rgba(0, 0, 0, 0);

  position: relative;
  display: inline-block;
  background: initial;
  color: inherit;
  font: inherit;
  text-transform: inherit;
  text-decoration: none;
  outline: none;
}
a:focus,
a:focus.page-selected {
  text-decoration: underline;
}
`,n.AH`
svg {
  display: block;
  min-width: var(--svg-icon-min-width, 24px);
  min-height: var(--svg-icon-min-height, 24px);
  fill: var(--svg-icon-fill, currentColor);
  pointer-events: none;
}
`,n.AH`[hidden] { display: none !important; }`,n.AH`
:host {
  display: block;

  /* --app-datepicker-width: 300px; */
  /* --app-datepicker-primary-color: #4285f4; */
  /* --app-datepicker-header-height: 80px; */
}

* {
  box-sizing: border-box;
}
`)},52588:function(e,t,a){a.a(e,async function(e,n){try{a.d(t,{$4:()=>y,$g:()=>u,B0:()=>o,Gf:()=>d,YB:()=>p,eB:()=>c,tn:()=>h});var r=a(22),i=e([r]);r=(i.then?(await i)():i)[0];const o=Intl&&Intl.DateTimeFormat,s=[38,33,36],l=[40,34,35],d=new Set([37,...s]),c=new Set([39,...l]),u=new Set([39,...s]),h=new Set([37,...l]),p=new Set([37,39,...s,...l]),y="app-datepicker";n()}catch(o){n(o)}})},33143:function(e,t,a){a.a(e,async function(e,n){try{a.d(t,{t:()=>L});var r=a(62826),i=a(96196),o=a(77845),s=a(57378),l=a(94333),d=a(4937),c=a(13192),u=a(43102),h=a(73095),p=a(52588),y=a(58981),f=a(35676),m=a(82004),_=a(24571),b=a(97076),w=a(20335),g=a(86530),v=a(57445),k=a(46719),D=a(47614),x=a(60117),S=a(57407),C=a(447),T=a(84073),$=a(30622),F=a(49060),M=a(93739),U=a(74745),E=a(46977),N=e([p,f,k,w]);[p,f,k,w]=N.then?(await N)():N;class L extends i.WF{get startView(){return this._startView}set startView(e){const t=e||"calendar";if("calendar"!==t&&"yearList"!==t)return;const a=this._startView;this._startView=t,this.requestUpdate("startView",a)}get min(){return this._hasMin?(0,F.h)(this._min):""}set min(e){const t=(0,v.t)(e),a=(0,x.v)(e,t);this._min=a?t:this._todayDate,this._hasMin=a,this.requestUpdate("min")}get max(){return this._hasMax?(0,F.h)(this._max):""}set max(e){const t=(0,v.t)(e),a=(0,x.v)(e,t);this._max=a?t:this._maxDate,this._hasMax=a,this.requestUpdate("max")}get value(){return(0,F.h)(this._focusedDate)}set value(e){const t=(0,v.t)(e),a=(0,x.v)(e,t)?t:this._todayDate;this._focusedDate=new Date(a),this._selectedDate=this._lastSelectedDate=new Date(a)}disconnectedCallback(){super.disconnectedCallback(),this._tracker&&(this._tracker.disconnect(),this._tracker=void 0)}render(){this._formatters.locale!==this.locale&&(this._formatters=(0,w.G)(this.locale));const e="yearList"===this._startView?this._renderDatepickerYearList():this._renderDatepickerCalendar(),t=this.inline?null:i.qy`<div class="datepicker-header" part="header">${this._renderHeaderSelectorButton()}</div>`;return i.qy`
    ${t}
    <div class="datepicker-body" part="body">${(0,s.P)(e)}</div>
    `}firstUpdated(){let e;e="calendar"===this._startView?this.inline?this.shadowRoot.querySelector(".btn__month-selector"):this._buttonSelectorYear:this._yearViewListItem,(0,m.w)(this,"datepicker-first-updated",{firstFocusableElement:e,value:this.value})}async updated(e){const t=this._startView;if(e.has("min")||e.has("max")){this._yearList=(0,M.N)(this._min,this._max),"yearList"===t&&this.requestUpdate();const e=+this._min,a=+this._max;if((0,b.u)(e,a)>864e5){const t=+this._focusedDate;let n=t;t<e&&(n=e),t>a&&(n=a),this.value=(0,F.h)(new Date(n))}}if(e.has("_startView")||e.has("startView")){if("yearList"===t){const e=48*(this._selectedDate.getUTCFullYear()-this._min.getUTCFullYear()-2);(0,$.G)(this._yearViewFullList,{top:e,left:0})}if("calendar"===t&&null==this._tracker){const e=this.calendarsContainer;let t=!1,a=!1,n=!1;if(e){const r={down:()=>{n||(t=!0,this._dx=0)},move:(r,i)=>{if(n||!t)return;const o=this._dx,s=o<0&&(0,D.n)(e,"has-max-date")||o>0&&(0,D.n)(e,"has-min-date");!s&&Math.abs(o)>0&&t&&(a=!0,e.style.transform=`translateX(${(0,S.b)(o)}px)`),this._dx=s?0:o+(r.x-i.x)},up:async(r,i,o)=>{if(t&&a){const r=this._dx,i=e.getBoundingClientRect().width/3,o=Math.abs(r)>Number(this.dragRatio)*i,s=350,l="cubic-bezier(0, 0, .4, 1)",d=o?(0,S.b)(i*(r<0?-1:1)):0;n=!0,await(0,y.K)(e,{hasNativeWebAnimation:this._hasNativeWebAnimation,keyframes:[{transform:`translateX(${r}px)`},{transform:`translateX(${d}px)`}],options:{duration:s,easing:l}}),o&&this._updateMonth(r<0?"next":"previous").handleEvent(),t=a=n=!1,this._dx=-1/0,e.removeAttribute("style"),(0,m.w)(this,"datepicker-animation-finished")}else t&&(this._updateFocusedDate(o),t=a=!1,this._dx=-1/0)}};this._tracker=new E.J(e,r)}}e.get("_startView")&&"calendar"===t&&this._focusElement('[part="year-selector"]')}this._updatingDateWithKey&&(this._focusElement('[part="calendars"]:nth-of-type(2) .day--focused'),this._updatingDateWithKey=!1)}_focusElement(e){const t=this.shadowRoot.querySelector(e);t&&t.focus()}_renderHeaderSelectorButton(){const{yearFormat:e,dateFormat:t}=this._formatters,a="calendar"===this.startView,n=this._focusedDate,r=t(n),o=e(n);return i.qy`
    <button
      class="${(0,l.H)({"btn__year-selector":!0,selected:!a})}"
      type="button"
      part="year-selector"
      data-view="${"yearList"}"
      @click="${this._updateView("yearList")}">${o}</button>

    <div class="datepicker-toolbar" part="toolbar">
      <button
        class="${(0,l.H)({"btn__calendar-selector":!0,selected:a})}"
        type="button"
        part="calendar-selector"
        data-view="${"calendar"}"
        @click="${this._updateView("calendar")}">${r}</button>
    </div>
    `}_renderDatepickerYearList(){const{yearFormat:e}=this._formatters,t=this._focusedDate.getUTCFullYear();return i.qy`
    <div class="datepicker-body__year-list-view" part="year-list-view">
      <div class="year-list-view__full-list" part="year-list" @click="${this._updateYear}">
      ${this._yearList.map(a=>i.qy`<button
        class="${(0,l.H)({"year-list-view__list-item":!0,"year--selected":t===a})}"
        type="button"
        part="year"
        .year="${a}">${e((0,c.m)(a,0,1))}</button>`)}</div>
    </div>
    `}_renderDatepickerCalendar(){const{longMonthYearFormat:e,dayFormat:t,fullDateFormat:a,longWeekdayFormat:n,narrowWeekdayFormat:r}=this._formatters,o=(0,T.S)(this.disabledDays,Number),s=(0,T.S)(this.disabledDates,v.t),c=this.showWeekNumber,h=this._focusedDate,p=this.firstDayOfWeek,y=(0,v.t)(),m=this._selectedDate,_=this._max,b=this._min,{calendars:w,disabledDaysSet:k,disabledDatesSet:D,weekdays:x}=(0,g.n)({dayFormat:t,fullDateFormat:a,longWeekdayFormat:n,narrowWeekdayFormat:r,firstDayOfWeek:p,disabledDays:o,disabledDates:s,locale:this.locale,selectedDate:m,showWeekNumber:this.showWeekNumber,weekNumberType:this.weekNumberType,max:_,min:b,weekLabel:this.weekLabel}),S=!w[0].calendar.length,C=!w[2].calendar.length,$=x.map(e=>i.qy`<th
        class="calendar-weekday"
        part="calendar-weekday"
        role="columnheader"
        aria-label="${e.label}"
      >
        <div class="weekday" part="weekday">${e.value}</div>
      </th>`),F=(0,d.u)(w,e=>e.key,({calendar:t},a)=>{if(!t.length)return i.qy`<div class="calendar-container" part="calendar"></div>`;const n=`calendarcaption${a}`,r=t[1][1].fullDate,o=1===a,s=o&&!this._isInVisibleMonth(h,m)?(0,f.Y)({disabledDaysSet:k,disabledDatesSet:D,hasAltKey:!1,keyCode:36,focusedDate:h,selectedDate:m,minTime:+b,maxTime:+_}):h;return i.qy`
      <div class="calendar-container" part="calendar">
        <table class="calendar-table" part="table" role="grid" aria-labelledby="${n}">
          <caption id="${n}">
            <div class="calendar-label" part="label">${r?e(r):""}</div>
          </caption>

          <thead role="rowgroup">
            <tr class="calendar-weekdays" part="weekdays" role="row">${$}</tr>
          </thead>

          <tbody role="rowgroup">${t.map(e=>i.qy`<tr role="row">${e.map((e,t)=>{const{disabled:a,fullDate:n,label:r,value:d}=e;if(!n&&d&&c&&t<1)return i.qy`<th
                      class="full-calendar__day weekday-label"
                      part="calendar-day"
                      scope="row"
                      role="rowheader"
                      abbr="${r}"
                      aria-label="${r}"
                    >${d}</th>`;if(!d||!n)return i.qy`<td class="full-calendar__day day--empty" part="calendar-day"></td>`;const u=+new Date(n),p=+h===u,f=o&&s.getUTCDate()===Number(d);return i.qy`
                  <td
                    tabindex="${f?"0":"-1"}"
                    class="${(0,l.H)({"full-calendar__day":!0,"day--disabled":a,"day--today":+y===u,"day--focused":!a&&p})}"
                    part="calendar-day${+y===u?" calendar-today":""}"
                    role="gridcell"
                    aria-disabled="${a?"true":"false"}"
                    aria-label="${r}"
                    aria-selected="${p?"true":"false"}"
                    .fullDate="${n}"
                    .day="${d}"
                  >
                    <div
                      class="calendar-day"
                      part="day${+y===u?" today":""}"
                    >${d}</div>
                  </td>
                  `})}</tr>`)}</tbody>
        </table>
      </div>
      `});return this._disabledDatesSet=D,this._disabledDaysSet=k,i.qy`
    <div class="datepicker-body__calendar-view" part="calendar-view">
      <div class="calendar-view__month-selector" part="month-selectors">
        <div class="month-selector-container">${S?null:i.qy`
          <button
            class="btn__month-selector"
            type="button"
            part="month-selector"
            aria-label="Previous month"
            @click="${this._updateMonth("previous")}"
          >${u.K}</button>
        `}</div>

        <div class="month-selector-container">${C?null:i.qy`
          <button
            class="btn__month-selector"
            type="button"
            part="month-selector"
            aria-label="Next month"
            @click="${this._updateMonth("next")}"
          >${u.t}</button>
        `}</div>
      </div>

      <div
        class="${(0,l.H)({"calendars-container":!0,"has-min-date":S,"has-max-date":C})}"
        part="calendars"
        @keyup="${this._updateFocusedDateWithKeyboard}"
      >${F}</div>
    </div>
    `}_updateView(e){return(0,C.c)(()=>{"calendar"===e&&(this._selectedDate=this._lastSelectedDate=new Date((0,U.V)(this._focusedDate,this._min,this._max))),this._startView=e})}_updateMonth(e){return(0,C.c)(()=>{if(null==this.calendarsContainer)return this.updateComplete;const t=this._lastSelectedDate||this._selectedDate,a=this._min,n=this._max,r="previous"===e,i=(0,c.m)(t.getUTCFullYear(),t.getUTCMonth()+(r?-1:1),1),o=i.getUTCFullYear(),s=i.getUTCMonth(),l=a.getUTCFullYear(),d=a.getUTCMonth(),u=n.getUTCFullYear(),h=n.getUTCMonth();return o<l||o<=l&&s<d||(o>u||o>=u&&s>h)||(this._lastSelectedDate=i,this._selectedDate=this._lastSelectedDate),this.updateComplete})}_updateYear(e){const t=(0,_.z)(e,e=>(0,D.n)(e,"year-list-view__list-item"));if(null==t)return;const a=(0,U.V)(new Date(this._focusedDate).setUTCFullYear(+t.year),this._min,this._max);this._selectedDate=this._lastSelectedDate=new Date(a),this._focusedDate=new Date(a),this._startView="calendar"}_updateFocusedDate(e){const t=(0,_.z)(e,e=>(0,D.n)(e,"full-calendar__day"));null==t||["day--empty","day--disabled","day--focused","weekday-label"].some(e=>(0,D.n)(t,e))||(this._focusedDate=new Date(t.fullDate),(0,m.w)(this,"datepicker-value-updated",{isKeypress:!1,value:this.value}))}_updateFocusedDateWithKeyboard(e){const t=e.keyCode;if(13===t||32===t)return(0,m.w)(this,"datepicker-value-updated",{keyCode:t,isKeypress:!0,value:this.value}),void(this._focusedDate=new Date(this._selectedDate));if(9===t||!p.YB.has(t))return;const a=this._selectedDate,n=(0,f.Y)({keyCode:t,selectedDate:a,disabledDatesSet:this._disabledDatesSet,disabledDaysSet:this._disabledDaysSet,focusedDate:this._focusedDate,hasAltKey:e.altKey,maxTime:+this._max,minTime:+this._min});this._isInVisibleMonth(n,a)||(this._selectedDate=this._lastSelectedDate=n),this._focusedDate=n,this._updatingDateWithKey=!0,(0,m.w)(this,"datepicker-value-updated",{keyCode:t,isKeypress:!0,value:this.value})}_isInVisibleMonth(e,t){const a=e.getUTCFullYear(),n=e.getUTCMonth(),r=t.getUTCFullYear(),i=t.getUTCMonth();return a===r&&n===i}get calendarsContainer(){return this.shadowRoot.querySelector(".calendars-container")}constructor(){super(),this.firstDayOfWeek=0,this.showWeekNumber=!1,this.weekNumberType="first-4-day-week",this.landscape=!1,this.locale=(0,k.f)(),this.disabledDays="",this.disabledDates="",this.weekLabel="Wk",this.inline=!1,this.dragRatio=.15,this._hasMin=!1,this._hasMax=!1,this._disabledDaysSet=new Set,this._disabledDatesSet=new Set,this._dx=-1/0,this._hasNativeWebAnimation="animate"in HTMLElement.prototype,this._updatingDateWithKey=!1;const e=(0,v.t)(),t=(0,w.G)(this.locale),a=(0,F.h)(e),n=(0,v.t)("2100-12-31");this.value=a,this.startView="calendar",this._min=new Date(e),this._max=new Date(n),this._todayDate=e,this._maxDate=n,this._yearList=(0,M.N)(e,n),this._selectedDate=new Date(e),this._focusedDate=new Date(e),this._formatters=t}}L.styles=[h.mm,h.WA,i.AH`
    :host {
      width: 312px;
      /** NOTE: Magic number as 16:9 aspect ratio does not look good */
      /* height: calc((var(--app-datepicker-width) / .66) - var(--app-datepicker-footer-height, 56px)); */
      background-color: var(--app-datepicker-bg-color, #fff);
      color: var(--app-datepicker-color, #000);
      border-radius:
        var(--app-datepicker-border-top-left-radius, 0)
        var(--app-datepicker-border-top-right-radius, 0)
        var(--app-datepicker-border-bottom-right-radius, 0)
        var(--app-datepicker-border-bottom-left-radius, 0);
      contain: content;
      overflow: hidden;
    }
    :host([landscape]) {
      display: flex;

      /** <iphone-5-landscape-width> - <standard-side-margin-width> */
      min-width: calc(568px - 16px * 2);
      width: calc(568px - 16px * 2);
    }

    .datepicker-header + .datepicker-body {
      border-top: 1px solid var(--app-datepicker-separator-color, #ddd);
    }
    :host([landscape]) > .datepicker-header + .datepicker-body {
      border-top: none;
      border-left: 1px solid var(--app-datepicker-separator-color, #ddd);
    }

    .datepicker-header {
      display: flex;
      flex-direction: column;
      align-items: flex-start;

      position: relative;
      padding: 16px 24px;
    }
    :host([landscape]) > .datepicker-header {
      /** :this.<one-liner-month-day-width> + :this.<side-padding-width> */
      min-width: calc(14ch + 24px * 2);
    }

    .btn__year-selector,
    .btn__calendar-selector {
      color: var(--app-datepicker-selector-color, rgba(0, 0, 0, .55));
      cursor: pointer;
      /* outline: none; */
    }
    .btn__year-selector.selected,
    .btn__calendar-selector.selected {
      color: currentColor;
    }

    /**
      * NOTE: IE11-only fix. This prevents formatted focused date from overflowing the container.
      */
    .datepicker-toolbar {
      width: 100%;
    }

    .btn__year-selector {
      font-size: 16px;
      font-weight: 700;
    }
    .btn__calendar-selector {
      font-size: 36px;
      font-weight: 700;
      line-height: 1;
    }

    .datepicker-body {
      position: relative;
      width: 100%;
      overflow: hidden;
    }

    .datepicker-body__calendar-view {
      min-height: 56px;
    }

    .calendar-view__month-selector {
      display: flex;
      align-items: center;

      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      padding: 0 8px;
      z-index: 1;
    }

    .month-selector-container {
      max-height: 56px;
      height: 100%;
    }
    .month-selector-container + .month-selector-container {
      margin: 0 0 0 auto;
    }

    .btn__month-selector {
      padding: calc((56px - 24px) / 2);
      /**
        * NOTE: button element contains no text, only SVG.
        * No extra height will incur with such setting.
        */
      line-height: 0;
    }
    .btn__month-selector > svg {
      fill: currentColor;
    }

    .calendars-container {
      display: flex;
      justify-content: center;

      position: relative;
      top: 0;
      left: calc(-100%);
      width: calc(100% * 3);
      transform: translateZ(0);
      will-change: transform;
      /**
        * NOTE: Required for Pointer Events API to work on touch devices.
        * Native \`pan-y\` action will be fired by the browsers since we only care about the
        * horizontal direction. This is great as vertical scrolling still works even when touch
        * event happens on a datepicker's calendar.
        */
      touch-action: pan-y;
      /* outline: none; */
    }

    .year-list-view__full-list {
      max-height: calc(48px * 7);
      overflow-y: auto;

      scrollbar-color: var(--app-datepicker-scrollbar-thumb-bg-color, rgba(0, 0, 0, .35)) rgba(0, 0, 0, 0);
      scrollbar-width: thin;
    }
    .year-list-view__full-list::-webkit-scrollbar {
      width: 8px;
      background-color: rgba(0, 0, 0, 0);
    }
    .year-list-view__full-list::-webkit-scrollbar-thumb {
      background-color: var(--app-datepicker-scrollbar-thumb-bg-color, rgba(0, 0, 0, .35));
      border-radius: 50px;
    }
    .year-list-view__full-list::-webkit-scrollbar-thumb:hover {
      background-color: var(--app-datepicker-scrollbar-thumb-hover-bg-color, rgba(0, 0, 0, .5));
    }

    .calendar-weekdays > th,
    .weekday-label {
      color: var(--app-datepicker-weekday-color, rgba(0, 0, 0, .55));
      font-weight: 400;
      transform: translateZ(0);
      will-change: transform;
    }

    .calendar-container,
    .calendar-label,
    .calendar-table {
      width: 100%;
    }

    .calendar-container {
      position: relative;
      padding: 0 16px 16px;
    }

    .calendar-table {
      -moz-user-select: none;
      -webkit-user-select: none;
      user-select: none;

      border-collapse: collapse;
      border-spacing: 0;
      text-align: center;
    }

    .calendar-label {
      display: flex;
      align-items: center;
      justify-content: center;

      height: 56px;
      font-weight: 500;
      text-align: center;
    }

    .calendar-weekday,
    .full-calendar__day {
      position: relative;
      width: calc(100% / 7);
      height: 0;
      padding: calc(100% / 7 / 2) 0;
      outline: none;
      text-align: center;
    }
    .full-calendar__day:not(.day--disabled):focus {
      outline: #000 dotted 1px;
      outline: -webkit-focus-ring-color auto 1px;
    }
    :host([showweeknumber]) .calendar-weekday,
    :host([showweeknumber]) .full-calendar__day {
      width: calc(100% / 8);
      padding-top: calc(100% / 8);
      padding-bottom: 0;
    }
    :host([showweeknumber]) th.weekday-label {
      padding: 0;
    }

    /**
      * NOTE: Interesting fact! That is ::after will trigger paint when dragging. This will trigger
      * layout and paint on **ONLY** affected nodes. This is much cheaper as compared to rendering
      * all :::after of all calendar day elements. When dragging the entire calendar container,
      * because of all layout and paint trigger on each and every ::after, this becomes a expensive
      * task for the browsers especially on low-end devices. Even though animating opacity is much
      * cheaper, the technique does not work here. Adding 'will-change' will further reduce overall
      * painting at the expense of memory consumption as many cells in a table has been promoted
      * a its own layer.
      */
    .full-calendar__day:not(.day--empty):not(.day--disabled):not(.weekday-label) {
      transform: translateZ(0);
      will-change: transform;
    }
    .full-calendar__day:not(.day--empty):not(.day--disabled):not(.weekday-label).day--focused::after,
    .full-calendar__day:not(.day--empty):not(.day--disabled):not(.day--focused):not(.weekday-label):hover::after {
      content: '';
      display: block;
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background-color: var(--app-datepicker-accent-color, #1a73e8);
      border-radius: 50%;
      opacity: 0;
      pointer-events: none;
    }
    .full-calendar__day:not(.day--empty):not(.day--disabled):not(.weekday-label) {
      cursor: pointer;
      pointer-events: auto;
      -webkit-tap-highlight-color: rgba(0, 0, 0, 0);
    }
    .full-calendar__day.day--focused:not(.day--empty):not(.day--disabled):not(.weekday-label)::after,
    .full-calendar__day.day--today.day--focused:not(.day--empty):not(.day--disabled):not(.weekday-label)::after {
      opacity: 1;
    }

    .calendar-weekday > .weekday,
    .full-calendar__day > .calendar-day {
      display: flex;
      align-items: center;
      justify-content: center;

      position: absolute;
      top: 5%;
      left: 5%;
      width: 90%;
      height: 90%;
      color: currentColor;
      font-size: 14px;
      pointer-events: none;
      z-index: 1;
    }
    .full-calendar__day.day--today {
      color: var(--app-datepicker-accent-color, #1a73e8);
    }
    .full-calendar__day.day--focused,
    .full-calendar__day.day--today.day--focused {
      color: var(--app-datepicker-focused-day-color, #fff);
    }
    .full-calendar__day.day--empty,
    .full-calendar__day.weekday-label,
    .full-calendar__day.day--disabled > .calendar-day {
      pointer-events: none;
    }
    .full-calendar__day.day--disabled:not(.day--today) {
      color: var(--app-datepicker-disabled-day-color, rgba(0, 0, 0, .55));
    }

    .year-list-view__list-item {
      position: relative;
      width: 100%;
      padding: 12px 16px;
      text-align: center;
      /** NOTE: Reduce paint when hovering and scrolling, but this increases memory usage */
      /* will-change: opacity; */
      /* outline: none; */
    }
    .year-list-view__list-item::after {
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background-color: var(--app-datepicker-focused-year-bg-color, #000);
      opacity: 0;
      pointer-events: none;
    }
    .year-list-view__list-item:focus::after {
      opacity: .05;
    }
    .year-list-view__list-item.year--selected {
      color: var(--app-datepicker-accent-color, #1a73e8);
      font-size: 24px;
      font-weight: 500;
    }

    @media (any-hover: hover) {
      .btn__month-selector:hover,
      .year-list-view__list-item:hover {
        cursor: pointer;
      }
      .full-calendar__day:not(.day--empty):not(.day--disabled):not(.day--focused):not(.weekday-label):hover::after {
        opacity: .15;
      }
      .year-list-view__list-item:hover::after {
        opacity: .05;
      }
    }

    @supports (background: -webkit-canvas(squares)) {
      .calendar-container {
        padding: 56px 16px 16px;
      }

      table > caption {
        position: absolute;
        top: 0;
        left: 50%;
        transform: translate3d(-50%, 0, 0);
        will-change: transform;
      }
    }
    `],(0,r.__decorate)([(0,o.MZ)({type:Number,reflect:!0})],L.prototype,"firstDayOfWeek",void 0),(0,r.__decorate)([(0,o.MZ)({type:Boolean,reflect:!0})],L.prototype,"showWeekNumber",void 0),(0,r.__decorate)([(0,o.MZ)({type:String,reflect:!0})],L.prototype,"weekNumberType",void 0),(0,r.__decorate)([(0,o.MZ)({type:Boolean,reflect:!0})],L.prototype,"landscape",void 0),(0,r.__decorate)([(0,o.MZ)({type:String,reflect:!0})],L.prototype,"startView",null),(0,r.__decorate)([(0,o.MZ)({type:String,reflect:!0})],L.prototype,"min",null),(0,r.__decorate)([(0,o.MZ)({type:String,reflect:!0})],L.prototype,"max",null),(0,r.__decorate)([(0,o.MZ)({type:String})],L.prototype,"value",null),(0,r.__decorate)([(0,o.MZ)({type:String})],L.prototype,"locale",void 0),(0,r.__decorate)([(0,o.MZ)({type:String})],L.prototype,"disabledDays",void 0),(0,r.__decorate)([(0,o.MZ)({type:String})],L.prototype,"disabledDates",void 0),(0,r.__decorate)([(0,o.MZ)({type:String})],L.prototype,"weekLabel",void 0),(0,r.__decorate)([(0,o.MZ)({type:Boolean})],L.prototype,"inline",void 0),(0,r.__decorate)([(0,o.MZ)({type:Number})],L.prototype,"dragRatio",void 0),(0,r.__decorate)([(0,o.MZ)({type:Date,attribute:!1})],L.prototype,"_selectedDate",void 0),(0,r.__decorate)([(0,o.MZ)({type:Date,attribute:!1})],L.prototype,"_focusedDate",void 0),(0,r.__decorate)([(0,o.MZ)({type:String,attribute:!1})],L.prototype,"_startView",void 0),(0,r.__decorate)([(0,o.P)(".year-list-view__full-list")],L.prototype,"_yearViewFullList",void 0),(0,r.__decorate)([(0,o.P)(".btn__year-selector")],L.prototype,"_buttonSelectorYear",void 0),(0,r.__decorate)([(0,o.P)(".year-list-view__list-item")],L.prototype,"_yearViewListItem",void 0),(0,r.__decorate)([(0,o.Ls)({passive:!0})],L.prototype,"_updateYear",null),(0,r.__decorate)([(0,o.Ls)({passive:!0})],L.prototype,"_updateFocusedDateWithKeyboard",null),n()}catch(L){n(L)}})},58981:function(e,t,a){async function n(e,t){const{hasNativeWebAnimation:a=!1,keyframes:n=[],options:r={duration:100}}=t||{};if(Array.isArray(n)&&n.length)return new Promise(t=>{if(a){e.animate(n,r).onfinish=()=>t()}else{const[,a]=n||[],i=()=>{e.removeEventListener("transitionend",i),t()};e.addEventListener("transitionend",i),e.style.transitionDuration=`${r.duration}ms`,r.easing&&(e.style.transitionTimingFunction=r.easing),Object.keys(a).forEach(t=>{t&&(e.style[t]=a[t])})}})}a.d(t,{K:()=>n})},35676:function(e,t,a){a.a(e,async function(e,n){try{a.d(t,{Y:()=>d});var r=a(13192),i=a(52588),o=a(61881),s=e([i,o]);function d({hasAltKey:e,keyCode:t,focusedDate:a,selectedDate:n,disabledDaysSet:s,disabledDatesSet:l,minTime:d,maxTime:c}){const u=a.getUTCFullYear(),h=a.getUTCMonth(),p=a.getUTCDate(),y=+a,f=n.getUTCFullYear(),m=n.getUTCMonth();let _=u,b=h,w=p,g=!0;switch((m!==h||f!==u)&&(_=f,b=m,w=1,g=34===t||33===t||35===t),g){case y===d&&i.Gf.has(t):case y===c&&i.eB.has(t):break;case 38===t:w-=7;break;case 40===t:w+=7;break;case 37===t:w-=1;break;case 39===t:w+=1;break;case 34===t:e?_+=1:b+=1;break;case 33===t:e?_-=1:b-=1;break;case 35===t:b+=1,w=0;break;default:w=1}if(34===t||33===t){const e=(0,r.m)(_,b+1,0).getUTCDate();w>e&&(w=e)}return(0,o.i)({keyCode:t,maxTime:c,minTime:d,disabledDaysSet:s,disabledDatesSet:l,focusedDate:(0,r.m)(_,b,w)})}[i,o]=s.then?(await s)():s,n()}catch(l){n(l)}})},12402:function(e,t,a){function n(e,t){window.customElements&&!window.customElements.get(e)&&window.customElements.define(e,t)}a.d(t,{U:()=>n})},82004:function(e,t,a){function n(e,t,a){return e.dispatchEvent(new CustomEvent(t,{detail:a,bubbles:!0,composed:!0}))}a.d(t,{w:()=>n})},24571:function(e,t,a){function n(e,t){return e.composedPath().find(e=>e instanceof HTMLElement&&t(e))}a.d(t,{z:()=>n})},97076:function(e,t,a){function n(e,t){return+t-+e}a.d(t,{u:()=>n})},20335:function(e,t,a){a.a(e,async function(e,n){try{a.d(t,{G:()=>l});var r=a(36886),i=a(52588),o=e([i]);function l(e){const t=(0,i.B0)(e,{timeZone:"UTC",weekday:"short",month:"short",day:"numeric"}),a=(0,i.B0)(e,{timeZone:"UTC",day:"numeric"}),n=(0,i.B0)(e,{timeZone:"UTC",year:"numeric",month:"short",day:"numeric"}),o=(0,i.B0)(e,{timeZone:"UTC",year:"numeric",month:"long"}),s=(0,i.B0)(e,{timeZone:"UTC",weekday:"long"}),l=(0,i.B0)(e,{timeZone:"UTC",weekday:"narrow"}),d=(0,i.B0)(e,{timeZone:"UTC",year:"numeric"});return{locale:e,dateFormat:(0,r.f)(t),dayFormat:(0,r.f)(a),fullDateFormat:(0,r.f)(n),longMonthYearFormat:(0,r.f)(o),longWeekdayFormat:(0,r.f)(s),narrowWeekdayFormat:(0,r.f)(l),yearFormat:(0,r.f)(d)}}i=(o.then?(await o)():o)[0],n()}catch(s){n(s)}})},86530:function(e,t,a){a.d(t,{n:()=>s});var n=a(13192);function r(e,t){const a=function(e,t){const a=t.getUTCFullYear(),r=t.getUTCMonth(),i=t.getUTCDate(),o=t.getUTCDay();let s=o;return"first-4-day-week"===e&&(s=3),"first-day-of-year"===e&&(s=6),"first-full-week"===e&&(s=0),(0,n.m)(a,r,i-o+s)}(e,t),r=(0,n.m)(a.getUTCFullYear(),0,1),i=1+(+a-+r)/864e5;return Math.ceil(i/7)}function i(e){if(e>=0&&e<7)return Math.abs(e);return((e<0?7*Math.ceil(Math.abs(e)):0)+e)%7}function o(e,t,a){const n=i(e-t);return a?1+n:n}function s(e){const{dayFormat:t,fullDateFormat:a,locale:s,longWeekdayFormat:l,narrowWeekdayFormat:d,selectedDate:c,disabledDates:u,disabledDays:h,firstDayOfWeek:p,max:y,min:f,showWeekNumber:m,weekLabel:_,weekNumberType:b}=e,w=null==f?Number.MIN_SAFE_INTEGER:+f,g=null==y?Number.MAX_SAFE_INTEGER:+y,v=function(e){const{firstDayOfWeek:t=0,showWeekNumber:a=!1,weekLabel:r,longWeekdayFormat:i,narrowWeekdayFormat:o}=e||{},s=1+(t+(t<0?7:0))%7,l=r||"Wk",d=a?[{label:"Wk"===l?"Week":l,value:l}]:[];return Array.from(Array(7)).reduce((e,t,a)=>{const r=(0,n.m)(2017,0,s+a);return e.push({label:i(r),value:o(r)}),e},d)}({longWeekdayFormat:l,narrowWeekdayFormat:d,firstDayOfWeek:p,showWeekNumber:m,weekLabel:_}),k=e=>[s,e.toJSON(),null==u?void 0:u.join("_"),null==h?void 0:h.join("_"),p,null==y?void 0:y.toJSON(),null==f?void 0:f.toJSON(),m,_,b].filter(Boolean).join(":"),D=c.getUTCFullYear(),x=c.getUTCMonth(),S=[-1,0,1].map(e=>{const l=(0,n.m)(D,x+e,1),d=+(0,n.m)(D,x+e+1,0),c=k(l);if(d<w||+l>g)return{key:c,calendar:[],disabledDatesSet:new Set,disabledDaysSet:new Set};const v=function(e){const{date:t,dayFormat:a,disabledDates:s=[],disabledDays:l=[],firstDayOfWeek:d=0,fullDateFormat:c,locale:u="en-US",max:h,min:p,showWeekNumber:y=!1,weekLabel:f="Week",weekNumberType:m="first-4-day-week"}=e||{},_=i(d),b=t.getUTCFullYear(),w=t.getUTCMonth(),g=(0,n.m)(b,w,1),v=new Set(l.map(e=>o(e,_,y))),k=new Set(s.map(e=>+e)),D=[g.toJSON(),_,u,null==h?"":h.toJSON(),null==p?"":p.toJSON(),Array.from(v).join(","),Array.from(k).join(","),m].filter(Boolean).join(":"),x=o(g.getUTCDay(),_,y),S=null==p?+new Date("2000-01-01"):+p,C=null==h?+new Date("2100-12-31"):+h,T=y?8:7,$=(0,n.m)(b,1+w,0).getUTCDate(),F=[];let M=[],U=!1,E=1;for(const i of[0,1,2,3,4,5]){for(const e of[0,1,2,3,4,5,6].concat(7===T?[]:[7])){const t=e+i*T;if(!U&&y&&0===e){const e=i<1?_:0,t=r(m,(0,n.m)(b,w,E-e)),a=`${f} ${t}`;M.push({fullDate:null,label:a,value:`${t}`,key:`${D}:${a}`,disabled:!0});continue}if(U||t<x){M.push({fullDate:null,label:"",value:"",key:`${D}:${t}`,disabled:!0});continue}const o=(0,n.m)(b,w,E),s=+o,l=v.has(e)||k.has(s)||s<S||s>C;l&&k.add(s),M.push({fullDate:o,label:c(o),value:a(o),key:`${D}:${o.toJSON()}`,disabled:l}),E+=1,E>$&&(U=!0)}F.push(M),M=[]}return{disabledDatesSet:k,calendar:F,disabledDaysSet:new Set(l.map(e=>i(e))),key:D}}({dayFormat:t,fullDateFormat:a,locale:s,disabledDates:u,disabledDays:h,firstDayOfWeek:p,max:y,min:f,showWeekNumber:m,weekLabel:_,weekNumberType:b,date:l});return{...v,key:c}}),C=[],T=new Set,$=new Set;for(const n of S){const{disabledDatesSet:e,disabledDaysSet:t,...a}=n;if(a.calendar.length>0){if(t.size>0)for(const e of t)$.add(e);if(e.size>0)for(const t of e)T.add(t)}C.push(a)}return{calendars:C,weekdays:v,disabledDatesSet:T,disabledDaysSet:$,key:k(c)}}},57445:function(e,t,a){a.d(t,{t:()=>r});var n=a(13192);function r(e){const t=null==e?new Date:new Date(e),a="string"==typeof e&&(/^\d{4}-\d{2}-\d{2}$/i.test(e)||/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}(Z|\+00:00|-00:00)$/i.test(e)),r="number"==typeof e&&e>0&&isFinite(e);let i=t.getFullYear(),o=t.getMonth(),s=t.getDate();return(a||r)&&(i=t.getUTCFullYear(),o=t.getUTCMonth(),s=t.getUTCDate()),(0,n.m)(i,o,s)}},46719:function(e,t,a){a.a(e,async function(e,n){try{a.d(t,{f:()=>s});var r=a(52588),i=e([r]);function s(){return r.B0&&(0,r.B0)().resolvedOptions&&(0,r.B0)().resolvedOptions().locale||"en-US"}r=(i.then?(await i)():i)[0],n()}catch(o){n(o)}})},61881:function(e,t,a){a.a(e,async function(e,n){try{a.d(t,{i:()=>d});var r=a(13192),i=a(52588),o=a(97076),s=e([i]);function d({keyCode:e,disabledDaysSet:t,disabledDatesSet:a,focusedDate:n,maxTime:s,minTime:l}){const d=+n;let c=d<l,u=d>s;if((0,o.u)(l,s)<864e5)return n;let h=c||u||t.has(n.getUTCDay())||a.has(d);if(!h)return n;let p=0,y=c===u?n:new Date(c?l-864e5:864e5+s);const f=y.getUTCFullYear(),m=y.getUTCMonth();let _=y.getUTCDate();for(;h;)(c||!u&&i.$g.has(e))&&(_+=1),(u||!c&&i.tn.has(e))&&(_-=1),y=(0,r.m)(f,m,_),p=+y,c||(c=p<l,c&&(y=new Date(l),p=+y,_=y.getUTCDate())),u||(u=p>s,u&&(y=new Date(s),p=+y,_=y.getUTCDate())),h=t.has(y.getUTCDay())||a.has(p);return y}i=(s.then?(await s)():s)[0],n()}catch(l){n(l)}})},47614:function(e,t,a){function n(e,t){return e.classList.contains(t)}a.d(t,{n:()=>n})},60117:function(e,t,a){function n(e,t){return!(null==e||!(t instanceof Date)||isNaN(+t))}a.d(t,{v:()=>n})},57407:function(e,t,a){function n(e){return e-Math.floor(e)>0?+e.toFixed(3):e}a.d(t,{b:()=>n})},447:function(e,t,a){function n(e){return{passive:!0,handleEvent:e}}a.d(t,{c:()=>n})},84073:function(e,t,a){function n(e,t){const a="string"==typeof e&&e.length>0?e.split(/,\s*/i):[];return a.length?"function"==typeof t?a.map(t):a:[]}a.d(t,{S:()=>n})},30622:function(e,t,a){function n(e,t){if(null==e.scrollTo){const{top:a,left:n}=t||{};e.scrollTop=a||0,e.scrollLeft=n||0}else e.scrollTo(t)}a.d(t,{G:()=>n})},49060:function(e,t,a){function n(e){if(e instanceof Date&&!isNaN(+e)){const t=e.toJSON();return null==t?"":t.replace(/^(.+)T.+/i,"$1")}return""}a.d(t,{h:()=>n})},93739:function(e,t,a){a.d(t,{N:()=>r});var n=a(97076);function r(e,t){if((0,n.u)(e,t)<864e5)return[];const a=e.getUTCFullYear();return Array.from(Array(t.getUTCFullYear()-a+1),(e,t)=>t+a)}},74745:function(e,t,a){function n(e,t,a){const n="number"==typeof e?e:+e,r=+t,i=+a;return n<r?r:n>i?i:e}a.d(t,{V:()=>n})},46977:function(e,t,a){a.d(t,{J:()=>s});var n=a(12130);function r(e){const{clientX:t,clientY:a,pageX:n,pageY:r}=e,i=Math.max(n,t),o=Math.max(r,a),s=e.identifier||e.pointerId;return{x:i,y:o,id:null==s?0:s}}function i(e,t){const a=t.changedTouches;if(null==a)return{newPointer:r(t),oldPointer:e};const n=Array.from(a,e=>r(e));return{newPointer:null==e?n[0]:n.find(t=>t.id===e.id),oldPointer:e}}function o(e,t,a){e.addEventListener(t,a,!!n.QQ&&{passive:!0})}class s{disconnect(){const e=this._element;e&&e.removeEventListener&&(e.removeEventListener("mousedown",this._down),e.removeEventListener("touchstart",this._down),e.removeEventListener("touchmove",this._move),e.removeEventListener("touchend",this._up))}_onDown(e){return t=>{t instanceof MouseEvent&&(this._element.addEventListener("mousemove",this._move),this._element.addEventListener("mouseup",this._up),this._element.addEventListener("mouseleave",this._up));const{newPointer:a}=i(this._startPointer,t);e(a,t),this._startPointer=a}}_onMove(e){return t=>{this._updatePointers(e,t)}}_onUp(e){return t=>{this._updatePointers(e,t,!0)}}_updatePointers(e,t,a){a&&t instanceof MouseEvent&&(this._element.removeEventListener("mousemove",this._move),this._element.removeEventListener("mouseup",this._up),this._element.removeEventListener("mouseleave",this._up));const{newPointer:n,oldPointer:r}=i(this._startPointer,t);e(n,r,t),this._startPointer=a?null:n}constructor(e,t){this._element=e,this._startPointer=null;const{down:a,move:n,up:r}=t;this._down=this._onDown(a),this._move=this._onMove(n),this._up=this._onUp(r),e&&e.addEventListener&&(e.addEventListener("mousedown",this._down),o(e,"touchstart",this._down),o(e,"touchmove",this._move),o(e,"touchend",this._up))}}},9395:function(e,t,a){function n(e,t){const a={waitUntilFirstUpdate:!1,...t};return(t,n)=>{const{update:r}=t,i=Array.isArray(e)?e:[e];t.update=function(e){i.forEach(t=>{const r=t;if(e.has(r)){const t=e.get(r),i=this[r];t!==i&&(a.waitUntilFirstUpdate&&!this.hasUpdated||this[n](t,i))}}),r.call(this,e)}}}a.d(t,{w:()=>n})},32510:function(e,t,a){a.d(t,{A:()=>y});var n=a(96196),r=a(77845);const i=":host {\n  box-sizing: border-box !important;\n}\n\n:host *,\n:host *::before,\n:host *::after {\n  box-sizing: inherit !important;\n}\n\n[hidden] {\n  display: none !important;\n}\n";class o extends Set{add(e){super.add(e);const t=this._existing;if(t)try{t.add(e)}catch{t.add(`--${e}`)}else this._el.setAttribute(`state-${e}`,"");return this}delete(e){super.delete(e);const t=this._existing;return t?(t.delete(e),t.delete(`--${e}`)):this._el.removeAttribute(`state-${e}`),!0}has(e){return super.has(e)}clear(){for(const e of this)this.delete(e)}constructor(e,t=null){super(),this._existing=null,this._el=e,this._existing=t}}const s=CSSStyleSheet.prototype.replaceSync;Object.defineProperty(CSSStyleSheet.prototype,"replaceSync",{value:function(e){e=e.replace(/:state\(([^)]+)\)/g,":where(:state($1), :--$1, [state-$1])"),s.call(this,e)}});var l,d=Object.defineProperty,c=Object.getOwnPropertyDescriptor,u=e=>{throw TypeError(e)},h=(e,t,a,n)=>{for(var r,i=n>1?void 0:n?c(t,a):t,o=e.length-1;o>=0;o--)(r=e[o])&&(i=(n?r(t,a,i):r(i))||i);return n&&i&&d(t,a,i),i},p=(e,t,a)=>t.has(e)||u("Cannot "+a);class y extends n.WF{static get styles(){const e=Array.isArray(this.css)?this.css:this.css?[this.css]:[];return[i,...e].map(e=>"string"==typeof e?(0,n.iz)(e):e)}attachInternals(){const e=super.attachInternals();return Object.defineProperty(e,"states",{value:new o(this,e.states)}),e}attributeChangedCallback(e,t,a){var n,r,i;p(n=this,r=l,"read from private field"),(i?i.call(n):r.get(n))||(this.constructor.elementProperties.forEach((e,t)=>{e.reflect&&null!=this[t]&&this.initialReflectedProperties.set(t,this[t])}),((e,t,a,n)=>{p(e,t,"write to private field"),n?n.call(e,a):t.set(e,a)})(this,l,!0)),super.attributeChangedCallback(e,t,a)}willUpdate(e){super.willUpdate(e),this.initialReflectedProperties.forEach((t,a)=>{e.has(a)&&null==this[a]&&(this[a]=t)})}firstUpdated(e){super.firstUpdated(e),this.didSSR&&this.shadowRoot?.querySelectorAll("slot").forEach(e=>{e.dispatchEvent(new Event("slotchange",{bubbles:!0,composed:!1,cancelable:!1}))})}update(e){try{super.update(e)}catch(t){if(this.didSSR&&!this.hasUpdated){const e=new Event("lit-hydration-error",{bubbles:!0,composed:!0,cancelable:!1});e.error=t,this.dispatchEvent(e)}throw t}}relayNativeEvent(e,t){e.stopImmediatePropagation(),this.dispatchEvent(new e.constructor(e.type,{...e,...t}))}constructor(){var e,t,a;super(),e=this,a=!1,(t=l).has(e)?u("Cannot add the same private member more than once"):t instanceof WeakSet?t.add(e):t.set(e,a),this.initialReflectedProperties=new Map,this.didSSR=n.S$||Boolean(this.shadowRoot),this.customStates={set:(e,t)=>{if(Boolean(this.internals?.states))try{t?this.internals.states.add(e):this.internals.states.delete(e)}catch(a){if(!String(a).includes("must start with '--'"))throw a;console.error("Your browser implements an outdated version of CustomStateSet. Consider using a polyfill")}},has:e=>{if(!Boolean(this.internals?.states))return!1;try{return this.internals.states.has(e)}catch{return!1}}};try{this.internals=this.attachInternals()}catch{console.error("Element internals are not supported in your browser. Consider using a polyfill")}this.customStates.set("wa-defined",!0);let r=this.constructor;for(let[n,i]of r.elementProperties)"inherit"===i.default&&void 0!==i.initial&&"string"==typeof n&&this.customStates.set(`initial-${n}-${i.initial}`,!0)}}l=new WeakMap,h([(0,r.MZ)()],y.prototype,"dir",2),h([(0,r.MZ)()],y.prototype,"lang",2),h([(0,r.MZ)({type:Boolean,reflect:!0,attribute:"did-ssr"})],y.prototype,"didSSR",2)},25594:function(e,t,a){a.a(e,async function(e,n){try{a.d(t,{A:()=>o});var r=a(38640),i=e([r]);r=(i.then?(await i)():i)[0];const s={$code:"en",$name:"English",$dir:"ltr",carousel:"Carousel",clearEntry:"Clear entry",close:"Close",copied:"Copied",copy:"Copy",currentValue:"Current value",error:"Error",goToSlide:(e,t)=>`Go to slide ${e} of ${t}`,hidePassword:"Hide password",loading:"Loading",nextSlide:"Next slide",numOptionsSelected:e=>0===e?"No options selected":1===e?"1 option selected":`${e} options selected`,pauseAnimation:"Pause animation",playAnimation:"Play animation",previousSlide:"Previous slide",progress:"Progress",remove:"Remove",resize:"Resize",scrollableRegion:"Scrollable region",scrollToEnd:"Scroll to end",scrollToStart:"Scroll to start",selectAColorFromTheScreen:"Select a color from the screen",showPassword:"Show password",slideNum:e=>`Slide ${e}`,toggleColorFormat:"Toggle color format",zoomIn:"Zoom in",zoomOut:"Zoom out"};(0,r.XC)(s);var o=s;n()}catch(s){n(s)}})},17060:function(e,t,a){a.a(e,async function(e,n){try{a.d(t,{c:()=>s});var r=a(38640),i=a(25594),o=e([r,i]);[r,i]=o.then?(await o)():o;class s extends r.c2{}(0,r.XC)(i.A),n()}catch(s){n(s)}})},38640:function(e,t,a){a.a(e,async function(e,n){try{a.d(t,{XC:()=>p,c2:()=>f});var r=a(22),i=e([r]);r=(i.then?(await i)():i)[0];const s=new Set,l=new Map;let d,c="ltr",u="en";const h="undefined"!=typeof MutationObserver&&"undefined"!=typeof document&&void 0!==document.documentElement;if(h){const m=new MutationObserver(y);c=document.documentElement.dir||"ltr",u=document.documentElement.lang||navigator.language,m.observe(document.documentElement,{attributes:!0,attributeFilter:["dir","lang"]})}function p(...e){e.map(e=>{const t=e.$code.toLowerCase();l.has(t)?l.set(t,Object.assign(Object.assign({},l.get(t)),e)):l.set(t,e),d||(d=e)}),y()}function y(){h&&(c=document.documentElement.dir||"ltr",u=document.documentElement.lang||navigator.language),[...s.keys()].map(e=>{"function"==typeof e.requestUpdate&&e.requestUpdate()})}class f{hostConnected(){s.add(this.host)}hostDisconnected(){s.delete(this.host)}dir(){return`${this.host.dir||c}`.toLowerCase()}lang(){return`${this.host.lang||u}`.toLowerCase()}getTranslationData(e){var t,a;const n=new Intl.Locale(e.replace(/_/g,"-")),r=null==n?void 0:n.language.toLowerCase(),i=null!==(a=null===(t=null==n?void 0:n.region)||void 0===t?void 0:t.toLowerCase())&&void 0!==a?a:"";return{locale:n,language:r,region:i,primary:l.get(`${r}-${i}`),secondary:l.get(r)}}exists(e,t){var a;const{primary:n,secondary:r}=this.getTranslationData(null!==(a=t.lang)&&void 0!==a?a:this.lang());return t=Object.assign({includeFallback:!1},t),!!(n&&n[e]||r&&r[e]||t.includeFallback&&d&&d[e])}term(e,...t){const{primary:a,secondary:n}=this.getTranslationData(this.lang());let r;if(a&&a[e])r=a[e];else if(n&&n[e])r=n[e];else{if(!d||!d[e])return console.error(`No translation found for: ${String(e)}`),String(e);r=d[e]}return"function"==typeof r?r(...t):r}date(e,t){return e=new Date(e),new Intl.DateTimeFormat(this.lang(),t).format(e)}number(e,t){return e=Number(e),isNaN(e)?"":new Intl.NumberFormat(this.lang(),t).format(e)}relativeTime(e,t,a){return new Intl.RelativeTimeFormat(this.lang(),a).format(e,t)}constructor(e){this.host=e,this.host.addController(this)}}n()}catch(o){n(o)}})},2045:function(e,t,a){a.d(t,{q:()=>r});let n={};function r(){return n}},74816:function(e,t,a){a.d(t,{x:()=>r});var n=a(73420);function r(e,...t){const a=n.w.bind(null,e||t.find(e=>"object"==typeof e));return t.map(a)}},9160:function(e,t,a){a.d(t,{Cg:()=>i,_P:()=>s,my:()=>n,s0:()=>o,w4:()=>r});Math.pow(10,8);const n=6048e5,r=864e5,i=6e4,o=36e5,s=Symbol.for("constructDateFrom")},73420:function(e,t,a){a.d(t,{w:()=>r});var n=a(9160);function r(e,t){return"function"==typeof e?e(t):e&&"object"==typeof e&&n._P in e?e[n._P](t):e instanceof Date?new e.constructor(t):new Date(t)}},3952:function(e,t,a){a.d(t,{m:()=>l});var n=a(83504);function r(e){const t=(0,n.a)(e),a=new Date(Date.UTC(t.getFullYear(),t.getMonth(),t.getDate(),t.getHours(),t.getMinutes(),t.getSeconds(),t.getMilliseconds()));return a.setUTCFullYear(t.getFullYear()),+e-+a}var i=a(74816),o=a(9160),s=a(35932);function l(e,t,a){const[n,l]=(0,i.x)(a?.in,e,t),d=(0,s.o)(n),c=(0,s.o)(l),u=+d-r(d),h=+c-r(c);return Math.round((u-h)/o.w4)}},35932:function(e,t,a){a.d(t,{o:()=>r});var n=a(83504);function r(e,t){const a=(0,n.a)(e,t?.in);return a.setHours(0,0,0,0),a}},52640:function(e,t,a){a.d(t,{k:()=>i});var n=a(2045),r=a(83504);function i(e,t){const a=(0,n.q)(),i=t?.weekStartsOn??t?.locale?.options?.weekStartsOn??a.weekStartsOn??a.locale?.options?.weekStartsOn??0,o=(0,r.a)(e,t?.in),s=o.getDay(),l=(s<i?7:0)+s-i;return o.setDate(o.getDate()-l),o.setHours(0,0,0,0),o}},83504:function(e,t,a){a.d(t,{a:()=>r});var n=a(73420);function r(e,t){return(0,n.w)(t||e,e)}},57378:function(e,t,a){a.d(t,{P:()=>s});var n=a(5055),r=a(42017),i=a(63937);const o=e=>(0,i.ps)(e)?e._$litType$.h:e.strings,s=(0,r.u$)(class extends r.WL{render(e){return[e]}update(e,[t]){const a=(0,i.qb)(this.it)?o(this.it):null,r=(0,i.qb)(t)?o(t):null;if(null!==a&&(null===r||a!==r)){const t=(0,i.cN)(e).pop();let r=this.et.get(a);if(void 0===r){const e=document.createDocumentFragment();r=(0,n.XX)(n.s6,e),r.setConnected(!1),this.et.set(a,r)}(0,i.mY)(r,[t]),(0,i.Dx)(r,void 0,t)}if(null!==r){if(null===a||a!==r){const t=this.et.get(r);if(void 0!==t){const a=(0,i.cN)(t).pop();(0,i.Jz)(e),(0,i.Dx)(e,void 0,a),(0,i.mY)(e,[a])}}this.it=t}else this.it=void 0;return this.render(t)}constructor(e){super(e),this.et=new WeakMap}})},4937:function(e,t,a){a.d(t,{u:()=>s});var n=a(5055),r=a(42017),i=a(63937);const o=(e,t,a)=>{const n=new Map;for(let r=t;r<=a;r++)n.set(e[r],r);return n},s=(0,r.u$)(class extends r.WL{dt(e,t,a){let n;void 0===a?a=t:void 0!==t&&(n=t);const r=[],i=[];let o=0;for(const s of e)r[o]=n?n(s,o):o,i[o]=a(s,o),o++;return{values:i,keys:r}}render(e,t,a){return this.dt(e,t,a).values}update(e,[t,a,r]){const s=(0,i.cN)(e),{values:l,keys:d}=this.dt(t,a,r);if(!Array.isArray(s))return this.ut=d,l;const c=this.ut??=[],u=[];let h,p,y=0,f=s.length-1,m=0,_=l.length-1;for(;y<=f&&m<=_;)if(null===s[y])y++;else if(null===s[f])f--;else if(c[y]===d[m])u[m]=(0,i.lx)(s[y],l[m]),y++,m++;else if(c[f]===d[_])u[_]=(0,i.lx)(s[f],l[_]),f--,_--;else if(c[y]===d[_])u[_]=(0,i.lx)(s[y],l[_]),(0,i.Dx)(e,u[_+1],s[y]),y++,_--;else if(c[f]===d[m])u[m]=(0,i.lx)(s[f],l[m]),(0,i.Dx)(e,s[y],s[f]),f--,m++;else if(void 0===h&&(h=o(d,m,_),p=o(c,y,f)),h.has(c[y]))if(h.has(c[f])){const t=p.get(d[m]),a=void 0!==t?s[t]:null;if(null===a){const t=(0,i.Dx)(e,s[y]);(0,i.lx)(t,l[m]),u[m]=t}else u[m]=(0,i.lx)(a,l[m]),(0,i.Dx)(e,s[y],a),s[t]=null;m++}else(0,i.KO)(s[f]),f--;else(0,i.KO)(s[y]),y++;for(;m<=_;){const t=(0,i.Dx)(e,u[_+1]);(0,i.lx)(t,l[m]),u[m++]=t}for(;y<=f;){const e=s[y++];null!==e&&(0,i.KO)(e)}return this.ut=d,(0,i.mY)(e,u),n.c0}constructor(e){if(super(e),e.type!==r.OA.CHILD)throw Error("repeat() can only be used in text expressions")}})},36886:function(e,t,a){function n(e){return t=>e.format(t).replace(/\u200e/gi,"")}a.d(t,{f:()=>n})},13192:function(e,t,a){function n(e,t,a){return new Date(Date.UTC(e,t,a))}a.d(t,{m:()=>n})}};
//# sourceMappingURL=4350.faf9c424035e01e6.js.map