/*! For license information please see 3249.735970c0082da9e6.js.LICENSE.txt */
export const __rspack_esm_id="3249";export const __rspack_esm_ids=["3249"];export const __webpack_modules__={76538(e,t,a){var i=a(62826),o=a(96196),s=a(97735);class r extends o.WF{render(){const e=o.qy`<div class="header-title"> <slot name="title"></slot> </div>`,t=o.qy`<div class="header-subtitle"> <slot name="subtitle"></slot> </div>`;return o.qy` <header class="header"> <div class="header-bar"> <section class="header-navigation-icon"> <slot name="navigationIcon"></slot> </section> <section class="header-content"> ${"above"===this.subtitlePosition?o.qy`${t}${e}`:o.qy`${e}${t}`} </section> <section class="header-action-items"> <slot name="actionItems"></slot> </section> </div> <slot></slot> </header> `}static get styles(){return[o.AH`:host{display:block}:host([show-border]){border-bottom:1px solid var(--mdc-dialog-scroll-divider-color,rgba(0,0,0,.12))}.header-bar{display:flex;flex-direction:row;align-items:center;padding:0 var(--ha-space-1);box-sizing:border-box}.header-content{flex:1;padding:10px var(--ha-space-1);display:flex;flex-direction:column;justify-content:center;min-height:var(--ha-space-12);min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.header-title{height:var(--ha-dialog-header-title-height,calc(var(--ha-font-size-xl) + var(--ha-space-1)));font-size:var(--ha-font-size-xl);line-height:var(--ha-line-height-condensed);font-weight:var(--ha-font-weight-medium);color:var(--ha-dialog-header-title-color,var(--primary-text-color))}.header-subtitle{font-size:var(--ha-font-size-m);line-height:var(--ha-line-height-normal);color:var(--ha-dialog-header-subtitle-color,var(--secondary-text-color))}@media all and (min-width:450px) and (min-height:500px){.header-bar{padding:0 var(--ha-space-2)}}.header-navigation-icon{flex:none;min-width:var(--ha-space-2);height:100%;display:flex;flex-direction:row}.header-action-items{flex:none;min-width:var(--ha-space-2);height:100%;display:flex;flex-direction:row}`]}constructor(...e){super(...e),this.subtitlePosition="below",this.showBorder=!1}}(0,i.Cg)([(0,s.MZ)({type:String,attribute:"subtitle-position"})],r.prototype,"subtitlePosition",void 0),(0,i.Cg)([(0,s.MZ)({type:Boolean,reflect:!0,attribute:"show-border"})],r.prototype,"showBorder",void 0),r=(0,i.Cg)([(0,s.EM)("ha-dialog-header")],r)},72554(e,t,a){a.a(e,async function(e,t){try{var i=a(62826),o=a(93900),s=a(96196),r=a(97735),l=a(32288),n=a(1087),d=a(59992),h=a(14503),c=a(22348),p=(a(76538),a(26300)),g=e([o,p]);[o,p]=g.then?(await g)():g;const u="M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z";class y extends((0,d.V)(s.WF)){get scrollableElement(){return this.bodyContainer}updated(e){super.updated(e),e.has("open")&&(this._open=this.open)}render(){return s.qy` <wa-dialog .open="${this._open}" .lightDismiss="${!this.preventScrimClose}" without-header aria-labelledby="${(0,l.J)(this.ariaLabelledBy||(void 0!==this.headerTitle?"ha-dialog-title":void 0))}" aria-describedby="${(0,l.J)(this.ariaDescribedBy)}" @keydown="${this._handleKeyDown}" @wa-hide="${this._handleHide}" @wa-show="${this._handleShow}" @wa-after-show="${this._handleAfterShow}" @wa-after-hide="${this._handleAfterHide}"> ${this.withoutHeader?s.s6:s.qy` <slot name="header"> <ha-dialog-header .subtitlePosition="${this.headerSubtitlePosition}" .showBorder="${this._bodyScrolled}"> <slot name="headerNavigationIcon" slot="navigationIcon"> <ha-icon-button data-dialog="close" .label="${this.hass?.localize("ui.common.close")??"Close"}" .path="${u}"></ha-icon-button> </slot> ${void 0!==this.headerTitle?s.qy`<span slot="title" class="title" id="ha-dialog-title"> ${this.headerTitle} </span>`:s.qy`<slot name="headerTitle" slot="title"></slot>`} ${void 0!==this.headerSubtitle?s.qy`<span slot="subtitle">${this.headerSubtitle}</span>`:s.qy`<slot name="headerSubtitle" slot="subtitle"></slot>`} <slot name="headerActionItems" slot="actionItems"></slot> </ha-dialog-header> </slot>`} <div class="content-wrapper"> <div class="body ha-scrollbar" @scroll="${this._handleBodyScroll}"> <slot></slot> </div> ${this.renderScrollableFades()} </div> <slot name="footer" slot="footer"></slot> </wa-dialog> `}disconnectedCallback(){super.disconnectedCallback(),this._open=!1}_handleBodyScroll(e){this._bodyScrolled=e.target.scrollTop>0}_handleKeyDown(e){"Escape"===e.key&&(this._escapePressed=!0,e.stopPropagation(),e.currentTarget.open=!1)}_handleHide(e){const t=e.detail?.source===e.target.dialog;this.preventScrimClose&&this._escapePressed&&t&&e.preventDefault(),this._escapePressed=!1}static get styles(){return[...super.styles,h.dp,s.AH`
        wa-dialog {
          --full-width: var(
            --ha-dialog-width-full,
            min(95vw, var(--safe-width))
          );
          --width: min(var(--ha-dialog-width-md, 580px), var(--full-width));
          --spacing: var(--dialog-content-padding, var(--ha-space-6));
          --show-duration: var(--ha-dialog-show-duration, 200ms);
          --hide-duration: var(--ha-dialog-hide-duration, 200ms);
          --ha-dialog-surface-background: var(
            --card-background-color,
            var(--ha-color-surface-default)
          );
          --wa-color-surface-raised: var(
            --ha-dialog-surface-background,
            var(--card-background-color, var(--ha-color-surface-default))
          );
          --wa-panel-border-radius: var(
            --ha-dialog-border-radius,
            var(--ha-border-radius-3xl)
          );
          max-width: var(--ha-dialog-max-width, var(--safe-width));
        }
        @media (prefers-reduced-motion: reduce) {
          wa-dialog {
            --show-duration: 0ms;
            --hide-duration: 0ms;
          }
        }

        :host([width="small"]) wa-dialog {
          --width: min(var(--ha-dialog-width-sm, 320px), var(--full-width));
        }

        :host([width="large"]) wa-dialog {
          --width: min(var(--ha-dialog-width-lg, 1024px), var(--full-width));
        }

        :host([width="full"]) wa-dialog {
          --width: var(--full-width);
        }

        wa-dialog::part(dialog) {
          color: var(--primary-text-color);
          min-width: var(--width, var(--full-width));
          max-width: var(--width, var(--full-width));
          max-height: var(
            --ha-dialog-max-height,
            calc(var(--safe-height) - var(--ha-space-20))
          );
          min-height: var(--ha-dialog-min-height);
          margin-top: var(--dialog-surface-margin-top, auto);
          /* Used to offset the dialog from the safe areas when space is limited */
          transform: translate(
            calc(
              var(--safe-area-offset-left, 0px) - var(
                  --safe-area-offset-right,
                  0px
                )
            ),
            calc(
              var(--safe-area-offset-top, 0px) - var(
                  --safe-area-offset-bottom,
                  0px
                )
            )
          );
          display: flex;
          flex-direction: column;
          overflow: hidden;
        }

        @media all and (max-width: 450px), all and (max-height: 500px) {
          :host([type="standard"]) {
            --ha-dialog-border-radius: 0;

            wa-dialog {
              /* Make the container fill the whole screen width and not the safe width */
              --full-width: var(--ha-dialog-width-full, 100vw);
              --width: var(--full-width);
            }

            wa-dialog::part(dialog) {
              /* Make the dialog fill the whole screen height and not the safe height */
              min-height: var(--ha-dialog-min-height, 100vh);
              min-height: var(--ha-dialog-min-height, 100dvh);
              max-height: var(--ha-dialog-max-height, 100vh);
              max-height: var(--ha-dialog-max-height, 100dvh);
              margin-top: 0;
              margin-bottom: 0;
              /* Use safe area as padding instead of the container size */
              padding-top: var(--safe-area-inset-top);
              padding-bottom: var(--safe-area-inset-bottom);
              padding-left: var(--safe-area-inset-left);
              padding-right: var(--safe-area-inset-right);
              /* Reset the transform to center the dialog */
              transform: none;
            }
          }
        }

        .header-title-container {
          display: flex;
          align-items: center;
        }

        .header-title {
          margin: 0;
          margin-bottom: 0;
          color: var(--ha-dialog-header-title-color, var(--primary-text-color));
          font-size: var(
            --ha-dialog-header-title-font-size,
            var(--ha-font-size-2xl)
          );
          line-height: var(
            --ha-dialog-header-title-line-height,
            var(--ha-line-height-condensed)
          );
          font-weight: var(
            --ha-dialog-header-title-font-weight,
            var(--ha-font-weight-normal)
          );
          overflow: hidden;
          text-overflow: ellipsis;
          white-space: nowrap;
          margin-right: var(--ha-space-3);
        }

        wa-dialog::part(body) {
          padding: 0;
          display: flex;
          flex-direction: column;
          max-width: 100%;
          overflow: hidden;
        }

        .content-wrapper {
          position: relative;
          flex: 1;
          display: flex;
          flex-direction: column;
          min-height: 0;
        }

        .body {
          position: var(--dialog-content-position, relative);
          padding: var(
            --dialog-content-padding,
            0 var(--ha-space-6) var(--ha-space-6) var(--ha-space-6)
          );
          overflow: auto;
          flex-grow: 1;
        }
        :host([flexcontent]) .body {
          max-width: 100%;
          flex: 1;
          display: flex;
          flex-direction: column;
        }

        wa-dialog::part(footer) {
          padding: 0;
        }

        ::slotted([slot="footer"]) {
          display: flex;
          padding: var(--ha-space-3) var(--ha-space-4) var(--ha-space-4)
            var(--ha-space-4);
          gap: var(--ha-space-3);
          justify-content: flex-end;
          align-items: center;
          width: 100%;
        }
      `]}constructor(...e){super(...e),this.open=!1,this.type="standard",this.width="medium",this.preventScrimClose=!1,this.headerSubtitlePosition="below",this.flexContent=!1,this.withoutHeader=!1,this._open=!1,this._bodyScrolled=!1,this._escapePressed=!1,this._handleShow=async()=>{this._open=!0,(0,n.r)(this,"opened"),await this.updateComplete,requestAnimationFrame(()=>{if(this.hass&&(0,c.V)(this.hass)){const e=this.querySelector("[autofocus]");return void(null!==e&&(e.id||(e.id="ha-dialog-autofocus"),this.hass?.auth.external?.fireMessage({type:"focus_element",payload:{element_id:e.id}})))}this.querySelector("[autofocus]")?.focus()})},this._handleAfterShow=()=>{(0,n.r)(this,"after-show")},this._handleAfterHide=e=>{e.eventPhase===Event.AT_TARGET&&(this._open=!1,(0,n.r)(this,"closed"))}}}(0,i.Cg)([(0,r.MZ)({attribute:!1})],y.prototype,"hass",void 0),(0,i.Cg)([(0,r.MZ)({attribute:"aria-labelledby"})],y.prototype,"ariaLabelledBy",void 0),(0,i.Cg)([(0,r.MZ)({attribute:"aria-describedby"})],y.prototype,"ariaDescribedBy",void 0),(0,i.Cg)([(0,r.MZ)({type:Boolean,reflect:!0})],y.prototype,"open",void 0),(0,i.Cg)([(0,r.MZ)({reflect:!0})],y.prototype,"type",void 0),(0,i.Cg)([(0,r.MZ)({type:String,reflect:!0,attribute:"width"})],y.prototype,"width",void 0),(0,i.Cg)([(0,r.MZ)({type:Boolean,reflect:!0,attribute:"prevent-scrim-close"})],y.prototype,"preventScrimClose",void 0),(0,i.Cg)([(0,r.MZ)({attribute:"header-title"})],y.prototype,"headerTitle",void 0),(0,i.Cg)([(0,r.MZ)({attribute:"header-subtitle"})],y.prototype,"headerSubtitle",void 0),(0,i.Cg)([(0,r.MZ)({type:String,attribute:"header-subtitle-position"})],y.prototype,"headerSubtitlePosition",void 0),(0,i.Cg)([(0,r.MZ)({type:Boolean,reflect:!0,attribute:"flexcontent"})],y.prototype,"flexContent",void 0),(0,i.Cg)([(0,r.MZ)({type:Boolean,attribute:"without-header"})],y.prototype,"withoutHeader",void 0),(0,i.Cg)([(0,r.wk)()],y.prototype,"_open",void 0),(0,i.Cg)([(0,r.P)(".body")],y.prototype,"bodyContainer",void 0),(0,i.Cg)([(0,r.wk)()],y.prototype,"_bodyScrolled",void 0),(0,i.Cg)([(0,r.Ls)({passive:!0})],y.prototype,"_handleBodyScroll",null),y=(0,i.Cg)([(0,r.EM)("ha-dialog")],y),t()}catch(e){t(e)}})},92639(e,t,a){a.a(e,async function(e,t){try{a(14603),a(47566),a(98721);var i=a(62826),o=a(96196),s=a(97735),r=a(29485),l=a(36312),n=a(1087),d=a(12587),h=a(10897),c=a(38962),p=e([c]);c=(p.then?(await p)():p)[0];class g extends o.WF{connectedCallback(){super.connectedCallback(),g.streamCount+=1,this.hasUpdated&&(this._resetError(),this._startHls()),document.addEventListener("visibilitychange",this._handleVisibilityChange)}disconnectedCallback(){super.disconnectedCallback(),document.removeEventListener("visibilitychange",this._handleVisibilityChange),g.streamCount-=1,this._cleanUp()}render(){return o.qy` ${this._error?o.qy`<ha-alert alert-type="error" class="${this._errorIsFatal?"fatal":"retry"}"> ${this._error} </ha-alert>`:""} ${this._errorIsFatal?"":o.qy`<video .poster="${this.posterUrl}" ?autoplay="${this.autoPlay}" .muted="${this.muted}" ?playsinline="${this.playsInline}" ?controls="${this.controls}" @loadeddata="${this._loadedData}" style="${(0,r.W)({height:null==this.aspectRatio?"100%":"auto",aspectRatio:this.aspectRatio,objectFit:this.fitMode})}"></video>`} `}updated(e){super.updated(e);const t=e.has("entityid"),a=e.has("url");t?this._getStreamUrlFromEntityId():a&&this.url&&(this._cleanUp(),this._resetError(),this._url=this.url,this._startHls())}async _getStreamUrlFromEntityId(){if(this._cleanUp(),this._resetError(),(0,l.x)(this.hass,"stream")){if(this.entityid)try{const{url:e}=await(0,h.wv)(this.hass,this.entityid);this._url=this.hass.hassUrl(e),this._cleanUp(),this._resetError(),this._startHls()}catch(e){console.error(e),(0,n.r)(this,"streams",{hasAudio:!1,hasVideo:!1})}}else this._setFatalError("Streaming component is not loaded.")}async _startHls(){const e=fetch(this._url),t=(await a.e("29091").then(a.bind(a,10318))).default;if(!this.isConnected)return;let i=t.isSupported();if(i||(i=""!==this._videoEl.canPlayType("application/vnd.apple.mpegurl")),!i)return void this._setFatalError(this.hass.localize("ui.components.media-browser.video_not_supported"));const o=this.allowExoPlayer&&this.hass.auth.external?.config.hasExoPlayer,s=await(await e).text();if(!this.isConnected)return;const r=/#EXT-X-STREAM-INF:.*?(?:CODECS=".*?([^.]*)?\..*?,([^.]*)?\..*?".*?)?(?:\n|\r\n)(.+)/g,l=r.exec(s),n=r.exec(s);let d;d=null!==l&&null===n?new URL(l[3],this._url).href:this._url;const h=l?`${l[1]},${l[2]}`:void 0;this._reportStreams(h),o&&(h?.includes("hevc")||h?.includes("hev1"))?this._renderHLSExoPlayer(d):t.isSupported()?this._renderHLSPolyfill(this._videoEl,t,d):this._renderHLSNative(this._videoEl,d)}async _renderHLSExoPlayer(e){this._exoPlayer=!0,window.addEventListener("resize",this._resizeExoPlayer),this.updateComplete.then(()=>(0,d.E)()).then(this._resizeExoPlayer),this._videoEl.style.visibility="hidden",await this.hass.auth.external.fireMessage({type:"exoplayer/play_hls",payload:{url:e,muted:this.muted}})}_isLLHLSSupported(){if(g.streamCount<=2)return!0;if(!("performance"in window)||0===performance.getEntriesByType("resource").length)return!1;const e=performance.getEntriesByType("resource")[0];return"nextHopProtocol"in e&&"h2"===e.nextHopProtocol}async _renderHLSPolyfill(e,t,a){const i=new t({backBufferLength:60,fragLoadingTimeOut:3e4,manifestLoadingTimeOut:3e4,levelLoadingTimeOut:3e4,maxLiveSyncPlaybackRate:2,lowLatencyMode:this._isLLHLSSupported()});this._hlsPolyfillInstance=i,i.attachMedia(e),i.on(t.Events.MEDIA_ATTACHED,()=>{this._resetError(),i.loadSource(a)}),i.on(t.Events.FRAG_LOADED,(e,t)=>{this._resetError()}),i.on(t.Events.ERROR,(e,a)=>{if(a.fatal)if(a.type===t.ErrorTypes.NETWORK_ERROR){switch(a.details){case t.ErrorDetails.MANIFEST_LOAD_ERROR:{let e="Error starting stream, see logs for details";void 0!==a.response&&void 0!==a.response.code&&(a.response.code>=500?e+=" (Server failure)":a.response.code>=400?e+=" (Stream never started)":e+=` (${a.response.code})`),this._setRetryableError(e);break}case t.ErrorDetails.MANIFEST_LOAD_TIMEOUT:this._setRetryableError("Timeout while starting stream");break;default:this._setRetryableError("Stream network error")}i.startLoad()}else a.type===t.ErrorTypes.MEDIA_ERROR?(this._setRetryableError("Error with media stream contents"),i.recoverMediaError()):this._setFatalError("Error playing stream")})}async _renderHLSNative(e,t){e.src=t,e.addEventListener("loadedmetadata",()=>{e.play()})}_cleanUp(){this._hlsPolyfillInstance&&(this._hlsPolyfillInstance.destroy(),this._hlsPolyfillInstance=void 0),this._exoPlayer&&(window.removeEventListener("resize",this._resizeExoPlayer),this.hass.auth.external.fireMessage({type:"exoplayer/stop"}),this._exoPlayer=!1),this._videoEl&&(this._videoEl.removeAttribute("src"),this._videoEl.load())}_resetError(){this._error=void 0,this._errorIsFatal=!1}_setFatalError(e){this._error=e,this._errorIsFatal=!0,(0,n.r)(this,"streams",{hasAudio:!1,hasVideo:!1})}_setRetryableError(e){this._error=e,this._errorIsFatal=!1,(0,n.r)(this,"streams",{hasAudio:!1,hasVideo:!1})}_reportStreams(e){const t=e?.split(",");(0,n.r)(this,"streams",{hasAudio:t?.includes("mp4a")??!1,hasVideo:t?.includes("mp4a")?t?.length>1:Boolean(t?.length)})}_loadedData(){(0,n.r)(this,"load")}constructor(...e){super(...e),this.controls=!1,this.muted=!1,this.autoPlay=!1,this.playsInline=!1,this.allowExoPlayer=!1,this._errorIsFatal=!1,this._exoPlayer=!1,this._handleVisibilityChange=()=>{document.pictureInPictureElement||(document.hidden?this._cleanUp():(this._resetError(),this._startHls()))},this._resizeExoPlayer=()=>{if(!this._videoEl)return;const e=this._videoEl.getBoundingClientRect();this.hass.auth.external.fireMessage({type:"exoplayer/resize",payload:{left:e.left,top:e.top,right:e.right,bottom:e.bottom}})}}}g.streamCount=0,g.styles=o.AH`:host,video{display:block}video{width:100%;max-height:var(--video-max-height,calc(100vh - 97px))}.fatal{display:block;padding:100px 16px}.retry{display:block}`,(0,i.Cg)([(0,s.MZ)({attribute:!1})],g.prototype,"hass",void 0),(0,i.Cg)([(0,s.MZ)()],g.prototype,"entityid",void 0),(0,i.Cg)([(0,s.MZ)()],g.prototype,"url",void 0),(0,i.Cg)([(0,s.MZ)({attribute:"poster-url"})],g.prototype,"posterUrl",void 0),(0,i.Cg)([(0,s.MZ)({attribute:!1})],g.prototype,"aspectRatio",void 0),(0,i.Cg)([(0,s.MZ)({attribute:!1})],g.prototype,"fitMode",void 0),(0,i.Cg)([(0,s.MZ)({type:Boolean,attribute:"controls"})],g.prototype,"controls",void 0),(0,i.Cg)([(0,s.MZ)({type:Boolean,attribute:"muted"})],g.prototype,"muted",void 0),(0,i.Cg)([(0,s.MZ)({type:Boolean,attribute:"autoplay"})],g.prototype,"autoPlay",void 0),(0,i.Cg)([(0,s.MZ)({type:Boolean,attribute:"playsinline"})],g.prototype,"playsInline",void 0),(0,i.Cg)([(0,s.MZ)({type:Boolean,attribute:"allow-exoplayer"})],g.prototype,"allowExoPlayer",void 0),(0,i.Cg)([(0,s.P)("video")],g.prototype,"_videoEl",void 0),(0,i.Cg)([(0,s.wk)()],g.prototype,"_error",void 0),(0,i.Cg)([(0,s.wk)()],g.prototype,"_errorIsFatal",void 0),(0,i.Cg)([(0,s.wk)()],g.prototype,"_url",void 0),g=(0,i.Cg)([(0,s.EM)("ha-hls-player")],g),t()}catch(e){t(e)}})},42856(e,t,a){a.a(e,async function(e,i){try{a.r(t),a.d(t,{HuiDialogWebBrowserPlayMedia:()=>p});var o=a(62826),s=a(96196),r=a(97735),l=a(1087),n=a(72554),d=a(92639),h=a(14503),c=e([n,d]);[n,d]=c.then?(await c)():c;class p extends s.WF{showDialog(e){this._params=e,this._open=!0}closeDialog(){this._open=!1}_dialogClosed(){const e=this.renderRoot.querySelector("img");e&&(e.src=""),this._params=void 0,(0,l.r)(this,"dialog-closed",{dialog:this.localName})}render(){if(!this._params||!this._params.sourceType||!this._params.sourceUrl)return s.s6;const e=this._params.sourceType.split("/",1)[0];return s.qy` <ha-dialog .hass="${this.hass}" .open="${this._open}" width="large" header-title="${this._params.title||this.hass.localize("ui.components.media-browser.media_player")}" @closed="${this._dialogClosed}"> ${"audio"===e?s.qy` <audio controls autoplay> <source src="${this._params.sourceUrl}" type="${this._params.sourceType}"> ${this.hass.localize("ui.components.media-browser.audio_not_supported")} </audio> `:"video"===e?s.qy` <video controls autoplay playsinline> <source src="${this._params.sourceUrl}" type="${this._params.sourceType}"> ${this.hass.localize("ui.components.media-browser.video_not_supported")} </video> `:"application/x-mpegURL"===this._params.sourceType?s.qy` <ha-hls-player controls autoplay playsinline .hass="${this.hass}" .url="${this._params.sourceUrl}"></ha-hls-player> `:"image"===e?s.qy`<img alt="${this._params.title||s.s6}" src="${this._params.sourceUrl}">`:s.qy`${this.hass.localize("ui.components.media-browser.media_not_supported")}`} </ha-dialog> `}static get styles(){return[h.nA,s.AH`audio,img,video{outline:0;width:100%}`]}constructor(...e){super(...e),this._open=!1}}(0,o.Cg)([(0,r.MZ)({attribute:!1})],p.prototype,"hass",void 0),(0,o.Cg)([(0,r.wk)()],p.prototype,"_params",void 0),(0,o.Cg)([(0,r.wk)()],p.prototype,"_open",void 0),p=(0,o.Cg)([(0,r.EM)("hui-dialog-web-browser-play-media")],p),i()}catch(e){i(e)}})},93900(e,t,a){a.a(e,async function(e,t){try{var i=a(96196),o=a(97735),s=a(94333),r=a(32288),l=a(17051),n=a(42462),d=a(28438),h=a(98779),c=a(27259),p=a(31247),g=a(93949),u=a(92070),y=a(9395),v=a(12754),m=a(17060),f=a(88496),w=a(91470),b=e([f,m]);[f,m]=b.then?(await b)():b;var _=Object.defineProperty,x=Object.getOwnPropertyDescriptor,E=(e,t,a,i)=>{for(var o,s=i>1?void 0:i?x(t,a):t,r=e.length-1;r>=0;r--)(o=e[r])&&(s=(i?o(t,a,s):o(s))||s);return i&&s&&_(t,a,s),s};let C=class extends v.A{firstUpdated(){this.open&&(this.addOpenListeners(),this.dialog.showModal(),(0,g.JG)(this))}disconnectedCallback(){super.disconnectedCallback(),(0,g.I7)(this),this.removeOpenListeners()}async requestClose(e){const t=new d.L({source:e});if(this.dispatchEvent(t),t.defaultPrevented)return this.open=!0,void(0,c.Ud)(this.dialog,"pulse");this.removeOpenListeners(),await(0,c.Ud)(this.dialog,"hide"),this.open=!1,this.dialog.close(),(0,g.I7)(this);const a=this.originalTrigger;"function"==typeof a?.focus&&setTimeout(()=>a.focus()),this.dispatchEvent(new l.Z)}addOpenListeners(){document.addEventListener("keydown",this.handleDocumentKeyDown)}removeOpenListeners(){document.removeEventListener("keydown",this.handleDocumentKeyDown)}handleDialogCancel(e){e.preventDefault(),this.dialog.classList.contains("hide")||e.target!==this.dialog||this.requestClose(this.dialog)}handleDialogClick(e){const t=e.target.closest('[data-dialog="close"]');t&&(e.stopPropagation(),this.requestClose(t))}async handleDialogPointerDown(e){e.target===this.dialog&&(this.lightDismiss?this.requestClose(this.dialog):await(0,c.Ud)(this.dialog,"pulse"))}handleOpenChange(){this.open&&!this.dialog.open?this.show():!this.open&&this.dialog.open&&(this.open=!0,this.requestClose(this.dialog))}async show(){const e=new h.k;this.dispatchEvent(e),e.defaultPrevented?this.open=!1:(this.addOpenListeners(),this.originalTrigger=document.activeElement,this.open=!0,this.dialog.showModal(),(0,g.JG)(this),requestAnimationFrame(()=>{const e=this.querySelector("[autofocus]");e&&"function"==typeof e.focus?e.focus():this.dialog.focus()}),await(0,c.Ud)(this.dialog,"show"),this.dispatchEvent(new n.q))}render(){const e=!this.withoutHeader,t=this.hasSlotController.test("footer");return i.qy` <dialog aria-labelledby="${this.ariaLabelledby??"title"}" aria-describedby="${(0,r.J)(this.ariaDescribedby)}" part="dialog" class="${(0,s.H)({dialog:!0,open:this.open})}" @cancel="${this.handleDialogCancel}" @click="${this.handleDialogClick}" @pointerdown="${this.handleDialogPointerDown}"> ${e?i.qy` <header part="header" class="header"> <h2 part="title" class="title" id="title"> <slot name="label"> ${this.label.length>0?this.label:String.fromCharCode(8203)} </slot> </h2> <div part="header-actions" class="header-actions"> <slot name="header-actions"></slot> <wa-button part="close-button" exportparts="base:close-button__base" class="close" appearance="plain" @click="${e=>this.requestClose(e.target)}"> <wa-icon name="xmark" label="${this.localize.term("close")}" library="system" variant="solid"></wa-icon> </wa-button> </div> </header> `:""} <div part="body" class="body"><slot></slot></div> ${t?i.qy` <footer part="footer" class="footer"> <slot name="footer"></slot> </footer> `:""} </dialog> `}constructor(){super(...arguments),this.localize=new m.c(this),this.hasSlotController=new u.X(this,"footer","header-actions","label"),this.open=!1,this.label="",this.withoutHeader=!1,this.lightDismiss=!1,this.handleDocumentKeyDown=e=>{"Escape"===e.key&&this.open&&(e.preventDefault(),e.stopPropagation(),this.requestClose(this.dialog))}}};C.css=w.A,E([(0,o.P)(".dialog")],C.prototype,"dialog",2),E([(0,o.MZ)({type:Boolean,reflect:!0})],C.prototype,"open",2),E([(0,o.MZ)({reflect:!0})],C.prototype,"label",2),E([(0,o.MZ)({attribute:"without-header",type:Boolean,reflect:!0})],C.prototype,"withoutHeader",2),E([(0,o.MZ)({attribute:"light-dismiss",type:Boolean})],C.prototype,"lightDismiss",2),E([(0,o.MZ)({attribute:"aria-labelledby"})],C.prototype,"ariaLabelledby",2),E([(0,o.MZ)({attribute:"aria-describedby"})],C.prototype,"ariaDescribedby",2),E([(0,y.w)("open",{waitUntilFirstUpdate:!0})],C.prototype,"handleOpenChange",1),C=E([(0,o.EM)("wa-dialog")],C),document.addEventListener("click",e=>{const t=e.target.closest("[data-dialog]");if(t instanceof Element){const[e,a]=(0,p.v)(t.getAttribute("data-dialog")||"");if("open"===e&&a?.length){const e=t.getRootNode().getElementById(a);"wa-dialog"===e?.localName?e.open=!0:console.warn(`A dialog with an ID of "${a}" could not be found in this document.`)}}}),i.S$||document.addEventListener("pointerdown",()=>{}),t()}catch(e){t(e)}})},91470(e,t,a){a.d(t,{A:()=>i});var i=a(96196).AH`:host{--width:31rem;--spacing:var(--wa-space-l);--show-duration:200ms;--hide-duration:200ms;display:none}:host([open]){display:block}.dialog{display:flex;flex-direction:column;top:0;right:0;bottom:0;left:0;width:var(--width);max-width:calc(100% - var(--wa-space-2xl));max-height:calc(100% - var(--wa-space-2xl));background-color:var(--wa-color-surface-raised);border-radius:var(--wa-panel-border-radius);border:none;box-shadow:var(--wa-shadow-l);padding:0;margin:auto}.dialog.show{animation:show-dialog var(--show-duration) ease}.dialog.show::backdrop{animation:show-backdrop var(--show-duration,200ms) ease}.dialog.hide{animation:show-dialog var(--hide-duration) ease reverse}.dialog.hide::backdrop{animation:show-backdrop var(--hide-duration,200ms) ease reverse}.dialog.pulse{animation:pulse 250ms ease}.dialog:focus{outline:0}@media screen and (max-width:420px){.dialog{max-height:80vh}}.open{display:flex;opacity:1}.header{flex:0 0 auto;display:flex;flex-wrap:nowrap;padding-inline-start:var(--spacing);padding-block-end:0;padding-inline-end:calc(var(--spacing) - var(--wa-form-control-padding-block));padding-block-start:calc(var(--spacing) - var(--wa-form-control-padding-block))}.title{align-self:center;flex:1 1 auto;font-family:inherit;font-size:var(--wa-font-size-l);font-weight:var(--wa-font-weight-heading);line-height:var(--wa-line-height-condensed);margin:0}.header-actions{align-self:start;display:flex;flex-shrink:0;flex-wrap:wrap;justify-content:end;gap:var(--wa-space-2xs);padding-inline-start:var(--spacing)}.header-actions ::slotted(wa-button),.header-actions wa-button{flex:0 0 auto;display:flex;align-items:center}.body{flex:1 1 auto;display:block;padding:var(--spacing);overflow:auto;-webkit-overflow-scrolling:touch}.body:focus{outline:0}.body:focus-visible{outline:var(--wa-focus-ring);outline-offset:var(--wa-focus-ring-offset)}.footer{flex:0 0 auto;display:flex;flex-wrap:wrap;gap:var(--wa-space-xs);justify-content:end;padding:var(--spacing);padding-block-start:0}.footer ::slotted(wa-button:not(:first-of-type)){margin-inline-start:var(--wa-spacing-xs)}.dialog::backdrop{background-color:var(--wa-color-overlay-modal,rgb(0 0 0 / .25))}@keyframes pulse{0%{scale:1}50%{scale:1.02}100%{scale:1}}@keyframes show-dialog{from{opacity:0;scale:0.8}to{opacity:1;scale:1}}@keyframes show-backdrop{from{opacity:0}to{opacity:1}}@media (forced-colors:active){.dialog{border:solid 1px #fff}}`}};
//# sourceMappingURL=3249.735970c0082da9e6.js.map