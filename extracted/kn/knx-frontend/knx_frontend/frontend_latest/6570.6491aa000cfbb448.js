export const __webpack_ids__=["6570"];export const __webpack_modules__={72199:function(t,a,i){i.a(t,(async function(t,e){try{i.r(a),i.d(a,{HaImagecropperDialog:()=>m});var o=i(73742),r=i(27007),s=i.n(r),p=i(93528),c=i(59048),n=i(7616),h=i(31733),_=(i(99298),i(30337)),l=i(77204),d=t([_]);_=(d.then?(await d)():d)[0];class m extends c.oi{showDialog(t){this._params=t,this._open=!0}closeDialog(){this._open=!1,this._params=void 0,this._cropper?.destroy(),this._cropper=void 0,this._isTargetAspectRatio=!1}updated(t){t.has("_params")&&this._params&&(this._cropper?this._cropper.replace(URL.createObjectURL(this._params.file)):(this._image.src=URL.createObjectURL(this._params.file),this._cropper=new(s())(this._image,{aspectRatio:this._params.options.aspectRatio,viewMode:1,dragMode:"move",minCropBoxWidth:50,ready:()=>{this._isTargetAspectRatio=this._checkMatchAspectRatio(),URL.revokeObjectURL(this._image.src)}})))}_checkMatchAspectRatio(){const t=this._params?.options.aspectRatio;if(!t)return!0;const a=this._cropper.getImageData();if(a.aspectRatio===t)return!0;if(a.naturalWidth>a.naturalHeight){const i=a.naturalWidth/t;return Math.abs(i-a.naturalHeight)<=1}const i=a.naturalHeight*t;return Math.abs(i-a.naturalWidth)<=1}render(){return c.dy`<ha-dialog
      @closed=${this.closeDialog}
      scrimClickAction
      escapeKeyAction
      .open=${this._open}
    >
      <div
        class="container ${(0,h.$)({round:Boolean(this._params?.options.round)})}"
      >
        <img alt=${this.hass.localize("ui.dialogs.image_cropper.crop_image")} />
      </div>
      <ha-button
        appearance="plain"
        slot="primaryAction"
        @click=${this.closeDialog}
      >
        ${this.hass.localize("ui.common.cancel")}
      </ha-button>
      ${this._isTargetAspectRatio?c.dy`<ha-button
            appearance="plain"
            slot="primaryAction"
            @click=${this._useOriginal}
          >
            ${this.hass.localize("ui.dialogs.image_cropper.use_original")}
          </ha-button>`:c.Ld}

      <ha-button slot="primaryAction" @click=${this._cropImage}>
        ${this.hass.localize("ui.dialogs.image_cropper.crop")}
      </ha-button>
    </ha-dialog>`}_cropImage(){this._cropper.getCroppedCanvas().toBlob((t=>{if(!t)return;const a=new File([t],this._params.file.name,{type:this._params.options.type||this._params.file.type});this._params.croppedCallback(a),this.closeDialog()}),this._params.options.type||this._params.file.type,this._params.options.quality)}_useOriginal(){this._params.croppedCallback(this._params.file),this.closeDialog()}static get styles(){return[l.yu,c.iv`
        ${(0,c.$m)(p)}
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
      `]}constructor(...t){super(...t),this._open=!1}}(0,o.__decorate)([(0,n.Cb)({attribute:!1})],m.prototype,"hass",void 0),(0,o.__decorate)([(0,n.SB)()],m.prototype,"_params",void 0),(0,o.__decorate)([(0,n.SB)()],m.prototype,"_open",void 0),(0,o.__decorate)([(0,n.IO)("img",!0)],m.prototype,"_image",void 0),(0,o.__decorate)([(0,n.SB)()],m.prototype,"_isTargetAspectRatio",void 0),m=(0,o.__decorate)([(0,n.Mo)("image-cropper-dialog")],m),e()}catch(m){e(m)}}))}};
//# sourceMappingURL=6570.6491aa000cfbb448.js.map