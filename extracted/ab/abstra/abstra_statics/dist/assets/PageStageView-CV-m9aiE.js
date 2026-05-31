import{L}from"./CircularLoading-Czg0Kjby.js";import{e as M,r as u,M as P,K as C,C as S,f as l,j as $,q as g,bu as q,ae as R,aj as j,g as d,aM as W}from"./jwt-decode.esm-RrwddusF.js";import{W as U}from"./Watermark-BcLZ6Ip3.js";import{u as V}from"./userStore-CnYDBR7j.js";import{b as T}from"./consoleCapture-CoIJycMz.js";import{b as A}from"./workspaceStore-T_JwO0pO.js";(function(){try{var t=typeof window<"u"?window:typeof global<"u"?global:typeof self<"u"?self:{},a=new Error().stack;a&&(t._sentryDebugIds=t._sentryDebugIds||{},t._sentryDebugIds[a]="7fc94f03-4c35-4f72-ba11-ebb66ff7fefd",t._sentryDebugIdIdentifier="sentry-dbid-7fc94f03-4c35-4f72-ba11-ebb66ff7fefd")}catch{}})();function B(){return`<script>
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
    if (url.origin !== location.origin) return;
    if (url.pathname !== rpcPrefix) return;
    e.preventDefault();
    window.parent.postMessage(
      { type: 'abstra-page-navigate', search: url.search, hash: url.hash },
      location.origin
    );
  }, true);
})();
<\/script>`}const J={class:"page-container"},N={key:0,class:"loading"},X={key:1,class:"error-container"},F=["srcdoc"],H=M({__name:"PageStageView",props:{uiData:{}},setup(t){const a=t,f=R(),m=j(),p=u(!0),s=u(""),o=u(!1),v=u(null);async function h(){const e=V();e.loadJWT(),p.value=!0,o.value=!1,s.value="";try{const n=a.uiData.path?`/_page/${a.uiData.path}`:"/_page-home",r=await A(n+window.location.search,{headers:e.authHeaders});if(r.status===401){e.removeJWT(),f.push({name:"playerLogin",query:{redirect:`/${a.uiData.path}`}});return}if(r.ok){const i=await r.text(),c=r.headers.get("X-Execution-Id"),_=r.headers.get("X-Abstra-Debug")==="true";if(i){const w=`<base href="${n}" target="_top">`,y=window.location.search.replace(/&/g,"&amp;").replace(/"/g,"&quot;"),k=`<meta name="abstra-page-endpoint" content="${n}${y}">`,D=B(),x=e.jwt?`<meta name="abstra-auth-token" content="${e.jwt}">`:"",I=c?`<meta name="abstra-execution-id" content="${c}">`:"",E=c&&_?T(c,a.uiData.id):"";s.value=w+k+x+I+D+E+i}else o.value=!0}else o.value=!0}catch{o.value=!0}p.value=!1}function b(e){if(e.origin!==window.location.origin||!e.data||e.data.type!=="abstra-page-navigate")return;const n=typeof e.data.search=="string"?e.data.search:"",r=typeof e.data.hash=="string"?e.data.hash:"",i=Object.fromEntries(new URLSearchParams(n));f.replace({path:m.path,query:i,hash:r||void 0})}return P(()=>{window.addEventListener("message",b),h()}),C(()=>{window.removeEventListener("message",b)}),S(()=>m.query,()=>{h()}),(e,n)=>(d(),l("div",J,[p.value?(d(),l("div",N,[g(L)])):o.value?(d(),l("div",X,[g(q,{"error-message":null,"execution-id":null,locale:"en"})])):s.value?(d(),l("iframe",{key:2,ref_key:"iframeRef",ref:v,class:"page-iframe",srcdoc:s.value},null,8,F)):$("",!0),g(U,{"page-id":t.uiData.id,locale:"en"},null,8,["page-id"])]))}}),Z=W(H,[["__scopeId","data-v-7e807aeb"]]);export{Z as P};
//# sourceMappingURL=PageStageView-CV-m9aiE.js.map
