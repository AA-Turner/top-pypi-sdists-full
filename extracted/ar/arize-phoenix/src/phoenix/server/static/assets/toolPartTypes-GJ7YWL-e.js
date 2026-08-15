import{o as e}from"./rolldown-runtime-C_s2cVnS.js";import{$n as t,$t as n,An as r,Bn as i,Ct as a,Dn as o,En as s,Er as c,Fn as l,Hn as u,In as d,Jn as f,Kn as p,Ln as m,Nn as h,On as g,Qn as _,Qt as v,Rn as y,Sn as b,Sr as x,Tn as S,Un as C,Vn as w,Xn as T,Yn as E,Zn as D,_r as O,_t as k,an as A,ar as j,at as M,bn as ee,br as te,bt as ne,cn as N,cr as re,dn as ie,dr as ae,en as oe,fn as se,fr as ce,gr as le,hn as ue,ht as de,ir as fe,it as pe,jn as me,kn as he,ln as ge,mn as _e,mr as ve,mt as ye,nn as be,nr as xe,on as Se,or as Ce,ot as we,pn as Te,pr as Ee,qn as De,rn as Oe,rt as ke,sn as Ae,sr as je,st as Me,tr as Ne,ur as Pe,vn as Fe,vr as Ie,vt as Le,wn as Re,wt as ze,xn as Be,xr as Ve,yn as He,yr as Ue,zn as We}from"./vendor-D6rkHpRE.js";import{D as Ge,M as P,d as Ke,rt as qe,u as Je,v as Ye,x as Xe,y as Ze}from"./vendor-codemirror-C30l0yEq.js";import{C as F,b as Qe,w as $e,y as I}from"./vendor-recharts-B_R8BYY6.js";import{$ as et,A as tt,C as nt,Cn as rt,D as L,Di as it,Dt as at,E as ot,Eo as st,Et as ct,F as lt,Fn as ut,Fo as R,Ft as dt,G as z,Gn as ft,Gt as pt,H as mt,Ha as ht,Ht as gt,Io as B,J as _t,Jr as vt,Jt as yt,K as bt,Ki as xt,Kr as St,Kt as Ct,L as wt,Ln as Tt,Lo as V,Lt as Et,M as Dt,Mi as Ot,Mn as kt,Na as At,Nn as jt,Nt as Mt,O as Nt,On as Pt,P as H,Pa as Ft,R as It,Ro as Lt,Rt,S as zt,Sn as Bt,T as Vt,Tt as Ht,Ui as Ut,Ur as Wt,Ut as Gt,Vi as Kt,Vr as U,Vt as qt,W as Jt,Wa as Yt,Wn as Xt,Wr as Zt,Wt as Qt,Xa as $t,Xi as en,Xr as tn,Xt as nn,Y as rn,Yr as an,Zr as on,_t as sn,bt as cn,ci as ln,cn as un,ct as dn,di as fn,dr as pn,ei as mn,er as hn,fa as gn,gn as _n,gr as vn,gt as yn,hr as bn,i as xn,ia as Sn,j as Cn,jn as wn,k as Tn,ki as En,ln as Dn,m as On,mn as kn,mr as An,n as jn,oi as Mn,on as Nn,p as Pn,q as Fn,qn as In,qt as Ln,r as Rn,ra as zn,rr as Bn,rt as Vn,sa as Hn,sn as Un,sr as Wn,t as Gn,un as Kn,ur as qn,vr as Jn,vt as Yn,wi as Xn,x as Zn,xn as Qn,xr as $n,xt as er,y as tr,z as W}from"./vendor-streamdown-BLV5_fPs.js";import{Hn as G,It as nr,On as rr,Ut as ir,Vn as K,Xn as ar,kn as or,mr as sr,pr as cr,qt as lr,rn as ur,tr as q}from"./vendor-ai-sdk-react-Cnv2ri0b.js";var J=e(qe()),dr=e($e()),Y=Lt();function fr(e){throw Error(`Unreachable`)}function pr(e){return typeof e==`number`||e===null}function mr(e){return typeof e==`string`||e===null}function hr(e){return mr(e)||e===void 0}function gr(e){return Array.isArray(e)?e.every(e=>typeof e==`string`):!1}function _r(e){return typeof e==`object`&&!!e}function vr(e){return _r(e)&&Object.keys(e).every(e=>typeof e==`string`)}var yr=()=>e=>e;(0,J.createContext)(null);var br=5e3,xr=new _e({maxVisibleToasts:3}),Sr=()=>(0,J.useCallback)(({expireMs:e=br,...t})=>xr.add({...t},e===null?void 0:{timeout:e}),[]),Cr=()=>(0,J.useCallback)(({expireMs:e=br,...t})=>xr.add({...t,variant:`success`},e===null?void 0:{timeout:e}),[]),wr=()=>(0,J.useCallback)(({expireMs:e=br,...t})=>xr.add({...t,variant:`error`},e===null?void 0:{timeout:e}),[]);function Tr(e){return e===`light`||e===`dark`||e===`system`}var Er=`arize-phoenix-theme`,Dr=`dark`,Or=`(prefers-color-scheme: dark)`;function kr(){let e=localStorage.getItem(Er);return Tr(e)?e:Dr}function Ar(){return window.matchMedia(Or).matches?`dark`:`light`}var jr=(0,J.createContext)(null);function Mr(){let e=(0,J.useContext)(jr);if(e===null)throw Error(`useTheme must be used within a ThemeProvider`);return e}function Nr(e){let t=(0,Y.c)(19),n;t[0]===e.themeMode?n=t[1]:(n=()=>e.themeMode||kr(),t[0]=e.themeMode,t[1]=n);let[r,i]=(0,J.useState)(n),a;t[2]===Symbol.for(`react.memo_cache_sentinel`)?(a=e=>{localStorage.setItem(Er,e),i(e)},t[2]=a):a=t[2];let o=a,[s,c]=(0,J.useState)(Ar),l;bb0:{if(r===`system`){l=s;break bb0}l=r}let u=l,d,f;t[3]===e.themeMode?(d=t[4],f=t[5]):(d=()=>{e.themeMode&&i(e.themeMode)},f=[e.themeMode,o],t[3]=e.themeMode,t[4]=d,t[5]=f),(0,J.useEffect)(d,f);let p,m;t[6]===Symbol.for(`react.memo_cache_sentinel`)?(p=()=>{let e=window.matchMedia(Or),t=()=>{c(Ar())};return e.addEventListener(`change`,t),()=>{e.removeEventListener(`change`,t)}},m=[],t[6]=p,t[7]=m):(p=t[6],m=t[7]),(0,J.useEffect)(p,m);let h,g;t[8]!==e.disableBodyTheme||t[9]!==u?(h=()=>{if(!e.disableBodyTheme)return document.body.classList.add(`theme--${u}`),document.body.classList.add(`theme`),()=>{document.body.classList.remove(`theme--${u}`),document.body.classList.remove(`theme`)}},g=[u,e.disableBodyTheme],t[8]=e.disableBodyTheme,t[9]=u,t[10]=h,t[11]=g):(h=t[10],g=t[11]),(0,J.useEffect)(h,g);let _;t[12]!==s||t[13]!==u||t[14]!==r?(_={theme:u,systemTheme:s,themeMode:r,setThemeMode:o},t[12]=s,t[13]=u,t[14]=r,t[15]=_):_=t[15];let v;return t[16]!==e.children||t[17]!==_?(v=B(jr.Provider,{value:_,children:e.children}),t[16]=e.children,t[17]=_,t[18]=v):v=t[18],v}var Pr=[`traces`,`spans`,`sessions`,`metrics`],Fr=e=>Pr.includes(e),Ir=[`traffic`,`traces`,`latency`,`cost`,`top_models_by_cost`,`tokens`,`top_models_by_tokens`,`prompt_token_details`,`completion_token_details`,`llm_spans`,`llm_span_errors`,`tool_spans`,`tool_span_errors`,`span_annotations`,`trace_annotations`,`session_annotations`],Lr=[`spans`,`traces`,`sessions`],Rr=`Evaluation results over time`,zr=`_annotation:`;function Br({view:e,annotationName:t}){return`${e}${zr}${t}`}function Vr(e){for(let t of Lr){let n=`${t}${zr}`;if(e.startsWith(n))return{view:t,annotationName:e.slice(n.length)}}}var Hr=e=>Ir.includes(e)||Vr(e)!=null,Ur={spans:[`traffic`],traces:[`traces`,`latency`,`trace_annotations`],sessions:[`traces`,`session_annotations`]},Wr=e=>`arize-phoenix-project-${e}`;function Gr({projectId:e}){return{state:oe()(n(v(e=>({defaultTab:`spans`,setDefaultTab:t=>{e({defaultTab:t},!1,{type:`setDefaultTab`})},showTableAside:!0,setShowTableAside:t=>{e({showTableAside:t},!1,{type:`setShowTableAside`})},metricChartKeys:Ur,setMetricChartKeys:(t,n)=>{e(e=>({metricChartKeys:{...e.metricChartKeys,[t]:n}}),!1,{type:`setMetricChartKeys`})}})),{name:Wr(e),merge:(e,t)=>{let n={...t,...e},r={...Ur};for(let e of Lr){let t=n.metricChartKeys?.[e];Array.isArray(t)&&(r[e]=t.filter(Hr))}return n.metricChartKeys=r,n}}))}}var Kr=(0,J.createContext)(null);function qr(e){let t=(0,Y.c)(5),{children:n,projectId:r}=e,i;t[0]===r?i=t[1]:(i=()=>Gr({projectId:r}),t[0]=r,t[1]=i);let[a]=(0,J.useState)(i),o;return t[2]!==n||t[3]!==a?(o=B(Kr.Provider,{value:a,children:n}),t[2]=n,t[3]=a,t[4]=o):o=t[4],o}function Jr(e,t){let n=(0,J.useContext)(Kr);if(!n)throw Error(`Missing ProjectContext.Provider in the tree`);return be(n.state,e,t)}var Yr=[`Python`,`TypeScript`];function Xr(e){return typeof e==`string`&&Yr.includes(e)}var Zr=[`npm`,`pnpm`,`bun`],Qr=[`pip`,`uv`],$r=[...Zr,...Qr];function ei(e){return typeof e==`string`&&$r.includes(e)}function ti(e){return typeof e==`string`&&Qr.includes(e)}function ni(e){return typeof e==`string`&&Zr.includes(e)}var ri=Intl.DateTimeFormat().resolvedOptions(),ii=[];function ai(){return ri.locale}function oi(){return ri.timeZone}function si(){return ii.length===0&&(ii=[...Intl.supportedValuesOf(`timeZone`)],ii.includes(`UTC`)||(ii=[`UTC`,...ii])),Object.freeze([...ii])}function ci(e,t){let n=new Intl.DateTimeFormat(`en-US`,{timeZone:t,year:`numeric`,month:`2-digit`,day:`2-digit`,hour:`2-digit`,minute:`2-digit`,second:`2-digit`,hour12:!1}).formatToParts(e).reduce((e,t)=>(t.type!==`literal`&&(e[t.type]=t.value),e),{}),{year:r,month:i,day:a}=n,o=n.hour;if(o===`24`){o=`00`;let e=new Date(`${r}-${i}-${a}T00:00:00Z`);e.setUTCDate(e.getUTCDate()+1),r=String(e.getUTCFullYear()),i=String(e.getUTCMonth()+1).padStart(2,`0`),a=String(e.getUTCDate()).padStart(2,`0`)}let s=`${r}-${i}-${a}`,c=`${o}:${n.minute}:${n.second}`,l=new Date(`${s}T${c}Z`).getTime(),u=Math.round((l-e.getTime())/6e4),d=u>=0?`+`:`-`,f=Math.abs(u);return`${s}T${c}${d}${String(Math.floor(f/60)).padStart(2,`0`)}:${String(f%60).padStart(2,`0`)}`}var li={Python:Qr,TypeScript:Zr},ui={Python:`pip`,TypeScript:`npm`},di=[``,`apac`,`au`,`ca`,`eu`,`global`,`il`,`jp`,`us`,`us-gov`],fi=e=>oe()(n(v(t=>({markdownDisplayMode:`text`,setMarkdownDisplayMode:e=>{t({markdownDisplayMode:e},!1,{type:`setMarkdownDisplayMode`})},traceStreamingEnabled:!0,setTraceStreamingEnabled:e=>{t({traceStreamingEnabled:e},!1,{type:`setTraceStreamingEnabled`})},lastNTimeRangeKey:`7d`,setLastNTimeRangeKey:e=>{t({lastNTimeRangeKey:e})},projectsAutoRefreshEnabled:!0,setProjectAutoRefreshEnabled:e=>{t({projectsAutoRefreshEnabled:e},!1,{type:`setProjectAutoRefreshEnabled`})},showMetricsInTraceTree:!0,setShowMetricsInTraceTree:e=>{t({showMetricsInTraceTree:e},!1,{type:`setShowMetricsInTraceTree`})},areTableRowsExpanded:!1,setAreTableRowsExpanded:e=>{t({areTableRowsExpanded:e},!1,{type:`setAreTableRowsExpanded`})},modelConfigByProvider:{},setModelConfigForProvider:({provider:e,modelConfig:n})=>{t(t=>({modelConfigByProvider:{...t.modelConfigByProvider,[e]:n}}),!1,{type:`setModelConfigForProvider`})},playgroundStreamingEnabled:!0,setPlaygroundStreamingEnabled:e=>{t({playgroundStreamingEnabled:e},!1,{type:`setPlaygroundStreamingEnabled`})},isAnnotatingSpans:!1,setIsAnnotatingSpans:e=>{t({isAnnotatingSpans:e},!1,{type:`setIsAnnotatingSpans`})},isTakingSpanNotes:!1,setIsTakingSpanNotes:e=>{t({isTakingSpanNotes:e},!1,{type:`setIsTakingSpanNotes`})},projectViewMode:`grid`,setProjectViewMode:e=>{t({projectViewMode:e},!1,{type:`setProjectViewMode`})},projectSortOrder:{column:`endTime`,direction:`desc`},setProjectSortOrder:e=>{t({projectSortOrder:e},!1,{type:`setProjectSortOrder`})},lastSelectedDashboardProjectId:void 0,setLastSelectedDashboardProjectId:e=>{t({lastSelectedDashboardProjectId:e},!1,{type:`setLastSelectedDashboardProjectId`})},isSideNavExpanded:!0,setIsSideNavExpanded:e=>{t({isSideNavExpanded:e},!1,{type:`setIsSideNavExpanded`})},setDisplayTimezone:e=>{if(e&&!si().includes(e))throw Error(`Invalid timezone: ${e}`);t({displayTimezone:e},!1,{type:`setDisplayTimezone`})},programmingLanguage:`Python`,setProgrammingLanguage:e=>{t({programmingLanguage:e},!1,{type:`setProgrammingLanguage`})},packageManagerByLanguage:{...ui},setPackageManager:(e,n)=>{t(t=>({packageManagerByLanguage:{...t.packageManagerByLanguage,[e]:n}}),!1,{type:`setPackageManager`})},awsBedrockModelPrefix:`us`,setAwsBedrockModelPrefix:e=>{t({awsBedrockModelPrefix:e},!1,{type:`setAwsBedrockModelPrefix`})},isAssistantAgentEnabled:!0,setIsAssistantAgentEnabled:e=>{t({isAssistantAgentEnabled:e},!1,{type:`setIsAssistantAgentEnabled`})},defaultModelProvider:void 0,setDefaultModelProvider:e=>{t({defaultModelProvider:e},!1,{type:`setDefaultModelProvider`})},defaultModelName:void 0,setDefaultModelName:e=>{let n=e?.trim();t({defaultModelName:n||void 0},!1,{type:`setDefaultModelName`})},isAIQueryEnabled:!0,setIsAIQueryEnabled:e=>{t({isAIQueryEnabled:e},!1,{type:`setIsAIQueryEnabled`})},aiQueryModelConfig:void 0,setAIQueryModelConfig:e=>{t({aiQueryModelConfig:e},!1,{type:`setAIQueryModelConfig`})},...e}),{name:`preferencesStore`}),{name:`arize-phoenix-preferences`})),pi=(0,J.createContext)(null);function mi(e){let t=(0,Y.c)(8),n,r;t[0]===e?(n=t[1],r=t[2]):({children:n,...r}=e,t[0]=e,t[1]=n,t[2]=r);let i;t[3]===r?i=t[4]:(i=()=>fi(r),t[3]=r,t[4]=i);let[a]=(0,J.useState)(i),o;return t[5]!==n||t[6]!==a?(o=B(pi.Provider,{value:a,children:n}),t[5]=n,t[6]=a,t[7]=o):o=t[7],o}function hi(e,t){let n=(0,J.useContext)(pi);if(!n)throw Error(`Missing PreferencesContext.Provider in the tree`);return be(n,e,t)}var gi=function(){var e={alias:null,args:null,kind:`ScalarField`,name:`id`,storageKey:null},t={alias:null,args:null,kind:`ScalarField`,name:`name`,storageKey:null},n={alias:null,args:null,kind:`ScalarField`,name:`createdAt`,storageKey:null},r={alias:null,args:null,kind:`ScalarField`,name:`expiresAt`,storageKey:null};return{fragment:{argumentDefinitions:[],kind:`Fragment`,metadata:null,name:`ViewerContextRefetchQuery`,selections:[{args:null,kind:`FragmentSpread`,name:`ViewerContext_viewer`}],type:`Query`,abstractKey:null},kind:`Request`,operation:{argumentDefinitions:[],kind:`Operation`,name:`ViewerContextRefetchQuery`,selections:[{alias:null,args:null,concreteType:`User`,kind:`LinkedField`,name:`viewer`,plural:!1,selections:[e,{alias:null,args:null,kind:`ScalarField`,name:`username`,storageKey:null},{alias:null,args:null,kind:`ScalarField`,name:`email`,storageKey:null},{alias:null,args:null,kind:`ScalarField`,name:`profilePictureUrl`,storageKey:null},{alias:null,args:null,kind:`ScalarField`,name:`isManagementUser`,storageKey:null},{alias:null,args:null,concreteType:`UserRole`,kind:`LinkedField`,name:`role`,plural:!1,selections:[t,e],storageKey:null},{alias:null,args:null,kind:`ScalarField`,name:`authMethod`,storageKey:null},{alias:null,args:null,concreteType:`UserApiKey`,kind:`LinkedField`,name:`apiKeys`,plural:!0,selections:[e,t,{alias:null,args:null,kind:`ScalarField`,name:`description`,storageKey:null},n,r],storageKey:null},{alias:null,args:null,concreteType:`OAuth2Grant`,kind:`LinkedField`,name:`oauth2Grants`,plural:!0,selections:[e,{alias:null,args:null,kind:`ScalarField`,name:`clientName`,storageKey:null},{alias:null,args:null,kind:`ScalarField`,name:`clientId`,storageKey:null},{alias:null,args:null,kind:`ScalarField`,name:`isFirstParty`,storageKey:null},{alias:null,args:null,kind:`ScalarField`,name:`scopes`,storageKey:null},n,r,{alias:null,args:null,kind:`ScalarField`,name:`lastUsedAt`,storageKey:null}],storageKey:null}],storageKey:null}]},params:{cacheID:`67fdf1bb616d5781701a75f68282f178`,id:null,metadata:{},name:`ViewerContextRefetchQuery`,operationKind:`query`,text:`query ViewerContextRefetchQuery {
  ...ViewerContext_viewer
}

fragment AuthorizedApplicationsCardFragment on User {
  id
  oauth2Grants {
    id
    clientName
    clientId
    isFirstParty
    scopes
    createdAt
    expiresAt
    lastUsedAt
  }
}

fragment ViewerAPIKeysListFragment on User {
  apiKeys {
    id
    name
    description
    createdAt
    expiresAt
  }
  id
}

fragment ViewerContext_viewer on Query {
  viewer {
    id
    username
    email
    profilePictureUrl
    isManagementUser
    role {
      name
      id
    }
    authMethod
    ...ViewerAPIKeysListFragment
    ...AuthorizedApplicationsCardFragment
  }
}
`}}}();gi.hash=`53341d080ff76da24b2f1bc9e36c4e23`;var _i={argumentDefinitions:[],kind:`Fragment`,metadata:{refetch:{connection:null,fragmentPathInResult:[],operation:gi}},name:`ViewerContext_viewer`,selections:[{alias:null,args:null,concreteType:`User`,kind:`LinkedField`,name:`viewer`,plural:!1,selections:[{alias:null,args:null,kind:`ScalarField`,name:`id`,storageKey:null},{alias:null,args:null,kind:`ScalarField`,name:`username`,storageKey:null},{alias:null,args:null,kind:`ScalarField`,name:`email`,storageKey:null},{alias:null,args:null,kind:`ScalarField`,name:`profilePictureUrl`,storageKey:null},{alias:null,args:null,kind:`ScalarField`,name:`isManagementUser`,storageKey:null},{alias:null,args:null,concreteType:`UserRole`,kind:`LinkedField`,name:`role`,plural:!1,selections:[{alias:null,args:null,kind:`ScalarField`,name:`name`,storageKey:null}],storageKey:null},{alias:null,args:null,kind:`ScalarField`,name:`authMethod`,storageKey:null},{args:null,kind:`FragmentSpread`,name:`ViewerAPIKeysListFragment`},{args:null,kind:`FragmentSpread`,name:`AuthorizedApplicationsCardFragment`}],storageKey:null}],type:`Query`,abstractKey:null};_i.hash=`53341d080ff76da24b2f1bc9e36c4e23`;var vi=c(),yi=J.createContext({viewer:null,refetchViewer:()=>{}});function bi(){let e=J.useContext(yi);if(e==null)throw Error(`useViewer must be used within a ViewerProvider`);return e}function xi(){let{viewer:e}=bi();return!(e&&e.role.name===`VIEWER`)}function Si(){let e=Ci();return!window.Config.authenticationEnabled||e}function Ci(){let{viewer:e}=bi();return window.Config.authenticationEnabled&&e?.role?.name===`ADMIN`}function wi(){return Si()}function Ti(){return Si()}function Ei(){return Si()}function Di(){return Si()}function Oi(){return Si()}function ki(e){let t=(0,Y.c)(9),{query:n,children:r}=e,i;t[0]===Symbol.for(`react.memo_cache_sentinel`)?(i=_i,t[0]=i):i=t[0];let[a,o]=(0,vi.useRefetchableFragment)(i,n),s;t[1]===o?s=t[2]:(s=()=>{(0,J.startTransition)(()=>{o({},{fetchPolicy:`network-only`})})},t[1]=o,t[2]=s);let c=s,l;t[3]!==a.viewer||t[4]!==c?(l={viewer:a.viewer,refetchViewer:c},t[3]=a.viewer,t[4]=c,t[5]=l):l=t[5];let u;return t[6]!==r||t[7]!==l?(u=B(yi.Provider,{value:l,children:r}),t[6]=r,t[7]=l,t[8]=u):u=t[8],u}var Ai={OPENAI:`OpenAI`,AZURE_OPENAI:`Azure OpenAI`,ANTHROPIC:`Anthropic`,GOOGLE:`Google`,DEEPSEEK:`DeepSeek`,XAI:`xAI`,OLLAMA:`Ollama`,AWS:`AWS Bedrock`,CEREBRAS:`Cerebras`,FIREWORKS:`Fireworks`,GROQ:`Groq`,MOONSHOT:`Moonshot`,PERPLEXITY:`Perplexity`,TOGETHER:`Together`},ji=`OPENAI`,Mi=`gpt-5.6-luna`,Ni=`user`,Pi=`RESPONSES`,Fi={user:[`user`,`human`],ai:[`assistant`,`bot`,`ai`,`model`],system:[`system`,`developer`],tool:[`tool`]},Ii={OPENAI:[{envVarName:`OPENAI_API_KEY`,isRequired:!0}],AZURE_OPENAI:[{envVarName:`AZURE_OPENAI_API_KEY`,isRequired:!0}],ANTHROPIC:[{envVarName:`ANTHROPIC_API_KEY`,isRequired:!0}],GOOGLE:[{envVarName:`GEMINI_API_KEY`,isRequired:!0}],DEEPSEEK:[{envVarName:`DEEPSEEK_API_KEY`,isRequired:!0}],XAI:[{envVarName:`XAI_API_KEY`,isRequired:!0}],OLLAMA:[],CEREBRAS:[{envVarName:`CEREBRAS_API_KEY`,isRequired:!0}],FIREWORKS:[{envVarName:`FIREWORKS_API_KEY`,isRequired:!0}],GROQ:[{envVarName:`GROQ_API_KEY`,isRequired:!0}],MOONSHOT:[{envVarName:`MOONSHOT_API_KEY`,isRequired:!0}],PERPLEXITY:[{envVarName:`PERPLEXITY_API_KEY`,isRequired:!0}],TOGETHER:[{envVarName:`TOGETHER_API_KEY`,isRequired:!0}],AWS:[{envVarName:`AWS_ACCESS_KEY_ID`,isRequired:!0},{envVarName:`AWS_SECRET_ACCESS_KEY`,isRequired:!0},{envVarName:`AWS_SESSION_TOKEN`,isRequired:!1}]},Li=`api_key`,Ri=`default_credentials`,zi={OPENAI:`OPENAI`,AZURE_OPENAI:`AZURE_OPENAI`,ANTHROPIC:`ANTHROPIC`,AWS_BEDROCK:`AWS`,GOOGLE_GENAI:`GOOGLE`},Bi={openai:`OPENAI`,azure:`AZURE_OPENAI`,anthropic:`ANTHROPIC`,aws:`AWS`,google:`GOOGLE`,xai:`XAI`,ollama:`OLLAMA`,deepseek:`DEEPSEEK`,cerebras:`CEREBRAS`,fireworks:`FIREWORKS`,groq:`GROQ`,moonshot:`MOONSHOT`,perplexity:`PERPLEXITY`,together:`TOGETHER`},Vi=Object.entries({OPENAI:`OpenAI`,AZURE_OPENAI:`Azure OpenAI`,ANTHROPIC:`Anthropic`,AWS_BEDROCK:`AWS Bedrock`,GOOGLE_GENAI:`Google GenAI`}).map(([e,t])=>({id:e,label:t})),Hi={OPENAI:`openai`,AZURE_OPENAI:`azure`,ANTHROPIC:`anthropic`,AWS_BEDROCK:`aws`,GOOGLE_GENAI:`google`},Ui=Object.entries({api_key:`API Key`,ad_token_provider:`Azure AD Token Provider`,default_credentials:`Default Credentials (Managed Identity)`}).map(([e,t])=>({id:e,label:t})),Wi=Object.entries({default_credentials:`Default Credentials (IAM Role)`,access_keys:`Access Keys`}).map(([e,t])=>({id:e,label:t}));function Gi(e){let t=(0,Y.c)(4),n;t[0]===Symbol.for(`react.memo_cache_sentinel`)?(n=U`
        display: inline-block;
        max-width: 100%;
        min-width: 0;
        color: var(--global-link-color);
      `,t[0]=n):n=t[0];let r;t[1]===Symbol.for(`react.memo_cache_sentinel`)?(r=U`
          display: inline-block;
          max-width: 100%;
          min-width: 0;
          border-radius: var(--global-rounding-small);
          color: var(--global-link-color);
          &:not(:hover) {
            text-decoration: none;
          }
          &:focus-visible {
            outline: var(--focus-ring-thickness) solid var(--focus-ring-color);
            outline-offset: var(--focus-ring-offset);
          }
        `,t[1]=r):r=t[1];let i;return t[2]===e?i=t[3]:(i=B(`div`,{className:`link-container`,onClick:Ki,css:n,children:B(Jn,{css:r,...e})}),t[2]=e,t[3]=i),i}function Ki(e){return e.stopPropagation()}function qi(e){let t=(0,Y.c)(5),{href:n,children:r}=e,i;t[0]===Symbol.for(`react.memo_cache_sentinel`)?(i=U`
        color: var(--global-link-color);
        text-decoration: none;
        display: inline-flex;
        align-items: center;
        &:hover {
          text-decoration: underline;
        }
        .icon-wrap {
          display: inline-block;
          margin-left: 0.1em;
          font-size: 1em;
        }
      `,t[0]=i):i=t[0];let a;t[1]===Symbol.for(`react.memo_cache_sentinel`)?(a=B(z,{svg:B(gt,{})}),t[1]=a):a=t[1];let o;return t[2]!==r||t[3]!==n?(o=V(`a`,{href:n,target:`_blank`,css:i,rel:`noreferrer`,children:[r,a]}),t[2]=r,t[3]=n,t[4]=o):o=t[4],o}var Ji=Wt`
  100% {
    transform: rotate(360deg);
  }
`,Yi=Wt`
  0% {
    stroke-dasharray: calc(var(--progress-circle-circumference) * 0.25), var(--progress-circle-circumference);
    stroke-dashoffset: 0;
  }
  80% {
    stroke-dasharray: calc(var(--progress-circle-circumference) * 0.75), var(--progress-circle-circumference);
    stroke-dashoffset: calc(-1 * var(--progress-circle-circumference));
  }
  100% {
    stroke-dasharray: calc(var(--progress-circle-circumference) * 0.25), var(--progress-circle-circumference);
    stroke-dashoffset: calc(-1.25 * var(--progress-circle-circumference));
  }
`,Xi=U`
  &[data-size="S"] {
    --progress-circle-size: 18px;
    --progress-circle-stroke-width: 2px;
  }
  &[data-size="M"] {
    --progress-circle-size: 32px;
    --progress-circle-stroke-width: 3px;
  }

  --progress-circle-center: calc(var(--progress-circle-size) / 2);
  --progress-circle-radius: calc(
    var(--progress-circle-center) - var(--progress-circle-stroke-width)
  );
  --progress-circle-circumference: calc(
    2 * 3.141592653589793 * var(--progress-circle-radius)
  );

  // Progress calculations for determinate mode
  --progress-circle-value: 0;
  --progress-circle-dasharray: var(--progress-circle-circumference)
    var(--progress-circle-circumference);
  --progress-circle-dashoffset: calc(
    var(--progress-circle-circumference) -
      (var(--progress-circle-value) / 100 * var(--progress-circle-circumference))
  );

  .progress-circle__svg {
    width: var(--progress-circle-size);
    height: var(--progress-circle-size);
    fill: none;
    display: block;
  }

  .progress-circle__background {
    cx: var(--progress-circle-center);
    cy: var(--progress-circle-center);
    r: var(--progress-circle-radius);
    stroke: var(--global-color-gray-300);
    stroke-width: var(--progress-circle-stroke-width);
  }

  .progress-circle__arc {
    cx: var(--progress-circle-center);
    cy: var(--progress-circle-center);
    r: var(--progress-circle-radius);
    stroke: var(--global-color-primary);
    stroke-width: var(--progress-circle-stroke-width);
    transition: stroke-dashoffset 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    stroke-dasharray: var(--progress-circle-dasharray);
    stroke-dashoffset: var(--progress-circle-dashoffset);
  }

  &[data-indeterminate] {
    .progress-circle__svg {
      animation: ${Ji} 3s linear infinite;
    }
    .progress-circle__arc {
      animation: ${Yi} 3s cubic-bezier(0.4, 0, 0.2, 1) infinite;
      stroke-dasharray:
        calc(var(--progress-circle-circumference) * 0.25),
        var(--progress-circle-circumference);
      stroke-dashoffset: 0;
    }
  }
`,Zi=U`
  inline-size: var(--global-dimension-size-2400);
  height: var(--global-dimension-size-75);

  .progress-bar__track {
    forced-color-adjust: none;
    height: 100%;
    border-radius: 3px;
    overflow: hidden;
    background-color: var(
      --mod-barloader-track-color,
      var(--global-color-gray-300)
    );
  }

  .progress-bar__fill {
    background: var(--mod-barloader-fill-color, var(--global-color-primary));
    height: 100%;
  }
`;function Qi({ref:e,...t}){let{isIndeterminate:n=!1,value:r,size:i=`M`}=t;return B(en,{...t,"data-size":i,"data-indeterminate":n||void 0,css:Xi,ref:e,style:!n&&r!=null?{"--progress-circle-value":r}:void 0,children:V(`svg`,{className:`progress-circle__svg`,children:[B(`circle`,{className:`progress-circle__background`}),B(`circle`,{className:`progress-circle__arc`})]})})}function $i(e){let t=(0,Y.c)(12),n,r,i,a;t[0]===e?(n=t[1],r=t[2],i=t[3],a=t[4]):({ref:i,width:a,height:n,...r}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a);let o;t[5]!==n||t[6]!==a?(o={width:a,height:n},t[5]=n,t[6]=a,t[7]=o):o=t[7];let s;return t[8]!==r||t[9]!==i||t[10]!==o?(s=B(en,{...r,ref:i,css:Zi,style:o,children:ea}),t[8]=r,t[9]=i,t[10]=o,t[11]=s):s=t[11],s}function ea(e){let{percentage:t}=e;return B(`div`,{className:`progress-bar__track`,children:B(`div`,{className:`progress-bar__fill`,style:{width:t+`%`}})})}function ta({ref:e,...t}){let{children:n,elementType:r=`div`,...i}=t,{styleProps:a}=bn(t,vn);return B(r,{...gn(i),...a,ref:e,css:U`
        overflow: hidden;
        box-sizing: border-box;
      `,className:`view`,children:n})}var na=U`
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
  border-radius: var(--global-rounding-small);
  background: var(--global-tooltip-background-color);
  border: var(--global-border-size-thin) solid
    var(--global-tooltip-border-color);
  color: var(--global-text-color-900);
  forced-color-adjust: none;
  outline: none;
  padding: var(--global-dimension-size-100) var(--global-dimension-size-200);
  max-width: 200px;
  font-size: var(--global-font-size-s);
  /* fixes FF gap */
  transform: translate3d(0, 0, 0);
  transition:
    transform 200ms,
    opacity 200ms;

  &[data-entering],
  &[data-exiting] {
    transform: var(--tooltip-origin);
    opacity: 0;
  }

  &[data-placement="top"] {
    margin-bottom: var(--global-dimension-size-100);
    --tooltip-origin: translateY(4px);
  }

  &[data-placement="bottom"] {
    margin-top: var(--global-dimension-size-100);
    --tooltip-origin: translateY(-4px);

    & .react-aria-OverlayArrow svg {
      transform: rotate(180deg);
    }
  }

  &[data-placement="right"] {
    margin-left: var(--global-dimension-size-100);
    --tooltip-origin: translateX(-4px);

    & .react-aria-OverlayArrow svg {
      transform: rotate(90deg);
    }
  }

  &[data-placement="left"] {
    margin-right: var(--global-dimension-size-100);
    --tooltip-origin: translateX(4px);

    & .react-aria-OverlayArrow svg {
      transform: rotate(-90deg);
    }
  }

  & .react-aria-OverlayArrow svg {
    display: block;
    fill: var(--global-tooltip-background-color);
    stroke: var(--global-tooltip-border-color);
    stroke-width: 1px;
  }
`,ra=U`
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
  border-radius: var(--global-rounding-medium);
  background: var(--global-tooltip-background-color);
  border: var(--global-border-size-thin) solid
    var(--global-tooltip-border-color);
  color: var(--global-text-color-900);
  forced-color-adjust: none;
  outline: none;
  padding: var(--global-dimension-size-200);
  min-width: 200px;
  font-size: var(--global-font-size-s);
  /* fixes FF gap */
  transform: translate3d(0, 0, 0);
  transition:
    transform 200ms,
    opacity 200ms;

  &[data-entering],
  &[data-exiting] {
    transform: var(--tooltip-origin);
    opacity: 0;
  }

  &[data-placement="top"] {
    margin-bottom: var(--global-dimension-size-100);
    --tooltip-origin: translateY(4px);
  }

  &[data-placement="bottom"] {
    margin-top: var(--global-dimension-size-100);
    --tooltip-origin: translateY(-4px);

    & .react-aria-OverlayArrow svg {
      transform: rotate(180deg);
    }
  }

  &[data-placement="right"] {
    margin-left: var(--global-dimension-size-100);
    --tooltip-origin: translateX(-4px);

    & .react-aria-OverlayArrow svg {
      transform: rotate(90deg);
    }
  }

  &[data-placement="left"] {
    margin-right: var(--global-dimension-size-100);
    --tooltip-origin: translateX(4px);

    & .react-aria-OverlayArrow svg {
      transform: rotate(-90deg);
    }
  }

  & .react-aria-OverlayArrow svg {
    display: block;
    fill: var(--global-tooltip-background-color);
    stroke: var(--global-tooltip-border-color);
    stroke-width: 1px;
  }
`;function ia(e){let t=(0,Y.c)(10),n,r,i,a;if(t[0]!==e){let{ref:o,...s}=e,{css:c,...l}=s;n=A,r=l,i=o,a=U(na,c),t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a}else n=t[1],r=t[2],i=t[3],a=t[4];let o;return t[5]!==n||t[6]!==r||t[7]!==i||t[8]!==a?(o=B(n,{...r,ref:i,css:a}),t[5]=n,t[6]=r,t[7]=i,t[8]=a,t[9]=o):o=t[9],o}function aa(e){let t=(0,Y.c)(8),n,r;t[0]===e?(n=t[1],r=t[2]):({ref:r,...n}=e,t[0]=e,t[1]=n,t[2]=r);let{css:i}=n,a;t[3]===Symbol.for(`react.memo_cache_sentinel`)?(a=F(`react-aria-OverlayArrow`),t[3]=a):a=t[3];let o;t[4]===Symbol.for(`react.memo_cache_sentinel`)?(o=B(`svg`,{width:8,height:8,viewBox:`0 0 8 8`,children:B(`path`,{d:`M0 0 L4 4 L8 0`})}),t[4]=o):o=t[4];let s;return t[5]!==i||t[6]!==r?(s=B(fn,{ref:r,css:i,className:a,children:o}),t[5]=i,t[6]=r,t[7]=s):s=t[7],s}var oa=1e3,sa=60*oa,ca=60*sa,la=24*ca;7*la;var ua=30*la,da=31536e3,fa=2592e3,pa=604800,ma=86400,ha=3600,ga=`https://arize.com/docs/phoenix`,X={accessControl:`${ga}/settings/access-control-rbac`,annotationConfigs:`${ga}/tracing/how-to-tracing/feedback-and-annotations/annotating-in-the-ui`,apiKeys:`${ga}/settings/api-keys`,customAiProviders:`${ga}/settings/custom-ai-providers`,dataRetention:`${ga}/settings/data-retention`,datasetLabels:`${ga}/release-notes/10-2025/10-08-2025-dataset-labels`,modelCostTracking:`${ga}/tracing/how-to-tracing/cost-tracking`,remoteMcpServer:`${ga}/integrations/remote-mcp`,promptLabels:`${ga}/release-notes/09-2025/09-15-2025-prompt-labels`,providers:`${ga}/prompt-engineering/how-to-prompts/configure-ai-providers`,pxi:`${ga}/pxi`,sandboxes:`${ga}/settings/sandboxes`,secrets:`${ga}/settings/secrets`},_a={aiProviderSettings:{href:X.providers,label:`AI provider settings`},aiProviders:{href:X.providers,label:`AI providers`},annotationConfigs:{href:X.annotationConfigs,label:`annotation configs`},apiKeys:{href:X.apiKeys,label:`API keys`},customAiProviders:{href:X.customAiProviders,label:`custom AI providers`},dataRetention:{href:X.dataRetention,label:`data retention`},datasetLabels:{href:X.datasetLabels,label:`dataset labels`},defaultRetentionPolicy:{href:X.dataRetention,label:`the default retention policy`},modelPricing:{href:X.modelCostTracking,label:`model pricing`},promptLabels:{href:X.promptLabels,label:`prompt labels`},pxi:{href:X.pxi,label:`PXI`},sandboxConfigurations:{href:X.sandboxes,label:`sandbox configurations`},sandboxProviders:{href:X.sandboxes,label:`sandbox providers`},secrets:{href:X.secrets,label:`secrets`},userAccess:{href:X.accessControl,label:`user access`}},va=e=>{switch(e){case`info`:return B(Un,{});default:return B(Tt,{})}},ya=U`
  & {
    all: unset;
    height: 14px !important;
    width: 14px !important;
    // Opt out of the shared square icon-button min-width so this stays a
    // compact 14px affordance rather than a full-height button
    min-width: 14px !important;
    min-height: 14px !important;
    padding: var(--global-dimension-size-50) !important;
    border-radius: var(--global-rounding-small);
    cursor: pointer;
    svg {
      height: 14px;
      width: 14px;
    }
  }
`,ba=({children:e,href:t,triggerAriaLabel:n=`More information`,variant:r=`help`,...i})=>{let a={"aria-label":n,css:ya,leadingVisual:B(z,{svg:va(r)}),size:`S`,variant:`quiet`};return V(Se,{delay:0,children:[t?B(Oe,{children:B(Dt,{...a,href:t})}):B(H,{...a}),B(ia,{...i,children:e})]})},xa=U`
  margin-top: var(--global-dimension-size-100);
`;function Sa(e){let t=(0,Y.c)(9),{children:n,topic:r}=e,{href:i,label:a}=_a[r],o=`Learn more about ${a}`,s;t[0]===n?s=t[1]:(s=B(L,{size:`S`,children:n}),t[0]=n,t[1]=s);let c;t[2]===i?c=t[3]:(c=B(`footer`,{css:xa,children:B(qi,{href:i,children:`View documentation`})}),t[2]=i,t[3]=c);let l;return t[4]!==i||t[5]!==o||t[6]!==s||t[7]!==c?(l=V(ba,{href:i,variant:`info`,triggerAriaLabel:o,children:[s,c]}),t[4]=i,t[5]=o,t[6]=s,t[7]=c,t[8]=l):l=t[8],l}function Ca(e){let t=(0,Y.c)(8),n,r;t[0]===e?(n=t[1],r=t[2]):({children:n,...r}=e,t[0]=e,t[1]=n,t[2]=r);let i;t[3]===n?i=t[4]:(i=B(`div`,{role:`button`,children:n}),t[3]=n,t[4]=i);let a;return t[5]!==r||t[6]!==i?(a=B(Oe,{...r,children:i}),t[5]=r,t[6]=i,t[7]=a):a=t[7],a}function wa(e){let t=(0,Y.c)(16),n,r,i,a,o,s;if(t[0]!==e){let{ref:c,...l}=e,{children:u,css:d,width:f,...p}=l;r=u,s=f,n=A,i=p,a=c,o=U(ra,d),t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a,t[5]=o,t[6]=s}else n=t[1],r=t[2],i=t[3],a=t[4],o=t[5],s=t[6];let c;t[7]===s?c=t[8]:(c=s?{width:s}:{maxWidth:`300px`},t[7]=s,t[8]=c);let l;return t[9]!==n||t[10]!==r||t[11]!==i||t[12]!==a||t[13]!==o||t[14]!==c?(l=B(n,{...i,ref:a,css:o,style:c,children:r}),t[9]=n,t[10]=r,t[11]=i,t[12]=a,t[13]=o,t[14]=c,t[15]=l):l=t[15],l}function Ta(e){let t=(0,Y.c)(3),{children:n}=e,r;t[0]===Symbol.for(`react.memo_cache_sentinel`)?(r=U`
        margin-bottom: var(--global-dimension-size-100);
      `,t[0]=r):r=t[0];let i;return t[1]===n?i=t[2]:(i=B(ot,{level:4,css:r,children:n}),t[1]=n,t[2]=i),i}function Ea(e){let t=(0,Y.c)(3),{children:n}=e,r;t[0]===Symbol.for(`react.memo_cache_sentinel`)?(r=U`
        margin-bottom: var(--global-dimension-size-100);
      `,t[0]=r):r=t[0];let i;return t[1]===n?i=t[2]:(i=B(L,{size:`S`,color:`text-700`,css:r,children:n}),t[1]=n,t[2]=i),i}function Da(e){let t=(0,Y.c)(2),{children:n}=e,r;return t[0]===n?r=t[1]:(r=B(ta,{paddingTop:`size-50`,children:n}),t[0]=n,t[1]=r),r}var Oa=2e3,ka=U`
  flex: none;
  box-sizing: content-box;
`;function Aa(e){let{text:t,size:n=`S`,tooltipText:r=`Copy`,...i}=e,[a,o]=(0,J.useState)(!1),s=(0,J.useCallback)(()=>{let e=typeof t==`string`?t:t.current||``;ze(e),o(!0),setTimeout(()=>{o(!1)},Oa)},[t]);return B(`div`,{className:`copy-to-clipboard-button`,css:ka,children:V(Se,{children:[B(H,{size:n,leadingVisual:B(z,{color:a?`success`:`inherit`,svgKey:a?`Checkmark`:`Duplicate`}),onPress:s,...i,className:`copy-button`}),B(ia,{offset:1,children:r})]})})}var ja=U`
  --menu-min-width: 250px;
  min-width: var(--menu-min-width);
  display: flex;
  flex-direction: column;
  gap: var(--global-menu-item-gap);
  flex: 1 1 auto;
  overflow-y: auto;
  overflow-x: hidden;
  padding: var(--global-menu-item-gap);
  /* The menu container itself takes focus when opened before focus moves to an
     item. Suppress the container-level focus ring — keyboard focus is already
     indicated on the focused item — so the whole menu doesn't get outlined. */
  &:focus-visible {
    outline: none;
  }
  &[data-empty] {
    align-items: center;
    justify-content: center;
    display: flex;
    padding: var(--global-dimension-size-100);
  }

  .react-aria-MenuSection {
    display: flex;
    flex-direction: column;
    gap: var(--global-menu-item-gap);
  }
`,Ma=vt,Na=e=>{let t=(0,Y.c)(10),n,r,i;t[0]===e?(n=t[1],r=t[2],i=t[3]):({className:n,onKeyDown:r,...i}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i);let a;t[4]===n?a=t[5]:(a=F(`react-aria-Menu`,n),t[4]=n,t[5]=a);let o;return t[6]!==r||t[7]!==i||t[8]!==a?(o=B(on,{className:a,css:ja,...i,onKeyDown:r}),t[6]=r,t[7]=i,t[8]=a,t[9]=o):o=t[9],o},Pa=U`
  padding: var(--global-dimension-size-50);
  border-radius: var(--global-rounding-small);
  outline: none;
  cursor: default;
  color: var(--global-text-color-900);
  text-decoration: none;
  position: relative;
  display: flex;

  align-items: center;
  justify-content: space-between;

  &[data-open],
  &[data-focused],
  &[data-hovered] {
    background-color: var(--global-menu-item-background-color-hover);
  }

  &[data-disabled] {
    cursor: not-allowed;
    color: var(--global-color-text-300);
    opacity: var(--global-opacity-disabled);
  }

  &[data-focus-visible] {
    outline: none;
  }

  @media (forced-colors: active) {
    &[data-focused] {
      forced-color-adjust: none;
      background: Highlight;
      color: HighlightText;
    }
  }
`,Fa=e=>{let t=(0,Y.c)(18),n,r,i,a,o;t[0]===e?(n=t[1],r=t[2],i=t[3],a=t[4],o=t[5]):({className:n,trailingContent:o,leadingContent:r,ref:a,...i}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a,t[5]=o);let s=i.textValue||(typeof i.children==`string`?i.children:void 0),c;t[6]===n?c=t[7]:(c=F(`react-aria-MenuItem`,n),t[6]=n,t[7]=c);let l;t[8]!==r||t[9]!==i||t[10]!==o?(l=e=>{let{hasSubmenu:t,isSelected:n,selectionMode:a}=e;return V(R,{children:[n&&B(z,{svg:B(yn,{})}),a!==`none`&&!n&&B(z,{svg:B(yn,{}),css:U`
                  visibility: hidden;
                `}),B(Ia,{trailingContent:o,leadingContent:r,children:typeof i.children==`function`?i.children(e):i.children}),t&&B(z,{svg:B(er,{})})]})},t[8]=r,t[9]=i,t[10]=o,t[11]=l):l=t[11];let u;return t[12]!==i||t[13]!==a||t[14]!==c||t[15]!==l||t[16]!==s?(u=B(an,{ref:a,...i,css:Pa,className:c,textValue:s,children:l}),t[12]=i,t[13]=a,t[14]=c,t[15]=l,t[16]=s,t[17]=u):u=t[17],u},Ia=e=>{let t=(0,Y.c)(7),{children:n,trailingContent:r,leadingContent:i}=e,a;t[0]===Symbol.for(`react.memo_cache_sentinel`)?(a=U`
        padding: var(--global-menu-item-gap);
      `,t[0]=a):a=t[0];let o;t[1]!==n||t[2]!==i?(o=i?V(W,{alignItems:`center`,gap:`var(--global-menu-item-content-gap)`,children:[i,` `,n]}):n,t[1]=n,t[2]=i,t[3]=o):o=t[3];let s;return t[4]!==o||t[5]!==r?(s=V(W,{direction:`row`,alignItems:`center`,justifyContent:`space-between`,gap:`var(--global-menu-split-item-content-gap)`,minWidth:0,flex:1,css:a,children:[o,r]}),t[4]=o,t[5]=r,t[6]=s):s=t[6],s},La=U`
  overflow-y: hidden;
  display: flex;
  flex-direction: column;
`,Ra=({children:e,placement:t=`bottom end`,minHeight:n=`var(--global-menu-min-height)`,maxHeight:r=`var(--global-menu-max-height-large)`,maxWidth:i=450,...a})=>B(tr,{shouldFlip:!1,placement:t,css:La,...a,children:B(`div`,{style:{minHeight:n,maxHeight:r,maxWidth:i},css:U`
          display: flex;
          flex-direction: column;
          height: 100%;
          min-width: 300px;
        `,children:e})}),za=U`
  padding: var(--global-dimension-size-50) var(--global-dimension-size-100) 0;
`,Ba=e=>{let t=(0,Y.c)(5),{title:n,trailingContent:r}=e,i;t[0]===n?i=t[1]:(i=B(L,{weight:`heavy`,children:n}),t[0]=n,t[1]=i);let a;return t[2]!==i||t[3]!==r?(a=B(Ot,{css:za,children:V(W,{justifyContent:`space-between`,alignItems:`center`,children:[i,r]})}),t[2]=i,t[3]=r,t[4]=a):a=t[4],a},Va=e=>{let t=(0,Y.c)(3),{children:n}=e,r;t[0]===Symbol.for(`react.memo_cache_sentinel`)?(r=U`
        display: flex;
        flex-direction: column;
        flex-shrink: 0;

        /* Draw the divider under (and, when stacked, between) quiet
           SearchFields in the header by re-coloring the field's own border.
           Scope with the block class (&.menu-header ...) so this wins over the
           quiet variant's border resets in EVERY interaction state — rest,
           hover, and focus. Without the extra specificity the variant's
           :focused reset ties on specificity and wins on source order, so a
           focused (e.g. autoFocused) search field silently loses its divider.
           Invalid fields keep their danger border. */
        &.menu-header
          .search-field[data-variant="quiet"]
          .react-aria-Input:not([data-invalid]) {
          border-bottom-color: var(--global-menu-border-color);
        }
        &.menu-header
          *
          + .search-field[data-variant="quiet"]
          .react-aria-Input:not([data-invalid]) {
          border-top-color: var(--global-menu-border-color);
        }
      `,t[0]=r):r=t[0];let i;return t[1]===n?i=t[2]:(i=B(`div`,{className:`menu-header`,css:r,children:n}),t[1]=n,t[2]=i),i},Ha=e=>{let t=(0,Y.c)(8),{children:n,leadingContent:r,trailingContent:i}=e,a;t[0]===Symbol.for(`react.memo_cache_sentinel`)?(a=U`
        padding: var(--global-dimension-size-100);
        border-bottom: 1px solid var(--global-menu-border-color);
      `,t[0]=a):a=t[0];let o;t[1]===Symbol.for(`react.memo_cache_sentinel`)?(o=U`
          flex: 1 1 auto;
          width: 100%;
          padding-left: var(--global-dimension-size-50);
        `,t[1]=o):o=t[1];let s;t[2]===n?s=t[3]:(s=B(ot,{level:4,weight:`heavy`,css:o,children:n}),t[2]=n,t[3]=s);let c;return t[4]!==r||t[5]!==s||t[6]!==i?(c=V(W,{direction:`row`,gap:`size-50`,alignItems:`center`,wrap:`nowrap`,minHeight:30,"data-testid":`menu-header-title`,css:a,children:[r,s,i]}),t[4]=r,t[5]=s,t[6]=i,t[7]=c):c=t[7],c},Ua=e=>{let t=(0,Y.c)(3),{children:n}=e,r;t[0]===Symbol.for(`react.memo_cache_sentinel`)?(r=U`
        padding: var(--global-dimension-size-100);
        border-top: 1px solid var(--global-menu-border-color);
        display: flex;
        flex-direction: column;
        flex-shrink: 0;
        gap: var(--global-dimension-size-50);
      `,t[0]=r):r=t[0];let i;return t[1]===n?i=t[2]:(i=B(`div`,{css:r,children:n}),t[1]=n,t[2]=i),i},Wa=e=>{let t=(0,Y.c)(3),{children:n}=e,r;t[0]===Symbol.for(`react.memo_cache_sentinel`)?(r=U`
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
      `,t[0]=r):r=t[0];let i;return t[1]===n?i=t[2]:(i=B(L,{color:`gray-400`,fontStyle:`italic`,css:r,children:n}),t[1]=n,t[2]=i),i},Ga=U`
  justify-content: flex-start;
  min-width: 0;

  &:not([data-disabled="true"]) {
    &[data-pressed],
    &:hover {
      --button-border-color: var(--global-input-field-border-color-active);
    }
  }

  .menu-button__value {
    flex: 1 1 auto;
    min-width: 0;
    overflow: hidden;
    text-align: start;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  .menu-button__value--placeholder {
    color: var(--text-color-placeholder);
    font-style: italic;
  }

  & > .icon-wrap:last-child {
    flex: none;
    margin-left: auto;
  }
`;function Ka(e){let t=(0,Y.c)(10),n,r,i;t[0]===e?(n=t[1],r=t[2],i=t[3]):({ref:i,css:n,...r}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i);let a;t[4]===n?a=t[5]:(a=U(Ga,n),t[4]=n,t[5]=a);let o;return t[6]!==r||t[7]!==i||t[8]!==a?(o=B(H,{ref:i,css:a,...r}),t[6]=r,t[7]=i,t[8]=a,t[9]=o):o=t[9],o}function qa(e){let t=(0,Y.c)(5),{children:n,isPlaceholder:r}=e,i=r&&`menu-button__value--placeholder`,a;t[0]===i?a=t[1]:(a=F(`menu-button__value`,i),t[0]=i,t[1]=a);let o;return t[2]!==n||t[3]!==a?(o=B(`span`,{className:a,children:n}),t[2]=n,t[3]=a,t[4]=o):o=t[4],o}var Ja=2e3;function Ya(e){let t=(0,Y.c)(18),{items:n}=e,[r,i]=(0,J.useState)(null),a=(0,J.useRef)(null),o;t[0]===n?o=t[1]:(o=e=>{let t=n.find(t=>t.name===e);t&&(ze(t.value),i(t.name),a.current&&clearTimeout(a.current),a.current=setTimeout(()=>{i(null)},Ja))},t[0]=n,t[1]=o);let s=o,c=r==null?`Duplicate`:`Checkmark`,l=r==null?`inherit`:`success`,u;t[2]!==c||t[3]!==l?(u=B(z,{svgKey:c,color:l}),t[2]=c,t[3]=l,t[4]=u):u=t[4];let d=r!=null||void 0,f=r==null?void 0:`Copied`,p;t[5]!==u||t[6]!==d||t[7]!==f?(p=B(H,{size:`S`,variant:`quiet`,"aria-label":`Copy`,leadingVisual:u,className:`copy-action-menu__button`,"data-copied":d,children:f}),t[5]=u,t[6]=d,t[7]=f,t[8]=p):p=t[8];let m;t[9]===Symbol.for(`react.memo_cache_sentinel`)?(m=U`
            --menu-min-width: auto;
          `,t[9]=m):m=t[9];let h;t[10]===n?h=t[11]:(h=n.map(Xa),t[10]=n,t[11]=h);let g;t[12]!==s||t[13]!==h?(g=B(tr,{placement:`bottom end`,offset:3,children:B(Na,{onAction:s,css:m,children:h})}),t[12]=s,t[13]=h,t[14]=g):g=t[14];let _;return t[15]!==p||t[16]!==g?(_=V(Ma,{children:[p,g]}),t[15]=p,t[16]=g,t[17]=_):_=t[17],_}function Xa(e){return B(Fa,{id:e.name,textValue:`Copy ${e.name}`,leadingContent:B(z,{svgKey:e.iconKey??`Duplicate`}),children:e.name},e.name)}var Za=U`
  --embedded-copy-button-size: calc(
    var(--global-input-height-m) - 2 * var(--global-dimension-size-125) +
      var(--global-dimension-size-50)
  );
`,Qa=U`
  ${Za}
  // The element selector keeps this ahead of the button's own size rule, which
  // is otherwise of equal specificity and would win or lose on style insertion
  // order alone
  .copy-to-clipboard-button button.copy-button {
    width: var(--embedded-copy-button-size);
    height: var(--embedded-copy-button-size);
    min-width: 0;
    padding: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: var(--field-copy-button-background-color);
    border: none;
    border-radius: var(--global-rounding-small);
    color: var(--field-copy-button-text-color);
    transition: background-color 0.2s;
    &:hover {
      background-color: var(--field-copy-button-background-color-hover);
    }
  }
`,$a=({children:e,bordered:t=!0})=>B(`div`,{"data-bordered":t,css:U`
        border-bottom: 1px solid var(--global-border-color-default);
        &[data-bordered="true"] {
          border-top: 1px solid var(--global-border-color-default);
        }
        & > * {
          display: flex;
          justify-content: space-between;
          align-items: center;
          padding: var(--global-dimension-size-100)
            var(--global-dimension-size-200);
        }
      `,children:B(ot,{children:e})}),eo=[/Unexpected token ['"]?<['"]?/i,/JSON\.parse.*unexpected character/i,/<!DOCTYPE/i,/timeout/i,/502|504|gateway/i];function to(e){if(e==null)return!1;let t=e instanceof Error?e.message:e;return typeof t!=`string`||t.length===0?!1:eo.some(e=>e.test(t))}function no(e){let t=(0,Y.c)(9),{error:n}=e;if(to(n)){let e;return t[0]===n?e=t[1]:(e=B(ro,{error:n}),t[0]=n,t[1]=e),e}let r,i;t[2]===Symbol.for(`react.memo_cache_sentinel`)?(r=B(W,{direction:`column`,width:`100%`,alignItems:`center`,children:B(`h1`,{children:`Something went wrong`})}),i=B(`p`,{children:`We strive to do our very best but 🐛 bugs happen. It would mean a lot to us if you could file a an issue. If you feel comfortable, please include the error details below in your issue. We will get back to you as soon as we can.`}),t[2]=r,t[3]=i):(r=t[2],i=t[3]);let a;t[4]===Symbol.for(`react.memo_cache_sentinel`)?(a=B(W,{direction:`row`,width:`100%`,justifyContent:`end`,children:B(qi,{href:`https://github.com/Arize-ai/phoenix/issues/new?assignees=&labels=bug&template=bug_report.md&title=%5BBUG%5D`,children:`file an issue with us`})}),t[4]=a):a=t[4];let o,s;t[5]===Symbol.for(`react.memo_cache_sentinel`)?(o=B(`summary`,{children:`error details`}),s=U`
              white-space: pre-wrap;
              overflow-wrap: break-word;
              overflow: hidden;
              overflow-y: auto;
              max-height: 500px;
            `,t[5]=o,t[6]=s):(o=t[5],s=t[6]);let c;return t[7]===n?c=t[8]:(c=B(ta,{padding:`size-200`,children:V(W,{direction:`column`,children:[r,i,a,V(`details`,{open:!0,children:[o,B(`pre`,{css:s,children:n})]})]})}),t[7]=n,t[8]=c),c}function ro(e){let t=(0,Y.c)(9),{error:n}=e,r,i,a,o;t[0]===Symbol.for(`react.memo_cache_sentinel`)?(r=B(W,{direction:`column`,width:`100%`,alignItems:`center`,children:B(`h1`,{children:`Connection timed out`})}),i=B(`p`,{children:`The connection to the Phoenix server timed out before a response was received. This typically happens when a load balancer or proxy closes the connection before the server can respond.`}),a=B(`p`,{children:`Possible solutions:`}),o=V(`ul`,{css:U`
            margin: var(--global-dimension-size-100) 0;
            padding-left: var(--global-dimension-size-300);
          `,children:[B(`li`,{children:`Increase your load balancer or proxy timeout settings`}),B(`li`,{children:`Check if the Phoenix server is overloaded or slow to respond`}),B(`li`,{children:`Verify network connectivity between components`})]}),t[0]=r,t[1]=i,t[2]=a,t[3]=o):(r=t[0],i=t[1],a=t[2],o=t[3]);let s;t[4]===Symbol.for(`react.memo_cache_sentinel`)?(s=B(W,{direction:`row`,width:`100%`,justifyContent:`end`,children:B(H,{variant:`primary`,size:`S`,onPress:io,children:`Retry`})}),t[4]=s):s=t[4];let c;t[5]===n?c=t[6]:(c=n&&V(`details`,{children:[B(`summary`,{children:`error details`}),B(`pre`,{css:U`
                white-space: pre-wrap;
                overflow-wrap: break-word;
                overflow: hidden;
                overflow-y: auto;
                max-height: 500px;
              `,children:n})]}),t[5]=n,t[6]=c);let l;return t[7]===c?l=t[8]:(l=B(ta,{padding:`size-200`,children:V(W,{direction:`column`,children:[r,i,a,o,s,c]})}),t[7]=c,t[8]=l),l}function io(){window.location.reload()}var ao=class extends J.Component{constructor(e){super(e),this.state={hasError:!1,error:null}}static getDerivedStateFromError(e){return{hasError:!0,error:e}}componentDidCatch(e,t){console.error(`ErrorBoundary caught error:`,e,t)}render(){if(this.state.hasError){let e=this.state.error instanceof Error?this.state.error.message:null;return typeof this.props.fallback==`function`?B(this.props.fallback,{error:e}):B(no,{error:e})}return this.props.children}};function oo({error:e}){let t=V(`div`,{css:U`
        text-align: center;
        display: inline-flex;
        align-items: center;
        color: var(--global-text-color-300);
        gap: var(--global-dimension-size-50);
        cursor: ${e?`help`:`default`};
      `,children:[B(z,{svg:B(bt,{})}),B(L,{color:`text-300`,children:`error`})]});return e?V(Se,{delay:200,children:[B(`span`,{tabIndex:0,children:t}),B(A,{offset:6,children:B(ta,{padding:`size-100`,borderColor:`default`,borderWidth:`thin`,borderRadius:`small`,backgroundColor:`gray-200`,maxWidth:`size-4600`,children:B(`pre`,{css:U`
              white-space: pre-wrap;
              overflow-wrap: break-word;
              margin: 0;
              font-size: var(--global-font-size-xs, 12px);
            `,children:e})})})]}):t}var so=U`
  background-color: var(--global-color-primary-100);
  color: var(--global-color-primary-700);
  padding: var(--global-dimension-size-50) var(--global-dimension-size-100);
  font-size: var(--global-dimension-font-size-50);
  border-radius: var(--global-dimension-size-100);
  border: 1px solid var(--global-color-primary-200);
  box-shadow: 0 2px 0 0 var(--global-color-primary-200);
  // Offset the shadow to make it look like it's on the key
  margin-top: -1px;
  text-transform: uppercase;
`,co=U`
  background-color: transparent;
  color: var(--ac-global-text-color-500);
  padding: 0 var(--global-dimension-size-75);
  font-size: var(--global-dimension-font-size-50);
  border-radius: var(--global-rounding-small);
  border: 1px solid var(--ac-global-border-color-default);
  text-transform: uppercase;
`;function lo({ref:e,children:t,variant:n=`default`,...r}){return B(Vt,{ref:e,css:n===`quiet`?co:so,...r,children:t})}function uo({ref:e,color:t,size:n=`M`,shape:r=`square`}){let i=typeof t==`string`&&t.startsWith(`var`),a=i?U`
        background-color: ${t} !important;
      `:void 0;return B(f,{color:i?void 0:t,"data-shape":r,"data-size":n,ref:e,css:U(U`
          --color-swatch-size: 6px;
          width: var(--color-swatch-size);
          height: var(--color-swatch-size);
          display: inline-block;
          flex-shrink: 0;
          &[data-shape="square"] {
            border-radius: 2px;
          }
          &[data-shape="circle"] {
            border-radius: 50%;
          }
          &[data-size="S"] {
            --color-swatch-size: 6px;
          }
          &[data-size="M"] {
            --color-swatch-size: 8px;
          }
          &[data-size="L"] {
            --color-swatch-size: 20px;
          }
        `,a)})}uo.displayName=`ColorSwatch`;var fo=U`
  opacity: 0.8;
  color: var(--global-text-color-500);
  .theme--dark & {
    color: var(--global-text-color-400);
  }
  .text {
    color: inherit;
  }
`,po=U`
  margin: var(--global-dimension-size-300);
  display: flex;
  flex-direction: column;
  align-items: center;
`;function mo(e){let{message:t,size:n=`M`}=e;return B(`div`,{css:U`
        width: 100%;
        display: flex;
        justify-content: center;
      `,children:B(`div`,{css:[po,fo],children:t&&B(L,{size:n,children:t})})})}var ho=U`
  width: 100%;
  // border-box so the 100% width includes the padding below; otherwise padding
  // is added outside the full width and overflows the popover → horizontal scroll.
  box-sizing: border-box;
  // Inherit the container's min-height so the glow fills sized regions (a sized
  // View, TableEmptyWrap, or command palette menu) while still wrapping to
  // content in compact popovers.
  min-height: inherit;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: var(--global-dimension-size-50);
  padding: var(--global-dimension-size-200);
  text-align: center;
  // Faint glow behind the center, to lift the icon off the background: a soft
  // dark halo in light mode, flipped to white in dark mode below.
  background: radial-gradient(
    circle 80px at center,
    rgba(0, 0, 0, 0.05),
    transparent
  );
  .theme--dark & {
    background: radial-gradient(
      circle 80px at center,
      rgba(255, 255, 255, 0.03),
      transparent
    );
  }
  .icon-wrap {
    width: 24px;
    height: 24px;
    font-size: 24px;
  }
  // Keep the caption narrow and balance it across lines so a wrap reads as two
  // even lines rather than a long line plus an orphan.
  .text {
    max-width: 180px;
    text-wrap: balance;
  }
`;function go(){let e=(0,Y.c)(2),t=(0,J.useContext)(Ft),n=(0,J.useContext)(u),r=t?.inputValue??n?.inputValue??``,i;return e[0]===r?i=e[1]:(i=r.trim(),e[0]=r,e[1]=i),i.length>0}function _o(e){let t=(0,Y.c)(9),{icon:n,description:r,isFiltered:i}=e,a=go(),o=i??a,s;t[0]===Symbol.for(`react.memo_cache_sentinel`)?(s=[ho,fo],t[0]=s):s=t[0];let c;t[1]!==n||t[2]!==o?(c=o?B(z,{svg:B(ft,{})}):n,t[1]=n,t[2]=o,t[3]=c):c=t[3];let l=o?`No results`:r,u;t[4]===l?u=t[5]:(u=B(L,{size:`S`,children:l}),t[4]=l,t[5]=u);let d;return t[6]!==c||t[7]!==u?(d=V(`div`,{css:s,children:[c,u]}),t[6]=c,t[7]=u,t[8]=d):d=t[8],d}var vo=U`
  display: flex;
  flex-direction: column;
  gap: var(--global-dimension-size-50);
  padding: var(--global-dimension-size-200);
  border-radius: var(--global-rounding-small);
  border: 1px solid var(--global-border-color-default);
  background-color: transparent;
  text-decoration: none;
  color: inherit;
  cursor: pointer;
  transition: border-color 0.15s ease;

  &:hover {
    border-color: var(--global-color-gray-400);
  }
`,yo=U`
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
`;function bo(e){let t=(0,Y.c)(14),{icon:n,title:r,description:i,href:a,external:o}=e,s;t[0]===o?s=t[1]:(s=o?{target:`_blank`,rel:`noopener noreferrer`}:void 0,t[0]=o,t[1]=s);let c;t[2]===r?c=t[3]:(c=B(L,{weight:`heavy`,children:r}),t[2]=r,t[3]=c);let l;t[4]!==n||t[5]!==c?(l=V(W,{direction:`row`,gap:`size-100`,alignItems:`center`,children:[n,c]}),t[4]=n,t[5]=c,t[6]=l):l=t[6];let u;t[7]===i?u=t[8]:(u=B(L,{size:`S`,color:`text-700`,css:yo,children:i}),t[7]=i,t[8]=u);let d;return t[9]!==a||t[10]!==s||t[11]!==l||t[12]!==u?(d=V(`a`,{href:a,css:vo,...s,children:[l,u]}),t[9]=a,t[10]=s,t[11]=l,t[12]=u,t[13]=d):d=t[13],d}function xo(e,t,n){return n==null?!1:e===`horizontal`||e!==`vertical`&&t?.type===`cards`&&(t.columns??1)===2&&t.items.length>=3}var So=U`
  max-width: var(--global-dimension-size-4000);
  text-align: center;
  text-wrap: balance;
`,Co=U`
  display: grid;
  gap: var(--global-dimension-size-200);
  width: min(100%, var(--global-dimension-size-4000));
`,wo=U`
  width: min(100%, calc(var(--global-dimension-size-4000) * 2));
  grid-template-columns: repeat(
    auto-fit,
    minmax(min(100%, var(--global-dimension-size-4000)), 1fr)
  );
`;function To(e){let t=(0,Y.c)(14),{action:n}=e;if(n.type===`strip`){let e;t[0]===n.items?e=t[1]:(e=n.items.map(Do),t[0]=n.items,t[1]=e);let r;return t[2]===e?r=t[3]:(r=B(W,{direction:`row`,gap:`size-100`,wrap:!0,alignItems:`center`,children:e}),t[2]=e,t[3]=r),r}let r=n.columns??1,i=r===2&&wo,a;t[4]===r?a=t[5]:(a=r===1&&U`
            grid-template-columns: 1fr;
          `,t[4]=r,t[5]=a);let o;t[6]!==i||t[7]!==a?(o=[Co,i,a],t[6]=i,t[7]=a,t[8]=o):o=t[8];let s;t[9]===n.items?s=t[10]:(s=n.items.map(Eo),t[9]=n.items,t[10]=s);let c;return t[11]!==o||t[12]!==s?(c=B(`div`,{css:o,children:s}),t[11]=o,t[12]=s,t[13]=c):c=t[13],c}function Eo(e,t){return B(bo,{...e},t)}function Do(e,t){if(e.kind===`link`)return B(Dt,{href:e.href,variant:`quiet`,size:`S`,children:e.label},t);if(e.kind===`node`)return B(J.Fragment,{children:e.node},t);let{kind:n,...r}=e;return B(H,{size:`S`,...r},t)}function Oo({graphic:e,title:t,description:n,action:r,orientation:i=`auto`}){let a=xo(i,r,e),o=r?.type===`cards`?`size-300`:`size-200`,s=r?.type===`cards`?`size-500`:`size-200`,c=t!=null||n!=null?V(W,{direction:`column`,gap:`size-25`,alignItems:`center`,children:[t!=null&&B(L,{size:`L`,weight:`heavy`,children:t}),n!=null&&B(L,{size:`S`,color:`text-700`,css:So,children:n})]}):null;return a?V(W,{direction:`column`,gap:s,alignItems:`center`,children:[V(W,{direction:`row`,wrap:!0,gap:`size-400`,alignItems:`center`,justifyContent:`center`,children:[B(W,{alignItems:`center`,justifyContent:`center`,children:e}),c]}),r!=null&&B(To,{action:r})]}):V(W,{direction:`column`,gap:`size-300`,alignItems:`center`,justifyContent:`center`,children:[e!=null&&e,V(W,{direction:`column`,gap:o,alignItems:`center`,children:[c,r!=null&&B(To,{action:r})]})]})}var ko=U`
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
`,Ao=U`
  flex: 0 1 var(--global-dimension-size-2000);
  min-height: var(--global-dimension-size-750);
`;function jo(e){let t=(0,Y.c)(3),{children:n}=e,r;t[0]===Symbol.for(`react.memo_cache_sentinel`)?(r=B(`div`,{css:Ao,"aria-hidden":`true`}),t[0]=r):r=t[0];let i;return t[1]===n?i=t[2]:(i=V(`div`,{css:ko,children:[r,n]}),t[1]=n,t[2]=i),i}var Mo={size:`small`,icon:B(z,{svg:B(ut,{})})},No={genericAdd:{size:`small`,icon:B(z,{svg:B(jt,{})})},genericEdit:{size:`small`,icon:B(z,{svg:B(Rt,{})})},trace:{size:`large`,icon:B(z,{svg:B(pn,{})})},dataset:{size:`large`,icon:B(z,{svg:B(Mt,{})})},evaluator:{size:`large`,icon:B(z,{svg:B(Xt,{})})},session:{size:`large`,icon:B(z,{svg:B(Bt,{})})},experiment:{size:`large`,icon:B(z,{svg:B(qt,{})})},prompt:{size:`large`,icon:B(z,{svg:B(Kn,{})})},project:{size:`large`,icon:B(z,{svg:B(yt,{})})},annotation:{size:`small`,icon:B(z,{svg:B(Wn,{})})},customAIProvider:{size:`small`,icon:B(z,{svg:B(hn,{})})},event:{size:`small`,icon:B(z,{svg:B(Ln,{})})},attribute:{size:`small`,icon:B(z,{svg:B(Un,{})})},config:{size:`small`,icon:B(z,{svg:B(In,{})})},credential:{size:`small`,icon:B(z,{svg:B(Dn,{})})},version:{size:`small`,icon:B(z,{svg:B(nn,{})})},tag:Mo,label:Mo,split:Mo};Object.keys(No),Object.fromEntries(Object.entries(No).map(([e,t])=>[e,t.size]));var Po=U`
  --esg-card-bg: #fdfdfd;
  --esg-stroke: #e2e2e2;
  --esg-stroke-subtle: #ededed;
  --esg-bar: #e2e2e2;
  --esg-icon: #a8a8a8;
  --esg-dots: #cfcfcf;

  .theme--dark & {
    --esg-card-bg: #101010;
    --esg-stroke: #232323;
    --esg-stroke-subtle: #232323;
    --esg-bar: #1b1b1b;
    --esg-icon: #424242;
    --esg-dots: #282828;
  }
`,Fo=(e,t)=>{let n=`linear-gradient(
    to bottom,
    transparent 0,
    #000 ${e},
    #000 calc(100% - ${t}),
    transparent 100%
  )`;return U`
    -webkit-mask-image: ${n};
    mask-image: ${n};
  `},Io=U`
  display: block;
  margin-bottom: calc(-1 * var(--global-dimension-size-200));
`,Lo=e=>U`
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
  color: var(--esg-icon);
  svg {
    width: ${e}px;
    height: ${e}px;
    display: block;
  }
`;function Ro(e){let t=(0,Y.c)(14),{id:n,x:r,y:i,width:a,height:o}=e,s,c,l,u,d,f,p,m;t[0]===Symbol.for(`react.memo_cache_sentinel`)?(s=B(`feFlood`,{floodOpacity:`0`,result:`BackgroundImageFix`}),c=B(`feColorMatrix`,{in:`SourceAlpha`,type:`matrix`,values:`0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 127 0`,result:`hardAlpha`}),l=B(`feOffset`,{dy:`4`}),u=B(`feGaussianBlur`,{stdDeviation:`6`}),d=B(`feComposite`,{in2:`hardAlpha`,operator:`out`}),f=B(`feColorMatrix`,{type:`matrix`,values:`0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0.19 0`}),p=B(`feBlend`,{mode:`normal`,in2:`BackgroundImageFix`,result:`effect1_dropShadow`}),m=B(`feBlend`,{mode:`normal`,in:`SourceGraphic`,in2:`effect1_dropShadow`,result:`shape`}),t[0]=s,t[1]=c,t[2]=l,t[3]=u,t[4]=d,t[5]=f,t[6]=p,t[7]=m):(s=t[0],c=t[1],l=t[2],u=t[3],d=t[4],f=t[5],p=t[6],m=t[7]);let h;return t[8]!==o||t[9]!==n||t[10]!==a||t[11]!==r||t[12]!==i?(h=V(`filter`,{id:n,x:r,y:i,width:a,height:o,filterUnits:`userSpaceOnUse`,colorInterpolationFilters:`sRGB`,children:[s,c,l,u,d,f,p,m]}),t[8]=o,t[9]=n,t[10]=a,t[11]=r,t[12]=i,t[13]=h):h=t[13],h}function zo(e){let t=(0,Y.c)(10),{x:n,y:r,size:i,icon:a}=e,o;t[0]===i?o=t[1]:(o=Lo(i),t[0]=i,t[1]=o);let s;t[2]!==a||t[3]!==o?(s=B(`div`,{css:o,children:a}),t[2]=a,t[3]=o,t[4]=s):s=t[4];let c;return t[5]!==i||t[6]!==s||t[7]!==n||t[8]!==r?(c=B(`foreignObject`,{x:n,y:r,width:i,height:i,children:s}),t[5]=i,t[6]=s,t[7]=n,t[8]=r,t[9]=c):c=t[9],c}function Bo(e){let t=(0,Y.c)(35),{icon:n,ids:r}=e,i;t[0]===Symbol.for(`react.memo_cache_sentinel`)?(i=[Po,Fo(`34%`,`34%`),Io],t[0]=i):i=t[0];let a=`url(#${r.f0})`,o,s,c;t[1]===Symbol.for(`react.memo_cache_sentinel`)?(o=B(`rect`,{x:`19`,y:`10`,width:`160`,height:`32`,rx:`8`,fill:`var(--esg-card-bg)`,shapeRendering:`crispEdges`}),s=B(`rect`,{x:`19.5`,y:`10.5`,width:`159`,height:`31`,rx:`7.5`,stroke:`var(--esg-stroke)`,shapeRendering:`crispEdges`}),c=B(`rect`,{opacity:`0.68`,x:`31`,y:`22`,width:`136`,height:`8`,rx:`3`,fill:`var(--esg-bar)`}),t[1]=o,t[2]=s,t[3]=c):(o=t[1],s=t[2],c=t[3]);let l;t[4]===a?l=t[5]:(l=V(`g`,{filter:a,children:[o,s,c]}),t[4]=a,t[5]=l);let u=`url(#${r.f1})`,d,f;t[6]===Symbol.for(`react.memo_cache_sentinel`)?(d=B(`rect`,{x:`12`,y:`52`,width:`174`,height:`48`,rx:`8`,fill:`var(--esg-card-bg)`,shapeRendering:`crispEdges`}),f=B(`rect`,{x:`12.5`,y:`52.5`,width:`173`,height:`47`,rx:`7.5`,stroke:`var(--esg-stroke-subtle)`,shapeRendering:`crispEdges`}),t[6]=d,t[7]=f):(d=t[6],f=t[7]);let p;t[8]===n?p=t[9]:(p=B(zo,{x:24,y:66,size:20,icon:n}),t[8]=n,t[9]=p);let m,h;t[10]===Symbol.for(`react.memo_cache_sentinel`)?(m=B(`rect`,{opacity:`0.68`,x:`56`,y:`65`,width:`120`,height:`8`,rx:`3`,fill:`var(--esg-bar)`}),h=B(`rect`,{opacity:`0.68`,x:`56`,y:`79`,width:`80`,height:`8`,rx:`3`,fill:`var(--esg-bar)`}),t[10]=m,t[11]=h):(m=t[10],h=t[11]);let g;t[12]!==p||t[13]!==u?(g=V(`g`,{filter:u,children:[d,f,p,m,h]}),t[12]=p,t[13]=u,t[14]=g):g=t[14];let _=`url(#${r.f2})`,v,y,b;t[15]===Symbol.for(`react.memo_cache_sentinel`)?(v=B(`rect`,{x:`19`,y:`110`,width:`160`,height:`32`,rx:`8`,fill:`var(--esg-card-bg)`,shapeRendering:`crispEdges`}),y=B(`rect`,{x:`19.5`,y:`110.5`,width:`159`,height:`31`,rx:`7.5`,stroke:`var(--esg-stroke)`,shapeRendering:`crispEdges`}),b=B(`rect`,{opacity:`0.68`,x:`31`,y:`122`,width:`136`,height:`8`,rx:`3`,fill:`var(--esg-bar)`}),t[15]=v,t[16]=y,t[17]=b):(v=t[15],y=t[16],b=t[17]);let x;t[18]===_?x=t[19]:(x=V(`g`,{filter:_,children:[v,y,b]}),t[18]=_,t[19]=x);let S;t[20]===r.f0?S=t[21]:(S=B(Ro,{id:r.f0,x:7,y:2,width:184,height:56}),t[20]=r.f0,t[21]=S);let C;t[22]===r.f1?C=t[23]:(C=B(Ro,{id:r.f1,x:0,y:44,width:198,height:72}),t[22]=r.f1,t[23]=C);let w;t[24]===r.f2?w=t[25]:(w=B(Ro,{id:r.f2,x:7,y:102,width:184,height:56}),t[24]=r.f2,t[25]=w);let T;t[26]!==S||t[27]!==C||t[28]!==w?(T=V(`defs`,{children:[S,C,w]}),t[26]=S,t[27]=C,t[28]=w,t[29]=T):T=t[29];let E;return t[30]!==g||t[31]!==x||t[32]!==T||t[33]!==l?(E=V(`svg`,{width:`198`,height:`158`,viewBox:`0 0 198 158`,fill:`none`,xmlns:`http://www.w3.org/2000/svg`,"aria-hidden":`true`,focusable:`false`,css:i,children:[l,g,x,T]}),t[30]=g,t[31]=x,t[32]=T,t[33]=l,t[34]=E):E=t[34],E}function Vo(e){let t=(0,Y.c)(40),{icon:n,ids:r}=e,i;t[0]===Symbol.for(`react.memo_cache_sentinel`)?(i=[Po,Fo(`38%`,`31%`),Io],t[0]=i):i=t[0];let a=`url(#${r.f0})`,o,s,c,l,u,d;t[1]===Symbol.for(`react.memo_cache_sentinel`)?(o=B(`rect`,{x:`12`,y:`8`,width:`174`,height:`32`,rx:`8`,fill:`var(--esg-card-bg)`,shapeRendering:`crispEdges`}),s=B(`rect`,{x:`12.5`,y:`8.5`,width:`173`,height:`31`,rx:`7.5`,stroke:`var(--esg-stroke)`,shapeRendering:`crispEdges`}),c=B(`path`,{d:`M27.75 22.5C28.5784 22.5 29.25 23.1716 29.25 24C29.25 24.8284 28.5784 25.5 27.75 25.5C26.9216 25.5 26.25 24.8284 26.25 24C26.25 23.1716 26.9216 22.5 27.75 22.5Z`,fill:`var(--esg-dots)`}),l=B(`path`,{d:`M33 22.5C33.8284 22.5 34.5 23.1716 34.5 24C34.5 24.8284 33.8284 25.5 33 25.5C32.1716 25.5 31.5 24.8284 31.5 24C31.5 23.1716 32.1716 22.5 33 22.5Z`,fill:`var(--esg-dots)`}),u=B(`path`,{d:`M38.25 22.5C39.0784 22.5 39.75 23.1716 39.75 24C39.75 24.8284 39.0784 25.5 38.25 25.5C37.4216 25.5 36.75 24.8284 36.75 24C36.75 23.1716 37.4216 22.5 38.25 22.5Z`,fill:`var(--esg-dots)`}),d=B(`rect`,{opacity:`0.68`,x:`54`,y:`20`,width:`120`,height:`8`,rx:`3`,fill:`var(--esg-bar)`}),t[1]=o,t[2]=s,t[3]=c,t[4]=l,t[5]=u,t[6]=d):(o=t[1],s=t[2],c=t[3],l=t[4],u=t[5],d=t[6]);let f;t[7]===a?f=t[8]:(f=V(`g`,{filter:a,children:[o,s,c,l,u,d]}),t[7]=a,t[8]=f);let p=`url(#${r.f1})`,m,h;t[9]===Symbol.for(`react.memo_cache_sentinel`)?(m=B(`rect`,{x:`12`,y:`50`,width:`174`,height:`32`,rx:`8`,fill:`var(--esg-card-bg)`,shapeRendering:`crispEdges`}),h=B(`rect`,{x:`12.5`,y:`50.5`,width:`173`,height:`31`,rx:`7.5`,stroke:`var(--esg-stroke-subtle)`,shapeRendering:`crispEdges`}),t[9]=m,t[10]=h):(m=t[9],h=t[10]);let g;t[11]===n?g=t[12]:(g=B(zo,{x:25,y:58,size:16,icon:n}),t[11]=n,t[12]=g);let _;t[13]===Symbol.for(`react.memo_cache_sentinel`)?(_=B(`rect`,{opacity:`0.68`,x:`54`,y:`62`,width:`120`,height:`8`,rx:`3`,fill:`var(--esg-bar)`}),t[13]=_):_=t[13];let v;t[14]!==p||t[15]!==g?(v=V(`g`,{filter:p,children:[m,h,g,_]}),t[14]=p,t[15]=g,t[16]=v):v=t[16];let y=`url(#${r.f2})`,b,x,S,C,w,T;t[17]===Symbol.for(`react.memo_cache_sentinel`)?(b=B(`rect`,{x:`12`,y:`92`,width:`174`,height:`32`,rx:`8`,fill:`var(--esg-card-bg)`,shapeRendering:`crispEdges`}),x=B(`rect`,{x:`12.5`,y:`92.5`,width:`173`,height:`31`,rx:`7.5`,stroke:`var(--esg-stroke)`,shapeRendering:`crispEdges`}),S=B(`path`,{d:`M27.75 106.5C28.5784 106.5 29.25 107.172 29.25 108C29.25 108.828 28.5784 109.5 27.75 109.5C26.9216 109.5 26.25 108.828 26.25 108C26.25 107.172 26.9216 106.5 27.75 106.5Z`,fill:`var(--esg-dots)`}),C=B(`path`,{d:`M33 106.5C33.8284 106.5 34.5 107.172 34.5 108C34.5 108.828 33.8284 109.5 33 109.5C32.1716 109.5 31.5 108.828 31.5 108C31.5 107.172 32.1716 106.5 33 106.5Z`,fill:`var(--esg-dots)`}),w=B(`path`,{d:`M38.25 106.5C39.0784 106.5 39.75 107.172 39.75 108C39.75 108.828 39.0784 109.5 38.25 109.5C37.4216 109.5 36.75 108.828 36.75 108C36.75 107.172 37.4216 106.5 38.25 106.5Z`,fill:`var(--esg-dots)`}),T=B(`rect`,{opacity:`0.68`,x:`54`,y:`104`,width:`120`,height:`8`,rx:`3`,fill:`var(--esg-bar)`}),t[17]=b,t[18]=x,t[19]=S,t[20]=C,t[21]=w,t[22]=T):(b=t[17],x=t[18],S=t[19],C=t[20],w=t[21],T=t[22]);let E;t[23]===y?E=t[24]:(E=V(`g`,{filter:y,children:[b,x,S,C,w,T]}),t[23]=y,t[24]=E);let D;t[25]===r.f0?D=t[26]:(D=B(Ro,{id:r.f0,x:0,y:0,width:198,height:56}),t[25]=r.f0,t[26]=D);let O;t[27]===r.f1?O=t[28]:(O=B(Ro,{id:r.f1,x:0,y:42,width:198,height:56}),t[27]=r.f1,t[28]=O);let k;t[29]===r.f2?k=t[30]:(k=B(Ro,{id:r.f2,x:0,y:84,width:198,height:56}),t[29]=r.f2,t[30]=k);let A;t[31]!==D||t[32]!==O||t[33]!==k?(A=V(`defs`,{children:[D,O,k]}),t[31]=D,t[32]=O,t[33]=k,t[34]=A):A=t[34];let j;return t[35]!==v||t[36]!==E||t[37]!==A||t[38]!==f?(j=V(`svg`,{width:`198`,height:`140`,viewBox:`0 0 198 140`,fill:`none`,xmlns:`http://www.w3.org/2000/svg`,"aria-hidden":`true`,focusable:`false`,css:i,children:[f,v,E,A]}),t[35]=v,t[36]=E,t[37]=A,t[38]=f,t[39]=j):j=t[39],j}function Ho({variant:e=`genericAdd`}){let{size:t,icon:n}=No[e],r=(0,J.useId)(),i={f0:`${r}-f0`,f1:`${r}-f1`,f2:`${r}-f2`};return B(t===`small`?Vo:Bo,{icon:n,ids:i})}function Uo(e){let t=(0,Y.c)(2),{children:n}=e;if(typeof n==`string`){let e;return t[0]===n?e=t[1]:(e=B(ot,{level:1,children:n}),t[0]=n,t[1]=e),e}return n}function Wo(e){let t=(0,Y.c)(2),{children:n}=e;if(!n)return null;if(typeof n==`string`){let e;return t[0]===n?e=t[1]:(e=B(L,{size:`S`,color:`text-700`,children:n}),t[0]=n,t[1]=e),e}return n}function Go(e){let t=(0,Y.c)(10),{title:n,subTitle:r,extra:i}=e,a;t[0]===n?a=t[1]:(a=B(Uo,{children:n}),t[0]=n,t[1]=a);let o;t[2]===r?o=t[3]:(o=B(Wo,{children:r}),t[2]=r,t[3]=o);let s;t[4]!==a||t[5]!==o?(s=V(W,{direction:`column`,gap:`size-50`,minWidth:0,children:[a,o]}),t[4]=a,t[5]=o,t[6]=s):s=t[6];let c;return t[7]!==i||t[8]!==s?(c=B(ta,{padding:`size-200`,flex:`none`,"data-testid":`page-header`,children:V(W,{direction:`row`,justifyContent:`space-between`,alignItems:`center`,"data-testid":`page-header-content`,gap:`size-100`,children:[s,i]})}),t[7]=i,t[8]=s,t[9]=c):c=t[9],c}var Ko=U`
  border-radius: 16px;
  padding: var(--global-dimension-size-50) var(--global-dimension-size-200) !important;
`,qo=e=>{let t=(0,Y.c)(10),{onLoadMore:n,isLoadingNext:r,buttonProps:i}=e,a;t[0]===n?a=t[1]:(a=()=>{n()},t[0]=n,t[1]=a);let o;t[2]===r?o=t[3]:(o=r?B(z,{svg:B(_n,{})}):void 0,t[2]=r,t[3]=o);let s=r?`Loading...`:`Load More`,c;return t[4]!==i||t[5]!==r||t[6]!==a||t[7]!==o||t[8]!==s?(c=B(H,{onPress:a,size:`S`,css:Ko,isDisabled:r,leadingVisual:o,...i,children:s}),t[4]=i,t[5]=r,t[6]=a,t[7]=o,t[8]=s,t[9]=c):c=t[9],c};function Jo(e,{filled:t}={filled:!0}){let n;switch(e){case`warning`:n=B(t?rn:_t,{});break;case`info`:n=B(t?un:Un,{});break;case`danger`:n=B(t?Fn:bt,{});break;case`success`:n=B(t?Yn:sn,{})}return B(z,{svg:n})}var Yo=U`
  --alert-base-color: var(--global-color-info);
  --alert-bg-color: lch(from var(--alert-base-color) 96 calc(c * 0.3) h);
  --alert-border-color: lch(from var(--alert-base-color) 88 calc(c * 0.4) h);
  --alert-text-color: lch(from var(--alert-base-color) 45 c h);

  padding: var(--global-dimension-size-100) var(--global-dimension-size-200);
  border-radius: var(--global-rounding-small);
  color: var(--alert-text-color);
  display: flex;
  flex-direction: row;
  align-items: center;
  backdrop-filter: blur(10px);
  border: 1px solid var(--alert-border-color);
  background-color: var(--alert-bg-color);

  &[data-banner="true"] {
    border-radius: 0;
    border-left: 0px;
    border-right: 0px;
  }

  &[data-variant="warning"] {
    --alert-base-color: var(--global-color-warning);
  }

  &[data-variant="info"] {
    --alert-base-color: var(--global-color-info);
  }

  &[data-variant="danger"] {
    --alert-base-color: var(--global-color-danger);
  }

  &[data-variant="success"] {
    --alert-base-color: var(--global-color-success);
  }

  &[data-theme="light"] {
    --alert-bg-color: lch(from var(--alert-base-color) 96 calc(c * 0.3) h);
    --alert-border-color: lch(from var(--alert-base-color) 88 calc(c * 0.4) h);
    --alert-text-color: lch(from var(--alert-base-color) 45 c h);
  }

  &[data-theme="dark"] {
    --alert-bg-color: lch(from var(--alert-base-color) 18 calc(c * 0.2) h);
    --alert-border-color: lch(from var(--alert-base-color) 28 calc(c * 0.3) h);
    --alert-text-color: lch(from var(--alert-base-color) 90 calc(c * 0.8) h);
  }

  .alert__icon-title-wrap {
    display: flex;
    flex-direction: row;

    .icon-wrap {
      margin-right: var(--global-dimension-size-100);
      font-size: var(--global-font-size-m);
      display: flex;
      align-items: center;
      height: var(--global-line-height-s);
    }
  }

  &[data-has-title="true"] .alert__icon-title-wrap .icon-wrap {
    height: var(--global-line-height-m);
  }
`,Xo=U`
  display: flex;
  flex-direction: row;
  align-items: flex-start;
  flex: 1 1 auto;
`,Zo=U`
  background-color: transparent;
  color: inherit;
  padding: 0;
  border: none;
  cursor: pointer;
  width: 20px;
  height: 20px;
  margin-left: var(--global-dimension-size-200);
`,Qo=({variant:e,title:t,icon:n,children:r,showIcon:i=!0,dismissable:a=!1,onDismissClick:o,banner:s=!1,extra:c,...l})=>{let{theme:u}=Mr();return!n&&i&&(n=Jo(e)),V(`div`,{...l,css:Yo,"data-variant":e,"data-banner":s,"data-has-title":!!t,"data-theme":u,children:[V(`div`,{css:Xo,className:`alert__icon-title-wrap`,children:[n,V(`div`,{children:[t?B(L,{elementType:`h5`,size:`M`,weight:`heavy`,color:`inherit`,children:t}):null,B(L,{color:`inherit`,size:`S`,children:r})]})]}),c,a?B(`button`,{css:Zo,onClick:o,children:B(z,{svg:B(Ht,{})})}):null]})},$o=U`
  --badge-base-color: var(--global-color-gray-600);
  --badge-bg-color: lch(from var(--badge-base-color) 96 calc(c * 0.3) h);
  --badge-border-color: lch(from var(--badge-base-color) 88 calc(c * 0.4) h);
  --badge-text-color: lch(from var(--badge-base-color) 45 c h);

  display: inline-flex;
  align-items: center;
  gap: var(--global-badge-gap);
  border: 1px solid var(--badge-border-color);
  border-radius: var(--global-badge-border-radius);
  background-color: var(--badge-bg-color);
  color: var(--badge-text-color);
  white-space: normal;
  box-sizing: border-box;

  &[data-overflow-mode="truncate"] {
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  /* Sizes */
  &[data-size="S"] {
    font-size: var(--global-badge-font-size-s);
    padding: var(--global-badge-padding-y-s) var(--global-badge-padding-x-s);
  }
  &[data-size="M"] {
    font-size: var(--global-badge-font-size-m);
    padding: var(--global-badge-padding-y-m) var(--global-badge-padding-x-m);
  }
  &[data-size="L"] {
    font-size: var(--global-badge-font-size-l);
    padding: var(--global-badge-padding-y-l) var(--global-badge-padding-x-l);
  }

  /* Variants */
  &[data-variant="info"] {
    --badge-base-color: var(--global-color-info);
  }
  &[data-variant="success"] {
    --badge-base-color: var(--global-color-success);
  }
  &[data-variant="warning"] {
    --badge-base-color: var(--global-color-warning);
  }
  &[data-variant="danger"] {
    --badge-base-color: var(--global-color-danger);
  }

  /* Theme-aware color derivation */
  &[data-theme="light"] {
    --badge-bg-color: lch(from var(--badge-base-color) 96 calc(c * 0.3) h);
    --badge-border-color: lch(from var(--badge-base-color) 88 calc(c * 0.4) h);
    --badge-text-color: lch(from var(--badge-base-color) 45 c h);
  }
  &[data-theme="dark"] {
    --badge-bg-color: lch(from var(--badge-base-color) 18 calc(c * 0.2) h);
    --badge-border-color: lch(from var(--badge-base-color) 28 calc(c * 0.3) h);
    --badge-text-color: lch(from var(--badge-base-color) 90 calc(c * 0.8) h);
  }
`,es=({children:e,variant:t=`default`,size:n=`S`,overflowMode:r=`wrap`,css:i,...a})=>{let{theme:o}=Mr();return B(`span`,{...a,css:U($o,i),"data-variant":t,"data-size":n,"data-overflow-mode":r,"data-theme":o,className:`badge`,children:e})},ts=U`
  & > * {
    width: 100%;
    .react-aria-Heading {
      width: 100%;
      .react-aria-Button[slot="trigger"] {
        width: 100%;
      }
    }
  }

  // add border between items, only when child is expanded
  > .disclosure:not(:last-child) {
    &[data-expanded="true"] {
      border-bottom: 1px solid var(--global-border-color-default);
    }
  }

  &[data-size="S"] > * {
    .react-aria-Heading {
      .react-aria-Button[slot="trigger"] {
        padding: var(--global-dimension-size-50);
      }
    }
  }
`,ns=U`
  .react-aria-Heading {
    margin: 0;
  }

  [slot="trigger"] {
    // reset trigger styles
    background: none;
    border: none;
    box-shadow: none;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 8px;
    font-size: var(--global-font-size-s);
    line-height: var(--global-line-height-s);
    padding: var(--global-dimension-size-100) var(--global-dimension-size-200);

    // style trigger
    color: var(--global-text-color-900);
    border-bottom: 1px solid var(--global-border-color-default);
    outline: none;
    background-color: transparent;
    &:hover:not([disabled]) {
      background-color: var(--global-disclosure-background-color-active);
    }
    &[data-focus-visible] {
      position: relative;
      z-index: 1;
      outline: var(--focus-ring-thickness) solid var(--focus-ring-color);
      outline-offset: calc(-1 * var(--focus-ring-thickness));
    }
    &:not([disabled]) {
      transition: all 0.2s ease-in-out;
    }
    &[disabled] {
      cursor: default;
      opacity: 0.6;
    }

    // style trigger icon
    > svg,
    > i {
      rotate: 90deg;
      transition: rotate 200ms ease-in-out;
      width: 1em;
      height: 1em;
      fill: currentColor;
      color: var(--global-text-color-500);
    }

    &[data-arrow-position="start"] {
      flex-direction: row-reverse;
      > svg,
      > i {
        rotate: 0deg;
      }
    }
  }

  &[data-size="L"] .react-aria-Button[slot="trigger"] {
    height: 48px;
    max-height: 48px;
  }

  &[data-expanded] .react-aria-Button[slot="trigger"] {
    > svg,
    > i {
      rotate: -90deg;
    }

    &[data-arrow-position="start"] {
      > svg,
      > i {
        rotate: 90deg;
      }
    }
  }
`,rs=e=>{let t=(0,Y.c)(14),n,r,i,a;t[0]===e?(n=t[1],r=t[2],i=t[3],a=t[4]):({className:n,css:r,size:a,...i}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a);let o;t[5]===n?o=t[6]:(o=F(`disclosure-group`,n),t[5]=n,t[6]=o);let s;t[7]===r?s=t[8]:(s=U(ts,r),t[7]=r,t[8]=s);let c;return t[9]!==i||t[10]!==a||t[11]!==o||t[12]!==s?(c=B(d,{allowsMultipleExpanded:!0,className:o,css:s,"data-size":a,...i}),t[9]=i,t[10]=a,t[11]=o,t[12]=s,t[13]=c):c=t[13],c},is=e=>{let t=(0,Y.c)(10),n,r,i;t[0]===e?(n=t[1],r=t[2],i=t[3]):({size:i,className:n,...r}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i);let a;t[4]===n?a=t[5]:(a=F(`disclosure`,n),t[4]=n,t[5]=a);let o;return t[6]!==r||t[7]!==i||t[8]!==a?(o=B(l,{className:a,css:ns,"data-size":i,defaultExpanded:!0,...r}),t[6]=r,t[7]=i,t[8]=a,t[9]=o):o=t[9],o},as=e=>{let t=(0,Y.c)(8),n,r;t[0]===e?(n=t[1],r=t[2]):({className:n,...r}=e,t[0]=e,t[1]=n,t[2]=r);let i;t[3]===n?i=t[4]:(i=F(`disclosure__panel`,n),t[3]=n,t[4]=i);let a;return t[5]!==r||t[6]!==i?(a=B(m,{className:i,...r}),t[5]=r,t[6]=i,t[7]=a):a=t[7],a},os=({children:e,arrowPosition:t,justifyContent:n,alignItems:r=`center`,direction:i=`row`,width:a})=>B(Ut,{className:`react-aria-Heading disclosure__trigger`,children:V(xt,{slot:`trigger`,"data-arrow-position":t,style:{width:a},children:[B(W,{justifyContent:n,direction:i,alignItems:r,width:`100%`,gap:i===`row`?`size-100`:`size-50`,children:e}),t===`none`?null:B(z,{svg:B(er,{})})]})}),ss=U`
  &[data-required] {
    .react-aria-Label {
      &::after {
        content: " *";
      }
    }
  }
  .react-aria-Label {
    padding: 5px 0;
    display: inline-block;
    font-size: var(--global-font-size-xs);
    line-height: var(--global-line-height-xs);
    font-weight: var(--font-weight-heavy);
  }

  .react-aria-Input,
  .react-aria-TextArea {
    transition: all 0.2s ease-in-out;
    margin: 0;
    flex: 1 1 auto;
    font-size: var(--global-font-size-s);
    // --field-min-width lets a field that has to fit a narrow container (a
    // flexed toolbar slot, a control that collapses to an icon) shrink below
    // the comfortable default rather than overriding this rule.
    min-width: var(--field-min-width, var(--global-input-field-min-width));
    background-color: var(--field-background-color);
    color: var(--field-text-color);
    border: var(--global-border-size-thin) solid var(--field-border-color);
    border-radius: var(--global-rounding-small);
    vertical-align: middle;

    &[data-focused] {
      // Pointer and programmatic focus emphasize the field boundary without
      // showing the keyboard focus ring.
      outline: none;
    }
    &[data-focused]:not([data-invalid]) {
      border-color: var(--field-border-color-active);
    }
    &[data-focus-visible] {
      outline: var(--focus-ring-thickness) solid var(--focus-ring-color);
      outline-offset: calc(-1 * var(--focus-ring-thickness));
    }
    &[data-hovered]:not([data-disabled]):not([data-invalid]) {
      border: 1px solid var(--field-border-color-active);
    }
    // Readonly reaches the input as the native \`readonly\` attribute (react-aria
    // does not emit data-readonly on the input), so we can style it directly.
    &:is([data-readonly], [readonly]) {
      background-color: var(--field-readonly-background-color);
      border-color: transparent;
      color: var(--field-readonly-text-color);
    }
    &:is([data-readonly], [readonly])[data-focused]:not([data-invalid]) {
      border-color: transparent;
    }
    &:is([data-readonly], [readonly])[data-focus-visible]:not([data-invalid]) {
      background-color: var(--field-readonly-background-color-hover);
      border-color: var(--field-readonly-border-color-focus);
      outline: var(--focus-ring-thickness) solid
        var(--field-readonly-border-color-focus);
      outline-offset: calc(-1 * var(--focus-ring-thickness));
    }
    &:is([data-readonly], [readonly])[data-hovered]:not([data-invalid]):not(
      [data-focus-visible]
    ) {
      background-color: var(--field-readonly-background-color-hover);
      border-color: transparent;
    }
    &[data-disabled] {
      opacity: var(--global-opacity-disabled);
    }
    &[data-invalid="true"] {
      border: 1px solid var(--field-invalid-border-color);
    }
    &::placeholder {
      color: var(--field-placeholder-color);
      font-style: italic;
    }
  }
  // Give the input a hover affordance when a sibling button (e.g. the copy /
  // reveal button) is interacted with. This depends on the parent field, so it
  // cannot be derived from the input's own state.
  &[data-readonly]:has(button:hover),
  &[data-readonly]:has(button[data-focus-visible]),
  &[data-readonly]:has(button:focus-visible) {
    .react-aria-Input,
    .react-aria-TextArea {
      background-color: var(--field-readonly-background-color-hover);
    }
  }
  [slot="description"],
  [slot="errorMessage"],
  .react-aria-FieldError {
    /* The overriding cascade here is non ideal but it lets us have only one notion of text  */
    font-size: var(--global-font-size-xs) !important;
    padding-top: var(--global-dimension-size-50);
    display: inline-block;
    line-height: var(--global-dimension-font-size-200) !important;
  }

  [slot="description"] {
    color: var(--field-description-text-color);
  }

  .react-aria-FieldError {
    color: var(--field-error-text-color);
  }
`,cs=U`
  width: var(--trigger-width);
  background-color: var(--field-popover-background-color);
  border-radius: var(--global-rounding-small);
  color: var(--field-text-color);
  box-shadow: 0px 4px 10px var(--field-popover-shadow-color);
  border: 1px solid var(--field-popover-border-color);
  max-height: inherit;
`,ls=U`
  position: relative;
  width: 100%;
  --field-icon-vertical-position: 50%;

  :has(.react-aria-Label) {
    /* 24px is the height of the label. TODO: make this variable based */
    --field-icon-vertical-position: calc(
      var(--textfield-vertical-padding) + 1px + 24px
    );
  }

  &[data-size="S"] {
    --textfield-input-height: var(--global-input-height-s);
    --textfield-vertical-padding: var(--global-dimension-size-75);
    --textfield-horizontal-padding: var(--global-dimension-size-75);
    --icon-size: var(--global-font-size-s);
  }
  &[data-size="M"] {
    --textfield-input-height: var(--global-input-height-m);
    --textfield-vertical-padding: var(--global-dimension-size-125);
    --textfield-horizontal-padding: var(--global-dimension-size-125);
    --icon-size: var(--global-font-size-m);
  }
  &[data-size="L"] {
    --textfield-input-height: var(--global-input-height-l);
    --textfield-vertical-padding: var(--global-dimension-size-150);
    --textfield-horizontal-padding: var(--global-dimension-size-150);
    --icon-size: var(--global-font-size-l);
  }

  &:has(.field__icon) {
    .react-aria-Input {
      padding-right: calc(
        var(--textfield-horizontal-padding) + var(--icon-size)
      );
    }
  }

  /* Icons */
  .field__icon {
    position: absolute;
    right: var(--textfield-horizontal-padding);
    top: var(--field-icon-vertical-position);
  }

  // Colors, background, border-radius, and the readonly background/border are
  // inherited from fieldBaseCSS (always composed before this). textFieldCSS
  // layers on sizing and preserves the field focus treatment at its higher
  // selector specificity.
  .react-aria-Input,
  .react-aria-TextArea,
  input {
    width: 100%;
    border: var(--global-border-size-thin) solid
      var(--field-border-color-override, var(--field-border-color));
    padding: var(--textfield-vertical-padding)
      var(--textfield-horizontal-padding);
    box-sizing: border-box;
    outline-offset: -1px;
    outline: var(--focus-ring-thickness) solid transparent;
    &[data-focused]:not([data-invalid]) {
      border-width: var(--global-border-size-thin);
    }
    &[data-focused][data-invalid] {
      border-width: var(--global-border-size-thin);
    }
    &[data-focus-visible] {
      outline: var(--focus-ring-thickness) solid var(--focus-ring-color);
    }
    // Suppress the focus outline while readonly (fieldBaseCSS handles the
    // readonly background/border), then restore it only for keyboard focus.
    &:is([data-readonly], [readonly]) {
      outline-color: transparent;
    }
    &:is([data-readonly], [readonly])[data-focused]:not([data-invalid]) {
      outline-color: transparent;
    }
    &:is([data-readonly], [readonly])[data-focus-visible]:not([data-invalid]) {
      border-width: var(--global-border-size-thin);
      outline: var(--focus-ring-thickness) solid
        var(--field-readonly-border-color-focus);
    }
  }

  .react-aria-Input {
    /* TODO: remove this sizing */
    height: var(--textfield-input-height);
  }

  .react-aria-TextArea {
    // Fix the line height and derive the vertical padding from it so a
    // single-line textarea lands exactly on the input height.
    --textarea-vertical-padding: calc(
      (var(--textfield-input-height) - var(--global-line-height-s)) / 2 -
        var(--global-border-size-thin)
    );
    line-height: var(--global-line-height-s);
    padding-top: var(--textarea-vertical-padding);
    padding-bottom: var(--textarea-vertical-padding);
  }

  [slot="description"],
  [slot="errorMessage"],
  .react-aria-FieldError {
    grid-area: help;
  }
`,us=U`
  &[data-size="M"] {
    --combobox-input-height: var(--global-input-height-s);
    --combobox-vertical-padding: 6px;
    --combobox-start-padding: var(--global-dimension-size-100);
    --combobox-end-padding: var(--global-dimension-size-50);
  }
  &[data-size="L"] {
    --combobox-input-height: var(--global-input-height-m);
    --combobox-vertical-padding: 10px;
    --combobox-start-padding: var(--global-dimension-size-200);
    --combobox-end-padding: var(--global-dimension-size-100);
  }
  color: var(--global-text-color-900);
  &[data-required] {
    .react-aria-Label {
      &::after {
        content: " *";
      }
    }
  }

  .combobox__container {
    display: flex;
    flex-direction: row;
    min-width: 200px;
    position: relative;

    .react-aria-Input {
      height: var(--combobox-input-height);
      box-sizing: border-box;
      padding: var(--combobox-vertical-padding) var(--combobox-end-padding)
        var(--combobox-vertical-padding) var(--combobox-start-padding);
      }
    }
    .react-aria-Button {
      /* Account for the border width of the input */
      padding: 0 calc(var(--combobox-end-padding) + 1px);
      background: none;
      color: inherit;
      forced-color-adjust: none;
      position: absolute;
      top: 50%;
      right: 0;
      border: none;
      transform: translateY(-50%);
      cursor: pointer;

      &[data-disabled] {
        opacity: var(--global-opacity-disabled);
      }
    }
  }
`,ds=U(cs,U`
    .react-aria-ListBox {
      display: block;
      width: unset;
      max-height: inherit;
      min-height: unset;
      border: none;
      overflow: auto;
    }
  `),fs=U`
  outline: none;
  display: flex;
  align-items: center;
  justify-content: space-between;
  color: var(--global-text-color-900);
  padding: var(--global-dimension-size-100) var(--global-dimension-size-200);
  font-size: var(--global-dimension-font-size-100);
  cursor: pointer;
  position: relative;
  & > .icon-wrap.menu-item__selected-checkmark {
    height: var(--global-dimension-size-200);
    width: var(--global-dimension-size-200);
  }
  &[href] {
    text-decoration: none;
    cursor: pointer;
  }
  &[data-selected] {
    i {
      color: var(--global-color-primary);
    }
  }
  &[data-focused],
  &[data-hovered] {
    background-color: var(--global-menu-item-background-color-hover);
  }

  &[data-disabled] {
    cursor: not-allowed;
    color: var(--global-color-text-30);
  }
  &[data-focus-visible] {
    outline: none;
  }
`,ps=e=>{e.stopPropagation()};function ms({label:e,placeholder:t,description:n,errorMessage:r,children:i,size:a=`M`,width:o,stopPropagation:s,renderEmptyState:c,isInvalid:l,menuTrigger:u=`focus`,...d}){return V(w,{...d,menuTrigger:u,css:U(ss,us),"data-size":a,isInvalid:l||!!r,style:{width:o},allowsEmptyCollection:!!c,children:[e&&B(Sn,{children:e}),V(`div`,{className:`combobox__container`,onClick:s?ps:void 0,onKeyDown:s?ps:void 0,onKeyUp:s?ps:void 0,children:[B(Ne,{placeholder:t}),B(xt,{children:B(mt,{})})]}),n&&!r?B(Kt,{slot:`description`,children:n}):null,B(fe,{children:r}),B(mn,{css:ds,children:B(p,{renderEmptyState:c,children:i})})]})}function hs(e){let t=(0,Y.c)(8),n,r;t[0]===e?(n=t[1],r=t[2]):({children:n,...r}=e,t[0]=e,t[1]=n,t[2]=r);let i;t[3]===n?i=t[4]:(i=e=>{let{isSelected:t}=e;return V(R,{children:[n,t&&B(z,{svg:B(yn,{}),className:`menu-item__selected-checkmark`})]})},t[3]=n,t[4]=i);let a;return t[5]!==r||t[6]!==i?(a=B(De,{...r,css:fs,children:i}),t[5]=r,t[6]=i,t[7]=a):a=t[7],a}function gs({ref:e,...t}){let{size:n=`M`,...r}=t;return B(ue,{"data-size":n,className:`text-field`,ref:e,...r,css:U(ss,ls)})}var _s=()=>{let e=(0,Y.c)(1),t;return e[0]===Symbol.for(`react.memo_cache_sentinel`)?(t=B(z,{className:`search-field__icon`,svg:B(ft,{})}),e[0]=t):t=e[0],t},vs=U`
  display: grid;
  grid-template-areas:
    "label label label"
    "icon input clear"
    "help help help";
  grid-template-columns: auto 1fr auto;
  align-items: center;

  /* Size-specific icon sizes to match TextField sizing */
  &[data-size="S"] {
    --searchfield-icon-size: var(--global-font-size-s);
  }
  &[data-size="M"] {
    --searchfield-icon-size: var(--global-font-size-m);
  }
  &[data-size="L"] {
    --searchfield-icon-size: var(--global-font-size-l);
  }

  .react-aria-Label {
    grid-area: label;
  }

  .search-field__icon {
    grid-area: icon;
    position: absolute;
    left: var(--textfield-horizontal-padding);
    top: 50%;
    transform: translateY(-50%);
    font-size: var(--searchfield-icon-size);
  }

  .react-aria-Input {
    grid-area: input;
    width: 100%;

    /* Hide browser native clear button since we have a custom one */
    &::-webkit-search-cancel-button,
    &::-webkit-search-decoration {
      -webkit-appearance: none;
      appearance: none;
      display: none;
    }
  }

  [slot="description"],
  [slot="errorMessage"],
  .react-aria-FieldError {
    grid-area: help;
  }

  .search-field__clear {
    grid-area: clear;
    position: absolute;
    /* account for clear button size */
    right: calc(var(--textfield-horizontal-padding) - 2px);
    top: 50%;
    transform: translateY(-50%);
    background: none;
    border: none;
    padding: 2px;
    cursor: pointer;
    color: var(--global-text-color-700);
    border-radius: var(--global-rounding-small);
    display: flex;
    align-items: center;
    justify-content: center;
    outline: none;
    font-size: var(--searchfield-icon-size);

    &[data-focus-visible] {
      outline: var(--focus-ring-thickness) solid var(--focus-ring-color);
      outline-offset: var(--focus-ring-offset);
    }

    &:hover {
      color: var(--global-text-color-900);
      background-color: var(--global-color-gray-300);
    }

    &[data-empty] {
      display: none;
    }
  }

  /*
   * The input's side padding clears the icon on the left and the clear button
   * on the right: inset + icon + gap (gap = inset). It carries !important to
   * beat the size-specific padding the shared text field rules set, so a
   * consumer needing a different inset — a search collapsed to an icon square,
   * a toolbar with its own icon metrics — sets these variables rather than
   * out-shouting the cascade in turn. Left undeclared here so that a value set
   * anywhere above the field wins.
   */
  .search-field__icon ~ .react-aria-Input {
    padding-left: var(
      --searchfield-input-padding-start,
      calc(
        var(--textfield-horizontal-padding) * 2 + var(--searchfield-icon-size)
      )
    ) !important;
  }

  .react-aria-Input {
    padding-right: var(
      --searchfield-input-padding-end,
      calc(
        var(--textfield-horizontal-padding) * 2 + var(--searchfield-icon-size)
      )
    ) !important;
  }

  &[data-invalid="true"] {
    .search-field__icon {
      color: var(--global-color-danger);
    }
  }

  &[data-variant="quiet"] {
    .react-aria-Input {
      background-color: transparent;
      border-color: transparent;
      border-radius: 0;
      outline: none;
    }

    .react-aria-Input[data-hovered]:not([data-disabled]):not([data-invalid]) {
      border-color: transparent;
    }

    .react-aria-Input[data-focused] {
      border-color: transparent;
      outline: none;
    }
  }
`;function ys({ref:e,...t}){let{size:n=`M`,variant:r=`default`,children:i,isReadOnly:a,...o}=t;return B(S,{"data-size":n,"data-variant":r,className:`search-field`,ref:e,isReadOnly:a,...o,css:U(ss,ls,vs),children:e=>V(R,{children:[typeof i==`function`?i(e):i,!a&&B(xt,{slot:`clear`,className:`search-field__clear`,"data-empty":e.isEmpty||void 0,children:B(z,{svg:B(Ht,{})})})]})})}var bs=e(a());function xs(e){let t=(0,Y.c)(5),{onChange:n,debounceMs:r}=e,i;t[0]===n?i=t[1]:(i=e=>{(0,J.startTransition)(()=>{n(e)})},t[0]=n,t[1]=i);let a;return t[2]!==r||t[3]!==i?(a=(0,bs.default)(i,r),t[2]=r,t[3]=i,t[4]=a):a=t[4],a}var Ss=U`
  --search-button-collapsed-size: var(--global-button-height-s);
  // the field's comfortable min-width would stop the input shrinking to the
  // collapsed square, so the floor moves out to this wrapper — the element a
  // tight toolbar actually squeezes — where it can be the collapsed square
  // while collapsed and the field's usual minimum once open. It animates
  // alongside the width so the widths never disagree mid-transition.
  --field-min-width: 0;
  position: relative;
  width: var(--global-dimension-size-3000);
  min-width: var(--global-input-field-min-width);
  transition:
    width 0.2s ease-in-out,
    min-width 0.2s ease-in-out;

  .search-field .search-field__icon {
    transition:
      left 0.2s ease-in-out,
      font-size 0.2s ease-in-out,
      color 0.2s ease-in-out,
      opacity 0.2s ease-in-out;
    // clicks on the icon fall through to the input beneath, so the collapsed
    // square is one hit target
    pointer-events: none;
  }

  // the placeholder fades in slightly after the field starts widening so its
  // text is never seen squeezed into a half-open field
  .search-field .react-aria-Input::placeholder {
    opacity: 1;
    transition: opacity 0.15s ease-in-out 0.1s;
  }

  // The trigger: a transparent hit target laid over the collapsed square. The
  // field beneath paints all of the chrome, so the button carries only the
  // semantics — and its own focus ring, since the field shows no focus
  // treatment while the button is what holds focus. It exists only while the
  // field is collapsed: once the field is open the trigger has no job, and
  // leaving the tab order means Tab moves on from the input rather than onto
  // an invisible button.
  .search-button__trigger {
    display: none;
    position: absolute;
    inset: 0;
    background: none;
    border: none;
    padding: 0;
    cursor: pointer;
    border-radius: var(--global-rounding-small);
    outline: none;

    &[data-focus-visible] {
      outline: var(--focus-ring-thickness) solid var(--focus-ring-color);
      outline-offset: var(--focus-ring-offset);
    }
  }

  // Collapsed and expanded are the same elements throughout — only this
  // attribute changes, so nothing mounts, moves focus, or flashes at the
  // moment of transition.
  &[data-collapsed="true"] {
    width: var(--search-button-collapsed-size);
    min-width: var(--search-button-collapsed-size);

    .search-button__trigger {
      display: block;
    }

    // Each variant only names the tokens; the collapsed square itself is
    // dressed once, below.
    //
    // Quiet: the field chrome is silenced at the token level, leaving an
    // IconButton — dimmed glyph on a bare square, background only on hover.
    &[data-variant="quiet"] {
      --search-button-collapsed-icon-size: var(--global-font-size-l);
      --search-button-collapsed-icon-color: var(--global-text-color-700);
      --search-button-collapsed-icon-opacity: 0.7;
      --field-background-color: transparent;
      --field-border-color: transparent;
      --field-border-color-active: transparent;

      &:hover {
        --field-background-color: var(--hover-background);
      }
    }

    // Default: the field's resting tokens already carry the default Button's
    // border and background, so the square reads as a bordered icon-only
    // Button as it stands. The hover trades the field's border highlight for
    // the Button's background change, and the glyph takes a Button icon's
    // size and color.
    &[data-variant="default"] {
      // Icon renders at 1.2em of the Button font size
      --search-button-collapsed-icon-size: calc(
        var(--global-dimension-font-size-100) * 1.2
      );
      --search-button-collapsed-icon-color: var(--global-text-color-900);
      --field-border-color-active: var(--field-border-color);

      &:hover {
        --field-background-color: var(
          --global-input-field-background-color-hover
        );
      }
    }

    // the expanded side insets would force the border box wider than the square
    --searchfield-input-padding-start: 0;
    --searchfield-input-padding-end: 0;

    .search-field .react-aria-Input {
      cursor: pointer;
      caret-color: transparent;
    }

    .search-field .react-aria-Input::placeholder {
      opacity: 0;
      transition-delay: 0s;
    }

    .search-field .search-field__icon {
      // at rest the glyph takes the variant's button icon size and color,
      // centered in the square, easing into the field's own icon as it expands
      font-size: var(--search-button-collapsed-icon-size);
      color: var(--search-button-collapsed-icon-color);
      opacity: var(--search-button-collapsed-icon-opacity, 1);
      left: calc(
        (var(--search-button-collapsed-size) -
            var(--search-button-collapsed-icon-size)) /
          2
      );
    }

    &:hover .search-field .search-field__icon {
      opacity: 1;
    }
  }

  @media (prefers-reduced-motion: reduce) {
    &,
    .search-field .react-aria-Input,
    .search-field .search-field__icon,
    .search-field .react-aria-Input::placeholder {
      transition: none;
    }
  }
`;function Cs({onChange:e,debounceMs:t=200,placeholder:n,variant:r=`default`,onKeyDown:i,...a}){let o=(0,J.useRef)(null),s=(0,J.useRef)(null),c=(0,J.useRef)(null),[l,u]=(0,J.useState)(!1),[d,f]=(0,J.useState)(()=>!!a.defaultValue),p=!d&&!l,m=xs({onChange:e,debounceMs:t}),h=e=>{f(e!==``),m(e)},g=e=>e!=null&&o.current?.contains(e)===!0;return V(`div`,{className:`search-button`,"data-variant":r,"data-collapsed":p,css:Ss,onFocus:e=>u(g(e.target)),onBlur:e=>{e.relatedTarget==null&&!document.hasFocus()||u(g(e.relatedTarget))},children:[V(ys,{ref:o,size:`S`,onChange:h,onKeyDown:e=>{e.key===`Escape`&&e.target instanceof HTMLInputElement&&e.target.value===``&&((0,dr.flushSync)(()=>u(!1)),c.current?.focus(),e.preventDefault(),e.stopPropagation()),i?.(e)},...a,children:[B(_s,{}),B(Ne,{ref:s,placeholder:n,inert:p})]}),B(xt,{ref:c,className:`search-button__trigger`,"aria-label":a[`aria-label`],"aria-expanded":!p,isDisabled:a.isDisabled,onPress:()=>{(0,dr.flushSync)(()=>u(!0)),s.current?.focus()}})]})}var ws=U`
  display: flex;
  min-width: 0;

  > * {
    position: relative;
    &:focus-within {
      z-index: 1;
    }
  }

  > *:not(:last-child),
  .left-child {
    border-right: none;
    border-top-right-radius: 0;
    border-bottom-right-radius: 0;
  }
  > *:last-child,
  .right-child {
    border-top-left-radius: 0;
    border-bottom-left-radius: 0;
  }
`;function Ts(e){let t=(0,Y.c)(2),n;return t[0]===e.children?n=t[1]:(n=B(`div`,{className:`composite-field`,css:ws,children:e.children}),t[0]=e.children,t[1]=n),n}function Es({ref:e,...t}){let{size:n=`M`,children:r,...i}=t;return B(wt,{size:n,children:B(ue,{"data-size":n,className:`copy-field`,isReadOnly:!0,ref:e,...i,css:U(ss,ls),children:r})})}var Ds=2e3;function Os(e){let t=(0,Y.c)(30),n,r;t[0]===e?(n=t[1],r=t[2]):({ref:r,...n}=e,t[0]=e,t[1]=n,t[2]=r);let i=It(),a,o;t[3]===n?(a=t[4],o=t[5]):({disabled:a,...o}=n,t[3]=n,t[4]=a,t[5]=o);let[s,c]=(0,J.useState)(!1),l=(0,J.useRef)(null),u;t[6]===Symbol.for(`react.memo_cache_sentinel`)?(u=()=>{let e=l.current?.value??``;ze(e),c(!0),setTimeout(()=>{c(!1)},Ds)},t[6]=u):u=t[6];let d=u,f;t[7]===Symbol.for(`react.memo_cache_sentinel`)?(f=U`
        position: relative;
        display: flex;
        align-items: center;
        width: 100%;
        --copy-button-size: calc(
          var(--textfield-input-height) - 2 *
            var(--textfield-vertical-padding) + var(--global-dimension-size-50)
        );

        & > input {
          padding-right: calc(
            var(--textfield-vertical-padding) + var(--copy-button-size) +
              var(--textfield-vertical-padding)
          ) !important;
        }

        .copy-input__copy-button {
          position: absolute;
          right: var(--textfield-vertical-padding);
          background: transparent;
          border: none;
          cursor: pointer;
          padding: 0;
          width: var(--copy-button-size);
          height: var(--copy-button-size);
          color: var(--field-copy-button-text-color);
          display: flex;
          align-items: center;
          justify-content: center;
          border-radius: var(--global-rounding-small);
          transition: background-color 0.2s;
          background-color: var(--field-copy-button-background-color);
          &:hover {
            background-color: var(--field-copy-button-background-color-hover);
          }

          &:focus-visible {
            outline: var(--focus-ring-thickness) solid var(--focus-ring-color);
            outline-offset: var(--focus-ring-offset);
          }

          &[disabled] {
            cursor: not-allowed;
            opacity: 0.5;
          }
        }
      `,t[7]=f):f=t[7];let p;t[8]===r?p=t[9]:(p=e=>{l.current=e,typeof r==`function`?r(e):r&&(r.current=e)},t[8]=r,t[9]=p);let m;t[10]!==a||t[11]!==o||t[12]!==p?(m=B(Ne,{...o,ref:p,type:`text`,readOnly:!0,disabled:a}),t[10]=a,t[11]=o,t[12]=p,t[13]=m):m=t[13];let h=s?`Copied`:`Copy to clipboard`,g=s?`success`:`inherit`,_=s?`Checkmark`:`Duplicate`,v;t[14]!==g||t[15]!==_?(v=B(z,{color:g,svgKey:_}),t[14]=g,t[15]=_,t[16]=v):v=t[16];let y;t[17]!==a||t[18]!==h||t[19]!==v?(y=B(xt,{className:`copy-input__copy-button`,onPress:d,isDisabled:a,"aria-label":h,children:v}),t[17]=a,t[18]=h,t[19]=v,t[20]=y):y=t[20];let b=s?`Copied`:`Copy`,x;t[21]===b?x=t[22]:(x=B(ia,{offset:1,children:b}),t[21]=b,t[22]=x);let S;t[23]!==x||t[24]!==y?(S=V(Se,{children:[y,x]}),t[23]=x,t[24]=y,t[25]=S):S=t[25];let C;return t[26]!==i||t[27]!==S||t[28]!==m?(C=V(`div`,{"data-size":i,"data-testid":`copy-input`,css:f,children:[m,S]}),t[26]=i,t[27]=S,t[28]=m,t[29]=C):C=t[29],C}var ks=(0,J.createContext)(null);function As(){let e=(0,J.useContext)(ks);if(!e)throw Error(`useCredentialContext must be used within a CredentialContext.Provider`);return e}function js({ref:e,...t}){let{size:n=`M`,children:r,...i}=t,[a,o]=(0,J.useState)(!1);return B(ks.Provider,{value:{isVisible:a,setIsVisible:o},children:B(wt,{size:n,children:B(ue,{"data-size":n,className:`credential-field`,autoComplete:`off`,ref:e,...i,css:U(ss,ls),children:r})})})}function Ms(e){let t=(0,Y.c)(28),n,r;t[0]===e?(n=t[1],r=t[2]):({ref:r,...n}=e,t[0]=e,t[1]=n,t[2]=r);let{isVisible:i,setIsVisible:a}=As(),o=It(),s,c,l;t[3]===n?(s=t[4],c=t[5],l=t[6]):({disabled:s,readOnly:l,...c}=n,t[3]=n,t[4]=s,t[5]=c,t[6]=l);let u;t[7]===Symbol.for(`react.memo_cache_sentinel`)?(u=U`
        position: relative;
        display: flex;
        align-items: center;
        width: 100%;
        // The 2px (e.g. 50) is to account making the toggle button to be slightly bigger
        --credential-visibility-toggle-size: calc(
          var(--textfield-input-height) - 2 *
            var(--textfield-vertical-padding) + var(--global-dimension-size-50)
        );

        & > input {
          padding-right: calc(
            var(--textfield-vertical-padding) +
              var(--credential-visibility-toggle-size) +
              var(--textfield-vertical-padding)
          ) !important; // Don't want to fight specificity here
        }

        .credential-input__toggle {
          position: absolute;
          right: var(
            --textfield-vertical-padding
          ); // We want it to be nestled evenly
          background: transparent;
          border: none;
          cursor: pointer;
          padding: 0;
          width: var(--credential-visibility-toggle-size);
          height: var(--credential-visibility-toggle-size);
          color: var(--global-text-color-700);
          display: flex;
          align-items: center;
          justify-content: center;
          border-radius: var(--global-rounding-small);
          transition: background-color 0.2s;
          background-color: var(--global-color-gray-200);
          &:hover {
            background-color: var(--global-color-gray-300);
          }

          &:focus-visible {
            outline: var(--focus-ring-thickness) solid var(--focus-ring-color);
            outline-offset: var(--focus-ring-offset);
          }

          &[disabled] {
            cursor: not-allowed;
            opacity: 0.5;
          }
        }
      `,t[7]=u):u=t[7];let d=i?`text`:`password`,f;t[8]!==s||t[9]!==c||t[10]!==l||t[11]!==r||t[12]!==d?(f=B(Ne,{...c,ref:r,type:d,disabled:s,readOnly:l}),t[8]=s,t[9]=c,t[10]=l,t[11]=r,t[12]=d,t[13]=f):f=t[13];let p;t[14]!==i||t[15]!==a?(p=()=>a(!i),t[14]=i,t[15]=a,t[16]=p):p=t[16];let m=s||l,h=i?`Hide credential`:`Show credential`,g;t[17]===i?g=t[18]:(g=B(z,{svg:B(i?Gt:Qt,{})}),t[17]=i,t[18]=g);let _;t[19]!==p||t[20]!==m||t[21]!==h||t[22]!==g?(_=B(xt,{className:`credential-input__toggle`,onPress:p,isDisabled:m,"aria-label":h,children:g}),t[19]=p,t[20]=m,t[21]=h,t[22]=g,t[23]=_):_=t[23];let v;return t[24]!==o||t[25]!==f||t[26]!==_?(v=V(`div`,{"data-size":o,"data-testid":`credential-input`,css:u,children:[f,_]}),t[24]=o,t[25]=f,t[26]=_,t[27]=v):v=t[27],v}var Ns=``,Ps=`${Ns}REDACTED${Ns}`;function Fs(e){return typeof e==`string`&&e.startsWith(Ps)}function Is(e){let t=e.slice(Ps.length),n=t.indexOf(Ns);return n<0?null:t.slice(0,n)||null}function Ls(e){if(!Fs(e))return null;let t=Is(e);return t?`••••${t}`:`••••••••`}function Rs({label:e,placeholder:t,description:n,value:r,onChange:i,onBlur:a,name:o,isDisabled:s,isRequired:c,errorMessage:l,size:u=`M`}){let[d,f]=(0,J.useState)(!1),p=!d&&Fs(r),m=p?``:r??``,h=p?Ls(r)??`••••••••`:t;return V(gs,{type:`password`,size:u,name:o,value:m,onChange:e=>{d||f(!0),i(e)},onBlur:a,isDisabled:s,isRequired:c,isInvalid:!!l,autoComplete:`off`,children:[B(Sn,{children:e}),B(Ne,{placeholder:h}),l?B(fe,{children:l}):n?B(L,{slot:`description`,children:n}):null]})}var zs=U`
  .react-aria-Input {
    text-align: right;
    font-feature-settings: "tnum" 1;
  }
`;function Bs({ref:e,...t}){let{size:n=`M`,...r}=t;return B(g,{"data-size":n,...r,className:F(`text-field react-aria-NumberField`,t.className),ref:e,css:U(ss,ls,zs)})}function Vs({onChange:e,debounceMs:t=200,placeholder:n,...r}){let i=xs({onChange:e,debounceMs:t});return V(ys,{onChange:i,...r,children:[B(_s,{}),B(Ne,{placeholder:n})]})}var Hs=()=>{let e=(0,Y.c)(1),t;return e[0]===Symbol.for(`react.memo_cache_sentinel`)?(t=B(z,{color:`danger`,className:`field__icon`,svg:B(ct,{})}),e[0]=t):t=e[0],t},Us=()=>{let e=(0,Y.c)(1),t;return e[0]===Symbol.for(`react.memo_cache_sentinel`)?(t=B(z,{color:`success`,className:`field__icon`,svg:B(yn,{})}),e[0]=t):t=e[0],t},Ws=U`
  /* Pin the palette near the top of the viewport instead of centering it so
     the list can grow and shrink without the dialog jumping around */
  &&[data-variant="default"] .react-aria-Dialog {
    top: 15vh;
    transform: translate(-50%, 0);
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }
`,Gs=U`
  display: flex;
  flex-direction: column;
  min-height: 0;

  .command-palette__field {
    display: flex;
    flex-direction: row;
    align-items: center;
    flex: none;
    gap: var(--global-dimension-size-100);
    padding-right: var(--global-dimension-size-100);
    border-bottom: 1px solid var(--global-border-color-default);

    .search-field {
      flex: 1 1 auto;
    }

    .react-aria-Input {
      font-size: var(--global-font-size-m);
      height: var(--global-dimension-size-550);
    }
  }

  .command-palette__menu {
    max-height: 50vh;
    overflow-y: auto;
    /* Fade results in/out as they settle so a new search transition reads as a
       smooth update rather than a hard swap. */
    transition: opacity 0.15s ease;
  }

  .command-palette__menu[data-empty] {
    /* When the menu is empty React Aria collapses it around the empty state;
       stretch it so the empty state can fill the available width instead of
       centering a collapsed box that gets clipped at the top and bottom. */
    align-items: stretch;
    padding: 0;
  }

  &[data-pending="true"] .command-palette__menu {
    /* While a search transition is in flight React keeps the prior results
       mounted (see startTransition in GlobalSearchPalette); dim them slightly
       to signal the refresh without unmounting anything. */
    opacity: 0.5;
  }

  .command-palette__section:not(:first-child) {
    margin-top: var(--global-dimension-size-100);
  }

  .command-palette__section-header {
    padding: var(--global-dimension-size-50) var(--global-dimension-size-100);
    color: var(--global-text-color-500);
    font-size: var(--global-font-size-xs);
    font-weight: 600;
    letter-spacing: 0.06em;
    text-transform: uppercase;
  }

  .command-palette__footer {
    display: flex;
    flex-direction: row;
    align-items: center;
    flex: none;
    gap: var(--global-dimension-size-200);
    padding: var(--global-dimension-size-150) var(--global-dimension-size-200);
    border-top: 1px solid var(--global-border-color-default);
  }

  .command-palette__hint {
    display: inline-flex;
    align-items: center;
    gap: var(--global-dimension-size-100);
  }

  .command-palette__empty-state {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
    min-height: var(--global-dimension-size-1600);
    box-sizing: border-box;
  }
`;function Ks({isOpen:e,onOpenChange:t,inputValue:n,onInputChange:r,filter:i,placeholder:a=`Search…`,"aria-label":o=`Command palette`,onAction:s,children:c,renderEmptyState:l,footer:u,isPending:d}){return B(On,{isOpen:e,onOpenChange:t,isDismissable:!0,children:B(Pn,{size:`M`,css:Ws,children:B(xn,{"aria-label":o,className:`command-palette`,css:Gs,"data-pending":d?`true`:void 0,children:V(At,{inputValue:n,onInputChange:r,filter:i,children:[B(`div`,{className:`command-palette__field`,children:V(ys,{"aria-label":o,variant:`quiet`,size:`L`,autoFocus:!0,children:[B(_s,{}),B(Ne,{placeholder:a})]})}),B(Na,{className:`command-palette__menu`,"aria-label":o,onAction:s,renderEmptyState:()=>B(`div`,{className:`command-palette__empty-state`,children:l?l():B(_o,{icon:B(z,{svg:B(ft,{})}),description:`No results`})}),children:c}),B(`div`,{className:`command-palette__footer`,children:u??B(qs,{})})]})})})})}function qs(){let e=(0,Y.c)(3),t;e[0]===Symbol.for(`react.memo_cache_sentinel`)?(t=V(`span`,{className:`command-palette__hint`,children:[B(lo,{children:`↑↓`}),B(L,{size:`XS`,color:`text-500`,children:`to navigate`})]}),e[0]=t):t=e[0];let n;e[1]===Symbol.for(`react.memo_cache_sentinel`)?(n=V(`span`,{className:`command-palette__hint`,children:[B(lo,{children:`↵`}),B(L,{size:`XS`,color:`text-500`,children:`to select`})]}),e[1]=n):n=e[1];let r;return e[2]===Symbol.for(`react.memo_cache_sentinel`)?(r=V(R,{children:[t,n,V(`span`,{className:`command-palette__hint`,children:[B(lo,{children:`esc`}),B(L,{size:`XS`,color:`text-500`,children:`to close`})]})]}),e[2]=r):r=e[2],r}function Js(e){let t=(0,Y.c)(5),{title:n,children:r}=e,i;t[0]===n?i=t[1]:(i=B(Ot,{className:`command-palette__section-header`,children:n}),t[0]=n,t[1]=i);let a;return t[2]!==r||t[3]!==i?(a=V(tn,{className:`command-palette__section`,children:[i,r]}),t[2]=r,t[3]=i,t[4]=a):a=t[4],a}var Ys=U`
  .command-palette-item__layout {
    display: flex;
    flex-direction: row;
    align-items: center;
    gap: var(--global-dimension-size-100);
    min-width: 0;
    flex: 1 1 auto;
  }

  .command-palette-item__icon {
    display: flex;
    align-items: center;
    flex: none;
    color: var(--global-text-color-700);
    font-size: var(--global-font-size-m);
  }

  .command-palette-item__label {
    flex: none;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    max-width: 60%;
  }

  .command-palette-item__description {
    flex: 1 1 auto;
    min-width: 0;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    color: var(--global-text-color-500);
    font-size: var(--global-font-size-s);
  }
`;function Xs(e){let t=(0,Y.c)(18),n,r,i,a;t[0]===e?(n=t[1],r=t[2],i=t[3],a=t[4]):({icon:i,description:r,children:n,...a}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a);let o;t[5]===i?o=t[6]:(o=i&&B(`span`,{className:`command-palette-item__icon`,children:i}),t[5]=i,t[6]=o);let s;t[7]===n?s=t[8]:(s=B(`span`,{className:`command-palette-item__label`,children:n}),t[7]=n,t[8]=s);let c;t[9]===r?c=t[10]:(c=r&&B(`span`,{className:`command-palette-item__description`,children:r}),t[9]=r,t[10]=c);let l;t[11]!==o||t[12]!==s||t[13]!==c?(l=V(`div`,{className:`command-palette-item__layout`,children:[o,s,c]}),t[11]=o,t[12]=s,t[13]=c,t[14]=l):l=t[14];let u;return t[15]!==a||t[16]!==l?(u=B(Fa,{...a,className:`command-palette-item`,css:Ys,children:l}),t[15]=a,t[16]=l,t[17]=u):u=t[17],u}var Zs=U`
  background-color: rgba(var(--global-color-blue-500-rgb), 0.4);
  color: inherit;
  border-radius: var(--global-rounding-xsmall);
`;function Qs(e){let t=(0,Y.c)(26),{text:n,match:r}=e,i;t[0]===r?i=t[1]:(i=r?.trim().length??0,t[0]=r,t[1]=i);let a=i;if(!r||a===0){let e;return t[2]===n?e=t[3]:(e=B(R,{children:n}),t[2]=n,t[3]=e),e}let o,s,c,l,u,d;if(t[4]!==r||t[5]!==a||t[6]!==n){d=Symbol.for(`react.early_return_sentinel`);bb0:{let e=n.toLowerCase().indexOf(r.trim().toLowerCase());if(e===-1){let e;t[13]===n?e=t[14]:(e=B(R,{children:n}),t[13]=n,t[14]=e),d=e;break bb0}o=e+a,u=n.slice(0,e),s=`match-text`,c=Zs,l=n.slice(e,o)}t[4]=r,t[5]=a,t[6]=n,t[7]=o,t[8]=s,t[9]=c,t[10]=l,t[11]=u,t[12]=d}else o=t[7],s=t[8],c=t[9],l=t[10],u=t[11],d=t[12];if(d!==Symbol.for(`react.early_return_sentinel`))return d;let f;t[15]!==s||t[16]!==c||t[17]!==l?(f=B(`mark`,{className:s,css:c,children:l}),t[15]=s,t[16]=c,t[17]=l,t[18]=f):f=t[18];let p;t[19]!==o||t[20]!==n?(p=n.slice(o),t[19]=o,t[20]=n,t[21]=p):p=t[21];let m;return t[22]!==u||t[23]!==f||t[24]!==p?(m=V(R,{children:[u,f,p]}),t[22]=u,t[23]=f,t[24]=p,t[25]=m):m=t[25],m}U`
  border: 1px solid var(--global-border-color-default);
  forced-color-adjust: none;
  border-radius: var(--global-rounding-small);
  padding: var(--global-dimension-size-50) var(--global-dimension-size-100);
  font-size: var(--global-font-size-s);
  color: var(--global-text-color-900);
  outline: none;
  cursor: default;
  display: flex;
  align-items: center;
  transition: all 200ms;

  &[data-hovered] {
    border-color: var(--global-color-primary);
  }

  &[data-focus-visible] {
    outline: var(--focus-ring-thickness) solid var(--focus-ring-color);
    outline-offset: var(--focus-ring-offset);
  }

  &[data-selected] {
    border-color: var(--global-color-primary);
    background: var(--global-color-primary-700);
  }
`,U`
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: var(--global-dimension-size-50);
  height: 28px;
`;var $s=U(`
  // fixes esoteric overflow bug with VisuallyHidden, which is used by Radio
  // If position is not set to relative, the radio group will explode the parent layout
  // This will impact any other react aria component that uses VisuallyHidden
  // https://github.com/adobe/react-spectrum/issues/5094
  position: relative;
  display: flex;
  flex-direction: row;
  align-items: center;
  width: fit-content;
  gap: var(--global-dimension-size-200);
  font-size: var(--global-dimension-font-size-100);

  & > .radio:not(:first-of-type) {
    border-left: none;
  }

  & > .radio:first-of-type {
    border-radius: var(--global-rounding-small) 0 0 var(--global-rounding-small);
  }

  & > .radio:last-of-type {
    border-radius: 0 var(--global-rounding-small) var(--global-rounding-small) 0;
  }

  &[data-direction="row"] {
    flex-direction: row;
    flex-wrap: wrap;

    .react-aria-Label {
      flex-basis: 100%;
    }

    [slot="description"] {
      flex-basis: 100%;
    }
  }

  &[data-direction="column"] {
    flex-direction: column;
    align-items: flex-start;
  }

  &[data-size="S"] {
    .radio {
      padding: var(--global-dimension-size-25) var(--global-dimension-size-100);
    }
  }

  &[data-size="L"] {
    .radio {
      padding: var(--global-dimension-size-100) var(--global-dimension-size-150);
    }
  }

  &[data-disabled] {
    opacity: 0.5;
  }

  &[data-readonly] {
    .radio:before {
      opacity: 0.5;
    }
  }

  &:has(.radio[data-focus-visible]) {
    border-radius: var(--global-rounding-small);
    outline: var(--focus-ring-thickness) solid var(--focus-ring-color);
    // display an outline offset around the radio group, accounting for the outline offset of the inner radios
    outline-offset: var(--global-dimension-size-100);
  }
`),ec=({size:e,css:t,className:n,direction:r=`row`,...i})=>B(s,{"data-size":e,"data-direction":r,className:F(`radio-group`,n),css:U(ss,$s,t),...i}),tc=U(`
  display: flex;
  align-items: center;
  gap: var(--global-dimension-size-50);
  font-size: 14px;
  color: var(--global-text-color-900);
  forced-color-adjust: none;

  &:before {
    content: '';
    display: block;
    width: 1.286rem;
    height: 1.286rem;
    box-sizing: border-box;
    border: 0.143rem solid var(--global-input-field-border-color);
    background: var(--global-input-field-background-color);
    border-radius: 1.286rem;
    transition: all 200ms;
  }

  &[data-pressed]:before {
    border-color: var(--global-input-field-border-color-active);
  }

  &[data-selected] {
    &:before {
      border-color: var(--global-button-primary-background-color);
      border-width: 0.429rem;
    }

    &[data-pressed]:before {
      border-color: var(--global-button-primary-background-color-active);
    }
  }

  &[data-focus-visible]:before {
    outline: var(--focus-ring-thickness) solid var(--focus-ring-color);
    outline-offset: var(--focus-ring-offset);
  }

  &[data-disabled] {
    opacity: var(--global-opacity-disabled);
  }
`),nc=e=>{let t=(0,Y.c)(12),n,r,i;t[0]===e?(n=t[1],r=t[2],i=t[3]):({className:n,css:r,...i}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i);let a;t[4]===n?a=t[5]:(a=F(`radio`,n),t[4]=n,t[5]=a);let s;t[6]===r?s=t[7]:(s=U(tc,r),t[6]=r,t[7]=s);let c;return t[8]!==i||t[9]!==a||t[10]!==s?(c=B(o,{className:a,css:s,...i}),t[8]=i,t[9]=a,t[10]=s,t[11]=c):c=t[11],c},rc=U(lt,`
    text-wrap: nowrap;
    &[data-selected="true"] {
      background-color: var(--global-button-primary-background-color);
      --button-border-color: var(--global-button-primary-border-color);
      color: var(--global-button-primary-foreground-color);
      &:hover:not([data-disabled]) {
        background-color: var(--global-button-primary-background-color-hover);
      }
    }
    &[data-hovered]:not([data-disabled]):not([data-selected="true"]) {
      background-color: var(--global-input-field-border-color-hover);
    }
    &[data-focus-visible] {
      outline: var(--focus-ring-thickness) solid var(--focus-ring-color);
      outline-offset: calc(-1 * var(--focus-ring-thickness));
    }
    &[data-selected="true"][data-focus-visible] {
      outline-color: var(--global-button-primary-foreground-color);
    }
`),ic=e=>{let t=(0,Y.c)(25),n,r,i;t[0]===e?(n=t[1],r=t[2],i=t[3]):({className:n,css:r,...i}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i);let a,o,s,c,l;t[4]===i?(a=t[5],o=t[6],s=t[7],c=t[8],l=t[9]):({leadingVisual:o,trailingVisual:l,size:s,children:a,...c}=i,t[4]=i,t[5]=a,t[6]=o,t[7]=s,t[8]=c,t[9]=l);let u=It(),d=s??u,f;t[10]!==a||t[11]!==o||t[12]!==l?(f=e=>V(R,{children:[o,typeof a==`function`?a(e):a,l]}),t[10]=a,t[11]=o,t[12]=l,t[13]=f):f=t[13];let p=f,m;t[14]===r?m=t[15]:(m=U(rc,r),t[14]=r,t[15]=m);let h=!a,g;t[16]===n?g=t[17]:(g=F(`toggle-button`,n),t[16]=n,t[17]=g);let _;return t[18]!==p||t[19]!==c||t[20]!==d||t[21]!==m||t[22]!==h||t[23]!==g?(_=B(N,{css:m,"data-size":d,"data-childless":h,className:g,...c,children:p}),t[18]=p,t[19]=c,t[20]=d,t[21]=m,t[22]=h,t[23]=g,t[24]=_):_=t[24],_},ac=U(`
  position: relative;
  display: flex;
  flex-direction: row;
  align-items: center;
  width: fit-content;
  & > button {
    border-radius: 0;
  }

  & > .toggle-button:not(:first-of-type):not([data-selected="true"]) {
    border-left: none;
  }
    
  & > .toggle-button[data-selected="true"]:not(:first-of-type) {
    margin-left: -1px;
  }

  & > .toggle-button:first-of-type {
    border-radius: var(--global-rounding-small) 0 0 var(--global-rounding-small);
  }

  & > .toggle-button:last-of-type {
    border-radius: 0 var(--global-rounding-small) var(--global-rounding-small) 0;
  }

  &:has(.toggle-button[data-focus-visible]) {
    border-radius: var(--global-rounding-small);
    outline: var(--focus-ring-thickness) solid var(--focus-ring-color);
    outline-offset: var(--focus-ring-offset);
  }
`),oc=({size:e=`M`,css:t,className:n,selectionMode:r=`single`,...i})=>B(wt,{size:e,children:B(ge,{"data-size":e,className:F(`toggle-button-group`,n),css:U(ac,t),selectionMode:r,...i})}),sc=U`
  --segmented-control-rounding: var(--global-rounding-small);
  /* Concentric with the track, since segments span its full height. */
  --segmented-control-item-rounding: calc(
    var(--segmented-control-rounding) - var(--global-border-size-thin)
  );
  /* One clock for every moving part; mixed durations read as stutter. */
  --segmented-control-motion-duration: 200ms;
  --segmented-control-motion-easing: cubic-bezier(0, 0, 0.4, 1);

  position: relative;
  box-sizing: border-box;
  display: inline-flex;
  /* A definite width opts out of a flex parent's align-items: stretch, which
     would widen the track without widening the segments. */
  width: fit-content;
  max-width: 100%;
  background-color: var(--global-segmented-control-background-color);
  border: var(--global-border-size-thin) solid
    var(--global-segmented-control-border-color);
  border-radius: var(--segmented-control-rounding);

  /* Labels hold at 14px through M to match Button and Select in a toolbar. */
  &[data-size="S"] {
    height: var(--global-button-height-s);
    --segmented-control-item-padding-x: var(--global-dimension-size-100);
    --segmented-control-item-font-size: var(--global-font-size-s);
    --segmented-control-item-line-height: var(--global-line-height-s);
  }

  &[data-size="M"] {
    height: var(--global-button-height-m);
    --segmented-control-item-padding-x: var(--global-dimension-size-150);
    --segmented-control-item-font-size: var(--global-font-size-s);
    --segmented-control-item-line-height: var(--global-line-height-s);
  }

  &[data-size="L"] {
    height: var(--global-button-height-l);
    --segmented-control-item-padding-x: var(--global-dimension-size-200);
    --segmented-control-item-font-size: var(--global-font-size-m);
    --segmented-control-item-line-height: var(--global-line-height-m);
  }

  &[data-justified="true"] {
    width: 100%;

    .segmented-control__item {
      flex: 1 1 0;
    }
  }

  /* Keyed on the BEM class, not the item's emotion class, so an item given its
     own css prop still divides from its neighbors. */
  .segmented-control__item + .segmented-control__item::before {
    content: "";
    position: absolute;
    left: calc(-1 * var(--global-border-size-thin) / 2);
    top: 25%;
    height: 50%;
    width: var(--global-border-size-thin);
    background-color: var(--global-segmented-control-divider-color);
    transition: opacity var(--segmented-control-motion-duration)
      var(--segmented-control-motion-easing);

    @media (prefers-reduced-motion: reduce) {
      transition: none;
    }
  }

  /* Beside the thumb, the thumb's own edge does the separating. */
  .segmented-control__item[data-selected]::before,
  .segmented-control__item[data-selected] + .segmented-control__item::before {
    opacity: 0;
  }
`,cc=U`
  position: relative;
  /* The thumb is a child of the selected item and slides in from the previous
     one, so the selected item drops below its siblings (see [data-selected]) to
     keep the thumb from crossing over the labels it passes. */
  z-index: 1;
  box-sizing: border-box;
  display: flex;
  /* Shrinkable, so an oversized control truncates labels rather than spilling
     segments outside the track. */
  flex: 0 1 auto;
  align-items: center;
  justify-content: center;
  min-width: 0;
  margin: 0;
  padding: 0 var(--segmented-control-item-padding-x);
  border: none;
  background-color: transparent;
  border-radius: var(--segmented-control-item-rounding);
  color: var(--global-segmented-control-item-text-color);
  font-family: inherit;
  font-size: var(--segmented-control-item-font-size);
  line-height: var(--segmented-control-item-line-height);
  font-weight: 400;
  white-space: nowrap;
  /* Not clipped: the thumb spends the animation outside this box. */
  overflow: visible;
  cursor: pointer;
  user-select: none;
  -webkit-tap-highlight-color: transparent;
  forced-color-adjust: none;
  outline: none;
  transition: color var(--segmented-control-motion-duration)
    var(--segmented-control-motion-easing);

  /* Every reduced-motion override sits with the transition it cancels: one
     block on the track would tie on specificity and lose on source order. */
  @media (prefers-reduced-motion: reduce) {
    transition: none;
  }

  /* Hover pill, inset so it reads as clickable without competing with the
     thumb. */
  &::after {
    content: "";
    position: absolute;
    inset: var(--global-dimension-size-50);
    border-radius: var(--segmented-control-item-rounding);
    background-color: transparent;
    transition: background-color var(--segmented-control-motion-duration)
      var(--segmented-control-motion-easing);
    z-index: -1;

    @media (prefers-reduced-motion: reduce) {
      transition: none;
    }
  }

  /* Matching on data-size outranks Text's own font rules instead of tying with
     them and depending on insertion order. */
  .text[data-size] {
    color: inherit;
    font-size: inherit;
    line-height: inherit;
  }

  &[data-hovered]:not([data-selected]):not([data-disabled]) {
    color: var(--global-segmented-control-item-text-color-hover);

    &::after {
      background-color: var(
        --global-segmented-control-item-background-color-hover
      );
    }
  }

  &[data-selected] {
    color: var(--global-segmented-control-item-text-color-selected);
    z-index: 0;
  }

  &[data-disabled] {
    cursor: default;
    color: var(--global-segmented-control-item-text-color-disabled);
  }

  &[data-focus-visible] {
    outline: var(--focus-ring-thickness) solid var(--focus-ring-color);
    outline-offset: calc(-1 * var(--focus-ring-thickness));
  }
`,lc=U`
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--global-dimension-size-100);
  min-width: 0;
  /* Here rather than on the item, so clipping the label never clips the thumb. */
  overflow: hidden;
  transition: scale var(--segmented-control-motion-duration)
    var(--segmented-control-motion-easing);

  @media (prefers-reduced-motion: reduce) {
    transition: none;
  }

  .text {
    overflow: hidden;
    text-overflow: ellipsis;
  }

  [data-pressed] > & {
    scale: 0.96;
  }
`,uc=U`
  position: absolute;
  /* Bleeds out by the track's border width so the two borders paint on top of
     each other instead of reading as a doubled line. */
  top: calc(-1 * var(--global-border-size-thin));
  left: calc(-1 * var(--global-border-size-thin));
  width: calc(100% + 2 * var(--global-border-size-thin));
  height: calc(100% + 2 * var(--global-border-size-thin));
  box-sizing: border-box;
  z-index: -1;
  contain: strict;
  /* Zero, but written as a percentage on purpose: a box-size-dependent translate
     can't be lifted to the compositor, so it stays on the main thread and
     resolves in the same style recalc as the width stretch. Left compositable,
     it keeps gliding through dropped frames while width stalls, and the thumb
     visibly wobbles. */
  translate: 0% 0px;
  background-color: var(--global-segmented-control-thumb-background-color);
  border: var(--global-border-size-thin) solid
    var(--global-segmented-control-thumb-border-color);
  border-radius: var(--segmented-control-rounding);
  transition-property: translate, width;
  transition-duration: var(--segmented-control-motion-duration);
  transition-timing-function: var(--segmented-control-motion-easing);

  /* none, not a zero duration: react-aria only snapshots the outgoing thumb when
     the incoming one has a transition-property. */
  @media (prefers-reduced-motion: reduce) {
    transition: none;
  }
`;function dc(e){for(let t of J.Children.toArray(e)){if(!(0,J.isValidElement)(t))continue;if(t.type===J.Fragment){let e=dc(t.props.children);if(e!=null)return e;continue}let{id:e,isDisabled:n}=t.props;if(e!=null&&!n)return e}}function fc({children:e,size:t=`M`,isJustified:n=!1,selectedKey:r,defaultSelectedKey:i,onSelectionChange:a,className:o,css:s,...c}){let[l]=(0,J.useState)(()=>i??dc(e));return B(ge,{...c,selectionMode:`single`,disallowEmptySelection:!0,orientation:`horizontal`,selectedKeys:r===void 0?void 0:[r],defaultSelectedKeys:l==null?void 0:[l],onSelectionChange:e=>{let[t]=e;t!=null&&a?.(t)},"data-size":t,"data-justified":n,className:F(`segmented-control`,o),css:U(sc,s),children:e})}function pc(e){let t=(0,Y.c)(4),{isSelected:n}=e,r=(0,J.useRef)(null),i,a;t[0]===n?(i=t[1],a=t[2]):(i=()=>{let e=r.current,t=e?.style.translate;e&&n&&t&&(e.style.translate=`${t.split(` `)[0]} 0px`)},a=[n],t[0]=n,t[1]=i,t[2]=a),(0,J.useLayoutEffect)(i,a);let o;return t[3]===Symbol.for(`react.memo_cache_sentinel`)?(o=B(En,{ref:r,className:`segmented-control__thumb`,css:uc}),t[3]=o):o=t[3],o}function mc(e){let t=(0,Y.c)(16),n,r,i,a;t[0]===e?(n=t[1],r=t[2],i=t[3],a=t[4]):({children:n,className:r,css:i,...a}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a);let o;t[5]===r?o=t[6]:(o=F(`segmented-control__item`,r),t[5]=r,t[6]=o);let s;t[7]===i?s=t[8]:(s=U(cc,i),t[7]=i,t[8]=s);let c;t[9]===n?c=t[10]:(c=e=>{let{isSelected:t}=e;return V(R,{children:[B(`div`,{className:`segmented-control__item-content`,css:lc,children:typeof n==`string`?B(L,{children:n}):n}),B(pc,{isSelected:t})]})},t[9]=n,t[10]=c);let l;return t[11]!==a||t[12]!==o||t[13]!==s||t[14]!==c?(l=B(N,{...a,className:o,css:s,children:c}),t[11]=a,t[12]=o,t[13]=s,t[14]=c,t[15]=l):l=t[15],l}var hc=U`
  display: flex;
  flex-direction: column;
  max-height: inherit;
  overflow: auto;
  forced-color-adjust: none;
  outline: none;
  box-sizing: border-box;

  &[data-focus-visible] {
    outline: var(--focus-ring-thickness) solid var(--focus-ring-color);
    outline-offset: -1px;
  }

  &[data-empty] {
    align-items: center;
    justify-content: center;
    font-style: italic;
    color: var(--global-text-color-700);
  }

  .react-aria-ListBoxItem {
    margin: var(--global-dimension-size-25);
    padding: var(--global-dimension-size-100) var(--global-dimension-size-150);
    border-radius: var(--global-rounding-small);
    outline: none;
    cursor: default;
    color: var(--global-text-color-900);
    font-size: var(--global-font-size-s);
    line-height: var(--global-line-height-s);

    position: relative;
    display: flex;
    flex-direction: column;

    &[data-focus-visible] {
      outline: var(--focus-ring-thickness) solid var(--focus-ring-color);
      outline-offset: -2px;
    }

    &[data-selected] {
      background: var(--highlight-background);
      color: var(--highlight-foreground);

      &[data-focus-visible] {
        outline-color: var(--highlight-foreground);
        outline-offset: -4px;
      }
    }
    &[data-hovered],
    &[data-active] {
      background: var(--global-menu-item-background-color-hover);
    }
  }
`;function gc(e){let t=(0,Y.c)(10),n,r,i;t[0]===e?(n=t[1],r=t[2],i=t[3]):({css:n,ref:r,...i}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i);let a;t[4]===n?a=t[5]:(a=U(hc,n),t[4]=n,t[5]=a);let o=a,s;return t[6]!==o||t[7]!==r||t[8]!==i?(s=B(p,{css:o,ref:r,...i}),t[6]=o,t[7]=r,t[8]=i,t[9]=s):s=t[9],s}var _c=U`
  --selected-color: var(--global-checkbox-selected-color);
  --selected-color-pressed: var(--global-checkbox-selected-color-pressed);
  --checkmark-color: var(--global-checkbox-checkmark-color);
  --border-color: var(--global-checkbox-border-color);
  --border-color-pressed: var(--global-checkbox-border-color-pressed);
  --border-color-hover: var(--global-checkbox-border-color-hover);
  --checkbox-focus-ring-color: var(--focus-ring-color);
  --checkbox-size: var(--global-dimension-size-200);

  display: flex;
  /* This is needed so the HiddenInput is positioned correctly */
  position: relative;
  align-items: center;
  gap: var(--global-dimension-size-100);
  forced-color-adjust: none;
  cursor: pointer;

  .checkbox {
    box-sizing: border-box;
    width: var(--checkbox-size);
    height: var(--checkbox-size);
    border: 2px solid var(--border-color);
    border-radius: var(--global-rounding-small);
    transition:
      background-color 200ms,
      border-color 200ms;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
  }

  .checkbox svg {
    width: 1rem;
    height: 1rem;
    fill: none;
    stroke: var(--checkmark-color);
    stroke-width: 3px;
    stroke-dasharray: 22px;
    stroke-dashoffset: 66;
    transition: all 200ms;
  }

  &[data-pressed] .checkbox {
    border-color: var(--border-color-pressed);
  }

  &[data-force-hovered],
  &[data-hovered] {
    .checkbox {
      border-color: var(--border-color-hover);
    }
  }

  &[data-focus-visible] .checkbox {
    outline: var(--focus-ring-thickness) solid var(--checkbox-focus-ring-color);
    outline-offset: var(--focus-ring-offset);
  }

  &[data-selected],
  &[data-indeterminate] {
    .checkbox {
      border-color: var(--selected-color);
      background: var(--selected-color);
    }

    &[data-pressed] .checkbox {
      border-color: var(--selected-color-pressed);
      background: var(--selected-color-pressed);
    }

    .checkbox svg {
      stroke-dashoffset: 44;
    }
  }

  &[data-indeterminate] {
    & .checkbox svg {
      stroke: none;
      fill: var(--checkmark-color);
    }
  }

  &[data-disabled] {
    cursor: not-allowed;
    opacity: 0.5;
  }
`;function vc(e){let t=(0,Y.c)(14),n,r;t[0]===e?(n=t[1],r=t[2]):({ref:r,...n}=e,t[0]=e,t[1]=n,t[2]=r);let i,a,o;t[3]===n?(i=t[4],a=t[5],o=t[6]):({children:i,isHovered:a,...o}=n,t[3]=n,t[4]=i,t[5]=a,t[6]=o);let s=a||void 0,c;t[7]===i?c=t[8]:(c=e=>{let{isIndeterminate:t}=e;return V(R,{children:[B(`div`,{className:`checkbox`,children:B(`svg`,{viewBox:`0 0 18 18`,"aria-hidden":`true`,children:t?B(`rect`,{x:1,y:7.5,width:15,height:3}):B(`polyline`,{points:`1 9 7 14 15 4`})})}),i]})},t[7]=i,t[8]=c);let l;return t[9]!==r||t[10]!==o||t[11]!==s||t[12]!==c?(l=B(xe,{...o,ref:r,css:_c,"data-force-hovered":s,children:c}),t[9]=r,t[10]=o,t[11]=s,t[12]=c,t[13]=l):l=t[13],l}var yc=U`
  --menu-min-width: 250px;
  min-width: var(--menu-min-width);
  display: flex;
  flex-direction: column;
  gap: var(--global-menu-item-gap);
  flex: 1 1 auto;
  overflow-y: auto;
  overflow-x: hidden;
  padding: var(--global-menu-item-gap);
  &:focus-visible {
    border-radius: var(--global-rounding-small);
    outline: var(--focus-ring-thickness) solid var(--focus-ring-color);
    outline-offset: 0px;
  }
  &[data-empty] {
    align-items: center;
    justify-content: center;
    display: flex;
    padding: var(--global-dimension-size-100);
  }

  .react-aria-GridListSection {
    display: flex;
    flex-direction: column;
    gap: var(--global-menu-item-gap);
  }
`,bc=U`
  border-radius: var(--global-rounding-small);
  outline: none;
  cursor: default;
  color: var(--global-text-color-900);
  position: relative;
  display: flex;
  gap: var(--global-menu-item-gap);
  align-items: center;
  justify-content: space-between;

  &[data-disabled] {
    cursor: not-allowed;
    color: var(--global-color-text-300);
    opacity: var(--global-opacity-disabled);
  }

  &[data-focus-visible] {
    outline: none;
  }

  @media (forced-colors: active) {
    &[data-focused] {
      forced-color-adjust: none;
      background: Highlight;
      color: HighlightText;
    }
  }

  &[data-focus-visible] {
    .GridListItem__content {
      background-color: var(--global-menu-item-background-color-hover);
    }
  }

  .GridListItem__content {
    padding: var(--global-menu-item-gap);
    padding-left: var(--global-dimension-size-100);
    border-radius: var(--global-rounding-small);

    &:hover {
      background-color: var(--global-menu-item-background-color-hover);
    }
  }
`,xc=U`
  padding: var(--global-dimension-size-50) var(--global-dimension-size-100) 0;
`;U`
  display: flex;
  flex-direction: column;
  gap: var(--global-menu-item-gap);
`;function Sc(e){let t=(0,Y.c)(6),n,i;t[0]===e?(n=t[1],i=t[2]):({ref:n,...i}=e,t[0]=e,t[1]=n,t[2]=i);let a;return t[3]!==n||t[4]!==i?(a=B(r,{css:yc,ref:n,...i}),t[3]=n,t[4]=i,t[5]=a):a=t[5],a}function Cc(e){let t=(0,Y.c)(14),n,r,i,a,o;t[0]===e?(n=t[1],r=t[2],i=t[3],a=t[4],o=t[5]):({ref:r,children:n,subtitle:a,trailingContent:o,...i}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a,t[5]=o);let s;t[6]!==n||t[7]!==a||t[8]!==o?(s=e=>{let{selectionMode:t,selectionBehavior:r}=e;return V(R,{children:[B(wc,{subtitle:a,selectionMode:t,selectionBehavior:r,children:n}),o]})},t[6]=n,t[7]=a,t[8]=o,t[9]=s):s=t[9];let c;return t[10]!==r||t[11]!==i||t[12]!==s?(c=B(me,{css:bc,ref:r,...i,children:s}),t[10]=r,t[11]=i,t[12]=s,t[13]=c):c=t[13],c}var wc=e=>{let t=(0,Y.c)(14),{children:n,subtitle:r,selectionMode:i,selectionBehavior:a}=e,[o,s]=(0,J.useState)(!1),c,l,u;t[0]===Symbol.for(`react.memo_cache_sentinel`)?(c=()=>s(!0),l=()=>s(!1),u=U`
        flex: 1;
        min-width: 0;
      `,t[0]=c,t[1]=l,t[2]=u):(c=t[0],l=t[1],u=t[2]);let d;t[3]!==o||t[4]!==a||t[5]!==i?(d=i===`multiple`&&a===`toggle`&&B(vc,{slot:`selection`,isHovered:o}),t[3]=o,t[4]=a,t[5]=i,t[6]=d):d=t[6];let f;t[7]===Symbol.for(`react.memo_cache_sentinel`)?(f=U`
            padding: var(--global-menu-item-gap);
          `,t[7]=f):f=t[7];let p;t[8]!==n||t[9]!==r?(p=V(W,{direction:`column`,gap:`var(--global-dimension-size-25)`,minWidth:0,flex:1,css:f,children:[n,r]}),t[8]=n,t[9]=r,t[10]=p):p=t[10];let m;return t[11]!==d||t[12]!==p?(m=B(`div`,{onMouseEnter:c,onMouseLeave:l,css:u,children:V(W,{direction:`row`,alignItems:`center`,gap:`size-100`,className:`GridListItem__content`,children:[d,p]})}),t[11]=d,t[12]=p,t[13]=m):m=t[13],m},Tc=e=>{let t=(0,Y.c)(2),{title:n}=e,r;return t[0]===n?r=t[1]:(r=B(he,{css:xc,children:B(L,{weight:`heavy`,children:n})}),t[0]=n,t[1]=r),r},Ec=U`
  --token-max-width: var(--global-dimension-size-2000);
  box-sizing: border-box;
  display: inline-flex;
  align-items: center;
  /* Keep the trailing gap (text → remove button) as tight as the leading
     visual's margin so the pill reads as one unit. */
  gap: var(--global-dimension-size-50);
  font-size: var(--global-dimension-font-size-75);
  line-height: var(--global-line-height-s);
  padding: 0 var(--global-dimension-size-100);
  border-radius: var(--global-rounding-large);
  border: 1px solid transparent;
  user-select: none;
  max-width: var(--token-max-width);

  .token__text {
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  &[data-size="S"] {
    height: var(--global-dimension-size-200);
  }

  &[data-size="M"] {
    height: var(--global-dimension-size-250);
  }

  &[data-size="L"] {
    height: var(--global-dimension-size-300);
    /* The large token scales its typography up to body size so token-heavy
       detail views stay readable; S and M keep the compact font. */
    font-size: var(--global-dimension-font-size-100);
  }

  /* Center the leading visual and the remove button inside the pill's
     rounded end caps. A cap is a semicircle of radius height/2, so the 16px
     visual/icon box lands centered when the side inset is
     capRadius - 1px border - 8px (half the box). */
  &[data-size="M"][data-leading-visual] {
    padding-left: 1px;
  }

  &[data-size="L"][data-leading-visual] {
    padding-left: calc(var(--global-dimension-size-50) - 1px);
  }

  &[data-size="S"][data-removable] {
    padding-right: var(--global-dimension-size-25);
  }

  &[data-size="M"][data-removable] {
    padding-right: 1px;
  }

  &[data-size="L"][data-removable] {
    padding-right: calc(var(--global-dimension-size-50) - 1px);
  }

  &[data-disabled] {
    opacity: 0.5;
    cursor: not-allowed;
  }

  &[data-theme="light"] {
    background: lch(from var(--internal-token-color) 96 calc(c * 0.3) h);
    border-color: lch(from var(--internal-token-color) 88 calc(c * 0.4) h);
    color: lch(from var(--internal-token-color) 45 c h);
  }

  &[data-theme="dark"] {
    background: lch(from var(--internal-token-color) 18 calc(c * 0.2) h);
    border-color: lch(from var(--internal-token-color) 28 calc(c * 0.3) h);
    color: lch(from var(--internal-token-color) 90 calc(c * 0.8) h);
  }

  &[data-interactive]:not([data-disabled]) {
    cursor: pointer;

    > button {
      &:focus-visible {
        outline: var(--focus-ring-thickness) solid var(--focus-ring-color);
        border-radius: var(--global-rounding-small);
      }
    }
  }

  > button {
    all: unset;
    cursor: pointer;
    display: flex;
    align-items: center;
    min-width: 0;
    overflow: hidden;

    &[disabled] {
      cursor: not-allowed;
    }
  }
`;function Dc(e){let t=(0,Y.c)(3),{children:n}=e,r;t[0]===Symbol.for(`react.memo_cache_sentinel`)?(r=U`
        display: flex;
        align-items: center;
        justify-content: center;
        width: var(--global-dimension-size-200);
        height: var(--global-dimension-size-200);
        /* The visual keeps its box when the token's text truncates —
           otherwise it compresses and the visual slides into the end cap. */
        flex-shrink: 0;
        margin-right: var(--global-dimension-size-50);
      `,t[0]=r):r=t[0];let i;return t[1]===n?i=t[2]:(i=B(`span`,{css:r,children:n}),t[1]=n,t[2]=i),i}function Oc({ref:e,children:t,isDisabled:n,css:r,color:i=`var(--global-color-gray-600)`,onPress:a,onRemove:o,size:s=`M`,style:c,leadingVisual:l,maxWidth:u,...d}){let{theme:f}=Mr(),p=l&&s!==`S`?B(Dc,{children:l}):null,m=o?B(`button`,{onClick:()=>{o()},disabled:n,"aria-label":`Remove`,children:B(z,{svg:B(Ht,{})})}):null,h=B(`span`,{className:`token__text`,children:t}),g=()=>a&&o?V(R,{children:[V(`button`,{onClick:()=>{a()},disabled:n,children:[p,h]}),m]}):a?V(`button`,{onClick:()=>{a()},disabled:n,children:[p,h]}):o?V(R,{children:[V(`span`,{children:[p,h]}),m]}):V(R,{children:[p,h]});return B(`div`,{ref:e,css:U(Ec,r),style:{"--internal-token-color":i,...u&&{"--token-max-width":u},...c},"data-theme":f,"data-size":s,...a&&{"data-interactive":!0},...o&&{"data-removable":!0},...p&&{"data-leading-visual":!0},...n&&{"data-disabled":!0},...d,children:g()})}var kc=U`
  --slider-thumb-size: var(--global-dimension-size-200);
  --slider-thumb-bg: white;
  --slider-thumb-border-color: var(--global-color-gray-400);
  --slider-track-height: var(--global-dimension-size-50);
  --slider-track-bg: var(--global-color-gray-300);
  --slider-filled-color: var(--global-color-primary);
  --slider-ring-color: var(--global-color-primary-200);
  --slider-focus-ring-color: var(--focus-ring-color);

  display: grid;
  grid-template-areas:
    "label output"
    "track track";
  gap: var(--global-dimension-size-100);
  grid-template-columns: 1fr auto;
  width: var(--alias-single-line-width, var(--global-dimension-size-2400));
  color: var(--text-color);

  .slider__label {
    grid-area: label;
  }

  .slider__output {
    grid-area: output;
    min-height: var(--global-dimension-size-350);
  }

  .slider__track {
    grid-area: track;
    position: relative;
    height: var(--slider-track-height);
    width: 100%;

    /* Background track line */
    &:before {
      content: "";
      display: block;
      position: absolute;
      background: var(--slider-track-bg);
      height: 100%;
      border-radius: var(--global-rounding-full);
    }

    /* Filled track line */
    &:after {
      content: "";
      display: block;
      position: absolute;
      background: var(--slider-filled-color);
      height: 100%;
      border-radius: var(--global-rounding-full);
    }
  }

  .slider__thumb {
    width: var(--slider-thumb-size);
    height: var(--slider-thumb-size);
    border-radius: 50%;
    background: var(--slider-thumb-bg);
    border: 2px solid var(--slider-thumb-border-color);
    box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.1);
    forced-color-adjust: none;
    transition: box-shadow 200ms cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;

    &:hover,
    &[data-dragging] {
      box-shadow: 0 0 0 4px var(--slider-ring-color);
    }

    &[data-focus-visible] {
      box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.1);
      outline: var(--focus-ring-thickness) solid var(--slider-focus-ring-color);
      outline-offset: var(--focus-ring-offset);
    }
  }

  &[data-orientation="horizontal"] {
    flex-direction: column;
    width: 100%;
    align-items: baseline;

    .slider__number-field {
      .react-aria-Input {
        min-width: var(--global-dimension-size-800);
        width: var(--global-dimension-size-800);
        padding: 0 var(--global-dimension-size-100);
        height: var(--global-dimension-size-350);
        text-align: right;
        margin-bottom: var(--global-dimension-size-100);
      }
    }

    .slider__track {
      height: var(--slider-track-height);
      width: calc(100% - var(--slider-thumb-size));
      left: calc(var(--slider-thumb-size) / 2);

      /* background track line */
      &:before {
        left: calc(var(--slider-thumb-size) / -2);
        width: calc(100% + var(--slider-thumb-size));
        top: 50%;
        transform: translateY(-50%);
      }

      /* filled track line */
      &:after {
        left: calc(var(--slider-start) - var(--slider-thumb-size) / 2);
        width: calc(
          var(--slider-end) - var(--slider-start) + var(--slider-thumb-size)
        );
        top: 50%;
        transform: translateY(-50%);
        z-index: 1;
      }
    }

    .slider__thumb {
      top: 50%;
      z-index: 2;
    }
  }
`;function Ac(e){let n=(0,Y.c)(24),r,i,a,o,s,c;n[0]===e?(r=n[1],i=n[2],a=n[3],o=n[4],s=n[5],c=n[6]):({ref:s,label:a,thumbLabels:c,children:i,css:r,...o}=e,n[0]=e,n[1]=r,n[2]=i,n[3]=a,n[4]=o,n[5]=s,n[6]=c);let l;n[7]===r?l=n[8]:(l=U(kc,r),n[7]=r,n[8]=l);let u;n[9]===a?u=n[10]:(u=a&&B(Sn,{className:`slider__label`,children:a}),n[9]=a,n[10]=u);let d;n[11]===i?d=n[12]:(d=i===void 0?B(Nc,{}):i,n[11]=i,n[12]=d);let f;n[13]===d?f=n[14]:(f=B(t,{className:`slider__output`,children:d}),n[13]=d,n[14]=f);let p;n[15]===c?p=n[16]:(p=B(E,{className:`slider__track`,style:jc,children:e=>{let{state:t}=e;return B(R,{children:t.values.map((e,t)=>B(D,{index:t,"aria-label":c?.[t],className:`slider__thumb`},t))})}}),n[15]=c,n[16]=p);let m;return n[17]!==o||n[18]!==s||n[19]!==l||n[20]!==u||n[21]!==f||n[22]!==p?(m=V(_,{css:l,...o,ref:s,children:[u,f,p]}),n[17]=o,n[18]=s,n[19]=l,n[20]=u,n[21]=f,n[22]=p,n[23]=m):m=n[23],m}function jc(e){let{state:t}=e;return t.values.length===1?{"--slider-start":`0%`,"--slider-end":`${t.getThumbPercent(0)*100}%`}:{"--slider-start":`${t.getThumbPercent(0)*100}%`,"--slider-end":`${t.getThumbPercent(1)*100}%`}}function Mc(e){let t=(0,Y.c)(19),n,r;t[0]===e?(n=t[1],r=t[2]):({onChange:n,...r}=e,t[0]=e,t[1]=n,t[2]=r);let{step:i,getThumbMinValue:a,getThumbMaxValue:o,values:s,setThumbValue:c}=(0,J.useContext)(T),l=`defaultValue`in r,u=s[0]===a(0),d=l&&u?r.defaultValue:s[0],f=st(zn),p=f.id,m;t[3]!==n||t[4]!==c?(m=e=>{n?n(e):typeof e==`number`&&c(0,e)},t[3]=n,t[4]=c,t[5]=m):m=t[5];let h;t[6]===o?h=t[7]:(h=o(0),t[6]=o,t[7]=h);let g;t[8]===a?g=t[9]:(g=a(0),t[8]=a,t[9]=g);let _;t[10]===Symbol.for(`react.memo_cache_sentinel`)?(_=B(Ne,{}),t[10]=_):_=t[10];let v;return t[11]!==f.id||t[12]!==r||t[13]!==i||t[14]!==m||t[15]!==h||t[16]!==g||t[17]!==d?(v=B(Bs,{className:`slider__number-field`,"aria-labelledby":p,value:d,onChange:m,step:i,maxValue:h,minValue:g,...r,children:_}),t[11]=f.id,t[12]=r,t[13]=i,t[14]=m,t[15]=h,t[16]=g,t[17]=d,t[18]=v):v=t[18],v}function Nc(){let e=(0,Y.c)(4),t=(0,J.useContext)(T),n;e[0]===t.values?n=e[1]:(n=t.values.map(Pc).join(` – `),e[0]=t.values,e[1]=n);let r;return e[2]===n?r=e[3]:(r=B(L,{children:n}),e[2]=n,e[3]=r),r}function Pc(e){return e.toString()}var Fc=U`
  display: inline-block;
  padding: 0 var(--global-dimension-size-50);
  border-radius: var(--global-rounding-large);
  border: 1px solid var(--global-color-gray-300);
  min-width: var(--global-dimension-size-150);
  background-color: var(--global-color-gray-200);
  font-size: var(--global-font-size-xs);
  line-height: var(--global-line-height-xs);
  text-align: center;
  color: var(--global-text-color-900);
  font-family: var(--global-font-family-mono);
  &[data-variant="danger"] {
    --counter-base-color: var(--global-color-danger);
    --counter-bg-color: lch(from var(--counter-base-color) 96 calc(c * 0.3) h);
    --counter-border-color: lch(
      from var(--counter-base-color) 88 calc(c * 0.4) h
    );
    --counter-text-color: lch(from var(--counter-base-color) 45 c h);

    background-color: var(--counter-bg-color);
    border-color: var(--counter-border-color);
    color: var(--counter-text-color);

    &[data-theme="dark"] {
      --counter-bg-color: lch(
        from var(--counter-base-color) 18 calc(c * 0.2) h
      );
      --counter-border-color: lch(
        from var(--counter-base-color) 28 calc(c * 0.3) h
      );
      --counter-text-color: lch(
        from var(--counter-base-color) 90 calc(c * 0.8) h
      );
    }
  }
  &[data-variant="quiet"] {
    border: none;
    background: transparent;
    color: var(--global-text-color-500);
  }
`;function Ic(e){let{children:t,variant:n=`default`}=e,{theme:r}=Mr();return B(`span`,{css:Fc,"data-variant":n,"data-theme":r,className:`counter`,children:t})}function Lc(){let e=(0,Y.c)(6),t=(0,J.useRef)(null),[n,r]=(0,J.useState)(!1),[i,a]=(0,J.useState)(!1),o;e[0]===Symbol.for(`react.memo_cache_sentinel`)?(o=()=>{let e=t.current;if(!e)return;if(e.getAttribute(`data-orientation`)!==`horizontal`){r(!1),a(!1);return}let{scrollLeft:n,scrollWidth:i,clientWidth:o}=e,s=i-o;r(n>1),a(n<s-1)},e[0]=o):o=e[0];let s=o;Yt(t,`scroll`,s);let c;e[1]===Symbol.for(`react.memo_cache_sentinel`)?(c={ref:t,onResize:s},e[1]=c):c=e[1],ln(c);let l;e[2]===Symbol.for(`react.memo_cache_sentinel`)?(l=()=>{s()},e[2]=l):l=e[2],(0,J.useEffect)(l);let u;return e[3]!==i||e[4]!==n?(u={ref:t,hasOverflowAtStart:n,hasOverflowAtEnd:i},e[3]=i,e[4]=n,e[5]=u):u=e[5],u}var Rc=U`
  display: flex;
  color: var(--global-text-color-900);
  --tab-border-color: var(--global-border-color-default);

  flex-direction: column;
  height: 100%;

  &[data-orientation="horizontal"] {
    flex: 1 1 auto;
    overflow: hidden;
    box-sizing: border-box;
    .react-aria-TabPanel[data-padded="true"] {
      padding-top: var(--global-dimension-size-200);
    }
  }

  &[data-orientation="vertical"] {
    flex-direction: row;
    .react-aria-TabPanel[data-padded="true"] {
      padding-left: var(--global-dimension-size-200);
    }
  }
`;function zc({children:e,css:t,className:n,orientation:r=`horizontal`,...i}){return B(ee,{css:U(Rc,t),className:F(`react-aria-Tabs`,`tabs`,n),orientation:r,...i,children:e})}var Bc=U`
  display: flex;

  // The sliding selection indicator. react-aria positions it over the
  // selected tab via translate and animates between tabs; only the
  // orientation-specific appearance is styled here.
  .react-aria-SelectionIndicator {
    position: absolute;
    border-radius: var(--global-rounding-small);
    transition-property: translate, width, height;
    transition-duration: 250ms;
    transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);

    @media (prefers-reduced-motion: reduce) {
      transition: none;
    }
  }

  &[data-orientation="vertical"] {
    flex-direction: column;

    // Tighter vertical rhythm than the horizontal bar: shorter tabs and a
    // slimmer pill inset so the rail reads as a compact list, not a stack of
    // spaced-out buttons.
    --tab-pill-inset: var(--global-dimension-size-25)
      var(--global-dimension-size-50);
    .react-aria-Tab {
      padding: var(--global-dimension-size-100) var(--global-dimension-size-200);
      // Lay the label out as a flex line rather than an inline one: a rail
      // label pairs an icon with text, and inline layout leaves the taller
      // icon's descender space below the label, which sits it above the
      // center of its pill.
      display: flex;
      align-items: center;
    }

    // The selected tab is marked with a filled pill behind its label (the
    // same treatment as the side nav's active item) rather than an edge bar,
    // which would float detached from the left-aligned labels. The pill is
    // inset to match the hover pill so the two states share a shape.
    .react-aria-SelectionIndicator {
      inset: var(--tab-pill-inset);
      background: var(--global-color-primary-100);
      z-index: -1;
    }
  }

  &[data-orientation="horizontal"] {
    // Draw the bottom border as an inset shadow so it stays pinned to the
    // visible width while tabs scroll beneath it. When the edge fade below is
    // active the line fades along with the rest of that edge — the whole edge
    // dissolves together.
    box-shadow: inset 0 -1px 0 0 var(--tab-border-color);
    // When there are more tabs than horizontal space, scroll rather than
    // wrapping tab labels or clipping tabs off the edge.
    overflow-x: auto;
    // react-aria scrolls the focused tab just into view on keyboard
    // navigation and honors scroll-padding, so inset the scroll port to keep
    // the focused tab from parking underneath the edge fade.
    scroll-padding-inline: var(--tab-fade-size);
    // Settle trackpad/touch scrolls on a tab boundary so the list never rests
    // with a half-clipped tab under the edge fade. Proximity (not mandatory)
    // keeps long free scrolls through many tabs feeling natural.
    scroll-snap-type: x proximity;
    // Hide the scrollbar; the overflow is still scrollable via trackpad,
    // shift-scroll, or keyboard navigation between tabs. A directional fade
    // (below) signals that more tabs are available since macOS hides the
    // scrollbar until the user scrolls.
    scrollbar-width: none;
    &::-webkit-scrollbar {
      display: none;
    }

    // Fade the edge(s) that have tabs hidden beyond them. The fade is
    // transparent-to-opaque so tabs appear to dissolve off the edge, hinting
    // that the list can be scrolled. Each side's fade width collapses to 0
    // when that side has no hidden tabs, and the mask is dropped entirely
    // when everything fits.
    --tab-fade-size: var(--global-dimension-size-400);
    --tab-fade-start: 0px;
    --tab-fade-end: 0px;
    &[data-overflow-start="true"] {
      --tab-fade-start: var(--tab-fade-size);
    }
    &[data-overflow-end="true"] {
      --tab-fade-end: var(--tab-fade-size);
    }
    &:is([data-overflow-start="true"], [data-overflow-end="true"]) {
      mask-image: linear-gradient(
        to right,
        transparent,
        black var(--tab-fade-start),
        black calc(100% - var(--tab-fade-end)),
        transparent
      );
    }

    .react-aria-SelectionIndicator {
      left: 0;
      bottom: 0;
      width: 100%;
      height: 3px;
      background: var(--tab-indicator-color, var(--global-color-primary));
      z-index: 1;
    }

    .react-aria-Tab {
      // Prevent tabs from shrinking or wrapping their labels when the list
      // runs out of room.
      flex: 0 0 auto;
      white-space: nowrap;
      scroll-snap-align: start;
    }
  }
`,Vc=U`
  display: flex;
  flex-direction: row;
  align-items: stretch;

  .react-aria-TabList {
    // the tabs take the row and the extra content keeps its own width, so the
    // tab list is what scrolls once there are more tabs than space
    flex: 1 1 auto;
    min-width: 0;
  }

  .tab-list-row__extra {
    // the margin, not the tab list's growth, is what holds this at the end —
    // page level styles are free to pin the tab list's flex, and several do
    margin-inline-start: auto;
    flex: none;
    display: flex;
    flex-direction: row;
    align-items: center;
    gap: var(--global-dimension-size-100);
    // the end inset matches the page gutter, so these controls line up with the
    // actions in the header above rather than hugging the edge
    padding-inline-start: var(--global-dimension-size-100);
    padding-inline-end: var(--global-dimension-size-200);
  }

  // the tab list draws its bottom border only under the tabs themselves, so the
  // row carries the rest of the edge across to the end
  &:has(> [data-orientation="horizontal"]) {
    box-shadow: inset 0 -1px 0 0 var(--tab-border-color);
  }
`;function Hc(e){let t=(0,Y.c)(23),n,r,i,a,o;t[0]===e?(n=t[1],r=t[2],i=t[3],a=t[4],o=t[5]):({children:r,extra:a,css:n,className:i,...o}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a,t[5]=o);let{ref:s,hasOverflowAtStart:c,hasOverflowAtEnd:l}=Lc(),u;t[6]===n?u=t[7]:(u=U(Bc,n),t[6]=n,t[7]=u);let d;t[8]===i?d=t[9]:(d=F(`react-aria-TabList`,i),t[8]=i,t[9]=d);let f;t[10]!==r||t[11]!==l||t[12]!==c||t[13]!==o||t[14]!==s||t[15]!==u||t[16]!==d?(f=B(Be,{ref:s,css:u,className:d,"data-overflow-start":c,"data-overflow-end":l,...o,children:r}),t[10]=r,t[11]=l,t[12]=c,t[13]=o,t[14]=s,t[15]=u,t[16]=d,t[17]=f):f=t[17];let p=f;if(a==null)return p;let m;t[18]===a?m=t[19]:(m=B(`div`,{className:`tab-list-row__extra`,children:a}),t[18]=a,t[19]=m);let h;return t[20]!==m||t[21]!==p?(h=V(`div`,{className:`tab-list-row`,css:Vc,children:[p,m]}),t[20]=m,t[21]=p,t[22]=h):h=t[22],h}var Uc=U`
  margin-top: 0;
  padding: 0;
  border-radius: 0;
  outline: none;
  flex: 1 1 auto;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  box-sizing: border-box;
  height: 100%;

  &[data-focus-visible] {
    outline: unset;
  }
`;function Wc(e){let t=(0,Y.c)(14),n,r,i,a;t[0]===e?(n=t[1],r=t[2],i=t[3],a=t[4]):({css:n,className:r,padded:i,...a}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a);let o;t[5]===n?o=t[6]:(o=U(Uc,n),t[5]=n,t[6]=o);let s;t[7]===r?s=t[8]:(s=F(`react-aria-TabPanel`,r),t[7]=r,t[8]=s);let c;return t[9]!==i||t[10]!==a||t[11]!==o||t[12]!==s?(c=B(Fe,{css:o,className:s,"data-padded":i,...a}),t[9]=i,t[10]=a,t[11]=o,t[12]=s,t[13]=c):c=t[13],c}function Gc(e){let t=(0,Y.c)(11),n,r,i;t[0]===e?(n=t[1],r=t[2],i=t[3]):({children:n,id:r,...i}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i);let a;t[4]!==n||t[5]!==r?(a=e=>{let{state:t}=e,{selectedKey:i}=t;return i===r?n:null},t[4]=n,t[5]=r,t[6]=a):a=t[6];let o;return t[7]!==r||t[8]!==i||t[9]!==a?(o=B(Wc,{id:r,...i,children:a}),t[7]=r,t[8]=i,t[9]=a,t[10]=o):o=t[10],o}var Kc=U`
  padding: var(--global-dimension-size-100) var(--global-dimension-size-200);
  cursor: default;
  outline: none;
  position: relative;
  // The hover pill and selection indicator sit at z-index -1; isolate the
  // tab so they paint just behind its label instead of escaping to an outer
  // stacking context and disappearing behind opaque page backgrounds.
  isolation: isolate;
  color: var(--global-text-color-700);
  transition: color 150ms ease-out;
  forced-color-adjust: none;
  -webkit-tap-highlight-color: transparent;
  font-weight: 400;
  line-height: var(--global-line-height-s);
  font-size: var(--global-font-size-s);

  // Hover pill, drawn behind the label and inset from the tab's hit area so
  // adjacent pills never touch. Kept as a pseudo-element so the tab's own box
  // (and the selection indicator's measurements) are unaffected.
  &:before {
    content: "";
    position: absolute;
    inset: var(--tab-pill-inset, var(--global-dimension-size-50));
    border-radius: var(--global-rounding-small);
    transition: background 150ms ease-out;
    z-index: -1;
  }

  @media (prefers-reduced-motion: reduce) {
    &,
    &:before {
      transition: none;
    }
  }

  &[data-hovered],
  &[data-focused],
  &[data-selected] {
    color: var(--global-text-color-900);
  }

  &[data-hovered]:not([data-selected]):before {
    background: var(--global-color-primary-50);
  }

  &[data-disabled] {
    color: var(--global-text-color-300);
    --tab-indicator-color: var(--global-text-color-300);
  }

  &[data-focus-visible]:after {
    content: "";
    position: absolute;
    inset: var(--tab-pill-inset, var(--global-dimension-size-50));
    border-radius: var(--global-rounding-small);
    border: var(--focus-ring-thickness) solid var(--focus-ring-color);
  }
`;function qc(e){let t=(0,Y.c)(15),n,r,i,a;t[0]===e?(n=t[1],r=t[2],i=t[3],a=t[4]):({children:r,css:n,className:i,...a}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a);let o;t[5]===n?o=t[6]:(o=U(Kc,n),t[5]=n,t[6]=o);let s;t[7]===i?s=t[8]:(s=F(`react-aria-Tab`,i),t[7]=i,t[8]=s);let c;t[9]===Symbol.for(`react.memo_cache_sentinel`)?(c=B(En,{className:`react-aria-SelectionIndicator`}),t[9]=c):c=t[9];let l;return t[10]!==r||t[11]!==a||t[12]!==o||t[13]!==s?(l=V(He,{css:o,className:s,...a,children:[r,c]}),t[10]=r,t[11]=a,t[12]=o,t[13]=s,t[14]=l):l=t[14],l}var Jc=e=>{let t=(0,Y.c)(9),{message:n,size:r,className:i}=e,a;t[0]===Symbol.for(`react.memo_cache_sentinel`)?(a=U`
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        width: 100%;
        height: 100%;
        gap: var(--global-dimension-size-100);
      `,t[0]=a):a=t[0];let o;t[1]===r?o=t[2]:(o=B(Qi,{isIndeterminate:!0,"aria-label":`loading`,size:r}),t[1]=r,t[2]=o);let s;t[3]===n?s=t[4]:(s=n==null?null:B(L,{children:n}),t[3]=n,t[4]=s);let c;return t[5]!==i||t[6]!==o||t[7]!==s?(c=V(`div`,{className:i,css:a,children:[o,s]}),t[5]=i,t[6]=o,t[7]=s,t[8]=c):c=t[8],c},Yc=Wt`
  0% {
    opacity: 1;
  }
  50% {
    opacity: 0.4;
  }
  100% {
    opacity: 1;
  }
`,Xc=Wt`
  0% {
    transform: translateX(-100%);
  }
  50% {
    transform: translateX(100%);
  }
  100% {
    transform: translateX(100%);
  }
`,Zc=U`
  display: block;
  background-color: var(--global-color-gray-200);
`,Qc=U`
  animation: ${Yc} 2s ease-in-out 0.5s infinite;
`,$c=U`
  position: relative;
  overflow: hidden;
  /* Fix bug in Safari https://bugs.webkit.org/show_bug.cgi?id=68196 */
  -webkit-mask-image: -webkit-radial-gradient(white, black);

  &::after {
    animation: ${Xc} 2s linear 0.5s infinite;
    background: linear-gradient(
      90deg,
      transparent,
      var(--global-color-gray-300),
      transparent
    );
    content: "";
    position: absolute;
    transform: translateX(-100%);
    bottom: 0;
    left: 0;
    right: 0;
    top: 0;
  }
`,el=e=>{if(typeof e==`number`)return`${e}px`;if(typeof e==`string`)switch(e){case`none`:return`0`;case`XS`:return`var(--global-rounding-xsmall)`;case`S`:return`var(--global-rounding-small)`;case`M`:return`var(--global-rounding-medium)`;case`L`:return`var(--global-rounding-large)`;case`circle`:return`50%`;default:return e}return`var(--global-rounding-medium)`};function tl({ref:e,width:t=`100%`,height:n=`1.2em`,borderRadius:r=`S`,animation:i=`pulse`,className:a,...o}){let s=typeof t==`number`?`${t}px`:t,c=typeof n==`number`?`${n}px`:n,l=el(r);return B(`span`,{ref:e,className:F(a,`skeleton`),css:[Zc,i===`pulse`&&Qc,i===`wave`&&$c,U`
          width: ${s};
          height: ${c};
          border-radius: ${l};
        `],...o})}tl.displayName=`Skeleton`;var nl=e=>{let t=(0,Y.c)(5),n,r,i;t[0]===Symbol.for(`react.memo_cache_sentinel`)?(n=B(tl,{height:100,borderRadius:8,animation:`wave`}),r=B(tl,{height:24,width:`80%`,animation:`wave`}),i=B(tl,{height:16,width:`60%`,animation:`wave`}),t[0]=n,t[1]=r,t[2]=i):(n=t[0],r=t[1],i=t[2]);let a;return t[3]===e?a=t[4]:(a=V(W,{direction:`column`,gap:`size-100`,width:`100%`,...e,children:[n,r,i]}),t[3]=e,t[4]=a),a},rl=U`
  display: flex;
  flex-direction: column;
`,il=U`
  display: flex;
  gap: 6px;
`,al=[[3,2,5,1.5,4,2.5,4],[2,4,1.5,5,3,3.5],[4,2.5,5,2,3],[3,4.5,2,4,1.5,4],[3.5,2,5,2.5]],ol=[`100%`,`95%`,`100%`,`88%`,`92%`];function sl({lines:e=3,animation:t=`pulse`,gap:n=8}){let r=(e,t)=>{let n=al[e%al.length],r=t?Math.ceil(n.length*.5):n.length;return n.slice(0,r)};return B(`div`,{css:[rl,U`
          gap: ${n}px;
        `],children:Array.from({length:e},(n,i)=>{let a=i===e-1,o=r(i,a),s=a?`55%`:ol[i%ol.length];return B(`div`,{css:[il,U`
                width: ${s};
              `],children:o.map((e,n)=>B(tl,{css:U`
                  flex-grow: ${e};
                  min-width: 20px;
                `,height:`1em`,animation:t},n))},i)})})}var cl=U`
  // TODO: respect trailingVisual and leadingVisual inside of phoenix button
  // ideally the content is justified start with leading visual, and trailing visual
  // is positioned at the end
  // the current styling assumes content + 1 trailing visual
  button {
    display: flex;
    align-items: center;
    justify-content: space-between;
    min-width: inherit;
    width: 100%;
    text-wrap: nowrap;

    &:not([data-disabled="true"]) {
      &[data-pressed],
      &:hover {
        --button-border-color: var(--global-input-field-border-color-active);
      }
    }
  }

  // A Select is mechanically triggered by a button, but visually behaves as
  // a bounded form field. Any focus emphasizes the field border; keyboard
  // focus adds the shared ring at the field boundary.
  &[data-focused]:not([data-invalid]) button {
    --button-border-color: var(--field-border-color-active);
  }

  &[data-focus-visible] button {
    outline: var(--focus-ring-thickness) solid var(--focus-ring-color);
    outline-offset: calc(-1 * var(--focus-ring-thickness));
  }

  button[data-size="S"][data-childless="false"] {
    padding-right: var(--global-dimension-size-50);
  }

  button[data-size="M"][data-childless="false"] {
    padding-right: var(--global-dimension-size-100);
  }

  &[data-invalid="true"] button {
    border-color: var(--global-color-danger);
  }

  .react-aria-SelectValue {
    &[data-placeholder] {
      font-style: italic;
      color: var(--text-color-placeholder);
    }
  }
`;function ll({ref:e,...t}){let{size:n=`M`,...r}=t;return B(wt,{size:n,children:B(Re,{"data-size":n,className:`select`,ref:e,css:U(ss,cl),...r})})}function ul(e){let t=(0,Y.c)(10),n,r,i;t[0]===e?(n=t[1],r=t[2],i=t[3]):({ref:r,children:n,...i}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i);let a;t[4]===n?a=t[5]:(a=e=>{let{isSelected:t}=e;return V(W,{direction:`row`,justifyContent:`space-between`,alignItems:`center`,gap:`size-200`,width:`100%`,children:[B(`span`,{children:n}),t&&B(z,{svg:B(yn,{})})]})},t[4]=n,t[5]=a);let o;return t[6]!==r||t[7]!==i||t[8]!==a?(o=B(De,{...i,ref:r,children:a}),t[6]=r,t[7]=i,t[8]=a,t[9]=o):o=t[9],o}ul.displayName=`SelectItem`,U`
  max-width: 100%;
  height: auto;
`;var dl=16,fl=8,pl=.05,ml=Wt`
  from {
    opacity: 0;
    transform: translateY(-130%);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
`,hl=U`
  position: fixed;
  top: var(--global-dimension-size-200);
  left: 50%;
  width: 400px;
  max-width: calc(100vw - var(--global-dimension-size-400));
  transform: translateX(-50%);
  outline: none;
  z-index: ${Zn};

  --collapsed-peek: ${dl}px;
  --expanded-gap: ${fl}px;
  --toast-row-height: 72px;
  --toast-count: 1;

  height: calc(
    var(--toast-row-height) + (var(--toast-count) - 1) * var(--collapsed-peek)
  );
  transition: height 300ms cubic-bezier(0.21, 1.02, 0.73, 1);

  &[data-hovered],
  &[data-focused] {
    height: calc(
      var(--toast-stack-height, var(--toast-row-height)) +
        (var(--toast-count) - 1) * var(--expanded-gap)
    );
  }

  /* Expand (un-stack) the toasts when the region is hovered or focused. */
  &[data-hovered] .toast-positioner,
  &[data-focused] .toast-positioner {
    transform: translateY(
      calc(var(--toast-offset, 0px) + var(--toast-index) * var(--expanded-gap))
    );
    opacity: 1;
  }

  @media (prefers-reduced-motion: reduce) {
    transition: none;
  }
`,gl=U`
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  transform-origin: top center;
  transform: translateY(
      calc(var(--toast-index) * var(--collapsed-peek, ${dl}px))
    )
    scale(calc(1 - var(--toast-index) * ${pl}));
  opacity: calc(1 - var(--toast-index) * 0.1);
  transition:
    transform 300ms cubic-bezier(0.21, 1.02, 0.73, 1),
    opacity 300ms ease;

  @media (prefers-reduced-motion: reduce) {
    transition: none;
  }
`,_l=U`
  display: flex;
  flex-direction: column;
  gap: var(--global-dimension-size-100);
  padding: var(--global-dimension-size-100) var(--global-dimension-size-100);
  border-radius: 8px;
  outline: none;
  width: 100%;
  box-sizing: border-box;
  position: relative;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  animation: ${ml} 280ms cubic-bezier(0.21, 1.02, 0.73, 1);
  --toast-border: 1px solid var(--global-border-color-default);
  --toast-color: var(--global-static-color-900);
  &[data-theme="light"] {
    --toast-border: 1px solid
      lch(from var(--internal-token-color) 88 calc(c * 0.4) h);
    --toast-background-color: lch(
      from var(--internal-token-color) 96 calc(c * 0.3) h
    );
    --toast-color: lch(from var(--internal-token-color) 45 c h);
  }
  &[data-theme="dark"] {
    --toast-border: 1px solid
      lch(from var(--internal-token-color) 28 calc(c * 0.3) h);
    --toast-background-color: lch(
      from var(--internal-token-color) 18 calc(c * 0.2) h
    );
    --toast-color: lch(from var(--internal-token-color) 90 calc(c * 0.8) h);
    backdrop-filter: blur(4px);
  }
  background: var(--toast-background-color);
  background-color: var(--toast-background-color);
  border: var(--toast-border);
  color: var(--toast-color);

  @media (prefers-reduced-motion: reduce) {
    animation: none;
  }

  &[data-focus-visible] {
    outline: var(--focus-ring-thickness) solid var(--focus-ring-color);
    outline-offset: var(--focus-ring-offset);
  }

  [slot="close"][data-hovered],
  [slot="close"][data-pressed] {
    background-color: transparent;
    color: inherit;
  }

  .toast-action-container {
    display: flex;
    align-items: center;
    justify-content: flex-end;
    width: 100%;
  }

  .toast-action-button {
    background: transparent;
    border: var(--toast-border);
    color: var(--toast-color);
    outline: none;
    backdrop-filter: blur(10px);

    &:hover,
    &:focus-visible,
    &:active {
      background: var(--toast-background-color);
      background-color: var(--toast-background-color);
    }
  }

  .react-aria-ToastContent {
    display: flex;
    flex-direction: column;
    flex: 1 1 auto;
    min-width: 0px;

    [slot="title"] {
      align-items: center;
      color: var(--toast-color);
      font-weight: bold;
      display: flex;
      flex-direction: row;
      gap: var(--global-dimension-size-50);
    }

    [slot="description"] {
      color: var(--toast-color);
    }
  }
`;function vl(e){let t=(0,Y.c)(6),{stackIndex:n,children:r}=e,i=100-n,a;t[0]!==n||t[1]!==i?(a={"--toast-index":n,zIndex:i},t[0]=n,t[1]=i,t[2]=a):a=t[2];let o;return t[3]!==r||t[4]!==a?(o=B(`div`,{className:`toast-positioner`,css:gl,style:a,children:r}),t[3]=r,t[4]=a,t[5]=o):o=t[5],o}var yl=e=>{switch(e){case`success`:return B(z,{svg:B(Yn,{})});case`error`:return B(z,{svg:B(Fn,{})});default:return null}},bl=e=>{switch(e){case`success`:return`var(--global-color-success)`;case`error`:return`var(--global-color-danger)`;default:return`var(--global-color-gray-600)`}},xl=e=>{let t=(0,Y.c)(33),{toast:n}=e,{theme:r}=Mr(),i=(0,J.useContext)(ie),a;t[0]!==i?.visibleToasts||t[1]!==n.key?(a=i?.visibleToasts.findIndex(e=>e.key===n.key)??0,t[0]=i?.visibleToasts,t[1]=n.key,t[2]=a):a=t[2];let o=Math.max(0,a),s;t[3]===n.content.variant?s=t[4]:(s=yl(n.content.variant),t[3]=n.content.variant,t[4]=s);let c=s,l;t[5]===n.content.variant?l=t[6]:(l=bl(n.content.variant),t[5]=n.content.variant,t[6]=l);let u;t[7]===l?u=t[8]:(u={"--internal-token-color":l},t[7]=l,t[8]=u);let d;t[9]===Symbol.for(`react.memo_cache_sentinel`)?(d=U`
            display: flex;
            justify-content: space-between;
            width: 100%;
          `,t[9]=d):d=t[9];let f;t[10]!==c||t[11]!==n.content.title?(f=V(L,{slot:`title`,size:`M`,children:[c,n.content.title]}),t[10]=c,t[11]=n.content.title,t[12]=f):f=t[12];let p;t[13]===n.content.message?p=t[14]:(p=B(L,{slot:`description`,children:n.content.message}),t[13]=n.content.message,t[14]=p);let m;t[15]!==f||t[16]!==p?(m=V(Te,{children:[f,p]}),t[15]=f,t[16]=p,t[17]=m):m=t[17];let h;t[18]===Symbol.for(`react.memo_cache_sentinel`)?(h=B(Cn,{slot:`close`,size:`S`,color:`inherit`,type:`button`,"aria-label":`Close notification`,children:B(z,{svg:B(Ht,{})})}),t[18]=h):h=t[18];let g;t[19]===m?g=t[20]:(g=V(`div`,{css:d,children:[m,h]}),t[19]=m,t[20]=g);let _;t[21]!==n.content.action||t[22]!==n.key?(_=n.content.action?B(`div`,{className:`toast-action-container`,children:typeof n.content.action==`object`&&`text`in n.content.action?B(H,{className:`toast-action-button`,onPress:()=>{let e=n.content.action;if(typeof e==`object`&&e&&`onClick`in e){let t=e.closeOnClick??!0,r=()=>{xr?.close(n.key)};e.onClick(r),t&&r()}},size:`S`,children:n.content.action.text}):n.content.action}):null,t[21]=n.content.action,t[22]=n.key,t[23]=_):_=t[23];let v;t[24]!==g||t[25]!==_||t[26]!==u||t[27]!==r||t[28]!==n?(v=V(se,{toast:n,css:_l,className:`react-aria-Toast`,style:u,"data-variant":n.content.variant,"data-theme":r,children:[g,_]}),t[24]=g,t[25]=_,t[26]=u,t[27]=r,t[28]=n,t[29]=v):v=t[29];let y;return t[30]!==o||t[31]!==v?(y=B(vl,{stackIndex:o,children:v}),t[30]=o,t[31]=v,t[32]=y):y=t[32],y},Sl=U`
  display: flex;
  align-items: center;

  a {
    color: var(--global-text-color-700);
    border-radius: var(--global-rounding-small);
    text-decoration: none;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    max-width: 40ch;
    &:hover {
      text-decoration: underline;
    }
  }

  &[data-current],
  &[data-current] a {
    color: var(--global-text-color-900);
    font-weight: 600;
    cursor: default;
    &:hover {
      text-decoration: none;
    }
  }
`;function Cl(e){let t=(0,Y.c)(12),n,r;t[0]===e?(n=t[1],r=t[2]):({ref:r,...n}=e,t[0]=e,t[1]=n,t[2]=r);let i,a;t[3]===n?(i=t[4],a=t[5]):({children:i,...a}=n,t[3]=n,t[4]=i,t[5]=a);let o;t[6]===i?o=t[7]:(o=e=>{let{isCurrent:t}=e;return V(R,{children:[i,!t&&B(z,{svg:B(er,{})})]})},t[6]=i,t[7]=o);let s;return t[8]!==r||t[9]!==a||t[10]!==o?(s=B(O,{css:Sl,...a,className:`breadcrumb`,ref:r,children:o}),t[8]=r,t[9]=a,t[10]=o,t[11]=s):s=t[11],s}var wl=U`
  display: flex;
  align-items: center;
  margin: 0;
  padding: 0;
  color: var(--global-text-color-900);
  --breadcrumb-separator-icon-padding: var(--global-dimension-size-50);

  &[data-size="S"] {
    font-size: var(--global-font-size-s);
    line-height: var(--global-line-height-s);
    --breadcrumb-separator-icon-padding: var(--global-dimension-size-25);
  }

  &[data-size="M"] {
    font-size: var(--global-font-size-m);
    line-height: var(--global-line-height-m);
    --breadcrumb-separator-icon-padding: var(--global-dimension-size-50);
  }

  &[data-size="L"] {
    font-size: var(--global-font-size-l);
    line-height: var(--global-line-height-l);
    --breadcrumb-separator-icon-padding: var(--global-dimension-size-75);
  }

  .breadcrumb > .icon-wrap {
    padding: 0 var(--breadcrumb-separator-icon-padding);
  }
`;function Tl({ref:e,...t}){let{size:n=`M`,...r}=t;return B(le,{css:wl,...r,ref:e,"data-size":n})}var El=U`
  list-style: none;
  padding: 0;
  margin: 0;

  & li {
    position: relative;
    padding: var(--global-dimension-size-200);

    &:not(:first-of-type)::after {
      content: " ";
      border-top: 1px solid var(--global-border-color-default);
      position: absolute;
      left: var(--global-dimension-size-200);
      right: 0;
      top: 0;
    }
  }

  &[data-list-size="S"] {
    & li {
      padding: var(--global-dimension-size-100);

      &:not(:first-of-type)::after {
        left: var(--global-dimension-size-100);
      }
    }
  }
`;function Dl({ref:e,size:t=`M`,children:n,...r}){return B(`ul`,{ref:e,css:El,"data-list-size":t,...r,children:n})}function Ol(e){let t=(0,Y.c)(8),n,r,i;t[0]===e?(n=t[1],r=t[2],i=t[3]):({ref:i,children:n,...r}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i);let a;return t[4]!==n||t[5]!==r||t[6]!==i?(a=B(`li`,{ref:i,...r,children:n}),t[4]=n,t[5]=r,t[6]=i,t[7]=a):a=t[7],a}var kl=Wt`
  from {
    transform: translate(-50%, var(--global-dimension-size-450));
    opacity: 0;
  }
  to {
    transform: translate(-50%, 0);
    opacity: 1;
  }
`,Al=U`
  position: absolute;
  bottom: var(--global-dimension-size-450);
  left: 50%;
  transform: translateX(-50%);
  z-index: 10;
  box-shadow:
    0px 10px 20px 0px rgba(0, 0, 0, 0.1),
    0px 4px 8px 0px rgba(0, 0, 0, 0.1);
  border-radius: var(--global-rounding-medium);
  padding: var(--global-dimension-size-100);
  background-color: var(--floating-toolbar-background-color);
  border: 1px solid var(--floating-toolbar-border-color);
  animation: ${kl} 0.1s ease-in-out;
`,jl=e=>{let t=(0,Y.c)(2),{children:n}=e,r;return t[0]===n?r=t[1]:(r=B(`div`,{css:Al,children:n}),t[0]=n,t[1]=r),r},Ml=U`
  display: flex;

  gap: var(--global-dimension-size-100);

  &[data-orientation="vertical"] {
    flex-direction: column;
    align-items: start;
  }

  &[data-orientation="horizontal"] {
    flex-direction: row;
    align-items: center;
  }

  .react-aria-Group {
    display: contents;
  }
`;function Nl(e){let t=(0,Y.c)(6),n,r;t[0]===e?(n=t[1],r=t[2]):({ref:r,...n}=e,t[0]=e,t[1]=n,t[2]=r);let i;return t[3]!==n||t[4]!==r?(i=B(Ae,{...n,ref:r,css:Ml,children:n.children}),t[3]=n,t[4]=r,t[5]=i):i=t[5],i}var Pl=U`
  align-self: stretch;
  background-color: var(--global-border-color-default);

  &[aria-orientation="vertical"] {
    width: 1px;
    margin: 0 var(--global-dimension-size-50);
  }

  &:not([aria-orientation="vertical"]) {
    border: none;
    height: 1px;
    width: 100%;
    margin: var(--global-dimension-size-50) 0;
  }
`;function Fl(e){let t=(0,Y.c)(6),n,r;t[0]===e?(n=t[1],r=t[2]):({ref:r,...n}=e,t[0]=e,t[1]=n,t[2]=r);let i;return t[3]!==n||t[4]!==r?(i=B(it,{...n,ref:r,css:Pl,className:`separator react-aria-Separator`}),t[3]=n,t[4]=r,t[5]=i):i=t[5],i}var Il=(0,J.createContext)(null);function Ll(e){let t=(0,Y.c)(5),{isCollapsed:n,children:r}=e,i;t[0]===n?i=t[1]:(i={isCollapsed:n},t[0]=n,t[1]=i);let a=i,o;return t[2]!==r||t[3]!==a?(o=B(Il.Provider,{value:a,children:r}),t[2]=r,t[3]=a,t[4]=o):o=t[4],o}function Rl(){return(0,J.useContext)(Il)}var zl=e=>U`
  ${e?.borderColor?`--global-card-border-color: ${e.borderColor};`:``}
  display: flex;
  flex-direction: column;
  color: var(--global-text-color-900);
  border-radius: var(--global-rounding-medium);
  border: 1px solid var(--global-card-border-color);
  overflow: hidden;
  box-sizing: border-box;

  /* Card Header Styles */
  & > header {
    display: flex;
    flex-direction: row;
    flex: none;
    justify-content: space-between;
    align-items: center;
    padding: 0 var(--global-dimension-size-200);
    height: var(--global-card-header-height);
    transition: background-color 0.2s ease-in-out;

    & .card__collapse-toggle-icon {
      margin-right: var(--global-dimension-size-100);
    }

    /* The title and subtitle are shown inline with a gap */
    & .card__heading {
      display: flex;
      flex-direction: row;
      align-items: center;
      gap: var(--global-dimension-size-200);
      min-width: 0;
    }

    & .card__title {
      font-size: var(--global-font-size-m);
      line-height: var(--global-line-height-m);
      display: flex;
      align-items: center;
      gap: var(--global-dimension-size-100);
      flex-shrink: 0;
      white-space: nowrap;
    }

    /* Takes what the title and subtitle leave, down to nothing, rather than
       widening the header */
    & .card__header-content {
      flex: 1 1 auto;
      min-width: 0;
    }

    /* The heading has room to give only if it grows itself */
    & .card__heading:has(.card__header-content) {
      flex: 1 1 auto;
    }

    /* The subtitle truncates rather than wrapping the fixed-height header */
    & .card__sub-title {
      color: var(--global-text-color-700);
      min-width: 0;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }

    /* Header layout when the title holds interactive controls */
    & .card__collapsible-header {
      display: flex;
      flex: 1;
      flex-direction: row;
      align-items: center;
      height: 100%;
      cursor: pointer;
      /* Without this the row floors at its contents' width and pushes the
         extra slot's controls past the card's edge */
      min-width: 0;

      & .card__collapsible-button {
        flex: none;
        width: auto;
      }
    }

    /* Collapsible button styles */
    & .card__collapsible-button {
      display: flex;
      flex: 1;
      flex-direction: row;
      align-items: center;
      text-align: left;
      /* Without this the button floors at the width of the heading it wraps and
         pushes the extra slot's controls past the card's edge. The title does
         not shrink, so the button also has to clip: squeezed hard enough it
         would otherwise paint the title over those same controls */
      min-width: 0;
      overflow: hidden;
      width: 100%;
      height: 100%;
      appearance: none;
      cursor: pointer;
      color: var(--global-text-color-900);
    }
  }

  &[data-collapsed="false"][data-title-separator="true"] > header {
    border-bottom: 1px solid var(--global-card-border-color);
  }

  /* Card Body Styles */
  & .card__body {
    flex: 1 1 auto;
    &[data-scrollable="true"] {
      overflow-y: auto;
    }
  }

  /* Compact variant styles */
  &[data-variant="compact"] .card__title {
    font-size: var(--global-font-size-m);
    line-height: var(--global-line-height-m);
  }

  /* Collapsible behavior: highlight the header only when a region that
     toggles is hovered, so the affordance matches the click target */
  &[data-collapsible="true"] {
    & > header:has(.card__collapsible-button:hover),
    & > header:has(.card__collapsible-header:hover) {
      background-color: var(--global-card-header-background-color-hover);
    }
  }

  &[data-collapsed="true"] {
    & .card__body {
      display: none !important;
    }
  }
`;function Bl({ref:e,title:t,titleExtra:n,titleSeparator:r=!0,subTitle:i,headerContent:a,children:o,collapsible:s=!1,interactiveTitle:c=!1,collapseButtonLabel:l,defaultOpen:u=!0,isOpen:d,scrollBody:f=!1,extra:p,onCollapseChange:m,onOpenChange:h,testId:g,..._}){let{styleProps:v}=bn(_,vn),[y,b]=(0,J.useState)(s?!u:!1),x=d==null?y:!d,S=(0,J.useId)(),C=(0,J.useId)(),w=(0,J.useId)(),T=(0,J.useId)(),E=(0,J.useEffectEvent)(e=>{m?.(e)});(0,J.useEffect)(()=>{E(x)},[x]);let D=V(`div`,{id:w,className:`card__heading`,children:[V(ot,{level:3,weight:`heavy`,className:`card__title`,children:[t,n]}),i&&B(ot,{level:4,className:`card__sub-title`,children:i}),a&&B(`div`,{className:`card__header-content`,children:a})]}),O=()=>{b(!x),h?.(x)},k=e=>{let t=e.target;t instanceof Element&&t.closest(`button,a,input,select,textarea,[role="button"]`)||O()},A=V(`button`,{onClick:O,className:`card__collapsible-button button--reset`,id:C,"aria-controls":T,"aria-expanded":!x,"aria-label":c?l:void 0,"aria-labelledby":c&&l==null?w:void 0,children:[B(Jt,{isExpanded:!x,className:`card__collapse-toggle-icon`}),!c&&D]});return B(Ll,{isCollapsed:x,children:V(`section`,{ref:e,css:zl(v.style),className:`card`,"data-collapsible":s,"data-collapsed":x,"data-title-separator":r,"data-testid":g,style:v.style,children:[V(`header`,{id:S,children:[s?c?V(`div`,{className:`card__collapsible-header`,onClick:k,children:[A,D]}):A:D,p]}),B(`div`,{className:`card__body`,id:T,"aria-labelledby":S,"aria-hidden":x,"data-scrollable":f,children:o})]})})}var Vl=U`
  /* The card wraps header content in a block, and an inline box ignores
     overflow — without this the excerpt lays itself out at full width and gets
     hard-clipped by the header instead of ending in an ellipsis */
  display: block;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  color: var(--global-text-color-700);
  font-size: var(--global-font-size-s);
  line-height: var(--global-line-height-s);
  /* The preview is the last thing in the header's growing side, so its ellipsis
     would otherwise butt up against the extra slot's controls, or against the
     card's edge on a card that has none */
  padding-right: var(--global-dimension-size-200);
`;function Hl(e){let t=(0,Y.c)(2),{children:n}=e;if(!Rl()?.isCollapsed||!n)return null;let r;return t[0]===n?r=t[1]:(r=B(`span`,{className:`card__collapsed-preview`,css:Vl,"aria-hidden":`true`,children:n}),t[0]=n,t[1]=r),r}var Ul=U`
  --switch-track-width: var(--global-dimension-size-450);
  --switch-track-height: var(--global-dimension-size-250);
  --switch-track-bg: var(--global-color-gray-400);
  --switch-track-bg-selected: var(--global-color-primary);
  --switch-thumb-size: var(--global-dimension-size-200);
  --switch-thumb-bg: var(--global-color-gray-900);
  --switch-thumb-bg-selected: var(--global-color-gray-50);
  --switch-thumb-inset: var(--global-dimension-size-25);

  display: flex;
  position: relative;
  align-items: center;
  gap: var(--global-dimension-size-100);
  color: var(--global-text-color-900);
  font-size: var(--global-font-size-m);
  line-height: var(--global-line-height-m);
  white-space: nowrap;
  cursor: pointer;

  .indicator {
    width: var(--switch-track-width);
    height: var(--switch-track-height);
    background: var(--switch-track-bg);
    border-radius: var(--global-rounding-full);
    transition: background 200ms cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    flex-shrink: 0;

    &:before {
      content: "";
      position: absolute;
      top: var(--switch-thumb-inset);
      left: var(--switch-thumb-inset);
      width: var(--switch-thumb-size);
      height: var(--switch-thumb-size);
      background: var(--switch-thumb-bg);
      border-radius: 50%;
      transition:
        transform 200ms cubic-bezier(0.4, 0, 0.2, 1),
        background 200ms cubic-bezier(0.4, 0, 0.2, 1);
    }
  }

  &:not([data-disabled]):hover .indicator {
    opacity: 0.85;
  }

  &[data-selected] {
    .indicator {
      background: var(--switch-track-bg-selected);

      &:before {
        transform: translateX(
          calc(
            var(--switch-track-width) - var(--switch-thumb-size) - 2 *
              var(--switch-thumb-inset)
          )
        );
        background: var(--switch-thumb-bg-selected);
      }
    }

    &:not([data-disabled]):hover .indicator {
      opacity: 0.9;
    }
  }

  &[data-focus-visible] .indicator {
    outline: var(--focus-ring-thickness) solid var(--focus-ring-color);
    outline-offset: var(--focus-ring-offset);
  }

  &[data-disabled] {
    opacity: 0.5;
    cursor: not-allowed;
  }

  &[data-label-placement="start"] {
    flex-direction: row-reverse;
  }

  &[data-label-placement="end"] {
    flex-direction: row;
  }

  &[data-size="S"] {
    --switch-track-width: var(--global-dimension-size-400);
    --switch-track-height: var(--global-dimension-size-225);
    --switch-thumb-size: var(--global-dimension-size-175);
    font-size: var(--global-font-size-s);
    line-height: var(--global-line-height-s);
  }
`;function Wl({ref:e,children:t,labelPlacement:n=`end`,size:r=`M`,...i}){return V(b,{...i,ref:e,css:Ul,"data-label-placement":n,"data-size":r,children:[B(`div`,{className:`indicator`}),t]})}U`
  position: relative;
`,U`
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: var(--global-rounding-medium);
  background: rgba(0 0 0 / 0.5);
  color: var(--global-text-color-900);
  font-size: var(--global-font-size-l);
  font-weight: 500;
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.2s ease-in-out;
  z-index: 1;

  [data-drop-target] > & {
    opacity: 1;
  }
`;var Gl=U`
  display: flex;
  flex-direction: column;
  min-height: 160px;
  border: 1px solid var(--global-color-gray-200);
  border-radius: var(--global-rounding-medium);
  background-color: var(--global-input-field-background-color);
  color: var(--global-text-color-700);
  text-align: center;
  cursor: pointer;
  transition:
    border-color 0.2s ease-in-out,
    background-color 0.2s ease-in-out;

  &[data-focus-visible] {
    border-color: var(--focus-ring-color);
    outline: var(--focus-ring-thickness) solid var(--focus-ring-color);
    outline-offset: calc(-1 * var(--focus-ring-thickness));
  }

  &[data-drop-target] {
    border-color: var(--global-color-primary);
    background-color: var(--global-color-primary-100);
  }

  &[data-disabled] {
    cursor: not-allowed;
    opacity: var(--global-opacity-disabled);

    .file-drop-zone__trigger {
      cursor: not-allowed;
    }
  }

  .file-drop-zone__trigger {
    display: flex;
    flex: 1;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: var(--global-dimension-size-100);
    padding: var(--global-dimension-size-400);
    cursor: pointer;
  }

  .file-drop-zone__icon {
    color: var(--global-text-color-500);
  }

  &[data-drop-target] .file-drop-zone__icon {
    color: var(--global-color-primary);
  }

  .file-drop-zone__label {
    font-size: var(--global-font-size-m);
    font-weight: 500;
    color: var(--global-text-color-900);
  }

  .file-drop-zone__description {
    font-size: var(--global-font-size-s);
    color: var(--global-text-color-700);
  }
`,Kl=U`
  display: flex;
  flex-direction: column;
  gap: var(--global-dimension-size-100);
  width: 100%;

  .file-list__item {
    display: flex;
    align-items: center;
    gap: var(--global-dimension-size-150);
    padding: var(--global-dimension-size-100) var(--global-dimension-size-150);
    background-color: var(--global-color-gray-100);
    border-radius: var(--global-rounding-small);
    border: 1px solid var(--global-color-gray-200);
  }

  .file-list__item[data-status="error"] {
    border-color: var(--global-severity-danger);
    background-color: var(--global-severity-danger-100);
  }

  .file-list__icon {
    flex-shrink: 0;
    font-size: 20px;
    color: var(--global-text-color-500);
  }

  .file-list__details {
    flex: 1;
    min-width: 0;
    display: flex;
    flex-direction: column;
    gap: var(--global-dimension-size-50);
  }

  .file-list__name {
    font-size: var(--global-font-size-s);
    font-weight: 500;
    color: var(--global-text-color-900);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .file-list__meta {
    display: flex;
    align-items: center;
    gap: var(--global-dimension-size-100);
    font-size: var(--global-font-size-xs);
    color: var(--global-text-color-700);
  }

  .file-list__error {
    font-size: var(--global-font-size-xs);
    color: var(--global-severity-danger);
  }

  .file-list__progress {
    flex: 1;
  }

  .file-list__remove {
    flex-shrink: 0;
  }
`;U`
  display: flex;
  flex-direction: column;

  .file-input__label {
    padding: 5px 0;
    display: inline-block;
    font-size: var(--global-font-size-xs);
    line-height: var(--global-line-height-xs);
    font-weight: var(--font-weight-heavy);
  }

  .file-input__control {
    display: flex;
    align-items: center;
    gap: var(--global-dimension-size-50);
    background-color: var(--global-input-field-background-color);
    border: var(--global-border-size-thin) solid
      var(--global-input-field-border-color);
    border-radius: var(--global-rounding-small);
    padding: 0 var(--global-dimension-size-25) 0
      var(--global-dimension-size-100);
    min-height: var(--global-input-height-m);
    box-sizing: border-box;
    transition: border-color 0.2s ease-in-out;

    &:hover:not([data-disabled]) {
      border-color: var(--global-input-field-border-color-active);
    }
  }

  &[data-disabled] {
    opacity: var(--global-opacity-disabled);

    .file-input__control {
      cursor: not-allowed;
    }
  }

  .file-input__name {
    flex: 1;
    min-width: 0;
    font-size: var(--global-font-size-s);
    color: var(--global-text-color-900);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .file-input__placeholder {
    flex: 1;
    min-width: 0;
    font-size: var(--global-font-size-s);
    color: var(--text-color-placeholder);
    font-style: italic;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .file-input__actions {
    display: flex;
    align-items: center;
    flex-shrink: 0;
  }

  [slot="description"] {
    font-size: var(--global-font-size-xs);
    padding-top: var(--global-dimension-size-50);
    color: var(--global-text-color-500);
    line-height: var(--global-dimension-font-size-200);
    min-height: var(--global-dimension-font-size-200);
    display: inline-block;
  }
`;function ql(e,t){let{si:n=!1,decimalPlaces:r=1}=t??{},i=n?1e3:1024;if(Math.abs(e)<i)return e+` B`;let a=n?[`kB`,`MB`,`GB`,`TB`,`PB`,`EB`,`ZB`,`YB`]:[`KiB`,`MiB`,`GiB`,`TiB`,`PiB`,`EiB`,`ZiB`,`YiB`],o=-1,s=10**r;do e/=i,++o;while(Math.round(Math.abs(e)*s)/s>=i&&o<a.length-1);return e.toFixed(r)+` `+a[o]}function Jl(e,t){return!t||t.length===0||t.some(t=>{if(t.startsWith(`.`))return e.name.toLowerCase().endsWith(t.toLowerCase());if(t.endsWith(`/*`)){let n=t.slice(0,-2);return e.type.startsWith(n)}return e.type===t})}function Yl(e,t){return t==null||e.size<=t}function Xl({acceptedFileTypes:e,allowsMultiple:t=!1,maxFiles:n,maxFileSize:r,onSelect:i,onSelectRejected:a,label:o=`Drag and drop files here`,description:s,isDisabled:c,...l}){let u=(0,J.useRef)(null),d=(0,J.useRef)(null);(0,J.useEffect)(()=>{let e=d.current;if(!e||c)return;let t=e=>{(e.key===`Enter`||e.key===` `)&&(e.preventDefault(),u.current?.click())};return e.addEventListener(`keydown`,t),()=>e.removeEventListener(`keydown`,t)},[c]);let f=(0,J.useCallback)(o=>{let s=[],c=[],l=t?n??1/0:1;for(let t of o){if(!Jl(t,e)){c.push({file:t,reason:`type`,message:`File type not accepted. Allowed: ${e?.join(`, `)}`});continue}if(!Yl(t,r)){c.push({file:t,reason:`size`,message:`File too large. Maximum size: ${ql(r)}`});continue}if(s.length>=l){c.push({file:t,reason:`count`,message:`Maximum ${l} file${l>1?`s`:``} allowed`});continue}s.push(t)}s.length>0&&i&&i(s),c.length>0&&a&&a(c)},[e,t,n,r,i,a]),p=(0,J.useCallback)(e=>{e.target.files&&(f(Array.from(e.target.files)),e.target.value=``)},[f]),m=(0,J.useCallback)(async e=>{let t=e.items.filter(e=>e.kind===`file`),n=(await Promise.allSettled(t.map(e=>e.getFile()))).filter(e=>e.status===`fulfilled`).map(e=>e.value);n.length>0&&f(n)},[f]),g=(0,J.useCallback)(t=>c?`cancel`:!e||e.length===0||e.some(e=>e.startsWith(`.`)||e.endsWith(`/*`)?!0:t.has(e))?`copy`:`cancel`,[e,c]),_=(0,J.useCallback)(()=>{c||u.current?.click()},[c]),v=s??(e&&e.length>0?`Accepted: ${e.join(`, `)}`:void 0);return B(h,{ref:d,css:Gl,onDrop:m,getDropOperation:g,isDisabled:c,...l,children:({isDropTarget:n})=>V(R,{children:[B(`input`,{ref:u,type:`file`,accept:e?.join(`,`),multiple:t,onChange:p,hidden:!0}),V(`div`,{className:`file-drop-zone__trigger`,onClick:_,children:[B(`div`,{className:`file-drop-zone__icon`,children:B(z,{svg:B(at,{})})}),B(Kt,{className:`file-drop-zone__label`,children:n?`Drop files here`:o}),v?B(Kt,{className:`file-drop-zone__description`,children:v}):null]})]})})}function Zl(e){switch(e.status){case`pending`:return`Pending`;case`uploading`:return`Uploading${e.progress===void 0?``:` ${e.progress}%`}`;case`parsing`:return`Parsing...`;case`complete`:return`Complete`;case`error`:return`Error`;default:return``}}function Ql(e){let t=(0,Y.c)(32),{file:n,onRemove:r,isDisabled:i}=e,{file:a,progress:o,status:s,error:c}=n,l=s===`uploading`&&o!==void 0,u;t[0]===Symbol.for(`react.memo_cache_sentinel`)?(u=B(`div`,{className:`file-list__icon`,children:B(z,{svg:B(pt,{})})}),t[0]=u):u=t[0];let d;t[1]===a.name?d=t[2]:(d=B(`span`,{className:`file-list__name`,title:a.name,children:a.name}),t[1]=a.name,t[2]=d);let f;t[3]===a.size?f=t[4]:(f=ql(a.size),t[3]=a.size,t[4]=f);let p;t[5]===f?p=t[6]:(p=B(`span`,{children:f}),t[5]=f,t[6]=p);let m;t[7]!==n||t[8]!==s?(m=s&&V(R,{children:[B(`span`,{children:`-`}),B(`span`,{children:Zl(n)})]}),t[7]=n,t[8]=s,t[9]=m):m=t[9];let h;t[10]!==p||t[11]!==m?(h=V(`div`,{className:`file-list__meta`,children:[p,m]}),t[10]=p,t[11]=m,t[12]=h):h=t[12];let g;t[13]===c?g=t[14]:(g=c&&B(`span`,{className:`file-list__error`,children:c}),t[13]=c,t[14]=g);let _;t[15]!==o||t[16]!==l?(_=l&&B(`div`,{className:`file-list__progress`,children:B($i,{value:o,width:`100%`,height:`4px`})}),t[15]=o,t[16]=l,t[17]=_):_=t[17];let v;t[18]!==d||t[19]!==h||t[20]!==g||t[21]!==_?(v=V(`div`,{className:`file-list__details`,children:[d,h,g,_]}),t[18]=d,t[19]=h,t[20]=g,t[21]=_,t[22]=v):v=t[22];let y;t[23]!==a||t[24]!==i||t[25]!==r||t[26]!==s?(y=r&&B(`div`,{className:`file-list__remove`,children:B(Cn,{size:`S`,"aria-label":`Remove ${a.name}`,onPress:()=>r(a),isDisabled:i||s===`uploading`||s===`parsing`,children:B(z,{svg:B(Ht,{})})})}),t[23]=a,t[24]=i,t[25]=r,t[26]=s,t[27]=y):y=t[27];let b;return t[28]!==s||t[29]!==y||t[30]!==v?(b=V(`li`,{className:`file-list__item`,"data-status":s,children:[u,v,y]}),t[28]=s,t[29]=y,t[30]=v,t[31]=b):b=t[31],b}function $l({files:e,onRemove:t,isDisabled:n,children:r,"aria-label":i=`Selected files`}){if(e.length===0)return null;let a=e=>`${e.file.name}-${e.file.size}-${e.file.lastModified}`,o=(e,i)=>r?B(J.Fragment,{children:r(e,i)},a(e)):B(Ql,{file:e,onRemove:t,isDisabled:n},a(e));return B(`ul`,{css:Kl,"aria-label":i,children:e.map((e,t)=>o(e,t))})}var eu=e=>U`
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: ${e};
  overflow: hidden;
  text-overflow: ellipsis;
`;function tu(e){let t=(0,Y.c)(5),{children:n,lines:r}=e,i;t[0]===r?i=t[1]:(i=eu(r),t[0]=r,t[1]=i);let a;return t[2]!==n||t[3]!==i?(a=B(`div`,{css:i,children:n}),t[2]=n,t[3]=i,t[4]=a):a=t[4],a}function nu(e){let t=(0,Y.c)(3),{children:n}=e,r;t[0]===Symbol.for(`react.memo_cache_sentinel`)?(r={display:`contents`},t[0]=r):r=t[0];let i;return t[1]===n?i=t[2]:(i=B(`div`,{style:r,onClick:cu,onKeyDown:su,onKeyUp:ou,onMouseDown:au,onPointerDown:iu,onPointerUp:ru,children:n}),t[1]=n,t[2]=i),i}function ru(e){return e.stopPropagation()}function iu(e){return e.stopPropagation()}function au(e){return e.stopPropagation()}function ou(e){return e.stopPropagation()}function su(e){return e.stopPropagation()}function cu(e){return e.stopPropagation()}var lu=U`
  border-radius: var(--global-dimension-size-50);
  border: 1px solid var(--global-border-color-default);
  transition: background-color 0.2s;
  &[data-clickable="true"] {
    cursor: pointer;
    &:hover {
      background-color: var(--global-color-gray-300);
    }
  }
`,uu=U`
  width: 1px;
  height: 0.7em;
  background-color: currentColor;
  opacity: 0.2;
`,du=U`
  cursor: pointer;
  border-radius: var(--global-rounding-small);
  padding: var(--global-dimension-size-25) var(--global-dimension-size-50);
  margin: calc(-1 * var(--global-dimension-size-25))
    calc(-1 * var(--global-dimension-size-50));
  transition: background-color 0.2s;
  &:hover,
  &[data-hovered] {
    background-color: var(--hover-background);
  }
`,fu=U`
  opacity: 0;

  &:hover,
  &:focus-within,
  &[data-hovered],
  &[data-focus-visible] {
    opacity: 1;
  }

  @media (hover: none) {
    opacity: 1;
  }
`,pu=U`
  display: flex;
  flex-direction: row;
  align-items: center;
  flex-wrap: wrap;
  gap: var(--global-dimension-size-50);
  min-width: 0;
  max-width: 100%;
  // the badge's reserved padding comes out of the row's width rather than
  // widening it
  box-sizing: border-box;

  &.overflow-row--collapsed {
    position: relative;
    // items that don't fit wrap to lines below the clamp and are cut off whole
    align-content: flex-start;
    overflow: clip;
  }
  &.overflow-row--overflowing {
    height: var(--overflow-row-line-height);
    // room for the badge, which sits out of flow at the end of the first line
    padding-right: var(--global-dimension-size-600);
  }

  // Not even the first item fits. The items stay in flow so they can still be
  // measured when the row is given its width back.
  &.overflow-row--badge-only {
    min-width: var(--global-dimension-size-600);
    > *:not(.overflow-row__badge-slot) {
      visibility: hidden;
    }
  }

  // Boxless, so the measurement skips the badge and the content observer can
  // tell the row's own output from its children's.
  .overflow-row__badge-slot {
    display: contents;
  }

  .overflow-row__badge {
    ${lu};
    position: absolute;
    left: var(--overflow-row-badge-left);
    top: 50%;
    transform: translateY(-50%);
    box-sizing: border-box;
    height: var(--overflow-row-line-height);
    padding: 0 var(--global-dimension-size-100);
    background-color: transparent;
    color: var(--global-text-color-700);
    font-family: inherit;
    font-size: var(--global-font-size-s);
    line-height: normal;
    &:hover {
      color: var(--global-text-color-900);
    }
    &:focus-visible {
      outline: var(--focus-ring-thickness) solid var(--focus-ring-color);
    }
  }
`,mu=1.5;function hu(e){return e.offsetWidth>0||e.offsetHeight>0}function gu(e){return Array.from(e.children).filter(e=>e instanceof HTMLElement&&hu(e))}function _u(e){let{paddingRight:t}=getComputedStyle(e);return e.clientWidth-(parseFloat(t)||0)}function vu(e){let t=gu(e),n=_u(e),r=0,i=0,a=0,o=1/0,s=-1/0;for(let e of t){let t=e.offsetTop,c=t+e.offsetHeight;if(r>0&&(t>=s||c<=o))break;let l=e.offsetLeft+e.offsetWidth;if(l>n+mu)break;r+=1,o=Math.min(o,t),s=Math.max(s,c),i=Math.max(i,l),a=Math.max(a,e.offsetHeight)}return{items:t,visibleCount:r,badgeLeft:i,lineHeight:a||(t[0]?.offsetHeight??0)}}var yu=[{name:`inert`,value:``,flag:`overflowRowInert`},{name:`aria-hidden`,value:`true`,flag:`overflowRowAriaHidden`}];function bu({items:e,visibleCount:t}){e.forEach((e,n)=>{if(n<t){xu(e);return}for(let{name:t,value:n,flag:r}of yu)e.hasAttribute(t)||(e.dataset[r]=`true`,e.setAttribute(t,n))})}function xu(e){for(let{name:t,flag:n}of yu)e.dataset[n]&&(delete e.dataset[n],e.removeAttribute(t))}function Su(e){for(let t of Array.from(e.children))t instanceof HTMLElement&&xu(t)}var Cu={childList:!0,characterData:!0,subtree:!0};function wu(e){let t=e=>(e instanceof Element?e:e.parentElement)?.closest(`.overflow-row__badge-slot`)!=null;return e.type===`childList`?[...e.addedNodes,...e.removedNodes].every(t):t(e.target)}function Tu(e,t){return e===null||t===null?e===t:e.hiddenCount===t.hiddenCount&&e.visibleCount===t.visibleCount&&e.badgeLeft===t.badgeLeft&&e.lineHeight===t.lineHeight}function Eu(e){let t=(0,Y.c)(5),{visibleCount:n,children:r}=e,i=(0,J.useRef)(null),a,o;t[0]===n?(a=t[1],o=t[2]):(a=()=>{let e=i.current;if(!e)return;let t=()=>{let t=Array.from(e.children).filter(Ou);for(let e of t)e.dataset.overflowRowHidden&&(e.style.display=``,delete e.dataset.overflowRowHidden);t.filter(hu).slice(0,n).forEach(Du)};t();let r=new MutationObserver(t);return r.observe(e,Cu),()=>r.disconnect()},o=[n],t[0]=n,t[1]=a,t[2]=o),(0,J.useLayoutEffect)(a,o);let s;return t[3]===r?s=t[4]:(s=B(W,{ref:i,direction:`row`,wrap:`wrap`,gap:`size-50`,maxWidth:`size-5000`,children:r}),t[3]=r,t[4]=s),s}function Du(e){e.style.display=`none`,e.dataset.overflowRowHidden=`true`}function Ou(e){return e instanceof HTMLElement}function ku({children:e,isExpanded:t=!1}){let n=(0,J.useRef)(null),r=(0,J.useRef)(null),[i,a]=(0,J.useState)(null);return(0,J.useLayoutEffect)(()=>{let e=n.current;if(t||!e){a(null);return}let i=null,o=()=>{i=e.getBoundingClientRect().width;let{items:t,visibleCount:n,badgeLeft:r,lineHeight:o}=vu(e);bu({items:t,visibleCount:n});let s=t.length-n,c=s===0?null:{hiddenCount:s,visibleCount:n,badgeLeft:r,lineHeight:o};a(e=>Tu(e,c)?e:c)};o(),r.current=o;let s=!1;document.fonts?.status===`loading`&&document.fonts.ready.then(()=>{s||o()});let c=new ResizeObserver(([e])=>{let t=e?.borderBoxSize?.[0]?.inlineSize??null;(t===null||t!==i)&&(i=t,o())});c.observe(e);let l=new MutationObserver(e=>{e.every(wu)||o()});return l.observe(e,Cu),()=>{s=!0,c.disconnect(),l.disconnect(),r.current=null,Su(e)}},[t]),(0,J.useLayoutEffect)(()=>{i!==null&&r.current?.()},[i]),V(`div`,{ref:n,css:pu,className:F(`overflow-row`,{"overflow-row--collapsed":!t,"overflow-row--overflowing":!t&&i!==null,"overflow-row--badge-only":!t&&i!==null&&i.visibleCount===0}),style:i===null?void 0:{"--overflow-row-badge-left":`calc(${i.badgeLeft}px + var(--global-dimension-size-50))`,"--overflow-row-line-height":`${i.lineHeight}px`},children:[e,!t&&i!==null?B(`div`,{className:`overflow-row__badge-slot`,children:V(St,{children:[V(xt,{className:`overflow-row__badge`,"data-clickable":`true`,"aria-label":`Show ${i.hiddenCount} more`,children:[`+`,i.hiddenCount]}),B(nu,{children:V(tr,{placement:`bottom end`,children:[B(zt,{}),B(xn,{children:B(ta,{padding:`size-150`,children:B(Eu,{visibleCount:i.visibleCount,children:e})})})]})})]})}):null]})}var Au=U`
  text-overflow: ellipsis;
  overflow: hidden;
  white-space: nowrap;
`,ju=U`
  display: -webkit-box;
  -webkit-box-orient: vertical;
  overflow: hidden;
`,Mu=e=>{let t=(0,Y.c)(11),{children:n,maxWidth:r,title:i,maxLines:a}=e,o=(a??0)>1,s=o?ju:Au,c;t[0]!==o||t[1]!==a?(c=o&&{WebkitLineClamp:a},t[0]=o,t[1]=a,t[2]=c):c=t[2];let l;t[3]!==r||t[4]!==c?(l={maxWidth:r,...c},t[3]=r,t[4]=c,t[5]=l):l=t[5];let u;return t[6]!==n||t[7]!==s||t[8]!==l||t[9]!==i?(u=B(`div`,{css:s,style:l,title:i,children:n}),t[6]=n,t[7]=s,t[8]=l,t[9]=i,t[10]=u):u=t[10],u};function Nu(){let e=(0,Y.c)(3),t,n;e[0]===Symbol.for(`react.memo_cache_sentinel`)?(t=B(Cn,{slot:`previous`,size:`S`,children:B(z,{svg:B(cn,{})})}),n=B(Ut,{className:`calendar__heading`}),e[0]=t,e[1]=n):(t=e[0],n=e[1]);let r;return e[2]===Symbol.for(`react.memo_cache_sentinel`)?(r=V(`header`,{className:`calendar__header`,children:[t,n,B(Cn,{slot:`next`,size:`S`,children:B(z,{svg:B(er,{})})})]}),e[2]=r):r=e[2],r}function Pu(e){let t=(0,Y.c)(8),{months:n,errorMessage:r}=e,i;t[0]===Symbol.for(`react.memo_cache_sentinel`)?(i=B(Nu,{}),t[0]=i):i=t[0];let a;t[1]===n?a=t[2]:(a=B(`div`,{className:`calendar__months`,children:Array.from({length:n},Fu)}),t[1]=n,t[2]=a);let o;t[3]===r?o=t[4]:(o=r&&B(Kt,{slot:`errorMessage`,children:r}),t[3]=r,t[4]=o);let s;return t[5]!==a||t[6]!==o?(s=V(R,{children:[i,a,o]}),t[5]=a,t[6]=o,t[7]=s):s=t[7],s}function Fu(e,t){return B(j,{offset:{months:t},children:Iu},t)}function Iu(e){return B(Ce,{date:e})}var Lu=U`
  --calendar-cell-size: var(--global-dimension-size-400);
  --calendar-cell-background-color-hover: var(
    --global-menu-item-background-color-hover
  );
  --calendar-cell-background-color-selected: var(--global-color-primary);
  --calendar-cell-foreground-color-selected: var(--global-color-gray-75);
  --calendar-cell-background-color-highlighted: var(--highlight-background);
  --calendar-cell-foreground-color-highlighted: var(--highlight-foreground);

  display: flex;
  flex-direction: column;
  gap: var(--global-dimension-size-100);
  width: max-content;
  color: var(--global-text-color-900);

  .calendar__header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: var(--global-dimension-size-100);
  }

  .calendar__heading {
    flex: 1;
    margin: 0;
    text-align: center;
    font-size: var(--global-font-size-m);
    font-weight: 600;
  }

  .calendar__months {
    display: flex;
    gap: var(--global-dimension-size-300);
  }

  .react-aria-CalendarGrid {
    border-spacing: 0;
    /* Dragging across days selects a range; never native text selection. */
    user-select: none;
    -webkit-user-select: none;
  }

  .react-aria-CalendarHeaderCell {
    padding-bottom: var(--global-dimension-size-50);
    color: var(--global-text-color-500);
    font-size: var(--global-font-size-xs);
    font-weight: 600;
  }

  .react-aria-CalendarCell {
    width: var(--calendar-cell-size);
    height: var(--calendar-cell-size);
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: var(--global-rounding-small);
    font-size: var(--global-font-size-s);
    font-variant-numeric: tabular-nums;
    cursor: pointer;
    outline: none;
    forced-color-adjust: none;
    -webkit-tap-highlight-color: transparent;

    &[data-outside-month] {
      display: none;
    }

    &[data-hovered] {
      background: var(--calendar-cell-background-color-hover);
    }

    &[data-focus-visible] {
      outline: var(--focus-ring-thickness) solid var(--focus-ring-color);
      outline-offset: calc(-1 * var(--focus-ring-thickness));
    }

    &[data-selected] {
      background: var(--calendar-cell-background-color-selected);
      color: var(--calendar-cell-foreground-color-selected);
    }

    &[data-disabled] {
      color: var(--global-text-color-300);
      cursor: not-allowed;
    }

    &[data-unavailable] {
      color: var(--global-color-danger);
      text-decoration: line-through;
      cursor: not-allowed;
    }

    &[data-invalid] {
      background: var(--global-color-danger);
      color: var(--global-static-color-white-900);
    }
  }

  [slot="errorMessage"] {
    color: var(--global-color-danger);
    font-size: var(--global-font-size-xs);
  }
`,Ru=U`
  .react-aria-CalendarCell {
    &[data-selected] {
      background: var(--calendar-cell-background-color-highlighted);
      color: var(--calendar-cell-foreground-color-highlighted);
      border-radius: 0;
    }

    &[data-selection-start],
    &[data-selection-end] {
      background: var(--calendar-cell-background-color-selected);
      color: var(--calendar-cell-foreground-color-selected);
    }

    &[data-selection-start] {
      border-start-start-radius: var(--global-rounding-small);
      border-end-start-radius: var(--global-rounding-small);
    }

    &[data-selection-end] {
      border-start-end-radius: var(--global-rounding-small);
      border-end-end-radius: var(--global-rounding-small);
    }

    &[data-invalid] {
      background: rgba(var(--global-color-red-700-rgb), 0.2);
      color: var(--global-color-danger);
    }
  }
`,zu=U`
  --date-field-vertical-padding: 6px;
  --date-field-horizontal-padding: 8px;
  color: var(--global-text-color-900);

  &[data-size="S"] .react-aria-DateInput {
    height: var(--global-input-height-s);
  }

  &[data-size="M"] .react-aria-DateInput {
    height: var(--global-input-height-m);
  }

  .react-aria-DateInput {
    display: flex;
    padding: var(--date-field-vertical-padding)
      var(--date-field-horizontal-padding);
    border: var(--global-border-size-thin) solid
      var(--global-input-field-border-color);
    border-radius: var(--global-rounding-small);
    background-color: var(--global-input-field-background-color);
    width: fit-content;
    box-sizing: border-box;
    min-width: 150px;
    white-space: nowrap;
    forced-color-adjust: none;

    &[data-focus-within] {
      border-color: var(--global-input-field-border-color-active);
    }

    &[data-focus-visible] {
      outline: var(--focus-ring-thickness) solid var(--focus-ring-color);
      outline-offset: calc(-1 * var(--focus-ring-thickness));
    }

    &[data-invalid] {
      border-color: var(--global-color-danger);
    }
  }

  .react-aria-DateSegment {
    padding: 0 2px;
    font-variant-numeric: tabular-nums;
    text-align: end;
    color: var(--global-text-color-900);

    &[data-type="literal"] {
      padding: 0;
      /* Preserve the locale separator (e.g. ", ") that flex would collapse. */
      white-space: pre;
    }

    &[data-placeholder] {
      color: var(--text-color-placeholder);
      font-style: italic;
    }

    &:focus {
      color: var(--highlight-foreground);
      background: var(--highlight-background);
      outline: none;
      border-radius: var(--global-rounding-small);
      caret-color: transparent;
    }
  }
`;function Bu(e){let t=(0,Y.c)(10),n,r,a,o;if(t[0]!==e){let{ref:s,...c}=e;r=s;let{css:l,...u}=c;a=u,n=i,o=U(ss,zu,l),t[0]=e,t[1]=n,t[2]=r,t[3]=a,t[4]=o}else n=t[1],r=t[2],a=t[3],o=t[4];let s;return t[5]!==n||t[6]!==r||t[7]!==a||t[8]!==o?(s=B(n,{css:o,...a,"data-size":`S`,ref:r}),t[5]=n,t[6]=r,t[7]=a,t[8]=o,t[9]=s):s=t[9],s}function Vu(e){let t=(0,Y.c)(17),n,r,i,a,o;t[0]===e?(n=t[1],r=t[2],i=t[3],a=t[4],o=t[5]):({errorMessage:r,css:i,children:n,ref:a,...o}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a,t[5]=o);let s=e.visibleDuration?.months||1,c;t[6]===i?c=t[7]:(c=U(Lu,Ru,i),t[6]=i,t[7]=c);let l;t[8]!==n||t[9]!==r||t[10]!==s?(l=n??B(Pu,{months:s,errorMessage:r}),t[8]=n,t[9]=r,t[10]=s,t[11]=l):l=t[11];let u;return t[12]!==a||t[13]!==o||t[14]!==c||t[15]!==l?(u=B(je,{ref:a,css:c,...o,children:l}),t[12]=a,t[13]=o,t[14]=c,t[15]=l,t[16]=u):u=t[16],u}U`
  --date-field-vertical-padding: 6px;
  --date-field-horizontal-padding: 8px;
  color: var(--global-text-color-900);

  .react-aria-DateInput {
    display: flex;
    padding: var(--date-field-vertical-padding)
      var(--date-field-horizontal-padding);
    border: var(--global-border-size-thin) solid
      var(--global-input-field-border-color);
    border-radius: var(--global-rounding-small);
    background-color: var(--global-input-field-background-color);
    width: fit-content;
    min-width: 150px;
    white-space: nowrap;
    forced-color-adjust: none;

    &[data-focus-within] {
      border-color: var(--global-input-field-border-color-active);
    }

    &[data-focus-visible] {
      outline: var(--focus-ring-thickness) solid var(--focus-ring-color);
      outline-offset: calc(-1 * var(--focus-ring-thickness));
    }
  }

  .react-aria-DateSegment {
    padding: 0 2px;
    font-variant-numeric: tabular-nums;
    text-align: end;
    color: var(--global-text-color-900);

    &[data-type="literal"] {
      padding: 0;
    }

    &[data-placeholder] {
      color: var(--text-color-placeholder);
      font-style: italic;
    }

    &:focus {
      color: var(--highlight-foreground);
      background: var(--highlight-background);
      outline: none;
      border-radius: var(--global-rounding-small);
      caret-color: transparent;
    }
  }
`;var Hu=U`
  font-family: var(--global-font-family-mono);
  font-variant-numeric: tabular-nums;
  ${tt};
`;function Uu(e){return e.toString().padStart(2,`0`)}function Wu(e){let t=Math.floor(e/3600),n=Math.floor(e%3600/60),r=e%60;return t>0?`${Uu(t)}:${Uu(n)}:${Uu(r)}`:`${Uu(n)}:${Uu(r)}`}function Gu(e){return Math.max(0,Math.floor((Date.now()-e.getTime())/1e3))}function Ku(e){let{startTime:t,color:n=`text-900`,size:r=`S`}=e,i=(0,J.useMemo)(()=>t??new Date,[t]),[a,o]=(0,J.useState)(()=>Gu(i));return(0,J.useEffect)(()=>{o(Gu(i));let e=setInterval(()=>{o(Gu(i))},1e3);return()=>clearInterval(e)},[i]),B(`time`,{css:Hu,"data-size":r,style:{color:Nt(n)},dateTime:`PT${a}S`,children:Wu(a)})}var qu=2e3,Ju=U`
  all: unset;
  display: inline-flex;
  cursor: pointer;
  &:focus-visible {
    outline: var(--focus-ring-thickness) solid var(--focus-ring-color);
    outline-offset: var(--focus-ring-offset);
    border-radius: var(--global-badge-border-radius);
  }
  &[data-hovered] .id-badge__copy-icon {
    color: var(--global-text-color-900);
  }
  .id-badge__copy-icon {
    font-size: 12px;
    color: var(--global-text-color-500);
    transition: color 0.2s;
  }
  &[data-variant="quiet"] {
    align-items: center;
    gap: var(--global-dimension-size-50);
    ${du}
  }
`,Yu=({id:e,size:t=`S`,tooltipText:n=`Copy ID`,variant:r=`badge`})=>{let[i,a]=(0,J.useState)(!1),o=B(z,{className:`id-badge__copy-icon`,color:i?`success`:`inherit`,svgKey:i?`Checkmark`:`Duplicate`});return V(Se,{children:[B(xt,{css:Ju,"data-variant":r,"aria-label":`${n} ${e}`,onPress:()=>{ze(e),a(!0),setTimeout(()=>{a(!1)},qu)},children:r===`badge`?V(es,{size:t,children:[B(z,{svgKey:`ID`}),B(L,{fontFamily:`mono`,size:`S`,color:`text-700`,children:e}),o]}):V(R,{children:[B(L,{fontFamily:`mono`,size:`S`,color:`text-500`,children:e}),o]})}),B(ia,{offset:1,children:i?`Copied`:n})]})},Xu=e=>{let t=(0,Y.c)(7),{title:n,id:r}=e,i;t[0]===n?i=t[1]:(i=B(ot,{children:n}),t[0]=n,t[1]=i);let a;t[2]===r?a=t[3]:(a=B(Yu,{size:`S`,id:r}),t[2]=r,t[3]=a);let o;return t[4]!==i||t[5]!==a?(o=V(W,{direction:`row`,gap:`size-100`,alignItems:`center`,children:[i,a]}),t[4]=i,t[5]=a,t[6]=o):o=t[6],o},Zu=`selectedSpanNodeId`,Qu=`spanFilterCondition`,$u=`sessionView`,ed=`selectedTraceId`,td=[ed,Zu],nd=`timeRangeKey`,rd=`timeRangeStart`,id=`timeRangeEnd`,ad=`labelId`,od=`createCodeEvaluator`,sd=`createLlmEvaluator`,cd=[{key:`15m`,label:`Last 15 Min`},{key:`1h`,label:`Last Hour`},{key:`12h`,label:`Last 12 Hours`},{key:`1d`,label:`Last Day`},{key:`7d`,label:`Last 7 Days`},{key:`30d`,label:`Last Month`}],ld=cd.reduce((e,t)=>({...e,[t.key]:t}),{}),ud=6e4,dd=60*ud,fd=24*dd,pd=/^(\d+)([mhd])$/;function md(e){if(typeof e!=`string`)return null;let t=pd.exec(e);if(!t)return null;let n=parseInt(t[1],10);return n<1?null:{quantity:n,unit:t[2]}}function hd({quantity:e,unit:t}){switch(t){case`m`:return e*ud;case`h`:return e*dd;case`d`:return e*fd;default:return fr(t)}}function gd(e,t=Date.now()){let n=md(e);if(!n)throw Error(`Invalid last N time range key: ${e}`);let{quantity:r,unit:i}=n,a;switch(i){case`m`:a=Ie(t,r);break;case`h`:a=Ue(t,r);break;case`d`:a=te(t,r);break;default:fr(i)}return{start:(hd(n)<=dd?Ve:x)(a),end:null}}function _d(e){let t=md(e),n=t&&hd(t)<=dd?ud:dd,r=Date.now()%n;return r===0?n:n-r}function vd(e){return md(e)!==null}function yd(e){if(e==null||e.trim()===``)return null;let t=new Date(e);return Number.isNaN(t.getTime())?void 0:t}function bd(e,t=Date.now()){let n=e.get(nd);if(vd(n))return{timeRangeKey:n,...gd(n,t)};let r=yd(e.get(rd)),i=yd(e.get(id));return r===void 0||i===void 0||r==null&&i==null||r!=null&&i!=null&&r>i?null:{timeRangeKey:`custom`,start:r,end:i}}function xd({searchParams:e,timeRange:t}){let n=new URLSearchParams(e),r=(e,t)=>{t==null?n.delete(e):n.set(e,t.toISOString())};return vd(t.timeRangeKey)?(n.set(nd,t.timeRangeKey),n.delete(rd),n.delete(id),n):(n.delete(nd),r(rd,t.start),r(id,t.end),n)}function Sd(e){let t=xd({searchParams:new URLSearchParams,timeRange:e}).toString();return t?`?${t}`:``}var Cd={m:{singular:`minute`,plural:`minutes`},h:{singular:`hour`,plural:`hours`},d:{singular:`day`,plural:`days`}};function wd(e){let t=ld[e];if(t)return t.label;let n=md(e);if(!n)return e;let{quantity:r,unit:i}=n,{singular:a,plural:o}=Cd[i];return`Last ${r} ${r===1?a:o}`}var Td=/^(?:last\s+)?(\d+)\s*(m|min|mins|minute|minutes|h|hr|hrs|hour|hours|d|day|days)$/,Ed=/^(?:last\s+)?(\d+)$/;function Dd(e){let t=Td.exec(e.trim().toLowerCase());if(!t)return null;let n=parseInt(t[1],10);return n<1?null:`${n}${t[2][0]}`}function Od(e){let t=Dd(e);if(t)return[t];let n=Ed.exec(e.trim().toLowerCase());if(!n)return[];let r=parseInt(n[1],10);return r<1?[]:[`${r}m`,`${r}h`,`${r}d`]}var kd=.5,Ad=2,jd=ud;function Md({value:e,now:t}){if(!e.start)return null;let n=e.start.getTime(),r=(e.end??t).getTime(),i=r-n;return i<=0?null:{startMs:n,endMs:r,durationMs:i}}function Nd(e){let t=Math.max(1,Math.round(e/ud)),n=t/1440;if(n>=2||Number.isInteger(n))return`${Math.round(n)}d`;let r=t/60;return r>=2||Number.isInteger(r)?`${Math.round(r)}h`:`${t}m`}function Pd({value:e,now:t=new Date,shiftFraction:n=kd}){let r=Md({value:e,now:t});if(!r)return null;let i=r.durationMs*n;return{timeRangeKey:`custom`,start:new Date(r.startMs-i),end:new Date(r.endMs-i)}}function Fd({value:e,now:t=new Date,shiftFraction:n=kd}){if(!e.end)return null;let r=Md({value:e,now:t});if(!r)return null;let i=Math.min(r.durationMs*n,t.getTime()-r.endMs);return i<=0?null:{timeRangeKey:`custom`,start:new Date(r.startMs+i),end:new Date(r.endMs+i)}}function Id({value:e,now:t=new Date,zoomFactor:n=Ad,minWindowMs:r=jd}){return Rd({value:e,now:t,factor:1/n,minWindowMs:r})}function Ld({value:e,now:t=new Date,zoomFactor:n=Ad,minWindowMs:r=jd}){return Rd({value:e,now:t,factor:n,minWindowMs:r})}function Rd({value:e,now:t,factor:n,minWindowMs:r}){if(!e.end){let i=md(e.timeRangeKey),a=i?hd(i):Md({value:e,now:t})?.durationMs;if(a==null)return null;let o=Math.max(a*n,r);if(n<1&&o>=a)return null;let s=Nd(o);return s===e.timeRangeKey?null:{timeRangeKey:s,...gd(s)}}let i=Md({value:e,now:t});if(!i)return null;let a=Math.max(i.durationMs*n,r);if(n<1?a>=i.durationMs:a===i.durationMs)return null;let o=(i.startMs+i.endMs)/2,s=o-a/2,c=o+a/2,l=c-t.getTime();return l>0&&(s-=l,c-=l),{timeRangeKey:`custom`,start:new Date(s),end:new Date(c)}}function zd(e,t){return e?Ee(e,t):null}var Bd=U`
  display: flex;
  flex-direction: column;
  gap: var(--global-dimension-size-200);
  padding: var(--global-dimension-size-200);

  .time-range-calendar-picker__fields {
    display: grid;
    /* Mirror the two month grids so each field sits squarely under a month. */
    grid-template-columns: 1fr 1fr;
    gap: var(--global-dimension-size-300);
  }

  .time-range-calendar-picker__controls {
    display: flex;
    align-items: center;
    justify-content: flex-end;
    gap: var(--global-dimension-size-100);
  }

  .time-range-calendar-picker__error {
    margin-right: auto;
  }
`,Vd=U`
  .react-aria-DateInput {
    width: 100%;
    min-width: 0;
  }
`,Hd=new re(0,0,0),Ud=new re(23,59,59);function Wd(e){let t=(0,Y.c)(56),{value:n,timeZone:r,onApply:i,onCancel:a}=e,o;t[0]!==r||t[1]!==n.start?(o=()=>zd(n.start,r),t[0]=r,t[1]=n.start,t[2]=o):o=t[2];let[s,c]=(0,J.useState)(o),l;t[3]!==r||t[4]!==n.end?(l=()=>zd(n.end,r)??ve(r),t[3]=r,t[4]=n.end,t[5]=l):l=t[5];let[u,d]=(0,J.useState)(l),f;t[6]!==s||t[7]!==r?(f=s?s.toDate(r):null,t[6]=s,t[7]=r,t[8]=f):f=t[8];let p=f,m;t[9]!==u||t[10]!==r?(m=u?u.toDate(r):null,t[9]=u,t[10]=r,t[11]=m):m=t[11];let h=m,g=!!(p&&h&&p>h),_;t[12]!==h||t[13]!==g||t[14]!==p?(_=p&&h&&!g?{start:p,end:h}:null,t[12]=h,t[13]=g,t[14]=p,t[15]=_):_=t[15];let v=_,y;t[16]!==u||t[17]!==g||t[18]!==s?(y=s&&u&&!g?{start:ae(s),end:ae(u)}:null,t[16]=u,t[17]=g,t[18]=s,t[19]=y):y=t[19];let b=y,x;t[20]===Symbol.for(`react.memo_cache_sentinel`)?(x={months:2},t[20]=x):x=t[20];let S;t[21]===r?S=t[22]:(S=e=>{e&&(c(Pe(ce(e.start,Hd),r)),d(Pe(ce(e.end,Ud),r)))},t[21]=r,t[22]=S);let C;t[23]!==b||t[24]!==S?(C=B(Vu,{"aria-label":`Time range`,visibleDuration:x,value:b,onChange:S}),t[23]=b,t[24]=S,t[25]=C):C=t[25];let w,T;t[26]===Symbol.for(`react.memo_cache_sentinel`)?(T=B(Sn,{children:`Start`}),w=B(We,{children:Kd}),t[26]=w,t[27]=T):(w=t[26],T=t[27]);let E;t[28]===s?E=t[29]:(E=V(Bu,{granularity:`minute`,hideTimeZone:!0,value:s,onChange:c,css:Vd,children:[T,w]}),t[28]=s,t[29]=E);let D,O;t[30]===Symbol.for(`react.memo_cache_sentinel`)?(D=B(Sn,{children:`End`}),O=B(We,{children:Gd}),t[30]=D,t[31]=O):(D=t[30],O=t[31]);let k;t[32]!==u||t[33]!==g?(k=V(Bu,{granularity:`minute`,hideTimeZone:!0,isInvalid:g,value:u,onChange:d,css:Vd,children:[D,O]}),t[32]=u,t[33]=g,t[34]=k):k=t[34];let A;t[35]!==E||t[36]!==k?(A=V(`div`,{className:`time-range-calendar-picker__fields`,children:[E,k]}),t[35]=E,t[36]=k,t[37]=A):A=t[37];let j;t[38]===g?j=t[39]:(j=g&&B(L,{size:`XS`,color:`danger`,className:`time-range-calendar-picker__error`,children:`End must be after the start`}),t[38]=g,t[39]=j);let M;t[40]===a?M=t[41]:(M=B(H,{size:`S`,onPress:a,children:`Cancel`}),t[40]=a,t[41]=M);let ee=!v,te;t[42]!==v||t[43]!==i?(te=()=>{v&&i(v)},t[42]=v,t[43]=i,t[44]=te):te=t[44];let ne;t[45]!==ee||t[46]!==te?(ne=B(H,{"data-testid":`time-range-calendar-picker-apply-button`,size:`S`,variant:`primary`,isDisabled:ee,onPress:te,children:`Apply`}),t[45]=ee,t[46]=te,t[47]=ne):ne=t[47];let N;t[48]!==j||t[49]!==M||t[50]!==ne?(N=V(`div`,{className:`time-range-calendar-picker__controls`,children:[j,M,ne]}),t[48]=j,t[49]=M,t[50]=ne,t[51]=N):N=t[51];let re;return t[52]!==A||t[53]!==N||t[54]!==C?(re=V(`div`,{"data-testid":`time-range-calendar-picker`,className:`time-range-calendar-picker`,css:Bd,children:[C,A,N]}),t[52]=A,t[53]=N,t[54]=C,t[55]=re):re=t[55],re}function Gd(e){return B(y,{segment:e})}function Kd(e){return B(y,{segment:e})}var qd=`set_time_range`,Jd=[`15m`,`1h`,`12h`,`1d`,`7d`,`30d`,`custom`];function Yd(e){return typeof e==`string`&&Jd.includes(e)}function Xd(e){if(typeof e!=`object`||!e)return null;let t=e;return!Yd(t.timeRangeKey)||t.startTime!==void 0&&typeof t.startTime!=`string`||t.endTime!==void 0&&typeof t.endTime!=`string`?null:{timeRangeKey:t.timeRangeKey,...t.startTime===void 0?{}:{startTime:t.startTime},...t.endTime===void 0?{}:{endTime:t.endTime}}}function Zd(e,t){return typeof e==`function`?e(t):e}function Qd(e){return{name:e.name,uiBehavior:e.uiBehavior,requiredCapabilities:e.requiredCapabilities,rehydratable:e.rehydratable,dispatch:async t=>{let n=e.parseInput(t.toolCall.input);if(n==null){await t.addToolOutput({state:`output-error`,tool:e.name,toolCallId:t.toolCall.toolCallId,errorText:Zd(e.invalidInputErrorText,t.toolCall.input)});return}await e.execute({...t,input:n})}}}async function $d({toolName:e,toolCall:t,sessionId:n,addToolOutput:r,errorText:i}){return n??(await r({state:`output-error`,tool:e,toolCallId:t.toolCallId,errorText:i}),null)}async function ef({result:e,toolName:t,toolCallId:n,addToolOutput:r,defaultSuccessOutput:i,emitSuccess:a}){if(e.ok){if(!a)return;await r({state:`output-available`,tool:t,toolCallId:n,output:e.output??i});return}await r({state:`output-error`,tool:t,toolCallId:n,errorText:e.error})}function tf(e){let t=e.emitSuccess??!0,n=e.defaultSuccessOutput??`Done.`;return Qd({name:e.name,parseInput:e.parseInput,invalidInputErrorText:e.invalidInputErrorText,requiredCapabilities:e.requiredCapabilities,uiBehavior:e.uiBehavior,execute:async({toolCall:r,input:i,sessionId:a,addToolOutput:o,agentStore:s})=>{let c=s.getState().registeredClientActions[e.name];if(!c){await o({state:`output-error`,tool:e.name,toolCallId:r.toolCallId,errorText:e.notMountedErrorText});return}e.requireSession&&await $d({toolName:e.name,toolCall:r,sessionId:a,addToolOutput:o,errorText:e.noSessionErrorText??`Cannot run this tool without an active session.`})==null||await ef({result:e.buildContext?await c(i,e.buildContext({toolCall:r,sessionId:a,addToolOutput:o,agentStore:s})):await c(i),toolName:e.name,toolCallId:r.toolCallId,addToolOutput:o,defaultSuccessOutput:n,emitSuccess:t})}})}var nf=tf({name:qd,parseInput:Xd,invalidInputErrorText:`Invalid ${qd} input. Expected { timeRangeKey: ${Jd.map(e=>`"${e}"`).join(` | `)}, startTime?: string, endTime?: string }.`,notMountedErrorText:`The app time range selector is not mounted on this page; cannot update the time range.`,defaultSuccessOutput:`Time range updated.`});function rf(e){switch(e.type){case`app`:return`app`;case`playground`:return`playground`;case`code_evaluator`:return e.evaluatorNodeId?`code_evaluator:${e.evaluatorNodeId}`:`code_evaluator:create`;case`llm_evaluator`:return e.evaluatorNodeId?`llm_evaluator:${e.evaluatorNodeId}`:`llm_evaluator:create`;case`dataset`:return e.datasetVersionNodeId?`dataset:${e.datasetNodeId}:${e.datasetVersionNodeId}`:`dataset:${e.datasetNodeId}`;case`project`:return`project:${e.projectNodeId}`;case`trace`:return`trace:${e.projectNodeId}:${e.otelTraceId}`;case`session`:return`session:${e.projectNodeId}:${e.sessionNodeId}`;case`prompt`:return`prompt:${e.promptNodeId}`;case`prompt_version`:return`prompt_version:${e.promptNodeId}:${e.promptVersionNodeId}`;case`span`:return`span:${e.projectNodeId??``}:${e.spanNodeId?`node:${e.spanNodeId}`:`otel:${e.otelSpanId}`}`;case`graphql`:return`graphql`;case`web_access`:return`web_access`;case`subagents`:return`subagents`;default:return fr(e)}}var af={"graphql.mutations":!1,"subagents.enabled":!1,"web.access":!1},of=[{key:`graphql.mutations`,label:`Dangerously enable mutations`,description:`Allows the phoenix-gql bash command to execute GraphQL mutations in addition to queries.`,defaultValue:!1,scope:`global`,controlSurface:`experimental-settings`},{key:`subagents.enabled`,label:`Subagents`,description:`Lets the assistant delegate work to subagents that run their own tool-using turns. Experimental and may consume large numbers of tokens.`,defaultValue:!1,scope:`global`},{key:`web.access`,label:`Web search`,description:`Lets the assistant use provider-native web search and URL fetching when the selected model supports it.`,defaultValue:!1,scope:`global`}],sf=Object.fromEntries(of.map(e=>[e.key,e]));for(let e of Object.keys(af))if(!sf[e])throw Error(`Missing AGENT_CAPABILITY_DEFINITIONS entry for capability key: "${e}"`);function cf(){return{...af}}function lf(e){return sf[e]}function uf(e){return of.filter(t=>t.controlSurface===e)}function df(e){return e.map(e=>e.toLowerCase())}var ff=[`NONE`,`MINIMAL`,`LOW`,`MEDIUM`,`HIGH`,`XHIGH`],pf=df(ff),mf=Object.fromEntries(ff.map(e=>[e,e.toLowerCase()]));function hf(e){return e in mf}function gf(e){if(typeof e!=`string`)return;let t=e.trim();if(!t)return;let n=t.toUpperCase();if(hf(n))return n}function _f(e){let t=gf(e);if(t!=null)return mf[t]}var vf=[`disabled`,`enabled`,`adaptive`],yf=[`SUMMARIZED`,`OMITTED`],bf=df(yf),xf=[`LOW`,`MEDIUM`,`HIGH`,`XHIGH`,`MAX`],Sf=df(xf),Cf=[`MINIMAL`,`LOW`,`MEDIUM`,`HIGH`],wf=df(Cf),Z={OPENAI:`openai`,ANTHROPIC:`anthropic`,GOOGLE_GENAI:`google_genai`,AWS_BEDROCK:`aws_bedrock`};function Tf(e){switch(e){case`OPENAI`:case`AZURE_OPENAI`:case`DEEPSEEK`:case`XAI`:case`OLLAMA`:case`CEREBRAS`:case`FIREWORKS`:case`GROQ`:case`MOONSHOT`:case`PERPLEXITY`:case`TOGETHER`:return Z.OPENAI;case`ANTHROPIC`:return Z.ANTHROPIC;case`GOOGLE`:return Z.GOOGLE_GENAI;case`AWS`:return Z.AWS_BEDROCK}return fr(e)}var Ef=[{name:`temperature`,type:`float`,min:0,max:2,label:`Temperature`,canonicalName:`TEMPERATURE`},{name:`topP`,type:`float`,min:0,max:1,label:`Top P`,canonicalName:`TOP_P`},{name:`maxCompletionTokens`,type:`int`,label:`Max Completion Tokens`,canonicalName:`MAX_COMPLETION_TOKENS`},{name:`frequencyPenalty`,type:`float`,min:-2,max:2,label:`Frequency Penalty`,applicableOpenAIApiTypes:[`CHAT_COMPLETIONS`]},{name:`presencePenalty`,type:`float`,min:-2,max:2,label:`Presence Penalty`,applicableOpenAIApiTypes:[`CHAT_COMPLETIONS`]},{name:`reasoningEffort`,type:`enum`,values:pf,label:`Reasoning Effort`,canonicalName:`REASONING_EFFORT`},{name:`seed`,type:`int`,label:`Seed`,canonicalName:`RANDOM_SEED`}],Df=[{name:`maxTokens`,type:`int`,label:`Max Tokens`,required:!0,canonicalName:`MAX_COMPLETION_TOKENS`},{name:`temperature`,type:`float`,min:0,max:1,label:`Temperature`,canonicalName:`TEMPERATURE`},{name:`stopSequences`,type:`string_list`,label:`Stop Sequences`,canonicalName:`STOP_SEQUENCES`},{name:`topP`,type:`float`,min:0,max:1,label:`Top P`,canonicalName:`TOP_P`},{name:`thinkingType`,type:`enum`,values:vf,label:`Thinking`,canonicalName:`ANTHROPIC_EXTENDED_THINKING`},{name:`thinkingBudgetTokens`,type:`int`,min:1024,label:`Budget Tokens`},{name:`thinkingDisplay`,type:`enum`,values:bf,label:`Thinking Display`},{name:`effort`,type:`enum`,values:Sf,label:`Effort`,canonicalName:`REASONING_EFFORT`}],Of=[{name:`temperature`,type:`float`,min:0,max:2,label:`Temperature`,canonicalName:`TEMPERATURE`},{name:`maxOutputTokens`,type:`int`,label:`Max Output Tokens`,canonicalName:`MAX_COMPLETION_TOKENS`},{name:`stopSequences`,type:`string_list`,label:`Stop Sequences`,canonicalName:`STOP_SEQUENCES`},{name:`presencePenalty`,type:`float`,label:`Presence Penalty`},{name:`frequencyPenalty`,type:`float`,label:`Frequency Penalty`},{name:`topP`,type:`float`,min:0,max:1,label:`Top P`,canonicalName:`TOP_P`},{name:`topK`,type:`int`,label:`Top K`},{name:`thinkingBudget`,type:`int`,min:0,label:`Thinking Budget`},{name:`thinkingLevel`,type:`enum`,values:wf,label:`Thinking Level`},{name:`includeThoughts`,type:`bool`,label:`Include Thoughts`}],kf=[{name:`maxTokens`,type:`int`,label:`Max Tokens`,canonicalName:`MAX_COMPLETION_TOKENS`},{name:`temperature`,type:`float`,min:0,max:1,label:`Temperature`,canonicalName:`TEMPERATURE`},{name:`topP`,type:`float`,min:0,max:1,label:`Top P`,canonicalName:`TOP_P`}];Z.OPENAI,Z.ANTHROPIC,Z.GOOGLE_GENAI,Z.AWS_BEDROCK;var Af=1024,jf=2e3,Mf={type:`adaptive`,display:`SUMMARIZED`},Nf=`HIGH`,Pf=q().transform(e=>e.toUpperCase()).pipe(nr(yf)).optional().catch(void 0),Ff=q().transform(e=>e.toUpperCase()).pipe(nr(xf)).optional().catch(void 0),If=ir(q()).optional().catch(void 0),Lf=ar(q(),sr()).optional().catch(void 0),Rf=ur(`type`,[G({type:rr(`disabled`)}),G({type:rr(`enabled`),budgetTokens:K(),display:Pf}),G({type:rr(`adaptive`),display:Pf})]).optional().catch(void 0),zf=ur(`type`,[G({type:rr(`disabled`)}),G({type:rr(`enabled`),budget_tokens:K(),display:Pf}),G({type:rr(`adaptive`),display:Pf})]).optional().catch(void 0);function Bf(e){if(e)switch(e.type){case`disabled`:return{type:`disabled`};case`enabled`:{let t={type:`enabled`,budgetTokens:e.budget_tokens};return e.display!==void 0&&(t.display=e.display),t}case`adaptive`:{let t={type:`adaptive`};return e.display!==void 0&&(t.display=e.display),t}default:return fr(e)}}function Vf(e){return e?.type===`enabled`||e?.type===`adaptive`}function Hf(){return{maxTokens:jf,thinking:Mf,effort:Nf}}function Uf(e){if(e==null)return Df;let t=Vf(e.thinking);return Df.flatMap(n=>{let r=`canonicalName`in n?n.canonicalName:null;return t&&(r===`TEMPERATURE`||r===`TOP_P`)?[]:n.name===`thinkingBudgetTokens`?e.thinking?.type===`enabled`?n.type===`int`?[{...n,max:e.maxTokens-1}]:[n]:[]:n.name===`thinkingDisplay`&&!t?[]:[n]})}var Wf=or({maxTokens:K().optional().catch(void 0),temperature:K().optional().catch(void 0),topP:K().optional().catch(void 0),stopSequences:If,thinking:Rf,effort:Ff,extraBody:Lf});function Gf(e){let t=Wf.safeParse(e),n=t.success?t.data:{},r={maxTokens:n.maxTokens??2e3};return n.temperature!==void 0&&(r.temperature=n.temperature),n.topP!==void 0&&(r.topP=n.topP),n.stopSequences!==void 0&&(r.stopSequences=[...n.stopSequences]),n.thinking!==void 0&&(r.thinking=n.thinking),n.effort!==void 0&&(r.effort=n.effort),n.extraBody!==void 0&&(r.extraBody={...n.extraBody}),r}function Q(e){if(!Vf(e.thinking)||e.temperature===void 0&&e.topP===void 0)return e;let t={...e};return delete t.temperature,delete t.topP,t}function Kf(e){let t=[];if(e.thinking?.type===`enabled`){let n=e.thinking.budgetTokens;n<1024&&t.push(`Thinking budget must be at least ${Af} (got ${n})`),n>=e.maxTokens&&t.push(`Thinking budget (${n}) must be less than max tokens (${e.maxTokens})`)}return t}function qf(e){switch(e.type){case`disabled`:return{disabled:{disabled:!0}};case`enabled`:return{enabled:{budgetTokens:e.budgetTokens,display:e.display??null}};case`adaptive`:return{adaptive:{display:e.display??null}};default:return fr(e)}}function Jf(e){let t=Q(e),n=Kf(t);if(n.length>0)throw Error(`Cannot serialize Anthropic invocation parameters: ${n.join(`; `)}`);let r={maxTokens:t.maxTokens};return t.temperature!==void 0&&(r.temperature=t.temperature),t.topP!==void 0&&(r.topP=t.topP),t.stopSequences!==void 0&&(r.stopSequences=t.stopSequences),t.thinking!==void 0&&(r.thinking=qf(t.thinking)),t.effort!==void 0&&(r.outputConfig={effort:t.effort}),t.extraBody!==void 0&&(r.extraBody=t.extraBody),{anthropic:r}}function Yf(e){if(e.__typename!==`PromptAnthropicInvocationParameters`)throw Error(`anthropicAdapter.fromPromptInvocationParameters called with non-Anthropic typename: ${e.__typename}`);let t={maxTokens:e.anthropicMaxTokens};if(e.temperature!=null&&(t.temperature=e.temperature),e.topP!=null&&(t.topP=e.topP),e.stopSequences!=null&&(t.stopSequences=[...e.stopSequences]),e.outputConfig?.effort!=null&&(t.effort=e.outputConfig.effort),e.thinking)switch(e.thinking.__typename){case`PromptAnthropicThinkingDisabled`:t.thinking={type:`disabled`};break;case`PromptAnthropicThinkingEnabled`:{let n={type:`enabled`,budgetTokens:e.thinking.budgetTokens};e.thinking.enabledDisplay!=null&&(n.display=e.thinking.enabledDisplay),t.thinking=n;break}case`PromptAnthropicThinkingAdaptive`:{let n={type:`adaptive`};e.thinking.adaptiveDisplay!=null&&(n.display=e.thinking.adaptiveDisplay),t.thinking=n;break}case`%other`:break;default:fr(e.thinking)}let n=np(e.extraBody);return n!=null&&(t.extraBody=n),Q(t)}function Xf(e){if(e.__typename!==`PromptAnthropicInvocationParameters`)throw Error(`anthropicAdapter.fromPromptInvocationParametersForDisplay called with non-Anthropic typename: ${e.__typename}`);let t={maxTokens:e.anthropicMaxTokens};if(e.temperature!=null&&(t.temperature=e.temperature),e.topP!=null&&(t.topP=e.topP),e.stopSequences!=null&&(t.stopSequences=[...e.stopSequences]),e.outputConfig?.effort!=null&&(t.outputConfig={effort:e.outputConfig.effort}),e.thinking)switch(e.thinking.__typename){case`PromptAnthropicThinkingDisabled`:t.thinking={type:`disabled`};break;case`PromptAnthropicThinkingEnabled`:{let n={type:`enabled`,budgetTokens:e.thinking.budgetTokens};e.thinking.enabledDisplay!=null&&(n.display=e.thinking.enabledDisplay),t.thinking=n;break}case`PromptAnthropicThinkingAdaptive`:{let n={type:`adaptive`};e.thinking.adaptiveDisplay!=null&&(n.display=e.thinking.adaptiveDisplay),t.thinking=n;break}case`%other`:break;default:fr(e.thinking)}let n=np(e.extraBody);return n!=null&&(t.extraBody=n),t}var Zf=or({effort:Ff,format:G({type:rr(`json_schema`),schema:ar(q(),sr())}).optional().catch(void 0)}).optional().catch(void 0),Qf=or({max_tokens:K().optional().catch(void 0),temperature:K().optional().catch(void 0),top_p:K().optional().catch(void 0),stop_sequences:If,thinking:zf,output_config:Zf,extra_body:Lf});function $f(e){let t=Qf.safeParse(e),n=t.success?t.data:{},r={maxTokens:n.max_tokens??2e3};n.temperature!==void 0&&(r.temperature=n.temperature),n.top_p!==void 0&&(r.topP=n.top_p),n.stop_sequences!==void 0&&(r.stopSequences=[...n.stop_sequences]);let i=Bf(n.thinking);if(i!==void 0&&(r.thinking=i),n.output_config?.effort!==void 0&&(r.effort=n.output_config.effort),n.extra_body!==void 0){let e=np(n.extra_body);e!==void 0&&(r.extraBody=e)}let a={},o=n.output_config?.format;return o&&(a.responseFormat={type:`json_schema`,jsonSchema:{name:`response`,schema:o.schema}}),{config:Q(r),promoted:a}}function ep(e,t){switch(t){case`maxTokens`:return e.maxTokens;case`temperature`:return e.temperature;case`topP`:return e.topP;case`stopSequences`:return e.stopSequences;case`thinkingType`:return e.thinking?.type;case`thinkingBudgetTokens`:return e.thinking?.type===`enabled`?e.thinking.budgetTokens:void 0;case`thinkingDisplay`:return e.thinking&&e.thinking.type!==`disabled`?e.thinking.display?.toLowerCase():void 0;case`effort`:return e.effort?.toLowerCase();case`extraBody`:return e.extraBody;default:return}}function tp(e,t,n){switch(t){case`maxTokens`:return typeof n!=`number`||Number.isNaN(n)?e:Q({...e,maxTokens:n});case`temperature`:if(n===void 0){let t={...e};return delete t.temperature,Q(t)}return typeof n!=`number`||Number.isNaN(n)?e:Q({...e,temperature:n});case`topP`:if(n===void 0){let t={...e};return delete t.topP,Q(t)}return typeof n!=`number`||Number.isNaN(n)?e:Q({...e,topP:n});case`stopSequences`:if(n===void 0){let t={...e};return delete t.stopSequences,Q(t)}return Array.isArray(n)?Q({...e,stopSequences:n.map(String)}):e;case`thinkingType`:if(n===void 0){let t={...e};return delete t.thinking,Q(t)}if(n===`disabled`)return Q({...e,thinking:{type:`disabled`}});if(n===`enabled`){let t=e.thinking,n=t?.type===`enabled`?t.budgetTokens:Af,r=t&&t.type!==`disabled`?t.display:void 0,i={type:`enabled`,budgetTokens:n};r!==void 0&&(i.display=r);let a=e.maxTokens>n?e.maxTokens:n+1;return Q({...e,maxTokens:a,thinking:i})}if(n===`adaptive`){let t=e.thinking,n=t&&t.type!==`disabled`?t.display:void 0,r={type:`adaptive`};return n!==void 0&&(r.display=n),Q({...e,thinking:r})}return e;case`thinkingBudgetTokens`:return e.thinking?.type!==`enabled`||n===void 0||typeof n!=`number`||Number.isNaN(n)?e:Q({...e,thinking:{...e.thinking,budgetTokens:n}});case`thinkingDisplay`:{let t=e.thinking;if(!t||t.type===`disabled`)return e;if(n===void 0){if(t.type===`enabled`){let n={type:`enabled`,budgetTokens:t.budgetTokens};return Q({...e,thinking:n})}return Q({...e,thinking:{type:`adaptive`}})}let r=Pf.safeParse(n);return!r.success||!r.data?e:t.type===`enabled`?Q({...e,thinking:{type:`enabled`,budgetTokens:t.budgetTokens,display:r.data}}):Q({...e,thinking:{type:`adaptive`,display:r.data}})}case`effort`:{if(n===void 0){let t={...e};return delete t.effort,Q(t)}let t=Ff.safeParse(n);return!t.success||!t.data?e:Q({...e,effort:t.data})}case`extraBody`:{if(n===void 0){let t={...e};return delete t.extraBody,Q(t)}let t=np(n);return t===void 0?e:Q({...e,extraBody:t})}default:return e}}function np(e){if(typeof e==`object`&&e&&!Array.isArray(e))return e}var rp={getDefaultConfig:Hf,getVisibleSpecs:Uf,parseConfig:Gf,normalize:Q,validateForSubmit:Kf,toPromptInput:Jf,fromPromptInvocationParameters:Yf,fromPromptInvocationParametersForDisplay:Xf,fromSpanInvocationParameters:$f,readField:ep,writeField:tp};function ip(e){return vr(e)&&!Array.isArray(e)}function ap({str:e,excludePrimitives:t=!1,excludeArray:n=!1,excludeNull:r=!1}){try{let i=JSON.parse(e);if(t&&typeof i!=`object`||n&&Array.isArray(i)||r&&i===null)return!1}catch{return!1}return!0}function op(e){return ap({str:e,excludeArray:!0,excludePrimitives:!0})}function sp(e){try{return{json:JSON.parse(e)}}catch(e){return{json:null,parseError:e}}}function cp(...e){try{return{json:JSON.stringify(...e)}}catch(e){return{json:null,stringifyError:e}}}function lp(e){if(typeof e==`string`){let t=xp(e);return t===void 0?e:lp(t)}return Array.isArray(e)?e.map(lp):typeof e==`object`&&e?Object.fromEntries(Object.entries(e).map(([e,t])=>[e,lp(t)])):e}function up(e){return typeof e==`string`?xp(e)!==void 0:Array.isArray(e)?e.some(up):typeof e==`object`&&e?Object.values(e).some(up):!1}var dp=`.`;function fp({parentKey:e,index:t,indexNotation:n}){return n===`bracket`?`${e}[${t}]`:e?`${e}${dp}${t}`:String(t)}function pp({value:e,indexNotation:t=`bracket`,parentKey:n=``}){return Array.isArray(e)&&e.length>0?e.flatMap((e,r)=>pp({value:e,indexNotation:t,parentKey:fp({parentKey:n,index:r,indexNotation:t})})):ip(e)&&Object.keys(e).length>0?Object.entries(e).flatMap(([e,r])=>pp({value:r,indexNotation:t,parentKey:n?`${n}${dp}${e}`:e})):n===``?[]:[{key:n,value:e}]}function mp(e){return typeof e==`string`?e:cp(e).json??String(e)}function hp({entries:e,query:t}){let n=t.trim().toLowerCase();return n?e.filter(({key:e,value:t})=>e.toLowerCase().includes(n)||mp(t).toLowerCase().includes(n)):e}function gp({obj:e,parentKey:t=``,separator:n=`.`,keepNonTerminalValues:r=!1,formatIndices:i=!1}){let a={};for(let[o,s]of Object.entries(e)){let c;c=i&&Array.isArray(e)?t?`${t}[${o}]`:`[${o}]`:t?`${t}${n}${o}`:o,s&&typeof s==`object`?(r&&(a[c]=s),Object.assign(a,gp({obj:s,parentKey:c,separator:n,keepNonTerminalValues:r,formatIndices:i}))):a[c]=s}return a}function _p(e,t=`.`){try{let n=JSON.parse(e);return typeof n==`object`?gp({obj:n,separator:t}):{}}catch{}return{}}function vp(e,t){let n=t?.unquotePlainString??!1;if(typeof e==`string`){let t=e.startsWith(`"{`)||e.startsWith(`"[`)||e.startsWith(`"\\"`);try{if(t){let t=JSON.parse(e),n=typeof t==`string`?JSON.parse(t):t;return JSON.stringify(n,null,2)}}catch{}return n?e:JSON.stringify(e)}try{let t=JSON.stringify(e,null,2);if(t!==void 0)return t}catch{}return String(e)}function yp(e){if(e!=null)try{return JSON.stringify(e)}catch{return}}function bp(e){if(e.trim())try{return JSON.parse(e)}catch{return}}function xp(e){let t=bp(e);if(!(typeof t!=`object`||!t))return t}function Sp(e){if(e==null)return``;if(Array.isArray(e))return e.length>0?e.map(Sp):[];if(typeof e==`object`){let t={};for(let n in e)t[n]=Sp(e[n]);return t}return typeof e==`string`?``:typeof e==`number`||typeof e==`boolean`?e:``}function Cp(e){try{let t=Sp(JSON.parse(e));return JSON.stringify(t,null,2)}catch{return`{
  
}`}}function wp(e){if(!vr(e))return{value:e,wasUnnested:!1};let t=Object.keys(e);if(t.length!==1)return{value:e,wasUnnested:!1};let n=e[t[0]];return typeof n==`string`?{value:n,wasUnnested:!0}:{value:e,wasUnnested:!1}}function Tp(){return{maxTokens:1024,temperature:1}}function Ep(){return kf}var Dp=or({maxTokens:K().optional().catch(void 0),temperature:K().optional().catch(void 0),topP:K().optional().catch(void 0),stopSequences:ir(q()).optional().catch(void 0)});function Op(e){let t=Dp.safeParse(e),n=t.success?t.data:{},r={};return n.maxTokens!==void 0&&(r.maxTokens=n.maxTokens),n.temperature!==void 0&&(r.temperature=n.temperature),n.topP!==void 0&&(r.topP=n.topP),n.stopSequences!==void 0&&(r.stopSequences=[...n.stopSequences]),r}function kp(e){return e}function Ap(e){return[]}function jp(e){let t=kp(e),n={};return t.maxTokens!==void 0&&(n.maxTokens=t.maxTokens),t.temperature!==void 0&&(n.temperature=t.temperature),t.topP!==void 0&&(n.topP=t.topP),t.stopSequences!==void 0&&(n.stopSequences=t.stopSequences),{aws:n}}function Mp(e){if(e.__typename!==`PromptAwsInvocationParameters`)throw Error(`awsAdapter.fromPromptInvocationParameters called with non-AWS typename: ${e.__typename}`);let t={};return e.awsMaxTokens!=null&&(t.maxTokens=e.awsMaxTokens),e.temperature!=null&&(t.temperature=e.temperature),e.topP!=null&&(t.topP=e.topP),e.stopSequences!=null&&(t.stopSequences=[...e.stopSequences]),kp(t)}function Np(e){if(e.__typename!==`PromptAwsInvocationParameters`)throw Error(`awsAdapter.fromPromptInvocationParametersForDisplay called with non-AWS typename: ${e.__typename}`);let t={};return e.awsMaxTokens!=null&&(t.maxTokens=e.awsMaxTokens),e.temperature!=null&&(t.temperature=e.temperature),e.topP!=null&&(t.topP=e.topP),e.stopSequences!=null&&(t.stopSequences=[...e.stopSequences]),t}var Pp=G({maxTokens:K().optional().catch(void 0),temperature:K().optional().catch(void 0),topP:K().optional().catch(void 0),stopSequences:ir(q()).optional().catch(void 0)}).optional().catch(void 0),Fp=G({schema:cr([q(),ar(q(),sr())]).optional(),name:q().optional(),description:q().optional()}).optional().catch(void 0),Ip=G({textFormat:G({structure:G({jsonSchema:Fp}).optional().catch(void 0)}).optional().catch(void 0)}).optional().catch(void 0),Lp=or({maxTokens:K().optional().catch(void 0),temperature:K().optional().catch(void 0),topP:K().optional().catch(void 0),stopSequences:ir(q()).optional().catch(void 0),inferenceConfig:Pp,outputConfig:Ip});function Rp(e){let t=Lp.safeParse(e),n=t.success?t.data:{},r={};n.maxTokens===void 0?n.inferenceConfig?.maxTokens!==void 0&&(r.maxTokens=n.inferenceConfig.maxTokens):r.maxTokens=n.maxTokens,n.temperature===void 0?n.inferenceConfig?.temperature!==void 0&&(r.temperature=n.inferenceConfig.temperature):r.temperature=n.temperature,n.topP===void 0?n.inferenceConfig?.topP!==void 0&&(r.topP=n.inferenceConfig.topP):r.topP=n.topP,n.stopSequences===void 0?n.inferenceConfig?.stopSequences!==void 0&&(r.stopSequences=[...n.inferenceConfig.stopSequences]):r.stopSequences=[...n.stopSequences];let i={},a=n.outputConfig?.textFormat?.structure?.jsonSchema;if(a?.schema!=null){let e=null;if(typeof a.schema==`string`){let{json:t}=sp(a.schema);typeof t==`object`&&t&&!Array.isArray(t)&&(e=t)}else typeof a.schema==`object`&&!Array.isArray(a.schema)&&(e=a.schema);if(e!=null){let t={name:typeof a.name==`string`?a.name:`response`,schema:e};typeof a.description==`string`&&(t.description=a.description),i.responseFormat={type:`json_schema`,jsonSchema:t}}}return{config:kp(r),promoted:i}}function zp(e,t){switch(t){case`maxTokens`:return e.maxTokens;case`temperature`:return e.temperature;case`topP`:return e.topP;case`stopSequences`:return e.stopSequences;default:return}}function Bp(e,t,n){switch(t){case`maxTokens`:case`temperature`:case`topP`:if(n===void 0){let n={...e};return delete n[t],kp(n)}return typeof n!=`number`||Number.isNaN(n)?e:kp({...e,[t]:n});case`stopSequences`:if(n===void 0){let t={...e};return delete t.stopSequences,kp(t)}return Array.isArray(n)?kp({...e,stopSequences:n.map(String)}):e;default:return e}}var Vp={getDefaultConfig:Tp,getVisibleSpecs:Ep,parseConfig:Op,normalize:kp,validateForSubmit:Ap,toPromptInput:jp,fromPromptInvocationParameters:Mp,fromPromptInvocationParametersForDisplay:Np,fromSpanInvocationParameters:e=>Rp(e),readField:zp,writeField:Bp};function Hp(){return{temperature:1,presencePenalty:0,frequencyPenalty:0,thinkingConfig:{thinkingLevel:`MEDIUM`,includeThoughts:!0}}}function Up(){return Of}var Wp=q().transform(e=>e.toUpperCase()).pipe(nr(Cf)).optional().catch(void 0),Gp=or({thinkingBudget:K().optional().catch(void 0),thinkingLevel:Wp,includeThoughts:lr().optional().catch(void 0)}).optional().catch(void 0),Kp=or({temperature:K().optional().catch(void 0),maxOutputTokens:K().optional().catch(void 0),stopSequences:ir(q()).optional().catch(void 0),presencePenalty:K().optional().catch(void 0),frequencyPenalty:K().optional().catch(void 0),topP:K().optional().catch(void 0),topK:K().optional().catch(void 0),thinkingConfig:Gp});function qp(e){let t=Kp.safeParse(e),n=t.success?t.data:{},r={};return n.temperature!==void 0&&(r.temperature=n.temperature),n.maxOutputTokens!==void 0&&(r.maxOutputTokens=n.maxOutputTokens),n.stopSequences!==void 0&&(r.stopSequences=[...n.stopSequences]),n.presencePenalty!==void 0&&(r.presencePenalty=n.presencePenalty),n.frequencyPenalty!==void 0&&(r.frequencyPenalty=n.frequencyPenalty),n.topP!==void 0&&(r.topP=n.topP),n.topK!==void 0&&(r.topK=n.topK),n.thinkingConfig!==void 0&&n.thinkingConfig!==null&&(r.thinkingConfig=Jp(n.thinkingConfig)),r}function Jp(e){let t={};return e.thinkingBudget!==void 0&&(t.thinkingBudget=e.thinkingBudget),e.thinkingLevel!==void 0&&(t.thinkingLevel=e.thinkingLevel),e.includeThoughts!==void 0&&(t.includeThoughts=e.includeThoughts),t}function Yp(e){return e}function Xp(e){return[]}function Zp(e){let t={};return e.thinkingBudget!==void 0&&(t.thinkingBudget=e.thinkingBudget),e.thinkingLevel!==void 0&&(t.thinkingLevel=e.thinkingLevel),e.includeThoughts!==void 0&&(t.includeThoughts=e.includeThoughts),Object.keys(t).length>0?t:void 0}function Qp(e){let t=Yp(e),n={};if(t.temperature!==void 0&&(n.temperature=t.temperature),t.maxOutputTokens!==void 0&&(n.maxOutputTokens=t.maxOutputTokens),t.stopSequences!==void 0&&(n.stopSequences=t.stopSequences),t.presencePenalty!==void 0&&(n.presencePenalty=t.presencePenalty),t.frequencyPenalty!==void 0&&(n.frequencyPenalty=t.frequencyPenalty),t.topP!==void 0&&(n.topP=t.topP),t.topK!==void 0&&(n.topK=t.topK),t.thinkingConfig!==void 0){let e=Zp(t.thinkingConfig);e&&(n.thinkingConfig=e)}return{google:n}}function $p(e){if(e.__typename!==`PromptGoogleInvocationParameters`)throw Error(`googleAdapter.fromPromptInvocationParameters called with non-Google typename: ${e.__typename}`);let t={};if(e.temperature!=null&&(t.temperature=e.temperature),e.maxOutputTokens!=null&&(t.maxOutputTokens=e.maxOutputTokens),e.stopSequences!=null&&(t.stopSequences=[...e.stopSequences]),e.presencePenalty!=null&&(t.presencePenalty=e.presencePenalty),e.frequencyPenalty!=null&&(t.frequencyPenalty=e.frequencyPenalty),e.topP!=null&&(t.topP=e.topP),e.topK!=null&&(t.topK=e.topK),e.thinkingConfig){let n={};e.thinkingConfig.thinkingBudget!=null&&(n.thinkingBudget=e.thinkingConfig.thinkingBudget),e.thinkingConfig.thinkingLevel!=null&&(n.thinkingLevel=e.thinkingConfig.thinkingLevel),e.thinkingConfig.includeThoughts!=null&&(n.includeThoughts=e.thinkingConfig.includeThoughts),Object.keys(n).length>0&&(t.thinkingConfig=n)}return Yp(t)}function em(e){if(e.__typename!==`PromptGoogleInvocationParameters`)throw Error(`googleAdapter.fromPromptInvocationParametersForDisplay called with non-Google typename: ${e.__typename}`);let t={};if(e.temperature!=null&&(t.temperature=e.temperature),e.maxOutputTokens!=null&&(t.maxOutputTokens=e.maxOutputTokens),e.stopSequences!=null&&(t.stopSequences=[...e.stopSequences]),e.presencePenalty!=null&&(t.presencePenalty=e.presencePenalty),e.frequencyPenalty!=null&&(t.frequencyPenalty=e.frequencyPenalty),e.topP!=null&&(t.topP=e.topP),e.topK!=null&&(t.topK=e.topK),e.thinkingConfig){let n={};e.thinkingConfig.thinkingBudget!=null&&(n.thinkingBudget=e.thinkingConfig.thinkingBudget),e.thinkingConfig.thinkingLevel!=null&&(n.thinkingLevel=e.thinkingConfig.thinkingLevel),e.thinkingConfig.includeThoughts!=null&&(n.includeThoughts=e.thinkingConfig.includeThoughts),Object.keys(n).length>0&&(t.thinkingConfig=n)}return t}var tm=or({thinking_budget:K().optional().catch(void 0),thinking_level:Wp,include_thoughts:lr().optional().catch(void 0)}).optional().catch(void 0),nm=or({temperature:K().optional().catch(void 0),max_output_tokens:K().optional().catch(void 0),stop_sequences:ir(q()).optional().catch(void 0),presence_penalty:K().optional().catch(void 0),frequency_penalty:K().optional().catch(void 0),top_p:K().optional().catch(void 0),top_k:K().optional().catch(void 0),thinking_config:tm,response_json_schema:sr().optional(),response_schema:sr().optional(),response_mime_type:q().optional().catch(void 0)});function rm(e){let t=nm.safeParse(e),n=t.success?t.data:{},r={};if(n.temperature!==void 0&&(r.temperature=n.temperature),n.max_output_tokens!==void 0&&(r.maxOutputTokens=n.max_output_tokens),n.stop_sequences!==void 0&&(r.stopSequences=[...n.stop_sequences]),n.presence_penalty!==void 0&&(r.presencePenalty=n.presence_penalty),n.frequency_penalty!==void 0&&(r.frequencyPenalty=n.frequency_penalty),n.top_p!==void 0&&(r.topP=n.top_p),n.top_k!==void 0&&(r.topK=n.top_k),n.thinking_config){let e={};n.thinking_config.thinking_budget!==void 0&&(e.thinkingBudget=n.thinking_config.thinking_budget),n.thinking_config.thinking_level!==void 0&&(e.thinkingLevel=n.thinking_config.thinking_level),n.thinking_config.include_thoughts!==void 0&&(e.includeThoughts=n.thinking_config.include_thoughts),Object.keys(e).length>0&&(r.thinkingConfig=e)}let i={},a=n.response_json_schema??n.response_schema;return a!=null&&n.response_mime_type===`application/json`&&(i.responseFormat={type:`json_schema`,jsonSchema:{name:`response`,schema:a}}),{config:Yp(r),promoted:i}}var im=new Set([`temperature`,`maxOutputTokens`,`presencePenalty`,`frequencyPenalty`,`topP`,`topK`]);function am(e){return im.has(e)}function om(e){let t={};return e.thinkingBudget!==void 0&&(t.thinkingBudget=e.thinkingBudget),e.thinkingLevel!==void 0&&(t.thinkingLevel=e.thinkingLevel),e.includeThoughts!==void 0&&(t.includeThoughts=e.includeThoughts),Object.keys(t).length===0?void 0:t}function sm(e,t){if(am(t))return e[t];switch(t){case`stopSequences`:return e.stopSequences;case`thinkingBudget`:return e.thinkingConfig?.thinkingBudget;case`thinkingLevel`:return e.thinkingConfig?.thinkingLevel?.toLowerCase();case`includeThoughts`:return e.thinkingConfig?.includeThoughts;default:return}}function cm(e,t,n){if(am(t)){if(n===void 0){let n={...e};return delete n[t],Yp(n)}return typeof n!=`number`||Number.isNaN(n)?e:Yp({...e,[t]:n})}switch(t){case`stopSequences`:if(n===void 0){let t={...e};return delete t.stopSequences,Yp(t)}return Array.isArray(n)?Yp({...e,stopSequences:n.map(String)}):e;case`thinkingBudget`:{let t={...e.thinkingConfig??{}};if(n===void 0)delete t.thinkingBudget;else if(typeof n==`number`&&!Number.isNaN(n))t.thinkingBudget=n;else return e;return lm(e,t)}case`thinkingLevel`:{let t={...e.thinkingConfig??{}};if(n===void 0)delete t.thinkingLevel;else{let r=Wp.safeParse(n);if(!r.success||!r.data)return e;t.thinkingLevel=r.data}return lm(e,t)}case`includeThoughts`:{let t={...e.thinkingConfig??{}};if(n===void 0)delete t.includeThoughts;else if(typeof n==`boolean`)t.includeThoughts=n;else return e;return lm(e,t)}default:return e}}function lm(e,t){let n=om(t),r={...e};return n===void 0?delete r.thinkingConfig:r.thinkingConfig=n,Yp(r)}var um={getDefaultConfig:Hp,getVisibleSpecs:Up,parseConfig:qp,normalize:Yp,validateForSubmit:Xp,toPromptInput:Qp,fromPromptInvocationParameters:$p,fromPromptInvocationParametersForDisplay:em,fromSpanInvocationParameters:e=>rm(e),readField:sm,writeField:cm};function dm(e){if(typeof e==`object`&&e&&!Array.isArray(e))return e}function fm(e){return e===0?void 0:e}function pm(){return{frequencyPenalty:0,presencePenalty:0}}function mm(e,t){let n=t.openaiApiType??`RESPONSES`;return Ef.filter(e=>{let t=`applicableOpenAIApiTypes`in e?e.applicableOpenAIApiTypes:void 0;return t==null||t.includes(n)})}var hm=or({temperature:K().optional().catch(void 0),topP:K().optional().catch(void 0),maxCompletionTokens:K().optional().catch(void 0),frequencyPenalty:K().optional().catch(void 0),presencePenalty:K().optional().catch(void 0),reasoningEffort:q().optional().catch(void 0),seed:K().optional().catch(void 0),stop:ir(q()).optional().catch(void 0),extraBody:ar(q(),sr()).optional().catch(void 0)});function gm(e){let t=hm.safeParse(e),n=t.success?t.data:{},r={};if(n.temperature!==void 0&&(r.temperature=n.temperature),n.topP!==void 0&&(r.topP=n.topP),n.maxCompletionTokens!==void 0&&(r.maxCompletionTokens=n.maxCompletionTokens),n.frequencyPenalty!==void 0&&(r.frequencyPenalty=n.frequencyPenalty),n.presencePenalty!==void 0&&(r.presencePenalty=n.presencePenalty),n.reasoningEffort!==void 0){let e=_f(n.reasoningEffort);e!==void 0&&(r.reasoningEffort=e)}return n.seed!==void 0&&(r.seed=n.seed),n.stop!==void 0&&(r.stop=[...n.stop]),n.extraBody!==void 0&&(r.extraBody={...n.extraBody}),r}function _m(e){return e}function vm(e){return[]}function ym(e){let t=_m(e),n={};t.temperature!==void 0&&(n.temperature=t.temperature),t.topP!==void 0&&(n.topP=t.topP),t.maxCompletionTokens!==void 0&&(n.maxCompletionTokens=t.maxCompletionTokens);let r=fm(t.frequencyPenalty);r!==void 0&&(n.frequencyPenalty=r);let i=fm(t.presencePenalty);if(i!==void 0&&(n.presencePenalty=i),t.reasoningEffort!==void 0){let e=gf(t.reasoningEffort);e!==void 0&&(n.reasoningEffort=e)}return t.seed!==void 0&&(n.seed=t.seed),t.stop!==void 0&&(n.stop=t.stop),t.extraBody!==void 0&&(n.extraBody=t.extraBody),{openai:n}}function bm(e){if(e.__typename!==`PromptOpenAIInvocationParameters`)throw Error(`openaiAdapter.fromPromptInvocationParameters called with non-OpenAI typename: ${e.__typename}`);let t={};if(e.temperature!=null&&(t.temperature=e.temperature),e.topP!=null&&(t.topP=e.topP),e.maxCompletionTokens==null?e.openaiMaxTokens!=null&&(t.maxCompletionTokens=e.openaiMaxTokens):t.maxCompletionTokens=e.maxCompletionTokens,e.frequencyPenalty!=null&&(t.frequencyPenalty=e.frequencyPenalty),e.presencePenalty!=null&&(t.presencePenalty=e.presencePenalty),e.seed!=null&&(t.seed=e.seed),e.stop!=null&&(t.stop=[...e.stop]),e.reasoningEffort!=null){let n=_f(e.reasoningEffort);n!==void 0&&(t.reasoningEffort=n)}let n=dm(e.extraBody);return n!=null&&(t.extraBody=n),_m(t)}function xm(e){if(e.__typename!==`PromptOpenAIInvocationParameters`)throw Error(`openaiAdapter.fromPromptInvocationParametersForDisplay called with non-OpenAI typename: ${e.__typename}`);let t={};e.temperature!=null&&(t.temperature=e.temperature),e.openaiMaxTokens!=null&&(t.maxTokens=e.openaiMaxTokens),e.maxCompletionTokens!=null&&(t.maxCompletionTokens=e.maxCompletionTokens),e.frequencyPenalty!=null&&(t.frequencyPenalty=e.frequencyPenalty),e.presencePenalty!=null&&(t.presencePenalty=e.presencePenalty),e.topP!=null&&(t.topP=e.topP),e.seed!=null&&(t.seed=e.seed),e.stop!=null&&(t.stop=[...e.stop]);let n=_f(e.reasoningEffort);n!==void 0&&(t.reasoningEffort=n);let r=dm(e.extraBody);return r!=null&&(t.extraBody=r),t}var Sm=G({name:q().optional(),schema:sr().optional(),strict:lr().nullish(),description:q().nullish()}),Cm=G({type:q().optional(),json_schema:Sm.optional()}).optional().catch(void 0),wm=G({type:q().optional(),name:q().optional(),schema:sr().optional(),strict:lr().optional(),description:q().optional()}).optional().catch(void 0),Tm=or({temperature:K().optional().catch(void 0),top_p:K().optional().catch(void 0),max_completion_tokens:K().optional().catch(void 0),max_tokens:K().optional().catch(void 0),max_output_tokens:K().optional().catch(void 0),frequency_penalty:K().optional().catch(void 0),presence_penalty:K().optional().catch(void 0),seed:K().optional().catch(void 0),stop:ir(q()).optional().catch(void 0),reasoning_effort:q().optional().catch(void 0),reasoning:or({effort:q().optional().catch(void 0)}).optional().catch(void 0),response_format:Cm,text:G({format:wm}).optional().catch(void 0),extra_body:ar(q(),sr()).optional().catch(void 0)});function Em(e,t){let n=Tm.safeParse(e),r=n.success?n.data:{},i={};r.temperature!==void 0&&(i.temperature=r.temperature),r.top_p!==void 0&&(i.topP=r.top_p),r.max_completion_tokens===void 0?r.max_tokens===void 0?t===`RESPONSES`&&r.max_output_tokens!==void 0&&(i.maxCompletionTokens=r.max_output_tokens):i.maxCompletionTokens=r.max_tokens:i.maxCompletionTokens=r.max_completion_tokens,r.frequency_penalty!==void 0&&(i.frequencyPenalty=r.frequency_penalty),r.presence_penalty!==void 0&&(i.presencePenalty=r.presence_penalty),r.seed!==void 0&&(i.seed=r.seed),r.stop!==void 0&&(i.stop=[...r.stop]);let a;if(r.reasoning_effort===void 0?t===`RESPONSES`&&r.reasoning?.effort!==void 0&&(a=r.reasoning.effort):a=r.reasoning_effort,a!==void 0){let e=_f(a);e!==void 0&&(i.reasoningEffort=e)}r.extra_body!==void 0&&(i.extraBody={...r.extra_body});let o={},s=r.response_format;if(s?.json_schema){let e=s.json_schema,t={name:typeof e.name==`string`?e.name:`response`};e.schema!==void 0&&(t.schema=e.schema),e.strict!==void 0&&e.strict!==null&&(t.strict=e.strict),e.description!==void 0&&e.description!==null&&(t.description=e.description),o.responseFormat={type:`json_schema`,jsonSchema:t}}else if(r.text?.format!==void 0){let e=r.text.format;if(e){let t={name:typeof e.name==`string`?e.name:`response`};e.schema!==void 0&&(t.schema=e.schema),e.strict!==void 0&&(t.strict=e.strict),e.description!==void 0&&(t.description=e.description),o.responseFormat={type:`json_schema`,jsonSchema:t}}}return{config:_m(i),promoted:o}}var Dm=new Set([`temperature`,`topP`,`maxCompletionTokens`,`frequencyPenalty`,`presencePenalty`,`seed`]);function Om(e){return Dm.has(e)}function km(e,t){if(Om(t))return e[t];switch(t){case`reasoningEffort`:return e.reasoningEffort;case`stop`:return e.stop;case`extraBody`:return e.extraBody;default:return}}function Am(e,t,n){if(Om(t)){if(n===void 0){let n={...e};return delete n[t],_m(n)}return typeof n!=`number`||Number.isNaN(n)?e:_m({...e,[t]:n})}switch(t){case`reasoningEffort`:if(n===void 0){let t={...e};return delete t.reasoningEffort,_m(t)}return typeof n==`string`?_m({...e,reasoningEffort:n}):e;case`stop`:if(n===void 0){let t={...e};return delete t.stop,_m(t)}return Array.isArray(n)?_m({...e,stop:n.map(String)}):e;case`extraBody`:{if(n===void 0){let t={...e};return delete t.extraBody,_m(t)}let t=dm(n);return t===void 0?e:_m({...e,extraBody:t})}default:return e}}var jm={getDefaultConfig:pm,getVisibleSpecs:mm,parseConfig:gm,normalize:_m,validateForSubmit:vm,toPromptInput:ym,fromPromptInvocationParameters:bm,fromPromptInvocationParametersForDisplay:xm,fromSpanInvocationParameters:(e,t)=>Em(e,t?.openaiApiType??null),readField:km,writeField:Am};function Mm(e){switch(e){case Z.OPENAI:return jm;case Z.ANTHROPIC:return rp;case Z.GOOGLE_GENAI:return um;case Z.AWS_BEDROCK:return Vp;default:return fr(e)}}function Nm(e){return Mm(Tf(e))}function Pm(e){let t=Nm(e);return t.normalize(t.getDefaultConfig())}function Fm(e,t){let n=Nm(e);return n.normalize(n.parseConfig(t))}function Im(e,t){return Nm(e).toPromptInput(t)}function Lm(e,t){if(t==null)return Pm(e);let n=Tf(e);return n===Z.OPENAI&&t.__typename===`PromptOpenAIInvocationParameters`||n===Z.ANTHROPIC&&t.__typename===`PromptAnthropicInvocationParameters`||n===Z.GOOGLE_GENAI&&t.__typename===`PromptGoogleInvocationParameters`||n===Z.AWS_BEDROCK&&t.__typename===`PromptAwsInvocationParameters`?Nm(e).fromPromptInvocationParameters(t):Pm(e)}function Rm(e){if(e==null)return null;let t;switch(e.__typename){case`PromptOpenAIInvocationParameters`:t=Z.OPENAI;break;case`PromptAnthropicInvocationParameters`:t=Z.ANTHROPIC;break;case`PromptGoogleInvocationParameters`:t=Z.GOOGLE_GENAI;break;case`PromptAwsInvocationParameters`:t=Z.AWS_BEDROCK;break;case`%other`:throw Error(`Unsupported prompt invocation parameters typename: %other`);default:return fr(e)}let n=Mm(t);return{family:t,parameters:n.fromPromptInvocationParametersForDisplay(e)}}function zm(e,t,n={}){let{config:r,promoted:i}=Nm(e).fromSpanInvocationParameters(t,n);return{invocationParameters:r,responseFormat:i.responseFormat}}function Bm(e,t,n){return Nm(e).readField(t,n)}function Vm(e,t){return Nm(e.provider).getVisibleSpecs(t,{openaiApiType:e.openaiApiType})}function Hm(e,t,n,r){return Nm(e).writeField(t,n,r)}function Um(e,t){return t?e.isBusyElsewhereBySessionId[t]?`busyElsewhere`:e.sessionNoticeBySessionId[t]??null:null}function Wm(e,t){if(!t)return!1;let n=e.chatStatusBySessionId[t];return n===`submitted`||n===`streaming`||e.isBusyElsewhereBySessionId[t]===!0}var Gm=`pxi:draft-session`,Km={provider:`ANTHROPIC`,modelName:`claude-opus-4-6`,invocationParameters:Pm(`ANTHROPIC`)},qm={collectorEndpoint:null,assistantProjectName:`assistant_agent`,forceTracing:!1,webAccessEnabled:!1,assistantEnabled:!1,allowLocalTraces:!1,allowRemoteExport:!1,sessionRetentionMaxIdleDays:null,sessionRetentionMaxCountPerUser:null},Jm={storeLocalTraces:!0,exportRemoteTraces:!1,attachUserId:!1,acknowledgedTraceConsent:null},Ym={edits:`manual`};function Xm(e){return{allowLocalTraces:e.allowLocalTraces,allowRemoteExport:!!e.collectorEndpoint&&e.allowRemoteExport}}function Zm({agentsConfig:e,observability:t}){if(e.forceTracing)return!0;let n=t.acknowledgedTraceConsent;if(!n)return!1;let r=Xm(e);return(!r.allowLocalTraces||n.allowLocalTraces)&&(!r.allowRemoteExport||n.allowRemoteExport)}function Qm({agentsConfig:e,observability:t}){if(e.forceTracing)return{ingestTraces:!0,exportRemoteTraces:!0};let n=Xm(e);return{ingestTraces:n.allowLocalTraces&&t.storeLocalTraces,exportRemoteTraces:n.allowRemoteExport&&t.exportRemoteTraces}}function $m({agentsConfig:e,observability:t}){return e.forceTracing||t.attachUserId}function eh({capabilities:e,defaultCapabilities:t=cf()}){if(!e||typeof e!=`object`)return{...t};let n=e;return Object.fromEntries(Object.keys(t).map(e=>{let r=n[e];return[e,typeof r==`boolean`?r:t[e]]}))}function th(e,t){if(!e||typeof e!=`object`)return t;let{sessions:n,activeSessionId:r,sessionMap:i,...a}=e,o=typeof a.defaultTemporaryChat==`boolean`?a.defaultTemporaryChat:t.defaultTemporaryChat;return{...t,...a,defaultTemporaryChat:o,isDraftSessionTemporary:o,observability:{...t.observability,...a.observability},capabilities:eh({capabilities:a.capabilities,defaultCapabilities:t.capabilities})}}function nh(e,t){return Object.fromEntries(Object.entries(e).filter(([,e])=>e?.sessionId!==t))}var rh=`arize-phoenix-assistant`;function ih(){let e=(window.Config?.basename??``).replace(/\/+$/,``);return e?`${rh}:${e}`:rh}var ah=e=>oe()(n(v((t,n)=>({isOpen:!1,position:`pinned`,fabMode:`pinned`,fabPlacement:`bottom-end`,activeSessionId:null,isDraftSessionTemporary:!1,defaultTemporaryChat:!1,defaultModelConfig:{...Km},agentsConfig:qm,observability:Jm,permissions:Ym,capabilities:cf(),routeContexts:[],mountedContexts:{},pendingPromptEditsByToolCallId:{},pendingPromptInstanceRemovalsByToolCallId:{},pendingBatchSpanAnnotatesByToolCallId:{},pendingDatasetWritesByToolCallId:{},pendingAnnotationConfigWritesByToolCallId:{},pendingPatchExperimentsByToolCallId:{},pendingPromptToolWritesByToolCallId:{},pendingSavePromptsByToolCallId:{},pendingCodeEvaluatorEditsByToolCallId:{},pendingLlmEvaluatorEditsByToolCallId:{},pendingLoadDatasetsByToolCallId:{},locallyInterruptedToolCallIds:{},setIsOpen:e=>{t({isOpen:e},!1,{type:`setIsOpen`})},toggleOpen:()=>{t(e=>({isOpen:!e.isOpen}),!1,{type:`toggleOpen`})},setPosition:e=>{t({position:e},!1,{type:`setPosition`})},setFabMode:e=>{t({fabMode:e},!1,{type:`setFabMode`})},setFabPlacement:e=>{t({fabPlacement:e},!1,{type:`setFabPlacement`})},setActiveSession:e=>{t({activeSessionId:e},!1,{type:`setActiveSession`})},setIsDraftSessionTemporary:e=>{t({isDraftSessionTemporary:e},!1,{type:`setIsDraftSessionTemporary`})},setDefaultTemporaryChat:e=>{t({defaultTemporaryChat:e},!1,{type:`setDefaultTemporaryChat`})},clearSessionEphemeralState:e=>{t(t=>{let n={...t.pendingElicitationBySessionId};delete n[e];let r={...t.chatStatusBySessionId};delete r[e];let i={...t.isResponsePendingBySessionId};delete i[e];let a={...t.isCompactionPendingBySessionId};delete a[e];let o={...t.isBusyElsewhereBySessionId};delete o[e];let s={...t.sessionNoticeBySessionId};delete s[e];let c={...t.draftInputBySessionId};delete c[e];let l={...t.pendingMessageBySessionId};return delete l[e],{pendingElicitationBySessionId:n,chatStatusBySessionId:r,isResponsePendingBySessionId:i,isCompactionPendingBySessionId:a,isBusyElsewhereBySessionId:o,sessionNoticeBySessionId:s,draftInputBySessionId:c,pendingMessageBySessionId:l,pendingPatchExperimentsByToolCallId:nh(t.pendingPatchExperimentsByToolCallId,e)}},!1,{type:`clearSessionEphemeralState`})},setDefaultModelConfig:e=>{t({defaultModelConfig:e},!1,{type:`setDefaultModelConfig`})},setObservability:e=>{t(t=>({observability:{...t.observability,...e}}),!1,{type:`setObservability`})},setPermissions:e=>{t(t=>({permissions:{...t.permissions,...e}}),!1,{type:`setPermissions`})},setAgentsConfig:e=>{t(t=>({agentsConfig:{...t.agentsConfig,...e}}),!1,{type:`setAgentsConfig`})},acknowledgeConsent:()=>{t(e=>({observability:{...e.observability,acknowledgedTraceConsent:Xm(e.agentsConfig)}}),!1,{type:`acknowledgeConsent`})},setCapability:({key:e,enabled:n})=>{t(t=>({capabilities:{...t.capabilities,[e]:n}}),!1,{type:`setCapability`})},pendingElicitationBySessionId:{},setPendingElicitation:(e,n)=>{t(t=>{let r={...t.pendingElicitationBySessionId};return n?r[e]=n:delete r[e],{pendingElicitationBySessionId:r}},!1,{type:`setPendingElicitation`})},draftInputBySessionId:{},setDraftInput:(e,n)=>{t(t=>{let r={...t.draftInputBySessionId};return n?r[e]=n:delete r[e],{draftInputBySessionId:r}},!1,{type:`setDraftInput`})},pendingMessageBySessionId:{},setPendingMessage:(e,n)=>{t(t=>{let r={...t.pendingMessageBySessionId};return n?r[e]=n:delete r[e],{pendingMessageBySessionId:r}},!1,{type:`setPendingMessage`})},consumePendingMessage:e=>{let r=n().pendingMessageBySessionId[e]??null;return r!=null&&t(t=>{if(!(e in t.pendingMessageBySessionId))return t;let n={...t.pendingMessageBySessionId};return delete n[e],{pendingMessageBySessionId:n}},!1,{type:`consumePendingMessage`}),r},chatStatusBySessionId:{},setSessionChatStatus:(e,n)=>{t(t=>({chatStatusBySessionId:{...t.chatStatusBySessionId,[e]:n}}),!1,{type:`setSessionChatStatus`})},isResponsePendingBySessionId:{},setSessionResponsePending:(e,n)=>{t(t=>{let r={...t.isResponsePendingBySessionId};return n?r[e]=!0:delete r[e],{isResponsePendingBySessionId:r}},!1,{type:`setSessionResponsePending`})},isCompactionPendingBySessionId:{},setSessionCompactionPending:(e,n)=>{t(t=>{let r={...t.isCompactionPendingBySessionId};return n?r[e]=!0:delete r[e],{isCompactionPendingBySessionId:r}},!1,{type:`setSessionCompactionPending`})},isBusyElsewhereBySessionId:{},setSessionBusyElsewhere:(e,n)=>{t(t=>{let r={...t.isBusyElsewhereBySessionId};return n?r[e]=!0:delete r[e],{isBusyElsewhereBySessionId:r}},!1,{type:`setSessionBusyElsewhere`})},sessionNoticeBySessionId:{},setSessionNotice:(e,n)=>{t(t=>{if((t.sessionNoticeBySessionId[e]??null)===n)return t;let r={...t.sessionNoticeBySessionId};return n?r[e]=n:delete r[e],{sessionNoticeBySessionId:r}},!1,{type:`setSessionNotice`})},setRouteContexts:e=>{t(t=>{if(t.routeContexts.length===e.length){let n=!0;for(let r=0;r<e.length;r++)if(rf(t.routeContexts[r])!==rf(e[r])){n=!1;break}if(n)return t}return{routeContexts:e}},!1,{type:`setRouteContexts`})},setMountedContext:(e,n)=>{t(t=>({mountedContexts:{...t.mountedContexts,[e]:n}}),!1,{type:`setMountedContext`})},removeMountedContext:e=>{t(t=>{if(!(e in t.mountedContexts))return t;let n={...t.mountedContexts};return delete n[e],{mountedContexts:n}},!1,{type:`removeMountedContext`})},registeredClientActions:{},registerClientAction:(e,n)=>{t(t=>({registeredClientActions:{...t.registeredClientActions,[e]:n}}),!1,{type:`registerClientAction`})},unregisterClientAction:e=>{t(t=>{if(!(e in t.registeredClientActions))return t;let n={...t.registeredClientActions};return delete n[e],{registeredClientActions:n}},!1,{type:`unregisterClientAction`})},markToolCallInterrupted:e=>{t(t=>t.locallyInterruptedToolCallIds[e]?t:{locallyInterruptedToolCallIds:{...t.locallyInterruptedToolCallIds,[e]:!0}},!1,{type:`markToolCallInterrupted`})},setPendingPromptEdit:(e,n)=>{t(t=>{let r={...t.pendingPromptEditsByToolCallId};return n?r[e]=n:delete r[e],{pendingPromptEditsByToolCallId:r}},!1,{type:`setPendingPromptEdit`})},setPendingPromptInstanceRemoval:(e,n)=>{t(t=>{let r={...t.pendingPromptInstanceRemovalsByToolCallId};return n?r[e]=n:delete r[e],{pendingPromptInstanceRemovalsByToolCallId:r}},!1,{type:`setPendingPromptInstanceRemoval`})},setPendingDatasetWrite:(e,n)=>{t(t=>{let r={...t.pendingDatasetWritesByToolCallId};return n?r[e]=n:delete r[e],{pendingDatasetWritesByToolCallId:r}},!1,{type:`setPendingDatasetWrite`})},setPendingAnnotationConfigWrite:(e,n)=>{t(t=>{let r={...t.pendingAnnotationConfigWritesByToolCallId};return n?r[e]=n:delete r[e],{pendingAnnotationConfigWritesByToolCallId:r}},!1,{type:`setPendingAnnotationConfigWrite`})},setPendingBatchSpanAnnotate:(e,n)=>{t(t=>{let r={...t.pendingBatchSpanAnnotatesByToolCallId};return n?r[e]=n:delete r[e],{pendingBatchSpanAnnotatesByToolCallId:r}},!1,{type:`setPendingBatchSpanAnnotate`})},setPendingPatchExperiment:(e,n)=>{t(t=>{let r={...t.pendingPatchExperimentsByToolCallId};return n?r[e]=n:delete r[e],{pendingPatchExperimentsByToolCallId:r}},!1,{type:`setPendingPatchExperiment`})},setPendingPromptToolWrite:(e,n)=>{t(t=>{let r={...t.pendingPromptToolWritesByToolCallId};return n?r[e]=n:delete r[e],{pendingPromptToolWritesByToolCallId:r}},!1,{type:`setPendingPromptToolWrite`})},setPendingSavePrompt:(e,n)=>{t(t=>{let r={...t.pendingSavePromptsByToolCallId};return n?r[e]=n:delete r[e],{pendingSavePromptsByToolCallId:r}},!1,{type:`setPendingSavePrompt`})},setPendingCodeEvaluatorEdit:(e,n)=>{t(t=>{let r={...t.pendingCodeEvaluatorEditsByToolCallId};return n?r[e]=n:delete r[e],{pendingCodeEvaluatorEditsByToolCallId:r}},!1,{type:`setPendingCodeEvaluatorEdit`})},setPendingLlmEvaluatorEdit:(e,n)=>{t(t=>{let r={...t.pendingLlmEvaluatorEditsByToolCallId};return n?r[e]=n:delete r[e],{pendingLlmEvaluatorEditsByToolCallId:r}},!1,{type:`setPendingLlmEvaluatorEdit`})},setPendingLoadDataset:(e,n)=>{t(t=>{let r={...t.pendingLoadDatasetsByToolCallId};return n?r[e]=n:delete r[e],{pendingLoadDatasetsByToolCallId:r}},!1,{type:`setPendingLoadDataset`})},...e}),{name:`agentStore`}),{name:ih(),version:0,partialize:e=>({isOpen:e.isOpen,position:e.position,fabMode:e.fabMode,fabPlacement:e.fabPlacement,defaultTemporaryChat:e.defaultTemporaryChat,defaultModelConfig:e.defaultModelConfig,observability:e.observability,permissions:e.permissions,capabilities:e.capabilities}),merge:th}));async function oh({agentStore:e,names:t,timeoutMs:n=5e3}){let r=e=>t.every(t=>t in e);return r(e.getState().registeredClientActions)?!0:new Promise(t=>{let i=!1,a=null,o=e=>{i||(i=!0,a&&clearTimeout(a),s(),t(e))},s=e.subscribe(e=>{r(e.registeredClientActions)&&o(!0)});a=setTimeout(()=>o(!1),n),r(e.getState().registeredClientActions)&&o(!0)})}var sh=(0,J.createContext)(null);function ch(e){let t=(0,Y.c)(8),n,r;t[0]===e?(n=t[1],r=t[2]):({children:n,...r}=e,t[0]=e,t[1]=n,t[2]=r);let i;t[3]===r?i=t[4]:(i=()=>ah(r),t[3]=r,t[4]=i);let[a]=(0,J.useState)(i),o;return t[5]!==n||t[6]!==a?(o=B(sh.Provider,{value:a,children:n}),t[5]=n,t[6]=a,t[7]=o):o=t[7],o}function lh(e,t){let n=(0,J.useContext)(sh);if(!n)throw Error(`Missing AgentContext.Provider in the tree`);return be(n,e,t)}function uh(){let e=(0,J.useContext)(sh);if(!e)throw Error(`Missing AgentContext.Provider in the tree`);return e}var dh=(0,J.createContext)(null);function fh(){return J.useContext(dh)}function ph(){let e=fh();if(e===null)throw Error(`useTimeRange must be used within a TimeRangeContextProvider`);return e}function mh(){let e=(0,Y.c)(2),{timeRange:t}=ph(),n;return e[0]===t?n=e[1]:(n=Sd(t),e[0]=t,e[1]=n),n}function hh({storedLastNTimeRangeKey:e,now:t}){return vd(e)?{timeRangeKey:e,...gd(e,t)}:{timeRangeKey:`7d`,...gd(`7d`,t)}}function gh(e){let t=(0,Y.c)(37),{children:n}=e,[r,i]=$n(),a=hi(yh),o=hi(vh),[s,c]=(0,J.useState)(_h),l,u,d,f,p;t[0]!==r||t[1]!==a||t[2]!==s?(p=bd(r,s),d=p??hh({storedLastNTimeRangeKey:a,now:s}),f=d.start?.getTime(),l=d.start?.toISOString(),u=d.end?.toISOString(),t[0]=r,t[1]=a,t[2]=s,t[3]=l,t[4]=u,t[5]=d,t[6]=f,t[7]=p):(l=t[3],u=t[4],d=t[5],f=t[6],p=t[7]);let m=u,h;t[8]!==m||t[9]!==l?(h={start:l,end:m},t[8]=m,t[9]=l,t[10]=h):h=t[10];let g=h,_;t[11]!==i||t[12]!==o?(_=e=>{(0,J.startTransition)(()=>{i(t=>xd({searchParams:t,timeRange:e}),{replace:!0}),vd(e.timeRangeKey)&&(o(e.timeRangeKey),c(Date.now()))})},t[11]=i,t[12]=o,t[13]=_):_=t[13];let v=_,y;t[14]===v?y=t[15]:(y=e=>{v({timeRangeKey:`custom`,start:e.start,end:e.end})},t[14]=v,t[15]=y);let b=y,x,S;t[16]!==r||t[17]!==i||t[18]!==d||t[19]!==p?(x=()=>{if(p!=null)return;let e=xd({searchParams:r,timeRange:d});e.toString()!==r.toString()&&i(e,{replace:!0})},S=[p,r,i,d],t[16]=r,t[17]=i,t[18]=d,t[19]=p,t[20]=x,t[21]=S):(x=t[20],S=t[21]),(0,J.useEffect)(x,S);let C;t[22]===d.timeRangeKey?C=t[23]:(C=()=>{if(!vd(d.timeRangeKey))return;let e=d.timeRangeKey,t=window.setTimeout(()=>{c(Date.now())},_d(e));return()=>{window.clearTimeout(t)}},t[22]=d.timeRangeKey,t[23]=C);let w;t[24]!==d.timeRangeKey||t[25]!==f?(w=[d.timeRangeKey,f],t[24]=d.timeRangeKey,t[25]=f,t[26]=w):w=t[26],(0,J.useEffect)(C,w);let T;t[27]===v?T=t[28]:(T={setTimeRange:v},t[27]=v,t[28]=T),xh(T);let E;t[29]!==b||t[30]!==v||t[31]!==d||t[32]!==g?(E={timeRange:d,timeRangeISOStrings:g,setTimeRange:v,setCustomTimeRange:b},t[29]=b,t[30]=v,t[31]=d,t[32]=g,t[33]=E):E=t[33];let D;return t[34]!==n||t[35]!==E?(D=B(dh.Provider,{value:E,children:n}),t[34]=n,t[35]=E,t[36]=D):D=t[36],D}function _h(){return Date.now()}function vh(e){return e.setLastNTimeRangeKey}function yh(e){return e.lastNTimeRangeKey}function bh(e){if(e===void 0||e.trim()===``)return;let t=new Date(e);if(Number.isNaN(t.getTime()))throw Error(`Invalid ISO datetime: ${e}`);return t}function xh({setTimeRange:e}){let t=uh(),n=(0,J.useEffectEvent)(async t=>{if(t.timeRangeKey!==`custom`)return e({timeRangeKey:t.timeRangeKey,...gd(t.timeRangeKey)}),{ok:!0,output:`Set time range to ${t.timeRangeKey}.`};try{let n=bh(t.startTime),r=bh(t.endTime);return n===void 0&&r===void 0?{ok:!1,error:`Custom time range requires at least one of startTime or endTime.`}:n!==void 0&&r!==void 0&&n>r?{ok:!1,error:`Custom time range startTime must be before endTime.`}:(e({timeRangeKey:`custom`,start:n,end:r}),{ok:!0,output:`Set custom time range from ${n?.toISOString()??`open start`} to ${r?.toISOString()??`open end`}.`})}catch(e){return{ok:!1,error:e instanceof Error?e.message:`Invalid time range.`}}});(0,J.useEffect)(()=>{let{registerClientAction:e,unregisterClientAction:r}=t.getState();return e(qd,e=>n(e)),()=>{r(qd)}},[t])}function Sh({once:e=!1,rootMargin:t,scrollMargin:n}={}){let[r,i]=(0,J.useState)(!1),[a,o]=(0,J.useState)(!1);return r&&!a&&o(!0),{ref:r=>{if(r==null)return()=>{};if(!e){let e=r.getBoundingClientRect(),t=e.width>0||e.height>0,n=e.bottom>=0&&e.top<=window.innerHeight&&e.right>=0&&e.left<=window.innerWidth;t&&n&&i(!0)}let a=new IntersectionObserver(t=>{let n=t[t.length-1];(0,J.startTransition)(()=>i(n.isIntersecting)),e&&n.isIntersecting&&a.disconnect()},{rootMargin:t,scrollMargin:n});return a.observe(r),()=>a.disconnect()},isVisible:r,hasBeenVisible:a}}var Ch=(0,J.createContext)(!0);function wh(e){let t=(0,J.useContext)(Ch),[n,r]=(0,J.useState)(e);return t&&n!==e&&r(e),n}var Th=ne(),Eh=500;function Dh(e,t){let n=(0,Y.c)(5),r=t===void 0?Eh:t,i;n[0]===e?i=n[1]:(i=t=>{try{e(JSON.parse(t))}catch{}},n[0]=e,n[1]=i);let a;return n[2]!==r||n[3]!==i?(a=(0,Th.debounce)(i,r),n[2]=r,n[3]=i,n[4]=a):a=n[4],a}function Oh(e,t){let n=(0,Y.c)(6),r=(0,J.useRef)(null),i,a;n[0]===e?(i=n[1],a=n[2]):(i=()=>{r.current=e},a=[e],n[0]=e,n[1]=i,n[2]=a),(0,J.useEffect)(i,a);let o,s;n[3]===t?(o=n[4],s=n[5]):(o=()=>{if(typeof t!=`number`)return;let e=t,n=function(){r.current?.()},i=setInterval(n,e),a=function(){document.visibilityState===`hidden`?i!=null&&(clearInterval(i),i=null):i??=(n(),setInterval(n,e))};return document.addEventListener(`visibilitychange`,a),()=>{i!=null&&clearInterval(i),document.removeEventListener(`visibilitychange`,a)}},s=[t],n[3]=t,n[4]=o,n[5]=s),(0,J.useEffect)(o,s)}var kh=.05,Ah=({word:e,theme:t})=>{let n=e.charCodeAt(0),r=Le(n%26/26),i=t===`light`?3:5,a=t===`light`?`#fdfdfd`:`#0E0E0E`,o=k(r,a);for(;o<i;)r=t===`light`?ye(kh,r):de(kh,r),o=k(r,a);return r},jh=e=>{let t=(0,Y.c)(3),{theme:n}=Mr(),r;return t[0]!==n||t[1]!==e?(r=Ah({word:e,theme:n}),t[0]=n,t[1]=e,t[2]=r):r=t[2],r};function Mh(e,t){let n=new Intl.DateTimeFormat(e,{...t});return e=>n.format(e)}function Nh(e){let{locale:t,timeZone:n}=e;return Mh(t,{year:`numeric`,month:`2-digit`,day:`2-digit`,hour:`2-digit`,minute:`2-digit`,second:`2-digit`,hour12:!0,timeZone:n})}function Ph(e){let{locale:t,timeZone:n}=e;return Mh(t,{hour:`2-digit`,minute:`2-digit`,hour12:!0,timeZone:n})}function Fh(e){let{locale:t,timeZone:n}=e;return Mh(t,{year:`numeric`,month:`2-digit`,day:`2-digit`,hour:`2-digit`,minute:`2-digit`,hour12:!0,timeZone:n})}function Ih(e){let t=Fh(e);return e=>e.start&&e.end?`${t(e.start)} - ${t(e.end)}`:e.start?`From ${t(e.start)}`:e.end?`Until ${t(e.end)}`:`All Time`}function Lh(e){let{timeZone:t,locale:n}=e;return Intl.DateTimeFormat(n,{timeZoneName:`short`,timeZone:t}).formatToParts().find(e=>e.type===`timeZoneName`)?.value}function Rh(e,t=Date.now()){if(e===0)return``;let n=t-e;return n<216e5?new Date(e).toLocaleTimeString(void 0,{hour:`numeric`,minute:`2-digit`}):n<864e5?`${Math.floor(n/ca)}h`:`${Math.floor(n/la)}d`}function zh(e){return new Intl.DateTimeFormat(e,{day:`2-digit`,month:`2-digit`,year:`numeric`}).formatToParts(new Date).map(e=>{switch(e.type){case`day`:return`dd`;case`month`:return`mm`;case`year`:return`yyyy`;case`literal`:return e.value;default:return``}}).join(``)}function Bh(){let e=(0,Y.c)(2),{locale:t}=ht(),n;return e[0]===t?n=e[1]:(n=zh(t),e[0]=t,e[1]=n),n}var Vh=e=>{let t=(0,Y.c)(3),[n,r]=(0,J.useState)(null),i,a;return t[0]===e?(i=t[1],a=t[2]):(i=()=>{if(!e.current)return;let t=new ResizeObserver(e=>{if(!e||e.length===0)return;let{width:t,height:n}=e[0].contentRect;r({width:t,height:n})});return t.observe(e.current),()=>{t.disconnect()}},a=[e],t[0]=e,t[1]=i,t[2]=a),(0,J.useEffect)(i,a),n};function Hh(){let e=(0,Y.c)(10),t=hi(Uh),n,r,i,a;if(e[0]!==t){let o=t??oi();n=Nh({locale:ai(),timeZone:o}),r=Ph({locale:ai(),timeZone:o}),i=Fh({locale:ai(),timeZone:o}),a=Ih({locale:ai(),timeZone:o}),e[0]=t,e[1]=n,e[2]=r,e[3]=i,e[4]=a}else n=e[1],r=e[2],i=e[3],a=e[4];let o;return e[5]!==n||e[6]!==r||e[7]!==i||e[8]!==a?(o={fullTimeFormatter:n,shortTimeFormatter:r,shortDateTimeFormatter:i,timeRangeFormatter:a},e[5]=n,e[6]=r,e[7]=i,e[8]=a,e[9]=o):o=e[9],o}function Uh(e){return e.displayTimezone}function Wh(e={}){let{updateIntervalMs:t=null}=e,[n,r]=(0,J.useState)(()=>Date.now());return(0,J.useEffect)(()=>{if(typeof t!=`number`)return;let e=setInterval(()=>{r(Date.now())},t);return()=>clearInterval(e)},[t]),{nowEpochMs:n}}function Gh(e){let t=(0,Y.c)(2),n;return t[0]===e?n=t[1]:(n=wp(e),t[0]=e,t[1]=n),n}var Kh=`https://pypi.org/pypi/arize-phoenix/json`,qh=null;function Jh(){return qh??=fetch(Kh).then(e=>e.ok?e.json():null).then(e=>{let t=e?.info?.version;return typeof t==`string`?t:null}).catch(()=>null).then(e=>(e??(qh=null),e)),qh}function Yh(){let e=(0,Y.c)(2),[t,n]=(0,J.useState)(null),r,i;return e[0]===Symbol.for(`react.memo_cache_sentinel`)?(r=()=>{let e=!0;return Jh().then(t=>{e&&n(t)}),()=>{e=!1}},i=[],e[0]=r,e[1]=i):(r=e[0],i=e[1]),(0,J.useEffect)(r,i),t}function Xh(e,t){let[n,r]=(0,J.useState)(()=>{try{let n=localStorage.getItem(e);return n?JSON.parse(n):t}catch{return t}});return[n,(0,J.useCallback)(t=>{r(n=>{let r=typeof t==`function`?t(n):t;try{localStorage.setItem(e,JSON.stringify(r))}catch{}return r})},[e])]}function Zh(e){let{query:t,queryRef:n}=e,[r]=(0,vi.useQueryLoader)(t,n);return Qe(r,`ownedQueryRef is required when initialized from queryRef`),(0,vi.usePreloadedQuery)(t,r)}function Qh(){let e=(0,Y.c)(7),[t,n]=$n(),r;e[0]===t?r=e[1]:(r=t.getAll(ad),e[0]=t,e[1]=r);let i=r,a;e[2]===n?a=e[3]:(a=e=>{n(t=>{let n=t.getAll(ad),r=typeof e==`function`?e(n):e,i=new URLSearchParams(t);return i.delete(ad),r.forEach(e=>i.append(ad,e)),i},{replace:!0})},e[2]=n,e[3]=a);let o=a,s;return e[4]!==i||e[5]!==o?(s=[i,o],e[4]=i,e[5]=o,e[6]=s):s=e[6],s}function $h(e){let t=(0,Y.c)(4),n;t[0]===e?n=t[1]:(n=t=>{let n=window.matchMedia(e);return n.addEventListener(`change`,t),()=>n.removeEventListener(`change`,t)},t[0]=e,t[1]=n);let r=n,i;return t[2]===e?i=t[3]:(i=()=>window.matchMedia(e).matches,t[2]=e,t[3]=i),(0,J.useSyncExternalStore)(r,i)}function eg(e){let t=(0,Y.c)(49),{start:n,end:r,timeZone:a,isDisabled:o,onCommit:s,autoFocus:c,onBlurWithin:l,onSubmit:u,ref:d}=e,f=(0,J.useRef)(!1),p=(0,J.useRef)(!1),m=r==null,h;t[0]!==n||t[1]!==a?(h=()=>zd(n,a),t[0]=n,t[1]=a,t[2]=h):h=t[2];let[g,_]=(0,J.useState)(h),v;t[3]!==r||t[4]!==a?(v=()=>zd(r,a)??ve(a),t[3]=r,t[4]=a,t[5]=v):v=t[5];let[y,b]=(0,J.useState)(v),x;t[6]!==g||t[7]!==a?(x=g?g.toDate(a):null,t[6]=g,t[7]=a,t[8]=x):x=t[8];let S=x,C;t[9]!==y||t[10]!==a?(C=y?y.toDate(a):null,t[9]=y,t[10]=a,t[11]=C):C=t[11];let w=C,T=!!(S&&w&&S>w),E;t[12]!==r||t[13]!==n||t[14]!==a?(E=()=>{_(zd(n,a)),b(zd(r,a)??ve(a)),f.current=!1,p.current=!1},t[12]=r,t[13]=n,t[14]=a,t[15]=E):E=t[15];let D=E,O;t[16]!==w||t[17]!==m||t[18]!==s||t[19]!==D||t[20]!==S?(O=()=>{if(!f.current)return;let e=m&&!p.current?null:w;if(S&&e&&S>e){D();return}f.current=!1,s({start:S,end:e})},t[16]=w,t[17]=m,t[18]=s,t[19]=D,t[20]=S,t[21]=O):O=t[21];let k=O,A,j;t[22]===k?(A=t[23],j=t[24]):(A=()=>({commit:k}),j=[k],t[22]=k,t[23]=A,t[24]=j),(0,J.useImperativeHandle)(d,A,j);let M;t[25]!==k||t[26]!==l?(M={onBlurWithin:()=>{k(),l?.()}},t[25]=k,t[26]=l,t[27]=M):M=t[27];let{focusWithinProps:ee}=Hn(M),te=T||void 0,ne;t[28]!==k||t[29]!==u?(ne=e=>{e.key===`Enter`&&(e.preventDefault(),k(),u?.())},t[28]=k,t[29]=u,t[30]=ne):ne=t[30];let N,re;t[31]===Symbol.for(`react.memo_cache_sentinel`)?(N=e=>{_(e),f.current=!0},re=B(We,{children:ng}),t[31]=N,t[32]=re):(N=t[31],re=t[32]);let ie;t[33]!==c||t[34]!==o||t[35]!==g?(ie=B(i,{"aria-label":`Start time`,className:`time-range-selector__field`,granularity:`minute`,hideTimeZone:!0,isDisabled:o,autoFocus:c,value:g,onChange:N,children:re}),t[33]=c,t[34]=o,t[35]=g,t[36]=ie):ie=t[36];let ae;t[37]===Symbol.for(`react.memo_cache_sentinel`)?(ae=B(`span`,{"aria-hidden":!0,className:`time-range-selector__separator`,children:`–`}),t[37]=ae):ae=t[37];let oe,se;t[38]===Symbol.for(`react.memo_cache_sentinel`)?(oe=e=>{b(e),f.current=!0,p.current=!0},se=B(We,{children:tg}),t[38]=oe,t[39]=se):(oe=t[38],se=t[39]);let ce;t[40]!==y||t[41]!==o?(ce=B(i,{"aria-label":`End time`,className:`time-range-selector__field`,granularity:`minute`,hideTimeZone:!0,isDisabled:o,value:y,onChange:oe,children:se}),t[40]=y,t[41]=o,t[42]=ce):ce=t[42];let le;return t[43]!==ee||t[44]!==te||t[45]!==ne||t[46]!==ie||t[47]!==ce?(le=V(`div`,{className:`time-range-selector__fields`,"data-invalid":te,onKeyDownCapture:ne,...ee,children:[ie,ae,ce]}),t[43]=ee,t[44]=te,t[45]=ne,t[46]=ie,t[47]=ce,t[48]=le):le=t[48],le}function tg(e){return B(y,{segment:e})}function ng(e){return B(y,{segment:e})}var rg=U`
  display: inline-flex;
  align-items: center;
  gap: var(--global-dimension-size-100);
  box-sizing: border-box;
  width: fit-content;
  max-width: 100%;
  height: var(--global-input-height-s);
  padding-inline: var(--global-dimension-size-100);
  background-color: var(--global-input-field-background-color);
  border: var(--global-border-size-thin) solid
    var(--global-input-field-border-color);
  border-radius: var(--global-rounding-small);
  color: var(--global-text-color-900);
  font-size: var(--global-font-size-s);
  cursor: pointer;
  transition: border-color 0.2s ease-in-out;

  /* Match the standard input field: a single border-color change for both
     hover and focus so the two states read consistently. */
  &:hover:not([data-disabled]),
  &[data-presets-open]:not([data-disabled]) {
    border-color: var(--global-input-field-border-color-active);
  }
  &:focus-within:not([data-disabled]) {
    border-color: var(--global-input-field-border-color-active);
  }
  &:has(:focus-visible):not([data-disabled]),
  &[data-focus-visible]:not([data-disabled]) {
    outline: var(--focus-ring-thickness) solid var(--focus-ring-color);
    outline-offset: calc(-1 * var(--focus-ring-thickness));
  }
  &[data-disabled] {
    opacity: var(--global-opacity-disabled);
    cursor: not-allowed;
  }

  .time-range-selector__fields {
    flex: 0 0 auto;
    display: flex;
    align-items: center;
    gap: var(--global-dimension-size-50);
    min-width: 0;
  }

  .time-range-selector__value-shell {
    flex: 0 0 auto;
    min-width: 0;
    overflow: hidden;
    transition: width 180ms cubic-bezier(0.2, 0.9, 0.2, 1);
  }

  .time-range-selector__value-measure {
    display: inline-flex;
    align-items: center;
    width: max-content;
  }

  .time-range-selector__value {
    flex: 0 1 auto;
    min-width: 0;
    padding: 0;
    border: 0;
    background: transparent;
    color: var(--global-text-color-900);
    font: inherit;
    white-space: nowrap;
    cursor: pointer;

    &:focus {
      outline: none;
    }

    &[disabled] {
      cursor: not-allowed;
    }
  }

  .time-range-selector__separator {
    flex: none;
    color: var(--global-text-color-500);
  }

  .react-aria-DateInput {
    display: flex;
    align-items: center;
    white-space: nowrap;
    padding-block: 2px;
    width: fit-content;
    forced-color-adjust: none;
  }

  .react-aria-DateSegment {
    padding: 0 1px;
    font-variant-numeric: tabular-nums;
    color: var(--global-text-color-900);
    border-radius: var(--global-rounding-xsmall);
    transition:
      color 0.1s ease-out,
      background-color 0.1s ease-out;

    &[data-type="literal"] {
      padding: 0;
      /* Preserve the locale separator (e.g. ", ") that flex would collapse. */
      white-space: pre;
    }
    &[data-placeholder] {
      color: var(--text-color-placeholder);
      font-style: italic;
    }
    &[data-disabled] {
      color: var(--global-text-color-500);
    }
    &:focus {
      color: var(--field-editing-foreground);
      background: var(--field-editing-background);
      outline: none;
      caret-color: transparent;
    }
  }

  .time-range-selector__fields[data-invalid] .react-aria-DateSegment {
    color: var(--global-color-danger);
  }

  .time-range-selector__timezone {
    flex: none;
    white-space: nowrap;
  }

  &[data-presets-open] .time-range-selector__value-shell {
    transition: none;
  }

  @media (prefers-reduced-motion: reduce) {
    .time-range-selector__value-shell {
      transition: none;
    }
  }
`,ig=U`
  /* Fill the popover, which is sized to the field it is anchored to. */
  width: 100%;
`,ag=U`
  padding: var(--global-dimension-size-200) var(--global-dimension-size-150);
`,og=U`
  width: 100%;
  border-bottom: var(--global-border-size-thin) solid
    var(--global-menu-border-color);
`,sg=U`
  flex: none;
  font-variant-numeric: tabular-nums;
`,cg=U`
  width: 100%;
  justify-content: flex-start;
`,lg=`var(--global-dimension-size-4000)`;function ug(e){let{value:t,isDisabled:n,onChange:r,size:i=`S`}=e,{timeRangeKey:a,start:o,end:s}=t,c=(0,J.useRef)(null),l=(0,J.useRef)(null),u=(0,J.useRef)(null),d=(0,J.useRef)(null),f=(0,J.useRef)(null),p=(0,J.useRef)(null),[m,h]=(0,J.useState)(!1),[g,_]=(0,J.useState)(!1),[v,y]=(0,J.useState)(!1),[b,x]=(0,J.useState)(),[S,w]=(0,J.useState)(``),{contains:T}=C({sensitivity:`base`}),{isFocusVisible:E}=$t({isTextInput:!0}),D=g&&E,O=(0,J.useCallback)(()=>{h(!1),y(!1),w(``)},[]),k=(0,J.useCallback)(()=>{let e=document.activeElement;return e instanceof HTMLElement&&(c.current?.contains(e)||l.current?.contains(e))?e:null},[]),A=(0,J.useCallback)(()=>{setTimeout(()=>{k()||(_(!1),O())})},[O,k]),j=(0,J.useCallback)(()=>{k()?.blur()},[k]),M=(0,J.useCallback)(()=>{j(),_(!1),O()},[j,O]),ee=(0,J.useCallback)(()=>{p.current?.commit(),M()},[M]),te=(0,J.useCallback)(()=>{h(!0)},[]);Mn({ref:c,isDisabled:!m,onInteractOutside:e=>{e.target instanceof Node&&l.current?.contains(e.target)||ee()}}),Zt(`escape`,e=>{if(e.stopPropagation(),S&&document.activeElement===u.current){w(``);return}ee()},{enabled:g,enableOnFormTags:!0,enableOnContentEditable:!0,preventDefault:!0,eventListenerOptions:{capture:!0}});let ne=Vh(d),N=hi(e=>e.displayTimezone)??oi(),re=ai(),ie=Lh({locale:re,timeZone:N}),ae=a===`custom`,oe=ae?`Custom`:a,se=Ih({locale:re,timeZone:N}),ce=vd(a)?wd(a):se({start:o,end:s}),le=Od(S),ue=cd.filter(({key:e})=>!le.includes(e)),de=`${a}|${o?.getTime()??``}|${s?.getTime()??``}|${N}`,fe=ne?.width,pe=`${g}|${de}|${ce}|${oe}|${ie??``}`,me=m&&b!=null;return(0,J.useLayoutEffect)(()=>{let e=m?c.current?.offsetWidth:void 0,t=e?`${e}px`:void 0;x(e=>e===t?e:t)},[m,pe]),(0,J.useLayoutEffect)(()=>{!me||v||u.current?.focus()},[me,v]),V(R,{children:[V(`div`,{ref:c,className:`time-range-selector`,css:rg,"data-size":i,"data-disabled":n||void 0,"data-focus-visible":D||void 0,"data-presets-open":m||void 0,role:`group`,"aria-label":`Time range`,onPointerDown:e=>{if(n||g)return;let t=f.current,r=e.target instanceof Node&&t?.contains(e.target);!t||r||(e.preventDefault(),t.focus())},children:[B(es,{size:`S`,variant:ae?`info`:`default`,css:sg,children:oe}),B(`div`,{className:`time-range-selector__value-shell`,style:{width:m||fe==null?`auto`:fe,minWidth:g?lg:void 0},children:B(`div`,{ref:d,className:`time-range-selector__value-measure`,children:g?B(eg,{ref:p,start:o,end:s,timeZone:N,isDisabled:n,autoFocus:!0,onBlurWithin:A,onSubmit:M,onCommit:e=>r({timeRangeKey:`custom`,...e})},de):B(`button`,{ref:f,type:`button`,className:`time-range-selector__value`,disabled:n,onFocus:()=>{n||(_(!0),te())},children:ce})})}),ie&&B(L,{size:`XS`,color:`text-500`,className:`time-range-selector__timezone`,children:ie})]}),B(tr,{ref:l,triggerRef:c,isOpen:me,onOpenChange:e=>{e||O()},isNonModal:!0,isKeyboardDismissDisabled:!0,placement:v?`bottom end`:`bottom start`,offset:2,style:{width:v?`max-content`:b,minWidth:v?b:void 0,overflow:`hidden`,transition:`none`,animation:`none`,transform:`translateY(0)`,opacity:1},children:v?B(Wd,{value:{start:o,end:s},timeZone:N,onCancel:()=>y(!1),onApply:e=>{_(!1),O(),r({timeRangeKey:`custom`,...e})}}):V(R,{children:[V(At,{filter:T,children:[V(ys,{"aria-label":`Search time range presets`,size:`M`,variant:`quiet`,value:S,onChange:w,css:og,children:[B(_s,{}),B(Ne,{ref:u,placeholder:`Search or type "25m"`,onBlur:A})]}),V(gc,{"aria-label":`time range preset selection`,selectionMode:`single`,selectedKeys:ae?[]:[a],css:ig,renderEmptyState:()=>B(`div`,{css:ag,children:`No matching time ranges`}),onSelectionChange:e=>{let t=e===`all`?void 0:e.keys().next().value,n=vd(t)?t:vd(a)?a:void 0;if(_(!1),!n){O();return}let i=gd(n);O(),r({timeRangeKey:n,...i})},children:[le.map(e=>B(De,{id:e,textValue:S,children:wd(e)},e)),ue.map(({key:e,label:t})=>B(De,{id:e,children:t},e))]})]}),B(Ua,{children:B(H,{size:`S`,variant:`quiet`,css:cg,leadingVisual:B(z,{svg:B(dn,{})}),onPress:()=>y(!0),children:`Pick from a calendar`})})]})})]})}var dg=Wt`
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.35;
  }
`,fg=U`
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: var(--global-dimension-size-50);
  width: fit-content;
  box-sizing: border-box;
  /* Uniform inset so each button's hover pill floats evenly in the shell. */
  padding: var(--global-dimension-size-50);
  background-color: var(--global-input-field-background-color);
  border: var(--global-border-size-thin) solid
    var(--global-input-field-border-color);
  border-radius: var(--global-rounding-small);

  /* Buttons get an explicit square (shell height minus border and padding):
     Safari resolves stretch + aspect-ratio inconsistently between Button
     and ToggleButton. */
  &[data-size="S"] {
    height: var(--global-input-height-s);
    --time-range-controls-button-size: calc(
      var(--global-input-height-s) - 2 *
        (var(--global-dimension-size-50) + var(--global-border-size-thin))
    );
  }
  &[data-size="M"] {
    height: var(--global-input-height-m);
    --time-range-controls-button-size: calc(
      var(--global-input-height-m) - 2 *
        (var(--global-dimension-size-50) + var(--global-border-size-thin))
    );
  }

  /* Fade the whole shell as one unit, not each button twice over. */
  &[data-disabled] {
    opacity: var(--global-opacity-disabled);
    button[disabled] {
      opacity: 1;
    }
  }
`,pg=U`
  position: relative;
  border: none;
  background-color: transparent;
  border-radius: var(--global-rounding-xsmall);
  color: var(--global-text-color-700);
  transition:
    background-color 0.2s ease-in-out,
    color 0.2s ease-in-out;

  /* Double attribute selector outranks the base button's height and
     childless min-width. */
  &[data-size][data-childless] {
    flex: none;
    width: var(--time-range-controls-button-size);
    min-width: var(--time-range-controls-button-size);
    height: var(--time-range-controls-button-size);
    padding: 0;
  }

  /* An outset focus ring would spill past the shell border. */
  &[data-focus-visible],
  &:focus-visible {
    outline-offset: calc(-1 * var(--focus-ring-thickness));
  }

  /* One optical size for glyphs from both icon families. */
  .icon-wrap {
    font-size: var(--global-font-size-s);
  }

  /* Solid play/pause glyphs give the center control a media-transport feel
     and anchor it against the stroked pan/zoom icons around it. */
  &.time-range-controls__live-toggle .icon-wrap svg :is(path, rect) {
    fill: currentColor;
  }

  &:hover:not([disabled]),
  &[data-hovered]:not([data-disabled]):not([data-selected="true"]) {
    background-color: var(--global-input-field-background-color-active);
    color: var(--global-text-color-900);
  }

  /* Streaming live uses a gently pulsing neutral tint so the center control
     doesn't compete with status colors elsewhere. The tint lives on an
     overlay so the pulse composes from the static token instead of
     animating between raw colors. */
  &[data-selected="true"] {
    isolation: isolate;
    background-color: transparent;
    color: var(--global-text-color-900);
    &:hover:not([data-disabled]) {
      background-color: var(--global-input-field-background-color-active);
    }
    &::before {
      content: "";
      position: absolute;
      inset: 0;
      z-index: -1;
      border-radius: inherit;
      background-color: var(--global-input-field-background-color-active);
      animation: ${dg} 3s ease-in-out infinite;
    }
  }

  @media (prefers-reduced-motion: reduce) {
    &[data-selected="true"]::before {
      animation: none;
    }
  }
`;function mg(e){let t=(0,Y.c)(13),{label:n,icon:r,size:i,isDisabled:a,onPress:o}=e,s;t[0]===r?s=t[1]:(s=B(z,{svg:r}),t[0]=r,t[1]=s);let c;t[2]!==a||t[3]!==n||t[4]!==o||t[5]!==i||t[6]!==s?(c=B(H,{size:i,variant:`quiet`,css:pg,"aria-label":n,isDisabled:a,leadingVisual:s,onPress:o}),t[2]=a,t[3]=n,t[4]=o,t[5]=i,t[6]=s,t[7]=c):c=t[7];let l;t[8]===n?l=t[9]:(l=B(ia,{children:n}),t[8]=n,t[9]=l);let u;return t[10]!==c||t[11]!==l?(u=V(Se,{children:[c,l]}),t[10]=c,t[11]=l,t[12]=u):u=t[12],u}function hg(e){let{value:t,onChange:n,isLive:r=!1,onIsLiveChange:i,isDisabled:a,size:o=`S`}=e,s=t.start!=null,c=r?`Stop live streaming`:`Resume live streaming`,l=t.end==null,u=e=>{e&&n(e)};return V(`div`,{className:`time-range-controls`,css:fg,role:`group`,"aria-label":`Time range controls`,"data-size":o,"data-disabled":a||void 0,children:[B(mg,{label:`Pan back in time`,icon:B(cn,{}),size:o,isDisabled:a||!s,onPress:()=>u(Pd({value:t}))}),B(mg,{label:`Zoom out`,icon:B(rt,{}),size:o,isDisabled:a||!s,onPress:()=>u(Ld({value:t}))}),i&&V(Se,{children:[B(ic,{size:o,className:`time-range-controls__live-toggle`,css:pg,"aria-label":c,isSelected:r,isDisabled:a,leadingVisual:B(z,{svg:B(r?Pt:wn,{})}),onChange:i}),B(ia,{children:c})]}),B(mg,{label:`Zoom in`,icon:B(jt,{}),size:o,isDisabled:a||!s,onPress:()=>u(Id({value:t}))}),B(mg,{label:`Pan forward in time`,icon:B(er,{}),size:o,isDisabled:a||!s||l,onPress:()=>u(Fd({value:t}))})]})}function gg({size:e=`S`}){let{timeRange:t,setTimeRange:n}=ph();return B(ug,{value:t,onChange:n,size:e})}function _g(e){let t=(0,Y.c)(4),{timeRange:n,setTimeRange:r}=ph(),i;return t[0]!==e||t[1]!==r||t[2]!==n?(i=B(hg,{...e,value:n,onChange:r}),t[0]=e,t[1]=r,t[2]=n,t[3]=i):i=t[3],i}U`
  display: flex;
  flex-direction: column;
  gap: var(--global-dimension-size-200);
`,U`
  display: flex;
  gap: var(--global-dimension-size-100);
  align-items: start;
  justify-content: end;
  /* Move the button down to align */
  button {
    margin-top: 26px;
  }
`,U`
  width: 100%;
  display: flex;
  justify-content: flex-end;
  gap: var(--global-dimension-size-100);
`,U`
  width: 100%;
  .react-aria-DateInput {
    width: 100%;
    // Eliminate the re-sizing of the DateField as you type
    min-width: 200px;
  }
`;var vg=Wt`
  to {
    --ai-conic-angle: 405deg;
  }
`,yg=Wt`
  0%, 100% {
    box-shadow: var(--ai-glow-box-shadow-rest);
  }
  50% {
    box-shadow: var(--ai-glow-box-shadow-strong);
  }
`,bg=Wt`
  0% {
    -webkit-mask-position: 170% center;
    mask-position: 170% center;
  }

  100% {
    -webkit-mask-position: -70% center;
    mask-position: -70% center;
  }
`,xg=Wt`
  0%, 100% {
    box-shadow: var(--ai-glow-box-shadow-contained-rest);
  }
  50% {
    box-shadow: var(--ai-glow-box-shadow-contained-strong);
  }
`,Sg=Wt`
  0% {
    opacity: 0;
    -webkit-mask-position: 200% center;
    mask-position: 200% center;
  }
  8% {
    opacity: 1;
  }
  40% {
    opacity: 1;
  }
  55% {
    opacity: 0;
    -webkit-mask-position: -60% center;
    mask-position: -60% center;
  }
  100% {
    opacity: 0;
    -webkit-mask-position: -60% center;
    mask-position: -60% center;
  }
`,Cg=Wt`
  0%, 100% {
    opacity: 0;
  }
  8%, 40% {
    opacity: var(--ai-glow-opacity);
  }
  55% {
    opacity: 0;
  }
`,wg=U`
  opacity: 0;
  mix-blend-mode: plus-lighter;
  -webkit-mask-image: linear-gradient(
    90deg,
    transparent 15%,
    black 45%,
    black 55%,
    transparent 85%
  );
  mask-image: linear-gradient(
    90deg,
    transparent 15%,
    black 45%,
    black 55%,
    transparent 85%
  );
  -webkit-mask-size: 200% 200%;
  mask-size: 200% 200%;
  -webkit-mask-repeat: no-repeat;
  mask-repeat: no-repeat;
  -webkit-mask-position: 200% center;
  mask-position: 200% center;
`,Tg=U`
  -webkit-mask-position: center;
  mask-position: center;
  animation: ${bg} var(--ai-glow-wipe-continuous-duration)
    linear infinite both var(--ai-glow-wipe-continuous-delay);
`,Eg=U`
  background: conic-gradient(
    from var(--ai-conic-angle),
    var(--ai-gradient-color-start),
    var(--ai-gradient-color-middle),
    var(--ai-gradient-color-end),
    var(--ai-gradient-color-start)
  );
`,Dg=U`
  ${Eg};
  padding: var(--ai-conic-band-stroke-width);
  -webkit-mask:
    linear-gradient(#000 0 0) content-box,
    linear-gradient(#000 0 0);
  mask:
    linear-gradient(#000 0 0) content-box,
    linear-gradient(#000 0 0);
  -webkit-mask-composite: xor;
  mask-composite: exclude;
`,Og=U`
  --ai-conic-band-stroke-width: 1.5px;
  --ai-outline-gap: var(--global-dimension-static-size-25);
  --ai-outline-target-radius: var(--global-rounding-small);
  position: relative;
  display: inline-grid;
  width: fit-content;
  max-width: 100%;
  min-width: 0;
  vertical-align: middle;
  isolation: isolate;
  border-radius: var(--ai-outline-target-radius);

  &[data-full-width="true"] {
    display: grid;
    width: 100%;
  }

  &[data-radius="medium"] {
    --ai-outline-target-radius: var(--global-rounding-medium);
  }

  .ai-outline__stroke,
  .ai-outline__glow {
    position: absolute;
    pointer-events: none;
  }

  .ai-outline__stroke {
    ${Dg};
    inset: calc(
      -1 * (var(--ai-outline-gap) + var(--ai-conic-band-stroke-width))
    );
    z-index: 2;
    border-radius: calc(
      var(--ai-outline-target-radius) + var(--ai-outline-gap) +
        var(--ai-conic-band-stroke-width)
    );
    opacity: 0.3;
    animation: ${vg} var(--ai-conic-spin-duration) linear infinite
      paused;
  }

  .ai-outline__glow {
    ${wg};
    inset: calc(
      -1 *
        (var(--ai-outline-gap) + var(--ai-conic-band-stroke-width) +
          var(--ai-glow-bleed))
    );
    z-index: 0;
    border-radius: calc(
      var(--ai-outline-target-radius) + var(--ai-outline-gap) +
        var(--ai-conic-band-stroke-width)
    );
  }

  .ai-outline__glow::before {
    content: "";
    position: absolute;
    inset: var(--ai-glow-bleed);
    border-radius: inherit;
    box-shadow: var(--ai-glow-box-shadow-rest);
    opacity: 0;
  }

  /* Eligible keeps the band's subtle rotation running at resting opacity
     so an engaged-but-idle target still reads as alive */
  &[data-state="eligible"] .ai-outline__stroke {
    opacity: 0.64;
    animation-play-state: running;
  }

  &[data-state="active"] .ai-outline__stroke {
    opacity: 1;
    animation-play-state: running;
  }

  /* Active gets the thinking glow: the breathing glow clipped by the
     traveling wipe, matching PxiButton's working state */
  &[data-state="active"] .ai-outline__glow {
    opacity: 1;
    ${Tg};
  }

  &[data-state="active"] .ai-outline__glow::before {
    opacity: 0.72;
    animation: ${yg} var(--ai-glow-wipe-duration) ease-in-out
      infinite;
  }

  &[data-state="eligible"][data-should-flash="true"] .ai-outline__glow {
    animation: ${Sg} var(--ai-glow-wipe-duration)
      var(--ai-glow-wipe-easing) 1;
  }

  &[data-state="eligible"][data-should-flash="true"] .ai-outline__glow::before {
    animation:
      ${yg} var(--ai-glow-wipe-duration) ease-in-out 1,
      ${Cg} var(--ai-glow-wipe-duration) linear 1;
  }

  &[data-glow-mode="contained"] {
    .ai-outline__stroke {
      inset: 0;
      border-radius: var(--ai-outline-target-radius);
    }

    .ai-outline__glow {
      inset: 0;
      border-radius: var(--ai-outline-target-radius);
    }

    .ai-outline__glow::before {
      inset: 0;
      box-shadow: var(--ai-glow-box-shadow-contained-rest);
    }

    &[data-state="active"] .ai-outline__glow::before {
      animation-name: ${xg};
    }

    &[data-state="eligible"][data-should-flash="true"]
      .ai-outline__glow::before {
      animation-name: ${xg}, ${Cg};
    }
  }

  @media (prefers-reduced-motion: reduce) {
    .ai-outline__stroke {
      animation-play-state: paused;
    }

    .ai-outline__glow,
    .ai-outline__glow::before {
      animation: none !important;
    }
  }
`;function kg({children:e,className:t,css:n,isFullWidth:r=!1,glowMode:i=`outer`,radius:a=`small`,shouldFlash:o=!1,state:s=`idle`}){let c=s===`eligible`&&o,l=(0,J.useMemo)(()=>U(Og,n),[n]);return V(`div`,{className:F(`ai-outline`,t),css:l,"data-full-width":r?`true`:void 0,"data-glow-mode":i,"data-radius":a,"data-should-flash":c?`true`:void 0,"data-state":s,children:[B(`span`,{className:`ai-outline__glow`,"aria-hidden":`true`}),B(`span`,{className:`ai-outline__stroke`,"aria-hidden":`true`}),e]})}var Ag=(0,J.createContext)(null);function jg(){return(0,J.useContext)(Ag)??{variant:`grid`}}var Mg=U`
  display: flex;
  align-items: flex-start;
  gap: var(--global-dimension-size-75);

  &[data-variant="grid"] {
    flex-wrap: wrap;
    margin-left: auto;
    width: fit-content;
  }

  &[data-variant="inline"] {
    flex-wrap: wrap;
    padding: var(--global-dimension-size-150) var(--global-dimension-size-150) 0;
  }

  &[data-variant="list"] {
    flex-direction: column;
    width: 100%;
  }

  /* Collapsible inline stack: at rest only the front chip shows, the rest tuck
     behind it as a deck peeking out by a sliver; hover/focus fans it out. */
  &[data-variant="inline"][data-collapsible] {
    --attachment-stack-separator-color: var(--global-background-color-default);
    /* Sliver each card behind the front peeks out by, and the width of a
       collapsed card before it is overlapped. */
    --attachment-stack-peek: var(--global-dimension-size-50);
    --attachment-stack-card: var(--global-dimension-size-200);

    flex-wrap: nowrap;
    gap: 0;
    transition: gap 0.2s ease;

    > [data-attachment] {
      position: relative;
      box-shadow: 0 0 0 var(--global-border-size-thin)
        var(--attachment-stack-separator-color);
      transition:
        width 0.2s ease,
        min-width 0.2s ease,
        padding 0.2s ease,
        margin-left 0.2s ease;
    }

    /* Collapse every chip but the front to a narrow card with clipped contents. */
    > [data-attachment]:not(:last-child) {
      width: var(--attachment-stack-card);
      min-width: var(--attachment-stack-card);
      padding: 0;
      overflow: hidden;
    }

    > [data-attachment]:not(:last-child) > * {
      opacity: 0;
      transition: opacity 0.2s ease;
    }

    /* Slide each card under its predecessor; later cards paint on top. */
    > [data-attachment] + [data-attachment] {
      margin-left: calc(
        var(--attachment-stack-peek) - var(--attachment-stack-card)
      );
    }

    .attachment-info__detail {
      max-width: 0;
      opacity: 0;
      margin-left: 0;
      transition:
        max-width 0.2s ease,
        opacity 0.2s ease,
        margin 0.2s ease;
    }
  }

  &[data-variant="inline"][data-collapsible]:hover,
  &[data-variant="inline"][data-collapsible]:focus-within {
    flex-wrap: wrap;
    gap: var(--global-dimension-size-75);

    > [data-attachment]:not(:last-child) {
      width: auto;
      min-width: 0;
      padding: 0 var(--global-dimension-size-100);
      overflow: visible;
    }

    > [data-attachment]:not(:last-child) > * {
      opacity: 1;
    }

    > [data-attachment] + [data-attachment] {
      margin-left: 0;
    }

    .attachment-info__detail {
      max-width: var(--global-dimension-size-3000);
      opacity: 1;
      margin-left: var(--global-dimension-size-50);
    }
  }
`,Ng=U`
  position: relative;
  box-sizing: border-box;

  &[data-variant="grid"] {
    width: var(--global-dimension-size-1200);
    height: var(--global-dimension-size-1200);
    overflow: hidden;
    border-radius: var(--global-rounding-medium);
    background-color: var(--global-color-gray-200);
  }

  &[data-variant="inline"] {
    --attachment-base-color: var(--global-color-info);
    --attachment-bg-color: lch(
      from var(--attachment-base-color) 96 calc(c * 0.3) h
    );
    --attachment-border-color: lch(
      from var(--attachment-base-color) 88 calc(c * 0.4) h
    );
    --attachment-text-color: lch(from var(--attachment-base-color) 45 c h);
    --attachment-detail-color: lch(
      from var(--attachment-base-color) 55 c h / 0.75
    );

    display: inline-flex;
    align-items: center;
    gap: var(--global-dimension-size-75);
    height: var(--global-dimension-size-300);
    padding: 0 var(--global-dimension-size-100);
    border: var(--global-border-size-thin) solid var(--attachment-border-color);
    border-radius: var(--global-rounding-medium);
    background-color: var(--attachment-bg-color);
    color: var(--attachment-text-color);
    font-size: var(--global-font-size-s);
    line-height: 1;
    user-select: none;
  }

  &[data-variant="inline"][data-theme="dark"] {
    --attachment-bg-color: lch(
      from var(--attachment-base-color) 18 calc(c * 0.2) h
    );
    --attachment-border-color: lch(
      from var(--attachment-base-color) 28 calc(c * 0.3) h
    );
    --attachment-text-color: lch(
      from var(--attachment-base-color) 90 calc(c * 0.8) h
    );
    --attachment-detail-color: lch(
      from var(--attachment-base-color) 78 calc(c * 0.6) h / 0.8
    );
  }

  &[data-variant="list"] {
    display: flex;
    align-items: center;
    gap: var(--global-dimension-size-150);
    width: 100%;
    padding: var(--global-dimension-size-150);
    border: var(--global-border-size-thin) solid var(--global-border-color);
    border-radius: var(--global-rounding-medium);
  }
`,Pg=U`
  flex: none;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  color: inherit;

  &[data-variant="grid"] {
    width: 100%;
    height: 100%;
    background-color: var(--global-color-gray-200);
  }

  &[data-variant="inline"] {
    width: var(--global-dimension-size-200);
    height: var(--global-dimension-size-200);
    .icon-wrap {
      font-size: var(--global-font-size-s);
      line-height: 0;
    }
  }

  &[data-variant="list"] {
    width: var(--global-dimension-size-500);
    height: var(--global-dimension-size-500);
    border-radius: var(--global-rounding-small);
    background-color: var(--global-color-gray-200);
  }

  img,
  video {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }
`,Fg=U`
  min-width: 0;
  flex: 1 1 auto;

  .attachment-info__label {
    display: block;
    overflow: hidden;
    white-space: nowrap;
    text-overflow: ellipsis;
  }

  .attachment-info__media-type {
    display: block;
    overflow: hidden;
    white-space: nowrap;
    text-overflow: ellipsis;
    color: var(--global-text-color-500);
    font-size: var(--global-font-size-xs);
  }

  /* Chips with a secondary detail lay label + dimmed detail on one row. */
  &.attachment-info--with-detail {
    display: inline-flex;
    align-items: baseline;
    overflow: hidden;

    .attachment-info__label {
      flex: 0 0 auto;
    }

    .attachment-info__detail {
      flex: 0 1 auto;
      min-width: 0;
      overflow: hidden;
      white-space: nowrap;
      text-overflow: ellipsis;
      color: var(--attachment-detail-color);
      font-variant-numeric: tabular-nums;
    }
  }
`;U`
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border: none;
  background: transparent;
  color: inherit;
  cursor: pointer;
  padding: 0;
  outline: none;
  transition: opacity 0.2s ease;

  &[data-variant="grid"] {
    ${fu}
    position: absolute;
    top: var(--global-dimension-size-75);
    right: var(--global-dimension-size-75);
    width: var(--global-dimension-size-300);
    height: var(--global-dimension-size-300);
    border-radius: 50%;
    background-color: var(--global-color-gray-50);
  }

  &[data-variant="inline"] {
    ${fu}
    width: var(--global-dimension-size-200);
    height: var(--global-dimension-size-200);
  }

  &[data-variant="list"] {
    width: var(--global-dimension-size-400);
    height: var(--global-dimension-size-400);
    border-radius: var(--global-rounding-small);
    flex: none;
  }

  [data-attachment]:hover &[data-variant="grid"],
  [data-attachment]:hover &[data-variant="inline"] {
    opacity: 1;
  }

  &[data-focus-visible] {
    outline: var(--focus-ring-thickness) solid var(--focus-ring-color);
    outline-offset: var(--focus-ring-offset);
  }

  .icon-wrap {
    font-size: var(--global-font-size-s);
    line-height: 0;
  }
`;function Ig({children:e,ref:t,variant:n=`grid`,collapsible:r=!1,...i}){let a=(0,J.useMemo)(()=>({variant:n}),[n]);return B(Ag.Provider,{value:a,children:B(`div`,{ref:t,css:Mg,"data-variant":n,"data-collapsible":r||void 0,...i,children:e})})}var Lg=(0,J.createContext)(null);function Rg(){let e=(0,J.useContext)(Lg);if(!e)throw Error(`useAttachmentContext must be used within an <Attachment> component`);return e}function zg(e){if(e.type===`context`)return`context`;if(e.type===`source-document`)return`source`;let t=e.mediaType??``;return t.startsWith(`image/`)?`image`:t.startsWith(`video/`)?`video`:t.startsWith(`audio/`)?`audio`:t.startsWith(`application/`)||t.startsWith(`text/`)?`document`:`unknown`}function Bg(e){return e.type===`context`?e.label:e.type===`source-document`?e.title||e.filename||`Source`:e.filename||(zg(e)===`image`?`Image`:`Attachment`)}function Vg(e){return e.type===`context`?e.detail:void 0}function Hg(e){switch(e){case`project`:return B(z,{svg:B(pn,{})});case`trace`:return B(z,{svg:B(pn,{})});case`session`:return B(z,{svg:B(Qn,{})});case`span`:return B(z,{svg:B(An,{})});case`span_filter`:return B(z,{svg:B(kn,{})});case`dataset`:return B(z,{svg:B(Mt,{})});case`playground`:return B(z,{svg:B(kt,{})});case`code_evaluator`:return B(z,{svg:B(Rt,{})});case`llm_evaluator`:return B(z,{svg:B(Xt,{})});default:return B(z,{svg:B(Un,{})})}}function Ug(e){if(e.type===`context`)return e.icon??Hg(e.category);switch(zg(e)){case`image`:return B(z,{svg:B(Nn,{})});case`video`:return B(z,{svg:B(kt,{})});case`audio`:return B(z,{svg:B(pt,{})});case`document`:return B(z,{svg:B(Ct,{})});case`source`:return B(z,{svg:B(Vn,{})});default:return B(z,{svg:B(pt,{})})}}function Wg(e){let t=(0,Y.c)(22),n,r,i,a,o;t[0]===e?(n=t[1],r=t[2],i=t[3],a=t[4],o=t[5]):({children:n,ref:a,data:r,onRemove:i,...o}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a,t[5]=o);let{variant:s}=jg(),{theme:c}=Mr(),l;t[6]===r?l=t[7]:(l=zg(r),t[6]=r,t[7]=l);let u=l,d;t[8]!==r||t[9]!==u||t[10]!==i||t[11]!==s?(d={data:r,mediaCategory:u,variant:s,onRemove:i},t[8]=r,t[9]=u,t[10]=i,t[11]=s,t[12]=d):d=t[12];let f=d,p;t[13]!==n||t[14]!==a||t[15]!==o||t[16]!==c||t[17]!==s?(p=B(`div`,{ref:a,css:Ng,"data-attachment":``,"data-variant":s,"data-theme":c,...o,children:n}),t[13]=n,t[14]=a,t[15]=o,t[16]=c,t[17]=s,t[18]=p):p=t[18];let m;return t[19]!==p||t[20]!==f?(m=B(Lg.Provider,{value:f,children:p}),t[19]=p,t[20]=f,t[21]=m):m=t[21],m}function Gg(e){let t=(0,Y.c)(16),n,r,i;t[0]===e?(n=t[1],r=t[2],i=t[3]):({ref:r,fallback:n,...i}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i);let{data:a,mediaCategory:o,variant:s}=Rg(),c;t[4]!==a||t[5]!==n||t[6]!==o?(c=()=>a.type===`file`&&o===`image`&&typeof a.url==`string`&&a.url?B(`img`,{src:a.url,alt:a.filename??`Image`}):a.type===`file`&&o===`video`&&typeof a.url==`string`&&a.url?B(`video`,{src:a.url,muted:!0}):n??Ug(a),t[4]=a,t[5]=n,t[6]=o,t[7]=c):c=t[7];let l=c,u;t[8]===l?u=t[9]:(u=l(),t[8]=l,t[9]=u);let d;return t[10]!==o||t[11]!==r||t[12]!==i||t[13]!==u||t[14]!==s?(d=B(`div`,{ref:r,css:Pg,"data-variant":s,"data-media-category":o,...i,children:u}),t[10]=o,t[11]=r,t[12]=i,t[13]=u,t[14]=s,t[15]=d):d=t[15],d}function Kg({ref:e,showMediaType:t=!1,...n}){let{data:r,variant:i}=Rg();if(i===`grid`)return null;let a=Bg(r),o=Vg(r),s=r.type===`file`||r.type===`source-document`?r.mediaType:void 0;return V(`div`,{ref:e,css:Fg,className:F(`attachment-info`,{"attachment-info--with-detail":o}),...n,children:[B(`span`,{className:`attachment-info__label`,children:a}),o?B(`span`,{className:`attachment-info__detail`,children:o}):null,t&&s?B(`span`,{className:`attachment-info__media-type`,children:s}):null]})}var qg=U`
  display: flex;
  flex-direction: column;

  .elicitation__header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: var(--global-dimension-size-150) var(--global-dimension-size-200)
      var(--global-dimension-size-50);
  }

  .elicitation__step-label {
    font-size: var(--global-font-size-xxs);
    font-weight: 600;
    color: var(--global-text-color-500);
    text-transform: uppercase;
    letter-spacing: 0.05em;
  }

  .elicitation__dots {
    display: flex;
    gap: var(--global-dimension-size-75);
  }

  .elicitation__dot {
    width: 8px;
    height: 8px;
    border-radius: var(--global-rounding-full);
    border: none;
    cursor: pointer;
    padding: 0;
    transition: background-color 0.2s ease;
  }

  .elicitation__dot--active {
    background-color: var(--global-text-color-900);
  }

  .elicitation__dot--inactive {
    background-color: var(--global-text-color-300);
  }

  .elicitation__body {
    position: relative;
    overflow: hidden;
  }

  .elicitation__question-content {
    padding: var(--global-dimension-size-100) var(--global-dimension-size-200)
      var(--global-dimension-size-150);
  }

  .elicitation__prompt {
    font-size: var(--global-font-size-s);
    font-weight: 500;
    color: var(--global-text-color-900);
    margin-bottom: var(--global-dimension-size-150);
    line-height: var(--global-line-height-s);
  }

  .elicitation__options {
    display: flex;
    flex-direction: column;
    gap: var(--global-dimension-size-75);
  }

  .elicitation__freeform {
    width: 100%;
    min-height: 100px;
    background: transparent;
    color: var(--global-text-color-900);
    border: var(--global-border-size-thin) solid
      var(--global-border-color-default);
    border-radius: var(--global-rounding-medium);
    outline: none;
    resize: none;
    padding: var(--global-dimension-size-125) var(--global-dimension-size-150);
    font-size: var(--global-font-size-s);
    font-family: inherit;
    line-height: var(--global-line-height-s);
    box-sizing: border-box;
    transition: border-color 0.15s ease;

    &::placeholder {
      color: var(--global-text-color-300);
    }

    &:focus {
      border-color: var(--global-color-primary);
    }
  }

  .elicitation__nav {
    display: flex;
    justify-content: space-between;
    padding: var(--global-dimension-size-50) var(--global-dimension-size-200)
      var(--global-dimension-size-150);
  }

  .elicitation__nav-group {
    display: flex;
    gap: var(--global-dimension-size-100);
  }

  .elicitation__nav .react-aria-Button {
    font-size: var(--global-font-size-xs);
  }
`,Jg=U`
  display: flex;
  align-items: flex-start;
  gap: var(--global-dimension-size-125);
  width: 100%;
  padding: var(--global-dimension-size-125) var(--global-dimension-size-150);
  border: var(--global-border-size-thin) solid
    var(--global-border-color-default);
  border-radius: var(--global-rounding-medium);
  cursor: pointer;
  font-size: var(--global-font-size-s);
  font-family: inherit;
  text-align: left;
  box-sizing: border-box;
  background: transparent;
  color: var(--global-text-color-500);

  .theme--light & {
    color: var(--global-text-color-600);
  }

  transition:
    border-color 0.15s ease,
    background-color 0.15s ease,
    color 0.15s ease;

  &:focus-visible {
    outline: var(--focus-ring-thickness) solid var(--focus-ring-color);
    outline-offset: var(--focus-ring-offset);
  }

  &[data-selected="true"] {
    background: rgba(var(--global-color-gray-900-rgb), 0.06);
    border-color: var(--global-text-color-700);
    color: var(--global-text-color-900);

    .theme--light & {
      background: var(--global-color-gray-75);
      border-color: var(--global-color-gray-600);
    }
  }

  .option-button__indicator {
    width: 18px;
    height: 18px;
    box-sizing: border-box;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    margin-top: 1px;
    transition: all 200ms;
  }

  .option-button__indicator--radio {
    border-radius: 50%;
    border: 2px solid var(--global-input-field-border-color);
    background: var(--global-input-field-background-color);
  }

  .option-button__indicator--checkbox {
    width: 16px;
    height: 16px;
    border-radius: var(--global-rounding-small);
    border: 2px solid var(--global-checkbox-border-color);
    background: transparent;
  }

  .option-button__indicator--checkbox svg {
    width: 1rem;
    height: 1rem;
    fill: none;
    stroke: var(--global-checkbox-checkmark-color);
    stroke-width: 3px;
    stroke-dasharray: 22px;
    stroke-dashoffset: 66;
    transition: all 200ms;
  }

  &[data-selected="true"] .option-button__indicator--radio {
    border-color: var(--global-button-primary-background-color);
    border-width: 6px;
  }

  &[data-selected="true"] .option-button__indicator--checkbox {
    border-color: var(--global-checkbox-selected-color);
    background: var(--global-checkbox-selected-color);
  }

  &[data-selected="true"] .option-button__indicator--checkbox svg {
    stroke-dashoffset: 44;
  }

  .option-button__content {
    display: flex;
    flex-direction: column;
    flex: 1;
    min-width: 0;
  }

  .option-button__label {
    line-height: var(--global-line-height-s);
  }

  .option-button__description {
    font-size: var(--global-font-size-xs);
    color: var(--global-text-color-500);
    line-height: var(--global-line-height-s);

    .theme--light & {
      color: var(--global-text-color-600);
    }
  }

  .option-button__text-entry {
    display: flex;
    align-items: center;
    gap: var(--global-dimension-size-75);
    flex: 1;
    min-width: 0;
  }

  .option-button__text-input {
    flex: 1;
    min-width: 0;
    background: transparent;
    border: none;
    border-bottom: var(--global-border-size-thin) solid
      var(--global-border-color-default);
    outline: none;
    color: var(--global-text-color-900);
    font-size: var(--global-font-size-s);
    font-family: inherit;
    padding: 2px 4px;
    transition: border-color 0.15s ease;

    &::placeholder {
      color: var(--global-text-color-500);
    }

    &:focus {
      border-color: var(--global-text-color-700);
    }
  }
`;function Yg(e){let t=(0,Y.c)(27),{selected:n,type:r,label:i,description:a,isFreeformEntry:o,textValue:s,onToggle:c,onTextChange:l}=e,u=(0,J.useRef)(null),d,f;t[0]!==o||t[1]!==n?(d=()=>{n&&o&&u.current&&u.current.focus()},f=[n,o],t[0]=o,t[1]=n,t[2]=d,t[3]=f):(d=t[2],f=t[3]),(0,J.useEffect)(d,f);let p=r===`single`?`option-button__indicator option-button__indicator--radio`:`option-button__indicator option-button__indicator--checkbox`,m;t[4]===Symbol.for(`react.memo_cache_sentinel`)?(m={scale:.98,transition:{type:`tween`,duration:.06}},t[4]=m):m=t[4];let h=r===`single`?`radio`:`checkbox`,g;t[5]===c?g=t[6]:(g=e=>{let t=e.target;t.tagName!==`INPUT`&&t.tagName!==`TEXTAREA`&&(e.key===`Enter`&&(e.metaKey||e.ctrlKey)||(e.key===`Enter`||e.key===` `)&&(e.preventDefault(),c()))},t[5]=c,t[6]=g);let _;t[7]===r?_=t[8]:(_=r===`multi`&&B(`svg`,{viewBox:`0 0 18 18`,"aria-hidden":`true`,children:B(`polyline`,{points:`1 9 7 14 15 4`})}),t[7]=r,t[8]=_);let v;t[9]!==p||t[10]!==_?(v=B(`span`,{className:p,children:_}),t[9]=p,t[10]=_,t[11]=v):v=t[11];let y;t[12]!==a||t[13]!==o||t[14]!==i||t[15]!==l||t[16]!==c||t[17]!==n||t[18]!==s?(y=o?B(`div`,{className:`option-button__text-entry`,onClick:Xg,children:B(`input`,{ref:u,type:`text`,className:`option-button__text-input`,value:s||``,placeholder:`Type your own answer…`,onMouseDown:()=>{n||c()},onChange:e=>{n||c(),l?.(e.target.value)},"aria-label":`Type your own answer`})}):V(`div`,{className:`option-button__content`,children:[B(`span`,{className:`option-button__label`,children:i}),a?B(`span`,{className:`option-button__description`,children:a}):null]}),t[12]=a,t[13]=o,t[14]=i,t[15]=l,t[16]=c,t[17]=n,t[18]=s,t[19]=y):y=t[19];let b;return t[20]!==c||t[21]!==n||t[22]!==h||t[23]!==g||t[24]!==v||t[25]!==y?(b=V(M.div,{css:Jg,"data-selected":n,onClick:c,whileTap:m,role:h,"aria-checked":n,tabIndex:0,onKeyDown:g,children:[v,y]}),t[20]=c,t[21]=n,t[22]=h,t[23]=g,t[24]=v,t[25]=y,t[26]=b):b=t[26],b}function Xg(e){return e.stopPropagation()}var Zg=`__freeform__`,Qg=.04,$g={enter:e=>({x:e>0?120:-120,opacity:0}),center:{x:0,opacity:1},exit:e=>({x:e>0?-120:120,opacity:0})},e_={type:`spring`,stiffness:400,damping:32,mass:.8},t_={type:`spring`,stiffness:700,damping:24,mass:.6};function n_({questions:e,onProgressStateChange:t,onSubmit:n,onCancel:r}){let[i,a]=(0,J.useState)({}),[o,s]=(0,J.useState)({}),[c,l]=(0,J.useState)(0),[u,d]=(0,J.useState)(0),f=(0,J.useRef)(!0),p=(0,J.useEffectEvent)(e=>{t?.(e)}),m=e.length,h=e[c];(0,J.useEffect)(()=>{let e=setTimeout(()=>{f.current=!1},500);return()=>clearTimeout(e)},[]),(0,J.useEffect)(()=>{p({answers:{},freeformTexts:{},currentIndex:0})},[]);let g=e=>{d(e>c?1:-1),l(e),t?.({answers:i,freeformTexts:o,currentIndex:e})},_=(e,t,n)=>{let r=i[e]||[],o;o=n===`single`?r.includes(t)?[]:[t]:r.includes(t)?r.filter(e=>e!==t):[...r,t],a(t=>({...t,[e]:o}))},v=(e,t)=>{a(n=>({...n,[e]:t}))},y=()=>{t?.({answers:i,freeformTexts:o,currentIndex:c}),n({answers:i,freeformTexts:o})},b=()=>{let t=i[e[c].id];((Array.isArray(t)?t.length>0:t)||e[c].allow_skip===!0)&&(c===m-1?y():g(c+1))},x=e=>{if(e.key!==`Enter`||e.nativeEvent.isComposing)return;let t=e.target;if(t.tagName===`TEXTAREA`)return;let n=t.tagName===`INPUT`&&t.type===`text`;(e.metaKey||e.ctrlKey||n)&&(e.preventDefault(),b())},S=e=>{e.key!==`Enter`||e.nativeEvent.isComposing||e.shiftKey||(e.preventDefault(),b())},C=f.current?Qg:0,w=C,T=2*C,E=e=>(3+e)*C,D=3*C,O=i[h.id],k=Array.isArray(O)?O.length>0:!!O,A=h.allow_skip===!0,j=k||A;return B(Xn,{autoFocus:!0,contain:!0,restoreFocus:!0,children:V(`div`,{css:qg,onKeyDown:x,children:[V(M.div,{className:`elicitation__header`,initial:{opacity:0,y:8},animate:{opacity:1,y:0},transition:{...t_,delay:w,opacity:{duration:.12,delay:w}},children:[V(`span`,{className:`elicitation__step-label`,children:[`Question `,c+1,` of `,m]}),B(`div`,{className:`elicitation__dots`,children:e.map((e,t)=>B(`button`,{className:`elicitation__dot ${t===c?`elicitation__dot--active`:`elicitation__dot--inactive`}`,onClick:()=>g(t),"aria-label":`Go to question ${t+1}`},t))})]}),B(`div`,{className:`elicitation__body`,children:B(Me,{custom:u,mode:`popLayout`,children:V(M.div,{custom:u,variants:$g,initial:!f.current&&`enter`,animate:`center`,exit:`exit`,transition:e_,className:`elicitation__question-content`,children:[B(M.div,{className:`elicitation__prompt`,initial:{opacity:0,y:-8},animate:{opacity:1,y:0},transition:{...t_,delay:T,opacity:{duration:.12,delay:T}},children:h.prompt}),h.type===`freeform`?B(M.div,{initial:{opacity:0,y:-8},animate:{opacity:1,y:0},transition:{...t_,delay:D,opacity:{duration:.12,delay:D}},children:B(`textarea`,{className:`elicitation__freeform`,value:i[h.id]||``,onChange:e=>v(h.id,e.target.value),onKeyDown:S,placeholder:`Type your response… (Enter to submit, Shift+Enter for newline)`,"aria-label":h.prompt})}):V(`div`,{className:`elicitation__options`,children:[h.options?.map((e,t)=>B(M.div,{initial:{opacity:0,y:-8},animate:{opacity:1,y:0},transition:{...t_,delay:E(t),opacity:{duration:.12,delay:E(t)}},children:B(Yg,{selected:(i[h.id]||[]).includes(e.id),type:h.type,label:e.label,description:e.description,onToggle:()=>_(h.id,e.id,h.type)})},e.id)),h.allow_freeform?B(M.div,{initial:{opacity:0,y:-8},animate:{opacity:1,y:0},transition:{...t_,delay:E(h.options?.length??0),opacity:{duration:.12,delay:E(h.options?.length??0)}},children:B(Yg,{selected:(i[h.id]||[]).includes(Zg),type:h.type,label:`Type your own answer`,isFreeformEntry:!0,textValue:o[h.id],onToggle:()=>_(h.id,Zg,h.type),onTextChange:e=>s(t=>({...t,[h.id]:e}))})},Zg):null]})]},h.id)})}),V(M.div,{className:`elicitation__nav`,initial:{opacity:0,y:8},animate:{opacity:1,y:0},transition:{...t_,delay:0,opacity:{duration:.12,delay:0}},children:[V(`div`,{className:`elicitation__nav-group`,children:[r&&B(H,{size:`S`,variant:`default`,onPress:r,children:`Cancel`}),B(H,{size:`S`,variant:`default`,isDisabled:c===0,onPress:()=>g(c-1),children:`Back`})]}),c===m-1?B(H,{size:`S`,variant:`primary`,isDisabled:!j,onPress:y,children:`Submit`}):B(H,{size:`S`,variant:k?`primary`:`default`,isDisabled:!j,onPress:()=>g(c+1),children:k?`Next`:`Skip`})]})]})})}var r_=(0,J.createContext)(null),i_=U`
  display: flex;
  flex-direction: column;
  gap: var(--global-dimension-size-50);
  font-size: var(--global-font-size-s);
  line-height: var(--global-line-height-s);

  &[data-from="user"] {
    align-items: flex-end;
  }

  &[data-from="assistant"] {
    align-items: flex-start;
    width: 100%;
  }
`,a_=U`
  word-wrap: break-word;
  overflow-wrap: break-word;
  min-width: 0;

  [data-from="user"] > & {
    background-color: var(--message-user-background-color);
    color: var(--message-user-text-color);
    border-radius: var(--message-user-border-radius);
    padding: var(--global-dimension-size-100) var(--global-dimension-size-200);
    max-width: 75%;
    white-space: pre-wrap;
  }

  [data-from="assistant"] > & {
    color: var(--global-text-color-900);
    width: 100%;
  }
`,o_=U`
  display: flex;
  align-items: center;
  gap: var(--global-dimension-size-50);
  margin-left: auto;
`,s_=U`
  display: flex;
  align-items: center;
  justify-content: center;
  border: var(--global-border-size-thin) solid transparent;
  border-radius: var(--global-rounding-small);
  background-color: transparent;
  color: var(--global-text-color-700);
  cursor: pointer;
  transition: all 0.2s ease;
  outline: none;
  padding: 0;
  flex: none;
  width: var(--global-button-height-s);
  min-width: var(--global-button-height-s);
  height: var(--global-button-height-s);

  .icon-wrap {
    font-size: var(--global-font-size-l);
    opacity: 0.7;
    transition: opacity 0.2s ease;
  }

  &[data-hovered] {
    background-color: var(--hover-background);
    .icon-wrap {
      opacity: 1;
    }
  }

  &[data-pressed] {
    background-color: var(--global-color-primary-100);
    color: var(--global-text-color-900);
  }

  &[data-focus-visible] {
    outline: var(--focus-ring-thickness) solid var(--focus-ring-color);
    outline-offset: var(--focus-ring-offset);
  }

  &[data-disabled] {
    opacity: var(--global-opacity-disabled);
    cursor: not-allowed;
  }
`,c_=U`
  display: flex;
  align-items: center;
  gap: var(--global-dimension-size-100);
  padding-top: var(--global-dimension-size-50);
  width: 100%;

  /* Reveal on hover: keep per-message action toolbars hidden by default
     to reduce the persistent visual noise of stacked toolbars, and reveal them
     when the message is hovered or contains keyboard focus. A message can opt
     out (always show) via [data-pin-toolbar="true"] on the Message root — used
     for the most recent assistant turn. */
  ${fu}
  transition: opacity 0.12s ease;

  [data-from]:hover > &,
  [data-from]:focus-within > &,
  [data-pin-toolbar="true"] > & {
    opacity: 1;
  }

  /* Keep the toolbar visible while one of its actions has an open menu/popover.
     The popover is portaled out of the message and takes focus with it, so
     :hover and :focus-within on the message both drop — but the trigger button
     keeps aria-expanded set, so the toolbar anchoring the open menu stays put
     instead of fading out from under it. */
  &:has([aria-expanded="true"]) {
    opacity: 1;
  }

  @media (prefers-reduced-motion: reduce) {
    transition: none;
  }
`;U`
  display: flex;
  align-items: center;
  gap: var(--global-dimension-size-50);
`,U`
  color: var(--global-text-color-500);
  font-size: var(--global-font-size-s);
  white-space: nowrap;
  user-select: none;
`;function l_(e){let t=(0,Y.c)(15),n,r,i,a;t[0]===e?(n=t[1],r=t[2],i=t[3],a=t[4]):({children:n,ref:i,from:r,...a}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a);let o;t[5]===r?o=t[6]:(o={from:r},t[5]=r,t[6]=o);let s;t[7]!==n||t[8]!==r||t[9]!==i||t[10]!==a?(s=B(`div`,{ref:i,css:i_,"data-from":r,...a,children:n}),t[7]=n,t[8]=r,t[9]=i,t[10]=a,t[11]=s):s=t[11];let c;return t[12]!==o||t[13]!==s?(c=B(r_.Provider,{value:o,children:s}),t[12]=o,t[13]=s,t[14]=c):c=t[14],c}function u_(e){let t=(0,Y.c)(8),n,r,i;t[0]===e?(n=t[1],r=t[2],i=t[3]):({children:n,ref:r,...i}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i);let a;return t[4]!==n||t[5]!==r||t[6]!==i?(a=B(`div`,{ref:r,css:a_,...i,children:n}),t[4]=n,t[5]=r,t[6]=i,t[7]=a):a=t[7],a}function d_(e,t){for(let n of e.tokenColors)if((Array.isArray(n.scope)?n.scope:n.scope?[n.scope]:[]).includes(t))return n.settings.foreground}function f_(e){let t=e.colors,n=t=>d_(e,t),r=[{tag:[P.standard(P.tagName),P.tagName],color:n(`entity.name.tag`)},{tag:[P.comment],color:n(`comment`)},{tag:[P.bracket,P.punctuation,P.separator,P.derefOperator],color:n(`punctuation`)},{tag:[P.className,P.typeName,P.namespace,P.definition(P.typeName)],color:n(`entity.name.type`)},{tag:[P.propertyName,P.attributeName],color:n(`entity.other.attribute-name`)},{tag:[P.function(P.variableName),P.function(P.propertyName),P.macroName],color:n(`entity.name.function`)},{tag:[P.variableName,P.definition(P.variableName)],color:n(`variable`)},{tag:[P.number,P.bool,P.atom],color:n(`constant.numeric`)},{tag:[P.keyword,P.modifier,P.operatorKeyword,P.controlKeyword],color:n(`keyword`)},{tag:[P.string,P.special(P.string),P.docString],color:n(`string`)},{tag:[P.operator],color:n(`keyword.operator`)},{tag:[P.constant(P.variableName),P.literal],color:n(`constant`)},{tag:[P.regexp],color:n(`string.regexp`)},{tag:[P.escape],color:n(`constant.character.escape`)},{tag:[P.heading,P.strong],color:n(`markup.heading`),fontWeight:`bold`},{tag:[P.emphasis],fontStyle:`italic`},{tag:[P.link,P.url],color:n(`markup.underline.link.markdown`),textDecoration:`underline`},{tag:[P.strikethrough],textDecoration:`line-through`},{tag:[P.invalid],color:t[`editor.foreground`]}];return Je({theme:e.type,settings:{background:t[`editor.background`],foreground:t[`editor.foreground`],caret:t[`editorCursor.foreground`],selection:t[`editor.selectionBackground`],selectionMatch:t[`editor.selectionBackground`],lineHighlight:t[`editor.lineHighlightBackground`],gutterBackground:t[`editor.background`],gutterForeground:t[`editorLineNumber.foreground`],gutterActiveForeground:t[`editorLineNumber.activeForeground`]},styles:r.filter(e=>e.color!=null||e.fontWeight!=null||e.fontStyle!=null||e.textDecoration!=null)})}var p_=f_(ke),m_=f_(pe);function h_(e){let t=(0,Y.c)(13),n,r;t[0]===e?(n=t[1],r=t[2]):({basicSetup:n,...r}=e,t[0]=e,t[1]=n,t[2]=r);let{theme:i}=Mr(),a=i===`light`?p_:m_,o;bb0:{let e;t[3]===Symbol.for(`react.memo_cache_sentinel`)?(e={lineNumbers:!0,foldGutter:!0,bracketMatching:!0,syntaxHighlighting:!0,highlightActiveLine:!1,highlightActiveLineGutter:!1},t[3]=e):e=t[3];let r=e;if(n){let e;t[4]===n?e=t[5]:(e={...r,...n},t[4]=n,t[5]=e),o=e;break bb0}o=r}let s=o,c=e.value,l;t[6]===Symbol.for(`react.memo_cache_sentinel`)?(l=Ze(),t[6]=l):l=t[6];let u;t[7]===Symbol.for(`react.memo_cache_sentinel`)?(u=[l,Ge.lineWrapping,Ye(Xe())],t[7]=u):u=t[7];let d;return t[8]!==s||t[9]!==a||t[10]!==e.value||t[11]!==r?(d=B(Ke,{value:c,extensions:u,editable:!1,theme:a,...r,basicSetup:s}),t[8]=s,t[9]=a,t[10]=e.value,t[11]=r,t[12]=d):d=t[12],d}function g_(e){let t=(0,Y.c)(6),n;try{let r;if(t[0]!==e){let n=JSON.parse(e);r=JSON.stringify(n,null,2),t[0]=e,t[1]=r}else r=t[1];let i;t[2]===r?i=t[3]:(i={text:r,textType:`json`},t[2]=r,t[3]=i),n=i}catch{let r;t[4]===e?r=t[5]:(r={text:e,textType:`string`},t[4]=e,t[5]=r),n=r}return n}function __({children:e,preCSS:t}){let{text:n,textType:r}=g_(e);return r===`string`?B(`pre`,{css:U`
          white-space: pre-wrap;
          text-wrap: wrap;
          overflow-wrap: anywhere;
          font-size: var(--global-font-size-s);
          margin: 0;
          ${t}
        `,children:n}):r===`json`?B(h_,{value:n}):fr(r)}var v_=(0,J.createContext)(null);function y_(){let e=(0,Y.c)(1),t=(0,J.useContext)(v_);if(t===null){console.warn(`useMarkdownMode must be used within a MarkdownDisplayProvider`);let n;e[0]===Symbol.for(`react.memo_cache_sentinel`)?(n={mode:`text`,setMode:b_},e[0]=n):n=e[0],t=n}return t}function b_(){}function x_(e){let t=(0,Y.c)(8),n=hi(C_),r=hi(S_),i;t[0]===r?i=t[1]:(i=e=>{(0,J.startTransition)(()=>{r(e)})},t[0]=r,t[1]=i);let a=i,o;t[2]!==n||t[3]!==a?(o={mode:n,setMode:a},t[2]=n,t[3]=a,t[4]=o):o=t[4];let s;return t[5]!==e.children||t[6]!==o?(s=B(v_.Provider,{value:o,children:e.children}),t[5]=e.children,t[6]=o,t[7]=s):s=t[7],s}function S_(e){return e.setMarkdownDisplayMode}function C_(e){return e.markdownDisplayMode}var w_=U`
  font-size: var(--global-font-size-s);
  line-height: var(--global-line-height-s);
  color: var(--global-text-color-900);
  overflow-wrap: anywhere;

  /* Streamdown's root div uses Tailwind "space-y-4" for vertical rhythm.
   * Since Phoenix doesn't load Tailwind, we replicate the spacing with
   * flex + gap on the root container. */
  & > div {
    display: flex;
    flex-direction: column;
    gap: var(--global-dimension-size-200);
  }

  /* -------------------------------------------------------------------
   * Shiki syntax-highlighting token colors
   *
   * Streamdown renders each syntax token as a <span> inside the code
   * body with inline style custom properties:
   *   --sdm-c       light-theme foreground
   *   --sdm-tbg     light-theme token background (highlighted ranges)
   *   --shiki-dark  dark-theme foreground
   *
   * It expects Tailwind utility classes (text-[var(--sdm-c,inherit)],
   * dark:text-[var(--shiki-dark,…)], etc.) to read those properties.
   * Phoenix doesn't use Tailwind, so we provide the equivalent rules,
   * scoped to the code block body to avoid any bleed.
   * ------------------------------------------------------------------- */

  [data-streamdown="code-block-body"] span {
    color: var(--sdm-c, inherit);
  }

  .theme--dark & [data-streamdown="code-block-body"] span {
    color: var(--shiki-dark, var(--sdm-c, inherit));
  }

  /* -------------------------------------------------------------------
   * Code block overrides
   *
   * Streamdown's CodeBlock renders with Tailwind utility classes. We
   * selectively override layout/color properties so the code blocks
   * integrate with our design-token-based system while preserving
   * Tailwind's whitespace and line-number handling internally.
   * ------------------------------------------------------------------- */

  [data-streamdown="code-block"] {
    margin-top: var(--global-dimension-size-100);
    padding: 0;
    gap: 0;
    border: 1px solid var(--global-code-block-border-color);
    border-radius: var(--global-rounding-medium);
    background: var(--global-code-block-background-color);
    position: relative;
    overflow: hidden;
  }

  [data-streamdown="code-block-header"] {
    min-height: var(--global-dimension-size-500);
    padding: 0 var(--global-dimension-size-150);
    border-bottom: 1px solid var(--global-code-block-border-color);
    background: var(--global-code-block-header-background-color);
    color: var(--global-code-block-header-text-color);
    font-family: var(--global-font-family-mono);
    font-size: var(--global-font-size-xs);
    line-height: var(--global-line-height-xs);
    letter-spacing: 0.03em;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }

  /* Actions wrapper — reposition into the header row.
   * Streamdown renders: <div class="pointer-events-none sticky …">
   *   <div data-streamdown="code-block-actions">…</div>
   * </div>
   * We collapse the sticky wrapper's negative margin overlap and
   * absolutely position it inside the header band instead. */
  [data-streamdown="code-block"]
    > div:has([data-streamdown="code-block-actions"]) {
    position: absolute;
    top: var(--global-dimension-size-50);
    right: var(--global-dimension-size-100);
    height: var(--global-code-block-actions-wrapper-height);
    display: flex;
    align-items: center;
    margin: 0;
    z-index: 1;
    pointer-events: auto;
  }

  [data-streamdown="code-block-actions"] {
    display: flex;
    align-items: center;
    gap: var(--global-dimension-size-25);
    padding: 0;
    border: 0;
    background: transparent;
    box-shadow: none;
    backdrop-filter: none;
  }

  [data-streamdown="code-block-actions"] button {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: var(--global-code-block-actions-button-size);
    height: var(--global-code-block-actions-button-size);
    padding: 0;
    border: 0;
    border-radius: var(--global-rounding-small);
    background: transparent;
    color: var(--global-text-color-500);
    cursor: pointer;
    transition:
      background-color 0.15s ease,
      color 0.15s ease;

    &:hover {
      background: var(--hover-background);
      color: var(--global-text-color-900);
    }

    /* Size icons to match IconButton size="S" and apply fill so
       Phoenix Icons (which rely on the Icon wrapper) inherit color. */
    & svg {
      width: var(--global-code-block-actions-icon-size);
      height: var(--global-code-block-actions-icon-size);
      fill: currentColor;
    }
  }

  [data-streamdown="code-block-body"] {
    overflow-x: auto;
    border: 0;
    border-radius: 0;
    padding: 0;
    background: transparent;
  }

  [data-streamdown="code-block-body"] pre {
    margin: 0;
    padding: var(--global-dimension-size-150);
    background: transparent;
    font-family: var(--global-font-family-mono);
    font-size: var(--global-font-size-sm);
    line-height: var(--global-line-height-s);
    white-space: pre;
    overflow-x: auto;
  }

  [data-streamdown="code-block-body"] code {
    font-family: var(--global-font-family-mono);
    white-space: pre;
  }

  /* Each highlighted line is a <span class="block …">. Tailwind's "block"
   * utility (display:block) has no CSS backing in Phoenix, so lines collapse
   * onto a single row. We restore the block display for direct-child spans
   * of <code> to get one line per span. */
  [data-streamdown="code-block-body"] code > span {
    display: block;
  }
`,T_={code:Rn},E_={CopyIcon:()=>B(Et,{}),CheckIcon:()=>B(yn,{}),DownloadIcon:()=>B(dt,{})};function D_({children:e,mode:t,renderMode:n=`static`,margin:r=`default`}){let i=r===`none`?U`
          margin: 0;
        `:U`
          margin: var(--global-dimension-size-200);
        `;return t===`markdown`?B(`div`,{css:[w_,i],children:B(jn,{components:Gn,controls:{code:{copy:!0,download:!0},table:!1},icons:E_,mode:n,plugins:T_,children:e})}):B(__,{preCSS:i,children:e})}function O_({children:e,renderMode:t,margin:n=`default`}){let{mode:r}=y_();return B(D_,{mode:r,renderMode:t,margin:n,children:e})}function k_(e){return typeof e==`string`?{content:e,position:`top`}:{position:`top`,...e}}function A_(e){let t=(0,Y.c)(22),n,r,i,a,o,s;t[0]===e?(n=t[1],r=t[2],i=t[3],a=t[4],o=t[5],s=t[6]):({children:n,ref:a,label:i,tooltip:s,className:r,...o}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a,t[5]=o,t[6]=s);let c;t[7]!==n||t[8]!==r||t[9]!==i||t[10]!==a||t[11]!==o?(c=B(xt,{ref:a,css:s_,className:r,"aria-label":i,...o,children:n}),t[7]=n,t[8]=r,t[9]=i,t[10]=a,t[11]=o,t[12]=c):c=t[12];let l=c;if(!s)return l;let u;t[13]===s?u=t[14]:(u=k_(s),t[13]=s,t[14]=u);let{content:d,position:f}=u,p;t[15]===Symbol.for(`react.memo_cache_sentinel`)?(p=B(aa,{}),t[15]=p):p=t[15];let m;t[16]!==d||t[17]!==f?(m=V(ia,{placement:f,children:[p,d]}),t[16]=d,t[17]=f,t[18]=m):m=t[18];let h;return t[19]!==l||t[20]!==m?(h=V(Se,{delay:500,closeDelay:0,children:[l,m]}),t[19]=l,t[20]=m,t[21]=h):h=t[21],h}var j_=2e3;function M_(e){let t=(0,Y.c)(11),{text:n}=e,[r,i]=(0,J.useState)(!1);if(n.trim().length===0)return null;let a;t[0]===n?a=t[1]:(a=()=>{ze(n),i(!0),setTimeout(()=>i(!1),j_)},t[0]=n,t[1]=a);let o=a,s=r?`Copied`:`Copy message`,c;t[2]===r?c=t[3]:(c=B(r?yn:Et,{}),t[2]=r,t[3]=c);let l=r?`success`:`inherit`,u;t[4]!==c||t[5]!==l?(u=B(z,{svg:c,color:l}),t[4]=c,t[5]=l,t[6]=u):u=t[6];let d;return t[7]!==o||t[8]!==s||t[9]!==u?(d=B(A_,{label:`Copy`,tooltip:s,onPress:o,children:u}),t[7]=o,t[8]=s,t[9]=u,t[10]=d):d=t[10],d}function N_(e){let t=(0,Y.c)(8),n,r,i;t[0]===e?(n=t[1],r=t[2],i=t[3]):({children:n,ref:r,...i}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i);let a;return t[4]!==n||t[5]!==r||t[6]!==i?(a=B(`div`,{ref:r,css:o_,role:`toolbar`,...i,children:n}),t[4]=n,t[5]=r,t[6]=i,t[7]=a):a=t[7],a}function P_(e){let t=(0,Y.c)(8),n,r,i;t[0]===e?(n=t[1],r=t[2],i=t[3]):({children:n,ref:r,...i}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i);let a;return t[4]!==n||t[5]!==r||t[6]!==i?(a=B(`div`,{ref:r,css:c_,...i,children:n}),t[4]=n,t[5]=r,t[6]=i,t[7]=a):a=t[7],a}(0,J.createContext)(null);var F_=(0,J.createContext)(null);function I_(){let e=(0,J.useContext)(F_);if(!e)throw Error(`usePromptInputContext must be used within a <PromptInput> component`);return e}var L_=U`
  display: flex;
  flex-direction: column;
  background-color: var(--prompt-input-background-color);
  border: var(--global-border-size-thin) solid var(--prompt-input-border-color);
  border-radius: var(--prompt-input-border-radius);
  transition: border-color 0.2s ease-in-out;

  &[data-input-mode="prompt"]:focus-within {
    border-color: var(--prompt-input-border-color-focus);
  }

  &[data-input-mode="prompt"]:has(textarea:focus-visible) {
    outline: var(--focus-ring-thickness) solid var(--focus-ring-color);
    outline-offset: calc(-1 * var(--focus-ring-thickness));
  }

  /* Elicitation surfaces host tall content (consent gate, question carousel,
     rewind confirmation) inside a height-constrained input region; shrink
     with the region and scroll the content instead of overflowing the panel. */
  &[data-input-mode="elicitation"] {
    min-height: 0;
    overflow-y: auto;
  }
`,R_=U`
  flex: 1 1 auto;
  padding: var(--global-dimension-size-200);
  padding-bottom: var(--global-dimension-size-100);
`,z_=U`
  display: block;
  width: 100%;
  min-height: calc(var(--global-line-height-s) * 3);
  border: none;
  outline: none;
  background: transparent;
  resize: none;
  padding: 0;
  margin: 0;
  font-family: inherit;
  font-size: var(--global-font-size-s);
  line-height: var(--global-line-height-s);
  color: var(--prompt-input-textarea-color);
  overflow-y: auto;

  &::placeholder {
    color: var(--prompt-input-textarea-placeholder-color);
    font-style: normal;
  }

  &:disabled {
    opacity: var(--global-opacity-disabled);
    cursor: not-allowed;
  }
`,B_=U`
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--global-dimension-size-100) var(--global-dimension-size-150);
  gap: var(--global-dimension-size-100);
`,V_=U`
  display: flex;
  align-items: center;
  gap: var(--global-dimension-size-50);
`,H_=U`
  display: flex;
  align-items: center;
  gap: var(--global-dimension-size-50);
`,U_=U`
  --prompt-input-submit-size: var(--global-button-height-s);

  display: flex;
  align-items: center;
  justify-content: center;
  width: var(--prompt-input-submit-size);
  height: var(--prompt-input-submit-size);
  border: none;
  border-radius: var(--global-rounding-medium);
  background-color: var(--prompt-input-submit-background-color);
  color: var(--prompt-input-submit-foreground-color);
  cursor: pointer;
  padding: 0;
  transition: background-color 0.2s ease-in-out;
  outline: none;
  flex: none;

  .icon-wrap {
    font-size: var(--global-font-size-l);
  }

  &[data-hovered] {
    background-color: var(--prompt-input-submit-background-color-hover);
  }

  &[data-focus-visible] {
    outline: var(--focus-ring-thickness) solid var(--focus-ring-color);
    outline-offset: var(--focus-ring-offset);
  }

  &[data-disabled] {
    background-color: var(--prompt-input-submit-background-color-disabled);
    color: var(--prompt-input-submit-foreground-color-disabled);
    cursor: not-allowed;
  }
`;U`
  display: flex;
  align-items: center;
  justify-content: center;
  border: var(--global-border-size-thin) solid transparent;
  border-radius: var(--global-rounding-small);
  background-color: transparent;
  color: var(--global-text-color-700);
  cursor: pointer;
  transition: all 0.2s ease;
  outline: none;
  padding: 0;
  flex: none;
  width: var(--global-button-height-s);
  min-width: var(--global-button-height-s);
  height: var(--global-button-height-s);

  .icon-wrap {
    font-size: var(--global-font-size-l);
    opacity: 0.7;
    transition: opacity 0.2s ease;
  }

  &[data-hovered] {
    background-color: var(--prompt-input-tool-button-background-color-hover);
    .icon-wrap {
      opacity: 1;
    }
  }

  &[data-pressed] {
    background-color: var(--global-color-primary-100);
    color: var(--global-text-color-900);
  }

  &[data-focus-visible] {
    outline: var(--focus-ring-thickness) solid var(--focus-ring-color);
    outline-offset: var(--focus-ring-offset);
  }

  &[data-disabled] {
    opacity: var(--global-opacity-disabled);
    cursor: not-allowed;
  }
`;function W_({children:e,ref:t,onSubmit:n,status:r=`ready`,isDisabled:i=!1,isSubmitDisabled:a=!1,mode:o=`prompt`,value:s,onValueChange:c,...l}){let[u,d]=(0,J.useState)(``),f=s!==void 0,p=f?s:u,m=e=>{f||d(e),c?.(e)},h=(0,J.useRef)(p);h.current=p;let g={status:r,isDisabled:i,onSubmit:()=>{if(a||r===`submitted`||r===`streaming`)return;let e=h.current.trim();e&&(n?.(e),m(``))},value:p,setValue:m};return B(F_.Provider,{value:g,children:B(`div`,{ref:t,css:L_,"data-status":r,"data-input-mode":o,...l,children:e})})}function G_(e){let t=(0,Y.c)(8),n,r,i;t[0]===e?(n=t[1],r=t[2],i=t[3]):({children:n,ref:r,...i}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i);let a;return t[4]!==n||t[5]!==r||t[6]!==i?(a=B(`div`,{ref:r,css:R_,...i,children:n}),t[4]=n,t[5]=r,t[6]=i,t[7]=a):a=t[7],a}function K_(e){let t=(0,Y.c)(8),n,r,i;t[0]===e?(n=t[1],r=t[2],i=t[3]):({children:n,ref:r,...i}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i);let a;return t[4]!==n||t[5]!==r||t[6]!==i?(a=B(`div`,{ref:r,css:B_,...i,children:n}),t[4]=n,t[5]=r,t[6]=i,t[7]=a):a=t[7],a}function q_(e){let t=(0,Y.c)(8),n,r,i;t[0]===e?(n=t[1],r=t[2],i=t[3]):({children:n,ref:r,...i}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i);let a;return t[4]!==n||t[5]!==r||t[6]!==i?(a=B(`div`,{ref:r,css:V_,role:`toolbar`,...i,children:n}),t[4]=n,t[5]=r,t[6]=i,t[7]=a):a=t[7],a}function J_(e){let t=(0,Y.c)(8),n,r,i;t[0]===e?(n=t[1],r=t[2],i=t[3]):({children:n,ref:r,...i}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i);let a;return t[4]!==n||t[5]!==r||t[6]!==i?(a=B(`div`,{ref:r,css:H_,...i,children:n}),t[4]=n,t[5]=r,t[6]=i,t[7]=a):a=t[7],a}function Y_({ref:e,placeholder:t=`Send a message...`,value:n,onChange:r,maxRows:i,"aria-label":a=`Message input`,className:o}){let s=I_(),c=(0,J.useRef)(null),l=n===void 0?s.value:n,u=r===void 0?s.setValue:r,d=t=>{c.current=t,typeof e==`function`?e(t):e&&`current`in e&&(e.current=t)};(0,J.useLayoutEffect)(()=>{let e=c.current;if(!e)return;let t=()=>{e.style.height=`auto`;let t=e.scrollHeight;if(i){let n=parseInt(getComputedStyle(e).lineHeight||`20`,10)*i;t=Math.min(t,n)}e.style.height=`${t}px`};t();let n=requestAnimationFrame(t);return()=>{cancelAnimationFrame(n)}},[l,i]);let{onSubmit:f}=s;return B(`textarea`,{ref:d,css:z_,className:o,value:l,onChange:e=>{u(e.target.value)},onKeyDown:e=>{e.key===`Enter`&&!e.shiftKey&&(e.preventDefault(),f())},placeholder:t,disabled:s.isDisabled,"aria-label":a,rows:1})}function X_(e){let t=(0,Y.c)(15),{ref:n,onPress:r,isDisabled:i,"aria-label":a,className:o}=e,s=I_(),c=s.status===`submitted`||s.status===`streaming`,l;t[0]===s.value?l=t[1]:(l=s.value.trim(),t[0]=s.value,t[1]=l);let u=l===``,d=i??(s.status===`ready`&&u),f=!c,p=a??(f?`Send message`:`Stop generation`),m;t[2]!==s||t[3]!==c||t[4]!==r?(m=()=>{if(c){r?.();return}s.onSubmit()},t[2]=s,t[3]=c,t[4]=r,t[5]=m):m=t[5];let h=m,g=d||s.isDisabled,_;t[6]===f?_=t[7]:(_=B(z,{svg:B(f?et:Bn,{})}),t[6]=f,t[7]=_);let v;return t[8]!==o||t[9]!==p||t[10]!==h||t[11]!==n||t[12]!==g||t[13]!==_?(v=B(xt,{ref:n,css:U_,className:o,isDisabled:g,onPress:h,"aria-label":p,children:_}),t[8]=o,t[9]=p,t[10]=h,t[11]=n,t[12]=g,t[13]=_,t[14]=v):v=t[14],v}U`
  display: flex;
  align-items: center;
  gap: var(--global-dimension-size-75);
`;var Z_=U`
  ${Tn};
  background-clip: text;
  -webkit-background-clip: text;
  color: transparent;
  background-repeat: no-repeat, padding-box;
  background-size:
    250% 100%,
    auto;
  background-image:
    linear-gradient(
      90deg,
      transparent calc(50% - var(--shimmer-spread)),
      var(--global-background-color-default),
      transparent calc(50% + var(--shimmer-spread))
    ),
    linear-gradient(var(--shimmer-color), var(--shimmer-color));

  @media (prefers-reduced-motion: reduce) {
    background: none;
    -webkit-background-clip: initial;
    background-clip: initial;
    color: var(--shimmer-color);
  }
`,Q_=new Map,$_=e=>{let t=Q_.get(e);if(t)return t;let n=M.create(e);return Q_.set(e,n),n};function ev({ref:e,children:t,elementType:n=`p`,size:r=`S`,weight:i=`normal`,color:a=`text-700`,fontStyle:o=`normal`,duration:s=2,spread:c=2,className:l,style:u,...d}){let f=we(),p=$_(n),m=(t?.length??0)*c,h=f?{}:{initial:{backgroundPosition:`100% center`},animate:{backgroundPosition:`0% center`},transition:{duration:s,ease:`linear`,repeat:1/0}};return B(p,{ref:e,className:F(`shimmer`,l),"data-size":r,"data-weight":i,css:Z_,style:{"--shimmer-spread":`${m}px`,"--shimmer-color":Nt(a),fontStyle:o,...u},...h,...d,children:t})}ev.displayName=`Shimmer`;var $=e=>`var(${e})`,tv=Object.freeze({blue100:$(`--global-color-blue-200`),blue200:$(`--global-color-blue-300`),blue300:$(`--global-color-blue-400`),blue400:$(`--global-color-blue-500`),blue500:$(`--global-color-blue-600`),blue600:$(`--global-color-blue-700`),blue700:$(`--global-color-blue-800`),blue800:$(`--global-color-blue-900`),blue900:$(`--global-color-blue-1000`),orange100:$(`--global-color-orange-500`),orange200:$(`--global-color-orange-600`),orange300:$(`--global-color-orange-700`),orange400:$(`--global-color-orange-800`),orange500:$(`--global-color-orange-900`),purple100:$(`--global-color-purple-100`),purple200:$(`--global-color-purple-200`),purple300:$(`--global-color-purple-300`),purple400:$(`--global-color-purple-400`),purple500:$(`--global-color-purple-500`),magenta100:$(`--global-color-magenta-200`),magenta200:$(`--global-color-magenta-300`),magenta300:$(`--global-color-magenta-400`),magenta400:$(`--global-color-magenta-500`),magenta500:$(`--global-color-magenta-600`),red100:$(`--global-color-red-200`),red200:$(`--global-color-red-300`),red300:$(`--global-color-red-400`),red400:$(`--global-color-red-500`),red500:$(`--global-color-red-600`),gray100:$(`--global-color-gray-100`),gray200:$(`--global-color-gray-200`),gray300:$(`--global-color-gray-300`),gray400:$(`--global-color-gray-400`),gray500:$(`--global-color-gray-500`),gray600:$(`--global-color-gray-600`),gray700:$(`--global-color-gray-700`),default:$(`--global-text-color-900`)});Object.keys(tv);var nv=()=>tv,rv=(e,t)=>{let n=[[`blue`,5],[`orange`,5],[`purple`,5],[`pink`,5],[`gray`,5]],r=n.length,i=e%r,a=Math.floor(e/r),[o,s]=n[i];return t[`${o}${500-a%s*100}`]||t.default},iv={danger:`var(--global-color-red-700)`,success:`var(--global-color-celery-700)`,warning:`var(--global-color-warning)`,info:`var(--global-color-blue-700)`};Object.keys(iv);var av=()=>iv,ov={category1:`var(--global-color-blue-700)`,category2:`var(--global-color-purple-900)`,category3:`var(--global-color-magenta-600)`,category4:`var(--global-color-indigo-600)`,category5:`var(--global-color-blue-900)`,category6:`var(--global-color-indigo-1100)`,category7:`var(--global-color-orange-600)`,category8:`var(--global-color-celery-400)`,category9:`var(--global-color-seafoam-600)`,category10:`var(--global-color-green-1000)`,category11:`var(--global-color-yellow-400)`,category12:`var(--global-color-red-1100)`},sv={category1:`var(--global-color-blue-700)`,category2:`var(--global-color-purple-800)`,category3:`var(--global-color-magenta-800)`,category4:`var(--global-color-indigo-600)`,category5:`var(--global-color-blue-900)`,category6:`var(--global-color-indigo-1100)`,category7:`var(--global-color-orange-600)`,category8:`var(--global-color-celery-400)`,category9:`var(--global-color-seafoam-600)`,category10:`var(--global-color-green-1000)`,category11:`var(--global-color-yellow-400)`,category12:`var(--global-color-red-1100)`},cv=()=>{let{theme:e}=Mr();return e===`dark`?sv:ov},lv=Object.keys(ov),uv=({index:e,colors:t})=>t[lv[e%lv.length]],dv={gray1:`var(--global-color-gray-800)`,gray2:`var(--global-color-gray-600)`,gray3:`var(--global-color-gray-500)`,gray4:`var(--global-color-gray-400)`},fv={gray1:`var(--global-color-gray-800)`,gray2:`var(--global-color-gray-600)`,gray3:`var(--global-color-gray-500)`,gray4:`var(--global-color-gray-400)`},pv=()=>{let{theme:e}=Mr();return e===`dark`?fv:dv},mv=Object.keys(dv),hv=U`
  width: 100%;
  display: flex;
  flex-direction: row;
  overflow: hidden;
  border-radius: var(--global-rounding-medium);
  gap: 2px;
`,gv=U`
  height: 100%;
  flex-shrink: 0;
  flex-grow: 0;
`,_v=({height:e=6,minimumSegmentPercentage:t=0,segments:n,totalValue:r})=>{let i=r??n.reduce((e,t)=>e+t.value,0),a=t>0?n.filter(e=>e.value>0):n;return a.some(e=>e.value>0)?B(`div`,{style:{height:`${e}px`},css:hv,children:a.map(e=>{let n=i>0?e.value/i*100:0,r=e.color,a=e.value>0&&t>0?`${t}%`:void 0;return B(`div`,{css:gv,style:{width:`${n}%`,minWidth:a,flexShrink:a==null?0:1,backgroundColor:r}},e.name)})}):null};function vv(e){return Math.abs(e)<1e6?I(`,`)(e):I(`0.2s`)(e).replace(`G`,`B`).replace(`k`,`K`)}function yv(e){return Math.abs(e)<1e3?I(`,`)(e):I(`0.2s`)(e).replace(`G`,`B`).replace(`k`,`K`)}function bv(e){let t=Math.abs(e);if(t===0)return`0.00`;if(t<.01)return I(`.2e`)(e);if(t<1){let t=Fv(e,2);return I(`0.2f`)(t)}return t<1e3?I(`0.2f`)(e):I(`0.2s`)(e)}function xv(e){let t=Math.abs(e);return t===0?`0.00`:t<.01?I(`.2e`)(e):t<1e3?I(`0.2f`)(e):I(`0.2s`)(e).replace(`G`,`B`).replace(`k`,`K`)}function Sv(e){return I(`.2f`)(e)+`%`}function Cv(e){return Number.isInteger(e)?vv(e):bv(e)}function wv(e){return e===0?`$0`:e<.01?`<$0.01`:e<100?`$${I(`0.2f`)(e)}`:e<1e4?`$${I(`,`)(e)}`:`$${I(`0.2s`)(e).replace(`G`,`B`).replace(`k`,`K`)}`}function Tv(e){let t=Math.floor(e/ca),n=Math.floor(e%ca/sa),r=Math.floor(e%sa/oa),i=Math.floor(e%oa);if(t>0)return`${t}h${n?` ${n}m`:``}${r?` ${r}s`:``}`;if(n>0)return`${n}m${r?` ${r}s`:``}`;if(r>0){let e=Math.floor(i/100);return`${r}${e>0?`.${e.toFixed(0)}`:``}s`}return`${i.toFixed(0)}ms`}function Ev(e){return t=>typeof t==`number`?e(t):`--`}var Dv=Ev(vv),Ov=Ev(yv),kv=Ev(xv),Av=Ev(bv),jv=Ev(Cv),Mv=Ev(Sv),Nv=Ev(wv),Pv=Ev(Tv);function Fv(e,t){let n=e.toString().split(`.`);return n.length<2?e:Number(n[0]+`.`+n[1].substring(0,t))}var Iv=U`
  display: flex;
  flex-direction: row;
  gap: var(--global-dimension-size-50);
  align-items: center;

  &[data-size="S"] {
    font-size: var(--global-font-size-s);
  }
  &[data-size="M"] {
    font-size: var(--global-font-size-m);
  }
  &[role="button"] {
    ${du}
  }
  .icon-wrap {
    font-size: 1em;
  }
`;function Lv({ref:e,...t}){let{children:n,color:r=`text-900`,size:i=`M`,...a}=t,o=Nt(r),s=typeof n==`number`?Cv(n):`--`;return V(`div`,{className:`token-count-item`,"data-size":i,css:Iv,ref:e,...a,children:[B(z,{svg:B(qn,{}),css:U`
          color: ${o};
        `}),B(L,{size:t.size,color:r,fontFamily:`mono`,children:s})]})}var Rv=1e-9,zv={input:0,output:0,cache_read:1,cache_write:2,reasoning:3,audio:4},Bv={input:`category1`,output:`category2`,cache_read:`category9`,cache_write:`category7`,reasoning:`category4`,audio:`category3`},Vv=[`category5`,`category6`,`category8`,`category10`,`category11`,`category12`];function Hv(e){let t=e.split(`_`).join(` `);return t.charAt(0).toUpperCase()+t.slice(1)}function Uv(e){return e?`input`:`output`}function Wv(e,t){let n=zv[e]??100,r=zv[t]??100;return n===r?e.localeCompare(t):n-r}function Gv({colors:e,index:t=0,tokenType:n}){let r=Bv[n];return r?e[r]:e[Vv[t%Vv.length]]}function Kv(e){return Vv.map(t=>e[t])}var qv=U`
  display: contents;

  .chat-token-usage__summary {
    display: flex;
    justify-content: flex-end;
    grid-column: 2;
    grid-row: 1;
  }

  .chat-token-usage__trigger {
    display: flex;
    align-items: center;
    gap: var(--global-dimension-size-25);
    border-radius: var(--global-rounding-small);
    color: var(--global-text-color-300);
    cursor: pointer;
    outline: none;
    transition: color 150ms ease-in-out;

    .token-count-item .icon-wrap,
    .token-count-item .text,
    .disclosure-arrow {
      color: currentColor;
    }

    &:hover,
    &:focus-visible,
    &[aria-expanded="true"] {
      color: var(--global-text-color-700);
    }

    &:focus-visible {
      outline: var(--global-border-size-thick) solid var(--focus-ring-color);
      outline-offset: var(--focus-ring-offset);
    }
  }

  .chat-token-usage__details {
    grid-column: 1 / -1;
    grid-row: 2;
    min-width: 0;
  }

  @media (prefers-reduced-motion: reduce) {
    .chat-token-usage__trigger {
      transition: none;
    }
  }
`,Jv=U`
  display: flex;
  flex-direction: column;
  gap: var(--global-dimension-size-100);
  padding-top: var(--global-dimension-size-100);

  .chat-token-usage-details__legend {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: var(--global-dimension-size-100);
  }

  .chat-token-usage-details__segments {
    display: flex;
    align-items: center;
    justify-content: flex-end;
    flex-wrap: wrap;
    gap: var(--global-dimension-size-200);
    list-style: none;
    margin: 0;
    padding: 0;
  }

  .chat-token-usage-details__segment {
    display: flex;
    align-items: center;
    gap: var(--global-dimension-size-50);
  }
`,Yv=U`
  & {
    all: unset;
    display: flex;
    align-items: center;
    gap: var(--global-dimension-size-50);
    border-radius: var(--global-rounding-small);
    cursor: help;
  }

  &[data-size="S"] {
    height: auto;
    padding: 0;
  }

  &[data-variant="quiet"],
  &[data-variant="quiet"]:hover:not([disabled]) {
    border-color: transparent;
    background-color: transparent;
  }

  .chat-token-usage-details__segment-text {
    text-decoration: underline dotted;
    text-underline-offset: 2px;
  }

  &:focus-visible {
    outline: var(--global-border-size-thick) solid var(--focus-ring-color);
    outline-offset: var(--focus-ring-offset);
  }
`,Xv=U`
  width: var(--global-dimension-size-100);
  height: var(--global-dimension-size-100);
  flex: none;
  border-radius: var(--global-rounding-full);
`,Zv=U`
  .chat-token-usage-details__tooltip-title {
    margin-bottom: var(--global-dimension-size-100);
  }

  .chat-token-usage-details__tooltip-segments {
    display: flex;
    flex-direction: column;
    gap: var(--global-dimension-size-75);
    list-style: none;
    margin: 0;
    padding: 0;
  }

  .chat-token-usage-details__tooltip-segment {
    display: flex;
    align-items: center;
    gap: var(--global-dimension-size-50);
  }
`;function Qv({value:e,maximum:t}){return Math.min(Math.max(e,0),Math.max(t,0))}function $v(e){let t=(0,Y.c)(10),{segment:n}=e,r;t[0]===n.color?r=t[1]:(r=B(`span`,{className:`chat-token-usage-details__swatch`,css:Xv,style:{backgroundColor:n.color},"aria-hidden":`true`}),t[0]=n.color,t[1]=r);let i;t[2]===n.value?i=t[3]:(i=yv(n.value),t[2]=n.value,t[3]=i);let a;t[4]!==n.name||t[5]!==i?(a=V(L,{className:`chat-token-usage-details__segment-text`,size:`XS`,color:`text-500`,fontFamily:`mono`,children:[i,` `,n.name]}),t[4]=n.name,t[5]=i,t[6]=a):a=t[6];let o;return t[7]!==r||t[8]!==a?(o=V(R,{children:[r,a]}),t[7]=r,t[8]=a,t[9]=o):o=t[9],o}function ey(e){let t=(0,Y.c)(15),{promptSegment:n,promptDetailsSegments:r}=e,i;t[0]===n.value?i=t[1]:(i=vv(n.value),t[0]=n.value,t[1]=i);let a=`${i} prompt tokens. Show cache details`,o;t[2]===n?o=t[3]:(o=B($v,{segment:n}),t[2]=n,t[3]=o);let s;t[4]!==a||t[5]!==o?(s=B(H,{className:`chat-token-usage-details__segment-trigger`,css:Yv,size:`S`,variant:`quiet`,"aria-label":a,children:o}),t[4]=a,t[5]=o,t[6]=s):s=t[6];let c;t[7]===Symbol.for(`react.memo_cache_sentinel`)?(c=B(L,{className:`chat-token-usage-details__tooltip-title`,size:`XS`,color:`text-700`,weight:`heavy`,children:`Prompt details`}),t[7]=c):c=t[7];let l;t[8]===r?l=t[9]:(l=r.map(ty),t[8]=r,t[9]=l);let u;t[10]===l?u=t[11]:(u=V(wa,{css:Zv,placement:`top`,offset:3,children:[c,B(`ul`,{className:`chat-token-usage-details__tooltip-segments`,"aria-label":`Prompt token types`,children:l})]}),t[10]=l,t[11]=u);let d;return t[12]!==s||t[13]!==u?(d=B(`li`,{className:`chat-token-usage-details__segment`,children:V(Se,{delay:0,closeDelay:0,children:[s,u]})}),t[12]=s,t[13]=u,t[14]=d):d=t[14],d}function ty(e){return B(`li`,{className:`chat-token-usage-details__tooltip-segment`,children:B($v,{segment:e})},e.name)}function ny(e){let t=(0,Y.c)(45),{total:n,prompt:r,completion:i,promptDetails:a}=e,o=cv(),s=a?.cacheRead??0,c;t[0]!==r||t[1]!==s?(c=Qv({value:s,maximum:r}),t[0]=r,t[1]=s,t[2]=c):c=t[2];let l=c,u=a?.cacheWrite??0,d=Math.max(r-l,0),f;t[3]!==u||t[4]!==d?(f=Qv({value:u,maximum:d}),t[3]=u,t[4]=d,t[5]=f):f=t[5];let p=f,m=Math.max(r-l-p,0),h=r>0&&(l>0||p>0),g;t[6]!==o.category1||t[7]!==r?(g={name:`Prompt`,value:r,color:o.category1},t[6]=o.category1,t[7]=r,t[8]=g):g=t[8];let _;t[9]!==o.category2||t[10]!==i?(_={name:`Completion`,value:i,color:o.category2},t[9]=o.category2,t[10]=i,t[11]=_):_=t[11];let v;t[12]!==g||t[13]!==_?(v=[g,_],t[12]=g,t[13]=_,t[14]=v):v=t[14];let y=v,b;t[15]===o?b=t[16]:(b=Gv({colors:o,tokenType:`input`}),t[15]=o,t[16]=b);let x;t[17]!==b||t[18]!==m?(x={name:`Uncached`,value:m,color:b},t[17]=b,t[18]=m,t[19]=x):x=t[19];let S;t[20]===o?S=t[21]:(S=Gv({colors:o,tokenType:`cache_read`}),t[20]=o,t[21]=S);let C;t[22]!==l||t[23]!==S?(C={name:`Cache read`,value:l,color:S},t[22]=l,t[23]=S,t[24]=C):C=t[24];let w;t[25]===o?w=t[26]:(w=Gv({colors:o,tokenType:`cache_write`}),t[25]=o,t[26]=w);let T;t[27]!==p||t[28]!==w?(T={name:`Cache write`,value:p,color:w},t[27]=p,t[28]=w,t[29]=T):T=t[29];let E;t[30]!==x||t[31]!==C||t[32]!==T?(E=[x,C,T].filter(ry),t[30]=x,t[31]=C,t[32]=T,t[33]=E):E=t[33];let D=E,O;t[34]!==y||t[35]!==n?(O=B(`div`,{"aria-hidden":`true`,children:B(_v,{height:6,minimumSegmentPercentage:1,totalValue:n,segments:y})}),t[34]=y,t[35]=n,t[36]=O):O=t[36];let k;t[37]===Symbol.for(`react.memo_cache_sentinel`)?(k=B(L,{size:`XS`,color:`text-700`,weight:`heavy`,children:`Total`}),t[37]=k):k=t[37];let A;t[38]!==y||t[39]!==h||t[40]!==D?(A=V(`div`,{className:`chat-token-usage-details__legend`,children:[k,B(`ul`,{className:`chat-token-usage-details__segments`,"aria-label":`Token types`,children:y.map(e=>e.name===`Prompt`&&h?B(ey,{promptSegment:e,promptDetailsSegments:D},e.name):B(`li`,{className:`chat-token-usage-details__segment`,children:B($v,{segment:e})},e.name))})]}),t[38]=y,t[39]=h,t[40]=D,t[41]=A):A=t[41];let j;return t[42]!==O||t[43]!==A?(j=V(`div`,{className:`chat-token-usage-details`,css:Jv,role:`region`,"aria-label":`Token usage breakdown`,children:[O,A]}),t[42]=O,t[43]=A,t[44]=j):j=t[44],j}function ry(e){return e.value>0}function iy(e){let t=(0,Y.c)(24),{total:n,prompt:r,completion:i,promptDetails:a}=e,[o,s]=(0,J.useState)(!1),c=(0,J.useId)(),l;t[0]===n?l=t[1]:(l=vv(n),t[0]=n,t[1]=l);let u=`${l} total tokens`,d;t[2]===Symbol.for(`react.memo_cache_sentinel`)?(d=()=>s(ay),t[2]=d):d=t[2];let f;t[3]===n?f=t[4]:(f=B(Lv,{size:`S`,color:`text-300`,children:n}),t[3]=n,t[4]=f);let p;t[5]===o?p=t[6]:(p=B(Jt,{isExpanded:o}),t[5]=o,t[6]=p);let m;t[7]!==c||t[8]!==o||t[9]!==u||t[10]!==f||t[11]!==p?(m=B(`div`,{className:`chat-token-usage__summary`,children:V(`button`,{className:`chat-token-usage__trigger button--reset`,type:`button`,"aria-controls":c,"aria-expanded":o,"aria-label":u,onClick:d,children:[f,p]})}),t[7]=c,t[8]=o,t[9]=u,t[10]=f,t[11]=p,t[12]=m):m=t[12];let h;t[13]!==i||t[14]!==c||t[15]!==o||t[16]!==r||t[17]!==a||t[18]!==n?(h=o?B(`div`,{className:`chat-token-usage__details`,id:c,children:B(ny,{total:n,prompt:r,completion:i,promptDetails:a})}):null,t[13]=i,t[14]=c,t[15]=o,t[16]=r,t[17]=a,t[18]=n,t[19]=h):h=t[19];let g;return t[20]!==o||t[21]!==m||t[22]!==h?(g=V(`div`,{className:`chat-token-usage`,css:qv,"data-expanded":o,children:[m,h]}),t[20]=o,t[21]=m,t[22]=h,t[23]=g):g=t[23],g}function ay(e){return!e}var oy=(0,J.createContext)(null);function sy(){return(0,J.useContext)(oy)}function cy(e){let t=e.parentElement;for(;t;){let{overflowY:e}=getComputedStyle(t);if((e===`auto`||e===`scroll`)&&t.scrollHeight>t.clientHeight)return t;t=t.parentElement}return null}function ly(){let e=(0,Y.c)(5),t=sy(),n=(0,J.useRef)(null),r;e[0]===t?r=e[1]:(r=e=>{if(t?.stopScroll(),n.current=null,!e)return;let r=cy(e);if(!r)return;let i=e.getBoundingClientRect(),a=r.getBoundingClientRect();n.current={scrollParent:r,offsetFromParentTop:i.top-a.top}},e[0]=t,e[1]=r);let i=r,a;e[2]===Symbol.for(`react.memo_cache_sentinel`)?(a=e=>{let t=n.current;if(n.current=null,!t||!e)return;let{scrollParent:r,offsetFromParentTop:i}=t,a=e.getBoundingClientRect(),o=r.getBoundingClientRect(),s=a.top-o.top;r.scrollTop+=s-i},e[2]=a):a=e[2];let o=a,s;return e[3]===i?s=e[4]:(s={capture:i,restore:o},e[3]=i,e[4]=s),s}var uy=Wt`
  from {
    opacity: 0;
    transform: translateY(-2px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
`,dy={titleFlex:`0 1 auto`,titleMinWidth:`0`,titleMaxWidth:`55%`,middleFlex:`1 1 50px`,middleMinWidth:`50px`,statusFlex:`0 1 auto`,statusMinWidth:`0`,statusMaxWidth:`none`};function fy(e){let t=(0,Y.c)(3),{children:n,variant:r}=e,i;return t[0]!==n||t[1]!==r?(i=B(`div`,{className:`tool-part__line`,children:B(`span`,{className:`tool-part__label`,"data-variant":r,children:n})}),t[0]=n,t[1]=r,t[2]=i):i=t[2],i}function py({children:e,allowCopy:t=!0}){return V(`div`,{className:`tool-part__line${t?` tool-part__line--copyable`:``}`,children:[B(`code`,{className:`tool-part__code`,children:e||`(empty)`}),t?B(Aa,{text:e,size:`S`,variant:`quiet`,tooltipText:`Copy`}):null]})}function my(e){let t=(0,Y.c)(3),{children:n,variant:r}=e,i;return t[0]!==n||t[1]!==r?(i=B(`span`,{className:`tool-part__status`,"data-variant":r,children:n}),t[0]=n,t[1]=r,t[2]=i):i=t[2],i}function hy(e){let t=(0,Y.c)(4),{items:n}=e,r;t[0]===n?r=t[1]:(r=n.map(gy),t[0]=n,t[1]=r);let i;return t[2]===r?i=t[3]:(i=B(`div`,{className:`tool-part__meta`,children:r}),t[2]=r,t[3]=i),i}function gy(e){let{label:t,value:n}=e;return V(`span`,{className:`tool-part__meta-group`,children:[B(`span`,{className:`tool-part__meta-label`,children:t}),B(`code`,{className:`tool-part__meta-value`,children:n})]},t)}var _y=U`
  padding: var(--global-dimension-size-50) var(--global-dimension-size-200)
    var(--global-dimension-size-150);
`;function vy({onAccept:e,onReject:t,isDisabled:n=!1,staleMessage:r}){let i=lh(e=>Wm(e,e.activeSessionId)),a=n||i;return V(R,{children:[B(`div`,{css:_y,children:V(W,{direction:`row-reverse`,gap:`size-100`,children:[B(H,{size:`S`,variant:`primary`,isDisabled:a,onPress:e,children:`Accept`}),B(H,{size:`S`,isDisabled:a,onPress:t,children:`Reject`})]})}),n&&r?B(py,{children:r}):null]})}var yy=320,by=U`
  --expandable-content-overlay-background-color: var(
    --tool-call-body-background-color
  );
`;function xy(e){let t=(0,Y.c)(6),{children:n}=e,r=(0,J.useRef)(null),[i,a]=(0,J.useState)(!1),o=ly(),s;t[0]===o?s=t[1]:(s=e=>{o.capture(r.current),a(e),requestAnimationFrame(()=>o.restore(r.current))},t[0]=o,t[1]=s);let c=s,l;return t[2]!==n||t[3]!==c||t[4]!==i?(l=B(`div`,{ref:r,css:by,children:B(nt,{height:yy,expandedBehavior:`grow`,isExpanded:i,onExpandedChange:c,children:n})}),t[2]=n,t[3]=c,t[4]=i,t[5]=l):l=t[5],l}function Sy(e){switch(e){case`input-streaming`:return`Preparing`;case`input-available`:return`Running`;case`approval-requested`:return`Awaiting approval`;case`approval-responded`:return`Approval received`;case`output-available`:return`Completed`;case`output-error`:return`Error`;case`output-denied`:return`Denied`;default:return fr(e)}}function Cy(e){if(e==null)return``;if(typeof e==`string`)return e;try{return JSON.stringify(e,null,2)}catch{return String(e)}}export{P_ as $,ei as $a,wa as $i,Bu as $n,Xs as $r,lh as $t,Sv as A,Ii as Aa,_o as Ai,xp as An,Qc as Ar,Zh as At,cv as B,wi as Ba,Ya as Bi,tf as Bn,Oc as Br,Lh as Bt,Av as C,Ri as Ca,es as Ci,up as Cn,hr as Co,hl as Cr,Sg as Ct,vv as D,ji as Da,Ho as Di,_p as Dn,sl as Dr,gg as Dt,bv as E,Mi as Ea,Go as Ei,ip as En,cl as Er,_g as Et,Mv as F,ki as Fa,ao as Fi,Tf as Fn,Wc as Fr,Hh as Ft,X_ as G,mi as Ga,Ua as Gi,Zu as Gn,gc as Gr,Ch as Gt,av as H,Ei as Ha,qa as Hi,Qd as Hn,Cc as Hr,Ah as Ht,_v as I,Si as Ia,to as Ii,uf as In,zc as Ir,Vh as It,q_ as J,li as Ja,Fa as Ji,$u as Jn,oc as Jr,gh as Jt,Y_ as K,hi as Ka,Va as Ki,ed as Kn,mc as Kr,wh as Kt,mv as L,Ci as La,$a as Li,lf as Ln,Ic as Lr,Bh as Lt,Ov as M,Vi as Ma,uo as Mi,cp as Mn,Gc as Mr,Yh as Mt,Pv as N,zi as Na,lo as Ni,pp as Nn,qc as Nr,Gh as Nt,yv as O,Pi as Oa,jo as Oi,yp as On,nl as Or,$h as Ot,jv as P,Bi as Pa,oo as Pi,Z as Pn,Hc as Pr,Wh as Pt,I_ as Q,ci as Qa,Aa as Qi,Ku as Qn,Qs as Qr,ch as Qt,uv as R,bi as Ra,Qa as Ri,rf as Rn,Ac as Rr,Mh as Rt,Nv as S,Fi as Sa,os as Si,mp as Sn,vr as So,xl as Sr,Cg as St,wv as T,Ni as Ta,qo as Ti,ap as Tn,ll as Tr,wg as Tt,nv as U,xi as Ua,Na as Ui,od as Un,Tc as Ur,Oh as Ut,pv as V,Ti as Va,Ka as Vi,$d as Vn,Sc as Vr,jh as Vt,ev as W,Di as Wa,Ra as Wi,sd as Wn,vc as Wr,Dh as Wt,G_ as X,si as Xa,Ma as Xi,Xu as Xn,nc as Xr,ph as Xt,K_ as Y,ai as Ya,Ba as Yi,Qu as Yn,ic as Yr,fh as Yt,W_ as Z,oi as Za,Wa as Zi,Yu as Zn,ec as Zr,mh as Zt,Uv as _,Qi as _a,hs as _i,Cp as _n,Cr as _o,jl as _r,kg as _t,vy as a,ba as aa,Bs as ai,Wm as an,Jr as ao,du as ar,x_ as at,Hv as b,Wi as ba,rs as bi,gp as bn,_r as bo,Tl as br,vg as bt,fy as c,ha as ca,js as ci,Pm as cn,Vr as co,tu as cr,m_ as ct,cy as d,pa as da,Ts as di,Fm as dn,Nr as do,ql as dr,l_ as dt,Da as ea,Ks as ei,uh as en,Xr as eo,Mu as er,N_ as et,ly as f,da as fa,Cs as fi,Rm as fn,Tr as fo,Wl as fr,n_ as ft,Wv as g,$i as ga,ms as gi,Hm as gn,wr as go,Nl as gr,Ig as gt,Rv as h,ta as ha,gs as hi,zm as hn,Sr as ho,Fl as hr,Wg as ht,uy as i,Sa as ia,Vs as ii,Zm as in,qr as io,lu as ir,D_ as it,Dv as j,Hi as ja,mo as ji,bp as jn,Jc as jr,Xh as jt,Cv as k,Ai as ka,Oo as ki,sp as kn,tl as kr,Qh as kt,hy as l,ua as la,Os as li,Vm as ln,Br as lo,$l as lr,p_ as lt,iy as m,ia as ma,_s as mi,Bm as mn,xr as mo,Bl as mr,Gg as mt,Cy as n,Ta as na,Us as ni,$m as nn,ni as no,ku as nr,A_ as nt,py as o,X as oa,Rs as oi,Um as on,Rr as oo,fu as or,y_ as ot,oy as p,aa as pa,ys as pi,Lm as pn,Mr as po,Hl as pr,Kg as pt,J_ as q,di as qa,Ha as qi,td as qn,fc as qr,Sh as qt,dy as r,Ca as ra,Hs as ri,Qm as rn,Yr as ro,uu as rr,O_ as rt,xy as s,ma as sa,Ms as si,oh as sn,Ir as so,nu as sr,h_ as st,Sy as t,Ea as ta,Js as ti,Gm as tn,ti as to,Au as tr,M_ as tt,my as u,fa as ua,Es as ui,Im as un,Fr as uo,Xl as ur,u_ as ut,Gv as v,qi as va,ss as vi,lp as vn,fr as vo,Ol as vr,Dg as vt,kv as w,Li as wa,Qo as wi,op as wn,yr as wo,ul as wr,Tg as wt,Lv as x,Ui as xa,as as xi,vp as xn,gr as xo,Cl as xr,yg as xt,Kv as y,Gi as ya,is as yi,hp as yn,pr as yo,Dl as yr,Eg as yt,rv as z,Oi as za,Za as zi,nf as zn,Mc as zr,Rh as zt};