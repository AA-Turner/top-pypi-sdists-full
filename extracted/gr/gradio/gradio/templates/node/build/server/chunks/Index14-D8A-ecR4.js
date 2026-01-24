import './async-Mo2Ia14K.js';
import { b as spread_props } from './index-D1Ptw7Az.js';
import { t as tick } from './spring-DE8vsW2o.js';
import { g, c as G, a as U } from './2-B89dC7Mi.js';
import { y } from './UploadText-Cj3NP7gm.js';
import Nt from './Gallery-BtyraTcF.js';
import { u as ul } from './FileUpload-B-cIOmot.js';
export { default as BaseExample } from './Example7-EhqFPUU1.js';
import './index5-BoOEKc6P.js';
import './dev-fallback-Bc5Ork7Y.js';
import 'path';
import 'url';
import 'fs';
import './Upload-DAOKtkC7.js';
import './BlockLabel-qrJKniS-.js';
import './Empty-DPmCPCDI.js';
import './ShareButton-BgNheG3R.js';
import './Download-CXUtRxuu.js';
import './Image2-rnCO69bR.js';
import './Play-D2fLH3is.js';
import './FullscreenButton-Dv8H9Qim.js';
import './Maximize-CwvDIx8B.js';
import './Upload2-oakrmUYI.js';
import './ModifyUpload-D9r3woqq.js';
import './DownloadLink-CHK0Lliu.js';
import './Edit-CJCte_uE.js';
import './Undo-TMAmuanl.js';
import './Video2-BcnuCSWl.js';
import './File-BPgKwfYm.js';

function J(u,h){u.component(d=>{let i;class _ extends g{async get_data(){return i&&(await i,await tick()),await super.get_data()}}const{$$slots:B,$$events:U$1,...m}=h,e=new _(m,{selected_index:null});let p=false,f=e.props.value===null?true:e.props.value.length===0;function v(a){if(!e.props.value)return;const{index:t}=a.detail;e.dispatch("delete",a.detail),e.props.value=e.props.value.filter((s,l)=>l!==t),e.dispatch("change",e.props.value);}async function c(a){return (await Promise.all(a.map(async s=>{if(s.path?.toLowerCase().endsWith(".svg")&&s.url){const r=await(await fetch(s.url)).text();return {...s,url:`data:image/svg+xml,${encodeURIComponent(r)}`}}return s}))).map(s=>s.mime_type?.includes("video")?{video:s,caption:null}:{image:s,caption:null})}let o=true,n;function w(a){G(a,{visible:e.shared.visible,variant:"solid",padding:false,elem_id:e.shared.elem_id,elem_classes:e.shared.elem_classes,container:e.shared.container,scale:e.shared.scale,min_width:e.shared.min_width,allow_overflow:false,height:typeof e.props.height=="number"?e.props.height:void 0,get fullscreen(){return p},set fullscreen(t){p=t,o=false;},children:t=>{U(t,spread_props([{autoscroll:e.shared.autoscroll,i18n:e.i18n},e.shared.loading_status,{on_clear_status:()=>e.dispatch("clear_status",e.shared.loading_status)}])),t.push("<!----> "),e.shared.interactive&&f?(t.push("<!--[-->"),ul(t,{value:null,root:e.shared.root,label:e.shared.label,max_file_size:e.shared.max_file_size,file_count:"multiple",file_types:e.props.file_types,i18n:e.i18n,upload:(...s)=>e.shared.client.upload(...s),stream_handler:(...s)=>e.shared.client.stream(...s),onupload:async s=>{const l=Array.isArray(s)?s:[s];e.props.value=await c(l),e.dispatch("upload",e.props.value),e.dispatch("change",e.props.value);},onerror:s=>{e.shared.loading_status=e.shared.loading_status||{},e.shared.loading_status.status="error",e.dispatch("error",s);},get upload_promise(){return i},set upload_promise(s){i=s,o=false;},children:s=>{y(s,{i18n:e.i18n,type:"gallery"});},$$slots:{default:true}})):(t.push("<!--[!-->"),Nt(t,{onchange:()=>e.dispatch("change"),onclear:()=>e.dispatch("change"),onselect:s=>e.dispatch("select",s),onshare:s=>e.dispatch("share",s.detail),onerror:s=>e.dispatch("error",s.detail),onpreview_open:()=>{e.dispatch("preview_open");},onpreview_close:()=>e.dispatch("preview_close"),onfullscreen:({detail:s})=>{p=s;},ondelete:v,onupload:async s=>{const l=Array.isArray(s)?s:[s],r=await c(l);e.props.value=e.props.value?[...e.props.value,...r]:r,e.dispatch("upload",r),e.dispatch("change",e.props.value);},label:e.shared.label,show_label:e.shared.show_label,columns:e.props.columns,rows:e.props.rows,height:e.props.height,preview:e.props.preview,object_fit:e.props.object_fit,interactive:e.shared.interactive,allow_preview:e.props.allow_preview,show_share_button:e.props.buttons.some(s=>typeof s=="string"&&s==="share"),show_download_button:e.props.buttons.some(s=>typeof s=="string"&&s==="download"),fit_columns:e.props.fit_columns,i18n:e.i18n,_fetch:(...s)=>e.shared.client.fetch(...s),show_fullscreen_button:e.props.buttons.some(s=>typeof s=="string"&&s==="fullscreen"),buttons:e.props.buttons,on_custom_button_click:s=>{e.dispatch("custom_button_click",{id:s});},fullscreen:p,root:e.shared.root,file_types:e.props.file_types,max_file_size:e.shared.max_file_size,upload:(...s)=>e.shared.client.upload(...s),stream_handler:(...s)=>e.shared.client.stream(...s),get selected_index(){return e.props.selected_index},set selected_index(s){e.props.selected_index=s,o=false;},get value(){return e.props.value},set value(s){e.props.value=s,o=false;}})),t.push("<!--]-->");},$$slots:{default:true}});}do o=true,n=d.copy(),w(n);while(!o);d.subsume(n);});}

export { Nt as BaseGallery, J as default };
//# sourceMappingURL=Index14-D8A-ecR4.js.map
