import{L as E}from"./CircularLoading-DSdNy3OB.js";import{e as L,r as u,M,K as P,C,f as d,j as R,q as g,bu as S,ae as $,aj as j,g as l,aM as q}from"./jwt-decode.esm-CMj0qxed.js";import{W}from"./Watermark-CDhf7chX.js";import{u as U}from"./userStore-JzsU92N_.js";import{b as V}from"./consoleCapture-CqJUCI7W.js";import{b as T}from"./workspaceStore-BpM_nIpQ.js";(function(){try{var t=typeof window<"u"?window:typeof global<"u"?global:typeof self<"u"?self:{},a=new Error().stack;a&&(t._sentryDebugIds=t._sentryDebugIds||{},t._sentryDebugIds[a]="09324036-9147-4457-8dee-1b73081a6659",t._sentryDebugIdIdentifier="sentry-dbid-09324036-9147-4457-8dee-1b73081a6659")}catch{}})();function A(){return`<script>
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
<\/script>`}const B={class:"page-container"},J={key:0,class:"loading"},N={key:1,class:"error-container"},X=["srcdoc"],F=L({__name:"PageStageView",props:{uiData:{}},setup(t){const a=t,p=$(),m=j(),f=u(!0),s=u(""),o=u(!1),b=u(null);async function h(){const e=U();e.loadJWT(),f.value=!0,o.value=!1,s.value="";try{const n=a.uiData.path?`/_page/${a.uiData.path}`:"/_page-home",r=await T(n+window.location.search,{headers:e.authHeaders});if(r.status===401){e.removeJWT(),p.push({name:"playerLogin",query:{redirect:`/${a.uiData.path}`}});return}if(r.ok){const i=await r.text(),c=r.headers.get("X-Execution-Id"),_=r.headers.get("X-Abstra-Debug")==="true";if(i){const y=`<base href="${n}" target="_top">`,w=`<meta name="abstra-page-endpoint" content="${n}">`,k=A(),D=e.jwt?`<meta name="abstra-auth-token" content="${e.jwt}">`:"",x=c?`<meta name="abstra-execution-id" content="${c}">`:"",I=c&&_?V(c,a.uiData.id):"";s.value=y+w+D+x+k+I+i}else o.value=!0}else o.value=!0}catch{o.value=!0}f.value=!1}function v(e){if(e.origin!==window.location.origin||!e.data||e.data.type!=="abstra-page-navigate")return;const n=typeof e.data.search=="string"?e.data.search:"",r=typeof e.data.hash=="string"?e.data.hash:"",i=Object.fromEntries(new URLSearchParams(n));p.replace({path:m.path,query:i,hash:r||void 0})}return M(()=>{window.addEventListener("message",v),h()}),P(()=>{window.removeEventListener("message",v)}),C(()=>m.query,()=>{h()}),(e,n)=>(l(),d("div",B,[f.value?(l(),d("div",J,[g(E)])):o.value?(l(),d("div",N,[g(S,{"error-message":null,"execution-id":null,locale:"en"})])):s.value?(l(),d("iframe",{key:2,ref_key:"iframeRef",ref:b,class:"page-iframe",srcdoc:s.value},null,8,X)):R("",!0),g(W,{"page-id":t.uiData.id,locale:"en"},null,8,["page-id"])]))}}),Y=q(F,[["__scopeId","data-v-dba6ede6"]]);export{Y as P};
//# sourceMappingURL=PageStageView-CIVVQjwv.js.map
