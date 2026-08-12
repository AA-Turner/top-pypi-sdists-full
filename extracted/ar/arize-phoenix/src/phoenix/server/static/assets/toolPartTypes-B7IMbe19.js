import{o as e}from"./rolldown-runtime-C_s2cVnS.js";import{$n as t,$t as n,An as r,Bn as i,Ct as a,Dn as o,En as s,Er as c,Fn as l,Hn as u,In as d,Jn as f,Kn as p,Ln as m,Nn as h,On as g,Qn as _,Qt as v,Rn as y,Sn as b,Sr as x,Tn as S,Un as C,Vn as w,Xn as T,Yn as E,Zn as D,_r as O,_t as k,an as A,ar as j,at as M,bn as N,br as P,bt as F,cn as I,cr as L,dn as ee,dr as te,en as ne,fn as re,fr as ie,gr as ae,hn as oe,ht as se,ir as ce,it as le,jn as ue,kn as de,ln as fe,mn as pe,mr as me,mt as he,nn as ge,nr as _e,on as ve,or as ye,ot as be,pn as xe,pr as Se,qn as Ce,rn as we,rt as Te,sn as Ee,sr as De,st as Oe,tr as ke,ur as Ae,vn as je,vr as Me,vt as Ne,wn as Pe,wt as Fe,xn as Ie,xr as Le,yn as Re,yr as ze,zn as Be}from"./vendor-D-NLM_Sx.js";import{D as Ve,M as R,d as He,rt as Ue,u as We,v as Ge,x as Ke,y as qe}from"./vendor-codemirror-DBU6IKGQ.js";import{C as z,b as Je,w as Ye,y as Xe}from"./vendor-recharts-CXg49ux2.js";import{$ as Ze,A as Qe,C as $e,Cn as et,D as B,Di as tt,Dt as nt,E as rt,Eo as it,Et as at,F as ot,Fn as st,Fo as V,Ft as ct,G as H,Gn as lt,Gt as ut,H as dt,Ha as ft,Ht as pt,Io as U,J as mt,Jr as ht,Jt as gt,K as _t,Ki as vt,Kr as yt,Kt as bt,L as xt,Ln as St,Lo as W,Lt as Ct,M as wt,Mi as Tt,Mn as Et,Na as Dt,Nn as Ot,Nt as kt,O as At,On as jt,P as Mt,Pa as Nt,R as Pt,Ro as Ft,Rt as It,S as Lt,Sn as Rt,T as zt,Tt as Bt,Ui as Vt,Ur as Ht,Ut,Vi as Wt,Vr as G,Vt as Gt,W as Kt,Wa as qt,Wn as Jt,Wr as Yt,Wt as Xt,Xa as Zt,Xi as Qt,Xr as $t,Xt as en,Y as tn,Yr as nn,Zr as rn,_t as an,bt as on,ci as sn,cn,ct as ln,di as un,dr as dn,ei as fn,er as pn,fa as mn,gn as hn,gr as gn,gt as _n,hr as vn,i as yn,ia as bn,j as xn,jn as Sn,k as Cn,ki as wn,ln as Tn,m as En,mn as Dn,mr as On,n as kn,oi as An,on as jn,p as Mn,q as Nn,qn as Pn,qt as Fn,r as In,ra as Ln,rr as Rn,rt as zn,sa as Bn,sn as Vn,sr as Hn,t as Un,un as Wn,ur as Gn,vr as Kn,vt as qn,wi as Jn,x as Yn,xn as Xn,xr as Zn,xt as Qn,y as $n,z as K}from"./vendor-streamdown-IFLESpXh.js";import{Hn as er,It as tr,On as nr,Ut as rr,Vn as q,Xn as ir,kn as ar,mr as or,pr as sr,qt as cr,rn as lr,tr as J}from"./vendor-ai-sdk-react-C7uh2X1G.js";var Y=e(Ue()),ur=e(Ye()),X=Ft();function dr(e){throw Error(`Unreachable`)}function fr(e){return typeof e==`number`||e===null}function pr(e){return typeof e==`string`||e===null}function mr(e){return pr(e)||e===void 0}function hr(e){return Array.isArray(e)?e.every(e=>typeof e==`string`):!1}function gr(e){return typeof e==`object`&&!!e}function _r(e){return gr(e)&&Object.keys(e).every(e=>typeof e==`string`)}var vr=()=>e=>e;(0,Y.createContext)(null);var yr=5e3,br=new pe({maxVisibleToasts:3}),xr=()=>wr,Sr=()=>Tr,Cr=()=>Er;function wr(e){let{expireMs:t,...n}=e,r=t===void 0?yr:t;return br.add({...n},r===null?void 0:{timeout:r})}function Tr(e){let{expireMs:t,...n}=e,r=t===void 0?yr:t;return br.add({...n,variant:`success`},r===null?void 0:{timeout:r})}function Er(e){let{expireMs:t,...n}=e,r=t===void 0?yr:t;return br.add({...n,variant:`error`},r===null?void 0:{timeout:r})}function Dr(e){return e===`light`||e===`dark`||e===`system`}var Or=`arize-phoenix-theme`,kr=`dark`,Ar=`(prefers-color-scheme: dark)`;function jr(){let e=localStorage.getItem(Or);return Dr(e)?e:kr}function Mr(){return window.matchMedia(Ar).matches?`dark`:`light`}var Nr=(0,Y.createContext)(null);function Pr(){let e=(0,Y.useContext)(Nr);if(e===null)throw Error(`useTheme must be used within a ThemeProvider`);return e}function Fr(e){let t=(0,X.c)(19),n;t[0]===e.themeMode?n=t[1]:(n=()=>e.themeMode||jr(),t[0]=e.themeMode,t[1]=n);let[r,i]=(0,Y.useState)(n),a;t[2]===Symbol.for(`react.memo_cache_sentinel`)?(a=e=>{localStorage.setItem(Or,e),i(e)},t[2]=a):a=t[2];let o=a,[s,c]=(0,Y.useState)(Mr),l;bb0:{if(r===`system`){l=s;break bb0}l=r}let u=l,d,f;t[3]===e.themeMode?(d=t[4],f=t[5]):(d=()=>{e.themeMode&&i(e.themeMode)},f=[e.themeMode,o],t[3]=e.themeMode,t[4]=d,t[5]=f),(0,Y.useEffect)(d,f);let p,m;t[6]===Symbol.for(`react.memo_cache_sentinel`)?(p=()=>{let e=window.matchMedia(Ar),t=()=>{c(Mr())};return e.addEventListener(`change`,t),()=>{e.removeEventListener(`change`,t)}},m=[],t[6]=p,t[7]=m):(p=t[6],m=t[7]),(0,Y.useEffect)(p,m);let h,g;t[8]!==e.disableBodyTheme||t[9]!==u?(h=()=>{if(!e.disableBodyTheme)return document.body.classList.add(`theme--${u}`),document.body.classList.add(`theme`),()=>{document.body.classList.remove(`theme--${u}`),document.body.classList.remove(`theme`)}},g=[u,e.disableBodyTheme],t[8]=e.disableBodyTheme,t[9]=u,t[10]=h,t[11]=g):(h=t[10],g=t[11]),(0,Y.useEffect)(h,g);let _;t[12]!==s||t[13]!==u||t[14]!==r?(_={theme:u,systemTheme:s,themeMode:r,setThemeMode:o},t[12]=s,t[13]=u,t[14]=r,t[15]=_):_=t[15];let v;return t[16]!==e.children||t[17]!==_?(v=U(Nr.Provider,{value:_,children:e.children}),t[16]=e.children,t[17]=_,t[18]=v):v=t[18],v}var Ir=[`traces`,`spans`,`sessions`,`metrics`],Lr=e=>Ir.includes(e),Rr=[`traffic`,`traces`,`latency`,`cost`,`top_models_by_cost`,`tokens`,`top_models_by_tokens`,`prompt_token_details`,`completion_token_details`,`llm_spans`,`llm_span_errors`,`tool_spans`,`tool_span_errors`,`span_annotations`,`trace_annotations`,`session_annotations`],zr=[`spans`,`traces`,`sessions`],Br=`Evaluation results over time`,Vr=`_annotation:`;function Hr({view:e,annotationName:t}){return`${e}${Vr}${t}`}function Ur(e){for(let t of zr){let n=`${t}${Vr}`;if(e.startsWith(n))return{view:t,annotationName:e.slice(n.length)}}}var Wr=e=>Rr.includes(e)||Ur(e)!=null,Gr={spans:[`traffic`],traces:[`traces`,`latency`,`trace_annotations`],sessions:[`traces`,`session_annotations`]},Kr=e=>`arize-phoenix-project-${e}`;function qr({projectId:e}){return{state:ne()(n(v(e=>({defaultTab:`spans`,setDefaultTab:t=>{e({defaultTab:t},!1,{type:`setDefaultTab`})},showTableAside:!0,setShowTableAside:t=>{e({showTableAside:t},!1,{type:`setShowTableAside`})},metricChartKeys:Gr,setMetricChartKeys:(t,n)=>{e(e=>({metricChartKeys:{...e.metricChartKeys,[t]:n}}),!1,{type:`setMetricChartKeys`})}})),{name:Kr(e),merge:(e,t)=>{let n={...t,...e},r={...Gr};for(let e of zr){let t=n.metricChartKeys?.[e];Array.isArray(t)&&(r[e]=t.filter(Wr))}return n.metricChartKeys=r,n}}))}}var Jr=(0,Y.createContext)(null);function Yr(e){let t=(0,X.c)(5),{children:n,projectId:r}=e,i;t[0]===r?i=t[1]:(i=()=>qr({projectId:r}),t[0]=r,t[1]=i);let[a]=(0,Y.useState)(i),o;return t[2]!==n||t[3]!==a?(o=U(Jr.Provider,{value:a,children:n}),t[2]=n,t[3]=a,t[4]=o):o=t[4],o}function Xr(e,t){let n=(0,Y.useContext)(Jr);if(!n)throw Error(`Missing ProjectContext.Provider in the tree`);return ge(n.state,e,t)}var Zr=[`Python`,`TypeScript`];function Qr(e){return typeof e==`string`&&Zr.includes(e)}var $r=[`npm`,`pnpm`,`bun`],ei=[`pip`,`uv`],ti=[...$r,...ei];function ni(e){return typeof e==`string`&&ti.includes(e)}function ri(e){return typeof e==`string`&&ei.includes(e)}function ii(e){return typeof e==`string`&&$r.includes(e)}var ai=Intl.DateTimeFormat().resolvedOptions(),oi=[];function si(){return ai.locale}function ci(){return ai.timeZone}function li(){return oi.length===0&&(oi=[...Intl.supportedValuesOf(`timeZone`)],oi.includes(`UTC`)||(oi=[`UTC`,...oi])),Object.freeze([...oi])}function ui(e,t){let n=new Intl.DateTimeFormat(`en-US`,{timeZone:t,year:`numeric`,month:`2-digit`,day:`2-digit`,hour:`2-digit`,minute:`2-digit`,second:`2-digit`,hour12:!1}).formatToParts(e).reduce((e,t)=>(t.type!==`literal`&&(e[t.type]=t.value),e),{}),{year:r,month:i,day:a}=n,o=n.hour;if(o===`24`){o=`00`;let e=new Date(`${r}-${i}-${a}T00:00:00Z`);e.setUTCDate(e.getUTCDate()+1),r=String(e.getUTCFullYear()),i=String(e.getUTCMonth()+1).padStart(2,`0`),a=String(e.getUTCDate()).padStart(2,`0`)}let s=`${r}-${i}-${a}`,c=`${o}:${n.minute}:${n.second}`,l=new Date(`${s}T${c}Z`).getTime(),u=Math.round((l-e.getTime())/6e4),d=u>=0?`+`:`-`,f=Math.abs(u);return`${s}T${c}${d}${String(Math.floor(f/60)).padStart(2,`0`)}:${String(f%60).padStart(2,`0`)}`}var di={Python:ei,TypeScript:$r},fi={Python:`pip`,TypeScript:`npm`},pi=[``,`apac`,`au`,`ca`,`eu`,`global`,`il`,`jp`,`us`,`us-gov`],mi=e=>ne()(n(v(t=>({markdownDisplayMode:`text`,setMarkdownDisplayMode:e=>{t({markdownDisplayMode:e},!1,{type:`setMarkdownDisplayMode`})},traceStreamingEnabled:!0,setTraceStreamingEnabled:e=>{t({traceStreamingEnabled:e},!1,{type:`setTraceStreamingEnabled`})},lastNTimeRangeKey:`7d`,setLastNTimeRangeKey:e=>{t({lastNTimeRangeKey:e})},projectsAutoRefreshEnabled:!0,setProjectAutoRefreshEnabled:e=>{t({projectsAutoRefreshEnabled:e},!1,{type:`setProjectAutoRefreshEnabled`})},showMetricsInTraceTree:!0,setShowMetricsInTraceTree:e=>{t({showMetricsInTraceTree:e},!1,{type:`setShowMetricsInTraceTree`})},areTableRowsExpanded:!1,setAreTableRowsExpanded:e=>{t({areTableRowsExpanded:e},!1,{type:`setAreTableRowsExpanded`})},modelConfigByProvider:{},setModelConfigForProvider:({provider:e,modelConfig:n})=>{t(t=>({modelConfigByProvider:{...t.modelConfigByProvider,[e]:n}}),!1,{type:`setModelConfigForProvider`})},playgroundStreamingEnabled:!0,setPlaygroundStreamingEnabled:e=>{t({playgroundStreamingEnabled:e},!1,{type:`setPlaygroundStreamingEnabled`})},isAnnotatingSpans:!1,setIsAnnotatingSpans:e=>{t({isAnnotatingSpans:e},!1,{type:`setIsAnnotatingSpans`})},isTakingSpanNotes:!1,setIsTakingSpanNotes:e=>{t({isTakingSpanNotes:e},!1,{type:`setIsTakingSpanNotes`})},projectViewMode:`grid`,setProjectViewMode:e=>{t({projectViewMode:e},!1,{type:`setProjectViewMode`})},projectSortOrder:{column:`endTime`,direction:`desc`},setProjectSortOrder:e=>{t({projectSortOrder:e},!1,{type:`setProjectSortOrder`})},lastSelectedDashboardProjectId:void 0,setLastSelectedDashboardProjectId:e=>{t({lastSelectedDashboardProjectId:e},!1,{type:`setLastSelectedDashboardProjectId`})},isSideNavExpanded:!0,setIsSideNavExpanded:e=>{t({isSideNavExpanded:e},!1,{type:`setIsSideNavExpanded`})},setDisplayTimezone:e=>{if(e&&!li().includes(e))throw Error(`Invalid timezone: ${e}`);t({displayTimezone:e},!1,{type:`setDisplayTimezone`})},programmingLanguage:`Python`,setProgrammingLanguage:e=>{t({programmingLanguage:e},!1,{type:`setProgrammingLanguage`})},packageManagerByLanguage:{...fi},setPackageManager:(e,n)=>{t(t=>({packageManagerByLanguage:{...t.packageManagerByLanguage,[e]:n}}),!1,{type:`setPackageManager`})},awsBedrockModelPrefix:`us`,setAwsBedrockModelPrefix:e=>{t({awsBedrockModelPrefix:e},!1,{type:`setAwsBedrockModelPrefix`})},isAssistantAgentEnabled:!0,setIsAssistantAgentEnabled:e=>{t({isAssistantAgentEnabled:e},!1,{type:`setIsAssistantAgentEnabled`})},defaultModelProvider:void 0,setDefaultModelProvider:e=>{t({defaultModelProvider:e},!1,{type:`setDefaultModelProvider`})},defaultModelName:void 0,setDefaultModelName:e=>{let n=e?.trim();t({defaultModelName:n||void 0},!1,{type:`setDefaultModelName`})},isAIQueryEnabled:!0,setIsAIQueryEnabled:e=>{t({isAIQueryEnabled:e},!1,{type:`setIsAIQueryEnabled`})},aiQueryModelConfig:void 0,setAIQueryModelConfig:e=>{t({aiQueryModelConfig:e},!1,{type:`setAIQueryModelConfig`})},...e}),{name:`preferencesStore`}),{name:`arize-phoenix-preferences`})),hi=(0,Y.createContext)(null);function gi(e){let t=(0,X.c)(8),n,r;t[0]===e?(n=t[1],r=t[2]):({children:n,...r}=e,t[0]=e,t[1]=n,t[2]=r);let i;t[3]===r?i=t[4]:(i=()=>mi(r),t[3]=r,t[4]=i);let[a]=(0,Y.useState)(i),o;return t[5]!==n||t[6]!==a?(o=U(hi.Provider,{value:a,children:n}),t[5]=n,t[6]=a,t[7]=o):o=t[7],o}function _i(e,t){let n=(0,Y.useContext)(hi);if(!n)throw Error(`Missing PreferencesContext.Provider in the tree`);return ge(n,e,t)}var vi=function(){var e={alias:null,args:null,kind:`ScalarField`,name:`id`,storageKey:null},t={alias:null,args:null,kind:`ScalarField`,name:`name`,storageKey:null},n={alias:null,args:null,kind:`ScalarField`,name:`createdAt`,storageKey:null},r={alias:null,args:null,kind:`ScalarField`,name:`expiresAt`,storageKey:null};return{fragment:{argumentDefinitions:[],kind:`Fragment`,metadata:null,name:`ViewerContextRefetchQuery`,selections:[{args:null,kind:`FragmentSpread`,name:`ViewerContext_viewer`}],type:`Query`,abstractKey:null},kind:`Request`,operation:{argumentDefinitions:[],kind:`Operation`,name:`ViewerContextRefetchQuery`,selections:[{alias:null,args:null,concreteType:`User`,kind:`LinkedField`,name:`viewer`,plural:!1,selections:[e,{alias:null,args:null,kind:`ScalarField`,name:`username`,storageKey:null},{alias:null,args:null,kind:`ScalarField`,name:`email`,storageKey:null},{alias:null,args:null,kind:`ScalarField`,name:`profilePictureUrl`,storageKey:null},{alias:null,args:null,kind:`ScalarField`,name:`isManagementUser`,storageKey:null},{alias:null,args:null,concreteType:`UserRole`,kind:`LinkedField`,name:`role`,plural:!1,selections:[t,e],storageKey:null},{alias:null,args:null,kind:`ScalarField`,name:`authMethod`,storageKey:null},{alias:null,args:null,concreteType:`UserApiKey`,kind:`LinkedField`,name:`apiKeys`,plural:!0,selections:[e,t,{alias:null,args:null,kind:`ScalarField`,name:`description`,storageKey:null},n,r],storageKey:null},{alias:null,args:null,concreteType:`OAuth2Grant`,kind:`LinkedField`,name:`oauth2Grants`,plural:!0,selections:[e,{alias:null,args:null,kind:`ScalarField`,name:`clientName`,storageKey:null},{alias:null,args:null,kind:`ScalarField`,name:`clientId`,storageKey:null},{alias:null,args:null,kind:`ScalarField`,name:`isFirstParty`,storageKey:null},{alias:null,args:null,kind:`ScalarField`,name:`scopes`,storageKey:null},n,r,{alias:null,args:null,kind:`ScalarField`,name:`lastUsedAt`,storageKey:null}],storageKey:null}],storageKey:null}]},params:{cacheID:`67fdf1bb616d5781701a75f68282f178`,id:null,metadata:{},name:`ViewerContextRefetchQuery`,operationKind:`query`,text:`query ViewerContextRefetchQuery {
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
`}}}();vi.hash=`53341d080ff76da24b2f1bc9e36c4e23`;var yi={argumentDefinitions:[],kind:`Fragment`,metadata:{refetch:{connection:null,fragmentPathInResult:[],operation:vi}},name:`ViewerContext_viewer`,selections:[{alias:null,args:null,concreteType:`User`,kind:`LinkedField`,name:`viewer`,plural:!1,selections:[{alias:null,args:null,kind:`ScalarField`,name:`id`,storageKey:null},{alias:null,args:null,kind:`ScalarField`,name:`username`,storageKey:null},{alias:null,args:null,kind:`ScalarField`,name:`email`,storageKey:null},{alias:null,args:null,kind:`ScalarField`,name:`profilePictureUrl`,storageKey:null},{alias:null,args:null,kind:`ScalarField`,name:`isManagementUser`,storageKey:null},{alias:null,args:null,concreteType:`UserRole`,kind:`LinkedField`,name:`role`,plural:!1,selections:[{alias:null,args:null,kind:`ScalarField`,name:`name`,storageKey:null}],storageKey:null},{alias:null,args:null,kind:`ScalarField`,name:`authMethod`,storageKey:null},{args:null,kind:`FragmentSpread`,name:`ViewerAPIKeysListFragment`},{args:null,kind:`FragmentSpread`,name:`AuthorizedApplicationsCardFragment`}],storageKey:null}],type:`Query`,abstractKey:null};yi.hash=`53341d080ff76da24b2f1bc9e36c4e23`;var bi=c(),xi=Y.createContext({viewer:null,refetchViewer:()=>{}});function Si(){let e=Y.useContext(xi);if(e==null)throw Error(`useViewer must be used within a ViewerProvider`);return e}function Ci(){let{viewer:e}=Si();return!(e&&e.role.name===`VIEWER`)}function wi(){let e=Ti();return!window.Config.authenticationEnabled||e}function Ti(){let{viewer:e}=Si();return window.Config.authenticationEnabled&&e?.role?.name===`ADMIN`}function Ei(){return wi()}function Di(){return wi()}function Oi(){return wi()}function ki(){return wi()}function Ai(){return wi()}function ji(e){let t=(0,X.c)(9),{query:n,children:r}=e,i;t[0]===Symbol.for(`react.memo_cache_sentinel`)?(i=yi,t[0]=i):i=t[0];let[a,o]=(0,bi.useRefetchableFragment)(i,n),s;t[1]===o?s=t[2]:(s=()=>{(0,Y.startTransition)(()=>{o({},{fetchPolicy:`network-only`})})},t[1]=o,t[2]=s);let c=s,l;t[3]!==a.viewer||t[4]!==c?(l={viewer:a.viewer,refetchViewer:c},t[3]=a.viewer,t[4]=c,t[5]=l):l=t[5];let u;return t[6]!==r||t[7]!==l?(u=U(xi.Provider,{value:l,children:r}),t[6]=r,t[7]=l,t[8]=u):u=t[8],u}var Mi={OPENAI:`OpenAI`,AZURE_OPENAI:`Azure OpenAI`,ANTHROPIC:`Anthropic`,GOOGLE:`Google`,DEEPSEEK:`DeepSeek`,XAI:`xAI`,OLLAMA:`Ollama`,AWS:`AWS Bedrock`,CEREBRAS:`Cerebras`,FIREWORKS:`Fireworks`,GROQ:`Groq`,MOONSHOT:`Moonshot`,PERPLEXITY:`Perplexity`,TOGETHER:`Together`},Ni=`OPENAI`,Pi=`gpt-5.6-luna`,Fi=`user`,Ii=`RESPONSES`,Li={user:[`user`,`human`],ai:[`assistant`,`bot`,`ai`,`model`],system:[`system`,`developer`],tool:[`tool`]},Ri={OPENAI:[{envVarName:`OPENAI_API_KEY`,isRequired:!0}],AZURE_OPENAI:[{envVarName:`AZURE_OPENAI_API_KEY`,isRequired:!0}],ANTHROPIC:[{envVarName:`ANTHROPIC_API_KEY`,isRequired:!0}],GOOGLE:[{envVarName:`GEMINI_API_KEY`,isRequired:!0}],DEEPSEEK:[{envVarName:`DEEPSEEK_API_KEY`,isRequired:!0}],XAI:[{envVarName:`XAI_API_KEY`,isRequired:!0}],OLLAMA:[],CEREBRAS:[{envVarName:`CEREBRAS_API_KEY`,isRequired:!0}],FIREWORKS:[{envVarName:`FIREWORKS_API_KEY`,isRequired:!0}],GROQ:[{envVarName:`GROQ_API_KEY`,isRequired:!0}],MOONSHOT:[{envVarName:`MOONSHOT_API_KEY`,isRequired:!0}],PERPLEXITY:[{envVarName:`PERPLEXITY_API_KEY`,isRequired:!0}],TOGETHER:[{envVarName:`TOGETHER_API_KEY`,isRequired:!0}],AWS:[{envVarName:`AWS_ACCESS_KEY_ID`,isRequired:!0},{envVarName:`AWS_SECRET_ACCESS_KEY`,isRequired:!0},{envVarName:`AWS_SESSION_TOKEN`,isRequired:!1}]},zi=`api_key`,Bi=`default_credentials`,Vi={OPENAI:`OPENAI`,AZURE_OPENAI:`AZURE_OPENAI`,ANTHROPIC:`ANTHROPIC`,AWS_BEDROCK:`AWS`,GOOGLE_GENAI:`GOOGLE`},Hi={openai:`OPENAI`,azure:`AZURE_OPENAI`,anthropic:`ANTHROPIC`,aws:`AWS`,google:`GOOGLE`,xai:`XAI`,ollama:`OLLAMA`,deepseek:`DEEPSEEK`,cerebras:`CEREBRAS`,fireworks:`FIREWORKS`,groq:`GROQ`,moonshot:`MOONSHOT`,perplexity:`PERPLEXITY`,together:`TOGETHER`},Ui=Object.entries({OPENAI:`OpenAI`,AZURE_OPENAI:`Azure OpenAI`,ANTHROPIC:`Anthropic`,AWS_BEDROCK:`AWS Bedrock`,GOOGLE_GENAI:`Google GenAI`}).map(([e,t])=>({id:e,label:t})),Wi={OPENAI:`openai`,AZURE_OPENAI:`azure`,ANTHROPIC:`anthropic`,AWS_BEDROCK:`aws`,GOOGLE_GENAI:`google`},Gi=Object.entries({api_key:`API Key`,ad_token_provider:`Azure AD Token Provider`,default_credentials:`Default Credentials (Managed Identity)`}).map(([e,t])=>({id:e,label:t})),Ki=Object.entries({default_credentials:`Default Credentials (IAM Role)`,access_keys:`Access Keys`}).map(([e,t])=>({id:e,label:t}));function qi(e){let t=(0,X.c)(4),n;t[0]===Symbol.for(`react.memo_cache_sentinel`)?(n=G`
        display: inline-block;
        max-width: 100%;
        min-width: 0;
        color: var(--global-link-color);
      `,t[0]=n):n=t[0];let r;t[1]===Symbol.for(`react.memo_cache_sentinel`)?(r=G`
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
        `,t[1]=r):r=t[1];let i;return t[2]===e?i=t[3]:(i=U(`div`,{className:`link-container`,onClick:Ji,css:n,children:U(Kn,{css:r,...e})}),t[2]=e,t[3]=i),i}function Ji(e){return e.stopPropagation()}function Yi(e){let t=(0,X.c)(5),{href:n,children:r}=e,i;t[0]===Symbol.for(`react.memo_cache_sentinel`)?(i=G`
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
      `,t[0]=i):i=t[0];let a;t[1]===Symbol.for(`react.memo_cache_sentinel`)?(a=U(H,{svg:U(pt,{})}),t[1]=a):a=t[1];let o;return t[2]!==r||t[3]!==n?(o=W(`a`,{href:n,target:`_blank`,css:i,rel:`noreferrer`,children:[r,a]}),t[2]=r,t[3]=n,t[4]=o):o=t[4],o}var Xi=Ht`
  100% {
    transform: rotate(360deg);
  }
`,Zi=Ht`
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
`,Qi=G`
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
      animation: ${Xi} 3s linear infinite;
    }
    .progress-circle__arc {
      animation: ${Zi} 3s cubic-bezier(0.4, 0, 0.2, 1) infinite;
      stroke-dasharray:
        calc(var(--progress-circle-circumference) * 0.25),
        var(--progress-circle-circumference);
      stroke-dashoffset: 0;
    }
  }
`,$i=G`
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
`;function ea(e){let t=(0,X.c)(13),n,r;t[0]===e?(n=t[1],r=t[2]):({ref:r,...n}=e,t[0]=e,t[1]=n,t[2]=r);let{isIndeterminate:i,value:a,size:o}=n,s=i!==void 0&&i,c=o===void 0?`M`:o,l=s||void 0,u;t[3]!==s||t[4]!==a?(u=!s&&a!=null?{"--progress-circle-value":a}:void 0,t[3]=s,t[4]=a,t[5]=u):u=t[5];let d;t[6]===Symbol.for(`react.memo_cache_sentinel`)?(d=W(`svg`,{className:`progress-circle__svg`,children:[U(`circle`,{className:`progress-circle__background`}),U(`circle`,{className:`progress-circle__arc`})]}),t[6]=d):d=t[6];let f;return t[7]!==n||t[8]!==r||t[9]!==c||t[10]!==l||t[11]!==u?(f=U(Qt,{...n,"data-size":c,"data-indeterminate":l,css:Qi,ref:r,style:u,children:d}),t[7]=n,t[8]=r,t[9]=c,t[10]=l,t[11]=u,t[12]=f):f=t[12],f}function ta(e){let t=(0,X.c)(12),n,r,i,a;t[0]===e?(n=t[1],r=t[2],i=t[3],a=t[4]):({ref:i,width:a,height:n,...r}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a);let o;t[5]!==n||t[6]!==a?(o={width:a,height:n},t[5]=n,t[6]=a,t[7]=o):o=t[7];let s;return t[8]!==r||t[9]!==i||t[10]!==o?(s=U(Qt,{...r,ref:i,css:$i,style:o,children:na}),t[8]=r,t[9]=i,t[10]=o,t[11]=s):s=t[11],s}function na(e){let{percentage:t}=e;return U(`div`,{className:`progress-bar__track`,children:U(`div`,{className:`progress-bar__fill`,style:{width:t+`%`}})})}function ra(e){let t=(0,X.c)(7),{ref:n,...r}=e,{children:i,elementType:a,...o}=r,s=a===void 0?`div`:a,{styleProps:c}=vn(r,gn),l=mn(o),u;t[0]===Symbol.for(`react.memo_cache_sentinel`)?(u=G`
        overflow: hidden;
        box-sizing: border-box;
      `,t[0]=u):u=t[0];let d;return t[1]!==s||t[2]!==i||t[3]!==n||t[4]!==c||t[5]!==l?(d=U(s,{...l,...c,ref:n,css:u,className:`view`,children:i}),t[1]=s,t[2]=i,t[3]=n,t[4]=c,t[5]=l,t[6]=d):d=t[6],d}var ia=G`
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
`,aa=G`
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
`;function oa(e){let t=(0,X.c)(10),n,r,i,a;if(t[0]!==e){let{ref:o,...s}=e,{css:c,...l}=s;n=A,r=l,i=o,a=G(ia,c),t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a}else n=t[1],r=t[2],i=t[3],a=t[4];let o;return t[5]!==n||t[6]!==r||t[7]!==i||t[8]!==a?(o=U(n,{...r,ref:i,css:a}),t[5]=n,t[6]=r,t[7]=i,t[8]=a,t[9]=o):o=t[9],o}function sa(e){let t=(0,X.c)(8),n,r;t[0]===e?(n=t[1],r=t[2]):({ref:r,...n}=e,t[0]=e,t[1]=n,t[2]=r);let{css:i}=n,a;t[3]===Symbol.for(`react.memo_cache_sentinel`)?(a=z(`react-aria-OverlayArrow`),t[3]=a):a=t[3];let o;t[4]===Symbol.for(`react.memo_cache_sentinel`)?(o=U(`svg`,{width:8,height:8,viewBox:`0 0 8 8`,children:U(`path`,{d:`M0 0 L4 4 L8 0`})}),t[4]=o):o=t[4];let s;return t[5]!==i||t[6]!==r?(s=U(un,{ref:r,css:i,className:a,children:o}),t[5]=i,t[6]=r,t[7]=s):s=t[7],s}var ca=1e3,la=60*ca,ua=60*la,da=24*ua;7*da;var fa=30*da,pa=31536e3,ma=2592e3,ha=604800,ga=86400,_a=3600,va=`https://arize.com/docs/phoenix`,ya={accessControl:`${va}/settings/access-control-rbac`,annotationConfigs:`${va}/tracing/how-to-tracing/feedback-and-annotations/annotating-in-the-ui`,apiKeys:`${va}/settings/api-keys`,customAiProviders:`${va}/settings/custom-ai-providers`,dataRetention:`${va}/settings/data-retention`,datasetLabels:`${va}/release-notes/10-2025/10-08-2025-dataset-labels`,modelCostTracking:`${va}/tracing/how-to-tracing/cost-tracking`,remoteMcpServer:`${va}/integrations/remote-mcp`,promptLabels:`${va}/release-notes/09-2025/09-15-2025-prompt-labels`,providers:`${va}/prompt-engineering/how-to-prompts/configure-ai-providers`,pxi:`${va}/pxi`,sandboxes:`${va}/settings/sandboxes`,secrets:`${va}/settings/secrets`},ba={aiProviderSettings:{href:ya.providers,label:`AI provider settings`},aiProviders:{href:ya.providers,label:`AI providers`},annotationConfigs:{href:ya.annotationConfigs,label:`annotation configs`},apiKeys:{href:ya.apiKeys,label:`API keys`},customAiProviders:{href:ya.customAiProviders,label:`custom AI providers`},dataRetention:{href:ya.dataRetention,label:`data retention`},datasetLabels:{href:ya.datasetLabels,label:`dataset labels`},defaultRetentionPolicy:{href:ya.dataRetention,label:`the default retention policy`},modelPricing:{href:ya.modelCostTracking,label:`model pricing`},promptLabels:{href:ya.promptLabels,label:`prompt labels`},pxi:{href:ya.pxi,label:`PXI`},sandboxConfigurations:{href:ya.sandboxes,label:`sandbox configurations`},sandboxProviders:{href:ya.sandboxes,label:`sandbox providers`},secrets:{href:ya.secrets,label:`secrets`},userAccess:{href:ya.accessControl,label:`user access`}},xa=e=>{switch(e){case`info`:return U(Vn,{});default:return U(St,{})}},Sa=G`
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
`,Ca=e=>{let t=(0,X.c)(22),n,r,i,a,o;t[0]===e?(n=t[1],r=t[2],i=t[3],a=t[4],o=t[5]):({children:n,href:r,triggerAriaLabel:i,variant:a,...o}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a,t[5]=o);let s=i===void 0?`More information`:i,c=a===void 0?`help`:a,l;t[6]===c?l=t[7]:(l=xa(c),t[6]=c,t[7]=l);let u;t[8]===l?u=t[9]:(u=U(H,{svg:l}),t[8]=l,t[9]=u);let d;t[10]!==u||t[11]!==s?(d={"aria-label":s,css:Sa,leadingVisual:u,size:`S`,variant:`quiet`},t[10]=u,t[11]=s,t[12]=d):d=t[12];let f=d,p;t[13]!==r||t[14]!==f?(p=r?U(we,{children:U(wt,{...f,href:r})}):U(Mt,{...f}),t[13]=r,t[14]=f,t[15]=p):p=t[15];let m;t[16]!==n||t[17]!==o?(m=U(oa,{...o,children:n}),t[16]=n,t[17]=o,t[18]=m):m=t[18];let h;return t[19]!==p||t[20]!==m?(h=W(ve,{delay:0,children:[p,m]}),t[19]=p,t[20]=m,t[21]=h):h=t[21],h},wa=G`
  margin-top: var(--global-dimension-size-100);
`;function Ta(e){let t=(0,X.c)(9),{children:n,topic:r}=e,{href:i,label:a}=ba[r],o=`Learn more about ${a}`,s;t[0]===n?s=t[1]:(s=U(B,{size:`S`,children:n}),t[0]=n,t[1]=s);let c;t[2]===i?c=t[3]:(c=U(`footer`,{css:wa,children:U(Yi,{href:i,children:`View documentation`})}),t[2]=i,t[3]=c);let l;return t[4]!==i||t[5]!==o||t[6]!==s||t[7]!==c?(l=W(Ca,{href:i,variant:`info`,triggerAriaLabel:o,children:[s,c]}),t[4]=i,t[5]=o,t[6]=s,t[7]=c,t[8]=l):l=t[8],l}function Ea(e){let t=(0,X.c)(8),n,r;t[0]===e?(n=t[1],r=t[2]):({children:n,...r}=e,t[0]=e,t[1]=n,t[2]=r);let i;t[3]===n?i=t[4]:(i=U(`div`,{role:`button`,children:n}),t[3]=n,t[4]=i);let a;return t[5]!==r||t[6]!==i?(a=U(we,{...r,children:i}),t[5]=r,t[6]=i,t[7]=a):a=t[7],a}function Da(e){let t=(0,X.c)(16),n,r,i,a,o,s;if(t[0]!==e){let{ref:c,...l}=e,{children:u,css:d,width:f,...p}=l;r=u,s=f,n=A,i=p,a=c,o=G(aa,d),t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a,t[5]=o,t[6]=s}else n=t[1],r=t[2],i=t[3],a=t[4],o=t[5],s=t[6];let c;t[7]===s?c=t[8]:(c=s?{width:s}:{maxWidth:`300px`},t[7]=s,t[8]=c);let l;return t[9]!==n||t[10]!==r||t[11]!==i||t[12]!==a||t[13]!==o||t[14]!==c?(l=U(n,{...i,ref:a,css:o,style:c,children:r}),t[9]=n,t[10]=r,t[11]=i,t[12]=a,t[13]=o,t[14]=c,t[15]=l):l=t[15],l}function Oa(e){let t=(0,X.c)(3),{children:n}=e,r;t[0]===Symbol.for(`react.memo_cache_sentinel`)?(r=G`
        margin-bottom: var(--global-dimension-size-100);
      `,t[0]=r):r=t[0];let i;return t[1]===n?i=t[2]:(i=U(rt,{level:4,css:r,children:n}),t[1]=n,t[2]=i),i}function ka(e){let t=(0,X.c)(3),{children:n}=e,r;t[0]===Symbol.for(`react.memo_cache_sentinel`)?(r=G`
        margin-bottom: var(--global-dimension-size-100);
      `,t[0]=r):r=t[0];let i;return t[1]===n?i=t[2]:(i=U(B,{size:`S`,color:`text-700`,css:r,children:n}),t[1]=n,t[2]=i),i}function Aa(e){let t=(0,X.c)(2),{children:n}=e,r;return t[0]===n?r=t[1]:(r=U(ra,{paddingTop:`size-50`,children:n}),t[0]=n,t[1]=r),r}var ja=2e3,Ma=G`
  flex: none;
  box-sizing: content-box;
`;function Na(e){let t=(0,X.c)(20),n,r,i,a;t[0]===e?(n=t[1],r=t[2],i=t[3],a=t[4]):({text:a,size:r,tooltipText:i,...n}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a);let o=r===void 0?`S`:r,s=i===void 0?`Copy`:i,[c,l]=(0,Y.useState)(!1),u;t[5]===a?u=t[6]:(u=()=>{let e=typeof a==`string`?a:a.current||``;Fe(e),l(!0),setTimeout(()=>{l(!1)},ja)},t[5]=a,t[6]=u);let d=u,f=c?`success`:`inherit`,p=c?`Checkmark`:`Duplicate`,m;t[7]!==f||t[8]!==p?(m=U(H,{color:f,svgKey:p}),t[7]=f,t[8]=p,t[9]=m):m=t[9];let h;t[10]!==d||t[11]!==n||t[12]!==o||t[13]!==m?(h=U(Mt,{size:o,leadingVisual:m,onPress:d,...n,className:`copy-button`}),t[10]=d,t[11]=n,t[12]=o,t[13]=m,t[14]=h):h=t[14];let g;t[15]===s?g=t[16]:(g=U(oa,{offset:1,children:s}),t[15]=s,t[16]=g);let _;return t[17]!==h||t[18]!==g?(_=U(`div`,{className:`copy-to-clipboard-button`,css:Ma,children:W(ve,{children:[h,g]})}),t[17]=h,t[18]=g,t[19]=_):_=t[19],_}var Pa=G`
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
`,Fa=ht,Ia=e=>{let t=(0,X.c)(10),n,r,i;t[0]===e?(n=t[1],r=t[2],i=t[3]):({className:n,onKeyDown:r,...i}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i);let a;t[4]===n?a=t[5]:(a=z(`react-aria-Menu`,n),t[4]=n,t[5]=a);let o;return t[6]!==r||t[7]!==i||t[8]!==a?(o=U(rn,{className:a,css:Pa,...i,onKeyDown:r}),t[6]=r,t[7]=i,t[8]=a,t[9]=o):o=t[9],o},La=G`
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
`,Ra=e=>{let t=(0,X.c)(18),n,r,i,a,o;t[0]===e?(n=t[1],r=t[2],i=t[3],a=t[4],o=t[5]):({className:n,trailingContent:o,leadingContent:r,ref:a,...i}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a,t[5]=o);let s=i.textValue||(typeof i.children==`string`?i.children:void 0),c;t[6]===n?c=t[7]:(c=z(`react-aria-MenuItem`,n),t[6]=n,t[7]=c);let l;t[8]!==r||t[9]!==i||t[10]!==o?(l=e=>{let{hasSubmenu:t,isSelected:n,selectionMode:a}=e;return W(V,{children:[n&&U(H,{svg:U(_n,{})}),a!==`none`&&!n&&U(H,{svg:U(_n,{}),css:G`
                  visibility: hidden;
                `}),U(za,{trailingContent:o,leadingContent:r,children:typeof i.children==`function`?i.children(e):i.children}),t&&U(H,{svg:U(Qn,{})})]})},t[8]=r,t[9]=i,t[10]=o,t[11]=l):l=t[11];let u;return t[12]!==i||t[13]!==a||t[14]!==c||t[15]!==l||t[16]!==s?(u=U(nn,{ref:a,...i,css:La,className:c,textValue:s,children:l}),t[12]=i,t[13]=a,t[14]=c,t[15]=l,t[16]=s,t[17]=u):u=t[17],u},za=e=>{let t=(0,X.c)(7),{children:n,trailingContent:r,leadingContent:i}=e,a;t[0]===Symbol.for(`react.memo_cache_sentinel`)?(a=G`
        padding: var(--global-menu-item-gap);
      `,t[0]=a):a=t[0];let o;t[1]!==n||t[2]!==i?(o=i?W(K,{alignItems:`center`,gap:`var(--global-menu-item-content-gap)`,children:[i,` `,n]}):n,t[1]=n,t[2]=i,t[3]=o):o=t[3];let s;return t[4]!==o||t[5]!==r?(s=W(K,{direction:`row`,alignItems:`center`,justifyContent:`space-between`,gap:`var(--global-menu-split-item-content-gap)`,minWidth:0,flex:1,css:a,children:[o,r]}),t[4]=o,t[5]=r,t[6]=s):s=t[6],s},Ba=G`
  overflow-y: hidden;
  display: flex;
  flex-direction: column;
`,Va=e=>{let t=(0,X.c)(19),n,r,i,a,o,s;t[0]===e?(n=t[1],r=t[2],i=t[3],a=t[4],o=t[5],s=t[6]):({children:n,placement:i,minHeight:a,maxHeight:o,maxWidth:s,...r}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a,t[5]=o,t[6]=s);let c=i===void 0?`bottom end`:i,l=a===void 0?`var(--global-menu-min-height)`:a,u=o===void 0?`var(--global-menu-max-height-large)`:o,d=s===void 0?450:s,f;t[7]!==u||t[8]!==d||t[9]!==l?(f={minHeight:l,maxHeight:u,maxWidth:d},t[7]=u,t[8]=d,t[9]=l,t[10]=f):f=t[10];let p;t[11]===Symbol.for(`react.memo_cache_sentinel`)?(p=G`
          display: flex;
          flex-direction: column;
          height: 100%;
          min-width: 300px;
        `,t[11]=p):p=t[11];let m;t[12]!==n||t[13]!==f?(m=U(`div`,{style:f,css:p,children:n}),t[12]=n,t[13]=f,t[14]=m):m=t[14];let h;return t[15]!==c||t[16]!==r||t[17]!==m?(h=U($n,{shouldFlip:!1,placement:c,css:Ba,...r,children:m}),t[15]=c,t[16]=r,t[17]=m,t[18]=h):h=t[18],h},Ha=G`
  padding: var(--global-dimension-size-50) var(--global-dimension-size-100) 0;
`,Ua=e=>{let t=(0,X.c)(5),{title:n,trailingContent:r}=e,i;t[0]===n?i=t[1]:(i=U(B,{weight:`heavy`,children:n}),t[0]=n,t[1]=i);let a;return t[2]!==i||t[3]!==r?(a=U(Tt,{css:Ha,children:W(K,{justifyContent:`space-between`,alignItems:`center`,children:[i,r]})}),t[2]=i,t[3]=r,t[4]=a):a=t[4],a},Wa=e=>{let t=(0,X.c)(3),{children:n}=e,r;t[0]===Symbol.for(`react.memo_cache_sentinel`)?(r=G`
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
      `,t[0]=r):r=t[0];let i;return t[1]===n?i=t[2]:(i=U(`div`,{className:`menu-header`,css:r,children:n}),t[1]=n,t[2]=i),i},Ga=e=>{let t=(0,X.c)(8),{children:n,leadingContent:r,trailingContent:i}=e,a;t[0]===Symbol.for(`react.memo_cache_sentinel`)?(a=G`
        padding: var(--global-dimension-size-100);
        border-bottom: 1px solid var(--global-menu-border-color);
      `,t[0]=a):a=t[0];let o;t[1]===Symbol.for(`react.memo_cache_sentinel`)?(o=G`
          flex: 1 1 auto;
          width: 100%;
          padding-left: var(--global-dimension-size-50);
        `,t[1]=o):o=t[1];let s;t[2]===n?s=t[3]:(s=U(rt,{level:4,weight:`heavy`,css:o,children:n}),t[2]=n,t[3]=s);let c;return t[4]!==r||t[5]!==s||t[6]!==i?(c=W(K,{direction:`row`,gap:`size-50`,alignItems:`center`,wrap:`nowrap`,minHeight:30,"data-testid":`menu-header-title`,css:a,children:[r,s,i]}),t[4]=r,t[5]=s,t[6]=i,t[7]=c):c=t[7],c},Ka=e=>{let t=(0,X.c)(3),{children:n}=e,r;t[0]===Symbol.for(`react.memo_cache_sentinel`)?(r=G`
        padding: var(--global-dimension-size-100);
        border-top: 1px solid var(--global-menu-border-color);
        display: flex;
        flex-direction: column;
        flex-shrink: 0;
        gap: var(--global-dimension-size-50);
      `,t[0]=r):r=t[0];let i;return t[1]===n?i=t[2]:(i=U(`div`,{css:r,children:n}),t[1]=n,t[2]=i),i},qa=e=>{let t=(0,X.c)(3),{children:n}=e,r;t[0]===Symbol.for(`react.memo_cache_sentinel`)?(r=G`
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
      `,t[0]=r):r=t[0];let i;return t[1]===n?i=t[2]:(i=U(B,{color:`gray-400`,fontStyle:`italic`,css:r,children:n}),t[1]=n,t[2]=i),i},Ja=G`
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
`;function Ya(e){let t=(0,X.c)(10),n,r,i;t[0]===e?(n=t[1],r=t[2],i=t[3]):({ref:i,css:n,...r}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i);let a;t[4]===n?a=t[5]:(a=G(Ja,n),t[4]=n,t[5]=a);let o;return t[6]!==r||t[7]!==i||t[8]!==a?(o=U(Mt,{ref:i,css:a,...r}),t[6]=r,t[7]=i,t[8]=a,t[9]=o):o=t[9],o}function Xa(e){let t=(0,X.c)(5),{children:n,isPlaceholder:r}=e,i=r&&`menu-button__value--placeholder`,a;t[0]===i?a=t[1]:(a=z(`menu-button__value`,i),t[0]=i,t[1]=a);let o;return t[2]!==n||t[3]!==a?(o=U(`span`,{className:a,children:n}),t[2]=n,t[3]=a,t[4]=o):o=t[4],o}var Za=2e3;function Qa(e){let t=(0,X.c)(18),{items:n}=e,[r,i]=(0,Y.useState)(null),a=(0,Y.useRef)(null),o;t[0]===n?o=t[1]:(o=e=>{let t=n.find(t=>t.name===e);t&&(Fe(t.value),i(t.name),a.current&&clearTimeout(a.current),a.current=setTimeout(()=>{i(null)},Za))},t[0]=n,t[1]=o);let s=o,c=r==null?`Duplicate`:`Checkmark`,l=r==null?`inherit`:`success`,u;t[2]!==c||t[3]!==l?(u=U(H,{svgKey:c,color:l}),t[2]=c,t[3]=l,t[4]=u):u=t[4];let d=r!=null||void 0,f=r==null?void 0:`Copied`,p;t[5]!==u||t[6]!==d||t[7]!==f?(p=U(Mt,{size:`S`,variant:`quiet`,"aria-label":`Copy`,leadingVisual:u,className:`copy-action-menu__button`,"data-copied":d,children:f}),t[5]=u,t[6]=d,t[7]=f,t[8]=p):p=t[8];let m;t[9]===Symbol.for(`react.memo_cache_sentinel`)?(m=G`
            --menu-min-width: auto;
          `,t[9]=m):m=t[9];let h;t[10]===n?h=t[11]:(h=n.map($a),t[10]=n,t[11]=h);let g;t[12]!==s||t[13]!==h?(g=U($n,{placement:`bottom end`,offset:3,children:U(Ia,{onAction:s,css:m,children:h})}),t[12]=s,t[13]=h,t[14]=g):g=t[14];let _;return t[15]!==p||t[16]!==g?(_=W(Fa,{children:[p,g]}),t[15]=p,t[16]=g,t[17]=_):_=t[17],_}function $a(e){return U(Ra,{id:e.name,textValue:`Copy ${e.name}`,leadingContent:U(H,{svgKey:e.iconKey??`Duplicate`}),children:e.name},e.name)}var eo=G`
  --embedded-copy-button-size: calc(
    var(--global-input-height-m) - 2 * var(--global-dimension-size-125) +
      var(--global-dimension-size-50)
  );
`,to=G`
  ${eo}
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
`,no=e=>{let t=(0,X.c)(6),{children:n,bordered:r}=e,i=r===void 0||r,a;t[0]===Symbol.for(`react.memo_cache_sentinel`)?(a=G`
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
      `,t[0]=a):a=t[0];let o;t[1]===n?o=t[2]:(o=U(rt,{children:n}),t[1]=n,t[2]=o);let s;return t[3]!==i||t[4]!==o?(s=U(`div`,{"data-bordered":i,css:a,children:o}),t[3]=i,t[4]=o,t[5]=s):s=t[5],s},ro=[/Unexpected token ['"]?<['"]?/i,/JSON\.parse.*unexpected character/i,/<!DOCTYPE/i,/timeout/i,/502|504|gateway/i];function io(e){if(e==null)return!1;let t=e instanceof Error?e.message:e;return typeof t!=`string`||t.length===0?!1:ro.some(e=>e.test(t))}function ao(e){let t=(0,X.c)(9),{error:n}=e;if(io(n)){let e;return t[0]===n?e=t[1]:(e=U(oo,{error:n}),t[0]=n,t[1]=e),e}let r,i;t[2]===Symbol.for(`react.memo_cache_sentinel`)?(r=U(K,{direction:`column`,width:`100%`,alignItems:`center`,children:U(`h1`,{children:`Something went wrong`})}),i=U(`p`,{children:`We strive to do our very best but 🐛 bugs happen. It would mean a lot to us if you could file a an issue. If you feel comfortable, please include the error details below in your issue. We will get back to you as soon as we can.`}),t[2]=r,t[3]=i):(r=t[2],i=t[3]);let a;t[4]===Symbol.for(`react.memo_cache_sentinel`)?(a=U(K,{direction:`row`,width:`100%`,justifyContent:`end`,children:U(Yi,{href:`https://github.com/Arize-ai/phoenix/issues/new?assignees=&labels=bug&template=bug_report.md&title=%5BBUG%5D`,children:`file an issue with us`})}),t[4]=a):a=t[4];let o,s;t[5]===Symbol.for(`react.memo_cache_sentinel`)?(o=U(`summary`,{children:`error details`}),s=G`
              white-space: pre-wrap;
              overflow-wrap: break-word;
              overflow: hidden;
              overflow-y: auto;
              max-height: 500px;
            `,t[5]=o,t[6]=s):(o=t[5],s=t[6]);let c;return t[7]===n?c=t[8]:(c=U(ra,{padding:`size-200`,children:W(K,{direction:`column`,children:[r,i,a,W(`details`,{open:!0,children:[o,U(`pre`,{css:s,children:n})]})]})}),t[7]=n,t[8]=c),c}function oo(e){let t=(0,X.c)(9),{error:n}=e,r,i,a,o;t[0]===Symbol.for(`react.memo_cache_sentinel`)?(r=U(K,{direction:`column`,width:`100%`,alignItems:`center`,children:U(`h1`,{children:`Connection timed out`})}),i=U(`p`,{children:`The connection to the Phoenix server timed out before a response was received. This typically happens when a load balancer or proxy closes the connection before the server can respond.`}),a=U(`p`,{children:`Possible solutions:`}),o=W(`ul`,{css:G`
            margin: var(--global-dimension-size-100) 0;
            padding-left: var(--global-dimension-size-300);
          `,children:[U(`li`,{children:`Increase your load balancer or proxy timeout settings`}),U(`li`,{children:`Check if the Phoenix server is overloaded or slow to respond`}),U(`li`,{children:`Verify network connectivity between components`})]}),t[0]=r,t[1]=i,t[2]=a,t[3]=o):(r=t[0],i=t[1],a=t[2],o=t[3]);let s;t[4]===Symbol.for(`react.memo_cache_sentinel`)?(s=U(K,{direction:`row`,width:`100%`,justifyContent:`end`,children:U(Mt,{variant:`primary`,size:`S`,onPress:so,children:`Retry`})}),t[4]=s):s=t[4];let c;t[5]===n?c=t[6]:(c=n&&W(`details`,{children:[U(`summary`,{children:`error details`}),U(`pre`,{css:G`
                white-space: pre-wrap;
                overflow-wrap: break-word;
                overflow: hidden;
                overflow-y: auto;
                max-height: 500px;
              `,children:n})]}),t[5]=n,t[6]=c);let l;return t[7]===c?l=t[8]:(l=U(ra,{padding:`size-200`,children:W(K,{direction:`column`,children:[r,i,a,o,s,c]})}),t[7]=c,t[8]=l),l}function so(){window.location.reload()}var co=class extends Y.Component{constructor(e){super(e),this.state={hasError:!1,error:null}}static getDerivedStateFromError(e){return{hasError:!0,error:e}}componentDidCatch(e,t){console.error(`ErrorBoundary caught error:`,e,t)}render(){if(this.state.hasError){let e=this.state.error instanceof Error?this.state.error.message:null;return typeof this.props.fallback==`function`?U(this.props.fallback,{error:e}):U(ao,{error:e})}return this.props.children}};function lo({error:e}){let t=W(`div`,{css:G`
        text-align: center;
        display: inline-flex;
        align-items: center;
        color: var(--global-text-color-300);
        gap: var(--global-dimension-size-50);
        cursor: ${e?`help`:`default`};
      `,children:[U(H,{svg:U(_t,{})}),U(B,{color:`text-300`,children:`error`})]});return e?W(ve,{delay:200,children:[U(`span`,{tabIndex:0,children:t}),U(A,{offset:6,children:U(ra,{padding:`size-100`,borderColor:`default`,borderWidth:`thin`,borderRadius:`small`,backgroundColor:`gray-200`,maxWidth:`size-4600`,children:U(`pre`,{css:G`
              white-space: pre-wrap;
              overflow-wrap: break-word;
              margin: 0;
              font-size: var(--global-font-size-xs, 12px);
            `,children:e})})})]}):t}var uo=G`
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
`,fo=G`
  background-color: transparent;
  color: var(--ac-global-text-color-500);
  padding: 0 var(--global-dimension-size-75);
  font-size: var(--global-dimension-font-size-50);
  border-radius: var(--global-rounding-small);
  border: 1px solid var(--ac-global-border-color-default);
  text-transform: uppercase;
`;function po(e){let t=(0,X.c)(10),n,r,i,a;t[0]===e?(n=t[1],r=t[2],i=t[3],a=t[4]):({ref:i,children:n,variant:a,...r}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a);let o=(a===void 0?`default`:a)===`quiet`?fo:uo,s;return t[5]!==n||t[6]!==r||t[7]!==i||t[8]!==o?(s=U(zt,{ref:i,css:o,...r,children:n}),t[5]=n,t[6]=r,t[7]=i,t[8]=o,t[9]=s):s=t[9],s}function mo({ref:e,color:t,size:n=`M`,shape:r=`square`}){let i=typeof t==`string`&&t.startsWith(`var`),a=i?G`
        background-color: ${t} !important;
      `:void 0;return U(f,{color:i?void 0:t,"data-shape":r,"data-size":n,ref:e,css:G(G`
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
        `,a)})}mo.displayName=`ColorSwatch`;var ho=G`
  opacity: 0.8;
  color: var(--global-text-color-500);
  .theme--dark & {
    color: var(--global-text-color-400);
  }
  .text {
    color: inherit;
  }
`,go=G`
  margin: var(--global-dimension-size-300);
  display: flex;
  flex-direction: column;
  align-items: center;
`;function _o(e){let t=(0,X.c)(7),{message:n,size:r}=e,i=r===void 0?`M`:r,a,o;t[0]===Symbol.for(`react.memo_cache_sentinel`)?(a=G`
        width: 100%;
        display: flex;
        justify-content: center;
      `,o=[go,ho],t[0]=a,t[1]=o):(a=t[0],o=t[1]);let s;t[2]!==n||t[3]!==i?(s=n&&U(B,{size:i,children:n}),t[2]=n,t[3]=i,t[4]=s):s=t[4];let c;return t[5]===s?c=t[6]:(c=U(`div`,{css:a,children:U(`div`,{css:o,children:s})}),t[5]=s,t[6]=c),c}var vo=G`
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
`;function yo(){let e=(0,X.c)(2),t=(0,Y.useContext)(Nt),n=(0,Y.useContext)(u),r=t?.inputValue??n?.inputValue??``,i;return e[0]===r?i=e[1]:(i=r.trim(),e[0]=r,e[1]=i),i.length>0}function bo(e){let t=(0,X.c)(9),{icon:n,description:r,isFiltered:i}=e,a=yo(),o=i??a,s;t[0]===Symbol.for(`react.memo_cache_sentinel`)?(s=[vo,ho],t[0]=s):s=t[0];let c;t[1]!==n||t[2]!==o?(c=o?U(H,{svg:U(lt,{})}):n,t[1]=n,t[2]=o,t[3]=c):c=t[3];let l=o?`No results`:r,u;t[4]===l?u=t[5]:(u=U(B,{size:`S`,children:l}),t[4]=l,t[5]=u);let d;return t[6]!==c||t[7]!==u?(d=W(`div`,{css:s,children:[c,u]}),t[6]=c,t[7]=u,t[8]=d):d=t[8],d}var xo=G`
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
`,So=G`
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
`;function Co(e){let t=(0,X.c)(14),{icon:n,title:r,description:i,href:a,external:o}=e,s;t[0]===o?s=t[1]:(s=o?{target:`_blank`,rel:`noopener noreferrer`}:void 0,t[0]=o,t[1]=s);let c;t[2]===r?c=t[3]:(c=U(B,{weight:`heavy`,children:r}),t[2]=r,t[3]=c);let l;t[4]!==n||t[5]!==c?(l=W(K,{direction:`row`,gap:`size-100`,alignItems:`center`,children:[n,c]}),t[4]=n,t[5]=c,t[6]=l):l=t[6];let u;t[7]===i?u=t[8]:(u=U(B,{size:`S`,color:`text-700`,css:So,children:i}),t[7]=i,t[8]=u);let d;return t[9]!==a||t[10]!==s||t[11]!==l||t[12]!==u?(d=W(`a`,{href:a,css:xo,...s,children:[l,u]}),t[9]=a,t[10]=s,t[11]=l,t[12]=u,t[13]=d):d=t[13],d}function wo(e,t,n){return n==null?!1:e===`horizontal`||e!==`vertical`&&t?.type===`cards`&&(t.columns??1)===2&&t.items.length>=3}var To=G`
  max-width: var(--global-dimension-size-4000);
  text-align: center;
  text-wrap: balance;
`,Eo=G`
  display: grid;
  gap: var(--global-dimension-size-200);
  width: min(100%, var(--global-dimension-size-4000));
`,Do=G`
  width: min(100%, calc(var(--global-dimension-size-4000) * 2));
  grid-template-columns: repeat(
    auto-fit,
    minmax(min(100%, var(--global-dimension-size-4000)), 1fr)
  );
`;function Oo(e){let t=(0,X.c)(14),{action:n}=e;if(n.type===`strip`){let e;t[0]===n.items?e=t[1]:(e=n.items.map(Ao),t[0]=n.items,t[1]=e);let r;return t[2]===e?r=t[3]:(r=U(K,{direction:`row`,gap:`size-100`,wrap:!0,alignItems:`center`,children:e}),t[2]=e,t[3]=r),r}let r=n.columns??1,i=r===2&&Do,a;t[4]===r?a=t[5]:(a=r===1&&G`
            grid-template-columns: 1fr;
          `,t[4]=r,t[5]=a);let o;t[6]!==i||t[7]!==a?(o=[Eo,i,a],t[6]=i,t[7]=a,t[8]=o):o=t[8];let s;t[9]===n.items?s=t[10]:(s=n.items.map(ko),t[9]=n.items,t[10]=s);let c;return t[11]!==o||t[12]!==s?(c=U(`div`,{css:o,children:s}),t[11]=o,t[12]=s,t[13]=c):c=t[13],c}function ko(e,t){return U(Co,{...e},t)}function Ao(e,t){if(e.kind===`link`)return U(wt,{href:e.href,variant:`quiet`,size:`S`,children:e.label},t);if(e.kind===`node`)return U(Y.Fragment,{children:e.node},t);let{kind:n,...r}=e;return U(Mt,{size:`S`,...r},t)}function jo(e){let t=(0,X.c)(23),{graphic:n,title:r,description:i,action:a,orientation:o}=e,s=wo(o===void 0?`auto`:o,a,n),c=a?.type===`cards`?`size-300`:`size-200`,l=a?.type===`cards`?`size-500`:`size-200`,u;t[0]!==i||t[1]!==r?(u=r!=null||i!=null?W(K,{direction:`column`,gap:`size-25`,alignItems:`center`,children:[r!=null&&U(B,{size:`L`,weight:`heavy`,children:r}),i!=null&&U(B,{size:`S`,color:`text-700`,css:To,children:i})]}):null,t[0]=i,t[1]=r,t[2]=u):u=t[2];let d=u;if(s){let e;t[3]===n?e=t[4]:(e=U(K,{alignItems:`center`,justifyContent:`center`,children:n}),t[3]=n,t[4]=e);let r;t[5]!==e||t[6]!==d?(r=W(K,{direction:`row`,wrap:!0,gap:`size-400`,alignItems:`center`,justifyContent:`center`,children:[e,d]}),t[5]=e,t[6]=d,t[7]=r):r=t[7];let i;t[8]===a?i=t[9]:(i=a!=null&&U(Oo,{action:a}),t[8]=a,t[9]=i);let o;return t[10]!==l||t[11]!==r||t[12]!==i?(o=W(K,{direction:`column`,gap:l,alignItems:`center`,children:[r,i]}),t[10]=l,t[11]=r,t[12]=i,t[13]=o):o=t[13],o}let f=n!=null&&n,p;t[14]===a?p=t[15]:(p=a!=null&&U(Oo,{action:a}),t[14]=a,t[15]=p);let m;t[16]!==c||t[17]!==p||t[18]!==d?(m=W(K,{direction:`column`,gap:c,alignItems:`center`,children:[d,p]}),t[16]=c,t[17]=p,t[18]=d,t[19]=m):m=t[19];let h;return t[20]!==f||t[21]!==m?(h=W(K,{direction:`column`,gap:`size-300`,alignItems:`center`,justifyContent:`center`,children:[f,m]}),t[20]=f,t[21]=m,t[22]=h):h=t[22],h}var Mo=G`
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
`,No=G`
  flex: 0 1 var(--global-dimension-size-2000);
  min-height: var(--global-dimension-size-750);
`;function Po(e){let t=(0,X.c)(3),{children:n}=e,r;t[0]===Symbol.for(`react.memo_cache_sentinel`)?(r=U(`div`,{css:No,"aria-hidden":`true`}),t[0]=r):r=t[0];let i;return t[1]===n?i=t[2]:(i=W(`div`,{css:Mo,children:[r,n]}),t[1]=n,t[2]=i),i}var Fo={size:`small`,icon:U(H,{svg:U(st,{})})},Io={genericAdd:{size:`small`,icon:U(H,{svg:U(Ot,{})})},genericEdit:{size:`small`,icon:U(H,{svg:U(It,{})})},trace:{size:`large`,icon:U(H,{svg:U(dn,{})})},dataset:{size:`large`,icon:U(H,{svg:U(kt,{})})},evaluator:{size:`large`,icon:U(H,{svg:U(Jt,{})})},session:{size:`large`,icon:U(H,{svg:U(Rt,{})})},experiment:{size:`large`,icon:U(H,{svg:U(Gt,{})})},prompt:{size:`large`,icon:U(H,{svg:U(Wn,{})})},project:{size:`large`,icon:U(H,{svg:U(gt,{})})},annotation:{size:`small`,icon:U(H,{svg:U(Hn,{})})},customAIProvider:{size:`small`,icon:U(H,{svg:U(pn,{})})},event:{size:`small`,icon:U(H,{svg:U(Fn,{})})},attribute:{size:`small`,icon:U(H,{svg:U(Vn,{})})},config:{size:`small`,icon:U(H,{svg:U(Pn,{})})},credential:{size:`small`,icon:U(H,{svg:U(Tn,{})})},version:{size:`small`,icon:U(H,{svg:U(en,{})})},tag:Fo,label:Fo,split:Fo};Object.keys(Io),Object.fromEntries(Object.entries(Io).map(([e,t])=>[e,t.size]));var Lo=G`
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
`,Ro=(e,t)=>{let n=`linear-gradient(
    to bottom,
    transparent 0,
    #000 ${e},
    #000 calc(100% - ${t}),
    transparent 100%
  )`;return G`
    -webkit-mask-image: ${n};
    mask-image: ${n};
  `},zo=G`
  display: block;
  margin-bottom: calc(-1 * var(--global-dimension-size-200));
`,Bo=e=>G`
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
`;function Vo(e){let t=(0,X.c)(14),{id:n,x:r,y:i,width:a,height:o}=e,s,c,l,u,d,f,p,m;t[0]===Symbol.for(`react.memo_cache_sentinel`)?(s=U(`feFlood`,{floodOpacity:`0`,result:`BackgroundImageFix`}),c=U(`feColorMatrix`,{in:`SourceAlpha`,type:`matrix`,values:`0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 127 0`,result:`hardAlpha`}),l=U(`feOffset`,{dy:`4`}),u=U(`feGaussianBlur`,{stdDeviation:`6`}),d=U(`feComposite`,{in2:`hardAlpha`,operator:`out`}),f=U(`feColorMatrix`,{type:`matrix`,values:`0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0.19 0`}),p=U(`feBlend`,{mode:`normal`,in2:`BackgroundImageFix`,result:`effect1_dropShadow`}),m=U(`feBlend`,{mode:`normal`,in:`SourceGraphic`,in2:`effect1_dropShadow`,result:`shape`}),t[0]=s,t[1]=c,t[2]=l,t[3]=u,t[4]=d,t[5]=f,t[6]=p,t[7]=m):(s=t[0],c=t[1],l=t[2],u=t[3],d=t[4],f=t[5],p=t[6],m=t[7]);let h;return t[8]!==o||t[9]!==n||t[10]!==a||t[11]!==r||t[12]!==i?(h=W(`filter`,{id:n,x:r,y:i,width:a,height:o,filterUnits:`userSpaceOnUse`,colorInterpolationFilters:`sRGB`,children:[s,c,l,u,d,f,p,m]}),t[8]=o,t[9]=n,t[10]=a,t[11]=r,t[12]=i,t[13]=h):h=t[13],h}function Ho(e){let t=(0,X.c)(10),{x:n,y:r,size:i,icon:a}=e,o;t[0]===i?o=t[1]:(o=Bo(i),t[0]=i,t[1]=o);let s;t[2]!==a||t[3]!==o?(s=U(`div`,{css:o,children:a}),t[2]=a,t[3]=o,t[4]=s):s=t[4];let c;return t[5]!==i||t[6]!==s||t[7]!==n||t[8]!==r?(c=U(`foreignObject`,{x:n,y:r,width:i,height:i,children:s}),t[5]=i,t[6]=s,t[7]=n,t[8]=r,t[9]=c):c=t[9],c}function Uo(e){let t=(0,X.c)(35),{icon:n,ids:r}=e,i;t[0]===Symbol.for(`react.memo_cache_sentinel`)?(i=[Lo,Ro(`34%`,`34%`),zo],t[0]=i):i=t[0];let a=`url(#${r.f0})`,o,s,c;t[1]===Symbol.for(`react.memo_cache_sentinel`)?(o=U(`rect`,{x:`19`,y:`10`,width:`160`,height:`32`,rx:`8`,fill:`var(--esg-card-bg)`,shapeRendering:`crispEdges`}),s=U(`rect`,{x:`19.5`,y:`10.5`,width:`159`,height:`31`,rx:`7.5`,stroke:`var(--esg-stroke)`,shapeRendering:`crispEdges`}),c=U(`rect`,{opacity:`0.68`,x:`31`,y:`22`,width:`136`,height:`8`,rx:`3`,fill:`var(--esg-bar)`}),t[1]=o,t[2]=s,t[3]=c):(o=t[1],s=t[2],c=t[3]);let l;t[4]===a?l=t[5]:(l=W(`g`,{filter:a,children:[o,s,c]}),t[4]=a,t[5]=l);let u=`url(#${r.f1})`,d,f;t[6]===Symbol.for(`react.memo_cache_sentinel`)?(d=U(`rect`,{x:`12`,y:`52`,width:`174`,height:`48`,rx:`8`,fill:`var(--esg-card-bg)`,shapeRendering:`crispEdges`}),f=U(`rect`,{x:`12.5`,y:`52.5`,width:`173`,height:`47`,rx:`7.5`,stroke:`var(--esg-stroke-subtle)`,shapeRendering:`crispEdges`}),t[6]=d,t[7]=f):(d=t[6],f=t[7]);let p;t[8]===n?p=t[9]:(p=U(Ho,{x:24,y:66,size:20,icon:n}),t[8]=n,t[9]=p);let m,h;t[10]===Symbol.for(`react.memo_cache_sentinel`)?(m=U(`rect`,{opacity:`0.68`,x:`56`,y:`65`,width:`120`,height:`8`,rx:`3`,fill:`var(--esg-bar)`}),h=U(`rect`,{opacity:`0.68`,x:`56`,y:`79`,width:`80`,height:`8`,rx:`3`,fill:`var(--esg-bar)`}),t[10]=m,t[11]=h):(m=t[10],h=t[11]);let g;t[12]!==p||t[13]!==u?(g=W(`g`,{filter:u,children:[d,f,p,m,h]}),t[12]=p,t[13]=u,t[14]=g):g=t[14];let _=`url(#${r.f2})`,v,y,b;t[15]===Symbol.for(`react.memo_cache_sentinel`)?(v=U(`rect`,{x:`19`,y:`110`,width:`160`,height:`32`,rx:`8`,fill:`var(--esg-card-bg)`,shapeRendering:`crispEdges`}),y=U(`rect`,{x:`19.5`,y:`110.5`,width:`159`,height:`31`,rx:`7.5`,stroke:`var(--esg-stroke)`,shapeRendering:`crispEdges`}),b=U(`rect`,{opacity:`0.68`,x:`31`,y:`122`,width:`136`,height:`8`,rx:`3`,fill:`var(--esg-bar)`}),t[15]=v,t[16]=y,t[17]=b):(v=t[15],y=t[16],b=t[17]);let x;t[18]===_?x=t[19]:(x=W(`g`,{filter:_,children:[v,y,b]}),t[18]=_,t[19]=x);let S;t[20]===r.f0?S=t[21]:(S=U(Vo,{id:r.f0,x:7,y:2,width:184,height:56}),t[20]=r.f0,t[21]=S);let C;t[22]===r.f1?C=t[23]:(C=U(Vo,{id:r.f1,x:0,y:44,width:198,height:72}),t[22]=r.f1,t[23]=C);let w;t[24]===r.f2?w=t[25]:(w=U(Vo,{id:r.f2,x:7,y:102,width:184,height:56}),t[24]=r.f2,t[25]=w);let T;t[26]!==S||t[27]!==C||t[28]!==w?(T=W(`defs`,{children:[S,C,w]}),t[26]=S,t[27]=C,t[28]=w,t[29]=T):T=t[29];let E;return t[30]!==g||t[31]!==x||t[32]!==T||t[33]!==l?(E=W(`svg`,{width:`198`,height:`158`,viewBox:`0 0 198 158`,fill:`none`,xmlns:`http://www.w3.org/2000/svg`,"aria-hidden":`true`,focusable:`false`,css:i,children:[l,g,x,T]}),t[30]=g,t[31]=x,t[32]=T,t[33]=l,t[34]=E):E=t[34],E}function Wo(e){let t=(0,X.c)(40),{icon:n,ids:r}=e,i;t[0]===Symbol.for(`react.memo_cache_sentinel`)?(i=[Lo,Ro(`38%`,`31%`),zo],t[0]=i):i=t[0];let a=`url(#${r.f0})`,o,s,c,l,u,d;t[1]===Symbol.for(`react.memo_cache_sentinel`)?(o=U(`rect`,{x:`12`,y:`8`,width:`174`,height:`32`,rx:`8`,fill:`var(--esg-card-bg)`,shapeRendering:`crispEdges`}),s=U(`rect`,{x:`12.5`,y:`8.5`,width:`173`,height:`31`,rx:`7.5`,stroke:`var(--esg-stroke)`,shapeRendering:`crispEdges`}),c=U(`path`,{d:`M27.75 22.5C28.5784 22.5 29.25 23.1716 29.25 24C29.25 24.8284 28.5784 25.5 27.75 25.5C26.9216 25.5 26.25 24.8284 26.25 24C26.25 23.1716 26.9216 22.5 27.75 22.5Z`,fill:`var(--esg-dots)`}),l=U(`path`,{d:`M33 22.5C33.8284 22.5 34.5 23.1716 34.5 24C34.5 24.8284 33.8284 25.5 33 25.5C32.1716 25.5 31.5 24.8284 31.5 24C31.5 23.1716 32.1716 22.5 33 22.5Z`,fill:`var(--esg-dots)`}),u=U(`path`,{d:`M38.25 22.5C39.0784 22.5 39.75 23.1716 39.75 24C39.75 24.8284 39.0784 25.5 38.25 25.5C37.4216 25.5 36.75 24.8284 36.75 24C36.75 23.1716 37.4216 22.5 38.25 22.5Z`,fill:`var(--esg-dots)`}),d=U(`rect`,{opacity:`0.68`,x:`54`,y:`20`,width:`120`,height:`8`,rx:`3`,fill:`var(--esg-bar)`}),t[1]=o,t[2]=s,t[3]=c,t[4]=l,t[5]=u,t[6]=d):(o=t[1],s=t[2],c=t[3],l=t[4],u=t[5],d=t[6]);let f;t[7]===a?f=t[8]:(f=W(`g`,{filter:a,children:[o,s,c,l,u,d]}),t[7]=a,t[8]=f);let p=`url(#${r.f1})`,m,h;t[9]===Symbol.for(`react.memo_cache_sentinel`)?(m=U(`rect`,{x:`12`,y:`50`,width:`174`,height:`32`,rx:`8`,fill:`var(--esg-card-bg)`,shapeRendering:`crispEdges`}),h=U(`rect`,{x:`12.5`,y:`50.5`,width:`173`,height:`31`,rx:`7.5`,stroke:`var(--esg-stroke-subtle)`,shapeRendering:`crispEdges`}),t[9]=m,t[10]=h):(m=t[9],h=t[10]);let g;t[11]===n?g=t[12]:(g=U(Ho,{x:25,y:58,size:16,icon:n}),t[11]=n,t[12]=g);let _;t[13]===Symbol.for(`react.memo_cache_sentinel`)?(_=U(`rect`,{opacity:`0.68`,x:`54`,y:`62`,width:`120`,height:`8`,rx:`3`,fill:`var(--esg-bar)`}),t[13]=_):_=t[13];let v;t[14]!==p||t[15]!==g?(v=W(`g`,{filter:p,children:[m,h,g,_]}),t[14]=p,t[15]=g,t[16]=v):v=t[16];let y=`url(#${r.f2})`,b,x,S,C,w,T;t[17]===Symbol.for(`react.memo_cache_sentinel`)?(b=U(`rect`,{x:`12`,y:`92`,width:`174`,height:`32`,rx:`8`,fill:`var(--esg-card-bg)`,shapeRendering:`crispEdges`}),x=U(`rect`,{x:`12.5`,y:`92.5`,width:`173`,height:`31`,rx:`7.5`,stroke:`var(--esg-stroke)`,shapeRendering:`crispEdges`}),S=U(`path`,{d:`M27.75 106.5C28.5784 106.5 29.25 107.172 29.25 108C29.25 108.828 28.5784 109.5 27.75 109.5C26.9216 109.5 26.25 108.828 26.25 108C26.25 107.172 26.9216 106.5 27.75 106.5Z`,fill:`var(--esg-dots)`}),C=U(`path`,{d:`M33 106.5C33.8284 106.5 34.5 107.172 34.5 108C34.5 108.828 33.8284 109.5 33 109.5C32.1716 109.5 31.5 108.828 31.5 108C31.5 107.172 32.1716 106.5 33 106.5Z`,fill:`var(--esg-dots)`}),w=U(`path`,{d:`M38.25 106.5C39.0784 106.5 39.75 107.172 39.75 108C39.75 108.828 39.0784 109.5 38.25 109.5C37.4216 109.5 36.75 108.828 36.75 108C36.75 107.172 37.4216 106.5 38.25 106.5Z`,fill:`var(--esg-dots)`}),T=U(`rect`,{opacity:`0.68`,x:`54`,y:`104`,width:`120`,height:`8`,rx:`3`,fill:`var(--esg-bar)`}),t[17]=b,t[18]=x,t[19]=S,t[20]=C,t[21]=w,t[22]=T):(b=t[17],x=t[18],S=t[19],C=t[20],w=t[21],T=t[22]);let E;t[23]===y?E=t[24]:(E=W(`g`,{filter:y,children:[b,x,S,C,w,T]}),t[23]=y,t[24]=E);let D;t[25]===r.f0?D=t[26]:(D=U(Vo,{id:r.f0,x:0,y:0,width:198,height:56}),t[25]=r.f0,t[26]=D);let O;t[27]===r.f1?O=t[28]:(O=U(Vo,{id:r.f1,x:0,y:42,width:198,height:56}),t[27]=r.f1,t[28]=O);let k;t[29]===r.f2?k=t[30]:(k=U(Vo,{id:r.f2,x:0,y:84,width:198,height:56}),t[29]=r.f2,t[30]=k);let A;t[31]!==D||t[32]!==O||t[33]!==k?(A=W(`defs`,{children:[D,O,k]}),t[31]=D,t[32]=O,t[33]=k,t[34]=A):A=t[34];let j;return t[35]!==v||t[36]!==E||t[37]!==A||t[38]!==f?(j=W(`svg`,{width:`198`,height:`140`,viewBox:`0 0 198 140`,fill:`none`,xmlns:`http://www.w3.org/2000/svg`,"aria-hidden":`true`,focusable:`false`,css:i,children:[f,v,E,A]}),t[35]=v,t[36]=E,t[37]=A,t[38]=f,t[39]=j):j=t[39],j}function Go(e){let t=(0,X.c)(8),{variant:n}=e,{size:r,icon:i}=Io[n===void 0?`genericAdd`:n],a=(0,Y.useId)(),o=`${a}-f0`,s=`${a}-f1`,c=`${a}-f2`,l;t[0]!==o||t[1]!==s||t[2]!==c?(l={f0:o,f1:s,f2:c},t[0]=o,t[1]=s,t[2]=c,t[3]=l):l=t[3];let u=l,d;return t[4]!==i||t[5]!==u||t[6]!==r?(d=U(r===`small`?Wo:Uo,{icon:i,ids:u}),t[4]=i,t[5]=u,t[6]=r,t[7]=d):d=t[7],d}function Ko(e){let t=(0,X.c)(2),{children:n}=e;if(typeof n==`string`){let e;return t[0]===n?e=t[1]:(e=U(rt,{level:1,children:n}),t[0]=n,t[1]=e),e}return n}function qo(e){let t=(0,X.c)(2),{children:n}=e;if(!n)return null;if(typeof n==`string`){let e;return t[0]===n?e=t[1]:(e=U(B,{size:`S`,color:`text-700`,children:n}),t[0]=n,t[1]=e),e}return n}function Jo(e){let t=(0,X.c)(10),{title:n,subTitle:r,extra:i}=e,a;t[0]===n?a=t[1]:(a=U(Ko,{children:n}),t[0]=n,t[1]=a);let o;t[2]===r?o=t[3]:(o=U(qo,{children:r}),t[2]=r,t[3]=o);let s;t[4]!==a||t[5]!==o?(s=W(K,{direction:`column`,gap:`size-50`,minWidth:0,children:[a,o]}),t[4]=a,t[5]=o,t[6]=s):s=t[6];let c;return t[7]!==i||t[8]!==s?(c=U(ra,{padding:`size-200`,flex:`none`,"data-testid":`page-header`,children:W(K,{direction:`row`,justifyContent:`space-between`,alignItems:`center`,"data-testid":`page-header-content`,gap:`size-100`,children:[s,i]})}),t[7]=i,t[8]=s,t[9]=c):c=t[9],c}var Yo=G`
  border-radius: 16px;
  padding: var(--global-dimension-size-50) var(--global-dimension-size-200) !important;
`,Xo=e=>{let t=(0,X.c)(10),{onLoadMore:n,isLoadingNext:r,buttonProps:i}=e,a;t[0]===n?a=t[1]:(a=()=>{n()},t[0]=n,t[1]=a);let o;t[2]===r?o=t[3]:(o=r?U(H,{svg:U(hn,{})}):void 0,t[2]=r,t[3]=o);let s=r?`Loading...`:`Load More`,c;return t[4]!==i||t[5]!==r||t[6]!==a||t[7]!==o||t[8]!==s?(c=U(Mt,{onPress:a,size:`S`,css:Yo,isDisabled:r,leadingVisual:o,...i,children:s}),t[4]=i,t[5]=r,t[6]=a,t[7]=o,t[8]=s,t[9]=c):c=t[9],c};function Zo(e,{filled:t}={filled:!0}){let n;switch(e){case`warning`:n=U(t?tn:mt,{});break;case`info`:n=U(t?cn:Vn,{});break;case`danger`:n=U(t?Nn:_t,{});break;case`success`:n=U(t?qn:an,{})}return U(H,{svg:n})}var Qo=G`
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
`,$o=G`
  display: flex;
  flex-direction: row;
  align-items: flex-start;
  flex: 1 1 auto;
`,es=G`
  background-color: transparent;
  color: inherit;
  padding: 0;
  border: none;
  cursor: pointer;
  width: 20px;
  height: 20px;
  margin-left: var(--global-dimension-size-200);
`,ts=e=>{let t=(0,X.c)(35),n,r,i,a,o,s,c,l,u,d;t[0]===e?(n=t[1],r=t[2],i=t[3],a=t[4],o=t[5],s=t[6],c=t[7],l=t[8],u=t[9],d=t[10]):({variant:d,title:u,icon:i,children:n,showIcon:s,dismissable:c,onDismissClick:a,banner:l,extra:r,...o}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a,t[5]=o,t[6]=s,t[7]=c,t[8]=l,t[9]=u,t[10]=d);let f=s===void 0||s,p=c!==void 0&&c,m=l!==void 0&&l,{theme:h}=Pr();if(!i&&f){let e;t[11]===d?e=t[12]:(e=Zo(d),t[11]=d,t[12]=e),i=e}let g=!!u,_;t[13]===u?_=t[14]:(_=u?U(B,{elementType:`h5`,size:`M`,weight:`heavy`,color:`inherit`,children:u}):null,t[13]=u,t[14]=_);let v;t[15]===n?v=t[16]:(v=U(B,{color:`inherit`,size:`S`,children:n}),t[15]=n,t[16]=v);let y;t[17]!==_||t[18]!==v?(y=W(`div`,{children:[_,v]}),t[17]=_,t[18]=v,t[19]=y):y=t[19];let b;t[20]!==i||t[21]!==y?(b=W(`div`,{css:$o,className:`alert__icon-title-wrap`,children:[i,y]}),t[20]=i,t[21]=y,t[22]=b):b=t[22];let x;t[23]!==p||t[24]!==a?(x=p?U(`button`,{css:es,onClick:a,children:U(H,{svg:U(Bt,{})})}):null,t[23]=p,t[24]=a,t[25]=x):x=t[25];let S;return t[26]!==m||t[27]!==r||t[28]!==o||t[29]!==g||t[30]!==b||t[31]!==x||t[32]!==h||t[33]!==d?(S=W(`div`,{...o,css:Qo,"data-variant":d,"data-banner":m,"data-has-title":g,"data-theme":h,children:[b,r,x]}),t[26]=m,t[27]=r,t[28]=o,t[29]=g,t[30]=b,t[31]=x,t[32]=h,t[33]=d,t[34]=S):S=t[34],S},ns=G`
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
`,rs=e=>{let t=(0,X.c)(17),n,r,i,a,o,s;t[0]===e?(n=t[1],r=t[2],i=t[3],a=t[4],o=t[5],s=t[6]):({children:n,variant:a,size:o,overflowMode:s,css:i,...r}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a,t[5]=o,t[6]=s);let c=a===void 0?`default`:a,l=o===void 0?`S`:o,u=s===void 0?`wrap`:s,{theme:d}=Pr(),f;t[7]===i?f=t[8]:(f=G(ns,i),t[7]=i,t[8]=f);let p;return t[9]!==n||t[10]!==r||t[11]!==u||t[12]!==l||t[13]!==f||t[14]!==d||t[15]!==c?(p=U(`span`,{...r,css:f,"data-variant":c,"data-size":l,"data-overflow-mode":u,"data-theme":d,className:`badge`,children:n}),t[9]=n,t[10]=r,t[11]=u,t[12]=l,t[13]=f,t[14]=d,t[15]=c,t[16]=p):p=t[16],p},is=G`
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
`,as=G`
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
`,os=e=>{let t=(0,X.c)(14),n,r,i,a;t[0]===e?(n=t[1],r=t[2],i=t[3],a=t[4]):({className:n,css:r,size:a,...i}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a);let o;t[5]===n?o=t[6]:(o=z(`disclosure-group`,n),t[5]=n,t[6]=o);let s;t[7]===r?s=t[8]:(s=G(is,r),t[7]=r,t[8]=s);let c;return t[9]!==i||t[10]!==a||t[11]!==o||t[12]!==s?(c=U(d,{allowsMultipleExpanded:!0,className:o,css:s,"data-size":a,...i}),t[9]=i,t[10]=a,t[11]=o,t[12]=s,t[13]=c):c=t[13],c},ss=e=>{let t=(0,X.c)(10),n,r,i;t[0]===e?(n=t[1],r=t[2],i=t[3]):({size:i,className:n,...r}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i);let a;t[4]===n?a=t[5]:(a=z(`disclosure`,n),t[4]=n,t[5]=a);let o;return t[6]!==r||t[7]!==i||t[8]!==a?(o=U(l,{className:a,css:as,"data-size":i,defaultExpanded:!0,...r}),t[6]=r,t[7]=i,t[8]=a,t[9]=o):o=t[9],o},cs=e=>{let t=(0,X.c)(8),n,r;t[0]===e?(n=t[1],r=t[2]):({className:n,...r}=e,t[0]=e,t[1]=n,t[2]=r);let i;t[3]===n?i=t[4]:(i=z(`disclosure__panel`,n),t[3]=n,t[4]=i);let a;return t[5]!==r||t[6]!==i?(a=U(m,{className:i,...r}),t[5]=r,t[6]=i,t[7]=a):a=t[7],a},ls=e=>{let t=(0,X.c)(15),{children:n,arrowPosition:r,justifyContent:i,alignItems:a,direction:o,width:s}=e,c=a===void 0?`center`:a,l=o===void 0?`row`:o,u;t[0]===s?u=t[1]:(u={width:s},t[0]=s,t[1]=u);let d=l===`row`?`size-100`:`size-50`,f;t[2]!==c||t[3]!==n||t[4]!==l||t[5]!==i||t[6]!==d?(f=U(K,{justifyContent:i,direction:l,alignItems:c,width:`100%`,gap:d,children:n}),t[2]=c,t[3]=n,t[4]=l,t[5]=i,t[6]=d,t[7]=f):f=t[7];let p;t[8]===r?p=t[9]:(p=r===`none`?null:U(H,{svg:U(Qn,{})}),t[8]=r,t[9]=p);let m;return t[10]!==r||t[11]!==u||t[12]!==f||t[13]!==p?(m=U(Vt,{className:`react-aria-Heading disclosure__trigger`,children:W(vt,{slot:`trigger`,"data-arrow-position":r,style:u,children:[f,p]})}),t[10]=r,t[11]=u,t[12]=f,t[13]=p,t[14]=m):m=t[14],m},us=G`
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
`,ds=G`
  width: var(--trigger-width);
  background-color: var(--field-popover-background-color);
  border-radius: var(--global-rounding-small);
  color: var(--field-text-color);
  box-shadow: 0px 4px 10px var(--field-popover-shadow-color);
  border: 1px solid var(--field-popover-border-color);
  max-height: inherit;
`,fs=G`
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
`,ps=G`
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
`,ms=G(ds,G`
    .react-aria-ListBox {
      display: block;
      width: unset;
      max-height: inherit;
      min-height: unset;
      border: none;
      overflow: auto;
    }
  `),hs=G`
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
`,gs=e=>{e.stopPropagation()};function _s(e){let t=(0,X.c)(46),n,r,i,a,o,s,c,l,u,d,f,m;t[0]===e?(n=t[1],r=t[2],i=t[3],a=t[4],o=t[5],s=t[6],c=t[7],l=t[8],u=t[9],d=t[10],f=t[11],m=t[12]):({label:o,placeholder:s,description:r,errorMessage:i,children:n,size:d,width:m,stopPropagation:u,renderEmptyState:l,isInvalid:a,menuTrigger:f,...c}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a,t[5]=o,t[6]=s,t[7]=c,t[8]=l,t[9]=u,t[10]=d,t[11]=f,t[12]=m);let h=d===void 0?`M`:d,g=f===void 0?`focus`:f,_;t[13]===Symbol.for(`react.memo_cache_sentinel`)?(_=G(us,ps),t[13]=_):_=t[13];let v=a||!!i,y;t[14]===m?y=t[15]:(y={width:m},t[14]=m,t[15]=y);let b=!!l,x;t[16]===o?x=t[17]:(x=o&&U(bn,{children:o}),t[16]=o,t[17]=x);let S=u?gs:void 0,C=u?gs:void 0,T=u?gs:void 0,E;t[18]===s?E=t[19]:(E=U(ke,{placeholder:s}),t[18]=s,t[19]=E);let D;t[20]===Symbol.for(`react.memo_cache_sentinel`)?(D=U(vt,{children:U(dt,{})}),t[20]=D):D=t[20];let O;t[21]!==T||t[22]!==E||t[23]!==S||t[24]!==C?(O=W(`div`,{className:`combobox__container`,onClick:S,onKeyDown:C,onKeyUp:T,children:[E,D]}),t[21]=T,t[22]=E,t[23]=S,t[24]=C,t[25]=O):O=t[25];let k;t[26]!==r||t[27]!==i?(k=r&&!i?U(Wt,{slot:`description`,children:r}):null,t[26]=r,t[27]=i,t[28]=k):k=t[28];let A;t[29]===i?A=t[30]:(A=U(ce,{children:i}),t[29]=i,t[30]=A);let j;t[31]!==n||t[32]!==l?(j=U(fn,{css:ms,children:U(p,{renderEmptyState:l,children:n})}),t[31]=n,t[32]=l,t[33]=j):j=t[33];let M;return t[34]!==g||t[35]!==c||t[36]!==h||t[37]!==O||t[38]!==k||t[39]!==A||t[40]!==j||t[41]!==v||t[42]!==y||t[43]!==b||t[44]!==x?(M=W(w,{...c,menuTrigger:g,css:_,"data-size":h,isInvalid:v,style:y,allowsEmptyCollection:b,children:[x,O,k,A,j]}),t[34]=g,t[35]=c,t[36]=h,t[37]=O,t[38]=k,t[39]=A,t[40]=j,t[41]=v,t[42]=y,t[43]=b,t[44]=x,t[45]=M):M=t[45],M}function vs(e){let t=(0,X.c)(8),n,r;t[0]===e?(n=t[1],r=t[2]):({children:n,...r}=e,t[0]=e,t[1]=n,t[2]=r);let i;t[3]===n?i=t[4]:(i=e=>{let{isSelected:t}=e;return W(V,{children:[n,t&&U(H,{svg:U(_n,{}),className:`menu-item__selected-checkmark`})]})},t[3]=n,t[4]=i);let a;return t[5]!==r||t[6]!==i?(a=U(Ce,{...r,css:hs,children:i}),t[5]=r,t[6]=i,t[7]=a):a=t[7],a}function ys(e){let t=(0,X.c)(11),n,r;t[0]===e?(n=t[1],r=t[2]):({ref:r,...n}=e,t[0]=e,t[1]=n,t[2]=r);let i,a;t[3]===n?(i=t[4],a=t[5]):({size:a,...i}=n,t[3]=n,t[4]=i,t[5]=a);let o=a===void 0?`M`:a,s;t[6]===Symbol.for(`react.memo_cache_sentinel`)?(s=G(us,fs),t[6]=s):s=t[6];let c;return t[7]!==i||t[8]!==r||t[9]!==o?(c=U(oe,{"data-size":o,className:`text-field`,ref:r,...i,css:s}),t[7]=i,t[8]=r,t[9]=o,t[10]=c):c=t[10],c}var bs=()=>{let e=(0,X.c)(1),t;return e[0]===Symbol.for(`react.memo_cache_sentinel`)?(t=U(H,{className:`search-field__icon`,svg:U(lt,{})}),e[0]=t):t=e[0],t},xs=G`
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
`;function Ss(e){let t=(0,X.c)(20),n,r;t[0]===e?(n=t[1],r=t[2]):({ref:r,...n}=e,t[0]=e,t[1]=n,t[2]=r);let i,a,o,s,c;t[3]===n?(i=t[4],a=t[5],o=t[6],s=t[7],c=t[8]):({size:s,variant:c,children:i,isReadOnly:a,...o}=n,t[3]=n,t[4]=i,t[5]=a,t[6]=o,t[7]=s,t[8]=c);let l=s===void 0?`M`:s,u=c===void 0?`default`:c,d;t[9]===Symbol.for(`react.memo_cache_sentinel`)?(d=G(us,fs,xs),t[9]=d):d=t[9];let f;t[10]!==i||t[11]!==a?(f=e=>W(V,{children:[typeof i==`function`?i(e):i,!a&&U(vt,{slot:`clear`,className:`search-field__clear`,"data-empty":e.isEmpty||void 0,children:U(H,{svg:U(Bt,{})})})]}),t[10]=i,t[11]=a,t[12]=f):f=t[12];let p;return t[13]!==a||t[14]!==o||t[15]!==r||t[16]!==l||t[17]!==f||t[18]!==u?(p=U(S,{"data-size":l,"data-variant":u,className:`search-field`,ref:r,isReadOnly:a,...o,css:d,children:f}),t[13]=a,t[14]=o,t[15]=r,t[16]=l,t[17]=f,t[18]=u,t[19]=p):p=t[19],p}var Cs=e(a());function ws(e){let t=(0,X.c)(5),{onChange:n,debounceMs:r}=e,i;t[0]===n?i=t[1]:(i=e=>{(0,Y.startTransition)(()=>{n(e)})},t[0]=n,t[1]=i);let a;return t[2]!==r||t[3]!==i?(a=(0,Cs.default)(i,r),t[2]=r,t[3]=i,t[4]=a):a=t[4],a}var Ts=G`
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
`;function Es(e){let t=(0,X.c)(38),n,r,i,a,o,s;t[0]===e?(n=t[1],r=t[2],i=t[3],a=t[4],o=t[5],s=t[6]):({onChange:i,debounceMs:o,placeholder:n,variant:s,onKeyDown:a,...r}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a,t[5]=o,t[6]=s);let c=o===void 0?200:o,l=s===void 0?`default`:s,u=(0,Y.useRef)(null),d=(0,Y.useRef)(null),f=(0,Y.useRef)(null),[p,m]=(0,Y.useState)(!1),h;t[7]===r.defaultValue?h=t[8]:(h=()=>!!r.defaultValue,t[7]=r.defaultValue,t[8]=h);let[g,_]=(0,Y.useState)(h),v=!g&&!p,y;t[9]!==c||t[10]!==i?(y={onChange:i,debounceMs:c},t[9]=c,t[10]=i,t[11]=y):y=t[11];let b=ws(y),x;t[12]===b?x=t[13]:(x=e=>{_(e!==``),b(e)},t[12]=b,t[13]=x);let S=x,C;t[14]===Symbol.for(`react.memo_cache_sentinel`)?(C=e=>e!=null&&u.current?.contains(e)===!0,t[14]=C):C=t[14];let w=C,T;t[15]===Symbol.for(`react.memo_cache_sentinel`)?(T=e=>m(w(e.target)),t[15]=T):T=t[15];let E=T,D;t[16]===Symbol.for(`react.memo_cache_sentinel`)?(D=e=>{e.relatedTarget==null&&!document.hasFocus()||m(w(e.relatedTarget))},t[16]=D):D=t[16];let O=D,k;t[17]===a?k=t[18]:(k=e=>{e.key===`Escape`&&e.target instanceof HTMLInputElement&&e.target.value===``&&((0,ur.flushSync)(()=>m(!1)),f.current?.focus(),e.preventDefault(),e.stopPropagation()),a?.(e)},t[17]=a,t[18]=k);let A=k,j;t[19]===Symbol.for(`react.memo_cache_sentinel`)?(j=U(bs,{}),t[19]=j):j=t[19];let M;t[20]!==v||t[21]!==n?(M=U(ke,{ref:d,placeholder:n,inert:v}),t[20]=v,t[21]=n,t[22]=M):M=t[22];let N;t[23]!==S||t[24]!==A||t[25]!==r||t[26]!==M?(N=W(Ss,{ref:u,size:`S`,onChange:S,onKeyDown:A,...r,children:[j,M]}),t[23]=S,t[24]=A,t[25]=r,t[26]=M,t[27]=N):N=t[27];let P=r[`aria-label`],F=!v,I;t[28]===Symbol.for(`react.memo_cache_sentinel`)?(I=()=>{(0,ur.flushSync)(()=>m(!0)),d.current?.focus()},t[28]=I):I=t[28];let L;t[29]!==r.isDisabled||t[30]!==P||t[31]!==F?(L=U(vt,{ref:f,className:`search-button__trigger`,"aria-label":P,"aria-expanded":F,isDisabled:r.isDisabled,onPress:I}),t[29]=r.isDisabled,t[30]=P,t[31]=F,t[32]=L):L=t[32];let ee;return t[33]!==v||t[34]!==N||t[35]!==L||t[36]!==l?(ee=W(`div`,{className:`search-button`,"data-variant":l,"data-collapsed":v,css:Ts,onFocus:E,onBlur:O,children:[N,L]}),t[33]=v,t[34]=N,t[35]=L,t[36]=l,t[37]=ee):ee=t[37],ee}var Ds=G`
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
`;function Os(e){let t=(0,X.c)(2),n;return t[0]===e.children?n=t[1]:(n=U(`div`,{className:`composite-field`,css:Ds,children:e.children}),t[0]=e.children,t[1]=n),n}function ks(e){let t=(0,X.c)(16),n,r;t[0]===e?(n=t[1],r=t[2]):({ref:r,...n}=e,t[0]=e,t[1]=n,t[2]=r);let i,a,o;t[3]===n?(i=t[4],a=t[5],o=t[6]):({size:o,children:i,...a}=n,t[3]=n,t[4]=i,t[5]=a,t[6]=o);let s=o===void 0?`M`:o,c;t[7]===Symbol.for(`react.memo_cache_sentinel`)?(c=G(us,fs),t[7]=c):c=t[7];let l;t[8]!==i||t[9]!==a||t[10]!==r||t[11]!==s?(l=U(oe,{"data-size":s,className:`copy-field`,isReadOnly:!0,ref:r,...a,css:c,children:i}),t[8]=i,t[9]=a,t[10]=r,t[11]=s,t[12]=l):l=t[12];let u;return t[13]!==s||t[14]!==l?(u=U(xt,{size:s,children:l}),t[13]=s,t[14]=l,t[15]=u):u=t[15],u}var As=2e3;function js(e){let t=(0,X.c)(30),n,r;t[0]===e?(n=t[1],r=t[2]):({ref:r,...n}=e,t[0]=e,t[1]=n,t[2]=r);let i=Pt(),a,o;t[3]===n?(a=t[4],o=t[5]):({disabled:a,...o}=n,t[3]=n,t[4]=a,t[5]=o);let[s,c]=(0,Y.useState)(!1),l=(0,Y.useRef)(null),u;t[6]===Symbol.for(`react.memo_cache_sentinel`)?(u=()=>{let e=l.current?.value??``;Fe(e),c(!0),setTimeout(()=>{c(!1)},As)},t[6]=u):u=t[6];let d=u,f;t[7]===Symbol.for(`react.memo_cache_sentinel`)?(f=G`
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
      `,t[7]=f):f=t[7];let p;t[8]===r?p=t[9]:(p=e=>{l.current=e,typeof r==`function`?r(e):r&&(r.current=e)},t[8]=r,t[9]=p);let m;t[10]!==a||t[11]!==o||t[12]!==p?(m=U(ke,{...o,ref:p,type:`text`,readOnly:!0,disabled:a}),t[10]=a,t[11]=o,t[12]=p,t[13]=m):m=t[13];let h=s?`Copied`:`Copy to clipboard`,g=s?`success`:`inherit`,_=s?`Checkmark`:`Duplicate`,v;t[14]!==g||t[15]!==_?(v=U(H,{color:g,svgKey:_}),t[14]=g,t[15]=_,t[16]=v):v=t[16];let y;t[17]!==a||t[18]!==h||t[19]!==v?(y=U(vt,{className:`copy-input__copy-button`,onPress:d,isDisabled:a,"aria-label":h,children:v}),t[17]=a,t[18]=h,t[19]=v,t[20]=y):y=t[20];let b=s?`Copied`:`Copy`,x;t[21]===b?x=t[22]:(x=U(oa,{offset:1,children:b}),t[21]=b,t[22]=x);let S;t[23]!==x||t[24]!==y?(S=W(ve,{children:[y,x]}),t[23]=x,t[24]=y,t[25]=S):S=t[25];let C;return t[26]!==i||t[27]!==S||t[28]!==m?(C=W(`div`,{"data-size":i,"data-testid":`copy-input`,css:f,children:[m,S]}),t[26]=i,t[27]=S,t[28]=m,t[29]=C):C=t[29],C}var Ms=(0,Y.createContext)(null);function Ns(){let e=(0,Y.useContext)(Ms);if(!e)throw Error(`useCredentialContext must be used within a CredentialContext.Provider`);return e}function Ps(e){let t=(0,X.c)(21),n,r;t[0]===e?(n=t[1],r=t[2]):({ref:r,...n}=e,t[0]=e,t[1]=n,t[2]=r);let i,a,o;t[3]===n?(i=t[4],a=t[5],o=t[6]):({size:o,children:i,...a}=n,t[3]=n,t[4]=i,t[5]=a,t[6]=o);let s=o===void 0?`M`:o,[c,l]=(0,Y.useState)(!1),u;t[7]===c?u=t[8]:(u={isVisible:c,setIsVisible:l},t[7]=c,t[8]=u);let d;t[9]===Symbol.for(`react.memo_cache_sentinel`)?(d=G(us,fs),t[9]=d):d=t[9];let f;t[10]!==i||t[11]!==a||t[12]!==r||t[13]!==s?(f=U(oe,{"data-size":s,className:`credential-field`,autoComplete:`off`,ref:r,...a,css:d,children:i}),t[10]=i,t[11]=a,t[12]=r,t[13]=s,t[14]=f):f=t[14];let p;t[15]!==s||t[16]!==f?(p=U(xt,{size:s,children:f}),t[15]=s,t[16]=f,t[17]=p):p=t[17];let m;return t[18]!==u||t[19]!==p?(m=U(Ms.Provider,{value:u,children:p}),t[18]=u,t[19]=p,t[20]=m):m=t[20],m}function Fs(e){let t=(0,X.c)(28),n,r;t[0]===e?(n=t[1],r=t[2]):({ref:r,...n}=e,t[0]=e,t[1]=n,t[2]=r);let{isVisible:i,setIsVisible:a}=Ns(),o=Pt(),s,c,l;t[3]===n?(s=t[4],c=t[5],l=t[6]):({disabled:s,readOnly:l,...c}=n,t[3]=n,t[4]=s,t[5]=c,t[6]=l);let u;t[7]===Symbol.for(`react.memo_cache_sentinel`)?(u=G`
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
      `,t[7]=u):u=t[7];let d=i?`text`:`password`,f;t[8]!==s||t[9]!==c||t[10]!==l||t[11]!==r||t[12]!==d?(f=U(ke,{...c,ref:r,type:d,disabled:s,readOnly:l}),t[8]=s,t[9]=c,t[10]=l,t[11]=r,t[12]=d,t[13]=f):f=t[13];let p;t[14]!==i||t[15]!==a?(p=()=>a(!i),t[14]=i,t[15]=a,t[16]=p):p=t[16];let m=s||l,h=i?`Hide credential`:`Show credential`,g;t[17]===i?g=t[18]:(g=U(H,{svg:U(i?Ut:Xt,{})}),t[17]=i,t[18]=g);let _;t[19]!==p||t[20]!==m||t[21]!==h||t[22]!==g?(_=U(vt,{className:`credential-input__toggle`,onPress:p,isDisabled:m,"aria-label":h,children:g}),t[19]=p,t[20]=m,t[21]=h,t[22]=g,t[23]=_):_=t[23];let v;return t[24]!==o||t[25]!==f||t[26]!==_?(v=W(`div`,{"data-size":o,"data-testid":`credential-input`,css:u,children:[f,_]}),t[24]=o,t[25]=f,t[26]=_,t[27]=v):v=t[27],v}var Is=``,Ls=`${Is}REDACTED${Is}`;function Rs(e){return typeof e==`string`&&e.startsWith(Ls)}function zs(e){let t=e.slice(Ls.length),n=t.indexOf(Is);return n<0?null:t.slice(0,n)||null}function Bs(e){if(!Rs(e))return null;let t=zs(e);return t?`••••${t}`:`••••••••`}function Vs(e){let t=(0,X.c)(29),{label:n,placeholder:r,description:i,value:a,onChange:o,onBlur:s,name:c,isDisabled:l,isRequired:u,errorMessage:d,size:f}=e,p=f===void 0?`M`:f,[m,h]=(0,Y.useState)(!1),g;t[0]!==m||t[1]!==a?(g=!m&&Rs(a),t[0]=m,t[1]=a,t[2]=g):g=t[2];let _=g,v=_?``:a??``,y;t[3]!==r||t[4]!==_||t[5]!==a?(y=_?Bs(a)??`••••••••`:r,t[3]=r,t[4]=_,t[5]=a,t[6]=y):y=t[6];let b=y,x;t[7]!==m||t[8]!==o?(x=e=>{m||h(!0),o(e)},t[7]=m,t[8]=o,t[9]=x):x=t[9];let S=x,C=!!d,w;t[10]===n?w=t[11]:(w=U(bn,{children:n}),t[10]=n,t[11]=w);let T;t[12]===b?T=t[13]:(T=U(ke,{placeholder:b}),t[12]=b,t[13]=T);let E;t[14]!==i||t[15]!==d?(E=d?U(ce,{children:d}):i?U(B,{slot:`description`,children:i}):null,t[14]=i,t[15]=d,t[16]=E):E=t[16];let D;return t[17]!==v||t[18]!==S||t[19]!==l||t[20]!==u||t[21]!==c||t[22]!==s||t[23]!==p||t[24]!==C||t[25]!==w||t[26]!==T||t[27]!==E?(D=W(ys,{type:`password`,size:p,name:c,value:v,onChange:S,onBlur:s,isDisabled:l,isRequired:u,isInvalid:C,autoComplete:`off`,children:[w,T,E]}),t[17]=v,t[18]=S,t[19]=l,t[20]=u,t[21]=c,t[22]=s,t[23]=p,t[24]=C,t[25]=w,t[26]=T,t[27]=E,t[28]=D):D=t[28],D}var Hs=G`
  .react-aria-Input {
    text-align: right;
    font-feature-settings: "tnum" 1;
  }
`;function Us(e){let t=(0,X.c)(13),n,r,i,a,o;if(t[0]!==e){let{ref:s,...c}=e;r=s;let{size:l,...u}=c,d=l===void 0?`M`:l;n=g,i=d,a=u,o=z(`text-field react-aria-NumberField`,c.className),t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a,t[5]=o}else n=t[1],r=t[2],i=t[3],a=t[4],o=t[5];let s;t[6]===Symbol.for(`react.memo_cache_sentinel`)?(s=G(us,fs,Hs),t[6]=s):s=t[6];let c;return t[7]!==n||t[8]!==r||t[9]!==i||t[10]!==a||t[11]!==o?(c=U(n,{"data-size":i,...a,className:o,ref:r,css:s}),t[7]=n,t[8]=r,t[9]=i,t[10]=a,t[11]=o,t[12]=c):c=t[12],c}function Ws(e){let t=(0,X.c)(15),n,r,i,a;t[0]===e?(n=t[1],r=t[2],i=t[3],a=t[4]):({onChange:i,debounceMs:a,placeholder:n,...r}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a);let o=a===void 0?200:a,s;t[5]!==o||t[6]!==i?(s={onChange:i,debounceMs:o},t[5]=o,t[6]=i,t[7]=s):s=t[7];let c=ws(s),l;t[8]===Symbol.for(`react.memo_cache_sentinel`)?(l=U(bs,{}),t[8]=l):l=t[8];let u;t[9]===n?u=t[10]:(u=U(ke,{placeholder:n}),t[9]=n,t[10]=u);let d;return t[11]!==c||t[12]!==r||t[13]!==u?(d=W(Ss,{onChange:c,...r,children:[l,u]}),t[11]=c,t[12]=r,t[13]=u,t[14]=d):d=t[14],d}var Gs=()=>{let e=(0,X.c)(1),t;return e[0]===Symbol.for(`react.memo_cache_sentinel`)?(t=U(H,{color:`danger`,className:`field__icon`,svg:U(at,{})}),e[0]=t):t=e[0],t},Ks=()=>{let e=(0,X.c)(1),t;return e[0]===Symbol.for(`react.memo_cache_sentinel`)?(t=U(H,{color:`success`,className:`field__icon`,svg:U(_n,{})}),e[0]=t):t=e[0],t},qs=G`
  /* Pin the palette near the top of the viewport instead of centering it so
     the list can grow and shrink without the dialog jumping around */
  &&[data-variant="default"] .react-aria-Dialog {
    top: 15vh;
    transform: translate(-50%, 0);
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }
`,Js=G`
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
`;function Ys(e){let t=(0,X.c)(32),{isOpen:n,onOpenChange:r,inputValue:i,onInputChange:a,filter:o,placeholder:s,"aria-label":c,onAction:l,children:u,renderEmptyState:d,footer:f,isPending:p}=e,m=s===void 0?`Search…`:s,h=c===void 0?`Command palette`:c,g=p?`true`:void 0,_;t[0]===Symbol.for(`react.memo_cache_sentinel`)?(_=U(bs,{}),t[0]=_):_=t[0];let v;t[1]===m?v=t[2]:(v=U(ke,{placeholder:m}),t[1]=m,t[2]=v);let y;t[3]!==h||t[4]!==v?(y=U(`div`,{className:`command-palette__field`,children:W(Ss,{"aria-label":h,variant:`quiet`,size:`L`,autoFocus:!0,children:[_,v]})}),t[3]=h,t[4]=v,t[5]=y):y=t[5];let b;t[6]===d?b=t[7]:(b=()=>U(`div`,{className:`command-palette__empty-state`,children:d?d():U(bo,{icon:U(H,{svg:U(lt,{})}),description:`No results`})}),t[6]=d,t[7]=b);let x;t[8]!==h||t[9]!==u||t[10]!==l||t[11]!==b?(x=U(Ia,{className:`command-palette__menu`,"aria-label":h,onAction:l,renderEmptyState:b,children:u}),t[8]=h,t[9]=u,t[10]=l,t[11]=b,t[12]=x):x=t[12];let S;t[13]===f?S=t[14]:(S=f??U(Xs,{}),t[13]=f,t[14]=S);let C;t[15]===S?C=t[16]:(C=U(`div`,{className:`command-palette__footer`,children:S}),t[15]=S,t[16]=C);let w;t[17]!==o||t[18]!==i||t[19]!==a||t[20]!==C||t[21]!==y||t[22]!==x?(w=W(Dt,{inputValue:i,onInputChange:a,filter:o,children:[y,x,C]}),t[17]=o,t[18]=i,t[19]=a,t[20]=C,t[21]=y,t[22]=x,t[23]=w):w=t[23];let T;t[24]!==h||t[25]!==w||t[26]!==g?(T=U(Mn,{size:`M`,css:qs,children:U(yn,{"aria-label":h,className:`command-palette`,css:Js,"data-pending":g,children:w})}),t[24]=h,t[25]=w,t[26]=g,t[27]=T):T=t[27];let E;return t[28]!==n||t[29]!==r||t[30]!==T?(E=U(En,{isOpen:n,onOpenChange:r,isDismissable:!0,children:T}),t[28]=n,t[29]=r,t[30]=T,t[31]=E):E=t[31],E}function Xs(){let e=(0,X.c)(3),t;e[0]===Symbol.for(`react.memo_cache_sentinel`)?(t=W(`span`,{className:`command-palette__hint`,children:[U(po,{children:`↑↓`}),U(B,{size:`XS`,color:`text-500`,children:`to navigate`})]}),e[0]=t):t=e[0];let n;e[1]===Symbol.for(`react.memo_cache_sentinel`)?(n=W(`span`,{className:`command-palette__hint`,children:[U(po,{children:`↵`}),U(B,{size:`XS`,color:`text-500`,children:`to select`})]}),e[1]=n):n=e[1];let r;return e[2]===Symbol.for(`react.memo_cache_sentinel`)?(r=W(V,{children:[t,n,W(`span`,{className:`command-palette__hint`,children:[U(po,{children:`esc`}),U(B,{size:`XS`,color:`text-500`,children:`to close`})]})]}),e[2]=r):r=e[2],r}function Zs(e){let t=(0,X.c)(5),{title:n,children:r}=e,i;t[0]===n?i=t[1]:(i=U(Tt,{className:`command-palette__section-header`,children:n}),t[0]=n,t[1]=i);let a;return t[2]!==r||t[3]!==i?(a=W($t,{className:`command-palette__section`,children:[i,r]}),t[2]=r,t[3]=i,t[4]=a):a=t[4],a}var Qs=G`
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
`;function $s(e){let t=(0,X.c)(18),n,r,i,a;t[0]===e?(n=t[1],r=t[2],i=t[3],a=t[4]):({icon:i,description:r,children:n,...a}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a);let o;t[5]===i?o=t[6]:(o=i&&U(`span`,{className:`command-palette-item__icon`,children:i}),t[5]=i,t[6]=o);let s;t[7]===n?s=t[8]:(s=U(`span`,{className:`command-palette-item__label`,children:n}),t[7]=n,t[8]=s);let c;t[9]===r?c=t[10]:(c=r&&U(`span`,{className:`command-palette-item__description`,children:r}),t[9]=r,t[10]=c);let l;t[11]!==o||t[12]!==s||t[13]!==c?(l=W(`div`,{className:`command-palette-item__layout`,children:[o,s,c]}),t[11]=o,t[12]=s,t[13]=c,t[14]=l):l=t[14];let u;return t[15]!==a||t[16]!==l?(u=U(Ra,{...a,className:`command-palette-item`,css:Qs,children:l}),t[15]=a,t[16]=l,t[17]=u):u=t[17],u}var ec=G`
  background-color: rgba(var(--global-color-blue-500-rgb), 0.4);
  color: inherit;
  border-radius: var(--global-rounding-xsmall);
`;function tc(e){let t=(0,X.c)(26),{text:n,match:r}=e,i;t[0]===r?i=t[1]:(i=r?.trim().length??0,t[0]=r,t[1]=i);let a=i;if(!r||a===0){let e;return t[2]===n?e=t[3]:(e=U(V,{children:n}),t[2]=n,t[3]=e),e}let o,s,c,l,u,d;if(t[4]!==r||t[5]!==a||t[6]!==n){d=Symbol.for(`react.early_return_sentinel`);bb0:{let e=n.toLowerCase().indexOf(r.trim().toLowerCase());if(e===-1){let e;t[13]===n?e=t[14]:(e=U(V,{children:n}),t[13]=n,t[14]=e),d=e;break bb0}o=e+a,u=n.slice(0,e),s=`match-text`,c=ec,l=n.slice(e,o)}t[4]=r,t[5]=a,t[6]=n,t[7]=o,t[8]=s,t[9]=c,t[10]=l,t[11]=u,t[12]=d}else o=t[7],s=t[8],c=t[9],l=t[10],u=t[11],d=t[12];if(d!==Symbol.for(`react.early_return_sentinel`))return d;let f;t[15]!==s||t[16]!==c||t[17]!==l?(f=U(`mark`,{className:s,css:c,children:l}),t[15]=s,t[16]=c,t[17]=l,t[18]=f):f=t[18];let p;t[19]!==o||t[20]!==n?(p=n.slice(o),t[19]=o,t[20]=n,t[21]=p):p=t[21];let m;return t[22]!==u||t[23]!==f||t[24]!==p?(m=W(V,{children:[u,f,p]}),t[22]=u,t[23]=f,t[24]=p,t[25]=m):m=t[25],m}G`
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
`,G`
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: var(--global-dimension-size-50);
  height: 28px;
`;var nc=G(`
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
`),rc=e=>{let t=(0,X.c)(16),n,r,i,a,o;t[0]===e?(n=t[1],r=t[2],i=t[3],a=t[4],o=t[5]):({size:a,css:r,className:n,direction:o,...i}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a,t[5]=o);let c=o===void 0?`row`:o,l;t[6]===n?l=t[7]:(l=z(`radio-group`,n),t[6]=n,t[7]=l);let u;t[8]===r?u=t[9]:(u=G(us,nc,r),t[8]=r,t[9]=u);let d;return t[10]!==c||t[11]!==i||t[12]!==a||t[13]!==l||t[14]!==u?(d=U(s,{"data-size":a,"data-direction":c,className:l,css:u,...i}),t[10]=c,t[11]=i,t[12]=a,t[13]=l,t[14]=u,t[15]=d):d=t[15],d},ic=G(`
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
`),ac=e=>{let t=(0,X.c)(12),n,r,i;t[0]===e?(n=t[1],r=t[2],i=t[3]):({className:n,css:r,...i}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i);let a;t[4]===n?a=t[5]:(a=z(`radio`,n),t[4]=n,t[5]=a);let s;t[6]===r?s=t[7]:(s=G(ic,r),t[6]=r,t[7]=s);let c;return t[8]!==i||t[9]!==a||t[10]!==s?(c=U(o,{className:a,css:s,...i}),t[8]=i,t[9]=a,t[10]=s,t[11]=c):c=t[11],c},oc=G(ot,`
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
`),sc=e=>{let t=(0,X.c)(25),n,r,i;t[0]===e?(n=t[1],r=t[2],i=t[3]):({className:n,css:r,...i}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i);let a,o,s,c,l;t[4]===i?(a=t[5],o=t[6],s=t[7],c=t[8],l=t[9]):({leadingVisual:o,trailingVisual:l,size:s,children:a,...c}=i,t[4]=i,t[5]=a,t[6]=o,t[7]=s,t[8]=c,t[9]=l);let u=Pt(),d=s??u,f;t[10]!==a||t[11]!==o||t[12]!==l?(f=e=>W(V,{children:[o,typeof a==`function`?a(e):a,l]}),t[10]=a,t[11]=o,t[12]=l,t[13]=f):f=t[13];let p=f,m;t[14]===r?m=t[15]:(m=G(oc,r),t[14]=r,t[15]=m);let h=!a,g;t[16]===n?g=t[17]:(g=z(`toggle-button`,n),t[16]=n,t[17]=g);let _;return t[18]!==p||t[19]!==c||t[20]!==d||t[21]!==m||t[22]!==h||t[23]!==g?(_=U(I,{css:m,"data-size":d,"data-childless":h,className:g,...c,children:p}),t[18]=p,t[19]=c,t[20]=d,t[21]=m,t[22]=h,t[23]=g,t[24]=_):_=t[24],_},cc=G(`
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
`),lc=e=>{let t=(0,X.c)(19),n,r,i,a,o;t[0]===e?(n=t[1],r=t[2],i=t[3],a=t[4],o=t[5]):({size:a,css:r,className:n,selectionMode:o,...i}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a,t[5]=o);let s=a===void 0?`M`:a,c=o===void 0?`single`:o,l;t[6]===n?l=t[7]:(l=z(`toggle-button-group`,n),t[6]=n,t[7]=l);let u;t[8]===r?u=t[9]:(u=G(cc,r),t[8]=r,t[9]=u);let d;t[10]!==i||t[11]!==c||t[12]!==s||t[13]!==l||t[14]!==u?(d=U(fe,{"data-size":s,className:l,css:u,selectionMode:c,...i}),t[10]=i,t[11]=c,t[12]=s,t[13]=l,t[14]=u,t[15]=d):d=t[15];let f;return t[16]!==s||t[17]!==d?(f=U(xt,{size:s,children:d}),t[16]=s,t[17]=d,t[18]=f):f=t[18],f},uc=G`
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
`,dc=G`
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
`,fc=G`
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
`,pc=G`
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
`;function mc(e){for(let t of Y.Children.toArray(e)){if(!(0,Y.isValidElement)(t))continue;if(t.type===Y.Fragment){let e=mc(t.props.children);if(e!=null)return e;continue}let{id:e,isDisabled:n}=t.props;if(e!=null&&!n)return e}}function hc(e){let t=(0,X.c)(33),n,r,i,a,o,s,c,l,u;t[0]===e?(n=t[1],r=t[2],i=t[3],a=t[4],o=t[5],s=t[6],c=t[7],l=t[8],u=t[9]):({children:n,size:l,isJustified:u,selectedKey:c,defaultSelectedKey:a,onSelectionChange:o,className:r,css:i,...s}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a,t[5]=o,t[6]=s,t[7]=c,t[8]=l,t[9]=u);let d=l===void 0?`M`:l,f=u!==void 0&&u,p;t[10]!==n||t[11]!==a?(p=()=>a??mc(n),t[10]=n,t[11]=a,t[12]=p):p=t[12];let[m]=(0,Y.useState)(p),h;t[13]===c?h=t[14]:(h=c===void 0?void 0:[c],t[13]=c,t[14]=h);let g;t[15]===m?g=t[16]:(g=m==null?void 0:[m],t[15]=m,t[16]=g);let _;t[17]===o?_=t[18]:(_=e=>{let[t]=e;t!=null&&o?.(t)},t[17]=o,t[18]=_);let v;t[19]===r?v=t[20]:(v=z(`segmented-control`,r),t[19]=r,t[20]=v);let y;t[21]===i?y=t[22]:(y=G(uc,i),t[21]=i,t[22]=y);let b;return t[23]!==n||t[24]!==f||t[25]!==s||t[26]!==d||t[27]!==h||t[28]!==g||t[29]!==_||t[30]!==v||t[31]!==y?(b=U(fe,{...s,selectionMode:`single`,disallowEmptySelection:!0,orientation:`horizontal`,selectedKeys:h,defaultSelectedKeys:g,onSelectionChange:_,"data-size":d,"data-justified":f,className:v,css:y,children:n}),t[23]=n,t[24]=f,t[25]=s,t[26]=d,t[27]=h,t[28]=g,t[29]=_,t[30]=v,t[31]=y,t[32]=b):b=t[32],b}function gc(e){let t=(0,X.c)(4),{isSelected:n}=e,r=(0,Y.useRef)(null),i,a;t[0]===n?(i=t[1],a=t[2]):(i=()=>{let e=r.current,t=e?.style.translate;e&&n&&t&&(e.style.translate=`${t.split(` `)[0]} 0px`)},a=[n],t[0]=n,t[1]=i,t[2]=a),(0,Y.useLayoutEffect)(i,a);let o;return t[3]===Symbol.for(`react.memo_cache_sentinel`)?(o=U(wn,{ref:r,className:`segmented-control__thumb`,css:pc}),t[3]=o):o=t[3],o}function _c(e){let t=(0,X.c)(16),n,r,i,a;t[0]===e?(n=t[1],r=t[2],i=t[3],a=t[4]):({children:n,className:r,css:i,...a}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a);let o;t[5]===r?o=t[6]:(o=z(`segmented-control__item`,r),t[5]=r,t[6]=o);let s;t[7]===i?s=t[8]:(s=G(dc,i),t[7]=i,t[8]=s);let c;t[9]===n?c=t[10]:(c=e=>{let{isSelected:t}=e;return W(V,{children:[U(`div`,{className:`segmented-control__item-content`,css:fc,children:typeof n==`string`?U(B,{children:n}):n}),U(gc,{isSelected:t})]})},t[9]=n,t[10]=c);let l;return t[11]!==a||t[12]!==o||t[13]!==s||t[14]!==c?(l=U(I,{...a,className:o,css:s,children:c}),t[11]=a,t[12]=o,t[13]=s,t[14]=c,t[15]=l):l=t[15],l}var vc=G`
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
`;function yc(e){let t=(0,X.c)(10),n,r,i;t[0]===e?(n=t[1],r=t[2],i=t[3]):({css:n,ref:r,...i}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i);let a;t[4]===n?a=t[5]:(a=G(vc,n),t[4]=n,t[5]=a);let o=a,s;return t[6]!==o||t[7]!==r||t[8]!==i?(s=U(p,{css:o,ref:r,...i}),t[6]=o,t[7]=r,t[8]=i,t[9]=s):s=t[9],s}var bc=G`
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
`;function xc(e){let t=(0,X.c)(14),n,r;t[0]===e?(n=t[1],r=t[2]):({ref:r,...n}=e,t[0]=e,t[1]=n,t[2]=r);let i,a,o;t[3]===n?(i=t[4],a=t[5],o=t[6]):({children:i,isHovered:a,...o}=n,t[3]=n,t[4]=i,t[5]=a,t[6]=o);let s=a||void 0,c;t[7]===i?c=t[8]:(c=e=>{let{isIndeterminate:t}=e;return W(V,{children:[U(`div`,{className:`checkbox`,children:U(`svg`,{viewBox:`0 0 18 18`,"aria-hidden":`true`,children:t?U(`rect`,{x:1,y:7.5,width:15,height:3}):U(`polyline`,{points:`1 9 7 14 15 4`})})}),i]})},t[7]=i,t[8]=c);let l;return t[9]!==r||t[10]!==o||t[11]!==s||t[12]!==c?(l=U(_e,{...o,ref:r,css:bc,"data-force-hovered":s,children:c}),t[9]=r,t[10]=o,t[11]=s,t[12]=c,t[13]=l):l=t[13],l}var Sc=G`
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
`,Cc=G`
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
`,wc=G`
  padding: var(--global-dimension-size-50) var(--global-dimension-size-100) 0;
`;G`
  display: flex;
  flex-direction: column;
  gap: var(--global-menu-item-gap);
`;function Tc(e){let t=(0,X.c)(6),n,i;t[0]===e?(n=t[1],i=t[2]):({ref:n,...i}=e,t[0]=e,t[1]=n,t[2]=i);let a;return t[3]!==n||t[4]!==i?(a=U(r,{css:Sc,ref:n,...i}),t[3]=n,t[4]=i,t[5]=a):a=t[5],a}function Ec(e){let t=(0,X.c)(14),n,r,i,a,o;t[0]===e?(n=t[1],r=t[2],i=t[3],a=t[4],o=t[5]):({ref:r,children:n,subtitle:a,trailingContent:o,...i}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a,t[5]=o);let s;t[6]!==n||t[7]!==a||t[8]!==o?(s=e=>{let{selectionMode:t,selectionBehavior:r}=e;return W(V,{children:[U(Dc,{subtitle:a,selectionMode:t,selectionBehavior:r,children:n}),o]})},t[6]=n,t[7]=a,t[8]=o,t[9]=s):s=t[9];let c;return t[10]!==r||t[11]!==i||t[12]!==s?(c=U(ue,{css:Cc,ref:r,...i,children:s}),t[10]=r,t[11]=i,t[12]=s,t[13]=c):c=t[13],c}var Dc=e=>{let t=(0,X.c)(14),{children:n,subtitle:r,selectionMode:i,selectionBehavior:a}=e,[o,s]=(0,Y.useState)(!1),c,l,u;t[0]===Symbol.for(`react.memo_cache_sentinel`)?(c=()=>s(!0),l=()=>s(!1),u=G`
        flex: 1;
        min-width: 0;
      `,t[0]=c,t[1]=l,t[2]=u):(c=t[0],l=t[1],u=t[2]);let d;t[3]!==o||t[4]!==a||t[5]!==i?(d=i===`multiple`&&a===`toggle`&&U(xc,{slot:`selection`,isHovered:o}),t[3]=o,t[4]=a,t[5]=i,t[6]=d):d=t[6];let f;t[7]===Symbol.for(`react.memo_cache_sentinel`)?(f=G`
            padding: var(--global-menu-item-gap);
          `,t[7]=f):f=t[7];let p;t[8]!==n||t[9]!==r?(p=W(K,{direction:`column`,gap:`var(--global-dimension-size-25)`,minWidth:0,flex:1,css:f,children:[n,r]}),t[8]=n,t[9]=r,t[10]=p):p=t[10];let m;return t[11]!==d||t[12]!==p?(m=U(`div`,{onMouseEnter:c,onMouseLeave:l,css:u,children:W(K,{direction:`row`,alignItems:`center`,gap:`size-100`,className:`GridListItem__content`,children:[d,p]})}),t[11]=d,t[12]=p,t[13]=m):m=t[13],m},Oc=e=>{let t=(0,X.c)(2),{title:n}=e,r;return t[0]===n?r=t[1]:(r=U(de,{css:wc,children:U(B,{weight:`heavy`,children:n})}),t[0]=n,t[1]=r),r},kc=G`
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
`;function Ac(e){let t=(0,X.c)(3),{children:n}=e,r;t[0]===Symbol.for(`react.memo_cache_sentinel`)?(r=G`
        display: flex;
        align-items: center;
        justify-content: center;
        width: var(--global-dimension-size-200);
        height: var(--global-dimension-size-200);
        /* The visual keeps its box when the token's text truncates —
           otherwise it compresses and the visual slides into the end cap. */
        flex-shrink: 0;
        margin-right: var(--global-dimension-size-50);
      `,t[0]=r):r=t[0];let i;return t[1]===n?i=t[2]:(i=U(`span`,{css:r,children:n}),t[1]=n,t[2]=i),i}function jc(e){let t=(0,X.c)(58),n,r,i,a,o,s,c,l,u,d,f,p;t[0]===e?(n=t[1],r=t[2],i=t[3],a=t[4],o=t[5],s=t[6],c=t[7],l=t[8],u=t[9],d=t[10],f=t[11],p=t[12]):({ref:l,children:n,isDisabled:i,css:r,color:f,onPress:s,onRemove:c,size:p,style:d,leadingVisual:a,maxWidth:o,...u}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a,t[5]=o,t[6]=s,t[7]=c,t[8]=l,t[9]=u,t[10]=d,t[11]=f,t[12]=p);let m=f===void 0?`var(--global-color-gray-600)`:f,h=p===void 0?`M`:p,{theme:g}=Pr(),_;t[13]!==a||t[14]!==h?(_=a&&h!==`S`?U(Ac,{children:a}):null,t[13]=a,t[14]=h,t[15]=_):_=t[15];let v=_,y;t[16]!==i||t[17]!==c?(y=c?U(`button`,{onClick:()=>{c()},disabled:i,"aria-label":`Remove`,children:U(H,{svg:U(Bt,{})})}):null,t[16]=i,t[17]=c,t[18]=y):y=t[18];let b=y,x;t[19]===n?x=t[20]:(x=U(`span`,{className:`token__text`,children:n}),t[19]=n,t[20]=x);let S=x,C;t[21]!==i||t[22]!==s||t[23]!==c||t[24]!==b||t[25]!==S||t[26]!==v?(C=()=>s&&c?W(V,{children:[W(`button`,{onClick:()=>{s()},disabled:i,children:[v,S]}),b]}):s?W(`button`,{onClick:()=>{s()},disabled:i,children:[v,S]}):c?W(V,{children:[W(`span`,{children:[v,S]}),b]}):W(V,{children:[v,S]}),t[21]=i,t[22]=s,t[23]=c,t[24]=b,t[25]=S,t[26]=v,t[27]=C):C=t[27];let w=C,T;t[28]===r?T=t[29]:(T=G(kc,r),t[28]=r,t[29]=T);let E;t[30]===o?E=t[31]:(E=o&&{"--token-max-width":o},t[30]=o,t[31]=E);let D;t[32]!==m||t[33]!==d||t[34]!==E?(D={"--internal-token-color":m,...E,...d},t[32]=m,t[33]=d,t[34]=E,t[35]=D):D=t[35];let O;t[36]===s?O=t[37]:(O=s&&{"data-interactive":!0},t[36]=s,t[37]=O);let k;t[38]===c?k=t[39]:(k=c&&{"data-removable":!0},t[38]=c,t[39]=k);let A;t[40]===v?A=t[41]:(A=v&&{"data-leading-visual":!0},t[40]=v,t[41]=A);let j;t[42]===i?j=t[43]:(j=i&&{"data-disabled":!0},t[42]=i,t[43]=j);let M;t[44]===w?M=t[45]:(M=w(),t[44]=w,t[45]=M);let N;return t[46]!==l||t[47]!==u||t[48]!==h||t[49]!==O||t[50]!==k||t[51]!==A||t[52]!==j||t[53]!==M||t[54]!==T||t[55]!==D||t[56]!==g?(N=U(`div`,{ref:l,css:T,style:D,"data-theme":g,"data-size":h,...O,...k,...A,...j,...u,children:M}),t[46]=l,t[47]=u,t[48]=h,t[49]=O,t[50]=k,t[51]=A,t[52]=j,t[53]=M,t[54]=T,t[55]=D,t[56]=g,t[57]=N):N=t[57],N}var Mc=G`
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
`;function Nc(e){let n=(0,X.c)(24),r,i,a,o,s,c;n[0]===e?(r=n[1],i=n[2],a=n[3],o=n[4],s=n[5],c=n[6]):({ref:s,label:a,thumbLabels:c,children:i,css:r,...o}=e,n[0]=e,n[1]=r,n[2]=i,n[3]=a,n[4]=o,n[5]=s,n[6]=c);let l;n[7]===r?l=n[8]:(l=G(Mc,r),n[7]=r,n[8]=l);let u;n[9]===a?u=n[10]:(u=a&&U(bn,{className:`slider__label`,children:a}),n[9]=a,n[10]=u);let d;n[11]===i?d=n[12]:(d=i===void 0?U(Ic,{}):i,n[11]=i,n[12]=d);let f;n[13]===d?f=n[14]:(f=U(t,{className:`slider__output`,children:d}),n[13]=d,n[14]=f);let p;n[15]===c?p=n[16]:(p=U(E,{className:`slider__track`,style:Pc,children:e=>{let{state:t}=e;return U(V,{children:t.values.map((e,t)=>U(D,{index:t,"aria-label":c?.[t],className:`slider__thumb`},t))})}}),n[15]=c,n[16]=p);let m;return n[17]!==o||n[18]!==s||n[19]!==l||n[20]!==u||n[21]!==f||n[22]!==p?(m=W(_,{css:l,...o,ref:s,children:[u,f,p]}),n[17]=o,n[18]=s,n[19]=l,n[20]=u,n[21]=f,n[22]=p,n[23]=m):m=n[23],m}function Pc(e){let{state:t}=e;return t.values.length===1?{"--slider-start":`0%`,"--slider-end":`${t.getThumbPercent(0)*100}%`}:{"--slider-start":`${t.getThumbPercent(0)*100}%`,"--slider-end":`${t.getThumbPercent(1)*100}%`}}function Fc(e){let t=(0,X.c)(19),n,r;t[0]===e?(n=t[1],r=t[2]):({onChange:n,...r}=e,t[0]=e,t[1]=n,t[2]=r);let{step:i,getThumbMinValue:a,getThumbMaxValue:o,values:s,setThumbValue:c}=(0,Y.useContext)(T),l=`defaultValue`in r,u=s[0]===a(0),d=l&&u?r.defaultValue:s[0],f=it(Ln),p=f.id,m;t[3]!==n||t[4]!==c?(m=e=>{n?n(e):typeof e==`number`&&c(0,e)},t[3]=n,t[4]=c,t[5]=m):m=t[5];let h;t[6]===o?h=t[7]:(h=o(0),t[6]=o,t[7]=h);let g;t[8]===a?g=t[9]:(g=a(0),t[8]=a,t[9]=g);let _;t[10]===Symbol.for(`react.memo_cache_sentinel`)?(_=U(ke,{}),t[10]=_):_=t[10];let v;return t[11]!==f.id||t[12]!==r||t[13]!==i||t[14]!==m||t[15]!==h||t[16]!==g||t[17]!==d?(v=U(Us,{className:`slider__number-field`,"aria-labelledby":p,value:d,onChange:m,step:i,maxValue:h,minValue:g,...r,children:_}),t[11]=f.id,t[12]=r,t[13]=i,t[14]=m,t[15]=h,t[16]=g,t[17]=d,t[18]=v):v=t[18],v}function Ic(){let e=(0,X.c)(4),t=(0,Y.useContext)(T),n;e[0]===t.values?n=e[1]:(n=t.values.map(Lc).join(` – `),e[0]=t.values,e[1]=n);let r;return e[2]===n?r=e[3]:(r=U(B,{children:n}),e[2]=n,e[3]=r),r}function Lc(e){return e.toString()}var Rc=G`
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
`;function zc(e){let t=(0,X.c)(4),{children:n,variant:r}=e,i=r===void 0?`default`:r,{theme:a}=Pr(),o;return t[0]!==n||t[1]!==a||t[2]!==i?(o=U(`span`,{css:Rc,"data-variant":i,"data-theme":a,className:`counter`,children:n}),t[0]=n,t[1]=a,t[2]=i,t[3]=o):o=t[3],o}function Bc(){let e=(0,X.c)(6),t=(0,Y.useRef)(null),[n,r]=(0,Y.useState)(!1),[i,a]=(0,Y.useState)(!1),o;e[0]===Symbol.for(`react.memo_cache_sentinel`)?(o=()=>{let e=t.current;if(!e)return;if(e.getAttribute(`data-orientation`)!==`horizontal`){r(!1),a(!1);return}let{scrollLeft:n,scrollWidth:i,clientWidth:o}=e,s=i-o;r(n>1),a(n<s-1)},e[0]=o):o=e[0];let s=o;qt(t,`scroll`,s);let c;e[1]===Symbol.for(`react.memo_cache_sentinel`)?(c={ref:t,onResize:s},e[1]=c):c=e[1],sn(c);let l;e[2]===Symbol.for(`react.memo_cache_sentinel`)?(l=()=>{s()},e[2]=l):l=e[2],(0,Y.useEffect)(l);let u;return e[3]!==i||e[4]!==n?(u={ref:t,hasOverflowAtStart:n,hasOverflowAtEnd:i},e[3]=i,e[4]=n,e[5]=u):u=e[5],u}var Vc=G`
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
`;function Hc(e){let t=(0,X.c)(16),n,r,i,a,o;t[0]===e?(n=t[1],r=t[2],i=t[3],a=t[4],o=t[5]):({children:r,css:n,className:i,orientation:o,...a}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a,t[5]=o);let s=o===void 0?`horizontal`:o,c;t[6]===n?c=t[7]:(c=G(Vc,n),t[6]=n,t[7]=c);let l;t[8]===i?l=t[9]:(l=z(`react-aria-Tabs`,`tabs`,i),t[8]=i,t[9]=l);let u;return t[10]!==r||t[11]!==s||t[12]!==a||t[13]!==c||t[14]!==l?(u=U(N,{css:c,className:l,orientation:s,...a,children:r}),t[10]=r,t[11]=s,t[12]=a,t[13]=c,t[14]=l,t[15]=u):u=t[15],u}var Uc=G`
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
`,Wc=G`
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
`;function Gc(e){let t=(0,X.c)(23),n,r,i,a,o;t[0]===e?(n=t[1],r=t[2],i=t[3],a=t[4],o=t[5]):({children:r,extra:a,css:n,className:i,...o}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a,t[5]=o);let{ref:s,hasOverflowAtStart:c,hasOverflowAtEnd:l}=Bc(),u;t[6]===n?u=t[7]:(u=G(Uc,n),t[6]=n,t[7]=u);let d;t[8]===i?d=t[9]:(d=z(`react-aria-TabList`,i),t[8]=i,t[9]=d);let f;t[10]!==r||t[11]!==l||t[12]!==c||t[13]!==o||t[14]!==s||t[15]!==u||t[16]!==d?(f=U(Ie,{ref:s,css:u,className:d,"data-overflow-start":c,"data-overflow-end":l,...o,children:r}),t[10]=r,t[11]=l,t[12]=c,t[13]=o,t[14]=s,t[15]=u,t[16]=d,t[17]=f):f=t[17];let p=f;if(a==null)return p;let m;t[18]===a?m=t[19]:(m=U(`div`,{className:`tab-list-row__extra`,children:a}),t[18]=a,t[19]=m);let h;return t[20]!==m||t[21]!==p?(h=W(`div`,{className:`tab-list-row`,css:Wc,children:[p,m]}),t[20]=m,t[21]=p,t[22]=h):h=t[22],h}var Kc=G`
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
`;function qc(e){let t=(0,X.c)(14),n,r,i,a;t[0]===e?(n=t[1],r=t[2],i=t[3],a=t[4]):({css:n,className:r,padded:i,...a}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a);let o;t[5]===n?o=t[6]:(o=G(Kc,n),t[5]=n,t[6]=o);let s;t[7]===r?s=t[8]:(s=z(`react-aria-TabPanel`,r),t[7]=r,t[8]=s);let c;return t[9]!==i||t[10]!==a||t[11]!==o||t[12]!==s?(c=U(je,{css:o,className:s,"data-padded":i,...a}),t[9]=i,t[10]=a,t[11]=o,t[12]=s,t[13]=c):c=t[13],c}function Jc(e){let t=(0,X.c)(11),n,r,i;t[0]===e?(n=t[1],r=t[2],i=t[3]):({children:n,id:r,...i}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i);let a;t[4]!==n||t[5]!==r?(a=e=>{let{state:t}=e,{selectedKey:i}=t;return i===r?n:null},t[4]=n,t[5]=r,t[6]=a):a=t[6];let o;return t[7]!==r||t[8]!==i||t[9]!==a?(o=U(qc,{id:r,...i,children:a}),t[7]=r,t[8]=i,t[9]=a,t[10]=o):o=t[10],o}var Yc=G`
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
`;function Xc(e){let t=(0,X.c)(15),n,r,i,a;t[0]===e?(n=t[1],r=t[2],i=t[3],a=t[4]):({children:r,css:n,className:i,...a}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a);let o;t[5]===n?o=t[6]:(o=G(Yc,n),t[5]=n,t[6]=o);let s;t[7]===i?s=t[8]:(s=z(`react-aria-Tab`,i),t[7]=i,t[8]=s);let c;t[9]===Symbol.for(`react.memo_cache_sentinel`)?(c=U(wn,{className:`react-aria-SelectionIndicator`}),t[9]=c):c=t[9];let l;return t[10]!==r||t[11]!==a||t[12]!==o||t[13]!==s?(l=W(Re,{css:o,className:s,...a,children:[r,c]}),t[10]=r,t[11]=a,t[12]=o,t[13]=s,t[14]=l):l=t[14],l}var Zc=e=>{let t=(0,X.c)(9),{message:n,size:r,className:i}=e,a;t[0]===Symbol.for(`react.memo_cache_sentinel`)?(a=G`
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        width: 100%;
        height: 100%;
        gap: var(--global-dimension-size-100);
      `,t[0]=a):a=t[0];let o;t[1]===r?o=t[2]:(o=U(ea,{isIndeterminate:!0,"aria-label":`loading`,size:r}),t[1]=r,t[2]=o);let s;t[3]===n?s=t[4]:(s=n==null?null:U(B,{children:n}),t[3]=n,t[4]=s);let c;return t[5]!==i||t[6]!==o||t[7]!==s?(c=W(`div`,{className:i,css:a,children:[o,s]}),t[5]=i,t[6]=o,t[7]=s,t[8]=c):c=t[8],c},Qc=Ht`
  0% {
    opacity: 1;
  }
  50% {
    opacity: 0.4;
  }
  100% {
    opacity: 1;
  }
`,$c=Ht`
  0% {
    transform: translateX(-100%);
  }
  50% {
    transform: translateX(100%);
  }
  100% {
    transform: translateX(100%);
  }
`,el=G`
  display: block;
  background-color: var(--global-color-gray-200);
`,tl=G`
  animation: ${Qc} 2s ease-in-out 0.5s infinite;
`,nl=G`
  position: relative;
  overflow: hidden;
  /* Fix bug in Safari https://bugs.webkit.org/show_bug.cgi?id=68196 */
  -webkit-mask-image: -webkit-radial-gradient(white, black);

  &::after {
    animation: ${$c} 2s linear 0.5s infinite;
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
`,rl=e=>{if(typeof e==`number`)return`${e}px`;if(typeof e==`string`)switch(e){case`none`:return`0`;case`XS`:return`var(--global-rounding-xsmall)`;case`S`:return`var(--global-rounding-small)`;case`M`:return`var(--global-rounding-medium)`;case`L`:return`var(--global-rounding-large)`;case`circle`:return`50%`;default:return e}return`var(--global-rounding-medium)`};function il({ref:e,width:t=`100%`,height:n=`1.2em`,borderRadius:r=`S`,animation:i=`pulse`,className:a,...o}){let s=typeof t==`number`?`${t}px`:t,c=typeof n==`number`?`${n}px`:n,l=rl(r);return U(`span`,{ref:e,className:z(a,`skeleton`),css:[el,i===`pulse`&&tl,i===`wave`&&nl,G`
          width: ${s};
          height: ${c};
          border-radius: ${l};
        `],...o})}il.displayName=`Skeleton`;var al=e=>{let t=(0,X.c)(5),n,r,i;t[0]===Symbol.for(`react.memo_cache_sentinel`)?(n=U(il,{height:100,borderRadius:8,animation:`wave`}),r=U(il,{height:24,width:`80%`,animation:`wave`}),i=U(il,{height:16,width:`60%`,animation:`wave`}),t[0]=n,t[1]=r,t[2]=i):(n=t[0],r=t[1],i=t[2]);let a;return t[3]===e?a=t[4]:(a=W(K,{direction:`column`,gap:`size-100`,width:`100%`,...e,children:[n,r,i]}),t[3]=e,t[4]=a),a},ol=G`
  display: flex;
  flex-direction: column;
`,sl=G`
  display: flex;
  gap: 6px;
`,cl=[[3,2,5,1.5,4,2.5,4],[2,4,1.5,5,3,3.5],[4,2.5,5,2,3],[3,4.5,2,4,1.5,4],[3.5,2,5,2.5]],ll=[`100%`,`95%`,`100%`,`88%`,`92%`];function ul({lines:e=3,animation:t=`pulse`,gap:n=8}){let r=(e,t)=>{let n=cl[e%cl.length],r=t?Math.ceil(n.length*.5):n.length;return n.slice(0,r)};return U(`div`,{css:[ol,G`
          gap: ${n}px;
        `],children:Array.from({length:e},(n,i)=>{let a=i===e-1,o=r(i,a),s=a?`55%`:ll[i%ll.length];return U(`div`,{css:[sl,G`
                width: ${s};
              `],children:o.map((e,n)=>U(il,{css:G`
                  flex-grow: ${e};
                  min-width: 20px;
                `,height:`1em`,animation:t},n))},i)})})}var dl=G`
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
`;function fl(e){let t=(0,X.c)(14),n,r;t[0]===e?(n=t[1],r=t[2]):({ref:r,...n}=e,t[0]=e,t[1]=n,t[2]=r);let i,a;t[3]===n?(i=t[4],a=t[5]):({size:a,...i}=n,t[3]=n,t[4]=i,t[5]=a);let o=a===void 0?`M`:a,s;t[6]===Symbol.for(`react.memo_cache_sentinel`)?(s=G(us,dl),t[6]=s):s=t[6];let c;t[7]!==i||t[8]!==r||t[9]!==o?(c=U(Pe,{"data-size":o,className:`select`,ref:r,css:s,...i}),t[7]=i,t[8]=r,t[9]=o,t[10]=c):c=t[10];let l;return t[11]!==o||t[12]!==c?(l=U(xt,{size:o,children:c}),t[11]=o,t[12]=c,t[13]=l):l=t[13],l}function pl(e){let t=(0,X.c)(10),n,r,i;t[0]===e?(n=t[1],r=t[2],i=t[3]):({ref:r,children:n,...i}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i);let a;t[4]===n?a=t[5]:(a=e=>{let{isSelected:t}=e;return W(K,{direction:`row`,justifyContent:`space-between`,alignItems:`center`,gap:`size-200`,width:`100%`,children:[U(`span`,{children:n}),t&&U(H,{svg:U(_n,{})})]})},t[4]=n,t[5]=a);let o;return t[6]!==r||t[7]!==i||t[8]!==a?(o=U(Ce,{...i,ref:r,children:a}),t[6]=r,t[7]=i,t[8]=a,t[9]=o):o=t[9],o}pl.displayName=`SelectItem`,G`
  max-width: 100%;
  height: auto;
`;var ml=16,hl=8,gl=.05,_l=Ht`
  from {
    opacity: 0;
    transform: translateY(-130%);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
`,vl=G`
  position: fixed;
  top: var(--global-dimension-size-200);
  left: 50%;
  width: 400px;
  max-width: calc(100vw - var(--global-dimension-size-400));
  transform: translateX(-50%);
  outline: none;
  z-index: ${Yn};

  --collapsed-peek: ${ml}px;
  --expanded-gap: ${hl}px;
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
`,yl=G`
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  transform-origin: top center;
  transform: translateY(
      calc(var(--toast-index) * var(--collapsed-peek, ${ml}px))
    )
    scale(calc(1 - var(--toast-index) * ${gl}));
  opacity: calc(1 - var(--toast-index) * 0.1);
  transition:
    transform 300ms cubic-bezier(0.21, 1.02, 0.73, 1),
    opacity 300ms ease;

  @media (prefers-reduced-motion: reduce) {
    transition: none;
  }
`,bl=G`
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
  animation: ${_l} 280ms cubic-bezier(0.21, 1.02, 0.73, 1);
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
`;function xl(e){let t=(0,X.c)(6),{stackIndex:n,children:r}=e,i=100-n,a;t[0]!==n||t[1]!==i?(a={"--toast-index":n,zIndex:i},t[0]=n,t[1]=i,t[2]=a):a=t[2];let o;return t[3]!==r||t[4]!==a?(o=U(`div`,{className:`toast-positioner`,css:yl,style:a,children:r}),t[3]=r,t[4]=a,t[5]=o):o=t[5],o}var Sl=e=>{switch(e){case`success`:return U(H,{svg:U(qn,{})});case`error`:return U(H,{svg:U(Nn,{})});default:return null}},Cl=e=>{switch(e){case`success`:return`var(--global-color-success)`;case`error`:return`var(--global-color-danger)`;default:return`var(--global-color-gray-600)`}},wl=e=>{let t=(0,X.c)(33),{toast:n}=e,{theme:r}=Pr(),i=(0,Y.useContext)(ee),a;t[0]!==i?.visibleToasts||t[1]!==n.key?(a=i?.visibleToasts.findIndex(e=>e.key===n.key)??0,t[0]=i?.visibleToasts,t[1]=n.key,t[2]=a):a=t[2];let o=Math.max(0,a),s;t[3]===n.content.variant?s=t[4]:(s=Sl(n.content.variant),t[3]=n.content.variant,t[4]=s);let c=s,l;t[5]===n.content.variant?l=t[6]:(l=Cl(n.content.variant),t[5]=n.content.variant,t[6]=l);let u;t[7]===l?u=t[8]:(u={"--internal-token-color":l},t[7]=l,t[8]=u);let d;t[9]===Symbol.for(`react.memo_cache_sentinel`)?(d=G`
            display: flex;
            justify-content: space-between;
            width: 100%;
          `,t[9]=d):d=t[9];let f;t[10]!==c||t[11]!==n.content.title?(f=W(B,{slot:`title`,size:`M`,children:[c,n.content.title]}),t[10]=c,t[11]=n.content.title,t[12]=f):f=t[12];let p;t[13]===n.content.message?p=t[14]:(p=U(B,{slot:`description`,children:n.content.message}),t[13]=n.content.message,t[14]=p);let m;t[15]!==f||t[16]!==p?(m=W(xe,{children:[f,p]}),t[15]=f,t[16]=p,t[17]=m):m=t[17];let h;t[18]===Symbol.for(`react.memo_cache_sentinel`)?(h=U(xn,{slot:`close`,size:`S`,color:`inherit`,type:`button`,"aria-label":`Close notification`,children:U(H,{svg:U(Bt,{})})}),t[18]=h):h=t[18];let g;t[19]===m?g=t[20]:(g=W(`div`,{css:d,children:[m,h]}),t[19]=m,t[20]=g);let _;t[21]!==n.content.action||t[22]!==n.key?(_=n.content.action?U(`div`,{className:`toast-action-container`,children:typeof n.content.action==`object`&&`text`in n.content.action?U(Mt,{className:`toast-action-button`,onPress:()=>{let e=n.content.action;if(typeof e==`object`&&e&&`onClick`in e){let t=e.closeOnClick??!0,r=()=>{br?.close(n.key)};e.onClick(r),t&&r()}},size:`S`,children:n.content.action.text}):n.content.action}):null,t[21]=n.content.action,t[22]=n.key,t[23]=_):_=t[23];let v;t[24]!==g||t[25]!==_||t[26]!==u||t[27]!==r||t[28]!==n?(v=W(re,{toast:n,css:bl,className:`react-aria-Toast`,style:u,"data-variant":n.content.variant,"data-theme":r,children:[g,_]}),t[24]=g,t[25]=_,t[26]=u,t[27]=r,t[28]=n,t[29]=v):v=t[29];let y;return t[30]!==o||t[31]!==v?(y=U(xl,{stackIndex:o,children:v}),t[30]=o,t[31]=v,t[32]=y):y=t[32],y},Tl=G`
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
`;function El(e){let t=(0,X.c)(12),n,r;t[0]===e?(n=t[1],r=t[2]):({ref:r,...n}=e,t[0]=e,t[1]=n,t[2]=r);let i,a;t[3]===n?(i=t[4],a=t[5]):({children:i,...a}=n,t[3]=n,t[4]=i,t[5]=a);let o;t[6]===i?o=t[7]:(o=e=>{let{isCurrent:t}=e;return W(V,{children:[i,!t&&U(H,{svg:U(Qn,{})})]})},t[6]=i,t[7]=o);let s;return t[8]!==r||t[9]!==a||t[10]!==o?(s=U(O,{css:Tl,...a,className:`breadcrumb`,ref:r,children:o}),t[8]=r,t[9]=a,t[10]=o,t[11]=s):s=t[11],s}var Dl=G`
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
`;function Ol(e){let t=(0,X.c)(10),n,r;t[0]===e?(n=t[1],r=t[2]):({ref:r,...n}=e,t[0]=e,t[1]=n,t[2]=r);let i,a;t[3]===n?(i=t[4],a=t[5]):({size:a,...i}=n,t[3]=n,t[4]=i,t[5]=a);let o=a===void 0?`M`:a,s;return t[6]!==r||t[7]!==i||t[8]!==o?(s=U(ae,{css:Dl,...i,ref:r,"data-size":o}),t[6]=r,t[7]=i,t[8]=o,t[9]=s):s=t[9],s}var kl=G`
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
`;function Al(e){let t=(0,X.c)(10),n,r,i,a;t[0]===e?(n=t[1],r=t[2],i=t[3],a=t[4]):({ref:i,size:a,children:n,...r}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a);let o=a===void 0?`M`:a,s;return t[5]!==n||t[6]!==r||t[7]!==i||t[8]!==o?(s=U(`ul`,{ref:i,css:kl,"data-list-size":o,...r,children:n}),t[5]=n,t[6]=r,t[7]=i,t[8]=o,t[9]=s):s=t[9],s}function jl(e){let t=(0,X.c)(8),n,r,i;t[0]===e?(n=t[1],r=t[2],i=t[3]):({ref:i,children:n,...r}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i);let a;return t[4]!==n||t[5]!==r||t[6]!==i?(a=U(`li`,{ref:i,...r,children:n}),t[4]=n,t[5]=r,t[6]=i,t[7]=a):a=t[7],a}var Ml=Ht`
  from {
    transform: translate(-50%, var(--global-dimension-size-450));
    opacity: 0;
  }
  to {
    transform: translate(-50%, 0);
    opacity: 1;
  }
`,Nl=G`
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
  animation: ${Ml} 0.1s ease-in-out;
`,Pl=e=>{let t=(0,X.c)(2),{children:n}=e,r;return t[0]===n?r=t[1]:(r=U(`div`,{css:Nl,children:n}),t[0]=n,t[1]=r),r},Fl=G`
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
`;function Il(e){let t=(0,X.c)(6),n,r;t[0]===e?(n=t[1],r=t[2]):({ref:r,...n}=e,t[0]=e,t[1]=n,t[2]=r);let i;return t[3]!==n||t[4]!==r?(i=U(Ee,{...n,ref:r,css:Fl,children:n.children}),t[3]=n,t[4]=r,t[5]=i):i=t[5],i}var Ll=G`
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
`;function Rl(e){let t=(0,X.c)(6),n,r;t[0]===e?(n=t[1],r=t[2]):({ref:r,...n}=e,t[0]=e,t[1]=n,t[2]=r);let i;return t[3]!==n||t[4]!==r?(i=U(tt,{...n,ref:r,css:Ll,className:`separator react-aria-Separator`}),t[3]=n,t[4]=r,t[5]=i):i=t[5],i}var zl=(0,Y.createContext)(null);function Bl(e){let t=(0,X.c)(5),{isCollapsed:n,children:r}=e,i;t[0]===n?i=t[1]:(i={isCollapsed:n},t[0]=n,t[1]=i);let a=i,o;return t[2]!==r||t[3]!==a?(o=U(zl.Provider,{value:a,children:r}),t[2]=r,t[3]=a,t[4]=o):o=t[4],o}function Vl(){return(0,Y.useContext)(zl)}var Hl=e=>G`
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
`;function Ul(e){let t=(0,X.c)(85),n,r,i,a,o,s,c,l,u,d,f,p,m,h,g,_,v,y;t[0]===e?(n=t[1],r=t[2],i=t[3],a=t[4],o=t[5],s=t[6],c=t[7],l=t[8],u=t[9],d=t[10],f=t[11],p=t[12],m=t[13],h=t[14],g=t[15],_=t[16],v=t[17],y=t[18]):({ref:u,title:v,titleExtra:y,titleSeparator:f,subTitle:d,headerContent:a,children:n,collapsible:p,interactiveTitle:m,collapseButtonLabel:r,defaultOpen:h,isOpen:o,scrollBody:g,extra:i,onCollapseChange:s,onOpenChange:c,testId:_,...l}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a,t[5]=o,t[6]=s,t[7]=c,t[8]=l,t[9]=u,t[10]=d,t[11]=f,t[12]=p,t[13]=m,t[14]=h,t[15]=g,t[16]=_,t[17]=v,t[18]=y);let b=f===void 0||f,x=p!==void 0&&p,S=m!==void 0&&m,C=h===void 0||h,w=g!==void 0&&g,{styleProps:T}=vn(l,gn),[E,D]=(0,Y.useState)(x?!C:!1),O=o==null?E:!o,k=(0,Y.useId)(),A=(0,Y.useId)(),j=(0,Y.useId)(),M=(0,Y.useId)(),N;t[19]===s?N=t[20]:(N=e=>{s?.(e)},t[19]=s,t[20]=N);let P=(0,Y.useEffectEvent)(N),F;t[21]!==P||t[22]!==O?(F=()=>{P(O)},t[21]=P,t[22]=O,t[23]=F):F=t[23];let I;t[24]===O?I=t[25]:(I=[O],t[24]=O,t[25]=I),(0,Y.useEffect)(F,I);let L;t[26]!==v||t[27]!==y?(L=W(rt,{level:3,weight:`heavy`,className:`card__title`,children:[v,y]}),t[26]=v,t[27]=y,t[28]=L):L=t[28];let ee;t[29]===d?ee=t[30]:(ee=d&&U(rt,{level:4,className:`card__sub-title`,children:d}),t[29]=d,t[30]=ee);let te;t[31]===a?te=t[32]:(te=a&&U(`div`,{className:`card__header-content`,children:a}),t[31]=a,t[32]=te);let ne;t[33]!==ee||t[34]!==te||t[35]!==L||t[36]!==j?(ne=W(`div`,{id:j,className:`card__heading`,children:[L,ee,te]}),t[33]=ee,t[34]=te,t[35]=L,t[36]=j,t[37]=ne):ne=t[37];let re=ne,ie;t[38]!==O||t[39]!==c?(ie=()=>{D(!O),c?.(O)},t[38]=O,t[39]=c,t[40]=ie):ie=t[40];let ae=ie,oe;t[41]===ae?oe=t[42]:(oe=e=>{let t=e.target;t instanceof Element&&t.closest(`button,a,input,select,textarea,[role="button"]`)||ae()},t[41]=ae,t[42]=oe);let se=oe,ce=!O,le=S?r:void 0,ue=S&&r==null?j:void 0,de=!O,fe;t[43]===de?fe=t[44]:(fe=U(Kt,{isExpanded:de,className:`card__collapse-toggle-icon`}),t[43]=de,t[44]=fe);let pe=!S&&re,me;t[45]!==M||t[46]!==A||t[47]!==ce||t[48]!==le||t[49]!==ue||t[50]!==fe||t[51]!==pe||t[52]!==ae?(me=W(`button`,{onClick:ae,className:`card__collapsible-button button--reset`,id:A,"aria-controls":M,"aria-expanded":ce,"aria-label":le,"aria-labelledby":ue,children:[fe,pe]}),t[45]=M,t[46]=A,t[47]=ce,t[48]=le,t[49]=ue,t[50]=fe,t[51]=pe,t[52]=ae,t[53]=me):me=t[53];let he=me,ge;t[54]===T.style?ge=t[55]:(ge=Hl(T.style),t[54]=T.style,t[55]=ge);let _e;t[56]!==he||t[57]!==x||t[58]!==se||t[59]!==re||t[60]!==S?(_e=x?S?W(`div`,{className:`card__collapsible-header`,onClick:se,children:[he,re]}):he:re,t[56]=he,t[57]=x,t[58]=se,t[59]=re,t[60]=S,t[61]=_e):_e=t[61];let ve;t[62]!==i||t[63]!==k||t[64]!==_e?(ve=W(`header`,{id:k,children:[_e,i]}),t[62]=i,t[63]=k,t[64]=_e,t[65]=ve):ve=t[65];let ye;t[66]!==M||t[67]!==n||t[68]!==k||t[69]!==O||t[70]!==w?(ye=U(`div`,{className:`card__body`,id:M,"aria-labelledby":k,"aria-hidden":O,"data-scrollable":w,children:n}),t[66]=M,t[67]=n,t[68]=k,t[69]=O,t[70]=w,t[71]=ye):ye=t[71];let be;t[72]!==x||t[73]!==O||t[74]!==u||t[75]!==T.style||t[76]!==ge||t[77]!==ve||t[78]!==ye||t[79]!==_||t[80]!==b?(be=W(`section`,{ref:u,css:ge,className:`card`,"data-collapsible":x,"data-collapsed":O,"data-title-separator":b,"data-testid":_,style:T.style,children:[ve,ye]}),t[72]=x,t[73]=O,t[74]=u,t[75]=T.style,t[76]=ge,t[77]=ve,t[78]=ye,t[79]=_,t[80]=b,t[81]=be):be=t[81];let xe;return t[82]!==O||t[83]!==be?(xe=U(Bl,{isCollapsed:O,children:be}),t[82]=O,t[83]=be,t[84]=xe):xe=t[84],xe}var Wl=G`
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
`;function Gl(e){let t=(0,X.c)(2),{children:n}=e;if(!Vl()?.isCollapsed||!n)return null;let r;return t[0]===n?r=t[1]:(r=U(`span`,{className:`card__collapsed-preview`,css:Wl,"aria-hidden":`true`,children:n}),t[0]=n,t[1]=r),r}var Kl=G`
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
`;function ql(e){let t=(0,X.c)(13),n,r,i,a,o;t[0]===e?(n=t[1],r=t[2],i=t[3],a=t[4],o=t[5]):({ref:i,children:n,labelPlacement:a,size:o,...r}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a,t[5]=o);let s=a===void 0?`end`:a,c=o===void 0?`M`:o,l;t[6]===Symbol.for(`react.memo_cache_sentinel`)?(l=U(`div`,{className:`indicator`}),t[6]=l):l=t[6];let u;return t[7]!==n||t[8]!==s||t[9]!==r||t[10]!==i||t[11]!==c?(u=W(b,{...r,ref:i,css:Kl,"data-label-placement":s,"data-size":c,children:[l,n]}),t[7]=n,t[8]=s,t[9]=r,t[10]=i,t[11]=c,t[12]=u):u=t[12],u}G`
  position: relative;
`,G`
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
`;var Jl=G`
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
`,Yl=G`
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
`;G`
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
`;function Xl(e,t){let{si:n=!1,decimalPlaces:r=1}=t??{},i=n?1e3:1024;if(Math.abs(e)<i)return e+` B`;let a=n?[`kB`,`MB`,`GB`,`TB`,`PB`,`EB`,`ZB`,`YB`]:[`KiB`,`MiB`,`GiB`,`TiB`,`PiB`,`EiB`,`ZiB`,`YiB`],o=-1,s=10**r;do e/=i,++o;while(Math.round(Math.abs(e)*s)/s>=i&&o<a.length-1);return e.toFixed(r)+` `+a[o]}function Zl(e,t){return!t||t.length===0||t.some(t=>{if(t.startsWith(`.`))return e.name.toLowerCase().endsWith(t.toLowerCase());if(t.endsWith(`/*`)){let n=t.slice(0,-2);return e.type.startsWith(n)}return e.type===t})}function Ql(e,t){return t==null||e.size<=t}function $l(e){let t=(0,X.c)(46),n,r,i,a,o,s,c,l,u,d;t[0]===e?(n=t[1],r=t[2],i=t[3],a=t[4],o=t[5],s=t[6],c=t[7],l=t[8],u=t[9],d=t[10]):({acceptedFileTypes:n,allowsMultiple:u,maxFiles:s,maxFileSize:o,onSelect:c,onSelectRejected:l,label:d,description:i,isDisabled:a,...r}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a,t[5]=o,t[6]=s,t[7]=c,t[8]=l,t[9]=u,t[10]=d);let f=u!==void 0&&u,p=d===void 0?`Drag and drop files here`:d,m=(0,Y.useRef)(null),g=(0,Y.useRef)(null),_,v;t[11]===a?(_=t[12],v=t[13]):(_=()=>{let e=g.current;if(!e||a)return;let t=e=>{(e.key===`Enter`||e.key===` `)&&(e.preventDefault(),m.current?.click())};return e.addEventListener(`keydown`,t),()=>e.removeEventListener(`keydown`,t)},v=[a],t[11]=a,t[12]=_,t[13]=v),(0,Y.useEffect)(_,v);let y;t[14]!==n||t[15]!==f||t[16]!==o||t[17]!==s||t[18]!==c||t[19]!==l?(y=e=>{let t=[],r=[],i=f?s??1/0:1;for(let a of e){if(!Zl(a,n)){r.push({file:a,reason:`type`,message:`File type not accepted. Allowed: ${n?.join(`, `)}`});continue}if(!Ql(a,o)){r.push({file:a,reason:`size`,message:`File too large. Maximum size: ${Xl(o)}`});continue}if(t.length>=i){r.push({file:a,reason:`count`,message:`Maximum ${i} file${i>1?`s`:``} allowed`});continue}t.push(a)}t.length>0&&c&&c(t),r.length>0&&l&&l(r)},t[14]=n,t[15]=f,t[16]=o,t[17]=s,t[18]=c,t[19]=l,t[20]=y):y=t[20];let b=y,x;t[21]===b?x=t[22]:(x=e=>{e.target.files&&(b(Array.from(e.target.files)),e.target.value=``)},t[21]=b,t[22]=x);let S=x,C;t[23]===b?C=t[24]:(C=async e=>{let t=e.items.filter(ru),n=(await Promise.allSettled(t.map(nu))).filter(tu).map(eu);n.length>0&&b(n)},t[23]=b,t[24]=C);let w=C,T;t[25]!==n||t[26]!==a?(T=e=>a?`cancel`:!n||n.length===0||n.some(t=>t.startsWith(`.`)||t.endsWith(`/*`)?!0:e.has(t))?`copy`:`cancel`,t[25]=n,t[26]=a,t[27]=T):T=t[27];let E=T,D;t[28]===a?D=t[29]:(D=()=>{a||m.current?.click()},t[28]=a,t[29]=D);let O=D,k;t[30]!==n||t[31]!==i?(k=i??(n&&n.length>0?`Accepted: ${n.join(`, `)}`:void 0),t[30]=n,t[31]=i,t[32]=k):k=t[32];let A=k,j;t[33]!==n||t[34]!==f||t[35]!==A||t[36]!==S||t[37]!==p||t[38]!==O?(j=e=>{let{isDropTarget:t}=e;return W(V,{children:[U(`input`,{ref:m,type:`file`,accept:n?.join(`,`),multiple:f,onChange:S,hidden:!0}),W(`div`,{className:`file-drop-zone__trigger`,onClick:O,children:[U(`div`,{className:`file-drop-zone__icon`,children:U(H,{svg:U(nt,{})})}),U(Wt,{className:`file-drop-zone__label`,children:t?`Drop files here`:p}),A?U(Wt,{className:`file-drop-zone__description`,children:A}):null]})]})},t[33]=n,t[34]=f,t[35]=A,t[36]=S,t[37]=p,t[38]=O,t[39]=j):j=t[39];let M;return t[40]!==r||t[41]!==E||t[42]!==w||t[43]!==a||t[44]!==j?(M=U(h,{ref:g,css:Jl,onDrop:w,getDropOperation:E,isDisabled:a,...r,children:j}),t[40]=r,t[41]=E,t[42]=w,t[43]=a,t[44]=j,t[45]=M):M=t[45],M}function eu(e){return e.value}function tu(e){return e.status===`fulfilled`}function nu(e){return e.getFile()}function ru(e){return e.kind===`file`}function iu(e){switch(e.status){case`pending`:return`Pending`;case`uploading`:return`Uploading${e.progress===void 0?``:` ${e.progress}%`}`;case`parsing`:return`Parsing...`;case`complete`:return`Complete`;case`error`:return`Error`;default:return``}}function au(e){let t=(0,X.c)(32),{file:n,onRemove:r,isDisabled:i}=e,{file:a,progress:o,status:s,error:c}=n,l=s===`uploading`&&o!==void 0,u;t[0]===Symbol.for(`react.memo_cache_sentinel`)?(u=U(`div`,{className:`file-list__icon`,children:U(H,{svg:U(ut,{})})}),t[0]=u):u=t[0];let d;t[1]===a.name?d=t[2]:(d=U(`span`,{className:`file-list__name`,title:a.name,children:a.name}),t[1]=a.name,t[2]=d);let f;t[3]===a.size?f=t[4]:(f=Xl(a.size),t[3]=a.size,t[4]=f);let p;t[5]===f?p=t[6]:(p=U(`span`,{children:f}),t[5]=f,t[6]=p);let m;t[7]!==n||t[8]!==s?(m=s&&W(V,{children:[U(`span`,{children:`-`}),U(`span`,{children:iu(n)})]}),t[7]=n,t[8]=s,t[9]=m):m=t[9];let h;t[10]!==p||t[11]!==m?(h=W(`div`,{className:`file-list__meta`,children:[p,m]}),t[10]=p,t[11]=m,t[12]=h):h=t[12];let g;t[13]===c?g=t[14]:(g=c&&U(`span`,{className:`file-list__error`,children:c}),t[13]=c,t[14]=g);let _;t[15]!==o||t[16]!==l?(_=l&&U(`div`,{className:`file-list__progress`,children:U(ta,{value:o,width:`100%`,height:`4px`})}),t[15]=o,t[16]=l,t[17]=_):_=t[17];let v;t[18]!==d||t[19]!==h||t[20]!==g||t[21]!==_?(v=W(`div`,{className:`file-list__details`,children:[d,h,g,_]}),t[18]=d,t[19]=h,t[20]=g,t[21]=_,t[22]=v):v=t[22];let y;t[23]!==a||t[24]!==i||t[25]!==r||t[26]!==s?(y=r&&U(`div`,{className:`file-list__remove`,children:U(xn,{size:`S`,"aria-label":`Remove ${a.name}`,onPress:()=>r(a),isDisabled:i||s===`uploading`||s===`parsing`,children:U(H,{svg:U(Bt,{})})})}),t[23]=a,t[24]=i,t[25]=r,t[26]=s,t[27]=y):y=t[27];let b;return t[28]!==s||t[29]!==y||t[30]!==v?(b=W(`li`,{className:`file-list__item`,"data-status":s,children:[u,v,y]}),t[28]=s,t[29]=y,t[30]=v,t[31]=b):b=t[31],b}function ou(e){let t=(0,X.c)(12),{files:n,onRemove:r,isDisabled:i,children:a,"aria-label":o}=e,s=o===void 0?`Selected files`:o;if(n.length===0)return null;let c=su,l;t[0]!==a||t[1]!==i||t[2]!==r?(l=(e,t)=>a?U(Y.Fragment,{children:a(e,t)},c(e)):U(au,{file:e,onRemove:r,isDisabled:i},c(e)),t[0]=a,t[1]=i,t[2]=r,t[3]=l):l=t[3];let u=l,d;if(t[4]!==n||t[5]!==u){let e;t[7]===u?e=t[8]:(e=(e,t)=>u(e,t),t[7]=u,t[8]=e),d=n.map(e),t[4]=n,t[5]=u,t[6]=d}else d=t[6];let f;return t[9]!==s||t[10]!==d?(f=U(`ul`,{css:Yl,"aria-label":s,children:d}),t[9]=s,t[10]=d,t[11]=f):f=t[11],f}function su(e){return`${e.file.name}-${e.file.size}-${e.file.lastModified}`}var cu=e=>G`
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: ${e};
  overflow: hidden;
  text-overflow: ellipsis;
`;function lu(e){let t=(0,X.c)(5),{children:n,lines:r}=e,i;t[0]===r?i=t[1]:(i=cu(r),t[0]=r,t[1]=i);let a;return t[2]!==n||t[3]!==i?(a=U(`div`,{css:i,children:n}),t[2]=n,t[3]=i,t[4]=a):a=t[4],a}function uu(e){let t=(0,X.c)(3),{children:n}=e,r;t[0]===Symbol.for(`react.memo_cache_sentinel`)?(r={display:`contents`},t[0]=r):r=t[0];let i;return t[1]===n?i=t[2]:(i=U(`div`,{style:r,onClick:gu,onKeyDown:hu,onKeyUp:mu,onMouseDown:pu,onPointerDown:fu,onPointerUp:du,children:n}),t[1]=n,t[2]=i),i}function du(e){return e.stopPropagation()}function fu(e){return e.stopPropagation()}function pu(e){return e.stopPropagation()}function mu(e){return e.stopPropagation()}function hu(e){return e.stopPropagation()}function gu(e){return e.stopPropagation()}var _u=G`
  border-radius: var(--global-dimension-size-50);
  border: 1px solid var(--global-border-color-default);
  transition: background-color 0.2s;
  &[data-clickable="true"] {
    cursor: pointer;
    &:hover {
      background-color: var(--global-color-gray-300);
    }
  }
`,vu=G`
  width: 1px;
  height: 0.7em;
  background-color: currentColor;
  opacity: 0.2;
`,yu=G`
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
`,bu=G`
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
`,xu=G`
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
    ${_u};
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
`,Su=1.5;function Cu(e){return e.offsetWidth>0||e.offsetHeight>0}function wu(e){return Array.from(e.children).filter(e=>e instanceof HTMLElement&&Cu(e))}function Tu(e){let{paddingRight:t}=getComputedStyle(e);return e.clientWidth-(parseFloat(t)||0)}function Eu(e){let t=wu(e),n=Tu(e),r=0,i=0,a=0,o=1/0,s=-1/0;for(let e of t){let t=e.offsetTop,c=t+e.offsetHeight;if(r>0&&(t>=s||c<=o))break;let l=e.offsetLeft+e.offsetWidth;if(l>n+Su)break;r+=1,o=Math.min(o,t),s=Math.max(s,c),i=Math.max(i,l),a=Math.max(a,e.offsetHeight)}return{items:t,visibleCount:r,badgeLeft:i,lineHeight:a||(t[0]?.offsetHeight??0)}}var Du=[{name:`inert`,value:``,flag:`overflowRowInert`},{name:`aria-hidden`,value:`true`,flag:`overflowRowAriaHidden`}];function Ou({items:e,visibleCount:t}){e.forEach((e,n)=>{if(n<t){ku(e);return}for(let{name:t,value:n,flag:r}of Du)e.hasAttribute(t)||(e.dataset[r]=`true`,e.setAttribute(t,n))})}function ku(e){for(let{name:t,flag:n}of Du)e.dataset[n]&&(delete e.dataset[n],e.removeAttribute(t))}function Au(e){for(let t of Array.from(e.children))t instanceof HTMLElement&&ku(t)}var ju={childList:!0,characterData:!0,subtree:!0};function Mu(e){let t=e=>(e instanceof Element?e:e.parentElement)?.closest(`.overflow-row__badge-slot`)!=null;return e.type===`childList`?[...e.addedNodes,...e.removedNodes].every(t):t(e.target)}function Nu(e,t){return e===null||t===null?e===t:e.hiddenCount===t.hiddenCount&&e.visibleCount===t.visibleCount&&e.badgeLeft===t.badgeLeft&&e.lineHeight===t.lineHeight}function Pu(e){let t=(0,X.c)(5),{visibleCount:n,children:r}=e,i=(0,Y.useRef)(null),a,o;t[0]===n?(a=t[1],o=t[2]):(a=()=>{let e=i.current;if(!e)return;let t=()=>{let t=Array.from(e.children).filter(Iu);for(let e of t)e.dataset.overflowRowHidden&&(e.style.display=``,delete e.dataset.overflowRowHidden);t.filter(Cu).slice(0,n).forEach(Fu)};t();let r=new MutationObserver(t);return r.observe(e,ju),()=>r.disconnect()},o=[n],t[0]=n,t[1]=a,t[2]=o),(0,Y.useLayoutEffect)(a,o);let s;return t[3]===r?s=t[4]:(s=U(K,{ref:i,direction:`row`,wrap:`wrap`,gap:`size-50`,maxWidth:`size-5000`,children:r}),t[3]=r,t[4]=s),s}function Fu(e){e.style.display=`none`,e.dataset.overflowRowHidden=`true`}function Iu(e){return e instanceof HTMLElement}function Lu(e){let t=(0,X.c)(21),{children:n,isExpanded:r}=e,i=r!==void 0&&r,a=(0,Y.useRef)(null),o=(0,Y.useRef)(null),[s,c]=(0,Y.useState)(null),l,u;t[0]===i?(l=t[1],u=t[2]):(l=()=>{let e=a.current;if(i||!e){c(null);return}let t=null,n=()=>{t=e.getBoundingClientRect().width;let{items:n,visibleCount:r,badgeLeft:i,lineHeight:a}=Eu(e);Ou({items:n,visibleCount:r});let o=n.length-r,s=o===0?null:{hiddenCount:o,visibleCount:r,badgeLeft:i,lineHeight:a};c(e=>Nu(e,s)?e:s)};n(),o.current=n;let r=!1;document.fonts?.status===`loading`&&document.fonts.ready.then(()=>{r||n()});let s=new ResizeObserver(e=>{let[r]=e,i=r?.borderBoxSize?.[0]?.inlineSize??null;(i===null||i!==t)&&(t=i,n())});s.observe(e);let l=new MutationObserver(e=>{e.every(Mu)||n()});return l.observe(e,ju),()=>{r=!0,s.disconnect(),l.disconnect(),o.current=null,Au(e)}},u=[i],t[0]=i,t[1]=l,t[2]=u),(0,Y.useLayoutEffect)(l,u);let d,f;t[3]===s?(d=t[4],f=t[5]):(d=()=>{s!==null&&o.current?.()},f=[s],t[3]=s,t[4]=d,t[5]=f),(0,Y.useLayoutEffect)(d,f);let p=!i,m=!i&&s!==null,h=!i&&s!==null&&s.visibleCount===0,g;t[6]!==p||t[7]!==m||t[8]!==h?(g=z(`overflow-row`,{"overflow-row--collapsed":p,"overflow-row--overflowing":m,"overflow-row--badge-only":h}),t[6]=p,t[7]=m,t[8]=h,t[9]=g):g=t[9];let _;t[10]===s?_=t[11]:(_=s===null?void 0:{"--overflow-row-badge-left":`calc(${s.badgeLeft}px + var(--global-dimension-size-50))`,"--overflow-row-line-height":`${s.lineHeight}px`},t[10]=s,t[11]=_);let v;t[12]!==n||t[13]!==i||t[14]!==s?(v=!i&&s!==null?U(`div`,{className:`overflow-row__badge-slot`,children:W(yt,{children:[W(vt,{className:`overflow-row__badge`,"data-clickable":`true`,"aria-label":`Show ${s.hiddenCount} more`,children:[`+`,s.hiddenCount]}),U(uu,{children:W($n,{placement:`bottom end`,children:[U(Lt,{}),U(yn,{children:U(ra,{padding:`size-150`,children:U(Pu,{visibleCount:s.visibleCount,children:n})})})]})})]})}):null,t[12]=n,t[13]=i,t[14]=s,t[15]=v):v=t[15];let y;return t[16]!==n||t[17]!==_||t[18]!==v||t[19]!==g?(y=W(`div`,{ref:a,css:xu,className:g,style:_,children:[n,v]}),t[16]=n,t[17]=_,t[18]=v,t[19]=g,t[20]=y):y=t[20],y}var Ru=G`
  text-overflow: ellipsis;
  overflow: hidden;
  white-space: nowrap;
`,zu=G`
  display: -webkit-box;
  -webkit-box-orient: vertical;
  overflow: hidden;
`,Bu=e=>{let t=(0,X.c)(11),{children:n,maxWidth:r,title:i,maxLines:a}=e,o=(a??0)>1,s=o?zu:Ru,c;t[0]!==o||t[1]!==a?(c=o&&{WebkitLineClamp:a},t[0]=o,t[1]=a,t[2]=c):c=t[2];let l;t[3]!==r||t[4]!==c?(l={maxWidth:r,...c},t[3]=r,t[4]=c,t[5]=l):l=t[5];let u;return t[6]!==n||t[7]!==s||t[8]!==l||t[9]!==i?(u=U(`div`,{css:s,style:l,title:i,children:n}),t[6]=n,t[7]=s,t[8]=l,t[9]=i,t[10]=u):u=t[10],u};function Vu(){let e=(0,X.c)(3),t,n;e[0]===Symbol.for(`react.memo_cache_sentinel`)?(t=U(xn,{slot:`previous`,size:`S`,children:U(H,{svg:U(on,{})})}),n=U(Vt,{className:`calendar__heading`}),e[0]=t,e[1]=n):(t=e[0],n=e[1]);let r;return e[2]===Symbol.for(`react.memo_cache_sentinel`)?(r=W(`header`,{className:`calendar__header`,children:[t,n,U(xn,{slot:`next`,size:`S`,children:U(H,{svg:U(Qn,{})})})]}),e[2]=r):r=e[2],r}function Hu(e){let t=(0,X.c)(8),{months:n,errorMessage:r}=e,i;t[0]===Symbol.for(`react.memo_cache_sentinel`)?(i=U(Vu,{}),t[0]=i):i=t[0];let a;t[1]===n?a=t[2]:(a=U(`div`,{className:`calendar__months`,children:Array.from({length:n},Uu)}),t[1]=n,t[2]=a);let o;t[3]===r?o=t[4]:(o=r&&U(Wt,{slot:`errorMessage`,children:r}),t[3]=r,t[4]=o);let s;return t[5]!==a||t[6]!==o?(s=W(V,{children:[i,a,o]}),t[5]=a,t[6]=o,t[7]=s):s=t[7],s}function Uu(e,t){return U(j,{offset:{months:t},children:Wu},t)}function Wu(e){return U(ye,{date:e})}var Gu=G`
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
`,Ku=G`
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
`,qu=G`
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
`;function Ju(e){let t=(0,X.c)(10),n,r,a,o;if(t[0]!==e){let{ref:s,...c}=e;r=s;let{css:l,...u}=c;a=u,n=i,o=G(us,qu,l),t[0]=e,t[1]=n,t[2]=r,t[3]=a,t[4]=o}else n=t[1],r=t[2],a=t[3],o=t[4];let s;return t[5]!==n||t[6]!==r||t[7]!==a||t[8]!==o?(s=U(n,{css:o,...a,"data-size":`S`,ref:r}),t[5]=n,t[6]=r,t[7]=a,t[8]=o,t[9]=s):s=t[9],s}function Yu(e){let t=(0,X.c)(17),n,r,i,a,o;t[0]===e?(n=t[1],r=t[2],i=t[3],a=t[4],o=t[5]):({errorMessage:r,css:i,children:n,ref:a,...o}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a,t[5]=o);let s=e.visibleDuration?.months||1,c;t[6]===i?c=t[7]:(c=G(Gu,Ku,i),t[6]=i,t[7]=c);let l;t[8]!==n||t[9]!==r||t[10]!==s?(l=n??U(Hu,{months:s,errorMessage:r}),t[8]=n,t[9]=r,t[10]=s,t[11]=l):l=t[11];let u;return t[12]!==a||t[13]!==o||t[14]!==c||t[15]!==l?(u=U(De,{ref:a,css:c,...o,children:l}),t[12]=a,t[13]=o,t[14]=c,t[15]=l,t[16]=u):u=t[16],u}G`
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
`;var Xu=G`
  font-family: var(--global-font-family-mono);
  font-variant-numeric: tabular-nums;
  ${Qe};
`;function Zu(e){return e.toString().padStart(2,`0`)}function Qu(e){let t=Math.floor(e/3600),n=Math.floor(e%3600/60),r=e%60;return t>0?`${Zu(t)}:${Zu(n)}:${Zu(r)}`:`${Zu(n)}:${Zu(r)}`}function $u(e){return Math.max(0,Math.floor((Date.now()-e.getTime())/1e3))}function ed(e){let t=(0,X.c)(18),{startTime:n,color:r,size:i}=e,a=r===void 0?`text-900`:r,o=i===void 0?`S`:i,s;t[0]===n?s=t[1]:(s=n??new Date,t[0]=n,t[1]=s);let c=s,l;t[2]===c?l=t[3]:(l=()=>$u(c),t[2]=c,t[3]=l);let[u,d]=(0,Y.useState)(l),f,p;t[4]===c?(f=t[5],p=t[6]):(f=()=>{d($u(c));let e=setInterval(()=>{d($u(c))},1e3);return()=>clearInterval(e)},p=[c],t[4]=c,t[5]=f,t[6]=p),(0,Y.useEffect)(f,p);let m;t[7]===a?m=t[8]:(m=At(a),t[7]=a,t[8]=m);let h;t[9]===m?h=t[10]:(h={color:m},t[9]=m,t[10]=h);let g=`PT${u}S`,_;t[11]===u?_=t[12]:(_=Qu(u),t[11]=u,t[12]=_);let v;return t[13]!==o||t[14]!==h||t[15]!==g||t[16]!==_?(v=U(`time`,{css:Xu,"data-size":o,style:h,dateTime:g,children:_}),t[13]=o,t[14]=h,t[15]=g,t[16]=_,t[17]=v):v=t[17],v}var td=2e3,nd=G`
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
    ${yu}
  }
`,rd=e=>{let t=(0,X.c)(20),{id:n,size:r,tooltipText:i,variant:a}=e,o=r===void 0?`S`:r,s=i===void 0?`Copy ID`:i,c=a===void 0?`badge`:a,[l,u]=(0,Y.useState)(!1),d=l?`success`:`inherit`,f=l?`Checkmark`:`Duplicate`,p;t[0]!==d||t[1]!==f?(p=U(H,{className:`id-badge__copy-icon`,color:d,svgKey:f}),t[0]=d,t[1]=f,t[2]=p):p=t[2];let m=p,h=`${s} ${n}`,g;t[3]===n?g=t[4]:(g=()=>{Fe(n),u(!0),setTimeout(()=>{u(!1)},td)},t[3]=n,t[4]=g);let _;t[5]!==m||t[6]!==n||t[7]!==o||t[8]!==c?(_=c===`badge`?W(rs,{size:o,children:[U(H,{svgKey:`ID`}),U(B,{fontFamily:`mono`,size:`S`,color:`text-700`,children:n}),m]}):W(V,{children:[U(B,{fontFamily:`mono`,size:`S`,color:`text-500`,children:n}),m]}),t[5]=m,t[6]=n,t[7]=o,t[8]=c,t[9]=_):_=t[9];let v;t[10]!==h||t[11]!==g||t[12]!==_||t[13]!==c?(v=U(vt,{css:nd,"data-variant":c,"aria-label":h,onPress:g,children:_}),t[10]=h,t[11]=g,t[12]=_,t[13]=c,t[14]=v):v=t[14];let y=l?`Copied`:s,b;t[15]===y?b=t[16]:(b=U(oa,{offset:1,children:y}),t[15]=y,t[16]=b);let x;return t[17]!==v||t[18]!==b?(x=W(ve,{children:[v,b]}),t[17]=v,t[18]=b,t[19]=x):x=t[19],x},id=e=>{let t=(0,X.c)(7),{title:n,id:r}=e,i;t[0]===n?i=t[1]:(i=U(rt,{children:n}),t[0]=n,t[1]=i);let a;t[2]===r?a=t[3]:(a=U(rd,{size:`S`,id:r}),t[2]=r,t[3]=a);let o;return t[4]!==i||t[5]!==a?(o=W(K,{direction:`row`,gap:`size-100`,alignItems:`center`,children:[i,a]}),t[4]=i,t[5]=a,t[6]=o):o=t[6],o},ad=`selectedSpanNodeId`,od=`spanFilterCondition`,sd=`sessionView`,cd=`selectedTraceId`,ld=[cd,ad],ud=`timeRangeKey`,dd=`timeRangeStart`,fd=`timeRangeEnd`,pd=`labelId`,md=`createCodeEvaluator`,hd=`createLlmEvaluator`,gd=[{key:`15m`,label:`Last 15 Min`},{key:`1h`,label:`Last Hour`},{key:`12h`,label:`Last 12 Hours`},{key:`1d`,label:`Last Day`},{key:`7d`,label:`Last 7 Days`},{key:`30d`,label:`Last Month`}],_d=gd.reduce((e,t)=>({...e,[t.key]:t}),{}),vd=6e4,yd=60*vd,bd=24*yd,xd=/^(\d+)([mhd])$/;function Sd(e){if(typeof e!=`string`)return null;let t=xd.exec(e);if(!t)return null;let n=parseInt(t[1],10);return n<1?null:{quantity:n,unit:t[2]}}function Cd({quantity:e,unit:t}){switch(t){case`m`:return e*vd;case`h`:return e*yd;case`d`:return e*bd;default:return dr(t)}}function wd(e,t=Date.now()){let n=Sd(e);if(!n)throw Error(`Invalid last N time range key: ${e}`);let{quantity:r,unit:i}=n,a;switch(i){case`m`:a=Me(t,r);break;case`h`:a=ze(t,r);break;case`d`:a=P(t,r);break;default:dr(i)}return{start:(Cd(n)<=yd?Le:x)(a),end:null}}function Td(e){let t=Sd(e),n=t&&Cd(t)<=yd?vd:yd,r=Date.now()%n;return r===0?n:n-r}function Ed(e){return Sd(e)!==null}function Dd(e){if(e==null||e.trim()===``)return null;let t=new Date(e);return Number.isNaN(t.getTime())?void 0:t}function Od(e,t=Date.now()){let n=e.get(ud);if(Ed(n))return{timeRangeKey:n,...wd(n,t)};let r=Dd(e.get(dd)),i=Dd(e.get(fd));return r===void 0||i===void 0||r==null&&i==null||r!=null&&i!=null&&r>i?null:{timeRangeKey:`custom`,start:r,end:i}}function kd({searchParams:e,timeRange:t}){let n=new URLSearchParams(e),r=(e,t)=>{t==null?n.delete(e):n.set(e,t.toISOString())};return Ed(t.timeRangeKey)?(n.set(ud,t.timeRangeKey),n.delete(dd),n.delete(fd),n):(n.delete(ud),r(dd,t.start),r(fd,t.end),n)}function Ad(e){let t=kd({searchParams:new URLSearchParams,timeRange:e}).toString();return t?`?${t}`:``}var jd={m:{singular:`minute`,plural:`minutes`},h:{singular:`hour`,plural:`hours`},d:{singular:`day`,plural:`days`}};function Md(e){let t=_d[e];if(t)return t.label;let n=Sd(e);if(!n)return e;let{quantity:r,unit:i}=n,{singular:a,plural:o}=jd[i];return`Last ${r} ${r===1?a:o}`}var Nd=/^(?:last\s+)?(\d+)\s*(m|min|mins|minute|minutes|h|hr|hrs|hour|hours|d|day|days)$/,Pd=/^(?:last\s+)?(\d+)$/;function Fd(e){let t=Nd.exec(e.trim().toLowerCase());if(!t)return null;let n=parseInt(t[1],10);return n<1?null:`${n}${t[2][0]}`}function Id(e){let t=Fd(e);if(t)return[t];let n=Pd.exec(e.trim().toLowerCase());if(!n)return[];let r=parseInt(n[1],10);return r<1?[]:[`${r}m`,`${r}h`,`${r}d`]}var Ld=.5,Rd=2,zd=vd;function Bd({value:e,now:t}){if(!e.start)return null;let n=e.start.getTime(),r=(e.end??t).getTime(),i=r-n;return i<=0?null:{startMs:n,endMs:r,durationMs:i}}function Vd(e){let t=Math.max(1,Math.round(e/vd)),n=t/1440;if(n>=2||Number.isInteger(n))return`${Math.round(n)}d`;let r=t/60;return r>=2||Number.isInteger(r)?`${Math.round(r)}h`:`${t}m`}function Hd({value:e,now:t=new Date,shiftFraction:n=Ld}){let r=Bd({value:e,now:t});if(!r)return null;let i=r.durationMs*n;return{timeRangeKey:`custom`,start:new Date(r.startMs-i),end:new Date(r.endMs-i)}}function Ud({value:e,now:t=new Date,shiftFraction:n=Ld}){if(!e.end)return null;let r=Bd({value:e,now:t});if(!r)return null;let i=Math.min(r.durationMs*n,t.getTime()-r.endMs);return i<=0?null:{timeRangeKey:`custom`,start:new Date(r.startMs+i),end:new Date(r.endMs+i)}}function Wd({value:e,now:t=new Date,zoomFactor:n=Rd,minWindowMs:r=zd}){return Kd({value:e,now:t,factor:1/n,minWindowMs:r})}function Gd({value:e,now:t=new Date,zoomFactor:n=Rd,minWindowMs:r=zd}){return Kd({value:e,now:t,factor:n,minWindowMs:r})}function Kd({value:e,now:t,factor:n,minWindowMs:r}){if(!e.end){let i=Sd(e.timeRangeKey),a=i?Cd(i):Bd({value:e,now:t})?.durationMs;if(a==null)return null;let o=Math.max(a*n,r);if(n<1&&o>=a)return null;let s=Vd(o);return s===e.timeRangeKey?null:{timeRangeKey:s,...wd(s)}}let i=Bd({value:e,now:t});if(!i)return null;let a=Math.max(i.durationMs*n,r);if(n<1?a>=i.durationMs:a===i.durationMs)return null;let o=(i.startMs+i.endMs)/2,s=o-a/2,c=o+a/2,l=c-t.getTime();return l>0&&(s-=l,c-=l),{timeRangeKey:`custom`,start:new Date(s),end:new Date(c)}}function qd(e,t){return e?Se(e,t):null}var Jd=G`
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
`,Yd=G`
  .react-aria-DateInput {
    width: 100%;
    min-width: 0;
  }
`,Xd=new L(0,0,0),Zd=new L(23,59,59);function Qd(e){let t=(0,X.c)(56),{value:n,timeZone:r,onApply:i,onCancel:a}=e,o;t[0]!==r||t[1]!==n.start?(o=()=>qd(n.start,r),t[0]=r,t[1]=n.start,t[2]=o):o=t[2];let[s,c]=(0,Y.useState)(o),l;t[3]!==r||t[4]!==n.end?(l=()=>qd(n.end,r)??me(r),t[3]=r,t[4]=n.end,t[5]=l):l=t[5];let[u,d]=(0,Y.useState)(l),f;t[6]!==s||t[7]!==r?(f=s?s.toDate(r):null,t[6]=s,t[7]=r,t[8]=f):f=t[8];let p=f,m;t[9]!==u||t[10]!==r?(m=u?u.toDate(r):null,t[9]=u,t[10]=r,t[11]=m):m=t[11];let h=m,g=!!(p&&h&&p>h),_;t[12]!==h||t[13]!==g||t[14]!==p?(_=p&&h&&!g?{start:p,end:h}:null,t[12]=h,t[13]=g,t[14]=p,t[15]=_):_=t[15];let v=_,y;t[16]!==u||t[17]!==g||t[18]!==s?(y=s&&u&&!g?{start:te(s),end:te(u)}:null,t[16]=u,t[17]=g,t[18]=s,t[19]=y):y=t[19];let b=y,x;t[20]===Symbol.for(`react.memo_cache_sentinel`)?(x={months:2},t[20]=x):x=t[20];let S;t[21]===r?S=t[22]:(S=e=>{e&&(c(Ae(ie(e.start,Xd),r)),d(Ae(ie(e.end,Zd),r)))},t[21]=r,t[22]=S);let C;t[23]!==b||t[24]!==S?(C=U(Yu,{"aria-label":`Time range`,visibleDuration:x,value:b,onChange:S}),t[23]=b,t[24]=S,t[25]=C):C=t[25];let w,T;t[26]===Symbol.for(`react.memo_cache_sentinel`)?(T=U(bn,{children:`Start`}),w=U(Be,{children:ef}),t[26]=w,t[27]=T):(w=t[26],T=t[27]);let E;t[28]===s?E=t[29]:(E=W(Ju,{granularity:`minute`,hideTimeZone:!0,value:s,onChange:c,css:Yd,children:[T,w]}),t[28]=s,t[29]=E);let D,O;t[30]===Symbol.for(`react.memo_cache_sentinel`)?(D=U(bn,{children:`End`}),O=U(Be,{children:$d}),t[30]=D,t[31]=O):(D=t[30],O=t[31]);let k;t[32]!==u||t[33]!==g?(k=W(Ju,{granularity:`minute`,hideTimeZone:!0,isInvalid:g,value:u,onChange:d,css:Yd,children:[D,O]}),t[32]=u,t[33]=g,t[34]=k):k=t[34];let A;t[35]!==E||t[36]!==k?(A=W(`div`,{className:`time-range-calendar-picker__fields`,children:[E,k]}),t[35]=E,t[36]=k,t[37]=A):A=t[37];let j;t[38]===g?j=t[39]:(j=g&&U(B,{size:`XS`,color:`danger`,className:`time-range-calendar-picker__error`,children:`End must be after the start`}),t[38]=g,t[39]=j);let M;t[40]===a?M=t[41]:(M=U(Mt,{size:`S`,onPress:a,children:`Cancel`}),t[40]=a,t[41]=M);let N=!v,P;t[42]!==v||t[43]!==i?(P=()=>{v&&i(v)},t[42]=v,t[43]=i,t[44]=P):P=t[44];let F;t[45]!==N||t[46]!==P?(F=U(Mt,{"data-testid":`time-range-calendar-picker-apply-button`,size:`S`,variant:`primary`,isDisabled:N,onPress:P,children:`Apply`}),t[45]=N,t[46]=P,t[47]=F):F=t[47];let I;t[48]!==j||t[49]!==M||t[50]!==F?(I=W(`div`,{className:`time-range-calendar-picker__controls`,children:[j,M,F]}),t[48]=j,t[49]=M,t[50]=F,t[51]=I):I=t[51];let L;return t[52]!==A||t[53]!==I||t[54]!==C?(L=W(`div`,{"data-testid":`time-range-calendar-picker`,className:`time-range-calendar-picker`,css:Jd,children:[C,A,I]}),t[52]=A,t[53]=I,t[54]=C,t[55]=L):L=t[55],L}function $d(e){return U(y,{segment:e})}function ef(e){return U(y,{segment:e})}var tf=`set_time_range`,nf=[`15m`,`1h`,`12h`,`1d`,`7d`,`30d`,`custom`];function rf(e){return typeof e==`string`&&nf.includes(e)}function af(e){if(typeof e!=`object`||!e)return null;let t=e;return!rf(t.timeRangeKey)||t.startTime!==void 0&&typeof t.startTime!=`string`||t.endTime!==void 0&&typeof t.endTime!=`string`?null:{timeRangeKey:t.timeRangeKey,...t.startTime===void 0?{}:{startTime:t.startTime},...t.endTime===void 0?{}:{endTime:t.endTime}}}function of(e,t){return typeof e==`function`?e(t):e}function sf(e){return{name:e.name,uiBehavior:e.uiBehavior,requiredCapabilities:e.requiredCapabilities,rehydratable:e.rehydratable,dispatch:async t=>{let n=e.parseInput(t.toolCall.input);if(n==null){await t.addToolOutput({state:`output-error`,tool:e.name,toolCallId:t.toolCall.toolCallId,errorText:of(e.invalidInputErrorText,t.toolCall.input)});return}await e.execute({...t,input:n})}}}async function cf({toolName:e,toolCall:t,sessionId:n,addToolOutput:r,errorText:i}){return n??(await r({state:`output-error`,tool:e,toolCallId:t.toolCallId,errorText:i}),null)}async function lf({result:e,toolName:t,toolCallId:n,addToolOutput:r,defaultSuccessOutput:i,emitSuccess:a}){if(e.ok){if(!a)return;await r({state:`output-available`,tool:t,toolCallId:n,output:e.output??i});return}await r({state:`output-error`,tool:t,toolCallId:n,errorText:e.error})}function uf(e){let t=e.emitSuccess??!0,n=e.defaultSuccessOutput??`Done.`;return sf({name:e.name,parseInput:e.parseInput,invalidInputErrorText:e.invalidInputErrorText,requiredCapabilities:e.requiredCapabilities,uiBehavior:e.uiBehavior,execute:async({toolCall:r,input:i,sessionId:a,addToolOutput:o,agentStore:s})=>{let c=s.getState().registeredClientActions[e.name];if(!c){await o({state:`output-error`,tool:e.name,toolCallId:r.toolCallId,errorText:e.notMountedErrorText});return}e.requireSession&&await cf({toolName:e.name,toolCall:r,sessionId:a,addToolOutput:o,errorText:e.noSessionErrorText??`Cannot run this tool without an active session.`})==null||await lf({result:e.buildContext?await c(i,e.buildContext({toolCall:r,sessionId:a,addToolOutput:o,agentStore:s})):await c(i),toolName:e.name,toolCallId:r.toolCallId,addToolOutput:o,defaultSuccessOutput:n,emitSuccess:t})}})}var df=uf({name:tf,parseInput:af,invalidInputErrorText:`Invalid ${tf} input. Expected { timeRangeKey: ${nf.map(e=>`"${e}"`).join(` | `)}, startTime?: string, endTime?: string }.`,notMountedErrorText:`The app time range selector is not mounted on this page; cannot update the time range.`,defaultSuccessOutput:`Time range updated.`});function ff(e){switch(e.type){case`app`:return`app`;case`playground`:return`playground`;case`code_evaluator`:return e.evaluatorNodeId?`code_evaluator:${e.evaluatorNodeId}`:`code_evaluator:create`;case`llm_evaluator`:return e.evaluatorNodeId?`llm_evaluator:${e.evaluatorNodeId}`:`llm_evaluator:create`;case`dataset`:return e.datasetVersionNodeId?`dataset:${e.datasetNodeId}:${e.datasetVersionNodeId}`:`dataset:${e.datasetNodeId}`;case`project`:return`project:${e.projectNodeId}`;case`trace`:return`trace:${e.projectNodeId}:${e.otelTraceId}`;case`session`:return`session:${e.projectNodeId}:${e.sessionNodeId}`;case`prompt`:return`prompt:${e.promptNodeId}`;case`prompt_version`:return`prompt_version:${e.promptNodeId}:${e.promptVersionNodeId}`;case`span`:return`span:${e.projectNodeId??``}:${e.spanNodeId?`node:${e.spanNodeId}`:`otel:${e.otelSpanId}`}`;case`graphql`:return`graphql`;case`web_access`:return`web_access`;case`subagents`:return`subagents`;default:return dr(e)}}var pf={"graphql.mutations":!1,"subagents.enabled":!1,"web.access":!1},mf=[{key:`graphql.mutations`,label:`Dangerously enable mutations`,description:`Allows the phoenix-gql bash command to execute GraphQL mutations in addition to queries.`,defaultValue:!1,scope:`global`,controlSurface:`experimental-settings`},{key:`subagents.enabled`,label:`Subagents`,description:`Lets the assistant delegate work to subagents that run their own tool-using turns. Experimental and may consume large numbers of tokens.`,defaultValue:!1,scope:`global`},{key:`web.access`,label:`Web search`,description:`Lets the assistant use provider-native web search and URL fetching when the selected model supports it.`,defaultValue:!1,scope:`global`}],hf=Object.fromEntries(mf.map(e=>[e.key,e]));for(let e of Object.keys(pf))if(!hf[e])throw Error(`Missing AGENT_CAPABILITY_DEFINITIONS entry for capability key: "${e}"`);function gf(){return{...pf}}function _f(e){return hf[e]}function vf(e){return mf.filter(t=>t.controlSurface===e)}function yf(e){return e.map(e=>e.toLowerCase())}var bf=[`NONE`,`MINIMAL`,`LOW`,`MEDIUM`,`HIGH`,`XHIGH`],xf=yf(bf),Sf=Object.fromEntries(bf.map(e=>[e,e.toLowerCase()]));function Cf(e){return e in Sf}function wf(e){if(typeof e!=`string`)return;let t=e.trim();if(!t)return;let n=t.toUpperCase();if(Cf(n))return n}function Tf(e){let t=wf(e);if(t!=null)return Sf[t]}var Ef=[`disabled`,`enabled`,`adaptive`],Df=[`SUMMARIZED`,`OMITTED`],Of=yf(Df),kf=[`LOW`,`MEDIUM`,`HIGH`,`XHIGH`,`MAX`],Af=yf(kf),jf=[`MINIMAL`,`LOW`,`MEDIUM`,`HIGH`],Mf=yf(jf),Z={OPENAI:`openai`,ANTHROPIC:`anthropic`,GOOGLE_GENAI:`google_genai`,AWS_BEDROCK:`aws_bedrock`};function Nf(e){switch(e){case`OPENAI`:case`AZURE_OPENAI`:case`DEEPSEEK`:case`XAI`:case`OLLAMA`:case`CEREBRAS`:case`FIREWORKS`:case`GROQ`:case`MOONSHOT`:case`PERPLEXITY`:case`TOGETHER`:return Z.OPENAI;case`ANTHROPIC`:return Z.ANTHROPIC;case`GOOGLE`:return Z.GOOGLE_GENAI;case`AWS`:return Z.AWS_BEDROCK}return dr(e)}var Pf=[{name:`temperature`,type:`float`,min:0,max:2,label:`Temperature`,canonicalName:`TEMPERATURE`},{name:`topP`,type:`float`,min:0,max:1,label:`Top P`,canonicalName:`TOP_P`},{name:`maxCompletionTokens`,type:`int`,label:`Max Completion Tokens`,canonicalName:`MAX_COMPLETION_TOKENS`},{name:`frequencyPenalty`,type:`float`,min:-2,max:2,label:`Frequency Penalty`,applicableOpenAIApiTypes:[`CHAT_COMPLETIONS`]},{name:`presencePenalty`,type:`float`,min:-2,max:2,label:`Presence Penalty`,applicableOpenAIApiTypes:[`CHAT_COMPLETIONS`]},{name:`reasoningEffort`,type:`enum`,values:xf,label:`Reasoning Effort`,canonicalName:`REASONING_EFFORT`},{name:`seed`,type:`int`,label:`Seed`,canonicalName:`RANDOM_SEED`}],Ff=[{name:`maxTokens`,type:`int`,label:`Max Tokens`,required:!0,canonicalName:`MAX_COMPLETION_TOKENS`},{name:`temperature`,type:`float`,min:0,max:1,label:`Temperature`,canonicalName:`TEMPERATURE`},{name:`stopSequences`,type:`string_list`,label:`Stop Sequences`,canonicalName:`STOP_SEQUENCES`},{name:`topP`,type:`float`,min:0,max:1,label:`Top P`,canonicalName:`TOP_P`},{name:`thinkingType`,type:`enum`,values:Ef,label:`Thinking`,canonicalName:`ANTHROPIC_EXTENDED_THINKING`},{name:`thinkingBudgetTokens`,type:`int`,min:1024,label:`Budget Tokens`},{name:`thinkingDisplay`,type:`enum`,values:Of,label:`Thinking Display`},{name:`effort`,type:`enum`,values:Af,label:`Effort`,canonicalName:`REASONING_EFFORT`}],If=[{name:`temperature`,type:`float`,min:0,max:2,label:`Temperature`,canonicalName:`TEMPERATURE`},{name:`maxOutputTokens`,type:`int`,label:`Max Output Tokens`,canonicalName:`MAX_COMPLETION_TOKENS`},{name:`stopSequences`,type:`string_list`,label:`Stop Sequences`,canonicalName:`STOP_SEQUENCES`},{name:`presencePenalty`,type:`float`,label:`Presence Penalty`},{name:`frequencyPenalty`,type:`float`,label:`Frequency Penalty`},{name:`topP`,type:`float`,min:0,max:1,label:`Top P`,canonicalName:`TOP_P`},{name:`topK`,type:`int`,label:`Top K`},{name:`thinkingBudget`,type:`int`,min:0,label:`Thinking Budget`},{name:`thinkingLevel`,type:`enum`,values:Mf,label:`Thinking Level`},{name:`includeThoughts`,type:`bool`,label:`Include Thoughts`}],Lf=[{name:`maxTokens`,type:`int`,label:`Max Tokens`,canonicalName:`MAX_COMPLETION_TOKENS`},{name:`temperature`,type:`float`,min:0,max:1,label:`Temperature`,canonicalName:`TEMPERATURE`},{name:`topP`,type:`float`,min:0,max:1,label:`Top P`,canonicalName:`TOP_P`}];Z.OPENAI,Z.ANTHROPIC,Z.GOOGLE_GENAI,Z.AWS_BEDROCK;var Rf=1024,zf=2e3,Bf={type:`adaptive`,display:`SUMMARIZED`},Vf=`HIGH`,Hf=J().transform(e=>e.toUpperCase()).pipe(tr(Df)).optional().catch(void 0),Uf=J().transform(e=>e.toUpperCase()).pipe(tr(kf)).optional().catch(void 0),Wf=rr(J()).optional().catch(void 0),Gf=ir(J(),or()).optional().catch(void 0),Kf=lr(`type`,[er({type:nr(`disabled`)}),er({type:nr(`enabled`),budgetTokens:q(),display:Hf}),er({type:nr(`adaptive`),display:Hf})]).optional().catch(void 0),qf=lr(`type`,[er({type:nr(`disabled`)}),er({type:nr(`enabled`),budget_tokens:q(),display:Hf}),er({type:nr(`adaptive`),display:Hf})]).optional().catch(void 0);function Jf(e){if(e)switch(e.type){case`disabled`:return{type:`disabled`};case`enabled`:{let t={type:`enabled`,budgetTokens:e.budget_tokens};return e.display!==void 0&&(t.display=e.display),t}case`adaptive`:{let t={type:`adaptive`};return e.display!==void 0&&(t.display=e.display),t}default:return dr(e)}}function Yf(e){return e?.type===`enabled`||e?.type===`adaptive`}function Xf(){return{maxTokens:zf,thinking:Bf,effort:Vf}}function Zf(e){if(e==null)return Ff;let t=Yf(e.thinking);return Ff.flatMap(n=>{let r=`canonicalName`in n?n.canonicalName:null;return t&&(r===`TEMPERATURE`||r===`TOP_P`)?[]:n.name===`thinkingBudgetTokens`?e.thinking?.type===`enabled`?n.type===`int`?[{...n,max:e.maxTokens-1}]:[n]:[]:n.name===`thinkingDisplay`&&!t?[]:[n]})}var Qf=ar({maxTokens:q().optional().catch(void 0),temperature:q().optional().catch(void 0),topP:q().optional().catch(void 0),stopSequences:Wf,thinking:Kf,effort:Uf,extraBody:Gf});function $f(e){let t=Qf.safeParse(e),n=t.success?t.data:{},r={maxTokens:n.maxTokens??2e3};return n.temperature!==void 0&&(r.temperature=n.temperature),n.topP!==void 0&&(r.topP=n.topP),n.stopSequences!==void 0&&(r.stopSequences=[...n.stopSequences]),n.thinking!==void 0&&(r.thinking=n.thinking),n.effort!==void 0&&(r.effort=n.effort),n.extraBody!==void 0&&(r.extraBody={...n.extraBody}),r}function Q(e){if(!Yf(e.thinking)||e.temperature===void 0&&e.topP===void 0)return e;let t={...e};return delete t.temperature,delete t.topP,t}function ep(e){let t=[];if(e.thinking?.type===`enabled`){let n=e.thinking.budgetTokens;n<1024&&t.push(`Thinking budget must be at least ${Rf} (got ${n})`),n>=e.maxTokens&&t.push(`Thinking budget (${n}) must be less than max tokens (${e.maxTokens})`)}return t}function tp(e){switch(e.type){case`disabled`:return{disabled:{disabled:!0}};case`enabled`:return{enabled:{budgetTokens:e.budgetTokens,display:e.display??null}};case`adaptive`:return{adaptive:{display:e.display??null}};default:return dr(e)}}function np(e){let t=Q(e),n=ep(t);if(n.length>0)throw Error(`Cannot serialize Anthropic invocation parameters: ${n.join(`; `)}`);let r={maxTokens:t.maxTokens};return t.temperature!==void 0&&(r.temperature=t.temperature),t.topP!==void 0&&(r.topP=t.topP),t.stopSequences!==void 0&&(r.stopSequences=t.stopSequences),t.thinking!==void 0&&(r.thinking=tp(t.thinking)),t.effort!==void 0&&(r.outputConfig={effort:t.effort}),t.extraBody!==void 0&&(r.extraBody=t.extraBody),{anthropic:r}}function rp(e){if(e.__typename!==`PromptAnthropicInvocationParameters`)throw Error(`anthropicAdapter.fromPromptInvocationParameters called with non-Anthropic typename: ${e.__typename}`);let t={maxTokens:e.anthropicMaxTokens};if(e.temperature!=null&&(t.temperature=e.temperature),e.topP!=null&&(t.topP=e.topP),e.stopSequences!=null&&(t.stopSequences=[...e.stopSequences]),e.outputConfig?.effort!=null&&(t.effort=e.outputConfig.effort),e.thinking)switch(e.thinking.__typename){case`PromptAnthropicThinkingDisabled`:t.thinking={type:`disabled`};break;case`PromptAnthropicThinkingEnabled`:{let n={type:`enabled`,budgetTokens:e.thinking.budgetTokens};e.thinking.enabledDisplay!=null&&(n.display=e.thinking.enabledDisplay),t.thinking=n;break}case`PromptAnthropicThinkingAdaptive`:{let n={type:`adaptive`};e.thinking.adaptiveDisplay!=null&&(n.display=e.thinking.adaptiveDisplay),t.thinking=n;break}case`%other`:break;default:dr(e.thinking)}let n=up(e.extraBody);return n!=null&&(t.extraBody=n),Q(t)}function ip(e){if(e.__typename!==`PromptAnthropicInvocationParameters`)throw Error(`anthropicAdapter.fromPromptInvocationParametersForDisplay called with non-Anthropic typename: ${e.__typename}`);let t={maxTokens:e.anthropicMaxTokens};if(e.temperature!=null&&(t.temperature=e.temperature),e.topP!=null&&(t.topP=e.topP),e.stopSequences!=null&&(t.stopSequences=[...e.stopSequences]),e.outputConfig?.effort!=null&&(t.outputConfig={effort:e.outputConfig.effort}),e.thinking)switch(e.thinking.__typename){case`PromptAnthropicThinkingDisabled`:t.thinking={type:`disabled`};break;case`PromptAnthropicThinkingEnabled`:{let n={type:`enabled`,budgetTokens:e.thinking.budgetTokens};e.thinking.enabledDisplay!=null&&(n.display=e.thinking.enabledDisplay),t.thinking=n;break}case`PromptAnthropicThinkingAdaptive`:{let n={type:`adaptive`};e.thinking.adaptiveDisplay!=null&&(n.display=e.thinking.adaptiveDisplay),t.thinking=n;break}case`%other`:break;default:dr(e.thinking)}let n=up(e.extraBody);return n!=null&&(t.extraBody=n),t}var ap=ar({effort:Uf,format:er({type:nr(`json_schema`),schema:ir(J(),or())}).optional().catch(void 0)}).optional().catch(void 0),op=ar({max_tokens:q().optional().catch(void 0),temperature:q().optional().catch(void 0),top_p:q().optional().catch(void 0),stop_sequences:Wf,thinking:qf,output_config:ap,extra_body:Gf});function sp(e){let t=op.safeParse(e),n=t.success?t.data:{},r={maxTokens:n.max_tokens??2e3};n.temperature!==void 0&&(r.temperature=n.temperature),n.top_p!==void 0&&(r.topP=n.top_p),n.stop_sequences!==void 0&&(r.stopSequences=[...n.stop_sequences]);let i=Jf(n.thinking);if(i!==void 0&&(r.thinking=i),n.output_config?.effort!==void 0&&(r.effort=n.output_config.effort),n.extra_body!==void 0){let e=up(n.extra_body);e!==void 0&&(r.extraBody=e)}let a={},o=n.output_config?.format;return o&&(a.responseFormat={type:`json_schema`,jsonSchema:{name:`response`,schema:o.schema}}),{config:Q(r),promoted:a}}function cp(e,t){switch(t){case`maxTokens`:return e.maxTokens;case`temperature`:return e.temperature;case`topP`:return e.topP;case`stopSequences`:return e.stopSequences;case`thinkingType`:return e.thinking?.type;case`thinkingBudgetTokens`:return e.thinking?.type===`enabled`?e.thinking.budgetTokens:void 0;case`thinkingDisplay`:return e.thinking&&e.thinking.type!==`disabled`?e.thinking.display?.toLowerCase():void 0;case`effort`:return e.effort?.toLowerCase();case`extraBody`:return e.extraBody;default:return}}function lp(e,t,n){switch(t){case`maxTokens`:return typeof n!=`number`||Number.isNaN(n)?e:Q({...e,maxTokens:n});case`temperature`:if(n===void 0){let t={...e};return delete t.temperature,Q(t)}return typeof n!=`number`||Number.isNaN(n)?e:Q({...e,temperature:n});case`topP`:if(n===void 0){let t={...e};return delete t.topP,Q(t)}return typeof n!=`number`||Number.isNaN(n)?e:Q({...e,topP:n});case`stopSequences`:if(n===void 0){let t={...e};return delete t.stopSequences,Q(t)}return Array.isArray(n)?Q({...e,stopSequences:n.map(String)}):e;case`thinkingType`:if(n===void 0){let t={...e};return delete t.thinking,Q(t)}if(n===`disabled`)return Q({...e,thinking:{type:`disabled`}});if(n===`enabled`){let t=e.thinking,n=t?.type===`enabled`?t.budgetTokens:Rf,r=t&&t.type!==`disabled`?t.display:void 0,i={type:`enabled`,budgetTokens:n};r!==void 0&&(i.display=r);let a=e.maxTokens>n?e.maxTokens:n+1;return Q({...e,maxTokens:a,thinking:i})}if(n===`adaptive`){let t=e.thinking,n=t&&t.type!==`disabled`?t.display:void 0,r={type:`adaptive`};return n!==void 0&&(r.display=n),Q({...e,thinking:r})}return e;case`thinkingBudgetTokens`:return e.thinking?.type!==`enabled`||n===void 0||typeof n!=`number`||Number.isNaN(n)?e:Q({...e,thinking:{...e.thinking,budgetTokens:n}});case`thinkingDisplay`:{let t=e.thinking;if(!t||t.type===`disabled`)return e;if(n===void 0){if(t.type===`enabled`){let n={type:`enabled`,budgetTokens:t.budgetTokens};return Q({...e,thinking:n})}return Q({...e,thinking:{type:`adaptive`}})}let r=Hf.safeParse(n);return!r.success||!r.data?e:t.type===`enabled`?Q({...e,thinking:{type:`enabled`,budgetTokens:t.budgetTokens,display:r.data}}):Q({...e,thinking:{type:`adaptive`,display:r.data}})}case`effort`:{if(n===void 0){let t={...e};return delete t.effort,Q(t)}let t=Uf.safeParse(n);return!t.success||!t.data?e:Q({...e,effort:t.data})}case`extraBody`:{if(n===void 0){let t={...e};return delete t.extraBody,Q(t)}let t=up(n);return t===void 0?e:Q({...e,extraBody:t})}default:return e}}function up(e){if(typeof e==`object`&&e&&!Array.isArray(e))return e}var dp={getDefaultConfig:Xf,getVisibleSpecs:Zf,parseConfig:$f,normalize:Q,validateForSubmit:ep,toPromptInput:np,fromPromptInvocationParameters:rp,fromPromptInvocationParametersForDisplay:ip,fromSpanInvocationParameters:sp,readField:cp,writeField:lp};function fp(e){return _r(e)&&!Array.isArray(e)}function pp({str:e,excludePrimitives:t=!1,excludeArray:n=!1,excludeNull:r=!1}){try{let i=JSON.parse(e);if(t&&typeof i!=`object`||n&&Array.isArray(i)||r&&i===null)return!1}catch{return!1}return!0}function mp(e){return pp({str:e,excludeArray:!0,excludePrimitives:!0})}function hp(e){try{return{json:JSON.parse(e)}}catch(e){return{json:null,parseError:e}}}function gp(...e){try{return{json:JSON.stringify(...e)}}catch(e){return{json:null,stringifyError:e}}}function _p(e){if(typeof e==`string`){let t=kp(e);return t===void 0?e:_p(t)}return Array.isArray(e)?e.map(_p):typeof e==`object`&&e?Object.fromEntries(Object.entries(e).map(([e,t])=>[e,_p(t)])):e}function vp(e){return typeof e==`string`?kp(e)!==void 0:Array.isArray(e)?e.some(vp):typeof e==`object`&&e?Object.values(e).some(vp):!1}var yp=`.`;function bp({parentKey:e,index:t,indexNotation:n}){return n===`bracket`?`${e}[${t}]`:e?`${e}${yp}${t}`:String(t)}function xp({value:e,indexNotation:t=`bracket`,parentKey:n=``}){return Array.isArray(e)&&e.length>0?e.flatMap((e,r)=>xp({value:e,indexNotation:t,parentKey:bp({parentKey:n,index:r,indexNotation:t})})):fp(e)&&Object.keys(e).length>0?Object.entries(e).flatMap(([e,r])=>xp({value:r,indexNotation:t,parentKey:n?`${n}${yp}${e}`:e})):n===``?[]:[{key:n,value:e}]}function Sp(e){return typeof e==`string`?e:gp(e).json??String(e)}function Cp({entries:e,query:t}){let n=t.trim().toLowerCase();return n?e.filter(({key:e,value:t})=>e.toLowerCase().includes(n)||Sp(t).toLowerCase().includes(n)):e}function wp({obj:e,parentKey:t=``,separator:n=`.`,keepNonTerminalValues:r=!1,formatIndices:i=!1}){let a={};for(let[o,s]of Object.entries(e)){let c;c=i&&Array.isArray(e)?t?`${t}[${o}]`:`[${o}]`:t?`${t}${n}${o}`:o,s&&typeof s==`object`?(r&&(a[c]=s),Object.assign(a,wp({obj:s,parentKey:c,separator:n,keepNonTerminalValues:r,formatIndices:i}))):a[c]=s}return a}function Tp(e,t=`.`){try{let n=JSON.parse(e);return typeof n==`object`?wp({obj:n,separator:t}):{}}catch{}return{}}function Ep(e,t){let n=t?.unquotePlainString??!1;if(typeof e==`string`){let t=e.startsWith(`"{`)||e.startsWith(`"[`)||e.startsWith(`"\\"`);try{if(t){let t=JSON.parse(e),n=typeof t==`string`?JSON.parse(t):t;return JSON.stringify(n,null,2)}}catch{}return n?e:JSON.stringify(e)}try{let t=JSON.stringify(e,null,2);if(t!==void 0)return t}catch{}return String(e)}function Dp(e){if(e!=null)try{return JSON.stringify(e)}catch{return}}function Op(e){if(e.trim())try{return JSON.parse(e)}catch{return}}function kp(e){let t=Op(e);if(!(typeof t!=`object`||!t))return t}function Ap(e){if(e==null)return``;if(Array.isArray(e))return e.length>0?e.map(Ap):[];if(typeof e==`object`){let t={};for(let n in e)t[n]=Ap(e[n]);return t}return typeof e==`string`?``:typeof e==`number`||typeof e==`boolean`?e:``}function jp(e){try{let t=Ap(JSON.parse(e));return JSON.stringify(t,null,2)}catch{return`{
  
}`}}function Mp(e){if(!_r(e))return{value:e,wasUnnested:!1};let t=Object.keys(e);if(t.length!==1)return{value:e,wasUnnested:!1};let n=e[t[0]];return typeof n==`string`?{value:n,wasUnnested:!0}:{value:e,wasUnnested:!1}}function Np(){return{maxTokens:1024,temperature:1}}function Pp(){return Lf}var Fp=ar({maxTokens:q().optional().catch(void 0),temperature:q().optional().catch(void 0),topP:q().optional().catch(void 0),stopSequences:rr(J()).optional().catch(void 0)});function Ip(e){let t=Fp.safeParse(e),n=t.success?t.data:{},r={};return n.maxTokens!==void 0&&(r.maxTokens=n.maxTokens),n.temperature!==void 0&&(r.temperature=n.temperature),n.topP!==void 0&&(r.topP=n.topP),n.stopSequences!==void 0&&(r.stopSequences=[...n.stopSequences]),r}function Lp(e){return e}function Rp(e){return[]}function zp(e){let t=Lp(e),n={};return t.maxTokens!==void 0&&(n.maxTokens=t.maxTokens),t.temperature!==void 0&&(n.temperature=t.temperature),t.topP!==void 0&&(n.topP=t.topP),t.stopSequences!==void 0&&(n.stopSequences=t.stopSequences),{aws:n}}function Bp(e){if(e.__typename!==`PromptAwsInvocationParameters`)throw Error(`awsAdapter.fromPromptInvocationParameters called with non-AWS typename: ${e.__typename}`);let t={};return e.awsMaxTokens!=null&&(t.maxTokens=e.awsMaxTokens),e.temperature!=null&&(t.temperature=e.temperature),e.topP!=null&&(t.topP=e.topP),e.stopSequences!=null&&(t.stopSequences=[...e.stopSequences]),Lp(t)}function Vp(e){if(e.__typename!==`PromptAwsInvocationParameters`)throw Error(`awsAdapter.fromPromptInvocationParametersForDisplay called with non-AWS typename: ${e.__typename}`);let t={};return e.awsMaxTokens!=null&&(t.maxTokens=e.awsMaxTokens),e.temperature!=null&&(t.temperature=e.temperature),e.topP!=null&&(t.topP=e.topP),e.stopSequences!=null&&(t.stopSequences=[...e.stopSequences]),t}var Hp=er({maxTokens:q().optional().catch(void 0),temperature:q().optional().catch(void 0),topP:q().optional().catch(void 0),stopSequences:rr(J()).optional().catch(void 0)}).optional().catch(void 0),Up=er({schema:sr([J(),ir(J(),or())]).optional(),name:J().optional(),description:J().optional()}).optional().catch(void 0),Wp=er({textFormat:er({structure:er({jsonSchema:Up}).optional().catch(void 0)}).optional().catch(void 0)}).optional().catch(void 0),Gp=ar({maxTokens:q().optional().catch(void 0),temperature:q().optional().catch(void 0),topP:q().optional().catch(void 0),stopSequences:rr(J()).optional().catch(void 0),inferenceConfig:Hp,outputConfig:Wp});function Kp(e){let t=Gp.safeParse(e),n=t.success?t.data:{},r={};n.maxTokens===void 0?n.inferenceConfig?.maxTokens!==void 0&&(r.maxTokens=n.inferenceConfig.maxTokens):r.maxTokens=n.maxTokens,n.temperature===void 0?n.inferenceConfig?.temperature!==void 0&&(r.temperature=n.inferenceConfig.temperature):r.temperature=n.temperature,n.topP===void 0?n.inferenceConfig?.topP!==void 0&&(r.topP=n.inferenceConfig.topP):r.topP=n.topP,n.stopSequences===void 0?n.inferenceConfig?.stopSequences!==void 0&&(r.stopSequences=[...n.inferenceConfig.stopSequences]):r.stopSequences=[...n.stopSequences];let i={},a=n.outputConfig?.textFormat?.structure?.jsonSchema;if(a?.schema!=null){let e=null;if(typeof a.schema==`string`){let{json:t}=hp(a.schema);typeof t==`object`&&t&&!Array.isArray(t)&&(e=t)}else typeof a.schema==`object`&&!Array.isArray(a.schema)&&(e=a.schema);if(e!=null){let t={name:typeof a.name==`string`?a.name:`response`,schema:e};typeof a.description==`string`&&(t.description=a.description),i.responseFormat={type:`json_schema`,jsonSchema:t}}}return{config:Lp(r),promoted:i}}function qp(e,t){switch(t){case`maxTokens`:return e.maxTokens;case`temperature`:return e.temperature;case`topP`:return e.topP;case`stopSequences`:return e.stopSequences;default:return}}function Jp(e,t,n){switch(t){case`maxTokens`:case`temperature`:case`topP`:if(n===void 0){let n={...e};return delete n[t],Lp(n)}return typeof n!=`number`||Number.isNaN(n)?e:Lp({...e,[t]:n});case`stopSequences`:if(n===void 0){let t={...e};return delete t.stopSequences,Lp(t)}return Array.isArray(n)?Lp({...e,stopSequences:n.map(String)}):e;default:return e}}var Yp={getDefaultConfig:Np,getVisibleSpecs:Pp,parseConfig:Ip,normalize:Lp,validateForSubmit:Rp,toPromptInput:zp,fromPromptInvocationParameters:Bp,fromPromptInvocationParametersForDisplay:Vp,fromSpanInvocationParameters:e=>Kp(e),readField:qp,writeField:Jp};function Xp(){return{temperature:1,presencePenalty:0,frequencyPenalty:0,thinkingConfig:{thinkingLevel:`MEDIUM`,includeThoughts:!0}}}function Zp(){return If}var Qp=J().transform(e=>e.toUpperCase()).pipe(tr(jf)).optional().catch(void 0),$p=ar({thinkingBudget:q().optional().catch(void 0),thinkingLevel:Qp,includeThoughts:cr().optional().catch(void 0)}).optional().catch(void 0),em=ar({temperature:q().optional().catch(void 0),maxOutputTokens:q().optional().catch(void 0),stopSequences:rr(J()).optional().catch(void 0),presencePenalty:q().optional().catch(void 0),frequencyPenalty:q().optional().catch(void 0),topP:q().optional().catch(void 0),topK:q().optional().catch(void 0),thinkingConfig:$p});function tm(e){let t=em.safeParse(e),n=t.success?t.data:{},r={};return n.temperature!==void 0&&(r.temperature=n.temperature),n.maxOutputTokens!==void 0&&(r.maxOutputTokens=n.maxOutputTokens),n.stopSequences!==void 0&&(r.stopSequences=[...n.stopSequences]),n.presencePenalty!==void 0&&(r.presencePenalty=n.presencePenalty),n.frequencyPenalty!==void 0&&(r.frequencyPenalty=n.frequencyPenalty),n.topP!==void 0&&(r.topP=n.topP),n.topK!==void 0&&(r.topK=n.topK),n.thinkingConfig!==void 0&&n.thinkingConfig!==null&&(r.thinkingConfig=nm(n.thinkingConfig)),r}function nm(e){let t={};return e.thinkingBudget!==void 0&&(t.thinkingBudget=e.thinkingBudget),e.thinkingLevel!==void 0&&(t.thinkingLevel=e.thinkingLevel),e.includeThoughts!==void 0&&(t.includeThoughts=e.includeThoughts),t}function rm(e){return e}function im(e){return[]}function am(e){let t={};return e.thinkingBudget!==void 0&&(t.thinkingBudget=e.thinkingBudget),e.thinkingLevel!==void 0&&(t.thinkingLevel=e.thinkingLevel),e.includeThoughts!==void 0&&(t.includeThoughts=e.includeThoughts),Object.keys(t).length>0?t:void 0}function om(e){let t=rm(e),n={};if(t.temperature!==void 0&&(n.temperature=t.temperature),t.maxOutputTokens!==void 0&&(n.maxOutputTokens=t.maxOutputTokens),t.stopSequences!==void 0&&(n.stopSequences=t.stopSequences),t.presencePenalty!==void 0&&(n.presencePenalty=t.presencePenalty),t.frequencyPenalty!==void 0&&(n.frequencyPenalty=t.frequencyPenalty),t.topP!==void 0&&(n.topP=t.topP),t.topK!==void 0&&(n.topK=t.topK),t.thinkingConfig!==void 0){let e=am(t.thinkingConfig);e&&(n.thinkingConfig=e)}return{google:n}}function sm(e){if(e.__typename!==`PromptGoogleInvocationParameters`)throw Error(`googleAdapter.fromPromptInvocationParameters called with non-Google typename: ${e.__typename}`);let t={};if(e.temperature!=null&&(t.temperature=e.temperature),e.maxOutputTokens!=null&&(t.maxOutputTokens=e.maxOutputTokens),e.stopSequences!=null&&(t.stopSequences=[...e.stopSequences]),e.presencePenalty!=null&&(t.presencePenalty=e.presencePenalty),e.frequencyPenalty!=null&&(t.frequencyPenalty=e.frequencyPenalty),e.topP!=null&&(t.topP=e.topP),e.topK!=null&&(t.topK=e.topK),e.thinkingConfig){let n={};e.thinkingConfig.thinkingBudget!=null&&(n.thinkingBudget=e.thinkingConfig.thinkingBudget),e.thinkingConfig.thinkingLevel!=null&&(n.thinkingLevel=e.thinkingConfig.thinkingLevel),e.thinkingConfig.includeThoughts!=null&&(n.includeThoughts=e.thinkingConfig.includeThoughts),Object.keys(n).length>0&&(t.thinkingConfig=n)}return rm(t)}function cm(e){if(e.__typename!==`PromptGoogleInvocationParameters`)throw Error(`googleAdapter.fromPromptInvocationParametersForDisplay called with non-Google typename: ${e.__typename}`);let t={};if(e.temperature!=null&&(t.temperature=e.temperature),e.maxOutputTokens!=null&&(t.maxOutputTokens=e.maxOutputTokens),e.stopSequences!=null&&(t.stopSequences=[...e.stopSequences]),e.presencePenalty!=null&&(t.presencePenalty=e.presencePenalty),e.frequencyPenalty!=null&&(t.frequencyPenalty=e.frequencyPenalty),e.topP!=null&&(t.topP=e.topP),e.topK!=null&&(t.topK=e.topK),e.thinkingConfig){let n={};e.thinkingConfig.thinkingBudget!=null&&(n.thinkingBudget=e.thinkingConfig.thinkingBudget),e.thinkingConfig.thinkingLevel!=null&&(n.thinkingLevel=e.thinkingConfig.thinkingLevel),e.thinkingConfig.includeThoughts!=null&&(n.includeThoughts=e.thinkingConfig.includeThoughts),Object.keys(n).length>0&&(t.thinkingConfig=n)}return t}var lm=ar({thinking_budget:q().optional().catch(void 0),thinking_level:Qp,include_thoughts:cr().optional().catch(void 0)}).optional().catch(void 0),um=ar({temperature:q().optional().catch(void 0),max_output_tokens:q().optional().catch(void 0),stop_sequences:rr(J()).optional().catch(void 0),presence_penalty:q().optional().catch(void 0),frequency_penalty:q().optional().catch(void 0),top_p:q().optional().catch(void 0),top_k:q().optional().catch(void 0),thinking_config:lm,response_json_schema:or().optional(),response_schema:or().optional(),response_mime_type:J().optional().catch(void 0)});function dm(e){let t=um.safeParse(e),n=t.success?t.data:{},r={};if(n.temperature!==void 0&&(r.temperature=n.temperature),n.max_output_tokens!==void 0&&(r.maxOutputTokens=n.max_output_tokens),n.stop_sequences!==void 0&&(r.stopSequences=[...n.stop_sequences]),n.presence_penalty!==void 0&&(r.presencePenalty=n.presence_penalty),n.frequency_penalty!==void 0&&(r.frequencyPenalty=n.frequency_penalty),n.top_p!==void 0&&(r.topP=n.top_p),n.top_k!==void 0&&(r.topK=n.top_k),n.thinking_config){let e={};n.thinking_config.thinking_budget!==void 0&&(e.thinkingBudget=n.thinking_config.thinking_budget),n.thinking_config.thinking_level!==void 0&&(e.thinkingLevel=n.thinking_config.thinking_level),n.thinking_config.include_thoughts!==void 0&&(e.includeThoughts=n.thinking_config.include_thoughts),Object.keys(e).length>0&&(r.thinkingConfig=e)}let i={},a=n.response_json_schema??n.response_schema;return a!=null&&n.response_mime_type===`application/json`&&(i.responseFormat={type:`json_schema`,jsonSchema:{name:`response`,schema:a}}),{config:rm(r),promoted:i}}var fm=new Set([`temperature`,`maxOutputTokens`,`presencePenalty`,`frequencyPenalty`,`topP`,`topK`]);function pm(e){return fm.has(e)}function mm(e){let t={};return e.thinkingBudget!==void 0&&(t.thinkingBudget=e.thinkingBudget),e.thinkingLevel!==void 0&&(t.thinkingLevel=e.thinkingLevel),e.includeThoughts!==void 0&&(t.includeThoughts=e.includeThoughts),Object.keys(t).length===0?void 0:t}function hm(e,t){if(pm(t))return e[t];switch(t){case`stopSequences`:return e.stopSequences;case`thinkingBudget`:return e.thinkingConfig?.thinkingBudget;case`thinkingLevel`:return e.thinkingConfig?.thinkingLevel?.toLowerCase();case`includeThoughts`:return e.thinkingConfig?.includeThoughts;default:return}}function gm(e,t,n){if(pm(t)){if(n===void 0){let n={...e};return delete n[t],rm(n)}return typeof n!=`number`||Number.isNaN(n)?e:rm({...e,[t]:n})}switch(t){case`stopSequences`:if(n===void 0){let t={...e};return delete t.stopSequences,rm(t)}return Array.isArray(n)?rm({...e,stopSequences:n.map(String)}):e;case`thinkingBudget`:{let t={...e.thinkingConfig??{}};if(n===void 0)delete t.thinkingBudget;else if(typeof n==`number`&&!Number.isNaN(n))t.thinkingBudget=n;else return e;return _m(e,t)}case`thinkingLevel`:{let t={...e.thinkingConfig??{}};if(n===void 0)delete t.thinkingLevel;else{let r=Qp.safeParse(n);if(!r.success||!r.data)return e;t.thinkingLevel=r.data}return _m(e,t)}case`includeThoughts`:{let t={...e.thinkingConfig??{}};if(n===void 0)delete t.includeThoughts;else if(typeof n==`boolean`)t.includeThoughts=n;else return e;return _m(e,t)}default:return e}}function _m(e,t){let n=mm(t),r={...e};return n===void 0?delete r.thinkingConfig:r.thinkingConfig=n,rm(r)}var vm={getDefaultConfig:Xp,getVisibleSpecs:Zp,parseConfig:tm,normalize:rm,validateForSubmit:im,toPromptInput:om,fromPromptInvocationParameters:sm,fromPromptInvocationParametersForDisplay:cm,fromSpanInvocationParameters:e=>dm(e),readField:hm,writeField:gm};function ym(e){if(typeof e==`object`&&e&&!Array.isArray(e))return e}function bm(e){return e===0?void 0:e}function xm(){return{frequencyPenalty:0,presencePenalty:0}}function Sm(e,t){let n=t.openaiApiType??`RESPONSES`;return Pf.filter(e=>{let t=`applicableOpenAIApiTypes`in e?e.applicableOpenAIApiTypes:void 0;return t==null||t.includes(n)})}var Cm=ar({temperature:q().optional().catch(void 0),topP:q().optional().catch(void 0),maxCompletionTokens:q().optional().catch(void 0),frequencyPenalty:q().optional().catch(void 0),presencePenalty:q().optional().catch(void 0),reasoningEffort:J().optional().catch(void 0),seed:q().optional().catch(void 0),stop:rr(J()).optional().catch(void 0),extraBody:ir(J(),or()).optional().catch(void 0)});function wm(e){let t=Cm.safeParse(e),n=t.success?t.data:{},r={};if(n.temperature!==void 0&&(r.temperature=n.temperature),n.topP!==void 0&&(r.topP=n.topP),n.maxCompletionTokens!==void 0&&(r.maxCompletionTokens=n.maxCompletionTokens),n.frequencyPenalty!==void 0&&(r.frequencyPenalty=n.frequencyPenalty),n.presencePenalty!==void 0&&(r.presencePenalty=n.presencePenalty),n.reasoningEffort!==void 0){let e=Tf(n.reasoningEffort);e!==void 0&&(r.reasoningEffort=e)}return n.seed!==void 0&&(r.seed=n.seed),n.stop!==void 0&&(r.stop=[...n.stop]),n.extraBody!==void 0&&(r.extraBody={...n.extraBody}),r}function Tm(e){return e}function Em(e){return[]}function Dm(e){let t=Tm(e),n={};t.temperature!==void 0&&(n.temperature=t.temperature),t.topP!==void 0&&(n.topP=t.topP),t.maxCompletionTokens!==void 0&&(n.maxCompletionTokens=t.maxCompletionTokens);let r=bm(t.frequencyPenalty);r!==void 0&&(n.frequencyPenalty=r);let i=bm(t.presencePenalty);if(i!==void 0&&(n.presencePenalty=i),t.reasoningEffort!==void 0){let e=wf(t.reasoningEffort);e!==void 0&&(n.reasoningEffort=e)}return t.seed!==void 0&&(n.seed=t.seed),t.stop!==void 0&&(n.stop=t.stop),t.extraBody!==void 0&&(n.extraBody=t.extraBody),{openai:n}}function Om(e){if(e.__typename!==`PromptOpenAIInvocationParameters`)throw Error(`openaiAdapter.fromPromptInvocationParameters called with non-OpenAI typename: ${e.__typename}`);let t={};if(e.temperature!=null&&(t.temperature=e.temperature),e.topP!=null&&(t.topP=e.topP),e.maxCompletionTokens==null?e.openaiMaxTokens!=null&&(t.maxCompletionTokens=e.openaiMaxTokens):t.maxCompletionTokens=e.maxCompletionTokens,e.frequencyPenalty!=null&&(t.frequencyPenalty=e.frequencyPenalty),e.presencePenalty!=null&&(t.presencePenalty=e.presencePenalty),e.seed!=null&&(t.seed=e.seed),e.stop!=null&&(t.stop=[...e.stop]),e.reasoningEffort!=null){let n=Tf(e.reasoningEffort);n!==void 0&&(t.reasoningEffort=n)}let n=ym(e.extraBody);return n!=null&&(t.extraBody=n),Tm(t)}function km(e){if(e.__typename!==`PromptOpenAIInvocationParameters`)throw Error(`openaiAdapter.fromPromptInvocationParametersForDisplay called with non-OpenAI typename: ${e.__typename}`);let t={};e.temperature!=null&&(t.temperature=e.temperature),e.openaiMaxTokens!=null&&(t.maxTokens=e.openaiMaxTokens),e.maxCompletionTokens!=null&&(t.maxCompletionTokens=e.maxCompletionTokens),e.frequencyPenalty!=null&&(t.frequencyPenalty=e.frequencyPenalty),e.presencePenalty!=null&&(t.presencePenalty=e.presencePenalty),e.topP!=null&&(t.topP=e.topP),e.seed!=null&&(t.seed=e.seed),e.stop!=null&&(t.stop=[...e.stop]);let n=Tf(e.reasoningEffort);n!==void 0&&(t.reasoningEffort=n);let r=ym(e.extraBody);return r!=null&&(t.extraBody=r),t}var Am=er({name:J().optional(),schema:or().optional(),strict:cr().nullish(),description:J().nullish()}),jm=er({type:J().optional(),json_schema:Am.optional()}).optional().catch(void 0),Mm=er({type:J().optional(),name:J().optional(),schema:or().optional(),strict:cr().optional(),description:J().optional()}).optional().catch(void 0),Nm=ar({temperature:q().optional().catch(void 0),top_p:q().optional().catch(void 0),max_completion_tokens:q().optional().catch(void 0),max_tokens:q().optional().catch(void 0),max_output_tokens:q().optional().catch(void 0),frequency_penalty:q().optional().catch(void 0),presence_penalty:q().optional().catch(void 0),seed:q().optional().catch(void 0),stop:rr(J()).optional().catch(void 0),reasoning_effort:J().optional().catch(void 0),reasoning:ar({effort:J().optional().catch(void 0)}).optional().catch(void 0),response_format:jm,text:er({format:Mm}).optional().catch(void 0),extra_body:ir(J(),or()).optional().catch(void 0)});function Pm(e,t){let n=Nm.safeParse(e),r=n.success?n.data:{},i={};r.temperature!==void 0&&(i.temperature=r.temperature),r.top_p!==void 0&&(i.topP=r.top_p),r.max_completion_tokens===void 0?r.max_tokens===void 0?t===`RESPONSES`&&r.max_output_tokens!==void 0&&(i.maxCompletionTokens=r.max_output_tokens):i.maxCompletionTokens=r.max_tokens:i.maxCompletionTokens=r.max_completion_tokens,r.frequency_penalty!==void 0&&(i.frequencyPenalty=r.frequency_penalty),r.presence_penalty!==void 0&&(i.presencePenalty=r.presence_penalty),r.seed!==void 0&&(i.seed=r.seed),r.stop!==void 0&&(i.stop=[...r.stop]);let a;if(r.reasoning_effort===void 0?t===`RESPONSES`&&r.reasoning?.effort!==void 0&&(a=r.reasoning.effort):a=r.reasoning_effort,a!==void 0){let e=Tf(a);e!==void 0&&(i.reasoningEffort=e)}r.extra_body!==void 0&&(i.extraBody={...r.extra_body});let o={},s=r.response_format;if(s?.json_schema){let e=s.json_schema,t={name:typeof e.name==`string`?e.name:`response`};e.schema!==void 0&&(t.schema=e.schema),e.strict!==void 0&&e.strict!==null&&(t.strict=e.strict),e.description!==void 0&&e.description!==null&&(t.description=e.description),o.responseFormat={type:`json_schema`,jsonSchema:t}}else if(r.text?.format!==void 0){let e=r.text.format;if(e){let t={name:typeof e.name==`string`?e.name:`response`};e.schema!==void 0&&(t.schema=e.schema),e.strict!==void 0&&(t.strict=e.strict),e.description!==void 0&&(t.description=e.description),o.responseFormat={type:`json_schema`,jsonSchema:t}}}return{config:Tm(i),promoted:o}}var Fm=new Set([`temperature`,`topP`,`maxCompletionTokens`,`frequencyPenalty`,`presencePenalty`,`seed`]);function Im(e){return Fm.has(e)}function Lm(e,t){if(Im(t))return e[t];switch(t){case`reasoningEffort`:return e.reasoningEffort;case`stop`:return e.stop;case`extraBody`:return e.extraBody;default:return}}function Rm(e,t,n){if(Im(t)){if(n===void 0){let n={...e};return delete n[t],Tm(n)}return typeof n!=`number`||Number.isNaN(n)?e:Tm({...e,[t]:n})}switch(t){case`reasoningEffort`:if(n===void 0){let t={...e};return delete t.reasoningEffort,Tm(t)}return typeof n==`string`?Tm({...e,reasoningEffort:n}):e;case`stop`:if(n===void 0){let t={...e};return delete t.stop,Tm(t)}return Array.isArray(n)?Tm({...e,stop:n.map(String)}):e;case`extraBody`:{if(n===void 0){let t={...e};return delete t.extraBody,Tm(t)}let t=ym(n);return t===void 0?e:Tm({...e,extraBody:t})}default:return e}}var zm={getDefaultConfig:xm,getVisibleSpecs:Sm,parseConfig:wm,normalize:Tm,validateForSubmit:Em,toPromptInput:Dm,fromPromptInvocationParameters:Om,fromPromptInvocationParametersForDisplay:km,fromSpanInvocationParameters:(e,t)=>Pm(e,t?.openaiApiType??null),readField:Lm,writeField:Rm};function Bm(e){switch(e){case Z.OPENAI:return zm;case Z.ANTHROPIC:return dp;case Z.GOOGLE_GENAI:return vm;case Z.AWS_BEDROCK:return Yp;default:return dr(e)}}function Vm(e){return Bm(Nf(e))}function Hm(e){let t=Vm(e);return t.normalize(t.getDefaultConfig())}function Um(e,t){let n=Vm(e);return n.normalize(n.parseConfig(t))}function Wm(e,t){return Vm(e).toPromptInput(t)}function Gm(e,t){if(t==null)return Hm(e);let n=Nf(e);return n===Z.OPENAI&&t.__typename===`PromptOpenAIInvocationParameters`||n===Z.ANTHROPIC&&t.__typename===`PromptAnthropicInvocationParameters`||n===Z.GOOGLE_GENAI&&t.__typename===`PromptGoogleInvocationParameters`||n===Z.AWS_BEDROCK&&t.__typename===`PromptAwsInvocationParameters`?Vm(e).fromPromptInvocationParameters(t):Hm(e)}function Km(e){if(e==null)return null;let t;switch(e.__typename){case`PromptOpenAIInvocationParameters`:t=Z.OPENAI;break;case`PromptAnthropicInvocationParameters`:t=Z.ANTHROPIC;break;case`PromptGoogleInvocationParameters`:t=Z.GOOGLE_GENAI;break;case`PromptAwsInvocationParameters`:t=Z.AWS_BEDROCK;break;case`%other`:throw Error(`Unsupported prompt invocation parameters typename: %other`);default:return dr(e)}let n=Bm(t);return{family:t,parameters:n.fromPromptInvocationParametersForDisplay(e)}}function qm(e,t,n={}){let{config:r,promoted:i}=Vm(e).fromSpanInvocationParameters(t,n);return{invocationParameters:r,responseFormat:i.responseFormat}}function Jm(e,t,n){return Vm(e).readField(t,n)}function Ym(e,t){return Vm(e.provider).getVisibleSpecs(t,{openaiApiType:e.openaiApiType})}function Xm(e,t,n,r){return Vm(e).writeField(t,n,r)}function Zm(e,t){return t?e.isBusyElsewhereBySessionId[t]?`busyElsewhere`:e.sessionNoticeBySessionId[t]??null:null}function Qm(e,t){if(!t)return!1;let n=e.chatStatusBySessionId[t];return n===`submitted`||n===`streaming`||e.isBusyElsewhereBySessionId[t]===!0}var $m=`pxi:draft-session`,eh={provider:`ANTHROPIC`,modelName:`claude-opus-4-6`,invocationParameters:Hm(`ANTHROPIC`)},th={collectorEndpoint:null,assistantProjectName:`assistant_agent`,forceTracing:!1,webAccessEnabled:!1,assistantEnabled:!1,allowLocalTraces:!1,allowRemoteExport:!1,sessionRetentionMaxIdleDays:null,sessionRetentionMaxCountPerUser:null},nh={storeLocalTraces:!0,exportRemoteTraces:!1,attachUserId:!1,acknowledgedTraceConsent:null},rh={edits:`manual`};function ih(e){return{allowLocalTraces:e.allowLocalTraces,allowRemoteExport:!!e.collectorEndpoint&&e.allowRemoteExport}}function ah({agentsConfig:e,observability:t}){if(e.forceTracing)return!0;let n=t.acknowledgedTraceConsent;if(!n)return!1;let r=ih(e);return(!r.allowLocalTraces||n.allowLocalTraces)&&(!r.allowRemoteExport||n.allowRemoteExport)}function oh({agentsConfig:e,observability:t}){if(e.forceTracing)return{ingestTraces:!0,exportRemoteTraces:!0};let n=ih(e);return{ingestTraces:n.allowLocalTraces&&t.storeLocalTraces,exportRemoteTraces:n.allowRemoteExport&&t.exportRemoteTraces}}function sh({agentsConfig:e,observability:t}){return e.forceTracing||t.attachUserId}function ch({capabilities:e,defaultCapabilities:t=gf()}){if(!e||typeof e!=`object`)return{...t};let n=e;return Object.fromEntries(Object.keys(t).map(e=>{let r=n[e];return[e,typeof r==`boolean`?r:t[e]]}))}function lh(e,t){if(!e||typeof e!=`object`)return t;let{sessions:n,activeSessionId:r,sessionMap:i,...a}=e,o=typeof a.defaultTemporaryChat==`boolean`?a.defaultTemporaryChat:t.defaultTemporaryChat;return{...t,...a,defaultTemporaryChat:o,isDraftSessionTemporary:o,observability:{...t.observability,...a.observability},capabilities:ch({capabilities:a.capabilities,defaultCapabilities:t.capabilities})}}function uh(e,t){return Object.fromEntries(Object.entries(e).filter(([,e])=>e?.sessionId!==t))}var dh=`arize-phoenix-assistant`;function fh(){let e=(window.Config?.basename??``).replace(/\/+$/,``);return e?`${dh}:${e}`:dh}var ph=e=>ne()(n(v((t,n)=>({isOpen:!1,position:`pinned`,fabMode:`pinned`,fabPlacement:`bottom-end`,activeSessionId:null,isDraftSessionTemporary:!1,defaultTemporaryChat:!1,defaultModelConfig:{...eh},agentsConfig:th,observability:nh,permissions:rh,capabilities:gf(),routeContexts:[],mountedContexts:{},pendingPromptEditsByToolCallId:{},pendingPromptInstanceRemovalsByToolCallId:{},pendingBatchSpanAnnotatesByToolCallId:{},pendingDatasetWritesByToolCallId:{},pendingAnnotationConfigWritesByToolCallId:{},pendingPatchExperimentsByToolCallId:{},pendingPromptToolWritesByToolCallId:{},pendingSavePromptsByToolCallId:{},pendingCodeEvaluatorEditsByToolCallId:{},pendingLlmEvaluatorEditsByToolCallId:{},pendingLoadDatasetsByToolCallId:{},locallyInterruptedToolCallIds:{},setIsOpen:e=>{t({isOpen:e},!1,{type:`setIsOpen`})},toggleOpen:()=>{t(e=>({isOpen:!e.isOpen}),!1,{type:`toggleOpen`})},setPosition:e=>{t({position:e},!1,{type:`setPosition`})},setFabMode:e=>{t({fabMode:e},!1,{type:`setFabMode`})},setFabPlacement:e=>{t({fabPlacement:e},!1,{type:`setFabPlacement`})},setActiveSession:e=>{t({activeSessionId:e},!1,{type:`setActiveSession`})},setIsDraftSessionTemporary:e=>{t({isDraftSessionTemporary:e},!1,{type:`setIsDraftSessionTemporary`})},setDefaultTemporaryChat:e=>{t({defaultTemporaryChat:e},!1,{type:`setDefaultTemporaryChat`})},clearSessionEphemeralState:e=>{t(t=>{let n={...t.pendingElicitationBySessionId};delete n[e];let r={...t.chatStatusBySessionId};delete r[e];let i={...t.isResponsePendingBySessionId};delete i[e];let a={...t.isCompactionPendingBySessionId};delete a[e];let o={...t.isBusyElsewhereBySessionId};delete o[e];let s={...t.sessionNoticeBySessionId};delete s[e];let c={...t.draftInputBySessionId};delete c[e];let l={...t.pendingMessageBySessionId};return delete l[e],{pendingElicitationBySessionId:n,chatStatusBySessionId:r,isResponsePendingBySessionId:i,isCompactionPendingBySessionId:a,isBusyElsewhereBySessionId:o,sessionNoticeBySessionId:s,draftInputBySessionId:c,pendingMessageBySessionId:l,pendingPatchExperimentsByToolCallId:uh(t.pendingPatchExperimentsByToolCallId,e)}},!1,{type:`clearSessionEphemeralState`})},setDefaultModelConfig:e=>{t({defaultModelConfig:e},!1,{type:`setDefaultModelConfig`})},setObservability:e=>{t(t=>({observability:{...t.observability,...e}}),!1,{type:`setObservability`})},setPermissions:e=>{t(t=>({permissions:{...t.permissions,...e}}),!1,{type:`setPermissions`})},setAgentsConfig:e=>{t(t=>({agentsConfig:{...t.agentsConfig,...e}}),!1,{type:`setAgentsConfig`})},acknowledgeConsent:()=>{t(e=>({observability:{...e.observability,acknowledgedTraceConsent:ih(e.agentsConfig)}}),!1,{type:`acknowledgeConsent`})},setCapability:({key:e,enabled:n})=>{t(t=>({capabilities:{...t.capabilities,[e]:n}}),!1,{type:`setCapability`})},pendingElicitationBySessionId:{},setPendingElicitation:(e,n)=>{t(t=>{let r={...t.pendingElicitationBySessionId};return n?r[e]=n:delete r[e],{pendingElicitationBySessionId:r}},!1,{type:`setPendingElicitation`})},draftInputBySessionId:{},setDraftInput:(e,n)=>{t(t=>{let r={...t.draftInputBySessionId};return n?r[e]=n:delete r[e],{draftInputBySessionId:r}},!1,{type:`setDraftInput`})},pendingMessageBySessionId:{},setPendingMessage:(e,n)=>{t(t=>{let r={...t.pendingMessageBySessionId};return n?r[e]=n:delete r[e],{pendingMessageBySessionId:r}},!1,{type:`setPendingMessage`})},consumePendingMessage:e=>{let r=n().pendingMessageBySessionId[e]??null;return r!=null&&t(t=>{if(!(e in t.pendingMessageBySessionId))return t;let n={...t.pendingMessageBySessionId};return delete n[e],{pendingMessageBySessionId:n}},!1,{type:`consumePendingMessage`}),r},chatStatusBySessionId:{},setSessionChatStatus:(e,n)=>{t(t=>({chatStatusBySessionId:{...t.chatStatusBySessionId,[e]:n}}),!1,{type:`setSessionChatStatus`})},isResponsePendingBySessionId:{},setSessionResponsePending:(e,n)=>{t(t=>{let r={...t.isResponsePendingBySessionId};return n?r[e]=!0:delete r[e],{isResponsePendingBySessionId:r}},!1,{type:`setSessionResponsePending`})},isCompactionPendingBySessionId:{},setSessionCompactionPending:(e,n)=>{t(t=>{let r={...t.isCompactionPendingBySessionId};return n?r[e]=!0:delete r[e],{isCompactionPendingBySessionId:r}},!1,{type:`setSessionCompactionPending`})},isBusyElsewhereBySessionId:{},setSessionBusyElsewhere:(e,n)=>{t(t=>{let r={...t.isBusyElsewhereBySessionId};return n?r[e]=!0:delete r[e],{isBusyElsewhereBySessionId:r}},!1,{type:`setSessionBusyElsewhere`})},sessionNoticeBySessionId:{},setSessionNotice:(e,n)=>{t(t=>{if((t.sessionNoticeBySessionId[e]??null)===n)return t;let r={...t.sessionNoticeBySessionId};return n?r[e]=n:delete r[e],{sessionNoticeBySessionId:r}},!1,{type:`setSessionNotice`})},setRouteContexts:e=>{t(t=>{if(t.routeContexts.length===e.length){let n=!0;for(let r=0;r<e.length;r++)if(ff(t.routeContexts[r])!==ff(e[r])){n=!1;break}if(n)return t}return{routeContexts:e}},!1,{type:`setRouteContexts`})},setMountedContext:(e,n)=>{t(t=>({mountedContexts:{...t.mountedContexts,[e]:n}}),!1,{type:`setMountedContext`})},removeMountedContext:e=>{t(t=>{if(!(e in t.mountedContexts))return t;let n={...t.mountedContexts};return delete n[e],{mountedContexts:n}},!1,{type:`removeMountedContext`})},registeredClientActions:{},registerClientAction:(e,n)=>{t(t=>({registeredClientActions:{...t.registeredClientActions,[e]:n}}),!1,{type:`registerClientAction`})},unregisterClientAction:e=>{t(t=>{if(!(e in t.registeredClientActions))return t;let n={...t.registeredClientActions};return delete n[e],{registeredClientActions:n}},!1,{type:`unregisterClientAction`})},markToolCallInterrupted:e=>{t(t=>t.locallyInterruptedToolCallIds[e]?t:{locallyInterruptedToolCallIds:{...t.locallyInterruptedToolCallIds,[e]:!0}},!1,{type:`markToolCallInterrupted`})},setPendingPromptEdit:(e,n)=>{t(t=>{let r={...t.pendingPromptEditsByToolCallId};return n?r[e]=n:delete r[e],{pendingPromptEditsByToolCallId:r}},!1,{type:`setPendingPromptEdit`})},setPendingPromptInstanceRemoval:(e,n)=>{t(t=>{let r={...t.pendingPromptInstanceRemovalsByToolCallId};return n?r[e]=n:delete r[e],{pendingPromptInstanceRemovalsByToolCallId:r}},!1,{type:`setPendingPromptInstanceRemoval`})},setPendingDatasetWrite:(e,n)=>{t(t=>{let r={...t.pendingDatasetWritesByToolCallId};return n?r[e]=n:delete r[e],{pendingDatasetWritesByToolCallId:r}},!1,{type:`setPendingDatasetWrite`})},setPendingAnnotationConfigWrite:(e,n)=>{t(t=>{let r={...t.pendingAnnotationConfigWritesByToolCallId};return n?r[e]=n:delete r[e],{pendingAnnotationConfigWritesByToolCallId:r}},!1,{type:`setPendingAnnotationConfigWrite`})},setPendingBatchSpanAnnotate:(e,n)=>{t(t=>{let r={...t.pendingBatchSpanAnnotatesByToolCallId};return n?r[e]=n:delete r[e],{pendingBatchSpanAnnotatesByToolCallId:r}},!1,{type:`setPendingBatchSpanAnnotate`})},setPendingPatchExperiment:(e,n)=>{t(t=>{let r={...t.pendingPatchExperimentsByToolCallId};return n?r[e]=n:delete r[e],{pendingPatchExperimentsByToolCallId:r}},!1,{type:`setPendingPatchExperiment`})},setPendingPromptToolWrite:(e,n)=>{t(t=>{let r={...t.pendingPromptToolWritesByToolCallId};return n?r[e]=n:delete r[e],{pendingPromptToolWritesByToolCallId:r}},!1,{type:`setPendingPromptToolWrite`})},setPendingSavePrompt:(e,n)=>{t(t=>{let r={...t.pendingSavePromptsByToolCallId};return n?r[e]=n:delete r[e],{pendingSavePromptsByToolCallId:r}},!1,{type:`setPendingSavePrompt`})},setPendingCodeEvaluatorEdit:(e,n)=>{t(t=>{let r={...t.pendingCodeEvaluatorEditsByToolCallId};return n?r[e]=n:delete r[e],{pendingCodeEvaluatorEditsByToolCallId:r}},!1,{type:`setPendingCodeEvaluatorEdit`})},setPendingLlmEvaluatorEdit:(e,n)=>{t(t=>{let r={...t.pendingLlmEvaluatorEditsByToolCallId};return n?r[e]=n:delete r[e],{pendingLlmEvaluatorEditsByToolCallId:r}},!1,{type:`setPendingLlmEvaluatorEdit`})},setPendingLoadDataset:(e,n)=>{t(t=>{let r={...t.pendingLoadDatasetsByToolCallId};return n?r[e]=n:delete r[e],{pendingLoadDatasetsByToolCallId:r}},!1,{type:`setPendingLoadDataset`})},...e}),{name:`agentStore`}),{name:fh(),version:0,partialize:e=>({isOpen:e.isOpen,position:e.position,fabMode:e.fabMode,fabPlacement:e.fabPlacement,defaultTemporaryChat:e.defaultTemporaryChat,defaultModelConfig:e.defaultModelConfig,observability:e.observability,permissions:e.permissions,capabilities:e.capabilities}),merge:lh}));async function mh({agentStore:e,names:t,timeoutMs:n=5e3}){let r=e=>t.every(t=>t in e);return r(e.getState().registeredClientActions)?!0:new Promise(t=>{let i=!1,a=null,o=e=>{i||(i=!0,a&&clearTimeout(a),s(),t(e))},s=e.subscribe(e=>{r(e.registeredClientActions)&&o(!0)});a=setTimeout(()=>o(!1),n),r(e.getState().registeredClientActions)&&o(!0)})}var hh=(0,Y.createContext)(null);function gh(e){let t=(0,X.c)(8),n,r;t[0]===e?(n=t[1],r=t[2]):({children:n,...r}=e,t[0]=e,t[1]=n,t[2]=r);let i;t[3]===r?i=t[4]:(i=()=>ph(r),t[3]=r,t[4]=i);let[a]=(0,Y.useState)(i),o;return t[5]!==n||t[6]!==a?(o=U(hh.Provider,{value:a,children:n}),t[5]=n,t[6]=a,t[7]=o):o=t[7],o}function _h(e,t){let n=(0,Y.useContext)(hh);if(!n)throw Error(`Missing AgentContext.Provider in the tree`);return ge(n,e,t)}function vh(){let e=(0,Y.useContext)(hh);if(!e)throw Error(`Missing AgentContext.Provider in the tree`);return e}var yh=(0,Y.createContext)(null);function bh(){return Y.useContext(yh)}function xh(){let e=bh();if(e===null)throw Error(`useTimeRange must be used within a TimeRangeContextProvider`);return e}function Sh(){let e=(0,X.c)(2),{timeRange:t}=xh(),n;return e[0]===t?n=e[1]:(n=Ad(t),e[0]=t,e[1]=n),n}function Ch({storedLastNTimeRangeKey:e,now:t}){return Ed(e)?{timeRangeKey:e,...wd(e,t)}:{timeRangeKey:`7d`,...wd(`7d`,t)}}function wh(e){let t=(0,X.c)(37),{children:n}=e,[r,i]=Zn(),a=_i(Dh),o=_i(Eh),[s,c]=(0,Y.useState)(Th),l,u,d,f,p;t[0]!==r||t[1]!==a||t[2]!==s?(p=Od(r,s),d=p??Ch({storedLastNTimeRangeKey:a,now:s}),f=d.start?.getTime(),l=d.start?.toISOString(),u=d.end?.toISOString(),t[0]=r,t[1]=a,t[2]=s,t[3]=l,t[4]=u,t[5]=d,t[6]=f,t[7]=p):(l=t[3],u=t[4],d=t[5],f=t[6],p=t[7]);let m=u,h;t[8]!==m||t[9]!==l?(h={start:l,end:m},t[8]=m,t[9]=l,t[10]=h):h=t[10];let g=h,_;t[11]!==i||t[12]!==o?(_=e=>{(0,Y.startTransition)(()=>{i(t=>kd({searchParams:t,timeRange:e}),{replace:!0}),Ed(e.timeRangeKey)&&(o(e.timeRangeKey),c(Date.now()))})},t[11]=i,t[12]=o,t[13]=_):_=t[13];let v=_,y;t[14]===v?y=t[15]:(y=e=>{v({timeRangeKey:`custom`,start:e.start,end:e.end})},t[14]=v,t[15]=y);let b=y,x,S;t[16]!==r||t[17]!==i||t[18]!==d||t[19]!==p?(x=()=>{if(p!=null)return;let e=kd({searchParams:r,timeRange:d});e.toString()!==r.toString()&&i(e,{replace:!0})},S=[p,r,i,d],t[16]=r,t[17]=i,t[18]=d,t[19]=p,t[20]=x,t[21]=S):(x=t[20],S=t[21]),(0,Y.useEffect)(x,S);let C;t[22]===d.timeRangeKey?C=t[23]:(C=()=>{if(!Ed(d.timeRangeKey))return;let e=d.timeRangeKey,t=window.setTimeout(()=>{c(Date.now())},Td(e));return()=>{window.clearTimeout(t)}},t[22]=d.timeRangeKey,t[23]=C);let w;t[24]!==d.timeRangeKey||t[25]!==f?(w=[d.timeRangeKey,f],t[24]=d.timeRangeKey,t[25]=f,t[26]=w):w=t[26],(0,Y.useEffect)(C,w);let T;t[27]===v?T=t[28]:(T={setTimeRange:v},t[27]=v,t[28]=T),kh(T);let E;t[29]!==b||t[30]!==v||t[31]!==d||t[32]!==g?(E={timeRange:d,timeRangeISOStrings:g,setTimeRange:v,setCustomTimeRange:b},t[29]=b,t[30]=v,t[31]=d,t[32]=g,t[33]=E):E=t[33];let D;return t[34]!==n||t[35]!==E?(D=U(yh.Provider,{value:E,children:n}),t[34]=n,t[35]=E,t[36]=D):D=t[36],D}function Th(){return Date.now()}function Eh(e){return e.setLastNTimeRangeKey}function Dh(e){return e.lastNTimeRangeKey}function Oh(e){if(e===void 0||e.trim()===``)return;let t=new Date(e);if(Number.isNaN(t.getTime()))throw Error(`Invalid ISO datetime: ${e}`);return t}function kh({setTimeRange:e}){let t=vh(),n=(0,Y.useEffectEvent)(async t=>{if(t.timeRangeKey!==`custom`)return e({timeRangeKey:t.timeRangeKey,...wd(t.timeRangeKey)}),{ok:!0,output:`Set time range to ${t.timeRangeKey}.`};try{let n=Oh(t.startTime),r=Oh(t.endTime);return n===void 0&&r===void 0?{ok:!1,error:`Custom time range requires at least one of startTime or endTime.`}:n!==void 0&&r!==void 0&&n>r?{ok:!1,error:`Custom time range startTime must be before endTime.`}:(e({timeRangeKey:`custom`,start:n,end:r}),{ok:!0,output:`Set custom time range from ${n?.toISOString()??`open start`} to ${r?.toISOString()??`open end`}.`})}catch(e){return{ok:!1,error:e instanceof Error?e.message:`Invalid time range.`}}});(0,Y.useEffect)(()=>{let{registerClientAction:e,unregisterClientAction:r}=t.getState();return e(tf,e=>n(e)),()=>{r(tf)}},[t])}function Ah(e){let t=(0,X.c)(10),n;t[0]===e?n=t[1]:(n=e===void 0?{}:e,t[0]=e,t[1]=n);let{once:r,rootMargin:i,scrollMargin:a}=n,o=r!==void 0&&r,[s,c]=(0,Y.useState)(!1),[l,u]=(0,Y.useState)(!1);s&&!l&&u(!0);let d;t[2]!==o||t[3]!==i||t[4]!==a?(d=e=>{if(e==null)return jh;if(!o){let t=e.getBoundingClientRect(),n=t.width>0||t.height>0,r=t.bottom>=0&&t.top<=window.innerHeight&&t.right>=0&&t.left<=window.innerWidth;n&&r&&c(!0)}let t=new IntersectionObserver(e=>{let n=e[e.length-1];(0,Y.startTransition)(()=>c(n.isIntersecting)),o&&n.isIntersecting&&t.disconnect()},{rootMargin:i,scrollMargin:a});return t.observe(e),()=>t.disconnect()},t[2]=o,t[3]=i,t[4]=a,t[5]=d):d=t[5];let f=d,p;return t[6]!==l||t[7]!==s||t[8]!==f?(p={ref:f,isVisible:s,hasBeenVisible:l},t[6]=l,t[7]=s,t[8]=f,t[9]=p):p=t[9],p}function jh(){}var Mh=(0,Y.createContext)(!0);function Nh(e){let t=(0,Y.useContext)(Mh),[n,r]=(0,Y.useState)(e);return t&&n!==e&&r(e),n}var Ph=F(),Fh=500;function Ih(e,t){let n=(0,X.c)(5),r=t===void 0?Fh:t,i;n[0]===e?i=n[1]:(i=t=>{try{e(JSON.parse(t))}catch{}},n[0]=e,n[1]=i);let a;return n[2]!==r||n[3]!==i?(a=(0,Ph.debounce)(i,r),n[2]=r,n[3]=i,n[4]=a):a=n[4],a}function Lh(e,t){let n=(0,X.c)(6),r=(0,Y.useRef)(null),i,a;n[0]===e?(i=n[1],a=n[2]):(i=()=>{r.current=e},a=[e],n[0]=e,n[1]=i,n[2]=a),(0,Y.useEffect)(i,a);let o,s;n[3]===t?(o=n[4],s=n[5]):(o=()=>{if(typeof t!=`number`)return;let e=t,n=function(){r.current?.()},i=setInterval(n,e),a=function(){document.visibilityState===`hidden`?i!=null&&(clearInterval(i),i=null):i??=(n(),setInterval(n,e))};return document.addEventListener(`visibilitychange`,a),()=>{i!=null&&clearInterval(i),document.removeEventListener(`visibilitychange`,a)}},s=[t],n[3]=t,n[4]=o,n[5]=s),(0,Y.useEffect)(o,s)}var Rh=.05,zh=({word:e,theme:t})=>{let n=e.charCodeAt(0),r=Ne(n%26/26),i=t===`light`?3:5,a=t===`light`?`#fdfdfd`:`#0E0E0E`,o=k(r,a);for(;o<i;)r=t===`light`?he(Rh,r):se(Rh,r),o=k(r,a);return r},Bh=e=>{let t=(0,X.c)(3),{theme:n}=Pr(),r;return t[0]!==n||t[1]!==e?(r=zh({word:e,theme:n}),t[0]=n,t[1]=e,t[2]=r):r=t[2],r};function Vh(e,t){let n=new Intl.DateTimeFormat(e,{...t});return e=>n.format(e)}function Hh(e){let{locale:t,timeZone:n}=e;return Vh(t,{year:`numeric`,month:`2-digit`,day:`2-digit`,hour:`2-digit`,minute:`2-digit`,second:`2-digit`,hour12:!0,timeZone:n})}function Uh(e){let{locale:t,timeZone:n}=e;return Vh(t,{hour:`2-digit`,minute:`2-digit`,hour12:!0,timeZone:n})}function Wh(e){let{locale:t,timeZone:n}=e;return Vh(t,{year:`numeric`,month:`2-digit`,day:`2-digit`,hour:`2-digit`,minute:`2-digit`,hour12:!0,timeZone:n})}function Gh(e){let t=Wh(e);return e=>e.start&&e.end?`${t(e.start)} - ${t(e.end)}`:e.start?`From ${t(e.start)}`:e.end?`Until ${t(e.end)}`:`All Time`}function Kh(e){let{timeZone:t,locale:n}=e;return Intl.DateTimeFormat(n,{timeZoneName:`short`,timeZone:t}).formatToParts().find(e=>e.type===`timeZoneName`)?.value}function qh(e,t=Date.now()){if(e===0)return``;let n=t-e;return n<216e5?new Date(e).toLocaleTimeString(void 0,{hour:`numeric`,minute:`2-digit`}):n<864e5?`${Math.floor(n/ua)}h`:`${Math.floor(n/da)}d`}function Jh(e){return new Intl.DateTimeFormat(e,{day:`2-digit`,month:`2-digit`,year:`numeric`}).formatToParts(new Date).map(e=>{switch(e.type){case`day`:return`dd`;case`month`:return`mm`;case`year`:return`yyyy`;case`literal`:return e.value;default:return``}}).join(``)}function Yh(){let e=(0,X.c)(2),{locale:t}=ft(),n;return e[0]===t?n=e[1]:(n=Jh(t),e[0]=t,e[1]=n),n}var Xh=e=>{let t=(0,X.c)(3),[n,r]=(0,Y.useState)(null),i,a;return t[0]===e?(i=t[1],a=t[2]):(i=()=>{if(!e.current)return;let t=new ResizeObserver(e=>{if(!e||e.length===0)return;let{width:t,height:n}=e[0].contentRect;r({width:t,height:n})});return t.observe(e.current),()=>{t.disconnect()}},a=[e],t[0]=e,t[1]=i,t[2]=a),(0,Y.useEffect)(i,a),n};function Zh(){let e=(0,X.c)(10),t=_i(Qh),n,r,i,a;if(e[0]!==t){let o=t??ci();n=Hh({locale:si(),timeZone:o}),r=Uh({locale:si(),timeZone:o}),i=Wh({locale:si(),timeZone:o}),a=Gh({locale:si(),timeZone:o}),e[0]=t,e[1]=n,e[2]=r,e[3]=i,e[4]=a}else n=e[1],r=e[2],i=e[3],a=e[4];let o;return e[5]!==n||e[6]!==r||e[7]!==i||e[8]!==a?(o={fullTimeFormatter:n,shortTimeFormatter:r,shortDateTimeFormatter:i,timeRangeFormatter:a},e[5]=n,e[6]=r,e[7]=i,e[8]=a,e[9]=o):o=e[9],o}function Qh(e){return e.displayTimezone}function $h(e){let t=(0,X.c)(7),n;t[0]===e?n=t[1]:(n=e===void 0?{}:e,t[0]=e,t[1]=n);let{updateIntervalMs:r}=n,i=r===void 0?null:r,[a,o]=(0,Y.useState)(eg),s,c;t[2]===i?(s=t[3],c=t[4]):(s=()=>{if(typeof i!=`number`)return;let e=setInterval(()=>{o(Date.now())},i);return()=>clearInterval(e)},c=[i],t[2]=i,t[3]=s,t[4]=c),(0,Y.useEffect)(s,c);let l;return t[5]===a?l=t[6]:(l={nowEpochMs:a},t[5]=a,t[6]=l),l}function eg(){return Date.now()}function tg(e){let t=(0,X.c)(2),n;return t[0]===e?n=t[1]:(n=Mp(e),t[0]=e,t[1]=n),n}var ng=`https://pypi.org/pypi/arize-phoenix/json`,rg=null;function ig(){return rg??=fetch(ng).then(e=>e.ok?e.json():null).then(e=>{let t=e?.info?.version;return typeof t==`string`?t:null}).catch(()=>null).then(e=>(e??(rg=null),e)),rg}function ag(){let e=(0,X.c)(2),[t,n]=(0,Y.useState)(null),r,i;return e[0]===Symbol.for(`react.memo_cache_sentinel`)?(r=()=>{let e=!0;return ig().then(t=>{e&&n(t)}),()=>{e=!1}},i=[],e[0]=r,e[1]=i):(r=e[0],i=e[1]),(0,Y.useEffect)(r,i),t}function og(e,t){let[n,r]=(0,Y.useState)(()=>{try{let n=localStorage.getItem(e);return n?JSON.parse(n):t}catch{return t}});return[n,(0,Y.useCallback)(t=>{r(n=>{let r=typeof t==`function`?t(n):t;try{localStorage.setItem(e,JSON.stringify(r))}catch{}return r})},[e])]}function sg(e){let{query:t,queryRef:n}=e,[r]=(0,bi.useQueryLoader)(t,n);return Je(r,`ownedQueryRef is required when initialized from queryRef`),(0,bi.usePreloadedQuery)(t,r)}function cg(){let e=(0,X.c)(7),[t,n]=Zn(),r;e[0]===t?r=e[1]:(r=t.getAll(pd),e[0]=t,e[1]=r);let i=r,a;e[2]===n?a=e[3]:(a=e=>{n(t=>{let n=t.getAll(pd),r=typeof e==`function`?e(n):e,i=new URLSearchParams(t);return i.delete(pd),r.forEach(e=>i.append(pd,e)),i},{replace:!0})},e[2]=n,e[3]=a);let o=a,s;return e[4]!==i||e[5]!==o?(s=[i,o],e[4]=i,e[5]=o,e[6]=s):s=e[6],s}function lg(e){let t=(0,X.c)(4),n;t[0]===e?n=t[1]:(n=t=>{let n=window.matchMedia(e);return n.addEventListener(`change`,t),()=>n.removeEventListener(`change`,t)},t[0]=e,t[1]=n);let r=n,i;return t[2]===e?i=t[3]:(i=()=>window.matchMedia(e).matches,t[2]=e,t[3]=i),(0,Y.useSyncExternalStore)(r,i)}function ug(e){let t=(0,X.c)(49),{start:n,end:r,timeZone:a,isDisabled:o,onCommit:s,autoFocus:c,onBlurWithin:l,onSubmit:u,ref:d}=e,f=(0,Y.useRef)(!1),p=(0,Y.useRef)(!1),m=r==null,h;t[0]!==n||t[1]!==a?(h=()=>qd(n,a),t[0]=n,t[1]=a,t[2]=h):h=t[2];let[g,_]=(0,Y.useState)(h),v;t[3]!==r||t[4]!==a?(v=()=>qd(r,a)??me(a),t[3]=r,t[4]=a,t[5]=v):v=t[5];let[y,b]=(0,Y.useState)(v),x;t[6]!==g||t[7]!==a?(x=g?g.toDate(a):null,t[6]=g,t[7]=a,t[8]=x):x=t[8];let S=x,C;t[9]!==y||t[10]!==a?(C=y?y.toDate(a):null,t[9]=y,t[10]=a,t[11]=C):C=t[11];let w=C,T=!!(S&&w&&S>w),E;t[12]!==r||t[13]!==n||t[14]!==a?(E=()=>{_(qd(n,a)),b(qd(r,a)??me(a)),f.current=!1,p.current=!1},t[12]=r,t[13]=n,t[14]=a,t[15]=E):E=t[15];let D=E,O;t[16]!==w||t[17]!==m||t[18]!==s||t[19]!==D||t[20]!==S?(O=()=>{if(!f.current)return;let e=m&&!p.current?null:w;if(S&&e&&S>e){D();return}f.current=!1,s({start:S,end:e})},t[16]=w,t[17]=m,t[18]=s,t[19]=D,t[20]=S,t[21]=O):O=t[21];let k=O,A,j;t[22]===k?(A=t[23],j=t[24]):(A=()=>({commit:k}),j=[k],t[22]=k,t[23]=A,t[24]=j),(0,Y.useImperativeHandle)(d,A,j);let M;t[25]!==k||t[26]!==l?(M={onBlurWithin:()=>{k(),l?.()}},t[25]=k,t[26]=l,t[27]=M):M=t[27];let{focusWithinProps:N}=Bn(M),P=T||void 0,F;t[28]!==k||t[29]!==u?(F=e=>{e.key===`Enter`&&(e.preventDefault(),k(),u?.())},t[28]=k,t[29]=u,t[30]=F):F=t[30];let I,L;t[31]===Symbol.for(`react.memo_cache_sentinel`)?(I=e=>{_(e),f.current=!0},L=U(Be,{children:fg}),t[31]=I,t[32]=L):(I=t[31],L=t[32]);let ee;t[33]!==c||t[34]!==o||t[35]!==g?(ee=U(i,{"aria-label":`Start time`,className:`time-range-selector__field`,granularity:`minute`,hideTimeZone:!0,isDisabled:o,autoFocus:c,value:g,onChange:I,children:L}),t[33]=c,t[34]=o,t[35]=g,t[36]=ee):ee=t[36];let te;t[37]===Symbol.for(`react.memo_cache_sentinel`)?(te=U(`span`,{"aria-hidden":!0,className:`time-range-selector__separator`,children:`–`}),t[37]=te):te=t[37];let ne,re;t[38]===Symbol.for(`react.memo_cache_sentinel`)?(ne=e=>{b(e),f.current=!0,p.current=!0},re=U(Be,{children:dg}),t[38]=ne,t[39]=re):(ne=t[38],re=t[39]);let ie;t[40]!==y||t[41]!==o?(ie=U(i,{"aria-label":`End time`,className:`time-range-selector__field`,granularity:`minute`,hideTimeZone:!0,isDisabled:o,value:y,onChange:ne,children:re}),t[40]=y,t[41]=o,t[42]=ie):ie=t[42];let ae;return t[43]!==N||t[44]!==P||t[45]!==F||t[46]!==ee||t[47]!==ie?(ae=W(`div`,{className:`time-range-selector__fields`,"data-invalid":P,onKeyDownCapture:F,...N,children:[ee,te,ie]}),t[43]=N,t[44]=P,t[45]=F,t[46]=ee,t[47]=ie,t[48]=ae):ae=t[48],ae}function dg(e){return U(y,{segment:e})}function fg(e){return U(y,{segment:e})}var pg=G`
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
`,mg=G`
  /* Fill the popover, which is sized to the field it is anchored to. */
  width: 100%;
`,hg=G`
  padding: var(--global-dimension-size-200) var(--global-dimension-size-150);
`,gg=G`
  width: 100%;
  border-bottom: var(--global-border-size-thin) solid
    var(--global-menu-border-color);
`,_g=G`
  flex: none;
  font-variant-numeric: tabular-nums;
`,vg=G`
  width: 100%;
  justify-content: flex-start;
`,yg=`var(--global-dimension-size-4000)`;function bg(e){let t=(0,X.c)(85),{value:n,isDisabled:r,onChange:i,size:a}=e,o=a===void 0?`S`:a,{timeRangeKey:s,start:c,end:l}=n,u=(0,Y.useRef)(null),d=(0,Y.useRef)(null),f=(0,Y.useRef)(null),p=(0,Y.useRef)(null),m=(0,Y.useRef)(null),h=(0,Y.useRef)(null),[g,_]=(0,Y.useState)(!1),[v,y]=(0,Y.useState)(!1),[b,x]=(0,Y.useState)(!1),[S,w]=(0,Y.useState)(),[T,E]=(0,Y.useState)(``),D;t[0]===Symbol.for(`react.memo_cache_sentinel`)?(D={sensitivity:`base`},t[0]=D):D=t[0];let{contains:O}=C(D),k;t[1]===Symbol.for(`react.memo_cache_sentinel`)?(k={isTextInput:!0},t[1]=k):k=t[1];let{isFocusVisible:A}=Zt(k),j=v&&A,M;t[2]===Symbol.for(`react.memo_cache_sentinel`)?(M=()=>{_(!1),x(!1),E(``)},t[2]=M):M=t[2];let N=M,P;t[3]===Symbol.for(`react.memo_cache_sentinel`)?(P=()=>{let e=document.activeElement;return e instanceof HTMLElement&&(u.current?.contains(e)||d.current?.contains(e))?e:null},t[3]=P):P=t[3];let F=P,I;t[4]===Symbol.for(`react.memo_cache_sentinel`)?(I=()=>{setTimeout(()=>{F()||(y(!1),N())})},t[4]=I):I=t[4];let L=I,ee;t[5]===Symbol.for(`react.memo_cache_sentinel`)?(ee=()=>{F()?.blur()},t[5]=ee):ee=t[5];let te=ee,ne;t[6]===Symbol.for(`react.memo_cache_sentinel`)?(ne=()=>{te(),y(!1),N()},t[6]=ne):ne=t[6];let re=ne,ie;t[7]===Symbol.for(`react.memo_cache_sentinel`)?(ie=()=>{h.current?.commit(),re()},t[7]=ie):ie=t[7];let ae=ie,oe;t[8]===Symbol.for(`react.memo_cache_sentinel`)?(oe=()=>{_(!0)},t[8]=oe):oe=t[8];let se=oe,ce=!g,le;t[9]===Symbol.for(`react.memo_cache_sentinel`)?(le=e=>{e.target instanceof Node&&d.current?.contains(e.target)||ae()},t[9]=le):le=t[9];let ue;t[10]===ce?ue=t[11]:(ue={ref:u,isDisabled:ce,onInteractOutside:le},t[10]=ce,t[11]=ue),An(ue);let de;t[12]===T?de=t[13]:(de=e=>{if(e.stopPropagation(),T&&document.activeElement===f.current){E(``);return}ae()},t[12]=T,t[13]=de);let fe;t[14]===Symbol.for(`react.memo_cache_sentinel`)?(fe={capture:!0},t[14]=fe):fe=t[14];let pe;t[15]===v?pe=t[16]:(pe={enabled:v,enableOnFormTags:!0,enableOnContentEditable:!0,preventDefault:!0,eventListenerOptions:fe},t[15]=v,t[16]=pe),Yt(`escape`,de,pe);let me=Xh(p),he=_i(Cg),ge,_e,ve,ye,be;if(t[17]!==he||t[18]!==l||t[19]!==c||t[20]!==s){ye=he??ci();let e=si();be=Kh({locale:e,timeZone:ye}),_e=s===`custom`,ge=_e?`Custom`:s;let n=Gh({locale:e,timeZone:ye});ve=Ed(s)?Md(s):n({start:c,end:l}),t[17]=he,t[18]=l,t[19]=c,t[20]=s,t[21]=ge,t[22]=_e,t[23]=ve,t[24]=ye,t[25]=be}else ge=t[21],_e=t[22],ve=t[23],ye=t[24],be=t[25];let xe=ve,Se=Id(T),we=gd.filter(e=>{let{key:t}=e;return!Se.includes(t)}),Te;t[26]===c?Te=t[27]:(Te=c?.getTime()??``,t[26]=c,t[27]=Te);let Ee;t[28]===l?Ee=t[29]:(Ee=l?.getTime()??``,t[28]=l,t[29]=Ee);let De=`${s}|${Te}|${Ee}|${ye}`,Oe=me?.width,Ae=`${v}|${De}|${xe}|${ge}|${be??``}`,je=g&&S!=null,Me;t[30]!==r||t[31]!==v?(Me=e=>{if(r||v)return;let t=m.current,n=e.target instanceof Node&&t?.contains(e.target);!t||n||(e.preventDefault(),t.focus())},t[30]=r,t[31]=v,t[32]=Me):Me=t[32];let Ne=Me,Pe;t[33]===g?Pe=t[34]:(Pe=()=>{let e=g?u.current?.offsetWidth:void 0,t=e?`${e}px`:void 0;w(e=>e===t?e:t)},t[33]=g,t[34]=Pe);let Fe;t[35]!==g||t[36]!==Ae?(Fe=[g,Ae],t[35]=g,t[36]=Ae,t[37]=Fe):Fe=t[37],(0,Y.useLayoutEffect)(Pe,Fe);let Ie,Le;t[38]!==b||t[39]!==je?(Ie=()=>{!je||b||f.current?.focus()},Le=[je,b],t[38]=b,t[39]=je,t[40]=Ie,t[41]=Le):(Ie=t[40],Le=t[41]),(0,Y.useLayoutEffect)(Ie,Le);let Re=r||void 0,ze=j||void 0,Be=g||void 0,Ve=_e?`info`:`default`,R;t[42]!==ge||t[43]!==Ve?(R=U(rs,{size:`S`,variant:Ve,css:_g,children:ge}),t[42]=ge,t[43]=Ve,t[44]=R):R=t[44];let He=g||Oe==null?`auto`:Oe,Ue=v?yg:void 0,We;t[45]!==He||t[46]!==Ue?(We={width:He,minWidth:Ue},t[45]=He,t[46]=Ue,t[47]=We):We=t[47];let Ge;t[48]!==l||t[49]!==De||t[50]!==r||t[51]!==v||t[52]!==i||t[53]!==c||t[54]!==ye||t[55]!==xe?(Ge=U(`div`,{ref:p,className:`time-range-selector__value-measure`,children:v?U(ug,{ref:h,start:c,end:l,timeZone:ye,isDisabled:r,autoFocus:!0,onBlurWithin:L,onSubmit:re,onCommit:e=>i({timeRangeKey:`custom`,...e})},De):U(`button`,{ref:m,type:`button`,className:`time-range-selector__value`,disabled:r,onFocus:()=>{r||(y(!0),se())},children:xe})}),t[48]=l,t[49]=De,t[50]=r,t[51]=v,t[52]=i,t[53]=c,t[54]=ye,t[55]=xe,t[56]=Ge):Ge=t[56];let Ke;t[57]!==We||t[58]!==Ge?(Ke=U(`div`,{className:`time-range-selector__value-shell`,style:We,children:Ge}),t[57]=We,t[58]=Ge,t[59]=Ke):Ke=t[59];let qe;t[60]===be?qe=t[61]:(qe=be&&U(B,{size:`XS`,color:`text-500`,className:`time-range-selector__timezone`,children:be}),t[60]=be,t[61]=qe);let z;t[62]!==Ne||t[63]!==o||t[64]!==Re||t[65]!==ze||t[66]!==Be||t[67]!==R||t[68]!==Ke||t[69]!==qe?(z=W(`div`,{ref:u,className:`time-range-selector`,css:pg,"data-size":o,"data-disabled":Re,"data-focus-visible":ze,"data-presets-open":Be,role:`group`,"aria-label":`Time range`,onPointerDown:Ne,children:[R,Ke,qe]}),t[62]=Ne,t[63]=o,t[64]=Re,t[65]=ze,t[66]=Be,t[67]=R,t[68]=Ke,t[69]=qe,t[70]=z):z=t[70];let Je=$n,Ye;t[71]===Symbol.for(`react.memo_cache_sentinel`)?(Ye=e=>{e||N()},t[71]=Ye):Ye=t[71];let Xe=b?`bottom end`:`bottom start`,Ze=b?`max-content`:S,Qe=b?S:void 0,$e;t[72]!==Ze||t[73]!==Qe?($e={width:Ze,minWidth:Qe,overflow:`hidden`,transition:`none`,animation:`none`,transform:`translateY(0)`,opacity:1},t[72]=Ze,t[73]=Qe,t[74]=$e):$e=t[74];let et=b?U(Qd,{value:{start:c,end:l},timeZone:ye,onCancel:()=>x(!1),onApply:e=>{y(!1),N(),i({timeRangeKey:`custom`,...e})}}):W(V,{children:[W(Dt,{filter:O,children:[W(Ss,{"aria-label":`Search time range presets`,size:`M`,variant:`quiet`,value:T,onChange:E,css:gg,children:[U(bs,{}),U(ke,{ref:f,placeholder:`Search or type "25m"`,onBlur:L})]}),W(yc,{"aria-label":`time range preset selection`,selectionMode:`single`,selectedKeys:_e?[]:[s],css:mg,renderEmptyState:Sg,onSelectionChange:e=>{let t=e===`all`?void 0:e.keys().next().value,n=Ed(t)?t:Ed(s)?s:void 0;if(y(!1),!n){N();return}let r=wd(n);N(),i({timeRangeKey:n,...r})},children:[Se.map(e=>U(Ce,{id:e,textValue:T,children:Md(e)},e)),we.map(xg)]})]}),U(Ka,{children:U(Mt,{size:`S`,variant:`quiet`,css:vg,leadingVisual:U(H,{svg:U(ln,{})}),onPress:()=>x(!0),children:`Pick from a calendar`})})]}),tt;t[75]!==Je||t[76]!==je||t[77]!==Ye||t[78]!==Xe||t[79]!==$e||t[80]!==et?(tt=U(Je,{ref:d,triggerRef:u,isOpen:je,onOpenChange:Ye,isNonModal:!0,isKeyboardDismissDisabled:!0,placement:Xe,offset:2,style:$e,children:et}),t[75]=Je,t[76]=je,t[77]=Ye,t[78]=Xe,t[79]=$e,t[80]=et,t[81]=tt):tt=t[81];let nt;return t[82]!==z||t[83]!==tt?(nt=W(V,{children:[z,tt]}),t[82]=z,t[83]=tt,t[84]=nt):nt=t[84],nt}function xg(e){let{key:t,label:n}=e;return U(Ce,{id:t,children:n},t)}function Sg(){return U(`div`,{css:hg,children:`No matching time ranges`})}function Cg(e){return e.displayTimezone}var wg=Ht`
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.35;
  }
`,Tg=G`
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
`,Eg=G`
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
      animation: ${wg} 3s ease-in-out infinite;
    }
  }

  @media (prefers-reduced-motion: reduce) {
    &[data-selected="true"]::before {
      animation: none;
    }
  }
`;function Dg(e){let t=(0,X.c)(13),{label:n,icon:r,size:i,isDisabled:a,onPress:o}=e,s;t[0]===r?s=t[1]:(s=U(H,{svg:r}),t[0]=r,t[1]=s);let c;t[2]!==a||t[3]!==n||t[4]!==o||t[5]!==i||t[6]!==s?(c=U(Mt,{size:i,variant:`quiet`,css:Eg,"aria-label":n,isDisabled:a,leadingVisual:s,onPress:o}),t[2]=a,t[3]=n,t[4]=o,t[5]=i,t[6]=s,t[7]=c):c=t[7];let l;t[8]===n?l=t[9]:(l=U(oa,{children:n}),t[8]=n,t[9]=l);let u;return t[10]!==c||t[11]!==l?(u=W(ve,{children:[c,l]}),t[10]=c,t[11]=l,t[12]=u):u=t[12],u}function Og(e){let t=(0,X.c)(48),{value:n,onChange:r,isLive:i,onIsLiveChange:a,isDisabled:o,size:s}=e,c=i!==void 0&&i,l=s===void 0?`S`:s,u=n.start!=null,d=c?`Stop live streaming`:`Resume live streaming`,f=n.end==null,p;t[0]===r?p=t[1]:(p=e=>{e&&r(e)},t[0]=r,t[1]=p);let m=p,h=o||void 0,g;t[2]===Symbol.for(`react.memo_cache_sentinel`)?(g=U(on,{}),t[2]=g):g=t[2];let _=o||!u,v;t[3]!==m||t[4]!==n?(v=()=>m(Hd({value:n})),t[3]=m,t[4]=n,t[5]=v):v=t[5];let y;t[6]!==l||t[7]!==_||t[8]!==v?(y=U(Dg,{label:`Pan back in time`,icon:g,size:l,isDisabled:_,onPress:v}),t[6]=l,t[7]=_,t[8]=v,t[9]=y):y=t[9];let b;t[10]===Symbol.for(`react.memo_cache_sentinel`)?(b=U(et,{}),t[10]=b):b=t[10];let x=o||!u,S;t[11]!==m||t[12]!==n?(S=()=>m(Gd({value:n})),t[11]=m,t[12]=n,t[13]=S):S=t[13];let C;t[14]!==l||t[15]!==S||t[16]!==x?(C=U(Dg,{label:`Zoom out`,icon:b,size:l,isDisabled:x,onPress:S}),t[14]=l,t[15]=S,t[16]=x,t[17]=C):C=t[17];let w;t[18]!==o||t[19]!==c||t[20]!==d||t[21]!==a||t[22]!==l?(w=a&&W(ve,{children:[U(sc,{size:l,className:`time-range-controls__live-toggle`,css:Eg,"aria-label":d,isSelected:c,isDisabled:o,leadingVisual:U(H,{svg:U(c?jt:Sn,{})}),onChange:a}),U(oa,{children:d})]}),t[18]=o,t[19]=c,t[20]=d,t[21]=a,t[22]=l,t[23]=w):w=t[23];let T;t[24]===Symbol.for(`react.memo_cache_sentinel`)?(T=U(Ot,{}),t[24]=T):T=t[24];let E=o||!u,D;t[25]!==m||t[26]!==n?(D=()=>m(Wd({value:n})),t[25]=m,t[26]=n,t[27]=D):D=t[27];let O;t[28]!==l||t[29]!==E||t[30]!==D?(O=U(Dg,{label:`Zoom in`,icon:T,size:l,isDisabled:E,onPress:D}),t[28]=l,t[29]=E,t[30]=D,t[31]=O):O=t[31];let k;t[32]===Symbol.for(`react.memo_cache_sentinel`)?(k=U(Qn,{}),t[32]=k):k=t[32];let A=o||!u||f,j;t[33]!==m||t[34]!==n?(j=()=>m(Ud({value:n})),t[33]=m,t[34]=n,t[35]=j):j=t[35];let M;t[36]!==l||t[37]!==A||t[38]!==j?(M=U(Dg,{label:`Pan forward in time`,icon:k,size:l,isDisabled:A,onPress:j}),t[36]=l,t[37]=A,t[38]=j,t[39]=M):M=t[39];let N;return t[40]!==l||t[41]!==C||t[42]!==w||t[43]!==O||t[44]!==M||t[45]!==h||t[46]!==y?(N=W(`div`,{className:`time-range-controls`,css:Tg,role:`group`,"aria-label":`Time range controls`,"data-size":l,"data-disabled":h,children:[y,C,w,O,M]}),t[40]=l,t[41]=C,t[42]=w,t[43]=O,t[44]=M,t[45]=h,t[46]=y,t[47]=N):N=t[47],N}function kg(e){let t=(0,X.c)(4),{size:n}=e,r=n===void 0?`S`:n,{timeRange:i,setTimeRange:a}=xh(),o;return t[0]!==a||t[1]!==r||t[2]!==i?(o=U(bg,{value:i,onChange:a,size:r}),t[0]=a,t[1]=r,t[2]=i,t[3]=o):o=t[3],o}function Ag(e){let t=(0,X.c)(4),{timeRange:n,setTimeRange:r}=xh(),i;return t[0]!==e||t[1]!==r||t[2]!==n?(i=U(Og,{...e,value:n,onChange:r}),t[0]=e,t[1]=r,t[2]=n,t[3]=i):i=t[3],i}G`
  display: flex;
  flex-direction: column;
  gap: var(--global-dimension-size-200);
`,G`
  display: flex;
  gap: var(--global-dimension-size-100);
  align-items: start;
  justify-content: end;
  /* Move the button down to align */
  button {
    margin-top: 26px;
  }
`,G`
  width: 100%;
  display: flex;
  justify-content: flex-end;
  gap: var(--global-dimension-size-100);
`,G`
  width: 100%;
  .react-aria-DateInput {
    width: 100%;
    // Eliminate the re-sizing of the DateField as you type
    min-width: 200px;
  }
`;var jg=Ht`
  to {
    --ai-conic-angle: 405deg;
  }
`,Mg=Ht`
  0%, 100% {
    box-shadow: var(--ai-glow-box-shadow-rest);
  }
  50% {
    box-shadow: var(--ai-glow-box-shadow-strong);
  }
`,Ng=Ht`
  0% {
    -webkit-mask-position: 170% center;
    mask-position: 170% center;
  }

  100% {
    -webkit-mask-position: -70% center;
    mask-position: -70% center;
  }
`,Pg=Ht`
  0%, 100% {
    box-shadow: var(--ai-glow-box-shadow-contained-rest);
  }
  50% {
    box-shadow: var(--ai-glow-box-shadow-contained-strong);
  }
`,Fg=Ht`
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
`,Ig=Ht`
  0%, 100% {
    opacity: 0;
  }
  8%, 40% {
    opacity: var(--ai-glow-opacity);
  }
  55% {
    opacity: 0;
  }
`,Lg=G`
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
`,Rg=G`
  -webkit-mask-position: center;
  mask-position: center;
  animation: ${Ng} var(--ai-glow-wipe-continuous-duration)
    linear infinite both var(--ai-glow-wipe-continuous-delay);
`,zg=G`
  background: conic-gradient(
    from var(--ai-conic-angle),
    var(--ai-gradient-color-start),
    var(--ai-gradient-color-middle),
    var(--ai-gradient-color-end),
    var(--ai-gradient-color-start)
  );
`,Bg=G`
  ${zg};
  padding: var(--ai-conic-band-stroke-width);
  -webkit-mask:
    linear-gradient(#000 0 0) content-box,
    linear-gradient(#000 0 0);
  mask:
    linear-gradient(#000 0 0) content-box,
    linear-gradient(#000 0 0);
  -webkit-mask-composite: xor;
  mask-composite: exclude;
`,Vg=G`
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
    ${Bg};
    inset: calc(
      -1 * (var(--ai-outline-gap) + var(--ai-conic-band-stroke-width))
    );
    z-index: 2;
    border-radius: calc(
      var(--ai-outline-target-radius) + var(--ai-outline-gap) +
        var(--ai-conic-band-stroke-width)
    );
    opacity: 0.3;
    animation: ${jg} var(--ai-conic-spin-duration) linear infinite
      paused;
  }

  .ai-outline__glow {
    ${Lg};
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
    ${Rg};
  }

  &[data-state="active"] .ai-outline__glow::before {
    opacity: 0.72;
    animation: ${Mg} var(--ai-glow-wipe-duration) ease-in-out
      infinite;
  }

  &[data-state="eligible"][data-should-flash="true"] .ai-outline__glow {
    animation: ${Fg} var(--ai-glow-wipe-duration)
      var(--ai-glow-wipe-easing) 1;
  }

  &[data-state="eligible"][data-should-flash="true"] .ai-outline__glow::before {
    animation:
      ${Mg} var(--ai-glow-wipe-duration) ease-in-out 1,
      ${Ig} var(--ai-glow-wipe-duration) linear 1;
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
      animation-name: ${Pg};
    }

    &[data-state="eligible"][data-should-flash="true"]
      .ai-outline__glow::before {
      animation-name: ${Pg}, ${Ig};
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
`;function Hg(e){let t=(0,X.c)(15),{children:n,className:r,css:i,isFullWidth:a,glowMode:o,radius:s,shouldFlash:c,state:l}=e,u=a!==void 0&&a,d=o===void 0?`outer`:o,f=s===void 0?`small`:s,p=c!==void 0&&c,m=l===void 0?`idle`:l,h=m===`eligible`&&p,g;t[0]===i?g=t[1]:(g=G(Vg,i),t[0]=i,t[1]=g);let _=g,v;t[2]===r?v=t[3]:(v=z(`ai-outline`,r),t[2]=r,t[3]=v);let y=u?`true`:void 0,b=h?`true`:void 0,x,S;t[4]===Symbol.for(`react.memo_cache_sentinel`)?(x=U(`span`,{className:`ai-outline__glow`,"aria-hidden":`true`}),S=U(`span`,{className:`ai-outline__stroke`,"aria-hidden":`true`}),t[4]=x,t[5]=S):(x=t[4],S=t[5]);let C;return t[6]!==n||t[7]!==_||t[8]!==d||t[9]!==f||t[10]!==m||t[11]!==v||t[12]!==y||t[13]!==b?(C=W(`div`,{className:v,css:_,"data-full-width":y,"data-glow-mode":d,"data-radius":f,"data-should-flash":b,"data-state":m,children:[x,S,n]}),t[6]=n,t[7]=_,t[8]=d,t[9]=f,t[10]=m,t[11]=v,t[12]=y,t[13]=b,t[14]=C):C=t[14],C}var Ug=(0,Y.createContext)(null);function Wg(){return(0,Y.useContext)(Ug)??{variant:`grid`}}var Gg=G`
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
`,Kg=G`
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
`,qg=G`
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
`,Jg=G`
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
`;G`
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
    ${bu}
    position: absolute;
    top: var(--global-dimension-size-75);
    right: var(--global-dimension-size-75);
    width: var(--global-dimension-size-300);
    height: var(--global-dimension-size-300);
    border-radius: 50%;
    background-color: var(--global-color-gray-50);
  }

  &[data-variant="inline"] {
    ${bu}
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
`;function Yg(e){let t=(0,X.c)(17),n,r,i,a,o;t[0]===e?(n=t[1],r=t[2],i=t[3],a=t[4],o=t[5]):({children:n,ref:r,variant:a,collapsible:o,...i}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a,t[5]=o);let s=a===void 0?`grid`:a,c=o!==void 0&&o,l;t[6]===s?l=t[7]:(l={variant:s},t[6]=s,t[7]=l);let u=l,d=c||void 0,f;t[8]!==n||t[9]!==r||t[10]!==i||t[11]!==d||t[12]!==s?(f=U(`div`,{ref:r,css:Gg,"data-variant":s,"data-collapsible":d,...i,children:n}),t[8]=n,t[9]=r,t[10]=i,t[11]=d,t[12]=s,t[13]=f):f=t[13];let p;return t[14]!==f||t[15]!==u?(p=U(Ug.Provider,{value:u,children:f}),t[14]=f,t[15]=u,t[16]=p):p=t[16],p}var Xg=(0,Y.createContext)(null);function Zg(){let e=(0,Y.useContext)(Xg);if(!e)throw Error(`useAttachmentContext must be used within an <Attachment> component`);return e}function Qg(e){if(e.type===`context`)return`context`;if(e.type===`source-document`)return`source`;let t=e.mediaType??``;return t.startsWith(`image/`)?`image`:t.startsWith(`video/`)?`video`:t.startsWith(`audio/`)?`audio`:t.startsWith(`application/`)||t.startsWith(`text/`)?`document`:`unknown`}function $g(e){return e.type===`context`?e.label:e.type===`source-document`?e.title||e.filename||`Source`:e.filename||(Qg(e)===`image`?`Image`:`Attachment`)}function e_(e){return e.type===`context`?e.detail:void 0}function t_(e){switch(e){case`project`:return U(H,{svg:U(dn,{})});case`trace`:return U(H,{svg:U(dn,{})});case`session`:return U(H,{svg:U(Xn,{})});case`span`:return U(H,{svg:U(On,{})});case`span_filter`:return U(H,{svg:U(Dn,{})});case`dataset`:return U(H,{svg:U(kt,{})});case`playground`:return U(H,{svg:U(Et,{})});case`code_evaluator`:return U(H,{svg:U(It,{})});case`llm_evaluator`:return U(H,{svg:U(Jt,{})});default:return U(H,{svg:U(Vn,{})})}}function n_(e){if(e.type===`context`)return e.icon??t_(e.category);switch(Qg(e)){case`image`:return U(H,{svg:U(jn,{})});case`video`:return U(H,{svg:U(Et,{})});case`audio`:return U(H,{svg:U(ut,{})});case`document`:return U(H,{svg:U(bt,{})});case`source`:return U(H,{svg:U(zn,{})});default:return U(H,{svg:U(ut,{})})}}function r_(e){let t=(0,X.c)(22),n,r,i,a,o;t[0]===e?(n=t[1],r=t[2],i=t[3],a=t[4],o=t[5]):({children:n,ref:a,data:r,onRemove:i,...o}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a,t[5]=o);let{variant:s}=Wg(),{theme:c}=Pr(),l;t[6]===r?l=t[7]:(l=Qg(r),t[6]=r,t[7]=l);let u=l,d;t[8]!==r||t[9]!==u||t[10]!==i||t[11]!==s?(d={data:r,mediaCategory:u,variant:s,onRemove:i},t[8]=r,t[9]=u,t[10]=i,t[11]=s,t[12]=d):d=t[12];let f=d,p;t[13]!==n||t[14]!==a||t[15]!==o||t[16]!==c||t[17]!==s?(p=U(`div`,{ref:a,css:Kg,"data-attachment":``,"data-variant":s,"data-theme":c,...o,children:n}),t[13]=n,t[14]=a,t[15]=o,t[16]=c,t[17]=s,t[18]=p):p=t[18];let m;return t[19]!==p||t[20]!==f?(m=U(Xg.Provider,{value:f,children:p}),t[19]=p,t[20]=f,t[21]=m):m=t[21],m}function i_(e){let t=(0,X.c)(16),n,r,i;t[0]===e?(n=t[1],r=t[2],i=t[3]):({ref:r,fallback:n,...i}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i);let{data:a,mediaCategory:o,variant:s}=Zg(),c;t[4]!==a||t[5]!==n||t[6]!==o?(c=()=>a.type===`file`&&o===`image`&&typeof a.url==`string`&&a.url?U(`img`,{src:a.url,alt:a.filename??`Image`}):a.type===`file`&&o===`video`&&typeof a.url==`string`&&a.url?U(`video`,{src:a.url,muted:!0}):n??n_(a),t[4]=a,t[5]=n,t[6]=o,t[7]=c):c=t[7];let l=c,u;t[8]===l?u=t[9]:(u=l(),t[8]=l,t[9]=u);let d;return t[10]!==o||t[11]!==r||t[12]!==i||t[13]!==u||t[14]!==s?(d=U(`div`,{ref:r,css:qg,"data-variant":s,"data-media-category":o,...i,children:u}),t[10]=o,t[11]=r,t[12]=i,t[13]=u,t[14]=s,t[15]=d):d=t[15],d}function a_(e){let t=(0,X.c)(28),n,r,i;t[0]===e?(n=t[1],r=t[2],i=t[3]):({ref:n,showMediaType:i,...r}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i);let a=i!==void 0&&i,{data:o,variant:s}=Zg();if(s===`grid`)return null;let c;t[4]===o?c=t[5]:(c=$g(o),t[4]=o,t[5]=c);let l=c,u,d,f,p,m;t[6]!==o||t[7]!==n?(u=e_(o),d=o.type===`file`||o.type===`source-document`?o.mediaType:void 0,f=n,p=Jg,m=z(`attachment-info`,{"attachment-info--with-detail":u}),t[6]=o,t[7]=n,t[8]=u,t[9]=d,t[10]=f,t[11]=p,t[12]=m):(u=t[8],d=t[9],f=t[10],p=t[11],m=t[12]);let h;t[13]===l?h=t[14]:(h=U(`span`,{className:`attachment-info__label`,children:l}),t[13]=l,t[14]=h);let g;t[15]===u?g=t[16]:(g=u?U(`span`,{className:`attachment-info__detail`,children:u}):null,t[15]=u,t[16]=g);let _;t[17]!==d||t[18]!==a?(_=a&&d?U(`span`,{className:`attachment-info__media-type`,children:d}):null,t[17]=d,t[18]=a,t[19]=_):_=t[19];let v;return t[20]!==r||t[21]!==f||t[22]!==p||t[23]!==m||t[24]!==h||t[25]!==g||t[26]!==_?(v=W(`div`,{ref:f,css:p,className:m,...r,children:[h,g,_]}),t[20]=r,t[21]=f,t[22]=p,t[23]=m,t[24]=h,t[25]=g,t[26]=_,t[27]=v):v=t[27],v}var o_=G`
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
`,s_=G`
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
`;function c_(e){let t=(0,X.c)(27),{selected:n,type:r,label:i,description:a,isFreeformEntry:o,textValue:s,onToggle:c,onTextChange:l}=e,u=(0,Y.useRef)(null),d,f;t[0]!==o||t[1]!==n?(d=()=>{n&&o&&u.current&&u.current.focus()},f=[n,o],t[0]=o,t[1]=n,t[2]=d,t[3]=f):(d=t[2],f=t[3]),(0,Y.useEffect)(d,f);let p=r===`single`?`option-button__indicator option-button__indicator--radio`:`option-button__indicator option-button__indicator--checkbox`,m;t[4]===Symbol.for(`react.memo_cache_sentinel`)?(m={scale:.98,transition:{type:`tween`,duration:.06}},t[4]=m):m=t[4];let h=r===`single`?`radio`:`checkbox`,g;t[5]===c?g=t[6]:(g=e=>{let t=e.target;t.tagName!==`INPUT`&&t.tagName!==`TEXTAREA`&&(e.key===`Enter`&&(e.metaKey||e.ctrlKey)||(e.key===`Enter`||e.key===` `)&&(e.preventDefault(),c()))},t[5]=c,t[6]=g);let _;t[7]===r?_=t[8]:(_=r===`multi`&&U(`svg`,{viewBox:`0 0 18 18`,"aria-hidden":`true`,children:U(`polyline`,{points:`1 9 7 14 15 4`})}),t[7]=r,t[8]=_);let v;t[9]!==p||t[10]!==_?(v=U(`span`,{className:p,children:_}),t[9]=p,t[10]=_,t[11]=v):v=t[11];let y;t[12]!==a||t[13]!==o||t[14]!==i||t[15]!==l||t[16]!==c||t[17]!==n||t[18]!==s?(y=o?U(`div`,{className:`option-button__text-entry`,onClick:l_,children:U(`input`,{ref:u,type:`text`,className:`option-button__text-input`,value:s||``,placeholder:`Type your own answer…`,onMouseDown:()=>{n||c()},onChange:e=>{n||c(),l?.(e.target.value)},"aria-label":`Type your own answer`})}):W(`div`,{className:`option-button__content`,children:[U(`span`,{className:`option-button__label`,children:i}),a?U(`span`,{className:`option-button__description`,children:a}):null]}),t[12]=a,t[13]=o,t[14]=i,t[15]=l,t[16]=c,t[17]=n,t[18]=s,t[19]=y):y=t[19];let b;return t[20]!==c||t[21]!==n||t[22]!==h||t[23]!==g||t[24]!==v||t[25]!==y?(b=W(M.div,{css:s_,"data-selected":n,onClick:c,whileTap:m,role:h,"aria-checked":n,tabIndex:0,onKeyDown:g,children:[v,y]}),t[20]=c,t[21]=n,t[22]=h,t[23]=g,t[24]=v,t[25]=y,t[26]=b):b=t[26],b}function l_(e){return e.stopPropagation()}var u_=`__freeform__`,d_=.04,f_={enter:e=>({x:e>0?120:-120,opacity:0}),center:{x:0,opacity:1},exit:e=>({x:e>0?-120:120,opacity:0})},p_={type:`spring`,stiffness:400,damping:32,mass:.8},m_={type:`spring`,stiffness:700,damping:24,mass:.6};function h_({questions:e,onProgressStateChange:t,onSubmit:n,onCancel:r}){let[i,a]=(0,Y.useState)({}),[o,s]=(0,Y.useState)({}),[c,l]=(0,Y.useState)(0),[u,d]=(0,Y.useState)(0),f=(0,Y.useRef)(!0),p=(0,Y.useEffectEvent)(e=>{t?.(e)}),m=e.length,h=e[c];(0,Y.useEffect)(()=>{let e=setTimeout(()=>{f.current=!1},500);return()=>clearTimeout(e)},[]),(0,Y.useEffect)(()=>{p({answers:{},freeformTexts:{},currentIndex:0})},[]);let g=e=>{d(e>c?1:-1),l(e),t?.({answers:i,freeformTexts:o,currentIndex:e})},_=(e,t,n)=>{let r=i[e]||[],o;o=n===`single`?r.includes(t)?[]:[t]:r.includes(t)?r.filter(e=>e!==t):[...r,t],a(t=>({...t,[e]:o}))},v=(e,t)=>{a(n=>({...n,[e]:t}))},y=()=>{t?.({answers:i,freeformTexts:o,currentIndex:c}),n({answers:i,freeformTexts:o})},b=()=>{let t=i[e[c].id];((Array.isArray(t)?t.length>0:t)||e[c].allow_skip===!0)&&(c===m-1?y():g(c+1))},x=e=>{if(e.key!==`Enter`||e.nativeEvent.isComposing)return;let t=e.target;if(t.tagName===`TEXTAREA`)return;let n=t.tagName===`INPUT`&&t.type===`text`;(e.metaKey||e.ctrlKey||n)&&(e.preventDefault(),b())},S=e=>{e.key!==`Enter`||e.nativeEvent.isComposing||e.shiftKey||(e.preventDefault(),b())},C=f.current?d_:0,w=C,T=2*C,E=e=>(3+e)*C,D=3*C,O=i[h.id],k=Array.isArray(O)?O.length>0:!!O,A=h.allow_skip===!0,j=k||A;return U(Jn,{autoFocus:!0,contain:!0,restoreFocus:!0,children:W(`div`,{css:o_,onKeyDown:x,children:[W(M.div,{className:`elicitation__header`,initial:{opacity:0,y:8},animate:{opacity:1,y:0},transition:{...m_,delay:w,opacity:{duration:.12,delay:w}},children:[W(`span`,{className:`elicitation__step-label`,children:[`Question `,c+1,` of `,m]}),U(`div`,{className:`elicitation__dots`,children:e.map((e,t)=>U(`button`,{className:`elicitation__dot ${t===c?`elicitation__dot--active`:`elicitation__dot--inactive`}`,onClick:()=>g(t),"aria-label":`Go to question ${t+1}`},t))})]}),U(`div`,{className:`elicitation__body`,children:U(Oe,{custom:u,mode:`popLayout`,children:W(M.div,{custom:u,variants:f_,initial:!f.current&&`enter`,animate:`center`,exit:`exit`,transition:p_,className:`elicitation__question-content`,children:[U(M.div,{className:`elicitation__prompt`,initial:{opacity:0,y:-8},animate:{opacity:1,y:0},transition:{...m_,delay:T,opacity:{duration:.12,delay:T}},children:h.prompt}),h.type===`freeform`?U(M.div,{initial:{opacity:0,y:-8},animate:{opacity:1,y:0},transition:{...m_,delay:D,opacity:{duration:.12,delay:D}},children:U(`textarea`,{className:`elicitation__freeform`,value:i[h.id]||``,onChange:e=>v(h.id,e.target.value),onKeyDown:S,placeholder:`Type your response… (Enter to submit, Shift+Enter for newline)`,"aria-label":h.prompt})}):W(`div`,{className:`elicitation__options`,children:[h.options?.map((e,t)=>U(M.div,{initial:{opacity:0,y:-8},animate:{opacity:1,y:0},transition:{...m_,delay:E(t),opacity:{duration:.12,delay:E(t)}},children:U(c_,{selected:(i[h.id]||[]).includes(e.id),type:h.type,label:e.label,description:e.description,onToggle:()=>_(h.id,e.id,h.type)})},e.id)),h.allow_freeform?U(M.div,{initial:{opacity:0,y:-8},animate:{opacity:1,y:0},transition:{...m_,delay:E(h.options?.length??0),opacity:{duration:.12,delay:E(h.options?.length??0)}},children:U(c_,{selected:(i[h.id]||[]).includes(u_),type:h.type,label:`Type your own answer`,isFreeformEntry:!0,textValue:o[h.id],onToggle:()=>_(h.id,u_,h.type),onTextChange:e=>s(t=>({...t,[h.id]:e}))})},u_):null]})]},h.id)})}),W(M.div,{className:`elicitation__nav`,initial:{opacity:0,y:8},animate:{opacity:1,y:0},transition:{...m_,delay:0,opacity:{duration:.12,delay:0}},children:[W(`div`,{className:`elicitation__nav-group`,children:[r&&U(Mt,{size:`S`,variant:`default`,onPress:r,children:`Cancel`}),U(Mt,{size:`S`,variant:`default`,isDisabled:c===0,onPress:()=>g(c-1),children:`Back`})]}),c===m-1?U(Mt,{size:`S`,variant:`primary`,isDisabled:!j,onPress:y,children:`Submit`}):U(Mt,{size:`S`,variant:k?`primary`:`default`,isDisabled:!j,onPress:()=>g(c+1),children:k?`Next`:`Skip`})]})]})})}var g_=(0,Y.createContext)(null),__=G`
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
`,v_=G`
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
`,y_=G`
  display: flex;
  align-items: center;
  gap: var(--global-dimension-size-50);
  margin-left: auto;
`,b_=G`
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
`,x_=G`
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
  ${bu}
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
`;G`
  display: flex;
  align-items: center;
  gap: var(--global-dimension-size-50);
`,G`
  color: var(--global-text-color-500);
  font-size: var(--global-font-size-s);
  white-space: nowrap;
  user-select: none;
`;function S_(e){let t=(0,X.c)(15),n,r,i,a;t[0]===e?(n=t[1],r=t[2],i=t[3],a=t[4]):({children:n,ref:i,from:r,...a}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a);let o;t[5]===r?o=t[6]:(o={from:r},t[5]=r,t[6]=o);let s;t[7]!==n||t[8]!==r||t[9]!==i||t[10]!==a?(s=U(`div`,{ref:i,css:__,"data-from":r,...a,children:n}),t[7]=n,t[8]=r,t[9]=i,t[10]=a,t[11]=s):s=t[11];let c;return t[12]!==o||t[13]!==s?(c=U(g_.Provider,{value:o,children:s}),t[12]=o,t[13]=s,t[14]=c):c=t[14],c}function C_(e){let t=(0,X.c)(8),n,r,i;t[0]===e?(n=t[1],r=t[2],i=t[3]):({children:n,ref:r,...i}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i);let a;return t[4]!==n||t[5]!==r||t[6]!==i?(a=U(`div`,{ref:r,css:v_,...i,children:n}),t[4]=n,t[5]=r,t[6]=i,t[7]=a):a=t[7],a}function w_(e,t){for(let n of e.tokenColors)if((Array.isArray(n.scope)?n.scope:n.scope?[n.scope]:[]).includes(t))return n.settings.foreground}function T_(e){let t=e.colors,n=t=>w_(e,t),r=[{tag:[R.standard(R.tagName),R.tagName],color:n(`entity.name.tag`)},{tag:[R.comment],color:n(`comment`)},{tag:[R.bracket,R.punctuation,R.separator,R.derefOperator],color:n(`punctuation`)},{tag:[R.className,R.typeName,R.namespace,R.definition(R.typeName)],color:n(`entity.name.type`)},{tag:[R.propertyName,R.attributeName],color:n(`entity.other.attribute-name`)},{tag:[R.function(R.variableName),R.function(R.propertyName),R.macroName],color:n(`entity.name.function`)},{tag:[R.variableName,R.definition(R.variableName)],color:n(`variable`)},{tag:[R.number,R.bool,R.atom],color:n(`constant.numeric`)},{tag:[R.keyword,R.modifier,R.operatorKeyword,R.controlKeyword],color:n(`keyword`)},{tag:[R.string,R.special(R.string),R.docString],color:n(`string`)},{tag:[R.operator],color:n(`keyword.operator`)},{tag:[R.constant(R.variableName),R.literal],color:n(`constant`)},{tag:[R.regexp],color:n(`string.regexp`)},{tag:[R.escape],color:n(`constant.character.escape`)},{tag:[R.heading,R.strong],color:n(`markup.heading`),fontWeight:`bold`},{tag:[R.emphasis],fontStyle:`italic`},{tag:[R.link,R.url],color:n(`markup.underline.link.markdown`),textDecoration:`underline`},{tag:[R.strikethrough],textDecoration:`line-through`},{tag:[R.invalid],color:t[`editor.foreground`]}];return We({theme:e.type,settings:{background:t[`editor.background`],foreground:t[`editor.foreground`],caret:t[`editorCursor.foreground`],selection:t[`editor.selectionBackground`],selectionMatch:t[`editor.selectionBackground`],lineHighlight:t[`editor.lineHighlightBackground`],gutterBackground:t[`editor.background`],gutterForeground:t[`editorLineNumber.foreground`],gutterActiveForeground:t[`editorLineNumber.activeForeground`]},styles:r.filter(e=>e.color!=null||e.fontWeight!=null||e.fontStyle!=null||e.textDecoration!=null)})}var E_=T_(Te),D_=T_(le);function O_(e){let t=(0,X.c)(13),n,r;t[0]===e?(n=t[1],r=t[2]):({basicSetup:n,...r}=e,t[0]=e,t[1]=n,t[2]=r);let{theme:i}=Pr(),a=i===`light`?E_:D_,o;bb0:{let e;t[3]===Symbol.for(`react.memo_cache_sentinel`)?(e={lineNumbers:!0,foldGutter:!0,bracketMatching:!0,syntaxHighlighting:!0,highlightActiveLine:!1,highlightActiveLineGutter:!1},t[3]=e):e=t[3];let r=e;if(n){let e;t[4]===n?e=t[5]:(e={...r,...n},t[4]=n,t[5]=e),o=e;break bb0}o=r}let s=o,c=e.value,l;t[6]===Symbol.for(`react.memo_cache_sentinel`)?(l=qe(),t[6]=l):l=t[6];let u;t[7]===Symbol.for(`react.memo_cache_sentinel`)?(u=[l,Ve.lineWrapping,Ge(Ke())],t[7]=u):u=t[7];let d;return t[8]!==s||t[9]!==a||t[10]!==e.value||t[11]!==r?(d=U(He,{value:c,extensions:u,editable:!1,theme:a,...r,basicSetup:s}),t[8]=s,t[9]=a,t[10]=e.value,t[11]=r,t[12]=d):d=t[12],d}function k_(e){let t=(0,X.c)(6),n;try{let r;if(t[0]!==e){let n=JSON.parse(e);r=JSON.stringify(n,null,2),t[0]=e,t[1]=r}else r=t[1];let i;t[2]===r?i=t[3]:(i={text:r,textType:`json`},t[2]=r,t[3]=i),n=i}catch{let r;t[4]===e?r=t[5]:(r={text:e,textType:`string`},t[4]=e,t[5]=r),n=r}return n}function A_({children:e,preCSS:t}){let{text:n,textType:r}=k_(e);return r===`string`?U(`pre`,{css:G`
          white-space: pre-wrap;
          text-wrap: wrap;
          overflow-wrap: anywhere;
          font-size: var(--global-font-size-s);
          margin: 0;
          ${t}
        `,children:n}):r===`json`?U(O_,{value:n}):dr(r)}var j_=(0,Y.createContext)(null);function M_(){let e=(0,X.c)(1),t=(0,Y.useContext)(j_);if(t===null){console.warn(`useMarkdownMode must be used within a MarkdownDisplayProvider`);let n;e[0]===Symbol.for(`react.memo_cache_sentinel`)?(n={mode:`text`,setMode:N_},e[0]=n):n=e[0],t=n}return t}function N_(){}function P_(e){let t=(0,X.c)(8),n=_i(I_),r=_i(F_),i;t[0]===r?i=t[1]:(i=e=>{(0,Y.startTransition)(()=>{r(e)})},t[0]=r,t[1]=i);let a=i,o;t[2]!==n||t[3]!==a?(o={mode:n,setMode:a},t[2]=n,t[3]=a,t[4]=o):o=t[4];let s;return t[5]!==e.children||t[6]!==o?(s=U(j_.Provider,{value:o,children:e.children}),t[5]=e.children,t[6]=o,t[7]=s):s=t[7],s}function F_(e){return e.setMarkdownDisplayMode}function I_(e){return e.markdownDisplayMode}var L_=G`
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
`,R_={code:In},z_={CopyIcon:()=>U(Ct,{}),CheckIcon:()=>U(_n,{}),DownloadIcon:()=>U(ct,{})};function B_(e){let t=(0,X.c)(7),{children:n,mode:r,renderMode:i,margin:a}=e,o=i===void 0?`static`:i,s=a===void 0?`default`:a,c;t[0]===s?c=t[1]:(c=s===`none`?G`
          margin: 0;
        `:G`
          margin: var(--global-dimension-size-200);
        `,t[0]=s,t[1]=c);let l=c,u;return t[2]!==n||t[3]!==r||t[4]!==o||t[5]!==l?(u=r===`markdown`?U(`div`,{css:[L_,l],children:U(kn,{components:Un,controls:{code:{copy:!0,download:!0},table:!1},icons:z_,mode:o,plugins:R_,children:n})}):U(A_,{preCSS:l,children:n}),t[2]=n,t[3]=r,t[4]=o,t[5]=l,t[6]=u):u=t[6],u}function V_(e){let t=(0,X.c)(5),{children:n,renderMode:r,margin:i}=e,a=i===void 0?`default`:i,{mode:o}=M_(),s;return t[0]!==n||t[1]!==a||t[2]!==o||t[3]!==r?(s=U(B_,{mode:o,renderMode:r,margin:a,children:n}),t[0]=n,t[1]=a,t[2]=o,t[3]=r,t[4]=s):s=t[4],s}function H_(e){return typeof e==`string`?{content:e,position:`top`}:{position:`top`,...e}}function U_(e){let t=(0,X.c)(22),n,r,i,a,o,s;t[0]===e?(n=t[1],r=t[2],i=t[3],a=t[4],o=t[5],s=t[6]):({children:n,ref:a,label:i,tooltip:s,className:r,...o}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a,t[5]=o,t[6]=s);let c;t[7]!==n||t[8]!==r||t[9]!==i||t[10]!==a||t[11]!==o?(c=U(vt,{ref:a,css:b_,className:r,"aria-label":i,...o,children:n}),t[7]=n,t[8]=r,t[9]=i,t[10]=a,t[11]=o,t[12]=c):c=t[12];let l=c;if(!s)return l;let u;t[13]===s?u=t[14]:(u=H_(s),t[13]=s,t[14]=u);let{content:d,position:f}=u,p;t[15]===Symbol.for(`react.memo_cache_sentinel`)?(p=U(sa,{}),t[15]=p):p=t[15];let m;t[16]!==d||t[17]!==f?(m=W(oa,{placement:f,children:[p,d]}),t[16]=d,t[17]=f,t[18]=m):m=t[18];let h;return t[19]!==l||t[20]!==m?(h=W(ve,{delay:500,closeDelay:0,children:[l,m]}),t[19]=l,t[20]=m,t[21]=h):h=t[21],h}var W_=2e3;function G_(e){let t=(0,X.c)(11),{text:n}=e,[r,i]=(0,Y.useState)(!1);if(n.trim().length===0)return null;let a;t[0]===n?a=t[1]:(a=()=>{Fe(n),i(!0),setTimeout(()=>i(!1),W_)},t[0]=n,t[1]=a);let o=a,s=r?`Copied`:`Copy message`,c;t[2]===r?c=t[3]:(c=U(r?_n:Ct,{}),t[2]=r,t[3]=c);let l=r?`success`:`inherit`,u;t[4]!==c||t[5]!==l?(u=U(H,{svg:c,color:l}),t[4]=c,t[5]=l,t[6]=u):u=t[6];let d;return t[7]!==o||t[8]!==s||t[9]!==u?(d=U(U_,{label:`Copy`,tooltip:s,onPress:o,children:u}),t[7]=o,t[8]=s,t[9]=u,t[10]=d):d=t[10],d}function K_(e){let t=(0,X.c)(8),n,r,i;t[0]===e?(n=t[1],r=t[2],i=t[3]):({children:n,ref:r,...i}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i);let a;return t[4]!==n||t[5]!==r||t[6]!==i?(a=U(`div`,{ref:r,css:y_,role:`toolbar`,...i,children:n}),t[4]=n,t[5]=r,t[6]=i,t[7]=a):a=t[7],a}function q_(e){let t=(0,X.c)(8),n,r,i;t[0]===e?(n=t[1],r=t[2],i=t[3]):({children:n,ref:r,...i}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i);let a;return t[4]!==n||t[5]!==r||t[6]!==i?(a=U(`div`,{ref:r,css:x_,...i,children:n}),t[4]=n,t[5]=r,t[6]=i,t[7]=a):a=t[7],a}(0,Y.createContext)(null);var J_=(0,Y.createContext)(null);function Y_(){let e=(0,Y.useContext)(J_);if(!e)throw Error(`usePromptInputContext must be used within a <PromptInput> component`);return e}var X_=G`
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
`,Z_=G`
  flex: 1 1 auto;
  padding: var(--global-dimension-size-200);
  padding-bottom: var(--global-dimension-size-100);
`,Q_=G`
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
`,$_=G`
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--global-dimension-size-100) var(--global-dimension-size-150);
  gap: var(--global-dimension-size-100);
`,ev=G`
  display: flex;
  align-items: center;
  gap: var(--global-dimension-size-50);
`,tv=G`
  display: flex;
  align-items: center;
  gap: var(--global-dimension-size-50);
`,nv=G`
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
`;G`
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
`;function rv({children:e,ref:t,onSubmit:n,status:r=`ready`,isDisabled:i=!1,isSubmitDisabled:a=!1,mode:o=`prompt`,value:s,onValueChange:c,...l}){let[u,d]=(0,Y.useState)(``),f=s!==void 0,p=f?s:u,m=e=>{f||d(e),c?.(e)},h=(0,Y.useRef)(p);h.current=p;let g={status:r,isDisabled:i,onSubmit:()=>{if(a||r===`submitted`||r===`streaming`)return;let e=h.current.trim();e&&(n?.(e),m(``))},value:p,setValue:m};return U(J_.Provider,{value:g,children:U(`div`,{ref:t,css:X_,"data-status":r,"data-input-mode":o,...l,children:e})})}function iv(e){let t=(0,X.c)(8),n,r,i;t[0]===e?(n=t[1],r=t[2],i=t[3]):({children:n,ref:r,...i}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i);let a;return t[4]!==n||t[5]!==r||t[6]!==i?(a=U(`div`,{ref:r,css:Z_,...i,children:n}),t[4]=n,t[5]=r,t[6]=i,t[7]=a):a=t[7],a}function av(e){let t=(0,X.c)(8),n,r,i;t[0]===e?(n=t[1],r=t[2],i=t[3]):({children:n,ref:r,...i}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i);let a;return t[4]!==n||t[5]!==r||t[6]!==i?(a=U(`div`,{ref:r,css:$_,...i,children:n}),t[4]=n,t[5]=r,t[6]=i,t[7]=a):a=t[7],a}function ov(e){let t=(0,X.c)(8),n,r,i;t[0]===e?(n=t[1],r=t[2],i=t[3]):({children:n,ref:r,...i}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i);let a;return t[4]!==n||t[5]!==r||t[6]!==i?(a=U(`div`,{ref:r,css:ev,role:`toolbar`,...i,children:n}),t[4]=n,t[5]=r,t[6]=i,t[7]=a):a=t[7],a}function sv(e){let t=(0,X.c)(8),n,r,i;t[0]===e?(n=t[1],r=t[2],i=t[3]):({children:n,ref:r,...i}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i);let a;return t[4]!==n||t[5]!==r||t[6]!==i?(a=U(`div`,{ref:r,css:tv,...i,children:n}),t[4]=n,t[5]=r,t[6]=i,t[7]=a):a=t[7],a}function cv(e){let t=(0,X.c)(20),{ref:n,placeholder:r,value:i,onChange:a,maxRows:o,"aria-label":s,className:c}=e,l=r===void 0?`Send a message...`:r,u=s===void 0?`Message input`:s,d=Y_(),f=(0,Y.useRef)(null),p=i===void 0?d.value:i,m=a===void 0?d.setValue:a,h;t[0]===n?h=t[1]:(h=e=>{f.current=e,typeof n==`function`?n(e):n&&`current`in n&&(n.current=e)},t[0]=n,t[1]=h);let g=h,_;t[2]===o?_=t[3]:(_=()=>{let e=f.current;if(!e)return;let t=()=>{e.style.height=`auto`;let t=e.scrollHeight;if(o){let n=parseInt(getComputedStyle(e).lineHeight||`20`,10)*o;t=Math.min(t,n)}e.style.height=`${t}px`};t();let n=requestAnimationFrame(t);return()=>{cancelAnimationFrame(n)}},t[2]=o,t[3]=_);let v;t[4]!==o||t[5]!==p?(v=[p,o],t[4]=o,t[5]=p,t[6]=v):v=t[6],(0,Y.useLayoutEffect)(_,v);let{onSubmit:y}=d,b;t[7]===y?b=t[8]:(b=e=>{e.key===`Enter`&&!e.shiftKey&&(e.preventDefault(),y())},t[7]=y,t[8]=b);let x=b,S;t[9]===m?S=t[10]:(S=e=>{m(e.target.value)},t[9]=m,t[10]=S);let C=S,w;return t[11]!==u||t[12]!==c||t[13]!==d.isDisabled||t[14]!==C||t[15]!==x||t[16]!==g||t[17]!==l||t[18]!==p?(w=U(`textarea`,{ref:g,css:Q_,className:c,value:p,onChange:C,onKeyDown:x,placeholder:l,disabled:d.isDisabled,"aria-label":u,rows:1}),t[11]=u,t[12]=c,t[13]=d.isDisabled,t[14]=C,t[15]=x,t[16]=g,t[17]=l,t[18]=p,t[19]=w):w=t[19],w}function lv(e){let t=(0,X.c)(15),{ref:n,onPress:r,isDisabled:i,"aria-label":a,className:o}=e,s=Y_(),c=s.status===`submitted`||s.status===`streaming`,l;t[0]===s.value?l=t[1]:(l=s.value.trim(),t[0]=s.value,t[1]=l);let u=l===``,d=i??(s.status===`ready`&&u),f=!c,p=a??(f?`Send message`:`Stop generation`),m;t[2]!==s||t[3]!==c||t[4]!==r?(m=()=>{if(c){r?.();return}s.onSubmit()},t[2]=s,t[3]=c,t[4]=r,t[5]=m):m=t[5];let h=m,g=d||s.isDisabled,_;t[6]===f?_=t[7]:(_=U(H,{svg:U(f?Ze:Rn,{})}),t[6]=f,t[7]=_);let v;return t[8]!==o||t[9]!==p||t[10]!==h||t[11]!==n||t[12]!==g||t[13]!==_?(v=U(vt,{ref:n,css:nv,className:o,isDisabled:g,onPress:h,"aria-label":p,children:_}),t[8]=o,t[9]=p,t[10]=h,t[11]=n,t[12]=g,t[13]=_,t[14]=v):v=t[14],v}G`
  display: flex;
  align-items: center;
  gap: var(--global-dimension-size-75);
`;var uv=G`
  ${Cn};
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
`,dv=new Map,fv=e=>{let t=dv.get(e);if(t)return t;let n=M.create(e);return dv.set(e,n),n};function pv(e){let t=(0,X.c)(37),n,r,i,a,o,s,c,l,u,d,f,p;t[0]===e?(n=t[1],r=t[2],i=t[3],a=t[4],o=t[5],s=t[6],c=t[7],l=t[8],u=t[9],d=t[10],f=t[11],p=t[12]):({ref:i,children:n,elementType:s,size:c,weight:l,color:u,fontStyle:d,duration:f,spread:p,className:r,style:o,...a}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a,t[5]=o,t[6]=s,t[7]=c,t[8]=l,t[9]=u,t[10]=d,t[11]=f,t[12]=p);let m=s===void 0?`p`:s,h=c===void 0?`S`:c,g=l===void 0?`normal`:l,_=u===void 0?`text-700`:u,v=d===void 0?`normal`:d,y=f===void 0?2:f,b=p===void 0?2:p,x=be(),S=m,C;t[13]===S?C=t[14]:(C=fv(S),t[13]=S,t[14]=C);let w=C,T=(n?.length??0)*b,E;t[15]!==y||t[16]!==x?(E=x?{}:{initial:{backgroundPosition:`100% center`},animate:{backgroundPosition:`0% center`},transition:{duration:y,ease:`linear`,repeat:1/0}},t[15]=y,t[16]=x,t[17]=E):E=t[17];let D=E,O=i,k;t[18]===r?k=t[19]:(k=z(`shimmer`,r),t[18]=r,t[19]=k);let A=`${T}px`,j;t[20]===_?j=t[21]:(j=At(_),t[20]=_,t[21]=j);let M;t[22]!==v||t[23]!==o||t[24]!==A||t[25]!==j?(M={"--shimmer-spread":A,"--shimmer-color":j,fontStyle:v,...o},t[22]=v,t[23]=o,t[24]=A,t[25]=j,t[26]=M):M=t[26];let N=M,P=a,F;return t[27]!==w||t[28]!==D||t[29]!==n||t[30]!==h||t[31]!==O||t[32]!==k||t[33]!==N||t[34]!==P||t[35]!==g?(F=U(w,{ref:O,className:k,"data-size":h,"data-weight":g,css:uv,style:N,...D,...P,children:n}),t[27]=w,t[28]=D,t[29]=n,t[30]=h,t[31]=O,t[32]=k,t[33]=N,t[34]=P,t[35]=g,t[36]=F):F=t[36],F}pv.displayName=`Shimmer`;var $=e=>`var(${e})`,mv=Object.freeze({blue100:$(`--global-color-blue-200`),blue200:$(`--global-color-blue-300`),blue300:$(`--global-color-blue-400`),blue400:$(`--global-color-blue-500`),blue500:$(`--global-color-blue-600`),blue600:$(`--global-color-blue-700`),blue700:$(`--global-color-blue-800`),blue800:$(`--global-color-blue-900`),blue900:$(`--global-color-blue-1000`),orange100:$(`--global-color-orange-500`),orange200:$(`--global-color-orange-600`),orange300:$(`--global-color-orange-700`),orange400:$(`--global-color-orange-800`),orange500:$(`--global-color-orange-900`),purple100:$(`--global-color-purple-100`),purple200:$(`--global-color-purple-200`),purple300:$(`--global-color-purple-300`),purple400:$(`--global-color-purple-400`),purple500:$(`--global-color-purple-500`),magenta100:$(`--global-color-magenta-200`),magenta200:$(`--global-color-magenta-300`),magenta300:$(`--global-color-magenta-400`),magenta400:$(`--global-color-magenta-500`),magenta500:$(`--global-color-magenta-600`),red100:$(`--global-color-red-200`),red200:$(`--global-color-red-300`),red300:$(`--global-color-red-400`),red400:$(`--global-color-red-500`),red500:$(`--global-color-red-600`),gray100:$(`--global-color-gray-100`),gray200:$(`--global-color-gray-200`),gray300:$(`--global-color-gray-300`),gray400:$(`--global-color-gray-400`),gray500:$(`--global-color-gray-500`),gray600:$(`--global-color-gray-600`),gray700:$(`--global-color-gray-700`),default:$(`--global-text-color-900`)});Object.keys(mv);var hv=()=>mv,gv=(e,t)=>{let n=[[`blue`,5],[`orange`,5],[`purple`,5],[`pink`,5],[`gray`,5]],r=n.length,i=e%r,a=Math.floor(e/r),[o,s]=n[i];return t[`${o}${500-a%s*100}`]||t.default},_v={danger:`var(--global-color-red-700)`,success:`var(--global-color-celery-700)`,warning:`var(--global-color-warning)`,info:`var(--global-color-blue-700)`};Object.keys(_v);var vv=()=>_v,yv={category1:`var(--global-color-blue-700)`,category2:`var(--global-color-purple-900)`,category3:`var(--global-color-magenta-600)`,category4:`var(--global-color-indigo-600)`,category5:`var(--global-color-blue-900)`,category6:`var(--global-color-indigo-1100)`,category7:`var(--global-color-orange-600)`,category8:`var(--global-color-celery-400)`,category9:`var(--global-color-seafoam-600)`,category10:`var(--global-color-green-1000)`,category11:`var(--global-color-yellow-400)`,category12:`var(--global-color-red-1100)`},bv={category1:`var(--global-color-blue-700)`,category2:`var(--global-color-purple-800)`,category3:`var(--global-color-magenta-800)`,category4:`var(--global-color-indigo-600)`,category5:`var(--global-color-blue-900)`,category6:`var(--global-color-indigo-1100)`,category7:`var(--global-color-orange-600)`,category8:`var(--global-color-celery-400)`,category9:`var(--global-color-seafoam-600)`,category10:`var(--global-color-green-1000)`,category11:`var(--global-color-yellow-400)`,category12:`var(--global-color-red-1100)`},xv=()=>{let{theme:e}=Pr();return e===`dark`?bv:yv},Sv=Object.keys(yv),Cv=({index:e,colors:t})=>t[Sv[e%Sv.length]],wv={gray1:`var(--global-color-gray-800)`,gray2:`var(--global-color-gray-600)`,gray3:`var(--global-color-gray-500)`,gray4:`var(--global-color-gray-400)`},Tv={gray1:`var(--global-color-gray-800)`,gray2:`var(--global-color-gray-600)`,gray3:`var(--global-color-gray-500)`,gray4:`var(--global-color-gray-400)`},Ev=()=>{let{theme:e}=Pr();return e===`dark`?Tv:wv},Dv=Object.keys(wv),Ov=G`
  width: 100%;
  display: flex;
  flex-direction: row;
  overflow: hidden;
  border-radius: var(--global-rounding-medium);
  gap: 2px;
`,kv=G`
  height: 100%;
  flex-shrink: 0;
  flex-grow: 0;
`,Av=e=>{let t=(0,X.c)(18),{height:n,minimumSegmentPercentage:r,segments:i,totalValue:a}=e,o=n===void 0?6:n,s=r===void 0?0:r,c;t[0]!==a||t[1]!==i?(c=a??i.reduce(jv,0),t[0]=a,t[1]=i,t[2]=c):c=t[2];let l=c,u;t[3]!==s||t[4]!==i?(u=s>0?i.filter(Mv):i,t[3]=s,t[4]=i,t[5]=u):u=t[5];let d=u;if(!d.some(Nv))return null;let f=`${o}px`,p;t[6]===f?p=t[7]:(p={height:f},t[6]=f,t[7]=p);let m;if(t[8]!==s||t[9]!==l||t[10]!==d){let e;t[12]!==s||t[13]!==l?(e=e=>{let t=l>0?e.value/l*100:0,n=e.color,r=e.value>0&&s>0?`${s}%`:void 0;return U(`div`,{css:kv,style:{width:`${t}%`,minWidth:r,flexShrink:r==null?0:1,backgroundColor:n}},e.name)},t[12]=s,t[13]=l,t[14]=e):e=t[14],m=d.map(e),t[8]=s,t[9]=l,t[10]=d,t[11]=m}else m=t[11];let h;return t[15]!==p||t[16]!==m?(h=U(`div`,{style:p,css:Ov,children:m}),t[15]=p,t[16]=m,t[17]=h):h=t[17],h};function jv(e,t){return e+t.value}function Mv(e){return e.value>0}function Nv(e){return e.value>0}function Pv(e){return Math.abs(e)<1e6?Xe(`,`)(e):Xe(`0.2s`)(e).replace(`G`,`B`).replace(`k`,`K`)}function Fv(e){return Math.abs(e)<1e3?Xe(`,`)(e):Xe(`0.2s`)(e).replace(`G`,`B`).replace(`k`,`K`)}function Iv(e){let t=Math.abs(e);if(t===0)return`0.00`;if(t<.01)return Xe(`.2e`)(e);if(t<1){let t=Zv(e,2);return Xe(`0.2f`)(t)}return t<1e3?Xe(`0.2f`)(e):Xe(`0.2s`)(e)}function Lv(e){let t=Math.abs(e);return t===0?`0.00`:t<.01?Xe(`.2e`)(e):t<1e3?Xe(`0.2f`)(e):Xe(`0.2s`)(e).replace(`G`,`B`).replace(`k`,`K`)}function Rv(e){return Xe(`.2f`)(e)+`%`}function zv(e){return Number.isInteger(e)?Pv(e):Iv(e)}function Bv(e){return e===0?`$0`:e<.01?`<$0.01`:e<100?`$${Xe(`0.2f`)(e)}`:e<1e4?`$${Xe(`,`)(e)}`:`$${Xe(`0.2s`)(e).replace(`G`,`B`).replace(`k`,`K`)}`}function Vv(e){let t=Math.floor(e/ua),n=Math.floor(e%ua/la),r=Math.floor(e%la/ca),i=Math.floor(e%ca);if(t>0)return`${t}h${n?` ${n}m`:``}${r?` ${r}s`:``}`;if(n>0)return`${n}m${r?` ${r}s`:``}`;if(r>0){let e=Math.floor(i/100);return`${r}${e>0?`.${e.toFixed(0)}`:``}s`}return`${i.toFixed(0)}ms`}function Hv(e){return t=>typeof t==`number`?e(t):`--`}var Uv=Hv(Pv),Wv=Hv(Fv),Gv=Hv(Lv),Kv=Hv(Iv),qv=Hv(zv),Jv=Hv(Rv),Yv=Hv(Bv),Xv=Hv(Vv);function Zv(e,t){let n=e.toString().split(`.`);return n.length<2?e:Number(n[0]+`.`+n[1].substring(0,t))}var Qv=G`
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
    ${yu}
  }
  .icon-wrap {
    font-size: 1em;
  }
`;function $v({ref:e,...t}){let{children:n,color:r=`text-900`,size:i=`M`,...a}=t,o=At(r),s=typeof n==`number`?zv(n):`--`;return W(`div`,{className:`token-count-item`,"data-size":i,css:Qv,ref:e,...a,children:[U(H,{svg:U(Gn,{}),css:G`
          color: ${o};
        `}),U(B,{size:t.size,color:r,fontFamily:`mono`,children:s})]})}var ey=1e-9,ty={input:0,output:0,cache_read:1,cache_write:2,reasoning:3,audio:4},ny={input:`category1`,output:`category2`,cache_read:`category9`,cache_write:`category7`,reasoning:`category4`,audio:`category3`},ry=[`category5`,`category6`,`category8`,`category10`,`category11`,`category12`];function iy(e){let t=e.split(`_`).join(` `);return t.charAt(0).toUpperCase()+t.slice(1)}function ay(e){return e?`input`:`output`}function oy(e,t){let n=ty[e]??100,r=ty[t]??100;return n===r?e.localeCompare(t):n-r}function sy({colors:e,index:t=0,tokenType:n}){let r=ny[n];return r?e[r]:e[ry[t%ry.length]]}function cy(e){return ry.map(t=>e[t])}var ly=G`
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
`,uy=G`
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
`,dy=G`
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
`,fy=G`
  width: var(--global-dimension-size-100);
  height: var(--global-dimension-size-100);
  flex: none;
  border-radius: var(--global-rounding-full);
`,py=G`
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
`;function my({value:e,maximum:t}){return Math.min(Math.max(e,0),Math.max(t,0))}function hy(e){let t=(0,X.c)(10),{segment:n}=e,r;t[0]===n.color?r=t[1]:(r=U(`span`,{className:`chat-token-usage-details__swatch`,css:fy,style:{backgroundColor:n.color},"aria-hidden":`true`}),t[0]=n.color,t[1]=r);let i;t[2]===n.value?i=t[3]:(i=Fv(n.value),t[2]=n.value,t[3]=i);let a;t[4]!==n.name||t[5]!==i?(a=W(B,{className:`chat-token-usage-details__segment-text`,size:`XS`,color:`text-500`,fontFamily:`mono`,children:[i,` `,n.name]}),t[4]=n.name,t[5]=i,t[6]=a):a=t[6];let o;return t[7]!==r||t[8]!==a?(o=W(V,{children:[r,a]}),t[7]=r,t[8]=a,t[9]=o):o=t[9],o}function gy(e){let t=(0,X.c)(15),{promptSegment:n,promptDetailsSegments:r}=e,i;t[0]===n.value?i=t[1]:(i=Pv(n.value),t[0]=n.value,t[1]=i);let a=`${i} prompt tokens. Show cache details`,o;t[2]===n?o=t[3]:(o=U(hy,{segment:n}),t[2]=n,t[3]=o);let s;t[4]!==a||t[5]!==o?(s=U(Mt,{className:`chat-token-usage-details__segment-trigger`,css:dy,size:`S`,variant:`quiet`,"aria-label":a,children:o}),t[4]=a,t[5]=o,t[6]=s):s=t[6];let c;t[7]===Symbol.for(`react.memo_cache_sentinel`)?(c=U(B,{className:`chat-token-usage-details__tooltip-title`,size:`XS`,color:`text-700`,weight:`heavy`,children:`Prompt details`}),t[7]=c):c=t[7];let l;t[8]===r?l=t[9]:(l=r.map(_y),t[8]=r,t[9]=l);let u;t[10]===l?u=t[11]:(u=W(Da,{css:py,placement:`top`,offset:3,children:[c,U(`ul`,{className:`chat-token-usage-details__tooltip-segments`,"aria-label":`Prompt token types`,children:l})]}),t[10]=l,t[11]=u);let d;return t[12]!==s||t[13]!==u?(d=U(`li`,{className:`chat-token-usage-details__segment`,children:W(ve,{delay:0,closeDelay:0,children:[s,u]})}),t[12]=s,t[13]=u,t[14]=d):d=t[14],d}function _y(e){return U(`li`,{className:`chat-token-usage-details__tooltip-segment`,children:U(hy,{segment:e})},e.name)}function vy(e){let t=(0,X.c)(45),{total:n,prompt:r,completion:i,promptDetails:a}=e,o=xv(),s=a?.cacheRead??0,c;t[0]!==r||t[1]!==s?(c=my({value:s,maximum:r}),t[0]=r,t[1]=s,t[2]=c):c=t[2];let l=c,u=a?.cacheWrite??0,d=Math.max(r-l,0),f;t[3]!==u||t[4]!==d?(f=my({value:u,maximum:d}),t[3]=u,t[4]=d,t[5]=f):f=t[5];let p=f,m=Math.max(r-l-p,0),h=r>0&&(l>0||p>0),g;t[6]!==o.category1||t[7]!==r?(g={name:`Prompt`,value:r,color:o.category1},t[6]=o.category1,t[7]=r,t[8]=g):g=t[8];let _;t[9]!==o.category2||t[10]!==i?(_={name:`Completion`,value:i,color:o.category2},t[9]=o.category2,t[10]=i,t[11]=_):_=t[11];let v;t[12]!==g||t[13]!==_?(v=[g,_],t[12]=g,t[13]=_,t[14]=v):v=t[14];let y=v,b;t[15]===o?b=t[16]:(b=sy({colors:o,tokenType:`input`}),t[15]=o,t[16]=b);let x;t[17]!==b||t[18]!==m?(x={name:`Uncached`,value:m,color:b},t[17]=b,t[18]=m,t[19]=x):x=t[19];let S;t[20]===o?S=t[21]:(S=sy({colors:o,tokenType:`cache_read`}),t[20]=o,t[21]=S);let C;t[22]!==l||t[23]!==S?(C={name:`Cache read`,value:l,color:S},t[22]=l,t[23]=S,t[24]=C):C=t[24];let w;t[25]===o?w=t[26]:(w=sy({colors:o,tokenType:`cache_write`}),t[25]=o,t[26]=w);let T;t[27]!==p||t[28]!==w?(T={name:`Cache write`,value:p,color:w},t[27]=p,t[28]=w,t[29]=T):T=t[29];let E;t[30]!==x||t[31]!==C||t[32]!==T?(E=[x,C,T].filter(yy),t[30]=x,t[31]=C,t[32]=T,t[33]=E):E=t[33];let D=E,O;t[34]!==y||t[35]!==n?(O=U(`div`,{"aria-hidden":`true`,children:U(Av,{height:6,minimumSegmentPercentage:1,totalValue:n,segments:y})}),t[34]=y,t[35]=n,t[36]=O):O=t[36];let k;t[37]===Symbol.for(`react.memo_cache_sentinel`)?(k=U(B,{size:`XS`,color:`text-700`,weight:`heavy`,children:`Total`}),t[37]=k):k=t[37];let A;t[38]!==y||t[39]!==h||t[40]!==D?(A=W(`div`,{className:`chat-token-usage-details__legend`,children:[k,U(`ul`,{className:`chat-token-usage-details__segments`,"aria-label":`Token types`,children:y.map(e=>e.name===`Prompt`&&h?U(gy,{promptSegment:e,promptDetailsSegments:D},e.name):U(`li`,{className:`chat-token-usage-details__segment`,children:U(hy,{segment:e})},e.name))})]}),t[38]=y,t[39]=h,t[40]=D,t[41]=A):A=t[41];let j;return t[42]!==O||t[43]!==A?(j=W(`div`,{className:`chat-token-usage-details`,css:uy,role:`region`,"aria-label":`Token usage breakdown`,children:[O,A]}),t[42]=O,t[43]=A,t[44]=j):j=t[44],j}function yy(e){return e.value>0}function by(e){let t=(0,X.c)(24),{total:n,prompt:r,completion:i,promptDetails:a}=e,[o,s]=(0,Y.useState)(!1),c=(0,Y.useId)(),l;t[0]===n?l=t[1]:(l=Pv(n),t[0]=n,t[1]=l);let u=`${l} total tokens`,d;t[2]===Symbol.for(`react.memo_cache_sentinel`)?(d=()=>s(xy),t[2]=d):d=t[2];let f;t[3]===n?f=t[4]:(f=U($v,{size:`S`,color:`text-300`,children:n}),t[3]=n,t[4]=f);let p;t[5]===o?p=t[6]:(p=U(Kt,{isExpanded:o}),t[5]=o,t[6]=p);let m;t[7]!==c||t[8]!==o||t[9]!==u||t[10]!==f||t[11]!==p?(m=U(`div`,{className:`chat-token-usage__summary`,children:W(`button`,{className:`chat-token-usage__trigger button--reset`,type:`button`,"aria-controls":c,"aria-expanded":o,"aria-label":u,onClick:d,children:[f,p]})}),t[7]=c,t[8]=o,t[9]=u,t[10]=f,t[11]=p,t[12]=m):m=t[12];let h;t[13]!==i||t[14]!==c||t[15]!==o||t[16]!==r||t[17]!==a||t[18]!==n?(h=o?U(`div`,{className:`chat-token-usage__details`,id:c,children:U(vy,{total:n,prompt:r,completion:i,promptDetails:a})}):null,t[13]=i,t[14]=c,t[15]=o,t[16]=r,t[17]=a,t[18]=n,t[19]=h):h=t[19];let g;return t[20]!==o||t[21]!==m||t[22]!==h?(g=W(`div`,{className:`chat-token-usage`,css:ly,"data-expanded":o,children:[m,h]}),t[20]=o,t[21]=m,t[22]=h,t[23]=g):g=t[23],g}function xy(e){return!e}var Sy=(0,Y.createContext)(null);function Cy(){return(0,Y.useContext)(Sy)}function wy(e){let t=e.parentElement;for(;t;){let{overflowY:e}=getComputedStyle(t);if((e===`auto`||e===`scroll`)&&t.scrollHeight>t.clientHeight)return t;t=t.parentElement}return null}function Ty(){let e=(0,X.c)(5),t=Cy(),n=(0,Y.useRef)(null),r;e[0]===t?r=e[1]:(r=e=>{if(t?.stopScroll(),n.current=null,!e)return;let r=wy(e);if(!r)return;let i=e.getBoundingClientRect(),a=r.getBoundingClientRect();n.current={scrollParent:r,offsetFromParentTop:i.top-a.top}},e[0]=t,e[1]=r);let i=r,a;e[2]===Symbol.for(`react.memo_cache_sentinel`)?(a=e=>{let t=n.current;if(n.current=null,!t||!e)return;let{scrollParent:r,offsetFromParentTop:i}=t,a=e.getBoundingClientRect(),o=r.getBoundingClientRect(),s=a.top-o.top;r.scrollTop+=s-i},e[2]=a):a=e[2];let o=a,s;return e[3]===i?s=e[4]:(s={capture:i,restore:o},e[3]=i,e[4]=s),s}var Ey=Ht`
  from {
    opacity: 0;
    transform: translateY(-2px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
`,Dy={titleFlex:`0 1 auto`,titleMinWidth:`0`,titleMaxWidth:`55%`,middleFlex:`1 1 50px`,middleMinWidth:`50px`,statusFlex:`0 1 auto`,statusMinWidth:`0`,statusMaxWidth:`none`};function Oy(e){let t=(0,X.c)(3),{children:n,variant:r}=e,i;return t[0]!==n||t[1]!==r?(i=U(`div`,{className:`tool-part__line`,children:U(`span`,{className:`tool-part__label`,"data-variant":r,children:n})}),t[0]=n,t[1]=r,t[2]=i):i=t[2],i}function ky(e){let t=(0,X.c)(9),{children:n,allowCopy:r}=e,i=r===void 0||r,a=`tool-part__line${i?` tool-part__line--copyable`:``}`,o=n||`(empty)`,s;t[0]===o?s=t[1]:(s=U(`code`,{className:`tool-part__code`,children:o}),t[0]=o,t[1]=s);let c;t[2]!==i||t[3]!==n?(c=i?U(Na,{text:n,size:`S`,variant:`quiet`,tooltipText:`Copy`}):null,t[2]=i,t[3]=n,t[4]=c):c=t[4];let l;return t[5]!==a||t[6]!==s||t[7]!==c?(l=W(`div`,{className:a,children:[s,c]}),t[5]=a,t[6]=s,t[7]=c,t[8]=l):l=t[8],l}function Ay(e){let t=(0,X.c)(3),{children:n,variant:r}=e,i;return t[0]!==n||t[1]!==r?(i=U(`span`,{className:`tool-part__status`,"data-variant":r,children:n}),t[0]=n,t[1]=r,t[2]=i):i=t[2],i}function jy(e){let t=(0,X.c)(4),{items:n}=e,r;t[0]===n?r=t[1]:(r=n.map(My),t[0]=n,t[1]=r);let i;return t[2]===r?i=t[3]:(i=U(`div`,{className:`tool-part__meta`,children:r}),t[2]=r,t[3]=i),i}function My(e){let{label:t,value:n}=e;return W(`span`,{className:`tool-part__meta-group`,children:[U(`span`,{className:`tool-part__meta-label`,children:t}),U(`code`,{className:`tool-part__meta-value`,children:n})]},t)}var Ny=G`
  padding: var(--global-dimension-size-50) var(--global-dimension-size-200)
    var(--global-dimension-size-150);
`;function Py(e){let t=(0,X.c)(15),{onAccept:n,onReject:r,isDisabled:i,staleMessage:a}=e,o=i!==void 0&&i,s=_h(Fy),c=o||s,l;t[0]!==c||t[1]!==n?(l=U(Mt,{size:`S`,variant:`primary`,isDisabled:c,onPress:n,children:`Accept`}),t[0]=c,t[1]=n,t[2]=l):l=t[2];let u;t[3]!==c||t[4]!==r?(u=U(Mt,{size:`S`,isDisabled:c,onPress:r,children:`Reject`}),t[3]=c,t[4]=r,t[5]=u):u=t[5];let d;t[6]!==l||t[7]!==u?(d=U(`div`,{css:Ny,children:W(K,{direction:`row-reverse`,gap:`size-100`,children:[l,u]})}),t[6]=l,t[7]=u,t[8]=d):d=t[8];let f;t[9]!==o||t[10]!==a?(f=o&&a?U(ky,{children:a}):null,t[9]=o,t[10]=a,t[11]=f):f=t[11];let p;return t[12]!==d||t[13]!==f?(p=W(V,{children:[d,f]}),t[12]=d,t[13]=f,t[14]=p):p=t[14],p}function Fy(e){return Qm(e,e.activeSessionId)}var Iy=320,Ly=G`
  --expandable-content-overlay-background-color: var(
    --tool-call-body-background-color
  );
`;function Ry(e){let t=(0,X.c)(6),{children:n}=e,r=(0,Y.useRef)(null),[i,a]=(0,Y.useState)(!1),o=Ty(),s;t[0]===o?s=t[1]:(s=e=>{o.capture(r.current),a(e),requestAnimationFrame(()=>o.restore(r.current))},t[0]=o,t[1]=s);let c=s,l;return t[2]!==n||t[3]!==c||t[4]!==i?(l=U(`div`,{ref:r,css:Ly,children:U($e,{height:Iy,expandedBehavior:`grow`,isExpanded:i,onExpandedChange:c,children:n})}),t[2]=n,t[3]=c,t[4]=i,t[5]=l):l=t[5],l}function zy(e){switch(e){case`input-streaming`:return`Preparing`;case`input-available`:return`Running`;case`approval-requested`:return`Awaiting approval`;case`approval-responded`:return`Approval received`;case`output-available`:return`Completed`;case`output-error`:return`Error`;case`output-denied`:return`Denied`;default:return dr(e)}}function By(e){if(e==null)return``;if(typeof e==`string`)return e;try{return JSON.stringify(e,null,2)}catch{return String(e)}}export{q_ as $,ni as $a,Da as $i,Ju as $n,$s as $r,_h as $t,Rv as A,Ri as Aa,bo as Ai,kp as An,tl as Ar,sg as At,xv as B,Ei as Ba,Qa as Bi,uf as Bn,jc as Br,Kh as Bt,Kv as C,Bi as Ca,rs as Ci,vp as Cn,mr as Co,vl as Cr,Fg as Ct,Pv as D,Ni as Da,Go as Di,Tp as Dn,ul as Dr,kg as Dt,Iv as E,Pi as Ea,Jo as Ei,fp as En,dl as Er,Ag as Et,Jv as F,ji as Fa,co as Fi,Nf as Fn,qc as Fr,Zh as Ft,lv as G,gi as Ga,Ka as Gi,ad as Gn,yc as Gr,Mh as Gt,vv as H,Oi as Ha,Xa as Hi,sf as Hn,Ec as Hr,zh as Ht,Av as I,wi as Ia,io as Ii,vf as In,Hc as Ir,Xh as It,ov as J,di as Ja,Ra as Ji,sd as Jn,lc as Jr,wh as Jt,cv as K,_i as Ka,Wa as Ki,cd as Kn,_c as Kr,Nh as Kt,Dv as L,Ti as La,no as Li,_f as Ln,zc as Lr,Yh as Lt,Wv as M,Ui as Ma,mo as Mi,gp as Mn,Jc as Mr,ag as Mt,Xv as N,Vi as Na,po as Ni,xp as Nn,Xc as Nr,tg as Nt,Fv as O,Ii as Oa,Po as Oi,Dp as On,al as Or,lg as Ot,qv as P,Hi as Pa,lo as Pi,Z as Pn,Gc as Pr,$h as Pt,Y_ as Q,ui as Qa,Na as Qi,ed as Qn,tc as Qr,gh as Qt,Cv as R,Si as Ra,to as Ri,ff as Rn,Nc as Rr,Vh as Rt,Yv as S,Li as Sa,ls as Si,Sp as Sn,_r as So,wl as Sr,Ig as St,Bv as T,Fi as Ta,Xo as Ti,pp as Tn,fl as Tr,Lg as Tt,hv as U,Ci as Ua,Ia as Ui,md as Un,Oc as Ur,Lh as Ut,Ev as V,Di as Va,Ya as Vi,cf as Vn,Tc as Vr,Bh as Vt,pv as W,ki as Wa,Va as Wi,hd as Wn,xc as Wr,Ih as Wt,iv as X,li as Xa,Fa as Xi,id as Xn,ac as Xr,xh as Xt,av as Y,si as Ya,Ua as Yi,od as Yn,sc as Yr,bh as Yt,rv as Z,ci as Za,qa as Zi,rd as Zn,rc as Zr,Sh as Zt,ay as _,ea as _a,vs as _i,jp as _n,Sr as _o,Pl as _r,Hg as _t,Py as a,Ca as aa,Us as ai,Qm as an,Xr as ao,yu as ar,P_ as at,iy as b,Ki as ba,os as bi,wp as bn,gr as bo,Ol as br,jg as bt,Oy as c,_a as ca,Ps as ci,Hm as cn,Ur as co,lu as cr,D_ as ct,wy as d,ha as da,Os as di,Um as dn,Fr as do,Xl as dr,S_ as dt,Aa as ea,Ys as ei,vh as en,Qr as eo,Bu as er,K_ as et,Ty as f,pa as fa,Es as fi,Km as fn,Dr as fo,ql as fr,h_ as ft,oy as g,ta as ga,_s as gi,Xm as gn,Cr as go,Il as gr,Yg as gt,ey as h,ra as ha,ys as hi,qm as hn,xr as ho,Rl as hr,r_ as ht,Ey as i,Ta as ia,Ws as ii,ah as in,Yr as io,_u as ir,B_ as it,Uv as j,Wi as ja,_o as ji,Op as jn,Zc as jr,og as jt,zv as k,Mi as ka,jo as ki,hp as kn,il as kr,cg as kt,jy as l,fa as la,js as li,Ym as ln,Hr as lo,ou as lr,E_ as lt,by as m,oa as ma,bs as mi,Jm as mn,br as mo,Ul as mr,i_ as mt,By as n,Oa as na,Ks as ni,sh as nn,ii as no,Lu as nr,U_ as nt,ky as o,ya as oa,Vs as oi,Zm as on,Br as oo,bu as or,M_ as ot,Sy as p,sa as pa,Ss as pi,Gm as pn,Pr as po,Gl as pr,a_ as pt,sv as q,pi as qa,Ga as qi,ld as qn,hc as qr,Ah as qt,Dy as r,Ea as ra,Gs as ri,oh as rn,Zr as ro,vu as rr,V_ as rt,Ry as s,ga as sa,Fs as si,mh as sn,Rr as so,uu as sr,O_ as st,zy as t,ka as ta,Zs as ti,$m as tn,ri as to,Ru as tr,G_ as tt,Ay as u,ma as ua,ks as ui,Wm as un,Lr as uo,$l as ur,C_ as ut,sy as v,Yi as va,us as vi,_p as vn,dr as vo,jl as vr,Bg as vt,Gv as w,zi as wa,ts as wi,mp as wn,vr as wo,pl as wr,Rg as wt,$v as x,Gi as xa,cs as xi,Ep as xn,hr as xo,El as xr,Mg as xt,cy as y,qi as ya,ss as yi,Cp as yn,fr as yo,Al as yr,zg as yt,gv as z,Ai as za,eo as zi,df as zn,Fc as zr,qh as zt};