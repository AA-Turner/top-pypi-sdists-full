import{c as ae,j as re,R as t,C as oe,am as Pe,an as le,ao as Fe,u as z,ag as ie,ap as Re,B as P,aq as Me,m as q,n as se,M as Ne,aj as Ge,ar as R,as as Ke,at as ze,au as x,av as B,aw as qe,ax as Be,h as v,ay as Ue,az as je,a4 as Qe,aA as We,aB as I,aC as ce,r as U,aD as He,U as $e,a as Ve,b as Ye,i as Ze,aE as Je,aF as Xe,O as T,aG as et,aH as ue,aI as tt,aJ as nt,x as at,aa as rt,aK as ot,aL as lt,aM as it,aN as st,aO as ct,aP as ut,aQ as dt,aR as mt}from"./index-Cp-cdq7a.js";const ft=ae(re.jsx("path",{d:"M12 3c-4.97 0-9 4.03-9 9s4.03 9 9 9 9-4.03 9-9c0-.46-.04-.92-.1-1.36-.98 1.37-2.58 2.26-4.4 2.26-2.98 0-5.4-2.42-5.4-5.4 0-1.81.89-3.42 2.26-4.4-.44-.06-.9-.1-1.36-.1"}),"DarkMode"),gt=ae(re.jsx("path",{d:"M12 7c-2.76 0-5 2.24-5 5s2.24 5 5 5 5-2.24 5-5-2.24-5-5-5M2 13h2c.55 0 1-.45 1-1s-.45-1-1-1H2c-.55 0-1 .45-1 1s.45 1 1 1m18 0h2c.55 0 1-.45 1-1s-.45-1-1-1h-2c-.55 0-1 .45-1 1s.45 1 1 1M11 2v2c0 .55.45 1 1 1s1-.45 1-1V2c0-.55-.45-1-1-1s-1 .45-1 1m0 18v2c0 .55.45 1 1 1s1-.45 1-1v-2c0-.55-.45-1-1-1s-1 .45-1 1M5.99 4.58c-.39-.39-1.03-.39-1.41 0-.39.39-.39 1.03 0 1.41l1.06 1.06c.39.39 1.03.39 1.41 0s.39-1.03 0-1.41zm12.37 12.37c-.39-.39-1.03-.39-1.41 0-.39.39-.39 1.03 0 1.41l1.06 1.06c.39.39 1.03.39 1.41 0 .39-.39.39-1.03 0-1.41zm1.06-10.96c.39-.39.39-1.03 0-1.41-.39-.39-1.03-.39-1.41 0l-1.06 1.06c-.39.39-.39 1.03 0 1.41s1.03.39 1.41 0zM7.05 18.36c.39-.39.39-1.03 0-1.41-.39-.39-1.03-.39-1.41 0l-1.06 1.06c-.39.39-.39 1.03 0 1.41s1.03.39 1.41 0z"}),"LightMode"),pt={dev:"MrAGfUuvQq2FOJIgAgbwgjMQgRNgruRa",prod:"SjCRPH72QTHlVhFZIT5067V9rhuq80Dl"},de=5e3,yt=({link:a,message:l})=>{const d=z();return t.createElement(ie,{style:{color:d.text.primary},href:a},l,t.createElement(Re,{style:{height:"1rem",marginTop:4.5,marginLeft:1}}))},me={bottom:"50px !important",vertical:"bottom",horizontal:"center"},fe=({onClick:a})=>{const l=z();return t.createElement("div",null,t.createElement(P,{"data-cy":"btn-dismiss-alert",variant:"contained",size:"small",onClick:()=>{a()},sx:{marginLeft:"auto",backgroundColor:l.primary.main,color:l.text.primary,boxShadow:0}},"Dismiss"))};function ht(){const[a,l]=oe(Pe);return a.length?t.createElement(le,{duration:de,layout:me,message:t.createElement("div",{style:{width:"100%"}},a),onHandleClose:()=>l([]),primary:()=>t.createElement(fe,{onClick:()=>l([])})}):null}function vt(){const[a,l]=oe(Fe);return a?t.createElement(le,{duration:de,layout:me,message:t.createElement("div",{style:{width:"100%"}},t.createElement(yt,{...a})),onHandleClose:()=>l(null),primary:()=>t.createElement(fe,{onClick:()=>l(null)})}):null}function sn(){return t.createElement(t.Fragment,null,t.createElement(ht,null),t.createElement(vt,null))}const bt=`import fiftyone as fo

# Name of an existing dataset
name = "quickstart"

dataset = fo.load_dataset(name)

# Launch a new App session
session = fo.launch_app(dataset)

# If you already have an active App session
# session.dataset = dataset`,_t=`import fiftyone as fo

dataset = fo.load_dataset("$CURRENT_DATASET_NAME")

samples = []
for filepath, label in zip(filepaths, labels):
    sample = fo.Sample(filepath=filepath)
    sample["ground_truth"] = fo.Classification(label=label)
    samples.append(sample)

dataset.add_samples(samples)`,Et=`import fiftyone as fo

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
)`,wt={SELECT_DATASET:{title:"No dataset selected",code:bt,subtitle:"Select a dataset with dataset selector above or",codeTitle:"Select a dataset with code",codeSubtitle:"Use Python or command line tools to set dataset for the current session",learnMoreLink:"https://docs.voxel51.com/user_guide/app.html",learnMoreLabel:"about using the FiftyOne App"},ADD_SAMPLE:{title:"No samples yet",code:_t,subtitle:"Add samples to this dataset with code or",codeTitle:"Add samples with code",codeSubtitle:"Use Python or command line tools to add sample to this dataset",learnMoreLink:"https://docs.voxel51.com/user_guide/dataset_creation/index.html#custom-formats",learnMoreLabel:"about loading data into FiftyOne"},ADD_DATASET:{title:"No datasets yet",code:Et,subtitle:"Add a dataset to FiftyOne with code or",codeTitle:"Create dataset with code",codeSubtitle:"Use Python or command line tools to add dataset to FiftyOne",learnMoreLink:"https://docs.voxel51.com/user_guide/dataset_creation/index.html",learnMoreLabel:"about loading data into FiftyOne"}},Z="@voxel51/utils/create_dataset",J="@voxel51/io/import_samples",kt="https://github.com/voxel51/fiftyone-plugins/tree/main/plugins/utils",St="https://github.com/voxel51/fiftyone-plugins/tree/main/plugins/io",At="@voxel51/utils",xt="@voxel51/io";function cn(a){const{mode:l}=a,{isLoading:d}=Me(!0),c=q(se);if(!l)return null;if(d)return t.createElement(Ne,null,"Pixelating...");const{code:m,codeTitle:h,learnMoreLabel:y,learnMoreLink:s,title:g}=wt[l],f=m.replace("$CURRENT_DATASET_NAME",c),p=l==="SELECT_DATASET";return t.createElement(t.Fragment,null,t.createElement(Ge,null),t.createElement(R,{spacing:6,divider:t.createElement(Ke,{sx:{width:"100%"}}),sx:{fontWeight:"normal",alignItems:"center",width:"100%",py:8,overflow:"auto"},className:ze},t.createElement(R,{alignItems:"center",spacing:1},t.createElement(x,{sx:{fontSize:16}},g),p&&t.createElement(x,{color:"text.secondary"},"You can use the selector above to open an existing dataset"),t.createElement(Ct,{...a}),!p&&t.createElement(x,{color:"text.secondary"},t.createElement(B,{href:s,target:"_blank",sx:{textDecoration:"underline",":hover":{textDecoration:"none"}}},"Learn more")," ",y)),t.createElement(R,{alignItems:"center"},t.createElement(x,{sx:{fontSize:16}},h),t.createElement(x,{sx:{pb:2},color:"text.secondary"},"You can use Python to ",l==="ADD_DATASET"&&t.createElement(t.Fragment,null,t.createElement(K,{href:s,target:"_blank"},"load data")," into FiftyOne"),p&&t.createElement(t.Fragment,null,"load a dataset in the App"),l==="ADD_SAMPLE"&&t.createElement(t.Fragment,null,t.createElement(K,{href:s,target:"_blank"},"add samples")," to this dataset")),t.createElement(qe,{tabs:[{id:"python",label:"Python",code:f}]}))))}function Ct(a){const{mode:l}=a,d=Be(),c=l==="ADD_SAMPLE",m=v.useCallback(L=>Array.isArray(d.choices)?d.choices.some(D=>(D==null?void 0:D.value)===L):!1,[d]),h=v.useMemo(()=>c?!1:m(Z),[c,m]),y=v.useMemo(()=>c?m(J):!1,[c,m]),s=c?y:h,g=c?St:kt,f=c?xt:At,p=c?"add samples to this dataset":"create a new dataset",O=c?"add samples to datasets":"create datasets",C=c?J:Z;return t.createElement(x,{color:"text.secondary"},s?t.createElement(t.Fragment,null,t.createElement(Lt,{uri:C}),"to ",p):t.createElement(t.Fragment,null,"Did you know? You can ",O," in the App by installing the ",t.createElement(K,{href:g,target:"_blank"},f)," plugin"),", or ",t.createElement(ge,{onClick:d.toggle},"browse operations")," for other options")}function Lt(a){const{uri:l,prompt:d=!0}=a,c=Ue(),{execute:m}=je(l),h=v.useCallback(()=>{d?c(l):m({})},[d,c,l,m]);return t.createElement(ge,{onClick:h},"Click here")}function ge(a){return t.createElement(P,{...a,sx:{p:0,textTransform:"none",fontSize:"inherit",lineHeight:"inherit",verticalAlign:"baseline",color:l=>l.palette.text.primary,textDecoration:"underline",...(a==null?void 0:a.sx)||{}}})}function K(a){return t.createElement(B,{...a,sx:{textDecoration:"underline",":hover":{textDecoration:"none"},...(a==null?void 0:a.sx)||{}}})}const pe={argumentDefinitions:[],kind:"Fragment",metadata:null,name:"NavFragment",selections:[{args:null,kind:"FragmentSpread",name:"Analytics"},{args:null,kind:"FragmentSpread",name:"NavDatasets"}],type:"Query",abstractKey:null};pe.hash="b4c1e5cfb810c869d7f48d036fc48cad";const ye=function(){var a=[{defaultValue:null,kind:"LocalArgument",name:"count"},{defaultValue:null,kind:"LocalArgument",name:"cursor"},{defaultValue:null,kind:"LocalArgument",name:"search"}],l=[{kind:"Variable",name:"after",variableName:"cursor"},{kind:"Variable",name:"first",variableName:"count"},{kind:"Variable",name:"search",variableName:"search"}];return{fragment:{argumentDefinitions:a,kind:"Fragment",metadata:null,name:"DatasetsPaginationQuery",selections:[{args:null,kind:"FragmentSpread",name:"NavDatasets"}],type:"Query",abstractKey:null},kind:"Request",operation:{argumentDefinitions:a,kind:"Operation",name:"DatasetsPaginationQuery",selections:[{alias:null,args:l,concreteType:"DatasetStrConnection",kind:"LinkedField",name:"datasets",plural:!1,selections:[{alias:null,args:null,kind:"ScalarField",name:"total",storageKey:null},{alias:null,args:null,concreteType:"DatasetStrEdge",kind:"LinkedField",name:"edges",plural:!0,selections:[{alias:null,args:null,kind:"ScalarField",name:"cursor",storageKey:null},{alias:null,args:null,concreteType:"Dataset",kind:"LinkedField",name:"node",plural:!1,selections:[{alias:null,args:null,kind:"ScalarField",name:"name",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"id",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"__typename",storageKey:null}],storageKey:null}],storageKey:null},{alias:null,args:null,concreteType:"DatasetStrPageInfo",kind:"LinkedField",name:"pageInfo",plural:!1,selections:[{alias:null,args:null,kind:"ScalarField",name:"endCursor",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"hasNextPage",storageKey:null}],storageKey:null}],storageKey:null},{alias:null,args:l,filters:["search"],handle:"connection",key:"DatasetsList_query_datasets",kind:"LinkedHandle",name:"datasets"}]},params:{cacheID:"51829dc84906da9b415d984d01b4ef24",id:null,metadata:{},name:"DatasetsPaginationQuery",operationKind:"query",text:`query DatasetsPaginationQuery(
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
`}}}();ye.hash="c3d4960b5532b1af0f3fe881adf27805";const he=function(){var a=["datasets"];return{argumentDefinitions:[{kind:"RootArgument",name:"count"},{kind:"RootArgument",name:"cursor"},{kind:"RootArgument",name:"search"}],kind:"Fragment",metadata:{connection:[{count:"count",cursor:"cursor",direction:"forward",path:a}],refetch:{connection:{forward:{count:"count",cursor:"cursor"},backward:null,path:a},fragmentPathInResult:[],operation:ye}},name:"NavDatasets",selections:[{alias:"datasets",args:[{kind:"Variable",name:"search",variableName:"search"}],concreteType:"DatasetStrConnection",kind:"LinkedField",name:"__DatasetsList_query_datasets_connection",plural:!1,selections:[{alias:null,args:null,kind:"ScalarField",name:"total",storageKey:null},{alias:null,args:null,concreteType:"DatasetStrEdge",kind:"LinkedField",name:"edges",plural:!0,selections:[{alias:null,args:null,kind:"ScalarField",name:"cursor",storageKey:null},{alias:null,args:null,concreteType:"Dataset",kind:"LinkedField",name:"node",plural:!1,selections:[{alias:null,args:null,kind:"ScalarField",name:"name",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"__typename",storageKey:null}],storageKey:null}],storageKey:null},{alias:null,args:null,concreteType:"DatasetStrPageInfo",kind:"LinkedField",name:"pageInfo",plural:!1,selections:[{alias:null,args:null,kind:"ScalarField",name:"endCursor",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"hasNextPage",storageKey:null}],storageKey:null}],storageKey:null}],type:"Query",abstractKey:null}}();he.hash="c3d4960b5532b1af0f3fe881adf27805";function Tt(a,l){var d=v.useRef(!1),c=v.useRef(),m=v.useRef(a),h=v.useCallback(function(){return d.current},[]),y=v.useCallback(function(){d.current=!1,c.current&&clearTimeout(c.current),c.current=setTimeout(function(){d.current=!0,m.current()},l)},[l]),s=v.useCallback(function(){d.current=null,c.current&&clearTimeout(c.current)},[]);return v.useEffect(function(){m.current=a},[a]),v.useEffect(function(){return y(),s},[l]),[h,s,y]}function Ot(a,l,d){d===void 0&&(d=[]);var c=Tt(a,l),m=c[0],h=c[1],y=c[2];return v.useEffect(y,d),[m,h]}const ve={argumentDefinitions:[],kind:"Fragment",metadata:null,name:"Analytics",selections:[{alias:null,args:null,kind:"ScalarField",name:"context",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"dev",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"doNotTrack",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"uid",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"version",storageKey:null}],type:"Query",abstractKey:null};ve.hash="042d0c5e3b5c588fc852e8a26d260126";var be={},_e={},Ee={};(function(a){Object.defineProperty(a,"__esModule",{value:!0}),a.default=void 0;var l=function(){for(var m=arguments.length,h=new Array(m),y=0;y<m;y++)h[y]=arguments[y];if(typeof window<"u"){var s;typeof window.gtag>"u"&&(window.dataLayer=window.dataLayer||[],window.gtag=function(){window.dataLayer.push(arguments)}),(s=window).gtag.apply(s,h)}},d=l;a.default=d})(Ee);var we={};(function(a){Object.defineProperty(a,"__esModule",{value:!0}),a.default=y;var l=/^(a|an|and|as|at|but|by|en|for|if|in|nor|of|on|or|per|the|to|vs?\.?|via)$/i;function d(s){return s.toString().trim().replace(/[A-Za-z0-9\u00C0-\u00FF]+[^\s-]*/g,function(g,f,p){return f>0&&f+g.length!==p.length&&g.search(l)>-1&&p.charAt(f-2)!==":"&&(p.charAt(f+g.length)!=="-"||p.charAt(f-1)==="-")&&p.charAt(f-1).search(/[^\s-]/)<0?g.toLowerCase():g.substr(1).search(/[A-Z]|\../)>-1?g:g.charAt(0).toUpperCase()+g.substr(1)})}function c(s){return typeof s=="string"&&s.indexOf("@")!==-1}var m="REDACTED (Potential Email Address)";function h(s){return c(s)?(console.warn("This arg looks like an email address, redacting."),m):s}function y(){var s=arguments.length>0&&arguments[0]!==void 0?arguments[0]:"",g=arguments.length>1&&arguments[1]!==void 0?arguments[1]:!0,f=arguments.length>2&&arguments[2]!==void 0?arguments[2]:!0,p=s||"";return g&&(p=d(s)),f&&(p=h(p)),p}})(we);(function(a){Object.defineProperty(a,"__esModule",{value:!0}),a.default=a.GA4=void 0;var l=y(Ee),d=y(we),c=["eventCategory","eventAction","eventLabel","eventValue","hitType"],m=["title","location"],h=["page","hitType"];function y(o){return o&&o.__esModule?o:{default:o}}function s(o,e){if(o==null)return{};var n=g(o,e),r,i;if(Object.getOwnPropertySymbols){var u=Object.getOwnPropertySymbols(o);for(i=0;i<u.length;i++)r=u[i],!(e.indexOf(r)>=0)&&Object.prototype.propertyIsEnumerable.call(o,r)&&(n[r]=o[r])}return n}function g(o,e){if(o==null)return{};var n={},r=Object.keys(o),i,u;for(u=0;u<r.length;u++)i=r[u],!(e.indexOf(i)>=0)&&(n[i]=o[i]);return n}function f(o){"@babel/helpers - typeof";return f=typeof Symbol=="function"&&typeof Symbol.iterator=="symbol"?function(e){return typeof e}:function(e){return e&&typeof Symbol=="function"&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e},f(o)}function p(o){return L(o)||C(o)||Q(o)||O()}function O(){throw new TypeError(`Invalid attempt to spread non-iterable instance.
In order to be iterable, non-array objects must have a [Symbol.iterator]() method.`)}function C(o){if(typeof Symbol<"u"&&o[Symbol.iterator]!=null||o["@@iterator"]!=null)return Array.from(o)}function L(o){if(Array.isArray(o))return M(o)}function D(o,e){var n=Object.keys(o);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(o);e&&(r=r.filter(function(i){return Object.getOwnPropertyDescriptor(o,i).enumerable})),n.push.apply(n,r)}return n}function A(o){for(var e=1;e<arguments.length;e++){var n=arguments[e]!=null?arguments[e]:{};e%2?D(Object(n),!0).forEach(function(r){E(o,r,n[r])}):Object.getOwnPropertyDescriptors?Object.defineProperties(o,Object.getOwnPropertyDescriptors(n)):D(Object(n)).forEach(function(r){Object.defineProperty(o,r,Object.getOwnPropertyDescriptor(n,r))})}return o}function Se(o,e){return Ce(o)||xe(o,e)||Q(o,e)||Ae()}function Ae(){throw new TypeError(`Invalid attempt to destructure non-iterable instance.
In order to be iterable, non-array objects must have a [Symbol.iterator]() method.`)}function Q(o,e){if(o){if(typeof o=="string")return M(o,e);var n=Object.prototype.toString.call(o).slice(8,-1);if(n==="Object"&&o.constructor&&(n=o.constructor.name),n==="Map"||n==="Set")return Array.from(o);if(n==="Arguments"||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n))return M(o,e)}}function M(o,e){(e==null||e>o.length)&&(e=o.length);for(var n=0,r=new Array(e);n<e;n++)r[n]=o[n];return r}function xe(o,e){var n=o==null?null:typeof Symbol<"u"&&o[Symbol.iterator]||o["@@iterator"];if(n!=null){var r,i,u,b,_=[],w=!0,k=!1;try{if(u=(n=n.call(o)).next,e!==0)for(;!(w=(r=u.call(n)).done)&&(_.push(r.value),_.length!==e);w=!0);}catch(S){k=!0,i=S}finally{try{if(!w&&n.return!=null&&(b=n.return(),Object(b)!==b))return}finally{if(k)throw i}}return _}}function Ce(o){if(Array.isArray(o))return o}function Le(o,e){if(!(o instanceof e))throw new TypeError("Cannot call a class as a function")}function Te(o,e){for(var n=0;n<e.length;n++){var r=e[n];r.enumerable=r.enumerable||!1,r.configurable=!0,"value"in r&&(r.writable=!0),Object.defineProperty(o,W(r.key),r)}}function Oe(o,e,n){return e&&Te(o.prototype,e),Object.defineProperty(o,"prototype",{writable:!1}),o}function E(o,e,n){return e=W(e),e in o?Object.defineProperty(o,e,{value:n,enumerable:!0,configurable:!0,writable:!0}):o[e]=n,o}function W(o){var e=De(o,"string");return f(e)==="symbol"?e:String(e)}function De(o,e){if(f(o)!=="object"||o===null)return o;var n=o[Symbol.toPrimitive];if(n!==void 0){var r=n.call(o,e||"default");if(f(r)!=="object")return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return(e==="string"?String:Number)(o)}var H=function(){function o(){var e=this;Le(this,o),E(this,"reset",function(){e.isInitialized=!1,e._testMode=!1,e._currentMeasurementId,e._hasLoadedGA=!1,e._isQueuing=!1,e._queueGtag=[]}),E(this,"_gtag",function(){for(var n=arguments.length,r=new Array(n),i=0;i<n;i++)r[i]=arguments[i];e._testMode||e._isQueuing?e._queueGtag.push(r):l.default.apply(void 0,r)}),E(this,"_loadGA",function(n,r){var i=arguments.length>2&&arguments[2]!==void 0?arguments[2]:"https://www.googletagmanager.com/gtag/js";if(!(typeof window>"u"||typeof document>"u")&&!e._hasLoadedGA){var u=document.createElement("script");u.async=!0,u.src="".concat(i,"?id=").concat(n),r&&u.setAttribute("nonce",r),document.body.appendChild(u),window.dataLayer=window.dataLayer||[],window.gtag=function(){window.dataLayer.push(arguments)},e._hasLoadedGA=!0}}),E(this,"_toGtagOptions",function(n){if(n){var r={cookieUpdate:"cookie_update",cookieExpires:"cookie_expires",cookieDomain:"cookie_domain",cookieFlags:"cookie_flags",userId:"user_id",clientId:"client_id",anonymizeIp:"anonymize_ip",contentGroup1:"content_group1",contentGroup2:"content_group2",contentGroup3:"content_group3",contentGroup4:"content_group4",contentGroup5:"content_group5",allowAdFeatures:"allow_google_signals",allowAdPersonalizationSignals:"allow_ad_personalization_signals",nonInteraction:"non_interaction",page:"page_path",hitCallback:"event_callback"},i=Object.entries(n).reduce(function(u,b){var _=Se(b,2),w=_[0],k=_[1];return r[w]?u[r[w]]=k:u[w]=k,u},{});return i}}),E(this,"initialize",function(n){var r=arguments.length>1&&arguments[1]!==void 0?arguments[1]:{};if(!n)throw new Error("Require GA_MEASUREMENT_ID");var i=typeof n=="string"?[{trackingId:n}]:n;e._currentMeasurementId=i[0].trackingId;var u=r.gaOptions,b=r.gtagOptions,_=r.nonce,w=r.testMode,k=w===void 0?!1:w,S=r.gtagUrl;if(e._testMode=k,k||e._loadGA(e._currentMeasurementId,_,S),e.isInitialized||(e._gtag("js",new Date),i.forEach(function(F){var Y=A(A(A({},e._toGtagOptions(A(A({},u),F.gaOptions))),b),F.gtagOptions);Object.keys(Y).length?e._gtag("config",F.trackingId,Y):e._gtag("config",F.trackingId)})),e.isInitialized=!0,!k){var $=p(e._queueGtag);for(e._queueGtag=[],e._isQueuing=!1;$.length;){var V=$.shift();e._gtag.apply(e,p(V)),V[0]==="get"&&(e._isQueuing=!0)}}}),E(this,"set",function(n){if(!n){console.warn("`fieldsObject` is required in .set()");return}if(f(n)!=="object"){console.warn("Expected `fieldsObject` arg to be an Object");return}Object.keys(n).length===0&&console.warn("empty `fieldsObject` given to .set()"),e._gaCommand("set",n)}),E(this,"_gaCommandSendEvent",function(n,r,i,u,b){e._gtag("event",r,A(A({event_category:n,event_label:i,value:u},b&&{non_interaction:b.nonInteraction}),e._toGtagOptions(b)))}),E(this,"_gaCommandSendEventParameters",function(){for(var n=arguments.length,r=new Array(n),i=0;i<n;i++)r[i]=arguments[i];if(typeof r[0]=="string")e._gaCommandSendEvent.apply(e,p(r.slice(1)));else{var u=r[0],b=u.eventCategory,_=u.eventAction,w=u.eventLabel,k=u.eventValue;u.hitType;var S=s(u,c);e._gaCommandSendEvent(b,_,w,k,S)}}),E(this,"_gaCommandSendTiming",function(n,r,i,u){e._gtag("event","timing_complete",{name:r,value:i,event_category:n,event_label:u})}),E(this,"_gaCommandSendPageview",function(n,r){if(r&&Object.keys(r).length){var i=e._toGtagOptions(r),u=i.title,b=i.location,_=s(i,m);e._gtag("event","page_view",A(A(A(A({},n&&{page_path:n}),u&&{page_title:u}),b&&{page_location:b}),_))}else n?e._gtag("event","page_view",{page_path:n}):e._gtag("event","page_view")}),E(this,"_gaCommandSendPageviewParameters",function(){for(var n=arguments.length,r=new Array(n),i=0;i<n;i++)r[i]=arguments[i];if(typeof r[0]=="string")e._gaCommandSendPageview.apply(e,p(r.slice(1)));else{var u=r[0],b=u.page;u.hitType;var _=s(u,h);e._gaCommandSendPageview(b,_)}}),E(this,"_gaCommandSend",function(){for(var n=arguments.length,r=new Array(n),i=0;i<n;i++)r[i]=arguments[i];var u=typeof r[0]=="string"?r[0]:r[0].hitType;switch(u){case"event":e._gaCommandSendEventParameters.apply(e,r);break;case"pageview":e._gaCommandSendPageviewParameters.apply(e,r);break;case"timing":e._gaCommandSendTiming.apply(e,p(r.slice(1)));break;case"screenview":case"transaction":case"item":case"social":case"exception":console.warn("Unsupported send command: ".concat(u));break;default:console.warn("Send command doesn't exist: ".concat(u))}}),E(this,"_gaCommandSet",function(){for(var n=arguments.length,r=new Array(n),i=0;i<n;i++)r[i]=arguments[i];typeof r[0]=="string"&&(r[0]=E({},r[0],r[1])),e._gtag("set",e._toGtagOptions(r[0]))}),E(this,"_gaCommand",function(n){for(var r=arguments.length,i=new Array(r>1?r-1:0),u=1;u<r;u++)i[u-1]=arguments[u];switch(n){case"send":e._gaCommandSend.apply(e,i);break;case"set":e._gaCommandSet.apply(e,i);break;default:console.warn("Command doesn't exist: ".concat(n))}}),E(this,"ga",function(){for(var n=arguments.length,r=new Array(n),i=0;i<n;i++)r[i]=arguments[i];if(typeof r[0]=="string")e._gaCommand.apply(e,r);else{var u=r[0];e._gtag("get",e._currentMeasurementId,"client_id",function(b){e._isQueuing=!1;var _=e._queueGtag;for(u({get:function(S){return S==="clientId"?b:S==="trackingId"?e._currentMeasurementId:S==="apiVersion"?"1":void 0}});_.length;){var w=_.shift();e._gtag.apply(e,p(w))}}),e._isQueuing=!0}return e.ga}),E(this,"event",function(n,r){if(typeof n=="string")e._gtag("event",n,e._toGtagOptions(r));else{var i=n.action,u=n.category,b=n.label,_=n.value,w=n.nonInteraction,k=n.transport;if(!u||!i){console.warn("args.category AND args.action are required in event()");return}var S={hitType:"event",eventCategory:(0,d.default)(u),eventAction:(0,d.default)(i)};b&&(S.eventLabel=(0,d.default)(b)),typeof _<"u"&&(typeof _!="number"?console.warn("Expected `args.value` arg to be a Number."):S.eventValue=_),typeof w<"u"&&(typeof w!="boolean"?console.warn("`args.nonInteraction` must be a boolean."):S.nonInteraction=w),typeof k<"u"&&(typeof k!="string"?console.warn("`args.transport` must be a string."):(["beacon","xhr","image"].indexOf(k)===-1&&console.warn("`args.transport` must be either one of these values: `beacon`, `xhr` or `image`"),S.transport=k)),e._gaCommand("send",S)}}),E(this,"send",function(n){e._gaCommand("send",n)}),this.reset()}return Oe(o,[{key:"gtag",value:function(){this._gtag.apply(this,arguments)}}]),o}();a.GA4=H;var Ie=new H;a.default=Ie})(_e);(function(a){function l(s){"@babel/helpers - typeof";return l=typeof Symbol=="function"&&typeof Symbol.iterator=="symbol"?function(g){return typeof g}:function(g){return g&&typeof Symbol=="function"&&g.constructor===Symbol&&g!==Symbol.prototype?"symbol":typeof g},l(s)}Object.defineProperty(a,"__esModule",{value:!0}),a.default=a.ReactGAImplementation=void 0;var d=m(_e);function c(s){if(typeof WeakMap!="function")return null;var g=new WeakMap,f=new WeakMap;return(c=function(O){return O?f:g})(s)}function m(s,g){if(s&&s.__esModule)return s;if(s===null||l(s)!=="object"&&typeof s!="function")return{default:s};var f=c(g);if(f&&f.has(s))return f.get(s);var p={},O=Object.defineProperty&&Object.getOwnPropertyDescriptor;for(var C in s)if(C!=="default"&&Object.prototype.hasOwnProperty.call(s,C)){var L=O?Object.getOwnPropertyDescriptor(s,C):null;L&&(L.get||L.set)?Object.defineProperty(p,C,L):p[C]=s[C]}return p.default=s,f&&f.set(s,p),p}var h=d.GA4;a.ReactGAImplementation=h;var y=d.default;a.default=y})(be);const Dt=Qe(be),It={app_ids:{prod:"G-NT3FLN0QHF",dev:"G-7TMZEFFWB7"},dimensions:{dev:"dimension1",version:"dimension2",context:"dimension3"}},N="fiftyone-do-not-track";function Pt(a){const[l,d]=v.useState(!1),[c,m]=v.useState(!1),h=window.localStorage.getItem(N);v.useEffect(()=>{a||h==="true"||h==="false"?(m(!1),d(!0)):m(!0)},[a,h]);const y=v.useCallback(()=>{window.localStorage.setItem(N,"true"),m(!1),d(!0)},[]),s=v.useCallback(()=>{window.localStorage.setItem(N,"false"),d(!0),m(!1)},[]);return{doNotTrack:h==="true"||a,handleDisable:y,handleEnable:s,ready:l,show:c}}function Ft({callGA:a,info:l}){const[d,c]=We(),{doNotTrack:m,handleDisable:h,handleEnable:y,ready:s,show:g}=Pt(l.doNotTrack);return v.useEffect(()=>{if(!s)return;const f=l.dev?"dev":"prod",p=pt[f];c({userId:l.uid,userGroup:"fiftyone-oss",writeKey:p,doNotTrack:m,debug:l.dev}),!m&&a()},[a,m,l,s,c]),g?t.createElement(Rt,null,t.createElement(I,{container:!0,direction:"column",alignItems:"center",borderTop:f=>`1px solid ${f.palette.divider}`,backgroundColor:"background.paper"},t.createElement(I,{padding:2},t.createElement(x,{variant:"h6",marginBottom:1},"Help us improve FiftyOne"),t.createElement(x,{marginBottom:1},"We use cookies to understand how FiftyOne is used and improve the product. You can help us by enabling anonymous analytics."),t.createElement(I,{container:!0,gap:2,justifyContent:"end",direction:"row"},t.createElement(I,{item:!0,alignContent:"center"},t.createElement(B,{style:{cursor:"pointer"},onClick:h,"data-cy":"btn-disable-cookies"},"Disable")),t.createElement(I,{item:!0},t.createElement(P,{variant:"contained",onClick:y},"Enable")))))):null}function Rt({children:a}){return t.createElement(ce,{position:"fixed",bottom:0,width:"100%",zIndex:51},a)}const Mt=a=>v.useCallback(()=>{const d=a.dev?"dev":"prod";Dt.initialize(It.app_ids[d],{testMode:!1,gaOptions:{storage:"none",cookieDomain:"none",clientId:a.uid,page_location:"omitted",page_path:"omitted",version:a.version,context:a.context,checkProtocolTask:null}})},[a]);function Nt({fragment:a}){const l=U.useFragment(ve,a),d=Mt(l);return window.IS_PLAYWRIGHT?(console.log("Analytics component is disabled in playwright"),null):t.createElement(Ft,{callGA:d,info:l})}const Gt=({className:a,value:l})=>t.createElement("span",{className:a,title:l},l),Kt=({useSearch:a})=>{const l=He(),d=q(se);return t.createElement($e,{cy:"dataset",component:Gt,placeholder:"Select dataset",inputStyle:{height:40,maxWidth:300},containerStyle:{position:"relative"},onSelect:async c=>(l(c),c),overflow:!0,useSearch:a,value:d})};var j={},zt=Ze;Object.defineProperty(j,"__esModule",{value:!0});var ke=j.default=void 0,qt=zt(Ve()),Bt=Ye();ke=j.default=(0,qt.default)((0,Bt.jsx)("path",{d:"m19 9 1.25-2.75L23 5l-2.75-1.25L19 1l-1.25 2.75L15 5l2.75 1.25zm-7.5.5L9 4 6.5 9.5 1 12l5.5 2.5L9 20l2.5-5.5L17 12zM19 15l-1.25 2.75L15 19l2.75 1.25L19 23l1.25-2.75L23 19l-2.75-1.25z"}),"AutoAwesome");const X="fiftyone-enterprise-tooltip-seen",ee="fo-cta-enterprise-button",G="#333333",te="#FFFFFF",Ut="#FF6D04",jt="#B681FF",Qt=Je`
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
`,Wt=Xe`
  animation: ${Qt} 1.5s ease-in-out infinite;
`,Ht=T.div`
  display: flex;
  align-items: center;
  transition: all 0.3s ease;
`,ne=()=>t.createElement(t.Fragment,null,t.createElement("svg",{width:0,height:0,"aria-label":"Gradient","aria-labelledby":"gradient"},t.createElement("title",null,"Gradient"),t.createElement("defs",null,t.createElement("linearGradient",{id:"gradient1",x1:"0%",y1:"0%",x2:"100%",y2:"100%"},t.createElement("stop",{offset:"0%",style:{stopColor:Ut,stopOpacity:1}}),t.createElement("stop",{offset:"100%",style:{stopColor:jt,stopOpacity:1}})))),t.createElement(Ht,{className:"fo-teams-cta-pulse-animation"},t.createElement(ke,{sx:{fontSize:{xs:16,sm:20},mr:1,fill:"url(#gradient1)"}}))),$t=T.div`
  background-color: ${({bgColor:a})=>a};
  border-radius: 16px;

  &:hover {
    background-color: transparent;
  }
`,Vt=T(ie)`
  text-decoration: none;

  &:hover {
    text-decoration: none;
  }
`,Yt=T(et)`
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
  border: 1px solid ${({borderColor:a})=>a};
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
    width: ${({isLightMode:a})=>a?"150%":"100%"};
    height: 100%;
    background: linear-gradient(
      90deg,
      rgba(255, 255, 255, 0) 0%,
      rgba(255, 255, 255, ${({isLightMode:a})=>a?"0.3":"0.2"})
        50%,
      rgba(255, 255, 255, 0) 100%
    );
    transition: all ${({isLightMode:a})=>a?"0.8s":"0.6s"} ease;
    z-index: 1;
  }

  &:hover,
  &:focus,
  &:active {
    transform: scale(1.03);
    text-decoration: none;
    border: 1px solid ${({borderColor:a})=>a} !important;
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
            ${({isLightMode:a})=>a?"0.6":"0.2"}
          )
          50%,
        rgba(255, 255, 255, 0) 100%
      );
    }

    .fo-teams-cta-pulse-animation {
      ${Wt}
    }
  }
`,Zt=T(ce)`
  padding: 16px;
  width: 310px;
  position: relative;
  display: flex;
  flex-direction: column;
  gap: 12px;
`,Jt=T(x)`
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
  margin-bottom: 12px;
`,Xt=T(x)`
  position: relative;
  color: var(--fo-palette-text-secondary);
  font-size: 15px !important;
`,en=T(R)`
  margin-top: 16px;
`;function tn({disablePopover:a=!1}){const[l,d]=v.useState(!1),{mode:c}=ue(),m=z(),h=c==="light"?te:G;v.useEffect(()=>{const f=window.localStorage.getItem(X),p=window.IS_PLAYWRIGHT;!f&&!p&&d(!0)},[]);const y=v.useCallback(()=>{localStorage.setItem(X,"true")},[]),s=v.useCallback(()=>{y(),d(!1)},[y]),g=v.useCallback(()=>{y(),d(!1),window.open("https://voxel51.com/why-upgrade?utm_source=FiftyOneApp","_blank")},[y]);return t.createElement(t.Fragment,null,t.createElement($t,{bgColor:c==="light"?"transparent":h},t.createElement(Vt,{href:"https://voxel51.com/why-upgrade?utm_source=FiftyOneApp"},t.createElement(Yt,{borderColor:c==="dark"?G:m.divider,isLightMode:c==="light",id:ee},t.createElement(ne,null),"Explore Enterprise"))),l&&!a&&t.createElement(tt,{open:!0,anchorEl:document.getElementById(ee),onClose:s,anchorOrigin:{vertical:"bottom",horizontal:"center"},transformOrigin:{vertical:-12,horizontal:"center"},elevation:3},t.createElement(Zt,{style:{backgroundColor:c==="light"?te:G}},t.createElement(Jt,{variant:"h6"},t.createElement(ne,null),t.createElement(x,{variant:"h6",letterSpacing:.3},"Accelerate your workflow")),t.createElement(Xt,{variant:"body2"},"With FiftyOne Enterprise you can connect to your data lake, automate your data curation and model analysis tasks, securely collaborate with your team, and more."),t.createElement(en,{direction:"row",spacing:2},t.createElement(P,{variant:"contained",onClick:g,size:"large",sx:{boxShadow:"none"}},"Explore Enterprise"),t.createElement(P,{variant:"outlined",color:"secondary",onClick:s,size:"large",sx:{boxShadow:"none"}},"Dismiss")))))}const nn=a=>l=>{const d=q(mt),{data:c,refetch:m}=U.usePaginationFragment(he,a);return Ot(()=>{m({search:l})},200,[l,d]),v.useMemo(()=>({total:c.datasets.total===null?void 0:c.datasets.total,values:c.datasets.edges.map(h=>h.node.name)}),[c])},un=({children:a,fragment:l,hasDataset:d})=>{const c=U.useFragment(pe,l),m=nn(c),h=nt(),{mode:y,setMode:s}=ue(),g=at(rt);return t.createElement(t.Fragment,null,t.createElement(ot,{title:"FiftyOne",onRefresh:h,navChildren:t.createElement(Kt,{useSearch:m})},d&&t.createElement(v.Suspense,{fallback:t.createElement("div",{style:{flex:1}})},t.createElement(lt,null)),!d&&t.createElement("div",{style:{flex:1}}),t.createElement("div",{className:it},t.createElement(tn,null),t.createElement(st,{title:y==="dark"?"Light mode":"Dark mode",onClick:()=>{const f=y==="dark"?"light":"dark";s(f),g(f)},sx:{color:f=>f.palette.text.secondary,pr:0}},y==="dark"?t.createElement(gt,{color:"inherit"}):t.createElement(ft,null)),t.createElement(ct,null),t.createElement(ut,null),t.createElement(dt,null))),a,t.createElement(Nt,{fragment:c}))},an="_page_8fb7q_1",rn="_rest_8fb7q_8",on="_icons_8fb7q_13",dn={page:an,rest:rn,icons:on};export{un as N,cn as S,sn as a,dn as s};
