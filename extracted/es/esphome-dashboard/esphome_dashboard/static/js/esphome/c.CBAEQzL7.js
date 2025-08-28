import{H as o,I as t,r as e,b as i,c as s,k as a,n as r,s as n,x as d,a4 as l,a5 as c}from"./index-aHi_iQYn.js";import"./c.DSo6oV4_.js";import"./c.DoYGBRi3.js";import{m as p}from"./c.MOzmpKvf.js";import"./c.C0yDzxzE.js";import"./c.B_bHDSZS.js";import"./c.BN8Quohf.js";import"./c.B25lovCM.js";let m=class extends n{render(){let o,t;return o="What version do you want to download?",t=d`
      ${this._error?d`<div class="error">${this._error}</div>`:""}
      ${this._downloadTypes?d`
            ${this._downloadTypes.map((o=>d`
                <mwc-list-item
                  twoline
                  hasMeta
                  dialogAction="close"
                  @click=${()=>this._handleDownload(o)}
                >
                  <span>${o.title}</span>
                  <span slot="secondary">${o.description}</span>
                  ${p}
                </mwc-list-item>
              `))}
          `:d`<div>Checking files to download...</div>`}
    `,d`
      <mwc-dialog open heading=${"What version do you want to download?"} scrimClickAction>
        ${t}
        ${this.platformSupportsWebSerial?d`
              <a
                href="https://web.esphome.io"
                target="_blank"
                rel="noopener noreferrer"
                class="bottom-left"
                >Open ESPHome Web</a
              >
            `:""}

        <mwc-button
          no-attention
          slot="primaryAction"
          dialogAction="close"
          label="Cancel"
        ></mwc-button>
      </mwc-dialog>
    `}firstUpdated(o){super.firstUpdated(o),l(this.configuration).then((o=>{if(1==o.length)return this._handleDownload(o[0]),void this._close();this._downloadTypes=o})).catch((o=>{this._error=o.message||o}))}_handleDownload(o){const t=document.createElement("a");t.download=o.download,t.href=c(this.configuration,o),document.body.appendChild(t),t.click(),t.remove()}_close(){this.shadowRoot.querySelector("mwc-dialog").close()}};m.styles=[o,t,e`
      mwc-list-item {
        margin: 0 -20px;
      }
    `],i([s()],m.prototype,"configuration",void 0),i([s()],m.prototype,"platformSupportsWebSerial",void 0),i([a()],m.prototype,"_error",void 0),i([a()],m.prototype,"_downloadTypes",void 0),m=i([r("esphome-download-type-dialog")],m);
//# sourceMappingURL=c.CBAEQzL7.js.map
