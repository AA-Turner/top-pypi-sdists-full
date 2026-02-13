import{D as o,r as t,_ as e,e as i,t as s,n as r,s as a,x as n}from"./index-CKXJf0jG.js";import"./c.BYxqlRZA.js";import{o as l,a as c}from"./c.obYWUynn.js";import"./c.CiCOf1P7.js";import"./c.BwIzS7IS.js";import"./c.buSEAcjq.js";import"./c.Co4m-0gF.js";import"./c.C1exYqSD.js";let p=class extends a{constructor(){super(...arguments),this.downloadFactoryFirmware=!0}render(){return n`
      <esphome-process-dialog
        .heading=${`Download ${this.configuration}`}
        .type=${"compile"}
        .spawnParams=${{configuration:this.configuration}}
        @closed=${this._handleClose}
        @process-done=${this._handleProcessDone}
      >
        ${void 0===this._result?"":0===this._result?n`
                <mwc-button
                  slot="secondaryAction"
                  label="Download"
                  @click=${this._handleDownload}
                ></mwc-button>
              `:n`
                <mwc-button
                  slot="secondaryAction"
                  dialogAction="close"
                  label="Retry"
                  @click=${this._handleRetry}
                ></mwc-button>
              `}
      </esphome-process-dialog>
    `}_handleProcessDone(o){this._result=o.detail,0===o.detail&&l(this.configuration,this.platformSupportsWebSerial)}_handleDownload(){l(this.configuration,this.platformSupportsWebSerial)}_handleRetry(){c(this.configuration,this.platformSupportsWebSerial)}_handleClose(){this.parentNode.removeChild(this)}};p.styles=[o,t`
      a {
        text-decoration: none;
      }
    `],e([i()],p.prototype,"configuration",void 0),e([i()],p.prototype,"platformSupportsWebSerial",void 0),e([i()],p.prototype,"downloadFactoryFirmware",void 0),e([s()],p.prototype,"_result",void 0),p=e([r("esphome-compile-dialog")],p);
//# sourceMappingURL=c.CCdbUBo_.js.map
