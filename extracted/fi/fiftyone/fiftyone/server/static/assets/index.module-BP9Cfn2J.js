import{h as be,j as t,b9 as Ge,ba as H,bb as Ne,bc as W,bd as Ke,be as qe,o as Q,aj as I,bf as ve,bg as ze,bh as Be,R as V,ar as xe,L as Ue,bi as He,bj as R,bk as We,aG as j,bl as Y,bm as Qe,bn as Ve,bo as Ye,bp as $e,bq as Ze,br as Je,bs as D,aF as $,bt as _e,r as Z,bu as Xe,S as et,bv as tt,bw as nt,bx as at,by as we,bz as rt,z as T,bA as ot,bB as st,bC as it,bD as lt,av as ct,bE as ut,bF as dt,bG as ft,bH as gt,bI as mt,bJ as pt,bK as ht,bL as yt,G as bt,H as vt,bM as xt}from"./index-UVEqhvqJ.js";import{r as b}from"./recharts-P5Vx6n6Z.js";import{g as ke}from"./plotly-CX4VOiKt.js";const _t=be(t.jsx("path",{d:"M12 3c-4.97 0-9 4.03-9 9s4.03 9 9 9 9-4.03 9-9c0-.46-.04-.92-.1-1.36-.98 1.37-2.58 2.26-4.4 2.26-2.98 0-5.4-2.42-5.4-5.4 0-1.81.89-3.42 2.26-4.4-.44-.06-.9-.1-1.36-.1"}),"DarkMode"),wt=be(t.jsx("path",{d:"M12 7c-2.76 0-5 2.24-5 5s2.24 5 5 5 5-2.24 5-5-2.24-5-5-5M2 13h2c.55 0 1-.45 1-1s-.45-1-1-1H2c-.55 0-1 .45-1 1s.45 1 1 1m18 0h2c.55 0 1-.45 1-1s-.45-1-1-1h-2c-.55 0-1 .45-1 1s.45 1 1 1M11 2v2c0 .55.45 1 1 1s1-.45 1-1V2c0-.55-.45-1-1-1s-1 .45-1 1m0 18v2c0 .55.45 1 1 1s1-.45 1-1v-2c0-.55-.45-1-1-1s-1 .45-1 1M5.99 4.58c-.39-.39-1.03-.39-1.41 0-.39.39-.39 1.03 0 1.41l1.06 1.06c.39.39 1.03.39 1.41 0s.39-1.03 0-1.41zm12.37 12.37c-.39-.39-1.03-.39-1.41 0-.39.39-.39 1.03 0 1.41l1.06 1.06c.39.39 1.03.39 1.41 0 .39-.39.39-1.03 0-1.41zm1.06-10.96c.39-.39.39-1.03 0-1.41-.39-.39-1.03-.39-1.41 0l-1.06 1.06c-.39.39-.39 1.03 0 1.41s1.03.39 1.41 0zM7.05 18.36c.39-.39.39-1.03 0-1.41-.39-.39-1.03-.39-1.41 0l-1.06 1.06c-.39.39-.39 1.03 0 1.41s1.03.39 1.41 0z"}),"LightMode"),kt={dev:"MrAGfUuvQq2FOJIgAgbwgjMQgRNgruRa",prod:"SjCRPH72QTHlVhFZIT5067V9rhuq80Dl"},J=5e3,St=({link:n,message:s})=>{const u=Q();return t.jsxs(ve,{style:{color:u.text.primary},href:n,children:[s,t.jsx(ze,{style:{height:"1rem",marginTop:4.5,marginLeft:1}})]})},X={bottom:"50px !important",vertical:"bottom",horizontal:"center"},ee=({onClick:n})=>{const s=Q();return t.jsx("div",{children:t.jsx(I,{"data-cy":"btn-dismiss-alert",variant:"contained",size:"small",onClick:()=>{n()},sx:{marginLeft:"auto",backgroundColor:s.primary.main,color:s.text.primary,boxShadow:0},children:"Dismiss"})})};function At(){const[n,s]=H(Ne);return n.length?t.jsx(W,{duration:J,layout:X,message:t.jsx("div",{style:{width:"100%"},children:n}),onHandleClose:()=>s([]),primary:()=>t.jsx(ee,{onClick:()=>s([])})}):null}function jt(){const[n,s]=H(Ke);return n?t.jsx(W,{duration:J,layout:X,message:t.jsx("div",{style:{width:"100%"},children:t.jsx(St,{...n})}),onHandleClose:()=>s(null),primary:()=>t.jsx(ee,{onClick:()=>s(null)})}):null}function Ct(){const[n,s]=H(qe);return n?t.jsx(W,{duration:J,layout:X,message:t.jsx("div",{style:{width:"100%"},children:n}),onHandleClose:()=>s(null),primary:()=>t.jsx(ee,{onClick:()=>s(null)})}):null}function kn(){return t.jsxs(t.Fragment,{children:[t.jsx(At,{}),t.jsx(jt,{}),t.jsx(Ct,{}),t.jsx(Ge,{})]})}const Lt=`import fiftyone as fo

# Name of an existing dataset
name = "quickstart"

dataset = fo.load_dataset(name)

# Launch a new App session
session = fo.launch_app(dataset)

# If you already have an active App session
# session.dataset = dataset`,Tt=`import fiftyone as fo

dataset = fo.load_dataset("$CURRENT_DATASET_NAME")

samples = []
for filepath, label in zip(filepaths, labels):
    sample = fo.Sample(filepath=filepath)
    sample["ground_truth"] = fo.Classification(label=label)
    samples.append(sample)

dataset.add_samples(samples)`,Ot=`import fiftyone as fo

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
)`,Dt={SELECT_DATASET:{title:"No dataset selected",code:Lt,subtitle:"Select a dataset with dataset selector above or",codeTitle:"Select a dataset with code",codeSubtitle:"Use Python or command line tools to set dataset for the current session",learnMoreLink:"https://docs.voxel51.com/user_guide/app.html",learnMoreLabel:"about using the FiftyOne App"},ADD_SAMPLE:{title:"No samples yet",code:Tt,subtitle:"Add samples to this dataset with code or",codeTitle:"Add samples with code",codeSubtitle:"Use Python or command line tools to add sample to this dataset",learnMoreLink:"https://docs.voxel51.com/user_guide/dataset_creation/index.html#custom-formats",learnMoreLabel:"about loading data into FiftyOne"},ADD_DATASET:{title:"No datasets yet",code:Ot,subtitle:"Add a dataset to FiftyOne with code or",codeTitle:"Create dataset with code",codeSubtitle:"Use Python or command line tools to add dataset to FiftyOne",learnMoreLink:"https://docs.voxel51.com/user_guide/dataset_creation/index.html",learnMoreLabel:"about loading data into FiftyOne"}},ie="@voxel51/utils/create_dataset",le="@voxel51/io/import_samples",Et="https://github.com/voxel51/fiftyone-plugins/tree/main/plugins/utils",It="https://github.com/voxel51/fiftyone-plugins/tree/main/plugins/io",Pt="@voxel51/utils",Ft="@voxel51/io";function Sn(n){const{mode:s}=n,{isLoading:u}=Be(!0),c=V(xe);if(!s)return null;if(u)return t.jsx(Ue,{children:"Pixelating..."});const{code:g,codeTitle:y,learnMoreLabel:h,learnMoreLink:l,title:p}=Dt[s],m=g.replace("$CURRENT_DATASET_NAME",c),f=s==="SELECT_DATASET";return t.jsxs(t.Fragment,{children:[t.jsx(He,{}),t.jsxs(R,{spacing:6,divider:t.jsx(Ve,{sx:{width:"100%"}}),sx:{fontWeight:"normal",alignItems:"center",width:"100%",py:8,overflow:"auto"},className:We,children:[t.jsxs(R,{alignItems:"center",spacing:1,children:[t.jsx(j,{sx:{fontSize:16},children:p}),f&&t.jsx(j,{color:"text.secondary",children:"You can use the selector above to open an existing dataset"}),t.jsx(Rt,{...n}),!f&&t.jsxs(j,{color:"text.secondary",children:[t.jsx(Y,{href:l,target:"_blank",sx:{textDecoration:"underline",":hover":{textDecoration:"none"}},children:"Learn more"})," ",h]})]}),t.jsxs(R,{alignItems:"center",children:[t.jsx(j,{sx:{fontSize:16},children:y}),t.jsxs(j,{sx:{pb:2},color:"text.secondary",children:["You can use Python to ",s==="ADD_DATASET"&&t.jsxs(t.Fragment,{children:[t.jsx(U,{href:l,target:"_blank",children:"load data"})," into FiftyOne"]}),f&&t.jsx(t.Fragment,{children:"load a dataset in the App"}),s==="ADD_SAMPLE"&&t.jsxs(t.Fragment,{children:[t.jsx(U,{href:l,target:"_blank",children:"add samples"})," to this dataset"]})]}),t.jsx(Qe,{tabs:[{id:"python",label:"Python",code:m}]})]})]})]})}function Rt(n){const{mode:s}=n,u=Ye(),c=s==="ADD_SAMPLE",g=b.useCallback(L=>Array.isArray(u.choices)?u.choices.some(P=>P?.value===L):!1,[u]),y=b.useMemo(()=>c?!1:g(ie),[c,g]),h=b.useMemo(()=>c?g(le):!1,[c,g]),l=c?h:y,p=c?It:Et,m=c?Ft:Pt,f=c?"add samples to this dataset":"create a new dataset",O=c?"add samples to datasets":"create datasets",C=c?le:ie;return t.jsxs(j,{color:"text.secondary",children:[l?t.jsxs(t.Fragment,{children:[t.jsx(Mt,{uri:C}),"to ",f]}):t.jsxs(t.Fragment,{children:["Did you know? You can ",O," in the App by installing the ",t.jsx(U,{href:p,target:"_blank",children:m})," plugin"]}),", or ",t.jsx(Se,{onClick:u.toggle,children:"browse operations"})," for other options"]})}function Mt(n){const{uri:s,prompt:u=!0}=n,c=$e(),{execute:g}=Ze(s),y=b.useCallback(()=>{u?c(s):g({})},[u,c,s,g]);return t.jsx(Se,{onClick:y,children:"Click here"})}function Se(n){return t.jsx(I,{...n,sx:{p:0,textTransform:"none",fontSize:"inherit",lineHeight:"inherit",verticalAlign:"baseline",color:s=>s.palette.text.primary,textDecoration:"underline",...n?.sx||{}}})}function U(n){return t.jsx(Y,{...n,sx:{textDecoration:"underline",":hover":{textDecoration:"none"},...n?.sx||{}}})}const Ae={argumentDefinitions:[],kind:"Fragment",metadata:null,name:"NavFragment",selections:[{args:null,kind:"FragmentSpread",name:"Analytics"},{args:null,kind:"FragmentSpread",name:"NavDatasets"}],type:"Query",abstractKey:null};Ae.hash="b4c1e5cfb810c869d7f48d036fc48cad";const je=(function(){var n=[{defaultValue:null,kind:"LocalArgument",name:"count"},{defaultValue:null,kind:"LocalArgument",name:"cursor"},{defaultValue:null,kind:"LocalArgument",name:"search"}],s=[{kind:"Variable",name:"after",variableName:"cursor"},{kind:"Variable",name:"first",variableName:"count"},{kind:"Variable",name:"search",variableName:"search"}];return{fragment:{argumentDefinitions:n,kind:"Fragment",metadata:null,name:"DatasetsPaginationQuery",selections:[{args:null,kind:"FragmentSpread",name:"NavDatasets"}],type:"Query",abstractKey:null},kind:"Request",operation:{argumentDefinitions:n,kind:"Operation",name:"DatasetsPaginationQuery",selections:[{alias:null,args:s,concreteType:"DatasetStrConnection",kind:"LinkedField",name:"datasets",plural:!1,selections:[{alias:null,args:null,kind:"ScalarField",name:"total",storageKey:null},{alias:null,args:null,concreteType:"DatasetStrEdge",kind:"LinkedField",name:"edges",plural:!0,selections:[{alias:null,args:null,kind:"ScalarField",name:"cursor",storageKey:null},{alias:null,args:null,concreteType:"Dataset",kind:"LinkedField",name:"node",plural:!1,selections:[{alias:null,args:null,kind:"ScalarField",name:"name",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"id",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"__typename",storageKey:null}],storageKey:null}],storageKey:null},{alias:null,args:null,concreteType:"DatasetStrPageInfo",kind:"LinkedField",name:"pageInfo",plural:!1,selections:[{alias:null,args:null,kind:"ScalarField",name:"endCursor",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"hasNextPage",storageKey:null}],storageKey:null}],storageKey:null},{alias:null,args:s,filters:["search"],handle:"connection",key:"DatasetsList_query_datasets",kind:"LinkedHandle",name:"datasets"}]},params:{cacheID:"51829dc84906da9b415d984d01b4ef24",id:null,metadata:{},name:"DatasetsPaginationQuery",operationKind:"query",text:`query DatasetsPaginationQuery(
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
`}}})();je.hash="c3d4960b5532b1af0f3fe881adf27805";const Ce=(function(){var n=["datasets"];return{argumentDefinitions:[{kind:"RootArgument",name:"count"},{kind:"RootArgument",name:"cursor"},{kind:"RootArgument",name:"search"}],kind:"Fragment",metadata:{connection:[{count:"count",cursor:"cursor",direction:"forward",path:n}],refetch:{connection:{forward:{count:"count",cursor:"cursor"},backward:null,path:n},fragmentPathInResult:[],operation:je}},name:"NavDatasets",selections:[{alias:"datasets",args:[{kind:"Variable",name:"search",variableName:"search"}],concreteType:"DatasetStrConnection",kind:"LinkedField",name:"__DatasetsList_query_datasets_connection",plural:!1,selections:[{alias:null,args:null,kind:"ScalarField",name:"total",storageKey:null},{alias:null,args:null,concreteType:"DatasetStrEdge",kind:"LinkedField",name:"edges",plural:!0,selections:[{alias:null,args:null,kind:"ScalarField",name:"cursor",storageKey:null},{alias:null,args:null,concreteType:"Dataset",kind:"LinkedField",name:"node",plural:!1,selections:[{alias:null,args:null,kind:"ScalarField",name:"name",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"__typename",storageKey:null}],storageKey:null}],storageKey:null},{alias:null,args:null,concreteType:"DatasetStrPageInfo",kind:"LinkedField",name:"pageInfo",plural:!1,selections:[{alias:null,args:null,kind:"ScalarField",name:"endCursor",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"hasNextPage",storageKey:null}],storageKey:null}],storageKey:null}],type:"Query",abstractKey:null}})();Ce.hash="c3d4960b5532b1af0f3fe881adf27805";function Gt(n,s){var u=b.useRef(!1),c=b.useRef(),g=b.useRef(n),y=b.useCallback(function(){return u.current},[]),h=b.useCallback(function(){u.current=!1,c.current&&clearTimeout(c.current),c.current=setTimeout(function(){u.current=!0,g.current()},s)},[s]),l=b.useCallback(function(){u.current=null,c.current&&clearTimeout(c.current)},[]);return b.useEffect(function(){g.current=n},[n]),b.useEffect(function(){return h(),l},[s]),[y,l,h]}function Nt(n,s,u){u===void 0&&(u=[]);var c=Gt(n,s),g=c[0],y=c[1],h=c[2];return b.useEffect(h,u),[g,y]}const Le={argumentDefinitions:[],kind:"Fragment",metadata:null,name:"Analytics",selections:[{alias:null,args:null,kind:"ScalarField",name:"context",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"dev",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"doNotTrack",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"uid",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"version",storageKey:null}],type:"Query",abstractKey:null};Le.hash="042d0c5e3b5c588fc852e8a26d260126";var G={},N={},K={},ce;function Kt(){return ce||(ce=1,(function(n){Object.defineProperty(n,"__esModule",{value:!0}),n.default=void 0;var s=function(){for(var g=arguments.length,y=new Array(g),h=0;h<g;h++)y[h]=arguments[h];if(typeof window<"u"){var l;typeof window.gtag>"u"&&(window.dataLayer=window.dataLayer||[],window.gtag=function(){window.dataLayer.push(arguments)}),(l=window).gtag.apply(l,y)}},u=s;n.default=u})(K)),K}var q={},ue;function qt(){return ue||(ue=1,(function(n){Object.defineProperty(n,"__esModule",{value:!0}),n.default=h;var s=/^(a|an|and|as|at|but|by|en|for|if|in|nor|of|on|or|per|the|to|vs?\.?|via)$/i;function u(l){return l.toString().trim().replace(/[A-Za-z0-9\u00C0-\u00FF]+[^\s-]*/g,function(p,m,f){return m>0&&m+p.length!==f.length&&p.search(s)>-1&&f.charAt(m-2)!==":"&&(f.charAt(m+p.length)!=="-"||f.charAt(m-1)==="-")&&f.charAt(m-1).search(/[^\s-]/)<0?p.toLowerCase():p.substr(1).search(/[A-Z]|\../)>-1?p:p.charAt(0).toUpperCase()+p.substr(1)})}function c(l){return typeof l=="string"&&l.indexOf("@")!==-1}var g="REDACTED (Potential Email Address)";function y(l){return c(l)?(console.warn("This arg looks like an email address, redacting."),g):l}function h(){var l=arguments.length>0&&arguments[0]!==void 0?arguments[0]:"",p=arguments.length>1&&arguments[1]!==void 0?arguments[1]:!0,m=arguments.length>2&&arguments[2]!==void 0?arguments[2]:!0,f=l||"";return p&&(f=u(l)),m&&(f=y(f)),f}})(q)),q}var de;function zt(){return de||(de=1,(function(n){Object.defineProperty(n,"__esModule",{value:!0}),n.default=n.GA4=void 0;var s=h(Kt()),u=h(qt()),c=["eventCategory","eventAction","eventLabel","eventValue","hitType"],g=["title","location"],y=["page","hitType"];function h(o){return o&&o.__esModule?o:{default:o}}function l(o,e){if(o==null)return{};var a=p(o,e),r,i;if(Object.getOwnPropertySymbols){var d=Object.getOwnPropertySymbols(o);for(i=0;i<d.length;i++)r=d[i],!(e.indexOf(r)>=0)&&Object.prototype.propertyIsEnumerable.call(o,r)&&(a[r]=o[r])}return a}function p(o,e){if(o==null)return{};var a={},r=Object.keys(o),i,d;for(d=0;d<r.length;d++)i=r[d],!(e.indexOf(i)>=0)&&(a[i]=o[i]);return a}function m(o){"@babel/helpers - typeof";return m=typeof Symbol=="function"&&typeof Symbol.iterator=="symbol"?function(e){return typeof e}:function(e){return e&&typeof Symbol=="function"&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e},m(o)}function f(o){return L(o)||C(o)||te(o)||O()}function O(){throw new TypeError(`Invalid attempt to spread non-iterable instance.
In order to be iterable, non-array objects must have a [Symbol.iterator]() method.`)}function C(o){if(typeof Symbol<"u"&&o[Symbol.iterator]!=null||o["@@iterator"]!=null)return Array.from(o)}function L(o){if(Array.isArray(o))return M(o)}function P(o,e){var a=Object.keys(o);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(o);e&&(r=r.filter(function(i){return Object.getOwnPropertyDescriptor(o,i).enumerable})),a.push.apply(a,r)}return a}function A(o){for(var e=1;e<arguments.length;e++){var a=arguments[e]!=null?arguments[e]:{};e%2?P(Object(a),!0).forEach(function(r){_(o,r,a[r])}):Object.getOwnPropertyDescriptors?Object.defineProperties(o,Object.getOwnPropertyDescriptors(a)):P(Object(a)).forEach(function(r){Object.defineProperty(o,r,Object.getOwnPropertyDescriptor(a,r))})}return o}function Te(o,e){return Ee(o)||De(o,e)||te(o,e)||Oe()}function Oe(){throw new TypeError(`Invalid attempt to destructure non-iterable instance.
In order to be iterable, non-array objects must have a [Symbol.iterator]() method.`)}function te(o,e){if(o){if(typeof o=="string")return M(o,e);var a=Object.prototype.toString.call(o).slice(8,-1);if(a==="Object"&&o.constructor&&(a=o.constructor.name),a==="Map"||a==="Set")return Array.from(o);if(a==="Arguments"||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(a))return M(o,e)}}function M(o,e){(e==null||e>o.length)&&(e=o.length);for(var a=0,r=new Array(e);a<e;a++)r[a]=o[a];return r}function De(o,e){var a=o==null?null:typeof Symbol<"u"&&o[Symbol.iterator]||o["@@iterator"];if(a!=null){var r,i,d,v,x=[],w=!0,k=!1;try{if(d=(a=a.call(o)).next,e!==0)for(;!(w=(r=d.call(a)).done)&&(x.push(r.value),x.length!==e);w=!0);}catch(S){k=!0,i=S}finally{try{if(!w&&a.return!=null&&(v=a.return(),Object(v)!==v))return}finally{if(k)throw i}}return x}}function Ee(o){if(Array.isArray(o))return o}function Ie(o,e){if(!(o instanceof e))throw new TypeError("Cannot call a class as a function")}function Pe(o,e){for(var a=0;a<e.length;a++){var r=e[a];r.enumerable=r.enumerable||!1,r.configurable=!0,"value"in r&&(r.writable=!0),Object.defineProperty(o,ne(r.key),r)}}function Fe(o,e,a){return e&&Pe(o.prototype,e),Object.defineProperty(o,"prototype",{writable:!1}),o}function _(o,e,a){return e=ne(e),e in o?Object.defineProperty(o,e,{value:a,enumerable:!0,configurable:!0,writable:!0}):o[e]=a,o}function ne(o){var e=Re(o,"string");return m(e)==="symbol"?e:String(e)}function Re(o,e){if(m(o)!=="object"||o===null)return o;var a=o[Symbol.toPrimitive];if(a!==void 0){var r=a.call(o,e);if(m(r)!=="object")return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return(e==="string"?String:Number)(o)}var ae=(function(){function o(){var e=this;Ie(this,o),_(this,"reset",function(){e.isInitialized=!1,e._testMode=!1,e._currentMeasurementId,e._hasLoadedGA=!1,e._isQueuing=!1,e._queueGtag=[]}),_(this,"_gtag",function(){for(var a=arguments.length,r=new Array(a),i=0;i<a;i++)r[i]=arguments[i];e._testMode||e._isQueuing?e._queueGtag.push(r):s.default.apply(void 0,r)}),_(this,"_loadGA",function(a,r){var i=arguments.length>2&&arguments[2]!==void 0?arguments[2]:"https://www.googletagmanager.com/gtag/js";if(!(typeof window>"u"||typeof document>"u")&&!e._hasLoadedGA){var d=document.createElement("script");d.async=!0,d.src="".concat(i,"?id=").concat(a),r&&d.setAttribute("nonce",r),document.body.appendChild(d),window.dataLayer=window.dataLayer||[],window.gtag=function(){window.dataLayer.push(arguments)},e._hasLoadedGA=!0}}),_(this,"_toGtagOptions",function(a){if(a){var r={cookieUpdate:"cookie_update",cookieExpires:"cookie_expires",cookieDomain:"cookie_domain",cookieFlags:"cookie_flags",userId:"user_id",clientId:"client_id",anonymizeIp:"anonymize_ip",contentGroup1:"content_group1",contentGroup2:"content_group2",contentGroup3:"content_group3",contentGroup4:"content_group4",contentGroup5:"content_group5",allowAdFeatures:"allow_google_signals",allowAdPersonalizationSignals:"allow_ad_personalization_signals",nonInteraction:"non_interaction",page:"page_path",hitCallback:"event_callback"},i=Object.entries(a).reduce(function(d,v){var x=Te(v,2),w=x[0],k=x[1];return r[w]?d[r[w]]=k:d[w]=k,d},{});return i}}),_(this,"initialize",function(a){var r=arguments.length>1&&arguments[1]!==void 0?arguments[1]:{};if(!a)throw new Error("Require GA_MEASUREMENT_ID");var i=typeof a=="string"?[{trackingId:a}]:a;e._currentMeasurementId=i[0].trackingId;var d=r.gaOptions,v=r.gtagOptions,x=r.nonce,w=r.testMode,k=w===void 0?!1:w,S=r.gtagUrl;if(e._testMode=k,k||e._loadGA(e._currentMeasurementId,x,S),e.isInitialized||(e._gtag("js",new Date),i.forEach(function(F){var se=A(A(A({},e._toGtagOptions(A(A({},d),F.gaOptions))),v),F.gtagOptions);Object.keys(se).length?e._gtag("config",F.trackingId,se):e._gtag("config",F.trackingId)})),e.isInitialized=!0,!k){var re=f(e._queueGtag);for(e._queueGtag=[],e._isQueuing=!1;re.length;){var oe=re.shift();e._gtag.apply(e,f(oe)),oe[0]==="get"&&(e._isQueuing=!0)}}}),_(this,"set",function(a){if(!a){console.warn("`fieldsObject` is required in .set()");return}if(m(a)!=="object"){console.warn("Expected `fieldsObject` arg to be an Object");return}Object.keys(a).length===0&&console.warn("empty `fieldsObject` given to .set()"),e._gaCommand("set",a)}),_(this,"_gaCommandSendEvent",function(a,r,i,d,v){e._gtag("event",r,A(A({event_category:a,event_label:i,value:d},v&&{non_interaction:v.nonInteraction}),e._toGtagOptions(v)))}),_(this,"_gaCommandSendEventParameters",function(){for(var a=arguments.length,r=new Array(a),i=0;i<a;i++)r[i]=arguments[i];if(typeof r[0]=="string")e._gaCommandSendEvent.apply(e,f(r.slice(1)));else{var d=r[0],v=d.eventCategory,x=d.eventAction,w=d.eventLabel,k=d.eventValue;d.hitType;var S=l(d,c);e._gaCommandSendEvent(v,x,w,k,S)}}),_(this,"_gaCommandSendTiming",function(a,r,i,d){e._gtag("event","timing_complete",{name:r,value:i,event_category:a,event_label:d})}),_(this,"_gaCommandSendPageview",function(a,r){if(r&&Object.keys(r).length){var i=e._toGtagOptions(r),d=i.title,v=i.location,x=l(i,g);e._gtag("event","page_view",A(A(A(A({},a&&{page_path:a}),d&&{page_title:d}),v&&{page_location:v}),x))}else a?e._gtag("event","page_view",{page_path:a}):e._gtag("event","page_view")}),_(this,"_gaCommandSendPageviewParameters",function(){for(var a=arguments.length,r=new Array(a),i=0;i<a;i++)r[i]=arguments[i];if(typeof r[0]=="string")e._gaCommandSendPageview.apply(e,f(r.slice(1)));else{var d=r[0],v=d.page;d.hitType;var x=l(d,y);e._gaCommandSendPageview(v,x)}}),_(this,"_gaCommandSend",function(){for(var a=arguments.length,r=new Array(a),i=0;i<a;i++)r[i]=arguments[i];var d=typeof r[0]=="string"?r[0]:r[0].hitType;switch(d){case"event":e._gaCommandSendEventParameters.apply(e,r);break;case"pageview":e._gaCommandSendPageviewParameters.apply(e,r);break;case"timing":e._gaCommandSendTiming.apply(e,f(r.slice(1)));break;case"screenview":case"transaction":case"item":case"social":case"exception":console.warn("Unsupported send command: ".concat(d));break;default:console.warn("Send command doesn't exist: ".concat(d))}}),_(this,"_gaCommandSet",function(){for(var a=arguments.length,r=new Array(a),i=0;i<a;i++)r[i]=arguments[i];typeof r[0]=="string"&&(r[0]=_({},r[0],r[1])),e._gtag("set",e._toGtagOptions(r[0]))}),_(this,"_gaCommand",function(a){for(var r=arguments.length,i=new Array(r>1?r-1:0),d=1;d<r;d++)i[d-1]=arguments[d];switch(a){case"send":e._gaCommandSend.apply(e,i);break;case"set":e._gaCommandSet.apply(e,i);break;default:console.warn("Command doesn't exist: ".concat(a))}}),_(this,"ga",function(){for(var a=arguments.length,r=new Array(a),i=0;i<a;i++)r[i]=arguments[i];if(typeof r[0]=="string")e._gaCommand.apply(e,r);else{var d=r[0];e._gtag("get",e._currentMeasurementId,"client_id",function(v){e._isQueuing=!1;var x=e._queueGtag;for(d({get:function(S){return S==="clientId"?v:S==="trackingId"?e._currentMeasurementId:S==="apiVersion"?"1":void 0}});x.length;){var w=x.shift();e._gtag.apply(e,f(w))}}),e._isQueuing=!0}return e.ga}),_(this,"event",function(a,r){if(typeof a=="string")e._gtag("event",a,e._toGtagOptions(r));else{var i=a.action,d=a.category,v=a.label,x=a.value,w=a.nonInteraction,k=a.transport;if(!d||!i){console.warn("args.category AND args.action are required in event()");return}var S={hitType:"event",eventCategory:(0,u.default)(d),eventAction:(0,u.default)(i)};v&&(S.eventLabel=(0,u.default)(v)),typeof x<"u"&&(typeof x!="number"?console.warn("Expected `args.value` arg to be a Number."):S.eventValue=x),typeof w<"u"&&(typeof w!="boolean"?console.warn("`args.nonInteraction` must be a boolean."):S.nonInteraction=w),typeof k<"u"&&(typeof k!="string"?console.warn("`args.transport` must be a string."):(["beacon","xhr","image"].indexOf(k)===-1&&console.warn("`args.transport` must be either one of these values: `beacon`, `xhr` or `image`"),S.transport=k)),e._gaCommand("send",S)}}),_(this,"send",function(a){e._gaCommand("send",a)}),this.reset()}return Fe(o,[{key:"gtag",value:function(){this._gtag.apply(this,arguments)}}]),o})();n.GA4=ae;var Me=new ae;n.default=Me})(N)),N}var fe;function Bt(){return fe||(fe=1,(function(n){function s(l){"@babel/helpers - typeof";return s=typeof Symbol=="function"&&typeof Symbol.iterator=="symbol"?function(p){return typeof p}:function(p){return p&&typeof Symbol=="function"&&p.constructor===Symbol&&p!==Symbol.prototype?"symbol":typeof p},s(l)}Object.defineProperty(n,"__esModule",{value:!0}),n.default=n.ReactGAImplementation=void 0;var u=g(zt());function c(l){if(typeof WeakMap!="function")return null;var p=new WeakMap,m=new WeakMap;return(c=function(O){return O?m:p})(l)}function g(l,p){if(l&&l.__esModule)return l;if(l===null||s(l)!=="object"&&typeof l!="function")return{default:l};var m=c(p);if(m&&m.has(l))return m.get(l);var f={},O=Object.defineProperty&&Object.getOwnPropertyDescriptor;for(var C in l)if(C!=="default"&&Object.prototype.hasOwnProperty.call(l,C)){var L=O?Object.getOwnPropertyDescriptor(l,C):null;L&&(L.get||L.set)?Object.defineProperty(f,C,L):f[C]=l[C]}return f.default=l,m&&m.set(l,f),f}var y=u.GA4;n.ReactGAImplementation=y;var h=u.default;n.default=h})(G)),G}var Ut=Bt();const Ht=ke(Ut),Wt={app_ids:{prod:"G-NT3FLN0QHF",dev:"G-7TMZEFFWB7"}},z="fiftyone-do-not-track";function Qt(n){const[s,u]=b.useState(!1),[c,g]=b.useState(!1),y=window.localStorage.getItem(z);b.useEffect(()=>{n||y==="true"||y==="false"?(g(!1),u(!0)):(g(!0),u(!0))},[n,y]);const h=b.useCallback(()=>{window.localStorage.setItem(z,"true"),g(!1),u(!0)},[]),l=b.useCallback(()=>{window.localStorage.setItem(z,"false"),g(!1),u(!0)},[]);return{doNotTrack:y==="true"||n,handleDisable:h,handleAllow:l,ready:s,show:c}}function Vt({callGA:n,info:s}){const[u,c]=Je(),{doNotTrack:g,handleDisable:y,handleAllow:h,ready:l,show:p}=Qt(s.doNotTrack);return b.useEffect(()=>{if(!l)return;const m=s.dev?"dev":"prod",f=kt[m];c({userId:s.uid,userGroup:"fiftyone-oss",writeKey:f,doNotTrack:g,debug:s.dev}),!g&&n()},[n,g,s,l,c]),p?t.jsxs(Yt,{children:[t.jsx($t,{}),t.jsx(D,{container:!0,direction:"column",alignItems:"center",sx:{borderTop:m=>`1px solid ${m.palette.divider}`,backgroundColor:"background.paper"},children:t.jsxs(D,{padding:2,children:[t.jsx(j,{variant:"h6",marginBottom:1,children:"Help us improve FiftyOne"}),t.jsx(j,{marginBottom:1,children:"We use cookies to understand how FiftyOne is used and improve the product. You can help us by allowing anonymous analytics."}),t.jsxs(D,{container:!0,gap:2,justifyContent:"end",direction:"row",children:[t.jsx(D,{item:!0,alignContent:"center",children:t.jsx(Y,{style:{cursor:"pointer"},onClick:y,"data-cy":"btn-disable-cookies",children:"Disable"})}),t.jsx(D,{item:!0,children:t.jsx(I,{variant:"contained",onClick:h,children:"Allow"})})]})]})})]}):null}function Yt({children:n}){return t.jsx($,{position:"fixed",bottom:0,width:"100%",zIndex:51,children:n})}function $t(){const n=_e();return b.useEffect(()=>{n("analytics-consent-shown")},[n]),null}const Zt=n=>b.useCallback(()=>{const u=n.dev?"dev":"prod";Ht.initialize(Wt.app_ids[u],{testMode:!1,gaOptions:{storage:"none",cookieDomain:"none",clientId:n.uid,page_location:"omitted",page_path:"omitted",version:n.version,context:n.context,checkProtocolTask:null}})},[n]);function Jt({fragment:n}){const s=Z.useFragment(Le,n),u=Zt(s);return window.IS_PLAYWRIGHT?(console.log("Analytics component is disabled in playwright"),null):t.jsx(Vt,{callGA:u,info:s})}const Xt=({className:n,value:s})=>t.jsx("span",{className:n,title:s,children:s}),en=({useSearch:n})=>{const s=Xe(),u=V(xe);return t.jsx(et,{cy:"dataset",component:Xt,placeholder:"Select dataset",inputStyle:{height:40,maxWidth:300},containerStyle:{position:"relative"},onSelect:async c=>(s(c),c),overflow:!0,useSearch:n,value:u})};var E={},ge;function tn(){if(ge)return E;ge=1;var n=tt();Object.defineProperty(E,"__esModule",{value:!0}),E.default=void 0;var s=n(nt()),u=at();return E.default=(0,s.default)((0,u.jsx)("path",{d:"m19 9 1.25-2.75L23 5l-2.75-1.25L19 1l-1.25 2.75L15 5l2.75 1.25zm-7.5.5L9 4 6.5 9.5 1 12l5.5 2.5L9 20l2.5-5.5L17 12zM19 15l-1.25 2.75L15 19l2.75 1.25L19 23l1.25-2.75L23 19l-2.75-1.25z"}),"AutoAwesome"),E}var nn=tn();const an=ke(nn),me="fiftyone-enterprise-tooltip-seen",pe="fo-cta-enterprise-button",B="#333333",he="#FFFFFF",rn="#FF6D04",on="#B681FF",sn=it`
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
`,ln=st`
  animation: ${sn} 1.5s ease-in-out infinite;
`,cn=T.div`
  display: flex;
  align-items: center;
  transition: all 0.3s ease;
`,ye=()=>t.jsxs(t.Fragment,{children:[t.jsxs("svg",{width:0,height:0,"aria-label":"Gradient","aria-labelledby":"gradient",children:[t.jsx("title",{children:"Gradient"}),t.jsx("defs",{children:t.jsxs("linearGradient",{id:"gradient1",x1:"0%",y1:"0%",x2:"100%",y2:"100%",children:[t.jsx("stop",{offset:"0%",style:{stopColor:rn,stopOpacity:1}}),t.jsx("stop",{offset:"100%",style:{stopColor:on,stopOpacity:1}})]})})]}),t.jsx(cn,{className:"fo-teams-cta-pulse-animation",children:t.jsx(an,{sx:{fontSize:{xs:16,sm:20},mr:1,fill:"url(#gradient1)"}})})]}),un=T.div`
  background-color: ${({$bgColor:n})=>n};
  border-radius: 16px;

  &:hover {
    background-color: transparent;
  }
`,dn=T(ve)`
  text-decoration: none;

  &:hover {
    text-decoration: none;
  }
`,fn=T(ot)`
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
      rgba(
          255,
          255,
          255,
          ${({$isLightMode:n})=>n?"0.3":"0.2"}
        )
        50%,
      rgba(255, 255, 255, 0) 100%
    );
    transition: all ${({$isLightMode:n})=>n?"0.8s":"0.6s"}
      ease;
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
      ${ln}
    }
  }
`,gn=T($)`
  padding: 16px;
  width: 310px;
  position: relative;
  display: flex;
  flex-direction: column;
  gap: 12px;
`,mn=T(j)`
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
  margin-bottom: 12px;
`,pn=T(j)`
  position: relative;
  color: var(--fo-palette-text-secondary);
  font-size: 15px !important;
`,hn=T(R)`
  margin-top: 16px;
`;function yn({disablePopover:n=!1}){const[s,u]=b.useState(!1),{mode:c}=we(),g=Q(),y=c==="light"?he:B;b.useEffect(()=>{const m=window.localStorage.getItem(me),f=window.IS_PLAYWRIGHT;!m&&!f&&u(!0)},[]);const h=b.useCallback(()=>{localStorage.setItem(me,"true")},[]),l=b.useCallback(()=>{h(),u(!1)},[h]),p=b.useCallback(()=>{h(),u(!1),window.open("https://voxel51.com/why-upgrade?utm_source=FiftyOneApp","_blank")},[h]);return t.jsxs(t.Fragment,{children:[t.jsx(un,{$bgColor:c==="light"?"transparent":y,children:t.jsx(dn,{href:"https://voxel51.com/why-upgrade?utm_source=FiftyOneApp",children:t.jsxs(fn,{$borderColor:c==="dark"?B:g.divider,$isLightMode:c==="light",id:pe,children:[t.jsx(ye,{}),"Explore Enterprise"]})})}),s&&!n&&t.jsx(rt,{open:!0,anchorEl:document.getElementById(pe),onClose:l,anchorOrigin:{vertical:"bottom",horizontal:"center"},transformOrigin:{vertical:-12,horizontal:"center"},elevation:3,children:t.jsxs(gn,{style:{backgroundColor:c==="light"?he:B},children:[t.jsxs(mn,{variant:"h6",children:[t.jsx(ye,{}),t.jsx(j,{variant:"h6",letterSpacing:.3,children:"Accelerate your workflow"})]}),t.jsx(pn,{variant:"body2",children:"With FiftyOne Enterprise you can connect to your data lake, automate your data curation and model analysis tasks, securely collaborate with your team, and more."}),t.jsxs(hn,{direction:"row",spacing:2,children:[t.jsx(I,{variant:"contained",onClick:p,size:"large",sx:{boxShadow:"none"},children:"Explore Enterprise"}),t.jsx(I,{variant:"outlined",color:"secondary",onClick:l,size:"large",sx:{boxShadow:"none"},children:"Dismiss"})]})]})})]})}const bn=n=>s=>{const u=V(xt),{data:c,refetch:g}=Z.usePaginationFragment(Ce,n);return Nt(()=>{g({search:s})},200,[s,u]),b.useMemo(()=>({total:c.datasets.total===null?void 0:c.datasets.total,values:c.datasets.edges.map(y=>y.node.name)}),[c])},An=({children:n,fragment:s,hasDataset:u})=>{const c=Z.useFragment(Ae,s),g=bn(c),y=lt(),{mode:h,setMode:l}=we(),p=ct(ut),m=_e();return t.jsxs(t.Fragment,{children:[t.jsxs(dt,{title:"FiftyOne",onRefresh:y,navChildren:t.jsx(en,{useSearch:g}),children:[u&&t.jsx(b.Suspense,{fallback:t.jsx("div",{style:{flex:1}}),children:t.jsx(ft,{})}),!u&&t.jsx("div",{style:{flex:1}}),t.jsx("div",{style:{padding:"0.5rem"},children:t.jsx(yn,{})}),t.jsxs("div",{className:gt,children:[t.jsx(mt,{title:h==="dark"?"Light mode":"Dark mode",onClick:()=>{const f=h==="dark"?"light":"dark";l(f),p(f),m("switch_app_theme",{theme:f})},sx:{color:f=>f.palette.text.secondary,m:0,p:"0.5rem"},children:h==="dark"?t.jsx(wt,{color:"inherit"}):t.jsx(_t,{})}),t.jsx(pt,{}),t.jsx(ht,{}),t.jsx(yt,{}),t.jsx($,{ml:1,children:t.jsx(bt,{place:vt.HEADER_ACTIONS})})]})]}),n,t.jsx(Jt,{fragment:c})]})},vn="_page_8fb7q_1",jn={page:vn};export{An as N,Sn as S,kn as a,jn as s};
