import{OrthographicCamera as W,Scene as R,WebGLRenderTarget as K,NearestFilter as D,HalfFloatType as Z,BufferGeometry as T,BufferAttribute as C,Sphere as q,Vector3 as $,RawShaderMaterial as _,Mesh as Q,Matrix4 as J,WebGLRenderer as tt,OneFactor as z,CustomBlending as H,Points as X,DynamicDrawUsage as F,NormalBlending as et}from"./three.module-DK_4hUQZ.js";import{M as Y,a as E,C as j,H as it,L as N,B as st,D as nt,b as rt,c as at,d as P,P as G,E as ot,e as lt,f as B}from"./EmbeddingsV2Panel-DGhx6uSj.js";import"./index-Dc58E4ij.js";import"./plotly-CrTaWLEP.js";import"./recharts-BXZtEhpB.js";import"./DatasetPage-BnOqq7Oh.js";import"./DatasetPageQuery.graphql-YZt51qfU.js";import"./index.module-lyrnYfOx.js";function ht(r,t=!1){const e=r.length,s=new Float32Array(e),i=new Float32Array(e),n=new Float32Array(e),a=new Array(e),o=new Uint32Array(e),l=[],h=new Map;let c=!1,d=1/0,f=-1/0,w=1/0,x=-1/0,p=1/0,u=-1/0;for(let y=0;y<e;y++){const{id:v,x:g,y:m,z:b,label:I}=r[y];b!==void 0&&!t&&(c=!0);const M=t?0:b??0;s[y]=g,i[y]=m,n[y]=M,a[y]=v,g<d&&(d=g),g>f&&(f=g),m<w&&(w=m),m>x&&(x=m),M<p&&(p=M),M>u&&(u=M);const A=String(I);let S=h.get(A);S===void 0&&(S=l.length,l.push(A),h.set(A,S)),o[y]=S}return e===0&&(d=w=p=0,f=x=u=1),{n:e,xs:s,ys:i,zs:n,hasZ:c,ids:a,labelIndex:o,labelKeys:l,xMin:d,xMax:f,yMin:w,yMax:x,zMin:p,zMax:u}}function ct(r,t){if(!t){const{xMin:l,xMax:h,yMin:c,yMax:d,zMin:f,zMax:w}=r;return{xMin:l,xMax:h,yMin:c,yMax:d,zMin:f,zMax:w}}let e=1/0,s=-1/0,i=1/0,n=-1/0,a=1/0,o=-1/0;for(let l=0;l<r.n;l++){if(!t[l])continue;const h=r.xs[l],c=r.ys[l],d=r.zs[l];h<e&&(e=h),h>s&&(s=h),c<i&&(i=c),c>n&&(n=c),d<a&&(a=d),d>o&&(o=d)}return e===1/0?null:{xMin:e,xMax:s,yMin:i,yMax:n,zMin:a,zMax:o}}function U(r,t){const e=r.labelKeys.map((i,n)=>{const a=t[n%t.length];return[parseInt(a.slice(1,3),16)/255,parseInt(a.slice(3,5),16)/255,parseInt(a.slice(5,7),16)/255]}),s=new Float32Array(r.n*3);for(let i=0;i<r.n;i++)s.set(e[r.labelIndex[i]],i*3);return s}function L(r,t,e,s){const i=r.xMax-r.xMin||1,n=r.yMax-r.yMin||1,a=Math.max(t-2*s,1),o=Math.max(e-2*s,1),l=Math.max(i/a,n/o),h=(r.xMin+r.xMax)/2,c=(r.yMin+r.yMax)/2,d=t*l/2,f=e*l/2;return{x0:h-d,x1:h+d,y0:c-f,y1:c+f}}function O(r,t){return(t.x1-t.x0)/(r.x1-r.x0)}function V(r,t,e,s,i){return[r.x0+s/t*(r.x1-r.x0),r.y1-i/e*(r.y1-r.y0)]}function k(r,t){let{x0:e,y0:s,x1:i,y1:n}=r;return e<t.x0&&(i+=t.x0-e,e=t.x0),i>t.x1&&(e-=i-t.x1,i=t.x1),s<t.y0&&(n+=t.y0-s,s=t.y0),n>t.y1&&(s-=n-t.y1,n=t.y1),{x0:e,y0:s,x1:i,y1:n}}function dt(r,t,e,s,i){const n=Math.min(Math.max(O(r,t)*s,1),i),a=(t.x1-t.x0)/n,o=(t.y1-t.y0)/n,[l,h]=e,c=(l-r.x0)/(r.x1-r.x0),d=(h-r.y0)/(r.y1-r.y0);return k({x0:l-c*a,x1:l+(1-c)*a,y0:h-d*o,y1:h+(1-d)*o},t)}function ut(r,t,e,s){return k({x0:r.x0+e,x1:r.x1+e,y0:r.y0+s,y1:r.y1+s},t)}function pt(r,t,e){let s=!1;for(let i=0,n=r.length-1;i<r.length;n=i++){const[a,o]=r[i],[l,h]=r[n];o>e!=h>e&&t<(l-a)*(e-o)/(h-o)+a&&(s=!s)}return s}function ft(r,t,e,s,i,n){let a=1/0,o=-1/0,l=1/0,h=-1/0;for(const[p,u]of i)p<a&&(a=p),p>o&&(o=p),u<l&&(l=u),u>h&&(h=u);const{n:c,xs:d,ys:f,zs:w}=r,x=[];for(let p=0;p<c;p++){if(n&&n[p]===0)continue;const u=d[p],y=f[p],v=w[p],g=t[3]*u+t[7]*y+t[11]*v+t[15];if(g<=0)continue;const m=((t[0]*u+t[4]*y+t[8]*v+t[12])/g*.5+.5)*e,b=(.5-(t[1]*u+t[5]*y+t[9]*v+t[13])/g*.5)*s;m>=a&&m<=o&&b>=l&&b<=h&&pt(i,m,b)&&x.push(p)}return x}function yt(r,t,e,s,i,n,a,o){const{n:l,xs:h,ys:c,zs:d}=r;let f=-1,w=a*a,x=0,p=0;for(let u=0;u<l;u++){if(o&&o[u]===0)continue;const y=h[u],v=c[u],g=d[u],m=t[3]*y+t[7]*v+t[11]*g+t[15];if(m<=0)continue;const b=((t[0]*y+t[4]*v+t[8]*g+t[12])/m*.5+.5)*e,I=(.5-(t[1]*y+t[5]*v+t[9]*g+t[13])/m*.5)*s,M=b-i,A=I-n,S=M*M+A*A;S<w&&(w=S,f=u,x=b,p=I)}return f<0?null:{index:f,id:r.ids[f],label:r.labelKeys[r.labelIndex[f]],x,y:p}}class gt{camera;element;onChange;listeners=new AbortController;bounds=null;focus=null;home={x0:-1,y0:-1,x1:1,y1:1};rect=this.home;width=1;height=1;panPointer=null;panLast=[0,0];mode="select";constructor(t,e){this.element=t,this.onChange=e,this.camera=new W(-1,1,1,-1,.1,10),this.camera.position.set(0,0,1);const{signal:s}=this.listeners;t.addEventListener("wheel",i=>this.handleWheel(i),{passive:!1,signal:s}),t.addEventListener("pointerdown",i=>this.handlePanStart(i),{signal:s}),t.addEventListener("pointermove",i=>this.handlePanMove(i),{signal:s});for(const i of["pointerup","pointercancel"])t.addEventListener(i,n=>this.handlePanEnd(n),{signal:s})}isLassoStart(t){return this.mode==="select"&&t.button===0&&!t.shiftKey}setMode(t){this.mode=t}toDataPolygon(t){return t.map(([e,s])=>V(this.rect,this.width,this.height,e,s))}setBounds(t,e,s){this.bounds=t,this.focus=null,this.width=e,this.height=s,this.home=L(t,e,s,E),this.rect=this.home,this.apply()}setFocus(t){this.focus=t}resize(t,e){if(this.width=t,this.height=e,!this.bounds)return;const s=O(this.rect,this.home),i=(this.rect.x0+this.rect.x1)/2,n=(this.rect.y0+this.rect.y1)/2;this.home=L(this.bounds,t,e,E);const a=(this.home.x1-this.home.x0)/s,o=(this.home.y1-this.home.y0)/s;this.rect=k({x0:i-a/2,x1:i+a/2,y0:n-o/2,y1:n+o/2},this.home),this.apply()}reset(){this.rect=this.focus?this.frameFocus(this.focus):this.home,this.apply()}frameFocus(t){const e=L(t,this.width,this.height,E),s=Math.min(O(e,this.home),Y),i=(this.home.x1-this.home.x0)/s,n=(this.home.y1-this.home.y0)/s,a=(t.xMin+t.xMax)/2,o=(t.yMin+t.yMax)/2;return k({x0:a-i/2,x1:a+i/2,y0:o-n/2,y1:o+n/2},this.home)}destroy(){this.listeners.abort()}apply(){const{x0:t,y0:e,x1:s,y1:i}=this.rect;this.camera.left=t,this.camera.right=s,this.camera.top=i,this.camera.bottom=e,this.camera.updateProjectionMatrix(),this.onChange()}handleWheel(t){t.preventDefault();const e=t.ctrlKey?.02:.002,s=Math.pow(2,-t.deltaY*e),i=V(this.rect,this.width,this.height,t.offsetX,t.offsetY);this.rect=dt(this.rect,this.home,i,s,Y),this.apply()}handlePanStart(t){(t.button===1||t.button===0&&(t.shiftKey||this.mode==="explore"))&&(t.preventDefault(),this.panPointer=t.pointerId,this.panLast=[t.offsetX,t.offsetY],this.element.setPointerCapture(t.pointerId))}handlePanMove(t){if(this.panPointer!==t.pointerId)return;const[e,s]=this.panLast;this.panLast=[t.offsetX,t.offsetY];const i=(this.rect.x1-this.rect.x0)/this.width,n=(this.rect.y1-this.rect.y0)/this.height;this.rect=ut(this.rect,this.home,-(t.offsetX-e)*i,(t.offsetY-s)*n),this.apply()}handlePanEnd(t){this.panPointer===t.pointerId&&(this.panPointer=null)}}class mt{listeners=new AbortController;pointerId=null;downX=0;downY=0;constructor(t,e){const{signal:s}=this.listeners;t.addEventListener("pointerdown",i=>{i.button!==0||i.shiftKey||(this.pointerId=i.pointerId,this.downX=i.offsetX,this.downY=i.offsetY)},{signal:s}),t.addEventListener("pointerup",i=>{if(this.pointerId!==i.pointerId)return;this.pointerId=null;const n=i.offsetX-this.downX,a=i.offsetY-this.downY;n*n+a*a>j*j||e.onClick(i.offsetX,i.offsetY)},{signal:s}),t.addEventListener("pointercancel",()=>{this.pointerId=null},{signal:s})}destroy(){this.listeners.abort()}}class wt{callbacks;listeners=new AbortController;handle=null;pointer=null;hitShown=!1;buttonsDown=!1;constructor(t,e){this.callbacks=e;const{signal:s}=this.listeners;t.addEventListener("pointerdown",()=>{this.buttonsDown=!0,this.clear()},{capture:!0,signal:s});for(const i of["pointerup","pointercancel"])t.addEventListener(i,()=>{this.buttonsDown=!1},{capture:!0,signal:s});t.addEventListener("pointermove",i=>{this.callbacks.isBlocked()||i.buttons!==0||(this.pointer=[i.offsetX,i.offsetY],this.schedule())},{signal:s}),t.addEventListener("pointerleave",()=>{this.pointer=null,this.clear()},{signal:s})}viewChanged(){this.buttonsDown?this.clear():this.schedule()}reset(){this.pointer=null,this.clear()}destroy(){this.cancel(),this.listeners.abort()}schedule(){this.clear(),this.pointer&&(this.handle=window.setTimeout(()=>{this.handle=null,this.hitTest()},it))}clear(){this.cancel(),this.hitShown&&(this.hitShown=!1,this.callbacks.onHover(null))}cancel(){this.handle!==null&&(window.clearTimeout(this.handle),this.handle=null)}hitTest(){if(!this.pointer||this.callbacks.isBlocked())return;const t=this.callbacks.pick(this.pointer[0],this.pointer[1]);t&&(this.hitShown=!0,this.callbacks.onHover(t))}}class xt{svg;path;listeners=new AbortController;polygon=[];drawing=!1;pointerId=null;constructor(t,e){const s="http://www.w3.org/2000/svg";this.svg=document.createElementNS(s,"svg"),Object.assign(this.svg.style,{position:"absolute",inset:"0",width:"100%",height:"100%",pointerEvents:"none",zIndex:"1"}),this.path=document.createElementNS(s,"path"),this.path.setAttribute("fill",N),this.path.setAttribute("fill-opacity","0.08"),this.path.setAttribute("stroke",N),this.path.setAttribute("stroke-width","1.5"),this.svg.appendChild(this.path),t.appendChild(this.svg);const{signal:i}=this.listeners;t.addEventListener("pointerdown",n=>{this.drawing||!e.shouldStart(n)||(n.stopPropagation(),n.preventDefault(),this.drawing=!0,this.pointerId=n.pointerId,this.polygon=[[n.offsetX,n.offsetY]],t.setPointerCapture(n.pointerId))},{capture:!0,signal:i}),t.addEventListener("pointermove",n=>{if(!this.drawing||n.pointerId!==this.pointerId)return;n.stopPropagation();const[a,o]=this.polygon[this.polygon.length-1],l=n.offsetX-a,h=n.offsetY-o;l*l+h*h<9||(this.polygon.push([n.offsetX,n.offsetY]),this.path.setAttribute("d",`M${this.polygon.map(c=>c.join(",")).join("L")}Z`))},{capture:!0,signal:i}),t.addEventListener("pointerup",n=>{if(!this.drawing||n.pointerId!==this.pointerId)return;n.stopPropagation(),this.drawing=!1,this.pointerId=null;const a=this.polygon;this.polygon=[],this.path.setAttribute("d",""),e.onComplete(a.length>=3?a:null,n.offsetX,n.offsetY)},{capture:!0,signal:i}),t.addEventListener("pointercancel",n=>{!this.drawing||n.pointerId!==this.pointerId||(this.drawing=!1,this.pointerId=null,this.polygon=[],this.path.setAttribute("d",""))},{capture:!0,signal:i})}isDrawing(){return this.drawing}destroy(){this.listeners.abort(),this.svg.remove()}}class vt{host=null;lasso=null;active=null;writeHost(t){return this.host=t,this.active=t?"host":this.lasso?"lasso":null,this.current()}writeLasso(t){return this.lasso=t,this.active=t?"lasso":this.host?"host":null,this.current()}clear(){return this.host=null,this.lasso=null,this.active=null,null}current(){return this.active==="host"?this.host:this.active==="lasso"?this.lasso:null}}const bt=`
  precision highp float;

  attribute vec3 position;
  attribute vec3 color;
  attribute float emphasis;
  attribute float visible;

  uniform mat4 projectionMatrix;
  uniform mat4 modelViewMatrix;
  uniform float uPointSize;
  uniform float uHasSelection;

  varying vec3 vColor;
  varying float vWeight;

  void main() {
    // dim = 1 for a non-selected point while a selection is active.
    // Dimming cuts the point's weight AND desaturates it toward gray:
    // the weight cut fades isolated points, the desaturation is what
    // survives density accumulation in deep piles (see constants.ts)
    float dim = uHasSelection * (1.0 - emphasis);
    vColor = mix(color, vec3(${nt}), dim * ${rt});
    vWeight = mix(1.0, ${at}, dim);
    if (visible < 0.5) {
      // Outside the clip volume (z > w): never rasterized
      gl_Position = vec4(2.0, 2.0, 2.0, 1.0);
      gl_PointSize = 0.0;
      return;
    }
    gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
    gl_PointSize = uPointSize;
  }
`,Mt=`
  precision highp float;

  uniform float uMode;
  uniform float uOpacity;

  varying vec3 vColor;
  varying float vWeight;

  void main() {
    float dist = length(gl_PointCoord - 0.5);
    if (uMode > 1.5) {
      // opaque(ish): depth-tested occlusion, AA edges via blending, and
      // uOpacity leaves a hint of see-through. Unsorted, so at low
      // opacity rear points pop instead of fading — keep it near 1.
      // Dimming darkens (a depth-written low-alpha point would block
      // whatever sits behind it)
      float edge = 1.0 - smoothstep(0.4, 0.5, dist);
      if (edge == 0.0) discard;
      gl_FragColor = vec4(vColor * vWeight, edge * uOpacity);
    } else {
      float edge = 1.0 - smoothstep(0.4, 0.5, dist);
      if (edge == 0.0) discard;
      float w = edge * vWeight;
      // density: premultiplied (color·w, w) for additive accumulation;
      // alpha: plain (color, coverage·alpha) for classic compositing
      gl_FragColor = mix(
        vec4(vColor, w * ${st}),
        vec4(vColor * w, w),
        uMode
      );
    }
  }
`,St=`
  precision highp float;

  attribute vec3 position;
  attribute vec3 color;
  attribute float emphasis;
  attribute float visible;

  uniform mat4 projectionMatrix;
  uniform mat4 modelViewMatrix;
  uniform float uPointSize;

  varying vec3 vColor;

  void main() {
    vColor = color;
    if (emphasis < 0.5 || visible < 0.5) {
      // Outside the clip volume (z > w): never rasterized
      gl_Position = vec4(2.0, 2.0, 2.0, 1.0);
      gl_PointSize = 0.0;
      return;
    }
    gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
    gl_PointSize = uPointSize;
  }
`,At=`
  precision highp float;

  varying vec3 vColor;

  void main() {
    float dist = length(gl_PointCoord - 0.5);
    float edge = 1.0 - smoothstep(0.44, 0.5, dist);
    if (edge == 0.0) discard;
    gl_FragColor = vec4(vColor, edge);
  }
`,Ct=`
  uniform float uGamma;
  uniform float uGlow;
  uniform float uAlphaSingle;

  vec4 toneMap(vec4 acc) {
    if (acc.a <= 0.0) return vec4(0.0);
    // rgb summed color*weight and a summed weight, so rgb/a is the
    // density-weighted average color at this pixel
    vec3 base = acc.rgb / acc.a;
    float d = pow(acc.a, uGamma);
    // Opacity: linear ramp up to the single-point alpha while coverage
    // is partial (d < 1), then exponential saturation toward 1.0 as the
    // pile deepens (d=2 ≈ 0.7, d=5 ≈ 0.95)
    float alpha = uAlphaSingle * min(d, 1.0) +
      (1.0 - uAlphaSingle) * (1.0 - exp(-max(d - 1.0, 0.0) * 0.35));
    // Glow: blend toward white with the log of density so 1000-deep
    // cores read hotter than 10-deep ones; capped at 45% so the point
    // hue stays recognizable
    vec3 color = mix(base, vec3(1.0), uGlow * min(0.45, 0.06 * log2(1.0 + d)));
    return vec4(color, alpha);
  }
`,Pt=`
  precision highp float;

  attribute vec2 position;
  varying vec2 vUv;

  void main() {
    vUv = position * 0.5 + 0.5;
    gl_Position = vec4(position, 0.0, 1.0);
  }
`,It=`
  precision highp float;

  varying vec2 vUv;
  uniform sampler2D uAcc;

  ${Ct}

  void main() {
    vec4 mapped = toneMap(texture2D(uAcc, vUv));
    if (mapped.a <= 0.0) discard;
    gl_FragColor = mapped;
  }
`;class zt{accumTarget;screenScene=new R;screenMaterial;screenCamera=new W(-1,1,1,-1,0,1);constructor(){this.accumTarget=new K(1,1,{type:Z,magFilter:D,minFilter:D,depthBuffer:!1,stencilBuffer:!1});const t=new T;t.setAttribute("position",new C(new Float32Array([-1,-1,3,-1,-1,3]),2)),t.boundingSphere=new q(new $(0,0,0),1),this.screenMaterial=new _({vertexShader:Pt,fragmentShader:It,uniforms:{uAcc:{value:this.accumTarget.texture},uGamma:{value:P.gamma},uGlow:{value:P.glow},uAlphaSingle:{value:P.singleAlpha}},transparent:!0,depthTest:!1,depthWrite:!1});const e=new Q(t,this.screenMaterial);e.frustumCulled=!1,this.screenScene.add(e)}setSize(t,e){this.accumTarget.setSize(t,e)}applySettings({gamma:t,glow:e,singleAlpha:s}){this.screenMaterial.uniforms.uGamma.value=t,this.screenMaterial.uniforms.uGlow.value=e,this.screenMaterial.uniforms.uAlphaSingle.value=s}render(t,e,s,i){i?(t.setRenderTarget(this.accumTarget),t.clear(),t.render(e,s),t.setRenderTarget(null),t.render(this.screenScene,this.screenCamera)):(t.setRenderTarget(null),t.render(e,s))}dispose(){this.screenMaterial.dispose(),this.accumTarget.dispose()}}class Ht{container;callbacks;zCamera;canvas;renderer;scene=new R;points;material;overlayScene=new R;emphasisPoints;emphasisMaterial;hasSelection=!1;selection=new vt;pipeline=new zt;lasso;picker;clicks;resizeObserver;listeners=new AbortController;viewProjection=new J;adapter=null;adapterHasZ=!1;cols=null;colorAttribute=null;emphasisMask=new Float32Array(0);emphasisAttribute=null;visibleMask=null;visibleAttribute=null;settings=P;interactionMode="select";width=0;height=0;renderQueued=!1;rafHandle=null;disposed=!1;constructor(t,e={},s={}){this.container=t,this.callbacks=e,this.zCamera=s.zCamera??null,getComputedStyle(t).position==="static"&&(t.style.position="relative"),this.canvas=document.createElement("canvas"),Object.assign(this.canvas.style,{position:"absolute",inset:"0",width:"100%",height:"100%"}),t.prepend(this.canvas),this.renderer=new tt({canvas:this.canvas,alpha:!0,antialias:!1,powerPreference:"high-performance"}),this.renderer.setPixelRatio(window.devicePixelRatio||1),this.renderer.sortObjects=!1,this.renderer.setClearColor(0,0),this.material=new _({vertexShader:bt,fragmentShader:Mt,uniforms:{uPointSize:{value:G*(window.devicePixelRatio||1)},uHasSelection:{value:0},uMode:{value:1},uOpacity:{value:P.singleAlpha}},transparent:!0,blending:H,blendSrc:z,blendDst:z,blendSrcAlpha:z,blendDstAlpha:z,depthTest:!1,depthWrite:!1}),this.points=new X(new T,this.material),this.points.frustumCulled=!1,this.scene.add(this.points),this.emphasisMaterial=new _({vertexShader:St,fragmentShader:At,uniforms:{uPointSize:{value:(G+ot)*(window.devicePixelRatio||1)}},transparent:!0,depthTest:!1,depthWrite:!1}),this.emphasisPoints=new X(this.points.geometry,this.emphasisMaterial),this.emphasisPoints.frustumCulled=!1,this.overlayScene.add(this.emphasisPoints),this.lasso=new xt(t,{shouldStart:i=>this.adapter?.isLassoStart(i)??!1,onComplete:(i,n,a)=>this.handleLasso(i,n,a)}),this.picker=new wt(t,{isBlocked:()=>this.lasso.isDrawing(),pick:(i,n)=>this.pick(i,n),onHover:i=>this.callbacks.onHover?.(i)}),this.clicks=new mt(t,{onClick:(i,n)=>this.handleClick(i,n)}),t.addEventListener("dblclick",()=>{this.adapter?.reset(),this.requestRender()},{signal:this.listeners.signal}),this.resizeObserver=new ResizeObserver(()=>this.resize()),this.resizeObserver.observe(t),this.resize()}setData(t){const e=ht(t,this.zCamera===null);this.cols=e;const s=new Float32Array(e.n*3);for(let n=0;n<e.n;n++)s[n*3]=e.xs[n],s[n*3+1]=e.ys[n],s[n*3+2]=e.zs[n];this.points.geometry.dispose();const i=new T;i.setAttribute("position",new C(s,3)),this.colorAttribute=new C(U(e,B),3),i.setAttribute("color",this.colorAttribute),this.emphasisMask=new Float32Array(e.n),this.emphasisAttribute=new C(this.emphasisMask,1).setUsage(F),i.setAttribute("emphasis",this.emphasisAttribute),this.visibleMask=null,this.visibleAttribute=new C(new Uint8Array(e.n).fill(1),1).setUsage(F),i.setAttribute("visible",this.visibleAttribute),i.boundingSphere=new q(new $(0,0,0),1),this.points.geometry=i,this.emphasisPoints.geometry=i,this.clearSelection(),this.ensureAdapter(e.hasZ),this.adapter?.setBounds(e,this.width,this.height),this.picker.reset(),this.requestRender(),this.callbacks.onSelection?.([])}setColors(t){const{cols:e,colorAttribute:s}=this;if(!e||!s)return;const i=t??U(e,B);if(i.length!==e.n*3)throw new Error(`setColors expects ${e.n*3} floats (n·rgb), got ${i.length}`);s.array.set(i),s.needsUpdate=!0,this.requestRender()}setVisible(t){const{cols:e,visibleAttribute:s}=this;if(!e||!s)return;if(t&&t.length!==e.n)throw new Error(`setVisible expects ${e.n} bytes (one per point), got ${t.length}`);const i=s.array;if(t?(i.set(t),this.visibleMask=i):(i.fill(1),this.visibleMask=null),this.adapter?.setFocus){const n=t?ct(e,t):null;(!t||n)&&this.adapter.setFocus(n)}s.needsUpdate=!0,this.picker.viewChanged(),this.requestRender()}setSelected(t){this.applySelection(this.selection.writeHost(t))}clearSelection(){this.applySelection(this.selection.clear())}applySelection(t){const{cols:e,emphasisAttribute:s}=this;if(!(!e||!s)){if(this.emphasisMask.fill(0),t)for(let i=0;i<t.length;i++){const n=t[i];n>=0&&n<e.n&&(this.emphasisMask[n]=1)}this.hasSelection=t!==null,this.material.uniforms.uHasSelection.value=this.hasSelection?1:0,s.needsUpdate=!0,this.requestRender()}}resetCamera(){this.adapter?.reset(),this.requestRender()}setInteractionMode(t){this.interactionMode=t,this.adapter?.setMode?.(t),this.applyCursor()}setRenderSettings(t){this.settings=t;const{mode:e,singleAlpha:s}=t,i=e==="opaque";this.material.uniforms.uMode.value=e==="density"?1:i?2:0,this.material.blending=e==="density"?H:et,this.material.depthTest=i,this.material.depthWrite=i,this.material.uniforms.uOpacity.value=s,this.pipeline.applySettings(t),this.requestRender()}destroy(){this.disposed=!0,this.rafHandle!==null&&(cancelAnimationFrame(this.rafHandle),this.rafHandle=null),this.picker.destroy(),this.lasso.destroy(),this.clicks.destroy(),this.adapter?.destroy(),this.listeners.abort(),this.resizeObserver.disconnect(),this.points.geometry.dispose(),this.material.dispose(),this.emphasisMaterial.dispose(),this.pipeline.dispose(),this.renderer.dispose(),this.renderer.forceContextLoss(),this.canvas.remove()}ensureAdapter(t){if(this.adapter&&this.adapterHasZ===t)return;this.adapter?.destroy();const e=()=>{this.requestRender(),this.picker.viewChanged()};this.adapter=t&&this.zCamera?this.zCamera(this.container,e):new gt(this.container,e),this.adapter.setMode?.(this.interactionMode),this.adapterHasZ=t,this.applyCursor()}applyCursor(){if(!this.adapter?.setMode){this.container.style.cursor="";return}this.container.style.cursor=this.interactionMode==="select"?"crosshair":"grab"}currentViewProjection(){const t=this.adapter?.camera;return t?(t.updateMatrixWorld(),this.viewProjection.multiplyMatrices(t.projectionMatrix,t.matrixWorldInverse).elements):null}pick(t,e){const{cols:s}=this,i=this.currentViewProjection();return!s||!i?null:yt(s,i,this.width,this.height,t,e,lt,this.visibleMask)}handleLasso(t,e,s){if(!t){this.handleClick(e,s);return}const{cols:i}=this,n=this.currentViewProjection();if(!i||!n)return;const a=ft(i,n,this.width,this.height,t,this.visibleMask);this.applySelection(this.selection.writeLasso(a.length>0?a:null)),this.callbacks.onSelection?.(a,this.adapter?.toDataPolygon?.(t)??null)}handleClick(t,e){const s=this.pick(t,e);if(s&&this.callbacks.onPointClick){this.callbacks.onPointClick(s);return}this.applySelection(this.selection.writeLasso(null)),this.callbacks.onSelection?.([]),s||this.callbacks.onBackgroundClick?.()}resize(){const t=this.container.clientWidth||1,e=this.container.clientHeight||1;if(t===this.width&&e===this.height)return;this.width=t,this.height=e;const s=window.devicePixelRatio||1;this.renderer.setSize(t,e,!1),this.pipeline.setSize(Math.round(t*s),Math.round(e*s)),this.adapter?.resize(t,e),this.requestRender()}requestRender(){this.renderQueued||this.disposed||(this.renderQueued=!0,this.rafHandle=requestAnimationFrame(()=>{this.rafHandle=null,this.renderQueued=!1,this.render()}))}render(){const t=this.adapter?.camera;t&&(this.pipeline.render(this.renderer,this.scene,t,this.settings.mode==="density"),this.hasSelection&&(this.renderer.autoClear=!1,this.renderer.render(this.overlayScene,t),this.renderer.autoClear=!0))}}export{Ht as EmbeddingsChart};
