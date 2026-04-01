var S0=Object.defineProperty;var T0=(tt,rt,Ut)=>rt in tt?S0(tt,rt,{enumerable:!0,configurable:!0,writable:!0,value:Ut}):tt[rt]=Ut;var Af=(tt,rt,Ut)=>T0(tt,typeof rt!="symbol"?rt+"":rt,Ut);(function(){"use strict";/*!
 * ONNX Runtime Web v1.24.3
 * Copyright (c) Microsoft Corporation. All rights reserved.
 * Licensed under the MIT License.
 */var tt=Object.defineProperty,rt=Object.getOwnPropertyDescriptor,Ut=Object.getOwnPropertyNames,Bf=Object.prototype.hasOwnProperty,Mf=(e=>typeof require<"u"?require:typeof Proxy<"u"?new Proxy(e,{get:(t,r)=>(typeof require<"u"?require:t)[r]}):e)(function(e){if(typeof require<"u")return require.apply(this,arguments);throw Error('Dynamic require of "'+e+'" is not supported')}),q=(e,t)=>()=>(e&&(t=e(e=0)),t),Pt=(e,t)=>{for(var r in t)tt(e,r,{get:t[r],enumerable:!0})},Nf=(e,t,r,i)=>{if(t&&typeof t=="object"||typeof t=="function")for(let a of Ut(t))!Bf.call(e,a)&&a!==r&&tt(e,a,{get:()=>t[a],enumerable:!(i=rt(t,a))||i.enumerable});return e},jt=e=>Nf(tt({},"__esModule",{value:!0}),e),Kt,ut,qt,mn,gn,yn=q(()=>{Kt=new Map,ut=[],qt=(e,t,r)=>{if(t&&typeof t.init=="function"&&typeof t.createInferenceSessionHandler=="function"){let i=Kt.get(e);if(i===void 0)Kt.set(e,{backend:t,priority:r});else{if(i.priority>r)return;if(i.priority===r&&i.backend!==t)throw new Error(`cannot register backend "${e}" using priority ${r}`)}if(r>=0){let a=ut.indexOf(e);a!==-1&&ut.splice(a,1);for(let n=0;n<ut.length;n++)if(Kt.get(ut[n]).priority<=r){ut.splice(n,0,e);return}ut.push(e)}return}throw new TypeError("not a valid backend")},mn=async e=>{let t=Kt.get(e);if(!t)return"backend not found.";if(t.initialized)return t.backend;if(t.aborted)return t.error;{let r=!!t.initPromise;try{return r||(t.initPromise=t.backend.init(e)),await t.initPromise,t.initialized=!0,t.backend}catch(i){return r||(t.error=`${i}`,t.aborted=!0),t.error}finally{delete t.initPromise}}},gn=async e=>{let t=e.executionProviders||[],r=t.map(l=>typeof l=="string"?l:l.name),i=r.length===0?ut:r,a,n=[],s=new Set;for(let l of i){let p=await mn(l);typeof p=="string"?n.push({name:l,err:p}):(a||(a=p),a===p&&s.add(l))}if(!a)throw new Error(`no available backend found. ERR: ${n.map(l=>`[${l.name}] ${l.err}`).join(", ")}`);for(let{name:l,err:p}of n)r.includes(l)&&console.warn(`removing requested execution provider "${l}" from session options because it is not available: ${p}`);let u=t.filter(l=>s.has(typeof l=="string"?l:l.name));return[a,new Proxy(e,{get:(l,p)=>p==="executionProviders"?u:Reflect.get(l,p)})]}}),Df=q(()=>{yn()}),_n,Uf=q(()=>{_n="1.24.3"}),ni,ke,wn=q(()=>{Uf(),ni="warning",ke={wasm:{},webgl:{},webgpu:{},versions:{common:_n},set logLevel(e){if(e!==void 0){if(typeof e!="string"||["verbose","info","warning","error","fatal"].indexOf(e)===-1)throw new Error(`Unsupported logging level: ${e}`);ni=e}},get logLevel(){return ni}},Object.defineProperty(ke,"logLevel",{enumerable:!0})}),ye,Pf=q(()=>{wn(),ye=ke}),bn,$n,qf=q(()=>{bn=(e,t)=>{let r=typeof document<"u"?document.createElement("canvas"):new OffscreenCanvas(1,1);r.width=e.dims[3],r.height=e.dims[2];let i=r.getContext("2d");if(i!=null){let a,n;(t==null?void 0:t.tensorLayout)!==void 0&&t.tensorLayout==="NHWC"?(a=e.dims[2],n=e.dims[3]):(a=e.dims[3],n=e.dims[2]);let s=(t==null?void 0:t.format)!==void 0?t.format:"RGB",u=t==null?void 0:t.norm,l,p;u===void 0||u.mean===void 0?l=[255,255,255,255]:typeof u.mean=="number"?l=[u.mean,u.mean,u.mean,u.mean]:(l=[u.mean[0],u.mean[1],u.mean[2],0],u.mean[3]!==void 0&&(l[3]=u.mean[3])),u===void 0||u.bias===void 0?p=[0,0,0,0]:typeof u.bias=="number"?p=[u.bias,u.bias,u.bias,u.bias]:(p=[u.bias[0],u.bias[1],u.bias[2],0],u.bias[3]!==void 0&&(p[3]=u.bias[3]));let h=n*a,f=0,g=h,y=h*2,_=-1;s==="RGBA"?(f=0,g=h,y=h*2,_=h*3):s==="RGB"?(f=0,g=h,y=h*2):s==="RBG"&&(f=0,y=h,g=h*2);for(let w=0;w<n;w++)for(let S=0;S<a;S++){let x=(e.data[f++]-p[0])*l[0],b=(e.data[g++]-p[1])*l[1],I=(e.data[y++]-p[2])*l[2],k=_===-1?255:(e.data[_++]-p[3])*l[3];i.fillStyle="rgba("+x+","+b+","+I+","+k+")",i.fillRect(S,w,1,1)}if("toDataURL"in r)return r.toDataURL();throw new Error("toDataURL is not supported")}else throw new Error("Can not access image data")},$n=(e,t)=>{let r=typeof document<"u"?document.createElement("canvas").getContext("2d"):new OffscreenCanvas(1,1).getContext("2d"),i;if(r!=null){let a,n,s;(t==null?void 0:t.tensorLayout)!==void 0&&t.tensorLayout==="NHWC"?(a=e.dims[2],n=e.dims[1],s=e.dims[3]):(a=e.dims[3],n=e.dims[2],s=e.dims[1]);let u=t!==void 0&&t.format!==void 0?t.format:"RGB",l=t==null?void 0:t.norm,p,h;l===void 0||l.mean===void 0?p=[255,255,255,255]:typeof l.mean=="number"?p=[l.mean,l.mean,l.mean,l.mean]:(p=[l.mean[0],l.mean[1],l.mean[2],255],l.mean[3]!==void 0&&(p[3]=l.mean[3])),l===void 0||l.bias===void 0?h=[0,0,0,0]:typeof l.bias=="number"?h=[l.bias,l.bias,l.bias,l.bias]:(h=[l.bias[0],l.bias[1],l.bias[2],0],l.bias[3]!==void 0&&(h[3]=l.bias[3]));let f=n*a;if(t!==void 0&&(t.format!==void 0&&s===4&&t.format!=="RGBA"||s===3&&t.format!=="RGB"&&t.format!=="BGR"))throw new Error("Tensor format doesn't match input tensor dims");let g=4,y=0,_=1,w=2,S=3,x=0,b=f,I=f*2,k=-1;u==="RGBA"?(x=0,b=f,I=f*2,k=f*3):u==="RGB"?(x=0,b=f,I=f*2):u==="RBG"&&(x=0,I=f,b=f*2),i=r.createImageData(a,n);for(let E=0;E<n*a;y+=g,_+=g,w+=g,S+=g,E++)i.data[y]=(e.data[x++]-h[0])*p[0],i.data[_]=(e.data[b++]-h[1])*p[1],i.data[w]=(e.data[I++]-h[2])*p[2],i.data[S]=k===-1?255:(e.data[k++]-h[3])*p[3]}else throw new Error("Can not access image data");return i}}),_r,vn,xn,Sn,Tn,kn,Lf=q(()=>{oi(),_r=(e,t)=>{if(e===void 0)throw new Error("Image buffer must be defined");if(t.height===void 0||t.width===void 0)throw new Error("Image height and width must be defined");if(t.tensorLayout==="NHWC")throw new Error("NHWC Tensor layout is not supported yet");let{height:r,width:i}=t,a=t.norm??{mean:255,bias:0},n,s;typeof a.mean=="number"?n=[a.mean,a.mean,a.mean,a.mean]:n=[a.mean[0],a.mean[1],a.mean[2],a.mean[3]??255],typeof a.bias=="number"?s=[a.bias,a.bias,a.bias,a.bias]:s=[a.bias[0],a.bias[1],a.bias[2],a.bias[3]??0];let u=t.format!==void 0?t.format:"RGBA",l=t.tensorFormat!==void 0&&t.tensorFormat!==void 0?t.tensorFormat:"RGB",p=r*i,h=l==="RGBA"?new Float32Array(p*4):new Float32Array(p*3),f=4,g=0,y=1,_=2,w=3,S=0,x=p,b=p*2,I=-1;u==="RGB"&&(f=3,g=0,y=1,_=2,w=-1),l==="RGBA"?I=p*3:l==="RBG"?(S=0,b=p,x=p*2):l==="BGR"&&(b=0,x=p,S=p*2);for(let k=0;k<p;k++,g+=f,_+=f,y+=f,w+=f)h[S++]=(e[g]+s[0])/n[0],h[x++]=(e[y]+s[1])/n[1],h[b++]=(e[_]+s[2])/n[2],I!==-1&&w!==-1&&(h[I++]=(e[w]+s[3])/n[3]);return l==="RGBA"?new Be("float32",h,[1,4,r,i]):new Be("float32",h,[1,3,r,i])},vn=async(e,t)=>{let r=typeof HTMLImageElement<"u"&&e instanceof HTMLImageElement,i=typeof ImageData<"u"&&e instanceof ImageData,a=typeof ImageBitmap<"u"&&e instanceof ImageBitmap,n=typeof e=="string",s,u=t??{},l=()=>{if(typeof document<"u")return document.createElement("canvas");if(typeof OffscreenCanvas<"u")return new OffscreenCanvas(1,1);throw new Error("Canvas is not supported")},p=h=>typeof HTMLCanvasElement<"u"&&h instanceof HTMLCanvasElement||h instanceof OffscreenCanvas?h.getContext("2d"):null;if(r){let h=l();h.width=e.width,h.height=e.height;let f=p(h);if(f!=null){let g=e.height,y=e.width;if(t!==void 0&&t.resizedHeight!==void 0&&t.resizedWidth!==void 0&&(g=t.resizedHeight,y=t.resizedWidth),t!==void 0){if(u=t,t.tensorFormat!==void 0)throw new Error("Image input config format must be RGBA for HTMLImageElement");u.tensorFormat="RGBA",u.height=g,u.width=y}else u.tensorFormat="RGBA",u.height=g,u.width=y;f.drawImage(e,0,0),s=f.getImageData(0,0,y,g).data}else throw new Error("Can not access image data")}else if(i){let h,f;if(t!==void 0&&t.resizedWidth!==void 0&&t.resizedHeight!==void 0?(h=t.resizedHeight,f=t.resizedWidth):(h=e.height,f=e.width),t!==void 0&&(u=t),u.format="RGBA",u.height=h,u.width=f,t!==void 0){let g=l();g.width=f,g.height=h;let y=p(g);if(y!=null)y.putImageData(e,0,0),s=y.getImageData(0,0,f,h).data;else throw new Error("Can not access image data")}else s=e.data}else if(a){if(t===void 0)throw new Error("Please provide image config with format for Imagebitmap");let h=l();h.width=e.width,h.height=e.height;let f=p(h);if(f!=null){let g=e.height,y=e.width;return f.drawImage(e,0,0,y,g),s=f.getImageData(0,0,y,g).data,u.height=g,u.width=y,_r(s,u)}else throw new Error("Can not access image data")}else{if(n)return new Promise((h,f)=>{let g=l(),y=p(g);if(!e||!y)return f();let _=new Image;_.crossOrigin="Anonymous",_.src=e,_.onload=()=>{g.width=_.width,g.height=_.height,y.drawImage(_,0,0,g.width,g.height);let w=y.getImageData(0,0,g.width,g.height);u.height=g.height,u.width=g.width,h(_r(w.data,u))}});throw new Error("Input data provided is not supported - aborted tensor creation")}if(s!==void 0)return _r(s,u);throw new Error("Input data provided is not supported - aborted tensor creation")},xn=(e,t)=>{let{width:r,height:i,download:a,dispose:n}=t,s=[1,i,r,4];return new Be({location:"texture",type:"float32",texture:e,dims:s,download:a,dispose:n})},Sn=(e,t)=>{let{dataType:r,dims:i,download:a,dispose:n}=t;return new Be({location:"gpu-buffer",type:r??"float32",gpuBuffer:e,dims:i,download:a,dispose:n})},Tn=(e,t)=>{let{dataType:r,dims:i,download:a,dispose:n}=t;return new Be({location:"ml-tensor",type:r??"float32",mlTensor:e,dims:i,download:a,dispose:n})},kn=(e,t,r)=>new Be({location:"cpu-pinned",type:e,data:t,dims:r??[t.length]})}),$t,Qt,si,In,Wf=q(()=>{$t=new Map([["float32",Float32Array],["uint8",Uint8Array],["int8",Int8Array],["uint16",Uint16Array],["int16",Int16Array],["int32",Int32Array],["bool",Uint8Array],["float64",Float64Array],["uint32",Uint32Array],["int4",Uint8Array],["uint4",Uint8Array]]),Qt=new Map([[Float32Array,"float32"],[Uint8Array,"uint8"],[Int8Array,"int8"],[Uint16Array,"uint16"],[Int16Array,"int16"],[Int32Array,"int32"],[Float64Array,"float64"],[Uint32Array,"uint32"]]),si=!1,In=()=>{if(!si){si=!0;let e=typeof BigInt64Array<"u"&&BigInt64Array.from,t=typeof BigUint64Array<"u"&&BigUint64Array.from,r=globalThis.Float16Array,i=typeof r<"u"&&r.from;e&&($t.set("int64",BigInt64Array),Qt.set(BigInt64Array,"int64")),t&&($t.set("uint64",BigUint64Array),Qt.set(BigUint64Array,"uint64")),i?($t.set("float16",r),Qt.set(r,"float16")):$t.set("float16",Uint16Array)}}}),En,zn,Vf=q(()=>{oi(),En=e=>{let t=1;for(let r=0;r<e.length;r++){let i=e[r];if(typeof i!="number"||!Number.isSafeInteger(i))throw new TypeError(`dims[${r}] must be an integer, got: ${i}`);if(i<0)throw new RangeError(`dims[${r}] must be a non-negative integer, got: ${i}`);t*=i}return t},zn=(e,t)=>{switch(e.location){case"cpu":return new Be(e.type,e.data,t);case"cpu-pinned":return new Be({location:"cpu-pinned",data:e.data,type:e.type,dims:t});case"texture":return new Be({location:"texture",texture:e.texture,type:e.type,dims:t});case"gpu-buffer":return new Be({location:"gpu-buffer",gpuBuffer:e.gpuBuffer,type:e.type,dims:t});case"ml-tensor":return new Be({location:"ml-tensor",mlTensor:e.mlTensor,type:e.type,dims:t});default:throw new Error(`tensorReshape: tensor location ${e.location} is not supported`)}}}),Be,oi=q(()=>{qf(),Lf(),Wf(),Vf(),Be=class{constructor(e,t,r){In();let i,a;if(typeof e=="object"&&"location"in e)switch(this.dataLocation=e.location,i=e.type,a=e.dims,e.location){case"cpu-pinned":{let s=$t.get(i);if(!s)throw new TypeError(`unsupported type "${i}" to create tensor from pinned buffer`);if(!(e.data instanceof s))throw new TypeError(`buffer should be of type ${s.name}`);this.cpuData=e.data;break}case"texture":{if(i!=="float32")throw new TypeError(`unsupported type "${i}" to create tensor from texture`);this.gpuTextureData=e.texture,this.downloader=e.download,this.disposer=e.dispose;break}case"gpu-buffer":{if(i!=="float32"&&i!=="float16"&&i!=="int32"&&i!=="int64"&&i!=="uint32"&&i!=="uint8"&&i!=="bool"&&i!=="uint4"&&i!=="int4")throw new TypeError(`unsupported type "${i}" to create tensor from gpu buffer`);this.gpuBufferData=e.gpuBuffer,this.downloader=e.download,this.disposer=e.dispose;break}case"ml-tensor":{if(i!=="float32"&&i!=="float16"&&i!=="int32"&&i!=="int64"&&i!=="uint32"&&i!=="uint64"&&i!=="int8"&&i!=="uint8"&&i!=="bool"&&i!=="uint4"&&i!=="int4")throw new TypeError(`unsupported type "${i}" to create tensor from MLTensor`);this.mlTensorData=e.mlTensor,this.downloader=e.download,this.disposer=e.dispose;break}default:throw new Error(`Tensor constructor: unsupported location '${this.dataLocation}'`)}else{let s,u;if(typeof e=="string")if(i=e,u=r,e==="string"){if(!Array.isArray(t))throw new TypeError("A string tensor's data must be a string array.");s=t}else{let l=$t.get(e);if(l===void 0)throw new TypeError(`Unsupported tensor type: ${e}.`);if(Array.isArray(t)){if(e==="float16"&&l===Uint16Array||e==="uint4"||e==="int4")throw new TypeError(`Creating a ${e} tensor from number array is not supported. Please use ${l.name} as data.`);e==="uint64"||e==="int64"?s=l.from(t,BigInt):s=l.from(t)}else if(t instanceof l)s=t;else if(t instanceof Uint8ClampedArray)if(e==="uint8")s=Uint8Array.from(t);else throw new TypeError("A Uint8ClampedArray tensor's data must be type of uint8");else if(e==="float16"&&t instanceof Uint16Array&&l!==Uint16Array)s=new globalThis.Float16Array(t.buffer,t.byteOffset,t.length);else throw new TypeError(`A ${i} tensor's data must be type of ${l}`)}else if(u=t,Array.isArray(e)){if(e.length===0)throw new TypeError("Tensor type cannot be inferred from an empty array.");let l=typeof e[0];if(l==="string")i="string",s=e;else if(l==="boolean")i="bool",s=Uint8Array.from(e);else throw new TypeError(`Invalid element type of data array: ${l}.`)}else if(e instanceof Uint8ClampedArray)i="uint8",s=Uint8Array.from(e);else{let l=Qt.get(e.constructor);if(l===void 0)throw new TypeError(`Unsupported type for tensor data: ${e.constructor}.`);i=l,s=e}if(u===void 0)u=[s.length];else if(!Array.isArray(u))throw new TypeError("A tensor's dims must be a number array");a=u,this.cpuData=s,this.dataLocation="cpu"}let n=En(a);if(this.cpuData&&n!==this.cpuData.length&&!((i==="uint4"||i==="int4")&&Math.ceil(n/2)===this.cpuData.length))throw new Error(`Tensor's size(${n}) does not match data length(${this.cpuData.length}).`);this.type=i,this.dims=a,this.size=n}static async fromImage(e,t){return vn(e,t)}static fromTexture(e,t){return xn(e,t)}static fromGpuBuffer(e,t){return Sn(e,t)}static fromMLTensor(e,t){return Tn(e,t)}static fromPinnedBuffer(e,t,r){return kn(e,t,r)}toDataURL(e){return bn(this,e)}toImageData(e){return $n(this,e)}get data(){if(this.ensureValid(),!this.cpuData)throw new Error("The data is not on CPU. Use `getData()` to download GPU data to CPU, or use `texture` or `gpuBuffer` property to access the GPU data directly.");return this.cpuData}get location(){return this.dataLocation}get texture(){if(this.ensureValid(),!this.gpuTextureData)throw new Error("The data is not stored as a WebGL texture.");return this.gpuTextureData}get gpuBuffer(){if(this.ensureValid(),!this.gpuBufferData)throw new Error("The data is not stored as a WebGPU buffer.");return this.gpuBufferData}get mlTensor(){if(this.ensureValid(),!this.mlTensorData)throw new Error("The data is not stored as a WebNN MLTensor.");return this.mlTensorData}async getData(e){switch(this.ensureValid(),this.dataLocation){case"cpu":case"cpu-pinned":return this.data;case"texture":case"gpu-buffer":case"ml-tensor":{if(!this.downloader)throw new Error("The current tensor is not created with a specified data downloader.");if(this.isDownloading)throw new Error("The current tensor is being downloaded.");try{this.isDownloading=!0;let t=await this.downloader();return this.downloader=void 0,this.dataLocation="cpu",this.cpuData=t,e&&this.disposer&&(this.disposer(),this.disposer=void 0),t}finally{this.isDownloading=!1}}default:throw new Error(`cannot get data from location: ${this.dataLocation}`)}}dispose(){if(this.isDownloading)throw new Error("The current tensor is being downloaded.");this.disposer&&(this.disposer(),this.disposer=void 0),this.cpuData=void 0,this.gpuTextureData=void 0,this.gpuBufferData=void 0,this.mlTensorData=void 0,this.downloader=void 0,this.isDownloading=void 0,this.dataLocation="none"}ensureValid(){if(this.dataLocation==="none")throw new Error("The tensor is disposed.")}reshape(e){if(this.ensureValid(),this.downloader||this.disposer)throw new Error("Cannot reshape a tensor that owns GPU resource.");return zn(this,e)}}}),Ce,Cn=q(()=>{oi(),Ce=Be}),wr,ui,Qe,Le,vt,xt,An=q(()=>{wn(),wr=(e,t)=>{(typeof ke.trace>"u"?!ke.wasm.trace:!ke.trace)||console.timeStamp(`${e}::ORT::${t}`)},ui=(e,t)=>{var a;let r=((a=new Error().stack)==null?void 0:a.split(/\r\n|\r|\n/g))||[],i=!1;for(let n=0;n<r.length;n++){if(i&&!r[n].includes("TRACE_FUNC")){let s=`FUNC_${e}::${r[n].trim().split(" ")[1]}`;t&&(s+=`::${t}`),wr("CPU",s);return}r[n].includes("TRACE_FUNC")&&(i=!0)}},Qe=e=>{(typeof ke.trace>"u"?!ke.wasm.trace:!ke.trace)||ui("BEGIN",e)},Le=e=>{(typeof ke.trace>"u"?!ke.wasm.trace:!ke.trace)||ui("END",e)},vt=e=>{(typeof ke.trace>"u"?!ke.wasm.trace:!ke.trace)||console.time(`ORT::${e}`)},xt=e=>{(typeof ke.trace>"u"?!ke.wasm.trace:!ke.trace)||console.timeEnd(`ORT::${e}`)}}),On,Gf=q(()=>{yn(),Cn(),An(),On=class Of{constructor(t){this.handler=t}async run(t,r,i){Qe(),vt("InferenceSession.run");let a={},n={};if(typeof t!="object"||t===null||t instanceof Ce||Array.isArray(t))throw new TypeError("'feeds' must be an object that use input names as keys and OnnxValue as corresponding values.");let s=!0;if(typeof r=="object"){if(r===null)throw new TypeError("Unexpected argument[1]: cannot be null.");if(r instanceof Ce)throw new TypeError("'fetches' cannot be a Tensor");if(Array.isArray(r)){if(r.length===0)throw new TypeError("'fetches' cannot be an empty array.");s=!1;for(let p of r){if(typeof p!="string")throw new TypeError("'fetches' must be a string array or an object.");if(this.outputNames.indexOf(p)===-1)throw new RangeError(`'fetches' contains invalid output name: ${p}.`);a[p]=null}if(typeof i=="object"&&i!==null)n=i;else if(typeof i<"u")throw new TypeError("'options' must be an object.")}else{let p=!1,h=Object.getOwnPropertyNames(r);for(let f of this.outputNames)if(h.indexOf(f)!==-1){let g=r[f];(g===null||g instanceof Ce)&&(p=!0,s=!1,a[f]=g)}if(p){if(typeof i=="object"&&i!==null)n=i;else if(typeof i<"u")throw new TypeError("'options' must be an object.")}else n=r}}else if(typeof r<"u")throw new TypeError("Unexpected argument[1]: must be 'fetches' or 'options'.");for(let p of this.inputNames)if(typeof t[p]>"u")throw new Error(`input '${p}' is missing in 'feeds'.`);if(s)for(let p of this.outputNames)a[p]=null;let u=await this.handler.run(t,a,n),l={};for(let p in u)if(Object.hasOwnProperty.call(u,p)){let h=u[p];h instanceof Ce?l[p]=h:l[p]=new Ce(h.type,h.data,h.dims)}return xt("InferenceSession.run"),Le(),l}async release(){return this.handler.dispose()}static async create(t,r,i,a){Qe(),vt("InferenceSession.create");let n,s={};if(typeof t=="string"){if(n=t,typeof r=="object"&&r!==null)s=r;else if(typeof r<"u")throw new TypeError("'options' must be an object.")}else if(t instanceof Uint8Array){if(n=t,typeof r=="object"&&r!==null)s=r;else if(typeof r<"u")throw new TypeError("'options' must be an object.")}else if(t instanceof ArrayBuffer||typeof SharedArrayBuffer<"u"&&t instanceof SharedArrayBuffer){let h=t,f=0,g=t.byteLength;if(typeof r=="object"&&r!==null)s=r;else if(typeof r=="number"){if(f=r,!Number.isSafeInteger(f))throw new RangeError("'byteOffset' must be an integer.");if(f<0||f>=h.byteLength)throw new RangeError(`'byteOffset' is out of range [0, ${h.byteLength}).`);if(g=t.byteLength-f,typeof i=="number"){if(g=i,!Number.isSafeInteger(g))throw new RangeError("'byteLength' must be an integer.");if(g<=0||f+g>h.byteLength)throw new RangeError(`'byteLength' is out of range (0, ${h.byteLength-f}].`);if(typeof a=="object"&&a!==null)s=a;else if(typeof a<"u")throw new TypeError("'options' must be an object.")}else if(typeof i<"u")throw new TypeError("'byteLength' must be a number.")}else if(typeof r<"u")throw new TypeError("'options' must be an object.");n=new Uint8Array(h,f,g)}else throw new TypeError("Unexpected argument[0]: must be 'path' or 'buffer'.");let[u,l]=await gn(s),p=await u.createInferenceSessionHandler(n,l);return xt("InferenceSession.create"),Le(),new Of(p)}startProfiling(){this.handler.startProfiling()}endProfiling(){this.handler.endProfiling()}get inputNames(){return this.handler.inputNames}get outputNames(){return this.handler.outputNames}get inputMetadata(){return this.handler.inputMetadata}get outputMetadata(){return this.handler.outputMetadata}}}),br,Hf=q(()=>{Gf(),br=On}),Ff=q(()=>{}),jf=q(()=>{}),Kf=q(()=>{}),Qf=q(()=>{}),Zf={};Pt(Zf,{InferenceSession:()=>br,TRACE:()=>wr,TRACE_EVENT_BEGIN:()=>vt,TRACE_EVENT_END:()=>xt,TRACE_FUNC_BEGIN:()=>Qe,TRACE_FUNC_END:()=>Le,Tensor:()=>Ce,env:()=>ye,registerBackend:()=>qt});var Pe=q(()=>{Df(),Pf(),Hf(),Cn(),Ff(),jf(),An(),Kf(),Qf()}),li=q(()=>{}),Rn={};Pt(Rn,{default:()=>Bn});var di,pi,Bn,Yf=q(()=>{var e;mc(),St(),yi(),di="ort-wasm-proxy-worker",pi=((e=globalThis.self)==null?void 0:e.name)===di,pi&&(self.onmessage=t=>{let{type:r,in:i}=t.data;try{switch(r){case"init-wasm":bi(i.wasm).then(()=>{Aa(i).then(()=>{postMessage({type:r})},a=>{postMessage({type:r,err:a})})},a=>{postMessage({type:r,err:a})});break;case"init-ep":{let{epName:a,env:n}=i;Oa(n,a).then(()=>{postMessage({type:r})},s=>{postMessage({type:r,err:s})});break}case"copy-from":{let{buffer:a}=i,n=Pr(a);postMessage({type:r,out:n});break}case"create":{let{model:a,options:n}=i;Ba(a,n).then(s=>{postMessage({type:r,out:s})},s=>{postMessage({type:r,err:s})});break}case"release":Ma(i),postMessage({type:r});break;case"run":{let{sessionId:a,inputIndices:n,inputs:s,outputIndices:u,options:l}=i;Da(a,n,s,u,new Array(u.length).fill(null),l).then(p=>{p.some(h=>h[3]!=="cpu")?postMessage({type:r,err:"Proxy does not support non-cpu tensor location."}):postMessage({type:r,out:p},Pa([...s,...p]))},p=>{postMessage({type:r,err:p})});break}case"end-profiling":Ua(i),postMessage({type:r});break;default:}}catch(a){postMessage({type:r,err:a})}}),Bn=pi?null:t=>new Worker(t??Me,{type:"module",name:di})}),Mn={};Pt(Mn,{default:()=>Dn});async function Nn(e={}){var zf,Cf;var t=e,r=!!globalThis.window,i=!!globalThis.WorkerGlobalScope,a=i&&((zf=self.name)==null?void 0:zf.startsWith("em-pthread"));t.mountExternalData=(o,d)=>{o.startsWith("./")&&(o=o.substring(2)),(t.Zc||(t.Zc=new Map)).set(o,d)},t.unmountExternalData=()=>{delete t.Zc},globalThis.SharedArrayBuffer??new WebAssembly.Memory({initial:0,maximum:0,ae:!0}).buffer.constructor;let n=o=>async(...d)=>{var m;try{if(t.$c)throw Error("Session already started");let c=t.$c={Nd:d[0],errors:[]},v=await o(...d);if(t.$c!==c)throw Error("Session mismatch");(m=t.gd)==null||m.flush();let T=c.errors;if(0<T.length){let z=await Promise.all(T);if(z=z.filter(B=>B),0<z.length)throw Error(z.join(`
`))}return v}finally{t.$c=null}};t.jsepInit=(o,d)=>{if(o==="webgpu"){[t.gd,t.Dd,t.Hd,t.jd,t.Gd,t.ac,t.Id,t.Kd,t.Ed,t.Fd,t.Jd]=d;let m=t.gd;t.jsepRegisterBuffer=(c,v,T,z)=>m.registerBuffer(c,v,T,z),t.jsepGetBuffer=c=>m.getBuffer(c),t.jsepCreateDownloader=(c,v,T)=>m.createDownloader(c,v,T),t.jsepOnCreateSession=c=>{m.onCreateSession(c)},t.jsepOnReleaseSession=c=>{m.onReleaseSession(c)},t.jsepOnRunStart=c=>m.onRunStart(c),t.Ld=(c,v)=>{m.upload(c,v)}}else if(o==="webnn"){let m=d[0];[t.Zd,t.vd,t.webnnEnsureTensor,t.xd,t.webnnDownloadTensor,t.Yd,t.webnnEnableTraceEvent]=d.slice(1),t.webnnReleaseTensorId=t.vd,t.webnnUploadTensor=t.xd,t.webnnRegisterMLContext=t.Yd,t.webnnOnRunStart=c=>m.onRunStart(c),t.webnnOnRunEnd=m.onRunEnd.bind(m),t.webnnOnReleaseSession=c=>{m.onReleaseSession(c)},t.webnnCreateMLTensorDownloader=(c,v)=>m.createMLTensorDownloader(c,v),t.webnnRegisterMLTensor=(c,v,T,z)=>m.registerMLTensor(c,v,T,z),t.webnnCreateMLContext=c=>m.createMLContext(c),t.webnnRegisterMLConstant=(c,v,T,z,B,W)=>m.registerMLConstant(c,v,T,z,B,t.Zc,W),t.webnnRegisterGraphInput=m.registerGraphInput.bind(m),t.webnnIsGraphInput=m.isGraphInput.bind(m),t.webnnRegisterGraphOutput=m.registerGraphOutput.bind(m),t.webnnIsGraphOutput=m.isGraphOutput.bind(m),t.webnnCreateTemporaryTensor=m.createTemporaryTensor.bind(m),t.webnnIsGraphInputOutputTypeSupported=m.isGraphInputOutputTypeSupported.bind(m)}};let s=()=>{let o=d=>(...m)=>{let c=Je;return m=d(...m),Je!=c?new Promise((v,T)=>{tn={resolve:v,reject:T}}):m};(()=>{for(let d of["_OrtAppendExecutionProvider","_OrtCreateSession","_OrtRun","_OrtRunWithBinding","_OrtBindInput"])t[d]=o(t[d])})(),n!==void 0&&(t._OrtRun=n(t._OrtRun),t._OrtRunWithBinding=n(t._OrtRunWithBinding)),s=void 0};t.asyncInit=()=>{s==null||s()};var u,l,p=(o,d)=>{throw d},h=self.location.href,f="";if(r||i){try{f=new URL(".",h).href}catch{}i&&(l=o=>{var d=new XMLHttpRequest;return d.open("GET",o,!1),d.responseType="arraybuffer",d.send(null),new Uint8Array(d.response)}),u=async o=>{if(C(o))return new Promise((m,c)=>{var v=new XMLHttpRequest;v.open("GET",o,!0),v.responseType="arraybuffer",v.onload=()=>{v.status==200||v.status==0&&v.response?m(v.response):c(v.status)},v.onerror=c,v.send(null)});var d=await fetch(o,{credentials:"same-origin"});if(d.ok)return d.arrayBuffer();throw Error(d.status+" : "+d.url)}}var g,y,_,w,S,x,b=console.log.bind(console),I=console.error.bind(console),k=b,E=I,A=!1,C=o=>o.startsWith("file://");function $(){yt.buffer!=D.buffer&&P()}if(a){let o=function(d){try{var m=d.data,c=m.Uc;if(c==="load"){let v=[];self.onmessage=T=>v.push(T),x=()=>{postMessage({Uc:"loaded"});for(let T of v)o(T);self.onmessage=o};for(let T of m.Ad)t[T]&&!t[T].proxy||(t[T]=(...z)=>{postMessage({Uc:"callHandler",zd:T,args:z})},T=="print"&&(k=t[T]),T=="printErr"&&(E=t[T]));yt=m.Vd,P(),y=m.Wd,ht(),ii()}else if(c==="run"){(function(v){var T=($(),K)[v+52>>>2>>>0];v=($(),K)[v+56>>>2>>>0],Dh(T,T-v),se(T)})(m.Tc),on(m.Tc,0,0,1,0,0),Uc(),Xa(m.Tc),N||(Ah(),N=!0);try{mg(m.Pd,m.dd)}catch(v){if(v!="unwind")throw v}}else m.target!=="setimmediate"&&(c==="checkMailbox"?N&&Zr():c&&(E(`worker: received unknown command ${c}`),E(m)))}catch(v){throw Oh(),v}};var N=!1;self.onunhandledrejection=d=>{throw d.reason||d},self.onmessage=o}var D,G,V,j,R,K,F,X,le,L,me,U=!1;function P(){var o=yt.buffer;t.HEAP8=D=new Int8Array(o),V=new Int16Array(o),t.HEAPU8=G=new Uint8Array(o),j=new Uint16Array(o),t.HEAP32=R=new Int32Array(o),t.HEAPU32=K=new Uint32Array(o),F=new Float32Array(o),X=new Float64Array(o),le=new BigInt64Array(o),L=new BigUint64Array(o)}function J(){U=!0,a?x():ot.tb()}function ee(o){throw E(o="Aborted("+o+")"),A=!0,o=new WebAssembly.RuntimeError(o+". Build with -sASSERTIONS for more info."),S==null||S(o),o}function $e(){return{a:{ma:Uy,hb:Dy,g:gg,J:yg,f:_g,o:wg,h:bg,ha:$g,b:vg,T:xg,Ia:Gc,n:Sg,_:Kc,Ya:Qc,Ea:Zc,Ga:Yc,Za:Xc,Wa:Jc,Pa:eh,Va:th,ka:rh,Fa:ih,Ca:ah,Xa:nh,Da:sh,cb:Tg,ea:kg,xa:Ig,va:zg,da:Ag,O:Og,H:Rg,wa:Bg,Z:Lg,ya:Wg,Sa:Vg,Aa:Hg,Ja:Fg,ta:jg,fa:Kg,Ra:Xa,$a:Qg,R:Jg,s:ay,c:Za,ib:ny,y:sy,M:oy,D:uy,m:ly,t:fh,jb:dy,I:py,S:cy,j:hy,v:fy,r:my,l:gy,Ma:yy,Na:_y,Oa:wy,Ka:_h,La:wh,ua:bh,eb:$y,bb:xy,u:Sy,aa:Ty,ga:ky,ab:vy,V:Iy,_a:Ey,Ba:zy,F:by,U:Cy,la:ti,za:Oy,gb:Ay,fb:Ry,Ta:Sh,Ua:Th,Ha:cr,$:kh,ja:Ih,Qa:Eh,ia:zh,lb:$0,na:f0,mb:b0,oa:h0,G:a0,d:Wy,q:qy,w:Py,B:Xy,pb:d0,K:t0,x:Gy,pa:p0,X:m0,ba:l0,nb:w0,ob:_0,ra:n0,qa:u0,qb:s0,N:r0,Y:c0,e:Vy,A:Hy,k:Ly,kb:v0,p:jy,z:Ky,C:Fy,E:Qy,L:Jy,rb:i0,Q:g0,ca:e0,W:y0,sb:Yy,sa:Zy,P:o0,i:My,a:yt,db:Ue}}}async function ht(){function o(c,v){var T=ot=c.exports;c={};for(let[z,B]of Object.entries(T))typeof B=="function"?(T=Zg(B),c[z]=T):c[z]=B;return ot=c,ot=function(){var z=ot,B=H=>ne=>H(ne)>>>0,W=H=>()=>H()>>>0;return(z=Object.assign({},z)).ub=B(z.ub),z.Yb=W(z.Yb),z._b=B(z._b),z.mc=B(z.mc),z.nc=W(z.nc),z.rc=B(z.rc),z}(),Nc.push(ot.$b),Ch=(c=ot).ub,Ah=c.vb,t._OrtInit=c.wb,t._OrtGetLastError=c.xb,t._OrtCreateSessionOptions=c.yb,t._OrtAppendExecutionProvider=c.zb,t._OrtAddFreeDimensionOverride=c.Ab,t._OrtAddSessionConfigEntry=c.Bb,t._OrtReleaseSessionOptions=c.Cb,t._OrtCreateSession=c.Db,t._OrtReleaseSession=c.Eb,t._OrtGetInputOutputCount=c.Fb,t._OrtGetInputOutputMetadata=c.Gb,t._OrtFree=c.Hb,t._OrtCreateTensor=c.Ib,t._OrtGetTensorData=c.Jb,t._OrtReleaseTensor=c.Kb,t._OrtCreateRunOptions=c.Lb,t._OrtAddRunConfigEntry=c.Mb,t._OrtReleaseRunOptions=c.Nb,t._OrtCreateBinding=c.Ob,t._OrtBindInput=c.Pb,t._OrtBindOutput=c.Qb,t._OrtClearBoundOutputs=c.Rb,t._OrtReleaseBinding=c.Sb,t._OrtRunWithBinding=c.Tb,t._OrtRun=c.Ub,t._OrtEndProfiling=c.Vb,t._JsepOutput=c.Wb,t._JsepGetNodeName=c.Xb,ri=c.Yb,et=t._free=c.Zb,mr=t._malloc=c._b,on=c.bc,Oh=c.cc,Rh=c.dc,Bh=c.ec,un=c.fc,Mh=c.gc,Nh=c.hc,ue=c.ic,gr=c.jc,Dh=c.kc,se=c.lc,ln=c.mc,oe=c.nc,Uh=c.oc,dn=c.pc,Ph=c.qc,qh=c.rc,Lh=c.sc,pn=c.tc,Wh=c.uc,Vh=c.vc,Gh=c.wc,Hh=c.xc,Fh=c.yc,jh=c.zc,Kh=c.Ac,Qh=c.Bc,Zh=c.Cc,Yh=c.Dc,Xh=c.Ec,Jh=c.Fc,ef=c.Gc,tf=c.Hc,rf=c.Ic,af=c.Jc,nf=c.Kc,sf=c.Lc,of=c.Mc,uf=c.Nc,lf=c.Oc,df=c.Pc,pf=c.Rc,cf=c.Sc,hf=c.bd,ff=c.cd,mf=c.hd,gf=c.kd,yf=c.ld,_f=c.md,wf=c.nd,bf=c.od,$f=c.pd,vf=c.qd,xf=c.rd,Sf=c.wd,Tf=c.Rd,kf=c.Sd,If=c.Td,Ef=c.Ud,y=v,ot}var d,m=$e();return t.instantiateWasm?new Promise(c=>{t.instantiateWasm(m,(v,T)=>{c(o(v,T))})}):a?o(new WebAssembly.Instance(y,$e()),y):(me??(me=t.locateFile?t.locateFile?t.locateFile("ort-wasm-simd-threaded.jsep.wasm",f):f+"ort-wasm-simd-threaded.jsep.wasm":new URL(""+new URL("ort-wasm-simd-threaded.jsep-C887KxcQ.wasm",self.location.href).href,self.location.href).href),d=await async function(c){var v=me;if(!g&&!C(v))try{var T=fetch(v,{credentials:"same-origin"});return await WebAssembly.instantiateStreaming(T,c)}catch(z){E(`wasm streaming compile failed: ${z}`),E("falling back to ArrayBuffer instantiation")}return async function(z,B){try{var W=await async function(H){if(!g)try{var ne=await u(H);return new Uint8Array(ne)}catch{}if(H==me&&g)H=new Uint8Array(g);else{if(!l)throw"both async and sync fetching of the wasm failed";H=l(H)}return H}(z);return await WebAssembly.instantiate(W,B)}catch(H){E(`failed to asynchronously prepare wasm: ${H}`),ee(H)}}(v,c)}(m),o(d.instance,d.module))}class ft{constructor(d){Af(this,"name","ExitStatus");this.message=`Program terminated with exit(${d})`,this.status=d}}var pr=o=>{o.terminate(),o.onmessage=()=>{}},Gr=[],De=0,Re=null,mt=o=>{gt.length==0&&(qc(),Pc(gt[0]));var d=gt.pop();if(!d)return 6;hr.push(d),Mt[o.Tc]=d,d.Tc=o.Tc;var m={Uc:"run",Pd:o.Od,dd:o.dd,Tc:o.Tc};return d.postMessage(m,o.ud),0},we=0,ie=(o,d,...m)=>{var c,v=16*m.length,T=oe(),z=ln(v),B=z>>>3;for(c of m)typeof c=="bigint"?(($(),le)[B++>>>0]=1n,($(),le)[B++>>>0]=c):(($(),le)[B++>>>0]=0n,($(),X)[B++>>>0]=c);return o=Rh(o,0,v,z,d),se(T),o};function Ue(o){if(a)return ie(0,1,o);if(_=o,!(0<we)){for(var d of hr)pr(d);for(d of gt)pr(d);gt=[],hr=[],Mt={},A=!0}p(0,new ft(o))}function Hr(o){if(a)return ie(1,0,o);cr(o)}var cr=o=>{if(_=o,a)throw Hr(o),"unwind";Ue(o)},gt=[],hr=[],Nc=[],Mt={},Dc=o=>{var d=o.Tc;delete Mt[d],gt.push(o),hr.splice(hr.indexOf(o),1),o.Tc=0,Bh(d)};function Uc(){Nc.forEach(o=>o())}var Pc=o=>new Promise(d=>{o.onmessage=v=>{var T=v.data;if(v=T.Uc,T.ad&&T.ad!=ri()){var z=Mt[T.ad];z?z.postMessage(T,T.ud):E(`Internal error! Worker sent a message "${v}" to target pthread ${T.ad}, but that thread no longer exists!`)}else v==="checkMailbox"?Zr():v==="spawnThread"?mt(T):v==="cleanupThread"?Qr(()=>{Dc(Mt[T.Qd])}):v==="loaded"?(o.loaded=!0,d(o)):T.target==="setimmediate"?o.postMessage(T):v==="uncaughtException"?o.onerror(T.error):v==="callHandler"?t[T.zd](...T.args):v&&E(`worker sent an unknown command ${v}`)},o.onerror=v=>{throw E(`worker sent an error! ${v.filename}:${v.lineno}: ${v.message}`),v};var m,c=[];for(m of[])t.propertyIsEnumerable(m)&&c.push(m);o.postMessage({Uc:"load",Ad:c,Vd:yt,Wd:y})});function qc(){var o=new Worker((()=>{let d=URL;return self.location.href>"file:"&&self.location.href<"file;"?new d("ort.bundle.min.mjs",self.location.href):new URL(self.location.href)})(),{type:"module",workerData:"em-pthread",name:"em-pthread"});gt.push(o)}var yt,mg=(o,d)=>{we=0,o=pn(o,d),0<we?_=o:un(o)},Fr=[],jr=0;function gg(o){var d=new Fa(o>>>=0);return($(),D)[d.Vc+12>>>0]==0&&(Lc(d,!0),jr--),Wc(d,!1),Fr.push(d),qh(o)}var Ht=0,yg=()=>{ue(0,0);var o=Fr.pop();Uh(o.ed),Ht=0};function Lc(o,d){d=d?1:0,($(),D)[o.Vc+12>>>0]=d}function Wc(o,d){d=d?1:0,($(),D)[o.Vc+13>>>0]=d}class Fa{constructor(d){this.ed=d,this.Vc=d-24}}var ja=o=>{var d=Ht;if(!d)return gr(0),0;var m=new Fa(d);($(),K)[m.Vc+16>>>2>>>0]=d;var c=($(),K)[m.Vc+4>>>2>>>0];if(!c)return gr(0),d;for(var v of o){if(v===0||v===c)break;if(Ph(v,c,m.Vc+16))return gr(v),d}return gr(c),d};function _g(){return ja([])}function wg(o){return ja([o>>>0])}function bg(o,d,m,c){return ja([o>>>0,d>>>0,m>>>0,c>>>0])}var $g=()=>{var o=Fr.pop();o||ee("no exception to throw");var d=o.ed;throw($(),D)[o.Vc+13>>>0]==0&&(Fr.push(o),Wc(o,!0),Lc(o,!1),jr++),dn(d),Ht=d};function vg(o,d,m){var c=new Fa(o>>>=0);throw d>>>=0,m>>>=0,($(),K)[c.Vc+16>>>2>>>0]=0,($(),K)[c.Vc+4>>>2>>>0]=d,($(),K)[c.Vc+8>>>2>>>0]=m,dn(o),jr++,Ht=o}var xg=()=>jr;function Vc(o,d,m,c){return a?ie(2,1,o,d,m,c):Gc(o,d,m,c)}function Gc(o,d,m,c){if(o>>>=0,d>>>=0,m>>>=0,c>>>=0,!globalThis.SharedArrayBuffer)return 6;var v=[];return a&&v.length===0?Vc(o,d,m,c):(o={Od:m,Tc:o,dd:c,ud:v},a?(o.Uc="spawnThread",postMessage(o,v),0):mt(o))}function Sg(o){throw Ht||(Ht=o>>>0),Ht}var Hc=globalThis.TextDecoder&&new TextDecoder,Fc=(o,d,m,c)=>{if(m=d+m,c)return m;for(;o[d]&&!(d>=m);)++d;return d},jc=(o,d=0,m,c)=>{if(16<(m=Fc(o,d>>>=0,m,c))-d&&o.buffer&&Hc)return Hc.decode(o.buffer instanceof ArrayBuffer?o.subarray(d,m):o.slice(d,m));for(c="";d<m;){var v=o[d++];if(128&v){var T=63&o[d++];if((224&v)==192)c+=String.fromCharCode((31&v)<<6|T);else{var z=63&o[d++];65536>(v=(240&v)==224?(15&v)<<12|T<<6|z:(7&v)<<18|T<<12|z<<6|63&o[d++])?c+=String.fromCharCode(v):(v-=65536,c+=String.fromCharCode(55296|v>>10,56320|1023&v))}}else c+=String.fromCharCode(v)}return c},Se=(o,d,m)=>(o>>>=0)?jc(($(),G),o,d,m):"";function Kc(o,d,m){return a?ie(3,1,o,d,m):0}function Qc(o,d){if(a)return ie(4,1,o,d)}function Zc(o,d){if(a)return ie(5,1,o,d)}function Yc(o,d,m){if(a)return ie(6,1,o,d,m)}function Xc(o,d,m){return a?ie(7,1,o,d,m):0}function Jc(o,d){if(a)return ie(8,1,o,d)}function eh(o,d,m){if(a)return ie(9,1,o,d,m)}function th(o,d,m,c){if(a)return ie(10,1,o,d,m,c)}function rh(o,d,m,c){if(a)return ie(11,1,o,d,m,c)}function ih(o,d,m,c){if(a)return ie(12,1,o,d,m,c)}function ah(o){if(a)return ie(13,1,o)}function nh(o,d){if(a)return ie(14,1,o,d)}function sh(o,d,m){if(a)return ie(15,1,o,d,m)}var Tg=()=>ee(""),Xe=o=>{o>>>=0;for(var d="";;){var m=($(),G)[o++>>>0];if(!m)return d;d+=String.fromCharCode(m)}},Ka={},Qa={},Ft=class extends Error{constructor(o){super(o),this.name="BindingError"}};function st(o,d,m={}){return function(c,v,T={}){var z=v.name;if(!c)throw new Ft(`type "${z}" must have a positive integer typeid pointer`);if(Qa.hasOwnProperty(c)){if(T.Bd)return;throw new Ft(`Cannot register type '${z}' twice`)}Qa[c]=v,Ka.hasOwnProperty(c)&&(v=Ka[c],delete Ka[c],v.forEach(B=>B()))}(o,d,m)}var oh=(o,d,m)=>{switch(d){case 1:return m?c=>($(),D)[c>>>0]:c=>($(),G)[c>>>0];case 2:return m?c=>($(),V)[c>>>1>>>0]:c=>($(),j)[c>>>1>>>0];case 4:return m?c=>($(),R)[c>>>2>>>0]:c=>($(),K)[c>>>2>>>0];case 8:return m?c=>($(),le)[c>>>3>>>0]:c=>($(),L)[c>>>3>>>0];default:throw new TypeError(`invalid integer width (${d}): ${o}`)}};function kg(o,d,m,c,v){o>>>=0,m>>>=0,d=Xe(d>>>0);let T=z=>z;if(c=c===0n){let z=8*m;T=B=>BigInt.asUintN(z,B),v=T(v)}st(o,{name:d,Qc:T,Xc:(z,B)=>(typeof B=="number"&&(B=BigInt(B)),B),Wc:oh(d,m,!c),Yc:null})}function Ig(o,d,m,c){st(o>>>=0,{name:d=Xe(d>>>0),Qc:function(v){return!!v},Xc:function(v,T){return T?m:c},Wc:function(v){return this.Qc(($(),G)[v>>>0])},Yc:null})}var uh=[],Nt=[0,1,,1,null,1,!0,1,!1,1];function Za(o){9<(o>>>=0)&&--Nt[o+1]==0&&(Nt[o]=void 0,uh.push(o))}var qe=o=>{if(!o)throw new Ft(`Cannot use deleted val. handle = ${o}`);return Nt[o]},Ke=o=>{switch(o){case void 0:return 2;case null:return 4;case!0:return 6;case!1:return 8;default:let d=uh.pop()||Nt.length;return Nt[d]=o,Nt[d+1]=1,d}};function Ya(o){return this.Qc(($(),K)[o>>>2>>>0])}var Eg={name:"emscripten::val",Qc:o=>{var d=qe(o);return Za(o),d},Xc:(o,d)=>Ke(d),Wc:Ya,Yc:null};function zg(o){return st(o>>>0,Eg)}var Cg=(o,d)=>{switch(d){case 4:return function(m){return this.Qc(($(),F)[m>>>2>>>0])};case 8:return function(m){return this.Qc(($(),X)[m>>>3>>>0])};default:throw new TypeError(`invalid float width (${d}): ${o}`)}};function Ag(o,d,m){m>>>=0,st(o>>>=0,{name:d=Xe(d>>>0),Qc:c=>c,Xc:(c,v)=>v,Wc:Cg(d,m),Yc:null})}function Og(o,d,m,c,v){o>>>=0,m>>>=0,d=Xe(d>>>0);let T=B=>B;if(c===0){var z=32-8*m;T=B=>B<<z>>>z,v=T(v)}st(o,{name:d,Qc:T,Xc:(B,W)=>W,Wc:oh(d,m,c!==0),Yc:null})}function Rg(o,d,m){function c(T){var z=($(),K)[T>>>2>>>0];return T=($(),K)[T+4>>>2>>>0],new v(($(),D).buffer,T,z)}var v=[Int8Array,Uint8Array,Int16Array,Uint16Array,Int32Array,Uint32Array,Float32Array,Float64Array,BigInt64Array,BigUint64Array][d];st(o>>>=0,{name:m=Xe(m>>>0),Qc:c,Wc:c},{Bd:!0})}var _t=(o,d,m)=>{var c=($(),G);if(d>>>=0,0<m){var v=d;m=d+m-1;for(var T=0;T<o.length;++T){var z=o.codePointAt(T);if(127>=z){if(d>=m)break;c[d++>>>0]=z}else if(2047>=z){if(d+1>=m)break;c[d++>>>0]=192|z>>6,c[d++>>>0]=128|63&z}else if(65535>=z){if(d+2>=m)break;c[d++>>>0]=224|z>>12,c[d++>>>0]=128|z>>6&63,c[d++>>>0]=128|63&z}else{if(d+3>=m)break;c[d++>>>0]=240|z>>18,c[d++>>>0]=128|z>>12&63,c[d++>>>0]=128|z>>6&63,c[d++>>>0]=128|63&z,T++}}c[d>>>0]=0,o=d-v}else o=0;return o},Kr=o=>{for(var d=0,m=0;m<o.length;++m){var c=o.charCodeAt(m);127>=c?d++:2047>=c?d+=2:55296<=c&&57343>=c?(d+=4,++m):d+=3}return d};function Bg(o,d){st(o>>>=0,{name:d=Xe(d>>>0),Qc(m){var c=($(),K)[m>>>2>>>0];return c=Se(m+4,c,!0),et(m),c},Xc(m,c){c instanceof ArrayBuffer&&(c=new Uint8Array(c));var v=typeof c=="string";if(!(v||ArrayBuffer.isView(c)&&c.BYTES_PER_ELEMENT==1))throw new Ft("Cannot pass non-string to std::string");var T=v?Kr(c):c.length,z=mr(4+T+1),B=z+4;return($(),K)[z>>>2>>>0]=T,v?_t(c,B,T+1):($(),G).set(c,B>>>0),m!==null&&m.push(et,z),z},Wc:Ya,Yc(m){et(m)}})}var lh=globalThis.TextDecoder?new TextDecoder("utf-16le"):void 0,Mg=(o,d,m)=>{if(o>>>=1,16<(d=Fc(($(),j),o,d/2,m))-o&&lh)return lh.decode(($(),j).slice(o,d));for(m="";o<d;++o){var c=($(),j)[o>>>0];m+=String.fromCharCode(c)}return m},Ng=(o,d,m)=>{if(m??(m=2147483647),2>m)return 0;var c=d;m=(m-=2)<2*o.length?m/2:o.length;for(var v=0;v<m;++v){var T=o.charCodeAt(v);($(),V)[d>>>1>>>0]=T,d+=2}return($(),V)[d>>>1>>>0]=0,d-c},Dg=o=>2*o.length,Ug=(o,d,m)=>{var c="";o>>>=2;for(var v=0;!(v>=d/4);v++){var T=($(),K)[o+v>>>0];if(!T&&!m)break;c+=String.fromCodePoint(T)}return c},Pg=(o,d,m)=>{if(d>>>=0,m??(m=2147483647),4>m)return 0;var c=d;m=c+m-4;for(var v=0;v<o.length;++v){var T=o.codePointAt(v);if(65535<T&&v++,($(),R)[d>>>2>>>0]=T,(d+=4)+4>m)break}return($(),R)[d>>>2>>>0]=0,d-c},qg=o=>{for(var d=0,m=0;m<o.length;++m)65535<o.codePointAt(m)&&m++,d+=4;return d};function Lg(o,d,m){if(o>>>=0,d>>>=0,m=Xe(m>>>=0),d===2)var c=Mg,v=Ng,T=Dg;else c=Ug,v=Pg,T=qg;st(o,{name:m,Qc:z=>{var B=($(),K)[z>>>2>>>0];return B=c(z+4,B*d,!0),et(z),B},Xc:(z,B)=>{if(typeof B!="string")throw new Ft(`Cannot pass non-string to C++ string type ${m}`);var W=T(B),H=mr(4+W+d);return($(),K)[H>>>2>>>0]=W/d,v(B,H+4,W+d),z!==null&&z.push(et,H),H},Wc:Ya,Yc(z){et(z)}})}function Wg(o,d){st(o>>>=0,{Cd:!0,name:d=Xe(d>>>0),Qc:()=>{},Xc:()=>{}})}function Vg(o){on(o>>>0,!i,1,!r,131072,!1),Uc()}var Qr=o=>{if(!A)try{if(o(),!(0<we))try{a?ri()&&un(_):cr(_)}catch(d){d instanceof ft||d=="unwind"||p(0,d)}}catch(d){d instanceof ft||d=="unwind"||p(0,d)}},Gg=!Atomics.waitAsync||((Cf=globalThis.navigator)==null?void 0:Cf.userAgent)&&91>Number((navigator.userAgent.match(/Chrom(e|ium)\/([0-9]+)\./)||[])[2]);function Xa(o){o>>>=0,Gg||(Atomics.waitAsync(($(),R),o>>>2,o).value.then(Zr),o+=128,Atomics.store(($(),R),o>>>2,1))}var Zr=()=>Qr(()=>{var o=ri();o&&(Xa(o),Nh())});function Hg(o,d){(o>>>=0)==d>>>0?setTimeout(Zr):a?postMessage({ad:o,Uc:"checkMailbox"}):(o=Mt[o])&&o.postMessage({Uc:"checkMailbox"})}var Ja=[];function Fg(o,d,m,c,v){for(d>>>=0,v>>>=0,Ja.length=0,m=v>>>3,c=v+c>>>3;m<c;){var T;T=($(),le)[m++>>>0]?($(),le)[m++>>>0]:($(),X)[m++>>>0],Ja.push(T)}return(d?cn[d]:Ny[o])(...Ja)}var jg=()=>{we=0};function Kg(o){o>>>=0,a?postMessage({Uc:"cleanupThread",Qd:o}):Dc(Mt[o])}function Qg(o){}var Yr=o=>{try{o()}catch(d){ee(d)}};function Zg(o){var d=(...m)=>{Xr.push(o);try{return o(...m)}finally{A||(Xr.pop(),Je&&wt===1&&Xr.length===0&&(wt=0,we+=1,Yr(kf),typeof Fibers<"u"&&Fibers.ce()))}};return ch.set(o,d),d}var wt=0,Je=null,dh=0,Xr=[],en=new Map,ph=new Map,ch=new Map,Yg=0,tn=null,Xg=[],hh=o=>function(d){if(!A){if(wt===0){var m=!1,c=!1;d((v=0)=>{if(!A&&(dh=v,m=!0,c)){wt=2,Yr(()=>If(Je)),typeof MainLoop<"u"&&MainLoop.yd&&MainLoop.resume(),v=!1;try{var T=function(){var W=($(),R)[Je+8>>>2>>>0];return W=ph.get(W),W=ch.get(W),--we,W()}()}catch(W){T=W,v=!0}var z=!1;if(!Je){var B=tn;B&&(tn=null,(v?B.reject:B.resolve)(T),z=!0)}if(v&&!z)throw T}}),c=!0,m||(wt=1,Je=function(){var v=mr(65548),T=v+12;if(($(),K)[v>>>2>>>0]=T,($(),K)[v+4>>>2>>>0]=T+65536,T=Xr[0],!en.has(T)){var z=Yg++;en.set(T,z),ph.set(z,T)}return T=en.get(T),($(),R)[v+8>>>2>>>0]=T,v}(),typeof MainLoop<"u"&&MainLoop.yd&&MainLoop.pause(),Yr(()=>Tf(Je)))}else wt===2?(wt=0,Yr(Ef),et(Je),Je=null,Xg.forEach(Qr)):ee(`invalid state: ${wt}`);return dh}}(d=>{o().then(d)});function Jg(o){return o>>>=0,hh(async()=>{var d=await qe(o);return Ke(d)})}var rn=[],ey=o=>{var d=rn.length;return rn.push(o),d},ty=(o,d)=>{for(var m=Array(o),c=0;c<o;++c){var v=c,T=($(),K)[d+4*c>>>2>>>0],z=Qa[T];if(z===void 0)throw o=`parameter ${c}`,T=Ch(T),d=Xe(T),et(T),new Ft(`${o} has unknown type ${d}`);m[v]=z}return m},ry=(o,d,m)=>{var c=[];return o=o(c,m),c.length&&(($(),K)[d>>>2>>>0]=Ke(c)),o},iy={},Jr=o=>{var d=iy[o];return d===void 0?Xe(o):d};function ay(o,d,m){var[c,...v]=ty(o,d>>>0);d=c.Xc.bind(c);var T=v.map(W=>W.Wc.bind(W));o--;var z={toValue:qe};switch(o=T.map((W,H)=>{var ne=`argFromPtr${H}`;return z[ne]=W,`${ne}(args${H?"+"+8*H:""})`}),m){case 0:var B="toValue(handle)";break;case 2:B="new (toValue(handle))";break;case 3:B="";break;case 1:z.getStringOrSymbol=Jr,B="toValue(handle)[getStringOrSymbol(methodName)]"}return B+=`(${o})`,c.Cd||(z.toReturnWire=d,z.emval_returnValue=ry,B=`return emval_returnValue(toReturnWire, destructorsRef, ${B})`),B=`return function (handle, methodName, destructorsRef, args) {
  ${B}
  }`,m=new Function(Object.keys(z),B)(...Object.values(z)),B=`methodCaller<(${v.map(W=>W.name)}) => ${c.name}>`,ey(Object.defineProperty(m,"name",{value:B}))}function ny(o,d){return d>>>=0,(o=qe(o>>>0))==qe(d)}function sy(o){return(o>>>=0)?(o=Jr(o),Ke(globalThis[o])):Ke(globalThis)}function oy(o){return o=Jr(o>>>0),Ke(t[o])}function uy(o,d){return d>>>=0,o=qe(o>>>0),d=qe(d),Ke(o[d])}function ly(o){9<(o>>>=0)&&(Nt[o+1]+=1)}function fh(o,d,m,c,v){return rn[o>>>0](d>>>0,m>>>0,c>>>0,v>>>0)}function dy(o,d,m,c,v){return fh(o>>>0,d>>>0,m>>>0,c>>>0,v>>>0)}function py(){return Ke([])}function cy(o){o=qe(o>>>0);for(var d=Array(o.length),m=0;m<o.length;m++)d[m]=o[m];return Ke(d)}function hy(o){return Ke(Jr(o>>>0))}function fy(){return Ke({})}function my(o){for(var d=qe(o>>>=0);d.length;){var m=d.pop();d.pop()(m)}Za(o)}function gy(o,d,m){d>>>=0,m>>>=0,o=qe(o>>>0),d=qe(d),m=qe(m),o[d]=m}function yy(o,d){o=-9007199254740992>o||9007199254740992<o?NaN:Number(o),d>>>=0,o=new Date(1e3*o),($(),R)[d>>>2>>>0]=o.getUTCSeconds(),($(),R)[d+4>>>2>>>0]=o.getUTCMinutes(),($(),R)[d+8>>>2>>>0]=o.getUTCHours(),($(),R)[d+12>>>2>>>0]=o.getUTCDate(),($(),R)[d+16>>>2>>>0]=o.getUTCMonth(),($(),R)[d+20>>>2>>>0]=o.getUTCFullYear()-1900,($(),R)[d+24>>>2>>>0]=o.getUTCDay(),o=(o.getTime()-Date.UTC(o.getUTCFullYear(),0,1,0,0,0,0))/864e5|0,($(),R)[d+28>>>2>>>0]=o}var mh=o=>o%4==0&&(o%100!=0||o%400==0),gh=[0,31,60,91,121,152,182,213,244,274,305,335],yh=[0,31,59,90,120,151,181,212,243,273,304,334];function _y(o,d){o=-9007199254740992>o||9007199254740992<o?NaN:Number(o),d>>>=0,o=new Date(1e3*o),($(),R)[d>>>2>>>0]=o.getSeconds(),($(),R)[d+4>>>2>>>0]=o.getMinutes(),($(),R)[d+8>>>2>>>0]=o.getHours(),($(),R)[d+12>>>2>>>0]=o.getDate(),($(),R)[d+16>>>2>>>0]=o.getMonth(),($(),R)[d+20>>>2>>>0]=o.getFullYear()-1900,($(),R)[d+24>>>2>>>0]=o.getDay();var m=(mh(o.getFullYear())?gh:yh)[o.getMonth()]+o.getDate()-1|0;($(),R)[d+28>>>2>>>0]=m,($(),R)[d+36>>>2>>>0]=-60*o.getTimezoneOffset(),m=new Date(o.getFullYear(),6,1).getTimezoneOffset();var c=new Date(o.getFullYear(),0,1).getTimezoneOffset();o=0|(m!=c&&o.getTimezoneOffset()==Math.min(c,m)),($(),R)[d+32>>>2>>>0]=o}function wy(o){o>>>=0;var d=new Date(($(),R)[o+20>>>2>>>0]+1900,($(),R)[o+16>>>2>>>0],($(),R)[o+12>>>2>>>0],($(),R)[o+8>>>2>>>0],($(),R)[o+4>>>2>>>0],($(),R)[o>>>2>>>0],0),m=($(),R)[o+32>>>2>>>0],c=d.getTimezoneOffset(),v=new Date(d.getFullYear(),6,1).getTimezoneOffset(),T=new Date(d.getFullYear(),0,1).getTimezoneOffset(),z=Math.min(T,v);return 0>m?($(),R)[o+32>>>2>>>0]=+(v!=T&&z==c):0<m!=(z==c)&&(v=Math.max(T,v),d.setTime(d.getTime()+6e4*((0<m?z:v)-c))),($(),R)[o+24>>>2>>>0]=d.getDay(),m=(mh(d.getFullYear())?gh:yh)[d.getMonth()]+d.getDate()-1|0,($(),R)[o+28>>>2>>>0]=m,($(),R)[o>>>2>>>0]=d.getSeconds(),($(),R)[o+4>>>2>>>0]=d.getMinutes(),($(),R)[o+8>>>2>>>0]=d.getHours(),($(),R)[o+12>>>2>>>0]=d.getDate(),($(),R)[o+16>>>2>>>0]=d.getMonth(),($(),R)[o+20>>>2>>>0]=d.getYear(),o=d.getTime(),BigInt(isNaN(o)?-1:o/1e3)}function _h(o,d,m,c,v,T,z){return a?ie(16,1,o,d,m,c,v,T,z):-52}function wh(o,d,m,c,v,T){if(a)return ie(17,1,o,d,m,c,v,T)}var fr={},by=()=>performance.timeOrigin+performance.now();function bh(o,d){if(a)return ie(18,1,o,d);if(fr[o]&&(clearTimeout(fr[o].id),delete fr[o]),!d)return 0;var m=setTimeout(()=>{delete fr[o],Qr(()=>Mh(o,performance.timeOrigin+performance.now()))},d);return fr[o]={id:m,be:d},0}function $y(o,d,m,c){o>>>=0,d>>>=0,m>>>=0,c>>>=0;var v=new Date().getFullYear(),T=new Date(v,0,1).getTimezoneOffset();v=new Date(v,6,1).getTimezoneOffset();var z=Math.max(T,v);($(),K)[o>>>2>>>0]=60*z,($(),R)[d>>>2>>>0]=+(T!=v),o=(d=B=>{var W=Math.abs(B);return`UTC${0<=B?"-":"+"}${String(Math.floor(W/60)).padStart(2,"0")}${String(W%60).padStart(2,"0")}`})(T),d=d(v),v<T?(_t(o,m,17),_t(d,c,17)):(_t(o,c,17),_t(d,m,17))}var vy=()=>Date.now();function xy(o,d,m){return m>>>=0,0<=o&&3>=o?(o===0?o=Date.now():o=performance.timeOrigin+performance.now(),o=Math.round(1e6*o),($(),le)[m>>>3>>>0]=BigInt(o),0):28}var an=[],$h=(o,d)=>{an.length=0;for(var m;m=($(),G)[o++>>>0];){var c=m!=105;d+=(c&=m!=112)&&d%8?4:0,an.push(m==112?($(),K)[d>>>2>>>0]:m==106?($(),le)[d>>>3>>>0]:m==105?($(),R)[d>>>2>>>0]:($(),X)[d>>>3>>>0]),d+=c?8:4}return an};function Sy(o,d,m){return o>>>=0,d=$h(d>>>0,m>>>0),cn[o](...d)}function Ty(o,d,m){return o>>>=0,d=$h(d>>>0,m>>>0),cn[o](...d)}var ky=()=>{};function Iy(o,d){return E(Se(o>>>0,d>>>0))}var Ey=()=>{throw we+=1,"unwind"};function zy(){return 4294901760}var Cy=()=>navigator.hardwareConcurrency,Dt={},ei=o=>{var d;return(d=/\bwasm-function\[\d+\]:(0x[0-9a-f]+)/.exec(o))?+d[1]:(d=/:(\d+):\d+(?:\)|$)/.exec(o))?2147483648|+d[1]:0},vh=o=>{for(var d of o)(o=ei(d))&&(Dt[o]=d)};function Ay(){var o=Error().stack.toString().split(`
`);return o[0]=="Error"&&o.shift(),vh(o),Dt.sd=ei(o[3]),Dt.Md=o,Dt.sd}function ti(o){if(!(o=Dt[o>>>0]))return 0;var d;if(d=/^\s+at .*\.wasm\.(.*) \(.*\)$/.exec(o))o=d[1];else if(d=/^\s+at (.*) \(.*\)$/.exec(o))o=d[1];else{if(!(d=/^(.+?)@/.exec(o)))return 0;o=d[1]}et(ti.td??0),d=Kr(o)+1;var m=mr(d);return m&&_t(o,m,d),ti.td=m,ti.td}function Oy(o){o>>>=0;var d=($(),G).length;if(o<=d||4294901760<o)return!1;for(var m=1;4>=m;m*=2){var c=d*(1+.2/m);c=Math.min(c,o+100663296);e:{c=(Math.min(4294901760,65536*Math.ceil(Math.max(o,c)/65536))-yt.buffer.byteLength+65535)/65536|0;try{yt.grow(c),P();var v=1;break e}catch{}v=void 0}if(v)return!0}return!1}function Ry(o,d,m){if(o>>>=0,d>>>=0,Dt.sd==o)var c=Dt.Md;else(c=Error().stack.toString().split(`
`))[0]=="Error"&&c.shift(),vh(c);for(var v=3;c[v]&&ei(c[v])!=o;)++v;for(o=0;o<m&&c[o+v];++o)($(),R)[d+4*o>>>2>>>0]=ei(c[o+v]);return o}var nn,sn={},xh=()=>{var c;if(!nn){var o,d={USER:"web_user",LOGNAME:"web_user",PATH:"/",PWD:"/",HOME:"/home/web_user",LANG:(((c=globalThis.navigator)==null?void 0:c.language)??"C").replace("-","_")+".UTF-8",_:"./this.program"};for(o in sn)sn[o]===void 0?delete d[o]:d[o]=sn[o];var m=[];for(o in d)m.push(`${o}=${d[o]}`);nn=m}return nn};function Sh(o,d){if(a)return ie(19,1,o,d);o>>>=0,d>>>=0;var m,c=0,v=0;for(m of xh()){var T=d+c;($(),K)[o+v>>>2>>>0]=T,c+=_t(m,T,1/0)+1,v+=4}return 0}function Th(o,d){if(a)return ie(20,1,o,d);o>>>=0,d>>>=0;var m=xh();for(var c of(($(),K)[o>>>2>>>0]=m.length,o=0,m))o+=Kr(c)+1;return($(),K)[d>>>2>>>0]=o,0}function kh(o){return a?ie(21,1,o):52}function Ih(o,d,m,c){return a?ie(22,1,o,d,m,c):52}function Eh(o,d,m,c){return a?ie(23,1,o,d,m,c):70}var By=[null,[],[]];function zh(o,d,m,c){if(a)return ie(24,1,o,d,m,c);d>>>=0,m>>>=0,c>>>=0;for(var v=0,T=0;T<m;T++){var z=($(),K)[d>>>2>>>0],B=($(),K)[d+4>>>2>>>0];d+=8;for(var W=0;W<B;W++){var H=o,ne=($(),G)[z+W>>>0],pe=By[H];ne===0||ne===10?((H===1?k:E)(jc(pe)),pe.length=0):pe.push(ne)}v+=B}return($(),K)[c>>>2>>>0]=v,0}function My(o){return o>>>0}a||function(){for(var o=t.numThreads-1;o--;)qc();Gr.push(async()=>{var d=async function(){if(!a)return Promise.all(gt.map(Pc))}();De++,await d,--De==0&&Re&&(d=Re,Re=null,d())})}(),a||(yt=new WebAssembly.Memory({initial:256,maximum:65536,shared:!0}),P()),t.wasmBinary&&(g=t.wasmBinary),t.stackSave=()=>oe(),t.stackRestore=o=>se(o),t.stackAlloc=o=>ln(o),t.setValue=function(o,d,m="i8"){switch(m.endsWith("*")&&(m="*"),m){case"i1":case"i8":($(),D)[o>>>0]=d;break;case"i16":($(),V)[o>>>1>>>0]=d;break;case"i32":($(),R)[o>>>2>>>0]=d;break;case"i64":($(),le)[o>>>3>>>0]=BigInt(d);break;case"float":($(),F)[o>>>2>>>0]=d;break;case"double":($(),X)[o>>>3>>>0]=d;break;case"*":($(),K)[o>>>2>>>0]=d;break;default:ee(`invalid type for setValue: ${m}`)}},t.getValue=function(o,d="i8"){switch(d.endsWith("*")&&(d="*"),d){case"i1":case"i8":return($(),D)[o>>>0];case"i16":return($(),V)[o>>>1>>>0];case"i32":return($(),R)[o>>>2>>>0];case"i64":return($(),le)[o>>>3>>>0];case"float":return($(),F)[o>>>2>>>0];case"double":return($(),X)[o>>>3>>>0];case"*":return($(),K)[o>>>2>>>0];default:ee(`invalid type for getValue: ${d}`)}},t.UTF8ToString=Se,t.stringToUTF8=_t,t.lengthBytesUTF8=Kr;var Ch,Ah,ri,et,mr,on,Oh,Rh,Bh,un,Mh,Nh,ue,gr,Dh,se,ln,oe,Uh,dn,Ph,qh,Lh,pn,Wh,Vh,Gh,Hh,Fh,jh,Kh,Qh,Zh,Yh,Xh,Jh,ef,tf,rf,af,nf,sf,of,uf,lf,df,pf,cf,hf,ff,mf,gf,yf,_f,wf,bf,$f,vf,xf,Sf,Tf,kf,If,Ef,ot,Ny=[Ue,Hr,Vc,Kc,Qc,Zc,Yc,Xc,Jc,eh,th,rh,ih,ah,nh,sh,_h,wh,bh,Sh,Th,kh,Ih,Eh,zh],cn={929356:(o,d,m,c,v)=>{if(t===void 0||!t.Zc)return 1;if((o=Se(Number(o>>>0))).startsWith("./")&&(o=o.substring(2)),!(o=t.Zc.get(o)))return 2;if(d=Number(d>>>0),m=Number(m>>>0),c=Number(c>>>0),d+m>o.byteLength)return 3;try{let T=o.subarray(d,d+m);switch(v){case 0:($(),G).set(T,c>>>0);break;case 1:t.Xd?t.Xd(c,T):t.Ld(c,T);break;default:return 4}return 0}catch{return 4}},930180:(o,d,m)=>{t.xd(o,($(),G).subarray(d>>>0,d+m>>>0))},930244:()=>t.Zd(),930286:o=>{t.vd(o)},930323:()=>{t.Ed()},930354:()=>{t.Fd()},930383:()=>{t.Jd()},930408:o=>t.Dd(o),930441:o=>t.Hd(o),930473:(o,d,m)=>{t.jd(Number(o),Number(d),Number(m),!0)},930536:(o,d,m)=>{t.jd(Number(o),Number(d),Number(m))},930593:()=>typeof wasmOffsetConverter<"u",930650:o=>{t.ac("Abs",o,void 0)},930701:o=>{t.ac("Neg",o,void 0)},930752:o=>{t.ac("Floor",o,void 0)},930805:o=>{t.ac("Ceil",o,void 0)},930857:o=>{t.ac("Reciprocal",o,void 0)},930915:o=>{t.ac("Sqrt",o,void 0)},930967:o=>{t.ac("Exp",o,void 0)},931018:o=>{t.ac("Erf",o,void 0)},931069:o=>{t.ac("Sigmoid",o,void 0)},931124:(o,d,m)=>{t.ac("HardSigmoid",o,{alpha:d,beta:m})},931203:o=>{t.ac("Log",o,void 0)},931254:o=>{t.ac("Sin",o,void 0)},931305:o=>{t.ac("Cos",o,void 0)},931356:o=>{t.ac("Tan",o,void 0)},931407:o=>{t.ac("Asin",o,void 0)},931459:o=>{t.ac("Acos",o,void 0)},931511:o=>{t.ac("Atan",o,void 0)},931563:o=>{t.ac("Sinh",o,void 0)},931615:o=>{t.ac("Cosh",o,void 0)},931667:o=>{t.ac("Asinh",o,void 0)},931720:o=>{t.ac("Acosh",o,void 0)},931773:o=>{t.ac("Atanh",o,void 0)},931826:o=>{t.ac("Tanh",o,void 0)},931878:o=>{t.ac("Not",o,void 0)},931929:(o,d,m)=>{t.ac("Clip",o,{min:d,max:m})},931998:o=>{t.ac("Clip",o,void 0)},932050:(o,d)=>{t.ac("Elu",o,{alpha:d})},932108:o=>{t.ac("Gelu",o,void 0)},932160:o=>{t.ac("Relu",o,void 0)},932212:(o,d)=>{t.ac("LeakyRelu",o,{alpha:d})},932276:(o,d)=>{t.ac("ThresholdedRelu",o,{alpha:d})},932346:(o,d)=>{t.ac("Cast",o,{to:d})},932404:o=>{t.ac("Add",o,void 0)},932455:o=>{t.ac("Sub",o,void 0)},932506:o=>{t.ac("Mul",o,void 0)},932557:o=>{t.ac("Div",o,void 0)},932608:o=>{t.ac("Pow",o,void 0)},932659:o=>{t.ac("Equal",o,void 0)},932712:o=>{t.ac("Greater",o,void 0)},932767:o=>{t.ac("GreaterOrEqual",o,void 0)},932829:o=>{t.ac("Less",o,void 0)},932881:o=>{t.ac("LessOrEqual",o,void 0)},932940:(o,d,m,c,v)=>{t.ac("ReduceMean",o,{keepDims:!!d,noopWithEmptyAxes:!!m,axes:c?Array.from(($(),R).subarray(Number(c)>>>0,Number(v)>>>0)):[]})},933115:(o,d,m,c,v)=>{t.ac("ReduceMax",o,{keepDims:!!d,noopWithEmptyAxes:!!m,axes:c?Array.from(($(),R).subarray(Number(c)>>>0,Number(v)>>>0)):[]})},933289:(o,d,m,c,v)=>{t.ac("ReduceMin",o,{keepDims:!!d,noopWithEmptyAxes:!!m,axes:c?Array.from(($(),R).subarray(Number(c)>>>0,Number(v)>>>0)):[]})},933463:(o,d,m,c,v)=>{t.ac("ReduceProd",o,{keepDims:!!d,noopWithEmptyAxes:!!m,axes:c?Array.from(($(),R).subarray(Number(c)>>>0,Number(v)>>>0)):[]})},933638:(o,d,m,c,v)=>{t.ac("ReduceSum",o,{keepDims:!!d,noopWithEmptyAxes:!!m,axes:c?Array.from(($(),R).subarray(Number(c)>>>0,Number(v)>>>0)):[]})},933812:(o,d,m,c,v)=>{t.ac("ReduceL1",o,{keepDims:!!d,noopWithEmptyAxes:!!m,axes:c?Array.from(($(),R).subarray(Number(c)>>>0,Number(v)>>>0)):[]})},933985:(o,d,m,c,v)=>{t.ac("ReduceL2",o,{keepDims:!!d,noopWithEmptyAxes:!!m,axes:c?Array.from(($(),R).subarray(Number(c)>>>0,Number(v)>>>0)):[]})},934158:(o,d,m,c,v)=>{t.ac("ReduceLogSum",o,{keepDims:!!d,noopWithEmptyAxes:!!m,axes:c?Array.from(($(),R).subarray(Number(c)>>>0,Number(v)>>>0)):[]})},934335:(o,d,m,c,v)=>{t.ac("ReduceSumSquare",o,{keepDims:!!d,noopWithEmptyAxes:!!m,axes:c?Array.from(($(),R).subarray(Number(c)>>>0,Number(v)>>>0)):[]})},934515:(o,d,m,c,v)=>{t.ac("ReduceLogSumExp",o,{keepDims:!!d,noopWithEmptyAxes:!!m,axes:c?Array.from(($(),R).subarray(Number(c)>>>0,Number(v)>>>0)):[]})},934695:o=>{t.ac("Where",o,void 0)},934748:(o,d,m)=>{t.ac("Transpose",o,{perm:d?Array.from(($(),R).subarray(Number(d)>>>0,Number(m)>>>0)):[]})},934872:(o,d,m,c)=>{t.ac("DepthToSpace",o,{blocksize:d,mode:Se(m),format:c?"NHWC":"NCHW"})},935005:(o,d,m,c)=>{t.ac("DepthToSpace",o,{blocksize:d,mode:Se(m),format:c?"NHWC":"NCHW"})},935138:(o,d,m,c,v,T,z,B,W,H,ne,pe,ge,be,bt)=>{t.ac("ConvTranspose",o,{format:W?"NHWC":"NCHW",autoPad:d,dilations:[m],group:c,kernelShape:[v],pads:[T,z],strides:[B],wIsConst:()=>!!($(),D)[H>>>0],outputPadding:ne?Array.from(($(),R).subarray(Number(ne)>>>0,Number(pe)>>>0)):[],outputShape:ge?Array.from(($(),R).subarray(Number(ge)>>>0,Number(be)>>>0)):[],activation:Se(bt)})},935571:(o,d,m,c,v,T,z,B,W,H,ne,pe,ge,be)=>{t.ac("ConvTranspose",o,{format:B?"NHWC":"NCHW",autoPad:d,dilations:Array.from(($(),R).subarray(Number(m)>>>0,2+(Number(m)>>>0)>>>0)),group:c,kernelShape:Array.from(($(),R).subarray(Number(v)>>>0,2+(Number(v)>>>0)>>>0)),pads:Array.from(($(),R).subarray(Number(T)>>>0,4+(Number(T)>>>0)>>>0)),strides:Array.from(($(),R).subarray(Number(z)>>>0,2+(Number(z)>>>0)>>>0)),wIsConst:()=>!!($(),D)[W>>>0],outputPadding:H?Array.from(($(),R).subarray(Number(H)>>>0,Number(ne)>>>0)):[],outputShape:pe?Array.from(($(),R).subarray(Number(pe)>>>0,Number(ge)>>>0)):[],activation:Se(be)})},936232:(o,d,m,c,v,T,z,B,W,H,ne,pe,ge,be,bt)=>{t.ac("ConvTranspose",o,{format:W?"NHWC":"NCHW",autoPad:d,dilations:[m],group:c,kernelShape:[v],pads:[T,z],strides:[B],wIsConst:()=>!!($(),D)[H>>>0],outputPadding:ne?Array.from(($(),R).subarray(Number(ne)>>>0,Number(pe)>>>0)):[],outputShape:ge?Array.from(($(),R).subarray(Number(ge)>>>0,Number(be)>>>0)):[],activation:Se(bt)})},936665:(o,d,m,c,v,T,z,B,W,H,ne,pe,ge,be)=>{t.ac("ConvTranspose",o,{format:B?"NHWC":"NCHW",autoPad:d,dilations:Array.from(($(),R).subarray(Number(m)>>>0,2+(Number(m)>>>0)>>>0)),group:c,kernelShape:Array.from(($(),R).subarray(Number(v)>>>0,2+(Number(v)>>>0)>>>0)),pads:Array.from(($(),R).subarray(Number(T)>>>0,4+(Number(T)>>>0)>>>0)),strides:Array.from(($(),R).subarray(Number(z)>>>0,2+(Number(z)>>>0)>>>0)),wIsConst:()=>!!($(),D)[W>>>0],outputPadding:H?Array.from(($(),R).subarray(Number(H)>>>0,Number(ne)>>>0)):[],outputShape:pe?Array.from(($(),R).subarray(Number(pe)>>>0,Number(ge)>>>0)):[],activation:Se(be)})},937326:(o,d)=>{t.ac("GlobalAveragePool",o,{format:d?"NHWC":"NCHW"})},937417:(o,d,m,c,v,T,z,B,W,H,ne,pe,ge,be)=>{t.ac("AveragePool",o,{format:be?"NHWC":"NCHW",auto_pad:d,ceil_mode:m,count_include_pad:c,storage_order:v,dilations:T?Array.from(($(),R).subarray(Number(T)>>>0,Number(z)>>>0)):[],kernel_shape:B?Array.from(($(),R).subarray(Number(B)>>>0,Number(W)>>>0)):[],pads:H?Array.from(($(),R).subarray(Number(H)>>>0,Number(ne)>>>0)):[],strides:pe?Array.from(($(),R).subarray(Number(pe)>>>0,Number(ge)>>>0)):[]})},937896:(o,d)=>{t.ac("GlobalAveragePool",o,{format:d?"NHWC":"NCHW"})},937987:(o,d,m,c,v,T,z,B,W,H,ne,pe,ge,be)=>{t.ac("AveragePool",o,{format:be?"NHWC":"NCHW",auto_pad:d,ceil_mode:m,count_include_pad:c,storage_order:v,dilations:T?Array.from(($(),R).subarray(Number(T)>>>0,Number(z)>>>0)):[],kernel_shape:B?Array.from(($(),R).subarray(Number(B)>>>0,Number(W)>>>0)):[],pads:H?Array.from(($(),R).subarray(Number(H)>>>0,Number(ne)>>>0)):[],strides:pe?Array.from(($(),R).subarray(Number(pe)>>>0,Number(ge)>>>0)):[]})},938466:(o,d)=>{t.ac("GlobalMaxPool",o,{format:d?"NHWC":"NCHW"})},938553:(o,d,m,c,v,T,z,B,W,H,ne,pe,ge,be)=>{t.ac("MaxPool",o,{format:be?"NHWC":"NCHW",auto_pad:d,ceil_mode:m,count_include_pad:c,storage_order:v,dilations:T?Array.from(($(),R).subarray(Number(T)>>>0,Number(z)>>>0)):[],kernel_shape:B?Array.from(($(),R).subarray(Number(B)>>>0,Number(W)>>>0)):[],pads:H?Array.from(($(),R).subarray(Number(H)>>>0,Number(ne)>>>0)):[],strides:pe?Array.from(($(),R).subarray(Number(pe)>>>0,Number(ge)>>>0)):[]})},939028:(o,d)=>{t.ac("GlobalMaxPool",o,{format:d?"NHWC":"NCHW"})},939115:(o,d,m,c,v,T,z,B,W,H,ne,pe,ge,be)=>{t.ac("MaxPool",o,{format:be?"NHWC":"NCHW",auto_pad:d,ceil_mode:m,count_include_pad:c,storage_order:v,dilations:T?Array.from(($(),R).subarray(Number(T)>>>0,Number(z)>>>0)):[],kernel_shape:B?Array.from(($(),R).subarray(Number(B)>>>0,Number(W)>>>0)):[],pads:H?Array.from(($(),R).subarray(Number(H)>>>0,Number(ne)>>>0)):[],strides:pe?Array.from(($(),R).subarray(Number(pe)>>>0,Number(ge)>>>0)):[]})},939590:(o,d,m,c,v)=>{t.ac("Gemm",o,{alpha:d,beta:m,transA:c,transB:v})},939694:o=>{t.ac("MatMul",o,void 0)},939748:(o,d,m,c)=>{t.ac("ArgMax",o,{keepDims:!!d,selectLastIndex:!!m,axis:c})},939856:(o,d,m,c)=>{t.ac("ArgMin",o,{keepDims:!!d,selectLastIndex:!!m,axis:c})},939964:(o,d)=>{t.ac("Softmax",o,{axis:d})},940027:(o,d)=>{t.ac("Concat",o,{axis:d})},940087:(o,d,m,c,v)=>{t.ac("Split",o,{axis:d,numOutputs:m,splitSizes:c?Array.from(($(),R).subarray(Number(c)>>>0,Number(v)>>>0)):[]})},940243:o=>{t.ac("Expand",o,void 0)},940297:(o,d)=>{t.ac("Gather",o,{axis:Number(d)})},940368:(o,d)=>{t.ac("GatherElements",o,{axis:Number(d)})},940447:(o,d)=>{t.ac("GatherND",o,{batch_dims:Number(d)})},940526:(o,d,m,c,v,T,z,B,W,H,ne)=>{t.ac("Resize",o,{antialias:d,axes:m?Array.from(($(),R).subarray(Number(m)>>>0,Number(c)>>>0)):[],coordinateTransformMode:Se(v),cubicCoeffA:T,excludeOutside:z,extrapolationValue:B,keepAspectRatioPolicy:Se(W),mode:Se(H),nearestMode:Se(ne)})},940888:(o,d,m,c,v,T,z)=>{t.ac("Slice",o,{starts:d?Array.from(($(),R).subarray(Number(d)>>>0,Number(m)>>>0)):[],ends:c?Array.from(($(),R).subarray(Number(c)>>>0,Number(v)>>>0)):[],axes:T?Array.from(($(),R).subarray(Number(T)>>>0,Number(z)>>>0)):[]})},941152:o=>{t.ac("Tile",o,void 0)},941204:(o,d,m)=>{t.ac("InstanceNormalization",o,{epsilon:d,format:m?"NHWC":"NCHW"})},941318:(o,d,m)=>{t.ac("InstanceNormalization",o,{epsilon:d,format:m?"NHWC":"NCHW"})},941432:o=>{t.ac("Range",o,void 0)},941485:(o,d)=>{t.ac("Einsum",o,{equation:Se(d)})},941566:(o,d,m,c,v)=>{t.ac("Pad",o,{mode:d,value:m,pads:c?Array.from(($(),R).subarray(Number(c)>>>0,Number(v)>>>0)):[]})},941709:(o,d,m,c,v,T)=>{t.ac("BatchNormalization",o,{epsilon:d,momentum:m,spatial:!!v,trainingMode:!!c,format:T?"NHWC":"NCHW"})},941878:(o,d,m,c,v,T)=>{t.ac("BatchNormalization",o,{epsilon:d,momentum:m,spatial:!!v,trainingMode:!!c,format:T?"NHWC":"NCHW"})},942047:(o,d,m)=>{t.ac("CumSum",o,{exclusive:Number(d),reverse:Number(m)})},942144:(o,d,m)=>{t.ac("DequantizeLinear",o,{axis:d,blockSize:m})},942234:(o,d,m,c,v)=>{t.ac("GridSample",o,{align_corners:d,mode:Se(m),padding_mode:Se(c),format:v?"NHWC":"NCHW"})},942404:(o,d,m,c,v)=>{t.ac("GridSample",o,{align_corners:d,mode:Se(m),padding_mode:Se(c),format:v?"NHWC":"NCHW"})},942574:(o,d)=>{t.ac("ScatterND",o,{reduction:Se(d)})},942659:(o,d,m,c,v,T,z,B,W)=>{t.ac("Attention",o,{numHeads:d,isUnidirectional:m,maskFilterValue:c,scale:v,doRotary:T,qkvHiddenSizes:z?Array.from(($(),R).subarray(Number(B)>>>0,Number(B)+z>>>0)):[],pastPresentShareBuffer:!!W})},942931:o=>{t.ac("BiasAdd",o,void 0)},942986:o=>{t.ac("BiasSplitGelu",o,void 0)},943047:o=>{t.ac("FastGelu",o,void 0)},943103:(o,d,m,c,v,T,z,B,W,H,ne,pe,ge,be,bt,hn)=>{t.ac("Conv",o,{format:pe?"NHWC":"NCHW",auto_pad:d,dilations:m?Array.from(($(),R).subarray(Number(m)>>>0,Number(c)>>>0)):[],group:v,kernel_shape:T?Array.from(($(),R).subarray(Number(T)>>>0,Number(z)>>>0)):[],pads:B?Array.from(($(),R).subarray(Number(B)>>>0,Number(W)>>>0)):[],strides:H?Array.from(($(),R).subarray(Number(H)>>>0,Number(ne)>>>0)):[],w_is_const:()=>!!($(),D)[Number(ge)>>>0],activation:Se(be),activation_params:bt?Array.from(($(),F).subarray(Number(bt)>>>0,Number(hn)>>>0)):[]})},943687:o=>{t.ac("Gelu",o,void 0)},943739:(o,d,m,c,v,T,z,B,W)=>{t.ac("GroupQueryAttention",o,{numHeads:d,kvNumHeads:m,scale:c,softcap:v,doRotary:T,rotaryInterleaved:z,smoothSoftmax:B,localWindowSize:W})},943956:(o,d,m,c)=>{t.ac("LayerNormalization",o,{axis:d,epsilon:m,simplified:!!c})},944067:(o,d,m,c)=>{t.ac("LayerNormalization",o,{axis:d,epsilon:m,simplified:!!c})},944178:(o,d,m,c,v,T)=>{t.ac("MatMulNBits",o,{k:d,n:m,accuracyLevel:c,bits:v,blockSize:T})},944305:(o,d,m,c,v,T)=>{t.ac("MultiHeadAttention",o,{numHeads:d,isUnidirectional:m,maskFilterValue:c,scale:v,doRotary:T})},944464:(o,d)=>{t.ac("QuickGelu",o,{alpha:d})},944528:(o,d,m,c,v)=>{t.ac("RotaryEmbedding",o,{interleaved:!!d,numHeads:m,rotaryEmbeddingDim:c,scale:v})},944667:(o,d,m)=>{t.ac("SkipLayerNormalization",o,{epsilon:d,simplified:!!m})},944769:(o,d,m)=>{t.ac("SkipLayerNormalization",o,{epsilon:d,simplified:!!m})},944871:(o,d,m,c)=>{t.ac("GatherBlockQuantized",o,{gatherAxis:d,quantizeAxis:m,blockSize:c})},944992:o=>{t.Id(o)},945026:(o,d)=>t.Kd(Number(o),Number(d),t.$c.Nd,t.$c.errors)};function Dy(o,d,m){return hh(async()=>{await t.Gd(Number(o),Number(d),Number(m))})}function Uy(){return typeof wasmOffsetConverter<"u"}function Py(o,d,m,c){var v=oe();try{return Qh(o,d,m,c)}catch(T){if(se(v),T!==T+0)throw T;ue(1,0)}}function qy(o,d,m){var c=oe();try{return Hh(o,d,m)}catch(v){if(se(c),v!==v+0)throw v;ue(1,0)}}function Ly(o,d,m){var c=oe();try{Lh(o,d,m)}catch(v){if(se(c),v!==v+0)throw v;ue(1,0)}}function Wy(o,d){var m=oe();try{return pn(o,d)}catch(c){if(se(m),c!==c+0)throw c;ue(1,0)}}function Vy(o){var d=oe();try{Wh(o)}catch(m){if(se(d),m!==m+0)throw m;ue(1,0)}}function Gy(o,d,m,c,v,T,z){var B=oe();try{return jh(o,d,m,c,v,T,z)}catch(W){if(se(B),W!==W+0)throw W;ue(1,0)}}function Hy(o,d){var m=oe();try{Zh(o,d)}catch(c){if(se(m),c!==c+0)throw c;ue(1,0)}}function Fy(o,d,m,c,v,T){var z=oe();try{Vh(o,d,m,c,v,T)}catch(B){if(se(z),B!==B+0)throw B;ue(1,0)}}function jy(o,d,m,c){var v=oe();try{Kh(o,d,m,c)}catch(T){if(se(v),T!==T+0)throw T;ue(1,0)}}function Ky(o,d,m,c,v){var T=oe();try{Gh(o,d,m,c,v)}catch(z){if(se(T),z!==z+0)throw z;ue(1,0)}}function Qy(o,d,m,c,v,T,z){var B=oe();try{Xh(o,d,m,c,v,T,z)}catch(W){if(se(B),W!==W+0)throw W;ue(1,0)}}function Zy(o,d,m,c,v,T,z){var B=oe();try{Jh(o,d,m,c,v,T,z)}catch(W){if(se(B),W!==W+0)throw W;ue(1,0)}}function Yy(o,d,m,c,v,T,z,B){var W=oe();try{af(o,d,m,c,v,T,z,B)}catch(H){if(se(W),H!==H+0)throw H;ue(1,0)}}function Xy(o,d,m,c,v){var T=oe();try{return Yh(o,d,m,c,v)}catch(z){if(se(T),z!==z+0)throw z;ue(1,0)}}function Jy(o,d,m,c,v,T,z,B){var W=oe();try{nf(o,d,m,c,v,T,z,B)}catch(H){if(se(W),H!==H+0)throw H;ue(1,0)}}function e0(o,d,m,c,v,T,z,B,W,H,ne,pe){var ge=oe();try{ef(o,d,m,c,v,T,z,B,W,H,ne,pe)}catch(be){if(se(ge),be!==be+0)throw be;ue(1,0)}}function t0(o,d,m,c,v,T){var z=oe();try{return tf(o,d,m,c,v,T)}catch(B){if(se(z),B!==B+0)throw B;ue(1,0)}}function r0(o,d,m){var c=oe();try{return sf(o,d,m)}catch(v){if(se(c),v!==v+0)throw v;return ue(1,0),0n}}function i0(o,d,m,c,v,T,z,B,W){var H=oe();try{Fh(o,d,m,c,v,T,z,B,W)}catch(ne){if(se(H),ne!==ne+0)throw ne;ue(1,0)}}function a0(o){var d=oe();try{return of(o)}catch(m){if(se(d),m!==m+0)throw m;ue(1,0)}}function n0(o,d,m){var c=oe();try{return uf(o,d,m)}catch(v){if(se(c),v!==v+0)throw v;ue(1,0)}}function s0(o,d){var m=oe();try{return Sf(o,d)}catch(c){if(se(m),c!==c+0)throw c;return ue(1,0),0n}}function o0(o,d,m,c,v){var T=oe();try{lf(o,d,m,c,v)}catch(z){if(se(T),z!==z+0)throw z;ue(1,0)}}function u0(o){var d=oe();try{return df(o)}catch(m){if(se(d),m!==m+0)throw m;return ue(1,0),0n}}function l0(o,d,m,c,v,T){var z=oe();try{return gf(o,d,m,c,v,T)}catch(B){if(se(z),B!==B+0)throw B;ue(1,0)}}function d0(o,d,m,c,v,T){var z=oe();try{return yf(o,d,m,c,v,T)}catch(B){if(se(z),B!==B+0)throw B;ue(1,0)}}function p0(o,d,m,c,v,T,z,B){var W=oe();try{return rf(o,d,m,c,v,T,z,B)}catch(H){if(se(W),H!==H+0)throw H;ue(1,0)}}function c0(o,d,m,c,v){var T=oe();try{return _f(o,d,m,c,v)}catch(z){if(se(T),z!==z+0)throw z;return ue(1,0),0n}}function h0(o,d,m,c){var v=oe();try{return wf(o,d,m,c)}catch(T){if(se(v),T!==T+0)throw T;ue(1,0)}}function f0(o,d,m,c){var v=oe();try{return bf(o,d,m,c)}catch(T){if(se(v),T!==T+0)throw T;ue(1,0)}}function m0(o,d,m,c,v,T,z,B,W,H,ne,pe){var ge=oe();try{return $f(o,d,m,c,v,T,z,B,W,H,ne,pe)}catch(be){if(se(ge),be!==be+0)throw be;ue(1,0)}}function g0(o,d,m,c,v,T,z,B,W,H,ne){var pe=oe();try{ff(o,d,m,c,v,T,z,B,W,H,ne)}catch(ge){if(se(pe),ge!==ge+0)throw ge;ue(1,0)}}function y0(o,d,m,c,v,T,z,B,W,H,ne,pe,ge,be,bt,hn){var x0=oe();try{mf(o,d,m,c,v,T,z,B,W,H,ne,pe,ge,be,bt,hn)}catch(fn){if(se(x0),fn!==fn+0)throw fn;ue(1,0)}}function _0(o,d,m,c){var v=oe();try{return vf(o,d,m,c)}catch(T){if(se(v),T!==T+0)throw T;ue(1,0)}}function w0(o,d,m,c,v){var T=oe();try{return xf(o,d,m,c,v)}catch(z){if(se(T),z!==z+0)throw z;ue(1,0)}}function b0(o,d,m){var c=oe();try{return pf(o,d,m)}catch(v){if(se(c),v!==v+0)throw v;ue(1,0)}}function $0(o,d,m){var c=oe();try{return cf(o,d,m)}catch(v){if(se(c),v!==v+0)throw v;ue(1,0)}}function v0(o,d,m,c){var v=oe();try{hf(o,d,m,c)}catch(T){if(se(v),T!==T+0)throw T;ue(1,0)}}function ii(){if(0<De)Re=ii;else if(a)w==null||w(t),J();else{for(var o=Gr;0<o.length;)o.shift()(t);0<De?Re=ii:(t.calledRun=!0,A||(J(),w==null||w(t)))}}return a||(ot=await ht(),ii()),t.PTR_SIZE=4,U?t:new Promise((o,d)=>{w=o,S=d})}var Dn,Un,Xf=q(()=>{var e,t;Dn=Nn,Un=(t=(e=globalThis.self)==null?void 0:e.name)==null?void 0:t.startsWith("em-pthread"),Un&&Nn()}),ci,hi,Pn,Me,qn,$r,Ln,Wn,fi,Vn,mi,Gn,gi,Hn,yi=q(()=>{li(),ci=typeof location>"u"?void 0:location.origin,hi=self.location.href>"file:"&&self.location.href<"file;",Pn=()=>{{if(hi){let e=URL;return new URL(new e("ort.bundle.min.mjs",self.location.href).href,ci).href}return self.location.href}},Me=Pn(),qn=()=>{if(Me&&!Me.startsWith("blob:"))return Me.substring(0,Me.lastIndexOf("/")+1)},$r=(e,t)=>{try{let r=t??Me;return(r?new URL(e,r):new URL(e)).origin===ci}catch{return!1}},Ln=(e,t)=>{let r=t??Me;try{return(r?new URL(e,r):new URL(e)).href}catch{return}},Wn=(e,t)=>`${t??"./"}${e}`,fi=async e=>{let t=await(await fetch(e,{credentials:"same-origin"})).blob();return URL.createObjectURL(t)},Vn=async e=>(await import(e)).default,mi=(Yf(),jt(Rn)).default,Gn=async()=>{if(!Me)throw new Error("Failed to load proxy worker: cannot determine the script source URL.");if($r(Me))return[void 0,mi()];let e=await fi(Me);return[e,mi(e)]},gi=(Xf(),jt(Mn)).default,Hn=async(e,t,r,i)=>{let a=gi&&!(e||t);if(a)if(Me)a=$r(Me)||i&&!r;else if(i&&!r)a=!0;else throw new Error("cannot determine the script source URL.");if(a)return[void 0,gi];{let n="ort-wasm-simd-threaded.jsep.mjs",s=e??Ln(n,t),u=r&&s&&!$r(s,t),l=u?await fi(s):s??Wn(n,t);return[u?l:void 0,await Vn(l)]}}}),_i,vr,Zt,wi,Fn,jn,Kn,bi,_e,St=q(()=>{yi(),vr=!1,Zt=!1,wi=!1,Fn=()=>{if(typeof SharedArrayBuffer>"u")return!1;try{return typeof MessageChannel<"u"&&new MessageChannel().port1.postMessage(new SharedArrayBuffer(1)),WebAssembly.validate(new Uint8Array([0,97,115,109,1,0,0,0,1,4,1,96,0,0,3,2,1,0,5,4,1,3,1,1,10,11,1,9,0,65,0,254,16,2,0,26,11]))}catch{return!1}},jn=()=>{try{return WebAssembly.validate(new Uint8Array([0,97,115,109,1,0,0,0,1,4,1,96,0,0,3,2,1,0,10,30,1,28,0,65,0,253,15,253,12,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,253,186,1,26,11]))}catch{return!1}},Kn=()=>{try{return WebAssembly.validate(new Uint8Array([0,97,115,109,1,0,0,0,1,5,1,96,0,1,123,3,2,1,0,10,19,1,17,0,65,1,253,15,65,2,253,15,65,3,253,15,253,147,2,11]))}catch{return!1}},bi=async e=>{if(vr)return Promise.resolve();if(Zt)throw new Error("multiple calls to 'initializeWebAssembly()' detected.");if(wi)throw new Error("previous call to 'initializeWebAssembly()' failed.");Zt=!0;let t=e.initTimeout,r=e.numThreads;if(e.simd!==!1){if(e.simd==="relaxed"){if(!Kn())throw new Error("Relaxed WebAssembly SIMD is not supported in the current environment.")}else if(!jn())throw new Error("WebAssembly SIMD is not supported in the current environment.")}let i=Fn();r>1&&!i&&(typeof self<"u"&&!self.crossOriginIsolated&&console.warn("env.wasm.numThreads is set to "+r+", but this will not work unless you enable crossOriginIsolated mode. See https://web.dev/cross-origin-isolation-guide/ for more info."),console.warn("WebAssembly multi-threading is not supported in the current environment. Falling back to single-threading."),e.numThreads=r=1);let a=e.wasmPaths,n=typeof a=="string"?a:void 0,s=a==null?void 0:a.mjs,u=(s==null?void 0:s.href)??s,l=a==null?void 0:a.wasm,p=(l==null?void 0:l.href)??l,h=e.wasmBinary,[f,g]=await Hn(u,n,r>1,!!h||!!p),y=!1,_=[];if(t>0&&_.push(new Promise(w=>{setTimeout(()=>{y=!0,w()},t)})),_.push(new Promise((w,S)=>{let x={numThreads:r};if(h)x.wasmBinary=h,x.locateFile=b=>b;else if(p||n)x.locateFile=b=>p??n+b;else if(u&&u.indexOf("blob:")!==0)x.locateFile=b=>new URL(b,u).href;else if(f){let b=qn();b&&(x.locateFile=I=>b+I)}g(x).then(b=>{Zt=!1,vr=!0,_i=b,w(),f&&URL.revokeObjectURL(f)},b=>{Zt=!1,wi=!0,S(b)})})),await Promise.race(_),y)throw new Error(`WebAssembly backend initializing failed due to timeout: ${t}ms`)},_e=()=>{if(vr&&_i)return _i;throw new Error("WebAssembly is not initialized yet.")}}),We,xr,fe,$i=q(()=>{St(),We=(e,t)=>{let r=_e(),i=r.lengthBytesUTF8(e)+1,a=r._malloc(i);return r.stringToUTF8(e,a,i),t.push(a),a},xr=(e,t,r,i)=>{if(typeof e=="object"&&e!==null){if(r.has(e))throw new Error("Circular reference in options");r.add(e)}Object.entries(e).forEach(([a,n])=>{let s=t?t+a:a;if(typeof n=="object")xr(n,s+".",r,i);else if(typeof n=="string"||typeof n=="number")i(s,n.toString());else if(typeof n=="boolean")i(s,n?"1":"0");else throw new Error(`Can't handle extra config type: ${typeof n}`)})},fe=e=>{let t=_e(),r=t.stackSave();try{let i=t.PTR_SIZE,a=t.stackAlloc(2*i);t._OrtGetLastError(a,a+i);let n=Number(t.getValue(a,i===4?"i32":"i64")),s=t.getValue(a+i,"*"),u=s?t.UTF8ToString(s):"";throw new Error(`${e} ERROR_CODE: ${n}, ERROR_MESSAGE: ${u}`)}finally{t.stackRestore(r)}}}),Qn,Jf=q(()=>{St(),$i(),Qn=e=>{let t=_e(),r=0,i=[],a=e||{};try{if((e==null?void 0:e.logSeverityLevel)===void 0)a.logSeverityLevel=2;else if(typeof e.logSeverityLevel!="number"||!Number.isInteger(e.logSeverityLevel)||e.logSeverityLevel<0||e.logSeverityLevel>4)throw new Error(`log severity level is not valid: ${e.logSeverityLevel}`);if((e==null?void 0:e.logVerbosityLevel)===void 0)a.logVerbosityLevel=0;else if(typeof e.logVerbosityLevel!="number"||!Number.isInteger(e.logVerbosityLevel))throw new Error(`log verbosity level is not valid: ${e.logVerbosityLevel}`);(e==null?void 0:e.terminate)===void 0&&(a.terminate=!1);let n=0;return(e==null?void 0:e.tag)!==void 0&&(n=We(e.tag,i)),r=t._OrtCreateRunOptions(a.logSeverityLevel,a.logVerbosityLevel,!!a.terminate,n),r===0&&fe("Can't create run options."),(e==null?void 0:e.extra)!==void 0&&xr(e.extra,"",new WeakSet,(s,u)=>{let l=We(s,i),p=We(u,i);t._OrtAddRunConfigEntry(r,l,p)!==0&&fe(`Can't set a run config entry: ${s} - ${u}.`)}),[r,i]}catch(n){throw r!==0&&t._OrtReleaseRunOptions(r),i.forEach(s=>t._free(s)),n}}}),Zn,Yn,Xn,Yt,Jn,es,em=q(()=>{St(),$i(),Zn=e=>{switch(e){case"disabled":return 0;case"basic":return 1;case"extended":return 2;case"layout":return 3;case"all":return 99;default:throw new Error(`unsupported graph optimization level: ${e}`)}},Yn=e=>{switch(e){case"sequential":return 0;case"parallel":return 1;default:throw new Error(`unsupported execution mode: ${e}`)}},Xn=e=>{e.extra||(e.extra={}),e.extra.session||(e.extra.session={});let t=e.extra.session;t.use_ort_model_bytes_directly||(t.use_ort_model_bytes_directly="1"),e.executionProviders&&e.executionProviders.some(r=>(typeof r=="string"?r:r.name)==="webgpu")&&(e.enableMemPattern=!1)},Yt=(e,t,r,i)=>{let a=We(t,i),n=We(r,i);_e()._OrtAddSessionConfigEntry(e,a,n)!==0&&fe(`Can't set a session config entry: ${t} - ${r}.`)},Jn=async(e,t,r)=>{let i=t.executionProviders;for(let a of i){let n=typeof a=="string"?a:a.name,s=[];switch(n){case"webnn":if(n="WEBNN",typeof a!="string"){let f=a==null?void 0:a.deviceType;f&&Yt(e,"deviceType",f,r)}break;case"webgpu":if(n="JS",typeof a!="string"){let f=a;if(f!=null&&f.preferredLayout){if(f.preferredLayout!=="NCHW"&&f.preferredLayout!=="NHWC")throw new Error(`preferredLayout must be either 'NCHW' or 'NHWC': ${f.preferredLayout}`);Yt(e,"preferredLayout",f.preferredLayout,r)}}break;case"wasm":case"cpu":continue;default:throw new Error(`not supported execution provider: ${n}`)}let u=We(n,r),l=s.length,p=0,h=0;if(l>0){p=_e()._malloc(l*_e().PTR_SIZE),r.push(p),h=_e()._malloc(l*_e().PTR_SIZE),r.push(h);for(let f=0;f<l;f++)_e().setValue(p+f*_e().PTR_SIZE,s[f][0],"*"),_e().setValue(h+f*_e().PTR_SIZE,s[f][1],"*")}await _e()._OrtAppendExecutionProvider(e,u,p,h,l)!==0&&fe(`Can't append execution provider: ${n}.`)}},es=async e=>{let t=_e(),r=0,i=[],a=e||{};Xn(a);try{let n=Zn(a.graphOptimizationLevel??"all"),s=Yn(a.executionMode??"sequential"),u=typeof a.logId=="string"?We(a.logId,i):0,l=a.logSeverityLevel??2;if(!Number.isInteger(l)||l<0||l>4)throw new Error(`log severity level is not valid: ${l}`);let p=a.logVerbosityLevel??0;if(!Number.isInteger(p)||p<0||p>4)throw new Error(`log verbosity level is not valid: ${p}`);let h=typeof a.optimizedModelFilePath=="string"?We(a.optimizedModelFilePath,i):0;if(r=t._OrtCreateSessionOptions(n,!!a.enableCpuMemArena,!!a.enableMemPattern,s,!!a.enableProfiling,0,u,l,p,h),r===0&&fe("Can't create session options."),a.executionProviders&&await Jn(r,a,i),a.enableGraphCapture!==void 0){if(typeof a.enableGraphCapture!="boolean")throw new Error(`enableGraphCapture must be a boolean value: ${a.enableGraphCapture}`);Yt(r,"enableGraphCapture",a.enableGraphCapture.toString(),i)}if(a.freeDimensionOverrides)for(let[f,g]of Object.entries(a.freeDimensionOverrides)){if(typeof f!="string")throw new Error(`free dimension override name must be a string: ${f}`);if(typeof g!="number"||!Number.isInteger(g)||g<0)throw new Error(`free dimension override value must be a non-negative integer: ${g}`);let y=We(f,i);t._OrtAddFreeDimensionOverride(r,y,g)!==0&&fe(`Can't set a free dimension override: ${f} - ${g}.`)}return a.extra!==void 0&&xr(a.extra,"",new WeakSet,(f,g)=>{Yt(r,f,g,i)}),[r,i]}catch(n){throw r!==0&&t._OrtReleaseSessionOptions(r)!==0&&fe("Can't release session options."),i.forEach(s=>t._free(s)),n}}}),Tt,it,kt,Sr,Tr,vi,xi,Si,te=q(()=>{Tt=e=>{switch(e){case"int8":return 3;case"uint8":return 2;case"bool":return 9;case"int16":return 5;case"uint16":return 4;case"int32":return 6;case"uint32":return 12;case"float16":return 10;case"float32":return 1;case"float64":return 11;case"string":return 8;case"int64":return 7;case"uint64":return 13;case"int4":return 22;case"uint4":return 21;default:throw new Error(`unsupported data type: ${e}`)}},it=e=>{switch(e){case 3:return"int8";case 2:return"uint8";case 9:return"bool";case 5:return"int16";case 4:return"uint16";case 6:return"int32";case 12:return"uint32";case 10:return"float16";case 1:return"float32";case 11:return"float64";case 8:return"string";case 7:return"int64";case 13:return"uint64";case 22:return"int4";case 21:return"uint4";default:throw new Error(`unsupported data type: ${e}`)}},kt=(e,t)=>{let r=[-1,4,1,1,2,2,4,8,-1,1,2,8,4,8,-1,-1,-1,-1,-1,-1,-1,.5,.5][e],i=typeof t=="number"?t:t.reduce((a,n)=>a*n,1);return r>0?Math.ceil(i*r):void 0},Sr=e=>{switch(e){case"float16":return typeof Float16Array<"u"&&Float16Array.from?Float16Array:Uint16Array;case"float32":return Float32Array;case"uint8":return Uint8Array;case"int8":return Int8Array;case"uint16":return Uint16Array;case"int16":return Int16Array;case"int32":return Int32Array;case"bool":return Uint8Array;case"float64":return Float64Array;case"uint32":return Uint32Array;case"int64":return BigInt64Array;case"uint64":return BigUint64Array;default:throw new Error(`unsupported type: ${e}`)}},Tr=e=>{switch(e){case"verbose":return 0;case"info":return 1;case"warning":return 2;case"error":return 3;case"fatal":return 4;default:throw new Error(`unsupported logging level: ${e}`)}},vi=e=>e==="float32"||e==="float16"||e==="int32"||e==="int64"||e==="uint32"||e==="uint8"||e==="bool"||e==="uint4"||e==="int4",xi=e=>e==="float32"||e==="float16"||e==="int32"||e==="int64"||e==="uint32"||e==="uint64"||e==="int8"||e==="uint8"||e==="bool"||e==="uint4"||e==="int4",Si=e=>{switch(e){case"none":return 0;case"cpu":return 1;case"cpu-pinned":return 2;case"texture":return 3;case"gpu-buffer":return 4;case"ml-tensor":return 5;default:throw new Error(`unsupported data location: ${e}`)}}}),Ti,ts=q(()=>{li(),Ti=async e=>{if(typeof e=="string"){let t=await fetch(e);if(!t.ok)throw new Error(`failed to load external data file: ${e}`);let r=t.headers.get("Content-Length"),i=r?parseInt(r,10):0;if(i<1073741824)return new Uint8Array(await t.arrayBuffer());{if(!t.body)throw new Error(`failed to load external data file: ${e}, no response body.`);let a=t.body.getReader(),n;try{n=new ArrayBuffer(i)}catch(u){if(u instanceof RangeError){let l=Math.ceil(i/65536);n=new WebAssembly.Memory({initial:l,maximum:l}).buffer}else throw u}let s=0;for(;;){let{done:u,value:l}=await a.read();if(u)break;let p=l.byteLength;new Uint8Array(n,s,p).set(l),s+=p}return new Uint8Array(n,0,i)}}else return e instanceof Blob?new Uint8Array(await e.arrayBuffer()):e instanceof Uint8Array?e:new Uint8Array(e)}}),rs,is,as,ns,ki,ss,de,at=q(()=>{te(),rs=["V","I","W","E","F"],is=(e,t)=>{console.log(`[${rs[e]},${new Date().toISOString()}]${t}`)},ki=(e,t)=>{as=e,ns=t},ss=(e,t)=>{let r=Tr(e),i=Tr(as);r>=i&&is(r,typeof t=="function"?t():t)},de=(...e)=>{ns&&ss(...e)}}),os,Lt,O,kr,us,ls,ds,re=q(()=>{os=class{static calcMatMulShape(e,t){return e[1]!==t[0]?void 0:[e[0],t[1]]}},Lt=class{static calcShape(e,t,r=!1){let i=e.length,a=t.length;if(i===0)return t;if(a===0)return e;let n=Math.max(e.length,t.length),s=new Array(n);if(r){if(i<2||a<2)return;let u=os.calcMatMulShape([e[i-2],e[i-1]],[t[a-2],t[a-1]]);if(u===void 0)return;[s[n-2],s[n-1]]=u}for(let u=r?3:1;u<=n;u++){let l=i-u<0?1:e[i-u],p=a-u<0?1:t[a-u];if(l!==p&&l>1&&p>1)return;let h=Math.max(l,p);if(l&&p)s[n-u]=Math.max(l,p);else{if(h>1)return;s[n-u]=0}}return s}static isValidBroadcast(e,t){let r=e.length,i=t.length;if(r>i)return!1;for(let a=1;a<=r;a++)if(e[r-a]!==1&&e[r-a]!==t[i-a])return!1;return!0}},O=class ai{static size(t){return ai.getSizeFromDimensionRange(t,0,t.length)}static convertShape(t,r=4){let i=t.length;if(i===0)return[];let a=new Array(i),n=i-1;for(;n>=0;){if(t[n]%r===0){a[n]=t[n]/r;break}if(r%t[n]!==0)throw new Error("cannot convert shape");a[n]=1,r/=t[n],n--}for(n--;n>=0;n--)a[n]=t[n];return a}static sizeFromDimension(t,r){if(r<0||r>t.length)throw new Error(`invalid dimension of ${r} for sizeFromDimension as Tensor has ${t.length} dimensions.`);return ai.getSizeFromDimensionRange(t,r,t.length)}static sizeToDimension(t,r){if(r<0||r>t.length)throw new Error(`invalid dimension of ${r} for sizeToDimension as Tensor has ${t.length} dimensions.`);return ai.getSizeFromDimensionRange(t,0,r)}static getSizeFromDimensionRange(t,r,i){let a=1;for(let n=r;n<i;n++){if(t[n]<0)throw new Error("cannot get valid size from specified dimension range. Most likely the range contains negative values in them.");a*=Number(t[n])}return a}static computeStrides(t){let r=t.length;if(r===0)return[];if(r===1)return[1];let i=new Array(r);i[r-1]=1,i[r-2]=t[r-1];for(let a=r-3;a>=0;--a)i[a]=i[a+1]*t[a+1];return i}static normalizeAxis(t,r){if(t<-r&&t>=r)throw new Error("unsupported axis for this operation.");return t<0?t+r:t}static normalizeAxes(t,r){return t.map(i=>this.normalizeAxis(i,r??t.length))}static sortBasedOnPerm(t,r){return r?r.map(i=>t[i]):t.slice().reverse()}static padShape(t,r){let i=t.length;return t.map((a,n)=>a+r[n]+r[n+i])}static areEqual(t,r){return t.length!==r.length?!1:t.every((i,a)=>i===r[a])}},kr=class yr{static adjustPoolAttributes(t,r,i,a,n,s){if(!t&&i.length!==r.length-2)throw new Error("length of specified kernel shapes should be 2 less than length of input dimensions");if(t)for(let u=0;u<r.length-2;u++)u>=i.length?i.push(r[u+2]):i[u]=r[u+2];for(let u=0;u<i.length;u++)if(u<a.length){if(a[u]<0)throw new Error("strides should be greater than or equal to 1")}else a.push(1);for(let u=0;u<i.length;u++)if(u<n.length){if(n[u]<0)throw new Error("dilations should be greater than or equal to 1")}else n.push(1);for(let u=0;u<i.length*2;u++)if(u<s.length){if(s[u]<0)throw new Error("pad should be greater than or equal to 1")}else s.push(0);for(let u=0;u<i.length;u++){if(i[u]<=0)throw new Error("kernel shapes need to be greater than 0");if(s[u]>=i[u]||s[u+i.length]>=i[u])throw new Error("pads should be smaller than kernel")}}static adjustPadsBasedOnAutoPad(t,r,i,a,n,s,u){if(u){if(n.length!==2*(t.length-2))throw new Error("length of pads should be twice the length of data dimensions");if(r.length!==t.length-2)throw new Error("length of strides should be the length of data dimensions");if(a.length!==t.length-2)throw new Error("length of kernel shapes should be the length of data dimensions");for(let l=0;l<t.length-2;l++)yr.adjustPadAndReturnShape(t[l+(s?1:2)],r[l],i[l],a[l],n,l,l+t.length-2,u)}}static computePoolOutputShape(t,r,i,a,n,s,u){if(r.length<=0)throw new Error("input shape must be of size greater than 0");let l=[r[0],r[1]];return yr.computeShapeHelper(t,r,l,i,a,n,s,u),l}static computeConvOutputShape(t,r,i,a,n,s,u){if(t.length<=0||r.length<=0)throw new Error("invalid input tensor dims or invalid filter tensor dims");let l=[t[0],r[0]];return yr.computeShapeHelper(!1,t,l,i,a,n,s,u),l}static computeShapeHelper(t,r,i,a,n,s,u,l){if(t)for(let p=0;p<r.length-2;p++)i.push(1);else for(let p=0;p<r.length-2;p++)i.push(yr.adjustPadAndReturnShape(r[p+2],a[p],n[p],s[p],u,p,p+r.length-2,l))}static adjustPadAndReturnShape(t,r,i,a,n,s,u,l){let p=i*(a-1)+1;if(l&&l!=="NOTSET")switch(l){case"VALID":return n[s]=0,n[u]=0,Math.floor((t-p)/r+1);case"SAME_LOWER":case"SAME_UPPER":if(i!==1)throw new Error("Dilation not supported for SAME_UPPER or SAME_LOWER");{let h=((t+r-1)/r-1)*r+a-t;return n[s]=Math.floor(l==="SAME_LOWER"?(h+1)/2:h/2),n[u]=h-n[s],Math.floor((t+h-a)/r+1)}default:throw new Error("Unsupported AutoPad type")}else return Math.floor((t+n[s]+n[u]-p)/r+1)}},us=class{static getShapeOfGemmResult(e,t,r,i,a){if(e.length!==2||r.length!==2)throw new Error("shape need to be of size 2");let n,s,u;t?(n=e[1],s=e[0]):(n=e[0],s=e[1]);let l=-1;if(i?(u=r[0],l=1):(u=r[1],l=0),r[l]!==s)throw new Error("dimension mismatch");if(n<=0||u<=0||s<=0)throw new Error("invalid shape specified");if(a&&!Lt.isValidBroadcast(a,[n,u]))throw new Error("gemm: invalid bias shape for broadcast");return[n,u,s]}},ls=-34028234663852886e22,ds=34028234663852886e22}),Ii,ps=q(()=>{te(),Ii=(e,t)=>new(Sr(t))(e)}),Ei,zi,Ci,cs,Ai,hs,Oi,Ri,Bi,fs,ms,tm=q(()=>{te(),at(),Ei=new Map([["float32",32],["float16",16],["int32",32],["uint32",32],["int64",64],["uint64",64],["int8",8],["uint8",8],["int4",4],["uint4",4]]),zi=(e,t)=>{if(t==="int32")return e;let r=Ei.get(t);if(!r)throw new Error(`WebNN backend does not support data type: ${t}`);let i=r/8;if(e.byteLength%i!==0)throw new Error(`Invalid Uint8Array length - must be a multiple of ${i}.`);let a=e.byteLength/i,n=new(Sr(t))(e.buffer,e.byteOffset,a);switch(t){case"int64":case"uint64":{let s=new Int32Array(a);for(let u=0;u<a;u++){let l=n[u];if(l>2147483647n||l<-2147483648n)throw new Error("Can not convert int64 data to int32 - value out of range.");s[u]=Number(l)}return new Uint8Array(s.buffer)}case"int8":case"uint8":case"uint32":{if(t==="uint32"&&n.some(u=>u>2147483647))throw new Error("Can not convert uint32 data to int32 - value out of range.");let s=Int32Array.from(n,Number);return new Uint8Array(s.buffer)}default:throw new Error(`Unsupported data conversion from ${t} to 'int32'`)}},Ci=(e,t)=>{if(t==="int32")return e;if(e.byteLength%4!==0)throw new Error("Invalid Uint8Array length - must be a multiple of 4 (int32).");let r=e.byteLength/4,i=new Int32Array(e.buffer,e.byteOffset,r);switch(t){case"int64":{let a=BigInt64Array.from(i,BigInt);return new Uint8Array(a.buffer)}case"uint64":{if(i.some(n=>n<0))throw new Error("Can not convert int32 data to uin64 - negative value found.");let a=BigUint64Array.from(i,BigInt);return new Uint8Array(a.buffer)}case"int8":{if(i.some(n=>n<-128||n>127))throw new Error("Can not convert int32 data to int8 - value out of range.");let a=Int8Array.from(i,Number);return new Uint8Array(a.buffer)}case"uint8":{if(i.some(a=>a<0||a>255))throw new Error("Can not convert int32 data to uint8 - value out of range.");return Uint8Array.from(i,Number)}case"uint32":{if(i.some(n=>n<0))throw new Error("Can not convert int32 data to uint32 - negative value found.");let a=Uint32Array.from(i,Number);return new Uint8Array(a.buffer)}default:throw new Error(`Unsupported data conversion from 'int32' to ${t}`)}},cs=1,Ai=()=>cs++,hs=new Map([["int8","int32"],["uint8","int32"],["uint32","int32"],["int64","int32"]]),Oi=(e,t)=>{let r=Ei.get(e);if(!r)throw new Error(`WebNN backend does not support data type: ${e}`);return t.length>0?Math.ceil(t.reduce((i,a)=>i*a)*r/8):0},Ri=class{constructor(e){this.isDataConverted=!1;let{sessionId:t,context:r,tensor:i,dataType:a,shape:n,fallbackDataType:s}=e;this.sessionId=t,this.mlContext=r,this.mlTensor=i,this.dataType=a,this.tensorShape=n,this.fallbackDataType=s}get tensor(){return this.mlTensor}get type(){return this.dataType}get fallbackType(){return this.fallbackDataType}get shape(){return this.tensorShape}get byteLength(){return Oi(this.dataType,this.tensorShape)}destroy(){de("verbose",()=>"[WebNN] TensorWrapper.destroy"),this.mlTensor.destroy()}write(e){this.mlContext.writeTensor(this.mlTensor,e)}async read(e){if(this.fallbackDataType){let t=await this.mlContext.readTensor(this.mlTensor),r=Ci(new Uint8Array(t),this.dataType);if(e){(e instanceof ArrayBuffer?new Uint8Array(e):new Uint8Array(e.buffer,e.byteOffset,e.byteLength)).set(r);return}else return r.buffer}else return e?this.mlContext.readTensor(this.mlTensor,e):this.mlContext.readTensor(this.mlTensor)}canReuseTensor(e,t,r){return this.mlContext===e&&this.dataType===t&&this.tensorShape.length===r.length&&this.tensorShape.every((i,a)=>i===r[a])}setIsDataConverted(e){this.isDataConverted=e}},Bi=class{constructor(e,t){this.tensorManager=e,this.wrapper=t}get tensorWrapper(){return this.wrapper}releaseTensor(){this.tensorWrapper&&(this.tensorManager.releaseTensor(this.tensorWrapper),this.wrapper=void 0)}async ensureTensor(e,t,r,i){let a=this.tensorManager.getMLContext(e),n=this.tensorManager.getMLOpSupportLimits(e),s;if(!(n!=null&&n.input.dataTypes.includes(t))){if(s=hs.get(t),!s||(n==null?void 0:n.input.dataTypes.includes(s)))throw new Error(`WebNN backend does not support data type: ${t}`);de("verbose",()=>`[WebNN] TensorIdTracker.ensureTensor: fallback dataType from ${t} to ${s}`)}if(this.wrapper){if(this.wrapper.canReuseTensor(a,t,r))return this.wrapper.tensor;if(i){if(this.wrapper.byteLength!==Oi(t,r))throw new Error("Unable to copy data to tensor with different size.");this.activeUpload=new Uint8Array(await this.wrapper.read())}this.tensorManager.releaseTensor(this.wrapper)}let u=typeof MLTensorUsage>"u"?void 0:MLTensorUsage.READ|MLTensorUsage.WRITE;return this.wrapper=await this.tensorManager.getCachedTensor(e,t,r,u,!0,!0,s),i&&this.activeUpload&&(this.wrapper.write(this.activeUpload),this.activeUpload=void 0),this.wrapper.tensor}upload(e){let t=e;if(this.wrapper){if(this.wrapper.fallbackType)if(this.wrapper.fallbackType==="int32")t=zi(e,this.wrapper.type),this.wrapper.setIsDataConverted(!0);else throw new Error(`Unsupported fallback data type: ${this.wrapper.fallbackType}`);if(e.byteLength===this.wrapper.byteLength){this.wrapper.write(t);return}else de("verbose",()=>"Data size does not match tensor size. Releasing tensor."),this.releaseTensor()}this.activeUpload?this.activeUpload.set(t):this.activeUpload=new Uint8Array(t)}async download(e){var t,r;if(this.activeUpload){let i=(t=this.wrapper)!=null&&t.isDataConverted?Ci(this.activeUpload,(r=this.wrapper)==null?void 0:r.type):this.activeUpload;if(e){e instanceof ArrayBuffer?new Uint8Array(e).set(i):new Uint8Array(e.buffer,e.byteOffset,e.byteLength).set(i);return}else return i.buffer}if(!this.wrapper)throw new Error("Tensor has not been created.");return e?this.wrapper.read(e):this.wrapper.read()}},fs=class{constructor(e){this.backend=e,this.tensorTrackersById=new Map,this.freeTensors=[],this.externalTensors=new Set}getMLContext(e){let t=this.backend.getMLContext(e);if(!t)throw new Error("MLContext not found for session.");return t}getMLOpSupportLimits(e){return this.backend.getMLOpSupportLimits(e)}reserveTensorId(){let e=Ai();return this.tensorTrackersById.set(e,new Bi(this)),e}releaseTensorId(e){let t=this.tensorTrackersById.get(e);t&&(this.tensorTrackersById.delete(e),t.tensorWrapper&&this.releaseTensor(t.tensorWrapper))}async ensureTensor(e,t,r,i,a){de("verbose",()=>`[WebNN] TensorManager.ensureTensor {tensorId: ${t}, dataType: ${r}, shape: ${i}, copyOld: ${a}}`);let n=this.tensorTrackersById.get(t);if(!n)throw new Error("Tensor not found.");return n.ensureTensor(e,r,i,a)}upload(e,t){let r=this.tensorTrackersById.get(e);if(!r)throw new Error("Tensor not found.");r.upload(t)}async download(e,t){de("verbose",()=>`[WebNN] TensorManager.download {tensorId: ${e}, dstBuffer: ${t==null?void 0:t.byteLength}}`);let r=this.tensorTrackersById.get(e);if(!r)throw new Error("Tensor not found.");return r.download(t)}releaseTensorsForSession(e){for(let t of this.freeTensors)t.sessionId===e&&t.destroy();this.freeTensors=this.freeTensors.filter(t=>t.sessionId!==e)}registerTensor(e,t,r,i){let a=this.getMLContext(e),n=Ai(),s=new Ri({sessionId:e,context:a,tensor:t,dataType:r,shape:i});return this.tensorTrackersById.set(n,new Bi(this,s)),this.externalTensors.add(s),n}async getCachedTensor(e,t,r,i,a,n,s){let u=this.getMLContext(e);for(let[p,h]of this.freeTensors.entries())if(h.canReuseTensor(u,t,r)){de("verbose",()=>`[WebNN] Reusing tensor {dataType: ${t}, ${s?`fallbackDataType: ${s},`:""} shape: ${r}`);let f=this.freeTensors.splice(p,1)[0];return f.sessionId=e,f}de("verbose",()=>`[WebNN] MLContext.createTensor {dataType: ${t}, ${s?`fallbackDataType: ${s},`:""} shape: ${r}}`);let l=await u.createTensor({dataType:s??t,shape:r,dimensions:r,usage:i,writable:a,readable:n});return new Ri({sessionId:e,context:u,tensor:l,dataType:t,shape:r,fallbackDataType:s})}releaseTensor(e){this.externalTensors.has(e)&&this.externalTensors.delete(e),this.freeTensors.push(e)}},ms=(...e)=>new fs(...e)}),Xt,gs,ys,rm=q(()=>{te(),St(),ps(),tm(),at(),Xt=new Map([[1,"float32"],[10,"float16"],[6,"int32"],[12,"uint32"],[7,"int64"],[13,"uint64"],[22,"int4"],[21,"uint4"],[3,"int8"],[2,"uint8"],[9,"uint8"]]),gs=(e,t)=>{if(e===t)return!0;if(e===void 0||t===void 0)return!1;let r=Object.keys(e).sort(),i=Object.keys(t).sort();return r.length===i.length&&r.every((a,n)=>a===i[n]&&e[a]===t[a])},ys=class{constructor(e){this.tensorManager=ms(this),this.mlContextBySessionId=new Map,this.sessionIdsByMLContext=new Map,this.mlContextCache=[],this.sessionGraphInputs=new Map,this.sessionGraphOutputs=new Map,this.temporaryGraphInputs=[],this.temporaryGraphOutputs=[],this.temporarySessionTensorIds=new Map,this.mlOpSupportLimitsBySessionId=new Map,ki(e.logLevel,!!e.debug)}get currentSessionId(){if(this.activeSessionId===void 0)throw new Error("No active session");return this.activeSessionId}onRunStart(e){de("verbose",()=>`[WebNN] onRunStart {sessionId: ${e}}`),this.activeSessionId=e}onRunEnd(e){de("verbose",()=>`[WebNN] onRunEnd {sessionId: ${e}}`);let t=this.temporarySessionTensorIds.get(e);if(t){for(let r of t)de("verbose",()=>`[WebNN] releasing temporary tensor {tensorId: ${r}}`),this.tensorManager.releaseTensorId(r);this.temporarySessionTensorIds.delete(e),this.activeSessionId=void 0}}async createMLContext(e){if(e instanceof GPUDevice){let r=this.mlContextCache.findIndex(i=>i.gpuDevice===e);if(r!==-1)return this.mlContextCache[r].mlContext;{let i=await navigator.ml.createContext(e);return this.mlContextCache.push({gpuDevice:e,mlContext:i}),i}}else if(e===void 0){let r=this.mlContextCache.findIndex(i=>i.options===void 0&&i.gpuDevice===void 0);if(r!==-1)return this.mlContextCache[r].mlContext;{let i=await navigator.ml.createContext();return this.mlContextCache.push({mlContext:i}),i}}let t=this.mlContextCache.findIndex(r=>gs(r.options,e));if(t!==-1)return this.mlContextCache[t].mlContext;{let r=await navigator.ml.createContext(e);return this.mlContextCache.push({options:e,mlContext:r}),r}}registerMLContext(e,t){this.mlContextBySessionId.set(e,t);let r=this.sessionIdsByMLContext.get(t);r||(r=new Set,this.sessionIdsByMLContext.set(t,r)),r.add(e),this.mlOpSupportLimitsBySessionId.has(e)||this.mlOpSupportLimitsBySessionId.set(e,t.opSupportLimits()),this.temporaryGraphInputs.length>0&&(this.sessionGraphInputs.set(e,this.temporaryGraphInputs),this.temporaryGraphInputs=[]),this.temporaryGraphOutputs.length>0&&(this.sessionGraphOutputs.set(e,this.temporaryGraphOutputs),this.temporaryGraphOutputs=[])}onReleaseSession(e){this.sessionGraphInputs.delete(e),this.sessionGraphOutputs.delete(e);let t=this.mlContextBySessionId.get(e);if(!t)return;this.tensorManager.releaseTensorsForSession(e),this.mlContextBySessionId.delete(e),this.mlOpSupportLimitsBySessionId.delete(e);let r=this.sessionIdsByMLContext.get(t);if(r.delete(e),r.size===0){this.sessionIdsByMLContext.delete(t);let i=this.mlContextCache.findIndex(a=>a.mlContext===t);i!==-1&&this.mlContextCache.splice(i,1)}}getMLContext(e){return this.mlContextBySessionId.get(e)}getMLOpSupportLimits(e){return this.mlOpSupportLimitsBySessionId.get(e)}reserveTensorId(){return this.tensorManager.reserveTensorId()}releaseTensorId(e){de("verbose",()=>`[WebNN] releaseTensorId {tensorId: ${e}}`),this.tensorManager.releaseTensorId(e)}async ensureTensor(e,t,r,i,a){let n=Xt.get(r);if(!n)throw new Error(`Unsupported ONNX data type: ${r}`);return this.tensorManager.ensureTensor(e??this.currentSessionId,t,n,i,a)}async createTemporaryTensor(e,t,r){de("verbose",()=>`[WebNN] createTemporaryTensor {onnxDataType: ${t}, shape: ${r}}`);let i=Xt.get(t);if(!i)throw new Error(`Unsupported ONNX data type: ${t}`);let a=this.tensorManager.reserveTensorId();await this.tensorManager.ensureTensor(e,a,i,r,!1);let n=this.temporarySessionTensorIds.get(e);return n?n.push(a):this.temporarySessionTensorIds.set(e,[a]),a}uploadTensor(e,t){if(!_e().shouldTransferToMLTensor)throw new Error("Trying to upload to a MLTensor while shouldTransferToMLTensor is false");de("verbose",()=>`[WebNN] uploadTensor {tensorId: ${e}, data: ${t.byteLength}}`),this.tensorManager.upload(e,t)}async downloadTensor(e,t){return this.tensorManager.download(e,t)}createMLTensorDownloader(e,t){return async()=>{let r=await this.tensorManager.download(e);return Ii(r,t)}}registerMLTensor(e,t,r,i){let a=Xt.get(r);if(!a)throw new Error(`Unsupported ONNX data type: ${r}`);let n=this.tensorManager.registerTensor(e,t,a,i);return de("verbose",()=>`[WebNN] registerMLTensor {tensor: ${t}, dataType: ${a}, dimensions: ${i}} -> {tensorId: ${n}}`),n}registerMLConstant(e,t,r,i,a,n,s=!1){if(!n)throw new Error("External mounted files are not available.");let u=e;e.startsWith("./")&&(u=e.substring(2));let l=n.get(u);if(!l)throw new Error(`File with name ${u} not found in preloaded files.`);if(t+r>l.byteLength)throw new Error("Out of bounds: data offset and length exceed the external file data size.");let p=l.slice(t,t+r).buffer,h;switch(a.dataType){case"float32":h=new Float32Array(p);break;case"float16":h=typeof Float16Array<"u"&&Float16Array.from?new Float16Array(p):new Uint16Array(p);break;case"int32":h=new Int32Array(p);break;case"uint32":h=new Uint32Array(p);break;case"int64":if(s){let f=zi(new Uint8Array(p),"int64");h=new Int32Array(f.buffer),a.dataType="int32"}else h=new BigInt64Array(p);break;case"uint64":h=new BigUint64Array(p);break;case"int8":h=new Int8Array(p);break;case"int4":case"uint4":case"uint8":h=new Uint8Array(p);break;default:throw new Error(`Unsupported data type: ${a.dataType} in creating WebNN Constant from external data.`)}return de("verbose",()=>`[WebNN] registerMLConstant {dataType: ${a.dataType}, shape: ${a.shape}}} ${s?"(Note: it was int64 data type and registered to int32 as workaround)":""}`),i.constant(a,h)}registerGraphInput(e){this.temporaryGraphInputs.push(e)}registerGraphOutput(e){this.temporaryGraphOutputs.push(e)}isGraphInput(e,t){let r=this.sessionGraphInputs.get(e);return r?r.includes(t):!1}isGraphOutput(e,t){let r=this.sessionGraphOutputs.get(e);return r?r.includes(t):!1}isGraphInputOutputTypeSupported(e,t,r=!0){let i=Xt.get(Tt(t)),a=this.mlOpSupportLimitsBySessionId.get(e);return typeof i>"u"?!1:r?!!(a!=null&&a.input.dataTypes.includes(i)):!!(a!=null&&a.output.dataTypes.includes(i))}flush(){}}}),Mi=q(()=>{}),Ni,Ir,Er,_s,ws,Di,Ui,bs,$s,im=q(()=>{at(),Mi(),Ni=new Map([[64,250],[128,200],[256,200],[512,200],[2048,230],[4096,200],[8192,50],[16384,50],[32768,50],[65536,50],[131072,50],[262144,50],[524288,50],[1048576,50],[2097152,30],[4194304,20],[8388608,10],[12582912,10],[16777216,10],[26214400,15],[33554432,22],[44236800,2],[58982400,6],[67108864,6],[134217728,6],[167772160,6]]),Ir=[],Er=e=>Math.ceil(Number(e)/16)*16,_s=e=>{for(let t=0;t<Ir.length;t++){let r=Ir[t];if(e<=r)return r}return Math.ceil(e/16)*16},ws=1,Di=()=>ws++,Ui=async(e,t,r,i)=>{let a=Er(r),n=e.device.createBuffer({size:a,usage:GPUBufferUsage.COPY_DST|GPUBufferUsage.MAP_READ});try{let s=e.getCommandEncoder();e.endComputePass(),s.copyBufferToBuffer(t,0,n,0,a),e.flush(),await n.mapAsync(GPUMapMode.READ);let u=n.getMappedRange();if(i){let l=i();return l.set(new Uint8Array(u,0,r)),l}else return new Uint8Array(u.slice(0,r))}finally{n.destroy()}},bs=class{constructor(e){this.backend=e,this.storageCache=new Map,this.freeBuffers=new Map,this.freeUniformBuffers=new Map,this.buffersPending=[],this.capturedPendingBuffers=new Map;for(let[t]of Ni)Ir.push(t),this.freeBuffers.set(t,[]),this.freeUniformBuffers.set(t,[]);this.sessionCount=0}upload(e,t){let r=t.buffer,i=t.byteOffset,a=t.byteLength,n=Er(a),s=this.storageCache.get(e);if(!s)throw new Error("gpu data for uploading does not exist");if(Number(s.originalSize)!==a)throw new Error(`inconsistent data size. gpu data size=${s.originalSize}, data size=${a}`);let u=this.backend.device.createBuffer({mappedAtCreation:!0,size:n,usage:GPUBufferUsage.MAP_WRITE|GPUBufferUsage.COPY_SRC}),l=u.getMappedRange();new Uint8Array(l).set(new Uint8Array(r,i,a)),u.unmap();let p=this.backend.device.createCommandEncoder();p.copyBufferToBuffer(u,0,s.gpuData.buffer,0,n),this.backend.device.queue.submit([p.finish()]),u.destroy(),de("verbose",()=>`[WebGPU] GpuDataManager.upload(id=${e})`)}memcpy(e,t){let r=this.storageCache.get(e);if(!r)throw new Error("source gpu data for memcpy does not exist");let i=this.storageCache.get(t);if(!i)throw new Error("destination gpu data for memcpy does not exist");if(r.originalSize!==i.originalSize)throw new Error("inconsistent source and destination gpu data size");let a=Er(r.originalSize),n=this.backend.getCommandEncoder();this.backend.endComputePass(),n.copyBufferToBuffer(r.gpuData.buffer,0,i.gpuData.buffer,0,a)}registerExternalBuffer(e,t,r){let i;if(r){if(i=r[0],e===r[1])return de("verbose",()=>`[WebGPU] GpuDataManager.registerExternalBuffer(size=${t}) => id=${i}, buffer is the same, skip.`),i;if(this.backend.capturedCommandList.has(this.backend.currentSessionId))throw new Error(`Registering a different external buffer under graph capture mode is not supported yet.
             Please use the previous external buffer!`)}else i=Di();return this.storageCache.set(i,{gpuData:{id:i,type:0,buffer:e},originalSize:t}),de("verbose",()=>`[WebGPU] GpuDataManager.registerExternalBuffer(size=${t}) => id=${i}, registered.`),i}unregisterExternalBuffer(e){e!==void 0&&(this.storageCache.delete(e),de("verbose",()=>`[WebGPU] GpuDataManager.unregisterExternalBuffer() => id=${e}`))}create(e,t=GPUBufferUsage.STORAGE|GPUBufferUsage.COPY_SRC|GPUBufferUsage.COPY_DST){let r=_s(e),i,a=(t&GPUBufferUsage.STORAGE)===GPUBufferUsage.STORAGE,n=(t&GPUBufferUsage.UNIFORM)===GPUBufferUsage.UNIFORM;if(a||n){let u=(a?this.freeBuffers:this.freeUniformBuffers).get(r);u?u.length>0?i=u.pop():i=this.backend.device.createBuffer({size:r,usage:t}):i=this.backend.device.createBuffer({size:r,usage:t})}else i=this.backend.device.createBuffer({size:r,usage:t});let s={id:Di(),type:0,buffer:i};return this.storageCache.set(s.id,{gpuData:s,originalSize:Number(e)}),de("verbose",()=>`[WebGPU] GpuDataManager.create(size=${e}) => id=${s.id}`),s}get(e){var t;return(t=this.storageCache.get(e))==null?void 0:t.gpuData}release(e){let t=typeof e=="bigint"?Number(e):e,r=this.storageCache.get(t);if(!r){if(this.storageCache.size===0)return 0;throw new Error("releasing data does not exist")}return de("verbose",()=>`[WebGPU] GpuDataManager.release(id=${t}), gpuDataId=${r.gpuData.id}`),this.storageCache.delete(t),this.buffersPending.push(r.gpuData.buffer),r.originalSize}async download(e,t){let r=this.storageCache.get(Number(e));if(!r)throw new Error("data does not exist");await Ui(this.backend,r.gpuData.buffer,r.originalSize,t)}refreshPendingBuffers(){if(this.buffersPending.length!==0)if(this.backend.sessionStatus==="default"){for(let e of this.buffersPending){let t=Ni.get(e.size);if((e.usage&GPUBufferUsage.STORAGE)===GPUBufferUsage.STORAGE){let r=this.freeBuffers.get(e.size)||[];t===void 0||r.length>=t?e.destroy():r.push(e)}else if((e.usage&GPUBufferUsage.UNIFORM)===GPUBufferUsage.UNIFORM){let r=this.freeUniformBuffers.get(e.size)||[];t===void 0||r.length>=t?e.destroy():r.push(e)}else e.destroy()}this.buffersPending=[]}else{let e=this.capturedPendingBuffers.get(this.backend.currentSessionId);e||(e=[],this.capturedPendingBuffers.set(this.backend.currentSessionId,e));for(let t of this.buffersPending)e.push(t);this.buffersPending=[]}}dispose(){this.freeBuffers.forEach(e=>{e.forEach(t=>{t.destroy()})}),this.freeUniformBuffers.forEach(e=>{e.forEach(t=>{t.destroy()})}),this.storageCache.forEach(e=>{e.gpuData.buffer.destroy()}),this.capturedPendingBuffers.forEach(e=>{e.forEach(t=>{t.destroy()})}),this.storageCache=new Map,this.freeBuffers=new Map,this.freeUniformBuffers=new Map,this.capturedPendingBuffers=new Map}onCreateSession(){this.sessionCount+=1}onReleaseSession(e){let t=this.capturedPendingBuffers.get(e);t&&(t.forEach(r=>{r.destroy()}),this.capturedPendingBuffers.delete(e)),this.sessionCount-=1,this.sessionCount===0&&(de("warning",()=>"[WebGPU] Clearing webgpu buffer cache"),this.storageCache.forEach(r=>{r.gpuData.buffer.destroy()}),this.storageCache=new Map)}},$s=(...e)=>new bs(...e)}),vs,he,xe=q(()=>{vs=class{constructor(e){Object.assign(this,e)}get cacheKey(){return this.key||(this.key=Object.getOwnPropertyNames(this).sort().map(e=>`${this[e]}`).join(";")),this.key}},he=e=>new vs(e)}),Wt,zr,Te,ze,Y,ve,Pi,Vt,lt,Z,Jt,M,Q,xs,qi,Ss,Ts,ae=q(()=>{te(),re(),Wt=64,zr=(e,t)=>{if(t===3)throw new Error("vec3 has same alignment as vec4, use vec4 instead");switch(Number(e)){case 10:return t>1?`vec${t}<f16>`:"f16";case 1:return t>1?`vec${t}<f32>`:"f32";case 6:return t>1?`vec${t}<i32>`:"i32";case 12:return t>1?`vec${t}<u32>`:"u32";case 7:if(t>1)throw new Error("currently not supported vecX of uint64 yet");return["vec2<u32>","i32"];case 13:if(t>1)throw new Error("currently not supported vecX of uint64 yet");return["vec2<u32>","u32"];case 9:if(t!==4)throw new Error("bool must be vec4");return["u32","vec4<bool>"];case 22:return"i32";case 21:return"u32";default:throw new Error(`Unknown data type: ${e}`)}},Te=(e,t=1)=>{let r=zr(e,t);return typeof r=="string"?r:r[0]},ze=(e,t=1)=>{let r=zr(e,t);return typeof r=="string"?r:r[1]},Y=(...e)=>{let t=[];return e.forEach(r=>{r.length!==0&&t.push({type:12,data:r},{type:12,data:O.computeStrides(r)})}),t},ve=e=>e%4===0?4:e%2===0?2:1,Pi=(e="f32",t,r="0")=>!t||t===1?`${e}(${r})`:`vec${t}<${e}>(${r})`,Vt=(e,t,r)=>e==="f32"?r:t===1?`f32(${r})`:`vec${t}<f32>(${r})`,lt=(e,t)=>t===4?`(${e}.x + ${e}.y + ${e}.z + ${e}.w)`:t===2?`(${e}.x + ${e}.y)`:t===3?`(${e}.x + ${e}.y + ${e}.z)`:e,Z=(e,t,r,i)=>e.startsWith("uniforms.")&&r>4?typeof t=="string"?i==="f16"?`${e}[(${t}) / 8][(${t}) % 8 / 4][(${t}) % 8 % 4]`:`${e}[(${t}) / 4][(${t}) % 4]`:i==="f16"?`${e}[${Math.floor(t/8)}][${Math.floor(t%8/4)}][${t%8%4}]`:`${e}[${Math.floor(t/4)}][${t%4}]`:r>1?`${e}[${t}]`:e,Jt=(e,t,r,i,a)=>{let n=typeof r=="number",s=n?r:r.length,u=[...new Array(s).keys()],l=s<2?"u32":s<=4?`vec${s}<u32>`:`array<u32, ${s}>`,p=zr(t,a),h=typeof p=="string"?p:p[1],f=typeof p=="string"?p:p[0],g={indices:l,value:h,storage:f,tensor:t},y=U=>typeof U=="string"?U:`${U}u`,_={offsetToIndices:!1,indicesToOffset:!1,broadcastedIndicesToOffset:!1,set:!1,setByIndices:!1,get:!1,getByIndices:!1},w=n?"uniforms.":"",S=`${w}${e}_shape`,x=`${w}${e}_strides`,b="";for(let U=0;U<s-1;U++)b+=`
    let dim${U} = current / ${Z(x,U,s)};
    let rest${U} = current % ${Z(x,U,s)};
    indices[${U}] = dim${U};
    current = rest${U};
    `;b+=`indices[${s-1}] = current;`;let I=s<2?"":`
  fn o2i_${e}(offset: u32) -> ${g.indices} {
    var indices: ${g.indices};
    var current = offset;
    ${b}
    return indices;
  }`,k=U=>(_.offsetToIndices=!0,s<2?U:`o2i_${e}(${U})`),E=[];if(s>=2)for(let U=s-1;U>=0;U--)E.push(`${Z(x,U,s)} * (indices[${U}])`);let A=s<2?"":`
  fn i2o_${e}(indices: ${g.indices}) -> u32 {
    return ${E.join("+")};
  }`,C=U=>(_.indicesToOffset=!0,s<2?U:`i2o_${e}(${U})`),$=(...U)=>s===0?"0u":`${g.indices}(${U.map(y).join(",")})`,N=(U,P)=>s<2?`${U}`:`${Z(U,P,s)}`,D=(U,P,J)=>s<2?`${U}=${J};`:`${Z(U,P,s)}=${J};`,G={},V=(U,P)=>{_.broadcastedIndicesToOffset=!0;let J=`${P.name}broadcastedIndicesTo${e}Offset`;if(J in G)return`${J}(${U})`;let ee=[];for(let $e=s-1;$e>=0;$e--){let ht=P.indicesGet("outputIndices",$e+P.rank-s);ee.push(`${N(x,$e)} * (${ht} % ${N(S,$e)})`)}return G[J]=`fn ${J}(outputIndices: ${P.type.indices}) -> u32 {
             return ${ee.length>0?ee.join("+"):"0u"};
           }`,`${J}(${U})`},j=(U,P)=>(()=>{if(g.storage===g.value)return`${e}[${U}]=${P};`;if(g.storage==="vec2<u32>"&&g.value==="i32")return`${e}[${U}]=vec2<u32>(u32(${P}), select(0u, 0xFFFFFFFFu, ${P} < 0));`;if(g.storage==="vec2<u32>"&&g.value==="u32")return`${e}[${U}]=vec2<u32>(u32(${P}), 0u);`;if(g.storage==="u32"&&g.value==="vec4<bool>")return`${e}[${U}]=dot(vec4<u32>(0x1, 0x100, 0x10000, 0x1000000), vec4<u32>(${P}));`;throw new Error(`not supported combination of storage type ${g.storage} and value type ${g.value} yet`)})(),R=U=>(()=>{if(g.storage===g.value)return`${e}[${U}]`;if(g.storage==="vec2<u32>"&&g.value==="i32")return`i32(${e}[${U}].x)`;if(g.storage==="vec2<u32>"&&g.value==="u32")return`u32(${e}[${U}].x)`;if(g.storage==="u32"&&g.value==="vec4<bool>")return`vec4<bool>(bool(${e}[${U}] & 0xFFu), bool(${e}[${U}] & 0xFF00u), bool(${e}[${U}] & 0xFF0000u), bool(${e}[${U}] & 0xFF000000u))`;throw new Error(`not supported combination of storage type ${g.storage} and value type ${g.value} yet`)})(),K=s<2?"":`
  fn get_${e}ByIndices(indices: ${g.indices}) -> ${h} {
    return ${R(`i2o_${e}(indices)`)};
  }`,F=s<2?"":(()=>{let U=u.map(J=>`d${J}: u32`).join(", "),P=u.map(J=>`d${J}`).join(", ");return`
  fn get_${e}(${U}) -> ${h} {
    return get_${e}ByIndices(${$(P)});
  }`})(),X=(...U)=>{if(U.length!==s)throw new Error(`indices length must be ${s}`);let P=U.map(y).join(",");return s===0?R("0u"):s===1?R(P[0]):(_.get=!0,_.getByIndices=!0,_.indicesToOffset=!0,`get_${e}(${P})`)},le=U=>s<2?R(U):(_.getByIndices=!0,_.indicesToOffset=!0,`get_${e}ByIndices(${U})`),L=s<2?"":`
  fn set_${e}ByIndices(indices: ${g.indices}, value: ${h}) {
    ${j(`i2o_${e}(indices)`,"value")}
  }`,me=s<2?"":(()=>{let U=u.map(J=>`d${J}: u32`).join(", "),P=u.map(J=>`d${J}`).join(", ");return`
  fn set_${e}(${U}, value: ${h}) {
    set_${e}ByIndices(${$(P)}, value);
  }`})();return{impl:()=>{let U=[],P=!1;return _.offsetToIndices&&(U.push(I),P=!0),_.indicesToOffset&&(U.push(A),P=!0),_.broadcastedIndicesToOffset&&(Object.values(G).forEach(J=>U.push(J)),P=!0),_.set&&(U.push(me),P=!0),_.setByIndices&&(U.push(L),P=!0),_.get&&(U.push(F),P=!0),_.getByIndices&&(U.push(K),P=!0),!n&&P&&U.unshift(`const ${S} = ${g.indices}(${r.join(",")});`,`const ${x} = ${g.indices}(${O.computeStrides(r).join(",")});`),U.join(`
`)},type:g,offsetToIndices:k,indicesToOffset:C,broadcastedIndicesToOffset:V,indices:$,indicesGet:N,indicesSet:D,set:(...U)=>{if(U.length!==s+1)throw new Error(`indices length must be ${s}`);let P=U[s];if(typeof P!="string")throw new Error("value must be string");let J=U.slice(0,s).map(y).join(",");return s===0?j("0u",P):s===1?j(J[0],P):(_.set=!0,_.setByIndices=!0,_.indicesToOffset=!0,`set_${e}(${J}, ${P})`)},setByOffset:j,setByIndices:(U,P)=>s<2?j(U,P):(_.setByIndices=!0,_.indicesToOffset=!0,`set_${e}ByIndices(${U}, ${P});`),get:X,getByOffset:R,getByIndices:le,usage:i,name:e,strides:x,shape:S,rank:s}},M=(e,t,r,i=1)=>Jt(e,t,r,"input",i),Q=(e,t,r,i=1)=>Jt(e,t,r,"output",i),xs=(e,t,r)=>Jt(e,t,r,"atomicOutput",1),qi=(e,t,r,i=1)=>Jt(e,t,r,"internal",i),Ss=class{constructor(e,t){this.normalizedDispatchGroup=e,this.limits=t,this.internalVariables=[],this.variables=[],this.uniforms=[],this.variableIndex=0}guardAgainstOutOfBoundsWorkgroupSizes(e){return`if (global_idx >= ${typeof e=="number"?`${e}u`:e}) { return; }`}mainStart(e=Wt){let t=typeof e=="number"?e:e[0],r=typeof e=="number"?1:e[1],i=typeof e=="number"?1:e[2];if(t>this.limits.maxComputeWorkgroupSizeX||r>this.limits.maxComputeWorkgroupSizeY||i>this.limits.maxComputeWorkgroupSizeZ)throw new Error(`workgroup size [${t}, ${r}, ${i}] exceeds the maximum workgroup size [${this.limits.maxComputeWorkgroupSizeX}, ${this.limits.maxComputeWorkgroupSizeY}, ${this.limits.maxComputeWorkgroupSizeZ}].`);if(t*r*i>this.limits.maxComputeInvocationsPerWorkgroup)throw new Error(`workgroup size [${t}, ${r}, ${i}] exceeds the maximum workgroup invocations ${this.limits.maxComputeInvocationsPerWorkgroup}.`);let a=this.normalizedDispatchGroup[1]===1&&this.normalizedDispatchGroup[2]===1,n=a?`@builtin(global_invocation_id) global_id : vec3<u32>,
    @builtin(workgroup_id) workgroup_id : vec3<u32>,
    @builtin(local_invocation_index) local_idx : u32,
    @builtin(local_invocation_id) local_id : vec3<u32>`:`@builtin(global_invocation_id) global_id : vec3<u32>,
                                             @builtin(local_invocation_id) local_id : vec3<u32>,
    @builtin(local_invocation_index) local_idx : u32,
    @builtin(workgroup_id) workgroup_id : vec3<u32>,
    @builtin(num_workgroups) num_workgroups : vec3<u32>`,s=a?`let global_idx = global_id.x;
         let workgroup_index = workgroup_id.x;`:`let workgroup_index = workgroup_id.z * num_workgroups[0] * num_workgroups[1] +
             workgroup_id.y * num_workgroups[0] + workgroup_id.x;
         let global_idx = workgroup_index * ${t*r*i}u + local_idx;`;return`@compute @workgroup_size(${t}, ${r}, ${i})
  fn main(${n}) {
    ${s}
  `}appendVariableUniforms(e){e.rank!==0&&(e.shape.startsWith("uniforms.")&&this.uniforms.push({name:e.shape.replace("uniforms.",""),type:"u32",length:e.rank}),e.strides.startsWith("uniforms.")&&this.uniforms.push({name:e.strides.replace("uniforms.",""),type:"u32",length:e.rank}))}declareVariable(e,t){if(e.usage==="internal")throw new Error("cannot use internal variable with declareVariable(). use registerInternalVariables() instead.");this.variables.push(e),this.appendVariableUniforms(e);let r=e.usage==="input"?"read":"read_write",i=e.usage==="atomicOutput"?"atomic<i32>":e.type.storage;return`@group(0) @binding(${t}) var<storage, ${r}> ${e.name}: array<${i}>;`}declareVariables(...e){return e.map(t=>this.declareVariable(t,this.variableIndex++)).join(`
`)}registerInternalVariable(e){if(e.usage!=="internal")throw new Error("cannot use input or output variable with registerInternalVariable(). use declareVariables() instead.");this.internalVariables.push(e),this.appendVariableUniforms(e)}registerInternalVariables(...e){return e.forEach(t=>this.registerInternalVariable(t)),this}registerUniform(e,t,r=1){return this.uniforms.push({name:e,type:t,length:r}),this}registerUniforms(e){return this.uniforms=this.uniforms.concat(e),this}uniformDeclaration(){if(this.uniforms.length===0)return"";let e=[];for(let{name:t,type:r,length:i}of this.uniforms)if(i&&i>4)r==="f16"?e.push(`@align(16) ${t}:array<mat2x4<${r}>, ${Math.ceil(i/8)}>`):e.push(`${t}:array<vec4<${r}>, ${Math.ceil(i/4)}>`);else{let a=i==null||i===1?r:`vec${i}<${r}>`;e.push(`${t}:${a}`)}return`
      struct Uniforms { ${e.join(", ")} };
      @group(0) @binding(${this.variableIndex}) var<uniform> uniforms: Uniforms;`}get additionalImplementations(){return this.uniformDeclaration()+this.variables.map(e=>e.impl()).join(`
`)+this.internalVariables.map(e=>e.impl()).join(`
`)}get variablesInfo(){if(this.uniforms.length===0)return;let e=t=>[12,10,1,6][["u32","f16","f32","i32"].indexOf(t)];return this.uniforms.map(t=>[e(t.type),t.length??1])}},Ts=(e,t)=>new Ss(e,t)}),ks,Li,Is,Es,zs,Cs,Ne,As,Os,dt=q(()=>{te(),re(),xe(),ae(),ks=(e,t)=>{if(!e||e.length!==1)throw new Error("Transpose requires 1 input.");if(t.length!==0&&t.length!==e[0].dims.length)throw new Error(`perm size ${t.length} does not match input rank ${e[0].dims.length}`)},Li=(e,t)=>t.length!==0?t:[...new Array(e).keys()].reverse(),Is=(e,t)=>O.sortBasedOnPerm(e,Li(e.length,t)),Es=(e,t,r,i)=>{let a=`fn perm(i: ${i.type.indices}) -> ${r.type.indices} {
    var a: ${r.type.indices};`;for(let n=0;n<t;++n)a+=`a[${e[n]}]=i[${n}];`;return a+="return a;}"},zs=(e,t)=>{let r=[],i=[];for(let a=0;a<e.length;++a)e[a]!==1&&r.push(e[a]),e[t[a]]!==1&&i.push(t[a]);return{newShape:r,newPerm:i}},Cs=(e,t)=>{let r=0;for(let i=0;i<e.length;++i)if(t[e[i]]!==1){if(e[i]<r)return!1;r=e[i]}return!0},Ne=(e,t)=>{let r=e.dataType,i=e.dims.length,a=Li(i,t),n=Is(e.dims,a),s=e.dims,u=n,l=i<2||Cs(a,e.dims),p;if(l)return p=_=>{let w=M("input",r,s,4),S=Q("output",r,u,4);return`
  ${_.registerUniform("output_size","u32").declareVariables(w,S)}
  ${_.mainStart()}
    ${_.guardAgainstOutOfBoundsWorkgroupSizes("uniforms.output_size")}
    output[global_idx] = input[global_idx];
  }`},{name:"TransposeCopy",shaderCache:{inputDependencies:["type"]},getRunData:()=>{let _=O.size(n);return{outputs:[{dims:n,dataType:e.dataType}],dispatchGroup:{x:Math.ceil(_/64/4)},programUniforms:[{type:12,data:Math.ceil(_/4)}]}},getShaderSource:p};let{newShape:h,newPerm:f}=zs(e.dims,a),g=O.areEqual(f,[2,3,1]),y=O.areEqual(f,[3,1,2]);if(h.length===2||g||y){s=g?[h[0],h[1]*h[2]]:y?[h[0]*h[1],h[2]]:h,u=[s[1],s[0]];let _=16;return p=w=>{let S=M("a",r,s.length),x=Q("output",r,u.length);return`
  ${w.registerUniform("output_size","u32").declareVariables(S,x)}
  var<workgroup> tile : array<array<${x.type.value}, ${_+1}>, ${_}>;
  ${w.mainStart([_,_,1])}
    let stride = (uniforms.output_shape[1] - 1) / ${_} + 1;
    let workgroup_id_x = workgroup_index % stride;
    let workgroup_id_y = workgroup_index / stride;
    let input_col = workgroup_id_y * ${_}u + local_id.x;
    let input_row = workgroup_id_x * ${_}u + local_id.y;
    if (input_row < uniforms.a_shape[0] && input_col < uniforms.a_shape[1]) {
      tile[local_id.y][local_id.x] = ${S.getByIndices(`${S.type.indices}(input_row, input_col)`)};
    }
    workgroupBarrier();

    let output_col = workgroup_id_x * ${_}u + local_id.x;
    let output_row = workgroup_id_y * ${_}u + local_id.y;
    if (output_row < uniforms.output_shape[0] && output_col < uniforms.output_shape[1]) {
      ${x.setByIndices(`${x.type.indices}(output_row, output_col)`,"tile[local_id.x][local_id.y]")}
    }
  }`},{name:"TransposeShared",shaderCache:{inputDependencies:["type"]},getRunData:()=>{let w=O.size(n);return{outputs:[{dims:n,dataType:e.dataType}],dispatchGroup:{x:Math.ceil(u[1]/_),y:Math.ceil(u[0]/_)},programUniforms:[{type:12,data:w},...Y(s,u)]}},getShaderSource:p}}return p=_=>{let w=M("a",r,s.length),S=Q("output",r,u.length);return`
  ${_.registerUniform("output_size","u32").declareVariables(w,S)}

  ${Es(a,i,w,S)}

  ${_.mainStart()}
    ${_.guardAgainstOutOfBoundsWorkgroupSizes("uniforms.output_size")}

    let indices = ${S.offsetToIndices("global_idx")};
    let aIndices = perm(indices);

    ${S.setByOffset("global_idx",w.getByIndices("aIndices"))}
  }`},{name:"Transpose",shaderCache:{hint:`${t}`,inputDependencies:["rank"]},getRunData:()=>{let _=O.size(n);return{outputs:[{dims:n,dataType:e.dataType}],dispatchGroup:{x:Math.ceil(_/64)},programUniforms:[{type:12,data:_},...Y(s,u)]}},getShaderSource:p}},As=(e,t)=>{ks(e.inputs,t.perm),e.compute(Ne(e.inputs[0],t.perm))},Os=e=>he({perm:e.perm})}),Rs,Bs,Ms,Ns,Ds,Us,Ps,qs,Ls,Ws,Ve,Vs,Gs,Hs,Fs,js,Ks,Qs,Zs,Ys,Xs,am=q(()=>{te(),re(),ae(),Vi(),dt(),Rs={max:"select(bestValue, candidate, candidate > bestValue)",min:"select(bestValue, candidate, candidate < bestValue)",mean:"bestValue + candidate",sum:"bestValue + candidate",prod:"bestValue * candidate",sumSquare:"bestValue + candidate * candidate",logSumExp:"bestValue + exp(candidate)",l1:"bestValue + abs(candidate)",l2:"bestValue + candidate * candidate",logSum:"bestValue + candidate"},Bs={max:"select(bestValue, candidate, candidate > bestValue)",min:"select(bestValue, candidate, candidate < bestValue)",mean:"bestValue + candidate",sum:"bestValue + candidate",prod:"bestValue * candidate",sumSquare:"bestValue + candidate",logSumExp:"bestValue + candidate",l1:"bestValue + candidate",l2:"bestValue + candidate",logSum:"bestValue + candidate"},Ms={max:"_A[offset]",min:"_A[offset]",mean:"0",sum:"0",prod:"1",sumSquare:"0",logSumExp:"0",l1:"0",l2:"0",logSum:"0"},Ns={max:"bestValue",min:"bestValue",sum:"bestValue",prod:"bestValue",sumSquare:"bestValue",logSumExp:"log(bestValue)",l1:"bestValue",l2:"sqrt(bestValue)",logSum:"log(bestValue)"},Ds=(e,t)=>{let r=[];for(let i=t-e;i<t;++i)r.push(i);return r},Us=(e,t)=>{let r=[],i=e.length;for(let n=0;n<i;n++)t.indexOf(n)===-1&&r.push(e[n]);let a=t.map(n=>e[n]);return[r,a]},Ps=(e,t)=>{let r=e.length+t.length,i=[],a=0;for(let n=0;n<r;n++)t.indexOf(n)===-1?i.push(e[a++]):i.push(1);return i},qs=(e,t)=>{for(let r=0;r<e.length;++r)if(e[e.length-r-1]!==t-1-r)return!1;return!0},Ls=(e,t)=>{let r=[];if(!qs(e,t)){for(let i=0;i<t;++i)e.indexOf(i)===-1&&r.push(i);e.forEach(i=>r.push(i))}return r},Ws=(e,t,r,i,a,n,s)=>{let u=r[0].dims,l=O.size(n),p=O.size(s),h=M("_A",r[0].dataType,u),f=Q("output",a,n),g=64;l===1&&(g=256);let y=`
          var<workgroup> aBestValues : array<f32, ${g}>;
       `,_=w=>`
        ${w.registerUniform("reduceSize","u32").declareVariables(h,f)}
        ${y}
        fn DIV_CEIL(a : u32, b : u32) -> u32 {
          return ((a - 1u) / b + 1u);
         }
         ${w.mainStart(g)}

          let outputIndex = global_idx / ${g};
          let offset = outputIndex * uniforms.reduceSize;

          var bestValue = f32(${Ms[i]});
          let Length = uniforms.reduceSize;
          for (var k = local_idx; k < Length; k = k + ${g}) {
           let candidate = f32(${h.getByOffset("offset + k")});
           bestValue = ${Rs[i]};
          }
          aBestValues[local_idx] = bestValue;
          workgroupBarrier();

         var reduceSize = min(Length, ${g}u);
         for (var currentSize = reduceSize / 2u; reduceSize > 1u;
             currentSize = reduceSize / 2u) {
           let interval = DIV_CEIL(reduceSize, 2u);
           if (local_idx < currentSize) {
            let candidate = aBestValues[local_idx + interval];
            bestValue = ${Bs[i]};
            aBestValues[local_idx] = bestValue;
           }
           reduceSize = interval;
           workgroupBarrier();
         }

         if (local_idx == 0u) {
          ${f.setByOffset("outputIndex",`${i==="mean"?`${f.type.storage}(bestValue / f32(uniforms.reduceSize))`:`${f.type.storage}(${Ns[i]})`}`)};
         }
        }`;return{name:e,shaderCache:{hint:`${t};${g}`,inputDependencies:["type"]},getShaderSource:_,getRunData:()=>({outputs:[{dims:n,dataType:a}],dispatchGroup:{x:l},programUniforms:[{type:12,data:p}]})}},Ve=(e,t,r,i)=>{let a=e.inputs.length===1?r:Wi(e.inputs,r),n=a.axes;n.length===0&&!a.noopWithEmptyAxes&&(n=e.inputs[0].dims.map((y,_)=>_));let s=O.normalizeAxes(n,e.inputs[0].dims.length),u=s,l=e.inputs[0],p=Ls(u,e.inputs[0].dims.length);p.length>0&&(l=e.compute(Ne(e.inputs[0],p),{inputs:[0],outputs:[-1]})[0],u=Ds(u.length,l.dims.length));let[h,f]=Us(l.dims,u),g=h;a.keepDims&&(g=Ps(h,s)),e.compute(Ws(t,a.cacheKey,[l],i,e.inputs[0].dataType,g,f),{inputs:[l]})},Vs=(e,t)=>{Ve(e,"ReduceMeanShared",t,"mean")},Gs=(e,t)=>{Ve(e,"ReduceL1Shared",t,"l1")},Hs=(e,t)=>{Ve(e,"ReduceL2Shared",t,"l2")},Fs=(e,t)=>{Ve(e,"ReduceLogSumExpShared",t,"logSumExp")},js=(e,t)=>{Ve(e,"ReduceMaxShared",t,"max")},Ks=(e,t)=>{Ve(e,"ReduceMinShared",t,"min")},Qs=(e,t)=>{Ve(e,"ReduceProdShared",t,"prod")},Zs=(e,t)=>{Ve(e,"ReduceSumShared",t,"sum")},Ys=(e,t)=>{Ve(e,"ReduceSumSquareShared",t,"sumSquare")},Xs=(e,t)=>{Ve(e,"ReduceLogSumShared",t,"logSum")}}),Ge,Js,Cr,Wi,He,eo,to,ro,io,ao,no,so,oo,uo,lo,Fe,po,co,ho,fo,mo,go,yo,_o,wo,bo,Vi=q(()=>{te(),re(),xe(),ae(),am(),Ge=e=>{if(!e||e.length===0||e.length>2)throw new Error("Reduce op requires 1 or 2 inputs.");if(e.length===2&&e[1].dims.length!==1)throw new Error("Invalid axes input dims.")},Js=e=>["","",`var value = ${e.getByIndices("input_indices")};`,""],Cr=(e,t,r,i,a,n,s=!1,u=!1)=>{let l=[],p=r[0].dims,h=p.length,f=O.normalizeAxes(a,h),g=!u&&f.length===0;p.forEach((w,S)=>{g||f.indexOf(S)>=0?s&&l.push(1):l.push(w)});let y=l.length,_=O.size(l);return{name:e,shaderCache:t,getShaderSource:w=>{let S=[],x=M("_A",r[0].dataType,h),b=Q("output",n,y),I=i(x,b,f),k=I[2];for(let E=0,A=0;E<h;E++)g||f.indexOf(E)>=0?(s&&A++,k=`for(var j${E}: u32 = 0; j${E} < ${p[E]}; j${E}++) {
                  ${I[2].includes("last_index")?`let last_index = j${E};`:""}
                  ${x.indicesSet("input_indices",E,`j${E}`)}
                  ${k}
                }`):(S.push(`${x.indicesSet("input_indices",E,b.indicesGet("output_indices",A))};`),A++);return`

        ${w.registerUniform("output_size","u32").declareVariables(x,b)}

        ${w.mainStart()}
          ${w.guardAgainstOutOfBoundsWorkgroupSizes("uniforms.output_size")}
          var input_indices: ${x.type.indices};
          let output_indices = ${b.offsetToIndices("global_idx")};

          ${S.join(`
`)}
          ${I[0]}       // init ops for reduce max/min
          ${I[1]}
          ${k}
          ${I[3]}
          ${I.length===4?b.setByOffset("global_idx","value"):I.slice(4).join(`
`)}
        }`},getRunData:()=>({outputs:[{dims:l,dataType:n}],dispatchGroup:{x:Math.ceil(_/64)},programUniforms:[{type:12,data:_},...Y(p,l)]})}},Wi=(e,t)=>{let r=[];return e[1].dims[0]>0&&e[1].getBigInt64Array().forEach(i=>r.push(Number(i))),he({axes:r,keepDims:t.keepDims,noopWithEmptyAxes:t.noopWithEmptyAxes})},He=(e,t,r,i)=>{let a=e.inputs,n=a.length===1?r:Wi(a,r);e.compute(Cr(t,{hint:n.cacheKey,inputDependencies:["rank"]},[a[0]],n.noopWithEmptyAxes&&n.axes.length===0?Js:i,n.axes,a[0].dataType,n.keepDims,n.noopWithEmptyAxes),{inputs:[0]})},eo=(e,t)=>{Ge(e.inputs),He(e,"ReduceLogSum",t,(r,i)=>[`var value = ${i.type.storage}(0);`,"",`value += ${r.getByIndices("input_indices")};`,"value = log(value);"])},to=(e,t)=>{Ge(e.inputs),He(e,"ReduceL1",t,(r,i)=>[`var value = ${i.type.storage}(0);`,"",`value += abs(${r.getByIndices("input_indices")});`,""])},ro=(e,t)=>{Ge(e.inputs),He(e,"ReduceL2",t,(r,i)=>[`var t = ${i.type.value}(0); var value = ${i.type.value}(0);`,"",`t = ${r.getByIndices("input_indices")}; value += (t * t);`,"value = sqrt(value);"])},io=(e,t)=>{Ge(e.inputs),He(e,"ReduceLogSumExp",t,(r,i)=>[`var value = ${i.type.storage}(0);`,"",`value += exp(${r.getByIndices("input_indices")});`,"value = log(value);"])},ao=(e,t)=>{Ge(e.inputs),He(e,"ReduceMax",t,(r,i,a)=>{let n=[];for(let s=0;s<r.rank;s++)(a.indexOf(s)>=0||a.length===0)&&n.push(r.indicesSet("input_indices",s,0));return[`${n.join(`
`)}`,`var value = ${r.getByIndices("input_indices")};`,`value = max(value, ${r.getByIndices("input_indices")});`,""]})},no=(e,t)=>{Ge(e.inputs),He(e,"ReduceMean",t,(r,i,a)=>{let n=1;for(let s=0;s<r.rank;s++)(a.indexOf(s)>=0||a.length===0)&&(n*=e.inputs[0].dims[s]);return["var sum = f32(0);","",`sum += f32(${r.getByIndices("input_indices")});`,`let value = ${i.type.value}(sum / ${n});`]})},so=(e,t)=>{Ge(e.inputs),He(e,"ReduceMin",t,(r,i,a)=>{let n=[];for(let s=0;s<r.rank;s++)(a.indexOf(s)>=0||a.length===0)&&n.push(`input_indices[${s}] = 0;`);return[`${n.join(`
`)}`,`var value = ${r.getByIndices("input_indices")};`,`value = min(value, ${r.getByIndices("input_indices")});`,""]})},oo=(e,t)=>{Ge(e.inputs),He(e,"ReduceProd",t,(r,i)=>[`var value = ${i.type.storage}(1);`,"",`value *= ${r.getByIndices("input_indices")};`,""])},uo=(e,t)=>{Ge(e.inputs),He(e,"ReduceSum",t,(r,i)=>[`var value = ${i.type.storage}(0);`,"",`value += ${r.getByIndices("input_indices")};`,""])},lo=(e,t)=>{Ge(e.inputs),He(e,"ReduceSumSquare",t,(r,i)=>[`var t = ${i.type.value}(0); var value = ${i.type.value}(0);`,"",`t = ${r.getByIndices("input_indices")}; value += t * t;`,""])},Fe=(e,t,r)=>{if(t.length===0)return r;let i=1,a=1;for(let n=0;n<t.length;n++)t.indexOf(n)===-1?i*=e[n]:a*=e[n];return a<32&&i>1024},po=(e,t)=>{Fe(e.inputs[0].dims,t.axes,t.noopWithEmptyAxes)?no(e,t):Vs(e,t)},co=(e,t)=>{Fe(e.inputs[0].dims,t.axes,t.noopWithEmptyAxes)?to(e,t):Gs(e,t)},ho=(e,t)=>{Fe(e.inputs[0].dims,t.axes,t.noopWithEmptyAxes)?ro(e,t):Hs(e,t)},fo=(e,t)=>{Fe(e.inputs[0].dims,t.axes,t.noopWithEmptyAxes)?io(e,t):Fs(e,t)},mo=(e,t)=>{Fe(e.inputs[0].dims,t.axes,t.noopWithEmptyAxes)?ao(e,t):js(e,t)},go=(e,t)=>{Fe(e.inputs[0].dims,t.axes,t.noopWithEmptyAxes)?so(e,t):Ks(e,t)},yo=(e,t)=>{Fe(e.inputs[0].dims,t.axes,t.noopWithEmptyAxes)?oo(e,t):Qs(e,t)},_o=(e,t)=>{Fe(e.inputs[0].dims,t.axes,t.noopWithEmptyAxes)?uo(e,t):Zs(e,t)},wo=(e,t)=>{Fe(e.inputs[0].dims,t.axes,t.noopWithEmptyAxes)?lo(e,t):Ys(e,t)},bo=(e,t)=>{Fe(e.inputs[0].dims,t.axes,t.noopWithEmptyAxes)?eo(e,t):Xs(e,t)}}),Gi,$o,vo,Hi,nm=q(()=>{te(),xe(),Vi(),Gi=e=>{if(!e||e.length===0||e.length>2)throw new Error("ArgMinMaxOp op requires 1 or 2 inputs.");if(e[0].dataType!==1)throw new Error("Invalid input type.")},$o=(e,t)=>{Gi(e.inputs);let r=(i,a,n)=>{let s=[];for(let u=0;u<i.rank;u++)(n.indexOf(u)>=0||n.length===0)&&s.push(`input_indices[${u}] = 0;`);return[`${s.join(`
`)}`,`var value = ${i.getByIndices("input_indices")};
var best_index : i32 = 0;`,`if (${i.getByIndices("input_indices")} ${t.selectLastIndex>0?"<=":"<"} value) {
         value = ${i.getByIndices("input_indices")};
         best_index = i32(last_index);
       }`,"",a.setByOffset("global_idx","best_index")]};e.compute(Cr("ArgMin",{hint:t.cacheKey,inputDependencies:["rank"]},[e.inputs[0]],r,[t.axis],7,t.keepDims),{inputs:[0]})},vo=(e,t)=>{Gi(e.inputs);let r=(i,a,n)=>{let s=[];for(let u=0;u<i.rank;u++)(n.indexOf(u)>=0||n.length===0)&&s.push(`input_indices[${u}] = 0;`);return[`${s.join(`
`)}`,`var value = ${i.getByIndices("input_indices")};
var best_index : i32 = 0;`,`if (${i.getByIndices("input_indices")} ${t.selectLastIndex>0?">=":">"} value) {
         value = ${i.getByIndices("input_indices")};
         best_index = i32(last_index);
       }`,"",a.setByOffset("global_idx","best_index")]};e.compute(Cr("argMax",{hint:t.cacheKey,inputDependencies:["rank"]},[e.inputs[0]],r,[t.axis],7,t.keepDims),{inputs:[0]})},Hi=e=>he(e)}),xo,Ar,So,To,ko,er,Io,Eo,Fi=q(()=>{te(),re(),Mi(),ae(),xo=(e,t)=>{let r=e[0],i=e[1],a=e[2],n=e[3],s=e[4],u=e[5];if(s&&u)throw new Error("Attention cannot have both past and attention_bias");if(r.dims.length!==3)throw new Error('Input "input" must have 3 dimensions');let l=r.dims[0],p=r.dims[1],h=r.dims[2];if(a.dims.length!==1)throw new Error('Input "bias" is expected to have 1 dimensions');if(i.dims.length!==2)throw new Error('Input "weights" is expected to have 2 dimensions');if(i.dims[0]!==h)throw new Error("Input 1 dimension 0 should have same length as dimension 2 of input 0");if(a.dims[0]!==i.dims[1])throw new Error('Input "bias" dimension 0 should have same length as dimension 1 of input "weights"');let f=a.dims[0]/3,g=f,y=g;if(t.qkvHiddenSizes.length>0){if(t.qkvHiddenSizes.length!==3)throw new Error("qkv_hidden_sizes attribute should have 3 elements");for(let I of t.qkvHiddenSizes)if(I%t.numHeads!==0)throw new Error("qkv_hidden_sizes should be divisible by num_heads");f=t.qkvHiddenSizes[0],g=t.qkvHiddenSizes[1],y=t.qkvHiddenSizes[2]}let _=p;if(f!==g)throw new Error("qkv_hidden_sizes first element should be same as the second");if(a.dims[0]!==f+g+y)throw new Error('Input "bias" dimension 0 should have same length as sum of Q/K/V hidden sizes');let w=0;if(s){if(g!==y)throw new Error('Input "past" expect k_hidden_size == v_hidden_size');if(s.dims.length!==5)throw new Error('Input "past" must have 5 dimensions');if(s.dims[0]!==2)throw new Error('Input "past" first dimension must be 2');if(s.dims[1]!==l)throw new Error('Input "past" second dimension must be batch_size');if(s.dims[2]!==t.numHeads)throw new Error('Input "past" third dimension must be num_heads');if(s.dims[4]!==g/t.numHeads)throw new Error('Input "past" fifth dimension must be k_hidden_size / num_heads');t.pastPresentShareBuffer||(w=s.dims[3])}let S=_+w,x=-1,b=0;if(n)throw new Error("Mask not supported");if(s)throw new Error("past is not supported");if(u){if(u.dims.length!==4)throw new Error('Input "attention_bias" must have 4 dimensions');if(u.dims[0]!==l||u.dims[1]!==t.numHeads||u.dims[2]!==p||u.dims[3]!==S)throw new Error('Expect "attention_bias" shape (batch_size, num_heads, sequence_length, total_sequence_length)')}return{batchSize:l,sequenceLength:p,pastSequenceLength:w,kvSequenceLength:_,totalSequenceLength:S,maxSequenceLength:x,inputHiddenSize:h,hiddenSize:f,vHiddenSize:y,headSize:Math.floor(f/t.numHeads),vHeadSize:Math.floor(y/t.numHeads),numHeads:t.numHeads,isUnidirectional:!1,pastPresentShareBuffer:!1,maskFilterValue:t.maskFilterValue,maskType:b,scale:t.scale,broadcastResPosBias:!1,passPastInKv:!1,qkvFormat:1}},Ar=(e,t,r)=>t&&e?`
      let total_sequence_length_input = u32(${t.getByOffset("0")});
      let present_sequence_length = max(total_sequence_length_input, uniforms.past_sequence_length);
      let is_subsequent_prompt: bool = sequence_length > 1 && sequence_length != total_sequence_length_input;
      let is_first_prompt: bool = is_subsequent_prompt == false && sequence_length == total_sequence_length_input;
      total_sequence_length = u32(${e==null?void 0:e.getByOffset("batchIdx")}) + 1;
      var past_sequence_length: u32 = 0;
      if (is_first_prompt == false) {
        past_sequence_length = total_sequence_length - sequence_length;
      }
       `:`
    ${r?"let past_sequence_length = uniforms.past_sequence_length":""};
    let present_sequence_length = total_sequence_length;
    `,So=(e,t,r,i,a,n,s,u)=>{let l=ve(s?1:n),p=64,h=n/l;h<p&&(p=32);let f=Math.ceil(n/l/p),g=[{type:12,data:t},{type:12,data:r},{type:12,data:i},{type:12,data:a},{type:12,data:h},{type:12,data:f}],y=Te(e.dataType,l),_=ze(1,l),w=["type"];s&&w.push("type"),u&&w.push("type");let S=x=>{let b=Q("x",e.dataType,e.dims,l),I=[b],k=s?M("seq_lens",s.dataType,s.dims):void 0;k&&I.push(k);let E=u?M("total_sequence_length_input",u.dataType,u.dims):void 0;E&&I.push(E);let A=ze(e.dataType),C=[{name:"batch_size",type:"u32"},{name:"num_heads",type:"u32"},{name:"past_sequence_length",type:"u32"},{name:"sequence_length",type:"u32"},{name:"total_sequence_length",type:"u32"},{name:"elements_per_thread",type:"u32"}];return`
  var<workgroup> thread_max: array<f32, ${p}>;
  var<workgroup> thread_sum: array<f32, ${p}>;
  ${x.registerUniforms(C).declareVariables(...I)}
  ${x.mainStart([p,1,1])}
    let batchIdx = workgroup_id.z / uniforms.num_heads;
    let headIdx = workgroup_id.z % uniforms.num_heads;
    let sequence_length = uniforms.sequence_length;
    var total_sequence_length = uniforms.total_sequence_length;
    ${Ar(k,E,!1)}
    let local_offset = local_idx * uniforms.elements_per_thread;
    let offset = (global_idx / ${p}) * uniforms.total_sequence_length + local_offset;
    let seq_causal_length = ${s?"u32(past_sequence_length + workgroup_id.y + 1)":"total_sequence_length"};
    var thread_max_vector = ${_}(-3.4028234663852886e+38f);
    for (var i: u32 = 0; i < uniforms.elements_per_thread && i + local_offset < seq_causal_length; i++) {
      thread_max_vector = max(${_}(x[offset + i]), thread_max_vector);
    }
    thread_max[local_idx] = ${(()=>{switch(l){case 1:return"thread_max_vector";case 2:return"max(thread_max_vector.x, thread_max_vector.y)";case 4:return"max(max(thread_max_vector.x, thread_max_vector.y), max(thread_max_vector.z, thread_max_vector.w))";default:throw new Error(`Unsupported components: ${l}`)}})()};
    workgroupBarrier();

    var max_value =  f32(-3.4028234663852886e+38f);
    for (var i = 0u; i < ${p}; i++) {
      max_value = max(thread_max[i], max_value);
    }

    var sum_vector = ${_}(0);
    for (var i: u32 = 0; i < uniforms.elements_per_thread && i + local_offset < seq_causal_length; i++) {
      sum_vector += exp(${_}(x[offset + i]) - max_value);
    }
    thread_sum[local_idx] = ${(()=>{switch(l){case 1:return"sum_vector";case 2:return"sum_vector.x + sum_vector.y";case 4:return"sum_vector.x + sum_vector.y + sum_vector.z + sum_vector.w";default:throw new Error(`Unsupported components: ${l}`)}})()};
    workgroupBarrier();

    var sum: f32 = 0;
    for (var i = 0u; i < ${p}; i++) {
      sum += thread_sum[i];
    }

    if (sum == 0) {
      for (var i: u32 = 0; i < uniforms.elements_per_thread && i + local_offset < seq_causal_length; i++) {
        x[offset + i] = ${b.type.value}(${A}(1.0) / ${A}(seq_causal_length));
      }
    } else {
      for (var i: u32 = 0; i < uniforms.elements_per_thread && i + local_offset < seq_causal_length; i++) {
        var f32input = ${_}(x[offset + i]);
        x[offset + i] = ${b.type.value}(exp(f32input - max_value) / sum);
      }
    }
      ${s?`
        for (var total_seq_id: u32 = seq_causal_length; total_seq_id + local_offset < uniforms.total_sequence_length; total_seq_id++) {
          x[offset + total_seq_id] = ${b.type.value}(${A}(0));
        }`:""};
  }`};return{name:"AttentionProbsSoftmax",shaderCache:{hint:`${p};${y};${l}`,inputDependencies:w},getShaderSource:S,getRunData:()=>({outputs:[],dispatchGroup:{x:1,y:a,z:t*r},programUniforms:g})}},To=(e,t,r,i,a,n,s,u,l)=>{let p=s+n.kvSequenceLength,h=[n.batchSize,n.numHeads,n.sequenceLength,p],f=e>1&&i,g=n.kvNumHeads?n.kvNumHeads:n.numHeads,y=f?[n.batchSize,g,p,n.headSize]:void 0,_=n.nReps?n.nReps:1,w=n.scale===0?1/Math.sqrt(n.headSize):n.scale,S=ve(n.headSize),x=n.headSize/S,b=12,I={x:Math.ceil(p/b),y:Math.ceil(n.sequenceLength/b),z:n.batchSize*n.numHeads},k=[{type:12,data:n.sequenceLength},{type:12,data:x},{type:12,data:p},{type:12,data:n.numHeads},{type:12,data:n.headSize},{type:1,data:w},{type:12,data:s},{type:12,data:n.kvSequenceLength},{type:12,data:_}],E=f&&i&&O.size(i.dims)>0,A=["type","type"];E&&A.push("type"),a&&A.push("type"),u&&A.push("type"),l&&A.push("type");let C=[{dims:h,dataType:t.dataType,gpuDataType:0}];f&&C.push({dims:y,dataType:t.dataType,gpuDataType:0});let $=N=>{let D=M("q",t.dataType,t.dims,S),G=M("key",r.dataType,r.dims,S),V=[D,G];if(E){let L=M("past_key",i.dataType,i.dims,S);V.push(L)}a&&V.push(M("attention_bias",a.dataType,a.dims));let j=u?M("seq_lens",u.dataType,u.dims):void 0;j&&V.push(j);let R=l?M("total_sequence_length_input",l.dataType,l.dims):void 0;R&&V.push(R);let K=Q("output",t.dataType,h),F=[K];f&&F.push(Q("present_key",t.dataType,y,S));let X=ze(1,S),le=[{name:"M",type:"u32"},{name:"K",type:"u32"},{name:"N",type:"u32"},{name:"num_heads",type:"u32"},{name:"head_size",type:"u32"},{name:"alpha",type:"f32"},{name:"past_sequence_length",type:"u32"},{name:"kv_sequence_length",type:"u32"},{name:"n_reps",type:"u32"}];return`
  const TILE_SIZE = ${b}u;

  var<workgroup> tileQ: array<${D.type.storage}, ${b*b}>;
  var<workgroup> tileK: array<${D.type.storage}, ${b*b}>;
  ${N.registerUniforms(le).declareVariables(...V,...F)}
  ${N.mainStart([b,b,1])}
    // x holds the N and y holds the M
    let headIdx = workgroup_id.z % uniforms.num_heads;
    let kvHeadIdx = ${_===1?"headIdx":"headIdx / uniforms.n_reps"};
    let kv_num_heads = ${_===1?"uniforms.num_heads":"uniforms.num_heads / uniforms.n_reps"};
    let batchIdx = workgroup_id.z / uniforms.num_heads;
    let m = workgroup_id.y * TILE_SIZE;
    let n = workgroup_id.x * TILE_SIZE;
    let sequence_length = uniforms.M;
    var total_sequence_length = uniforms.N;
    ${Ar(j,R,!0)}
    let absKvHeadIdx = batchIdx * kv_num_heads + kvHeadIdx;
    let qOffset = workgroup_id.z * uniforms.M * uniforms.K + m * uniforms.K;
    ${E&&f?"let pastKeyOffset = absKvHeadIdx * uniforms.past_sequence_length * uniforms.K;":""};
    let kOffset = absKvHeadIdx * uniforms.kv_sequence_length * uniforms.K;
    ${f?"let presentKeyOffset = absKvHeadIdx * uniforms.N * uniforms.K;":""}
    var value = ${X}(0);
    for (var w: u32 = 0u; w < uniforms.K; w += TILE_SIZE) {
      if (global_id.y < uniforms.M && w + local_id.x < uniforms.K) {
        tileQ[TILE_SIZE * local_id.y + local_id.x] = q[qOffset + local_id.y * uniforms.K + w + local_id.x];
      }
      if (n + local_id.y < uniforms.N && w + local_id.x < uniforms.K) {
        var idx = TILE_SIZE * local_id.y + local_id.x;
      ${E&&f?`
              if (n + local_id.y < past_sequence_length) {
                tileK[idx] = past_key[pastKeyOffset + (n + local_id.y) * uniforms.K + w + local_id.x];
              } else if (n + local_id.y - past_sequence_length < uniforms.kv_sequence_length) {
                tileK[idx] = key[kOffset + (n + local_id.y - past_sequence_length) * uniforms.K + w + local_id.x];
              }`:`
          if (n + local_id.y < uniforms.kv_sequence_length) {
            tileK[idx] = key[kOffset + (n + local_id.y) * uniforms.K + w + local_id.x];
          }`}
      ${f?`if (n + local_id.y < present_sequence_length) {
        present_key[presentKeyOffset + (n + local_id.y) * uniforms.K + w + local_id.x] = tileK[idx];
      }`:""}
      }
      workgroupBarrier();

      for (var k: u32 = 0u; k < TILE_SIZE && w+k < uniforms.K; k++) {
          value += ${X}(tileQ[TILE_SIZE * local_id.y + k] * tileK[TILE_SIZE * local_id.x + k]);
      }

      workgroupBarrier();
    }

    if (global_id.y < uniforms.M && global_id.x < total_sequence_length) {
      let headOffset = workgroup_id.z * uniforms.M * uniforms.N;
      let outputIdx = headOffset + global_id.y * uniforms.N + global_id.x;
      var sum: f32 = ${(()=>{switch(S){case 1:return"value";case 2:return"value.x + value.y";case 4:return"value.x + value.y + value.z + value.w";default:throw new Error(`Unsupported components: ${S}`)}})()};
        output[outputIdx] = ${K.type.value} (sum * uniforms.alpha) + ${a?"attention_bias[outputIdx]":"0.0"};
    }
  }`};return{name:"AttentionProbs",shaderCache:{hint:`${S};${a!==void 0};${i!==void 0};${e}`,inputDependencies:A},getRunData:()=>({outputs:C,dispatchGroup:I,programUniforms:k}),getShaderSource:$}},ko=(e,t,r,i,a,n,s=void 0,u=void 0)=>{let l=n+a.kvSequenceLength,p=a.nReps?a.nReps:1,h=a.vHiddenSize*p,f=e>1&&i,g=a.kvNumHeads?a.kvNumHeads:a.numHeads,y=f?[a.batchSize,g,l,a.headSize]:void 0,_=[a.batchSize,a.sequenceLength,h],w=12,S={x:Math.ceil(a.vHeadSize/w),y:Math.ceil(a.sequenceLength/w),z:a.batchSize*a.numHeads},x=[{type:12,data:a.sequenceLength},{type:12,data:l},{type:12,data:a.vHeadSize},{type:12,data:a.numHeads},{type:12,data:a.headSize},{type:12,data:h},{type:12,data:n},{type:12,data:a.kvSequenceLength},{type:12,data:p}],b=f&&i&&O.size(i.dims)>0,I=["type","type"];b&&I.push("type"),s&&I.push("type"),u&&I.push("type");let k=[{dims:_,dataType:t.dataType,gpuDataType:0}];f&&k.push({dims:y,dataType:t.dataType,gpuDataType:0});let E=A=>{let C=M("probs",t.dataType,t.dims),$=M("v",r.dataType,r.dims),N=[C,$];b&&N.push(M("past_value",i.dataType,i.dims));let D=s?M("seq_lens",s.dataType,s.dims):void 0;s&&N.push(D);let G=u?M("total_sequence_length_input",u.dataType,u.dims):void 0;u&&N.push(G);let V=[Q("output",t.dataType,_)];f&&V.push(Q("present_value",t.dataType,y));let j=[{name:"M",type:"u32"},{name:"K",type:"u32"},{name:"N",type:"u32"},{name:"num_heads",type:"u32"},{name:"head_size",type:"u32"},{name:"v_hidden_size",type:"u32"},{name:"past_sequence_length",type:"u32"},{name:"kv_sequence_length",type:"u32"},{name:"n_reps",type:"u32"}];return`
  const TILE_SIZE = ${w}u;
  var<workgroup> tileQ: array<${C.type.value}, ${w*w}>;
  var<workgroup> tileV: array<${C.type.value}, ${w*w}>;
  ${A.registerUniforms(j).declareVariables(...N,...V)}
  ${A.mainStart([w,w,1])}
   let headIdx = workgroup_id.z % uniforms.num_heads;
   let batchIdx = workgroup_id.z / uniforms.num_heads;
   let kvHeadIdx = ${p===1?"headIdx":"headIdx / uniforms.n_reps"};
   let kv_num_heads = ${p===1?"uniforms.num_heads":"uniforms.num_heads / uniforms.n_reps"};
   let m = global_id.y;
   let n = global_id.x;
   let sequence_length = uniforms.M;
   var total_sequence_length = uniforms.K;
   ${Ar(D,G,!0)}
   let offsetA = workgroup_id.z * uniforms.M * uniforms.K + m * uniforms.K;
   let absKvHeadIdx = batchIdx * kv_num_heads + kvHeadIdx; // kvHeadIdx is relative to the batch
   ${b&&f?"let pastValueOffset = absKvHeadIdx * uniforms.N * uniforms.past_sequence_length + n;":""};
   let vOffset = absKvHeadIdx * uniforms.N * uniforms.kv_sequence_length + n;
   ${f?"let presentValueOffset = absKvHeadIdx * uniforms.N * uniforms.K + n;":""}
   var value = ${C.type.storage}(0);
   for (var w: u32 = 0u; w < uniforms.K; w += TILE_SIZE) {
      if (m < uniforms.M && w + local_id.x < uniforms.K) {
        tileQ[TILE_SIZE * local_id.y + local_id.x] = probs[offsetA + w + local_id.x];
      }
      if (n < uniforms.N && w + local_id.y < uniforms.K) {
        var idx = TILE_SIZE * local_id.y + local_id.x;
        ${b&&f?`
        if (w + local_id.y < past_sequence_length) {
          tileV[idx] = past_value[pastValueOffset + (w + local_id.y) * uniforms.N];
        } else if (w + local_id.y - past_sequence_length < uniforms.kv_sequence_length) {
          tileV[idx] = v[vOffset + (w + local_id.y - past_sequence_length) * uniforms.N];
        }
      `:`
            if (w + local_id.y < uniforms.kv_sequence_length) {
              tileV[idx] = v[vOffset + (w + local_id.y) * uniforms.N];
            }`}
        ${f?`
            if (w + local_id.y < present_sequence_length) {
          present_value[presentValueOffset + (w + local_id.y) * uniforms.N] = tileV[idx];
        }`:""}
      }
     workgroupBarrier();
     for (var k: u32 = 0u; k < TILE_SIZE && w+k < total_sequence_length; k++) {
       value += tileQ[TILE_SIZE * local_id.y + k] * tileV[TILE_SIZE * k + local_id.x];
     }
     workgroupBarrier();
   }

   // we need to transpose output from BNSH_v to BSND_v
   if (m < uniforms.M && n < uniforms.N) {
     let outputIdx = batchIdx * uniforms.M * uniforms.v_hidden_size + m * uniforms.v_hidden_size
       + headIdx * uniforms.N + n;
     output[outputIdx] = value;
   }
  }`};return{name:"AttentionScore",shaderCache:{hint:`${i!==void 0};${e}`,inputDependencies:I},getRunData:()=>({outputs:k,dispatchGroup:S,programUniforms:x}),getShaderSource:E}},er=(e,t,r,i,a,n,s,u,l,p,h=void 0,f=void 0)=>{let g=Math.min(e.outputCount,1+(s?1:0)+(u?1:0)),y=g>1?p.pastSequenceLength:0,_=y+p.kvSequenceLength,w=l&&O.size(l.dims)>0?l:void 0,S=[t,r];g>1&&s&&O.size(s.dims)>0&&S.push(s),w&&S.push(w),h&&S.push(h),f&&S.push(f);let x=e.compute(To(g,t,r,s,w,p,y,h,f),{inputs:S,outputs:g>1?[-1,1]:[-1]})[0];e.compute(So(x,p.batchSize,p.numHeads,y,p.sequenceLength,_,h,f),{inputs:h&&f?[x,h,f]:[x],outputs:[]});let b=[x,i];g>1&&u&&O.size(u.dims)>0&&b.push(u),h&&b.push(h),f&&b.push(f),e.compute(ko(g,x,i,u,p,y,h,f),{inputs:b,outputs:g>1?[0,2]:[0]})},Io=(e,t)=>{let r=[t.batchSize,t.numHeads,t.sequenceLength,t.headSize],i=t.sequenceLength,a=t.inputHiddenSize,n=t.headSize,s=12,u={x:Math.ceil(t.headSize/s),y:Math.ceil(t.sequenceLength/s),z:t.batchSize*t.numHeads},l=[e.inputs[0],e.inputs[1],e.inputs[2]],p=[{type:12,data:i},{type:12,data:a},{type:12,data:n},{type:12,data:t.numHeads},{type:12,data:t.headSize},{type:12,data:t.hiddenSize},{type:12,data:t.hiddenSize+t.hiddenSize+t.vHiddenSize}],h=f=>{let g=Q("output_q",l[0].dataType,r),y=Q("output_k",l[0].dataType,r),_=Q("output_v",l[0].dataType,r),w=M("input",l[0].dataType,l[0].dims),S=M("weight",l[1].dataType,l[1].dims),x=M("bias",l[2].dataType,l[2].dims),b=w.type.storage,I=[{name:"M",type:"u32"},{name:"K",type:"u32"},{name:"N",type:"u32"},{name:"num_heads",type:"u32"},{name:"head_size",type:"u32"},{name:"hidden_size",type:"u32"},{name:"ldb",type:"u32"}];return`
  const TILE_SIZE = ${s}u;
  var<workgroup> tileInput: array<${b}, ${s*s}>;
  var<workgroup> tileWeightQ: array<${b}, ${s*s}>;
  var<workgroup> tileWeightK: array<${b}, ${s*s}>;
  var<workgroup> tileWeightV: array<${b}, ${s*s}>;
  ${f.registerUniforms(I).declareVariables(w,S,x,g,y,_)}
  ${f.mainStart([s,s,1])}
    let batchIndex = workgroup_id.z / uniforms.num_heads;
    let headNumber = workgroup_id.z % uniforms.num_heads;
    let m = global_id.y;
    let n = global_id.x;

    let inputOffset = batchIndex * (uniforms.M * uniforms.K) + m * uniforms.K;
    let biasOffsetQ = headNumber * uniforms.head_size;
    let biasOffsetK = uniforms.hidden_size + biasOffsetQ;
    let biasOffsetV = uniforms.hidden_size + biasOffsetK;

    var valueQ = ${b}(0);
    var valueK = ${b}(0);
    var valueV = ${b}(0);
    for (var w: u32 = 0u; w < uniforms.K; w += TILE_SIZE) {
      if (m < uniforms.M && w + local_id.x < uniforms.K) {
        tileInput[TILE_SIZE * local_id.y + local_id.x] = input[inputOffset + w + local_id.x];
      }
      if (n < uniforms.N && w + local_id.y < uniforms.K) {
        let offset = n + (w + local_id.y) * uniforms.ldb;
        tileWeightQ[TILE_SIZE * local_id.y + local_id.x] = weight[biasOffsetQ + offset];
        tileWeightK[TILE_SIZE * local_id.y + local_id.x] = weight[biasOffsetK + offset];
        tileWeightV[TILE_SIZE * local_id.y + local_id.x] = weight[biasOffsetV + offset];
      }
      workgroupBarrier();
      for (var k: u32 = 0u; k<TILE_SIZE && w+k < uniforms.K; k++) {
        let inputTileOffset = TILE_SIZE * local_id.y + k;
        let weightTileOffset = TILE_SIZE * k + local_id.x;
        valueQ += tileInput[inputTileOffset] * tileWeightQ[weightTileOffset];
        valueK += tileInput[inputTileOffset] * tileWeightK[weightTileOffset];
        valueV += tileInput[inputTileOffset] * tileWeightV[weightTileOffset];
      }

      workgroupBarrier();
    }

    let headOffset = (m * uniforms.N + n) % uniforms.head_size;
    valueQ += bias[headOffset + biasOffsetQ];
    valueK += bias[headOffset + biasOffsetK];
    valueV += bias[headOffset + biasOffsetV];

    let offset = workgroup_id.z * uniforms.M * uniforms.N;
    if (m < uniforms.M && n < uniforms.N) {
      let outputIdx = offset + m * uniforms.N + n;
      output_q[outputIdx] = valueQ;
      output_k[outputIdx] = valueK;
      output_v[outputIdx] = valueV;
    }
  }`};return e.compute({name:"AttentionPrepare",shaderCache:{inputDependencies:["type","type","type"]},getRunData:()=>({outputs:[{dims:r,dataType:e.inputs[0].dataType,gpuDataType:0},{dims:r,dataType:e.inputs[0].dataType,gpuDataType:0},{dims:r,dataType:e.inputs[0].dataType,gpuDataType:0}],dispatchGroup:u,programUniforms:p}),getShaderSource:h},{inputs:l,outputs:[-1,-1,-1]})},Eo=(e,t)=>{let r=xo(e.inputs,t),[i,a,n]=Io(e,r);return er(e,i,a,n,e.inputs[4],void 0,void 0,void 0,e.inputs[5],r)}}),zo,Co,Ao,Oo,sm=q(()=>{Pe(),te(),re(),xe(),ae(),zo=(e,t)=>{if(!e||e.length!==5)throw new Error("BatchNormalization requires 5 inputs");let r=(i,a,n)=>{let s=a.length;if(s!==i.length)throw new Error(`${n}: num dimensions != ${s}`);a.forEach((u,l)=>{if(u!==i[l])throw new Error(`${n}: dim[${l}] do not match`)})};if(e[0].dims.length>1){let i=t.format==="NHWC"?t.spatial?e[0].dims.slice(-1):e[0].dims.slice(-1).concat(e[0].dims.slice(1,e[0].dims.length-1)):e[0].dims.slice(1,t.spatial?2:void 0);r(e[1].dims,i,"Invalid input scale"),r(e[2].dims,i,"Invalid input B"),r(e[3].dims,i,"Invalid input mean"),r(e[4].dims,i,"Invalid input var")}else r(e[1].dims,[1],"Invalid input scale"),r(e[2].dims,[1],"Invalid input B"),r(e[3].dims,[1],"Invalid input mean"),r(e[4].dims,[1],"Invalid input var")},Co=(e,t)=>{let{epsilon:r,spatial:i,format:a}=t,n=e[0].dims,s=i?ve(n[n.length-1]):1,u=a==="NHWC"&&n.length>1?s:1,l=O.size(n)/s,p=i,h=p?n.length:n,f=M("x",e[0].dataType,e[0].dims,s),g=M("scale",e[1].dataType,e[1].dims,u),y=M("bias",e[2].dataType,e[2].dims,u),_=M("inputMean",e[3].dataType,e[3].dims,u),w=M("inputVar",e[4].dataType,e[4].dims,u),S=Q("y",e[0].dataType,h,s),x=()=>{let I="";if(i)I=`let cOffset = ${n.length===1?"0u":a==="NHWC"?`outputIndices[${n.length-1}] / ${s}`:"outputIndices[1]"};`;else if(a==="NCHW")I=`
            ${S.indicesSet("outputIndices","0","0")}
            let cOffset = ${S.indicesToOffset("outputIndices")};`;else{I=`var cIndices = ${g.type.indices}(0);
                       cIndices[0] = outputIndices[${n.length-1}];`;for(let k=1;k<g.rank;k++)I+=`cIndices[${k}] = outputIndices[${k}];`;I+=`let cOffset = ${g.indicesToOffset("cIndices")};`}return I},b=I=>`
  const epsilon = ${r};
  ${I.registerUniform("outputSize","u32").declareVariables(f,g,y,_,w,S)}
  ${I.mainStart()}
  ${I.guardAgainstOutOfBoundsWorkgroupSizes("uniforms.outputSize")}
    var outputIndices = ${S.offsetToIndices(`global_idx * ${s}`)};
    ${x()}
    let scale = ${g.getByOffset("cOffset")};
    let bias = ${y.getByOffset("cOffset")};
    let inputMean = ${_.getByOffset("cOffset")};
    let inputVar = ${w.getByOffset("cOffset")};
    let x = ${f.getByOffset("global_idx")};
    let value = (x - inputMean) * inverseSqrt(inputVar + epsilon) * scale + bias;
    ${S.setByOffset("global_idx","value")}
  }`;return{name:"BatchNormalization",shaderCache:{hint:`${t.epsilon}_${t.format}_${i}_${s}`,inputDependencies:p?["rank","type","type","type","type"]:void 0},getShaderSource:b,getRunData:()=>({outputs:[{dims:e[0].dims,dataType:e[0].dataType}],dispatchGroup:{x:Math.ceil(l/64)},programUniforms:p?[{type:12,data:l},...Y(n)]:[{type:12,data:l}]})}},Ao=e=>he(e),Oo=(e,t)=>{let{inputs:r,outputCount:i}=e,a=Ao({...t,outputCount:i});if(ye.webgpu.validateInputContent&&zo(r,a),t.trainingMode)throw new Error("BatchNormalization trainingMode is not supported yet.");e.compute(Co(r,a))}}),Ro,Bo,Mo,om=q(()=>{re(),ae(),Ro=e=>{if(e[0].dims.length!==3)throw new Error("input should have 3 dimensions");if(![320,640,1280].includes(e[0].dims[2]))throw new Error("number of channels should be 320, 640 or 1280");if(e[1].dims.length!==1)throw new Error("bias is expected to have 1 dimensions");if(e[0].dims[2]!==e[1].dims[0])throw new Error("last dimension of input and bias are not the same")},Bo=e=>{let t=e[0].dims,r=e[0].dims[2],i=O.size(t)/4,a=e[0].dataType,n=M("input",a,t,4),s=M("bias",a,[r],4),u=M("residual",a,t,4),l=Q("output",a,t,4);return{name:"BiasAdd",getRunData:()=>({outputs:[{dims:t,dataType:e[0].dataType}],dispatchGroup:{x:Math.ceil(i/64)}}),getShaderSource:p=>`
  const channels = ${r}u / 4;
  ${p.declareVariables(n,s,u,l)}

  ${p.mainStart()}
    ${p.guardAgainstOutOfBoundsWorkgroupSizes(i)}
    let value = ${n.getByOffset("global_idx")}
      + ${s.getByOffset("global_idx % channels")} + ${u.getByOffset("global_idx")};
    ${l.setByOffset("global_idx","value")}
  }`}},Mo=e=>{Ro(e.inputs),e.compute(Bo(e.inputs))}}),No,ce,Do,Uo,Po,qo,Lo,Wo,Vo,Go,Ho,Fo,jo,Ko,Qo,Zo,tr,Yo,Or,Xo,Jo,eu,tu,ru,iu,au,nu,su,ou,uu,lu,du,pu,cu,hu,ji,fu,Ki,Qi,mu,gu,yu,_u,wu,bu,Zi=q(()=>{te(),re(),xe(),ae(),No=(e,t,r,i,a,n,s)=>{let u=Math.ceil(t/4),l="";typeof a=="string"?l=`${a}(a)`:l=a("a");let p=M("inputData",r,[u],4),h=Q("outputData",i,[u],4),f=[{name:"vec_size",type:"u32"}];return s&&f.push(...s),`
      ${e.registerUniforms(f).declareVariables(p,h)}

  ${n??""}

  ${e.mainStart()}
    ${e.guardAgainstOutOfBoundsWorkgroupSizes("uniforms.vec_size")}

    let a = ${p.getByOffset("global_idx")};
    ${h.setByOffset("global_idx",l)}
  }`},ce=(e,t,r,i,a,n=e.dataType,s,u)=>{let l=[{type:12,data:Math.ceil(O.size(e.dims)/4)}];return s&&l.push(...s),{name:t,shaderCache:{hint:a,inputDependencies:["type"]},getShaderSource:p=>No(p,O.size(e.dims),e.dataType,n,r,i,u),getRunData:p=>({outputs:[{dims:e.dims,dataType:n}],dispatchGroup:{x:Math.ceil(O.size(p[0].dims)/64/4)},programUniforms:l})}},Do=e=>{e.compute(ce(e.inputs[0],"Abs","abs"))},Uo=e=>{e.compute(ce(e.inputs[0],"Acos","acos"))},Po=e=>{e.compute(ce(e.inputs[0],"Acosh","acosh"))},qo=e=>{e.compute(ce(e.inputs[0],"Asin","asin"))},Lo=e=>{e.compute(ce(e.inputs[0],"Asinh","asinh"))},Wo=e=>{e.compute(ce(e.inputs[0],"Atan","atan"))},Vo=e=>{e.compute(ce(e.inputs[0],"Atanh","atanh"))},Go=e=>he(e),Ho=(e,t)=>{let r;switch(t.to){case 10:r="vec4<f16>";break;case 1:r="vec4<f32>";break;case 12:r="vec4<u32>";break;case 6:r="vec4<i32>";break;case 9:r="vec4<bool>";break;default:throw new RangeError(`not supported type (specified in attribute 'to' from 'Cast' operator): ${t.to}`)}e.compute(ce(e.inputs[0],"Cast",r,void 0,t.cacheKey,t.to))},Fo=e=>{let t,r,i=e.length>=2&&e[1].data!==0,a=e.length>=3&&e[2].data!==0;switch(e[0].dataType){case 1:t=i?e[1].getFloat32Array()[0]:-34028234663852886e22,r=a?e[2].getFloat32Array()[0]:34028234663852886e22;break;case 10:t=i?e[1].getUint16Array()[0]:64511,r=a?e[2].getUint16Array()[0]:31743;break;default:throw new Error("Unsupport data type")}return he({min:t,max:r})},jo=(e,t)=>{let r=t||Fo(e.inputs),i=ze(e.inputs[0].dataType);e.compute(ce(e.inputs[0],"Clip",a=>`clamp(${a}, vec4<${i}>(uniforms.min), vec4<${i}>(uniforms.max))`,void 0,r.cacheKey,void 0,[{type:e.inputs[0].dataType,data:r.min},{type:e.inputs[0].dataType,data:r.max}],[{name:"min",type:i},{name:"max",type:i}]),{inputs:[0]})},Ko=e=>{e.compute(ce(e.inputs[0],"Ceil","ceil"))},Qo=e=>{e.compute(ce(e.inputs[0],"Cos","cos"))},Zo=e=>{e.compute(ce(e.inputs[0],"Cosh","cosh"))},tr=e=>he(e),Yo=(e,t)=>{let r=ze(e.inputs[0].dataType);e.compute(ce(e.inputs[0],"Elu",i=>`elu_vf32(${i})`,`
  const elu_alpha_ = ${r}(${t.alpha});

  fn elu_f32(a: ${r}) -> ${r} {
  return select((exp(a) - 1.0) * elu_alpha_, a, a >= 0.0);
  }

  fn elu_vf32(v: vec4<${r}>) -> vec4<${r}> {
  return vec4(elu_f32(v.x), elu_f32(v.y), elu_f32(v.z), elu_f32(v.w));
  }`,t.cacheKey))},Or=(e="f32")=>`
const r0: ${e} = 0.3275911;
const r1: ${e} = 0.254829592;
const r2: ${e} = -0.284496736;
const r3: ${e} = 1.421413741;
const r4: ${e} = -1.453152027;
const r5: ${e} = 1.061405429;

fn erf_vf32(v: vec4<${e}>) -> vec4<${e}> {
  let absv = abs(v);
  let x = 1.0 / (1.0 + r0 * absv);
  return sign(v) * (1.0 - ((((r5 * x + r4) * x + r3) * x + r2) * x + r1) * x * exp(-absv * absv));
}`,Xo=e=>{let t=ze(e.inputs[0].dataType);e.compute(ce(e.inputs[0],"Erf",r=>`erf_vf32(${r})`,Or(t)))},Jo=e=>{e.compute(ce(e.inputs[0],"Exp","exp"))},eu=e=>{e.compute(ce(e.inputs[0],"Floor","floor"))},tu=e=>{let t=ze(e.inputs[0].dataType);e.compute(ce(e.inputs[0],"Gelu",r=>`0.5 * ${r} * (1.0 + erf_vf32(${r} * 0.7071067811865475))`,Or(t)))},ru=(e,t)=>{let r=ze(e.inputs[0].dataType);e.compute(ce(e.inputs[0],"LeakyRelu",i=>`select(leaky_relu_alpha_ * ${i}, ${i}, ${i} >= vec4<${r}>(0.0))`,`const leaky_relu_alpha_ = ${r}(${t.alpha});`,t.cacheKey))},iu=e=>{e.compute(ce(e.inputs[0],"Not",t=>`!${t}`))},au=e=>{e.compute(ce(e.inputs[0],"Neg",t=>`-${t}`))},nu=e=>{e.compute(ce(e.inputs[0],"Reciprocal",t=>`1.0/${t}`))},su=e=>{let t=ze(e.inputs[0].dataType);e.compute(ce(e.inputs[0],"Relu",r=>`select(vec4<${t}>(0.0), ${r}, ${r} > vec4<${t}>(0.0))`))},ou=e=>{e.compute(ce(e.inputs[0],"Sigmoid",t=>`(1.0 / (1.0 + exp(-${t})))`))},uu=e=>he(e),lu=(e,t)=>{let r=ze(e.inputs[0].dataType);e.compute(ce(e.inputs[0],"HardSigmoid",i=>`max(vec4<${r}>(0.0), min(vec4<${r}>(1.0), ${t.alpha} * ${i} + vec4<${r}>(${t.beta})))`,void 0,t.cacheKey))},du=e=>{e.compute(ce(e.inputs[0],"Sin","sin"))},pu=e=>{e.compute(ce(e.inputs[0],"Sinh","sinh"))},cu=e=>{e.compute(ce(e.inputs[0],"Sqrt","sqrt"))},hu=e=>{e.compute(ce(e.inputs[0],"Tan","tan"))},ji=e=>`sign(${e}) * (1 - exp(-2 * abs(${e}))) / (1 + exp(-2 * abs(${e})))`,fu=e=>{e.compute(ce(e.inputs[0],"Tanh",ji))},Ki=(e="f32")=>`
const fast_gelu_a: ${e} = 0.5;
const fast_gelu_b: ${e} = 0.7978845608028654;
const fast_gelu_c: ${e} = 0.035677408136300125;

fn tanh_v(v: vec4<${e}>) -> vec4<${e}> {
  return ${ji("v")};
}
`,Qi=e=>`(fast_gelu_a + fast_gelu_a * tanh_v(${e} * (fast_gelu_c * ${e} * ${e} + fast_gelu_b))) * ${e}`,mu=e=>{let t=ze(e.inputs[0].dataType);e.compute(ce(e.inputs[0],"FastGelu",Qi,Ki(t),void 0,e.inputs[0].dataType))},gu=(e,t)=>{let r=ze(e.inputs[0].dataType);return e.compute(ce(e.inputs[0],"ThresholdedRelu",i=>`select(vec4<${r}>(0.0), ${i}, ${i} > thresholded_relu_alpha_)`,`const thresholded_relu_alpha_ = vec4<${r}>(${t.alpha});`,t.cacheKey)),0},yu=e=>{e.compute(ce(e.inputs[0],"Log","log"))},_u=(e,t)=>`
const alpha = vec4<${e}>(${t});
const one = ${e}(1.0);
const zero = ${e}(0.0);

fn quick_gelu_impl(x: vec4<${e}>) -> vec4<${e}> {
  let v = x *alpha;
  var x1 : vec4<${e}>;
  for (var i = 0; i < 4; i = i + 1) {
    if (v[i] >= zero) {
      x1[i] = one / (one + exp(-v[i]));
    } else {
      x1[i] = one - one / (one + exp(v[i]));
    }
  }
  return x * x1;
}
`,wu=e=>`quick_gelu_impl(${e})`,bu=(e,t)=>{let r=ze(e.inputs[0].dataType);e.compute(ce(e.inputs[0],"QuickGelu",wu,_u(r,t.alpha),t.cacheKey,e.inputs[0].dataType))}}),$u,vu,xu,um=q(()=>{re(),ae(),Zi(),$u=e=>{if(e[0].dims.length!==3)throw new Error("input should have 3 dimensions");if(![2560,5120,10240].includes(e[0].dims[2]))throw new Error("hidden state should be 2560, 5120 or 10240");if(e[1].dims.length!==1)throw new Error("bias is expected to have 1 dimensions");if(e[0].dims[2]!==e[1].dims[0])throw new Error("last dimension of input and bias are not the same")},vu=e=>{let t=e[0].dims.slice();t[2]=t[2]/2;let r=M("input",e[0].dataType,e[0].dims,4),i=M("bias",e[0].dataType,[e[0].dims[2]],4),a=Q("output",e[0].dataType,t,4),n=O.size(t)/4,s=Te(e[0].dataType);return{name:"BiasSplitGelu",getRunData:()=>({outputs:[{dims:t,dataType:e[0].dataType}],dispatchGroup:{x:Math.ceil(n/64)}}),getShaderSource:u=>`
  const M_SQRT2 = sqrt(2.0);
  const halfChannels = ${e[0].dims[2]/4/2}u;

  ${u.declareVariables(r,i,a)}

  ${Or(s)}

  ${u.mainStart()}
    ${u.guardAgainstOutOfBoundsWorkgroupSizes(n)}
    let biasIdx = global_idx % halfChannels;
    let batchIndex = global_idx / halfChannels;
    let inputOffset = biasIdx + batchIndex * halfChannels * 2;
    let valueLeft = input[inputOffset] + bias[biasIdx];
    let valueRight = input[inputOffset + halfChannels] + bias[biasIdx + halfChannels];
    let geluRight = valueRight * 0.5 * (erf_vf32(valueRight / M_SQRT2) + 1);

    ${a.setByOffset("global_idx","valueLeft * geluRight")}
  }`}},xu=e=>{$u(e.inputs),e.compute(vu(e.inputs))}}),Su,Tu,je,ku,Iu,Eu,zu,Cu,Au,Ou,Ru,Bu,Mu,lm=q(()=>{te(),re(),ae(),Su=(e,t,r,i,a,n,s,u,l,p,h,f)=>{let g,y;typeof u=="string"?g=y=(b,I)=>`${u}((${b}),(${I}))`:typeof u=="function"?g=y=u:(g=u.scalar,y=u.vector);let _=Q("outputData",h,i.length,4),w=M("aData",l,t.length,4),S=M("bData",p,r.length,4),x;if(a)if(n){let b=O.size(t)===1,I=O.size(r)===1,k=t.length>0&&t[t.length-1]%4===0,E=r.length>0&&r[r.length-1]%4===0;b||I?x=_.setByOffset("global_idx",y(b?`${w.type.value}(${w.getByOffset("0")}.x)`:w.getByOffset("global_idx"),I?`${S.type.value}(${S.getByOffset("0")}.x)`:S.getByOffset("global_idx"))):x=`
            let outputIndices = ${_.offsetToIndices("global_idx * 4u")};
            let offsetA = ${w.broadcastedIndicesToOffset("outputIndices",_)};
            let offsetB = ${S.broadcastedIndicesToOffset("outputIndices",_)};
            ${_.setByOffset("global_idx",y(s||k?w.getByOffset("offsetA / 4u"):`${w.type.value}(${w.getByOffset("offsetA / 4u")}[offsetA % 4u])`,s||E?S.getByOffset("offsetB / 4u"):`${S.type.value}(${S.getByOffset("offsetB / 4u")}[offsetB % 4u])`))}
          `}else x=_.setByOffset("global_idx",y(w.getByOffset("global_idx"),S.getByOffset("global_idx")));else{if(!n)throw new Error("no necessary to use scalar implementation for element-wise binary op implementation.");let b=(I,k,E="")=>{let A=`aData[indexA${k}][componentA${k}]`,C=`bData[indexB${k}][componentB${k}]`;return`
            let outputIndices${k} = ${_.offsetToIndices(`global_idx * 4u + ${k}u`)};
            let offsetA${k} = ${w.broadcastedIndicesToOffset(`outputIndices${k}`,_)};
            let offsetB${k} = ${S.broadcastedIndicesToOffset(`outputIndices${k}`,_)};
            let indexA${k} = offsetA${k} / 4u;
            let indexB${k} = offsetB${k} / 4u;
            let componentA${k} = offsetA${k} % 4u;
            let componentB${k} = offsetB${k} % 4u;
            ${I}[${k}] = ${E}(${g(A,C)});
          `};h===9?x=`
            var data = vec4<u32>(0);
            ${b("data",0,"u32")}
            ${b("data",1,"u32")}
            ${b("data",2,"u32")}
            ${b("data",3,"u32")}
            outputData[global_idx] = dot(vec4<u32>(0x1, 0x100, 0x10000, 0x1000000), vec4<u32>(data));`:x=`
            ${b("outputData[global_idx]",0)}
            ${b("outputData[global_idx]",1)}
            ${b("outputData[global_idx]",2)}
            ${b("outputData[global_idx]",3)}
          `}return`
        ${e.registerUniform("vec_size","u32").declareVariables(w,S,_)}

        ${f??""}

        ${e.mainStart()}
        ${e.guardAgainstOutOfBoundsWorkgroupSizes("uniforms.vec_size")}
        ${x}
      }`},Tu=(e,t,r,i,a,n,s=r.dataType)=>{let u=r.dims.map(Number),l=i.dims.map(Number),p=!O.areEqual(u,l),h=u,f=O.size(u),g=!1,y=!1,_=[p];if(p){let w=Lt.calcShape(u,l,!1);if(!w)throw new Error("Can't perform binary op on the given tensors");h=w.slice(),f=O.size(h);let S=O.size(u)===1,x=O.size(l)===1,b=u.length>0&&u[u.length-1]%4===0,I=l.length>0&&l[l.length-1]%4===0;_.push(S),_.push(x),_.push(b),_.push(I);let k=1;for(let E=1;E<h.length;E++){let A=u[u.length-E],C=l[l.length-E];if(A===C)k*=A;else break}k%4===0?(y=!0,g=!0):(S||x||b||I)&&(g=!0)}else g=!0;return _.push(g),{name:e,shaderCache:{hint:t+_.map(w=>w.toString()).join("_"),inputDependencies:["rank","rank"]},getShaderSource:w=>Su(w,u,l,h,g,p,y,a,r.dataType,i.dataType,s,n),getRunData:()=>({outputs:[{dims:h,dataType:s}],dispatchGroup:{x:Math.ceil(f/64/4)},programUniforms:[{type:12,data:Math.ceil(O.size(h)/4)},...Y(u,l,h)]})}},je=(e,t,r,i,a,n)=>{e.compute(Tu(t,a??"",e.inputs[0],e.inputs[1],r,i,n))},ku=e=>{je(e,"Add",(t,r)=>`${t}+${r}`)},Iu=e=>{je(e,"Div",(t,r)=>`${t}/${r}`)},Eu=e=>{je(e,"Equal",{scalar:(t,r)=>`u32(${t}==${r})`,vector:(t,r)=>`vec4<u32>(${t}==${r})`},void 0,void 0,9)},zu=e=>{je(e,"Mul",(t,r)=>`${t}*${r}`)},Cu=e=>{let t=M("input",e.inputs[0].dataType,e.inputs[0].dims).type.value;je(e,"Pow",{scalar:(r,i)=>`pow_custom(${r},${i})`,vector:(r,i)=>`pow_vector_custom(${r},${i})`},`
    fn pow_custom(a : ${t}, b : ${t}) -> ${t} {
      if (b == ${t}(0.0)) {
        return ${t}(1.0);
      } else if (a < ${t}(0.0) && f32(b) != floor(f32(b))) {
        return ${t}(pow(f32(a), f32(b))); // NaN
      }
      return select(sign(a), ${t}(1.0), round(f32(abs(b) % ${t}(2.0))) != 1.0) * ${t}(${t==="i32"?"round":""}(pow(f32(abs(a)), f32(b))));
    }
    fn pow_vector_custom(a : vec4<${t}>, b : vec4<${t}>) -> vec4<${t}> {
      // TODO: implement vectorized pow
      return vec4<${t}>(pow_custom(a.x, b.x), pow_custom(a.y, b.y), pow_custom(a.z, b.z), pow_custom(a.w, b.w));
    }
      `)},Au=e=>{je(e,"Sub",(t,r)=>`${t}-${r}`)},Ou=e=>{je(e,"Greater",{scalar:(t,r)=>`u32(${t}>${r})`,vector:(t,r)=>`vec4<u32>(${t}>${r})`},void 0,void 0,9)},Ru=e=>{je(e,"Less",{scalar:(t,r)=>`u32(${t}<${r})`,vector:(t,r)=>`vec4<u32>(${t}<${r})`},void 0,void 0,9)},Bu=e=>{je(e,"GreaterOrEqual",{scalar:(t,r)=>`u32(${t}>=${r})`,vector:(t,r)=>`vec4<u32>(${t}>=${r})`},void 0,void 0,9)},Mu=e=>{je(e,"LessOrEqual",{scalar:(t,r)=>`u32(${t}<=${r})`,vector:(t,r)=>`vec4<u32>(${t}<=${r})`},void 0,void 0,9)}}),Nu,Du,Uu,Pu,qu,Lu,dm=q(()=>{te(),re(),xe(),ae(),Nu=(e,t)=>{if(!e||e.length<1)throw new Error("too few inputs");let r=0,i=e[r],a=i.dataType,n=i.dims.length;e.forEach((s,u)=>{if(u!==r){if(s.dataType!==a)throw new Error("input tensors should be one type");if(s.dims.length!==n)throw new Error("input tensors should have the same shape");s.dims.forEach((l,p)=>{if(p!==t&&l!==i.dims[p])throw new Error("non concat dimensions must match")})}})},Du=(e,t)=>`
  fn calculateInputIndex(index: u32) -> u32 {
    let sizeInConcatAxis = array<u32, ${e}u>(${t});
    for (var i: u32 = 0u; i < ${e}; i += 1u ) {
      if (index < sizeInConcatAxis[i]) {
        return i;
      }
    }
    return ${e}u;
  }`,Uu=(e,t)=>{let r=e.length,i=[];for(let a=0;a<r;++a){let n=t.setByOffset("global_idx",e[a].getByIndices("indices"));r===1?i.push(n):a===0?i.push(`if (inputIndex == ${a}u) { ${n} }`):a===r-1?i.push(`else { ${n} }`):i.push(`else if (inputIndex == ${a}) { ${n} }`)}return i.join(`
`)},Pu=(e,t,r,i)=>{let a=O.size(r),n=new Array(e.length),s=new Array(e.length),u=0,l=[],p=[],h=[{type:12,data:a}];for(let w=0;w<e.length;++w)u+=e[w].dims[t],n[w]=u,p.push(e[w].dims.length),s[w]=M(`input${w}`,i,p[w]),l.push("rank"),h.push({type:12,data:n[w]});for(let w=0;w<e.length;++w)h.push(...Y(e[w].dims));h.push(...Y(r));let f=Q("output",i,r.length),g=f.indicesGet("indices",t),y=Array.from(Array(n.length).keys()).map(w=>`uniforms.sizeInConcatAxis${w}`).join(","),_=w=>`

  ${(()=>{w.registerUniform("outputSize","u32");for(let S=0;S<e.length;S++)w.registerUniform(`sizeInConcatAxis${S}`,"u32");return w.declareVariables(...s,f)})()}

  ${Du(n.length,y)}

  ${w.mainStart()}
    ${w.guardAgainstOutOfBoundsWorkgroupSizes("uniforms.outputSize")}

    var indices = ${f.offsetToIndices("global_idx")};

    let inputIndex = calculateInputIndex(${g});
    if (inputIndex != 0u) {
      let sizeInConcatAxis = array<u32, ${n.length}u>(${y});
      ${g} -= sizeInConcatAxis[inputIndex - 1u];
    }

    ${Uu(s,f)}
  }`;return{name:"Concat",shaderCache:{hint:`${t}`,inputDependencies:l},getRunData:()=>({outputs:[{dims:r,dataType:i}],dispatchGroup:{x:Math.ceil(a/64)},programUniforms:h}),getShaderSource:_}},qu=(e,t)=>{let r=e.inputs,i=r[0].dims,a=O.normalizeAxis(t.axis,i.length);Nu(r,a);let n=i.slice();n[a]=r.reduce((u,l)=>u+(l.dims.length>a?l.dims[a]:0),0);let s=r.filter(u=>O.size(u.dims)>0);e.compute(Pu(s,a,n,r[0].dataType),{inputs:s})},Lu=e=>he({axis:e.axis})}),It,Et,zt,Yi,Ct=q(()=>{te(),re(),It=(e,t,r="f32")=>{switch(e.activation){case"Relu":return`value = max(value, ${t}(0.0));`;case"Sigmoid":return`value = (${t}(1.0) / (${t}(1.0) + exp(-value)));`;case"Clip":return`value = clamp(value, ${t}(${r}(uniforms.clip_min)), ${t}(${r}(uniforms.clip_max)));`;case"HardSigmoid":return`value = max(${t}(0.0), min(${t}(1.0), ${r}(uniforms.alpha) * value + ${r}(uniforms.beta)));`;case"LeakyRelu":return`value = select(${r}(uniforms.alpha) * value, value, value >= ${t}(0.0));`;case"Tanh":return`let e2x = exp(-2.0 * abs(value));
              value = sign(value) * (1.0 - e2x) / (1.0 + e2x);
        `;case"":return"";default:throw new Error(`Unsupported activation ${e.activation}`)}},Et=(e,t)=>{e.activation==="Clip"?t.push({type:1,data:e.clipMax},{type:1,data:e.clipMin}):e.activation==="HardSigmoid"?t.push({type:1,data:e.alpha},{type:1,data:e.beta}):e.activation==="LeakyRelu"&&t.push({type:1,data:e.alpha})},zt=(e,t)=>{e.activation==="Clip"?t.push({name:"clip_max",type:"f32"},{name:"clip_min",type:"f32"}):e.activation==="HardSigmoid"?t.push({name:"alpha",type:"f32"},{name:"beta",type:"f32"}):e.activation==="LeakyRelu"&&t.push({name:"alpha",type:"f32"})},Yi=e=>{let t=(e==null?void 0:e.activation)||"";if(t==="HardSigmoid"){let[r,i]=(e==null?void 0:e.activation_params)||[.2,.5];return{activation:t,alpha:r,beta:i}}else if(t==="Clip"){let[r,i]=(e==null?void 0:e.activation_params)||[ls,ds];return{activation:t,clipMax:i,clipMin:r}}else if(t==="LeakyRelu"){let[r]=(e==null?void 0:e.activation_params)||[.01];return{activation:t,alpha:r}}return{activation:t}}}),Ie,Wu,Xi=q(()=>{Ie=(e,t)=>{switch(e){case 1:return t;case 2:return`vec2<${t}>`;case 3:return`vec3<${t}>`;case 4:return`vec4<${t}>`;default:throw new Error(`${e}-component is not supported.`)}},Wu=e=>`
      ${e?"value = value + getBiasByOutputCoords(coords);":""}
      `}),Vu,pm=q(()=>{Vu=e=>`
fn getIndexFromCoords4D(coords : vec4<i32>, shape : vec4<i32>) -> i32 {
  return dot(coords, vec4<i32>(
      shape.y * shape.z * shape.w, shape.z * shape.w, shape.w, 1));
}
fn getOutputIndexFromCoords(coords : vec4<i32>) -> i32 {
  return dot(coords, vec4<i32>(
    i32(${e}.x), i32(${e}.y), i32(${e}.z), 1));
}
`}),rr,Ji,ea=q(()=>{te(),re(),ae(),Ct(),rr=(e,t,r,i,a)=>{let n=i-r;return`
      ${Array.from({length:r}).map((s,u)=>`
      if (${Z(t.shape,u,t.rank)} != 1) {
        ${t.indicesSet(e,u,Z(a,u+n,i))}
      } else {
        ${t.indicesSet(e,u,0)}
      }`).join("")}
`},Ji=(e,t,r,i,a=!1,n)=>{let s=e[0].dims,u=e[1].dims,l=s[s.length-2],p=u[u.length-1],h=s[s.length-1],f=ve(p),g=ve(h),y=ve(l),_=O.size(r)/f/y,w=e.length>2,S=i?i.slice(0,-2):r.slice(0,-2),x=[O.size(S),l,p],b=[{type:12,data:_},{type:12,data:l},{type:12,data:p},{type:12,data:h}];Et(t,b),b.push(...Y(S,s,u)),w&&b.push(...Y(e[2].dims)),b.push(...Y(x));let I=k=>{let E=qi("batch_dims",e[0].dataType,S.length),A=M("a",e[0].dataType,s.length,g),C=M("b",e[1].dataType,u.length,f),$=Q("output",e[0].dataType,x.length,f),N=Te($.type.tensor),D=It(t,$.type.value,N),G=[A,C],V="";if(w){let K=a?f:1;G.push(M("bias",e[2].dataType,e[2].dims.length,K)),V=`${a?`value += bias[col / ${K}];`:`value += ${$.type.value}(bias[row + i]);`}`}let j=[{name:"output_size",type:"u32"},{name:"M",type:"u32"},{name:"N",type:"u32"},{name:"K",type:"u32"}];zt(t,j);let R=()=>{let K=`var a_data: ${A.type.value};`;for(let F=0;F<g;F++)K+=`
              let b_data${F} = b[(b_offset + (k + ${F}) * uniforms.N + col) / ${f}];`;for(let F=0;F<y;F++){K+=`a_data = a[(a_offset + (row + ${F}) * uniforms.K + k) / ${g}];`;for(let X=0;X<g;X++)K+=`
            values[${F}] = fma(${C.type.value}(a_data${g===1?"":`[${X}]`}), b_data${X}, values[${F}]);
`}return K};return`
  ${k.registerUniforms(j).registerInternalVariables(E).declareVariables(...G,$)}
  ${k.mainStart()}
    ${k.guardAgainstOutOfBoundsWorkgroupSizes("uniforms.output_size")}
    let col = (global_idx % (uniforms.N / ${f})) * ${f};
    var index1 = global_idx / (uniforms.N / ${f});
    let stride1 = uniforms.M / ${y};
    let row = (index1 % stride1) * ${y};
    let batch = index1 / stride1;

    ${r.length===2?"":`let batch_indices = ${E.offsetToIndices("batch")};`}

    var a_indices: ${A.type.indices};
    ${rr("a_indices",A,A.rank-2,E.rank,"batch_indices")}
    ${A.indicesSet("a_indices",A.rank-2,0)}
    ${A.indicesSet("a_indices",A.rank-1,0)}
    let a_offset = ${A.indicesToOffset("a_indices")};

    var b_indices: ${C.type.indices};
    ${rr("b_indices",C,C.rank-2,E.rank,"batch_indices")}
    ${C.indicesSet("b_indices",C.rank-2,0)}
    ${C.indicesSet("b_indices",C.rank-1,0)}
    let b_offset = ${C.indicesToOffset("b_indices")};
    var values: array<${$.type.value}, ${y}>;
    for (var k: u32 = 0u; k < uniforms.K; k = k + ${g}) {
      ${R()}
    }
    for (var i = 0u; i < ${y}u; i++) {
      var value = values[i];
      ${V}
      ${D}
      let cur_indices = ${$.type.indices}(batch, row + i, col);
      let offset = ${$.indicesToOffset("cur_indices")};
      ${$.setByOffset(`offset / ${f}`,"value")};
    }
  }
  `};return{name:"MatMulNaive",shaderCache:{hint:`${t.activation};${f};${g};${y};${a}`,inputDependencies:w?["rank","rank","rank"]:["rank","rank"]},getRunData:()=>({outputs:[{dims:n?n(r):r,dataType:e[0].dataType}],dispatchGroup:{x:Math.ceil(_/64)},programUniforms:b}),getShaderSource:I}}}),Gu,Hu,ta,ra,Fu,ia,ju,Rr,aa=q(()=>{te(),re(),ae(),Ct(),ea(),Xi(),Gu=(e,t)=>e?`
        mm_Asub[inputRow][inputCol] = mm_readA(batch,
          kStart + inputRow,
          globalRowStart / innerElementSize + inputCol${t?", batchIndices":""});
        `:`
        mm_Asub[inputRow][inputCol] = mm_readA(batch,
          globalRow + innerRow,
          kStart / innerElementSize + inputCol${t?", batchIndices":""});
        `,Hu=(e,t)=>e?`
        let ACached0 = mm_Asub[k * innerElementSize][localRow];
        let ACached1 = mm_Asub[k * innerElementSize + 1][localRow];
        let ACached2 = mm_Asub[k * innerElementSize + 2][localRow];
        ${t===3?"":"let ACached3 = mm_Asub[k * innerElementSize + 3][localRow];"}
        for (var i = 0; i < rowPerThread; i = i + 1) {
          acc[i] = BCached0 * ACached0[i] + acc[i];
          acc[i] = BCached1 * ACached1[i] + acc[i];
          acc[i] = BCached2 * ACached2[i] + acc[i];
          ${t===3?"":"acc[i] = BCached3 * ACached3[i] + acc[i];"}
        }`:`
        for (var i = 0; i < rowPerThread; i = i + 1) {
          let ACached = mm_Asub[tileRow + i][k];
          acc[i] = BCached0 * ACached.x + acc[i];
          acc[i] = BCached1 * ACached.y + acc[i];
          acc[i] = BCached2 * ACached.z + acc[i];
          ${t===3?"":"acc[i] = BCached3 * ACached.w + acc[i];"}
        }`,ta=(e,t,r="f32",i,a=!1,n=32,s=!1,u=32)=>{let l=t[1]*e[1],p=t[0]*e[0],h=a?l:n,f=a?n:l,g=h/t[0],y=n/t[1];if(!((a&&g===4&&e[1]===4||!a&&(g===3||g===4))&&h%t[0]===0&&n%t[1]===0&&e[0]===4))throw new Error(`If transposeA ${a} is true, innerElementSize ${g} and workPerThread[1] ${e[1]} must be 4.
      Otherwise, innerElementSize ${g} must be 3 or 4.
  tileAWidth ${h} must be divisible by workgroupSize[0]${t[0]}. tileInner ${n} must be divisible by workgroupSize[1] ${t[1]}. colPerThread ${e[0]} must be 4.`);return`
var<workgroup> mm_Asub: array<array<vec${g}<${r}>, ${h/g}>, ${f}>;
var<workgroup> mm_Bsub: array<array<vec4<${r}>, ${p/e[0]}>, ${n}>;

const rowPerThread = ${e[1]};
const colPerThread = ${e[0]};
const innerElementSize = ${g};
const tileInner = ${n};

@compute @workgroup_size(${t[0]}, ${t[1]}, ${t[2]})
fn main(@builtin(local_invocation_id) localId : vec3<u32>,
        @builtin(global_invocation_id) globalId : vec3<u32>,
        @builtin(workgroup_id) workgroupId : vec3<u32>) {
  let localRow = i32(localId.y);
  let tileRow = localRow * rowPerThread;
  let tileCol = i32(localId.x);

  let globalRow =i32(globalId.y) * rowPerThread;
  let globalCol = i32(globalId.x);
  let batch = ${s?"0":"i32(globalId.z)"};
  ${i?`let batchIndices = ${i.offsetToIndices("u32(batch)")};`:""}
  let globalRowStart = i32(workgroupId.y) * ${l};

  let num_tiles = ${s?`${Math.ceil(u/n)}`:"(uniforms.dim_inner - 1) / tileInner + 1"};
  var kStart = ${s?`i32(globalId.z) * ${u}`:"0"};

  var acc: array<vec4<${r}>, rowPerThread>;

  // Loop over shared dimension.
  let tileRowB = localRow * ${y};
  for (var t = 0; t < num_tiles; t = t + 1) {
      // Load one tile of A into local memory.
      for (var innerRow = 0; innerRow < rowPerThread; innerRow = innerRow + 1) {
          let inputRow = tileRow + innerRow;
          let inputCol = tileCol;
          ${Gu(a,i)}
      }

      // Load one tile of B into local memory.
      for (var innerRow = 0; innerRow < ${y}; innerRow = innerRow + 1) {
          let inputRow = tileRowB + innerRow;
          let inputCol = tileCol;
          mm_Bsub[inputRow][inputCol] = mm_readB(batch, kStart + inputRow, globalCol${i?", batchIndices":""});
      }
      kStart = kStart + tileInner;
      workgroupBarrier();

      // Compute acc values for a single thread.
      for (var k = 0; k < tileInner / innerElementSize; k = k + 1) {
          let BCached0 = mm_Bsub[k * innerElementSize][tileCol];
          let BCached1 = mm_Bsub[k * innerElementSize + 1][tileCol];
          let BCached2 = mm_Bsub[k * innerElementSize + 2][tileCol];
          ${g===3?"":"let BCached3 = mm_Bsub[k * innerElementSize + 3][tileCol];"}

          ${Hu(a,g)}
      }

      workgroupBarrier();
  }

  for (var innerRow = 0; innerRow < rowPerThread; innerRow = innerRow + 1) {
      mm_write(batch, globalRow + innerRow, globalCol, acc[innerRow]);
  }
}`},ra=(e,t)=>e?`
            mm_Asub[inputRow][inputCol] = mm_readA(batch,
              kStart + inputRow,
              globalRowStart + inputCol${t?", batchIndices":""});
            `:`
            mm_Asub[inputRow][inputCol] = mm_readA(batch,
              globalRowStart + inputRow,
              kStart + inputCol${t?", batchIndices":""});
            `,Fu=e=>e?"let ACached = mm_Asub[k][tileRow + innerRow];":"let ACached = mm_Asub[tileRow + innerRow][k];",ia=(e,t,r="f32",i,a=!1,n=32,s=!1,u=32,l=!1)=>{let p=e[1]*t[1],h=e[0]*t[0],f=a?p:n,g=a?n:p;if(!(g%t[1]===0&&f%t[0]===0&&n%t[1]===0))throw new Error(`tileAHight ${g} must be divisible by workgroupSize[1]${t[1]}, tileAWidth ${f} must be divisible by workgroupSize[0]${t[0]}, tileInner ${n} must be divisible by workgroupSize[1]${t[1]}`);let y=g/t[1],_=f/t[0],w=n/t[1],S=l?`
    let localRow = i32(localId.y);
    let localCol = i32(localId.x);
    let globalRowStart = i32(workgroupId.y) * ${p};
    let globalColStart = i32(workgroupId.x) * ${h};

    // Loop over shared dimension.
    for (var t = 0; t < num_tiles; t = t + 1) {
      // Load one tile of A into local memory.
      for (var inputRow = localRow; inputRow < ${g}; inputRow = inputRow + ${t[1]}) {
        for (var inputCol = localCol; inputCol < ${f}; inputCol = inputCol + ${t[0]}) {
          ${ra(a,i)}
        }
      }
      // Load one tile of B into local memory.
      for (var inputRow = localRow; inputRow < ${n}; inputRow = inputRow + ${t[1]}) {
            for (var inputCol = localCol; inputCol < ${h}; inputCol = inputCol + ${t[0]}) {
          mm_Bsub[inputRow][inputCol] = mm_readB(batch,
            kStart + inputRow,
            globalColStart + inputCol${i?", batchIndices":""});
        }
      }
      kStart = kStart + tileInner;
      workgroupBarrier();

      // Compute acc values for a single thread.
      var BCached : array<${r}, colPerThread>;
      for (var k = 0; k < tileInner; k = k + 1) {
        for (var inner = 0; inner < colPerThread; inner = inner + 1) {
          BCached[inner] = mm_Bsub[k][localCol + inner * ${t[0]}];
        }
        for (var innerRow = 0; innerRow < rowPerThread; innerRow = innerRow + 1) {
          let ACached = ${a?`mm_Asub[k][localRow + innerRow * ${t[1]}];`:`mm_Asub[localRow + innerRow * ${t[1]}][k];`}
          for (var innerCol = 0; innerCol < colPerThread; innerCol = innerCol + 1) {
            acc[innerRow][innerCol] = acc[innerRow][innerCol] +
                ACached * BCached[innerCol];
          }
        }
      }
      workgroupBarrier();
    }
    for (var innerRow = 0; innerRow < rowPerThread; innerRow = innerRow + 1) {
      let gRow = globalRowStart + localRow + innerRow * ${t[1]};
      for (var innerCol = 0; innerCol < colPerThread; innerCol = innerCol + 1) {
        let gCol = globalColStart + localCol + innerCol * ${t[0]};
        mm_write(batch, gRow, gCol, acc[innerRow][innerCol]);
      }
    }
    `:`
let tileRow = i32(localId.y) * rowPerThread;
let tileCol = i32(localId.x) * colPerThread;

let globalRow = i32(globalId.y) * rowPerThread;
let globalCol = i32(globalId.x) * colPerThread;
let globalRowStart = i32(workgroupId.y) * ${p};

let tileRowA = i32(localId.y) * ${y};
let tileColA = i32(localId.x) * ${_};
let tileRowB = i32(localId.y) * ${w};
// Loop over shared dimension.
for (var t = 0; t < num_tiles; t = t + 1) {
  // Load one tile of A into local memory.
  for (var innerRow = 0; innerRow < ${y}; innerRow = innerRow + 1) {
    for (var innerCol = 0; innerCol < ${_}; innerCol = innerCol + 1) {
      let inputRow = tileRowA + innerRow;
      let inputCol = tileColA + innerCol;
      ${ra(a,i)}
    }
  }

  // Load one tile of B into local memory.
  for (var innerRow = 0; innerRow < ${w}; innerRow = innerRow + 1) {
    for (var innerCol = 0; innerCol < colPerThread; innerCol = innerCol + 1) {
      let inputRow = tileRowB + innerRow;
      let inputCol = tileCol + innerCol;
      mm_Bsub[inputRow][inputCol] = mm_readB(batch,
        kStart + inputRow,
        globalCol + innerCol${i?", batchIndices":""});
    }
  }
  kStart = kStart + tileInner;
  workgroupBarrier();

  // Compute acc values for a single thread.
  var BCached : array<${r}, colPerThread>;
  for (var k = 0; k < tileInner; k = k + 1) {
    for (var inner = 0; inner < colPerThread; inner = inner + 1) {
      BCached[inner] = mm_Bsub[k][tileCol + inner];
    }

    for (var innerRow = 0; innerRow < rowPerThread; innerRow = innerRow + 1) {
      ${Fu(a)}
      for (var innerCol = 0; innerCol < colPerThread; innerCol = innerCol + 1) {
        acc[innerRow][innerCol] = acc[innerRow][innerCol] + ACached * BCached[innerCol];
      }
    }
  }

  workgroupBarrier();
}

for (var innerRow = 0; innerRow < rowPerThread; innerRow = innerRow + 1) {
  for (var innerCol = 0; innerCol < colPerThread; innerCol = innerCol + 1) {
    mm_write(batch, globalRow + innerRow, globalCol + innerCol,
        acc[innerRow][innerCol]);
  }
}
`;return`
  var<workgroup> mm_Asub : array<array<${r}, ${f}>, ${g}>;
  var<workgroup> mm_Bsub : array<array<${r}, ${h}>, ${n}>;
  const rowPerThread = ${e[1]};
  const colPerThread = ${e[0]};
  const tileInner = ${n};

@compute @workgroup_size(${t[0]}, ${t[1]}, ${t[2]})
fn main(@builtin(local_invocation_id) localId : vec3<u32>,
        @builtin(global_invocation_id) globalId : vec3<u32>,
        @builtin(workgroup_id) workgroupId : vec3<u32>) {
    let batch = ${s?"0":"i32(globalId.z)"};
    ${i?`let batchIndices = ${i.offsetToIndices("u32(batch)")};`:""}
    let num_tiles = ${s?`${Math.ceil(u/n)}`:"(uniforms.dim_inner - 1) / tileInner + 1"};
    var kStart = ${s?`i32(globalId.z) * ${u}`:"0"};

    var acc : array<array<${r}, colPerThread>, rowPerThread>;
    ${S}
  }
`},ju=(e,t,r,i,a=!1)=>{let[n,s,u,l]=i,p=Te(i[0].type.tensor);return`
    fn mm_readA(batch: i32, row: i32, colIn: i32, batchIndices: ${n.type.indices}) -> ${Ie(e,p)} {
      var value = ${Ie(e,p)}(0.0);
      let col = colIn * ${e};
      if(row < uniforms.dim_a_outer && col < uniforms.dim_inner)
      {
        var aIndices: ${s.type.indices};
        ${rr("aIndices",s,s.rank-2,n.rank,"batchIndices")}
        ${s.indicesSet("aIndices",s.rank-2,"u32(row)")}
        ${s.indicesSet("aIndices",s.rank-1,"u32(colIn)")}
        value = ${s.getByIndices("aIndices")};
      }
      return value;
    }

    fn mm_readB(batch: i32, row: i32, colIn: i32, batchIndices: ${n.type.indices}) -> ${Ie(e,p)} {
      var value = ${Ie(e,p)}(0.0);
      let col = colIn * ${e};
      if(row < uniforms.dim_inner && col < uniforms.dim_b_outer)
      {
        var bIndices: ${u.type.indices};
        ${rr("bIndices",u,u.rank-2,n.rank,"batchIndices")}
        ${u.indicesSet("bIndices",u.rank-2,"u32(row)")}
        ${u.indicesSet("bIndices",u.rank-1,"u32(colIn)")}
        value = ${u.getByIndices("bIndices")};
      }
      return value;
    }

    fn mm_write(batch: i32, row: i32, colIn: i32, valueIn: ${Ie(e,p)}) {
      let col = colIn * ${e};
      if (row < uniforms.dim_a_outer && col < uniforms.dim_b_outer) {
        var value = valueIn;
        let coords = vec3<i32>(batch, row, colIn);
        ${t?`value = value + ${a?"bias[colIn]":`${Ie(e,p)}(bias[row])`};`:""}
        ${r}
        ${l.setByIndices("vec3<u32>(coords)","value")}
      }
    }
    `},Rr=(e,t,r,i,a=!1,n)=>{let s=e[0].dims,u=e[1].dims,l=s.slice(0,-2),p=u.slice(0,-2),h=i?i.slice(0,-2):r.slice(0,-2),f=O.size(h),g=s[s.length-2],y=s[s.length-1],_=u[u.length-1],w=y%4===0&&_%4===0,S=g<=8?[4,1,1]:[4,4,1],x=[8,8,1],b=[Math.ceil(_/x[0]/S[0]),Math.ceil(g/x[1]/S[1]),Math.ceil(f/x[2]/S[2])],I=w?4:1,k=[...l,g,y/I],E=k.length,A=[...p,y,_/I],C=A.length,$=[f,g,_/I],N=[{type:6,data:g},{type:6,data:_},{type:6,data:y}];Et(t,N),N.push(...Y(h,k,A));let D=["rank","rank"],G=e.length>2;G&&(N.push(...Y(e[2].dims)),D.push("rank")),N.push(...Y($));let V=j=>{let R=h.length,K=qi("batchDims",e[0].dataType,R,1),F=Te(e[0].dataType),X=M("a",e[0].dataType,E,I),le=M("b",e[1].dataType,C,I),L=Q("result",e[0].dataType,$.length,I),me=[X,le];if(G){let $e=a?I:1;me.push(M("bias",e[2].dataType,e[2].dims.length,$e))}let U=[{name:"dim_a_outer",type:"i32"},{name:"dim_b_outer",type:"i32"},{name:"dim_inner",type:"i32"}];zt(t,U);let P=Te(L.type.tensor),J=It(t,L.type.value,P),ee=ju(I,G,J,[K,X,le,L],a);return`
  ${j.registerUniforms(U).registerInternalVariables(K).declareVariables(...me,L)}
  ${ee}
  ${w?ta(S,x,F,K):ia(S,x,F,K)}
                   `};return{name:"MatMul",shaderCache:{hint:`${S};${t.activation};${w};${a}`,inputDependencies:D},getRunData:()=>({outputs:[{dims:n?n(r):r,dataType:e[0].dataType}],dispatchGroup:{x:b[0],y:b[1],z:b[2]},programUniforms:N}),getShaderSource:V}}}),Ku,Qu,cm=q(()=>{te(),at(),ae(),Ct(),Xi(),pm(),aa(),Ku=(e,t,r,i,a=!1,n,s=4,u=4,l=4,p="f32")=>{let h=N=>{switch(N){case 1:return"resData = x[xIndex];";case 3:return`resData = vec3<${p}>(x[xIndex], x[xIndex + 1], x[xIndex + 2]);`;case 4:return"resData = x[xIndex / 4];";default:throw new Error(`innerElementSize ${N} is not supported.`)}},f=N=>{switch(N){case 1:return"return w[row * i32(uniforms.w_shape[3]) + colIn];";case 4:return"return w[row * i32(uniforms.w_shape[3]) / 4 + colIn];";default:throw new Error(`innerElementSize ${N} is not supported.`)}},g=e?`
    let coord = vec4<i32>(batch, xRow, xCol, xCh);
    `:`
    let coord = vec4<i32>(batch, xCh, xRow, xCol);
    `,y=e?`
    let coords = vec4<i32>(
      batch,
      row / outWidth,
      row % outWidth,
      col);
    `:`
    let coords = vec4<i32>(
      batch,
      row,
      col / outWidth,
      col % outWidth);
    `,_=e?"i32(uniforms.x_shape[1])":"i32(uniforms.x_shape[2])",w=e?"i32(uniforms.x_shape[2])":"i32(uniforms.x_shape[3])",S=e?"row":"col",x=e?"col":"row",b=`
    let inChannels = i32(uniforms.w_shape[2]);
    let outWidth = ${e?"i32(uniforms.result_shape[2])":"i32(uniforms.result_shape[3])"};
    let outRow = ${S} / outWidth;
    let outCol = ${S} % outWidth;

    let WRow = ${x} / (i32(uniforms.w_shape[1]) * inChannels);
    let WCol = ${x} / inChannels % i32(uniforms.w_shape[1]);
    let xRow = outRow * uniforms.stride[0] + uniforms.dilation[0] * WRow - uniforms.pad[0];
    let xCol = outCol * uniforms.stride[1] + uniforms.dilation[1] * WCol - uniforms.pad[1];
    let xCh = ${x} % inChannels;
    var resData = ${Ie(s,p)}(0.0);
    // The bounds checking is always needed since we use it to pad zero for
    // the 'same' padding type.
    if (xRow >= 0 && xRow < ${_} && xCol >= 0 && xCol < ${w}) {
      ${g}
      let xIndex = getIndexFromCoords4D(coord, vec4<i32>(uniforms.x_shape));
      ${h(s)}
    }
    return resData;`,I=e?t&&i?`
    let col = colIn * ${s};
    ${b}`:`
    let col = colIn * ${s};
    if (row < uniforms.dim_a_outer && col < uniforms.dim_inner) {
      ${b}
    }
    return ${Ie(s,p)}(0.0);`:i&&r?`
    let col = colIn * ${s};
    ${b}`:`
    let col = colIn * ${s};
    if (row < uniforms.dim_inner && col < uniforms.dim_b_outer) {
      ${b}
    }
    return ${Ie(s,p)}(0.0);`,k=e?i&&r?f(u):`
    let col = colIn * ${u};
    if (row < uniforms.dim_inner && col < uniforms.dim_b_outer) {
      ${f(u)}
    }
    return ${Ie(u,p)}(0.0);`:`
    let col = colIn * ${u};
    if (row < uniforms.dim_inner && col < uniforms.dim_a_outer) {
      ${f(u)}
    }
    return ${Ie(u,p)}(0.0);`,E=Ie(l,p),A=Ie(e?s:u,p),C=Ie(e?u:s,p),$=It(n,E,p);return`
    fn mm_readA(batch: i32, row : i32, colIn : i32) -> ${A} {
      ${e?I:k}
    }

    fn mm_readB(batch: i32, row : i32, colIn : i32) -> ${C} {
      ${e?k:I}
    }

    fn mm_write(batch: i32, row : i32, colIn : i32, valueIn : ${E}) {
      let col = colIn * ${l};
      if (row < uniforms.dim_a_outer && col < uniforms.dim_b_outer)
      {
      var value = valueIn;
      let outWidth = ${e?"i32(uniforms.result_shape[2])":"i32(uniforms.result_shape[3])"};
      ${y}
      ${Wu(a)}
      ${$}
      setOutputAtCoords(coords[0], coords[1], coords[2], coords[3], value);
      }
    }`},Qu=(e,t,r,i,a,n,s,u,l)=>{let p=t.format==="NHWC",h=p?e[0].dims[3]:e[0].dims[1],f=r[0],g=p?r[2]:r[3],y=p?r[1]:r[2],_=p?r[3]:r[1],w=p&&(h%4===0||h%3===0)&&_%4===0,S=p?_:g*y,x=p?g*y:_,b=[8,8,1],I=i<=8?[4,1,1]:[4,4,1],k=[Math.ceil(S/b[0]/I[0]),Math.ceil(x/b[1]/I[1]),Math.ceil(f/b[2]/I[2])];de("verbose",()=>`[conv2d_mm_webgpu] dispatch = ${k}`);let E=w?p&&h%4!==0?3:4:1,A=b[1]*I[1],C=b[0]*I[0],$=Math.max(b[0]*E,b[1]),N=i%A===0,D=a%C===0,G=n%$===0,V=w?[E,4,4]:[1,1,1],j=[{type:6,data:i},{type:6,data:a},{type:6,data:n},{type:6,data:[t.pads[0],t.pads[1]]},{type:6,data:t.strides},{type:6,data:t.dilations}];Et(t,j),j.push(...Y(e[0].dims,e[1].dims));let R=["rank","rank"];s&&(j.push(...Y(e[2].dims)),R.push("rank")),j.push(...Y(r));let K=F=>{let X=[{name:"dim_a_outer",type:"i32"},{name:"dim_b_outer",type:"i32"},{name:"dim_inner",type:"i32"},{name:"pad",type:"i32",length:2},{name:"stride",type:"i32",length:2},{name:"dilation",type:"i32",length:2}];zt(t,X);let le=w?4:1,L=Te(e[0].dataType),me=`
      fn setOutputAtIndex(flatIndex : i32, value : ${w?`vec4<${L}>`:L}) {
        result[flatIndex] = ${w?`vec4<${L}>`:L}(value);
      }
      fn setOutputAtCoords(d0 : i32, d1 : i32, d2 : i32, d3 : i32, value : ${w?`vec4<${L}>`:L}) {
        let flatIndex = getOutputIndexFromCoords(vec4<i32>(d0, d1, d2, d3));
        setOutputAtIndex(flatIndex ${w?"/ 4":""}, value);
      }`,U=M("x",e[0].dataType,e[0].dims.length,E===3?1:E),P=M("w",e[1].dataType,e[1].dims.length,le),J=[U,P],ee=Q("result",e[0].dataType,r.length,le);if(s){let $e=M("bias",e[2].dataType,e[2].dims.length,le);J.push($e),me+=`
        fn getBiasByOutputCoords(coords : vec4<i32>) -> ${w?`vec4<${L}>`:L} {
          return bias[coords.${p?"w":"y"}${w?"/ 4":""}];
        }`}return`
        ${Vu("uniforms.result_strides")}
        //struct Uniforms { xShape : vec4<i32>, wShape : vec4<i32>, outShape : vec4<i32>,
        //  outShapeStrides: vec3<i32>, filterDims : vec2<i32>, pad : vec2<i32>, stride : vec2<i32>,
        //  dilation : vec2<i32>, dimAOuter : i32, dimBOuter : i32, dimInner : i32 };
        ${F.registerUniforms(X).declareVariables(...J,ee)}
        ${me}
        ${Ku(p,N,D,G,s,t,V[0],V[1],V[2],L)}
        ${w?ta(I,b,L,void 0,!p,$):ia(I,b,L,void 0,!p,$,!1,void 0,u)}`};return{name:"Conv2DMatMul",shaderCache:{hint:`${t.cacheKey};${E};${w};${N};${D};${G};${A};${C};${$}`,inputDependencies:R},getRunData:()=>({outputs:[{dims:l?l(r):r,dataType:e[0].dataType}],dispatchGroup:{x:k[0],y:k[1],z:k[2]},programUniforms:j}),getShaderSource:K}}}),Zu,na,ir,Yu,sa,Xu,Ju,el,hm=q(()=>{te(),at(),re(),ae(),Ct(),Xi(),Zu=e=>{let t=1;for(let r=0;r<e.length;r++)t*=e[r];return t},na=e=>typeof e=="number"?[e,e,e]:e,ir=(e,t)=>t<=1?e:e+(e-1)*(t-1),Yu=(e,t,r,i=1)=>{let a=ir(t,i);return Math.floor((e[0]*(r-1)-r+a)/2)},sa=(e,t,r,i,a)=>{a==null&&(a=Yu(e,t[0],i[0]));let n=[0,0,0,r];for(let s=0;s<3;s++)e[s]+2*a>=t[s]&&(n[s]=Math.trunc((e[s]-t[s]+2*a)/i[s]+1));return n},Xu=(e,t,r,i,a,n,s,u,l,p)=>{let h,f,g,y;if(e==="VALID"&&(e=0),typeof e=="number"){h={top:e,bottom:e,left:e,right:e,front:e,back:e};let _=sa([t,r,i,1],[u,l,p],1,[a,n,s],e);f=_[0],g=_[1],y=_[2]}else if(Array.isArray(e)){if(!e.every((w,S,x)=>w===x[0]))throw Error(`Unsupported padding parameter: ${e}`);h={top:e[0],bottom:e[1],left:e[2],right:e[3],front:e[4],back:e[5]};let _=sa([t,r,i,1],[u,l,p],1,[a,n,s],e[0]);f=_[0],g=_[1],y=_[2]}else if(e==="SAME_UPPER"){f=Math.ceil(t/a),g=Math.ceil(r/n),y=Math.ceil(i/s);let _=(f-1)*a+u-t,w=(g-1)*n+l-r,S=(y-1)*s+p-i,x=Math.floor(_/2),b=_-x,I=Math.floor(w/2),k=w-I,E=Math.floor(S/2),A=S-E;h={top:I,bottom:k,left:E,right:A,front:x,back:b}}else throw Error(`Unknown padding parameter: ${e}`);return{padInfo:h,outDepth:f,outHeight:g,outWidth:y}},Ju=(e,t,r,i,a,n=!1,s="channelsLast")=>{let u,l,p,h,f;if(s==="channelsLast")[u,l,p,h,f]=e;else if(s==="channelsFirst")[u,f,l,p,h]=e;else throw new Error(`Unknown dataFormat ${s}`);let[g,,y,_,w]=t,[S,x,b]=na(r),[I,k,E]=na(i),A=ir(y,I),C=ir(_,k),$=ir(w,E),{padInfo:N,outDepth:D,outHeight:G,outWidth:V}=Xu(a,l,p,h,S,x,b,A,C,$),j=n?g*f:g,R=[0,0,0,0,0];return s==="channelsFirst"?R=[u,j,D,G,V]:s==="channelsLast"&&(R=[u,D,G,V,j]),{batchSize:u,dataFormat:s,inDepth:l,inHeight:p,inWidth:h,inChannels:f,outDepth:D,outHeight:G,outWidth:V,outChannels:j,padInfo:N,strideDepth:S,strideHeight:x,strideWidth:b,filterDepth:y,filterHeight:_,filterWidth:w,effectiveFilterDepth:A,effectiveFilterHeight:C,effectiveFilterWidth:$,dilationDepth:I,dilationHeight:k,dilationWidth:E,inShape:e,outShape:R,filterShape:t}},el=(e,t,r,i,a,n)=>{let s=n==="channelsLast";s?e[0].dims[3]:e[0].dims[1];let u=[64,1,1],l={x:r.map((S,x)=>x)},p=[Math.ceil(Zu(l.x.map(S=>r[S]))/u[0]),1,1];de("verbose",()=>`[conv3d_naive_webgpu] dispatch = ${p}`);let h=1,f=O.size(r),g=[{type:12,data:f},{type:12,data:i},{type:12,data:a},{type:12,data:t.strides},{type:12,data:t.dilations}];Et(t,g),g.push(...Y(e[0].dims,e[1].dims));let y=["rank","rank"],_=e.length===3;_&&(g.push(...Y(e[2].dims)),y.push("rank")),g.push(...Y(r));let w=S=>{let x=[{name:"output_size",type:"u32"},{name:"filter_dims",type:"u32",length:i.length},{name:"pads",type:"u32",length:a.length},{name:"strides",type:"u32",length:t.strides.length},{name:"dilations",type:"u32",length:t.dilations.length}];zt(t,x);let b=1,I=Te(e[0].dataType),k=M("x",e[0].dataType,e[0].dims.length,h),E=M("W",e[1].dataType,e[1].dims.length,b),A=[k,E],C=Q("result",e[0].dataType,r.length,b),$="";if(_){let G=M("bias",e[2].dataType,e[2].dims.length,b);A.push(G),$+=`
        fn getBiasByOutputCoords(coords : array<u32, 5>) -> ${I} {
          return bias[${s?Z("coords",4,5):Z("coords",1,5)}];
        }`}let N=Ie(h,I),D=It(t,N,I);return`
            ${$}
            fn getX(d0 : u32, d1 : u32, d2 : u32, d3 : u32, d4 : u32) -> f32 {
              let aIndices = array<u32, 5>(d0, d1, d2, d3, d4);
              return ${k.getByIndices("aIndices")};
            }
            fn getW(d0 : u32, d1 : u32, d2 : u32, d3 : u32, d4 : u32) -> f32 {
              let aIndices = array<u32, 5>(d0, d1, d2, d3, d4);
              return ${E.getByIndices("aIndices")};
            }
          ${S.registerUniforms(x).declareVariables(...A,C)}
          ${S.mainStart()}
          ${S.guardAgainstOutOfBoundsWorkgroupSizes("uniforms.output_size")}
              let coords = ${C.offsetToIndices("global_idx")};
              let batch = ${Z("coords",0,k.rank)};
              let d2 = ${s?Z("coords",k.rank-1,k.rank):Z("coords",1,k.rank)};
              let xFRCCorner = vec3<u32>(${s?Z("coords",1,k.rank):Z("coords",2,k.rank)},
              ${s?Z("coords",2,k.rank):Z("coords",3,k.rank)},
              ${s?Z("coords",3,k.rank):Z("coords",4,k.rank)}) * uniforms.strides - uniforms.pads;
              let xFCorner = xFRCCorner.x;
              let xRCorner = xFRCCorner.y;
              let xCCorner = xFRCCorner.z;
              let xShapeY = ${s?Z("uniforms.x_shape",1,k.rank):Z("uniforms.x_shape",2,k.rank)};
              let xShapeZ = ${s?Z("uniforms.x_shape",2,k.rank):Z("uniforms.x_shape",3,k.rank)};
              let xShapeW = ${s?Z("uniforms.x_shape",3,k.rank):Z("uniforms.x_shape",4,k.rank)};
              let xShapeU = ${s?Z("uniforms.x_shape",4,k.rank):Z("uniforms.x_shape",1,k.rank)};
              let inputDepthNearestVec4 = (xShapeU / 4) * 4;
              let inputDepthVec4Remainder = xShapeU % 4;

              var value = 0.0;
              for (var wF = 0u; wF < uniforms.filter_dims[0]; wF++) {
                let xF = xFCorner + wF * uniforms.dilations[0];
                if (xF < 0 || xF >= xShapeY) {
                  continue;
                }

                for (var wR = 0u; wR < uniforms.filter_dims[1]; wR++) {
                  let xR = xRCorner + wR * uniforms.dilations[1];
                  if (xR < 0 || xR >= xShapeZ) {
                    continue;
                  }

                  for (var wC = 0u; wC < uniforms.filter_dims[2]; wC++) {
                    let xC = xCCorner + wC * uniforms.dilations[2];
                    if (xC < 0 || xC >= xShapeW) {
                      continue;
                    }

                    for (var d1 = 0u; d1 < inputDepthNearestVec4; d1 += 4) {
                      ${s?`let xValues = vec4<f32>(
                               getX(batch, xF, xR, xC, d1),
                               getX(batch, xF, xR, xC, d1 + 1),
                               getX(batch, xF, xR, xC, d1 + 2),
                               getX(batch, xF, xR, xC, d1 + 3));
                            `:`let xValues = vec4<f32>(
                               getX(batch, d1, xF, xR, xC),
                               getX(batch, d1 + 1, xF, xR, xC),
                               getX(batch, d1 + 2, xF, xR, xC),
                               getX(batch, d1 + 3, xF, xR, xC));
                            `}
                            let wValues = vec4<f32>(
                              getW(d2, d1, wF, wR, wC),
                              getW(d2, d1 + 1, wF, wR, wC),
                              getW(d2, d1 + 2, wF, wR, wC),
                              getW(d2, d1 + 3, wF, wR, wC));
                      value += dot(xValues, wValues);
                    }
                    if (inputDepthVec4Remainder == 1) {
                        ${s?`value += getX(batch, xF, xR, xC, inputDepthNearestVec4)
                          * getW(d2, inputDepthNearestVec4, wF, wR, wC);`:`value += getX(batch, inputDepthNearestVec4, xF, xR, xC)
                          * getW(d2, inputDepthNearestVec4, wF, wR, wC);`}
                    } else if (inputDepthVec4Remainder == 2) {
                      ${s?`let xValues = vec2<f32>(
                        getX(batch, xF, xR, xC, inputDepthNearestVec4),
                        getX(batch, xF, xR, xC, inputDepthNearestVec4 + 1));
                      `:`let xValues = vec2<f32>(
                        getX(batch, inputDepthNearestVec4, xF, xR, xC),
                        getX(batch, inputDepthNearestVec4 + 1, xF, xR, xC));
                    `}
                    let wValues = vec2<f32>(
                      getW(d2, inputDepthNearestVec4, wF, wR, wC),
                      getW(d2, inputDepthNearestVec4 + 1, wF, wR, wC));
                      value += dot(xValues, wValues);
                    } else if (inputDepthVec4Remainder == 3) {
                      ${s?`let xValues = vec3<f32>(
                        getX(batch, xF, xR, xC, inputDepthNearestVec4),
                        getX(batch, xF, xR, xC, inputDepthNearestVec4 + 1),
                        getX(batch, xF, xR, xC, inputDepthNearestVec4 + 2));
                      `:`let xValues = vec3<f32>(
                        getX(batch, inputDepthNearestVec4, xF, xR, xC),
                        getX(batch, inputDepthNearestVec4 + 1, xF, xR, xC),
                        getX(batch, inputDepthNearestVec4 + 2, xF, xR, xC));
                    `}
                    let wValues = vec3<f32>(
                      getW(d2, inputDepthNearestVec4, wF, wR, wC),
                      getW(d2, inputDepthNearestVec4 + 1, wF, wR, wC),
                      getW(d2, inputDepthNearestVec4 + 2, wF, wR, wC));
                      value += dot(xValues, wValues);
                    }
                  }
                }
              }
              ${_?"value = value + getBiasByOutputCoords(coords)":""};
              ${D}
              result[global_idx] = f32(value);
          }`};return{name:"Conv3DNaive",shaderCache:{hint:`${t.cacheKey};${s};${h};${_}`,inputDependencies:y},getRunData:()=>({outputs:[{dims:r,dataType:e[0].dataType}],dispatchGroup:{x:p[0],y:p[1],z:p[2]},programUniforms:g}),getShaderSource:w}}}),tl,rl,fm=q(()=>{te(),re(),ae(),Ct(),tl=(e,t,r,i)=>{let a=e.length>2,n=a?"value += b[output_channel];":"",s=e[0].dims,u=e[1].dims,l=t.format==="NHWC",p=l?r[3]:r[1],h=p/t.group,f=l&&h>=4?ve(p):1,g=O.size(r)/f,y=[{type:12,data:g},{type:12,data:t.dilations},{type:12,data:[t.strides[0],t.strides[1]]},{type:12,data:[t.pads[0],t.pads[1]]},{type:12,data:h}];Et(t,y),y.push(...Y(s,[u[0],u[1],u[2],u[3]/f]));let _=a?["rank","rank","rank"]:["rank","rank"];y.push(...Y([r[0],r[1],r[2],r[3]/f]));let w=S=>{let x=Q("output",e[0].dataType,r.length,f),b=Te(x.type.tensor),I=It(t,x.type.value,b),k=M("x",e[0].dataType,s.length),E=M("w",e[1].dataType,u.length,f),A=[k,E];a&&A.push(M("b",e[2].dataType,e[2].dims,f));let C=[{name:"output_size",type:"u32"},{name:"dilations",type:"u32",length:t.dilations.length},{name:"strides",type:"u32",length:2},{name:"pads",type:"u32",length:2},{name:"output_channels_per_group",type:"u32"}];zt(t,C);let $=l?`
      for (var wHeight: u32 = 0u; wHeight < uniforms.w_shape[0]; wHeight++) {
        let xHeight = xRCCorner.x + wHeight * uniforms.dilations[0];

        if (xHeight < 0u || xHeight >= uniforms.x_shape[1]) {
          continue;
        }

        for (var wWidth: u32 = 0u; wWidth < uniforms.w_shape[1]; wWidth++) {
          let xWidth = xRCCorner.y + wWidth * uniforms.dilations[1];
          if (xWidth < 0u || xWidth >= uniforms.x_shape[2]) {
            continue;
          }

          for (var wInChannel: u32 = 0u; wInChannel < uniforms.w_shape[2]; wInChannel++) {
            let input_channel = in_channel_offset + wInChannel;
            let xVal = ${k.get("batch","xHeight","xWidth","input_channel")};
            let wVal = ${E.get("wHeight","wWidth","wInChannel","output_channel")};
            value += xVal * wVal;
          }
        }
      }
      `:`
      for (var wInChannel: u32 = 0u; wInChannel < uniforms.w_shape[1]; wInChannel++) {
        let input_channel = in_channel_offset + wInChannel;
        for (var wHeight: u32 = 0u; wHeight < uniforms.w_shape[2]; wHeight++) {
          let xHeight = xRCCorner.x + wHeight * uniforms.dilations[0];

          if (xHeight < 0u || xHeight >= uniforms.x_shape[2]) {
            continue;
          }

          for (var wWidth: u32 = 0u; wWidth < uniforms.w_shape[3]; wWidth++) {
            let xWidth = xRCCorner.y + wWidth * uniforms.dilations[1];
            if (xWidth < 0u || xWidth >= uniforms.x_shape[3]) {
              continue;
            }

            let xVal = ${k.get("batch","input_channel","xHeight","xWidth")};
            let wVal = ${E.get("output_channel","wInChannel","wHeight","wWidth")};
            value += xVal * wVal;
          }
        }
      }
      `;return`
  ${S.registerUniforms(C).declareVariables(...A,x)}

  ${S.mainStart()}
    ${S.guardAgainstOutOfBoundsWorkgroupSizes("uniforms.output_size")}

    let outputIndices = ${x.offsetToIndices("global_idx")};
    let batch: u32 = outputIndices[0];
    let output_channel: u32 = outputIndices[${l?3:1}];
    let xRCCorner: vec2<u32> = vec2<u32>(outputIndices[${l?1:2}], outputIndices[${l?2:3}]) * uniforms.strides - uniforms.pads;
    let group_id: u32 = output_channel * ${f} / uniforms.output_channels_per_group;
    var in_channel_offset = group_id * uniforms.w_shape[${l?2:1}];

    var value: ${x.type.value} = ${x.type.value}(0);
    ${$}
    ${n}
    ${I}
    ${x.setByOffset("global_idx","value")}
  }`};return{name:"GroupedConv",shaderCache:{hint:`${t.cacheKey}_${f}`,inputDependencies:_},getRunData:()=>({outputs:[{dims:i?i(r):r,dataType:e[0].dataType}],dispatchGroup:{x:Math.ceil(g/64)},programUniforms:y}),getShaderSource:w}},rl=(e,t,r,i)=>{let a=e.length>2,n=ve(r[3]),s=ve(r[2]),u=O.size(r)/n/s,l=[e[0].dims[0],e[0].dims[1],e[0].dims[2],e[0].dims[3]/n],p=[e[1].dims[0],e[1].dims[1],e[1].dims[2],e[1].dims[3]/n],h=[r[0],r[1],r[2],r[3]/n],f=[{type:12,data:u},{type:6,data:[t.strides[0],t.strides[1]]},{type:6,data:[t.pads[0],t.pads[1]]}];Et(t,f),f.push(...Y(l,p,h));let g=(s-1)*t.strides[1]+p[1],y=_=>{let w=Q("output",e[0].dataType,h.length,n),S=Te(w.type.tensor),x=It(t,w.type.value,S),b=M("x",e[0].dataType,l.length,n),I=M("w",e[1].dataType,p.length,n),k=[b,I];a&&k.push(M("b",e[2].dataType,e[2].dims,n));let E=a?"value += b[output_channel];":"",A=[{name:"output_size",type:"u32"},{name:"strides",type:"i32",length:2},{name:"pads",type:"i32",length:2}];return zt(t,A),`
  ${_.registerUniforms(A).declareVariables(...k,w)}
  ${_.mainStart()}
    ${_.guardAgainstOutOfBoundsWorkgroupSizes("uniforms.output_size")}
    let width0 = uniforms.output_shape[3];
    let output_channel = global_idx % width0;
    var index1 = global_idx / width0;
    let width1 = uniforms.output_shape[2] / ${s}u;
    let col = (index1 % width1) * ${s}u;
    index1 = index1 / width1;
    let row = index1 % uniforms.output_shape[1];
    let batch = index1 / uniforms.output_shape[1];

    let x_corner = vec2<i32>(i32(row), i32(col)) * uniforms.strides - uniforms.pads;

    var x_vals: array<${b.type.value}, ${g}>;
    var values: array<${w.type.value}, ${s}>;
    let input_channel = output_channel;
    // Use constant instead of uniform can give better performance for w's height/width.
    for (var w_height: u32 = 0u; w_height < ${p[0]}; w_height++) {
      let x_height = x_corner.x + i32(w_height);
      if (x_height >= 0 && u32(x_height) < uniforms.x_shape[1]) {
        for (var i = 0; i < ${g}; i++) {
          let x_width = x_corner.y + i;
          if (x_width >= 0 && u32(x_width) < uniforms.x_shape[2]) {
            x_vals[i] = ${b.get("batch","u32(x_height)","u32(x_width)","input_channel")};
          } else {
            x_vals[i] = ${b.type.value}(0);
          }
        }
        for (var w_width: u32 = 0u; w_width < ${p[1]}; w_width++) {
          let w_val = ${I.get("w_height","w_width","0","output_channel")};
          for (var i = 0u; i < ${s}u; i++) {
            values[i] = fma(x_vals[i * u32(uniforms.strides[1]) + w_width], w_val, values[i]);
          }
        }
      }
    }

    for (var i = 0u; i < ${s}u; i++) {
      var value = values[i];
      ${E}
      ${x}
      ${w.set("batch","row","col + i","output_channel","value")};
    }
  }`};return{name:"GroupedConv-Vectorize",shaderCache:{hint:`${t.cacheKey};${n};${s};${g};${p[0]};${p[1]}`,inputDependencies:a?["rank","rank","type"]:["rank","rank"]},getRunData:()=>({outputs:[{dims:i?i(r):r,dataType:e[0].dataType}],dispatchGroup:{x:Math.ceil(u/64)},programUniforms:f}),getShaderSource:y}}}),il,Br,al,Mr,oa,ua,nl,sl,la,mm=q(()=>{re(),cm(),hm(),aa(),fm(),Ct(),ea(),dt(),il=(e,t,r,i,a,n)=>{let s=e[0],u=e.slice(n?1:2,n?3:4),l=u.length,p=t[0],h=t.slice(2).map((g,y)=>g+(g-1)*(r[y]-1)),f=u.map((g,y)=>g+i[y]+i[y+l]).map((g,y)=>Math.floor((g-h[y]+a[y])/a[y]));return f.splice(0,0,s),f.splice(n?3:1,0,p),f},Br=[2,3,1,0],al=(e,t)=>{if(!e||e.length!==2&&e.length!==3)throw new Error("Conv requires 2 or 3 inputs");if(e[0].dims.length>5)throw new Error("greater than 5D is not supported");if(e[0].dims.length!==e[1].dims.length)throw new Error("filter does not have same dimension as input");let r=e[0].dims[t.format==="NHWC"?e[0].dims.length-1:1],i=e[1].dims[1]*t.group;if(r!==i)throw new Error("FILTER_IN_CHANNEL should be equal to DATA_CHANNEL");if(e.length===3&&(e[2].dims.length!==1||e[1].dims[0]!==e[2].dims[0]))throw new Error("invalid bias");let a=e[0].dims.length-2;if(t.dilations.length!==a)throw new Error(`dilations should be ${a}D`);if(t.strides.length!==a)throw new Error(`strides should be ${a}D`);if(t.pads.length!==a*2)throw new Error(`pads should be ${a*2}D`);if(t.kernelShape.length!==0&&t.kernelShape.length!==e[1].dims.length-2)throw new Error("invalid kernel shape")},Mr=(e,t)=>{let r=e.kernelShape.slice();r.length<t[1].dims.length-2&&r.push(...Array(t[1].dims.length-2-r.length).fill(0));for(let n=2;n<t[1].dims.length;++n)r[n-2]===0&&(r[n-2]=t[1].dims[n]);let i=e.pads.slice();kr.adjustPadsBasedOnAutoPad(t[0].dims,e.strides,e.dilations,r,i,e.format==="NHWC",e.autoPad);let a=Object.assign({},e);return Object.assign(a,{kernelShape:r,pads:i}),a},oa=e=>{let t=Yi(e),r=e.format,i=["NOTSET","VALID","SAME_UPPER","SAME_LOWER"][e.auto_pad],a=e.dilations,n=e.group,s=e.kernel_shape,u=e.pads,l=e.strides,p=e.w_is_const();return{autoPad:i,format:r,dilations:a,group:n,kernelShape:s,pads:u,strides:l,wIsConst:p,...t,cacheKey:`${e.format};${t.activation};`}},ua=(e,t,r,i)=>{let a=r.format==="NHWC",n=il(t[0].dims,t[1].dims,r.dilations,r.pads,r.strides,a);if(r.group!==1){let A=[t[0]];if(a){let C=e.kernelCustomData.wT??e.compute(Ne(t[1],Br),{inputs:[1],outputs:[r.wIsConst?-2:-1]})[0];r.wIsConst&&!e.kernelCustomData.wT&&(e.kernelCustomData.wT=C),A.push(C)}else A.push(t[1]);t.length===3&&A.push(t[2]),!e.adapterInfo.isArchitecture("ampere")&&a&&t[1].dims[0]===r.group&&t[1].dims[1]===1&&r.dilations[0]===1&&r.dilations[1]===1?e.compute(rl(A,r,n,i),{inputs:A}):e.compute(tl(A,r,n,i),{inputs:A});return}let s=t.length===3,u=t[0].dims[a?1:2],l=t[0].dims[a?2:3],p=t[0].dims[a?3:1],h=t[1].dims[2],f=t[1].dims[3],g=n[a?1:2],y=n[a?2:3],_=n[a?3:1],w=a&&h===u&&f===l&&r.pads[0]===0&&r.pads[1]===0;if(w||h===1&&f===1&&r.dilations[0]===1&&r.dilations[1]===1&&r.strides[0]===1&&r.strides[1]===1&&r.pads[0]===0&&r.pads[1]===0){let A=n[0],C,$,N,D=[];if(a){let j=e.kernelCustomData.wT??e.compute(Ne(t[1],Br),{inputs:[1],outputs:[r.wIsConst?-2:-1]})[0];if(r.wIsConst&&!e.kernelCustomData.wT&&(e.kernelCustomData.wT=j),w){let R=u*l*p;C=t[0].reshape([1,A,R]),$=j.reshape([1,R,_]),N=[1,A,_]}else C=t[0].reshape([A,u*l,p]),$=j.reshape([1,p,_]),N=[A,g*y,_];D.push(C),D.push($)}else C=t[0].reshape([A,p,u*l]),$=t[1].reshape([1,_,p]),N=[A,_,g*y],D.push($),D.push(C);s&&D.push(t[2]);let G=N[2],V=D[0].dims[D[0].dims.length-1];G<8&&V<8?e.compute(Ji(D,r,n,N,a,i),{inputs:D}):e.compute(Rr(D,r,n,N,a,i),{inputs:D});return}let S=!0,x=e.kernelCustomData.wT??e.compute(Ne(t[1],Br),{inputs:[1],outputs:[r.wIsConst?-2:-1]})[0];r.wIsConst&&!e.kernelCustomData.wT&&(e.kernelCustomData.wT=x);let b=[t[0],x];s&&b.push(t[2]);let I=a?g*y:_,k=a?_:g*y,E=h*f*p;e.compute(Qu(b,r,n,I,k,E,s,S,i),{inputs:b})},nl=(e,t)=>{let r=t.format==="NHWC",i=[e.inputs[0].reshape(r?[e.inputs[0].dims[0],1,e.inputs[0].dims[1],e.inputs[0].dims[2]]:[e.inputs[0].dims[0],e.inputs[0].dims[1],1,e.inputs[0].dims[2]]),e.inputs[1].reshape([e.inputs[1].dims[0],e.inputs[1].dims[1],1,e.inputs[1].dims[2]])];e.inputs.length===3&&i.push(e.inputs[2]);let a=[0,t.pads[0],0,t.pads[1]],n=[1].concat(t.strides),s=[1].concat(t.dilations),u=[1].concat(t.kernelShape),l=Mr({...t,pads:a,strides:n,dilations:s,kernelShape:u},i);ua(e,i,l,p=>r?[p[0],p[2],p[3]]:[p[0],p[1],p[3]])},sl=(e,t,r)=>{let i=r.format==="NHWC"?"channelsLast":"channelsFirst",a=Mr(r,t),n=r.autoPad==="NOTSET"?r.pads:r.autoPad,s=Ju(t[0].dims,t[1].dims,r.strides,r.dilations,n,!1,i);e.compute(el(t,a,s.outShape,[s.filterDepth,s.filterHeight,s.filterWidth],[s.padInfo.front,s.padInfo.top,s.padInfo.left],i))},la=(e,t)=>{if(al(e.inputs,t),e.inputs[0].dims.length===3)nl(e,t);else if(e.inputs[0].dims.length===5)sl(e,e.inputs,t);else{let r=Mr(t,e.inputs);ua(e,e.inputs,r)}}}),ol,gm=q(()=>{te(),at(),re(),ae(),ol=(e,t,r)=>{let i=e.length>2,a=t.outputShape,n=t.format==="NHWC",s=t.group,u=e[1].dims,l=u[2]/s,p=u[3],h=n?ve(l):1,f=n&&p===1&&l>=4,g=f?Math.floor(l/4)*4:Math.floor(l/h)*h,y=l-g,_=n?ve(p):1,w=n?p===1?h:_:1,S=O.size(a)/_,x=[Math.ceil(S/64),1,1];de("verbose",()=>`[conv2d_backprop_webgpu] dispatch = ${x}`);let b=["rank","rank"],I=[t.strides[0],t.strides[1]],k=[t.kernelShape[n?1:2],t.kernelShape[n?2:3]],E=[t.dilations[0],t.dilations[1]],A=[k[0]+(t.dilations[0]<=1?0:(t.kernelShape[n?1:2]-1)*(t.dilations[0]-1)),k[1]+(t.dilations[1]<=1?0:(t.kernelShape[n?2:3]-1)*(t.dilations[1]-1))],C=[A[0]-1-Math.floor((t.pads[0]+t.pads[2])/2),A[1]-1-Math.floor((t.pads[1]+t.pads[3])/2)],$=[{type:12,data:S},{type:12,data:I},{type:12,data:k},{type:12,data:E},{type:12,data:A},{type:6,data:C},{type:12,data:g},{type:12,data:l},{type:12,data:p},...Y(e[0].dims,e[1].dims)];i&&($.push(...Y(e[2].dims)),b.push("rank")),$.push(...Y(a));let N=D=>{let G=[{name:"output_size",type:"u32"},{name:"strides",type:"u32",length:I.length},{name:"filter_dims",type:"u32",length:k.length},{name:"dilations",type:"u32",length:k.length},{name:"effective_filter_dims",type:"u32",length:A.length},{name:"pads",type:"i32",length:C.length},{name:"input_channels_per_group_int",type:"u32"},{name:"input_channels_per_group",type:"u32"},{name:"output_channels_per_group",type:"u32"}],V=Te(e[0].dataType),j=n?1:2,R=n?2:3,K=n?3:1,F=M("W",e[1].dataType,e[1].dims.length,w),X=M("Dy",e[0].dataType,e[0].dims.length,h),le=[X,F];i&&le.push(M("bias",e[2].dataType,[a[K]].length,_));let L=Q("result",e[0].dataType,a.length,_),me=()=>{let J="";if(f)h===4?J+=`
        let xValue = ${X.getByOffset("x_offset")};
        let wValue = ${F.getByOffset("w_offset")};
        dotProd = dotProd + dot(xValue, wValue);
        x_offset += 1u;
        w_offset += 1u;`:h===2?J+=`
          dotProd = dotProd + dot(vec4<${V}>(${X.getByOffset("x_offset")}, ${X.getByOffset("x_offset + 1u")}), vec4<${V}>(${F.getByOffset("w_offset")}, ${F.getByOffset("w_offset + 1u")}));
          x_offset += 2u;
          w_offset += 2u;`:h===1&&(J+=`
          dotProd = dotProd + dot(vec4<${V}>(${X.getByOffset("x_offset")}, ${X.getByOffset("x_offset + 1u")}, ${X.getByOffset("x_offset + 2u")}, ${X.getByOffset("x_offset + 3u")}), vec4<${V}>(${F.getByOffset("w_offset")}, ${F.getByOffset("w_offset + 1u")}, ${F.getByOffset("w_offset + 2u")}, ${F.getByOffset("w_offset + 3u")}));
          x_offset += 4u;
          w_offset += 4u;`);else if(J+=`
                  let xValue = ${n?X.getByOffset(`${X.indicesToOffset(`${X.type.indices}(batch, idyR, idyC, inputChannel)`)} / ${h}`):X.get("batch","inputChannel","idyR","idyC")};
        `,h===1)J+=`
          let w_offset = ${F.indicesToOffset(`${F.type.indices}(u32(wRPerm), u32(wCPerm), inputChannel, wOutChannel)`)};
          let wValue = ${F.getByOffset(`w_offset / ${w}`)};
          dotProd = dotProd + xValue * wValue;`;else for(let ee=0;ee<h;ee++)J+=`
            let wValue${ee} = ${F.getByOffset(`${F.indicesToOffset(`${F.type.indices}(u32(wRPerm), u32(wCPerm), inputChannel + ${ee}, wOutChannel)`)} / ${w}`)};
            dotProd = dotProd + xValue[${ee}] * wValue${ee};`;return J},U=()=>{if(y===0)return"";if(!f)throw new Error(`packInputAs4 ${f} is not true.`);let J="";if(h===1){J+="dotProd = dotProd";for(let ee=0;ee<y;ee++)J+=`
            + ${X.getByOffset(`x_offset + ${ee}`)} * ${F.getByOffset(`w_offset + ${ee}`)}`;J+=";"}else if(h===2){if(y!==2)throw new Error(`Invalid inputChannelsRemainder ${y}.`);J+=`
          let xValue = ${X.getByOffset("x_offset")};
          let wValue = ${F.getByOffset("w_offset")};
          dotProd = dotProd + dot(xValue, wValue);`}return J},P=`
            let outputIndices = ${L.offsetToIndices(`global_idx * ${_}`)};
            let batch = ${L.indicesGet("outputIndices",0)};
            let d1 = ${L.indicesGet("outputIndices",K)};
            let r = ${L.indicesGet("outputIndices",j)};
            let c = ${L.indicesGet("outputIndices",R)};
            let dyCorner = vec2<i32>(i32(r), i32(c)) - uniforms.pads;
            let dyRCorner = dyCorner.x;
            let dyCCorner = dyCorner.y;
            let groupId = d1 / uniforms.output_channels_per_group;
            let wOutChannel = d1 - groupId * uniforms.output_channels_per_group;
            // Convolve dy(?, ?, d2) with w(:, :, d1, d2) to compute dx(xR, xC, d1).
            // ? = to be determined. : = across all values in that axis.
            var dotProd = ${L.type.value}(0.0);
            var wR: u32 = 0;
            if (uniforms.dilations.x == 1) {
              // Minimum wR >= 0 that satisfies (dyRCorner + wR) % (uniforms.strides.x) == 0
              wR = u32(((dyRCorner + i32(uniforms.strides.x) - 1) / i32(uniforms.strides.x)) * i32(uniforms.strides.x) - dyRCorner);
            }
            for (; wR < uniforms.effective_filter_dims.x; wR = wR + 1) {
              if (wR % uniforms.dilations.x != 0) {
                continue;
              }
              let dyR = (${V}(dyRCorner) + ${V}(wR)) / ${V}(uniforms.strides[0]);
              let wRPerm = uniforms.filter_dims.x - 1 - wR / uniforms.dilations.x;
              if (dyR < 0.0 || dyR >= ${V}(uniforms.Dy_shape[${j}]) || fract(dyR) > 0.0 ||
                  wRPerm < 0) {
                continue;
              }
              let idyR: u32 = u32(dyR);
              var wC: u32 = 0;
              if (uniforms.dilations.y == 1) {
                // Minimum wC >= 0 that satisfies (dyCCorner + wC) % (uniforms.strides.y) == 0
                wC = u32(((dyCCorner + i32(uniforms.strides.y) - 1) / i32(uniforms.strides.y)) * i32(uniforms.strides.y) - dyCCorner);
              }
              for (; wC < uniforms.effective_filter_dims.y; wC = wC + 1) {
                if (wC % uniforms.dilations.y != 0) {
                  continue;
                }
                let dyC = (${V}(dyCCorner) + ${V}(wC)) / ${V}(uniforms.strides.y);
                let wCPerm = uniforms.filter_dims.y - 1 - wC / uniforms.dilations.y;
                if (dyC < 0.0 || dyC >= ${V}(uniforms.Dy_shape[${R}]) ||
                    fract(dyC) > 0.0 || wCPerm < 0) {
                  continue;
                }
                let idyC: u32 = u32(dyC);
                var inputChannel = groupId * uniforms.input_channels_per_group;
                ${f?`
                var x_offset = ${X.indicesToOffset(`${X.type.indices}(batch, idyR, idyC, inputChannel)`)} / ${h};
                var w_offset = ${F.indicesToOffset(`${F.type.indices}(wRPerm, wCPerm, inputChannel, wOutChannel)`)} / ${w};
                  `:""}
                for (var d2: u32 = 0; d2 < uniforms.input_channels_per_group_int; d2 = d2 + ${f?4:h}) {
                  ${me()}
                  inputChannel = inputChannel + ${f?4:h};
                }
                ${U()}
                wC = wC + uniforms.strides.y - 1;
              }
              wR = wR + uniforms.strides[0] - 1;
            }
            let value = dotProd${i?` + bias[d1 / ${_}]`:""};
            ${L.setByOffset("global_idx","value")};
          `;return`
    ${D.registerUniforms(G).declareVariables(...le,L)}
      ${D.mainStart()}
      ${D.guardAgainstOutOfBoundsWorkgroupSizes("uniforms.output_size")};
    ${P}}`};return{name:"ConvTranspose2D",shaderCache:{hint:`${t.cacheKey};${h}${w}${_}${f}${y}`,inputDependencies:b},getRunData:()=>({dispatchGroup:{x:x[0],y:x[1],z:x[2]},outputs:[{dims:r?r(a):a,dataType:e[0].dataType}],programUniforms:$}),getShaderSource:N}}}),ul,ll,dl,da,pl,cl,pa,hl,fl,ym=q(()=>{gm(),Ct(),dt(),ul=(e,t,r,i,a,n)=>(e-1)*t+r+(i-1)*a+1-n,ll=(e,t,r,i,a)=>{let n=Math.floor(e/2);t==="SAME_UPPER"?(r[i]=n,r[a]=e-n):t==="SAME_LOWER"&&(r[i]=e-n,r[a]=n)},dl=(e,t,r,i,a,n,s,u,l,p)=>{let h=e.length-2,f=p.length===0;l.length<h&&l.push(...Array(h-l.length).fill(0));let g=e[0],y=t[u?3:1]*a;for(let _=0,w=e.length-h-(u?1:0);_<h;++_,++w){let S=e[w],x=f?S*s[_]:p[_],b=ul(S,s[_],n[_],t[w],r[_],x);ll(b,i,n,_,_+h),f&&p.push(s[_]*(S-1)+l[_]+(t[w]-1)*r[_]+1-n[_]-n[_+h])}p.splice(0,0,g),p.splice(u?3:1,0,y)},da=(e,t)=>{let r=e.kernelShape.slice();if(e.kernelShape.length===0||e.kernelShape.reduce((f,g)=>f*g,1)===0){r.length=0;for(let f=2;f<t[1].dims.length;++f)r.push(t[1].dims[f])}let i=e.format==="NHWC";r.splice(0,0,t[1].dims[0]),r.splice(i?3:1,0,t[1].dims[1]);let a=e.pads.slice(),n=e.outputShape.slice(),s=e.outputPadding.slice(),u=t[0].dims,l=e.dilations.slice();if(l.reduce((f,g)=>f+g,0)===0){let f=t[0].dims.length-2;l=new Array(f).fill(1)}let p=e.strides.slice();if(p.reduce((f,g)=>f+g,0)===0){let f=t[0].dims.length-2;p=new Array(f).fill(1)}dl(u,r,l,e.autoPad,e.group,a,p,i,s,n);let h=Object.assign({},e);return Object.assign(h,{kernelShape:r,pads:a,outputPadding:s,outputShape:n,dilations:l,strides:p}),h},pl=e=>{let t=Yi(e),r=e.format,i=["NOTSET","VALID","SAME_UPPER","SAME_LOWER"][typeof e.autoPad>"u"?0:e.autoPad],a=e.dilations,n=e.group??1,s=e.kernelShape,u=e.pads,l=e.strides,p=e.wIsConst(),h=e.outputPadding,f=e.outputShape;return{autoPad:i,format:r,dilations:a,group:n,kernelShape:s,outputPadding:h,outputShape:f,pads:u,strides:l,wIsConst:p,...t,cacheKey:`${e.format};${t.activation};`}},cl=(e,t)=>{if(!e||e.length!==2&&e.length!==3)throw new Error("Conv requires 2 or 3 inputs");if(e[0].dims.length!==4&&e[0].dims.length!==3)throw new Error("currently only support 2-dimensional conv");if(e[0].dims.length!==e[1].dims.length)throw new Error("filter does not have same dimension as input");let r=e[0].dims[t.format==="NHWC"?e[0].dims.length-1:1],i=e[1].dims[0];if(r!==i)throw new Error("FILTER_IN_CHANNEL should be equal to DATA_CHANNEL");let a=e[1].dims[1]*t.group;if(e.length===3&&(e[2].dims.length!==1||e[2].dims[0]!==a))throw new Error("invalid bias");let n=e[0].dims.length-2;if(t.dilations.reduce((s,u)=>s+u,0)>0&&t.dilations.length!==n)throw new Error(`dilations should be ${n}D`);if(t.strides.reduce((s,u)=>s+u,0)>0&&t.strides.length!==n)throw new Error(`strides should be ${n}D`);if(t.pads.reduce((s,u)=>s+u,0)>0&&t.pads.length!==n*2)throw new Error(`pads should be ${n*2}D`);if(t.outputPadding.length!==n&&t.outputPadding.length!==0)throw new Error(`output_padding should be ${n}D`);if(t.kernelShape.reduce((s,u)=>s+u,0)>0&&t.kernelShape.length!==0&&t.kernelShape.length!==e[1].dims.length-2)throw new Error("invalid kernel shape");if(t.outputShape.length!==0&&t.outputShape.length!==e[0].dims.length-2)throw new Error("invalid output shape")},pa=(e,t,r,i)=>{let a=e.kernelCustomData.wT??e.compute(Ne(t[1],[2,3,0,1]),{inputs:[1],outputs:[r.wIsConst?-2:-1]})[0];r.wIsConst&&!e.kernelCustomData.wT&&(e.kernelCustomData.wT=a);let n=[t[0],a];t.length===3&&n.push(t[2]),e.compute(ol(n,r,i),{inputs:n})},hl=(e,t)=>{let r=t.format==="NHWC",i=[e.inputs[0].reshape(r?[e.inputs[0].dims[0],1,e.inputs[0].dims[1],e.inputs[0].dims[2]]:[e.inputs[0].dims[0],e.inputs[0].dims[1],1,e.inputs[0].dims[2]]),e.inputs[1].reshape([e.inputs[1].dims[0],e.inputs[1].dims[1],1,e.inputs[1].dims[2]])];e.inputs.length===3&&i.push(e.inputs[2]);let a=t.kernelShape;(a.length===0||a[0]===0)&&(a=[e.inputs[1].dims[2]]);let n=t.dilations;(n.length===0||n[0]===0)&&(n=[1]);let s=t.strides;(s.length===0||s[0]===0)&&(s=[1]);let u=t.pads;u.length===0&&(u=[0,0]),u=[0,u[0],0,u[1]],s=[1].concat(s),n=[1].concat(n),a=[1].concat(a);let l=t.outputPadding;l=[0].concat(l);let p=da({...t,pads:u,strides:s,dilations:n,kernelShape:a,outputPadding:l},i);pa(e,i,p,h=>r?[h[0],h[2],h[3]]:[h[0],h[1],h[3]])},fl=(e,t)=>{if(cl(e.inputs,t),e.inputs[0].dims.length===3)hl(e,t);else{let r=da(t,e.inputs);pa(e,e.inputs,r)}}}),ml,gl,yl,_m=q(()=>{te(),re(),xe(),ae(),ml=(e,t,r,i)=>{let a=O.size(t),n=t.length,s=M("input",e,n),u=Q("output",e,n),l=r.dataType===6?r.getInt32Array()[0]:Number(r.getBigInt64Array()[0]),p=O.normalizeAxis(l,n),h=f=>{let g=` i32(${s.indicesGet("inputIndices","uniforms.axis")}) `,y=Z("uniforms.input_shape","uniforms.axis",n),_=i.reverse?g+(i.exclusive?" + 1":""):"0",w=i.reverse?y:g+(i.exclusive?"":" + 1");return`
                ${f.registerUniform("outputSize","u32").registerUniform("axis","u32").declareVariables(s,u)}
                ${f.mainStart()}
                  ${f.guardAgainstOutOfBoundsWorkgroupSizes("uniforms.outputSize")}
                  var inputIndices = ${u.offsetToIndices("global_idx")};
                  var sum = ${u.type.value}(0);
                  let first : i32 = ${_};
                  let last : i32 = ${w};
                  for (var i : i32 = first; i < last; i++) {
                    ${s.indicesSet("inputIndices","uniforms.axis","u32(i)")};
                    sum = sum + ${s.getByIndices("inputIndices")};
                  }
                  ${u.setByOffset("global_idx","sum")};
                }`};return{name:"CumSum",shaderCache:{hint:i.cacheKey,inputDependencies:["rank"]},getRunData:()=>({outputs:[{dims:t,dataType:e}],dispatchGroup:{x:Math.ceil(a/64)},programUniforms:[{type:12,data:a},{type:12,data:p},...Y(t,t)]}),getShaderSource:h}},gl=(e,t)=>{let r=e.inputs[0].dims,i=e.inputs[0].dataType,a=e.inputs[1];e.compute(ml(i,r,a,t),{inputs:[0]})},yl=e=>{let t=e.exclusive===1,r=e.reverse===1;return he({exclusive:t,reverse:r})}}),_l,wl,bl,$l,vl,wm=q(()=>{te(),re(),xe(),ae(),_l=e=>{if(!e||e.length!==1)throw new Error("DepthToSpace requires 1 input.");if(e[0].dims.length!==4)throw new Error("DepthToSpace requires 4D input.")},wl=(e,t,r,i)=>{let a=[];a.push(`fn perm(i: ${i.type.indices}) -> ${r.type.indices} {
    var a: ${r.type.indices};`);for(let n=0;n<t;++n)a.push(r.indicesSet("a",e[n],`i[${n}]`));return a.push("return a;}"),a.join(`
`)},bl=(e,t)=>{let r,i,a,n,s,u,l=t.format==="NHWC",p=t.blocksize,h=t.mode==="DCR";l?([r,i,a,n]=e.dims,s=h?[r,i,a,p,p,n/p**2]:[r,i,a,n/p**2,p,p],u=h?[0,1,3,2,4,5]:[0,1,4,2,5,3]):([r,i,a,n]=[e.dims[0],e.dims[2],e.dims[3],e.dims[1]],s=h?[r,p,p,n/p**2,i,a]:[r,n/p**2,p,p,i,a],u=h?[0,3,4,1,5,2]:[0,1,4,2,5,3]);let f=e.reshape(s),g=f.dims.length,y=e.dataType,_=M("a",y,g),w=Q("output",y,g),S=x=>`
  ${x.registerUniform("output_size","u32").declareVariables(_,w)}

  ${wl(u,g,_,w)}

  ${x.mainStart()}
    ${x.guardAgainstOutOfBoundsWorkgroupSizes("uniforms.output_size")}

    let indices = ${w.offsetToIndices("global_idx")};
    let aIndices = perm(indices);

    ${w.setByOffset("global_idx",_.getByIndices("aIndices"))}
  }`;return{name:"DepthToSpace",shaderCache:{hint:`${e.dims};${t.blocksize};${t.mode}`,inputDependencies:["rank"]},getRunData:x=>{let b=l?[r,i*p,a*p,n/p**2]:[r,n/p**2,i*p,a*p],I=O.size(b),k=f.dims,E=O.sortBasedOnPerm(k,u);return{outputs:[{dims:b,dataType:x[0].dataType}],dispatchGroup:{x:Math.ceil(I/64)},programUniforms:[{type:12,data:I},...Y(k,E)]}},getShaderSource:S}},$l=(e,t)=>{_l(e.inputs),e.compute(bl(e.inputs[0],t))},vl=e=>he({blocksize:e.blocksize,mode:e.mode,format:e.format})}),Nr,ar,ca,xl,Sl,Tl,kl,ha,Il,El,zl,bm=q(()=>{te(),re(),xe(),ae(),Nr="[a-zA-Z]|\\.\\.\\.",ar="("+Nr+")+",ca="^"+ar+"$",xl="("+ar+",)*"+ar,Sl="^"+xl+"$",Tl=class{constructor(e=-1){this.symbolToIndices=new Map,this.inputIndex=e}addSymbol(e,t){let r=this.symbolToIndices.get(e);r===void 0?r=[t]:r.push(t),this.symbolToIndices.set(e,r)}},kl=class{constructor(e,t){var a;this.equation=t,this.hasEllipsis=!1,this.symbolToInfo=new Map,this.lhs=new Array,this.outputDims=[];let[r,i]=t.includes("->")?t.split("->",2):[t,""];if(!r.match(RegExp(Sl)))throw new Error("Invalid LHS term");if(r.split(",").forEach((n,s)=>{let u=e[s].dims.slice();if(!n.match(RegExp(ca)))throw new Error("Invalid LHS term");let l=this.processTerm(n,!0,u,s);this.lhs.push(l)}),i==="")i+=[...this.symbolToInfo.entries()].filter(([n,s])=>s.count===1||n==="...").map(([n])=>n).join("");else if(!i.match(RegExp(ar)))throw new Error("Invalid RHS");(a=i.match(RegExp(Nr,"g")))==null||a.forEach(n=>{if(n==="...")this.outputDims=this.outputDims.concat(this.ellipsisDims);else{let s=this.symbolToInfo.get(n);if(s===void 0)throw new Error("Invalid RHS symbol");this.outputDims.push(s.dimValue)}}),this.rhs=this.processTerm(i,!1,this.outputDims)}addSymbol(e,t,r){let i=this.symbolToInfo.get(e);if(i!==void 0){if(i.dimValue!==t&&i.count!==1)throw new Error("Dimension mismatch");i.count++,i.inputIndices.push(r)}else i={count:1,dimValue:t,inputIndices:[r]};this.symbolToInfo.set(e,i)}processTerm(e,t,r,i=-1){let a=r.length,n=!1,s=[],u=0;if(!e.match(RegExp(ca))&&!t&&e!=="")throw new Error("Invalid LHS term");let l=e.match(RegExp(Nr,"g")),p=new Tl(i);return l==null||l.forEach((h,f)=>{if(h==="..."){if(n)throw new Error("Only one ellipsis is allowed per input term");n=!0;let g=a-l.length+1;if(g<0)throw new Error("Ellipsis out of bounds");if(s=r.slice(u,u+g),this.hasEllipsis){if(this.ellipsisDims.length!==s.length||this.ellipsisDims.toString()!==s.toString())throw new Error("Ellipsis dimensions mismatch")}else if(t)this.hasEllipsis=!0,this.ellipsisDims=s;else throw new Error("Ellipsis must be specified in the LHS");for(let y=0;y<s.length;y++){let _=String.fromCharCode(48+y);p.addSymbol(_,f+y),this.addSymbol(_,r[u++],i)}}else p.addSymbol(h,f+(this.hasEllipsis?this.ellipsisDims.length-1:0)),this.addSymbol(h,r[u++],i)}),p}},ha=e=>e+"_max",Il=(e,t,r,i)=>{let a=e.map(p=>p.length).map((p,h)=>M(`input${h}`,t,p)),n=O.size(i),s=Q("output",t,i.length),u=[...r.symbolToInfo.keys()].filter(p=>!r.rhs.symbolToIndices.has(p)),l=p=>{let h=[],f="var prod = 1.0;",g="var sum = 0.0;",y="sum += prod;",_=[],w=[],S=[],x=[],b=r.symbolToInfo.size===r.rhs.symbolToIndices.size;r.symbolToInfo.forEach((k,E)=>{var A;if(r.rhs.symbolToIndices.has(E)){let C=(A=r.rhs.symbolToIndices.get(E))==null?void 0:A[0];C!==void 0&&r.lhs.forEach(($,N)=>{if(k.inputIndices.includes(N)){let D=$.symbolToIndices.get(E);if(D===void 0)throw new Error("Invalid symbol error");D.forEach(G=>{h.push(`${a[N].indicesSet(`input${N}Indices`,G,s.indicesGet("outputIndices",C))}`)})}})}else r.lhs.forEach((C,$)=>{if(k.inputIndices.includes($)){let N=C.symbolToIndices.get(E);if(N===void 0)throw new Error("Invalid symbol error");N.forEach(D=>{_.push(`${a[$].indicesSet(`input${$}Indices`,D,`${E}`)}`)}),x.push(`prod *= ${a[$].getByIndices(`input${$}Indices`)};`)}}),w.push(`for(var ${E}: u32 = 0; ${E} < uniforms.${ha(E)}; ${E}++) {`),S.push("}")});let I=b?[...h,`let sum = ${a.map((k,E)=>k.getByIndices(`input${E}Indices`)).join(" * ")};`]:[...h,g,...w,..._,f,...x,y,...S];return`
            ${p.registerUniforms(u.map(k=>({name:`${ha(k)}`,type:"u32"}))).registerUniform("outputSize","u32").declareVariables(...a,s)}

            ${p.mainStart()}
            ${p.guardAgainstOutOfBoundsWorkgroupSizes("uniforms.outputSize")}
            var outputIndices = ${s.offsetToIndices("global_idx")};
            ${a.map((k,E)=>`var input${E}Indices: ${a[E].type.indices};`).join(`
`)}
            ${I.join(`
`)};
            ${s.setByOffset("global_idx","sum")};
          }`};return{name:"Einsum",shaderCache:{hint:r.equation,inputDependencies:e.map(()=>"rank")},getRunData:()=>{let p=u.filter(f=>r.symbolToInfo.has(f)).map(f=>{var g;return{type:12,data:((g=r.symbolToInfo.get(f))==null?void 0:g.dimValue)||0}});p.push({type:12,data:n});let h=e.map((f,g)=>[...Y(f)]).reduce((f,g)=>f.concat(g),p);return h.push(...Y(i)),{outputs:[{dims:i,dataType:t}],dispatchGroup:{x:Math.ceil(n/64)},programUniforms:h}},getShaderSource:l}},El=(e,t)=>{let r=new kl(e.inputs,t.equation),i=r.outputDims,a=e.inputs.map((n,s)=>n.dims);e.compute(Il(a,e.inputs[0].dataType,r,i))},zl=e=>{let t=e.equation.replace(/\s+/g,"");return he({equation:t})}}),Cl,fa,Al,Ol,Rl,$m=q(()=>{te(),re(),ae(),Cl=e=>{if(!e||e.length!==2)throw new Error("Expand requires 2 input.");let t=e[0].dims,r=Array.from(e[1].getBigInt64Array(),Number),i=r.length<t.length?0:r.length-t.length,a=t.length<r.length?0:t.length-r.length;for(;i<r.length&&a<t.length;++i,++a)if(r[i]!==t[a]&&r[i]!==1&&t[a]!==1)throw new Error("Expand requires shape to be broadcastable to input")},fa=(e,t)=>{let r=e.length-t.length,i=[];for(let a=0;a<r;++a)i.push(e[a]);for(let a=0;a<t.length;++a)i.push(t[a]===1?e[a+r]:t[a]);return i},Al=(e,t)=>e.length>t.length?fa(e,t):fa(t,e),Ol=e=>{let t=e[0].dims,r=Array.from(e[1].getBigInt64Array(),Number),i=Al(t,r),a=e[0].dataType,n=a===9||O.size(t)===1,s=a===9||t.length>0&&t[t.length-1]%4===0?4:1,u=n||i.length>0&&i[i.length-1]%4===0?4:1,l=Math.ceil(O.size(i)/u),p=f=>{let g=M("input",a,t.length,s),y=Q("output",a,i.length,u),_;if(a===9){let w=(S,x,b="")=>`
          let outputIndices${x} = ${y.offsetToIndices(`outputOffset + ${x}u`)};
          let offset${x} = ${g.broadcastedIndicesToOffset(`outputIndices${x}`,y)};
          let index${x} = offset${x} / 4u;
          let component${x} = offset${x} % 4u;
          ${S}[${x}] = ${b}(${g.getByOffset(`index${x}`)}[component${x}]);
        `;_=`
        let outputOffset = global_idx * ${u};
        var data = vec4<u32>(0);
        ${w("data",0,"u32")}
        ${w("data",1,"u32")}
        ${w("data",2,"u32")}
        ${w("data",3,"u32")}
        ${y.setByOffset("global_idx","data")}
      }`}else _=`
        let outputIndices = ${y.offsetToIndices(`global_idx * ${u}`)};
        let inputOffset = ${g.broadcastedIndicesToOffset("outputIndices",y)};
        let data = ${y.type.value}(${g.getByOffset(`inputOffset / ${s}`)});
        ${y.setByOffset("global_idx","data")}
      }`;return`
    ${f.registerUniform("vec_size","u32").declareVariables(g,y)}
    ${f.mainStart()}
    ${f.guardAgainstOutOfBoundsWorkgroupSizes("uniforms.vec_size")}
    ${_}`},h=[{type:12,data:l},...Y(t,i)];return{name:"Expand",shaderCache:{hint:`${i.length};${s}${u}`,inputDependencies:["rank"]},getShaderSource:p,getRunData:()=>({outputs:[{dims:i,dataType:e[0].dataType}],dispatchGroup:{x:Math.ceil(l/64)},programUniforms:h})}},Rl=e=>{Cl(e.inputs),e.compute(Ol(e.inputs),{inputs:[0]})}}),Bl,Ml,vm=q(()=>{te(),re(),ae(),Zi(),Bl=e=>{let t=e[0].dataType,r=O.size(e[0].dims),i=O.size(e[1].dims),a=i%4===0,n=s=>{let u=M("x",t,[1],4),l=M("bias",t,[1],4),p=Q("y",t,[1],4),h=[{name:"output_vec_size",type:"u32"},{name:"bias_size",type:"u32"}],f=y=>`
      let bias${y}_offset: u32 = (global_idx * 4 + ${y}) % uniforms.bias_size;
      let bias${y} = ${l.getByOffset(`bias${y}_offset / 4`)}[bias${y}_offset % 4];`,g=a?`
      let bias = ${l.getByOffset("global_idx % (uniforms.bias_size / 4)")};`:`${f(0)}${f(1)}${f(2)}${f(3)}
      let bias = ${u.type.value}(bias0, bias1, bias2, bias3);`;return`${s.registerUniforms(h).declareVariables(u,l,p)}

    ${Ki(ze(t))}

    ${s.mainStart(Wt)}
      ${s.guardAgainstOutOfBoundsWorkgroupSizes("uniforms.output_vec_size")}

      let x = ${u.getByOffset("global_idx")};
      ${g}
      let x_in = x + bias;
      ${p.setByOffset("global_idx",Qi("x_in"))}
    }`};return{name:"FastGeluWithBias",shaderCache:{hint:`${a}`,inputDependencies:["type","type"]},getShaderSource:n,getRunData:s=>({outputs:[{dims:s[0].dims,dataType:s[0].dataType}],programUniforms:[{type:12,data:Math.ceil(r/4)},{type:12,data:i}],dispatchGroup:{x:Math.ceil(r/Wt/4)}})}},Ml=e=>{e.inputs.length<2||O.size(e.inputs[1].dims)===0?mu(e):e.compute(Bl(e.inputs))}}),Nl,Dl,Ul,Pl,xm=q(()=>{te(),re(),xe(),ae(),Nl=e=>{if(!e||e.length!==2)throw new Error("Gather requires 2 inputs.")},Dl=(e,t)=>{let r=e[0].dims,i=e[1].dims,a=r.length,n=O.normalizeAxis(t.axis,a),s=r.slice(0);s.splice(n,1,...i);let u=r[n],l=e[0].dataType===9?4:1,p=Math.ceil(O.size(s)/l),h=[{type:12,data:p},{type:6,data:u},{type:12,data:n},...Y(e[0].dims,e[1].dims,s)],f=g=>{let y=M("data",e[0].dataType,e[0].dims.length,l),_=M("inputIndices",e[1].dataType,e[1].dims.length),w=Q("output",e[0].dataType,s.length,l),S=b=>{let I=i.length,k=`var indicesIndices${b}  = ${_.type.indices}(0);`;for(let E=0;E<I;E++)k+=`${I>1?`indicesIndices${b}[${E}]`:`indicesIndices${b}`} = ${s.length>1?`outputIndices${b}[uniforms.axis + ${E}]`:`outputIndices${b}`};`;k+=`
          var idx${b} = ${_.getByIndices(`indicesIndices${b}`)};
          if (idx${b} < 0) {
            idx${b} = idx${b} + uniforms.axisDimLimit;
          }
          var dataIndices${b} : ${y.type.indices};
        `;for(let E=0,A=0;E<a;E++)E===n?(k+=`${a>1?`dataIndices${b}[${E}]`:`dataIndices${b}`} = u32(idx${b});`,A+=I):(k+=`${a>1?`dataIndices${b}[${E}]`:`dataIndices${b}`} = ${s.length>1?`outputIndices${b}[${A}]`:`outputIndices${b}`};`,A++);return k},x;if(e[0].dataType===9){let b=(I,k,E="")=>`
          let outputIndices${k} = ${w.offsetToIndices(`outputOffset + ${k}u`)};
          ${S(k)};
          let offset${k} = ${y.indicesToOffset(`dataIndices${k}`)};
          let index${k} = offset${k} / 4u;
          let component${k} = offset${k} % 4u;
          ${I}[${k}] = ${E}(${y.getByOffset(`index${k}`)}[component${k}]);
        `;x=`
        let outputOffset = global_idx * ${l};
        var value = vec4<u32>(0);
        ${b("value",0,"u32")}
        ${b("value",1,"u32")}
        ${b("value",2,"u32")}
        ${b("value",3,"u32")}
        ${w.setByOffset("global_idx","value")}
      `}else x=`
      let outputIndices = ${w.offsetToIndices("global_idx")};
      ${S("")};
      let value = ${y.getByIndices("dataIndices")};
      ${w.setByOffset("global_idx","value")};
      `;return`
      ${g.registerUniform("outputSize","u32").registerUniform("axisDimLimit","i32").registerUniform("axis","u32").declareVariables(y,_,w)}
      ${g.mainStart()}
        ${g.guardAgainstOutOfBoundsWorkgroupSizes("uniforms.outputSize")}
        ${x}
      }`};return{name:"Gather",shaderCache:{hint:t.cacheKey,inputDependencies:["rank","rank"]},getRunData:()=>({outputs:[{dims:s,dataType:e[0].dataType}],dispatchGroup:{x:Math.ceil(p/64)},programUniforms:h}),getShaderSource:f}},Ul=e=>he({axis:e.axis}),Pl=(e,t)=>{let r=e.inputs;Nl(r),e.compute(Dl(e.inputs,t))}}),ql,Ll,Wl,Sm=q(()=>{te(),re(),ae(),ql=(e,t,r,i,a,n,s,u,l)=>{let p=[{type:12,data:n},{type:12,data:i},{type:12,data:a},{type:12,data:r},{type:12,data:s},{type:12,data:u},{type:12,data:l}],h=[n];p.push(...Y(t.dims,h));let f=g=>{let y=M("indices_data",t.dataType,t.dims.length),_=Q("input_slice_offsets_data",12,1,1),w=[y,_],S=[{name:"output_size",type:"u32"},{name:"batch_dims",type:"u32"},{name:"input_dims",type:"u32",length:a.length},{name:"sizes_from_slice_dims_data",type:"u32",length:r.length},{name:"num_slices_per_batch",type:"u32"},{name:"input_batch_stride",type:"u32"},{name:"num_slice_dims",type:"u32"}];return`
  ${g.registerUniforms(S).declareVariables(...w)}
  ${g.mainStart()}
    ${g.guardAgainstOutOfBoundsWorkgroupSizes("uniforms.output_size")}
    let batch_idx = global_idx / uniforms.num_slices_per_batch;
    let base_offset = batch_idx * uniforms.input_batch_stride;

    let slice_indices_base_offset = global_idx * uniforms.num_slice_dims;
    var relative_slice_offset = 0;
    for (var dim_idx = 0u; dim_idx < uniforms.num_slice_dims; dim_idx ++) {
      var index = i32(indices_data[dim_idx + slice_indices_base_offset].x);
      let input_dim_idx = uniforms.batch_dims + dim_idx;
      if (index < 0) {
        ${a.length===1?"index += i32(uniforms.input_dims);":"index += i32(uniforms.input_dims[input_dim_idx]);"}
      }
      ${r.length===1?"relative_slice_offset += index * i32(uniforms.sizes_from_slice_dims_data);":"relative_slice_offset += index * i32(uniforms.sizes_from_slice_dims_data[dim_idx]);"}
    }

    input_slice_offsets_data[global_idx] =  base_offset + u32(relative_slice_offset);
  }`};return e.compute({name:"computeSliceOffsets",shaderCache:{hint:`${a.length}_${r.length}`,inputDependencies:["rank"]},getRunData:()=>({outputs:[{dims:h,dataType:e.inputs[1].dataType}],dispatchGroup:{x:Math.ceil(n/64)},programUniforms:p}),getShaderSource:f},{inputs:[t],outputs:[-1]})[0]},Ll=(e,t)=>{let r=e.inputs,i=r[0].dims,a=r[0].dataType,n=r[1].dims,s=n[n.length-1],u=O.sizeToDimension(n,n.length-1),l=O.sizeFromDimension(i,t.batchDims+s),p=O.sizeToDimension(i,t.batchDims),h=O.sizeFromDimension(i,t.batchDims),f=u/p,g=new Array(s),y=l;for(let k=0;k<s;++k)g[s-1-k]=y,y*=i[t.batchDims+s-1-k];let _=ql(e,r[1],g,t.batchDims,i,u,f,h,s),w=t.batchDims+s;if(w>i.length)throw new Error("last dimension of indices must not be larger than rank of input tensor");let S=n.slice(0,-1).concat(i.slice(w)),x=O.size(S),b=[{type:12,data:x},{type:12,data:l},...Y(r[0].dims,_.dims,S)],I=k=>{let E=M("data",r[0].dataType,r[0].dims.length),A=M("slice_offsets",12,_.dims.length),C=Q("output",r[0].dataType,S.length);return`
          ${k.registerUniform("output_size","u32").registerUniform("slice_size","u32").declareVariables(E,A,C)}
            ${k.mainStart()}
            ${k.guardAgainstOutOfBoundsWorkgroupSizes("uniforms.output_size")}
          let slice_offset = slice_offsets[global_idx / uniforms.slice_size];
          output[global_idx] = data[u32(slice_offset) + global_idx % uniforms.slice_size];
        }`};e.compute({name:"GatherND",shaderCache:{hint:t.cacheKey,inputDependencies:["rank","rank"]},getRunData:()=>({outputs:[{dims:S,dataType:a}],dispatchGroup:{x:Math.ceil(x/64)},programUniforms:b}),getShaderSource:I},{inputs:[r[0],_]})},Wl=e=>({batchDims:e.batch_dims,cacheKey:""})}),Vl,Gl,Hl,Fl,Tm=q(()=>{te(),re(),xe(),ae(),Vl=(e,t)=>{if(e.length<3||e.length>4)throw new Error("GatherBlockQuantized requires 3 or 4 inputs.");let r=O.normalizeAxis(t.quantizeAxis,e[0].dims.length),i=t.blockSize,a=e[0],n=e[2],s=e.length===4?e[3]:void 0;if(n.dims.length!==a.dims.length||!a.dims.map((u,l)=>l===r?Math.ceil(u/i)===n.dims[l]:u===n.dims[l]).reduce((u,l)=>u&&l,!0))throw new Error("Scales must have the same rank as the input tensor and the dims should match except on gatherAxis.");if(s){if(s.dataType!==a.dataType)throw new Error("Zero point must have the same data type as the input tensor.");if(s.dims.length!==n.dims.length||!s.dims.map((u,l)=>u===n.dims[l]).reduce((u,l)=>u&&l,!0))throw new Error("Zero point must have the same rank as the input tensor and the dims should match except on quantizeAxis.")}},Gl=(e,t)=>{let r=e[0].dims,i=e[1].dims,a=r.length,n=O.normalizeAxis(t.gatherAxis,a),s=O.normalizeAxis(t.quantizeAxis,a),u=r.slice(0);u.splice(n,1,...i);let l=O.size(u),p=e[2].dataType,h=e[0].dataType===22,f=[{type:12,data:l},{type:12,data:s},{type:12,data:n},{type:12,data:t.blockSize},...Y(...e.map((y,_)=>y.dims),u)],g=y=>{let _=M("data",e[0].dataType,e[0].dims.length),w=M("inputIndices",e[1].dataType,e[1].dims.length),S=M("scales",e[2].dataType,e[2].dims.length),x=e.length>3?M("zeroPoint",e[3].dataType,e[3].dims.length):void 0,b=Q("output",p,u.length),I=[_,w,S];x&&I.push(x);let k=[{name:"output_size",type:"u32"},{name:"quantize_axis",type:"u32"},{name:"gather_axis",type:"u32"},{name:"block_size",type:"u32"}];return`
        ${y.registerUniforms(k).declareVariables(...I,b)}
        ${y.mainStart()}
        let output_indices = ${b.offsetToIndices("global_idx")};
        var indices_indices = ${w.type.indices}(0);
        ${i.length>1?`
          for (var i: u32 = 0; i < ${i.length}; i++) {
            let index = ${b.indicesGet("output_indices","uniforms.gather_axis + i")};
            ${w.indicesSet("indices_indices","i","index")};
          }`:`indices_indices = ${b.indicesGet("output_indices","uniforms.gather_axis")};`};
        var data_indices = ${_.type.indices}(0);
        for (var i: u32 = 0; i < uniforms.gather_axis; i++) {
          let index = ${b.indicesGet("output_indices","i")};
          ${_.indicesSet("data_indices","i","index")};
        }
        var index_from_indices = ${w.getByIndices("indices_indices")};
        if (index_from_indices < 0) {
          index_from_indices += ${r[n]};
        }
        ${_.indicesSet("data_indices","uniforms.gather_axis","u32(index_from_indices)")};
        for (var i = uniforms.gather_axis + 1; i < ${u.length}; i++) {
          let index = ${b.indicesGet("output_indices",`i + ${i.length} - 1`)};
          ${_.indicesSet("data_indices","i","index")};
        }
        let data_offset = ${_.indicesToOffset("data_indices")};
        let data_index = data_offset % 8;
        // Convert 4-bit packed data to 8-bit packed data.
        let packed_4bit_quantized_data = ${_.getByOffset("data_offset / 8")};
        let packed_8bit_quantized_data = (packed_4bit_quantized_data >> (4 * (data_index % 2))) & 0x0f0f0f0f;
        let quantized_data_vec = ${h?"unpack4xI8":"unpack4xU8"}(u32(packed_8bit_quantized_data));
        let quantized_data = quantized_data_vec[data_index / 2];
        var scale_indices = data_indices;
        let quantize_axis_index = ${S.indicesGet("data_indices","uniforms.quantize_axis")} / uniforms.block_size;
        ${S.indicesSet("scale_indices","uniforms.quantize_axis","quantize_axis_index")};
        var scale = ${S.getByIndices("scale_indices")};
        ${x?`
              let zero_point_indices = scale_indices;
              let zero_point_offset = ${x.indicesToOffset("zero_point_indices")};
              let zero_point_index = zero_point_offset % 8;
              let packed_4bit_zero_points = ${x.getByOffset("zero_point_offset / 8")};
              let packed_8bit_zero_points = (packed_4bit_zero_points >> (4 * (zero_point_index % 2))) & 0x0f0f0f0f;
              let zero_point_vec = ${h?"unpack4xI8":"unpack4xU8"}(u32(packed_8bit_zero_points));
              let zero_point = zero_point_vec[zero_point_index / 2];`:"var zero_point = 0"};
        let dequantized_data = ${ze(p)}(quantized_data - zero_point) * scale;
        ${b.setByOffset("global_idx","dequantized_data")};
    }`};return{name:"GatherBlockQuantized",shaderCache:{hint:`${t.cacheKey};${e.filter((y,_)=>_!==1).map(y=>y.dims.join("_")).join(";")}`,inputDependencies:Array.from({length:e.length},(y,_)=>"rank")},getRunData:()=>({outputs:[{dims:u,dataType:p}],dispatchGroup:{x:Math.ceil(l/64)},programUniforms:f}),getShaderSource:g}},Hl=(e,t)=>{let r=e.inputs;Vl(r,t),e.compute(Gl(e.inputs,t))},Fl=e=>he({blockSize:e.blockSize,gatherAxis:e.gatherAxis,quantizeAxis:e.quantizeAxis})}),jl,Kl,Ql,Zl,km=q(()=>{te(),re(),xe(),ae(),jl=e=>{if(!e||e.length!==2)throw new Error("GatherElements requires 2 inputs.");if(e[0].dims.length<1)throw new Error("GatherElements requires that the data input be rank >= 1.");if(e[0].dims.length!==e[1].dims.length)throw new Error(`GatherElements requires that the data input and
                     indices input tensors be of same rank.`)},Kl=(e,t)=>{let r=e[0].dims,i=e[0].dataType,a=r.length,n=e[1].dims,s=e[1].dataType,u=O.normalizeAxis(t.axis,a),l=r[u],p=n.slice(0),h=O.size(p),f=M("input",i,a),g=M("indicesInput",s,n.length),y=Q("output",i,p.length),_=[{type:12,data:h},{type:6,data:l},{type:12,data:u}];return _.push(...Y(r,n,p)),{name:"GatherElements",shaderCache:{inputDependencies:["rank","rank"]},getRunData:()=>({outputs:[{dims:p,dataType:e[0].dataType}],dispatchGroup:{x:Math.ceil(h/64)},programUniforms:_}),getShaderSource:w=>`
      ${w.registerUniform("outputSize","u32").registerUniform("axisDimLimit","i32").registerUniform("axis","u32").declareVariables(f,g,y)}
      ${w.mainStart()}
      ${w.guardAgainstOutOfBoundsWorkgroupSizes("uniforms.outputSize")}

      let outputIndices = ${y.offsetToIndices("global_idx")};

      var idx = ${g.getByOffset("global_idx")};
      if (idx < 0) {
        idx = idx + uniforms.axisDimLimit;
      }
      var inputIndices = ${f.type.indices}(outputIndices);
      ${f.indicesSet("inputIndices","uniforms.axis","u32(idx)")};
      let value = ${f.getByIndices("inputIndices")};

      ${y.setByOffset("global_idx","value")};
  }`}},Ql=e=>he({axis:e.axis}),Zl=(e,t)=>{let r=e.inputs;jl(r),e.compute(Kl(e.inputs,t))}}),Yl,Xl,Jl,ed,Im=q(()=>{te(),re(),ae(),Yl=e=>{if(!e)throw new Error("Input is missing");if(e.length<2||e.length>3)throw new Error("Invaid input number.");if(e.length===3&&e[2].dims.length>2)throw new Error("Invalid input shape of C");if(e[0].dataType!==e[1].dataType||e.length===3&&e[0].dataType!==e[2].dataType)throw new Error("Input types are mismatched")},Xl=(e,t)=>{let r=e[0].dims.slice(),i=e[1].dims.slice(),[a,n,s]=us.getShapeOfGemmResult(r,t.transA,i,t.transB,e.length===3?e[2].dims:void 0),u=[a,n];if(!u)throw new Error("Can't use gemm on the given tensors");let l=16,p=Math.ceil(n/l),h=Math.ceil(a/l),f=!0,g=O.size(u),y=[{type:12,data:f?p:g},{type:12,data:a},{type:12,data:n},{type:12,data:s},{type:1,data:t.alpha},{type:1,data:t.beta}],_=["type","type"];e.length===3&&(y.push(...Y(e[2].dims)),_.push("rank")),y.push(...Y(u));let w=x=>{let b="";t.transA&&t.transB?b="value += a[k * uniforms.M + m] * b[n * uniforms.K + k];":t.transA&&!t.transB?b="value += a[k * uniforms.M + m] * b[k * uniforms.N + n];":!t.transA&&t.transB?b="value += a[m * uniforms.K + k] * b[n * uniforms.K + k];":!t.transA&&!t.transB&&(b="value += a[m * uniforms.K + k] * b[k * uniforms.N + n];");let I=t.alpha===1?"":"value *= uniforms.alpha;",k=M("a",e[0].dataType,e[0].dims),E=M("b",e[1].dataType,e[1].dims),A=k.type.value,C=null,$=[k,E];e.length===3&&(C=M("c",e[2].dataType,e[2].dims.length),$.push(C));let N=Q("output",e[0].dataType,u.length);$.push(N);let D=[{name:"output_size",type:"u32"},{name:"M",type:"u32"},{name:"N",type:"u32"},{name:"K",type:"u32"},{name:"alpha",type:"f32"},{name:"beta",type:"f32"}];return`
  ${x.registerUniforms(D).declareVariables(...$)}

  ${x.mainStart()}
    ${x.guardAgainstOutOfBoundsWorkgroupSizes("uniforms.output_size")}

    let m = global_idx / uniforms.N;
    let n = global_idx % uniforms.N;

    var value = ${A}(0);
    for (var k: u32 = 0u; k < uniforms.K; k++) {
      ${b}
    }

    ${I}
    ${C!=null?`let cOffset = ${C.broadcastedIndicesToOffset("vec2(m, n)",N)}; value += ${A}(uniforms.beta) * ${C.getByOffset("cOffset")};`:""}
    output[global_idx] = value;
  }`},S=x=>{let b=M("a",e[0].dataType,e[0].dims),I=M("b",e[1].dataType,e[1].dims),k=null,E=[b,I];e.length===3&&(k=M("c",e[2].dataType,e[2].dims.length),E.push(k));let A=Q("output",e[0].dataType,u.length);E.push(A);let C=[{name:"num_tile_n",type:"u32"},{name:"M",type:"u32"},{name:"N",type:"u32"},{name:"K",type:"u32"},{name:"alpha",type:"f32"},{name:"beta",type:"f32"}],$="",N="";t.transA&&t.transB?(N=`
      var col = tile_row_start + local_id.x;
      var row = k_start + local_id.y;
      if (col < uniforms.M && row < uniforms.K) {
        tile_a[local_id.y][local_id.x] = a[row * uniforms.M + col];
      } else {
        tile_a[local_id.y][local_id.x] = ${b.type.value}(0);
      }

      col = k_start + local_id.x;
      row = tile_col_start + local_id.y;
      if (col < uniforms.K && row < uniforms.N) {
        tile_b[local_id.y][local_id.x] = b[row * uniforms.K + col];
      } else {
        tile_b[local_id.y][local_id.x] = ${I.type.value}(0);
      }
      `,$="value += tile_a[k][local_id.y] * tile_b[local_id.x][k];"):t.transA&&!t.transB?(N=`
      var col = tile_row_start + local_id.x;
      var row = k_start + local_id.y;
      if (col < uniforms.M && row < uniforms.K) {
        tile_a[local_id.y][local_id.x] = a[row * uniforms.M + col];
      } else {
        tile_a[local_id.y][local_id.x] = ${b.type.value}(0);
      }

      col = tile_col_start + local_id.x;
      row = k_start + local_id.y;
      if (col < uniforms.N && row < uniforms.K) {
        tile_b[local_id.y][local_id.x] = b[row * uniforms.N + col];
      } else {
        tile_b[local_id.y][local_id.x] = ${I.type.value}(0);
      }
      `,$="value += tile_a[k][local_id.y] * tile_b[k][local_id.x];"):!t.transA&&t.transB?(N=`
      var col = k_start + local_id.x;
      var row = tile_row_start + local_id.y;
      if (col < uniforms.K && row < uniforms.M) {
        tile_a[local_id.y][local_id.x] = a[row * uniforms.K + col];
      } else {
        tile_a[local_id.y][local_id.x] = ${b.type.value}(0);
      }

      col = k_start + local_id.x;
      row = tile_col_start + local_id.y;
      if (col < uniforms.K && row < uniforms.N) {
        tile_b[local_id.y][local_id.x] = b[row * uniforms.K + col];
      } else {
        tile_b[local_id.y][local_id.x] = ${I.type.value}(0);
      }
      `,$="value += tile_a[local_id.y][k] * tile_b[local_id.x][k];"):!t.transA&&!t.transB&&(N=`
      var col = k_start + local_id.x;
      var row = tile_row_start + local_id.y;
      if (col < uniforms.K && row < uniforms.M) {
        tile_a[local_id.y][local_id.x] = a[row * uniforms.K + col];
      } else {
        tile_a[local_id.y][local_id.x] = ${b.type.value}(0);
      }

      col = tile_col_start + local_id.x;
      row = k_start + local_id.y;
      if (col < uniforms.N && row < uniforms.K) {
        tile_b[local_id.y][local_id.x] = b[row * uniforms.N + col];
      } else {
        tile_b[local_id.y][local_id.x] = ${I.type.value}(0);
      }
      `,$="value += tile_a[local_id.y][k] * tile_b[k][local_id.x];");let D=t.alpha===1?"":"value *= uniforms.alpha;";return`
  ${x.registerUniforms(C).declareVariables(...E)}
  var<workgroup> tile_a: array<array<${b.type.storage}, ${l}>, ${l}>;
  var<workgroup> tile_b: array<array<${I.type.storage}, ${l}>, ${l}>;
  ${x.mainStart([l,l,1])}
    let tile_col_start = (workgroup_index % uniforms.num_tile_n) * ${l};
    let tile_row_start = (workgroup_index / uniforms.num_tile_n) * ${l};
    let num_tiles = (uniforms.K - 1) / ${l} + 1;
    var k_start = 0u;
    var value = ${A.type.value}(0);
    for (var t: u32 = 0u; t < num_tiles; t++) {
      ${N}
      k_start = k_start + ${l};
      workgroupBarrier();

      for (var k: u32 = 0u; k < ${l}; k++) {
        ${$}
      }
      workgroupBarrier();
    }

    ${D}
    let m = tile_row_start + local_id.y;
    let n = tile_col_start + local_id.x;
    ${k!=null?`let cOffset = ${k.broadcastedIndicesToOffset("vec2(m, n)",A)}; value += ${A.type.value}(uniforms.beta) * ${k.getByOffset("cOffset")};`:""}
    if (m < uniforms.M && n < uniforms.N) {
      output[m * uniforms.N + n] = value;
    }
  }`};return f?{name:"GemmShared",shaderCache:{hint:`${t.cacheKey}`,inputDependencies:_},getRunData:()=>({outputs:[{dims:u,dataType:e[0].dataType}],dispatchGroup:{x:p*h},programUniforms:y}),getShaderSource:S}:{name:"Gemm",shaderCache:{hint:`${t.cacheKey}`,inputDependencies:_},getRunData:()=>({outputs:[{dims:u,dataType:e[0].dataType}],dispatchGroup:{x:Math.ceil(g/64)},programUniforms:y}),getShaderSource:w}},Jl=e=>{let t=e.transA,r=e.transB,i=e.alpha,a=e.beta;return{transA:t,transB:r,alpha:i,beta:a,cacheKey:`${e.transA};${e.transB};${e.alpha===1}`}},ed=(e,t)=>{Yl(e.inputs),e.compute(Xl(e.inputs,t))}}),Ze,nt,At,Ot,td,rd,id,ad,nd,sd,od,ud,ld,dd,Em=q(()=>{te(),re(),xe(),ae(),[Ze,nt,At,Ot]=[0,1,2,3],td=e=>{if(e[0].dims.length!==4)throw new Error("only 4-D tensor is supported.");if(e[0].dims.length!==e[1].dims.length)throw new Error("input dimensions must be equal to grid dimensions");if(e[0].dims.length-2!==e[1].dims[e[1].dims.length-1])throw new Error(`last dimension of grid must be equal to ${e[0].dims.length-2}`);if(e[0].dims[0]!==e[1].dims[0])throw new Error("grid batch size must match input batch size")},rd=`
  fn gs_get_cubic_coeffs(x: f32) -> vec4<f32> {
    let cubic_alpha = -0.75f;
    let x_abs = abs(x);
    var coeffs: vec4<f32>;
    coeffs[0] = (((cubic_alpha * (x_abs + 1) - 5 * cubic_alpha) * (x_abs + 1) + 8 * cubic_alpha) * (x_abs + 1) - 4 * cubic_alpha);
    coeffs[1] = (((cubic_alpha + 2) * x_abs - (cubic_alpha + 3)) * x_abs * x_abs + 1);
    coeffs[2] = (((cubic_alpha + 2) * (1 - x_abs) - (cubic_alpha + 3)) * (1 - x_abs) * (1 - x_abs) + 1);
    coeffs[3] = (((cubic_alpha * (2 - x_abs) - 5 * cubic_alpha) * (2 - x_abs) + 8 * cubic_alpha) * (2 - x_abs) - 4 * cubic_alpha);
    return coeffs;
  }
`,id=e=>`
  fn gs_bicubic_interpolate(p: mat4x4<${e}>, x: f32, y: f32) -> ${e} {
    var v: vec4<f32>;
    var coeffs = gs_get_cubic_coeffs(x);
    for (var i = 0; i < 4; i++) {
      v[i] = coeffs[0] * p[i][0] + coeffs[1] * p[i][1] + coeffs[2] * p[i][2] + coeffs[3] * p[i][3];
    }
    coeffs = gs_get_cubic_coeffs(y);
    let pixel = ${e}(coeffs[0] * v[0] + coeffs[1] * v[1] + coeffs[2] * v[2] + coeffs[3] * v[3]);
    return pixel;
  }
`,ad=e=>`
  fn gs_denormalize(n: f32, length: i32) -> f32 {
    ${e.alignCorners===0?`
    // alignCorners: false => [-1, 1] to [-0.5, length - 0.5]
    return ((n + 1.0) * f32(length) - 1.0) / 2.0;
    `:`
    // alignCorners: true => [-1, 1] to [0, length - 1]
    return (n + 1.0) / 2.0 * (f32(length - 1));
    `}
  }
`,nd=e=>`
  ${e.paddingMode==="reflection"?`
      fn gs_reflect(x: i32, x_min: f32, x_max: f32) -> u32 {
        var dx = 0.0;
        var fx = f32(x);
        let range = x_max - x_min;
        if (fx < x_min) {
          dx = x_min - fx;
          let n = u32(dx / range);
          let r = dx - f32(n) * range;
          if (n % 2 == 0) {
            fx = x_min + r;
          } else {
            fx = x_max - r;
          }
        } else if (fx > x_max) {
          dx = fx - x_max;
          let n = u32(dx / range);
          let r = dx - f32(n) * range;
          if (n % 2 == 0) {
            fx = x_max - r;
          } else {
            fx = x_min + r;
          }
        }
        return u32(fx);
      }`:""}
`,sd=(e,t,r)=>`
  fn pixel_at_grid(r: i32, c: i32, H: i32, W: i32, batch: u32, channel: u32, border: vec4<f32>) -> ${t} {
     var pixel = ${t}(0);
     var indices = vec4<u32>(0);
     indices[${Ze}] = batch;
     indices[${nt}] = channel;`+(()=>{switch(r.paddingMode){case"zeros":return`
          if (r >= 0 && r < H && c >=0 && c < W) {
            indices[${At}] = u32(r);
            indices[${Ot}] = u32(c);
          } else {
            return ${t}(0);
          }
        `;case"border":return`
          indices[${At}] = u32(clamp(r, 0, H - 1));
          indices[${Ot}] = u32(clamp(c, 0, W - 1));
        `;case"reflection":return`
          indices[${At}] = gs_reflect(r, border[1], border[3]);
          indices[${Ot}] = gs_reflect(c, border[0], border[2]);
        `;default:throw new Error(`padding mode ${r.paddingMode} is not supported`)}})()+`
    return ${e.getByIndices("indices")};
  }
`,od=(e,t,r)=>(()=>{switch(r.mode){case"nearest":return`
          let result = pixel_at_grid(i32(round(y)), i32(round(x)), H_in, W_in, indices[${Ze}], indices[${nt}], border);
        `;case"bilinear":return`
          let x1 = i32(floor(x));
          let y1 = i32(floor(y));
          let x2 = x1 + 1;
          let y2 = y1 + 1;

          let p11 = pixel_at_grid(y1, x1, H_in, W_in, indices[${Ze}], indices[${nt}], border);
          let p12 = pixel_at_grid(y1, x2, H_in, W_in, indices[${Ze}], indices[${nt}], border);
          let p21 = pixel_at_grid(y2, x1, H_in, W_in, indices[${Ze}], indices[${nt}], border);
          let p22 = pixel_at_grid(y2, x2, H_in, W_in, indices[${Ze}], indices[${nt}], border);

          let dx2 = ${t}(f32(x2) - x);
          let dx1 = ${t}(x - f32(x1));
          let dy2 = ${t}(f32(y2) - y);
          let dy1 = ${t}(y - f32(y1));
          let result = dy2 * (dx2 * p11 + dx1 * p12) + dy1 * (dx2 * p21 + dx1 * p22);
        `;case"bicubic":return`
          let x0 = i32(floor(x)) - 1;
          let y0 = i32(floor(y)) - 1;
          var p: mat4x4<${t}>;
          for (var h = 0; h < 4; h++) {
            for (var w = 0; w < 4; w++) {
              p[h][w] = pixel_at_grid(h + y0, w + x0, H_in, W_in, indices[${Ze}], indices[${nt}], border);
            }
          }

          let dx = x - f32(x0 + 1);
          let dy = y - f32(y0 + 1);
          let result = gs_bicubic_interpolate(p, dx, dy);
        `;default:throw new Error(`mode ${r.mode} is not supported`)}})()+`${e.setByOffset("global_idx","result")}`,ud=(e,t)=>{let r=M("x",e[0].dataType,e[0].dims.length),i=[e[1].dims[0],e[1].dims[1],e[1].dims[2]],a=M("grid",e[1].dataType,i.length,2),n=[e[0].dims[0],e[0].dims[1],e[1].dims[1],e[1].dims[2]];t.format==="NHWC"&&(n=[e[0].dims[0],e[1].dims[1],e[1].dims[2],e[0].dims[3]],[Ze,nt,At,Ot]=[0,3,1,2]);let s=Q("output",e[0].dataType,n.length),u=r.type.value,l=O.size(n),p=[{type:12,data:l},...Y(e[0].dims,i,n)],h=f=>`
  ${f.registerUniform("output_size","u32").declareVariables(r,a,s)}
  ${rd}
  ${id(u)}
  ${ad(t)}
  ${nd(t)}
  ${sd(r,u,t)}

  ${f.mainStart()}
    ${f.guardAgainstOutOfBoundsWorkgroupSizes("uniforms.output_size")}
      let H_in = i32(uniforms.x_shape[${At}]);
      let W_in = i32(uniforms.x_shape[${Ot}]);

      ${t.alignCorners===0?`
      let x_min = -0.5;
      let x_max = f32(W_in) - 0.5;
      let y_min = -0.5;
      let y_max = f32(H_in) - 0.5;
      `:`
      let x_min = 0.0;
      let x_max = f32(W_in) - 1.0;
      let y_min = 0.0;
      let y_max = f32(H_in) - 1.0;
      `};
      let border = vec4<f32>(x_min, y_min, x_max, y_max);

      let indices = ${s.offsetToIndices("global_idx")};
      var grid_indices = vec3<u32>(indices[${Ze}], indices[${At}], indices[${Ot}]);
      let nxy = ${a.getByIndices("grid_indices")};
      var x = gs_denormalize(f32(nxy[0]), W_in);
      var y = gs_denormalize(f32(nxy[1]), H_in);

      ${od(s,u,t)}
  }`;return{name:"GridSample",shaderCache:{hint:`${t.cacheKey}`,inputDependencies:["type","type"]},getRunData:f=>{let g=O.size(n);return{outputs:[{dims:n,dataType:f[0].dataType}],dispatchGroup:{x:Math.ceil(g/64)},programUniforms:p}},getShaderSource:h}},ld=(e,t)=>{td(e.inputs),e.compute(ud(e.inputs,t))},dd=e=>he({alignCorners:e.align_corners,mode:e.mode,paddingMode:e.padding_mode,format:e.format})}),Ae,pd,cd,ma,hd,nr,fd,md=q(()=>{te(),re(),xe(),Mi(),Fi(),ae(),dt(),Ae=(e,t)=>e.length>t&&e[t].dims.length>0?e[t]:void 0,pd=(e,t)=>{let r=e[0],i=Ae(e,1),a=Ae(e,2),n=Ae(e,3),s=Ae(e,4),u=Ae(e,5),l=Ae(e,6),p=Ae(e,7);if(r.dims.length!==3&&r.dims.length!==5)throw new Error("Input query is expected to have 3 or 5 dimensions");let h=r.dims[0],f=r.dims[1],g=r.dims.length===3?r.dims[2]:t.numHeads*r.dims[4],y=f,_=0,w=0,S=Math.floor(g/t.numHeads);if(l&&p&&O.size(l.dims)&&O.size(p.dims)){if(l.dims.length!==4)throw new Error('Input "past_key" is expected to have 4 dimensions');if(l.dims[0]!==h||l.dims[1]!==t.numHeads||l.dims[3]!==S)throw new Error('Input "past_key" shape (batch_size, num_heads, past_sequence_length, head_size)');if(p.dims[0]!==h||p.dims[1]!==t.numHeads||p.dims[3]!==S)throw new Error('Input "past_value" shape (batch_size, num_heads, past_sequence_length, head_size)');if(l.dims[2]!==p.dims[2])throw new Error('Input "past_key" and "past_value" shall have same dim 2 (past_sequence_length)');if(p.dims.length!==4)throw new Error('Input "past_value" is expected to have 4 dimensions');_=l.dims[2],w=l.dims[2]}else if(l&&O.size(l.dims)||p&&O.size(p.dims))throw new Error('Input "past_key" and "past_value" shall be both present or both absent');let x;if(i&&O.size(i.dims)>0){if(r.dims.length!==3)throw new Error('Input "query" is expected to have 3 dimensions when key is given');if(i.dims.length<3||i.dims.length>5)throw new Error('Input "key" is expected to have 3, 4, or 5 dimensions');if(r.dims[0]!==i.dims[0])throw new Error('Input "query" and "key" shall have same dim 0 (batch size)');if(i.dims.length===3){if(i.dims[2]!==r.dims[2])throw new Error('Input "query" and "key" shall have same dim 2 (hidden_size)');x=2,y=i.dims[1]}else if(i.dims.length===5){if(i.dims[2]!==t.numHeads||i.dims[3]!==2||i.dims[4]!==S)throw new Error('Expect "key" shape (batch_size, kv_sequence_length, num_heads, 2, head_size) for packed kv');if(a)throw new Error('Expect "value" be none when "key" has packed kv format.');x=5,y=i.dims[1]}else{if(i.dims[1]!==t.numHeads||i.dims[3]!==S)throw new Error('Expect "key" shape (batch_size, num_heads, kv_sequence_length, head_size) for past_key');x=0,y=i.dims[2]}}else{if(r.dims.length!==5)throw new Error('Input "query" is expected to have 5 dimensions when key is empty');if(r.dims[2]!==t.numHeads||r.dims[3]!==3)throw new Error('Expect "query" shape (batch_size, kv_sequence_length, num_heads, 3, head_size) for packed kv');x=3}if(n&&O.size(n.dims)>0){if(n.dims.length!==1)throw new Error('Input "bias" is expected to have 1 dimension');if(i&&i.dims.length===5&&i.dims[3]===2)throw new Error("bias is not allowed for packed kv.")}let b=_+y,I=0;if(s&&O.size(s.dims)>0){I=8;let C=s.dims;throw C.length===1?C[0]===h?I=1:C[0]===3*h+2&&(I=3):C.length===2&&C[0]===h&&C[1]===b&&(I=5),I===8?new Error('Input "key_padding_mask" shape shall be (batch_size) or (batch_size, total_sequence_length)'):new Error("Mask not supported")}let k=!1,E=g;if(a&&O.size(a.dims)>0){if(a.dims.length!==3&&a.dims.length!==4)throw new Error('Input "value" is expected to have 3 or 4 dimensions');if(r.dims[0]!==a.dims[0])throw new Error('Input "query" and "value" shall have same dim 0 (batch_size)');if(a.dims.length===3){if(y!==a.dims[1])throw new Error('Input "key" and "value" shall have the same dim 1 (kv_sequence_length)');E=a.dims[2]}else{if(y!==a.dims[2])throw new Error('Input "key" and "value" shall have the same dim 2 (kv_sequence_length)');E=a.dims[1]*a.dims[3],k=!0}}let A=!1;if(s&&O.size(s.dims)>0)throw new Error("Key padding mask is not supported");if(u&&O.size(u.dims)>0){if(u.dims.length!==4)throw new Error('Input "attention_bias" is expected to have 4 dimensions');if(u.dims[0]!==h||u.dims[1]!==t.numHeads||u.dims[2]!==f||u.dims[3]!==b)throw new Error('Expect "attention_bias" shape (batch_size, num_heads, sequence_length, total_sequence_length)')}return{batchSize:h,sequenceLength:f,pastSequenceLength:_,kvSequenceLength:y,totalSequenceLength:b,maxSequenceLength:w,inputHiddenSize:0,hiddenSize:g,vHiddenSize:E,headSize:S,vHeadSize:Math.floor(E/t.numHeads),numHeads:t.numHeads,isUnidirectional:!1,pastPresentShareBuffer:!1,maskFilterValue:t.maskFilterValue,maskType:I,scale:t.scale,broadcastResPosBias:A,passPastInKv:k,qkvFormat:x}},cd=e=>he({...e}),ma=he({perm:[0,2,1,3]}),hd=(e,t,r,i,a,n,s)=>{let u=[i,a,n],l=O.size(u),p=[{type:12,data:l},{type:12,data:s},{type:12,data:n}],h=f=>{let g=Q("qkv_with_bias",t.dataType,u),y=M("qkv",t.dataType,u),_=M("bias",r.dataType,u),w=[{name:"output_size",type:"u32"},{name:"bias_offset",type:"u32"},{name:"hidden_size",type:"u32"}];return`
  ${f.registerUniforms(w).declareVariables(y,_,g)}
  ${f.mainStart()}
    ${f.guardAgainstOutOfBoundsWorkgroupSizes("uniforms.output_size")}
    let bias_offset_idx = (global_idx % uniforms.hidden_size) + uniforms.bias_offset;

    qkv_with_bias[global_idx] = qkv[global_idx] + bias[bias_offset_idx];
  }`};return e.compute({name:"MultiHeadAttentionAddBias",shaderCache:{inputDependencies:["type","type"]},getRunData:()=>({outputs:[{dims:u,dataType:t.dataType,gpuDataType:0}],dispatchGroup:{x:Math.ceil(l/64)},programUniforms:p}),getShaderSource:h},{inputs:[t,r],outputs:[-1]})[0]},nr=(e,t,r,i,a,n,s,u)=>{let l=n;if(s&&O.size(s.dims)>0){if(i===1)throw new Error("AddBiasReshape is not implemented. Please export your model with packed QKV or KV");return l=hd(e,n,s,t,i,r*a,u),l=l.reshape([t,i,r,a]),r===1||i===1?l:e.compute(Ne(l,ma.perm),{inputs:[l],outputs:[-1]})[0]}else return n.dims.length===3&&(l=n.reshape([t,i,r,a])),r===1||i===1?l:e.compute(Ne(l,ma.perm),{inputs:[l],outputs:[-1]})[0]},fd=(e,t)=>{let r=pd(e.inputs,t),i=e.inputs[0],a=Ae(e.inputs,1),n=Ae(e.inputs,2),s=Ae(e.inputs,3),u=Ae(e.inputs,4),l=Ae(e.inputs,5),p=Ae(e.inputs,6),h=Ae(e.inputs,7);if(i.dims.length===5)throw new Error("Packed QKV is not implemented");if((a==null?void 0:a.dims.length)===5)throw new Error("Packed KV is not implemented");let f=a&&n&&a.dims.length===4&&n.dims.length===4,g=nr(e,r.batchSize,r.numHeads,r.sequenceLength,r.headSize,i,s,0);if(f)return er(e,g,a,n,u,void 0,p,h,l,r);if(!a||!n)throw new Error("key and value must be provided");let y=nr(e,r.batchSize,r.numHeads,r.kvSequenceLength,r.headSize,a,s,r.hiddenSize),_=nr(e,r.batchSize,r.numHeads,r.kvSequenceLength,r.vHeadSize,n,s,2*r.hiddenSize);er(e,g,y,_,u,void 0,p,h,l,r)}}),gd,yd,_d,wd,ga,bd,$d,vd=q(()=>{te(),re(),xe(),ae(),gd=e=>{if(!e||e.length<1)throw new Error("too few inputs")},yd=(e,t)=>{let r=[],i=t.numOutputs;return e[1].dims[0]>0&&(e[1].getBigInt64Array().forEach(a=>r.push(Number(a))),i=r.length),he({numOutputs:i,axis:t.axis,splitSizes:r})},_d=e=>`
fn calculateOutputIndex(index: u32) -> u32 {
    for (var i: u32 = 0u; i < ${e}u; i += 1u ) {
    if (index < ${Z("uniforms.size_in_split_axis","i",e)}) {
        return i;
    }
    }
    return ${e}u;
}`,wd=e=>{let t=e.length,r=[];for(let i=0;i<t;++i){let a=e[i].setByIndices("indices","input[global_idx]");t===1?r.push(a):i===0?r.push(`if (output_number == ${i}u) { ${a} }`):i===t-1?r.push(`else { ${a} }`):r.push(`else if (output_number == ${i}) { ${a} }`)}return`
      fn writeBufferData(output_number: u32, indices: ${e[0].type.indices}, global_idx: u32) {
        ${r.join(`
`)}
      }`},ga=(e,t)=>{let r=e[0].dims,i=O.size(r),a=e[0].dataType,n=O.normalizeAxis(t.axis,r.length),s=new Array(t.numOutputs),u=M("input",a,r.length),l=new Array(t.numOutputs),p=[],h=[],f=0,g=[{type:12,data:i}];for(let _=0;_<t.numOutputs;_++){f+=t.splitSizes[_],l[_]=f;let w=r.slice();w[n]=t.splitSizes[_],h.push(w),s[_]=Q(`output${_}`,a,w.length),p.push({dims:h[_],dataType:e[0].dataType})}g.push({type:12,data:l},...Y(r,...h));let y=_=>`
  ${_.registerUniform("input_size","u32").registerUniform("size_in_split_axis","u32",l.length).declareVariables(u,...s)}
  ${_d(l.length)}
  ${wd(s)}

  ${_.mainStart()}
    ${_.guardAgainstOutOfBoundsWorkgroupSizes("uniforms.input_size")}

    var indices = ${u.offsetToIndices("global_idx")};
    var index = ${u.indicesGet("indices",n)};
    let output_number = calculateOutputIndex(index);
    if (output_number != 0) {
      index -= ${Z("uniforms.size_in_split_axis","output_number - 1u",l.length)};
      ${u.indicesSet("indices",n,"index")};
    }
    writeBufferData(output_number, indices, global_idx);
  }`;return{name:"Split",shaderCache:{hint:t.cacheKey,inputDependencies:["rank"]},getShaderSource:y,getRunData:()=>({outputs:p,dispatchGroup:{x:Math.ceil(i/64)},programUniforms:g})}},bd=(e,t)=>{gd(e.inputs);let r=e.inputs.length===1?t:yd(e.inputs,t);e.compute(ga(e.inputs,r),{inputs:[0]})},$d=e=>{let t=e.axis,r=e.splitSizes,i=e.numOutputs<0?r.length:e.numOutputs;if(i!==r.length)throw new Error("numOutputs and splitSizes length must be equal");return he({axis:t,numOutputs:i,splitSizes:r})}}),xd,Dr,Sd,Td=q(()=>{te(),re(),xe(),ae(),xd=(e,t)=>{let[r,i,a,n]=e,{numHeads:s,rotaryEmbeddingDim:u}=t;if(r.dims.length!==3&&r.dims.length!==4)throw new Error(`Input 'x' is expected to have 3 or 4 dimensions, got ${r.dims.length}`);if(!O.areEqual(i.dims,[])&&!O.areEqual(i.dims,[1])&&i.dims.length!==2)throw new Error(`Input 'position_ids' is expected to have 0, 1, or 2 dimensions, got ${i.dims.length}`);if(a.dims.length!==2)throw new Error(`Input 'cos_cache' is expected to have 2 dimensions, got ${a.dims.length}`);if(n.dims.length!==2)throw new Error(`Input 'sin_cache' is expected to have 2 dimensions, got ${n.dims.length}`);if(!O.areEqual(a.dims,n.dims))throw new Error("Inputs 'cos_cache' and 'sin_cache' are expected to have the same shape");if(u>0&&s===0)throw new Error("num_heads must be provided if rotary_embedding_dim is specified");let l=r.dims[0],p=r.dims[r.dims.length-2],h=a.dims[0],f=O.sizeFromDimension(r.dims,1)/p,g=u===0?a.dims[1]*2:f/s;if(u>g)throw new Error("rotary_embedding_dim must be less than or equal to head_size");if(i.dims.length===2){if(l!==i.dims[0])throw new Error(`Input 'position_ids' dimension 0 should be of size batch_size, got ${i.dims[0]}`);if(p!==i.dims[1])throw new Error(`Input 'position_ids' dimension 1 should be of size sequence_length, got ${i.dims[1]}`)}if(g/2!==a.dims[1]&&u/2!==a.dims[1])throw new Error(`Input 'cos_cache' dimension 1 should be same as head_size / 2 or rotary_embedding_dim / 2, got ${a.dims[1]}`);if(p>h)throw new Error("Updating cos_cache and sin_cache in RotaryEmbedding is not currently supported")},Dr=(e,t)=>{let{interleaved:r,numHeads:i,rotaryEmbeddingDim:a,scale:n}=t,s=e[0].dims[0],u=O.sizeFromDimension(e[0].dims,1),l=e[0].dims[e[0].dims.length-2],p=u/l,h=e[2].dims[1],f=a===0?h*2:p/i,g=new Array(s,l,p/f,f-h),y=O.computeStrides(g),_=[{type:1,data:n},{type:12,data:g},{type:12,data:y},...e[0].dims.length===3?new Array({type:12,data:[u,p,f,1]}):[],...e[0].dims.length===4?new Array({type:12,data:[u,f,l*f,1]}):[],...Y(e[0].dims,e[1].dims,e[2].dims,e[3].dims,e[0].dims)],w=S=>{let x=M("input",e[0].dataType,e[0].dims.length),b=M("position_ids",e[1].dataType,e[1].dims.length),I=M("cos_cache",e[2].dataType,e[2].dims.length),k=M("sin_cache",e[3].dataType,e[3].dims.length),E=Q("output",e[0].dataType,e[0].dims.length);return S.registerUniforms([{name:"scale",type:"f32"},{name:"global_shape",type:"u32",length:g.length},{name:"global_strides",type:"u32",length:y.length},{name:"input_output_strides",type:"u32",length:y.length}]),`
        ${S.declareVariables(x,b,I,k,E)}

        ${S.mainStart(Wt)}
          let half_rotary_emb_dim = uniforms.${I.name}_shape[1];
          let bsnh = global_idx / uniforms.global_strides % uniforms.global_shape;
          let size = uniforms.global_shape[0] * uniforms.global_strides[0];
          ${S.guardAgainstOutOfBoundsWorkgroupSizes("size")}

          if (bsnh[3] < half_rotary_emb_dim) {
            let position_ids_idx =
                ${b.broadcastedIndicesToOffset("bsnh.xy",Q("",b.type.tensor,2))};
            let position_id =
                u32(${b.getByOffset("position_ids_idx")}) + select(0, bsnh[1], position_ids_idx == 0);
            let i = dot(bsnh, uniforms.input_output_strides) + select(0, bsnh[3], ${r});
            let j = i + select(half_rotary_emb_dim, 1, ${r});
            let re = ${x.getByOffset("i")} * ${I.get("position_id","bsnh[3]")} -
                ${x.getByOffset("j")} * ${k.get("position_id","bsnh[3]")};
            ${E.setByOffset("i","re")}
            let im = ${x.getByOffset("i")} * ${k.get("position_id","bsnh[3]")} +
                ${x.getByOffset("j")} * ${I.get("position_id","bsnh[3]")};
            ${E.setByOffset("j","im")}
          } else {
            let k = dot(bsnh, uniforms.input_output_strides) + half_rotary_emb_dim;
            ${E.setByOffset("k",x.getByOffset("k"))}
          }
        }`};return{name:"RotaryEmbedding",shaderCache:{hint:he({interleaved:r}).cacheKey,inputDependencies:["rank","rank","rank","rank"]},getShaderSource:w,getRunData:()=>({outputs:[{dims:e[0].dims,dataType:e[0].dataType}],dispatchGroup:{x:Math.ceil(O.size(g)/Wt)},programUniforms:_})}},Sd=(e,t)=>{xd(e.inputs,t),e.compute(Dr(e.inputs,t))}}),kd,Id,ya,Ed,zd,zm=q(()=>{xe(),te(),Fi(),md(),vd(),dt(),Td(),ae(),kd=(e,t)=>{if(t.doRotary&&e.length<=7)throw new Error("cos_cache and sin_cache inputs are required if do_rotary is specified");let r=e[0],i=e[1],a=e[2],n=e[3],s=e[4];if(t.doRotary!==0&&e.length<=7)throw new Error("cos_cast and sin_cache are expected if do_rotary attribute is non-zero");if(t.localWindowSize!==-1)throw new Error("Local attention is not supported");if(t.softcap!==0)throw new Error("Softcap is not supported");if(t.rotaryInterleaved!==0)throw new Error("Rotary interleaved is not supported");if(t.smoothSoftmax)throw new Error("Smooth softmax is not supported");if(r.dims.length!==3&&r.dims.length!==5)throw new Error("Input query is expected to have 3 or 5 dimensions");let u=!1,l=r.dims[0],p=r.dims[1],h=r.dims.length===3?u?r.dims[2]/3:r.dims[2]:t.numHeads*r.dims[4],f=p,g=0,y=!i||i.dims.length===0,_=Math.floor(y?h/(t.numHeads+2*t.kvNumHeads):h/t.numHeads);y&&(h=_*t.numHeads);let w=n&&n.dims.length!==0,S=s&&s.dims.length!==0;if(w&&n.dims.length===4&&n.dims[0]===l&&n.dims[1]!==t.kvNumHeads&&n.dims[2]===t.kvNumHeads&&n.dims[3]===_)throw new Error("BSNH pastKey/pastValue is not supported");if(w&&S){if(n.dims.length!==4)throw new Error('Input "past_key" is expected to have 4 dimensions');if(s.dims.length!==4)throw new Error('Input "past_value" is expected to have 4 dimensions');g=n.dims[2]}else if(w||S)throw new Error('Input "past_key" and "past_value" shall be both present or both absent');let x=1;if(i&&i.dims.length>0){if(r.dims.length!==3)throw new Error('Input "query" is expected to have 3 dimensions when key is given');if(i.dims.length<3||i.dims.length>5)throw new Error('Input "key" is expected to have 3, 4, or 5 dimensions');if(r.dims[0]!==i.dims[0])throw new Error('Input "query" and "key" shall have same dim 0 (batch size)');if(i.dims.length===3){if(r.dims[2]%i.dims[2]!==0)throw new Error('Dimension 2 of "query" should be a multiple of "key"');f=i.dims[1]}else if(i.dims.length===5){if(i.dims[2]!==t.numHeads||i.dims[3]!==2||i.dims[4]!==_)throw new Error('Expect "key" shape (batch_size, kv_sequence_length, num_heads, 2, head_size) for packed kv');if(a)throw new Error('Expect "value" be none when "key" has packed kv format.');f=i.dims[1]}else{if(i.dims[1]!==t.numHeads||i.dims[3]!==_)throw new Error('Expect "key" shape (batch_size, num_heads, kv_sequence_length, head_size) for past_key');f=i.dims[2]}}else{if(r.dims.length!==3&&r.dims.length!==5)throw new Error('Input "query" is expected to have 3 or 5 dimensions when key is empty');if(r.dims.length===5&&(r.dims[2]!==t.numHeads||r.dims[3]!==3))throw new Error('Expect "query" shape (batch_size, kv_sequence_length, num_heads, 3, head_size) for packed kv');x=3}let b=0,I=!1,k=t.kvNumHeads?_*t.kvNumHeads:h;if(a&&a.dims.length>0){if(a.dims.length!==3&&a.dims.length!==4)throw new Error('Input "value" is expected to have 3 or 4 dimensions');if(r.dims[0]!==a.dims[0])throw new Error('Input "query" and "value" shall have same dim 0 (batch_size)');if(a.dims.length===3){if(f!==a.dims[1])throw new Error('Input "key" and "value" shall have the same dim 1 (kv_sequence_length)');k=a.dims[2]}else{if(f!==a.dims[2])throw new Error('Input "past_key" and "past_value" shall have the same dim 2 (kv_sequence_length)');k=a.dims[1]*a.dims[3],I=!0}}let E=e.length>4?e[5]:void 0;if(E&&E.dims.length!==1&&E.dims[0]!==l)throw new Error('Input "seqlens" is expected to have 1 dimension and the same dim 0 as batch_size');return{batchSize:l,sequenceLength:p,pastSequenceLength:g,kvSequenceLength:f,totalSequenceLength:-1,maxSequenceLength:-1,inputHiddenSize:0,hiddenSize:h,vHiddenSize:k,headSize:_,vHeadSize:Math.floor(k/t.kvNumHeads),numHeads:t.numHeads,kvNumHeads:t.kvNumHeads,nReps:t.numHeads/t.kvNumHeads,pastPresentShareBuffer:!1,maskType:b,scale:t.scale,broadcastResPosBias:!1,passPastInKv:I,qkvFormat:x}},Id=he({perm:[0,2,1,3]}),ya=(e,t,r)=>{let i=t,a=r.kvNumHeads;return t.dims.length===3&&r.kvSequenceLength!==0&&(i=t.reshape([r.batchSize,r.kvSequenceLength,a,r.headSize]),i=e.compute(Ne(i,Id.perm),{inputs:[i],outputs:[-1]})[0]),i},Ed=(e,t,r,i)=>{let a=7,n=["type","type"],s=[e*t],u=e*t,l=[{type:12,data:u},{type:12,data:t},{type:12,data:e}],p=h=>{let f=M("seq_lens",r.dataType,r.dims),g=M("total_seq_lens",i.dataType,i.dims),y=Q("pos_ids",a,s),_=[{name:"output_size",type:"u32"},{name:"sequence_length",type:"u32"},{name:"batch_size",type:"u32"}];return`
  ${h.registerUniforms(_).declareVariables(f,g,y)}
  ${h.mainStart()}
    ${h.guardAgainstOutOfBoundsWorkgroupSizes("uniforms.output_size")}
    let total_sequence_length = u32(${g.getByOffset("0")});
    let is_subsequent_prompt = uniforms.sequence_length > 1 && uniforms.sequence_length != total_sequence_length;
    let is_first_prompt = !is_subsequent_prompt && uniforms.sequence_length == total_sequence_length;
    let batch_idx = global_idx / uniforms.sequence_length;
    let sequence_idx = i32(global_idx % uniforms.sequence_length);
    var pos_id: i32 = 0;
    let seqlen = ${f.getByOffset("batch_idx")};
    let total_seqlen = seqlen + 1;
    if (is_first_prompt) {
      if (sequence_idx < total_seqlen) {
        pos_id = sequence_idx;
      } else {
        pos_id = 1;
      }
      ${y.setByOffset("global_idx","pos_id")}
    } else if (is_subsequent_prompt) {
      let past_seqlen = total_seqlen - i32(uniforms.sequence_length);
      if (past_seqlen + sequence_idx < total_seqlen) {
        pos_id = past_seqlen + sequence_idx;
      } else {
        pos_id = 1;
      }
      ${y.setByOffset("global_idx","pos_id")}
    } else if (global_idx < uniforms.batch_size) {
      ${y.setByOffset("global_idx","seqlen")}
    };
  }
  `};return{name:"GeneratePositionIds",shaderCache:{hint:`${e};${t}`,inputDependencies:n},getRunData:()=>({outputs:[{dims:s,dataType:a}],dispatchGroup:{x:Math.ceil(u/64)},programUniforms:l}),getShaderSource:p}},zd=(e,t)=>{var k;let r=kd(e.inputs,t);if(e.inputs[0].dims.length===5)throw new Error("Packed QKV is not implemented");if(((k=e.inputs[1])==null?void 0:k.dims.length)===5)throw new Error("Packed KV is not implemented");let i=e.inputs[0],a=e.inputs[1]&&e.inputs[1].dims.length>0?e.inputs[1]:void 0,n=e.inputs[2]&&e.inputs[2].dims.length>0?e.inputs[2]:void 0,s=e.inputs[3]&&e.inputs[3].dims.length!==0?e.inputs[3]:void 0,u=e.inputs[4]&&e.inputs[4].dims.length!==0?e.inputs[4]:void 0,l=e.inputs.length>4?e.inputs[5]:void 0,p=e.inputs.length>5?e.inputs[6]:void 0,h=r.kvNumHeads?r.kvNumHeads:r.numHeads,f=he({axis:2,numOutputs:3,splitSizes:[r.numHeads*r.headSize,h*r.headSize,h*r.headSize]}),[g,y,_]=!a&&!n?e.compute(ga([i],f),{inputs:[i],outputs:[-1,-1,-1]}):[i,a,n],w,S;if(t.doRotary){let E=e.compute(Ed(r.batchSize,r.sequenceLength,l,p),{inputs:[l,p],outputs:[-1]})[0],A=e.inputs[7],C=e.inputs[8],$=he({interleaved:t.rotaryInterleaved!==0,numHeads:r.numHeads,rotaryEmbeddingDim:0,scale:t.scale}),N=[g,E,A,C],D=[-1];w=e.compute(Dr(N,$),{inputs:N,outputs:D})[0],N.splice(0,1,y);let G=he({interleaved:t.rotaryInterleaved!==0,numHeads:r.kvNumHeads,rotaryEmbeddingDim:0,scale:t.scale});S=e.compute(Dr(N,G),{inputs:N,outputs:D})[0]}let x=nr(e,r.batchSize,r.numHeads,r.sequenceLength,r.headSize,t.doRotary?w:g,void 0,0),b=ya(e,t.doRotary?S:y,r),I=ya(e,_,r);er(e,x,b,I,void 0,void 0,s,u,void 0,r,l,p)}}),_a,Cd,Ad,Od,Cm=q(()=>{te(),re(),dt(),ae(),_a=(e,t,r,i,a,n,s,u)=>{let l=ve(n),p=l===1?"f32":`vec${l}f`,h=l===1?"vec2f":`mat2x${l}f`,f=a*s,g=64;f===1&&(g=256);let y=[a,s,n/l],_=[a,s,2],w=["rank","type","type"],S=[];S.push(...Y(y,_));let x=b=>{let I=M("x",t.dataType,3,l),k=M("scale",r.dataType,r.dims),E=M("bias",i.dataType,i.dims),A=Q("output",1,3,2),C=[I,k,E,A];return`
  var<workgroup> workgroup_shared : array<${h}, ${g}>;
  const workgroup_size = ${g}u;
  ${b.declareVariables(...C)}
  ${b.mainStart(g)}
    let batch = workgroup_index / uniforms.x_shape[1];
    let channel = workgroup_index % uniforms.x_shape[1];
    let hight = uniforms.x_shape[2];
    // initialize workgroup memory
    var sum = ${p}(0);
    var squared_sum = ${p}(0);
    for (var h = local_idx; h < hight; h += workgroup_size) {
      let value = ${p}(${I.get("batch","channel","h")});
      sum += value;
      squared_sum += value * value;
    }
    workgroup_shared[local_idx] = ${h}(sum, squared_sum);
    workgroupBarrier();

    for (var currSize = workgroup_size >> 1;  currSize > 0; currSize = currSize >> 1) {
      if (local_idx < currSize) {
        workgroup_shared[local_idx] = workgroup_shared[local_idx] + workgroup_shared[local_idx + currSize];
      }
      workgroupBarrier();
    }
    if (local_idx == 0) {
      let sum_final = ${lt("workgroup_shared[0][0]",l)} / f32(hight * ${l});
      let squared_sum_final = ${lt("workgroup_shared[0][1]",l)} / f32(hight * ${l});

      let inv_std_dev = inverseSqrt(squared_sum_final - sum_final * sum_final + f32(${u}));
      let channel_scale = inv_std_dev * f32(scale[channel]);
      let channel_shift = f32(bias[channel]) - sum_final * channel_scale;
      output[workgroup_index] = vec2f(channel_scale, channel_shift);
    }
  }`};return e.compute({name:"InstanceNormComputeChannelScaleShift",shaderCache:{hint:`${l};${u};${g}`,inputDependencies:w},getRunData:()=>({outputs:[{dims:_,dataType:1}],dispatchGroup:{x:f},programUniforms:S}),getShaderSource:x},{inputs:[t,r,i],outputs:[-1]})[0]},Cd=(e,t,r)=>{let i=t[0].dims,a=i,n=2,s=i[0],u=i[1],l=O.sizeFromDimension(i,n),p=ve(l),h=O.size(a)/p,f=_a(e,t[0],t[1],t[2],s,l,u,r.epsilon),g=[s,u,l/p],y=[s,u],_=["type","none"],w=S=>{let x=M("x",t[0].dataType,g.length,p),b=M("scale_shift",1,y.length,2),I=Q("output",t[0].dataType,g.length,p),k=[x,b,I];return`
  ${S.registerUniform("output_size","u32").declareVariables(...k)}
  ${S.mainStart()}
  ${S.guardAgainstOutOfBoundsWorkgroupSizes("uniforms.output_size")}
      let outputIndices = ${I.offsetToIndices("global_idx")};
      let batch = outputIndices[0];
      let channel = outputIndices[1];
      let scale_shift = ${b.getByIndices("vec2<u32>(batch, channel)")};
      let value = ${x.getByOffset("global_idx")} * ${I.type.value}(scale_shift.x) + ${I.type.value}(scale_shift.y);
      ${I.setByOffset("global_idx","value")};
  }`};e.compute({name:"InstanceNormalization",shaderCache:{hint:`${p}`,inputDependencies:_},getRunData:()=>({outputs:[{dims:a,dataType:t[0].dataType}],dispatchGroup:{x:Math.ceil(h/64)},programUniforms:[{type:12,data:h},...Y(g,y,g)]}),getShaderSource:w},{inputs:[t[0],f]})},Ad=(e,t,r)=>{let i=t[0].dims,a=i,n=i[0],s=i[i.length-1],u=O.sizeFromDimension(i,1)/s,l=ve(s),p=O.size(a)/l,h=[{type:12,data:u},{type:12,data:Math.floor(s/l)}],f=["type","type"],g=!1,y=[0,i.length-1];for(let x=0;x<i.length-2;x++)g=g||i[x+1]!==1,y.push(x+1);g=g&&i[i.length-1]!==1;let _=g?e.compute(Ne(e.inputs[0],y),{inputs:[e.inputs[0]],outputs:[-1]})[0]:e.inputs[0].reshape(Array.from({length:i.length},(x,b)=>i[y[b]])),w=_a(e,_,t[1],t[2],n,u,s,r.epsilon),S=x=>{let b=Te(t[0].dataType),I=l===1?"vec2f":`mat${l}x2f`,k=C=>{let $=C===0?"x":"y",N=l===1?"f32":`vec${l}f`;switch(l){case 1:return`${b}(${N}(scale.${$}))`;case 2:return`vec2<${b}>(${N}(scale[0].${$}, scale[1].${$}))`;case 4:return`vec4<${b}>(${N}(scale[0].${$}, scale[1].${$}, scale[2].${$}, scale[3].${$}))`;default:throw new Error(`Not supported compoents ${l}`)}},E=M("input",t[0].dataType,t[0].dims,l),A=Q("output",t[0].dataType,a,l);return`
  @group(0) @binding(0) var<storage, read> input : array<${E.type.storage}>;
  @group(0) @binding(1) var<storage, read> scale_input : array<${I}>;
  @group(0) @binding(2) var<storage, read_write> output : array<${A.type.storage}>;
  struct Uniforms {H: u32, C : u32};
  @group(0) @binding(3) var<uniform> uniforms: Uniforms;

  ${x.mainStart()}
    let current_image_number = global_idx / (uniforms.C * uniforms.H);
    let current_channel_number = global_idx % uniforms.C;

    let scale_offset = current_image_number * uniforms.C + current_channel_number;
    let scale = scale_input[scale_offset];
    output[global_idx] = fma(input[global_idx], ${k(0)}, ${k(1)});
  }`};e.compute({name:"InstanceNormalizationNHWC",shaderCache:{hint:`${l}`,inputDependencies:f},getRunData:()=>({outputs:[{dims:a,dataType:t[0].dataType}],dispatchGroup:{x:Math.ceil(p/64)},programUniforms:h}),getShaderSource:S},{inputs:[t[0],w]})},Od=(e,t)=>{t.format==="NHWC"?Ad(e,e.inputs,t):Cd(e,e.inputs,t)}}),Rd,Bd,Md,Am=q(()=>{te(),re(),ae(),Rd=e=>{if(!e||e.length<2)throw new Error("layerNorm requires at least 2 inputs.")},Bd=(e,t,r)=>{let i=t.simplified,a=e[0].dims,n=e[1],s=!i&&e[2],u=a,l=O.normalizeAxis(t.axis,a.length),p=O.sizeToDimension(a,l),h=O.sizeFromDimension(a,l),f=O.size(n.dims),g=s?O.size(s.dims):0;if(f!==h||s&&g!==h)throw new Error(`Size of X.shape()[axis:] == ${h}.
       Size of scale and bias (if provided) must match this.
       Got scale size of ${f} and bias size of ${g}`);let y=[];for(let E=0;E<a.length;++E)E<l?y.push(a[E]):y.push(1);let _=ve(h),w=["type","type"],S=[{type:12,data:p},{type:1,data:h},{type:12,data:Math.floor(h/_)},{type:1,data:t.epsilon}];s&&w.push("type");let x=r>1,b=r>2,I=E=>{let A=Te(e[0].dataType),C=[M("x",e[0].dataType,e[0].dims,_),M("scale",n.dataType,n.dims,_)];s&&C.push(M("bias",s.dataType,s.dims,_)),C.push(Q("output",e[0].dataType,u,_)),x&&C.push(Q("mean_data_output",1,y)),b&&C.push(Q("inv_std_output",1,y));let $=[{name:"norm_count",type:"u32"},{name:"norm_size",type:"f32"},{name:"norm_size_vectorized",type:"u32"},{name:"epsilon",type:"f32"}];return`
  ${E.registerUniforms($).declareVariables(...C)}
  ${E.mainStart()}
    ${E.guardAgainstOutOfBoundsWorkgroupSizes("uniforms.norm_count")}
    let offset = global_idx * uniforms.norm_size_vectorized;
    var mean_vector = ${Pi("f32",_)};
    var mean_square_vector = ${Pi("f32",_)};

    for (var h: u32 = 0u; h < uniforms.norm_size_vectorized; h++) {
      let value = ${Vt(A,_,"x[h + offset]")};
      mean_vector += value;
      mean_square_vector += value * value;
    }
    let mean = ${lt("mean_vector",_)} / uniforms.norm_size;
    let inv_std_dev = inverseSqrt(${lt("mean_square_vector",_)} / uniforms.norm_size ${i?"":"- mean * mean"} + uniforms.epsilon);

    for (var j: u32 = 0; j < uniforms.norm_size_vectorized; j++) {
      let f32input = ${Vt(A,_,"x[j + offset]")};
      let f32scale = ${Vt(A,_,"scale[j]")};
      output[j + offset] = ${C[0].type.value}((f32input ${i?"":"- mean"}) * inv_std_dev * f32scale
        ${s?`+ ${Vt(A,_,"bias[j]")}`:""}
      );
    }

    ${x?"mean_data_output[global_idx] = mean":""};
    ${b?"inv_std_output[global_idx] = inv_std_dev":""};
  }`},k=[{dims:u,dataType:e[0].dataType}];return x&&k.push({dims:y,dataType:1}),b&&k.push({dims:y,dataType:1}),{name:"LayerNormalization",shaderCache:{hint:`${_};${r};${i}`,inputDependencies:w},getRunData:()=>({outputs:k,dispatchGroup:{x:Math.ceil(p/64)},programUniforms:S}),getShaderSource:I}},Md=(e,t)=>{Rd(e.inputs),e.compute(Bd(e.inputs,t,e.outputCount))}}),Nd,Dd,Om=q(()=>{re(),ea(),aa(),Nd=e=>{if(!e||e.length!==2)throw new Error("MatMul requires 2 inputs.");if(e[0].dims[e[0].dims.length-1]!==e[1].dims[e[1].dims.length-2])throw new Error("shared dimension does not match.")},Dd=e=>{Nd(e.inputs);let t=Lt.calcShape(e.inputs[0].dims,e.inputs[1].dims,!0);if(!t)throw new Error("Can't use matmul on the given tensors");let r=t[t.length-1],i=e.inputs[0].dims[e.inputs[0].dims.length-1];if(r<8&&i<8)e.compute(Ji(e.inputs,{activation:""},t));else{let a=t[t.length-2],n=O.size(e.inputs[0].dims.slice(0,-2)),s=O.size(e.inputs[1].dims.slice(0,-2));if(n!==1&&a===1&&s===1){let u=e.inputs[0].reshape([1,n,i]),l=e.inputs[1].reshape([1,i,r]),p=[1,n,r],h=[u,l];e.compute(Rr(h,{activation:""},t,p),{inputs:h})}else e.compute(Rr(e.inputs,{activation:""},t))}}}),Ud,Pd,qd,Ld,Wd,Rm=q(()=>{te(),re(),xe(),ae(),Ud=(e,t)=>{if(e.length<3||e.length>4)throw new Error("MatMulNBits requires 3 or 4 inputs");let r=e[0],i=r.dims.length;if(r.dims[i-1]!==t.k)throw new Error("The last dim of input shape does not match the k value");let a=Math.floor((t.k+t.blockSize-1)/t.blockSize),n=t.blockSize/8*t.bits,s=e[1];if(!O.areEqual(s.dims,[t.n,a,n]))throw new Error("The second inputs must be 3D tensor with shape N X nBlocksPerCol X blobSize");let u=e[2].dims;if(O.size(u)!==t.n*a)throw new Error("scales input size error.");if(e.length===4){let l=e[3].dims,p=t.n*(t.bits===8?a:Math.floor((a*t.bits+7)/8));if(O.size(l)!==p)throw new Error("zeroPoints input size error.")}},Pd=(e,t)=>{let r=e[0].dims,i=r.length,a=r[i-2],n=t.k,s=t.n,u=r.slice(0,i-2),l=O.size(u),p=e[1].dims[2]/4,h=e[0].dataType,f=ve(t.k),g=ve(p),y=ve(s),_=u.concat([a,s]),w=a>1&&s/y%2===0?2:1,S=O.size(_)/y/w,x=64,b=[],I=[l,a,n/f],k=O.convertShape(e[1].dims).slice();k.splice(-1,1,p/g),b.push(...Y(I)),b.push(...Y(k)),b.push(...Y(e[2].dims)),e.length===4&&b.push(...Y(O.convertShape(e[3].dims)));let E=[l,a,s/y];b.push(...Y(E));let A=C=>{let $=I.length,N=M("a",e[0].dataType,$,f),D=M("b",12,k.length,g),G=M("scales",e[2].dataType,e[2].dims.length),V=[N,D,G],j=e.length===4?M("zero_points",12,e[3].dims.length):void 0;j&&V.push(j);let R=E.length,K=Q("output",e[0].dataType,R,y),F=Te(e[0].dataType),X=(()=>{switch(f){case 1:return`array<${F}, 8>`;case 2:return`mat4x2<${F}>`;case 4:return`mat2x4<${F}>`;default:throw new Error(`${f}-component is not supported.`)}})(),le=()=>{let U=`
          // reuse a data
            var input_offset = ${N.indicesToOffset(`${N.type.indices}(batch, row, word_offset)`)};
            var a_data: ${X};
            for (var j: u32 = 0; j < ${8/f}; j++) {
              a_data[j] = ${N.getByOffset("input_offset")};
              input_offset++;
            }
          `;for(let P=0;P<y*w;P++)U+=`
            b_value = ${g===1?`b${P}_data`:`b${P}_data[i]`};
            b_value_lower = unpack4xU8(b_value & b_mask);
            b_value_upper = unpack4xU8((b_value >> 4) & b_mask);
            b_quantized_values = ${X}(${Array.from({length:4},(J,ee)=>`${F}(b_value_lower[${ee}]), ${F}(b_value_upper[${ee}])`).join(", ")});
            b_dequantized_values = ${f===1?`${X}(${Array.from({length:8},(J,ee)=>`(b_quantized_values[${ee}] - ${j?`zero_point${P}`:"zero_point"}) * scale${P}`).join(", ")});`:`(b_quantized_values - ${X}(${Array(8).fill(`${j?`zero_point${P}`:"zero_point"}`).join(",")})) * scale${P};`};
            workgroup_shared[local_id.x * ${w} + ${Math.floor(P/y)}]${y>1?`[${P%y}]`:""} += ${Array.from({length:8/f},(J,ee)=>`${f===1?`a_data[${ee}] * b_dequantized_values[${ee}]`:`dot(a_data[${ee}], b_dequantized_values[${ee}])`}`).join(" + ")};
          `;return U},L=()=>{let U=`
            var col_index = col * ${y};
            ${j?`
            let zero_point_bytes_per_col = (nBlocksPerCol + 1) / 2;
            var zero_point_byte_count: u32;
            var zero_point_word_index: u32;
            var zero_point_byte_offset: u32;
            let zero_point_nibble_offset: u32 = block & 0x1u;
            var zero_point_bits_offset: u32;
            var zero_point_word: u32;`:`
            // The default zero point is 8 for unsigned 4-bit quantization.
            let zero_point = ${F}(8);`}
            `;for(let P=0;P<y*w;P++)U+=`
            let scale${P} = ${G.getByOffset("col_index * nBlocksPerCol + block")};
            ${j?`
            zero_point_byte_count = col_index * zero_point_bytes_per_col + (block >> 0x1u);
            zero_point_word_index = zero_point_byte_count >> 0x2u;
            zero_point_byte_offset = zero_point_byte_count & 0x3u;
            zero_point_bits_offset = (zero_point_byte_offset << 3) + (zero_point_nibble_offset << 2);
            zero_point_word = ${j.getByOffset("zero_point_word_index")} >> zero_point_bits_offset;
            let zero_point${P} = ${F}((zero_point_word) & 0xFu);`:""}
            col_index += 1;`;return U},me=()=>{let U=`col_index = col * ${y};`;for(let P=0;P<y*w;P++)U+=`
            let b${P}_data = ${D.getByIndices(`${D.type.indices}(col_index, block, word)`)};
            col_index += 1;`;return U+=`
            var b_value: u32;
            let b_mask: u32 = 0x0F0F0F0Fu;
            var b_value_lower: vec4<u32>;
            var b_value_upper: vec4<u32>;
            var b_quantized_values: ${X};
            var b_dequantized_values: ${X};`,U};return`
        var<workgroup> workgroup_shared: array<${K.type.value}, ${w*x}>;
        ${C.declareVariables(...V,K)}
        ${C.mainStart([x,1,1])}
          let output_indices = ${K.offsetToIndices(`(global_idx / ${x}) * ${w}`)};
          let col = output_indices[2];
          let row = output_indices[1];
          let batch = output_indices[0];
          let nBlocksPerCol = uniforms.b_shape[1];

          for (var block = local_id.x; block < nBlocksPerCol; block += ${x}) {
            //process one block
            var word_offset: u32 = block * ${t.blockSize/f};
            ${L()}
            for (var word: u32 = 0; word < ${p}; word += ${g}) {
              ${me()}
              for (var i: u32 = 0; i < ${g}; i++) {
                ${le()}
                word_offset += ${8/f};
              }
            }
          }
          workgroupBarrier();

          if (local_id.x < ${w}) {
            var output_value: ${K.type.value} = ${K.type.value}(0);
            var workgroup_shared_offset: u32 = local_id.x;
            for (var b: u32 = 0u; b < ${x}u; b++) {
              output_value += workgroup_shared[workgroup_shared_offset];
              workgroup_shared_offset += ${w};
            }
            ${K.setByIndices(`${K.type.indices}(batch, row, col + local_id.x)`,"output_value")};
          }
        }`};return{name:"MatMulNBits",shaderCache:{hint:`${t.blockSize};${t.bits};${f};${g};${y};${w};${x}`,inputDependencies:Array(e.length).fill("rank")},getRunData:()=>({outputs:[{dims:_,dataType:h}],dispatchGroup:{x:S},programUniforms:b}),getShaderSource:A}},qd=(e,t)=>{let r=e[0].dims,i=r.length,a=r[i-2],n=t.k,s=t.n,u=r.slice(0,i-2),l=O.size(u),p=e[1].dims[2]/4,h=e[0].dataType,f=ve(t.k),g=ve(p),y=u.concat([a,s]),_=128,w=s%8===0?8:s%4===0?4:1,S=_/w,x=S*g*8,b=x/f,I=x/t.blockSize,k=O.size(y)/w,E=[],A=[l,a,n/f],C=O.convertShape(e[1].dims).slice();C.splice(-1,1,p/g),E.push(...Y(A)),E.push(...Y(C)),E.push(...Y(e[2].dims)),e.length===4&&E.push(...Y(O.convertShape(e[3].dims)));let $=[l,a,s];E.push(...Y($));let N=D=>{let G=A.length,V=M("a",e[0].dataType,G,f),j=M("b",12,C.length,g),R=M("scales",e[2].dataType,e[2].dims.length),K=[V,j,R],F=e.length===4?M("zero_points",12,e[3].dims.length):void 0;F&&K.push(F);let X=$.length,le=Q("output",e[0].dataType,X),L=Te(e[0].dataType),me=()=>{switch(f){case 1:return`
          let a_data0 = vec4<${L}>(sub_a[word_offset], sub_a[word_offset + 1], sub_a[word_offset + 2], sub_a[word_offset + 3]);
          let a_data1 = vec4<${L}>(sub_a[word_offset + 4], sub_a[word_offset + 5], sub_a[word_offset + 6], sub_a[word_offset + 7]);`;case 2:return`
          let a_data0 = vec4<${L}>(sub_a[word_offset], sub_a[word_offset + 1]);
          let a_data1 = vec4<${L}>(sub_a[word_offset + 2], sub_a[word_offset + 3]);`;case 4:return`
          let a_data0 = sub_a[word_offset];
          let a_data1 = sub_a[word_offset + 1];`;default:throw new Error(`${f}-component is not supported.`)}};return`
        var<workgroup> sub_a: array<${V.type.value}, ${b}>;
        var<workgroup> inter_results: array<array<${le.type.value}, ${S}>, ${w}>;
        ${D.declareVariables(...K,le)}
        ${D.mainStart([S,w,1])}
          let output_indices = ${le.offsetToIndices(`workgroup_index * ${w}`)};
          let col = output_indices[2];
          let row = output_indices[1];
          let batch = output_indices[0];
          let n_blocks_per_col = uniforms.b_shape[1];
          let num_tiles =  (n_blocks_per_col - 1) / ${I} + 1;

          // Loop over shared dimension.
          for (var tile: u32 = 0; tile < num_tiles; tile += 1) {
            let a_col_start = tile * ${b};
            // load one tile A data into shared memory.
            for (var a_offset = local_idx; a_offset < ${b}; a_offset += ${_})
            {
              let a_col = a_col_start + a_offset;
              if (a_col < uniforms.a_shape[2])
              {
                sub_a[a_offset] = ${V.getByIndices(`${V.type.indices}(batch, row, a_col)`)};
              } else {
                sub_a[a_offset] = ${V.type.value}(0);
              }
            }
            workgroupBarrier();

            // each thread process one block
            let b_row = col + local_id.y;
            let block = tile * ${I} + local_id.x;
            ${F?`
            let zero_point_bytes_per_col = (n_blocks_per_col + 1) / 2;
            let zero_point_byte_count = b_row * zero_point_bytes_per_col + (block >> 0x1u);
            let zero_point_word_index = zero_point_byte_count >> 0x2u;
            let zero_point_byte_offset = zero_point_byte_count & 0x3u;
            let zero_point_nibble_offset: u32 = block & 0x1u;
            let zero_point_bits_offset = (zero_point_byte_offset << 3) + (zero_point_nibble_offset << 2);
            let zero_point_word = ${F.getByOffset("zero_point_word_index")} >> zero_point_bits_offset;
            let zero_point = ${L}((zero_point_word) & 0xFu);`:`
            // The default zero point is 8 for unsigned 4-bit quantization.
            let zero_point = ${L}(8);`}
            let scale = ${R.getByOffset("b_row * n_blocks_per_col + block")};
            let b_data = ${j.getByIndices(`${j.type.indices}(b_row, block, 0)`)};
            var word_offset = local_id.x * ${t.blockSize/f};
            for (var i: u32 = 0; i < ${g}; i++) {
              ${me()}
              let b_value = ${g===1?"b_data":"b_data[i]"};
              let b_value_lower = unpack4xU8(b_value & 0x0F0F0F0Fu);
              let b_value_upper = unpack4xU8((b_value >> 4) & 0x0F0F0F0Fu);
              let b_quantized_values = mat2x4<${L}>(${Array.from({length:4},(U,P)=>`${L}(b_value_lower[${P}]), ${L}(b_value_upper[${P}])`).join(", ")});
              let b_dequantized_values = (b_quantized_values - mat2x4<${L}>(${Array(8).fill("zero_point").join(",")})) * scale;
              inter_results[local_id.y][local_id.x] += ${Array.from({length:2},(U,P)=>`${`dot(a_data${P}, b_dequantized_values[${P}])`}`).join(" + ")};
              word_offset += ${8/f};
            }
            workgroupBarrier();
          }

          if (local_idx < ${w}) {
            var output_value: ${le.type.value} = ${le.type.value}(0);
            for (var b = 0u; b < ${S}; b++) {
              output_value += inter_results[local_idx][b];
            }
            if (col + local_idx < uniforms.output_shape[2])
            {
              ${le.setByIndices(`${le.type.indices}(batch, row, col + local_idx)`,"output_value")}
            }
          }
        }`};return{name:"BlockwiseMatMulNBits32",shaderCache:{hint:`${t.blockSize};${f};${g};${S};${w}`,inputDependencies:Array(e.length).fill("rank")},getRunData:()=>({outputs:[{dims:y,dataType:h}],dispatchGroup:{x:k},programUniforms:E}),getShaderSource:N}},Ld=(e,t)=>{Ud(e.inputs,t),t.blockSize===32&&e.adapterInfo.isVendor("intel")&&e.adapterInfo.isArchitecture("gen-12lp")?e.compute(qd(e.inputs,t)):e.compute(Pd(e.inputs,t))},Wd=e=>he(e)}),Vd,Gd,Hd,Fd,jd,Kd,Qd,Zd,Yd,Bm=q(()=>{te(),re(),ae(),Vd=e=>{if(!e||e.length<1)throw new Error("Too few inputs");if(e[0].dataType!==1&&e[0].dataType!==10)throw new Error("Input type must be float or float16.");if(e.length>=2){let t=e[0].dims.length*2===e[1].dims[0];if(e.length===4&&(t=e[3].dims[0]*2===e[1].dims[0]),!t)throw new Error("The pads should be a 1D tensor of shape [2 * input_rank] or [2 * num_axes].")}},Gd=(e,t,r)=>{let i="";for(let a=t-1;a>=0;--a)i+=`
            k = i32(${e.indicesGet("indices",a)}) - ${Z("uniforms.pads",a,r)};
            if (k < 0) {
              break;
            }
            if (k >= i32(${Z("uniforms.x_shape",a,t)})) {
              break;
            }
            offset += k * i32(${Z("uniforms.x_strides",a,t)});
        `;return`
          value = ${e.type.value}(uniforms.constant_value);
          for (var i = 0; i < 1; i++) {
            var offset = 0;
            var k = 0;
            ${i}
            value = x[offset];
          }
      `},Hd=(e,t,r)=>{let i="";for(let a=t-1;a>=0;--a)i+=`
                k = i32(${e.indicesGet("indices",a)}) - ${Z("uniforms.pads",a,r)};
                if (k < 0) {
                  k = -k;
                }
                {
                  let _2n_1 = 2 * (i32(${Z("uniforms.x_shape",a,t)}) - 1);
                  k = k % _2n_1;
                  if(k >= i32(${Z("uniforms.x_shape",a,t)})) {
                    k = _2n_1 - k;
                  }
                }
                offset += k * i32(${Z("uniforms.x_strides",a,t)});
            `;return`
              var offset = 0;
              var k = 0;
              ${i}
              value = x[offset];
          `},Fd=(e,t,r)=>{let i="";for(let a=t-1;a>=0;--a)i+=`
                k = i32(${e.indicesGet("indices",a)}) - ${Z("uniforms.pads",a,r)};
                if (k < 0) {
                  k = 0;
                }
                if (k >= i32(${Z("uniforms.x_shape",a,t)})) {
                  k = i32(${Z("uniforms.x_shape",a,t)}) - 1;
                }
                offset += k * i32(${Z("uniforms.x_strides",a,t)});
            `;return`
              var offset = 0;
              var k = 0;
              ${i}
              value = x[offset];
          `},jd=(e,t,r)=>{let i="";for(let a=t-1;a>=0;--a)i+=`
                k = i32(${e.indicesGet("indices",a)}) - ${Z("uniforms.pads",a,r)};
                if (k < 0)  {
                  k += i32(${Z("uniforms.x_shape",a,t)}]);
                }
                if (k >= i32(${Z("uniforms.x_shape",a,t)})) {
                  k -= i32(${Z("uniforms.x_shape",a,t)});
                }
                offset += k * i32(${Z("uniforms.x_strides",a,t)});
            `;return`
              var offset = 0;
              var k = 0;
              ${i}
              value = x[offset];
          `},Kd=(e,t,r)=>{switch(r.mode){case 0:return Gd(e,t,r.pads.length);case 1:return Hd(e,t,r.pads.length);case 2:return Fd(e,t,r.pads.length);case 3:return jd(e,t,r.pads.length);default:throw new Error("Invalid mode")}},Qd=(e,t)=>{let r=O.padShape(e[0].dims.slice(),t.pads),i=e[0].dims,a=O.size(r),n=[{type:12,data:a},{type:6,data:t.pads}],s=e.length>=3&&e[2].data;t.mode===0&&n.push({type:s?e[2].dataType:1,data:t.value}),n.push(...Y(e[0].dims,r));let u=["rank"],l=p=>{let h=Q("output",e[0].dataType,r.length),f=M("x",e[0].dataType,i.length),g=f.type.value,y=Kd(h,i.length,t),_=[{name:"output_size",type:"u32"},{name:"pads",type:"i32",length:t.pads.length}];return t.mode===0&&_.push({name:"constant_value",type:s?g:"f32"}),`
            ${p.registerUniforms(_).declareVariables(f,h)}
            ${p.mainStart()}
            ${p.guardAgainstOutOfBoundsWorkgroupSizes("uniforms.output_size")}

            let indices = ${h.offsetToIndices("global_idx")};

            var value = ${g}(0);
            ${y}
            output[global_idx] = value;
        }`};return{name:"Pad",shaderCache:{hint:`${t.mode}${s}`,inputDependencies:u},getRunData:()=>({outputs:[{dims:r,dataType:e[0].dataType}],dispatchGroup:{x:Math.ceil(O.size(r)/64)},programUniforms:n}),getShaderSource:l}},Zd=(e,t)=>{if(e.length>1){let r=e[1].getBigInt64Array(),i=e.length>=3&&e[2].data?e[2].dataType===10?e[2].getUint16Array()[0]:e[2].getFloat32Array()[0]:0,a=e[0].dims.length,n=new Int32Array(2*a).fill(0);if(e.length>=4){let u=e[3].getBigInt64Array();for(let l=0;l<u.length;l++)n[Number(u[l])]=Number(r[l]),n[Number(u[l])+a]=Number(r[l+u.length])}else r.forEach((u,l)=>n[Number(l)]=Number(u));let s=[];return n.forEach(u=>s.push(u)),{mode:t.mode,value:i,pads:s}}else return t},Yd=(e,t)=>{Vd(e.inputs);let r=Zd(e.inputs,t);e.compute(Qd(e.inputs,r),{inputs:[0]})}}),sr,wa,ba,$a,va,Xd,Jd,xa,Sa,ep,tp,Ta,rp,ip,ka,ap,np,sp,op,Mm=q(()=>{Pe(),te(),re(),ae(),sr=e=>{if(ye.webgpu.validateInputContent&&(!e||e.length!==1))throw new Error("Pool ops requires 1 input.")},wa=(e,t,r)=>{let i=t.format==="NHWC",a=e.dims.slice();i&&a.splice(1,0,a.pop());let n=Object.hasOwnProperty.call(t,"dilations"),s=t.kernelShape.slice(),u=t.strides.slice(),l=n?t.dilations.slice():[],p=t.pads.slice();kr.adjustPoolAttributes(r,a,s,u,l,p);let h=kr.computePoolOutputShape(r,a,u,l,s,p,t.autoPad),f=Object.assign({},t);n?Object.assign(f,{kernelShape:s,strides:u,pads:p,dilations:l,cacheKey:t.cacheKey}):Object.assign(f,{kernelShape:s,strides:u,pads:p,cacheKey:t.cacheKey});let g=h.slice();return g.push(g.splice(1,1)[0]),[f,i?g:h]},ba=(e,t)=>{let r=t.format==="NHWC",i=O.size(e),a=O.size(t.kernelShape),n=[{type:12,data:i},{type:12,data:a}],s=[{name:"outputSize",type:"u32"},{name:"kernelSize",type:"u32"}];if(t.kernelShape.length<=2){let u=t.kernelShape[t.kernelShape.length-1],l=t.strides[t.strides.length-1],p=t.pads[t.pads.length/2-1],h=t.pads[t.pads.length-1],f=!!(p+h);n.push({type:12,data:u},{type:12,data:l},{type:12,data:p},{type:12,data:h}),s.push({name:"kw",type:"u32"},{name:"sw",type:"u32"},{name:"pwStart",type:"u32"},{name:"pwEnd",type:"u32"});let g=!1;if(t.kernelShape.length===2){let y=t.kernelShape[t.kernelShape.length-2],_=t.strides[t.strides.length-2],w=t.pads[t.pads.length/2-2],S=t.pads[t.pads.length-2];g=!!(w+S),n.push({type:12,data:y},{type:12,data:_},{type:12,data:w},{type:12,data:S}),s.push({name:"kh",type:"u32"},{name:"sh",type:"u32"},{name:"phStart",type:"u32"},{name:"phEnd",type:"u32"})}return[n,s,!0,f,g]}else{if(r)throw new Error("Pooling with kernelShape.length > 2 is not supported for NHWC format.");let u=O.computeStrides(t.kernelShape);n.push({type:12,data:u},{type:12,data:t.pads},{type:12,data:t.strides}),s.push({name:"kernelStrides",type:"u32",length:u.length},{name:"pads",type:"u32",length:t.pads.length},{name:"strides",type:"u32",length:t.strides.length});let l=t.pads.reduce((p,h)=>p+h);return[n,s,!!l,!1,!1]}},$a=(e,t,r,i,a,n,s,u,l,p,h,f)=>{let g=a.format==="NHWC",y=t.type.value,_=Q("output",t.type.tensor,i);if(a.kernelShape.length<=2){let w="",S="",x="",b=r-(g?2:1);if(h?w=`
                for (var i: u32 = 0u; i < uniforms.kw; i++) {
                  xIndices[${b}] = indices[${b}] * uniforms.sw - uniforms.pwStart + i;
                  if (xIndices[${b}] < 0 || xIndices[${b}]
                      >= uniforms.x_shape[${b}]) {
                    pad++;
                    continue;
                  }
                  let x_val = x[${t.indicesToOffset("xIndices")}];
                  ${n}
                }`:w=`
                for (var i: u32 = 0u; i < uniforms.kw; i++) {
                  xIndices[${b}] = indices[${b}] * uniforms.sw - uniforms.pwStart + i;
                  let x_val = x[${t.indicesToOffset("xIndices")}];
                  ${n}
                }`,a.kernelShape.length===2){let I=r-(g?3:2);f?S=`
                for (var j: u32 = 0u; j < uniforms.kh; j++) {
                  xIndices[${I}] = indices[${I}] * uniforms.sh - uniforms.phStart + j;
                  if (xIndices[${I}] < 0 || xIndices[${I}] >= uniforms.x_shape[${I}]) {
                    pad += i32(uniforms.kw);
                    continue;
                  }
              `:S=`
                for (var j: u32 = 0u; j < uniforms.kh; j++) {
                  xIndices[${I}] = indices[${I}] * uniforms.sh - uniforms.phStart + j;
                `,x=`
              }
            `}return`
            ${e.registerUniforms(l).declareVariables(t,_)}

            ${e.mainStart()}
              ${e.guardAgainstOutOfBoundsWorkgroupSizes("uniforms.outputSize")}

              let indices = ${_.offsetToIndices("global_idx")};
              var xIndices = ${_.offsetToIndices("global_idx")};

              var value = ${y}(${u});
              var pad = 0;
              ${S}
              ${w}
              ${x}
              ${s}

              output[global_idx] = value;
            }`}else{if(g)throw new Error("Pooling with kernelShape.length > 2 is not supported for NHWC format.");let w=a.kernelShape.length,S=a.pads.length,x="";return p?x=`
                if (xIndices[j] >= uniforms.x_shape[j]) {
                  pad++;
                  isPad = true;
                  break;
                }
              }
              if (!isPad) {
                let x_val = x[${t.indicesToOffset("xIndices")}];
                ${n}
              }`:x=`
              }
              let x_val = x[${t.indicesToOffset("xIndices")}];
              ${n}
            `,`
            ${e.registerUniforms(l).declareVariables(t,_)}

            ${e.mainStart()}
              ${e.guardAgainstOutOfBoundsWorkgroupSizes("uniforms.outputSize")}
              let indices = ${_.offsetToIndices("global_idx")};
              var xIndices = ${_.offsetToIndices("global_idx")};

              var offsets: array<u32, ${w}>;

              var value = ${y}(${u});
              var pad = 0;
              var isPad = false;

              for (var i: u32 = 0u; i < uniforms.kernelSize; i++) {
                var offset = i;
                for (var j = 0u; j < ${w-1}u; j++) {
                  offsets[j] = offset / ${Z("uniforms.kernelStrides","j",w)};
                  offset -= offsets[j] * ${Z("uniforms.kernelStrides","j",w)};
                }
                offsets[${w-1}] = offset;

                isPad = false;
                for (var j = ${r-w}u; j < ${r}u; j++) {
                  xIndices[j] = indices[j] * ${Z("uniforms.strides",`j - ${r-w}u`,w)}
                    + offsets[j - ${r-w}u] - ${Z("uniforms.pads","j - 2u",S)};
                  ${x}
              }
              ${s}

              output[global_idx] = value;
            }`}},va=e=>`${e.format};${e.ceilMode};${e.autoPad};${e.kernelShape.length}`,Xd=e=>`${va(e)};${e.countIncludePad}`,Jd=e=>`${va(e)};${e.storageOrder};${e.dilations}`,xa=e=>({format:e.format,autoPad:["NOTSET","VALID","SAME_UPPER","SAME_LOWER"][e.auto_pad],ceilMode:e.ceil_mode,kernelShape:e.kernel_shape,strides:e.strides,pads:e.pads}),Sa=(e,t,r,i)=>{let[a,n]=wa(t,i,r),s=M("x",t.dataType,t.dims.length),u=s.type.value,l="value += x_val;",p="";a.countIncludePad?p+=`value /= ${u}(uniforms.kernelSize);`:p+=`value /= ${u}(i32(uniforms.kernelSize) - pad);`;let[h,f,g,y,_]=ba(n,a);h.push(...Y(t.dims,n));let w=["rank"];return{name:e,shaderCache:{hint:`${i.cacheKey};${g};${y};${_}`,inputDependencies:w},getRunData:()=>({outputs:[{dims:n,dataType:t.dataType}],dispatchGroup:{x:Math.ceil(O.size(n)/64)},programUniforms:h}),getShaderSource:S=>$a(S,s,t.dims.length,n.length,a,l,p,0,f,g,y,_)}},ep=e=>{let t=e.count_include_pad!==0,r=xa(e);if(r.ceilMode!==0)throw new Error("using ceil() in shape computation is not yet supported for AveragePool");let i={countIncludePad:t,...r,cacheKey:""};return{...i,cacheKey:Xd(i)}},tp=(e,t)=>{sr(e.inputs),e.compute(Sa("AveragePool",e.inputs[0],!1,t))},Ta={autoPad:"",ceilMode:0,countIncludePad:!1,kernelShape:[],strides:[],pads:[],storageOrder:0,dilations:[]},rp=e=>{let t=e.format;return{format:t,...Ta,cacheKey:t}},ip=(e,t)=>{sr(e.inputs),e.compute(Sa("GlobalAveragePool",e.inputs[0],!0,t))},ka=(e,t,r,i)=>{let[a,n]=wa(t,i,r),s=`
      value = max(x_val, value);
    `,u="",l=M("x",t.dataType,t.dims.length),p=["rank"],[h,f,g,y,_]=ba(n,a);return h.push(...Y(t.dims,n)),{name:e,shaderCache:{hint:`${i.cacheKey};${g};${y};${_}`,inputDependencies:p},getRunData:()=>({outputs:[{dims:n,dataType:t.dataType}],dispatchGroup:{x:Math.ceil(O.size(n)/64)},programUniforms:h}),getShaderSource:w=>$a(w,l,t.dims.length,n.length,a,s,u,t.dataType===10?-65504:-1e5,f,g,y,_)}},ap=(e,t)=>{sr(e.inputs),e.compute(ka("MaxPool",e.inputs[0],!1,t))},np=e=>{let t=e.storage_order,r=e.dilations,i=xa(e);if(t!==0)throw new Error("column major storage order is not yet supported for MaxPool");if(i.ceilMode!==0)throw new Error("using ceil() in shape computation is not yet supported for MaxPool");let a={storageOrder:t,dilations:r,...i,cacheKey:""};return{...a,cacheKey:Jd(a)}},sp=e=>{let t=e.format;return{format:t,...Ta,cacheKey:t}},op=(e,t)=>{sr(e.inputs),e.compute(ka("GlobalMaxPool",e.inputs[0],!0,t))}}),up,lp,dp,pp,Nm=q(()=>{te(),re(),xe(),ae(),up=(e,t)=>{if(e.length<2||e.length>3)throw new Error("DequantizeLinear requires 2 or 3 inputs.");if(e.length===3&&e[1].dims===e[2].dims)throw new Error("x-scale and x-zero-point must have the same shape.");if(e.length===3&&e[0].dataType!==e[2].dataType)throw new Error("x and x-zero-point must have the same data type.");if(e[0].dataType===6&&e.length>2)throw new Error("In the case of dequantizing int32 there is no zero point.");if(e[1].dims.length!==0&&e[1].dims.length!==1&&e[1].dims.length!==e[0].dims.length)throw new Error("scale input must be a scalar, a 1D tensor, or have the same rank as the input tensor.");if(e.length>2){if(e[0].dataType!==e[2].dataType)throw new Error("x and x-zero-point must have the same data type.");if(e[1].dims.length!==e[2].dims.length)throw new Error("scale and zero-point inputs must have the same rank.");if(!e[1].dims.map((r,i)=>r===e[2].dims[i]).reduce((r,i)=>r&&i,!0))throw new Error("scale and zero-point inputs must have the same shape.")}if(t.blockSize>0){if(e[1].dims.length===0||e[1].dims.length===1&&e[1].dims[0]===1)throw new Error("blockSize must be set only for block quantization.");if(!e[1].dims.map((a,n)=>n===t.axis||a===e[0].dims[n]).reduce((a,n)=>a&&n,!0))throw new Error("For block qunatization, scale input shape to match the input shape except for the axis");if(e[1].dims.length!==e[0].dims.length)throw new Error("For block qunatization the scale input rank must be the same as the x rank.");let r=e[0].dims[t.axis],i=e[1].dims[t.axis];if(t.blockSize<Math.ceil(r/i)||t.blockSize>Math.ceil(r/(i-1)-1))throw new Error("blockSize must be with in the range [ceil(dI / Si), ceil(dI / (Si - 1) - 1)].")}},lp=(e,t)=>{let r=O.normalizeAxis(t.axis,e[0].dims.length),i=e[0].dataType,a=i===3,n=e[0].dims,s=e[1].dataType,u=O.size(n),l=i===3||i===2,p=l?[Math.ceil(O.size(e[0].dims)/4)]:e[0].dims,h=e[1].dims,f=e.length>2?e[2]:void 0,g=f?l?[Math.ceil(O.size(f.dims)/4)]:f.dims:void 0,y=h.length===0||h.length===1&&h[0]===1,_=y===!1&&h.length===1,w=ve(u),S=y&&(!l||w===4),x=S?w:1,b=S&&!l?w:1,I=M("input",l?12:i,p.length,b),k=M("scale",s,h.length),E=f?M("zero_point",l?12:i,g.length):void 0,A=Q("output",s,n.length,x),C=[I,k];E&&C.push(E);let $=[p,h];f&&$.push(g);let N=[{type:12,data:u/x},{type:12,data:r},{type:12,data:t.blockSize},...Y(...$,n)],D=G=>{let V=[{name:"output_size",type:"u32"},{name:"axis",type:"u32"},{name:"block_size",type:"u32"}];return`
      ${G.registerUniforms(V).declareVariables(...C,A)}
      ${G.mainStart()}
          ${G.guardAgainstOutOfBoundsWorkgroupSizes("uniforms.output_size")}
          let output_indices = ${A.offsetToIndices("global_idx")};

          // Set input x
          ${l?`
            let input = ${I.getByOffset("global_idx / 4")};
            let x_vec = ${a?"unpack4xI8(input)":"unpack4xU8(input)"};
            let x_value = ${x===1?"x_vec[global_idx % 4]":"x_vec"};`:`let x_value = ${I.getByOffset("global_idx")};`};

          // Set scale input
          ${y?`let scale_value= ${k.getByOffset("0")}`:_?`
            let scale_index = ${A.indicesGet("output_indices","uniforms.axis")};
            let scale_value= ${k.getByOffset("scale_index")};`:`
            var scale_indices: ${k.type.indices} = output_indices;
            let index = ${k.indicesGet("scale_indices","uniforms.axis")} / uniforms.block_size;
            ${k.indicesSet("scale_indices","uniforms.axis","index")};
            let scale_value= ${k.getByIndices("scale_indices")};`};

          // Set zero-point input
          ${E?y?l?`
                let zero_point_input = ${E.getByOffset("0")};
                let zero_point_vec =  ${a?"unpack4xI8(zero_point_input)":"unpack4xU8(zero_point_input)"};
                let zero_point_value= zero_point_vec[0]`:`let zero_point_value = ${E.getByOffset("0")}`:_?l?`
                let zero_point_index = ${A.indicesGet("output_indices","uniforms.axis")};
                let zero_point_input = ${E.getByOffset("zero_point_index / 4")};
                let zero_point_vec =  ${a?"unpack4xI8(zero_point_input)":"unpack4xU8(zero_point_input)"};
                let zero_point_value = zero_point_vec[zero_point_index % 4]`:`
                let zero_point_index = ${A.indicesGet("output_indices","uniforms.axis")};
                let zero_point_value = ${E.getByOffset("zero_point_index")};`:l?`
                let zero_point_offset = ${k.indicesToOffset("scale_indices")};
                let zero_point_input = ${E.getByOffset("zero_point_offset / 4")};
                let zero_point_vec = ${a?"unpack4xI8(zero_point_input)":"unpack4xU8(zero_point_input)"};
                let zero_point_value = zero_point_vec[zero_point_offset % 4];`:`let zero_point_value = ${E.getByIndices("scale_indices")};`:`let zero_point_value = ${l?a?"i32":"u32":I.type.value}(0);`};
      // Compute and write output
      ${A.setByOffset("global_idx",`${A.type.value}(x_value - zero_point_value) * scale_value`)};
      }`};return{name:"DequantizeLinear",shaderCache:{hint:t.cacheKey,inputDependencies:E?["rank","rank","rank"]:["rank","rank"]},getShaderSource:D,getRunData:()=>({outputs:[{dims:n,dataType:s}],dispatchGroup:{x:Math.ceil(u/x/64),y:1,z:1},programUniforms:N})}},dp=(e,t)=>{up(e.inputs,t),e.compute(lp(e.inputs,t))},pp=e=>he({axis:e.axis,blockSize:e.blockSize})}),cp,hp,fp,Dm=q(()=>{Pe(),te(),ae(),cp=(e,t,r)=>{let i=e===t,a=e<t&&r<0,n=e>t&&r>0;if(i||a||n)throw new Error("Range these inputs' contents are invalid.")},hp=(e,t,r,i)=>{let a=Math.abs(Math.ceil((t-e)/r)),n=[a],s=a,u=[{type:12,data:s},{type:i,data:e},{type:i,data:r},...Y(n)],l=p=>{let h=Q("output",i,n.length),f=h.type.value,g=[{name:"outputSize",type:"u32"},{name:"start",type:f},{name:"delta",type:f}];return`
        ${p.registerUniforms(g).declareVariables(h)}
        ${p.mainStart()}
        ${p.guardAgainstOutOfBoundsWorkgroupSizes("uniforms.outputSize")}
        output[global_idx] = uniforms.start + ${f}(global_idx) * uniforms.delta;
      }`};return{name:"Range",shaderCache:{hint:`${i}`},getShaderSource:l,getRunData:()=>({outputs:[{dims:n,dataType:i}],dispatchGroup:{x:Math.ceil(s/64)},programUniforms:u})}},fp=e=>{let t=0,r=0,i=0;e.inputs[0].dataType===6?(t=e.inputs[0].getInt32Array()[0],r=e.inputs[1].getInt32Array()[0],i=e.inputs[2].getInt32Array()[0]):e.inputs[0].dataType===1&&(t=e.inputs[0].getFloat32Array()[0],r=e.inputs[1].getFloat32Array()[0],i=e.inputs[2].getFloat32Array()[0]),ye.webgpu.validateInputContent&&cp(t,r,i),e.compute(hp(t,r,i,e.inputs[0].dataType),{inputs:[]})}}),mp,gp,yp,_p,Um=q(()=>{te(),re(),xe(),ae(),mp=(e,t,r,i)=>{if(e!=="none"&&i!=="i32"&&i!=="u32"&&i!=="f32")throw new Error(`Input ${i} is not supported with reduction ${e}.`);let a=`{
                var oldValue = 0;
                loop {
                  let newValueF32 =`,n=`;
                  let newValue = bitcast<i32>(newValueF32);
                  let res = atomicCompareExchangeWeak(&${t}, oldValue, newValue);
                  if res.exchanged {
                    break;
                  }
                  oldValue = res.old_value;
                }
              }`;switch(e){case"none":return`${t}=${r};`;case"add":return i==="i32"||i==="u32"?`atomicAdd(&${t}, bitcast<${i}>(${r}));`:`
              ${a}bitcast<${i}>(oldValue) + (${r})${n}`;case"max":return i==="i32"||i==="u32"?`atomicMax(&${t}, bitcast<${i}>(${r}));`:`
                ${a}max(bitcast<f32>(oldValue), (${r}))${n}`;case"min":return i==="i32"||i==="u32"?`atomicMin(&${t}, bitcast<${i}>(${r}));`:`${a}min(bitcast<${i}>(oldValue), (${r}))${n}`;case"mul":return`${a}(bitcast<${i}>(oldValue) * (${r}))${n}`;default:throw new Error(`Reduction ${e} is not supported.`)}},gp=(e,t)=>{let r=e[0].dims,i=e[1].dims,a=r,n=1,s=Math.ceil(O.sizeToDimension(i,i.length-1)/n),u=i[i.length-1],l=O.sizeFromDimension(r,u),p=[{type:12,data:s},{type:12,data:u},{type:12,data:l},...Y(e[1].dims,e[2].dims,a)],h=f=>{let g=M("indices",e[1].dataType,e[1].dims.length),y=M("updates",e[2].dataType,e[2].dims.length,n),_=t.reduction!=="none"&&t.reduction!==""?xs("output",e[0].dataType,a.length):Q("output",e[0].dataType,a.length,n);return`
      ${f.registerUniform("output_size","u32").registerUniform("last_index_dimension","u32").registerUniform("num_updates_elements","u32").declareVariables(g,y,_)}
      ${f.mainStart()}
        ${f.guardAgainstOutOfBoundsWorkgroupSizes("uniforms.output_size")}
  var data_offset = 0u;
  let indices_start = uniforms.last_index_dimension * global_idx;
  let indices_end = indices_start + uniforms.last_index_dimension;
  for (var i = indices_start; i < indices_end; i++) {
    var index = i32(indices[i].x);
    ${e[0].dims.length===1?`
    let element_count_dim = uniforms.output_strides;
    let dim_value = uniforms.output_shape;`:`
    let element_count_dim = uniforms.output_strides[i - indices_start];
    let dim_value = uniforms.output_shape[i - indices_start];`}
    if (index >= 0) {
      if (index >= i32(dim_value)) {
        index = i32(dim_value - 1);
      }
    } else {
      if (index < -i32(dim_value)) {
        index = 0;
      } else {
        index += i32(dim_value);
      }
    }
    data_offset += u32((u32(index) * element_count_dim));
  }

  for (var i = 0u; i < uniforms.num_updates_elements; i++) {
    let value = updates[uniforms.num_updates_elements * global_idx + i];
    ${mp(t.reduction,"output[data_offset + i]","value",_.type.value)}
  }

      }`};return{name:"ScatterND",shaderCache:{hint:`${t.cacheKey}_${t.reduction}`,inputDependencies:["rank","rank"]},getRunData:()=>({outputs:[{dims:a,dataType:e[0].dataType}],dispatchGroup:{x:Math.ceil(s/64)},programUniforms:p}),getShaderSource:h}},yp=e=>he({reduction:e.reduction}),_p=(e,t)=>{e.compute(gp(e.inputs,t),{inputs:[e.inputs[1],e.inputs[2]],outputs:[]})}}),wp,bp,$p,Ia,vp,xp,Sp,Tp,kp,Ip,Ep,zp,Ea,Cp,Ap,Op,Rp,Bp,Mp,Np,Pm=q(()=>{te(),re(),xe(),ae(),wp=(e,t)=>{if(e.every(r=>r>0||(()=>{throw new Error("Resize requires scales input values to be positive")})),e.length>0){if(t.mode==="linear"){if(!(e.length===2||e.length===3||e.length===4&&e[0]===1&&e[1]===1||e.length===4&&e[0]===1&&e[3]===1||e.length===5&&e[0]===1&&e[1]===1))throw new Error(`For linear mode, Resize requires scales to be 2D, 3D, 4D with either two outermost or one innermost and
            one outermost scale values equal to 1, or 5D with two outermost scale values equal to 1`)}else if(t.mode==="cubic"&&!(e.length===2||e.length===4&&e[0]===1&&e[1]===1||e.length===4&&e[0]===1&&e[3]===1))throw new Error("Resize requires scales input size to be 2 or 4 for cubic mode")}},bp=(e,t,r)=>{t.every(a=>a>=0&&a<r||(()=>{throw new Error("Resize requires axes input values to be positive and less than rank")}));let i=new Array(r).fill(1);return t.forEach((a,n)=>i[a]=e[n]),i},$p=(e,t,r,i,a,n)=>{let[s,u,l]=r>10?[1,2,3]:[-1,e.length>1?1:-1,-1],p=e[0].dims.length;if(s>0&&e.length>s&&e[s].dims.length>0)e[s].getFloat32Array().forEach(h=>n.push(h));else if(t.coordinateTransformMode==="tf_crop_and_resize")throw new Error("Resize requires RoI input to be specified when coordinateTransformMode is tfCropAndResize");if(u>0&&e.length>u&&e[u].dims.length===1&&e[u].dims[0]>0){if(e[u].getFloat32Array().forEach(h=>i.push(h)),i.length!==0&&i.length!==p&&r>=18&&i.length!==t.axes.length)throw new Error("Resize requires scales input size to be same as input rank or axes size for opset 18 and up");wp(i,t),t.axes.length>0&&bp(i,t.axes,p).forEach((h,f)=>i[f]=h)}if(l>0&&e.length>l&&e[l].dims.length===1&&e[l].dims[0]>0&&(e[l].getBigInt64Array().forEach(h=>a.push(Number(h))),a.length!==0&&a.length!==p&&r>=18&&a.length!==t.axes.length))throw new Error("Resize requires sizes input size to be same as input rank or axes size for opset 18 and up");if(t.axes.length>0){if(i.length!==0&&i.length!==t.axes.length)throw new Error('Resize requires "scales" input size to be of axes rank when axes attributes is specified');if(a.length!==0&&a.length!==t.axes.length)throw new Error('Resize requires "sizes" input size to be of rank axes rank when axes attributes is specified')}if(typeof i<"u"&&typeof a<"u"&&i.length>0&&a.length>p)throw new Error("Resize requires only of scales or sizes to be specified")},Ia=(e,t,r,i)=>`
  // The whole part and the fractional part are calculated separately due to inaccuracy of floating
  // point division. As an example, f32(21) / f32(7) may evaluate to 2.99... instead of 3, causing an
  // offset-by-one error later in floor().
  let big = (${e}) * (${t});
  let whole = ${i}(big / (${r}));
  let fract = ${i}(big % (${r})) / ${i}(${r});
  return whole + fract;
`,vp=(e,t)=>`fn getOriginalCoordinateFromResizedCoordinate(xResized: u32, xScale: f32, lengthResized: u32,
     lengthOriginal: u32, roiStart: f32, roiEnd: f32) -> ${t} { `+(()=>{switch(e){case"asymmetric":return`
          if (xScale < 1.0 || floor(xScale) != xScale) {
            return ${t}(xResized) / ${t}(xScale);
          } else {
            ${Ia("xResized","lengthOriginal","lengthResized",t)}
          }
        `;case"pytorch_half_pixel":return`if (lengthResized > 1) {
                    return (${t}(xResized) + 0.5) / ${t}(xScale) - 0.5;
                  } else {
                    return 0.0;
                  }`;case"tf_half_pixel_for_nn":return`return (${t}(xResized) + 0.5) / ${t}(xScale);`;case"align_corners":return`if (lengthResized == 1) {
                    return 0.0;
                  } else {
                    ${Ia("xResized","lengthOriginal - 1","lengthResized - 1",t)}
                  }`;case"tf_crop_and_resize":return`if (lengthResized > 1) {
                    return ${t}(roiStart) * ${t}(lengthOriginal - 1) +
                        (${t}(xResized) * ${t}(roiEnd - roiStart) * ${t}(lengthOriginal - 1)) /
                        ${t}(lengthResized - 1);
                  } else {
                    return 0.5 * ${t}(roiStart + roiEnd) * ${t}(lengthOriginal - 1);
                  }`;case"half_pixel_symmetric":return`const outputWidth = ${t}xScale * ${t}(lengthResized);
                  const adjustment = ${t}(lengthResized) / outputWidth;
                  const center = ${t}(lengthOriginal) / 2;
                  const offset = center * (1 - adjustment);
                  return offset + ((${t}(xResized) + 0.5) / ${t}(xScale)) - 0.5;`;case"half_pixel":return`return ((${t}(xResized) + 0.5) / ${t}(xScale)) - 0.5;`;default:throw new Error(`Coordinate transform mode ${e} is not supported`)}})()+"}",xp=(e,t,r)=>`fn getNearestPixelFromOriginal(xOriginal: ${r}, isDownSample: bool) -> ${r} {`+(()=>{switch(e){case"round_prefer_ceil":return"if (fract(xOriginal) == 0.5) {             return ceil(xOriginal);           } else {             return round(xOriginal);           }";case"floor":return"return floor(xOriginal);";case"ceil":return"return ceil(xOriginal);";case"round_prefer_floor":return"if (fract(xOriginal) == 0.5) {                     return floor(xOriginal);                   } else {                     return round(xOriginal);                   }";case"simple":default:if(t<11)return"if (isDownSample)                     {                       return ceil(xOriginal);                     } else {                       return xOriginal;                     }";throw new Error(`Nearest mode ${e} is not supported`)}})()+"}",Sp=(e,t,r)=>{let i=new Array(r).fill(0).concat(new Array(r).fill(1)),a=e.length===0?i:e.slice();return t.length>0?(t.forEach((n,s)=>{i[n]=a[s],i[s+r]=a[t.length+s]}),i):a},Tp=(e,t,r,i)=>{let a=[];if(r.length>0)if(i.length>0){if(e.forEach(n=>a.push(n)),Math.max(...i)>e.length)throw new Error("axes is out of bound");i.forEach((n,s)=>a[n]=r[s])}else r.forEach(n=>a.push(n));else{if(t.length===0)throw new Error("Resize requires either scales or sizes.");a=e.map((n,s)=>Math.round(n*t[s]))}return a},kp=(e,t,r)=>{let i=(()=>{switch(r.keepAspectRatioPolicy){case"not_larger":return r.axes.length>0?Math.min(...r.axes.map(n=>t[n]),Number.MAX_VALUE):Math.min(...t,Number.MAX_VALUE);case"not_smaller":return r.axes.length>0?Math.max(...r.axes.map(n=>t[n]),Number.MIN_VALUE):Math.max(...t,Number.MIN_VALUE);default:throw new Error(`Keep aspect ratio policy ${r.keepAspectRatioPolicy} is not supported`)}})();t.fill(1,0,t.length);let a=e.slice();return r.axes.length>0?(r.axes.forEach(n=>t[n]=i),r.axes.forEach(n=>a[n]=Math.round(e[n]*t[n]))):(t.fill(i,0,t.length),a.forEach((n,s)=>a[s]=Math.round(n*t[s]))),a},Ip=(e,t,r,i,a)=>`
    fn calculateOriginalIndicesFromOutputIndices(output_indices: ${e.type.indices}) -> array<${e.type.value}, ${r.length}> {
      var original_indices: array<${e.type.value}, ${r.length}>;
      for (var i:u32 = 0; i < ${r.length}; i++) {
        var output_index = ${e.indicesGet("output_indices","i")};
        var scale = ${Z("uniforms.scales","i",i)};
        var roi_low = ${Z("uniforms.roi","i",a)};
        var roi_hi = ${Z("uniforms.roi",`i + ${t.length}`,a)};
        if (scale == 1.0) {
          original_indices[i] = ${e.type.value}(output_index);
        } else {
          var input_shape_i = ${Z("uniforms.input_shape","i",t.length)};
          var output_shape_i = ${Z("uniforms.output_shape","i",r.length)};
          original_indices[i] = getOriginalCoordinateFromResizedCoordinate(output_index, scale, output_shape_i,
                                                                           input_shape_i, roi_low, roi_hi);
        }
      }
      return original_indices;
    }`,Ep=(e,t,r,i,a,n,s)=>`
    fn calculateInputIndicesFromOutputIndices(output_indices: ${t.type.indices}) -> ${e.type.indices} {
      var input_indices: ${e.type.indices};
      for (var i:u32 = 0; i < ${i.length}; i++) {
        var output_index = ${t.indicesGet("output_indices","i")};
        var input_index: u32;
        var scale = ${Z("uniforms.scales","i",a)};
        if (scale == 1.0) {
          input_index = output_index;
        } else {
          var roi_low = ${Z("uniforms.roi","i",n)};
          var roi_hi = ${Z("uniforms.roi",`i + ${r.length}`,n)};
          var input_shape_i = ${Z("uniforms.input_shape","i",r.length)};
          var output_shape_i = ${Z("uniforms.output_shape","i",i.length)};
          var original_idx = getOriginalCoordinateFromResizedCoordinate(output_index, scale, output_shape_i,
                                                                        input_shape_i, roi_low, roi_hi);
          if (!${s} || (original_idx >= 0 && original_idx < ${t.type.value}(input_shape_i))) {
            if (original_idx < 0) {
              input_index = 0;
            } else if (original_idx > ${t.type.value}(input_shape_i - 1)) {
              input_index = input_shape_i - 1;
            } else {
              input_index = u32(getNearestPixelFromOriginal(original_idx, scale < 1));
            }
          } else {
            input_index = u32(original_idx);
          }
        }
        ${e.indicesSet("input_indices","i","input_index")}
      }
      return input_indices;
    }`,zp=(e,t)=>`
    fn checkInputIndices(input_indices: ${e.type.indices}) -> bool {
      for (var i:u32 = 0; i < ${t.length}; i++) {
        var input_index = ${e.indicesGet("input_indices","i")};
        if (input_index < 0 || input_index >= ${Z("uniforms.input_shape","i",t.length)}) {
          return false;
        }
      }
      return true;
    }`,Ea=(e,t,r,i)=>e.rank>i?`
    ${e.indicesSet("input_indices",t,"channel")};
    ${e.indicesSet("input_indices",r,"batch")};
`:"",Cp=(e,t,r,i,a)=>{let[n,s,u,l]=r.length===2?[-1,0,1,-1]:[0,2,3,1],p=e.type.value;return`
    fn getInputValue(batch: u32, channel: u32, row: u32, col: u32) -> ${p} {
      var input_indices: ${e.type.indices};
      ${e.indicesSet("input_indices",s,`max(0, min(row, ${r[s]} - 1))`)};
      ${e.indicesSet("input_indices",u,`max(0, min(col, ${r[u]} - 1))`)};
      ${Ea(e,l,n,2)}
      return ${e.getByIndices("input_indices")};
    }

    fn bilinearInterpolation(output_indices: ${t.type.indices}) -> ${p} {
      var originalIndices = calculateOriginalIndicesFromOutputIndices(output_indices);
      var row:${p} = originalIndices[${s}];
      var col:${p} = originalIndices[${u}];
      ${i?`if (row < 0 || row > (${r[s]} - 1) || col < 0 || col > (${r[u]} - 1)) {
        return ${a};
      }`:""};
      row = max(0, min(row, ${r[s]} - 1));
      col = max(0, min(col, ${r[u]} - 1));
      var row1: u32 = u32(row);
      var col1: u32 = u32(col);
      var row2: u32 = u32(row + 1);
      var col2: u32 = u32(col + 1);
      var channel: u32 = ${r.length>2?`u32(originalIndices[${l}])`:"0"};
      var batch: u32 =  ${r.length>2?`u32(originalIndices[${n}])`:"0"};
      var x11: ${p} = getInputValue(batch, channel, row1, col1);
      var x12: ${p} = getInputValue(batch, channel, row1, col2);
      var x21: ${p} = getInputValue(batch, channel, row2, col1);
      var x22: ${p} = getInputValue(batch, channel, row2, col2);
      var dx1: ${p} = abs(row - ${p}(row1));
      var dx2: ${p} = abs(${p}(row2) - row);
      var dy1: ${p} = abs(col - ${p}(col1));
      var dy2: ${p} = abs(${p}(col2) - col);
      if (row1 == row2) {
        dx1 = 0.5;
        dx2 = 0.5;
      }
      if (col1 == col2) {
        dy1 = 0.5;
        dy2 = 0.5;
      }
      return (x11 * dx2 * dy2 + x12 * dx2 * dy1 + x21 * dx1 * dy2 + x22 * dx1 * dy1);
    }`},Ap=(e,t,r,i,a,n,s,u,l,p)=>{let h=r.length===2,[f,g]=h?[0,1]:[2,3],y=e.type.value,_=w=>{let S=w===f?"row":"col";return`
      fn ${S}CubicInterpolation(input_indices: ${e.type.indices}, output_indices: ${t.type.indices}) -> ${y} {
        var output_index = ${t.indicesGet("output_indices",w)};
        var originalIdx: ${y} = getOriginalCoordinateFromResizedCoordinate(output_index, ${a[w]},
        ${i[w]}, ${r[w]}, ${n[w]}, ${n[w]} + ${r.length});
        var fractOriginalIdx: ${y} = originalIdx - floor(originalIdx);
        var coefs = getCubicInterpolationCoefs(fractOriginalIdx);

        if (${u} && (originalIdx < 0 || originalIdx > (${r[w]} - 1))) {
          return ${l};
        }
        var data: array<${y}, 4> = array<${y}, 4>(0.0, 0.0, 0.0, 0.0);
        for (var i: i32 = -1; i < 3; i++) {
          var ${S}: ${y} = originalIdx + ${y}(i);
          if (${S} < 0 || ${S} >= ${r[w]}) {
            ${p?`coefs[i + 1] = 0.0;
                        continue;`:u?`return ${l};`:`${S} = max(0, min(${S}, ${r[w]} - 1));`};
          }
        var input_indices_copy: ${e.type.indices} = input_indices;
          ${e.indicesSet("input_indices_copy",w,`u32(${S})`)};
          data[i + 1] = ${w===f?e.getByIndices("input_indices_copy"):"rowCubicInterpolation(input_indices_copy, output_indices)"};
        }
        return cubicInterpolation1D(data, coefs);
      }`};return`
    ${_(f)};
    ${_(g)};
  fn getCubicInterpolationCoefs(s: ${y}) -> array<${y}, 4> {
    var absS = abs(s);
    var coeffs: array<${y}, 4> = array<${y}, 4>(0.0, 0.0, 0.0, 0.0);
    var oneMinusAbsS: ${y} = 1.0 - absS;
    var twoMinusAbsS: ${y} = 2.0 - absS;
    var onePlusAbsS: ${y} = 1.0 + absS;
    coeffs[0] = ((${s} * onePlusAbsS - 5 * ${s}) * onePlusAbsS + 8 * ${s}) * onePlusAbsS - 4 * ${s};
    coeffs[1] = ((${s} + 2) * absS - (${s} + 3)) * absS * absS + 1;
    coeffs[2] = ((${s} + 2) * oneMinusAbsS - (${s} + 3)) * oneMinusAbsS * oneMinusAbsS + 1;
    coeffs[3] = ((${s} * twoMinusAbsS - 5 * ${s}) * twoMinusAbsS + 8 * ${s}) * twoMinusAbsS - 4 * ${s};
    return coeffs;
  }

  fn cubicInterpolation1D(x: array<${y}, 4>, coefs: array<${y}, 4>) -> ${y} {
    var coefsSum: ${y} = coefs[0] + coefs[1] + coefs[2] + coefs[3];
    return (x[0] * coefs[0] + x[1] * coefs[1]+ x[2] * coefs[2]+ x[3] * coefs[3]) / coefsSum;
  }

  fn bicubicInterpolation(output_indices: ${t.type.indices}) -> ${y} {
    var input_indices: ${e.type.indices} = output_indices;
    return colCubicInterpolation(input_indices, output_indices);
  }
    `},Op=(e,t,r,i,a)=>{let[n,s,u,l,p]=r.length===3?[-1,0,1,2,-1]:[0,2,3,4,1],h=e.type.value;return`
    fn getInputValue(batch: u32, channel: u32, depth:u32, height: u32, width: u32) -> ${h} {
      var input_indices: ${e.type.indices};
      ${e.indicesSet("input_indices",s,`max(0, min(depth, ${r[s]} - 1))`)};
      ${e.indicesSet("input_indices",u,`max(0, min(height, ${r[u]} - 1))`)};
      ${e.indicesSet("input_indices",l,`max(0, min(width, ${r[l]} - 1))`)};
      ${Ea(e,p,n,3)}
      return ${e.getByIndices("input_indices")};
    }

    fn trilinearInterpolation(output_indices: ${t.type.indices}) -> ${h} {
      var originalIndices = calculateOriginalIndicesFromOutputIndices(output_indices);
      var depth:${h} = originalIndices[${s}];
      var height:${h} = originalIndices[${u}];
      var width:${h} = originalIndices[${l}];
      ${i?`if (depth < 0 || depth > (${r[s]} - 1) || height < 0 || height > (${r[u]} - 1) || width < 0 || (width > ${r[l]} - 1)) {
      return ${a};
        }`:""};

    depth = max(0, min(depth, ${r[s]} - 1));
      height = max(0, min(height, ${r[u]} - 1));
      width = max(0, min(width, ${r[l]} - 1));
      var depth1: u32 = u32(depth);
      var height1: u32 = u32(height);
      var width1: u32 = u32(width);
      var depth2: u32 = u32(depth + 1);
      var height2: u32 = u32(height + 1);
      var width2: u32 = u32(width + 1);
      var channel: u32 = ${r.length>3?`u32(originalIndices[${p}])`:"0"};
      var batch: u32 =  ${r.length>3?`u32(originalIndices[${n}])`:"0"};

      var x111: ${h} = getInputValue(batch, channel, depth1, height1, width1);
      var x112: ${h} = getInputValue(batch, channel, depth1, height1, width2);
      var x121: ${h} = getInputValue(batch, channel, depth1, height2, width1);
      var x122: ${h} = getInputValue(batch, channel, depth1, height2, width2);
      var x211: ${h} = getInputValue(batch, channel, depth2, height1, width1);
      var x212: ${h} = getInputValue(batch, channel, depth2, height1, width2);
      var x221: ${h} = getInputValue(batch, channel, depth2, height2, width1);
      var x222: ${h} = getInputValue(batch, channel, depth2, height2, width2);
      var dx1: ${h} = abs(depth - ${h}(depth1));
      var dx2: ${h} = abs(${h}(depth2) - depth);
      var dy1: ${h} = abs(height - ${h}(height1));
      var dy2: ${h} = abs(${h}(height2) - height);
      var dz1: ${h} = abs(width - ${h}(width1));
      var dz2: ${h} = abs(${h}(width2) - width);
      if (depth1 == depth2) {
        dx1 = 0.5;
        dx2 = 0.5;
      }
      if (height1 == height2) {
        dy1 = 0.5;
        dy2 = 0.5;
      }
      if (width1 == width2) {
        dz1 = 0.5;
        dz2 = 0.5;
      }
      return (x111 * dx2 * dy2 * dz2 + x112 * dx2 * dy2 * dz1 + x121 * dx2 * dy1 *dz2 + x122 * dx2 * dy1 * dz1 +
              x211 * dx1 * dy2 * dz2 + x212 * dx1 * dy2 * dz1 + x221 * dx1 * dy1 *dz2 + x222 * dx1 * dy1 * dz1);
    }`},Rp=(e,t,r,i,a,n)=>{let s=e.dims,u=Sp(n,t.axes,s.length),l=Tp(s,i,a,t.axes),p=i.slice();i.length===0&&(p=s.map((b,I)=>b===0?1:l[I]/b),t.keepAspectRatioPolicy!=="stretch"&&(l=kp(s,p,t)));let h=Q("output",e.dataType,l.length),f=M("input",e.dataType,s.length),g=O.size(l),y=s.length===l.length&&s.every((b,I)=>b===l[I]),_=t.coordinateTransformMode==="tf_crop_and_resize",w=t.extrapolationValue,S=f.type.value,x=b=>`
      ${y?"":`
      ${vp(t.coordinateTransformMode,S)};
      ${(()=>{switch(t.mode){case"nearest":return`
              ${zp(f,s)};
              ${xp(t.nearestMode,r,S)};
              ${Ep(f,h,s,l,p.length,u.length,_)};
              `;case"linear":return`
              ${Ip(h,s,l,p.length,u.length)};
              ${(()=>{if(s.length===2||s.length===4)return`${Cp(f,h,s,_,w)}`;if(s.length===3||s.length===5)return`${Op(f,h,s,_,w)}`;throw Error("Linear mode only supports input dims 2, 3, 4 and 5 are supported in linear mode.")})()};
            `;case"cubic":return`
            ${(()=>{if(s.length===2||s.length===4)return`${Ap(f,h,s,l,p,u,t.cubicCoeffA,_,t.extrapolationValue,t.excludeOutside)}`;throw Error("Cubic mode only supports input dims 2 and 4 are supported in linear mode.")})()};
            `;default:throw Error("Invalid resize mode")}})()};
      `}
      ${b.registerUniform("output_size","u32").registerUniform("scales","f32",p.length).registerUniform("roi","f32",u.length).declareVariables(f,h)}
      ${b.mainStart()}
        ${b.guardAgainstOutOfBoundsWorkgroupSizes("uniforms.output_size")}
        ${y?"output[global_idx] = input[global_idx];":`
        let output_indices = ${h.offsetToIndices("global_idx")};
        var input_indices: ${f.type.indices};
        ${(()=>{switch(t.mode){case"nearest":return`input_indices = calculateInputIndicesFromOutputIndices(output_indices);
                if (checkInputIndices(input_indices)) {
                  output[global_idx] = ${f.getByIndices("input_indices")};
                } else {
                  output[global_idx] = ${t.extrapolationValue};
                }`;case"linear":return`output[global_idx] = ${s.length===2||s.length===4?"bilinearInterpolation":"trilinearInterpolation"}(output_indices);`;case"cubic":return"output[global_idx] = bicubicInterpolation(output_indices);";default:throw Error(`Unsupported resize mode: ${t.mode}`)}})()};
`}
      }`;return{name:"Resize",shaderCache:{hint:`${t.cacheKey}|${r}|${p.length>0?t.mode==="cubic"?p:p.length:""}|${a.length>0?a:""}|${u.length>0?u:""}|${y}|${t.mode==="nearest"?s.length:s}`,inputDependencies:["rank"]},getShaderSource:x,getRunData:()=>({outputs:[{dims:l,dataType:e.dataType}],dispatchGroup:{x:Math.ceil(g/64)},programUniforms:[{type:12,data:g},{type:1,data:p},{type:1,data:u},...Y(s,l)]})}},Bp=e=>{let t=e.customDataBuffer;return new Uint32Array(t,t.byteOffset,1)[0]},Mp=(e,t)=>{let r=[],i=[],a=[],n=Bp(e);if(t.antialias!==0)throw Error("Only default value (0) for Antialias attribute is supported");$p(e.inputs,t,n,r,i,a),e.compute(Rp(e.inputs[0],t,n,r,i,a),{inputs:[0]})},Np=e=>{let t=e.antialias,r=e.axes,i=e.coordinateTransformMode,a=e.cubicCoeffA,n=e.excludeOutside!==0,s=e.extrapolationValue,u=e.keepAspectRatioPolicy,l=e.mode,p=e.nearestMode===""?"simple":e.nearestMode;return he({antialias:t,axes:r,coordinateTransformMode:i,cubicCoeffA:a,excludeOutside:n,extrapolationValue:s,keepAspectRatioPolicy:u,mode:l,nearestMode:p})}}),Dp,Up,Pp,qm=q(()=>{te(),re(),ae(),Dp=e=>{if(!e||e.length<3)throw new Error("layerNorm requires at least 3 inputs.");let t=e[0],r=e[1],i=e[2];if(t.dataType!==r.dataType||t.dataType!==i.dataType)throw new Error("All inputs must have the same data type");if(t.dims.length!==3&&t.dims.length!==2)throw new Error("Input must be 2D or 3D");if(r.dims.length!==3&&r.dims.length!==2)throw new Error("Skip must be 2D or 3D");let a=t.dims[t.dims.length-1],n=t.dims[t.dims.length-2];if(r.dims[r.dims.length-1]!==a)throw new Error("Skip must have the same hidden size as input");if(r.dims[r.dims.length-2]!==n)throw new Error("Skip must have the same sequence length as input");if(i.dims.length!==1)throw new Error("Gamma must be 1D");if(i.dims[i.dims.length-1]!==a)throw new Error("Gamma must have the same hidden size as input");if(e.length>3){let s=e[3];if(s.dims.length!==1)throw new Error("Beta must be 1D");if(s.dims[s.dims.length-1]!==a)throw new Error("Beta must have the same hidden size as input")}if(e.length>4){let s=e[4];if(s.dims.length!==1)throw new Error("Bias must be 1D");if(s.dims[s.dims.length-1]!==a)throw new Error("Bias must have the same hidden size as input")}},Up=(e,t,r,i)=>{let a=t.simplified,n=e[0].dims,s=O.size(n),u=n,l=s,p=n.slice(-1)[0],h=i?n.slice(0,-1).concat(1):[],f=!a&&e.length>3,g=e.length>4,y=i&&r>1,_=i&&r>2,w=r>3,S=64,x=ve(p),b=[{type:12,data:l},{type:12,data:x},{type:12,data:p},{type:1,data:t.epsilon}],I=E=>{let A=[{name:"output_size",type:"u32"},{name:"components",type:"u32"},{name:"hidden_size",type:"u32"},{name:"epsilon",type:"f32"}],C=[M("x",e[0].dataType,e[0].dims,x),M("skip",e[1].dataType,e[1].dims,x),M("gamma",e[2].dataType,e[2].dims,x)];f&&C.push(M("beta",e[3].dataType,e[3].dims,x)),g&&C.push(M("bias",e[4].dataType,e[4].dims,x)),C.push(Q("output",e[0].dataType,u,x)),y&&C.push(Q("mean_output",1,h)),_&&C.push(Q("inv_std_output",1,h)),w&&C.push(Q("input_skip_bias_sum",e[0].dataType,u,x));let $=Te(e[0].dataType),N=Te(1,x);return`

      ${E.registerUniforms(A).declareVariables(...C)}
      var<workgroup> sum_shared : array<${N}, ${S}>;
      var<workgroup> sum_squared_shared : array<${N}, ${S}>;

      ${E.mainStart([S,1,1])}
        let ix = local_id.x;
        let iy = global_id.x / ${S};

        let hidden_size_vectorized: u32 = uniforms.hidden_size / uniforms.components;
        var stride = hidden_size_vectorized / ${S};
        let offset = ix * stride + iy * hidden_size_vectorized;
        let offset1d = stride * ix;
        if (ix == ${S-1}) {
          stride = hidden_size_vectorized - stride * ix;
        }
        for (var i: u32 = 0; i < stride; i++) {
          let skip_value = skip[offset + i];
          let bias_value = ${g?"bias[offset1d + i]":$+"(0.0)"};
          let input_value = x[offset + i];
          let value = input_value + skip_value + bias_value;
          ${w?"input_skip_bias_sum[offset + i] = value;":""}
          output[offset + i] = value;
          let f32_value = ${Vt($,x,"value")};
          sum_shared[ix] += f32_value;
          sum_squared_shared[ix] += f32_value * f32_value;
        }
        workgroupBarrier();

        var reduce_size : u32 = ${S};
        for (var curr_size = reduce_size >> 1;  curr_size > 0; curr_size = reduce_size >> 1) {
          reduce_size = curr_size + (reduce_size & 1);
          if (ix < curr_size) {
            sum_shared[ix] += sum_shared[ix + reduce_size];
            sum_squared_shared[ix] += sum_squared_shared[ix + reduce_size];
          }
          workgroupBarrier();
        }

        let sum = sum_shared[0];
        let square_sum = sum_squared_shared[0];
        let mean = ${lt("sum",x)} / f32(uniforms.hidden_size);
        let inv_std_dev = inverseSqrt(${lt("square_sum",x)} / f32(uniforms.hidden_size) ${a?"":"- mean * mean"} + uniforms.epsilon);
        ${y?"mean_output[global_idx] = mean;":""}
        ${_?"inv_std_output[global_idx] = inv_std_dev;":""}

        for (var i: u32 = 0; i < stride; i++) {
          output[offset + i] = (output[offset + i] ${a?"":`- ${$}(mean)`}) *
            ${$}(inv_std_dev) * gamma[offset1d + i]
            ${f?"+ beta[offset1d + i]":""};
        }
      }`},k=[{dims:u,dataType:e[0].dataType}];return r>1&&k.push({dims:h,dataType:1}),r>2&&k.push({dims:h,dataType:1}),r>3&&k.push({dims:n,dataType:e[0].dataType}),{name:"SkipLayerNormalization",shaderCache:{hint:`${x};${y};${_};${w}`,inputDependencies:e.map((E,A)=>"type")},getShaderSource:I,getRunData:()=>({outputs:k,dispatchGroup:{x:Math.ceil(l/p)},programUniforms:b})}},Pp=(e,t)=>{Dp(e.inputs);let r=[0];e.outputCount>1&&r.push(-3),e.outputCount>2&&r.push(-3),e.outputCount>3&&r.push(3),e.compute(Up(e.inputs,t,e.outputCount,!1),{outputs:r})}}),qp,or,Lp,za,Wp,Vp,Gp,Hp,Lm=q(()=>{te(),re(),xe(),ae(),qp=(e,t)=>{if(!e||e.length<1)throw new Error("too few inputs");if(t.axes.length!==0){if(t.axes.length!==t.starts.length||t.axes.length!==t.ends.length)throw new Error("axes, starts and ends must have the same length")}else if(t.starts.length!==t.ends.length)throw new Error("starts and ends must have the same length");e.slice(1).forEach((r,i)=>{if(e[i+1].dataType!==6&&e[i+1].dataType!==7)throw new Error(`Input ${i} must be an array of int32 or int64`)})},or=(e,t)=>{let r=[];if(e.length>t)if(e[t].dataType===7)e[t].getBigInt64Array().forEach(i=>r.push(Number(i)));else if(e[t].dataType===6)e[t].getInt32Array().forEach(i=>r.push(Number(i)));else throw new Error(`Input ${t} must be an array of int32 or int64`);return r},Lp=(e,t)=>{if(e.length>1){let r=or(e,1),i=or(e,2),a=or(e,3);return a.length===0&&(a=[...Array(e[0].dims.length).keys()]),he({starts:r,ends:i,axes:a})}else return t},za=(e,t,r,i,a)=>{let n=e;return e<0&&(n+=r[i[t]]),a[t]<0?Math.max(0,Math.min(n,r[i[t]]-1)):Math.max(0,Math.min(n,r[i[t]]))},Wp=(e,t,r)=>`fn calculateInputIndices(output_indices: ${t.type.indices}) -> ${e.type.indices} {
          var input_indices: ${e.type.indices};
          var carry = 0u;
          for (var i = ${r.length-1}; i >= 0; i--) {
            let input_shape_i = ${Z("uniforms.input_shape","i",r.length)};
            let steps_i = ${Z("uniforms.steps","i",r.length)};
            let signs_i = ${Z("uniforms.signs","i",r.length)};
            let starts_i = ${Z("uniforms.starts","i",r.length)};
            var output_index = ${t.indicesGet("output_indices","i")};
            var input_index = output_index * steps_i + starts_i + carry;
            carry = input_index / input_shape_i;
            input_index = input_index % input_shape_i;
            if (signs_i < 0) {
              input_index = input_shape_i - input_index - 1u + starts_i;
            }
            ${e.indicesSet("input_indices","i","input_index")};
          }
          return input_indices;
      }`,Vp=(e,t)=>{let r=e[0].dims,i=O.size(r),a=t.axes.length>0?O.normalizeAxes(t.axes,r.length):[...Array(r.length).keys()],n=or(e,4);n.forEach(x=>x!==0||(()=>{throw new Error("step cannot be 0")})),n.length===0&&(n=Array(a.length).fill(1));let s=t.starts.map((x,b)=>za(x,b,r,a,n)),u=t.ends.map((x,b)=>za(x,b,r,a,n));if(a.length!==s.length||a.length!==u.length)throw new Error("start, ends and axes should have the same number of elements");if(a.length!==r.length)for(let x=0;x<r.length;++x)a.includes(x)||(s.splice(x,0,0),u.splice(x,0,r[x]),n.splice(x,0,1));let l=n.map(x=>Math.sign(x));n.forEach((x,b,I)=>{if(x<0){let k=(u[b]-s[b])/x,E=s[b],A=E+k*n[b];s[b]=A,u[b]=E,I[b]=-x}});let p=r.slice(0);a.forEach((x,b)=>{p[x]=Math.ceil((u[x]-s[x])/n[x])});let h={dims:p,dataType:e[0].dataType},f=Q("output",e[0].dataType,p.length),g=M("input",e[0].dataType,e[0].dims.length),y=O.size(p),_=[{name:"outputSize",type:"u32"},{name:"starts",type:"u32",length:s.length},{name:"signs",type:"i32",length:l.length},{name:"steps",type:"u32",length:n.length}],w=[{type:12,data:y},{type:12,data:s},{type:6,data:l},{type:12,data:n},...Y(e[0].dims,p)],S=x=>`
      ${x.registerUniforms(_).declareVariables(g,f)}
        ${Wp(g,f,r)}
        ${x.mainStart()}
          ${x.guardAgainstOutOfBoundsWorkgroupSizes("uniforms.outputSize")}
          let output_indices = ${f.offsetToIndices("global_idx")};
          let input_indices = calculateInputIndices(output_indices);
          ${f.setByOffset("global_idx",g.getByIndices("input_indices"))}
      }`;return{name:"Slice",shaderCache:{hint:`${l.length}_${s.length}_${n.length}`,inputDependencies:["rank"]},getShaderSource:S,getRunData:()=>({outputs:[h],dispatchGroup:{x:Math.ceil(i/64)},programUniforms:w})}},Gp=(e,t)=>{qp(e.inputs,t);let r=Lp(e.inputs,t);e.compute(Vp(e.inputs,r),{inputs:[0]})},Hp=e=>{let t=e.starts,r=e.ends,i=e.axes;return he({starts:t,ends:r,axes:i})}}),Fp,jp,Kp,Qp,Wm=q(()=>{te(),re(),xe(),dt(),ae(),Fp=e=>{if(!e||e.length!==1)throw new Error("Softmax op requires 1 input.")},jp=(e,t)=>{let r=e.inputs[0],i=r.dims,a=O.size(i),n=i.length,s=O.normalizeAxis(t.axis,n),u=s<i.length-1,l,p=[];u?(p=Array.from({length:n},(C,$)=>$),p[s]=n-1,p[n-1]=s,l=e.compute(Ne(r,p),{inputs:[r],outputs:[-1]})[0]):l=r;let h=l.dims,f=h[n-1],g=a/f,y=ve(f),_=f/y,w=64;g===1&&(w=256);let S=(C,$)=>$===4?`max(max(${C}.x, ${C}.y), max(${C}.z, ${C}.w))`:$===2?`max(${C}.x, ${C}.y)`:$===3?`max(max(${C}.x, ${C}.y), ${C}.z)`:C,x=M("x",l.dataType,l.dims,y),b=Q("result",l.dataType,l.dims,y),I=x.type.value,k=Te(l.dataType)==="f32"?`var threadMax = ${I}(-3.4028234663852886e+38f);`:`var threadMax = ${I}(-65504.0h);`,E=C=>`
      var<workgroup> rowMaxShared : ${I};
      var<workgroup> rowSumShared : ${I};
      var<workgroup> threadShared : array<${I}, ${w}>;

      fn getValue(row: i32, col: i32, row_stride: i32) -> ${I} {
        let index = row * row_stride + col;
        return x[index];
      }

      fn setValue(row: i32, col: i32, row_stride: i32, value: ${I}) {
        let index = row * row_stride + col;
        result[index] = value;
      }
      ${C.registerUniform("packedCols","i32").declareVariables(x,b)}
      ${C.mainStart(w)}
        let gindex = i32(global_idx);
        let lindex = i32(local_idx);
        const wg = ${w};
        let row = gindex / wg;
        let cols = uniforms.packedCols;
        let row_stride : i32 = uniforms.packedCols;

        // find the rows max
        ${k}
        for (var col = lindex; col < cols; col += wg) {
          let value = getValue(row, col, row_stride);
          threadMax = max(threadMax, value);
        }
        if (lindex < cols) {
          threadShared[lindex] = threadMax;
        }
        workgroupBarrier();

        var reduceSize = min(cols, wg);
        for (var currSize = reduceSize >> 1;  currSize > 0; currSize = reduceSize >> 1) {
          reduceSize = currSize + (reduceSize & 1);
          if (lindex < currSize) {
            threadShared[lindex] = max(threadShared[lindex], threadShared[lindex + reduceSize]);
          }
          workgroupBarrier();
        }
        if (lindex == 0) {
          rowMaxShared = ${I}(${S("threadShared[0]",y)});
        }
        workgroupBarrier();

        // find the rows sum
        var threadSum = ${I}(0.0);
        for (var col = lindex; col < cols; col += wg) {
          let subExp = exp(getValue(row, col, row_stride) - rowMaxShared);
          threadSum += subExp;
        }
        threadShared[lindex] = threadSum;
        workgroupBarrier();

        for (var currSize = wg >> 1;  currSize > 0; currSize = currSize >> 1) {
          if (lindex < currSize) {
            threadShared[lindex] = threadShared[lindex] + threadShared[lindex + currSize];
          }
          workgroupBarrier();
        }
        if (lindex == 0) {
          rowSumShared = ${I}(${lt("threadShared[0]",y)});
        }
        workgroupBarrier();

        // calculate final value for each element in the row
        for (var col = lindex; col < cols; col += wg) {
          var value = exp(getValue(row, col, row_stride) - rowMaxShared) / rowSumShared;
          // max operation protects against NaN since all values should be >=0
          value = max(value, ${I}(0.0));
          setValue(row, col, row_stride, value);
        }
      }`,A=e.compute({name:"Softmax",shaderCache:{hint:`${y};${w}`,inputDependencies:["type"]},getRunData:()=>({outputs:[{dims:h,dataType:l.dataType}],dispatchGroup:{x:g},programUniforms:[{type:6,data:_}]}),getShaderSource:E},{inputs:[l],outputs:[u?-1:0]})[0];u&&e.compute(Ne(A,p),{inputs:[A]})},Kp=(e,t)=>{Fp(e.inputs),jp(e,t)},Qp=e=>he({axis:e.axis})}),Ca,Zp,Yp,Xp,Jp,Vm=q(()=>{te(),re(),ae(),Ca=e=>Array.from(e.getBigInt64Array(),Number),Zp=e=>{if(!e||e.length!==2)throw new Error("Tile requires 2 inputs.");if(e[0].dataType!==1&&e[0].dataType!==10&&e[0].dataType!==6&&e[0].dataType!==12)throw new Error("Tile only support float, float16, int32, and uint32 data types");if(e[1].dataType!==7)throw new Error("Tile `repeats` input should be of int64 data type");if(e[1].dims.length!==1)throw new Error("Tile `repeats` input should be 1-D");if(Ca(e[1]).length!==e[0].dims.length)throw new Error("Tile `repeats` input should have same number of elements as rank of input data tensor")},Yp=(e,t)=>{let r=[];for(let i=0;i<e.length;++i)r.push(e[i]*t[i]);return r},Xp=(e,t)=>{let r=e[0].dims,i=t??Ca(e[1]),a=Yp(r,i),n=O.size(a),s=e[0].dataType,u=M("input",s,r.length),l=Q("output",s,a.length),p=h=>`
      const inputShape = ${u.indices(...r)};
      ${h.registerUniform("output_size","u32").declareVariables(u,l)}
      ${h.mainStart()}
      ${h.guardAgainstOutOfBoundsWorkgroupSizes("uniforms.output_size")}
      let output_indices = ${l.offsetToIndices("global_idx")};
      var input_indices: ${u.type.indices};
      for (var i = 0; i < ${r.length}; i++) {
        let input_dim_i = ${u.indicesGet("uniforms.input_shape","i")};
        let input_dim_value = ${l.indicesGet("output_indices","i")}  % input_dim_i;

        ${u.indicesSet("input_indices","i","input_dim_value")}
      }
      ${l.setByOffset("global_idx",u.getByIndices("input_indices"))}
    }`;return{name:"Tile",shaderCache:{hint:`${i}`,inputDependencies:["rank"]},getRunData:()=>({outputs:[{dims:a,dataType:e[0].dataType}],dispatchGroup:{x:Math.ceil(n/64)},programUniforms:[{type:12,data:n},...Y(e[0].dims,a)]}),getShaderSource:p}},Jp=e=>{Zp(e.inputs),e.compute(Xp(e.inputs),{inputs:[0]})}}),ec,tc,rc,Gm=q(()=>{te(),re(),ae(),ec=(e,t,r,i,a)=>{let n=Q("output_data",a,r.length,4),s=M("a_data",t[1].dataType,t[1].dims.length,4),u=M("b_data",t[2].dataType,t[2].dims.length,4),l=M("c_data",t[0].dataType,t[0].dims.length,4),p,h=(f,g,y)=>`select(${g}, ${f}, ${y})`;if(!i)p=n.setByOffset("global_idx",h(s.getByOffset("global_idx"),u.getByOffset("global_idx"),l.getByOffset("global_idx")));else{let f=(g,y,_="")=>{let w=`a_data[index_a${y}][component_a${y}]`,S=`b_data[index_b${y}][component_b${y}]`,x=`bool(c_data[index_c${y}] & (0xffu << (component_c${y} * 8)))`;return`
            let output_indices${y} = ${n.offsetToIndices(`global_idx * 4u + ${y}u`)};
            let offset_a${y} = ${s.broadcastedIndicesToOffset(`output_indices${y}`,n)};
            let offset_b${y} = ${u.broadcastedIndicesToOffset(`output_indices${y}`,n)};
            let offset_c${y} = ${l.broadcastedIndicesToOffset(`output_indices${y}`,n)};
            let index_a${y} = offset_a${y} / 4u;
            let index_b${y} = offset_b${y} / 4u;
            let index_c${y} = offset_c${y} / 4u;
            let component_a${y} = offset_a${y} % 4u;
            let component_b${y} = offset_b${y} % 4u;
            let component_c${y} = offset_c${y} % 4u;
            ${g}[${y}] = ${_}(${h(w,S,x)});
          `};a===9?p=`
            var data = vec4<u32>(0);
            ${f("data",0,"u32")}
            ${f("data",1,"u32")}
            ${f("data",2,"u32")}
            ${f("data",3,"u32")}
            output_data[global_idx] = dot(vec4<u32>(0x1, 0x100, 0x10000, 0x1000000), vec4<u32>(data));`:p=`
            ${f("output_data[global_idx]",0)}
            ${f("output_data[global_idx]",1)}
            ${f("output_data[global_idx]",2)}
            ${f("output_data[global_idx]",3)}
          `}return`
        ${e.registerUniform("vec_size","u32").declareVariables(l,s,u,n)}
        ${e.mainStart()}
        ${e.guardAgainstOutOfBoundsWorkgroupSizes("uniforms.vec_size")}
        ${p}
      }`},tc=e=>{let t=e[1].dims,r=e[2].dims,i=e[0].dims,a=e[1].dataType,n=!(O.areEqual(t,r)&&O.areEqual(r,i)),s=t,u=O.size(t);if(n){let p=Lt.calcShape(Lt.calcShape(t,r,!1),i,!1);if(!p)throw new Error("Can't perform where op on the given tensors");s=p,u=O.size(s)}let l=Math.ceil(u/4);return{name:"Where",shaderCache:{inputDependencies:["rank","rank","rank"]},getShaderSource:p=>ec(p,e,s,n,a),getRunData:()=>({outputs:[{dims:s,dataType:a}],dispatchGroup:{x:Math.ceil(u/64/4)},programUniforms:[{type:12,data:l},...Y(i,t,r,s)]})}},rc=e=>{e.compute(tc(e.inputs))}}),ic,Hm=q(()=>{nm(),Fi(),sm(),om(),um(),lm(),dm(),mm(),ym(),_m(),wm(),bm(),$m(),vm(),xm(),Sm(),Tm(),km(),Im(),Em(),zm(),Cm(),Am(),Om(),Rm(),md(),Bm(),Mm(),Nm(),Dm(),Um(),Vi(),Pm(),Td(),qm(),Lm(),Wm(),vd(),Vm(),dt(),Zi(),Gm(),ic=new Map([["Abs",[Do]],["Acos",[Uo]],["Acosh",[Po]],["Add",[ku]],["ArgMax",[vo,Hi]],["ArgMin",[$o,Hi]],["Asin",[qo]],["Asinh",[Lo]],["Atan",[Wo]],["Atanh",[Vo]],["Attention",[Eo]],["AveragePool",[tp,ep]],["BatchNormalization",[Oo]],["BiasAdd",[Mo]],["BiasSplitGelu",[xu]],["Cast",[Ho,Go]],["Ceil",[Ko]],["Clip",[jo]],["Concat",[qu,Lu]],["Conv",[la,oa]],["ConvTranspose",[fl,pl]],["Cos",[Qo]],["Cosh",[Zo]],["CumSum",[gl,yl]],["DepthToSpace",[$l,vl]],["DequantizeLinear",[dp,pp]],["Div",[Iu]],["Einsum",[El,zl]],["Elu",[Yo,tr]],["Equal",[Eu]],["Erf",[Xo]],["Exp",[Jo]],["Expand",[Rl]],["FastGelu",[Ml]],["Floor",[eu]],["FusedConv",[la,oa]],["Gather",[Pl,Ul]],["GatherElements",[Zl,Ql]],["GatherBlockQuantized",[Hl,Fl]],["GatherND",[Ll,Wl]],["Gelu",[tu]],["Gemm",[ed,Jl]],["GlobalAveragePool",[ip,rp]],["GlobalMaxPool",[op,sp]],["Greater",[Ou]],["GreaterOrEqual",[Bu]],["GridSample",[ld,dd]],["GroupQueryAttention",[zd]],["HardSigmoid",[lu,uu]],["InstanceNormalization",[Od]],["LayerNormalization",[Md]],["LeakyRelu",[ru,tr]],["Less",[Ru]],["LessOrEqual",[Mu]],["Log",[yu]],["MatMul",[Dd]],["MatMulNBits",[Ld,Wd]],["MaxPool",[ap,np]],["Mul",[zu]],["MultiHeadAttention",[fd,cd]],["Neg",[au]],["Not",[iu]],["Pad",[Yd]],["Pow",[Cu]],["QuickGelu",[bu,tr]],["Range",[fp]],["Reciprocal",[nu]],["ReduceMin",[go]],["ReduceMean",[po]],["ReduceMax",[mo]],["ReduceSum",[_o]],["ReduceProd",[yo]],["ReduceL1",[co]],["ReduceL2",[ho]],["ReduceLogSum",[bo]],["ReduceLogSumExp",[fo]],["ReduceSumSquare",[wo]],["Relu",[su]],["Resize",[Mp,Np]],["RotaryEmbedding",[Sd]],["ScatterND",[_p,yp]],["Sigmoid",[ou]],["Sin",[du]],["Sinh",[pu]],["Slice",[Gp,Hp]],["SkipLayerNormalization",[Pp]],["Split",[bd,$d]],["Sqrt",[cu]],["Softmax",[Kp,Qp]],["Sub",[Au]],["Tan",[hu]],["Tanh",[fu]],["ThresholdedRelu",[gu,tr]],["Tile",[Jp]],["Transpose",[As,Os]],["Where",[rc]]])}),ac,Fm=q(()=>{Pe(),at(),ae(),ac=class{constructor(e){this.backend=e,this.repo=new Map,this.attributesBound=!1}getArtifact(e){return this.repo.get(e)}setArtifact(e,t){this.repo.set(e,t)}run(e,t,r,i,a){Qe(e.programInfo.name);let n=this.backend.device,s=this.backend.getComputePassEncoder();this.backend.writeTimestamp(this.backend.pendingDispatchNumber*2);let u=[];for(let p of t)u.push({binding:u.length,resource:{buffer:p.buffer}});for(let p of r)u.push({binding:u.length,resource:{buffer:p.buffer}});a&&u.push({binding:u.length,resource:a});let l=n.createBindGroup({layout:e.computePipeline.getBindGroupLayout(0),entries:u,label:e.programInfo.name});if(this.backend.sessionStatus==="capturing"){let p={kernelId:this.backend.currentKernelId,computePipeline:e.computePipeline,bindGroup:l,dispatchGroup:i};this.backend.capturedCommandList.get(this.backend.currentSessionId).push(p)}s.setPipeline(e.computePipeline),s.setBindGroup(0,l),s.dispatchWorkgroups(...i),this.backend.writeTimestamp(this.backend.pendingDispatchNumber*2+1),this.backend.pendingDispatchNumber++,(this.backend.pendingDispatchNumber>=this.backend.maxDispatchNumber||this.backend.queryType==="at-passes")&&this.backend.endComputePass(),this.backend.pendingDispatchNumber>=this.backend.maxDispatchNumber&&this.backend.flush(),Le(e.programInfo.name)}dispose(){}build(e,t){Qe(e.name);let r=this.backend.device,i=[];[{feature:"shader-f16",extension:"f16"},{feature:"subgroups",extension:"subgroups"}].forEach(p=>{r.features.has(p.feature)&&i.push(`enable ${p.extension};`)});let a=Ts(t,this.backend.device.limits),n=e.getShaderSource(a),s=`${i.join(`
`)}
${a.additionalImplementations}
${n}`,u=r.createShaderModule({code:s,label:e.name});de("verbose",()=>`[WebGPU] ${e.name} shader code: ${s}`);let l=r.createComputePipeline({compute:{module:u,entryPoint:"main"},layout:"auto",label:e.name});return Le(e.name),{programInfo:e,computePipeline:l,uniformVariablesInfo:a.variablesInfo}}normalizeDispatchGroupSize(e){let t=typeof e=="number"?e:e.x,r=typeof e=="number"?1:e.y||1,i=typeof e=="number"?1:e.z||1,a=this.backend.device.limits.maxComputeWorkgroupsPerDimension;if(t<=a&&r<=a&&i<=a)return[t,r,i];let n=t*r*i,s=Math.ceil(Math.sqrt(n));if(s>a){if(s=Math.ceil(Math.cbrt(n)),s>a)throw new Error("Total dispatch size exceeds WebGPU maximum.");return[s,s,s]}else return[s,s,1]}}}),nc={};Pt(nc,{WebGpuBackend:()=>lc});var sc,oc,uc,lc,jm=q(()=>{Pe(),te(),at(),ps(),im(),Hm(),Fm(),sc=(e,t)=>{if(t.length!==e.length)throw new Error(`inputDependencies length ${t.length} is not equal to inputTensors length ${e.length}.`);let r=[];for(let i=0;i<e.length;++i){let a=e[i].dataType;switch(t[i]){case"none":{r.push("");break}case"type":{r.push(`${a}`);break}case"rank":{let n=e[i].dims.length;r.push(`${a};${n}`);break}case"dims":{let n=e[i].dims.join(",");r.push(`${a};${n}`);break}default:throw new Error(`unsupported input dependency: ${t[i]}`)}}return r.join("|")},oc=(e,t,r)=>{var a,n;let i=e.name;return(a=e.shaderCache)!=null&&a.hint&&(i+="["+e.shaderCache.hint+"]"),i+=":"+r+`:${sc(t,((n=e.shaderCache)==null?void 0:n.inputDependencies)??new Array(t.length).fill("dims"))}`,i},uc=class{constructor(e){e&&(this.architecture=e.architecture,this.vendor=e.vendor)}isArchitecture(e){return this.architecture===e}isVendor(e){return this.vendor===e}},lc=class{constructor(){this.currentSessionId=null,this.currentKernelId=null,this.commandEncoder=null,this.computePassEncoder=null,this.maxDispatchNumber=16,this.pendingDispatchNumber=0,this.pendingKernels=[],this.pendingQueries=new Map,this.sessionStatus="default",this.capturedCommandList=new Map,this.capturedPendingKernels=new Map,this.sessionExternalDataMapping=new Map}get currentKernelCustomData(){if(this.currentKernelId===null)throw new Error("currentKernelCustomData(): currentKernelId is null. (should not happen)");let e=this.kernelCustomData.get(this.currentKernelId);return e||(e={},this.kernelCustomData.set(this.currentKernelId,e)),e}async initialize(e,t){this.env=e;let r=[],i={requiredLimits:{maxComputeWorkgroupStorageSize:t.limits.maxComputeWorkgroupStorageSize,maxComputeWorkgroupsPerDimension:t.limits.maxComputeWorkgroupsPerDimension,maxStorageBufferBindingSize:t.limits.maxStorageBufferBindingSize,maxBufferSize:t.limits.maxBufferSize,maxComputeInvocationsPerWorkgroup:t.limits.maxComputeInvocationsPerWorkgroup,maxComputeWorkgroupSizeX:t.limits.maxComputeWorkgroupSizeX,maxComputeWorkgroupSizeY:t.limits.maxComputeWorkgroupSizeY,maxComputeWorkgroupSizeZ:t.limits.maxComputeWorkgroupSizeZ},requiredFeatures:r},a=n=>t.features.has(n)&&r.push(n)&&!0;a("chromium-experimental-timestamp-query-inside-passes")||a("timestamp-query"),a("shader-f16"),a("subgroups"),this.device=await t.requestDevice(i),this.adapterInfo=new uc(t.info||await t.requestAdapterInfo()),this.gpuDataManager=$s(this),this.programManager=new ac(this),this.kernels=new Map,this.kernelPersistentData=new Map,this.kernelCustomData=new Map,ki(e.logLevel,!!e.debug),this.device.onuncapturederror=n=>{n.error instanceof GPUValidationError&&console.error(`An uncaught WebGPU validation error was raised: ${n.error.message}`)},Object.defineProperty(this.env.webgpu,"device",{value:this.device,writable:!1,enumerable:!0,configurable:!1}),Object.defineProperty(this.env.webgpu,"adapter",{value:t,writable:!1,enumerable:!0,configurable:!1}),this.setQueryType()}dispose(){typeof this.querySet<"u"&&this.querySet.destroy(),this.gpuDataManager.dispose()}getCommandEncoder(){return this.commandEncoder||(this.commandEncoder=this.device.createCommandEncoder()),this.commandEncoder}getComputePassEncoder(){if(!this.computePassEncoder){let e=this.getCommandEncoder(),t={};this.queryType==="at-passes"&&(t.timestampWrites={querySet:this.querySet,beginningOfPassWriteIndex:this.pendingDispatchNumber*2,endOfPassWriteIndex:this.pendingDispatchNumber*2+1}),this.computePassEncoder=e.beginComputePass(t)}return this.computePassEncoder}endComputePass(){this.computePassEncoder&&(this.computePassEncoder.end(),this.computePassEncoder=null)}flush(){if(!this.commandEncoder)return;Qe(),this.endComputePass();let e;this.queryType!=="none"&&(this.commandEncoder.resolveQuerySet(this.querySet,0,this.pendingDispatchNumber*2,this.queryResolveBuffer,0),e=this.device.createBuffer({size:this.pendingDispatchNumber*2*8,usage:GPUBufferUsage.MAP_READ|GPUBufferUsage.COPY_DST}),this.pendingQueries.set(e,this.pendingKernels),this.pendingKernels=[],this.commandEncoder.copyBufferToBuffer(this.queryResolveBuffer,0,e,0,this.pendingDispatchNumber*2*8)),this.device.queue.submit([this.commandEncoder.finish()]),this.gpuDataManager.refreshPendingBuffers(),this.commandEncoder=null,this.pendingDispatchNumber=0,this.queryType!=="none"&&e.mapAsync(GPUMapMode.READ).then(()=>{var i;let t=new BigUint64Array(e.getMappedRange()),r=this.pendingQueries.get(e);for(let a=0;a<t.length/2;a++){let n=r[a],s=n.kernelId,u=this.kernels.get(s),l=u.kernelType,p=u.kernelName,h=n.programName,f=n.inputTensorViews,g=n.outputTensorViews,y=t[a*2],_=t[a*2+1];typeof this.queryTimeBase>"u"&&(this.queryTimeBase=y);let w=Number(y-this.queryTimeBase),S=Number(_-this.queryTimeBase);if(!Number.isSafeInteger(w)||!Number.isSafeInteger(S))throw new RangeError("incorrect timestamp range");if((i=this.env.webgpu.profiling)!=null&&i.ondata)this.env.webgpu.profiling.ondata({version:1,inputsMetadata:f.map(x=>({dims:x.dims,dataType:it(x.dataType)})),outputsMetadata:g.map(x=>({dims:x.dims,dataType:it(x.dataType)})),kernelId:s,kernelType:l,kernelName:p,programName:h,startTime:w,endTime:S});else{let x="";f.forEach((I,k)=>{x+=`input[${k}]: [${I.dims}] | ${it(I.dataType)}, `});let b="";g.forEach((I,k)=>{b+=`output[${k}]: [${I.dims}] | ${it(I.dataType)}, `}),console.log(`[profiling] kernel "${s}|${l}|${p}|${h}" ${x}${b}start time: ${w} ns, execution time: ${S-w} ns`)}wr("GPU",`${h}::${y}::${_}`)}e.unmap(),this.pendingQueries.delete(e)}),Le()}run(e,t,r,i,a,n){Qe(e.name);let s=[];for(let b=0;b<t.length;++b){let I=t[b].data;if(I===0)continue;let k=this.gpuDataManager.get(I);if(!k)throw new Error(`no GPU data for input: ${I}`);s.push(k)}let{outputs:u,dispatchGroup:l,programUniforms:p}=e.getRunData(t),h=r.length===0?u.map((b,I)=>I):r;if(h.length!==u.length)throw new Error(`Output size ${h.length} must be equal to ${u.length}.`);let f=[],g=[];for(let b=0;b<u.length;++b){if(!Number.isInteger(h[b])||h[b]<-3||h[b]>=n)throw new Error(`Invalid output index: ${h[b]}`);if(h[b]===-3)continue;let I=h[b]===-1,k=h[b]===-2,E=I||k?a(u[b].dataType,u[b].dims):i(h[b],u[b].dataType,u[b].dims);if(f.push(E),E.data===0)continue;let A=this.gpuDataManager.get(E.data);if(!A)throw new Error(`no GPU data for output: ${E.data}`);if(I&&this.temporaryData.push(A),k){let C=this.kernelPersistentData.get(this.currentKernelId);C||(C=[],this.kernelPersistentData.set(this.currentKernelId,C)),C.push(A)}g.push(A)}if(s.length!==t.length||g.length!==f.length){if(g.length===0)return Le(e.name),f;throw new Error(`Program ${e.name} has zero-sized tensor(s) in inputs or outputs. This is not supported now.`)}let y;if(p){let b=0,I=[];p.forEach(C=>{let $=typeof C.data=="number"?[C.data]:C.data;if($.length===0)return;let N=C.type===10?2:4,D,G;C.type===10?(G=$.length>4?16:$.length>2?8:$.length*N,D=$.length>4?16:N*$.length):(G=$.length<=2?$.length*N:16,D=16),b=Math.ceil(b/G)*G,I.push(b);let V=C.type===10?8:4;b+=$.length>4?Math.ceil($.length/V)*D:$.length*N});let k=16;b=Math.ceil(b/k)*k;let E=new ArrayBuffer(b);p.forEach((C,$)=>{let N=I[$],D=typeof C.data=="number"?[C.data]:C.data;if(C.type===6)new Int32Array(E,N,D.length).set(D);else if(C.type===12)new Uint32Array(E,N,D.length).set(D);else if(C.type===10)new Uint16Array(E,N,D.length).set(D);else if(C.type===1)new Float32Array(E,N,D.length).set(D);else throw new Error(`Unsupported uniform type: ${it(C.type)}`)});let A=this.gpuDataManager.create(b,GPUBufferUsage.COPY_DST|GPUBufferUsage.UNIFORM);this.device.queue.writeBuffer(A.buffer,0,E,0,b),this.gpuDataManager.release(A.id),y={offset:0,size:b,buffer:A.buffer}}let _=this.programManager.normalizeDispatchGroupSize(l),w=_[1]===1&&_[2]===1,S=oc(e,t,w),x=this.programManager.getArtifact(S);if(x||(x=this.programManager.build(e,_),this.programManager.setArtifact(S,x),de("info",()=>`[artifact] key: ${S}, programName: ${e.name}`)),p&&x.uniformVariablesInfo){if(p.length!==x.uniformVariablesInfo.length)throw new Error(`Uniform variables count mismatch: expect ${x.uniformVariablesInfo.length}, got ${p.length} in program "${x.programInfo.name}".`);for(let b=0;b<p.length;b++){let I=p[b],k=I.type,E=typeof I.data=="number"?1:I.data.length,[A,C]=x.uniformVariablesInfo[b];if(k!==A||E!==C)throw new Error(`Uniform variable ${b} mismatch: expect type ${A} with size ${C}, got type ${k} with size ${E} in program "${x.programInfo.name}".`)}}if(de("info",()=>`[ProgramManager] run "${e.name}" (key=${S}) with ${_[0]}x${_[1]}x${_[2]}`),this.queryType!=="none"||this.sessionStatus==="capturing"){let b={kernelId:this.currentKernelId,programName:x.programInfo.name,inputTensorViews:t,outputTensorViews:f};this.pendingKernels.push(b),this.sessionStatus==="capturing"&&this.capturedPendingKernels.get(this.currentSessionId).push(b)}return this.programManager.run(x,s,g,_,y),Le(e.name),f}upload(e,t){this.gpuDataManager.upload(e,t)}memcpy(e,t){this.gpuDataManager.memcpy(e,t)}async download(e,t){await this.gpuDataManager.download(e,t)}alloc(e){return this.gpuDataManager.create(e).id}free(e){return this.gpuDataManager.release(e)}createKernel(e,t,r,i){let a=ic.get(e);if(!a)throw new Error(`kernel not implemented: ${e}`);let n={kernelType:e,kernelName:i,kernelEntry:a[0],attributes:[a[1],r]};this.kernels.set(t,n)}releaseKernel(e){let t=this.kernelPersistentData.get(e);if(t){for(let r of t)this.gpuDataManager.release(r.id);this.kernelPersistentData.delete(e)}this.kernelCustomData.delete(e),this.kernels.delete(e)}computeKernel(e,t,r){let i=this.kernels.get(e);if(!i)throw new Error(`kernel not created: ${e}`);let a=i.kernelType,n=i.kernelName,s=i.kernelEntry,u=i.attributes;if(this.currentKernelId!==null)throw new Error(`kernel "[${a}] ${n}" is not allowed to be called recursively`);this.currentKernelId=e,u[0]&&(u[1]=u[0](u[1]),u[0]=void 0),de("info",()=>`[WebGPU] Start to run kernel "[${a}] ${n}"...`);let l=this.env.debug;this.temporaryData=[];try{return l&&this.device.pushErrorScope("validation"),s(t,u[1]),0}catch(p){return r.push(Promise.resolve(`[WebGPU] Kernel "[${a}] ${n}" failed. ${p}`)),1}finally{l&&r.push(this.device.popErrorScope().then(p=>p?`GPU validation error for kernel "[${a}] ${n}": ${p.message}`:null));for(let p of this.temporaryData)this.gpuDataManager.release(p.id);this.temporaryData=[],this.currentKernelId=null}}registerBuffer(e,t,r,i){let a=this.sessionExternalDataMapping.get(e);a||(a=new Map,this.sessionExternalDataMapping.set(e,a));let n=a.get(t),s=this.gpuDataManager.registerExternalBuffer(r,i,n);return a.set(t,[s,r]),s}unregisterBuffers(e){let t=this.sessionExternalDataMapping.get(e);t&&(t.forEach(r=>this.gpuDataManager.unregisterExternalBuffer(r[0])),this.sessionExternalDataMapping.delete(e))}getBuffer(e){let t=this.gpuDataManager.get(e);if(!t)throw new Error(`no GPU data for buffer: ${e}`);return t.buffer}createDownloader(e,t,r){return async()=>{let i=await Ui(this,e,t);return Ii(i.buffer,r)}}writeTimestamp(e){this.queryType==="inside-passes"&&this.computePassEncoder.writeTimestamp(this.querySet,e)}setQueryType(){var e;this.queryType="none",(((e=this.env.webgpu.profiling)==null?void 0:e.mode)==="default"||(typeof this.env.trace>"u"?this.env.wasm.trace:this.env.trace))&&(this.device.features.has("chromium-experimental-timestamp-query-inside-passes")?this.queryType="inside-passes":this.device.features.has("timestamp-query")&&(this.queryType="at-passes"),this.queryType!=="none"&&typeof this.querySet>"u"&&(this.querySet=this.device.createQuerySet({type:"timestamp",count:this.maxDispatchNumber*2}),this.queryResolveBuffer=this.device.createBuffer({size:this.maxDispatchNumber*2*8,usage:GPUBufferUsage.COPY_SRC|GPUBufferUsage.QUERY_RESOLVE})))}captureBegin(){de("info","captureBegin"),this.capturedCommandList.get(this.currentSessionId)||this.capturedCommandList.set(this.currentSessionId,[]),this.capturedPendingKernels.get(this.currentSessionId)||this.capturedPendingKernels.set(this.currentSessionId,[]),this.flush(),this.sessionStatus="capturing"}captureEnd(){de("info","captureEnd"),this.flush(),this.sessionStatus="default"}replay(){de("info","replay"),this.sessionStatus="replaying";let e=this.capturedCommandList.get(this.currentSessionId),t=this.capturedPendingKernels.get(this.currentSessionId),r=e.length;this.pendingKernels=[];for(let i=0;i<r;i++){let a=this.getComputePassEncoder(),n=e[i];this.writeTimestamp(this.pendingDispatchNumber*2),a.setPipeline(n.computePipeline),a.setBindGroup(0,n.bindGroup),a.dispatchWorkgroups(...n.dispatchGroup),this.writeTimestamp(this.pendingDispatchNumber*2+1),this.pendingDispatchNumber++,this.queryType!=="none"&&this.pendingKernels.push(t[i]),(this.pendingDispatchNumber>=this.maxDispatchNumber||this.queryType==="at-passes")&&this.endComputePass(),this.pendingDispatchNumber>=this.maxDispatchNumber&&this.flush()}this.flush(),this.sessionStatus="default"}onCreateSession(){this.gpuDataManager.onCreateSession()}onReleaseSession(e){this.unregisterBuffers(e),this.capturedCommandList.has(e)&&this.capturedCommandList.delete(e),this.capturedPendingKernels.has(e)&&this.capturedPendingKernels.delete(e),this.gpuDataManager.onReleaseSession(e)}onRunStart(e){this.currentSessionId=e,this.setQueryType()}}}),dc={};Pt(dc,{init:()=>cc});var Ur,pc,cc,Km=q(()=>{te(),at(),re(),rm(),Ur=class Rf{constructor(t,r,i,a){this.module=t,this.dataType=r,this.data=i,this.dims=a}getFloat32Array(){if(this.dataType!==1)throw new Error("Invalid data type");let t=O.size(this.dims);return t===0?new Float32Array:new Float32Array(this.module.HEAP8.buffer,this.data,t)}getBigInt64Array(){if(this.dataType!==7)throw new Error("Invalid data type");let t=O.size(this.dims);return t===0?new BigInt64Array:new BigInt64Array(this.module.HEAP8.buffer,this.data,t)}getInt32Array(){if(this.dataType!==6)throw new Error("Invalid data type");let t=O.size(this.dims);return t===0?new Int32Array:new Int32Array(this.module.HEAP8.buffer,this.data,t)}getUint16Array(){if(this.dataType!==10&&this.dataType!==4)throw new Error("Invalid data type");let t=O.size(this.dims);return t===0?new Uint16Array:new Uint16Array(this.module.HEAP8.buffer,this.data,t)}reshape(t){if(O.size(t)!==O.size(this.dims))throw new Error("Invalid new shape");return new Rf(this.module,this.dataType,this.data,t)}},pc=class{constructor(e,t,r){this.module=e,this.backend=t,this.customDataOffset=0,this.customDataSize=0,this.adapterInfo=t.adapterInfo;let i=e.PTR_SIZE,a=r/e.PTR_SIZE,n=i===4?"i32":"i64";this.opKernelContext=Number(e.getValue(i*a++,n));let s=Number(e.getValue(i*a++,n));this.outputCount=Number(e.getValue(i*a++,n)),this.customDataOffset=Number(e.getValue(i*a++,"*")),this.customDataSize=Number(e.getValue(i*a++,n));let u=[];for(let l=0;l<s;l++){let p=Number(e.getValue(i*a++,n)),h=Number(e.getValue(i*a++,"*")),f=Number(e.getValue(i*a++,n)),g=[];for(let y=0;y<f;y++)g.push(Number(e.getValue(i*a++,n)));u.push(new Ur(e,p,h,g))}this.inputs=u}get kernelCustomData(){return this.backend.currentKernelCustomData}get customDataBuffer(){return this.module.HEAPU8.subarray(this.customDataOffset,this.customDataOffset+this.customDataSize)}compute(e,t){var s;let r=((s=t==null?void 0:t.inputs)==null?void 0:s.map(u=>typeof u=="number"?this.inputs[u]:u))??this.inputs,i=(t==null?void 0:t.outputs)??[],a=(u,l,p)=>new Ur(this.module,l,this.output(u,p),p),n=(u,l)=>{let p=kt(u,l);if(!p)throw new Error(`Unsupported data type: ${u}`);let h=p>0?this.backend.gpuDataManager.create(p).id:0;return new Ur(this.module,u,h,l)};return this.backend.run(e,r,i,a,n,this.outputCount)}output(e,t){let r=this.module.stackSave();try{let i=this.module.PTR_SIZE,a=i===4?"i32":"i64",n=this.module.stackAlloc((1+t.length)*i);this.module.setValue(n,t.length,a);for(let s=0;s<t.length;s++)this.module.setValue(n+i*(s+1),t[s],a);return this.module._JsepOutput(this.opKernelContext,e,n)}catch(i){throw new Error(`Failed to generate kernel's output[${e}] with dims [${t}]. If you are running with pre-allocated output, please make sure the output type/dims are correct. Error: ${i}`)}finally{this.module.stackRestore(r)}}},cc=async(e,t,r,i)=>{let a=t.jsepInit;if(!a)throw new Error("Failed to initialize JSEP. The WebAssembly module is not built with JSEP support.");if(e==="webgpu"){let n=(jm(),jt(nc)).WebGpuBackend,s=new n;await s.initialize(r,i),a("webgpu",[s,u=>s.alloc(Number(u)),u=>s.free(u),(u,l,p,h=!1)=>{if(h)de("verbose",()=>`[WebGPU] jsepCopyGpuToGpu: src=${Number(u)}, dst=${Number(l)}, size=${Number(p)}`),s.memcpy(Number(u),Number(l));else{de("verbose",()=>`[WebGPU] jsepCopyCpuToGpu: dataOffset=${Number(u)}, gpuDataId=${Number(l)}, size=${Number(p)}`);let f=t.HEAPU8.subarray(Number(u>>>0),Number(u>>>0)+Number(p));s.upload(Number(l),f)}},async(u,l,p)=>{de("verbose",()=>`[WebGPU] jsepCopyGpuToCpu: gpuDataId=${u}, dataOffset=${l}, size=${p}`),await s.download(Number(u),()=>t.HEAPU8.subarray(Number(l)>>>0,Number(l+p)>>>0))},(u,l,p)=>s.createKernel(u,Number(l),p,t.UTF8ToString(t._JsepGetNodeName(Number(l)))),u=>s.releaseKernel(u),(u,l,p,h)=>{de("verbose",()=>`[WebGPU] jsepRun: sessionHandle=${p}, kernel=${u}, contextDataOffset=${l}`);let f=new pc(t,s,Number(l));return s.computeKernel(Number(u),f,h)},()=>s.captureBegin(),()=>s.captureEnd(),()=>s.replay()])}else{let n=new ys(r);a("webnn",[n,()=>n.reserveTensorId(),s=>n.releaseTensorId(s),async(s,u,l,p,h)=>n.ensureTensor(s,u,l,p,h),(s,u)=>{n.uploadTensor(s,u)},async(s,u)=>n.downloadTensor(s,u),(s,u)=>n.registerMLContext(s,u),!!r.trace])}}}),hc,Aa,Oa,pt,fc,Ra,Pr,Ba,Ma,Na,Da,Ua,Pa,mc=q(()=>{Pe(),Jf(),em(),te(),St(),$i(),ts(),hc=(e,t)=>{_e()._OrtInit(e,t)!==0&&fe("Can't initialize onnxruntime.")},Aa=async e=>{hc(e.wasm.numThreads,Tr(e.logLevel))},Oa=async(e,t)=>{var i,a;(a=(i=_e()).asyncInit)==null||a.call(i);let r=e.webgpu.adapter;if(t==="webgpu"){if(typeof navigator>"u"||!navigator.gpu)throw new Error("WebGPU is not supported in current environment");if(r){if(typeof r.limits!="object"||typeof r.features!="object"||typeof r.requestDevice!="function")throw new Error("Invalid GPU adapter set in `env.webgpu.adapter`. It must be a GPUAdapter object.")}else{let n=e.webgpu.powerPreference;if(n!==void 0&&n!=="low-power"&&n!=="high-performance")throw new Error(`Invalid powerPreference setting: "${n}"`);let s=e.webgpu.forceFallbackAdapter;if(s!==void 0&&typeof s!="boolean")throw new Error(`Invalid forceFallbackAdapter setting: "${s}"`);if(r=await navigator.gpu.requestAdapter({powerPreference:n,forceFallbackAdapter:s}),!r)throw new Error('Failed to get GPU adapter. You may need to enable flag "--enable-unsafe-webgpu" if you are using Chrome.')}}if(t==="webnn"&&(typeof navigator>"u"||!navigator.ml))throw new Error("WebNN is not supported in current environment");{let n=(Km(),jt(dc)).init;t==="webgpu"&&await n("webgpu",_e(),e,r),t==="webnn"&&await n("webnn",_e(),e)}},pt=new Map,fc=e=>{let t=_e(),r=t.stackSave();try{let i=t.PTR_SIZE,a=t.stackAlloc(2*i);t._OrtGetInputOutputCount(e,a,a+i)!==0&&fe("Can't get session input/output count.");let n=i===4?"i32":"i64";return[Number(t.getValue(a,n)),Number(t.getValue(a+i,n))]}finally{t.stackRestore(r)}},Ra=(e,t)=>{let r=_e(),i=r.stackSave(),a=0;try{let n=r.PTR_SIZE,s=r.stackAlloc(2*n);r._OrtGetInputOutputMetadata(e,t,s,s+n)!==0&&fe("Can't get session input/output metadata.");let u=Number(r.getValue(s,"*"));a=Number(r.getValue(s+n,"*"));let l=r.HEAP32[a/4];if(l===0)return[u,0];let p=r.HEAPU32[a/4+1],h=[];for(let f=0;f<p;f++){let g=Number(r.getValue(a+8+f*n,"*"));h.push(g!==0?r.UTF8ToString(g):Number(r.getValue(a+8+(f+p)*n,"*")))}return[u,l,h]}finally{r.stackRestore(i),a!==0&&r._OrtFree(a)}},Pr=e=>{let t=_e(),r=t._malloc(e.byteLength);if(r===0)throw new Error(`Can't create a session. failed to allocate a buffer of size ${e.byteLength}.`);return t.HEAPU8.set(e,r),[r,e.byteLength]},Ba=async(e,t)=>{var f,g,y,_;let r,i,a=_e();Array.isArray(e)?[r,i]=e:e.buffer===a.HEAPU8.buffer?[r,i]=[e.byteOffset,e.byteLength]:[r,i]=Pr(e);let n=0,s=0,u=0,l=[],p=[],h=[];try{if([s,l]=await es(t),(t==null?void 0:t.externalData)&&a.mountExternalData){let $=[];for(let N of t.externalData){let D=typeof N=="string"?N:N.path;$.push(Ti(typeof N=="string"?N:N.data).then(G=>{a.mountExternalData(D,G)}))}await Promise.all($)}for(let $ of(t==null?void 0:t.executionProviders)??[])if((typeof $=="string"?$:$.name)==="webnn"){if(a.shouldTransferToMLTensor=!1,typeof $!="string"){let N=$,D=N==null?void 0:N.context,G=N==null?void 0:N.gpuDevice,V=N==null?void 0:N.deviceType,j=N==null?void 0:N.powerPreference;D?a.currentContext=D:G?a.currentContext=await a.webnnCreateMLContext(G):a.currentContext=await a.webnnCreateMLContext({deviceType:V,powerPreference:j})}else a.currentContext=await a.webnnCreateMLContext();break}n=await a._OrtCreateSession(r,i,s),(f=a.webgpuOnCreateSession)==null||f.call(a,n),n===0&&fe("Can't create a session."),(g=a.jsepOnCreateSession)==null||g.call(a),a.currentContext&&(a.webnnRegisterMLContext(n,a.currentContext),a.currentContext=void 0,a.shouldTransferToMLTensor=!0);let[w,S]=fc(n),x=!!(t!=null&&t.enableGraphCapture),b=[],I=[],k=[],E=[],A=[];for(let $=0;$<w;$++){let[N,D,G]=Ra(n,$);N===0&&fe("Can't get an input name."),p.push(N);let V=a.UTF8ToString(N);b.push(V),k.push(D===0?{name:V,isTensor:!1}:{name:V,isTensor:!0,type:it(D),shape:G})}for(let $=0;$<S;$++){let[N,D,G]=Ra(n,$+w);N===0&&fe("Can't get an output name."),h.push(N);let V=a.UTF8ToString(N);I.push(V),E.push(D===0?{name:V,isTensor:!1}:{name:V,isTensor:!0,type:it(D),shape:G});{if(x&&(t==null?void 0:t.preferredOutputLocation)===void 0){A.push("gpu-buffer");continue}let j=typeof(t==null?void 0:t.preferredOutputLocation)=="string"?t.preferredOutputLocation:((y=t==null?void 0:t.preferredOutputLocation)==null?void 0:y[V])??"cpu",R=a.webnnIsGraphOutput;if(j==="cpu"&&R&&R(n,V)){A.push("ml-tensor-cpu-output");continue}if(j!=="cpu"&&j!=="cpu-pinned"&&j!=="gpu-buffer"&&j!=="ml-tensor")throw new Error(`Not supported preferred output location: ${j}.`);if(x&&j!=="gpu-buffer")throw new Error(`Not supported preferred output location: ${j}. Only 'gpu-buffer' location is supported when enableGraphCapture is true.`);A.push(j)}}let C=null;return A.some($=>$==="gpu-buffer"||$==="ml-tensor"||$==="ml-tensor-cpu-output")&&(u=a._OrtCreateBinding(n),u===0&&fe("Can't create IO binding."),C={handle:u,outputPreferredLocations:A,outputPreferredLocationsEncoded:A.map($=>$==="ml-tensor-cpu-output"?"ml-tensor":$).map($=>Si($))}),pt.set(n,[n,p,h,C,x,!1]),[n,b,I,k,E]}catch(w){throw p.forEach(S=>a._OrtFree(S)),h.forEach(S=>a._OrtFree(S)),u!==0&&a._OrtReleaseBinding(u)!==0&&fe("Can't release IO binding."),n!==0&&a._OrtReleaseSession(n)!==0&&fe("Can't release session."),w}finally{a._free(r),s!==0&&a._OrtReleaseSessionOptions(s)!==0&&fe("Can't release session options."),l.forEach(w=>a._free(w)),(_=a.unmountExternalData)==null||_.call(a)}},Ma=e=>{var l,p,h;let t=_e(),r=pt.get(e);if(!r)throw new Error(`cannot release session. invalid session id: ${e}`);let[i,a,n,s,u]=r;s&&(u&&t._OrtClearBoundOutputs(s.handle)!==0&&fe("Can't clear bound outputs."),t._OrtReleaseBinding(s.handle)!==0&&fe("Can't release IO binding.")),(l=t.jsepOnReleaseSession)==null||l.call(t,e),(p=t.webnnOnReleaseSession)==null||p.call(t,e),(h=t.webgpuOnReleaseSession)==null||h.call(t,e),a.forEach(f=>t._OrtFree(f)),n.forEach(f=>t._OrtFree(f)),t._OrtReleaseSession(i)!==0&&fe("Can't release session."),pt.delete(e)},Na=async(e,t,r,i,a,n,s=!1)=>{if(!e){t.push(0);return}let u=_e(),l=u.PTR_SIZE,p=e[0],h=e[1],f=e[3],g=f,y,_;if(p==="string"&&(f==="gpu-buffer"||f==="ml-tensor"))throw new Error("String tensor is not supported on GPU.");if(s&&f!=="gpu-buffer")throw new Error(`External buffer must be provided for input/output index ${n} when enableGraphCapture is true.`);if(f==="gpu-buffer"){let x=e[2].gpuBuffer;_=kt(Tt(p),h);{let b=u.jsepRegisterBuffer;if(!b)throw new Error('Tensor location "gpu-buffer" is not supported without using WebGPU.');y=b(i,n,x,_)}}else if(f==="ml-tensor"){let x=e[2].mlTensor;_=kt(Tt(p),h);let b=u.webnnRegisterMLTensor;if(!b)throw new Error('Tensor location "ml-tensor" is not supported without using WebNN.');y=b(i,x,Tt(p),h)}else{let x=e[2];if(Array.isArray(x)){_=l*x.length,y=u._malloc(_),r.push(y);for(let b=0;b<x.length;b++){if(typeof x[b]!="string")throw new TypeError(`tensor data at index ${b} is not a string`);u.setValue(y+b*l,We(x[b],r),"*")}}else{let b=u.webnnIsGraphInput,I=u.webnnIsGraphOutput;if(p!=="string"&&b&&I){let k=u.UTF8ToString(a);if(b(i,k)||I(i,k)){let E=Tt(p);_=kt(E,h),g="ml-tensor";let A=u.webnnCreateTemporaryTensor,C=u.webnnUploadTensor;if(!A||!C)throw new Error('Tensor location "ml-tensor" is not supported without using WebNN.');let $=await A(i,E,h);C($,new Uint8Array(x.buffer,x.byteOffset,x.byteLength)),y=$}else _=x.byteLength,y=u._malloc(_),r.push(y),u.HEAPU8.set(new Uint8Array(x.buffer,x.byteOffset,_),y)}else _=x.byteLength,y=u._malloc(_),r.push(y),u.HEAPU8.set(new Uint8Array(x.buffer,x.byteOffset,_),y)}}let w=u.stackSave(),S=u.stackAlloc(4*h.length);try{h.forEach((b,I)=>u.setValue(S+I*l,b,l===4?"i32":"i64"));let x=u._OrtCreateTensor(Tt(p),y,_,S,h.length,Si(g));x===0&&fe(`Can't create tensor for input/output. session=${i}, index=${n}.`),t.push(x)}finally{u.stackRestore(w)}},Da=async(e,t,r,i,a,n)=>{var V,j,R,K;let s=_e(),u=s.PTR_SIZE,l=pt.get(e);if(!l)throw new Error(`cannot run inference. invalid session id: ${e}`);let p=l[0],h=l[1],f=l[2],g=l[3],y=l[4],_=l[5],w=t.length,S=i.length,x=0,b=[],I=[],k=[],E=[],A=[],C=s.stackSave(),$=s.stackAlloc(w*u),N=s.stackAlloc(w*u),D=s.stackAlloc(S*u),G=s.stackAlloc(S*u);try{[x,b]=Qn(n),vt("wasm prepareInputOutputTensor");for(let L=0;L<w;L++)await Na(r[L],I,E,e,h[t[L]],t[L],y);for(let L=0;L<S;L++)await Na(a[L],k,E,e,f[i[L]],w+i[L],y);xt("wasm prepareInputOutputTensor");for(let L=0;L<w;L++)s.setValue($+L*u,I[L],"*"),s.setValue(N+L*u,h[t[L]],"*");for(let L=0;L<S;L++)s.setValue(D+L*u,k[L],"*"),s.setValue(G+L*u,f[i[L]],"*");if(g&&!_){let{handle:L,outputPreferredLocations:me,outputPreferredLocationsEncoded:U}=g;if(h.length!==w)throw new Error(`input count from feeds (${w}) is expected to be always equal to model's input count (${h.length}).`);vt("wasm bindInputsOutputs");for(let P=0;P<w;P++){let J=t[P];await s._OrtBindInput(L,h[J],I[P])!==0&&fe(`Can't bind input[${P}] for session=${e}.`)}for(let P=0;P<S;P++){let J=i[P];(V=a[P])!=null&&V[3]?(A.push(k[P]),s._OrtBindOutput(L,f[J],k[P],0)!==0&&fe(`Can't bind pre-allocated output[${P}] for session=${e}.`)):s._OrtBindOutput(L,f[J],0,U[J])!==0&&fe(`Can't bind output[${P}] to ${me[P]} for session=${e}.`)}xt("wasm bindInputsOutputs"),pt.set(e,[p,h,f,g,y,!0])}(j=s.jsepOnRunStart)==null||j.call(s,p),(R=s.webnnOnRunStart)==null||R.call(s,p);let F;g?F=await s._OrtRunWithBinding(p,g.handle,S,D,x):F=await s._OrtRun(p,N,$,w,G,S,D,x),F!==0&&fe("failed to call OrtRun().");let X=[],le=[];vt("wasm ProcessOutputTensor");for(let L=0;L<S;L++){let me=Number(s.getValue(D+L*u,"*"));if(me===k[L]||A.includes(k[L])){X.push(a[L]),me!==k[L]&&s._OrtReleaseTensor(me)!==0&&fe("Can't release tensor.");continue}let U=s.stackSave(),P=s.stackAlloc(4*u),J=!1,ee,$e=0;try{s._OrtGetTensorData(me,P,P+u,P+2*u,P+3*u)!==0&&fe(`Can't access output tensor data on index ${L}.`);let ht=u===4?"i32":"i64",ft=Number(s.getValue(P,ht));$e=s.getValue(P+u,"*");let pr=s.getValue(P+u*2,"*"),Gr=Number(s.getValue(P+u*3,ht)),De=[];for(let we=0;we<Gr;we++)De.push(Number(s.getValue(pr+we*u,ht)));s._OrtFree(pr)!==0&&fe("Can't free memory for tensor dims.");let Re=De.reduce((we,ie)=>we*ie,1);ee=it(ft);let mt=g==null?void 0:g.outputPreferredLocations[i[L]];if(ee==="string"){if(mt==="gpu-buffer"||mt==="ml-tensor")throw new Error("String tensor is not supported on GPU.");let we=[];for(let ie=0;ie<Re;ie++){let Ue=s.getValue($e+ie*u,"*"),Hr=s.getValue($e+(ie+1)*u,"*"),cr=ie===Re-1?void 0:Hr-Ue;we.push(s.UTF8ToString(Ue,cr))}X.push([ee,De,we,"cpu"])}else if(mt==="gpu-buffer"&&Re>0){let we=s.jsepGetBuffer;if(!we)throw new Error('preferredLocation "gpu-buffer" is not supported without using WebGPU.');let ie=we($e),Ue=kt(ft,Re);if(Ue===void 0||!vi(ee))throw new Error(`Unsupported data type: ${ee}`);J=!0,X.push([ee,De,{gpuBuffer:ie,download:s.jsepCreateDownloader(ie,Ue,ee),dispose:()=>{s._OrtReleaseTensor(me)!==0&&fe("Can't release tensor.")}},"gpu-buffer"])}else if(mt==="ml-tensor"&&Re>0){let we=s.webnnEnsureTensor,ie=s.webnnIsGraphInputOutputTypeSupported;if(!we||!ie)throw new Error('preferredLocation "ml-tensor" is not supported without using WebNN.');if(kt(ft,Re)===void 0||!xi(ee))throw new Error(`Unsupported data type: ${ee}`);if(!ie(e,ee,!1))throw new Error(`preferredLocation "ml-tensor" for ${ee} output is not supported by current WebNN Context.`);let Ue=await we(e,$e,ft,De,!1);J=!0,X.push([ee,De,{mlTensor:Ue,download:s.webnnCreateMLTensorDownloader($e,ee),dispose:()=>{s.webnnReleaseTensorId($e),s._OrtReleaseTensor(me)}},"ml-tensor"])}else if(mt==="ml-tensor-cpu-output"&&Re>0){let we=s.webnnCreateMLTensorDownloader($e,ee)(),ie=X.length;J=!0,le.push((async()=>{let Ue=[ie,await we];return s.webnnReleaseTensorId($e),s._OrtReleaseTensor(me),Ue})()),X.push([ee,De,[],"cpu"])}else{let we=Sr(ee),ie=new we(Re);new Uint8Array(ie.buffer,ie.byteOffset,ie.byteLength).set(s.HEAPU8.subarray($e,$e+ie.byteLength)),X.push([ee,De,ie,"cpu"])}}finally{s.stackRestore(U),ee==="string"&&$e&&s._free($e),J||s._OrtReleaseTensor(me)}}g&&!y&&(s._OrtClearBoundOutputs(g.handle)!==0&&fe("Can't clear bound outputs."),pt.set(e,[p,h,f,g,y,!1]));for(let[L,me]of await Promise.all(le))X[L][2]=me;return xt("wasm ProcessOutputTensor"),X}finally{(K=s.webnnOnRunEnd)==null||K.call(s,p),s.stackRestore(C),I.forEach(F=>s._OrtReleaseTensor(F)),k.forEach(F=>s._OrtReleaseTensor(F)),E.forEach(F=>s._free(F)),x!==0&&s._OrtReleaseRunOptions(x),b.forEach(F=>s._free(F))}},Ua=e=>{let t=_e(),r=pt.get(e);if(!r)throw new Error("invalid session id");let i=r[0],a=t._OrtEndProfiling(i);a===0&&fe("Can't get an profile file name."),t._OrtFree(a)},Pa=e=>{let t=[];for(let r of e){let i=r[2];!Array.isArray(i)&&"buffer"in i&&t.push(i.buffer)}return t}}),ct,Oe,Gt,ur,lr,qr,qa,Lr,Rt,Bt,gc,yc,_c,wc,bc,$c,vc,xc,Sc=q(()=>{Pe(),mc(),St(),yi(),ct=()=>!!ye.wasm.proxy&&typeof document<"u",Gt=!1,ur=!1,lr=!1,Lr=new Map,Rt=(e,t)=>{let r=Lr.get(e);r?r.push(t):Lr.set(e,[t])},Bt=()=>{if(Gt||!ur||lr||!Oe)throw new Error("worker not ready")},gc=e=>{switch(e.data.type){case"init-wasm":Gt=!1,e.data.err?(lr=!0,qa[1](e.data.err)):(ur=!0,qa[0]()),qr&&(URL.revokeObjectURL(qr),qr=void 0);break;case"init-ep":case"copy-from":case"create":case"release":case"run":case"end-profiling":{let t=Lr.get(e.data.type);e.data.err?t.shift()[1](e.data.err):t.shift()[0](e.data.out);break}}},yc=async()=>{if(!ur){if(Gt)throw new Error("multiple calls to 'initWasm()' detected.");if(lr)throw new Error("previous call to 'initWasm()' failed.");if(Gt=!0,ct())return new Promise((e,t)=>{Oe==null||Oe.terminate(),Gn().then(([r,i])=>{try{Oe=i,Oe.onerror=n=>t(n),Oe.onmessage=gc,qa=[e,t];let a={type:"init-wasm",in:ye};!a.in.wasm.wasmPaths&&(r||hi)&&(a.in.wasm.wasmPaths={wasm:new URL(""+new URL("ort-wasm-simd-threaded.jsep-C887KxcQ.wasm",self.location.href).href,self.location.href).href}),Oe.postMessage(a),qr=r}catch(a){t(a)}},t)});try{await bi(ye.wasm),await Aa(ye),ur=!0}catch(e){throw lr=!0,e}finally{Gt=!1}}},_c=async e=>{if(ct())return Bt(),new Promise((t,r)=>{Rt("init-ep",[t,r]);let i={type:"init-ep",in:{epName:e,env:ye}};Oe.postMessage(i)});await Oa(ye,e)},wc=async e=>ct()?(Bt(),new Promise((t,r)=>{Rt("copy-from",[t,r]);let i={type:"copy-from",in:{buffer:e}};Oe.postMessage(i,[e.buffer])})):Pr(e),bc=async(e,t)=>{if(ct()){if(t!=null&&t.preferredOutputLocation)throw new Error('session option "preferredOutputLocation" is not supported for proxy.');return Bt(),new Promise((r,i)=>{Rt("create",[r,i]);let a={type:"create",in:{model:e,options:{...t}}},n=[];e instanceof Uint8Array&&n.push(e.buffer),Oe.postMessage(a,n)})}else return Ba(e,t)},$c=async e=>{if(ct())return Bt(),new Promise((t,r)=>{Rt("release",[t,r]);let i={type:"release",in:e};Oe.postMessage(i)});Ma(e)},vc=async(e,t,r,i,a,n)=>{if(ct()){if(r.some(s=>s[3]!=="cpu"))throw new Error("input tensor on GPU is not supported for proxy.");if(a.some(s=>s))throw new Error("pre-allocated output tensor is not supported for proxy.");return Bt(),new Promise((s,u)=>{Rt("run",[s,u]);let l=r,p={type:"run",in:{sessionId:e,inputIndices:t,inputs:l,outputIndices:i,options:n}};Oe.postMessage(p,Pa(l))})}else return Da(e,t,r,i,a,n)},xc=async e=>{if(ct())return Bt(),new Promise((t,r)=>{Rt("end-profiling",[t,r]);let i={type:"end-profiling",in:e};Oe.postMessage(i)});Ua(e)}}),La,Tc,kc,Qm=q(()=>{Pe(),Sc(),te(),li(),ts(),La=(e,t)=>{switch(e.location){case"cpu":return[e.type,e.dims,e.data,"cpu"];case"gpu-buffer":return[e.type,e.dims,{gpuBuffer:e.gpuBuffer},"gpu-buffer"];case"ml-tensor":return[e.type,e.dims,{mlTensor:e.mlTensor},"ml-tensor"];default:throw new Error(`invalid data location: ${e.location} for ${t()}`)}},Tc=e=>{switch(e[3]){case"cpu":return new Ce(e[0],e[2],e[1]);case"gpu-buffer":{let t=e[0];if(!vi(t))throw new Error(`not supported data type: ${t} for deserializing GPU tensor`);let{gpuBuffer:r,download:i,dispose:a}=e[2];return Ce.fromGpuBuffer(r,{dataType:t,dims:e[1],download:i,dispose:a})}case"ml-tensor":{let t=e[0];if(!xi(t))throw new Error(`not supported data type: ${t} for deserializing MLTensor tensor`);let{mlTensor:r,download:i,dispose:a}=e[2];return Ce.fromMLTensor(r,{dataType:t,dims:e[1],download:i,dispose:a})}default:throw new Error(`invalid data location: ${e[3]}`)}},kc=class{async fetchModelAndCopyToWasmMemory(e){return wc(await Ti(e))}async loadModel(e,t){Qe();let r;typeof e=="string"?r=await this.fetchModelAndCopyToWasmMemory(e):r=e,[this.sessionId,this.inputNames,this.outputNames,this.inputMetadata,this.outputMetadata]=await bc(r,t),Le()}async dispose(){return $c(this.sessionId)}async run(e,t,r){Qe();let i=[],a=[];Object.entries(e).forEach(f=>{let g=f[0],y=f[1],_=this.inputNames.indexOf(g);if(_===-1)throw new Error(`invalid input '${g}'`);i.push(y),a.push(_)});let n=[],s=[];Object.entries(t).forEach(f=>{let g=f[0],y=f[1],_=this.outputNames.indexOf(g);if(_===-1)throw new Error(`invalid output '${g}'`);n.push(y),s.push(_)});let u=i.map((f,g)=>La(f,()=>`input "${this.inputNames[a[g]]}"`)),l=n.map((f,g)=>f?La(f,()=>`output "${this.outputNames[s[g]]}"`):null),p=await vc(this.sessionId,a,u,s,l,r),h={};for(let f=0;f<p.length;f++)h[this.outputNames[s[f]]]=n[f]??Tc(p[f]);return Le(),h}startProfiling(){}endProfiling(){xc(this.sessionId)}}}),Ic={};Pt(Ic,{OnnxruntimeWebAssemblyBackend:()=>Va,initializeFlags:()=>Wa,wasmBackend:()=>Ec});var Wa,Va,Ec,Zm=q(()=>{Pe(),Sc(),Qm(),Wa=()=>{(typeof ye.wasm.initTimeout!="number"||ye.wasm.initTimeout<0)&&(ye.wasm.initTimeout=0);let e=ye.wasm.simd;if(typeof e!="boolean"&&e!==void 0&&e!=="fixed"&&e!=="relaxed"&&(console.warn(`Property "env.wasm.simd" is set to unknown value "${e}". Reset it to \`false\` and ignore SIMD feature checking.`),ye.wasm.simd=!1),typeof ye.wasm.proxy!="boolean"&&(ye.wasm.proxy=!1),typeof ye.wasm.trace!="boolean"&&(ye.wasm.trace=!1),typeof ye.wasm.numThreads!="number"||!Number.isInteger(ye.wasm.numThreads)||ye.wasm.numThreads<=0)if(typeof self<"u"&&!self.crossOriginIsolated)ye.wasm.numThreads=1;else{let t=typeof navigator>"u"?Mf("node:os").cpus().length:navigator.hardwareConcurrency;ye.wasm.numThreads=Math.min(4,Math.ceil((t||1)/2))}},Va=class{async init(e){Wa(),await yc(),await _c(e)}async createInferenceSessionHandler(e,t){let r=new kc;return await r.loadModel(e,t),r}},Ec=new Va});Pe(),Pe(),Pe();var Ym="1.24.3";{let e=(Zm(),jt(Ic)).wasmBackend;qt("webgpu",e,5),qt("webnn",e,5),qt("cpu",e,10),qt("wasm",e,10)}Object.defineProperty(ye.versions,"web",{value:Ym,enumerable:!0});/**
* @license
* Copyright 2021 Google LLC. All Rights Reserved.
* Licensed under the Apache License, Version 2.0 (the "License");
* you may not use this file except in compliance with the License.
* You may obtain a copy of the License at
*
* http://www.apache.org/licenses/LICENSE-2.0
*
* Unless required by applicable law or agreed to in writing, software
* distributed under the License is distributed on an "AS IS" BASIS,
* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
* See the License for the specific language governing permissions and
* limitations under the License.
* =============================================================================
*//**
 * @license
 * Copyright 2020 Google LLC. All Rights Reserved.
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 * =============================================================================
 *//**
 * @license
 * Copyright 2019 Google LLC. All Rights Reserved.
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 * =============================================================================
 */const Ee=1024,Ye=256;function Xm(e,t,r){return[e*r.originalWidth*r.scale+r.padX,t*r.originalHeight*r.scale+r.padY]}function Jm(e,t){return{x:e.x/t.originalWidth,y:e.y/t.originalHeight,w:e.w/t.originalWidth,h:e.h/t.originalHeight}}function eg(e,t,r=Ye,i=Ye){const{originalWidth:a,originalHeight:n,scale:s,padX:u,padY:l}=t,p=i/Ee,h=r/Ee,f=Math.floor(u*p),g=Math.floor(l*h),y=Math.round(a*s*p),_=Math.round(n*s*h);let w=i,S=r,x=-1,b=-1;for(let C=0;C<r;C++)for(let $=0;$<i;$++)e[C*i+$]>0&&($<w&&(w=$),$>x&&(x=$),C<S&&(S=C),C>b&&(b=C));if(x<0)return null;const I=Math.max(0,Math.floor((w-f)/y*a)),k=Math.max(0,Math.floor((S-g)/_*n)),E=Math.min(a-1,Math.ceil((x-f)/y*a)),A=Math.min(n-1,Math.ceil((b-g)/_*n));return{x:I,y:k,w:E-I+1,h:A-k+1}}function tg(e,t,r,i=Ye,a=Ye){const{originalWidth:n,originalHeight:s,scale:u,padX:l,padY:p}=t,h=a/Ee,f=i/Ee,g=Math.floor(l*h),y=Math.floor(p*f),_=Math.round(n*u*h),w=Math.round(s*u*f),S=new Float32Array(r.w*r.h);for(let x=0;x<r.h;x++)for(let b=0;b<r.w;b++){const I=r.x+b,k=r.y+x,E=I/n*_+g,A=k/s*w+y,C=Math.max(0,Math.min(Math.floor(E),a-1)),$=Math.min(C+1,a-1),N=Math.max(0,Math.min(Math.floor(A),i-1)),D=Math.min(N+1,i-1),G=E-Math.floor(E),V=A-Math.floor(A),j=e[N*a+C]*(1-G)*(1-V)+e[N*a+$]*G*(1-V)+e[D*a+C]*(1-G)*V+e[D*a+$]*G*V;S[x*r.w+b]=1/(1+Math.exp(-j))}return S}const rg="fiftyone-models",dr="weights",ig=1e3,ag=6e4,zc=3;function ng(){return new Promise((e,t)=>{const r=indexedDB.open(rg,1);r.onupgradeneeded=()=>r.result.createObjectStore(dr),r.onsuccess=()=>e(r.result),r.onerror=()=>t(r.error)})}function sg(e,t){return new Promise((r,i)=>{const n=e.transaction(dr,"readonly").objectStore(dr).get(t);n.onsuccess=()=>r(n.result),n.onerror=()=>i(n.error)})}function og(e,t,r){return new Promise((i,a)=>{const n=e.transaction(dr,"readwrite");n.objectStore(dr).put(r,t),n.oncomplete=()=>i(),n.onerror=()=>a(n.error)})}async function Cc(e,t){let r=null;for(let i=0;i<zc;i++){i>0&&await new Promise(s=>setTimeout(s,ig*i));const a=new AbortController,n=setTimeout(()=>a.abort(),ag);try{const s=await fetch(e,{signal:a.signal});if(!s.ok){if(r=new Error(`${s.status} ${s.statusText} (${e})`),s.status>=400&&s.status<500&&s.status!==408&&s.status!==429)break;continue}const u=s.headers.get("content-length"),l=u?Number(u):0;if(!t||!l||!s.body)return await s.arrayBuffer();const p=s.body.getReader(),h=new Uint8Array(l);let f=0;for(;;){const{done:g,value:y}=await p.read();if(g)break;h.set(y,f),f+=y.byteLength,t(f,l)}if(f!==l)throw new Error(`Truncated response: received ${f} of ${l} bytes (${e})`);return h.buffer}catch(s){r=s instanceof Error?s:new Error(String(s))}finally{clearTimeout(n)}}throw r??new Error(`Failed to fetch ${e} after ${zc} attempts`)}async function Ac(e,t,r){let i=null;try{i=await ng()}catch(a){return r==null||r(`IndexedDB open failed, downloading instead: ${a}`),Cc(e,t)}try{try{const n=await sg(i,e);if(n)return t==null||t(n.byteLength,n.byteLength),n}catch(n){r==null||r(`IndexedDB cache read failed, downloading instead: ${n}`)}const a=await Cc(e,t);try{await og(i,e,a)}catch(n){r==null||r(`IndexedDB cache write failed: ${n}`)}return a}finally{i.close()}}function Oc(e,t){self.postMessage({type:e,result:t})}function Rc(e,t,r,i){self.postMessage({id:e,type:t,success:!0,result:r},i)}function Bc(e,t,r){self.postMessage({id:e,type:t,success:!1,error:r})}const Ga=[.485,.456,.406],Ha=[.229,.224,.225],Mc="https://huggingface.co/SharpAI/sam2-hiera-tiny-onnx/resolve/main",ug=`${Mc}/encoder.with_runtime_opt.ort`,lg=`${Mc}/decoder.onnx`,dg=typeof crossOriginIsolated<"u"&&crossOriginIsolated;ye.wasm.numThreads=dg?4:1,ye.wasm.simd=!0;let Wr=null,Vr=null;async function pg(e){let t;try{t=await fetch(e)}catch(s){throw new Error(`Image fetch failed (check CORS headers): ${s}`)}if(!t.ok)throw new Error(`Image fetch failed: ${t.status} ${t.statusText}`);const r=await t.blob(),i=await createImageBitmap(r).catch(s=>{throw new Error(`Failed to decode image: ${s}`)}),a=new OffscreenCanvas(i.width,i.height),n=a.getContext("2d");if(!n)throw new Error("Failed to get 2d context");return n.drawImage(i,0,0),i.close(),n.getImageData(0,0,a.width,a.height)}function cg(e){const{width:t,height:r}=e,i=Math.min(Ee/t,Ee/r),a=Math.round(t*i),n=Math.round(r*i),s=Math.floor((Ee-a)/2),u=Math.floor((Ee-n)/2),p=new OffscreenCanvas(Ee,Ee).getContext("2d");if(!p)throw new Error("Failed to get 2d context");p.fillStyle="black",p.fillRect(0,0,Ee,Ee);const h=new OffscreenCanvas(t,r),f=h.getContext("2d");if(!f)throw new Error("Failed to get 2d context");f.putImageData(e,0,0),p.drawImage(h,s,u,a,n);const g=p.getImageData(0,0,Ee,Ee).data,y=Ee*Ee,_=new Float32Array(3*y);for(let w=0;w<y;w++){const S=w*4;_[w]=(g[S]/255-Ga[0])/Ha[0],_[w+y]=(g[S+1]/255-Ga[1])/Ha[1],_[w+2*y]=(g[S+2]/255-Ga[2])/Ha[2]}return{tensor:_,originalWidth:t,originalHeight:r,scale:i,padX:s,padY:u}}async function hg(){const e={executionProviders:["wasm"]},t=(i,a,n)=>Oc("progress",{file:i,loaded:a,total:n}),r=i=>Oc("warning",i);if(!Wr){const i=await Ac(ug,(a,n)=>t("encoder",a,n),r);Wr=await br.create(i,e)}if(!Vr){const i=await Ac(lg,(a,n)=>t("decoder",a,n),r);Vr=await br.create(i,e)}}async function fg(e,t){if(!Wr||!Vr)throw new Error("Model not loaded");if(t.length===0)throw new Error("At least one prompt point is required");const r=await pg(e),i=cg(r),a=await Wr.run({image:new Ce("float32",i.tensor,[1,3,Ee,Ee])}),n=t.length,s=new Float32Array(n*2),u=new Float32Array(n);for(let S=0;S<n;S++){const[x,b]=Xm(t[S].x,t[S].y,i);s[S*2]=x,s[S*2+1]=b,u[S]=t[S].label}const l=await Vr.run({image_embed:a.image_embed,high_res_feats_0:a.high_res_feats_0,high_res_feats_1:a.high_res_feats_1,point_coords:new Ce("float32",s,[1,n,2]),point_labels:new Ce("float32",u,[1,n]),mask_input:new Ce("float32",new Float32Array(Ye*Ye),[1,1,Ye,Ye]),has_mask_input:new Ce("float32",new Float32Array([0]),[1])}),p=l.masks.data,h=l.iou_predictions.data,f=Ye*Ye;let g=0;for(let S=1;S<h.length;S++)h[S]>h[g]&&(g=S);const y=p.slice(g*f,(g+1)*f),_=eg(y,i);if(!_)throw new Error("Model returned an empty mask");return{mask:tg(y,i,_),bbox:Jm(_,i)}}self.onmessage=async e=>{const{id:t,type:r,payload:i}=e.data;try{if(r==="loadModel")await hg(),Rc(t,"loadModel",void 0);else if(r==="embedAndDecode"){const{mask:a,bbox:n}=await fg(i.imageUrl,i.points);Rc(t,"embedAndDecode",{mask:a,bbox:n},[a.buffer])}else Bc(t,r,`Unknown message type: ${r}`)}catch(a){Bc(t,r,a instanceof Error?a.message:String(a))}},self.postMessage({type:"ready"})})();
