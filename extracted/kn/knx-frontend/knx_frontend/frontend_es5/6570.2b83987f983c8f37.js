"use strict";(self.webpackChunkknx_frontend=self.webpackChunkknx_frontend||[]).push([["6570"],{72199:function(t,a,i){i.a(t,(async function(t,e){try{i.r(a),i.d(a,{HaImagecropperDialog:function(){return y}});i(26847),i(64455),i(6202),i(27530),i(41465),i(34845),i(73249),i(36330),i(38221),i(75863);var o=i(73742),r=i(27007),s=i.n(r),p=i(93528),c=i(59048),n=i(7616),h=i(31733),l=(i(99298),i(30337)),_=i(77204),d=t([l]);l=(d.then?(await d)():d)[0];let u,m,g,v=t=>t;class y extends c.oi{showDialog(t){this._params=t,this._open=!0}closeDialog(){var t;this._open=!1,this._params=void 0,null===(t=this._cropper)||void 0===t||t.destroy(),this._cropper=void 0,this._isTargetAspectRatio=!1}updated(t){t.has("_params")&&this._params&&(this._cropper?this._cropper.replace(URL.createObjectURL(this._params.file)):(this._image.src=URL.createObjectURL(this._params.file),this._cropper=new(s())(this._image,{aspectRatio:this._params.options.aspectRatio,viewMode:1,dragMode:"move",minCropBoxWidth:50,ready:()=>{this._isTargetAspectRatio=this._checkMatchAspectRatio(),URL.revokeObjectURL(this._image.src)}})))}_checkMatchAspectRatio(){var t;const a=null===(t=this._params)||void 0===t?void 0:t.options.aspectRatio;if(!a)return!0;const i=this._cropper.getImageData();if(i.aspectRatio===a)return!0;if(i.naturalWidth>i.naturalHeight){const t=i.naturalWidth/a;return Math.abs(t-i.naturalHeight)<=1}const e=i.naturalHeight*a;return Math.abs(e-i.naturalWidth)<=1}render(){var t;return(0,c.dy)(u||(u=v`<ha-dialog
      @closed=${0}
      scrimClickAction
      escapeKeyAction
      .open=${0}
    >
      <div
        class="container ${0}"
      >
        <img alt=${0} />
      </div>
      <ha-button
        appearance="plain"
        slot="primaryAction"
        @click=${0}
      >
        ${0}
      </ha-button>
      ${0}

      <ha-button slot="primaryAction" @click=${0}>
        ${0}
      </ha-button>
    </ha-dialog>`),this.closeDialog,this._open,(0,h.$)({round:Boolean(null===(t=this._params)||void 0===t?void 0:t.options.round)}),this.hass.localize("ui.dialogs.image_cropper.crop_image"),this.closeDialog,this.hass.localize("ui.common.cancel"),this._isTargetAspectRatio?(0,c.dy)(m||(m=v`<ha-button
            appearance="plain"
            slot="primaryAction"
            @click=${0}
          >
            ${0}
          </ha-button>`),this._useOriginal,this.hass.localize("ui.dialogs.image_cropper.use_original")):c.Ld,this._cropImage,this.hass.localize("ui.dialogs.image_cropper.crop"))}_cropImage(){this._cropper.getCroppedCanvas().toBlob((t=>{if(!t)return;const a=new File([t],this._params.file.name,{type:this._params.options.type||this._params.file.type});this._params.croppedCallback(a),this.closeDialog()}),this._params.options.type||this._params.file.type,this._params.options.quality)}_useOriginal(){this._params.croppedCallback(this._params.file),this.closeDialog()}static get styles(){return[_.yu,(0,c.iv)(g||(g=v`
        ${0}
        .container {
          max-width: 640px;
        }
        img {
          max-width: 100%;
        }
        .container.round .cropper-view-box,
        .container.round .cropper-face {
          border-radius: 50%;
        }
        .cropper-line,
        .cropper-point,
        .cropper-point.point-se::before {
          background-color: var(--primary-color);
        }
      `),(0,c.$m)(p))]}constructor(...t){super(...t),this._open=!1}}(0,o.__decorate)([(0,n.Cb)({attribute:!1})],y.prototype,"hass",void 0),(0,o.__decorate)([(0,n.SB)()],y.prototype,"_params",void 0),(0,o.__decorate)([(0,n.SB)()],y.prototype,"_open",void 0),(0,o.__decorate)([(0,n.IO)("img",!0)],y.prototype,"_image",void 0),(0,o.__decorate)([(0,n.SB)()],y.prototype,"_isTargetAspectRatio",void 0),y=(0,o.__decorate)([(0,n.Mo)("image-cropper-dialog")],y),e()}catch(u){e(u)}}))}}]);
//# sourceMappingURL=6570.2b83987f983c8f37.js.map