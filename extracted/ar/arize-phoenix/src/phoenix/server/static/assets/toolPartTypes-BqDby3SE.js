import{s as e}from"./rolldown-runtime-BcKkbAw3.js";import{$n as t,$t as n,An as r,Bn as i,Cn as a,Cr as o,Dn as s,Dr as c,En as l,Hn as u,In as d,Jn as f,Ln as p,Mn as m,On as h,Pn as g,Qn as _,Rn as v,Sn as y,Sr as b,Tn as x,Tt as S,Un as C,Vn as w,Wn as T,Xn as E,Yn as D,Zn as O,_r as k,ar as A,at as j,bn as M,br as N,cn as P,cr as F,ct as I,dr as L,en as R,er as ee,fn as te,fr as ne,gn as re,gt as ie,hn as ae,hr as oe,ht as se,in as ce,it as le,jn as ue,kn as de,ln as fe,lr as pe,mn as me,mr as he,nr as ge,on as _e,or as ve,ot as ye,pn as be,pr as xe,qn as Se,rn as Ce,rr as we,sn as Te,sr as Ee,st as De,tn as Oe,un as ke,vr as Ae,vt as je,wt as Me,xn as Ne,xr as Pe,xt as Fe,yn as Ie,yr as Le,yt as Re,zn as ze}from"./vendor-CGXZFvlB.js";import{D as Be,M as z,d as Ve,rt as He,u as Ue,v as We,x as Ge,y as Ke}from"./vendor-codemirror-Dj-jduiy.js";import{C as B,b as qe,w as Je,y as Ye}from"./vendor-recharts-Cx47-5QL.js";import{$ as Xe,A as Ze,Ai as Qe,An as $e,Ba as et,Bt as tt,C as nt,Ct as rt,D as V,Di as it,E as at,En as ot,F as st,Fn as ct,Fo as H,Ft as lt,G as U,Gn as ut,Gt as dt,H as ft,Ha as pt,Hn as mt,Hr as ht,Ht as gt,Io as _t,It as vt,J as yt,Ja as bt,Ji as xt,Jr as St,Jt as Ct,K as wt,Kr as Tt,Kt as Et,L as Dt,M as Ot,Ma as kt,Nn as At,No as W,Nt as jt,O as Mt,P as Nt,Po as G,Qn as Pt,Qr as Ft,R as It,S as Lt,Si as Rt,T as zt,Ti as Bt,Tt as Vt,Un as Ht,Ut,Vi as Wt,Vr as Gt,Vt as Kt,W as qt,Wi as Jt,Wr as Yt,Wt as Xt,Y as Zt,Yr as Qt,aa as $t,an as en,ar as tn,bn as nn,cn as rn,cr as an,ct as on,fn as sn,fr as cn,gr as ln,gt as un,ht as dn,i as fn,ii as pn,in as mn,j as hn,ja as gn,jn as _n,jt as vn,k as yn,kn as bn,li as xn,lr as Sn,m as Cn,mn as wn,mr as Tn,mt as En,n as Dn,na as On,oi as kn,on as An,p as jn,pr as Mn,q as Nn,qr as Pn,r as Fn,rt as In,sn as Ln,t as Rn,ta as zn,tr as Bn,ua as Vn,vt as Hn,wo as Un,wt as Wn,x as Gn,xn as Kn,y as qn,yn as Jn,yr as Yn,yt as Xn,z as K,zi as Zn,zr as q,zt as Qn}from"./vendor-streamdown-DicArkC7.js";import{Bt as $n,En as er,Nt as tr,Qn as J,Rn as Y,Tn as nr,Wt as rr,dr as ir,en as ar,qn as or,s as sr,ur as cr,zn as lr}from"./vendor-ai-sdk-react-CwOyc_X3.js";var X=e(He()),ur=e(Je()),Z=_t();function dr(e){throw Error(`Unreachable`)}function fr(e){return typeof e==`number`||e===null}function pr(e){return typeof e==`string`||e===null}function mr(e){return pr(e)||e===void 0}function hr(e){return Array.isArray(e)?e.every(e=>typeof e==`string`):!1}function gr(e){return typeof e==`object`&&!!e}function _r(e){return gr(e)&&Object.keys(e).every(e=>typeof e==`string`)}var vr=()=>e=>e;(0,X.createContext)(null);var yr=5e3,br=new ae({maxVisibleToasts:3}),xr=()=>wr,Sr=()=>Tr,Cr=()=>Er;function wr(e){let{expireMs:t,...n}=e,r=t===void 0?yr:t;return br.add({...n},r===null?void 0:{timeout:r})}function Tr(e){let{expireMs:t,...n}=e,r=t===void 0?yr:t;return br.add({...n,variant:`success`},r===null?void 0:{timeout:r})}function Er(e){let{expireMs:t,...n}=e,r=t===void 0?yr:t;return br.add({...n,variant:`error`},r===null?void 0:{timeout:r})}function Dr(e){return e===`light`||e===`dark`||e===`system`}var Or=`arize-phoenix-theme`,kr=`dark`,Ar=`(prefers-color-scheme: dark)`;function jr(){let e=localStorage.getItem(Or);return Dr(e)?e:kr}function Mr(){return window.matchMedia(Ar).matches?`dark`:`light`}var Nr=(0,X.createContext)(null);function Pr(){let e=(0,X.useContext)(Nr);if(e===null)throw Error(`useTheme must be used within a ThemeProvider`);return e}function Fr(e){let t=(0,Z.c)(19),n;t[0]===e.themeMode?n=t[1]:(n=()=>e.themeMode||jr(),t[0]=e.themeMode,t[1]=n);let[r,i]=(0,X.useState)(n),a;t[2]===Symbol.for(`react.memo_cache_sentinel`)?(a=e=>{localStorage.setItem(Or,e),i(e)},t[2]=a):a=t[2];let o=a,[s,c]=(0,X.useState)(Mr),l;bb0:{if(r===`system`){l=s;break bb0}l=r}let u=l,d,f;t[3]===e.themeMode?(d=t[4],f=t[5]):(d=()=>{e.themeMode&&i(e.themeMode)},f=[e.themeMode,o],t[3]=e.themeMode,t[4]=d,t[5]=f),(0,X.useEffect)(d,f);let p,m;t[6]===Symbol.for(`react.memo_cache_sentinel`)?(p=()=>{let e=window.matchMedia(Ar),t=()=>{c(Mr())};return e.addEventListener(`change`,t),()=>{e.removeEventListener(`change`,t)}},m=[],t[6]=p,t[7]=m):(p=t[6],m=t[7]),(0,X.useEffect)(p,m);let h,g;t[8]!==e.disableBodyTheme||t[9]!==u?(h=()=>{if(!e.disableBodyTheme)return document.body.classList.add(`theme--${u}`),document.body.classList.add(`theme`),()=>{document.body.classList.remove(`theme--${u}`),document.body.classList.remove(`theme`)}},g=[u,e.disableBodyTheme],t[8]=e.disableBodyTheme,t[9]=u,t[10]=h,t[11]=g):(h=t[10],g=t[11]),(0,X.useEffect)(h,g);let _;t[12]!==s||t[13]!==u||t[14]!==r?(_={theme:u,systemTheme:s,themeMode:r,setThemeMode:o},t[12]=s,t[13]=u,t[14]=r,t[15]=_):_=t[15];let v;return t[16]!==e.children||t[17]!==_?(v=G(Nr.Provider,{value:_,children:e.children}),t[16]=e.children,t[17]=_,t[18]=v):v=t[18],v}var Ir=[`traces`,`spans`,`sessions`,`metrics`],Lr=e=>Ir.includes(e),Rr=[`traffic`,`traces`,`latency`,`cost`,`top_models_by_cost`,`tokens`,`top_models_by_tokens`,`prompt_token_details`,`completion_token_details`,`llm_spans`,`llm_span_errors`,`tool_spans`,`tool_span_errors`,`span_annotations`,`trace_annotations`,`session_annotations`],zr=[`spans`,`traces`,`sessions`],Br=`Evaluation results over time`,Vr=`_annotation:`;function Hr({view:e,annotationName:t}){return`${e}${Vr}${t}`}function Ur(e){for(let t of zr){let n=`${t}${Vr}`;if(e.startsWith(n))return{view:t,annotationName:e.slice(n.length)}}}var Wr=e=>Rr.includes(e)||Ur(e)!=null,Gr={spans:[`traffic`],traces:[`traces`,`latency`,`trace_annotations`],sessions:[`traces`,`session_annotations`]},Kr=e=>`arize-phoenix-project-${e}`;function qr({projectId:e}){return{state:Oe()(R(n(e=>({defaultTab:`spans`,setDefaultTab:t=>{e({defaultTab:t},!1,{type:`setDefaultTab`})},showTableAside:!0,setShowTableAside:t=>{e({showTableAside:t},!1,{type:`setShowTableAside`})},metricChartKeys:Gr,setMetricChartKeys:(t,n)=>{e(e=>({metricChartKeys:{...e.metricChartKeys,[t]:n}}),!1,{type:`setMetricChartKeys`})}})),{name:Kr(e),merge:(e,t)=>{let n={...t,...e},r={...Gr};for(let e of zr){let t=n.metricChartKeys?.[e];Array.isArray(t)&&(r[e]=t.filter(Wr))}return n.metricChartKeys=r,n}}))}}var Jr=(0,X.createContext)(null);function Yr(e){let t=(0,Z.c)(5),{children:n,projectId:r}=e,i;t[0]===r?i=t[1]:(i=()=>qr({projectId:r}),t[0]=r,t[1]=i);let[a]=(0,X.useState)(i),o;return t[2]!==n||t[3]!==a?(o=G(Jr.Provider,{value:a,children:n}),t[2]=n,t[3]=a,t[4]=o):o=t[4],o}function Xr(e,t){let n=(0,X.useContext)(Jr);if(!n)throw Error(`Missing ProjectContext.Provider in the tree`);return Ce(n.state,e,t)}var Zr=[`Python`,`TypeScript`];function Qr(e){return typeof e==`string`&&Zr.includes(e)}var $r=[`npm`,`pnpm`,`bun`],ei=[`pip`,`uv`],ti=[...$r,...ei];function ni(e){return typeof e==`string`&&ti.includes(e)}function ri(e){return typeof e==`string`&&ei.includes(e)}function ii(e){return typeof e==`string`&&$r.includes(e)}var ai=Intl.DateTimeFormat().resolvedOptions(),oi=[];function si(){return ai.locale}function ci(){return ai.timeZone}function li(){return oi.length===0&&(oi=[...Intl.supportedValuesOf(`timeZone`)],oi.includes(`UTC`)||(oi=[`UTC`,...oi])),Object.freeze([...oi])}function ui(e,t){let n=new Intl.DateTimeFormat(`en-US`,{timeZone:t,year:`numeric`,month:`2-digit`,day:`2-digit`,hour:`2-digit`,minute:`2-digit`,second:`2-digit`,hour12:!1}).formatToParts(e).reduce((e,t)=>(t.type!==`literal`&&(e[t.type]=t.value),e),{}),{year:r,month:i,day:a}=n,o=n.hour;if(o===`24`){o=`00`;let e=new Date(`${r}-${i}-${a}T00:00:00Z`);e.setUTCDate(e.getUTCDate()+1),r=String(e.getUTCFullYear()),i=String(e.getUTCMonth()+1).padStart(2,`0`),a=String(e.getUTCDate()).padStart(2,`0`)}let s=`${r}-${i}-${a}`,c=`${o}:${n.minute}:${n.second}`,l=new Date(`${s}T${c}Z`).getTime(),u=Math.round((l-e.getTime())/6e4),d=u>=0?`+`:`-`,f=Math.abs(u);return`${s}T${c}${d}${String(Math.floor(f/60)).padStart(2,`0`)}:${String(f%60).padStart(2,`0`)}`}var di={Python:ei,TypeScript:$r},fi={Python:`pip`,TypeScript:`npm`},pi=[``,`apac`,`au`,`ca`,`eu`,`global`,`il`,`jp`,`us`,`us-gov`],mi=e=>Oe()(R(n(t=>({markdownDisplayMode:`text`,setMarkdownDisplayMode:e=>{t({markdownDisplayMode:e},!1,{type:`setMarkdownDisplayMode`})},traceStreamingEnabled:!0,setTraceStreamingEnabled:e=>{t({traceStreamingEnabled:e},!1,{type:`setTraceStreamingEnabled`})},lastNTimeRangeKey:`7d`,setLastNTimeRangeKey:e=>{t({lastNTimeRangeKey:e})},projectsAutoRefreshEnabled:!0,setProjectAutoRefreshEnabled:e=>{t({projectsAutoRefreshEnabled:e},!1,{type:`setProjectAutoRefreshEnabled`})},showMetricsInTraceTree:!0,setShowMetricsInTraceTree:e=>{t({showMetricsInTraceTree:e},!1,{type:`setShowMetricsInTraceTree`})},areTableRowsExpanded:!1,setAreTableRowsExpanded:e=>{t({areTableRowsExpanded:e},!1,{type:`setAreTableRowsExpanded`})},modelConfigByProvider:{},setModelConfigForProvider:({provider:e,modelConfig:n})=>{t(t=>({modelConfigByProvider:{...t.modelConfigByProvider,[e]:n}}),!1,{type:`setModelConfigForProvider`})},playgroundStreamingEnabled:!0,setPlaygroundStreamingEnabled:e=>{t({playgroundStreamingEnabled:e},!1,{type:`setPlaygroundStreamingEnabled`})},isAnnotatingSpans:!1,setIsAnnotatingSpans:e=>{t({isAnnotatingSpans:e},!1,{type:`setIsAnnotatingSpans`})},isTakingSpanNotes:!1,setIsTakingSpanNotes:e=>{t({isTakingSpanNotes:e},!1,{type:`setIsTakingSpanNotes`})},projectViewMode:`grid`,setProjectViewMode:e=>{t({projectViewMode:e},!1,{type:`setProjectViewMode`})},projectSortOrder:{column:`endTime`,direction:`desc`},setProjectSortOrder:e=>{t({projectSortOrder:e},!1,{type:`setProjectSortOrder`})},lastSelectedDashboardProjectId:void 0,setLastSelectedDashboardProjectId:e=>{t({lastSelectedDashboardProjectId:e},!1,{type:`setLastSelectedDashboardProjectId`})},isSideNavExpanded:!0,setIsSideNavExpanded:e=>{t({isSideNavExpanded:e},!1,{type:`setIsSideNavExpanded`})},setDisplayTimezone:e=>{if(e&&!li().includes(e))throw Error(`Invalid timezone: ${e}`);t({displayTimezone:e},!1,{type:`setDisplayTimezone`})},programmingLanguage:`Python`,setProgrammingLanguage:e=>{t({programmingLanguage:e},!1,{type:`setProgrammingLanguage`})},packageManagerByLanguage:{...fi},setPackageManager:(e,n)=>{t(t=>({packageManagerByLanguage:{...t.packageManagerByLanguage,[e]:n}}),!1,{type:`setPackageManager`})},awsBedrockModelPrefix:`us`,setAwsBedrockModelPrefix:e=>{t({awsBedrockModelPrefix:e},!1,{type:`setAwsBedrockModelPrefix`})},isAssistantAgentEnabled:!0,setIsAssistantAgentEnabled:e=>{t({isAssistantAgentEnabled:e},!1,{type:`setIsAssistantAgentEnabled`})},defaultModelProvider:void 0,setDefaultModelProvider:e=>{t({defaultModelProvider:e},!1,{type:`setDefaultModelProvider`})},defaultModelName:void 0,setDefaultModelName:e=>{let n=e?.trim();t({defaultModelName:n||void 0},!1,{type:`setDefaultModelName`})},isAIQueryEnabled:!0,setIsAIQueryEnabled:e=>{t({isAIQueryEnabled:e},!1,{type:`setIsAIQueryEnabled`})},aiQueryModelConfig:void 0,setAIQueryModelConfig:e=>{t({aiQueryModelConfig:e},!1,{type:`setAIQueryModelConfig`})},...e}),{name:`preferencesStore`}),{name:`arize-phoenix-preferences`})),hi=(0,X.createContext)(null);function gi(e){let t=(0,Z.c)(8),n,r;t[0]===e?(n=t[1],r=t[2]):({children:n,...r}=e,t[0]=e,t[1]=n,t[2]=r);let i;t[3]===r?i=t[4]:(i=()=>mi(r),t[3]=r,t[4]=i);let[a]=(0,X.useState)(i),o;return t[5]!==n||t[6]!==a?(o=G(hi.Provider,{value:a,children:n}),t[5]=n,t[6]=a,t[7]=o):o=t[7],o}function _i(e,t){let n=(0,X.useContext)(hi);if(!n)throw Error(`Missing PreferencesContext.Provider in the tree`);return Ce(n,e,t)}var vi=function(){var e={alias:null,args:null,kind:`ScalarField`,name:`id`,storageKey:null},t={alias:null,args:null,kind:`ScalarField`,name:`name`,storageKey:null},n={alias:null,args:null,kind:`ScalarField`,name:`createdAt`,storageKey:null},r={alias:null,args:null,kind:`ScalarField`,name:`expiresAt`,storageKey:null};return{fragment:{argumentDefinitions:[],kind:`Fragment`,metadata:null,name:`ViewerContextRefetchQuery`,selections:[{args:null,kind:`FragmentSpread`,name:`ViewerContext_viewer`}],type:`Query`,abstractKey:null},kind:`Request`,operation:{argumentDefinitions:[],kind:`Operation`,name:`ViewerContextRefetchQuery`,selections:[{alias:null,args:null,concreteType:`User`,kind:`LinkedField`,name:`viewer`,plural:!1,selections:[e,{alias:null,args:null,kind:`ScalarField`,name:`username`,storageKey:null},{alias:null,args:null,kind:`ScalarField`,name:`email`,storageKey:null},{alias:null,args:null,kind:`ScalarField`,name:`profilePictureUrl`,storageKey:null},{alias:null,args:null,kind:`ScalarField`,name:`isManagementUser`,storageKey:null},{alias:null,args:null,concreteType:`UserRole`,kind:`LinkedField`,name:`role`,plural:!1,selections:[t,e],storageKey:null},{alias:null,args:null,kind:`ScalarField`,name:`authMethod`,storageKey:null},{alias:null,args:null,concreteType:`UserApiKey`,kind:`LinkedField`,name:`apiKeys`,plural:!0,selections:[e,t,{alias:null,args:null,kind:`ScalarField`,name:`description`,storageKey:null},n,r],storageKey:null},{alias:null,args:null,concreteType:`OAuth2Grant`,kind:`LinkedField`,name:`oauth2Grants`,plural:!0,selections:[e,{alias:null,args:null,kind:`ScalarField`,name:`clientName`,storageKey:null},{alias:null,args:null,kind:`ScalarField`,name:`clientId`,storageKey:null},{alias:null,args:null,kind:`ScalarField`,name:`isFirstParty`,storageKey:null},{alias:null,args:null,kind:`ScalarField`,name:`scopes`,storageKey:null},n,r,{alias:null,args:null,kind:`ScalarField`,name:`lastUsedAt`,storageKey:null}],storageKey:null}],storageKey:null}]},params:{cacheID:`67fdf1bb616d5781701a75f68282f178`,id:null,metadata:{},name:`ViewerContextRefetchQuery`,operationKind:`query`,text:`query ViewerContextRefetchQuery {
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
`}}}();vi.hash=`53341d080ff76da24b2f1bc9e36c4e23`;var yi={argumentDefinitions:[],kind:`Fragment`,metadata:{refetch:{connection:null,fragmentPathInResult:[],operation:vi}},name:`ViewerContext_viewer`,selections:[{alias:null,args:null,concreteType:`User`,kind:`LinkedField`,name:`viewer`,plural:!1,selections:[{alias:null,args:null,kind:`ScalarField`,name:`id`,storageKey:null},{alias:null,args:null,kind:`ScalarField`,name:`username`,storageKey:null},{alias:null,args:null,kind:`ScalarField`,name:`email`,storageKey:null},{alias:null,args:null,kind:`ScalarField`,name:`profilePictureUrl`,storageKey:null},{alias:null,args:null,kind:`ScalarField`,name:`isManagementUser`,storageKey:null},{alias:null,args:null,concreteType:`UserRole`,kind:`LinkedField`,name:`role`,plural:!1,selections:[{alias:null,args:null,kind:`ScalarField`,name:`name`,storageKey:null}],storageKey:null},{alias:null,args:null,kind:`ScalarField`,name:`authMethod`,storageKey:null},{args:null,kind:`FragmentSpread`,name:`ViewerAPIKeysListFragment`},{args:null,kind:`FragmentSpread`,name:`AuthorizedApplicationsCardFragment`}],storageKey:null}],type:`Query`,abstractKey:null};yi.hash=`53341d080ff76da24b2f1bc9e36c4e23`;var bi=c(),xi=X.createContext({viewer:null,refetchViewer:()=>{}});function Si(){let e=X.useContext(xi);if(e==null)throw Error(`useViewer must be used within a ViewerProvider`);return e}function Ci(){let{viewer:e}=Si();return!(e&&e.role.name===`VIEWER`)}function wi(){let e=Ti();return!window.Config.authenticationEnabled||e}function Ti(){let{viewer:e}=Si();return window.Config.authenticationEnabled&&e?.role?.name===`ADMIN`}function Ei(){return wi()}function Di(){return wi()}function Oi(){return wi()}function ki(){return wi()}function Ai(){return wi()}function ji(e){let t=(0,Z.c)(9),{query:n,children:r}=e,i;t[0]===Symbol.for(`react.memo_cache_sentinel`)?(i=yi,t[0]=i):i=t[0];let[a,o]=(0,bi.useRefetchableFragment)(i,n),s;t[1]===o?s=t[2]:(s=()=>{(0,X.startTransition)(()=>{o({},{fetchPolicy:`network-only`})})},t[1]=o,t[2]=s);let c=s,l;t[3]!==a.viewer||t[4]!==c?(l={viewer:a.viewer,refetchViewer:c},t[3]=a.viewer,t[4]=c,t[5]=l):l=t[5];let u;return t[6]!==r||t[7]!==l?(u=G(xi.Provider,{value:l,children:r}),t[6]=r,t[7]=l,t[8]=u):u=t[8],u}var Mi={OPENAI:`OpenAI`,AZURE_OPENAI:`Azure OpenAI`,ANTHROPIC:`Anthropic`,GOOGLE:`Google`,DEEPSEEK:`DeepSeek`,XAI:`xAI`,OLLAMA:`Ollama`,AWS:`AWS Bedrock`,CEREBRAS:`Cerebras`,FIREWORKS:`Fireworks`,GROQ:`Groq`,MOONSHOT:`Moonshot`,PERPLEXITY:`Perplexity`,TOGETHER:`Together`},Ni=`OPENAI`,Pi=`gpt-5.6-luna`,Fi=`user`,Ii=`RESPONSES`,Li={user:[`user`,`human`],ai:[`assistant`,`bot`,`ai`,`model`],system:[`system`,`developer`],tool:[`tool`]},Ri={OPENAI:[{envVarName:`OPENAI_API_KEY`,isRequired:!0}],AZURE_OPENAI:[{envVarName:`AZURE_OPENAI_API_KEY`,isRequired:!0}],ANTHROPIC:[{envVarName:`ANTHROPIC_API_KEY`,isRequired:!0}],GOOGLE:[{envVarName:`GEMINI_API_KEY`,isRequired:!0}],DEEPSEEK:[{envVarName:`DEEPSEEK_API_KEY`,isRequired:!0}],XAI:[{envVarName:`XAI_API_KEY`,isRequired:!0}],OLLAMA:[],CEREBRAS:[{envVarName:`CEREBRAS_API_KEY`,isRequired:!0}],FIREWORKS:[{envVarName:`FIREWORKS_API_KEY`,isRequired:!0}],GROQ:[{envVarName:`GROQ_API_KEY`,isRequired:!0}],MOONSHOT:[{envVarName:`MOONSHOT_API_KEY`,isRequired:!0}],PERPLEXITY:[{envVarName:`PERPLEXITY_API_KEY`,isRequired:!0}],TOGETHER:[{envVarName:`TOGETHER_API_KEY`,isRequired:!0}],AWS:[{envVarName:`AWS_ACCESS_KEY_ID`,isRequired:!0},{envVarName:`AWS_SECRET_ACCESS_KEY`,isRequired:!0},{envVarName:`AWS_SESSION_TOKEN`,isRequired:!1}]},zi=`api_key`,Bi=`default_credentials`,Vi={OPENAI:`OPENAI`,AZURE_OPENAI:`AZURE_OPENAI`,ANTHROPIC:`ANTHROPIC`,AWS_BEDROCK:`AWS`,GOOGLE_GENAI:`GOOGLE`},Hi={openai:`OPENAI`,azure:`AZURE_OPENAI`,anthropic:`ANTHROPIC`,aws:`AWS`,google:`GOOGLE`,xai:`XAI`,ollama:`OLLAMA`,deepseek:`DEEPSEEK`,cerebras:`CEREBRAS`,fireworks:`FIREWORKS`,groq:`GROQ`,moonshot:`MOONSHOT`,perplexity:`PERPLEXITY`,together:`TOGETHER`},Ui=Object.entries({OPENAI:`OpenAI`,AZURE_OPENAI:`Azure OpenAI`,ANTHROPIC:`Anthropic`,AWS_BEDROCK:`AWS Bedrock`,GOOGLE_GENAI:`Google GenAI`}).map(([e,t])=>({id:e,label:t})),Wi={OPENAI:`openai`,AZURE_OPENAI:`azure`,ANTHROPIC:`anthropic`,AWS_BEDROCK:`aws`,GOOGLE_GENAI:`google`},Gi=Object.entries({api_key:`API Key`,ad_token_provider:`Azure AD Token Provider`,default_credentials:`Default Credentials (Managed Identity)`}).map(([e,t])=>({id:e,label:t})),Ki=Object.entries({default_credentials:`Default Credentials (IAM Role)`,access_keys:`Access Keys`}).map(([e,t])=>({id:e,label:t}));function qi(e){let t=(0,Z.c)(4),n;t[0]===Symbol.for(`react.memo_cache_sentinel`)?(n=q`
        display: inline-block;
        max-width: 100%;
        min-width: 0;
        color: var(--global-link-color);
      `,t[0]=n):n=t[0];let r;t[1]===Symbol.for(`react.memo_cache_sentinel`)?(r=q`
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
        `,t[1]=r):r=t[1];let i;return t[2]===e?i=t[3]:(i=G(`div`,{className:`link-container`,onClick:Ji,css:n,children:G(ln,{css:r,...e})}),t[2]=e,t[3]=i),i}function Ji(e){return e.stopPropagation()}function Yi(e){let t=(0,Z.c)(5),{href:n,children:r}=e,i;t[0]===Symbol.for(`react.memo_cache_sentinel`)?(i=q`
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
      `,t[0]=i):i=t[0];let a;t[1]===Symbol.for(`react.memo_cache_sentinel`)?(a=G(U,{svg:G(tt,{})}),t[1]=a):a=t[1];let o;return t[2]!==r||t[3]!==n?(o=H(`a`,{href:n,target:`_blank`,css:i,rel:`noreferrer`,children:[r,a]}),t[2]=r,t[3]=n,t[4]=o):o=t[4],o}var Xi=Gt`
  100% {
    transform: rotate(360deg);
  }
`,Zi=Gt`
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
`,Qi=q`
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
`,$i=q`
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
`;function ea(e){let t=(0,Z.c)(13),n,r;t[0]===e?(n=t[1],r=t[2]):({ref:r,...n}=e,t[0]=e,t[1]=n,t[2]=r);let{isIndeterminate:i,value:a,size:o}=n,s=i!==void 0&&i,c=o===void 0?`M`:o,l=s||void 0,u;t[3]!==s||t[4]!==a?(u=!s&&a!=null?{"--progress-circle-value":a}:void 0,t[3]=s,t[4]=a,t[5]=u):u=t[5];let d;t[6]===Symbol.for(`react.memo_cache_sentinel`)?(d=H(`svg`,{className:`progress-circle__svg`,children:[G(`circle`,{className:`progress-circle__background`}),G(`circle`,{className:`progress-circle__arc`})]}),t[6]=d):d=t[6];let f;return t[7]!==n||t[8]!==r||t[9]!==c||t[10]!==l||t[11]!==u?(f=G(xt,{...n,"data-size":c,"data-indeterminate":l,css:Qi,ref:r,style:u,children:d}),t[7]=n,t[8]=r,t[9]=c,t[10]=l,t[11]=u,t[12]=f):f=t[12],f}function ta(e){let t=(0,Z.c)(12),n,r,i,a;t[0]===e?(n=t[1],r=t[2],i=t[3],a=t[4]):({ref:i,width:a,height:n,...r}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a);let o;t[5]!==n||t[6]!==a?(o={width:a,height:n},t[5]=n,t[6]=a,t[7]=o):o=t[7];let s;return t[8]!==r||t[9]!==i||t[10]!==o?(s=G(xt,{...r,ref:i,css:$i,style:o,children:na}),t[8]=r,t[9]=i,t[10]=o,t[11]=s):s=t[11],s}function na(e){let{percentage:t}=e;return G(`div`,{className:`progress-bar__track`,children:G(`div`,{className:`progress-bar__fill`,style:{width:t+`%`}})})}function ra(e){let t=(0,Z.c)(7),{ref:n,...r}=e,{children:i,elementType:a,...o}=r,s=a===void 0?`div`:a,{styleProps:c}=Mn(r,Tn),l=Vn(o),u;t[0]===Symbol.for(`react.memo_cache_sentinel`)?(u=q`
        overflow: hidden;
        box-sizing: border-box;
      `,t[0]=u):u=t[0];let d;return t[1]!==s||t[2]!==i||t[3]!==n||t[4]!==c||t[5]!==l?(d=G(s,{...l,...c,ref:n,css:u,className:`view`,children:i}),t[1]=s,t[2]=i,t[3]=n,t[4]=c,t[5]=l,t[6]=d):d=t[6],d}var ia=q`
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
`,aa=q`
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
`;function oa(e){let t=(0,Z.c)(10),n,r,i,a;if(t[0]!==e){let{ref:o,...s}=e,{css:c,...l}=s;n=_e,r=l,i=o,a=q(ia,c),t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a}else n=t[1],r=t[2],i=t[3],a=t[4];let o;return t[5]!==n||t[6]!==r||t[7]!==i||t[8]!==a?(o=G(n,{...r,ref:i,css:a}),t[5]=n,t[6]=r,t[7]=i,t[8]=a,t[9]=o):o=t[9],o}function sa(e){let t=(0,Z.c)(8),n,r;t[0]===e?(n=t[1],r=t[2]):({ref:r,...n}=e,t[0]=e,t[1]=n,t[2]=r);let{css:i}=n,a;t[3]===Symbol.for(`react.memo_cache_sentinel`)?(a=B(`react-aria-OverlayArrow`),t[3]=a):a=t[3];let o;t[4]===Symbol.for(`react.memo_cache_sentinel`)?(o=G(`svg`,{width:8,height:8,viewBox:`0 0 8 8`,children:G(`path`,{d:`M0 0 L4 4 L8 0`})}),t[4]=o):o=t[4];let s;return t[5]!==i||t[6]!==r?(s=G(xn,{ref:r,css:i,className:a,children:o}),t[5]=i,t[6]=r,t[7]=s):s=t[7],s}var ca=1e3,la=60*ca,ua=60*la,da=24*ua;7*da;var fa=30*da,pa=31536e3,ma=2592e3,ha=604800,ga=86400,_a=3600,va=`https://arize.com/docs/phoenix`,ya={accessControl:`${va}/settings/access-control-rbac`,annotationConfigs:`${va}/tracing/how-to-tracing/feedback-and-annotations/annotating-in-the-ui`,apiKeys:`${va}/settings/api-keys`,customAiProviders:`${va}/settings/custom-ai-providers`,dataRetention:`${va}/settings/data-retention`,datasetLabels:`${va}/release-notes/10-2025/10-08-2025-dataset-labels`,modelCostTracking:`${va}/tracing/how-to-tracing/cost-tracking`,remoteMcpServer:`${va}/integrations/remote-mcp`,promptLabels:`${va}/release-notes/09-2025/09-15-2025-prompt-labels`,providers:`${va}/prompt-engineering/how-to-prompts/configure-ai-providers`,pxi:`${va}/pxi`,sandboxes:`${va}/settings/sandboxes`,secrets:`${va}/settings/secrets`},ba={aiProviderSettings:{href:ya.providers,label:`AI provider settings`},aiProviders:{href:ya.providers,label:`AI providers`},annotationConfigs:{href:ya.annotationConfigs,label:`annotation configs`},apiKeys:{href:ya.apiKeys,label:`API keys`},customAiProviders:{href:ya.customAiProviders,label:`custom AI providers`},dataRetention:{href:ya.dataRetention,label:`data retention`},datasetLabels:{href:ya.datasetLabels,label:`dataset labels`},defaultRetentionPolicy:{href:ya.dataRetention,label:`the default retention policy`},modelPricing:{href:ya.modelCostTracking,label:`model pricing`},promptLabels:{href:ya.promptLabels,label:`prompt labels`},pxi:{href:ya.pxi,label:`PXI`},sandboxConfigurations:{href:ya.sandboxes,label:`sandbox configurations`},sandboxProviders:{href:ya.sandboxes,label:`sandbox providers`},secrets:{href:ya.secrets,label:`secrets`},userAccess:{href:ya.accessControl,label:`user access`}},xa=e=>{switch(e){case`info`:return G(en,{});default:return G(ct,{})}},Sa=q`
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
`,Ca=e=>{let t=(0,Z.c)(22),n,r,i,a,o;t[0]===e?(n=t[1],r=t[2],i=t[3],a=t[4],o=t[5]):({children:n,href:r,triggerAriaLabel:i,variant:a,...o}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a,t[5]=o);let s=i===void 0?`More information`:i,c=a===void 0?`help`:a,l;t[6]===c?l=t[7]:(l=xa(c),t[6]=c,t[7]=l);let u;t[8]===l?u=t[9]:(u=G(U,{svg:l}),t[8]=l,t[9]=u);let d;t[10]!==u||t[11]!==s?(d={"aria-label":s,css:Sa,leadingVisual:u,size:`S`,variant:`quiet`},t[10]=u,t[11]=s,t[12]=d):d=t[12];let f=d,p;t[13]!==r||t[14]!==f?(p=r?G(ce,{children:G(Ot,{...f,href:r})}):G(Nt,{...f}),t[13]=r,t[14]=f,t[15]=p):p=t[15];let m;t[16]!==n||t[17]!==o?(m=G(oa,{...o,children:n}),t[16]=n,t[17]=o,t[18]=m):m=t[18];let h;return t[19]!==p||t[20]!==m?(h=H(Te,{delay:0,children:[p,m]}),t[19]=p,t[20]=m,t[21]=h):h=t[21],h},wa=q`
  margin-top: var(--global-dimension-size-100);
`;function Ta(e){let t=(0,Z.c)(9),{children:n,topic:r}=e,{href:i,label:a}=ba[r],o=`Learn more about ${a}`,s;t[0]===n?s=t[1]:(s=G(V,{size:`S`,children:n}),t[0]=n,t[1]=s);let c;t[2]===i?c=t[3]:(c=G(`footer`,{css:wa,children:G(Yi,{href:i,children:`View documentation`})}),t[2]=i,t[3]=c);let l;return t[4]!==i||t[5]!==o||t[6]!==s||t[7]!==c?(l=H(Ca,{href:i,variant:`info`,triggerAriaLabel:o,children:[s,c]}),t[4]=i,t[5]=o,t[6]=s,t[7]=c,t[8]=l):l=t[8],l}function Ea(e){let t=(0,Z.c)(8),n,r;t[0]===e?(n=t[1],r=t[2]):({children:n,...r}=e,t[0]=e,t[1]=n,t[2]=r);let i;t[3]===n?i=t[4]:(i=G(`div`,{role:`button`,children:n}),t[3]=n,t[4]=i);let a;return t[5]!==r||t[6]!==i?(a=G(ce,{...r,children:i}),t[5]=r,t[6]=i,t[7]=a):a=t[7],a}function Da(e){let t=(0,Z.c)(16),n,r,i,a,o,s;if(t[0]!==e){let{ref:c,...l}=e,{children:u,css:d,width:f,...p}=l;r=u,s=f,n=_e,i=p,a=c,o=q(aa,d),t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a,t[5]=o,t[6]=s}else n=t[1],r=t[2],i=t[3],a=t[4],o=t[5],s=t[6];let c;t[7]===s?c=t[8]:(c=s?{width:s}:{maxWidth:`300px`},t[7]=s,t[8]=c);let l;return t[9]!==n||t[10]!==r||t[11]!==i||t[12]!==a||t[13]!==o||t[14]!==c?(l=G(n,{...i,ref:a,css:o,style:c,children:r}),t[9]=n,t[10]=r,t[11]=i,t[12]=a,t[13]=o,t[14]=c,t[15]=l):l=t[15],l}function Oa(e){let t=(0,Z.c)(3),{children:n}=e,r;t[0]===Symbol.for(`react.memo_cache_sentinel`)?(r=q`
        margin-bottom: var(--global-dimension-size-100);
      `,t[0]=r):r=t[0];let i;return t[1]===n?i=t[2]:(i=G(at,{level:4,css:r,children:n}),t[1]=n,t[2]=i),i}function ka(e){let t=(0,Z.c)(3),{children:n}=e,r;t[0]===Symbol.for(`react.memo_cache_sentinel`)?(r=q`
        margin-bottom: var(--global-dimension-size-100);
      `,t[0]=r):r=t[0];let i;return t[1]===n?i=t[2]:(i=G(V,{size:`S`,color:`text-700`,css:r,children:n}),t[1]=n,t[2]=i),i}function Aa(e){let t=(0,Z.c)(2),{children:n}=e,r;return t[0]===n?r=t[1]:(r=G(ra,{paddingTop:`size-50`,children:n}),t[0]=n,t[1]=r),r}var ja=2e3,Ma=q`
  flex: none;
  box-sizing: content-box;
`;function Na(e){let t=(0,Z.c)(20),n,r,i,a;t[0]===e?(n=t[1],r=t[2],i=t[3],a=t[4]):({text:a,size:r,tooltipText:i,...n}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a);let o=r===void 0?`S`:r,s=i===void 0?`Copy`:i,[c,l]=(0,X.useState)(!1),u;t[5]===a?u=t[6]:(u=()=>{let e=typeof a==`string`?a:a.current||``;S(e),l(!0),setTimeout(()=>{l(!1)},ja)},t[5]=a,t[6]=u);let d=u,f=c?`success`:`inherit`,p=c?`Checkmark`:`Duplicate`,m;t[7]!==f||t[8]!==p?(m=G(U,{color:f,svgKey:p}),t[7]=f,t[8]=p,t[9]=m):m=t[9];let h;t[10]!==d||t[11]!==n||t[12]!==o||t[13]!==m?(h=G(Nt,{size:o,leadingVisual:m,onPress:d,...n,className:`copy-button`}),t[10]=d,t[11]=n,t[12]=o,t[13]=m,t[14]=h):h=t[14];let g;t[15]===s?g=t[16]:(g=G(oa,{offset:1,children:s}),t[15]=s,t[16]=g);let _;return t[17]!==h||t[18]!==g?(_=G(`div`,{className:`copy-to-clipboard-button`,css:Ma,children:H(Te,{children:[h,g]})}),t[17]=h,t[18]=g,t[19]=_):_=t[19],_}var Pa=q`
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
`,Fa=Tt,Ia=e=>{let t=(0,Z.c)(10),n,r,i;t[0]===e?(n=t[1],r=t[2],i=t[3]):({className:n,onKeyDown:r,...i}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i);let a;t[4]===n?a=t[5]:(a=B(`react-aria-Menu`,n),t[4]=n,t[5]=a);let o;return t[6]!==r||t[7]!==i||t[8]!==a?(o=G(Qt,{className:a,css:Pa,...i,onKeyDown:r}),t[6]=r,t[7]=i,t[8]=a,t[9]=o):o=t[9],o},La=q`
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
`,Ra=e=>{let t=(0,Z.c)(18),n,r,i,a,o;t[0]===e?(n=t[1],r=t[2],i=t[3],a=t[4],o=t[5]):({className:n,trailingContent:o,leadingContent:r,ref:a,...i}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a,t[5]=o);let s=i.textValue||(typeof i.children==`string`?i.children:void 0),c;t[6]===n?c=t[7]:(c=B(`react-aria-MenuItem`,n),t[6]=n,t[7]=c);let l;t[8]!==r||t[9]!==i||t[10]!==o?(l=e=>{let{hasSubmenu:t,isSelected:n,selectionMode:a}=e;return H(W,{children:[n&&G(U,{svg:G(En,{})}),a!==`none`&&!n&&G(U,{svg:G(En,{}),css:q`
                  visibility: hidden;
                `}),G(za,{trailingContent:o,leadingContent:r,children:typeof i.children==`function`?i.children(e):i.children}),t&&G(U,{svg:G(Xn,{})})]})},t[8]=r,t[9]=i,t[10]=o,t[11]=l):l=t[11];let u;return t[12]!==i||t[13]!==a||t[14]!==c||t[15]!==l||t[16]!==s?(u=G(Pn,{ref:a,...i,css:La,className:c,textValue:s,children:l}),t[12]=i,t[13]=a,t[14]=c,t[15]=l,t[16]=s,t[17]=u):u=t[17],u},za=e=>{let t=(0,Z.c)(7),{children:n,trailingContent:r,leadingContent:i}=e,a;t[0]===Symbol.for(`react.memo_cache_sentinel`)?(a=q`
        padding: var(--global-menu-item-gap);
      `,t[0]=a):a=t[0];let o;t[1]!==n||t[2]!==i?(o=i?H(K,{alignItems:`center`,gap:`var(--global-menu-item-content-gap)`,children:[i,` `,n]}):n,t[1]=n,t[2]=i,t[3]=o):o=t[3];let s;return t[4]!==o||t[5]!==r?(s=H(K,{direction:`row`,alignItems:`center`,justifyContent:`space-between`,gap:`var(--global-menu-split-item-content-gap)`,minWidth:0,flex:1,css:a,children:[o,r]}),t[4]=o,t[5]=r,t[6]=s):s=t[6],s},Ba=q`
  overflow-y: hidden;
  display: flex;
  flex-direction: column;
`,Va=e=>{let t=(0,Z.c)(19),n,r,i,a,o,s;t[0]===e?(n=t[1],r=t[2],i=t[3],a=t[4],o=t[5],s=t[6]):({children:n,placement:i,minHeight:a,maxHeight:o,maxWidth:s,...r}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a,t[5]=o,t[6]=s);let c=i===void 0?`bottom end`:i,l=a===void 0?`var(--global-menu-min-height)`:a,u=o===void 0?`var(--global-menu-max-height-large)`:o,d=s===void 0?450:s,f;t[7]!==u||t[8]!==d||t[9]!==l?(f={minHeight:l,maxHeight:u,maxWidth:d},t[7]=u,t[8]=d,t[9]=l,t[10]=f):f=t[10];let p;t[11]===Symbol.for(`react.memo_cache_sentinel`)?(p=q`
          display: flex;
          flex-direction: column;
          height: 100%;
          min-width: 300px;
        `,t[11]=p):p=t[11];let m;t[12]!==n||t[13]!==f?(m=G(`div`,{style:f,css:p,children:n}),t[12]=n,t[13]=f,t[14]=m):m=t[14];let h;return t[15]!==c||t[16]!==r||t[17]!==m?(h=G(qn,{shouldFlip:!1,placement:c,css:Ba,...r,children:m}),t[15]=c,t[16]=r,t[17]=m,t[18]=h):h=t[18],h},Ha=q`
  padding: var(--global-dimension-size-50) var(--global-dimension-size-100) 0;
`,Ua=e=>{let t=(0,Z.c)(5),{title:n,trailingContent:r}=e,i;t[0]===n?i=t[1]:(i=G(V,{weight:`heavy`,children:n}),t[0]=n,t[1]=i);let a;return t[2]!==i||t[3]!==r?(a=G(Qe,{css:Ha,children:H(K,{justifyContent:`space-between`,alignItems:`center`,children:[i,r]})}),t[2]=i,t[3]=r,t[4]=a):a=t[4],a},Wa=e=>{let t=(0,Z.c)(3),{children:n}=e,r;t[0]===Symbol.for(`react.memo_cache_sentinel`)?(r=q`
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
      `,t[0]=r):r=t[0];let i;return t[1]===n?i=t[2]:(i=G(`div`,{className:`menu-header`,css:r,children:n}),t[1]=n,t[2]=i),i},Ga=e=>{let t=(0,Z.c)(8),{children:n,leadingContent:r,trailingContent:i}=e,a;t[0]===Symbol.for(`react.memo_cache_sentinel`)?(a=q`
        padding: var(--global-dimension-size-100);
        border-bottom: 1px solid var(--global-menu-border-color);
      `,t[0]=a):a=t[0];let o;t[1]===Symbol.for(`react.memo_cache_sentinel`)?(o=q`
          flex: 1 1 auto;
          width: 100%;
          padding-left: var(--global-dimension-size-50);
        `,t[1]=o):o=t[1];let s;t[2]===n?s=t[3]:(s=G(at,{level:4,weight:`heavy`,css:o,children:n}),t[2]=n,t[3]=s);let c;return t[4]!==r||t[5]!==s||t[6]!==i?(c=H(K,{direction:`row`,gap:`size-50`,alignItems:`center`,wrap:`nowrap`,minHeight:30,"data-testid":`menu-header-title`,css:a,children:[r,s,i]}),t[4]=r,t[5]=s,t[6]=i,t[7]=c):c=t[7],c},Ka=e=>{let t=(0,Z.c)(3),{children:n}=e,r;t[0]===Symbol.for(`react.memo_cache_sentinel`)?(r=q`
        padding: var(--global-dimension-size-100);
        border-top: 1px solid var(--global-menu-border-color);
        display: flex;
        flex-direction: column;
        flex-shrink: 0;
        gap: var(--global-dimension-size-50);
      `,t[0]=r):r=t[0];let i;return t[1]===n?i=t[2]:(i=G(`div`,{css:r,children:n}),t[1]=n,t[2]=i),i},qa=e=>{let t=(0,Z.c)(3),{children:n}=e,r;t[0]===Symbol.for(`react.memo_cache_sentinel`)?(r=q`
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
      `,t[0]=r):r=t[0];let i;return t[1]===n?i=t[2]:(i=G(V,{color:`gray-400`,fontStyle:`italic`,css:r,children:n}),t[1]=n,t[2]=i),i},Ja=q`
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
`;function Ya(e){let t=(0,Z.c)(10),n,r,i;t[0]===e?(n=t[1],r=t[2],i=t[3]):({ref:i,css:n,...r}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i);let a;t[4]===n?a=t[5]:(a=q(Ja,n),t[4]=n,t[5]=a);let o;return t[6]!==r||t[7]!==i||t[8]!==a?(o=G(Nt,{ref:i,css:a,...r}),t[6]=r,t[7]=i,t[8]=a,t[9]=o):o=t[9],o}function Xa(e){let t=(0,Z.c)(5),{children:n,isPlaceholder:r}=e,i=r&&`menu-button__value--placeholder`,a;t[0]===i?a=t[1]:(a=B(`menu-button__value`,i),t[0]=i,t[1]=a);let o;return t[2]!==n||t[3]!==a?(o=G(`span`,{className:a,children:n}),t[2]=n,t[3]=a,t[4]=o):o=t[4],o}var Za=2e3;function Qa(e){let t=(0,Z.c)(18),{items:n}=e,[r,i]=(0,X.useState)(null),a=(0,X.useRef)(null),o;t[0]===n?o=t[1]:(o=e=>{let t=n.find(t=>t.name===e);t&&(S(t.value),i(t.name),a.current&&clearTimeout(a.current),a.current=setTimeout(()=>{i(null)},Za))},t[0]=n,t[1]=o);let s=o,c=r==null?`Duplicate`:`Checkmark`,l=r==null?`inherit`:`success`,u;t[2]!==c||t[3]!==l?(u=G(U,{svgKey:c,color:l}),t[2]=c,t[3]=l,t[4]=u):u=t[4];let d=r!=null||void 0,f=r==null?void 0:`Copied`,p;t[5]!==u||t[6]!==d||t[7]!==f?(p=G(Nt,{size:`S`,variant:`quiet`,"aria-label":`Copy`,leadingVisual:u,className:`copy-action-menu__button`,"data-copied":d,children:f}),t[5]=u,t[6]=d,t[7]=f,t[8]=p):p=t[8];let m;t[9]===Symbol.for(`react.memo_cache_sentinel`)?(m=q`
            --menu-min-width: auto;
          `,t[9]=m):m=t[9];let h;t[10]===n?h=t[11]:(h=n.map($a),t[10]=n,t[11]=h);let g;t[12]!==s||t[13]!==h?(g=G(qn,{placement:`bottom end`,offset:3,children:G(Ia,{onAction:s,css:m,children:h})}),t[12]=s,t[13]=h,t[14]=g):g=t[14];let _;return t[15]!==p||t[16]!==g?(_=H(Fa,{children:[p,g]}),t[15]=p,t[16]=g,t[17]=_):_=t[17],_}function $a(e){return G(Ra,{id:e.name,textValue:`Copy ${e.name}`,leadingContent:G(U,{svgKey:e.iconKey??`Duplicate`}),children:e.name},e.name)}var eo=q`
  --embedded-copy-button-size: calc(
    var(--global-input-height-m) - 2 * var(--global-dimension-size-125) +
      var(--global-dimension-size-50)
  );
`,to=q`
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
`,no=e=>{let t=(0,Z.c)(6),{children:n,bordered:r}=e,i=r===void 0||r,a;t[0]===Symbol.for(`react.memo_cache_sentinel`)?(a=q`
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
      `,t[0]=a):a=t[0];let o;t[1]===n?o=t[2]:(o=G(at,{children:n}),t[1]=n,t[2]=o);let s;return t[3]!==i||t[4]!==o?(s=G(`div`,{"data-bordered":i,css:a,children:o}),t[3]=i,t[4]=o,t[5]=s):s=t[5],s},ro=[/Unexpected token ['"]?<['"]?/i,/JSON\.parse.*unexpected character/i,/<!DOCTYPE/i,/timeout/i,/502|504|gateway/i];function io(e){if(e==null)return!1;let t=e instanceof Error?e.message:e;return typeof t!=`string`||t.length===0?!1:ro.some(e=>e.test(t))}function ao(e){let t=(0,Z.c)(9),{error:n}=e;if(io(n)){let e;return t[0]===n?e=t[1]:(e=G(oo,{error:n}),t[0]=n,t[1]=e),e}let r,i;t[2]===Symbol.for(`react.memo_cache_sentinel`)?(r=G(K,{direction:`column`,width:`100%`,alignItems:`center`,children:G(`h1`,{children:`Something went wrong`})}),i=G(`p`,{children:`We strive to do our very best but 🐛 bugs happen. It would mean a lot to us if you could file a an issue. If you feel comfortable, please include the error details below in your issue. We will get back to you as soon as we can.`}),t[2]=r,t[3]=i):(r=t[2],i=t[3]);let a;t[4]===Symbol.for(`react.memo_cache_sentinel`)?(a=G(K,{direction:`row`,width:`100%`,justifyContent:`end`,children:G(Yi,{href:`https://github.com/Arize-ai/phoenix/issues/new?assignees=&labels=bug&template=bug_report.md&title=%5BBUG%5D`,children:`file an issue with us`})}),t[4]=a):a=t[4];let o,s;t[5]===Symbol.for(`react.memo_cache_sentinel`)?(o=G(`summary`,{children:`error details`}),s=q`
              white-space: pre-wrap;
              overflow-wrap: break-word;
              overflow: hidden;
              overflow-y: auto;
              max-height: 500px;
            `,t[5]=o,t[6]=s):(o=t[5],s=t[6]);let c;return t[7]===n?c=t[8]:(c=G(ra,{padding:`size-200`,children:H(K,{direction:`column`,children:[r,i,a,H(`details`,{open:!0,children:[o,G(`pre`,{css:s,children:n})]})]})}),t[7]=n,t[8]=c),c}function oo(e){let t=(0,Z.c)(9),{error:n}=e,r,i,a,o;t[0]===Symbol.for(`react.memo_cache_sentinel`)?(r=G(K,{direction:`column`,width:`100%`,alignItems:`center`,children:G(`h1`,{children:`Connection timed out`})}),i=G(`p`,{children:`The connection to the Phoenix server timed out before a response was received. This typically happens when a load balancer or proxy closes the connection before the server can respond.`}),a=G(`p`,{children:`Possible solutions:`}),o=H(`ul`,{css:q`
            margin: var(--global-dimension-size-100) 0;
            padding-left: var(--global-dimension-size-300);
          `,children:[G(`li`,{children:`Increase your load balancer or proxy timeout settings`}),G(`li`,{children:`Check if the Phoenix server is overloaded or slow to respond`}),G(`li`,{children:`Verify network connectivity between components`})]}),t[0]=r,t[1]=i,t[2]=a,t[3]=o):(r=t[0],i=t[1],a=t[2],o=t[3]);let s;t[4]===Symbol.for(`react.memo_cache_sentinel`)?(s=G(K,{direction:`row`,width:`100%`,justifyContent:`end`,children:G(Nt,{variant:`primary`,size:`S`,onPress:so,children:`Retry`})}),t[4]=s):s=t[4];let c;t[5]===n?c=t[6]:(c=n&&H(`details`,{children:[G(`summary`,{children:`error details`}),G(`pre`,{css:q`
                white-space: pre-wrap;
                overflow-wrap: break-word;
                overflow: hidden;
                overflow-y: auto;
                max-height: 500px;
              `,children:n})]}),t[5]=n,t[6]=c);let l;return t[7]===c?l=t[8]:(l=G(ra,{padding:`size-200`,children:H(K,{direction:`column`,children:[r,i,a,o,s,c]})}),t[7]=c,t[8]=l),l}function so(){window.location.reload()}var co=class extends X.Component{constructor(e){super(e),this.state={hasError:!1,error:null}}static getDerivedStateFromError(e){return{hasError:!0,error:e}}componentDidCatch(e,t){console.error(`ErrorBoundary caught error:`,e,t)}render(){if(this.state.hasError){let e=this.state.error instanceof Error?this.state.error.message:null;return typeof this.props.fallback==`function`?G(this.props.fallback,{error:e}):G(ao,{error:e})}return this.props.children}};function lo({error:e}){let t=H(`div`,{css:q`
        text-align: center;
        display: inline-flex;
        align-items: center;
        color: var(--global-text-color-300);
        gap: var(--global-dimension-size-50);
        cursor: ${e?`help`:`default`};
      `,children:[G(U,{svg:G(wt,{})}),G(V,{color:`text-300`,children:`error`})]});return e?H(Te,{delay:200,children:[G(`span`,{tabIndex:0,children:t}),G(_e,{offset:6,children:G(ra,{padding:`size-100`,borderColor:`default`,borderWidth:`thin`,borderRadius:`small`,backgroundColor:`gray-200`,maxWidth:`size-4600`,children:G(`pre`,{css:q`
              white-space: pre-wrap;
              overflow-wrap: break-word;
              margin: 0;
              font-size: var(--global-font-size-xs, 12px);
            `,children:e})})})]}):t}var uo=q`
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
`,fo=q`
  background-color: transparent;
  color: var(--ac-global-text-color-500);
  padding: 0 var(--global-dimension-size-75);
  font-size: var(--global-dimension-font-size-50);
  border-radius: var(--global-rounding-small);
  border: 1px solid var(--ac-global-border-color-default);
  text-transform: uppercase;
`;function po(e){let t=(0,Z.c)(10),n,r,i,a;t[0]===e?(n=t[1],r=t[2],i=t[3],a=t[4]):({ref:i,children:n,variant:a,...r}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a);let o=(a===void 0?`default`:a)===`quiet`?fo:uo,s;return t[5]!==n||t[6]!==r||t[7]!==i||t[8]!==o?(s=G(zt,{ref:i,css:o,...r,children:n}),t[5]=n,t[6]=r,t[7]=i,t[8]=o,t[9]=s):s=t[9],s}function mo({ref:e,color:t,size:n=`M`,shape:r=`square`}){let i=typeof t==`string`&&t.startsWith(`var`),a=i?q`
        background-color: ${t} !important;
      `:void 0;return G(D,{color:i?void 0:t,"data-shape":r,"data-size":n,ref:e,css:q(q`
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
        `,a)})}mo.displayName=`ColorSwatch`;var ho=q`
  opacity: 0.8;
  color: var(--global-text-color-500);
  .theme--dark & {
    color: var(--global-text-color-400);
  }
  .text {
    color: inherit;
  }
`,go=q`
  margin: var(--global-dimension-size-300);
  display: flex;
  flex-direction: column;
  align-items: center;
`;function _o(e){let t=(0,Z.c)(7),{message:n,size:r}=e,i=r===void 0?`M`:r,a,o;t[0]===Symbol.for(`react.memo_cache_sentinel`)?(a=q`
        width: 100%;
        display: flex;
        justify-content: center;
      `,o=[go,ho],t[0]=a,t[1]=o):(a=t[0],o=t[1]);let s;t[2]!==n||t[3]!==i?(s=n&&G(V,{size:i,children:n}),t[2]=n,t[3]=i,t[4]=s):s=t[4];let c;return t[5]===s?c=t[6]:(c=G(`div`,{css:a,children:G(`div`,{css:o,children:s})}),t[5]=s,t[6]=c),c}var vo=q`
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
`;function yo(){let e=(0,Z.c)(2),t=(0,X.useContext)(kt),n=(0,X.useContext)(C),r=t?.inputValue??n?.inputValue??``,i;return e[0]===r?i=e[1]:(i=r.trim(),e[0]=r,e[1]=i),i.length>0}function bo(e){let t=(0,Z.c)(9),{icon:n,description:r,isFiltered:i}=e,a=yo(),o=i??a,s;t[0]===Symbol.for(`react.memo_cache_sentinel`)?(s=[vo,ho],t[0]=s):s=t[0];let c;t[1]!==n||t[2]!==o?(c=o?G(U,{svg:G(Ht,{})}):n,t[1]=n,t[2]=o,t[3]=c):c=t[3];let l=o?`No results`:r,u;t[4]===l?u=t[5]:(u=G(V,{size:`S`,children:l}),t[4]=l,t[5]=u);let d;return t[6]!==c||t[7]!==u?(d=H(`div`,{css:s,children:[c,u]}),t[6]=c,t[7]=u,t[8]=d):d=t[8],d}var xo=q`
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
`,So=q`
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
`;function Co(e){let t=(0,Z.c)(14),{icon:n,title:r,description:i,href:a,external:o}=e,s;t[0]===o?s=t[1]:(s=o?{target:`_blank`,rel:`noopener noreferrer`}:void 0,t[0]=o,t[1]=s);let c;t[2]===r?c=t[3]:(c=G(V,{weight:`heavy`,children:r}),t[2]=r,t[3]=c);let l;t[4]!==n||t[5]!==c?(l=H(K,{direction:`row`,gap:`size-100`,alignItems:`center`,children:[n,c]}),t[4]=n,t[5]=c,t[6]=l):l=t[6];let u;t[7]===i?u=t[8]:(u=G(V,{size:`S`,color:`text-700`,css:So,children:i}),t[7]=i,t[8]=u);let d;return t[9]!==a||t[10]!==s||t[11]!==l||t[12]!==u?(d=H(`a`,{href:a,css:xo,...s,children:[l,u]}),t[9]=a,t[10]=s,t[11]=l,t[12]=u,t[13]=d):d=t[13],d}function wo(e,t,n){return n==null?!1:e===`horizontal`||e!==`vertical`&&t?.type===`cards`&&(t.columns??1)===2&&t.items.length>=3}var To=q`
  max-width: var(--global-dimension-size-4000);
  text-align: center;
  text-wrap: balance;
`,Eo=q`
  display: grid;
  gap: var(--global-dimension-size-200);
  width: min(100%, var(--global-dimension-size-4000));
`,Do=q`
  width: min(100%, calc(var(--global-dimension-size-4000) * 2));
  grid-template-columns: repeat(
    auto-fit,
    minmax(min(100%, var(--global-dimension-size-4000)), 1fr)
  );
`;function Oo(e){let t=(0,Z.c)(14),{action:n}=e;if(n.type===`strip`){let e;t[0]===n.items?e=t[1]:(e=n.items.map(Ao),t[0]=n.items,t[1]=e);let r;return t[2]===e?r=t[3]:(r=G(K,{direction:`row`,gap:`size-100`,wrap:!0,alignItems:`center`,children:e}),t[2]=e,t[3]=r),r}let r=n.columns??1,i=r===2&&Do,a;t[4]===r?a=t[5]:(a=r===1&&q`
            grid-template-columns: 1fr;
          `,t[4]=r,t[5]=a);let o;t[6]!==i||t[7]!==a?(o=[Eo,i,a],t[6]=i,t[7]=a,t[8]=o):o=t[8];let s;t[9]===n.items?s=t[10]:(s=n.items.map(ko),t[9]=n.items,t[10]=s);let c;return t[11]!==o||t[12]!==s?(c=G(`div`,{css:o,children:s}),t[11]=o,t[12]=s,t[13]=c):c=t[13],c}function ko(e,t){return G(Co,{...e},t)}function Ao(e,t){if(e.kind===`link`)return G(Ot,{href:e.href,variant:`quiet`,size:`S`,children:e.label},t);if(e.kind===`node`)return G(X.Fragment,{children:e.node},t);let{kind:n,...r}=e;return G(Nt,{size:`S`,...r},t)}function jo(e){let t=(0,Z.c)(23),{graphic:n,title:r,description:i,action:a,orientation:o}=e,s=wo(o===void 0?`auto`:o,a,n),c=a?.type===`cards`?`size-300`:`size-200`,l=a?.type===`cards`?`size-500`:`size-200`,u;t[0]!==i||t[1]!==r?(u=r!=null||i!=null?H(K,{direction:`column`,gap:`size-25`,alignItems:`center`,children:[r!=null&&G(V,{size:`L`,weight:`heavy`,children:r}),i!=null&&G(V,{size:`S`,color:`text-700`,css:To,children:i})]}):null,t[0]=i,t[1]=r,t[2]=u):u=t[2];let d=u;if(s){let e;t[3]===n?e=t[4]:(e=G(K,{alignItems:`center`,justifyContent:`center`,children:n}),t[3]=n,t[4]=e);let r;t[5]!==e||t[6]!==d?(r=H(K,{direction:`row`,wrap:!0,gap:`size-400`,alignItems:`center`,justifyContent:`center`,children:[e,d]}),t[5]=e,t[6]=d,t[7]=r):r=t[7];let i;t[8]===a?i=t[9]:(i=a!=null&&G(Oo,{action:a}),t[8]=a,t[9]=i);let o;return t[10]!==l||t[11]!==r||t[12]!==i?(o=H(K,{direction:`column`,gap:l,alignItems:`center`,children:[r,i]}),t[10]=l,t[11]=r,t[12]=i,t[13]=o):o=t[13],o}let f=n!=null&&n,p;t[14]===a?p=t[15]:(p=a!=null&&G(Oo,{action:a}),t[14]=a,t[15]=p);let m;t[16]!==c||t[17]!==p||t[18]!==d?(m=H(K,{direction:`column`,gap:c,alignItems:`center`,children:[d,p]}),t[16]=c,t[17]=p,t[18]=d,t[19]=m):m=t[19];let h;return t[20]!==f||t[21]!==m?(h=H(K,{direction:`column`,gap:`size-300`,alignItems:`center`,justifyContent:`center`,children:[f,m]}),t[20]=f,t[21]=m,t[22]=h):h=t[22],h}var Mo=q`
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
`,No=q`
  flex: 0 1 var(--global-dimension-size-2000);
  min-height: var(--global-dimension-size-750);
`;function Po(e){let t=(0,Z.c)(3),{children:n}=e,r;t[0]===Symbol.for(`react.memo_cache_sentinel`)?(r=G(`div`,{css:No,"aria-hidden":`true`}),t[0]=r):r=t[0];let i;return t[1]===n?i=t[2]:(i=H(`div`,{css:Mo,children:[r,n]}),t[1]=n,t[2]=i),i}var Fo={size:`small`,icon:G(U,{svg:G(At,{})})},Io={genericAdd:{size:`small`,icon:G(U,{svg:G(_n,{})})},genericEdit:{size:`small`,icon:G(U,{svg:G(vt,{})})},trace:{size:`large`,icon:G(U,{svg:G(Sn,{})})},dataset:{size:`large`,icon:G(U,{svg:G(vn,{})})},evaluator:{size:`large`,icon:G(U,{svg:G(mt,{})})},session:{size:`large`,icon:G(U,{svg:G(nn,{})})},experiment:{size:`large`,icon:G(U,{svg:G(Qn,{})})},prompt:{size:`large`,icon:G(U,{svg:G(rn,{})})},project:{size:`large`,icon:G(U,{svg:G(Et,{})})},annotation:{size:`small`,icon:G(U,{svg:G(tn,{})})},customAIProvider:{size:`small`,icon:G(U,{svg:G(Pt,{})})},event:{size:`small`,icon:G(U,{svg:G(dt,{})})},attribute:{size:`small`,icon:G(U,{svg:G(en,{})})},config:{size:`small`,icon:G(U,{svg:G(ut,{})})},credential:{size:`small`,icon:G(U,{svg:G(Ln,{})})},version:{size:`small`,icon:G(U,{svg:G(Ct,{})})},tag:Fo,label:Fo,split:Fo};Object.keys(Io),Object.fromEntries(Object.entries(Io).map(([e,t])=>[e,t.size]));var Lo=q`
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
  )`;return q`
    -webkit-mask-image: ${n};
    mask-image: ${n};
  `},zo=q`
  display: block;
  margin-bottom: calc(-1 * var(--global-dimension-size-200));
`,Bo=e=>q`
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
`;function Vo(e){let t=(0,Z.c)(14),{id:n,x:r,y:i,width:a,height:o}=e,s,c,l,u,d,f,p,m;t[0]===Symbol.for(`react.memo_cache_sentinel`)?(s=G(`feFlood`,{floodOpacity:`0`,result:`BackgroundImageFix`}),c=G(`feColorMatrix`,{in:`SourceAlpha`,type:`matrix`,values:`0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 127 0`,result:`hardAlpha`}),l=G(`feOffset`,{dy:`4`}),u=G(`feGaussianBlur`,{stdDeviation:`6`}),d=G(`feComposite`,{in2:`hardAlpha`,operator:`out`}),f=G(`feColorMatrix`,{type:`matrix`,values:`0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0.19 0`}),p=G(`feBlend`,{mode:`normal`,in2:`BackgroundImageFix`,result:`effect1_dropShadow`}),m=G(`feBlend`,{mode:`normal`,in:`SourceGraphic`,in2:`effect1_dropShadow`,result:`shape`}),t[0]=s,t[1]=c,t[2]=l,t[3]=u,t[4]=d,t[5]=f,t[6]=p,t[7]=m):(s=t[0],c=t[1],l=t[2],u=t[3],d=t[4],f=t[5],p=t[6],m=t[7]);let h;return t[8]!==o||t[9]!==n||t[10]!==a||t[11]!==r||t[12]!==i?(h=H(`filter`,{id:n,x:r,y:i,width:a,height:o,filterUnits:`userSpaceOnUse`,colorInterpolationFilters:`sRGB`,children:[s,c,l,u,d,f,p,m]}),t[8]=o,t[9]=n,t[10]=a,t[11]=r,t[12]=i,t[13]=h):h=t[13],h}function Ho(e){let t=(0,Z.c)(10),{x:n,y:r,size:i,icon:a}=e,o;t[0]===i?o=t[1]:(o=Bo(i),t[0]=i,t[1]=o);let s;t[2]!==a||t[3]!==o?(s=G(`div`,{css:o,children:a}),t[2]=a,t[3]=o,t[4]=s):s=t[4];let c;return t[5]!==i||t[6]!==s||t[7]!==n||t[8]!==r?(c=G(`foreignObject`,{x:n,y:r,width:i,height:i,children:s}),t[5]=i,t[6]=s,t[7]=n,t[8]=r,t[9]=c):c=t[9],c}function Uo(e){let t=(0,Z.c)(35),{icon:n,ids:r}=e,i;t[0]===Symbol.for(`react.memo_cache_sentinel`)?(i=[Lo,Ro(`34%`,`34%`),zo],t[0]=i):i=t[0];let a=`url(#${r.f0})`,o,s,c;t[1]===Symbol.for(`react.memo_cache_sentinel`)?(o=G(`rect`,{x:`19`,y:`10`,width:`160`,height:`32`,rx:`8`,fill:`var(--esg-card-bg)`,shapeRendering:`crispEdges`}),s=G(`rect`,{x:`19.5`,y:`10.5`,width:`159`,height:`31`,rx:`7.5`,stroke:`var(--esg-stroke)`,shapeRendering:`crispEdges`}),c=G(`rect`,{opacity:`0.68`,x:`31`,y:`22`,width:`136`,height:`8`,rx:`3`,fill:`var(--esg-bar)`}),t[1]=o,t[2]=s,t[3]=c):(o=t[1],s=t[2],c=t[3]);let l;t[4]===a?l=t[5]:(l=H(`g`,{filter:a,children:[o,s,c]}),t[4]=a,t[5]=l);let u=`url(#${r.f1})`,d,f;t[6]===Symbol.for(`react.memo_cache_sentinel`)?(d=G(`rect`,{x:`12`,y:`52`,width:`174`,height:`48`,rx:`8`,fill:`var(--esg-card-bg)`,shapeRendering:`crispEdges`}),f=G(`rect`,{x:`12.5`,y:`52.5`,width:`173`,height:`47`,rx:`7.5`,stroke:`var(--esg-stroke-subtle)`,shapeRendering:`crispEdges`}),t[6]=d,t[7]=f):(d=t[6],f=t[7]);let p;t[8]===n?p=t[9]:(p=G(Ho,{x:24,y:66,size:20,icon:n}),t[8]=n,t[9]=p);let m,h;t[10]===Symbol.for(`react.memo_cache_sentinel`)?(m=G(`rect`,{opacity:`0.68`,x:`56`,y:`65`,width:`120`,height:`8`,rx:`3`,fill:`var(--esg-bar)`}),h=G(`rect`,{opacity:`0.68`,x:`56`,y:`79`,width:`80`,height:`8`,rx:`3`,fill:`var(--esg-bar)`}),t[10]=m,t[11]=h):(m=t[10],h=t[11]);let g;t[12]!==p||t[13]!==u?(g=H(`g`,{filter:u,children:[d,f,p,m,h]}),t[12]=p,t[13]=u,t[14]=g):g=t[14];let _=`url(#${r.f2})`,v,y,b;t[15]===Symbol.for(`react.memo_cache_sentinel`)?(v=G(`rect`,{x:`19`,y:`110`,width:`160`,height:`32`,rx:`8`,fill:`var(--esg-card-bg)`,shapeRendering:`crispEdges`}),y=G(`rect`,{x:`19.5`,y:`110.5`,width:`159`,height:`31`,rx:`7.5`,stroke:`var(--esg-stroke)`,shapeRendering:`crispEdges`}),b=G(`rect`,{opacity:`0.68`,x:`31`,y:`122`,width:`136`,height:`8`,rx:`3`,fill:`var(--esg-bar)`}),t[15]=v,t[16]=y,t[17]=b):(v=t[15],y=t[16],b=t[17]);let x;t[18]===_?x=t[19]:(x=H(`g`,{filter:_,children:[v,y,b]}),t[18]=_,t[19]=x);let S;t[20]===r.f0?S=t[21]:(S=G(Vo,{id:r.f0,x:7,y:2,width:184,height:56}),t[20]=r.f0,t[21]=S);let C;t[22]===r.f1?C=t[23]:(C=G(Vo,{id:r.f1,x:0,y:44,width:198,height:72}),t[22]=r.f1,t[23]=C);let w;t[24]===r.f2?w=t[25]:(w=G(Vo,{id:r.f2,x:7,y:102,width:184,height:56}),t[24]=r.f2,t[25]=w);let T;t[26]!==S||t[27]!==C||t[28]!==w?(T=H(`defs`,{children:[S,C,w]}),t[26]=S,t[27]=C,t[28]=w,t[29]=T):T=t[29];let E;return t[30]!==g||t[31]!==x||t[32]!==T||t[33]!==l?(E=H(`svg`,{width:`198`,height:`158`,viewBox:`0 0 198 158`,fill:`none`,xmlns:`http://www.w3.org/2000/svg`,"aria-hidden":`true`,focusable:`false`,css:i,children:[l,g,x,T]}),t[30]=g,t[31]=x,t[32]=T,t[33]=l,t[34]=E):E=t[34],E}function Wo(e){let t=(0,Z.c)(40),{icon:n,ids:r}=e,i;t[0]===Symbol.for(`react.memo_cache_sentinel`)?(i=[Lo,Ro(`38%`,`31%`),zo],t[0]=i):i=t[0];let a=`url(#${r.f0})`,o,s,c,l,u,d;t[1]===Symbol.for(`react.memo_cache_sentinel`)?(o=G(`rect`,{x:`12`,y:`8`,width:`174`,height:`32`,rx:`8`,fill:`var(--esg-card-bg)`,shapeRendering:`crispEdges`}),s=G(`rect`,{x:`12.5`,y:`8.5`,width:`173`,height:`31`,rx:`7.5`,stroke:`var(--esg-stroke)`,shapeRendering:`crispEdges`}),c=G(`path`,{d:`M27.75 22.5C28.5784 22.5 29.25 23.1716 29.25 24C29.25 24.8284 28.5784 25.5 27.75 25.5C26.9216 25.5 26.25 24.8284 26.25 24C26.25 23.1716 26.9216 22.5 27.75 22.5Z`,fill:`var(--esg-dots)`}),l=G(`path`,{d:`M33 22.5C33.8284 22.5 34.5 23.1716 34.5 24C34.5 24.8284 33.8284 25.5 33 25.5C32.1716 25.5 31.5 24.8284 31.5 24C31.5 23.1716 32.1716 22.5 33 22.5Z`,fill:`var(--esg-dots)`}),u=G(`path`,{d:`M38.25 22.5C39.0784 22.5 39.75 23.1716 39.75 24C39.75 24.8284 39.0784 25.5 38.25 25.5C37.4216 25.5 36.75 24.8284 36.75 24C36.75 23.1716 37.4216 22.5 38.25 22.5Z`,fill:`var(--esg-dots)`}),d=G(`rect`,{opacity:`0.68`,x:`54`,y:`20`,width:`120`,height:`8`,rx:`3`,fill:`var(--esg-bar)`}),t[1]=o,t[2]=s,t[3]=c,t[4]=l,t[5]=u,t[6]=d):(o=t[1],s=t[2],c=t[3],l=t[4],u=t[5],d=t[6]);let f;t[7]===a?f=t[8]:(f=H(`g`,{filter:a,children:[o,s,c,l,u,d]}),t[7]=a,t[8]=f);let p=`url(#${r.f1})`,m,h;t[9]===Symbol.for(`react.memo_cache_sentinel`)?(m=G(`rect`,{x:`12`,y:`50`,width:`174`,height:`32`,rx:`8`,fill:`var(--esg-card-bg)`,shapeRendering:`crispEdges`}),h=G(`rect`,{x:`12.5`,y:`50.5`,width:`173`,height:`31`,rx:`7.5`,stroke:`var(--esg-stroke-subtle)`,shapeRendering:`crispEdges`}),t[9]=m,t[10]=h):(m=t[9],h=t[10]);let g;t[11]===n?g=t[12]:(g=G(Ho,{x:25,y:58,size:16,icon:n}),t[11]=n,t[12]=g);let _;t[13]===Symbol.for(`react.memo_cache_sentinel`)?(_=G(`rect`,{opacity:`0.68`,x:`54`,y:`62`,width:`120`,height:`8`,rx:`3`,fill:`var(--esg-bar)`}),t[13]=_):_=t[13];let v;t[14]!==p||t[15]!==g?(v=H(`g`,{filter:p,children:[m,h,g,_]}),t[14]=p,t[15]=g,t[16]=v):v=t[16];let y=`url(#${r.f2})`,b,x,S,C,w,T;t[17]===Symbol.for(`react.memo_cache_sentinel`)?(b=G(`rect`,{x:`12`,y:`92`,width:`174`,height:`32`,rx:`8`,fill:`var(--esg-card-bg)`,shapeRendering:`crispEdges`}),x=G(`rect`,{x:`12.5`,y:`92.5`,width:`173`,height:`31`,rx:`7.5`,stroke:`var(--esg-stroke)`,shapeRendering:`crispEdges`}),S=G(`path`,{d:`M27.75 106.5C28.5784 106.5 29.25 107.172 29.25 108C29.25 108.828 28.5784 109.5 27.75 109.5C26.9216 109.5 26.25 108.828 26.25 108C26.25 107.172 26.9216 106.5 27.75 106.5Z`,fill:`var(--esg-dots)`}),C=G(`path`,{d:`M33 106.5C33.8284 106.5 34.5 107.172 34.5 108C34.5 108.828 33.8284 109.5 33 109.5C32.1716 109.5 31.5 108.828 31.5 108C31.5 107.172 32.1716 106.5 33 106.5Z`,fill:`var(--esg-dots)`}),w=G(`path`,{d:`M38.25 106.5C39.0784 106.5 39.75 107.172 39.75 108C39.75 108.828 39.0784 109.5 38.25 109.5C37.4216 109.5 36.75 108.828 36.75 108C36.75 107.172 37.4216 106.5 38.25 106.5Z`,fill:`var(--esg-dots)`}),T=G(`rect`,{opacity:`0.68`,x:`54`,y:`104`,width:`120`,height:`8`,rx:`3`,fill:`var(--esg-bar)`}),t[17]=b,t[18]=x,t[19]=S,t[20]=C,t[21]=w,t[22]=T):(b=t[17],x=t[18],S=t[19],C=t[20],w=t[21],T=t[22]);let E;t[23]===y?E=t[24]:(E=H(`g`,{filter:y,children:[b,x,S,C,w,T]}),t[23]=y,t[24]=E);let D;t[25]===r.f0?D=t[26]:(D=G(Vo,{id:r.f0,x:0,y:0,width:198,height:56}),t[25]=r.f0,t[26]=D);let O;t[27]===r.f1?O=t[28]:(O=G(Vo,{id:r.f1,x:0,y:42,width:198,height:56}),t[27]=r.f1,t[28]=O);let k;t[29]===r.f2?k=t[30]:(k=G(Vo,{id:r.f2,x:0,y:84,width:198,height:56}),t[29]=r.f2,t[30]=k);let A;t[31]!==D||t[32]!==O||t[33]!==k?(A=H(`defs`,{children:[D,O,k]}),t[31]=D,t[32]=O,t[33]=k,t[34]=A):A=t[34];let j;return t[35]!==v||t[36]!==E||t[37]!==A||t[38]!==f?(j=H(`svg`,{width:`198`,height:`140`,viewBox:`0 0 198 140`,fill:`none`,xmlns:`http://www.w3.org/2000/svg`,"aria-hidden":`true`,focusable:`false`,css:i,children:[f,v,E,A]}),t[35]=v,t[36]=E,t[37]=A,t[38]=f,t[39]=j):j=t[39],j}function Go(e){let t=(0,Z.c)(8),{variant:n}=e,{size:r,icon:i}=Io[n===void 0?`genericAdd`:n],a=(0,X.useId)(),o=`${a}-f0`,s=`${a}-f1`,c=`${a}-f2`,l;t[0]!==o||t[1]!==s||t[2]!==c?(l={f0:o,f1:s,f2:c},t[0]=o,t[1]=s,t[2]=c,t[3]=l):l=t[3];let u=l,d;return t[4]!==i||t[5]!==u||t[6]!==r?(d=G(r===`small`?Wo:Uo,{icon:i,ids:u}),t[4]=i,t[5]=u,t[6]=r,t[7]=d):d=t[7],d}function Ko(e){let t=(0,Z.c)(2),{children:n}=e;if(typeof n==`string`){let e;return t[0]===n?e=t[1]:(e=G(at,{level:1,children:n}),t[0]=n,t[1]=e),e}return n}function qo(e){let t=(0,Z.c)(2),{children:n}=e;if(!n)return null;if(typeof n==`string`){let e;return t[0]===n?e=t[1]:(e=G(V,{size:`S`,color:`text-700`,children:n}),t[0]=n,t[1]=e),e}return n}function Jo(e){let t=(0,Z.c)(10),{title:n,subTitle:r,extra:i}=e,a;t[0]===n?a=t[1]:(a=G(Ko,{children:n}),t[0]=n,t[1]=a);let o;t[2]===r?o=t[3]:(o=G(qo,{children:r}),t[2]=r,t[3]=o);let s;t[4]!==a||t[5]!==o?(s=H(K,{direction:`column`,gap:`size-50`,minWidth:0,children:[a,o]}),t[4]=a,t[5]=o,t[6]=s):s=t[6];let c;return t[7]!==i||t[8]!==s?(c=G(ra,{padding:`size-200`,flex:`none`,"data-testid":`page-header`,children:H(K,{direction:`row`,justifyContent:`space-between`,alignItems:`center`,"data-testid":`page-header-content`,gap:`size-100`,children:[s,i]})}),t[7]=i,t[8]=s,t[9]=c):c=t[9],c}var Yo=q`
  border-radius: 16px;
  padding: var(--global-dimension-size-50) var(--global-dimension-size-200) !important;
`,Xo=e=>{let t=(0,Z.c)(10),{onLoadMore:n,isLoadingNext:r,buttonProps:i}=e,a;t[0]===n?a=t[1]:(a=()=>{n()},t[0]=n,t[1]=a);let o;t[2]===r?o=t[3]:(o=r?G(U,{svg:G(wn,{})}):void 0,t[2]=r,t[3]=o);let s=r?`Loading...`:`Load More`,c;return t[4]!==i||t[5]!==r||t[6]!==a||t[7]!==o||t[8]!==s?(c=G(Nt,{onPress:a,size:`S`,css:Yo,isDisabled:r,leadingVisual:o,...i,children:s}),t[4]=i,t[5]=r,t[6]=a,t[7]=o,t[8]=s,t[9]=c):c=t[9],c};function Zo(e,{filled:t}={filled:!0}){let n;switch(e){case`warning`:n=G(t?Zt:yt,{});break;case`info`:n=G(t?An:en,{});break;case`danger`:n=G(t?Nn:wt,{});break;case`success`:n=G(t?un:dn,{})}return G(U,{svg:n})}var Qo=q`
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
`,$o=q`
  display: flex;
  flex-direction: row;
  align-items: flex-start;
  flex: 1 1 auto;
`,es=q`
  background-color: transparent;
  color: inherit;
  padding: 0;
  border: none;
  cursor: pointer;
  width: 20px;
  height: 20px;
  margin-left: var(--global-dimension-size-200);
`,ts=e=>{let t=(0,Z.c)(35),n,r,i,a,o,s,c,l,u,d;t[0]===e?(n=t[1],r=t[2],i=t[3],a=t[4],o=t[5],s=t[6],c=t[7],l=t[8],u=t[9],d=t[10]):({variant:d,title:u,icon:i,children:n,showIcon:s,dismissable:c,onDismissClick:a,banner:l,extra:r,...o}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a,t[5]=o,t[6]=s,t[7]=c,t[8]=l,t[9]=u,t[10]=d);let f=s===void 0||s,p=c!==void 0&&c,m=l!==void 0&&l,{theme:h}=Pr();if(!i&&f){let e;t[11]===d?e=t[12]:(e=Zo(d),t[11]=d,t[12]=e),i=e}let g=!!u,_;t[13]===u?_=t[14]:(_=u?G(V,{elementType:`h5`,size:`M`,weight:`heavy`,color:`inherit`,children:u}):null,t[13]=u,t[14]=_);let v;t[15]===n?v=t[16]:(v=G(V,{color:`inherit`,size:`S`,children:n}),t[15]=n,t[16]=v);let y;t[17]!==_||t[18]!==v?(y=H(`div`,{children:[_,v]}),t[17]=_,t[18]=v,t[19]=y):y=t[19];let b;t[20]!==i||t[21]!==y?(b=H(`div`,{css:$o,className:`alert__icon-title-wrap`,children:[i,y]}),t[20]=i,t[21]=y,t[22]=b):b=t[22];let x;t[23]!==p||t[24]!==a?(x=p?G(`button`,{css:es,onClick:a,children:G(U,{svg:G(rt,{})})}):null,t[23]=p,t[24]=a,t[25]=x):x=t[25];let S;return t[26]!==m||t[27]!==r||t[28]!==o||t[29]!==g||t[30]!==b||t[31]!==x||t[32]!==h||t[33]!==d?(S=H(`div`,{...o,css:Qo,"data-variant":d,"data-banner":m,"data-has-title":g,"data-theme":h,children:[b,r,x]}),t[26]=m,t[27]=r,t[28]=o,t[29]=g,t[30]=b,t[31]=x,t[32]=h,t[33]=d,t[34]=S):S=t[34],S},ns=q`
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
`,rs=e=>{let t=(0,Z.c)(17),n,r,i,a,o,s;t[0]===e?(n=t[1],r=t[2],i=t[3],a=t[4],o=t[5],s=t[6]):({children:n,variant:a,size:o,overflowMode:s,css:i,...r}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a,t[5]=o,t[6]=s);let c=a===void 0?`default`:a,l=o===void 0?`S`:o,u=s===void 0?`wrap`:s,{theme:d}=Pr(),f;t[7]===i?f=t[8]:(f=q(ns,i),t[7]=i,t[8]=f);let p;return t[9]!==n||t[10]!==r||t[11]!==u||t[12]!==l||t[13]!==f||t[14]!==d||t[15]!==c?(p=G(`span`,{...r,css:f,"data-variant":c,"data-size":l,"data-overflow-mode":u,"data-theme":d,className:`badge`,children:n}),t[9]=n,t[10]=r,t[11]=u,t[12]=l,t[13]=f,t[14]=d,t[15]=c,t[16]=p):p=t[16],p},is=q`
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
`,as=q`
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
`,os=e=>{let t=(0,Z.c)(14),n,r,i,a;t[0]===e?(n=t[1],r=t[2],i=t[3],a=t[4]):({className:n,css:r,size:a,...i}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a);let o;t[5]===n?o=t[6]:(o=B(`disclosure-group`,n),t[5]=n,t[6]=o);let s;t[7]===r?s=t[8]:(s=q(is,r),t[7]=r,t[8]=s);let c;return t[9]!==i||t[10]!==a||t[11]!==o||t[12]!==s?(c=G(p,{allowsMultipleExpanded:!0,className:o,css:s,"data-size":a,...i}),t[9]=i,t[10]=a,t[11]=o,t[12]=s,t[13]=c):c=t[13],c},ss=e=>{let t=(0,Z.c)(10),n,r,i;t[0]===e?(n=t[1],r=t[2],i=t[3]):({size:i,className:n,...r}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i);let a;t[4]===n?a=t[5]:(a=B(`disclosure`,n),t[4]=n,t[5]=a);let o;return t[6]!==r||t[7]!==i||t[8]!==a?(o=G(d,{className:a,css:as,"data-size":i,defaultExpanded:!0,...r}),t[6]=r,t[7]=i,t[8]=a,t[9]=o):o=t[9],o},cs=e=>{let t=(0,Z.c)(8),n,r;t[0]===e?(n=t[1],r=t[2]):({className:n,...r}=e,t[0]=e,t[1]=n,t[2]=r);let i;t[3]===n?i=t[4]:(i=B(`disclosure__panel`,n),t[3]=n,t[4]=i);let a;return t[5]!==r||t[6]!==i?(a=G(v,{className:i,...r}),t[5]=r,t[6]=i,t[7]=a):a=t[7],a},ls=e=>{let t=(0,Z.c)(15),{children:n,arrowPosition:r,justifyContent:i,alignItems:a,direction:o,width:s}=e,c=a===void 0?`center`:a,l=o===void 0?`row`:o,u;t[0]===s?u=t[1]:(u={width:s},t[0]=s,t[1]=u);let d=l===`row`?`size-100`:`size-50`,f;t[2]!==c||t[3]!==n||t[4]!==l||t[5]!==i||t[6]!==d?(f=G(K,{justifyContent:i,direction:l,alignItems:c,width:`100%`,gap:d,children:n}),t[2]=c,t[3]=n,t[4]=l,t[5]=i,t[6]=d,t[7]=f):f=t[7];let p;t[8]===r?p=t[9]:(p=r===`none`?null:G(U,{svg:G(Xn,{})}),t[8]=r,t[9]=p);let m;return t[10]!==r||t[11]!==u||t[12]!==f||t[13]!==p?(m=G(Wt,{className:`react-aria-Heading disclosure__trigger`,children:H(Jt,{slot:`trigger`,"data-arrow-position":r,style:u,children:[f,p]})}),t[10]=r,t[11]=u,t[12]=f,t[13]=p,t[14]=m):m=t[14],m},us=q`
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
`,ds=q`
  width: var(--trigger-width);
  background-color: var(--field-popover-background-color);
  border-radius: var(--global-rounding-small);
  color: var(--field-text-color);
  box-shadow: 0px 4px 10px var(--field-popover-shadow-color);
  border: 1px solid var(--field-popover-border-color);
  max-height: inherit;
`,fs=q`
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
`,ps=q`
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
`,ms=q(ds,q`
    .react-aria-ListBox {
      display: block;
      width: unset;
      max-height: inherit;
      min-height: unset;
      border: none;
      overflow: auto;
    }
  `),hs=q`
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
`,gs=e=>{e.stopPropagation()};function _s(e){let t=(0,Z.c)(46),n,r,i,a,o,s,c,l,d,f,p,m;t[0]===e?(n=t[1],r=t[2],i=t[3],a=t[4],o=t[5],s=t[6],c=t[7],l=t[8],d=t[9],f=t[10],p=t[11],m=t[12]):({label:o,placeholder:s,description:r,errorMessage:i,children:n,size:f,width:m,stopPropagation:d,renderEmptyState:l,isInvalid:a,menuTrigger:p,...c}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a,t[5]=o,t[6]=s,t[7]=c,t[8]=l,t[9]=d,t[10]=f,t[11]=p,t[12]=m);let h=f===void 0?`M`:f,g=p===void 0?`focus`:p,_;t[13]===Symbol.for(`react.memo_cache_sentinel`)?(_=q(us,ps),t[13]=_):_=t[13];let v=a||!!i,y;t[14]===m?y=t[15]:(y={width:m},t[14]=m,t[15]=y);let b=!!l,x;t[16]===o?x=t[17]:(x=o&&G(On,{children:o}),t[16]=o,t[17]=x);let S=d?gs:void 0,C=d?gs:void 0,w=d?gs:void 0,T;t[18]===s?T=t[19]:(T=G(ge,{placeholder:s}),t[18]=s,t[19]=T);let E;t[20]===Symbol.for(`react.memo_cache_sentinel`)?(E=G(Jt,{children:G(ft,{})}),t[20]=E):E=t[20];let D;t[21]!==w||t[22]!==T||t[23]!==S||t[24]!==C?(D=H(`div`,{className:`combobox__container`,onClick:S,onKeyDown:C,onKeyUp:w,children:[T,E]}),t[21]=w,t[22]=T,t[23]=S,t[24]=C,t[25]=D):D=t[25];let O;t[26]!==r||t[27]!==i?(O=r&&!i?G(Zn,{slot:`description`,children:r}):null,t[26]=r,t[27]=i,t[28]=O):O=t[28];let k;t[29]===i?k=t[30]:(k=G(A,{children:i}),t[29]=i,t[30]=k);let j;t[31]!==n||t[32]!==l?(j=G(Ft,{css:ms,children:G(Se,{renderEmptyState:l,children:n})}),t[31]=n,t[32]=l,t[33]=j):j=t[33];let M;return t[34]!==g||t[35]!==c||t[36]!==h||t[37]!==D||t[38]!==O||t[39]!==k||t[40]!==j||t[41]!==v||t[42]!==y||t[43]!==b||t[44]!==x?(M=H(u,{...c,menuTrigger:g,css:_,"data-size":h,isInvalid:v,style:y,allowsEmptyCollection:b,children:[x,D,O,k,j]}),t[34]=g,t[35]=c,t[36]=h,t[37]=D,t[38]=O,t[39]=k,t[40]=j,t[41]=v,t[42]=y,t[43]=b,t[44]=x,t[45]=M):M=t[45],M}function vs(e){let t=(0,Z.c)(8),n,r;t[0]===e?(n=t[1],r=t[2]):({children:n,...r}=e,t[0]=e,t[1]=n,t[2]=r);let i;t[3]===n?i=t[4]:(i=e=>{let{isSelected:t}=e;return H(W,{children:[n,t&&G(U,{svg:G(En,{}),className:`menu-item__selected-checkmark`})]})},t[3]=n,t[4]=i);let a;return t[5]!==r||t[6]!==i?(a=G(f,{...r,css:hs,children:i}),t[5]=r,t[6]=i,t[7]=a):a=t[7],a}function ys(e){let t=(0,Z.c)(11),n,r;t[0]===e?(n=t[1],r=t[2]):({ref:r,...n}=e,t[0]=e,t[1]=n,t[2]=r);let i,a;t[3]===n?(i=t[4],a=t[5]):({size:a,...i}=n,t[3]=n,t[4]=i,t[5]=a);let o=a===void 0?`M`:a,s;t[6]===Symbol.for(`react.memo_cache_sentinel`)?(s=q(us,fs),t[6]=s):s=t[6];let c;return t[7]!==i||t[8]!==r||t[9]!==o?(c=G(re,{"data-size":o,className:`text-field`,ref:r,...i,css:s}),t[7]=i,t[8]=r,t[9]=o,t[10]=c):c=t[10],c}var bs=()=>{let e=(0,Z.c)(1),t;return e[0]===Symbol.for(`react.memo_cache_sentinel`)?(t=G(U,{className:`search-field__icon`,svg:G(Ht,{})}),e[0]=t):t=e[0],t},xs=q`
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
`;function Ss(e){let t=(0,Z.c)(20),n,r;t[0]===e?(n=t[1],r=t[2]):({ref:r,...n}=e,t[0]=e,t[1]=n,t[2]=r);let i,a,o,s,c;t[3]===n?(i=t[4],a=t[5],o=t[6],s=t[7],c=t[8]):({size:s,variant:c,children:i,isReadOnly:a,...o}=n,t[3]=n,t[4]=i,t[5]=a,t[6]=o,t[7]=s,t[8]=c);let u=s===void 0?`M`:s,d=c===void 0?`default`:c,f;t[9]===Symbol.for(`react.memo_cache_sentinel`)?(f=q(us,fs,xs),t[9]=f):f=t[9];let p;t[10]!==i||t[11]!==a?(p=e=>H(W,{children:[typeof i==`function`?i(e):i,!a&&G(Jt,{slot:`clear`,className:`search-field__clear`,"data-empty":e.isEmpty||void 0,children:G(U,{svg:G(rt,{})})})]}),t[10]=i,t[11]=a,t[12]=p):p=t[12];let m;return t[13]!==a||t[14]!==o||t[15]!==r||t[16]!==u||t[17]!==p||t[18]!==d?(m=G(l,{"data-size":u,"data-variant":d,className:`search-field`,ref:r,isReadOnly:a,...o,css:f,children:p}),t[13]=a,t[14]=o,t[15]=r,t[16]=u,t[17]=p,t[18]=d,t[19]=m):m=t[19],m}var Cs=e(Me());function ws(e){let t=(0,Z.c)(5),{onChange:n,debounceMs:r}=e,i;t[0]===n?i=t[1]:(i=e=>{(0,X.startTransition)(()=>{n(e)})},t[0]=n,t[1]=i);let a;return t[2]!==r||t[3]!==i?(a=(0,Cs.default)(i,r),t[2]=r,t[3]=i,t[4]=a):a=t[4],a}var Ts=q`
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
`;function Es(e){let t=(0,Z.c)(38),n,r,i,a,o,s;t[0]===e?(n=t[1],r=t[2],i=t[3],a=t[4],o=t[5],s=t[6]):({onChange:i,debounceMs:o,placeholder:n,variant:s,onKeyDown:a,...r}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a,t[5]=o,t[6]=s);let c=o===void 0?200:o,l=s===void 0?`default`:s,u=(0,X.useRef)(null),d=(0,X.useRef)(null),f=(0,X.useRef)(null),[p,m]=(0,X.useState)(!1),h;t[7]===r.defaultValue?h=t[8]:(h=()=>!!r.defaultValue,t[7]=r.defaultValue,t[8]=h);let[g,_]=(0,X.useState)(h),v=!g&&!p,y;t[9]!==c||t[10]!==i?(y={onChange:i,debounceMs:c},t[9]=c,t[10]=i,t[11]=y):y=t[11];let b=ws(y),x;t[12]===b?x=t[13]:(x=e=>{_(e!==``),b(e)},t[12]=b,t[13]=x);let S=x,C;t[14]===Symbol.for(`react.memo_cache_sentinel`)?(C=e=>e!=null&&u.current?.contains(e)===!0,t[14]=C):C=t[14];let w=C,T;t[15]===Symbol.for(`react.memo_cache_sentinel`)?(T=e=>m(w(e.target)),t[15]=T):T=t[15];let E=T,D;t[16]===Symbol.for(`react.memo_cache_sentinel`)?(D=e=>{e.relatedTarget==null&&!document.hasFocus()||m(w(e.relatedTarget))},t[16]=D):D=t[16];let O=D,k;t[17]===a?k=t[18]:(k=e=>{e.key===`Escape`&&e.target instanceof HTMLInputElement&&e.target.value===``&&((0,ur.flushSync)(()=>m(!1)),f.current?.focus(),e.preventDefault(),e.stopPropagation()),a?.(e)},t[17]=a,t[18]=k);let A=k,j;t[19]===Symbol.for(`react.memo_cache_sentinel`)?(j=G(bs,{}),t[19]=j):j=t[19];let M;t[20]!==v||t[21]!==n?(M=G(ge,{ref:d,placeholder:n,inert:v}),t[20]=v,t[21]=n,t[22]=M):M=t[22];let N;t[23]!==S||t[24]!==A||t[25]!==r||t[26]!==M?(N=H(Ss,{ref:u,size:`S`,onChange:S,onKeyDown:A,...r,children:[j,M]}),t[23]=S,t[24]=A,t[25]=r,t[26]=M,t[27]=N):N=t[27];let P=r[`aria-label`],F=!v,I;t[28]===Symbol.for(`react.memo_cache_sentinel`)?(I=()=>{(0,ur.flushSync)(()=>m(!0)),d.current?.focus()},t[28]=I):I=t[28];let L;t[29]!==r.isDisabled||t[30]!==P||t[31]!==F?(L=G(Jt,{ref:f,className:`search-button__trigger`,"aria-label":P,"aria-expanded":F,isDisabled:r.isDisabled,onPress:I}),t[29]=r.isDisabled,t[30]=P,t[31]=F,t[32]=L):L=t[32];let R;return t[33]!==v||t[34]!==N||t[35]!==L||t[36]!==l?(R=H(`div`,{className:`search-button`,"data-variant":l,"data-collapsed":v,css:Ts,onFocus:E,onBlur:O,children:[N,L]}),t[33]=v,t[34]=N,t[35]=L,t[36]=l,t[37]=R):R=t[37],R}var Ds=q`
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
`;function Os(e){let t=(0,Z.c)(2),n;return t[0]===e.children?n=t[1]:(n=G(`div`,{className:`composite-field`,css:Ds,children:e.children}),t[0]=e.children,t[1]=n),n}function ks(e){let t=(0,Z.c)(16),n,r;t[0]===e?(n=t[1],r=t[2]):({ref:r,...n}=e,t[0]=e,t[1]=n,t[2]=r);let i,a,o;t[3]===n?(i=t[4],a=t[5],o=t[6]):({size:o,children:i,...a}=n,t[3]=n,t[4]=i,t[5]=a,t[6]=o);let s=o===void 0?`M`:o,c;t[7]===Symbol.for(`react.memo_cache_sentinel`)?(c=q(us,fs),t[7]=c):c=t[7];let l;t[8]!==i||t[9]!==a||t[10]!==r||t[11]!==s?(l=G(re,{"data-size":s,className:`copy-field`,isReadOnly:!0,ref:r,...a,css:c,children:i}),t[8]=i,t[9]=a,t[10]=r,t[11]=s,t[12]=l):l=t[12];let u;return t[13]!==s||t[14]!==l?(u=G(Dt,{size:s,children:l}),t[13]=s,t[14]=l,t[15]=u):u=t[15],u}var As=2e3;function js(e){let t=(0,Z.c)(30),n,r;t[0]===e?(n=t[1],r=t[2]):({ref:r,...n}=e,t[0]=e,t[1]=n,t[2]=r);let i=It(),a,o;t[3]===n?(a=t[4],o=t[5]):({disabled:a,...o}=n,t[3]=n,t[4]=a,t[5]=o);let[s,c]=(0,X.useState)(!1),l=(0,X.useRef)(null),u;t[6]===Symbol.for(`react.memo_cache_sentinel`)?(u=()=>{let e=l.current?.value??``;S(e),c(!0),setTimeout(()=>{c(!1)},As)},t[6]=u):u=t[6];let d=u,f;t[7]===Symbol.for(`react.memo_cache_sentinel`)?(f=q`
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
      `,t[7]=f):f=t[7];let p;t[8]===r?p=t[9]:(p=e=>{l.current=e,typeof r==`function`?r(e):r&&(r.current=e)},t[8]=r,t[9]=p);let m;t[10]!==a||t[11]!==o||t[12]!==p?(m=G(ge,{...o,ref:p,type:`text`,readOnly:!0,disabled:a}),t[10]=a,t[11]=o,t[12]=p,t[13]=m):m=t[13];let h=s?`Copied`:`Copy to clipboard`,g=s?`success`:`inherit`,_=s?`Checkmark`:`Duplicate`,v;t[14]!==g||t[15]!==_?(v=G(U,{color:g,svgKey:_}),t[14]=g,t[15]=_,t[16]=v):v=t[16];let y;t[17]!==a||t[18]!==h||t[19]!==v?(y=G(Jt,{className:`copy-input__copy-button`,onPress:d,isDisabled:a,"aria-label":h,children:v}),t[17]=a,t[18]=h,t[19]=v,t[20]=y):y=t[20];let b=s?`Copied`:`Copy`,x;t[21]===b?x=t[22]:(x=G(oa,{offset:1,children:b}),t[21]=b,t[22]=x);let C;t[23]!==x||t[24]!==y?(C=H(Te,{children:[y,x]}),t[23]=x,t[24]=y,t[25]=C):C=t[25];let w;return t[26]!==i||t[27]!==C||t[28]!==m?(w=H(`div`,{"data-size":i,"data-testid":`copy-input`,css:f,children:[m,C]}),t[26]=i,t[27]=C,t[28]=m,t[29]=w):w=t[29],w}var Ms=(0,X.createContext)(null);function Ns(){let e=(0,X.useContext)(Ms);if(!e)throw Error(`useCredentialContext must be used within a CredentialContext.Provider`);return e}function Ps(e){let t=(0,Z.c)(21),n,r;t[0]===e?(n=t[1],r=t[2]):({ref:r,...n}=e,t[0]=e,t[1]=n,t[2]=r);let i,a,o;t[3]===n?(i=t[4],a=t[5],o=t[6]):({size:o,children:i,...a}=n,t[3]=n,t[4]=i,t[5]=a,t[6]=o);let s=o===void 0?`M`:o,[c,l]=(0,X.useState)(!1),u;t[7]===c?u=t[8]:(u={isVisible:c,setIsVisible:l},t[7]=c,t[8]=u);let d;t[9]===Symbol.for(`react.memo_cache_sentinel`)?(d=q(us,fs),t[9]=d):d=t[9];let f;t[10]!==i||t[11]!==a||t[12]!==r||t[13]!==s?(f=G(re,{"data-size":s,className:`credential-field`,autoComplete:`off`,ref:r,...a,css:d,children:i}),t[10]=i,t[11]=a,t[12]=r,t[13]=s,t[14]=f):f=t[14];let p;t[15]!==s||t[16]!==f?(p=G(Dt,{size:s,children:f}),t[15]=s,t[16]=f,t[17]=p):p=t[17];let m;return t[18]!==u||t[19]!==p?(m=G(Ms.Provider,{value:u,children:p}),t[18]=u,t[19]=p,t[20]=m):m=t[20],m}function Fs(e){let t=(0,Z.c)(28),n,r;t[0]===e?(n=t[1],r=t[2]):({ref:r,...n}=e,t[0]=e,t[1]=n,t[2]=r);let{isVisible:i,setIsVisible:a}=Ns(),o=It(),s,c,l;t[3]===n?(s=t[4],c=t[5],l=t[6]):({disabled:s,readOnly:l,...c}=n,t[3]=n,t[4]=s,t[5]=c,t[6]=l);let u;t[7]===Symbol.for(`react.memo_cache_sentinel`)?(u=q`
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
      `,t[7]=u):u=t[7];let d=i?`text`:`password`,f;t[8]!==s||t[9]!==c||t[10]!==l||t[11]!==r||t[12]!==d?(f=G(ge,{...c,ref:r,type:d,disabled:s,readOnly:l}),t[8]=s,t[9]=c,t[10]=l,t[11]=r,t[12]=d,t[13]=f):f=t[13];let p;t[14]!==i||t[15]!==a?(p=()=>a(!i),t[14]=i,t[15]=a,t[16]=p):p=t[16];let m=s||l,h=i?`Hide credential`:`Show credential`,g;t[17]===i?g=t[18]:(g=G(U,{svg:G(i?Kt:gt,{})}),t[17]=i,t[18]=g);let _;t[19]!==p||t[20]!==m||t[21]!==h||t[22]!==g?(_=G(Jt,{className:`credential-input__toggle`,onPress:p,isDisabled:m,"aria-label":h,children:g}),t[19]=p,t[20]=m,t[21]=h,t[22]=g,t[23]=_):_=t[23];let v;return t[24]!==o||t[25]!==f||t[26]!==_?(v=H(`div`,{"data-size":o,"data-testid":`credential-input`,css:u,children:[f,_]}),t[24]=o,t[25]=f,t[26]=_,t[27]=v):v=t[27],v}var Is=``,Ls=`${Is}REDACTED${Is}`;function Rs(e){return typeof e==`string`&&e.startsWith(Ls)}function zs(e){let t=e.slice(Ls.length),n=t.indexOf(Is);return n<0?null:t.slice(0,n)||null}function Bs(e){if(!Rs(e))return null;let t=zs(e);return t?`••••${t}`:`••••••••`}function Vs(e){let t=(0,Z.c)(29),{label:n,placeholder:r,description:i,value:a,onChange:o,onBlur:s,name:c,isDisabled:l,isRequired:u,errorMessage:d,size:f}=e,p=f===void 0?`M`:f,[m,h]=(0,X.useState)(!1),g;t[0]!==m||t[1]!==a?(g=!m&&Rs(a),t[0]=m,t[1]=a,t[2]=g):g=t[2];let _=g,v=_?``:a??``,y;t[3]!==r||t[4]!==_||t[5]!==a?(y=_?Bs(a)??`••••••••`:r,t[3]=r,t[4]=_,t[5]=a,t[6]=y):y=t[6];let b=y,x;t[7]!==m||t[8]!==o?(x=e=>{m||h(!0),o(e)},t[7]=m,t[8]=o,t[9]=x):x=t[9];let S=x,C=!!d,w;t[10]===n?w=t[11]:(w=G(On,{children:n}),t[10]=n,t[11]=w);let T;t[12]===b?T=t[13]:(T=G(ge,{placeholder:b}),t[12]=b,t[13]=T);let E;t[14]!==i||t[15]!==d?(E=d?G(A,{children:d}):i?G(V,{slot:`description`,children:i}):null,t[14]=i,t[15]=d,t[16]=E):E=t[16];let D;return t[17]!==v||t[18]!==S||t[19]!==l||t[20]!==u||t[21]!==c||t[22]!==s||t[23]!==p||t[24]!==C||t[25]!==w||t[26]!==T||t[27]!==E?(D=H(ys,{type:`password`,size:p,name:c,value:v,onChange:S,onBlur:s,isDisabled:l,isRequired:u,isInvalid:C,autoComplete:`off`,children:[w,T,E]}),t[17]=v,t[18]=S,t[19]=l,t[20]=u,t[21]=c,t[22]=s,t[23]=p,t[24]=C,t[25]=w,t[26]=T,t[27]=E,t[28]=D):D=t[28],D}var Hs=q`
  .react-aria-Input {
    text-align: right;
    font-feature-settings: "tnum" 1;
  }
`;function Us(e){let t=(0,Z.c)(13),n,r,i,a,o;if(t[0]!==e){let{ref:s,...c}=e;r=s;let{size:l,...u}=c,d=l===void 0?`M`:l;n=de,i=d,a=u,o=B(`text-field react-aria-NumberField`,c.className),t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a,t[5]=o}else n=t[1],r=t[2],i=t[3],a=t[4],o=t[5];let s;t[6]===Symbol.for(`react.memo_cache_sentinel`)?(s=q(us,fs,Hs),t[6]=s):s=t[6];let c;return t[7]!==n||t[8]!==r||t[9]!==i||t[10]!==a||t[11]!==o?(c=G(n,{"data-size":i,...a,className:o,ref:r,css:s}),t[7]=n,t[8]=r,t[9]=i,t[10]=a,t[11]=o,t[12]=c):c=t[12],c}function Ws(e){let t=(0,Z.c)(15),n,r,i,a;t[0]===e?(n=t[1],r=t[2],i=t[3],a=t[4]):({onChange:i,debounceMs:a,placeholder:n,...r}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a);let o=a===void 0?200:a,s;t[5]!==o||t[6]!==i?(s={onChange:i,debounceMs:o},t[5]=o,t[6]=i,t[7]=s):s=t[7];let c=ws(s),l;t[8]===Symbol.for(`react.memo_cache_sentinel`)?(l=G(bs,{}),t[8]=l):l=t[8];let u;t[9]===n?u=t[10]:(u=G(ge,{placeholder:n}),t[9]=n,t[10]=u);let d;return t[11]!==c||t[12]!==r||t[13]!==u?(d=H(Ss,{onChange:c,...r,children:[l,u]}),t[11]=c,t[12]=r,t[13]=u,t[14]=d):d=t[14],d}var Gs=()=>{let e=(0,Z.c)(1),t;return e[0]===Symbol.for(`react.memo_cache_sentinel`)?(t=G(U,{color:`danger`,className:`field__icon`,svg:G(Wn,{})}),e[0]=t):t=e[0],t},Ks=()=>{let e=(0,Z.c)(1),t;return e[0]===Symbol.for(`react.memo_cache_sentinel`)?(t=G(U,{color:`success`,className:`field__icon`,svg:G(En,{})}),e[0]=t):t=e[0],t},qs=q`
  /* Pin the palette near the top of the viewport instead of centering it so
     the list can grow and shrink without the dialog jumping around */
  &&[data-variant="default"] .react-aria-Dialog {
    top: 15vh;
    transform: translate(-50%, 0);
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }
`,Js=q`
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
`;function Ys(e){let t=(0,Z.c)(32),{isOpen:n,onOpenChange:r,inputValue:i,onInputChange:a,filter:o,placeholder:s,"aria-label":c,onAction:l,children:u,renderEmptyState:d,footer:f,isPending:p}=e,m=s===void 0?`Search…`:s,h=c===void 0?`Command palette`:c,g=p?`true`:void 0,_;t[0]===Symbol.for(`react.memo_cache_sentinel`)?(_=G(bs,{}),t[0]=_):_=t[0];let v;t[1]===m?v=t[2]:(v=G(ge,{placeholder:m}),t[1]=m,t[2]=v);let y;t[3]!==h||t[4]!==v?(y=G(`div`,{className:`command-palette__field`,children:H(Ss,{"aria-label":h,variant:`quiet`,size:`L`,autoFocus:!0,children:[_,v]})}),t[3]=h,t[4]=v,t[5]=y):y=t[5];let b;t[6]===d?b=t[7]:(b=()=>G(`div`,{className:`command-palette__empty-state`,children:d?d():G(bo,{icon:G(U,{svg:G(Ht,{})}),description:`No results`})}),t[6]=d,t[7]=b);let x;t[8]!==h||t[9]!==u||t[10]!==l||t[11]!==b?(x=G(Ia,{className:`command-palette__menu`,"aria-label":h,onAction:l,renderEmptyState:b,children:u}),t[8]=h,t[9]=u,t[10]=l,t[11]=b,t[12]=x):x=t[12];let S;t[13]===f?S=t[14]:(S=f??G(Xs,{}),t[13]=f,t[14]=S);let C;t[15]===S?C=t[16]:(C=G(`div`,{className:`command-palette__footer`,children:S}),t[15]=S,t[16]=C);let w;t[17]!==o||t[18]!==i||t[19]!==a||t[20]!==C||t[21]!==y||t[22]!==x?(w=H(gn,{inputValue:i,onInputChange:a,filter:o,children:[y,x,C]}),t[17]=o,t[18]=i,t[19]=a,t[20]=C,t[21]=y,t[22]=x,t[23]=w):w=t[23];let T;t[24]!==h||t[25]!==w||t[26]!==g?(T=G(jn,{size:`M`,css:qs,children:G(fn,{"aria-label":h,className:`command-palette`,css:Js,"data-pending":g,children:w})}),t[24]=h,t[25]=w,t[26]=g,t[27]=T):T=t[27];let E;return t[28]!==n||t[29]!==r||t[30]!==T?(E=G(Cn,{isOpen:n,onOpenChange:r,isDismissable:!0,children:T}),t[28]=n,t[29]=r,t[30]=T,t[31]=E):E=t[31],E}function Xs(){let e=(0,Z.c)(3),t;e[0]===Symbol.for(`react.memo_cache_sentinel`)?(t=H(`span`,{className:`command-palette__hint`,children:[G(po,{children:`↑↓`}),G(V,{size:`XS`,color:`text-500`,children:`to navigate`})]}),e[0]=t):t=e[0];let n;e[1]===Symbol.for(`react.memo_cache_sentinel`)?(n=H(`span`,{className:`command-palette__hint`,children:[G(po,{children:`↵`}),G(V,{size:`XS`,color:`text-500`,children:`to select`})]}),e[1]=n):n=e[1];let r;return e[2]===Symbol.for(`react.memo_cache_sentinel`)?(r=H(W,{children:[t,n,H(`span`,{className:`command-palette__hint`,children:[G(po,{children:`esc`}),G(V,{size:`XS`,color:`text-500`,children:`to close`})]})]}),e[2]=r):r=e[2],r}function Zs(e){let t=(0,Z.c)(5),{title:n,children:r}=e,i;t[0]===n?i=t[1]:(i=G(Qe,{className:`command-palette__section-header`,children:n}),t[0]=n,t[1]=i);let a;return t[2]!==r||t[3]!==i?(a=H(St,{className:`command-palette__section`,children:[i,r]}),t[2]=r,t[3]=i,t[4]=a):a=t[4],a}var Qs=q`
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
`;function $s(e){let t=(0,Z.c)(18),n,r,i,a;t[0]===e?(n=t[1],r=t[2],i=t[3],a=t[4]):({icon:i,description:r,children:n,...a}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a);let o;t[5]===i?o=t[6]:(o=i&&G(`span`,{className:`command-palette-item__icon`,children:i}),t[5]=i,t[6]=o);let s;t[7]===n?s=t[8]:(s=G(`span`,{className:`command-palette-item__label`,children:n}),t[7]=n,t[8]=s);let c;t[9]===r?c=t[10]:(c=r&&G(`span`,{className:`command-palette-item__description`,children:r}),t[9]=r,t[10]=c);let l;t[11]!==o||t[12]!==s||t[13]!==c?(l=H(`div`,{className:`command-palette-item__layout`,children:[o,s,c]}),t[11]=o,t[12]=s,t[13]=c,t[14]=l):l=t[14];let u;return t[15]!==a||t[16]!==l?(u=G(Ra,{...a,className:`command-palette-item`,css:Qs,children:l}),t[15]=a,t[16]=l,t[17]=u):u=t[17],u}var ec=q`
  background-color: rgba(var(--global-color-blue-500-rgb), 0.4);
  color: inherit;
  border-radius: var(--global-rounding-xsmall);
`;function tc(e){let t=(0,Z.c)(26),{text:n,match:r}=e,i;t[0]===r?i=t[1]:(i=r?.trim().length??0,t[0]=r,t[1]=i);let a=i;if(!r||a===0){let e;return t[2]===n?e=t[3]:(e=G(W,{children:n}),t[2]=n,t[3]=e),e}let o,s,c,l,u,d;if(t[4]!==r||t[5]!==a||t[6]!==n){d=Symbol.for(`react.early_return_sentinel`);bb0:{let e=n.toLowerCase().indexOf(r.trim().toLowerCase());if(e===-1){let e;t[13]===n?e=t[14]:(e=G(W,{children:n}),t[13]=n,t[14]=e),d=e;break bb0}o=e+a,u=n.slice(0,e),s=`match-text`,c=ec,l=n.slice(e,o)}t[4]=r,t[5]=a,t[6]=n,t[7]=o,t[8]=s,t[9]=c,t[10]=l,t[11]=u,t[12]=d}else o=t[7],s=t[8],c=t[9],l=t[10],u=t[11],d=t[12];if(d!==Symbol.for(`react.early_return_sentinel`))return d;let f;t[15]!==s||t[16]!==c||t[17]!==l?(f=G(`mark`,{className:s,css:c,children:l}),t[15]=s,t[16]=c,t[17]=l,t[18]=f):f=t[18];let p;t[19]!==o||t[20]!==n?(p=n.slice(o),t[19]=o,t[20]=n,t[21]=p):p=t[21];let m;return t[22]!==u||t[23]!==f||t[24]!==p?(m=H(W,{children:[u,f,p]}),t[22]=u,t[23]=f,t[24]=p,t[25]=m):m=t[25],m}q`
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
`,q`
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: var(--global-dimension-size-50);
  height: 28px;
`;var nc=q(`
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
`),rc=e=>{let t=(0,Z.c)(16),n,r,i,a,o;t[0]===e?(n=t[1],r=t[2],i=t[3],a=t[4],o=t[5]):({size:a,css:r,className:n,direction:o,...i}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a,t[5]=o);let c=o===void 0?`row`:o,l;t[6]===n?l=t[7]:(l=B(`radio-group`,n),t[6]=n,t[7]=l);let u;t[8]===r?u=t[9]:(u=q(us,nc,r),t[8]=r,t[9]=u);let d;return t[10]!==c||t[11]!==i||t[12]!==a||t[13]!==l||t[14]!==u?(d=G(s,{"data-size":a,"data-direction":c,className:l,css:u,...i}),t[10]=c,t[11]=i,t[12]=a,t[13]=l,t[14]=u,t[15]=d):d=t[15],d},ic=q(`
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
`),ac=e=>{let t=(0,Z.c)(12),n,r,i;t[0]===e?(n=t[1],r=t[2],i=t[3]):({className:n,css:r,...i}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i);let a;t[4]===n?a=t[5]:(a=B(`radio`,n),t[4]=n,t[5]=a);let o;t[6]===r?o=t[7]:(o=q(ic,r),t[6]=r,t[7]=o);let s;return t[8]!==i||t[9]!==a||t[10]!==o?(s=G(h,{className:a,css:o,...i}),t[8]=i,t[9]=a,t[10]=o,t[11]=s):s=t[11],s},oc=q(st,`
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
`),sc=e=>{let t=(0,Z.c)(25),n,r,i;t[0]===e?(n=t[1],r=t[2],i=t[3]):({className:n,css:r,...i}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i);let a,o,s,c,l;t[4]===i?(a=t[5],o=t[6],s=t[7],c=t[8],l=t[9]):({leadingVisual:o,trailingVisual:l,size:s,children:a,...c}=i,t[4]=i,t[5]=a,t[6]=o,t[7]=s,t[8]=c,t[9]=l);let u=It(),d=s??u,f;t[10]!==a||t[11]!==o||t[12]!==l?(f=e=>H(W,{children:[o,typeof a==`function`?a(e):a,l]}),t[10]=a,t[11]=o,t[12]=l,t[13]=f):f=t[13];let p=f,m;t[14]===r?m=t[15]:(m=q(oc,r),t[14]=r,t[15]=m);let h=!a,g;t[16]===n?g=t[17]:(g=B(`toggle-button`,n),t[16]=n,t[17]=g);let _;return t[18]!==p||t[19]!==c||t[20]!==d||t[21]!==m||t[22]!==h||t[23]!==g?(_=G(fe,{css:m,"data-size":d,"data-childless":h,className:g,...c,children:p}),t[18]=p,t[19]=c,t[20]=d,t[21]=m,t[22]=h,t[23]=g,t[24]=_):_=t[24],_},cc=q(`
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
`),lc=e=>{let t=(0,Z.c)(19),n,r,i,a,o;t[0]===e?(n=t[1],r=t[2],i=t[3],a=t[4],o=t[5]):({size:a,css:r,className:n,selectionMode:o,...i}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a,t[5]=o);let s=a===void 0?`M`:a,c=o===void 0?`single`:o,l;t[6]===n?l=t[7]:(l=B(`toggle-button-group`,n),t[6]=n,t[7]=l);let u;t[8]===r?u=t[9]:(u=q(cc,r),t[8]=r,t[9]=u);let d;t[10]!==i||t[11]!==c||t[12]!==s||t[13]!==l||t[14]!==u?(d=G(ke,{"data-size":s,className:l,css:u,selectionMode:c,...i}),t[10]=i,t[11]=c,t[12]=s,t[13]=l,t[14]=u,t[15]=d):d=t[15];let f;return t[16]!==s||t[17]!==d?(f=G(Dt,{size:s,children:d}),t[16]=s,t[17]=d,t[18]=f):f=t[18],f},uc=q`
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
`,dc=q`
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
`,fc=q`
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
`,pc=q`
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
`;function mc(e){for(let t of X.Children.toArray(e)){if(!(0,X.isValidElement)(t))continue;if(t.type===X.Fragment){let e=mc(t.props.children);if(e!=null)return e;continue}let{id:e,isDisabled:n}=t.props;if(e!=null&&!n)return e}}function hc(e){let t=(0,Z.c)(33),n,r,i,a,o,s,c,l,u;t[0]===e?(n=t[1],r=t[2],i=t[3],a=t[4],o=t[5],s=t[6],c=t[7],l=t[8],u=t[9]):({children:n,size:l,isJustified:u,selectedKey:c,defaultSelectedKey:a,onSelectionChange:o,className:r,css:i,...s}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a,t[5]=o,t[6]=s,t[7]=c,t[8]=l,t[9]=u);let d=l===void 0?`M`:l,f=u!==void 0&&u,p;t[10]!==n||t[11]!==a?(p=()=>a??mc(n),t[10]=n,t[11]=a,t[12]=p):p=t[12];let[m]=(0,X.useState)(p),h;t[13]===c?h=t[14]:(h=c===void 0?void 0:[c],t[13]=c,t[14]=h);let g;t[15]===m?g=t[16]:(g=m==null?void 0:[m],t[15]=m,t[16]=g);let _;t[17]===o?_=t[18]:(_=e=>{let[t]=e;t!=null&&o?.(t)},t[17]=o,t[18]=_);let v;t[19]===r?v=t[20]:(v=B(`segmented-control`,r),t[19]=r,t[20]=v);let y;t[21]===i?y=t[22]:(y=q(uc,i),t[21]=i,t[22]=y);let b;return t[23]!==n||t[24]!==f||t[25]!==s||t[26]!==d||t[27]!==h||t[28]!==g||t[29]!==_||t[30]!==v||t[31]!==y?(b=G(ke,{...s,selectionMode:`single`,disallowEmptySelection:!0,orientation:`horizontal`,selectedKeys:h,defaultSelectedKeys:g,onSelectionChange:_,"data-size":d,"data-justified":f,className:v,css:y,children:n}),t[23]=n,t[24]=f,t[25]=s,t[26]=d,t[27]=h,t[28]=g,t[29]=_,t[30]=v,t[31]=y,t[32]=b):b=t[32],b}function gc(e){let t=(0,Z.c)(4),{isSelected:n}=e,r=(0,X.useRef)(null),i,a;t[0]===n?(i=t[1],a=t[2]):(i=()=>{let e=r.current,t=e?.style.translate;e&&n&&t&&(e.style.translate=`${t.split(` `)[0]} 0px`)},a=[n],t[0]=n,t[1]=i,t[2]=a),(0,X.useLayoutEffect)(i,a);let o;return t[3]===Symbol.for(`react.memo_cache_sentinel`)?(o=G(it,{ref:r,className:`segmented-control__thumb`,css:pc}),t[3]=o):o=t[3],o}function _c(e){let t=(0,Z.c)(16),n,r,i,a;t[0]===e?(n=t[1],r=t[2],i=t[3],a=t[4]):({children:n,className:r,css:i,...a}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a);let o;t[5]===r?o=t[6]:(o=B(`segmented-control__item`,r),t[5]=r,t[6]=o);let s;t[7]===i?s=t[8]:(s=q(dc,i),t[7]=i,t[8]=s);let c;t[9]===n?c=t[10]:(c=e=>{let{isSelected:t}=e;return H(W,{children:[G(`div`,{className:`segmented-control__item-content`,css:fc,children:typeof n==`string`?G(V,{children:n}):n}),G(gc,{isSelected:t})]})},t[9]=n,t[10]=c);let l;return t[11]!==a||t[12]!==o||t[13]!==s||t[14]!==c?(l=G(fe,{...a,className:o,css:s,children:c}),t[11]=a,t[12]=o,t[13]=s,t[14]=c,t[15]=l):l=t[15],l}var vc=q`
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
`;function yc(e){let t=(0,Z.c)(10),n,r,i;t[0]===e?(n=t[1],r=t[2],i=t[3]):({css:n,ref:r,...i}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i);let a;t[4]===n?a=t[5]:(a=q(vc,n),t[4]=n,t[5]=a);let o=a,s;return t[6]!==o||t[7]!==r||t[8]!==i?(s=G(Se,{css:o,ref:r,...i}),t[6]=o,t[7]=r,t[8]=i,t[9]=s):s=t[9],s}var bc=q`
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
`;function xc(e){let t=(0,Z.c)(14),n,r;t[0]===e?(n=t[1],r=t[2]):({ref:r,...n}=e,t[0]=e,t[1]=n,t[2]=r);let i,a,o;t[3]===n?(i=t[4],a=t[5],o=t[6]):({children:i,isHovered:a,...o}=n,t[3]=n,t[4]=i,t[5]=a,t[6]=o);let s=a||void 0,c;t[7]===i?c=t[8]:(c=e=>{let{isIndeterminate:t}=e;return H(W,{children:[G(`div`,{className:`checkbox`,children:G(`svg`,{viewBox:`0 0 18 18`,"aria-hidden":`true`,children:t?G(`rect`,{x:1,y:7.5,width:15,height:3}):G(`polyline`,{points:`1 9 7 14 15 4`})})}),i]})},t[7]=i,t[8]=c);let l;return t[9]!==r||t[10]!==o||t[11]!==s||t[12]!==c?(l=G(we,{...o,ref:r,css:bc,"data-force-hovered":s,children:c}),t[9]=r,t[10]=o,t[11]=s,t[12]=c,t[13]=l):l=t[13],l}var Sc=q`
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
`,Cc=q`
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
`,wc=q`
  padding: var(--global-dimension-size-50) var(--global-dimension-size-100) 0;
`;q`
  display: flex;
  flex-direction: column;
  gap: var(--global-menu-item-gap);
`;function Tc(e){let t=(0,Z.c)(6),n,r;t[0]===e?(n=t[1],r=t[2]):({ref:n,...r}=e,t[0]=e,t[1]=n,t[2]=r);let i;return t[3]!==n||t[4]!==r?(i=G(ue,{css:Sc,ref:n,...r}),t[3]=n,t[4]=r,t[5]=i):i=t[5],i}function Ec(e){let t=(0,Z.c)(14),n,r,i,a,o;t[0]===e?(n=t[1],r=t[2],i=t[3],a=t[4],o=t[5]):({ref:r,children:n,subtitle:a,trailingContent:o,...i}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a,t[5]=o);let s;t[6]!==n||t[7]!==a||t[8]!==o?(s=e=>{let{selectionMode:t,selectionBehavior:r}=e;return H(W,{children:[G(Dc,{subtitle:a,selectionMode:t,selectionBehavior:r,children:n}),o]})},t[6]=n,t[7]=a,t[8]=o,t[9]=s):s=t[9];let c;return t[10]!==r||t[11]!==i||t[12]!==s?(c=G(m,{css:Cc,ref:r,...i,children:s}),t[10]=r,t[11]=i,t[12]=s,t[13]=c):c=t[13],c}var Dc=e=>{let t=(0,Z.c)(14),{children:n,subtitle:r,selectionMode:i,selectionBehavior:a}=e,[o,s]=(0,X.useState)(!1),c,l,u;t[0]===Symbol.for(`react.memo_cache_sentinel`)?(c=()=>s(!0),l=()=>s(!1),u=q`
        flex: 1;
        min-width: 0;
      `,t[0]=c,t[1]=l,t[2]=u):(c=t[0],l=t[1],u=t[2]);let d;t[3]!==o||t[4]!==a||t[5]!==i?(d=i===`multiple`&&a===`toggle`&&G(xc,{slot:`selection`,isHovered:o}),t[3]=o,t[4]=a,t[5]=i,t[6]=d):d=t[6];let f;t[7]===Symbol.for(`react.memo_cache_sentinel`)?(f=q`
            padding: var(--global-menu-item-gap);
          `,t[7]=f):f=t[7];let p;t[8]!==n||t[9]!==r?(p=H(K,{direction:`column`,gap:`var(--global-dimension-size-25)`,minWidth:0,flex:1,css:f,children:[n,r]}),t[8]=n,t[9]=r,t[10]=p):p=t[10];let m;return t[11]!==d||t[12]!==p?(m=G(`div`,{onMouseEnter:c,onMouseLeave:l,css:u,children:H(K,{direction:`row`,alignItems:`center`,gap:`size-100`,className:`GridListItem__content`,children:[d,p]})}),t[11]=d,t[12]=p,t[13]=m):m=t[13],m},Oc=e=>{let t=(0,Z.c)(2),{title:n}=e,i;return t[0]===n?i=t[1]:(i=G(r,{css:wc,children:G(V,{weight:`heavy`,children:n})}),t[0]=n,t[1]=i),i},kc=q`
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
`;function Ac(e){let t=(0,Z.c)(3),{children:n}=e,r;t[0]===Symbol.for(`react.memo_cache_sentinel`)?(r=q`
        display: flex;
        align-items: center;
        justify-content: center;
        width: var(--global-dimension-size-200);
        height: var(--global-dimension-size-200);
        /* The visual keeps its box when the token's text truncates —
           otherwise it compresses and the visual slides into the end cap. */
        flex-shrink: 0;
        margin-right: var(--global-dimension-size-50);
      `,t[0]=r):r=t[0];let i;return t[1]===n?i=t[2]:(i=G(`span`,{css:r,children:n}),t[1]=n,t[2]=i),i}function jc(e){let t=(0,Z.c)(58),n,r,i,a,o,s,c,l,u,d,f,p;t[0]===e?(n=t[1],r=t[2],i=t[3],a=t[4],o=t[5],s=t[6],c=t[7],l=t[8],u=t[9],d=t[10],f=t[11],p=t[12]):({ref:l,children:n,isDisabled:i,css:r,color:f,onPress:s,onRemove:c,size:p,style:d,leadingVisual:a,maxWidth:o,...u}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a,t[5]=o,t[6]=s,t[7]=c,t[8]=l,t[9]=u,t[10]=d,t[11]=f,t[12]=p);let m=f===void 0?`var(--global-color-gray-600)`:f,h=p===void 0?`M`:p,{theme:g}=Pr(),_;t[13]!==a||t[14]!==h?(_=a&&h!==`S`?G(Ac,{children:a}):null,t[13]=a,t[14]=h,t[15]=_):_=t[15];let v=_,y;t[16]!==i||t[17]!==c?(y=c?G(`button`,{onClick:()=>{c()},disabled:i,"aria-label":`Remove`,children:G(U,{svg:G(rt,{})})}):null,t[16]=i,t[17]=c,t[18]=y):y=t[18];let b=y,x;t[19]===n?x=t[20]:(x=G(`span`,{className:`token__text`,children:n}),t[19]=n,t[20]=x);let S=x,C;t[21]!==i||t[22]!==s||t[23]!==c||t[24]!==b||t[25]!==S||t[26]!==v?(C=()=>s&&c?H(W,{children:[H(`button`,{onClick:()=>{s()},disabled:i,children:[v,S]}),b]}):s?H(`button`,{onClick:()=>{s()},disabled:i,children:[v,S]}):c?H(W,{children:[H(`span`,{children:[v,S]}),b]}):H(W,{children:[v,S]}),t[21]=i,t[22]=s,t[23]=c,t[24]=b,t[25]=S,t[26]=v,t[27]=C):C=t[27];let w=C,T;t[28]===r?T=t[29]:(T=q(kc,r),t[28]=r,t[29]=T);let E;t[30]===o?E=t[31]:(E=o&&{"--token-max-width":o},t[30]=o,t[31]=E);let D;t[32]!==m||t[33]!==d||t[34]!==E?(D={"--internal-token-color":m,...E,...d},t[32]=m,t[33]=d,t[34]=E,t[35]=D):D=t[35];let O;t[36]===s?O=t[37]:(O=s&&{"data-interactive":!0},t[36]=s,t[37]=O);let k;t[38]===c?k=t[39]:(k=c&&{"data-removable":!0},t[38]=c,t[39]=k);let A;t[40]===v?A=t[41]:(A=v&&{"data-leading-visual":!0},t[40]=v,t[41]=A);let j;t[42]===i?j=t[43]:(j=i&&{"data-disabled":!0},t[42]=i,t[43]=j);let M;t[44]===w?M=t[45]:(M=w(),t[44]=w,t[45]=M);let N;return t[46]!==l||t[47]!==u||t[48]!==h||t[49]!==O||t[50]!==k||t[51]!==A||t[52]!==j||t[53]!==M||t[54]!==T||t[55]!==D||t[56]!==g?(N=G(`div`,{ref:l,css:T,style:D,"data-theme":g,"data-size":h,...O,...k,...A,...j,...u,children:M}),t[46]=l,t[47]=u,t[48]=h,t[49]=O,t[50]=k,t[51]=A,t[52]=j,t[53]=M,t[54]=T,t[55]=D,t[56]=g,t[57]=N):N=t[57],N}var Mc=q`
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
`;function Nc(e){let n=(0,Z.c)(24),r,i,a,o,s,c;n[0]===e?(r=n[1],i=n[2],a=n[3],o=n[4],s=n[5],c=n[6]):({ref:s,label:a,thumbLabels:c,children:i,css:r,...o}=e,n[0]=e,n[1]=r,n[2]=i,n[3]=a,n[4]=o,n[5]=s,n[6]=c);let l;n[7]===r?l=n[8]:(l=q(Mc,r),n[7]=r,n[8]=l);let u;n[9]===a?u=n[10]:(u=a&&G(On,{className:`slider__label`,children:a}),n[9]=a,n[10]=u);let d;n[11]===i?d=n[12]:(d=i===void 0?G(Ic,{}):i,n[11]=i,n[12]=d);let f;n[13]===d?f=n[14]:(f=G(ee,{className:`slider__output`,children:d}),n[13]=d,n[14]=f);let p;n[15]===c?p=n[16]:(p=G(E,{className:`slider__track`,style:Pc,children:e=>{let{state:t}=e;return G(W,{children:t.values.map((e,t)=>G(_,{index:t,"aria-label":c?.[t],className:`slider__thumb`},t))})}}),n[15]=c,n[16]=p);let m;return n[17]!==o||n[18]!==s||n[19]!==l||n[20]!==u||n[21]!==f||n[22]!==p?(m=H(t,{css:l,...o,ref:s,children:[u,f,p]}),n[17]=o,n[18]=s,n[19]=l,n[20]=u,n[21]=f,n[22]=p,n[23]=m):m=n[23],m}function Pc(e){let{state:t}=e;return t.values.length===1?{"--slider-start":`0%`,"--slider-end":`${t.getThumbPercent(0)*100}%`}:{"--slider-start":`${t.getThumbPercent(0)*100}%`,"--slider-end":`${t.getThumbPercent(1)*100}%`}}function Fc(e){let t=(0,Z.c)(19),n,r;t[0]===e?(n=t[1],r=t[2]):({onChange:n,...r}=e,t[0]=e,t[1]=n,t[2]=r);let{step:i,getThumbMinValue:a,getThumbMaxValue:o,values:s,setThumbValue:c}=(0,X.useContext)(O),l=`defaultValue`in r,u=s[0]===a(0),d=l&&u?r.defaultValue:s[0],f=Un(zn),p=f.id,m;t[3]!==n||t[4]!==c?(m=e=>{n?n(e):typeof e==`number`&&c(0,e)},t[3]=n,t[4]=c,t[5]=m):m=t[5];let h;t[6]===o?h=t[7]:(h=o(0),t[6]=o,t[7]=h);let g;t[8]===a?g=t[9]:(g=a(0),t[8]=a,t[9]=g);let _;t[10]===Symbol.for(`react.memo_cache_sentinel`)?(_=G(ge,{}),t[10]=_):_=t[10];let v;return t[11]!==f.id||t[12]!==r||t[13]!==i||t[14]!==m||t[15]!==h||t[16]!==g||t[17]!==d?(v=G(Us,{className:`slider__number-field`,"aria-labelledby":p,value:d,onChange:m,step:i,maxValue:h,minValue:g,...r,children:_}),t[11]=f.id,t[12]=r,t[13]=i,t[14]=m,t[15]=h,t[16]=g,t[17]=d,t[18]=v):v=t[18],v}function Ic(){let e=(0,Z.c)(4),t=(0,X.useContext)(O),n;e[0]===t.values?n=e[1]:(n=t.values.map(Lc).join(` – `),e[0]=t.values,e[1]=n);let r;return e[2]===n?r=e[3]:(r=G(V,{children:n}),e[2]=n,e[3]=r),r}function Lc(e){return e.toString()}var Rc=q`
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
`;function zc(e){let t=(0,Z.c)(4),{children:n,variant:r}=e,i=r===void 0?`default`:r,{theme:a}=Pr(),o;return t[0]!==n||t[1]!==a||t[2]!==i?(o=G(`span`,{css:Rc,"data-variant":i,"data-theme":a,className:`counter`,children:n}),t[0]=n,t[1]=a,t[2]=i,t[3]=o):o=t[3],o}function Bc(){let e=(0,Z.c)(6),t=(0,X.useRef)(null),[n,r]=(0,X.useState)(!1),[i,a]=(0,X.useState)(!1),o;e[0]===Symbol.for(`react.memo_cache_sentinel`)?(o=()=>{let e=t.current;if(!e)return;if(e.getAttribute(`data-orientation`)!==`horizontal`){r(!1),a(!1);return}let{scrollLeft:n,scrollWidth:i,clientWidth:o}=e,s=i-o;r(n>1),a(n<s-1)},e[0]=o):o=e[0];let s=o;pt(t,`scroll`,s);let c;e[1]===Symbol.for(`react.memo_cache_sentinel`)?(c={ref:t,onResize:s},e[1]=c):c=e[1],kn(c);let l;e[2]===Symbol.for(`react.memo_cache_sentinel`)?(l=()=>{s()},e[2]=l):l=e[2],(0,X.useEffect)(l);let u;return e[3]!==i||e[4]!==n?(u={ref:t,hasOverflowAtStart:n,hasOverflowAtEnd:i},e[3]=i,e[4]=n,e[5]=u):u=e[5],u}var Vc=q`
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
`;function Hc(e){let t=(0,Z.c)(16),n,r,i,a,o;t[0]===e?(n=t[1],r=t[2],i=t[3],a=t[4],o=t[5]):({children:r,css:n,className:i,orientation:o,...a}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a,t[5]=o);let s=o===void 0?`horizontal`:o,c;t[6]===n?c=t[7]:(c=q(Vc,n),t[6]=n,t[7]=c);let l;t[8]===i?l=t[9]:(l=B(`react-aria-Tabs`,`tabs`,i),t[8]=i,t[9]=l);let u;return t[10]!==r||t[11]!==s||t[12]!==a||t[13]!==c||t[14]!==l?(u=G(Ne,{css:c,className:l,orientation:s,...a,children:r}),t[10]=r,t[11]=s,t[12]=a,t[13]=c,t[14]=l,t[15]=u):u=t[15],u}var Uc=q`
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
`,Wc=q`
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
`;function Gc(e){let t=(0,Z.c)(23),n,r,i,a,o;t[0]===e?(n=t[1],r=t[2],i=t[3],a=t[4],o=t[5]):({children:r,extra:a,css:n,className:i,...o}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a,t[5]=o);let{ref:s,hasOverflowAtStart:c,hasOverflowAtEnd:l}=Bc(),u;t[6]===n?u=t[7]:(u=q(Uc,n),t[6]=n,t[7]=u);let d;t[8]===i?d=t[9]:(d=B(`react-aria-TabList`,i),t[8]=i,t[9]=d);let f;t[10]!==r||t[11]!==l||t[12]!==c||t[13]!==o||t[14]!==s||t[15]!==u||t[16]!==d?(f=G(y,{ref:s,css:u,className:d,"data-overflow-start":c,"data-overflow-end":l,...o,children:r}),t[10]=r,t[11]=l,t[12]=c,t[13]=o,t[14]=s,t[15]=u,t[16]=d,t[17]=f):f=t[17];let p=f;if(a==null)return p;let m;t[18]===a?m=t[19]:(m=G(`div`,{className:`tab-list-row__extra`,children:a}),t[18]=a,t[19]=m);let h;return t[20]!==m||t[21]!==p?(h=H(`div`,{className:`tab-list-row`,css:Wc,children:[p,m]}),t[20]=m,t[21]=p,t[22]=h):h=t[22],h}var Kc=q`
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
`;function qc(e){let t=(0,Z.c)(14),n,r,i,a;t[0]===e?(n=t[1],r=t[2],i=t[3],a=t[4]):({css:n,className:r,padded:i,...a}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a);let o;t[5]===n?o=t[6]:(o=q(Kc,n),t[5]=n,t[6]=o);let s;t[7]===r?s=t[8]:(s=B(`react-aria-TabPanel`,r),t[7]=r,t[8]=s);let c;return t[9]!==i||t[10]!==a||t[11]!==o||t[12]!==s?(c=G(Ie,{css:o,className:s,"data-padded":i,...a}),t[9]=i,t[10]=a,t[11]=o,t[12]=s,t[13]=c):c=t[13],c}function Jc(e){let t=(0,Z.c)(11),n,r,i;t[0]===e?(n=t[1],r=t[2],i=t[3]):({children:n,id:r,...i}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i);let a;t[4]!==n||t[5]!==r?(a=e=>{let{state:t}=e,{selectedKey:i}=t;return i===r?n:null},t[4]=n,t[5]=r,t[6]=a):a=t[6];let o;return t[7]!==r||t[8]!==i||t[9]!==a?(o=G(qc,{id:r,...i,children:a}),t[7]=r,t[8]=i,t[9]=a,t[10]=o):o=t[10],o}var Yc=q`
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
`;function Xc(e){let t=(0,Z.c)(15),n,r,i,a;t[0]===e?(n=t[1],r=t[2],i=t[3],a=t[4]):({children:r,css:n,className:i,...a}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a);let o;t[5]===n?o=t[6]:(o=q(Yc,n),t[5]=n,t[6]=o);let s;t[7]===i?s=t[8]:(s=B(`react-aria-Tab`,i),t[7]=i,t[8]=s);let c;t[9]===Symbol.for(`react.memo_cache_sentinel`)?(c=G(it,{className:`react-aria-SelectionIndicator`}),t[9]=c):c=t[9];let l;return t[10]!==r||t[11]!==a||t[12]!==o||t[13]!==s?(l=H(M,{css:o,className:s,...a,children:[r,c]}),t[10]=r,t[11]=a,t[12]=o,t[13]=s,t[14]=l):l=t[14],l}var Zc=e=>{let t=(0,Z.c)(9),{message:n,size:r,className:i}=e,a;t[0]===Symbol.for(`react.memo_cache_sentinel`)?(a=q`
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        width: 100%;
        height: 100%;
        gap: var(--global-dimension-size-100);
      `,t[0]=a):a=t[0];let o;t[1]===r?o=t[2]:(o=G(ea,{isIndeterminate:!0,"aria-label":`loading`,size:r}),t[1]=r,t[2]=o);let s;t[3]===n?s=t[4]:(s=n==null?null:G(V,{children:n}),t[3]=n,t[4]=s);let c;return t[5]!==i||t[6]!==o||t[7]!==s?(c=H(`div`,{className:i,css:a,children:[o,s]}),t[5]=i,t[6]=o,t[7]=s,t[8]=c):c=t[8],c},Qc=Gt`
  0% {
    opacity: 1;
  }
  50% {
    opacity: 0.4;
  }
  100% {
    opacity: 1;
  }
`,$c=Gt`
  0% {
    transform: translateX(-100%);
  }
  50% {
    transform: translateX(100%);
  }
  100% {
    transform: translateX(100%);
  }
`,el=q`
  display: block;
  background-color: var(--global-color-gray-200);
`,tl=q`
  animation: ${Qc} 2s ease-in-out 0.5s infinite;
`,nl=q`
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
`,rl=e=>{if(typeof e==`number`)return`${e}px`;if(typeof e==`string`)switch(e){case`none`:return`0`;case`XS`:return`var(--global-rounding-xsmall)`;case`S`:return`var(--global-rounding-small)`;case`M`:return`var(--global-rounding-medium)`;case`L`:return`var(--global-rounding-large)`;case`circle`:return`50%`;default:return e}return`var(--global-rounding-medium)`};function il({ref:e,width:t=`100%`,height:n=`1.2em`,borderRadius:r=`S`,animation:i=`pulse`,className:a,...o}){let s=typeof t==`number`?`${t}px`:t,c=typeof n==`number`?`${n}px`:n,l=rl(r);return G(`span`,{ref:e,className:B(a,`skeleton`),css:[el,i===`pulse`&&tl,i===`wave`&&nl,q`
          width: ${s};
          height: ${c};
          border-radius: ${l};
        `],...o})}il.displayName=`Skeleton`;var al=e=>{let t=(0,Z.c)(5),n,r,i;t[0]===Symbol.for(`react.memo_cache_sentinel`)?(n=G(il,{height:100,borderRadius:8,animation:`wave`}),r=G(il,{height:24,width:`80%`,animation:`wave`}),i=G(il,{height:16,width:`60%`,animation:`wave`}),t[0]=n,t[1]=r,t[2]=i):(n=t[0],r=t[1],i=t[2]);let a;return t[3]===e?a=t[4]:(a=H(K,{direction:`column`,gap:`size-100`,width:`100%`,...e,children:[n,r,i]}),t[3]=e,t[4]=a),a},ol=q`
  display: flex;
  flex-direction: column;
`,sl=q`
  display: flex;
  gap: 6px;
`,cl=[[3,2,5,1.5,4,2.5,4],[2,4,1.5,5,3,3.5],[4,2.5,5,2,3],[3,4.5,2,4,1.5,4],[3.5,2,5,2.5]],ll=[`100%`,`95%`,`100%`,`88%`,`92%`];function ul({lines:e=3,animation:t=`pulse`,gap:n=8}){let r=(e,t)=>{let n=cl[e%cl.length],r=t?Math.ceil(n.length*.5):n.length;return n.slice(0,r)};return G(`div`,{css:[ol,q`
          gap: ${n}px;
        `],children:Array.from({length:e},(n,i)=>{let a=i===e-1,o=r(i,a),s=a?`55%`:ll[i%ll.length];return G(`div`,{css:[sl,q`
                width: ${s};
              `],children:o.map((e,n)=>G(il,{css:q`
                  flex-grow: ${e};
                  min-width: 20px;
                `,height:`1em`,animation:t},n))},i)})})}var dl=q`
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
`;function fl(e){let t=(0,Z.c)(14),n,r;t[0]===e?(n=t[1],r=t[2]):({ref:r,...n}=e,t[0]=e,t[1]=n,t[2]=r);let i,a;t[3]===n?(i=t[4],a=t[5]):({size:a,...i}=n,t[3]=n,t[4]=i,t[5]=a);let o=a===void 0?`M`:a,s;t[6]===Symbol.for(`react.memo_cache_sentinel`)?(s=q(us,dl),t[6]=s):s=t[6];let c;t[7]!==i||t[8]!==r||t[9]!==o?(c=G(x,{"data-size":o,className:`select`,ref:r,css:s,...i}),t[7]=i,t[8]=r,t[9]=o,t[10]=c):c=t[10];let l;return t[11]!==o||t[12]!==c?(l=G(Dt,{size:o,children:c}),t[11]=o,t[12]=c,t[13]=l):l=t[13],l}function pl(e){let t=(0,Z.c)(10),n,r,i;t[0]===e?(n=t[1],r=t[2],i=t[3]):({ref:r,children:n,...i}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i);let a;t[4]===n?a=t[5]:(a=e=>{let{isSelected:t}=e;return H(K,{direction:`row`,justifyContent:`space-between`,alignItems:`center`,gap:`size-200`,width:`100%`,children:[G(`span`,{children:n}),t&&G(U,{svg:G(En,{})})]})},t[4]=n,t[5]=a);let o;return t[6]!==r||t[7]!==i||t[8]!==a?(o=G(f,{...i,ref:r,children:a}),t[6]=r,t[7]=i,t[8]=a,t[9]=o):o=t[9],o}pl.displayName=`SelectItem`,q`
  max-width: 100%;
  height: auto;
`;var ml=16,hl=8,gl=.05,_l=Gt`
  from {
    opacity: 0;
    transform: translateY(-130%);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
`,vl=q`
  position: fixed;
  top: var(--global-dimension-size-200);
  left: 50%;
  width: 400px;
  max-width: calc(100vw - var(--global-dimension-size-400));
  transform: translateX(-50%);
  outline: none;
  z-index: ${Gn};

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
`,yl=q`
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
`,bl=q`
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
`;function xl(e){let t=(0,Z.c)(6),{stackIndex:n,children:r}=e,i=100-n,a;t[0]!==n||t[1]!==i?(a={"--toast-index":n,zIndex:i},t[0]=n,t[1]=i,t[2]=a):a=t[2];let o;return t[3]!==r||t[4]!==a?(o=G(`div`,{className:`toast-positioner`,css:yl,style:a,children:r}),t[3]=r,t[4]=a,t[5]=o):o=t[5],o}var Sl=e=>{switch(e){case`success`:return G(U,{svg:G(un,{})});case`error`:return G(U,{svg:G(Nn,{})});default:return null}},Cl=e=>{switch(e){case`success`:return`var(--global-color-success)`;case`error`:return`var(--global-color-danger)`;default:return`var(--global-color-gray-600)`}},wl=e=>{let t=(0,Z.c)(33),{toast:n}=e,{theme:r}=Pr(),i=(0,X.useContext)(te),a;t[0]!==i?.visibleToasts||t[1]!==n.key?(a=i?.visibleToasts.findIndex(e=>e.key===n.key)??0,t[0]=i?.visibleToasts,t[1]=n.key,t[2]=a):a=t[2];let o=Math.max(0,a),s;t[3]===n.content.variant?s=t[4]:(s=Sl(n.content.variant),t[3]=n.content.variant,t[4]=s);let c=s,l;t[5]===n.content.variant?l=t[6]:(l=Cl(n.content.variant),t[5]=n.content.variant,t[6]=l);let u;t[7]===l?u=t[8]:(u={"--internal-token-color":l},t[7]=l,t[8]=u);let d;t[9]===Symbol.for(`react.memo_cache_sentinel`)?(d=q`
            display: flex;
            justify-content: space-between;
            width: 100%;
          `,t[9]=d):d=t[9];let f;t[10]!==c||t[11]!==n.content.title?(f=H(V,{slot:`title`,size:`M`,children:[c,n.content.title]}),t[10]=c,t[11]=n.content.title,t[12]=f):f=t[12];let p;t[13]===n.content.message?p=t[14]:(p=G(V,{slot:`description`,children:n.content.message}),t[13]=n.content.message,t[14]=p);let m;t[15]!==f||t[16]!==p?(m=H(me,{children:[f,p]}),t[15]=f,t[16]=p,t[17]=m):m=t[17];let h;t[18]===Symbol.for(`react.memo_cache_sentinel`)?(h=G(hn,{slot:`close`,size:`S`,color:`inherit`,type:`button`,"aria-label":`Close notification`,children:G(U,{svg:G(rt,{})})}),t[18]=h):h=t[18];let g;t[19]===m?g=t[20]:(g=H(`div`,{css:d,children:[m,h]}),t[19]=m,t[20]=g);let _;t[21]!==n.content.action||t[22]!==n.key?(_=n.content.action?G(`div`,{className:`toast-action-container`,children:typeof n.content.action==`object`&&`text`in n.content.action?G(Nt,{className:`toast-action-button`,onPress:()=>{let e=n.content.action;if(typeof e==`object`&&e&&`onClick`in e){let t=e.closeOnClick??!0,r=()=>{br?.close(n.key)};e.onClick(r),t&&r()}},size:`S`,children:n.content.action.text}):n.content.action}):null,t[21]=n.content.action,t[22]=n.key,t[23]=_):_=t[23];let v;t[24]!==g||t[25]!==_||t[26]!==u||t[27]!==r||t[28]!==n?(v=H(be,{toast:n,css:bl,className:`react-aria-Toast`,style:u,"data-variant":n.content.variant,"data-theme":r,children:[g,_]}),t[24]=g,t[25]=_,t[26]=u,t[27]=r,t[28]=n,t[29]=v):v=t[29];let y;return t[30]!==o||t[31]!==v?(y=G(xl,{stackIndex:o,children:v}),t[30]=o,t[31]=v,t[32]=y):y=t[32],y},Tl=q`
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
`;function El(e){let t=(0,Z.c)(12),n,r;t[0]===e?(n=t[1],r=t[2]):({ref:r,...n}=e,t[0]=e,t[1]=n,t[2]=r);let i,a;t[3]===n?(i=t[4],a=t[5]):({children:i,...a}=n,t[3]=n,t[4]=i,t[5]=a);let o;t[6]===i?o=t[7]:(o=e=>{let{isCurrent:t}=e;return H(W,{children:[i,!t&&G(U,{svg:G(Xn,{})})]})},t[6]=i,t[7]=o);let s;return t[8]!==r||t[9]!==a||t[10]!==o?(s=G(Ae,{css:Tl,...a,className:`breadcrumb`,ref:r,children:o}),t[8]=r,t[9]=a,t[10]=o,t[11]=s):s=t[11],s}var Dl=q`
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
`;function Ol(e){let t=(0,Z.c)(10),n,r;t[0]===e?(n=t[1],r=t[2]):({ref:r,...n}=e,t[0]=e,t[1]=n,t[2]=r);let i,a;t[3]===n?(i=t[4],a=t[5]):({size:a,...i}=n,t[3]=n,t[4]=i,t[5]=a);let o=a===void 0?`M`:a,s;return t[6]!==r||t[7]!==i||t[8]!==o?(s=G(k,{css:Dl,...i,ref:r,"data-size":o}),t[6]=r,t[7]=i,t[8]=o,t[9]=s):s=t[9],s}var kl=q`
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
`;function Al(e){let t=(0,Z.c)(10),n,r,i,a;t[0]===e?(n=t[1],r=t[2],i=t[3],a=t[4]):({ref:i,size:a,children:n,...r}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a);let o=a===void 0?`M`:a,s;return t[5]!==n||t[6]!==r||t[7]!==i||t[8]!==o?(s=G(`ul`,{ref:i,css:kl,"data-list-size":o,...r,children:n}),t[5]=n,t[6]=r,t[7]=i,t[8]=o,t[9]=s):s=t[9],s}function jl(e){let t=(0,Z.c)(8),n,r,i;t[0]===e?(n=t[1],r=t[2],i=t[3]):({ref:i,children:n,...r}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i);let a;return t[4]!==n||t[5]!==r||t[6]!==i?(a=G(`li`,{ref:i,...r,children:n}),t[4]=n,t[5]=r,t[6]=i,t[7]=a):a=t[7],a}var Ml=Gt`
  from {
    transform: translate(-50%, var(--global-dimension-size-450));
    opacity: 0;
  }
  to {
    transform: translate(-50%, 0);
    opacity: 1;
  }
`,Nl=q`
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
`,Pl=e=>{let t=(0,Z.c)(2),{children:n}=e,r;return t[0]===n?r=t[1]:(r=G(`div`,{css:Nl,children:n}),t[0]=n,t[1]=r),r},Fl=q`
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
`;function Il(e){let t=(0,Z.c)(6),n,r;t[0]===e?(n=t[1],r=t[2]):({ref:r,...n}=e,t[0]=e,t[1]=n,t[2]=r);let i;return t[3]!==n||t[4]!==r?(i=G(P,{...n,ref:r,css:Fl,children:n.children}),t[3]=n,t[4]=r,t[5]=i):i=t[5],i}var Ll=q`
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
`;function Rl(e){let t=(0,Z.c)(6),n,r;t[0]===e?(n=t[1],r=t[2]):({ref:r,...n}=e,t[0]=e,t[1]=n,t[2]=r);let i;return t[3]!==n||t[4]!==r?(i=G(Bt,{...n,ref:r,css:Ll,className:`separator react-aria-Separator`}),t[3]=n,t[4]=r,t[5]=i):i=t[5],i}var zl=(0,X.createContext)(null);function Bl(e){let t=(0,Z.c)(5),{isCollapsed:n,children:r}=e,i;t[0]===n?i=t[1]:(i={isCollapsed:n},t[0]=n,t[1]=i);let a=i,o;return t[2]!==r||t[3]!==a?(o=G(zl.Provider,{value:a,children:r}),t[2]=r,t[3]=a,t[4]=o):o=t[4],o}function Vl(){return(0,X.useContext)(zl)}var Hl=e=>q`
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
`;function Ul(e){let t=(0,Z.c)(85),n,r,i,a,o,s,c,l,u,d,f,p,m,h,g,_,v,y;t[0]===e?(n=t[1],r=t[2],i=t[3],a=t[4],o=t[5],s=t[6],c=t[7],l=t[8],u=t[9],d=t[10],f=t[11],p=t[12],m=t[13],h=t[14],g=t[15],_=t[16],v=t[17],y=t[18]):({ref:u,title:v,titleExtra:y,titleSeparator:f,subTitle:d,headerContent:a,children:n,collapsible:p,interactiveTitle:m,collapseButtonLabel:r,defaultOpen:h,isOpen:o,scrollBody:g,extra:i,onCollapseChange:s,onOpenChange:c,testId:_,...l}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a,t[5]=o,t[6]=s,t[7]=c,t[8]=l,t[9]=u,t[10]=d,t[11]=f,t[12]=p,t[13]=m,t[14]=h,t[15]=g,t[16]=_,t[17]=v,t[18]=y);let b=f===void 0||f,x=p!==void 0&&p,S=m!==void 0&&m,C=h===void 0||h,w=g!==void 0&&g,{styleProps:T}=Mn(l,Tn),[E,D]=(0,X.useState)(x?!C:!1),O=o==null?E:!o,k=(0,X.useId)(),A=(0,X.useId)(),j=(0,X.useId)(),M=(0,X.useId)(),N;t[19]===s?N=t[20]:(N=e=>{s?.(e)},t[19]=s,t[20]=N);let P=(0,X.useEffectEvent)(N),F;t[21]!==P||t[22]!==O?(F=()=>{P(O)},t[21]=P,t[22]=O,t[23]=F):F=t[23];let I;t[24]===O?I=t[25]:(I=[O],t[24]=O,t[25]=I),(0,X.useEffect)(F,I);let L;t[26]!==v||t[27]!==y?(L=H(at,{level:3,weight:`heavy`,className:`card__title`,children:[v,y]}),t[26]=v,t[27]=y,t[28]=L):L=t[28];let R;t[29]===d?R=t[30]:(R=d&&G(at,{level:4,className:`card__sub-title`,children:d}),t[29]=d,t[30]=R);let ee;t[31]===a?ee=t[32]:(ee=a&&G(`div`,{className:`card__header-content`,children:a}),t[31]=a,t[32]=ee);let te;t[33]!==R||t[34]!==ee||t[35]!==L||t[36]!==j?(te=H(`div`,{id:j,className:`card__heading`,children:[L,R,ee]}),t[33]=R,t[34]=ee,t[35]=L,t[36]=j,t[37]=te):te=t[37];let ne=te,re;t[38]!==O||t[39]!==c?(re=()=>{D(!O),c?.(O)},t[38]=O,t[39]=c,t[40]=re):re=t[40];let ie=re,ae;t[41]===ie?ae=t[42]:(ae=e=>{let t=e.target;t instanceof Element&&t.closest(`button,a,input,select,textarea,[role="button"]`)||ie()},t[41]=ie,t[42]=ae);let oe=ae,se=!O,ce=S?r:void 0,le=S&&r==null?j:void 0,ue=!O,de;t[43]===ue?de=t[44]:(de=G(qt,{isExpanded:ue,className:`card__collapse-toggle-icon`}),t[43]=ue,t[44]=de);let fe=!S&&ne,pe;t[45]!==M||t[46]!==A||t[47]!==se||t[48]!==ce||t[49]!==le||t[50]!==de||t[51]!==fe||t[52]!==ie?(pe=H(`button`,{onClick:ie,className:`card__collapsible-button button--reset`,id:A,"aria-controls":M,"aria-expanded":se,"aria-label":ce,"aria-labelledby":le,children:[de,fe]}),t[45]=M,t[46]=A,t[47]=se,t[48]=ce,t[49]=le,t[50]=de,t[51]=fe,t[52]=ie,t[53]=pe):pe=t[53];let me=pe,he;t[54]===T.style?he=t[55]:(he=Hl(T.style),t[54]=T.style,t[55]=he);let ge;t[56]!==me||t[57]!==x||t[58]!==oe||t[59]!==ne||t[60]!==S?(ge=x?S?H(`div`,{className:`card__collapsible-header`,onClick:oe,children:[me,ne]}):me:ne,t[56]=me,t[57]=x,t[58]=oe,t[59]=ne,t[60]=S,t[61]=ge):ge=t[61];let _e;t[62]!==i||t[63]!==k||t[64]!==ge?(_e=H(`header`,{id:k,children:[ge,i]}),t[62]=i,t[63]=k,t[64]=ge,t[65]=_e):_e=t[65];let ve;t[66]!==M||t[67]!==n||t[68]!==k||t[69]!==O||t[70]!==w?(ve=G(`div`,{className:`card__body`,id:M,"aria-labelledby":k,"aria-hidden":O,"data-scrollable":w,children:n}),t[66]=M,t[67]=n,t[68]=k,t[69]=O,t[70]=w,t[71]=ve):ve=t[71];let ye;t[72]!==x||t[73]!==O||t[74]!==u||t[75]!==T.style||t[76]!==he||t[77]!==_e||t[78]!==ve||t[79]!==_||t[80]!==b?(ye=H(`section`,{ref:u,css:he,className:`card`,"data-collapsible":x,"data-collapsed":O,"data-title-separator":b,"data-testid":_,style:T.style,children:[_e,ve]}),t[72]=x,t[73]=O,t[74]=u,t[75]=T.style,t[76]=he,t[77]=_e,t[78]=ve,t[79]=_,t[80]=b,t[81]=ye):ye=t[81];let be;return t[82]!==O||t[83]!==ye?(be=G(Bl,{isCollapsed:O,children:ye}),t[82]=O,t[83]=ye,t[84]=be):be=t[84],be}var Wl=q`
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
`;function Gl(e){let t=(0,Z.c)(2),{children:n}=e;if(!Vl()?.isCollapsed||!n)return null;let r;return t[0]===n?r=t[1]:(r=G(`span`,{className:`card__collapsed-preview`,css:Wl,"aria-hidden":`true`,children:n}),t[0]=n,t[1]=r),r}var Kl=q`
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
`;function ql(e){let t=(0,Z.c)(13),n,r,i,o,s;t[0]===e?(n=t[1],r=t[2],i=t[3],o=t[4],s=t[5]):({ref:i,children:n,labelPlacement:o,size:s,...r}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=o,t[5]=s);let c=o===void 0?`end`:o,l=s===void 0?`M`:s,u;t[6]===Symbol.for(`react.memo_cache_sentinel`)?(u=G(`div`,{className:`indicator`}),t[6]=u):u=t[6];let d;return t[7]!==n||t[8]!==c||t[9]!==r||t[10]!==i||t[11]!==l?(d=H(a,{...r,ref:i,css:Kl,"data-label-placement":c,"data-size":l,children:[u,n]}),t[7]=n,t[8]=c,t[9]=r,t[10]=i,t[11]=l,t[12]=d):d=t[12],d}q`
  position: relative;
`,q`
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
`;var Jl=q`
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
`,Yl=q`
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
`;q`
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
`;function Xl(e,t){let{si:n=!1,decimalPlaces:r=1}=t??{},i=n?1e3:1024;if(Math.abs(e)<i)return e+` B`;let a=n?[`kB`,`MB`,`GB`,`TB`,`PB`,`EB`,`ZB`,`YB`]:[`KiB`,`MiB`,`GiB`,`TiB`,`PiB`,`EiB`,`ZiB`,`YiB`],o=-1,s=10**r;do e/=i,++o;while(Math.round(Math.abs(e)*s)/s>=i&&o<a.length-1);return e.toFixed(r)+` `+a[o]}function Zl(e,t){return!t||t.length===0||t.some(t=>{if(t.startsWith(`.`))return e.name.toLowerCase().endsWith(t.toLowerCase());if(t.endsWith(`/*`)){let n=t.slice(0,-2);return e.type.startsWith(n)}return e.type===t})}function Ql(e,t){return t==null||e.size<=t}function $l(e){let t=(0,Z.c)(46),n,r,i,a,o,s,c,l,u,d;t[0]===e?(n=t[1],r=t[2],i=t[3],a=t[4],o=t[5],s=t[6],c=t[7],l=t[8],u=t[9],d=t[10]):({acceptedFileTypes:n,allowsMultiple:u,maxFiles:s,maxFileSize:o,onSelect:c,onSelectRejected:l,label:d,description:i,isDisabled:a,...r}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a,t[5]=o,t[6]=s,t[7]=c,t[8]=l,t[9]=u,t[10]=d);let f=u!==void 0&&u,p=d===void 0?`Drag and drop files here`:d,m=(0,X.useRef)(null),h=(0,X.useRef)(null),_,v;t[11]===a?(_=t[12],v=t[13]):(_=()=>{let e=h.current;if(!e||a)return;let t=e=>{(e.key===`Enter`||e.key===` `)&&(e.preventDefault(),m.current?.click())};return e.addEventListener(`keydown`,t),()=>e.removeEventListener(`keydown`,t)},v=[a],t[11]=a,t[12]=_,t[13]=v),(0,X.useEffect)(_,v);let y;t[14]!==n||t[15]!==f||t[16]!==o||t[17]!==s||t[18]!==c||t[19]!==l?(y=e=>{let t=[],r=[],i=f?s??1/0:1;for(let a of e){if(!Zl(a,n)){r.push({file:a,reason:`type`,message:`File type not accepted. Allowed: ${n?.join(`, `)}`});continue}if(!Ql(a,o)){r.push({file:a,reason:`size`,message:`File too large. Maximum size: ${Xl(o)}`});continue}if(t.length>=i){r.push({file:a,reason:`count`,message:`Maximum ${i} file${i>1?`s`:``} allowed`});continue}t.push(a)}t.length>0&&c&&c(t),r.length>0&&l&&l(r)},t[14]=n,t[15]=f,t[16]=o,t[17]=s,t[18]=c,t[19]=l,t[20]=y):y=t[20];let b=y,x;t[21]===b?x=t[22]:(x=e=>{e.target.files&&(b(Array.from(e.target.files)),e.target.value=``)},t[21]=b,t[22]=x);let S=x,C;t[23]===b?C=t[24]:(C=async e=>{let t=e.items.filter(ru),n=(await Promise.allSettled(t.map(nu))).filter(tu).map(eu);n.length>0&&b(n)},t[23]=b,t[24]=C);let w=C,T;t[25]!==n||t[26]!==a?(T=e=>a?`cancel`:!n||n.length===0||n.some(t=>t.startsWith(`.`)||t.endsWith(`/*`)?!0:e.has(t))?`copy`:`cancel`,t[25]=n,t[26]=a,t[27]=T):T=t[27];let E=T,D;t[28]===a?D=t[29]:(D=()=>{a||m.current?.click()},t[28]=a,t[29]=D);let O=D,k;t[30]!==n||t[31]!==i?(k=i??(n&&n.length>0?`Accepted: ${n.join(`, `)}`:void 0),t[30]=n,t[31]=i,t[32]=k):k=t[32];let A=k,j;t[33]!==n||t[34]!==f||t[35]!==A||t[36]!==S||t[37]!==p||t[38]!==O?(j=e=>{let{isDropTarget:t}=e;return H(W,{children:[G(`input`,{ref:m,type:`file`,accept:n?.join(`,`),multiple:f,onChange:S,hidden:!0}),H(`div`,{className:`file-drop-zone__trigger`,onClick:O,children:[G(`div`,{className:`file-drop-zone__icon`,children:G(U,{svg:G(Vt,{})})}),G(Zn,{className:`file-drop-zone__label`,children:t?`Drop files here`:p}),A?G(Zn,{className:`file-drop-zone__description`,children:A}):null]})]})},t[33]=n,t[34]=f,t[35]=A,t[36]=S,t[37]=p,t[38]=O,t[39]=j):j=t[39];let M;return t[40]!==r||t[41]!==E||t[42]!==w||t[43]!==a||t[44]!==j?(M=G(g,{ref:h,css:Jl,onDrop:w,getDropOperation:E,isDisabled:a,...r,children:j}),t[40]=r,t[41]=E,t[42]=w,t[43]=a,t[44]=j,t[45]=M):M=t[45],M}function eu(e){return e.value}function tu(e){return e.status===`fulfilled`}function nu(e){return e.getFile()}function ru(e){return e.kind===`file`}function iu(e){switch(e.status){case`pending`:return`Pending`;case`uploading`:return`Uploading${e.progress===void 0?``:` ${e.progress}%`}`;case`parsing`:return`Parsing...`;case`complete`:return`Complete`;case`error`:return`Error`;default:return``}}function au(e){let t=(0,Z.c)(32),{file:n,onRemove:r,isDisabled:i}=e,{file:a,progress:o,status:s,error:c}=n,l=s===`uploading`&&o!==void 0,u;t[0]===Symbol.for(`react.memo_cache_sentinel`)?(u=G(`div`,{className:`file-list__icon`,children:G(U,{svg:G(Ut,{})})}),t[0]=u):u=t[0];let d;t[1]===a.name?d=t[2]:(d=G(`span`,{className:`file-list__name`,title:a.name,children:a.name}),t[1]=a.name,t[2]=d);let f;t[3]===a.size?f=t[4]:(f=Xl(a.size),t[3]=a.size,t[4]=f);let p;t[5]===f?p=t[6]:(p=G(`span`,{children:f}),t[5]=f,t[6]=p);let m;t[7]!==n||t[8]!==s?(m=s&&H(W,{children:[G(`span`,{children:`-`}),G(`span`,{children:iu(n)})]}),t[7]=n,t[8]=s,t[9]=m):m=t[9];let h;t[10]!==p||t[11]!==m?(h=H(`div`,{className:`file-list__meta`,children:[p,m]}),t[10]=p,t[11]=m,t[12]=h):h=t[12];let g;t[13]===c?g=t[14]:(g=c&&G(`span`,{className:`file-list__error`,children:c}),t[13]=c,t[14]=g);let _;t[15]!==o||t[16]!==l?(_=l&&G(`div`,{className:`file-list__progress`,children:G(ta,{value:o,width:`100%`,height:`4px`})}),t[15]=o,t[16]=l,t[17]=_):_=t[17];let v;t[18]!==d||t[19]!==h||t[20]!==g||t[21]!==_?(v=H(`div`,{className:`file-list__details`,children:[d,h,g,_]}),t[18]=d,t[19]=h,t[20]=g,t[21]=_,t[22]=v):v=t[22];let y;t[23]!==a||t[24]!==i||t[25]!==r||t[26]!==s?(y=r&&G(`div`,{className:`file-list__remove`,children:G(hn,{size:`S`,"aria-label":`Remove ${a.name}`,onPress:()=>r(a),isDisabled:i||s===`uploading`||s===`parsing`,children:G(U,{svg:G(rt,{})})})}),t[23]=a,t[24]=i,t[25]=r,t[26]=s,t[27]=y):y=t[27];let b;return t[28]!==s||t[29]!==y||t[30]!==v?(b=H(`li`,{className:`file-list__item`,"data-status":s,children:[u,v,y]}),t[28]=s,t[29]=y,t[30]=v,t[31]=b):b=t[31],b}function ou(e){let t=(0,Z.c)(12),{files:n,onRemove:r,isDisabled:i,children:a,"aria-label":o}=e,s=o===void 0?`Selected files`:o;if(n.length===0)return null;let c=su,l;t[0]!==a||t[1]!==i||t[2]!==r?(l=(e,t)=>a?G(X.Fragment,{children:a(e,t)},c(e)):G(au,{file:e,onRemove:r,isDisabled:i},c(e)),t[0]=a,t[1]=i,t[2]=r,t[3]=l):l=t[3];let u=l,d;if(t[4]!==n||t[5]!==u){let e;t[7]===u?e=t[8]:(e=(e,t)=>u(e,t),t[7]=u,t[8]=e),d=n.map(e),t[4]=n,t[5]=u,t[6]=d}else d=t[6];let f;return t[9]!==s||t[10]!==d?(f=G(`ul`,{css:Yl,"aria-label":s,children:d}),t[9]=s,t[10]=d,t[11]=f):f=t[11],f}function su(e){return`${e.file.name}-${e.file.size}-${e.file.lastModified}`}var cu=e=>q`
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: ${e};
  overflow: hidden;
  text-overflow: ellipsis;
`;function lu(e){let t=(0,Z.c)(5),{children:n,lines:r}=e,i;t[0]===r?i=t[1]:(i=cu(r),t[0]=r,t[1]=i);let a;return t[2]!==n||t[3]!==i?(a=G(`div`,{css:i,children:n}),t[2]=n,t[3]=i,t[4]=a):a=t[4],a}function uu(e){let t=(0,Z.c)(3),{children:n}=e,r;t[0]===Symbol.for(`react.memo_cache_sentinel`)?(r={display:`contents`},t[0]=r):r=t[0];let i;return t[1]===n?i=t[2]:(i=G(`div`,{style:r,onClick:gu,onKeyDown:hu,onKeyUp:mu,onMouseDown:pu,onPointerDown:fu,onPointerUp:du,children:n}),t[1]=n,t[2]=i),i}function du(e){return e.stopPropagation()}function fu(e){return e.stopPropagation()}function pu(e){return e.stopPropagation()}function mu(e){return e.stopPropagation()}function hu(e){return e.stopPropagation()}function gu(e){return e.stopPropagation()}var _u=q`
  border-radius: var(--global-dimension-size-50);
  border: 1px solid var(--global-border-color-default);
  transition: background-color 0.2s;
  &[data-clickable="true"] {
    cursor: pointer;
    &:hover {
      background-color: var(--global-color-gray-300);
    }
  }
`,vu=q`
  width: 1px;
  height: 0.7em;
  background-color: currentColor;
  opacity: 0.2;
`,yu=q`
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
`,bu=q`
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
`,xu=q`
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
`,Su=1.5;function Cu(e){return e.offsetWidth>0||e.offsetHeight>0}function wu(e){return Array.from(e.children).filter(e=>e instanceof HTMLElement&&Cu(e))}function Tu(e){let{paddingRight:t}=getComputedStyle(e);return e.clientWidth-(parseFloat(t)||0)}function Eu(e){let t=wu(e),n=Tu(e),r=0,i=0,a=0,o=1/0,s=-1/0;for(let e of t){let t=e.offsetTop,c=t+e.offsetHeight;if(r>0&&(t>=s||c<=o))break;let l=e.offsetLeft+e.offsetWidth;if(l>n+Su)break;r+=1,o=Math.min(o,t),s=Math.max(s,c),i=Math.max(i,l),a=Math.max(a,e.offsetHeight)}return{items:t,visibleCount:r,badgeLeft:i,lineHeight:a||(t[0]?.offsetHeight??0)}}var Du=[{name:`inert`,value:``,flag:`overflowRowInert`},{name:`aria-hidden`,value:`true`,flag:`overflowRowAriaHidden`}];function Ou({items:e,visibleCount:t}){e.forEach((e,n)=>{if(n<t){ku(e);return}for(let{name:t,value:n,flag:r}of Du)e.hasAttribute(t)||(e.dataset[r]=`true`,e.setAttribute(t,n))})}function ku(e){for(let{name:t,flag:n}of Du)e.dataset[n]&&(delete e.dataset[n],e.removeAttribute(t))}function Au(e){for(let t of Array.from(e.children))t instanceof HTMLElement&&ku(t)}var ju={childList:!0,characterData:!0,subtree:!0};function Mu(e){let t=e=>(e instanceof Element?e:e.parentElement)?.closest(`.overflow-row__badge-slot`)!=null;return e.type===`childList`?[...e.addedNodes,...e.removedNodes].every(t):t(e.target)}function Nu(e,t){return e===null||t===null?e===t:e.hiddenCount===t.hiddenCount&&e.visibleCount===t.visibleCount&&e.badgeLeft===t.badgeLeft&&e.lineHeight===t.lineHeight}function Pu(e){let t=(0,Z.c)(5),{visibleCount:n,children:r}=e,i=(0,X.useRef)(null),a,o;t[0]===n?(a=t[1],o=t[2]):(a=()=>{let e=i.current;if(!e)return;let t=()=>{let t=Array.from(e.children).filter(Iu);for(let e of t)e.dataset.overflowRowHidden&&(e.style.display=``,delete e.dataset.overflowRowHidden);t.filter(Cu).slice(0,n).forEach(Fu)};t();let r=new MutationObserver(t);return r.observe(e,ju),()=>r.disconnect()},o=[n],t[0]=n,t[1]=a,t[2]=o),(0,X.useLayoutEffect)(a,o);let s;return t[3]===r?s=t[4]:(s=G(K,{ref:i,direction:`row`,wrap:`wrap`,gap:`size-50`,maxWidth:`size-5000`,children:r}),t[3]=r,t[4]=s),s}function Fu(e){e.style.display=`none`,e.dataset.overflowRowHidden=`true`}function Iu(e){return e instanceof HTMLElement}function Lu(e){let t=(0,Z.c)(21),{children:n,isExpanded:r}=e,i=r!==void 0&&r,a=(0,X.useRef)(null),o=(0,X.useRef)(null),[s,c]=(0,X.useState)(null),l,u;t[0]===i?(l=t[1],u=t[2]):(l=()=>{let e=a.current;if(i||!e){c(null);return}let t=null,n=()=>{t=e.getBoundingClientRect().width;let{items:n,visibleCount:r,badgeLeft:i,lineHeight:a}=Eu(e);Ou({items:n,visibleCount:r});let o=n.length-r,s=o===0?null:{hiddenCount:o,visibleCount:r,badgeLeft:i,lineHeight:a};c(e=>Nu(e,s)?e:s)};n(),o.current=n;let r=!1;document.fonts?.status===`loading`&&document.fonts.ready.then(()=>{r||n()});let s=new ResizeObserver(e=>{let[r]=e,i=r?.borderBoxSize?.[0]?.inlineSize??null;(i===null||i!==t)&&(t=i,n())});s.observe(e);let l=new MutationObserver(e=>{e.every(Mu)||n()});return l.observe(e,ju),()=>{r=!0,s.disconnect(),l.disconnect(),o.current=null,Au(e)}},u=[i],t[0]=i,t[1]=l,t[2]=u),(0,X.useLayoutEffect)(l,u);let d,f;t[3]===s?(d=t[4],f=t[5]):(d=()=>{s!==null&&o.current?.()},f=[s],t[3]=s,t[4]=d,t[5]=f),(0,X.useLayoutEffect)(d,f);let p=!i,m=!i&&s!==null,h=!i&&s!==null&&s.visibleCount===0,g;t[6]!==p||t[7]!==m||t[8]!==h?(g=B(`overflow-row`,{"overflow-row--collapsed":p,"overflow-row--overflowing":m,"overflow-row--badge-only":h}),t[6]=p,t[7]=m,t[8]=h,t[9]=g):g=t[9];let _;t[10]===s?_=t[11]:(_=s===null?void 0:{"--overflow-row-badge-left":`calc(${s.badgeLeft}px + var(--global-dimension-size-50))`,"--overflow-row-line-height":`${s.lineHeight}px`},t[10]=s,t[11]=_);let v;t[12]!==n||t[13]!==i||t[14]!==s?(v=!i&&s!==null?G(`div`,{className:`overflow-row__badge-slot`,children:H(Yt,{children:[H(Jt,{className:`overflow-row__badge`,"data-clickable":`true`,"aria-label":`Show ${s.hiddenCount} more`,children:[`+`,s.hiddenCount]}),G(uu,{children:H(qn,{placement:`bottom end`,children:[G(Lt,{}),G(fn,{children:G(ra,{padding:`size-150`,children:G(Pu,{visibleCount:s.visibleCount,children:n})})})]})})]})}):null,t[12]=n,t[13]=i,t[14]=s,t[15]=v):v=t[15];let y;return t[16]!==n||t[17]!==_||t[18]!==v||t[19]!==g?(y=H(`div`,{ref:a,css:xu,className:g,style:_,children:[n,v]}),t[16]=n,t[17]=_,t[18]=v,t[19]=g,t[20]=y):y=t[20],y}var Ru=q`
  text-overflow: ellipsis;
  overflow: hidden;
  white-space: nowrap;
`,zu=q`
  display: -webkit-box;
  -webkit-box-orient: vertical;
  overflow: hidden;
`,Bu=e=>{let t=(0,Z.c)(11),{children:n,maxWidth:r,title:i,maxLines:a}=e,o=(a??0)>1,s=o?zu:Ru,c;t[0]!==o||t[1]!==a?(c=o&&{WebkitLineClamp:a},t[0]=o,t[1]=a,t[2]=c):c=t[2];let l;t[3]!==r||t[4]!==c?(l={maxWidth:r,...c},t[3]=r,t[4]=c,t[5]=l):l=t[5];let u;return t[6]!==n||t[7]!==s||t[8]!==l||t[9]!==i?(u=G(`div`,{css:s,style:l,title:i,children:n}),t[6]=n,t[7]=s,t[8]=l,t[9]=i,t[10]=u):u=t[10],u};function Vu(){let e=(0,Z.c)(3),t,n;e[0]===Symbol.for(`react.memo_cache_sentinel`)?(t=G(hn,{slot:`previous`,size:`S`,children:G(U,{svg:G(Hn,{})})}),n=G(Wt,{className:`calendar__heading`}),e[0]=t,e[1]=n):(t=e[0],n=e[1]);let r;return e[2]===Symbol.for(`react.memo_cache_sentinel`)?(r=H(`header`,{className:`calendar__header`,children:[t,n,G(hn,{slot:`next`,size:`S`,children:G(U,{svg:G(Xn,{})})})]}),e[2]=r):r=e[2],r}function Hu(e){let t=(0,Z.c)(8),{months:n,errorMessage:r}=e,i;t[0]===Symbol.for(`react.memo_cache_sentinel`)?(i=G(Vu,{}),t[0]=i):i=t[0];let a;t[1]===n?a=t[2]:(a=G(`div`,{className:`calendar__months`,children:Array.from({length:n},Uu)}),t[1]=n,t[2]=a);let o;t[3]===r?o=t[4]:(o=r&&G(Zn,{slot:`errorMessage`,children:r}),t[3]=r,t[4]=o);let s;return t[5]!==a||t[6]!==o?(s=H(W,{children:[i,a,o]}),t[5]=a,t[6]=o,t[7]=s):s=t[7],s}function Uu(e,t){return G(ve,{offset:{months:t},children:Wu},t)}function Wu(e){return G(Ee,{date:e})}var Gu=q`
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
`,Ku=q`
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
`,qu=q`
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
`;function Ju(e){let t=(0,Z.c)(10),n,r,i,a;if(t[0]!==e){let{ref:o,...s}=e;r=o;let{css:c,...l}=s;i=l,n=w,a=q(us,qu,c),t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a}else n=t[1],r=t[2],i=t[3],a=t[4];let o;return t[5]!==n||t[6]!==r||t[7]!==i||t[8]!==a?(o=G(n,{css:a,...i,"data-size":`S`,ref:r}),t[5]=n,t[6]=r,t[7]=i,t[8]=a,t[9]=o):o=t[9],o}function Yu(e){let t=(0,Z.c)(17),n,r,i,a,o;t[0]===e?(n=t[1],r=t[2],i=t[3],a=t[4],o=t[5]):({errorMessage:r,css:i,children:n,ref:a,...o}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a,t[5]=o);let s=e.visibleDuration?.months||1,c;t[6]===i?c=t[7]:(c=q(Gu,Ku,i),t[6]=i,t[7]=c);let l;t[8]!==n||t[9]!==r||t[10]!==s?(l=n??G(Hu,{months:s,errorMessage:r}),t[8]=n,t[9]=r,t[10]=s,t[11]=l):l=t[11];let u;return t[12]!==a||t[13]!==o||t[14]!==c||t[15]!==l?(u=G(F,{ref:a,css:c,...o,children:l}),t[12]=a,t[13]=o,t[14]=c,t[15]=l,t[16]=u):u=t[16],u}q`
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
`;var Xu=q`
  font-family: var(--global-font-family-mono);
  font-variant-numeric: tabular-nums;
  ${Ze};
`;function Zu(e){return e.toString().padStart(2,`0`)}function Qu(e){let t=Math.floor(e/3600),n=Math.floor(e%3600/60),r=e%60;return t>0?`${Zu(t)}:${Zu(n)}:${Zu(r)}`:`${Zu(n)}:${Zu(r)}`}function $u(e){return Math.max(0,Math.floor((Date.now()-e.getTime())/1e3))}function ed(e){let t=(0,Z.c)(18),{startTime:n,color:r,size:i}=e,a=r===void 0?`text-900`:r,o=i===void 0?`S`:i,s;t[0]===n?s=t[1]:(s=n??new Date,t[0]=n,t[1]=s);let c=s,l;t[2]===c?l=t[3]:(l=()=>$u(c),t[2]=c,t[3]=l);let[u,d]=(0,X.useState)(l),f,p;t[4]===c?(f=t[5],p=t[6]):(f=()=>{d($u(c));let e=setInterval(()=>{d($u(c))},1e3);return()=>clearInterval(e)},p=[c],t[4]=c,t[5]=f,t[6]=p),(0,X.useEffect)(f,p);let m;t[7]===a?m=t[8]:(m=Mt(a),t[7]=a,t[8]=m);let h;t[9]===m?h=t[10]:(h={color:m},t[9]=m,t[10]=h);let g=`PT${u}S`,_;t[11]===u?_=t[12]:(_=Qu(u),t[11]=u,t[12]=_);let v;return t[13]!==o||t[14]!==h||t[15]!==g||t[16]!==_?(v=G(`time`,{css:Xu,"data-size":o,style:h,dateTime:g,children:_}),t[13]=o,t[14]=h,t[15]=g,t[16]=_,t[17]=v):v=t[17],v}var td=2e3,nd=q`
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
`,rd=e=>{let t=(0,Z.c)(20),{id:n,size:r,tooltipText:i,variant:a}=e,o=r===void 0?`S`:r,s=i===void 0?`Copy ID`:i,c=a===void 0?`badge`:a,[l,u]=(0,X.useState)(!1),d=l?`success`:`inherit`,f=l?`Checkmark`:`Duplicate`,p;t[0]!==d||t[1]!==f?(p=G(U,{className:`id-badge__copy-icon`,color:d,svgKey:f}),t[0]=d,t[1]=f,t[2]=p):p=t[2];let m=p,h=`${s} ${n}`,g;t[3]===n?g=t[4]:(g=()=>{S(n),u(!0),setTimeout(()=>{u(!1)},td)},t[3]=n,t[4]=g);let _;t[5]!==m||t[6]!==n||t[7]!==o||t[8]!==c?(_=c===`badge`?H(rs,{size:o,children:[G(U,{svgKey:`ID`}),G(V,{fontFamily:`mono`,size:`S`,color:`text-700`,children:n}),m]}):H(W,{children:[G(V,{fontFamily:`mono`,size:`S`,color:`text-500`,children:n}),m]}),t[5]=m,t[6]=n,t[7]=o,t[8]=c,t[9]=_):_=t[9];let v;t[10]!==h||t[11]!==g||t[12]!==_||t[13]!==c?(v=G(Jt,{css:nd,"data-variant":c,"aria-label":h,onPress:g,children:_}),t[10]=h,t[11]=g,t[12]=_,t[13]=c,t[14]=v):v=t[14];let y=l?`Copied`:s,b;t[15]===y?b=t[16]:(b=G(oa,{offset:1,children:y}),t[15]=y,t[16]=b);let x;return t[17]!==v||t[18]!==b?(x=H(Te,{children:[v,b]}),t[17]=v,t[18]=b,t[19]=x):x=t[19],x},id=e=>{let t=(0,Z.c)(7),{title:n,id:r}=e,i;t[0]===n?i=t[1]:(i=G(at,{children:n}),t[0]=n,t[1]=i);let a;t[2]===r?a=t[3]:(a=G(rd,{size:`S`,id:r}),t[2]=r,t[3]=a);let o;return t[4]!==i||t[5]!==a?(o=H(K,{direction:`row`,gap:`size-100`,alignItems:`center`,children:[i,a]}),t[4]=i,t[5]=a,t[6]=o):o=t[6],o},ad=`selectedSpanNodeId`,od=`spanFilterCondition`,sd=`sessionView`,cd=`selectedTraceId`,ld=[cd,ad],ud=`timeRangeKey`,dd=`timeRangeStart`,fd=`timeRangeEnd`,pd=`labelId`,md=`createCodeEvaluator`,hd=`createLlmEvaluator`,gd=[{key:`15m`,label:`Last 15 Min`},{key:`1h`,label:`Last Hour`},{key:`12h`,label:`Last 12 Hours`},{key:`1d`,label:`Last Day`},{key:`7d`,label:`Last 7 Days`},{key:`30d`,label:`Last Month`}],_d=gd.reduce((e,t)=>({...e,[t.key]:t}),{}),vd=6e4,yd=60*vd,bd=24*yd,xd=/^(\d+)([mhd])$/;function Sd(e){if(typeof e!=`string`)return null;let t=xd.exec(e);if(!t)return null;let n=parseInt(t[1],10);return n<1?null:{quantity:n,unit:t[2]}}function Cd({quantity:e,unit:t}){switch(t){case`m`:return e*vd;case`h`:return e*yd;case`d`:return e*bd;default:return dr(t)}}function wd(e,t=Date.now()){let n=Sd(e);if(!n)throw Error(`Invalid last N time range key: ${e}`);let{quantity:r,unit:i}=n,a;switch(i){case`m`:a=Le(t,r);break;case`h`:a=N(t,r);break;case`d`:a=Pe(t,r);break;default:dr(i)}return{start:(Cd(n)<=yd?b:o)(a),end:null}}function Td(e){let t=Sd(e),n=t&&Cd(t)<=yd?vd:yd,r=Date.now()%n;return r===0?n:n-r}function Ed(e){return Sd(e)!==null}function Dd(e){if(e==null||e.trim()===``)return null;let t=new Date(e);return Number.isNaN(t.getTime())?void 0:t}function Od(e,t=Date.now()){let n=e.get(ud);if(Ed(n))return{timeRangeKey:n,...wd(n,t)};let r=Dd(e.get(dd)),i=Dd(e.get(fd));return r===void 0||i===void 0||r==null&&i==null||r!=null&&i!=null&&r>i?null:{timeRangeKey:`custom`,start:r,end:i}}function kd({searchParams:e,timeRange:t}){let n=new URLSearchParams(e),r=(e,t)=>{t==null?n.delete(e):n.set(e,t.toISOString())};return Ed(t.timeRangeKey)?(n.set(ud,t.timeRangeKey),n.delete(dd),n.delete(fd),n):(n.delete(ud),r(dd,t.start),r(fd,t.end),n)}function Ad(e){let t=kd({searchParams:new URLSearchParams,timeRange:e}).toString();return t?`?${t}`:``}var jd={m:{singular:`minute`,plural:`minutes`},h:{singular:`hour`,plural:`hours`},d:{singular:`day`,plural:`days`}};function Md(e){let t=_d[e];if(t)return t.label;let n=Sd(e);if(!n)return e;let{quantity:r,unit:i}=n,{singular:a,plural:o}=jd[i];return`Last ${r} ${r===1?a:o}`}var Nd=/^(?:last\s+)?(\d+)\s*(m|min|mins|minute|minutes|h|hr|hrs|hour|hours|d|day|days)$/,Pd=/^(?:last\s+)?(\d+)$/;function Fd(e){let t=Nd.exec(e.trim().toLowerCase());if(!t)return null;let n=parseInt(t[1],10);return n<1?null:`${n}${t[2][0]}`}function Id(e){let t=Fd(e);if(t)return[t];let n=Pd.exec(e.trim().toLowerCase());if(!n)return[];let r=parseInt(n[1],10);return r<1?[]:[`${r}m`,`${r}h`,`${r}d`]}var Ld=.5,Rd=2,zd=vd;function Bd({value:e,now:t}){if(!e.start)return null;let n=e.start.getTime(),r=(e.end??t).getTime(),i=r-n;return i<=0?null:{startMs:n,endMs:r,durationMs:i}}function Vd(e){let t=Math.max(1,Math.round(e/vd)),n=t/1440;if(n>=2||Number.isInteger(n))return`${Math.round(n)}d`;let r=t/60;return r>=2||Number.isInteger(r)?`${Math.round(r)}h`:`${t}m`}function Hd({value:e,now:t=new Date,shiftFraction:n=Ld}){let r=Bd({value:e,now:t});if(!r)return null;let i=r.durationMs*n;return{timeRangeKey:`custom`,start:new Date(r.startMs-i),end:new Date(r.endMs-i)}}function Ud({value:e,now:t=new Date,shiftFraction:n=Ld}){if(!e.end)return null;let r=Bd({value:e,now:t});if(!r)return null;let i=Math.min(r.durationMs*n,t.getTime()-r.endMs);return i<=0?null:{timeRangeKey:`custom`,start:new Date(r.startMs+i),end:new Date(r.endMs+i)}}function Wd({value:e,now:t=new Date,zoomFactor:n=Rd,minWindowMs:r=zd}){return Kd({value:e,now:t,factor:1/n,minWindowMs:r})}function Gd({value:e,now:t=new Date,zoomFactor:n=Rd,minWindowMs:r=zd}){return Kd({value:e,now:t,factor:n,minWindowMs:r})}function Kd({value:e,now:t,factor:n,minWindowMs:r}){if(!e.end){let i=Sd(e.timeRangeKey),a=i?Cd(i):Bd({value:e,now:t})?.durationMs;if(a==null)return null;let o=Math.max(a*n,r);if(n<1&&o>=a)return null;let s=Vd(o);return s===e.timeRangeKey?null:{timeRangeKey:s,...wd(s)}}let i=Bd({value:e,now:t});if(!i)return null;let a=Math.max(i.durationMs*n,r);if(n<1?a>=i.durationMs:a===i.durationMs)return null;let o=(i.startMs+i.endMs)/2,s=o-a/2,c=o+a/2,l=c-t.getTime();return l>0&&(s-=l,c-=l),{timeRangeKey:`custom`,start:new Date(s),end:new Date(c)}}function qd(e,t){return e?he(e,t):null}var Jd=q`
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
`,Yd=q`
  .react-aria-DateInput {
    width: 100%;
    min-width: 0;
  }
`,Xd=new pe(0,0,0),Zd=new pe(23,59,59);function Qd(e){let t=(0,Z.c)(56),{value:n,timeZone:r,onApply:a,onCancel:o}=e,s;t[0]!==r||t[1]!==n.start?(s=()=>qd(n.start,r),t[0]=r,t[1]=n.start,t[2]=s):s=t[2];let[c,l]=(0,X.useState)(s),u;t[3]!==r||t[4]!==n.end?(u=()=>qd(n.end,r)??oe(r),t[3]=r,t[4]=n.end,t[5]=u):u=t[5];let[d,f]=(0,X.useState)(u),p;t[6]!==c||t[7]!==r?(p=c?c.toDate(r):null,t[6]=c,t[7]=r,t[8]=p):p=t[8];let m=p,h;t[9]!==d||t[10]!==r?(h=d?d.toDate(r):null,t[9]=d,t[10]=r,t[11]=h):h=t[11];let g=h,_=!!(m&&g&&m>g),v;t[12]!==g||t[13]!==_||t[14]!==m?(v=m&&g&&!_?{start:m,end:g}:null,t[12]=g,t[13]=_,t[14]=m,t[15]=v):v=t[15];let y=v,b;t[16]!==d||t[17]!==_||t[18]!==c?(b=c&&d&&!_?{start:ne(c),end:ne(d)}:null,t[16]=d,t[17]=_,t[18]=c,t[19]=b):b=t[19];let x=b,S;t[20]===Symbol.for(`react.memo_cache_sentinel`)?(S={months:2},t[20]=S):S=t[20];let C;t[21]===r?C=t[22]:(C=e=>{e&&(l(L(xe(e.start,Xd),r)),f(L(xe(e.end,Zd),r)))},t[21]=r,t[22]=C);let w;t[23]!==x||t[24]!==C?(w=G(Yu,{"aria-label":`Time range`,visibleDuration:S,value:x,onChange:C}),t[23]=x,t[24]=C,t[25]=w):w=t[25];let T,E;t[26]===Symbol.for(`react.memo_cache_sentinel`)?(E=G(On,{children:`Start`}),T=G(i,{children:ef}),t[26]=T,t[27]=E):(T=t[26],E=t[27]);let D;t[28]===c?D=t[29]:(D=H(Ju,{granularity:`minute`,hideTimeZone:!0,value:c,onChange:l,css:Yd,children:[E,T]}),t[28]=c,t[29]=D);let O,k;t[30]===Symbol.for(`react.memo_cache_sentinel`)?(O=G(On,{children:`End`}),k=G(i,{children:$d}),t[30]=O,t[31]=k):(O=t[30],k=t[31]);let A;t[32]!==d||t[33]!==_?(A=H(Ju,{granularity:`minute`,hideTimeZone:!0,isInvalid:_,value:d,onChange:f,css:Yd,children:[O,k]}),t[32]=d,t[33]=_,t[34]=A):A=t[34];let j;t[35]!==D||t[36]!==A?(j=H(`div`,{className:`time-range-calendar-picker__fields`,children:[D,A]}),t[35]=D,t[36]=A,t[37]=j):j=t[37];let M;t[38]===_?M=t[39]:(M=_&&G(V,{size:`XS`,color:`danger`,className:`time-range-calendar-picker__error`,children:`End must be after the start`}),t[38]=_,t[39]=M);let N;t[40]===o?N=t[41]:(N=G(Nt,{size:`S`,onPress:o,children:`Cancel`}),t[40]=o,t[41]=N);let P=!y,F;t[42]!==y||t[43]!==a?(F=()=>{y&&a(y)},t[42]=y,t[43]=a,t[44]=F):F=t[44];let I;t[45]!==P||t[46]!==F?(I=G(Nt,{"data-testid":`time-range-calendar-picker-apply-button`,size:`S`,variant:`primary`,isDisabled:P,onPress:F,children:`Apply`}),t[45]=P,t[46]=F,t[47]=I):I=t[47];let R;t[48]!==M||t[49]!==N||t[50]!==I?(R=H(`div`,{className:`time-range-calendar-picker__controls`,children:[M,N,I]}),t[48]=M,t[49]=N,t[50]=I,t[51]=R):R=t[51];let ee;return t[52]!==j||t[53]!==R||t[54]!==w?(ee=H(`div`,{"data-testid":`time-range-calendar-picker`,className:`time-range-calendar-picker`,css:Jd,children:[w,j,R]}),t[52]=j,t[53]=R,t[54]=w,t[55]=ee):ee=t[55],ee}function $d(e){return G(ze,{segment:e})}function ef(e){return G(ze,{segment:e})}var tf=`set_time_range`,nf=[`15m`,`1h`,`12h`,`1d`,`7d`,`30d`,`custom`];function rf(e){return typeof e==`string`&&nf.includes(e)}function af(e){if(typeof e!=`object`||!e)return null;let t=e;return!rf(t.timeRangeKey)||t.startTime!==void 0&&typeof t.startTime!=`string`||t.endTime!==void 0&&typeof t.endTime!=`string`?null:{timeRangeKey:t.timeRangeKey,...t.startTime===void 0?{}:{startTime:t.startTime},...t.endTime===void 0?{}:{endTime:t.endTime}}}function of(e,t){return typeof e==`function`?e(t):e}function sf(e){return{name:e.name,uiBehavior:e.uiBehavior,requiredCapabilities:e.requiredCapabilities,dispatch:async t=>{let n=e.parseInput(t.toolCall.input);if(n==null){await t.addToolOutput({state:`output-error`,tool:e.name,toolCallId:t.toolCall.toolCallId,errorText:of(e.invalidInputErrorText,t.toolCall.input)});return}await e.execute({...t,input:n})}}}async function cf({toolName:e,toolCall:t,sessionId:n,addToolOutput:r,errorText:i}){return n??(await r({state:`output-error`,tool:e,toolCallId:t.toolCallId,errorText:i}),null)}async function lf({result:e,toolName:t,toolCallId:n,addToolOutput:r,defaultSuccessOutput:i,emitSuccess:a}){if(e.ok){if(!a)return;await r({state:`output-available`,tool:t,toolCallId:n,output:e.output??i});return}await r({state:`output-error`,tool:t,toolCallId:n,errorText:e.error})}function uf(e){let t=e.emitSuccess??!0,n=e.defaultSuccessOutput??`Done.`;return sf({name:e.name,parseInput:e.parseInput,invalidInputErrorText:e.invalidInputErrorText,requiredCapabilities:e.requiredCapabilities,uiBehavior:e.uiBehavior,execute:async({toolCall:r,input:i,sessionId:a,addToolOutput:o,agentStore:s})=>{let c=s.getState().registeredClientActions[e.name];if(!c){await o({state:`output-error`,tool:e.name,toolCallId:r.toolCallId,errorText:e.notMountedErrorText});return}e.requireSession&&await cf({toolName:e.name,toolCall:r,sessionId:a,addToolOutput:o,errorText:e.noSessionErrorText??`Cannot run this tool without an active session.`})==null||await lf({result:e.buildContext?await c(i,e.buildContext({toolCall:r,sessionId:a,addToolOutput:o,agentStore:s})):await c(i),toolName:e.name,toolCallId:r.toolCallId,addToolOutput:o,defaultSuccessOutput:n,emitSuccess:t})}})}var df=uf({name:tf,parseInput:af,invalidInputErrorText:`Invalid ${tf} input. Expected { timeRangeKey: ${nf.map(e=>`"${e}"`).join(` | `)}, startTime?: string, endTime?: string }.`,notMountedErrorText:`The app time range selector is not mounted on this page; cannot update the time range.`,defaultSuccessOutput:`Time range updated.`});function ff(e){switch(e.type){case`app`:return`app`;case`playground`:return`playground`;case`code_evaluator`:return e.evaluatorNodeId?`code_evaluator:${e.evaluatorNodeId}`:`code_evaluator:create`;case`llm_evaluator`:return e.evaluatorNodeId?`llm_evaluator:${e.evaluatorNodeId}`:`llm_evaluator:create`;case`dataset`:return e.datasetVersionNodeId?`dataset:${e.datasetNodeId}:${e.datasetVersionNodeId}`:`dataset:${e.datasetNodeId}`;case`project`:return`project:${e.projectNodeId}`;case`trace`:return`trace:${e.projectNodeId}:${e.otelTraceId}`;case`session`:return`session:${e.projectNodeId}:${e.sessionNodeId}`;case`prompt`:return`prompt:${e.promptNodeId}`;case`prompt_version`:return`prompt_version:${e.promptNodeId}:${e.promptVersionNodeId}`;case`span`:return`span:${e.projectNodeId??``}:${e.spanNodeId?`node:${e.spanNodeId}`:`otel:${e.otelSpanId}`}`;case`graphql`:return`graphql`;case`web_access`:return`web_access`;case`subagents`:return`subagents`;default:return dr(e)}}var pf={"bash.retainInactiveSessions":!1,"graphql.mutations":!1,"session.storeSessions":!1,"subagents.enabled":!1,"web.access":!1},mf=[{key:`bash.retainInactiveSessions`,label:`Retain inactive bash sessions`,description:`Keeps browser bash runtimes alive when switching sessions instead of eagerly garbage-collecting them.`,defaultValue:!1,scope:`global`,controlSurface:`experimental-settings`},{key:`graphql.mutations`,label:`Dangerously enable mutations`,description:`Allows the phoenix-gql bash command to execute GraphQL mutations in addition to queries.`,defaultValue:!1,scope:`global`,controlSurface:`experimental-settings`},{key:`session.storeSessions`,label:`Store recent sessions`,description:`Keeps the three most recent chat sessions instead of replacing session history when starting a new chat.`,defaultValue:!1,scope:`global`,controlSurface:`experimental-settings`},{key:`subagents.enabled`,label:`Subagents`,description:`Lets the assistant delegate work to subagents that run their own tool-using turns. Experimental and may consume large numbers of tokens.`,defaultValue:!1,scope:`global`},{key:`web.access`,label:`Web search`,description:`Lets the assistant use provider-native web search and URL fetching when the selected model supports it.`,defaultValue:!1,scope:`global`}],hf=Object.fromEntries(mf.map(e=>[e.key,e]));for(let e of Object.keys(pf))if(!hf[e])throw Error(`Missing AGENT_CAPABILITY_DEFINITIONS entry for capability key: "${e}"`);function gf(){return{...pf}}function _f(e){return hf[e]}function vf(e){return mf.filter(t=>t.controlSurface===e)}function yf(e){return e.map(e=>e.toLowerCase())}var bf=[`NONE`,`MINIMAL`,`LOW`,`MEDIUM`,`HIGH`,`XHIGH`],xf=yf(bf),Sf=Object.fromEntries(bf.map(e=>[e,e.toLowerCase()]));function Cf(e){return e in Sf}function wf(e){if(typeof e!=`string`)return;let t=e.trim();if(!t)return;let n=t.toUpperCase();if(Cf(n))return n}function Tf(e){let t=wf(e);if(t!=null)return Sf[t]}var Ef=[`disabled`,`enabled`,`adaptive`],Df=[`SUMMARIZED`,`OMITTED`],Of=yf(Df),kf=[`LOW`,`MEDIUM`,`HIGH`,`XHIGH`,`MAX`],Af=yf(kf),jf=[`MINIMAL`,`LOW`,`MEDIUM`,`HIGH`],Mf=yf(jf),Nf={OPENAI:`openai`,ANTHROPIC:`anthropic`,GOOGLE_GENAI:`google_genai`,AWS_BEDROCK:`aws_bedrock`};function Pf(e){switch(e){case`OPENAI`:case`AZURE_OPENAI`:case`DEEPSEEK`:case`XAI`:case`OLLAMA`:case`CEREBRAS`:case`FIREWORKS`:case`GROQ`:case`MOONSHOT`:case`PERPLEXITY`:case`TOGETHER`:return Nf.OPENAI;case`ANTHROPIC`:return Nf.ANTHROPIC;case`GOOGLE`:return Nf.GOOGLE_GENAI;case`AWS`:return Nf.AWS_BEDROCK}return dr(e)}var Ff=[{name:`temperature`,type:`float`,min:0,max:2,label:`Temperature`,canonicalName:`TEMPERATURE`},{name:`topP`,type:`float`,min:0,max:1,label:`Top P`,canonicalName:`TOP_P`},{name:`maxCompletionTokens`,type:`int`,label:`Max Completion Tokens`,canonicalName:`MAX_COMPLETION_TOKENS`},{name:`frequencyPenalty`,type:`float`,min:-2,max:2,label:`Frequency Penalty`,applicableOpenAIApiTypes:[`CHAT_COMPLETIONS`]},{name:`presencePenalty`,type:`float`,min:-2,max:2,label:`Presence Penalty`,applicableOpenAIApiTypes:[`CHAT_COMPLETIONS`]},{name:`reasoningEffort`,type:`enum`,values:xf,label:`Reasoning Effort`,canonicalName:`REASONING_EFFORT`},{name:`seed`,type:`int`,label:`Seed`,canonicalName:`RANDOM_SEED`}],If=[{name:`maxTokens`,type:`int`,label:`Max Tokens`,required:!0,canonicalName:`MAX_COMPLETION_TOKENS`},{name:`temperature`,type:`float`,min:0,max:1,label:`Temperature`,canonicalName:`TEMPERATURE`},{name:`stopSequences`,type:`string_list`,label:`Stop Sequences`,canonicalName:`STOP_SEQUENCES`},{name:`topP`,type:`float`,min:0,max:1,label:`Top P`,canonicalName:`TOP_P`},{name:`thinkingType`,type:`enum`,values:Ef,label:`Thinking`,canonicalName:`ANTHROPIC_EXTENDED_THINKING`},{name:`thinkingBudgetTokens`,type:`int`,min:1024,label:`Budget Tokens`},{name:`thinkingDisplay`,type:`enum`,values:Of,label:`Thinking Display`},{name:`effort`,type:`enum`,values:Af,label:`Effort`,canonicalName:`REASONING_EFFORT`}],Lf=[{name:`temperature`,type:`float`,min:0,max:2,label:`Temperature`,canonicalName:`TEMPERATURE`},{name:`maxOutputTokens`,type:`int`,label:`Max Output Tokens`,canonicalName:`MAX_COMPLETION_TOKENS`},{name:`stopSequences`,type:`string_list`,label:`Stop Sequences`,canonicalName:`STOP_SEQUENCES`},{name:`presencePenalty`,type:`float`,label:`Presence Penalty`},{name:`frequencyPenalty`,type:`float`,label:`Frequency Penalty`},{name:`topP`,type:`float`,min:0,max:1,label:`Top P`,canonicalName:`TOP_P`},{name:`topK`,type:`int`,label:`Top K`},{name:`thinkingBudget`,type:`int`,min:0,label:`Thinking Budget`},{name:`thinkingLevel`,type:`enum`,values:Mf,label:`Thinking Level`},{name:`includeThoughts`,type:`bool`,label:`Include Thoughts`}],Rf=[{name:`maxTokens`,type:`int`,label:`Max Tokens`,canonicalName:`MAX_COMPLETION_TOKENS`},{name:`temperature`,type:`float`,min:0,max:1,label:`Temperature`,canonicalName:`TEMPERATURE`},{name:`topP`,type:`float`,min:0,max:1,label:`Top P`,canonicalName:`TOP_P`}];Nf.OPENAI,Nf.ANTHROPIC,Nf.GOOGLE_GENAI,Nf.AWS_BEDROCK;var zf=1024,Bf=2e3,Vf={type:`adaptive`,display:`SUMMARIZED`},Hf=`HIGH`,Uf=J().transform(e=>e.toUpperCase()).pipe(tr(Df)).optional().catch(void 0),Wf=J().transform(e=>e.toUpperCase()).pipe(tr(kf)).optional().catch(void 0),Gf=$n(J()).optional().catch(void 0),Kf=or(J(),ir()).optional().catch(void 0),qf=ar(`type`,[lr({type:nr(`disabled`)}),lr({type:nr(`enabled`),budgetTokens:Y(),display:Uf}),lr({type:nr(`adaptive`),display:Uf})]).optional().catch(void 0),Jf=ar(`type`,[lr({type:nr(`disabled`)}),lr({type:nr(`enabled`),budget_tokens:Y(),display:Uf}),lr({type:nr(`adaptive`),display:Uf})]).optional().catch(void 0);function Yf(e){if(e)switch(e.type){case`disabled`:return{type:`disabled`};case`enabled`:{let t={type:`enabled`,budgetTokens:e.budget_tokens};return e.display!==void 0&&(t.display=e.display),t}case`adaptive`:{let t={type:`adaptive`};return e.display!==void 0&&(t.display=e.display),t}default:return dr(e)}}function Xf(e){return e?.type===`enabled`||e?.type===`adaptive`}function Zf(){return{maxTokens:Bf,thinking:Vf,effort:Hf}}function Qf(e){if(e==null)return If;let t=Xf(e.thinking);return If.flatMap(n=>{let r=`canonicalName`in n?n.canonicalName:null;return t&&(r===`TEMPERATURE`||r===`TOP_P`)?[]:n.name===`thinkingBudgetTokens`?e.thinking?.type===`enabled`?n.type===`int`?[{...n,max:e.maxTokens-1}]:[n]:[]:n.name===`thinkingDisplay`&&!t?[]:[n]})}var $f=er({maxTokens:Y().optional().catch(void 0),temperature:Y().optional().catch(void 0),topP:Y().optional().catch(void 0),stopSequences:Gf,thinking:qf,effort:Wf,extraBody:Kf});function ep(e){let t=$f.safeParse(e),n=t.success?t.data:{},r={maxTokens:n.maxTokens??2e3};return n.temperature!==void 0&&(r.temperature=n.temperature),n.topP!==void 0&&(r.topP=n.topP),n.stopSequences!==void 0&&(r.stopSequences=[...n.stopSequences]),n.thinking!==void 0&&(r.thinking=n.thinking),n.effort!==void 0&&(r.effort=n.effort),n.extraBody!==void 0&&(r.extraBody={...n.extraBody}),r}function Q(e){if(!Xf(e.thinking)||e.temperature===void 0&&e.topP===void 0)return e;let t={...e};return delete t.temperature,delete t.topP,t}function tp(e){let t=[];if(e.thinking?.type===`enabled`){let n=e.thinking.budgetTokens;n<1024&&t.push(`Thinking budget must be at least ${zf} (got ${n})`),n>=e.maxTokens&&t.push(`Thinking budget (${n}) must be less than max tokens (${e.maxTokens})`)}return t}function np(e){switch(e.type){case`disabled`:return{disabled:{disabled:!0}};case`enabled`:return{enabled:{budgetTokens:e.budgetTokens,display:e.display??null}};case`adaptive`:return{adaptive:{display:e.display??null}};default:return dr(e)}}function rp(e){let t=Q(e),n=tp(t);if(n.length>0)throw Error(`Cannot serialize Anthropic invocation parameters: ${n.join(`; `)}`);let r={maxTokens:t.maxTokens};return t.temperature!==void 0&&(r.temperature=t.temperature),t.topP!==void 0&&(r.topP=t.topP),t.stopSequences!==void 0&&(r.stopSequences=t.stopSequences),t.thinking!==void 0&&(r.thinking=np(t.thinking)),t.effort!==void 0&&(r.outputConfig={effort:t.effort}),t.extraBody!==void 0&&(r.extraBody=t.extraBody),{anthropic:r}}function ip(e){if(e.__typename!==`PromptAnthropicInvocationParameters`)throw Error(`anthropicAdapter.fromPromptInvocationParameters called with non-Anthropic typename: ${e.__typename}`);let t={maxTokens:e.anthropicMaxTokens};if(e.temperature!=null&&(t.temperature=e.temperature),e.topP!=null&&(t.topP=e.topP),e.stopSequences!=null&&(t.stopSequences=[...e.stopSequences]),e.outputConfig?.effort!=null&&(t.effort=e.outputConfig.effort),e.thinking)switch(e.thinking.__typename){case`PromptAnthropicThinkingDisabled`:t.thinking={type:`disabled`};break;case`PromptAnthropicThinkingEnabled`:{let n={type:`enabled`,budgetTokens:e.thinking.budgetTokens};e.thinking.enabledDisplay!=null&&(n.display=e.thinking.enabledDisplay),t.thinking=n;break}case`PromptAnthropicThinkingAdaptive`:{let n={type:`adaptive`};e.thinking.adaptiveDisplay!=null&&(n.display=e.thinking.adaptiveDisplay),t.thinking=n;break}case`%other`:break;default:dr(e.thinking)}let n=dp(e.extraBody);return n!=null&&(t.extraBody=n),Q(t)}function ap(e){if(e.__typename!==`PromptAnthropicInvocationParameters`)throw Error(`anthropicAdapter.fromPromptInvocationParametersForDisplay called with non-Anthropic typename: ${e.__typename}`);let t={maxTokens:e.anthropicMaxTokens};if(e.temperature!=null&&(t.temperature=e.temperature),e.topP!=null&&(t.topP=e.topP),e.stopSequences!=null&&(t.stopSequences=[...e.stopSequences]),e.outputConfig?.effort!=null&&(t.outputConfig={effort:e.outputConfig.effort}),e.thinking)switch(e.thinking.__typename){case`PromptAnthropicThinkingDisabled`:t.thinking={type:`disabled`};break;case`PromptAnthropicThinkingEnabled`:{let n={type:`enabled`,budgetTokens:e.thinking.budgetTokens};e.thinking.enabledDisplay!=null&&(n.display=e.thinking.enabledDisplay),t.thinking=n;break}case`PromptAnthropicThinkingAdaptive`:{let n={type:`adaptive`};e.thinking.adaptiveDisplay!=null&&(n.display=e.thinking.adaptiveDisplay),t.thinking=n;break}case`%other`:break;default:dr(e.thinking)}let n=dp(e.extraBody);return n!=null&&(t.extraBody=n),t}var op=er({effort:Wf,format:lr({type:nr(`json_schema`),schema:or(J(),ir())}).optional().catch(void 0)}).optional().catch(void 0),sp=er({max_tokens:Y().optional().catch(void 0),temperature:Y().optional().catch(void 0),top_p:Y().optional().catch(void 0),stop_sequences:Gf,thinking:Jf,output_config:op,extra_body:Kf});function cp(e){let t=sp.safeParse(e),n=t.success?t.data:{},r={maxTokens:n.max_tokens??2e3};n.temperature!==void 0&&(r.temperature=n.temperature),n.top_p!==void 0&&(r.topP=n.top_p),n.stop_sequences!==void 0&&(r.stopSequences=[...n.stop_sequences]);let i=Yf(n.thinking);if(i!==void 0&&(r.thinking=i),n.output_config?.effort!==void 0&&(r.effort=n.output_config.effort),n.extra_body!==void 0){let e=dp(n.extra_body);e!==void 0&&(r.extraBody=e)}let a={},o=n.output_config?.format;return o&&(a.responseFormat={type:`json_schema`,jsonSchema:{name:`response`,schema:o.schema}}),{config:Q(r),promoted:a}}function lp(e,t){switch(t){case`maxTokens`:return e.maxTokens;case`temperature`:return e.temperature;case`topP`:return e.topP;case`stopSequences`:return e.stopSequences;case`thinkingType`:return e.thinking?.type;case`thinkingBudgetTokens`:return e.thinking?.type===`enabled`?e.thinking.budgetTokens:void 0;case`thinkingDisplay`:return e.thinking&&e.thinking.type!==`disabled`?e.thinking.display?.toLowerCase():void 0;case`effort`:return e.effort?.toLowerCase();case`extraBody`:return e.extraBody;default:return}}function up(e,t,n){switch(t){case`maxTokens`:return typeof n!=`number`||Number.isNaN(n)?e:Q({...e,maxTokens:n});case`temperature`:if(n===void 0){let t={...e};return delete t.temperature,Q(t)}return typeof n!=`number`||Number.isNaN(n)?e:Q({...e,temperature:n});case`topP`:if(n===void 0){let t={...e};return delete t.topP,Q(t)}return typeof n!=`number`||Number.isNaN(n)?e:Q({...e,topP:n});case`stopSequences`:if(n===void 0){let t={...e};return delete t.stopSequences,Q(t)}return Array.isArray(n)?Q({...e,stopSequences:n.map(String)}):e;case`thinkingType`:if(n===void 0){let t={...e};return delete t.thinking,Q(t)}if(n===`disabled`)return Q({...e,thinking:{type:`disabled`}});if(n===`enabled`){let t=e.thinking,n=t?.type===`enabled`?t.budgetTokens:zf,r=t&&t.type!==`disabled`?t.display:void 0,i={type:`enabled`,budgetTokens:n};r!==void 0&&(i.display=r);let a=e.maxTokens>n?e.maxTokens:n+1;return Q({...e,maxTokens:a,thinking:i})}if(n===`adaptive`){let t=e.thinking,n=t&&t.type!==`disabled`?t.display:void 0,r={type:`adaptive`};return n!==void 0&&(r.display=n),Q({...e,thinking:r})}return e;case`thinkingBudgetTokens`:return e.thinking?.type!==`enabled`||n===void 0||typeof n!=`number`||Number.isNaN(n)?e:Q({...e,thinking:{...e.thinking,budgetTokens:n}});case`thinkingDisplay`:{let t=e.thinking;if(!t||t.type===`disabled`)return e;if(n===void 0){if(t.type===`enabled`){let n={type:`enabled`,budgetTokens:t.budgetTokens};return Q({...e,thinking:n})}return Q({...e,thinking:{type:`adaptive`}})}let r=Uf.safeParse(n);return!r.success||!r.data?e:t.type===`enabled`?Q({...e,thinking:{type:`enabled`,budgetTokens:t.budgetTokens,display:r.data}}):Q({...e,thinking:{type:`adaptive`,display:r.data}})}case`effort`:{if(n===void 0){let t={...e};return delete t.effort,Q(t)}let t=Wf.safeParse(n);return!t.success||!t.data?e:Q({...e,effort:t.data})}case`extraBody`:{if(n===void 0){let t={...e};return delete t.extraBody,Q(t)}let t=dp(n);return t===void 0?e:Q({...e,extraBody:t})}default:return e}}function dp(e){if(typeof e==`object`&&e&&!Array.isArray(e))return e}var fp={getDefaultConfig:Zf,getVisibleSpecs:Qf,parseConfig:ep,normalize:Q,validateForSubmit:tp,toPromptInput:rp,fromPromptInvocationParameters:ip,fromPromptInvocationParametersForDisplay:ap,fromSpanInvocationParameters:cp,readField:lp,writeField:up};function pp(e){return _r(e)&&!Array.isArray(e)}function mp({str:e,excludePrimitives:t=!1,excludeArray:n=!1,excludeNull:r=!1}){try{let i=JSON.parse(e);if(t&&typeof i!=`object`||n&&Array.isArray(i)||r&&i===null)return!1}catch{return!1}return!0}function hp(e){return mp({str:e,excludeArray:!0,excludePrimitives:!0})}function gp(e){try{return{json:JSON.parse(e)}}catch(e){return{json:null,parseError:e}}}function _p(...e){try{return{json:JSON.stringify(...e)}}catch(e){return{json:null,stringifyError:e}}}function vp(e){if(typeof e==`string`){let t=Ap(e);return t===void 0?e:vp(t)}return Array.isArray(e)?e.map(vp):typeof e==`object`&&e?Object.fromEntries(Object.entries(e).map(([e,t])=>[e,vp(t)])):e}function yp(e){return typeof e==`string`?Ap(e)!==void 0:Array.isArray(e)?e.some(yp):typeof e==`object`&&e?Object.values(e).some(yp):!1}var bp=`.`;function xp({parentKey:e,index:t,indexNotation:n}){return n===`bracket`?`${e}[${t}]`:e?`${e}${bp}${t}`:String(t)}function Sp({value:e,indexNotation:t=`bracket`,parentKey:n=``}){return Array.isArray(e)&&e.length>0?e.flatMap((e,r)=>Sp({value:e,indexNotation:t,parentKey:xp({parentKey:n,index:r,indexNotation:t})})):pp(e)&&Object.keys(e).length>0?Object.entries(e).flatMap(([e,r])=>Sp({value:r,indexNotation:t,parentKey:n?`${n}${bp}${e}`:e})):n===``?[]:[{key:n,value:e}]}function Cp(e){return typeof e==`string`?e:_p(e).json??String(e)}function wp({entries:e,query:t}){let n=t.trim().toLowerCase();return n?e.filter(({key:e,value:t})=>e.toLowerCase().includes(n)||Cp(t).toLowerCase().includes(n)):e}function Tp({obj:e,parentKey:t=``,separator:n=`.`,keepNonTerminalValues:r=!1,formatIndices:i=!1}){let a={};for(let[o,s]of Object.entries(e)){let c;c=i&&Array.isArray(e)?t?`${t}[${o}]`:`[${o}]`:t?`${t}${n}${o}`:o,s&&typeof s==`object`?(r&&(a[c]=s),Object.assign(a,Tp({obj:s,parentKey:c,separator:n,keepNonTerminalValues:r,formatIndices:i}))):a[c]=s}return a}function Ep(e,t=`.`){try{let n=JSON.parse(e);return typeof n==`object`?Tp({obj:n,separator:t}):{}}catch{}return{}}function Dp(e,t){let n=t?.unquotePlainString??!1;if(typeof e==`string`){let t=e.startsWith(`"{`)||e.startsWith(`"[`)||e.startsWith(`"\\"`);try{if(t){let t=JSON.parse(e),n=typeof t==`string`?JSON.parse(t):t;return JSON.stringify(n,null,2)}}catch{}return n?e:JSON.stringify(e)}try{let t=JSON.stringify(e,null,2);if(t!==void 0)return t}catch{}return String(e)}function Op(e){if(e!=null)try{return JSON.stringify(e)}catch{return}}function kp(e){if(e.trim())try{return JSON.parse(e)}catch{return}}function Ap(e){let t=kp(e);if(!(typeof t!=`object`||!t))return t}function jp(e){if(e==null)return``;if(Array.isArray(e))return e.length>0?e.map(jp):[];if(typeof e==`object`){let t={};for(let n in e)t[n]=jp(e[n]);return t}return typeof e==`string`?``:typeof e==`number`||typeof e==`boolean`?e:``}function Mp(e){try{let t=jp(JSON.parse(e));return JSON.stringify(t,null,2)}catch{return`{
  
}`}}function Np(e){if(!_r(e))return{value:e,wasUnnested:!1};let t=Object.keys(e);if(t.length!==1)return{value:e,wasUnnested:!1};let n=e[t[0]];return typeof n==`string`?{value:n,wasUnnested:!0}:{value:e,wasUnnested:!1}}function Pp(){return{maxTokens:1024,temperature:1}}function Fp(){return Rf}var Ip=er({maxTokens:Y().optional().catch(void 0),temperature:Y().optional().catch(void 0),topP:Y().optional().catch(void 0),stopSequences:$n(J()).optional().catch(void 0)});function Lp(e){let t=Ip.safeParse(e),n=t.success?t.data:{},r={};return n.maxTokens!==void 0&&(r.maxTokens=n.maxTokens),n.temperature!==void 0&&(r.temperature=n.temperature),n.topP!==void 0&&(r.topP=n.topP),n.stopSequences!==void 0&&(r.stopSequences=[...n.stopSequences]),r}function Rp(e){return e}function zp(e){return[]}function Bp(e){let t=Rp(e),n={};return t.maxTokens!==void 0&&(n.maxTokens=t.maxTokens),t.temperature!==void 0&&(n.temperature=t.temperature),t.topP!==void 0&&(n.topP=t.topP),t.stopSequences!==void 0&&(n.stopSequences=t.stopSequences),{aws:n}}function Vp(e){if(e.__typename!==`PromptAwsInvocationParameters`)throw Error(`awsAdapter.fromPromptInvocationParameters called with non-AWS typename: ${e.__typename}`);let t={};return e.awsMaxTokens!=null&&(t.maxTokens=e.awsMaxTokens),e.temperature!=null&&(t.temperature=e.temperature),e.topP!=null&&(t.topP=e.topP),e.stopSequences!=null&&(t.stopSequences=[...e.stopSequences]),Rp(t)}function Hp(e){if(e.__typename!==`PromptAwsInvocationParameters`)throw Error(`awsAdapter.fromPromptInvocationParametersForDisplay called with non-AWS typename: ${e.__typename}`);let t={};return e.awsMaxTokens!=null&&(t.maxTokens=e.awsMaxTokens),e.temperature!=null&&(t.temperature=e.temperature),e.topP!=null&&(t.topP=e.topP),e.stopSequences!=null&&(t.stopSequences=[...e.stopSequences]),t}var Up=lr({maxTokens:Y().optional().catch(void 0),temperature:Y().optional().catch(void 0),topP:Y().optional().catch(void 0),stopSequences:$n(J()).optional().catch(void 0)}).optional().catch(void 0),Wp=lr({schema:cr([J(),or(J(),ir())]).optional(),name:J().optional(),description:J().optional()}).optional().catch(void 0),Gp=lr({textFormat:lr({structure:lr({jsonSchema:Wp}).optional().catch(void 0)}).optional().catch(void 0)}).optional().catch(void 0),Kp=er({maxTokens:Y().optional().catch(void 0),temperature:Y().optional().catch(void 0),topP:Y().optional().catch(void 0),stopSequences:$n(J()).optional().catch(void 0),inferenceConfig:Up,outputConfig:Gp});function qp(e){let t=Kp.safeParse(e),n=t.success?t.data:{},r={};n.maxTokens===void 0?n.inferenceConfig?.maxTokens!==void 0&&(r.maxTokens=n.inferenceConfig.maxTokens):r.maxTokens=n.maxTokens,n.temperature===void 0?n.inferenceConfig?.temperature!==void 0&&(r.temperature=n.inferenceConfig.temperature):r.temperature=n.temperature,n.topP===void 0?n.inferenceConfig?.topP!==void 0&&(r.topP=n.inferenceConfig.topP):r.topP=n.topP,n.stopSequences===void 0?n.inferenceConfig?.stopSequences!==void 0&&(r.stopSequences=[...n.inferenceConfig.stopSequences]):r.stopSequences=[...n.stopSequences];let i={},a=n.outputConfig?.textFormat?.structure?.jsonSchema;if(a?.schema!=null){let e=null;if(typeof a.schema==`string`){let{json:t}=gp(a.schema);typeof t==`object`&&t&&!Array.isArray(t)&&(e=t)}else typeof a.schema==`object`&&!Array.isArray(a.schema)&&(e=a.schema);if(e!=null){let t={name:typeof a.name==`string`?a.name:`response`,schema:e};typeof a.description==`string`&&(t.description=a.description),i.responseFormat={type:`json_schema`,jsonSchema:t}}}return{config:Rp(r),promoted:i}}function Jp(e,t){switch(t){case`maxTokens`:return e.maxTokens;case`temperature`:return e.temperature;case`topP`:return e.topP;case`stopSequences`:return e.stopSequences;default:return}}function Yp(e,t,n){switch(t){case`maxTokens`:case`temperature`:case`topP`:if(n===void 0){let n={...e};return delete n[t],Rp(n)}return typeof n!=`number`||Number.isNaN(n)?e:Rp({...e,[t]:n});case`stopSequences`:if(n===void 0){let t={...e};return delete t.stopSequences,Rp(t)}return Array.isArray(n)?Rp({...e,stopSequences:n.map(String)}):e;default:return e}}var Xp={getDefaultConfig:Pp,getVisibleSpecs:Fp,parseConfig:Lp,normalize:Rp,validateForSubmit:zp,toPromptInput:Bp,fromPromptInvocationParameters:Vp,fromPromptInvocationParametersForDisplay:Hp,fromSpanInvocationParameters:e=>qp(e),readField:Jp,writeField:Yp};function Zp(){return{temperature:1,presencePenalty:0,frequencyPenalty:0,thinkingConfig:{thinkingLevel:`MEDIUM`,includeThoughts:!0}}}function Qp(){return Lf}var $p=J().transform(e=>e.toUpperCase()).pipe(tr(jf)).optional().catch(void 0),em=er({thinkingBudget:Y().optional().catch(void 0),thinkingLevel:$p,includeThoughts:rr().optional().catch(void 0)}).optional().catch(void 0),tm=er({temperature:Y().optional().catch(void 0),maxOutputTokens:Y().optional().catch(void 0),stopSequences:$n(J()).optional().catch(void 0),presencePenalty:Y().optional().catch(void 0),frequencyPenalty:Y().optional().catch(void 0),topP:Y().optional().catch(void 0),topK:Y().optional().catch(void 0),thinkingConfig:em});function nm(e){let t=tm.safeParse(e),n=t.success?t.data:{},r={};return n.temperature!==void 0&&(r.temperature=n.temperature),n.maxOutputTokens!==void 0&&(r.maxOutputTokens=n.maxOutputTokens),n.stopSequences!==void 0&&(r.stopSequences=[...n.stopSequences]),n.presencePenalty!==void 0&&(r.presencePenalty=n.presencePenalty),n.frequencyPenalty!==void 0&&(r.frequencyPenalty=n.frequencyPenalty),n.topP!==void 0&&(r.topP=n.topP),n.topK!==void 0&&(r.topK=n.topK),n.thinkingConfig!==void 0&&n.thinkingConfig!==null&&(r.thinkingConfig=rm(n.thinkingConfig)),r}function rm(e){let t={};return e.thinkingBudget!==void 0&&(t.thinkingBudget=e.thinkingBudget),e.thinkingLevel!==void 0&&(t.thinkingLevel=e.thinkingLevel),e.includeThoughts!==void 0&&(t.includeThoughts=e.includeThoughts),t}function im(e){return e}function am(e){return[]}function om(e){let t={};return e.thinkingBudget!==void 0&&(t.thinkingBudget=e.thinkingBudget),e.thinkingLevel!==void 0&&(t.thinkingLevel=e.thinkingLevel),e.includeThoughts!==void 0&&(t.includeThoughts=e.includeThoughts),Object.keys(t).length>0?t:void 0}function sm(e){let t=im(e),n={};if(t.temperature!==void 0&&(n.temperature=t.temperature),t.maxOutputTokens!==void 0&&(n.maxOutputTokens=t.maxOutputTokens),t.stopSequences!==void 0&&(n.stopSequences=t.stopSequences),t.presencePenalty!==void 0&&(n.presencePenalty=t.presencePenalty),t.frequencyPenalty!==void 0&&(n.frequencyPenalty=t.frequencyPenalty),t.topP!==void 0&&(n.topP=t.topP),t.topK!==void 0&&(n.topK=t.topK),t.thinkingConfig!==void 0){let e=om(t.thinkingConfig);e&&(n.thinkingConfig=e)}return{google:n}}function cm(e){if(e.__typename!==`PromptGoogleInvocationParameters`)throw Error(`googleAdapter.fromPromptInvocationParameters called with non-Google typename: ${e.__typename}`);let t={};if(e.temperature!=null&&(t.temperature=e.temperature),e.maxOutputTokens!=null&&(t.maxOutputTokens=e.maxOutputTokens),e.stopSequences!=null&&(t.stopSequences=[...e.stopSequences]),e.presencePenalty!=null&&(t.presencePenalty=e.presencePenalty),e.frequencyPenalty!=null&&(t.frequencyPenalty=e.frequencyPenalty),e.topP!=null&&(t.topP=e.topP),e.topK!=null&&(t.topK=e.topK),e.thinkingConfig){let n={};e.thinkingConfig.thinkingBudget!=null&&(n.thinkingBudget=e.thinkingConfig.thinkingBudget),e.thinkingConfig.thinkingLevel!=null&&(n.thinkingLevel=e.thinkingConfig.thinkingLevel),e.thinkingConfig.includeThoughts!=null&&(n.includeThoughts=e.thinkingConfig.includeThoughts),Object.keys(n).length>0&&(t.thinkingConfig=n)}return im(t)}function lm(e){if(e.__typename!==`PromptGoogleInvocationParameters`)throw Error(`googleAdapter.fromPromptInvocationParametersForDisplay called with non-Google typename: ${e.__typename}`);let t={};if(e.temperature!=null&&(t.temperature=e.temperature),e.maxOutputTokens!=null&&(t.maxOutputTokens=e.maxOutputTokens),e.stopSequences!=null&&(t.stopSequences=[...e.stopSequences]),e.presencePenalty!=null&&(t.presencePenalty=e.presencePenalty),e.frequencyPenalty!=null&&(t.frequencyPenalty=e.frequencyPenalty),e.topP!=null&&(t.topP=e.topP),e.topK!=null&&(t.topK=e.topK),e.thinkingConfig){let n={};e.thinkingConfig.thinkingBudget!=null&&(n.thinkingBudget=e.thinkingConfig.thinkingBudget),e.thinkingConfig.thinkingLevel!=null&&(n.thinkingLevel=e.thinkingConfig.thinkingLevel),e.thinkingConfig.includeThoughts!=null&&(n.includeThoughts=e.thinkingConfig.includeThoughts),Object.keys(n).length>0&&(t.thinkingConfig=n)}return t}var um=er({thinking_budget:Y().optional().catch(void 0),thinking_level:$p,include_thoughts:rr().optional().catch(void 0)}).optional().catch(void 0),dm=er({temperature:Y().optional().catch(void 0),max_output_tokens:Y().optional().catch(void 0),stop_sequences:$n(J()).optional().catch(void 0),presence_penalty:Y().optional().catch(void 0),frequency_penalty:Y().optional().catch(void 0),top_p:Y().optional().catch(void 0),top_k:Y().optional().catch(void 0),thinking_config:um,response_json_schema:ir().optional(),response_schema:ir().optional(),response_mime_type:J().optional().catch(void 0)});function fm(e){let t=dm.safeParse(e),n=t.success?t.data:{},r={};if(n.temperature!==void 0&&(r.temperature=n.temperature),n.max_output_tokens!==void 0&&(r.maxOutputTokens=n.max_output_tokens),n.stop_sequences!==void 0&&(r.stopSequences=[...n.stop_sequences]),n.presence_penalty!==void 0&&(r.presencePenalty=n.presence_penalty),n.frequency_penalty!==void 0&&(r.frequencyPenalty=n.frequency_penalty),n.top_p!==void 0&&(r.topP=n.top_p),n.top_k!==void 0&&(r.topK=n.top_k),n.thinking_config){let e={};n.thinking_config.thinking_budget!==void 0&&(e.thinkingBudget=n.thinking_config.thinking_budget),n.thinking_config.thinking_level!==void 0&&(e.thinkingLevel=n.thinking_config.thinking_level),n.thinking_config.include_thoughts!==void 0&&(e.includeThoughts=n.thinking_config.include_thoughts),Object.keys(e).length>0&&(r.thinkingConfig=e)}let i={},a=n.response_json_schema??n.response_schema;return a!=null&&n.response_mime_type===`application/json`&&(i.responseFormat={type:`json_schema`,jsonSchema:{name:`response`,schema:a}}),{config:im(r),promoted:i}}var pm=new Set([`temperature`,`maxOutputTokens`,`presencePenalty`,`frequencyPenalty`,`topP`,`topK`]);function mm(e){return pm.has(e)}function hm(e){let t={};return e.thinkingBudget!==void 0&&(t.thinkingBudget=e.thinkingBudget),e.thinkingLevel!==void 0&&(t.thinkingLevel=e.thinkingLevel),e.includeThoughts!==void 0&&(t.includeThoughts=e.includeThoughts),Object.keys(t).length===0?void 0:t}function gm(e,t){if(mm(t))return e[t];switch(t){case`stopSequences`:return e.stopSequences;case`thinkingBudget`:return e.thinkingConfig?.thinkingBudget;case`thinkingLevel`:return e.thinkingConfig?.thinkingLevel?.toLowerCase();case`includeThoughts`:return e.thinkingConfig?.includeThoughts;default:return}}function _m(e,t,n){if(mm(t)){if(n===void 0){let n={...e};return delete n[t],im(n)}return typeof n!=`number`||Number.isNaN(n)?e:im({...e,[t]:n})}switch(t){case`stopSequences`:if(n===void 0){let t={...e};return delete t.stopSequences,im(t)}return Array.isArray(n)?im({...e,stopSequences:n.map(String)}):e;case`thinkingBudget`:{let t={...e.thinkingConfig??{}};if(n===void 0)delete t.thinkingBudget;else if(typeof n==`number`&&!Number.isNaN(n))t.thinkingBudget=n;else return e;return vm(e,t)}case`thinkingLevel`:{let t={...e.thinkingConfig??{}};if(n===void 0)delete t.thinkingLevel;else{let r=$p.safeParse(n);if(!r.success||!r.data)return e;t.thinkingLevel=r.data}return vm(e,t)}case`includeThoughts`:{let t={...e.thinkingConfig??{}};if(n===void 0)delete t.includeThoughts;else if(typeof n==`boolean`)t.includeThoughts=n;else return e;return vm(e,t)}default:return e}}function vm(e,t){let n=hm(t),r={...e};return n===void 0?delete r.thinkingConfig:r.thinkingConfig=n,im(r)}var ym={getDefaultConfig:Zp,getVisibleSpecs:Qp,parseConfig:nm,normalize:im,validateForSubmit:am,toPromptInput:sm,fromPromptInvocationParameters:cm,fromPromptInvocationParametersForDisplay:lm,fromSpanInvocationParameters:e=>fm(e),readField:gm,writeField:_m};function bm(e){if(typeof e==`object`&&e&&!Array.isArray(e))return e}function xm(e){return e===0?void 0:e}function Sm(){return{frequencyPenalty:0,presencePenalty:0}}function Cm(e,t){let n=t.openaiApiType??`RESPONSES`;return Ff.filter(e=>{let t=`applicableOpenAIApiTypes`in e?e.applicableOpenAIApiTypes:void 0;return t==null||t.includes(n)})}var wm=er({temperature:Y().optional().catch(void 0),topP:Y().optional().catch(void 0),maxCompletionTokens:Y().optional().catch(void 0),frequencyPenalty:Y().optional().catch(void 0),presencePenalty:Y().optional().catch(void 0),reasoningEffort:J().optional().catch(void 0),seed:Y().optional().catch(void 0),stop:$n(J()).optional().catch(void 0),extraBody:or(J(),ir()).optional().catch(void 0)});function Tm(e){let t=wm.safeParse(e),n=t.success?t.data:{},r={};if(n.temperature!==void 0&&(r.temperature=n.temperature),n.topP!==void 0&&(r.topP=n.topP),n.maxCompletionTokens!==void 0&&(r.maxCompletionTokens=n.maxCompletionTokens),n.frequencyPenalty!==void 0&&(r.frequencyPenalty=n.frequencyPenalty),n.presencePenalty!==void 0&&(r.presencePenalty=n.presencePenalty),n.reasoningEffort!==void 0){let e=Tf(n.reasoningEffort);e!==void 0&&(r.reasoningEffort=e)}return n.seed!==void 0&&(r.seed=n.seed),n.stop!==void 0&&(r.stop=[...n.stop]),n.extraBody!==void 0&&(r.extraBody={...n.extraBody}),r}function Em(e){return e}function Dm(e){return[]}function Om(e){let t=Em(e),n={};t.temperature!==void 0&&(n.temperature=t.temperature),t.topP!==void 0&&(n.topP=t.topP),t.maxCompletionTokens!==void 0&&(n.maxCompletionTokens=t.maxCompletionTokens);let r=xm(t.frequencyPenalty);r!==void 0&&(n.frequencyPenalty=r);let i=xm(t.presencePenalty);if(i!==void 0&&(n.presencePenalty=i),t.reasoningEffort!==void 0){let e=wf(t.reasoningEffort);e!==void 0&&(n.reasoningEffort=e)}return t.seed!==void 0&&(n.seed=t.seed),t.stop!==void 0&&(n.stop=t.stop),t.extraBody!==void 0&&(n.extraBody=t.extraBody),{openai:n}}function km(e){if(e.__typename!==`PromptOpenAIInvocationParameters`)throw Error(`openaiAdapter.fromPromptInvocationParameters called with non-OpenAI typename: ${e.__typename}`);let t={};if(e.temperature!=null&&(t.temperature=e.temperature),e.topP!=null&&(t.topP=e.topP),e.maxCompletionTokens==null?e.openaiMaxTokens!=null&&(t.maxCompletionTokens=e.openaiMaxTokens):t.maxCompletionTokens=e.maxCompletionTokens,e.frequencyPenalty!=null&&(t.frequencyPenalty=e.frequencyPenalty),e.presencePenalty!=null&&(t.presencePenalty=e.presencePenalty),e.seed!=null&&(t.seed=e.seed),e.stop!=null&&(t.stop=[...e.stop]),e.reasoningEffort!=null){let n=Tf(e.reasoningEffort);n!==void 0&&(t.reasoningEffort=n)}let n=bm(e.extraBody);return n!=null&&(t.extraBody=n),Em(t)}function Am(e){if(e.__typename!==`PromptOpenAIInvocationParameters`)throw Error(`openaiAdapter.fromPromptInvocationParametersForDisplay called with non-OpenAI typename: ${e.__typename}`);let t={};e.temperature!=null&&(t.temperature=e.temperature),e.openaiMaxTokens!=null&&(t.maxTokens=e.openaiMaxTokens),e.maxCompletionTokens!=null&&(t.maxCompletionTokens=e.maxCompletionTokens),e.frequencyPenalty!=null&&(t.frequencyPenalty=e.frequencyPenalty),e.presencePenalty!=null&&(t.presencePenalty=e.presencePenalty),e.topP!=null&&(t.topP=e.topP),e.seed!=null&&(t.seed=e.seed),e.stop!=null&&(t.stop=[...e.stop]);let n=Tf(e.reasoningEffort);n!==void 0&&(t.reasoningEffort=n);let r=bm(e.extraBody);return r!=null&&(t.extraBody=r),t}var jm=lr({name:J().optional(),schema:ir().optional(),strict:rr().nullish(),description:J().nullish()}),Mm=lr({type:J().optional(),json_schema:jm.optional()}).optional().catch(void 0),Nm=lr({type:J().optional(),name:J().optional(),schema:ir().optional(),strict:rr().optional(),description:J().optional()}).optional().catch(void 0),Pm=er({temperature:Y().optional().catch(void 0),top_p:Y().optional().catch(void 0),max_completion_tokens:Y().optional().catch(void 0),max_tokens:Y().optional().catch(void 0),max_output_tokens:Y().optional().catch(void 0),frequency_penalty:Y().optional().catch(void 0),presence_penalty:Y().optional().catch(void 0),seed:Y().optional().catch(void 0),stop:$n(J()).optional().catch(void 0),reasoning_effort:J().optional().catch(void 0),reasoning:er({effort:J().optional().catch(void 0)}).optional().catch(void 0),response_format:Mm,text:lr({format:Nm}).optional().catch(void 0),extra_body:or(J(),ir()).optional().catch(void 0)});function Fm(e,t){let n=Pm.safeParse(e),r=n.success?n.data:{},i={};r.temperature!==void 0&&(i.temperature=r.temperature),r.top_p!==void 0&&(i.topP=r.top_p),r.max_completion_tokens===void 0?r.max_tokens===void 0?t===`RESPONSES`&&r.max_output_tokens!==void 0&&(i.maxCompletionTokens=r.max_output_tokens):i.maxCompletionTokens=r.max_tokens:i.maxCompletionTokens=r.max_completion_tokens,r.frequency_penalty!==void 0&&(i.frequencyPenalty=r.frequency_penalty),r.presence_penalty!==void 0&&(i.presencePenalty=r.presence_penalty),r.seed!==void 0&&(i.seed=r.seed),r.stop!==void 0&&(i.stop=[...r.stop]);let a;if(r.reasoning_effort===void 0?t===`RESPONSES`&&r.reasoning?.effort!==void 0&&(a=r.reasoning.effort):a=r.reasoning_effort,a!==void 0){let e=Tf(a);e!==void 0&&(i.reasoningEffort=e)}r.extra_body!==void 0&&(i.extraBody={...r.extra_body});let o={},s=r.response_format;if(s?.json_schema){let e=s.json_schema,t={name:typeof e.name==`string`?e.name:`response`};e.schema!==void 0&&(t.schema=e.schema),e.strict!==void 0&&e.strict!==null&&(t.strict=e.strict),e.description!==void 0&&e.description!==null&&(t.description=e.description),o.responseFormat={type:`json_schema`,jsonSchema:t}}else if(r.text?.format!==void 0){let e=r.text.format;if(e){let t={name:typeof e.name==`string`?e.name:`response`};e.schema!==void 0&&(t.schema=e.schema),e.strict!==void 0&&(t.strict=e.strict),e.description!==void 0&&(t.description=e.description),o.responseFormat={type:`json_schema`,jsonSchema:t}}}return{config:Em(i),promoted:o}}var Im=new Set([`temperature`,`topP`,`maxCompletionTokens`,`frequencyPenalty`,`presencePenalty`,`seed`]);function Lm(e){return Im.has(e)}function Rm(e,t){if(Lm(t))return e[t];switch(t){case`reasoningEffort`:return e.reasoningEffort;case`stop`:return e.stop;case`extraBody`:return e.extraBody;default:return}}function zm(e,t,n){if(Lm(t)){if(n===void 0){let n={...e};return delete n[t],Em(n)}return typeof n!=`number`||Number.isNaN(n)?e:Em({...e,[t]:n})}switch(t){case`reasoningEffort`:if(n===void 0){let t={...e};return delete t.reasoningEffort,Em(t)}return typeof n==`string`?Em({...e,reasoningEffort:n}):e;case`stop`:if(n===void 0){let t={...e};return delete t.stop,Em(t)}return Array.isArray(n)?Em({...e,stop:n.map(String)}):e;case`extraBody`:{if(n===void 0){let t={...e};return delete t.extraBody,Em(t)}let t=bm(n);return t===void 0?e:Em({...e,extraBody:t})}default:return e}}var Bm={getDefaultConfig:Sm,getVisibleSpecs:Cm,parseConfig:Tm,normalize:Em,validateForSubmit:Dm,toPromptInput:Om,fromPromptInvocationParameters:km,fromPromptInvocationParametersForDisplay:Am,fromSpanInvocationParameters:(e,t)=>Fm(e,t?.openaiApiType??null),readField:Rm,writeField:zm};function Vm(e){switch(e){case Nf.OPENAI:return Bm;case Nf.ANTHROPIC:return fp;case Nf.GOOGLE_GENAI:return ym;case Nf.AWS_BEDROCK:return Xp;default:return dr(e)}}function Hm(e){return Vm(Pf(e))}function Um(e){let t=Hm(e);return t.normalize(t.getDefaultConfig())}function Wm(e,t){let n=Hm(e);return n.normalize(n.parseConfig(t))}function Gm(e,t){return Hm(e).toPromptInput(t)}function Km(e,t){if(t==null)return Um(e);let n=Pf(e);return n===Nf.OPENAI&&t.__typename===`PromptOpenAIInvocationParameters`||n===Nf.ANTHROPIC&&t.__typename===`PromptAnthropicInvocationParameters`||n===Nf.GOOGLE_GENAI&&t.__typename===`PromptGoogleInvocationParameters`||n===Nf.AWS_BEDROCK&&t.__typename===`PromptAwsInvocationParameters`?Hm(e).fromPromptInvocationParameters(t):Um(e)}function qm(e){if(e==null)return null;let t;switch(e.__typename){case`PromptOpenAIInvocationParameters`:t=Nf.OPENAI;break;case`PromptAnthropicInvocationParameters`:t=Nf.ANTHROPIC;break;case`PromptGoogleInvocationParameters`:t=Nf.GOOGLE_GENAI;break;case`PromptAwsInvocationParameters`:t=Nf.AWS_BEDROCK;break;case`%other`:throw Error(`Unsupported prompt invocation parameters typename: %other`);default:return dr(e)}let n=Vm(t);return{family:t,parameters:n.fromPromptInvocationParametersForDisplay(e)}}function Jm(e,t,n={}){let{config:r,promoted:i}=Hm(e).fromSpanInvocationParameters(t,n);return{invocationParameters:r,responseFormat:i.responseFormat}}function Ym(e,t,n){return Hm(e).readField(t,n)}function Xm(e,t){return Hm(e.provider).getVisibleSpecs(t,{openaiApiType:e.openaiApiType})}function Zm(e,t,n,r){return Hm(e).writeField(t,n,r)}function Qm(){if(typeof crypto<`u`&&typeof crypto.randomUUID==`function`)return crypto.randomUUID();let e=new Uint8Array(16);crypto.getRandomValues(e),e[6]=e[6]&15|64,e[8]=e[8]&63|128;let t=Array.from(e).map(e=>e.toString(16).padStart(2,`0`)).join(``);return`${t.slice(0,8)}-${t.slice(8,12)}-${t.slice(12,16)}-${t.slice(16,20)}-${t.slice(20)}`}var $m={provider:`ANTHROPIC`,modelName:`claude-opus-4-6`,invocationParameters:Um(`ANTHROPIC`)},eh={collectorEndpoint:null,assistantProjectName:`assistant_agent`,forceTracing:!1,webAccessEnabled:!1,assistantEnabled:!1,allowLocalTraces:!1,allowRemoteExport:!1},th={storeLocalTraces:!0,exportRemoteTraces:!1,attachUserId:!1,acknowledgedTraceConsent:null},nh={edits:`manual`},rh=`(branch) `,ih=50;function ah(e){let t=e.shortSummary.trim();if(!t){let n=e.messages.find(e=>e.role===`user`)?.parts.filter(sr).map(e=>e.text).join(` `).trim();t=n?n.length>ih?`${n.slice(0,ih)}...`:n:``}return t.startsWith(rh)?t:t?`${rh}${t}`:rh.trim()}function oh(e){return{allowLocalTraces:e.allowLocalTraces,allowRemoteExport:!!e.collectorEndpoint&&e.allowRemoteExport}}function sh({agentsConfig:e,observability:t}){if(e.forceTracing)return!0;let n=t.acknowledgedTraceConsent;if(!n)return!1;let r=oh(e);return(!r.allowLocalTraces||n.allowLocalTraces)&&(!r.allowRemoteExport||n.allowRemoteExport)}function ch({agentsConfig:e,observability:t}){if(e.forceTracing)return{ingestTraces:!0,exportRemoteTraces:!0};let n=oh(e);return{ingestTraces:n.allowLocalTraces&&t.storeLocalTraces,exportRemoteTraces:n.allowRemoteExport&&t.exportRemoteTraces}}function lh({agentsConfig:e,observability:t}){return e.forceTracing||t.attachUserId}function uh({capabilities:e,defaultCapabilities:t=gf()}){if(!e||typeof e!=`object`)return{...t};let n=e;return Object.fromEntries(Object.keys(t).map(e=>{let r=n[e];return[e,typeof r==`boolean`?r:t[e]]}))}function dh(e,t){if(!e||typeof e!=`object`)return t;let n=e;return{...t,...n,observability:{...t.observability,...n.observability},capabilities:uh({capabilities:n.capabilities,defaultCapabilities:t.capabilities})}}function fh({record:e,retainedSessionIds:t}){return Object.fromEntries(Object.entries(e).filter(([e])=>t.has(e)))}function ph({record:e,retainedSessionIds:t}){return Object.fromEntries(Object.entries(e).filter(([,e])=>e!=null&&t.has(e.sessionId)))}function mh(e,t){return Object.fromEntries(Object.entries(e).filter(([,e])=>e?.sessionId!==t))}function hh({state:e,retainedSessionIds:t,activeSessionId:n}){let r=new Set(t);return{sessions:t,activeSessionId:n,sessionMap:fh({record:e.sessionMap,retainedSessionIds:r}),pendingElicitationBySessionId:fh({record:e.pendingElicitationBySessionId,retainedSessionIds:r}),chatStatusBySessionId:fh({record:e.chatStatusBySessionId,retainedSessionIds:r}),isResponsePendingBySessionId:fh({record:e.isResponsePendingBySessionId,retainedSessionIds:r}),draftInputBySessionId:fh({record:e.draftInputBySessionId,retainedSessionIds:r}),pendingMessageBySessionId:fh({record:e.pendingMessageBySessionId,retainedSessionIds:r}),pendingPatchExperimentsByToolCallId:ph({record:e.pendingPatchExperimentsByToolCallId,retainedSessionIds:r})}}var gh=`arize-phoenix-assistant`;function _h(){let e=(window.Config?.basename??``).replace(/\/+$/,``);return e?`${gh}:${e}`:gh}var vh=e=>Oe()(R(n((t,n)=>({isOpen:!1,position:`pinned`,fabMode:`pinned`,fabPlacement:`bottom-end`,sessions:[],activeSessionId:null,sessionMap:{},defaultModelConfig:{...$m},agentsConfig:eh,observability:th,permissions:nh,capabilities:gf(),routeContexts:[],mountedContexts:{},pendingPromptEditsByToolCallId:{},pendingPromptInstanceRemovalsByToolCallId:{},pendingBatchSpanAnnotatesByToolCallId:{},pendingDatasetWritesByToolCallId:{},pendingAnnotationConfigWritesByToolCallId:{},pendingPatchExperimentsByToolCallId:{},pendingPromptToolWritesByToolCallId:{},pendingSavePromptsByToolCallId:{},pendingCodeEvaluatorEditsByToolCallId:{},pendingLlmEvaluatorEditsByToolCallId:{},pendingLoadDatasetsByToolCallId:{},setIsOpen:e=>{t({isOpen:e},!1,{type:`setIsOpen`})},toggleOpen:()=>{t(e=>({isOpen:!e.isOpen}),!1,{type:`toggleOpen`})},setPosition:e=>{t({position:e},!1,{type:`setPosition`})},setFabMode:e=>{t({fabMode:e},!1,{type:`setFabMode`})},setFabPlacement:e=>{t({fabPlacement:e},!1,{type:`setFabPlacement`})},createSession:()=>{let e=Qm();return t(t=>{let n={id:e,shortSummary:``,messages:[],context:[],modelConfig:{...t.defaultModelConfig},createdAt:Date.now()},r;return r=t.capabilities[`session.storeSessions`]?[...t.sessions,e].slice(-3):[e],{...hh({state:{...t,sessionMap:{...t.sessionMap,[e]:n}},retainedSessionIds:r,activeSessionId:e})}},!1,{type:`createSession`}),e},forkSession:({sourceSessionId:e,messages:n,restoredInput:r})=>{let i=Qm(),a=!1;return t(t=>{let o=t.sessionMap[e];if(!o)return t;a=!0;let s={id:i,shortSummary:ah(o),messages:n,context:[...o.context],modelConfig:{...o.modelConfig},createdAt:Date.now()},c=[...t.sessions,i].slice(-3),l=r?{...t.draftInputBySessionId,[i]:r}:t.draftInputBySessionId;return{...hh({state:{...t,sessionMap:{...t.sessionMap,[i]:s},draftInputBySessionId:l},retainedSessionIds:c,activeSessionId:i})}},!1,{type:`forkSession`}),a?i:null},deleteSession:e=>{t(t=>{if(!t.sessionMap[e])return t;let n={...t.sessionMap};delete n[e];let r={...t.pendingElicitationBySessionId};delete r[e];let i={...t.chatStatusBySessionId};delete i[e];let a={...t.isResponsePendingBySessionId};delete a[e];let o={...t.draftInputBySessionId};delete o[e];let s={...t.pendingMessageBySessionId};delete s[e];let c=mh(t.pendingPatchExperimentsByToolCallId,e),l=t.sessions.filter(t=>t!==e);return{sessions:l,sessionMap:n,activeSessionId:t.activeSessionId===e?l[l.length-1]??null:t.activeSessionId,pendingElicitationBySessionId:r,chatStatusBySessionId:i,isResponsePendingBySessionId:a,draftInputBySessionId:o,pendingMessageBySessionId:s,pendingPatchExperimentsByToolCallId:c}},!1,{type:`deleteSession`})},setActiveSession:e=>{t({activeSessionId:e},!1,{type:`setActiveSession`})},updateSessionSummary:(e,n)=>{t(t=>{let r=t.sessionMap[e];return r?{sessionMap:{...t.sessionMap,[e]:{...r,shortSummary:n}}}:t},!1,{type:`updateSessionSummary`})},updateSessionModelConfig:(e,n)=>{t(t=>{let r=t.sessionMap[e];return r?{sessionMap:{...t.sessionMap,[e]:{...r,modelConfig:{...r.modelConfig,...n}}}}:t},!1,{type:`updateSessionModelConfig`})},addSessionContext:(e,n)=>{t(t=>{let r=t.sessionMap[e];return r?{sessionMap:{...t.sessionMap,[e]:{...r,context:[...r.context,n]}}}:t},!1,{type:`addSessionContext`})},removeSessionContext:(e,n)=>{t(t=>{let r=t.sessionMap[e];return r?{sessionMap:{...t.sessionMap,[e]:{...r,context:r.context.filter(e=>e!==n)}}}:t},!1,{type:`removeSessionContext`})},setSessionMessages:(e,n)=>{t(t=>{let r=t.sessionMap[e];return r?{sessionMap:{...t.sessionMap,[e]:{...r,messages:n}}}:t},!1,{type:`setSessionMessages`})},setDefaultModelConfig:e=>{t({defaultModelConfig:e},!1,{type:`setDefaultModelConfig`})},setObservability:e=>{t(t=>({observability:{...t.observability,...e}}),!1,{type:`setObservability`})},setPermissions:e=>{t(t=>({permissions:{...t.permissions,...e}}),!1,{type:`setPermissions`})},setAgentsConfig:e=>{t(t=>({agentsConfig:{...t.agentsConfig,...e}}),!1,{type:`setAgentsConfig`})},acknowledgeConsent:()=>{t(e=>({observability:{...e.observability,acknowledgedTraceConsent:oh(e.agentsConfig)}}),!1,{type:`acknowledgeConsent`})},clearAllSessions:()=>{t({sessions:[],activeSessionId:null,sessionMap:{},pendingElicitationBySessionId:{},chatStatusBySessionId:{},isResponsePendingBySessionId:{},draftInputBySessionId:{},pendingMessageBySessionId:{},pendingPatchExperimentsByToolCallId:{}},!1,{type:`clearAllSessions`})},setCapability:({key:e,enabled:n})=>{t(t=>{let r={...t.capabilities,[e]:n};return e!==`session.storeSessions`||n?{capabilities:r}:{capabilities:r,...hh({state:t,retainedSessionIds:t.activeSessionId?[t.activeSessionId]:[],activeSessionId:t.activeSessionId})}},!1,{type:`setCapability`})},pendingElicitationBySessionId:{},setPendingElicitation:(e,n)=>{t(t=>{let r={...t.pendingElicitationBySessionId};return n?r[e]=n:delete r[e],{pendingElicitationBySessionId:r}},!1,{type:`setPendingElicitation`})},draftInputBySessionId:{},setDraftInput:(e,n)=>{t(t=>{let r={...t.draftInputBySessionId};return n?r[e]=n:delete r[e],{draftInputBySessionId:r}},!1,{type:`setDraftInput`})},pendingMessageBySessionId:{},setPendingMessage:(e,n)=>{t(t=>{let r={...t.pendingMessageBySessionId};return n?r[e]=n:delete r[e],{pendingMessageBySessionId:r}},!1,{type:`setPendingMessage`})},consumePendingMessage:e=>{let r=n().pendingMessageBySessionId[e]??null;return r!=null&&t(t=>{if(!(e in t.pendingMessageBySessionId))return t;let n={...t.pendingMessageBySessionId};return delete n[e],{pendingMessageBySessionId:n}},!1,{type:`consumePendingMessage`}),r},chatStatusBySessionId:{},setSessionChatStatus:(e,n)=>{t(t=>({chatStatusBySessionId:{...t.chatStatusBySessionId,[e]:n}}),!1,{type:`setSessionChatStatus`})},isResponsePendingBySessionId:{},setSessionResponsePending:(e,n)=>{t(t=>{if(!(e in t.sessionMap))return t;let r={...t.isResponsePendingBySessionId};return n?r[e]=!0:delete r[e],{isResponsePendingBySessionId:r}},!1,{type:`setSessionResponsePending`})},setSessionUsage:(e,n)=>{t(t=>{let r=t.sessionMap[e];if(!r)return t;let i=r.usage??{tokenCount:{total:0,completion:0,prompt:0}};return{sessionMap:{...t.sessionMap,[e]:{...r,usage:{...i,tokenCount:{prompt:n.prompt,completion:n.completion,total:n.total??n.prompt+n.completion,...n.promptDetails?{promptDetails:n.promptDetails}:{}}}}}}},!1,{type:`setSessionUsage`})},setRouteContexts:e=>{t(t=>{if(t.routeContexts.length===e.length){let n=!0;for(let r=0;r<e.length;r++)if(ff(t.routeContexts[r])!==ff(e[r])){n=!1;break}if(n)return t}return{routeContexts:e}},!1,{type:`setRouteContexts`})},setMountedContext:(e,n)=>{t(t=>({mountedContexts:{...t.mountedContexts,[e]:n}}),!1,{type:`setMountedContext`})},removeMountedContext:e=>{t(t=>{if(!(e in t.mountedContexts))return t;let n={...t.mountedContexts};return delete n[e],{mountedContexts:n}},!1,{type:`removeMountedContext`})},registeredClientActions:{},registerClientAction:(e,n)=>{t(t=>({registeredClientActions:{...t.registeredClientActions,[e]:n}}),!1,{type:`registerClientAction`})},unregisterClientAction:e=>{t(t=>{if(!(e in t.registeredClientActions))return t;let n={...t.registeredClientActions};return delete n[e],{registeredClientActions:n}},!1,{type:`unregisterClientAction`})},setPendingPromptEdit:(e,n)=>{t(t=>{let r={...t.pendingPromptEditsByToolCallId};return n?r[e]=n:delete r[e],{pendingPromptEditsByToolCallId:r}},!1,{type:`setPendingPromptEdit`})},setPendingPromptInstanceRemoval:(e,n)=>{t(t=>{let r={...t.pendingPromptInstanceRemovalsByToolCallId};return n?r[e]=n:delete r[e],{pendingPromptInstanceRemovalsByToolCallId:r}},!1,{type:`setPendingPromptInstanceRemoval`})},setPendingDatasetWrite:(e,n)=>{t(t=>{let r={...t.pendingDatasetWritesByToolCallId};return n?r[e]=n:delete r[e],{pendingDatasetWritesByToolCallId:r}},!1,{type:`setPendingDatasetWrite`})},setPendingAnnotationConfigWrite:(e,n)=>{t(t=>{let r={...t.pendingAnnotationConfigWritesByToolCallId};return n?r[e]=n:delete r[e],{pendingAnnotationConfigWritesByToolCallId:r}},!1,{type:`setPendingAnnotationConfigWrite`})},setPendingBatchSpanAnnotate:(e,n)=>{t(t=>{let r={...t.pendingBatchSpanAnnotatesByToolCallId};return n?r[e]=n:delete r[e],{pendingBatchSpanAnnotatesByToolCallId:r}},!1,{type:`setPendingBatchSpanAnnotate`})},setPendingPatchExperiment:(e,n)=>{t(t=>{let r={...t.pendingPatchExperimentsByToolCallId};return n?r[e]=n:delete r[e],{pendingPatchExperimentsByToolCallId:r}},!1,{type:`setPendingPatchExperiment`})},setPendingPromptToolWrite:(e,n)=>{t(t=>{let r={...t.pendingPromptToolWritesByToolCallId};return n?r[e]=n:delete r[e],{pendingPromptToolWritesByToolCallId:r}},!1,{type:`setPendingPromptToolWrite`})},setPendingSavePrompt:(e,n)=>{t(t=>{let r={...t.pendingSavePromptsByToolCallId};return n?r[e]=n:delete r[e],{pendingSavePromptsByToolCallId:r}},!1,{type:`setPendingSavePrompt`})},setPendingCodeEvaluatorEdit:(e,n)=>{t(t=>{let r={...t.pendingCodeEvaluatorEditsByToolCallId};return n?r[e]=n:delete r[e],{pendingCodeEvaluatorEditsByToolCallId:r}},!1,{type:`setPendingCodeEvaluatorEdit`})},setPendingLlmEvaluatorEdit:(e,n)=>{t(t=>{let r={...t.pendingLlmEvaluatorEditsByToolCallId};return n?r[e]=n:delete r[e],{pendingLlmEvaluatorEditsByToolCallId:r}},!1,{type:`setPendingLlmEvaluatorEdit`})},setPendingLoadDataset:(e,n)=>{t(t=>{let r={...t.pendingLoadDatasetsByToolCallId};return n?r[e]=n:delete r[e],{pendingLoadDatasetsByToolCallId:r}},!1,{type:`setPendingLoadDataset`})},...e}),{name:`agentStore`}),{name:_h(),version:0,partialize:e=>({isOpen:e.isOpen,position:e.position,fabMode:e.fabMode,fabPlacement:e.fabPlacement,sessions:e.sessions,activeSessionId:e.activeSessionId,sessionMap:e.sessionMap,defaultModelConfig:e.defaultModelConfig,observability:e.observability,permissions:e.permissions,capabilities:e.capabilities}),merge:dh}));async function yh({agentStore:e,names:t,timeoutMs:n=5e3}){let r=e=>t.every(t=>t in e);return r(e.getState().registeredClientActions)?!0:new Promise(t=>{let i=!1,a=null,o=e=>{i||(i=!0,a&&clearTimeout(a),s(),t(e))},s=e.subscribe(e=>{r(e.registeredClientActions)&&o(!0)});a=setTimeout(()=>o(!1),n),r(e.getState().registeredClientActions)&&o(!0)})}var bh=(0,X.createContext)(null);function xh(e){let t=(0,Z.c)(8),n,r;t[0]===e?(n=t[1],r=t[2]):({children:n,...r}=e,t[0]=e,t[1]=n,t[2]=r);let i;t[3]===r?i=t[4]:(i=()=>vh(r),t[3]=r,t[4]=i);let[a]=(0,X.useState)(i),o;return t[5]!==n||t[6]!==a?(o=G(bh.Provider,{value:a,children:n}),t[5]=n,t[6]=a,t[7]=o):o=t[7],o}function Sh(e,t){let n=(0,X.useContext)(bh);if(!n)throw Error(`Missing AgentContext.Provider in the tree`);return Ce(n,e,t)}function Ch(){let e=(0,X.useContext)(bh);if(!e)throw Error(`Missing AgentContext.Provider in the tree`);return e}var wh=(0,X.createContext)(null);function Th(){return X.useContext(wh)}function Eh(){let e=Th();if(e===null)throw Error(`useTimeRange must be used within a TimeRangeContextProvider`);return e}function Dh(){let e=(0,Z.c)(2),{timeRange:t}=Eh(),n;return e[0]===t?n=e[1]:(n=Ad(t),e[0]=t,e[1]=n),n}function Oh({storedLastNTimeRangeKey:e,now:t}){return Ed(e)?{timeRangeKey:e,...wd(e,t)}:{timeRangeKey:`7d`,...wd(`7d`,t)}}function kh(e){let t=(0,Z.c)(37),{children:n}=e,[r,i]=Yn(),a=_i(Mh),o=_i(jh),[s,c]=(0,X.useState)(Ah),l,u,d,f,p;t[0]!==r||t[1]!==a||t[2]!==s?(p=Od(r,s),d=p??Oh({storedLastNTimeRangeKey:a,now:s}),f=d.start?.getTime(),l=d.start?.toISOString(),u=d.end?.toISOString(),t[0]=r,t[1]=a,t[2]=s,t[3]=l,t[4]=u,t[5]=d,t[6]=f,t[7]=p):(l=t[3],u=t[4],d=t[5],f=t[6],p=t[7]);let m=u,h;t[8]!==m||t[9]!==l?(h={start:l,end:m},t[8]=m,t[9]=l,t[10]=h):h=t[10];let g=h,_;t[11]!==i||t[12]!==o?(_=e=>{(0,X.startTransition)(()=>{i(t=>kd({searchParams:t,timeRange:e}),{replace:!0}),Ed(e.timeRangeKey)&&(o(e.timeRangeKey),c(Date.now()))})},t[11]=i,t[12]=o,t[13]=_):_=t[13];let v=_,y;t[14]===v?y=t[15]:(y=e=>{v({timeRangeKey:`custom`,start:e.start,end:e.end})},t[14]=v,t[15]=y);let b=y,x,S;t[16]!==r||t[17]!==i||t[18]!==d||t[19]!==p?(x=()=>{if(p!=null)return;let e=kd({searchParams:r,timeRange:d});e.toString()!==r.toString()&&i(e,{replace:!0})},S=[p,r,i,d],t[16]=r,t[17]=i,t[18]=d,t[19]=p,t[20]=x,t[21]=S):(x=t[20],S=t[21]),(0,X.useEffect)(x,S);let C;t[22]===d.timeRangeKey?C=t[23]:(C=()=>{if(!Ed(d.timeRangeKey))return;let e=d.timeRangeKey,t=window.setTimeout(()=>{c(Date.now())},Td(e));return()=>{window.clearTimeout(t)}},t[22]=d.timeRangeKey,t[23]=C);let w;t[24]!==d.timeRangeKey||t[25]!==f?(w=[d.timeRangeKey,f],t[24]=d.timeRangeKey,t[25]=f,t[26]=w):w=t[26],(0,X.useEffect)(C,w);let T;t[27]===v?T=t[28]:(T={setTimeRange:v},t[27]=v,t[28]=T),Ph(T);let E;t[29]!==b||t[30]!==v||t[31]!==d||t[32]!==g?(E={timeRange:d,timeRangeISOStrings:g,setTimeRange:v,setCustomTimeRange:b},t[29]=b,t[30]=v,t[31]=d,t[32]=g,t[33]=E):E=t[33];let D;return t[34]!==n||t[35]!==E?(D=G(wh.Provider,{value:E,children:n}),t[34]=n,t[35]=E,t[36]=D):D=t[36],D}function Ah(){return Date.now()}function jh(e){return e.setLastNTimeRangeKey}function Mh(e){return e.lastNTimeRangeKey}function Nh(e){if(e===void 0||e.trim()===``)return;let t=new Date(e);if(Number.isNaN(t.getTime()))throw Error(`Invalid ISO datetime: ${e}`);return t}function Ph({setTimeRange:e}){let t=Ch(),n=(0,X.useEffectEvent)(async t=>{if(t.timeRangeKey!==`custom`)return e({timeRangeKey:t.timeRangeKey,...wd(t.timeRangeKey)}),{ok:!0,output:`Set time range to ${t.timeRangeKey}.`};try{let n=Nh(t.startTime),r=Nh(t.endTime);return n===void 0&&r===void 0?{ok:!1,error:`Custom time range requires at least one of startTime or endTime.`}:n!==void 0&&r!==void 0&&n>r?{ok:!1,error:`Custom time range startTime must be before endTime.`}:(e({timeRangeKey:`custom`,start:n,end:r}),{ok:!0,output:`Set custom time range from ${n?.toISOString()??`open start`} to ${r?.toISOString()??`open end`}.`})}catch(e){return{ok:!1,error:e instanceof Error?e.message:`Invalid time range.`}}});(0,X.useEffect)(()=>{let{registerClientAction:e,unregisterClientAction:r}=t.getState();return e(tf,e=>n(e)),()=>{r(tf)}},[t])}function Fh(e){let t=(0,Z.c)(10),n;t[0]===e?n=t[1]:(n=e===void 0?{}:e,t[0]=e,t[1]=n);let{once:r,rootMargin:i,scrollMargin:a}=n,o=r!==void 0&&r,[s,c]=(0,X.useState)(!1),[l,u]=(0,X.useState)(!1);s&&!l&&u(!0);let d;t[2]!==o||t[3]!==i||t[4]!==a?(d=e=>{if(e==null)return Ih;if(!o){let t=e.getBoundingClientRect(),n=t.width>0||t.height>0,r=t.bottom>=0&&t.top<=window.innerHeight&&t.right>=0&&t.left<=window.innerWidth;n&&r&&c(!0)}let t=new IntersectionObserver(e=>{let n=e[e.length-1];(0,X.startTransition)(()=>c(n.isIntersecting)),o&&n.isIntersecting&&t.disconnect()},{rootMargin:i,scrollMargin:a});return t.observe(e),()=>t.disconnect()},t[2]=o,t[3]=i,t[4]=a,t[5]=d):d=t[5];let f=d,p;return t[6]!==l||t[7]!==s||t[8]!==f?(p={ref:f,isVisible:s,hasBeenVisible:l},t[6]=l,t[7]=s,t[8]=f,t[9]=p):p=t[9],p}function Ih(){}var Lh=(0,X.createContext)(!0);function Rh(e){let t=(0,X.useContext)(Lh),[n,r]=(0,X.useState)(e);return t&&n!==e&&r(e),n}var zh=Fe(),Bh=500;function Vh(e,t){let n=(0,Z.c)(5),r=t===void 0?Bh:t,i;n[0]===e?i=n[1]:(i=t=>{try{e(JSON.parse(t))}catch{}},n[0]=e,n[1]=i);let a;return n[2]!==r||n[3]!==i?(a=(0,zh.debounce)(i,r),n[2]=r,n[3]=i,n[4]=a):a=n[4],a}function Hh(e,t){let n=(0,Z.c)(6),r=(0,X.useRef)(null),i,a;n[0]===e?(i=n[1],a=n[2]):(i=()=>{r.current=e},a=[e],n[0]=e,n[1]=i,n[2]=a),(0,X.useEffect)(i,a);let o,s;n[3]===t?(o=n[4],s=n[5]):(o=()=>{if(typeof t!=`number`)return;let e=t,n=function(){r.current?.()},i=setInterval(n,e),a=function(){document.visibilityState===`hidden`?i!=null&&(clearInterval(i),i=null):i??=(n(),setInterval(n,e))};return document.addEventListener(`visibilitychange`,a),()=>{i!=null&&clearInterval(i),document.removeEventListener(`visibilitychange`,a)}},s=[t],n[3]=t,n[4]=o,n[5]=s),(0,X.useEffect)(o,s)}var Uh=.05,Wh=({word:e,theme:t})=>{let n=e.charCodeAt(0),r=Re(n%26/26),i=t===`light`?3:5,a=t===`light`?`#fdfdfd`:`#0E0E0E`,o=je(r,a);for(;o<i;)r=t===`light`?se(Uh,r):ie(Uh,r),o=je(r,a);return r},Gh=e=>{let t=(0,Z.c)(3),{theme:n}=Pr(),r;return t[0]!==n||t[1]!==e?(r=Wh({word:e,theme:n}),t[0]=n,t[1]=e,t[2]=r):r=t[2],r};function Kh(e,t){let n=new Intl.DateTimeFormat(e,{...t});return e=>n.format(e)}function qh(e){let{locale:t,timeZone:n}=e;return Kh(t,{year:`numeric`,month:`2-digit`,day:`2-digit`,hour:`2-digit`,minute:`2-digit`,second:`2-digit`,hour12:!0,timeZone:n})}function Jh(e){let{locale:t,timeZone:n}=e;return Kh(t,{hour:`2-digit`,minute:`2-digit`,hour12:!0,timeZone:n})}function Yh(e){let{locale:t,timeZone:n}=e;return Kh(t,{year:`numeric`,month:`2-digit`,day:`2-digit`,hour:`2-digit`,minute:`2-digit`,hour12:!0,timeZone:n})}function Xh(e){let t=Yh(e);return e=>e.start&&e.end?`${t(e.start)} - ${t(e.end)}`:e.start?`From ${t(e.start)}`:e.end?`Until ${t(e.end)}`:`All Time`}function Zh(e){let{timeZone:t,locale:n}=e;return Intl.DateTimeFormat(n,{timeZoneName:`short`,timeZone:t}).formatToParts().find(e=>e.type===`timeZoneName`)?.value}function Qh(e,t=Date.now()){if(e===0)return``;let n=t-e;return n<216e5?new Date(e).toLocaleTimeString(void 0,{hour:`numeric`,minute:`2-digit`}):n<864e5?`${Math.floor(n/ua)}h`:`${Math.floor(n/da)}d`}function $h(e){return new Intl.DateTimeFormat(e,{day:`2-digit`,month:`2-digit`,year:`numeric`}).formatToParts(new Date).map(e=>{switch(e.type){case`day`:return`dd`;case`month`:return`mm`;case`year`:return`yyyy`;case`literal`:return e.value;default:return``}}).join(``)}function eg(){let e=(0,Z.c)(2),{locale:t}=et(),n;return e[0]===t?n=e[1]:(n=$h(t),e[0]=t,e[1]=n),n}var tg=e=>{let t=(0,Z.c)(3),[n,r]=(0,X.useState)(null),i,a;return t[0]===e?(i=t[1],a=t[2]):(i=()=>{if(!e.current)return;let t=new ResizeObserver(e=>{if(!e||e.length===0)return;let{width:t,height:n}=e[0].contentRect;r({width:t,height:n})});return t.observe(e.current),()=>{t.disconnect()}},a=[e],t[0]=e,t[1]=i,t[2]=a),(0,X.useEffect)(i,a),n};function ng(){let e=(0,Z.c)(10),t=_i(rg),n,r,i,a;if(e[0]!==t){let o=t??ci();n=qh({locale:si(),timeZone:o}),r=Jh({locale:si(),timeZone:o}),i=Yh({locale:si(),timeZone:o}),a=Xh({locale:si(),timeZone:o}),e[0]=t,e[1]=n,e[2]=r,e[3]=i,e[4]=a}else n=e[1],r=e[2],i=e[3],a=e[4];let o;return e[5]!==n||e[6]!==r||e[7]!==i||e[8]!==a?(o={fullTimeFormatter:n,shortTimeFormatter:r,shortDateTimeFormatter:i,timeRangeFormatter:a},e[5]=n,e[6]=r,e[7]=i,e[8]=a,e[9]=o):o=e[9],o}function rg(e){return e.displayTimezone}function ig(e){let t=(0,Z.c)(7),n;t[0]===e?n=t[1]:(n=e===void 0?{}:e,t[0]=e,t[1]=n);let{updateIntervalMs:r}=n,i=r===void 0?null:r,[a,o]=(0,X.useState)(ag),s,c;t[2]===i?(s=t[3],c=t[4]):(s=()=>{if(typeof i!=`number`)return;let e=setInterval(()=>{o(Date.now())},i);return()=>clearInterval(e)},c=[i],t[2]=i,t[3]=s,t[4]=c),(0,X.useEffect)(s,c);let l;return t[5]===a?l=t[6]:(l={nowEpochMs:a},t[5]=a,t[6]=l),l}function ag(){return Date.now()}function og(e){let t=(0,Z.c)(2),n;return t[0]===e?n=t[1]:(n=Np(e),t[0]=e,t[1]=n),n}var sg=`https://pypi.org/pypi/arize-phoenix/json`,cg=null;function lg(){return cg??=fetch(sg).then(e=>e.ok?e.json():null).then(e=>{let t=e?.info?.version;return typeof t==`string`?t:null}).catch(()=>null).then(e=>(e??(cg=null),e)),cg}function ug(){let e=(0,Z.c)(2),[t,n]=(0,X.useState)(null),r,i;return e[0]===Symbol.for(`react.memo_cache_sentinel`)?(r=()=>{let e=!0;return lg().then(t=>{e&&n(t)}),()=>{e=!1}},i=[],e[0]=r,e[1]=i):(r=e[0],i=e[1]),(0,X.useEffect)(r,i),t}function dg(e,t){let[n,r]=(0,X.useState)(()=>{try{let n=localStorage.getItem(e);return n?JSON.parse(n):t}catch{return t}});return[n,(0,X.useCallback)(t=>{r(n=>{let r=typeof t==`function`?t(n):t;try{localStorage.setItem(e,JSON.stringify(r))}catch{}return r})},[e])]}function fg(e){let{query:t,queryRef:n}=e,[r]=(0,bi.useQueryLoader)(t,n);return qe(r,`ownedQueryRef is required when initialized from queryRef`),(0,bi.usePreloadedQuery)(t,r)}function pg(){let e=(0,Z.c)(7),[t,n]=Yn(),r;e[0]===t?r=e[1]:(r=t.getAll(pd),e[0]=t,e[1]=r);let i=r,a;e[2]===n?a=e[3]:(a=e=>{n(t=>{let n=t.getAll(pd),r=typeof e==`function`?e(n):e,i=new URLSearchParams(t);return i.delete(pd),r.forEach(e=>i.append(pd,e)),i},{replace:!0})},e[2]=n,e[3]=a);let o=a,s;return e[4]!==i||e[5]!==o?(s=[i,o],e[4]=i,e[5]=o,e[6]=s):s=e[6],s}function mg(e){let t=(0,Z.c)(4),n;t[0]===e?n=t[1]:(n=t=>{let n=window.matchMedia(e);return n.addEventListener(`change`,t),()=>n.removeEventListener(`change`,t)},t[0]=e,t[1]=n);let r=n,i;return t[2]===e?i=t[3]:(i=()=>window.matchMedia(e).matches,t[2]=e,t[3]=i),(0,X.useSyncExternalStore)(r,i)}function hg(e){let t=(0,Z.c)(49),{start:n,end:r,timeZone:a,isDisabled:o,onCommit:s,autoFocus:c,onBlurWithin:l,onSubmit:u,ref:d}=e,f=(0,X.useRef)(!1),p=(0,X.useRef)(!1),m=r==null,h;t[0]!==n||t[1]!==a?(h=()=>qd(n,a),t[0]=n,t[1]=a,t[2]=h):h=t[2];let[g,_]=(0,X.useState)(h),v;t[3]!==r||t[4]!==a?(v=()=>qd(r,a)??oe(a),t[3]=r,t[4]=a,t[5]=v):v=t[5];let[y,b]=(0,X.useState)(v),x;t[6]!==g||t[7]!==a?(x=g?g.toDate(a):null,t[6]=g,t[7]=a,t[8]=x):x=t[8];let S=x,C;t[9]!==y||t[10]!==a?(C=y?y.toDate(a):null,t[9]=y,t[10]=a,t[11]=C):C=t[11];let T=C,E=!!(S&&T&&S>T),D;t[12]!==r||t[13]!==n||t[14]!==a?(D=()=>{_(qd(n,a)),b(qd(r,a)??oe(a)),f.current=!1,p.current=!1},t[12]=r,t[13]=n,t[14]=a,t[15]=D):D=t[15];let O=D,k;t[16]!==T||t[17]!==m||t[18]!==s||t[19]!==O||t[20]!==S?(k=()=>{if(!f.current)return;let e=m&&!p.current?null:T;if(S&&e&&S>e){O();return}f.current=!1,s({start:S,end:e})},t[16]=T,t[17]=m,t[18]=s,t[19]=O,t[20]=S,t[21]=k):k=t[21];let A=k,j,M;t[22]===A?(j=t[23],M=t[24]):(j=()=>({commit:A}),M=[A],t[22]=A,t[23]=j,t[24]=M),(0,X.useImperativeHandle)(d,j,M);let N;t[25]!==A||t[26]!==l?(N={onBlurWithin:()=>{A(),l?.()}},t[25]=A,t[26]=l,t[27]=N):N=t[27];let{focusWithinProps:P}=$t(N),F=E||void 0,I;t[28]!==A||t[29]!==u?(I=e=>{e.key===`Enter`&&(e.preventDefault(),A(),u?.())},t[28]=A,t[29]=u,t[30]=I):I=t[30];let L,R;t[31]===Symbol.for(`react.memo_cache_sentinel`)?(L=e=>{_(e),f.current=!0},R=G(i,{children:_g}),t[31]=L,t[32]=R):(L=t[31],R=t[32]);let ee;t[33]!==c||t[34]!==o||t[35]!==g?(ee=G(w,{"aria-label":`Start time`,className:`time-range-selector__field`,granularity:`minute`,hideTimeZone:!0,isDisabled:o,autoFocus:c,value:g,onChange:L,children:R}),t[33]=c,t[34]=o,t[35]=g,t[36]=ee):ee=t[36];let te;t[37]===Symbol.for(`react.memo_cache_sentinel`)?(te=G(`span`,{"aria-hidden":!0,className:`time-range-selector__separator`,children:`–`}),t[37]=te):te=t[37];let ne,re;t[38]===Symbol.for(`react.memo_cache_sentinel`)?(ne=e=>{b(e),f.current=!0,p.current=!0},re=G(i,{children:gg}),t[38]=ne,t[39]=re):(ne=t[38],re=t[39]);let ie;t[40]!==y||t[41]!==o?(ie=G(w,{"aria-label":`End time`,className:`time-range-selector__field`,granularity:`minute`,hideTimeZone:!0,isDisabled:o,value:y,onChange:ne,children:re}),t[40]=y,t[41]=o,t[42]=ie):ie=t[42];let ae;return t[43]!==P||t[44]!==F||t[45]!==I||t[46]!==ee||t[47]!==ie?(ae=H(`div`,{className:`time-range-selector__fields`,"data-invalid":F,onKeyDownCapture:I,...P,children:[ee,te,ie]}),t[43]=P,t[44]=F,t[45]=I,t[46]=ee,t[47]=ie,t[48]=ae):ae=t[48],ae}function gg(e){return G(ze,{segment:e})}function _g(e){return G(ze,{segment:e})}var vg=q`
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
`,yg=q`
  /* Fill the popover, which is sized to the field it is anchored to. */
  width: 100%;
`,bg=q`
  padding: var(--global-dimension-size-200) var(--global-dimension-size-150);
`,xg=q`
  width: 100%;
  border-bottom: var(--global-border-size-thin) solid
    var(--global-menu-border-color);
`,Sg=q`
  flex: none;
  font-variant-numeric: tabular-nums;
`,Cg=q`
  width: 100%;
  justify-content: flex-start;
`,wg=`var(--global-dimension-size-4000)`;function Tg(e){let t=(0,Z.c)(85),{value:n,isDisabled:r,onChange:i,size:a}=e,o=a===void 0?`S`:a,{timeRangeKey:s,start:c,end:l}=n,u=(0,X.useRef)(null),d=(0,X.useRef)(null),p=(0,X.useRef)(null),m=(0,X.useRef)(null),h=(0,X.useRef)(null),g=(0,X.useRef)(null),[_,v]=(0,X.useState)(!1),[y,b]=(0,X.useState)(!1),[x,S]=(0,X.useState)(!1),[C,w]=(0,X.useState)(),[E,D]=(0,X.useState)(``),O;t[0]===Symbol.for(`react.memo_cache_sentinel`)?(O={sensitivity:`base`},t[0]=O):O=t[0];let{contains:k}=T(O),A;t[1]===Symbol.for(`react.memo_cache_sentinel`)?(A={isTextInput:!0},t[1]=A):A=t[1];let{isFocusVisible:j}=bt(A),M=y&&j,N;t[2]===Symbol.for(`react.memo_cache_sentinel`)?(N=()=>{v(!1),S(!1),D(``)},t[2]=N):N=t[2];let P=N,F;t[3]===Symbol.for(`react.memo_cache_sentinel`)?(F=()=>{let e=document.activeElement;return e instanceof HTMLElement&&(u.current?.contains(e)||d.current?.contains(e))?e:null},t[3]=F):F=t[3];let I=F,L;t[4]===Symbol.for(`react.memo_cache_sentinel`)?(L=()=>{setTimeout(()=>{I()||(b(!1),P())})},t[4]=L):L=t[4];let R=L,ee;t[5]===Symbol.for(`react.memo_cache_sentinel`)?(ee=()=>{I()?.blur()},t[5]=ee):ee=t[5];let te=ee,ne;t[6]===Symbol.for(`react.memo_cache_sentinel`)?(ne=()=>{te(),b(!1),P()},t[6]=ne):ne=t[6];let re=ne,ie;t[7]===Symbol.for(`react.memo_cache_sentinel`)?(ie=()=>{g.current?.commit(),re()},t[7]=ie):ie=t[7];let ae=ie,oe;t[8]===Symbol.for(`react.memo_cache_sentinel`)?(oe=()=>{v(!0)},t[8]=oe):oe=t[8];let se=oe,ce=!_,le;t[9]===Symbol.for(`react.memo_cache_sentinel`)?(le=e=>{e.target instanceof Node&&d.current?.contains(e.target)||ae()},t[9]=le):le=t[9];let ue;t[10]===ce?ue=t[11]:(ue={ref:u,isDisabled:ce,onInteractOutside:le},t[10]=ce,t[11]=ue),pn(ue);let de;t[12]===E?de=t[13]:(de=e=>{if(e.stopPropagation(),E&&document.activeElement===p.current){D(``);return}ae()},t[12]=E,t[13]=de);let fe;t[14]===Symbol.for(`react.memo_cache_sentinel`)?(fe={capture:!0},t[14]=fe):fe=t[14];let pe;t[15]===y?pe=t[16]:(pe={enabled:y,enableOnFormTags:!0,enableOnContentEditable:!0,preventDefault:!0,eventListenerOptions:fe},t[15]=y,t[16]=pe),ht(`escape`,de,pe);let me=tg(m),he=_i(Og),_e,ve,ye,be,xe;if(t[17]!==he||t[18]!==l||t[19]!==c||t[20]!==s){be=he??ci();let e=si();xe=Zh({locale:e,timeZone:be}),ve=s===`custom`,_e=ve?`Custom`:s;let n=Xh({locale:e,timeZone:be});ye=Ed(s)?Md(s):n({start:c,end:l}),t[17]=he,t[18]=l,t[19]=c,t[20]=s,t[21]=_e,t[22]=ve,t[23]=ye,t[24]=be,t[25]=xe}else _e=t[21],ve=t[22],ye=t[23],be=t[24],xe=t[25];let Se=ye,Ce=Id(E),we=gd.filter(e=>{let{key:t}=e;return!Ce.includes(t)}),Te;t[26]===c?Te=t[27]:(Te=c?.getTime()??``,t[26]=c,t[27]=Te);let Ee;t[28]===l?Ee=t[29]:(Ee=l?.getTime()??``,t[28]=l,t[29]=Ee);let De=`${s}|${Te}|${Ee}|${be}`,Oe=me?.width,ke=`${y}|${De}|${Se}|${_e}|${xe??``}`,Ae=_&&C!=null,je;t[30]!==r||t[31]!==y?(je=e=>{if(r||y)return;let t=h.current,n=e.target instanceof Node&&t?.contains(e.target);!t||n||(e.preventDefault(),t.focus())},t[30]=r,t[31]=y,t[32]=je):je=t[32];let Me=je,Ne;t[33]===_?Ne=t[34]:(Ne=()=>{let e=_?u.current?.offsetWidth:void 0,t=e?`${e}px`:void 0;w(e=>e===t?e:t)},t[33]=_,t[34]=Ne);let Pe;t[35]!==_||t[36]!==ke?(Pe=[_,ke],t[35]=_,t[36]=ke,t[37]=Pe):Pe=t[37],(0,X.useLayoutEffect)(Ne,Pe);let Fe,Ie;t[38]!==x||t[39]!==Ae?(Fe=()=>{!Ae||x||p.current?.focus()},Ie=[Ae,x],t[38]=x,t[39]=Ae,t[40]=Fe,t[41]=Ie):(Fe=t[40],Ie=t[41]),(0,X.useLayoutEffect)(Fe,Ie);let Le=r||void 0,Re=M||void 0,ze=_||void 0,Be=ve?`info`:`default`,z;t[42]!==_e||t[43]!==Be?(z=G(rs,{size:`S`,variant:Be,css:Sg,children:_e}),t[42]=_e,t[43]=Be,t[44]=z):z=t[44];let Ve=_||Oe==null?`auto`:Oe,He=y?wg:void 0,Ue;t[45]!==Ve||t[46]!==He?(Ue={width:Ve,minWidth:He},t[45]=Ve,t[46]=He,t[47]=Ue):Ue=t[47];let We;t[48]!==l||t[49]!==De||t[50]!==r||t[51]!==y||t[52]!==i||t[53]!==c||t[54]!==be||t[55]!==Se?(We=G(`div`,{ref:m,className:`time-range-selector__value-measure`,children:y?G(hg,{ref:g,start:c,end:l,timeZone:be,isDisabled:r,autoFocus:!0,onBlurWithin:R,onSubmit:re,onCommit:e=>i({timeRangeKey:`custom`,...e})},De):G(`button`,{ref:h,type:`button`,className:`time-range-selector__value`,disabled:r,onFocus:()=>{r||(b(!0),se())},children:Se})}),t[48]=l,t[49]=De,t[50]=r,t[51]=y,t[52]=i,t[53]=c,t[54]=be,t[55]=Se,t[56]=We):We=t[56];let Ge;t[57]!==Ue||t[58]!==We?(Ge=G(`div`,{className:`time-range-selector__value-shell`,style:Ue,children:We}),t[57]=Ue,t[58]=We,t[59]=Ge):Ge=t[59];let Ke;t[60]===xe?Ke=t[61]:(Ke=xe&&G(V,{size:`XS`,color:`text-500`,className:`time-range-selector__timezone`,children:xe}),t[60]=xe,t[61]=Ke);let B;t[62]!==Me||t[63]!==o||t[64]!==Le||t[65]!==Re||t[66]!==ze||t[67]!==z||t[68]!==Ge||t[69]!==Ke?(B=H(`div`,{ref:u,className:`time-range-selector`,css:vg,"data-size":o,"data-disabled":Le,"data-focus-visible":Re,"data-presets-open":ze,role:`group`,"aria-label":`Time range`,onPointerDown:Me,children:[z,Ge,Ke]}),t[62]=Me,t[63]=o,t[64]=Le,t[65]=Re,t[66]=ze,t[67]=z,t[68]=Ge,t[69]=Ke,t[70]=B):B=t[70];let qe=qn,Je;t[71]===Symbol.for(`react.memo_cache_sentinel`)?(Je=e=>{e||P()},t[71]=Je):Je=t[71];let Ye=x?`bottom end`:`bottom start`,Xe=x?`max-content`:C,Ze=x?C:void 0,Qe;t[72]!==Xe||t[73]!==Ze?(Qe={width:Xe,minWidth:Ze,overflow:`hidden`,transition:`none`,animation:`none`,transform:`translateY(0)`,opacity:1},t[72]=Xe,t[73]=Ze,t[74]=Qe):Qe=t[74];let $e=x?G(Qd,{value:{start:c,end:l},timeZone:be,onCancel:()=>S(!1),onApply:e=>{b(!1),P(),i({timeRangeKey:`custom`,...e})}}):H(W,{children:[H(gn,{filter:k,children:[H(Ss,{"aria-label":`Search time range presets`,size:`M`,variant:`quiet`,value:E,onChange:D,css:xg,children:[G(bs,{}),G(ge,{ref:p,placeholder:`Search or type "25m"`,onBlur:R})]}),H(yc,{"aria-label":`time range preset selection`,selectionMode:`single`,selectedKeys:ve?[]:[s],css:yg,renderEmptyState:Dg,onSelectionChange:e=>{let t=e===`all`?void 0:e.keys().next().value,n=Ed(t)?t:Ed(s)?s:void 0;if(b(!1),!n){P();return}let r=wd(n);P(),i({timeRangeKey:n,...r})},children:[Ce.map(e=>G(f,{id:e,textValue:E,children:Md(e)},e)),we.map(Eg)]})]}),G(Ka,{children:G(Nt,{size:`S`,variant:`quiet`,css:Cg,leadingVisual:G(U,{svg:G(on,{})}),onPress:()=>S(!0),children:`Pick from a calendar`})})]}),et;t[75]!==qe||t[76]!==Ae||t[77]!==Je||t[78]!==Ye||t[79]!==Qe||t[80]!==$e?(et=G(qe,{ref:d,triggerRef:u,isOpen:Ae,onOpenChange:Je,isNonModal:!0,isKeyboardDismissDisabled:!0,placement:Ye,offset:2,style:Qe,children:$e}),t[75]=qe,t[76]=Ae,t[77]=Je,t[78]=Ye,t[79]=Qe,t[80]=$e,t[81]=et):et=t[81];let tt;return t[82]!==B||t[83]!==et?(tt=H(W,{children:[B,et]}),t[82]=B,t[83]=et,t[84]=tt):tt=t[84],tt}function Eg(e){let{key:t,label:n}=e;return G(f,{id:t,children:n},t)}function Dg(){return G(`div`,{css:bg,children:`No matching time ranges`})}function Og(e){return e.displayTimezone}var kg=Gt`
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.35;
  }
`,Ag=q`
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
`,jg=q`
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
      animation: ${kg} 3s ease-in-out infinite;
    }
  }

  @media (prefers-reduced-motion: reduce) {
    &[data-selected="true"]::before {
      animation: none;
    }
  }
`;function Mg(e){let t=(0,Z.c)(13),{label:n,icon:r,size:i,isDisabled:a,onPress:o}=e,s;t[0]===r?s=t[1]:(s=G(U,{svg:r}),t[0]=r,t[1]=s);let c;t[2]!==a||t[3]!==n||t[4]!==o||t[5]!==i||t[6]!==s?(c=G(Nt,{size:i,variant:`quiet`,css:jg,"aria-label":n,isDisabled:a,leadingVisual:s,onPress:o}),t[2]=a,t[3]=n,t[4]=o,t[5]=i,t[6]=s,t[7]=c):c=t[7];let l;t[8]===n?l=t[9]:(l=G(oa,{children:n}),t[8]=n,t[9]=l);let u;return t[10]!==c||t[11]!==l?(u=H(Te,{children:[c,l]}),t[10]=c,t[11]=l,t[12]=u):u=t[12],u}function Ng(e){let t=(0,Z.c)(48),{value:n,onChange:r,isLive:i,onIsLiveChange:a,isDisabled:o,size:s}=e,c=i!==void 0&&i,l=s===void 0?`S`:s,u=n.start!=null,d=c?`Stop live streaming`:`Resume live streaming`,f=n.end==null,p;t[0]===r?p=t[1]:(p=e=>{e&&r(e)},t[0]=r,t[1]=p);let m=p,h=o||void 0,g;t[2]===Symbol.for(`react.memo_cache_sentinel`)?(g=G(Hn,{}),t[2]=g):g=t[2];let _=o||!u,v;t[3]!==m||t[4]!==n?(v=()=>m(Hd({value:n})),t[3]=m,t[4]=n,t[5]=v):v=t[5];let y;t[6]!==l||t[7]!==_||t[8]!==v?(y=G(Mg,{label:`Pan back in time`,icon:g,size:l,isDisabled:_,onPress:v}),t[6]=l,t[7]=_,t[8]=v,t[9]=y):y=t[9];let b;t[10]===Symbol.for(`react.memo_cache_sentinel`)?(b=G(Kn,{}),t[10]=b):b=t[10];let x=o||!u,S;t[11]!==m||t[12]!==n?(S=()=>m(Gd({value:n})),t[11]=m,t[12]=n,t[13]=S):S=t[13];let C;t[14]!==l||t[15]!==S||t[16]!==x?(C=G(Mg,{label:`Zoom out`,icon:b,size:l,isDisabled:x,onPress:S}),t[14]=l,t[15]=S,t[16]=x,t[17]=C):C=t[17];let w;t[18]!==o||t[19]!==c||t[20]!==d||t[21]!==a||t[22]!==l?(w=a&&H(Te,{children:[G(sc,{size:l,className:`time-range-controls__live-toggle`,css:jg,"aria-label":d,isSelected:c,isDisabled:o,leadingVisual:G(U,{svg:G(c?ot:bn,{})}),onChange:a}),G(oa,{children:d})]}),t[18]=o,t[19]=c,t[20]=d,t[21]=a,t[22]=l,t[23]=w):w=t[23];let T;t[24]===Symbol.for(`react.memo_cache_sentinel`)?(T=G(_n,{}),t[24]=T):T=t[24];let E=o||!u,D;t[25]!==m||t[26]!==n?(D=()=>m(Wd({value:n})),t[25]=m,t[26]=n,t[27]=D):D=t[27];let O;t[28]!==l||t[29]!==E||t[30]!==D?(O=G(Mg,{label:`Zoom in`,icon:T,size:l,isDisabled:E,onPress:D}),t[28]=l,t[29]=E,t[30]=D,t[31]=O):O=t[31];let k;t[32]===Symbol.for(`react.memo_cache_sentinel`)?(k=G(Xn,{}),t[32]=k):k=t[32];let A=o||!u||f,j;t[33]!==m||t[34]!==n?(j=()=>m(Ud({value:n})),t[33]=m,t[34]=n,t[35]=j):j=t[35];let M;t[36]!==l||t[37]!==A||t[38]!==j?(M=G(Mg,{label:`Pan forward in time`,icon:k,size:l,isDisabled:A,onPress:j}),t[36]=l,t[37]=A,t[38]=j,t[39]=M):M=t[39];let N;return t[40]!==l||t[41]!==C||t[42]!==w||t[43]!==O||t[44]!==M||t[45]!==h||t[46]!==y?(N=H(`div`,{className:`time-range-controls`,css:Ag,role:`group`,"aria-label":`Time range controls`,"data-size":l,"data-disabled":h,children:[y,C,w,O,M]}),t[40]=l,t[41]=C,t[42]=w,t[43]=O,t[44]=M,t[45]=h,t[46]=y,t[47]=N):N=t[47],N}function Pg(e){let t=(0,Z.c)(4),{size:n}=e,r=n===void 0?`S`:n,{timeRange:i,setTimeRange:a}=Eh(),o;return t[0]!==a||t[1]!==r||t[2]!==i?(o=G(Tg,{value:i,onChange:a,size:r}),t[0]=a,t[1]=r,t[2]=i,t[3]=o):o=t[3],o}function Fg(e){let t=(0,Z.c)(4),{timeRange:n,setTimeRange:r}=Eh(),i;return t[0]!==e||t[1]!==r||t[2]!==n?(i=G(Ng,{...e,value:n,onChange:r}),t[0]=e,t[1]=r,t[2]=n,t[3]=i):i=t[3],i}q`
  display: flex;
  flex-direction: column;
  gap: var(--global-dimension-size-200);
`,q`
  display: flex;
  gap: var(--global-dimension-size-100);
  align-items: start;
  justify-content: end;
  /* Move the button down to align */
  button {
    margin-top: 26px;
  }
`,q`
  width: 100%;
  display: flex;
  justify-content: flex-end;
  gap: var(--global-dimension-size-100);
`,q`
  width: 100%;
  .react-aria-DateInput {
    width: 100%;
    // Eliminate the re-sizing of the DateField as you type
    min-width: 200px;
  }
`;var Ig=Gt`
  to {
    --ai-conic-angle: 405deg;
  }
`,Lg=Gt`
  0%, 100% {
    box-shadow: var(--ai-glow-box-shadow-rest);
  }
  50% {
    box-shadow: var(--ai-glow-box-shadow-strong);
  }
`,Rg=Gt`
  0% {
    -webkit-mask-position: 170% center;
    mask-position: 170% center;
  }

  100% {
    -webkit-mask-position: -70% center;
    mask-position: -70% center;
  }
`,zg=Gt`
  0%, 100% {
    box-shadow: var(--ai-glow-box-shadow-contained-rest);
  }
  50% {
    box-shadow: var(--ai-glow-box-shadow-contained-strong);
  }
`,Bg=Gt`
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
`,Vg=Gt`
  0%, 100% {
    opacity: 0;
  }
  8%, 40% {
    opacity: var(--ai-glow-opacity);
  }
  55% {
    opacity: 0;
  }
`,Hg=q`
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
`,Ug=q`
  -webkit-mask-position: center;
  mask-position: center;
  animation: ${Rg} var(--ai-glow-wipe-continuous-duration)
    linear infinite both var(--ai-glow-wipe-continuous-delay);
`,Wg=q`
  background: conic-gradient(
    from var(--ai-conic-angle),
    var(--ai-gradient-color-start),
    var(--ai-gradient-color-middle),
    var(--ai-gradient-color-end),
    var(--ai-gradient-color-start)
  );
`,Gg=q`
  ${Wg};
  padding: var(--ai-conic-band-stroke-width);
  -webkit-mask:
    linear-gradient(#000 0 0) content-box,
    linear-gradient(#000 0 0);
  mask:
    linear-gradient(#000 0 0) content-box,
    linear-gradient(#000 0 0);
  -webkit-mask-composite: xor;
  mask-composite: exclude;
`,Kg=q`
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
    ${Gg};
    inset: calc(
      -1 * (var(--ai-outline-gap) + var(--ai-conic-band-stroke-width))
    );
    z-index: 2;
    border-radius: calc(
      var(--ai-outline-target-radius) + var(--ai-outline-gap) +
        var(--ai-conic-band-stroke-width)
    );
    opacity: 0.3;
    animation: ${Ig} var(--ai-conic-spin-duration) linear infinite
      paused;
  }

  .ai-outline__glow {
    ${Hg};
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
    ${Ug};
  }

  &[data-state="active"] .ai-outline__glow::before {
    opacity: 0.72;
    animation: ${Lg} var(--ai-glow-wipe-duration) ease-in-out
      infinite;
  }

  &[data-state="eligible"][data-should-flash="true"] .ai-outline__glow {
    animation: ${Bg} var(--ai-glow-wipe-duration)
      var(--ai-glow-wipe-easing) 1;
  }

  &[data-state="eligible"][data-should-flash="true"] .ai-outline__glow::before {
    animation:
      ${Lg} var(--ai-glow-wipe-duration) ease-in-out 1,
      ${Vg} var(--ai-glow-wipe-duration) linear 1;
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
      animation-name: ${zg};
    }

    &[data-state="eligible"][data-should-flash="true"]
      .ai-outline__glow::before {
      animation-name: ${zg}, ${Vg};
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
`;function qg(e){let t=(0,Z.c)(15),{children:n,className:r,css:i,isFullWidth:a,glowMode:o,radius:s,shouldFlash:c,state:l}=e,u=a!==void 0&&a,d=o===void 0?`outer`:o,f=s===void 0?`small`:s,p=c!==void 0&&c,m=l===void 0?`idle`:l,h=m===`eligible`&&p,g;t[0]===i?g=t[1]:(g=q(Kg,i),t[0]=i,t[1]=g);let _=g,v;t[2]===r?v=t[3]:(v=B(`ai-outline`,r),t[2]=r,t[3]=v);let y=u?`true`:void 0,b=h?`true`:void 0,x,S;t[4]===Symbol.for(`react.memo_cache_sentinel`)?(x=G(`span`,{className:`ai-outline__glow`,"aria-hidden":`true`}),S=G(`span`,{className:`ai-outline__stroke`,"aria-hidden":`true`}),t[4]=x,t[5]=S):(x=t[4],S=t[5]);let C;return t[6]!==n||t[7]!==_||t[8]!==d||t[9]!==f||t[10]!==m||t[11]!==v||t[12]!==y||t[13]!==b?(C=H(`div`,{className:v,css:_,"data-full-width":y,"data-glow-mode":d,"data-radius":f,"data-should-flash":b,"data-state":m,children:[x,S,n]}),t[6]=n,t[7]=_,t[8]=d,t[9]=f,t[10]=m,t[11]=v,t[12]=y,t[13]=b,t[14]=C):C=t[14],C}var Jg=(0,X.createContext)(null);function Yg(){return(0,X.useContext)(Jg)??{variant:`grid`}}var Xg=q`
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
`,Zg=q`
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
`,Qg=q`
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
`,$g=q`
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
`;q`
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
`;function e_(e){let t=(0,Z.c)(17),n,r,i,a,o;t[0]===e?(n=t[1],r=t[2],i=t[3],a=t[4],o=t[5]):({children:n,ref:r,variant:a,collapsible:o,...i}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a,t[5]=o);let s=a===void 0?`grid`:a,c=o!==void 0&&o,l;t[6]===s?l=t[7]:(l={variant:s},t[6]=s,t[7]=l);let u=l,d=c||void 0,f;t[8]!==n||t[9]!==r||t[10]!==i||t[11]!==d||t[12]!==s?(f=G(`div`,{ref:r,css:Xg,"data-variant":s,"data-collapsible":d,...i,children:n}),t[8]=n,t[9]=r,t[10]=i,t[11]=d,t[12]=s,t[13]=f):f=t[13];let p;return t[14]!==f||t[15]!==u?(p=G(Jg.Provider,{value:u,children:f}),t[14]=f,t[15]=u,t[16]=p):p=t[16],p}var t_=(0,X.createContext)(null);function n_(){let e=(0,X.useContext)(t_);if(!e)throw Error(`useAttachmentContext must be used within an <Attachment> component`);return e}function r_(e){if(e.type===`context`)return`context`;if(e.type===`source-document`)return`source`;let t=e.mediaType??``;return t.startsWith(`image/`)?`image`:t.startsWith(`video/`)?`video`:t.startsWith(`audio/`)?`audio`:t.startsWith(`application/`)||t.startsWith(`text/`)?`document`:`unknown`}function i_(e){return e.type===`context`?e.label:e.type===`source-document`?e.title||e.filename||`Source`:e.filename||(r_(e)===`image`?`Image`:`Attachment`)}function a_(e){return e.type===`context`?e.detail:void 0}function o_(e){switch(e){case`project`:return G(U,{svg:G(Sn,{})});case`trace`:return G(U,{svg:G(Sn,{})});case`session`:return G(U,{svg:G(Jn,{})});case`span`:return G(U,{svg:G(cn,{})});case`span_filter`:return G(U,{svg:G(sn,{})});case`dataset`:return G(U,{svg:G(vn,{})});case`playground`:return G(U,{svg:G($e,{})});case`code_evaluator`:return G(U,{svg:G(vt,{})});case`llm_evaluator`:return G(U,{svg:G(mt,{})});default:return G(U,{svg:G(en,{})})}}function s_(e){if(e.type===`context`)return e.icon??o_(e.category);switch(r_(e)){case`image`:return G(U,{svg:G(mn,{})});case`video`:return G(U,{svg:G($e,{})});case`audio`:return G(U,{svg:G(Ut,{})});case`document`:return G(U,{svg:G(Xt,{})});case`source`:return G(U,{svg:G(In,{})});default:return G(U,{svg:G(Ut,{})})}}function c_(e){let t=(0,Z.c)(22),n,r,i,a,o;t[0]===e?(n=t[1],r=t[2],i=t[3],a=t[4],o=t[5]):({children:n,ref:a,data:r,onRemove:i,...o}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a,t[5]=o);let{variant:s}=Yg(),{theme:c}=Pr(),l;t[6]===r?l=t[7]:(l=r_(r),t[6]=r,t[7]=l);let u=l,d;t[8]!==r||t[9]!==u||t[10]!==i||t[11]!==s?(d={data:r,mediaCategory:u,variant:s,onRemove:i},t[8]=r,t[9]=u,t[10]=i,t[11]=s,t[12]=d):d=t[12];let f=d,p;t[13]!==n||t[14]!==a||t[15]!==o||t[16]!==c||t[17]!==s?(p=G(`div`,{ref:a,css:Zg,"data-attachment":``,"data-variant":s,"data-theme":c,...o,children:n}),t[13]=n,t[14]=a,t[15]=o,t[16]=c,t[17]=s,t[18]=p):p=t[18];let m;return t[19]!==p||t[20]!==f?(m=G(t_.Provider,{value:f,children:p}),t[19]=p,t[20]=f,t[21]=m):m=t[21],m}function l_(e){let t=(0,Z.c)(16),n,r,i;t[0]===e?(n=t[1],r=t[2],i=t[3]):({ref:r,fallback:n,...i}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i);let{data:a,mediaCategory:o,variant:s}=n_(),c;t[4]!==a||t[5]!==n||t[6]!==o?(c=()=>a.type===`file`&&o===`image`&&typeof a.url==`string`&&a.url?G(`img`,{src:a.url,alt:a.filename??`Image`}):a.type===`file`&&o===`video`&&typeof a.url==`string`&&a.url?G(`video`,{src:a.url,muted:!0}):n??s_(a),t[4]=a,t[5]=n,t[6]=o,t[7]=c):c=t[7];let l=c,u;t[8]===l?u=t[9]:(u=l(),t[8]=l,t[9]=u);let d;return t[10]!==o||t[11]!==r||t[12]!==i||t[13]!==u||t[14]!==s?(d=G(`div`,{ref:r,css:Qg,"data-variant":s,"data-media-category":o,...i,children:u}),t[10]=o,t[11]=r,t[12]=i,t[13]=u,t[14]=s,t[15]=d):d=t[15],d}function u_(e){let t=(0,Z.c)(28),n,r,i;t[0]===e?(n=t[1],r=t[2],i=t[3]):({ref:n,showMediaType:i,...r}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i);let a=i!==void 0&&i,{data:o,variant:s}=n_();if(s===`grid`)return null;let c;t[4]===o?c=t[5]:(c=i_(o),t[4]=o,t[5]=c);let l=c,u,d,f,p,m;t[6]!==o||t[7]!==n?(u=a_(o),d=o.type===`file`||o.type===`source-document`?o.mediaType:void 0,f=n,p=$g,m=B(`attachment-info`,{"attachment-info--with-detail":u}),t[6]=o,t[7]=n,t[8]=u,t[9]=d,t[10]=f,t[11]=p,t[12]=m):(u=t[8],d=t[9],f=t[10],p=t[11],m=t[12]);let h;t[13]===l?h=t[14]:(h=G(`span`,{className:`attachment-info__label`,children:l}),t[13]=l,t[14]=h);let g;t[15]===u?g=t[16]:(g=u?G(`span`,{className:`attachment-info__detail`,children:u}):null,t[15]=u,t[16]=g);let _;t[17]!==d||t[18]!==a?(_=a&&d?G(`span`,{className:`attachment-info__media-type`,children:d}):null,t[17]=d,t[18]=a,t[19]=_):_=t[19];let v;return t[20]!==r||t[21]!==f||t[22]!==p||t[23]!==m||t[24]!==h||t[25]!==g||t[26]!==_?(v=H(`div`,{ref:f,css:p,className:m,...r,children:[h,g,_]}),t[20]=r,t[21]=f,t[22]=p,t[23]=m,t[24]=h,t[25]=g,t[26]=_,t[27]=v):v=t[27],v}var d_=q`
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
`,f_=q`
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
`;function p_(e){let t=(0,Z.c)(27),{selected:n,type:r,label:i,description:a,isFreeformEntry:o,textValue:s,onToggle:c,onTextChange:l}=e,u=(0,X.useRef)(null),d,f;t[0]!==o||t[1]!==n?(d=()=>{n&&o&&u.current&&u.current.focus()},f=[n,o],t[0]=o,t[1]=n,t[2]=d,t[3]=f):(d=t[2],f=t[3]),(0,X.useEffect)(d,f);let p=r===`single`?`option-button__indicator option-button__indicator--radio`:`option-button__indicator option-button__indicator--checkbox`,m;t[4]===Symbol.for(`react.memo_cache_sentinel`)?(m={scale:.98,transition:{type:`tween`,duration:.06}},t[4]=m):m=t[4];let h=r===`single`?`radio`:`checkbox`,g;t[5]===c?g=t[6]:(g=e=>{let t=e.target;t.tagName!==`INPUT`&&t.tagName!==`TEXTAREA`&&(e.key===`Enter`&&(e.metaKey||e.ctrlKey)||(e.key===`Enter`||e.key===` `)&&(e.preventDefault(),c()))},t[5]=c,t[6]=g);let _;t[7]===r?_=t[8]:(_=r===`multi`&&G(`svg`,{viewBox:`0 0 18 18`,"aria-hidden":`true`,children:G(`polyline`,{points:`1 9 7 14 15 4`})}),t[7]=r,t[8]=_);let v;t[9]!==p||t[10]!==_?(v=G(`span`,{className:p,children:_}),t[9]=p,t[10]=_,t[11]=v):v=t[11];let y;t[12]!==a||t[13]!==o||t[14]!==i||t[15]!==l||t[16]!==c||t[17]!==n||t[18]!==s?(y=o?G(`div`,{className:`option-button__text-entry`,onClick:m_,children:G(`input`,{ref:u,type:`text`,className:`option-button__text-input`,value:s||``,placeholder:`Type your own answer…`,onMouseDown:()=>{n||c()},onChange:e=>{n||c(),l?.(e.target.value)},"aria-label":`Type your own answer`})}):H(`div`,{className:`option-button__content`,children:[G(`span`,{className:`option-button__label`,children:i}),a?G(`span`,{className:`option-button__description`,children:a}):null]}),t[12]=a,t[13]=o,t[14]=i,t[15]=l,t[16]=c,t[17]=n,t[18]=s,t[19]=y):y=t[19];let b;return t[20]!==c||t[21]!==n||t[22]!==h||t[23]!==g||t[24]!==v||t[25]!==y?(b=H(ye.div,{css:f_,"data-selected":n,onClick:c,whileTap:m,role:h,"aria-checked":n,tabIndex:0,onKeyDown:g,children:[v,y]}),t[20]=c,t[21]=n,t[22]=h,t[23]=g,t[24]=v,t[25]=y,t[26]=b):b=t[26],b}function m_(e){return e.stopPropagation()}var h_=`__freeform__`,g_=.04,__={enter:e=>({x:e>0?120:-120,opacity:0}),center:{x:0,opacity:1},exit:e=>({x:e>0?-120:120,opacity:0})},v_={type:`spring`,stiffness:400,damping:32,mass:.8},y_={type:`spring`,stiffness:700,damping:24,mass:.6};function b_({questions:e,onProgressStateChange:t,onSubmit:n,onCancel:r}){let[i,a]=(0,X.useState)({}),[o,s]=(0,X.useState)({}),[c,l]=(0,X.useState)(0),[u,d]=(0,X.useState)(0),f=(0,X.useRef)(!0),p=(0,X.useEffectEvent)(e=>{t?.(e)}),m=e.length,h=e[c];(0,X.useEffect)(()=>{let e=setTimeout(()=>{f.current=!1},500);return()=>clearTimeout(e)},[]),(0,X.useEffect)(()=>{p({answers:{},freeformTexts:{},currentIndex:0})},[]);let g=e=>{d(e>c?1:-1),l(e),t?.({answers:i,freeformTexts:o,currentIndex:e})},_=(e,t,n)=>{let r=i[e]||[],o;o=n===`single`?r.includes(t)?[]:[t]:r.includes(t)?r.filter(e=>e!==t):[...r,t],a(t=>({...t,[e]:o}))},v=(e,t)=>{a(n=>({...n,[e]:t}))},y=()=>{t?.({answers:i,freeformTexts:o,currentIndex:c}),n({answers:i,freeformTexts:o})},b=()=>{let t=i[e[c].id];((Array.isArray(t)?t.length>0:t)||e[c].allow_skip===!0)&&(c===m-1?y():g(c+1))},x=e=>{if(e.key!==`Enter`||e.nativeEvent.isComposing)return;let t=e.target;if(t.tagName===`TEXTAREA`)return;let n=t.tagName===`INPUT`&&t.type===`text`;(e.metaKey||e.ctrlKey||n)&&(e.preventDefault(),b())},S=e=>{e.key!==`Enter`||e.nativeEvent.isComposing||e.shiftKey||(e.preventDefault(),b())},C=f.current?g_:0,w=C,T=2*C,E=e=>(3+e)*C,D=3*C,O=i[h.id],k=Array.isArray(O)?O.length>0:!!O,A=h.allow_skip===!0,j=k||A;return G(Rt,{autoFocus:!0,contain:!0,restoreFocus:!0,children:H(`div`,{css:d_,onKeyDown:x,children:[H(ye.div,{className:`elicitation__header`,initial:{opacity:0,y:8},animate:{opacity:1,y:0},transition:{...y_,delay:w,opacity:{duration:.12,delay:w}},children:[H(`span`,{className:`elicitation__step-label`,children:[`Question `,c+1,` of `,m]}),G(`div`,{className:`elicitation__dots`,children:e.map((e,t)=>G(`button`,{className:`elicitation__dot ${t===c?`elicitation__dot--active`:`elicitation__dot--inactive`}`,onClick:()=>g(t),"aria-label":`Go to question ${t+1}`},t))})]}),G(`div`,{className:`elicitation__body`,children:G(I,{custom:u,mode:`popLayout`,children:H(ye.div,{custom:u,variants:__,initial:!f.current&&`enter`,animate:`center`,exit:`exit`,transition:v_,className:`elicitation__question-content`,children:[G(ye.div,{className:`elicitation__prompt`,initial:{opacity:0,y:-8},animate:{opacity:1,y:0},transition:{...y_,delay:T,opacity:{duration:.12,delay:T}},children:h.prompt}),h.type===`freeform`?G(ye.div,{initial:{opacity:0,y:-8},animate:{opacity:1,y:0},transition:{...y_,delay:D,opacity:{duration:.12,delay:D}},children:G(`textarea`,{className:`elicitation__freeform`,value:i[h.id]||``,onChange:e=>v(h.id,e.target.value),onKeyDown:S,placeholder:`Type your response… (Enter to submit, Shift+Enter for newline)`,"aria-label":h.prompt})}):H(`div`,{className:`elicitation__options`,children:[h.options?.map((e,t)=>G(ye.div,{initial:{opacity:0,y:-8},animate:{opacity:1,y:0},transition:{...y_,delay:E(t),opacity:{duration:.12,delay:E(t)}},children:G(p_,{selected:(i[h.id]||[]).includes(e.id),type:h.type,label:e.label,description:e.description,onToggle:()=>_(h.id,e.id,h.type)})},e.id)),h.allow_freeform?G(ye.div,{initial:{opacity:0,y:-8},animate:{opacity:1,y:0},transition:{...y_,delay:E(h.options?.length??0),opacity:{duration:.12,delay:E(h.options?.length??0)}},children:G(p_,{selected:(i[h.id]||[]).includes(h_),type:h.type,label:`Type your own answer`,isFreeformEntry:!0,textValue:o[h.id],onToggle:()=>_(h.id,h_,h.type),onTextChange:e=>s(t=>({...t,[h.id]:e}))})},h_):null]})]},h.id)})}),H(ye.div,{className:`elicitation__nav`,initial:{opacity:0,y:8},animate:{opacity:1,y:0},transition:{...y_,delay:0,opacity:{duration:.12,delay:0}},children:[H(`div`,{className:`elicitation__nav-group`,children:[r&&G(Nt,{size:`S`,variant:`default`,onPress:r,children:`Cancel`}),G(Nt,{size:`S`,variant:`default`,isDisabled:c===0,onPress:()=>g(c-1),children:`Back`})]}),c===m-1?G(Nt,{size:`S`,variant:`primary`,isDisabled:!j,onPress:y,children:`Submit`}):G(Nt,{size:`S`,variant:k?`primary`:`default`,isDisabled:!j,onPress:()=>g(c+1),children:k?`Next`:`Skip`})]})]})})}var x_=(0,X.createContext)(null),S_=q`
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
`,C_=q`
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
`,w_=q`
  display: flex;
  align-items: center;
  gap: var(--global-dimension-size-50);
  margin-left: auto;
`,T_=q`
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
`,E_=q`
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
`;q`
  display: flex;
  align-items: center;
  gap: var(--global-dimension-size-50);
`,q`
  color: var(--global-text-color-500);
  font-size: var(--global-font-size-s);
  white-space: nowrap;
  user-select: none;
`;function D_(e){let t=(0,Z.c)(15),n,r,i,a;t[0]===e?(n=t[1],r=t[2],i=t[3],a=t[4]):({children:n,ref:i,from:r,...a}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a);let o;t[5]===r?o=t[6]:(o={from:r},t[5]=r,t[6]=o);let s;t[7]!==n||t[8]!==r||t[9]!==i||t[10]!==a?(s=G(`div`,{ref:i,css:S_,"data-from":r,...a,children:n}),t[7]=n,t[8]=r,t[9]=i,t[10]=a,t[11]=s):s=t[11];let c;return t[12]!==o||t[13]!==s?(c=G(x_.Provider,{value:o,children:s}),t[12]=o,t[13]=s,t[14]=c):c=t[14],c}function O_(e){let t=(0,Z.c)(8),n,r,i;t[0]===e?(n=t[1],r=t[2],i=t[3]):({children:n,ref:r,...i}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i);let a;return t[4]!==n||t[5]!==r||t[6]!==i?(a=G(`div`,{ref:r,css:C_,...i,children:n}),t[4]=n,t[5]=r,t[6]=i,t[7]=a):a=t[7],a}function k_(e,t){for(let n of e.tokenColors)if((Array.isArray(n.scope)?n.scope:n.scope?[n.scope]:[]).includes(t))return n.settings.foreground}function A_(e){let t=e.colors,n=t=>k_(e,t),r=[{tag:[z.standard(z.tagName),z.tagName],color:n(`entity.name.tag`)},{tag:[z.comment],color:n(`comment`)},{tag:[z.bracket,z.punctuation,z.separator,z.derefOperator],color:n(`punctuation`)},{tag:[z.className,z.typeName,z.namespace,z.definition(z.typeName)],color:n(`entity.name.type`)},{tag:[z.propertyName,z.attributeName],color:n(`entity.other.attribute-name`)},{tag:[z.function(z.variableName),z.function(z.propertyName),z.macroName],color:n(`entity.name.function`)},{tag:[z.variableName,z.definition(z.variableName)],color:n(`variable`)},{tag:[z.number,z.bool,z.atom],color:n(`constant.numeric`)},{tag:[z.keyword,z.modifier,z.operatorKeyword,z.controlKeyword],color:n(`keyword`)},{tag:[z.string,z.special(z.string),z.docString],color:n(`string`)},{tag:[z.operator],color:n(`keyword.operator`)},{tag:[z.constant(z.variableName),z.literal],color:n(`constant`)},{tag:[z.regexp],color:n(`string.regexp`)},{tag:[z.escape],color:n(`constant.character.escape`)},{tag:[z.heading,z.strong],color:n(`markup.heading`),fontWeight:`bold`},{tag:[z.emphasis],fontStyle:`italic`},{tag:[z.link,z.url],color:n(`markup.underline.link.markdown`),textDecoration:`underline`},{tag:[z.strikethrough],textDecoration:`line-through`},{tag:[z.invalid],color:t[`editor.foreground`]}];return Ue({theme:e.type,settings:{background:t[`editor.background`],foreground:t[`editor.foreground`],caret:t[`editorCursor.foreground`],selection:t[`editor.selectionBackground`],selectionMatch:t[`editor.selectionBackground`],lineHighlight:t[`editor.lineHighlightBackground`],gutterBackground:t[`editor.background`],gutterForeground:t[`editorLineNumber.foreground`],gutterActiveForeground:t[`editorLineNumber.activeForeground`]},styles:r.filter(e=>e.color!=null||e.fontWeight!=null||e.fontStyle!=null||e.textDecoration!=null)})}var j_=A_(le),M_=A_(j);function N_(e){let t=(0,Z.c)(13),n,r;t[0]===e?(n=t[1],r=t[2]):({basicSetup:n,...r}=e,t[0]=e,t[1]=n,t[2]=r);let{theme:i}=Pr(),a=i===`light`?j_:M_,o;bb0:{let e;t[3]===Symbol.for(`react.memo_cache_sentinel`)?(e={lineNumbers:!0,foldGutter:!0,bracketMatching:!0,syntaxHighlighting:!0,highlightActiveLine:!1,highlightActiveLineGutter:!1},t[3]=e):e=t[3];let r=e;if(n){let e;t[4]===n?e=t[5]:(e={...r,...n},t[4]=n,t[5]=e),o=e;break bb0}o=r}let s=o,c=e.value,l;t[6]===Symbol.for(`react.memo_cache_sentinel`)?(l=Ke(),t[6]=l):l=t[6];let u;t[7]===Symbol.for(`react.memo_cache_sentinel`)?(u=[l,Be.lineWrapping,We(Ge())],t[7]=u):u=t[7];let d;return t[8]!==s||t[9]!==a||t[10]!==e.value||t[11]!==r?(d=G(Ve,{value:c,extensions:u,editable:!1,theme:a,...r,basicSetup:s}),t[8]=s,t[9]=a,t[10]=e.value,t[11]=r,t[12]=d):d=t[12],d}function P_(e){let t=(0,Z.c)(6),n;try{let r;if(t[0]!==e){let n=JSON.parse(e);r=JSON.stringify(n,null,2),t[0]=e,t[1]=r}else r=t[1];let i;t[2]===r?i=t[3]:(i={text:r,textType:`json`},t[2]=r,t[3]=i),n=i}catch{let r;t[4]===e?r=t[5]:(r={text:e,textType:`string`},t[4]=e,t[5]=r),n=r}return n}function F_({children:e,preCSS:t}){let{text:n,textType:r}=P_(e);return r===`string`?G(`pre`,{css:q`
          white-space: pre-wrap;
          text-wrap: wrap;
          overflow-wrap: anywhere;
          font-size: var(--global-font-size-s);
          margin: 0;
          ${t}
        `,children:n}):r===`json`?G(N_,{value:n}):dr(r)}var I_=(0,X.createContext)(null);function L_(){let e=(0,Z.c)(1),t=(0,X.useContext)(I_);if(t===null){console.warn(`useMarkdownMode must be used within a MarkdownDisplayProvider`);let n;e[0]===Symbol.for(`react.memo_cache_sentinel`)?(n={mode:`text`,setMode:R_},e[0]=n):n=e[0],t=n}return t}function R_(){}function z_(e){let t=(0,Z.c)(8),n=_i(V_),r=_i(B_),i;t[0]===r?i=t[1]:(i=e=>{(0,X.startTransition)(()=>{r(e)})},t[0]=r,t[1]=i);let a=i,o;t[2]!==n||t[3]!==a?(o={mode:n,setMode:a},t[2]=n,t[3]=a,t[4]=o):o=t[4];let s;return t[5]!==e.children||t[6]!==o?(s=G(I_.Provider,{value:o,children:e.children}),t[5]=e.children,t[6]=o,t[7]=s):s=t[7],s}function B_(e){return e.setMarkdownDisplayMode}function V_(e){return e.markdownDisplayMode}var H_=q`
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
`,U_={code:Fn},W_={CopyIcon:()=>G(lt,{}),CheckIcon:()=>G(En,{}),DownloadIcon:()=>G(jt,{})};function G_(e){let t=(0,Z.c)(7),{children:n,mode:r,renderMode:i,margin:a}=e,o=i===void 0?`static`:i,s=a===void 0?`default`:a,c;t[0]===s?c=t[1]:(c=s===`none`?q`
          margin: 0;
        `:q`
          margin: var(--global-dimension-size-200);
        `,t[0]=s,t[1]=c);let l=c,u;return t[2]!==n||t[3]!==r||t[4]!==o||t[5]!==l?(u=r===`markdown`?G(`div`,{css:[H_,l],children:G(Dn,{components:Rn,controls:{code:{copy:!0,download:!0},table:!1},icons:W_,mode:o,plugins:U_,children:n})}):G(F_,{preCSS:l,children:n}),t[2]=n,t[3]=r,t[4]=o,t[5]=l,t[6]=u):u=t[6],u}function K_(e){let t=(0,Z.c)(5),{children:n,renderMode:r,margin:i}=e,a=i===void 0?`default`:i,{mode:o}=L_(),s;return t[0]!==n||t[1]!==a||t[2]!==o||t[3]!==r?(s=G(G_,{mode:o,renderMode:r,margin:a,children:n}),t[0]=n,t[1]=a,t[2]=o,t[3]=r,t[4]=s):s=t[4],s}function q_(e){return typeof e==`string`?{content:e,position:`top`}:{position:`top`,...e}}function J_(e){let t=(0,Z.c)(22),n,r,i,a,o,s;t[0]===e?(n=t[1],r=t[2],i=t[3],a=t[4],o=t[5],s=t[6]):({children:n,ref:a,label:i,tooltip:s,className:r,...o}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a,t[5]=o,t[6]=s);let c;t[7]!==n||t[8]!==r||t[9]!==i||t[10]!==a||t[11]!==o?(c=G(Jt,{ref:a,css:T_,className:r,"aria-label":i,...o,children:n}),t[7]=n,t[8]=r,t[9]=i,t[10]=a,t[11]=o,t[12]=c):c=t[12];let l=c;if(!s)return l;let u;t[13]===s?u=t[14]:(u=q_(s),t[13]=s,t[14]=u);let{content:d,position:f}=u,p;t[15]===Symbol.for(`react.memo_cache_sentinel`)?(p=G(sa,{}),t[15]=p):p=t[15];let m;t[16]!==d||t[17]!==f?(m=H(oa,{placement:f,children:[p,d]}),t[16]=d,t[17]=f,t[18]=m):m=t[18];let h;return t[19]!==l||t[20]!==m?(h=H(Te,{delay:500,closeDelay:0,children:[l,m]}),t[19]=l,t[20]=m,t[21]=h):h=t[21],h}var Y_=2e3;function X_(e){let t=(0,Z.c)(11),{text:n}=e,[r,i]=(0,X.useState)(!1);if(n.trim().length===0)return null;let a;t[0]===n?a=t[1]:(a=()=>{S(n),i(!0),setTimeout(()=>i(!1),Y_)},t[0]=n,t[1]=a);let o=a,s=r?`Copied`:`Copy message`,c;t[2]===r?c=t[3]:(c=G(r?En:lt,{}),t[2]=r,t[3]=c);let l=r?`success`:`inherit`,u;t[4]!==c||t[5]!==l?(u=G(U,{svg:c,color:l}),t[4]=c,t[5]=l,t[6]=u):u=t[6];let d;return t[7]!==o||t[8]!==s||t[9]!==u?(d=G(J_,{label:`Copy`,tooltip:s,onPress:o,children:u}),t[7]=o,t[8]=s,t[9]=u,t[10]=d):d=t[10],d}function Z_(e){let t=(0,Z.c)(8),n,r,i;t[0]===e?(n=t[1],r=t[2],i=t[3]):({children:n,ref:r,...i}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i);let a;return t[4]!==n||t[5]!==r||t[6]!==i?(a=G(`div`,{ref:r,css:w_,role:`toolbar`,...i,children:n}),t[4]=n,t[5]=r,t[6]=i,t[7]=a):a=t[7],a}function Q_(e){let t=(0,Z.c)(8),n,r,i;t[0]===e?(n=t[1],r=t[2],i=t[3]):({children:n,ref:r,...i}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i);let a;return t[4]!==n||t[5]!==r||t[6]!==i?(a=G(`div`,{ref:r,css:E_,...i,children:n}),t[4]=n,t[5]=r,t[6]=i,t[7]=a):a=t[7],a}(0,X.createContext)(null);var $_=(0,X.createContext)(null);function ev(){let e=(0,X.useContext)($_);if(!e)throw Error(`usePromptInputContext must be used within a <PromptInput> component`);return e}var tv=q`
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
`,nv=q`
  flex: 1 1 auto;
  padding: var(--global-dimension-size-200);
  padding-bottom: var(--global-dimension-size-100);
`,rv=q`
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
`,iv=q`
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--global-dimension-size-100) var(--global-dimension-size-150);
  gap: var(--global-dimension-size-100);
`,av=q`
  display: flex;
  align-items: center;
  gap: var(--global-dimension-size-50);
`,ov=q`
  display: flex;
  align-items: center;
  gap: var(--global-dimension-size-50);
`,sv=q`
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
`;q`
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
`;function cv({children:e,ref:t,onSubmit:n,status:r=`ready`,isDisabled:i=!1,mode:a=`prompt`,value:o,onValueChange:s,...c}){let[l,u]=(0,X.useState)(``),d=o!==void 0,f=d?o:l,p=e=>{d||u(e),s?.(e)},m=(0,X.useRef)(f);m.current=f;let h={status:r,isDisabled:i,onSubmit:()=>{if(r===`submitted`||r===`streaming`)return;let e=m.current.trim();e&&(n?.(e),p(``))},value:f,setValue:p};return G($_.Provider,{value:h,children:G(`div`,{ref:t,css:tv,"data-status":r,"data-input-mode":a,...c,children:e})})}function lv(e){let t=(0,Z.c)(8),n,r,i;t[0]===e?(n=t[1],r=t[2],i=t[3]):({children:n,ref:r,...i}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i);let a;return t[4]!==n||t[5]!==r||t[6]!==i?(a=G(`div`,{ref:r,css:nv,...i,children:n}),t[4]=n,t[5]=r,t[6]=i,t[7]=a):a=t[7],a}function uv(e){let t=(0,Z.c)(8),n,r,i;t[0]===e?(n=t[1],r=t[2],i=t[3]):({children:n,ref:r,...i}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i);let a;return t[4]!==n||t[5]!==r||t[6]!==i?(a=G(`div`,{ref:r,css:iv,...i,children:n}),t[4]=n,t[5]=r,t[6]=i,t[7]=a):a=t[7],a}function dv(e){let t=(0,Z.c)(8),n,r,i;t[0]===e?(n=t[1],r=t[2],i=t[3]):({children:n,ref:r,...i}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i);let a;return t[4]!==n||t[5]!==r||t[6]!==i?(a=G(`div`,{ref:r,css:av,role:`toolbar`,...i,children:n}),t[4]=n,t[5]=r,t[6]=i,t[7]=a):a=t[7],a}function fv(e){let t=(0,Z.c)(8),n,r,i;t[0]===e?(n=t[1],r=t[2],i=t[3]):({children:n,ref:r,...i}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i);let a;return t[4]!==n||t[5]!==r||t[6]!==i?(a=G(`div`,{ref:r,css:ov,...i,children:n}),t[4]=n,t[5]=r,t[6]=i,t[7]=a):a=t[7],a}function pv(e){let t=(0,Z.c)(20),{ref:n,placeholder:r,value:i,onChange:a,maxRows:o,"aria-label":s,className:c}=e,l=r===void 0?`Send a message...`:r,u=s===void 0?`Message input`:s,d=ev(),f=(0,X.useRef)(null),p=i===void 0?d.value:i,m=a===void 0?d.setValue:a,h;t[0]===n?h=t[1]:(h=e=>{f.current=e,typeof n==`function`?n(e):n&&`current`in n&&(n.current=e)},t[0]=n,t[1]=h);let g=h,_;t[2]===o?_=t[3]:(_=()=>{let e=f.current;if(!e)return;let t=()=>{e.style.height=`auto`;let t=e.scrollHeight;if(o){let n=parseInt(getComputedStyle(e).lineHeight||`20`,10)*o;t=Math.min(t,n)}e.style.height=`${t}px`};t();let n=requestAnimationFrame(t);return()=>{cancelAnimationFrame(n)}},t[2]=o,t[3]=_);let v;t[4]!==o||t[5]!==p?(v=[p,o],t[4]=o,t[5]=p,t[6]=v):v=t[6],(0,X.useLayoutEffect)(_,v);let{onSubmit:y}=d,b;t[7]===y?b=t[8]:(b=e=>{e.key===`Enter`&&!e.shiftKey&&(e.preventDefault(),y())},t[7]=y,t[8]=b);let x=b,S;t[9]===m?S=t[10]:(S=e=>{m(e.target.value)},t[9]=m,t[10]=S);let C=S,w;return t[11]!==u||t[12]!==c||t[13]!==d.isDisabled||t[14]!==C||t[15]!==x||t[16]!==g||t[17]!==l||t[18]!==p?(w=G(`textarea`,{ref:g,css:rv,className:c,value:p,onChange:C,onKeyDown:x,placeholder:l,disabled:d.isDisabled,"aria-label":u,rows:1}),t[11]=u,t[12]=c,t[13]=d.isDisabled,t[14]=C,t[15]=x,t[16]=g,t[17]=l,t[18]=p,t[19]=w):w=t[19],w}function mv(e){let t=(0,Z.c)(15),{ref:n,onPress:r,isDisabled:i,"aria-label":a,className:o}=e,s=ev(),c=s.status===`submitted`||s.status===`streaming`,l;t[0]===s.value?l=t[1]:(l=s.value.trim(),t[0]=s.value,t[1]=l);let u=l===``,d=i??(s.status===`ready`&&u),f=!c,p=a??(f?`Send message`:`Stop generation`),m;t[2]!==s||t[3]!==c||t[4]!==r?(m=()=>{if(c){r?.();return}s.onSubmit()},t[2]=s,t[3]=c,t[4]=r,t[5]=m):m=t[5];let h=m,g=d||s.isDisabled,_;t[6]===f?_=t[7]:(_=G(U,{svg:G(f?Xe:Bn,{})}),t[6]=f,t[7]=_);let v;return t[8]!==o||t[9]!==p||t[10]!==h||t[11]!==n||t[12]!==g||t[13]!==_?(v=G(Jt,{ref:n,css:sv,className:o,isDisabled:g,onPress:h,"aria-label":p,children:_}),t[8]=o,t[9]=p,t[10]=h,t[11]=n,t[12]=g,t[13]=_,t[14]=v):v=t[14],v}q`
  display: flex;
  align-items: center;
  gap: var(--global-dimension-size-75);
`;var hv=q`
  ${yn};
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
`,gv=new Map,_v=e=>{let t=gv.get(e);if(t)return t;let n=ye.create(e);return gv.set(e,n),n};function vv(e){let t=(0,Z.c)(37),n,r,i,a,o,s,c,l,u,d,f,p;t[0]===e?(n=t[1],r=t[2],i=t[3],a=t[4],o=t[5],s=t[6],c=t[7],l=t[8],u=t[9],d=t[10],f=t[11],p=t[12]):({ref:i,children:n,elementType:s,size:c,weight:l,color:u,fontStyle:d,duration:f,spread:p,className:r,style:o,...a}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a,t[5]=o,t[6]=s,t[7]=c,t[8]=l,t[9]=u,t[10]=d,t[11]=f,t[12]=p);let m=s===void 0?`p`:s,h=c===void 0?`S`:c,g=l===void 0?`normal`:l,_=u===void 0?`text-700`:u,v=d===void 0?`normal`:d,y=f===void 0?2:f,b=p===void 0?2:p,x=De(),S=m,C;t[13]===S?C=t[14]:(C=_v(S),t[13]=S,t[14]=C);let w=C,T=(n?.length??0)*b,E;t[15]!==y||t[16]!==x?(E=x?{}:{initial:{backgroundPosition:`100% center`},animate:{backgroundPosition:`0% center`},transition:{duration:y,ease:`linear`,repeat:1/0}},t[15]=y,t[16]=x,t[17]=E):E=t[17];let D=E,O=i,k;t[18]===r?k=t[19]:(k=B(`shimmer`,r),t[18]=r,t[19]=k);let A=`${T}px`,j;t[20]===_?j=t[21]:(j=Mt(_),t[20]=_,t[21]=j);let M;t[22]!==v||t[23]!==o||t[24]!==A||t[25]!==j?(M={"--shimmer-spread":A,"--shimmer-color":j,fontStyle:v,...o},t[22]=v,t[23]=o,t[24]=A,t[25]=j,t[26]=M):M=t[26];let N=M,P=a,F;return t[27]!==w||t[28]!==D||t[29]!==n||t[30]!==h||t[31]!==O||t[32]!==k||t[33]!==N||t[34]!==P||t[35]!==g?(F=G(w,{ref:O,className:k,"data-size":h,"data-weight":g,css:hv,style:N,...D,...P,children:n}),t[27]=w,t[28]=D,t[29]=n,t[30]=h,t[31]=O,t[32]=k,t[33]=N,t[34]=P,t[35]=g,t[36]=F):F=t[36],F}vv.displayName=`Shimmer`;var $=e=>`var(${e})`,yv=Object.freeze({blue100:$(`--global-color-blue-200`),blue200:$(`--global-color-blue-300`),blue300:$(`--global-color-blue-400`),blue400:$(`--global-color-blue-500`),blue500:$(`--global-color-blue-600`),blue600:$(`--global-color-blue-700`),blue700:$(`--global-color-blue-800`),blue800:$(`--global-color-blue-900`),blue900:$(`--global-color-blue-1000`),orange100:$(`--global-color-orange-500`),orange200:$(`--global-color-orange-600`),orange300:$(`--global-color-orange-700`),orange400:$(`--global-color-orange-800`),orange500:$(`--global-color-orange-900`),purple100:$(`--global-color-purple-100`),purple200:$(`--global-color-purple-200`),purple300:$(`--global-color-purple-300`),purple400:$(`--global-color-purple-400`),purple500:$(`--global-color-purple-500`),magenta100:$(`--global-color-magenta-200`),magenta200:$(`--global-color-magenta-300`),magenta300:$(`--global-color-magenta-400`),magenta400:$(`--global-color-magenta-500`),magenta500:$(`--global-color-magenta-600`),red100:$(`--global-color-red-200`),red200:$(`--global-color-red-300`),red300:$(`--global-color-red-400`),red400:$(`--global-color-red-500`),red500:$(`--global-color-red-600`),gray100:$(`--global-color-gray-100`),gray200:$(`--global-color-gray-200`),gray300:$(`--global-color-gray-300`),gray400:$(`--global-color-gray-400`),gray500:$(`--global-color-gray-500`),gray600:$(`--global-color-gray-600`),gray700:$(`--global-color-gray-700`),default:$(`--global-text-color-900`)});Object.keys(yv);var bv=()=>yv,xv=(e,t)=>{let n=[[`blue`,5],[`orange`,5],[`purple`,5],[`pink`,5],[`gray`,5]],r=n.length,i=e%r,a=Math.floor(e/r),[o,s]=n[i];return t[`${o}${500-a%s*100}`]||t.default},Sv={danger:`var(--global-color-red-700)`,success:`var(--global-color-celery-700)`,warning:`var(--global-color-warning)`,info:`var(--global-color-blue-700)`};Object.keys(Sv);var Cv=()=>Sv,wv={category1:`var(--global-color-blue-700)`,category2:`var(--global-color-purple-900)`,category3:`var(--global-color-magenta-600)`,category4:`var(--global-color-indigo-600)`,category5:`var(--global-color-blue-900)`,category6:`var(--global-color-indigo-1100)`,category7:`var(--global-color-orange-600)`,category8:`var(--global-color-celery-400)`,category9:`var(--global-color-seafoam-600)`,category10:`var(--global-color-green-1000)`,category11:`var(--global-color-yellow-400)`,category12:`var(--global-color-red-1100)`},Tv={category1:`var(--global-color-blue-700)`,category2:`var(--global-color-purple-800)`,category3:`var(--global-color-magenta-800)`,category4:`var(--global-color-indigo-600)`,category5:`var(--global-color-blue-900)`,category6:`var(--global-color-indigo-1100)`,category7:`var(--global-color-orange-600)`,category8:`var(--global-color-celery-400)`,category9:`var(--global-color-seafoam-600)`,category10:`var(--global-color-green-1000)`,category11:`var(--global-color-yellow-400)`,category12:`var(--global-color-red-1100)`},Ev=()=>{let{theme:e}=Pr();return e===`dark`?Tv:wv},Dv=Object.keys(wv),Ov=({index:e,colors:t})=>t[Dv[e%Dv.length]],kv={gray1:`var(--global-color-gray-800)`,gray2:`var(--global-color-gray-600)`,gray3:`var(--global-color-gray-500)`,gray4:`var(--global-color-gray-400)`},Av={gray1:`var(--global-color-gray-800)`,gray2:`var(--global-color-gray-600)`,gray3:`var(--global-color-gray-500)`,gray4:`var(--global-color-gray-400)`},jv=()=>{let{theme:e}=Pr();return e===`dark`?Av:kv},Mv=Object.keys(kv),Nv=q`
  width: 100%;
  display: flex;
  flex-direction: row;
  overflow: hidden;
  border-radius: var(--global-rounding-medium);
  gap: 2px;
`,Pv=q`
  height: 100%;
  flex-shrink: 0;
  flex-grow: 0;
`,Fv=e=>{let t=(0,Z.c)(18),{height:n,minimumSegmentPercentage:r,segments:i,totalValue:a}=e,o=n===void 0?6:n,s=r===void 0?0:r,c;t[0]!==a||t[1]!==i?(c=a??i.reduce(Iv,0),t[0]=a,t[1]=i,t[2]=c):c=t[2];let l=c,u;t[3]!==s||t[4]!==i?(u=s>0?i.filter(Lv):i,t[3]=s,t[4]=i,t[5]=u):u=t[5];let d=u;if(!d.some(Rv))return null;let f=`${o}px`,p;t[6]===f?p=t[7]:(p={height:f},t[6]=f,t[7]=p);let m;if(t[8]!==s||t[9]!==l||t[10]!==d){let e;t[12]!==s||t[13]!==l?(e=e=>{let t=l>0?e.value/l*100:0,n=e.color,r=e.value>0&&s>0?`${s}%`:void 0;return G(`div`,{css:Pv,style:{width:`${t}%`,minWidth:r,flexShrink:r==null?0:1,backgroundColor:n}},e.name)},t[12]=s,t[13]=l,t[14]=e):e=t[14],m=d.map(e),t[8]=s,t[9]=l,t[10]=d,t[11]=m}else m=t[11];let h;return t[15]!==p||t[16]!==m?(h=G(`div`,{style:p,css:Nv,children:m}),t[15]=p,t[16]=m,t[17]=h):h=t[17],h};function Iv(e,t){return e+t.value}function Lv(e){return e.value>0}function Rv(e){return e.value>0}function zv(e){return Math.abs(e)<1e6?Ye(`,`)(e):Ye(`0.2s`)(e).replace(`G`,`B`).replace(`k`,`K`)}function Bv(e){return Math.abs(e)<1e3?Ye(`,`)(e):Ye(`0.2s`)(e).replace(`G`,`B`).replace(`k`,`K`)}function Vv(e){let t=Math.abs(e);if(t===0)return`0.00`;if(t<.01)return Ye(`.2e`)(e);if(t<1){let t=ny(e,2);return Ye(`0.2f`)(t)}return t<1e3?Ye(`0.2f`)(e):Ye(`0.2s`)(e)}function Hv(e){let t=Math.abs(e);return t===0?`0.00`:t<.01?Ye(`.2e`)(e):t<1e3?Ye(`0.2f`)(e):Ye(`0.2s`)(e).replace(`G`,`B`).replace(`k`,`K`)}function Uv(e){return Ye(`.2f`)(e)+`%`}function Wv(e){return Number.isInteger(e)?zv(e):Vv(e)}function Gv(e){return e===0?`$0`:e<.01?`<$0.01`:e<100?`$${Ye(`0.2f`)(e)}`:e<1e4?`$${Ye(`,`)(e)}`:`$${Ye(`0.2s`)(e).replace(`G`,`B`).replace(`k`,`K`)}`}function Kv(e){let t=Math.floor(e/ua),n=Math.floor(e%ua/la),r=Math.floor(e%la/ca),i=Math.floor(e%ca);if(t>0)return`${t}h${n?` ${n}m`:``}${r?` ${r}s`:``}`;if(n>0)return`${n}m${r?` ${r}s`:``}`;if(r>0){let e=Math.floor(i/100);return`${r}${e>0?`.${e.toFixed(0)}`:``}s`}return`${i.toFixed(0)}ms`}function qv(e){return t=>typeof t==`number`?e(t):`--`}var Jv=qv(zv),Yv=qv(Bv),Xv=qv(Hv),Zv=qv(Vv),Qv=qv(Wv),$v=qv(Uv),ey=qv(Gv),ty=qv(Kv);function ny(e,t){let n=e.toString().split(`.`);return n.length<2?e:Number(n[0]+`.`+n[1].substring(0,t))}var ry=q`
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
`;function iy({ref:e,...t}){let{children:n,color:r=`text-900`,size:i=`M`,...a}=t,o=Mt(r),s=typeof n==`number`?Wv(n):`--`;return H(`div`,{className:`token-count-item`,"data-size":i,css:ry,ref:e,...a,children:[G(U,{svg:G(an,{}),css:q`
          color: ${o};
        `}),G(V,{size:t.size,color:r,fontFamily:`mono`,children:s})]})}var ay=1e-9,oy={input:0,output:0,cache_read:1,cache_write:2,reasoning:3,audio:4},sy={input:`category1`,output:`category2`,cache_read:`category9`,cache_write:`category7`,reasoning:`category4`,audio:`category3`},cy=[`category5`,`category6`,`category8`,`category10`,`category11`,`category12`];function ly(e){let t=e.split(`_`).join(` `);return t.charAt(0).toUpperCase()+t.slice(1)}function uy(e){return e?`input`:`output`}function dy(e,t){let n=oy[e]??100,r=oy[t]??100;return n===r?e.localeCompare(t):n-r}function fy({colors:e,index:t=0,tokenType:n}){let r=sy[n];return r?e[r]:e[cy[t%cy.length]]}function py(e){return cy.map(t=>e[t])}var my=q`
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
`,hy=q`
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
`,gy=q`
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
`,_y=q`
  width: var(--global-dimension-size-100);
  height: var(--global-dimension-size-100);
  flex: none;
  border-radius: var(--global-rounding-full);
`,vy=q`
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
`;function yy({value:e,maximum:t}){return Math.min(Math.max(e,0),Math.max(t,0))}function by(e){let t=(0,Z.c)(10),{segment:n}=e,r;t[0]===n.color?r=t[1]:(r=G(`span`,{className:`chat-token-usage-details__swatch`,css:_y,style:{backgroundColor:n.color},"aria-hidden":`true`}),t[0]=n.color,t[1]=r);let i;t[2]===n.value?i=t[3]:(i=Bv(n.value),t[2]=n.value,t[3]=i);let a;t[4]!==n.name||t[5]!==i?(a=H(V,{className:`chat-token-usage-details__segment-text`,size:`XS`,color:`text-500`,fontFamily:`mono`,children:[i,` `,n.name]}),t[4]=n.name,t[5]=i,t[6]=a):a=t[6];let o;return t[7]!==r||t[8]!==a?(o=H(W,{children:[r,a]}),t[7]=r,t[8]=a,t[9]=o):o=t[9],o}function xy(e){let t=(0,Z.c)(15),{promptSegment:n,promptDetailsSegments:r}=e,i;t[0]===n.value?i=t[1]:(i=zv(n.value),t[0]=n.value,t[1]=i);let a=`${i} prompt tokens. Show cache details`,o;t[2]===n?o=t[3]:(o=G(by,{segment:n}),t[2]=n,t[3]=o);let s;t[4]!==a||t[5]!==o?(s=G(Nt,{className:`chat-token-usage-details__segment-trigger`,css:gy,size:`S`,variant:`quiet`,"aria-label":a,children:o}),t[4]=a,t[5]=o,t[6]=s):s=t[6];let c;t[7]===Symbol.for(`react.memo_cache_sentinel`)?(c=G(V,{className:`chat-token-usage-details__tooltip-title`,size:`XS`,color:`text-700`,weight:`heavy`,children:`Prompt details`}),t[7]=c):c=t[7];let l;t[8]===r?l=t[9]:(l=r.map(Sy),t[8]=r,t[9]=l);let u;t[10]===l?u=t[11]:(u=H(Da,{css:vy,placement:`top`,offset:3,children:[c,G(`ul`,{className:`chat-token-usage-details__tooltip-segments`,"aria-label":`Prompt token types`,children:l})]}),t[10]=l,t[11]=u);let d;return t[12]!==s||t[13]!==u?(d=G(`li`,{className:`chat-token-usage-details__segment`,children:H(Te,{delay:0,closeDelay:0,children:[s,u]})}),t[12]=s,t[13]=u,t[14]=d):d=t[14],d}function Sy(e){return G(`li`,{className:`chat-token-usage-details__tooltip-segment`,children:G(by,{segment:e})},e.name)}function Cy(e){let t=(0,Z.c)(45),{total:n,prompt:r,completion:i,promptDetails:a}=e,o=Ev(),s=a?.cacheRead??0,c;t[0]!==r||t[1]!==s?(c=yy({value:s,maximum:r}),t[0]=r,t[1]=s,t[2]=c):c=t[2];let l=c,u=a?.cacheWrite??0,d=Math.max(r-l,0),f;t[3]!==u||t[4]!==d?(f=yy({value:u,maximum:d}),t[3]=u,t[4]=d,t[5]=f):f=t[5];let p=f,m=Math.max(r-l-p,0),h=r>0&&(l>0||p>0),g;t[6]!==o.category1||t[7]!==r?(g={name:`Prompt`,value:r,color:o.category1},t[6]=o.category1,t[7]=r,t[8]=g):g=t[8];let _;t[9]!==o.category2||t[10]!==i?(_={name:`Completion`,value:i,color:o.category2},t[9]=o.category2,t[10]=i,t[11]=_):_=t[11];let v;t[12]!==g||t[13]!==_?(v=[g,_],t[12]=g,t[13]=_,t[14]=v):v=t[14];let y=v,b;t[15]===o?b=t[16]:(b=fy({colors:o,tokenType:`input`}),t[15]=o,t[16]=b);let x;t[17]!==b||t[18]!==m?(x={name:`Uncached`,value:m,color:b},t[17]=b,t[18]=m,t[19]=x):x=t[19];let S;t[20]===o?S=t[21]:(S=fy({colors:o,tokenType:`cache_read`}),t[20]=o,t[21]=S);let C;t[22]!==l||t[23]!==S?(C={name:`Cache read`,value:l,color:S},t[22]=l,t[23]=S,t[24]=C):C=t[24];let w;t[25]===o?w=t[26]:(w=fy({colors:o,tokenType:`cache_write`}),t[25]=o,t[26]=w);let T;t[27]!==p||t[28]!==w?(T={name:`Cache write`,value:p,color:w},t[27]=p,t[28]=w,t[29]=T):T=t[29];let E;t[30]!==x||t[31]!==C||t[32]!==T?(E=[x,C,T].filter(wy),t[30]=x,t[31]=C,t[32]=T,t[33]=E):E=t[33];let D=E,O;t[34]!==y||t[35]!==n?(O=G(`div`,{"aria-hidden":`true`,children:G(Fv,{height:6,minimumSegmentPercentage:1,totalValue:n,segments:y})}),t[34]=y,t[35]=n,t[36]=O):O=t[36];let k;t[37]===Symbol.for(`react.memo_cache_sentinel`)?(k=G(V,{size:`XS`,color:`text-700`,weight:`heavy`,children:`Total`}),t[37]=k):k=t[37];let A;t[38]!==y||t[39]!==h||t[40]!==D?(A=H(`div`,{className:`chat-token-usage-details__legend`,children:[k,G(`ul`,{className:`chat-token-usage-details__segments`,"aria-label":`Token types`,children:y.map(e=>e.name===`Prompt`&&h?G(xy,{promptSegment:e,promptDetailsSegments:D},e.name):G(`li`,{className:`chat-token-usage-details__segment`,children:G(by,{segment:e})},e.name))})]}),t[38]=y,t[39]=h,t[40]=D,t[41]=A):A=t[41];let j;return t[42]!==O||t[43]!==A?(j=H(`div`,{className:`chat-token-usage-details`,css:hy,role:`region`,"aria-label":`Token usage breakdown`,children:[O,A]}),t[42]=O,t[43]=A,t[44]=j):j=t[44],j}function wy(e){return e.value>0}function Ty(e){let t=(0,Z.c)(24),{total:n,prompt:r,completion:i,promptDetails:a}=e,[o,s]=(0,X.useState)(!1),c=(0,X.useId)(),l;t[0]===n?l=t[1]:(l=zv(n),t[0]=n,t[1]=l);let u=`${l} total tokens`,d;t[2]===Symbol.for(`react.memo_cache_sentinel`)?(d=()=>s(Ey),t[2]=d):d=t[2];let f;t[3]===n?f=t[4]:(f=G(iy,{size:`S`,color:`text-300`,children:n}),t[3]=n,t[4]=f);let p;t[5]===o?p=t[6]:(p=G(qt,{isExpanded:o}),t[5]=o,t[6]=p);let m;t[7]!==c||t[8]!==o||t[9]!==u||t[10]!==f||t[11]!==p?(m=G(`div`,{className:`chat-token-usage__summary`,children:H(`button`,{className:`chat-token-usage__trigger button--reset`,type:`button`,"aria-controls":c,"aria-expanded":o,"aria-label":u,onClick:d,children:[f,p]})}),t[7]=c,t[8]=o,t[9]=u,t[10]=f,t[11]=p,t[12]=m):m=t[12];let h;t[13]!==i||t[14]!==c||t[15]!==o||t[16]!==r||t[17]!==a||t[18]!==n?(h=o?G(`div`,{className:`chat-token-usage__details`,id:c,children:G(Cy,{total:n,prompt:r,completion:i,promptDetails:a})}):null,t[13]=i,t[14]=c,t[15]=o,t[16]=r,t[17]=a,t[18]=n,t[19]=h):h=t[19];let g;return t[20]!==o||t[21]!==m||t[22]!==h?(g=H(`div`,{className:`chat-token-usage`,css:my,"data-expanded":o,children:[m,h]}),t[20]=o,t[21]=m,t[22]=h,t[23]=g):g=t[23],g}function Ey(e){return!e}var Dy=(0,X.createContext)(null);function Oy(){return(0,X.useContext)(Dy)}function ky(e){let t=e.parentElement;for(;t;){let{overflowY:e}=getComputedStyle(t);if((e===`auto`||e===`scroll`)&&t.scrollHeight>t.clientHeight)return t;t=t.parentElement}return null}function Ay(){let e=(0,Z.c)(5),t=Oy(),n=(0,X.useRef)(null),r;e[0]===t?r=e[1]:(r=e=>{if(t?.stopScroll(),n.current=null,!e)return;let r=ky(e);if(!r)return;let i=e.getBoundingClientRect(),a=r.getBoundingClientRect();n.current={scrollParent:r,offsetFromParentTop:i.top-a.top}},e[0]=t,e[1]=r);let i=r,a;e[2]===Symbol.for(`react.memo_cache_sentinel`)?(a=e=>{let t=n.current;if(n.current=null,!t||!e)return;let{scrollParent:r,offsetFromParentTop:i}=t,a=e.getBoundingClientRect(),o=r.getBoundingClientRect(),s=a.top-o.top;r.scrollTop+=s-i},e[2]=a):a=e[2];let o=a,s;return e[3]===i?s=e[4]:(s={capture:i,restore:o},e[3]=i,e[4]=s),s}var jy=Gt`
  from {
    opacity: 0;
    transform: translateY(-2px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
`,My={titleFlex:`0 1 auto`,titleMinWidth:`0`,titleMaxWidth:`55%`,middleFlex:`1 1 50px`,middleMinWidth:`50px`,statusFlex:`0 1 auto`,statusMinWidth:`0`,statusMaxWidth:`none`};function Ny(e){let t=(0,Z.c)(3),{children:n,variant:r}=e,i;return t[0]!==n||t[1]!==r?(i=G(`div`,{className:`tool-part__line`,children:G(`span`,{className:`tool-part__label`,"data-variant":r,children:n})}),t[0]=n,t[1]=r,t[2]=i):i=t[2],i}function Py(e){let t=(0,Z.c)(9),{children:n,allowCopy:r}=e,i=r===void 0||r,a=`tool-part__line${i?` tool-part__line--copyable`:``}`,o=n||`(empty)`,s;t[0]===o?s=t[1]:(s=G(`code`,{className:`tool-part__code`,children:o}),t[0]=o,t[1]=s);let c;t[2]!==i||t[3]!==n?(c=i?G(Na,{text:n,size:`S`,variant:`quiet`,tooltipText:`Copy`}):null,t[2]=i,t[3]=n,t[4]=c):c=t[4];let l;return t[5]!==a||t[6]!==s||t[7]!==c?(l=H(`div`,{className:a,children:[s,c]}),t[5]=a,t[6]=s,t[7]=c,t[8]=l):l=t[8],l}function Fy(e){let t=(0,Z.c)(3),{children:n,variant:r}=e,i;return t[0]!==n||t[1]!==r?(i=G(`span`,{className:`tool-part__status`,"data-variant":r,children:n}),t[0]=n,t[1]=r,t[2]=i):i=t[2],i}function Iy(e){let t=(0,Z.c)(4),{items:n}=e,r;t[0]===n?r=t[1]:(r=n.map(Ly),t[0]=n,t[1]=r);let i;return t[2]===r?i=t[3]:(i=G(`div`,{className:`tool-part__meta`,children:r}),t[2]=r,t[3]=i),i}function Ly(e){let{label:t,value:n}=e;return H(`span`,{className:`tool-part__meta-group`,children:[G(`span`,{className:`tool-part__meta-label`,children:t}),G(`code`,{className:`tool-part__meta-value`,children:n})]},t)}var Ry=q`
  padding: var(--global-dimension-size-50) var(--global-dimension-size-200)
    var(--global-dimension-size-150);
`;function zy(e){let t=(0,Z.c)(15),{onAccept:n,onReject:r,isDisabled:i,staleMessage:a}=e,o=i!==void 0&&i,s;t[0]!==o||t[1]!==n?(s=G(Nt,{size:`S`,variant:`primary`,isDisabled:o,onPress:n,children:`Accept`}),t[0]=o,t[1]=n,t[2]=s):s=t[2];let c;t[3]!==o||t[4]!==r?(c=G(Nt,{size:`S`,isDisabled:o,onPress:r,children:`Reject`}),t[3]=o,t[4]=r,t[5]=c):c=t[5];let l;t[6]!==s||t[7]!==c?(l=G(`div`,{css:Ry,children:H(K,{direction:`row-reverse`,gap:`size-100`,children:[s,c]})}),t[6]=s,t[7]=c,t[8]=l):l=t[8];let u;t[9]!==o||t[10]!==a?(u=o&&a?G(Py,{children:a}):null,t[9]=o,t[10]=a,t[11]=u):u=t[11];let d;return t[12]!==l||t[13]!==u?(d=H(W,{children:[l,u]}),t[12]=l,t[13]=u,t[14]=d):d=t[14],d}var By=320,Vy=q`
  --expandable-content-overlay-background-color: var(
    --tool-call-body-background-color
  );
`;function Hy(e){let t=(0,Z.c)(6),{children:n}=e,r=(0,X.useRef)(null),[i,a]=(0,X.useState)(!1),o=Ay(),s;t[0]===o?s=t[1]:(s=e=>{o.capture(r.current),a(e),requestAnimationFrame(()=>o.restore(r.current))},t[0]=o,t[1]=s);let c=s,l;return t[2]!==n||t[3]!==c||t[4]!==i?(l=G(`div`,{ref:r,css:Vy,children:G(nt,{height:By,expandedBehavior:`grow`,isExpanded:i,onExpandedChange:c,children:n})}),t[2]=n,t[3]=c,t[4]=i,t[5]=l):l=t[5],l}function Uy(e){switch(e){case`input-streaming`:return`Preparing`;case`input-available`:return`Running`;case`approval-requested`:return`Awaiting approval`;case`approval-responded`:return`Approval received`;case`output-available`:return`Completed`;case`output-error`:return`Error`;case`output-denied`:return`Denied`;default:return dr(e)}}function Wy(e){if(e==null)return``;if(typeof e==`string`)return e;try{return JSON.stringify(e,null,2)}catch{return String(e)}}export{Q_ as $,ri as $a,ka as $i,Ru as $n,Zs as $r,Sh as $t,Uv as A,Ui as Aa,mo as Ai,_p as An,Jc as Ar,fg as At,Ev as B,Oi as Ba,Xa as Bi,sf as Bn,Ec as Br,Zh as Bt,Zv as C,Fi as Ca,Xo as Ci,mp as Cn,fl as Cr,Bg as Ct,zv as D,Mi as Da,jo as Di,gp as Dn,il as Dr,Pg as Dt,Vv as E,Ii as Ea,Po as Ei,Op as En,al as Er,Fg as Et,$v as F,Ti as Fa,no as Fi,_f as Fn,zc as Fr,ng as Ft,mv as G,pi as Ga,Ga as Gi,ld as Gn,hc as Gr,Lh as Gt,Cv as H,ki as Ha,Va as Hi,hd as Hn,xc as Hr,Wh as Ht,Fv as I,Si as Ia,to as Ii,ff as In,Nc as Ir,tg as It,dv as J,li as Ja,Fa as Ji,id as Jn,ac as Jr,kh as Jt,pv as K,di as Ka,Ra as Ki,sd as Kn,lc as Kr,Rh as Kt,Mv as L,Ai as La,eo as Li,df as Ln,Fc as Lr,eg as Lt,Yv as M,Hi as Ma,lo as Mi,Nf as Mn,Gc as Mr,ug as Mt,ty as N,ji as Na,co as Ni,Pf as Nn,qc as Nr,og as Nt,Bv as O,Ri as Oa,bo as Oi,Ap as On,tl as Or,mg as Ot,Qv as P,wi as Pa,io as Pi,vf as Pn,Hc as Pr,ig as Pt,ev as Q,Qr as Qa,Aa as Qi,Bu as Qn,Ys as Qr,xh as Qt,Ov as R,Ei as Ra,Qa as Ri,uf as Rn,jc as Rr,Kh as Rt,ey as S,zi as Sa,ts as Si,hp as Sn,vr as So,pl as Sr,Vg as St,Gv as T,Ni as Ta,Go as Ti,Ep as Tn,ul as Tr,Hg as Tt,bv as U,gi as Ua,Ka as Ui,ad as Un,yc as Ur,Hh as Ut,jv as V,Ci as Va,Ia as Vi,md as Vn,Oc as Vr,Gh as Vt,vv as W,_i as Wa,Wa as Wi,cd as Wn,_c as Wr,Vh as Wt,lv as X,ui as Xa,Na as Xi,ed as Xn,tc as Xr,Eh as Xt,uv as Y,ci as Ya,qa as Yi,rd as Yn,rc as Yr,Th as Yt,cv as Z,ni as Za,Da as Zi,Ju as Zn,$s as Zr,Dh as Zt,uy as _,qi as _a,ss as _i,wp as _n,fr as _o,Al as _r,qg as _t,zy as a,ga as aa,Fs as ai,Qm as an,Rr as ao,uu as ar,z_ as at,ly as b,Li as ba,ls as bi,Cp as bn,_r as bo,wl as br,Ig as bt,Ny as c,ma as ca,ks as ci,Gm as cn,Lr as co,$l as cr,M_ as ct,ky as d,sa as da,Ss as di,Km as dn,Pr as do,Gl as dr,D_ as dt,Oa as ea,Ks as ei,Ch as en,ii as eo,Lu as er,Z_ as et,Ay as f,oa as fa,bs as fi,Ym as fn,br as fo,Ul as fr,b_ as ft,dy as g,Yi as ga,us as gi,vp as gn,dr as go,jl as gr,e_ as gt,ay as h,ea as ha,vs as hi,Mp as hn,Sr as ho,Pl as hr,c_ as ht,jy as i,ya as ia,Vs as ii,yh as in,Br as io,bu as ir,G_ as it,Jv as j,Vi as ja,po as ji,Sp as jn,Xc as jr,dg as jt,Wv as k,Wi as ka,_o as ki,kp as kn,Zc as kr,pg as kt,Iy as l,ha as la,Os as li,Wm as ln,Fr as lo,Xl as lr,j_ as lt,Ty as m,ta as ma,_s as mi,Zm as mn,Cr as mo,Il as mr,l_ as mt,Wy as n,Ta as na,Ws as ni,ch as nn,Yr as no,_u as nr,J_ as nt,Py as o,_a as oa,Ps as oi,Um as on,Ur as oo,lu as or,L_ as ot,Dy as p,ra as pa,ys as pi,Jm as pn,xr as po,Rl as pr,u_ as pt,fv as q,si as qa,Ua as qi,od as qn,sc as qr,Fh as qt,My as r,Ca as ra,Us as ri,sh as rn,Xr as ro,yu as rr,K_ as rt,Hy as s,fa as sa,js as si,Xm as sn,Hr as so,ou as sr,N_ as st,Uy as t,Ea as ta,Gs as ti,lh as tn,Zr as to,vu as tr,X_ as tt,Fy as u,pa as ua,Es as ui,qm as un,Dr as uo,ql as ur,O_ as ut,fy as v,Ki as va,os as vi,Tp as vn,gr as vo,Ol as vr,Gg as vt,Xv as w,Pi as wa,Jo as wi,pp as wn,dl as wr,Ug as wt,iy as x,Bi as xa,rs as xi,yp as xn,mr as xo,vl as xr,Lg as xt,py as y,Gi as ya,cs as yi,Dp as yn,hr as yo,El as yr,Wg as yt,xv as z,Di as za,Ya as zi,cf as zn,Tc as zr,Qh as zt};