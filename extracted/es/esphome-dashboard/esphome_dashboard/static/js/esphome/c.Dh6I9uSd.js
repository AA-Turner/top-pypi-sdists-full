import{_ as e,e as o,t as s,n as t,s as i,x as n,a3 as a}from"./index-CZy-fyXs.js";import"./c.wXqWYNVx.js";import"./c.0EIqk-ip.js";let r=class extends i{render(){return n`
      <esphome-process-dialog
        always-show-close
        .heading=${`Rename ${this.configuration}`}
        .type=${"rename"}
        .spawnParams=${{configuration:this.configuration,newName:`${this.newName}`}}
        @closed=${this._handleClose}
        @process-done=${this._handleProcessDone}
      >
        ${void 0===this._result||0===this._result?"":n`
              <mwc-button
                slot="secondaryAction"
                dialogAction="close"
                label="Retry"
                @click=${this._handleRetry}
              ></mwc-button>
            `}
      </esphome-process-dialog>
    `}_handleProcessDone(e){this._result=e.detail}_handleRetry(){a(this.configuration,this.newName)}_handleClose(){this.parentNode.removeChild(this)}};e([o()],r.prototype,"configuration",void 0),e([o()],r.prototype,"newName",void 0),e([s()],r.prototype,"_result",void 0),r=e([t("esphome-rename-process-dialog")],r);
//# sourceMappingURL=c.Dh6I9uSd.js.map
