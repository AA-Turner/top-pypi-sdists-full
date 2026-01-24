import{D as t,r as o,_ as e,e as s,t as i,n,s as r,x as a,G as l}from"./index-k-0Bmjyg.js";import"./c.9Q3Mj6jC.js";import{o as c}from"./c.CHBCN0fJ.js";import"./c.BrUPbrSm.js";let h=class extends r{render(){return a`
      <esphome-process-dialog
        .heading=${`Install ${this.configuration}`}
        .type=${"run"}
        .spawnParams=${{configuration:this.configuration,port:this.target}}
        @closed=${this._handleClose}
        @process-done=${this._handleProcessDone}
      >
        ${"OTA"===this.target?"":a`
              <a
                href="https://esphome.io/guides/faq.html#i-can-t-get-flashing-over-usb-to-work"
                slot="secondaryAction"
                target="_blank"
                >❓</a
              >
            `}
        <mwc-button
          slot="secondaryAction"
          dialogAction="close"
          label="Edit"
          @click=${this._openEdit}
        ></mwc-button>
        ${void 0===this._result||0===this._result?"":a`
              <mwc-button
                slot="secondaryAction"
                dialogAction="close"
                label="Retry"
                @click=${this._handleRetry}
              ></mwc-button>
            `}
      </esphome-process-dialog>
    `}_openEdit(){l(this.configuration)}_handleProcessDone(t){this._result=t.detail}_handleRetry(){c(this.configuration,this.target)}_handleClose(){this.parentNode.removeChild(this)}};h.styles=[t,o`
      a[slot="secondaryAction"] {
        text-decoration: none;
        line-height: 32px;
      }
    `],e([s()],h.prototype,"configuration",void 0),e([s()],h.prototype,"target",void 0),e([i()],h.prototype,"_result",void 0),h=e([n("esphome-install-server-dialog")],h);
//# sourceMappingURL=c.BXJ5CnAy.js.map
