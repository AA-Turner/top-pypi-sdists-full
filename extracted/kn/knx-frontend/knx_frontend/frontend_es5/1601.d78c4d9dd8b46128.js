"use strict";(self.webpackChunkknx_frontend=self.webpackChunkknx_frontend||[]).push([["1601"],{67552:function(t,e,i){i.a(t,(async function(t,a){try{i.r(e),i.d(e,{HaFormOptionalActions:function(){return f}});i(39710),i(26847),i(81738),i(94814),i(6989),i(1455),i(56389),i(27530);var o=i(73742),s=i(59048),d=i(7616),n=i(28105),c=i(41806),l=i(30337),h=(i(93795),i(40830),i(91337),t([l]));l=(h.then?(await h)():h)[0];let r,p,u,m,_,b=t=>t;const y="M19,13H13V19H11V13H5V11H11V5H13V11H19V13Z",v=[];class f extends s.oi{async focus(){var t;await this.updateComplete,null===(t=this.renderRoot.querySelector("ha-form"))||void 0===t||t.focus()}updated(t){if(super.updated(t),t.has("data")){var e;const t=null!==(e=this._displayActions)&&void 0!==e?e:v,i=this._hiddenActions(this.schema.schema,t);this._displayActions=[...t,...i.filter((t=>t in this.data))]}}render(){var t,e,i;const a=null!==(t=this._displayActions)&&void 0!==t?t:v,o=this._displaySchema(this.schema.schema,null!==(e=this._displayActions)&&void 0!==e?e:[]),d=this._hiddenActions(this.schema.schema,a),n=new Map(this.computeLabel?this.schema.schema.map((t=>[t.name,t])):[]);return(0,s.dy)(r||(r=b`
      ${0}
      ${0}
    `),o.length>0?(0,s.dy)(p||(p=b`
            <ha-form
              .hass=${0}
              .data=${0}
              .schema=${0}
              .disabled=${0}
              .computeLabel=${0}
              .computeHelper=${0}
              .localizeValue=${0}
            ></ha-form>
          `),this.hass,this.data,o,this.disabled,this.computeLabel,this.computeHelper,this.localizeValue):s.Ld,d.length>0?(0,s.dy)(u||(u=b`
            <ha-button-menu
              @action=${0}
              fixed
              @closed=${0}
            >
              <ha-button slot="trigger" appearance="filled" size="small">
                <ha-svg-icon .path=${0} slot="start"></ha-svg-icon>
                ${0}
              </ha-button>
              ${0}
            </ha-button-menu>
          `),this._handleAddAction,c.U,y,(null===(i=this.localize)||void 0===i?void 0:i.call(this,"ui.components.form-optional-actions.add"))||"Add interaction",d.map((t=>{const e=n.get(t);return(0,s.dy)(m||(m=b`
                  <ha-list-item>
                    ${0}
                  </ha-list-item>
                `),this.computeLabel&&e?this.computeLabel(e):t)}))):s.Ld)}_handleAddAction(t){var e,i;const a=this._hiddenActions(this.schema.schema,null!==(e=this._displayActions)&&void 0!==e?e:v)[t.detail.index];this._displayActions=[...null!==(i=this._displayActions)&&void 0!==i?i:[],a]}constructor(...t){super(...t),this.disabled=!1,this._hiddenActions=(0,n.Z)(((t,e)=>t.map((t=>t.name)).filter((t=>!e.includes(t))))),this._displaySchema=(0,n.Z)(((t,e)=>t.filter((t=>e.includes(t.name)))))}}f.styles=(0,s.iv)(_||(_=b`
    :host {
      display: flex !important;
      flex-direction: column;
      gap: 24px;
    }
    :host ha-form {
      display: block;
    }
  `)),(0,o.__decorate)([(0,d.Cb)({attribute:!1})],f.prototype,"localize",void 0),(0,o.__decorate)([(0,d.Cb)({attribute:!1})],f.prototype,"hass",void 0),(0,o.__decorate)([(0,d.Cb)({attribute:!1})],f.prototype,"data",void 0),(0,o.__decorate)([(0,d.Cb)({attribute:!1})],f.prototype,"schema",void 0),(0,o.__decorate)([(0,d.Cb)({type:Boolean})],f.prototype,"disabled",void 0),(0,o.__decorate)([(0,d.Cb)({attribute:!1})],f.prototype,"computeLabel",void 0),(0,o.__decorate)([(0,d.Cb)({attribute:!1})],f.prototype,"computeHelper",void 0),(0,o.__decorate)([(0,d.Cb)({attribute:!1})],f.prototype,"localizeValue",void 0),(0,o.__decorate)([(0,d.SB)()],f.prototype,"_displayActions",void 0),f=(0,o.__decorate)([(0,d.Mo)("ha-form-optional_actions")],f),a()}catch(r){a(r)}}))}}]);
//# sourceMappingURL=1601.d78c4d9dd8b46128.js.map