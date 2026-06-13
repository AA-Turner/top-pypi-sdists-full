import{L as $}from"./CircularLoading-223w4e_R.js";import{e as P,r as d,$ as q,E as C,N as M,f as l,j as R,q as m,bc as W,J as V,V as j,g as p,ar as B}from"./jwt-decode.esm-01iVuizL.js";import{W as J}from"./Watermark-DfAB5ULw.js";import{u as v}from"./userStore-iHeQ9myT.js";import{b as T,l as U}from"./workspaceStore-BhaNP0o0.js";import{b as A,a as N}from"./consoleCapture-CTAnNYCQ.js";(function(){try{var a=typeof window<"u"?window:typeof global<"u"?global:typeof self<"u"?self:{},t=new Error().stack;t&&(a._sentryDebugIds=a._sentryDebugIds||{},a._sentryDebugIds[t]="cd6a7b8a-bb3c-4329-89ee-8a799cc0e4ea",a._sentryDebugIdIdentifier="sentry-dbid-cd6a7b8a-bb3c-4329-89ee-8a799cc0e4ea")}catch{}})();function X(){return`<script>
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
<\/script>`}const F={class:"page-container"},H={key:0,class:"loading"},O={key:1,class:"error-container"},z=["srcdoc"],G=P({__name:"PageStageView",props:{uiData:{}},setup(a){const t=a,i=V(),h=j(),f=d(!0),c=d(""),o=d(!1),w=d(null);async function g(){const e=v();e.loadJWT(),f.value=!0,o.value=!1,c.value="";try{const n=t.uiData.path?`/_page/${t.uiData.path}`:"/_page-home",r=await T(n+window.location.search,{headers:e.authHeaders});if(r.status===401){e.removeJWT(),i.push({name:"playerLogin",query:{redirect:`/${t.uiData.path}`}});return}if(r.ok){const u=await r.text(),s=r.headers.get("X-Execution-Id"),y=r.headers.get("X-Abstra-Debug")==="true";if(u){const _=`<base href="${n}" target="_top">`,k=window.location.search.replace(/&/g,"&amp;").replace(/"/g,"&quot;"),D=`<meta name="abstra-page-endpoint" content="${n}${k}">`,x=X(),I=A(),E=e.jwt?`<meta name="abstra-auth-token" content="${e.jwt}">`:"",L=s?`<meta name="abstra-execution-id" content="${s}">`:"",S=s&&y?N(s,t.uiData.id):"";c.value=_+D+E+L+x+I+S+u}else o.value=!0}else o.value=!0}catch{o.value=!0}f.value=!1}function b(e){if(e.origin!==window.location.origin||!e.data)return;if(e.data.type==="abstra-login"){i.push({name:"playerLogin",query:{redirect:`/${t.uiData.path}`}});return}if(e.data.type==="abstra-logout"){v().removeJWT(),U(),g();return}if(e.data.type!=="abstra-page-navigate")return;const n=typeof e.data.search=="string"?e.data.search:"",r=typeof e.data.hash=="string"?e.data.hash:"",u=Object.fromEntries(new URLSearchParams(n));i.replace({path:h.path,query:u,hash:r||void 0})}return q(()=>{window.addEventListener("message",b),g()}),C(()=>{window.removeEventListener("message",b)}),M(()=>h.query,()=>{g()}),(e,n)=>(p(),l("div",F,[f.value?(p(),l("div",H,[m($)])):o.value?(p(),l("div",O,[m(W,{"error-message":null,"execution-id":null,locale:"en"})])):c.value?(p(),l("iframe",{key:2,ref_key:"iframeRef",ref:w,class:"page-iframe",srcdoc:c.value},null,8,z)):R("",!0),m(J,{"page-id":a.uiData.id,locale:"en"},null,8,["page-id"])]))}}),ae=B(G,[["__scopeId","data-v-0a019559"]]);export{ae as P};
//# sourceMappingURL=PageStageView-BOFXhF2K.js.map
