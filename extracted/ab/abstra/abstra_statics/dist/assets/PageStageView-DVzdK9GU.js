import{L as P}from"./CircularLoading-D28qBOBt.js";import{e as $,r as d,n as q,l as C,O as M,f as l,j as R,x as m,bb as W,K as V,V as j,g as p,ar as B}from"./jwt-decode.esm-DNXB6x7p.js";import{W as T}from"./Watermark-D_N41MG3.js";import{u as v}from"./userStore-CkOgc8ws.js";import{b as U,l as A}from"./workspaceStore-DznSgMwr.js";import{b as J,a as N}from"./consoleCapture-BgsIQUeO.js";(function(){try{var a=typeof window<"u"?window:typeof global<"u"?global:typeof self<"u"?self:{},t=new Error().stack;t&&(a._sentryDebugIds=a._sentryDebugIds||{},a._sentryDebugIds[t]="134a995f-f43b-4b0c-bc57-3d7be7f3fc6d",a._sentryDebugIdIdentifier="sentry-dbid-134a995f-f43b-4b0c-bc57-3d7be7f3fc6d")}catch{}})();function O(){return`<script>
(function() {
  var meta = document.querySelector('meta[name="abstra-page-endpoint"]');
  var rpcPrefix = meta && meta.content;
  if (!rpcPrefix) return;
  document.addEventListener('click', function(e) {
    var a = e.target && e.target.closest && e.target.closest('a');
    if (!a) return;
    // <base target="_top"> applies when target is "" or "_top". Anything
    // else (_self, _blank, _parent, framename) keeps default behavior.
    if (a.target !== '' && a.target !== '_top') return;
    var url;
    try { url = new URL(a.href); } catch (err) { return; }
    if (url.origin !== window.origin) return;
    if (url.pathname !== rpcPrefix) return;
    e.preventDefault();
    window.parent.postMessage(
      { type: 'abstra-page-navigate', search: url.search, hash: url.hash },
      window.origin
    );
  }, true);
})();
<\/script>`}const X={class:"page-container"},F={key:0,class:"loading"},H={key:1,class:"error-container"},K=["srcdoc"],z=$({__name:"PageStageView",props:{uiData:{}},setup(a){const t=a,i=V(),h=j(),f=d(!0),c=d(""),o=d(!1),w=d(null);async function g(){const e=v();e.loadJWT(),f.value=!0,o.value=!1,c.value="";try{const n=t.uiData.path?`/_page/${t.uiData.path}`:"/_page-home",r=await U(n+window.location.search,{headers:e.authHeaders});if(r.status===401){e.removeJWT(),i.push({name:"playerLogin",query:{redirect:`/${t.uiData.path}`}});return}if(r.ok){const u=await r.text(),s=r.headers.get("X-Execution-Id"),y=r.headers.get("X-Abstra-Debug")==="true";if(u){const _=`<base href="${n}" target="_top">`,k=window.location.search.replace(/&/g,"&amp;").replace(/"/g,"&quot;"),D=`<meta name="abstra-page-endpoint" content="${n}${k}">`,x=O(),I=J(),E=e.jwt?`<meta name="abstra-auth-token" content="${e.jwt}">`:"",L=s?`<meta name="abstra-execution-id" content="${s}">`:"",S=s&&y?N(s,t.uiData.id):"";c.value=_+D+E+L+x+I+S+u}else o.value=!0}else o.value=!0}catch{o.value=!0}f.value=!1}function b(e){if(e.origin!==window.location.origin||!e.data)return;if(e.data.type==="abstra-login"){i.push({name:"playerLogin",query:{redirect:`/${t.uiData.path}`}});return}if(e.data.type==="abstra-logout"){v().removeJWT(),A(),g();return}if(e.data.type!=="abstra-page-navigate")return;const n=typeof e.data.search=="string"?e.data.search:"",r=typeof e.data.hash=="string"?e.data.hash:"",u=Object.fromEntries(new URLSearchParams(n));i.replace({path:h.path,query:u,hash:r||void 0})}return q(()=>{window.addEventListener("message",b),g()}),C(()=>{window.removeEventListener("message",b)}),M(()=>h.query,()=>{g()}),(e,n)=>(p(),l("div",X,[f.value?(p(),l("div",F,[m(P)])):o.value?(p(),l("div",H,[m(W,{"error-message":null,"execution-id":null,locale:"en"})])):c.value?(p(),l("iframe",{key:2,ref_key:"iframeRef",ref:w,class:"page-iframe",srcdoc:c.value},null,8,K)):R("",!0),m(T,{"page-id":a.uiData.id,locale:"en"},null,8,["page-id"])]))}}),ae=B(z,[["__scopeId","data-v-0a019559"]]);export{ae as P};
//# sourceMappingURL=PageStageView-DVzdK9GU.js.map
