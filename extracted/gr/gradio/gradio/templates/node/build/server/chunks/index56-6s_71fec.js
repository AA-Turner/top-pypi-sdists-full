import { f as fallback, e as escape_html } from './async-Mo2Ia14K.js';
import { c as bind_props, i as slot, b as spread_props } from './index-D1Ptw7Az.js';
import { c as createEventDispatcher, t as tick } from './spring-DE8vsW2o.js';
import { e as ee } from './Upload2-oakrmUYI.js';
import { g, c as G, a as U } from './2-B89dC7Mi.js';
import { k } from './BlockLabel-qrJKniS-.js';
import { r } from './Video-DAthbxcF.js';
import { k as k$1 } from './SelectSource-0bGNnJ-5.js';
import { $ } from './Webcam2-DM3IfvNU.js';
import { P as Lt, p as Kt, V as Tt } from './VideoPreview-DvvBit-H.js';
export { l as loaded, a as playable } from './VideoPreview-DvvBit-H.js';
export { default as BaseExample } from './Example28-WErkdcJM.js';
import { y } from './UploadText-Cj3NP7gm.js';
import './index5-BoOEKc6P.js';
import './dev-fallback-Bc5Ork7Y.js';
import 'path';
import 'url';
import 'fs';
import './Microphone-C7JgPGGY.js';
import './Upload-DAOKtkC7.js';
import './StreamingBar-DcBNpjjC.js';
import './DownloadLink-CHK0Lliu.js';
import './Empty-DPmCPCDI.js';
import './ShareButton-BgNheG3R.js';
import './Download-CXUtRxuu.js';
import './Maximize-CwvDIx8B.js';
import './VolumeLevels-BjhSlQIz.js';
import './Play-D2fLH3is.js';
import './Undo-TMAmuanl.js';
import './Video2-BcnuCSWl.js';
import './ModifyUpload-D9r3woqq.js';
import './Edit-CJCte_uE.js';

