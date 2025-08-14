import{H as o,r as t,b as e,c as s,k as i,n as r,s as a,x as n}from"./index-DsQ6s3QV.js";import"./c.B_BeI3Fi.js";import{o as l,a as c}from"./c.XHbs4ilG.js";import"./c.DyhSc74d.js";import"./c.C7W_QUPQ.js";import"./c.BhBMbg7A.js";import"./c.dS8MQso4.js";import"./c.CilBUOZp.js";import"./c.Bfw8PfUM.js";let p=class extends a{constructor(){super(...arguments),this.downloadFactoryFirmware=!0}render(){return n`
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
    `],e([s()],p.prototype,"configuration",void 0),e([s()],p.prototype,"platformSupportsWebSerial",void 0),e([s()],p.prototype,"downloadFactoryFirmware",void 0),e([i()],p.prototype,"_result",void 0),p=e([r("esphome-compile-dialog")],p);
//# sourceMappingURL=c.ZSczBHkm.js.map
