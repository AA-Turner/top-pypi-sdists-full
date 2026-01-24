import{D as o,_ as t,e as s,t as e,n as i,s as r,x as n,G as a}from"./index-k-0Bmjyg.js";import"./c.9Q3Mj6jC.js";import{o as l}from"./c.DEY7aO34.js";import"./c.BrUPbrSm.js";import"./c.DGUWn8xJ.js";import"./c.BN-eppHo.js";let c=class extends r{render(){return n`
      <esphome-process-dialog
        always-show-close
        .heading=${`Logs ${this.configuration}`}
        .type=${"logs"}
        .spawnParams=${{configuration:this.configuration,port:this.target}}
        @closed=${this._handleClose}
        @process-done=${this._handleProcessDone}
      >
        <mwc-button
          slot="secondaryAction"
          dialogAction="close"
          label="Edit"
          @click=${this._openEdit}
        ></mwc-button>
        ${void 0===this._result||0===this._result?"":n`
              <mwc-button
                slot="secondaryAction"
                dialogAction="close"
                label="Retry"
                @click=${this._handleRetry}
              ></mwc-button>
            `}
      </esphome-process-dialog>
    `}_openEdit(){a(this.configuration)}_handleProcessDone(o){this._result=o.detail}_handleRetry(){l(this.configuration,this.target)}_handleClose(){this.parentNode.removeChild(this)}};c.styles=[o],t([s()],c.prototype,"configuration",void 0),t([s()],c.prototype,"target",void 0),t([e()],c.prototype,"_result",void 0),c=t([i("esphome-logs-dialog")],c);
//# sourceMappingURL=c.DMhIay9X.js.map