function R(k$2,s$1){k$2.component(v=>{let u=fallback(s$1.value,null),x=fallback(s$1.subtitle,null),g=fallback(s$1.sources,()=>["webcam","upload"],true),c=fallback(s$1.label,void 0),w=fallback(s$1.show_download_button,false),a=fallback(s$1.show_label,true),r$1=s$1.webcam_options,m=s$1.include_audio,f=s$1.autoplay,b=s$1.root,p=s$1.i18n,n=fallback(s$1.active_source,"webcam"),y=fallback(s$1.handle_reset_value,()=>{}),d=fallback(s$1.max_file_size,null),o=s$1.upload,e=s$1.stream_handler,P=s$1.loop,z=fallback(s$1.uploading,false),B=fallback(s$1.upload_promise,null),V=fallback(s$1.playback_position,0),U=false;const _=createEventDispatcher();function D(l){u=l;}function G(){u=null;}function L(l){U=true;}let S=false;let h=true,I;function T(l){k(l,{show_label:a,Icon:r,label:c||"Video"}),l.push('<!----> <div data-testid="video" class="video-container svelte-ey25pz">'),u===null||u?.url===void 0?(l.push("<!--[-->"),l.push('<div class="upload-container svelte-ey25pz">'),n==="upload"?(l.push("<!--[-->"),ee(l,{filetype:"video/x-m4v,video/*",onload:D,max_file_size:d,onerror:i=>_("error",i),root:b,upload:o,stream_handler:e,aria_label:p("video.drop_to_upload"),get upload_promise(){return B},set upload_promise(i){B=i,h=false;},get dragging(){return S},set dragging(i){S=i,h=false;},get uploading(){return z},set uploading(i){z=i,h=false;},children:i=>{i.push("<!--[-->"),slot(i,s$1,"default",{},null),i.push("<!--]-->");},$$slots:{default:true}})):(l.push("<!--[!-->"),n==="webcam"?(l.push("<!--[-->"),$(l,{root:b,mirror_webcam:r$1.mirror,webcam_constraints:r$1.constraints,include_audio:m,mode:"video",i18n:p,upload:o,stream_every:1})):l.push("<!--[!-->"),l.push("<!--]-->")),l.push("<!--]--></div>")):(l.push("<!--[!-->"),u?.url?(l.push("<!--[-->"),l.push("<!---->"),Lt(l,{upload:o,root:b,interactive:true,autoplay:f,src:u.url,subtitle:x?.url,is_stream:false,mirror:r$1.mirror&&n==="webcam",label:c,handle_change:L,handle_reset_value:y,loop:P,value:u,i18n:p,show_download_button:w,handle_clear:G,has_change_history:U,get playback_position(){return V},set playback_position(i){V=i,h=false;}}),l.push("<!---->")):(l.push("<!--[!-->"),u.size?(l.push("<!--[-->"),l.push(`<div class="file-name svelte-ey25pz">${escape_html(u.orig_name||u.url)}</div> <div class="file-size svelte-ey25pz">${escape_html(Kt(u.size))}</div>`)):l.push("<!--[!-->"),l.push("<!--]-->")),l.push("<!--]-->")),l.push("<!--]--> "),k$1(l,{sources:g,handle_clear:G,get active_source(){return n},set active_source(i){n=i,h=false;}}),l.push("<!----></div>");}do h=true,I=v.copy(),T(I);while(!h);v.subsume(I),bind_props(s$1,{value:u,subtitle:x,sources:g,label:c,show_download_button:w,show_label:a,webcam_options:r$1,include_audio:m,autoplay:f,root:b,i18n:p,active_source:n,handle_reset_value:y,max_file_size:d,upload:o,stream_handler:e,loop:P,uploading:z,upload_promise:B,playback_position:V});});}function ga(k,s$1){k.component(v=>{const{$$slots:u,$$events:x,...g$1}=s$1;let c;class w extends g{async get_data(){return c&&(await c,await tick()),await super.get_data()}}const a=new w(g$1);a.props.value;let r=false,m=a.props.sources?a.props.sources[0]:void 0,f=a.props.value;const b=()=>{f===null||a.props.value===f||(a.props.value=f);};let p=true,n;function y$1(d){a.shared.interactive?(d.push("<!--[!-->"),G(d,{visible:a.shared.visible,variant:a.props.value===null&&m==="upload"?"dashed":"solid",border_mode:"base",padding:false,elem_id:a.shared.elem_id,elem_classes:a.shared.elem_classes,height:a.props.height||void 0,width:a.props.width,container:a.shared.container,scale:a.shared.scale,min_width:a.shared.min_width,allow_overflow:false,children:o=>{U(o,spread_props([{autoscroll:a.shared.autoscroll,i18n:a.i18n},a.shared.loading_status,{on_clear_status:()=>a.dispatch("clear_status",a.shared.loading_status)}])),o.push("<!----> "),R(o,{value:a.props.value,subtitle:a.props.subtitles,label:a.shared.label,show_label:a.shared.show_label,buttons:a.props.buttons??["download","share"],on_custom_button_click:e=>{a.dispatch("custom_button_click",{id:e});},sources:a.props.sources,active_source:m,webcam_options:a.props.webcam_options,include_audio:a.props.include_audio,autoplay:a.props.autoplay,root:a.shared.root,loop:a.props.loop,handle_reset_value:b,i18n:a.i18n,max_file_size:a.shared.max_file_size,upload:(...e)=>a.shared.client.upload(...e),stream_handler:(...e)=>a.shared.client.stream(...e),get upload_promise(){return c},set upload_promise(e){c=e,p=false;},get uploading(){return r},set uploading(e){r=e,p=false;},get playback_position(){return a.props.playback_position},set playback_position(e){a.props.playback_position=e,p=false;},children:e=>{y(e,{i18n:a.i18n,type:"video"});},$$slots:{default:true}}),o.push("<!---->");},$$slots:{default:true}})):(d.push("<!--[-->"),G(d,{visible:a.shared.visible,variant:a.props.value===null&&m==="upload"?"dashed":"solid",border_mode:"base",padding:false,elem_id:a.shared.elem_id,elem_classes:a.shared.elem_classes,height:a.props.height||void 0,width:a.props.width,container:a.shared.container,scale:a.shared.scale,min_width:a.shared.min_width,allow_overflow:false,children:o=>{U(o,spread_props([{autoscroll:a.shared.autoscroll,i18n:a.i18n},a.shared.loading_status,{on_clear_status:()=>a.dispatch("clear_status",a.shared.loading_status)}])),o.push("<!----> "),Tt(o,{value:a.props.value,subtitle:a.props.subtitles,label:a.shared.label,show_label:a.shared.show_label,autoplay:a.props.autoplay,loop:a.props.loop,buttons:a.props.buttons??["download","share"],on_custom_button_click:e=>{a.dispatch("custom_button_click",{id:e});},i18n:a.i18n,upload:(...e)=>a.shared.client.upload(...e),get playback_position(){return a.props.playback_position},set playback_position(e){a.props.playback_position=e,p=false;}}),o.push("<!---->");},$$slots:{default:true}})),d.push("<!--]-->");}do p=true,n=v.copy(),y$1(n);while(!p);v.subsume(n);});}

export { R as BaseInteractiveVideo, Lt as BasePlayer, Tt as BaseStaticVideo, ga as default, Kt as prettyBytes };
//# sourceMappingURL=index56-6s_71fec.js.map
