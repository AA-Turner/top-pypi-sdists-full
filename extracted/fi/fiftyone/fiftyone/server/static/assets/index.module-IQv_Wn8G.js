import{J as se,K as ce,R as t,S as Pe,L as z,M as Fe,N as q,O as Re,Q as Me,V as B,W as ue,X as Ne,Y as P,Z as Ge,$ as U,a0 as de,a1 as Ke,a2 as ze,a3 as R,a4 as qe,a5 as Be,a6 as x,a7 as j,a8 as Ue,a9 as je,e as v,aa as $e,ab as We,d as Qe,ac as He,ad as I,ae as me,af as Ve,r as $,ag as Ye,ah as Ze,ai as Je,aj as Xe,ak as et,al as tt,am as nt,an as T,ao as at,ap as fe,aq as rt,ar as ot,as as lt,at as it,au as st,av as ct,aw as ut,ax as dt,ay as mt,az as ft,aA as gt,aB as pt}from"./index-CaQ_cEQV.js";const yt=se(ce.jsx("path",{d:"M12 3c-4.97 0-9 4.03-9 9s4.03 9 9 9 9-4.03 9-9c0-.46-.04-.92-.1-1.36-.98 1.37-2.58 2.26-4.4 2.26-2.98 0-5.4-2.42-5.4-5.4 0-1.81.89-3.42 2.26-4.4-.44-.06-.9-.1-1.36-.1"}),"DarkMode"),ht=se(ce.jsx("path",{d:"M12 7c-2.76 0-5 2.24-5 5s2.24 5 5 5 5-2.24 5-5-2.24-5-5-5M2 13h2c.55 0 1-.45 1-1s-.45-1-1-1H2c-.55 0-1 .45-1 1s.45 1 1 1m18 0h2c.55 0 1-.45 1-1s-.45-1-1-1h-2c-.55 0-1 .45-1 1s.45 1 1 1M11 2v2c0 .55.45 1 1 1s1-.45 1-1V2c0-.55-.45-1-1-1s-1 .45-1 1m0 18v2c0 .55.45 1 1 1s1-.45 1-1v-2c0-.55-.45-1-1-1s-1 .45-1 1M5.99 4.58c-.39-.39-1.03-.39-1.41 0-.39.39-.39 1.03 0 1.41l1.06 1.06c.39.39 1.03.39 1.41 0s.39-1.03 0-1.41zm12.37 12.37c-.39-.39-1.03-.39-1.41 0-.39.39-.39 1.03 0 1.41l1.06 1.06c.39.39 1.03.39 1.41 0 .39-.39.39-1.03 0-1.41zm1.06-10.96c.39-.39.39-1.03 0-1.41-.39-.39-1.03-.39-1.41 0l-1.06 1.06c-.39.39-.39 1.03 0 1.41s1.03.39 1.41 0zM7.05 18.36c.39-.39.39-1.03 0-1.41-.39-.39-1.03-.39-1.41 0l-1.06 1.06c-.39.39-.39 1.03 0 1.41s1.03.39 1.41 0z"}),"LightMode"),vt={dev:"MrAGfUuvQq2FOJIgAgbwgjMQgRNgruRa",prod:"SjCRPH72QTHlVhFZIT5067V9rhuq80Dl"},W=5e3,bt=({link:n,message:l})=>{const d=B();return t.createElement(ue,{style:{color:d.text.primary},href:n},l,t.createElement(Ne,{style:{height:"1rem",marginTop:4.5,marginLeft:1}}))},Q={bottom:"50px !important",vertical:"bottom",horizontal:"center"},H=({onClick:n})=>{const l=B();return t.createElement("div",null,t.createElement(P,{"data-cy":"btn-dismiss-alert",variant:"contained",size:"small",onClick:()=>{n()},sx:{marginLeft:"auto",backgroundColor:l.primary.main,color:l.text.primary,boxShadow:0}},"Dismiss"))};function _t(){const[n,l]=z(Fe);return n.length?t.createElement(q,{duration:W,layout:Q,message:t.createElement("div",{style:{width:"100%"}},n),onHandleClose:()=>l([]),primary:()=>t.createElement(H,{onClick:()=>l([])})}):null}function Et(){const[n,l]=z(Re);return n?t.createElement(q,{duration:W,layout:Q,message:t.createElement("div",{style:{width:"100%"}},t.createElement(bt,{...n})),onHandleClose:()=>l(null),primary:()=>t.createElement(H,{onClick:()=>l(null)})}):null}function wt(){const[n,l]=z(Me);return n?t.createElement(q,{duration:W,layout:Q,message:t.createElement("div",{style:{width:"100%"}},n),onHandleClose:()=>l(null),primary:()=>t.createElement(H,{onClick:()=>l(null)})}):null}function fn(){return t.createElement(t.Fragment,null,t.createElement(_t,null),t.createElement(Et,null),t.createElement(wt,null),t.createElement(Pe,null))}const kt=`import fiftyone as fo

# Name of an existing dataset
name = "quickstart"

dataset = fo.load_dataset(name)

# Launch a new App session
session = fo.launch_app(dataset)

# If you already have an active App session
# session.dataset = dataset`,St=`import fiftyone as fo

dataset = fo.load_dataset("$CURRENT_DATASET_NAME")

samples = []
for filepath, label in zip(filepaths, labels):
    sample = fo.Sample(filepath=filepath)
    sample["ground_truth"] = fo.Classification(label=label)
    samples.append(sample)

dataset.add_samples(samples)`,At=`import fiftyone as fo

# A name for the dataset
name = "my-dataset"

# The directory containing the data to import
dataset_dir = "/path/to/data"

# The type of data being imported
dataset_type = fo.types.COCODetectionDataset

dataset = fo.Dataset.from_dir(
    dataset_dir=dataset_dir,
    dataset_type=dataset_type,
    name=name,
)`,xt={SELECT_DATASET:{title:"No dataset selected",code:kt,subtitle:"Select a dataset with dataset selector above or",codeTitle:"Select a dataset with code",codeSubtitle:"Use Python or command line tools to set dataset for the current session",learnMoreLink:"https://docs.voxel51.com/user_guide/app.html",learnMoreLabel:"about using the FiftyOne App"},ADD_SAMPLE:{title:"No samples yet",code:St,subtitle:"Add samples to this dataset with code or",codeTitle:"Add samples with code",codeSubtitle:"Use Python or command line tools to add sample to this dataset",learnMoreLink:"https://docs.voxel51.com/user_guide/dataset_creation/index.html#custom-formats",learnMoreLabel:"about loading data into FiftyOne"},ADD_DATASET:{title:"No datasets yet",code:At,subtitle:"Add a dataset to FiftyOne with code or",codeTitle:"Create dataset with code",codeSubtitle:"Use Python or command line tools to add dataset to FiftyOne",learnMoreLink:"https://docs.voxel51.com/user_guide/dataset_creation/index.html",learnMoreLabel:"about loading data into FiftyOne"}},ne="@voxel51/utils/create_dataset",ae="@voxel51/io/import_samples",Ct="https://github.com/voxel51/fiftyone-plugins/tree/main/plugins/utils",Lt="https://github.com/voxel51/fiftyone-plugins/tree/main/plugins/io",Tt="@voxel51/utils",Ot="@voxel51/io";function gn(n){const{mode:l}=n,{isLoading:d}=Ge(!0),c=U(de);if(!l)return null;if(d)return t.createElement(Ke,null,"Pixelating...");const{code:m,codeTitle:h,learnMoreLabel:y,learnMoreLink:s,title:g}=xt[l],f=m.replace("$CURRENT_DATASET_NAME",c),p=l==="SELECT_DATASET";return t.createElement(t.Fragment,null,t.createElement(ze,null),t.createElement(R,{spacing:6,divider:t.createElement(qe,{sx:{width:"100%"}}),sx:{fontWeight:"normal",alignItems:"center",width:"100%",py:8,overflow:"auto"},className:Be},t.createElement(R,{alignItems:"center",spacing:1},t.createElement(x,{sx:{fontSize:16}},g),p&&t.createElement(x,{color:"text.secondary"},"You can use the selector above to open an existing dataset"),t.createElement(Dt,{...n}),!p&&t.createElement(x,{color:"text.secondary"},t.createElement(j,{href:s,target:"_blank",sx:{textDecoration:"underline",":hover":{textDecoration:"none"}}},"Learn more")," ",y)),t.createElement(R,{alignItems:"center"},t.createElement(x,{sx:{fontSize:16}},h),t.createElement(x,{sx:{pb:2},color:"text.secondary"},"You can use Python to ",l==="ADD_DATASET"&&t.createElement(t.Fragment,null,t.createElement(K,{href:s,target:"_blank"},"load data")," into FiftyOne"),p&&t.createElement(t.Fragment,null,"load a dataset in the App"),l==="ADD_SAMPLE"&&t.createElement(t.Fragment,null,t.createElement(K,{href:s,target:"_blank"},"add samples")," to this dataset")),t.createElement(Ue,{tabs:[{id:"python",label:"Python",code:f}]}))))}function Dt(n){const{mode:l}=n,d=je(),c=l==="ADD_SAMPLE",m=v.useCallback(L=>Array.isArray(d.choices)?d.choices.some(D=>(D==null?void 0:D.value)===L):!1,[d]),h=v.useMemo(()=>c?!1:m(ne),[c,m]),y=v.useMemo(()=>c?m(ae):!1,[c,m]),s=c?y:h,g=c?Lt:Ct,f=c?Ot:Tt,p=c?"add samples to this dataset":"create a new dataset",O=c?"add samples to datasets":"create datasets",C=c?ae:ne;return t.createElement(x,{color:"text.secondary"},s?t.createElement(t.Fragment,null,t.createElement(It,{uri:C}),"to ",p):t.createElement(t.Fragment,null,"Did you know? You can ",O," in the App by installing the ",t.createElement(K,{href:g,target:"_blank"},f)," plugin"),", or ",t.createElement(ge,{onClick:d.toggle},"browse operations")," for other options")}function It(n){const{uri:l,prompt:d=!0}=n,c=$e(),{execute:m}=We(l),h=v.useCallback(()=>{d?c(l):m({})},[d,c,l,m]);return t.createElement(ge,{onClick:h},"Click here")}function ge(n){return t.createElement(P,{...n,sx:{p:0,textTransform:"none",fontSize:"inherit",lineHeight:"inherit",verticalAlign:"baseline",color:l=>l.palette.text.primary,textDecoration:"underline",...(n==null?void 0:n.sx)||{}}})}function K(n){return t.createElement(j,{...n,sx:{textDecoration:"underline",":hover":{textDecoration:"none"},...(n==null?void 0:n.sx)||{}}})}const pe={argumentDefinitions:[],kind:"Fragment",metadata:null,name:"NavFragment",selections:[{args:null,kind:"FragmentSpread",name:"Analytics"},{args:null,kind:"FragmentSpread",name:"NavDatasets"}],type:"Query",abstractKey:null};pe.hash="b4c1e5cfb810c869d7f48d036fc48cad";const ye=function(){var n=[{defaultValue:null,kind:"LocalArgument",name:"count"},{defaultValue:null,kind:"LocalArgument",name:"cursor"},{defaultValue:null,kind:"LocalArgument",name:"search"}],l=[{kind:"Variable",name:"after",variableName:"cursor"},{kind:"Variable",name:"first",variableName:"count"},{kind:"Variable",name:"search",variableName:"search"}];return{fragment:{argumentDefinitions:n,kind:"Fragment",metadata:null,name:"DatasetsPaginationQuery",selections:[{args:null,kind:"FragmentSpread",name:"NavDatasets"}],type:"Query",abstractKey:null},kind:"Request",operation:{argumentDefinitions:n,kind:"Operation",name:"DatasetsPaginationQuery",selections:[{alias:null,args:l,concreteType:"DatasetStrConnection",kind:"LinkedField",name:"datasets",plural:!1,selections:[{alias:null,args:null,kind:"ScalarField",name:"total",storageKey:null},{alias:null,args:null,concreteType:"DatasetStrEdge",kind:"LinkedField",name:"edges",plural:!0,selections:[{alias:null,args:null,kind:"ScalarField",name:"cursor",storageKey:null},{alias:null,args:null,concreteType:"Dataset",kind:"LinkedField",name:"node",plural:!1,selections:[{alias:null,args:null,kind:"ScalarField",name:"name",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"id",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"__typename",storageKey:null}],storageKey:null}],storageKey:null},{alias:null,args:null,concreteType:"DatasetStrPageInfo",kind:"LinkedField",name:"pageInfo",plural:!1,selections:[{alias:null,args:null,kind:"ScalarField",name:"endCursor",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"hasNextPage",storageKey:null}],storageKey:null}],storageKey:null},{alias:null,args:l,filters:["search"],handle:"connection",key:"DatasetsList_query_datasets",kind:"LinkedHandle",name:"datasets"}]},params:{cacheID:"51829dc84906da9b415d984d01b4ef24",id:null,metadata:{},name:"DatasetsPaginationQuery",operationKind:"query",text:`query DatasetsPaginationQuery(
  $count: Int
  $cursor: String
  $search: String
) {
  ...NavDatasets
}

fragment NavDatasets on Query {
  datasets(search: $search, first: $count, after: $cursor) {
    total
    edges {
      cursor
      node {
        name
        id
        __typename
      }
    }
    pageInfo {
      endCursor
      hasNextPage
    }
  }
}
`}}}();ye.hash="c3d4960b5532b1af0f3fe881adf27805";const he=function(){var n=["datasets"];return{argumentDefinitions:[{kind:"RootArgument",name:"count"},{kind:"RootArgument",name:"cursor"},{kind:"RootArgument",name:"search"}],kind:"Fragment",metadata:{connection:[{count:"count",cursor:"cursor",direction:"forward",path:n}],refetch:{connection:{forward:{count:"count",cursor:"cursor"},backward:null,path:n},fragmentPathInResult:[],operation:ye}},name:"NavDatasets",selections:[{alias:"datasets",args:[{kind:"Variable",name:"search",variableName:"search"}],concreteType:"DatasetStrConnection",kind:"LinkedField",name:"__DatasetsList_query_datasets_connection",plural:!1,selections:[{alias:null,args:null,kind:"ScalarField",name:"total",storageKey:null},{alias:null,args:null,concreteType:"DatasetStrEdge",kind:"LinkedField",name:"edges",plural:!0,selections:[{alias:null,args:null,kind:"ScalarField",name:"cursor",storageKey:null},{alias:null,args:null,concreteType:"Dataset",kind:"LinkedField",name:"node",plural:!1,selections:[{alias:null,args:null,kind:"ScalarField",name:"name",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"__typename",storageKey:null}],storageKey:null}],storageKey:null},{alias:null,args:null,concreteType:"DatasetStrPageInfo",kind:"LinkedField",name:"pageInfo",plural:!1,selections:[{alias:null,args:null,kind:"ScalarField",name:"endCursor",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"hasNextPage",storageKey:null}],storageKey:null}],storageKey:null}],type:"Query",abstractKey:null}}();he.hash="c3d4960b5532b1af0f3fe881adf27805";function Pt(n,l){var d=v.useRef(!1),c=v.useRef(),m=v.useRef(n),h=v.useCallback(function(){return d.current},[]),y=v.useCallback(function(){d.current=!1,c.current&&clearTimeout(c.current),c.current=setTimeout(function(){d.current=!0,m.current()},l)},[l]),s=v.useCallback(function(){d.current=null,c.current&&clearTimeout(c.current)},[]);return v.useEffect(function(){m.current=n},[n]),v.useEffect(function(){return y(),s},[l]),[h,s,y]}function Ft(n,l,d){d===void 0&&(d=[]);var c=Pt(n,l),m=c[0],h=c[1],y=c[2];return v.useEffect(y,d),[m,h]}const ve={argumentDefinitions:[],kind:"Fragment",metadata:null,name:"Analytics",selections:[{alias:null,args:null,kind:"ScalarField",name:"context",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"dev",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"doNotTrack",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"uid",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"version",storageKey:null}],type:"Query",abstractKey:null};ve.hash="042d0c5e3b5c588fc852e8a26d260126";var be={},_e={},Ee={};(function(n){Object.defineProperty(n,"__esModule",{value:!0}),n.default=void 0;var l=function(){for(var m=arguments.length,h=new Array(m),y=0;y<m;y++)h[y]=arguments[y];if(typeof window<"u"){var s;typeof window.gtag>"u"&&(window.dataLayer=window.dataLayer||[],window.gtag=function(){window.dataLayer.push(arguments)}),(s=window).gtag.apply(s,h)}},d=l;n.default=d})(Ee);var we={};(function(n){Object.defineProperty(n,"__esModule",{value:!0}),n.default=y;var l=/^(a|an|and|as|at|but|by|en|for|if|in|nor|of|on|or|per|the|to|vs?\.?|via)$/i;function d(s){return s.toString().trim().replace(/[A-Za-z0-9\u00C0-\u00FF]+[^\s-]*/g,function(g,f,p){return f>0&&f+g.length!==p.length&&g.search(l)>-1&&p.charAt(f-2)!==":"&&(p.charAt(f+g.length)!=="-"||p.charAt(f-1)==="-")&&p.charAt(f-1).search(/[^\s-]/)<0?g.toLowerCase():g.substr(1).search(/[A-Z]|\../)>-1?g:g.charAt(0).toUpperCase()+g.substr(1)})}function c(s){return typeof s=="string"&&s.indexOf("@")!==-1}var m="REDACTED (Potential Email Address)";function h(s){return c(s)?(console.warn("This arg looks like an email address, redacting."),m):s}function y(){var s=arguments.length>0&&arguments[0]!==void 0?arguments[0]:"",g=arguments.length>1&&arguments[1]!==void 0?arguments[1]:!0,f=arguments.length>2&&arguments[2]!==void 0?arguments[2]:!0,p=s||"";return g&&(p=d(s)),f&&(p=h(p)),p}})(we);(function(n){Object.defineProperty(n,"__esModule",{value:!0}),n.default=n.GA4=void 0;var l=y(Ee),d=y(we),c=["eventCategory","eventAction","eventLabel","eventValue","hitType"],m=["title","location"],h=["page","hitType"];function y(o){return o&&o.__esModule?o:{default:o}}function s(o,e){if(o==null)return{};var a=g(o,e),r,i;if(Object.getOwnPropertySymbols){var u=Object.getOwnPropertySymbols(o);for(i=0;i<u.length;i++)r=u[i],!(e.indexOf(r)>=0)&&Object.prototype.propertyIsEnumerable.call(o,r)&&(a[r]=o[r])}return a}function g(o,e){if(o==null)return{};var a={},r=Object.keys(o),i,u;for(u=0;u<r.length;u++)i=r[u],!(e.indexOf(i)>=0)&&(a[i]=o[i]);return a}function f(o){"@babel/helpers - typeof";return f=typeof Symbol=="function"&&typeof Symbol.iterator=="symbol"?function(e){return typeof e}:function(e){return e&&typeof Symbol=="function"&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e},f(o)}function p(o){return L(o)||C(o)||Y(o)||O()}function O(){throw new TypeError(`Invalid attempt to spread non-iterable instance.
In order to be iterable, non-array objects must have a [Symbol.iterator]() method.`)}function C(o){if(typeof Symbol<"u"&&o[Symbol.iterator]!=null||o["@@iterator"]!=null)return Array.from(o)}function L(o){if(Array.isArray(o))return M(o)}function D(o,e){var a=Object.keys(o);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(o);e&&(r=r.filter(function(i){return Object.getOwnPropertyDescriptor(o,i).enumerable})),a.push.apply(a,r)}return a}function A(o){for(var e=1;e<arguments.length;e++){var a=arguments[e]!=null?arguments[e]:{};e%2?D(Object(a),!0).forEach(function(r){E(o,r,a[r])}):Object.getOwnPropertyDescriptors?Object.defineProperties(o,Object.getOwnPropertyDescriptors(a)):D(Object(a)).forEach(function(r){Object.defineProperty(o,r,Object.getOwnPropertyDescriptor(a,r))})}return o}function Se(o,e){return Ce(o)||xe(o,e)||Y(o,e)||Ae()}function Ae(){throw new TypeError(`Invalid attempt to destructure non-iterable instance.
In order to be iterable, non-array objects must have a [Symbol.iterator]() method.`)}function Y(o,e){if(o){if(typeof o=="string")return M(o,e);var a=Object.prototype.toString.call(o).slice(8,-1);if(a==="Object"&&o.constructor&&(a=o.constructor.name),a==="Map"||a==="Set")return Array.from(o);if(a==="Arguments"||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(a))return M(o,e)}}function M(o,e){(e==null||e>o.length)&&(e=o.length);for(var a=0,r=new Array(e);a<e;a++)r[a]=o[a];return r}function xe(o,e){var a=o==null?null:typeof Symbol<"u"&&o[Symbol.iterator]||o["@@iterator"];if(a!=null){var r,i,u,b,_=[],w=!0,k=!1;try{if(u=(a=a.call(o)).next,e!==0)for(;!(w=(r=u.call(a)).done)&&(_.push(r.value),_.length!==e);w=!0);}catch(S){k=!0,i=S}finally{try{if(!w&&a.return!=null&&(b=a.return(),Object(b)!==b))return}finally{if(k)throw i}}return _}}function Ce(o){if(Array.isArray(o))return o}function Le(o,e){if(!(o instanceof e))throw new TypeError("Cannot call a class as a function")}function Te(o,e){for(var a=0;a<e.length;a++){var r=e[a];r.enumerable=r.enumerable||!1,r.configurable=!0,"value"in r&&(r.writable=!0),Object.defineProperty(o,Z(r.key),r)}}function Oe(o,e,a){return e&&Te(o.prototype,e),Object.defineProperty(o,"prototype",{writable:!1}),o}function E(o,e,a){return e=Z(e),e in o?Object.defineProperty(o,e,{value:a,enumerable:!0,configurable:!0,writable:!0}):o[e]=a,o}function Z(o){var e=De(o,"string");return f(e)==="symbol"?e:String(e)}function De(o,e){if(f(o)!=="object"||o===null)return o;var a=o[Symbol.toPrimitive];if(a!==void 0){var r=a.call(o,e||"default");if(f(r)!=="object")return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return(e==="string"?String:Number)(o)}var J=function(){function o(){var e=this;Le(this,o),E(this,"reset",function(){e.isInitialized=!1,e._testMode=!1,e._currentMeasurementId,e._hasLoadedGA=!1,e._isQueuing=!1,e._queueGtag=[]}),E(this,"_gtag",function(){for(var a=arguments.length,r=new Array(a),i=0;i<a;i++)r[i]=arguments[i];e._testMode||e._isQueuing?e._queueGtag.push(r):l.default.apply(void 0,r)}),E(this,"_loadGA",function(a,r){var i=arguments.length>2&&arguments[2]!==void 0?arguments[2]:"https://www.googletagmanager.com/gtag/js";if(!(typeof window>"u"||typeof document>"u")&&!e._hasLoadedGA){var u=document.createElement("script");u.async=!0,u.src="".concat(i,"?id=").concat(a),r&&u.setAttribute("nonce",r),document.body.appendChild(u),window.dataLayer=window.dataLayer||[],window.gtag=function(){window.dataLayer.push(arguments)},e._hasLoadedGA=!0}}),E(this,"_toGtagOptions",function(a){if(a){var r={cookieUpdate:"cookie_update",cookieExpires:"cookie_expires",cookieDomain:"cookie_domain",cookieFlags:"cookie_flags",userId:"user_id",clientId:"client_id",anonymizeIp:"anonymize_ip",contentGroup1:"content_group1",contentGroup2:"content_group2",contentGroup3:"content_group3",contentGroup4:"content_group4",contentGroup5:"content_group5",allowAdFeatures:"allow_google_signals",allowAdPersonalizationSignals:"allow_ad_personalization_signals",nonInteraction:"non_interaction",page:"page_path",hitCallback:"event_callback"},i=Object.entries(a).reduce(function(u,b){var _=Se(b,2),w=_[0],k=_[1];return r[w]?u[r[w]]=k:u[w]=k,u},{});return i}}),E(this,"initialize",function(a){var r=arguments.length>1&&arguments[1]!==void 0?arguments[1]:{};if(!a)throw new Error("Require GA_MEASUREMENT_ID");var i=typeof a=="string"?[{trackingId:a}]:a;e._currentMeasurementId=i[0].trackingId;var u=r.gaOptions,b=r.gtagOptions,_=r.nonce,w=r.testMode,k=w===void 0?!1:w,S=r.gtagUrl;if(e._testMode=k,k||e._loadGA(e._currentMeasurementId,_,S),e.isInitialized||(e._gtag("js",new Date),i.forEach(function(F){var te=A(A(A({},e._toGtagOptions(A(A({},u),F.gaOptions))),b),F.gtagOptions);Object.keys(te).length?e._gtag("config",F.trackingId,te):e._gtag("config",F.trackingId)})),e.isInitialized=!0,!k){var X=p(e._queueGtag);for(e._queueGtag=[],e._isQueuing=!1;X.length;){var ee=X.shift();e._gtag.apply(e,p(ee)),ee[0]==="get"&&(e._isQueuing=!0)}}}),E(this,"set",function(a){if(!a){console.warn("`fieldsObject` is required in .set()");return}if(f(a)!=="object"){console.warn("Expected `fieldsObject` arg to be an Object");return}Object.keys(a).length===0&&console.warn("empty `fieldsObject` given to .set()"),e._gaCommand("set",a)}),E(this,"_gaCommandSendEvent",function(a,r,i,u,b){e._gtag("event",r,A(A({event_category:a,event_label:i,value:u},b&&{non_interaction:b.nonInteraction}),e._toGtagOptions(b)))}),E(this,"_gaCommandSendEventParameters",function(){for(var a=arguments.length,r=new Array(a),i=0;i<a;i++)r[i]=arguments[i];if(typeof r[0]=="string")e._gaCommandSendEvent.apply(e,p(r.slice(1)));else{var u=r[0],b=u.eventCategory,_=u.eventAction,w=u.eventLabel,k=u.eventValue;u.hitType;var S=s(u,c);e._gaCommandSendEvent(b,_,w,k,S)}}),E(this,"_gaCommandSendTiming",function(a,r,i,u){e._gtag("event","timing_complete",{name:r,value:i,event_category:a,event_label:u})}),E(this,"_gaCommandSendPageview",function(a,r){if(r&&Object.keys(r).length){var i=e._toGtagOptions(r),u=i.title,b=i.location,_=s(i,m);e._gtag("event","page_view",A(A(A(A({},a&&{page_path:a}),u&&{page_title:u}),b&&{page_location:b}),_))}else a?e._gtag("event","page_view",{page_path:a}):e._gtag("event","page_view")}),E(this,"_gaCommandSendPageviewParameters",function(){for(var a=arguments.length,r=new Array(a),i=0;i<a;i++)r[i]=arguments[i];if(typeof r[0]=="string")e._gaCommandSendPageview.apply(e,p(r.slice(1)));else{var u=r[0],b=u.page;u.hitType;var _=s(u,h);e._gaCommandSendPageview(b,_)}}),E(this,"_gaCommandSend",function(){for(var a=arguments.length,r=new Array(a),i=0;i<a;i++)r[i]=arguments[i];var u=typeof r[0]=="string"?r[0]:r[0].hitType;switch(u){case"event":e._gaCommandSendEventParameters.apply(e,r);break;case"pageview":e._gaCommandSendPageviewParameters.apply(e,r);break;case"timing":e._gaCommandSendTiming.apply(e,p(r.slice(1)));break;case"screenview":case"transaction":case"item":case"social":case"exception":console.warn("Unsupported send command: ".concat(u));break;default:console.warn("Send command doesn't exist: ".concat(u))}}),E(this,"_gaCommandSet",function(){for(var a=arguments.length,r=new Array(a),i=0;i<a;i++)r[i]=arguments[i];typeof r[0]=="string"&&(r[0]=E({},r[0],r[1])),e._gtag("set",e._toGtagOptions(r[0]))}),E(this,"_gaCommand",function(a){for(var r=arguments.length,i=new Array(r>1?r-1:0),u=1;u<r;u++)i[u-1]=arguments[u];switch(a){case"send":e._gaCommandSend.apply(e,i);break;case"set":e._gaCommandSet.apply(e,i);break;default:console.warn("Command doesn't exist: ".concat(a))}}),E(this,"ga",function(){for(var a=arguments.length,r=new Array(a),i=0;i<a;i++)r[i]=arguments[i];if(typeof r[0]=="string")e._gaCommand.apply(e,r);else{var u=r[0];e._gtag("get",e._currentMeasurementId,"client_id",function(b){e._isQueuing=!1;var _=e._queueGtag;for(u({get:function(S){return S==="clientId"?b:S==="trackingId"?e._currentMeasurementId:S==="apiVersion"?"1":void 0}});_.length;){var w=_.shift();e._gtag.apply(e,p(w))}}),e._isQueuing=!0}return e.ga}),E(this,"event",function(a,r){if(typeof a=="string")e._gtag("event",a,e._toGtagOptions(r));else{var i=a.action,u=a.category,b=a.label,_=a.value,w=a.nonInteraction,k=a.transport;if(!u||!i){console.warn("args.category AND args.action are required in event()");return}var S={hitType:"event",eventCategory:(0,d.default)(u),eventAction:(0,d.default)(i)};b&&(S.eventLabel=(0,d.default)(b)),typeof _<"u"&&(typeof _!="number"?console.warn("Expected `args.value` arg to be a Number."):S.eventValue=_),typeof w<"u"&&(typeof w!="boolean"?console.warn("`args.nonInteraction` must be a boolean."):S.nonInteraction=w),typeof k<"u"&&(typeof k!="string"?console.warn("`args.transport` must be a string."):(["beacon","xhr","image"].indexOf(k)===-1&&console.warn("`args.transport` must be either one of these values: `beacon`, `xhr` or `image`"),S.transport=k)),e._gaCommand("send",S)}}),E(this,"send",function(a){e._gaCommand("send",a)}),this.reset()}return Oe(o,[{key:"gtag",value:function(){this._gtag.apply(this,arguments)}}]),o}();n.GA4=J;var Ie=new J;n.default=Ie})(_e);(function(n){function l(s){"@babel/helpers - typeof";return l=typeof Symbol=="function"&&typeof Symbol.iterator=="symbol"?function(g){return typeof g}:function(g){return g&&typeof Symbol=="function"&&g.constructor===Symbol&&g!==Symbol.prototype?"symbol":typeof g},l(s)}Object.defineProperty(n,"__esModule",{value:!0}),n.default=n.ReactGAImplementation=void 0;var d=m(_e);function c(s){if(typeof WeakMap!="function")return null;var g=new WeakMap,f=new WeakMap;return(c=function(O){return O?f:g})(s)}function m(s,g){if(s&&s.__esModule)return s;if(s===null||l(s)!=="object"&&typeof s!="function")return{default:s};var f=c(g);if(f&&f.has(s))return f.get(s);var p={},O=Object.defineProperty&&Object.getOwnPropertyDescriptor;for(var C in s)if(C!=="default"&&Object.prototype.hasOwnProperty.call(s,C)){var L=O?Object.getOwnPropertyDescriptor(s,C):null;L&&(L.get||L.set)?Object.defineProperty(p,C,L):p[C]=s[C]}return p.default=s,f&&f.set(s,p),p}var h=d.GA4;n.ReactGAImplementation=h;var y=d.default;n.default=y})(be);const Rt=Qe(be),Mt={app_ids:{prod:"G-NT3FLN0QHF",dev:"G-7TMZEFFWB7"},dimensions:{dev:"dimension1",version:"dimension2",context:"dimension3"}},N="fiftyone-do-not-track";function Nt(n){const[l,d]=v.useState(!1),[c,m]=v.useState(!1),h=window.localStorage.getItem(N);v.useEffect(()=>{n||h==="true"||h==="false"?(m(!1),d(!0)):(m(!0),d(!0))},[n,h]);const y=v.useCallback(()=>{window.localStorage.setItem(N,"true"),m(!1),d(!0)},[]),s=v.useCallback(()=>{window.localStorage.setItem(N,"false"),m(!1),d(!0)},[]);return{doNotTrack:h==="true"||n,handleDisable:y,handleAllow:s,ready:l,show:c}}function Gt({callGA:n,info:l}){const[d,c]=He(),{doNotTrack:m,handleDisable:h,handleAllow:y,ready:s,show:g}=Nt(l.doNotTrack);return v.useEffect(()=>{if(!s)return;const f=l.dev?"dev":"prod",p=vt[f];c({userId:l.uid,userGroup:"fiftyone-oss",writeKey:p,doNotTrack:m,debug:l.dev}),!m&&n()},[n,m,l,s,c]),g?t.createElement(Kt,null,t.createElement(zt,null),t.createElement(I,{container:!0,direction:"column",alignItems:"center",sx:{borderTop:f=>`1px solid ${f.palette.divider}`,backgroundColor:"background.paper"}},t.createElement(I,{padding:2},t.createElement(x,{variant:"h6",marginBottom:1},"Help us improve FiftyOne"),t.createElement(x,{marginBottom:1},"We use cookies to understand how FiftyOne is used and improve the product. You can help us by allowing anonymous analytics."),t.createElement(I,{container:!0,gap:2,justifyContent:"end",direction:"row"},t.createElement(I,{item:!0,alignContent:"center"},t.createElement(j,{style:{cursor:"pointer"},onClick:h,"data-cy":"btn-disable-cookies"},"Disable")),t.createElement(I,{item:!0},t.createElement(P,{variant:"contained",onClick:y},"Allow")))))):null}function Kt({children:n}){return t.createElement(me,{position:"fixed",bottom:0,width:"100%",zIndex:51},n)}function zt(){const n=Ve();return v.useEffect(()=>{n("analytics-consent-shown")},[n]),null}const qt=n=>v.useCallback(()=>{const d=n.dev?"dev":"prod";Rt.initialize(Mt.app_ids[d],{testMode:!1,gaOptions:{storage:"none",cookieDomain:"none",clientId:n.uid,page_location:"omitted",page_path:"omitted",version:n.version,context:n.context,checkProtocolTask:null}})},[n]);function Bt({fragment:n}){const l=$.useFragment(ve,n),d=qt(l);return window.IS_PLAYWRIGHT?(console.log("Analytics component is disabled in playwright"),null):t.createElement(Gt,{callGA:d,info:l})}const Ut=({className:n,value:l})=>t.createElement("span",{className:n,title:l},l),jt=({useSearch:n})=>{const l=Ye(),d=U(de);return t.createElement(Ze,{cy:"dataset",component:Ut,placeholder:"Select dataset",inputStyle:{height:40,maxWidth:300},containerStyle:{position:"relative"},onSelect:async c=>(l(c),c),overflow:!0,useSearch:n,value:d})};var V={},$t=et;Object.defineProperty(V,"__esModule",{value:!0});var ke=V.default=void 0,Wt=$t(Je()),Qt=Xe();ke=V.default=(0,Wt.default)((0,Qt.jsx)("path",{d:"m19 9 1.25-2.75L23 5l-2.75-1.25L19 1l-1.25 2.75L15 5l2.75 1.25zm-7.5.5L9 4 6.5 9.5 1 12l5.5 2.5L9 20l2.5-5.5L17 12zM19 15l-1.25 2.75L15 19l2.75 1.25L19 23l1.25-2.75L23 19l-2.75-1.25z"}),"AutoAwesome");const re="fiftyone-enterprise-tooltip-seen",oe="fo-cta-enterprise-button",G="#333333",le="#FFFFFF",Ht="#FF6D04",Vt="#B681FF",Yt=tt`
  0% {
    transform: scale(1);
    opacity: 1;
  }
  50% {
    transform: scale(1.1);
    opacity: 0.9;
  }
  100% {
    transform: scale(1);
    opacity: 1;
  }
`,Zt=nt`
  animation: ${Yt} 1.5s ease-in-out infinite;
`,Jt=T.div`
  display: flex;
  align-items: center;
  transition: all 0.3s ease;
`,ie=()=>t.createElement(t.Fragment,null,t.createElement("svg",{width:0,height:0,"aria-label":"Gradient","aria-labelledby":"gradient"},t.createElement("title",null,"Gradient"),t.createElement("defs",null,t.createElement("linearGradient",{id:"gradient1",x1:"0%",y1:"0%",x2:"100%",y2:"100%"},t.createElement("stop",{offset:"0%",style:{stopColor:Ht,stopOpacity:1}}),t.createElement("stop",{offset:"100%",style:{stopColor:Vt,stopOpacity:1}})))),t.createElement(Jt,{className:"fo-teams-cta-pulse-animation"},t.createElement(ke,{sx:{fontSize:{xs:16,sm:20},mr:1,fill:"url(#gradient1)"}}))),Xt=T.div`
  background-color: ${({$bgColor:n})=>n};
  border-radius: 16px;

  &:hover {
    background-color: transparent;
  }
`,en=T(ue)`
  text-decoration: none;

  &:hover {
    text-decoration: none;
  }
`,tn=T(at)`
  background: linear-gradient(45deg, #ff6d04 0%, #b681ff 100%);
  background-clip: text;
  -webkit-background-clip: text;
  text-fill-color: transparent;
  -webkit-text-fill-color: transparent;
  display: flex;
  align-items: center;
  gap: 2px;
  padding: 6px 12px;
  border-radius: 16px;
  font-weight: 500;
  text-transform: none;
  transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  text-decoration: none;
  font-size: 16px;
  position: relative;
  overflow: hidden;
  border: 1px solid ${({$borderColor:n})=>n};
  outline: none;
  box-shadow: none;

  @media (max-width: 767px) {
    font-size: 14px;
    padding: 4px 10px;
  }

  &:before {
    content: "";
    position: absolute;
    top: 0;
    left: -100%;
    width: ${({$isLightMode:n})=>n?"150%":"100%"};
    height: 100%;
    background: linear-gradient(
      90deg,
      rgba(255, 255, 255, 0) 0%,
      rgba(255, 255, 255, ${({$isLightMode:n})=>n?"0.3":"0.2"})
        50%,
      rgba(255, 255, 255, 0) 100%
    );
    transition: all ${({$isLightMode:n})=>n?"0.8s":"0.6s"} ease;
    z-index: 1;
  }

  &:hover,
  &:focus,
  &:active {
    transform: scale(1.03);
    text-decoration: none;
    border: 1px solid ${({$borderColor:n})=>n} !important;
    outline: none;
    box-shadow: none;

    background: linear-gradient(45deg, #ff6d04 0%, #b681ff 100%) !important;
    background-clip: text !important;
    -webkit-background-clip: text !important;
    text-fill-color: transparent !important;
    -webkit-text-fill-color: transparent !important;

    &:before {
      left: 100%;
      background: linear-gradient(
        90deg,
        rgba(255, 255, 255, 0) 0%,
        rgba(
            255,
            255,
            255,
            ${({isLightMode:n})=>n?"0.6":"0.2"}
          )
          50%,
        rgba(255, 255, 255, 0) 100%
      );
    }

    .fo-teams-cta-pulse-animation {
      ${Zt}
    }
  }
`,nn=T(me)`
  padding: 16px;
  width: 310px;
  position: relative;
  display: flex;
  flex-direction: column;
  gap: 12px;
`,an=T(x)`
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
  margin-bottom: 12px;
`,rn=T(x)`
  position: relative;
  color: var(--fo-palette-text-secondary);
  font-size: 15px !important;
`,on=T(R)`
  margin-top: 16px;
`;function ln({disablePopover:n=!1}){const[l,d]=v.useState(!1),{mode:c}=fe(),m=B(),h=c==="light"?le:G;v.useEffect(()=>{const f=window.localStorage.getItem(re),p=window.IS_PLAYWRIGHT;!f&&!p&&d(!0)},[]);const y=v.useCallback(()=>{localStorage.setItem(re,"true")},[]),s=v.useCallback(()=>{y(),d(!1)},[y]),g=v.useCallback(()=>{y(),d(!1),window.open("https://voxel51.com/why-upgrade?utm_source=FiftyOneApp","_blank")},[y]);return t.createElement(t.Fragment,null,t.createElement(Xt,{$bgColor:c==="light"?"transparent":h},t.createElement(en,{href:"https://voxel51.com/why-upgrade?utm_source=FiftyOneApp"},t.createElement(tn,{$borderColor:c==="dark"?G:m.divider,$isLightMode:c==="light",id:oe},t.createElement(ie,null),"Explore Enterprise"))),l&&!n&&t.createElement(rt,{open:!0,anchorEl:document.getElementById(oe),onClose:s,anchorOrigin:{vertical:"bottom",horizontal:"center"},transformOrigin:{vertical:-12,horizontal:"center"},elevation:3},t.createElement(nn,{style:{backgroundColor:c==="light"?le:G}},t.createElement(an,{variant:"h6"},t.createElement(ie,null),t.createElement(x,{variant:"h6",letterSpacing:.3},"Accelerate your workflow")),t.createElement(rn,{variant:"body2"},"With FiftyOne Enterprise you can connect to your data lake, automate your data curation and model analysis tasks, securely collaborate with your team, and more."),t.createElement(on,{direction:"row",spacing:2},t.createElement(P,{variant:"contained",onClick:g,size:"large",sx:{boxShadow:"none"}},"Explore Enterprise"),t.createElement(P,{variant:"outlined",color:"secondary",onClick:s,size:"large",sx:{boxShadow:"none"}},"Dismiss")))))}const sn=n=>l=>{const d=U(pt),{data:c,refetch:m}=$.usePaginationFragment(he,n);return Ft(()=>{m({search:l})},200,[l,d]),v.useMemo(()=>({total:c.datasets.total===null?void 0:c.datasets.total,values:c.datasets.edges.map(h=>h.node.name)}),[c])},pn=({children:n,fragment:l,hasDataset:d})=>{const c=$.useFragment(pe,l),m=sn(c),h=ot(),{mode:y,setMode:s}=fe(),g=lt(it);return t.createElement(t.Fragment,null,t.createElement(st,{title:"FiftyOne",onRefresh:h,navChildren:t.createElement(jt,{useSearch:m})},d&&t.createElement(v.Suspense,{fallback:t.createElement("div",{style:{flex:1}})},t.createElement(ct,null)),!d&&t.createElement("div",{style:{flex:1}}),t.createElement("div",{className:ut},t.createElement(ln,null),t.createElement(dt,{title:y==="dark"?"Light mode":"Dark mode",onClick:()=>{const f=y==="dark"?"light":"dark";s(f),g(f)},sx:{color:f=>f.palette.text.secondary,pr:0}},y==="dark"?t.createElement(ht,{color:"inherit"}):t.createElement(yt,null)),t.createElement(mt,null),t.createElement(ft,null),t.createElement(gt,null))),n,t.createElement(Bt,{fragment:c}))},cn="_page_8fb7q_1",un="_rest_8fb7q_8",dn="_icons_8fb7q_13",yn={page:cn,rest:un,icons:dn};export{pn as N,gn as S,fn as a,yn as s};
