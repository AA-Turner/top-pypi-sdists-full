import{s as e}from"./rolldown-runtime-BG2f4sTM.js";import{$n as t,$t as n,An as r,Bn as i,Bt as a,Cn as o,Dn as s,En as c,Fn as l,Gn as u,Gt as d,Hn as f,Ht as p,In as m,Jn as h,Jt as g,Kn as _,Ln as v,Nn as y,On as b,Pn as x,Qn as S,Rn as C,Sn as w,Tn as T,Un as E,Vt as D,Wt as O,Xt as k,Yn as A,Yt as j,Zn as M,Zt as N,_n as P,_t as F,an as I,ar as L,bn as ee,bt as R,cn as te,cr as ne,dn as re,dt as ie,en as ae,er as oe,fn as se,ft as ce,gn as le,hn as ue,ht as de,ir as fe,it as pe,kn as me,ln as he,lr as ge,mn as _e,mt as ve,nn as ye,nt as be,on as xe,or as Se,pn as Ce,pr as we,qn as Te,qt as Ee,rn as De,rr as Oe,rt as ke,sn as Ae,sr as je,tn as Me,tr as Ne,vn as Pe,wn as Fe,xt as Ie,zn as Le}from"./vendor-CgFfs1Xx.js";import{et as Re}from"./vendor-codemirror-BTy1OBzQ.js";import{S as z,y as ze}from"./vendor-recharts-oGxA8ozY.js";import{$ as Be,$n as Ve,A as He,Aa as Ue,An as We,Bi as Ge,Br as Ke,C as qe,D as B,Dn as Je,Dt as Ye,E as Xe,Ei as Ze,Et as Qe,F as $e,G as V,Gr as et,Gt as tt,H as nt,Ht as rt,In as it,J as at,Jr as ot,Jt as st,K as ct,Kn as lt,Kr as ut,Kt as dt,L as ft,M as pt,Mn as mt,Mo as H,No as U,Nt as ht,O as gt,P as W,Pn as _t,Po as vt,R as yt,Ri as bt,Rt as xt,So as St,T as Ct,Tt as wt,Ui as Tt,Un as Et,Ut as Dt,Va as Ot,Vr as kt,Vt as At,W as jt,Wn as Mt,Wt as Nt,Xt as Pt,Y as Ft,Zr as It,_t as Lt,ai as Rt,ar as zt,at as Bt,bn as Vt,bt as Ht,ci as Ut,cn as Wt,ea as Gt,fr as Kt,gn as qt,gr as Jt,gt as Yt,i as Xt,ia as Zt,j as Qt,ja as $t,jn as en,jo as G,k as tn,ki as nn,la as rn,ln as an,lr as on,m as sn,mn as cn,mr as ln,on as un,p as dn,pr as fn,q as pn,qi as mn,qr as hn,qt as gn,ri as _n,sn as vn,ta as yn,tr as bn,un as xn,ut as Sn,vt as Cn,wi as wn,x as Tn,xi as En,xn as Dn,xt as On,y as kn,yn as An,yr as jn,z as K,za as Mn,zr as q}from"./vendor-streamdown-u9LXYtNJ.js";import{Ft as Nn,Hn as Pn,Nn as J,Ot as Fn,Pn as In,Yt as Ln,ar as Rn,bn as zn,or as Bn,qn as Y,s as Vn,xn as Hn,zt as Un}from"./vendor-ai-sdk-react-Cd-QT6XP.js";var X=e(Re()),Z=vt();function Wn(e){throw Error(`Unreachable`)}function Gn(e){return typeof e==`number`||e===null}function Kn(e){return typeof e==`string`||e===null}function qn(e){return Kn(e)||e===void 0}function Jn(e){return Array.isArray(e)?e.every(e=>typeof e==`string`):!1}function Yn(e){return typeof e==`object`&&!!e}function Xn(e){return Yn(e)&&Object.keys(e).every(e=>typeof e==`string`)}var Zn=()=>e=>e;(0,X.createContext)(null);var Qn=5e3,$n=new ye({maxVisibleToasts:3}),er=()=>rr,tr=()=>ir,nr=()=>ar;function rr(e){let{expireMs:t,...n}=e,r=t===void 0?Qn:t;return $n.add({...n},r===null?void 0:{timeout:r})}function ir(e){let{expireMs:t,...n}=e,r=t===void 0?Qn:t;return $n.add({...n,variant:`success`},r===null?void 0:{timeout:r})}function ar(e){let{expireMs:t,...n}=e,r=t===void 0?Qn:t;return $n.add({...n,variant:`error`},r===null?void 0:{timeout:r})}function or(e){return e===`light`||e===`dark`||e===`system`}var sr=`arize-phoenix-theme`,cr=`dark`,lr=`(prefers-color-scheme: dark)`;function ur(){let e=localStorage.getItem(sr);return or(e)?e:cr}function dr(){return window.matchMedia(lr).matches?`dark`:`light`}var fr=(0,X.createContext)(null);function pr(){let e=(0,X.useContext)(fr);if(e===null)throw Error(`useTheme must be used within a ThemeProvider`);return e}function mr(e){let t=(0,Z.c)(19),n;t[0]===e.themeMode?n=t[1]:(n=()=>e.themeMode||ur(),t[0]=e.themeMode,t[1]=n);let[r,i]=(0,X.useState)(n),a;t[2]===Symbol.for(`react.memo_cache_sentinel`)?(a=e=>{localStorage.setItem(sr,e),i(e)},t[2]=a):a=t[2];let o=a,[s,c]=(0,X.useState)(dr),l;bb0:{if(r===`system`){l=s;break bb0}l=r}let u=l,d,f;t[3]===e.themeMode?(d=t[4],f=t[5]):(d=()=>{e.themeMode&&i(e.themeMode)},f=[e.themeMode,o],t[3]=e.themeMode,t[4]=d,t[5]=f),(0,X.useEffect)(d,f);let p,m;t[6]===Symbol.for(`react.memo_cache_sentinel`)?(p=()=>{let e=window.matchMedia(lr),t=()=>{c(dr())};return e.addEventListener(`change`,t),()=>{e.removeEventListener(`change`,t)}},m=[],t[6]=p,t[7]=m):(p=t[6],m=t[7]),(0,X.useEffect)(p,m);let h,g;t[8]!==e.disableBodyTheme||t[9]!==u?(h=()=>{if(!e.disableBodyTheme)return document.body.classList.add(`theme--${u}`),document.body.classList.add(`theme`),()=>{document.body.classList.remove(`theme--${u}`),document.body.classList.remove(`theme`)}},g=[u,e.disableBodyTheme],t[8]=e.disableBodyTheme,t[9]=u,t[10]=h,t[11]=g):(h=t[10],g=t[11]),(0,X.useEffect)(h,g);let _;t[12]!==s||t[13]!==u||t[14]!==r?(_={theme:u,systemTheme:s,themeMode:r,setThemeMode:o},t[12]=s,t[13]=u,t[14]=r,t[15]=_):_=t[15];let v;return t[16]!==e.children||t[17]!==_?(v=H(fr.Provider,{value:_,children:e.children}),t[16]=e.children,t[17]=_,t[18]=v):v=t[18],v}var hr=[`traces`,`spans`,`sessions`,`metrics`],gr=e=>hr.includes(e),_r=[`traffic`,`traces`,`latency`,`cost`,`top_models_by_cost`,`tokens`,`top_models_by_tokens`,`prompt_token_details`,`completion_token_details`,`llm_spans`,`llm_span_errors`,`tool_spans`,`tool_span_errors`,`span_annotations`,`trace_annotations`,`session_annotations`],vr=e=>_r.includes(e),yr=[`spans`,`traces`,`sessions`],br={spans:[`traffic`],traces:[`traces`,`latency`,`trace_annotations`],sessions:[`traces`,`session_annotations`]},xr=e=>`arize-phoenix-project-${e}`;function Sr({projectId:e}){return{state:p()(D(a(e=>({defaultTab:`spans`,setDefaultTab:t=>{e({defaultTab:t},!1,{type:`setDefaultTab`})},treatOrphansAsRoots:!1,setTreatOrphansAsRoots:t=>{e({treatOrphansAsRoots:t},!1,{type:`setTreatOrphansAsRoots`})},showTableAside:!0,setShowTableAside:t=>{e({showTableAside:t},!1,{type:`setShowTableAside`})},metricChartKeys:br,setMetricChartKeys:(t,n)=>{e(e=>({metricChartKeys:{...e.metricChartKeys,[t]:n}}),!1,{type:`setMetricChartKeys`})}})),{name:xr(e),merge:(e,t)=>{let n={...t,...e},r={...br};for(let e of yr){let t=n.metricChartKeys?.[e];Array.isArray(t)&&(r[e]=t.filter(vr).slice(0,3))}return n.metricChartKeys=r,n}}))}}var Cr=(0,X.createContext)(null);function wr(e){let t=(0,Z.c)(5),{children:n,projectId:r}=e,i;t[0]===r?i=t[1]:(i=()=>Sr({projectId:r}),t[0]=r,t[1]=i);let[a]=(0,X.useState)(i),o;return t[2]!==n||t[3]!==a?(o=H(Cr.Provider,{value:a,children:n}),t[2]=n,t[3]=a,t[4]=o):o=t[4],o}function Tr(e,t){let n=(0,X.useContext)(Cr);if(!n)throw Error(`Missing ProjectContext.Provider in the tree`);return O(n.state,e,t)}var Er=[`Python`,`TypeScript`];function Dr(e){return typeof e==`string`&&Er.includes(e)}var Or=[`npm`,`pnpm`,`bun`],kr=[`pip`,`uv`],Ar=[...Or,...kr];function jr(e){return typeof e==`string`&&Ar.includes(e)}function Mr(e){return typeof e==`string`&&kr.includes(e)}function Nr(e){return typeof e==`string`&&Or.includes(e)}var Pr=Intl.DateTimeFormat().resolvedOptions(),Fr=[];function Ir(){return Pr.locale}function Lr(){return Pr.timeZone}function Rr(){return Fr.length===0&&(Fr=[...Intl.supportedValuesOf(`timeZone`)],Fr.includes(`UTC`)||(Fr=[`UTC`,...Fr])),Object.freeze([...Fr])}function zr(e,t){let n=new Intl.DateTimeFormat(`en-US`,{timeZone:t,year:`numeric`,month:`2-digit`,day:`2-digit`,hour:`2-digit`,minute:`2-digit`,second:`2-digit`,hour12:!1}).formatToParts(e).reduce((e,t)=>(t.type!==`literal`&&(e[t.type]=t.value),e),{}),{year:r,month:i,day:a}=n,o=n.hour;if(o===`24`){o=`00`;let e=new Date(`${r}-${i}-${a}T00:00:00Z`);e.setUTCDate(e.getUTCDate()+1),r=String(e.getUTCFullYear()),i=String(e.getUTCMonth()+1).padStart(2,`0`),a=String(e.getUTCDate()).padStart(2,`0`)}let s=`${r}-${i}-${a}`,c=`${o}:${n.minute}:${n.second}`,l=new Date(`${s}T${c}Z`).getTime(),u=Math.round((l-e.getTime())/6e4),d=u>=0?`+`:`-`,f=Math.abs(u);return`${s}T${c}${d}${String(Math.floor(f/60)).padStart(2,`0`)}:${String(f%60).padStart(2,`0`)}`}var Br={Python:kr,TypeScript:Or},Vr={Python:`pip`,TypeScript:`npm`},Hr=[``,`apac`,`au`,`ca`,`eu`,`global`,`il`,`jp`,`us`,`us-gov`],Ur=e=>p()(D(a(t=>({markdownDisplayMode:`text`,setMarkdownDisplayMode:e=>{t({markdownDisplayMode:e},!1,{type:`setMarkdownDisplayMode`})},traceStreamingEnabled:!0,setTraceStreamingEnabled:e=>{t({traceStreamingEnabled:e},!1,{type:`setTraceStreamingEnabled`})},lastNTimeRangeKey:`7d`,setLastNTimeRangeKey:e=>{t({lastNTimeRangeKey:e})},projectsAutoRefreshEnabled:!0,setProjectAutoRefreshEnabled:e=>{t({projectsAutoRefreshEnabled:e},!1,{type:`setProjectAutoRefreshEnabled`})},showMetricsInTraceTree:!0,setShowMetricsInTraceTree:e=>{t({showMetricsInTraceTree:e},!1,{type:`setShowMetricsInTraceTree`})},modelConfigByProvider:{},setModelConfigForProvider:({provider:e,modelConfig:n})=>{t(t=>({modelConfigByProvider:{...t.modelConfigByProvider,[e]:n}}),!1,{type:`setModelConfigForProvider`})},playgroundStreamingEnabled:!0,setPlaygroundStreamingEnabled:e=>{t({playgroundStreamingEnabled:e},!1,{type:`setPlaygroundStreamingEnabled`})},isAnnotatingSpans:!1,setIsAnnotatingSpans:e=>{t({isAnnotatingSpans:e},!1,{type:`setIsAnnotatingSpans`})},projectViewMode:`grid`,setProjectViewMode:e=>{t({projectViewMode:e},!1,{type:`setProjectViewMode`})},projectSortOrder:{column:`endTime`,direction:`desc`},setProjectSortOrder:e=>{t({projectSortOrder:e},!1,{type:`setProjectSortOrder`})},lastSelectedDashboardProjectId:void 0,setLastSelectedDashboardProjectId:e=>{t({lastSelectedDashboardProjectId:e},!1,{type:`setLastSelectedDashboardProjectId`})},isSideNavExpanded:!0,setIsSideNavExpanded:e=>{t({isSideNavExpanded:e},!1,{type:`setIsSideNavExpanded`})},setDisplayTimezone:e=>{if(e&&!Rr().includes(e))throw Error(`Invalid timezone: ${e}`);t({displayTimezone:e},!1,{type:`setDisplayTimezone`})},programmingLanguage:`Python`,setProgrammingLanguage:e=>{t({programmingLanguage:e},!1,{type:`setProgrammingLanguage`})},packageManagerByLanguage:{...Vr},setPackageManager:(e,n)=>{t(t=>({packageManagerByLanguage:{...t.packageManagerByLanguage,[e]:n}}),!1,{type:`setPackageManager`})},awsBedrockModelPrefix:`us`,setAwsBedrockModelPrefix:e=>{t({awsBedrockModelPrefix:e},!1,{type:`setAwsBedrockModelPrefix`})},isAssistantAgentEnabled:!0,setIsAssistantAgentEnabled:e=>{t({isAssistantAgentEnabled:e},!1,{type:`setIsAssistantAgentEnabled`})},defaultModelProvider:void 0,setDefaultModelProvider:e=>{t({defaultModelProvider:e},!1,{type:`setDefaultModelProvider`})},defaultModelName:void 0,setDefaultModelName:e=>{let n=e?.trim();t({defaultModelName:n||void 0},!1,{type:`setDefaultModelName`})},...e}),{name:`preferencesStore`}),{name:`arize-phoenix-preferences`})),Wr=(0,X.createContext)(null);function Gr(e){let t=(0,Z.c)(8),n,r;t[0]===e?(n=t[1],r=t[2]):({children:n,...r}=e,t[0]=e,t[1]=n,t[2]=r);let i;t[3]===r?i=t[4]:(i=()=>Ur(r),t[3]=r,t[4]=i);let[a]=(0,X.useState)(i),o;return t[5]!==n||t[6]!==a?(o=H(Wr.Provider,{value:a,children:n}),t[5]=n,t[6]=a,t[7]=o):o=t[7],o}function Kr(e,t){let n=(0,X.useContext)(Wr);if(!n)throw Error(`Missing PreferencesContext.Provider in the tree`);return O(n,e,t)}var qr=function(){var e={alias:null,args:null,kind:`ScalarField`,name:`id`,storageKey:null},t={alias:null,args:null,kind:`ScalarField`,name:`name`,storageKey:null},n={alias:null,args:null,kind:`ScalarField`,name:`createdAt`,storageKey:null},r={alias:null,args:null,kind:`ScalarField`,name:`expiresAt`,storageKey:null};return{fragment:{argumentDefinitions:[],kind:`Fragment`,metadata:null,name:`ViewerContextRefetchQuery`,selections:[{args:null,kind:`FragmentSpread`,name:`ViewerContext_viewer`}],type:`Query`,abstractKey:null},kind:`Request`,operation:{argumentDefinitions:[],kind:`Operation`,name:`ViewerContextRefetchQuery`,selections:[{alias:null,args:null,concreteType:`User`,kind:`LinkedField`,name:`viewer`,plural:!1,selections:[e,{alias:null,args:null,kind:`ScalarField`,name:`username`,storageKey:null},{alias:null,args:null,kind:`ScalarField`,name:`email`,storageKey:null},{alias:null,args:null,kind:`ScalarField`,name:`profilePictureUrl`,storageKey:null},{alias:null,args:null,kind:`ScalarField`,name:`isManagementUser`,storageKey:null},{alias:null,args:null,concreteType:`UserRole`,kind:`LinkedField`,name:`role`,plural:!1,selections:[t,e],storageKey:null},{alias:null,args:null,kind:`ScalarField`,name:`authMethod`,storageKey:null},{alias:null,args:null,concreteType:`UserApiKey`,kind:`LinkedField`,name:`apiKeys`,plural:!0,selections:[e,t,{alias:null,args:null,kind:`ScalarField`,name:`description`,storageKey:null},n,r],storageKey:null},{alias:null,args:null,concreteType:`OAuth2Grant`,kind:`LinkedField`,name:`oauth2Grants`,plural:!0,selections:[e,{alias:null,args:null,kind:`ScalarField`,name:`clientName`,storageKey:null},{alias:null,args:null,kind:`ScalarField`,name:`clientId`,storageKey:null},{alias:null,args:null,kind:`ScalarField`,name:`isFirstParty`,storageKey:null},{alias:null,args:null,kind:`ScalarField`,name:`scopes`,storageKey:null},n,r,{alias:null,args:null,kind:`ScalarField`,name:`lastUsedAt`,storageKey:null}],storageKey:null}],storageKey:null}]},params:{cacheID:`67fdf1bb616d5781701a75f68282f178`,id:null,metadata:{},name:`ViewerContextRefetchQuery`,operationKind:`query`,text:`query ViewerContextRefetchQuery {
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
`}}}();qr.hash=`53341d080ff76da24b2f1bc9e36c4e23`;var Jr={argumentDefinitions:[],kind:`Fragment`,metadata:{refetch:{connection:null,fragmentPathInResult:[],operation:qr}},name:`ViewerContext_viewer`,selections:[{alias:null,args:null,concreteType:`User`,kind:`LinkedField`,name:`viewer`,plural:!1,selections:[{alias:null,args:null,kind:`ScalarField`,name:`id`,storageKey:null},{alias:null,args:null,kind:`ScalarField`,name:`username`,storageKey:null},{alias:null,args:null,kind:`ScalarField`,name:`email`,storageKey:null},{alias:null,args:null,kind:`ScalarField`,name:`profilePictureUrl`,storageKey:null},{alias:null,args:null,kind:`ScalarField`,name:`isManagementUser`,storageKey:null},{alias:null,args:null,concreteType:`UserRole`,kind:`LinkedField`,name:`role`,plural:!1,selections:[{alias:null,args:null,kind:`ScalarField`,name:`name`,storageKey:null}],storageKey:null},{alias:null,args:null,kind:`ScalarField`,name:`authMethod`,storageKey:null},{args:null,kind:`FragmentSpread`,name:`ViewerAPIKeysListFragment`},{args:null,kind:`FragmentSpread`,name:`AuthorizedApplicationsCardFragment`}],storageKey:null}],type:`Query`,abstractKey:null};Jr.hash=`53341d080ff76da24b2f1bc9e36c4e23`;var Yr=we(),Xr=X.createContext({viewer:null,refetchViewer:()=>{}});function Zr(){let e=X.useContext(Xr);if(e==null)throw Error(`useViewer must be used within a ViewerProvider`);return e}function Qr(){let{viewer:e}=Zr();return!(e&&e.role.name===`VIEWER`)}function $r(){let e=ei();return!window.Config.authenticationEnabled||e}function ei(){let{viewer:e}=Zr();return window.Config.authenticationEnabled&&e?.role?.name===`ADMIN`}function ti(){return $r()}function ni(){return $r()}function ri(){return $r()}function ii(){return $r()}function ai(){return $r()}function oi(e){let t=(0,Z.c)(9),{query:n,children:r}=e,i;t[0]===Symbol.for(`react.memo_cache_sentinel`)?(i=Jr,t[0]=i):i=t[0];let[a,o]=(0,Yr.useRefetchableFragment)(i,n),s;t[1]===o?s=t[2]:(s=()=>{(0,X.startTransition)(()=>{o({},{fetchPolicy:`network-only`})})},t[1]=o,t[2]=s);let c=s,l;t[3]!==a.viewer||t[4]!==c?(l={viewer:a.viewer,refetchViewer:c},t[3]=a.viewer,t[4]=c,t[5]=l):l=t[5];let u;return t[6]!==r||t[7]!==l?(u=H(Xr.Provider,{value:l,children:r}),t[6]=r,t[7]=l,t[8]=u):u=t[8],u}var si={OPENAI:`OpenAI`,AZURE_OPENAI:`Azure OpenAI`,ANTHROPIC:`Anthropic`,GOOGLE:`Google`,DEEPSEEK:`DeepSeek`,XAI:`xAI`,OLLAMA:`Ollama`,AWS:`AWS Bedrock`,CEREBRAS:`Cerebras`,FIREWORKS:`Fireworks`,GROQ:`Groq`,MOONSHOT:`Moonshot`,PERPLEXITY:`Perplexity`,TOGETHER:`Together`},ci=`OPENAI`,li=`gpt-5.6-luna`,ui=`user`,di=`RESPONSES`,fi={user:[`user`,`human`],ai:[`assistant`,`bot`,`ai`,`model`],system:[`system`,`developer`],tool:[`tool`]},pi={OPENAI:[{envVarName:`OPENAI_API_KEY`,isRequired:!0}],AZURE_OPENAI:[{envVarName:`AZURE_OPENAI_API_KEY`,isRequired:!0}],ANTHROPIC:[{envVarName:`ANTHROPIC_API_KEY`,isRequired:!0}],GOOGLE:[{envVarName:`GEMINI_API_KEY`,isRequired:!0}],DEEPSEEK:[{envVarName:`DEEPSEEK_API_KEY`,isRequired:!0}],XAI:[{envVarName:`XAI_API_KEY`,isRequired:!0}],OLLAMA:[],CEREBRAS:[{envVarName:`CEREBRAS_API_KEY`,isRequired:!0}],FIREWORKS:[{envVarName:`FIREWORKS_API_KEY`,isRequired:!0}],GROQ:[{envVarName:`GROQ_API_KEY`,isRequired:!0}],MOONSHOT:[{envVarName:`MOONSHOT_API_KEY`,isRequired:!0}],PERPLEXITY:[{envVarName:`PERPLEXITY_API_KEY`,isRequired:!0}],TOGETHER:[{envVarName:`TOGETHER_API_KEY`,isRequired:!0}],AWS:[{envVarName:`AWS_ACCESS_KEY_ID`,isRequired:!0},{envVarName:`AWS_SECRET_ACCESS_KEY`,isRequired:!0},{envVarName:`AWS_SESSION_TOKEN`,isRequired:!1}]},mi=`api_key`,hi=`default_credentials`,gi={OPENAI:`OPENAI`,AZURE_OPENAI:`AZURE_OPENAI`,ANTHROPIC:`ANTHROPIC`,AWS_BEDROCK:`AWS`,GOOGLE_GENAI:`GOOGLE`},_i={openai:`OPENAI`,azure:`AZURE_OPENAI`,anthropic:`ANTHROPIC`,aws:`AWS`,google:`GOOGLE`,xai:`XAI`,ollama:`OLLAMA`,deepseek:`DEEPSEEK`,cerebras:`CEREBRAS`,fireworks:`FIREWORKS`,groq:`GROQ`,moonshot:`MOONSHOT`,perplexity:`PERPLEXITY`,together:`TOGETHER`},vi=Object.entries({OPENAI:`OpenAI`,AZURE_OPENAI:`Azure OpenAI`,ANTHROPIC:`Anthropic`,AWS_BEDROCK:`AWS Bedrock`,GOOGLE_GENAI:`Google GenAI`}).map(([e,t])=>({id:e,label:t})),yi={OPENAI:`openai`,AZURE_OPENAI:`azure`,ANTHROPIC:`anthropic`,AWS_BEDROCK:`aws`,GOOGLE_GENAI:`google`},bi=Object.entries({api_key:`API Key`,ad_token_provider:`Azure AD Token Provider`,default_credentials:`Default Credentials (Managed Identity)`}).map(([e,t])=>({id:e,label:t})),xi=Object.entries({default_credentials:`Default Credentials (IAM Role)`,access_keys:`Access Keys`}).map(([e,t])=>({id:e,label:t}));function Si(e){let t=(0,Z.c)(4),n;t[0]===Symbol.for(`react.memo_cache_sentinel`)?(n=q`
        display: inline-block;
        max-width: 100%;
        overflow: hidden;
        text-overflow: ellipsis;
        color: var(--global-link-color);
      `,t[0]=n):n=t[0];let r;t[1]===Symbol.for(`react.memo_cache_sentinel`)?(r=q`
          color: var(--global-link-color);
          &:not(:hover) {
            text-decoration: none;
          }
        `,t[1]=r):r=t[1];let i;return t[2]===e?i=t[3]:(i=H(`div`,{className:`link-container`,onClick:Ci,css:n,children:H(Jt,{css:r,...e})}),t[2]=e,t[3]=i),i}function Ci(e){return e.stopPropagation()}function wi(e){let t=(0,Z.c)(5),{href:n,children:r}=e,i;t[0]===Symbol.for(`react.memo_cache_sentinel`)?(i=q`
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
      `,t[0]=i):i=t[0];let a;t[1]===Symbol.for(`react.memo_cache_sentinel`)?(a=H(V,{svg:H(rt,{})}),t[1]=a):a=t[1];let o;return t[2]!==r||t[3]!==n?(o=U(`a`,{href:n,target:`_blank`,css:i,rel:`noreferrer`,children:[r,a]}),t[2]=r,t[3]=n,t[4]=o):o=t[4],o}var Ti=q`
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
`,Ei=q`
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
`;function Di(e){let t=(0,Z.c)(13),n,r;t[0]===e?(n=t[1],r=t[2]):({ref:r,...n}=e,t[0]=e,t[1]=n,t[2]=r);let{isIndeterminate:i,value:a,size:o}=n,s=i!==void 0&&i,c=o===void 0?`M`:o,l=s||void 0,u;t[3]!==s||t[4]!==a?(u=!s&&a!=null?{"--progress-circle-value":a}:void 0,t[3]=s,t[4]=a,t[5]=u):u=t[5];let d;t[6]===Symbol.for(`react.memo_cache_sentinel`)?(d=U(`svg`,{className:`progress-circle__svg`,children:[H(`circle`,{className:`progress-circle__background`}),H(`circle`,{className:`progress-circle__arc`})]}),t[6]=d):d=t[6];let f;return t[7]!==n||t[8]!==r||t[9]!==c||t[10]!==l||t[11]!==u?(f=H(mn,{...n,"data-size":c,"data-indeterminate":l,css:Ti,ref:r,style:u,children:d}),t[7]=n,t[8]=r,t[9]=c,t[10]=l,t[11]=u,t[12]=f):f=t[12],f}function Oi(e){let t=(0,Z.c)(12),n,r,i,a;t[0]===e?(n=t[1],r=t[2],i=t[3],a=t[4]):({ref:i,width:a,height:n,...r}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a);let o;t[5]!==n||t[6]!==a?(o={width:a,height:n},t[5]=n,t[6]=a,t[7]=o):o=t[7];let s;return t[8]!==r||t[9]!==i||t[10]!==o?(s=H(mn,{...r,ref:i,css:Ei,style:o,children:ki}),t[8]=r,t[9]=i,t[10]=o,t[11]=s):s=t[11],s}function ki(e){let{percentage:t}=e;return H(`div`,{className:`progress-bar__track`,children:H(`div`,{className:`progress-bar__fill`,style:{width:t+`%`}})})}function Ai(e){let t=(0,Z.c)(7),{ref:n,...r}=e,{children:i,elementType:a,...o}=r,s=a===void 0?`div`:a,{styleProps:c}=fn(r,ln),l=rn(o),u;t[0]===Symbol.for(`react.memo_cache_sentinel`)?(u=q`
        overflow: hidden;
        box-sizing: border-box;
      `,t[0]=u):u=t[0];let d;return t[1]!==s||t[2]!==i||t[3]!==n||t[4]!==c||t[5]!==l?(d=H(s,{...l,...c,ref:n,css:u,className:`view`,children:i}),t[1]=s,t[2]=i,t[3]=n,t[4]=c,t[5]=l,t[6]=d):d=t[6],d}var ji=q`
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
`,Mi=q`
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
`;function Ni(e){let t=(0,Z.c)(10),n,r,i,a;if(t[0]!==e){let{ref:o,...s}=e,{css:c,...l}=s;n=Ee,r=l,i=o,a=q(ji,c),t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a}else n=t[1],r=t[2],i=t[3],a=t[4];let o;return t[5]!==n||t[6]!==r||t[7]!==i||t[8]!==a?(o=H(n,{...r,ref:i,css:a}),t[5]=n,t[6]=r,t[7]=i,t[8]=a,t[9]=o):o=t[9],o}function Pi(e){let t=(0,Z.c)(8),n,r;t[0]===e?(n=t[1],r=t[2]):({ref:r,...n}=e,t[0]=e,t[1]=n,t[2]=r);let{css:i}=n,a;t[3]===Symbol.for(`react.memo_cache_sentinel`)?(a=z(`react-aria-OverlayArrow`),t[3]=a):a=t[3];let o;t[4]===Symbol.for(`react.memo_cache_sentinel`)?(o=H(`svg`,{width:8,height:8,viewBox:`0 0 8 8`,children:H(`path`,{d:`M0 0 L4 4 L8 0`})}),t[4]=o):o=t[4];let s;return t[5]!==i||t[6]!==r?(s=H(Ut,{ref:r,css:i,className:a,children:o}),t[5]=i,t[6]=r,t[7]=s):s=t[7],s}var Fi=1e3,Ii=60*Fi,Li=60*Ii,Ri=24*Li;7*Ri;var zi=30*Ri,Bi=3600*24*365,Vi=3600*24*30,Hi=3600*24*7,Ui=3600*24,Wi=3600,Gi=`https://arize.com/docs/phoenix`,Ki={accessControl:`${Gi}/settings/access-control-rbac`,annotationConfigs:`${Gi}/tracing/how-to-tracing/feedback-and-annotations/annotating-in-the-ui`,apiKeys:`${Gi}/settings/api-keys`,customAiProviders:`${Gi}/settings/custom-ai-providers`,dataRetention:`${Gi}/settings/data-retention`,datasetLabels:`${Gi}/release-notes/10-2025/10-08-2025-dataset-labels`,modelCostTracking:`${Gi}/tracing/how-to-tracing/cost-tracking`,remoteMcpServer:`${Gi}/integrations/remote-mcp`,promptLabels:`${Gi}/release-notes/09-2025/09-15-2025-prompt-labels`,providers:`${Gi}/prompt-engineering/how-to-prompts/configure-ai-providers`,pxi:`${Gi}/pxi`,sandboxes:`${Gi}/settings/sandboxes`,secrets:`${Gi}/settings/secrets`},qi={aiProviderSettings:{href:Ki.providers,label:`AI provider settings`},aiProviders:{href:Ki.providers,label:`AI providers`},annotationConfigs:{href:Ki.annotationConfigs,label:`annotation configs`},apiKeys:{href:Ki.apiKeys,label:`API keys`},customAiProviders:{href:Ki.customAiProviders,label:`custom AI providers`},dataRetention:{href:Ki.dataRetention,label:`data retention`},datasetLabels:{href:Ki.datasetLabels,label:`dataset labels`},defaultRetentionPolicy:{href:Ki.dataRetention,label:`the default retention policy`},modelPricing:{href:Ki.modelCostTracking,label:`model pricing`},promptLabels:{href:Ki.promptLabels,label:`prompt labels`},pxi:{href:Ki.pxi,label:`PXI`},sandboxConfigurations:{href:Ki.sandboxes,label:`sandbox configurations`},sandboxProviders:{href:Ki.sandboxes,label:`sandbox providers`},secrets:{href:Ki.secrets,label:`secrets`},userAccess:{href:Ki.accessControl,label:`user access`}},Ji=e=>{switch(e){case`info`:return H(vn,{});default:return H(it,{})}},Yi=q`
  & {
    all: unset;
    height: 14px !important;
    width: 14px !important;
    padding: var(--global-dimension-size-50) !important;
    border-radius: var(--global-rounding-small);
    cursor: pointer;
    svg {
      height: 14px;
      width: 14px;
    }
  }
`,Xi=e=>{let t=(0,Z.c)(22),n,r,i,a,o;t[0]===e?(n=t[1],r=t[2],i=t[3],a=t[4],o=t[5]):({children:n,href:r,triggerAriaLabel:i,variant:a,...o}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a,t[5]=o);let s=i===void 0?`More information`:i,c=a===void 0?`help`:a,l;t[6]===c?l=t[7]:(l=Ji(c),t[6]=c,t[7]=l);let u;t[8]===l?u=t[9]:(u=H(V,{svg:l}),t[8]=l,t[9]=u);let f;t[10]!==u||t[11]!==s?(f={"aria-label":s,css:Yi,leadingVisual:u,size:`S`,variant:`quiet`},t[10]=u,t[11]=s,t[12]=f):f=t[12];let p=f,m;t[13]!==r||t[14]!==p?(m=r?H(d,{children:H(pt,{...p,href:r})}):H(W,{...p}),t[13]=r,t[14]=p,t[15]=m):m=t[15];let h;t[16]!==n||t[17]!==o?(h=H(Ni,{...o,children:n}),t[16]=n,t[17]=o,t[18]=h):h=t[18];let _;return t[19]!==m||t[20]!==h?(_=U(g,{delay:0,children:[m,h]}),t[19]=m,t[20]=h,t[21]=_):_=t[21],_},Zi=q`
  margin-top: var(--global-dimension-size-100);
`;function Qi(e){let t=(0,Z.c)(9),{children:n,topic:r}=e,{href:i,label:a}=qi[r],o=`Learn more about ${a}`,s;t[0]===n?s=t[1]:(s=H(B,{size:`S`,children:n}),t[0]=n,t[1]=s);let c;t[2]===i?c=t[3]:(c=H(`footer`,{css:Zi,children:H(wi,{href:i,children:`View documentation`})}),t[2]=i,t[3]=c);let l;return t[4]!==i||t[5]!==o||t[6]!==s||t[7]!==c?(l=U(Xi,{href:i,variant:`info`,triggerAriaLabel:o,children:[s,c]}),t[4]=i,t[5]=o,t[6]=s,t[7]=c,t[8]=l):l=t[8],l}function $i(e){let t=(0,Z.c)(8),n,r;t[0]===e?(n=t[1],r=t[2]):({children:n,...r}=e,t[0]=e,t[1]=n,t[2]=r);let i;t[3]===n?i=t[4]:(i=H(`div`,{role:`button`,children:n}),t[3]=n,t[4]=i);let a;return t[5]!==r||t[6]!==i?(a=H(d,{...r,children:i}),t[5]=r,t[6]=i,t[7]=a):a=t[7],a}function ea(e){let t=(0,Z.c)(16),n,r,i,a,o,s;if(t[0]!==e){let{ref:c,...l}=e,{children:u,css:d,width:f,...p}=l;r=u,s=f,n=Ee,i=p,a=c,o=q(Mi,d),t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a,t[5]=o,t[6]=s}else n=t[1],r=t[2],i=t[3],a=t[4],o=t[5],s=t[6];let c;t[7]===s?c=t[8]:(c=s?{width:s}:{maxWidth:`300px`},t[7]=s,t[8]=c);let l;return t[9]!==n||t[10]!==r||t[11]!==i||t[12]!==a||t[13]!==o||t[14]!==c?(l=H(n,{...i,ref:a,css:o,style:c,children:r}),t[9]=n,t[10]=r,t[11]=i,t[12]=a,t[13]=o,t[14]=c,t[15]=l):l=t[15],l}function ta(e){let t=(0,Z.c)(3),{children:n}=e,r;t[0]===Symbol.for(`react.memo_cache_sentinel`)?(r=q`
        margin-bottom: var(--global-dimension-size-100);
      `,t[0]=r):r=t[0];let i;return t[1]===n?i=t[2]:(i=H(Xe,{level:4,css:r,children:n}),t[1]=n,t[2]=i),i}function na(e){let t=(0,Z.c)(3),{children:n}=e,r;t[0]===Symbol.for(`react.memo_cache_sentinel`)?(r=q`
        margin-bottom: var(--global-dimension-size-100);
      `,t[0]=r):r=t[0];let i;return t[1]===n?i=t[2]:(i=H(B,{size:`S`,color:`text-700`,css:r,children:n}),t[1]=n,t[2]=i),i}function ra(e){let t=(0,Z.c)(2),{children:n}=e,r;return t[0]===n?r=t[1]:(r=H(Ai,{paddingTop:`size-50`,children:n}),t[0]=n,t[1]=r),r}var ia=2e3,aa=q`
  flex: none;
  box-sizing: content-box;
`;function oa(e){let t=(0,Z.c)(20),n,r,i,a;t[0]===e?(n=t[1],r=t[2],i=t[3],a=t[4]):({text:a,size:r,tooltipText:i,...n}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a);let o=r===void 0?`S`:r,s=i===void 0?`Copy`:i,[c,l]=(0,X.useState)(!1),u;t[5]===a?u=t[6]:(u=()=>{Ie(typeof a==`string`?a:a.current||``),l(!0),setTimeout(()=>{l(!1)},ia)},t[5]=a,t[6]=u);let d=u,f=c?`success`:`inherit`,p=c?`Checkmark`:`Duplicate`,m;t[7]!==f||t[8]!==p?(m=H(V,{color:f,svgKey:p}),t[7]=f,t[8]=p,t[9]=m):m=t[9];let h;t[10]!==d||t[11]!==n||t[12]!==o||t[13]!==m?(h=H(W,{size:o,leadingVisual:m,onPress:d,...n,className:`copy-button`}),t[10]=d,t[11]=n,t[12]=o,t[13]=m,t[14]=h):h=t[14];let _;t[15]===s?_=t[16]:(_=H(Ni,{offset:1,children:s}),t[15]=s,t[16]=_);let v;return t[17]!==h||t[18]!==_?(v=H(`div`,{className:`copy-to-clipboard-button`,css:aa,children:U(g,{children:[h,_]})}),t[17]=h,t[18]=_,t[19]=v):v=t[19],v}var sa=q`
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
`,ca=et,la=e=>{let t=(0,Z.c)(10),n,r,i;t[0]===e?(n=t[1],r=t[2],i=t[3]):({className:n,onKeyDown:r,...i}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i);let a;t[4]===n?a=t[5]:(a=z(`react-aria-Menu`,n),t[4]=n,t[5]=a);let o;return t[6]!==r||t[7]!==i||t[8]!==a?(o=H(ot,{className:a,css:sa,...i,onKeyDown:r}),t[6]=r,t[7]=i,t[8]=a,t[9]=o):o=t[9],o},ua=q`
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
`,da=e=>{let t=(0,Z.c)(16),n,r,i,a;t[0]===e?(n=t[1],r=t[2],i=t[3],a=t[4]):({className:n,trailingContent:a,leadingContent:r,...i}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a);let o=i.textValue||(typeof i.children==`string`?i.children:void 0),s;t[5]===n?s=t[6]:(s=z(`react-aria-MenuItem`,n),t[5]=n,t[6]=s);let c;t[7]!==r||t[8]!==i||t[9]!==a?(c=e=>{let{hasSubmenu:t,isSelected:n,selectionMode:o}=e;return U(G,{children:[n&&H(V,{svg:H(Yt,{})}),o!==`none`&&!n&&H(V,{svg:H(Yt,{}),css:q`
                  visibility: hidden;
                `}),H(fa,{trailingContent:a,leadingContent:r,children:typeof i.children==`function`?i.children(e):i.children}),t&&H(V,{svg:H(On,{})})]})},t[7]=r,t[8]=i,t[9]=a,t[10]=c):c=t[10];let l;return t[11]!==i||t[12]!==s||t[13]!==c||t[14]!==o?(l=H(ut,{...i,css:ua,className:s,textValue:o,children:c}),t[11]=i,t[12]=s,t[13]=c,t[14]=o,t[15]=l):l=t[15],l},fa=e=>{let t=(0,Z.c)(7),{children:n,trailingContent:r,leadingContent:i}=e,a;t[0]===Symbol.for(`react.memo_cache_sentinel`)?(a=q`
        padding: var(--global-menu-item-gap);
      `,t[0]=a):a=t[0];let o;t[1]!==n||t[2]!==i?(o=i?U(K,{alignItems:`center`,gap:`var(--global-menu-item-content-gap)`,children:[i,` `,n]}):n,t[1]=n,t[2]=i,t[3]=o):o=t[3];let s;return t[4]!==o||t[5]!==r?(s=U(K,{direction:`row`,alignItems:`center`,justifyContent:`space-between`,gap:`var(--global-menu-split-item-content-gap)`,minWidth:0,flex:1,css:a,children:[o,r]}),t[4]=o,t[5]=r,t[6]=s):s=t[6],s},pa=q`
  overflow-y: hidden;
  display: flex;
  flex-direction: column;
`,ma=e=>{let t=(0,Z.c)(19),n,r,i,a,o,s;t[0]===e?(n=t[1],r=t[2],i=t[3],a=t[4],o=t[5],s=t[6]):({children:n,placement:i,minHeight:a,maxHeight:o,maxWidth:s,...r}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a,t[5]=o,t[6]=s);let c=i===void 0?`bottom end`:i,l=a===void 0?`var(--global-menu-min-height)`:a,u=o===void 0?`var(--global-menu-max-height-large)`:o,d=s===void 0?450:s,f;t[7]!==u||t[8]!==d||t[9]!==l?(f={minHeight:l,maxHeight:u,maxWidth:d},t[7]=u,t[8]=d,t[9]=l,t[10]=f):f=t[10];let p;t[11]===Symbol.for(`react.memo_cache_sentinel`)?(p=q`
          display: flex;
          flex-direction: column;
          height: 100%;
          min-width: 300px;
        `,t[11]=p):p=t[11];let m;t[12]!==n||t[13]!==f?(m=H(`div`,{style:f,css:p,children:n}),t[12]=n,t[13]=f,t[14]=m):m=t[14];let h;return t[15]!==c||t[16]!==r||t[17]!==m?(h=H(kn,{shouldFlip:!1,placement:c,css:pa,...r,children:m}),t[15]=c,t[16]=r,t[17]=m,t[18]=h):h=t[18],h},ha=q`
  padding: var(--global-dimension-size-50) var(--global-dimension-size-100) 0;
`,ga=e=>{let t=(0,Z.c)(5),{title:n,trailingContent:r}=e,i;t[0]===n?i=t[1]:(i=H(B,{weight:`heavy`,children:n}),t[0]=n,t[1]=i);let a;return t[2]!==i||t[3]!==r?(a=H(nn,{css:ha,children:U(K,{justifyContent:`space-between`,alignItems:`center`,children:[i,r]})}),t[2]=i,t[3]=r,t[4]=a):a=t[4],a},_a=e=>{let t=(0,Z.c)(3),{children:n}=e,r;t[0]===Symbol.for(`react.memo_cache_sentinel`)?(r=q`
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
      `,t[0]=r):r=t[0];let i;return t[1]===n?i=t[2]:(i=H(`div`,{className:`menu-header`,css:r,children:n}),t[1]=n,t[2]=i),i},va=e=>{let t=(0,Z.c)(8),{children:n,leadingContent:r,trailingContent:i}=e,a;t[0]===Symbol.for(`react.memo_cache_sentinel`)?(a=q`
        padding: var(--global-dimension-size-100);
        border-bottom: 1px solid var(--global-menu-border-color);
      `,t[0]=a):a=t[0];let o;t[1]===Symbol.for(`react.memo_cache_sentinel`)?(o=q`
          flex: 1 1 auto;
          width: 100%;
          padding-left: var(--global-dimension-size-50);
        `,t[1]=o):o=t[1];let s;t[2]===n?s=t[3]:(s=H(Xe,{level:4,weight:`heavy`,css:o,children:n}),t[2]=n,t[3]=s);let c;return t[4]!==r||t[5]!==s||t[6]!==i?(c=U(K,{direction:`row`,gap:`size-50`,alignItems:`center`,wrap:`nowrap`,minHeight:30,"data-testid":`menu-header-title`,css:a,children:[r,s,i]}),t[4]=r,t[5]=s,t[6]=i,t[7]=c):c=t[7],c},ya=e=>{let t=(0,Z.c)(3),{children:n}=e,r;t[0]===Symbol.for(`react.memo_cache_sentinel`)?(r=q`
        padding: var(--global-dimension-size-100);
        border-top: 1px solid var(--global-menu-border-color);
        display: flex;
        flex-direction: column;
        flex-shrink: 0;
        gap: var(--global-dimension-size-50);
      `,t[0]=r):r=t[0];let i;return t[1]===n?i=t[2]:(i=H(`div`,{css:r,children:n}),t[1]=n,t[2]=i),i},ba=e=>{let t=(0,Z.c)(3),{children:n}=e,r;t[0]===Symbol.for(`react.memo_cache_sentinel`)?(r=q`
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
      `,t[0]=r):r=t[0];let i;return t[1]===n?i=t[2]:(i=H(B,{color:`gray-400`,fontStyle:`italic`,css:r,children:n}),t[1]=n,t[2]=i),i},xa=q`
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
`;function Sa(e){let t=(0,Z.c)(10),n,r,i;t[0]===e?(n=t[1],r=t[2],i=t[3]):({ref:i,css:n,...r}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i);let a;t[4]===n?a=t[5]:(a=q(xa,n),t[4]=n,t[5]=a);let o;return t[6]!==r||t[7]!==i||t[8]!==a?(o=H(W,{ref:i,css:a,...r}),t[6]=r,t[7]=i,t[8]=a,t[9]=o):o=t[9],o}function Ca(e){let t=(0,Z.c)(5),{children:n,isPlaceholder:r}=e,i=r&&`menu-button__value--placeholder`,a;t[0]===i?a=t[1]:(a=z(`menu-button__value`,i),t[0]=i,t[1]=a);let o;return t[2]!==n||t[3]!==a?(o=H(`span`,{className:a,children:n}),t[2]=n,t[3]=a,t[4]=o):o=t[4],o}var wa=2e3;function Ta(e){let t=(0,Z.c)(18),{items:n}=e,[r,i]=(0,X.useState)(null),a=(0,X.useRef)(null),o;t[0]===n?o=t[1]:(o=e=>{let t=n.find(t=>t.name===e);t&&(Ie(t.value),i(t.name),a.current&&clearTimeout(a.current),a.current=setTimeout(()=>{i(null)},wa))},t[0]=n,t[1]=o);let s=o,c=r==null?`Duplicate`:`Checkmark`,l=r==null?`inherit`:`success`,u;t[2]!==c||t[3]!==l?(u=H(V,{svgKey:c,color:l}),t[2]=c,t[3]=l,t[4]=u):u=t[4];let d=r!=null||void 0,f=r==null?void 0:`Copied`,p;t[5]!==u||t[6]!==d||t[7]!==f?(p=H(W,{size:`S`,variant:`quiet`,"aria-label":`Copy`,leadingVisual:u,className:`copy-action-menu__button`,"data-copied":d,children:f}),t[5]=u,t[6]=d,t[7]=f,t[8]=p):p=t[8];let m;t[9]===Symbol.for(`react.memo_cache_sentinel`)?(m=q`
            --menu-min-width: auto;
          `,t[9]=m):m=t[9];let h;t[10]===n?h=t[11]:(h=n.map(Ea),t[10]=n,t[11]=h);let g;t[12]!==s||t[13]!==h?(g=H(kn,{placement:`bottom end`,offset:3,children:H(la,{onAction:s,css:m,children:h})}),t[12]=s,t[13]=h,t[14]=g):g=t[14];let _;return t[15]!==p||t[16]!==g?(_=U(ca,{children:[p,g]}),t[15]=p,t[16]=g,t[17]=_):_=t[17],_}function Ea(e){return H(da,{id:e.name,textValue:`Copy ${e.name}`,leadingContent:H(V,{svgKey:e.iconKey??`Duplicate`}),children:e.name},e.name)}var Da=e=>{let t=(0,Z.c)(6),{children:n,bordered:r}=e,i=r===void 0||r,a;t[0]===Symbol.for(`react.memo_cache_sentinel`)?(a=q`
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
      `,t[0]=a):a=t[0];let o;t[1]===n?o=t[2]:(o=H(Xe,{children:n}),t[1]=n,t[2]=o);let s;return t[3]!==i||t[4]!==o?(s=H(`div`,{"data-bordered":i,css:a,children:o}),t[3]=i,t[4]=o,t[5]=s):s=t[5],s},Oa=[/Unexpected token ['"]?<['"]?/i,/JSON\.parse.*unexpected character/i,/<!DOCTYPE/i,/timeout/i,/502|504|gateway/i];function ka(e){if(e==null)return!1;let t=e instanceof Error?e.message:e;return typeof t!=`string`||t.length===0?!1:Oa.some(e=>e.test(t))}function Aa(e){let t=(0,Z.c)(9),{error:n}=e;if(ka(n)){let e;return t[0]===n?e=t[1]:(e=H(ja,{error:n}),t[0]=n,t[1]=e),e}let r,i;t[2]===Symbol.for(`react.memo_cache_sentinel`)?(r=H(K,{direction:`column`,width:`100%`,alignItems:`center`,children:H(`h1`,{children:`Something went wrong`})}),i=H(`p`,{children:`We strive to do our very best but 🐛 bugs happen. It would mean a lot to us if you could file a an issue. If you feel comfortable, please include the error details below in your issue. We will get back to you as soon as we can.`}),t[2]=r,t[3]=i):(r=t[2],i=t[3]);let a;t[4]===Symbol.for(`react.memo_cache_sentinel`)?(a=H(K,{direction:`row`,width:`100%`,justifyContent:`end`,children:H(wi,{href:`https://github.com/Arize-ai/phoenix/issues/new?assignees=&labels=bug&template=bug_report.md&title=%5BBUG%5D`,children:`file an issue with us`})}),t[4]=a):a=t[4];let o,s;t[5]===Symbol.for(`react.memo_cache_sentinel`)?(o=H(`summary`,{children:`error details`}),s=q`
              white-space: pre-wrap;
              overflow-wrap: break-word;
              overflow: hidden;
              overflow-y: auto;
              max-height: 500px;
            `,t[5]=o,t[6]=s):(o=t[5],s=t[6]);let c;return t[7]===n?c=t[8]:(c=H(Ai,{padding:`size-200`,children:U(K,{direction:`column`,children:[r,i,a,U(`details`,{open:!0,children:[o,H(`pre`,{css:s,children:n})]})]})}),t[7]=n,t[8]=c),c}function ja(e){let t=(0,Z.c)(9),{error:n}=e,r,i,a,o;t[0]===Symbol.for(`react.memo_cache_sentinel`)?(r=H(K,{direction:`column`,width:`100%`,alignItems:`center`,children:H(`h1`,{children:`Connection timed out`})}),i=H(`p`,{children:`The connection to the Phoenix server timed out before a response was received. This typically happens when a load balancer or proxy closes the connection before the server can respond.`}),a=H(`p`,{children:`Possible solutions:`}),o=U(`ul`,{css:q`
            margin: var(--global-dimension-size-100) 0;
            padding-left: var(--global-dimension-size-300);
          `,children:[H(`li`,{children:`Increase your load balancer or proxy timeout settings`}),H(`li`,{children:`Check if the Phoenix server is overloaded or slow to respond`}),H(`li`,{children:`Verify network connectivity between components`})]}),t[0]=r,t[1]=i,t[2]=a,t[3]=o):(r=t[0],i=t[1],a=t[2],o=t[3]);let s;t[4]===Symbol.for(`react.memo_cache_sentinel`)?(s=H(K,{direction:`row`,width:`100%`,justifyContent:`end`,children:H(W,{variant:`primary`,size:`S`,onPress:Ma,children:`Retry`})}),t[4]=s):s=t[4];let c;t[5]===n?c=t[6]:(c=n&&U(`details`,{children:[H(`summary`,{children:`error details`}),H(`pre`,{css:q`
                white-space: pre-wrap;
                overflow-wrap: break-word;
                overflow: hidden;
                overflow-y: auto;
                max-height: 500px;
              `,children:n})]}),t[5]=n,t[6]=c);let l;return t[7]===c?l=t[8]:(l=H(Ai,{padding:`size-200`,children:U(K,{direction:`column`,children:[r,i,a,o,s,c]})}),t[7]=c,t[8]=l),l}function Ma(){window.location.reload()}var Na=class extends X.Component{constructor(e){super(e),this.state={hasError:!1,error:null}}static getDerivedStateFromError(e){return{hasError:!0,error:e}}componentDidCatch(e,t){console.error(`ErrorBoundary caught error:`,e,t)}render(){if(this.state.hasError){let e=this.state.error instanceof Error?this.state.error.message:null;return typeof this.props.fallback==`function`?H(this.props.fallback,{error:e}):H(Aa,{error:e})}return this.props.children}};function Pa({error:e}){let t=U(`div`,{css:q`
        text-align: center;
        display: inline-flex;
        align-items: center;
        color: var(--global-text-color-300);
        gap: var(--global-dimension-size-50);
        cursor: ${e?`help`:`default`};
      `,children:[H(V,{svg:H(ct,{})}),H(B,{color:`text-300`,children:`error`})]});return e?U(g,{delay:200,children:[H(`span`,{tabIndex:0,children:t}),H(Ee,{offset:6,children:H(Ai,{padding:`size-100`,borderColor:`default`,borderWidth:`thin`,borderRadius:`small`,backgroundColor:`gray-200`,maxWidth:`size-4600`,children:H(`pre`,{css:q`
              white-space: pre-wrap;
              overflow-wrap: break-word;
              margin: 0;
              font-size: var(--global-font-size-xs, 12px);
            `,children:e})})})]}):t}var Fa=q`
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
`,Ia=q`
  background-color: transparent;
  color: var(--ac-global-text-color-500);
  padding: 0 var(--global-dimension-size-75);
  font-size: var(--global-dimension-font-size-50);
  border-radius: var(--global-rounding-small);
  border: 1px solid var(--ac-global-border-color-default);
  text-transform: uppercase;
`;function La(e){let t=(0,Z.c)(10),n,r,i,a;t[0]===e?(n=t[1],r=t[2],i=t[3],a=t[4]):({ref:i,children:n,variant:a,...r}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a);let o=(a===void 0?`default`:a)===`quiet`?Ia:Fa,s;return t[5]!==n||t[6]!==r||t[7]!==i||t[8]!==o?(s=H(Ct,{ref:i,css:o,...r,children:n}),t[5]=n,t[6]=r,t[7]=i,t[8]=o,t[9]=s):s=t[9],s}function Ra({ref:e,color:t,size:n=`M`,shape:r=`square`}){let i=typeof t==`string`&&t.startsWith(`var`),a=i?q`
        background-color: ${t} !important;
      `:void 0;return H(l,{color:i?void 0:t,"data-shape":r,"data-size":n,ref:e,css:q(q`
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
        `,a)})}Ra.displayName=`ColorSwatch`;var za=q`
  opacity: 0.8;
  color: var(--global-text-color-500);
  .theme--dark & {
    color: var(--global-text-color-400);
  }
  .text {
    color: inherit;
  }
`,Ba=q`
  margin: var(--global-dimension-size-300);
  display: flex;
  flex-direction: column;
  align-items: center;
`;function Va(e){let t=(0,Z.c)(7),{message:n,size:r}=e,i=r===void 0?`M`:r,a,o;t[0]===Symbol.for(`react.memo_cache_sentinel`)?(a=q`
        width: 100%;
        display: flex;
        justify-content: center;
      `,o=[Ba,za],t[0]=a,t[1]=o):(a=t[0],o=t[1]);let s;t[2]!==n||t[3]!==i?(s=n&&H(B,{size:i,children:n}),t[2]=n,t[3]=i,t[4]=s):s=t[4];let c;return t[5]===s?c=t[6]:(c=H(`div`,{css:a,children:H(`div`,{css:o,children:s})}),t[5]=s,t[6]=c),c}var Ha=q`
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
`;function Ua(){let e=(0,Z.c)(2),t=(0,X.useContext)($t),n=(0,X.useContext)(me),r=t?.inputValue??n?.inputValue??``,i;return e[0]===r?i=e[1]:(i=r.trim(),e[0]=r,e[1]=i),i.length>0}function Wa(e){let t=(0,Z.c)(9),{icon:n,description:r,isFiltered:i}=e,a=Ua(),o=i??a,s;t[0]===Symbol.for(`react.memo_cache_sentinel`)?(s=[Ha,za],t[0]=s):s=t[0];let c;t[1]!==n||t[2]!==o?(c=o?H(V,{svg:H(Mt,{})}):n,t[1]=n,t[2]=o,t[3]=c):c=t[3];let l=o?`No results`:r,u;t[4]===l?u=t[5]:(u=H(B,{size:`S`,children:l}),t[4]=l,t[5]=u);let d;return t[6]!==c||t[7]!==u?(d=U(`div`,{css:s,children:[c,u]}),t[6]=c,t[7]=u,t[8]=d):d=t[8],d}var Ga=q`
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
`,Ka=q`
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
`;function qa(e){let t=(0,Z.c)(14),{icon:n,title:r,description:i,href:a,external:o}=e,s;t[0]===o?s=t[1]:(s=o?{target:`_blank`,rel:`noopener noreferrer`}:void 0,t[0]=o,t[1]=s);let c;t[2]===r?c=t[3]:(c=H(B,{weight:`heavy`,children:r}),t[2]=r,t[3]=c);let l;t[4]!==n||t[5]!==c?(l=U(K,{direction:`row`,gap:`size-100`,alignItems:`center`,children:[n,c]}),t[4]=n,t[5]=c,t[6]=l):l=t[6];let u;t[7]===i?u=t[8]:(u=H(B,{size:`S`,color:`text-700`,css:Ka,children:i}),t[7]=i,t[8]=u);let d;return t[9]!==a||t[10]!==s||t[11]!==l||t[12]!==u?(d=U(`a`,{href:a,css:Ga,...s,children:[l,u]}),t[9]=a,t[10]=s,t[11]=l,t[12]=u,t[13]=d):d=t[13],d}function Ja(e,t,n){return n==null?!1:e===`horizontal`||e!==`vertical`&&t?.type===`cards`&&(t.columns??1)===2&&t.items.length>=3}var Ya=q`
  max-width: var(--global-dimension-size-4000);
  text-align: center;
  text-wrap: balance;
`,Xa=q`
  display: grid;
  gap: var(--global-dimension-size-200);
  width: min(100%, var(--global-dimension-size-4000));
`,Za=q`
  width: min(100%, calc(var(--global-dimension-size-4000) * 2));
  grid-template-columns: repeat(
    auto-fit,
    minmax(min(100%, var(--global-dimension-size-4000)), 1fr)
  );
`;function Qa(e){let t=(0,Z.c)(14),{action:n}=e;if(n.type===`strip`){let e;t[0]===n.items?e=t[1]:(e=n.items.map(eo),t[0]=n.items,t[1]=e);let r;return t[2]===e?r=t[3]:(r=H(K,{direction:`row`,gap:`size-100`,wrap:!0,alignItems:`center`,children:e}),t[2]=e,t[3]=r),r}let r=n.columns??1,i=r===2&&Za,a;t[4]===r?a=t[5]:(a=r===1&&q`
            grid-template-columns: 1fr;
          `,t[4]=r,t[5]=a);let o;t[6]!==i||t[7]!==a?(o=[Xa,i,a],t[6]=i,t[7]=a,t[8]=o):o=t[8];let s;t[9]===n.items?s=t[10]:(s=n.items.map($a),t[9]=n.items,t[10]=s);let c;return t[11]!==o||t[12]!==s?(c=H(`div`,{css:o,children:s}),t[11]=o,t[12]=s,t[13]=c):c=t[13],c}function $a(e,t){return H(qa,{...e},t)}function eo(e,t){if(e.kind===`link`)return H(pt,{href:e.href,variant:`quiet`,size:`S`,children:e.label},t);if(e.kind===`node`)return H(X.Fragment,{children:e.node},t);let{kind:n,...r}=e;return H(W,{size:`S`,...r},t)}function to(e){let t=(0,Z.c)(23),{graphic:n,title:r,description:i,action:a,orientation:o}=e,s=Ja(o===void 0?`auto`:o,a,n),c=a?.type===`cards`?`size-300`:`size-200`,l=a?.type===`cards`?`size-500`:`size-200`,u;t[0]!==i||t[1]!==r?(u=r!=null||i!=null?U(K,{direction:`column`,gap:`size-25`,alignItems:`center`,children:[r!=null&&H(B,{size:`L`,weight:`heavy`,children:r}),i!=null&&H(B,{size:`S`,color:`text-700`,css:Ya,children:i})]}):null,t[0]=i,t[1]=r,t[2]=u):u=t[2];let d=u;if(s){let e;t[3]===n?e=t[4]:(e=H(K,{alignItems:`center`,justifyContent:`center`,children:n}),t[3]=n,t[4]=e);let r;t[5]!==e||t[6]!==d?(r=U(K,{direction:`row`,wrap:!0,gap:`size-400`,alignItems:`center`,justifyContent:`center`,children:[e,d]}),t[5]=e,t[6]=d,t[7]=r):r=t[7];let i;t[8]===a?i=t[9]:(i=a!=null&&H(Qa,{action:a}),t[8]=a,t[9]=i);let o;return t[10]!==l||t[11]!==r||t[12]!==i?(o=U(K,{direction:`column`,gap:l,alignItems:`center`,children:[r,i]}),t[10]=l,t[11]=r,t[12]=i,t[13]=o):o=t[13],o}let f=n!=null&&n,p;t[14]===a?p=t[15]:(p=a!=null&&H(Qa,{action:a}),t[14]=a,t[15]=p);let m;t[16]!==c||t[17]!==p||t[18]!==d?(m=U(K,{direction:`column`,gap:c,alignItems:`center`,children:[d,p]}),t[16]=c,t[17]=p,t[18]=d,t[19]=m):m=t[19];let h;return t[20]!==f||t[21]!==m?(h=U(K,{direction:`column`,gap:`size-300`,alignItems:`center`,justifyContent:`center`,children:[f,m]}),t[20]=f,t[21]=m,t[22]=h):h=t[22],h}var no=q`
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
`,ro=q`
  flex: 0 1 var(--global-dimension-size-2000);
  min-height: var(--global-dimension-size-750);
`;function io(e){let t=(0,Z.c)(3),{children:n}=e,r;t[0]===Symbol.for(`react.memo_cache_sentinel`)?(r=H(`div`,{css:ro,"aria-hidden":`true`}),t[0]=r):r=t[0];let i;return t[1]===n?i=t[2]:(i=U(`div`,{css:no,children:[r,n]}),t[1]=n,t[2]=i),i}var ao={size:`small`,icon:H(V,{svg:H(_t,{})})},oo={genericAdd:{size:`small`,icon:H(V,{svg:H(mt,{})})},genericEdit:{size:`small`,icon:H(V,{svg:H(xt,{})})},trace:{size:`large`,icon:H(V,{svg:H(on,{})})},dataset:{size:`large`,icon:H(V,{svg:H(ht,{})})},evaluator:{size:`large`,icon:H(V,{svg:H(Et,{})})},session:{size:`large`,icon:H(V,{svg:H(Vt,{})})},experiment:{size:`large`,icon:H(V,{svg:H(At,{})})},prompt:{size:`large`,icon:H(V,{svg:H(xn,{})})},project:{size:`large`,icon:H(V,{svg:H(st,{})})},annotation:{size:`small`,icon:H(V,{svg:H(zt,{})})},customAIProvider:{size:`small`,icon:H(V,{svg:H(Ve,{})})},event:{size:`small`,icon:H(V,{svg:H(gn,{})})},attribute:{size:`small`,icon:H(V,{svg:H(vn,{})})},config:{size:`small`,icon:H(V,{svg:H(lt,{})})},credential:{size:`small`,icon:H(V,{svg:H(an,{})})},version:{size:`small`,icon:H(V,{svg:H(Pt,{})})},tag:ao,label:ao,split:ao};Object.keys(oo),Object.fromEntries(Object.entries(oo).map(([e,t])=>[e,t.size]));var so=q`
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
`,co=(e,t)=>{let n=`linear-gradient(
    to bottom,
    transparent 0,
    #000 ${e},
    #000 calc(100% - ${t}),
    transparent 100%
  )`;return q`
    -webkit-mask-image: ${n};
    mask-image: ${n};
  `},lo=q`
  display: block;
  margin-bottom: calc(-1 * var(--global-dimension-size-200));
`,uo=e=>q`
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
`;function fo(e){let t=(0,Z.c)(14),{id:n,x:r,y:i,width:a,height:o}=e,s,c,l,u,d,f,p,m;t[0]===Symbol.for(`react.memo_cache_sentinel`)?(s=H(`feFlood`,{floodOpacity:`0`,result:`BackgroundImageFix`}),c=H(`feColorMatrix`,{in:`SourceAlpha`,type:`matrix`,values:`0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 127 0`,result:`hardAlpha`}),l=H(`feOffset`,{dy:`4`}),u=H(`feGaussianBlur`,{stdDeviation:`6`}),d=H(`feComposite`,{in2:`hardAlpha`,operator:`out`}),f=H(`feColorMatrix`,{type:`matrix`,values:`0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0.19 0`}),p=H(`feBlend`,{mode:`normal`,in2:`BackgroundImageFix`,result:`effect1_dropShadow`}),m=H(`feBlend`,{mode:`normal`,in:`SourceGraphic`,in2:`effect1_dropShadow`,result:`shape`}),t[0]=s,t[1]=c,t[2]=l,t[3]=u,t[4]=d,t[5]=f,t[6]=p,t[7]=m):(s=t[0],c=t[1],l=t[2],u=t[3],d=t[4],f=t[5],p=t[6],m=t[7]);let h;return t[8]!==o||t[9]!==n||t[10]!==a||t[11]!==r||t[12]!==i?(h=U(`filter`,{id:n,x:r,y:i,width:a,height:o,filterUnits:`userSpaceOnUse`,colorInterpolationFilters:`sRGB`,children:[s,c,l,u,d,f,p,m]}),t[8]=o,t[9]=n,t[10]=a,t[11]=r,t[12]=i,t[13]=h):h=t[13],h}function po(e){let t=(0,Z.c)(10),{x:n,y:r,size:i,icon:a}=e,o;t[0]===i?o=t[1]:(o=uo(i),t[0]=i,t[1]=o);let s;t[2]!==a||t[3]!==o?(s=H(`div`,{css:o,children:a}),t[2]=a,t[3]=o,t[4]=s):s=t[4];let c;return t[5]!==i||t[6]!==s||t[7]!==n||t[8]!==r?(c=H(`foreignObject`,{x:n,y:r,width:i,height:i,children:s}),t[5]=i,t[6]=s,t[7]=n,t[8]=r,t[9]=c):c=t[9],c}function mo(e){let t=(0,Z.c)(35),{icon:n,ids:r}=e,i;t[0]===Symbol.for(`react.memo_cache_sentinel`)?(i=[so,co(`34%`,`34%`),lo],t[0]=i):i=t[0];let a=`url(#${r.f0})`,o,s,c;t[1]===Symbol.for(`react.memo_cache_sentinel`)?(o=H(`rect`,{x:`19`,y:`10`,width:`160`,height:`32`,rx:`8`,fill:`var(--esg-card-bg)`,shapeRendering:`crispEdges`}),s=H(`rect`,{x:`19.5`,y:`10.5`,width:`159`,height:`31`,rx:`7.5`,stroke:`var(--esg-stroke)`,shapeRendering:`crispEdges`}),c=H(`rect`,{opacity:`0.68`,x:`31`,y:`22`,width:`136`,height:`8`,rx:`3`,fill:`var(--esg-bar)`}),t[1]=o,t[2]=s,t[3]=c):(o=t[1],s=t[2],c=t[3]);let l;t[4]===a?l=t[5]:(l=U(`g`,{filter:a,children:[o,s,c]}),t[4]=a,t[5]=l);let u=`url(#${r.f1})`,d,f;t[6]===Symbol.for(`react.memo_cache_sentinel`)?(d=H(`rect`,{x:`12`,y:`52`,width:`174`,height:`48`,rx:`8`,fill:`var(--esg-card-bg)`,shapeRendering:`crispEdges`}),f=H(`rect`,{x:`12.5`,y:`52.5`,width:`173`,height:`47`,rx:`7.5`,stroke:`var(--esg-stroke-subtle)`,shapeRendering:`crispEdges`}),t[6]=d,t[7]=f):(d=t[6],f=t[7]);let p;t[8]===n?p=t[9]:(p=H(po,{x:24,y:66,size:20,icon:n}),t[8]=n,t[9]=p);let m,h;t[10]===Symbol.for(`react.memo_cache_sentinel`)?(m=H(`rect`,{opacity:`0.68`,x:`56`,y:`65`,width:`120`,height:`8`,rx:`3`,fill:`var(--esg-bar)`}),h=H(`rect`,{opacity:`0.68`,x:`56`,y:`79`,width:`80`,height:`8`,rx:`3`,fill:`var(--esg-bar)`}),t[10]=m,t[11]=h):(m=t[10],h=t[11]);let g;t[12]!==p||t[13]!==u?(g=U(`g`,{filter:u,children:[d,f,p,m,h]}),t[12]=p,t[13]=u,t[14]=g):g=t[14];let _=`url(#${r.f2})`,v,y,b;t[15]===Symbol.for(`react.memo_cache_sentinel`)?(v=H(`rect`,{x:`19`,y:`110`,width:`160`,height:`32`,rx:`8`,fill:`var(--esg-card-bg)`,shapeRendering:`crispEdges`}),y=H(`rect`,{x:`19.5`,y:`110.5`,width:`159`,height:`31`,rx:`7.5`,stroke:`var(--esg-stroke)`,shapeRendering:`crispEdges`}),b=H(`rect`,{opacity:`0.68`,x:`31`,y:`122`,width:`136`,height:`8`,rx:`3`,fill:`var(--esg-bar)`}),t[15]=v,t[16]=y,t[17]=b):(v=t[15],y=t[16],b=t[17]);let x;t[18]===_?x=t[19]:(x=U(`g`,{filter:_,children:[v,y,b]}),t[18]=_,t[19]=x);let S;t[20]===r.f0?S=t[21]:(S=H(fo,{id:r.f0,x:7,y:2,width:184,height:56}),t[20]=r.f0,t[21]=S);let C;t[22]===r.f1?C=t[23]:(C=H(fo,{id:r.f1,x:0,y:44,width:198,height:72}),t[22]=r.f1,t[23]=C);let w;t[24]===r.f2?w=t[25]:(w=H(fo,{id:r.f2,x:7,y:102,width:184,height:56}),t[24]=r.f2,t[25]=w);let T;t[26]!==S||t[27]!==C||t[28]!==w?(T=U(`defs`,{children:[S,C,w]}),t[26]=S,t[27]=C,t[28]=w,t[29]=T):T=t[29];let E;return t[30]!==g||t[31]!==x||t[32]!==T||t[33]!==l?(E=U(`svg`,{width:`198`,height:`158`,viewBox:`0 0 198 158`,fill:`none`,xmlns:`http://www.w3.org/2000/svg`,"aria-hidden":`true`,focusable:`false`,css:i,children:[l,g,x,T]}),t[30]=g,t[31]=x,t[32]=T,t[33]=l,t[34]=E):E=t[34],E}function ho(e){let t=(0,Z.c)(40),{icon:n,ids:r}=e,i;t[0]===Symbol.for(`react.memo_cache_sentinel`)?(i=[so,co(`38%`,`31%`),lo],t[0]=i):i=t[0];let a=`url(#${r.f0})`,o,s,c,l,u,d;t[1]===Symbol.for(`react.memo_cache_sentinel`)?(o=H(`rect`,{x:`12`,y:`8`,width:`174`,height:`32`,rx:`8`,fill:`var(--esg-card-bg)`,shapeRendering:`crispEdges`}),s=H(`rect`,{x:`12.5`,y:`8.5`,width:`173`,height:`31`,rx:`7.5`,stroke:`var(--esg-stroke)`,shapeRendering:`crispEdges`}),c=H(`path`,{d:`M27.75 22.5C28.5784 22.5 29.25 23.1716 29.25 24C29.25 24.8284 28.5784 25.5 27.75 25.5C26.9216 25.5 26.25 24.8284 26.25 24C26.25 23.1716 26.9216 22.5 27.75 22.5Z`,fill:`var(--esg-dots)`}),l=H(`path`,{d:`M33 22.5C33.8284 22.5 34.5 23.1716 34.5 24C34.5 24.8284 33.8284 25.5 33 25.5C32.1716 25.5 31.5 24.8284 31.5 24C31.5 23.1716 32.1716 22.5 33 22.5Z`,fill:`var(--esg-dots)`}),u=H(`path`,{d:`M38.25 22.5C39.0784 22.5 39.75 23.1716 39.75 24C39.75 24.8284 39.0784 25.5 38.25 25.5C37.4216 25.5 36.75 24.8284 36.75 24C36.75 23.1716 37.4216 22.5 38.25 22.5Z`,fill:`var(--esg-dots)`}),d=H(`rect`,{opacity:`0.68`,x:`54`,y:`20`,width:`120`,height:`8`,rx:`3`,fill:`var(--esg-bar)`}),t[1]=o,t[2]=s,t[3]=c,t[4]=l,t[5]=u,t[6]=d):(o=t[1],s=t[2],c=t[3],l=t[4],u=t[5],d=t[6]);let f;t[7]===a?f=t[8]:(f=U(`g`,{filter:a,children:[o,s,c,l,u,d]}),t[7]=a,t[8]=f);let p=`url(#${r.f1})`,m,h;t[9]===Symbol.for(`react.memo_cache_sentinel`)?(m=H(`rect`,{x:`12`,y:`50`,width:`174`,height:`32`,rx:`8`,fill:`var(--esg-card-bg)`,shapeRendering:`crispEdges`}),h=H(`rect`,{x:`12.5`,y:`50.5`,width:`173`,height:`31`,rx:`7.5`,stroke:`var(--esg-stroke-subtle)`,shapeRendering:`crispEdges`}),t[9]=m,t[10]=h):(m=t[9],h=t[10]);let g;t[11]===n?g=t[12]:(g=H(po,{x:25,y:58,size:16,icon:n}),t[11]=n,t[12]=g);let _;t[13]===Symbol.for(`react.memo_cache_sentinel`)?(_=H(`rect`,{opacity:`0.68`,x:`54`,y:`62`,width:`120`,height:`8`,rx:`3`,fill:`var(--esg-bar)`}),t[13]=_):_=t[13];let v;t[14]!==p||t[15]!==g?(v=U(`g`,{filter:p,children:[m,h,g,_]}),t[14]=p,t[15]=g,t[16]=v):v=t[16];let y=`url(#${r.f2})`,b,x,S,C,w,T;t[17]===Symbol.for(`react.memo_cache_sentinel`)?(b=H(`rect`,{x:`12`,y:`92`,width:`174`,height:`32`,rx:`8`,fill:`var(--esg-card-bg)`,shapeRendering:`crispEdges`}),x=H(`rect`,{x:`12.5`,y:`92.5`,width:`173`,height:`31`,rx:`7.5`,stroke:`var(--esg-stroke)`,shapeRendering:`crispEdges`}),S=H(`path`,{d:`M27.75 106.5C28.5784 106.5 29.25 107.172 29.25 108C29.25 108.828 28.5784 109.5 27.75 109.5C26.9216 109.5 26.25 108.828 26.25 108C26.25 107.172 26.9216 106.5 27.75 106.5Z`,fill:`var(--esg-dots)`}),C=H(`path`,{d:`M33 106.5C33.8284 106.5 34.5 107.172 34.5 108C34.5 108.828 33.8284 109.5 33 109.5C32.1716 109.5 31.5 108.828 31.5 108C31.5 107.172 32.1716 106.5 33 106.5Z`,fill:`var(--esg-dots)`}),w=H(`path`,{d:`M38.25 106.5C39.0784 106.5 39.75 107.172 39.75 108C39.75 108.828 39.0784 109.5 38.25 109.5C37.4216 109.5 36.75 108.828 36.75 108C36.75 107.172 37.4216 106.5 38.25 106.5Z`,fill:`var(--esg-dots)`}),T=H(`rect`,{opacity:`0.68`,x:`54`,y:`104`,width:`120`,height:`8`,rx:`3`,fill:`var(--esg-bar)`}),t[17]=b,t[18]=x,t[19]=S,t[20]=C,t[21]=w,t[22]=T):(b=t[17],x=t[18],S=t[19],C=t[20],w=t[21],T=t[22]);let E;t[23]===y?E=t[24]:(E=U(`g`,{filter:y,children:[b,x,S,C,w,T]}),t[23]=y,t[24]=E);let D;t[25]===r.f0?D=t[26]:(D=H(fo,{id:r.f0,x:0,y:0,width:198,height:56}),t[25]=r.f0,t[26]=D);let O;t[27]===r.f1?O=t[28]:(O=H(fo,{id:r.f1,x:0,y:42,width:198,height:56}),t[27]=r.f1,t[28]=O);let k;t[29]===r.f2?k=t[30]:(k=H(fo,{id:r.f2,x:0,y:84,width:198,height:56}),t[29]=r.f2,t[30]=k);let A;t[31]!==D||t[32]!==O||t[33]!==k?(A=U(`defs`,{children:[D,O,k]}),t[31]=D,t[32]=O,t[33]=k,t[34]=A):A=t[34];let j;return t[35]!==v||t[36]!==E||t[37]!==A||t[38]!==f?(j=U(`svg`,{width:`198`,height:`140`,viewBox:`0 0 198 140`,fill:`none`,xmlns:`http://www.w3.org/2000/svg`,"aria-hidden":`true`,focusable:`false`,css:i,children:[f,v,E,A]}),t[35]=v,t[36]=E,t[37]=A,t[38]=f,t[39]=j):j=t[39],j}function go(e){let t=(0,Z.c)(8),{variant:n}=e,{size:r,icon:i}=oo[n===void 0?`genericAdd`:n],a=(0,X.useId)(),o=`${a}-f0`,s=`${a}-f1`,c=`${a}-f2`,l;t[0]!==o||t[1]!==s||t[2]!==c?(l={f0:o,f1:s,f2:c},t[0]=o,t[1]=s,t[2]=c,t[3]=l):l=t[3];let u=l,d;return t[4]!==i||t[5]!==u||t[6]!==r?(d=H(r===`small`?ho:mo,{icon:i,ids:u}),t[4]=i,t[5]=u,t[6]=r,t[7]=d):d=t[7],d}function _o(e){let t=(0,Z.c)(2),{children:n}=e;if(typeof n==`string`){let e;return t[0]===n?e=t[1]:(e=H(Xe,{level:1,children:n}),t[0]=n,t[1]=e),e}return n}function vo(e){let t=(0,Z.c)(2),{children:n}=e;if(!n)return null;if(typeof n==`string`){let e;return t[0]===n?e=t[1]:(e=H(B,{size:`S`,color:`text-700`,children:n}),t[0]=n,t[1]=e),e}return n}function yo(e){let t=(0,Z.c)(10),{title:n,subTitle:r,extra:i}=e,a;t[0]===n?a=t[1]:(a=H(_o,{children:n}),t[0]=n,t[1]=a);let o;t[2]===r?o=t[3]:(o=H(vo,{children:r}),t[2]=r,t[3]=o);let s;t[4]!==a||t[5]!==o?(s=U(K,{direction:`column`,gap:`size-50`,minWidth:0,children:[a,o]}),t[4]=a,t[5]=o,t[6]=s):s=t[6];let c;return t[7]!==i||t[8]!==s?(c=H(Ai,{padding:`size-200`,flex:`none`,"data-testid":`page-header`,children:U(K,{direction:`row`,justifyContent:`space-between`,alignItems:`center`,"data-testid":`page-header-content`,gap:`size-100`,children:[s,i]})}),t[7]=i,t[8]=s,t[9]=c):c=t[9],c}var bo=q`
  border-radius: 16px;
  padding: var(--global-dimension-size-50) var(--global-dimension-size-200) !important;
`,xo=e=>{let t=(0,Z.c)(10),{onLoadMore:n,isLoadingNext:r,buttonProps:i}=e,a;t[0]===n?a=t[1]:(a=()=>{n()},t[0]=n,t[1]=a);let o;t[2]===r?o=t[3]:(o=r?H(V,{svg:H(qt,{})}):void 0,t[2]=r,t[3]=o);let s=r?`Loading...`:`Load More`,c;return t[4]!==i||t[5]!==r||t[6]!==a||t[7]!==o||t[8]!==s?(c=H(W,{onPress:a,size:`S`,css:bo,isDisabled:r,leadingVisual:o,...i,children:s}),t[4]=i,t[5]=r,t[6]=a,t[7]=o,t[8]=s,t[9]=c):c=t[9],c};function So(e,{filled:t}={filled:!0}){let n;switch(e){case`warning`:n=H(t?Ft:at,{});break;case`info`:n=H(t?Wt:vn,{});break;case`danger`:n=H(t?pn:ct,{});break;case`success`:n=H(t?Cn:Lt,{});break}return H(V,{svg:n})}var Co=q`
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
`,wo=q`
  display: flex;
  flex-direction: row;
  align-items: flex-start;
  flex: 1 1 auto;
`,To=q`
  background-color: transparent;
  color: inherit;
  padding: 0;
  border: none;
  cursor: pointer;
  width: 20px;
  height: 20px;
  margin-left: var(--global-dimension-size-200);
`,Eo=e=>{let t=(0,Z.c)(35),n,r,i,a,o,s,c,l,u,d;t[0]===e?(n=t[1],r=t[2],i=t[3],a=t[4],o=t[5],s=t[6],c=t[7],l=t[8],u=t[9],d=t[10]):({variant:d,title:u,icon:i,children:n,showIcon:s,dismissable:c,onDismissClick:a,banner:l,extra:r,...o}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a,t[5]=o,t[6]=s,t[7]=c,t[8]=l,t[9]=u,t[10]=d);let f=s===void 0||s,p=c!==void 0&&c,m=l!==void 0&&l,{theme:h}=pr();if(!i&&f){let e;t[11]===d?e=t[12]:(e=So(d),t[11]=d,t[12]=e),i=e}let g=!!u,_;t[13]===u?_=t[14]:(_=u?H(B,{elementType:`h5`,size:`M`,weight:`heavy`,color:`inherit`,children:u}):null,t[13]=u,t[14]=_);let v;t[15]===n?v=t[16]:(v=H(B,{color:`inherit`,size:`S`,children:n}),t[15]=n,t[16]=v);let y;t[17]!==_||t[18]!==v?(y=U(`div`,{children:[_,v]}),t[17]=_,t[18]=v,t[19]=y):y=t[19];let b;t[20]!==i||t[21]!==y?(b=U(`div`,{css:wo,className:`alert__icon-title-wrap`,children:[i,y]}),t[20]=i,t[21]=y,t[22]=b):b=t[22];let x;t[23]!==p||t[24]!==a?(x=p?H(`button`,{css:To,onClick:a,children:H(V,{svg:H(wt,{})})}):null,t[23]=p,t[24]=a,t[25]=x):x=t[25];let S;return t[26]!==m||t[27]!==r||t[28]!==o||t[29]!==g||t[30]!==b||t[31]!==x||t[32]!==h||t[33]!==d?(S=U(`div`,{...o,css:Co,"data-variant":d,"data-banner":m,"data-has-title":g,"data-theme":h,children:[b,r,x]}),t[26]=m,t[27]=r,t[28]=o,t[29]=g,t[30]=b,t[31]=x,t[32]=h,t[33]=d,t[34]=S):S=t[34],S},Do=q`
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
`,Oo=e=>{let t=(0,Z.c)(17),n,r,i,a,o,s;t[0]===e?(n=t[1],r=t[2],i=t[3],a=t[4],o=t[5],s=t[6]):({children:n,variant:a,size:o,overflowMode:s,css:i,...r}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a,t[5]=o,t[6]=s);let c=a===void 0?`default`:a,l=o===void 0?`S`:o,u=s===void 0?`wrap`:s,{theme:d}=pr(),f;t[7]===i?f=t[8]:(f=q(Do,i),t[7]=i,t[8]=f);let p;return t[9]!==n||t[10]!==r||t[11]!==u||t[12]!==l||t[13]!==f||t[14]!==d||t[15]!==c?(p=H(`span`,{...r,css:f,"data-variant":c,"data-size":l,"data-overflow-mode":u,"data-theme":d,className:`badge`,children:n}),t[9]=n,t[10]=r,t[11]=u,t[12]=l,t[13]=f,t[14]=d,t[15]=c,t[16]=p):p=t[16],p},ko=q`
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
`,Ao=q`
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
`,jo=e=>{let t=(0,Z.c)(14),n,r,i,a;t[0]===e?(n=t[1],r=t[2],i=t[3],a=t[4]):({className:n,css:r,size:a,...i}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a);let s;t[5]===n?s=t[6]:(s=z(`disclosure-group`,n),t[5]=n,t[6]=s);let c;t[7]===r?c=t[8]:(c=q(ko,r),t[7]=r,t[8]=c);let l;return t[9]!==i||t[10]!==a||t[11]!==s||t[12]!==c?(l=H(o,{allowsMultipleExpanded:!0,className:s,css:c,"data-size":a,...i}),t[9]=i,t[10]=a,t[11]=s,t[12]=c,t[13]=l):l=t[13],l},Mo=e=>{let t=(0,Z.c)(10),n,r,i;t[0]===e?(n=t[1],r=t[2],i=t[3]):({size:i,className:n,...r}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i);let a;t[4]===n?a=t[5]:(a=z(`disclosure`,n),t[4]=n,t[5]=a);let o;return t[6]!==r||t[7]!==i||t[8]!==a?(o=H(w,{className:a,css:Ao,"data-size":i,defaultExpanded:!0,...r}),t[6]=r,t[7]=i,t[8]=a,t[9]=o):o=t[9],o},No=e=>{let t=(0,Z.c)(8),n,r;t[0]===e?(n=t[1],r=t[2]):({className:n,...r}=e,t[0]=e,t[1]=n,t[2]=r);let i;t[3]===n?i=t[4]:(i=z(`disclosure__panel`,n),t[3]=n,t[4]=i);let a;return t[5]!==r||t[6]!==i?(a=H(Fe,{className:i,...r}),t[5]=r,t[6]=i,t[7]=a):a=t[7],a},Po=e=>{let t=(0,Z.c)(15),{children:n,arrowPosition:r,justifyContent:i,alignItems:a,direction:o,width:s}=e,c=a===void 0?`center`:a,l=o===void 0?`row`:o,u;t[0]===s?u=t[1]:(u={width:s},t[0]=s,t[1]=u);let d=l===`row`?`size-100`:`size-50`,f;t[2]!==c||t[3]!==n||t[4]!==l||t[5]!==i||t[6]!==d?(f=H(K,{justifyContent:i,direction:l,alignItems:c,width:`100%`,gap:d,children:n}),t[2]=c,t[3]=n,t[4]=l,t[5]=i,t[6]=d,t[7]=f):f=t[7];let p;t[8]===r?p=t[9]:(p=r===`none`?null:H(V,{svg:H(On,{})}),t[8]=r,t[9]=p);let m;return t[10]!==r||t[11]!==u||t[12]!==f||t[13]!==p?(m=H(Ge,{className:`react-aria-Heading disclosure__trigger`,children:U(Tt,{slot:`trigger`,"data-arrow-position":r,style:u,children:[f,p]})}),t[10]=r,t[11]=u,t[12]=f,t[13]=p,t[14]=m):m=t[14],m},Fo=q`
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
    min-width: var(--global-input-field-min-width);
    background-color: var(--field-background-color);
    color: var(--field-text-color);
    border: var(--global-border-size-thin) solid var(--field-border-color);
    border-radius: var(--global-rounding-small);
    vertical-align: middle;

    &[data-focused] {
      // State-specific selectors below provide the visible focus treatment.
      outline: none;
    }
    &[data-focused]:not([data-invalid]) {
      border-color: var(--field-border-color-active);
      outline: var(--focus-ring-thickness) solid
        var(--field-border-color-active);
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
`,Io=q`
  width: var(--trigger-width);
  background-color: var(--field-popover-background-color);
  border-radius: var(--global-rounding-small);
  color: var(--field-text-color);
  box-shadow: 0px 4px 10px var(--field-popover-shadow-color);
  border: 1px solid var(--field-popover-border-color);
  max-height: inherit;
`,Lo=q`
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
  // inherited from fieldBaseCSS (always composed before this). textFieldCSS only
  // layers on sizing and swaps the focus ring from a border to an outline.
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
      outline: var(--focus-ring-thickness) solid
        var(--field-border-color-active);
    }
    &[data-focused][data-invalid] {
      border-width: var(--global-border-size-thin);
      outline: var(--focus-ring-thickness) solid
        var(--field-invalid-border-color);
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
`,Ro=q`
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
`,zo=q(Io,q`
    .react-aria-ListBox {
      display: block;
      width: unset;
      max-height: inherit;
      min-height: unset;
      border: none;
      overflow: auto;
    }
  `),Bo=q`
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
`,Vo=e=>{e.stopPropagation()};function Ho(e){let t=(0,Z.c)(46),n,r,i,a,o,s,c,l,d,p,m,h;t[0]===e?(n=t[1],r=t[2],i=t[3],a=t[4],o=t[5],s=t[6],c=t[7],l=t[8],d=t[9],p=t[10],m=t[11],h=t[12]):({label:o,placeholder:s,description:r,errorMessage:i,children:n,size:p,width:h,stopPropagation:d,renderEmptyState:l,isInvalid:a,menuTrigger:m,...c}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a,t[5]=o,t[6]=s,t[7]=c,t[8]=l,t[9]=d,t[10]=p,t[11]=m,t[12]=h);let g=p===void 0?`M`:p,_=m===void 0?`focus`:m,v;t[13]===Symbol.for(`react.memo_cache_sentinel`)?(v=q(Fo,Ro),t[13]=v):v=t[13];let x=a||!!i,S;t[14]===h?S=t[15]:(S={width:h},t[14]=h,t[15]=S);let C=!!l,w;t[16]===o?w=t[17]:(w=o&&H(yn,{children:o}),t[16]=o,t[17]=w);let T=d?Vo:void 0,E=d?Vo:void 0,D=d?Vo:void 0,O;t[18]===s?O=t[19]:(O=H(f,{placeholder:s}),t[18]=s,t[19]=O);let k;t[20]===Symbol.for(`react.memo_cache_sentinel`)?(k=H(Tt,{children:H(nt,{})}),t[20]=k):k=t[20];let A;t[21]!==D||t[22]!==O||t[23]!==T||t[24]!==E?(A=U(`div`,{className:`combobox__container`,onClick:T,onKeyDown:E,onKeyUp:D,children:[O,k]}),t[21]=D,t[22]=O,t[23]=T,t[24]=E,t[25]=A):A=t[25];let j;t[26]!==r||t[27]!==i?(j=r&&!i?H(bt,{slot:`description`,children:r}):null,t[26]=r,t[27]=i,t[28]=j):j=t[28];let M;t[29]===i?M=t[30]:(M=H(u,{children:i}),t[29]=i,t[30]=M);let N;t[31]!==n||t[32]!==l?(N=H(It,{css:zo,children:H(y,{renderEmptyState:l,children:n})}),t[31]=n,t[32]=l,t[33]=N):N=t[33];let P;return t[34]!==_||t[35]!==c||t[36]!==g||t[37]!==A||t[38]!==j||t[39]!==M||t[40]!==N||t[41]!==x||t[42]!==S||t[43]!==C||t[44]!==w?(P=U(b,{...c,menuTrigger:_,css:v,"data-size":g,isInvalid:x,style:S,allowsEmptyCollection:C,children:[w,A,j,M,N]}),t[34]=_,t[35]=c,t[36]=g,t[37]=A,t[38]=j,t[39]=M,t[40]=N,t[41]=x,t[42]=S,t[43]=C,t[44]=w,t[45]=P):P=t[45],P}function Uo(e){let t=(0,Z.c)(8),n,r;t[0]===e?(n=t[1],r=t[2]):({children:n,...r}=e,t[0]=e,t[1]=n,t[2]=r);let i;t[3]===n?i=t[4]:(i=e=>{let{isSelected:t}=e;return U(G,{children:[n,t&&H(V,{svg:H(Yt,{}),className:`menu-item__selected-checkmark`})]})},t[3]=n,t[4]=i);let a;return t[5]!==r||t[6]!==i?(a=H(x,{...r,css:Bo,children:i}),t[5]=r,t[6]=i,t[7]=a):a=t[7],a}function Wo(e){let t=(0,Z.c)(11),n,r;t[0]===e?(n=t[1],r=t[2]):({ref:r,...n}=e,t[0]=e,t[1]=n,t[2]=r);let i,a;t[3]===n?(i=t[4],a=t[5]):({size:a,...i}=n,t[3]=n,t[4]=i,t[5]=a);let o=a===void 0?`M`:a,s;t[6]===Symbol.for(`react.memo_cache_sentinel`)?(s=q(Fo,Lo),t[6]=s):s=t[6];let c;return t[7]!==i||t[8]!==r||t[9]!==o?(c=H(De,{"data-size":o,className:`text-field`,ref:r,...i,css:s}),t[7]=i,t[8]=r,t[9]=o,t[10]=c):c=t[10],c}var Go=()=>{let e=(0,Z.c)(1),t;return e[0]===Symbol.for(`react.memo_cache_sentinel`)?(t=H(V,{className:`search-field__icon`,svg:H(Mt,{})}),e[0]=t):t=e[0],t},Ko=q`
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

  /* Left padding when icon present: inset + icon + gap (gap = inset) */
  .search-field__icon ~ .react-aria-Input {
    padding-left: calc(
      var(--textfield-horizontal-padding) * 2 + var(--searchfield-icon-size)
    ) !important;
  }

  /* Right padding for clear button: inset + icon + gap */
  .react-aria-Input {
    padding-right: calc(
      var(--textfield-horizontal-padding) * 2 + var(--searchfield-icon-size)
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
`;function qo(e){let t=(0,Z.c)(20),n,r;t[0]===e?(n=t[1],r=t[2]):({ref:r,...n}=e,t[0]=e,t[1]=n,t[2]=r);let i,a,o,s,c;t[3]===n?(i=t[4],a=t[5],o=t[6],s=t[7],c=t[8]):({size:s,variant:c,children:i,isReadOnly:a,...o}=n,t[3]=n,t[4]=i,t[5]=a,t[6]=o,t[7]=s,t[8]=c);let l=s===void 0?`M`:s,u=c===void 0?`default`:c,d;t[9]===Symbol.for(`react.memo_cache_sentinel`)?(d=q(Fo,Lo,Ko),t[9]=d):d=t[9];let f;t[10]!==i||t[11]!==a?(f=e=>U(G,{children:[typeof i==`function`?i(e):i,!a&&H(Tt,{slot:`clear`,className:`search-field__clear`,"data-empty":e.isEmpty||void 0,children:H(V,{svg:H(wt,{})})})]}),t[10]=i,t[11]=a,t[12]=f):f=t[12];let p;return t[13]!==a||t[14]!==o||t[15]!==r||t[16]!==l||t[17]!==f||t[18]!==u?(p=H(se,{"data-size":l,"data-variant":u,className:`search-field`,ref:r,isReadOnly:a,...o,css:d,children:f}),t[13]=a,t[14]=o,t[15]=r,t[16]=l,t[17]=f,t[18]=u,t[19]=p):p=t[19],p}var Jo=q`
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
`;function Yo(e){let t=(0,Z.c)(2),n;return t[0]===e.children?n=t[1]:(n=H(`div`,{className:`composite-field`,css:Jo,children:e.children}),t[0]=e.children,t[1]=n),n}function Xo(e){let t=(0,Z.c)(16),n,r;t[0]===e?(n=t[1],r=t[2]):({ref:r,...n}=e,t[0]=e,t[1]=n,t[2]=r);let i,a,o;t[3]===n?(i=t[4],a=t[5],o=t[6]):({size:o,children:i,...a}=n,t[3]=n,t[4]=i,t[5]=a,t[6]=o);let s=o===void 0?`M`:o,c;t[7]===Symbol.for(`react.memo_cache_sentinel`)?(c=q(Fo,Lo),t[7]=c):c=t[7];let l;t[8]!==i||t[9]!==a||t[10]!==r||t[11]!==s?(l=H(De,{"data-size":s,className:`copy-field`,isReadOnly:!0,ref:r,...a,css:c,children:i}),t[8]=i,t[9]=a,t[10]=r,t[11]=s,t[12]=l):l=t[12];let u;return t[13]!==s||t[14]!==l?(u=H(ft,{size:s,children:l}),t[13]=s,t[14]=l,t[15]=u):u=t[15],u}var Zo=2e3;function Qo(e){let t=(0,Z.c)(30),n,r;t[0]===e?(n=t[1],r=t[2]):({ref:r,...n}=e,t[0]=e,t[1]=n,t[2]=r);let i=yt(),a,o;t[3]===n?(a=t[4],o=t[5]):({disabled:a,...o}=n,t[3]=n,t[4]=a,t[5]=o);let[s,c]=(0,X.useState)(!1),l=(0,X.useRef)(null),u;t[6]===Symbol.for(`react.memo_cache_sentinel`)?(u=()=>{Ie(l.current?.value??``),c(!0),setTimeout(()=>{c(!1)},Zo)},t[6]=u):u=t[6];let d=u,p;t[7]===Symbol.for(`react.memo_cache_sentinel`)?(p=q`
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
      `,t[7]=p):p=t[7];let m;t[8]===r?m=t[9]:(m=e=>{l.current=e,typeof r==`function`?r(e):r&&(r.current=e)},t[8]=r,t[9]=m);let h;t[10]!==a||t[11]!==o||t[12]!==m?(h=H(f,{...o,ref:m,type:`text`,readOnly:!0,disabled:a}),t[10]=a,t[11]=o,t[12]=m,t[13]=h):h=t[13];let _=s?`Copied`:`Copy to clipboard`,v=s?`success`:`inherit`,y=s?`Checkmark`:`Duplicate`,b;t[14]!==v||t[15]!==y?(b=H(V,{color:v,svgKey:y}),t[14]=v,t[15]=y,t[16]=b):b=t[16];let x;t[17]!==a||t[18]!==_||t[19]!==b?(x=H(Tt,{className:`copy-input__copy-button`,onPress:d,isDisabled:a,"aria-label":_,children:b}),t[17]=a,t[18]=_,t[19]=b,t[20]=x):x=t[20];let S=s?`Copied`:`Copy`,C;t[21]===S?C=t[22]:(C=H(Ni,{offset:1,children:S}),t[21]=S,t[22]=C);let w;t[23]!==C||t[24]!==x?(w=U(g,{children:[x,C]}),t[23]=C,t[24]=x,t[25]=w):w=t[25];let T;return t[26]!==i||t[27]!==w||t[28]!==h?(T=U(`div`,{"data-size":i,"data-testid":`copy-input`,css:p,children:[h,w]}),t[26]=i,t[27]=w,t[28]=h,t[29]=T):T=t[29],T}var $o=(0,X.createContext)(null);function es(){let e=(0,X.useContext)($o);if(!e)throw Error(`useCredentialContext must be used within a CredentialContext.Provider`);return e}function ts(e){let t=(0,Z.c)(21),n,r;t[0]===e?(n=t[1],r=t[2]):({ref:r,...n}=e,t[0]=e,t[1]=n,t[2]=r);let i,a,o;t[3]===n?(i=t[4],a=t[5],o=t[6]):({size:o,children:i,...a}=n,t[3]=n,t[4]=i,t[5]=a,t[6]=o);let s=o===void 0?`M`:o,[c,l]=(0,X.useState)(!1),u;t[7]===c?u=t[8]:(u={isVisible:c,setIsVisible:l},t[7]=c,t[8]=u);let d;t[9]===Symbol.for(`react.memo_cache_sentinel`)?(d=q(Fo,Lo),t[9]=d):d=t[9];let f;t[10]!==i||t[11]!==a||t[12]!==r||t[13]!==s?(f=H(De,{"data-size":s,className:`credential-field`,autoComplete:`off`,ref:r,...a,css:d,children:i}),t[10]=i,t[11]=a,t[12]=r,t[13]=s,t[14]=f):f=t[14];let p;t[15]!==s||t[16]!==f?(p=H(ft,{size:s,children:f}),t[15]=s,t[16]=f,t[17]=p):p=t[17];let m;return t[18]!==u||t[19]!==p?(m=H($o.Provider,{value:u,children:p}),t[18]=u,t[19]=p,t[20]=m):m=t[20],m}function ns(e){let t=(0,Z.c)(28),n,r;t[0]===e?(n=t[1],r=t[2]):({ref:r,...n}=e,t[0]=e,t[1]=n,t[2]=r);let{isVisible:i,setIsVisible:a}=es(),o=yt(),s,c,l;t[3]===n?(s=t[4],c=t[5],l=t[6]):({disabled:s,readOnly:l,...c}=n,t[3]=n,t[4]=s,t[5]=c,t[6]=l);let u;t[7]===Symbol.for(`react.memo_cache_sentinel`)?(u=q`
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
      `,t[7]=u):u=t[7];let d=i?`text`:`password`,p;t[8]!==s||t[9]!==c||t[10]!==l||t[11]!==r||t[12]!==d?(p=H(f,{...c,ref:r,type:d,disabled:s,readOnly:l}),t[8]=s,t[9]=c,t[10]=l,t[11]=r,t[12]=d,t[13]=p):p=t[13];let m;t[14]!==i||t[15]!==a?(m=()=>a(!i),t[14]=i,t[15]=a,t[16]=m):m=t[16];let h=s||l,g=i?`Hide credential`:`Show credential`,_;t[17]===i?_=t[18]:(_=H(V,{svg:H(i?Dt:Nt,{})}),t[17]=i,t[18]=_);let v;t[19]!==m||t[20]!==h||t[21]!==g||t[22]!==_?(v=H(Tt,{className:`credential-input__toggle`,onPress:m,isDisabled:h,"aria-label":g,children:_}),t[19]=m,t[20]=h,t[21]=g,t[22]=_,t[23]=v):v=t[23];let y;return t[24]!==o||t[25]!==p||t[26]!==v?(y=U(`div`,{"data-size":o,"data-testid":`credential-input`,css:u,children:[p,v]}),t[24]=o,t[25]=p,t[26]=v,t[27]=y):y=t[27],y}var rs=``,is=`${rs}REDACTED${rs}`;function as(e){return typeof e==`string`&&e.startsWith(is)}function os(e){let t=e.slice(is.length),n=t.indexOf(rs);return n<0?null:t.slice(0,n)||null}function ss(e){if(!as(e))return null;let t=os(e);return t?`••••${t}`:`••••••••`}function cs(e){let t=(0,Z.c)(29),{label:n,placeholder:r,description:i,value:a,onChange:o,onBlur:s,name:c,isDisabled:l,isRequired:d,errorMessage:p,size:m}=e,h=m===void 0?`M`:m,[g,_]=(0,X.useState)(!1),v;t[0]!==g||t[1]!==a?(v=!g&&as(a),t[0]=g,t[1]=a,t[2]=v):v=t[2];let y=v,b=y?``:a??``,x;t[3]!==r||t[4]!==y||t[5]!==a?(x=y?ss(a)??`••••••••`:r,t[3]=r,t[4]=y,t[5]=a,t[6]=x):x=t[6];let S=x,C;t[7]!==g||t[8]!==o?(C=e=>{g||_(!0),o(e)},t[7]=g,t[8]=o,t[9]=C):C=t[9];let w=C,T=!!p,E;t[10]===n?E=t[11]:(E=H(yn,{children:n}),t[10]=n,t[11]=E);let D;t[12]===S?D=t[13]:(D=H(f,{placeholder:S}),t[12]=S,t[13]=D);let O;t[14]!==i||t[15]!==p?(O=p?H(u,{children:p}):i?H(B,{slot:`description`,children:i}):null,t[14]=i,t[15]=p,t[16]=O):O=t[16];let k;return t[17]!==b||t[18]!==w||t[19]!==l||t[20]!==d||t[21]!==c||t[22]!==s||t[23]!==h||t[24]!==T||t[25]!==E||t[26]!==D||t[27]!==O?(k=U(Wo,{type:`password`,size:h,name:c,value:b,onChange:w,onBlur:s,isDisabled:l,isRequired:d,isInvalid:T,autoComplete:`off`,children:[E,D,O]}),t[17]=b,t[18]=w,t[19]=l,t[20]=d,t[21]=c,t[22]=s,t[23]=h,t[24]=T,t[25]=E,t[26]=D,t[27]=O,t[28]=k):k=t[28],k}var ls=q`
  .react-aria-Input {
    text-align: right;
    font-feature-settings: "tnum" 1;
  }
`;function us(e){let t=(0,Z.c)(13),n,r,i,a,o;if(t[0]!==e){let{ref:s,...c}=e;r=s;let{size:l,...u}=c,d=l===void 0?`M`:l;n=ue,i=d,a=u,o=z(`text-field react-aria-NumberField`,c.className),t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a,t[5]=o}else n=t[1],r=t[2],i=t[3],a=t[4],o=t[5];let s;t[6]===Symbol.for(`react.memo_cache_sentinel`)?(s=q(Fo,Lo,ls),t[6]=s):s=t[6];let c;return t[7]!==n||t[8]!==r||t[9]!==i||t[10]!==a||t[11]!==o?(c=H(n,{"data-size":i,...a,className:o,ref:r,css:s}),t[7]=n,t[8]=r,t[9]=i,t[10]=a,t[11]=o,t[12]=c):c=t[12],c}var ds=e(R());function fs(e){let t=(0,Z.c)(19),n,r,i,a;t[0]===e?(n=t[1],r=t[2],i=t[3],a=t[4]):({onChange:i,debounceMs:a,placeholder:n,...r}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a);let o=a===void 0?200:a,s;t[5]===i?s=t[6]:(s=e=>{(0,X.startTransition)(()=>{i(e)})},t[5]=i,t[6]=s);let c;t[7]!==o||t[8]!==s?(c=(0,ds.default)(s,o),t[7]=o,t[8]=s,t[9]=c):c=t[9];let l=c,u;t[10]===l?u=t[11]:(u=e=>{l(e)},t[10]=l,t[11]=u);let d=u,p;t[12]===Symbol.for(`react.memo_cache_sentinel`)?(p=H(Go,{}),t[12]=p):p=t[12];let m;t[13]===n?m=t[14]:(m=H(f,{placeholder:n}),t[13]=n,t[14]=m);let h;return t[15]!==d||t[16]!==r||t[17]!==m?(h=U(qo,{onChange:d,...r,children:[p,m]}),t[15]=d,t[16]=r,t[17]=m,t[18]=h):h=t[18],h}var ps=()=>{let e=(0,Z.c)(1),t;return e[0]===Symbol.for(`react.memo_cache_sentinel`)?(t=H(V,{color:`danger`,className:`field__icon`,svg:H(Qe,{})}),e[0]=t):t=e[0],t},ms=()=>{let e=(0,Z.c)(1),t;return e[0]===Symbol.for(`react.memo_cache_sentinel`)?(t=H(V,{color:`success`,className:`field__icon`,svg:H(Yt,{})}),e[0]=t):t=e[0],t},hs=q`
  /* Pin the palette near the top of the viewport instead of centering it so
     the list can grow and shrink without the dialog jumping around */
  &&[data-variant="default"] .react-aria-Dialog {
    top: 15vh;
    transform: translate(-50%, 0);
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }
`,gs=q`
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
`;function _s(e){let t=(0,Z.c)(32),{isOpen:n,onOpenChange:r,inputValue:i,onInputChange:a,filter:o,placeholder:s,"aria-label":c,onAction:l,children:u,renderEmptyState:d,footer:p,isPending:m}=e,h=s===void 0?`Search…`:s,g=c===void 0?`Command palette`:c,_=m?`true`:void 0,v;t[0]===Symbol.for(`react.memo_cache_sentinel`)?(v=H(Go,{}),t[0]=v):v=t[0];let y;t[1]===h?y=t[2]:(y=H(f,{placeholder:h}),t[1]=h,t[2]=y);let b;t[3]!==g||t[4]!==y?(b=H(`div`,{className:`command-palette__field`,children:U(qo,{"aria-label":g,variant:`quiet`,size:`L`,autoFocus:!0,children:[v,y]})}),t[3]=g,t[4]=y,t[5]=b):b=t[5];let x;t[6]===d?x=t[7]:(x=()=>H(`div`,{className:`command-palette__empty-state`,children:d?d():H(Wa,{icon:H(V,{svg:H(Mt,{})}),description:`No results`})}),t[6]=d,t[7]=x);let S;t[8]!==g||t[9]!==u||t[10]!==l||t[11]!==x?(S=H(la,{className:`command-palette__menu`,"aria-label":g,onAction:l,renderEmptyState:x,children:u}),t[8]=g,t[9]=u,t[10]=l,t[11]=x,t[12]=S):S=t[12];let C;t[13]===p?C=t[14]:(C=p??H(vs,{}),t[13]=p,t[14]=C);let w;t[15]===C?w=t[16]:(w=H(`div`,{className:`command-palette__footer`,children:C}),t[15]=C,t[16]=w);let T;t[17]!==o||t[18]!==i||t[19]!==a||t[20]!==w||t[21]!==b||t[22]!==S?(T=U(Ue,{inputValue:i,onInputChange:a,filter:o,children:[b,S,w]}),t[17]=o,t[18]=i,t[19]=a,t[20]=w,t[21]=b,t[22]=S,t[23]=T):T=t[23];let E;t[24]!==g||t[25]!==T||t[26]!==_?(E=H(dn,{size:`M`,css:hs,children:H(Xt,{"aria-label":g,className:`command-palette`,css:gs,"data-pending":_,children:T})}),t[24]=g,t[25]=T,t[26]=_,t[27]=E):E=t[27];let D;return t[28]!==n||t[29]!==r||t[30]!==E?(D=H(sn,{isOpen:n,onOpenChange:r,isDismissable:!0,children:E}),t[28]=n,t[29]=r,t[30]=E,t[31]=D):D=t[31],D}function vs(){let e=(0,Z.c)(3),t;e[0]===Symbol.for(`react.memo_cache_sentinel`)?(t=U(`span`,{className:`command-palette__hint`,children:[H(La,{children:`↑↓`}),H(B,{size:`XS`,color:`text-500`,children:`to navigate`})]}),e[0]=t):t=e[0];let n;e[1]===Symbol.for(`react.memo_cache_sentinel`)?(n=U(`span`,{className:`command-palette__hint`,children:[H(La,{children:`↵`}),H(B,{size:`XS`,color:`text-500`,children:`to select`})]}),e[1]=n):n=e[1];let r;return e[2]===Symbol.for(`react.memo_cache_sentinel`)?(r=U(G,{children:[t,n,U(`span`,{className:`command-palette__hint`,children:[H(La,{children:`esc`}),H(B,{size:`XS`,color:`text-500`,children:`to close`})]})]}),e[2]=r):r=e[2],r}function ys(e){let t=(0,Z.c)(5),{title:n,children:r}=e,i;t[0]===n?i=t[1]:(i=H(nn,{className:`command-palette__section-header`,children:n}),t[0]=n,t[1]=i);let a;return t[2]!==r||t[3]!==i?(a=U(hn,{className:`command-palette__section`,children:[i,r]}),t[2]=r,t[3]=i,t[4]=a):a=t[4],a}var bs=q`
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
`;function xs(e){let t=(0,Z.c)(18),n,r,i,a;t[0]===e?(n=t[1],r=t[2],i=t[3],a=t[4]):({icon:i,description:r,children:n,...a}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a);let o;t[5]===i?o=t[6]:(o=i&&H(`span`,{className:`command-palette-item__icon`,children:i}),t[5]=i,t[6]=o);let s;t[7]===n?s=t[8]:(s=H(`span`,{className:`command-palette-item__label`,children:n}),t[7]=n,t[8]=s);let c;t[9]===r?c=t[10]:(c=r&&H(`span`,{className:`command-palette-item__description`,children:r}),t[9]=r,t[10]=c);let l;t[11]!==o||t[12]!==s||t[13]!==c?(l=U(`div`,{className:`command-palette-item__layout`,children:[o,s,c]}),t[11]=o,t[12]=s,t[13]=c,t[14]=l):l=t[14];let u;return t[15]!==a||t[16]!==l?(u=H(da,{...a,className:`command-palette-item`,css:bs,children:l}),t[15]=a,t[16]=l,t[17]=u):u=t[17],u}var Ss=q`
  background-color: rgba(var(--global-color-blue-500-rgb), 0.4);
  color: inherit;
  border-radius: var(--global-rounding-xsmall);
`;function Cs(e){let t=(0,Z.c)(26),{text:n,match:r}=e,i;t[0]===r?i=t[1]:(i=r?.trim().length??0,t[0]=r,t[1]=i);let a=i;if(!r||a===0){let e;return t[2]===n?e=t[3]:(e=H(G,{children:n}),t[2]=n,t[3]=e),e}let o,s,c,l,u,d;if(t[4]!==r||t[5]!==a||t[6]!==n){d=Symbol.for(`react.early_return_sentinel`);bb0:{let e=n.toLowerCase().indexOf(r.trim().toLowerCase());if(e===-1){let e;t[13]===n?e=t[14]:(e=H(G,{children:n}),t[13]=n,t[14]=e),d=e;break bb0}o=e+a,u=n.slice(0,e),s=`match-text`,c=Ss,l=n.slice(e,o)}t[4]=r,t[5]=a,t[6]=n,t[7]=o,t[8]=s,t[9]=c,t[10]=l,t[11]=u,t[12]=d}else o=t[7],s=t[8],c=t[9],l=t[10],u=t[11],d=t[12];if(d!==Symbol.for(`react.early_return_sentinel`))return d;let f;t[15]!==s||t[16]!==c||t[17]!==l?(f=H(`mark`,{className:s,css:c,children:l}),t[15]=s,t[16]=c,t[17]=l,t[18]=f):f=t[18];let p;t[19]!==o||t[20]!==n?(p=n.slice(o),t[19]=o,t[20]=n,t[21]=p):p=t[21];let m;return t[22]!==u||t[23]!==f||t[24]!==p?(m=U(G,{children:[u,f,p]}),t[22]=u,t[23]=f,t[24]=p,t[25]=m):m=t[25],m}q`
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
`;var ws=q(`
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
`),Ts=e=>{let t=(0,Z.c)(16),n,r,i,a,o;t[0]===e?(n=t[1],r=t[2],i=t[3],a=t[4],o=t[5]):({size:a,css:r,className:n,direction:o,...i}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a,t[5]=o);let s=o===void 0?`row`:o,c;t[6]===n?c=t[7]:(c=z(`radio-group`,n),t[6]=n,t[7]=c);let l;t[8]===r?l=t[9]:(l=q(Fo,ws,r),t[8]=r,t[9]=l);let u;return t[10]!==s||t[11]!==i||t[12]!==a||t[13]!==c||t[14]!==l?(u=H(Ce,{"data-size":a,"data-direction":s,className:c,css:l,...i}),t[10]=s,t[11]=i,t[12]=a,t[13]=c,t[14]=l,t[15]=u):u=t[15],u},Es=q(`
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
`),Ds=e=>{let t=(0,Z.c)(12),n,r,i;t[0]===e?(n=t[1],r=t[2],i=t[3]):({className:n,css:r,...i}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i);let a;t[4]===n?a=t[5]:(a=z(`radio`,n),t[4]=n,t[5]=a);let o;t[6]===r?o=t[7]:(o=q(Es,r),t[6]=r,t[7]=o);let s;return t[8]!==i||t[9]!==a||t[10]!==o?(s=H(_e,{className:a,css:o,...i}),t[8]=i,t[9]=a,t[10]=o,t[11]=s):s=t[11],s},Os=q($e,`
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
`),ks=e=>{let t=(0,Z.c)(25),n,r,i;t[0]===e?(n=t[1],r=t[2],i=t[3]):({className:n,css:r,...i}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i);let a,o,s,c,l;t[4]===i?(a=t[5],o=t[6],s=t[7],c=t[8],l=t[9]):({leadingVisual:o,trailingVisual:l,size:s,children:a,...c}=i,t[4]=i,t[5]=a,t[6]=o,t[7]=s,t[8]=c,t[9]=l);let u=yt(),d=s??u,f;t[10]!==a||t[11]!==o||t[12]!==l?(f=e=>U(G,{children:[o,typeof a==`function`?a(e):a,l]}),t[10]=a,t[11]=o,t[12]=l,t[13]=f):f=t[13];let p=f,m;t[14]===r?m=t[15]:(m=q(Os,r),t[14]=r,t[15]=m);let h=!a,g;t[16]===n?g=t[17]:(g=z(`toggle-button`,n),t[16]=n,t[17]=g);let _;return t[18]!==p||t[19]!==c||t[20]!==d||t[21]!==m||t[22]!==h||t[23]!==g?(_=H(k,{css:m,"data-size":d,"data-childless":h,className:g,...c,children:p}),t[18]=p,t[19]=c,t[20]=d,t[21]=m,t[22]=h,t[23]=g,t[24]=_):_=t[24],_},As=q(`
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
`),js=e=>{let t=(0,Z.c)(19),n,r,i,a,o;t[0]===e?(n=t[1],r=t[2],i=t[3],a=t[4],o=t[5]):({size:a,css:r,className:n,selectionMode:o,...i}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a,t[5]=o);let s=a===void 0?`M`:a,c=o===void 0?`single`:o,l;t[6]===n?l=t[7]:(l=z(`toggle-button-group`,n),t[6]=n,t[7]=l);let u;t[8]===r?u=t[9]:(u=q(As,r),t[8]=r,t[9]=u);let d;t[10]!==i||t[11]!==c||t[12]!==s||t[13]!==l||t[14]!==u?(d=H(N,{"data-size":s,className:l,css:u,selectionMode:c,...i}),t[10]=i,t[11]=c,t[12]=s,t[13]=l,t[14]=u,t[15]=d):d=t[15];let f;return t[16]!==s||t[17]!==d?(f=H(ft,{size:s,children:d}),t[16]=s,t[17]=d,t[18]=f):f=t[18],f},Ms=q`
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
`;function Ns(e){let t=(0,Z.c)(10),n,r,i;t[0]===e?(n=t[1],r=t[2],i=t[3]):({css:n,ref:r,...i}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i);let a;t[4]===n?a=t[5]:(a=q(Ms,n),t[4]=n,t[5]=a);let o=a,s;return t[6]!==o||t[7]!==r||t[8]!==i?(s=H(y,{css:o,ref:r,...i}),t[6]=o,t[7]=r,t[8]=i,t[9]=s):s=t[9],s}var Ps=q`
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
    transition: all 200ms;
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
`;function Fs(e){let t=(0,Z.c)(14),n,r;t[0]===e?(n=t[1],r=t[2]):({ref:r,...n}=e,t[0]=e,t[1]=n,t[2]=r);let i,a,o;t[3]===n?(i=t[4],a=t[5],o=t[6]):({children:i,isHovered:a,...o}=n,t[3]=n,t[4]=i,t[5]=a,t[6]=o);let s=a||void 0,c;t[7]===i?c=t[8]:(c=e=>{let{isIndeterminate:t}=e;return U(G,{children:[H(`div`,{className:`checkbox`,children:H(`svg`,{viewBox:`0 0 18 18`,"aria-hidden":`true`,children:t?H(`rect`,{x:1,y:7.5,width:15,height:3}):H(`polyline`,{points:`1 9 7 14 15 4`})})}),i]})},t[7]=i,t[8]=c);let l;return t[9]!==r||t[10]!==o||t[11]!==s||t[12]!==c?(l=H(E,{...o,ref:r,css:Ps,"data-force-hovered":s,children:c}),t[9]=r,t[10]=o,t[11]=s,t[12]=c,t[13]=l):l=t[13],l}var Is=q`
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
`,Ls=q`
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
`,Rs=q`
  padding: var(--global-dimension-size-50) var(--global-dimension-size-100) 0;
`;q`
  display: flex;
  flex-direction: column;
  gap: var(--global-menu-item-gap);
`;function zs(e){let t=(0,Z.c)(6),n,r;t[0]===e?(n=t[1],r=t[2]):({ref:n,...r}=e,t[0]=e,t[1]=n,t[2]=r);let i;return t[3]!==n||t[4]!==r?(i=H(P,{css:Is,ref:n,...r}),t[3]=n,t[4]=r,t[5]=i):i=t[5],i}function Bs(e){let t=(0,Z.c)(14),n,r,i,a,o;t[0]===e?(n=t[1],r=t[2],i=t[3],a=t[4],o=t[5]):({ref:r,children:n,subtitle:a,trailingContent:o,...i}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a,t[5]=o);let s;t[6]!==n||t[7]!==a||t[8]!==o?(s=e=>{let{selectionMode:t,selectionBehavior:r}=e;return U(G,{children:[H(Vs,{subtitle:a,selectionMode:t,selectionBehavior:r,children:n}),o]})},t[6]=n,t[7]=a,t[8]=o,t[9]=s):s=t[9];let c;return t[10]!==r||t[11]!==i||t[12]!==s?(c=H(Pe,{css:Ls,ref:r,...i,children:s}),t[10]=r,t[11]=i,t[12]=s,t[13]=c):c=t[13],c}var Vs=e=>{let t=(0,Z.c)(14),{children:n,subtitle:r,selectionMode:i,selectionBehavior:a}=e,[o,s]=(0,X.useState)(!1),c,l,u;t[0]===Symbol.for(`react.memo_cache_sentinel`)?(c=()=>s(!0),l=()=>s(!1),u=q`
        flex: 1;
        min-width: 0;
      `,t[0]=c,t[1]=l,t[2]=u):(c=t[0],l=t[1],u=t[2]);let d;t[3]!==o||t[4]!==a||t[5]!==i?(d=i===`multiple`&&a===`toggle`&&H(Fs,{slot:`selection`,isHovered:o}),t[3]=o,t[4]=a,t[5]=i,t[6]=d):d=t[6];let f;t[7]===Symbol.for(`react.memo_cache_sentinel`)?(f=q`
            padding: var(--global-menu-item-gap);
          `,t[7]=f):f=t[7];let p;t[8]!==n||t[9]!==r?(p=U(K,{direction:`column`,gap:`var(--global-dimension-size-25)`,minWidth:0,flex:1,css:f,children:[n,r]}),t[8]=n,t[9]=r,t[10]=p):p=t[10];let m;return t[11]!==d||t[12]!==p?(m=H(`div`,{onMouseEnter:c,onMouseLeave:l,css:u,children:U(K,{direction:`row`,alignItems:`center`,gap:`size-100`,className:`GridListItem__content`,children:[d,p]})}),t[11]=d,t[12]=p,t[13]=m):m=t[13],m},Hs=e=>{let t=(0,Z.c)(2),{title:n}=e,r;return t[0]===n?r=t[1]:(r=H(le,{css:Rs,children:H(B,{weight:`heavy`,children:n})}),t[0]=n,t[1]=r),r},Us=q`
  --token-max-width: var(--global-dimension-size-2000);
  box-sizing: border-box;
  display: inline-flex;
  align-items: center;
  gap: var(--global-dimension-size-100);
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

  &[data-removable] {
    padding-right: var(--global-dimension-size-25);
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
`;function Ws(e){let t=(0,Z.c)(4),{children:n,size:r}=e,i=r===void 0?`M`:r,a;t[0]===Symbol.for(`react.memo_cache_sentinel`)?(a=q`
        display: flex;
        align-items: center;
        justify-content: center;
        width: var(--global-dimension-size-200);
        height: var(--global-dimension-size-200);

        &[data-size="M"] {
          margin-right: var(--global-dimension-size-50);
        }

        &[data-size="L"] {
          margin-right: var(--global-dimension-size-100);
        }
      `,t[0]=a):a=t[0];let o;return t[1]!==n||t[2]!==i?(o=H(`span`,{"data-size":i,css:a,children:n}),t[1]=n,t[2]=i,t[3]=o):o=t[3],o}function Gs(e){let t=(0,Z.c)(55),n,r,i,a,o,s,c,l,u,d,f,p;t[0]===e?(n=t[1],r=t[2],i=t[3],a=t[4],o=t[5],s=t[6],c=t[7],l=t[8],u=t[9],d=t[10],f=t[11],p=t[12]):({ref:l,children:n,isDisabled:i,css:r,color:f,onPress:s,onRemove:c,size:p,style:d,leadingVisual:a,maxWidth:o,...u}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a,t[5]=o,t[6]=s,t[7]=c,t[8]=l,t[9]=u,t[10]=d,t[11]=f,t[12]=p);let m=f===void 0?`var(--global-color-gray-600)`:f,h=p===void 0?`M`:p,{theme:g}=pr(),_;t[13]!==a||t[14]!==h?(_=a&&h!==`S`?H(Ws,{size:h,children:a}):null,t[13]=a,t[14]=h,t[15]=_):_=t[15];let v=_,y;t[16]!==i||t[17]!==c?(y=c?H(`button`,{onClick:()=>{c()},disabled:i,"aria-label":`Remove`,children:H(V,{svg:H(wt,{})})}):null,t[16]=i,t[17]=c,t[18]=y):y=t[18];let b=y,x;t[19]===n?x=t[20]:(x=H(`span`,{className:`token__text`,children:n}),t[19]=n,t[20]=x);let S=x,C;t[21]!==i||t[22]!==s||t[23]!==c||t[24]!==b||t[25]!==S||t[26]!==v?(C=()=>s&&c?U(G,{children:[U(`button`,{onClick:()=>{s()},disabled:i,children:[v,S]}),b]}):s?U(`button`,{onClick:()=>{s()},disabled:i,children:[v,S]}):c?U(G,{children:[U(`span`,{children:[v,S]}),b]}):U(G,{children:[v,S]}),t[21]=i,t[22]=s,t[23]=c,t[24]=b,t[25]=S,t[26]=v,t[27]=C):C=t[27];let w=C,T;t[28]===r?T=t[29]:(T=q(Us,r),t[28]=r,t[29]=T);let E;t[30]===o?E=t[31]:(E=o&&{"--token-max-width":o},t[30]=o,t[31]=E);let D;t[32]!==m||t[33]!==d||t[34]!==E?(D={"--internal-token-color":m,...E,...d},t[32]=m,t[33]=d,t[34]=E,t[35]=D):D=t[35];let O;t[36]===s?O=t[37]:(O=s&&{"data-interactive":!0},t[36]=s,t[37]=O);let k;t[38]===c?k=t[39]:(k=c&&{"data-removable":!0},t[38]=c,t[39]=k);let A;t[40]===i?A=t[41]:(A=i&&{"data-disabled":!0},t[40]=i,t[41]=A);let j;t[42]===w?j=t[43]:(j=w(),t[42]=w,t[43]=j);let M;return t[44]!==l||t[45]!==u||t[46]!==h||t[47]!==O||t[48]!==k||t[49]!==A||t[50]!==j||t[51]!==T||t[52]!==D||t[53]!==g?(M=H(`div`,{ref:l,css:T,style:D,"data-theme":g,"data-size":h,...O,...k,...A,...u,children:j}),t[44]=l,t[45]=u,t[46]=h,t[47]=O,t[48]=k,t[49]=A,t[50]=j,t[51]=T,t[52]=D,t[53]=g,t[54]=M):M=t[54],M}var Ks=q`
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
`;function qs(e){let t=(0,Z.c)(24),n,r,a,o,s,c;t[0]===e?(n=t[1],r=t[2],a=t[3],o=t[4],s=t[5],c=t[6]):({ref:s,label:a,thumbLabels:c,children:r,css:n,...o}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=a,t[4]=o,t[5]=s,t[6]=c);let l;t[7]===n?l=t[8]:(l=q(Ks,n),t[7]=n,t[8]=l);let u;t[9]===a?u=t[10]:(u=a&&H(yn,{className:`slider__label`,children:a}),t[9]=a,t[10]=u);let d;t[11]===r?d=t[12]:(d=r===void 0?H(Xs,{}):r,t[11]=r,t[12]=d);let f;t[13]===d?f=t[14]:(f=H(i,{className:`slider__output`,children:d}),t[13]=d,t[14]=f);let p;t[15]===c?p=t[16]:(p=H(m,{className:`slider__track`,style:Js,children:e=>{let{state:t}=e;return H(G,{children:t.values.map((e,t)=>H(C,{index:t,"aria-label":c?.[t],className:`slider__thumb`},t))})}}),t[15]=c,t[16]=p);let h;return t[17]!==o||t[18]!==s||t[19]!==l||t[20]!==u||t[21]!==f||t[22]!==p?(h=U(Le,{css:l,...o,ref:s,children:[u,f,p]}),t[17]=o,t[18]=s,t[19]=l,t[20]=u,t[21]=f,t[22]=p,t[23]=h):h=t[23],h}function Js(e){let{state:t}=e;return t.values.length===1?{"--slider-start":`0%`,"--slider-end":`${t.getThumbPercent(0)*100}%`}:{"--slider-start":`${t.getThumbPercent(0)*100}%`,"--slider-end":`${t.getThumbPercent(1)*100}%`}}function Ys(e){let t=(0,Z.c)(19),n,r;t[0]===e?(n=t[1],r=t[2]):({onChange:n,...r}=e,t[0]=e,t[1]=n,t[2]=r);let{step:i,getThumbMinValue:a,getThumbMaxValue:o,values:s,setThumbValue:c}=(0,X.useContext)(v),l=`defaultValue`in r,u=s[0]===a(0),d=l&&u?r.defaultValue:s[0],p=St(Gt),m=p.id,h;t[3]!==n||t[4]!==c?(h=e=>{n?n(e):typeof e==`number`&&c(0,e)},t[3]=n,t[4]=c,t[5]=h):h=t[5];let g;t[6]===o?g=t[7]:(g=o(0),t[6]=o,t[7]=g);let _;t[8]===a?_=t[9]:(_=a(0),t[8]=a,t[9]=_);let y;t[10]===Symbol.for(`react.memo_cache_sentinel`)?(y=H(f,{}),t[10]=y):y=t[10];let b;return t[11]!==p.id||t[12]!==r||t[13]!==i||t[14]!==h||t[15]!==g||t[16]!==_||t[17]!==d?(b=H(us,{className:`slider__number-field`,"aria-labelledby":m,value:d,onChange:h,step:i,maxValue:g,minValue:_,...r,children:y}),t[11]=p.id,t[12]=r,t[13]=i,t[14]=h,t[15]=g,t[16]=_,t[17]=d,t[18]=b):b=t[18],b}function Xs(){let e=(0,Z.c)(4),t=(0,X.useContext)(v),n;e[0]===t.values?n=e[1]:(n=t.values.map(Zs).join(` – `),e[0]=t.values,e[1]=n);let r;return e[2]===n?r=e[3]:(r=H(B,{children:n}),e[2]=n,e[3]=r),r}function Zs(e){return e.toString()}var Qs=q`
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
`;function $s(e){let t=(0,Z.c)(4),{children:n,variant:r}=e,i=r===void 0?`default`:r,{theme:a}=pr(),o;return t[0]!==n||t[1]!==a||t[2]!==i?(o=H(`span`,{css:Qs,"data-variant":i,"data-theme":a,className:`counter`,children:n}),t[0]=n,t[1]=a,t[2]=i,t[3]=o):o=t[3],o}function ec(){let e=(0,Z.c)(6),t=(0,X.useRef)(null),[n,r]=(0,X.useState)(!1),[i,a]=(0,X.useState)(!1),o;e[0]===Symbol.for(`react.memo_cache_sentinel`)?(o=()=>{let e=t.current;if(!e)return;if(e.getAttribute(`data-orientation`)!==`horizontal`){r(!1),a(!1);return}let{scrollLeft:n,scrollWidth:i,clientWidth:o}=e,s=i-o;r(n>1),a(n<s-1)},e[0]=o):o=e[0];let s=o;Ot(t,`scroll`,s);let c;e[1]===Symbol.for(`react.memo_cache_sentinel`)?(c={ref:t,onResize:s},e[1]=c):c=e[1],Rt(c);let l;e[2]===Symbol.for(`react.memo_cache_sentinel`)?(l=()=>{s()},e[2]=l):l=e[2],(0,X.useEffect)(l);let u;return e[3]!==i||e[4]!==n?(u={ref:t,hasOverflowAtStart:n,hasOverflowAtEnd:i},e[3]=i,e[4]=n,e[5]=u):u=e[5],u}var tc=q`
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
`;function nc(e){let t=(0,Z.c)(16),n,r,i,a,o;t[0]===e?(n=t[1],r=t[2],i=t[3],a=t[4],o=t[5]):({children:r,css:n,className:i,orientation:o,...a}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a,t[5]=o);let s=o===void 0?`horizontal`:o,c;t[6]===n?c=t[7]:(c=q(tc,n),t[6]=n,t[7]=c);let l;t[8]===i?l=t[9]:(l=z(`react-aria-Tabs`,`tabs`,i),t[8]=i,t[9]=l);let u;return t[10]!==r||t[11]!==s||t[12]!==a||t[13]!==c||t[14]!==l?(u=H(Ae,{css:c,className:l,orientation:s,...a,children:r}),t[10]=r,t[11]=s,t[12]=a,t[13]=c,t[14]=l,t[15]=u):u=t[15],u}var rc=q`
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
`;function ic(e){let t=(0,Z.c)(17),n,r,i,a;t[0]===e?(n=t[1],r=t[2],i=t[3],a=t[4]):({children:r,css:n,className:i,...a}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a);let{ref:o,hasOverflowAtStart:s,hasOverflowAtEnd:c}=ec(),l;t[5]===n?l=t[6]:(l=q(rc,n),t[5]=n,t[6]=l);let u;t[7]===i?u=t[8]:(u=z(`react-aria-TabList`,i),t[7]=i,t[8]=u);let d;return t[9]!==r||t[10]!==c||t[11]!==s||t[12]!==a||t[13]!==o||t[14]!==l||t[15]!==u?(d=H(te,{ref:o,css:l,className:u,"data-overflow-start":s,"data-overflow-end":c,...a,children:r}),t[9]=r,t[10]=c,t[11]=s,t[12]=a,t[13]=o,t[14]=l,t[15]=u,t[16]=d):d=t[16],d}var ac=q`
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
`;function oc(e){let t=(0,Z.c)(14),n,r,i,a;t[0]===e?(n=t[1],r=t[2],i=t[3],a=t[4]):({css:n,className:r,padded:i,...a}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a);let o;t[5]===n?o=t[6]:(o=q(ac,n),t[5]=n,t[6]=o);let s;t[7]===r?s=t[8]:(s=z(`react-aria-TabPanel`,r),t[7]=r,t[8]=s);let c;return t[9]!==i||t[10]!==a||t[11]!==o||t[12]!==s?(c=H(I,{css:o,className:s,"data-padded":i,...a}),t[9]=i,t[10]=a,t[11]=o,t[12]=s,t[13]=c):c=t[13],c}function sc(e){let t=(0,Z.c)(11),n,r,i;t[0]===e?(n=t[1],r=t[2],i=t[3]):({children:n,id:r,...i}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i);let a;t[4]!==n||t[5]!==r?(a=e=>{let{state:t}=e,{selectedKey:i}=t;return i===r?n:null},t[4]=n,t[5]=r,t[6]=a):a=t[6];let o;return t[7]!==r||t[8]!==i||t[9]!==a?(o=H(oc,{id:r,...i,children:a}),t[7]=r,t[8]=i,t[9]=a,t[10]=o):o=t[10],o}var cc=q`
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
`;function lc(e){let t=(0,Z.c)(15),n,r,i,a;t[0]===e?(n=t[1],r=t[2],i=t[3],a=t[4]):({children:r,css:n,className:i,...a}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a);let o;t[5]===n?o=t[6]:(o=q(cc,n),t[5]=n,t[6]=o);let s;t[7]===i?s=t[8]:(s=z(`react-aria-Tab`,i),t[7]=i,t[8]=s);let c;t[9]===Symbol.for(`react.memo_cache_sentinel`)?(c=H(Ze,{className:`react-aria-SelectionIndicator`}),t[9]=c):c=t[9];let l;return t[10]!==r||t[11]!==a||t[12]!==o||t[13]!==s?(l=U(xe,{css:o,className:s,...a,children:[r,c]}),t[10]=r,t[11]=a,t[12]=o,t[13]=s,t[14]=l):l=t[14],l}var uc=e=>{let t=(0,Z.c)(9),{message:n,size:r,className:i}=e,a;t[0]===Symbol.for(`react.memo_cache_sentinel`)?(a=q`
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        width: 100%;
        height: 100%;
        gap: var(--global-dimension-size-100);
      `,t[0]=a):a=t[0];let o;t[1]===r?o=t[2]:(o=H(Di,{isIndeterminate:!0,"aria-label":`loading`,size:r}),t[1]=r,t[2]=o);let s;t[3]===n?s=t[4]:(s=n==null?null:H(B,{children:n}),t[3]=n,t[4]=s);let c;return t[5]!==i||t[6]!==o||t[7]!==s?(c=U(`div`,{className:i,css:a,children:[o,s]}),t[5]=i,t[6]=o,t[7]=s,t[8]=c):c=t[8],c},dc=Ke`
  0% {
    opacity: 1;
  }
  50% {
    opacity: 0.4;
  }
  100% {
    opacity: 1;
  }
`,fc=Ke`
  0% {
    transform: translateX(-100%);
  }
  50% {
    transform: translateX(100%);
  }
  100% {
    transform: translateX(100%);
  }
`,pc=q`
  display: block;
  background-color: var(--global-color-gray-200);
`,mc=q`
  animation: ${dc} 2s ease-in-out 0.5s infinite;
`,hc=q`
  position: relative;
  overflow: hidden;
  /* Fix bug in Safari https://bugs.webkit.org/show_bug.cgi?id=68196 */
  -webkit-mask-image: -webkit-radial-gradient(white, black);

  &::after {
    animation: ${fc} 2s linear 0.5s infinite;
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
`,gc=e=>{if(typeof e==`number`)return`${e}px`;if(typeof e==`string`)switch(e){case`none`:return`0`;case`XS`:return`var(--global-rounding-xsmall)`;case`S`:return`var(--global-rounding-small)`;case`M`:return`var(--global-rounding-medium)`;case`L`:return`var(--global-rounding-large)`;case`circle`:return`50%`;default:return e}return`var(--global-rounding-medium)`};function _c({ref:e,width:t=`100%`,height:n=`1.2em`,borderRadius:r=`S`,animation:i=`pulse`,className:a,...o}){let s=typeof t==`number`?`${t}px`:t,c=typeof n==`number`?`${n}px`:n,l=gc(r);return H(`span`,{ref:e,className:z(a,`skeleton`),css:[pc,i===`pulse`&&mc,i===`wave`&&hc,q`
          width: ${s};
          height: ${c};
          border-radius: ${l};
        `],...o})}_c.displayName=`Skeleton`;var vc=e=>{let t=(0,Z.c)(5),n,r,i;t[0]===Symbol.for(`react.memo_cache_sentinel`)?(n=H(_c,{height:100,borderRadius:8,animation:`wave`}),r=H(_c,{height:24,width:`80%`,animation:`wave`}),i=H(_c,{height:16,width:`60%`,animation:`wave`}),t[0]=n,t[1]=r,t[2]=i):(n=t[0],r=t[1],i=t[2]);let a;return t[3]===e?a=t[4]:(a=U(K,{direction:`column`,gap:`size-100`,width:`100%`,...e,children:[n,r,i]}),t[3]=e,t[4]=a),a},yc=q`
  display: flex;
  flex-direction: column;
`,bc=q`
  display: flex;
  gap: 6px;
`,xc=[[3,2,5,1.5,4,2.5,4],[2,4,1.5,5,3,3.5],[4,2.5,5,2,3],[3,4.5,2,4,1.5,4],[3.5,2,5,2.5]],Sc=[`100%`,`95%`,`100%`,`88%`,`92%`];function Cc({lines:e=3,animation:t=`pulse`,gap:n=8}){let r=(e,t)=>{let n=xc[e%xc.length],r=t?Math.ceil(n.length*.5):n.length;return n.slice(0,r)};return H(`div`,{css:[yc,q`
          gap: ${n}px;
        `],children:Array.from({length:e},(n,i)=>{let a=i===e-1,o=r(i,a);return H(`div`,{css:[bc,q`
                width: ${a?`55%`:Sc[i%Sc.length]};
              `],children:o.map((e,n)=>H(_c,{css:q`
                  flex-grow: ${e};
                  min-width: 20px;
                `,height:`1em`,animation:t},n))},i)})})}var wc=q`
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
`;function Tc(e){let t=(0,Z.c)(14),n,r;t[0]===e?(n=t[1],r=t[2]):({ref:r,...n}=e,t[0]=e,t[1]=n,t[2]=r);let i,a;t[3]===n?(i=t[4],a=t[5]):({size:a,...i}=n,t[3]=n,t[4]=i,t[5]=a);let o=a===void 0?`M`:a,s;t[6]===Symbol.for(`react.memo_cache_sentinel`)?(s=q(Fo,wc),t[6]=s):s=t[6];let c;t[7]!==i||t[8]!==r||t[9]!==o?(c=H(re,{"data-size":o,className:`select`,ref:r,css:s,...i}),t[7]=i,t[8]=r,t[9]=o,t[10]=c):c=t[10];let l;return t[11]!==o||t[12]!==c?(l=H(ft,{size:o,children:c}),t[11]=o,t[12]=c,t[13]=l):l=t[13],l}function Ec(e){let t=(0,Z.c)(10),n,r,i;t[0]===e?(n=t[1],r=t[2],i=t[3]):({ref:r,children:n,...i}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i);let a;t[4]===n?a=t[5]:(a=e=>{let{isSelected:t}=e;return U(K,{direction:`row`,justifyContent:`space-between`,alignItems:`center`,children:[H(`span`,{children:n}),t&&H(V,{svg:H(Yt,{})})]})},t[4]=n,t[5]=a);let o;return t[6]!==r||t[7]!==i||t[8]!==a?(o=H(x,{...i,ref:r,children:a}),t[6]=r,t[7]=i,t[8]=a,t[9]=o):o=t[9],o}Ec.displayName=`SelectItem`,q`
  max-width: 100%;
  height: auto;
`;var Dc=16,Oc=8,kc=.05,Ac=Ke`
  from {
    opacity: 0;
    transform: translateY(-130%);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
`,jc=q`
  position: fixed;
  top: var(--global-dimension-size-200);
  left: 50%;
  width: 400px;
  max-width: calc(100vw - var(--global-dimension-size-400));
  transform: translateX(-50%);
  outline: none;
  z-index: ${Tn};

  --collapsed-peek: ${Dc}px;
  --expanded-gap: ${Oc}px;
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
`,Mc=q`
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  transform-origin: top center;
  transform: translateY(
      calc(var(--toast-index) * var(--collapsed-peek, ${Dc}px))
    )
    scale(calc(1 - var(--toast-index) * ${kc}));
  opacity: calc(1 - var(--toast-index) * 0.1);
  transition:
    transform 300ms cubic-bezier(0.21, 1.02, 0.73, 1),
    opacity 300ms ease;

  @media (prefers-reduced-motion: reduce) {
    transition: none;
  }
`,Nc=q`
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
  animation: ${Ac} 280ms cubic-bezier(0.21, 1.02, 0.73, 1);
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
`;function Pc(e){let t=(0,Z.c)(6),{stackIndex:n,children:r}=e,i=100-n,a;t[0]!==n||t[1]!==i?(a={"--toast-index":n,zIndex:i},t[0]=n,t[1]=i,t[2]=a):a=t[2];let o;return t[3]!==r||t[4]!==a?(o=H(`div`,{className:`toast-positioner`,css:Mc,style:a,children:r}),t[3]=r,t[4]=a,t[5]=o):o=t[5],o}var Fc=e=>{switch(e){case`success`:return H(V,{svg:H(Cn,{})});case`error`:return H(V,{svg:H(pn,{})});default:return null}},Ic=e=>{switch(e){case`success`:return`var(--global-color-success)`;case`error`:return`var(--global-color-danger)`;default:return`var(--global-color-gray-600)`}},Lc=e=>{let t=(0,Z.c)(33),{toast:r}=e,{theme:i}=pr(),a=(0,X.useContext)(n),o;t[0]!==a?.visibleToasts||t[1]!==r.key?(o=a?.visibleToasts.findIndex(e=>e.key===r.key)??0,t[0]=a?.visibleToasts,t[1]=r.key,t[2]=o):o=t[2];let s=Math.max(0,o),c;t[3]===r.content.variant?c=t[4]:(c=Fc(r.content.variant),t[3]=r.content.variant,t[4]=c);let l=c,u;t[5]===r.content.variant?u=t[6]:(u=Ic(r.content.variant),t[5]=r.content.variant,t[6]=u);let d;t[7]===u?d=t[8]:(d={"--internal-token-color":u},t[7]=u,t[8]=d);let f;t[9]===Symbol.for(`react.memo_cache_sentinel`)?(f=q`
            display: flex;
            justify-content: space-between;
            width: 100%;
          `,t[9]=f):f=t[9];let p;t[10]!==l||t[11]!==r.content.title?(p=U(B,{slot:`title`,size:`M`,children:[l,r.content.title]}),t[10]=l,t[11]=r.content.title,t[12]=p):p=t[12];let m;t[13]===r.content.message?m=t[14]:(m=H(B,{slot:`description`,children:r.content.message}),t[13]=r.content.message,t[14]=m);let h;t[15]!==p||t[16]!==m?(h=U(Me,{children:[p,m]}),t[15]=p,t[16]=m,t[17]=h):h=t[17];let g;t[18]===Symbol.for(`react.memo_cache_sentinel`)?(g=H(Qt,{slot:`close`,size:`S`,color:`inherit`,type:`button`,"aria-label":`Close notification`,children:H(V,{svg:H(wt,{})})}),t[18]=g):g=t[18];let _;t[19]===h?_=t[20]:(_=U(`div`,{css:f,children:[h,g]}),t[19]=h,t[20]=_);let v;t[21]!==r.content.action||t[22]!==r.key?(v=r.content.action?H(`div`,{className:`toast-action-container`,children:typeof r.content.action==`object`&&`text`in r.content.action?H(W,{className:`toast-action-button`,onPress:()=>{let e=r.content.action;if(typeof e==`object`&&e&&`onClick`in e){let t=e.closeOnClick??!0,n=()=>{$n?.close(r.key)};e.onClick(n),t&&n()}},size:`S`,children:r.content.action.text}):r.content.action}):null,t[21]=r.content.action,t[22]=r.key,t[23]=v):v=t[23];let y;t[24]!==_||t[25]!==v||t[26]!==d||t[27]!==i||t[28]!==r?(y=U(ae,{toast:r,css:Nc,className:`react-aria-Toast`,style:d,"data-variant":r.content.variant,"data-theme":i,children:[_,v]}),t[24]=_,t[25]=v,t[26]=d,t[27]=i,t[28]=r,t[29]=y):y=t[29];let b;return t[30]!==s||t[31]!==y?(b=H(Pc,{stackIndex:s,children:y}),t[30]=s,t[31]=y,t[32]=b):b=t[32],b},Rc=q`
  display: flex;
  align-items: center;

  a {
    color: var(--global-text-color-700);
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
`;function zc(e){let t=(0,Z.c)(12),n,r;t[0]===e?(n=t[1],r=t[2]):({ref:r,...n}=e,t[0]=e,t[1]=n,t[2]=r);let i,a;t[3]===n?(i=t[4],a=t[5]):({children:i,...a}=n,t[3]=n,t[4]=i,t[5]=a);let o;t[6]===i?o=t[7]:(o=e=>{let{isCurrent:t}=e;return U(G,{children:[i,!t&&H(V,{svg:H(On,{})})]})},t[6]=i,t[7]=o);let s;return t[8]!==r||t[9]!==a||t[10]!==o?(s=H(fe,{css:Rc,...a,className:`breadcrumb`,ref:r,children:o}),t[8]=r,t[9]=a,t[10]=o,t[11]=s):s=t[11],s}var Bc=q`
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
`;function Vc(e){let t=(0,Z.c)(10),n,r;t[0]===e?(n=t[1],r=t[2]):({ref:r,...n}=e,t[0]=e,t[1]=n,t[2]=r);let i,a;t[3]===n?(i=t[4],a=t[5]):({size:a,...i}=n,t[3]=n,t[4]=i,t[5]=a);let o=a===void 0?`M`:a,s;return t[6]!==r||t[7]!==i||t[8]!==o?(s=H(Oe,{css:Bc,...i,ref:r,"data-size":o}),t[6]=r,t[7]=i,t[8]=o,t[9]=s):s=t[9],s}var Hc=q`
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
`;function Uc(e){let t=(0,Z.c)(10),n,r,i,a;t[0]===e?(n=t[1],r=t[2],i=t[3],a=t[4]):({ref:i,size:a,children:n,...r}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a);let o=a===void 0?`M`:a,s;return t[5]!==n||t[6]!==r||t[7]!==i||t[8]!==o?(s=H(`ul`,{ref:i,css:Hc,"data-list-size":o,...r,children:n}),t[5]=n,t[6]=r,t[7]=i,t[8]=o,t[9]=s):s=t[9],s}function Wc(e){let t=(0,Z.c)(8),n,r,i;t[0]===e?(n=t[1],r=t[2],i=t[3]):({ref:i,children:n,...r}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i);let a;return t[4]!==n||t[5]!==r||t[6]!==i?(a=H(`li`,{ref:i,...r,children:n}),t[4]=n,t[5]=r,t[6]=i,t[7]=a):a=t[7],a}var Gc=q`
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
`,Kc=e=>{let t=(0,Z.c)(2),{children:n}=e,r;return t[0]===n?r=t[1]:(r=H(`div`,{css:Gc,children:n}),t[0]=n,t[1]=r),r},qc=q`
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
`;function Jc(e){let t=(0,Z.c)(6),n,r;t[0]===e?(n=t[1],r=t[2]):({ref:r,...n}=e,t[0]=e,t[1]=n,t[2]=r);let i;return t[3]!==n||t[4]!==r?(i=H(j,{...n,ref:r,css:qc,children:n.children}),t[3]=n,t[4]=r,t[5]=i):i=t[5],i}var Yc=q`
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
`;function Xc(e){let t=(0,Z.c)(6),n,r;t[0]===e?(n=t[1],r=t[2]):({ref:r,...n}=e,t[0]=e,t[1]=n,t[2]=r);let i;return t[3]!==n||t[4]!==r?(i=H(wn,{...n,ref:r,css:Yc,className:`separator react-aria-Separator`}),t[3]=n,t[4]=r,t[5]=i):i=t[5],i}var Zc=e=>q`
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

    & .card__title {
      font-size: var(--global-font-size-m);
      line-height: var(--global-line-height-m);
      display: flex;
      align-items: center;
      gap: var(--global-dimension-size-100);
    }

    & .card__sub-title {
      color: var(--global-text-color-700);
    }

    /* Header layout when the title holds interactive controls */
    & .card__collapsible-header {
      display: flex;
      flex: 1;
      flex-direction: row;
      align-items: center;
      height: 100%;

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

  /* Collapsible behavior: highlight the header only when the collapse
     trigger itself is hovered, so the affordance matches the click target
     (with interactiveTitle only the arrow button toggles) */
  &[data-collapsible="true"] {
    & > header:has(.card__collapsible-button:hover) {
      background-color: var(--global-card-header-background-color-hover);
    }
  }

  &[data-collapsed="true"] {
    & .card__body {
      display: none !important;
    }
  }
`;function Qc(e){let t=(0,Z.c)(72),n,r,i,a,o,s,c,l,u,d,f,p,m,h,g;t[0]===e?(n=t[1],r=t[2],i=t[3],a=t[4],o=t[5],s=t[6],c=t[7],l=t[8],u=t[9],d=t[10],f=t[11],p=t[12],m=t[13],h=t[14],g=t[15]):({ref:s,title:h,titleExtra:g,titleSeparator:l,subTitle:c,children:n,collapsible:u,interactiveTitle:d,collapseButtonLabel:r,defaultOpen:f,scrollBody:p,extra:i,onCollapseChange:a,testId:m,...o}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a,t[5]=o,t[6]=s,t[7]=c,t[8]=l,t[9]=u,t[10]=d,t[11]=f,t[12]=p,t[13]=m,t[14]=h,t[15]=g);let _=l===void 0||l,v=u!==void 0&&u,y=d!==void 0&&d,b=f===void 0||f,x=p!==void 0&&p,{styleProps:S}=fn(o,ln),[C,w]=(0,X.useState)(v?!b:!1),T=(0,X.useId)(),E=(0,X.useId)(),D=(0,X.useId)(),O=(0,X.useId)(),k;t[16]===a?k=t[17]:(k=e=>{a?.(e)},t[16]=a,t[17]=k);let A=(0,X.useEffectEvent)(k),j;t[18]!==A||t[19]!==C?(j=()=>{A(C)},t[18]=A,t[19]=C,t[20]=j):j=t[20];let M;t[21]===C?M=t[22]:(M=[C],t[21]=C,t[22]=M),(0,X.useEffect)(j,M);let N;t[23]!==h||t[24]!==g?(N=U(Xe,{level:3,weight:`heavy`,className:`card__title`,children:[h,g]}),t[23]=h,t[24]=g,t[25]=N):N=t[25];let P;t[26]===c?P=t[27]:(P=c&&H(Xe,{level:4,className:`card__sub-title`,children:c}),t[26]=c,t[27]=P);let F;t[28]!==P||t[29]!==N||t[30]!==D?(F=U(`div`,{id:D,children:[N,P]}),t[28]=P,t[29]=N,t[30]=D,t[31]=F):F=t[31];let I=F,L;t[32]===C?L=t[33]:(L=()=>{w(!C)},t[32]=C,t[33]=L);let ee=!C,R=y?r:void 0,te=y&&r==null?D:void 0,ne=!C,re;t[34]===ne?re=t[35]:(re=H(jt,{isExpanded:ne,className:`card__collapse-toggle-icon`}),t[34]=ne,t[35]=re);let ie=!y&&I,ae;t[36]!==O||t[37]!==E||t[38]!==L||t[39]!==ee||t[40]!==R||t[41]!==te||t[42]!==re||t[43]!==ie?(ae=U(`button`,{onClick:L,className:`card__collapsible-button button--reset`,id:E,"aria-controls":O,"aria-expanded":ee,"aria-label":R,"aria-labelledby":te,children:[re,ie]}),t[36]=O,t[37]=E,t[38]=L,t[39]=ee,t[40]=R,t[41]=te,t[42]=re,t[43]=ie,t[44]=ae):ae=t[44];let oe=ae,se;t[45]===S.style?se=t[46]:(se=Zc(S.style),t[45]=S.style,t[46]=se);let ce;t[47]!==oe||t[48]!==v||t[49]!==I||t[50]!==y?(ce=v?y?U(`div`,{className:`card__collapsible-header`,children:[oe,I]}):oe:I,t[47]=oe,t[48]=v,t[49]=I,t[50]=y,t[51]=ce):ce=t[51];let le;t[52]!==i||t[53]!==T||t[54]!==ce?(le=U(`header`,{id:T,children:[ce,i]}),t[52]=i,t[53]=T,t[54]=ce,t[55]=le):le=t[55];let ue;t[56]!==O||t[57]!==n||t[58]!==T||t[59]!==C||t[60]!==x?(ue=H(`div`,{className:`card__body`,id:O,"aria-labelledby":T,"aria-hidden":C,"data-scrollable":x,children:n}),t[56]=O,t[57]=n,t[58]=T,t[59]=C,t[60]=x,t[61]=ue):ue=t[61];let de;return t[62]!==v||t[63]!==C||t[64]!==s||t[65]!==S.style||t[66]!==se||t[67]!==le||t[68]!==ue||t[69]!==m||t[70]!==_?(de=U(`section`,{ref:s,css:se,className:`card`,"data-collapsible":v,"data-collapsed":C,"data-title-separator":_,"data-testid":m,style:S.style,children:[le,ue]}),t[62]=v,t[63]=C,t[64]=s,t[65]=S.style,t[66]=se,t[67]=le,t[68]=ue,t[69]=m,t[70]=_,t[71]=de):de=t[71],de}var $c=q`
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
`;function el(e){let t=(0,Z.c)(13),n,r,i,a,o;t[0]===e?(n=t[1],r=t[2],i=t[3],a=t[4],o=t[5]):({ref:i,children:n,labelPlacement:a,size:o,...r}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a,t[5]=o);let s=a===void 0?`end`:a,c=o===void 0?`M`:o,l;t[6]===Symbol.for(`react.memo_cache_sentinel`)?(l=H(`div`,{className:`indicator`}),t[6]=l):l=t[6];let u;return t[7]!==n||t[8]!==s||t[9]!==r||t[10]!==i||t[11]!==c?(u=U(he,{...r,ref:i,css:$c,"data-label-placement":s,"data-size":c,children:[l,n]}),t[7]=n,t[8]=s,t[9]=r,t[10]=i,t[11]=c,t[12]=u):u=t[12],u}q`
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
`;var tl=q`
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
`,nl=q`
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
`;function rl(e,t){let{si:n=!1,decimalPlaces:r=1}=t??{},i=n?1e3:1024;if(Math.abs(e)<i)return e+` B`;let a=n?[`kB`,`MB`,`GB`,`TB`,`PB`,`EB`,`ZB`,`YB`]:[`KiB`,`MiB`,`GiB`,`TiB`,`PiB`,`EiB`,`ZiB`,`YiB`],o=-1,s=10**r;do e/=i,++o;while(Math.round(Math.abs(e)*s)/s>=i&&o<a.length-1);return e.toFixed(r)+` `+a[o]}function il(e,t){return!t||t.length===0||t.some(t=>{if(t.startsWith(`.`))return e.name.toLowerCase().endsWith(t.toLowerCase());if(t.endsWith(`/*`)){let n=t.slice(0,-2);return e.type.startsWith(n)}return e.type===t})}function al(e,t){return t==null||e.size<=t}function ol(e){let t=(0,Z.c)(46),n,r,i,a,o,s,c,l,u,d;t[0]===e?(n=t[1],r=t[2],i=t[3],a=t[4],o=t[5],s=t[6],c=t[7],l=t[8],u=t[9],d=t[10]):({acceptedFileTypes:n,allowsMultiple:u,maxFiles:s,maxFileSize:o,onSelect:c,onSelectRejected:l,label:d,description:i,isDisabled:a,...r}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a,t[5]=o,t[6]=s,t[7]=c,t[8]=l,t[9]=u,t[10]=d);let f=u!==void 0&&u,p=d===void 0?`Drag and drop files here`:d,m=(0,X.useRef)(null),h=(0,X.useRef)(null),g,_;t[11]===a?(g=t[12],_=t[13]):(g=()=>{let e=h.current;if(!e||a)return;let t=e=>{(e.key===`Enter`||e.key===` `)&&(e.preventDefault(),m.current?.click())};return e.addEventListener(`keydown`,t),()=>e.removeEventListener(`keydown`,t)},_=[a],t[11]=a,t[12]=g,t[13]=_),(0,X.useEffect)(g,_);let v;t[14]!==n||t[15]!==f||t[16]!==o||t[17]!==s||t[18]!==c||t[19]!==l?(v=e=>{let t=[],r=[],i=f?s??1/0:1;for(let a of e){if(!il(a,n)){r.push({file:a,reason:`type`,message:`File type not accepted. Allowed: ${n?.join(`, `)}`});continue}if(!al(a,o)){r.push({file:a,reason:`size`,message:`File too large. Maximum size: ${rl(o)}`});continue}if(t.length>=i){r.push({file:a,reason:`count`,message:`Maximum ${i} file${i>1?`s`:``} allowed`});continue}t.push(a)}t.length>0&&c&&c(t),r.length>0&&l&&l(r)},t[14]=n,t[15]=f,t[16]=o,t[17]=s,t[18]=c,t[19]=l,t[20]=v):v=t[20];let y=v,b;t[21]===y?b=t[22]:(b=e=>{e.target.files&&(y(Array.from(e.target.files)),e.target.value=``)},t[21]=y,t[22]=b);let x=b,S;t[23]===y?S=t[24]:(S=async e=>{let t=e.items.filter(ul),n=(await Promise.allSettled(t.map(ll))).filter(cl).map(sl);n.length>0&&y(n)},t[23]=y,t[24]=S);let C=S,w;t[25]!==n||t[26]!==a?(w=e=>a?`cancel`:!n||n.length===0||n.some(t=>t.startsWith(`.`)||t.endsWith(`/*`)?!0:e.has(t))?`copy`:`cancel`,t[25]=n,t[26]=a,t[27]=w):w=t[27];let T=w,E;t[28]===a?E=t[29]:(E=()=>{a||m.current?.click()},t[28]=a,t[29]=E);let D=E,O;t[30]!==n||t[31]!==i?(O=i??(n&&n.length>0?`Accepted: ${n.join(`, `)}`:void 0),t[30]=n,t[31]=i,t[32]=O):O=t[32];let k=O,A;t[33]!==n||t[34]!==f||t[35]!==k||t[36]!==x||t[37]!==p||t[38]!==D?(A=e=>{let{isDropTarget:t}=e;return U(G,{children:[H(`input`,{ref:m,type:`file`,accept:n?.join(`,`),multiple:f,onChange:x,hidden:!0}),U(`div`,{className:`file-drop-zone__trigger`,onClick:D,children:[H(`div`,{className:`file-drop-zone__icon`,children:H(V,{svg:H(Ye,{})})}),H(bt,{className:`file-drop-zone__label`,children:t?`Drop files here`:p}),k?H(bt,{className:`file-drop-zone__description`,children:k}):null]})]})},t[33]=n,t[34]=f,t[35]=k,t[36]=x,t[37]=p,t[38]=D,t[39]=A):A=t[39];let j;return t[40]!==r||t[41]!==T||t[42]!==C||t[43]!==a||t[44]!==A?(j=H(ee,{ref:h,css:tl,onDrop:C,getDropOperation:T,isDisabled:a,...r,children:A}),t[40]=r,t[41]=T,t[42]=C,t[43]=a,t[44]=A,t[45]=j):j=t[45],j}function sl(e){return e.value}function cl(e){return e.status===`fulfilled`}function ll(e){return e.getFile()}function ul(e){return e.kind===`file`}function dl(e){switch(e.status){case`pending`:return`Pending`;case`uploading`:return`Uploading${e.progress===void 0?``:` ${e.progress}%`}`;case`parsing`:return`Parsing...`;case`complete`:return`Complete`;case`error`:return`Error`;default:return``}}function fl(e){let t=(0,Z.c)(32),{file:n,onRemove:r,isDisabled:i}=e,{file:a,progress:o,status:s,error:c}=n,l=s===`uploading`&&o!==void 0,u;t[0]===Symbol.for(`react.memo_cache_sentinel`)?(u=H(`div`,{className:`file-list__icon`,children:H(V,{svg:H(tt,{})})}),t[0]=u):u=t[0];let d;t[1]===a.name?d=t[2]:(d=H(`span`,{className:`file-list__name`,title:a.name,children:a.name}),t[1]=a.name,t[2]=d);let f;t[3]===a.size?f=t[4]:(f=rl(a.size),t[3]=a.size,t[4]=f);let p;t[5]===f?p=t[6]:(p=H(`span`,{children:f}),t[5]=f,t[6]=p);let m;t[7]!==n||t[8]!==s?(m=s&&U(G,{children:[H(`span`,{children:`-`}),H(`span`,{children:dl(n)})]}),t[7]=n,t[8]=s,t[9]=m):m=t[9];let h;t[10]!==p||t[11]!==m?(h=U(`div`,{className:`file-list__meta`,children:[p,m]}),t[10]=p,t[11]=m,t[12]=h):h=t[12];let g;t[13]===c?g=t[14]:(g=c&&H(`span`,{className:`file-list__error`,children:c}),t[13]=c,t[14]=g);let _;t[15]!==o||t[16]!==l?(_=l&&H(`div`,{className:`file-list__progress`,children:H(Oi,{value:o,width:`100%`,height:`4px`})}),t[15]=o,t[16]=l,t[17]=_):_=t[17];let v;t[18]!==d||t[19]!==h||t[20]!==g||t[21]!==_?(v=U(`div`,{className:`file-list__details`,children:[d,h,g,_]}),t[18]=d,t[19]=h,t[20]=g,t[21]=_,t[22]=v):v=t[22];let y;t[23]!==a||t[24]!==i||t[25]!==r||t[26]!==s?(y=r&&H(`div`,{className:`file-list__remove`,children:H(Qt,{size:`S`,"aria-label":`Remove ${a.name}`,onPress:()=>r(a),isDisabled:i||s===`uploading`||s===`parsing`,children:H(V,{svg:H(wt,{})})})}),t[23]=a,t[24]=i,t[25]=r,t[26]=s,t[27]=y):y=t[27];let b;return t[28]!==s||t[29]!==y||t[30]!==v?(b=U(`li`,{className:`file-list__item`,"data-status":s,children:[u,v,y]}),t[28]=s,t[29]=y,t[30]=v,t[31]=b):b=t[31],b}function pl(e){let t=(0,Z.c)(12),{files:n,onRemove:r,isDisabled:i,children:a,"aria-label":o}=e,s=o===void 0?`Selected files`:o;if(n.length===0)return null;let c=ml,l;t[0]!==a||t[1]!==i||t[2]!==r?(l=(e,t)=>a?H(X.Fragment,{children:a(e,t)},c(e)):H(fl,{file:e,onRemove:r,isDisabled:i},c(e)),t[0]=a,t[1]=i,t[2]=r,t[3]=l):l=t[3];let u=l,d;if(t[4]!==n||t[5]!==u){let e;t[7]===u?e=t[8]:(e=(e,t)=>u(e,t),t[7]=u,t[8]=e),d=n.map(e),t[4]=n,t[5]=u,t[6]=d}else d=t[6];let f;return t[9]!==s||t[10]!==d?(f=H(`ul`,{css:nl,"aria-label":s,children:d}),t[9]=s,t[10]=d,t[11]=f):f=t[11],f}function ml(e){return`${e.file.name}-${e.file.size}-${e.file.lastModified}`}var hl=e=>q`
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: ${e};
  overflow: hidden;
  text-overflow: ellipsis;
`;function gl(e){let t=(0,Z.c)(5),{children:n,lines:r}=e,i;t[0]===r?i=t[1]:(i=hl(r),t[0]=r,t[1]=i);let a;return t[2]!==n||t[3]!==i?(a=H(`div`,{css:i,children:n}),t[2]=n,t[3]=i,t[4]=a):a=t[4],a}var _l=q`
  text-overflow: ellipsis;
  overflow: hidden;
  white-space: nowrap;
`,vl=q`
  display: -webkit-box;
  -webkit-box-orient: vertical;
  overflow: hidden;
`,yl=e=>{let t=(0,Z.c)(11),{children:n,maxWidth:r,title:i,maxLines:a}=e,o=(a??0)>1,s=o?vl:_l,c;t[0]!==o||t[1]!==a?(c=o&&{WebkitLineClamp:a},t[0]=o,t[1]=a,t[2]=c):c=t[2];let l;t[3]!==r||t[4]!==c?(l={maxWidth:r,...c},t[3]=r,t[4]=c,t[5]=l):l=t[5];let u;return t[6]!==n||t[7]!==s||t[8]!==l||t[9]!==i?(u=H(`div`,{css:s,style:l,title:i,children:n}),t[6]=n,t[7]=s,t[8]=l,t[9]=i,t[10]=u):u=t[10],u};function bl(){let e=(0,Z.c)(3),t,n;e[0]===Symbol.for(`react.memo_cache_sentinel`)?(t=H(Qt,{slot:`previous`,size:`S`,children:H(V,{svg:H(Ht,{})})}),n=H(Ge,{className:`calendar__heading`}),e[0]=t,e[1]=n):(t=e[0],n=e[1]);let r;return e[2]===Symbol.for(`react.memo_cache_sentinel`)?(r=U(`header`,{className:`calendar__header`,children:[t,n,H(Qt,{slot:`next`,size:`S`,children:H(V,{svg:H(On,{})})})]}),e[2]=r):r=e[2],r}function xl(e){let t=(0,Z.c)(8),{months:n,errorMessage:r}=e,i;t[0]===Symbol.for(`react.memo_cache_sentinel`)?(i=H(bl,{}),t[0]=i):i=t[0];let a;t[1]===n?a=t[2]:(a=H(`div`,{className:`calendar__months`,children:Array.from({length:n},Sl)}),t[1]=n,t[2]=a);let o;t[3]===r?o=t[4]:(o=r&&H(bt,{slot:`errorMessage`,children:r}),t[3]=r,t[4]=o);let s;return t[5]!==a||t[6]!==o?(s=U(G,{children:[i,a,o]}),t[5]=a,t[6]=o,t[7]=s):s=t[7],s}function Sl(e,t){return H(_,{offset:{months:t},children:Cl},t)}function Cl(e){return H(Te,{date:e})}var wl=q`
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
`,Tl=q`
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
`,El=q`
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
`;function Dl(e){let t=(0,Z.c)(10),n,r,i,a;if(t[0]!==e){let{ref:o,...c}=e;r=o;let{css:l,...u}=c;i=u,n=s,a=q(Fo,El,l),t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a}else n=t[1],r=t[2],i=t[3],a=t[4];let o;return t[5]!==n||t[6]!==r||t[7]!==i||t[8]!==a?(o=H(n,{css:a,...i,"data-size":`S`,ref:r}),t[5]=n,t[6]=r,t[7]=i,t[8]=a,t[9]=o):o=t[9],o}function Ol(e){let t=(0,Z.c)(17),n,r,i,a,o;t[0]===e?(n=t[1],r=t[2],i=t[3],a=t[4],o=t[5]):({errorMessage:r,css:i,children:n,ref:a,...o}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a,t[5]=o);let s=e.visibleDuration?.months||1,c;t[6]===i?c=t[7]:(c=q(wl,Tl,i),t[6]=i,t[7]=c);let l;t[8]!==n||t[9]!==r||t[10]!==s?(l=n??H(xl,{months:s,errorMessage:r}),t[8]=n,t[9]=r,t[10]=s,t[11]=l):l=t[11];let u;return t[12]!==a||t[13]!==o||t[14]!==c||t[15]!==l?(u=H(h,{ref:a,css:c,...o,children:l}),t[12]=a,t[13]=o,t[14]=c,t[15]=l,t[16]=u):u=t[16],u}q`
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
`;var kl=q`
  font-family: var(--global-font-family-mono);
  font-variant-numeric: tabular-nums;
  ${He};
`;function Al(e){return e.toString().padStart(2,`0`)}function jl(e){let t=Math.floor(e/3600),n=Math.floor(e%3600/60),r=e%60;return t>0?`${Al(t)}:${Al(n)}:${Al(r)}`:`${Al(n)}:${Al(r)}`}function Ml(e){return Math.max(0,Math.floor((Date.now()-e.getTime())/1e3))}function Nl(e){let t=(0,Z.c)(18),{startTime:n,color:r,size:i}=e,a=r===void 0?`text-900`:r,o=i===void 0?`S`:i,s;t[0]===n?s=t[1]:(s=n??new Date,t[0]=n,t[1]=s);let c=s,l;t[2]===c?l=t[3]:(l=()=>Ml(c),t[2]=c,t[3]=l);let[u,d]=(0,X.useState)(l),f,p;t[4]===c?(f=t[5],p=t[6]):(f=()=>{d(Ml(c));let e=setInterval(()=>{d(Ml(c))},1e3);return()=>clearInterval(e)},p=[c],t[4]=c,t[5]=f,t[6]=p),(0,X.useEffect)(f,p);let m;t[7]===a?m=t[8]:(m=gt(a),t[7]=a,t[8]=m);let h;t[9]===m?h=t[10]:(h={color:m},t[9]=m,t[10]=h);let g=`PT${u}S`,_;t[11]===u?_=t[12]:(_=jl(u),t[11]=u,t[12]=_);let v;return t[13]!==o||t[14]!==h||t[15]!==g||t[16]!==_?(v=H(`time`,{css:kl,"data-size":o,style:h,dateTime:g,children:_}),t[13]=o,t[14]=h,t[15]=g,t[16]=_,t[17]=v):v=t[17],v}var Pl=q`
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
`,Fl=2e3,Il=q`
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
    ${Pl}
  }
`,Ll=e=>{let t=(0,Z.c)(20),{id:n,size:r,tooltipText:i,variant:a}=e,o=r===void 0?`S`:r,s=i===void 0?`Copy ID`:i,c=a===void 0?`badge`:a,[l,u]=(0,X.useState)(!1),d=l?`success`:`inherit`,f=l?`Checkmark`:`Duplicate`,p;t[0]!==d||t[1]!==f?(p=H(V,{className:`id-badge__copy-icon`,color:d,svgKey:f}),t[0]=d,t[1]=f,t[2]=p):p=t[2];let m=p,h=`${s} ${n}`,_;t[3]===n?_=t[4]:(_=()=>{Ie(n),u(!0),setTimeout(()=>{u(!1)},Fl)},t[3]=n,t[4]=_);let v;t[5]!==m||t[6]!==n||t[7]!==o||t[8]!==c?(v=c===`badge`?U(Oo,{size:o,children:[H(V,{svgKey:`ID`}),H(B,{fontFamily:`mono`,size:`S`,color:`text-700`,children:n}),m]}):U(G,{children:[H(B,{fontFamily:`mono`,size:`S`,color:`text-500`,children:n}),m]}),t[5]=m,t[6]=n,t[7]=o,t[8]=c,t[9]=v):v=t[9];let y;t[10]!==h||t[11]!==_||t[12]!==v||t[13]!==c?(y=H(Tt,{css:Il,"data-variant":c,"aria-label":h,onPress:_,children:v}),t[10]=h,t[11]=_,t[12]=v,t[13]=c,t[14]=y):y=t[14];let b=l?`Copied`:s,x;t[15]===b?x=t[16]:(x=H(Ni,{offset:1,children:b}),t[15]=b,t[16]=x);let S;return t[17]!==y||t[18]!==x?(S=U(g,{children:[y,x]}),t[17]=y,t[18]=x,t[19]=S):S=t[19],S},Rl=e=>{let t=(0,Z.c)(7),{title:n,id:r}=e,i;t[0]===n?i=t[1]:(i=H(Xe,{children:n}),t[0]=n,t[1]=i);let a;t[2]===r?a=t[3]:(a=H(Ll,{size:`S`,id:r}),t[2]=r,t[3]=a);let o;return t[4]!==i||t[5]!==a?(o=U(K,{direction:`row`,gap:`size-100`,alignItems:`center`,children:[i,a]}),t[4]=i,t[5]=a,t[6]=o):o=t[6],o},zl=`selectedSpanNodeId`,Bl=`sessionView`,Vl=`selectedTraceId`,Hl=[Vl,zl],Ul=`timeRangeKey`,Wl=`timeRangeStart`,Gl=`timeRangeEnd`,Kl=`labelId`,ql=`createCodeEvaluator`,Jl=`createLlmEvaluator`,Yl=[{key:`15m`,label:`Last 15 Min`},{key:`1h`,label:`Last Hour`},{key:`12h`,label:`Last 12 Hours`},{key:`1d`,label:`Last Day`},{key:`7d`,label:`Last 7 Days`},{key:`30d`,label:`Last Month`}],Xl=Yl.reduce((e,t)=>({...e,[t.key]:t}),{}),Zl=60*1e3,Ql=60*Zl,$l=24*Ql,eu=/^(\d+)([mhd])$/;function tu(e){if(typeof e!=`string`)return null;let t=eu.exec(e);if(!t)return null;let n=parseInt(t[1],10);return n<1?null:{quantity:n,unit:t[2]}}function nu({quantity:e,unit:t}){switch(t){case`m`:return e*Zl;case`h`:return e*Ql;case`d`:return e*$l;default:Wn(t)}}function ru(e,t=Date.now()){let n=tu(e);if(!n)throw Error(`Invalid last N time range key: ${e}`);let{quantity:r,unit:i}=n,a;switch(i){case`m`:a=L(t,r);break;case`h`:a=Se(t,r);break;case`d`:a=je(t,r);break;default:Wn(i)}return{start:(nu(n)<=Ql?ne:ge)(a),end:null}}function iu(e){let t=tu(e),n=t&&nu(t)<=Ql?Zl:Ql,r=Date.now()%n;return r===0?n:n-r}function au(e){return tu(e)!==null}function ou(e){if(e==null||e.trim()===``)return null;let t=new Date(e);return Number.isNaN(t.getTime())?void 0:t}function su(e,t=Date.now()){let n=e.get(Ul);if(au(n))return{timeRangeKey:n,...ru(n,t)};let r=ou(e.get(Wl)),i=ou(e.get(Gl));return r===void 0||i===void 0||r==null&&i==null||r!=null&&i!=null&&r>i?null:{timeRangeKey:`custom`,start:r,end:i}}function cu({searchParams:e,timeRange:t}){let n=new URLSearchParams(e),r=(e,t)=>{t==null?n.delete(e):n.set(e,t.toISOString())};return au(t.timeRangeKey)?(n.set(Ul,t.timeRangeKey),n.delete(Wl),n.delete(Gl),n):(n.delete(Ul),r(Wl,t.start),r(Gl,t.end),n)}var lu={m:{singular:`minute`,plural:`minutes`},h:{singular:`hour`,plural:`hours`},d:{singular:`day`,plural:`days`}};function uu(e){let t=Xl[e];if(t)return t.label;let n=tu(e);if(!n)return e;let{quantity:r,unit:i}=n,{singular:a,plural:o}=lu[i];return`Last ${r} ${r===1?a:o}`}var du=/^(?:last\s+)?(\d+)\s*(m|min|mins|minute|minutes|h|hr|hrs|hour|hours|d|day|days)$/,fu=/^(?:last\s+)?(\d+)$/;function pu(e){let t=du.exec(e.trim().toLowerCase());if(!t)return null;let n=parseInt(t[1],10);return n<1?null:`${n}${t[2][0]}`}function mu(e){let t=pu(e);if(t)return[t];let n=fu.exec(e.trim().toLowerCase());if(!n)return[];let r=parseInt(n[1],10);return r<1?[]:[`${r}m`,`${r}h`,`${r}d`]}var hu=.5,gu=2,_u=Zl;function vu({value:e,now:t}){if(!e.start)return null;let n=e.start.getTime(),r=(e.end??t).getTime(),i=r-n;return i<=0?null:{startMs:n,endMs:r,durationMs:i}}function yu(e){let t=Math.max(1,Math.round(e/Zl)),n=t/1440;if(n>=2||Number.isInteger(n))return`${Math.round(n)}d`;let r=t/60;return r>=2||Number.isInteger(r)?`${Math.round(r)}h`:`${t}m`}function bu({value:e,now:t=new Date,shiftFraction:n=hu}){let r=vu({value:e,now:t});if(!r)return null;let i=r.durationMs*n;return{timeRangeKey:`custom`,start:new Date(r.startMs-i),end:new Date(r.endMs-i)}}function xu({value:e,now:t=new Date,shiftFraction:n=hu}){if(!e.end)return null;let r=vu({value:e,now:t});if(!r)return null;let i=Math.min(r.durationMs*n,t.getTime()-r.endMs);return i<=0?null:{timeRangeKey:`custom`,start:new Date(r.startMs+i),end:new Date(r.endMs+i)}}function Su({value:e,now:t=new Date,zoomFactor:n=gu,minWindowMs:r=_u}){return wu({value:e,now:t,factor:1/n,minWindowMs:r})}function Cu({value:e,now:t=new Date,zoomFactor:n=gu,minWindowMs:r=_u}){return wu({value:e,now:t,factor:n,minWindowMs:r})}function wu({value:e,now:t,factor:n,minWindowMs:r}){if(!e.end){let i=tu(e.timeRangeKey),a=i?nu(i):vu({value:e,now:t})?.durationMs;if(a==null)return null;let o=Math.max(a*n,r);if(n<1&&o>=a)return null;let s=yu(o);return s===e.timeRangeKey?null:{timeRangeKey:s,...ru(s)}}let i=vu({value:e,now:t});if(!i)return null;let a=Math.max(i.durationMs*n,r);if(n<1?a>=i.durationMs:a===i.durationMs)return null;let o=(i.startMs+i.endMs)/2,s=o-a/2,c=o+a/2,l=c-t.getTime();return l>0&&(s-=l,c-=l),{timeRangeKey:`custom`,start:new Date(s),end:new Date(c)}}function Tu(e,t){return e?oe(e,t):null}var Eu=q`
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
`,Du=q`
  .react-aria-DateInput {
    width: 100%;
    min-width: 0;
  }
`,Ou=new A(0,0,0),ku=new A(23,59,59);function Au(e){let n=(0,Z.c)(56),{value:r,timeZone:i,onApply:a,onCancel:o}=e,s;n[0]!==i||n[1]!==r.start?(s=()=>Tu(r.start,i),n[0]=i,n[1]=r.start,n[2]=s):s=n[2];let[l,u]=(0,X.useState)(s),d;n[3]!==i||n[4]!==r.end?(d=()=>Tu(r.end,i)??Ne(i),n[3]=i,n[4]=r.end,n[5]=d):d=n[5];let[f,p]=(0,X.useState)(d),m;n[6]!==l||n[7]!==i?(m=l?l.toDate(i):null,n[6]=l,n[7]=i,n[8]=m):m=n[8];let h=m,g;n[9]!==f||n[10]!==i?(g=f?f.toDate(i):null,n[9]=f,n[10]=i,n[11]=g):g=n[11];let _=g,v=!!(h&&_&&h>_),y;n[12]!==_||n[13]!==v||n[14]!==h?(y=h&&_&&!v?{start:h,end:_}:null,n[12]=_,n[13]=v,n[14]=h,n[15]=y):y=n[15];let b=y,x;n[16]!==f||n[17]!==v||n[18]!==l?(x=l&&f&&!v?{start:S(l),end:S(f)}:null,n[16]=f,n[17]=v,n[18]=l,n[19]=x):x=n[19];let C=x,w;n[20]===Symbol.for(`react.memo_cache_sentinel`)?(w={months:2},n[20]=w):w=n[20];let T;n[21]===i?T=n[22]:(T=e=>{e&&(u(M(t(e.start,Ou),i)),p(M(t(e.end,ku),i)))},n[21]=i,n[22]=T);let E;n[23]!==C||n[24]!==T?(E=H(Ol,{"aria-label":`Time range`,visibleDuration:w,value:C,onChange:T}),n[23]=C,n[24]=T,n[25]=E):E=n[25];let D,O;n[26]===Symbol.for(`react.memo_cache_sentinel`)?(O=H(yn,{children:`Start`}),D=H(c,{children:Mu}),n[26]=D,n[27]=O):(D=n[26],O=n[27]);let k;n[28]===l?k=n[29]:(k=U(Dl,{granularity:`minute`,hideTimeZone:!0,value:l,onChange:u,css:Du,children:[O,D]}),n[28]=l,n[29]=k);let A,j;n[30]===Symbol.for(`react.memo_cache_sentinel`)?(A=H(yn,{children:`End`}),j=H(c,{children:ju}),n[30]=A,n[31]=j):(A=n[30],j=n[31]);let N;n[32]!==f||n[33]!==v?(N=U(Dl,{granularity:`minute`,hideTimeZone:!0,isInvalid:v,value:f,onChange:p,css:Du,children:[A,j]}),n[32]=f,n[33]=v,n[34]=N):N=n[34];let P;n[35]!==k||n[36]!==N?(P=U(`div`,{className:`time-range-calendar-picker__fields`,children:[k,N]}),n[35]=k,n[36]=N,n[37]=P):P=n[37];let F;n[38]===v?F=n[39]:(F=v&&H(B,{size:`XS`,color:`danger`,className:`time-range-calendar-picker__error`,children:`End must be after the start`}),n[38]=v,n[39]=F);let I;n[40]===o?I=n[41]:(I=H(W,{size:`S`,onPress:o,children:`Cancel`}),n[40]=o,n[41]=I);let L=!b,ee;n[42]!==b||n[43]!==a?(ee=()=>{b&&a(b)},n[42]=b,n[43]=a,n[44]=ee):ee=n[44];let R;n[45]!==L||n[46]!==ee?(R=H(W,{"data-testid":`time-range-calendar-picker-apply-button`,size:`S`,variant:`primary`,isDisabled:L,onPress:ee,children:`Apply`}),n[45]=L,n[46]=ee,n[47]=R):R=n[47];let te;n[48]!==F||n[49]!==I||n[50]!==R?(te=U(`div`,{className:`time-range-calendar-picker__controls`,children:[F,I,R]}),n[48]=F,n[49]=I,n[50]=R,n[51]=te):te=n[51];let ne;return n[52]!==P||n[53]!==te||n[54]!==E?(ne=U(`div`,{"data-testid":`time-range-calendar-picker`,className:`time-range-calendar-picker`,css:Eu,children:[E,P,te]}),n[52]=P,n[53]=te,n[54]=E,n[55]=ne):ne=n[55],ne}function ju(e){return H(T,{segment:e})}function Mu(e){return H(T,{segment:e})}var Nu=`set_time_range`,Pu=[`15m`,`1h`,`12h`,`1d`,`7d`,`30d`,`custom`];function Fu(e){return typeof e==`string`&&Pu.includes(e)}function Iu(e){if(typeof e!=`object`||!e)return null;let t=e;return!Fu(t.timeRangeKey)||t.startTime!==void 0&&typeof t.startTime!=`string`||t.endTime!==void 0&&typeof t.endTime!=`string`?null:{timeRangeKey:t.timeRangeKey,...t.startTime===void 0?{}:{startTime:t.startTime},...t.endTime===void 0?{}:{endTime:t.endTime}}}function Lu(e,t){return typeof e==`function`?e(t):e}function Ru(e){return{name:e.name,uiBehavior:e.uiBehavior,requiredCapabilities:e.requiredCapabilities,dispatch:async t=>{let n=e.parseInput(t.toolCall.input);if(n==null){await t.addToolOutput({state:`output-error`,tool:e.name,toolCallId:t.toolCall.toolCallId,errorText:Lu(e.invalidInputErrorText,t.toolCall.input)});return}await e.execute({...t,input:n})}}}async function zu({toolName:e,toolCall:t,sessionId:n,addToolOutput:r,errorText:i}){return n??(await r({state:`output-error`,tool:e,toolCallId:t.toolCallId,errorText:i}),null)}async function Bu({result:e,toolName:t,toolCallId:n,addToolOutput:r,defaultSuccessOutput:i,emitSuccess:a}){if(e.ok){if(!a)return;await r({state:`output-available`,tool:t,toolCallId:n,output:e.output??i});return}await r({state:`output-error`,tool:t,toolCallId:n,errorText:e.error})}function Vu(e){let t=e.emitSuccess??!0,n=e.defaultSuccessOutput??`Done.`;return Ru({name:e.name,parseInput:e.parseInput,invalidInputErrorText:e.invalidInputErrorText,requiredCapabilities:e.requiredCapabilities,uiBehavior:e.uiBehavior,execute:async({toolCall:r,input:i,sessionId:a,addToolOutput:o,agentStore:s})=>{let c=s.getState().registeredClientActions[e.name];if(!c){await o({state:`output-error`,tool:e.name,toolCallId:r.toolCallId,errorText:e.notMountedErrorText});return}e.requireSession&&await zu({toolName:e.name,toolCall:r,sessionId:a,addToolOutput:o,errorText:e.noSessionErrorText??`Cannot run this tool without an active session.`})==null||await Bu({result:e.buildContext?await c(i,e.buildContext({toolCall:r,sessionId:a,addToolOutput:o,agentStore:s})):await c(i),toolName:e.name,toolCallId:r.toolCallId,addToolOutput:o,defaultSuccessOutput:n,emitSuccess:t})}})}var Hu=Vu({name:Nu,parseInput:Iu,invalidInputErrorText:`Invalid ${Nu} input. Expected { timeRangeKey: ${Pu.map(e=>`"${e}"`).join(` | `)}, startTime?: string, endTime?: string }.`,notMountedErrorText:`The app time range selector is not mounted on this page; cannot update the time range.`,defaultSuccessOutput:`Time range updated.`});function Uu(e){switch(e.type){case`app`:return`app`;case`playground`:return`playground`;case`code_evaluator`:return e.evaluatorNodeId?`code_evaluator:${e.evaluatorNodeId}`:`code_evaluator:create`;case`llm_evaluator`:return e.evaluatorNodeId?`llm_evaluator:${e.evaluatorNodeId}`:`llm_evaluator:create`;case`dataset`:return e.datasetVersionNodeId?`dataset:${e.datasetNodeId}:${e.datasetVersionNodeId}`:`dataset:${e.datasetNodeId}`;case`project`:return`project:${e.projectNodeId}`;case`trace`:return`trace:${e.projectNodeId}:${e.otelTraceId}`;case`session`:return`session:${e.projectNodeId}:${e.sessionNodeId}`;case`prompt`:return`prompt:${e.promptNodeId}`;case`prompt_version`:return`prompt_version:${e.promptNodeId}:${e.promptVersionNodeId}`;case`span`:return`span:${e.projectNodeId??``}:${e.spanNodeId?`node:${e.spanNodeId}`:`otel:${e.otelSpanId}`}`;case`graphql`:return`graphql`;case`web_access`:return`web_access`;case`subagents`:return`subagents`}}var Wu={"bash.retainInactiveSessions":!1,"graphql.mutations":!1,"session.storeSessions":!1,"subagents.enabled":!1,"web.access":!1},Gu=[{key:`bash.retainInactiveSessions`,label:`Retain inactive bash sessions`,description:`Keeps browser bash runtimes alive when switching sessions instead of eagerly garbage-collecting them.`,defaultValue:!1,scope:`global`,controlSurface:`experimental-settings`},{key:`graphql.mutations`,label:`Dangerously enable mutations`,description:`Allows the phoenix-gql bash command to execute GraphQL mutations in addition to queries.`,defaultValue:!1,scope:`global`,controlSurface:`experimental-settings`},{key:`session.storeSessions`,label:`Store recent sessions`,description:`Keeps the three most recent chat sessions instead of replacing session history when starting a new chat.`,defaultValue:!1,scope:`global`,controlSurface:`experimental-settings`},{key:`subagents.enabled`,label:`Subagents`,description:`Lets the assistant delegate work to subagents that run their own tool-using turns. Experimental and may consume large numbers of tokens.`,defaultValue:!1,scope:`global`},{key:`web.access`,label:`Web search`,description:`Lets the assistant use provider-native web search and URL fetching when the selected model supports it.`,defaultValue:!1,scope:`global`}],Ku=Object.fromEntries(Gu.map(e=>[e.key,e]));for(let e of Object.keys(Wu))if(!Ku[e])throw Error(`Missing AGENT_CAPABILITY_DEFINITIONS entry for capability key: "${e}"`);function qu(){return{...Wu}}function Ju(e){return Ku[e]}function Yu(e){return Gu.filter(t=>t.controlSurface===e)}function Xu(e){return e.map(e=>e.toLowerCase())}var Zu=[`NONE`,`MINIMAL`,`LOW`,`MEDIUM`,`HIGH`,`XHIGH`],Qu=Xu(Zu),$u=Object.fromEntries(Zu.map(e=>[e,e.toLowerCase()]));function ed(e){return e in $u}function td(e){if(typeof e!=`string`)return;let t=e.trim();if(!t)return;let n=t.toUpperCase();if(ed(n))return n}function nd(e){let t=td(e);if(t!=null)return $u[t]}var rd=[`disabled`,`enabled`,`adaptive`],id=[`SUMMARIZED`,`OMITTED`],ad=Xu(id),od=[`LOW`,`MEDIUM`,`HIGH`,`XHIGH`,`MAX`],sd=Xu(od),cd=[`MINIMAL`,`LOW`,`MEDIUM`,`HIGH`],ld=Xu(cd),Q={OPENAI:`openai`,ANTHROPIC:`anthropic`,GOOGLE_GENAI:`google_genai`,AWS_BEDROCK:`aws_bedrock`};function ud(e){switch(e){case`OPENAI`:case`AZURE_OPENAI`:case`DEEPSEEK`:case`XAI`:case`OLLAMA`:case`CEREBRAS`:case`FIREWORKS`:case`GROQ`:case`MOONSHOT`:case`PERPLEXITY`:case`TOGETHER`:return Q.OPENAI;case`ANTHROPIC`:return Q.ANTHROPIC;case`GOOGLE`:return Q.GOOGLE_GENAI;case`AWS`:return Q.AWS_BEDROCK}return Wn(e)}var dd=[{name:`temperature`,type:`float`,min:0,max:2,label:`Temperature`,canonicalName:`TEMPERATURE`},{name:`topP`,type:`float`,min:0,max:1,label:`Top P`,canonicalName:`TOP_P`},{name:`maxCompletionTokens`,type:`int`,label:`Max Completion Tokens`,canonicalName:`MAX_COMPLETION_TOKENS`},{name:`frequencyPenalty`,type:`float`,min:-2,max:2,label:`Frequency Penalty`,applicableOpenAIApiTypes:[`CHAT_COMPLETIONS`]},{name:`presencePenalty`,type:`float`,min:-2,max:2,label:`Presence Penalty`,applicableOpenAIApiTypes:[`CHAT_COMPLETIONS`]},{name:`reasoningEffort`,type:`enum`,values:Qu,label:`Reasoning Effort`,canonicalName:`REASONING_EFFORT`},{name:`seed`,type:`int`,label:`Seed`,canonicalName:`RANDOM_SEED`}],fd=[{name:`maxTokens`,type:`int`,label:`Max Tokens`,required:!0,canonicalName:`MAX_COMPLETION_TOKENS`},{name:`temperature`,type:`float`,min:0,max:1,label:`Temperature`,canonicalName:`TEMPERATURE`},{name:`stopSequences`,type:`string_list`,label:`Stop Sequences`,canonicalName:`STOP_SEQUENCES`},{name:`topP`,type:`float`,min:0,max:1,label:`Top P`,canonicalName:`TOP_P`},{name:`thinkingType`,type:`enum`,values:rd,label:`Thinking`,canonicalName:`ANTHROPIC_EXTENDED_THINKING`},{name:`thinkingBudgetTokens`,type:`int`,min:1024,label:`Budget Tokens`},{name:`thinkingDisplay`,type:`enum`,values:ad,label:`Thinking Display`},{name:`effort`,type:`enum`,values:sd,label:`Effort`,canonicalName:`REASONING_EFFORT`}],pd=[{name:`temperature`,type:`float`,min:0,max:2,label:`Temperature`,canonicalName:`TEMPERATURE`},{name:`maxOutputTokens`,type:`int`,label:`Max Output Tokens`,canonicalName:`MAX_COMPLETION_TOKENS`},{name:`stopSequences`,type:`string_list`,label:`Stop Sequences`,canonicalName:`STOP_SEQUENCES`},{name:`presencePenalty`,type:`float`,label:`Presence Penalty`},{name:`frequencyPenalty`,type:`float`,label:`Frequency Penalty`},{name:`topP`,type:`float`,min:0,max:1,label:`Top P`,canonicalName:`TOP_P`},{name:`topK`,type:`int`,label:`Top K`},{name:`thinkingBudget`,type:`int`,min:0,label:`Thinking Budget`},{name:`thinkingLevel`,type:`enum`,values:ld,label:`Thinking Level`},{name:`includeThoughts`,type:`bool`,label:`Include Thoughts`}],md=[{name:`maxTokens`,type:`int`,label:`Max Tokens`,canonicalName:`MAX_COMPLETION_TOKENS`},{name:`temperature`,type:`float`,min:0,max:1,label:`Temperature`,canonicalName:`TEMPERATURE`},{name:`topP`,type:`float`,min:0,max:1,label:`Top P`,canonicalName:`TOP_P`}];Q.OPENAI,Q.ANTHROPIC,Q.GOOGLE_GENAI,Q.AWS_BEDROCK;var hd=1024,gd=2e3,_d={type:`adaptive`,display:`SUMMARIZED`},vd=`HIGH`,yd=Y().transform(e=>e.toUpperCase()).pipe(Fn(id)).optional().catch(void 0),bd=Y().transform(e=>e.toUpperCase()).pipe(Fn(od)).optional().catch(void 0),xd=Nn(Y()).optional().catch(void 0),Sd=Pn(Y(),Bn()).optional().catch(void 0),Cd=Ln(`type`,[In({type:zn(`disabled`)}),In({type:zn(`enabled`),budgetTokens:J(),display:yd}),In({type:zn(`adaptive`),display:yd})]).optional().catch(void 0),wd=Ln(`type`,[In({type:zn(`disabled`)}),In({type:zn(`enabled`),budget_tokens:J(),display:yd}),In({type:zn(`adaptive`),display:yd})]).optional().catch(void 0);function Td(e){if(e)switch(e.type){case`disabled`:return{type:`disabled`};case`enabled`:{let t={type:`enabled`,budgetTokens:e.budget_tokens};return e.display!==void 0&&(t.display=e.display),t}case`adaptive`:{let t={type:`adaptive`};return e.display!==void 0&&(t.display=e.display),t}default:return Wn(e)}}function Ed(e){return e?.type===`enabled`||e?.type===`adaptive`}function Dd(){return{maxTokens:gd,thinking:_d,effort:vd}}function Od(e){if(e==null)return fd;let t=Ed(e.thinking);return fd.flatMap(n=>{let r=`canonicalName`in n?n.canonicalName:null;return t&&(r===`TEMPERATURE`||r===`TOP_P`)?[]:n.name===`thinkingBudgetTokens`?e.thinking?.type===`enabled`?n.type===`int`?[{...n,max:e.maxTokens-1}]:[n]:[]:n.name===`thinkingDisplay`&&!t?[]:[n]})}var kd=Hn({maxTokens:J().optional().catch(void 0),temperature:J().optional().catch(void 0),topP:J().optional().catch(void 0),stopSequences:xd,thinking:Cd,effort:bd,extraBody:Sd});function Ad(e){let t=kd.safeParse(e),n=t.success?t.data:{},r={maxTokens:n.maxTokens??2e3};return n.temperature!==void 0&&(r.temperature=n.temperature),n.topP!==void 0&&(r.topP=n.topP),n.stopSequences!==void 0&&(r.stopSequences=[...n.stopSequences]),n.thinking!==void 0&&(r.thinking=n.thinking),n.effort!==void 0&&(r.effort=n.effort),n.extraBody!==void 0&&(r.extraBody={...n.extraBody}),r}function $(e){if(!Ed(e.thinking)||e.temperature===void 0&&e.topP===void 0)return e;let t={...e};return delete t.temperature,delete t.topP,t}function jd(e){let t=[];if(e.thinking?.type===`enabled`){let n=e.thinking.budgetTokens;n<1024&&t.push(`Thinking budget must be at least ${hd} (got ${n})`),n>=e.maxTokens&&t.push(`Thinking budget (${n}) must be less than max tokens (${e.maxTokens})`)}return t}function Md(e){switch(e.type){case`disabled`:return{disabled:{disabled:!0}};case`enabled`:return{enabled:{budgetTokens:e.budgetTokens,display:e.display??null}};case`adaptive`:return{adaptive:{display:e.display??null}};default:return Wn(e)}}function Nd(e){let t=$(e),n=jd(t);if(n.length>0)throw Error(`Cannot serialize Anthropic invocation parameters: ${n.join(`; `)}`);let r={maxTokens:t.maxTokens};return t.temperature!==void 0&&(r.temperature=t.temperature),t.topP!==void 0&&(r.topP=t.topP),t.stopSequences!==void 0&&(r.stopSequences=t.stopSequences),t.thinking!==void 0&&(r.thinking=Md(t.thinking)),t.effort!==void 0&&(r.outputConfig={effort:t.effort}),t.extraBody!==void 0&&(r.extraBody=t.extraBody),{anthropic:r}}function Pd(e){if(e.__typename!==`PromptAnthropicInvocationParameters`)throw Error(`anthropicAdapter.fromPromptInvocationParameters called with non-Anthropic typename: ${e.__typename}`);let t={maxTokens:e.anthropicMaxTokens};if(e.temperature!=null&&(t.temperature=e.temperature),e.topP!=null&&(t.topP=e.topP),e.stopSequences!=null&&(t.stopSequences=[...e.stopSequences]),e.outputConfig?.effort!=null&&(t.effort=e.outputConfig.effort),e.thinking)switch(e.thinking.__typename){case`PromptAnthropicThinkingDisabled`:t.thinking={type:`disabled`};break;case`PromptAnthropicThinkingEnabled`:{let n={type:`enabled`,budgetTokens:e.thinking.budgetTokens};e.thinking.enabledDisplay!=null&&(n.display=e.thinking.enabledDisplay),t.thinking=n;break}case`PromptAnthropicThinkingAdaptive`:{let n={type:`adaptive`};e.thinking.adaptiveDisplay!=null&&(n.display=e.thinking.adaptiveDisplay),t.thinking=n;break}case`%other`:break;default:Wn(e.thinking)}let n=Vd(e.extraBody);return n!=null&&(t.extraBody=n),$(t)}function Fd(e){if(e.__typename!==`PromptAnthropicInvocationParameters`)throw Error(`anthropicAdapter.fromPromptInvocationParametersForDisplay called with non-Anthropic typename: ${e.__typename}`);let t={maxTokens:e.anthropicMaxTokens};if(e.temperature!=null&&(t.temperature=e.temperature),e.topP!=null&&(t.topP=e.topP),e.stopSequences!=null&&(t.stopSequences=[...e.stopSequences]),e.outputConfig?.effort!=null&&(t.outputConfig={effort:e.outputConfig.effort}),e.thinking)switch(e.thinking.__typename){case`PromptAnthropicThinkingDisabled`:t.thinking={type:`disabled`};break;case`PromptAnthropicThinkingEnabled`:{let n={type:`enabled`,budgetTokens:e.thinking.budgetTokens};e.thinking.enabledDisplay!=null&&(n.display=e.thinking.enabledDisplay),t.thinking=n;break}case`PromptAnthropicThinkingAdaptive`:{let n={type:`adaptive`};e.thinking.adaptiveDisplay!=null&&(n.display=e.thinking.adaptiveDisplay),t.thinking=n;break}case`%other`:break;default:Wn(e.thinking)}let n=Vd(e.extraBody);return n!=null&&(t.extraBody=n),t}var Id=Hn({effort:bd,format:In({type:zn(`json_schema`),schema:Pn(Y(),Bn())}).optional().catch(void 0)}).optional().catch(void 0),Ld=Hn({max_tokens:J().optional().catch(void 0),temperature:J().optional().catch(void 0),top_p:J().optional().catch(void 0),stop_sequences:xd,thinking:wd,output_config:Id,extra_body:Sd});function Rd(e){let t=Ld.safeParse(e),n=t.success?t.data:{},r={maxTokens:n.max_tokens??2e3};n.temperature!==void 0&&(r.temperature=n.temperature),n.top_p!==void 0&&(r.topP=n.top_p),n.stop_sequences!==void 0&&(r.stopSequences=[...n.stop_sequences]);let i=Td(n.thinking);if(i!==void 0&&(r.thinking=i),n.output_config?.effort!==void 0&&(r.effort=n.output_config.effort),n.extra_body!==void 0){let e=Vd(n.extra_body);e!==void 0&&(r.extraBody=e)}let a={},o=n.output_config?.format;return o&&(a.responseFormat={type:`json_schema`,jsonSchema:{name:`response`,schema:o.schema}}),{config:$(r),promoted:a}}function zd(e,t){switch(t){case`maxTokens`:return e.maxTokens;case`temperature`:return e.temperature;case`topP`:return e.topP;case`stopSequences`:return e.stopSequences;case`thinkingType`:return e.thinking?.type;case`thinkingBudgetTokens`:return e.thinking?.type===`enabled`?e.thinking.budgetTokens:void 0;case`thinkingDisplay`:return e.thinking&&e.thinking.type!==`disabled`?e.thinking.display?.toLowerCase():void 0;case`effort`:return e.effort?.toLowerCase();case`extraBody`:return e.extraBody;default:return}}function Bd(e,t,n){switch(t){case`maxTokens`:return typeof n!=`number`||Number.isNaN(n)?e:$({...e,maxTokens:n});case`temperature`:if(n===void 0){let t={...e};return delete t.temperature,$(t)}return typeof n!=`number`||Number.isNaN(n)?e:$({...e,temperature:n});case`topP`:if(n===void 0){let t={...e};return delete t.topP,$(t)}return typeof n!=`number`||Number.isNaN(n)?e:$({...e,topP:n});case`stopSequences`:if(n===void 0){let t={...e};return delete t.stopSequences,$(t)}return Array.isArray(n)?$({...e,stopSequences:n.map(String)}):e;case`thinkingType`:if(n===void 0){let t={...e};return delete t.thinking,$(t)}if(n===`disabled`)return $({...e,thinking:{type:`disabled`}});if(n===`enabled`){let t=e.thinking,n=t?.type===`enabled`?t.budgetTokens:hd,r=t&&t.type!==`disabled`?t.display:void 0,i={type:`enabled`,budgetTokens:n};r!==void 0&&(i.display=r);let a=e.maxTokens>n?e.maxTokens:n+1;return $({...e,maxTokens:a,thinking:i})}if(n===`adaptive`){let t=e.thinking,n=t&&t.type!==`disabled`?t.display:void 0,r={type:`adaptive`};return n!==void 0&&(r.display=n),$({...e,thinking:r})}return e;case`thinkingBudgetTokens`:return e.thinking?.type!==`enabled`||n===void 0||typeof n!=`number`||Number.isNaN(n)?e:$({...e,thinking:{...e.thinking,budgetTokens:n}});case`thinkingDisplay`:{let t=e.thinking;if(!t||t.type===`disabled`)return e;if(n===void 0){if(t.type===`enabled`){let n={type:`enabled`,budgetTokens:t.budgetTokens};return $({...e,thinking:n})}return $({...e,thinking:{type:`adaptive`}})}let r=yd.safeParse(n);return!r.success||!r.data?e:t.type===`enabled`?$({...e,thinking:{type:`enabled`,budgetTokens:t.budgetTokens,display:r.data}}):$({...e,thinking:{type:`adaptive`,display:r.data}})}case`effort`:{if(n===void 0){let t={...e};return delete t.effort,$(t)}let t=bd.safeParse(n);return!t.success||!t.data?e:$({...e,effort:t.data})}case`extraBody`:{if(n===void 0){let t={...e};return delete t.extraBody,$(t)}let t=Vd(n);return t===void 0?e:$({...e,extraBody:t})}default:return e}}function Vd(e){if(typeof e==`object`&&e&&!Array.isArray(e))return e}var Hd={getDefaultConfig:Dd,getVisibleSpecs:Od,parseConfig:Ad,normalize:$,validateForSubmit:jd,toPromptInput:Nd,fromPromptInvocationParameters:Pd,fromPromptInvocationParametersForDisplay:Fd,fromSpanInvocationParameters:Rd,readField:zd,writeField:Bd};function Ud(e){return Xn(e)&&!Array.isArray(e)}function Wd({str:e,excludePrimitives:t=!1,excludeArray:n=!1,excludeNull:r=!1}){try{let i=JSON.parse(e);if(t&&typeof i!=`object`||n&&Array.isArray(i)||r&&i===null)return!1}catch{return!1}return!0}function Gd(e){return Wd({str:e,excludeArray:!0,excludePrimitives:!0})}function Kd(e){try{return{json:JSON.parse(e)}}catch(e){return{json:null,parseError:e}}}function qd(...e){try{return{json:JSON.stringify(...e)}}catch(e){return{json:null,stringifyError:e}}}function Jd({obj:e,parentKey:t=``,separator:n=`.`,keepNonTerminalValues:r=!1,formatIndices:i=!1}){let a={};for(let[o,s]of Object.entries(e)){let c;c=i&&Array.isArray(e)?t?`${t}[${o}]`:`[${o}]`:t?`${t}${n}${o}`:o,s&&typeof s==`object`?(r&&(a[c]=s),Object.assign(a,Jd({obj:s,parentKey:c,separator:n,keepNonTerminalValues:r,formatIndices:i}))):a[c]=s}return a}function Yd(e,t=`.`){try{let n=JSON.parse(e);return typeof n==`object`?Jd({obj:n,separator:t}):{}}catch{}return{}}function Xd(e,t){let n=t?.unquotePlainString??!1;if(typeof e==`string`){let t=e.startsWith(`"{`)||e.startsWith(`"[`)||e.startsWith(`"\\"`);try{if(t){let t=JSON.parse(e),n=typeof t==`string`?JSON.parse(t):t;return JSON.stringify(n,null,2)}}catch{}return n?e:JSON.stringify(e)}try{let t=JSON.stringify(e,null,2);if(t!==void 0)return t}catch{}return String(e)}function Zd(e){if(e!=null)try{return JSON.stringify(e)}catch{return}}function Qd(e){if(e.trim())try{return JSON.parse(e)}catch{return}}function $d(e){let t=Qd(e);if(!(typeof t!=`object`||!t))return t}function ef(e){if(e==null)return``;if(Array.isArray(e))return e.length>0?e.map(ef):[];if(typeof e==`object`){let t={};for(let n in e)t[n]=ef(e[n]);return t}return typeof e==`string`?``:typeof e==`number`||typeof e==`boolean`?e:``}function tf(e){try{let t=ef(JSON.parse(e));return JSON.stringify(t,null,2)}catch{return`{
  
}`}}function nf(e){if(!Xn(e))return{value:e,wasUnnested:!1};let t=Object.keys(e);if(t.length!==1)return{value:e,wasUnnested:!1};let n=e[t[0]];return typeof n==`string`?{value:n,wasUnnested:!0}:{value:e,wasUnnested:!1}}function rf(){return{maxTokens:1024,temperature:1}}function af(){return md}var of=Hn({maxTokens:J().optional().catch(void 0),temperature:J().optional().catch(void 0),topP:J().optional().catch(void 0),stopSequences:Nn(Y()).optional().catch(void 0)});function sf(e){let t=of.safeParse(e),n=t.success?t.data:{},r={};return n.maxTokens!==void 0&&(r.maxTokens=n.maxTokens),n.temperature!==void 0&&(r.temperature=n.temperature),n.topP!==void 0&&(r.topP=n.topP),n.stopSequences!==void 0&&(r.stopSequences=[...n.stopSequences]),r}function cf(e){return e}function lf(e){return[]}function uf(e){let t=cf(e),n={};return t.maxTokens!==void 0&&(n.maxTokens=t.maxTokens),t.temperature!==void 0&&(n.temperature=t.temperature),t.topP!==void 0&&(n.topP=t.topP),t.stopSequences!==void 0&&(n.stopSequences=t.stopSequences),{aws:n}}function df(e){if(e.__typename!==`PromptAwsInvocationParameters`)throw Error(`awsAdapter.fromPromptInvocationParameters called with non-AWS typename: ${e.__typename}`);let t={};return e.awsMaxTokens!=null&&(t.maxTokens=e.awsMaxTokens),e.temperature!=null&&(t.temperature=e.temperature),e.topP!=null&&(t.topP=e.topP),e.stopSequences!=null&&(t.stopSequences=[...e.stopSequences]),cf(t)}function ff(e){if(e.__typename!==`PromptAwsInvocationParameters`)throw Error(`awsAdapter.fromPromptInvocationParametersForDisplay called with non-AWS typename: ${e.__typename}`);let t={};return e.awsMaxTokens!=null&&(t.maxTokens=e.awsMaxTokens),e.temperature!=null&&(t.temperature=e.temperature),e.topP!=null&&(t.topP=e.topP),e.stopSequences!=null&&(t.stopSequences=[...e.stopSequences]),t}var pf=In({maxTokens:J().optional().catch(void 0),temperature:J().optional().catch(void 0),topP:J().optional().catch(void 0),stopSequences:Nn(Y()).optional().catch(void 0)}).optional().catch(void 0),mf=In({textFormat:In({structure:In({jsonSchema:In({schema:Rn([Y(),Pn(Y(),Bn())]).optional(),name:Y().optional(),description:Y().optional()}).optional().catch(void 0)}).optional().catch(void 0)}).optional().catch(void 0)}).optional().catch(void 0),hf=Hn({maxTokens:J().optional().catch(void 0),temperature:J().optional().catch(void 0),topP:J().optional().catch(void 0),stopSequences:Nn(Y()).optional().catch(void 0),inferenceConfig:pf,outputConfig:mf});function gf(e){let t=hf.safeParse(e),n=t.success?t.data:{},r={};n.maxTokens===void 0?n.inferenceConfig?.maxTokens!==void 0&&(r.maxTokens=n.inferenceConfig.maxTokens):r.maxTokens=n.maxTokens,n.temperature===void 0?n.inferenceConfig?.temperature!==void 0&&(r.temperature=n.inferenceConfig.temperature):r.temperature=n.temperature,n.topP===void 0?n.inferenceConfig?.topP!==void 0&&(r.topP=n.inferenceConfig.topP):r.topP=n.topP,n.stopSequences===void 0?n.inferenceConfig?.stopSequences!==void 0&&(r.stopSequences=[...n.inferenceConfig.stopSequences]):r.stopSequences=[...n.stopSequences];let i={},a=n.outputConfig?.textFormat?.structure?.jsonSchema;if(a?.schema!=null){let e=null;if(typeof a.schema==`string`){let{json:t}=Kd(a.schema);typeof t==`object`&&t&&!Array.isArray(t)&&(e=t)}else typeof a.schema==`object`&&!Array.isArray(a.schema)&&(e=a.schema);if(e!=null){let t={name:typeof a.name==`string`?a.name:`response`,schema:e};typeof a.description==`string`&&(t.description=a.description),i.responseFormat={type:`json_schema`,jsonSchema:t}}}return{config:cf(r),promoted:i}}function _f(e,t){switch(t){case`maxTokens`:return e.maxTokens;case`temperature`:return e.temperature;case`topP`:return e.topP;case`stopSequences`:return e.stopSequences;default:return}}function vf(e,t,n){switch(t){case`maxTokens`:case`temperature`:case`topP`:if(n===void 0){let n={...e};return delete n[t],cf(n)}return typeof n!=`number`||Number.isNaN(n)?e:cf({...e,[t]:n});case`stopSequences`:if(n===void 0){let t={...e};return delete t.stopSequences,cf(t)}return Array.isArray(n)?cf({...e,stopSequences:n.map(String)}):e;default:return e}}var yf={getDefaultConfig:rf,getVisibleSpecs:af,parseConfig:sf,normalize:cf,validateForSubmit:lf,toPromptInput:uf,fromPromptInvocationParameters:df,fromPromptInvocationParametersForDisplay:ff,fromSpanInvocationParameters:e=>gf(e),readField:_f,writeField:vf};function bf(){return{temperature:1,presencePenalty:0,frequencyPenalty:0,thinkingConfig:{thinkingLevel:`MEDIUM`,includeThoughts:!0}}}function xf(){return pd}var Sf=Y().transform(e=>e.toUpperCase()).pipe(Fn(cd)).optional().catch(void 0),Cf=Hn({thinkingBudget:J().optional().catch(void 0),thinkingLevel:Sf,includeThoughts:Un().optional().catch(void 0)}).optional().catch(void 0),wf=Hn({temperature:J().optional().catch(void 0),maxOutputTokens:J().optional().catch(void 0),stopSequences:Nn(Y()).optional().catch(void 0),presencePenalty:J().optional().catch(void 0),frequencyPenalty:J().optional().catch(void 0),topP:J().optional().catch(void 0),topK:J().optional().catch(void 0),thinkingConfig:Cf});function Tf(e){let t=wf.safeParse(e),n=t.success?t.data:{},r={};return n.temperature!==void 0&&(r.temperature=n.temperature),n.maxOutputTokens!==void 0&&(r.maxOutputTokens=n.maxOutputTokens),n.stopSequences!==void 0&&(r.stopSequences=[...n.stopSequences]),n.presencePenalty!==void 0&&(r.presencePenalty=n.presencePenalty),n.frequencyPenalty!==void 0&&(r.frequencyPenalty=n.frequencyPenalty),n.topP!==void 0&&(r.topP=n.topP),n.topK!==void 0&&(r.topK=n.topK),n.thinkingConfig!==void 0&&n.thinkingConfig!==null&&(r.thinkingConfig=Ef(n.thinkingConfig)),r}function Ef(e){let t={};return e.thinkingBudget!==void 0&&(t.thinkingBudget=e.thinkingBudget),e.thinkingLevel!==void 0&&(t.thinkingLevel=e.thinkingLevel),e.includeThoughts!==void 0&&(t.includeThoughts=e.includeThoughts),t}function Df(e){return e}function Of(e){return[]}function kf(e){let t={};return e.thinkingBudget!==void 0&&(t.thinkingBudget=e.thinkingBudget),e.thinkingLevel!==void 0&&(t.thinkingLevel=e.thinkingLevel),e.includeThoughts!==void 0&&(t.includeThoughts=e.includeThoughts),Object.keys(t).length>0?t:void 0}function Af(e){let t=Df(e),n={};if(t.temperature!==void 0&&(n.temperature=t.temperature),t.maxOutputTokens!==void 0&&(n.maxOutputTokens=t.maxOutputTokens),t.stopSequences!==void 0&&(n.stopSequences=t.stopSequences),t.presencePenalty!==void 0&&(n.presencePenalty=t.presencePenalty),t.frequencyPenalty!==void 0&&(n.frequencyPenalty=t.frequencyPenalty),t.topP!==void 0&&(n.topP=t.topP),t.topK!==void 0&&(n.topK=t.topK),t.thinkingConfig!==void 0){let e=kf(t.thinkingConfig);e&&(n.thinkingConfig=e)}return{google:n}}function jf(e){if(e.__typename!==`PromptGoogleInvocationParameters`)throw Error(`googleAdapter.fromPromptInvocationParameters called with non-Google typename: ${e.__typename}`);let t={};if(e.temperature!=null&&(t.temperature=e.temperature),e.maxOutputTokens!=null&&(t.maxOutputTokens=e.maxOutputTokens),e.stopSequences!=null&&(t.stopSequences=[...e.stopSequences]),e.presencePenalty!=null&&(t.presencePenalty=e.presencePenalty),e.frequencyPenalty!=null&&(t.frequencyPenalty=e.frequencyPenalty),e.topP!=null&&(t.topP=e.topP),e.topK!=null&&(t.topK=e.topK),e.thinkingConfig){let n={};e.thinkingConfig.thinkingBudget!=null&&(n.thinkingBudget=e.thinkingConfig.thinkingBudget),e.thinkingConfig.thinkingLevel!=null&&(n.thinkingLevel=e.thinkingConfig.thinkingLevel),e.thinkingConfig.includeThoughts!=null&&(n.includeThoughts=e.thinkingConfig.includeThoughts),Object.keys(n).length>0&&(t.thinkingConfig=n)}return Df(t)}function Mf(e){if(e.__typename!==`PromptGoogleInvocationParameters`)throw Error(`googleAdapter.fromPromptInvocationParametersForDisplay called with non-Google typename: ${e.__typename}`);let t={};if(e.temperature!=null&&(t.temperature=e.temperature),e.maxOutputTokens!=null&&(t.maxOutputTokens=e.maxOutputTokens),e.stopSequences!=null&&(t.stopSequences=[...e.stopSequences]),e.presencePenalty!=null&&(t.presencePenalty=e.presencePenalty),e.frequencyPenalty!=null&&(t.frequencyPenalty=e.frequencyPenalty),e.topP!=null&&(t.topP=e.topP),e.topK!=null&&(t.topK=e.topK),e.thinkingConfig){let n={};e.thinkingConfig.thinkingBudget!=null&&(n.thinkingBudget=e.thinkingConfig.thinkingBudget),e.thinkingConfig.thinkingLevel!=null&&(n.thinkingLevel=e.thinkingConfig.thinkingLevel),e.thinkingConfig.includeThoughts!=null&&(n.includeThoughts=e.thinkingConfig.includeThoughts),Object.keys(n).length>0&&(t.thinkingConfig=n)}return t}var Nf=Hn({thinking_budget:J().optional().catch(void 0),thinking_level:Sf,include_thoughts:Un().optional().catch(void 0)}).optional().catch(void 0),Pf=Hn({temperature:J().optional().catch(void 0),max_output_tokens:J().optional().catch(void 0),stop_sequences:Nn(Y()).optional().catch(void 0),presence_penalty:J().optional().catch(void 0),frequency_penalty:J().optional().catch(void 0),top_p:J().optional().catch(void 0),top_k:J().optional().catch(void 0),thinking_config:Nf,response_json_schema:Bn().optional(),response_schema:Bn().optional(),response_mime_type:Y().optional().catch(void 0)});function Ff(e){let t=Pf.safeParse(e),n=t.success?t.data:{},r={};if(n.temperature!==void 0&&(r.temperature=n.temperature),n.max_output_tokens!==void 0&&(r.maxOutputTokens=n.max_output_tokens),n.stop_sequences!==void 0&&(r.stopSequences=[...n.stop_sequences]),n.presence_penalty!==void 0&&(r.presencePenalty=n.presence_penalty),n.frequency_penalty!==void 0&&(r.frequencyPenalty=n.frequency_penalty),n.top_p!==void 0&&(r.topP=n.top_p),n.top_k!==void 0&&(r.topK=n.top_k),n.thinking_config){let e={};n.thinking_config.thinking_budget!==void 0&&(e.thinkingBudget=n.thinking_config.thinking_budget),n.thinking_config.thinking_level!==void 0&&(e.thinkingLevel=n.thinking_config.thinking_level),n.thinking_config.include_thoughts!==void 0&&(e.includeThoughts=n.thinking_config.include_thoughts),Object.keys(e).length>0&&(r.thinkingConfig=e)}let i={},a=n.response_json_schema??n.response_schema;return a!=null&&n.response_mime_type===`application/json`&&(i.responseFormat={type:`json_schema`,jsonSchema:{name:`response`,schema:a}}),{config:Df(r),promoted:i}}var If=new Set([`temperature`,`maxOutputTokens`,`presencePenalty`,`frequencyPenalty`,`topP`,`topK`]);function Lf(e){return If.has(e)}function Rf(e){let t={};return e.thinkingBudget!==void 0&&(t.thinkingBudget=e.thinkingBudget),e.thinkingLevel!==void 0&&(t.thinkingLevel=e.thinkingLevel),e.includeThoughts!==void 0&&(t.includeThoughts=e.includeThoughts),Object.keys(t).length===0?void 0:t}function zf(e,t){if(Lf(t))return e[t];switch(t){case`stopSequences`:return e.stopSequences;case`thinkingBudget`:return e.thinkingConfig?.thinkingBudget;case`thinkingLevel`:return e.thinkingConfig?.thinkingLevel?.toLowerCase();case`includeThoughts`:return e.thinkingConfig?.includeThoughts;default:return}}function Bf(e,t,n){if(Lf(t)){if(n===void 0){let n={...e};return delete n[t],Df(n)}return typeof n!=`number`||Number.isNaN(n)?e:Df({...e,[t]:n})}switch(t){case`stopSequences`:if(n===void 0){let t={...e};return delete t.stopSequences,Df(t)}return Array.isArray(n)?Df({...e,stopSequences:n.map(String)}):e;case`thinkingBudget`:{let t={...e.thinkingConfig??{}};if(n===void 0)delete t.thinkingBudget;else if(typeof n==`number`&&!Number.isNaN(n))t.thinkingBudget=n;else return e;return Vf(e,t)}case`thinkingLevel`:{let t={...e.thinkingConfig??{}};if(n===void 0)delete t.thinkingLevel;else{let r=Sf.safeParse(n);if(!r.success||!r.data)return e;t.thinkingLevel=r.data}return Vf(e,t)}case`includeThoughts`:{let t={...e.thinkingConfig??{}};if(n===void 0)delete t.includeThoughts;else if(typeof n==`boolean`)t.includeThoughts=n;else return e;return Vf(e,t)}default:return e}}function Vf(e,t){let n=Rf(t),r={...e};return n===void 0?delete r.thinkingConfig:r.thinkingConfig=n,Df(r)}var Hf={getDefaultConfig:bf,getVisibleSpecs:xf,parseConfig:Tf,normalize:Df,validateForSubmit:Of,toPromptInput:Af,fromPromptInvocationParameters:jf,fromPromptInvocationParametersForDisplay:Mf,fromSpanInvocationParameters:e=>Ff(e),readField:zf,writeField:Bf};function Uf(e){if(typeof e==`object`&&e&&!Array.isArray(e))return e}function Wf(e){return e===0?void 0:e}function Gf(){return{frequencyPenalty:0,presencePenalty:0}}function Kf(e,t){let n=t.openaiApiType??`RESPONSES`;return dd.filter(e=>{let t=`applicableOpenAIApiTypes`in e?e.applicableOpenAIApiTypes:void 0;return t==null||t.includes(n)})}var qf=Hn({temperature:J().optional().catch(void 0),topP:J().optional().catch(void 0),maxCompletionTokens:J().optional().catch(void 0),frequencyPenalty:J().optional().catch(void 0),presencePenalty:J().optional().catch(void 0),reasoningEffort:Y().optional().catch(void 0),seed:J().optional().catch(void 0),stop:Nn(Y()).optional().catch(void 0),extraBody:Pn(Y(),Bn()).optional().catch(void 0)});function Jf(e){let t=qf.safeParse(e),n=t.success?t.data:{},r={};if(n.temperature!==void 0&&(r.temperature=n.temperature),n.topP!==void 0&&(r.topP=n.topP),n.maxCompletionTokens!==void 0&&(r.maxCompletionTokens=n.maxCompletionTokens),n.frequencyPenalty!==void 0&&(r.frequencyPenalty=n.frequencyPenalty),n.presencePenalty!==void 0&&(r.presencePenalty=n.presencePenalty),n.reasoningEffort!==void 0){let e=nd(n.reasoningEffort);e!==void 0&&(r.reasoningEffort=e)}return n.seed!==void 0&&(r.seed=n.seed),n.stop!==void 0&&(r.stop=[...n.stop]),n.extraBody!==void 0&&(r.extraBody={...n.extraBody}),r}function Yf(e){return e}function Xf(e){return[]}function Zf(e){let t=Yf(e),n={};t.temperature!==void 0&&(n.temperature=t.temperature),t.topP!==void 0&&(n.topP=t.topP),t.maxCompletionTokens!==void 0&&(n.maxCompletionTokens=t.maxCompletionTokens);let r=Wf(t.frequencyPenalty);r!==void 0&&(n.frequencyPenalty=r);let i=Wf(t.presencePenalty);if(i!==void 0&&(n.presencePenalty=i),t.reasoningEffort!==void 0){let e=td(t.reasoningEffort);e!==void 0&&(n.reasoningEffort=e)}return t.seed!==void 0&&(n.seed=t.seed),t.stop!==void 0&&(n.stop=t.stop),t.extraBody!==void 0&&(n.extraBody=t.extraBody),{openai:n}}function Qf(e){if(e.__typename!==`PromptOpenAIInvocationParameters`)throw Error(`openaiAdapter.fromPromptInvocationParameters called with non-OpenAI typename: ${e.__typename}`);let t={};if(e.temperature!=null&&(t.temperature=e.temperature),e.topP!=null&&(t.topP=e.topP),e.maxCompletionTokens==null?e.openaiMaxTokens!=null&&(t.maxCompletionTokens=e.openaiMaxTokens):t.maxCompletionTokens=e.maxCompletionTokens,e.frequencyPenalty!=null&&(t.frequencyPenalty=e.frequencyPenalty),e.presencePenalty!=null&&(t.presencePenalty=e.presencePenalty),e.seed!=null&&(t.seed=e.seed),e.stop!=null&&(t.stop=[...e.stop]),e.reasoningEffort!=null){let n=nd(e.reasoningEffort);n!==void 0&&(t.reasoningEffort=n)}let n=Uf(e.extraBody);return n!=null&&(t.extraBody=n),Yf(t)}function $f(e){if(e.__typename!==`PromptOpenAIInvocationParameters`)throw Error(`openaiAdapter.fromPromptInvocationParametersForDisplay called with non-OpenAI typename: ${e.__typename}`);let t={};e.temperature!=null&&(t.temperature=e.temperature),e.openaiMaxTokens!=null&&(t.maxTokens=e.openaiMaxTokens),e.maxCompletionTokens!=null&&(t.maxCompletionTokens=e.maxCompletionTokens),e.frequencyPenalty!=null&&(t.frequencyPenalty=e.frequencyPenalty),e.presencePenalty!=null&&(t.presencePenalty=e.presencePenalty),e.topP!=null&&(t.topP=e.topP),e.seed!=null&&(t.seed=e.seed),e.stop!=null&&(t.stop=[...e.stop]);let n=nd(e.reasoningEffort);n!==void 0&&(t.reasoningEffort=n);let r=Uf(e.extraBody);return r!=null&&(t.extraBody=r),t}var ep=In({name:Y().optional(),schema:Bn().optional(),strict:Un().nullish(),description:Y().nullish()}),tp=In({type:Y().optional(),json_schema:ep.optional()}).optional().catch(void 0),np=In({type:Y().optional(),name:Y().optional(),schema:Bn().optional(),strict:Un().optional(),description:Y().optional()}).optional().catch(void 0),rp=Hn({temperature:J().optional().catch(void 0),top_p:J().optional().catch(void 0),max_completion_tokens:J().optional().catch(void 0),max_tokens:J().optional().catch(void 0),max_output_tokens:J().optional().catch(void 0),frequency_penalty:J().optional().catch(void 0),presence_penalty:J().optional().catch(void 0),seed:J().optional().catch(void 0),stop:Nn(Y()).optional().catch(void 0),reasoning_effort:Y().optional().catch(void 0),reasoning:Hn({effort:Y().optional().catch(void 0)}).optional().catch(void 0),response_format:tp,text:In({format:np}).optional().catch(void 0),extra_body:Pn(Y(),Bn()).optional().catch(void 0)});function ip(e,t){let n=rp.safeParse(e),r=n.success?n.data:{},i={};r.temperature!==void 0&&(i.temperature=r.temperature),r.top_p!==void 0&&(i.topP=r.top_p),r.max_completion_tokens===void 0?r.max_tokens===void 0?t===`RESPONSES`&&r.max_output_tokens!==void 0&&(i.maxCompletionTokens=r.max_output_tokens):i.maxCompletionTokens=r.max_tokens:i.maxCompletionTokens=r.max_completion_tokens,r.frequency_penalty!==void 0&&(i.frequencyPenalty=r.frequency_penalty),r.presence_penalty!==void 0&&(i.presencePenalty=r.presence_penalty),r.seed!==void 0&&(i.seed=r.seed),r.stop!==void 0&&(i.stop=[...r.stop]);let a;if(r.reasoning_effort===void 0?t===`RESPONSES`&&r.reasoning?.effort!==void 0&&(a=r.reasoning.effort):a=r.reasoning_effort,a!==void 0){let e=nd(a);e!==void 0&&(i.reasoningEffort=e)}r.extra_body!==void 0&&(i.extraBody={...r.extra_body});let o={},s=r.response_format;if(s?.json_schema){let e=s.json_schema,t={name:typeof e.name==`string`?e.name:`response`};e.schema!==void 0&&(t.schema=e.schema),e.strict!==void 0&&e.strict!==null&&(t.strict=e.strict),e.description!==void 0&&e.description!==null&&(t.description=e.description),o.responseFormat={type:`json_schema`,jsonSchema:t}}else if(r.text?.format!==void 0){let e=r.text.format;if(e){let t={name:typeof e.name==`string`?e.name:`response`};e.schema!==void 0&&(t.schema=e.schema),e.strict!==void 0&&(t.strict=e.strict),e.description!==void 0&&(t.description=e.description),o.responseFormat={type:`json_schema`,jsonSchema:t}}}return{config:Yf(i),promoted:o}}var ap=new Set([`temperature`,`topP`,`maxCompletionTokens`,`frequencyPenalty`,`presencePenalty`,`seed`]);function op(e){return ap.has(e)}function sp(e,t){if(op(t))return e[t];switch(t){case`reasoningEffort`:return e.reasoningEffort;case`stop`:return e.stop;case`extraBody`:return e.extraBody;default:return}}function cp(e,t,n){if(op(t)){if(n===void 0){let n={...e};return delete n[t],Yf(n)}return typeof n!=`number`||Number.isNaN(n)?e:Yf({...e,[t]:n})}switch(t){case`reasoningEffort`:if(n===void 0){let t={...e};return delete t.reasoningEffort,Yf(t)}return typeof n==`string`?Yf({...e,reasoningEffort:n}):e;case`stop`:if(n===void 0){let t={...e};return delete t.stop,Yf(t)}return Array.isArray(n)?Yf({...e,stop:n.map(String)}):e;case`extraBody`:{if(n===void 0){let t={...e};return delete t.extraBody,Yf(t)}let t=Uf(n);return t===void 0?e:Yf({...e,extraBody:t})}default:return e}}var lp={getDefaultConfig:Gf,getVisibleSpecs:Kf,parseConfig:Jf,normalize:Yf,validateForSubmit:Xf,toPromptInput:Zf,fromPromptInvocationParameters:Qf,fromPromptInvocationParametersForDisplay:$f,fromSpanInvocationParameters:(e,t)=>ip(e,t?.openaiApiType??null),readField:sp,writeField:cp};function up(e){switch(e){case Q.OPENAI:return lp;case Q.ANTHROPIC:return Hd;case Q.GOOGLE_GENAI:return Hf;case Q.AWS_BEDROCK:return yf;default:return Wn(e)}}function dp(e){return up(ud(e))}function fp(e){let t=dp(e);return t.normalize(t.getDefaultConfig())}function pp(e,t){let n=dp(e);return n.normalize(n.parseConfig(t))}function mp(e,t){return dp(e).toPromptInput(t)}function hp(e,t){if(t==null)return fp(e);let n=ud(e);return n===Q.OPENAI&&t.__typename===`PromptOpenAIInvocationParameters`||n===Q.ANTHROPIC&&t.__typename===`PromptAnthropicInvocationParameters`||n===Q.GOOGLE_GENAI&&t.__typename===`PromptGoogleInvocationParameters`||n===Q.AWS_BEDROCK&&t.__typename===`PromptAwsInvocationParameters`?dp(e).fromPromptInvocationParameters(t):fp(e)}function gp(e){if(e==null)return null;let t;switch(e.__typename){case`PromptOpenAIInvocationParameters`:t=Q.OPENAI;break;case`PromptAnthropicInvocationParameters`:t=Q.ANTHROPIC;break;case`PromptGoogleInvocationParameters`:t=Q.GOOGLE_GENAI;break;case`PromptAwsInvocationParameters`:t=Q.AWS_BEDROCK;break;case`%other`:throw Error(`Unsupported prompt invocation parameters typename: %other`);default:return Wn(e)}let n=up(t);return{family:t,parameters:n.fromPromptInvocationParametersForDisplay(e)}}function _p(e,t,n={}){let{config:r,promoted:i}=dp(e).fromSpanInvocationParameters(t,n);return{invocationParameters:r,responseFormat:i.responseFormat}}function vp(e,t,n){return dp(e).readField(t,n)}function yp(e,t){return dp(e.provider).getVisibleSpecs(t,{openaiApiType:e.openaiApiType})}function bp(e,t,n,r){return dp(e).writeField(t,n,r)}function xp(){if(typeof crypto<`u`&&typeof crypto.randomUUID==`function`)return crypto.randomUUID();let e=new Uint8Array(16);crypto.getRandomValues(e),e[6]=e[6]&15|64,e[8]=e[8]&63|128;let t=Array.from(e).map(e=>e.toString(16).padStart(2,`0`)).join(``);return`${t.slice(0,8)}-${t.slice(8,12)}-${t.slice(12,16)}-${t.slice(16,20)}-${t.slice(20)}`}var Sp={provider:`ANTHROPIC`,modelName:`claude-opus-4-6`,invocationParameters:fp(`ANTHROPIC`)},Cp={collectorEndpoint:null,assistantProjectName:`assistant_agent`,forceTracing:!1,webAccessEnabled:!1,assistantEnabled:!1,allowLocalTraces:!1,allowRemoteExport:!1},wp={storeLocalTraces:!0,exportRemoteTraces:!1,attachUserId:!1,acknowledgedTraceConsent:null},Tp={edits:`manual`},Ep=`(branch) `,Dp=50;function Op(e){let t=e.shortSummary.trim();if(!t){let n=e.messages.find(e=>e.role===`user`)?.parts.filter(Vn).map(e=>e.text).join(` `).trim();t=n?n.length>Dp?`${n.slice(0,Dp)}...`:n:``}return t.startsWith(Ep)?t:t?`${Ep}${t}`:Ep.trim()}function kp(e){return{allowLocalTraces:e.allowLocalTraces,allowRemoteExport:!!e.collectorEndpoint&&e.allowRemoteExport}}function Ap({agentsConfig:e,observability:t}){if(e.forceTracing)return!0;let n=t.acknowledgedTraceConsent;if(!n)return!1;let r=kp(e);return(!r.allowLocalTraces||n.allowLocalTraces)&&(!r.allowRemoteExport||n.allowRemoteExport)}function jp({agentsConfig:e,observability:t}){if(e.forceTracing)return{ingestTraces:!0,exportRemoteTraces:!0};let n=kp(e);return{ingestTraces:n.allowLocalTraces&&t.storeLocalTraces,exportRemoteTraces:n.allowRemoteExport&&t.exportRemoteTraces}}function Mp({agentsConfig:e,observability:t}){return e.forceTracing||t.attachUserId}function Np({capabilities:e,defaultCapabilities:t=qu()}){if(!e||typeof e!=`object`)return{...t};let n=e;return Object.fromEntries(Object.keys(t).map(e=>{let r=n[e];return[e,typeof r==`boolean`?r:t[e]]}))}function Pp(e,t){if(!e||typeof e!=`object`)return t;let n=e;return{...t,...n,observability:{...t.observability,...n.observability},capabilities:Np({capabilities:n.capabilities,defaultCapabilities:t.capabilities})}}function Fp({record:e,retainedSessionIds:t}){return Object.fromEntries(Object.entries(e).filter(([e])=>t.has(e)))}function Ip({record:e,retainedSessionIds:t}){return Object.fromEntries(Object.entries(e).filter(([,e])=>e!=null&&t.has(e.sessionId)))}function Lp(e,t){return Object.fromEntries(Object.entries(e).filter(([,e])=>e?.sessionId!==t))}function Rp({state:e,retainedSessionIds:t,activeSessionId:n}){let r=new Set(t);return{sessions:t,activeSessionId:n,sessionMap:Fp({record:e.sessionMap,retainedSessionIds:r}),pendingElicitationBySessionId:Fp({record:e.pendingElicitationBySessionId,retainedSessionIds:r}),chatStatusBySessionId:Fp({record:e.chatStatusBySessionId,retainedSessionIds:r}),isResponsePendingBySessionId:Fp({record:e.isResponsePendingBySessionId,retainedSessionIds:r}),draftInputBySessionId:Fp({record:e.draftInputBySessionId,retainedSessionIds:r}),pendingMessageBySessionId:Fp({record:e.pendingMessageBySessionId,retainedSessionIds:r}),pendingPatchExperimentsByToolCallId:Ip({record:e.pendingPatchExperimentsByToolCallId,retainedSessionIds:r})}}var zp=`arize-phoenix-assistant`;function Bp(){let e=(window.Config?.basename??``).replace(/\/+$/,``);return e?`${zp}:${e}`:zp}var Vp=e=>p()(D(a((t,n)=>({isOpen:!1,position:`pinned`,fabMode:`pinned`,fabPlacement:`bottom-end`,sessions:[],activeSessionId:null,sessionMap:{},defaultModelConfig:{...Sp},agentsConfig:Cp,observability:wp,permissions:Tp,capabilities:qu(),routeContexts:[],mountedContexts:{},pendingPromptEditsByToolCallId:{},pendingPromptInstanceRemovalsByToolCallId:{},pendingBatchSpanAnnotatesByToolCallId:{},pendingDatasetWritesByToolCallId:{},pendingAnnotationConfigWritesByToolCallId:{},pendingPatchExperimentsByToolCallId:{},pendingPromptToolWritesByToolCallId:{},pendingSavePromptsByToolCallId:{},pendingCodeEvaluatorEditsByToolCallId:{},pendingLlmEvaluatorEditsByToolCallId:{},pendingLoadDatasetsByToolCallId:{},setIsOpen:e=>{t({isOpen:e},!1,{type:`setIsOpen`})},toggleOpen:()=>{t(e=>({isOpen:!e.isOpen}),!1,{type:`toggleOpen`})},setPosition:e=>{t({position:e},!1,{type:`setPosition`})},setFabMode:e=>{t({fabMode:e},!1,{type:`setFabMode`})},setFabPlacement:e=>{t({fabPlacement:e},!1,{type:`setFabPlacement`})},createSession:()=>{let e=xp();return t(t=>{let n={id:e,shortSummary:``,messages:[],context:[],modelConfig:{...t.defaultModelConfig},createdAt:Date.now()},r;return r=t.capabilities[`session.storeSessions`]?[...t.sessions,e].slice(-3):[e],{...Rp({state:{...t,sessionMap:{...t.sessionMap,[e]:n}},retainedSessionIds:r,activeSessionId:e})}},!1,{type:`createSession`}),e},forkSession:({sourceSessionId:e,messages:n,restoredInput:r})=>{let i=xp(),a=!1;return t(t=>{let o=t.sessionMap[e];if(!o)return t;a=!0;let s={id:i,shortSummary:Op(o),messages:n,context:[...o.context],modelConfig:{...o.modelConfig},createdAt:Date.now()},c=[...t.sessions,i].slice(-3),l=r?{...t.draftInputBySessionId,[i]:r}:t.draftInputBySessionId;return{...Rp({state:{...t,sessionMap:{...t.sessionMap,[i]:s},draftInputBySessionId:l},retainedSessionIds:c,activeSessionId:i})}},!1,{type:`forkSession`}),a?i:null},deleteSession:e=>{t(t=>{if(!t.sessionMap[e])return t;let n={...t.sessionMap};delete n[e];let r={...t.pendingElicitationBySessionId};delete r[e];let i={...t.chatStatusBySessionId};delete i[e];let a={...t.isResponsePendingBySessionId};delete a[e];let o={...t.draftInputBySessionId};delete o[e];let s={...t.pendingMessageBySessionId};delete s[e];let c=Lp(t.pendingPatchExperimentsByToolCallId,e),l=t.sessions.filter(t=>t!==e);return{sessions:l,sessionMap:n,activeSessionId:t.activeSessionId===e?l[l.length-1]??null:t.activeSessionId,pendingElicitationBySessionId:r,chatStatusBySessionId:i,isResponsePendingBySessionId:a,draftInputBySessionId:o,pendingMessageBySessionId:s,pendingPatchExperimentsByToolCallId:c}},!1,{type:`deleteSession`})},setActiveSession:e=>{t({activeSessionId:e},!1,{type:`setActiveSession`})},updateSessionSummary:(e,n)=>{t(t=>{let r=t.sessionMap[e];return r?{sessionMap:{...t.sessionMap,[e]:{...r,shortSummary:n}}}:t},!1,{type:`updateSessionSummary`})},updateSessionModelConfig:(e,n)=>{t(t=>{let r=t.sessionMap[e];return r?{sessionMap:{...t.sessionMap,[e]:{...r,modelConfig:{...r.modelConfig,...n}}}}:t},!1,{type:`updateSessionModelConfig`})},addSessionContext:(e,n)=>{t(t=>{let r=t.sessionMap[e];return r?{sessionMap:{...t.sessionMap,[e]:{...r,context:[...r.context,n]}}}:t},!1,{type:`addSessionContext`})},removeSessionContext:(e,n)=>{t(t=>{let r=t.sessionMap[e];return r?{sessionMap:{...t.sessionMap,[e]:{...r,context:r.context.filter(e=>e!==n)}}}:t},!1,{type:`removeSessionContext`})},setSessionMessages:(e,n)=>{t(t=>{let r=t.sessionMap[e];return r?{sessionMap:{...t.sessionMap,[e]:{...r,messages:n}}}:t},!1,{type:`setSessionMessages`})},setDefaultModelConfig:e=>{t({defaultModelConfig:e},!1,{type:`setDefaultModelConfig`})},setObservability:e=>{t(t=>({observability:{...t.observability,...e}}),!1,{type:`setObservability`})},setPermissions:e=>{t(t=>({permissions:{...t.permissions,...e}}),!1,{type:`setPermissions`})},setAgentsConfig:e=>{t(t=>({agentsConfig:{...t.agentsConfig,...e}}),!1,{type:`setAgentsConfig`})},acknowledgeConsent:()=>{t(e=>({observability:{...e.observability,acknowledgedTraceConsent:kp(e.agentsConfig)}}),!1,{type:`acknowledgeConsent`})},clearAllSessions:()=>{t({sessions:[],activeSessionId:null,sessionMap:{},pendingElicitationBySessionId:{},chatStatusBySessionId:{},isResponsePendingBySessionId:{},draftInputBySessionId:{},pendingMessageBySessionId:{},pendingPatchExperimentsByToolCallId:{}},!1,{type:`clearAllSessions`})},setCapability:({key:e,enabled:n})=>{t(t=>{let r={...t.capabilities,[e]:n};return e!==`session.storeSessions`||n?{capabilities:r}:{capabilities:r,...Rp({state:t,retainedSessionIds:t.activeSessionId?[t.activeSessionId]:[],activeSessionId:t.activeSessionId})}},!1,{type:`setCapability`})},pendingElicitationBySessionId:{},setPendingElicitation:(e,n)=>{t(t=>{let r={...t.pendingElicitationBySessionId};return n?r[e]=n:delete r[e],{pendingElicitationBySessionId:r}},!1,{type:`setPendingElicitation`})},draftInputBySessionId:{},setDraftInput:(e,n)=>{t(t=>{let r={...t.draftInputBySessionId};return n?r[e]=n:delete r[e],{draftInputBySessionId:r}},!1,{type:`setDraftInput`})},pendingMessageBySessionId:{},setPendingMessage:(e,n)=>{t(t=>{let r={...t.pendingMessageBySessionId};return n?r[e]=n:delete r[e],{pendingMessageBySessionId:r}},!1,{type:`setPendingMessage`})},consumePendingMessage:e=>{let r=n().pendingMessageBySessionId[e]??null;return r!=null&&t(t=>{if(!(e in t.pendingMessageBySessionId))return t;let n={...t.pendingMessageBySessionId};return delete n[e],{pendingMessageBySessionId:n}},!1,{type:`consumePendingMessage`}),r},chatStatusBySessionId:{},setSessionChatStatus:(e,n)=>{t(t=>({chatStatusBySessionId:{...t.chatStatusBySessionId,[e]:n}}),!1,{type:`setSessionChatStatus`})},isResponsePendingBySessionId:{},setSessionResponsePending:(e,n)=>{t(t=>{if(!(e in t.sessionMap))return t;let r={...t.isResponsePendingBySessionId};return n?r[e]=!0:delete r[e],{isResponsePendingBySessionId:r}},!1,{type:`setSessionResponsePending`})},setSessionUsage:(e,n)=>{t(t=>{let r=t.sessionMap[e];if(!r)return t;let i=r.usage??{tokenCount:{total:0,completion:0,prompt:0}};return{sessionMap:{...t.sessionMap,[e]:{...r,usage:{...i,tokenCount:{prompt:n.prompt,completion:n.completion,total:n.total??n.prompt+n.completion,...n.promptDetails?{promptDetails:n.promptDetails}:{}}}}}}},!1,{type:`setSessionUsage`})},setRouteContexts:e=>{t(t=>{if(t.routeContexts.length===e.length){let n=!0;for(let r=0;r<e.length;r++)if(Uu(t.routeContexts[r])!==Uu(e[r])){n=!1;break}if(n)return t}return{routeContexts:e}},!1,{type:`setRouteContexts`})},setMountedContext:(e,n)=>{t(t=>({mountedContexts:{...t.mountedContexts,[e]:n}}),!1,{type:`setMountedContext`})},removeMountedContext:e=>{t(t=>{if(!(e in t.mountedContexts))return t;let n={...t.mountedContexts};return delete n[e],{mountedContexts:n}},!1,{type:`removeMountedContext`})},registeredClientActions:{},registerClientAction:(e,n)=>{t(t=>({registeredClientActions:{...t.registeredClientActions,[e]:n}}),!1,{type:`registerClientAction`})},unregisterClientAction:e=>{t(t=>{if(!(e in t.registeredClientActions))return t;let n={...t.registeredClientActions};return delete n[e],{registeredClientActions:n}},!1,{type:`unregisterClientAction`})},setPendingPromptEdit:(e,n)=>{t(t=>{let r={...t.pendingPromptEditsByToolCallId};return n?r[e]=n:delete r[e],{pendingPromptEditsByToolCallId:r}},!1,{type:`setPendingPromptEdit`})},setPendingPromptInstanceRemoval:(e,n)=>{t(t=>{let r={...t.pendingPromptInstanceRemovalsByToolCallId};return n?r[e]=n:delete r[e],{pendingPromptInstanceRemovalsByToolCallId:r}},!1,{type:`setPendingPromptInstanceRemoval`})},setPendingDatasetWrite:(e,n)=>{t(t=>{let r={...t.pendingDatasetWritesByToolCallId};return n?r[e]=n:delete r[e],{pendingDatasetWritesByToolCallId:r}},!1,{type:`setPendingDatasetWrite`})},setPendingAnnotationConfigWrite:(e,n)=>{t(t=>{let r={...t.pendingAnnotationConfigWritesByToolCallId};return n?r[e]=n:delete r[e],{pendingAnnotationConfigWritesByToolCallId:r}},!1,{type:`setPendingAnnotationConfigWrite`})},setPendingBatchSpanAnnotate:(e,n)=>{t(t=>{let r={...t.pendingBatchSpanAnnotatesByToolCallId};return n?r[e]=n:delete r[e],{pendingBatchSpanAnnotatesByToolCallId:r}},!1,{type:`setPendingBatchSpanAnnotate`})},setPendingPatchExperiment:(e,n)=>{t(t=>{let r={...t.pendingPatchExperimentsByToolCallId};return n?r[e]=n:delete r[e],{pendingPatchExperimentsByToolCallId:r}},!1,{type:`setPendingPatchExperiment`})},setPendingPromptToolWrite:(e,n)=>{t(t=>{let r={...t.pendingPromptToolWritesByToolCallId};return n?r[e]=n:delete r[e],{pendingPromptToolWritesByToolCallId:r}},!1,{type:`setPendingPromptToolWrite`})},setPendingSavePrompt:(e,n)=>{t(t=>{let r={...t.pendingSavePromptsByToolCallId};return n?r[e]=n:delete r[e],{pendingSavePromptsByToolCallId:r}},!1,{type:`setPendingSavePrompt`})},setPendingCodeEvaluatorEdit:(e,n)=>{t(t=>{let r={...t.pendingCodeEvaluatorEditsByToolCallId};return n?r[e]=n:delete r[e],{pendingCodeEvaluatorEditsByToolCallId:r}},!1,{type:`setPendingCodeEvaluatorEdit`})},setPendingLlmEvaluatorEdit:(e,n)=>{t(t=>{let r={...t.pendingLlmEvaluatorEditsByToolCallId};return n?r[e]=n:delete r[e],{pendingLlmEvaluatorEditsByToolCallId:r}},!1,{type:`setPendingLlmEvaluatorEdit`})},setPendingLoadDataset:(e,n)=>{t(t=>{let r={...t.pendingLoadDatasetsByToolCallId};return n?r[e]=n:delete r[e],{pendingLoadDatasetsByToolCallId:r}},!1,{type:`setPendingLoadDataset`})},...e}),{name:`agentStore`}),{name:Bp(),version:0,partialize:e=>({isOpen:e.isOpen,position:e.position,fabMode:e.fabMode,fabPlacement:e.fabPlacement,sessions:e.sessions,activeSessionId:e.activeSessionId,sessionMap:e.sessionMap,defaultModelConfig:e.defaultModelConfig,observability:e.observability,permissions:e.permissions,capabilities:e.capabilities}),merge:Pp}));async function Hp({agentStore:e,names:t,timeoutMs:n=5e3}){let r=e=>t.every(t=>t in e);return r(e.getState().registeredClientActions)?!0:new Promise(t=>{let i=!1,a=null,o=e=>{i||(i=!0,a&&clearTimeout(a),s(),t(e))},s=e.subscribe(e=>{r(e.registeredClientActions)&&o(!0)});a=setTimeout(()=>o(!1),n),r(e.getState().registeredClientActions)&&o(!0)})}var Up=(0,X.createContext)(null);function Wp(e){let t=(0,Z.c)(8),n,r;t[0]===e?(n=t[1],r=t[2]):({children:n,...r}=e,t[0]=e,t[1]=n,t[2]=r);let i;t[3]===r?i=t[4]:(i=()=>Vp(r),t[3]=r,t[4]=i);let[a]=(0,X.useState)(i),o;return t[5]!==n||t[6]!==a?(o=H(Up.Provider,{value:a,children:n}),t[5]=n,t[6]=a,t[7]=o):o=t[7],o}function Gp(e,t){let n=(0,X.useContext)(Up);if(!n)throw Error(`Missing AgentContext.Provider in the tree`);return O(n,e,t)}function Kp(){let e=(0,X.useContext)(Up);if(!e)throw Error(`Missing AgentContext.Provider in the tree`);return e}var qp=(0,X.createContext)(null);function Jp(){return X.useContext(qp)}function Yp(){let e=Jp();if(e===null)throw Error(`useTimeRange must be used within a TimeRangeContextProvider`);return e}function Xp({storedLastNTimeRangeKey:e,now:t}){return au(e)?{timeRangeKey:e,...ru(e,t)}:{timeRangeKey:`7d`,...ru(`7d`,t)}}function Zp(e){let t=(0,Z.c)(37),{children:n}=e,[r,i]=jn(),a=Kr(em),o=Kr($p),[s,c]=(0,X.useState)(Qp),l,u,d,f,p;t[0]!==r||t[1]!==a||t[2]!==s?(p=su(r,s),d=p??Xp({storedLastNTimeRangeKey:a,now:s}),f=d.start?.getTime(),l=d.start?.toISOString(),u=d.end?.toISOString(),t[0]=r,t[1]=a,t[2]=s,t[3]=l,t[4]=u,t[5]=d,t[6]=f,t[7]=p):(l=t[3],u=t[4],d=t[5],f=t[6],p=t[7]);let m=u,h;t[8]!==m||t[9]!==l?(h={start:l,end:m},t[8]=m,t[9]=l,t[10]=h):h=t[10];let g=h,_;t[11]!==i||t[12]!==o?(_=e=>{(0,X.startTransition)(()=>{i(t=>cu({searchParams:t,timeRange:e}),{replace:!0}),au(e.timeRangeKey)&&(o(e.timeRangeKey),c(Date.now()))})},t[11]=i,t[12]=o,t[13]=_):_=t[13];let v=_,y;t[14]===v?y=t[15]:(y=e=>{v({timeRangeKey:`custom`,start:e.start,end:e.end})},t[14]=v,t[15]=y);let b=y,x,S;t[16]!==r||t[17]!==i||t[18]!==d||t[19]!==p?(x=()=>{if(p!=null)return;let e=cu({searchParams:r,timeRange:d});e.toString()!==r.toString()&&i(e,{replace:!0})},S=[p,r,i,d],t[16]=r,t[17]=i,t[18]=d,t[19]=p,t[20]=x,t[21]=S):(x=t[20],S=t[21]),(0,X.useEffect)(x,S);let C;t[22]===d.timeRangeKey?C=t[23]:(C=()=>{if(!au(d.timeRangeKey))return;let e=d.timeRangeKey,t=window.setTimeout(()=>{c(Date.now())},iu(e));return()=>{window.clearTimeout(t)}},t[22]=d.timeRangeKey,t[23]=C);let w;t[24]!==d.timeRangeKey||t[25]!==f?(w=[d.timeRangeKey,f],t[24]=d.timeRangeKey,t[25]=f,t[26]=w):w=t[26],(0,X.useEffect)(C,w);let T;t[27]===v?T=t[28]:(T={setTimeRange:v},t[27]=v,t[28]=T),nm(T);let E;t[29]!==b||t[30]!==v||t[31]!==d||t[32]!==g?(E={timeRange:d,timeRangeISOStrings:g,setTimeRange:v,setCustomTimeRange:b},t[29]=b,t[30]=v,t[31]=d,t[32]=g,t[33]=E):E=t[33];let D;return t[34]!==n||t[35]!==E?(D=H(qp.Provider,{value:E,children:n}),t[34]=n,t[35]=E,t[36]=D):D=t[36],D}function Qp(){return Date.now()}function $p(e){return e.setLastNTimeRangeKey}function em(e){return e.lastNTimeRangeKey}function tm(e){if(e===void 0||e.trim()===``)return;let t=new Date(e);if(Number.isNaN(t.getTime()))throw Error(`Invalid ISO datetime: ${e}`);return t}function nm({setTimeRange:e}){let t=Kp(),n=(0,X.useEffectEvent)(async t=>{if(t.timeRangeKey!==`custom`)return e({timeRangeKey:t.timeRangeKey,...ru(t.timeRangeKey)}),{ok:!0,output:`Set time range to ${t.timeRangeKey}.`};try{let n=tm(t.startTime),r=tm(t.endTime);return n===void 0&&r===void 0?{ok:!1,error:`Custom time range requires at least one of startTime or endTime.`}:n!==void 0&&r!==void 0&&n>r?{ok:!1,error:`Custom time range startTime must be before endTime.`}:(e({timeRangeKey:`custom`,start:n,end:r}),{ok:!0,output:`Set custom time range from ${n?.toISOString()??`open start`} to ${r?.toISOString()??`open end`}.`})}catch(e){return{ok:!1,error:e instanceof Error?e.message:`Invalid time range.`}}});(0,X.useEffect)(()=>{let{registerClientAction:e,unregisterClientAction:r}=t.getState();return e(Nu,e=>n(e)),()=>{r(Nu)}},[t])}var rm=F(),im=500;function am(e,t){let n=(0,Z.c)(5),r=t===void 0?im:t,i;n[0]===e?i=n[1]:(i=t=>{try{e(JSON.parse(t))}catch{}},n[0]=e,n[1]=i);let a;return n[2]!==r||n[3]!==i?(a=(0,rm.debounce)(i,r),n[2]=r,n[3]=i,n[4]=a):a=n[4],a}function om(e,t){let n=(0,Z.c)(6),r=(0,X.useRef)(null),i,a;n[0]===e?(i=n[1],a=n[2]):(i=()=>{r.current=e},a=[e],n[0]=e,n[1]=i,n[2]=a),(0,X.useEffect)(i,a);let o,s;n[3]===t?(o=n[4],s=n[5]):(o=()=>{if(typeof t!=`number`)return;let e=t,n=function(){r.current?.()},i=setInterval(n,e),a=function(){document.visibilityState===`hidden`?i!=null&&(clearInterval(i),i=null):i??=(n(),setInterval(n,e))};return document.addEventListener(`visibilitychange`,a),()=>{i!=null&&clearInterval(i),document.removeEventListener(`visibilitychange`,a)}},s=[t],n[3]=t,n[4]=o,n[5]=s),(0,X.useEffect)(o,s)}var sm=.05,cm=({word:e,theme:t})=>{let n=de(e.charCodeAt(0)%26/26),r=t===`light`?3:5,i=t===`light`?`#fdfdfd`:`#0E0E0E`,a=ve(n,i);for(;a<r;)n=t===`light`?ie(sm,n):ce(sm,n),a=ve(n,i);return n},lm=e=>{let t=(0,Z.c)(3),{theme:n}=pr(),r;return t[0]!==n||t[1]!==e?(r=cm({word:e,theme:n}),t[0]=n,t[1]=e,t[2]=r):r=t[2],r};function um(e,t){let n=new Intl.DateTimeFormat(e,{...t});return e=>n.format(e)}function dm(e){let{locale:t,timeZone:n}=e;return um(t,{year:`numeric`,month:`2-digit`,day:`2-digit`,hour:`2-digit`,minute:`2-digit`,second:`2-digit`,hour12:!0,timeZone:n})}function fm(e){let{locale:t,timeZone:n}=e;return um(t,{hour:`2-digit`,minute:`2-digit`,hour12:!0,timeZone:n})}function pm(e){let{locale:t,timeZone:n}=e;return um(t,{year:`numeric`,month:`2-digit`,day:`2-digit`,hour:`2-digit`,minute:`2-digit`,hour12:!0,timeZone:n})}function mm(e){let t=pm(e);return e=>e.start&&e.end?`${t(e.start)} - ${t(e.end)}`:e.start?`From ${t(e.start)}`:e.end?`Until ${t(e.end)}`:`All Time`}function hm(e){let{timeZone:t,locale:n}=e;return Intl.DateTimeFormat(n,{timeZoneName:`short`,timeZone:t}).formatToParts().find(e=>e.type===`timeZoneName`)?.value}function gm(e,t=Date.now()){if(e===0)return``;let n=t-e;return n<6*36e5?new Date(e).toLocaleTimeString(void 0,{hour:`numeric`,minute:`2-digit`}):n<864e5?`${Math.floor(n/Li)}h`:`${Math.floor(n/Ri)}d`}function _m(e){return new Intl.DateTimeFormat(e,{day:`2-digit`,month:`2-digit`,year:`numeric`}).formatToParts(new Date).map(e=>{switch(e.type){case`day`:return`dd`;case`month`:return`mm`;case`year`:return`yyyy`;case`literal`:return e.value;default:return``}}).join(``)}function vm(){let e=(0,Z.c)(2),{locale:t}=Mn(),n;return e[0]===t?n=e[1]:(n=_m(t),e[0]=t,e[1]=n),n}var ym=e=>{let t=(0,Z.c)(3),[n,r]=(0,X.useState)(null),i,a;return t[0]===e?(i=t[1],a=t[2]):(i=()=>{if(!e.current)return;let t=new ResizeObserver(e=>{if(!e||e.length===0)return;let{width:t,height:n}=e[0].contentRect;r({width:t,height:n})});return t.observe(e.current),()=>{t.disconnect()}},a=[e],t[0]=e,t[1]=i,t[2]=a),(0,X.useEffect)(i,a),n};function bm(){let e=(0,Z.c)(10),t=Kr(xm),n,r,i,a;if(e[0]!==t){let o=t??Lr();n=dm({locale:Ir(),timeZone:o}),r=fm({locale:Ir(),timeZone:o}),i=pm({locale:Ir(),timeZone:o}),a=mm({locale:Ir(),timeZone:o}),e[0]=t,e[1]=n,e[2]=r,e[3]=i,e[4]=a}else n=e[1],r=e[2],i=e[3],a=e[4];let o;return e[5]!==n||e[6]!==r||e[7]!==i||e[8]!==a?(o={fullTimeFormatter:n,shortTimeFormatter:r,shortDateTimeFormatter:i,timeRangeFormatter:a},e[5]=n,e[6]=r,e[7]=i,e[8]=a,e[9]=o):o=e[9],o}function xm(e){return e.displayTimezone}function Sm(e){let t=(0,Z.c)(7),n;t[0]===e?n=t[1]:(n=e===void 0?{}:e,t[0]=e,t[1]=n);let{updateIntervalMs:r}=n,i=r===void 0?null:r,[a,o]=(0,X.useState)(Cm),s,c;t[2]===i?(s=t[3],c=t[4]):(s=()=>{if(typeof i!=`number`)return;let e=setInterval(()=>{o(Date.now())},i);return()=>clearInterval(e)},c=[i],t[2]=i,t[3]=s,t[4]=c),(0,X.useEffect)(s,c);let l;return t[5]===a?l=t[6]:(l={nowEpochMs:a},t[5]=a,t[6]=l),l}function Cm(){return Date.now()}function wm(e){let t=(0,Z.c)(2),n;return t[0]===e?n=t[1]:(n=nf(e),t[0]=e,t[1]=n),n}var Tm=`https://pypi.org/pypi/arize-phoenix/json`,Em=null;function Dm(){return Em??=fetch(Tm).then(e=>e.ok?e.json():null).then(e=>{let t=e?.info?.version;return typeof t==`string`?t:null}).catch(()=>null).then(e=>(e??(Em=null),e)),Em}function Om(){let e=(0,Z.c)(2),[t,n]=(0,X.useState)(null),r,i;return e[0]===Symbol.for(`react.memo_cache_sentinel`)?(r=()=>{let e=!0;return Dm().then(t=>{e&&n(t)}),()=>{e=!1}},i=[],e[0]=r,e[1]=i):(r=e[0],i=e[1]),(0,X.useEffect)(r,i),t}function km(e,t){let[n,r]=(0,X.useState)(()=>{try{let n=localStorage.getItem(e);return n?JSON.parse(n):t}catch{return t}});return[n,(0,X.useCallback)(t=>{r(n=>{let r=typeof t==`function`?t(n):t;try{localStorage.setItem(e,JSON.stringify(r))}catch{}return r})},[e])]}function Am(e){let{query:t,queryRef:n}=e,[r]=(0,Yr.useQueryLoader)(t,n);return ze(r,`ownedQueryRef is required when initialized from queryRef`),(0,Yr.usePreloadedQuery)(t,r)}function jm(){let e=(0,Z.c)(7),[t,n]=jn(),r;e[0]===t?r=e[1]:(r=t.getAll(Kl),e[0]=t,e[1]=r);let i=r,a;e[2]===n?a=e[3]:(a=e=>{n(t=>{let n=t.getAll(Kl),r=typeof e==`function`?e(n):e,i=new URLSearchParams(t);return i.delete(Kl),r.forEach(e=>i.append(Kl,e)),i},{replace:!0})},e[2]=n,e[3]=a);let o=a,s;return e[4]!==i||e[5]!==o?(s=[i,o],e[4]=i,e[5]=o,e[6]=s):s=e[6],s}function Mm(e){let t=(0,Z.c)(4),n;t[0]===e?n=t[1]:(n=t=>{let n=window.matchMedia(e);return n.addEventListener(`change`,t),()=>n.removeEventListener(`change`,t)},t[0]=e,t[1]=n);let r=n,i;return t[2]===e?i=t[3]:(i=()=>window.matchMedia(e).matches,t[2]=e,t[3]=i),(0,X.useSyncExternalStore)(r,i)}function Nm(e){let t=(0,Z.c)(49),{start:n,end:r,timeZone:i,isDisabled:a,onCommit:o,autoFocus:l,onBlurWithin:u,onSubmit:d,ref:f}=e,p=(0,X.useRef)(!1),m=(0,X.useRef)(!1),h=r==null,g;t[0]!==n||t[1]!==i?(g=()=>Tu(n,i),t[0]=n,t[1]=i,t[2]=g):g=t[2];let[_,v]=(0,X.useState)(g),y;t[3]!==r||t[4]!==i?(y=()=>Tu(r,i)??Ne(i),t[3]=r,t[4]=i,t[5]=y):y=t[5];let[b,x]=(0,X.useState)(y),S;t[6]!==_||t[7]!==i?(S=_?_.toDate(i):null,t[6]=_,t[7]=i,t[8]=S):S=t[8];let C=S,w;t[9]!==b||t[10]!==i?(w=b?b.toDate(i):null,t[9]=b,t[10]=i,t[11]=w):w=t[11];let T=w,E=!!(C&&T&&C>T),D;t[12]!==r||t[13]!==n||t[14]!==i?(D=()=>{v(Tu(n,i)),x(Tu(r,i)??Ne(i)),p.current=!1,m.current=!1},t[12]=r,t[13]=n,t[14]=i,t[15]=D):D=t[15];let O=D,k;t[16]!==T||t[17]!==h||t[18]!==o||t[19]!==O||t[20]!==C?(k=()=>{if(!p.current)return;let e=h&&!m.current?null:T;if(C&&e&&C>e){O();return}p.current=!1,o({start:C,end:e})},t[16]=T,t[17]=h,t[18]=o,t[19]=O,t[20]=C,t[21]=k):k=t[21];let A=k,j,M;t[22]===A?(j=t[23],M=t[24]):(j=()=>({commit:A}),M=[A],t[22]=A,t[23]=j,t[24]=M),(0,X.useImperativeHandle)(f,j,M);let N;t[25]!==A||t[26]!==u?(N={onBlurWithin:()=>{A(),u?.()}},t[25]=A,t[26]=u,t[27]=N):N=t[27];let{focusWithinProps:P}=Zt(N),F=E||void 0,I;t[28]!==A||t[29]!==d?(I=e=>{e.key===`Enter`&&(e.preventDefault(),A(),d?.())},t[28]=A,t[29]=d,t[30]=I):I=t[30];let L,ee;t[31]===Symbol.for(`react.memo_cache_sentinel`)?(L=e=>{v(e),p.current=!0},ee=H(c,{children:Fm}),t[31]=L,t[32]=ee):(L=t[31],ee=t[32]);let R;t[33]!==l||t[34]!==a||t[35]!==_?(R=H(s,{"aria-label":`Start time`,className:`time-range-selector__field`,granularity:`minute`,hideTimeZone:!0,isDisabled:a,autoFocus:l,value:_,onChange:L,children:ee}),t[33]=l,t[34]=a,t[35]=_,t[36]=R):R=t[36];let te;t[37]===Symbol.for(`react.memo_cache_sentinel`)?(te=H(`span`,{"aria-hidden":!0,className:`time-range-selector__separator`,children:`–`}),t[37]=te):te=t[37];let ne,re;t[38]===Symbol.for(`react.memo_cache_sentinel`)?(ne=e=>{x(e),p.current=!0,m.current=!0},re=H(c,{children:Pm}),t[38]=ne,t[39]=re):(ne=t[38],re=t[39]);let ie;t[40]!==b||t[41]!==a?(ie=H(s,{"aria-label":`End time`,className:`time-range-selector__field`,granularity:`minute`,hideTimeZone:!0,isDisabled:a,value:b,onChange:ne,children:re}),t[40]=b,t[41]=a,t[42]=ie):ie=t[42];let ae;return t[43]!==P||t[44]!==F||t[45]!==I||t[46]!==R||t[47]!==ie?(ae=U(`div`,{className:`time-range-selector__fields`,"data-invalid":F,onKeyDownCapture:I,...P,children:[R,te,ie]}),t[43]=P,t[44]=F,t[45]=I,t[46]=R,t[47]=ie,t[48]=ae):ae=t[48],ae}function Pm(e){return H(T,{segment:e})}function Fm(e){return H(T,{segment:e})}var Im=q`
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
`,Lm=q`
  /* Fill the popover, which is sized to the field it is anchored to. */
  width: 100%;
`,Rm=q`
  padding: var(--global-dimension-size-200) var(--global-dimension-size-150);
`,zm=q`
  width: 100%;
  border-bottom: var(--global-border-size-thin) solid
    var(--global-menu-border-color);
`,Bm=q`
  flex: none;
  font-variant-numeric: tabular-nums;
`,Vm=q`
  width: 100%;
  justify-content: flex-start;
`,Hm=`var(--global-dimension-size-4000)`;function Um(e){let t=(0,Z.c)(83),{value:n,isDisabled:i,onChange:a,size:o}=e,s=o===void 0?`S`:o,{timeRangeKey:c,start:l,end:u}=n,d=(0,X.useRef)(null),p=(0,X.useRef)(null),m=(0,X.useRef)(null),h=(0,X.useRef)(null),g=(0,X.useRef)(null),_=(0,X.useRef)(null),[v,y]=(0,X.useState)(!1),[b,S]=(0,X.useState)(!1),[C,w]=(0,X.useState)(!1),[T,E]=(0,X.useState)(),[D,O]=(0,X.useState)(``),k;t[0]===Symbol.for(`react.memo_cache_sentinel`)?(k={sensitivity:`base`},t[0]=k):k=t[0];let{contains:A}=r(k),j;t[1]===Symbol.for(`react.memo_cache_sentinel`)?(j=()=>{y(!1),w(!1),O(``)},t[1]=j):j=t[1];let M=j,N;t[2]===Symbol.for(`react.memo_cache_sentinel`)?(N=()=>{let e=document.activeElement;return e instanceof HTMLElement&&(d.current?.contains(e)||p.current?.contains(e))?e:null},t[2]=N):N=t[2];let P=N,F;t[3]===Symbol.for(`react.memo_cache_sentinel`)?(F=()=>{setTimeout(()=>{P()||(S(!1),M())})},t[3]=F):F=t[3];let I=F,L;t[4]===Symbol.for(`react.memo_cache_sentinel`)?(L=()=>{P()?.blur()},t[4]=L):L=t[4];let ee=L,R;t[5]===Symbol.for(`react.memo_cache_sentinel`)?(R=()=>{ee(),S(!1),M()},t[5]=R):R=t[5];let te=R,ne;t[6]===Symbol.for(`react.memo_cache_sentinel`)?(ne=()=>{_.current?.commit(),te()},t[6]=ne):ne=t[6];let re=ne,ie;t[7]===Symbol.for(`react.memo_cache_sentinel`)?(ie=()=>{y(!0)},t[7]=ie):ie=t[7];let ae=ie,oe=!v,se;t[8]===Symbol.for(`react.memo_cache_sentinel`)?(se=e=>{e.target instanceof Node&&p.current?.contains(e.target)||re()},t[8]=se):se=t[8];let ce;t[9]===oe?ce=t[10]:(ce={ref:d,isDisabled:oe,onInteractOutside:se},t[9]=oe,t[10]=ce),_n(ce);let le;t[11]===D?le=t[12]:(le=e=>{if(e.stopPropagation(),D&&document.activeElement===m.current){O(``);return}re()},t[11]=D,t[12]=le);let ue;t[13]===Symbol.for(`react.memo_cache_sentinel`)?(ue={capture:!0},t[13]=ue):ue=t[13];let de;t[14]===b?de=t[15]:(de={enabled:b,enableOnFormTags:!0,enableOnContentEditable:!0,preventDefault:!0,eventListenerOptions:ue},t[14]=b,t[15]=de),kt(`escape`,le,de);let fe=ym(h),pe=Kr(Km),me,he,ge,_e,ve;if(t[16]!==pe||t[17]!==u||t[18]!==l||t[19]!==c){_e=pe??Lr();let e=Ir();ve=hm({locale:e,timeZone:_e}),he=c===`custom`,me=he?`Custom`:c;let n=mm({locale:e,timeZone:_e});ge=au(c)?uu(c):n({start:l,end:u}),t[16]=pe,t[17]=u,t[18]=l,t[19]=c,t[20]=me,t[21]=he,t[22]=ge,t[23]=_e,t[24]=ve}else me=t[20],he=t[21],ge=t[22],_e=t[23],ve=t[24];let ye=ge,be=mu(D),xe=Yl.filter(e=>{let{key:t}=e;return!be.includes(t)}),Se;t[25]===l?Se=t[26]:(Se=l?.getTime()??``,t[25]=l,t[26]=Se);let Ce;t[27]===u?Ce=t[28]:(Ce=u?.getTime()??``,t[27]=u,t[28]=Ce);let we=`${c}|${Se}|${Ce}|${_e}`,Te=fe?.width,Ee=`${b}|${we}|${ye}|${me}|${ve??``}`,De=v&&T!=null,Oe;t[29]!==i||t[30]!==b?(Oe=e=>{if(i||b)return;let t=g.current,n=e.target instanceof Node&&t?.contains(e.target);!t||n||(e.preventDefault(),t.focus())},t[29]=i,t[30]=b,t[31]=Oe):Oe=t[31];let ke=Oe,Ae;t[32]===v?Ae=t[33]:(Ae=()=>{let e=v?d.current?.offsetWidth:void 0,t=e?`${e}px`:void 0;E(e=>e===t?e:t)},t[32]=v,t[33]=Ae);let je;t[34]!==v||t[35]!==Ee?(je=[v,Ee],t[34]=v,t[35]=Ee,t[36]=je):je=t[36],(0,X.useLayoutEffect)(Ae,je);let Me,Ne;t[37]!==C||t[38]!==De?(Me=()=>{!De||C||m.current?.focus()},Ne=[De,C],t[37]=C,t[38]=De,t[39]=Me,t[40]=Ne):(Me=t[39],Ne=t[40]),(0,X.useLayoutEffect)(Me,Ne);let Pe=i||void 0,Fe=v||void 0,Ie=he?`info`:`default`,Le;t[41]!==me||t[42]!==Ie?(Le=H(Oo,{size:`S`,variant:Ie,css:Bm,children:me}),t[41]=me,t[42]=Ie,t[43]=Le):Le=t[43];let Re=v||Te==null?`auto`:Te,z=b?Hm:void 0,ze;t[44]!==Re||t[45]!==z?(ze={width:Re,minWidth:z},t[44]=Re,t[45]=z,t[46]=ze):ze=t[46];let Be;t[47]!==u||t[48]!==we||t[49]!==i||t[50]!==b||t[51]!==a||t[52]!==l||t[53]!==_e||t[54]!==ye?(Be=H(`div`,{ref:h,className:`time-range-selector__value-measure`,children:b?H(Nm,{ref:_,start:l,end:u,timeZone:_e,isDisabled:i,autoFocus:!0,onBlurWithin:I,onSubmit:te,onCommit:e=>a({timeRangeKey:`custom`,...e})},we):H(`button`,{ref:g,type:`button`,className:`time-range-selector__value`,disabled:i,onFocus:()=>{i||(S(!0),ae())},children:ye})}),t[47]=u,t[48]=we,t[49]=i,t[50]=b,t[51]=a,t[52]=l,t[53]=_e,t[54]=ye,t[55]=Be):Be=t[55];let Ve;t[56]!==ze||t[57]!==Be?(Ve=H(`div`,{className:`time-range-selector__value-shell`,style:ze,children:Be}),t[56]=ze,t[57]=Be,t[58]=Ve):Ve=t[58];let He;t[59]===ve?He=t[60]:(He=ve&&H(B,{size:`XS`,color:`text-500`,className:`time-range-selector__timezone`,children:ve}),t[59]=ve,t[60]=He);let We;t[61]!==ke||t[62]!==s||t[63]!==Pe||t[64]!==Fe||t[65]!==Le||t[66]!==Ve||t[67]!==He?(We=U(`div`,{ref:d,className:`time-range-selector`,css:Im,"data-size":s,"data-disabled":Pe,"data-presets-open":Fe,role:`group`,"aria-label":`Time range`,onPointerDown:ke,children:[Le,Ve,He]}),t[61]=ke,t[62]=s,t[63]=Pe,t[64]=Fe,t[65]=Le,t[66]=Ve,t[67]=He,t[68]=We):We=t[68];let Ge=kn,Ke;t[69]===Symbol.for(`react.memo_cache_sentinel`)?(Ke=e=>{e||M()},t[69]=Ke):Ke=t[69];let qe=C?`bottom end`:`bottom start`,Je=C?`max-content`:T,Ye=C?T:void 0,Xe;t[70]!==Je||t[71]!==Ye?(Xe={width:Je,minWidth:Ye,overflow:`hidden`,transition:`none`,animation:`none`,transform:`translateY(0)`,opacity:1},t[70]=Je,t[71]=Ye,t[72]=Xe):Xe=t[72];let Ze=C?H(Au,{value:{start:l,end:u},timeZone:_e,onCancel:()=>w(!1),onApply:e=>{S(!1),M(),a({timeRangeKey:`custom`,...e})}}):U(G,{children:[U(Ue,{filter:A,children:[U(qo,{"aria-label":`Search time range presets`,size:`M`,variant:`quiet`,value:D,onChange:O,css:zm,children:[H(Go,{}),H(f,{ref:m,placeholder:`Search or type "25m"`,onBlur:I})]}),U(Ns,{"aria-label":`time range preset selection`,selectionMode:`single`,selectedKeys:he?[]:[c],css:Lm,renderEmptyState:Gm,onSelectionChange:e=>{let t=e===`all`?void 0:e.keys().next().value,n=au(t)?t:au(c)?c:void 0;if(S(!1),!n){M();return}let r=ru(n);M(),a({timeRangeKey:n,...r})},children:[be.map(e=>H(x,{id:e,textValue:D,children:uu(e)},e)),xe.map(Wm)]})]}),H(ya,{children:H(W,{size:`S`,variant:`quiet`,css:Vm,leadingVisual:H(V,{svg:H(Sn,{})}),onPress:()=>w(!0),children:`Pick from a calendar`})})]}),Qe;t[73]!==Ge||t[74]!==De||t[75]!==Ke||t[76]!==qe||t[77]!==Xe||t[78]!==Ze?(Qe=H(Ge,{ref:p,triggerRef:d,isOpen:De,onOpenChange:Ke,isNonModal:!0,isKeyboardDismissDisabled:!0,placement:qe,offset:2,style:Xe,children:Ze}),t[73]=Ge,t[74]=De,t[75]=Ke,t[76]=qe,t[77]=Xe,t[78]=Ze,t[79]=Qe):Qe=t[79];let $e;return t[80]!==We||t[81]!==Qe?($e=U(G,{children:[We,Qe]}),t[80]=We,t[81]=Qe,t[82]=$e):$e=t[82],$e}function Wm(e){let{key:t,label:n}=e;return H(x,{id:t,children:n},t)}function Gm(){return H(`div`,{css:Rm,children:`No matching time ranges`})}function Km(e){return e.displayTimezone}var qm=Ke`
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.35;
  }
`,Jm=q`
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
`,Ym=q`
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
      animation: ${qm} 3s ease-in-out infinite;
    }
  }

  @media (prefers-reduced-motion: reduce) {
    &[data-selected="true"]::before {
      animation: none;
    }
  }
`;function Xm(e){let t=(0,Z.c)(13),{label:n,icon:r,size:i,isDisabled:a,onPress:o}=e,s;t[0]===r?s=t[1]:(s=H(V,{svg:r}),t[0]=r,t[1]=s);let c;t[2]!==a||t[3]!==n||t[4]!==o||t[5]!==i||t[6]!==s?(c=H(W,{size:i,variant:`quiet`,css:Ym,"aria-label":n,isDisabled:a,leadingVisual:s,onPress:o}),t[2]=a,t[3]=n,t[4]=o,t[5]=i,t[6]=s,t[7]=c):c=t[7];let l;t[8]===n?l=t[9]:(l=H(Ni,{children:n}),t[8]=n,t[9]=l);let u;return t[10]!==c||t[11]!==l?(u=U(g,{children:[c,l]}),t[10]=c,t[11]=l,t[12]=u):u=t[12],u}function Zm(e){let t=(0,Z.c)(48),{value:n,onChange:r,isLive:i,onIsLiveChange:a,isDisabled:o,size:s}=e,c=i!==void 0&&i,l=s===void 0?`S`:s,u=n.start!=null,d=c?`Stop live streaming`:`Resume live streaming`,f=n.end==null,p;t[0]===r?p=t[1]:(p=e=>{e&&r(e)},t[0]=r,t[1]=p);let m=p,h=o||void 0,_;t[2]===Symbol.for(`react.memo_cache_sentinel`)?(_=H(Ht,{}),t[2]=_):_=t[2];let v=o||!u,y;t[3]!==m||t[4]!==n?(y=()=>m(bu({value:n})),t[3]=m,t[4]=n,t[5]=y):y=t[5];let b;t[6]!==l||t[7]!==v||t[8]!==y?(b=H(Xm,{label:`Pan back in time`,icon:_,size:l,isDisabled:v,onPress:y}),t[6]=l,t[7]=v,t[8]=y,t[9]=b):b=t[9];let x;t[10]===Symbol.for(`react.memo_cache_sentinel`)?(x=H(Dn,{}),t[10]=x):x=t[10];let S=o||!u,C;t[11]!==m||t[12]!==n?(C=()=>m(Cu({value:n})),t[11]=m,t[12]=n,t[13]=C):C=t[13];let w;t[14]!==l||t[15]!==C||t[16]!==S?(w=H(Xm,{label:`Zoom out`,icon:x,size:l,isDisabled:S,onPress:C}),t[14]=l,t[15]=C,t[16]=S,t[17]=w):w=t[17];let T;t[18]!==o||t[19]!==c||t[20]!==d||t[21]!==a||t[22]!==l?(T=a&&U(g,{children:[H(ks,{size:l,className:`time-range-controls__live-toggle`,css:Ym,"aria-label":d,isSelected:c,isDisabled:o,leadingVisual:H(V,{svg:H(c?Je:We,{})}),onChange:a}),H(Ni,{children:d})]}),t[18]=o,t[19]=c,t[20]=d,t[21]=a,t[22]=l,t[23]=T):T=t[23];let E;t[24]===Symbol.for(`react.memo_cache_sentinel`)?(E=H(mt,{}),t[24]=E):E=t[24];let D=o||!u,O;t[25]!==m||t[26]!==n?(O=()=>m(Su({value:n})),t[25]=m,t[26]=n,t[27]=O):O=t[27];let k;t[28]!==l||t[29]!==D||t[30]!==O?(k=H(Xm,{label:`Zoom in`,icon:E,size:l,isDisabled:D,onPress:O}),t[28]=l,t[29]=D,t[30]=O,t[31]=k):k=t[31];let A;t[32]===Symbol.for(`react.memo_cache_sentinel`)?(A=H(On,{}),t[32]=A):A=t[32];let j=o||!u||f,M;t[33]!==m||t[34]!==n?(M=()=>m(xu({value:n})),t[33]=m,t[34]=n,t[35]=M):M=t[35];let N;t[36]!==l||t[37]!==j||t[38]!==M?(N=H(Xm,{label:`Pan forward in time`,icon:A,size:l,isDisabled:j,onPress:M}),t[36]=l,t[37]=j,t[38]=M,t[39]=N):N=t[39];let P;return t[40]!==l||t[41]!==w||t[42]!==T||t[43]!==k||t[44]!==N||t[45]!==h||t[46]!==b?(P=U(`div`,{className:`time-range-controls`,css:Jm,role:`group`,"aria-label":`Time range controls`,"data-size":l,"data-disabled":h,children:[b,w,T,k,N]}),t[40]=l,t[41]=w,t[42]=T,t[43]=k,t[44]=N,t[45]=h,t[46]=b,t[47]=P):P=t[47],P}function Qm(e){let t=(0,Z.c)(4),{size:n}=e,r=n===void 0?`S`:n,{timeRange:i,setTimeRange:a}=Yp(),o;return t[0]!==a||t[1]!==r||t[2]!==i?(o=H(Um,{value:i,onChange:a,size:r}),t[0]=a,t[1]=r,t[2]=i,t[3]=o):o=t[3],o}function $m(e){let t=(0,Z.c)(4),{timeRange:n,setTimeRange:r}=Yp(),i;return t[0]!==e||t[1]!==r||t[2]!==n?(i=H(Zm,{...e,value:n,onChange:r}),t[0]=e,t[1]=r,t[2]=n,t[3]=i):i=t[3],i}q`
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
`;var eh=(0,X.createContext)(null);function th(){return(0,X.useContext)(eh)??{variant:`grid`}}var nh=q`
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
`,rh=q`
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
`,ih=q`
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
`,ah=q`
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
    position: absolute;
    top: var(--global-dimension-size-75);
    right: var(--global-dimension-size-75);
    width: var(--global-dimension-size-300);
    height: var(--global-dimension-size-300);
    border-radius: 50%;
    background-color: var(--global-color-gray-50);
    opacity: 0;
  }

  &[data-variant="inline"] {
    width: var(--global-dimension-size-200);
    height: var(--global-dimension-size-200);
    opacity: 0;
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
    opacity: 1;
    outline: var(--focus-ring-thickness) solid var(--focus-ring-color);
    outline-offset: var(--focus-ring-offset);
  }

  .icon-wrap {
    font-size: var(--global-font-size-s);
    line-height: 0;
  }
`;function oh(e){let t=(0,Z.c)(17),n,r,i,a,o;t[0]===e?(n=t[1],r=t[2],i=t[3],a=t[4],o=t[5]):({children:n,ref:r,variant:a,collapsible:o,...i}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a,t[5]=o);let s=a===void 0?`grid`:a,c=o!==void 0&&o,l;t[6]===s?l=t[7]:(l={variant:s},t[6]=s,t[7]=l);let u=l,d=c||void 0,f;t[8]!==n||t[9]!==r||t[10]!==i||t[11]!==d||t[12]!==s?(f=H(`div`,{ref:r,css:nh,"data-variant":s,"data-collapsible":d,...i,children:n}),t[8]=n,t[9]=r,t[10]=i,t[11]=d,t[12]=s,t[13]=f):f=t[13];let p;return t[14]!==f||t[15]!==u?(p=H(eh.Provider,{value:u,children:f}),t[14]=f,t[15]=u,t[16]=p):p=t[16],p}var sh=(0,X.createContext)(null);function ch(){let e=(0,X.useContext)(sh);if(!e)throw Error(`useAttachmentContext must be used within an <Attachment> component`);return e}function lh(e){if(e.type===`context`)return`context`;if(e.type===`source-document`)return`source`;let t=e.mediaType??``;return t.startsWith(`image/`)?`image`:t.startsWith(`video/`)?`video`:t.startsWith(`audio/`)?`audio`:t.startsWith(`application/`)||t.startsWith(`text/`)?`document`:`unknown`}function uh(e){return e.type===`context`?e.label:e.type===`source-document`?e.title||e.filename||`Source`:e.filename||(lh(e)===`image`?`Image`:`Attachment`)}function dh(e){return e.type===`context`?e.detail:void 0}function fh(e){switch(e){case`project`:return H(V,{svg:H(on,{})});case`trace`:return H(V,{svg:H(on,{})});case`session`:return H(V,{svg:H(An,{})});case`span`:return H(V,{svg:H(Kt,{})});case`span_filter`:return H(V,{svg:H(cn,{})});case`dataset`:return H(V,{svg:H(ht,{})});case`playground`:return H(V,{svg:H(en,{})});case`code_evaluator`:return H(V,{svg:H(xt,{})});case`llm_evaluator`:return H(V,{svg:H(Et,{})});default:return H(V,{svg:H(vn,{})})}}function ph(e){if(e.type===`context`)return e.icon??fh(e.category);switch(lh(e)){case`image`:return H(V,{svg:H(un,{})});case`video`:return H(V,{svg:H(en,{})});case`audio`:return H(V,{svg:H(tt,{})});case`document`:return H(V,{svg:H(dt,{})});case`source`:return H(V,{svg:H(Bt,{})});default:return H(V,{svg:H(tt,{})})}}function mh(e){let t=(0,Z.c)(22),n,r,i,a,o;t[0]===e?(n=t[1],r=t[2],i=t[3],a=t[4],o=t[5]):({children:n,ref:a,data:r,onRemove:i,...o}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a,t[5]=o);let{variant:s}=th(),{theme:c}=pr(),l;t[6]===r?l=t[7]:(l=lh(r),t[6]=r,t[7]=l);let u=l,d;t[8]!==r||t[9]!==u||t[10]!==i||t[11]!==s?(d={data:r,mediaCategory:u,variant:s,onRemove:i},t[8]=r,t[9]=u,t[10]=i,t[11]=s,t[12]=d):d=t[12];let f=d,p;t[13]!==n||t[14]!==a||t[15]!==o||t[16]!==c||t[17]!==s?(p=H(`div`,{ref:a,css:rh,"data-attachment":``,"data-variant":s,"data-theme":c,...o,children:n}),t[13]=n,t[14]=a,t[15]=o,t[16]=c,t[17]=s,t[18]=p):p=t[18];let m;return t[19]!==p||t[20]!==f?(m=H(sh.Provider,{value:f,children:p}),t[19]=p,t[20]=f,t[21]=m):m=t[21],m}function hh(e){let t=(0,Z.c)(16),n,r,i;t[0]===e?(n=t[1],r=t[2],i=t[3]):({ref:r,fallback:n,...i}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i);let{data:a,mediaCategory:o,variant:s}=ch(),c;t[4]!==a||t[5]!==n||t[6]!==o?(c=()=>a.type===`file`&&o===`image`&&typeof a.url==`string`&&a.url?H(`img`,{src:a.url,alt:a.filename??`Image`}):a.type===`file`&&o===`video`&&typeof a.url==`string`&&a.url?H(`video`,{src:a.url,muted:!0}):n??ph(a),t[4]=a,t[5]=n,t[6]=o,t[7]=c):c=t[7];let l=c,u;t[8]===l?u=t[9]:(u=l(),t[8]=l,t[9]=u);let d;return t[10]!==o||t[11]!==r||t[12]!==i||t[13]!==u||t[14]!==s?(d=H(`div`,{ref:r,css:ih,"data-variant":s,"data-media-category":o,...i,children:u}),t[10]=o,t[11]=r,t[12]=i,t[13]=u,t[14]=s,t[15]=d):d=t[15],d}function gh(e){let t=(0,Z.c)(28),n,r,i;t[0]===e?(n=t[1],r=t[2],i=t[3]):({ref:n,showMediaType:i,...r}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i);let a=i!==void 0&&i,{data:o,variant:s}=ch();if(s===`grid`)return null;let c;t[4]===o?c=t[5]:(c=uh(o),t[4]=o,t[5]=c);let l=c,u,d,f,p,m;t[6]!==o||t[7]!==n?(u=dh(o),d=o.type===`file`||o.type===`source-document`?o.mediaType:void 0,f=n,p=ah,m=z(`attachment-info`,{"attachment-info--with-detail":u}),t[6]=o,t[7]=n,t[8]=u,t[9]=d,t[10]=f,t[11]=p,t[12]=m):(u=t[8],d=t[9],f=t[10],p=t[11],m=t[12]);let h;t[13]===l?h=t[14]:(h=H(`span`,{className:`attachment-info__label`,children:l}),t[13]=l,t[14]=h);let g;t[15]===u?g=t[16]:(g=u?H(`span`,{className:`attachment-info__detail`,children:u}):null,t[15]=u,t[16]=g);let _;t[17]!==d||t[18]!==a?(_=a&&d?H(`span`,{className:`attachment-info__media-type`,children:d}):null,t[17]=d,t[18]=a,t[19]=_):_=t[19];let v;return t[20]!==r||t[21]!==f||t[22]!==p||t[23]!==m||t[24]!==h||t[25]!==g||t[26]!==_?(v=U(`div`,{ref:f,css:p,className:m,...r,children:[h,g,_]}),t[20]=r,t[21]=f,t[22]=p,t[23]=m,t[24]=h,t[25]=g,t[26]=_,t[27]=v):v=t[27],v}var _h=q`
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
`,vh=q`
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
`;function yh(e){let t=(0,Z.c)(27),{selected:n,type:r,label:i,description:a,isFreeformEntry:o,textValue:s,onToggle:c,onTextChange:l}=e,u=(0,X.useRef)(null),d,f;t[0]!==o||t[1]!==n?(d=()=>{n&&o&&u.current&&u.current.focus()},f=[n,o],t[0]=o,t[1]=n,t[2]=d,t[3]=f):(d=t[2],f=t[3]),(0,X.useEffect)(d,f);let p=r===`single`?`option-button__indicator option-button__indicator--radio`:`option-button__indicator option-button__indicator--checkbox`,m;t[4]===Symbol.for(`react.memo_cache_sentinel`)?(m={scale:.98,transition:{type:`tween`,duration:.06}},t[4]=m):m=t[4];let h=r===`single`?`radio`:`checkbox`,g;t[5]===c?g=t[6]:(g=e=>{let t=e.target;t.tagName===`INPUT`||t.tagName===`TEXTAREA`||e.key===`Enter`&&(e.metaKey||e.ctrlKey)||(e.key===`Enter`||e.key===` `)&&(e.preventDefault(),c())},t[5]=c,t[6]=g);let _;t[7]===r?_=t[8]:(_=r===`multi`&&H(`svg`,{viewBox:`0 0 18 18`,"aria-hidden":`true`,children:H(`polyline`,{points:`1 9 7 14 15 4`})}),t[7]=r,t[8]=_);let v;t[9]!==p||t[10]!==_?(v=H(`span`,{className:p,children:_}),t[9]=p,t[10]=_,t[11]=v):v=t[11];let y;t[12]!==a||t[13]!==o||t[14]!==i||t[15]!==l||t[16]!==c||t[17]!==n||t[18]!==s?(y=o?H(`div`,{className:`option-button__text-entry`,onClick:bh,children:H(`input`,{ref:u,type:`text`,className:`option-button__text-input`,value:s||``,placeholder:`Type your own answer…`,onMouseDown:()=>{n||c()},onChange:e=>{n||c(),l?.(e.target.value)},"aria-label":`Type your own answer`})}):U(`div`,{className:`option-button__content`,children:[H(`span`,{className:`option-button__label`,children:i}),a?H(`span`,{className:`option-button__description`,children:a}):null]}),t[12]=a,t[13]=o,t[14]=i,t[15]=l,t[16]=c,t[17]=n,t[18]=s,t[19]=y):y=t[19];let b;return t[20]!==c||t[21]!==n||t[22]!==h||t[23]!==g||t[24]!==v||t[25]!==y?(b=U(be.div,{css:vh,"data-selected":n,onClick:c,whileTap:m,role:h,"aria-checked":n,tabIndex:0,onKeyDown:g,children:[v,y]}),t[20]=c,t[21]=n,t[22]=h,t[23]=g,t[24]=v,t[25]=y,t[26]=b):b=t[26],b}function bh(e){return e.stopPropagation()}var xh=`__freeform__`,Sh=.04,Ch={enter:e=>({x:e>0?120:-120,opacity:0}),center:{x:0,opacity:1},exit:e=>({x:e>0?-120:120,opacity:0})},wh={type:`spring`,stiffness:400,damping:32,mass:.8},Th={type:`spring`,stiffness:700,damping:24,mass:.6};function Eh({questions:e,onProgressStateChange:t,onSubmit:n,onCancel:r}){let[i,a]=(0,X.useState)({}),[o,s]=(0,X.useState)({}),[c,l]=(0,X.useState)(0),[u,d]=(0,X.useState)(0),f=(0,X.useRef)(!0),p=(0,X.useEffectEvent)(e=>{t?.(e)}),m=e.length,h=e[c];(0,X.useEffect)(()=>{let e=setTimeout(()=>{f.current=!1},500);return()=>clearTimeout(e)},[]),(0,X.useEffect)(()=>{p({answers:{},freeformTexts:{},currentIndex:0})},[]);let g=e=>{d(e>c?1:-1),l(e),t?.({answers:i,freeformTexts:o,currentIndex:e})},_=(e,t,n)=>{let r=i[e]||[],o;o=n===`single`?r.includes(t)?[]:[t]:r.includes(t)?r.filter(e=>e!==t):[...r,t],a(t=>({...t,[e]:o}))},v=(e,t)=>{a(n=>({...n,[e]:t}))},y=()=>{t?.({answers:i,freeformTexts:o,currentIndex:c}),n({answers:i,freeformTexts:o})},b=()=>{let t=i[e[c].id];((Array.isArray(t)?t.length>0:t)||e[c].allow_skip===!0)&&(c===m-1?y():g(c+1))},x=e=>{if(e.key!==`Enter`||e.nativeEvent.isComposing)return;let t=e.target;if(t.tagName===`TEXTAREA`)return;let n=t.tagName===`INPUT`&&t.type===`text`;(e.metaKey||e.ctrlKey||n)&&(e.preventDefault(),b())},S=e=>{e.key!==`Enter`||e.nativeEvent.isComposing||e.shiftKey||(e.preventDefault(),b())},C=f.current?Sh:0,w=C,T=2*C,E=e=>(3+e)*C,D=3*C,O=i[h.id],k=Array.isArray(O)?O.length>0:!!O,A=h.allow_skip===!0,j=k||A;return H(En,{autoFocus:!0,contain:!0,restoreFocus:!0,children:U(`div`,{css:_h,onKeyDown:x,children:[U(be.div,{className:`elicitation__header`,initial:{opacity:0,y:8},animate:{opacity:1,y:0},transition:{...Th,delay:w,opacity:{duration:.12,delay:w}},children:[U(`span`,{className:`elicitation__step-label`,children:[`Question `,c+1,` of `,m]}),H(`div`,{className:`elicitation__dots`,children:e.map((e,t)=>H(`button`,{className:`elicitation__dot ${t===c?`elicitation__dot--active`:`elicitation__dot--inactive`}`,onClick:()=>g(t),"aria-label":`Go to question ${t+1}`},t))})]}),H(`div`,{className:`elicitation__body`,children:H(pe,{custom:u,mode:`popLayout`,children:U(be.div,{custom:u,variants:Ch,initial:!f.current&&`enter`,animate:`center`,exit:`exit`,transition:wh,className:`elicitation__question-content`,children:[H(be.div,{className:`elicitation__prompt`,initial:{opacity:0,y:-8},animate:{opacity:1,y:0},transition:{...Th,delay:T,opacity:{duration:.12,delay:T}},children:h.prompt}),h.type===`freeform`?H(be.div,{initial:{opacity:0,y:-8},animate:{opacity:1,y:0},transition:{...Th,delay:D,opacity:{duration:.12,delay:D}},children:H(`textarea`,{className:`elicitation__freeform`,value:i[h.id]||``,onChange:e=>v(h.id,e.target.value),onKeyDown:S,placeholder:`Type your response… (Enter to submit, Shift+Enter for newline)`,"aria-label":h.prompt})}):U(`div`,{className:`elicitation__options`,children:[h.options?.map((e,t)=>H(be.div,{initial:{opacity:0,y:-8},animate:{opacity:1,y:0},transition:{...Th,delay:E(t),opacity:{duration:.12,delay:E(t)}},children:H(yh,{selected:(i[h.id]||[]).includes(e.id),type:h.type,label:e.label,description:e.description,onToggle:()=>_(h.id,e.id,h.type)})},e.id)),h.allow_freeform?H(be.div,{initial:{opacity:0,y:-8},animate:{opacity:1,y:0},transition:{...Th,delay:E(h.options?.length??0),opacity:{duration:.12,delay:E(h.options?.length??0)}},children:H(yh,{selected:(i[h.id]||[]).includes(xh),type:h.type,label:`Type your own answer`,isFreeformEntry:!0,textValue:o[h.id],onToggle:()=>_(h.id,xh,h.type),onTextChange:e=>s(t=>({...t,[h.id]:e}))})},xh):null]})]},h.id)})}),U(be.div,{className:`elicitation__nav`,initial:{opacity:0,y:8},animate:{opacity:1,y:0},transition:{...Th,delay:0,opacity:{duration:.12,delay:0}},children:[U(`div`,{className:`elicitation__nav-group`,children:[r&&H(W,{size:`S`,variant:`default`,onPress:r,children:`Cancel`}),H(W,{size:`S`,variant:`default`,isDisabled:c===0,onPress:()=>g(c-1),children:`Back`})]}),c===m-1?H(W,{size:`S`,variant:`primary`,isDisabled:!j,onPress:y,children:`Submit`}):H(W,{size:`S`,variant:k?`primary`:`default`,isDisabled:!j,onPress:()=>g(c+1),children:k?`Next`:`Skip`})]})]})})}var Dh=(0,X.createContext)(null);function Oh(){let e=(0,X.useContext)(Dh);if(!e)throw Error(`usePromptInputContext must be used within a <PromptInput> component`);return e}var kh=q`
  display: flex;
  flex-direction: column;
  background-color: var(--prompt-input-background-color);
  border: var(--global-border-size-thin) solid var(--prompt-input-border-color);
  border-radius: var(--prompt-input-border-radius);
  transition: border-color 0.2s ease-in-out;

  &[data-input-mode="prompt"]:focus-within {
    border-color: var(--prompt-input-border-color-focus);
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
`,Ah=q`
  flex: 1 1 auto;
  padding: var(--global-dimension-size-200);
  padding-bottom: var(--global-dimension-size-100);
`,jh=q`
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
`,Mh=q`
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--global-dimension-size-100) var(--global-dimension-size-150);
  gap: var(--global-dimension-size-100);
`,Nh=q`
  display: flex;
  align-items: center;
  gap: var(--global-dimension-size-50);
`,Ph=q`
  display: flex;
  align-items: center;
  gap: var(--global-dimension-size-50);
`,Fh=q`
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
`;function Ih({children:e,ref:t,onSubmit:n,status:r=`ready`,isDisabled:i=!1,mode:a=`prompt`,value:o,onValueChange:s,...c}){let[l,u]=(0,X.useState)(``),d=o!==void 0,f=d?o:l,p=e=>{d||u(e),s?.(e)},m=(0,X.useRef)(f);m.current=f;let h={status:r,isDisabled:i,onSubmit:()=>{if(r===`submitted`||r===`streaming`)return;let e=m.current.trim();e&&(n?.(e),p(``))},value:f,setValue:p};return H(Dh.Provider,{value:h,children:H(`div`,{ref:t,css:kh,"data-status":r,"data-input-mode":a,...c,children:e})})}function Lh(e){let t=(0,Z.c)(8),n,r,i;t[0]===e?(n=t[1],r=t[2],i=t[3]):({children:n,ref:r,...i}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i);let a;return t[4]!==n||t[5]!==r||t[6]!==i?(a=H(`div`,{ref:r,css:Ah,...i,children:n}),t[4]=n,t[5]=r,t[6]=i,t[7]=a):a=t[7],a}function Rh(e){let t=(0,Z.c)(8),n,r,i;t[0]===e?(n=t[1],r=t[2],i=t[3]):({children:n,ref:r,...i}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i);let a;return t[4]!==n||t[5]!==r||t[6]!==i?(a=H(`div`,{ref:r,css:Mh,...i,children:n}),t[4]=n,t[5]=r,t[6]=i,t[7]=a):a=t[7],a}function zh(e){let t=(0,Z.c)(8),n,r,i;t[0]===e?(n=t[1],r=t[2],i=t[3]):({children:n,ref:r,...i}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i);let a;return t[4]!==n||t[5]!==r||t[6]!==i?(a=H(`div`,{ref:r,css:Nh,role:`toolbar`,...i,children:n}),t[4]=n,t[5]=r,t[6]=i,t[7]=a):a=t[7],a}function Bh(e){let t=(0,Z.c)(8),n,r,i;t[0]===e?(n=t[1],r=t[2],i=t[3]):({children:n,ref:r,...i}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i);let a;return t[4]!==n||t[5]!==r||t[6]!==i?(a=H(`div`,{ref:r,css:Ph,...i,children:n}),t[4]=n,t[5]=r,t[6]=i,t[7]=a):a=t[7],a}function Vh(e){let t=(0,Z.c)(20),{ref:n,placeholder:r,value:i,onChange:a,maxRows:o,"aria-label":s,className:c}=e,l=r===void 0?`Send a message...`:r,u=s===void 0?`Message input`:s,d=Oh(),f=(0,X.useRef)(null),p=i===void 0?d.value:i,m=a===void 0?d.setValue:a,h;t[0]===n?h=t[1]:(h=e=>{f.current=e,typeof n==`function`?n(e):n&&`current`in n&&(n.current=e)},t[0]=n,t[1]=h);let g=h,_;t[2]===o?_=t[3]:(_=()=>{let e=f.current;if(!e)return;let t=()=>{e.style.height=`auto`;let t=e.scrollHeight;if(o){let n=parseInt(getComputedStyle(e).lineHeight||`20`,10)*o;t=Math.min(t,n)}e.style.height=`${t}px`};t();let n=requestAnimationFrame(t);return()=>{cancelAnimationFrame(n)}},t[2]=o,t[3]=_);let v;t[4]!==o||t[5]!==p?(v=[p,o],t[4]=o,t[5]=p,t[6]=v):v=t[6],(0,X.useLayoutEffect)(_,v);let{onSubmit:y}=d,b;t[7]===y?b=t[8]:(b=e=>{e.key===`Enter`&&!e.shiftKey&&(e.preventDefault(),y())},t[7]=y,t[8]=b);let x=b,S;t[9]===m?S=t[10]:(S=e=>{m(e.target.value)},t[9]=m,t[10]=S);let C=S,w;return t[11]!==u||t[12]!==c||t[13]!==d.isDisabled||t[14]!==C||t[15]!==x||t[16]!==g||t[17]!==l||t[18]!==p?(w=H(`textarea`,{ref:g,css:jh,className:c,value:p,onChange:C,onKeyDown:x,placeholder:l,disabled:d.isDisabled,"aria-label":u,rows:1}),t[11]=u,t[12]=c,t[13]=d.isDisabled,t[14]=C,t[15]=x,t[16]=g,t[17]=l,t[18]=p,t[19]=w):w=t[19],w}function Hh(e){let t=(0,Z.c)(15),{ref:n,onPress:r,isDisabled:i,"aria-label":a,className:o}=e,s=Oh(),c=s.status===`submitted`||s.status===`streaming`,l;t[0]===s.value?l=t[1]:(l=s.value.trim(),t[0]=s.value,t[1]=l);let u=l===``,d=i??(s.status===`ready`&&u),f=!c,p=a??(f?`Send message`:`Stop generation`),m;t[2]!==s||t[3]!==c||t[4]!==r?(m=()=>{if(c){r?.();return}s.onSubmit()},t[2]=s,t[3]=c,t[4]=r,t[5]=m):m=t[5];let h=m,g=d||s.isDisabled,_;t[6]===f?_=t[7]:(_=H(V,{svg:H(f?Be:bn,{})}),t[6]=f,t[7]=_);let v;return t[8]!==o||t[9]!==p||t[10]!==h||t[11]!==n||t[12]!==g||t[13]!==_?(v=H(Tt,{ref:n,css:Fh,className:o,isDisabled:g,onPress:h,"aria-label":p,children:_}),t[8]=o,t[9]=p,t[10]=h,t[11]=n,t[12]=g,t[13]=_,t[14]=v):v=t[14],v}q`
  display: flex;
  align-items: center;
  gap: var(--global-dimension-size-75);
`;var Uh=q`
  ${tn};
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
`,Wh=new Map,Gh=e=>{let t=Wh.get(e);if(t)return t;let n=be.create(e);return Wh.set(e,n),n};function Kh(e){let t=(0,Z.c)(37),n,r,i,a,o,s,c,l,u,d,f,p;t[0]===e?(n=t[1],r=t[2],i=t[3],a=t[4],o=t[5],s=t[6],c=t[7],l=t[8],u=t[9],d=t[10],f=t[11],p=t[12]):({ref:i,children:n,elementType:s,size:c,weight:l,color:u,fontStyle:d,duration:f,spread:p,className:r,style:o,...a}=e,t[0]=e,t[1]=n,t[2]=r,t[3]=i,t[4]=a,t[5]=o,t[6]=s,t[7]=c,t[8]=l,t[9]=u,t[10]=d,t[11]=f,t[12]=p);let m=s===void 0?`p`:s,h=c===void 0?`S`:c,g=l===void 0?`normal`:l,_=u===void 0?`text-700`:u,v=d===void 0?`normal`:d,y=f===void 0?2:f,b=p===void 0?2:p,x=ke(),S=m,C;t[13]===S?C=t[14]:(C=Gh(S),t[13]=S,t[14]=C);let w=C,T=(n?.length??0)*b,E;t[15]!==y||t[16]!==x?(E=x?{}:{initial:{backgroundPosition:`100% center`},animate:{backgroundPosition:`0% center`},transition:{duration:y,ease:`linear`,repeat:1/0}},t[15]=y,t[16]=x,t[17]=E):E=t[17];let D=E,O=i,k;t[18]===r?k=t[19]:(k=z(`shimmer`,r),t[18]=r,t[19]=k);let A=`${T}px`,j;t[20]===_?j=t[21]:(j=gt(_),t[20]=_,t[21]=j);let M;t[22]!==v||t[23]!==o||t[24]!==A||t[25]!==j?(M={"--shimmer-spread":A,"--shimmer-color":j,fontStyle:v,...o},t[22]=v,t[23]=o,t[24]=A,t[25]=j,t[26]=M):M=t[26];let N=M,P=a,F;return t[27]!==w||t[28]!==D||t[29]!==n||t[30]!==h||t[31]!==O||t[32]!==k||t[33]!==N||t[34]!==P||t[35]!==g?(F=H(w,{ref:O,className:k,"data-size":h,"data-weight":g,css:Uh,style:N,...D,...P,children:n}),t[27]=w,t[28]=D,t[29]=n,t[30]=h,t[31]=O,t[32]=k,t[33]=N,t[34]=P,t[35]=g,t[36]=F):F=t[36],F}Kh.displayName=`Shimmer`;var qh=(0,X.createContext)(null);function Jh(){return(0,X.useContext)(qh)}function Yh(e){let t=e.parentElement;for(;t;){let{overflowY:e}=getComputedStyle(t);if((e===`auto`||e===`scroll`)&&t.scrollHeight>t.clientHeight)return t;t=t.parentElement}return null}function Xh(){let e=(0,Z.c)(5),t=Jh(),n=(0,X.useRef)(null),r;e[0]===t?r=e[1]:(r=e=>{if(t?.stopScroll(),n.current=null,!e)return;let r=Yh(e);if(!r)return;let i=e.getBoundingClientRect(),a=r.getBoundingClientRect();n.current={scrollParent:r,offsetFromParentTop:i.top-a.top}},e[0]=t,e[1]=r);let i=r,a;e[2]===Symbol.for(`react.memo_cache_sentinel`)?(a=e=>{let t=n.current;if(n.current=null,!t||!e)return;let{scrollParent:r,offsetFromParentTop:i}=t,a=e.getBoundingClientRect(),o=r.getBoundingClientRect(),s=a.top-o.top;r.scrollTop+=s-i},e[2]=a):a=e[2];let o=a,s;return e[3]===i?s=e[4]:(s={capture:i,restore:o},e[3]=i,e[4]=s),s}var Zh=Ke`
  from {
    opacity: 0;
    transform: translateY(-2px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
`,Qh={titleFlex:`0 1 auto`,titleMinWidth:`0`,titleMaxWidth:`55%`,middleFlex:`1 1 50px`,middleMinWidth:`50px`,statusFlex:`0 1 auto`,statusMinWidth:`0`,statusMaxWidth:`none`};function $h(e){let t=(0,Z.c)(3),{children:n,variant:r}=e,i;return t[0]!==n||t[1]!==r?(i=H(`div`,{className:`tool-part__line`,children:H(`span`,{className:`tool-part__label`,"data-variant":r,children:n})}),t[0]=n,t[1]=r,t[2]=i):i=t[2],i}function eg(e){let t=(0,Z.c)(9),{children:n,allowCopy:r}=e,i=r===void 0||r,a=`tool-part__line${i?` tool-part__line--copyable`:``}`,o=n||`(empty)`,s;t[0]===o?s=t[1]:(s=H(`code`,{className:`tool-part__code`,children:o}),t[0]=o,t[1]=s);let c;t[2]!==i||t[3]!==n?(c=i?H(oa,{text:n,size:`S`,variant:`quiet`,tooltipText:`Copy`}):null,t[2]=i,t[3]=n,t[4]=c):c=t[4];let l;return t[5]!==a||t[6]!==s||t[7]!==c?(l=U(`div`,{className:a,children:[s,c]}),t[5]=a,t[6]=s,t[7]=c,t[8]=l):l=t[8],l}function tg(e){let t=(0,Z.c)(3),{children:n,variant:r}=e,i;return t[0]!==n||t[1]!==r?(i=H(`span`,{className:`tool-part__status`,"data-variant":r,children:n}),t[0]=n,t[1]=r,t[2]=i):i=t[2],i}function ng(e){let t=(0,Z.c)(4),{items:n}=e,r;t[0]===n?r=t[1]:(r=n.map(rg),t[0]=n,t[1]=r);let i;return t[2]===r?i=t[3]:(i=H(`div`,{className:`tool-part__meta`,children:r}),t[2]=r,t[3]=i),i}function rg(e){let{label:t,value:n}=e;return U(`span`,{className:`tool-part__meta-group`,children:[H(`span`,{className:`tool-part__meta-label`,children:t}),H(`code`,{className:`tool-part__meta-value`,children:n})]},t)}var ig=q`
  padding: var(--global-dimension-size-50) var(--global-dimension-size-200)
    var(--global-dimension-size-150);
`;function ag(e){let t=(0,Z.c)(15),{onAccept:n,onReject:r,isDisabled:i,staleMessage:a}=e,o=i!==void 0&&i,s;t[0]!==o||t[1]!==n?(s=H(W,{size:`S`,variant:`primary`,isDisabled:o,onPress:n,children:`Accept`}),t[0]=o,t[1]=n,t[2]=s):s=t[2];let c;t[3]!==o||t[4]!==r?(c=H(W,{size:`S`,isDisabled:o,onPress:r,children:`Reject`}),t[3]=o,t[4]=r,t[5]=c):c=t[5];let l;t[6]!==s||t[7]!==c?(l=H(`div`,{css:ig,children:U(K,{direction:`row-reverse`,gap:`size-100`,children:[s,c]})}),t[6]=s,t[7]=c,t[8]=l):l=t[8];let u;t[9]!==o||t[10]!==a?(u=o&&a?H(eg,{children:a}):null,t[9]=o,t[10]=a,t[11]=u):u=t[11];let d;return t[12]!==l||t[13]!==u?(d=U(G,{children:[l,u]}),t[12]=l,t[13]=u,t[14]=d):d=t[14],d}var og=320,sg=q`
  --expandable-content-overlay-background-color: var(
    --tool-call-body-background-color
  );
`;function cg(e){let t=(0,Z.c)(6),{children:n}=e,r=(0,X.useRef)(null),[i,a]=(0,X.useState)(!1),o=Xh(),s;t[0]===o?s=t[1]:(s=e=>{o.capture(r.current),a(e),requestAnimationFrame(()=>o.restore(r.current))},t[0]=o,t[1]=s);let c=s,l;return t[2]!==n||t[3]!==c||t[4]!==i?(l=H(`div`,{ref:r,css:sg,children:H(qe,{height:og,expandedBehavior:`grow`,isExpanded:i,onExpandedChange:c,children:n})}),t[2]=n,t[3]=c,t[4]=i,t[5]=l):l=t[5],l}function lg(e){switch(e){case`input-streaming`:return`Preparing`;case`input-available`:return`Running`;case`approval-requested`:return`Awaiting approval`;case`approval-responded`:return`Approval received`;case`output-available`:return`Completed`;case`output-error`:return`Error`;case`output-denied`:return`Denied`}}function ug(e){if(e==null)return``;if(typeof e==`string`)return e;try{return JSON.stringify(e,null,2)}catch{return String(e)}}export{Mp as $,Xn as $i,jo as $n,Si as $r,Jc as $t,Mm as A,Rr as Ai,Ds as An,ea as Ar,Hu as At,um as B,_r as Bi,cs as Bn,Wi as Br,Rl as Bt,Eh as C,Qr as Ci,zs as Cn,_a as Cr,Qd as Ct,oh as D,Hr as Di,Ns as Dn,ca as Dr,Yu as Dt,mh as E,Kr as Ei,Fs as En,ga as Er,ud as Et,wm as F,Mr as Fi,ys as Fn,Qi as Fr,Jl as Ft,om as G,$n as Gi,Yo as Gn,Hi as Gr,yl as Gt,hm as H,mr as Hi,ts as Hn,zi as Hr,Pl as Ht,Sm as I,Nr as Ii,ms as In,Xi as Ir,zl as It,Jp as J,tr as Ji,Wo as Jn,Ni as Jr,ol as Jt,am as K,er as Ki,qo as Kn,Bi as Kr,gl as Kt,bm as L,Er as Li,ps as Ln,Ki as Lr,Vl as Lt,Am as M,zr as Mi,Cs as Mn,na as Mr,zu as Mt,km as N,jr as Ni,xs as Nn,ta as Nr,Ru as Nt,$m as O,Br as Oi,js as On,ba as Or,Ju as Ot,Om as P,Dr as Pi,_s as Pn,$i as Pr,ql as Pt,Kp as Q,Jn as Qi,Mo as Qn,wi as Qr,Xc as Qt,ym as R,wr as Ri,fs as Rn,Ui as Rr,Hl as Rt,Oh as S,ri as Si,Gs as Sn,ya as Sr,$d as St,hh as T,Gr as Ti,Hs as Tn,da as Tr,Q as Tt,lm as U,or as Ui,Qo as Un,Vi as Ur,Nl as Ut,gm as V,gr as Vi,ns as Vn,Ii as Vr,Ll as Vt,cm as W,pr as Wi,Xo as Wn,Fi as Wr,Dl as Wt,Wp as X,Gn as Xi,Uo as Xn,Oi as Xr,el as Xt,Yp as Y,Wn as Yi,Ho as Yn,Ai as Yr,rl as Yt,Gp as Z,Yn as Zi,Fo as Zn,Di as Zr,Qc as Zt,Bh as _,ei as _i,oc as _n,Ta as _r,Wd as _t,ag as a,ui as ai,Lc as an,yo as ar,yp as at,Lh as b,ti as bi,qs as bn,la as br,Zd as bt,$h as c,di as ci,Tc as cn,to as cr,gp as ct,Yh as d,yi as di,vc as dn,Ra as dr,_p as dt,qn as ea,xi as ei,Kc as en,No as er,jp as et,Xh as f,vi as fi,_c as fn,La as fr,bp as ft,Vh as g,$r as gi,ic as gn,Da as gr,Gd as gt,Hh as h,oi as hi,lc as hn,ka as hr,Xd as ht,Zh as i,mi as ii,zc as in,xo as ir,fp as it,jm as j,Lr as ji,Ts as jn,ra as jr,Vu as jt,Qm as k,Ir as ki,ks as kn,oa as kr,Uu as kt,ng as l,si as li,wc as ln,Wa as lr,hp as lt,Kh as m,_i as mi,sc as mn,Na as mr,Jd as mt,ug as n,fi as ni,Uc as nn,Oo as nr,Hp as nt,eg as o,li as oi,jc as on,go as or,mp as ot,qh as p,gi as pi,uc as pn,Pa as pr,tf as pt,Zp as q,nr as qi,Go as qn,Pi as qr,pl as qt,Qh as r,hi as ri,Vc as rn,Eo as rr,xp as rt,cg as s,ci as si,Ec as sn,io as sr,pp as st,lg as t,Zn as ta,bi as ti,Wc as tn,Po as tr,Ap as tt,tg as u,pi as ui,Cc as un,Va as ur,vp as ut,zh as v,Zr as vi,nc as vn,Sa as vr,Ud as vt,gh as w,ii as wi,Bs as wn,va as wr,qd as wt,Ih as x,ni as xi,Ys as xn,ma as xr,Kd as xt,Rh as y,ai as yi,$s as yn,Ca as yr,Yd as yt,vm as z,Tr as zi,us as zn,Li as zr,Bl as zt};