import{s as e}from"./rolldown-runtime-BG2f4sTM.js";import{$n as t,An as n,Bn as r,Dn as i,En as a,Fn as o,Gn as s,Gt as c,Hn as l,Ht as u,In as d,Jn as f,Jt as p,Kt as m,Ln as h,Mn as g,On as _,Qt as v,Rn as y,Sn as b,St as x,Tn as S,Ut as C,Vn as w,Vt as T,Wn as E,Xn as D,Xt as O,Yn as k,Yt as A,Zn as j,Zt as M,_n as N,ar as P,at as F,bn as I,cn as L,cr as R,dn as z,dr as ee,en as te,er as ne,ft as re,gn as ie,gt as ae,hn as oe,hr as se,ht as ce,in as le,it as ue,jn as de,kn as fe,ln as pe,lr as me,mn as he,nn as ge,nr as _e,or as ve,pn as ye,pt as be,qn as xe,rn as Se,rr as Ce,rt as we,sn as Te,sr as Ee,tn as De,tr as Oe,un as ke,ur as Ae,vn as je,vt as Me,wn as Ne,xt as Pe,yn as Fe,zn as Ie}from"./vendor-DRJB2dTi.js";import{et as Le}from"./vendor-codemirror-BZW8dsuL.js";import{C as B,b as Re,w as ze}from"./vendor-recharts-DS6URa-P.js";import{$ as Be,$n as Ve,A as He,Aa as Ue,An as We,Bi as Ge,Br as Ke,Bt as qe,C as Je,Co as Ye,Ct as Xe,D as V,Dn as Ze,E as Qe,Ei as $e,F as et,Fo as tt,G as H,Gr as nt,Gt as rt,H as it,Ht as at,In as ot,It as st,J as ct,Jr as lt,Jt as ut,K as dt,Kn as ft,Kr as pt,Kt as mt,L as ht,M as gt,Mn as _t,Mo as U,No as W,O as vt,P as yt,Pn as bt,Po as G,R as xt,Ri as St,S as Ct,T as wt,Tt,Ui as Et,Un as Dt,Ur as Ot,Ut as kt,Va as At,Vr as jt,Vt as Mt,W as Nt,Wn as Pt,Wt as Ft,Y as It,Zr as Lt,ai as Rt,an as zt,ar as Bt,bn as Vt,ci as Ht,cn as Ut,ct as Wt,ea as Gt,fn as Kt,fr as qt,gr as Jt,gt as Yt,ht as Xt,i as Zt,ia as Qt,in as $t,j as en,ja as tn,jn as nn,jt as rn,k as an,ki as on,la as sn,lr as cn,m as ln,mn as un,mr as dn,mt as fn,on as pn,p as mn,pr as hn,q as gn,qa as _n,qi as vn,qr as yn,ri as bn,rt as xn,sn as Sn,ta as Cn,tr as wn,vt as Tn,wi as En,wt as Dn,x as On,xi as kn,xn as An,y as jn,yn as Mn,yr as Nn,yt as Pn,z as K,za as Fn,zr as q,zt as In}from"./vendor-streamdown-CYxShiF9.js";import{Ft as Ln,Hn as Rn,Nn as J,Ot as zn,Pn as Bn,Yt as Vn,ar as Hn,bn as Un,or as Wn,qn as Y,s as Gn,xn as Kn,zt as qn}from"./vendor-ai-sdk-react-DzHUzjJV.js";var X=e(Le()),Jn=e(ze()),Z=tt();function Yn(e){throw Error(`Unreachable`)}function Xn(e){return typeof e==`number`||e===null}function Zn(e){return typeof e==`string`||e===null}function Qn(e){return Zn(e)||e===void 0}function $n(e){return Array.isArray(e)?e.every(e=>typeof e==`string`):!1}function er(e){return typeof e==`object`&&!!e}function tr(e){return er(e)&&Object.keys(e).every(e=>typeof e==`string`)}var nr=()=>e=>e;(0,X.createContext)(null);var rr=5e3,ir=new Se({maxVisibleToasts:3}),ar=()=>cr,or=()=>lr,sr=()=>ur;function cr(e){let{expireMs:t,...n}=e,r=t===void 0?rr:t;return ir.add({...n},r===null?void 0:{timeout:r})}function lr(e){let{expireMs:t,...n}=e,r=t===void 0?rr:t;return ir.add({...n,variant:`success`},r===null?void 0:{timeout:r})}function ur(e){let{expireMs:t,...n}=e,r=t===void 0?rr:t;return ir.add({...n,variant:`error`},r===null?void 0:{timeout:r})}function dr(e){return e===`light`||e===`dark`||e===`system`}var fr=`arize-phoenix-theme`,pr=`dark`,mr=`(prefers-color-scheme: dark)`;function hr(){let e=localStorage.getItem(fr);return dr(e)?e:pr}function gr(){return window.matchMedia(mr).matches?`dark`:`light`}var _r=(0,X.createContext)(null);function vr(){let e=(0,X.useContext)(_r);if(e===null)throw Error(`useTheme must be used within a ThemeProvider`);return e}function yr(e){let t=(0,Z.c)(19),n;t[0]===e.themeMode?n=t[1]:(n=()=>e.themeMode||hr(),t[0]=e.themeMode,t[1]=n);let[r,i]=(0,X.useState)(n),a;t[2]===Symbol.for(`react.memo_cache_sentinel`)?(a=e=>{localStorage.setItem(fr,e),i(e)},t[2]=a):a=t[2];let o=a,[s,c]=(0,X.useState)(gr),l;bb0:{if(r===`system`){l=s;break bb0}l=r}let u=l,d,f;t[3]===e.themeMode?(d=t[4],f=t[5]):(d=()=>{e.themeMode&&i(e.themeMode)},f=[e.themeMode,o],t[3]=e.themeMode,t[4]=d,t[5]=f),(0,X.useEffect)(d,f);let p,m;t[6]===Symbol.for(`react.memo_cache_sentinel`)?(p=()=>{let e=window.matchMedia(mr),t=()=>{c(gr())};return e.addEventListener(`change`,t),()=>{e.removeEventListener(`change`,t)}},m=[],t[6]=p,t[7]=m):(p=t[6],m=t[7]),(0,X.useEffect)(p,m);let h,g;t[8]!==e.disableBodyTheme||t[9]!==u?(h=()=>{if(!e.disableBodyTheme)return document.body.classList.add(`theme--${u}`),document.body.classList.add(`theme`),()=>{document.body.classList.remove(`theme--${u}`),document.body.classList.remove(`theme`)}},g=[u,e.disableBodyTheme],t[8]=e.disableBodyTheme,t[9]=u,t[10]=h,t[11]=g):(h=t[10],g=t[11]),(0,X.useEffect)(h,g);let _;t[12]!==s||t[13]!==u||t[14]!==r?(_={theme:u,systemTheme:s,themeMode:r,setThemeMode:o},t[12]=s,t[13]=u,t[14]=r,t[15]=_):_=t[15];let v;return t[16]!==e.children||t[17]!==_?(v=W(_r.Provider,{value:_,children:e.children}),t[16]=e.children,t[17]=_,t[18]=v):v=t[18],v}var br=[`traces`,`spans`,`sessions`,`metrics`],xr=e=>br.includes(e),Sr=[`traffic`,`traces`,`latency`,`cost`,`top_models_by_cost`,`tokens`,`top_models_by_tokens`,`prompt_token_details`,`completion_token_details`,`llm_spans`,`llm_span_errors`,`tool_spans`,`tool_span_errors`,`span_annotations`,`trace_annotations`,`session_annotations`],Cr=e=>Sr.includes(e),wr=[`spans`,`traces`,`sessions`],Tr={spans:[`traffic`],traces:[`traces`,`latency`,`trace_annotations`],sessions:[`traces`,`session_annotations`]},Er=e=>`arize-phoenix-project-${e}`;function Dr({projectId:e}){return{state:C()(u(T(e=>({defaultTab:`spans`,setDefaultTab:t=>{e({defaultTab:t},!1,{type:`setDefaultTab`})},treatOrphansAsRoots:!1,setTreatOrphansAsRoots:t=>{e({treatOrphansAsRoots:t},!1,{type:`setTreatOrphansAsRoots`})},showTableAside:!0,setShowTableAside:t=>{e({showTableAside:t},!1,{type:`setShowTableAside`})},metricChartKeys:Tr,setMetricChartKeys:(t,n)=>{e(e=>({metricChartKeys:{...e.metricChartKeys,[t]:n}}),!1,{type:`setMetricChartKeys`})}})),{name:Er(e),merge:(e,t)=>{let n={...t,...e},r={...Tr};for(let e of wr){let t=n.metricChartKeys?.[e];Array.isArray(t)&&(r[e]=t.filter(Cr).slice(0,3))}return n.metricChartKeys=r,n}}))}}var Or=(0,X.createContext)(null);function kr(e){let t=(0,Z.c)(5),{children:n,projectId:r}=e,i;t[0]===r?i=t[1]:(i=()=>Dr({projectId:r}),t[0]=r,t[1]=i);let[a]=(0,X.useState)(i),o;return t[2]!==n||t[3]!==a?(o=W(Or.Provider,{value:a,children:n}),t[2]=n,t[3]=a,t[4]=o):o=t[4],o}function Ar(e,t){let n=(0,X.useContext)(Or);if(!n)throw Error(`Missing ProjectContext.Provider in the tree`);return c(n.state,e,t)}var jr=[`Python`,`TypeScript`];function Mr(e){return typeof e==`string`&&jr.includes(e)}var Nr=[`npm`,`pnpm`,`bun`],Pr=[`pip`,`uv`],Fr=[...Nr,...Pr];function Ir(e){return typeof e==`string`&&Fr.includes(e)}function Lr(e){return typeof e==`string`&&Pr.includes(e)}function Rr(e){return typeof e==`string`&&Nr.includes(e)}var zr=Intl.DateTimeFormat().resolvedOptions(),Br=[];function Vr(){return zr.locale}function Hr(){return zr.timeZone}function Ur(){return Br.length===0&&(Br=[...Intl.supportedValuesOf(`timeZone`)],Br.includes(`UTC`)||(Br=[`UTC`,...Br])),Object.freeze([...Br])}function Wr(e,t){let n=new Intl.DateTimeFormat(`en-US`,{timeZone:t,year:`numeric`,month:`2-digit`,day:`2-digit`,hour:`2-digit`,minute:`2-digit`,second:`2-digit`,hour12:!1}).formatToParts(e).reduce((e,t)=>(t.type!==`literal`&&(e[t.type]=t.value),e),{}),{year:r,month:i,day:a}=n,o=n.hour;if(o===`24`){o=`00`;let e=new Date(`${r}-${i}-${a}T00:00:00Z`);e.setUTCDate(e.getUTCDate()+1),r=String(e.getUTCFullYear()),i=String(e.getUTCMonth()+1).padStart(2,`0`),a=String(e.getUTCDate()).padStart(2,`0`)}let s=`${r}-${i}-${a}`,c=`${o}:${n.minute}:${n.second}`,l=new Date(`${s}T${c}Z`).getTime(),u=Math.round((l-e.getTime())/6e4),d=u>=0?`+`:`-`,f=Math.abs(u);return`${s}T${c}${d}${String(Math.floor(f/60)).padStart(2,`0`)}:${String(f%60).padStart(2,`0`)}`}var Gr={Python:Pr,TypeScript:Nr},Kr={Python:`pip`,TypeScript:`npm`},qr=[``,`apac`,`au`,`ca`,`eu`,`global`,`il`,`jp`,`us`,`us-gov`],Jr=e=>C()(u(T(t=>({markdownDisplayMode:`text`,setMarkdownDisplayMode:e=>{t({markdownDisplayMode:e},!1,{type:`setMarkdownDisplayMode`})},traceStreamingEnabled:!0,setTraceStreamingEnabled:e=>{t({traceStreamingEnabled:e},!1,{type:`setTraceStreamingEnabled`})},lastNTimeRangeKey:`7d`,setLastNTimeRangeKey:e=>{t({lastNTimeRangeKey:e})},projectsAutoRefreshEnabled:!0,setProjectAutoRefreshEnabled:e=>{t({projectsAutoRefreshEnabled:e},!1,{type:`setProjectAutoRefreshEnabled`})},showMetricsInTraceTree:!0,setShowMetricsInTraceTree:e=>{t({showMetricsInTraceTree:e},!1,{type:`setShowMetricsInTraceTree`})},areTableRowsExpanded:!1,setAreTableRowsExpanded:e=>{t({areTableRowsExpanded:e},!1,{type:`setAreTableRowsExpanded`})},modelConfigByProvider:{},setModelConfigForProvider:({provider:e,modelConfig:n})=>{t(t=>({modelConfigByProvider:{...t.modelConfigByProvider,[e]:n}}),!1,{type:`setModelConfigForProvider`})},playgroundStreamingEnabled:!0,setPlaygroundStreamingEnabled:e=>{t({playgroundStreamingEnabled:e},!1,{type:`setPlaygroundStreamingEnabled`})},isAnnotatingSpans:!1,setIsAnnotatingSpans:e=>{t({isAnnotatingSpans:e},!1,{type:`setIsAnnotatingSpans`})},projectViewMode:`grid`,setProjectViewMode:e=>{t({projectViewMode:e},!1,{type:`setProjectViewMode`})},projectSortOrder:{column:`endTime`,direction:`desc`},setProjectSortOrder:e=>{t({projectSortOrder:e},!1,{type:`setProjectSortOrder`})},lastSelectedDashboardProjectId:void 0,setLastSelectedDashboardProjectId:e=>{t({lastSelectedDashboardProjectId:e},!1,{type:`setLastSelectedDashboardProjectId`})},isSideNavExpanded:!0,setIsSideNavExpanded:e=>{t({isSideNavExpanded:e},!1,{type:`setIsSideNavExpanded`})},setDisplayTimezone:e=>{if(e&&!Ur().includes(e))throw Error(`Invalid timezone: ${e}`);t({displayTimezone:e},!1,{type:`setDisplayTimezone`})},programmingLanguage:`Python`,setProgrammingLanguage:e=>{t({programmingLanguage:e},!1,{type:`setProgrammingLanguage`})},packageManagerByLanguage:{...Kr},setPackageManager:(e,n)=>{t(t=>({packageManagerByLanguage:{...t.packageManagerByLanguage,[e]:n}}),!1,{type:`setPackageManager`})},awsBedrockModelPrefix:`us`,setAwsBedrockModelPrefix:e=>{t({awsBedrockModelPrefix:e},!1,{type:`setAwsBedrockModelPrefix`})},isAssistantAgentEnabled:!0,setIsAssistantAgentEnabled:e=>{t({isAssistantAgentEnabled:e},!1,{type:`setIsAssistantAgentEnabled`})},defaultModelProvider:void 0,setDefaultModelProvider:e=>{t({defaultModelProvider:e},!1,{type:`setDefaultModelProvider`})},defaultModelName:void 0,setDefaultModelName:e=>{let n=e?.trim();t({defaultModelName:n||void 0},!1,{type:`setDefaultModelName`})},...e}),{name:`preferencesStore`}),{name:`arize-phoenix-preferences`})),Yr=(0,X.createContext)(null);function Xr(e){let t=(0,Z.c)(8),n,r;t[0]===e?(n=t[1],r=t[2]):({children:n,...r}=e,t[0]=e,t[1]=n,t[2]=r);let i;t[3]===r?i=t[4]:(i=()=>Jr(r),t[3]=r,t[4]=i);let[a]=(0,X.useState)(i),o;return t[5]!==n||t[6]!==a?(o=W(Yr.Provider,{value:a,children:n}),t[5]=n,t[6]=a,t[7]=o):o=t[7],o}function Zr(e,t){let n=(0,X.useContext)(Yr);if(!n)throw Error(`Missing PreferencesContext.Provider in the tree`);return c(n,e,t)}var Qr=function(){var e={alias:null,args:null,kind:`ScalarField`,name:`id`,storageKey:null},t={alias:null,args:null,kind:`ScalarField`,name:`name`,storageKey:null},n={alias:null,args:null,kind:`ScalarField`,name:`createdAt`,storageKey:null},r={alias:null,args:null,kind:`ScalarField`,name:`expiresAt`,storageKey:null};return{fragment:{argumentDefinitions:[],kind:`Fragment`,metadata:null,name:`ViewerContextRefetchQuery`,selections:[{args:null,kind:`FragmentSpread`,name:`ViewerContext_viewer`}],type:`Query`,abstractKey:null},kind:`Request`,operation:{argumentDefinitions:[],kind:`Operation`,name:`ViewerContextRefetchQuery`,selections:[{alias:null,args:null,concreteType:`User`,kind:`LinkedField`,name:`viewer`,plural:!1,selections:[e,{alias:null,args:null,kind:`ScalarField`,name:`username`,storageKey:null},{alias:null,args:null,kind:`ScalarField`,name:`email`,storageKey:null},{alias:null,args:null,kind:`ScalarField`,name:`profilePictureUrl`,storageKey:null},{alias:null,args:null,kind:`ScalarField`,name:`isManagementUser`,storageKey:null},{alias:null,args:null,concreteType:`UserRole`,kind:`LinkedField`,name:`role`,plural:!1,selections:[t,e],storageKey:null},{alias:null,args:null,kind:`ScalarField`,name:`authMethod`,storageKey:null},{alias:null,args:null,concreteType:`UserApiKey`,kind:`LinkedField`,name:`apiKeys`,plural:!0,selections:[e,t,{alias:null,args:null,kind:`ScalarField`,name:`description`,storageKey:null},n,r],storageKey:null},{alias:null,args:null,concreteType:`OAuth2Grant`,kind:`LinkedField`,name:`oauth2Grants`,plural:!0,selections:[e,{alias:null,args:null,kind:`ScalarField`,name:`clientName`,storageKey:null},{alias:null,args:null,kind:`ScalarField`,name:`clientId`,storageKey:null},{alias:null,args:null,kind:`ScalarField`,name:`isFirstParty`,storageKey:null},{alias:null,args:null,kind:`ScalarField`,name:`scopes`,storageKey:null},n,r,{alias:null,args:null,kind:`ScalarField`,name:`lastUsedAt`,storageKey:null}],storageKey:null}],storageKey:null}]},params:{cacheID:`67fdf1bb616d5781701a75f68282f178`,id:null,metadata:{},name:`ViewerContextRefetchQuery`,operationKind:`query`,text:`query ViewerContextRefetchQuery {
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
`}}}();Qr.hash=`53341d080ff76da24b2f1bc9e36c4e23`;var $r={argumentDefinitions:[],kind:`Fragment`,metadata:{refetch:{connection:null,fragmentPathInResult:[],operation:Qr}},name:`ViewerContext_viewer`,selections:[{alias:null,args:null,concreteType:`User`,kind:`LinkedField`,name:`viewer`,plural:!1,selections:[{alias:null,args:null,kind:`ScalarField`,name:`id`,storageKey:null},{alias:null,args:null,kind:`ScalarField`,name:`username`,storageKey:null},{alias:null,args:null,kind:`ScalarField`,name:`email`,storageKey:null},{alias:null,args:null,kind:`ScalarField`,name:`profilePictureUrl`,storageKey:null},{alias:null,args:null,kind:`ScalarField`,name:`isManagementUser`,storageKey:null},{alias:null,args:null,concreteType:`UserRole`,kind:`LinkedField`,name:`role`,plural:!1,selections:[{alias:null,args:null,kind:`ScalarField`,name:`name`,storageKey:null}],storageKey:null},{alias:null,args:null,kind:`ScalarField`,name:`authMethod`,storageKey:null},{args:null,kind:`FragmentSpread`,name:`ViewerAPIKeysListFragment`},{args:null,kind:`FragmentSpread`,name:`AuthorizedApplicationsCardFragment`}],storageKey:null}],type:`Query`,abstractKey:null};$r.hash=`53341d080ff76da24b2f1bc9e36c4e23`;var ei=se(),ti=X.createContext({viewer:null,refetchViewer:()=>{}});function ni(){let e=X.useContext(ti);if(e==null)throw Error(`useViewer must be used within a ViewerProvider`);return e}function ri(){let{viewer:e}=ni();return!(e&&e.role.name===`VIEWER`)}function ii(){let e=ai();return!window.Config.authenticationEnabled||e}function ai(){let{viewer:e}=ni();return window.Config.authenticationEnabled&&e?.role?.name===`ADMIN`}function oi(){return ii()}function si(){return ii()}function ci(){return ii()}function li(){return ii()}function ui(){return ii()}function di(e){let t=(0,Z.c)(9),{query:n,children:r}=e,i;t[0]===Symbol.for(`react.memo_cache_sentinel`)?(i=$r,t[0]=i):i=t[0];let[a,o]=(0,ei.useRefetchableFragment)(i,n),s;t[1]===o?s=t[2]:(s=()=>{(0,X.startTransition)(()=>{o({},{fetchPolicy:`network-only`})})},t[1]=o,t[2]=s);let c=s,l;t[3]!==a.viewer||t[4]!==c?(l={viewer:a.viewer,refetchViewer:c},t[3]=a.viewer,t[4]=c,t[5]=l):l=t[5];let u;return t[6]!==r||t[7]!==l?(u=W(ti.Provider,{value:l,children:r}),t[6]=r,t[7]=l,t[8]=u):u=t[8],u}var fi={OPENAI:`OpenAI`,AZURE_OPENAI:`Azure OpenAI`,ANTHROPIC:`Anthropic`,GOOGLE:`Google`,DEEPSEEK:`DeepSeek`,XAI:`xAI`,OLLAMA:`Ollama`,AWS:`AWS Bedrock`,CEREBRAS:`Cerebras`,FIREWORKS:`Fireworks`,GROQ:`Groq`,MOONSHOT:`Moonshot`,PERPLEXITY:`Perplexity`,TOGETHER:`Together`},pi=`OPENAI`,mi=`gpt-5.6-luna`,hi=`user`,gi=`RESPONSES`,_i={user:[`user`,`human`],ai:[`assistant`,`bot`,`ai`,`model`],system:[`system`,`developer`],tool:[`tool`]},vi={OPENAI:[{envVarName:`OPENAI_API_KEY`,isRequired:!0}],AZURE_OPENAI:[{envVarName:`AZURE_OPENAI_API_KEY`,isRequired:!0}],ANTHROPIC:[{envVarName:`ANTHROPIC_API_KEY`,isRequired:!0}],GOOGLE:[{envVarName:`GEMINI_API_KEY`,isRequired:!0}],DEEPSEEK:[{envVarName:`DEEPSEEK_API_KEY`,isRequired:!0}],XAI:[{envVarName:`XAI_API_KEY`,isRequired:!0}],OLLAMA:[],CEREBRAS:[{envVarName:`CEREBRAS_API_KEY`,isRequired:!0}],FIREWORKS:[{envVarName:`FIREWORKS_API_KEY`,isRequired:!0}],GROQ:[{envVarName:`GROQ_API_KEY`,isRequired:!0}],MOONSHOT:[{envVarName:`MOONSHOT_API_KEY`,isRequired:!0}],PERPLEXITY:[{envVarName:`PERPLEXITY_API_KEY`,isRequired:!0}],TOGETHER:[{envVarName:`TOGETHER_API_KEY`,isRequired:!0}],AWS:[{envVarName:`AWS_ACCESS_KEY_ID`,isRequired:!0},{envVarName:`AWS_SECRET_ACCESS_KEY`,isRequired:!0},{envVarName:`AWS_SESSION_TOKEN`,isRequired:!1}]},yi=`api_key`,bi=`default_credentials`,xi={OPENAI:`OPENAI`,AZURE_OPENAI:`AZURE_OPENAI`,ANTHROPIC:`ANTHROPIC`,AWS_BEDROCK:`AWS`,GOOGLE_GENAI:`GOOGLE`},Si={openai:`OPENAI`,azure:`AZURE_OPENAI`,anthropic:`ANTHROPIC`,aws:`AWS`,google:`GOOGLE`,xai:`XAI`,ollama:`OLLAMA`,deepseek:`DEEPSEEK`,cerebras:`CEREBRAS`,fireworks:`FIREWORKS`,groq:`GROQ`,moonshot:`MOONSHOT`,perplexity:`PERPLEXITY`,together:`TOGETHER`},Ci=Object.entries({OPENAI:`OpenAI`,AZURE_OPENAI:`Azure OpenAI`,ANTHROPIC:`Anthropic`,AWS_BEDROCK:`AWS Bedrock`,GOOGLE_GENAI:`Google GenAI`}).map(([e,t])=>({id:e,label:t})),wi={OPENAI:`openai`,AZURE_OPENAI:`azure`,ANTHROPIC:`anthropic`,AWS_BEDROCK:`aws`,GOOGLE_GENAI:`google`},Ti=Object.entries({api_key:`API Key`,ad_token_provider:`Azure AD Token Provider`,default_credentials:`Default Credentials (Managed Identity)`}).map(([e,t])=>({id:e,label:t})),Ei=Object.entries({default_credentials:`Default Credentials (IAM Role)`,access_keys:`Access Keys`}).map(([e,t])=>({id:e,label:t}));function Di(e){let t=(0,Z.c)(4),n;t[0]===Symbol.for(`react.memo_cache_sentinel`)?(n=q`
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
        `,t[1]=r):r=t[1];let i;return t[2]===e?i=t[3]:(i=W(`div`,{className:`link-container`,onClick:Oi,css:n,children:W(Jt,{css:r,...e})}),t[2]=e,t[3]=i),i}function Oi(e){return e.stopPropagation()}function ki(e){let t=(0,Z.c)(5),{href:n,children:r}=e,i;t[0]===Symbol.for(`react.memo_cache_sentinel`)?(i=q`
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
      `,t[0]=i):i=t[0];let a;t[1]===Symbol.for(`react.memo_cache_sentinel`)?(a=W(H,{svg:W(qe,{})}),t[1]=a):a=t[1];let o;return t[2]!==r||t[3]!==n?(o=G(`a`,{href:n,target:`_blank`,css:i,rel:`noreferrer`,children:[r,a]}),t[2]=r,t[3]=n,t[4]=o):o=t[4],o}var Ai=q`
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
      animation: ${Ke`
  100% {
    transform: rotate(360deg);
  }
`} 3s linear infinite;
    }
    .progress-circle__arc {
      animation: ${Ke`
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
`} 3s cubic-bezier(0.4, 0, 0.2, 1) infinite;
      stroke-dasharray:
        calc(var(--progress-circle-circumference) * 0.25),
        var(--progress-circle-circumference);
      stroke-dashoffset: 0;
    }
  }
`,ji=q`
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
`;function Mi(e){let t=(0,Z.c)(13),n,r;t[0]===e?(n=t[1],r=t[2]):({ref:r,...n}=e,t[0]=e,t[1]=n,t[2]=r);let{isIndeterminate:i,value:a,size:o}=n,s=i!==void 0&&i,c=o===void 0?`M`:o,l=s||void 0,u;t[3]!==s||t[4]!==a?(u=!s&&a!=null?{"--progress-circle-value":a}:void 0,t[3]=s,t[4]=a,t[5]=u):u=t[5];let d;t[6]===Symbol.for(`react.memo_cache_sentinel`)?(d=G(`svg`,{className:`progress-circle__svg`,children:[W(`circle`,{className:`progress-circle__background`}),W(`circle`,{className:`progress-circle__arc`})]}),t[6]=d):d=t[6];let f;return t[7]!==n||t[8]!==r||t[9]!==c||t[10]!==l||t[11]!==u?(f=W(vn,{...n,"data-size":c,"data-indeterminate":l,css:Ai,ref:r,style:u,children:d}),t[7]=n,t[8]=r,t[9]=c,t[10]=l,t[11]=u,t[12]=f):f=t[12],f}function Ni(e){let t=(0,Z.c)(12),n,r,i,a;t[0]===e?(n=t[1],r=t[2],i=t[3],a=t[4]):({ref:i,width:a,height:n,...r}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a);let o;t[5]!==n||t[6]!==a?(o={width:a,height:n},t[5]=n,t[6]=a,t[7]=o):o=t[7];let s;return t[8]!==r||t[9]!==i||t[10]!==o?(s=W(vn,{...r,ref:i,css:ji,style:o,children:Pi}),t[8]=r,t[9]=i,t[10]=o,t[11]=s):s=t[11],s}function Pi(e){let{percentage:t}=e;return W(`div`,{className:`progress-bar__track`,children:W(`div`,{className:`progress-bar__fill`,style:{width:t+`%`}})})}function Fi(e){let t=(0,Z.c)(7),{ref:n,...r}=e,{children:i,elementType:a,...o}=r,s=a===void 0?`div`:a,{styleProps:c}=hn(r,dn),l=sn(o),u;t[0]===Symbol.for(`react.memo_cache_sentinel`)?(u=q`
        overflow: hidden;
        box-sizing: border-box;
      `,t[0]=u):u=t[0];let d;return t[1]!==s||t[2]!==i||t[3]!==n||t[4]!==c||t[5]!==l?(d=W(s,{...l,...c,ref:n,css:u,className:`view`,children:i}),t[1]=s,t[2]=i,t[3]=n,t[4]=c,t[5]=l,t[6]=d):d=t[6],d}var Ii=q`
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
`,Li=q`
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
`;function Ri(e){let t=(0,Z.c)(10),n,r,i,a;if(t[0]!==e){let{ref:o,...s}=e,{css:c,...l}=s;n=p,r=l,i=o,a=q(Ii,c),t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a}else n=t[1],r=t[2],i=t[3],a=t[4];let o;return t[5]!==n||t[6]!==r||t[7]!==i||t[8]!==a?(o=W(n,{...r,ref:i,css:a}),t[5]=n,t[6]=r,t[7]=i,t[8]=a,t[9]=o):o=t[9],o}function zi(e){let t=(0,Z.c)(8),n,r;t[0]===e?(n=t[1],r=t[2]):({ref:r,...n}=e,t[0]=e,t[1]=n,t[2]=r);let{css:i}=n,a;t[3]===Symbol.for(`react.memo_cache_sentinel`)?(a=B(`react-aria-OverlayArrow`),t[3]=a):a=t[3];let o;t[4]===Symbol.for(`react.memo_cache_sentinel`)?(o=W(`svg`,{width:8,height:8,viewBox:`0 0 8 8`,children:W(`path`,{d:`M0 0 L4 4 L8 0`})}),t[4]=o):o=t[4];let s;return t[5]!==i||t[6]!==r?(s=W(Ht,{ref:r,css:i,className:a,children:o}),t[5]=i,t[6]=r,t[7]=s):s=t[7],s}var Bi=1e3,Vi=60*Bi,Hi=60*Vi,Ui=24*Hi;7*Ui;var Wi=30*Ui,Gi=3600*24*365,Ki=3600*24*30,qi=3600*24*7,Ji=3600*24,Yi=3600,Xi=`https://arize.com/docs/phoenix`,Zi={accessControl:`${Xi}/settings/access-control-rbac`,annotationConfigs:`${Xi}/tracing/how-to-tracing/feedback-and-annotations/annotating-in-the-ui`,apiKeys:`${Xi}/settings/api-keys`,customAiProviders:`${Xi}/settings/custom-ai-providers`,dataRetention:`${Xi}/settings/data-retention`,datasetLabels:`${Xi}/release-notes/10-2025/10-08-2025-dataset-labels`,modelCostTracking:`${Xi}/tracing/how-to-tracing/cost-tracking`,remoteMcpServer:`${Xi}/integrations/remote-mcp`,promptLabels:`${Xi}/release-notes/09-2025/09-15-2025-prompt-labels`,providers:`${Xi}/prompt-engineering/how-to-prompts/configure-ai-providers`,pxi:`${Xi}/pxi`,sandboxes:`${Xi}/settings/sandboxes`,secrets:`${Xi}/settings/secrets`},Qi={aiProviderSettings:{href:Zi.providers,label:`AI provider settings`},aiProviders:{href:Zi.providers,label:`AI providers`},annotationConfigs:{href:Zi.annotationConfigs,label:`annotation configs`},apiKeys:{href:Zi.apiKeys,label:`API keys`},customAiProviders:{href:Zi.customAiProviders,label:`custom AI providers`},dataRetention:{href:Zi.dataRetention,label:`data retention`},datasetLabels:{href:Zi.datasetLabels,label:`dataset labels`},defaultRetentionPolicy:{href:Zi.dataRetention,label:`the default retention policy`},modelPricing:{href:Zi.modelCostTracking,label:`model pricing`},promptLabels:{href:Zi.promptLabels,label:`prompt labels`},pxi:{href:Zi.pxi,label:`PXI`},sandboxConfigurations:{href:Zi.sandboxes,label:`sandbox configurations`},sandboxProviders:{href:Zi.sandboxes,label:`sandbox providers`},secrets:{href:Zi.secrets,label:`secrets`},userAccess:{href:Zi.accessControl,label:`user access`}},$i=e=>{switch(e){case`info`:return W(zt,{});default:return W(ot,{})}},ea=q`
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
`,ta=e=>{let t=(0,Z.c)(22),n,r,i,a,o;t[0]===e?(n=t[1],r=t[2],i=t[3],a=t[4],o=t[5]):({children:n,href:r,triggerAriaLabel:i,variant:a,...o}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a,t[5]=o);let s=i===void 0?`More information`:i,c=a===void 0?`help`:a,l;t[6]===c?l=t[7]:(l=$i(c),t[6]=c,t[7]=l);let u;t[8]===l?u=t[9]:(u=W(H,{svg:l}),t[8]=l,t[9]=u);let d;t[10]!==u||t[11]!==s?(d={"aria-label":s,css:ea,leadingVisual:u,size:`S`,variant:`quiet`},t[10]=u,t[11]=s,t[12]=d):d=t[12];let f=d,p;t[13]!==r||t[14]!==f?(p=r?W(m,{children:W(gt,{...f,href:r})}):W(yt,{...f}),t[13]=r,t[14]=f,t[15]=p):p=t[15];let h;t[16]!==n||t[17]!==o?(h=W(Ri,{...o,children:n}),t[16]=n,t[17]=o,t[18]=h):h=t[18];let g;return t[19]!==p||t[20]!==h?(g=G(A,{delay:0,children:[p,h]}),t[19]=p,t[20]=h,t[21]=g):g=t[21],g},na=q`
  margin-top: var(--global-dimension-size-100);
`;function ra(e){let t=(0,Z.c)(9),{children:n,topic:r}=e,{href:i,label:a}=Qi[r],o=`Learn more about ${a}`,s;t[0]===n?s=t[1]:(s=W(V,{size:`S`,children:n}),t[0]=n,t[1]=s);let c;t[2]===i?c=t[3]:(c=W(`footer`,{css:na,children:W(ki,{href:i,children:`View documentation`})}),t[2]=i,t[3]=c);let l;return t[4]!==i||t[5]!==o||t[6]!==s||t[7]!==c?(l=G(ta,{href:i,variant:`info`,triggerAriaLabel:o,children:[s,c]}),t[4]=i,t[5]=o,t[6]=s,t[7]=c,t[8]=l):l=t[8],l}function ia(e){let t=(0,Z.c)(8),n,r;t[0]===e?(n=t[1],r=t[2]):({children:n,...r}=e,t[0]=e,t[1]=n,t[2]=r);let i;t[3]===n?i=t[4]:(i=W(`div`,{role:`button`,children:n}),t[3]=n,t[4]=i);let a;return t[5]!==r||t[6]!==i?(a=W(m,{...r,children:i}),t[5]=r,t[6]=i,t[7]=a):a=t[7],a}function aa(e){let t=(0,Z.c)(16),n,r,i,a,o,s;if(t[0]!==e){let{ref:c,...l}=e,{children:u,css:d,width:f,...m}=l;r=u,s=f,n=p,i=m,a=c,o=q(Li,d),t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a,t[5]=o,t[6]=s}else n=t[1],r=t[2],i=t[3],a=t[4],o=t[5],s=t[6];let c;t[7]===s?c=t[8]:(c=s?{width:s}:{maxWidth:`300px`},t[7]=s,t[8]=c);let l;return t[9]!==n||t[10]!==r||t[11]!==i||t[12]!==a||t[13]!==o||t[14]!==c?(l=W(n,{...i,ref:a,css:o,style:c,children:r}),t[9]=n,t[10]=r,t[11]=i,t[12]=a,t[13]=o,t[14]=c,t[15]=l):l=t[15],l}function oa(e){let t=(0,Z.c)(3),{children:n}=e,r;t[0]===Symbol.for(`react.memo_cache_sentinel`)?(r=q`
        margin-bottom: var(--global-dimension-size-100);
      `,t[0]=r):r=t[0];let i;return t[1]===n?i=t[2]:(i=W(Qe,{level:4,css:r,children:n}),t[1]=n,t[2]=i),i}function sa(e){let t=(0,Z.c)(3),{children:n}=e,r;t[0]===Symbol.for(`react.memo_cache_sentinel`)?(r=q`
        margin-bottom: var(--global-dimension-size-100);
      `,t[0]=r):r=t[0];let i;return t[1]===n?i=t[2]:(i=W(V,{size:`S`,color:`text-700`,css:r,children:n}),t[1]=n,t[2]=i),i}function ca(e){let t=(0,Z.c)(2),{children:n}=e,r;return t[0]===n?r=t[1]:(r=W(Fi,{paddingTop:`size-50`,children:n}),t[0]=n,t[1]=r),r}var la=2e3,ua=q`
  flex: none;
  box-sizing: content-box;
`;function da(e){let t=(0,Z.c)(20),n,r,i,a;t[0]===e?(n=t[1],r=t[2],i=t[3],a=t[4]):({text:a,size:r,tooltipText:i,...n}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a);let o=r===void 0?`S`:r,s=i===void 0?`Copy`:i,[c,l]=(0,X.useState)(!1),u;t[5]===a?u=t[6]:(u=()=>{x(typeof a==`string`?a:a.current||``),l(!0),setTimeout(()=>{l(!1)},la)},t[5]=a,t[6]=u);let d=u,f=c?`success`:`inherit`,p=c?`Checkmark`:`Duplicate`,m;t[7]!==f||t[8]!==p?(m=W(H,{color:f,svgKey:p}),t[7]=f,t[8]=p,t[9]=m):m=t[9];let h;t[10]!==d||t[11]!==n||t[12]!==o||t[13]!==m?(h=W(yt,{size:o,leadingVisual:m,onPress:d,...n,className:`copy-button`}),t[10]=d,t[11]=n,t[12]=o,t[13]=m,t[14]=h):h=t[14];let g;t[15]===s?g=t[16]:(g=W(Ri,{offset:1,children:s}),t[15]=s,t[16]=g);let _;return t[17]!==h||t[18]!==g?(_=W(`div`,{className:`copy-to-clipboard-button`,css:ua,children:G(A,{children:[h,g]})}),t[17]=h,t[18]=g,t[19]=_):_=t[19],_}var fa=q`
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
`,pa=nt,ma=e=>{let t=(0,Z.c)(10),n,r,i;t[0]===e?(n=t[1],r=t[2],i=t[3]):({className:n,onKeyDown:r,...i}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i);let a;t[4]===n?a=t[5]:(a=B(`react-aria-Menu`,n),t[4]=n,t[5]=a);let o;return t[6]!==r||t[7]!==i||t[8]!==a?(o=W(lt,{className:a,css:fa,...i,onKeyDown:r}),t[6]=r,t[7]=i,t[8]=a,t[9]=o):o=t[9],o},ha=q`
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
`,ga=e=>{let t=(0,Z.c)(18),n,r,i,a,o;t[0]===e?(n=t[1],r=t[2],i=t[3],a=t[4],o=t[5]):({className:n,trailingContent:o,leadingContent:r,ref:a,...i}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a,t[5]=o);let s=i.textValue||(typeof i.children==`string`?i.children:void 0),c;t[6]===n?c=t[7]:(c=B(`react-aria-MenuItem`,n),t[6]=n,t[7]=c);let l;t[8]!==r||t[9]!==i||t[10]!==o?(l=e=>{let{hasSubmenu:t,isSelected:n,selectionMode:a}=e;return G(U,{children:[n&&W(H,{svg:W(fn,{})}),a!==`none`&&!n&&W(H,{svg:W(fn,{}),css:q`
                  visibility: hidden;
                `}),W(_a,{trailingContent:o,leadingContent:r,children:typeof i.children==`function`?i.children(e):i.children}),t&&W(H,{svg:W(Pn,{})})]})},t[8]=r,t[9]=i,t[10]=o,t[11]=l):l=t[11];let u;return t[12]!==i||t[13]!==a||t[14]!==c||t[15]!==l||t[16]!==s?(u=W(pt,{ref:a,...i,css:ha,className:c,textValue:s,children:l}),t[12]=i,t[13]=a,t[14]=c,t[15]=l,t[16]=s,t[17]=u):u=t[17],u},_a=e=>{let t=(0,Z.c)(7),{children:n,trailingContent:r,leadingContent:i}=e,a;t[0]===Symbol.for(`react.memo_cache_sentinel`)?(a=q`
        padding: var(--global-menu-item-gap);
      `,t[0]=a):a=t[0];let o;t[1]!==n||t[2]!==i?(o=i?G(K,{alignItems:`center`,gap:`var(--global-menu-item-content-gap)`,children:[i,` `,n]}):n,t[1]=n,t[2]=i,t[3]=o):o=t[3];let s;return t[4]!==o||t[5]!==r?(s=G(K,{direction:`row`,alignItems:`center`,justifyContent:`space-between`,gap:`var(--global-menu-split-item-content-gap)`,minWidth:0,flex:1,css:a,children:[o,r]}),t[4]=o,t[5]=r,t[6]=s):s=t[6],s},va=q`
  overflow-y: hidden;
  display: flex;
  flex-direction: column;
`,ya=e=>{let t=(0,Z.c)(19),n,r,i,a,o,s;t[0]===e?(n=t[1],r=t[2],i=t[3],a=t[4],o=t[5],s=t[6]):({children:n,placement:i,minHeight:a,maxHeight:o,maxWidth:s,...r}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a,t[5]=o,t[6]=s);let c=i===void 0?`bottom end`:i,l=a===void 0?`var(--global-menu-min-height)`:a,u=o===void 0?`var(--global-menu-max-height-large)`:o,d=s===void 0?450:s,f;t[7]!==u||t[8]!==d||t[9]!==l?(f={minHeight:l,maxHeight:u,maxWidth:d},t[7]=u,t[8]=d,t[9]=l,t[10]=f):f=t[10];let p;t[11]===Symbol.for(`react.memo_cache_sentinel`)?(p=q`
          display: flex;
          flex-direction: column;
          height: 100%;
          min-width: 300px;
        `,t[11]=p):p=t[11];let m;t[12]!==n||t[13]!==f?(m=W(`div`,{style:f,css:p,children:n}),t[12]=n,t[13]=f,t[14]=m):m=t[14];let h;return t[15]!==c||t[16]!==r||t[17]!==m?(h=W(jn,{shouldFlip:!1,placement:c,css:va,...r,children:m}),t[15]=c,t[16]=r,t[17]=m,t[18]=h):h=t[18],h},ba=q`
  padding: var(--global-dimension-size-50) var(--global-dimension-size-100) 0;
`,xa=e=>{let t=(0,Z.c)(5),{title:n,trailingContent:r}=e,i;t[0]===n?i=t[1]:(i=W(V,{weight:`heavy`,children:n}),t[0]=n,t[1]=i);let a;return t[2]!==i||t[3]!==r?(a=W(on,{css:ba,children:G(K,{justifyContent:`space-between`,alignItems:`center`,children:[i,r]})}),t[2]=i,t[3]=r,t[4]=a):a=t[4],a},Sa=e=>{let t=(0,Z.c)(3),{children:n}=e,r;t[0]===Symbol.for(`react.memo_cache_sentinel`)?(r=q`
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
      `,t[0]=r):r=t[0];let i;return t[1]===n?i=t[2]:(i=W(`div`,{className:`menu-header`,css:r,children:n}),t[1]=n,t[2]=i),i},Ca=e=>{let t=(0,Z.c)(8),{children:n,leadingContent:r,trailingContent:i}=e,a;t[0]===Symbol.for(`react.memo_cache_sentinel`)?(a=q`
        padding: var(--global-dimension-size-100);
        border-bottom: 1px solid var(--global-menu-border-color);
      `,t[0]=a):a=t[0];let o;t[1]===Symbol.for(`react.memo_cache_sentinel`)?(o=q`
          flex: 1 1 auto;
          width: 100%;
          padding-left: var(--global-dimension-size-50);
        `,t[1]=o):o=t[1];let s;t[2]===n?s=t[3]:(s=W(Qe,{level:4,weight:`heavy`,css:o,children:n}),t[2]=n,t[3]=s);let c;return t[4]!==r||t[5]!==s||t[6]!==i?(c=G(K,{direction:`row`,gap:`size-50`,alignItems:`center`,wrap:`nowrap`,minHeight:30,"data-testid":`menu-header-title`,css:a,children:[r,s,i]}),t[4]=r,t[5]=s,t[6]=i,t[7]=c):c=t[7],c},wa=e=>{let t=(0,Z.c)(3),{children:n}=e,r;t[0]===Symbol.for(`react.memo_cache_sentinel`)?(r=q`
        padding: var(--global-dimension-size-100);
        border-top: 1px solid var(--global-menu-border-color);
        display: flex;
        flex-direction: column;
        flex-shrink: 0;
        gap: var(--global-dimension-size-50);
      `,t[0]=r):r=t[0];let i;return t[1]===n?i=t[2]:(i=W(`div`,{css:r,children:n}),t[1]=n,t[2]=i),i},Ta=e=>{let t=(0,Z.c)(3),{children:n}=e,r;t[0]===Symbol.for(`react.memo_cache_sentinel`)?(r=q`
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
      `,t[0]=r):r=t[0];let i;return t[1]===n?i=t[2]:(i=W(V,{color:`gray-400`,fontStyle:`italic`,css:r,children:n}),t[1]=n,t[2]=i),i},Ea=q`
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
`;function Da(e){let t=(0,Z.c)(10),n,r,i;t[0]===e?(n=t[1],r=t[2],i=t[3]):({ref:i,css:n,...r}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i);let a;t[4]===n?a=t[5]:(a=q(Ea,n),t[4]=n,t[5]=a);let o;return t[6]!==r||t[7]!==i||t[8]!==a?(o=W(yt,{ref:i,css:a,...r}),t[6]=r,t[7]=i,t[8]=a,t[9]=o):o=t[9],o}function Oa(e){let t=(0,Z.c)(5),{children:n,isPlaceholder:r}=e,i=r&&`menu-button__value--placeholder`,a;t[0]===i?a=t[1]:(a=B(`menu-button__value`,i),t[0]=i,t[1]=a);let o;return t[2]!==n||t[3]!==a?(o=W(`span`,{className:a,children:n}),t[2]=n,t[3]=a,t[4]=o):o=t[4],o}var ka=2e3;function Aa(e){let t=(0,Z.c)(18),{items:n}=e,[r,i]=(0,X.useState)(null),a=(0,X.useRef)(null),o;t[0]===n?o=t[1]:(o=e=>{let t=n.find(t=>t.name===e);t&&(x(t.value),i(t.name),a.current&&clearTimeout(a.current),a.current=setTimeout(()=>{i(null)},ka))},t[0]=n,t[1]=o);let s=o,c=r==null?`Duplicate`:`Checkmark`,l=r==null?`inherit`:`success`,u;t[2]!==c||t[3]!==l?(u=W(H,{svgKey:c,color:l}),t[2]=c,t[3]=l,t[4]=u):u=t[4];let d=r!=null||void 0,f=r==null?void 0:`Copied`,p;t[5]!==u||t[6]!==d||t[7]!==f?(p=W(yt,{size:`S`,variant:`quiet`,"aria-label":`Copy`,leadingVisual:u,className:`copy-action-menu__button`,"data-copied":d,children:f}),t[5]=u,t[6]=d,t[7]=f,t[8]=p):p=t[8];let m;t[9]===Symbol.for(`react.memo_cache_sentinel`)?(m=q`
            --menu-min-width: auto;
          `,t[9]=m):m=t[9];let h;t[10]===n?h=t[11]:(h=n.map(ja),t[10]=n,t[11]=h);let g;t[12]!==s||t[13]!==h?(g=W(jn,{placement:`bottom end`,offset:3,children:W(ma,{onAction:s,css:m,children:h})}),t[12]=s,t[13]=h,t[14]=g):g=t[14];let _;return t[15]!==p||t[16]!==g?(_=G(pa,{children:[p,g]}),t[15]=p,t[16]=g,t[17]=_):_=t[17],_}function ja(e){return W(ga,{id:e.name,textValue:`Copy ${e.name}`,leadingContent:W(H,{svgKey:e.iconKey??`Duplicate`}),children:e.name},e.name)}var Ma=q`
  --embedded-copy-button-size: calc(
    var(--global-input-height-m) - 2 * var(--global-dimension-size-125) +
      var(--global-dimension-size-50)
  );
`,Na=q`
  ${Ma}
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
`,Pa=e=>{let t=(0,Z.c)(6),{children:n,bordered:r}=e,i=r===void 0||r,a;t[0]===Symbol.for(`react.memo_cache_sentinel`)?(a=q`
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
      `,t[0]=a):a=t[0];let o;t[1]===n?o=t[2]:(o=W(Qe,{children:n}),t[1]=n,t[2]=o);let s;return t[3]!==i||t[4]!==o?(s=W(`div`,{"data-bordered":i,css:a,children:o}),t[3]=i,t[4]=o,t[5]=s):s=t[5],s},Fa=[/Unexpected token ['"]?<['"]?/i,/JSON\.parse.*unexpected character/i,/<!DOCTYPE/i,/timeout/i,/502|504|gateway/i];function Ia(e){if(e==null)return!1;let t=e instanceof Error?e.message:e;return typeof t!=`string`||t.length===0?!1:Fa.some(e=>e.test(t))}function La(e){let t=(0,Z.c)(9),{error:n}=e;if(Ia(n)){let e;return t[0]===n?e=t[1]:(e=W(Ra,{error:n}),t[0]=n,t[1]=e),e}let r,i;t[2]===Symbol.for(`react.memo_cache_sentinel`)?(r=W(K,{direction:`column`,width:`100%`,alignItems:`center`,children:W(`h1`,{children:`Something went wrong`})}),i=W(`p`,{children:`We strive to do our very best but 🐛 bugs happen. It would mean a lot to us if you could file a an issue. If you feel comfortable, please include the error details below in your issue. We will get back to you as soon as we can.`}),t[2]=r,t[3]=i):(r=t[2],i=t[3]);let a;t[4]===Symbol.for(`react.memo_cache_sentinel`)?(a=W(K,{direction:`row`,width:`100%`,justifyContent:`end`,children:W(ki,{href:`https://github.com/Arize-ai/phoenix/issues/new?assignees=&labels=bug&template=bug_report.md&title=%5BBUG%5D`,children:`file an issue with us`})}),t[4]=a):a=t[4];let o,s;t[5]===Symbol.for(`react.memo_cache_sentinel`)?(o=W(`summary`,{children:`error details`}),s=q`
              white-space: pre-wrap;
              overflow-wrap: break-word;
              overflow: hidden;
              overflow-y: auto;
              max-height: 500px;
            `,t[5]=o,t[6]=s):(o=t[5],s=t[6]);let c;return t[7]===n?c=t[8]:(c=W(Fi,{padding:`size-200`,children:G(K,{direction:`column`,children:[r,i,a,G(`details`,{open:!0,children:[o,W(`pre`,{css:s,children:n})]})]})}),t[7]=n,t[8]=c),c}function Ra(e){let t=(0,Z.c)(9),{error:n}=e,r,i,a,o;t[0]===Symbol.for(`react.memo_cache_sentinel`)?(r=W(K,{direction:`column`,width:`100%`,alignItems:`center`,children:W(`h1`,{children:`Connection timed out`})}),i=W(`p`,{children:`The connection to the Phoenix server timed out before a response was received. This typically happens when a load balancer or proxy closes the connection before the server can respond.`}),a=W(`p`,{children:`Possible solutions:`}),o=G(`ul`,{css:q`
            margin: var(--global-dimension-size-100) 0;
            padding-left: var(--global-dimension-size-300);
          `,children:[W(`li`,{children:`Increase your load balancer or proxy timeout settings`}),W(`li`,{children:`Check if the Phoenix server is overloaded or slow to respond`}),W(`li`,{children:`Verify network connectivity between components`})]}),t[0]=r,t[1]=i,t[2]=a,t[3]=o):(r=t[0],i=t[1],a=t[2],o=t[3]);let s;t[4]===Symbol.for(`react.memo_cache_sentinel`)?(s=W(K,{direction:`row`,width:`100%`,justifyContent:`end`,children:W(yt,{variant:`primary`,size:`S`,onPress:za,children:`Retry`})}),t[4]=s):s=t[4];let c;t[5]===n?c=t[6]:(c=n&&G(`details`,{children:[W(`summary`,{children:`error details`}),W(`pre`,{css:q`
                white-space: pre-wrap;
                overflow-wrap: break-word;
                overflow: hidden;
                overflow-y: auto;
                max-height: 500px;
              `,children:n})]}),t[5]=n,t[6]=c);let l;return t[7]===c?l=t[8]:(l=W(Fi,{padding:`size-200`,children:G(K,{direction:`column`,children:[r,i,a,o,s,c]})}),t[7]=c,t[8]=l),l}function za(){window.location.reload()}var Ba=class extends X.Component{constructor(e){super(e),this.state={hasError:!1,error:null}}static getDerivedStateFromError(e){return{hasError:!0,error:e}}componentDidCatch(e,t){console.error(`ErrorBoundary caught error:`,e,t)}render(){if(this.state.hasError){let e=this.state.error instanceof Error?this.state.error.message:null;return typeof this.props.fallback==`function`?W(this.props.fallback,{error:e}):W(La,{error:e})}return this.props.children}};function Va({error:e}){let t=G(`div`,{css:q`
        text-align: center;
        display: inline-flex;
        align-items: center;
        color: var(--global-text-color-300);
        gap: var(--global-dimension-size-50);
        cursor: ${e?`help`:`default`};
      `,children:[W(H,{svg:W(dt,{})}),W(V,{color:`text-300`,children:`error`})]});return e?G(A,{delay:200,children:[W(`span`,{tabIndex:0,children:t}),W(p,{offset:6,children:W(Fi,{padding:`size-100`,borderColor:`default`,borderWidth:`thin`,borderRadius:`small`,backgroundColor:`gray-200`,maxWidth:`size-4600`,children:W(`pre`,{css:q`
              white-space: pre-wrap;
              overflow-wrap: break-word;
              margin: 0;
              font-size: var(--global-font-size-xs, 12px);
            `,children:e})})})]}):t}var Ha=q`
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
`,Ua=q`
  background-color: transparent;
  color: var(--ac-global-text-color-500);
  padding: 0 var(--global-dimension-size-75);
  font-size: var(--global-dimension-font-size-50);
  border-radius: var(--global-rounding-small);
  border: 1px solid var(--ac-global-border-color-default);
  text-transform: uppercase;
`;function Wa(e){let t=(0,Z.c)(10),n,r,i,a;t[0]===e?(n=t[1],r=t[2],i=t[3],a=t[4]):({ref:i,children:n,variant:a,...r}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a);let o=(a===void 0?`default`:a)===`quiet`?Ua:Ha,s;return t[5]!==n||t[6]!==r||t[7]!==i||t[8]!==o?(s=W(wt,{ref:i,css:o,...r,children:n}),t[5]=n,t[6]=r,t[7]=i,t[8]=o,t[9]=s):s=t[9],s}function Ga({ref:e,color:t,size:n=`M`,shape:r=`square`}){let i=typeof t==`string`&&t.startsWith(`var`),a=i?q`
        background-color: ${t} !important;
      `:void 0;return W(h,{color:i?void 0:t,"data-shape":r,"data-size":n,ref:e,css:q(q`
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
        `,a)})}Ga.displayName=`ColorSwatch`;var Ka=q`
  opacity: 0.8;
  color: var(--global-text-color-500);
  .theme--dark & {
    color: var(--global-text-color-400);
  }
  .text {
    color: inherit;
  }
`,qa=q`
  margin: var(--global-dimension-size-300);
  display: flex;
  flex-direction: column;
  align-items: center;
`;function Ja(e){let t=(0,Z.c)(7),{message:n,size:r}=e,i=r===void 0?`M`:r,a,o;t[0]===Symbol.for(`react.memo_cache_sentinel`)?(a=q`
        width: 100%;
        display: flex;
        justify-content: center;
      `,o=[qa,Ka],t[0]=a,t[1]=o):(a=t[0],o=t[1]);let s;t[2]!==n||t[3]!==i?(s=n&&W(V,{size:i,children:n}),t[2]=n,t[3]=i,t[4]=s):s=t[4];let c;return t[5]===s?c=t[6]:(c=W(`div`,{css:a,children:W(`div`,{css:o,children:s})}),t[5]=s,t[6]=c),c}var Ya=q`
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
`;function Xa(){let e=(0,Z.c)(2),t=(0,X.useContext)(tn),n=(0,X.useContext)(de),r=t?.inputValue??n?.inputValue??``,i;return e[0]===r?i=e[1]:(i=r.trim(),e[0]=r,e[1]=i),i.length>0}function Za(e){let t=(0,Z.c)(9),{icon:n,description:r,isFiltered:i}=e,a=Xa(),o=i??a,s;t[0]===Symbol.for(`react.memo_cache_sentinel`)?(s=[Ya,Ka],t[0]=s):s=t[0];let c;t[1]!==n||t[2]!==o?(c=o?W(H,{svg:W(Pt,{})}):n,t[1]=n,t[2]=o,t[3]=c):c=t[3];let l=o?`No results`:r,u;t[4]===l?u=t[5]:(u=W(V,{size:`S`,children:l}),t[4]=l,t[5]=u);let d;return t[6]!==c||t[7]!==u?(d=G(`div`,{css:s,children:[c,u]}),t[6]=c,t[7]=u,t[8]=d):d=t[8],d}var Qa=q`
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
`,$a=q`
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
`;function eo(e){let t=(0,Z.c)(14),{icon:n,title:r,description:i,href:a,external:o}=e,s;t[0]===o?s=t[1]:(s=o?{target:`_blank`,rel:`noopener noreferrer`}:void 0,t[0]=o,t[1]=s);let c;t[2]===r?c=t[3]:(c=W(V,{weight:`heavy`,children:r}),t[2]=r,t[3]=c);let l;t[4]!==n||t[5]!==c?(l=G(K,{direction:`row`,gap:`size-100`,alignItems:`center`,children:[n,c]}),t[4]=n,t[5]=c,t[6]=l):l=t[6];let u;t[7]===i?u=t[8]:(u=W(V,{size:`S`,color:`text-700`,css:$a,children:i}),t[7]=i,t[8]=u);let d;return t[9]!==a||t[10]!==s||t[11]!==l||t[12]!==u?(d=G(`a`,{href:a,css:Qa,...s,children:[l,u]}),t[9]=a,t[10]=s,t[11]=l,t[12]=u,t[13]=d):d=t[13],d}function to(e,t,n){return n==null?!1:e===`horizontal`||e!==`vertical`&&t?.type===`cards`&&(t.columns??1)===2&&t.items.length>=3}var no=q`
  max-width: var(--global-dimension-size-4000);
  text-align: center;
  text-wrap: balance;
`,ro=q`
  display: grid;
  gap: var(--global-dimension-size-200);
  width: min(100%, var(--global-dimension-size-4000));
`,io=q`
  width: min(100%, calc(var(--global-dimension-size-4000) * 2));
  grid-template-columns: repeat(
    auto-fit,
    minmax(min(100%, var(--global-dimension-size-4000)), 1fr)
  );
`;function ao(e){let t=(0,Z.c)(14),{action:n}=e;if(n.type===`strip`){let e;t[0]===n.items?e=t[1]:(e=n.items.map(so),t[0]=n.items,t[1]=e);let r;return t[2]===e?r=t[3]:(r=W(K,{direction:`row`,gap:`size-100`,wrap:!0,alignItems:`center`,children:e}),t[2]=e,t[3]=r),r}let r=n.columns??1,i=r===2&&io,a;t[4]===r?a=t[5]:(a=r===1&&q`
            grid-template-columns: 1fr;
          `,t[4]=r,t[5]=a);let o;t[6]!==i||t[7]!==a?(o=[ro,i,a],t[6]=i,t[7]=a,t[8]=o):o=t[8];let s;t[9]===n.items?s=t[10]:(s=n.items.map(oo),t[9]=n.items,t[10]=s);let c;return t[11]!==o||t[12]!==s?(c=W(`div`,{css:o,children:s}),t[11]=o,t[12]=s,t[13]=c):c=t[13],c}function oo(e,t){return W(eo,{...e},t)}function so(e,t){if(e.kind===`link`)return W(gt,{href:e.href,variant:`quiet`,size:`S`,children:e.label},t);if(e.kind===`node`)return W(X.Fragment,{children:e.node},t);let{kind:n,...r}=e;return W(yt,{size:`S`,...r},t)}function co(e){let t=(0,Z.c)(23),{graphic:n,title:r,description:i,action:a,orientation:o}=e,s=to(o===void 0?`auto`:o,a,n),c=a?.type===`cards`?`size-300`:`size-200`,l=a?.type===`cards`?`size-500`:`size-200`,u;t[0]!==i||t[1]!==r?(u=r!=null||i!=null?G(K,{direction:`column`,gap:`size-25`,alignItems:`center`,children:[r!=null&&W(V,{size:`L`,weight:`heavy`,children:r}),i!=null&&W(V,{size:`S`,color:`text-700`,css:no,children:i})]}):null,t[0]=i,t[1]=r,t[2]=u):u=t[2];let d=u;if(s){let e;t[3]===n?e=t[4]:(e=W(K,{alignItems:`center`,justifyContent:`center`,children:n}),t[3]=n,t[4]=e);let r;t[5]!==e||t[6]!==d?(r=G(K,{direction:`row`,wrap:!0,gap:`size-400`,alignItems:`center`,justifyContent:`center`,children:[e,d]}),t[5]=e,t[6]=d,t[7]=r):r=t[7];let i;t[8]===a?i=t[9]:(i=a!=null&&W(ao,{action:a}),t[8]=a,t[9]=i);let o;return t[10]!==l||t[11]!==r||t[12]!==i?(o=G(K,{direction:`column`,gap:l,alignItems:`center`,children:[r,i]}),t[10]=l,t[11]=r,t[12]=i,t[13]=o):o=t[13],o}let f=n!=null&&n,p;t[14]===a?p=t[15]:(p=a!=null&&W(ao,{action:a}),t[14]=a,t[15]=p);let m;t[16]!==c||t[17]!==p||t[18]!==d?(m=G(K,{direction:`column`,gap:c,alignItems:`center`,children:[d,p]}),t[16]=c,t[17]=p,t[18]=d,t[19]=m):m=t[19];let h;return t[20]!==f||t[21]!==m?(h=G(K,{direction:`column`,gap:`size-300`,alignItems:`center`,justifyContent:`center`,children:[f,m]}),t[20]=f,t[21]=m,t[22]=h):h=t[22],h}var lo=q`
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
`,uo=q`
  flex: 0 1 var(--global-dimension-size-2000);
  min-height: var(--global-dimension-size-750);
`;function fo(e){let t=(0,Z.c)(3),{children:n}=e,r;t[0]===Symbol.for(`react.memo_cache_sentinel`)?(r=W(`div`,{css:uo,"aria-hidden":`true`}),t[0]=r):r=t[0];let i;return t[1]===n?i=t[2]:(i=G(`div`,{css:lo,children:[r,n]}),t[1]=n,t[2]=i),i}var po={size:`small`,icon:W(H,{svg:W(bt,{})})},mo={genericAdd:{size:`small`,icon:W(H,{svg:W(_t,{})})},genericEdit:{size:`small`,icon:W(H,{svg:W(st,{})})},trace:{size:`large`,icon:W(H,{svg:W(cn,{})})},dataset:{size:`large`,icon:W(H,{svg:W(rn,{})})},evaluator:{size:`large`,icon:W(H,{svg:W(Dt,{})})},session:{size:`large`,icon:W(H,{svg:W(Vt,{})})},experiment:{size:`large`,icon:W(H,{svg:W(In,{})})},prompt:{size:`large`,icon:W(H,{svg:W(Ut,{})})},project:{size:`large`,icon:W(H,{svg:W(mt,{})})},annotation:{size:`small`,icon:W(H,{svg:W(Bt,{})})},customAIProvider:{size:`small`,icon:W(H,{svg:W(Ve,{})})},event:{size:`small`,icon:W(H,{svg:W(rt,{})})},attribute:{size:`small`,icon:W(H,{svg:W(zt,{})})},config:{size:`small`,icon:W(H,{svg:W(ft,{})})},credential:{size:`small`,icon:W(H,{svg:W(Sn,{})})},version:{size:`small`,icon:W(H,{svg:W(ut,{})})},tag:po,label:po,split:po};Object.keys(mo),Object.fromEntries(Object.entries(mo).map(([e,t])=>[e,t.size]));var ho=q`
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
`,go=(e,t)=>{let n=`linear-gradient(
    to bottom,
    transparent 0,
    #000 ${e},
    #000 calc(100% - ${t}),
    transparent 100%
  )`;return q`
    -webkit-mask-image: ${n};
    mask-image: ${n};
  `},_o=q`
  display: block;
  margin-bottom: calc(-1 * var(--global-dimension-size-200));
`,vo=e=>q`
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
`;function yo(e){let t=(0,Z.c)(14),{id:n,x:r,y:i,width:a,height:o}=e,s,c,l,u,d,f,p,m;t[0]===Symbol.for(`react.memo_cache_sentinel`)?(s=W(`feFlood`,{floodOpacity:`0`,result:`BackgroundImageFix`}),c=W(`feColorMatrix`,{in:`SourceAlpha`,type:`matrix`,values:`0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 127 0`,result:`hardAlpha`}),l=W(`feOffset`,{dy:`4`}),u=W(`feGaussianBlur`,{stdDeviation:`6`}),d=W(`feComposite`,{in2:`hardAlpha`,operator:`out`}),f=W(`feColorMatrix`,{type:`matrix`,values:`0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0.19 0`}),p=W(`feBlend`,{mode:`normal`,in2:`BackgroundImageFix`,result:`effect1_dropShadow`}),m=W(`feBlend`,{mode:`normal`,in:`SourceGraphic`,in2:`effect1_dropShadow`,result:`shape`}),t[0]=s,t[1]=c,t[2]=l,t[3]=u,t[4]=d,t[5]=f,t[6]=p,t[7]=m):(s=t[0],c=t[1],l=t[2],u=t[3],d=t[4],f=t[5],p=t[6],m=t[7]);let h;return t[8]!==o||t[9]!==n||t[10]!==a||t[11]!==r||t[12]!==i?(h=G(`filter`,{id:n,x:r,y:i,width:a,height:o,filterUnits:`userSpaceOnUse`,colorInterpolationFilters:`sRGB`,children:[s,c,l,u,d,f,p,m]}),t[8]=o,t[9]=n,t[10]=a,t[11]=r,t[12]=i,t[13]=h):h=t[13],h}function bo(e){let t=(0,Z.c)(10),{x:n,y:r,size:i,icon:a}=e,o;t[0]===i?o=t[1]:(o=vo(i),t[0]=i,t[1]=o);let s;t[2]!==a||t[3]!==o?(s=W(`div`,{css:o,children:a}),t[2]=a,t[3]=o,t[4]=s):s=t[4];let c;return t[5]!==i||t[6]!==s||t[7]!==n||t[8]!==r?(c=W(`foreignObject`,{x:n,y:r,width:i,height:i,children:s}),t[5]=i,t[6]=s,t[7]=n,t[8]=r,t[9]=c):c=t[9],c}function xo(e){let t=(0,Z.c)(35),{icon:n,ids:r}=e,i;t[0]===Symbol.for(`react.memo_cache_sentinel`)?(i=[ho,go(`34%`,`34%`),_o],t[0]=i):i=t[0];let a=`url(#${r.f0})`,o,s,c;t[1]===Symbol.for(`react.memo_cache_sentinel`)?(o=W(`rect`,{x:`19`,y:`10`,width:`160`,height:`32`,rx:`8`,fill:`var(--esg-card-bg)`,shapeRendering:`crispEdges`}),s=W(`rect`,{x:`19.5`,y:`10.5`,width:`159`,height:`31`,rx:`7.5`,stroke:`var(--esg-stroke)`,shapeRendering:`crispEdges`}),c=W(`rect`,{opacity:`0.68`,x:`31`,y:`22`,width:`136`,height:`8`,rx:`3`,fill:`var(--esg-bar)`}),t[1]=o,t[2]=s,t[3]=c):(o=t[1],s=t[2],c=t[3]);let l;t[4]===a?l=t[5]:(l=G(`g`,{filter:a,children:[o,s,c]}),t[4]=a,t[5]=l);let u=`url(#${r.f1})`,d,f;t[6]===Symbol.for(`react.memo_cache_sentinel`)?(d=W(`rect`,{x:`12`,y:`52`,width:`174`,height:`48`,rx:`8`,fill:`var(--esg-card-bg)`,shapeRendering:`crispEdges`}),f=W(`rect`,{x:`12.5`,y:`52.5`,width:`173`,height:`47`,rx:`7.5`,stroke:`var(--esg-stroke-subtle)`,shapeRendering:`crispEdges`}),t[6]=d,t[7]=f):(d=t[6],f=t[7]);let p;t[8]===n?p=t[9]:(p=W(bo,{x:24,y:66,size:20,icon:n}),t[8]=n,t[9]=p);let m,h;t[10]===Symbol.for(`react.memo_cache_sentinel`)?(m=W(`rect`,{opacity:`0.68`,x:`56`,y:`65`,width:`120`,height:`8`,rx:`3`,fill:`var(--esg-bar)`}),h=W(`rect`,{opacity:`0.68`,x:`56`,y:`79`,width:`80`,height:`8`,rx:`3`,fill:`var(--esg-bar)`}),t[10]=m,t[11]=h):(m=t[10],h=t[11]);let g;t[12]!==p||t[13]!==u?(g=G(`g`,{filter:u,children:[d,f,p,m,h]}),t[12]=p,t[13]=u,t[14]=g):g=t[14];let _=`url(#${r.f2})`,v,y,b;t[15]===Symbol.for(`react.memo_cache_sentinel`)?(v=W(`rect`,{x:`19`,y:`110`,width:`160`,height:`32`,rx:`8`,fill:`var(--esg-card-bg)`,shapeRendering:`crispEdges`}),y=W(`rect`,{x:`19.5`,y:`110.5`,width:`159`,height:`31`,rx:`7.5`,stroke:`var(--esg-stroke)`,shapeRendering:`crispEdges`}),b=W(`rect`,{opacity:`0.68`,x:`31`,y:`122`,width:`136`,height:`8`,rx:`3`,fill:`var(--esg-bar)`}),t[15]=v,t[16]=y,t[17]=b):(v=t[15],y=t[16],b=t[17]);let x;t[18]===_?x=t[19]:(x=G(`g`,{filter:_,children:[v,y,b]}),t[18]=_,t[19]=x);let S;t[20]===r.f0?S=t[21]:(S=W(yo,{id:r.f0,x:7,y:2,width:184,height:56}),t[20]=r.f0,t[21]=S);let C;t[22]===r.f1?C=t[23]:(C=W(yo,{id:r.f1,x:0,y:44,width:198,height:72}),t[22]=r.f1,t[23]=C);let w;t[24]===r.f2?w=t[25]:(w=W(yo,{id:r.f2,x:7,y:102,width:184,height:56}),t[24]=r.f2,t[25]=w);let T;t[26]!==S||t[27]!==C||t[28]!==w?(T=G(`defs`,{children:[S,C,w]}),t[26]=S,t[27]=C,t[28]=w,t[29]=T):T=t[29];let E;return t[30]!==g||t[31]!==x||t[32]!==T||t[33]!==l?(E=G(`svg`,{width:`198`,height:`158`,viewBox:`0 0 198 158`,fill:`none`,xmlns:`http://www.w3.org/2000/svg`,"aria-hidden":`true`,focusable:`false`,css:i,children:[l,g,x,T]}),t[30]=g,t[31]=x,t[32]=T,t[33]=l,t[34]=E):E=t[34],E}function So(e){let t=(0,Z.c)(40),{icon:n,ids:r}=e,i;t[0]===Symbol.for(`react.memo_cache_sentinel`)?(i=[ho,go(`38%`,`31%`),_o],t[0]=i):i=t[0];let a=`url(#${r.f0})`,o,s,c,l,u,d;t[1]===Symbol.for(`react.memo_cache_sentinel`)?(o=W(`rect`,{x:`12`,y:`8`,width:`174`,height:`32`,rx:`8`,fill:`var(--esg-card-bg)`,shapeRendering:`crispEdges`}),s=W(`rect`,{x:`12.5`,y:`8.5`,width:`173`,height:`31`,rx:`7.5`,stroke:`var(--esg-stroke)`,shapeRendering:`crispEdges`}),c=W(`path`,{d:`M27.75 22.5C28.5784 22.5 29.25 23.1716 29.25 24C29.25 24.8284 28.5784 25.5 27.75 25.5C26.9216 25.5 26.25 24.8284 26.25 24C26.25 23.1716 26.9216 22.5 27.75 22.5Z`,fill:`var(--esg-dots)`}),l=W(`path`,{d:`M33 22.5C33.8284 22.5 34.5 23.1716 34.5 24C34.5 24.8284 33.8284 25.5 33 25.5C32.1716 25.5 31.5 24.8284 31.5 24C31.5 23.1716 32.1716 22.5 33 22.5Z`,fill:`var(--esg-dots)`}),u=W(`path`,{d:`M38.25 22.5C39.0784 22.5 39.75 23.1716 39.75 24C39.75 24.8284 39.0784 25.5 38.25 25.5C37.4216 25.5 36.75 24.8284 36.75 24C36.75 23.1716 37.4216 22.5 38.25 22.5Z`,fill:`var(--esg-dots)`}),d=W(`rect`,{opacity:`0.68`,x:`54`,y:`20`,width:`120`,height:`8`,rx:`3`,fill:`var(--esg-bar)`}),t[1]=o,t[2]=s,t[3]=c,t[4]=l,t[5]=u,t[6]=d):(o=t[1],s=t[2],c=t[3],l=t[4],u=t[5],d=t[6]);let f;t[7]===a?f=t[8]:(f=G(`g`,{filter:a,children:[o,s,c,l,u,d]}),t[7]=a,t[8]=f);let p=`url(#${r.f1})`,m,h;t[9]===Symbol.for(`react.memo_cache_sentinel`)?(m=W(`rect`,{x:`12`,y:`50`,width:`174`,height:`32`,rx:`8`,fill:`var(--esg-card-bg)`,shapeRendering:`crispEdges`}),h=W(`rect`,{x:`12.5`,y:`50.5`,width:`173`,height:`31`,rx:`7.5`,stroke:`var(--esg-stroke-subtle)`,shapeRendering:`crispEdges`}),t[9]=m,t[10]=h):(m=t[9],h=t[10]);let g;t[11]===n?g=t[12]:(g=W(bo,{x:25,y:58,size:16,icon:n}),t[11]=n,t[12]=g);let _;t[13]===Symbol.for(`react.memo_cache_sentinel`)?(_=W(`rect`,{opacity:`0.68`,x:`54`,y:`62`,width:`120`,height:`8`,rx:`3`,fill:`var(--esg-bar)`}),t[13]=_):_=t[13];let v;t[14]!==p||t[15]!==g?(v=G(`g`,{filter:p,children:[m,h,g,_]}),t[14]=p,t[15]=g,t[16]=v):v=t[16];let y=`url(#${r.f2})`,b,x,S,C,w,T;t[17]===Symbol.for(`react.memo_cache_sentinel`)?(b=W(`rect`,{x:`12`,y:`92`,width:`174`,height:`32`,rx:`8`,fill:`var(--esg-card-bg)`,shapeRendering:`crispEdges`}),x=W(`rect`,{x:`12.5`,y:`92.5`,width:`173`,height:`31`,rx:`7.5`,stroke:`var(--esg-stroke)`,shapeRendering:`crispEdges`}),S=W(`path`,{d:`M27.75 106.5C28.5784 106.5 29.25 107.172 29.25 108C29.25 108.828 28.5784 109.5 27.75 109.5C26.9216 109.5 26.25 108.828 26.25 108C26.25 107.172 26.9216 106.5 27.75 106.5Z`,fill:`var(--esg-dots)`}),C=W(`path`,{d:`M33 106.5C33.8284 106.5 34.5 107.172 34.5 108C34.5 108.828 33.8284 109.5 33 109.5C32.1716 109.5 31.5 108.828 31.5 108C31.5 107.172 32.1716 106.5 33 106.5Z`,fill:`var(--esg-dots)`}),w=W(`path`,{d:`M38.25 106.5C39.0784 106.5 39.75 107.172 39.75 108C39.75 108.828 39.0784 109.5 38.25 109.5C37.4216 109.5 36.75 108.828 36.75 108C36.75 107.172 37.4216 106.5 38.25 106.5Z`,fill:`var(--esg-dots)`}),T=W(`rect`,{opacity:`0.68`,x:`54`,y:`104`,width:`120`,height:`8`,rx:`3`,fill:`var(--esg-bar)`}),t[17]=b,t[18]=x,t[19]=S,t[20]=C,t[21]=w,t[22]=T):(b=t[17],x=t[18],S=t[19],C=t[20],w=t[21],T=t[22]);let E;t[23]===y?E=t[24]:(E=G(`g`,{filter:y,children:[b,x,S,C,w,T]}),t[23]=y,t[24]=E);let D;t[25]===r.f0?D=t[26]:(D=W(yo,{id:r.f0,x:0,y:0,width:198,height:56}),t[25]=r.f0,t[26]=D);let O;t[27]===r.f1?O=t[28]:(O=W(yo,{id:r.f1,x:0,y:42,width:198,height:56}),t[27]=r.f1,t[28]=O);let k;t[29]===r.f2?k=t[30]:(k=W(yo,{id:r.f2,x:0,y:84,width:198,height:56}),t[29]=r.f2,t[30]=k);let A;t[31]!==D||t[32]!==O||t[33]!==k?(A=G(`defs`,{children:[D,O,k]}),t[31]=D,t[32]=O,t[33]=k,t[34]=A):A=t[34];let j;return t[35]!==v||t[36]!==E||t[37]!==A||t[38]!==f?(j=G(`svg`,{width:`198`,height:`140`,viewBox:`0 0 198 140`,fill:`none`,xmlns:`http://www.w3.org/2000/svg`,"aria-hidden":`true`,focusable:`false`,css:i,children:[f,v,E,A]}),t[35]=v,t[36]=E,t[37]=A,t[38]=f,t[39]=j):j=t[39],j}function Co(e){let t=(0,Z.c)(8),{variant:n}=e,{size:r,icon:i}=mo[n===void 0?`genericAdd`:n],a=(0,X.useId)(),o=`${a}-f0`,s=`${a}-f1`,c=`${a}-f2`,l;t[0]!==o||t[1]!==s||t[2]!==c?(l={f0:o,f1:s,f2:c},t[0]=o,t[1]=s,t[2]=c,t[3]=l):l=t[3];let u=l,d;return t[4]!==i||t[5]!==u||t[6]!==r?(d=W(r===`small`?So:xo,{icon:i,ids:u}),t[4]=i,t[5]=u,t[6]=r,t[7]=d):d=t[7],d}function wo(e){let t=(0,Z.c)(2),{children:n}=e;if(typeof n==`string`){let e;return t[0]===n?e=t[1]:(e=W(Qe,{level:1,children:n}),t[0]=n,t[1]=e),e}return n}function To(e){let t=(0,Z.c)(2),{children:n}=e;if(!n)return null;if(typeof n==`string`){let e;return t[0]===n?e=t[1]:(e=W(V,{size:`S`,color:`text-700`,children:n}),t[0]=n,t[1]=e),e}return n}function Eo(e){let t=(0,Z.c)(10),{title:n,subTitle:r,extra:i}=e,a;t[0]===n?a=t[1]:(a=W(wo,{children:n}),t[0]=n,t[1]=a);let o;t[2]===r?o=t[3]:(o=W(To,{children:r}),t[2]=r,t[3]=o);let s;t[4]!==a||t[5]!==o?(s=G(K,{direction:`column`,gap:`size-50`,minWidth:0,children:[a,o]}),t[4]=a,t[5]=o,t[6]=s):s=t[6];let c;return t[7]!==i||t[8]!==s?(c=W(Fi,{padding:`size-200`,flex:`none`,"data-testid":`page-header`,children:G(K,{direction:`row`,justifyContent:`space-between`,alignItems:`center`,"data-testid":`page-header-content`,gap:`size-100`,children:[s,i]})}),t[7]=i,t[8]=s,t[9]=c):c=t[9],c}var Do=q`
  border-radius: 16px;
  padding: var(--global-dimension-size-50) var(--global-dimension-size-200) !important;
`,Oo=e=>{let t=(0,Z.c)(10),{onLoadMore:n,isLoadingNext:r,buttonProps:i}=e,a;t[0]===n?a=t[1]:(a=()=>{n()},t[0]=n,t[1]=a);let o;t[2]===r?o=t[3]:(o=r?W(H,{svg:W(un,{})}):void 0,t[2]=r,t[3]=o);let s=r?`Loading...`:`Load More`,c;return t[4]!==i||t[5]!==r||t[6]!==a||t[7]!==o||t[8]!==s?(c=W(yt,{onPress:a,size:`S`,css:Do,isDisabled:r,leadingVisual:o,...i,children:s}),t[4]=i,t[5]=r,t[6]=a,t[7]=o,t[8]=s,t[9]=c):c=t[9],c};function ko(e,{filled:t}={filled:!0}){let n;switch(e){case`warning`:n=W(t?It:ct,{});break;case`info`:n=W(t?pn:zt,{});break;case`danger`:n=W(t?gn:dt,{});break;case`success`:n=W(t?Yt:Xt,{});break}return W(H,{svg:n})}var Ao=q`
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
`,jo=q`
  display: flex;
  flex-direction: row;
  align-items: flex-start;
  flex: 1 1 auto;
`,Mo=q`
  background-color: transparent;
  color: inherit;
  padding: 0;
  border: none;
  cursor: pointer;
  width: 20px;
  height: 20px;
  margin-left: var(--global-dimension-size-200);
`,No=e=>{let t=(0,Z.c)(35),n,r,i,a,o,s,c,l,u,d;t[0]===e?(n=t[1],r=t[2],i=t[3],a=t[4],o=t[5],s=t[6],c=t[7],l=t[8],u=t[9],d=t[10]):({variant:d,title:u,icon:i,children:n,showIcon:s,dismissable:c,onDismissClick:a,banner:l,extra:r,...o}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a,t[5]=o,t[6]=s,t[7]=c,t[8]=l,t[9]=u,t[10]=d);let f=s===void 0||s,p=c!==void 0&&c,m=l!==void 0&&l,{theme:h}=vr();if(!i&&f){let e;t[11]===d?e=t[12]:(e=ko(d),t[11]=d,t[12]=e),i=e}let g=!!u,_;t[13]===u?_=t[14]:(_=u?W(V,{elementType:`h5`,size:`M`,weight:`heavy`,color:`inherit`,children:u}):null,t[13]=u,t[14]=_);let v;t[15]===n?v=t[16]:(v=W(V,{color:`inherit`,size:`S`,children:n}),t[15]=n,t[16]=v);let y;t[17]!==_||t[18]!==v?(y=G(`div`,{children:[_,v]}),t[17]=_,t[18]=v,t[19]=y):y=t[19];let b;t[20]!==i||t[21]!==y?(b=G(`div`,{css:jo,className:`alert__icon-title-wrap`,children:[i,y]}),t[20]=i,t[21]=y,t[22]=b):b=t[22];let x;t[23]!==p||t[24]!==a?(x=p?W(`button`,{css:Mo,onClick:a,children:W(H,{svg:W(Xe,{})})}):null,t[23]=p,t[24]=a,t[25]=x):x=t[25];let S;return t[26]!==m||t[27]!==r||t[28]!==o||t[29]!==g||t[30]!==b||t[31]!==x||t[32]!==h||t[33]!==d?(S=G(`div`,{...o,css:Ao,"data-variant":d,"data-banner":m,"data-has-title":g,"data-theme":h,children:[b,r,x]}),t[26]=m,t[27]=r,t[28]=o,t[29]=g,t[30]=b,t[31]=x,t[32]=h,t[33]=d,t[34]=S):S=t[34],S},Po=q`
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
`,Fo=e=>{let t=(0,Z.c)(17),n,r,i,a,o,s;t[0]===e?(n=t[1],r=t[2],i=t[3],a=t[4],o=t[5],s=t[6]):({children:n,variant:a,size:o,overflowMode:s,css:i,...r}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a,t[5]=o,t[6]=s);let c=a===void 0?`default`:a,l=o===void 0?`S`:o,u=s===void 0?`wrap`:s,{theme:d}=vr(),f;t[7]===i?f=t[8]:(f=q(Po,i),t[7]=i,t[8]=f);let p;return t[9]!==n||t[10]!==r||t[11]!==u||t[12]!==l||t[13]!==f||t[14]!==d||t[15]!==c?(p=W(`span`,{...r,css:f,"data-variant":c,"data-size":l,"data-overflow-mode":u,"data-theme":d,className:`badge`,children:n}),t[9]=n,t[10]=r,t[11]=u,t[12]=l,t[13]=f,t[14]=d,t[15]=c,t[16]=p):p=t[16],p},Io=q`
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
`,Lo=q`
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
`,Ro=e=>{let t=(0,Z.c)(14),n,r,i,a;t[0]===e?(n=t[1],r=t[2],i=t[3],a=t[4]):({className:n,css:r,size:a,...i}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a);let o;t[5]===n?o=t[6]:(o=B(`disclosure-group`,n),t[5]=n,t[6]=o);let s;t[7]===r?s=t[8]:(s=q(Io,r),t[7]=r,t[8]=s);let c;return t[9]!==i||t[10]!==a||t[11]!==o||t[12]!==s?(c=W(S,{allowsMultipleExpanded:!0,className:o,css:s,"data-size":a,...i}),t[9]=i,t[10]=a,t[11]=o,t[12]=s,t[13]=c):c=t[13],c},zo=e=>{let t=(0,Z.c)(10),n,r,i;t[0]===e?(n=t[1],r=t[2],i=t[3]):({size:i,className:n,...r}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i);let a;t[4]===n?a=t[5]:(a=B(`disclosure`,n),t[4]=n,t[5]=a);let o;return t[6]!==r||t[7]!==i||t[8]!==a?(o=W(Ne,{className:a,css:Lo,"data-size":i,defaultExpanded:!0,...r}),t[6]=r,t[7]=i,t[8]=a,t[9]=o):o=t[9],o},Bo=e=>{let t=(0,Z.c)(8),n,r;t[0]===e?(n=t[1],r=t[2]):({className:n,...r}=e,t[0]=e,t[1]=n,t[2]=r);let i;t[3]===n?i=t[4]:(i=B(`disclosure__panel`,n),t[3]=n,t[4]=i);let o;return t[5]!==r||t[6]!==i?(o=W(a,{className:i,...r}),t[5]=r,t[6]=i,t[7]=o):o=t[7],o},Vo=e=>{let t=(0,Z.c)(15),{children:n,arrowPosition:r,justifyContent:i,alignItems:a,direction:o,width:s}=e,c=a===void 0?`center`:a,l=o===void 0?`row`:o,u;t[0]===s?u=t[1]:(u={width:s},t[0]=s,t[1]=u);let d=l===`row`?`size-100`:`size-50`,f;t[2]!==c||t[3]!==n||t[4]!==l||t[5]!==i||t[6]!==d?(f=W(K,{justifyContent:i,direction:l,alignItems:c,width:`100%`,gap:d,children:n}),t[2]=c,t[3]=n,t[4]=l,t[5]=i,t[6]=d,t[7]=f):f=t[7];let p;t[8]===r?p=t[9]:(p=r===`none`?null:W(H,{svg:W(Pn,{})}),t[8]=r,t[9]=p);let m;return t[10]!==r||t[11]!==u||t[12]!==f||t[13]!==p?(m=W(Ge,{className:`react-aria-Heading disclosure__trigger`,children:G(Et,{slot:`trigger`,"data-arrow-position":r,style:u,children:[f,p]})}),t[10]=r,t[11]=u,t[12]=f,t[13]=p,t[14]=m):m=t[14],m},Ho=q`
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
`,Uo=q`
  width: var(--trigger-width);
  background-color: var(--field-popover-background-color);
  border-radius: var(--global-rounding-small);
  color: var(--field-text-color);
  box-shadow: 0px 4px 10px var(--field-popover-shadow-color);
  border: 1px solid var(--field-popover-border-color);
  max-height: inherit;
`,Wo=q`
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

  [slot="description"],
  [slot="errorMessage"],
  .react-aria-FieldError {
    grid-area: help;
  }
`,Go=q`
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
`,Ko=q(Uo,q`
    .react-aria-ListBox {
      display: block;
      width: unset;
      max-height: inherit;
      min-height: unset;
      border: none;
      overflow: auto;
    }
  `),qo=q`
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
`,Jo=e=>{e.stopPropagation()};function Yo(e){let t=(0,Z.c)(46),r,i,a,s,c,l,u,d,f,p,m,h;t[0]===e?(r=t[1],i=t[2],a=t[3],s=t[4],c=t[5],l=t[6],u=t[7],d=t[8],f=t[9],p=t[10],m=t[11],h=t[12]):({label:c,placeholder:l,description:i,errorMessage:a,children:r,size:p,width:h,stopPropagation:f,renderEmptyState:d,isInvalid:s,menuTrigger:m,...u}=e,t[0]=e,t[1]=r,t[2]=i,t[3]=a,t[4]=s,t[5]=c,t[6]=l,t[7]=u,t[8]=d,t[9]=f,t[10]=p,t[11]=m,t[12]=h);let g=p===void 0?`M`:p,_=m===void 0?`focus`:m,v;t[13]===Symbol.for(`react.memo_cache_sentinel`)?(v=q(Ho,Go),t[13]=v):v=t[13];let y=s||!!a,b;t[14]===h?b=t[15]:(b={width:h},t[14]=h,t[15]=b);let x=!!d,S;t[16]===c?S=t[17]:(S=c&&W(Cn,{children:c}),t[16]=c,t[17]=S);let C=f?Jo:void 0,w=f?Jo:void 0,T=f?Jo:void 0,D;t[18]===l?D=t[19]:(D=W(E,{placeholder:l}),t[18]=l,t[19]=D);let O;t[20]===Symbol.for(`react.memo_cache_sentinel`)?(O=W(Et,{children:W(it,{})}),t[20]=O):O=t[20];let k;t[21]!==T||t[22]!==D||t[23]!==C||t[24]!==w?(k=G(`div`,{className:`combobox__container`,onClick:C,onKeyDown:w,onKeyUp:T,children:[D,O]}),t[21]=T,t[22]=D,t[23]=C,t[24]=w,t[25]=k):k=t[25];let A;t[26]!==i||t[27]!==a?(A=i&&!a?W(St,{slot:`description`,children:i}):null,t[26]=i,t[27]=a,t[28]=A):A=t[28];let j;t[29]===a?j=t[30]:(j=W(xe,{children:a}),t[29]=a,t[30]=j);let M;t[31]!==r||t[32]!==d?(M=W(Lt,{css:Ko,children:W(o,{renderEmptyState:d,children:r})}),t[31]=r,t[32]=d,t[33]=M):M=t[33];let N;return t[34]!==_||t[35]!==u||t[36]!==g||t[37]!==k||t[38]!==A||t[39]!==j||t[40]!==M||t[41]!==y||t[42]!==b||t[43]!==x||t[44]!==S?(N=G(n,{...u,menuTrigger:_,css:v,"data-size":g,isInvalid:y,style:b,allowsEmptyCollection:x,children:[S,k,A,j,M]}),t[34]=_,t[35]=u,t[36]=g,t[37]=k,t[38]=A,t[39]=j,t[40]=M,t[41]=y,t[42]=b,t[43]=x,t[44]=S,t[45]=N):N=t[45],N}function Xo(e){let t=(0,Z.c)(8),n,r;t[0]===e?(n=t[1],r=t[2]):({children:n,...r}=e,t[0]=e,t[1]=n,t[2]=r);let i;t[3]===n?i=t[4]:(i=e=>{let{isSelected:t}=e;return G(U,{children:[n,t&&W(H,{svg:W(fn,{}),className:`menu-item__selected-checkmark`})]})},t[3]=n,t[4]=i);let a;return t[5]!==r||t[6]!==i?(a=W(d,{...r,css:qo,children:i}),t[5]=r,t[6]=i,t[7]=a):a=t[7],a}function Zo(e){let t=(0,Z.c)(11),n,r;t[0]===e?(n=t[1],r=t[2]):({ref:r,...n}=e,t[0]=e,t[1]=n,t[2]=r);let i,a;t[3]===n?(i=t[4],a=t[5]):({size:a,...i}=n,t[3]=n,t[4]=i,t[5]=a);let o=a===void 0?`M`:a,s;t[6]===Symbol.for(`react.memo_cache_sentinel`)?(s=q(Ho,Wo),t[6]=s):s=t[6];let c;return t[7]!==i||t[8]!==r||t[9]!==o?(c=W(le,{"data-size":o,className:`text-field`,ref:r,...i,css:s}),t[7]=i,t[8]=r,t[9]=o,t[10]=c):c=t[10],c}var Qo=()=>{let e=(0,Z.c)(1),t;return e[0]===Symbol.for(`react.memo_cache_sentinel`)?(t=W(H,{className:`search-field__icon`,svg:W(Pt,{})}),e[0]=t):t=e[0],t},$o=q`
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
`;function es(e){let t=(0,Z.c)(20),n,r;t[0]===e?(n=t[1],r=t[2]):({ref:r,...n}=e,t[0]=e,t[1]=n,t[2]=r);let i,a,o,s,c;t[3]===n?(i=t[4],a=t[5],o=t[6],s=t[7],c=t[8]):({size:s,variant:c,children:i,isReadOnly:a,...o}=n,t[3]=n,t[4]=i,t[5]=a,t[6]=o,t[7]=s,t[8]=c);let l=s===void 0?`M`:s,u=c===void 0?`default`:c,d;t[9]===Symbol.for(`react.memo_cache_sentinel`)?(d=q(Ho,Wo,$o),t[9]=d):d=t[9];let f;t[10]!==i||t[11]!==a?(f=e=>G(U,{children:[typeof i==`function`?i(e):i,!a&&W(Et,{slot:`clear`,className:`search-field__clear`,"data-empty":e.isEmpty||void 0,children:W(H,{svg:W(Xe,{})})})]}),t[10]=i,t[11]=a,t[12]=f):f=t[12];let p;return t[13]!==a||t[14]!==o||t[15]!==r||t[16]!==l||t[17]!==f||t[18]!==u?(p=W(he,{"data-size":l,"data-variant":u,className:`search-field`,ref:r,isReadOnly:a,...o,css:d,children:f}),t[13]=a,t[14]=o,t[15]=r,t[16]=l,t[17]=f,t[18]=u,t[19]=p):p=t[19],p}var ts=e(Pe());function ns(e){let t=(0,Z.c)(5),{onChange:n,debounceMs:r}=e,i;t[0]===n?i=t[1]:(i=e=>{(0,X.startTransition)(()=>{n(e)})},t[0]=n,t[1]=i);let a;return t[2]!==r||t[3]!==i?(a=(0,ts.default)(i,r),t[2]=r,t[3]=i,t[4]=a):a=t[4],a}var rs=q`
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
`;function is(e){let t=(0,Z.c)(38),n,r,i,a,o,s;t[0]===e?(n=t[1],r=t[2],i=t[3],a=t[4],o=t[5],s=t[6]):({onChange:i,debounceMs:o,placeholder:n,variant:s,onKeyDown:a,...r}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a,t[5]=o,t[6]=s);let c=o===void 0?200:o,l=s===void 0?`default`:s,u=(0,X.useRef)(null),d=(0,X.useRef)(null),f=(0,X.useRef)(null),[p,m]=(0,X.useState)(!1),h;t[7]===r.defaultValue?h=t[8]:(h=()=>!!r.defaultValue,t[7]=r.defaultValue,t[8]=h);let[g,_]=(0,X.useState)(h),v=!g&&!p,y;t[9]!==c||t[10]!==i?(y={onChange:i,debounceMs:c},t[9]=c,t[10]=i,t[11]=y):y=t[11];let b=ns(y),x;t[12]===b?x=t[13]:(x=e=>{_(e!==``),b(e)},t[12]=b,t[13]=x);let S=x,C;t[14]===Symbol.for(`react.memo_cache_sentinel`)?(C=e=>e!=null&&u.current?.contains(e)===!0,t[14]=C):C=t[14];let w=C,T;t[15]===Symbol.for(`react.memo_cache_sentinel`)?(T=e=>m(w(e.target)),t[15]=T):T=t[15];let D=T,O;t[16]===Symbol.for(`react.memo_cache_sentinel`)?(O=e=>{e.relatedTarget==null&&!document.hasFocus()||m(w(e.relatedTarget))},t[16]=O):O=t[16];let k=O,A;t[17]===a?A=t[18]:(A=e=>{e.key===`Escape`&&e.target instanceof HTMLInputElement&&e.target.value===``&&((0,Jn.flushSync)(()=>m(!1)),f.current?.focus(),e.preventDefault(),e.stopPropagation()),a?.(e)},t[17]=a,t[18]=A);let j=A,M;t[19]===Symbol.for(`react.memo_cache_sentinel`)?(M=W(Qo,{}),t[19]=M):M=t[19];let N;t[20]!==v||t[21]!==n?(N=W(E,{ref:d,placeholder:n,inert:v}),t[20]=v,t[21]=n,t[22]=N):N=t[22];let P;t[23]!==S||t[24]!==j||t[25]!==r||t[26]!==N?(P=G(es,{ref:u,size:`S`,onChange:S,onKeyDown:j,...r,children:[M,N]}),t[23]=S,t[24]=j,t[25]=r,t[26]=N,t[27]=P):P=t[27];let F=r[`aria-label`],I=!v,L;t[28]===Symbol.for(`react.memo_cache_sentinel`)?(L=()=>{(0,Jn.flushSync)(()=>m(!0)),d.current?.focus()},t[28]=L):L=t[28];let R;t[29]!==r.isDisabled||t[30]!==F||t[31]!==I?(R=W(Et,{ref:f,className:`search-button__trigger`,"aria-label":F,"aria-expanded":I,isDisabled:r.isDisabled,onPress:L}),t[29]=r.isDisabled,t[30]=F,t[31]=I,t[32]=R):R=t[32];let z;return t[33]!==v||t[34]!==P||t[35]!==R||t[36]!==l?(z=G(`div`,{className:`search-button`,"data-variant":l,"data-collapsed":v,css:rs,onFocus:D,onBlur:k,children:[P,R]}),t[33]=v,t[34]=P,t[35]=R,t[36]=l,t[37]=z):z=t[37],z}var as=q`
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
`;function os(e){let t=(0,Z.c)(2),n;return t[0]===e.children?n=t[1]:(n=W(`div`,{className:`composite-field`,css:as,children:e.children}),t[0]=e.children,t[1]=n),n}function ss(e){let t=(0,Z.c)(16),n,r;t[0]===e?(n=t[1],r=t[2]):({ref:r,...n}=e,t[0]=e,t[1]=n,t[2]=r);let i,a,o;t[3]===n?(i=t[4],a=t[5],o=t[6]):({size:o,children:i,...a}=n,t[3]=n,t[4]=i,t[5]=a,t[6]=o);let s=o===void 0?`M`:o,c;t[7]===Symbol.for(`react.memo_cache_sentinel`)?(c=q(Ho,Wo),t[7]=c):c=t[7];let l;t[8]!==i||t[9]!==a||t[10]!==r||t[11]!==s?(l=W(le,{"data-size":s,className:`copy-field`,isReadOnly:!0,ref:r,...a,css:c,children:i}),t[8]=i,t[9]=a,t[10]=r,t[11]=s,t[12]=l):l=t[12];let u;return t[13]!==s||t[14]!==l?(u=W(ht,{size:s,children:l}),t[13]=s,t[14]=l,t[15]=u):u=t[15],u}var cs=2e3;function ls(e){let t=(0,Z.c)(30),n,r;t[0]===e?(n=t[1],r=t[2]):({ref:r,...n}=e,t[0]=e,t[1]=n,t[2]=r);let i=xt(),a,o;t[3]===n?(a=t[4],o=t[5]):({disabled:a,...o}=n,t[3]=n,t[4]=a,t[5]=o);let[s,c]=(0,X.useState)(!1),l=(0,X.useRef)(null),u;t[6]===Symbol.for(`react.memo_cache_sentinel`)?(u=()=>{x(l.current?.value??``),c(!0),setTimeout(()=>{c(!1)},cs)},t[6]=u):u=t[6];let d=u,f;t[7]===Symbol.for(`react.memo_cache_sentinel`)?(f=q`
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
      `,t[7]=f):f=t[7];let p;t[8]===r?p=t[9]:(p=e=>{l.current=e,typeof r==`function`?r(e):r&&(r.current=e)},t[8]=r,t[9]=p);let m;t[10]!==a||t[11]!==o||t[12]!==p?(m=W(E,{...o,ref:p,type:`text`,readOnly:!0,disabled:a}),t[10]=a,t[11]=o,t[12]=p,t[13]=m):m=t[13];let h=s?`Copied`:`Copy to clipboard`,g=s?`success`:`inherit`,_=s?`Checkmark`:`Duplicate`,v;t[14]!==g||t[15]!==_?(v=W(H,{color:g,svgKey:_}),t[14]=g,t[15]=_,t[16]=v):v=t[16];let y;t[17]!==a||t[18]!==h||t[19]!==v?(y=W(Et,{className:`copy-input__copy-button`,onPress:d,isDisabled:a,"aria-label":h,children:v}),t[17]=a,t[18]=h,t[19]=v,t[20]=y):y=t[20];let b=s?`Copied`:`Copy`,S;t[21]===b?S=t[22]:(S=W(Ri,{offset:1,children:b}),t[21]=b,t[22]=S);let C;t[23]!==S||t[24]!==y?(C=G(A,{children:[y,S]}),t[23]=S,t[24]=y,t[25]=C):C=t[25];let w;return t[26]!==i||t[27]!==C||t[28]!==m?(w=G(`div`,{"data-size":i,"data-testid":`copy-input`,css:f,children:[m,C]}),t[26]=i,t[27]=C,t[28]=m,t[29]=w):w=t[29],w}var us=(0,X.createContext)(null);function ds(){let e=(0,X.useContext)(us);if(!e)throw Error(`useCredentialContext must be used within a CredentialContext.Provider`);return e}function fs(e){let t=(0,Z.c)(21),n,r;t[0]===e?(n=t[1],r=t[2]):({ref:r,...n}=e,t[0]=e,t[1]=n,t[2]=r);let i,a,o;t[3]===n?(i=t[4],a=t[5],o=t[6]):({size:o,children:i,...a}=n,t[3]=n,t[4]=i,t[5]=a,t[6]=o);let s=o===void 0?`M`:o,[c,l]=(0,X.useState)(!1),u;t[7]===c?u=t[8]:(u={isVisible:c,setIsVisible:l},t[7]=c,t[8]=u);let d;t[9]===Symbol.for(`react.memo_cache_sentinel`)?(d=q(Ho,Wo),t[9]=d):d=t[9];let f;t[10]!==i||t[11]!==a||t[12]!==r||t[13]!==s?(f=W(le,{"data-size":s,className:`credential-field`,autoComplete:`off`,ref:r,...a,css:d,children:i}),t[10]=i,t[11]=a,t[12]=r,t[13]=s,t[14]=f):f=t[14];let p;t[15]!==s||t[16]!==f?(p=W(ht,{size:s,children:f}),t[15]=s,t[16]=f,t[17]=p):p=t[17];let m;return t[18]!==u||t[19]!==p?(m=W(us.Provider,{value:u,children:p}),t[18]=u,t[19]=p,t[20]=m):m=t[20],m}function ps(e){let t=(0,Z.c)(28),n,r;t[0]===e?(n=t[1],r=t[2]):({ref:r,...n}=e,t[0]=e,t[1]=n,t[2]=r);let{isVisible:i,setIsVisible:a}=ds(),o=xt(),s,c,l;t[3]===n?(s=t[4],c=t[5],l=t[6]):({disabled:s,readOnly:l,...c}=n,t[3]=n,t[4]=s,t[5]=c,t[6]=l);let u;t[7]===Symbol.for(`react.memo_cache_sentinel`)?(u=q`
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
      `,t[7]=u):u=t[7];let d=i?`text`:`password`,f;t[8]!==s||t[9]!==c||t[10]!==l||t[11]!==r||t[12]!==d?(f=W(E,{...c,ref:r,type:d,disabled:s,readOnly:l}),t[8]=s,t[9]=c,t[10]=l,t[11]=r,t[12]=d,t[13]=f):f=t[13];let p;t[14]!==i||t[15]!==a?(p=()=>a(!i),t[14]=i,t[15]=a,t[16]=p):p=t[16];let m=s||l,h=i?`Hide credential`:`Show credential`,g;t[17]===i?g=t[18]:(g=W(H,{svg:W(i?Mt:at,{})}),t[17]=i,t[18]=g);let _;t[19]!==p||t[20]!==m||t[21]!==h||t[22]!==g?(_=W(Et,{className:`credential-input__toggle`,onPress:p,isDisabled:m,"aria-label":h,children:g}),t[19]=p,t[20]=m,t[21]=h,t[22]=g,t[23]=_):_=t[23];let v;return t[24]!==o||t[25]!==f||t[26]!==_?(v=G(`div`,{"data-size":o,"data-testid":`credential-input`,css:u,children:[f,_]}),t[24]=o,t[25]=f,t[26]=_,t[27]=v):v=t[27],v}var ms=``,hs=`${ms}REDACTED${ms}`;function gs(e){return typeof e==`string`&&e.startsWith(hs)}function _s(e){let t=e.slice(hs.length),n=t.indexOf(ms);return n<0?null:t.slice(0,n)||null}function vs(e){if(!gs(e))return null;let t=_s(e);return t?`••••${t}`:`••••••••`}function ys(e){let t=(0,Z.c)(29),{label:n,placeholder:r,description:i,value:a,onChange:o,onBlur:s,name:c,isDisabled:l,isRequired:u,errorMessage:d,size:f}=e,p=f===void 0?`M`:f,[m,h]=(0,X.useState)(!1),g;t[0]!==m||t[1]!==a?(g=!m&&gs(a),t[0]=m,t[1]=a,t[2]=g):g=t[2];let _=g,v=_?``:a??``,y;t[3]!==r||t[4]!==_||t[5]!==a?(y=_?vs(a)??`••••••••`:r,t[3]=r,t[4]=_,t[5]=a,t[6]=y):y=t[6];let b=y,x;t[7]!==m||t[8]!==o?(x=e=>{m||h(!0),o(e)},t[7]=m,t[8]=o,t[9]=x):x=t[9];let S=x,C=!!d,w;t[10]===n?w=t[11]:(w=W(Cn,{children:n}),t[10]=n,t[11]=w);let T;t[12]===b?T=t[13]:(T=W(E,{placeholder:b}),t[12]=b,t[13]=T);let D;t[14]!==i||t[15]!==d?(D=d?W(xe,{children:d}):i?W(V,{slot:`description`,children:i}):null,t[14]=i,t[15]=d,t[16]=D):D=t[16];let O;return t[17]!==v||t[18]!==S||t[19]!==l||t[20]!==u||t[21]!==c||t[22]!==s||t[23]!==p||t[24]!==C||t[25]!==w||t[26]!==T||t[27]!==D?(O=G(Zo,{type:`password`,size:p,name:c,value:v,onChange:S,onBlur:s,isDisabled:l,isRequired:u,isInvalid:C,autoComplete:`off`,children:[w,T,D]}),t[17]=v,t[18]=S,t[19]=l,t[20]=u,t[21]=c,t[22]=s,t[23]=p,t[24]=C,t[25]=w,t[26]=T,t[27]=D,t[28]=O):O=t[28],O}var bs=q`
  .react-aria-Input {
    text-align: right;
    font-feature-settings: "tnum" 1;
  }
`;function xs(e){let t=(0,Z.c)(13),n,r,i,a,o;if(t[0]!==e){let{ref:s,...c}=e;r=s;let{size:l,...u}=c,d=l===void 0?`M`:l;n=N,i=d,a=u,o=B(`text-field react-aria-NumberField`,c.className),t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a,t[5]=o}else n=t[1],r=t[2],i=t[3],a=t[4],o=t[5];let s;t[6]===Symbol.for(`react.memo_cache_sentinel`)?(s=q(Ho,Wo,bs),t[6]=s):s=t[6];let c;return t[7]!==n||t[8]!==r||t[9]!==i||t[10]!==a||t[11]!==o?(c=W(n,{"data-size":i,...a,className:o,ref:r,css:s}),t[7]=n,t[8]=r,t[9]=i,t[10]=a,t[11]=o,t[12]=c):c=t[12],c}function Ss(e){let t=(0,Z.c)(15),n,r,i,a;t[0]===e?(n=t[1],r=t[2],i=t[3],a=t[4]):({onChange:i,debounceMs:a,placeholder:n,...r}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a);let o=a===void 0?200:a,s;t[5]!==o||t[6]!==i?(s={onChange:i,debounceMs:o},t[5]=o,t[6]=i,t[7]=s):s=t[7];let c=ns(s),l;t[8]===Symbol.for(`react.memo_cache_sentinel`)?(l=W(Qo,{}),t[8]=l):l=t[8];let u;t[9]===n?u=t[10]:(u=W(E,{placeholder:n}),t[9]=n,t[10]=u);let d;return t[11]!==c||t[12]!==r||t[13]!==u?(d=G(es,{onChange:c,...r,children:[l,u]}),t[11]=c,t[12]=r,t[13]=u,t[14]=d):d=t[14],d}var Cs=()=>{let e=(0,Z.c)(1),t;return e[0]===Symbol.for(`react.memo_cache_sentinel`)?(t=W(H,{color:`danger`,className:`field__icon`,svg:W(Dn,{})}),e[0]=t):t=e[0],t},ws=()=>{let e=(0,Z.c)(1),t;return e[0]===Symbol.for(`react.memo_cache_sentinel`)?(t=W(H,{color:`success`,className:`field__icon`,svg:W(fn,{})}),e[0]=t):t=e[0],t},Ts=q`
  /* Pin the palette near the top of the viewport instead of centering it so
     the list can grow and shrink without the dialog jumping around */
  &&[data-variant="default"] .react-aria-Dialog {
    top: 15vh;
    transform: translate(-50%, 0);
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }
`,Es=q`
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
`;function Ds(e){let t=(0,Z.c)(32),{isOpen:n,onOpenChange:r,inputValue:i,onInputChange:a,filter:o,placeholder:s,"aria-label":c,onAction:l,children:u,renderEmptyState:d,footer:f,isPending:p}=e,m=s===void 0?`Search…`:s,h=c===void 0?`Command palette`:c,g=p?`true`:void 0,_;t[0]===Symbol.for(`react.memo_cache_sentinel`)?(_=W(Qo,{}),t[0]=_):_=t[0];let v;t[1]===m?v=t[2]:(v=W(E,{placeholder:m}),t[1]=m,t[2]=v);let y;t[3]!==h||t[4]!==v?(y=W(`div`,{className:`command-palette__field`,children:G(es,{"aria-label":h,variant:`quiet`,size:`L`,autoFocus:!0,children:[_,v]})}),t[3]=h,t[4]=v,t[5]=y):y=t[5];let b;t[6]===d?b=t[7]:(b=()=>W(`div`,{className:`command-palette__empty-state`,children:d?d():W(Za,{icon:W(H,{svg:W(Pt,{})}),description:`No results`})}),t[6]=d,t[7]=b);let x;t[8]!==h||t[9]!==u||t[10]!==l||t[11]!==b?(x=W(ma,{className:`command-palette__menu`,"aria-label":h,onAction:l,renderEmptyState:b,children:u}),t[8]=h,t[9]=u,t[10]=l,t[11]=b,t[12]=x):x=t[12];let S;t[13]===f?S=t[14]:(S=f??W(Os,{}),t[13]=f,t[14]=S);let C;t[15]===S?C=t[16]:(C=W(`div`,{className:`command-palette__footer`,children:S}),t[15]=S,t[16]=C);let w;t[17]!==o||t[18]!==i||t[19]!==a||t[20]!==C||t[21]!==y||t[22]!==x?(w=G(Ue,{inputValue:i,onInputChange:a,filter:o,children:[y,x,C]}),t[17]=o,t[18]=i,t[19]=a,t[20]=C,t[21]=y,t[22]=x,t[23]=w):w=t[23];let T;t[24]!==h||t[25]!==w||t[26]!==g?(T=W(mn,{size:`M`,css:Ts,children:W(Zt,{"aria-label":h,className:`command-palette`,css:Es,"data-pending":g,children:w})}),t[24]=h,t[25]=w,t[26]=g,t[27]=T):T=t[27];let D;return t[28]!==n||t[29]!==r||t[30]!==T?(D=W(ln,{isOpen:n,onOpenChange:r,isDismissable:!0,children:T}),t[28]=n,t[29]=r,t[30]=T,t[31]=D):D=t[31],D}function Os(){let e=(0,Z.c)(3),t;e[0]===Symbol.for(`react.memo_cache_sentinel`)?(t=G(`span`,{className:`command-palette__hint`,children:[W(Wa,{children:`↑↓`}),W(V,{size:`XS`,color:`text-500`,children:`to navigate`})]}),e[0]=t):t=e[0];let n;e[1]===Symbol.for(`react.memo_cache_sentinel`)?(n=G(`span`,{className:`command-palette__hint`,children:[W(Wa,{children:`↵`}),W(V,{size:`XS`,color:`text-500`,children:`to select`})]}),e[1]=n):n=e[1];let r;return e[2]===Symbol.for(`react.memo_cache_sentinel`)?(r=G(U,{children:[t,n,G(`span`,{className:`command-palette__hint`,children:[W(Wa,{children:`esc`}),W(V,{size:`XS`,color:`text-500`,children:`to close`})]})]}),e[2]=r):r=e[2],r}function ks(e){let t=(0,Z.c)(5),{title:n,children:r}=e,i;t[0]===n?i=t[1]:(i=W(on,{className:`command-palette__section-header`,children:n}),t[0]=n,t[1]=i);let a;return t[2]!==r||t[3]!==i?(a=G(yn,{className:`command-palette__section`,children:[i,r]}),t[2]=r,t[3]=i,t[4]=a):a=t[4],a}var As=q`
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
`;function js(e){let t=(0,Z.c)(18),n,r,i,a;t[0]===e?(n=t[1],r=t[2],i=t[3],a=t[4]):({icon:i,description:r,children:n,...a}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a);let o;t[5]===i?o=t[6]:(o=i&&W(`span`,{className:`command-palette-item__icon`,children:i}),t[5]=i,t[6]=o);let s;t[7]===n?s=t[8]:(s=W(`span`,{className:`command-palette-item__label`,children:n}),t[7]=n,t[8]=s);let c;t[9]===r?c=t[10]:(c=r&&W(`span`,{className:`command-palette-item__description`,children:r}),t[9]=r,t[10]=c);let l;t[11]!==o||t[12]!==s||t[13]!==c?(l=G(`div`,{className:`command-palette-item__layout`,children:[o,s,c]}),t[11]=o,t[12]=s,t[13]=c,t[14]=l):l=t[14];let u;return t[15]!==a||t[16]!==l?(u=W(ga,{...a,className:`command-palette-item`,css:As,children:l}),t[15]=a,t[16]=l,t[17]=u):u=t[17],u}var Ms=q`
  background-color: rgba(var(--global-color-blue-500-rgb), 0.4);
  color: inherit;
  border-radius: var(--global-rounding-xsmall);
`;function Ns(e){let t=(0,Z.c)(26),{text:n,match:r}=e,i;t[0]===r?i=t[1]:(i=r?.trim().length??0,t[0]=r,t[1]=i);let a=i;if(!r||a===0){let e;return t[2]===n?e=t[3]:(e=W(U,{children:n}),t[2]=n,t[3]=e),e}let o,s,c,l,u,d;if(t[4]!==r||t[5]!==a||t[6]!==n){d=Symbol.for(`react.early_return_sentinel`);bb0:{let e=n.toLowerCase().indexOf(r.trim().toLowerCase());if(e===-1){let e;t[13]===n?e=t[14]:(e=W(U,{children:n}),t[13]=n,t[14]=e),d=e;break bb0}o=e+a,u=n.slice(0,e),s=`match-text`,c=Ms,l=n.slice(e,o)}t[4]=r,t[5]=a,t[6]=n,t[7]=o,t[8]=s,t[9]=c,t[10]=l,t[11]=u,t[12]=d}else o=t[7],s=t[8],c=t[9],l=t[10],u=t[11],d=t[12];if(d!==Symbol.for(`react.early_return_sentinel`))return d;let f;t[15]!==s||t[16]!==c||t[17]!==l?(f=W(`mark`,{className:s,css:c,children:l}),t[15]=s,t[16]=c,t[17]=l,t[18]=f):f=t[18];let p;t[19]!==o||t[20]!==n?(p=n.slice(o),t[19]=o,t[20]=n,t[21]=p):p=t[21];let m;return t[22]!==u||t[23]!==f||t[24]!==p?(m=G(U,{children:[u,f,p]}),t[22]=u,t[23]=f,t[24]=p,t[25]=m):m=t[25],m}q`
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
`;var Ps=q(`
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
`),Fs=e=>{let t=(0,Z.c)(16),n,r,i,a,o;t[0]===e?(n=t[1],r=t[2],i=t[3],a=t[4],o=t[5]):({size:a,css:r,className:n,direction:o,...i}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a,t[5]=o);let s=o===void 0?`row`:o,c;t[6]===n?c=t[7]:(c=B(`radio-group`,n),t[6]=n,t[7]=c);let l;t[8]===r?l=t[9]:(l=q(Ho,Ps,r),t[8]=r,t[9]=l);let u;return t[10]!==s||t[11]!==i||t[12]!==a||t[13]!==c||t[14]!==l?(u=W(oe,{"data-size":a,"data-direction":s,className:c,css:l,...i}),t[10]=s,t[11]=i,t[12]=a,t[13]=c,t[14]=l,t[15]=u):u=t[15],u},Is=q(`
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
`),Ls=e=>{let t=(0,Z.c)(12),n,r,i;t[0]===e?(n=t[1],r=t[2],i=t[3]):({className:n,css:r,...i}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i);let a;t[4]===n?a=t[5]:(a=B(`radio`,n),t[4]=n,t[5]=a);let o;t[6]===r?o=t[7]:(o=q(Is,r),t[6]=r,t[7]=o);let s;return t[8]!==i||t[9]!==a||t[10]!==o?(s=W(ie,{className:a,css:o,...i}),t[8]=i,t[9]=a,t[10]=o,t[11]=s):s=t[11],s},Rs=q(et,`
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
`),zs=e=>{let t=(0,Z.c)(25),n,r,i;t[0]===e?(n=t[1],r=t[2],i=t[3]):({className:n,css:r,...i}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i);let a,o,s,c,l;t[4]===i?(a=t[5],o=t[6],s=t[7],c=t[8],l=t[9]):({leadingVisual:o,trailingVisual:l,size:s,children:a,...c}=i,t[4]=i,t[5]=a,t[6]=o,t[7]=s,t[8]=c,t[9]=l);let u=xt(),d=s??u,f;t[10]!==a||t[11]!==o||t[12]!==l?(f=e=>G(U,{children:[o,typeof a==`function`?a(e):a,l]}),t[10]=a,t[11]=o,t[12]=l,t[13]=f):f=t[13];let p=f,m;t[14]===r?m=t[15]:(m=q(Rs,r),t[14]=r,t[15]=m);let h=!a,g;t[16]===n?g=t[17]:(g=B(`toggle-button`,n),t[16]=n,t[17]=g);let _;return t[18]!==p||t[19]!==c||t[20]!==d||t[21]!==m||t[22]!==h||t[23]!==g?(_=W(M,{css:m,"data-size":d,"data-childless":h,className:g,...c,children:p}),t[18]=p,t[19]=c,t[20]=d,t[21]=m,t[22]=h,t[23]=g,t[24]=_):_=t[24],_},Bs=q(`
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
`),Vs=e=>{let t=(0,Z.c)(19),n,r,i,a,o;t[0]===e?(n=t[1],r=t[2],i=t[3],a=t[4],o=t[5]):({size:a,css:r,className:n,selectionMode:o,...i}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a,t[5]=o);let s=a===void 0?`M`:a,c=o===void 0?`single`:o,l;t[6]===n?l=t[7]:(l=B(`toggle-button-group`,n),t[6]=n,t[7]=l);let u;t[8]===r?u=t[9]:(u=q(Bs,r),t[8]=r,t[9]=u);let d;t[10]!==i||t[11]!==c||t[12]!==s||t[13]!==l||t[14]!==u?(d=W(v,{"data-size":s,className:l,css:u,selectionMode:c,...i}),t[10]=i,t[11]=c,t[12]=s,t[13]=l,t[14]=u,t[15]=d):d=t[15];let f;return t[16]!==s||t[17]!==d?(f=W(ht,{size:s,children:d}),t[16]=s,t[17]=d,t[18]=f):f=t[18],f},Hs=q`
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
`,Us=q`
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
`,Ws=q`
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
`,Gs=q`
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
`;function Ks(e){for(let t of X.Children.toArray(e)){if(!(0,X.isValidElement)(t))continue;if(t.type===X.Fragment){let e=Ks(t.props.children);if(e!=null)return e;continue}let{id:e,isDisabled:n}=t.props;if(e!=null&&!n)return e}}function qs(e){let t=(0,Z.c)(33),n,r,i,a,o,s,c,l,u;t[0]===e?(n=t[1],r=t[2],i=t[3],a=t[4],o=t[5],s=t[6],c=t[7],l=t[8],u=t[9]):({children:n,size:l,isJustified:u,selectedKey:c,defaultSelectedKey:a,onSelectionChange:o,className:r,css:i,...s}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a,t[5]=o,t[6]=s,t[7]=c,t[8]=l,t[9]=u);let d=l===void 0?`M`:l,f=u!==void 0&&u,p;t[10]!==n||t[11]!==a?(p=()=>a??Ks(n),t[10]=n,t[11]=a,t[12]=p):p=t[12];let[m]=(0,X.useState)(p),h;t[13]===c?h=t[14]:(h=c===void 0?void 0:[c],t[13]=c,t[14]=h);let g;t[15]===m?g=t[16]:(g=m==null?void 0:[m],t[15]=m,t[16]=g);let _;t[17]===o?_=t[18]:(_=e=>{let[t]=e;t!=null&&o?.(t)},t[17]=o,t[18]=_);let y;t[19]===r?y=t[20]:(y=B(`segmented-control`,r),t[19]=r,t[20]=y);let b;t[21]===i?b=t[22]:(b=q(Hs,i),t[21]=i,t[22]=b);let x;return t[23]!==n||t[24]!==f||t[25]!==s||t[26]!==d||t[27]!==h||t[28]!==g||t[29]!==_||t[30]!==y||t[31]!==b?(x=W(v,{...s,selectionMode:`single`,disallowEmptySelection:!0,orientation:`horizontal`,selectedKeys:h,defaultSelectedKeys:g,onSelectionChange:_,"data-size":d,"data-justified":f,className:y,css:b,children:n}),t[23]=n,t[24]=f,t[25]=s,t[26]=d,t[27]=h,t[28]=g,t[29]=_,t[30]=y,t[31]=b,t[32]=x):x=t[32],x}function Js(e){let t=(0,Z.c)(4),{isSelected:n}=e,r=(0,X.useRef)(null),i,a;t[0]===n?(i=t[1],a=t[2]):(i=()=>{let e=r.current,t=e?.style.translate;e&&n&&t&&(e.style.translate=`${t.split(` `)[0]} 0px`)},a=[n],t[0]=n,t[1]=i,t[2]=a),(0,X.useLayoutEffect)(i,a);let o;return t[3]===Symbol.for(`react.memo_cache_sentinel`)?(o=W($e,{ref:r,className:`segmented-control__thumb`,css:Gs}),t[3]=o):o=t[3],o}function Ys(e){let t=(0,Z.c)(16),n,r,i,a;t[0]===e?(n=t[1],r=t[2],i=t[3],a=t[4]):({children:n,className:r,css:i,...a}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a);let o;t[5]===r?o=t[6]:(o=B(`segmented-control__item`,r),t[5]=r,t[6]=o);let s;t[7]===i?s=t[8]:(s=q(Us,i),t[7]=i,t[8]=s);let c;t[9]===n?c=t[10]:(c=e=>{let{isSelected:t}=e;return G(U,{children:[W(`div`,{className:`segmented-control__item-content`,css:Ws,children:typeof n==`string`?W(V,{children:n}):n}),W(Js,{isSelected:t})]})},t[9]=n,t[10]=c);let l;return t[11]!==a||t[12]!==o||t[13]!==s||t[14]!==c?(l=W(M,{...a,className:o,css:s,children:c}),t[11]=a,t[12]=o,t[13]=s,t[14]=c,t[15]=l):l=t[15],l}var Xs=q`
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
`;function Zs(e){let t=(0,Z.c)(10),n,r,i;t[0]===e?(n=t[1],r=t[2],i=t[3]):({css:n,ref:r,...i}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i);let a;t[4]===n?a=t[5]:(a=q(Xs,n),t[4]=n,t[5]=a);let s=a,c;return t[6]!==s||t[7]!==r||t[8]!==i?(c=W(o,{css:s,ref:r,...i}),t[6]=s,t[7]=r,t[8]=i,t[9]=c):c=t[9],c}var Qs=q`
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
`;function $s(e){let t=(0,Z.c)(14),n,r;t[0]===e?(n=t[1],r=t[2]):({ref:r,...n}=e,t[0]=e,t[1]=n,t[2]=r);let i,a,o;t[3]===n?(i=t[4],a=t[5],o=t[6]):({children:i,isHovered:a,...o}=n,t[3]=n,t[4]=i,t[5]=a,t[6]=o);let c=a||void 0,l;t[7]===i?l=t[8]:(l=e=>{let{isIndeterminate:t}=e;return G(U,{children:[W(`div`,{className:`checkbox`,children:W(`svg`,{viewBox:`0 0 18 18`,"aria-hidden":`true`,children:t?W(`rect`,{x:1,y:7.5,width:15,height:3}):W(`polyline`,{points:`1 9 7 14 15 4`})})}),i]})},t[7]=i,t[8]=l);let u;return t[9]!==r||t[10]!==o||t[11]!==c||t[12]!==l?(u=W(s,{...o,ref:r,css:Qs,"data-force-hovered":c,children:l}),t[9]=r,t[10]=o,t[11]=c,t[12]=l,t[13]=u):u=t[13],u}var ec=q`
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
`,tc=q`
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
`,nc=q`
  padding: var(--global-dimension-size-50) var(--global-dimension-size-100) 0;
`;q`
  display: flex;
  flex-direction: column;
  gap: var(--global-menu-item-gap);
`;function rc(e){let t=(0,Z.c)(6),n,r;t[0]===e?(n=t[1],r=t[2]):({ref:n,...r}=e,t[0]=e,t[1]=n,t[2]=r);let i;return t[3]!==n||t[4]!==r?(i=W(Fe,{css:ec,ref:n,...r}),t[3]=n,t[4]=r,t[5]=i):i=t[5],i}function ic(e){let t=(0,Z.c)(14),n,r,i,a,o;t[0]===e?(n=t[1],r=t[2],i=t[3],a=t[4],o=t[5]):({ref:r,children:n,subtitle:a,trailingContent:o,...i}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a,t[5]=o);let s;t[6]!==n||t[7]!==a||t[8]!==o?(s=e=>{let{selectionMode:t,selectionBehavior:r}=e;return G(U,{children:[W(ac,{subtitle:a,selectionMode:t,selectionBehavior:r,children:n}),o]})},t[6]=n,t[7]=a,t[8]=o,t[9]=s):s=t[9];let c;return t[10]!==r||t[11]!==i||t[12]!==s?(c=W(I,{css:tc,ref:r,...i,children:s}),t[10]=r,t[11]=i,t[12]=s,t[13]=c):c=t[13],c}var ac=e=>{let t=(0,Z.c)(14),{children:n,subtitle:r,selectionMode:i,selectionBehavior:a}=e,[o,s]=(0,X.useState)(!1),c,l,u;t[0]===Symbol.for(`react.memo_cache_sentinel`)?(c=()=>s(!0),l=()=>s(!1),u=q`
        flex: 1;
        min-width: 0;
      `,t[0]=c,t[1]=l,t[2]=u):(c=t[0],l=t[1],u=t[2]);let d;t[3]!==o||t[4]!==a||t[5]!==i?(d=i===`multiple`&&a===`toggle`&&W($s,{slot:`selection`,isHovered:o}),t[3]=o,t[4]=a,t[5]=i,t[6]=d):d=t[6];let f;t[7]===Symbol.for(`react.memo_cache_sentinel`)?(f=q`
            padding: var(--global-menu-item-gap);
          `,t[7]=f):f=t[7];let p;t[8]!==n||t[9]!==r?(p=G(K,{direction:`column`,gap:`var(--global-dimension-size-25)`,minWidth:0,flex:1,css:f,children:[n,r]}),t[8]=n,t[9]=r,t[10]=p):p=t[10];let m;return t[11]!==d||t[12]!==p?(m=W(`div`,{onMouseEnter:c,onMouseLeave:l,css:u,children:G(K,{direction:`row`,alignItems:`center`,gap:`size-100`,className:`GridListItem__content`,children:[d,p]})}),t[11]=d,t[12]=p,t[13]=m):m=t[13],m},oc=e=>{let t=(0,Z.c)(2),{title:n}=e,r;return t[0]===n?r=t[1]:(r=W(je,{css:nc,children:W(V,{weight:`heavy`,children:n})}),t[0]=n,t[1]=r),r},sc=q`
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
`;function cc(e){let t=(0,Z.c)(3),{children:n}=e,r;t[0]===Symbol.for(`react.memo_cache_sentinel`)?(r=q`
        display: flex;
        align-items: center;
        justify-content: center;
        width: var(--global-dimension-size-200);
        height: var(--global-dimension-size-200);
        /* The visual keeps its box when the token's text truncates —
           otherwise it compresses and the visual slides into the end cap. */
        flex-shrink: 0;
        margin-right: var(--global-dimension-size-50);
      `,t[0]=r):r=t[0];let i;return t[1]===n?i=t[2]:(i=W(`span`,{css:r,children:n}),t[1]=n,t[2]=i),i}function lc(e){let t=(0,Z.c)(58),n,r,i,a,o,s,c,l,u,d,f,p;t[0]===e?(n=t[1],r=t[2],i=t[3],a=t[4],o=t[5],s=t[6],c=t[7],l=t[8],u=t[9],d=t[10],f=t[11],p=t[12]):({ref:l,children:n,isDisabled:i,css:r,color:f,onPress:s,onRemove:c,size:p,style:d,leadingVisual:a,maxWidth:o,...u}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a,t[5]=o,t[6]=s,t[7]=c,t[8]=l,t[9]=u,t[10]=d,t[11]=f,t[12]=p);let m=f===void 0?`var(--global-color-gray-600)`:f,h=p===void 0?`M`:p,{theme:g}=vr(),_;t[13]!==a||t[14]!==h?(_=a&&h!==`S`?W(cc,{children:a}):null,t[13]=a,t[14]=h,t[15]=_):_=t[15];let v=_,y;t[16]!==i||t[17]!==c?(y=c?W(`button`,{onClick:()=>{c()},disabled:i,"aria-label":`Remove`,children:W(H,{svg:W(Xe,{})})}):null,t[16]=i,t[17]=c,t[18]=y):y=t[18];let b=y,x;t[19]===n?x=t[20]:(x=W(`span`,{className:`token__text`,children:n}),t[19]=n,t[20]=x);let S=x,C;t[21]!==i||t[22]!==s||t[23]!==c||t[24]!==b||t[25]!==S||t[26]!==v?(C=()=>s&&c?G(U,{children:[G(`button`,{onClick:()=>{s()},disabled:i,children:[v,S]}),b]}):s?G(`button`,{onClick:()=>{s()},disabled:i,children:[v,S]}):c?G(U,{children:[G(`span`,{children:[v,S]}),b]}):G(U,{children:[v,S]}),t[21]=i,t[22]=s,t[23]=c,t[24]=b,t[25]=S,t[26]=v,t[27]=C):C=t[27];let w=C,T;t[28]===r?T=t[29]:(T=q(sc,r),t[28]=r,t[29]=T);let E;t[30]===o?E=t[31]:(E=o&&{"--token-max-width":o},t[30]=o,t[31]=E);let D;t[32]!==m||t[33]!==d||t[34]!==E?(D={"--internal-token-color":m,...E,...d},t[32]=m,t[33]=d,t[34]=E,t[35]=D):D=t[35];let O;t[36]===s?O=t[37]:(O=s&&{"data-interactive":!0},t[36]=s,t[37]=O);let k;t[38]===c?k=t[39]:(k=c&&{"data-removable":!0},t[38]=c,t[39]=k);let A;t[40]===v?A=t[41]:(A=v&&{"data-leading-visual":!0},t[40]=v,t[41]=A);let j;t[42]===i?j=t[43]:(j=i&&{"data-disabled":!0},t[42]=i,t[43]=j);let M;t[44]===w?M=t[45]:(M=w(),t[44]=w,t[45]=M);let N;return t[46]!==l||t[47]!==u||t[48]!==h||t[49]!==O||t[50]!==k||t[51]!==A||t[52]!==j||t[53]!==M||t[54]!==T||t[55]!==D||t[56]!==g?(N=W(`div`,{ref:l,css:T,style:D,"data-theme":g,"data-size":h,...O,...k,...A,...j,...u,children:M}),t[46]=l,t[47]=u,t[48]=h,t[49]=O,t[50]=k,t[51]=A,t[52]=j,t[53]=M,t[54]=T,t[55]=D,t[56]=g,t[57]=N):N=t[57],N}var uc=q`
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
`;function dc(e){let t=(0,Z.c)(24),n,i,a,o,s,c;t[0]===e?(n=t[1],i=t[2],a=t[3],o=t[4],s=t[5],c=t[6]):({ref:s,label:a,thumbLabels:c,children:i,css:n,...o}=e,t[0]=e,t[1]=n,t[2]=i,t[3]=a,t[4]=o,t[5]=s,t[6]=c);let u;t[7]===n?u=t[8]:(u=q(uc,n),t[7]=n,t[8]=u);let d;t[9]===a?d=t[10]:(d=a&&W(Cn,{className:`slider__label`,children:a}),t[9]=a,t[10]=d);let f;t[11]===i?f=t[12]:(f=i===void 0?W(mc,{}):i,t[11]=i,t[12]=f);let p;t[13]===f?p=t[14]:(p=W(l,{className:`slider__output`,children:f}),t[13]=f,t[14]=p);let m;t[15]===c?m=t[16]:(m=W(y,{className:`slider__track`,style:fc,children:e=>{let{state:t}=e;return W(U,{children:t.values.map((e,t)=>W(r,{index:t,"aria-label":c?.[t],className:`slider__thumb`},t))})}}),t[15]=c,t[16]=m);let h;return t[17]!==o||t[18]!==s||t[19]!==u||t[20]!==d||t[21]!==p||t[22]!==m?(h=G(w,{css:u,...o,ref:s,children:[d,p,m]}),t[17]=o,t[18]=s,t[19]=u,t[20]=d,t[21]=p,t[22]=m,t[23]=h):h=t[23],h}function fc(e){let{state:t}=e;return t.values.length===1?{"--slider-start":`0%`,"--slider-end":`${t.getThumbPercent(0)*100}%`}:{"--slider-start":`${t.getThumbPercent(0)*100}%`,"--slider-end":`${t.getThumbPercent(1)*100}%`}}function pc(e){let t=(0,Z.c)(19),n,r;t[0]===e?(n=t[1],r=t[2]):({onChange:n,...r}=e,t[0]=e,t[1]=n,t[2]=r);let{step:i,getThumbMinValue:a,getThumbMaxValue:o,values:s,setThumbValue:c}=(0,X.useContext)(Ie),l=`defaultValue`in r,u=s[0]===a(0),d=l&&u?r.defaultValue:s[0],f=Ye(Gt),p=f.id,m;t[3]!==n||t[4]!==c?(m=e=>{n?n(e):typeof e==`number`&&c(0,e)},t[3]=n,t[4]=c,t[5]=m):m=t[5];let h;t[6]===o?h=t[7]:(h=o(0),t[6]=o,t[7]=h);let g;t[8]===a?g=t[9]:(g=a(0),t[8]=a,t[9]=g);let _;t[10]===Symbol.for(`react.memo_cache_sentinel`)?(_=W(E,{}),t[10]=_):_=t[10];let v;return t[11]!==f.id||t[12]!==r||t[13]!==i||t[14]!==m||t[15]!==h||t[16]!==g||t[17]!==d?(v=W(xs,{className:`slider__number-field`,"aria-labelledby":p,value:d,onChange:m,step:i,maxValue:h,minValue:g,...r,children:_}),t[11]=f.id,t[12]=r,t[13]=i,t[14]=m,t[15]=h,t[16]=g,t[17]=d,t[18]=v):v=t[18],v}function mc(){let e=(0,Z.c)(4),t=(0,X.useContext)(Ie),n;e[0]===t.values?n=e[1]:(n=t.values.map(hc).join(` – `),e[0]=t.values,e[1]=n);let r;return e[2]===n?r=e[3]:(r=W(V,{children:n}),e[2]=n,e[3]=r),r}function hc(e){return e.toString()}var gc=q`
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
`;function _c(e){let t=(0,Z.c)(4),{children:n,variant:r}=e,i=r===void 0?`default`:r,{theme:a}=vr(),o;return t[0]!==n||t[1]!==a||t[2]!==i?(o=W(`span`,{css:gc,"data-variant":i,"data-theme":a,className:`counter`,children:n}),t[0]=n,t[1]=a,t[2]=i,t[3]=o):o=t[3],o}function vc(){let e=(0,Z.c)(6),t=(0,X.useRef)(null),[n,r]=(0,X.useState)(!1),[i,a]=(0,X.useState)(!1),o;e[0]===Symbol.for(`react.memo_cache_sentinel`)?(o=()=>{let e=t.current;if(!e)return;if(e.getAttribute(`data-orientation`)!==`horizontal`){r(!1),a(!1);return}let{scrollLeft:n,scrollWidth:i,clientWidth:o}=e,s=i-o;r(n>1),a(n<s-1)},e[0]=o):o=e[0];let s=o;At(t,`scroll`,s);let c;e[1]===Symbol.for(`react.memo_cache_sentinel`)?(c={ref:t,onResize:s},e[1]=c):c=e[1],Rt(c);let l;e[2]===Symbol.for(`react.memo_cache_sentinel`)?(l=()=>{s()},e[2]=l):l=e[2],(0,X.useEffect)(l);let u;return e[3]!==i||e[4]!==n?(u={ref:t,hasOverflowAtStart:n,hasOverflowAtEnd:i},e[3]=i,e[4]=n,e[5]=u):u=e[5],u}var yc=q`
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
`;function bc(e){let t=(0,Z.c)(16),n,r,i,a,o;t[0]===e?(n=t[1],r=t[2],i=t[3],a=t[4],o=t[5]):({children:r,css:n,className:i,orientation:o,...a}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a,t[5]=o);let s=o===void 0?`horizontal`:o,c;t[6]===n?c=t[7]:(c=q(yc,n),t[6]=n,t[7]=c);let l;t[8]===i?l=t[9]:(l=B(`react-aria-Tabs`,`tabs`,i),t[8]=i,t[9]=l);let u;return t[10]!==r||t[11]!==s||t[12]!==a||t[13]!==c||t[14]!==l?(u=W(pe,{css:c,className:l,orientation:s,...a,children:r}),t[10]=r,t[11]=s,t[12]=a,t[13]=c,t[14]=l,t[15]=u):u=t[15],u}var xc=q`
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
`,Sc=q`
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
`;function Cc(e){let t=(0,Z.c)(23),n,r,i,a,o;t[0]===e?(n=t[1],r=t[2],i=t[3],a=t[4],o=t[5]):({children:r,extra:a,css:n,className:i,...o}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a,t[5]=o);let{ref:s,hasOverflowAtStart:c,hasOverflowAtEnd:l}=vc(),u;t[6]===n?u=t[7]:(u=q(xc,n),t[6]=n,t[7]=u);let d;t[8]===i?d=t[9]:(d=B(`react-aria-TabList`,i),t[8]=i,t[9]=d);let f;t[10]!==r||t[11]!==l||t[12]!==c||t[13]!==o||t[14]!==s||t[15]!==u||t[16]!==d?(f=W(ke,{ref:s,css:u,className:d,"data-overflow-start":c,"data-overflow-end":l,...o,children:r}),t[10]=r,t[11]=l,t[12]=c,t[13]=o,t[14]=s,t[15]=u,t[16]=d,t[17]=f):f=t[17];let p=f;if(a==null)return p;let m;t[18]===a?m=t[19]:(m=W(`div`,{className:`tab-list-row__extra`,children:a}),t[18]=a,t[19]=m);let h;return t[20]!==m||t[21]!==p?(h=G(`div`,{className:`tab-list-row`,css:Sc,children:[p,m]}),t[20]=m,t[21]=p,t[22]=h):h=t[22],h}var wc=q`
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
`;function Tc(e){let t=(0,Z.c)(14),n,r,i,a;t[0]===e?(n=t[1],r=t[2],i=t[3],a=t[4]):({css:n,className:r,padded:i,...a}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a);let o;t[5]===n?o=t[6]:(o=q(wc,n),t[5]=n,t[6]=o);let s;t[7]===r?s=t[8]:(s=B(`react-aria-TabPanel`,r),t[7]=r,t[8]=s);let c;return t[9]!==i||t[10]!==a||t[11]!==o||t[12]!==s?(c=W(Te,{css:o,className:s,"data-padded":i,...a}),t[9]=i,t[10]=a,t[11]=o,t[12]=s,t[13]=c):c=t[13],c}function Ec(e){let t=(0,Z.c)(11),n,r,i;t[0]===e?(n=t[1],r=t[2],i=t[3]):({children:n,id:r,...i}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i);let a;t[4]!==n||t[5]!==r?(a=e=>{let{state:t}=e,{selectedKey:i}=t;return i===r?n:null},t[4]=n,t[5]=r,t[6]=a):a=t[6];let o;return t[7]!==r||t[8]!==i||t[9]!==a?(o=W(Tc,{id:r,...i,children:a}),t[7]=r,t[8]=i,t[9]=a,t[10]=o):o=t[10],o}var Dc=q`
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
`;function Oc(e){let t=(0,Z.c)(15),n,r,i,a;t[0]===e?(n=t[1],r=t[2],i=t[3],a=t[4]):({children:r,css:n,className:i,...a}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a);let o;t[5]===n?o=t[6]:(o=q(Dc,n),t[5]=n,t[6]=o);let s;t[7]===i?s=t[8]:(s=B(`react-aria-Tab`,i),t[7]=i,t[8]=s);let c;t[9]===Symbol.for(`react.memo_cache_sentinel`)?(c=W($e,{className:`react-aria-SelectionIndicator`}),t[9]=c):c=t[9];let l;return t[10]!==r||t[11]!==a||t[12]!==o||t[13]!==s?(l=G(L,{css:o,className:s,...a,children:[r,c]}),t[10]=r,t[11]=a,t[12]=o,t[13]=s,t[14]=l):l=t[14],l}var kc=e=>{let t=(0,Z.c)(9),{message:n,size:r,className:i}=e,a;t[0]===Symbol.for(`react.memo_cache_sentinel`)?(a=q`
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        width: 100%;
        height: 100%;
        gap: var(--global-dimension-size-100);
      `,t[0]=a):a=t[0];let o;t[1]===r?o=t[2]:(o=W(Mi,{isIndeterminate:!0,"aria-label":`loading`,size:r}),t[1]=r,t[2]=o);let s;t[3]===n?s=t[4]:(s=n==null?null:W(V,{children:n}),t[3]=n,t[4]=s);let c;return t[5]!==i||t[6]!==o||t[7]!==s?(c=G(`div`,{className:i,css:a,children:[o,s]}),t[5]=i,t[6]=o,t[7]=s,t[8]=c):c=t[8],c},Ac=Ke`
  0% {
    opacity: 1;
  }
  50% {
    opacity: 0.4;
  }
  100% {
    opacity: 1;
  }
`,jc=Ke`
  0% {
    transform: translateX(-100%);
  }
  50% {
    transform: translateX(100%);
  }
  100% {
    transform: translateX(100%);
  }
`,Mc=q`
  display: block;
  background-color: var(--global-color-gray-200);
`,Nc=q`
  animation: ${Ac} 2s ease-in-out 0.5s infinite;
`,Pc=q`
  position: relative;
  overflow: hidden;
  /* Fix bug in Safari https://bugs.webkit.org/show_bug.cgi?id=68196 */
  -webkit-mask-image: -webkit-radial-gradient(white, black);

  &::after {
    animation: ${jc} 2s linear 0.5s infinite;
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
`,Fc=e=>{if(typeof e==`number`)return`${e}px`;if(typeof e==`string`)switch(e){case`none`:return`0`;case`XS`:return`var(--global-rounding-xsmall)`;case`S`:return`var(--global-rounding-small)`;case`M`:return`var(--global-rounding-medium)`;case`L`:return`var(--global-rounding-large)`;case`circle`:return`50%`;default:return e}return`var(--global-rounding-medium)`};function Ic({ref:e,width:t=`100%`,height:n=`1.2em`,borderRadius:r=`S`,animation:i=`pulse`,className:a,...o}){let s=typeof t==`number`?`${t}px`:t,c=typeof n==`number`?`${n}px`:n,l=Fc(r);return W(`span`,{ref:e,className:B(a,`skeleton`),css:[Mc,i===`pulse`&&Nc,i===`wave`&&Pc,q`
          width: ${s};
          height: ${c};
          border-radius: ${l};
        `],...o})}Ic.displayName=`Skeleton`;var Lc=e=>{let t=(0,Z.c)(5),n,r,i;t[0]===Symbol.for(`react.memo_cache_sentinel`)?(n=W(Ic,{height:100,borderRadius:8,animation:`wave`}),r=W(Ic,{height:24,width:`80%`,animation:`wave`}),i=W(Ic,{height:16,width:`60%`,animation:`wave`}),t[0]=n,t[1]=r,t[2]=i):(n=t[0],r=t[1],i=t[2]);let a;return t[3]===e?a=t[4]:(a=G(K,{direction:`column`,gap:`size-100`,width:`100%`,...e,children:[n,r,i]}),t[3]=e,t[4]=a),a},Rc=q`
  display: flex;
  flex-direction: column;
`,zc=q`
  display: flex;
  gap: 6px;
`,Bc=[[3,2,5,1.5,4,2.5,4],[2,4,1.5,5,3,3.5],[4,2.5,5,2,3],[3,4.5,2,4,1.5,4],[3.5,2,5,2.5]],Vc=[`100%`,`95%`,`100%`,`88%`,`92%`];function Hc({lines:e=3,animation:t=`pulse`,gap:n=8}){let r=(e,t)=>{let n=Bc[e%Bc.length],r=t?Math.ceil(n.length*.5):n.length;return n.slice(0,r)};return W(`div`,{css:[Rc,q`
          gap: ${n}px;
        `],children:Array.from({length:e},(n,i)=>{let a=i===e-1,o=r(i,a);return W(`div`,{css:[zc,q`
                width: ${a?`55%`:Vc[i%Vc.length]};
              `],children:o.map((e,n)=>W(Ic,{css:q`
                  flex-grow: ${e};
                  min-width: 20px;
                `,height:`1em`,animation:t},n))},i)})})}var Uc=q`
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
`;function Wc(e){let t=(0,Z.c)(14),n,r;t[0]===e?(n=t[1],r=t[2]):({ref:r,...n}=e,t[0]=e,t[1]=n,t[2]=r);let i,a;t[3]===n?(i=t[4],a=t[5]):({size:a,...i}=n,t[3]=n,t[4]=i,t[5]=a);let o=a===void 0?`M`:a,s;t[6]===Symbol.for(`react.memo_cache_sentinel`)?(s=q(Ho,Uc),t[6]=s):s=t[6];let c;t[7]!==i||t[8]!==r||t[9]!==o?(c=W(ye,{"data-size":o,className:`select`,ref:r,css:s,...i}),t[7]=i,t[8]=r,t[9]=o,t[10]=c):c=t[10];let l;return t[11]!==o||t[12]!==c?(l=W(ht,{size:o,children:c}),t[11]=o,t[12]=c,t[13]=l):l=t[13],l}function Gc(e){let t=(0,Z.c)(10),n,r,i;t[0]===e?(n=t[1],r=t[2],i=t[3]):({ref:r,children:n,...i}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i);let a;t[4]===n?a=t[5]:(a=e=>{let{isSelected:t}=e;return G(K,{direction:`row`,justifyContent:`space-between`,alignItems:`center`,gap:`size-200`,width:`100%`,children:[W(`span`,{children:n}),t&&W(H,{svg:W(fn,{})})]})},t[4]=n,t[5]=a);let o;return t[6]!==r||t[7]!==i||t[8]!==a?(o=W(d,{...i,ref:r,children:a}),t[6]=r,t[7]=i,t[8]=a,t[9]=o):o=t[9],o}Gc.displayName=`SelectItem`,q`
  max-width: 100%;
  height: auto;
`;var Kc=16,qc=8,Jc=.05,Yc=Ke`
  from {
    opacity: 0;
    transform: translateY(-130%);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
`,Xc=q`
  position: fixed;
  top: var(--global-dimension-size-200);
  left: 50%;
  width: 400px;
  max-width: calc(100vw - var(--global-dimension-size-400));
  transform: translateX(-50%);
  outline: none;
  z-index: ${On};

  --collapsed-peek: ${Kc}px;
  --expanded-gap: ${qc}px;
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
`,Zc=q`
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  transform-origin: top center;
  transform: translateY(
      calc(var(--toast-index) * var(--collapsed-peek, ${Kc}px))
    )
    scale(calc(1 - var(--toast-index) * ${Jc}));
  opacity: calc(1 - var(--toast-index) * 0.1);
  transition:
    transform 300ms cubic-bezier(0.21, 1.02, 0.73, 1),
    opacity 300ms ease;

  @media (prefers-reduced-motion: reduce) {
    transition: none;
  }
`,Qc=q`
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
  animation: ${Yc} 280ms cubic-bezier(0.21, 1.02, 0.73, 1);
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
`;function $c(e){let t=(0,Z.c)(6),{stackIndex:n,children:r}=e,i=100-n,a;t[0]!==n||t[1]!==i?(a={"--toast-index":n,zIndex:i},t[0]=n,t[1]=i,t[2]=a):a=t[2];let o;return t[3]!==r||t[4]!==a?(o=W(`div`,{className:`toast-positioner`,css:Zc,style:a,children:r}),t[3]=r,t[4]=a,t[5]=o):o=t[5],o}var el=e=>{switch(e){case`success`:return W(H,{svg:W(Yt,{})});case`error`:return W(H,{svg:W(gn,{})});default:return null}},tl=e=>{switch(e){case`success`:return`var(--global-color-success)`;case`error`:return`var(--global-color-danger)`;default:return`var(--global-color-gray-600)`}},nl=e=>{let t=(0,Z.c)(33),{toast:n}=e,{theme:r}=vr(),i=(0,X.useContext)(te),a;t[0]!==i?.visibleToasts||t[1]!==n.key?(a=i?.visibleToasts.findIndex(e=>e.key===n.key)??0,t[0]=i?.visibleToasts,t[1]=n.key,t[2]=a):a=t[2];let o=Math.max(0,a),s;t[3]===n.content.variant?s=t[4]:(s=el(n.content.variant),t[3]=n.content.variant,t[4]=s);let c=s,l;t[5]===n.content.variant?l=t[6]:(l=tl(n.content.variant),t[5]=n.content.variant,t[6]=l);let u;t[7]===l?u=t[8]:(u={"--internal-token-color":l},t[7]=l,t[8]=u);let d;t[9]===Symbol.for(`react.memo_cache_sentinel`)?(d=q`
            display: flex;
            justify-content: space-between;
            width: 100%;
          `,t[9]=d):d=t[9];let f;t[10]!==c||t[11]!==n.content.title?(f=G(V,{slot:`title`,size:`M`,children:[c,n.content.title]}),t[10]=c,t[11]=n.content.title,t[12]=f):f=t[12];let p;t[13]===n.content.message?p=t[14]:(p=W(V,{slot:`description`,children:n.content.message}),t[13]=n.content.message,t[14]=p);let m;t[15]!==f||t[16]!==p?(m=G(ge,{children:[f,p]}),t[15]=f,t[16]=p,t[17]=m):m=t[17];let h;t[18]===Symbol.for(`react.memo_cache_sentinel`)?(h=W(en,{slot:`close`,size:`S`,color:`inherit`,type:`button`,"aria-label":`Close notification`,children:W(H,{svg:W(Xe,{})})}),t[18]=h):h=t[18];let g;t[19]===m?g=t[20]:(g=G(`div`,{css:d,children:[m,h]}),t[19]=m,t[20]=g);let _;t[21]!==n.content.action||t[22]!==n.key?(_=n.content.action?W(`div`,{className:`toast-action-container`,children:typeof n.content.action==`object`&&`text`in n.content.action?W(yt,{className:`toast-action-button`,onPress:()=>{let e=n.content.action;if(typeof e==`object`&&e&&`onClick`in e){let t=e.closeOnClick??!0,r=()=>{ir?.close(n.key)};e.onClick(r),t&&r()}},size:`S`,children:n.content.action.text}):n.content.action}):null,t[21]=n.content.action,t[22]=n.key,t[23]=_):_=t[23];let v;t[24]!==g||t[25]!==_||t[26]!==u||t[27]!==r||t[28]!==n?(v=G(De,{toast:n,css:Qc,className:`react-aria-Toast`,style:u,"data-variant":n.content.variant,"data-theme":r,children:[g,_]}),t[24]=g,t[25]=_,t[26]=u,t[27]=r,t[28]=n,t[29]=v):v=t[29];let y;return t[30]!==o||t[31]!==v?(y=W($c,{stackIndex:o,children:v}),t[30]=o,t[31]=v,t[32]=y):y=t[32],y},rl=q`
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
`;function il(e){let t=(0,Z.c)(12),n,r;t[0]===e?(n=t[1],r=t[2]):({ref:r,...n}=e,t[0]=e,t[1]=n,t[2]=r);let i,a;t[3]===n?(i=t[4],a=t[5]):({children:i,...a}=n,t[3]=n,t[4]=i,t[5]=a);let o;t[6]===i?o=t[7]:(o=e=>{let{isCurrent:t}=e;return G(U,{children:[i,!t&&W(H,{svg:W(Pn,{})})]})},t[6]=i,t[7]=o);let s;return t[8]!==r||t[9]!==a||t[10]!==o?(s=W(ve,{css:rl,...a,className:`breadcrumb`,ref:r,children:o}),t[8]=r,t[9]=a,t[10]=o,t[11]=s):s=t[11],s}var al=q`
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
`;function ol(e){let t=(0,Z.c)(10),n,r;t[0]===e?(n=t[1],r=t[2]):({ref:r,...n}=e,t[0]=e,t[1]=n,t[2]=r);let i,a;t[3]===n?(i=t[4],a=t[5]):({size:a,...i}=n,t[3]=n,t[4]=i,t[5]=a);let o=a===void 0?`M`:a,s;return t[6]!==r||t[7]!==i||t[8]!==o?(s=W(P,{css:al,...i,ref:r,"data-size":o}),t[6]=r,t[7]=i,t[8]=o,t[9]=s):s=t[9],s}var sl=q`
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
`;function cl(e){let t=(0,Z.c)(10),n,r,i,a;t[0]===e?(n=t[1],r=t[2],i=t[3],a=t[4]):({ref:i,size:a,children:n,...r}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a);let o=a===void 0?`M`:a,s;return t[5]!==n||t[6]!==r||t[7]!==i||t[8]!==o?(s=W(`ul`,{ref:i,css:sl,"data-list-size":o,...r,children:n}),t[5]=n,t[6]=r,t[7]=i,t[8]=o,t[9]=s):s=t[9],s}function ll(e){let t=(0,Z.c)(8),n,r,i;t[0]===e?(n=t[1],r=t[2],i=t[3]):({ref:i,children:n,...r}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i);let a;return t[4]!==n||t[5]!==r||t[6]!==i?(a=W(`li`,{ref:i,...r,children:n}),t[4]=n,t[5]=r,t[6]=i,t[7]=a):a=t[7],a}var ul=q`
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
  animation: ${Ke`
  from {
    transform: translate(-50%, var(--global-dimension-size-450));
    opacity: 0;
  }
  to {
    transform: translate(-50%, 0);
    opacity: 1;
  }
`} 0.1s ease-in-out;
`,dl=e=>{let t=(0,Z.c)(2),{children:n}=e,r;return t[0]===n?r=t[1]:(r=W(`div`,{css:ul,children:n}),t[0]=n,t[1]=r),r},fl=q`
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
`;function pl(e){let t=(0,Z.c)(6),n,r;t[0]===e?(n=t[1],r=t[2]):({ref:r,...n}=e,t[0]=e,t[1]=n,t[2]=r);let i;return t[3]!==n||t[4]!==r?(i=W(O,{...n,ref:r,css:fl,children:n.children}),t[3]=n,t[4]=r,t[5]=i):i=t[5],i}var ml=q`
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
`;function hl(e){let t=(0,Z.c)(6),n,r;t[0]===e?(n=t[1],r=t[2]):({ref:r,...n}=e,t[0]=e,t[1]=n,t[2]=r);let i;return t[3]!==n||t[4]!==r?(i=W(En,{...n,ref:r,css:ml,className:`separator react-aria-Separator`}),t[3]=n,t[4]=r,t[5]=i):i=t[5],i}var gl=e=>q`
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
`;function _l(e){let t=(0,Z.c)(82),n,r,i,a,o,s,c,l,u,d,f,p,m,h,g,_,v,y;t[0]===e?(n=t[1],r=t[2],i=t[3],a=t[4],o=t[5],s=t[6],c=t[7],l=t[8],u=t[9],d=t[10],f=t[11],p=t[12],m=t[13],h=t[14],g=t[15],_=t[16],v=t[17],y=t[18]):({ref:u,title:v,titleExtra:y,titleSeparator:f,subTitle:d,headerContent:a,children:n,collapsible:p,interactiveTitle:m,collapseButtonLabel:r,defaultOpen:h,isOpen:o,scrollBody:g,extra:i,onCollapseChange:s,onOpenChange:c,testId:_,...l}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a,t[5]=o,t[6]=s,t[7]=c,t[8]=l,t[9]=u,t[10]=d,t[11]=f,t[12]=p,t[13]=m,t[14]=h,t[15]=g,t[16]=_,t[17]=v,t[18]=y);let b=f===void 0||f,x=p!==void 0&&p,S=m!==void 0&&m,C=h===void 0||h,w=g!==void 0&&g,{styleProps:T}=hn(l,dn),[E,D]=(0,X.useState)(x?!C:!1),O=o==null?E:!o,k=(0,X.useId)(),A=(0,X.useId)(),j=(0,X.useId)(),M=(0,X.useId)(),N;t[19]===s?N=t[20]:(N=e=>{s?.(e)},t[19]=s,t[20]=N);let P=(0,X.useEffectEvent)(N),F;t[21]!==P||t[22]!==O?(F=()=>{P(O)},t[21]=P,t[22]=O,t[23]=F):F=t[23];let I;t[24]===O?I=t[25]:(I=[O],t[24]=O,t[25]=I),(0,X.useEffect)(F,I);let L;t[26]!==v||t[27]!==y?(L=G(Qe,{level:3,weight:`heavy`,className:`card__title`,children:[v,y]}),t[26]=v,t[27]=y,t[28]=L):L=t[28];let R;t[29]===d?R=t[30]:(R=d&&W(Qe,{level:4,className:`card__sub-title`,children:d}),t[29]=d,t[30]=R);let z;t[31]===a?z=t[32]:(z=a&&W(`div`,{className:`card__header-content`,children:a}),t[31]=a,t[32]=z);let ee;t[33]!==R||t[34]!==z||t[35]!==L||t[36]!==j?(ee=G(`div`,{id:j,className:`card__heading`,children:[L,R,z]}),t[33]=R,t[34]=z,t[35]=L,t[36]=j,t[37]=ee):ee=t[37];let te=ee,ne;t[38]!==O||t[39]!==c?(ne=()=>{D(!O),c?.(O)},t[38]=O,t[39]=c,t[40]=ne):ne=t[40];let re=ne,ie;t[41]===re?ie=t[42]:(ie=e=>{let t=e.target;t instanceof Element&&t.closest(`button,a,input,select,textarea,[role="button"]`)||re()},t[41]=re,t[42]=ie);let ae=ie,oe=!O,se=S?r:void 0,ce=S&&r==null?j:void 0,le=!O,ue;t[43]===le?ue=t[44]:(ue=W(Nt,{isExpanded:le,className:`card__collapse-toggle-icon`}),t[43]=le,t[44]=ue);let de=!S&&te,fe;t[45]!==M||t[46]!==A||t[47]!==oe||t[48]!==se||t[49]!==ce||t[50]!==ue||t[51]!==de||t[52]!==re?(fe=G(`button`,{onClick:re,className:`card__collapsible-button button--reset`,id:A,"aria-controls":M,"aria-expanded":oe,"aria-label":se,"aria-labelledby":ce,children:[ue,de]}),t[45]=M,t[46]=A,t[47]=oe,t[48]=se,t[49]=ce,t[50]=ue,t[51]=de,t[52]=re,t[53]=fe):fe=t[53];let pe=fe,me;t[54]===T.style?me=t[55]:(me=gl(T.style),t[54]=T.style,t[55]=me);let he;t[56]!==pe||t[57]!==x||t[58]!==ae||t[59]!==te||t[60]!==S?(he=x?S?G(`div`,{className:`card__collapsible-header`,onClick:ae,children:[pe,te]}):pe:te,t[56]=pe,t[57]=x,t[58]=ae,t[59]=te,t[60]=S,t[61]=he):he=t[61];let ge;t[62]!==i||t[63]!==k||t[64]!==he?(ge=G(`header`,{id:k,children:[he,i]}),t[62]=i,t[63]=k,t[64]=he,t[65]=ge):ge=t[65];let _e;t[66]!==M||t[67]!==n||t[68]!==k||t[69]!==O||t[70]!==w?(_e=W(`div`,{className:`card__body`,id:M,"aria-labelledby":k,"aria-hidden":O,"data-scrollable":w,children:n}),t[66]=M,t[67]=n,t[68]=k,t[69]=O,t[70]=w,t[71]=_e):_e=t[71];let ve;return t[72]!==x||t[73]!==O||t[74]!==u||t[75]!==T.style||t[76]!==me||t[77]!==ge||t[78]!==_e||t[79]!==_||t[80]!==b?(ve=G(`section`,{ref:u,css:me,className:`card`,"data-collapsible":x,"data-collapsed":O,"data-title-separator":b,"data-testid":_,style:T.style,children:[ge,_e]}),t[72]=x,t[73]=O,t[74]=u,t[75]=T.style,t[76]=me,t[77]=ge,t[78]=_e,t[79]=_,t[80]=b,t[81]=ve):ve=t[81],ve}var vl=q`
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
`;function yl(e){let t=(0,Z.c)(13),n,r,i,a,o;t[0]===e?(n=t[1],r=t[2],i=t[3],a=t[4],o=t[5]):({ref:i,children:n,labelPlacement:a,size:o,...r}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a,t[5]=o);let s=a===void 0?`end`:a,c=o===void 0?`M`:o,l;t[6]===Symbol.for(`react.memo_cache_sentinel`)?(l=W(`div`,{className:`indicator`}),t[6]=l):l=t[6];let u;return t[7]!==n||t[8]!==s||t[9]!==r||t[10]!==i||t[11]!==c?(u=G(z,{...r,ref:i,css:vl,"data-label-placement":s,"data-size":c,children:[l,n]}),t[7]=n,t[8]=s,t[9]=r,t[10]=i,t[11]=c,t[12]=u):u=t[12],u}q`
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
`;var bl=q`
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
`,xl=q`
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
`;function Sl(e,t){let{si:n=!1,decimalPlaces:r=1}=t??{},i=n?1e3:1024;if(Math.abs(e)<i)return e+` B`;let a=n?[`kB`,`MB`,`GB`,`TB`,`PB`,`EB`,`ZB`,`YB`]:[`KiB`,`MiB`,`GiB`,`TiB`,`PiB`,`EiB`,`ZiB`,`YiB`],o=-1,s=10**r;do e/=i,++o;while(Math.round(Math.abs(e)*s)/s>=i&&o<a.length-1);return e.toFixed(r)+` `+a[o]}function Cl(e,t){return!t||t.length===0||t.some(t=>{if(t.startsWith(`.`))return e.name.toLowerCase().endsWith(t.toLowerCase());if(t.endsWith(`/*`)){let n=t.slice(0,-2);return e.type.startsWith(n)}return e.type===t})}function wl(e,t){return t==null||e.size<=t}function Tl(e){let t=(0,Z.c)(46),n,r,i,a,o,s,c,l,u,d;t[0]===e?(n=t[1],r=t[2],i=t[3],a=t[4],o=t[5],s=t[6],c=t[7],l=t[8],u=t[9],d=t[10]):({acceptedFileTypes:n,allowsMultiple:u,maxFiles:s,maxFileSize:o,onSelect:c,onSelectRejected:l,label:d,description:i,isDisabled:a,...r}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a,t[5]=o,t[6]=s,t[7]=c,t[8]=l,t[9]=u,t[10]=d);let f=u!==void 0&&u,p=d===void 0?`Drag and drop files here`:d,m=(0,X.useRef)(null),h=(0,X.useRef)(null),g,_;t[11]===a?(g=t[12],_=t[13]):(g=()=>{let e=h.current;if(!e||a)return;let t=e=>{(e.key===`Enter`||e.key===` `)&&(e.preventDefault(),m.current?.click())};return e.addEventListener(`keydown`,t),()=>e.removeEventListener(`keydown`,t)},_=[a],t[11]=a,t[12]=g,t[13]=_),(0,X.useEffect)(g,_);let v;t[14]!==n||t[15]!==f||t[16]!==o||t[17]!==s||t[18]!==c||t[19]!==l?(v=e=>{let t=[],r=[],i=f?s??1/0:1;for(let a of e){if(!Cl(a,n)){r.push({file:a,reason:`type`,message:`File type not accepted. Allowed: ${n?.join(`, `)}`});continue}if(!wl(a,o)){r.push({file:a,reason:`size`,message:`File too large. Maximum size: ${Sl(o)}`});continue}if(t.length>=i){r.push({file:a,reason:`count`,message:`Maximum ${i} file${i>1?`s`:``} allowed`});continue}t.push(a)}t.length>0&&c&&c(t),r.length>0&&l&&l(r)},t[14]=n,t[15]=f,t[16]=o,t[17]=s,t[18]=c,t[19]=l,t[20]=v):v=t[20];let y=v,x;t[21]===y?x=t[22]:(x=e=>{e.target.files&&(y(Array.from(e.target.files)),e.target.value=``)},t[21]=y,t[22]=x);let S=x,C;t[23]===y?C=t[24]:(C=async e=>{let t=e.items.filter(kl),n=(await Promise.allSettled(t.map(Ol))).filter(Dl).map(El);n.length>0&&y(n)},t[23]=y,t[24]=C);let w=C,T;t[25]!==n||t[26]!==a?(T=e=>a?`cancel`:!n||n.length===0||n.some(t=>t.startsWith(`.`)||t.endsWith(`/*`)?!0:e.has(t))?`copy`:`cancel`,t[25]=n,t[26]=a,t[27]=T):T=t[27];let E=T,D;t[28]===a?D=t[29]:(D=()=>{a||m.current?.click()},t[28]=a,t[29]=D);let O=D,k;t[30]!==n||t[31]!==i?(k=i??(n&&n.length>0?`Accepted: ${n.join(`, `)}`:void 0),t[30]=n,t[31]=i,t[32]=k):k=t[32];let A=k,j;t[33]!==n||t[34]!==f||t[35]!==A||t[36]!==S||t[37]!==p||t[38]!==O?(j=e=>{let{isDropTarget:t}=e;return G(U,{children:[W(`input`,{ref:m,type:`file`,accept:n?.join(`,`),multiple:f,onChange:S,hidden:!0}),G(`div`,{className:`file-drop-zone__trigger`,onClick:O,children:[W(`div`,{className:`file-drop-zone__icon`,children:W(H,{svg:W(Tt,{})})}),W(St,{className:`file-drop-zone__label`,children:t?`Drop files here`:p}),A?W(St,{className:`file-drop-zone__description`,children:A}):null]})]})},t[33]=n,t[34]=f,t[35]=A,t[36]=S,t[37]=p,t[38]=O,t[39]=j):j=t[39];let M;return t[40]!==r||t[41]!==E||t[42]!==w||t[43]!==a||t[44]!==j?(M=W(b,{ref:h,css:bl,onDrop:w,getDropOperation:E,isDisabled:a,...r,children:j}),t[40]=r,t[41]=E,t[42]=w,t[43]=a,t[44]=j,t[45]=M):M=t[45],M}function El(e){return e.value}function Dl(e){return e.status===`fulfilled`}function Ol(e){return e.getFile()}function kl(e){return e.kind===`file`}function Al(e){switch(e.status){case`pending`:return`Pending`;case`uploading`:return`Uploading${e.progress===void 0?``:` ${e.progress}%`}`;case`parsing`:return`Parsing...`;case`complete`:return`Complete`;case`error`:return`Error`;default:return``}}function jl(e){let t=(0,Z.c)(32),{file:n,onRemove:r,isDisabled:i}=e,{file:a,progress:o,status:s,error:c}=n,l=s===`uploading`&&o!==void 0,u;t[0]===Symbol.for(`react.memo_cache_sentinel`)?(u=W(`div`,{className:`file-list__icon`,children:W(H,{svg:W(kt,{})})}),t[0]=u):u=t[0];let d;t[1]===a.name?d=t[2]:(d=W(`span`,{className:`file-list__name`,title:a.name,children:a.name}),t[1]=a.name,t[2]=d);let f;t[3]===a.size?f=t[4]:(f=Sl(a.size),t[3]=a.size,t[4]=f);let p;t[5]===f?p=t[6]:(p=W(`span`,{children:f}),t[5]=f,t[6]=p);let m;t[7]!==n||t[8]!==s?(m=s&&G(U,{children:[W(`span`,{children:`-`}),W(`span`,{children:Al(n)})]}),t[7]=n,t[8]=s,t[9]=m):m=t[9];let h;t[10]!==p||t[11]!==m?(h=G(`div`,{className:`file-list__meta`,children:[p,m]}),t[10]=p,t[11]=m,t[12]=h):h=t[12];let g;t[13]===c?g=t[14]:(g=c&&W(`span`,{className:`file-list__error`,children:c}),t[13]=c,t[14]=g);let _;t[15]!==o||t[16]!==l?(_=l&&W(`div`,{className:`file-list__progress`,children:W(Ni,{value:o,width:`100%`,height:`4px`})}),t[15]=o,t[16]=l,t[17]=_):_=t[17];let v;t[18]!==d||t[19]!==h||t[20]!==g||t[21]!==_?(v=G(`div`,{className:`file-list__details`,children:[d,h,g,_]}),t[18]=d,t[19]=h,t[20]=g,t[21]=_,t[22]=v):v=t[22];let y;t[23]!==a||t[24]!==i||t[25]!==r||t[26]!==s?(y=r&&W(`div`,{className:`file-list__remove`,children:W(en,{size:`S`,"aria-label":`Remove ${a.name}`,onPress:()=>r(a),isDisabled:i||s===`uploading`||s===`parsing`,children:W(H,{svg:W(Xe,{})})})}),t[23]=a,t[24]=i,t[25]=r,t[26]=s,t[27]=y):y=t[27];let b;return t[28]!==s||t[29]!==y||t[30]!==v?(b=G(`li`,{className:`file-list__item`,"data-status":s,children:[u,v,y]}),t[28]=s,t[29]=y,t[30]=v,t[31]=b):b=t[31],b}function Ml(e){let t=(0,Z.c)(12),{files:n,onRemove:r,isDisabled:i,children:a,"aria-label":o}=e,s=o===void 0?`Selected files`:o;if(n.length===0)return null;let c=Nl,l;t[0]!==a||t[1]!==i||t[2]!==r?(l=(e,t)=>a?W(X.Fragment,{children:a(e,t)},c(e)):W(jl,{file:e,onRemove:r,isDisabled:i},c(e)),t[0]=a,t[1]=i,t[2]=r,t[3]=l):l=t[3];let u=l,d;if(t[4]!==n||t[5]!==u){let e;t[7]===u?e=t[8]:(e=(e,t)=>u(e,t),t[7]=u,t[8]=e),d=n.map(e),t[4]=n,t[5]=u,t[6]=d}else d=t[6];let f;return t[9]!==s||t[10]!==d?(f=W(`ul`,{css:xl,"aria-label":s,children:d}),t[9]=s,t[10]=d,t[11]=f):f=t[11],f}function Nl(e){return`${e.file.name}-${e.file.size}-${e.file.lastModified}`}var Pl=e=>q`
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: ${e};
  overflow: hidden;
  text-overflow: ellipsis;
`;function Fl(e){let t=(0,Z.c)(5),{children:n,lines:r}=e,i;t[0]===r?i=t[1]:(i=Pl(r),t[0]=r,t[1]=i);let a;return t[2]!==n||t[3]!==i?(a=W(`div`,{css:i,children:n}),t[2]=n,t[3]=i,t[4]=a):a=t[4],a}function Il(e){let t=(0,Z.c)(3),{children:n}=e,r;t[0]===Symbol.for(`react.memo_cache_sentinel`)?(r={display:`contents`},t[0]=r):r=t[0];let i;return t[1]===n?i=t[2]:(i=W(`div`,{style:r,onClick:Hl,onKeyDown:Vl,onKeyUp:Bl,onMouseDown:zl,onPointerDown:Rl,onPointerUp:Ll,children:n}),t[1]=n,t[2]=i),i}function Ll(e){return e.stopPropagation()}function Rl(e){return e.stopPropagation()}function zl(e){return e.stopPropagation()}function Bl(e){return e.stopPropagation()}function Vl(e){return e.stopPropagation()}function Hl(e){return e.stopPropagation()}var Ul=q`
  border-radius: var(--global-dimension-size-50);
  border: 1px solid var(--global-border-color-default);
  transition: background-color 0.2s;
  &[data-clickable="true"] {
    cursor: pointer;
    &:hover {
      background-color: var(--global-color-gray-300);
    }
  }
`,Wl=q`
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
`,Gl=q`
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
`,Kl=q`
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
    ${Ul};
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
`,ql=1.5;function Jl(e){return e.offsetWidth>0||e.offsetHeight>0}function Yl(e){return Array.from(e.children).filter(e=>e instanceof HTMLElement&&Jl(e))}function Xl(e){let{paddingRight:t}=getComputedStyle(e);return e.clientWidth-(parseFloat(t)||0)}function Zl(e){let t=Yl(e),n=Xl(e),r=0,i=0,a=0,o=1/0,s=-1/0;for(let e of t){let t=e.offsetTop,c=t+e.offsetHeight;if(r>0&&(t>=s||c<=o))break;let l=e.offsetLeft+e.offsetWidth;if(l>n+ql)break;r+=1,o=Math.min(o,t),s=Math.max(s,c),i=Math.max(i,l),a=Math.max(a,e.offsetHeight)}return{items:t,visibleCount:r,badgeLeft:i,lineHeight:a||(t[0]?.offsetHeight??0)}}var Ql=[{name:`inert`,value:``,flag:`overflowRowInert`},{name:`aria-hidden`,value:`true`,flag:`overflowRowAriaHidden`}];function $l({items:e,visibleCount:t}){e.forEach((e,n)=>{if(n<t){eu(e);return}for(let{name:t,value:n,flag:r}of Ql)e.hasAttribute(t)||(e.dataset[r]=`true`,e.setAttribute(t,n))})}function eu(e){for(let{name:t,flag:n}of Ql)e.dataset[n]&&(delete e.dataset[n],e.removeAttribute(t))}function tu(e){for(let t of Array.from(e.children))t instanceof HTMLElement&&eu(t)}var nu={childList:!0,characterData:!0,subtree:!0};function ru(e){let t=e=>(e instanceof Element?e:e.parentElement)?.closest(`.overflow-row__badge-slot`)!=null;return e.type===`childList`?[...e.addedNodes,...e.removedNodes].every(t):t(e.target)}function iu(e,t){return e===null||t===null?e===t:e.hiddenCount===t.hiddenCount&&e.visibleCount===t.visibleCount&&e.badgeLeft===t.badgeLeft&&e.lineHeight===t.lineHeight}function au(e){let t=(0,Z.c)(5),{visibleCount:n,children:r}=e,i=(0,X.useRef)(null),a,o;t[0]===n?(a=t[1],o=t[2]):(a=()=>{let e=i.current;if(!e)return;let t=()=>{let t=Array.from(e.children).filter(su);for(let e of t)e.dataset.overflowRowHidden&&(e.style.display=``,delete e.dataset.overflowRowHidden);t.filter(Jl).slice(0,n).forEach(ou)};t();let r=new MutationObserver(t);return r.observe(e,nu),()=>r.disconnect()},o=[n],t[0]=n,t[1]=a,t[2]=o),(0,X.useLayoutEffect)(a,o);let s;return t[3]===r?s=t[4]:(s=W(K,{ref:i,direction:`row`,wrap:`wrap`,gap:`size-50`,maxWidth:`size-5000`,children:r}),t[3]=r,t[4]=s),s}function ou(e){e.style.display=`none`,e.dataset.overflowRowHidden=`true`}function su(e){return e instanceof HTMLElement}function cu(e){let t=(0,Z.c)(21),{children:n,isExpanded:r}=e,i=r!==void 0&&r,a=(0,X.useRef)(null),o=(0,X.useRef)(null),[s,c]=(0,X.useState)(null),l,u;t[0]===i?(l=t[1],u=t[2]):(l=()=>{let e=a.current;if(i||!e){c(null);return}let t=null,n=()=>{t=e.getBoundingClientRect().width;let{items:n,visibleCount:r,badgeLeft:i,lineHeight:a}=Zl(e);$l({items:n,visibleCount:r});let o=n.length-r,s=o===0?null:{hiddenCount:o,visibleCount:r,badgeLeft:i,lineHeight:a};c(e=>iu(e,s)?e:s)};n(),o.current=n;let r=!1;document.fonts?.status===`loading`&&document.fonts.ready.then(()=>{r||n()});let s=new ResizeObserver(e=>{let[r]=e,i=r?.borderBoxSize?.[0]?.inlineSize??null;i!==null&&i===t||(t=i,n())});s.observe(e);let l=new MutationObserver(e=>{e.every(ru)||n()});return l.observe(e,nu),()=>{r=!0,s.disconnect(),l.disconnect(),o.current=null,tu(e)}},u=[i],t[0]=i,t[1]=l,t[2]=u),(0,X.useLayoutEffect)(l,u);let d,f;t[3]===s?(d=t[4],f=t[5]):(d=()=>{s!==null&&o.current?.()},f=[s],t[3]=s,t[4]=d,t[5]=f),(0,X.useLayoutEffect)(d,f);let p=!i,m=!i&&s!==null,h=!i&&s!==null&&s.visibleCount===0,g;t[6]!==p||t[7]!==m||t[8]!==h?(g=B(`overflow-row`,{"overflow-row--collapsed":p,"overflow-row--overflowing":m,"overflow-row--badge-only":h}),t[6]=p,t[7]=m,t[8]=h,t[9]=g):g=t[9];let _;t[10]===s?_=t[11]:(_=s===null?void 0:{"--overflow-row-badge-left":`calc(${s.badgeLeft}px + var(--global-dimension-size-50))`,"--overflow-row-line-height":`${s.lineHeight}px`},t[10]=s,t[11]=_);let v;t[12]!==n||t[13]!==i||t[14]!==s?(v=!i&&s!==null?W(`div`,{className:`overflow-row__badge-slot`,children:G(Ot,{children:[G(Et,{className:`overflow-row__badge`,"data-clickable":`true`,"aria-label":`Show ${s.hiddenCount} more`,children:[`+`,s.hiddenCount]}),W(Il,{children:G(jn,{placement:`bottom end`,children:[W(Ct,{}),W(Zt,{children:W(Fi,{padding:`size-150`,children:W(au,{visibleCount:s.visibleCount,children:n})})})]})})]})}):null,t[12]=n,t[13]=i,t[14]=s,t[15]=v):v=t[15];let y;return t[16]!==n||t[17]!==_||t[18]!==v||t[19]!==g?(y=G(`div`,{ref:a,css:Kl,className:g,style:_,children:[n,v]}),t[16]=n,t[17]=_,t[18]=v,t[19]=g,t[20]=y):y=t[20],y}var lu=q`
  text-overflow: ellipsis;
  overflow: hidden;
  white-space: nowrap;
`,uu=q`
  display: -webkit-box;
  -webkit-box-orient: vertical;
  overflow: hidden;
`,du=e=>{let t=(0,Z.c)(11),{children:n,maxWidth:r,title:i,maxLines:a}=e,o=(a??0)>1,s=o?uu:lu,c;t[0]!==o||t[1]!==a?(c=o&&{WebkitLineClamp:a},t[0]=o,t[1]=a,t[2]=c):c=t[2];let l;t[3]!==r||t[4]!==c?(l={maxWidth:r,...c},t[3]=r,t[4]=c,t[5]=l):l=t[5];let u;return t[6]!==n||t[7]!==s||t[8]!==l||t[9]!==i?(u=W(`div`,{css:s,style:l,title:i,children:n}),t[6]=n,t[7]=s,t[8]=l,t[9]=i,t[10]=u):u=t[10],u};function fu(){let e=(0,Z.c)(3),t,n;e[0]===Symbol.for(`react.memo_cache_sentinel`)?(t=W(en,{slot:`previous`,size:`S`,children:W(H,{svg:W(Tn,{})})}),n=W(Ge,{className:`calendar__heading`}),e[0]=t,e[1]=n):(t=e[0],n=e[1]);let r;return e[2]===Symbol.for(`react.memo_cache_sentinel`)?(r=G(`header`,{className:`calendar__header`,children:[t,n,W(en,{slot:`next`,size:`S`,children:W(H,{svg:W(Pn,{})})})]}),e[2]=r):r=e[2],r}function pu(e){let t=(0,Z.c)(8),{months:n,errorMessage:r}=e,i;t[0]===Symbol.for(`react.memo_cache_sentinel`)?(i=W(fu,{}),t[0]=i):i=t[0];let a;t[1]===n?a=t[2]:(a=W(`div`,{className:`calendar__months`,children:Array.from({length:n},mu)}),t[1]=n,t[2]=a);let o;t[3]===r?o=t[4]:(o=r&&W(St,{slot:`errorMessage`,children:r}),t[3]=r,t[4]=o);let s;return t[5]!==a||t[6]!==o?(s=G(U,{children:[i,a,o]}),t[5]=a,t[6]=o,t[7]=s):s=t[7],s}function mu(e,t){return W(f,{offset:{months:t},children:hu},t)}function hu(e){return W(k,{date:e})}var gu=q`
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
`,_u=q`
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
`,vu=q`
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
`;function yu(e){let t=(0,Z.c)(10),n,r,i,a;if(t[0]!==e){let{ref:o,...s}=e;r=o;let{css:c,...l}=s;i=l,n=fe,a=q(Ho,vu,c),t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a}else n=t[1],r=t[2],i=t[3],a=t[4];let o;return t[5]!==n||t[6]!==r||t[7]!==i||t[8]!==a?(o=W(n,{css:a,...i,"data-size":`S`,ref:r}),t[5]=n,t[6]=r,t[7]=i,t[8]=a,t[9]=o):o=t[9],o}function bu(e){let t=(0,Z.c)(17),n,r,i,a,o;t[0]===e?(n=t[1],r=t[2],i=t[3],a=t[4],o=t[5]):({errorMessage:r,css:i,children:n,ref:a,...o}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a,t[5]=o);let s=e.visibleDuration?.months||1,c;t[6]===i?c=t[7]:(c=q(gu,_u,i),t[6]=i,t[7]=c);let l;t[8]!==n||t[9]!==r||t[10]!==s?(l=n??W(pu,{months:s,errorMessage:r}),t[8]=n,t[9]=r,t[10]=s,t[11]=l):l=t[11];let u;return t[12]!==a||t[13]!==o||t[14]!==c||t[15]!==l?(u=W(D,{ref:a,css:c,...o,children:l}),t[12]=a,t[13]=o,t[14]=c,t[15]=l,t[16]=u):u=t[16],u}q`
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
`;var xu=q`
  font-family: var(--global-font-family-mono);
  font-variant-numeric: tabular-nums;
  ${He};
`;function Su(e){return e.toString().padStart(2,`0`)}function Cu(e){let t=Math.floor(e/3600),n=Math.floor(e%3600/60),r=e%60;return t>0?`${Su(t)}:${Su(n)}:${Su(r)}`:`${Su(n)}:${Su(r)}`}function wu(e){return Math.max(0,Math.floor((Date.now()-e.getTime())/1e3))}function Tu(e){let t=(0,Z.c)(18),{startTime:n,color:r,size:i}=e,a=r===void 0?`text-900`:r,o=i===void 0?`S`:i,s;t[0]===n?s=t[1]:(s=n??new Date,t[0]=n,t[1]=s);let c=s,l;t[2]===c?l=t[3]:(l=()=>wu(c),t[2]=c,t[3]=l);let[u,d]=(0,X.useState)(l),f,p;t[4]===c?(f=t[5],p=t[6]):(f=()=>{d(wu(c));let e=setInterval(()=>{d(wu(c))},1e3);return()=>clearInterval(e)},p=[c],t[4]=c,t[5]=f,t[6]=p),(0,X.useEffect)(f,p);let m;t[7]===a?m=t[8]:(m=vt(a),t[7]=a,t[8]=m);let h;t[9]===m?h=t[10]:(h={color:m},t[9]=m,t[10]=h);let g=`PT${u}S`,_;t[11]===u?_=t[12]:(_=Cu(u),t[11]=u,t[12]=_);let v;return t[13]!==o||t[14]!==h||t[15]!==g||t[16]!==_?(v=W(`time`,{css:xu,"data-size":o,style:h,dateTime:g,children:_}),t[13]=o,t[14]=h,t[15]=g,t[16]=_,t[17]=v):v=t[17],v}var Eu=2e3,Du=q`
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
    ${Wl}
  }
`,Ou=e=>{let t=(0,Z.c)(20),{id:n,size:r,tooltipText:i,variant:a}=e,o=r===void 0?`S`:r,s=i===void 0?`Copy ID`:i,c=a===void 0?`badge`:a,[l,u]=(0,X.useState)(!1),d=l?`success`:`inherit`,f=l?`Checkmark`:`Duplicate`,p;t[0]!==d||t[1]!==f?(p=W(H,{className:`id-badge__copy-icon`,color:d,svgKey:f}),t[0]=d,t[1]=f,t[2]=p):p=t[2];let m=p,h=`${s} ${n}`,g;t[3]===n?g=t[4]:(g=()=>{x(n),u(!0),setTimeout(()=>{u(!1)},Eu)},t[3]=n,t[4]=g);let _;t[5]!==m||t[6]!==n||t[7]!==o||t[8]!==c?(_=c===`badge`?G(Fo,{size:o,children:[W(H,{svgKey:`ID`}),W(V,{fontFamily:`mono`,size:`S`,color:`text-700`,children:n}),m]}):G(U,{children:[W(V,{fontFamily:`mono`,size:`S`,color:`text-500`,children:n}),m]}),t[5]=m,t[6]=n,t[7]=o,t[8]=c,t[9]=_):_=t[9];let v;t[10]!==h||t[11]!==g||t[12]!==_||t[13]!==c?(v=W(Et,{css:Du,"data-variant":c,"aria-label":h,onPress:g,children:_}),t[10]=h,t[11]=g,t[12]=_,t[13]=c,t[14]=v):v=t[14];let y=l?`Copied`:s,b;t[15]===y?b=t[16]:(b=W(Ri,{offset:1,children:y}),t[15]=y,t[16]=b);let S;return t[17]!==v||t[18]!==b?(S=G(A,{children:[v,b]}),t[17]=v,t[18]=b,t[19]=S):S=t[19],S},ku=e=>{let t=(0,Z.c)(7),{title:n,id:r}=e,i;t[0]===n?i=t[1]:(i=W(Qe,{children:n}),t[0]=n,t[1]=i);let a;t[2]===r?a=t[3]:(a=W(Ou,{size:`S`,id:r}),t[2]=r,t[3]=a);let o;return t[4]!==i||t[5]!==a?(o=G(K,{direction:`row`,gap:`size-100`,alignItems:`center`,children:[i,a]}),t[4]=i,t[5]=a,t[6]=o):o=t[6],o},Au=`selectedSpanNodeId`,ju=`sessionView`,Mu=`selectedTraceId`,Nu=[Mu,Au],Pu=`timeRangeKey`,Fu=`timeRangeStart`,Iu=`timeRangeEnd`,Lu=`labelId`,Ru=`createCodeEvaluator`,zu=`createLlmEvaluator`,Bu=[{key:`15m`,label:`Last 15 Min`},{key:`1h`,label:`Last Hour`},{key:`12h`,label:`Last 12 Hours`},{key:`1d`,label:`Last Day`},{key:`7d`,label:`Last 7 Days`},{key:`30d`,label:`Last Month`}],Vu=Bu.reduce((e,t)=>({...e,[t.key]:t}),{}),Hu=60*1e3,Uu=60*Hu,Wu=24*Uu,Gu=/^(\d+)([mhd])$/;function Ku(e){if(typeof e!=`string`)return null;let t=Gu.exec(e);if(!t)return null;let n=parseInt(t[1],10);return n<1?null:{quantity:n,unit:t[2]}}function qu({quantity:e,unit:t}){switch(t){case`m`:return e*Hu;case`h`:return e*Uu;case`d`:return e*Wu;default:return Yn(t)}}function Ju(e,t=Date.now()){let n=Ku(e);if(!n)throw Error(`Invalid last N time range key: ${e}`);let{quantity:r,unit:i}=n,a;switch(i){case`m`:a=Ee(t,r);break;case`h`:a=R(t,r);break;case`d`:a=me(t,r);break;default:Yn(i)}return{start:(qu(n)<=Uu?Ae:ee)(a),end:null}}function Yu(e){let t=Ku(e),n=t&&qu(t)<=Uu?Hu:Uu,r=Date.now()%n;return r===0?n:n-r}function Xu(e){return Ku(e)!==null}function Zu(e){if(e==null||e.trim()===``)return null;let t=new Date(e);return Number.isNaN(t.getTime())?void 0:t}function Qu(e,t=Date.now()){let n=e.get(Pu);if(Xu(n))return{timeRangeKey:n,...Ju(n,t)};let r=Zu(e.get(Fu)),i=Zu(e.get(Iu));return r===void 0||i===void 0||r==null&&i==null||r!=null&&i!=null&&r>i?null:{timeRangeKey:`custom`,start:r,end:i}}function $u({searchParams:e,timeRange:t}){let n=new URLSearchParams(e),r=(e,t)=>{t==null?n.delete(e):n.set(e,t.toISOString())};return Xu(t.timeRangeKey)?(n.set(Pu,t.timeRangeKey),n.delete(Fu),n.delete(Iu),n):(n.delete(Pu),r(Fu,t.start),r(Iu,t.end),n)}var ed={m:{singular:`minute`,plural:`minutes`},h:{singular:`hour`,plural:`hours`},d:{singular:`day`,plural:`days`}};function td(e){let t=Vu[e];if(t)return t.label;let n=Ku(e);if(!n)return e;let{quantity:r,unit:i}=n,{singular:a,plural:o}=ed[i];return`Last ${r} ${r===1?a:o}`}var nd=/^(?:last\s+)?(\d+)\s*(m|min|mins|minute|minutes|h|hr|hrs|hour|hours|d|day|days)$/,rd=/^(?:last\s+)?(\d+)$/;function id(e){let t=nd.exec(e.trim().toLowerCase());if(!t)return null;let n=parseInt(t[1],10);return n<1?null:`${n}${t[2][0]}`}function ad(e){let t=id(e);if(t)return[t];let n=rd.exec(e.trim().toLowerCase());if(!n)return[];let r=parseInt(n[1],10);return r<1?[]:[`${r}m`,`${r}h`,`${r}d`]}var od=.5,sd=2,cd=Hu;function ld({value:e,now:t}){if(!e.start)return null;let n=e.start.getTime(),r=(e.end??t).getTime(),i=r-n;return i<=0?null:{startMs:n,endMs:r,durationMs:i}}function ud(e){let t=Math.max(1,Math.round(e/Hu)),n=t/1440;if(n>=2||Number.isInteger(n))return`${Math.round(n)}d`;let r=t/60;return r>=2||Number.isInteger(r)?`${Math.round(r)}h`:`${t}m`}function dd({value:e,now:t=new Date,shiftFraction:n=od}){let r=ld({value:e,now:t});if(!r)return null;let i=r.durationMs*n;return{timeRangeKey:`custom`,start:new Date(r.startMs-i),end:new Date(r.endMs-i)}}function fd({value:e,now:t=new Date,shiftFraction:n=od}){if(!e.end)return null;let r=ld({value:e,now:t});if(!r)return null;let i=Math.min(r.durationMs*n,t.getTime()-r.endMs);return i<=0?null:{timeRangeKey:`custom`,start:new Date(r.startMs+i),end:new Date(r.endMs+i)}}function pd({value:e,now:t=new Date,zoomFactor:n=sd,minWindowMs:r=cd}){return hd({value:e,now:t,factor:1/n,minWindowMs:r})}function md({value:e,now:t=new Date,zoomFactor:n=sd,minWindowMs:r=cd}){return hd({value:e,now:t,factor:n,minWindowMs:r})}function hd({value:e,now:t,factor:n,minWindowMs:r}){if(!e.end){let i=Ku(e.timeRangeKey),a=i?qu(i):ld({value:e,now:t})?.durationMs;if(a==null)return null;let o=Math.max(a*n,r);if(n<1&&o>=a)return null;let s=ud(o);return s===e.timeRangeKey?null:{timeRangeKey:s,...Ju(s)}}let i=ld({value:e,now:t});if(!i)return null;let a=Math.max(i.durationMs*n,r);if(n<1?a>=i.durationMs:a===i.durationMs)return null;let o=(i.startMs+i.endMs)/2,s=o-a/2,c=o+a/2,l=c-t.getTime();return l>0&&(s-=l,c-=l),{timeRangeKey:`custom`,start:new Date(s),end:new Date(c)}}function gd(e,t){return e?_e(e,t):null}var _d=q`
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
`,vd=q`
  .react-aria-DateInput {
    width: 100%;
    min-width: 0;
  }
`,yd=new j(0,0,0),bd=new j(23,59,59);function xd(e){let n=(0,Z.c)(56),{value:r,timeZone:i,onApply:a,onCancel:o}=e,s;n[0]!==i||n[1]!==r.start?(s=()=>gd(r.start,i),n[0]=i,n[1]=r.start,n[2]=s):s=n[2];let[c,l]=(0,X.useState)(s),u;n[3]!==i||n[4]!==r.end?(u=()=>gd(r.end,i)??Ce(i),n[3]=i,n[4]=r.end,n[5]=u):u=n[5];let[d,f]=(0,X.useState)(u),p;n[6]!==c||n[7]!==i?(p=c?c.toDate(i):null,n[6]=c,n[7]=i,n[8]=p):p=n[8];let m=p,h;n[9]!==d||n[10]!==i?(h=d?d.toDate(i):null,n[9]=d,n[10]=i,n[11]=h):h=n[11];let g=h,v=!!(m&&g&&m>g),y;n[12]!==g||n[13]!==v||n[14]!==m?(y=m&&g&&!v?{start:m,end:g}:null,n[12]=g,n[13]=v,n[14]=m,n[15]=y):y=n[15];let b=y,x;n[16]!==d||n[17]!==v||n[18]!==c?(x=c&&d&&!v?{start:ne(c),end:ne(d)}:null,n[16]=d,n[17]=v,n[18]=c,n[19]=x):x=n[19];let S=x,C;n[20]===Symbol.for(`react.memo_cache_sentinel`)?(C={months:2},n[20]=C):C=n[20];let w;n[21]===i?w=n[22]:(w=e=>{e&&(l(t(Oe(e.start,yd),i)),f(t(Oe(e.end,bd),i)))},n[21]=i,n[22]=w);let T;n[23]!==S||n[24]!==w?(T=W(bu,{"aria-label":`Time range`,visibleDuration:C,value:S,onChange:w}),n[23]=S,n[24]=w,n[25]=T):T=n[25];let E,D;n[26]===Symbol.for(`react.memo_cache_sentinel`)?(D=W(Cn,{children:`Start`}),E=W(_,{children:Cd}),n[26]=E,n[27]=D):(E=n[26],D=n[27]);let O;n[28]===c?O=n[29]:(O=G(yu,{granularity:`minute`,hideTimeZone:!0,value:c,onChange:l,css:vd,children:[D,E]}),n[28]=c,n[29]=O);let k,A;n[30]===Symbol.for(`react.memo_cache_sentinel`)?(k=W(Cn,{children:`End`}),A=W(_,{children:Sd}),n[30]=k,n[31]=A):(k=n[30],A=n[31]);let j;n[32]!==d||n[33]!==v?(j=G(yu,{granularity:`minute`,hideTimeZone:!0,isInvalid:v,value:d,onChange:f,css:vd,children:[k,A]}),n[32]=d,n[33]=v,n[34]=j):j=n[34];let M;n[35]!==O||n[36]!==j?(M=G(`div`,{className:`time-range-calendar-picker__fields`,children:[O,j]}),n[35]=O,n[36]=j,n[37]=M):M=n[37];let N;n[38]===v?N=n[39]:(N=v&&W(V,{size:`XS`,color:`danger`,className:`time-range-calendar-picker__error`,children:`End must be after the start`}),n[38]=v,n[39]=N);let P;n[40]===o?P=n[41]:(P=W(yt,{size:`S`,onPress:o,children:`Cancel`}),n[40]=o,n[41]=P);let F=!b,I;n[42]!==b||n[43]!==a?(I=()=>{b&&a(b)},n[42]=b,n[43]=a,n[44]=I):I=n[44];let L;n[45]!==F||n[46]!==I?(L=W(yt,{"data-testid":`time-range-calendar-picker-apply-button`,size:`S`,variant:`primary`,isDisabled:F,onPress:I,children:`Apply`}),n[45]=F,n[46]=I,n[47]=L):L=n[47];let R;n[48]!==N||n[49]!==P||n[50]!==L?(R=G(`div`,{className:`time-range-calendar-picker__controls`,children:[N,P,L]}),n[48]=N,n[49]=P,n[50]=L,n[51]=R):R=n[51];let z;return n[52]!==M||n[53]!==R||n[54]!==T?(z=G(`div`,{"data-testid":`time-range-calendar-picker`,className:`time-range-calendar-picker`,css:_d,children:[T,M,R]}),n[52]=M,n[53]=R,n[54]=T,n[55]=z):z=n[55],z}function Sd(e){return W(i,{segment:e})}function Cd(e){return W(i,{segment:e})}var wd=`set_time_range`,Td=[`15m`,`1h`,`12h`,`1d`,`7d`,`30d`,`custom`];function Ed(e){return typeof e==`string`&&Td.includes(e)}function Dd(e){if(typeof e!=`object`||!e)return null;let t=e;return!Ed(t.timeRangeKey)||t.startTime!==void 0&&typeof t.startTime!=`string`||t.endTime!==void 0&&typeof t.endTime!=`string`?null:{timeRangeKey:t.timeRangeKey,...t.startTime===void 0?{}:{startTime:t.startTime},...t.endTime===void 0?{}:{endTime:t.endTime}}}function Od(e,t){return typeof e==`function`?e(t):e}function kd(e){return{name:e.name,uiBehavior:e.uiBehavior,requiredCapabilities:e.requiredCapabilities,dispatch:async t=>{let n=e.parseInput(t.toolCall.input);if(n==null){await t.addToolOutput({state:`output-error`,tool:e.name,toolCallId:t.toolCall.toolCallId,errorText:Od(e.invalidInputErrorText,t.toolCall.input)});return}await e.execute({...t,input:n})}}}async function Ad({toolName:e,toolCall:t,sessionId:n,addToolOutput:r,errorText:i}){return n??(await r({state:`output-error`,tool:e,toolCallId:t.toolCallId,errorText:i}),null)}async function jd({result:e,toolName:t,toolCallId:n,addToolOutput:r,defaultSuccessOutput:i,emitSuccess:a}){if(e.ok){if(!a)return;await r({state:`output-available`,tool:t,toolCallId:n,output:e.output??i});return}await r({state:`output-error`,tool:t,toolCallId:n,errorText:e.error})}function Md(e){let t=e.emitSuccess??!0,n=e.defaultSuccessOutput??`Done.`;return kd({name:e.name,parseInput:e.parseInput,invalidInputErrorText:e.invalidInputErrorText,requiredCapabilities:e.requiredCapabilities,uiBehavior:e.uiBehavior,execute:async({toolCall:r,input:i,sessionId:a,addToolOutput:o,agentStore:s})=>{let c=s.getState().registeredClientActions[e.name];if(!c){await o({state:`output-error`,tool:e.name,toolCallId:r.toolCallId,errorText:e.notMountedErrorText});return}e.requireSession&&await Ad({toolName:e.name,toolCall:r,sessionId:a,addToolOutput:o,errorText:e.noSessionErrorText??`Cannot run this tool without an active session.`})==null||await jd({result:e.buildContext?await c(i,e.buildContext({toolCall:r,sessionId:a,addToolOutput:o,agentStore:s})):await c(i),toolName:e.name,toolCallId:r.toolCallId,addToolOutput:o,defaultSuccessOutput:n,emitSuccess:t})}})}var Nd=Md({name:wd,parseInput:Dd,invalidInputErrorText:`Invalid ${wd} input. Expected { timeRangeKey: ${Td.map(e=>`"${e}"`).join(` | `)}, startTime?: string, endTime?: string }.`,notMountedErrorText:`The app time range selector is not mounted on this page; cannot update the time range.`,defaultSuccessOutput:`Time range updated.`});function Pd(e){switch(e.type){case`app`:return`app`;case`playground`:return`playground`;case`code_evaluator`:return e.evaluatorNodeId?`code_evaluator:${e.evaluatorNodeId}`:`code_evaluator:create`;case`llm_evaluator`:return e.evaluatorNodeId?`llm_evaluator:${e.evaluatorNodeId}`:`llm_evaluator:create`;case`dataset`:return e.datasetVersionNodeId?`dataset:${e.datasetNodeId}:${e.datasetVersionNodeId}`:`dataset:${e.datasetNodeId}`;case`project`:return`project:${e.projectNodeId}`;case`trace`:return`trace:${e.projectNodeId}:${e.otelTraceId}`;case`session`:return`session:${e.projectNodeId}:${e.sessionNodeId}`;case`prompt`:return`prompt:${e.promptNodeId}`;case`prompt_version`:return`prompt_version:${e.promptNodeId}:${e.promptVersionNodeId}`;case`span`:return`span:${e.projectNodeId??``}:${e.spanNodeId?`node:${e.spanNodeId}`:`otel:${e.otelSpanId}`}`;case`graphql`:return`graphql`;case`web_access`:return`web_access`;case`subagents`:return`subagents`;default:return Yn(e)}}var Fd={"bash.retainInactiveSessions":!1,"graphql.mutations":!1,"session.storeSessions":!1,"subagents.enabled":!1,"web.access":!1},Id=[{key:`bash.retainInactiveSessions`,label:`Retain inactive bash sessions`,description:`Keeps browser bash runtimes alive when switching sessions instead of eagerly garbage-collecting them.`,defaultValue:!1,scope:`global`,controlSurface:`experimental-settings`},{key:`graphql.mutations`,label:`Dangerously enable mutations`,description:`Allows the phoenix-gql bash command to execute GraphQL mutations in addition to queries.`,defaultValue:!1,scope:`global`,controlSurface:`experimental-settings`},{key:`session.storeSessions`,label:`Store recent sessions`,description:`Keeps the three most recent chat sessions instead of replacing session history when starting a new chat.`,defaultValue:!1,scope:`global`,controlSurface:`experimental-settings`},{key:`subagents.enabled`,label:`Subagents`,description:`Lets the assistant delegate work to subagents that run their own tool-using turns. Experimental and may consume large numbers of tokens.`,defaultValue:!1,scope:`global`},{key:`web.access`,label:`Web search`,description:`Lets the assistant use provider-native web search and URL fetching when the selected model supports it.`,defaultValue:!1,scope:`global`}],Ld=Object.fromEntries(Id.map(e=>[e.key,e]));for(let e of Object.keys(Fd))if(!Ld[e])throw Error(`Missing AGENT_CAPABILITY_DEFINITIONS entry for capability key: "${e}"`);function Rd(){return{...Fd}}function zd(e){return Ld[e]}function Bd(e){return Id.filter(t=>t.controlSurface===e)}function Vd(e){return e.map(e=>e.toLowerCase())}var Hd=[`NONE`,`MINIMAL`,`LOW`,`MEDIUM`,`HIGH`,`XHIGH`],Ud=Vd(Hd),Wd=Object.fromEntries(Hd.map(e=>[e,e.toLowerCase()]));function Gd(e){return e in Wd}function Kd(e){if(typeof e!=`string`)return;let t=e.trim();if(!t)return;let n=t.toUpperCase();if(Gd(n))return n}function qd(e){let t=Kd(e);if(t!=null)return Wd[t]}var Jd=[`disabled`,`enabled`,`adaptive`],Yd=[`SUMMARIZED`,`OMITTED`],Xd=Vd(Yd),Zd=[`LOW`,`MEDIUM`,`HIGH`,`XHIGH`,`MAX`],Qd=Vd(Zd),$d=[`MINIMAL`,`LOW`,`MEDIUM`,`HIGH`],ef=Vd($d),Q={OPENAI:`openai`,ANTHROPIC:`anthropic`,GOOGLE_GENAI:`google_genai`,AWS_BEDROCK:`aws_bedrock`};function tf(e){switch(e){case`OPENAI`:case`AZURE_OPENAI`:case`DEEPSEEK`:case`XAI`:case`OLLAMA`:case`CEREBRAS`:case`FIREWORKS`:case`GROQ`:case`MOONSHOT`:case`PERPLEXITY`:case`TOGETHER`:return Q.OPENAI;case`ANTHROPIC`:return Q.ANTHROPIC;case`GOOGLE`:return Q.GOOGLE_GENAI;case`AWS`:return Q.AWS_BEDROCK}return Yn(e)}var nf=[{name:`temperature`,type:`float`,min:0,max:2,label:`Temperature`,canonicalName:`TEMPERATURE`},{name:`topP`,type:`float`,min:0,max:1,label:`Top P`,canonicalName:`TOP_P`},{name:`maxCompletionTokens`,type:`int`,label:`Max Completion Tokens`,canonicalName:`MAX_COMPLETION_TOKENS`},{name:`frequencyPenalty`,type:`float`,min:-2,max:2,label:`Frequency Penalty`,applicableOpenAIApiTypes:[`CHAT_COMPLETIONS`]},{name:`presencePenalty`,type:`float`,min:-2,max:2,label:`Presence Penalty`,applicableOpenAIApiTypes:[`CHAT_COMPLETIONS`]},{name:`reasoningEffort`,type:`enum`,values:Ud,label:`Reasoning Effort`,canonicalName:`REASONING_EFFORT`},{name:`seed`,type:`int`,label:`Seed`,canonicalName:`RANDOM_SEED`}],rf=[{name:`maxTokens`,type:`int`,label:`Max Tokens`,required:!0,canonicalName:`MAX_COMPLETION_TOKENS`},{name:`temperature`,type:`float`,min:0,max:1,label:`Temperature`,canonicalName:`TEMPERATURE`},{name:`stopSequences`,type:`string_list`,label:`Stop Sequences`,canonicalName:`STOP_SEQUENCES`},{name:`topP`,type:`float`,min:0,max:1,label:`Top P`,canonicalName:`TOP_P`},{name:`thinkingType`,type:`enum`,values:Jd,label:`Thinking`,canonicalName:`ANTHROPIC_EXTENDED_THINKING`},{name:`thinkingBudgetTokens`,type:`int`,min:1024,label:`Budget Tokens`},{name:`thinkingDisplay`,type:`enum`,values:Xd,label:`Thinking Display`},{name:`effort`,type:`enum`,values:Qd,label:`Effort`,canonicalName:`REASONING_EFFORT`}],af=[{name:`temperature`,type:`float`,min:0,max:2,label:`Temperature`,canonicalName:`TEMPERATURE`},{name:`maxOutputTokens`,type:`int`,label:`Max Output Tokens`,canonicalName:`MAX_COMPLETION_TOKENS`},{name:`stopSequences`,type:`string_list`,label:`Stop Sequences`,canonicalName:`STOP_SEQUENCES`},{name:`presencePenalty`,type:`float`,label:`Presence Penalty`},{name:`frequencyPenalty`,type:`float`,label:`Frequency Penalty`},{name:`topP`,type:`float`,min:0,max:1,label:`Top P`,canonicalName:`TOP_P`},{name:`topK`,type:`int`,label:`Top K`},{name:`thinkingBudget`,type:`int`,min:0,label:`Thinking Budget`},{name:`thinkingLevel`,type:`enum`,values:ef,label:`Thinking Level`},{name:`includeThoughts`,type:`bool`,label:`Include Thoughts`}],of=[{name:`maxTokens`,type:`int`,label:`Max Tokens`,canonicalName:`MAX_COMPLETION_TOKENS`},{name:`temperature`,type:`float`,min:0,max:1,label:`Temperature`,canonicalName:`TEMPERATURE`},{name:`topP`,type:`float`,min:0,max:1,label:`Top P`,canonicalName:`TOP_P`}];Q.OPENAI,Q.ANTHROPIC,Q.GOOGLE_GENAI,Q.AWS_BEDROCK;var sf=1024,cf=2e3,lf={type:`adaptive`,display:`SUMMARIZED`},uf=`HIGH`,df=Y().transform(e=>e.toUpperCase()).pipe(zn(Yd)).optional().catch(void 0),ff=Y().transform(e=>e.toUpperCase()).pipe(zn(Zd)).optional().catch(void 0),pf=Ln(Y()).optional().catch(void 0),mf=Rn(Y(),Wn()).optional().catch(void 0),hf=Vn(`type`,[Bn({type:Un(`disabled`)}),Bn({type:Un(`enabled`),budgetTokens:J(),display:df}),Bn({type:Un(`adaptive`),display:df})]).optional().catch(void 0),gf=Vn(`type`,[Bn({type:Un(`disabled`)}),Bn({type:Un(`enabled`),budget_tokens:J(),display:df}),Bn({type:Un(`adaptive`),display:df})]).optional().catch(void 0);function _f(e){if(e)switch(e.type){case`disabled`:return{type:`disabled`};case`enabled`:{let t={type:`enabled`,budgetTokens:e.budget_tokens};return e.display!==void 0&&(t.display=e.display),t}case`adaptive`:{let t={type:`adaptive`};return e.display!==void 0&&(t.display=e.display),t}default:return Yn(e)}}function vf(e){return e?.type===`enabled`||e?.type===`adaptive`}function yf(){return{maxTokens:cf,thinking:lf,effort:uf}}function bf(e){if(e==null)return rf;let t=vf(e.thinking);return rf.flatMap(n=>{let r=`canonicalName`in n?n.canonicalName:null;return t&&(r===`TEMPERATURE`||r===`TOP_P`)?[]:n.name===`thinkingBudgetTokens`?e.thinking?.type===`enabled`?n.type===`int`?[{...n,max:e.maxTokens-1}]:[n]:[]:n.name===`thinkingDisplay`&&!t?[]:[n]})}var xf=Kn({maxTokens:J().optional().catch(void 0),temperature:J().optional().catch(void 0),topP:J().optional().catch(void 0),stopSequences:pf,thinking:hf,effort:ff,extraBody:mf});function Sf(e){let t=xf.safeParse(e),n=t.success?t.data:{},r={maxTokens:n.maxTokens??2e3};return n.temperature!==void 0&&(r.temperature=n.temperature),n.topP!==void 0&&(r.topP=n.topP),n.stopSequences!==void 0&&(r.stopSequences=[...n.stopSequences]),n.thinking!==void 0&&(r.thinking=n.thinking),n.effort!==void 0&&(r.effort=n.effort),n.extraBody!==void 0&&(r.extraBody={...n.extraBody}),r}function $(e){if(!vf(e.thinking)||e.temperature===void 0&&e.topP===void 0)return e;let t={...e};return delete t.temperature,delete t.topP,t}function Cf(e){let t=[];if(e.thinking?.type===`enabled`){let n=e.thinking.budgetTokens;n<1024&&t.push(`Thinking budget must be at least ${sf} (got ${n})`),n>=e.maxTokens&&t.push(`Thinking budget (${n}) must be less than max tokens (${e.maxTokens})`)}return t}function wf(e){switch(e.type){case`disabled`:return{disabled:{disabled:!0}};case`enabled`:return{enabled:{budgetTokens:e.budgetTokens,display:e.display??null}};case`adaptive`:return{adaptive:{display:e.display??null}};default:return Yn(e)}}function Tf(e){let t=$(e),n=Cf(t);if(n.length>0)throw Error(`Cannot serialize Anthropic invocation parameters: ${n.join(`; `)}`);let r={maxTokens:t.maxTokens};return t.temperature!==void 0&&(r.temperature=t.temperature),t.topP!==void 0&&(r.topP=t.topP),t.stopSequences!==void 0&&(r.stopSequences=t.stopSequences),t.thinking!==void 0&&(r.thinking=wf(t.thinking)),t.effort!==void 0&&(r.outputConfig={effort:t.effort}),t.extraBody!==void 0&&(r.extraBody=t.extraBody),{anthropic:r}}function Ef(e){if(e.__typename!==`PromptAnthropicInvocationParameters`)throw Error(`anthropicAdapter.fromPromptInvocationParameters called with non-Anthropic typename: ${e.__typename}`);let t={maxTokens:e.anthropicMaxTokens};if(e.temperature!=null&&(t.temperature=e.temperature),e.topP!=null&&(t.topP=e.topP),e.stopSequences!=null&&(t.stopSequences=[...e.stopSequences]),e.outputConfig?.effort!=null&&(t.effort=e.outputConfig.effort),e.thinking)switch(e.thinking.__typename){case`PromptAnthropicThinkingDisabled`:t.thinking={type:`disabled`};break;case`PromptAnthropicThinkingEnabled`:{let n={type:`enabled`,budgetTokens:e.thinking.budgetTokens};e.thinking.enabledDisplay!=null&&(n.display=e.thinking.enabledDisplay),t.thinking=n;break}case`PromptAnthropicThinkingAdaptive`:{let n={type:`adaptive`};e.thinking.adaptiveDisplay!=null&&(n.display=e.thinking.adaptiveDisplay),t.thinking=n;break}case`%other`:break;default:Yn(e.thinking)}let n=Nf(e.extraBody);return n!=null&&(t.extraBody=n),$(t)}function Df(e){if(e.__typename!==`PromptAnthropicInvocationParameters`)throw Error(`anthropicAdapter.fromPromptInvocationParametersForDisplay called with non-Anthropic typename: ${e.__typename}`);let t={maxTokens:e.anthropicMaxTokens};if(e.temperature!=null&&(t.temperature=e.temperature),e.topP!=null&&(t.topP=e.topP),e.stopSequences!=null&&(t.stopSequences=[...e.stopSequences]),e.outputConfig?.effort!=null&&(t.outputConfig={effort:e.outputConfig.effort}),e.thinking)switch(e.thinking.__typename){case`PromptAnthropicThinkingDisabled`:t.thinking={type:`disabled`};break;case`PromptAnthropicThinkingEnabled`:{let n={type:`enabled`,budgetTokens:e.thinking.budgetTokens};e.thinking.enabledDisplay!=null&&(n.display=e.thinking.enabledDisplay),t.thinking=n;break}case`PromptAnthropicThinkingAdaptive`:{let n={type:`adaptive`};e.thinking.adaptiveDisplay!=null&&(n.display=e.thinking.adaptiveDisplay),t.thinking=n;break}case`%other`:break;default:Yn(e.thinking)}let n=Nf(e.extraBody);return n!=null&&(t.extraBody=n),t}var Of=Kn({effort:ff,format:Bn({type:Un(`json_schema`),schema:Rn(Y(),Wn())}).optional().catch(void 0)}).optional().catch(void 0),kf=Kn({max_tokens:J().optional().catch(void 0),temperature:J().optional().catch(void 0),top_p:J().optional().catch(void 0),stop_sequences:pf,thinking:gf,output_config:Of,extra_body:mf});function Af(e){let t=kf.safeParse(e),n=t.success?t.data:{},r={maxTokens:n.max_tokens??2e3};n.temperature!==void 0&&(r.temperature=n.temperature),n.top_p!==void 0&&(r.topP=n.top_p),n.stop_sequences!==void 0&&(r.stopSequences=[...n.stop_sequences]);let i=_f(n.thinking);if(i!==void 0&&(r.thinking=i),n.output_config?.effort!==void 0&&(r.effort=n.output_config.effort),n.extra_body!==void 0){let e=Nf(n.extra_body);e!==void 0&&(r.extraBody=e)}let a={},o=n.output_config?.format;return o&&(a.responseFormat={type:`json_schema`,jsonSchema:{name:`response`,schema:o.schema}}),{config:$(r),promoted:a}}function jf(e,t){switch(t){case`maxTokens`:return e.maxTokens;case`temperature`:return e.temperature;case`topP`:return e.topP;case`stopSequences`:return e.stopSequences;case`thinkingType`:return e.thinking?.type;case`thinkingBudgetTokens`:return e.thinking?.type===`enabled`?e.thinking.budgetTokens:void 0;case`thinkingDisplay`:return e.thinking&&e.thinking.type!==`disabled`?e.thinking.display?.toLowerCase():void 0;case`effort`:return e.effort?.toLowerCase();case`extraBody`:return e.extraBody;default:return}}function Mf(e,t,n){switch(t){case`maxTokens`:return typeof n!=`number`||Number.isNaN(n)?e:$({...e,maxTokens:n});case`temperature`:if(n===void 0){let t={...e};return delete t.temperature,$(t)}return typeof n!=`number`||Number.isNaN(n)?e:$({...e,temperature:n});case`topP`:if(n===void 0){let t={...e};return delete t.topP,$(t)}return typeof n!=`number`||Number.isNaN(n)?e:$({...e,topP:n});case`stopSequences`:if(n===void 0){let t={...e};return delete t.stopSequences,$(t)}return Array.isArray(n)?$({...e,stopSequences:n.map(String)}):e;case`thinkingType`:if(n===void 0){let t={...e};return delete t.thinking,$(t)}if(n===`disabled`)return $({...e,thinking:{type:`disabled`}});if(n===`enabled`){let t=e.thinking,n=t?.type===`enabled`?t.budgetTokens:sf,r=t&&t.type!==`disabled`?t.display:void 0,i={type:`enabled`,budgetTokens:n};r!==void 0&&(i.display=r);let a=e.maxTokens>n?e.maxTokens:n+1;return $({...e,maxTokens:a,thinking:i})}if(n===`adaptive`){let t=e.thinking,n=t&&t.type!==`disabled`?t.display:void 0,r={type:`adaptive`};return n!==void 0&&(r.display=n),$({...e,thinking:r})}return e;case`thinkingBudgetTokens`:return e.thinking?.type!==`enabled`||n===void 0||typeof n!=`number`||Number.isNaN(n)?e:$({...e,thinking:{...e.thinking,budgetTokens:n}});case`thinkingDisplay`:{let t=e.thinking;if(!t||t.type===`disabled`)return e;if(n===void 0){if(t.type===`enabled`){let n={type:`enabled`,budgetTokens:t.budgetTokens};return $({...e,thinking:n})}return $({...e,thinking:{type:`adaptive`}})}let r=df.safeParse(n);return!r.success||!r.data?e:t.type===`enabled`?$({...e,thinking:{type:`enabled`,budgetTokens:t.budgetTokens,display:r.data}}):$({...e,thinking:{type:`adaptive`,display:r.data}})}case`effort`:{if(n===void 0){let t={...e};return delete t.effort,$(t)}let t=ff.safeParse(n);return!t.success||!t.data?e:$({...e,effort:t.data})}case`extraBody`:{if(n===void 0){let t={...e};return delete t.extraBody,$(t)}let t=Nf(n);return t===void 0?e:$({...e,extraBody:t})}default:return e}}function Nf(e){if(typeof e==`object`&&e&&!Array.isArray(e))return e}var Pf={getDefaultConfig:yf,getVisibleSpecs:bf,parseConfig:Sf,normalize:$,validateForSubmit:Cf,toPromptInput:Tf,fromPromptInvocationParameters:Ef,fromPromptInvocationParametersForDisplay:Df,fromSpanInvocationParameters:Af,readField:jf,writeField:Mf};function Ff(e){return tr(e)&&!Array.isArray(e)}function If({str:e,excludePrimitives:t=!1,excludeArray:n=!1,excludeNull:r=!1}){try{let i=JSON.parse(e);if(t&&typeof i!=`object`||n&&Array.isArray(i)||r&&i===null)return!1}catch{return!1}return!0}function Lf(e){return If({str:e,excludeArray:!0,excludePrimitives:!0})}function Rf(e){try{return{json:JSON.parse(e)}}catch(e){return{json:null,parseError:e}}}function zf(...e){try{return{json:JSON.stringify(...e)}}catch(e){return{json:null,stringifyError:e}}}function Bf(e){if(typeof e==`string`){let t=Qf(e);return t===void 0?e:Bf(t)}return Array.isArray(e)?e.map(Bf):typeof e==`object`&&e?Object.fromEntries(Object.entries(e).map(([e,t])=>[e,Bf(t)])):e}function Vf(e){return typeof e==`string`?Qf(e)!==void 0:Array.isArray(e)?e.some(Vf):typeof e==`object`&&e?Object.values(e).some(Vf):!1}var Hf=`.`;function Uf({parentKey:e,index:t,indexNotation:n}){return n===`bracket`?`${e}[${t}]`:e?`${e}${Hf}${t}`:String(t)}function Wf({value:e,indexNotation:t=`bracket`,parentKey:n=``}){return Array.isArray(e)&&e.length>0?e.flatMap((e,r)=>Wf({value:e,indexNotation:t,parentKey:Uf({parentKey:n,index:r,indexNotation:t})})):Ff(e)&&Object.keys(e).length>0?Object.entries(e).flatMap(([e,r])=>Wf({value:r,indexNotation:t,parentKey:n?`${n}${Hf}${e}`:e})):n===``?[]:[{key:n,value:e}]}function Gf(e){return typeof e==`string`?e:zf(e).json??String(e)}function Kf({entries:e,query:t}){let n=t.trim().toLowerCase();return n?e.filter(({key:e,value:t})=>e.toLowerCase().includes(n)||Gf(t).toLowerCase().includes(n)):e}function qf({obj:e,parentKey:t=``,separator:n=`.`,keepNonTerminalValues:r=!1,formatIndices:i=!1}){let a={};for(let[o,s]of Object.entries(e)){let c;c=i&&Array.isArray(e)?t?`${t}[${o}]`:`[${o}]`:t?`${t}${n}${o}`:o,s&&typeof s==`object`?(r&&(a[c]=s),Object.assign(a,qf({obj:s,parentKey:c,separator:n,keepNonTerminalValues:r,formatIndices:i}))):a[c]=s}return a}function Jf(e,t=`.`){try{let n=JSON.parse(e);return typeof n==`object`?qf({obj:n,separator:t}):{}}catch{}return{}}function Yf(e,t){let n=t?.unquotePlainString??!1;if(typeof e==`string`){let t=e.startsWith(`"{`)||e.startsWith(`"[`)||e.startsWith(`"\\"`);try{if(t){let t=JSON.parse(e),n=typeof t==`string`?JSON.parse(t):t;return JSON.stringify(n,null,2)}}catch{}return n?e:JSON.stringify(e)}try{let t=JSON.stringify(e,null,2);if(t!==void 0)return t}catch{}return String(e)}function Xf(e){if(e!=null)try{return JSON.stringify(e)}catch{return}}function Zf(e){if(e.trim())try{return JSON.parse(e)}catch{return}}function Qf(e){let t=Zf(e);if(!(typeof t!=`object`||!t))return t}function $f(e){if(e==null)return``;if(Array.isArray(e))return e.length>0?e.map($f):[];if(typeof e==`object`){let t={};for(let n in e)t[n]=$f(e[n]);return t}return typeof e==`string`?``:typeof e==`number`||typeof e==`boolean`?e:``}function ep(e){try{let t=$f(JSON.parse(e));return JSON.stringify(t,null,2)}catch{return`{
  
}`}}function tp(e){if(!tr(e))return{value:e,wasUnnested:!1};let t=Object.keys(e);if(t.length!==1)return{value:e,wasUnnested:!1};let n=e[t[0]];return typeof n==`string`?{value:n,wasUnnested:!0}:{value:e,wasUnnested:!1}}function np(){return{maxTokens:1024,temperature:1}}function rp(){return of}var ip=Kn({maxTokens:J().optional().catch(void 0),temperature:J().optional().catch(void 0),topP:J().optional().catch(void 0),stopSequences:Ln(Y()).optional().catch(void 0)});function ap(e){let t=ip.safeParse(e),n=t.success?t.data:{},r={};return n.maxTokens!==void 0&&(r.maxTokens=n.maxTokens),n.temperature!==void 0&&(r.temperature=n.temperature),n.topP!==void 0&&(r.topP=n.topP),n.stopSequences!==void 0&&(r.stopSequences=[...n.stopSequences]),r}function op(e){return e}function sp(e){return[]}function cp(e){let t=op(e),n={};return t.maxTokens!==void 0&&(n.maxTokens=t.maxTokens),t.temperature!==void 0&&(n.temperature=t.temperature),t.topP!==void 0&&(n.topP=t.topP),t.stopSequences!==void 0&&(n.stopSequences=t.stopSequences),{aws:n}}function lp(e){if(e.__typename!==`PromptAwsInvocationParameters`)throw Error(`awsAdapter.fromPromptInvocationParameters called with non-AWS typename: ${e.__typename}`);let t={};return e.awsMaxTokens!=null&&(t.maxTokens=e.awsMaxTokens),e.temperature!=null&&(t.temperature=e.temperature),e.topP!=null&&(t.topP=e.topP),e.stopSequences!=null&&(t.stopSequences=[...e.stopSequences]),op(t)}function up(e){if(e.__typename!==`PromptAwsInvocationParameters`)throw Error(`awsAdapter.fromPromptInvocationParametersForDisplay called with non-AWS typename: ${e.__typename}`);let t={};return e.awsMaxTokens!=null&&(t.maxTokens=e.awsMaxTokens),e.temperature!=null&&(t.temperature=e.temperature),e.topP!=null&&(t.topP=e.topP),e.stopSequences!=null&&(t.stopSequences=[...e.stopSequences]),t}var dp=Bn({maxTokens:J().optional().catch(void 0),temperature:J().optional().catch(void 0),topP:J().optional().catch(void 0),stopSequences:Ln(Y()).optional().catch(void 0)}).optional().catch(void 0),fp=Bn({textFormat:Bn({structure:Bn({jsonSchema:Bn({schema:Hn([Y(),Rn(Y(),Wn())]).optional(),name:Y().optional(),description:Y().optional()}).optional().catch(void 0)}).optional().catch(void 0)}).optional().catch(void 0)}).optional().catch(void 0),pp=Kn({maxTokens:J().optional().catch(void 0),temperature:J().optional().catch(void 0),topP:J().optional().catch(void 0),stopSequences:Ln(Y()).optional().catch(void 0),inferenceConfig:dp,outputConfig:fp});function mp(e){let t=pp.safeParse(e),n=t.success?t.data:{},r={};n.maxTokens===void 0?n.inferenceConfig?.maxTokens!==void 0&&(r.maxTokens=n.inferenceConfig.maxTokens):r.maxTokens=n.maxTokens,n.temperature===void 0?n.inferenceConfig?.temperature!==void 0&&(r.temperature=n.inferenceConfig.temperature):r.temperature=n.temperature,n.topP===void 0?n.inferenceConfig?.topP!==void 0&&(r.topP=n.inferenceConfig.topP):r.topP=n.topP,n.stopSequences===void 0?n.inferenceConfig?.stopSequences!==void 0&&(r.stopSequences=[...n.inferenceConfig.stopSequences]):r.stopSequences=[...n.stopSequences];let i={},a=n.outputConfig?.textFormat?.structure?.jsonSchema;if(a?.schema!=null){let e=null;if(typeof a.schema==`string`){let{json:t}=Rf(a.schema);typeof t==`object`&&t&&!Array.isArray(t)&&(e=t)}else typeof a.schema==`object`&&!Array.isArray(a.schema)&&(e=a.schema);if(e!=null){let t={name:typeof a.name==`string`?a.name:`response`,schema:e};typeof a.description==`string`&&(t.description=a.description),i.responseFormat={type:`json_schema`,jsonSchema:t}}}return{config:op(r),promoted:i}}function hp(e,t){switch(t){case`maxTokens`:return e.maxTokens;case`temperature`:return e.temperature;case`topP`:return e.topP;case`stopSequences`:return e.stopSequences;default:return}}function gp(e,t,n){switch(t){case`maxTokens`:case`temperature`:case`topP`:if(n===void 0){let n={...e};return delete n[t],op(n)}return typeof n!=`number`||Number.isNaN(n)?e:op({...e,[t]:n});case`stopSequences`:if(n===void 0){let t={...e};return delete t.stopSequences,op(t)}return Array.isArray(n)?op({...e,stopSequences:n.map(String)}):e;default:return e}}var _p={getDefaultConfig:np,getVisibleSpecs:rp,parseConfig:ap,normalize:op,validateForSubmit:sp,toPromptInput:cp,fromPromptInvocationParameters:lp,fromPromptInvocationParametersForDisplay:up,fromSpanInvocationParameters:e=>mp(e),readField:hp,writeField:gp};function vp(){return{temperature:1,presencePenalty:0,frequencyPenalty:0,thinkingConfig:{thinkingLevel:`MEDIUM`,includeThoughts:!0}}}function yp(){return af}var bp=Y().transform(e=>e.toUpperCase()).pipe(zn($d)).optional().catch(void 0),xp=Kn({thinkingBudget:J().optional().catch(void 0),thinkingLevel:bp,includeThoughts:qn().optional().catch(void 0)}).optional().catch(void 0),Sp=Kn({temperature:J().optional().catch(void 0),maxOutputTokens:J().optional().catch(void 0),stopSequences:Ln(Y()).optional().catch(void 0),presencePenalty:J().optional().catch(void 0),frequencyPenalty:J().optional().catch(void 0),topP:J().optional().catch(void 0),topK:J().optional().catch(void 0),thinkingConfig:xp});function Cp(e){let t=Sp.safeParse(e),n=t.success?t.data:{},r={};return n.temperature!==void 0&&(r.temperature=n.temperature),n.maxOutputTokens!==void 0&&(r.maxOutputTokens=n.maxOutputTokens),n.stopSequences!==void 0&&(r.stopSequences=[...n.stopSequences]),n.presencePenalty!==void 0&&(r.presencePenalty=n.presencePenalty),n.frequencyPenalty!==void 0&&(r.frequencyPenalty=n.frequencyPenalty),n.topP!==void 0&&(r.topP=n.topP),n.topK!==void 0&&(r.topK=n.topK),n.thinkingConfig!==void 0&&n.thinkingConfig!==null&&(r.thinkingConfig=wp(n.thinkingConfig)),r}function wp(e){let t={};return e.thinkingBudget!==void 0&&(t.thinkingBudget=e.thinkingBudget),e.thinkingLevel!==void 0&&(t.thinkingLevel=e.thinkingLevel),e.includeThoughts!==void 0&&(t.includeThoughts=e.includeThoughts),t}function Tp(e){return e}function Ep(e){return[]}function Dp(e){let t={};return e.thinkingBudget!==void 0&&(t.thinkingBudget=e.thinkingBudget),e.thinkingLevel!==void 0&&(t.thinkingLevel=e.thinkingLevel),e.includeThoughts!==void 0&&(t.includeThoughts=e.includeThoughts),Object.keys(t).length>0?t:void 0}function Op(e){let t=Tp(e),n={};if(t.temperature!==void 0&&(n.temperature=t.temperature),t.maxOutputTokens!==void 0&&(n.maxOutputTokens=t.maxOutputTokens),t.stopSequences!==void 0&&(n.stopSequences=t.stopSequences),t.presencePenalty!==void 0&&(n.presencePenalty=t.presencePenalty),t.frequencyPenalty!==void 0&&(n.frequencyPenalty=t.frequencyPenalty),t.topP!==void 0&&(n.topP=t.topP),t.topK!==void 0&&(n.topK=t.topK),t.thinkingConfig!==void 0){let e=Dp(t.thinkingConfig);e&&(n.thinkingConfig=e)}return{google:n}}function kp(e){if(e.__typename!==`PromptGoogleInvocationParameters`)throw Error(`googleAdapter.fromPromptInvocationParameters called with non-Google typename: ${e.__typename}`);let t={};if(e.temperature!=null&&(t.temperature=e.temperature),e.maxOutputTokens!=null&&(t.maxOutputTokens=e.maxOutputTokens),e.stopSequences!=null&&(t.stopSequences=[...e.stopSequences]),e.presencePenalty!=null&&(t.presencePenalty=e.presencePenalty),e.frequencyPenalty!=null&&(t.frequencyPenalty=e.frequencyPenalty),e.topP!=null&&(t.topP=e.topP),e.topK!=null&&(t.topK=e.topK),e.thinkingConfig){let n={};e.thinkingConfig.thinkingBudget!=null&&(n.thinkingBudget=e.thinkingConfig.thinkingBudget),e.thinkingConfig.thinkingLevel!=null&&(n.thinkingLevel=e.thinkingConfig.thinkingLevel),e.thinkingConfig.includeThoughts!=null&&(n.includeThoughts=e.thinkingConfig.includeThoughts),Object.keys(n).length>0&&(t.thinkingConfig=n)}return Tp(t)}function Ap(e){if(e.__typename!==`PromptGoogleInvocationParameters`)throw Error(`googleAdapter.fromPromptInvocationParametersForDisplay called with non-Google typename: ${e.__typename}`);let t={};if(e.temperature!=null&&(t.temperature=e.temperature),e.maxOutputTokens!=null&&(t.maxOutputTokens=e.maxOutputTokens),e.stopSequences!=null&&(t.stopSequences=[...e.stopSequences]),e.presencePenalty!=null&&(t.presencePenalty=e.presencePenalty),e.frequencyPenalty!=null&&(t.frequencyPenalty=e.frequencyPenalty),e.topP!=null&&(t.topP=e.topP),e.topK!=null&&(t.topK=e.topK),e.thinkingConfig){let n={};e.thinkingConfig.thinkingBudget!=null&&(n.thinkingBudget=e.thinkingConfig.thinkingBudget),e.thinkingConfig.thinkingLevel!=null&&(n.thinkingLevel=e.thinkingConfig.thinkingLevel),e.thinkingConfig.includeThoughts!=null&&(n.includeThoughts=e.thinkingConfig.includeThoughts),Object.keys(n).length>0&&(t.thinkingConfig=n)}return t}var jp=Kn({thinking_budget:J().optional().catch(void 0),thinking_level:bp,include_thoughts:qn().optional().catch(void 0)}).optional().catch(void 0),Mp=Kn({temperature:J().optional().catch(void 0),max_output_tokens:J().optional().catch(void 0),stop_sequences:Ln(Y()).optional().catch(void 0),presence_penalty:J().optional().catch(void 0),frequency_penalty:J().optional().catch(void 0),top_p:J().optional().catch(void 0),top_k:J().optional().catch(void 0),thinking_config:jp,response_json_schema:Wn().optional(),response_schema:Wn().optional(),response_mime_type:Y().optional().catch(void 0)});function Np(e){let t=Mp.safeParse(e),n=t.success?t.data:{},r={};if(n.temperature!==void 0&&(r.temperature=n.temperature),n.max_output_tokens!==void 0&&(r.maxOutputTokens=n.max_output_tokens),n.stop_sequences!==void 0&&(r.stopSequences=[...n.stop_sequences]),n.presence_penalty!==void 0&&(r.presencePenalty=n.presence_penalty),n.frequency_penalty!==void 0&&(r.frequencyPenalty=n.frequency_penalty),n.top_p!==void 0&&(r.topP=n.top_p),n.top_k!==void 0&&(r.topK=n.top_k),n.thinking_config){let e={};n.thinking_config.thinking_budget!==void 0&&(e.thinkingBudget=n.thinking_config.thinking_budget),n.thinking_config.thinking_level!==void 0&&(e.thinkingLevel=n.thinking_config.thinking_level),n.thinking_config.include_thoughts!==void 0&&(e.includeThoughts=n.thinking_config.include_thoughts),Object.keys(e).length>0&&(r.thinkingConfig=e)}let i={},a=n.response_json_schema??n.response_schema;return a!=null&&n.response_mime_type===`application/json`&&(i.responseFormat={type:`json_schema`,jsonSchema:{name:`response`,schema:a}}),{config:Tp(r),promoted:i}}var Pp=new Set([`temperature`,`maxOutputTokens`,`presencePenalty`,`frequencyPenalty`,`topP`,`topK`]);function Fp(e){return Pp.has(e)}function Ip(e){let t={};return e.thinkingBudget!==void 0&&(t.thinkingBudget=e.thinkingBudget),e.thinkingLevel!==void 0&&(t.thinkingLevel=e.thinkingLevel),e.includeThoughts!==void 0&&(t.includeThoughts=e.includeThoughts),Object.keys(t).length===0?void 0:t}function Lp(e,t){if(Fp(t))return e[t];switch(t){case`stopSequences`:return e.stopSequences;case`thinkingBudget`:return e.thinkingConfig?.thinkingBudget;case`thinkingLevel`:return e.thinkingConfig?.thinkingLevel?.toLowerCase();case`includeThoughts`:return e.thinkingConfig?.includeThoughts;default:return}}function Rp(e,t,n){if(Fp(t)){if(n===void 0){let n={...e};return delete n[t],Tp(n)}return typeof n!=`number`||Number.isNaN(n)?e:Tp({...e,[t]:n})}switch(t){case`stopSequences`:if(n===void 0){let t={...e};return delete t.stopSequences,Tp(t)}return Array.isArray(n)?Tp({...e,stopSequences:n.map(String)}):e;case`thinkingBudget`:{let t={...e.thinkingConfig??{}};if(n===void 0)delete t.thinkingBudget;else if(typeof n==`number`&&!Number.isNaN(n))t.thinkingBudget=n;else return e;return zp(e,t)}case`thinkingLevel`:{let t={...e.thinkingConfig??{}};if(n===void 0)delete t.thinkingLevel;else{let r=bp.safeParse(n);if(!r.success||!r.data)return e;t.thinkingLevel=r.data}return zp(e,t)}case`includeThoughts`:{let t={...e.thinkingConfig??{}};if(n===void 0)delete t.includeThoughts;else if(typeof n==`boolean`)t.includeThoughts=n;else return e;return zp(e,t)}default:return e}}function zp(e,t){let n=Ip(t),r={...e};return n===void 0?delete r.thinkingConfig:r.thinkingConfig=n,Tp(r)}var Bp={getDefaultConfig:vp,getVisibleSpecs:yp,parseConfig:Cp,normalize:Tp,validateForSubmit:Ep,toPromptInput:Op,fromPromptInvocationParameters:kp,fromPromptInvocationParametersForDisplay:Ap,fromSpanInvocationParameters:e=>Np(e),readField:Lp,writeField:Rp};function Vp(e){if(typeof e==`object`&&e&&!Array.isArray(e))return e}function Hp(e){return e===0?void 0:e}function Up(){return{frequencyPenalty:0,presencePenalty:0}}function Wp(e,t){let n=t.openaiApiType??`RESPONSES`;return nf.filter(e=>{let t=`applicableOpenAIApiTypes`in e?e.applicableOpenAIApiTypes:void 0;return t==null||t.includes(n)})}var Gp=Kn({temperature:J().optional().catch(void 0),topP:J().optional().catch(void 0),maxCompletionTokens:J().optional().catch(void 0),frequencyPenalty:J().optional().catch(void 0),presencePenalty:J().optional().catch(void 0),reasoningEffort:Y().optional().catch(void 0),seed:J().optional().catch(void 0),stop:Ln(Y()).optional().catch(void 0),extraBody:Rn(Y(),Wn()).optional().catch(void 0)});function Kp(e){let t=Gp.safeParse(e),n=t.success?t.data:{},r={};if(n.temperature!==void 0&&(r.temperature=n.temperature),n.topP!==void 0&&(r.topP=n.topP),n.maxCompletionTokens!==void 0&&(r.maxCompletionTokens=n.maxCompletionTokens),n.frequencyPenalty!==void 0&&(r.frequencyPenalty=n.frequencyPenalty),n.presencePenalty!==void 0&&(r.presencePenalty=n.presencePenalty),n.reasoningEffort!==void 0){let e=qd(n.reasoningEffort);e!==void 0&&(r.reasoningEffort=e)}return n.seed!==void 0&&(r.seed=n.seed),n.stop!==void 0&&(r.stop=[...n.stop]),n.extraBody!==void 0&&(r.extraBody={...n.extraBody}),r}function qp(e){return e}function Jp(e){return[]}function Yp(e){let t=qp(e),n={};t.temperature!==void 0&&(n.temperature=t.temperature),t.topP!==void 0&&(n.topP=t.topP),t.maxCompletionTokens!==void 0&&(n.maxCompletionTokens=t.maxCompletionTokens);let r=Hp(t.frequencyPenalty);r!==void 0&&(n.frequencyPenalty=r);let i=Hp(t.presencePenalty);if(i!==void 0&&(n.presencePenalty=i),t.reasoningEffort!==void 0){let e=Kd(t.reasoningEffort);e!==void 0&&(n.reasoningEffort=e)}return t.seed!==void 0&&(n.seed=t.seed),t.stop!==void 0&&(n.stop=t.stop),t.extraBody!==void 0&&(n.extraBody=t.extraBody),{openai:n}}function Xp(e){if(e.__typename!==`PromptOpenAIInvocationParameters`)throw Error(`openaiAdapter.fromPromptInvocationParameters called with non-OpenAI typename: ${e.__typename}`);let t={};if(e.temperature!=null&&(t.temperature=e.temperature),e.topP!=null&&(t.topP=e.topP),e.maxCompletionTokens==null?e.openaiMaxTokens!=null&&(t.maxCompletionTokens=e.openaiMaxTokens):t.maxCompletionTokens=e.maxCompletionTokens,e.frequencyPenalty!=null&&(t.frequencyPenalty=e.frequencyPenalty),e.presencePenalty!=null&&(t.presencePenalty=e.presencePenalty),e.seed!=null&&(t.seed=e.seed),e.stop!=null&&(t.stop=[...e.stop]),e.reasoningEffort!=null){let n=qd(e.reasoningEffort);n!==void 0&&(t.reasoningEffort=n)}let n=Vp(e.extraBody);return n!=null&&(t.extraBody=n),qp(t)}function Zp(e){if(e.__typename!==`PromptOpenAIInvocationParameters`)throw Error(`openaiAdapter.fromPromptInvocationParametersForDisplay called with non-OpenAI typename: ${e.__typename}`);let t={};e.temperature!=null&&(t.temperature=e.temperature),e.openaiMaxTokens!=null&&(t.maxTokens=e.openaiMaxTokens),e.maxCompletionTokens!=null&&(t.maxCompletionTokens=e.maxCompletionTokens),e.frequencyPenalty!=null&&(t.frequencyPenalty=e.frequencyPenalty),e.presencePenalty!=null&&(t.presencePenalty=e.presencePenalty),e.topP!=null&&(t.topP=e.topP),e.seed!=null&&(t.seed=e.seed),e.stop!=null&&(t.stop=[...e.stop]);let n=qd(e.reasoningEffort);n!==void 0&&(t.reasoningEffort=n);let r=Vp(e.extraBody);return r!=null&&(t.extraBody=r),t}var Qp=Bn({name:Y().optional(),schema:Wn().optional(),strict:qn().nullish(),description:Y().nullish()}),$p=Bn({type:Y().optional(),json_schema:Qp.optional()}).optional().catch(void 0),em=Bn({type:Y().optional(),name:Y().optional(),schema:Wn().optional(),strict:qn().optional(),description:Y().optional()}).optional().catch(void 0),tm=Kn({temperature:J().optional().catch(void 0),top_p:J().optional().catch(void 0),max_completion_tokens:J().optional().catch(void 0),max_tokens:J().optional().catch(void 0),max_output_tokens:J().optional().catch(void 0),frequency_penalty:J().optional().catch(void 0),presence_penalty:J().optional().catch(void 0),seed:J().optional().catch(void 0),stop:Ln(Y()).optional().catch(void 0),reasoning_effort:Y().optional().catch(void 0),reasoning:Kn({effort:Y().optional().catch(void 0)}).optional().catch(void 0),response_format:$p,text:Bn({format:em}).optional().catch(void 0),extra_body:Rn(Y(),Wn()).optional().catch(void 0)});function nm(e,t){let n=tm.safeParse(e),r=n.success?n.data:{},i={};r.temperature!==void 0&&(i.temperature=r.temperature),r.top_p!==void 0&&(i.topP=r.top_p),r.max_completion_tokens===void 0?r.max_tokens===void 0?t===`RESPONSES`&&r.max_output_tokens!==void 0&&(i.maxCompletionTokens=r.max_output_tokens):i.maxCompletionTokens=r.max_tokens:i.maxCompletionTokens=r.max_completion_tokens,r.frequency_penalty!==void 0&&(i.frequencyPenalty=r.frequency_penalty),r.presence_penalty!==void 0&&(i.presencePenalty=r.presence_penalty),r.seed!==void 0&&(i.seed=r.seed),r.stop!==void 0&&(i.stop=[...r.stop]);let a;if(r.reasoning_effort===void 0?t===`RESPONSES`&&r.reasoning?.effort!==void 0&&(a=r.reasoning.effort):a=r.reasoning_effort,a!==void 0){let e=qd(a);e!==void 0&&(i.reasoningEffort=e)}r.extra_body!==void 0&&(i.extraBody={...r.extra_body});let o={},s=r.response_format;if(s?.json_schema){let e=s.json_schema,t={name:typeof e.name==`string`?e.name:`response`};e.schema!==void 0&&(t.schema=e.schema),e.strict!==void 0&&e.strict!==null&&(t.strict=e.strict),e.description!==void 0&&e.description!==null&&(t.description=e.description),o.responseFormat={type:`json_schema`,jsonSchema:t}}else if(r.text?.format!==void 0){let e=r.text.format;if(e){let t={name:typeof e.name==`string`?e.name:`response`};e.schema!==void 0&&(t.schema=e.schema),e.strict!==void 0&&(t.strict=e.strict),e.description!==void 0&&(t.description=e.description),o.responseFormat={type:`json_schema`,jsonSchema:t}}}return{config:qp(i),promoted:o}}var rm=new Set([`temperature`,`topP`,`maxCompletionTokens`,`frequencyPenalty`,`presencePenalty`,`seed`]);function im(e){return rm.has(e)}function am(e,t){if(im(t))return e[t];switch(t){case`reasoningEffort`:return e.reasoningEffort;case`stop`:return e.stop;case`extraBody`:return e.extraBody;default:return}}function om(e,t,n){if(im(t)){if(n===void 0){let n={...e};return delete n[t],qp(n)}return typeof n!=`number`||Number.isNaN(n)?e:qp({...e,[t]:n})}switch(t){case`reasoningEffort`:if(n===void 0){let t={...e};return delete t.reasoningEffort,qp(t)}return typeof n==`string`?qp({...e,reasoningEffort:n}):e;case`stop`:if(n===void 0){let t={...e};return delete t.stop,qp(t)}return Array.isArray(n)?qp({...e,stop:n.map(String)}):e;case`extraBody`:{if(n===void 0){let t={...e};return delete t.extraBody,qp(t)}let t=Vp(n);return t===void 0?e:qp({...e,extraBody:t})}default:return e}}var sm={getDefaultConfig:Up,getVisibleSpecs:Wp,parseConfig:Kp,normalize:qp,validateForSubmit:Jp,toPromptInput:Yp,fromPromptInvocationParameters:Xp,fromPromptInvocationParametersForDisplay:Zp,fromSpanInvocationParameters:(e,t)=>nm(e,t?.openaiApiType??null),readField:am,writeField:om};function cm(e){switch(e){case Q.OPENAI:return sm;case Q.ANTHROPIC:return Pf;case Q.GOOGLE_GENAI:return Bp;case Q.AWS_BEDROCK:return _p;default:return Yn(e)}}function lm(e){return cm(tf(e))}function um(e){let t=lm(e);return t.normalize(t.getDefaultConfig())}function dm(e,t){let n=lm(e);return n.normalize(n.parseConfig(t))}function fm(e,t){return lm(e).toPromptInput(t)}function pm(e,t){if(t==null)return um(e);let n=tf(e);return n===Q.OPENAI&&t.__typename===`PromptOpenAIInvocationParameters`||n===Q.ANTHROPIC&&t.__typename===`PromptAnthropicInvocationParameters`||n===Q.GOOGLE_GENAI&&t.__typename===`PromptGoogleInvocationParameters`||n===Q.AWS_BEDROCK&&t.__typename===`PromptAwsInvocationParameters`?lm(e).fromPromptInvocationParameters(t):um(e)}function mm(e){if(e==null)return null;let t;switch(e.__typename){case`PromptOpenAIInvocationParameters`:t=Q.OPENAI;break;case`PromptAnthropicInvocationParameters`:t=Q.ANTHROPIC;break;case`PromptGoogleInvocationParameters`:t=Q.GOOGLE_GENAI;break;case`PromptAwsInvocationParameters`:t=Q.AWS_BEDROCK;break;case`%other`:throw Error(`Unsupported prompt invocation parameters typename: %other`);default:return Yn(e)}let n=cm(t);return{family:t,parameters:n.fromPromptInvocationParametersForDisplay(e)}}function hm(e,t,n={}){let{config:r,promoted:i}=lm(e).fromSpanInvocationParameters(t,n);return{invocationParameters:r,responseFormat:i.responseFormat}}function gm(e,t,n){return lm(e).readField(t,n)}function _m(e,t){return lm(e.provider).getVisibleSpecs(t,{openaiApiType:e.openaiApiType})}function vm(e,t,n,r){return lm(e).writeField(t,n,r)}function ym(){if(typeof crypto<`u`&&typeof crypto.randomUUID==`function`)return crypto.randomUUID();let e=new Uint8Array(16);crypto.getRandomValues(e),e[6]=e[6]&15|64,e[8]=e[8]&63|128;let t=Array.from(e).map(e=>e.toString(16).padStart(2,`0`)).join(``);return`${t.slice(0,8)}-${t.slice(8,12)}-${t.slice(12,16)}-${t.slice(16,20)}-${t.slice(20)}`}var bm={provider:`ANTHROPIC`,modelName:`claude-opus-4-6`,invocationParameters:um(`ANTHROPIC`)},xm={collectorEndpoint:null,assistantProjectName:`assistant_agent`,forceTracing:!1,webAccessEnabled:!1,assistantEnabled:!1,allowLocalTraces:!1,allowRemoteExport:!1},Sm={storeLocalTraces:!0,exportRemoteTraces:!1,attachUserId:!1,acknowledgedTraceConsent:null},Cm={edits:`manual`},wm=`(branch) `,Tm=50;function Em(e){let t=e.shortSummary.trim();if(!t){let n=e.messages.find(e=>e.role===`user`)?.parts.filter(Gn).map(e=>e.text).join(` `).trim();t=n?n.length>Tm?`${n.slice(0,Tm)}...`:n:``}return t.startsWith(wm)?t:t?`${wm}${t}`:wm.trim()}function Dm(e){return{allowLocalTraces:e.allowLocalTraces,allowRemoteExport:!!e.collectorEndpoint&&e.allowRemoteExport}}function Om({agentsConfig:e,observability:t}){if(e.forceTracing)return!0;let n=t.acknowledgedTraceConsent;if(!n)return!1;let r=Dm(e);return(!r.allowLocalTraces||n.allowLocalTraces)&&(!r.allowRemoteExport||n.allowRemoteExport)}function km({agentsConfig:e,observability:t}){if(e.forceTracing)return{ingestTraces:!0,exportRemoteTraces:!0};let n=Dm(e);return{ingestTraces:n.allowLocalTraces&&t.storeLocalTraces,exportRemoteTraces:n.allowRemoteExport&&t.exportRemoteTraces}}function Am({agentsConfig:e,observability:t}){return e.forceTracing||t.attachUserId}function jm({capabilities:e,defaultCapabilities:t=Rd()}){if(!e||typeof e!=`object`)return{...t};let n=e;return Object.fromEntries(Object.keys(t).map(e=>{let r=n[e];return[e,typeof r==`boolean`?r:t[e]]}))}function Mm(e,t){if(!e||typeof e!=`object`)return t;let n=e;return{...t,...n,observability:{...t.observability,...n.observability},capabilities:jm({capabilities:n.capabilities,defaultCapabilities:t.capabilities})}}function Nm({record:e,retainedSessionIds:t}){return Object.fromEntries(Object.entries(e).filter(([e])=>t.has(e)))}function Pm({record:e,retainedSessionIds:t}){return Object.fromEntries(Object.entries(e).filter(([,e])=>e!=null&&t.has(e.sessionId)))}function Fm(e,t){return Object.fromEntries(Object.entries(e).filter(([,e])=>e?.sessionId!==t))}function Im({state:e,retainedSessionIds:t,activeSessionId:n}){let r=new Set(t);return{sessions:t,activeSessionId:n,sessionMap:Nm({record:e.sessionMap,retainedSessionIds:r}),pendingElicitationBySessionId:Nm({record:e.pendingElicitationBySessionId,retainedSessionIds:r}),chatStatusBySessionId:Nm({record:e.chatStatusBySessionId,retainedSessionIds:r}),isResponsePendingBySessionId:Nm({record:e.isResponsePendingBySessionId,retainedSessionIds:r}),draftInputBySessionId:Nm({record:e.draftInputBySessionId,retainedSessionIds:r}),pendingMessageBySessionId:Nm({record:e.pendingMessageBySessionId,retainedSessionIds:r}),pendingPatchExperimentsByToolCallId:Pm({record:e.pendingPatchExperimentsByToolCallId,retainedSessionIds:r})}}var Lm=`arize-phoenix-assistant`;function Rm(){let e=(window.Config?.basename??``).replace(/\/+$/,``);return e?`${Lm}:${e}`:Lm}var zm=e=>C()(u(T((t,n)=>({isOpen:!1,position:`pinned`,fabMode:`pinned`,fabPlacement:`bottom-end`,sessions:[],activeSessionId:null,sessionMap:{},defaultModelConfig:{...bm},agentsConfig:xm,observability:Sm,permissions:Cm,capabilities:Rd(),routeContexts:[],mountedContexts:{},pendingPromptEditsByToolCallId:{},pendingPromptInstanceRemovalsByToolCallId:{},pendingBatchSpanAnnotatesByToolCallId:{},pendingDatasetWritesByToolCallId:{},pendingAnnotationConfigWritesByToolCallId:{},pendingPatchExperimentsByToolCallId:{},pendingPromptToolWritesByToolCallId:{},pendingSavePromptsByToolCallId:{},pendingCodeEvaluatorEditsByToolCallId:{},pendingLlmEvaluatorEditsByToolCallId:{},pendingLoadDatasetsByToolCallId:{},setIsOpen:e=>{t({isOpen:e},!1,{type:`setIsOpen`})},toggleOpen:()=>{t(e=>({isOpen:!e.isOpen}),!1,{type:`toggleOpen`})},setPosition:e=>{t({position:e},!1,{type:`setPosition`})},setFabMode:e=>{t({fabMode:e},!1,{type:`setFabMode`})},setFabPlacement:e=>{t({fabPlacement:e},!1,{type:`setFabPlacement`})},createSession:()=>{let e=ym();return t(t=>{let n={id:e,shortSummary:``,messages:[],context:[],modelConfig:{...t.defaultModelConfig},createdAt:Date.now()},r;return r=t.capabilities[`session.storeSessions`]?[...t.sessions,e].slice(-3):[e],{...Im({state:{...t,sessionMap:{...t.sessionMap,[e]:n}},retainedSessionIds:r,activeSessionId:e})}},!1,{type:`createSession`}),e},forkSession:({sourceSessionId:e,messages:n,restoredInput:r})=>{let i=ym(),a=!1;return t(t=>{let o=t.sessionMap[e];if(!o)return t;a=!0;let s={id:i,shortSummary:Em(o),messages:n,context:[...o.context],modelConfig:{...o.modelConfig},createdAt:Date.now()},c=[...t.sessions,i].slice(-3),l=r?{...t.draftInputBySessionId,[i]:r}:t.draftInputBySessionId;return{...Im({state:{...t,sessionMap:{...t.sessionMap,[i]:s},draftInputBySessionId:l},retainedSessionIds:c,activeSessionId:i})}},!1,{type:`forkSession`}),a?i:null},deleteSession:e=>{t(t=>{if(!t.sessionMap[e])return t;let n={...t.sessionMap};delete n[e];let r={...t.pendingElicitationBySessionId};delete r[e];let i={...t.chatStatusBySessionId};delete i[e];let a={...t.isResponsePendingBySessionId};delete a[e];let o={...t.draftInputBySessionId};delete o[e];let s={...t.pendingMessageBySessionId};delete s[e];let c=Fm(t.pendingPatchExperimentsByToolCallId,e),l=t.sessions.filter(t=>t!==e);return{sessions:l,sessionMap:n,activeSessionId:t.activeSessionId===e?l[l.length-1]??null:t.activeSessionId,pendingElicitationBySessionId:r,chatStatusBySessionId:i,isResponsePendingBySessionId:a,draftInputBySessionId:o,pendingMessageBySessionId:s,pendingPatchExperimentsByToolCallId:c}},!1,{type:`deleteSession`})},setActiveSession:e=>{t({activeSessionId:e},!1,{type:`setActiveSession`})},updateSessionSummary:(e,n)=>{t(t=>{let r=t.sessionMap[e];return r?{sessionMap:{...t.sessionMap,[e]:{...r,shortSummary:n}}}:t},!1,{type:`updateSessionSummary`})},updateSessionModelConfig:(e,n)=>{t(t=>{let r=t.sessionMap[e];return r?{sessionMap:{...t.sessionMap,[e]:{...r,modelConfig:{...r.modelConfig,...n}}}}:t},!1,{type:`updateSessionModelConfig`})},addSessionContext:(e,n)=>{t(t=>{let r=t.sessionMap[e];return r?{sessionMap:{...t.sessionMap,[e]:{...r,context:[...r.context,n]}}}:t},!1,{type:`addSessionContext`})},removeSessionContext:(e,n)=>{t(t=>{let r=t.sessionMap[e];return r?{sessionMap:{...t.sessionMap,[e]:{...r,context:r.context.filter(e=>e!==n)}}}:t},!1,{type:`removeSessionContext`})},setSessionMessages:(e,n)=>{t(t=>{let r=t.sessionMap[e];return r?{sessionMap:{...t.sessionMap,[e]:{...r,messages:n}}}:t},!1,{type:`setSessionMessages`})},setDefaultModelConfig:e=>{t({defaultModelConfig:e},!1,{type:`setDefaultModelConfig`})},setObservability:e=>{t(t=>({observability:{...t.observability,...e}}),!1,{type:`setObservability`})},setPermissions:e=>{t(t=>({permissions:{...t.permissions,...e}}),!1,{type:`setPermissions`})},setAgentsConfig:e=>{t(t=>({agentsConfig:{...t.agentsConfig,...e}}),!1,{type:`setAgentsConfig`})},acknowledgeConsent:()=>{t(e=>({observability:{...e.observability,acknowledgedTraceConsent:Dm(e.agentsConfig)}}),!1,{type:`acknowledgeConsent`})},clearAllSessions:()=>{t({sessions:[],activeSessionId:null,sessionMap:{},pendingElicitationBySessionId:{},chatStatusBySessionId:{},isResponsePendingBySessionId:{},draftInputBySessionId:{},pendingMessageBySessionId:{},pendingPatchExperimentsByToolCallId:{}},!1,{type:`clearAllSessions`})},setCapability:({key:e,enabled:n})=>{t(t=>{let r={...t.capabilities,[e]:n};return e!==`session.storeSessions`||n?{capabilities:r}:{capabilities:r,...Im({state:t,retainedSessionIds:t.activeSessionId?[t.activeSessionId]:[],activeSessionId:t.activeSessionId})}},!1,{type:`setCapability`})},pendingElicitationBySessionId:{},setPendingElicitation:(e,n)=>{t(t=>{let r={...t.pendingElicitationBySessionId};return n?r[e]=n:delete r[e],{pendingElicitationBySessionId:r}},!1,{type:`setPendingElicitation`})},draftInputBySessionId:{},setDraftInput:(e,n)=>{t(t=>{let r={...t.draftInputBySessionId};return n?r[e]=n:delete r[e],{draftInputBySessionId:r}},!1,{type:`setDraftInput`})},pendingMessageBySessionId:{},setPendingMessage:(e,n)=>{t(t=>{let r={...t.pendingMessageBySessionId};return n?r[e]=n:delete r[e],{pendingMessageBySessionId:r}},!1,{type:`setPendingMessage`})},consumePendingMessage:e=>{let r=n().pendingMessageBySessionId[e]??null;return r!=null&&t(t=>{if(!(e in t.pendingMessageBySessionId))return t;let n={...t.pendingMessageBySessionId};return delete n[e],{pendingMessageBySessionId:n}},!1,{type:`consumePendingMessage`}),r},chatStatusBySessionId:{},setSessionChatStatus:(e,n)=>{t(t=>({chatStatusBySessionId:{...t.chatStatusBySessionId,[e]:n}}),!1,{type:`setSessionChatStatus`})},isResponsePendingBySessionId:{},setSessionResponsePending:(e,n)=>{t(t=>{if(!(e in t.sessionMap))return t;let r={...t.isResponsePendingBySessionId};return n?r[e]=!0:delete r[e],{isResponsePendingBySessionId:r}},!1,{type:`setSessionResponsePending`})},setSessionUsage:(e,n)=>{t(t=>{let r=t.sessionMap[e];if(!r)return t;let i=r.usage??{tokenCount:{total:0,completion:0,prompt:0}};return{sessionMap:{...t.sessionMap,[e]:{...r,usage:{...i,tokenCount:{prompt:n.prompt,completion:n.completion,total:n.total??n.prompt+n.completion,...n.promptDetails?{promptDetails:n.promptDetails}:{}}}}}}},!1,{type:`setSessionUsage`})},setRouteContexts:e=>{t(t=>{if(t.routeContexts.length===e.length){let n=!0;for(let r=0;r<e.length;r++)if(Pd(t.routeContexts[r])!==Pd(e[r])){n=!1;break}if(n)return t}return{routeContexts:e}},!1,{type:`setRouteContexts`})},setMountedContext:(e,n)=>{t(t=>({mountedContexts:{...t.mountedContexts,[e]:n}}),!1,{type:`setMountedContext`})},removeMountedContext:e=>{t(t=>{if(!(e in t.mountedContexts))return t;let n={...t.mountedContexts};return delete n[e],{mountedContexts:n}},!1,{type:`removeMountedContext`})},registeredClientActions:{},registerClientAction:(e,n)=>{t(t=>({registeredClientActions:{...t.registeredClientActions,[e]:n}}),!1,{type:`registerClientAction`})},unregisterClientAction:e=>{t(t=>{if(!(e in t.registeredClientActions))return t;let n={...t.registeredClientActions};return delete n[e],{registeredClientActions:n}},!1,{type:`unregisterClientAction`})},setPendingPromptEdit:(e,n)=>{t(t=>{let r={...t.pendingPromptEditsByToolCallId};return n?r[e]=n:delete r[e],{pendingPromptEditsByToolCallId:r}},!1,{type:`setPendingPromptEdit`})},setPendingPromptInstanceRemoval:(e,n)=>{t(t=>{let r={...t.pendingPromptInstanceRemovalsByToolCallId};return n?r[e]=n:delete r[e],{pendingPromptInstanceRemovalsByToolCallId:r}},!1,{type:`setPendingPromptInstanceRemoval`})},setPendingDatasetWrite:(e,n)=>{t(t=>{let r={...t.pendingDatasetWritesByToolCallId};return n?r[e]=n:delete r[e],{pendingDatasetWritesByToolCallId:r}},!1,{type:`setPendingDatasetWrite`})},setPendingAnnotationConfigWrite:(e,n)=>{t(t=>{let r={...t.pendingAnnotationConfigWritesByToolCallId};return n?r[e]=n:delete r[e],{pendingAnnotationConfigWritesByToolCallId:r}},!1,{type:`setPendingAnnotationConfigWrite`})},setPendingBatchSpanAnnotate:(e,n)=>{t(t=>{let r={...t.pendingBatchSpanAnnotatesByToolCallId};return n?r[e]=n:delete r[e],{pendingBatchSpanAnnotatesByToolCallId:r}},!1,{type:`setPendingBatchSpanAnnotate`})},setPendingPatchExperiment:(e,n)=>{t(t=>{let r={...t.pendingPatchExperimentsByToolCallId};return n?r[e]=n:delete r[e],{pendingPatchExperimentsByToolCallId:r}},!1,{type:`setPendingPatchExperiment`})},setPendingPromptToolWrite:(e,n)=>{t(t=>{let r={...t.pendingPromptToolWritesByToolCallId};return n?r[e]=n:delete r[e],{pendingPromptToolWritesByToolCallId:r}},!1,{type:`setPendingPromptToolWrite`})},setPendingSavePrompt:(e,n)=>{t(t=>{let r={...t.pendingSavePromptsByToolCallId};return n?r[e]=n:delete r[e],{pendingSavePromptsByToolCallId:r}},!1,{type:`setPendingSavePrompt`})},setPendingCodeEvaluatorEdit:(e,n)=>{t(t=>{let r={...t.pendingCodeEvaluatorEditsByToolCallId};return n?r[e]=n:delete r[e],{pendingCodeEvaluatorEditsByToolCallId:r}},!1,{type:`setPendingCodeEvaluatorEdit`})},setPendingLlmEvaluatorEdit:(e,n)=>{t(t=>{let r={...t.pendingLlmEvaluatorEditsByToolCallId};return n?r[e]=n:delete r[e],{pendingLlmEvaluatorEditsByToolCallId:r}},!1,{type:`setPendingLlmEvaluatorEdit`})},setPendingLoadDataset:(e,n)=>{t(t=>{let r={...t.pendingLoadDatasetsByToolCallId};return n?r[e]=n:delete r[e],{pendingLoadDatasetsByToolCallId:r}},!1,{type:`setPendingLoadDataset`})},...e}),{name:`agentStore`}),{name:Rm(),version:0,partialize:e=>({isOpen:e.isOpen,position:e.position,fabMode:e.fabMode,fabPlacement:e.fabPlacement,sessions:e.sessions,activeSessionId:e.activeSessionId,sessionMap:e.sessionMap,defaultModelConfig:e.defaultModelConfig,observability:e.observability,permissions:e.permissions,capabilities:e.capabilities}),merge:Mm}));async function Bm({agentStore:e,names:t,timeoutMs:n=5e3}){let r=e=>t.every(t=>t in e);return r(e.getState().registeredClientActions)?!0:new Promise(t=>{let i=!1,a=null,o=e=>{i||(i=!0,a&&clearTimeout(a),s(),t(e))},s=e.subscribe(e=>{r(e.registeredClientActions)&&o(!0)});a=setTimeout(()=>o(!1),n),r(e.getState().registeredClientActions)&&o(!0)})}var Vm=(0,X.createContext)(null);function Hm(e){let t=(0,Z.c)(8),n,r;t[0]===e?(n=t[1],r=t[2]):({children:n,...r}=e,t[0]=e,t[1]=n,t[2]=r);let i;t[3]===r?i=t[4]:(i=()=>zm(r),t[3]=r,t[4]=i);let[a]=(0,X.useState)(i),o;return t[5]!==n||t[6]!==a?(o=W(Vm.Provider,{value:a,children:n}),t[5]=n,t[6]=a,t[7]=o):o=t[7],o}function Um(e,t){let n=(0,X.useContext)(Vm);if(!n)throw Error(`Missing AgentContext.Provider in the tree`);return c(n,e,t)}function Wm(){let e=(0,X.useContext)(Vm);if(!e)throw Error(`Missing AgentContext.Provider in the tree`);return e}var Gm=(0,X.createContext)(null);function Km(){return X.useContext(Gm)}function qm(){let e=Km();if(e===null)throw Error(`useTimeRange must be used within a TimeRangeContextProvider`);return e}function Jm({storedLastNTimeRangeKey:e,now:t}){return Xu(e)?{timeRangeKey:e,...Ju(e,t)}:{timeRangeKey:`7d`,...Ju(`7d`,t)}}function Ym(e){let t=(0,Z.c)(37),{children:n}=e,[r,i]=Nn(),a=Zr(Qm),o=Zr(Zm),[s,c]=(0,X.useState)(Xm),l,u,d,f,p;t[0]!==r||t[1]!==a||t[2]!==s?(p=Qu(r,s),d=p??Jm({storedLastNTimeRangeKey:a,now:s}),f=d.start?.getTime(),l=d.start?.toISOString(),u=d.end?.toISOString(),t[0]=r,t[1]=a,t[2]=s,t[3]=l,t[4]=u,t[5]=d,t[6]=f,t[7]=p):(l=t[3],u=t[4],d=t[5],f=t[6],p=t[7]);let m=u,h;t[8]!==m||t[9]!==l?(h={start:l,end:m},t[8]=m,t[9]=l,t[10]=h):h=t[10];let g=h,_;t[11]!==i||t[12]!==o?(_=e=>{(0,X.startTransition)(()=>{i(t=>$u({searchParams:t,timeRange:e}),{replace:!0}),Xu(e.timeRangeKey)&&(o(e.timeRangeKey),c(Date.now()))})},t[11]=i,t[12]=o,t[13]=_):_=t[13];let v=_,y;t[14]===v?y=t[15]:(y=e=>{v({timeRangeKey:`custom`,start:e.start,end:e.end})},t[14]=v,t[15]=y);let b=y,x,S;t[16]!==r||t[17]!==i||t[18]!==d||t[19]!==p?(x=()=>{if(p!=null)return;let e=$u({searchParams:r,timeRange:d});e.toString()!==r.toString()&&i(e,{replace:!0})},S=[p,r,i,d],t[16]=r,t[17]=i,t[18]=d,t[19]=p,t[20]=x,t[21]=S):(x=t[20],S=t[21]),(0,X.useEffect)(x,S);let C;t[22]===d.timeRangeKey?C=t[23]:(C=()=>{if(!Xu(d.timeRangeKey))return;let e=d.timeRangeKey,t=window.setTimeout(()=>{c(Date.now())},Yu(e));return()=>{window.clearTimeout(t)}},t[22]=d.timeRangeKey,t[23]=C);let w;t[24]!==d.timeRangeKey||t[25]!==f?(w=[d.timeRangeKey,f],t[24]=d.timeRangeKey,t[25]=f,t[26]=w):w=t[26],(0,X.useEffect)(C,w);let T;t[27]===v?T=t[28]:(T={setTimeRange:v},t[27]=v,t[28]=T),eh(T);let E;t[29]!==b||t[30]!==v||t[31]!==d||t[32]!==g?(E={timeRange:d,timeRangeISOStrings:g,setTimeRange:v,setCustomTimeRange:b},t[29]=b,t[30]=v,t[31]=d,t[32]=g,t[33]=E):E=t[33];let D;return t[34]!==n||t[35]!==E?(D=W(Gm.Provider,{value:E,children:n}),t[34]=n,t[35]=E,t[36]=D):D=t[36],D}function Xm(){return Date.now()}function Zm(e){return e.setLastNTimeRangeKey}function Qm(e){return e.lastNTimeRangeKey}function $m(e){if(e===void 0||e.trim()===``)return;let t=new Date(e);if(Number.isNaN(t.getTime()))throw Error(`Invalid ISO datetime: ${e}`);return t}function eh({setTimeRange:e}){let t=Wm(),n=(0,X.useEffectEvent)(async t=>{if(t.timeRangeKey!==`custom`)return e({timeRangeKey:t.timeRangeKey,...Ju(t.timeRangeKey)}),{ok:!0,output:`Set time range to ${t.timeRangeKey}.`};try{let n=$m(t.startTime),r=$m(t.endTime);return n===void 0&&r===void 0?{ok:!1,error:`Custom time range requires at least one of startTime or endTime.`}:n!==void 0&&r!==void 0&&n>r?{ok:!1,error:`Custom time range startTime must be before endTime.`}:(e({timeRangeKey:`custom`,start:n,end:r}),{ok:!0,output:`Set custom time range from ${n?.toISOString()??`open start`} to ${r?.toISOString()??`open end`}.`})}catch(e){return{ok:!1,error:e instanceof Error?e.message:`Invalid time range.`}}});(0,X.useEffect)(()=>{let{registerClientAction:e,unregisterClientAction:r}=t.getState();return e(wd,e=>n(e)),()=>{r(wd)}},[t])}var th=Me(),nh=500;function rh(e,t){let n=(0,Z.c)(5),r=t===void 0?nh:t,i;n[0]===e?i=n[1]:(i=t=>{try{e(JSON.parse(t))}catch{}},n[0]=e,n[1]=i);let a;return n[2]!==r||n[3]!==i?(a=(0,th.debounce)(i,r),n[2]=r,n[3]=i,n[4]=a):a=n[4],a}function ih(e,t){let n=(0,Z.c)(6),r=(0,X.useRef)(null),i,a;n[0]===e?(i=n[1],a=n[2]):(i=()=>{r.current=e},a=[e],n[0]=e,n[1]=i,n[2]=a),(0,X.useEffect)(i,a);let o,s;n[3]===t?(o=n[4],s=n[5]):(o=()=>{if(typeof t!=`number`)return;let e=t,n=function(){r.current?.()},i=setInterval(n,e),a=function(){document.visibilityState===`hidden`?i!=null&&(clearInterval(i),i=null):i??=(n(),setInterval(n,e))};return document.addEventListener(`visibilitychange`,a),()=>{i!=null&&clearInterval(i),document.removeEventListener(`visibilitychange`,a)}},s=[t],n[3]=t,n[4]=o,n[5]=s),(0,X.useEffect)(o,s)}var ah=.05,oh=({word:e,theme:t})=>{let n=ae(e.charCodeAt(0)%26/26),r=t===`light`?3:5,i=t===`light`?`#fdfdfd`:`#0E0E0E`,a=ce(n,i);for(;a<r;)n=t===`light`?re(ah,n):be(ah,n),a=ce(n,i);return n},sh=e=>{let t=(0,Z.c)(3),{theme:n}=vr(),r;return t[0]!==n||t[1]!==e?(r=oh({word:e,theme:n}),t[0]=n,t[1]=e,t[2]=r):r=t[2],r};function ch(e,t){let n=new Intl.DateTimeFormat(e,{...t});return e=>n.format(e)}function lh(e){let{locale:t,timeZone:n}=e;return ch(t,{year:`numeric`,month:`2-digit`,day:`2-digit`,hour:`2-digit`,minute:`2-digit`,second:`2-digit`,hour12:!0,timeZone:n})}function uh(e){let{locale:t,timeZone:n}=e;return ch(t,{hour:`2-digit`,minute:`2-digit`,hour12:!0,timeZone:n})}function dh(e){let{locale:t,timeZone:n}=e;return ch(t,{year:`numeric`,month:`2-digit`,day:`2-digit`,hour:`2-digit`,minute:`2-digit`,hour12:!0,timeZone:n})}function fh(e){let t=dh(e);return e=>e.start&&e.end?`${t(e.start)} - ${t(e.end)}`:e.start?`From ${t(e.start)}`:e.end?`Until ${t(e.end)}`:`All Time`}function ph(e){let{timeZone:t,locale:n}=e;return Intl.DateTimeFormat(n,{timeZoneName:`short`,timeZone:t}).formatToParts().find(e=>e.type===`timeZoneName`)?.value}function mh(e,t=Date.now()){if(e===0)return``;let n=t-e;return n<6*36e5?new Date(e).toLocaleTimeString(void 0,{hour:`numeric`,minute:`2-digit`}):n<864e5?`${Math.floor(n/Hi)}h`:`${Math.floor(n/Ui)}d`}function hh(e){return new Intl.DateTimeFormat(e,{day:`2-digit`,month:`2-digit`,year:`numeric`}).formatToParts(new Date).map(e=>{switch(e.type){case`day`:return`dd`;case`month`:return`mm`;case`year`:return`yyyy`;case`literal`:return e.value;default:return``}}).join(``)}function gh(){let e=(0,Z.c)(2),{locale:t}=Fn(),n;return e[0]===t?n=e[1]:(n=hh(t),e[0]=t,e[1]=n),n}var _h=e=>{let t=(0,Z.c)(3),[n,r]=(0,X.useState)(null),i,a;return t[0]===e?(i=t[1],a=t[2]):(i=()=>{if(!e.current)return;let t=new ResizeObserver(e=>{if(!e||e.length===0)return;let{width:t,height:n}=e[0].contentRect;r({width:t,height:n})});return t.observe(e.current),()=>{t.disconnect()}},a=[e],t[0]=e,t[1]=i,t[2]=a),(0,X.useEffect)(i,a),n};function vh(){let e=(0,Z.c)(10),t=Zr(yh),n,r,i,a;if(e[0]!==t){let o=t??Hr();n=lh({locale:Vr(),timeZone:o}),r=uh({locale:Vr(),timeZone:o}),i=dh({locale:Vr(),timeZone:o}),a=fh({locale:Vr(),timeZone:o}),e[0]=t,e[1]=n,e[2]=r,e[3]=i,e[4]=a}else n=e[1],r=e[2],i=e[3],a=e[4];let o;return e[5]!==n||e[6]!==r||e[7]!==i||e[8]!==a?(o={fullTimeFormatter:n,shortTimeFormatter:r,shortDateTimeFormatter:i,timeRangeFormatter:a},e[5]=n,e[6]=r,e[7]=i,e[8]=a,e[9]=o):o=e[9],o}function yh(e){return e.displayTimezone}function bh(e){let t=(0,Z.c)(7),n;t[0]===e?n=t[1]:(n=e===void 0?{}:e,t[0]=e,t[1]=n);let{updateIntervalMs:r}=n,i=r===void 0?null:r,[a,o]=(0,X.useState)(xh),s,c;t[2]===i?(s=t[3],c=t[4]):(s=()=>{if(typeof i!=`number`)return;let e=setInterval(()=>{o(Date.now())},i);return()=>clearInterval(e)},c=[i],t[2]=i,t[3]=s,t[4]=c),(0,X.useEffect)(s,c);let l;return t[5]===a?l=t[6]:(l={nowEpochMs:a},t[5]=a,t[6]=l),l}function xh(){return Date.now()}function Sh(e){let t=(0,Z.c)(2),n;return t[0]===e?n=t[1]:(n=tp(e),t[0]=e,t[1]=n),n}var Ch=`https://pypi.org/pypi/arize-phoenix/json`,wh=null;function Th(){return wh??=fetch(Ch).then(e=>e.ok?e.json():null).then(e=>{let t=e?.info?.version;return typeof t==`string`?t:null}).catch(()=>null).then(e=>(e??(wh=null),e)),wh}function Eh(){let e=(0,Z.c)(2),[t,n]=(0,X.useState)(null),r,i;return e[0]===Symbol.for(`react.memo_cache_sentinel`)?(r=()=>{let e=!0;return Th().then(t=>{e&&n(t)}),()=>{e=!1}},i=[],e[0]=r,e[1]=i):(r=e[0],i=e[1]),(0,X.useEffect)(r,i),t}function Dh(e,t){let[n,r]=(0,X.useState)(()=>{try{let n=localStorage.getItem(e);return n?JSON.parse(n):t}catch{return t}});return[n,(0,X.useCallback)(t=>{r(n=>{let r=typeof t==`function`?t(n):t;try{localStorage.setItem(e,JSON.stringify(r))}catch{}return r})},[e])]}function Oh(e){let{query:t,queryRef:n}=e,[r]=(0,ei.useQueryLoader)(t,n);return Re(r,`ownedQueryRef is required when initialized from queryRef`),(0,ei.usePreloadedQuery)(t,r)}function kh(){let e=(0,Z.c)(7),[t,n]=Nn(),r;e[0]===t?r=e[1]:(r=t.getAll(Lu),e[0]=t,e[1]=r);let i=r,a;e[2]===n?a=e[3]:(a=e=>{n(t=>{let n=t.getAll(Lu),r=typeof e==`function`?e(n):e,i=new URLSearchParams(t);return i.delete(Lu),r.forEach(e=>i.append(Lu,e)),i},{replace:!0})},e[2]=n,e[3]=a);let o=a,s;return e[4]!==i||e[5]!==o?(s=[i,o],e[4]=i,e[5]=o,e[6]=s):s=e[6],s}function Ah(e){let t=(0,Z.c)(4),n;t[0]===e?n=t[1]:(n=t=>{let n=window.matchMedia(e);return n.addEventListener(`change`,t),()=>n.removeEventListener(`change`,t)},t[0]=e,t[1]=n);let r=n,i;return t[2]===e?i=t[3]:(i=()=>window.matchMedia(e).matches,t[2]=e,t[3]=i),(0,X.useSyncExternalStore)(r,i)}function jh(e){let t=(0,Z.c)(49),{start:n,end:r,timeZone:i,isDisabled:a,onCommit:o,autoFocus:s,onBlurWithin:c,onSubmit:l,ref:u}=e,d=(0,X.useRef)(!1),f=(0,X.useRef)(!1),p=r==null,m;t[0]!==n||t[1]!==i?(m=()=>gd(n,i),t[0]=n,t[1]=i,t[2]=m):m=t[2];let[h,g]=(0,X.useState)(m),v;t[3]!==r||t[4]!==i?(v=()=>gd(r,i)??Ce(i),t[3]=r,t[4]=i,t[5]=v):v=t[5];let[y,b]=(0,X.useState)(v),x;t[6]!==h||t[7]!==i?(x=h?h.toDate(i):null,t[6]=h,t[7]=i,t[8]=x):x=t[8];let S=x,C;t[9]!==y||t[10]!==i?(C=y?y.toDate(i):null,t[9]=y,t[10]=i,t[11]=C):C=t[11];let w=C,T=!!(S&&w&&S>w),E;t[12]!==r||t[13]!==n||t[14]!==i?(E=()=>{g(gd(n,i)),b(gd(r,i)??Ce(i)),d.current=!1,f.current=!1},t[12]=r,t[13]=n,t[14]=i,t[15]=E):E=t[15];let D=E,O;t[16]!==w||t[17]!==p||t[18]!==o||t[19]!==D||t[20]!==S?(O=()=>{if(!d.current)return;let e=p&&!f.current?null:w;if(S&&e&&S>e){D();return}d.current=!1,o({start:S,end:e})},t[16]=w,t[17]=p,t[18]=o,t[19]=D,t[20]=S,t[21]=O):O=t[21];let k=O,A,j;t[22]===k?(A=t[23],j=t[24]):(A=()=>({commit:k}),j=[k],t[22]=k,t[23]=A,t[24]=j),(0,X.useImperativeHandle)(u,A,j);let M;t[25]!==k||t[26]!==c?(M={onBlurWithin:()=>{k(),c?.()}},t[25]=k,t[26]=c,t[27]=M):M=t[27];let{focusWithinProps:N}=Qt(M),P=T||void 0,F;t[28]!==k||t[29]!==l?(F=e=>{e.key===`Enter`&&(e.preventDefault(),k(),l?.())},t[28]=k,t[29]=l,t[30]=F):F=t[30];let I,L;t[31]===Symbol.for(`react.memo_cache_sentinel`)?(I=e=>{g(e),d.current=!0},L=W(_,{children:Nh}),t[31]=I,t[32]=L):(I=t[31],L=t[32]);let R;t[33]!==s||t[34]!==a||t[35]!==h?(R=W(fe,{"aria-label":`Start time`,className:`time-range-selector__field`,granularity:`minute`,hideTimeZone:!0,isDisabled:a,autoFocus:s,value:h,onChange:I,children:L}),t[33]=s,t[34]=a,t[35]=h,t[36]=R):R=t[36];let z;t[37]===Symbol.for(`react.memo_cache_sentinel`)?(z=W(`span`,{"aria-hidden":!0,className:`time-range-selector__separator`,children:`–`}),t[37]=z):z=t[37];let ee,te;t[38]===Symbol.for(`react.memo_cache_sentinel`)?(ee=e=>{b(e),d.current=!0,f.current=!0},te=W(_,{children:Mh}),t[38]=ee,t[39]=te):(ee=t[38],te=t[39]);let ne;t[40]!==y||t[41]!==a?(ne=W(fe,{"aria-label":`End time`,className:`time-range-selector__field`,granularity:`minute`,hideTimeZone:!0,isDisabled:a,value:y,onChange:ee,children:te}),t[40]=y,t[41]=a,t[42]=ne):ne=t[42];let re;return t[43]!==N||t[44]!==P||t[45]!==F||t[46]!==R||t[47]!==ne?(re=G(`div`,{className:`time-range-selector__fields`,"data-invalid":P,onKeyDownCapture:F,...N,children:[R,z,ne]}),t[43]=N,t[44]=P,t[45]=F,t[46]=R,t[47]=ne,t[48]=re):re=t[48],re}function Mh(e){return W(i,{segment:e})}function Nh(e){return W(i,{segment:e})}var Ph=q`
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
`,Fh=q`
  /* Fill the popover, which is sized to the field it is anchored to. */
  width: 100%;
`,Ih=q`
  padding: var(--global-dimension-size-200) var(--global-dimension-size-150);
`,Lh=q`
  width: 100%;
  border-bottom: var(--global-border-size-thin) solid
    var(--global-menu-border-color);
`,Rh=q`
  flex: none;
  font-variant-numeric: tabular-nums;
`,zh=q`
  width: 100%;
  justify-content: flex-start;
`,Bh=`var(--global-dimension-size-4000)`;function Vh(e){let t=(0,Z.c)(85),{value:n,isDisabled:r,onChange:i,size:a}=e,o=a===void 0?`S`:a,{timeRangeKey:s,start:c,end:l}=n,u=(0,X.useRef)(null),f=(0,X.useRef)(null),p=(0,X.useRef)(null),m=(0,X.useRef)(null),h=(0,X.useRef)(null),_=(0,X.useRef)(null),[v,y]=(0,X.useState)(!1),[b,x]=(0,X.useState)(!1),[S,C]=(0,X.useState)(!1),[w,T]=(0,X.useState)(),[D,O]=(0,X.useState)(``),k;t[0]===Symbol.for(`react.memo_cache_sentinel`)?(k={sensitivity:`base`},t[0]=k):k=t[0];let{contains:A}=g(k),j;t[1]===Symbol.for(`react.memo_cache_sentinel`)?(j={isTextInput:!0},t[1]=j):j=t[1];let{isFocusVisible:M}=_n(j),N=b&&M,P;t[2]===Symbol.for(`react.memo_cache_sentinel`)?(P=()=>{y(!1),C(!1),O(``)},t[2]=P):P=t[2];let F=P,I;t[3]===Symbol.for(`react.memo_cache_sentinel`)?(I=()=>{let e=document.activeElement;return e instanceof HTMLElement&&(u.current?.contains(e)||f.current?.contains(e))?e:null},t[3]=I):I=t[3];let L=I,R;t[4]===Symbol.for(`react.memo_cache_sentinel`)?(R=()=>{setTimeout(()=>{L()||(x(!1),F())})},t[4]=R):R=t[4];let z=R,ee;t[5]===Symbol.for(`react.memo_cache_sentinel`)?(ee=()=>{L()?.blur()},t[5]=ee):ee=t[5];let te=ee,ne;t[6]===Symbol.for(`react.memo_cache_sentinel`)?(ne=()=>{te(),x(!1),F()},t[6]=ne):ne=t[6];let re=ne,ie;t[7]===Symbol.for(`react.memo_cache_sentinel`)?(ie=()=>{_.current?.commit(),re()},t[7]=ie):ie=t[7];let ae=ie,oe;t[8]===Symbol.for(`react.memo_cache_sentinel`)?(oe=()=>{y(!0)},t[8]=oe):oe=t[8];let se=oe,ce=!v,le;t[9]===Symbol.for(`react.memo_cache_sentinel`)?(le=e=>{e.target instanceof Node&&f.current?.contains(e.target)||ae()},t[9]=le):le=t[9];let ue;t[10]===ce?ue=t[11]:(ue={ref:u,isDisabled:ce,onInteractOutside:le},t[10]=ce,t[11]=ue),bn(ue);let de;t[12]===D?de=t[13]:(de=e=>{if(e.stopPropagation(),D&&document.activeElement===p.current){O(``);return}ae()},t[12]=D,t[13]=de);let fe;t[14]===Symbol.for(`react.memo_cache_sentinel`)?(fe={capture:!0},t[14]=fe):fe=t[14];let pe;t[15]===b?pe=t[16]:(pe={enabled:b,enableOnFormTags:!0,enableOnContentEditable:!0,preventDefault:!0,eventListenerOptions:fe},t[15]=b,t[16]=pe),jt(`escape`,de,pe);let me=_h(m),he=Zr(Wh),ge,_e,ve,ye,be;if(t[17]!==he||t[18]!==l||t[19]!==c||t[20]!==s){ye=he??Hr();let e=Vr();be=ph({locale:e,timeZone:ye}),_e=s===`custom`,ge=_e?`Custom`:s;let n=fh({locale:e,timeZone:ye});ve=Xu(s)?td(s):n({start:c,end:l}),t[17]=he,t[18]=l,t[19]=c,t[20]=s,t[21]=ge,t[22]=_e,t[23]=ve,t[24]=ye,t[25]=be}else ge=t[21],_e=t[22],ve=t[23],ye=t[24],be=t[25];let xe=ve,Se=ad(D),Ce=Bu.filter(e=>{let{key:t}=e;return!Se.includes(t)}),we;t[26]===c?we=t[27]:(we=c?.getTime()??``,t[26]=c,t[27]=we);let Te;t[28]===l?Te=t[29]:(Te=l?.getTime()??``,t[28]=l,t[29]=Te);let Ee=`${s}|${we}|${Te}|${ye}`,De=me?.width,Oe=`${b}|${Ee}|${xe}|${ge}|${be??``}`,ke=v&&w!=null,Ae;t[30]!==r||t[31]!==b?(Ae=e=>{if(r||b)return;let t=h.current,n=e.target instanceof Node&&t?.contains(e.target);!t||n||(e.preventDefault(),t.focus())},t[30]=r,t[31]=b,t[32]=Ae):Ae=t[32];let je=Ae,Me;t[33]===v?Me=t[34]:(Me=()=>{let e=v?u.current?.offsetWidth:void 0,t=e?`${e}px`:void 0;T(e=>e===t?e:t)},t[33]=v,t[34]=Me);let Ne;t[35]!==v||t[36]!==Oe?(Ne=[v,Oe],t[35]=v,t[36]=Oe,t[37]=Ne):Ne=t[37],(0,X.useLayoutEffect)(Me,Ne);let Pe,Fe;t[38]!==S||t[39]!==ke?(Pe=()=>{!ke||S||p.current?.focus()},Fe=[ke,S],t[38]=S,t[39]=ke,t[40]=Pe,t[41]=Fe):(Pe=t[40],Fe=t[41]),(0,X.useLayoutEffect)(Pe,Fe);let Ie=r||void 0,Le=N||void 0,B=v||void 0,Re=_e?`info`:`default`,ze;t[42]!==ge||t[43]!==Re?(ze=W(Fo,{size:`S`,variant:Re,css:Rh,children:ge}),t[42]=ge,t[43]=Re,t[44]=ze):ze=t[44];let Be=v||De==null?`auto`:De,Ve=b?Bh:void 0,He;t[45]!==Be||t[46]!==Ve?(He={width:Be,minWidth:Ve},t[45]=Be,t[46]=Ve,t[47]=He):He=t[47];let We;t[48]!==l||t[49]!==Ee||t[50]!==r||t[51]!==b||t[52]!==i||t[53]!==c||t[54]!==ye||t[55]!==xe?(We=W(`div`,{ref:m,className:`time-range-selector__value-measure`,children:b?W(jh,{ref:_,start:c,end:l,timeZone:ye,isDisabled:r,autoFocus:!0,onBlurWithin:z,onSubmit:re,onCommit:e=>i({timeRangeKey:`custom`,...e})},Ee):W(`button`,{ref:h,type:`button`,className:`time-range-selector__value`,disabled:r,onFocus:()=>{r||(x(!0),se())},children:xe})}),t[48]=l,t[49]=Ee,t[50]=r,t[51]=b,t[52]=i,t[53]=c,t[54]=ye,t[55]=xe,t[56]=We):We=t[56];let Ge;t[57]!==He||t[58]!==We?(Ge=W(`div`,{className:`time-range-selector__value-shell`,style:He,children:We}),t[57]=He,t[58]=We,t[59]=Ge):Ge=t[59];let Ke;t[60]===be?Ke=t[61]:(Ke=be&&W(V,{size:`XS`,color:`text-500`,className:`time-range-selector__timezone`,children:be}),t[60]=be,t[61]=Ke);let qe;t[62]!==je||t[63]!==o||t[64]!==Ie||t[65]!==Le||t[66]!==B||t[67]!==ze||t[68]!==Ge||t[69]!==Ke?(qe=G(`div`,{ref:u,className:`time-range-selector`,css:Ph,"data-size":o,"data-disabled":Ie,"data-focus-visible":Le,"data-presets-open":B,role:`group`,"aria-label":`Time range`,onPointerDown:je,children:[ze,Ge,Ke]}),t[62]=je,t[63]=o,t[64]=Ie,t[65]=Le,t[66]=B,t[67]=ze,t[68]=Ge,t[69]=Ke,t[70]=qe):qe=t[70];let Je=jn,Ye;t[71]===Symbol.for(`react.memo_cache_sentinel`)?(Ye=e=>{e||F()},t[71]=Ye):Ye=t[71];let Xe=S?`bottom end`:`bottom start`,Ze=S?`max-content`:w,Qe=S?w:void 0,$e;t[72]!==Ze||t[73]!==Qe?($e={width:Ze,minWidth:Qe,overflow:`hidden`,transition:`none`,animation:`none`,transform:`translateY(0)`,opacity:1},t[72]=Ze,t[73]=Qe,t[74]=$e):$e=t[74];let et=S?W(xd,{value:{start:c,end:l},timeZone:ye,onCancel:()=>C(!1),onApply:e=>{x(!1),F(),i({timeRangeKey:`custom`,...e})}}):G(U,{children:[G(Ue,{filter:A,children:[G(es,{"aria-label":`Search time range presets`,size:`M`,variant:`quiet`,value:D,onChange:O,css:Lh,children:[W(Qo,{}),W(E,{ref:p,placeholder:`Search or type "25m"`,onBlur:z})]}),G(Zs,{"aria-label":`time range preset selection`,selectionMode:`single`,selectedKeys:_e?[]:[s],css:Fh,renderEmptyState:Uh,onSelectionChange:e=>{let t=e===`all`?void 0:e.keys().next().value,n=Xu(t)?t:Xu(s)?s:void 0;if(x(!1),!n){F();return}let r=Ju(n);F(),i({timeRangeKey:n,...r})},children:[Se.map(e=>W(d,{id:e,textValue:D,children:td(e)},e)),Ce.map(Hh)]})]}),W(wa,{children:W(yt,{size:`S`,variant:`quiet`,css:zh,leadingVisual:W(H,{svg:W(Wt,{})}),onPress:()=>C(!0),children:`Pick from a calendar`})})]}),tt;t[75]!==Je||t[76]!==ke||t[77]!==Ye||t[78]!==Xe||t[79]!==$e||t[80]!==et?(tt=W(Je,{ref:f,triggerRef:u,isOpen:ke,onOpenChange:Ye,isNonModal:!0,isKeyboardDismissDisabled:!0,placement:Xe,offset:2,style:$e,children:et}),t[75]=Je,t[76]=ke,t[77]=Ye,t[78]=Xe,t[79]=$e,t[80]=et,t[81]=tt):tt=t[81];let nt;return t[82]!==qe||t[83]!==tt?(nt=G(U,{children:[qe,tt]}),t[82]=qe,t[83]=tt,t[84]=nt):nt=t[84],nt}function Hh(e){let{key:t,label:n}=e;return W(d,{id:t,children:n},t)}function Uh(){return W(`div`,{css:Ih,children:`No matching time ranges`})}function Wh(e){return e.displayTimezone}var Gh=Ke`
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.35;
  }
`,Kh=q`
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

  &[data-size="S"] {
    height: var(--global-input-height-s);
  }
  &[data-size="M"] {
    height: var(--global-input-height-m);
  }

  /* Fade the whole shell as one unit, not each button twice over. */
  &[data-disabled] {
    opacity: var(--global-opacity-disabled);
    button[disabled] {
      opacity: 1;
    }
  }
`,qh=q`
  position: relative;
  border: none;
  background-color: transparent;
  border-radius: var(--global-rounding-xsmall);
  color: var(--global-text-color-700);
  transition:
    background-color 0.2s ease-in-out,
    color 0.2s ease-in-out;

  &[data-size] {
    align-self: stretch;
    height: auto;
    aspect-ratio: 1 / 1;
  }
  &[data-size][data-childless] {
    padding: 0;
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
      animation: ${Gh} 3s ease-in-out infinite;
    }
  }

  @media (prefers-reduced-motion: reduce) {
    &[data-selected="true"]::before {
      animation: none;
    }
  }
`;function Jh(e){let t=(0,Z.c)(13),{label:n,icon:r,size:i,isDisabled:a,onPress:o}=e,s;t[0]===r?s=t[1]:(s=W(H,{svg:r}),t[0]=r,t[1]=s);let c;t[2]!==a||t[3]!==n||t[4]!==o||t[5]!==i||t[6]!==s?(c=W(yt,{size:i,variant:`quiet`,css:qh,"aria-label":n,isDisabled:a,leadingVisual:s,onPress:o}),t[2]=a,t[3]=n,t[4]=o,t[5]=i,t[6]=s,t[7]=c):c=t[7];let l;t[8]===n?l=t[9]:(l=W(Ri,{children:n}),t[8]=n,t[9]=l);let u;return t[10]!==c||t[11]!==l?(u=G(A,{children:[c,l]}),t[10]=c,t[11]=l,t[12]=u):u=t[12],u}function Yh(e){let t=(0,Z.c)(48),{value:n,onChange:r,isLive:i,onIsLiveChange:a,isDisabled:o,size:s}=e,c=i!==void 0&&i,l=s===void 0?`S`:s,u=n.start!=null,d=c?`Stop live streaming`:`Resume live streaming`,f=n.end==null,p;t[0]===r?p=t[1]:(p=e=>{e&&r(e)},t[0]=r,t[1]=p);let m=p,h=o||void 0,g;t[2]===Symbol.for(`react.memo_cache_sentinel`)?(g=W(Tn,{}),t[2]=g):g=t[2];let _=o||!u,v;t[3]!==m||t[4]!==n?(v=()=>m(dd({value:n})),t[3]=m,t[4]=n,t[5]=v):v=t[5];let y;t[6]!==l||t[7]!==_||t[8]!==v?(y=W(Jh,{label:`Pan back in time`,icon:g,size:l,isDisabled:_,onPress:v}),t[6]=l,t[7]=_,t[8]=v,t[9]=y):y=t[9];let b;t[10]===Symbol.for(`react.memo_cache_sentinel`)?(b=W(An,{}),t[10]=b):b=t[10];let x=o||!u,S;t[11]!==m||t[12]!==n?(S=()=>m(md({value:n})),t[11]=m,t[12]=n,t[13]=S):S=t[13];let C;t[14]!==l||t[15]!==S||t[16]!==x?(C=W(Jh,{label:`Zoom out`,icon:b,size:l,isDisabled:x,onPress:S}),t[14]=l,t[15]=S,t[16]=x,t[17]=C):C=t[17];let w;t[18]!==o||t[19]!==c||t[20]!==d||t[21]!==a||t[22]!==l?(w=a&&G(A,{children:[W(zs,{size:l,className:`time-range-controls__live-toggle`,css:qh,"aria-label":d,isSelected:c,isDisabled:o,leadingVisual:W(H,{svg:W(c?Ze:We,{})}),onChange:a}),W(Ri,{children:d})]}),t[18]=o,t[19]=c,t[20]=d,t[21]=a,t[22]=l,t[23]=w):w=t[23];let T;t[24]===Symbol.for(`react.memo_cache_sentinel`)?(T=W(_t,{}),t[24]=T):T=t[24];let E=o||!u,D;t[25]!==m||t[26]!==n?(D=()=>m(pd({value:n})),t[25]=m,t[26]=n,t[27]=D):D=t[27];let O;t[28]!==l||t[29]!==E||t[30]!==D?(O=W(Jh,{label:`Zoom in`,icon:T,size:l,isDisabled:E,onPress:D}),t[28]=l,t[29]=E,t[30]=D,t[31]=O):O=t[31];let k;t[32]===Symbol.for(`react.memo_cache_sentinel`)?(k=W(Pn,{}),t[32]=k):k=t[32];let j=o||!u||f,M;t[33]!==m||t[34]!==n?(M=()=>m(fd({value:n})),t[33]=m,t[34]=n,t[35]=M):M=t[35];let N;t[36]!==l||t[37]!==j||t[38]!==M?(N=W(Jh,{label:`Pan forward in time`,icon:k,size:l,isDisabled:j,onPress:M}),t[36]=l,t[37]=j,t[38]=M,t[39]=N):N=t[39];let P;return t[40]!==l||t[41]!==C||t[42]!==w||t[43]!==O||t[44]!==N||t[45]!==h||t[46]!==y?(P=G(`div`,{className:`time-range-controls`,css:Kh,role:`group`,"aria-label":`Time range controls`,"data-size":l,"data-disabled":h,children:[y,C,w,O,N]}),t[40]=l,t[41]=C,t[42]=w,t[43]=O,t[44]=N,t[45]=h,t[46]=y,t[47]=P):P=t[47],P}function Xh(e){let t=(0,Z.c)(4),{size:n}=e,r=n===void 0?`S`:n,{timeRange:i,setTimeRange:a}=qm(),o;return t[0]!==a||t[1]!==r||t[2]!==i?(o=W(Vh,{value:i,onChange:a,size:r}),t[0]=a,t[1]=r,t[2]=i,t[3]=o):o=t[3],o}function Zh(e){let t=(0,Z.c)(4),{timeRange:n,setTimeRange:r}=qm(),i;return t[0]!==e||t[1]!==r||t[2]!==n?(i=W(Yh,{...e,value:n,onChange:r}),t[0]=e,t[1]=r,t[2]=n,t[3]=i):i=t[3],i}q`
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
`;var Qh=(0,X.createContext)(null);function $h(){return(0,X.useContext)(Qh)??{variant:`grid`}}var eg=q`
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
`,tg=q`
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
`,ng=q`
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
`,rg=q`
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
    ${Gl}
    position: absolute;
    top: var(--global-dimension-size-75);
    right: var(--global-dimension-size-75);
    width: var(--global-dimension-size-300);
    height: var(--global-dimension-size-300);
    border-radius: 50%;
    background-color: var(--global-color-gray-50);
  }

  &[data-variant="inline"] {
    ${Gl}
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
`;function ig(e){let t=(0,Z.c)(17),n,r,i,a,o;t[0]===e?(n=t[1],r=t[2],i=t[3],a=t[4],o=t[5]):({children:n,ref:r,variant:a,collapsible:o,...i}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a,t[5]=o);let s=a===void 0?`grid`:a,c=o!==void 0&&o,l;t[6]===s?l=t[7]:(l={variant:s},t[6]=s,t[7]=l);let u=l,d=c||void 0,f;t[8]!==n||t[9]!==r||t[10]!==i||t[11]!==d||t[12]!==s?(f=W(`div`,{ref:r,css:eg,"data-variant":s,"data-collapsible":d,...i,children:n}),t[8]=n,t[9]=r,t[10]=i,t[11]=d,t[12]=s,t[13]=f):f=t[13];let p;return t[14]!==f||t[15]!==u?(p=W(Qh.Provider,{value:u,children:f}),t[14]=f,t[15]=u,t[16]=p):p=t[16],p}var ag=(0,X.createContext)(null);function og(){let e=(0,X.useContext)(ag);if(!e)throw Error(`useAttachmentContext must be used within an <Attachment> component`);return e}function sg(e){if(e.type===`context`)return`context`;if(e.type===`source-document`)return`source`;let t=e.mediaType??``;return t.startsWith(`image/`)?`image`:t.startsWith(`video/`)?`video`:t.startsWith(`audio/`)?`audio`:t.startsWith(`application/`)||t.startsWith(`text/`)?`document`:`unknown`}function cg(e){return e.type===`context`?e.label:e.type===`source-document`?e.title||e.filename||`Source`:e.filename||(sg(e)===`image`?`Image`:`Attachment`)}function lg(e){return e.type===`context`?e.detail:void 0}function ug(e){switch(e){case`project`:return W(H,{svg:W(cn,{})});case`trace`:return W(H,{svg:W(cn,{})});case`session`:return W(H,{svg:W(Mn,{})});case`span`:return W(H,{svg:W(qt,{})});case`span_filter`:return W(H,{svg:W(Kt,{})});case`dataset`:return W(H,{svg:W(rn,{})});case`playground`:return W(H,{svg:W(nn,{})});case`code_evaluator`:return W(H,{svg:W(st,{})});case`llm_evaluator`:return W(H,{svg:W(Dt,{})});default:return W(H,{svg:W(zt,{})})}}function dg(e){if(e.type===`context`)return e.icon??ug(e.category);switch(sg(e)){case`image`:return W(H,{svg:W($t,{})});case`video`:return W(H,{svg:W(nn,{})});case`audio`:return W(H,{svg:W(kt,{})});case`document`:return W(H,{svg:W(Ft,{})});case`source`:return W(H,{svg:W(xn,{})});default:return W(H,{svg:W(kt,{})})}}function fg(e){let t=(0,Z.c)(22),n,r,i,a,o;t[0]===e?(n=t[1],r=t[2],i=t[3],a=t[4],o=t[5]):({children:n,ref:a,data:r,onRemove:i,...o}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a,t[5]=o);let{variant:s}=$h(),{theme:c}=vr(),l;t[6]===r?l=t[7]:(l=sg(r),t[6]=r,t[7]=l);let u=l,d;t[8]!==r||t[9]!==u||t[10]!==i||t[11]!==s?(d={data:r,mediaCategory:u,variant:s,onRemove:i},t[8]=r,t[9]=u,t[10]=i,t[11]=s,t[12]=d):d=t[12];let f=d,p;t[13]!==n||t[14]!==a||t[15]!==o||t[16]!==c||t[17]!==s?(p=W(`div`,{ref:a,css:tg,"data-attachment":``,"data-variant":s,"data-theme":c,...o,children:n}),t[13]=n,t[14]=a,t[15]=o,t[16]=c,t[17]=s,t[18]=p):p=t[18];let m;return t[19]!==p||t[20]!==f?(m=W(ag.Provider,{value:f,children:p}),t[19]=p,t[20]=f,t[21]=m):m=t[21],m}function pg(e){let t=(0,Z.c)(16),n,r,i;t[0]===e?(n=t[1],r=t[2],i=t[3]):({ref:r,fallback:n,...i}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i);let{data:a,mediaCategory:o,variant:s}=og(),c;t[4]!==a||t[5]!==n||t[6]!==o?(c=()=>a.type===`file`&&o===`image`&&typeof a.url==`string`&&a.url?W(`img`,{src:a.url,alt:a.filename??`Image`}):a.type===`file`&&o===`video`&&typeof a.url==`string`&&a.url?W(`video`,{src:a.url,muted:!0}):n??dg(a),t[4]=a,t[5]=n,t[6]=o,t[7]=c):c=t[7];let l=c,u;t[8]===l?u=t[9]:(u=l(),t[8]=l,t[9]=u);let d;return t[10]!==o||t[11]!==r||t[12]!==i||t[13]!==u||t[14]!==s?(d=W(`div`,{ref:r,css:ng,"data-variant":s,"data-media-category":o,...i,children:u}),t[10]=o,t[11]=r,t[12]=i,t[13]=u,t[14]=s,t[15]=d):d=t[15],d}function mg(e){let t=(0,Z.c)(28),n,r,i;t[0]===e?(n=t[1],r=t[2],i=t[3]):({ref:n,showMediaType:i,...r}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i);let a=i!==void 0&&i,{data:o,variant:s}=og();if(s===`grid`)return null;let c;t[4]===o?c=t[5]:(c=cg(o),t[4]=o,t[5]=c);let l=c,u,d,f,p,m;t[6]!==o||t[7]!==n?(u=lg(o),d=o.type===`file`||o.type===`source-document`?o.mediaType:void 0,f=n,p=rg,m=B(`attachment-info`,{"attachment-info--with-detail":u}),t[6]=o,t[7]=n,t[8]=u,t[9]=d,t[10]=f,t[11]=p,t[12]=m):(u=t[8],d=t[9],f=t[10],p=t[11],m=t[12]);let h;t[13]===l?h=t[14]:(h=W(`span`,{className:`attachment-info__label`,children:l}),t[13]=l,t[14]=h);let g;t[15]===u?g=t[16]:(g=u?W(`span`,{className:`attachment-info__detail`,children:u}):null,t[15]=u,t[16]=g);let _;t[17]!==d||t[18]!==a?(_=a&&d?W(`span`,{className:`attachment-info__media-type`,children:d}):null,t[17]=d,t[18]=a,t[19]=_):_=t[19];let v;return t[20]!==r||t[21]!==f||t[22]!==p||t[23]!==m||t[24]!==h||t[25]!==g||t[26]!==_?(v=G(`div`,{ref:f,css:p,className:m,...r,children:[h,g,_]}),t[20]=r,t[21]=f,t[22]=p,t[23]=m,t[24]=h,t[25]=g,t[26]=_,t[27]=v):v=t[27],v}var hg=q`
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
`,gg=q`
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
`;function _g(e){let t=(0,Z.c)(27),{selected:n,type:r,label:i,description:a,isFreeformEntry:o,textValue:s,onToggle:c,onTextChange:l}=e,u=(0,X.useRef)(null),d,f;t[0]!==o||t[1]!==n?(d=()=>{n&&o&&u.current&&u.current.focus()},f=[n,o],t[0]=o,t[1]=n,t[2]=d,t[3]=f):(d=t[2],f=t[3]),(0,X.useEffect)(d,f);let p=r===`single`?`option-button__indicator option-button__indicator--radio`:`option-button__indicator option-button__indicator--checkbox`,m;t[4]===Symbol.for(`react.memo_cache_sentinel`)?(m={scale:.98,transition:{type:`tween`,duration:.06}},t[4]=m):m=t[4];let h=r===`single`?`radio`:`checkbox`,g;t[5]===c?g=t[6]:(g=e=>{let t=e.target;t.tagName===`INPUT`||t.tagName===`TEXTAREA`||e.key===`Enter`&&(e.metaKey||e.ctrlKey)||(e.key===`Enter`||e.key===` `)&&(e.preventDefault(),c())},t[5]=c,t[6]=g);let _;t[7]===r?_=t[8]:(_=r===`multi`&&W(`svg`,{viewBox:`0 0 18 18`,"aria-hidden":`true`,children:W(`polyline`,{points:`1 9 7 14 15 4`})}),t[7]=r,t[8]=_);let v;t[9]!==p||t[10]!==_?(v=W(`span`,{className:p,children:_}),t[9]=p,t[10]=_,t[11]=v):v=t[11];let y;t[12]!==a||t[13]!==o||t[14]!==i||t[15]!==l||t[16]!==c||t[17]!==n||t[18]!==s?(y=o?W(`div`,{className:`option-button__text-entry`,onClick:vg,children:W(`input`,{ref:u,type:`text`,className:`option-button__text-input`,value:s||``,placeholder:`Type your own answer…`,onMouseDown:()=>{n||c()},onChange:e=>{n||c(),l?.(e.target.value)},"aria-label":`Type your own answer`})}):G(`div`,{className:`option-button__content`,children:[W(`span`,{className:`option-button__label`,children:i}),a?W(`span`,{className:`option-button__description`,children:a}):null]}),t[12]=a,t[13]=o,t[14]=i,t[15]=l,t[16]=c,t[17]=n,t[18]=s,t[19]=y):y=t[19];let b;return t[20]!==c||t[21]!==n||t[22]!==h||t[23]!==g||t[24]!==v||t[25]!==y?(b=G(we.div,{css:gg,"data-selected":n,onClick:c,whileTap:m,role:h,"aria-checked":n,tabIndex:0,onKeyDown:g,children:[v,y]}),t[20]=c,t[21]=n,t[22]=h,t[23]=g,t[24]=v,t[25]=y,t[26]=b):b=t[26],b}function vg(e){return e.stopPropagation()}var yg=`__freeform__`,bg=.04,xg={enter:e=>({x:e>0?120:-120,opacity:0}),center:{x:0,opacity:1},exit:e=>({x:e>0?-120:120,opacity:0})},Sg={type:`spring`,stiffness:400,damping:32,mass:.8},Cg={type:`spring`,stiffness:700,damping:24,mass:.6};function wg({questions:e,onProgressStateChange:t,onSubmit:n,onCancel:r}){let[i,a]=(0,X.useState)({}),[o,s]=(0,X.useState)({}),[c,l]=(0,X.useState)(0),[u,d]=(0,X.useState)(0),f=(0,X.useRef)(!0),p=(0,X.useEffectEvent)(e=>{t?.(e)}),m=e.length,h=e[c];(0,X.useEffect)(()=>{let e=setTimeout(()=>{f.current=!1},500);return()=>clearTimeout(e)},[]),(0,X.useEffect)(()=>{p({answers:{},freeformTexts:{},currentIndex:0})},[]);let g=e=>{d(e>c?1:-1),l(e),t?.({answers:i,freeformTexts:o,currentIndex:e})},_=(e,t,n)=>{let r=i[e]||[],o;o=n===`single`?r.includes(t)?[]:[t]:r.includes(t)?r.filter(e=>e!==t):[...r,t],a(t=>({...t,[e]:o}))},v=(e,t)=>{a(n=>({...n,[e]:t}))},y=()=>{t?.({answers:i,freeformTexts:o,currentIndex:c}),n({answers:i,freeformTexts:o})},b=()=>{let t=i[e[c].id];((Array.isArray(t)?t.length>0:t)||e[c].allow_skip===!0)&&(c===m-1?y():g(c+1))},x=e=>{if(e.key!==`Enter`||e.nativeEvent.isComposing)return;let t=e.target;if(t.tagName===`TEXTAREA`)return;let n=t.tagName===`INPUT`&&t.type===`text`;(e.metaKey||e.ctrlKey||n)&&(e.preventDefault(),b())},S=e=>{e.key!==`Enter`||e.nativeEvent.isComposing||e.shiftKey||(e.preventDefault(),b())},C=f.current?bg:0,w=C,T=2*C,E=e=>(3+e)*C,D=3*C,O=i[h.id],k=Array.isArray(O)?O.length>0:!!O,A=h.allow_skip===!0,j=k||A;return W(kn,{autoFocus:!0,contain:!0,restoreFocus:!0,children:G(`div`,{css:hg,onKeyDown:x,children:[G(we.div,{className:`elicitation__header`,initial:{opacity:0,y:8},animate:{opacity:1,y:0},transition:{...Cg,delay:w,opacity:{duration:.12,delay:w}},children:[G(`span`,{className:`elicitation__step-label`,children:[`Question `,c+1,` of `,m]}),W(`div`,{className:`elicitation__dots`,children:e.map((e,t)=>W(`button`,{className:`elicitation__dot ${t===c?`elicitation__dot--active`:`elicitation__dot--inactive`}`,onClick:()=>g(t),"aria-label":`Go to question ${t+1}`},t))})]}),W(`div`,{className:`elicitation__body`,children:W(F,{custom:u,mode:`popLayout`,children:G(we.div,{custom:u,variants:xg,initial:!f.current&&`enter`,animate:`center`,exit:`exit`,transition:Sg,className:`elicitation__question-content`,children:[W(we.div,{className:`elicitation__prompt`,initial:{opacity:0,y:-8},animate:{opacity:1,y:0},transition:{...Cg,delay:T,opacity:{duration:.12,delay:T}},children:h.prompt}),h.type===`freeform`?W(we.div,{initial:{opacity:0,y:-8},animate:{opacity:1,y:0},transition:{...Cg,delay:D,opacity:{duration:.12,delay:D}},children:W(`textarea`,{className:`elicitation__freeform`,value:i[h.id]||``,onChange:e=>v(h.id,e.target.value),onKeyDown:S,placeholder:`Type your response… (Enter to submit, Shift+Enter for newline)`,"aria-label":h.prompt})}):G(`div`,{className:`elicitation__options`,children:[h.options?.map((e,t)=>W(we.div,{initial:{opacity:0,y:-8},animate:{opacity:1,y:0},transition:{...Cg,delay:E(t),opacity:{duration:.12,delay:E(t)}},children:W(_g,{selected:(i[h.id]||[]).includes(e.id),type:h.type,label:e.label,description:e.description,onToggle:()=>_(h.id,e.id,h.type)})},e.id)),h.allow_freeform?W(we.div,{initial:{opacity:0,y:-8},animate:{opacity:1,y:0},transition:{...Cg,delay:E(h.options?.length??0),opacity:{duration:.12,delay:E(h.options?.length??0)}},children:W(_g,{selected:(i[h.id]||[]).includes(yg),type:h.type,label:`Type your own answer`,isFreeformEntry:!0,textValue:o[h.id],onToggle:()=>_(h.id,yg,h.type),onTextChange:e=>s(t=>({...t,[h.id]:e}))})},yg):null]})]},h.id)})}),G(we.div,{className:`elicitation__nav`,initial:{opacity:0,y:8},animate:{opacity:1,y:0},transition:{...Cg,delay:0,opacity:{duration:.12,delay:0}},children:[G(`div`,{className:`elicitation__nav-group`,children:[r&&W(yt,{size:`S`,variant:`default`,onPress:r,children:`Cancel`}),W(yt,{size:`S`,variant:`default`,isDisabled:c===0,onPress:()=>g(c-1),children:`Back`})]}),c===m-1?W(yt,{size:`S`,variant:`primary`,isDisabled:!j,onPress:y,children:`Submit`}):W(yt,{size:`S`,variant:k?`primary`:`default`,isDisabled:!j,onPress:()=>g(c+1),children:k?`Next`:`Skip`})]})]})})}var Tg=(0,X.createContext)(null);function Eg(){let e=(0,X.useContext)(Tg);if(!e)throw Error(`usePromptInputContext must be used within a <PromptInput> component`);return e}var Dg=q`
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
`,Og=q`
  flex: 1 1 auto;
  padding: var(--global-dimension-size-200);
  padding-bottom: var(--global-dimension-size-100);
`,kg=q`
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
`,Ag=q`
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--global-dimension-size-100) var(--global-dimension-size-150);
  gap: var(--global-dimension-size-100);
`,jg=q`
  display: flex;
  align-items: center;
  gap: var(--global-dimension-size-50);
`,Mg=q`
  display: flex;
  align-items: center;
  gap: var(--global-dimension-size-50);
`,Ng=q`
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
`;function Pg({children:e,ref:t,onSubmit:n,status:r=`ready`,isDisabled:i=!1,mode:a=`prompt`,value:o,onValueChange:s,...c}){let[l,u]=(0,X.useState)(``),d=o!==void 0,f=d?o:l,p=e=>{d||u(e),s?.(e)},m=(0,X.useRef)(f);m.current=f;let h={status:r,isDisabled:i,onSubmit:()=>{if(r===`submitted`||r===`streaming`)return;let e=m.current.trim();e&&(n?.(e),p(``))},value:f,setValue:p};return W(Tg.Provider,{value:h,children:W(`div`,{ref:t,css:Dg,"data-status":r,"data-input-mode":a,...c,children:e})})}function Fg(e){let t=(0,Z.c)(8),n,r,i;t[0]===e?(n=t[1],r=t[2],i=t[3]):({children:n,ref:r,...i}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i);let a;return t[4]!==n||t[5]!==r||t[6]!==i?(a=W(`div`,{ref:r,css:Og,...i,children:n}),t[4]=n,t[5]=r,t[6]=i,t[7]=a):a=t[7],a}function Ig(e){let t=(0,Z.c)(8),n,r,i;t[0]===e?(n=t[1],r=t[2],i=t[3]):({children:n,ref:r,...i}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i);let a;return t[4]!==n||t[5]!==r||t[6]!==i?(a=W(`div`,{ref:r,css:Ag,...i,children:n}),t[4]=n,t[5]=r,t[6]=i,t[7]=a):a=t[7],a}function Lg(e){let t=(0,Z.c)(8),n,r,i;t[0]===e?(n=t[1],r=t[2],i=t[3]):({children:n,ref:r,...i}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i);let a;return t[4]!==n||t[5]!==r||t[6]!==i?(a=W(`div`,{ref:r,css:jg,role:`toolbar`,...i,children:n}),t[4]=n,t[5]=r,t[6]=i,t[7]=a):a=t[7],a}function Rg(e){let t=(0,Z.c)(8),n,r,i;t[0]===e?(n=t[1],r=t[2],i=t[3]):({children:n,ref:r,...i}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i);let a;return t[4]!==n||t[5]!==r||t[6]!==i?(a=W(`div`,{ref:r,css:Mg,...i,children:n}),t[4]=n,t[5]=r,t[6]=i,t[7]=a):a=t[7],a}function zg(e){let t=(0,Z.c)(20),{ref:n,placeholder:r,value:i,onChange:a,maxRows:o,"aria-label":s,className:c}=e,l=r===void 0?`Send a message...`:r,u=s===void 0?`Message input`:s,d=Eg(),f=(0,X.useRef)(null),p=i===void 0?d.value:i,m=a===void 0?d.setValue:a,h;t[0]===n?h=t[1]:(h=e=>{f.current=e,typeof n==`function`?n(e):n&&`current`in n&&(n.current=e)},t[0]=n,t[1]=h);let g=h,_;t[2]===o?_=t[3]:(_=()=>{let e=f.current;if(!e)return;let t=()=>{e.style.height=`auto`;let t=e.scrollHeight;if(o){let n=parseInt(getComputedStyle(e).lineHeight||`20`,10)*o;t=Math.min(t,n)}e.style.height=`${t}px`};t();let n=requestAnimationFrame(t);return()=>{cancelAnimationFrame(n)}},t[2]=o,t[3]=_);let v;t[4]!==o||t[5]!==p?(v=[p,o],t[4]=o,t[5]=p,t[6]=v):v=t[6],(0,X.useLayoutEffect)(_,v);let{onSubmit:y}=d,b;t[7]===y?b=t[8]:(b=e=>{e.key===`Enter`&&!e.shiftKey&&(e.preventDefault(),y())},t[7]=y,t[8]=b);let x=b,S;t[9]===m?S=t[10]:(S=e=>{m(e.target.value)},t[9]=m,t[10]=S);let C=S,w;return t[11]!==u||t[12]!==c||t[13]!==d.isDisabled||t[14]!==C||t[15]!==x||t[16]!==g||t[17]!==l||t[18]!==p?(w=W(`textarea`,{ref:g,css:kg,className:c,value:p,onChange:C,onKeyDown:x,placeholder:l,disabled:d.isDisabled,"aria-label":u,rows:1}),t[11]=u,t[12]=c,t[13]=d.isDisabled,t[14]=C,t[15]=x,t[16]=g,t[17]=l,t[18]=p,t[19]=w):w=t[19],w}function Bg(e){let t=(0,Z.c)(15),{ref:n,onPress:r,isDisabled:i,"aria-label":a,className:o}=e,s=Eg(),c=s.status===`submitted`||s.status===`streaming`,l;t[0]===s.value?l=t[1]:(l=s.value.trim(),t[0]=s.value,t[1]=l);let u=l===``,d=i??(s.status===`ready`&&u),f=!c,p=a??(f?`Send message`:`Stop generation`),m;t[2]!==s||t[3]!==c||t[4]!==r?(m=()=>{if(c){r?.();return}s.onSubmit()},t[2]=s,t[3]=c,t[4]=r,t[5]=m):m=t[5];let h=m,g=d||s.isDisabled,_;t[6]===f?_=t[7]:(_=W(H,{svg:W(f?Be:wn,{})}),t[6]=f,t[7]=_);let v;return t[8]!==o||t[9]!==p||t[10]!==h||t[11]!==n||t[12]!==g||t[13]!==_?(v=W(Et,{ref:n,css:Ng,className:o,isDisabled:g,onPress:h,"aria-label":p,children:_}),t[8]=o,t[9]=p,t[10]=h,t[11]=n,t[12]=g,t[13]=_,t[14]=v):v=t[14],v}q`
  display: flex;
  align-items: center;
  gap: var(--global-dimension-size-75);
`;var Vg=q`
  ${an};
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
`,Hg=new Map,Ug=e=>{let t=Hg.get(e);if(t)return t;let n=we.create(e);return Hg.set(e,n),n};function Wg(e){let t=(0,Z.c)(37),n,r,i,a,o,s,c,l,u,d,f,p;t[0]===e?(n=t[1],r=t[2],i=t[3],a=t[4],o=t[5],s=t[6],c=t[7],l=t[8],u=t[9],d=t[10],f=t[11],p=t[12]):({ref:i,children:n,elementType:s,size:c,weight:l,color:u,fontStyle:d,duration:f,spread:p,className:r,style:o,...a}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a,t[5]=o,t[6]=s,t[7]=c,t[8]=l,t[9]=u,t[10]=d,t[11]=f,t[12]=p);let m=s===void 0?`p`:s,h=c===void 0?`S`:c,g=l===void 0?`normal`:l,_=u===void 0?`text-700`:u,v=d===void 0?`normal`:d,y=f===void 0?2:f,b=p===void 0?2:p,x=ue(),S=m,C;t[13]===S?C=t[14]:(C=Ug(S),t[13]=S,t[14]=C);let w=C,T=(n?.length??0)*b,E;t[15]!==y||t[16]!==x?(E=x?{}:{initial:{backgroundPosition:`100% center`},animate:{backgroundPosition:`0% center`},transition:{duration:y,ease:`linear`,repeat:1/0}},t[15]=y,t[16]=x,t[17]=E):E=t[17];let D=E,O=i,k;t[18]===r?k=t[19]:(k=B(`shimmer`,r),t[18]=r,t[19]=k);let A=`${T}px`,j;t[20]===_?j=t[21]:(j=vt(_),t[20]=_,t[21]=j);let M;t[22]!==v||t[23]!==o||t[24]!==A||t[25]!==j?(M={"--shimmer-spread":A,"--shimmer-color":j,fontStyle:v,...o},t[22]=v,t[23]=o,t[24]=A,t[25]=j,t[26]=M):M=t[26];let N=M,P=a,F;return t[27]!==w||t[28]!==D||t[29]!==n||t[30]!==h||t[31]!==O||t[32]!==k||t[33]!==N||t[34]!==P||t[35]!==g?(F=W(w,{ref:O,className:k,"data-size":h,"data-weight":g,css:Vg,style:N,...D,...P,children:n}),t[27]=w,t[28]=D,t[29]=n,t[30]=h,t[31]=O,t[32]=k,t[33]=N,t[34]=P,t[35]=g,t[36]=F):F=t[36],F}Wg.displayName=`Shimmer`;var Gg=(0,X.createContext)(null);function Kg(){return(0,X.useContext)(Gg)}function qg(e){let t=e.parentElement;for(;t;){let{overflowY:e}=getComputedStyle(t);if((e===`auto`||e===`scroll`)&&t.scrollHeight>t.clientHeight)return t;t=t.parentElement}return null}function Jg(){let e=(0,Z.c)(5),t=Kg(),n=(0,X.useRef)(null),r;e[0]===t?r=e[1]:(r=e=>{if(t?.stopScroll(),n.current=null,!e)return;let r=qg(e);if(!r)return;let i=e.getBoundingClientRect(),a=r.getBoundingClientRect();n.current={scrollParent:r,offsetFromParentTop:i.top-a.top}},e[0]=t,e[1]=r);let i=r,a;e[2]===Symbol.for(`react.memo_cache_sentinel`)?(a=e=>{let t=n.current;if(n.current=null,!t||!e)return;let{scrollParent:r,offsetFromParentTop:i}=t,a=e.getBoundingClientRect(),o=r.getBoundingClientRect(),s=a.top-o.top;r.scrollTop+=s-i},e[2]=a):a=e[2];let o=a,s;return e[3]===i?s=e[4]:(s={capture:i,restore:o},e[3]=i,e[4]=s),s}var Yg=Ke`
  from {
    opacity: 0;
    transform: translateY(-2px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
`,Xg={titleFlex:`0 1 auto`,titleMinWidth:`0`,titleMaxWidth:`55%`,middleFlex:`1 1 50px`,middleMinWidth:`50px`,statusFlex:`0 1 auto`,statusMinWidth:`0`,statusMaxWidth:`none`};function Zg(e){let t=(0,Z.c)(3),{children:n,variant:r}=e,i;return t[0]!==n||t[1]!==r?(i=W(`div`,{className:`tool-part__line`,children:W(`span`,{className:`tool-part__label`,"data-variant":r,children:n})}),t[0]=n,t[1]=r,t[2]=i):i=t[2],i}function Qg(e){let t=(0,Z.c)(9),{children:n,allowCopy:r}=e,i=r===void 0||r,a=`tool-part__line${i?` tool-part__line--copyable`:``}`,o=n||`(empty)`,s;t[0]===o?s=t[1]:(s=W(`code`,{className:`tool-part__code`,children:o}),t[0]=o,t[1]=s);let c;t[2]!==i||t[3]!==n?(c=i?W(da,{text:n,size:`S`,variant:`quiet`,tooltipText:`Copy`}):null,t[2]=i,t[3]=n,t[4]=c):c=t[4];let l;return t[5]!==a||t[6]!==s||t[7]!==c?(l=G(`div`,{className:a,children:[s,c]}),t[5]=a,t[6]=s,t[7]=c,t[8]=l):l=t[8],l}function $g(e){let t=(0,Z.c)(3),{children:n,variant:r}=e,i;return t[0]!==n||t[1]!==r?(i=W(`span`,{className:`tool-part__status`,"data-variant":r,children:n}),t[0]=n,t[1]=r,t[2]=i):i=t[2],i}function e_(e){let t=(0,Z.c)(4),{items:n}=e,r;t[0]===n?r=t[1]:(r=n.map(t_),t[0]=n,t[1]=r);let i;return t[2]===r?i=t[3]:(i=W(`div`,{className:`tool-part__meta`,children:r}),t[2]=r,t[3]=i),i}function t_(e){let{label:t,value:n}=e;return G(`span`,{className:`tool-part__meta-group`,children:[W(`span`,{className:`tool-part__meta-label`,children:t}),W(`code`,{className:`tool-part__meta-value`,children:n})]},t)}var n_=q`
  padding: var(--global-dimension-size-50) var(--global-dimension-size-200)
    var(--global-dimension-size-150);
`;function r_(e){let t=(0,Z.c)(15),{onAccept:n,onReject:r,isDisabled:i,staleMessage:a}=e,o=i!==void 0&&i,s;t[0]!==o||t[1]!==n?(s=W(yt,{size:`S`,variant:`primary`,isDisabled:o,onPress:n,children:`Accept`}),t[0]=o,t[1]=n,t[2]=s):s=t[2];let c;t[3]!==o||t[4]!==r?(c=W(yt,{size:`S`,isDisabled:o,onPress:r,children:`Reject`}),t[3]=o,t[4]=r,t[5]=c):c=t[5];let l;t[6]!==s||t[7]!==c?(l=W(`div`,{css:n_,children:G(K,{direction:`row-reverse`,gap:`size-100`,children:[s,c]})}),t[6]=s,t[7]=c,t[8]=l):l=t[8];let u;t[9]!==o||t[10]!==a?(u=o&&a?W(Qg,{children:a}):null,t[9]=o,t[10]=a,t[11]=u):u=t[11];let d;return t[12]!==l||t[13]!==u?(d=G(U,{children:[l,u]}),t[12]=l,t[13]=u,t[14]=d):d=t[14],d}var i_=320,a_=q`
  --expandable-content-overlay-background-color: var(
    --tool-call-body-background-color
  );
`;function o_(e){let t=(0,Z.c)(6),{children:n}=e,r=(0,X.useRef)(null),[i,a]=(0,X.useState)(!1),o=Jg(),s;t[0]===o?s=t[1]:(s=e=>{o.capture(r.current),a(e),requestAnimationFrame(()=>o.restore(r.current))},t[0]=o,t[1]=s);let c=s,l;return t[2]!==n||t[3]!==c||t[4]!==i?(l=W(`div`,{ref:r,css:a_,children:W(Je,{height:i_,expandedBehavior:`grow`,isExpanded:i,onExpandedChange:c,children:n})}),t[2]=n,t[3]=c,t[4]=i,t[5]=l):l=t[5],l}function s_(e){switch(e){case`input-streaming`:return`Preparing`;case`input-available`:return`Running`;case`approval-requested`:return`Awaiting approval`;case`approval-responded`:return`Approval received`;case`output-available`:return`Completed`;case`output-error`:return`Error`;case`output-denied`:return`Denied`;default:return Yn(e)}}function c_(e){if(e==null)return``;if(typeof e==`string`)return e;try{return JSON.stringify(e,null,2)}catch{return String(e)}}export{Am as $,kr as $i,ps as $n,Ji as $r,Wl as $t,Ah as A,di as Ai,dc as An,Na as Ar,Q as At,ch as B,Xr as Bi,Vs as Bn,ga as Br,zu as Bt,wg as C,gi as Ci,kc as Cn,Ja as Cr,Jf as Ct,ig as D,Ci as Di,Tc as Dn,Ba as Dr,Zf as Dt,fg as E,wi as Ei,Cc as En,Va as Er,Qf as Et,Sh as F,oi as Fi,oc as Fn,ma as Fr,Nd as Ft,ih as G,Ur as Gi,js as Gn,aa as Gr,ku as Gt,ph as H,qr as Hi,Ls as Hn,pa as Hr,Mu as Ht,bh as I,si as Ii,$s as In,ya as Ir,Md as It,Km as J,Ir as Ji,ws as Jn,oa as Jr,yu as Jt,rh as K,Hr as Ki,Ds as Kn,ca as Kr,Ou as Kt,vh as L,ci as Li,Zs as Ln,wa as Lr,Ad as Lt,Oh as M,ai as Mi,lc as Mn,Aa as Mr,Bd as Mt,Dh as N,ni as Ni,rc as Nn,Da as Nr,zd as Nt,Zh as O,xi as Oi,bc as On,Ia as Or,zf as Ot,Eh as P,ui as Pi,ic as Pn,Oa as Pr,Pd as Pt,Wm as Q,jr as Qi,ys as Qn,Zi as Qr,Ul as Qt,_h as R,ri as Ri,Ys as Rn,Sa as Rr,kd as Rt,Eg as S,pi as Si,Ic as Sn,Za as Sr,Ff as St,pg as T,vi as Ti,Oc as Tn,Wa as Tr,Rf as Tt,sh as U,Gr as Ui,Fs as Un,Ta as Ur,Nu as Ut,mh as V,Zr as Vi,zs as Vn,xa as Vr,Au as Vt,oh as W,Vr as Wi,Ns as Wn,da as Wr,ju as Wt,Hm as X,Lr as Xi,Ss as Xn,ra as Xr,lu as Xt,qm as Y,Mr as Yi,Cs as Yn,ia as Yr,du as Yt,Um as Z,Rr as Zi,xs as Zn,ta as Zr,cu as Zt,Rg as _,_i,Gc as _n,Oo as _r,Yf as _t,r_ as a,vr as aa,Bi as ai,Sl as an,es as ar,_m as at,Fg as b,hi as bi,Hc as bn,fo as br,Lf as bt,Zg as c,sr as ca,zi as ci,hl as cn,Yo as cr,mm as ct,qg as d,Xn as da,Ni as di,ll as dn,zo as dr,hm as dt,Ar as ea,Hi as ei,Gl as en,fs as er,km as et,Jg as f,er as fa,Mi as fi,cl as fn,Ro as fr,vm as ft,zg as g,nr as ga,Ti as gi,Xc as gn,No as gr,qf as gt,Bg as h,Qn as ha,Ei as hi,nl as hn,Fo as hr,Kf as ht,Yg as i,dr as ia,Ki as ii,Tl as in,is as ir,um as it,kh as j,ii as ji,pc as jn,Ma as jr,tf as jt,Xh as k,Si as ki,_c as kn,Pa as kr,Wf as kt,e_ as l,or as la,Ri as li,pl as ln,Xo as lr,pm as lt,Wg as m,tr as ma,Di as mi,il as mn,Vo as mr,Bf as mt,c_ as n,xr as na,Vi as ni,Fl as nn,ss as nr,Bm as nt,Qg as o,ir as oa,qi as oi,yl as on,Qo as or,fm as ot,Gg as p,$n as pa,ki as pi,ol as pn,Bo as pr,ep as pt,Ym as q,Wr as qi,ks as qn,sa as qr,Tu as qt,Xg as r,yr as ra,Wi as ri,Ml as rn,os as rr,ym as rt,o_ as s,ar as sa,Gi as si,_l as sn,Zo as sr,dm as st,s_ as t,Sr as ta,Yi as ti,Il as tn,ls as tr,Om as tt,$g as u,Yn as ua,Fi as ui,dl as un,Ho as ur,gm as ut,Lg as v,bi as vi,Wc as vn,Eo as vr,Gf as vt,mg as w,fi as wi,Ec as wn,Ga as wr,Xf as wt,Pg as x,mi as xi,Lc as xn,co as xr,If as xt,Ig as y,yi,Uc as yn,Co as yr,Vf as yt,gh as z,li as zi,qs as zn,Ca as zr,Ru as zt};