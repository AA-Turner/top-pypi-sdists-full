import{r as p,j as e,u as gt,a as un,e as Yn,s as Ma,b as Fa,c as En,d as Wa,f as Ao,g as Je,h as Io,i as zo,k as qa,L as ua,l as m,m as s,n as Pl,$ as R,o as Mo,p as V,q as Vl,t as Rl,v as Fo,w as Me,x as Eo,y as Do,z as Ln,A as _o,F as U,B as bn,C as K,D as j,E as W,G as Ol,H as Nl,I as Ko,R as rn,J as $l,K as Po,M as Bl,N as Vo,O as Ro,P as Hl,Q as Oo,S as No,T as $o,U as jl,V as Bo,W as Ho,X as wn,Y as ga,Z as Bn,_ as jo,a0 as Ie,a1 as Zl,a2 as _e,a3 as Zo,a4 as Uo,a5 as Re,a6 as Xa,a7 as Ya,a8 as Ja,a9 as $,aa as on,ab as Wt,ac as Ul,ad as Gl,ae as Go,af as Qo,ag as Wo,ah as qo,ai as Xo,aj as Yo,ak as Ql,al as Jo,am as e1,an as n1,ao as a1,ap as t1,aq as l1,ar as i1,as as r1,at as o1,au as s1,av as mt,aw as te,ax as c1,ay as d1,az as Wl,aA as u1,aB as g1,aC as m1,aD as p1,aE as M,aF as pt,aG as Dn,aH as h1,aI as ta,aJ as f1,aK as b1,aL as ql,aM as Xl,aN as Yl,aO as Be,aP as sn,aQ as q,aR as y1,aS as pn,aT as v1,aU as C1,aV as Ue,aW as tn,aX as Z,aY as k1,aZ as ce,a_ as Sn,a$ as Pn,b0 as Jl,b1 as An,b2 as Oe,b3 as ei,b4 as qt,b5 as L1,b6 as ni,b7 as he,b8 as w1,b9 as ma,ba as S1,bb as x1,bc as T1,bd as A1,be as Xt,bf as ai,bg as I1,bh as z1,bi as M1,bj as F1,bk as ye,bl as E1,bm as ht,bn as D1,bo as _1,bp as pa,bq as K1,br as P1,bs as V1,bt as R1,bu as ti,bv as O1,bw as N1,bx as $1,by as B1,bz as H1,bA as j1,bB as Z1,bC as Yt,bD as U1,bE as Ea,bF as G1,bG as Q1,bH as W1,bI as q1,bJ as X1,bK as Y1,bL as J1,bM as es,bN as ns,bO as Jn}from"./vendor-DHb1kz-d.js";import{_ as as,F as li,I as ts,a as ls,b as is,c as rs,d as os,e as ss,f as cs,P as ds,g as us,h as gs,i as ms,T as ps,j as hs}from"./vendor-arizeai-BWffpt59.js";import{a as Jt,R as fs,b as bs,c as ys,m as vs,T as Cs,A as ks,S as Ls,d as ws,e as Ss,f as xs,u as Ts}from"./pages-CJs8SCmq.js";import{L as ii,a as ri,j as oi,E as ft,k as si,d as ci,l as et,b as di,h as As,c as Is,e as zs,f as Ms,g as Fs,i as Es,s as Ds,m as Hn,n as jn,R as Zn,p as _s,o as Ks}from"./vendor-codemirror-BI6d4ZER.js";import{V as Ps}from"./vendor-three-BLWp5bic.js";const ui=(function(){var n={defaultValue:null,kind:"LocalArgument",name:"clusters"},a={defaultValue:null,kind:"LocalArgument",name:"dataQualityMetricColumnName"},t={defaultValue:null,kind:"LocalArgument",name:"fetchDataQualityMetric"},l={defaultValue:null,kind:"LocalArgument",name:"fetchPerformanceMetric"},i={defaultValue:null,kind:"LocalArgument",name:"performanceMetric"},r=[{alias:null,args:null,kind:"ScalarField",name:"primaryValue",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"referenceValue",storageKey:null}],o=[{alias:null,args:[{kind:"Variable",name:"clusters",variableName:"clusters"}],concreteType:"Cluster",kind:"LinkedField",name:"clusters",plural:!0,selections:[{alias:null,args:null,kind:"ScalarField",name:"id",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"eventIds",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"driftRatio",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"primaryToCorpusRatio",storageKey:null},{condition:"fetchDataQualityMetric",kind:"Condition",passingValue:!0,selections:[{alias:null,args:[{fields:[{kind:"Variable",name:"columnName",variableName:"dataQualityMetricColumnName"},{kind:"Literal",name:"metric",value:"mean"}],kind:"ObjectValue",name:"metric"}],concreteType:"DatasetValues",kind:"LinkedField",name:"dataQualityMetric",plural:!1,selections:r,storageKey:null}]},{condition:"fetchPerformanceMetric",kind:"Condition",passingValue:!0,selections:[{alias:null,args:[{fields:[{kind:"Variable",name:"metric",variableName:"performanceMetric"}],kind:"ObjectValue",name:"metric"}],concreteType:"DatasetValues",kind:"LinkedField",name:"performanceMetric",plural:!1,selections:r,storageKey:null}]}],storageKey:null}];return{fragment:{argumentDefinitions:[n,a,t,l,i],kind:"Fragment",metadata:null,name:"pointCloudStore_clusterMetricsQuery",selections:o,type:"Query",abstractKey:null},kind:"Request",operation:{argumentDefinitions:[n,t,a,l,i],kind:"Operation",name:"pointCloudStore_clusterMetricsQuery",selections:o},params:{cacheID:"86666967012812887ac0a0149d2d2535",id:null,metadata:{},name:"pointCloudStore_clusterMetricsQuery",operationKind:"query",text:`query pointCloudStore_clusterMetricsQuery(
  $clusters: [ClusterInput!]!
  $fetchDataQualityMetric: Boolean!
  $dataQualityMetricColumnName: String
  $fetchPerformanceMetric: Boolean!
  $performanceMetric: PerformanceMetric!
) {
  clusters(clusters: $clusters) {
    id
    eventIds
    driftRatio
    primaryToCorpusRatio
    dataQualityMetric(metric: {metric: mean, columnName: $dataQualityMetricColumnName}) @include(if: $fetchDataQualityMetric) {
      primaryValue
      referenceValue
    }
    performanceMetric(metric: {metric: $performanceMetric}) @include(if: $fetchPerformanceMetric) {
      primaryValue
      referenceValue
    }
  }
}
`}}})();ui.hash="dbfc8c02ba1ec4f2ba0317b371854d9b";const gi=(function(){var n={defaultValue:null,kind:"LocalArgument",name:"clusterMinSamples"},a={defaultValue:null,kind:"LocalArgument",name:"clusterSelectionEpsilon"},t={defaultValue:null,kind:"LocalArgument",name:"coordinates"},l={defaultValue:null,kind:"LocalArgument",name:"dataQualityMetricColumnName"},i={defaultValue:null,kind:"LocalArgument",name:"eventIds"},r={defaultValue:null,kind:"LocalArgument",name:"fetchDataQualityMetric"},o={defaultValue:null,kind:"LocalArgument",name:"fetchPerformanceMetric"},c={defaultValue:null,kind:"LocalArgument",name:"minClusterSize"},d={defaultValue:null,kind:"LocalArgument",name:"performanceMetric"},u=[{alias:null,args:null,kind:"ScalarField",name:"primaryValue",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"referenceValue",storageKey:null}],g=[{alias:null,args:[{kind:"Variable",name:"clusterMinSamples",variableName:"clusterMinSamples"},{kind:"Variable",name:"clusterSelectionEpsilon",variableName:"clusterSelectionEpsilon"},{kind:"Variable",name:"coordinates3d",variableName:"coordinates"},{kind:"Variable",name:"eventIds",variableName:"eventIds"},{kind:"Variable",name:"minClusterSize",variableName:"minClusterSize"}],concreteType:"Cluster",kind:"LinkedField",name:"hdbscanClustering",plural:!0,selections:[{alias:null,args:null,kind:"ScalarField",name:"id",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"eventIds",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"driftRatio",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"primaryToCorpusRatio",storageKey:null},{condition:"fetchDataQualityMetric",kind:"Condition",passingValue:!0,selections:[{alias:null,args:[{fields:[{kind:"Variable",name:"columnName",variableName:"dataQualityMetricColumnName"},{kind:"Literal",name:"metric",value:"mean"}],kind:"ObjectValue",name:"metric"}],concreteType:"DatasetValues",kind:"LinkedField",name:"dataQualityMetric",plural:!1,selections:u,storageKey:null}]},{condition:"fetchPerformanceMetric",kind:"Condition",passingValue:!0,selections:[{alias:null,args:[{fields:[{kind:"Variable",name:"metric",variableName:"performanceMetric"}],kind:"ObjectValue",name:"metric"}],concreteType:"DatasetValues",kind:"LinkedField",name:"performanceMetric",plural:!1,selections:u,storageKey:null}]}],storageKey:null}];return{fragment:{argumentDefinitions:[n,a,t,l,i,r,o,c,d],kind:"Fragment",metadata:null,name:"pointCloudStore_clustersQuery",selections:g,type:"Query",abstractKey:null},kind:"Request",operation:{argumentDefinitions:[i,t,c,n,a,r,l,o,d],kind:"Operation",name:"pointCloudStore_clustersQuery",selections:g},params:{cacheID:"a1a02d970d255935edfcdd797e4ca80d",id:null,metadata:{},name:"pointCloudStore_clustersQuery",operationKind:"query",text:`query pointCloudStore_clustersQuery(
  $eventIds: [ID!]!
  $coordinates: [InputCoordinate3D!]!
  $minClusterSize: Int!
  $clusterMinSamples: Int!
  $clusterSelectionEpsilon: Float!
  $fetchDataQualityMetric: Boolean!
  $dataQualityMetricColumnName: String
  $fetchPerformanceMetric: Boolean!
  $performanceMetric: PerformanceMetric!
) {
  hdbscanClustering(eventIds: $eventIds, coordinates3d: $coordinates, minClusterSize: $minClusterSize, clusterMinSamples: $clusterMinSamples, clusterSelectionEpsilon: $clusterSelectionEpsilon) {
    id
    eventIds
    driftRatio
    primaryToCorpusRatio
    dataQualityMetric(metric: {metric: mean, columnName: $dataQualityMetricColumnName}) @include(if: $fetchDataQualityMetric) {
      primaryValue
      referenceValue
    }
    performanceMetric(metric: {metric: $performanceMetric}) @include(if: $fetchPerformanceMetric) {
      primaryValue
      referenceValue
    }
  }
}
`}}})();gi.hash="b26f299a862a3bc4f5487ace49db1d43";const mi=(function(){var n={defaultValue:null,kind:"LocalArgument",name:"corpusEventIds"},a={defaultValue:null,kind:"LocalArgument",name:"primaryEventIds"},t={defaultValue:null,kind:"LocalArgument",name:"referenceEventIds"},l=[{kind:"Variable",name:"eventIds",variableName:"primaryEventIds"}],i={alias:null,args:null,kind:"ScalarField",name:"id",storageKey:null},r={alias:null,args:null,kind:"ScalarField",name:"name",storageKey:null},o={alias:null,args:null,kind:"ScalarField",name:"type",storageKey:null},c={alias:null,args:null,kind:"ScalarField",name:"value",storageKey:null},d={alias:null,args:null,concreteType:"EventMetadata",kind:"LinkedField",name:"eventMetadata",plural:!1,selections:[{alias:null,args:null,kind:"ScalarField",name:"predictionId",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"predictionLabel",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"predictionScore",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"actualLabel",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"actualScore",storageKey:null}],storageKey:null},u={alias:null,args:null,concreteType:"PromptResponse",kind:"LinkedField",name:"promptAndResponse",plural:!1,selections:[{alias:null,args:null,kind:"ScalarField",name:"prompt",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"response",storageKey:null}],storageKey:null},g={alias:null,args:null,kind:"ScalarField",name:"documentText",storageKey:null},h=[i,{alias:null,args:null,concreteType:"DimensionWithValue",kind:"LinkedField",name:"dimensions",plural:!0,selections:[{alias:null,args:null,concreteType:"Dimension",kind:"LinkedField",name:"dimension",plural:!1,selections:[r,o],storageKey:null},c],storageKey:null},d,u,g],f={alias:null,args:null,concreteType:"Inferences",kind:"LinkedField",name:"referenceInferences",plural:!1,selections:[{alias:null,args:[{kind:"Variable",name:"eventIds",variableName:"referenceEventIds"}],concreteType:"Event",kind:"LinkedField",name:"events",plural:!0,selections:[i,{alias:null,args:null,concreteType:"DimensionWithValue",kind:"LinkedField",name:"dimensions",plural:!0,selections:[{alias:null,args:null,concreteType:"Dimension",kind:"LinkedField",name:"dimension",plural:!1,selections:[i,r,o],storageKey:null},c],storageKey:null},d,u,g],storageKey:null}],storageKey:null},b=[{kind:"Variable",name:"eventIds",variableName:"corpusEventIds"}],y=[i,{alias:null,args:null,concreteType:"DimensionWithValue",kind:"LinkedField",name:"dimensions",plural:!0,selections:[{alias:null,args:null,concreteType:"Dimension",kind:"LinkedField",name:"dimension",plural:!1,selections:[r,o,i],storageKey:null},c],storageKey:null},d,u,g];return{fragment:{argumentDefinitions:[n,a,t],kind:"Fragment",metadata:null,name:"pointCloudStore_eventsQuery",selections:[{alias:null,args:null,concreteType:"InferenceModel",kind:"LinkedField",name:"model",plural:!1,selections:[{alias:null,args:null,concreteType:"Inferences",kind:"LinkedField",name:"primaryInferences",plural:!1,selections:[{alias:null,args:l,concreteType:"Event",kind:"LinkedField",name:"events",plural:!0,selections:h,storageKey:null}],storageKey:null},f,{alias:null,args:null,concreteType:"Inferences",kind:"LinkedField",name:"corpusInferences",plural:!1,selections:[{alias:null,args:b,concreteType:"Event",kind:"LinkedField",name:"events",plural:!0,selections:h,storageKey:null}],storageKey:null}],storageKey:null}],type:"Query",abstractKey:null},kind:"Request",operation:{argumentDefinitions:[a,t,n],kind:"Operation",name:"pointCloudStore_eventsQuery",selections:[{alias:null,args:null,concreteType:"InferenceModel",kind:"LinkedField",name:"model",plural:!1,selections:[{alias:null,args:null,concreteType:"Inferences",kind:"LinkedField",name:"primaryInferences",plural:!1,selections:[{alias:null,args:l,concreteType:"Event",kind:"LinkedField",name:"events",plural:!0,selections:y,storageKey:null}],storageKey:null},f,{alias:null,args:null,concreteType:"Inferences",kind:"LinkedField",name:"corpusInferences",plural:!1,selections:[{alias:null,args:b,concreteType:"Event",kind:"LinkedField",name:"events",plural:!0,selections:y,storageKey:null}],storageKey:null}],storageKey:null}]},params:{cacheID:"bcac76c653bed7d4f922f175d03a3408",id:null,metadata:{},name:"pointCloudStore_eventsQuery",operationKind:"query",text:`query pointCloudStore_eventsQuery(
  $primaryEventIds: [ID!]!
  $referenceEventIds: [ID!]!
  $corpusEventIds: [ID!]!
) {
  model {
    primaryInferences {
      events(eventIds: $primaryEventIds) {
        id
        dimensions {
          dimension {
            name
            type
            id
          }
          value
        }
        eventMetadata {
          predictionId
          predictionLabel
          predictionScore
          actualLabel
          actualScore
        }
        promptAndResponse {
          prompt
          response
        }
        documentText
      }
    }
    referenceInferences {
      events(eventIds: $referenceEventIds) {
        id
        dimensions {
          dimension {
            id
            name
            type
          }
          value
        }
        eventMetadata {
          predictionId
          predictionLabel
          predictionScore
          actualLabel
          actualScore
        }
        promptAndResponse {
          prompt
          response
        }
        documentText
      }
    }
    corpusInferences {
      events(eventIds: $corpusEventIds) {
        id
        dimensions {
          dimension {
            name
            type
            id
          }
          value
        }
        eventMetadata {
          predictionId
          predictionLabel
          predictionScore
          actualLabel
          actualScore
        }
        promptAndResponse {
          prompt
          response
        }
        documentText
      }
    }
  }
}
`}}})();mi.hash="00a957322684d9186fdf16d33a75b931";const pi=(function(){var n={defaultValue:null,kind:"LocalArgument",name:"getDimensionCategories"},a={defaultValue:null,kind:"LocalArgument",name:"getDimensionMinMax"},t={defaultValue:null,kind:"LocalArgument",name:"id"},l=[{kind:"Variable",name:"id",variableName:"id"}],i={alias:null,args:null,kind:"ScalarField",name:"id",storageKey:null},r={condition:"getDimensionMinMax",kind:"Condition",passingValue:!0,selections:[{alias:"min",args:[{kind:"Literal",name:"metric",value:"min"}],kind:"ScalarField",name:"dataQualityMetric",storageKey:'dataQualityMetric(metric:"min")'},{alias:"max",args:[{kind:"Literal",name:"metric",value:"max"}],kind:"ScalarField",name:"dataQualityMetric",storageKey:'dataQualityMetric(metric:"max")'}]},o={condition:"getDimensionCategories",kind:"Condition",passingValue:!0,selections:[{alias:null,args:null,kind:"ScalarField",name:"categories",storageKey:null}]};return{fragment:{argumentDefinitions:[n,a,t],kind:"Fragment",metadata:null,name:"pointCloudStore_dimensionMetadataQuery",selections:[{kind:"RequiredField",field:{alias:"dimension",args:l,concreteType:null,kind:"LinkedField",name:"node",plural:!1,selections:[{kind:"InlineFragment",selections:[i,r,o],type:"Dimension",abstractKey:null}],storageKey:null},action:"THROW"}],type:"Query",abstractKey:null},kind:"Request",operation:{argumentDefinitions:[t,a,n],kind:"Operation",name:"pointCloudStore_dimensionMetadataQuery",selections:[{alias:"dimension",args:l,concreteType:null,kind:"LinkedField",name:"node",plural:!1,selections:[{alias:null,args:null,kind:"ScalarField",name:"__typename",storageKey:null},i,{kind:"InlineFragment",selections:[r,o],type:"Dimension",abstractKey:null}],storageKey:null}]},params:{cacheID:"cc8c5b634ad1f06e595b1542b2f9830b",id:null,metadata:{},name:"pointCloudStore_dimensionMetadataQuery",operationKind:"query",text:`query pointCloudStore_dimensionMetadataQuery(
  $id: ID!
  $getDimensionMinMax: Boolean!
  $getDimensionCategories: Boolean!
) {
  dimension: node(id: $id) {
    __typename
    ... on Dimension {
      id
      min: dataQualityMetric(metric: min) @include(if: $getDimensionMinMax)
      max: dataQualityMetric(metric: max) @include(if: $getDimensionMinMax)
      categories @include(if: $getDimensionCategories)
    }
    id
  }
}
`}}})();pi.hash="2d61766d79c27d5fe1d17dba940dfe52";const Vs=30,Da=5,_a=100,Rs=0,Ka=0,Pa=.99,Os=500,el=300,nl=1e5,Ns=10,al=1,$s=2,Bs=1,Hs=0;var B=(n=>(n.inferences="inferences",n.correctness="correctness",n.dimension="dimension",n))(B||{}),yn=(n=>(n.list="list",n.gallery="gallery",n))(yn||{}),hn=(n=>(n.small="small",n.medium="medium",n.large="large",n))(hn||{}),G=(n=>(n.primary="primary",n.reference="reference",n.corpus="corpus",n))(G||{}),se=(n=>(n.correct="correct",n.incorrect="incorrect",n.unknown="unknown",n))(se||{});const js=["#05fbff","#cb8afd"],Zs=["#00add0","#4500d9"],He="#a5a5a5",gn=He;var Te=(n=>(n.primary="primary",n.reference="reference",n.corpus="corpus",n))(Te||{});function P(n){throw new Error("Unreachable")}function bt(n){return typeof n=="number"||n===null}function Us(n){return typeof n=="string"||n===null}function Gs(n){return Us(n)||n===void 0}function S7(n){return Array.isArray(n)?n.every(a=>typeof a=="string"):!1}function fe(n){return typeof n=="object"&&n!==null}function x7(n){return fe(n)&&Object.keys(n).every(a=>typeof a=="string")}const Qs=()=>n=>n,yt=p.createContext(null);function ha(){const n=p.useContext(yt);if(n===null)throw new Error("useInferences must be used within a InferencesProvider");return n}function T7(n){return e(yt.Provider,{value:{primaryInferences:n.primaryInferences,referenceInferences:n.referenceInferences,corpusInferences:n.corpusInferences,getInferencesNameByRole:a=>{var t,l;switch(a){case Te.primary:return n.primaryInferences.name;case Te.reference:return((t=n.referenceInferences)==null?void 0:t.name)??"reference";case Te.corpus:return((l=n.corpusInferences)==null?void 0:l.name)??"corpus";default:P()}}},children:n.children})}const vt=p.createContext(null);function A7({children:n,...a}){const[t]=p.useState(()=>N2(a));return e(vt.Provider,{value:t,children:n})}function I(n,a){const t=p.useContext(vt);if(!t)throw new Error("Missing PointCloudContext.Provider in the tree");return gt(t,n,a)}var J=(n=>(n.last_hour="Last Hour",n.last_day="Last Day",n.last_week="Last Week",n.last_month="Last Month",n.last_3_months="Last 3 Months",n.first_hour="First Hour",n.first_day="First Day",n.first_week="First Week",n.first_month="First Month",n.all="All",n))(J||{});const hi=p.createContext(null);function Ws(){const n=p.useContext(hi);if(n===null)throw new Error("useTimeRange must be used within a TimeRangeProvider");return n}function qs(n,a){return p.useMemo(()=>{switch(n){case"Last Hour":{const l=un(zo(a.end),{roundingMethod:"ceil"});return{start:qa(l,1),end:l}}case"Last Day":{const l=un(Io(a.end),{roundingMethod:"ceil"});return{start:Je(l,1),end:l}}case"Last Week":{const l=un(Yn(a.end),{roundingMethod:"ceil"});return{start:Je(l,7),end:l}}case"Last Month":{const l=un(Yn(a.end),{roundingMethod:"ceil"});return{start:Je(l,30),end:l}}case"Last 3 Months":{const l=un(Yn(a.end),{roundingMethod:"ceil"});return{start:Je(l,90),end:l}}case"First Hour":{const l=Wa(a.start);return{start:l,end:Ao(l,1)}}case"First Day":{const l=En(a.start);return{start:l,end:Fa(l,1)}}case"First Week":{const l=Ma(a.start);return{start:l,end:Fa(l,7)}}case"First Month":{const l=Ma(a.start);return{start:l,end:Fa(l,30)}}case"All":{const l=un(Yn(a.end),{roundingMethod:"floor"});return{start:Ma(a.start),end:l}}default:P()}},[n,a])}function I7(n){const[a,t]=p.useState("Last Month"),l=qs(a,n.timeRangeBounds),i=p.useCallback(r=>{p.startTransition(()=>{t(r)})},[]);return e(hi.Provider,{value:{timeRange:l,timePreset:a,setTimePreset:i},children:n.children})}function fa(n){return e("div",{onClick:a=>a.stopPropagation(),css:m`
        display: inline-block;
      `,children:e(ua,{css:m`
          color: var(--ac-global-link-color);
          &:not(:hover) {
            text-decoration: none;
          }
        `,...n})})}function de({href:n,children:a}){return s("a",{href:n,target:"_blank",css:m`
        color: var(--ac-global-link-color);
        text-decoration: none;
        display: inline-flex;
        align-items: center;
        &:hover {
          text-decoration: underline;
        }
        .ac-icon-wrap {
          display: inline-block;
          margin-left: 0.1em;
          font-size: 1em;
        }
      `,rel:"noreferrer",children:[a,e(T,{svg:e(Ec,{})})]})}const z7=()=>e("div",{css:m`
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        display: flex;
        justify-content: center;
        align-items: center;
        background-color: rgba(0, 0, 0, 0.2);
      `,children:e(Ki,{isIndeterminate:!0,"aria-label":"loading"})});function M7(n){const{width:a="size-1250"}=n;return e(w,{width:a,backgroundColor:"light",borderStartWidth:"thin",borderStartColor:"dark",padding:"size-200",flex:"none",children:e(S,{direction:"column",alignItems:"end",justifyContent:"center",height:"100%",children:n.children})})}const Xs=2e3,Ys=m`
  flex: none;
  box-sizing: content-box;
`;function Ct(n){const{text:a,size:t="S",...l}=n,[i,r]=p.useState(!1),o=p.useCallback(()=>{const c=typeof a=="string"?a:a.current||"";Pl(c),r(!0),setTimeout(()=>{r(!1)},Xs)},[a]);return e("div",{className:"copy-to-clipboard-button",css:Ys,children:s(R,{delay:0,children:[e(z,{size:t,leadingVisual:e(T,{svg:i?e(Li,{}):e(Si,{})}),onPress:o,...l}),e(ke,{offset:5,children:"Copy"})]})})}const fi={margin:["margin",N],marginStart:[pe("marginLeft","marginRight"),N],marginEnd:[pe("marginRight","marginLeft"),N],marginTop:["marginTop",N],marginBottom:["marginBottom",N],marginX:[["marginLeft","marginRight"],N],marginY:[["marginTop","marginBottom"],N],width:["width",N],height:["height",N],minWidth:["minWidth",N],minHeight:["minHeight",N],maxWidth:["maxWidth",N],maxHeight:["maxHeight",N],isHidden:["display",lc],alignSelf:["alignSelf",ge],justifySelf:["justifySelf",ge],position:["position",Ra],zIndex:["zIndex",Ra],top:["top",N],bottom:["bottom",N],start:[pe("left","right"),N],end:[pe("right","left"),N],left:["left",N],right:["right",N],order:["order",Ra],flex:["flex",ic],flexGrow:["flexGrow",ge],flexShrink:["flexShrink",ge],flexBasis:["flexBasis",ge],gridArea:["gridArea",ge],gridColumn:["gridColumn",ge],gridColumnEnd:["gridColumnEnd",ge],gridColumnStart:["gridColumnStart",ge],gridRow:["gridRow",ge],gridRowEnd:["gridRowEnd",ge],gridRowStart:["gridRowStart",ge]},bi={...fi,backgroundColor:["backgroundColor",tc],borderWidth:["borderWidth",Ee],borderStartWidth:[pe("borderLeftWidth","borderRightWidth"),Ee],borderEndWidth:[pe("borderRightWidth","borderLeftWidth"),Ee],borderLeftWidth:["borderLeftWidth",Ee],borderRightWidth:["borderRightWidth",Ee],borderTopWidth:["borderTopWidth",Ee],borderBottomWidth:["borderBottomWidth",Ee],borderXWidth:[["borderLeftWidth","borderRightWidth"],Ee],borderYWidth:[["borderTopWidth","borderBottomWidth"],Ee],borderColor:["borderColor",Fe],borderStartColor:[pe("borderLeftColor","borderRightColor"),Fe],borderEndColor:[pe("borderRightColor","borderLeftColor"),Fe],borderLeftColor:["borderLeftColor",Fe],borderRightColor:["borderRightColor",Fe],borderTopColor:["borderTopColor",Fe],borderBottomColor:["borderBottomColor",Fe],borderXColor:[["borderLeftColor","borderRightColor"],Fe],borderYColor:[["borderTopColor","borderBottomColor"],Fe],borderRadius:["borderRadius",De],borderTopStartRadius:[pe("borderTopLeftRadius","borderTopRightRadius"),De],borderTopEndRadius:[pe("borderTopRightRadius","borderTopLeftRadius"),De],borderBottomStartRadius:[pe("borderBottomLeftRadius","borderBottomRightRadius"),De],borderBottomEndRadius:[pe("borderBottomRightRadius","borderBottomLeftRadius"),De],borderTopLeftRadius:["borderTopLeftRadius",De],borderTopRightRadius:["borderTopRightRadius",De],borderBottomLeftRadius:["borderBottomLeftRadius",De],borderBottomRightRadius:["borderBottomRightRadius",De],padding:["padding",N],paddingStart:[pe("paddingLeft","paddingRight"),N],paddingEnd:[pe("paddingRight","paddingLeft"),N],paddingLeft:["paddingLeft",N],paddingRight:["paddingRight",N],paddingTop:["paddingTop",N],paddingBottom:["paddingBottom",N],paddingX:[["paddingLeft","paddingRight"],N],paddingY:[["paddingTop","paddingBottom"],N],overflow:["overflow",ge]},tl={borderWidth:"borderStyle",borderLeftWidth:"borderLeftStyle",borderRightWidth:"borderRightStyle",borderTopWidth:"borderTopStyle",borderBottomWidth:"borderBottomStyle"},Js=/(%|px|em|rem|vw|vh|auto|cm|mm|in|pt|pc|ex|ch|rem|vmin|vmax|fr)$/,ec=/^\s*\w+\(/,nc=/(static-)?size-\d+|single-line-(height|width)/g;function N(n){return typeof n=="number"?n+"px":Js.test(n)?n:ec.test(n)?n.replace(nc,"var(--ac-global-dimension-$&)"):`var(--ac-global-dimension-${n})`}function Va(n,a){return n=kt(n,a),N(n)}function ac(n,a,t,l){const i={};for(const r in n){const o=a[r];if(!o||n[r]==null)continue;let[c,d]=o;typeof c=="function"&&(c=c(t));const u=kt(n[r],l),g=d(u);if(Array.isArray(c))for(const h of c)i[h]=g;else i[c]=g}for(const r in tl)i[r]&&(i[tl[r]]="solid",i.boxSizing="border-box");return i}function pe(n,a){return t=>t==="rtl"?a:n}function Un(n,a="default"){return`var(--ac-global-color-${n}, var(--ac-semantic-${n}-color-${a}))`}function tc(n){return`var(--ac-global-background-color-${n}, ${Un(n,"background")})`}function Fe(n){return n==="default"?"var(--ac-global-border-color)":`var(--ac-global-border-color-${n}, ${Un(n,"border")})`}function Ee(n){return`var(--ac-global-border-size-${n})`}function ge(n){return n}function De(n){return`var(--ac-global-rounding-${n})`}function lc(n){return n?"none":void 0}function Ra(n){return n}function ic(n){return typeof n=="boolean"?n?"1":void 0:""+n}function kt(n,a){if(n&&typeof n=="object"&&!Array.isArray(n)){for(let t=0;t<a.length;t++){const l=a[t];if(n[l]!=null)return n[l]}return n.base}return n}function Vn(n,a=fi,t={}){const{direction:l}=Mo(),{matchedBreakpoints:i=["base"]}=t,c={style:{...ac(n,a,l,i)}};return kt(n.isHidden,i)&&(c.hidden=!0),{styleProps:c}}const yi=m`
  margin: 0;
  font-weight: 400;
  &[data-size="XS"] {
    font-size: var(--ac-global-font-size-xs);
    line-height: var(--ac-global-line-height-xs);
  }
  &[data-size="S"] {
    font-size: var(--ac-global-font-size-s);
    line-height: var(--ac-global-line-height-s);
  }
  &[data-size="M"] {
    font-size: var(--ac-global-font-size-m);
    line-height: var(--ac-global-line-height-m);
  }
  &[data-size="L"] {
    font-size: var(--ac-global-font-size-l);
    line-height: var(--ac-global-line-height-l);
  }
  &[data-size="XL"] {
    font-size: var(--ac-global-font-size-xl);
    line-height: var(--ac-global-line-height-xl);
  }
  &[data-weight="heavy"] {
    font-weight: 600;
  }
`,rc=m`
  color: var(--ac-global-text-color-900);
  &[data-level="1"] {
    font-size: var(--ac-global-font-size-xl);
    line-height: var(--ac-global-line-height-xl);
  }
  &[data-level="2"] {
    font-size: var(--ac-global-font-size-l);
    line-height: var(--ac-global-line-height-l);
  }
  &[data-level="3"] {
    font-size: var(--ac-global-font-size-m);
    line-height: var(--ac-global-line-height-m);
  }
  &[data-level="4"] {
    font-size: var(--ac-global-font-size-s);
    line-height: var(--ac-global-line-height-s);
  }
  &[data-level="5"] {
    font-size: var(--ac-global-font-size-xs);
    line-height: var(--ac-global-line-height-xs);
  }
  &[data-level="6"] {
    font-size: var(--ac-global-font-size-xxs);
    line-height: var(--ac-global-line-height-xxs);
  }
`,oc=n=>{if(n==="inherit")return"inherit";if(n.startsWith("text-")){const[,a]=n.split("-");return`var(--ac-global-text-color-${a})`}return Un(n)},sc=n=>m(m`
      color: ${oc(n)};
    `,yi);function cc(n,a){const{isDisabled:t=!1}=n,{children:l,color:i=t?"text-300":"text-900",size:r="S",weight:o="normal",fontStyle:c="normal",fontFamily:d="default",...u}=n,{styleProps:g}=Vn(u);return e(Vl,{className:V("ac-text",`font-${d}`),...u,...g,css:m`
        ${sc(i)};
        font-style: ${c};
      `,"data-size":r,"data-weight":o,ref:a,children:l})}const C=p.forwardRef(cc);function dc(n,a){const{children:t,level:l=3,weight:i="normal",...r}=n;return e(Rl,{...r,css:m(yi,rc),className:V("ac-Heading",n.className),ref:a,level:l,"data-level":l,"data-weight":i,children:t})}const ne=p.forwardRef(dc),uc=m`
  font-family:
    -apple-system, "system-ui", "Segoe UI", "Noto Sans", Helvetica, Arial,
    sans-serif, "Apple Color Emoji", "Segoe UI Emoji";
`,gc=p.forwardRef(function({children:a,className:t,...l},i){return e("kbd",{ref:i,css:uc,className:V("ac-keyboard",t),...l,children:a})}),mc=m`
  border: 0;
  clip: rect(0 0 0 0);
  margin: -1px;
  overflow: hidden;
  padding: 0;
  position: absolute;
  width: 1px;
  height: 1px;
`,F7=({children:n})=>e("span",{className:"ac-visually-hidden",css:mc,children:n}),E7=({children:n,bordered:a=!0})=>e("div",{"data-bordered":a,css:m`
        border-bottom: 1px solid var(--ac-global-border-color-default);
        &[data-bordered="true"] {
          border-top: 1px solid var(--ac-global-border-color-default);
        }
        & > * {
          display: flex;
          justify-content: space-between;
          align-items: center;
          padding: var(--ac-global-dimension-static-size-100)
            var(--ac-global-dimension-static-size-200);
        }
      `,children:e(ne,{children:n})});function pc(n){const{message:a}=n;return e("div",{css:m`
        width: 100%;
        display: flex;
        justify-content: center;
      `,children:e("div",{css:m`
          margin: var(--ac-global-dimension-size-300);
          display: flex;
          flex-direction: column;
          align-items: center;
        `,children:a&&e(C,{size:"M",color:"text-700",children:a})})})}function hc({error:n}){return e(w,{padding:"size-200",children:s(S,{direction:"column",children:[e(S,{direction:"column",width:"100%",alignItems:"center",children:e("h1",{children:"Something went wrong"})}),e("p",{children:"We strive to do our very best but 🐛 bugs happen. It would mean a lot to us if you could file a an issue. If you feel comfortable, please include the error details below in your issue. We will get back to you as soon as we can."}),e(S,{direction:"row",width:"100%",justifyContent:"end",children:e(de,{href:"https://github.com/Arize-ai/phoenix/issues/new?assignees=&labels=bug&template=bug_report.md&title=%5BBUG%5D",children:"file an issue with us"})}),s("details",{open:!0,children:[e("summary",{children:"error details"}),e("pre",{css:m`
              white-space: pre-wrap;
              overflow-wrap: break-word;
              overflow: hidden;
              overflow-y: auto;
              max-height: 500px;
            `,children:n})]})]})})}class D7 extends p.Component{constructor(a){super(a),this.state={hasError:!1,error:null}}static getDerivedStateFromError(a){return{hasError:!0,error:a}}componentDidCatch(a,t){}render(){if(this.state.hasError){const a=this.state.error instanceof Error?this.state.error.message:null;return typeof this.props.fallback=="function"?e(this.props.fallback,{error:a}):e(hc,{error:a})}return this.props.children}}function _7(n){return s("div",{css:m`
        text-align: center;
        display: flex;
        color: var(--ac-global-text-color-300);
        gap: var(--ac-global-dimension-size-50);
      `,children:[e(T,{svg:e(Lt,{})}),e(C,{color:"text-300",children:"error"})]})}const fc=m`
  background-color: var(--ac-global-color-primary-100);
  color: var(--ac-global-color-primary-700);
  padding: var(--ac-global-dimension-static-size-50)
    var(--ac-global-dimension-static-size-100);
  font-size: var(--ac-global-dimension-static-font-size-50);
  border-radius: var(--ac-global-dimension-static-size-100);
  border: 1px solid var(--ac-global-color-primary-200);
  box-shadow: 0 2px 0 0 var(--ac-global-color-primary-200);
  // Offset the shadow to make it look like it's on the key
  margin-top: -1px;
  text-transform: uppercase;
`,K7=p.forwardRef(function({children:a,...t},l){return e(gc,{ref:l,css:fc,...t,children:a})}),me=p.forwardRef(({color:n,size:a="M",shape:t="square"},l)=>{const i=typeof n=="string"&&n.startsWith("var"),r=i?m`
          background-color: ${n} !important;
        `:void 0;return e(Fo,{color:i?void 0:n,"data-shape":t,"data-size":a,ref:l,css:m(m`
            --color-swatch-size: 6px;
            width: var(--color-swatch-size);
            height: var(--color-swatch-size);
            display: inline-block;
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
          `,r)})});me.displayName="ColorSwatch";const T=({svg:n,isDisabled:a,color:t="inherit",css:l,className:i="",...r})=>{const o=t==="inherit"?"inherit":Un(t);return e("i",{className:V("ac-icon-wrap",i),css:m(m`
          width: 1em;
          height: 1em;
          font-size: 1.2rem;
          color: ${o};
          display: flex;
          svg {
            fill: currentColor;
            width: 1em;
            height: 1em;
            display: inline-block;
            flex-shrink: 0;
            user-select: none;
          }
        `,l),...r,children:n})},bc=Me`
 100% {
    transform: rotate(360deg);
  }
`,P7=()=>e("svg",{xmlns:"http://www.w3.org/2000/svg",viewBox:"0 0 24 24",children:e("g",{"data-name":"Layer 2",children:s("g",{"data-name":"arrow-back",children:[e("rect",{width:"24",height:"24",transform:"rotate(90 12 12)",opacity:"0"}),e("path",{d:"M19 11H7.14l3.63-4.36a1 1 0 1 0-1.54-1.28l-5 6a1.19 1.19 0 0 0-.09.15c0 .05 0 .08-.07.13A1 1 0 0 0 4 12a1 1 0 0 0 .07.36c0 .05 0 .08.07.13a1.19 1.19 0 0 0 .09.15l5 6A1 1 0 0 0 10 19a1 1 0 0 0 .64-.23 1 1 0 0 0 .13-1.41L7.14 13H19a1 1 0 0 0 0-2z"})]})})}),V7=()=>s("svg",{width:"24",height:"24",viewBox:"0 0 24 24",fill:"none",xmlns:"http://www.w3.org/2000/svg",children:[e("path",{d:"M7.18367 12.44H18.93C19.4765 12.44 19.92 12.8835 19.92 13.43C19.92 13.9765 19.4765 14.42 18.93 14.42H7.18367L10.7803 18.7364C11.1308 19.1562 11.0734 19.7809 10.6536 20.1303C10.4685 20.2848 10.2438 20.36 10.02 20.36C9.73688 20.36 9.45572 20.2382 9.2597 20.0036L4.3097 14.0636C4.27109 14.0171 4.25129 13.9626 4.22258 13.9111C4.19882 13.8696 4.17011 13.8339 4.15229 13.7884C4.10774 13.6745 4.08101 13.5547 4.08101 13.434C4.08101 13.433 4.08002 13.431 4.08002 13.43C4.08002 13.429 4.08101 13.427 4.08101 13.426C4.08101 13.3053 4.10774 13.1855 4.15229 13.0716C4.17011 13.0261 4.19882 12.9904 4.22258 12.9489C4.41566 12.6026 4.86258 12.476 5.25896 12.4699L7.18367 12.44Z"}),e("path",{d:"M16.8964 11.52H5.15003C4.60355 11.52 4.16003 11.0764 4.16003 10.53C4.16003 9.98348 4.60355 9.53996 5.15003 9.53996H16.8964L13.2997 5.22356C12.9493 4.8038 13.0067 4.17911 13.4264 3.82964C13.6116 3.6752 13.8363 3.59996 14.06 3.59996C14.3432 3.59996 14.6243 3.72173 14.8204 3.95636L19.7704 9.89636C19.809 9.94289 19.8288 9.99734 19.8575 10.0488C19.8812 10.0904 19.9099 10.126 19.9278 10.1716C19.9723 10.2854 19.999 10.4052 19.999 10.526C19.999 10.527 20 10.529 20 10.53C20 10.5309 19.999 10.5329 19.999 10.5339C19.999 10.6547 19.9723 10.7745 19.9278 10.8883C19.9099 10.9339 19.8812 10.9695 19.8575 11.0111C19.6644 11.3573 19.2175 11.4839 18.8211 11.4901L16.8964 11.52Z"})]}),yc=()=>e("svg",{xmlns:"http://www.w3.org/2000/svg",viewBox:"0 0 24 24",children:e("g",{"data-name":"Layer 2",children:s("g",{"data-name":"arrow-ios-back",children:[e("rect",{width:"24",height:"24",transform:"rotate(90 12 12)",opacity:"0"}),e("path",{d:"M13.83 19a1 1 0 0 1-.78-.37l-4.83-6a1 1 0 0 1 0-1.27l5-6a1 1 0 0 1 1.54 1.28L10.29 12l4.32 5.36a1 1 0 0 1-.78 1.64z"})]})})}),R7=()=>e("svg",{xmlns:"http://www.w3.org/2000/svg",viewBox:"0 0 24 24",children:e("g",{"data-name":"Layer 2",children:s("g",{"data-name":"arrow-downward",children:[e("rect",{width:"24",height:"24",transform:"rotate(-90 12 12)",opacity:"0"}),e("path",{d:"M12 17a1.72 1.72 0 0 1-1.33-.64l-4.21-5.1a2.1 2.1 0 0 1-.26-2.21A1.76 1.76 0 0 1 7.79 8h8.42a1.76 1.76 0 0 1 1.59 1.05 2.1 2.1 0 0 1-.26 2.21l-4.21 5.1A1.72 1.72 0 0 1 12 17z"})]})})}),vi=()=>e("svg",{xmlns:"http://www.w3.org/2000/svg",viewBox:"0 0 24 24",children:e("g",{"data-name":"Layer 2",children:s("g",{"data-name":"arrow-ios-downward",children:[e("rect",{width:"24",height:"24",opacity:"0"}),e("path",{d:"M12 16a1 1 0 0 1-.64-.23l-6-5a1 1 0 1 1 1.28-1.54L12 13.71l5.36-4.32a1 1 0 0 1 1.41.15 1 1 0 0 1-.14 1.46l-6 4.83A1 1 0 0 1 12 16z"})]})})}),O7=()=>e("svg",{xmlns:"http://www.w3.org/2000/svg",viewBox:"0 0 24 24",children:e("g",{"data-name":"Layer 2",children:s("g",{"data-name":"arrow-upward",children:[e("rect",{width:"24",height:"24",transform:"rotate(180 12 12)",opacity:"0"}),e("path",{d:"M5.23 10.64a1 1 0 0 0 1.41.13L11 7.14V19a1 1 0 0 0 2 0V7.14l4.36 3.63a1 1 0 1 0 1.28-1.54l-6-5-.15-.09-.13-.07a1 1 0 0 0-.72 0l-.13.07-.15.09-6 5a1 1 0 0 0-.13 1.41z"})]})})}),N7=()=>e("svg",{xmlns:"http://www.w3.org/2000/svg",viewBox:"0 0 24 24",children:e("g",{"data-name":"Layer 2",children:s("g",{"data-name":"arrow-downward",children:[e("rect",{width:"24",height:"24",opacity:"0"}),e("path",{d:"M18.77 13.36a1 1 0 0 0-1.41-.13L13 16.86V5a1 1 0 0 0-2 0v11.86l-4.36-3.63a1 1 0 1 0-1.28 1.54l6 5 .15.09.13.07a1 1 0 0 0 .72 0l.13-.07.15-.09 6-5a1 1 0 0 0 .13-1.41z"})]})})}),$7=()=>e("svg",{xmlns:"http://www.w3.org/2000/svg",viewBox:"0 0 24 24",children:e("g",{"data-name":"Layer 2",children:s("g",{"data-name":"arrow-up",children:[e("rect",{width:"24",height:"24",transform:"rotate(90 12 12)",opacity:"0"}),e("path",{d:"M16.21 16H7.79a1.76 1.76 0 0 1-1.59-1 2.1 2.1 0 0 1 .26-2.21l4.21-5.1a1.76 1.76 0 0 1 2.66 0l4.21 5.1A2.1 2.1 0 0 1 17.8 15a1.76 1.76 0 0 1-1.59 1z"})]})})}),Ci=()=>e("svg",{xmlns:"http://www.w3.org/2000/svg",viewBox:"0 0 24 24",children:e("g",{"data-name":"Layer 2",children:s("g",{"data-name":"arrow-ios-forward",children:[e("rect",{width:"24",height:"24",transform:"rotate(-90 12 12)",opacity:"0"}),e("path",{d:"M10 19a1 1 0 0 1-.64-.23 1 1 0 0 1-.13-1.41L13.71 12 9.39 6.63a1 1 0 0 1 .15-1.41 1 1 0 0 1 1.46.15l4.83 6a1 1 0 0 1 0 1.27l-5 6A1 1 0 0 1 10 19z"})]})})}),vc=()=>e("svg",{xmlns:"http://www.w3.org/2000/svg",viewBox:"0 0 24 24",children:e("g",{"data-name":"Layer 2",children:s("g",{"data-name":"alert-triangle",children:[e("rect",{width:"24",height:"24",transform:"rotate(90 12 12)",opacity:"0"}),e("path",{d:"M22.56 16.3L14.89 3.58a3.43 3.43 0 0 0-5.78 0L1.44 16.3a3 3 0 0 0-.05 3A3.37 3.37 0 0 0 4.33 21h15.34a3.37 3.37 0 0 0 2.94-1.66 3 3 0 0 0-.05-3.04zm-1.7 2.05a1.31 1.31 0 0 1-1.19.65H4.33a1.31 1.31 0 0 1-1.19-.65 1 1 0 0 1 0-1l7.68-12.73a1.48 1.48 0 0 1 2.36 0l7.67 12.72a1 1 0 0 1 .01 1.01z"}),e("circle",{cx:"12",cy:"16",r:"1"}),e("path",{d:"M12 8a1 1 0 0 0-1 1v4a1 1 0 0 0 2 0V9a1 1 0 0 0-1-1z"})]})})}),Cc=()=>e("svg",{xmlns:"http://www.w3.org/2000/svg",viewBox:"0 0 24 24",children:e("g",{"data-name":"Layer 2",children:s("g",{"data-name":"alert-triangle",children:[e("rect",{width:"24",height:"24",transform:"rotate(90 12 12)",opacity:"0"}),e("path",{d:"M22.56 16.3L14.89 3.58a3.43 3.43 0 0 0-5.78 0L1.44 16.3a3 3 0 0 0-.05 3A3.37 3.37 0 0 0 4.33 21h15.34a3.37 3.37 0 0 0 2.94-1.66 3 3 0 0 0-.05-3.04zM12 17a1 1 0 1 1 1-1 1 1 0 0 1-1 1zm1-4a1 1 0 0 1-2 0V9a1 1 0 0 1 2 0z"})]})})}),Lt=()=>e("svg",{xmlns:"http://www.w3.org/2000/svg",viewBox:"0 0 24 24",children:e("g",{"data-name":"Layer 2",children:s("g",{"data-name":"alert-circle",children:[e("rect",{width:"24",height:"24",opacity:"0"}),e("path",{d:"M12 2a10 10 0 1 0 10 10A10 10 0 0 0 12 2zm0 18a8 8 0 1 1 8-8 8 8 0 0 1-8 8z"}),e("circle",{cx:"12",cy:"16",r:"1"}),e("path",{d:"M12 7a1 1 0 0 0-1 1v5a1 1 0 0 0 2 0V8a1 1 0 0 0-1-1z"})]})})}),ki=()=>e("svg",{xmlns:"http://www.w3.org/2000/svg",viewBox:"0 0 24 24",children:e("g",{"data-name":"Layer 2",children:s("g",{"data-name":"alert-circle",children:[e("rect",{width:"24",height:"24",opacity:"0"}),e("path",{d:"M12 2a10 10 0 1 0 10 10A10 10 0 0 0 12 2zm0 15a1 1 0 1 1 1-1 1 1 0 0 1-1 1zm1-4a1 1 0 0 1-2 0V8a1 1 0 0 1 2 0z"})]})})}),kc=()=>e("svg",{xmlns:"http://www.w3.org/2000/svg",viewBox:"0 0 24 24",children:e("g",{"data-name":"Layer 2",children:s("g",{"data-name":"bar-chart",children:[e("rect",{width:"24",height:"24",transform:"rotate(90 12 12)",opacity:"0"}),e("path",{d:"M12 4a1 1 0 0 0-1 1v15a1 1 0 0 0 2 0V5a1 1 0 0 0-1-1z"}),e("path",{d:"M19 12a1 1 0 0 0-1 1v7a1 1 0 0 0 2 0v-7a1 1 0 0 0-1-1z"}),e("path",{d:"M5 8a1 1 0 0 0-1 1v11a1 1 0 0 0 2 0V9a1 1 0 0 0-1-1z"})]})})}),B7=()=>e("svg",{xmlns:"http://www.w3.org/2000/svg",viewBox:"0 0 24 24",children:e("g",{"data-name":"Layer 2",children:s("g",{"data-name":"book",children:[e("rect",{width:"24",height:"24",opacity:"0"}),e("path",{d:"M19 3H7a3 3 0 0 0-3 3v12a3 3 0 0 0 3 3h12a1 1 0 0 0 1-1V4a1 1 0 0 0-1-1zM7 19a1 1 0 0 1 0-2h11v2z"})]})})}),Lc=()=>e("svg",{xmlns:"http://www.w3.org/2000/svg",viewBox:"0 0 24 24",children:e("g",{"data-name":"Layer 2",children:s("g",{"data-name":"book",children:[e("rect",{width:"24",height:"24",opacity:"0"}),e("path",{d:"M19 3H7a3 3 0 0 0-3 3v12a3 3 0 0 0 3 3h12a1 1 0 0 0 1-1V4a1 1 0 0 0-1-1zM7 5h11v10H7a3 3 0 0 0-1 .18V6a1 1 0 0 1 1-1zm0 14a1 1 0 0 1 0-2h11v2z"})]})})}),H7=()=>e("svg",{xmlns:"http://www.w3.org/2000/svg",viewBox:"0 0 24 24",children:e("g",{"data-name":"Layer 2",children:s("g",{"data-name":"bulb",children:[e("rect",{width:"24",height:"24",transform:"rotate(180 12 12)",opacity:"0"}),e("path",{d:"M12 7a5 5 0 0 0-3 9v4a2 2 0 0 0 2 2h2a2 2 0 0 0 2-2v-4a5 5 0 0 0-3-9zm1.5 7.59a1 1 0 0 0-.5.87V20h-2v-4.54a1 1 0 0 0-.5-.87A3 3 0 0 1 9 12a3 3 0 0 1 6 0 3 3 0 0 1-1.5 2.59z"}),e("path",{d:"M12 6a1 1 0 0 0 1-1V3a1 1 0 0 0-2 0v2a1 1 0 0 0 1 1z"}),e("path",{d:"M21 11h-2a1 1 0 0 0 0 2h2a1 1 0 0 0 0-2z"}),e("path",{d:"M5 11H3a1 1 0 0 0 0 2h2a1 1 0 0 0 0-2z"}),e("path",{d:"M7.66 6.42L6.22 5a1 1 0 0 0-1.39 1.47l1.44 1.39a1 1 0 0 0 .73.28 1 1 0 0 0 .72-.31 1 1 0 0 0-.06-1.41z"}),e("path",{d:"M19.19 5.05a1 1 0 0 0-1.41 0l-1.44 1.37a1 1 0 0 0 0 1.41 1 1 0 0 0 .72.31 1 1 0 0 0 .69-.28l1.44-1.39a1 1 0 0 0 0-1.42z"})]})})}),wc=()=>e("svg",{xmlns:"http://www.w3.org/2000/svg",viewBox:"0 0 24 24",children:e("g",{"data-name":"Layer 2",children:s("g",{"data-name":"calendar",children:[e("rect",{width:"24",height:"24",opacity:"0"}),e("path",{d:"M18 4h-1V3a1 1 0 0 0-2 0v1H9V3a1 1 0 0 0-2 0v1H6a3 3 0 0 0-3 3v12a3 3 0 0 0 3 3h12a3 3 0 0 0 3-3V7a3 3 0 0 0-3-3zM6 6h1v1a1 1 0 0 0 2 0V6h6v1a1 1 0 0 0 2 0V6h1a1 1 0 0 1 1 1v4H5V7a1 1 0 0 1 1-1zm12 14H6a1 1 0 0 1-1-1v-6h14v6a1 1 0 0 1-1 1z"}),e("circle",{cx:"8",cy:"16",r:"1"}),e("path",{d:"M16 15h-4a1 1 0 0 0 0 2h4a1 1 0 0 0 0-2z"})]})})}),Sc=()=>s("svg",{xmlns:"http://www.w3.org/2000/svg",height:"24",viewBox:"0 0 18 18",width:"24",children:[e("path",{className:"fill",d:"M14,5.99a1,1,0,0,1-1.7055.7055L9.006,3.409,5.717,6.695A1,1,0,0,1,4.28,5.3085l.0245-.0245L8.3,1.2925a1,1,0,0,1,1.4125,0L13.707,5.284A.99446.99446,0,0,1,14,5.99Z"}),e("path",{className:"fill",d:"M4,12.01a1,1,0,0,1,1.7055-.7055l3.289,3.286,3.289-3.286a1,1,0,0,1,1.437,1.3865l-.0245.0245L9.7,16.707a1,1,0,0,1-1.4125,0L4.293,12.7155A.99452.99452,0,0,1,4,12.01Z"})]}),j7=()=>e("svg",{width:"12",height:"13",viewBox:"0 0 12 13",fill:"none",xmlns:"http://www.w3.org/2000/svg",children:e("path",{d:"M2.2 12.4H9.8C10.0889 12.4 10.375 12.3431 10.6419 12.2325C10.9088 12.122 11.1513 11.9599 11.3556 11.7556C11.5599 11.5513 11.722 11.3088 11.8325 11.0419C11.9431 10.775 12 10.4889 12 10.2V2.2C12 1.91109 11.9431 1.62501 11.8325 1.3581C11.722 1.09118 11.5599 0.848654 11.3556 0.644365C11.1513 0.440076 10.9088 0.278026 10.6419 0.167465C10.375 0.0569049 10.0889 0 9.8 0H2.2C1.61652 0 1.05694 0.231785 0.644365 0.644365C0.231785 1.05694 0 1.61652 0 2.2V10.2C0 10.7835 0.231785 11.3431 0.644365 11.7556C1.05694 12.1682 1.61652 12.4 2.2 12.4ZM4.8 11.2V1.2H7.2V11.2H4.8ZM10.8 2.2V10.2C10.8 10.4652 10.6946 10.7196 10.5071 10.9071C10.3196 11.0946 10.0652 11.2 9.8 11.2H8.4V1.2H9.8C10.0652 1.2 10.3196 1.30536 10.5071 1.49289C10.6946 1.68043 10.8 1.93478 10.8 2.2ZM1.2 2.2C1.2 1.93478 1.30536 1.68043 1.49289 1.49289C1.68043 1.30536 1.93478 1.2 2.2 1.2H3.6V11.2H2.2C1.93478 11.2 1.68043 11.0946 1.49289 10.9071C1.30536 10.7196 1.2 10.4652 1.2 10.2V2.2Z"})}),Z7=()=>e("svg",{xmlns:"http://www.w3.org/2000/svg",viewBox:"0 0 24 24",children:e("g",{"data-name":"Layer 2",children:s("g",{"data-name":"corner-up-right",children:[e("rect",{width:"24",height:"24",transform:"rotate(-90 12 12)",opacity:"0"}),e("path",{d:"M19.78 10.38l-4-5a1 1 0 0 0-1.56 1.24l2.7 3.38H8a3 3 0 0 0-3 3v5a1 1 0 0 0 2 0v-5a1 1 0 0 1 1-1h8.92l-2.7 3.38a1 1 0 0 0 .16 1.4A1 1 0 0 0 15 17a1 1 0 0 0 .78-.38l4-5a1 1 0 0 0 0-1.24z"})]})})}),U7=()=>e("svg",{xmlns:"http://www.w3.org/2000/svg",viewBox:"0 0 24 24",children:e("g",{"data-name":"Layer 2",children:s("g",{"data-name":"code",children:[e("rect",{width:"24",height:"24",transform:"rotate(90 12 12)",opacity:"0"}),e("path",{d:"M8.64 5.23a1 1 0 0 0-1.41.13l-5 6a1 1 0 0 0 0 1.27l4.83 6a1 1 0 0 0 .78.37 1 1 0 0 0 .78-1.63L4.29 12l4.48-5.36a1 1 0 0 0-.13-1.41z"}),e("path",{d:"M21.78 11.37l-4.78-6a1 1 0 0 0-1.41-.15 1 1 0 0 0-.15 1.41L19.71 12l-4.48 5.37a1 1 0 0 0 .13 1.41A1 1 0 0 0 16 19a1 1 0 0 0 .77-.36l5-6a1 1 0 0 0 .01-1.27z"})]})})}),G7=()=>e("svg",{xmlns:"http://www.w3.org/2000/svg",viewBox:"0 0 24 24",children:e("g",{"data-name":"Layer 2",children:s("g",{"data-name":"chevron-left",children:[e("rect",{width:"24",height:"24",transform:"rotate(90 12 12)",opacity:"0"}),e("path",{d:"M13.36 17a1 1 0 0 1-.72-.31l-3.86-4a1 1 0 0 1 0-1.4l4-4a1 1 0 1 1 1.42 1.42L10.9 12l3.18 3.3a1 1 0 0 1 0 1.41 1 1 0 0 1-.72.29z"})]})})}),xc=()=>e("svg",{xmlns:"http://www.w3.org/2000/svg",viewBox:"0 0 24 24",children:e("g",{"data-name":"Layer 2",children:s("g",{"data-name":"chevron-right",children:[e("rect",{width:"24",height:"24",transform:"rotate(-90 12 12)",opacity:"0"}),e("path",{d:"M10.5 17a1 1 0 0 1-.71-.29 1 1 0 0 1 0-1.42L13.1 12 9.92 8.69a1 1 0 0 1 0-1.41 1 1 0 0 1 1.42 0l3.86 4a1 1 0 0 1 0 1.4l-4 4a1 1 0 0 1-.7.32z"})]})})}),Tc=()=>e("svg",{xmlns:"http://www.w3.org/2000/svg",viewBox:"0 0 24 24",children:e("g",{"data-name":"Layer 2",children:s("g",{"data-name":"chevron-right",children:[e("rect",{width:"24",height:"24",transform:"rotate(-90 12 12)",opacity:"0"}),e("path",{d:"M10.5 17a1 1 0 0 1-.71-.29 1 1 0 0 1 0-1.42L13.1 12 9.92 8.69a1 1 0 0 1 0-1.41 1 1 0 0 1 1.42 0l3.86 4a1 1 0 0 1 0 1.4l-4 4a1 1 0 0 1-.7.32z"})]})})}),Ac=()=>e("svg",{xmlns:"http://www.w3.org/2000/svg",viewBox:"0 0 24 24",children:e("g",{"data-name":"Layer 2",children:s("g",{"data-name":"chevron-down",children:[e("rect",{width:"24",height:"24",opacity:"0"}),e("path",{d:"M12 15.5a1 1 0 0 1-.71-.29l-4-4a1 1 0 1 1 1.42-1.42L12 13.1l3.3-3.18a1 1 0 1 1 1.38 1.44l-4 3.86a1 1 0 0 1-.68.28z"})]})})}),Ic=()=>e("svg",{xmlns:"http://www.w3.org/2000/svg",viewBox:"0 0 24 24",children:e("g",{"data-name":"Layer 2",children:s("g",{"data-name":"chevron-down",children:[e("rect",{width:"24",height:"24",opacity:"0"}),e("path",{d:"M12 15.5a1 1 0 0 1-.71-.29l-4-4a1 1 0 1 1 1.42-1.42L12 13.1l3.3-3.18a1 1 0 1 1 1.38 1.44l-4 3.86a1 1 0 0 1-.68.28z"})]})})}),Q7=()=>e("svg",{width:"24",height:"24",viewBox:"0 0 24 24",xmlns:"http://www.w3.org/2000/svg",children:s("g",{id:"cube",children:[e("path",{fillRule:"evenodd",clipRule:"evenodd",d:"M20.654 7.24778C20.6545 7.25157 20.655 7.25534 20.6564 7.25891C20.8684 7.62191 20.9994 8.02891 21.0004 8.45691V15.5399C20.9994 16.4879 20.4224 17.3659 19.5304 17.7779L13.1334 20.7499C12.7724 20.9179 12.3844 21.0019 11.9964 21.0019C11.6074 21.0019 11.2194 20.9179 10.8574 20.7489L4.45839 17.7769C3.56439 17.3589 2.99239 16.4749 3.00039 15.5249V8.45791C3.00039 8.02991 3.13139 7.62291 3.34239 7.26091C3.34439 7.25641 3.34514 7.25191 3.34589 7.24741C3.34664 7.24291 3.34739 7.23841 3.34939 7.23391C3.35141 7.22986 3.35446 7.22633 3.35763 7.22266C3.36072 7.21907 3.36392 7.21536 3.36639 7.21091C3.40377 7.14975 3.44764 7.09363 3.49188 7.03705C3.49972 7.02703 3.50756 7.017 3.51539 7.00691C3.52685 6.99407 3.53758 6.98061 3.54827 6.96723C3.56835 6.94207 3.58824 6.91715 3.61239 6.89691C3.84739 6.62091 4.12539 6.37891 4.46939 6.21991L10.8664 3.24791C11.5874 2.91591 12.4124 2.91491 13.1314 3.24691C13.1314 3.24791 13.1324 3.24791 13.1334 3.24791L19.5334 6.22091C19.8774 6.37991 20.1544 6.62291 20.3894 6.89891C20.4111 6.91742 20.4291 6.93959 20.4474 6.96205C20.4577 6.97478 20.4682 6.98761 20.4794 6.99991C20.492 7.01663 20.5049 7.03318 20.5177 7.04972C20.5586 7.10243 20.5994 7.15507 20.6344 7.21291C20.6365 7.21633 20.6392 7.21919 20.6418 7.22198C20.6453 7.22572 20.6487 7.22933 20.6504 7.23391C20.6526 7.23834 20.6533 7.24308 20.654 7.24778ZM11.7074 5.06391C11.7984 5.02091 11.8994 4.99991 12.0004 4.99991C12.1004 4.99991 12.2014 5.02091 12.2924 5.06391L17.6214 7.53791L12.0004 10.1499L6.37839 7.53791L11.7074 5.06391ZM5.00039 15.5319C4.99839 15.7139 5.11439 15.8759 5.30339 15.9639L11.0004 18.6089V11.8909L5.00039 9.10391V15.5319ZM13.0004 18.6069L18.6904 15.9629C18.8824 15.8749 19.0004 15.7129 19.0004 15.5389V9.10391L13.0004 11.8909V18.6069Z"}),e("mask",{id:"mask0_0_196",mask:"alpha",maskUnits:"userSpaceOnUse",x:"3",y:"2",width:"19",height:"20",children:e("path",{fillRule:"evenodd",clipRule:"evenodd",d:"M20.654 7.24778C20.6545 7.25157 20.655 7.25534 20.6564 7.25891C20.8684 7.62191 20.9994 8.02891 21.0004 8.45691V15.5399C20.9994 16.4879 20.4224 17.3659 19.5304 17.7779L13.1334 20.7499C12.7724 20.9179 12.3844 21.0019 11.9964 21.0019C11.6074 21.0019 11.2194 20.9179 10.8574 20.7489L4.45839 17.7769C3.56439 17.3589 2.99239 16.4749 3.00039 15.5249V8.45791C3.00039 8.02991 3.13139 7.62291 3.34239 7.26091C3.34439 7.25641 3.34514 7.25191 3.34589 7.24741C3.34664 7.24291 3.34739 7.23841 3.34939 7.23391C3.35141 7.22986 3.35446 7.22633 3.35763 7.22266C3.36072 7.21907 3.36392 7.21536 3.36639 7.21091C3.40377 7.14975 3.44764 7.09363 3.49188 7.03705C3.49972 7.02703 3.50756 7.017 3.51539 7.00691C3.52685 6.99407 3.53758 6.98061 3.54827 6.96723C3.56835 6.94207 3.58824 6.91715 3.61239 6.89691C3.84739 6.62091 4.12539 6.37891 4.46939 6.21991L10.8664 3.24791C11.5874 2.91591 12.4124 2.91491 13.1314 3.24691C13.1314 3.24791 13.1324 3.24791 13.1334 3.24791L19.5334 6.22091C19.8774 6.37991 20.1544 6.62291 20.3894 6.89891C20.4111 6.91742 20.4291 6.93959 20.4474 6.96205C20.4577 6.97478 20.4682 6.98761 20.4794 6.99991C20.492 7.01663 20.5049 7.03318 20.5177 7.04972C20.5586 7.10243 20.5994 7.15507 20.6344 7.21291C20.6365 7.21633 20.6392 7.21919 20.6418 7.22198C20.6453 7.22572 20.6487 7.22933 20.6504 7.23391C20.6526 7.23834 20.6533 7.24308 20.654 7.24778ZM11.7074 5.06391C11.7984 5.02091 11.8994 4.99991 12.0004 4.99991C12.1004 4.99991 12.2014 5.02091 12.2924 5.06391L17.6214 7.53791L12.0004 10.1499L6.37839 7.53791L11.7074 5.06391ZM5.00039 15.5319C4.99839 15.7139 5.11439 15.8759 5.30339 15.9639L11.0004 18.6089V11.8909L5.00039 9.10391V15.5319ZM13.0004 18.6069L18.6904 15.9629C18.8824 15.8749 19.0004 15.7129 19.0004 15.5389V9.10391L13.0004 11.8909V18.6069Z"})}),e("g",{mask:"url(#mask0_0_196)"})]})}),zc=()=>e("svg",{xmlns:"http://www.w3.org/2000/svg",viewBox:"0 0 24 24",children:e("g",{"data-name":"Layer 2",children:s("g",{"data-name":"clock",children:[e("rect",{width:"24",height:"24",transform:"rotate(180 12 12)",opacity:"0"}),e("path",{d:"M12 2a10 10 0 1 0 10 10A10 10 0 0 0 12 2zm0 18a8 8 0 1 1 8-8 8 8 0 0 1-8 8z"}),e("path",{d:"M16 11h-3V8a1 1 0 0 0-2 0v4a1 1 0 0 0 1 1h4a1 1 0 0 0 0-2z"})]})})}),Li=()=>e("svg",{xmlns:"http://www.w3.org/2000/svg",viewBox:"0 0 24 24",children:e("g",{"data-name":"Layer 2",children:s("g",{"data-name":"checkmark",children:[e("rect",{width:"24",height:"24",opacity:"0"}),e("path",{d:"M9.86 18a1 1 0 0 1-.73-.32l-4.86-5.17a1 1 0 1 1 1.46-1.37l4.12 4.39 8.41-9.2a1 1 0 1 1 1.48 1.34l-9.14 10a1 1 0 0 1-.73.33z"})]})})}),Mc=()=>e("svg",{xmlns:"http://www.w3.org/2000/svg",viewBox:"0 0 24 24",children:e("g",{"data-name":"Layer 2",children:s("g",{"data-name":"checkmark",children:[e("rect",{width:"24",height:"24",opacity:"0"}),e("path",{d:"M9.86 18a1 1 0 0 1-.73-.32l-4.86-5.17a1 1 0 1 1 1.46-1.37l4.12 4.39 8.41-9.2a1 1 0 1 1 1.48 1.34l-9.14 10a1 1 0 0 1-.73.33z"})]})})}),wi=()=>e("svg",{width:"24",height:"24",viewBox:"0 0 24 24",fill:"none",xmlns:"http://www.w3.org/2000/svg",children:s("g",{children:[e("path",{fillRule:"evenodd",clipRule:"evenodd",d:"M20.997 10.9741H21C21.551 10.9741 21.999 11.4201 22 11.9711C22.008 14.6421 20.975 17.1571 19.091 19.0511C17.208 20.9451 14.7 21.9921 12.029 22.0001H12C9.339 22.0001 6.836 20.9681 4.949 19.0911C3.055 17.2081 2.008 14.7001 2 12.0291C1.992 9.3571 3.025 6.8431 4.909 4.9491C6.792 3.0551 9.3 2.0081 11.971 2.0001C12.766 2.0121 13.576 2.0921 14.352 2.2781C14.888 2.4081 15.219 2.9481 15.089 3.4851C14.96 4.0211 14.417 4.3511 13.883 4.2231C13.262 4.0731 12.603 4.0101 11.977 4.0001C9.84 4.0061 7.833 4.8441 6.327 6.3591C4.82 7.8741 3.994 9.8861 4 12.0231C4.006 14.1601 4.844 16.1661 6.359 17.6731C7.869 19.1741 9.871 20.0001 12 20.0001H12.023C14.16 19.9941 16.167 19.1561 17.673 17.6411C19.18 16.1251 20.006 14.1141 20 11.9771C19.999 11.4251 20.445 10.9751 20.997 10.9741ZM8.293 11.293C8.684 10.902 9.316 10.902 9.707 11.293L11.951 13.537L18.248 6.341C18.612 5.928 19.243 5.884 19.659 6.248C20.074 6.611 20.116 7.243 19.752 7.659L12.752 15.659C12.57 15.867 12.31 15.99 12.033 16H12C11.735 16 11.481 15.895 11.293 15.707L8.293 12.707C7.902 12.316 7.902 11.684 8.293 11.293Z"}),e("mask",{mask:"alpha",maskUnits:"userSpaceOnUse",x:"2",y:"2",width:"20",height:"20",children:e("path",{fillRule:"evenodd",clipRule:"evenodd",d:"M20.997 10.9741H21C21.551 10.9741 21.999 11.4201 22 11.9711C22.008 14.6421 20.975 17.1571 19.091 19.0511C17.208 20.9451 14.7 21.9921 12.029 22.0001H12C9.339 22.0001 6.836 20.9681 4.949 19.0911C3.055 17.2081 2.008 14.7001 2 12.0291C1.992 9.3571 3.025 6.8431 4.909 4.9491C6.792 3.0551 9.3 2.0081 11.971 2.0001C12.766 2.0121 13.576 2.0921 14.352 2.2781C14.888 2.4081 15.219 2.9481 15.089 3.4851C14.96 4.0211 14.417 4.3511 13.883 4.2231C13.262 4.0731 12.603 4.0101 11.977 4.0001C9.84 4.0061 7.833 4.8441 6.327 6.3591C4.82 7.8741 3.994 9.8861 4 12.0231C4.006 14.1601 4.844 16.1661 6.359 17.6731C7.869 19.1741 9.871 20.0001 12 20.0001H12.023C14.16 19.9941 16.167 19.1561 17.673 17.6411C19.18 16.1251 20.006 14.1141 20 11.9771C19.999 11.4251 20.445 10.9751 20.997 10.9741ZM8.293 11.293C8.684 10.902 9.316 10.902 9.707 11.293L11.951 13.537L18.248 6.341C18.612 5.928 19.243 5.884 19.659 6.248C20.074 6.611 20.116 7.243 19.752 7.659L12.752 15.659C12.57 15.867 12.31 15.99 12.033 16H12C11.735 16 11.481 15.895 11.293 15.707L8.293 12.707C7.902 12.316 7.902 11.684 8.293 11.293Z"})}),e("g",{mask:"url(#mask0)"})]})}),wt=()=>e("svg",{xmlns:"http://www.w3.org/2000/svg",viewBox:"0 0 24 24",children:e("g",{"data-name":"Layer 2",children:s("g",{"data-name":"checkmark-circle-2",children:[e("rect",{width:"24",height:"24",opacity:"0"}),e("path",{d:"M12 2a10 10 0 1 0 10 10A10 10 0 0 0 12 2zm4.3 7.61l-4.57 6a1 1 0 0 1-.79.39 1 1 0 0 1-.79-.38l-2.44-3.11a1 1 0 0 1 1.58-1.23l1.63 2.08 3.78-5a1 1 0 1 1 1.6 1.22z"})]})})}),Fc=()=>e("svg",{xmlns:"http://www.w3.org/2000/svg",viewBox:"0 0 24 24",children:e("g",{"data-name":"Layer 2",children:s("g",{"data-name":"close-circle",children:[e("rect",{width:"24",height:"24",opacity:"0"}),e("path",{d:"M12 2a10 10 0 1 0 10 10A10 10 0 0 0 12 2zm2.71 11.29a1 1 0 0 1 0 1.42 1 1 0 0 1-1.42 0L12 13.41l-1.29 1.3a1 1 0 0 1-1.42 0 1 1 0 0 1 0-1.42l1.3-1.29-1.3-1.29a1 1 0 0 1 1.42-1.42l1.29 1.3 1.29-1.3a1 1 0 0 1 1.42 1.42L13.41 12z"})]})})}),ba=()=>e("svg",{xmlns:"http://www.w3.org/2000/svg",viewBox:"0 0 24 24",children:e("g",{"data-name":"Layer 2",children:s("g",{"data-name":"close",children:[e("rect",{width:"24",height:"24",transform:"rotate(180 12 12)",opacity:"0"}),e("path",{d:"M13.41 12l4.3-4.29a1 1 0 1 0-1.42-1.42L12 10.59l-4.29-4.3a1 1 0 0 0-1.42 1.42l4.3 4.29-4.3 4.29a1 1 0 0 0 0 1.42 1 1 0 0 0 1.42 0l4.29-4.3 4.29 4.3a1 1 0 0 0 1.42 0 1 1 0 0 0 0-1.42z"})]})})}),W7=()=>e("svg",{xmlns:"http://www.w3.org/2000/svg",viewBox:"0 0 24 24",children:e("g",{"data-name":"Layer 2",children:s("g",{"data-name":"close-circle",children:[e("rect",{width:"24",height:"24",opacity:"0"}),e("path",{d:"M12 2a10 10 0 1 0 10 10A10 10 0 0 0 12 2zm0 18a8 8 0 1 1 8-8 8 8 0 0 1-8 8z"}),e("path",{d:"M14.71 9.29a1 1 0 0 0-1.42 0L12 10.59l-1.29-1.3a1 1 0 0 0-1.42 1.42l1.3 1.29-1.3 1.29a1 1 0 0 0 0 1.42 1 1 0 0 0 1.42 0l1.29-1.3 1.29 1.3a1 1 0 0 0 1.42 0 1 1 0 0 0 0-1.42L13.41 12l1.3-1.29a1 1 0 0 0 0-1.42z"})]})})}),Si=()=>e("svg",{xmlns:"http://www.w3.org/2000/svg",viewBox:"0 0 24 24",children:e("g",{"data-name":"Layer 2",children:s("g",{"data-name":"clipboard",children:[e("rect",{width:"24",height:"24",opacity:"0"}),e("path",{d:"M18 5V4a2 2 0 0 0-2-2H8a2 2 0 0 0-2 2v1a3 3 0 0 0-3 3v11a3 3 0 0 0 3 3h12a3 3 0 0 0 3-3V8a3 3 0 0 0-3-3zM8 4h8v4H8V4zm11 15a1 1 0 0 1-1 1H6a1 1 0 0 1-1-1V8a1 1 0 0 1 1-1v1a2 2 0 0 0 2 2h8a2 2 0 0 0 2-2V7a1 1 0 0 1 1 1z"})]})})}),q7=()=>e("svg",{xmlns:"http://www.w3.org/2000/svg",viewBox:"0 0 24 24",children:e("g",{"data-name":"Layer 2",children:s("g",{"data-name":"collapse",children:[e("rect",{width:"24",height:"24",transform:"rotate(180 12 12)",opacity:"0"}),e("path",{d:"M19 9h-2.58l3.29-3.29a1 1 0 1 0-1.42-1.42L15 7.57V5a1 1 0 0 0-1-1 1 1 0 0 0-1 1v5a1 1 0 0 0 1 1h5a1 1 0 0 0 0-2z"}),e("path",{d:"M10 13H5a1 1 0 0 0 0 2h2.57l-3.28 3.29a1 1 0 0 0 0 1.42 1 1 0 0 0 1.42 0L9 16.42V19a1 1 0 0 0 1 1 1 1 0 0 0 1-1v-5a1 1 0 0 0-1-1z"})]})})}),X7=()=>s("svg",{width:"24",height:"24",viewBox:"0 0 24 24",stroke:"currentColor",xmlns:"http://www.w3.org/2000/svg",children:[e("path",{d:"M12 8.66669C16.1421 8.66669 19.5 7.5474 19.5 6.16669C19.5 4.78598 16.1421 3.66669 12 3.66669C7.85786 3.66669 4.5 4.78598 4.5 6.16669C4.5 7.5474 7.85786 8.66669 12 8.66669Z",strokeWidth:"2",fill:"none",strokeLinecap:"round",strokeLinejoin:"round"}),e("path",{d:"M19.5 12C19.5 13.3833 16.1667 14.5 12 14.5C7.83333 14.5 4.5 13.3833 4.5 12",strokeWidth:"2",fill:"none",strokeLinecap:"round",strokeLinejoin:"round"}),e("path",{d:"M4.5 6.16669V17.8334C4.5 19.2167 7.83333 20.3334 12 20.3334C16.1667 20.3334 19.5 19.2167 19.5 17.8334V6.16669",strokeWidth:"2",fill:"none",strokeLinecap:"round",strokeLinejoin:"round"})]}),Y7=()=>e("svg",{xmlns:"http://www.w3.org/2000/svg",viewBox:"0 0 24 24",children:e("g",{"data-name":"Layer 2",children:s("g",{"data-name":"download",children:[e("rect",{width:"24",height:"24",opacity:"0"}),e("rect",{x:"4",y:"18",width:"16",height:"2",rx:"1",ry:"1"}),e("rect",{x:"3",y:"17",width:"4",height:"2",rx:"1",ry:"1",transform:"rotate(-90 5 18)"}),e("rect",{x:"17",y:"17",width:"4",height:"2",rx:"1",ry:"1",transform:"rotate(-90 19 18)"}),e("path",{d:"M12 15a1 1 0 0 1-.58-.18l-4-2.82a1 1 0 0 1-.24-1.39 1 1 0 0 1 1.4-.24L12 12.76l3.4-2.56a1 1 0 0 1 1.2 1.6l-4 3a1 1 0 0 1-.6.2z"}),e("path",{d:"M12 13a1 1 0 0 1-1-1V4a1 1 0 0 1 2 0v8a1 1 0 0 1-1 1z"})]})})}),J7=()=>s("svg",{width:"24",height:"24",viewBox:"0 0 24 24",fill:"none",xmlns:"http://www.w3.org/2000/svg",children:[e("path",{fillRule:"evenodd",clipRule:"evenodd",d:"M9 13V12C9 10.346 10.346 9 12 9H13V5.667C13 5.299 12.701 5 12.333 5H5.667C5.299 5 5 5.299 5 5.667V12.333C5 12.701 5.299 13 5.667 13H9ZM9 15H5.667C4.196 15 3 13.804 3 12.333V5.667C3 4.196 4.196 3 5.667 3H12.333C13.804 3 15 4.196 15 5.667V9H18C19.654 9 21 10.346 21 12V18C21 19.654 19.654 21 18 21H12C10.346 21 9 19.654 9 18V15ZM12 11C11.449 11 11 11.449 11 12V18C11 18.551 11.449 19 12 19H18C18.552 19 19 18.551 19 18V12C19 11.449 18.552 11 18 11H12Z"}),e("mask",{id:"mask0_725_12898",style:{maskType:"alpha"},maskUnits:"userSpaceOnUse",x:"3",y:"3",width:"18",height:"18",children:e("path",{fillRule:"evenodd",clipRule:"evenodd",d:"M9 13V12C9 10.346 10.346 9 12 9H13V5.667C13 5.299 12.701 5 12.333 5H5.667C5.299 5 5 5.299 5 5.667V12.333C5 12.701 5.299 13 5.667 13H9ZM9 15H5.667C4.196 15 3 13.804 3 12.333V5.667C3 4.196 4.196 3 5.667 3H12.333C13.804 3 15 4.196 15 5.667V9H18C19.654 9 21 10.346 21 12V18C21 19.654 19.654 21 18 21H12C10.346 21 9 19.654 9 18V15ZM12 11C11.449 11 11 11.449 11 12V18C11 18.551 11.449 19 12 19H18C18.552 19 19 18.551 19 18V12C19 11.449 18.552 11 18 11H12Z"})}),e("g",{mask:"url(#mask0_725_12898)"})]}),e8=()=>e("svg",{xmlns:"http://www.w3.org/2000/svg",viewBox:"0 0 24 24",children:e("g",{"data-name":"Layer 2",children:s("g",{"data-name":"edit",children:[e("rect",{width:"24",height:"24",opacity:"0"}),e("path",{d:"M19.4 7.34L16.66 4.6A2 2 0 0 0 14 4.53l-9 9a2 2 0 0 0-.57 1.21L4 18.91a1 1 0 0 0 .29.8A1 1 0 0 0 5 20h.09l4.17-.38a2 2 0 0 0 1.21-.57l9-9a1.92 1.92 0 0 0-.07-2.71zM9.08 17.62l-3 .28.27-3L12 9.32l2.7 2.7zM16 10.68L13.32 8l1.95-2L18 8.73z"})]})})}),n8=()=>e("svg",{xmlns:"http://www.w3.org/2000/svg",viewBox:"0 0 24 24",children:e("g",{"data-name":"Layer 2",children:s("g",{"data-name":"edit-2",children:[e("rect",{width:"24",height:"24",opacity:"0"}),e("path",{d:"M19 20H5a1 1 0 0 0 0 2h14a1 1 0 0 0 0-2z"}),e("path",{d:"M5 18h.09l4.17-.38a2 2 0 0 0 1.21-.57l9-9a1.92 1.92 0 0 0-.07-2.71L16.66 2.6A2 2 0 0 0 14 2.53l-9 9a2 2 0 0 0-.57 1.21L4 16.91a1 1 0 0 0 .29.8A1 1 0 0 0 5 18zM15.27 4L18 6.73l-2 1.95L13.32 6zm-8.9 8.91L12 7.32l2.7 2.7-5.6 5.6-3 .28z"})]})})}),Ec=()=>e("svg",{xmlns:"http://www.w3.org/2000/svg",viewBox:"0 0 24 24",children:e("g",{"data-name":"Layer 2",children:s("g",{"data-name":"external-link",children:[e("rect",{width:"24",height:"24",opacity:"0"}),e("path",{d:"M20 11a1 1 0 0 0-1 1v6a1 1 0 0 1-1 1H6a1 1 0 0 1-1-1V6a1 1 0 0 1 1-1h6a1 1 0 0 0 0-2H6a3 3 0 0 0-3 3v12a3 3 0 0 0 3 3h12a3 3 0 0 0 3-3v-6a1 1 0 0 0-1-1z"}),e("path",{d:"M16 5h1.58l-6.29 6.28a1 1 0 0 0 0 1.42 1 1 0 0 0 1.42 0L19 6.42V8a1 1 0 0 0 1 1 1 1 0 0 0 1-1V4a1 1 0 0 0-1-1h-4a1 1 0 0 0 0 2z"})]})})}),a8=()=>e("svg",{xmlns:"http://www.w3.org/2000/svg",viewBox:"0 0 24 24",children:e("g",{"data-name":"Layer 2",children:s("g",{"data-name":"expand",children:[e("rect",{width:"24",height:"24",transform:"rotate(180 12 12)",opacity:"0"}),e("path",{d:"M20 5a1 1 0 0 0-1-1h-5a1 1 0 0 0 0 2h2.57l-3.28 3.29a1 1 0 0 0 0 1.42 1 1 0 0 0 1.42 0L18 7.42V10a1 1 0 0 0 1 1 1 1 0 0 0 1-1z"}),e("path",{d:"M10.71 13.29a1 1 0 0 0-1.42 0L6 16.57V14a1 1 0 0 0-1-1 1 1 0 0 0-1 1v5a1 1 0 0 0 1 1h5a1 1 0 0 0 0-2H7.42l3.29-3.29a1 1 0 0 0 0-1.42z"})]})})}),t8=()=>s("svg",{width:"20",height:"20",viewBox:"0 0 20 20",fill:"none",xmlns:"http://www.w3.org/2000/svg",children:[e("path",{d:"M11.7325 8.3969L12.9778 9.61741L5.58892 16.9977C4.90368 17.6822 3.79253 17.6823 3.10751 16.9981C2.42238 16.3137 2.42238 15.2042 3.10751 14.5198L10.4967 7.13917L11.7245 8.38888L11.7244 8.38895L11.7325 8.3969Z",stroke:"currentColor",strokeWidth:"1.2",fill:"none"}),e("circle",{cx:"12",cy:"5",r:"0.75",stroke:"currentColor",strokeWidth:"0.5",fill:"none"}),e("circle",{cx:"15",cy:"4",r:"0.75",stroke:"currentColor",strokeWidth:"0.5",fill:"none"}),e("circle",{cx:"14.5",cy:"7.5",r:"1.2",stroke:"currentColor",strokeWidth:"0.6",fill:"none"})]}),Dc=()=>s("svg",{xmlns:"http://www.w3.org/2000/svg",width:"20",height:"20",viewBox:"0 0 20 20",fill:"none",children:[e("path",{fillRule:"evenodd",clipRule:"evenodd",d:"M9.77475 4.16985C14.7548 4.01401 17.6914 8.65901 18.2231 9.58568C18.3698 9.84235 18.3698 10.1582 18.2231 10.4148C17.5114 11.6557 14.8314 15.7132 10.2256 15.8307C10.1573 15.8323 10.0889 15.8332 10.0206 15.8332C5.13475 15.8332 2.30142 11.329 1.77725 10.4148C1.62975 10.1582 1.62975 9.84235 1.77725 9.58568C2.48892 8.34485 5.16808 4.28651 9.77475 4.16985ZM10.1831 14.1648C6.59475 14.2482 4.25392 11.179 3.47725 9.99651C4.33225 8.65901 6.48558 5.92068 9.81725 5.83568C13.3914 5.74485 15.7456 8.82151 16.5223 10.004C15.6681 11.3415 13.5139 14.0798 10.1831 14.1648ZM7.08333 10.0002C7.08333 8.39185 8.39167 7.08351 10 7.08351C11.6083 7.08351 12.9167 8.39185 12.9167 10.0002C12.9167 11.6085 11.6083 12.9168 10 12.9168C8.39167 12.9168 7.08333 11.6085 7.08333 10.0002ZM8.75 10.0002C8.75 10.6893 9.31083 11.2502 10 11.2502C10.6892 11.2502 11.25 10.6893 11.25 10.0002C11.25 9.31101 10.6892 8.75018 10 8.75018C9.31083 8.75018 8.75 9.31101 8.75 10.0002Z"}),e("mask",{id:"mask0_935_15127",style:{maskType:"alpha"},maskUnits:"userSpaceOnUse",x:"1",y:"4",width:"18",height:"12",children:e("path",{fillRule:"evenodd",clipRule:"evenodd",d:"M9.77475 4.16985C14.7548 4.01401 17.6914 8.65901 18.2231 9.58568C18.3698 9.84235 18.3698 10.1582 18.2231 10.4148C17.5114 11.6557 14.8314 15.7132 10.2256 15.8307C10.1573 15.8323 10.0889 15.8332 10.0206 15.8332C5.13475 15.8332 2.30142 11.329 1.77725 10.4148C1.62975 10.1582 1.62975 9.84235 1.77725 9.58568C2.48892 8.34485 5.16808 4.28651 9.77475 4.16985ZM10.1831 14.1648C6.59475 14.2482 4.25392 11.179 3.47725 9.99651C4.33225 8.65901 6.48558 5.92068 9.81725 5.83568C13.3914 5.74485 15.7456 8.82151 16.5223 10.004C15.6681 11.3415 13.5139 14.0798 10.1831 14.1648ZM7.08333 10.0002C7.08333 8.39185 8.39167 7.08351 10 7.08351C11.6083 7.08351 12.9167 8.39185 12.9167 10.0002C12.9167 11.6085 11.6083 12.9168 10 12.9168C8.39167 12.9168 7.08333 11.6085 7.08333 10.0002ZM8.75 10.0002C8.75 10.6893 9.31083 11.2502 10 11.2502C10.6892 11.2502 11.25 10.6893 11.25 10.0002C11.25 9.31101 10.6892 8.75018 10 8.75018C9.31083 8.75018 8.75 9.31101 8.75 10.0002Z"})}),e("g",{mask:"url(#mask0_935_15127)"})]}),_c=()=>e("svg",{xmlns:"http://www.w3.org/2000/svg",viewBox:"0 0 24 24",children:e("g",{"data-name":"Layer 2",children:s("g",{"data-name":"eye-off",children:[e("rect",{width:"24",height:"24",opacity:"0"}),e("path",{d:"M4.71 3.29a1 1 0 0 0-1.42 1.42l5.63 5.63a3.5 3.5 0 0 0 4.74 4.74l5.63 5.63a1 1 0 0 0 1.42 0 1 1 0 0 0 0-1.42zM12 13.5a1.5 1.5 0 0 1-1.5-1.5v-.07l1.56 1.56z"}),e("path",{d:"M12.22 17c-4.3.1-7.12-3.59-8-5a13.7 13.7 0 0 1 2.24-2.72L5 7.87a15.89 15.89 0 0 0-2.87 3.63 1 1 0 0 0 0 1c.63 1.09 4 6.5 9.89 6.5h.25a9.48 9.48 0 0 0 3.23-.67l-1.58-1.58a7.74 7.74 0 0 1-1.7.25z"}),e("path",{d:"M21.87 11.5c-.64-1.11-4.17-6.68-10.14-6.5a9.48 9.48 0 0 0-3.23.67l1.58 1.58a7.74 7.74 0 0 1 1.7-.25c4.29-.11 7.11 3.59 8 5a13.7 13.7 0 0 1-2.29 2.72L19 16.13a15.89 15.89 0 0 0 2.91-3.63 1 1 0 0 0-.04-1z"})]})})}),l8=()=>e("svg",{xmlns:"http://www.w3.org/2000/svg",viewBox:"0 0 24 24",children:e("g",{"data-name":"Layer 2",children:s("g",{"data-name":"file",children:[e("rect",{width:"24",height:"24",opacity:"0"}),e("path",{d:"M19.74 8.33l-5.44-6a1 1 0 0 0-.74-.33h-7A2.53 2.53 0 0 0 4 4.5v15A2.53 2.53 0 0 0 6.56 22h10.88A2.53 2.53 0 0 0 20 19.5V9a1 1 0 0 0-.26-.67zM17.65 9h-3.94a.79.79 0 0 1-.71-.85V4h.11zm-.21 11H6.56a.53.53 0 0 1-.56-.5v-15a.53.53 0 0 1 .56-.5H11v4.15A2.79 2.79 0 0 0 13.71 11H18v8.5a.53.53 0 0 1-.56.5z"})]})})}),Kc=()=>e("svg",{xmlns:"http://www.w3.org/2000/svg",width:"20",height:"20",viewBox:"0 0 24 24",children:s("g",{"data-name":"Layer 2",children:[e("rect",{width:"24",height:"24",transform:"rotate(180 12 12)",opacity:"0"}),e("path",{d:"M12 1A10.89 10.89 0 0 0 1 11.77 10.79 10.79 0 0 0 8.52 22c.55.1.75-.23.75-.52v-1.83c-3.06.65-3.71-1.44-3.71-1.44a2.86 2.86 0 0 0-1.22-1.58c-1-.66.08-.65.08-.65a2.31 2.31 0 0 1 1.68 1.11 2.37 2.37 0 0 0 3.2.89 2.33 2.33 0 0 1 .7-1.44c-2.44-.27-5-1.19-5-5.32a4.15 4.15 0 0 1 1.11-2.91 3.78 3.78 0 0 1 .11-2.84s.93-.29 3 1.1a10.68 10.68 0 0 1 5.5 0c2.1-1.39 3-1.1 3-1.1a3.78 3.78 0 0 1 .11 2.84A4.15 4.15 0 0 1 19 11.2c0 4.14-2.58 5.05-5 5.32a2.5 2.5 0 0 1 .75 2v2.95c0 .35.2.63.75.52A10.8 10.8 0 0 0 23 11.77 10.89 10.89 0 0 0 12 1"})]})}),xi=()=>e("svg",{xmlns:"http://www.w3.org/2000/svg",viewBox:"0 0 24 24",children:e("g",{"data-name":"Layer 2",children:s("g",{"data-name":"grid",children:[e("rect",{width:"24",height:"24",opacity:"0"}),e("path",{d:"M9 3H5a2 2 0 0 0-2 2v4a2 2 0 0 0 2 2h4a2 2 0 0 0 2-2V5a2 2 0 0 0-2-2z"}),e("path",{d:"M19 3h-4a2 2 0 0 0-2 2v4a2 2 0 0 0 2 2h4a2 2 0 0 0 2-2V5a2 2 0 0 0-2-2z"}),e("path",{d:"M9 13H5a2 2 0 0 0-2 2v4a2 2 0 0 0 2 2h4a2 2 0 0 0 2-2v-4a2 2 0 0 0-2-2z"}),e("path",{d:"M19 13h-4a2 2 0 0 0-2 2v4a2 2 0 0 0 2 2h4a2 2 0 0 0 2-2v-4a2 2 0 0 0-2-2z"})]})})}),i8=()=>e("svg",{xmlns:"http://www.w3.org/2000/svg",viewBox:"0 0 24 24",children:e("g",{"data-name":"Layer 2",children:s("g",{"data-name":"grid",children:[e("rect",{width:"24",height:"24",opacity:"0"}),e("path",{d:"M9 3H5a2 2 0 0 0-2 2v4a2 2 0 0 0 2 2h4a2 2 0 0 0 2-2V5a2 2 0 0 0-2-2zM5 9V5h4v4z"}),e("path",{d:"M19 3h-4a2 2 0 0 0-2 2v4a2 2 0 0 0 2 2h4a2 2 0 0 0 2-2V5a2 2 0 0 0-2-2zm-4 6V5h4v4z"}),e("path",{d:"M9 13H5a2 2 0 0 0-2 2v4a2 2 0 0 0 2 2h4a2 2 0 0 0 2-2v-4a2 2 0 0 0-2-2zm-4 6v-4h4v4z"}),e("path",{d:"M19 13h-4a2 2 0 0 0-2 2v4a2 2 0 0 0 2 2h4a2 2 0 0 0 2-2v-4a2 2 0 0 0-2-2zm-4 6v-4h4v4z"})]})})}),Pc=()=>e("svg",{xmlns:"http://www.w3.org/2000/svg",viewBox:"0 0 24 24",children:e("g",{"data-name":"Layer 2",children:s("g",{"data-name":"info",children:[e("rect",{width:"24",height:"24",transform:"rotate(180 12 12)",opacity:"0"}),e("path",{d:"M12 2a10 10 0 1 0 10 10A10 10 0 0 0 12 2zm1 14a1 1 0 0 1-2 0v-5a1 1 0 0 1 2 0zm-1-7a1 1 0 1 1 1-1 1 1 0 0 1-1 1z"})]})})}),St=()=>e("svg",{xmlns:"http://www.w3.org/2000/svg",viewBox:"0 0 24 24",children:e("g",{"data-name":"Layer 2",children:s("g",{"data-name":"info",children:[e("rect",{width:"24",height:"24",transform:"rotate(180 12 12)",opacity:"0"}),e("path",{d:"M12 2a10 10 0 1 0 10 10A10 10 0 0 0 12 2zm0 18a8 8 0 1 1 8-8 8 8 0 0 1-8 8z"}),e("circle",{cx:"12",cy:"8",r:"1"}),e("path",{d:"M12 10a1 1 0 0 0-1 1v5a1 1 0 0 0 2 0v-5a1 1 0 0 0-1-1z"})]})})}),Vc=()=>e("svg",{width:"20",height:"20",viewBox:"0 0 20 20",xmlns:"http://www.w3.org/2000/svg",children:e("path",{fillRule:"evenodd",clipRule:"evenodd",d:"M12.2257 11.8L11.7393 8.41153C11.7109 8.22144 11.7902 8.03189 11.9431 7.9217C12.0956 7.81142 12.2951 7.79984 12.4586 7.89091L16.2173 9.99324C17.4623 8.99204 18.1154 7.77352 18.1154 6.53971C18.1154 5.16011 17.2989 3.79965 15.7513 2.74073C14.2085 1.6851 12.0218 1 9.55769 1C7.09362 1 4.90688 1.6851 3.36408 2.74073C1.81649 3.79965 1 5.16011 1 6.53971C1 7.9193 1.81649 9.27976 3.36408 10.3387C3.42007 10.377 3.4769 10.4148 3.53457 10.4521C3.57721 10.4488 3.6203 10.447 3.66378 10.447C4.25644 10.447 4.7771 10.7654 5.0742 11.2456C6.36894 11.7696 7.9006 12.0794 9.55769 12.0794C10.4938 12.0794 11.3898 11.9805 12.2257 11.8ZM12.3681 12.7921C11.4796 12.9789 10.5358 13.0794 9.55769 13.0794C8.03657 13.0794 6.59844 12.8363 5.32179 12.4037C5.2538 12.9334 4.95341 13.3874 4.5299 13.6526C4.61517 13.7612 4.70537 13.8853 4.79522 14.0242C5.16436 14.5947 5.54041 15.4345 5.51764 16.4699C5.49439 17.5267 5.00709 18.3616 4.55343 18.915C4.32482 19.1938 4.0981 19.4095 3.92766 19.5564C3.84217 19.63 3.77007 19.687 3.71793 19.7265C3.69184 19.7463 3.67068 19.7618 3.65525 19.7728L3.6365 19.7861L3.63052 19.7902L3.62841 19.7917L3.62759 19.7922L3.62723 19.7925C3.62707 19.7926 3.62691 19.7927 3.34519 19.379L3.62691 19.7927C3.39879 19.9479 3.08774 19.8884 2.93215 19.66C2.7767 19.4317 2.83526 19.1211 3.06288 18.9658L3.06295 18.9658L3.06304 18.9657L3.06326 18.9655L3.07183 18.9595C3.08034 18.9534 3.0943 18.9432 3.11293 18.9291C3.15023 18.9008 3.20601 18.8569 3.27421 18.7981C3.41116 18.6801 3.59512 18.5051 3.77969 18.28C4.15237 17.8254 4.50136 17.1997 4.51794 16.4459C4.53499 15.6707 4.25394 15.0268 3.95603 14.5663C3.80773 14.3371 3.65843 14.1585 3.54764 14.0386C3.49243 13.9788 3.44732 13.9342 3.41742 13.9058C3.40487 13.8938 3.39504 13.8848 3.38831 13.8787C2.59563 13.743 1.99119 13.0317 1.99119 12.1745C1.99119 11.6923 2.18248 11.2563 2.49096 10.9429C0.943505 9.78084 0 8.23567 0 6.53971C0 2.92793 4.27912 0 9.55769 0C14.8363 0 19.1154 2.92793 19.1154 6.53971C19.1154 8.03471 18.3822 9.41255 17.1485 10.5141L19.7425 11.965C19.9297 12.0691 20.029 12.285 19.9925 12.4988C19.9907 12.5093 19.9885 12.5192 19.9863 12.5291C19.9347 12.7525 19.7439 12.912 19.5215 12.9178L15.7303 13.0197C15.5329 13.0249 15.3583 13.1512 15.286 13.341L13.8962 16.9857C13.8153 17.1997 13.6049 17.3304 13.384 17.304C13.1626 17.2776 12.9862 17.1018 12.9542 16.8745L12.3681 12.7921ZM3.36757 11.5227C3.15331 11.6367 2.99119 11.872 2.99119 12.1745C2.99119 12.607 3.3225 12.902 3.66378 12.902C4.00506 12.902 4.33638 12.607 4.33638 12.1745C4.33638 12.1174 4.3306 12.0627 4.31979 12.0108C3.98738 11.8615 3.66939 11.6984 3.36757 11.5227Z"})}),r8=()=>s("svg",{xmlns:"http://www.w3.org/2000/svg",width:"24",height:"24",viewBox:"0 0 24 24",stroke:"currentColor",strokeWidth:"2",strokeLinecap:"round",strokeLinejoin:"round",children:[e("circle",{cx:"12",cy:"12",r:"10",fill:"none"}),e("circle",{cx:"12",cy:"12",r:"4",fill:"none"}),e("line",{x1:"4.93",y1:"4.93",x2:"9.17",y2:"9.17"}),e("line",{x1:"14.83",y1:"14.83",x2:"19.07",y2:"19.07"}),e("line",{x1:"14.83",y1:"9.17",x2:"19.07",y2:"4.93"}),e("line",{x1:"14.83",y1:"9.17",x2:"18.36",y2:"5.64"}),e("line",{x1:"4.93",y1:"19.07",x2:"9.17",y2:"14.83"})]}),Ti=()=>e("svg",{xmlns:"http://www.w3.org/2000/svg",viewBox:"0 0 24 24",children:e("g",{"data-name":"Layer 2",children:s("g",{"data-name":"list",children:[e("rect",{width:"24",height:"24",transform:"rotate(180 12 12)",opacity:"0"}),e("circle",{cx:"4",cy:"7",r:"1"}),e("circle",{cx:"4",cy:"12",r:"1"}),e("circle",{cx:"4",cy:"17",r:"1"}),e("rect",{x:"7",y:"11",width:"14",height:"2",rx:".94",ry:".94"}),e("rect",{x:"7",y:"16",width:"14",height:"2",rx:".94",ry:".94"}),e("rect",{x:"7",y:"6",width:"14",height:"2",rx:".94",ry:".94"})]})})}),Ai=()=>e("svg",{width:"24",height:"24",viewBox:"0 0 24 24",fill:"none",xmlns:"http://www.w3.org/2000/svg",css:m`
      animation: ${bc} 1s infinite linear;
    `,children:s("g",{id:"loading",children:[e("mask",{id:"mask0_804_24",style:{maskType:"alpha"},maskUnits:"userSpaceOnUse",x:"2",y:"2",width:"20",height:"20",children:e("path",{fillRule:"evenodd",clipRule:"evenodd",d:"M2 12C2 6.486 6.486 2 12 2C17.514 2 22 6.486 22 12C22 17.514 17.514 22 12 22C6.486 22 2 17.514 2 12ZM4 12C4 16.411 7.589 20 12 20C16.411 20 20 16.411 20 12C20 7.589 16.411 4 12 4C7.589 4 4 7.589 4 12Z",fill:"inherit"})}),e("g",{mask:"url(#mask0_804_24)",children:e("path",{id:"Union",fillRule:"evenodd",clipRule:"evenodd",d:"M15.8268 2.7612C14.6136 2.25866 13.3132 2 12 2C11.4477 2 11 2.44772 11 3C11 3.55228 11.4477 4 12 4V12H20C20 12.5523 20.4477 13 21 13C21.5523 13 22 12.5523 22 12C22 10.6868 21.7413 9.38642 21.2388 8.17317C20.7362 6.95991 19.9997 5.85752 19.0711 4.92893C18.1425 4.00035 17.0401 3.26375 15.8268 2.7612Z",fill:"inherit"})})]})}),o8=()=>e("svg",{xmlns:"http://www.w3.org/2000/svg",viewBox:"0 0 24 24",children:e("g",{"data-name":"Layer 2",children:s("g",{"data-name":"log-out",children:[e("rect",{width:"24",height:"24",transform:"rotate(90 12 12)",opacity:"0"}),e("path",{d:"M7 6a1 1 0 0 0 0-2H5a1 1 0 0 0-1 1v14a1 1 0 0 0 1 1h2a1 1 0 0 0 0-2H6V6z"}),e("path",{d:"M20.82 11.42l-2.82-4a1 1 0 0 0-1.39-.24 1 1 0 0 0-.24 1.4L18.09 11H10a1 1 0 0 0 0 2h8l-1.8 2.4a1 1 0 0 0 .2 1.4 1 1 0 0 0 .6.2 1 1 0 0 0 .8-.4l3-4a1 1 0 0 0 .02-1.18z"})]})})}),s8=()=>e("svg",{xmlns:"http://www.w3.org/2000/svg",viewBox:"0 0 24 24",children:e("g",{"data-name":"Layer 2",children:s("g",{"data-name":"message-square",children:[e("rect",{width:"24",height:"24",opacity:"0"}),e("circle",{cx:"12",cy:"11",r:"1"}),e("circle",{cx:"16",cy:"11",r:"1"}),e("circle",{cx:"8",cy:"11",r:"1"}),e("path",{d:"M19 3H5a3 3 0 0 0-3 3v15a1 1 0 0 0 .51.87A1 1 0 0 0 3 22a1 1 0 0 0 .51-.14L8 19.14a1 1 0 0 1 .55-.14H19a3 3 0 0 0 3-3V6a3 3 0 0 0-3-3zm1 13a1 1 0 0 1-1 1H8.55a3 3 0 0 0-1.55.43l-3 1.8V6a1 1 0 0 1 1-1h14a1 1 0 0 1 1 1z"})]})})}),ll=()=>e("svg",{xmlns:"http://www.w3.org/2000/svg",viewBox:"0 0 24 24",children:e("g",{"data-name":"Layer 2",children:s("g",{"data-name":"minus-circle",children:[e("rect",{width:"24",height:"24",opacity:"0"}),e("path",{d:"M12 2a10 10 0 1 0 10 10A10 10 0 0 0 12 2zm0 18a8 8 0 1 1 8-8 8 8 0 0 1-8 8z"}),e("path",{d:"M15 11H9a1 1 0 0 0 0 2h6a1 1 0 0 0 0-2z"})]})})}),Rc=()=>e("svg",{xmlns:"http://www.w3.org/2000/svg",viewBox:"0 0 24 24",children:e("g",{"data-name":"Layer 2",children:s("g",{"data-name":"moon",children:[e("rect",{width:"24",height:"24",opacity:"0"}),e("path",{d:"M12.3 22h-.1a10.31 10.31 0 0 1-7.34-3.15 10.46 10.46 0 0 1-.26-14 10.13 10.13 0 0 1 4-2.74 1 1 0 0 1 1.06.22 1 1 0 0 1 .24 1 8.4 8.4 0 0 0 1.94 8.81 8.47 8.47 0 0 0 8.83 1.94 1 1 0 0 1 1.27 1.29A10.16 10.16 0 0 1 19.6 19a10.28 10.28 0 0 1-7.3 3zM7.46 4.92a7.93 7.93 0 0 0-1.37 1.22 8.44 8.44 0 0 0 .2 11.32A8.29 8.29 0 0 0 12.22 20h.08a8.34 8.34 0 0 0 6.78-3.49A10.37 10.37 0 0 1 7.46 4.92z"})]})})}),Oc=()=>e("svg",{xmlns:"http://www.w3.org/2000/svg",viewBox:"0 0 24 24",children:e("g",{"data-name":"Layer 2",children:s("g",{"data-name":"more-horizotnal",children:[e("rect",{width:"24",height:"24",opacity:"0"}),e("circle",{cx:"12",cy:"12",r:"2"}),e("circle",{cx:"19",cy:"12",r:"2"}),e("circle",{cx:"5",cy:"12",r:"2"})]})})}),Nc=()=>e("svg",{xmlns:"http://www.w3.org/2000/svg",viewBox:"0 0 24 24",children:e("g",{"data-name":"Layer 2",children:s("g",{"data-name":"move",children:[e("rect",{width:"24",height:"24",transform:"rotate(180 12 12)",opacity:"0"}),e("path",{d:"M21.71 11.31l-3-3a1 1 0 0 0-1.42 1.42L18.58 11H13V5.41l1.29 1.3A1 1 0 0 0 15 7a1 1 0 0 0 .71-.29 1 1 0 0 0 0-1.42l-3-3A1 1 0 0 0 12 2a1 1 0 0 0-.7.29l-3 3a1 1 0 0 0 1.41 1.42L11 5.42V11H5.41l1.3-1.29a1 1 0 0 0-1.42-1.42l-3 3A1 1 0 0 0 2 12a1 1 0 0 0 .29.71l3 3A1 1 0 0 0 6 16a1 1 0 0 0 .71-.29 1 1 0 0 0 0-1.42L5.42 13H11v5.59l-1.29-1.3a1 1 0 0 0-1.42 1.42l3 3A1 1 0 0 0 12 22a1 1 0 0 0 .7-.29l3-3a1 1 0 0 0-1.42-1.42L13 18.58V13h5.59l-1.3 1.29a1 1 0 0 0 0 1.42A1 1 0 0 0 18 16a1 1 0 0 0 .71-.29l3-3A1 1 0 0 0 22 12a1 1 0 0 0-.29-.69z"})]})})}),c8=()=>e("svg",{xmlns:"http://www.w3.org/2000/svg",viewBox:"0 0 24 24",children:e("g",{"data-name":"Layer 2",children:s("g",{"data-name":"options",children:[e("rect",{width:"24",height:"24",opacity:"0"}),e("path",{d:"M7 14.18V3a1 1 0 0 0-2 0v11.18a3 3 0 0 0 0 5.64V21a1 1 0 0 0 2 0v-1.18a3 3 0 0 0 0-5.64zM6 18a1 1 0 1 1 1-1 1 1 0 0 1-1 1z"}),e("path",{d:"M21 13a3 3 0 0 0-2-2.82V3a1 1 0 0 0-2 0v7.18a3 3 0 0 0 0 5.64V21a1 1 0 0 0 2 0v-5.18A3 3 0 0 0 21 13zm-3 1a1 1 0 1 1 1-1 1 1 0 0 1-1 1z"}),e("path",{d:"M15 5a3 3 0 1 0-4 2.82V21a1 1 0 0 0 2 0V7.82A3 3 0 0 0 15 5zm-3 1a1 1 0 1 1 1-1 1 1 0 0 1-1 1z"})]})})}),$c=()=>e("svg",{xmlns:"http://www.w3.org/2000/svg",viewBox:"0 0 24 24",children:e("g",{"data-name":"Layer 2",children:s("g",{"data-name":"paper-plane",children:[e("rect",{width:"24",height:"24",opacity:"0"}),e("path",{d:"M21 4a1.31 1.31 0 0 0-.06-.27v-.09a1 1 0 0 0-.2-.3 1 1 0 0 0-.29-.19h-.09a.86.86 0 0 0-.31-.15H20a1 1 0 0 0-.3 0l-18 6a1 1 0 0 0 0 1.9l8.53 2.84 2.84 8.53a1 1 0 0 0 1.9 0l6-18A1 1 0 0 0 21 4zm-4.7 2.29l-5.57 5.57L5.16 10zM14 18.84l-1.86-5.57 5.57-5.57z"})]})})}),d8=()=>e("svg",{xmlns:"http://www.w3.org/2000/svg",viewBox:"0 0 24 24",children:e("g",{"data-name":"Layer 2",children:s("g",{"data-name":"person",children:[e("rect",{width:"24",height:"24",opacity:"0"}),e("path",{d:"M12 11a4 4 0 1 0-4-4 4 4 0 0 0 4 4zm0-6a2 2 0 1 1-2 2 2 2 0 0 1 2-2z"}),e("path",{d:"M12 13a7 7 0 0 0-7 7 1 1 0 0 0 2 0 5 5 0 0 1 10 0 1 1 0 0 0 2 0 7 7 0 0 0-7-7z"})]})})}),u8=()=>e("svg",{xmlns:"http://www.w3.org/2000/svg",viewBox:"0 0 24 24",children:e("g",{"data-name":"Layer 2",children:s("g",{"data-name":"play-circle",children:[e("rect",{width:"24",height:"24",opacity:"0"}),e("path",{d:"M12 2a10 10 0 1 0 10 10A10 10 0 0 0 12 2zm0 18a8 8 0 1 1 8-8 8 8 0 0 1-8 8z"}),e("path",{d:"M12.34 7.45a1.7 1.7 0 0 0-1.85-.3 1.6 1.6 0 0 0-1 1.48v6.74a1.6 1.6 0 0 0 1 1.48 1.68 1.68 0 0 0 .69.15 1.74 1.74 0 0 0 1.16-.45L16 13.18a1.6 1.6 0 0 0 0-2.36zm-.84 7.15V9.4l2.81 2.6z"})]})})}),Bc=()=>e("svg",{xmlns:"http://www.w3.org/2000/svg",viewBox:"0 0 24 24",children:e("g",{"data-name":"Layer 2",children:s("g",{"data-name":"plus",children:[e("rect",{width:"24",height:"24",transform:"rotate(180 12 12)",opacity:"0"}),e("path",{d:"M19 11h-6V5a1 1 0 0 0-2 0v6H5a1 1 0 0 0 0 2h6v6a1 1 0 0 0 2 0v-6h6a1 1 0 0 0 0-2z"})]})})}),xt=()=>e("svg",{xmlns:"http://www.w3.org/2000/svg",viewBox:"0 0 24 24",children:e("g",{"data-name":"Layer 2",children:s("g",{"data-name":"plus-circle",children:[e("rect",{width:"24",height:"24",opacity:"0"}),e("path",{d:"M12 2a10 10 0 1 0 10 10A10 10 0 0 0 12 2zm0 18a8 8 0 1 1 8-8 8 8 0 0 1-8 8z"}),e("path",{d:"M15 11h-2V9a1 1 0 0 0-2 0v2H9a1 1 0 0 0 0 2h2v2a1 1 0 0 0 2 0v-2h2a1 1 0 0 0 0-2z"})]})})}),Hc=()=>e("svg",{xmlns:"http://www.w3.org/2000/svg",viewBox:"0 0 24 24",children:e("g",{"data-name":"Layer 2",children:s("g",{"data-name":"pricetags",children:[e("rect",{width:"24",height:"24",opacity:"0"}),e("path",{d:"M12.87 22a1.84 1.84 0 0 1-1.29-.53l-6.41-6.42a1 1 0 0 1-.29-.61L4 5.09a1 1 0 0 1 .29-.8 1 1 0 0 1 .8-.29l9.35.88a1 1 0 0 1 .61.29l6.42 6.41a1.82 1.82 0 0 1 0 2.57l-7.32 7.32a1.82 1.82 0 0 1-1.28.53zm-6-8.11l6 6 7.05-7.05-6-6-7.81-.73z"}),e("circle",{cx:"10.5",cy:"10.5",r:"1.5"})]})})}),il=()=>e("svg",{xmlns:"http://www.w3.org/2000/svg",viewBox:"0 0 24 24",children:e("g",{"data-name":"Layer 2",children:s("g",{"data-name":"refresh",children:[e("rect",{width:"24",height:"24",opacity:"0"}),e("path",{d:"M20.3 13.43a1 1 0 0 0-1.25.65A7.14 7.14 0 0 1 12.18 19 7.1 7.1 0 0 1 5 12a7.1 7.1 0 0 1 7.18-7 7.26 7.26 0 0 1 4.65 1.67l-2.17-.36a1 1 0 0 0-1.15.83 1 1 0 0 0 .83 1.15l4.24.7h.17a1 1 0 0 0 .34-.06.33.33 0 0 0 .1-.06.78.78 0 0 0 .2-.11l.09-.11c0-.05.09-.09.13-.15s0-.1.05-.14a1.34 1.34 0 0 0 .07-.18l.75-4a1 1 0 0 0-2-.38l-.27 1.45A9.21 9.21 0 0 0 12.18 3 9.1 9.1 0 0 0 3 12a9.1 9.1 0 0 0 9.18 9A9.12 9.12 0 0 0 21 14.68a1 1 0 0 0-.7-1.25z"})]})})}),g8=()=>e("svg",{xmlns:"http://www.w3.org/2000/svg",viewBox:"0 0 24 24",children:e("g",{"data-name":"Layer 2",children:s("g",{"data-name":"repeat",children:[e("rect",{width:"24",height:"24",opacity:"0"}),e("path",{d:"M17.91 5h-12l1.3-1.29a1 1 0 0 0-1.42-1.42l-3 3a1 1 0 0 0 0 1.42l3 3a1 1 0 0 0 1.42 0 1 1 0 0 0 0-1.42L5.91 7h12a1.56 1.56 0 0 1 1.59 1.53V11a1 1 0 0 0 2 0V8.53A3.56 3.56 0 0 0 17.91 5z"}),e("path",{d:"M18.21 14.29a1 1 0 0 0-1.42 1.42l1.3 1.29h-12a1.56 1.56 0 0 1-1.59-1.53V13a1 1 0 0 0-2 0v2.47A3.56 3.56 0 0 0 6.09 19h12l-1.3 1.29a1 1 0 0 0 0 1.42 1 1 0 0 0 1.42 0l3-3a1 1 0 0 0 0-1.42z"})]})})}),m8=()=>s("svg",{xmlns:"http://www.w3.org/2000/svg",width:"24",height:"24",viewBox:"0 0 24 24",fill:"none",stroke:"currentColor",strokeWidth:"2",strokeLinecap:"round",strokeLinejoin:"round",children:[e("path",{d:"M4.5 16.5c-1.5 1.26-2 5-2 5s3.74-.5 5-2c.71-.84.7-2.13-.09-2.91a2.18 2.18 0 0 0-2.91-.09z",fill:"none"}),e("path",{d:"m12 15-3-3a22 22 0 0 1 2-3.95A12.88 12.88 0 0 1 22 2c0 2.72-.78 7.5-6 11a22.35 22.35 0 0 1-4 2z",fill:"none"}),e("path",{d:"M9 12H4s.55-3.03 2-4c1.62-1.08 5 0 5 0",fill:"none"}),e("path",{d:"M12 15v5s3.03-.55 4-2c1.08-1.62 0-5 0-5",fill:"none"})]}),jc=()=>e("svg",{width:"24",height:"24",viewBox:"0 0 24 24",fill:"none",xmlns:"http://www.w3.org/2000/svg",children:e("path",{fillRule:"evenodd",clipRule:"evenodd",d:"M3 11.25C2.58579 11.25 2.25 11.5858 2.25 12C2.25 12.4142 2.58579 12.75 3 12.75H3.9C4.31421 12.75 4.65 12.4142 4.65 12C4.65 11.5858 4.31421 11.25 3.9 11.25H3ZM5.7 11.25C5.28579 11.25 4.95 11.5858 4.95 12C4.95 12.4142 5.28579 12.75 5.7 12.75H7.5C7.91421 12.75 8.25 12.4142 8.25 12C8.25 11.5858 7.91421 11.25 7.5 11.25H5.7ZM9.3 11.25C8.88579 11.25 8.55 11.5858 8.55 12C8.55 12.4142 8.88579 12.75 9.3 12.75H11.1C11.5142 12.75 11.85 12.4142 11.85 12C11.85 11.5858 11.5142 11.25 11.1 11.25H9.3ZM12.9 11.25C12.4858 11.25 12.15 11.5858 12.15 12C12.15 12.4142 12.4858 12.75 12.9 12.75H14.7C15.1142 12.75 15.45 12.4142 15.45 12C15.45 11.5858 15.1142 11.25 14.7 11.25H12.9ZM16.5 11.25C16.0858 11.25 15.75 11.5858 15.75 12C15.75 12.4142 16.0858 12.75 16.5 12.75L18.3 12.75C18.7142 12.75 19.05 12.4142 19.05 12C19.05 11.5858 18.7142 11.25 18.3 11.25L16.5 11.25ZM20.1 11.25C19.6858 11.25 19.35 11.5858 19.35 12C19.35 12.4142 19.6858 12.75 20.1 12.75H21C21.4142 12.75 21.75 12.4142 21.75 12C21.75 11.5858 21.4142 11.25 21 11.25H20.1ZM12.5746 15.1596L15.5744 16.7468C16.0263 17.025 16.1363 17.571 15.8174 17.9656C15.4994 18.3611 14.8754 18.4564 14.4245 18.1782L12.9816 17.55C12.9829 17.5618 12.9867 17.5728 12.9904 17.5838C12.995 17.5974 12.9996 17.6108 12.9996 17.6252V21.1251C12.9996 21.608 12.5526 22 11.9997 22C11.4467 22 10.9998 21.608 10.9998 21.1251V17.6252V17.6243L9.59887 18.3252C9.15791 18.6148 8.53096 18.5369 8.19998 18.1502C8.06499 17.9927 8 17.8081 8 17.6261C8 17.3601 8.13799 17.0967 8.39997 16.9253L11.3997 15.1753C11.7457 14.9478 12.2207 14.9408 12.5746 15.1596ZM12.5746 8.84043L15.5744 7.25325C16.0263 6.97502 16.1363 6.42904 15.8174 6.03444C15.4994 5.63895 14.8754 5.54358 14.4245 5.82182L12.9816 6.45004C12.9829 6.43826 12.9867 6.42718 12.9904 6.41617C12.995 6.40266 12.9996 6.38926 12.9996 6.3748V2.87496C12.9996 2.39198 12.5526 2 11.9997 2C11.4467 2 10.9998 2.39198 10.9998 2.87496V6.3748V6.37567L9.59887 5.67483C9.15791 5.38522 8.53096 5.46309 8.19998 5.84982C8.06499 6.00731 8 6.19193 8 6.37392C8 6.63991 8.13799 6.90327 8.39997 7.07476L11.3997 8.82468C11.7457 9.05217 12.2207 9.05917 12.5746 8.84043Z",fill:"currentColor"})}),Zc=()=>e("svg",{width:"24",height:"24",viewBox:"0 0 24 24",fill:"none",xmlns:"http://www.w3.org/2000/svg",children:e("path",{fillRule:"evenodd",clipRule:"evenodd",d:"M3 11.25C2.58579 11.25 2.25 11.5858 2.25 12C2.25 12.4142 2.58579 12.75 3 12.75H3.9C4.31421 12.75 4.65 12.4142 4.65 12C4.65 11.5858 4.31421 11.25 3.9 11.25H3ZM5.7 11.25C5.28579 11.25 4.95 11.5858 4.95 12C4.95 12.4142 5.28579 12.75 5.7 12.75H7.5C7.91421 12.75 8.25 12.4142 8.25 12C8.25 11.5858 7.91421 11.25 7.5 11.25H5.7ZM9.3 11.25C8.88579 11.25 8.55 11.5858 8.55 12C8.55 12.4142 8.88579 12.75 9.3 12.75H11.1C11.5142 12.75 11.85 12.4142 11.85 12C11.85 11.5858 11.5142 11.25 11.1 11.25H9.3ZM12.9 11.25C12.4858 11.25 12.15 11.5858 12.15 12C12.15 12.4142 12.4858 12.75 12.9 12.75H14.7C15.1142 12.75 15.45 12.4142 15.45 12C15.45 11.5858 15.1142 11.25 14.7 11.25H12.9ZM16.5 11.25C16.0858 11.25 15.75 11.5858 15.75 12C15.75 12.4142 16.0858 12.75 16.5 12.75L18.3 12.75C18.7142 12.75 19.05 12.4142 19.05 12C19.05 11.5858 18.7142 11.25 18.3 11.25L16.5 11.25ZM20.1 11.25C19.6858 11.25 19.35 11.5858 19.35 12C19.35 12.4142 19.6858 12.75 20.1 12.75H21C21.4142 12.75 21.75 12.4142 21.75 12C21.75 11.5858 21.4142 11.25 21 11.25H20.1ZM11.4254 21.8405L8.42561 20.2533C7.97365 19.975 7.86366 19.4291 8.18263 19.0345C8.50061 18.639 9.12456 18.5436 9.57552 18.8219L11.0184 19.4501C11.0171 19.4383 11.0133 19.4272 11.0096 19.4162C11.005 19.4027 11.0004 19.3893 11.0004 19.3748V15.875C11.0004 15.392 11.4474 15 12.0003 15C12.5533 15 13.0002 15.392 13.0002 15.875V19.3748V19.3757L14.4011 18.6749C14.8421 18.3852 15.469 18.4631 15.8 18.8499C15.935 19.0073 16 19.192 16 19.374C16 19.6399 15.862 19.9033 15.6 20.0748L12.6003 21.8247C12.2543 22.0522 11.7793 22.0592 11.4254 21.8405ZM11.4254 2.1596L8.42561 3.74678C7.97365 4.02501 7.86366 4.57099 8.18263 4.96559C8.50061 5.36108 9.12456 5.45645 9.57552 5.17821L11.0184 4.54999C11.0171 4.56177 11.0133 4.57285 11.0096 4.58386C11.005 4.59737 11.0004 4.61077 11.0004 4.62523L11.0004 8.12507C11.0004 8.60805 11.4474 9.00003 12.0003 9.00003C12.5533 9.00003 13.0002 8.60805 13.0002 8.12507L13.0002 4.62523V4.62436L14.4011 5.3252C14.8421 5.61481 15.469 5.53694 15.8 5.15021C15.935 4.99272 16 4.8081 16 4.62611C16 4.36012 15.862 4.09676 15.6 3.92527L12.6003 2.17535C12.2543 1.94786 11.7793 1.94086 11.4254 2.1596Z",fill:"currentColor"})}),p8=()=>e("svg",{xmlns:"http://www.w3.org/2000/svg",viewBox:"0 0 24 24",children:e("g",{"data-name":"Layer 2",children:s("g",{"data-name":"save",children:[e("rect",{width:"24",height:"24",opacity:"0"}),e("path",{d:"M20.12 8.71l-4.83-4.83A3 3 0 0 0 13.17 3H6a3 3 0 0 0-3 3v12a3 3 0 0 0 3 3h12a3 3 0 0 0 3-3v-7.17a3 3 0 0 0-.88-2.12zM10 19v-2h4v2zm9-1a1 1 0 0 1-1 1h-2v-3a1 1 0 0 0-1-1H9a1 1 0 0 0-1 1v3H6a1 1 0 0 1-1-1V6a1 1 0 0 1 1-1h2v5a1 1 0 0 0 1 1h4a1 1 0 0 0 0-2h-3V5h3.17a1.05 1.05 0 0 1 .71.29l4.83 4.83a1 1 0 0 1 .29.71z"})]})})}),Uc=()=>e("svg",{xmlns:"http://www.w3.org/2000/svg",viewBox:"0 0 24 24",children:e("g",{"data-name":"Layer 2",children:s("g",{"data-name":"search",children:[e("rect",{width:"24",height:"24",opacity:"0"}),e("path",{d:"M20.71 19.29l-3.4-3.39A7.92 7.92 0 0 0 19 11a8 8 0 1 0-8 8 7.92 7.92 0 0 0 4.9-1.69l3.39 3.4a1 1 0 0 0 1.42 0 1 1 0 0 0 0-1.42zM5 11a6 6 0 1 1 6 6 6 6 0 0 1-6-6z"})]})})}),Gc=()=>s("svg",{xmlns:"http://www.w3.org/2000/svg",width:"24",height:"24",viewBox:"0 0 24 24",fill:"none",style:{fill:"none"},stroke:"currentColor",strokeWidth:"2",strokeLinecap:"round",strokeLinejoin:"round",children:[e("rect",{x:"2",y:"2",width:"20",height:"8",rx:"2",ry:"2"}),e("rect",{x:"2",y:"14",width:"20",height:"8",rx:"2",ry:"2"}),e("line",{x1:"6",y1:"6",x2:"6.01",y2:"6"}),e("line",{x1:"6",y1:"18",x2:"6.01",y2:"18"})]}),h8=()=>e("svg",{xmlns:"http://www.w3.org/2000/svg",viewBox:"0 0 24 24",children:e("g",{"data-name":"Layer 2",children:s("g",{"data-name":"settings",children:[e("rect",{width:"24",height:"24",opacity:"0"}),e("path",{d:"M8.61 22a2.25 2.25 0 0 1-1.35-.46L5.19 20a2.37 2.37 0 0 1-.49-3.22 2.06 2.06 0 0 0 .23-1.86l-.06-.16a1.83 1.83 0 0 0-1.12-1.22h-.16a2.34 2.34 0 0 1-1.48-2.94L2.93 8a2.18 2.18 0 0 1 1.12-1.41 2.14 2.14 0 0 1 1.68-.12 1.93 1.93 0 0 0 1.78-.29l.13-.1a1.94 1.94 0 0 0 .73-1.51v-.24A2.32 2.32 0 0 1 10.66 2h2.55a2.26 2.26 0 0 1 1.6.67 2.37 2.37 0 0 1 .68 1.68v.28a1.76 1.76 0 0 0 .69 1.43l.11.08a1.74 1.74 0 0 0 1.59.26l.34-.11A2.26 2.26 0 0 1 21.1 7.8l.79 2.52a2.36 2.36 0 0 1-1.46 2.93l-.2.07A1.89 1.89 0 0 0 19 14.6a2 2 0 0 0 .25 1.65l.26.38a2.38 2.38 0 0 1-.5 3.23L17 21.41a2.24 2.24 0 0 1-3.22-.53l-.12-.17a1.75 1.75 0 0 0-1.5-.78 1.8 1.8 0 0 0-1.43.77l-.23.33A2.25 2.25 0 0 1 9 22a2 2 0 0 1-.39 0zM4.4 11.62a3.83 3.83 0 0 1 2.38 2.5v.12a4 4 0 0 1-.46 3.62.38.38 0 0 0 0 .51L8.47 20a.25.25 0 0 0 .37-.07l.23-.33a3.77 3.77 0 0 1 6.2 0l.12.18a.3.3 0 0 0 .18.12.25.25 0 0 0 .19-.05l2.06-1.56a.36.36 0 0 0 .07-.49l-.26-.38A4 4 0 0 1 17.1 14a3.92 3.92 0 0 1 2.49-2.61l.2-.07a.34.34 0 0 0 .19-.44l-.78-2.49a.35.35 0 0 0-.2-.19.21.21 0 0 0-.19 0l-.34.11a3.74 3.74 0 0 1-3.43-.57L15 7.65a3.76 3.76 0 0 1-1.49-3v-.31a.37.37 0 0 0-.1-.26.31.31 0 0 0-.21-.08h-2.54a.31.31 0 0 0-.29.33v.25a3.9 3.9 0 0 1-1.52 3.09l-.13.1a3.91 3.91 0 0 1-3.63.59.22.22 0 0 0-.14 0 .28.28 0 0 0-.12.15L4 11.12a.36.36 0 0 0 .22.45z","data-name":"<Group>"}),e("path",{d:"M12 15.5a3.5 3.5 0 1 1 3.5-3.5 3.5 3.5 0 0 1-3.5 3.5zm0-5a1.5 1.5 0 1 0 1.5 1.5 1.5 1.5 0 0 0-1.5-1.5z"})]})})}),Qc=()=>e("svg",{xmlns:"http://www.w3.org/2000/svg",viewBox:"0 0 24 24",children:e("g",{"data-name":"Layer 2",children:s("g",{"data-name":"share",children:[e("rect",{width:"24",height:"24",opacity:"0"}),e("path",{d:"M18 15a3 3 0 0 0-2.1.86L8 12.34V12v-.33l7.9-3.53A3 3 0 1 0 15 6v.34L7.1 9.86a3 3 0 1 0 0 4.28l7.9 3.53V18a3 3 0 1 0 3-3zm0-10a1 1 0 1 1-1 1 1 1 0 0 1 1-1zM5 13a1 1 0 1 1 1-1 1 1 0 0 1-1 1zm13 6a1 1 0 1 1 1-1 1 1 0 0 1-1 1z"})]})})}),f8=()=>s("svg",{xmlns:"http://www.w3.org/2000/svg",width:"24",height:"24",viewBox:"0 0 24 24",fill:"none",stroke:"currentColor",strokeWidth:"2",strokeLinecap:"round",strokeLinejoin:"round",className:"feather feather-slack",children:[e("path",{d:"M14.5 10c-.83 0-1.5-.67-1.5-1.5v-5c0-.83.67-1.5 1.5-1.5s1.5.67 1.5 1.5v5c0 .83-.67 1.5-1.5 1.5z"}),e("path",{d:"M20.5 10H19V8.5c0-.83.67-1.5 1.5-1.5s1.5.67 1.5 1.5-.67 1.5-1.5 1.5z"}),e("path",{d:"M9.5 14c.83 0 1.5.67 1.5 1.5v5c0 .83-.67 1.5-1.5 1.5S8 21.33 8 20.5v-5c0-.83.67-1.5 1.5-1.5z"}),e("path",{d:"M3.5 14H5v1.5c0 .83-.67 1.5-1.5 1.5S2 16.33 2 15.5 2.67 14 3.5 14z"}),e("path",{d:"M14 14.5c0-.83.67-1.5 1.5-1.5h5c.83 0 1.5.67 1.5 1.5s-.67 1.5-1.5 1.5h-5c-.83 0-1.5-.67-1.5-1.5z"}),e("path",{d:"M15.5 19H14v1.5c0 .83.67 1.5 1.5 1.5s1.5-.67 1.5-1.5-.67-1.5-1.5-1.5z"}),e("path",{d:"M10 9.5C10 8.67 9.33 8 8.5 8h-5C2.67 8 2 8.67 2 9.5S2.67 11 3.5 11h5c.83 0 1.5-.67 1.5-1.5z"}),e("path",{d:"M8.5 5H10V3.5C10 2.67 9.33 2 8.5 2S7 2.67 7 3.5 7.67 5 8.5 5z"})]}),Wc=()=>s("svg",{width:"24",height:"24",viewBox:"0 0 24 24",fill:"none",xmlns:"http://www.w3.org/2000/svg",children:[e("path",{fillRule:"evenodd",clipRule:"evenodd",d:"M6 21H18C19.654 21 21 19.654 21 18V6C21 4.346 19.654 3 18 3H6C4.346 3 3 4.346 3 6V18C3 19.654 4.346 21 6 21ZM5 6C5 5.449 5.449 5 6 5H18C18.551 5 19 5.449 19 6V18C19 18.551 18.551 19 18 19H6C5.449 19 5 18.551 5 18V6Z",fill:"currentColor"}),e("rect",{x:"9",y:"4",width:"2",height:"16",fill:"currentColor"}),e("path",{d:"M16.0955 14.9999C15.9704 14.9999 15.8461 14.9455 15.7613 14.8401L13.6921 12.2686C13.5644 12.1095 13.5661 11.8824 13.6968 11.7255L15.8397 9.15401C15.991 8.97229 16.2614 8.94786 16.4435 9.09915C16.6253 9.25045 16.6497 9.52088 16.498 9.70261L14.5801 12.0045L16.4294 14.3026C16.5777 14.4869 16.5485 14.7569 16.3638 14.9052C16.285 14.9691 16.1898 14.9999 16.0955 14.9999Z",fill:"currentColor",stroke:"currentColor",strokeWidth:"0.5"}),e("mask",{id:"mask0_2304_25",maskUnits:"userSpaceOnUse",x:"3",y:"3",width:"18",height:"18",children:e("path",{fillRule:"evenodd",clipRule:"evenodd",d:"M6 21H18C19.654 21 21 19.654 21 18V6C21 4.346 19.654 3 18 3H6C4.346 3 3 4.346 3 6V18C3 19.654 4.346 21 6 21ZM5 6C5 5.449 5.449 5 6 5H18C18.551 5 19 5.449 19 6V18C19 18.551 18.551 19 18 19H6C5.449 19 5 18.551 5 18V6Z",fill:"white"})}),e("g",{mask:"url(#mask0_2304_25)"})]}),qc=()=>s("svg",{width:"24",height:"24",viewBox:"0 0 24 24",fill:"none",xmlns:"http://www.w3.org/2000/svg",children:[e("path",{fillRule:"evenodd",clipRule:"evenodd",d:"M6 21H18C19.654 21 21 19.654 21 18V6C21 4.346 19.654 3 18 3H6C4.346 3 3 4.346 3 6V18C3 19.654 4.346 21 6 21ZM5 6C5 5.449 5.449 5 6 5H18C18.551 5 19 5.449 19 6V18C19 18.551 18.551 19 18 19H6C5.449 19 5 18.551 5 18V6Z",fill:"currentColor"}),e("rect",{x:"9",y:"4",width:"2",height:"16",fill:"currentColor"}),e("path",{d:"M14.0995 9.00021C14.2247 9.00021 14.349 9.05464 14.4338 9.16008L16.503 11.7316C16.6307 11.8906 16.629 12.1178 16.4982 12.2746L14.3554 14.8461C14.2041 15.0279 13.9337 15.0523 13.7515 14.901C13.5698 14.7497 13.5454 14.4793 13.6971 14.2975L15.615 11.9956L13.7657 9.69752C13.6174 9.51323 13.6465 9.24322 13.8312 9.09493C13.9101 9.03107 14.0052 9.00021 14.0995 9.00021Z",fill:"currentColor",stroke:"currentColor",strokeWidth:"0.5"}),e("mask",{id:"mask0_2304_26",maskUnits:"userSpaceOnUse",x:"3",y:"3",width:"18",height:"18",children:e("path",{fillRule:"evenodd",clipRule:"evenodd",d:"M6 21H18C19.654 21 21 19.654 21 18V6C21 4.346 19.654 3 18 3H6C4.346 3 3 4.346 3 6V18C3 19.654 4.346 21 6 21ZM5 6C5 5.449 5.449 5 6 5H18C18.551 5 19 5.449 19 6V18C19 18.551 18.551 19 18 19H6C5.449 19 5 18.551 5 18V6Z",fill:"white"})}),e("g",{mask:"url(#mask0_2304_26)"})]}),Xc=()=>e("svg",{xmlns:"http://www.w3.org/2000/svg",viewBox:"0 0 24 24",children:e("g",{"data-name":"Layer 2",children:s("g",{"data-name":"sun",children:[e("rect",{width:"24",height:"24",transform:"rotate(180 12 12)",opacity:"0"}),e("path",{d:"M12 6a1 1 0 0 0 1-1V3a1 1 0 0 0-2 0v2a1 1 0 0 0 1 1z"}),e("path",{d:"M21 11h-2a1 1 0 0 0 0 2h2a1 1 0 0 0 0-2z"}),e("path",{d:"M6 12a1 1 0 0 0-1-1H3a1 1 0 0 0 0 2h2a1 1 0 0 0 1-1z"}),e("path",{d:"M6.22 5a1 1 0 0 0-1.39 1.47l1.44 1.39a1 1 0 0 0 .73.28 1 1 0 0 0 .72-.31 1 1 0 0 0 0-1.41z"}),e("path",{d:"M17 8.14a1 1 0 0 0 .69-.28l1.44-1.39A1 1 0 0 0 17.78 5l-1.44 1.42a1 1 0 0 0 0 1.41 1 1 0 0 0 .66.31z"}),e("path",{d:"M12 18a1 1 0 0 0-1 1v2a1 1 0 0 0 2 0v-2a1 1 0 0 0-1-1z"}),e("path",{d:"M17.73 16.14a1 1 0 0 0-1.39 1.44L17.78 19a1 1 0 0 0 .69.28 1 1 0 0 0 .72-.3 1 1 0 0 0 0-1.42z"}),e("path",{d:"M6.27 16.14l-1.44 1.39a1 1 0 0 0 0 1.42 1 1 0 0 0 .72.3 1 1 0 0 0 .67-.25l1.44-1.39a1 1 0 0 0-1.39-1.44z"}),e("path",{d:"M12 8a4 4 0 1 0 4 4 4 4 0 0 0-4-4zm0 6a2 2 0 1 1 2-2 2 2 0 0 1-2 2z"})]})})}),Yc=()=>e("svg",{width:"24",height:"24",viewBox:"0 0 24 24",fill:"none",xmlns:"http://www.w3.org/2000/svg",children:s("g",{id:"timer",children:[e("path",{fillRule:"evenodd",clipRule:"evenodd",d:"M12.994 4.03164C12.9914 4.04002 12.9889 4.0485 12.988 4.058C17.487 4.552 21 8.372 21 13C21 17.963 16.962 22 12 22C7.038 22 3 17.963 3 13C3 8.372 6.513 4.552 11.012 4.058C11.0111 4.0485 11.0086 4.04002 11.006 4.03164C11.003 4.0215 11 4.0115 11 4V3H10C9.448 3 9 2.553 9 2C9 1.447 9.448 1 10 1H14C14.552 1 15 1.447 15 2C15 2.553 14.552 3 14 3H13V4C13 4.0115 12.997 4.0215 12.994 4.03164ZM12 19.75C8.278 19.75 5.25 16.722 5.25 13C5.25 9.278 8.278 6.25 12 6.25C15.722 6.25 18.75 9.278 18.75 13C18.75 16.722 15.722 19.75 12 19.75ZM16 13C16 12.447 15.552 12 15 12H13V10C13 9.447 12.552 9 12 9C11.448 9 11 9.447 11 10V13C11 13.553 11.448 14 12 14H15C15.552 14 16 13.553 16 13Z",fill:"currentColor"}),e("mask",{id:"mask0_0_1974",maskUnits:"userSpaceOnUse",x:"3",y:"1",width:"18",height:"21",children:e("path",{fillRule:"evenodd",clipRule:"evenodd",d:"M12.994 4.03164C12.9914 4.04002 12.9889 4.0485 12.988 4.058C17.487 4.552 21 8.372 21 13C21 17.963 16.962 22 12 22C7.038 22 3 17.963 3 13C3 8.372 6.513 4.552 11.012 4.058C11.0111 4.0485 11.0086 4.04002 11.006 4.03164C11.003 4.0215 11 4.0115 11 4V3H10C9.448 3 9 2.553 9 2C9 1.447 9.448 1 10 1H14C14.552 1 15 1.447 15 2C15 2.553 14.552 3 14 3H13V4C13 4.0115 12.997 4.0215 12.994 4.03164ZM12 19.75C8.278 19.75 5.25 16.722 5.25 13C5.25 9.278 8.278 6.25 12 6.25C15.722 6.25 18.75 9.278 18.75 13C18.75 16.722 15.722 19.75 12 19.75ZM16 13C16 12.447 15.552 12 15 12H13V10C13 9.447 12.552 9 12 9C11.448 9 11 9.447 11 10V13C11 13.553 11.448 14 12 14H15C15.552 14 16 13.553 16 13Z",fill:"currentColor"})})]})}),Jc=()=>e("svg",{width:"24",height:"24",viewBox:"0 0 24 24",fill:"none",xmlns:"http://www.w3.org/2000/svg",children:e("path",{fillRule:"evenodd",clipRule:"evenodd",d:"M12.988 4.058C12.9889 4.0485 12.9914 4.04002 12.994 4.03164C12.997 4.0215 13 4.0115 13 4V3H14C14.552 3 15 2.553 15 2C15 1.447 14.552 1 14 1H10C9.448 1 9 1.447 9 2C9 2.553 9.448 3 10 3H11V4C11 4.0115 11.003 4.0215 11.006 4.03164C11.0086 4.04002 11.0111 4.0485 11.012 4.058C10.1864 4.14865 9.394 4.35131 8.65042 4.65041L10.4335 6.43348C10.9364 6.31352 11.4609 6.25 12 6.25C15.722 6.25 18.75 9.278 18.75 13C18.75 13.5391 18.6865 14.0636 18.5665 14.5665L20.3525 16.3525C20.7701 15.3159 21 14.1843 21 13C21 8.372 17.487 4.552 12.988 4.058ZM12 19.75C12.82 19.75 13.6063 19.603 14.334 19.334L16.0408 21.0408C14.825 21.6543 13.4521 22 12 22C7.038 22 3 17.963 3 13C3 11.8156 3.23007 10.6842 3.64786 9.64786L5.43348 11.4335C5.31353 11.9364 5.25 12.4609 5.25 13C5.25 16.722 8.278 19.75 12 19.75ZM3.85828 3.09123C3.35638 2.61722 2.56525 2.63982 2.09124 3.14172C1.61722 3.64362 1.63983 4.43475 2.14172 4.90877L20.1417 21.9088C20.6436 22.3828 21.4348 22.3602 21.9088 21.8583C22.3828 21.3564 22.3602 20.5652 21.8583 20.0912L3.85828 3.09123Z",fill:"currentColor"})}),b8=()=>e("svg",{xmlns:"http://www.w3.org/2000/svg",width:"24",height:"24",viewBox:"0 0 24 24",fill:"none",stroke:"currentColor",strokeWidth:"2",strokeLinecap:"round",strokeLinejoin:"round",children:e("path",{fill:"None",d:"M14 9V5a3 3 0 0 0-3-3l-4 9v11h11.28a2 2 0 0 0 2-1.7l1.38-9a2 2 0 0 0-2-2.3zM7 22H4a2 2 0 0 1-2-2v-7a2 2 0 0 1 2-2h3"})}),y8=()=>e("svg",{xmlns:"http://www.w3.org/2000/svg",width:"24",height:"24",viewBox:"0 0 24 24",fill:"none",stroke:"currentColor",strokeWidth:"2",strokeLinecap:"round",strokeLinejoin:"round",children:e("path",{fill:"None",d:"M10 15v4a3 3 0 0 0 3 3l4-9V2H5.72a2 2 0 0 0-2 1.7l-1.38 9a2 2 0 0 0 2 2.3zm7-13h2.67A2.31 2.31 0 0 1 22 4v7a2.31 2.31 0 0 1-2.33 2H17"})}),e0=()=>e("svg",{width:"16",height:"16",viewBox:"0 0 16 16",fill:"none",xmlns:"http://www.w3.org/2000/svg",children:s("g",{children:[e("path",{fillRule:"evenodd",clipRule:"evenodd",d:"M7.32264 7.73275L6.26721 6.67733C5.93552 6.34564 5.39776 6.34564 5.06607 6.67733L4.01064 7.73275C3.67895 8.06445 3.67895 8.60221 4.01064 8.9339L5.06607 9.98933C5.39776 10.321 5.93552 10.321 6.26721 9.98933L7.32264 8.9339C7.65433 8.60221 7.65433 8.06445 7.32264 7.73275ZM4.75695 8.33333L5.66664 7.42364L6.57633 8.33333L5.66664 9.24302L4.75695 8.33333Z"}),e("path",{fillRule:"evenodd",clipRule:"evenodd",d:"M5.66672 13.3333C6.43362 13.3333 7.16019 13.1607 7.80972 12.8521C8.4596 13.1608 9.18643 13.3333 9.95243 13.3333C12.7139 13.3333 14.9524 11.0948 14.9524 8.33334C14.9524 5.57192 12.7139 3.33334 9.95243 3.33334C9.18643 3.33334 8.4596 3.50591 7.80969 3.81458C7.16019 3.50601 6.43362 3.33334 5.66672 3.33334C2.90529 3.33334 0.666718 5.57192 0.666718 8.33334C0.666718 11.0948 2.90529 13.3333 5.66672 13.3333ZM5.66672 4.28572C3.43129 4.28572 1.6191 6.09791 1.6191 8.33334C1.6191 10.5688 3.43129 12.381 5.66672 12.381C7.72319 12.381 9.42146 10.8473 9.68019 8.86141C9.70272 8.68858 9.71434 8.51232 9.71434 8.33334C9.71434 8.19363 9.70727 8.05556 9.69343 7.91949C9.48617 5.87846 7.76243 4.28572 5.66672 4.28572ZM9.95243 12.381C9.55679 12.381 9.17481 12.3243 8.81393 12.2188C9.81991 11.4029 10.5028 10.2043 10.6409 8.84456C10.658 8.67649 10.6667 8.50594 10.6667 8.33334C10.6667 8.10822 10.6518 7.88658 10.623 7.66934C10.451 6.37275 9.78208 5.23306 8.81393 4.44791C9.17481 4.34237 9.55679 4.28572 9.95243 4.28572C12.1879 4.28572 14.0001 6.09791 14.0001 8.33334C14.0001 10.5688 12.1879 12.381 9.95243 12.381Z"})]})}),n0=()=>e("svg",{width:"24",height:"24",viewBox:"0 0 24 24",fill:"none",xmlns:"http://www.w3.org/2000/svg",children:e("path",{fillRule:"evenodd",clipRule:"evenodd",d:"M7 5C7 4.44772 6.55228 4 6 4C5.44772 4 5 4.44772 5 5V9V15C5 16.6569 6.34315 18 8 18H13.4375C13.8375 19.0243 14.834 19.75 16 19.75C17.5188 19.75 18.75 18.5188 18.75 17C18.75 15.4812 17.5188 14.25 16 14.25C14.834 14.25 13.8375 14.9757 13.4375 16H8C7.44772 16 7 15.5523 7 15V11H13.4375C13.8375 12.0243 14.834 12.75 16 12.75C17.5188 12.75 18.75 11.5188 18.75 10C18.75 8.48122 17.5188 7.25 16 7.25C14.834 7.25 13.8375 7.97566 13.4375 9H7V5ZM16 8.75C15.3096 8.75 14.75 9.30964 14.75 10C14.75 10.6904 15.3096 11.25 16 11.25C16.6904 11.25 17.25 10.6904 17.25 10C17.25 9.30964 16.6904 8.75 16 8.75ZM14.75 17C14.75 16.3096 15.3096 15.75 16 15.75C16.6904 15.75 17.25 16.3096 17.25 17C17.25 17.6904 16.6904 18.25 16 18.25C15.3096 18.25 14.75 17.6904 14.75 17Z"})}),Tt=()=>e("svg",{xmlns:"http://www.w3.org/2000/svg",viewBox:"0 0 24 24",children:e("g",{"data-name":"Layer 2",children:s("g",{"data-name":"trash",children:[e("rect",{width:"24",height:"24",opacity:"0"}),e("path",{d:"M21 6h-5V4.33A2.42 2.42 0 0 0 13.5 2h-3A2.42 2.42 0 0 0 8 4.33V6H3a1 1 0 0 0 0 2h1v11a3 3 0 0 0 3 3h10a3 3 0 0 0 3-3V8h1a1 1 0 0 0 0-2zM10 4.33c0-.16.21-.33.5-.33h3c.29 0 .5.17.5.33V6h-4zM18 19a1 1 0 0 1-1 1H7a1 1 0 0 1-1-1V8h12z"})]})})}),Ae=()=>e(T,{svg:e(Sc,{}),css:m`
        font-size: 0.8rem;
      `});function a0(n,{filled:a}={filled:!0}){let t;switch(n){case"warning":t=a?e(Cc,{}):e(vc,{});break;case"info":t=a?e(Pc,{}):e(St,{});break;case"danger":t=a?e(ki,{}):e(Lt,{});break;case"success":t=a?e(wt,{}):e(wi,{});break}return e(T,{svg:t})}const t0=m`
  --alert-base-color: var(--ac-global-color-info);
  --alert-bg-color: lch(from var(--alert-base-color) l c h / 0.1);
  --alert-border-color: lch(from var(--alert-base-color) l c h / 0.3);
  --alert-text-color: lch(
    from var(--alert-base-color) calc((50 - l) * infinity) 0 0
  );

  padding: var(--ac-global-dimension-static-size-100)
    var(--ac-global-dimension-static-size-200);
  border-radius: var(--ac-global-rounding-small);
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
    --alert-base-color: var(--ac-global-color-warning);
  }

  &[data-variant="info"] {
    --alert-base-color: var(--ac-global-color-info);
  }

  &[data-variant="danger"] {
    --alert-base-color: var(--ac-global-color-danger);
  }

  &[data-variant="success"] {
    --alert-base-color: var(--ac-global-color-success);
  }

  &[data-theme="light"] {
    --alert-bg-color: lch(from var(--alert-base-color) l c h / 0.1);
    --alert-border-color: lch(from var(--alert-base-color) l c h / 0.3);
    --alert-text-color: var(--alert-base-color);
  }

  &[data-theme="dark"] {
    --alert-bg-color: lch(from var(--alert-base-color) l c h / 0.2);
    --alert-border-color: lch(from var(--alert-base-color) l c h / 0.4);
    --alert-text-color: lch(
      from var(--alert-base-color) calc((l) * infinity) c h / 1
    );
  }

  .ac-alert__icon-title-wrap {
    display: flex;
    flex-direction: row;

    .ac-icon-wrap {
      margin-top: 4px;
      margin-right: var(--ac-global-dimension-static-size-200);
      font-size: var(--ac-global-font-size-l);
    }
  }
`,l0=m`
  display: flex;
  flex-direction: row;
  align-items: flex-start;
  flex: 1 1 auto;
`,i0=m`
  background-color: transparent;
  color: inherit;
  padding: 0;
  border: none;
  cursor: pointer;
  width: 20px;
  height: 20px;
  margin-left: var(--ac-global-dimension-static-size-200);
`,ya=({variant:n,title:a,icon:t,children:l,showIcon:i=!0,dismissable:r=!1,onDismissClick:o,banner:c=!1,extra:d,...u})=>{const{theme:g}=le();return!t&&i&&(t=a0(n)),s("div",{...u,css:t0,"data-variant":n,"data-banner":c,"data-has-title":!!a,"data-theme":g,children:[s("div",{css:l0,className:"ac-alert__icon-title-wrap",children:[t,s("div",{children:[a?e(C,{elementType:"h5",size:"L",weight:"heavy",color:"inherit",children:a}):null,e(C,{color:"inherit",size:"M",children:l})]})]}),d,r?e("button",{css:i0,onClick:o,children:e(T,{svg:e(ba,{})})}):null]})},r0=m`
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
  > .ac-disclosure:not(:last-child) {
    &[data-expanded="true"] {
      border-bottom: 1px solid var(--ac-global-border-color-default);
    }
  }

  &[data-size="S"] > * {
    .react-aria-Heading {
      .react-aria-Button[slot="trigger"] {
        padding: var(--ac-global-dimension-static-size-50);
      }
    }
  }
`,o0=m`
  .react-aria-Heading {
    margin: 0;
  }

  .react-aria-Button[slot="trigger"] {
    // reset trigger styles
    background: none;
    border: none;
    box-shadow: none;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 8px;
    font-size: var(--ac-global-font-size-s);
    line-height: var(--ac-global-line-height-s);
    padding: var(--ac-global-dimension-static-size-100)
      var(--ac-global-dimension-static-size-200);

    // style trigger
    color: var(--ac-global-text-color-900);
    border-bottom: 1px solid var(--ac-global-border-color-default);
    outline: none;
    background-color: transparent;
    &:hover:not([disabled]) {
      background-color: var(--ac-global-disclosure-background-color-active);
    }
    &[data-focus-visible] {
      outline: 1px solid var(--ac-global-input-field-border-color-active);
      outline-offset: -1px;
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
      transition: rotate 200ms;
      width: 1em;
      height: 1em;
      fill: currentColor;
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
`,v8=({className:n,css:a,size:t,...l})=>e(Eo,{allowsMultipleExpanded:!0,className:V("ac-disclosure-group",n),css:m(r0,a),"data-size":t,...l}),C8=({size:n,className:a,...t})=>e(Do,{className:V("ac-disclosure",a),css:o0,"data-size":n,defaultExpanded:!0,...t}),k8=({className:n,...a})=>e(_o,{className:V("ac-disclosure-panel",n),...a}),L8=({children:n,arrowPosition:a,justifyContent:t,width:l})=>e(Rl,{className:"react-aria-Heading ac-disclosure-trigger",children:s(Ln,{slot:"trigger","data-arrow-position":a,style:{width:l},children:[e(S,{justifyContent:t,alignItems:"center",width:"100%",gap:"size-100",children:n}),e(T,{svg:e(Ci,{})})]})}),Le=m`
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
    font-size: var(--ac-global-font-size-xs);
    line-height: var(--ac-global-line-height-xs);
    font-weight: var(--px-font-weight-heavy);
  }

  .react-aria-Input,
  .react-aria-TextArea {
    transition: all 0.2s ease-in-out;
    margin: 0;
    flex: 1 1 auto;
    font-size: var(--ac-global-font-size-s);
    min-width: var(--ac-global-input-field-min-width);
    background-color: var(--ac-global-input-field-background-color);
    color: var(--ac-global-text-color-900);
    border: var(--ac-global-border-size-thin) solid
      var(--ac-global-input-field-border-color);
    border-radius: var(--ac-global-rounding-small);
    vertical-align: middle;

    &[data-focused] {
      // TODO: figure out focus ring behavior. For now the color is enough
      outline: none;
    }
    &[data-focused]:not([data-invalid]) {
      border: 1px solid var(--ac-global-input-field-border-color-active);
    }
    &[data-hovered]:not([data-disabled]):not([data-invalid]) {
      border: 1px solid var(--ac-global-input-field-border-color-active);
    }
    &[data-disabled] {
      opacity: var(--ac-global-opacity-disabled);
    }
    &[data-invalid="true"] {
      border-color: var(--ac-global-color-danger);
    }
    &::placeholder {
      color: var(--ac-text-color-placeholder);
      font-style: italic;
    }
  }
  [slot="description"],
  [slot="errorMessage"],
  .react-aria-FieldError {
    /* The overriding cascade here is non ideal but it lets us have only one notion of text  */
    font-size: var(--ac-global-font-size-xs) !important;
    padding-top: var(--ac-global-dimension-static-size-50);
    display: inline-block;
    line-height: var(--ac-global-dimension-static-font-size-200) !important;
  }

  [slot="description"] {
    color: var(--ac-global-text-color-500);
  }

  .react-aria-FieldError {
    color: var(--ac-global-color-danger);
  }
`,s0=m`
  width: var(--trigger-width);
  background-color: var(--ac-global-menu-background-color);
  border-radius: var(--ac-global-rounding-small);
  color: var(--ac-global-text-color-900);
  box-shadow: 0px 4px 10px var(--px-overlay-shadow-color);
  border: 1px solid var(--ac-global-menu-border-color);
  max-height: inherit;
`,va=m`
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
    --textfield-input-height: var(--ac-global-input-height-s);
    --textfield-vertical-padding: 6px;
    --textfield-horizontal-padding: 6px;
  }
  &[data-size="M"] {
    --textfield-input-height: var(--ac-global-input-height-m);
    --textfield-vertical-padding: 10px;
    --textfield-horizontal-padding: var(--ac-global-dimension-static-size-200);
    --icon-size: var(--ac-global-font-size-l);
  }

  &:has(.ac-field-icon) {
    .react-aria-Input {
      padding-right: calc(
        var(--textfield-horizontal-padding) + var(--icon-size)
      );
    }
  }

  /* Icons */
  .ac-field-icon {
    position: absolute;
    right: var(--textfield-horizontal-padding);
    top: var(--field-icon-vertical-position);
  }

  .react-aria-Input,
  .react-aria-TextArea,
  input {
    width: 100%;
    margin: 0;
    border: var(--ac-global-border-size-thin) solid
      var(
        --ac-field-border-color-override,
        var(--ac-global-input-field-border-color)
      );
    border-radius: var(--ac-global-rounding-small);
    background-color: var(--ac-global-input-field-background-color);
    color: var(--ac-global-text-color-900);
    padding: var(--textfield-vertical-padding)
      var(--textfield-horizontal-padding);
    box-sizing: border-box;
    outline-offset: -1px;
    outline: var(--ac-global-border-size-thin) solid transparent;
    &[data-focused]:not([data-invalid]) {
      outline: 1px solid var(--ac-global-input-field-border-color-active);
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
`,c0=m`
  &[data-size="M"] {
    --combobox-input-height: var(--ac-global-input-height-s);
    --combobox-vertical-padding: 6px;
    --combobox-start-padding: var(--ac-global-dimension-static-size-100);
    --combobox-end-padding: var(--ac-global-dimension-static-size-50);
  }
  &[data-size="L"] {
    --combobox-input-height: var(--ac-global-input-height-m);
    --combobox-vertical-padding: 10px;
    --combobox-start-padding: var(--ac-global-dimension-static-size-200);
    --combobox-end-padding: var(--ac-global-dimension-static-size-100);
  }
  color: var(--ac-global-text-color-900);
  &[data-required] {
    .react-aria-Label {
      &::after {
        content: " *";
      }
    }
  }

  .px-combobox-container {
    display: flex;
    flex-direction: row;
    min-width: 200px;
    position: relative;

    .react-aria-Input {
      height: var(--combobox-input-height);
      box-sizing: border-box;
      padding: var(--combobox-vertical-padding) var(--combobox-end-padding)
        var(--combobox-vertical-padding) var(--combobox-start-padding);
      &:hover:not([disabled]) {
        background-color: var(--ac-global-input-field-border-color-hover);
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
        opacity: var(--ac-global-opacity-disabled);
      }
    }
  }
`,d0=m(s0,m`
    .react-aria-ListBox {
      display: block;
      width: unset;
      max-height: inherit;
      min-height: unset;
      border: none;
      overflow: auto;
    }
  `),u0=m`
  outline: none;
  display: flex;
  align-items: center;
  justify-content: space-between;
  color: var(--ac-global-text-color-900);
  padding: var(--ac-global-dimension-static-size-100)
    var(--ac-global-dimension-static-size-200);
  font-size: var(--ac-global-dimension-static-font-size-100);
  cursor: pointer;
  position: relative;
  & > .ac-icon-wrap.px-menu-item__selected-checkmark {
    height: var(--ac-global-dimension-static-size-200);
    width: var(--ac-global-dimension-static-size-200);
  }
  &[href] {
    text-decoration: none;
    cursor: pointer;
  }
  &[data-selected] {
    i {
      color: var(--ac-global-color-primary);
    }
  }
  &[data-focused],
  &[data-hovered] {
    background-color: var(--ac-global-menu-item-background-color-hover);
  }

  &[data-disabled] {
    cursor: not-allowed;
    color: var(--ac-global-color-text-30);
  }
  &[data-focus-visible] {
    outline: none;
  }
`,Oa=n=>{n.preventDefault(),n.stopPropagation()};function w8({label:n,placeholder:a,description:t,errorMessage:l,children:i,container:r,size:o="M",width:c,stopPropagation:d,renderEmptyState:u,isInvalid:g,...h}){return s(Ko,{...h,css:m(Le,c0),"data-size":o,isInvalid:g||!!l,style:{width:c},children:[n&&e(K,{children:n}),s("div",{className:"px-combobox-container",onClick:d?Oa:void 0,onKeyDown:d?Oa:void 0,onKeyUp:d?Oa:void 0,children:[e(j,{placeholder:a}),e(Ln,{children:e(Ae,{})})]}),t&&!l?e(Vl,{slot:"description",children:t}):null,e(W,{children:l}),e(Nl,{css:d0,UNSTABLE_portalContainer:r,children:e(Ol,{renderEmptyState:u,children:i})})]})}function S8(n){const{children:a,...t}=n;return e(bn,{...t,css:u0,children:({isSelected:l})=>s(U,{children:[a,l&&e(T,{svg:e(Mc,{}),className:"px-menu-item__selected-checkmark"})]})})}const Ca=m`
  --button-border-color: var(--ac-global-input-field-border-color);
  border: 1px solid var(--button-border-color);
  font-size: var(--ac-global-dimension-static-font-size-100);
  line-height: 20px; // TODO(mikeldking): move this into a consistent variable
  margin: 0;
  flex: none;

  display: flex;
  gap: var(--ac-global-dimension-static-size-100);
  justify-content: center;
  align-items: center;
  flex-direction: row;
  box-sizing: border-box;
  border-radius: var(--ac-global-rounding-small);
  color: var(--ac-global-text-color-900);
  transition: background-color 0.2s ease-in-out;
  cursor: pointer;

  /* Disable outline since there are other mechanisms to show focus */
  outline: none;
  &[data-focus-visible] {
    // Only show outline on focus-visible, aka only when tabbed but not clicked
    outline: 1px solid var(--ac-global-input-field-border-color-active);
    outline-offset: 1px;
  }
  &[disabled] {
    cursor: default;
    opacity: var(--ac-opacity-disabled);
  }
  &[data-size="S"] {
    height: var(--ac-global-button-height-s);
  }
  &[data-size="M"] {
    height: var(--ac-global-button-height-m);
  }
  &[data-size="M"][data-childless="false"] {
    padding: var(--ac-global-dimension-static-size-100)
      var(--ac-global-dimension-static-size-200);
  }
  &[data-size="S"][data-childless="false"] {
    padding: var(--ac-global-dimension-static-size-50)
      var(--ac-global-dimension-static-size-100);
  }
  &[data-size="M"][data-childless="true"] {
    padding: var(--ac-global-dimension-static-size-100)
      var(--ac-global-dimension-static-size-100);
  }
  &[data-size="S"][data-childless="true"] {
    padding: var(--ac-global-dimension-static-size-50)
      var(--ac-global-dimension-static-size-50);
  }
  // The default style

  background-color: var(--ac-global-input-field-background-color);
  border-color: var(--button-border-color);
  &:hover:not([disabled]) {
    background-color: var(--ac-global-input-field-border-color-hover);
  }

  &[data-variant="primary"] {
    background-color: var(--ac-global-button-primary-background-color);
    --button-border-color: var(--ac-global-button-primary-border-color);
    color: var(--ac-global-button-primary-foreground-color);
    &:hover:not([disabled]) {
      background-color: var(--ac-global-button-primary-background-color-hover);
    }
  }
  &[data-variant="danger"] {
    background-color: var(--ac-global-button-danger-background-color);
    --button-border-color: var(--ac-global-button-danger-border-color);
    color: var(--ac-global-static-color-white-900);
    &:hover:not([disabled]) {
      background-color: var(--ac-global-button-danger-background-color-hover);
    }
  }
  &[data-variant="success"] {
    background-color: var(--ac-global-button-success-background-color);
    --button-border-color: var(--ac-global-button-success-border-color);
    color: var(--ac-global-static-color-white-900);
    &:hover:not([disabled]) {
      background-color: var(--ac-global-button-success-background-color-hover);
    }
  }
  &[data-variant="quiet"] {
    background-color: transparent;
    --button-border-color: transparent;
    &:hover:not([disabled]) {
      border-color: transparent;
      background-color: var(--ac-global-input-field-background-color-active);
    }
  }

  kbd {
    background-color: var(--ac-global-color-grey-400);
    border-radius: var(--ac-global-rounding-small);
    padding: var(--ac-global-dimension-size-50)
      var(--ac-global-dimension-size-75);
    font-size: var(--ac-global-font-size-xs);
    line-height: var(--ac-global-font-size-xxs);
    display: flex;
    align-items: center;
    justify-content: center;
    gap: var(--ac-global-dimension-static-size-25);
    text-transform: uppercase;
  }

  &[data-variant="primary"] {
    kbd {
      background-color: var(--ac-global-color-grey-700);
    }
  }
`;function g0(n,a){const{size:t,variant:l="default",leadingVisual:i,trailingVisual:r,children:o,css:c,className:d,...u}=n,g=At(),h=t||g||"M",f=p.useCallback(b=>s(U,{children:[i,typeof o=="function"?o(b):o,r]}),[i,r,o]);return e(Ln,{...u,ref:a,"data-size":h,"data-variant":l,"data-childless":!o,css:m(Ca,c),className:V("react-aria-Button",d),children:f})}const z=p.forwardRef(g0),m0=m`
  text-decoration: none;
  user-select: none;
  &[data-disabled="true"] {
    pointer-events: none;
    cursor: default;
    opacity: var(--ac-opacity-disabled);
  }
`;function p0(n,a){const{size:t="M",variant:l="default",leadingVisual:i,trailingVisual:r,children:o,css:c,isDisabled:d,to:u}=n;return s(ua,{ref:a,"data-size":t,"data-variant":l,"data-childless":!o,"data-disabled":d,css:m(Ca,m0,c),to:u,children:[i,o,r]})}const x8=p.forwardRef(p0),h0=m`
  text-decoration: none;
  user-select: none;
  &[data-disabled="true"] {
    pointer-events: none;
    cursor: default;
    opacity: var(--ac-opacity-disabled);
  }
`;function f0(n,a){const{size:t="M",variant:l="default",leadingVisual:i,trailingVisual:r,children:o,css:c,isDisabled:d,target:u="_blank",...g}=n;return s("a",{ref:a,target:u,rel:"noopener noreferrer","data-size":t,"data-variant":l,"data-childless":!o,"data-disabled":d,css:m(Ca,h0,c),tabIndex:d?-1:void 0,"aria-disabled":d,...g,children:[i,o,r]})}const T8=rn.forwardRef(f0),b0=n=>{if(n==="inherit")return"inherit";if(n.startsWith("text-")){const[,a]=n.split("-");return`var(--ac-global-text-color-${a})`}return Un(n)},y0=n=>m`
  --icon-button-font-size-s: var(--ac-global-font-size-l);
  --icon-button-font-size-m: var(--ac-global-font-size-xl);
  --icon-button-font-size-l: var(--ac-global-font-size-2xl);

  display: inline-flex;
  align-items: center;
  justify-content: center;
  border: var(--ac-global-border-size-thin) solid transparent;
  border-radius: var(--ac-global-rounding-small);
  color: ${b0(n)};
  background-color: transparent;
  cursor: pointer;
  transition: all 0.2s ease;
  position: relative;
  padding: 0;

  &[data-size="S"] {
    width: var(--ac-global-button-height-s);
    height: var(--ac-global-button-height-s);
    .ac-icon-wrap {
      font-size: var(--icon-button-font-size-s);
    }
  }

  &[data-size="M"] {
    width: var(--ac-global-button-height-m);
    height: var(--ac-global-button-height-m);
    .ac-icon-wrap {
      font-size: var(--icon-button-font-size-m);
    }
  }

  .ac-icon-wrap {
    opacity: 0.7;
    transition: opacity 0.2s ease;
  }

  &[data-hovered] {
    background-color: var(--ac-hover-background);
    .ac-icon-wrap {
      opacity: 1;
    }
  }

  &[data-pressed] {
    background-color: var(--ac-global-color-primary-100);
    color: var(--ac-global-text-color-900);
  }

  &[data-focus-visible] {
    outline: var(--ac-global-border-size-thick) solid var(--ac-focus-ring-color);
    outline-offset: var(--ac-global-border-offset-thin);
  }

  &[data-disabled] {
    opacity: var(--ac-global-opacity-disabled);
    cursor: not-allowed;
  }
`;function v0({size:n="M",color:a="text-700",children:t,...l}){return e(Ln,{css:y0(a),"data-size":n,...l,children:t})}function C0(n,a){const{children:t,elementType:l="div",...i}=n,{styleProps:r}=Vn(n,bi);return e(l,{...$l(i),...r,ref:a,css:m`
        overflow: hidden;
        box-sizing: border-box;
      `,className:"ac-view",children:t})}const w=p.forwardRef(C0),k0=m`
  display: flex;
`,L0={direction:["flexDirection",ge],wrap:["flexWrap",S0],justifyContent:["justifyContent",Na],alignItems:["alignItems",Na],alignContent:["alignContent",Na]};function w0(n,a){const{children:t,className:l,...i}=n,r=["base"],{styleProps:o}=Vn(i),{styleProps:c}=Vn(i,L0),d={...o.style,...c.style};return n.gap!=null&&(d.gap=Va(n.gap,r)),n.columnGap!=null&&(d.columnGap=Va(n.columnGap,r)),n.rowGap!=null&&(d.rowGap=Va(n.rowGap,r)),e("div",{css:k0,...$l(i),className:V("flex",l),style:d,ref:a,children:t})}function Na(n){return n==="start"?"flex-start":n==="end"?"flex-end":n}function S0(n){return typeof n=="boolean"?n?"wrap":"nowrap":n}const S=p.forwardRef(w0),x0=m`
  display: flex;
  align-items: center;
  gap: var(--ac-global-dimension-size-100);
`,T0=p.forwardRef(({size:n,...a},t)=>e(ka,{size:n,children:e(Po,{...a,ref:t,css:x0,className:"ac-group react-aria-Group"})}));T0.displayName="Group";function A0(n,a){const{size:t="M",...l}=n;return e(Bl,{"data-size":t,className:"ac-textfield",ref:a,...l,css:m(Le,va)})}const Q=p.forwardRef(A0),I0=m`
  --searchfield-icon-left-padding: var(--textfield-horizontal-padding);

  &[data-size="M"] {
    --searchfield-icon-left-padding: calc(
      var(--textfield-horizontal-padding) - 0.4rem
    );
  }

  display: grid;
  grid-template-areas:
    "label label"
    "icon input"
    "help  help";
  grid-template-columns: auto 1fr;
  .react-aria-Label {
    grid-area: label;
  }
  .ac-search-icon {
    grid-area: icon;
    position: absolute;
    left: var(--searchfield-icon-left-padding);
    top: 50%;
    transform: translateY(-50%);
  }
  .react-aria-Input {
    grid-area: input;
    width: 100%;
  }
  [slot="description"],
  [slot="errorMessage"],
  .react-aria-FieldError {
    grid-area: help;
  }

  /* Adjust the padding if there is an icon */
  .ac-search-icon + .react-aria-Input {
    padding-left: calc(
      2 * var(--searchfield-icon-left-padding) + 1rem
    ) !important;
  }

  &[data-invalid="true"] {
    .ac-search-icon {
      color: var(--ac-global-color-danger);
    }
  }
`;function z0(n,a){const{size:t="M",...l}=n;return e(Vo,{"data-size":t,className:"ac-searchfield",ref:a,...l,css:m(Le,va,I0)})}const M0=p.forwardRef(z0),Ii=p.createContext({size:"M"});function ka({size:n="M",children:a}){return e(Ii.Provider,{value:{size:n},children:a})}function At(){return p.useContext(Ii).size}const zi=p.createContext(null);function F0(){const n=p.useContext(zi);if(!n)throw new Error("useCredentialContext must be used within a CredentialContext.Provider");return n}function E0(n,a){const{size:t="M",children:l,...i}=n,[r,o]=p.useState(!1);return e(zi.Provider,{value:{isVisible:r,setIsVisible:o},children:e(ka,{size:t,children:e(Bl,{"data-size":t,className:"ac-credentialfield",autoComplete:"off",ref:a,...i,css:m(Le,va),children:l})})})}const A8=p.forwardRef(E0);function D0(n,a){const{isVisible:t,setIsVisible:l}=F0(),i=At(),{disabled:r,readOnly:o,...c}=n;return s("div",{"data-size":i,"data-testid":"credential-input",css:m`
        position: relative;
        display: flex;
        align-items: center;
        width: 100%;
        // The 2px (e.g. 50) is to account making the toggle button to be slightly bigger
        --credential-visibility-toggle-size: calc(
          var(--textfield-input-height) - 2 *
            var(--textfield-vertical-padding) +
            var(--ac-global-dimension-size-50)
        );

        & > input {
          padding-right: calc(
            var(--textfield-vertical-padding) +
              var(--credential-visibility-toggle-size) +
              var(--textfield-vertical-padding)
          ) !important; // Don't want to fight specificity here
        }

        .ac-credential-input__toggle {
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
          color: var(--ac-global-text-color-700);
          display: flex;
          align-items: center;
          justify-content: center;
          border-radius: var(--ac-global-rounding-small);
          transition: background-color 0.2s;
          background-color: var(--ac-global-color-grey-200);
          &:hover {
            background-color: var(--ac-global-color-grey-300);
          }

          &:focus-visible {
            outline: 2px solid var(--ac-global-color-primary);
            outline-offset: 2px;
          }

          &[disabled] {
            cursor: not-allowed;
            opacity: 0.5;
          }
        }
      `,children:[e(j,{...c,ref:a,type:t?"text":"password",disabled:r,readOnly:o}),e(Ln,{className:"ac-credential-input__toggle",onPress:()=>l(!t),isDisabled:r||o,"aria-label":t?"Hide credential":"Show credential",children:e(T,{svg:t?e(Dc,{}):e(_c,{})})})]})}const I8=p.forwardRef(D0),_0=m`
  .react-aria-Input {
    text-align: right;
  }
`,Mi=p.forwardRef(function(a,t){const{size:l="M",...i}=a;return e(Ro,{"data-size":l,...i,className:V("ac-textfield react-aria-NumberField",a.className),ref:t,css:m(Le,va,_0)})}),K0=()=>e(T,{className:"ac-search-icon",svg:e(Uc,{})});function z8({onChange:n,debounceMs:a=200,placeholder:t,...l}){const i=p.useMemo(()=>Hl(o=>{p.startTransition(()=>{n(o)})},a),[n,a]),r=p.useCallback(o=>{i(o)},[i]);return s(M0,{onChange:r,...l,children:[e(K0,{}),e(j,{placeholder:t})]})}const P0=m`
  border: 1px solid var(--ac-global-border-color-light);
  forced-color-adjust: none;
  border-radius: var(--ac-global-rounding-small);
  padding: var(--ac-global-dimension-size-50)
    var(--ac-global-dimension-size-100);
  font-size: var(--ac-global-font-size-s);
  color: var(--ac-global-text-color-900);
  outline: none;
  cursor: default;
  display: flex;
  align-items: center;
  transition: all 200ms;

  &[data-hovered] {
    border-color: var(--ac-global-border-color-dark);
  }

  &[data-focus-visible] {
    outline: 1px solid var(--ac-global-color-primary);
    outline-offset: 1px;
  }

  &[data-selected] {
    border-color: var(--ac-global-color-primary);
    background: var(--ac-global-color-primary-700);
  }
`;function V0(n,a){return e(Oo,{...n,ref:a,css:P0})}p.forwardRef(V0);function R0(n,a){return e(No,{...n,ref:a,css:Le})}p.forwardRef(R0);const O0=m`
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: var(--ac-global-dimension-size-50);
  height: 28px;
`;function N0(n,a){return e($o,{...n,ref:a,css:O0})}p.forwardRef(N0);function $0(n,a){return e(jl,{...n,ref:a,children:e("svg",{width:12,height:12,viewBox:"0 0 12 12",children:e("path",{d:"M0 0 L6 6 L12 0"})})})}const It=p.forwardRef($0),rl=Me`
 100% {
  from {
     transform: var(--origin);
     opacity: 0;
   }

   to {
     transform: translateY(0);
     opacity: 1;
   }
  }
`,B0=m`
  box-sizing: border-box;
  --background-color: var(--ac-global-popover-background-color);
  transition:
    transform 200ms,
    opacity 200ms;
  border: 1px solid var(--ac-global-border-color-light);
  box-shadow: 3px 5px 10px rgba(0 0 0 / 0.2);
  border-radius: var(--ac-global-rounding-small);
  background: var(--background-color);
  color: var(--ac-global-text-color-900);
  outline: none;

  &[data-entering],
  &[data-exiting] {
    transform: var(--origin);
    opacity: 0;
  }

  .react-aria-OverlayArrow svg {
    display: block;
    fill: var(--background-color);
    stroke: var(--ac-global-border-color-light);
    stroke-width: 1px;
  }

  &[data-trigger="Select"] {
    min-width: var(--trigger-width);
  }

  &[data-placement="top"] {
    --origin: translateY(8px);

    &:has(.react-aria-OverlayArrow) {
      margin-bottom: 6px;
    }
  }

  &[data-placement="bottom"] {
    --origin: translateY(-8px);

    &:has(.react-aria-OverlayArrow) {
      margin-top: 4px;
    }

    .react-aria-OverlayArrow svg {
      transform: rotate(180deg);
    }
  }

  &[data-placement="right"] {
    --origin: translateX(-8px);

    &:has(.react-aria-OverlayArrow) {
      margin-left: 6px;
    }

    .react-aria-OverlayArrow svg {
      transform: rotate(90deg);
    }
  }

  &[data-placement="left"] {
    --origin: translateX(8px);

    &:has(.react-aria-OverlayArrow) {
      margin-right: 6px;
    }

    .react-aria-OverlayArrow svg {
      transform: rotate(-90deg);
    }
  }

  &[data-entering] {
    animation: ${rl} 200ms;
  }

  &[data-exiting] {
    animation: ${rl} 200ms reverse ease-in;
  }

  .react-aria-Dialog {
    outline: none;
  }

  & div[role="listbox"] {
    padding: var(--ac-global-dimension-size-25);
  }
`;function H0(n,a){return e(Nl,{...n,ref:a,className:V("ac-popover react-aria-Popover",n.className),css:B0})}const ue=p.forwardRef(H0),ol=Me`
  from {
    transform: translateX(100%);
  }
  to {
    transform: translateX(0);
  }
    `,la=Me`
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
  `,j0=Me`
  from {
    transform: scale(0.8);
  }
  to {
    transform: scale(1);
  }
  `,Z0=m`
  --modal-width: var(--ac-global-modal-width-M);

  &[data-size="S"] {
    --modal-width: var(--ac-global-modal-width-S);
  }

  &[data-size="M"] {
    --modal-width: var(--ac-global-modal-width-M);
  }

  &[data-size="L"] {
    --modal-width: var(--ac-global-modal-width-L);
  }

  &[data-size="fullscreen"] {
    --modal-width: var(--ac-global-modal-width-FULLSCREEN);
  }

  &[data-variant="slideover"] {
    --visual-viewport-height: 100vh;
    width: var(--modal-width);
    height: var(--visual-viewport-height);
    position: fixed;
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 100;
    top: 0;
    right: 0;
    left: auto;
    align-items: flex-start;
    justify-content: flex-end;

    &[data-entering] {
      animation: ${ol} 300ms;
    }

    &[data-exiting] {
      animation: ${ol} 300ms reverse ease-in;
    }

    .react-aria-Dialog {
      height: 100%;
      border-radius: 0;
      border-left-color: var(--ac-global-border-color-dark);
      border-top: none;
      border-bottom: none;
      border-right: none;
    }
  }

  &[data-variant="default"] {
    &[data-entering] {
      animation: ${la} 200ms;
    }

    &[data-exiting] {
      animation: ${la} 200ms reverse ease-in;
    }

    .react-aria-Dialog {
      position: fixed;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      z-index: 1001;
      // 90% gives a decent amount of padding around the dialog when it would
      // otherwise be cut off by the edges of the screen
      max-height: calc(100% - var(--ac-global-dimension-size-800));
      overflow: auto;
      // prevent bounce in safari when scrolling
      overscroll-behavior: contain;

      &[data-entering] {
        animation: ${j0} 300ms cubic-bezier(0.175, 0.885, 0.32, 1.275);
      }
    }
  }

  .react-aria-Dialog {
    box-shadow: 0 8px 20px rgba(0 0 0 / 0.1);
    width: var(--modal-width);
    border-radius: var(--ac-global-rounding-medium);
    background: var(--ac-global-background-color-dark);
    color: var(--ac-global-text-color-900);
    border: 1px solid var(--ac-global-border-color-light);
    outline: none;

    & .ac-DialogHeader {
      position: sticky;
      top: 0;
      background: var(--ac-global-background-color-dark);
      z-index: 1;
    }
  }
`;function U0(n,a){const{size:t="M",variant:l="default",...i}=n;return e(Bo,{...i,"data-size":t,"data-variant":l,ref:a,css:Z0})}const vn=p.forwardRef(U0),G0=m`
  position: fixed;
  inset: 0;
  background: rgba(0 0 0 / 0.5);
  z-index: 1000;

  &[data-entering] {
    // ensure overlay animation is longer than child animations
    animation: ${la} 300ms;
  }

  &[data-exiting] {
    // ensure overlay animation is longer than child animations
    animation: ${la} 300ms reverse ease-in;
  }
`;function Q0(n,a){return e(Ho,{...n,"data-testid":"modal-overlay",css:G0,className:V(n.className,"react-aria-ModalOverlay"),isDismissable:n.isDismissable??!0,ref:a})}const Cn=p.forwardRef(Q0),W0=n=>{const a=t=>({markdownDisplayMode:"text",setMarkdownDisplayMode:l=>{t({markdownDisplayMode:l})},traceStreamingEnabled:!0,setTraceStreamingEnabled:l=>{t({traceStreamingEnabled:l})},lastNTimeRangeKey:"7d",setLastNTimeRangeKey:l=>{t({lastNTimeRangeKey:l})},projectsAutoRefreshEnabled:!0,setProjectAutoRefreshEnabled:l=>{t({projectsAutoRefreshEnabled:l})},showMetricsInTraceTree:!0,setShowMetricsInTraceTree:l=>{t({showMetricsInTraceTree:l})},modelConfigByProvider:{},setModelConfigForProvider:({provider:l,modelConfig:i})=>{t(r=>({modelConfigByProvider:{...r.modelConfigByProvider,[l]:i}}))},playgroundStreamingEnabled:!0,setPlaygroundStreamingEnabled:l=>{t({playgroundStreamingEnabled:l})},isAnnotatingSpans:!0,setIsAnnotatingSpans:l=>{t({isAnnotatingSpans:l})},projectViewMode:"grid",setProjectViewMode:l=>{t({projectViewMode:l})},projectSortOrder:{column:"endTime",direction:"desc"},setProjectSortOrder:l=>{t({projectSortOrder:l})},isSideNavExpanded:!0,setIsSideNavExpanded:l=>{t({isSideNavExpanded:l})},...n});return wn()(ga(Bn(a),{name:"arize-phoenix-preferences"}))},Fi=p.createContext(null);function M8({children:n,...a}){const[t]=p.useState(()=>W0(a));return e(Fi.Provider,{value:t,children:n})}function Ge(n,a){const t=p.useContext(Fi);if(!t)throw new Error("Missing PreferencesContext.Provider in the tree");return gt(t,n,a)}const La=[{key:"15m",label:"Last 15 Min"},{key:"1h",label:"Last Hour"},{key:"12h",label:"Last 12 Hours"},{key:"1d",label:"Last Day"},{key:"7d",label:"Last 7 Days"},{key:"30d",label:"Last Month"}];La.reduce((n,a)=>({...n,[a.key]:a}),{});function nt(n){const a=Date.now();switch(n){case"15m":return{start:Wa(jo(a))};case"1h":return{start:Wa(qa(a,1))};case"12h":return{start:En(qa(a,12))};case"1d":return{start:En(Je(a,1))};case"7d":return{start:En(Je(a,7))};case"30d":return{start:En(Je(a,30))};default:P()}}function at(n){return La.some(a=>a.key===n)}function q0(n){return at(n)||n==="custom"}const Ei=p.createContext(null);function Di(){return rn.useContext(Ei)}function X0(){const n=Di();if(n===null)throw new Error("useTimeRange must be used within a TimeRangeContextProvider");return n}function F8({children:n}){const a=Ge(o=>o.lastNTimeRangeKey),t=Ge(o=>o.setLastNTimeRangeKey),[l,i]=p.useState(()=>at(a)?{timeRangeKey:a,...nt(a)}:{timeRangeKey:"7d",...nt("7d")}),r=p.useCallback(o=>{i(o),at(o.timeRangeKey)&&t(o.timeRangeKey)},[t]);return e(Ei.Provider,{value:{timeRange:l,setTimeRange:r},children:n})}const en=Ie("%x %H:%M:%S %p");Ie("%H:%M %p");const Y0=Ie("%x %H:%M %p"),J0=n=>n.start&&n.end?`${en(n.start)} - ${en(n.end)}`:n.start?`From ${en(n.start)}`:n.end?`Until ${en(n.end)}`:"All Time";function E8(n){return new Intl.DateTimeFormat(n,{day:"2-digit",month:"2-digit",year:"numeric"}).formatToParts(new Date).map(l=>{switch(l.type){case"day":return"dd";case"month":return"mm";case"year":return"yyyy";case"literal":return l.value;default:return""}}).join("")}const ed=m`
  width: 130px;
`;function nd({timeRangeKey:n,start:a,end:t}){if(n==="custom")return J0({start:a,end:t});const l=La.find(i=>i.key===n);return l?l.label:"invalid"}function ad(n){const{value:a,isDisabled:t,onChange:l,size:i="S"}=n,{timeRangeKey:r,start:o,end:c}=a;return s(_e,{children:[s(z,{size:i,leadingVisual:e(T,{svg:e(wc,{})}),isDisabled:t,children:[nd(a),e(Ae,{})]}),e(ue,{placement:"bottom end",children:e(Zl,{children:({close:d})=>s(U,{children:[e(It,{}),s(S,{direction:"row",children:[e(td,{visible:r==="custom",children:r==="custom"&&s(S,{direction:"column",gap:"size-100",height:"100%",children:[e(ne,{level:2,weight:"heavy",children:"Time Range"}),e(ud,{initialValue:{start:o,end:c},onSubmit:u=>{l&&l({timeRangeKey:"custom",...u}),d()}})]})}),s(we,{"aria-label":"time range preset selection",selectionMode:"single",autoFocus:!0,selectedKeys:[r],css:ed,onSelectionChange:u=>{if(u==="all"){d();return}const g=u.keys().next().value;if(q0(g))if(g!=="custom"){l({timeRangeKey:g,...nt(g)}),d();return}else l({timeRangeKey:g,start:o,end:c})},children:[La.map(({key:u,label:g})=>e(bn,{id:u,children:g},u)),e(bn,{id:"custom",children:"Custom"},"custom")]})]})]})})})]})}function td({children:n,visible:a}){return e("div",{css:m`
        display: ${a?"block":"none"};
      `,children:e(w,{borderEndWidth:"thin",borderColor:"light",padding:"size-200",height:"100%",children:n})})}function D8({size:n="S"}){const{timeRange:a,setTimeRange:t}=X0(),l=p.useCallback(i=>{p.startTransition(()=>{t(i)})},[t]);return e(ad,{value:a,onChange:l,size:n})}const ld=m`
  --date-field-vertical-padding: 6px;
  --date-field-horizontal-padding: 8px;
  color: var(--ac-global-text-color-900);

  &[data-size="S"] .react-aria-DateInput {
    height: var(--ac-global-input-height-s);
  }

  &[data-size="M"] .react-aria-DateInput {
    height: var(--ac-global-input-height-m);
  }

  .react-aria-DateInput {
    display: flex;
    padding: var(--date-field-vertical-padding)
      var(--date-field-horizontal-padding);
    border: var(--ac-global-border-size-thin) solid
      var(--ac-global-input-field-border-color);
    border-radius: var(--ac-global-rounding-small);
    background-color: var(--ac-global-input-field-background-color);
    width: fit-content;
    box-sizing: border-box;
    min-width: 150px;
    white-space: nowrap;
    forced-color-adjust: none;

    &[data-focus-within] {
      outline: 1px solid var(--ac-global-color-primary);
      outline-offset: -1px;
    }

    &[data-invalid] {
      border-color: var(--ac-global-color-danger);
    }
  }

  .react-aria-DateSegment {
    padding: 0 2px;
    font-variant-numeric: tabular-nums;
    text-align: end;
    color: var(--ac-global-text-color-900);

    &[data-type="literal"] {
      padding: 0;
    }

    &[data-placeholder] {
      color: var(--ac-text-color-placeholder);
      font-style: italic;
    }

    &:focus {
      color: var(--ac-highlight-foreground);
      background: var(--ac-highlight-background);
      outline: none;
      border-radius: var(--ac-global-rounding-small);
      caret-color: transparent;
    }
  }
`;function id(n,a){const{css:t,...l}=n;return e(Zo,{css:m(Le,ld,t),...l,"data-size":"S",ref:a})}const tt=p.forwardRef(id),rd=m`
  --date-field-vertical-padding: 6px;
  --date-field-horizontal-padding: 8px;
  color: var(--ac-global-text-color-900);

  .react-aria-DateInput {
    display: flex;
    padding: var(--date-field-vertical-padding)
      var(--date-field-horizontal-padding);
    border: var(--ac-global-border-size-thin) solid
      var(--ac-global-input-field-border-color);
    border-radius: var(--ac-global-rounding-small);
    background-color: var(--ac-global-input-field-background-color);
    width: fit-content;
    min-width: 150px;
    white-space: nowrap;
    forced-color-adjust: none;

    &[data-focus-within] {
      outline: 1px solid var(--ac-global-color-primary);
      outline-offset: -1px;
    }
  }

  .react-aria-DateSegment {
    padding: 0 2px;
    font-variant-numeric: tabular-nums;
    text-align: end;
    color: var(--ac-global-text-color-900);

    &[data-type="literal"] {
      padding: 0;
    }

    &[data-placeholder] {
      color: var(--ac-text-color-placeholder);
      font-style: italic;
    }

    &:focus {
      color: var(--ac-highlight-foreground);
      background: var(--ac-highlight-background);
      outline: none;
      border-radius: var(--ac-global-rounding-small);
      caret-color: transparent;
    }
  }
`;function od(n,a){return e(Uo,{css:m(Le,rd),...n,ref:a})}p.forwardRef(od);const sd=m`
  display: flex;
  flex-direction: column;
  gap: var(--ac-global-dimension-size-200);
`,sl=m`
  display: flex;
  gap: var(--ac-global-dimension-size-100);
  align-items: start;
  justify-content: end;
  /* Move the button down to align */
  button {
    margin-top: 26px;
  }
`,cd=m`
  width: 100%;
  display: flex;
  justify-content: flex-end;
  gap: var(--ac-global-dimension-size-100);
`,cl=m`
  width: 100%;
  .react-aria-DateInput {
    width: 100%;
    // Eliminate the re-sizing of the DateField as you type
    min-width: 200px;
  }
`;function dd(n){return{startDate:n.start?Wt(n.start.toISOString()):null,endDate:n.end?Wt(n.end.toISOString()):null}}function ud(n){const{initialValue:a,onSubmit:t}=n,{control:l,handleSubmit:i,formState:{isValid:r},resetField:o,setError:c,clearErrors:d}=Re({defaultValues:dd(a||{})}),u=p.useCallback(()=>{o("startDate",{defaultValue:null})},[o]),g=p.useCallback(()=>{o("endDate",{defaultValue:null})},[o]),h=p.useCallback(f=>{d();const{startDate:b,endDate:y}=f,v=b?b.toDate(Xa()):null,k=y?y.toDate(Xa()):null;if(v&&k&&v>k){c("endDate",{message:"End must be after the start date"});return}t({start:v,end:k})},[t,c,d]);return s(on,{css:sd,"data-testid":"time-range-form",onSubmit:i(h),children:[s("div",{"data-testid":"start-time",css:sl,children:[e($,{name:"startDate",control:l,render:({field:{onChange:f,onBlur:b,value:y},fieldState:{invalid:v}})=>s(tt,{isInvalid:v,onChange:f,onBlur:b,value:y,granularity:"second",hideTimeZone:!0,css:cl,children:[e(K,{children:"Start Date"}),e(Ya,{children:k=>e(Ja,{segment:k})})]})}),e(z,{size:"S",excludeFromTabOrder:!0,onPress:u,"aria-label":"Clear start date and time",leadingVisual:e(T,{svg:e(il,{})})})]}),s("div",{"data-testid":"end-time",css:sl,children:[e($,{name:"endDate",control:l,render:({field:{onChange:f,onBlur:b,value:y},fieldState:{invalid:v,error:k}})=>s(tt,{isInvalid:v,onChange:f,onBlur:b,value:y,granularity:"second",hideTimeZone:!0,css:cl,children:[e(K,{children:"End Date"}),e(Ya,{children:L=>e(Ja,{segment:L})}),k?e(W,{children:k.message}):null]})}),e(z,{size:"S",excludeFromTabOrder:!0,onPress:g,"aria-label":"Clear end date and time",leadingVisual:e(T,{svg:e(il,{})})})]}),e("div",{"data-testid":"controls",css:cd,children:e(z,{isDisabled:!r,size:"S",type:"submit",variant:"primary",children:"Apply"})})]})}const gd=m(`
  // fixes esoteric overflow bug with VisuallyHidden, which is used by Radio
  // If position is not set to relative, the radio group will explode the parent layout
  // This will impact any other react aria component that uses VisuallyHidden
  // https://github.com/adobe/react-spectrum/issues/5094
  position: relative;
  display: flex;
  flex-direction: row;
  align-items: center;
  width: fit-content;
  gap: var(--ac-global-dimension-size-200);
  font-size: var(--ac-global-dimension-static-font-size-100);

  & > .ac-radio:not(:first-of-type) {
    border-left: none;
  }

  & > .ac-radio:first-of-type {
    border-radius: var(--ac-global-rounding-small) 0 0 var(--ac-global-rounding-small);
  }

  & > .ac-radio:last-of-type {
    border-radius: 0 var(--ac-global-rounding-small) var(--ac-global-rounding-small) 0;
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
    .ac-radio {
      padding: var(--ac-global-dimension-size-25) var(--ac-global-dimension-size-100);
    }
  }

  &[data-size="L"] {
    .ac-radio {
      padding: var(--ac-global-dimension-size-100) var(--ac-global-dimension-size-150);
    }
  }

  &[data-disabled] {
    opacity: 0.5;
  }

  &[data-readonly] {
    .ac-radio:before {
      opacity: 0.5;
    }
  }

  &:has(.ac-radio[data-focus-visible]) {
    border-radius: var(--ac-global-rounding-small);
    outline: 1px solid var(--ac-global-input-field-border-color-active);
    // display an outline offset around the radio group, accounting for the outline offset of the inner radios
    outline-offset: var(--ac-global-dimension-size-100);
  }
`),_8=({size:n,css:a,className:t,direction:l="row",...i})=>e(Ul,{"data-size":n,"data-direction":l,className:V("ac-radio-group",t),css:m(Le,gd,a),...i}),md=m(`
  display: flex;
  align-items: center;
  gap: var(--ac-global-dimension-size-50);
  font-size: 14px;
  color: var(--ac-global-text-color-900);
  forced-color-adjust: none;

  &:before {
    content: '';
    display: block;
    width: 1.286rem;
    height: 1.286rem;
    box-sizing: border-box;
    border: 0.143rem solid var(--ac-global-input-field-border-color);
    background: var(--ac-global-input-field-background-color);
    border-radius: 1.286rem;
    transition: all 200ms;
  }

  &[data-pressed]:before {
    border-color: var(--ac-global-input-field-border-color-active);
  }

  &[data-selected] {
    &:before {
      border-color: var(--ac-global-button-primary-background-color);
      border-width: 0.429rem;
    }

    &[data-pressed]:before {
      border-color: var(--ac-global-button-primary-background-color-active);
    }
  }

  &[data-focus-visible]:before {
    outline: 2px solid var(--ac-global-input-field-border-color-active);
    outline-offset: 2px;
  }

  &[data-disabled] {
    opacity: var(--ac-global-opacity-disabled);
  }
`),K8=({className:n,css:a,...t})=>e(Gl,{className:V("ac-radio",n),css:m(md,a),...t}),pd=m(Ca,`
    text-wrap: nowrap;
    &[data-selected="true"] {
      background-color: var(--ac-global-button-primary-background-color);
      --button-border-color: var(--ac-global-button-primary-border-color);
      color: var(--ac-global-button-primary-foreground-color);
      &:hover:not([data-disabled]) {
        background-color: var(--ac-global-button-primary-background-color-hover);
      }
    }
    &[data-hovered]:not([data-disabled]):not([data-selected="true"]) {
      background-color: var(--ac-global-input-field-border-color-hover);
    }
    &[data-focus-visible] {
      outline: 1px solid var(--ac-global-input-field-border-color-active);
      outline-offset: -2px;
    }
`),Ce=({className:n,css:a,...t})=>{const{leadingVisual:l,trailingVisual:i,size:r,children:o,...c}=t,d=At(),u=r??d,g=p.useCallback(h=>s(U,{children:[l,typeof o=="function"?o(h):o,i]}),[l,i,o]);return e(Go,{css:m(pd,a),"data-size":u,"data-childless":!o,className:V("ac-toggle-button",n),...c,children:g})},hd=m(`
  position: relative;
  display: flex;
  flex-direction: row;
  align-items: center;
  width: fit-content;
  & > button {
    border-radius: 0;
    z-index: 1;

    &[data-disabled] {
      z-index: 0;
    }

    &[data-selected],
    &[data-focus-visible] {
      z-index: 2;
    }
  }

  & > .ac-toggle-button:not(:first-of-type):not([data-selected="true"]) {
    border-left: none;
  }
    
  & > .ac-toggle-button[data-selected="true"]:not(:first-of-type) {
    margin-left: -1px;
  }

  & > .ac-toggle-button:first-of-type {
    border-radius: var(--ac-global-rounding-small) 0 0 var(--ac-global-rounding-small);
  }

  & > .ac-toggle-button:last-of-type {
    border-radius: 0 var(--ac-global-rounding-small) var(--ac-global-rounding-small) 0;
  }

  &:has(.ac-toggle-button[data-focus-visible]) {
    border-radius: var(--ac-global-rounding-small);
    outline: 1px solid var(--ac-global-input-field-border-color-active);
    outline-offset: 1px;
  }
`),Gn=({size:n="M",css:a,className:t,selectionMode:l="single",...i})=>e(ka,{size:n,children:e(Qo,{"data-size":n,className:V("ac-toggle-button-group",t),css:m(hd,a),selectionMode:l,...i})}),fd=m`
  display: flex;
  flex-direction: column;
  max-height: inherit;
  overflow: auto;
  forced-color-adjust: none;
  outline: none;
  box-sizing: border-box;

  &[data-focus-visible] {
    outline: 2px solid var(--focus-ring-color);
    outline-offset: -1px;
  }

  &[data-empty] {
    align-items: center;
    justify-content: center;
    font-style: italic;
    color: var(--ac-global-text-color-700);
  }

  .react-aria-ListBoxItem {
    margin: var(--ac-global-dimension-size-25);
    padding: var(--ac-global-dimension-size-100)
      var(--ac-global-dimension-size-150);
    border-radius: var(--ac-global-rounding-small);
    outline: none;
    cursor: default;
    color: var(--ac-global-text-color-900);
    font-size: var(--ac-global-font-size-s);
    line-height: var(--ac-global-line-height-s);

    position: relative;
    display: flex;
    flex-direction: column;

    &[data-focus-visible] {
      outline: 2px solid var(--ac-focus-ring-color);
      outline-offset: -2px;
    }

    &[data-selected] {
      background: var(--ac-highlight-background);
      color: var(--ac-highlight-foreground);

      &[data-focus-visible] {
        outline-color: var(--ac-highlight-foreground);
        outline-offset: -4px;
      }
    }
    &[data-hovered],
    &[data-active] {
      background: var(--ac-global-background-color-light-hover);
    }
  }
`;function bd(n,a){const{css:t,...l}=n,i=m(fd,t);return e(Ol,{css:i,ref:a,...l})}const we=p.forwardRef(bd),yd=m`
  display: inline-flex;
  align-items: center;
  gap: var(--ac-global-dimension-static-size-100);
  font-size: var(--ac-global-dimension-static-font-size-75);
  line-height: var(--ac-global-line-height-s);
  padding: 0 var(--ac-global-dimension-static-size-100);
  border-radius: var(--ac-global-rounding-large);
  border: 1px solid
    lch(from var(--ac-internal-token-color) calc((l) * infinity) c h / 0.3);
  color: lch(from var(--ac-internal-token-color) calc((50 - l) * infinity) 0 0);
  user-select: none;

  &[data-size="S"] {
    height: var(--ac-global-dimension-static-size-200);
  }

  &[data-size="M"] {
    height: var(--ac-global-dimension-static-size-250);
  }

  &[data-size="L"] {
    height: var(--ac-global-dimension-static-size-300);
  }

  &[data-disabled] {
    opacity: 0.5;
    cursor: not-allowed;
  }

  &[data-theme="light"] {
    background: var(--ac-internal-token-color);
    border-color: var(--ac-internal-token-color);
  }

  &[data-theme="dark"] {
    // generate a new dark token bg color from the input color
    --scoped-token-dark-bg: lch(
      from var(--ac-internal-token-color) l c h / calc(alpha - 0.8)
    );
    background: var(--scoped-token-dark-bg);
    // generate a new dark token text color from the input color
    color: lch(from var(--scoped-token-dark-bg) calc((l) * infinity) c h / 1);
  }

  &[data-interactive]:not([data-disabled]) {
    cursor: pointer;

    > button {
      &:focus-visible {
        outline: 2px solid var(--ac-focus-ring-color);
        border-radius: var(--ac-global-rounding-small);
      }
    }
  }

  &[data-removable] {
    padding-right: var(--ac-global-dimension-static-size-25);
  }

  > button {
    all: unset;
    cursor: pointer;
    display: flex;
    align-items: center;

    &[disabled] {
      cursor: not-allowed;
    }
  }
`;function vd({children:n,size:a="M"}){return e("span",{"data-size":a,css:m`
        display: flex;
        align-items: center;
        justify-content: center;
        width: var(--ac-global-dimension-static-size-200);
        height: var(--ac-global-dimension-static-size-200);

        &[data-size="M"] {
          margin-right: var(--ac-global-dimension-static-size-50);
        }

        &[data-size="L"] {
          margin-right: var(--ac-global-dimension-static-size-100);
        }
      `,children:n})}function Cd({children:n,isDisabled:a,css:t,color:l="var(--ac-global-color-grey-300)",onPress:i,onRemove:r,size:o="M",style:c,leadingVisual:d,...u},g){const{theme:h}=le(),f=d&&o!=="S"?e(vd,{size:o,children:d}):null,b=r?e("button",{onClick:()=>{r()},disabled:a,"aria-label":"Remove",children:e(T,{svg:e(ba,{})})}):null,y=()=>i&&r?s(U,{children:[s("button",{onClick:()=>{i()},disabled:a,children:[f,n]}),b]}):i?s("button",{onClick:()=>{i()},disabled:a,children:[f,n]}):r?s(U,{children:[s("span",{children:[f,n]}),b]}):s(U,{children:[f,n]});return e("div",{ref:g,css:m(yd,t),style:{"--ac-internal-token-color":l,...c},"data-theme":h,"data-size":o,...i&&{"data-interactive":!0},...r&&{"data-removable":!0},...a&&{"data-disabled":!0},...u,children:y()})}const je=p.forwardRef(Cd),kd=m`
  --ac-slider-track-height: var(--ac-global-dimension-size-30);
  --ac-slider-handle-width: var(--ac-global-dimension-size-250);
  --ac-slider-handle-height: var(--ac-global-dimension-size-250);
  --ac-slider-handle-halo-width: var(--ac-global-dimension-size-350);
  --ac-slider-handle-border-radius: var(--ac-global-dimension-size-250);
  --ac-slider-handle-background-color: white;
  --ac-slider-track-height: var(--ac-global-dimension-size-100);
  --ac-slider-filled-color: var(--ac-global-color-primary);

  display: grid;
  grid-template-areas:
    "label output"
    "track track";
  gap: var(--ac-global-dimension-size-100);
  grid-template-columns: 1fr auto;
  width: var(
    --ac-alias-single-line-width,
    var(--ac-global-dimension-size-2400)
  );
  color: var(--text-color);

  .ac-slider-label {
    grid-area: label;
  }

  .ac-slider-output {
    grid-area: output;
    min-height: var(--ac-global-dimension-size-350);
  }

  .ac-slider-track {
    grid-area: track;
    position: relative;
    height: var(--ac-slider-track-height, var(--ac-global-border-size-thick));
    width: 100%;

    /* Background track line */
    &:before {
      content: "";
      display: block;
      position: absolute;
      background: var(--ac-global-color-grey-300);
      height: 100%;
      border-radius: var(--ac-global-border-size-thicker);
    }

    /* Filled track line */
    &:after {
      content: "";
      display: block;
      position: absolute;
      background: var(--ac-slider-filled-color);
      height: 100%;
      border-radius: var(--ac-global-border-size-thicker);
    }
  }

  .ac-slider-thumb {
    width: var(--ac-slider-handle-width, var(--ac-global-dimension-size-200));
    height: var(--ac-slider-handle-height, var(--ac-global-dimension-size-200));
    border-radius: var(
      --ac-slider-handle-border-radius,
      var(--ac-global-rounding-medium)
    );
    background-color: var(--ac-slider-handle-background-color);
    border: 2px solid var(--background-color);
    box-shadow: 0 4px 4px 0 rgba(0, 0, 0, 0.25);
    forced-color-adjust: none;
    transition: border-width
      var(
        --ac-slider-animation-duration,
        var(--ac-global-animation-duration-100)
      )
      ease-in-out;
    position: relative;

    /* show a halo when hovering over the thumb */
    &:hover::after {
      content: "";
      position: absolute;
      background: white;
      opacity: 0.5;
      display: block;
      width: var(--ac-slider-handle-halo-width);
      height: var(--ac-slider-handle-halo-width);
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      border-radius: var(
        --ac-slider-handle-border-radius,
        var(--ac-global-rounding-medium)
      );
      z-index: -1;
    }

    &[data-dragging] {
      background: white;
    }

    &[data-focus-visible] {
      outline: 2px solid var(--ac-focus-ring-color);
    }
  }

  &[data-orientation="horizontal"] {
    flex-direction: column;
    width: 100%;
    align-items: baseline;

    .ac-slider-number-field {
      .react-aria-Input {
        min-width: var(--ac-global-dimension-size-800);
        width: var(--ac-global-dimension-size-800);
        padding: 0 var(--ac-global-dimension-size-100);
        height: var(--ac-global-dimension-size-350);
        text-align: right;
        margin-bottom: var(--ac-global-dimension-size-100);
      }
    }

    .ac-slider-track {
      height: var(--ac-slider-track-height, var(--ac-global-border-size-thick));
      width: calc(100% - var(--ac-slider-handle-width));
      left: calc(var(--ac-slider-handle-width) / 2);

      /* background track line */
      &:before {
        left: calc(var(--ac-slider-handle-width) / -2);
        width: calc(100% + var(--ac-slider-handle-width));
        top: 50%;
        transform: translateY(-50%);
      }

      /* filled track line */
      &:after {
        left: calc(var(--slider-start) - var(--ac-slider-handle-width) / 2);
        width: calc(
          var(--slider-end) - var(--slider-start) +
            var(--ac-slider-handle-width)
        );
        top: 50%;
        transform: translateY(-50%);
        z-index: 1;
      }
    }

    .ac-slider-thumb {
      top: 50%;
      z-index: 2;
    }
  }
`;function Ld({label:n,thumbLabels:a,children:t,css:l,...i},r){return s(Yo,{css:m(kd,l),...i,ref:r,children:[n&&e(K,{className:"ac-slider-label",children:n}),e(Wo,{className:"ac-slider-output",children:typeof t>"u"?e(wd,{}):t}),e(Xo,{className:"ac-slider-track",style:({state:o})=>o.values.length===1?{"--slider-start":"0%","--slider-end":`${o.getThumbPercent(0)*100}%`}:{"--slider-start":`${o.getThumbPercent(0)*100}%`,"--slider-end":`${o.getThumbPercent(1)*100}%`},children:({state:o})=>e(U,{children:o.values.map((c,d)=>e(qo,{index:d,"aria-label":a==null?void 0:a[d],className:"ac-slider-thumb"},d))})})]})}const P8=p.forwardRef(Ld);function V8({onChange:n,...a}){const t=p.useContext(Ql),{step:l,getThumbMinValue:i,getThumbMaxValue:r,values:o,setThumbValue:c}=t,d="defaultValue"in a,u=o[0]===i(0),h=d&&u?a.defaultValue:o[0],f=Jo(e1);return e(Mi,{className:"ac-slider-number-field","aria-labelledby":f.id,value:h,onChange:b=>{n?n(b):typeof b=="number"&&c(0,b)},step:l,maxValue:r(0),minValue:i(0),...a,children:e(j,{})})}function wd(){const n=p.useContext(Ql);return e(C,{children:n.values.map(a=>a.toString()).join(" – ")})}const Sd=m`
  display: inline-block;
  padding: 0 var(--ac-global-dimension-size-50);
  border-radius: var(--ac-global-rounding-large);
  border: 1px solid var(--ac-global-color-grey-300);
  min-width: var(--ac-global-dimension-size-150);
  background-color: var(--ac-global-background-color-light);
  font-size: var(--ac-global-font-size-xs);
  line-height: var(--ac-global-line-height-xs);
  text-align: center;
  color: var(--ac-global-text-color-900);
  &[data-variant="danger"] {
    background-color: var(--ac-global-background-color-danger);
  }
`;function xd(n){const{children:a,variant:t="default"}=n;return e("span",{css:Sd,"data-variant":t,className:"ac-counter",children:a})}const Td=m`
  display: flex;
  color: var(--ac-global-text-color-900);
  --ac-tab-border-color: var(--ac-global-border-color-default);

  flex-direction: column;
  height: 100%;

  &[data-orientation="horizontal"] {
    flex: 1 1 auto;
    overflow: hidden;
    box-sizing: border-box;
    .react-aria-TabPanel[data-padded="true"] {
      padding-top: var(--ac-global-dimension-static-size-200);
    }
  }

  &[data-orientation="vertical"] {
    flex-direction: row;
    .react-aria-TabPanel[data-padded="true"] {
      padding-left: var(--ac-global-dimension-static-size-200);
    }
  }
`;function Ad({children:n,css:a,className:t,orientation:l="horizontal",...i}){return e(n1,{css:m(Td,a),className:V("react-aria-Tabs",t),orientation:l,...i,children:n})}const Id=m`
  display: flex;

  &[data-orientation="vertical"] {
    flex-direction: column;
    border-inline-end: 1px solid var(--ac-tab-border-color);

    .react-aria-Tab {
      border-inline-end: 3px solid var(--ac-tab-border-color, transparent);
    }
  }

  &[data-orientation="horizontal"] {
    border-bottom: 1px solid var(--ac-tab-border-color);

    .react-aria-Tab {
      border-bottom: 3px solid var(--ac-tab-border-color);
    }
  }
`;function zd({children:n,css:a,className:t,...l}){return e(a1,{css:m(Id,a),className:V("react-aria-TabList",t),...l,children:n})}const Md=m`
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
`;function lt({css:n,className:a,padded:t,...l}){return e(l1,{css:m(Md,n),className:V("react-aria-TabPanel",a),"data-padded":t,...l})}function R8({children:n,id:a,...t}){return e(lt,{id:a,...t,children:({state:{selectedKey:l}})=>l===a?n:null})}const Fd=m`
  padding: var(--ac-global-dimension-static-size-100)
    var(--ac-global-dimension-static-size-200);
  cursor: default;
  outline: none;
  position: relative;
  color: var(--ac-global-text-color-700);
  transition: color 200ms;
  --ac-tab-border-color: transparent;
  forced-color-adjust: none;
  font-weight: 600;
  line-height: var(--ac-global-line-height-s);
  font-size: var(--ac-global-font-size-s);

  &[data-hovered],
  &[data-focused] {
    --ac-tab-border-color: var(--ac-global-color-primary-300);
  }

  &[data-selected] {
    --ac-tab-border-color: var(--ac-global-color-primary);
    color: var(--ac-global-text-color-900);
  }

  &[data-disabled] {
    color: var(--ac-global-text-color-300);
    &[data-selected] {
      --ac-tab-border-color: var(--ac-global-text-color-300);
    }
  }

  &[data-focus-visible]:after {
    content: "";
    position: absolute;
    inset: var(--ac-global-dimension-size-50);
    border-radius: var(--ac-global-rounding-small);
    border: 2px solid var(--ac-focus-ring-color);
  }
`;function dl({children:n,css:a,className:t,...l}){return e(t1,{css:m(Fd,a),className:V("react-aria-Tab",t),...l,children:n})}const re=({message:n,size:a,className:t})=>s("div",{className:t,css:m`
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        width: 100%;
        height: 100%;
        gap: var(--ac-global-dimension-static-size-100);
      `,children:[e(Ki,{isIndeterminate:!0,"aria-label":"loading",size:a}),n!=null?e(C,{children:n}):null]}),Ed=Me`
  0% {
    opacity: 1;
  }
  50% {
    opacity: 0.4;
  }
  100% {
    opacity: 1;
  }
`,Dd=Me`
  0% {
    transform: translateX(-100%);
  }
  50% {
    transform: translateX(100%);
  }
  100% {
    transform: translateX(100%);
  }
`,_d=m`
  display: block;
  background-color: var(--ac-global-color-grey-200);
`,Kd=m`
  animation: ${Ed} 2s ease-in-out 0.5s infinite;
`,Pd=m`
  position: relative;
  overflow: hidden;
  /* Fix bug in Safari https://bugs.webkit.org/show_bug.cgi?id=68196 */
  -webkit-mask-image: -webkit-radial-gradient(white, black);

  &::after {
    animation: ${Dd} 2s linear 0.5s infinite;
    background: linear-gradient(
      90deg,
      transparent,
      var(--ac-global-color-grey-300),
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
`,Vd=n=>{if(typeof n=="number")return`${n}px`;if(typeof n=="string")switch(n){case"none":return"0";case"XS":return"var(--ac-global-rounding-xsmall)";case"S":return"var(--ac-global-rounding-small)";case"M":return"var(--ac-global-rounding-medium)";case"L":return"var(--ac-global-rounding-large)";case"circle":return"50%";default:return n}return"var(--ac-global-rounding-medium)"},fn=p.forwardRef(({width:n="100%",height:a="1.2em",borderRadius:t="S",animation:l="pulse",className:i,...r},o)=>{const c=typeof n=="number"?`${n}px`:n,d=typeof a=="number"?`${a}px`:a,u=Vd(t);return e("span",{ref:o,className:V(i,"ac-skeleton"),css:[_d,l==="pulse"&&Kd,l==="wave"&&Pd,m`
            width: ${c};
            height: ${d};
            border-radius: ${u};
          `],...r})});fn.displayName="Skeleton";const O8=n=>s(S,{direction:"column",gap:"size-100",width:"100%",...n,children:[e(fn,{height:100,borderRadius:8,animation:"wave"}),e(fn,{height:24,width:"80%",animation:"wave"}),e(fn,{height:16,width:"60%",animation:"wave"})]}),Rd=m`
  button {
    display: flex;
    align-items: center;
    justify-content: space-between;
    min-width: 200px;
    width: 100%;

    &[data-pressed],
    &:hover {
      --button-border-color: var(--ac-global-input-field-border-color-active);
    }
  }

  button[data-size="S"][data-childless="false"] {
    padding-right: var(--ac-global-dimension-size-50);
  }

  button[data-size="M"][data-childless="false"] {
    padding-right: var(--ac-global-dimension-size-100);
  }

  &[data-invalid="true"] button {
    border-color: var(--ac-global-color-danger);
  }

  .react-aria-SelectValue {
    &[data-placeholder] {
      font-style: italic;
      color: var(--ac-text-color-placeholder);
    }
  }
`;function Od(n,a){const{size:t="M",...l}=n;return e(ka,{size:t,children:e(i1,{"data-size":t,className:"ac-select",ref:a,css:m(Le,Rd),...l})})}const Ne=p.forwardRef(Od),ee=p.forwardRef((n,a)=>{const{children:t,...l}=n;return e(bn,{...l,ref:a,children:({isSelected:i})=>s(S,{direction:"row",justifyContent:"space-between",alignItems:"center",children:[e("span",{children:t}),i&&e(T,{svg:e(Li,{})})]})})});ee.displayName="SelectItem";const Nd=m`
  max-width: 100%;
  height: auto;
`,N8=({src:n,width:a,height:t,controls:l=!0,autoPlay:i=!1,loop:r=!1,muted:o=!1,poster:c,preload:d="none",className:u})=>e("video",{css:Nd,src:n,width:a,height:t,controls:l,autoPlay:i,loop:r,muted:o,poster:c,className:u,preload:d,children:"Your browser does not support the video tag."}),be=p.forwardRef(({children:n,...a},t)=>e(Zl,{"data-testid":"dialog",...a,className:V(a.className,"react-aria-Dialog"),ref:t,children:n}));be.displayName="Dialog";const Ke=({children:n,...a})=>e(S,{direction:"column",height:"100%","data-testid":"dialog-content",...a,className:V(a.className,"react-aria-DialogContent"),children:n}),$d=m`
  padding: var(--ac-global-dimension-size-100)
    var(--ac-global-dimension-size-200);
  border-bottom: var(--ac-global-border-size-thin) solid
    var(--ac-global-border-color-dark);
  flex-shrink: 0;
`,Pe=({children:n,...a})=>e("div",{...a,css:$d,className:V(a.className,"ac-DialogHeader"),children:e(S,{width:"100%",justifyContent:"space-between",alignItems:"center",children:n})}),Ve=({children:n,...a})=>e(ne,{level:2,"data-testid":"dialog-title",slot:"title",...a,className:V(a.className,"ac-DialogTitle"),children:n}),ln=({children:n,...a})=>e(S,{gap:"size-100",alignItems:"center","data-testid":"dialog-title-extra",...a,className:V(a.className,"ac-DialogTitleExtra"),children:n}),Qe=({children:n,close:a,onPress:t,...l})=>e(z,{size:"S","data-testid":"dialog-close-button",leadingVisual:e(T,{svg:e(ba,{})}),onPress:i=>{a==null||a(),t==null||t(i)},type:"button",slot:"close",...l,className:V(l.className,"ac-DialogCloseButton"),children:n}),Bd=m`
  position: fixed;
  bottom: 24px;
  right: 24px;
  display: flex;
  flex-direction: column-reverse;
  gap: 8px;
  border-radius: 8px;
  outline: none;
`,Hd=m`
  display: flex;
  flex-direction: column;
  gap: var(--ac-global-dimension-static-size-100);
  padding: var(--ac-global-dimension-static-size-100)
    var(--ac-global-dimension-static-size-100);
  border-radius: 8px;
  outline: none;
  width: 400px;
  position: relative;
  --toast-border: 1px solid var(--ac-global-border-color-default);
  --toast-background-color: var(--ac-global-background-color-dark);
  --toast-color: var(--ac-global-static-color-900);
  &[data-theme="light"] {
    --toast-border: 1px solid
      lch(from var(--ac-internal-token-color) calc((50 - l) * infinity) 0 0);
    --toast-background-color: var(--ac-internal-token-color);
    --toast-color: lch(
      from var(--ac-internal-token-color) calc((50 - l) * infinity) 0 0
    );
  }
  &[data-theme="dark"] {
    // generate a new dark token bg color from the input color
    --scoped-token-dark-bg: lch(
      from var(--ac-internal-token-color) l c h / calc(alpha - 0.8)
    );
    --toast-border: 1px solid
      lch(from var(--ac-internal-token-color) calc((l) * infinity) c h / 0.3);
    --toast-background-color: var(--scoped-token-dark-bg);
    // generate a new dark token text color from the input color
    --toast-color: lch(
      from var(--scoped-token-dark-bg) calc((l) * infinity) c h / 1
    );
    // because the background may render with transparency, add a blur to improve
    // text readability
    backdrop-filter: blur(4px);
  }
  background: var(--toast-background-color);
  background-color: var(--toast-background-color);
  border: var(--toast-border);
  color: var(--toast-color);

  &[data-focus-visible] {
    outline: 2px solid slateblue;
    outline-offset: 2px;
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
      gap: var(--ac-global-dimension-static-size-50);
    }

    [slot="description"] {
      color: var(--toast-color);
    }
  }

  .react-aria-Button[slot="close"] {
    flex: 0 0 auto;
    background: none;
    border: none;
    appearance: none;
    border-radius: 50%;
    height: 18px;
    width: 18px;
    border: none;
    color: var(--toast-color);
    padding: 0;
    outline: none;

    &[data-focus-visible] {
      border: 1px solid var(--ac-global-input-field-border-color-active);
      background: var(--toast-background-color);
    }

    &[data-hovered] {
      background: var(--toast-background-color);
    }

    &[data-pressed] {
      background: var(--toast-background-color);
    }
  }
`,jd=({queue:n})=>e(r1,{queue:n,css:Bd,className:"react-aria-ToastRegion",children:({toast:a})=>e(Ud,{toast:a,queue:n})}),Zd=n=>{switch(n){case"success":return"var(--ac-global-color-success)";case"error":return"var(--ac-global-color-danger)";default:return"var(--ac-global-background-color-dark)"}},Ud=({toast:n,queue:a})=>{const{theme:t}=le();return s(s1,{toast:n,css:Hd,className:"react-aria-Toast",style:{viewTransitionName:n.key,"--ac-internal-token-color":Zd(n.content.variant)},"data-variant":n.content.variant,"data-theme":t,children:[s("div",{css:m`
          display: flex;
          justify-content: space-between;
          width: 100%;
        `,children:[s(o1,{children:[s(C,{slot:"title",size:"M",children:[n.content.icon,n.content.title]}),e(C,{slot:"description",children:n.content.message})]}),e(z,{slot:"close",size:"S",type:"button",leadingVisual:e(T,{svg:e(ba,{})})})]}),n.content.action?e("div",{className:"toast-action-container",children:typeof n.content.action=="object"&&"text"in n.content.action?e(z,{className:"toast-action-button",onPress:()=>{const l=n.content.action;if(typeof l=="object"&&l&&"onClick"in l){const i=l.closeOnClick??!0,r=()=>{a==null||a.close(n.key)};l.onClick(r),i&&r()}},size:"S",children:n.content.action.text}):n.content.action}):null]})},Gd=m`
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
  border-radius: var(--ac-global-rounding-small);
  background: var(--ac-global-tooltip-background-color);
  border: var(--ac-global-border-size-thin) solid
    var(--ac-global-tooltip-border-color);
  color: var(--ac-global-text-color-900);
  forced-color-adjust: none;
  outline: none;
  padding: var(--ac-global-dimension-static-size-100)
    var(--ac-global-dimension-static-size-200);
  max-width: 200px;
  font-size: var(--ac-global-font-size-s);
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
    margin-bottom: var(--ac-global-dimension-static-size-100);
    --tooltip-origin: translateY(4px);
  }

  &[data-placement="bottom"] {
    margin-top: var(--ac-global-dimension-static-size-100);
    --tooltip-origin: translateY(-4px);

    & .react-aria-OverlayArrow svg {
      transform: rotate(180deg);
    }
  }

  &[data-placement="right"] {
    margin-left: var(--ac-global-dimension-static-size-100);
    --tooltip-origin: translateX(-4px);

    & .react-aria-OverlayArrow svg {
      transform: rotate(90deg);
    }
  }

  &[data-placement="left"] {
    margin-right: var(--ac-global-dimension-static-size-100);
    --tooltip-origin: translateX(4px);

    & .react-aria-OverlayArrow svg {
      transform: rotate(-90deg);
    }
  }

  & .react-aria-OverlayArrow svg {
    display: block;
    fill: var(--ac-global-tooltip-background-color);
    stroke: var(--ac-global-tooltip-border-color);
    stroke-width: 1px;
  }
`,Qd=m`
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
  border-radius: var(--ac-global-rounding-medium);
  background: var(--ac-global-tooltip-background-color);
  border: var(--ac-global-border-size-thin) solid
    var(--ac-global-tooltip-border-color);
  color: var(--ac-global-text-color-900);
  forced-color-adjust: none;
  outline: none;
  padding: var(--ac-global-dimension-static-size-200);
  min-width: 200px;
  font-size: var(--ac-global-font-size-s);
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
    margin-bottom: var(--ac-global-dimension-static-size-100);
    --tooltip-origin: translateY(4px);
  }

  &[data-placement="bottom"] {
    margin-top: var(--ac-global-dimension-static-size-100);
    --tooltip-origin: translateY(-4px);

    & .react-aria-OverlayArrow svg {
      transform: rotate(180deg);
    }
  }

  &[data-placement="right"] {
    margin-left: var(--ac-global-dimension-static-size-100);
    --tooltip-origin: translateX(-4px);

    & .react-aria-OverlayArrow svg {
      transform: rotate(90deg);
    }
  }

  &[data-placement="left"] {
    margin-right: var(--ac-global-dimension-static-size-100);
    --tooltip-origin: translateX(4px);

    & .react-aria-OverlayArrow svg {
      transform: rotate(-90deg);
    }
  }

  & .react-aria-OverlayArrow svg {
    display: block;
    fill: var(--ac-global-tooltip-background-color);
    stroke: var(--ac-global-tooltip-border-color);
    stroke-width: 1px;
  }
`;function Wd(n,a){const{css:t,...l}=n;return e(mt,{...l,ref:a,css:m(Gd,t)})}const ke=p.forwardRef(Wd);function qd(n,a){const{css:t}=n;return e(jl,{ref:a,css:t,className:V("react-aria-OverlayArrow"),children:e("svg",{width:8,height:8,viewBox:"0 0 8 8",children:e("path",{d:"M0 0 L4 4 L8 0"})})})}const ae=p.forwardRef(qd);function _i({children:n,...a}){return e(te,{...a,children:e("div",{role:"button",children:n})})}function Xd(n,a){const{children:t,css:l,width:i,...r}=n;return e(mt,{...r,ref:a,css:m(Qd,l),style:i?{width:i}:{maxWidth:"300px"},children:t})}const ie=p.forwardRef(Xd),Yd=m`
  display: flex;
  align-items: center;

  a {
    color: var(--ac-global-text-color-700);
    text-decoration: none;
    &:hover {
      text-decoration: underline;
    }
  }

  &[data-current],
  &[data-current] a {
    color: var(--ac-global-text-color-900);
    font-weight: 600;
    cursor: default;
    &:hover {
      text-decoration: none;
    }
  }
`;function Jd(n,a){const{children:t,...l}=n;return e(c1,{css:Yd,...l,ref:a,children:({isCurrent:i})=>s(U,{children:[t,!i&&e(T,{svg:e(xc,{})})]})})}const e2=p.forwardRef(Jd),n2=m`
  display: flex;
  align-items: center;
  margin: 0;
  padding: 0;
  color: var(--ac-global-text-color-900);
  --breadcrumb-separator-icon-padding: var(--ac-global-dimension-size-50);

  &[data-size="S"] {
    font-size: var(--ac-global-font-size-s);
    line-height: var(--ac-global-line-height-s);
    --breadcrumb-separator-icon-padding: var(--ac-global-dimension-size-25);
  }

  &[data-size="M"] {
    font-size: var(--ac-global-font-size-m);
    line-height: var(--ac-global-line-height-m);
    --breadcrumb-separator-icon-padding: var(--ac-global-dimension-size-50);
  }

  &[data-size="L"] {
    font-size: var(--ac-global-font-size-l);
    line-height: var(--ac-global-line-height-l);
    --breadcrumb-separator-icon-padding: var(--ac-global-dimension-size-75);
  }

  .ac-icon-wrap {
    padding: 0 var(--breadcrumb-separator-icon-padding);
  }
`;function a2(n,a){const{size:t="M",...l}=n;return e(d1,{css:n2,...l,ref:a,"data-size":t})}const t2=p.forwardRef(a2),l2=Me`
  100% {
    transform: rotate(360deg);
  }
`,i2=Me`
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
`,r2=m`
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
      (
        var(--progress-circle-value) / 100 *
          var(--progress-circle-circumference)
      )
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
    stroke: var(--ac-global-color-grey-300);
    stroke-width: var(--progress-circle-stroke-width);
  }

  .progress-circle__arc {
    cx: var(--progress-circle-center);
    cy: var(--progress-circle-center);
    r: var(--progress-circle-radius);
    stroke: var(--ac-global-color-primary);
    stroke-width: var(--progress-circle-stroke-width);
    transition: stroke-dashoffset 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    stroke-dasharray: var(--progress-circle-dasharray);
    stroke-dashoffset: var(--progress-circle-dashoffset);
  }

  &[data-indeterminate] {
    .progress-circle__svg {
      animation: ${l2} 3s linear infinite;
    }
    .progress-circle__arc {
      animation: ${i2} 3s cubic-bezier(0.4, 0, 0.2, 1) infinite;
      stroke-dasharray:
        calc(var(--progress-circle-circumference) * 0.25),
        var(--progress-circle-circumference);
      stroke-dashoffset: 0;
    }
  }
`,o2=m`
  inline-size: var(--ac-global-dimension-size-2400);
  height: var(--ac-global-dimension-size-75);

  .progress-bar__track {
    forced-color-adjust: none;
    height: 100%;
    border-radius: 3px;
    overflow: hidden;
    background-color: var(
      --mod-barloader-track-color,
      var(--ac-global-color-grey-300)
    );
  }

  .progress-bar__fill {
    background: var(--mod-barloader-fill-color, var(--ac-global-color-primary));
    height: 100%;
  }
`;function s2(n,a){const{isIndeterminate:t=!1,value:l,size:i="M"}=n;return e(Wl,{...n,"data-size":i,"data-indeterminate":t||void 0,css:r2,ref:a,style:!t&&l!=null?{"--progress-circle-value":l}:void 0,children:s("svg",{className:"progress-circle__svg",children:[e("circle",{className:"progress-circle__background"}),e("circle",{className:"progress-circle__arc"})]})})}const Ki=p.forwardRef(s2);function c2({width:n,height:a,...t},l){return e(Wl,{...t,ref:l,css:o2,style:{width:n,height:a},children:({percentage:i})=>e("div",{className:"progress-bar__track",children:e("div",{className:"progress-bar__fill",style:{width:i+"%"}})})})}const $8=p.forwardRef(c2),d2=m`
  list-style: none;
  padding: 0;
  margin: 0;

  & li {
    position: relative;
    padding: var(--ac-global-dimension-static-size-200);

    &:not(:first-of-type)::after {
      content: " ";
      border-top: 1px solid var(--ac-global-border-color-default);
      position: absolute;
      left: var(--ac-global-dimension-static-size-200);
      right: 0;
      top: 0;
    }
  }

  &[data-list-size="S"] {
    & li {
      padding: var(--ac-global-dimension-static-size-100);

      &:not(:first-of-type)::after {
        left: var(--ac-global-dimension-static-size-100);
      }
    }
  }
`;function u2({size:n="M",children:a,...t},l){return e("ul",{ref:l,css:d2,"data-list-size":n,...t,children:a})}const B8=p.forwardRef(u2);function g2({children:n,...a},t){return e("li",{ref:t,...a,children:n})}const H8=p.forwardRef(g2),m2=Me`
  from {
    transform: translate(-50%, var(--ac-global-dimension-size-450));
    opacity: 0;
  }
  to {
    transform: translate(-50%, 0);
    opacity: 1;
  }
`,p2=m`
  position: absolute;
  bottom: var(--ac-global-dimension-size-450);
  left: 50%;
  transform: translateX(-50%);
  z-index: 10;
  box-shadow:
    0px 10px 20px 0px rgba(0, 0, 0, 0.1),
    0px 4px 8px 0px rgba(0, 0, 0, 0.1);
  border-radius: var(--ac-global-rounding-medium);
  padding: var(--ac-global-dimension-size-100);
  background-color: var(--ac-floating-toolbar-background-color);
  border: 1px solid var(--ac-floating-toolbar-border-color);
  animation: ${m2} 0.1s ease-in-out;
`,j8=({children:n})=>e("div",{css:p2,children:n}),h2=m`
  display: flex;

  gap: var(--ac-global-dimension-size-100);

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
`;function f2(n,a){return e(u1,{...n,ref:a,css:h2,children:n.children})}const b2=p.forwardRef(f2);b2.displayName="Toolbar";const y2=m`
  align-self: stretch;
  background-color: var(--ac-global-border-color-default);

  &[aria-orientation="vertical"] {
    width: 1px;
    margin: 0 var(--ac-global-dimension-size-50);
  }

  &:not([aria-orientation="vertical"]) {
    border: none;
    height: 1px;
    width: 100%;
    margin: var(--ac-global-dimension-size-50) 0;
  }
`;function v2(n,a){return e(g1,{...n,ref:a,css:y2,className:"ac-separator react-aria-Separator"})}const C2=p.forwardRef(v2);C2.displayName="Separator";const k2=n=>m`
  --scope-border-color: ${(n==null?void 0:n.borderColor)??"var(--ac-global-border-color-default)"};
  --collapsible-card-animation-duration: 200ms;
  --collapsible-card-icon-size: var(--ac-global-dimension-size-300);

  display: flex;
  flex-direction: column;
  background-color: var(--ac-global-background-color-dark);
  color: var(--ac-global-text-color-900);
  border-radius: var(--ac-global-rounding-medium);
  border: 1px solid var(--scope-border-color);
  overflow: hidden;

  /* Card Header Styles */
  & > header {
    display: flex;
    flex-direction: row;
    flex: none;
    justify-content: space-between;
    align-items: center;
    padding: 0 var(--ac-global-dimension-static-size-200);
    height: var(--ac-global-card-header-height);
    transition: background-color 0.2s ease-in-out;

    & .card__collapse-toggle-icon {
      width: var(--collapsible-card-icon-size);
      height: var(--collapsible-card-icon-size);
      font-size: 1.3em;
      color: inherit;
      display: flex;
      margin-right: var(--ac-global-dimension-static-size-100);
      transition: transform ease var(--collapsible-card-animation-duration);

      & svg {
        height: var(--collapsible-card-icon-size);
        width: var(--collapsible-card-icon-size);
      }
    }

    & .card__title {
      font-size: var(--ac-global-font-size-m);
      line-height: var(--ac-global-line-height-m);
      display: flex;
      align-items: center;
      gap: var(--ac-global-dimension-static-size-100);
    }

    & .card__sub-title {
      color: var(--ac-global-text-color-700);
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
      color: var(--ac-global-text-color-900);
    }
  }

  &[data-collapsed="false"][data-title-separator="true"] > header {
    border-bottom: 1px solid var(--scope-border-color);
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
    font-size: var(--ac-global-font-size-m);
    line-height: var(--ac-global-line-height-m);
  }

  /* Collapsible behavior */
  &[data-collapsible="true"] {
    & > header:hover {
      background-color: rgba(255, 255, 255, 0.1);
    }
  }

  &[data-collapsed="true"] {
    & .card__body {
      display: none !important;
    }
    & .card__collapse-toggle-icon {
      transform: rotate(-90deg);
    }
  }
`;function L2({title:n,titleExtra:a,titleSeparator:t=!0,subTitle:l,children:i,collapsible:r=!1,defaultOpen:o=!0,scrollBody:c=!1,extra:d,...u},g){const{styleProps:h}=Vn(u,bi),[f,b]=p.useState(r?!o:!1),y=p.useId(),v=p.useId(),k=p.useId(),L=s("div",{children:[s(ne,{level:3,weight:"heavy",className:"card__title",children:[n,a]}),l&&e(ne,{level:4,className:"card__sub-title",children:l})]});return s("section",{ref:g,css:k2(h.style),className:"card","data-collapsible":r,"data-collapsed":f,"data-title-separator":t,style:h.style,children:[s("header",{id:y,children:[r?s("button",{onClick:()=>b(!f),className:"card__collapsible-button button--reset",id:v,"aria-controls":k,"aria-expanded":!f,children:[e(T,{svg:e(Ac,{}),className:"card__collapse-toggle-icon","aria-hidden":"true"}),L]}):L,d]}),e("div",{className:"card__body",id:k,"aria-labelledby":y,"aria-hidden":f,"data-scrollable":c,children:i})]})}const Pi=p.forwardRef(L2),Vi=5e3,Ri=p.createContext(null),w2=(...n)=>new m1(...n),Z8=({children:n})=>{const[a]=p.useState(()=>w2({wrapUpdate(t){"startViewTransition"in document?document==null||document.startViewTransition(()=>{p1.flushSync(t)}):t()}}));return s(Ri.Provider,{value:{queue:a},children:[e(jd,{queue:a}),n]})},Oi=()=>{const n=p.useContext(Ri);if(!n)throw new Error("useNotificationContext must be used within a NotificationProvider");return n.queue},zt=()=>{const n=Oi();return({expireMs:a=Vi,...t})=>n.add({...t,variant:"success",icon:e(T,{svg:e(wt,{})})},a===null?void 0:{timeout:a})},Ni=()=>{const n=Oi();return({expireMs:a=Vi,...t})=>n.add({...t,variant:"error",icon:e(T,{svg:e(ki,{})})},a===null?void 0:{timeout:a})},$i="arize-phoenix-theme";function Bi(){return localStorage.getItem($i)==="light"?"light":"dark"}const Mt=p.createContext(null);function le(){const n=p.useContext(Mt);if(n===null)throw new Error("useTheme must be used within a ThemeProvider");return n}function U8(n){const[a,t]=p.useState(()=>n.theme||Bi()),l=p.useCallback(i=>{localStorage.setItem($i,i),t(i)},[]);return p.useEffect(()=>{n.theme&&t(n.theme)},[n.theme,l]),p.useEffect(()=>(document.body.classList.add(`ac-theme--${a}`),()=>{document.body.classList.remove(`ac-theme--${a}`)}),[a]),e(Mt.Provider,{value:{theme:a,setTheme:l},children:n.children})}const S2=n=>`arize-phoenix-project-${n}`;function x2({projectId:n}){return{state:wn()(ga(t=>({defaultTab:"spans",setDefaultTab:l=>{t({defaultTab:l})},treatOrphansAsRoots:!1,setTreatOrphansAsRoots:l=>{t({treatOrphansAsRoots:l})}}),{name:S2(n)}))}}const Hi=p.createContext(null);function G8({children:n,projectId:a}){const[t]=p.useState(()=>x2({projectId:a}));return e(Hi.Provider,{value:t,children:n})}function Q8(n,a){const t=p.useContext(Hi);if(!t)throw new Error("Missing ProjectContext.Provider in the tree");return gt(t.state,n,a)}const ji=(function(){var n={alias:null,args:null,kind:"ScalarField",name:"id",storageKey:null},a={alias:null,args:null,kind:"ScalarField",name:"name",storageKey:null};return{fragment:{argumentDefinitions:[],kind:"Fragment",metadata:null,name:"ViewerContextRefetchQuery",selections:[{args:null,kind:"FragmentSpread",name:"ViewerContext_viewer"}],type:"Query",abstractKey:null},kind:"Request",operation:{argumentDefinitions:[],kind:"Operation",name:"ViewerContextRefetchQuery",selections:[{alias:null,args:null,concreteType:"User",kind:"LinkedField",name:"viewer",plural:!1,selections:[n,{alias:null,args:null,kind:"ScalarField",name:"username",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"email",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"profilePictureUrl",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"isManagementUser",storageKey:null},{alias:null,args:null,concreteType:"UserRole",kind:"LinkedField",name:"role",plural:!1,selections:[a,n],storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"authMethod",storageKey:null},{alias:null,args:null,concreteType:"UserApiKey",kind:"LinkedField",name:"apiKeys",plural:!0,selections:[n,a,{alias:null,args:null,kind:"ScalarField",name:"description",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"createdAt",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"expiresAt",storageKey:null}],storageKey:null}],storageKey:null}]},params:{cacheID:"79221da09cbb1334cb0c446af434f607",id:null,metadata:{},name:"ViewerContextRefetchQuery",operationKind:"query",text:`query ViewerContextRefetchQuery {
  ...ViewerContext_viewer
}

fragment APIKeysTableFragment on User {
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
    ...APIKeysTableFragment
  }
}
`}}})();ji.hash="d85505e5f9dffd2a1c791f8e0007ab61";const Zi={argumentDefinitions:[],kind:"Fragment",metadata:{refetch:{connection:null,fragmentPathInResult:[],operation:ji}},name:"ViewerContext_viewer",selections:[{alias:null,args:null,concreteType:"User",kind:"LinkedField",name:"viewer",plural:!1,selections:[{alias:null,args:null,kind:"ScalarField",name:"id",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"username",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"email",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"profilePictureUrl",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"isManagementUser",storageKey:null},{alias:null,args:null,concreteType:"UserRole",kind:"LinkedField",name:"role",plural:!1,selections:[{alias:null,args:null,kind:"ScalarField",name:"name",storageKey:null}],storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"authMethod",storageKey:null},{args:null,kind:"FragmentSpread",name:"APIKeysTableFragment"}],storageKey:null}],type:"Query",abstractKey:null};Zi.hash="d85505e5f9dffd2a1c791f8e0007ab61";const Ui=rn.createContext({viewer:null,refetchViewer:()=>{}});function xn(){const n=rn.useContext(Ui);if(n==null)throw new Error("useViewer must be used within a ViewerProvider");return n}function T2(){var a;const{viewer:n}=xn();return!(n&&((a=n==null?void 0:n.role)==null?void 0:a.name)!=="ADMIN")}function W8({query:n,children:a}){const[t,l]=M.useRefetchableFragment(Zi,n),i=()=>{p.startTransition(()=>{l({},{fetchPolicy:"network-only"})})};return e(Ui.Provider,{value:{viewer:t.viewer,refetchViewer:i},children:a})}function A2(n){return n.endsWith("/")?n.slice(0,-1):n}const I2=A2(window.Config.basename),Tn=`${window.location.protocol}//${window.location.host}${I2}`,q8=window.Config.platformVersion,Rn="returnUrl";function ul(n,a){const t=new URL(n,window.location.origin);return a.forEach((l,i)=>{t.searchParams.append(i,l)}),t.pathname+t.search}function Gi(){const n=window.Config.basename,a=n==null||n===""||n==="/",t=n!=null&&n.startsWith("/")&&!n.endsWith("/");if(!(a||t))throw new Error(`Invalid basename: ${n}`);const l=window.location.pathname,i=window.location.origin,r=new URLSearchParams(window.location.search);if(a){const o=new URL("/login",i);return o.searchParams.set(Rn,ul(l,r)),o.pathname+o.search}if(l.startsWith(n)){const o=l.slice(n.length);if(o===""||o.startsWith("/")){const d=new URL(n+"/login",i);return d.searchParams.set(Rn,ul(o,r)),d.pathname+d.search}}return n+"/login"}function X8(n){const a=window.Config.basename,t=a==null||a===""||a==="/",l=a!=null&&a.startsWith("/")&&!a.endsWith("/");if(!(t||l))throw new Error(`Invalid basename: ${a}`);return t?n:a+n}const Y8=({path:n,searchParams:a})=>{const l=new URL(window.location.href).searchParams.get(Rn),i=new URLSearchParams(a||{});l&&i.set(Rn,l);const r=i.toString();return`${n}${r?`?${r}`:""}`},z2=n=>!(typeof n!="string"||!n.startsWith("/")||n.replace(/\\/g,"/").startsWith("//")),M2=n=>z2(n)?n:"/",J8=()=>{const n=new URL(window.location.href);return M2(n.searchParams.get(Rn))},F2=Tn+"/auth/refresh";class gl extends Error{constructor(){super("Unauthorized")}}async function E2(n,a){try{return await fetch(n,a).then(t=>{if(t.status===401)throw new gl;return t})}catch(t){if(t instanceof gl){const l=await D2();return pt(l.ok,`Failed to authenticate. Please visit ${Gi()} to login.`),fetch(n,a)}if(t instanceof Error&&t.name==="AbortError")throw t}throw new Error("An unexpected error occurred while fetching data")}let In=null;async function D2(){return In||(In=fetch(F2,{method:"POST"}).then(n=>n.ok?(In=null,Promise.resolve(n)):(window.location.href=Gi(),new Promise(()=>{}))),In)}const Qi=Tn+"/graphql",_2=window.Config.authenticationEnabled,Wi=_2?E2:fetch;function K2(n,a,t){return Dn.Observable.create(l=>{const i=new AbortController;return Wi(n,{...a,signal:i.signal}).then(r=>(pt(r instanceof Response),r.json())).then(r=>{const o=t==null?void 0:t(r);if(o)throw o;l.next(r),l.complete()}).catch(r=>{r.name==="AbortError"?l.complete():l.error(r)}),()=>{i.abort()}})}const P2=(n,a,t)=>K2(Qi,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({query:n.text,variables:a})},l=>{if(!(!fe(l)||!("errors"in l))&&Array.isArray(l.errors))return new Error(`Error fetching GraphQL query '${n.name}' with variables '${JSON.stringify(a)}': ${JSON.stringify(l.errors)}`)}),V2=h1(Qi,{fetch:Wi}),Qn=new Dn.Environment({network:Dn.Network.create(P2,V2),store:new Dn.Store(new Dn.RecordSource,{gcReleaseBufferSize:20})});function qi(n){return n.includes("PRIMARY")?Te.primary:n.includes("CORPUS")?Te.corpus:Te.reference}function Ft(n){const a=[],t=[],l=[];return n.forEach(i=>{const r=qi(i);r==Te.primary?a.push(i):r==Te.corpus?l.push(i):t.push(i)}),{primaryEventIds:a,referenceEventIds:t,corpusEventIds:l}}const ia=10,_n="unknown",Xi=b1,Yi=f1,R2=n=>Yi[n],O2=n=>Xi(n/ia);var kn=(n=>(n.move="move",n.select="select",n))(kn||{}),Et=(n=>(n.default="default",n.highlight="highlight",n))(Et||{});const mn=()=>Bi()==="light"?Zs:js;function eg(){const n=mn();return{coloringStrategy:B.inferences,pointGroupVisibility:{[G.primary]:!0,[G.reference]:!0},pointGroupColors:{[G.primary]:n[0],[G.reference]:n[1],[G.corpus]:He},metric:{type:"drift",metric:"euclideanDistance"}}}function ng(){const n=mn();return{coloringStrategy:B.inferences,pointGroupVisibility:{[G.primary]:!0,[G.corpus]:!0},pointGroupColors:{[G.primary]:n[0],[G.corpus]:He},metric:{type:"retrieval",metric:"queryDistance"},clusterSort:{dir:"desc",column:"primaryMetricValue"}}}function ag(){return{coloringStrategy:B.correctness,pointGroupVisibility:{[se.correct]:!0,[se.incorrect]:!0,[se.unknown]:!0},pointGroupColors:{[se.correct]:ta.Discrete2.LightBlueOrange[0],[se.incorrect]:ta.Discrete2.LightBlueOrange[1],[se.unknown]:gn},metric:{type:"performance",metric:"accuracyScore"},clusterSort:{dir:"asc",column:"primaryMetricValue"}}}const N2=n=>{const a={loading:!1,errorMessage:null,points:[],eventIdToDataMap:new Map,clusters:[],clusterSort:{dir:"desc",column:"driftRatio"},pointData:null,selectedEventIds:new Set,hoveredEventId:null,highlightedClusterId:null,selectedClusterId:null,canvasMode:"move",pointSizeScale:1,clusterColorMode:"default",coloringStrategy:B.inferences,inferencesVisibility:{primary:!0,reference:!0,corpus:!0},pointGroupVisibility:{[G.primary]:!0,[G.reference]:!0,[G.corpus]:!0},pointGroupColors:{[G.primary]:mn()[0],[G.reference]:mn()[1],[G.corpus]:He},eventIdToGroup:{},selectionDisplay:yn.gallery,selectionGridSize:hn.large,dimension:null,dimensionMetadata:null,umapParameters:{minDist:Rs,nNeighbors:Vs,nSamples:Os},hdbscanParameters:{minClusterSize:Ns,clusterMinSamples:Bs,clusterSelectionEpsilon:Hs},clustersLoading:!1,metric:{type:"drift",metric:"euclideanDistance"},selectionSearchText:""},t=(l,i)=>({...a,...n,setInitialData:async({points:r,clusters:o,retrievals:c})=>{const d=i(),u=new Map,g=c.reduce((b,y)=>{const{queryId:v}=y;return b[v]?b[v].push(y):b[v]=[y],b},{});r.forEach(b=>{b={...b,retrievals:g[b.eventId]??[]},u.set(b.eventId,b)});const h=o.map(pl).sort(Ba(d.clusterSort));l({loading:!1,points:r,eventIdToDataMap:u,clusters:h,clustersLoading:!1,selectedEventIds:new Set,selectedClusterId:null,pointData:null,eventIdToGroup:Ye({points:r,coloringStrategy:d.coloringStrategy,pointsData:d.pointData??{},dimension:d.dimension||null,dimensionMetadata:d.dimensionMetadata})});const f=await H2(r.map(b=>b.eventId)).catch(()=>l({errorMessage:"Failed to load the point events"}));f&&l({pointData:f,clusters:h,clustersLoading:!1,eventIdToGroup:Ye({points:r,coloringStrategy:d.coloringStrategy,pointsData:f??{},dimension:d.dimension||null,dimensionMetadata:d.dimensionMetadata})})},setClusters:r=>{const o=i(),c=r.map(pl).sort(Ba(o.clusterSort));l({clusters:c,clustersLoading:!1,selectedClusterId:null,highlightedClusterId:null})},setClusterSort:r=>{const c=[...i().clusters].sort(Ba(r));l({clusterSort:r,clusters:c})},setSelectedEventIds:r=>l({selectedEventIds:r,selectionSearchText:""}),setHoveredEventId:r=>l({hoveredEventId:r}),setHighlightedClusterId:r=>l({highlightedClusterId:r}),setSelectedClusterId:r=>l({selectedClusterId:r,highlightedClusterId:null}),setPointSizeScale:r=>l({pointSizeScale:r}),setCanvasMode:r=>l({canvasMode:r}),setClusterColorMode:r=>l({clusterColorMode:r}),setColoringStrategy:r=>{const o=i();switch(l({coloringStrategy:r}),r){case B.correctness:l({pointGroupVisibility:{[se.correct]:!0,[se.incorrect]:!0,[se.unknown]:!0},pointGroupColors:{[se.correct]:ta.Discrete2.LightBlueOrange[0],[se.incorrect]:ta.Discrete2.LightBlueOrange[1],[se.unknown]:gn},dimension:null,dimensionMetadata:null,eventIdToGroup:Ye({points:o.points,coloringStrategy:r,pointsData:o.pointData??{},dimension:o.dimension||null,dimensionMetadata:o.dimensionMetadata})});break;case B.inferences:{l({pointGroupVisibility:{[G.primary]:!0,[G.reference]:!0,[G.corpus]:!0},pointGroupColors:{[G.primary]:mn()[0],[G.reference]:mn()[1],[G.corpus]:He},dimension:null,dimensionMetadata:null,eventIdToGroup:Ye({points:o.points,coloringStrategy:r,pointsData:o.pointData??{},dimension:o.dimension||null,dimensionMetadata:o.dimensionMetadata})});break}case B.dimension:{l({pointGroupVisibility:{unknown:!0},pointGroupColors:{unknown:gn},dimension:null,dimensionMetadata:null,eventIdToGroup:Ye({points:o.points,coloringStrategy:r,pointsData:o.pointData??{},dimension:o.dimension||null,dimensionMetadata:o.dimensionMetadata})});break}default:P()}},inferencesVisibility:{primary:!0,reference:!0,corpus:!0},setInferencesVisibility:r=>l({inferencesVisibility:r}),setPointGroupVisibility:r=>l({pointGroupVisibility:r}),selectionDisplay:yn.gallery,setSelectionDisplay:r=>l({selectionDisplay:r}),setSelectionGridSize:r=>l({selectionGridSize:r}),reset:()=>{l({points:[],clusters:[],selectedEventIds:new Set,selectedClusterId:null,eventIdToGroup:{}})},setDimension:async r=>{const o=i();l({dimension:r,dimensionMetadata:null});const c=await B2(r).catch(()=>l({errorMessage:"Failed to load the dimension metadata"}));if(c){if(l({dimensionMetadata:c}),c.categories&&c.categories.length){const d=c.categories.length,g=d<=Yi.length?R2:h=>Xi(h/d);l({pointGroupVisibility:{...c.categories.reduce((h,f)=>({...h,[f]:!0}),{}),unknown:!0},pointGroupColors:{...c.categories.reduce((h,f,b)=>({...h,[f]:g(b)}),{}),unknown:gn},eventIdToGroup:Ye({points:o.points,coloringStrategy:o.coloringStrategy,pointsData:o.pointData??{},dimension:r,dimensionMetadata:c})})}else if(c.interval!==null){const d=Ji(c.interval);l({pointGroupVisibility:{...d.reduce((u,g)=>({...u,[g.name]:!0}),{}),unknown:!0},pointGroupColors:{...d.reduce((u,g,h)=>({...u,[g.name]:O2(h)}),{}),unknown:gn},eventIdToGroup:Ye({points:o.points,coloringStrategy:o.coloringStrategy,pointsData:o.pointData??{},dimension:r,dimensionMetadata:c})})}}},setDimensionMetadata:r=>l({dimensionMetadata:r}),setUMAPParameters:r=>l({umapParameters:r}),setHDBSCANParameters:async r=>{const o=i();l({hdbscanParameters:r,clustersLoading:!0});const c=await j2({metric:o.metric,points:o.points,hdbscanParameters:r});o.setClusters(c)},getHDSCANParameters:()=>i().hdbscanParameters,getMetric:()=>i().metric,setErrorMessage:r=>l({errorMessage:r}),setLoading:r=>l({loading:r}),setMetric:async r=>{const o=i();l({metric:r,clustersLoading:!0});const c=await Z2({metric:r,clusters:o.clusters,hdbscanParameters:o.hdbscanParameters});o.setClusters(c)},setSelectionSearchText:r=>l({selectionSearchText:r})});return wn()(Bn(t))},ml=new Intl.NumberFormat([],{maximumFractionDigits:2});function $2({min:n,max:a}){return`${ml.format(n)} - ${ml.format(a)}`}function Ji({min:n,max:a}){const l=(a-n)/ia,i=[];for(let r=0;r<ia;r++){const o=n+r*l,c=n+(r+1)*l;i.push({min:o,max:c,name:$2({min:o,max:c})})}return i}function $a({numericGroupIntervals:n,numericValue:a}){let t=_n,l=n.findIndex(i=>a>=i.min&&a<i.max);return l=l===-1?ia-1:l,t=n[l].name,t}function Ye(n){const{points:a,coloringStrategy:t,pointsData:l,dimension:i,dimensionMetadata:r}=n,o={},c=a.map(d=>d.eventId);switch(t){case B.inferences:{const{primaryEventIds:d,referenceEventIds:u,corpusEventIds:g}=Ft(c);d.forEach(h=>{o[h]=G.primary}),u.forEach(h=>{o[h]=G.reference}),g.forEach(h=>{o[h]=G.corpus});break}case B.correctness:{a.forEach(d=>{let u=se.unknown;const{predictionLabel:g,actualLabel:h}=d.eventMetadata;g!==null&&h!==null&&(u=g===h?se.correct:se.incorrect),o[d.eventId]=u});break}case B.dimension:{let d;r&&(r==null?void 0:r.interval)!==null&&(d=Ji(r.interval));const u=(i==null?void 0:i.type)==="prediction"&&(i==null?void 0:i.dataType)==="categorical",g=(i==null?void 0:i.type)==="prediction"&&(i==null?void 0:i.dataType)==="numeric",h=(i==null?void 0:i.type)==="actual"&&(i==null?void 0:i.dataType)==="categorical",f=(i==null?void 0:i.type)==="actual"&&(i==null?void 0:i.dataType)==="numeric";a.forEach(b=>{let y=_n;const v=l[b.eventId];if(i!=null&&v!=null)if(u)y=v.eventMetadata.predictionLabel??_n;else if(g){if(d==null)throw new Error("Cannot color by prediction score without numeric group intervals");const L=v.eventMetadata.predictionScore;typeof L=="number"&&(y=$a({numericGroupIntervals:d,numericValue:L}))}else if(f){if(d==null)throw new Error("Cannot color by actual score without numeric group intervals");const L=v.eventMetadata.actualScore;typeof L=="number"&&(y=$a({numericGroupIntervals:d,numericValue:L}))}else if(h)y=v.eventMetadata.actualLabel??_n;else{const L=v.dimensions.find(E=>E.dimension.name===i.name);if(L!=null&&i.dataType==="categorical")y=L.value??_n;else if(L!=null&&i.dataType==="numeric"&&d!=null){const E=typeof(L==null?void 0:L.value)=="string"?parseFloat(L.value):null;typeof E=="number"&&(y=$a({numericGroupIntervals:d,numericValue:E}))}}o[b.eventId]=y});break}default:P()}return o}async function B2(n){const a=await M.fetchQuery(Qn,pi,{id:n.id,getDimensionMinMax:n.dataType==="numeric",getDimensionCategories:n.dataType==="categorical"}).toPromise(),t=a==null?void 0:a.dimension;if(!n)throw new Error("Dimension not found");let l=null;return typeof(t==null?void 0:t.min)=="number"&&typeof(t==null?void 0:t.max)=="number"&&(l={min:t.min,max:t.max}),{interval:l,categories:(t==null?void 0:t.categories)??null}}async function H2(n){var u,g,h,f,b,y;const{primaryEventIds:a,referenceEventIds:t,corpusEventIds:l}=Ft([...n]),i=await M.fetchQuery(Qn,mi,{primaryEventIds:a,referenceEventIds:t,corpusEventIds:l}).toPromise(),r=((g=(u=i==null?void 0:i.model)==null?void 0:u.primaryInferences)==null?void 0:g.events)??[],o=((f=(h=i==null?void 0:i.model)==null?void 0:h.referenceInferences)==null?void 0:f.events)??[],c=((y=(b=i==null?void 0:i.model)==null?void 0:b.corpusInferences)==null?void 0:y.events)??[];return[...r,...o,...c].reduce((v,k)=>(v[k.id]=k,v),{})}async function j2({metric:n,points:a,hdbscanParameters:t}){const l=await M.fetchQuery(Qn,gi,{eventIds:a.map(i=>i.eventId),coordinates:a.map(i=>({x:i.position[0],y:i.position[1],z:i.position[2]})),fetchDataQualityMetric:n.type==="dataQuality",dataQualityMetricColumnName:n.type==="dataQuality"?n.dimension.name:null,fetchPerformanceMetric:n.type==="performance",performanceMetric:n.type==="performance"?n.metric:"accuracyScore",...t},{fetchPolicy:"network-only"}).toPromise();return(l==null?void 0:l.hdbscanClustering)??[]}async function Z2({metric:n,clusters:a,hdbscanParameters:t}){const l=await M.fetchQuery(Qn,ui,{clusters:a.map(i=>({id:i.id,eventIds:i.eventIds})),fetchDataQualityMetric:n.type==="dataQuality",dataQualityMetricColumnName:n.type==="dataQuality"?n.dimension.name:null,fetchPerformanceMetric:n.type==="performance",performanceMetric:n.type==="performance"?n.metric:"accuracyScore",...t},{fetchPolicy:"network-only"}).toPromise();return(l==null?void 0:l.clusters)??[]}const Ba=n=>(a,t)=>{const{dir:l,column:i}=n,r=l==="asc",o=a[i],c=t[i];return o==null?1:c==null?-1:o>c?r?1:-1:o<c?r?-1:1:0};function pl(n){let a=n.driftRatio,t=null;return n.dataQualityMetric?(a=n.dataQualityMetric.primaryValue,t=n.dataQualityMetric.referenceValue):n.performanceMetric?(a=n.performanceMetric.primaryValue,t=n.performanceMetric.referenceValue):n.primaryToCorpusRatio!=null&&(a=(n.primaryToCorpusRatio+1)/2*100),{...n,size:n.eventIds.length,primaryMetricValue:a,referenceMetricValue:t}}const U2=({projectId:n,tableId:a})=>`arize-phoenix-tracing-${n}-${a}`,tg=n=>{const a=t=>({...n,columnVisibility:{metadata:!1},columnSizing:{metadata:200},annotationColumnVisibility:{},setColumnVisibility:l=>{t({columnVisibility:l})},setAnnotationColumnVisibility:l=>{t({annotationColumnVisibility:l})},setColumnSizing:l=>{t(typeof l=="function"?i=>({columnSizing:l(i.columnSizing)}):{columnSizing:l})}});return wn()(ga(Bn(a),{name:U2(n)}))},Ze={NONE:"NONE",FString:"F_STRING",Mustache:"MUSTACHE"},lg={OPENAI:"OpenAI",AZURE_OPENAI:"Azure OpenAI",ANTHROPIC:"Anthropic",GOOGLE:"Google",DEEPSEEK:"DeepSeek",XAI:"xAI",OLLAMA:"Ollama",AWS:"AWS Bedrock"},er="OPENAI",G2="gpt-4o",Q2="user",ig=["2024-10-01-preview","2024-09-01-preview","2024-08-01-preview","2024-07-01-preview","2024-06-01","2024-05-01-preview","2024-04-01-preview","2024-03-01-preview","2024-02-15-preview","2024-02-01","2023-10-01-preview","2023-09-01-preview","2023-08-01-preview","2023-07-01-preview","2023-06-01-preview","2023-05-15","2023-03-15-preview"],rg={user:["user","human"],ai:["assistant","bot","ai","model"],system:["system","developer"],tool:["tool"]},it={OPENAI:[{envVarName:"OPENAI_API_KEY",isRequired:!0}],AZURE_OPENAI:[{envVarName:"AZURE_OPENAI_API_KEY",isRequired:!0}],ANTHROPIC:[{envVarName:"ANTHROPIC_API_KEY",isRequired:!0}],GOOGLE:[{envVarName:"GEMINI_API_KEY",isRequired:!0}],DEEPSEEK:[{envVarName:"DEEPSEEK_API_KEY",isRequired:!0}],XAI:[{envVarName:"XAI_API_KEY",isRequired:!0}],OLLAMA:[],AWS:[{envVarName:"AWS_ACCESS_KEY_ID",isRequired:!0},{envVarName:"AWS_SECRET_ACCESS_KEY",isRequired:!0},{envVarName:"AWS_SESSION_TOKEN",isRequired:!1}]},nr=({parser:n,text:a})=>{const t=n.parse(a),l=[],i=t.cursor();do if(i.name==="Variable"){const r=a.slice(i.node.from,i.node.to).trim();l.push(r)}while(i.next());return l},ar=({parser:n,text:a,variables:t,postFormat:l})=>{if(!a)return"";let i=a,r=n.parse(i),o=r.cursor();do if(o.name==="Variable"){const c=i.slice(o.node.from,o.node.to).trim(),d=o.node.parent;c in t&&(i=`${i.slice(0,d.from)}${t[c]}${i.slice(d.to)}`,r=n.parse(i),o=r.cursor())}while(o.next());return l&&(i=l(i)),i},W2=ql.deserialize({version:14,states:"!WQQOPOOOcOQO'#C^OOOO'#Cb'#CbQQOPOOOOOO'#Cc'#CcOhOQO,58xOOOO-E6`-E6`OOOO-E6a-E6aOOOO1G.d1G.d",stateData:"v~ORPOXQOYQOZQO[QO~OSSO~OSSOTWO~OZRX[X~",goto:"iWPPXPPP]cTQORQRORURQTPRVT",nodeNames:"⚠ FStringTemplate Template LBrace Variable RBrace",maxTerm:12,skippedNodes:[0],repeatNodeCount:2,tokenData:"%[~RaXY!WYZ!W]^!Wpq!Wqr!Wrs!]sw!Wwx!bx#O!W#O#P!i#P#o!W#o#p$c#p#q!W#q#r$|#r;'S!W;'S;=`%U<%lO!W~!]OX~~!bO[~~!iOX~[~~!lYrs!W!P!Q!W#O#P!W#U#V!W#Y#Z!W#b#c!W#f#g!W#h#i!W#i#j#[#o#p$^~#_R!Q![#h!c!i#h#T#Z#h~#kR!Q![#t!c!i#t#T#Z#t~#wR!Q![$Q!c!i$Q#T#Z$Q~$TR!Q![!W!c!i!W#T#Z!W~$cOZ~~$jQR~X~#o#p$p#q#r$w~$wOZ~[~~$|OY~~%RPX~#q#r!]~%XP;=`<%l!W",tokenizers:[1,new Xl("!p~RVO#Oh#O#P!P#P#qh#q#r!j#r;'Sh;'S;=`y<%lOh~mSS~O#qh#r;'Sh;'S;=`y<%lOh~|P;=`<%lh~!UTS~O#qh#q#r!e#r;'Sh;'S;=`y<%lOh~!jOS~~!oOT~~",77)],topRules:{FStringTemplate:[0,1]},tokenPrec:32}),Dt=ii.define({parser:W2.configure({props:[Yl({"Template/LBrace":Be.quote,"Template/RBrace":Be.quote,"Template/Variable":Be.variableName,"⚠":Be.invalid})]}),languageData:{}}),q2=({text:n,variables:a})=>ar({parser:Dt.parser,text:n,variables:a,postFormat:t=>t.replaceAll("\\{","{").replaceAll("{{","{").replaceAll("}}","}")}),X2=n=>nr({parser:Dt.parser,text:n});function Y2(){return new ri(Dt)}const J2=ql.deserialize({version:14,states:"!WQQOPOOOcOQO'#C^OOOO'#Cb'#CbQQOPOOOOOO'#Cc'#CcOhOQO,58xOOOO-E6`-E6`OOOO-E6a-E6aOOOO1G.d1G.d",stateData:"v~ORPOXQOYQOZQO[QO~OSSO~OSSOTWO~OZRX[X~",goto:"iWPPXPPP]cTQORQRORURQTPRVT",nodeNames:"⚠ MustacheLikeTemplate Template LBrace Variable RBrace",maxTerm:12,skippedNodes:[0],repeatNodeCount:2,tokenData:"%W~RaXY!WYZ!W]^!Wpq!Wqr!Wrs!]sw!Wwx!bx#O!W#O#P!i#P#o!W#o#p$c#p#q!W#q#r!b#r;'S!W;'S;=`%Q<%lO!W~!]OX~~!bO[~~!iOX~[~~!lYrs!W!P!Q!W#O#P!W#U#V!W#Y#Z!W#b#c!W#f#g!W#h#i!W#i#j#[#o#p$^~#_R!Q![#h!c!i#h#T#Z#h~#kR!Q![#t!c!i#t#T#Z#t~#wR!Q![$Q!c!i$Q#T#Z$Q~$TR!Q![!W!c!i!W#T#Z!W~$cOZ~~$jPX~[~#o#p$m~$rPR~#q#r$u~$xP#q#r${~%QOY~~%TP;=`<%l!W",tokenizers:[1,new Xl("#e~RVO#oh#o#p!P#p#qh#q#r#X#r;'Sh;'S;=`y<%lOh~mSS~O#qh#r;'Sh;'S;=`y<%lOh~|P;=`<%lh~!USS~O#q!b#r;'S!b;'S;=`#R<%lO!b~!gVS~O#O!b#O#P!b#P#q!b#q#r!|#r;'S!b;'S;=`#R<%lO!b~#ROS~~#UP;=`<%l!b~#[P#q#r#_~#dOT~~",112)],topRules:{MustacheLikeTemplate:[0,1]},tokenPrec:32}),_t=ii.define({parser:J2.configure({props:[Yl({"Template/LBrace":Be.quote,"Template/RBrace":Be.quote,"Template/Variable":Be.variableName,"Template/⚠":Be.invalid})]}),languageData:{}}),eu=({text:n,variables:a})=>ar({parser:_t.parser,text:n,variables:a,postFormat:t=>t.replaceAll("\\{{","{{")}),nu=n=>nr({parser:_t.parser,text:n});function au(){return new ri(_t)}const og=n=>{switch(n){case Ze.FString:return{format:q2,extractVariables:X2};case Ze.Mustache:return{format:eu,extractVariables:nu};case Ze.NONE:return{format:({text:a})=>a,extractVariables:()=>[]};default:P()}},tu=sn([q(),y1(),pn(),v1()]),ra=C1(()=>sn([tu,Ue(ra),tn(ra)])),hl=Z({type:k1(["string","number","boolean","object","array","null","integer"]).describe("The type of the parameter"),description:q().optional().describe("A description of the parameter"),enum:Ue(q()).optional().describe("The allowed values")}).passthrough().describe("A map of parameter names to their definitions"),Kt=Z({type:ce("object"),properties:tn(sn([hl,Z({anyOf:Ue(hl)}).describe("A list of possible parameter names to their definitions")])).optional(),required:Ue(q()).optional().describe("The required parameters"),additionalProperties:pn().optional().describe("Whether or not additional properties are allowed in the schema")}).passthrough(),Wn=Z({type:ce("function").describe("The type of the tool"),function:Z({name:q().describe("The name of the function"),description:q().optional().describe("A description of the function"),parameters:Kt.extend({strict:pn().optional().describe("Whether or not the arguments should exactly match the function definition, only supported for OpenAI models")}).describe("The parameters that the function accepts")}).passthrough().describe("The function definition")}).passthrough(),sg=Sn(Wn,{removeAdditionalStrategy:"passthrough"}),wa=Z({name:q(),description:q(),input_schema:Kt}),cg=Sn(wa,{removeAdditionalStrategy:"passthrough"}),Sa=Z({toolSpec:Z({name:q(),description:q().min(1),inputSchema:Z({json:Kt})})}),dg=Sn(Sa,{removeAdditionalStrategy:"passthrough"}),lu=Sa.transform(n=>({type:"function",function:{name:n.toolSpec.name,description:n.toolSpec.description,parameters:n.toolSpec.inputSchema.json}})),iu=Wn.transform(n=>({toolSpec:{name:n.function.name,description:n.function.description??n.function.name,inputSchema:{json:n.function.parameters}}})),ru=wa.transform(n=>({type:"function",function:{name:n.name,description:n.description,parameters:n.input_schema}})),ou=Wn.transform(n=>({name:n.function.name,description:n.function.description??n.function.name,input_schema:n.function.parameters})),tr=sn([Wn,wa,Sa,ra]),su=n=>{const{success:a,data:t}=Wn.safeParse(n);if(a)return{provider:"OPENAI",validatedToolDefinition:t};const{success:l,data:i}=wa.safeParse(n);if(l)return{provider:"ANTHROPIC",validatedToolDefinition:i};const{success:r,data:o}=Sa.safeParse(n);return r?{provider:"AWS",validatedToolDefinition:o}:{provider:"UNKNOWN",validatedToolDefinition:null}},Ha=n=>{const{provider:a,validatedToolDefinition:t}=su(n);switch(a){case"AZURE_OPENAI":case"OPENAI":return t;case"ANTHROPIC":return ru.parse(t);case"AWS":return lu.parse(t);case"UNKNOWN":return null;default:P()}},fl=({toolDefinition:n,targetProvider:a})=>{switch(a){case"AZURE_OPENAI":case"OPENAI":case"DEEPSEEK":case"XAI":case"OLLAMA":return n;case"ANTHROPIC":return ou.parse(n);case"AWS":return iu.parse(n);case"GOOGLE":return n;default:P()}};function ug(n){return{type:"function",function:{name:`new_function_${n}`,description:"a description",parameters:{type:"object",properties:{new_arg:{type:"string"}},required:[]}}}}function gg(n){return{name:`new_function_${n}`,description:"a description",input_schema:{type:"object",properties:{new_arg:{type:"string"}},required:[]}}}function mg(n){return{toolSpec:{name:`new_function_${n}`,description:"a description",inputSchema:{json:{type:"object",properties:{new_arg:{type:"string"}},required:[]}}}}}const pg=n=>{const a=tr.safeParse(n);return!a.success||a.data===null||!fe(a.data)?null:"function"in a.data&&fe(a.data.function)&&"name"in a.data.function&&typeof a.data.function.name=="string"?a.data.function.name:"name"in a.data&&typeof a.data.name=="string"?a.data.name:null},hg=n=>{const a=tr.safeParse(n);return!a.success||a.data===null||!fe(a.data)?null:"function"in a.data&&fe(a.data.function)&&"description"in a.data.function&&typeof a.data.function.description=="string"?a.data.function.description:"description"in a.data&&typeof a.data.description=="string"?a.data.description:null};function cu({str:n,excludePrimitives:a=!1,excludeArray:t=!1,excludeNull:l=!1}){try{const i=JSON.parse(n);if(a&&typeof i!="object"||t&&Array.isArray(i)||l&&i===null)return!1}catch{return!1}return!0}function du(n){return cu({str:n,excludeArray:!0,excludePrimitives:!0})}function xa(n){try{return{json:JSON.parse(n)}}catch(a){return{json:null,parseError:a}}}function fg(...n){try{return{json:JSON.stringify(...n)}}catch(a){return{json:null,stringifyError:a}}}function lr(n,a="",t="."){const l={};for(const[i,r]of Object.entries(n)){const o=a?`${a}${t}${i}`:i;r&&typeof r=="object"?Object.assign(l,lr(r,o,t)):l[o]=r}return l}function bg(n,a="."){try{const t=JSON.parse(n);return typeof t!="object"?{}:lr(t,"",a)}catch{}return{}}const qn=Z({id:q().describe("The ID of the tool call"),type:ce("function").describe("The type of the tool call").default("function"),function:Z({name:q().describe("The name of the function"),arguments:tn(Pn()).describe("The arguments for the function")}).describe("The function that is being called").passthrough()}),uu=Ue(qn),yg=Sn(uu,{removeAdditionalStrategy:"passthrough"}),Ta=Z({toolUse:Z({toolUseId:q().describe("The ID of the tool call"),name:q().describe("The name of the tool"),input:tn(Pn()).describe("The input for the tool")})}),gu=Ue(Ta),vg=Sn(gu,{removeAdditionalStrategy:"passthrough"}),mu=qn.transform(n=>({toolUse:{toolUseId:n.id,name:n.function.name,input:n.function.arguments}})),pu=Ta.transform(n=>({id:n.toolUse.toolUseId,type:"function",function:{name:n.toolUse.name,arguments:n.toolUse.input}})),Aa=Z({id:q().describe("The ID of the tool call"),type:ce("tool_use"),name:q().describe("The name of the tool"),input:tn(Pn()).describe("The input for the tool")}).passthrough(),hu=Ue(Aa),Cg=Sn(hu,{removeAdditionalStrategy:"passthrough"}),fu=Aa.transform(n=>({id:n.id,type:"function",function:{name:n.name,arguments:n.input}})),bu=qn.transform(n=>({id:n.id,type:"tool_use",name:n.function.name,input:typeof n.function.arguments=="string"?{[n.function.arguments]:n.function.arguments}:n.function.arguments??{}})),yu=sn([qn,Aa,Ta,ra]);Ue(yu);const vu=n=>{const{success:a,data:t}=qn.safeParse(n);if(a)return{provider:"OPENAI",validatedToolCall:t};const{success:l,data:i}=Aa.safeParse(n);if(l)return{provider:"ANTHROPIC",validatedToolCall:i};const{success:r,data:o}=Ta.safeParse(n);return r?{provider:"AWS",validatedToolCall:o}:{provider:"UNKNOWN",validatedToolCall:null}},an=n=>{const{provider:a,validatedToolCall:t}=vu(n);switch(a){case"AZURE_OPENAI":case"OPENAI":return t;case"ANTHROPIC":return fu.parse(t);case"AWS":return pu.parse(t);case"UNKNOWN":return null;default:P()}},rt=({toolCall:n,targetProvider:a})=>{switch(a){case"AZURE_OPENAI":case"OPENAI":case"DEEPSEEK":case"XAI":case"OLLAMA":return n;case"AWS":return mu.parse(n);case"ANTHROPIC":return bu.parse(n);case"GOOGLE":return n;default:P()}},kg=(n,a)=>{const t=an({id:n.toolCall.toolCallId,function:{name:n.toolCall.toolCall.name,arguments:xa(n.toolCall.toolCall.arguments).json||""}});return t?rt({toolCall:t,targetProvider:a}):null};function Lg(){return{id:"",type:"function",function:{name:"",arguments:{}}}}function wg(){return{id:"",type:"tool_use",name:"",input:{}}}const Pt=Z({id:q().optional(),name:q().optional(),arguments:tn(Pn()).optional(),function:Z({name:q().optional(),arguments:tn(Pn()).optional()}).optional()});function Sg(n){let a=n;typeof n=="string"&&(a=xa(n).json);const t=an(a);if(t)return t.id;const l=Pt.safeParse(a);return l.success?l.data.id??l.data.name??null:null}function xg(n){var i;let a=n;typeof n=="string"&&(a=xa(n).json);const t=an(a);if(t)return t.function.name;const l=Pt.safeParse(a);return l.success?((i=l.data.function)==null?void 0:i.name)??l.data.name??l.data.id??null:null}function Tg(n){var i;let a=n;typeof n=="string"&&(a=xa(n).json);const t=an(a);if(t)return t.function.arguments;const l=Pt.safeParse(a);return l.success?l.data.arguments??((i=l.data.function)==null?void 0:i.arguments)??null:null}const Ia=Qs()(sn([ce("auto"),ce("none"),ce("required"),Z({type:ce("function"),function:Z({name:q()})})]));Jl("type",[Z({type:ce("auto")}),Z({type:ce("any")}),Z({type:ce("tool"),name:q()}),Z({type:ce("none")})]);const Vt=Jl("type",[Z({type:ce("none")}),Z({type:ce("auto"),disable_parallel_tool_use:pn().optional()}),Z({type:ce("any"),disable_parallel_tool_use:pn().optional()}),Z({type:ce("tool"),name:q(),disable_parallel_tool_use:pn().optional()})]),Cu=Vt.transform(n=>{switch(n.type){case"any":return"required";case"auto":return"auto";case"tool":return n.name?{type:"function",function:{name:n.name}}:"auto";case"none":return"none";default:return"auto"}}),ku=Ia.transform(n=>{if(fe(n))return{type:"tool",name:n.function.name};switch(n){case"none":return{type:"none"};case"auto":return{type:"auto"};case"required":return{type:"any"};default:P()}}),Lu=Ia.transform(n=>{if(fe(n))return{type:"tool",name:n.function.name};switch(n){case"none":return{type:"none"};case"auto":return{type:"auto"};case"required":return{type:"any"};default:P()}});sn([Ia,Vt]);const wu=n=>{const{success:a,data:t}=Ia.safeParse(n);if(a)return{provider:"OPENAI",toolChoice:t};const{success:l,data:i}=Vt.safeParse(n);return l?{provider:"ANTHROPIC",toolChoice:i}:{provider:null,toolChoice:null}},Su=n=>{const{provider:a,toolChoice:t}=wu(n);if(a==null||t==null)throw new Error("Could not detect provider of tool choice");switch(a){case"AZURE_OPENAI":case"OPENAI":return t;case"ANTHROPIC":return Cu.parse(t);default:P()}},xu=({toolChoice:n,targetProvider:a})=>{switch(a){case"AZURE_OPENAI":case"OPENAI":case"DEEPSEEK":case"XAI":case"OLLAMA":return n;case"AWS":return ku.parse(n);case"ANTHROPIC":return Lu.parse(n);case"GOOGLE":return n;default:P()}},Tu=({toolChoice:n,targetProvider:a})=>{try{const t=Su(n);return xu({toolChoice:t,targetProvider:a})}catch{return null}},bl=n=>n,yl=n=>n,vl=n=>n,Au=n=>fe(n)?"function"in n&&fe(n.function)&&"name"in n.function&&typeof n.function.name=="string"?n.function.name:"name"in n&&typeof n.name=="string"?n.name:null:null,Iu=({instanceTools:n,provider:a})=>n.map(t=>{switch(a){case"OPENAI":case"DEEPSEEK":case"XAI":case"OLLAMA":case"AZURE_OPENAI":{const l=Ha(t.definition);return{...t,definition:l??t.definition}}case"ANTHROPIC":{const l=Ha(t.definition),i=l?fl({toolDefinition:l,targetProvider:a}):t.definition;return{...t,definition:i}}case"AWS":{const l=Ha(t.definition),i=l?fl({toolDefinition:l,targetProvider:a}):t.definition;return{...t,definition:i}}case"GOOGLE":return t;default:P()}}),zu=({toolCalls:n,provider:a})=>{if(n!=null)return n.map(t=>{switch(a){case"OPENAI":case"DEEPSEEK":case"XAI":case"OLLAMA":case"AZURE_OPENAI":return an(t)??t;case"ANTHROPIC":{const l=an(t);return l!=null?rt({toolCall:l,targetProvider:a}):t}case"AWS":{const l=an(t);return l!=null?rt({toolCall:l,targetProvider:a}):t}case"GOOGLE":return t;default:P()}})};let Mu=0,Fu=0,Eu=1,Du=0;const ir=()=>Mu++,oa=()=>Eu++,Ag=()=>Du++,_u=()=>Fu++,rr=()=>({__type:"chat",messages:[{id:oa(),role:"system",content:"You are a chatbot"},{id:oa(),role:"user",content:"{{question}}"}]}),Rt=n=>({template:{__type:"chat",messageIds:n.messages.map(a=>a.id)},messages:n.messages.reduce((a,t)=>(a[t.id]=t,a),{})}),Ku={__type:"text_completion",prompt:"{{question}}"},Pu=()=>({model:{provider:er,modelName:G2,invocationParameters:[],supportedInvocationParameters:[]},tools:[],toolChoice:"auto",output:void 0,spanId:null,activeRunId:null});function Vu(){const n=rr(),a=Rt(n);return{instance:{id:ir(),template:a.template,...Pu()},instanceMessages:a.messages}}function Ig(){return{type:"json_schema",json_schema:{name:"response",schema:{type:"object",properties:{},required:[],additionalProperties:!1},strict:!0}}}function Ru(n){if(n.instances!=null&&n.instances.length>0){let o={};return{instances:n.instances.map(d=>{if(d.template.__type==="chat"){const u=Rt(d.template);return o={...o,...u.messages},{...d,template:u.template}}return d}),instanceMessages:o}}const{instance:a,instanceMessages:t}=Vu(),l=Object.values(n.modelConfigByProvider);if(!(l.length>0))return{instances:[a],instanceMessages:t};const r=l.find(o=>o.provider===er)??l[0];return a.model={...a.model,...r},{instances:[a],instanceMessages:t}}const zg=n=>{const{instances:a,instanceMessages:t}=Ru(n);return wn(Bn((i,r)=>({streaming:!0,operationType:"chat",inputMode:"manual",dirtyInstances:{},input:{variablesValueCache:{}},templateFormat:Ze.Mustache,...n,instances:a,allInstanceMessages:t,setInput:o=>{i({input:o})},setOperationType:o=>{if(o==="chat"){const c=[];let d={};r().instances.forEach(u=>{const g=rr(),h=Rt(g);d={...d,...h.messages},c.push({...u,template:h.template})}),i({instances:c,allInstanceMessages:d})}else i({instances:r().instances.map(c=>({...c,template:Ku}))});i({operationType:o})},addInstance:()=>{const o=r().instances,c=r().allInstanceMessages,d=r().instances[0];if(!d)return;let u=[],g={};if(d.template.__type==="chat"){const f=d.template.messageIds.map(b=>c[b]).map(b=>({...b,id:oa()}));u=f.map(b=>b.id),g=f.reduce((b,y)=>(b[y.id]=y,b),{})}i({allInstanceMessages:{...c,...g},instances:[...o,{...d,...d.template.__type==="chat"?{template:{...d.template,messageIds:u}}:{},id:ir(),activeRunId:null,experimentId:null,spanId:null}]})},updateModelSupportedInvocationParameters:({instanceId:o,supportedInvocationParameters:c,modelConfigByProvider:d})=>{const u=r().instances;i({instances:u.map(g=>{if(g.id===o){const{baseUrl:h,endpoint:f,apiVersion:b,region:y}=d[g.model.provider]??{},v=ys(g.model.invocationParameters,c),k=vs(v,c);return{...g,model:{...g.model,baseUrl:g.model.baseUrl??h,endpoint:g.model.endpoint??f,apiVersion:g.model.apiVersion??b,region:g.model.region??y,supportedInvocationParameters:c,invocationParameters:k},tools:c.find(L=>L.canonicalName===Cs)?g.tools:[]}}return g})})},updateProvider:({instanceId:o,provider:c,modelConfigByProvider:d})=>{const u=r().instances,g=u.find(k=>k.id===o);if(!g||g.model.provider===c)return;const h=d[c],f=g.model.invocationParameters.find(k=>k.canonicalName===fs||k.invocationName===bs),b=k=>k==="OLLAMA"?"http://localhost:11434/v1":null,y={model:h?{...g.model,...h,invocationParameters:[...h.invocationParameters,...f?[f]:[]],provider:c}:{...g.model,modelName:null,baseUrl:b(c),apiVersion:null,endpoint:null,region:null,provider:c},toolChoice:Tu({toolChoice:g.toolChoice,targetProvider:c})??void 0,tools:Iu({instanceTools:g.tools,provider:c})},v={};g.template.__type==="chat"&&g.template.messageIds.forEach(k=>{const L=r().allInstanceMessages[k];L&&(v[k]={...L,toolCalls:zu({toolCalls:L.toolCalls,provider:c})})}),i({allInstanceMessages:{...r().allInstanceMessages,...v},dirtyInstances:{...r().dirtyInstances,[o]:!0},instances:u.map(k=>k.id===o?{...k,...y}:k)})},updateModel:({instanceId:o,patch:c})=>{const d=r().instances;d.find(g=>g.id===o)&&i({dirtyInstances:{...r().dirtyInstances,[o]:!0},instances:d.map(g=>g.id===o?{...g,model:{...g.model,...c}}:g)})},deleteInstance:o=>{const c=r().instances;i({instances:c.filter(d=>d.id!==o),dirtyInstances:{...r().dirtyInstances,[o]:!1}})},addMessage:({playgroundInstanceId:o,messages:c})=>{const d=r().instances;let u=[];Array.isArray(c)?u=c:c?u=[c]:u=[{id:oa(),role:Q2,content:""}],i({allInstanceMessages:{...r().allInstanceMessages,...u.reduce((g,h)=>(g[h.id]=h,g),{})},dirtyInstances:{...r().dirtyInstances,[o]:!0},instances:d.map(g=>g.id===o&&(g!=null&&g.template)&&(g==null?void 0:g.template.__type)==="chat"?{...g,template:{...g.template,messageIds:[...g.template.messageIds,...u.map(h=>h.id)]}}:g)})},updateMessage:({messageId:o,patch:c,instanceId:d})=>{const u=r().allInstanceMessages;i({allInstanceMessages:{...u,[o]:{...u[o],...c}},dirtyInstances:{...r().dirtyInstances,[d]:!0}})},deleteMessage:({instanceId:o,messageId:c})=>{const d=r().instances,u=r().allInstanceMessages;i({allInstanceMessages:Object.fromEntries(Object.entries(u).filter(([,{id:g}])=>g!==c)),dirtyInstances:{...r().dirtyInstances,[o]:!0},instances:d.map(g=>g.id===o&&(g!=null&&g.template)&&(g==null?void 0:g.template.__type)==="chat"?{...g,template:{...g.template,messageIds:g.template.messageIds.filter(h=>h!==c)}}:g)})},updateInstance:({instanceId:o,patch:c,dirty:d})=>{const u=r().instances;i({dirtyInstances:{...r().dirtyInstances,...d!=null?{[o]:d}:{}},instances:u.map(g=>g.id===o?{...g,...c}:g)})},runPlaygroundInstances:()=>{const o=r().instances;i({instances:o.map(c=>({...c,activeRunId:_u(),spanId:null}))})},cancelPlaygroundInstances:()=>{const o=r().instances;i({instances:o.map(c=>({...c,activeRunId:null,spanId:null}))})},markPlaygroundInstanceComplete:o=>{const c=r().instances;i({instances:c.map(d=>d.id===o?{...d,activeRunId:null}:d)})},setTemplateFormat:o=>{i({templateFormat:o})},setVariableValue:(o,c)=>{const d=r().input;i({input:{...d,variablesValueCache:{...d.variablesValueCache,[o]:c}}})},setStreaming:o=>{i({streaming:o})},updateInstanceModelInvocationParameters:({instanceId:o,invocationParameters:c})=>{r().instances.find(u=>u.id===o)&&i({dirtyInstances:{...r().dirtyInstances,[o]:!0},instances:r().instances.map(u=>u.id===o?{...u,model:{...u.model,invocationParameters:c}}:u)})},upsertInvocationParameterInput:({instanceId:o,invocationParameterInput:c})=>{const d=r().instances.find(g=>g.id===o);if(!d)return;const u=d.model.invocationParameters.find(g=>Jt(g,c));i(u?{dirtyInstances:{...r().dirtyInstances,[o]:!0},instances:r().instances.map(g=>g.id===o?{...g,model:{...g.model,invocationParameters:g.model.invocationParameters.map(h=>Jt(h,c)?c:h)}}:g)}:{dirtyInstances:{...r().dirtyInstances,[o]:!0},instances:r().instances.map(g=>g.id===o?{...g,model:{...g.model,invocationParameters:[...g.model.invocationParameters,c]}}:g)})},deleteInvocationParameterInput:({instanceId:o,invocationParameterInputInvocationName:c})=>{r().instances.find(u=>u.id===o)&&i({dirtyInstances:{...r().dirtyInstances,[o]:!0},instances:r().instances.map(u=>u.id===o?{...u,model:{...u.model,invocationParameters:u.model.invocationParameters.filter(g=>g.invocationName!==c)}}:u)})},setDirty:(o,c)=>{i({dirtyInstances:{...r().dirtyInstances,[o]:c}})}})))};function Ou(n){return n==="OPENAI"||n==="AZURE_OPENAI"||n==="ANTHROPIC"||n==="GOOGLE"||n==="DEEPSEEK"||n==="XAI"||n==="OLLAMA"||n==="AWS"}function Mg(n){switch(n){case"OPENAI":return"OpenAI";case"AZURE_OPENAI":return"Azure OpenAI";case"ANTHROPIC":return"Anthropic";case"GOOGLE":return"Google";case"DEEPSEEK":return"DeepSeek";case"XAI":return"XAI";case"OLLAMA":return"Ollama";case"AWS":return"AWS";default:P()}}function Fg(n){switch(n){case"OPENAI":return An.OPENAI.toString();case"AZURE_OPENAI":return An.AZURE.toString();case"ANTHROPIC":return An.ANTHROPIC.toString();case"GOOGLE":return An.GOOGLE.toString();case"AWS":return An.AWS.toString();case"DEEPSEEK":return"deepseek";case"XAI":return"xai";case"OLLAMA":throw new Error("Ollama is not supported");default:P()}}function Nu(n){return typeof n=="object"&&n!==null&&Object.keys(n).length>0&&Object.keys(n).every(a=>a in it)&&Object.values(n).every(a=>typeof a=="string")}function $u(n){const a={};for(const t of Object.keys(n))Ou(t)&&it[t].length===1&&(a[t]={[it[t][0].envVarName]:n[t]});return a}const Eg=n=>{const a=t=>({setCredential:({provider:l,envVarName:i,value:r})=>{t(o=>({[l]:{...o[l],[i]:r}}))},...n});return wn()(ga(Bn(a),{version:1,name:"arize-phoenix-credentials",migrate:t=>{if(Nu(t))return $u(t)}}))},sa={OPENAI:["required","auto","none"],AZURE_OPENAI:["required","auto","none"],DEEPSEEK:["required","auto","none"],XAI:["required","auto","none"],OLLAMA:["required","auto","none"],ANTHROPIC:["any","auto","none"],AWS:["any","auto","none"]},Bu=(n,a)=>{switch(n){case"AZURE_OPENAI":case"DEEPSEEK":case"XAI":case"OLLAMA":case"OPENAI":return fe(a)&&"type"in a&&typeof a.type=="string"?a.type:a;case"AWS":return fe(a)&&"type"in a&&typeof a.type=="string"?a.type:a;case"ANTHROPIC":return fe(a)&&"type"in a&&typeof a.type=="string"?a.type:a;case"GOOGLE":return"auto";default:P()}},Dg=n=>n in sa,Cl=(n,a)=>{var t;return((t=sa[n])==null?void 0:t.includes(a))??!1},ca="tool_",ja=n=>`${ca}${n}`,Za=n=>n.startsWith(ca)?n.slice(ca.length):n,Hu=({choiceType:n})=>{switch(n){case"any":case"required":return s(S,{gap:"size-100",alignItems:"center",justifyContent:"space-between",width:"100%",children:[e("span",{children:"Use at least one tool"}),e(je,{color:"var(--ac-global-color-grey-900)",size:"S",children:n})]});case"none":return s(S,{gap:"size-100",alignItems:"center",justifyContent:"space-between",width:"100%",children:[e("span",{children:"Don't use any tools"}),e(je,{color:"var(--ac-global-color-grey-900)",size:"S",children:n})]});case"auto":default:return s(S,{gap:"size-100",alignItems:"center",justifyContent:"space-between",width:"100%",children:[e("span",{children:"Tools auto-selected by LLM"}),e(je,{color:"var(--ac-global-color-grey-900)",size:"S",children:n})]})}};function _g({choice:n,onChange:a,toolNames:t,provider:l}){const i=Bu(l,n),o=Cl(l,i)?i:ja(Au(n)??"");return s(Ne,{selectedKey:o,"aria-label":"Tool Choice for an LLM",onSelectionChange:c=>{if(typeof c=="string"){if(c.startsWith(ca))switch(l){case"AZURE_OPENAI":case"DEEPSEEK":case"XAI":case"OLLAMA":case"OPENAI":a(bl({type:"function",function:{name:Za(c)}}));break;case"AWS":a(vl({type:"tool",name:Za(c)}));break;case"ANTHROPIC":a(yl({type:"tool",name:Za(c)}));break;default:P()}else if(Cl(l,c))switch(l){case"AZURE_OPENAI":case"DEEPSEEK":case"XAI":case"OLLAMA":case"OPENAI":a(bl(c));break;case"AWS":a(vl({type:c}));break;case"ANTHROPIC":a(yl({type:c}));break;default:P()}}},children:[e(K,{children:"Tool Choice"}),s(z,{children:[e(Oe,{}),e(Ae,{})]}),e(ue,{children:e(we,{children:[...sa[l]?sa[l].map(c=>e(ee,{id:c,textValue:c,children:e(Hu,{choiceType:c})},c)):[],...t.map(c=>e(ee,{id:ja(c),textValue:c,children:c},ja(c)))]})})]})}const ju=({height:n})=>s("svg",{viewBox:"0 0 24 24",width:n,height:n,xmlns:"http://www.w3.org/2000/svg",children:[e("title",{children:"Azure"}),e("path",{d:"M11.49 2H2v9.492h9.492V2h-.002z",fill:"#F25022"}),e("path",{d:"M22 2h-9.492v9.492H22V2z",fill:"#7FBA00"}),e("path",{d:"M11.49 12.508H2V22h9.492v-9.492h-.002z",fill:"#00A4EF"}),e("path",{d:"M22 12.508h-9.492V22H22v-9.492z",fill:"#FFB900"})]}),Zu=({height:n})=>s("svg",{viewBox:"0 0 24 24",width:n,height:n,xmlns:"http://www.w3.org/2000/svg",children:[e("title",{children:"Google"}),e("defs",{children:s("linearGradient",{id:"lobe-icons-google-fill",x1:"0%",x2:"68.73%",y1:"100%",y2:"30.395%",children:[e("stop",{offset:"0%",stopColor:"#1C7DFF"}),e("stop",{offset:"52.021%",stopColor:"#1C69FF"}),e("stop",{offset:"100%",stopColor:"#F0DCD6"})]})}),e("path",{d:"M12 24A14.304 14.304 0 000 12 14.304 14.304 0 0012 0a14.305 14.305 0 0012 12 14.305 14.305 0 00-12 12",fill:"url(#lobe-icons-google-fill)",fillRule:"nonzero"})]}),Uu=({height:n})=>s("svg",{fill:"var(--ac-global-text-color-900)",fillRule:"evenodd",viewBox:"0 0 24 24",width:n,height:n,xmlns:"http://www.w3.org/2000/svg",children:[e("title",{children:"OpenAI"}),e("path",{d:"M21.55 10.004a5.416 5.416 0 00-.478-4.501c-1.217-2.09-3.662-3.166-6.05-2.66A5.59 5.59 0 0010.831 1C8.39.995 6.224 2.546 5.473 4.838A5.553 5.553 0 001.76 7.496a5.487 5.487 0 00.691 6.5 5.416 5.416 0 00.477 4.502c1.217 2.09 3.662 3.165 6.05 2.66A5.586 5.586 0 0013.168 23c2.443.006 4.61-1.546 5.361-3.84a5.553 5.553 0 003.715-2.66 5.488 5.488 0 00-.693-6.497v.001zm-8.381 11.558a4.199 4.199 0 01-2.675-.954c.034-.018.093-.05.132-.074l4.44-2.53a.71.71 0 00.364-.623v-6.176l1.877 1.069c.02.01.033.029.036.05v5.115c-.003 2.274-1.87 4.118-4.174 4.123zM4.192 17.78a4.059 4.059 0 01-.498-2.763c.032.02.09.055.131.078l4.44 2.53c.225.13.504.13.73 0l5.42-3.088v2.138a.068.068 0 01-.027.057L9.9 19.288c-1.999 1.136-4.552.46-5.707-1.51h-.001zM3.023 8.216A4.15 4.15 0 015.198 6.41l-.002.151v5.06a.711.711 0 00.364.624l5.42 3.087-1.876 1.07a.067.067 0 01-.063.005l-4.489-2.559c-1.995-1.14-2.679-3.658-1.53-5.63h.001zm15.417 3.54l-5.42-3.088L14.896 7.6a.067.067 0 01.063-.006l4.489 2.557c1.998 1.14 2.683 3.662 1.529 5.633a4.163 4.163 0 01-2.174 1.807V12.38a.71.71 0 00-.363-.623zm1.867-2.773a6.04 6.04 0 00-.132-.078l-4.44-2.53a.731.731 0 00-.729 0l-5.42 3.088V7.325a.068.068 0 01.027-.057L14.1 4.713c2-1.137 4.555-.46 5.707 1.513.487.833.664 1.809.499 2.757h.001zm-11.741 3.81l-1.877-1.068a.065.065 0 01-.036-.051V6.559c.001-2.277 1.873-4.122 4.181-4.12.976 0 1.92.338 2.671.954-.034.018-.092.05-.131.073l-4.44 2.53a.71.71 0 00-.365.623l-.003 6.173v.002zm1.02-2.168L12 9.25l2.414 1.375v2.75L12 14.75l-2.415-1.375v-2.75z"})]}),Gu=({height:n})=>s("svg",{fill:"var(--ac-global-text-color-900)",fillRule:"evenodd",viewBox:"0 0 24 24",width:n,height:n,xmlns:"http://www.w3.org/2000/svg",children:[e("title",{children:"Anthropic"}),e("path",{d:"M13.827 3.52h3.603L24 20h-3.603l-6.57-16.48zm-7.258 0h3.767L16.906 20h-3.674l-1.343-3.461H5.017l-1.344 3.46H0L6.57 3.522zm4.132 9.959L8.453 7.687 6.205 13.48H10.7z"})]}),Qu=({height:n})=>s("svg",{viewBox:"0 0 24 24",width:n,height:n,xmlns:"http://www.w3.org/2000/svg",children:[e("title",{children:"DeepSeek"}),e("path",{d:"M23.748 4.482c-.254-.124-.364.113-.512.234-.051.039-.094.09-.137.136-.372.397-.806.657-1.373.626-.829-.046-1.537.214-2.163.848-.133-.782-.575-1.248-1.247-1.548-.352-.156-.708-.311-.955-.65-.172-.241-.219-.51-.305-.774-.055-.16-.11-.323-.293-.35-.2-.031-.278.136-.356.276-.313.572-.434 1.202-.422 1.84.027 1.436.633 2.58 1.838 3.393.137.093.172.187.129.323-.082.28-.18.552-.266.833-.055.179-.137.217-.329.14a5.526 5.526 0 01-1.736-1.18c-.857-.828-1.631-1.742-2.597-2.458a11.365 11.365 0 00-.689-.471c-.985-.957.13-1.743.388-1.836.27-.098.093-.432-.779-.428-.872.004-1.67.295-2.687.684a3.055 3.055 0 01-.465.137 9.597 9.597 0 00-2.883-.102c-1.885.21-3.39 1.102-4.497 2.623C.082 8.606-.231 10.684.152 12.85c.403 2.284 1.569 4.175 3.36 5.653 1.858 1.533 3.997 2.284 6.438 2.14 1.482-.085 3.133-.284 4.994-1.86.47.234.962.327 1.78.397.63.059 1.236-.03 1.705-.128.735-.156.684-.837.419-.961-2.155-1.004-1.682-.595-2.113-.926 1.096-1.296 2.746-2.642 3.392-7.003.05-.347.007-.565 0-.845-.004-.17.035-.237.23-.256a4.173 4.173 0 001.545-.475c1.396-.763 1.96-2.015 2.093-3.517.02-.23-.004-.467-.247-.588zM11.581 18c-2.089-1.642-3.102-2.183-3.52-2.16-.392.024-.321.471-.235.763.09.288.207.486.371.739.114.167.192.416-.113.603-.673.416-1.842-.14-1.897-.167-1.361-.802-2.5-1.86-3.301-3.307-.774-1.393-1.224-2.887-1.298-4.482-.02-.386.093-.522.477-.592a4.696 4.696 0 011.529-.039c2.132.312 3.946 1.265 5.468 2.774.868.86 1.525 1.887 2.202 2.891.72 1.066 1.494 2.082 2.48 2.914.348.292.625.514.891.677-.802.09-2.14.11-3.054-.614zm1-6.44a.306.306 0 01.415-.287.302.302 0 01.2.288.306.306 0 01-.31.307.303.303 0 01-.304-.308zm3.11 1.596c-.2.081-.399.151-.59.16a1.245 1.245 0 01-.798-.254c-.274-.23-.47-.358-.552-.758a1.73 1.73 0 01.016-.588c.07-.327-.008-.537-.239-.727-.187-.156-.426-.199-.688-.199a.559.559 0 01-.254-.078c-.11-.054-.2-.19-.114-.358.028-.054.16-.186.192-.21.356-.202.767-.136 1.146.016.352.144.618.408 1.001.782.391.451.462.576.685.914.176.265.336.537.445.848.067.195-.019.354-.25.452z",fill:"#4D6BFE"})]}),Wu=({height:n})=>s("svg",{fill:"var(--ac-global-text-color-900)",fillRule:"evenodd",viewBox:"0 0 24 24",width:n,height:n,xmlns:"http://www.w3.org/2000/svg",children:[e("title",{children:"xAI"}),e("path",{d:"M6.469 8.776L16.512 23h-4.464L2.005 8.776H6.47zm-.004 7.9l2.233 3.164L6.467 23H2l4.465-6.324zM22 2.582V23h-3.659V7.764L22 2.582zM22 1l-9.952 14.095-2.233-3.163L17.533 1H22z"})]}),qu=({height:n})=>s("svg",{fill:"currentColor",fillRule:"evenodd",height:n,style:{flex:"none",lineHeight:1},viewBox:"0 0 24 24",width:n,xmlns:"http://www.w3.org/2000/svg",children:[e("title",{children:"Ollama"}),e("path",{d:"M7.905 1.09c.216.085.411.225.588.41.295.306.544.744.734 1.263.191.522.315 1.1.362 1.68a5.054 5.054 0 012.049-.636l.051-.004c.87-.07 1.73.087 2.48.474.101.053.2.11.297.17.05-.569.172-1.134.36-1.644.19-.52.439-.957.733-1.264a1.67 1.67 0 01.589-.41c.257-.1.53-.118.796-.042.401.114.745.368 1.016.737.248.337.434.769.561 1.287.23.934.27 2.163.115 3.645l.053.04.026.019c.757.576 1.284 1.397 1.563 2.35.435 1.487.216 3.155-.534 4.088l-.018.021.002.003c.417.762.67 1.567.724 2.4l.002.03c.064 1.065-.2 2.137-.814 3.19l-.007.01.01.024c.472 1.157.62 2.322.438 3.486l-.006.039a.651.651 0 01-.747.536.648.648 0 01-.54-.742c.167-1.033.01-2.069-.48-3.123a.643.643 0 01.04-.617l.004-.006c.604-.924.854-1.83.8-2.72-.046-.779-.325-1.544-.8-2.273a.644.644 0 01.18-.886l.009-.006c.243-.159.467-.565.58-1.12a4.229 4.229 0 00-.095-1.974c-.205-.7-.58-1.284-1.105-1.683-.595-.454-1.383-.673-2.38-.61a.653.653 0 01-.632-.371c-.314-.665-.772-1.141-1.343-1.436a3.288 3.288 0 00-1.772-.332c-1.245.099-2.343.801-2.67 1.686a.652.652 0 01-.61.425c-1.067.002-1.893.252-2.497.703-.522.39-.878.935-1.066 1.588a4.07 4.07 0 00-.068 1.886c.112.558.331 1.02.582 1.269l.008.007c.212.207.257.53.109.785-.36.622-.629 1.549-.673 2.44-.05 1.018.186 1.902.719 2.536l.016.019a.643.643 0 01.095.69c-.576 1.236-.753 2.252-.562 3.052a.652.652 0 01-1.269.298c-.243-1.018-.078-2.184.473-3.498l.014-.035-.008-.012a4.339 4.339 0 01-.598-1.309l-.005-.019a5.764 5.764 0 01-.177-1.785c.044-.91.278-1.842.622-2.59l.012-.026-.002-.002c-.293-.418-.51-.953-.63-1.545l-.005-.024a5.352 5.352 0 01.093-2.49c.262-.915.777-1.701 1.536-2.269.06-.045.123-.09.186-.132-.159-1.493-.119-2.73.112-3.67.127-.518.314-.95.562-1.287.27-.368.614-.622 1.015-.737.266-.076.54-.059.797.042zm4.116 9.09c.936 0 1.8.313 2.446.855.63.527 1.005 1.235 1.005 1.94 0 .888-.406 1.58-1.133 2.022-.62.375-1.451.557-2.403.557-1.009 0-1.871-.259-2.493-.734-.617-.47-.963-1.13-.963-1.845 0-.707.398-1.417 1.056-1.946.668-.537 1.55-.849 2.485-.849zm0 .896a3.07 3.07 0 00-1.916.65c-.461.37-.722.835-.722 1.25 0 .428.21.829.61 1.134.455.347 1.124.548 1.943.548.799 0 1.473-.147 1.932-.426.463-.28.7-.686.7-1.257 0-.423-.246-.89-.683-1.256-.484-.405-1.14-.643-1.864-.643zm.662 1.21l.004.004c.12.151.095.37-.056.49l-.292.23v.446a.375.375 0 01-.376.373.375.375 0 01-.376-.373v-.46l-.271-.218a.347.347 0 01-.052-.49.353.353 0 01.494-.051l.215.172.22-.174a.353.353 0 01.49.051zm-5.04-1.919c.478 0 .867.39.867.871a.87.87 0 01-.868.871.87.87 0 01-.867-.87.87.87 0 01.867-.872zm8.706 0c.48 0 .868.39.868.871a.87.87 0 01-.868.871.87.87 0 01-.867-.87.87.87 0 01.867-.872zM7.44 2.3l-.003.002a.659.659 0 00-.285.238l-.005.006c-.138.189-.258.467-.348.832-.17.692-.216 1.631-.124 2.782.43-.128.899-.208 1.404-.237l.01-.001.019-.034c.046-.082.095-.161.148-.239.123-.771.022-1.692-.253-2.444-.134-.364-.297-.65-.453-.813a.628.628 0 00-.107-.09L7.44 2.3zm9.174.04l-.002.001a.628.628 0 00-.107.09c-.156.163-.32.45-.453.814-.29.794-.387 1.776-.23 2.572l.058.097.008.014h.03a5.184 5.184 0 011.466.212c.086-1.124.038-2.043-.128-2.722-.09-.365-.21-.643-.349-.832l-.004-.006a.659.659 0 00-.285-.239h-.004z"})]}),Xu=({height:n})=>s("svg",{height:n,style:{flex:"none",lineHeight:1},viewBox:"0 0 24 24",width:n,xmlns:"http://www.w3.org/2000/svg",children:[e("title",{children:"Bedrock"}),e("defs",{children:s("linearGradient",{id:"lobe-icons-bedrock-fill",x1:"80%",x2:"20%",y1:"20%",y2:"80%",children:[e("stop",{offset:"0%",stopColor:"#6350FB"}),e("stop",{offset:"50%",stopColor:"#3D8FFF"}),e("stop",{offset:"100%",stopColor:"#9AD8F8"})]})}),e("path",{d:"M13.05 15.513h3.08c.214 0 .389.177.389.394v1.82a1.704 1.704 0 011.296 1.661c0 .943-.755 1.708-1.685 1.708-.931 0-1.686-.765-1.686-1.708 0-.807.554-1.484 1.297-1.662v-1.425h-2.69v4.663a.395.395 0 01-.188.338l-2.69 1.641a.385.385 0 01-.405-.002l-4.926-3.086a.395.395 0 01-.185-.336V16.3L2.196 14.87A.395.395 0 012 14.555L2 14.528V9.406c0-.14.073-.27.192-.34l2.465-1.462V4.448c0-.129.062-.249.165-.322l.021-.014L9.77 1.058a.385.385 0 01.407 0l2.69 1.675a.395.395 0 01.185.336V7.6h3.856V5.683a1.704 1.704 0 01-1.296-1.662c0-.943.755-1.708 1.685-1.708.931 0 1.685.765 1.685 1.708 0 .807-.553 1.484-1.296 1.662v2.311a.391.391 0 01-.389.394h-4.245v1.806h6.624a1.69 1.69 0 011.64-1.313c.93 0 1.685.764 1.685 1.707 0 .943-.754 1.708-1.685 1.708a1.69 1.69 0 01-1.64-1.314H13.05v1.937h4.953l.915 1.18a1.66 1.66 0 01.84-.227c.931 0 1.685.764 1.685 1.707 0 .943-.754 1.708-1.685 1.708-.93 0-1.685-.765-1.685-1.708 0-.346.102-.668.276-.937l-.724-.935H13.05v1.806zM9.973 1.856L7.93 3.122V6.09h-.778V3.604L5.435 4.669v2.945l2.11 1.36L9.712 7.61V5.334h.778V7.83c0 .136-.07.263-.184.335L7.963 9.638v2.081l1.422 1.009-.446.646-1.406-.998-1.53 1.005-.423-.66 1.605-1.055v-1.99L5.038 8.29l-2.26 1.34v1.676l1.972-1.189.398.677-2.37 1.429V14.3l2.166 1.258 2.27-1.368.397.677-2.176 1.311V19.3l1.876 1.175 2.365-1.426.398.678-2.017 1.216 1.918 1.201 2.298-1.403v-5.78l-4.758 2.893-.4-.675 5.158-3.136V3.289L9.972 1.856zM16.13 18.47a.913.913 0 00-.908.92c0 .507.406.918.908.918a.913.913 0 00.907-.919.913.913 0 00-.907-.92zm3.63-3.81a.913.913 0 00-.908.92c0 .508.406.92.907.92a.913.913 0 00.908-.92.913.913 0 00-.908-.92zm1.555-4.99a.913.913 0 00-.908.92c0 .507.407.918.908.918a.913.913 0 00.907-.919.913.913 0 00-.907-.92zM17.296 3.1a.913.913 0 00-.907.92c0 .508.406.92.907.92a.913.913 0 00.908-.92.913.913 0 00-.908-.92z",fill:"url(#lobe-icons-bedrock-fill)",fillRule:"nonzero"})]}),Yu={AZURE_OPENAI:ju,GOOGLE:Zu,OPENAI:Uu,ANTHROPIC:Gu,DEEPSEEK:Qu,XAI:Wu,OLLAMA:qu,AWS:Xu};function Kg({provider:n,height:a=18}){return Yu[n]({height:a})}const Ot=m`
  // fixes table row sizing issues with full height cell children
  // this enables features like hovering anywhere on a cell to display controls
  height: fit-content;
  font-size: var(--ac-global-font-size-s);
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  thead {
    position: sticky;
    top: 0;
    z-index: 1;
    tr {
      th {
        padding: var(--ac-global-dimension-size-100)
          var(--ac-global-dimension-size-200);
        background-color: var(--ac-global-color-grey-100);
        position: relative;
        text-align: left;
        user-select: none;
        vertical-align: top;
        font-weight: 600;
        font-size: var(--ac-global-font-size-s);
        line-height: var(--ac-global-line-height-s);
        border-bottom: 1px solid var(--ac-global-border-color-default);
        &:not(:last-of-type) {
          border-right: 1px solid var(--ac-global-border-color-default);
        }
        .sort {
          /* The sortable part of the header */
          cursor: pointer;
          display: flex;
          flex-direction: row;
          align-items: center;

          gap: var(--ac-global-dimension-size-50);
        }
        .sort-icon {
          margin-left: var(--ac-global-dimension-size-50);
          font-size: var(--ac-global-font-size-xs);
          vertical-align: middle;
          display: inline-block;
        }
        &:hover .resizer {
          background: var(--ac-global-color-grey-300);
        }
        div.resizer {
          display: inline-block;

          width: 2px;
          height: 100%;
          position: absolute;
          right: 0;
          top: 0;
          cursor: grab;
          z-index: 4;
          touch-action: none;
          &.isResizing,
          &:hover {
            background: var(--ac-global-color-primary);
          }
        }
        // Style action menu buttons in the header
        .ac-button[data-size="compact"][data-childless="true"] {
          padding: 0;
          border: none;
          background-color: transparent;
        }
      }
    }
  }
  tbody:not(.is-empty) {
    tr {
      // when paired with table.height:fit-content, allows table cells and their children to fill entire row height
      height: 100%;
      &:not(:last-of-type) {
        & > td {
          border-bottom: 1px solid var(--ac-global-border-color-default);
        }
      }
      & > td {
        padding: var(--ac-global-dimension-size-100)
          var(--ac-global-dimension-size-200);
      }
      &[data-selected="true"] {
        background-color: var(--ac-global-color-primary-100);
      }
    }
  }
`,Pg=m`
  tbody:not(.is-empty) {
    tr {
      & > td {
        border-bottom: 1px solid var(--ac-global-border-color-default);
      }
      & > td:not(:last-of-type) {
        border-right: 1px solid var(--ac-global-border-color-default);
      }
    }
  }
`,Ju=m`
  tbody:not(.is-empty) {
    tr {
      &:hover {
        background-color: var(--ac-hover-background);
      }
    }
  }
`,Vg=m(Ot,Ju,m`
    tbody:not(.is-empty) {
      tr {
        cursor: pointer;
      }
    }
  `),e3=m`
  display: flex;
  justify-content: flex-end;
  align-items: center;
  padding: var(--ac-global-dimension-size-100);
  gap: var(--ac-global-dimension-size-50);
  border-top: 1px solid var(--ac-global-color-grey-300);
`;function Rg(n){const a=n.getIsPinned(),t=a==="left"&&n.getIsLastColumn("left"),l=a==="right"&&n.getIsFirstColumn("right");return{boxShadow:t?"-8px 0 8px -8px var(--ac-global-color-grey-200) inset":l?"8px 0 8px -8px var(--ac-global-color-grey-200) inset":void 0,left:a==="left"?`${n.getStart("left")}px`:void 0,right:a==="right"?`${n.getAfter("right")}px`:void 0,opacity:a?.95:1,position:a?"sticky":"relative",width:n.getSize(),zIndex:a?1:0,backgroundColor:a?"var(--ac-global-color-grey-100)":void 0}}const kl=.05,n3=({word:n,theme:a})=>{const t=n.charCodeAt(0);let l=ei(t%26/26);const i=a==="light"?3:5,r=a==="light"?"#fdfdfd":"#0E0E0E";let o=qt(l,r);for(;o<i;)l=a==="light"?L1(kl,l):ni(kl,l),o=qt(l,r);return l},or=n=>{const{theme:a}=le();return p.useMemo(()=>n3({word:n,theme:a}),[n,a])};function Nt({annotationName:n,...a}){const t=or(n);return e(me,{color:t,...a})}const ot=1e3,st=60*ot,ct=60*st,a3=24*ct,Og=30*a3,Ng=3600*24*365,$g=3600*24*30,Bg=3600*24*7,Hg=3600*24,jg=3600;function sr(n){return Math.abs(n)<1e6?he(",")(n):he("0.2s")(n).replace("G","B").replace("k","K")}function t3(n){return he("0.2s")(n).replace("G","B").replace("k","K")}function We(n){const a=Math.abs(n);return a===0?"0.00":a<.01?he(".2e")(n):a<1e3?he("0.2f")(n):he("0.2s")(n)}function l3(n){const a=Math.abs(n);return a===0?"0.00":a<.01?he(".2e")(n):a<1e3?he("0.2f")(n):he("0.2s")(n).replace("G","B").replace("k","K")}function i3(n){return he(".2f")(n)+"%"}function On(n){return Number.isInteger(n)?sr(n):We(n)}function r3(n){return n===0?"$0":n<.01?"<$0.01":n<100?`$${he("0.2f")(n)}`:n<1e4?`$${he(",")(n)}`:`$${he("0.2s")(n).replace("G","B").replace("k","K")}`}function o3(n){const a=Math.floor(n/ct),t=Math.floor(n%ct/st),l=Math.floor(n%st/ot),i=Math.floor(n%ot);if(a>0)return`${a}h${t?` ${t}m`:""}${l?` ${l}s`:""}`;if(t>0)return`${t}m${l?` ${l}s`:""}`;if(l>0){const r=Math.floor(i/100);return`${l}${r>0?`.${r.toFixed(0)}`:""}s`}return`${i.toFixed(0)}ms`}function qe(n){return a=>typeof a!="number"?"--":n(a)}const s3=qe(sr),Zg=qe(t3),Ug=qe(l3),cr=qe(We),Ll=qe(On),c3=qe(i3),dr=qe(r3),Gg=qe(o3),wl=m`
  display: flex;
  align-items: center;
  .ac-text {
    display: inline-block;
    max-width: 9rem;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
`,d3=({annotation:n,displayPreference:a})=>{switch(a){case"label":return n.label||typeof n.score=="number"&&We(n.score)||"n/a";case"score":return typeof n.score=="number"&&We(n.score)||n.label||"n/a";case"none":return"";default:P()}};function u3({annotation:n,displayPreference:a,size:t}){const l=d3({annotation:n,displayPreference:a});return s(S,{direction:"row",gap:"size-100",alignItems:"center",className:"annotation-name-and-value",children:[e(Nt,{annotationName:n.name}),e("div",{css:m(wl,{minWidth:"5rem"}),children:e(C,{weight:"heavy",size:t,color:"inherit",children:n.name})}),l&&e("div",{css:m(wl,m`
              margin-left: var(--ac-global-dimension-100);
            `),children:e(C,{fontFamily:"mono",children:l})})]})}const g3=m`
  border-radius: var(--ac-global-dimension-size-50);
  border: 1px solid var(--ac-global-color-grey-400);
  padding: var(--ac-global-dimension-size-50)
    var(--ac-global-dimension-size-100);
  transition: background-color 0.2s;
  display: flex;
  flex-direction: row;
  gap: var(--ac-global-dimension-size-50);
  &[data-clickable="true"] {
    cursor: pointer;
    &:hover {
      background-color: var(--ac-global-color-grey-300);
    }
  }
  .ac-icon-wrap {
    font-size: 12px;
  }
`;function ur({annotation:n,onClick:a,annotationDisplayPreference:t="score",className:l,children:i,clickable:r}){const o=r??typeof a=="function";return s("div",{role:o?"button":void 0,"data-clickable":o,className:l,css:m(g3),"aria-label":o?"Click to view the annotation trace":`Annotation: ${n.name}`,onClick:c=>{a&&(c.stopPropagation(),c.preventDefault(),a())},children:[e(u3,{annotation:n,displayPreference:t}),i]})}const m3=m`
  text-overflow: ellipsis;
  overflow: hidden;
  white-space: nowrap;
`,da=({children:n,maxWidth:a,title:t})=>e("div",{css:m3,style:{maxWidth:a},title:t,children:n});function p3({annotation:n}){return e(S,{direction:"column",gap:"size-100",height:"100%",justifyContent:"space-between",children:s(w,{children:[s(S,{direction:"row",gap:"size-100",alignItems:"center",children:[e(Nt,{annotationName:n.name}),e(C,{weight:"heavy",color:"inherit",size:"L",elementType:"h3",children:n.name})]}),s(w,{paddingTop:"size-100",minWidth:"150px",children:[s(S,{direction:"row",justifyContent:"space-between",children:[e(C,{weight:"heavy",color:"inherit",children:"label"}),e(C,{color:"inherit",title:n.label??void 0,children:e(da,{maxWidth:"200px",children:n.label||"--"})})]}),s(S,{direction:"row",justifyContent:"space-between",children:[e(C,{weight:"heavy",color:"inherit",children:"score"}),e(C,{color:"inherit",fontFamily:"mono",children:cr(n.score)})]}),n.annotatorKind?s(S,{direction:"row",justifyContent:"space-between",children:[e(C,{weight:"heavy",color:"inherit",children:"annotator kind"}),e(C,{color:"inherit",children:n.annotatorKind})]}):null]}),n.explanation?e(w,{paddingTop:"size-50",children:s(S,{direction:"column",children:[e(C,{weight:"heavy",color:"inherit",children:"explanation"}),e(w,{maxHeight:"300px",overflow:"auto",children:e(C,{color:"inherit",children:n.explanation})})]})}):null,n.createdAt?s(S,{direction:"row",justifyContent:"space-between",wrap:"wrap",gap:"size-100",children:[e(C,{weight:"heavy",color:"inherit",children:"created at"}),e(C,{color:"inherit",children:new Date(n.createdAt).toLocaleString().split(",").join(`,
`)})]}):null]})})}function Qg({annotation:n,children:a}){return s(R,{delay:500,children:[e(_i,{children:a}),e(ie,{offset:3,children:e(p3,{annotation:n})})]})}function Wg({indeterminate:n,...a}){const t=p.useRef(null);return p.useEffect(()=>{typeof n=="boolean"&&(t.current.indeterminate=!a.checked&&n)},[t,n,a.checked]),e("div",{onClick:l=>{l.stopPropagation()},children:e("input",{type:"checkbox",ref:t,css:m`
          cursor: pointer;
        `,...a})})}function h3(n){const{children:a}=n;return e("tbody",{className:"is-empty",children:e("tr",{children:e("td",{colSpan:100,css:m`
            text-align: center;
            padding: var(--ac-global-dimension-size-300)
              var(--ac-global-dimension-size-300) !important;
          `,children:a})})})}function f3(n){const{message:a="No Data"}=n;return e(h3,{children:e(C,{children:a})})}const b3=n=>typeof n=="object"&&n!==null&&typeof n.message=="string",y3=/["]message["]:\s*["]([^""]+)["]/g,$t=n=>{if(!b3(n))return null;const a=n.message;if(typeof a!="string")return null;const t=[...a.matchAll(y3)].map(l=>l[1]);return t.length>0?t:null},v3=n=>{const a=n;return typeof a=="object"&&a!==null&&typeof a.source=="object"&&a.source!==null&&Array.isArray(a.source.errors)&&a.source.errors.every(t=>typeof t=="object"&&t!==null&&typeof t.message=="string")},C3=n=>Array.isArray(n)&&n.every(a=>typeof a=="object"&&a!==null&&typeof a.message=="string"),qg=n=>v3(n)?n.source.errors.map(a=>a.message):C3(n)?n.map(a=>a.message):null;function Xg(n){const{isCommitting:a,onSubmit:t,defaultName:l}=n,{control:i,handleSubmit:r,formState:{isDirty:o,isValid:c}}=Re({defaultValues:{name:l??"New Key",description:"",expiresAt:null}});return e(be,{children:({close:d})=>s(Ke,{children:[s(Pe,{children:[e(Ve,{children:"Create an API Key"}),e(ln,{children:e(Qe,{slot:"close"})})]}),s(w1,{onSubmit:r(u=>t(u,d)),children:[s(w,{padding:"size-200",children:[e($,{name:"name",control:i,rules:{required:"System key name is required"},render:({field:{onChange:u,onBlur:g,value:h},fieldState:{invalid:f,error:b}})=>s(Q,{isInvalid:f,onChange:u,onBlur:g,value:h.toString(),size:"S",children:[e(K,{children:"Name"}),e(j,{}),b!=null&&b.message?e(W,{children:b.message}):e(C,{slot:"description",children:"A name to identify the key"})]})}),e($,{name:"description",control:i,render:({field:{onChange:u,onBlur:g,value:h},fieldState:{invalid:f,error:b}})=>s(Q,{isInvalid:f,onChange:u,onBlur:g,value:h==null?void 0:h.toString(),size:"S",children:[e(K,{children:"Description"}),e(ma,{}),b!=null&&b.message?e(W,{children:b.message}):e(C,{slot:"description",children:"A description of the system key"})]})}),e($,{name:"expiresAt",control:i,rules:{validate:u=>u&&u.toDate(Xa())<new Date?"Date must be in the future":!0},render:({field:{name:u,onChange:g,onBlur:h,value:f},fieldState:{invalid:b,error:y}})=>s(tt,{isInvalid:b,onChange:g,onBlur:h,value:f,name:u,granularity:"minute",css:m`
                      .react-aria-DateInput {
                        width: 100%;
                      }
                    `,children:[e(K,{children:"Expires At"}),e(Ya,{children:v=>e(Ja,{segment:v})}),y!=null&&y.message?e(W,{children:y.message}):e(C,{slot:"description",children:"The date at which the key will expire. Optional"})]})})]}),e(w,{paddingStart:"size-200",paddingEnd:"size-200",paddingTop:"size-100",paddingBottom:"size-100",borderColor:"dark",borderTopWidth:"thin",children:e(S,{direction:"row",gap:"size-100",justifyContent:"end",children:e(z,{variant:o?"primary":"default",type:"submit",size:"S",isDisabled:!c||a,children:a?"Creating...":"Create Key"})})})]})]})})}function k3(n){var g;const{theme:a}=le(),{jsonSchema:t,optionalLint:l,basicSetup:i,...r}=n,o=a==="light"?Hn:jn,c=(g=n.value)==null?void 0:g.length,d=!l||c&&c>0,u=p.useMemo(()=>{const h=[oi(),ft.lineWrapping,si.of([...ci.filter(f=>f.key!=="Mod-Enter")])];return d&&h.push(et(di())),t&&h.push(et(Is(),{needsRefresh:As}),zs.data.of({autocomplete:Ms()}),Fs(Es()),Ds(t)),h},[t,d]);return e(Zn,{value:n.value,extensions:u,editable:!0,theme:o,basicSetup:{...i,defaultKeymap:!1},...r})}function gr(n){const{basicSetup:a,...t}=n,{theme:l}=le(),i=l==="light"?Hn:jn,r=p.useMemo(()=>{const o={lineNumbers:!0,foldGutter:!0,bracketMatching:!0,syntaxHighlighting:!0,highlightActiveLine:!1,highlightActiveLineGutter:!1};return a?{...o,...a}:o},[a]);return e(Zn,{value:n.value,extensions:[oi(),ft.lineWrapping,et(di())],editable:!1,theme:i,...t,basicSetup:r})}function L3(n){const{theme:a}=le(),t=a==="light"?Hn:jn,{basicSetup:l={}}=n,i=p.useMemo(()=>({lineNumbers:!1,foldGutter:!0,bracketMatching:!0,syntaxHighlighting:!0,highlightActiveLine:!1,highlightActiveLineGutter:!1,...l}),[l]);return e(Zn,{value:n.value,extensions:[_s()],editable:!1,theme:t,...n,basicSetup:i})}const mr=m`
  position: relative;
  --code-block-min-height: 40px;
  min-height: var(--code-block-min-height);
  display: flex;
  flex-direction: row;
  align-items: center;
  .cm-theme,
  .cm-editor {
    width: 100%;
    min-height: var(--code-block-min-height);
  }
  .cm-editor {
    padding-top: var(--ac-global-dimension-size-100);
    padding-bottom: var(--ac-global-dimension-size-100);
  }
  .cm-gutters,
  .cm-gutters * {
    background: none;
    background-color: transparent !important;
    border-right: none;
  }
  .copy-to-clipboard-button {
    position: absolute;
    top: var(--ac-global-dimension-size-100);
    right: var(--ac-global-dimension-size-100);
    z-index: 1;
  }
`;function xe(n){const{value:a}=n;return s("div",{className:"python-code-block",css:mr,children:[e(Ct,{text:a}),e(L3,{value:a})]})}function ve({children:n,...a}){return e(w,{borderColor:"light",borderWidth:"thin",borderRadius:"small",...a,children:n})}function w3(n){const{theme:a}=le(),t=a==="light"?Hn:jn,{basicSetup:l}=n,i=p.useMemo(()=>({lineNumbers:!1,foldGutter:!0,bracketMatching:!0,syntaxHighlighting:!0,highlightActiveLine:!1,highlightActiveLineGutter:!1,...l}),[l]);return e(Zn,{value:n.value,extensions:[Ks({typescript:!0})],editable:!1,theme:t,...n,basicSetup:i})}const S3=m`
  &.is-hovered {
    border: 1px solid var(--ac-global-input-field-border-color-active);
  }
  &.is-focused {
    border: 1px solid var(--ac-global-input-field-border-color-active);
  }
  &.is-invalid {
    border: 1px solid var(--ac-global-color-danger);
  }
  border-radius: var(--ac-global-rounding-small);
  border: 1px solid var(--ac-global-input-field-border-color);
  width: 100%;
  .cm-content,
  .cm-editor {
    border-radius: var(--ac-global-rounding-small);
  }
  box-sizing: border-box;
  .cm-focused {
    outline: none;
  }
  transition: all 0.2s ease-in-out;
`;function x3({children:n,validationState:a,...t}){const[l,i]=p.useState(!1),[r,o]=p.useState(!1),c=a==="invalid";return e(as,{...t,validationState:c?"invalid":"valid",children:e("div",{className:V("json-editor-wrap",{"is-hovered":r,"is-focused":l,"is-invalid":c}),onFocus:()=>i(!0),onBlur:()=>i(!1),onMouseEnter:()=>o(!0),onMouseLeave:()=>o(!1),css:S3,children:n})})}const T3=["Python","TypeScript"];function A3(n){return typeof n=="string"&&T3.includes(n)}function Yg({language:n,onChange:a,size:t}){return s(Gn,{size:t,selectedKeys:[n],"aria-label":"Code Language",onSelectionChange:l=>{if(l.size===0)return;const i=l.keys().next().value;if(A3(i))a(i);else throw new Error(`Unknown language: ${i}`)},children:[e(Ce,{"aria-label":"Python",id:"Python",children:"Python"}),e(Ce,{"aria-label":"TypeScript",id:"TypeScript",children:"TypeScript"})]})}function Jg(n){const{jwt:a}=n;return e(be,{children:s(Ke,{children:[s(Pe,{children:[e(Ve,{children:"New API Key Created"}),e(ln,{children:e(Qe,{slot:"close"})})]}),e(ya,{variant:"success",banner:!0,children:"You have successfully created a new API key. The API key will only be displayed once below. Please copy and save it in a secure location."}),s("div",{css:m`
            .ac-field {
              width: 100%;
            }
          `,children:[e(w,{padding:"size-200",children:s(S,{direction:"row",gap:"size-100",alignItems:"end",children:[s(Q,{isReadOnly:!0,value:a,children:[e(K,{children:"API Key"}),e(j,{})]}),e(Ct,{text:a,size:"M"})]})}),s(w,{padding:"size-200",borderTopColor:"light",borderTopWidth:"thin",children:[e(ne,{level:2,weight:"heavy",children:"How to Use the API Key"}),e(w,{paddingBottom:"size-100",paddingTop:"size-100",children:e(C,{children:"When interacting with Phoenix clients and OTEL SDKs, set the environment variable"})}),e(ve,{children:e(xe,{value:`PHOENIX_API_KEY=${a}`})}),e(w,{paddingBottom:"size-100",paddingTop:"size-100",children:e(C,{children:"When using OpenTelemetry SDKs pass the API key in the headers"})}),e(ve,{children:e(xe,{value:`OTEL_EXPORTER_OTLP_HEADERS='Authorization=Bearer ${a}'`})}),e(w,{paddingBottom:"size-100",paddingTop:"size-100",children:s(C,{children:["When using the Phoenix REST and GraphQL APIs, pass the API key as a"," ",e(de,{href:"https://swagger.io/docs/specification/authentication/bearer-authentication/",children:"bearer token"}),"."]})}),e(ve,{children:e(xe,{value:`Authorization: Bearer ${a}`})})]}),e(w,{padding:"size-200",borderTopColor:"light",borderTopWidth:"thin",children:e(S,{direction:"row",justifyContent:"end",children:e(z,{variant:"primary","aria-label":"dismiss",slot:"close",children:"Close"})})})]})]})})}function em({handleDelete:n}){return s(_e,{children:[e(z,{variant:"danger",size:"S",leadingVisual:e(T,{svg:e(Tt,{})}),"aria-label":"Delete System Key"}),e(Cn,{isDismissable:!0,children:e(vn,{children:e(be,{children:({close:a})=>s(Ke,{children:[s(Pe,{children:[e(Ve,{children:"Delete API Key"}),e(ln,{children:e(Qe,{slot:"close"})})]}),e(w,{padding:"size-200",children:e(C,{color:"danger",children:"Are you sure you want to delete this key? This cannot be undone and will disable all uses of this key."})}),e(w,{paddingEnd:"size-200",paddingTop:"size-100",paddingBottom:"size-100",borderTopColor:"light",borderTopWidth:"thin",children:s(S,{direction:"row",justifyContent:"end",gap:"size-100",children:[e(z,{slot:"close",size:"S",children:"Cancel"}),e(z,{variant:"danger",onPress:()=>{a(),n()},size:"S",children:"Delete Key"})]})})]})})})})]})}function I3(n){const{fallback:a=null,children:t}=n,{viewer:l}=xn();return l?t:e(U,{children:a})}function pr(n){const{fallback:a=null,children:t}=n,{viewer:l}=xn();return!l||l.role.name!=="ADMIN"?e(U,{children:a}):t}function nm(n){const{fallback:a=null,children:t}=n;return T2()?t:e(U,{children:a})}function hr({children:n}){return e("div",{style:{display:"contents"},onClick:a=>a.stopPropagation(),onKeyDown:a=>a.stopPropagation(),onMouseDown:a=>a.stopPropagation(),onPointerDown:a=>a.stopPropagation(),children:n})}function fr({columns:n,data:a}){const t=S1({columns:n,data:a,getCoreRowModel:A1(),getPaginationRowModel:T1(),getSortedRowModel:x1()}),l=t.getRowModel().rows,r=l.length>0?e("tbody",{children:l.map(o=>e("tr",{children:o.getVisibleCells().map(c=>e("td",{children:Xt(c.column.columnDef.cell,c.getContext())},c.id))},o.id))}):e(f3,{});return s(U,{children:[s("table",{css:Ot,children:[e("thead",{children:t.getHeaderGroups().map(o=>e("tr",{children:o.headers.map(c=>e("th",{colSpan:c.colSpan,children:c.isPlaceholder?null:e("div",{children:Xt(c.column.columnDef.header,c.getContext())})},c.id))},o.id))}),r]}),s("div",{css:e3,children:[e(z,{variant:"default",size:"S",onPress:t.previousPage,isDisabled:!t.getCanPreviousPage(),"aria-label":"Previous Page",leadingVisual:e(T,{svg:e(yc,{})})}),e(z,{size:"S",onPress:t.nextPage,isDisabled:!t.getCanNextPage(),"aria-label":"Next Page",leadingVisual:e(T,{svg:e(Ci,{})})})]})]})}const z3=m`
  float: right;
`;function Kn({getValue:n}){const a=n();if(!bt(a))throw new Error("IntCell only supports number or null values.");return e("span",{title:a!=null?String(a):"",className:"font-mono",css:z3,children:cr(a)})}const M3=m`
  float: right;
`;function F3({getValue:n}){const a=n();if(!bt(a))throw new Error("IntCell only supports number or null values.");return e("span",{title:a!=null?String(a):"",className:"font-mono",css:M3,children:s3(a)})}function E3({getValue:n}){const a=n();if(!bt(a))throw new Error("IntCell only supports number or null values.");return e("span",{title:a!=null?String(a):"",children:c3(a)})}const Sl=100;function D3(n){return n.length>Sl?`${n.slice(0,Sl)}...`:n}function am({getValue:n}){const a=n(),t=a!=null&&typeof a=="string"?D3(a):"--";return e("span",{children:t})}function tm({getValue:n}){const a=n(),t=a!=null&&typeof a=="string"?a:"--";return e("pre",{style:{whiteSpace:"pre-wrap"},children:t})}const _3=m`
  margin: 0;
  white-space: pre-wrap;
  word-wrap: break-word;
`;function xl(n,a){return n.length>a?`${n.slice(0,a)}...`:n}function K3({json:n,maxLength:a,space:t=0,disableTitle:l=!1,collapseSingleKey:i=!0}){const r=typeof a=="number",o=p.useMemo(()=>JSON.stringify(n,null,t),[n,t]),c=p.useMemo(()=>JSON.stringify(n,null,2),[n]),d=l?void 0:c;if(!fe(n))return console.warn("JSONText component received a non-object value",n),e("span",{title:d,className:"font-mono",children:String(n)});const u=n;if(Object.keys(u).length===0)return e("span",{title:d,children:"--"});if(Object.keys(u).length===1&&i){const b=Object.keys(u)[0],y=u[b];if(typeof y=="string"){const v=r?xl(y,a):y;return e("span",{title:d,className:"font-mono",children:v})}}const g=r?xl(o,a):o;return e(r?"span":"pre",{title:d,css:r?void 0:_3,children:g})}const P3=100;function lm({getValue:n}){const a=n();return e(K3,{json:a,maxLength:P3})}m`
  position: relative;
  height: 100%;
  min-height: 100%;
  .controls {
    transition: opacity 0.2s ease-in-out;
    opacity: 0;
    display: none;
    z-index: 1;
  }
  &:hover .controls {
    opacity: 1;
    display: flex;
    // make them stand out
    button {
      border-color: var(--ac-global-color-primary);
    }
  }
`;m`
  position: absolute;
  top: calc(-1 * var(--ac-global-dimension-static-size-200));
  right: var(--ac-global-dimension-static-size-200);
  display: flex;
  flex-direction: row;
  gap: var(--ac-global-dimension-static-size-100);
`;const V3=m`
  border-radius: 16px;
  padding: var(--ac-global-dimension-size-50)
    var(--ac-global-dimension-size-200) !important;
`,R3=({onLoadMore:n,isLoadingNext:a,buttonProps:t})=>e(z,{onPress:()=>{n()},size:"S",css:V3,isDisabled:a,leadingVisual:a?e(T,{svg:e(Ai,{})}):void 0,...t,children:a?"Loading...":"Load More"}),O3=m`
  position: relative;
`,N3=m`
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
`;function im({onLoadMore:n,isLoadingNext:a}){return e("tr",{css:O3,children:e("td",{colSpan:100,css:N3,children:e(R3,{onLoadMore:n,isLoadingNext:a})})})}function rm({children:n,extra:a}){return s("div",{css:$3,children:[e("div",{css:B3,children:n}),e("div",{css:H3,children:a})]})}const $3=m`
  padding: 0 var(--ac-global-dimension-static-size-100) 0
    var(--ac-global-dimension-static-size-200);
  border-bottom: var(--ac-global-border-size-thin) solid
    var(--ac-global-color-grey-200);
  background-color: var(--ac-global-color-grey-50);
  min-height: 39px;
  display: flex;
  flex-direction: row;
  gap: var(--ac-global-dimension-static-size-100);
  align-items: center;
  justify-content: space-between;
  min-width: 0;
  flex: none;
`,B3=m`
  height: 100%;
  min-width: 0;
  flex: 1 1 auto;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  display: flex;
  align-items: center;
`,H3=m`
  display: flex;
  flex-direction: row;
  gap: var(--ac-global-dimension-static-size-50);
  align-items: center;
  flex: none;
`,j3={year:"numeric",month:"numeric",day:"numeric",hour:"2-digit",minute:"2-digit"};function om({getValue:n,format:a=j3}){const t=n();if(!Gs(t))throw new Error("TimestampCell only supports string, null, or undefined values.");const l=t!=null?new Date(t).toLocaleString([],a):"--";return e("time",{title:t!=null?String(t):"",children:l})}function sm(n){return e("div",{css:m`
        background-color: var(--ac-global-color-grey-200);
        border: 1px solid var(--ac-global-color-grey-300);
        padding: var(--ac-global-dimension-static-size-100);
        border-radius: var(--ac-global-rounding-medium);
        display: flex;
        flex-direction: column;
        gap: var(--ac-global-dimension-static-size-50);
        min-width: 200px;
        box-shadow: 0 8px 8px rgba(0, 0, 0, 0.1);
      `,children:n.children})}function cm(n){return s("div",{css:m`
        display: flex;
        flex-direction: row;
        justify-content: space-between;
      `,children:[s("div",{css:m`
          display: flex;
          flex-direction: row;
          gap: var(--ac-global-dimension-static-size-100);
          align-items: center;
        `,children:[e(U3,{color:n.color,shape:n.shape??"line"}),e(C,{title:n.name,children:e(da,{maxWidth:"120px",children:n.name})})]}),e(C,{children:n.value})]})}function dm(){return e("div",{css:m`
        height: 1px;
        background-color: var(--ac-global-color-grey-300);
        width: 100%;
      `})}const Z3=n=>{if(n==="line")return m`
      width: 8px;
      height: 2px;
    `;if(n==="circle")return m`
      width: 8px;
      height: 8px;
      border-radius: 50%;
    `;if(n==="square")return m`
      width: 8px;
      height: 8px;
    `};function U3({color:n,shape:a="line"}){return e("div",{css:m(Z3(a),m`
          background-color: ${n};
          flex: none;
        `)})}const um={dataKey:"timestamp",stroke:"var(--ac-global-colo-grey-400)",style:{fill:"var(--ac-global-text-color-700)"},scale:"time",type:"number",domain:["auto","auto"],padding:"gap"},gm={stroke:"var(--ac-global-color-grey-900)"},mm={value:"▼",position:"top",style:{fill:"#fabe32",fontSize:"var(--ac-global-font-size-xs)"}},pm={cursor:{fill:"var(--ac-global-color-grey-300)"}},hm={strokeDasharray:"4 4",stroke:"var(--chart-cartesian-grid-stroke-color)"},fm={stroke:"var(--chart-axis-stroke-color)",style:{fill:"var(--chart-axis-text-color)"}},bm={stroke:"var(--chart-axis-stroke-color)",style:{fill:"var(--chart-axis-text-color)"}},ym={align:"right",formatter:n=>e("span",{style:{color:"var(--chart-legend-text-color)"},children:n})},Nn=60,$n=Nn*24,Ua=2*$n;function vm(n){const{start:a,end:t}=n,l=Math.floor((t.valueOf()-a.valueOf())/1e3/60/60);return l<=1?{evaluationWindowMinutes:1,samplingIntervalMinutes:1}:l<=24?{evaluationWindowMinutes:Nn,samplingIntervalMinutes:Nn}:{evaluationWindowMinutes:$n,samplingIntervalMinutes:$n}}function Cm(n){const{start:a,end:t}=n,l=Math.floor((t.valueOf()-a.valueOf())/1e3/60/60);return l<=1?{evaluationWindowMinutes:Ua,samplingIntervalMinutes:1}:l<=24?{evaluationWindowMinutes:Ua,samplingIntervalMinutes:Nn}:{evaluationWindowMinutes:Ua,samplingIntervalMinutes:$n}}function G3(n){let a;return n<Nn?a="%H:%M %p":n<$n?a="%x %H:%M %p":a="%-m/%-d",a}function km(n){const a=n.samplingIntervalMinutes;return p.useMemo(()=>Ie(G3(a)),[a])}function Lm({scale:n}){return p.useMemo(()=>{switch(n){case"YEAR":return Ie("%Y");case"MONTH":return Ie("%b %Y");case"WEEK":case"DAY":return Ie("%-m/%-d");case"HOUR":return Ie("%H:%M");case"MINUTE":return Ie("%H:%M");default:P()}},[n])}const x=n=>`var(${n})`,Q3=Object.freeze({blue100:x("--ac-global-color-blue-200"),blue200:x("--ac-global-color-blue-300"),blue300:x("--ac-global-color-blue-400"),blue400:x("--ac-global-color-blue-500"),blue500:x("--ac-global-color-blue-600"),blue600:x("--ac-global-color-blue-700"),blue700:x("--ac-global-color-blue-800"),blue800:x("--ac-global-color-blue-900"),blue900:x("--ac-global-color-blue-1000"),orange100:x("--ac-global-color-orange-500"),orange200:x("--ac-global-color-orange-600"),orange300:x("--ac-global-color-orange-700"),orange400:x("--ac-global-color-orange-800"),orange500:x("--ac-global-color-orange-900"),purple100:x("--ac-global-color-purple-100"),purple200:x("--ac-global-color-purple-200"),purple300:x("--ac-global-color-purple-300"),purple400:x("--ac-global-color-purple-400"),purple500:x("--ac-global-color-purple-500"),magenta100:x("--ac-global-color-magenta-200"),magenta200:x("--ac-global-color-magenta-300"),magenta300:x("--ac-global-color-magenta-400"),magenta400:x("--ac-global-color-magenta-500"),magenta500:x("--ac-global-color-magenta-600"),red100:x("--ac-global-color-red-200"),red200:x("--ac-global-color-red-300"),red300:x("--ac-global-color-red-400"),red400:x("--ac-global-color-red-500"),red500:x("--ac-global-color-red-600"),grey100:x("--ac-global-color-grey-100"),grey200:x("--ac-global-color-grey-200"),grey300:x("--ac-global-color-grey-300"),grey400:x("--ac-global-color-grey-400"),grey500:x("--ac-global-color-grey-500"),grey600:x("--ac-global-color-grey-600"),grey700:x("--ac-global-color-grey-700"),default:x("--ac-global-text-color-900"),primary:x("--px-primary-color"),reference:x("--px-reference-color")}),W3=Object.freeze({blue100:x("--ac-global-color-blue-200"),blue200:x("--ac-global-color-blue-300"),blue300:x("--ac-global-color-blue-400"),blue400:x("--ac-global-color-blue-500"),blue500:x("--ac-global-color-blue-600"),blue600:x("--ac-global-color-blue-700"),blue700:x("--ac-global-color-blue-800"),blue800:x("--ac-global-color-blue-900"),blue900:x("--ac-global-color-blue-1000"),orange100:x("--ac-global-color-orange-500"),orange200:x("--ac-global-color-orange-600"),orange300:x("--ac-global-color-orange-700"),orange400:x("--ac-global-color-orange-800"),orange500:x("--ac-global-color-orange-900"),purple100:x("--ac-global-color-purple-100"),purple200:x("--ac-global-color-purple-200"),purple300:x("--ac-global-color-purple-300"),purple400:x("--ac-global-color-purple-400"),purple500:x("--ac-global-color-purple-500"),magenta100:x("--ac-global-color-magenta-200"),magenta200:x("--ac-global-color-magenta-300"),magenta300:x("--ac-global-color-magenta-400"),magenta400:x("--ac-global-color-magenta-500"),magenta500:x("--ac-global-color-magenta-600"),red100:x("--ac-global-color-red-200"),red200:x("--ac-global-color-red-300"),red300:x("--ac-global-color-red-400"),red400:x("--ac-global-color-red-500"),red500:x("--ac-global-color-red-600"),grey100:x("--ac-global-color-grey-100"),grey200:x("--ac-global-color-grey-200"),grey300:x("--ac-global-color-grey-300"),grey400:x("--ac-global-color-grey-400"),grey500:x("--ac-global-color-grey-500"),grey600:x("--ac-global-color-grey-600"),grey700:x("--ac-global-color-grey-700"),default:x("--ac-global-text-color-900"),primary:x("--px-primary-color"),reference:x("--px-reference-color")}),q3=()=>{const{theme:n}=le();return p.useMemo(()=>n==="dark"?Q3:W3,[n])},X3=(n,a)=>{const t=[["blue",5],["orange",5],["purple",5],["pink",5],["gray",5]],l=t.length,i=n%l,r=Math.floor(n/l),[o,c]=t[i],d=500-100*(r%c),u=`${o}${d}`;return a[u]||a.default},Y3={danger:"var(--ac-global-color-red-700)",success:"var(--ac-global-color-celery-700)",warning:"var(--ac-global-color-orange-700)",info:"var(--ac-global-color-blue-700)"},J3={danger:"var(--ac-global-color-red-700)",success:"var(--ac-global-color-celery-700)",warning:"var(--ac-global-color-orange-700)",info:"var(--ac-global-color-blue-700)"},wm=()=>{const{theme:n}=le();return p.useMemo(()=>n==="dark"?J3:Y3,[n])},e5={category1:"var(--ac-global-color-blue-700)",category2:"var(--ac-global-color-purple-900)",category3:"var(--ac-global-color-magenta-600)",category4:"var(--ac-global-color-indigo-600)",category5:"var(--ac-global-color-blue-900)",category6:"var(--ac-global-color-indigo-1100)",category7:"var(--ac-global-color-orange-600)",category8:"var(--ac-global-color-celery-400)",category9:"var(--ac-global-color-seafoam-600)",category10:"var(--ac-global-color-green-1000)",category11:"var(--ac-global-color-yellow-400)",category12:"var(--ac-global-color-red-1100)"},n5={category1:"var(--ac-global-color-blue-700)",category2:"var(--ac-global-color-purple-800)",category3:"var(--ac-global-color-magenta-800)",category4:"var(--ac-global-color-indigo-600)",category5:"var(--ac-global-color-blue-900)",category6:"var(--ac-global-color-indigo-1100)",category7:"var(--ac-global-color-orange-600)",category8:"var(--ac-global-color-celery-400)",category9:"var(--ac-global-color-seafoam-600)",category10:"var(--ac-global-color-green-1000)",category11:"var(--ac-global-color-yellow-400)",category12:"var(--ac-global-color-red-1100)"},a5=()=>{const{theme:n}=le();return p.useMemo(()=>n==="dark"?n5:e5,[n])};function Sm(n){switch(n.__typename){case"NominalBin":return n.name;case"IntervalBin":return`${On(n.range.start)} - ${On(n.range.end)}`;case"MissingValueBin":return"(empty)";case"%other":throw new Error("Unexpected bin type %other");default:P()}}function xm({scale:n}){return p.useMemo(()=>{switch(n){case"YEAR":return 1;case"MONTH":return 1;case"WEEK":case"DAY":return 1;case"HOUR":return 1;case"MINUTE":return 5;default:P()}},[n])}var Xn=(n=>(n.ADMIN="ADMIN",n.MEMBER="MEMBER",n))(Xn||{});function t5(n){return n.toLocaleLowerCase()}function l5(n){return typeof n=="string"&&n in Xn}const Ga=2147483647,Tm=[{name:"production",description:"The version deployed to production"},{name:"staging",description:"The version deployed to staging"},{name:"development",description:"The version deployed for development"}],i5=Object.values(Xn),r5=m`
  .ac-field-label {
    display: none;
  }
`;function br({onChange:n,role:a,includeLabel:t=!0,errorMessage:l,isInvalid:i=!1,size:r="M",...o}){return s(Ne,{css:t?void 0:r5,className:"role-select",size:r,selectedKey:a??void 0,"aria-label":"User Role",isInvalid:i,onSelectionChange:c=>{l5(c)&&n(c)},...o,children:[t&&e(K,{children:"Role"}),s(z,{children:[e(Oe,{}),e(Ae,{})]}),e(ue,{children:e(we,{children:i5.map(c=>e(ee,{id:c,children:t5(c)},c))})}),e(W,{children:l})]})}function Am({onSubmit:n,email:a,username:t,role:l,isSubmitting:i}){const{control:r,handleSubmit:o,formState:{isDirty:c}}=Re({defaultValues:{email:a??"",username:t??"",role:l??Xn.MEMBER}}),d=u=>{const g={...u,email:u.email.trim().toLowerCase()};n(g)};return e("div",{css:m`
        .role-select {
          width: 100%;
          .ac-dropdown--picker,
          .ac-dropdown-button {
            width: 100%;
          }
        }
      `,children:s(on,{onSubmit:o(d),children:[e(w,{padding:"size-200",children:s(S,{direction:"column",gap:"size-100",children:[e($,{name:"email",control:r,rules:{required:"Email is required",pattern:{value:/^[^@\s]+@[^@\s]+[.][^@\s]+$/,message:"Invalid email format"}},render:({field:{name:u,onChange:g,onBlur:h,value:f},fieldState:{error:b,invalid:y}})=>s(Q,{type:"email",name:u,isRequired:!0,onChange:g,isInvalid:y,onBlur:h,value:f,children:[e(K,{children:"Email"}),e(j,{}),b?e(W,{children:b==null?void 0:b.message}):e(C,{slot:"description",children:"The user's email address. Must be unique."})]})}),e($,{name:"username",control:r,rules:{required:"Username is required"},render:({field:{name:u,onChange:g,onBlur:h,value:f},fieldState:{error:b,invalid:y}})=>s(Q,{name:u,isRequired:!0,onChange:g,isInvalid:y,onBlur:h,value:f,children:[e(K,{children:"Username"}),e(j,{}),b?e(W,{children:b==null?void 0:b.message}):e(C,{slot:"description",children:"A unique username."})]})}),e($,{name:"role",control:r,render:({field:{onChange:u,value:g},fieldState:{error:h}})=>e(br,{onChange:u,role:g,errorMessage:h==null?void 0:h.message})})]})}),e(w,{paddingStart:"size-200",paddingEnd:"size-200",paddingTop:"size-100",paddingBottom:"size-100",borderColor:"dark",borderTopWidth:"thin",children:e(S,{direction:"row",gap:"size-100",justifyContent:"end",children:e(z,{variant:c?"primary":"default",type:"submit",size:"S",isDisabled:i,children:i?"Adding...":"Add User"})})})]})})}const ea=4;function Im({onSubmit:n,email:a,username:t,password:l,role:i,isSubmitting:r}){const{control:o,handleSubmit:c,formState:{isDirty:d}}=Re({defaultValues:{email:a??"",username:t??"",password:l??void 0,confirmPassword:void 0,role:i??Xn.MEMBER}}),u=g=>{const h={...g,email:g.email.trim().toLowerCase()};n(h)};return e("div",{css:m`
        .role-select {
          width: 100%;
          .ac-dropdown--picker,
          .ac-dropdown-button {
            width: 100%;
          }
        }
      `,children:s(on,{onSubmit:c(u),children:[e(w,{padding:"size-200",children:s(S,{direction:"column",gap:"size-100",children:[e($,{name:"email",control:o,rules:{required:"Email is required",pattern:{value:/^[^@\s]+@[^@\s]+[.][^@\s]+$/,message:"Invalid email format"}},render:({field:{name:g,onChange:h,onBlur:f,value:b},fieldState:{invalid:y,error:v}})=>s(Q,{type:"email",name:g,isRequired:!0,onChange:h,isInvalid:y,onBlur:f,value:b,children:[e(K,{children:"Email"}),e(j,{}),v?e(W,{children:v==null?void 0:v.message}):e(C,{slot:"description",children:"The user's email address. Must be unique."})]})}),e($,{name:"username",control:o,rules:{required:"Username is required"},render:({field:{name:g,onChange:h,onBlur:f,value:b},fieldState:{invalid:y,error:v}})=>s(Q,{name:g,isRequired:!0,onChange:h,isInvalid:y,onBlur:f,value:b,children:[e(K,{children:"Username"}),e(j,{}),v?e(W,{children:v==null?void 0:v.message}):e(C,{slot:"description",children:"A unique username."})]})}),s(U,{children:[e($,{name:"password",control:o,rules:{required:"Password is required",minLength:{value:ea,message:`Password must be at least ${ea} characters`}},render:({field:{name:g,onChange:h,onBlur:f,value:b},fieldState:{invalid:y,error:v}})=>s(Q,{type:"password",isRequired:!0,name:g,isInvalid:y,onChange:h,onBlur:f,value:b||"",autoComplete:"new-password",children:[e(K,{children:"Password"}),e(j,{}),v?e(W,{children:v==null?void 0:v.message}):e(C,{slot:"description",children:"Password must be at least 4 characters"})]})}),e($,{name:"confirmPassword",control:o,rules:{required:"Please confirm your password",minLength:{value:ea,message:`Password must be at least ${ea} characters`},validate:(g,h)=>g===h.password||"Passwords do not match"},render:({field:{name:g,onChange:h,onBlur:f,value:b},fieldState:{invalid:y,error:v}})=>s(Q,{isRequired:!0,type:"password",name:g,isInvalid:y,onChange:h,onBlur:f,value:b||"",autoComplete:"new-password",children:[e(K,{children:"Confirm Password"}),e(j,{}),v?e(W,{children:v==null?void 0:v.message}):e(C,{slot:"description",children:"Confirm the new password"})]})})]}),e($,{name:"role",control:o,render:({field:{onChange:g,value:h},fieldState:{error:f,invalid:b}})=>e(br,{onChange:g,role:h,errorMessage:f==null?void 0:f.message,isInvalid:b})})]})}),e(w,{paddingStart:"size-200",paddingEnd:"size-200",paddingTop:"size-100",paddingBottom:"size-100",borderColor:"dark",borderTopWidth:"thin",children:e(S,{direction:"row",gap:"size-100",justifyContent:"end",children:e(z,{variant:d?"primary":"default",type:"submit",size:"S",isDisabled:r,children:r?"Adding...":"Add User"})})})]})})}function yr({name:n="system",profilePictureUrl:a,size:t=75}){const l=n.length?n[0].toUpperCase():"?",i=or(n),{theme:r}=le(),o=p.useMemo(()=>m`
      width: ${t}px;
      height: ${t}px;
      border-radius: 50%;
      font-size: ${Math.floor(t/2)}px;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      flex: none;
      overflow: hidden;
      --ac-internal-avatar-color: ${i};

      &[data-theme="light"] {
        background: var(--ac-internal-avatar-color);
        border: 1px solid
          lch(from var(--ac-internal-avatar-color) calc(l * infinity) c h / 0.3);
        color: lch(
          from var(--ac-internal-avatar-color) calc((50 - l) * infinity) 0 0
        );
      }

      &[data-theme="dark"] {
        --scoped-avatar-dark-bg: lch(
          from var(--ac-internal-avatar-color) calc(l * 0.7) c h
        );
        background: linear-gradient(
          120deg,
          var(--scoped-avatar-dark-bg),
          lch(from var(--scoped-avatar-dark-bg) calc(l * 0.6) c h)
        );
        border: 1px solid
          lch(from var(--scoped-avatar-dark-bg) calc(l * infinity) c h / 0.2);
        color: lch(from var(--scoped-avatar-dark-bg) calc(l * infinity) c h);
      }

      img {
        width: 100%;
        height: 100%;
        object-fit: cover;
      }
    `,[t,i]);return e("div",{css:o,"data-theme":r,children:a?e("img",{src:a}):l})}const vr=(function(){var n=[{defaultValue:null,kind:"LocalArgument",name:"input"}],a=[{alias:null,args:[{kind:"Variable",name:"regex",variableName:"input"}],concreteType:"ValidationResult",kind:"LinkedField",name:"validateRegularExpression",plural:!1,selections:[{alias:null,args:null,kind:"ScalarField",name:"isValid",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"errorMessage",storageKey:null}],storageKey:null}];return{fragment:{argumentDefinitions:n,kind:"Fragment",metadata:null,name:"RegexFieldQuery",selections:a,type:"Query",abstractKey:null},kind:"Request",operation:{argumentDefinitions:n,kind:"Operation",name:"RegexFieldQuery",selections:a},params:{cacheID:"a194706b4bec602eb34e8e12671ec9b7",id:null,metadata:{},name:"RegexFieldQuery",operationKind:"query",text:`query RegexFieldQuery(
  $input: String!
) {
  validateRegularExpression(regex: $input) {
    isValid
    errorMessage
  }
}
`}}})();vr.hash="588f0ae4347a5d65fd17babc2d6be11f";const zm=({value:n,onChange:a,error:t,isInvalid:l,description:i,label:r,ariaLabel:o,placeholder:c,...d})=>s(Q,{isInvalid:l,"aria-label":o||r,value:n,onChange:a,...d,children:[r&&e(K,{children:r}),e(j,{placeholder:c}),!t&&i&&e(C,{slot:"description",children:i}),t&&e(W,{children:t}),l&&n&&e(T,{style:{color:"var(--ac-global-color-danger)"},svg:e(Fc,{})}),!l&&n&&e(T,{style:{color:"var(--ac-global-color-success)"},svg:e(wt,{})})]}),o5=vr,Mm=({initialValue:n}={initialValue:""})=>{const[a,t]=p.useState(n),[l,i]=p.useState(a),[r,o]=p.useState(void 0),c=M.useRelayEnvironment(),d=p.useMemo(()=>ai.debounce(u=>{i(u)},500),[]);return p.useEffect(()=>{d(a)},[a,d]),p.useEffect(()=>{if(!l){o(void 0);return}const g=M.fetchQuery(c,o5,{input:l}).subscribe({next:h=>{h.validateRegularExpression.isValid?o(void 0):o(h.validateRegularExpression.errorMessage??"Regular expression is invalid")}});return()=>{g.unsubscribe()}},[l,c]),{value:a,onChange:t,isInvalid:r!=null,error:r}};function s5(){const[n,a]=p.useState("--");return p.useEffect(()=>{fetch("https://api.github.com/repos/Arize-ai/phoenix").then(t=>t.json()).then(t=>{a(he(".2s")(t.stargazers_count))})},[]),e(xd,{children:n})}function c5(n){const{size:a=34}=n;return s("svg",{xmlns:"http://www.w3.org/2000/svg",xmlnsXlink:"http://www.w3.org/1999/xlink",viewBox:"0 0 305.92 350.13",width:a,height:a,css:m`
        .cls-1 {
          fill: url(#linear-gradient);
        }

        .cls-2 {
          fill: url(#Fade_to_Black_2-2);
        }

        .cls-2,
        .cls-3 {
          opacity: 0.5;
        }

        .cls-4 {
          fill: #fedbb5;
        }

        .cls-5 {
          fill: #e5b4a6;
        }

        .cls-6 {
          fill: url(#Fade_to_Black_2);
        }

        .cls-6,
        .cls-7,
        .cls-8,
        .cls-9,
        .cls-10,
        .cls-11,
        .cls-12,
        .cls-13,
        .cls-14 {
          opacity: 0.4;
        }

        .cls-3 {
          fill: url(#linear-gradient-10);
        }

        .cls-7 {
          fill: url(#linear-gradient-6);
        }

        .cls-8 {
          fill: url(#linear-gradient-3);
        }

        .cls-9 {
          fill: url(#linear-gradient-4);
        }

        .cls-10 {
          fill: url(#linear-gradient-2);
        }

        .cls-11 {
          fill: url(#linear-gradient-7);
        }

        .cls-12 {
          fill: url(#linear-gradient-5);
        }

        .cls-13 {
          fill: url(#linear-gradient-8);
        }

        .cls-14 {
          fill: url(#linear-gradient-9);
        }
      `,children:[s("defs",{children:[s("linearGradient",{id:"linear-gradient",x1:"45.77",y1:"21.43",x2:"201.89",y2:"291.83",gradientUnits:"userSpaceOnUse",children:[e("stop",{offset:"0",stopColor:"#18bab6"}),e("stop",{offset:".5",stopColor:"#00adee"}),e("stop",{offset:"1",stopColor:"#0095c4"})]}),s("linearGradient",{id:"linear-gradient-2",x1:"197.65",y1:"237.84",x2:"65.97",y2:"9.77",gradientUnits:"userSpaceOnUse",children:[e("stop",{offset:"0",stopColor:"#fdfdfe",stopOpacity:"0"}),e("stop",{offset:".11",stopColor:"#fdfdfe",stopOpacity:".17"}),e("stop",{offset:".3",stopColor:"#fdfdfe",stopOpacity:".42"}),e("stop",{offset:".47",stopColor:"#fdfdfe",stopOpacity:".63"}),e("stop",{offset:".64",stopColor:"#fdfdfe",stopOpacity:".79"}),e("stop",{offset:".78",stopColor:"#fdfdfe",stopOpacity:".9"}),e("stop",{offset:".91",stopColor:"#fdfdfe",stopOpacity:".97"}),e("stop",{offset:"1",stopColor:"#fdfdfe"})]}),e("linearGradient",{id:"linear-gradient-3",x1:"158.8",y1:"236.43",x2:"63.93",y2:"72.09",xlinkHref:"#linear-gradient-2"}),e("linearGradient",{id:"linear-gradient-4",x1:"145.73",y1:"248.43",x2:"92.77",y2:"156.7",xlinkHref:"#linear-gradient-2"}),e("linearGradient",{id:"linear-gradient-5",x1:"147.93",y1:"266.95",x2:"114.95",y2:"209.83",xlinkHref:"#linear-gradient-2"}),s("linearGradient",{id:"linear-gradient-6",x1:"92.25",y1:"261.75",x2:"92.25",y2:"321.91",gradientUnits:"userSpaceOnUse",children:[e("stop",{offset:"0",stopColor:"#231f20"}),e("stop",{offset:".03",stopColor:"#231f20",stopOpacity:".9"}),e("stop",{offset:".22",stopColor:"#231f20",stopOpacity:".4"}),e("stop",{offset:".42",stopColor:"#231f20",stopOpacity:".1"}),e("stop",{offset:".65",stopColor:"#231f20",stopOpacity:"0"})]}),s("linearGradient",{id:"Fade_to_Black_2","data-name":"Fade to Black 2",x1:"159.88",y1:"256.07",x2:"159.88",y2:"286.75",gradientUnits:"userSpaceOnUse",children:[e("stop",{offset:"0",stopColor:"#231f20"}),e("stop",{offset:"1",stopColor:"#231f20",stopOpacity:"0"})]}),s("linearGradient",{id:"linear-gradient-7",x1:"174.69",y1:"176.58",x2:"174.69",y2:"151.5",gradientUnits:"userSpaceOnUse",children:[e("stop",{offset:"0",stopColor:"#231f20"}),e("stop",{offset:".03",stopColor:"#231f20",stopOpacity:".95"}),e("stop",{offset:".51",stopColor:"#231f20",stopOpacity:".26"}),e("stop",{offset:".81",stopColor:"#231f20",stopOpacity:"0"})]}),s("linearGradient",{id:"linear-gradient-8",x1:"229.53",y1:"195.1",x2:"229.53",y2:"134.41",gradientUnits:"userSpaceOnUse",children:[e("stop",{offset:"0",stopColor:"#231f20"}),e("stop",{offset:".18",stopColor:"#231f20",stopOpacity:".48"}),e("stop",{offset:".38",stopColor:"#231f20",stopOpacity:".12"}),e("stop",{offset:".58",stopColor:"#231f20",stopOpacity:"0"})]}),e("linearGradient",{id:"Fade_to_Black_2-2","data-name":"Fade to Black 2",x1:"286",y1:"242.89",x2:"265.05",y2:"206.61",xlinkHref:"#Fade_to_Black_2"}),e("linearGradient",{id:"linear-gradient-9",x1:"302.87",y1:"232.93",x2:"271.49",y2:"178.58",xlinkHref:"#linear-gradient-2"}),s("linearGradient",{id:"linear-gradient-10",x1:"221.39",y1:"223.73",x2:"267.07",y2:"197.36",gradientUnits:"userSpaceOnUse",children:[e("stop",{offset:"0",stopColor:"#231f20"}),e("stop",{offset:".31",stopColor:"#231f20",stopOpacity:".5"}),e("stop",{offset:".67",stopColor:"#231f20",stopOpacity:".13"}),e("stop",{offset:"1",stopColor:"#231f20",stopOpacity:"0"})]})]}),s("g",{id:"Layer_1-2","data-name":"Layer 1",children:[e("path",{className:"cls-1",d:"m305.42,218.76c-.9-4.06-2.96-7.8-6.14-11.13-1.22-1.28-2.59-2.48-4.07-3.58-.72-.53-1.48-1.03-2.26-1.52-.97-.6-1.98-1.19-3.07-1.75-4.05-2.08-7.5-4.17-10.53-6.41-1.23-.91-2.42-1.86-3.53-2.83-2.71-2.37-4.53-4.38-5.88-6.53-.44-.69-.83-1.44-1.2-2.14-.16-.31-.39-.57-.66-.77-.49-.36-1.12-.52-1.75-.4-.97.18-1.72.97-1.83,1.96-.09.76-.08,1.57.02,2.41.06.5-.2.96-.66,1.17-.11.05-.22.08-.33.09-.64.08-1.23.43-1.6.96-.37.54-.48,1.2-.33,1.83.14.55.32.93.48,1.24l.14.28c.1.19.2.39.31.58.3.57.62,1.15,1,1.71.71,1.04,1.52,2.07,2.46,3.18.3.35.35.86.13,1.27-.22.41-.68.64-1.14.58-5.37-.73-10.17-1.93-14.65-3.59-.51-.19-1.03-.37-1.53-.57-4.02-1.69,3.23-8.92,6.55-14.03,14.55-22.37,17.56-48,17.68-73.93.12-25.07-2.59-49.78-7.57-74.18v-.04c-3.25-20.44-6.01-28.12-7.74-30.97-.37-.76-.78-1.22-1.21-1.45-.48-.32-.73-.17-.73-.17-.93.03-2.01.87-3.3,2.22-5.42,5.71-5.12,12.49-3.62,19.58,6.85,32.22,12.01,64.63,9.66,97.75-1.61,22.83-5.87,44.82-21.82,62.69-.96,1.08-1.99,2.08-3.02,3.1-1.2,1.17-3.04,3.46-4.42,2.51-1.84-1.28-.2-3.9.37-5.25,9.35-21.89,12.04-44.77,10.6-68.36-.03-.55-.09-1.09-.13-1.63l.02-.03c-.04-.44-.08-.85-.12-1.28-.24-3.12-.53-6.23-.92-9.33-4.02-37.42-8.84-39.84-8.84-39.84h0c-.32-.28-.72-.51-1.25-.62-2.53-.53-3.92,1.7-5.04,3.39-5.07,7.6-2.83,15.67-1.19,23.67,5.73,28.01,5.82,55.75-4.02,83-.9,2.48-1.98,4.9-3.12,7.28-1.2,2.53-1.99,5.7-6.12,4.34-3.86-1.28-2.78-4.2-2.27-6.87,1.29-6.79,2.33-13.59,2.98-20.42l.02.04c.06-.67.1-1.32.16-1.98.1-1.18.17-2.36.24-3.54.06-.99.11-1.96.15-2.91.02-.49.04-.97.06-1.46.78-21.63-2.85-31.46-4.23-34.37-.15-.36-.32-.68-.51-.97h0s0,0,0,0c-1.43-2.14-3.8-1.89-5.84.13-3.76,3.72-5.84,8.1-4.88,13.62,2.8,16.09,1.16,32.03-1.84,47.9-.41,2.13-1.36,6-5.9,5.01-3.09-.68-3.81-2.01-3.99-4.69.03-2.03.01-4.05-.06-6.08,0-.05,0-.1,0-.15h0c-.01-.29-.03-.57-.04-.86v-.02c0-.14,0-.27-.02-.4-.13-2.76-.36-5.53-.7-8.3-.03-.27-.08-.53-.12-.79-1.74-15.62-4-17.13-4-17.13-1.45-1.88-3.71-1.57-5.67.38-3.76,3.72-5.67,8.08-4.88,13.62.57,4.06.43,2.81.84,6.34.33,1.82.66,5.13.69,6.19-.09.94-.32,1.76-.9,2.37-1.92,2.07-5.02-.05-7.37-1.02-45.52-18.84-84.49-45.28-118.5-78.71C29.51,74.47,6.74,46.89,6.74,46.89h0c-.84-.99-1.91-1.55-3.53-.85C.24,47.32.33,51.13.06,54.33c-.54,6.41,2.88,11.07,6.62,15.42,51.36,59.92,114.05,102.98,189.7,124.51l13.61,3.61c.16.04.32.08.48.12.03,0,.05.02.07.02l11.72,3.11.32.08c-.38.11-.82.2-1.28.28-12.9,2.55-38.42-2.14-58.91-6.92-10.15-2.13-20.1-4.71-29.85-7.79-.45-.13-.69-.2-.69-.2v-.02c-37.88-12.05-72.58-31.59-102.92-61.4-2.87-2.82-5.54-5.86-8.15-8.95-2.41-2.86-7.36-8.84-9.06-10.89-.19-.27-.39-.51-.6-.73h0s0,0,0,0c-.52-.53-1.14-.87-2.03-.66-2.12.49-2.72,2.67-3.11,4.51-1.55,7.39.8,13.59,5.76,19.15,31.09,34.84,70.09,57.1,113.9,71.7,24.88,8.29,50.46,13.32,76.57,16.54-15.56,5.04-31.58,6.57-47.72,6.17-31.26-.78-60.57-8.29-88.12-21.68-10.16-5.22-19.62-11.05-22.11-12.6-1.43-.98-2.9-1.57-4.36-.45-2.74,2.12-.85,5.85.03,8.76,1.69,5.6,5.58,9.47,10.63,12.14,44.88,23.74,92.26,33.22,142.71,24.8,5.11-.85,9.95-1.79,15.29-3.59-8.43,7.3-18.2,12.06-28.47,15.82-31.59,11.56-62.98,11.09-94.25,3.27-10.03-2.69-21.68-7.05-21.68-7.05h0c-1.68-.73-3.34-.99-4.64.87-2.28,3.27-.29,6.66,1.68,9.74,4.67,7.27,13.68,7.98,20.81,10.44,2.44.77-4.2,5.21-6.34,6.84-10.34,7.91-20.46,15.14-30.76,22.8l-6.74,4.97h0c-1.16.8-2.18,1.69-1.64,3.37.61,1.88,2.57,2.22,4.47,2.62,7.37,1.53,13.66-.92,19.48-5.27,12.48-9.35,25.18-18.41,37.39-28.11,4.64-3.7,8.86-3.39,15.21-1.74-15.88,11.97-30.73,23.17-45.6,34.36-15.08,11.35-30.18,22.7-45.28,34.03l-9.98,7.38c-.15.1-.29.21-.43.32l-.15.11h0c-.85.68-1.48,1.44-1.3,2.44.4,2.25,3.05,2.81,5.21,3.18,8.92,1.54,14.44-1.82,20.54-6.39,30.5-22.9,61.12-45.64,91.44-68.76,6.8-5.18,13.79-8.11,23.61-7.01-8.36,6.25-16.38,12.24-24.3,18.16l-21.51,15.92c-.15.11-.3.22-.45.33h-.02c-1.14.9-1.94,1.96-1.49,3.53.82,2.84,4.24,3.18,7.15,3.62,5.34.8,9.87-1.09,14.06-4.21,2.41-1.8,4.84-3.57,7.28-5.33h0s32.84-26.08,32.84-26.08c0,0,7.76-5.54,16.74-10.64.8-.5,1.61-1,2.41-1.49.34-.15,1.2-.54,2.48-1.16.97-.5,1.93-.99,2.89-1.44,1.41-.72,3.05-1.59,4.88-2.59,5.3-2.2,20.44-9.27,32.98-22.62,5.96-4.6,14.34-10.6,20.87-13.49h0s.04-.02.04-.02c.5-.22.98-.42,1.46-.6h0s.03,0,.06-.02c.32-.12.63-.23.93-.33l.84-.33c2.36-.67,6.22-.92,6.71,4.29.09,1.28.06,2.59-.08,3.97-.11,1.04-.3,2.14-.46,3.02-.15.85.2,1.71.88,2.21.11.08.22.15.34.21.9.44,1.99.24,2.66-.51.25-.28.51-.55.77-.83,3.22-3.38,6.47-5.73,9.95-7.16,5.07-2.1,10.2-2.11,15.68-.02,2.6.99,5.05,2.34,7.48,4.14,1.03.76,2.08,1.62,3.11,2.55.61.56,1.22,1.18,1.76,1.72l.09.09.44.45c.08.08.17.16.26.22.52.38,1.18.53,1.82.39.75-.16,1.37-.69,1.63-1.41.05-.14.1-.28.15-.41,1.56-4.59,1.87-8.82.97-12.93Z"}),e("path",{className:"cls-4",d:"m208.42,169.5c-.37,2.28-.76,4.55-1.19,6.82.43-2.27.82-4.55,1.19-6.82h0Z"}),e("path",{className:"cls-4",d:"m248.79,194.81c.16.07.33.13.5.19-.17-.06-.33-.13-.5-.19"}),e("path",{className:"cls-4",d:"m230.37,180.81s0,0,0,.01c0,0,0,0,0-.01"}),e("path",{className:"cls-4",d:"m230.5,180.5s-.03.06-.04.1c.01-.03.03-.07.04-.1"}),e("path",{className:"cls-4",d:"m255.55,180.46s-.05.08-.08.13c.03-.04.05-.08.08-.13"}),e("path",{className:"cls-4",d:"m215.62,178.85c-.28.59-.54,1.22-.82,1.82.28-.59.54-1.22.82-1.82"}),e("path",{className:"cls-4",d:"m188.53,177.51s.01,0,.02,0c0,0-.01,0-.02,0"}),e("polyline",{className:"cls-4",points:"184.47 175.68 184.47 175.69 184.47 175.68"}),e("polyline",{className:"cls-4",points:"184.45 175.66 184.46 175.66 184.45 175.66"}),e("polyline",{className:"cls-4",points:"184.43 175.62 184.44 175.64 184.43 175.62"}),e("path",{className:"cls-4",d:"m184.42,175.6s0,0,0,.01c0,0,0,0,0-.01"}),e("path",{className:"cls-4",d:"m184.39,175.57s.01.02.02.03c0-.01-.01-.02-.02-.03"}),e("path",{className:"cls-4",d:"m183.65,172.72s0,.01,0,.02c0,0,0-.01,0-.02"}),e("path",{className:"cls-4",d:"m193.79,171c-.08.46-.17.91-.26,1.37.09-.46.17-.91.26-1.37"}),e("path",{className:"cls-4",d:"m168.79,167.86c-.3.32-.63.54-.99.68.35-.14.68-.36.99-.68"}),e("path",{className:"cls-5",d:"m184.47,175.69c.25.35.57.64.99.9h0c-.42-.25-.74-.55-.99-.9m-.02-.03s0,.01.01.02c0,0,0-.01-.01-.02m-.02-.02v.02s0-.01,0-.02m-.01-.02s0,0,0,0c0,0,0,0,0,0m-.01-.01s0,0,0,0c0,0,0,0,0,0m-.02-.04s0,0,0,0c0,0,0,0,0,0m-.74-2.82s0,.01,0,.01c0,0,0,0,0-.01m0-.06h0s0,.03,0,.04c0-.01,0-.02,0-.04m-19.74-4.71s.03.01.04.02c.95.41,1.9.74,2.79.74.37,0,.73-.06,1.06-.19-.34.13-.69.19-1.06.19-.9,0-1.87-.34-2.83-.75m19.61-2.97s0,.01,0,.02c0,0,0-.01,0-.02"}),e("path",{className:"cls-5",d:"m249.29,195c.08.03.16.06.24.09h0c-.08-.03-.16-.06-.24-.09m-18.14-7.32s0,0-.01,0c0,0,.01,0,.01,0m-2.75-1.47c0,.64.22,1.23.85,1.66.23.16.47.23.71.23.38,0,.77-.16,1.17-.41-.4.25-.79.41-1.17.41-.25,0-.49-.07-.72-.23-.63-.43-.85-1.02-.85-1.66m1.33-3.84c-.04.08-.07.17-.11.25.04-.08.07-.17.11-.25m.64-1.54c-.21.51-.42,1.02-.64,1.53.22-.51.43-1.02.64-1.53m.09-.23c-.03.07-.06.14-.09.22.03-.07.06-.14.09-.22m25.01-.01s-.01.02-.02.03c0-.01.01-.02.02-.03m.1-.16s-.01.02-.02.03c0-.01.01-.02.02-.03m-25.03-.01s-.03.06-.04.09c.01-.03.02-.06.04-.09m-23.84-.69c0,1.46.59,2.74,2.81,3.47.68.23,1.28.33,1.8.33,1.87,0,2.77-1.32,3.5-2.85-.73,1.53-1.62,2.85-3.5,2.85-.52,0-1.11-.1-1.8-.33-2.22-.73-2.8-2.01-2.81-3.47m-18.18-2.21h.01-.01m3.63-1.49c-.67.87-1.65,1.51-3.14,1.51-.15,0-.3,0-.46-.02.16.01.31.02.46.02,1.48,0,2.47-.63,3.14-1.51m28.75-10.95s-.01,0-.02,0c-.66,2.17-1.35,4.33-2.13,6.49-.9,2.48-1.98,4.9-3.12,7.28h0c1.13-2.38,2.22-4.8,3.12-7.28.78-2.16,1.5-4.33,2.16-6.49m-25.9-1.2c-.36,2.38-.76,4.75-1.2,7.12.44-2.37.84-4.75,1.2-7.12h0m58.07-11.39s0,0,0,0c-3.26,10.69-8.32,20.76-16.37,29.77-.96,1.08-1.99,2.08-3.02,3.1h0c1.03-1.01,2.06-2.02,3.02-3.1,8.05-9.02,13.12-19.09,16.38-29.78"}),e("path",{className:"cls-10",d:"m4.56,45.73c-.4,0-.85.09-1.34.31-2.11.91-2.68,3.11-2.93,5.45,11.33,14.85,56.07,69.62,126.46,107.18,0,0,68.91,36.38,138.24,40.31-5.37-.73-10.17-1.93-14.65-3.59-.26-.1-.53-.19-.8-.29h0c-25.19-5.44-46.66-12.25-61.84-17.7.29.06.57.1.84.13-.28-.03-.57-.07-.88-.14-.92-.2-1.62-.46-2.17-.79-12.01-4.39-19.66-7.76-21.51-8.59-.88-.38-1.75-.83-2.53-1.15-45.52-18.84-84.49-45.28-118.5-78.71C29.51,74.47,6.74,46.89,6.74,46.89h0c-.58-.68-1.28-1.16-2.18-1.16"}),e("path",{className:"cls-8",d:"m9.57,103.87c-.16,0-.33.02-.51.06-2.12.49-2.72,2.67-3.11,4.51-.07.33-.13.66-.18.99,35.19,47.67,82.41,67.15,82.41,67.15,47.15,22.21,85.84,26.69,109.4,26.69,9.75,0,16.91-.77,21.01-1.37-1.87.21-3.93.31-6.14.31-13.81,0-33.56-3.79-50.06-7.64-10.15-2.13-20.1-4.71-29.85-7.79-.45-.13-.69-.2-.69-.2v-.02c-37.88-12.05-72.58-31.59-102.92-61.4-2.87-2.82-5.54-5.86-8.15-8.95-2.41-2.86-7.36-8.84-9.06-10.89-.19-.27-.39-.51-.6-.73h0s0,0,0,0c-.41-.42-.9-.72-1.53-.72"}),e("path",{className:"cls-9",d:"m41.57,186.66c-.56,0-1.13.18-1.69.61-2.39,1.85-1.26,4.91-.35,7.6,17.64,10.71,58.1,31.53,106.02,31.53,18.09,0,37.24-2.97,56.64-10.57-14,4.54-28.37,6.23-42.87,6.23-1.61,0-3.23-.02-4.85-.06-31.26-.78-60.57-8.29-88.12-21.68-10.16-5.22-19.62-11.05-22.11-12.6-.88-.6-1.78-1.06-2.68-1.06"}),e("path",{className:"cls-12",d:"m205.41,231.93c-7.68,5.89-16.32,9.97-25.34,13.27-16.95,6.2-33.84,8.94-50.68,8.94-14.56,0-29.08-2.05-43.57-5.67-10.03-2.69-21.68-7.05-21.68-7.05h0c-.74-.32-1.47-.55-2.17-.55-.9,0-1.74.38-2.47,1.42-1.06,1.52-1.2,3.07-.85,4.6,11.13,5.17,35,14.36,64.11,14.36,25.24,0,54.41-6.9,82.66-29.31"}),e("path",{className:"cls-7",d:"m130.35,268.02c-27.34,0-48.01-5.54-50.62-6.27.77.23,1.52.46,2.26.71,2.44.77-4.2,5.21-6.34,6.84-7.65,5.85-15.17,11.32-22.73,16.88h23.2c7.31-5.4,14.6-10.84,21.72-16.5,2.65-2.11,5.15-2.91,7.99-2.91,2.15,0,4.48.46,7.22,1.17-15.88,11.97-30.73,23.17-45.6,34.36-8.69,6.54-17.39,13.07-26.09,19.61h23.34c20.99-15.71,41.97-31.42,62.82-47.32,4.81-3.67,9.71-6.2,15.64-6.98-4.39.29-8.67.41-12.8.41Z"}),e("path",{className:"cls-6",d:"m125.47,286.75h22.55l16.66-13.24s7.76-5.54,16.74-10.64c.8-.5,1.61-1,2.41-1.49.34-.15,1.2-.54,2.48-1.16.97-.5,1.93-.99,2.89-1.44,1.46-.75,3.18-1.65,5.09-2.71-16.08,6.73-32.54,10.02-47.79,11.29.21,0,.42,0,.63,0,1.28,0,2.61.07,3.99.23-8.36,6.25-16.38,12.24-24.3,18.16l-1.36,1Z"}),e("path",{className:"cls-11",d:"m183.65,172.69c.03-2.03.01-4.05-.06-6.08v-.15s0,0,0,0c-.01-.29-.03-.57-.04-.86v-.02s-.02-.4-.02-.4c-.08-1.7-.21-3.41-.37-5.12-5.38-2.26-10.45-5.15-15.12-8.56.03.48.05.96.12,1.46.57,4.06.43,2.81.84,6.34.33,1.82.66,5.13.69,6.19-.09.94-.32,1.76-.9,2.37-.59.63-1.29.87-2.05.87-.9,0-1.87-.34-2.83-.75,1.78.8,9.45,4.19,21.55,8.61-1.3-.79-1.69-2.01-1.81-3.9Z"}),e("path",{className:"cls-13",d:"m271.38,134.41c-5.03,7.01-11.24,13.15-18.32,18.08-3.26,10.69-8.32,20.76-16.37,29.77-.96,1.08-1.99,2.08-3.02,3.1-1,.97-2.45,2.73-3.7,2.73-.25,0-.49-.07-.72-.23-1.84-1.28-.2-3.9.37-5.25,3.02-7.06,5.33-14.23,7.04-21.49-5.04,1.89-10.33,3.22-15.79,3.96-.66,2.17-1.35,4.33-2.13,6.49-.9,2.48-1.98,4.9-3.12,7.28-1,2.11-1.72,4.67-4.32,4.67-.52,0-1.11-.1-1.8-.33-3.86-1.28-2.78-4.2-2.27-6.87.67-3.54,1.27-7.08,1.79-10.63-4.8-.15-9.49-.77-14.03-1.82-.43,2.83-.92,5.67-1.46,8.49-.36,1.89-1.16,5.17-4.53,5.17-.4,0-.85-.05-1.33-.15,15.19,5.45,36.66,12.26,61.84,17.71h0c-.25-.1-.5-.19-.74-.29-4.02-1.69,3.23-8.92,6.55-14.03,9.35-14.37,13.92-30.09,16.03-46.36Z"}),e("path",{className:"cls-2",d:"m267.61,212.35c-3.15,0-6.32.3-9.44.88-.59.11-1.17.16-1.72.16-.89,0-1.72-.13-2.5-.37.13.16.25.3.37.47,1.37,1.9,2.08,3.98,2.35,6.14.34.37.63.84.86,1.43h0s0,.02.01.03c0,0,0,0,0,0,0,0,0,.01,0,.02,0,0,0,0,0,0,0,0,0,.01,0,.02,0,0,0,0,0,0,0,0,0,.01,0,.02,0,0,0,0,0,0,0,0,0,.01,0,.02,0,0,0,0,0,0,0,0,0,.01,0,.02,0,0,0,0,0,.01,0,0,0,.01,0,.02,0,0,0,0,0,.01,0,0,0,0,0,.01,0,0,0,0,0,.01,0,0,0,.01,0,.01,0,0,0,0,0,0,0,0,0,.01,0,.02,0,0,0,0,0,.01,0,0,0,0,0,0v.02s0,0,0,.01c0,0,0,.01,0,.02,0,0,0,0,0,.01,0,0,0,.01,0,.02,0,0,0,0,0,0,0,0,0,.01,0,.02,0,0,0,0,0,0,0,0,0,.02,0,.02,0,0,0,0,0,0,0,0,0,.01,0,.02,0,0,0,0,0,0,0,.01,0,.02,0,.03,0,0,0,0,0,0,0,0,0,0,0,.01t0,0s0,.02,0,.03c0,0,0,0,0,0,0,0,0,.02,0,.03,0,0,0,0,0,0,0,0,0,.01,0,.02,0,0,0,0,0,.01,0,0,0,0,0,.02,0,0,0,.01,0,.02,0,0,0,.01,0,.01,0,0,0,.01,0,.01,0,0,0,.01,0,.02,0,0,0,.01,0,.01,0,0,0,0,0,.02s0,.01,0,.02c0,0,0,0,0,.01,0,0,0,.01,0,.02,0,0,0,0,0,.01,0,0,0,.01,0,.02,0,0,0,.01,0,.01s0,.01,0,.01c0,0,0,0,0,.01,0,0,0,.01,0,.02,0,0,0,0,0,.01,0,0,0,.01,0,.02,0,0,0,0,0,.01,0,0,0,.01,0,.02,0,0,0,0,0,.01,0,0,0,.01,0,.02,0,0,0,0,0,.01,0,0,0,.01,0,.02,0,0,0,0,0,0,0,0,0,.02,0,.03,0,0,0,0,0,0,0,0,0,.02,0,.03,0,0,0,0,0,0,0,0,0,.02,0,.02,0,0,0,0,0,0,0,.01,0,.02,0,.03,0,0,0,0,0,0,0,0,0,.02,0,.03,0,0,0,0,0,0,0,0,0,.02,0,.03h0s0,.03,0,.04h0s0,.02,0,.03h0s0,.03,0,.03h0s0,.03,0,.04h0s0,.02,0,.03h0s0,.02,0,.03h0s0,.02,0,.03h0s0,.02,0,.04c0,0,0,0,0,0,0,.03.01.07.01.1h0s0,.03,0,.04h0s0,.07.01.11h0s0,.02,0,.04h0s0,.03,0,.04h0s0,.05,0,.07h0s0,.02,0,.04h0s0,.03,0,.04h0s0,.03,0,.04h0c.03.5.05,1,.05,1.52,0,.8-.04,1.61-.13,2.46-.11,1.04-.3,2.14-.46,3.02-.02.13-.04.27-.04.4,0,.71.34,1.39.92,1.81l.34.21c.32.16.66.23,1,.23.62,0,1.23-.26,1.67-.74.25-.28.51-.55.77-.83,3.22-3.38,6.47-5.73,9.95-7.16,2.54-1.05,5.1-1.58,7.71-1.58s5.24.52,7.96,1.56c2.6.99,5.05,2.34,7.48,4.14,1.03.76,2.08,1.62,3.11,2.55.61.56,1.22,1.18,1.76,1.72l.09.09.44.45.26.22c.38.28.83.43,1.3.44-2.15-4.61-4.88-8.9-8.73-12.24-7.28-6.31-16.46-8.98-25.8-8.98"}),e("path",{className:"cls-14",d:"m266.74,181.67l-.41.04c-.97.18-1.72.97-1.83,1.96-.09.76-.08,1.57.02,2.41.03.26-.03.52-.16.73,3.89,5.78,12.33,16.03,25.15,19.91,0,0,19.81,10.36,14.8,25.38h0l.15-.41c1.56-4.59,1.87-8.82.97-12.93-.9-4.06-2.96-7.8-6.14-11.13-1.22-1.28-2.59-2.48-4.07-3.58-.72-.53-1.48-1.03-2.26-1.52-.97-.6-1.98-1.19-3.07-1.75-4.05-2.08-7.5-4.17-10.53-6.41-1.23-.91-2.42-1.86-3.53-2.83-2.71-2.37-4.53-4.38-5.88-6.53-.44-.69-.83-1.44-1.2-2.14-.16-.31-.39-.57-.66-.77-.38-.28-.85-.44-1.34-.44"}),e("path",{className:"cls-3",d:"m241.61,223.53l4.01-2.33,16.87-22.61s-9.24-1.75-13.7-3.78c0,0-4.64,21.12-21.73,38.76l6.3-4.67c2.51-1.76,4.79-3.29,8.24-5.37Z"})]})]})}function d5({className:n}){return e("svg",{width:"90",height:"30",viewBox:"0 0 50 13",fill:"none",xmlns:"http://www.w3.org/2000/svg",className:n,children:e("path",{d:"M3.25 0.582999C4.12267 0.582999 4.82533 0.900333 5.358 1.535C5.902 2.15833 6.174 2.98 6.174 4C6.174 4.99733 5.91333 5.802 5.392 6.414C4.87067 7.026 4.185 7.332 3.335 7.332H1.737C1.69167 7.332 1.669 7.35467 1.669 7.4V12.33C1.669 12.4433 1.61233 12.5 1.499 12.5H0.207C0.0936667 12.5 0.0370001 12.4433 0.0370001 12.33V0.752999C0.0370001 0.639666 0.0936667 0.582999 0.207 0.582999H3.25ZM2.995 6.023C3.45967 6.023 3.83367 5.84733 4.117 5.496C4.40033 5.13333 4.542 4.646 4.542 4.034C4.542 3.41067 4.40033 2.91767 4.117 2.555C3.83367 2.181 3.45967 1.994 2.995 1.994H1.737C1.69167 1.994 1.669 2.01667 1.669 2.062V5.955C1.669 6.00033 1.69167 6.023 1.737 6.023H2.995ZM12.0589 0.769999C12.0589 0.656666 12.1156 0.599999 12.2289 0.599999H13.5209C13.6343 0.599999 13.6909 0.656666 13.6909 0.769999V12.33C13.6909 12.4433 13.6343 12.5 13.5209 12.5H12.2289C12.1156 12.5 12.0589 12.4433 12.0589 12.33V7.315C12.0589 7.26967 12.0363 7.247 11.9909 7.247H9.42392C9.37859 7.247 9.35592 7.26967 9.35592 7.315V12.33C9.35592 12.4433 9.29926 12.5 9.18592 12.5H7.89392C7.78059 12.5 7.72392 12.4433 7.72392 12.33V0.769999C7.72392 0.656666 7.78059 0.599999 7.89392 0.599999H9.18592C9.29926 0.599999 9.35592 0.656666 9.35592 0.769999V5.768C9.35592 5.81333 9.37859 5.836 9.42392 5.836H11.9909C12.0363 5.836 12.0589 5.81333 12.0589 5.768V0.769999ZM18.6483 12.636C17.7189 12.636 16.9709 12.3527 16.4043 11.786C15.8376 11.2193 15.5543 10.4657 15.5543 9.525V3.592C15.5543 2.65133 15.8376 1.89767 16.4043 1.331C16.9709 0.753 17.7189 0.464 18.6483 0.464C19.5889 0.464 20.3426 0.753 20.9093 1.331C21.4873 1.89767 21.7763 2.65133 21.7763 3.592V9.525C21.7763 10.4657 21.4873 11.2193 20.9093 11.786C20.3426 12.3527 19.5889 12.636 18.6483 12.636ZM18.6483 11.225C19.1016 11.225 19.4643 11.0777 19.7363 10.783C20.0083 10.477 20.1443 10.0803 20.1443 9.593V3.507C20.1443 3.01967 20.0083 2.62867 19.7363 2.334C19.4643 2.028 19.1016 1.875 18.6483 1.875C18.2063 1.875 17.8493 2.028 17.5773 2.334C17.3166 2.62867 17.1863 3.01967 17.1863 3.507V9.593C17.1863 10.0803 17.3166 10.477 17.5773 10.783C17.8493 11.0777 18.2063 11.225 18.6483 11.225ZM29.3398 1.841C29.3398 1.95433 29.2832 2.011 29.1698 2.011H25.3448C25.2995 2.011 25.2768 2.03367 25.2768 2.079V5.768C25.2768 5.81333 25.2995 5.836 25.3448 5.836H27.6908C27.8042 5.836 27.8608 5.89267 27.8608 6.006V7.077C27.8608 7.19033 27.8042 7.247 27.6908 7.247H25.3448C25.2995 7.247 25.2768 7.26967 25.2768 7.315V11.021C25.2768 11.0663 25.2995 11.089 25.3448 11.089H29.1698C29.2832 11.089 29.3398 11.1457 29.3398 11.259V12.33C29.3398 12.4433 29.2832 12.5 29.1698 12.5H23.8148C23.7015 12.5 23.6448 12.4433 23.6448 12.33V0.769999C23.6448 0.656666 23.7015 0.599999 23.8148 0.599999H29.1698C29.2832 0.599999 29.3398 0.656666 29.3398 0.769999V1.841ZM35.7767 0.769999C35.7767 0.656666 35.8334 0.599999 35.9467 0.599999H37.2217C37.335 0.599999 37.3917 0.656666 37.3917 0.769999V12.33C37.3917 12.4433 37.335 12.5 37.2217 12.5H35.7597C35.669 12.5 35.6067 12.4547 35.5727 12.364L32.6827 4.595C32.6714 4.57233 32.6544 4.56667 32.6317 4.578C32.609 4.578 32.5977 4.58933 32.5977 4.612L32.6147 12.33C32.6147 12.4433 32.558 12.5 32.4447 12.5H31.1527C31.0394 12.5 30.9827 12.4433 30.9827 12.33V0.769999C30.9827 0.656666 31.0394 0.599999 31.1527 0.599999H32.5977C32.6884 0.599999 32.7507 0.645333 32.7847 0.735999L35.6917 8.505C35.703 8.539 35.72 8.556 35.7427 8.556C35.7654 8.54467 35.7767 8.522 35.7767 8.488V0.769999ZM39.6693 12.5C39.556 12.5 39.4993 12.4433 39.4993 12.33V0.769999C39.4993 0.656666 39.556 0.599999 39.6693 0.599999H40.9613C41.0746 0.599999 41.1313 0.656666 41.1313 0.769999V12.33C41.1313 12.4433 41.0746 12.5 40.9613 12.5H39.6693ZM42.8947 12.5C42.838 12.5 42.7927 12.483 42.7587 12.449C42.736 12.4037 42.736 12.3527 42.7587 12.296L45.1217 6.601C45.1443 6.567 45.1443 6.533 45.1217 6.499L42.7587 0.804L42.7417 0.735999C42.7417 0.645333 42.7927 0.599999 42.8947 0.599999H44.2207C44.3113 0.599999 44.3737 0.645333 44.4077 0.735999L45.9547 4.833C45.966 4.867 45.983 4.884 46.0057 4.884C46.0283 4.884 46.0453 4.867 46.0567 4.833L47.5867 0.735999C47.6207 0.645333 47.683 0.599999 47.7737 0.599999H49.0997C49.1563 0.599999 49.196 0.622666 49.2187 0.667999C49.2527 0.702 49.2583 0.747333 49.2357 0.804L46.8727 6.516C46.8613 6.55 46.8613 6.584 46.8727 6.618L49.2357 12.296L49.2527 12.364C49.2527 12.4547 49.2017 12.5 49.0997 12.5H47.7907C47.7 12.5 47.6377 12.4547 47.6037 12.364L46.0567 8.284C46.0453 8.25 46.0283 8.233 46.0057 8.233C45.983 8.233 45.966 8.25 45.9547 8.284L44.4077 12.364C44.3737 12.4547 44.3113 12.5 44.2207 12.5H42.8947Z",fill:"var(--ac-global-text-color-900)"})})}const u5=m`
  padding: var(--ac-global-dimension-static-size-100);
  background-color: var(--ac-global-color-grey-100);
  flex: none;
  display: flex;
  flex-direction: row;
  justify-content: flex-start;
  align-items: center;
  gap: var(--ac-global-dimension-static-size-100);
`,g5=m`
  padding: var(--ac-global-dimension-static-size-200)
    var(--ac-global-dimension-static-size-100);
  background-color: var(--ac-global-color-grey-100);
  flex: none;
  display: flex;
  flex-direction: column;
  box-sizing: border-box;
  height: 100vh;
  width: var(--px-nav-collapsed-width);
  transition: width 0.15s cubic-bezier(0, 0.57, 0.21, 0.99);
  &[data-expanded="true"] {
    width: var(--px-nav-expanded-width);
  }
  &[data-expanded="false"] {
    .brand-text-wrap {
      opacity: 0;
    }
  }
`,za=m`
  width: 100%;
  color: var(--ac-global-color-grey-500);
  background-color: transparent;
  border-radius: var(--ac-global-rounding-small);
  display: flex;
  flex-direction: row;
  align-items: center;
  overflow: hidden;
  transition:
    color 0.2s ease-in-out,
    background-color 0.2s ease-in-out;
  text-decoration: none;
  cursor: pointer;

  &.active {
    color: var(--ac-global-text-color-900);
    background-color: var(--ac-global-color-grey-200);
  }
  &:hover:not(.active) {
    color: var(--ac-global-text-color-900);
    background-color: var(--ac-global-color-grey-200);
  }
  & > .ac-icon-wrap {
    padding: var(--ac-global-dimension-size-100);
    display: inline-block;
  }
  .ac-text {
    padding-inline-start: var(--ac-global-dimension-size-50);
    padding-inline-end: var(--ac-global-dimension-size-100);
    white-space: nowrap;
  }
`,m5=m`
  color: var(--ac-global-text-color-900);
  font-size: var(--ac-global-font-size-xl);
  text-decoration: none;
  margin: 0 0 var(--ac-global-dimension-static-size-200) 0;
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: var(--ac-global-dimension-static-size-150);
  overflow: hidden;
  & > * {
    flex: none;
  }
  .brand-text-wrap {
    opacity: 1;
    transition: all 0.8s ease-in-out;
    display: flex;
    flex-direction: row;
    align-items: center;
  }
`;function Bt(n){return s(R,{delay:0,isDisabled:n.isExpanded,children:[e(te,{children:s("a",{href:n.href,target:n.replaceTab?void 0:"_blank",css:za,rel:"noreferrer",role:"button",children:[n.leadingVisual,e(C,{children:n.text}),n.trailingVisual]})}),e(ke,{placement:"right",offset:10,children:n.text})]})}function Fm({isExpanded:n}){return e(Bt,{href:"https://arize.com/docs/phoenix",leadingVisual:e(T,{svg:e(Lc,{})}),text:"Documentation",isExpanded:n})}function Em({isExpanded:n}){return e(Bt,{href:"https://github.com/Arize-ai/phoenix",leadingVisual:e(T,{svg:e(Kc,{})}),trailingVisual:e(s5,{}),text:"Star on GitHub",isExpanded:n})}function Dm({isExpanded:n}){const{theme:a,setTheme:t}=le(),l=a==="dark";return s(R,{delay:0,isDisabled:n,children:[e(te,{children:s("button",{css:za,onClick:()=>t(l?"light":"dark"),className:"button--reset",children:[e(T,{svg:l?e(Rc,{}):e(Xc,{})}),e(C,{children:l?"Dark":"Light"})]})}),e(ke,{placement:"right",offset:10,children:l?"Dark":"Light"})]})}function _m(){return s(ua,{to:"/",css:m5,title:`version: ${window.Config.platformVersion}`,children:[e(c5,{}),e("div",{className:"brand-text-wrap",children:e(d5,{className:"brand-text"})})]})}function Km({children:n}){return e("nav",{css:u5,children:n})}function Pm({children:n,isExpanded:a}){return e("nav",{"data-expanded":a,css:g5,children:n})}function Vm(n){return s(R,{delay:0,isDisabled:n.isExpanded,children:[e(te,{children:e("div",{role:"button",children:s(I1,{to:n.to,css:za,children:[n.leadingVisual,e(C,{children:n.text})]})})}),e(ke,{placement:"right",offset:10,children:n.text})]})}function Rm(n){return s("button",{className:"button--reset",css:za,onClick:n.onClick,children:[n.leadingVisual,e(C,{children:n.text})]})}const Om=({isExpanded:n})=>{const{viewer:a}=xn();return a!=null&&a.isManagementUser&&window.Config.managementUrl?e("li",{children:e(Bt,{href:window.Config.managementUrl,leadingVisual:e(T,{svg:e(Gc,{})}),text:"Management Console",replaceTab:!0,isExpanded:n})},"management"):null};function p5(n){var a;return typeof n.handle=="object"&&typeof((a=n.handle)==null?void 0:a.crumb)=="function"}function Nm(){const a=z1().filter(p5);return e(t2,{size:"L",children:a.map((t,l)=>e(e2,{children:e(ua,{to:t.pathname,children:t.handle.crumb(t.data)})},l))})}function $m(){const{isSideNavExpanded:n,setIsSideNavExpanded:a}=Ge(t=>({isSideNavExpanded:t.isSideNavExpanded,setIsSideNavExpanded:t.setIsSideNavExpanded}));return s(R,{children:[e(v0,{size:"S",onPress:()=>a(!n),"aria-label":n?"Collapse side":"Expand side",children:e(T,{svg:n?e(Wc,{}):e(qc,{})})}),e(ke,{placement:"bottom",offset:10,children:n?"Collapse":"Expand"})]})}const Cr=(function(){var n={alias:null,args:null,kind:"ScalarField",name:"maxCount",storageKey:null},a={alias:null,args:null,kind:"ScalarField",name:"maxDays",storageKey:null};return{argumentDefinitions:[],kind:"Fragment",metadata:null,name:"ProjectTraceRetentionPolicySelectFragment",selections:[{alias:null,args:null,concreteType:"ProjectTraceRetentionPolicyConnection",kind:"LinkedField",name:"projectTraceRetentionPolicies",plural:!1,selections:[{alias:null,args:null,concreteType:"ProjectTraceRetentionPolicyEdge",kind:"LinkedField",name:"edges",plural:!0,selections:[{alias:null,args:null,concreteType:"ProjectTraceRetentionPolicy",kind:"LinkedField",name:"node",plural:!1,selections:[{alias:null,args:null,kind:"ScalarField",name:"id",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"name",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"cronExpression",storageKey:null},{alias:null,args:null,concreteType:null,kind:"LinkedField",name:"rule",plural:!1,selections:[{kind:"InlineFragment",selections:[n],type:"TraceRetentionRuleMaxCount",abstractKey:null},{kind:"InlineFragment",selections:[a],type:"TraceRetentionRuleMaxDays",abstractKey:null},{kind:"InlineFragment",selections:[a,n],type:"TraceRetentionRuleMaxDaysOrCount",abstractKey:null}],storageKey:null}],storageKey:null}],storageKey:null}],storageKey:null}],type:"Query",abstractKey:null}})();Cr.hash="319a452afbbe089cfba02eaf9722b595";function Bm({defaultValue:n,onChange:a,query:t,isDisabled:l}){const r=M.useFragment(Cr,t).projectTraceRetentionPolicies.edges.map(o=>o.node);return s(Ne,{size:"S",defaultSelectedKey:n,onSelectionChange:o=>{o&&(a==null||a(o.toString()))},isDisabled:l,children:[e(K,{children:"Retention Policy"}),s(z,{children:[e(Oe,{}),e(Ae,{})]}),e(ue,{children:e(we,{children:r.map(o=>e(ee,{id:o.id,children:o.name},o.id))})})]})}const kr=(function(){var n={defaultValue:null,kind:"LocalArgument",name:"connections"},a={defaultValue:null,kind:"LocalArgument",name:"label"},t=[{kind:"Variable",name:"input",variableName:"label"}],l={alias:null,args:null,concreteType:"PromptLabel",kind:"LinkedField",name:"promptLabels",plural:!0,selections:[{alias:null,args:null,kind:"ScalarField",name:"id",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"name",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"color",storageKey:null}],storageKey:null};return{fragment:{argumentDefinitions:[n,a],kind:"Fragment",metadata:null,name:"NewPromptLabelDialogMutation",selections:[{alias:null,args:t,concreteType:"PromptLabelMutationPayload",kind:"LinkedField",name:"createPromptLabel",plural:!1,selections:[l],storageKey:null}],type:"Mutation",abstractKey:null},kind:"Request",operation:{argumentDefinitions:[a,n],kind:"Operation",name:"NewPromptLabelDialogMutation",selections:[{alias:null,args:t,concreteType:"PromptLabelMutationPayload",kind:"LinkedField",name:"createPromptLabel",plural:!1,selections:[l,{alias:null,args:null,filters:null,handle:"prependNode",key:"",kind:"LinkedHandle",name:"promptLabels",handleArgs:[{kind:"Variable",name:"connections",variableName:"connections"},{kind:"Literal",name:"edgeTypeName",value:"PromptLabelEdge"}]}],storageKey:null}]},params:{cacheID:"c61bebc2bf20d8cf12760e79bfd8205b",id:null,metadata:{},name:"NewPromptLabelDialogMutation",operationKind:"mutation",text:`mutation NewPromptLabelDialogMutation(
  $label: CreatePromptLabelInput!
) {
  createPromptLabel(input: $label) {
    promptLabels {
      id
      name
      color
    }
  }
}
`}}})();kr.hash="ddbd14ff91d53dfbceede5ee349cb9ab";const h5=p.forwardRef((n,a)=>e(M1,{...n,ref:a}));h5.displayName="ColorField";const f5=m`
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: var(--ac-global-dimension-size-100);
  flex-wrap: wrap;

  .react-aria-ColorSwatchPickerItem {
    position: relative;
    outline: none;
    width: fit-content;
    height: fit-content;
    forced-color-adjust: none;
    display: inline-flex;

    &[data-focus-visible] {
      outline: 2px solid var(--focus-ring-color);
      outline-offset: 2px;
    }

    &[data-selected]::after {
      content: "";
      position: absolute;
      inset: 0;
      border: 2px solid var(--ac-global-text-color-900);
      outline-offset: -4px;
      border-radius: inherit;
    }
  }
`,Lr=p.forwardRef((n,a)=>e(F1,{css:f5,...n,ref:a}));Lr.displayName="ColorSwatchPicker";function b5({onSubmit:n,isSubmitting:a}){const{control:t,handleSubmit:l,watch:i,formState:{isDirty:r}}=Re({defaultValues:{name:"",description:"",color:"#33c5e8"}});return s(on,{onSubmit:l(n),children:[s(w,{padding:"size-200",children:[e(w,{paddingY:"size-300",children:e(S,{direction:"row",alignItems:"center",justifyContent:"center",width:"100%",children:e(je,{color:i("color"),children:i("name")||"label preview"})})}),e($,{name:"name",control:t,rules:{required:"label name is required",minLength:{value:1,message:"label name must be at least 1 character long"},maxLength:{value:30,message:"label name must be less than 30 characters long"}},render:({field:{onChange:o,onBlur:c,value:d},fieldState:{invalid:u,error:g}})=>s(Q,{isInvalid:u,onChange:o,onBlur:c,value:d.toString(),children:[e(K,{children:"Label Name"}),e(j,{placeholder:"e.x. classifier"}),g!=null&&g.message?e(W,{children:g.message}):e(C,{slot:"description",children:"The name of the label"})]})}),e($,{name:"description",control:t,render:({field:{onChange:o,onBlur:c,value:d},fieldState:{invalid:u,error:g}})=>s(Q,{isInvalid:u,onChange:o,onBlur:c,value:d.toString(),children:[e(K,{children:"Description"}),e(ma,{placeholder:"A short description"}),g!=null&&g.message?e(W,{children:g.message}):e(C,{slot:"description",children:"The description of the label"})]})}),e($,{name:"color",control:t,render:({field:{onChange:o,value:c}})=>s("div",{css:Le,children:[e(K,{children:"Color"}),s(Lr,{value:c,onChange:d=>o(d.toString()),children:[e(ye,{color:"#ff9b88",children:e(me,{size:"L"})}),e(ye,{color:"#ffa037",children:e(me,{size:"L"})}),e(ye,{color:"#d7b300",children:e(me,{size:"L"})}),e(ye,{color:"#98c50a",children:e(me,{size:"L"})}),e(ye,{color:"#4ecf50",children:e(me,{size:"L"})}),e(ye,{color:"#49cc93",children:e(me,{size:"L"})}),e(ye,{color:"#33c5e8",children:e(me,{size:"L"})}),e(ye,{color:"#78bbfa",children:e(me,{size:"L"})}),e(ye,{color:"#acafff",children:e(me,{size:"L"})}),e(ye,{color:"#cca4fd",children:e(me,{size:"L"})}),e(ye,{color:"#f592f3",children:e(me,{size:"L"})}),e(ye,{color:"#ff95bd",children:e(me,{size:"L"})})]})]})})]}),e(w,{paddingEnd:"size-200",paddingTop:"size-100",paddingBottom:"size-200",children:e(S,{direction:"row",justifyContent:"end",children:e(z,{isDisabled:a,variant:r?"primary":"default",size:"M",type:"submit",children:"Create Label"})})})]})}function y5(n){const[a,t]=p.useState(""),{onCompleted:l}=n,[i,r]=M.useMutation(kr);return e(be,{children:s(Ke,{children:[s(Pe,{children:[e(Ve,{children:"New Prompt Label"}),e(Qe,{})]}),a?e(ya,{banner:!0,variant:"danger",children:a}):null,e(b5,{onSubmit:c=>{const d=[M.ConnectionHandler.getConnectionID("client:root","PromptLabelConfigButtonAllLabels_promptLabels"),M.ConnectionHandler.getConnectionID("client:root","PromptLabelsTable__promptLabels")];i({variables:{label:c,connections:d},onCompleted:l,onError:u=>{const g=$t(u);t((g==null?void 0:g[0])??u.message)}})},isSubmitting:r})]})})}const v5={lineNumbers:!0,highlightActiveLine:!1,foldGutter:!1,highlightActiveLineGutter:!1,bracketMatching:!1,defaultKeymap:!1},C5=[ft.lineWrapping,si.of([...ci.filter(n=>n.key!=="Mod-Enter")])],Hm=({templateFormat:n,defaultValue:a,readOnly:t,...l})=>{const[i,r]=p.useState(()=>a),{theme:o}=le(),c=o==="light"?Hn:jn,d=p.useMemo(()=>{const u=[...C5];switch(n){case Ze.FString:u.push(Y2());break;case Ze.Mustache:u.push(au());break;case Ze.NONE:break;default:P()}return u},[n]);return p.useEffect(()=>{t&&r(a)},[t,a]),e(Zn,{theme:c,extensions:d,basicSetup:v5,readOnly:t,...l,value:i})},jm=({readOnly:n,children:a})=>e("div",{css:m`
        & .cm-editor,
        & .cm-gutters {
          background-color: ${n?"transparent !important":"auto"};
        }
        & .cm-gutters {
          border-right: none !important;
        }
        & .cm-content {
          padding: var(--ac-global-dimension-size-100)
            var(--ac-global-dimension-size-250);
        }
        & .cm-gutter,
        & .cm-content {
          min-height: ${n?"100%":"75px"};
        }
        & .cm-line {
          padding-left: 0;
          padding-right: 0;
        }
        & .cm-cursor {
          display: ${n?"none !important":"auto"};
        }
      `,children:a});function k5({blocker:n}){return e(w,{padding:"size-100",borderTopColor:"dark",borderTopWidth:"thin",children:s(S,{justifyContent:"end",gap:"size-100",children:[e(z,{onPress:()=>n.reset&&n.reset(),size:"S",children:"Cancel"}),e(z,{variant:"primary",onPress:()=>n.proceed&&n.proceed(),size:"S",children:"Confirm"})]})})}function Zm({blocker:n,message:a="Are you sure you want to leave the page? Some changes may not be saved."}){return e(Cn,{isDismissable:!1,isOpen:n.state==="blocked",children:e(vn,{children:e(be,{children:s(Ke,{children:[s(Pe,{children:[e(Ve,{children:"Confirm Navigation"}),e(ln,{children:e(Qe,{close:()=>{var t;return(t=n.reset)==null?void 0:t.call(n)}})})]}),e(w,{padding:"size-200",children:e(C,{children:a})}),e(k5,{blocker:n})]})})})})}const Um=m`
  transition: 250ms linear all;
  background-color: var(--ac-global-color-grey-200);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1.8px;
  --px-resize-handle-size: 8px;
  --px-resize-icon-width: 24px;
  --px-resize-icon-height: 2px;
  outline: none;
  &[data-panel-group-direction="vertical"] {
    height: var(--px-resize-handle-size);
    flex-direction: column;
    &:before,
    &:after {
      width: var(--px-resize-icon-width);
      height: var(--px-resize-icon-height);
    }
  }
  &[data-panel-group-direction="horizontal"] {
    width: var(--px-resize-handle-size);
    flex-direction: row;
    &:before,
    &:after {
      width: var(--px-resize-icon-height);
      height: var(--px-resize-icon-width);
    }
  }

  &:hover {
    background-color: var(--ac-global-color-grey-300);
    border-radius: 4px;
    &:before,
    &:after {
      background-color: var(--ac-global-color-primary);
    }
  }

  &:before,
  &:after {
    content: "";
    color: var(--color-solid-resize-bar);
    flex: 0 0 1rem;
    border-radius: 6px;
    background-color: var(--ac-global-color-grey-300);
    flex: none;
  }
`,L5=m`
  transition: 250ms linear all;
  background-color: var(--ac-global-color-grey-200);
  --px-resize-handle-size: 4px;
  outline: none;
  &[data-panel-group-direction="vertical"] {
    height: var(--px-resize-handle-size);
  }
  &[data-panel-group-direction="horizontal"] {
    width: var(--px-resize-handle-size);
  }

  &:hover {
    background-color: var(--ac-global-color-primary);
  }
`;function w5({latencyMs:n,size:a="M",showIcon:t=!0}){const l=p.useMemo(()=>n<3e3?"success":n<8e3?"warning":"danger",[n]),i=p.useMemo(()=>n<10?We(n)+"ms":We(n/1e3)+"s",[n]);return s(S,{direction:"row",alignItems:"center",justifyContent:"start",gap:"size-50",className:"latency-text",children:[t?e(C,{color:l,size:a,children:e(T,{svg:e(zc,{}),css:m`
              font-size: 1.1em;
            `})}):null,e(C,{color:l,size:a,fontFamily:"mono",children:i})]})}function S5(n){const a=65+n;return String.fromCharCode(a)}function Gm({index:n}){const a=p.useMemo(()=>S5(n),[n]),t=p.useMemo(()=>E1[n%8],[n]),l=p.useMemo(()=>ht(.8,t),[t]);return e("div",{css:m`
        color: ${t};
        background-color: ${l};
        width: 24px;
        height: 24px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        border-radius: var(--ac-global-rounding-small);
      `,children:a})}function wr({spanKind:n}){const{theme:a}=le(),t=a==="dark";let l=t?"--ac-global-color-grey-600":"--ac-global-color-grey-200";switch(n){case"llm":l=t?"--ac-global-color-orange-1000":"--ac-global-color-orange-500";break;case"chain":l=t?"--ac-global-color-blue-1000":"--ac-global-color-blue-500";break;case"retriever":l=t?"--ac-global-color-seafoam-1000":"--ac-global-color-seafoam-500";break;case"embedding":l=t?"--ac-global-color-indigo-1000":"--ac-global-color-indigo-500";break;case"agent":l=t?"--ac-global-color-grey-600":"--ac-global-color-grey-300";break;case"tool":l=t?"--ac-global-color-yellow-1200":"--ac-global-color-yellow-500";break;case"reranker":l=t?"--ac-global-color-celery-1000":"--ac-global-color-celery-500";break;case"evaluator":l=t?"--ac-global-color-indigo-1000":"--ac-global-color-indigo-500";break;case"guardrail":l=t?"--ac-global-color-fuchsia-1200":"--ac-global-color-fuchsia-500";break}return`var(${l})`}const x5=()=>s("svg",{width:"20",height:"20",viewBox:"0 0 20 20",fill:"none",xmlns:"http://www.w3.org/2000/svg",children:[e("rect",{x:"0.5",y:"0.5",width:"19",height:"19",rx:"3.5",stroke:"currentColor",strokeOpacity:"0.9"}),e("mask",{id:"path-2-inside-1_33_16916",fill:"currentColor",children:e("path",{fillRule:"evenodd",clipRule:"evenodd",d:"M13 8C13 8.64491 12.8779 9.2613 12.6556 9.82732L17.1924 14.3641L14.364 17.1926L9.82706 12.6557C9.26111 12.8779 8.64481 13 8 13C5.23858 13 3 10.7614 3 8C3 7.13361 3.22036 6.31869 3.60809 5.60822L6 8L7.5 7.50016L8 6.00016L5.60803 3.60819C6.31854 3.2204 7.13353 3 8 3C10.7614 3 13 5.23858 13 8Z"})}),e("path",{d:"M12.6556 9.82732L11.7248 9.46171L11.4853 10.0713L11.9485 10.5344L12.6556 9.82732ZM17.1924 14.3641L17.8995 15.0713L18.6066 14.3641L17.8995 13.657L17.1924 14.3641ZM14.364 17.1926L13.6569 17.8997L14.364 18.6068L15.0711 17.8997L14.364 17.1926ZM9.82706 12.6557L10.5342 11.9486L10.0711 11.4855L9.4615 11.7249L9.82706 12.6557ZM3.60809 5.60822L4.31518 4.90109L3.37037 3.95634L2.7303 5.12917L3.60809 5.60822ZM6 8L5.29291 8.70713L5.72988 9.14407L6.31613 8.94871L6 8ZM7.5 7.50016L7.81614 8.44888L8.29055 8.29079L8.44869 7.81639L7.5 7.50016ZM8 6.00016L8.94869 6.31639L9.14413 5.73007L8.70711 5.29306L8 6.00016ZM5.60803 3.60819L5.12895 2.73042L3.95616 3.37053L4.90093 4.3153L5.60803 3.60819ZM13.5863 10.1929C13.8537 9.51235 14 8.77206 14 8H12C12 8.51776 11.9021 9.01026 11.7248 9.46171L13.5863 10.1929ZM17.8995 13.657L13.3627 9.12022L11.9485 10.5344L16.4853 15.0713L17.8995 13.657ZM15.0711 17.8997L17.8995 15.0713L16.4853 13.657L13.6569 16.4855L15.0711 17.8997ZM9.11995 13.3628L13.6569 17.8997L15.0711 16.4855L10.5342 11.9486L9.11995 13.3628ZM8 14C8.77194 14 9.51211 13.8537 10.1926 13.5865L9.4615 11.7249C9.0101 11.9022 8.51768 12 8 12V14ZM2 8C2 11.3137 4.68629 14 8 14V12C5.79086 12 4 10.2091 4 8H2ZM2.7303 5.12917C2.2644 5.98288 2 6.96206 2 8H4C4 7.30516 4.17633 6.65449 4.48588 6.08727L2.7303 5.12917ZM6.70709 7.29287L4.31518 4.90109L2.901 6.31535L5.29291 8.70713L6.70709 7.29287ZM7.18387 6.55145L5.68387 7.05129L6.31613 8.94871L7.81614 8.44888L7.18387 6.55145ZM7.05132 5.68394L6.55132 7.18394L8.44869 7.81639L8.94869 6.31639L7.05132 5.68394ZM4.90093 4.3153L7.2929 6.70727L8.70711 5.29306L6.31514 2.90109L4.90093 4.3153ZM8 2C6.96197 2 5.98271 2.26444 5.12895 2.73042L6.08712 4.48596C6.65437 4.17636 7.3051 4 8 4V2ZM14 8C14 4.68629 11.3137 2 8 2V4C10.2091 4 12 5.79086 12 8H14Z",fill:"currentColor",fillOpacity:"0.9",mask:"url(#path-2-inside-1_33_16916)"})]}),T5=()=>s("svg",{width:"20",height:"20",viewBox:"0 0 20 20",fill:"none",xmlns:"http://www.w3.org/2000/svg",children:[e("rect",{x:"0.5",y:"0.5",width:"19",height:"19",rx:"3.5",fill:"currentColor",stroke:"currentColor"}),e("mask",{id:"path-2-inside-1_2321_643",fill:"white",children:e("path",{fillRule:"evenodd",clipRule:"evenodd",d:"M13 8C13 8.64491 12.8779 9.2613 12.6556 9.82732L17.1924 14.3641L14.364 17.1926L9.82706 12.6557C9.26111 12.8779 8.64481 13 8 13C5.23858 13 3 10.7614 3 8C3 7.13361 3.22036 6.31869 3.60809 5.60822L6 8L7.5 7.50016L8 6.00016L5.60803 3.60819C6.31854 3.2204 7.13353 3 8 3C10.7614 3 13 5.23858 13 8Z"})}),e("path",{d:"M12.6556 9.82732L11.7248 9.46171L11.4853 10.0713L11.9485 10.5344L12.6556 9.82732ZM17.1924 14.3641L17.8995 15.0713L18.6066 14.3641L17.8995 13.657L17.1924 14.3641ZM14.364 17.1926L13.6569 17.8997L14.364 18.6068L15.0711 17.8997L14.364 17.1926ZM9.82706 12.6557L10.5342 11.9486L10.0711 11.4855L9.4615 11.7249L9.82706 12.6557ZM3.60809 5.60822L4.31518 4.90109L3.37037 3.95634L2.7303 5.12917L3.60809 5.60822ZM6 8L5.29291 8.70713L5.72988 9.14407L6.31613 8.94871L6 8ZM7.5 7.50016L7.81614 8.44888L8.29055 8.29079L8.44869 7.81639L7.5 7.50016ZM8 6.00016L8.94869 6.31639L9.14413 5.73007L8.70711 5.29306L8 6.00016ZM5.60803 3.60819L5.12895 2.73042L3.95616 3.37053L4.90093 4.3153L5.60803 3.60819ZM13.5863 10.1929C13.8537 9.51235 14 8.77206 14 8H12C12 8.51776 11.9021 9.01026 11.7248 9.46171L13.5863 10.1929ZM17.8995 13.657L13.3627 9.12022L11.9485 10.5344L16.4853 15.0713L17.8995 13.657ZM15.0711 17.8997L17.8995 15.0713L16.4853 13.657L13.6569 16.4855L15.0711 17.8997ZM9.11995 13.3628L13.6569 17.8997L15.0711 16.4855L10.5342 11.9486L9.11995 13.3628ZM8 14C8.77194 14 9.51211 13.8537 10.1926 13.5865L9.4615 11.7249C9.0101 11.9022 8.51768 12 8 12V14ZM2 8C2 11.3137 4.68629 14 8 14V12C5.79086 12 4 10.2091 4 8H2ZM2.7303 5.12917C2.2644 5.98288 2 6.96206 2 8H4C4 7.30516 4.17633 6.65449 4.48588 6.08727L2.7303 5.12917ZM6.70709 7.29287L4.31518 4.90109L2.901 6.31535L5.29291 8.70713L6.70709 7.29287ZM7.18387 6.55145L5.68387 7.05129L6.31613 8.94871L7.81614 8.44888L7.18387 6.55145ZM7.05132 5.68394L6.55132 7.18394L8.44869 7.81639L8.94869 6.31639L7.05132 5.68394ZM4.90093 4.3153L7.2929 6.70727L8.70711 5.29306L6.31514 2.90109L4.90093 4.3153ZM8 2C6.96197 2 5.98271 2.26444 5.12895 2.73042L6.08712 4.48596C6.65437 4.17636 7.3051 4 8 4V2ZM14 8C14 4.68629 11.3137 2 8 2V4C10.2091 4 12 5.79086 12 8H14Z",fill:"black",mask:"url(#path-2-inside-1_2321_643)"})]}),A5=()=>s("svg",{width:"20",height:"20",viewBox:"0 0 20 20",fill:"none",xmlns:"http://www.w3.org/2000/svg",children:[e("rect",{x:"0.5",y:"0.5",width:"19",height:"19",rx:"3.5",stroke:"currentColor",strokeOpacity:"0.9"}),e("path",{d:"M4.43782 6.78868L10 3.57735L15.5622 6.78868V13.2113L10 16.4226L4.43782 13.2113V6.78868Z",stroke:"currentColor",strokeOpacity:"0.9"})]}),I5=()=>s("svg",{width:"20",height:"20",viewBox:"0 0 20 20",fill:"none",xmlns:"http://www.w3.org/2000/svg",children:[e("rect",{x:"0.5",y:"0.5",width:"19",height:"19",rx:"3.5",fill:"currentColor",stroke:"currentColor"}),e("path",{d:"M4.43782 6.78868L10 3.57735L15.5622 6.78868V13.2113L10 16.4226L4.43782 13.2113V6.78868Z",stroke:"black"})]}),z5=()=>s("svg",{width:"20",height:"20",viewBox:"0 0 20 20",fill:"none",xmlns:"http://www.w3.org/2000/svg",children:[e("rect",{x:"0.5",y:"0.5",width:"19",height:"19",rx:"3.5",stroke:"currentColor",strokeOpacity:"0.9"}),e("path",{d:"M5 16C5 16 5 11 10 11C15 11 15 16 15 16",stroke:"currentColor",strokeOpacity:"0.9"}),e("rect",{x:"6.5",y:"4.5",width:"7",height:"5",rx:"0.5",stroke:"currentColor",strokeOpacity:"0.9"})]}),M5=()=>s("svg",{width:"20",height:"20",viewBox:"0 0 20 20",fill:"none",xmlns:"http://www.w3.org/2000/svg",children:[e("rect",{width:"20",height:"20",rx:"4",fill:"currentColor"}),e("path",{d:"M10 11C5 11 5 16 5 16H15C15 16 15 11 10 11Z",stroke:"black"}),e("rect",{x:"6.5",y:"4.5",width:"7",height:"5",rx:"0.5",stroke:"black"})]}),F5=()=>s("svg",{width:"20",height:"20",viewBox:"0 0 20 20",fill:"none",xmlns:"http://www.w3.org/2000/svg",children:[e("rect",{x:"0.5",y:"0.5",width:"19",height:"19",rx:"3.5",stroke:"currentColor",strokeOpacity:"0.9"}),e("path",{fillRule:"evenodd",clipRule:"evenodd",d:"M10 6C10 7.10457 9.10457 8 8 8C6.89543 8 6 7.10457 6 6C6 4.89543 6.89543 4 8 4C9.10457 4 10 4.89543 10 6ZM10.0558 8.18487C9.51887 8.6903 8.7956 9 8 9C7.91155 9 7.824 8.99617 7.7375 8.98867L7.10304 11.2093C8.21409 11.6488 9 12.7326 9 14C9 15.6569 7.65685 17 6 17C4.34315 17 3 15.6569 3 14C3 12.3431 4.34315 11 6 11C6.0409 11 6.08161 11.0008 6.12212 11.0024L6.76944 8.73682C5.72625 8.26703 5 7.21833 5 6C5 4.34315 6.34315 3 8 3C9.65685 3 11 4.34315 11 6C11 6.50075 10.8773 6.97285 10.6604 7.38788L12.1873 8.6094C12.6908 8.22697 13.3189 8 14 8C15.6569 8 17 9.34315 17 11C17 12.6569 15.6569 14 14 14C12.3431 14 11 12.6569 11 11C11 10.3864 11.1842 9.81579 11.5004 9.34053L10.0558 8.18487ZM16 11C16 12.1046 15.1046 13 14 13C12.8954 13 12 12.1046 12 11C12 9.89543 12.8954 9 14 9C15.1046 9 16 9.89543 16 11ZM6 16C7.10457 16 8 15.1046 8 14C8 12.8954 7.10457 12 6 12C4.89543 12 4 12.8954 4 14C4 15.1046 4.89543 16 6 16Z",fill:"currentColor",fillOpacity:"0.9"})]}),E5=()=>s("svg",{width:"20",height:"20",viewBox:"0 0 20 20",fill:"none",xmlns:"http://www.w3.org/2000/svg",children:[e("rect",{x:"0.5",y:"0.5",width:"19",height:"19",rx:"3.5",fill:"currentColor",stroke:"currentColor"}),e("path",{fillRule:"evenodd",clipRule:"evenodd",d:"M10 6.00003C10 7.1046 9.10457 8.00003 8 8.00003C6.89543 8.00003 6 7.1046 6 6.00003C6 4.89546 6.89543 4.00003 8 4.00003C9.10457 4.00003 10 4.89546 10 6.00003ZM10.0558 8.1849C9.51887 8.69033 8.7956 9.00003 8 9.00003C7.91155 9.00003 7.824 8.9962 7.7375 8.9887L7.10304 11.2093C8.21409 11.6488 9 12.7326 9 14C9 15.6569 7.65685 17 6 17C4.34315 17 3 15.6569 3 14C3 12.3432 4.34315 11 6 11C6.0409 11 6.08161 11.0008 6.12212 11.0025L6.76944 8.73685C5.72625 8.26706 5 7.21836 5 6.00003C5 4.34318 6.34315 3.00003 8 3.00003C9.65685 3.00003 11 4.34318 11 6.00003C11 6.50078 10.8773 6.97288 10.6604 7.38791L12.1873 8.60943C12.6908 8.227 13.3189 8.00003 14 8.00003C15.6569 8.00003 17 9.34318 17 11C17 12.6569 15.6569 14 14 14C12.3431 14 11 12.6569 11 11C11 10.3864 11.1842 9.81582 11.5004 9.34056L10.0558 8.1849ZM16 11C16 12.1046 15.1046 13 14 13C12.8954 13 12 12.1046 12 11C12 9.89546 12.8954 9.00003 14 9.00003C15.1046 9.00003 16 9.89546 16 11ZM6 16C7.10457 16 8 15.1046 8 14C8 12.8955 7.10457 12 6 12C4.89543 12 4 12.8955 4 14C4 15.1046 4.89543 16 6 16Z",fill:"black"})]}),D5=()=>s("svg",{width:"20",height:"20",viewBox:"0 0 20 20",fill:"none",xmlns:"http://www.w3.org/2000/svg",children:[e("rect",{x:"0.5",y:"0.5",width:"19",height:"19",rx:"3.5",stroke:"currentColor",strokeOpacity:"0.9"}),e("path",{d:"M14.65 6.5C14.65 6.98637 14.2466 7.52091 13.379 7.95472C12.5323 8.37806 11.3382 8.65 10 8.65C8.66184 8.65 7.46767 8.37806 6.62099 7.95472C5.75338 7.52091 5.35 6.98637 5.35 6.5C5.35 6.01363 5.75338 5.47909 6.62099 5.04528C7.46767 4.62194 8.66184 4.35 10 4.35C11.3382 4.35 12.5323 4.62194 13.379 5.04528C14.2466 5.47909 14.65 6.01363 14.65 6.5Z",stroke:"currentColor",strokeOpacity:"0.9",strokeWidth:"0.7"}),e("path",{d:"M14.6875 6.83482V9.62479C14.6875 9.62479 13.0769 11.1873 10 11.1873C6.92308 11.1873 5.3125 9.62479 5.3125 9.62479V6.7437",stroke:"currentColor",strokeOpacity:"0.9",strokeWidth:"0.7"}),e("path",{d:"M14.6875 9.625V12.125C14.6875 12.125 13.0769 13.6875 10 13.6875C6.92308 13.6875 5.3125 12.125 5.3125 12.125V9.625",stroke:"currentColor",strokeOpacity:"0.9",strokeWidth:"0.7"}),e("path",{d:"M14.6875 12.125V14.625C14.6875 14.625 13.0769 16.1875 10 16.1875C6.92308 16.1875 5.3125 14.625 5.3125 14.625V12.125",stroke:"currentColor",strokeOpacity:"0.9",strokeWidth:"0.7"})]}),_5=()=>s("svg",{width:"20",height:"20",viewBox:"0 0 20 20",fill:"none",xmlns:"http://www.w3.org/2000/svg",children:[e("rect",{x:"0.5",y:"0.5",width:"19",height:"19",rx:"3.5",fill:"currentColor",stroke:"currentColor"}),e("path",{d:"M14.65 6.5C14.65 6.98637 14.2466 7.52091 13.379 7.95472C12.5323 8.37806 11.3382 8.65 10 8.65C8.66184 8.65 7.46767 8.37806 6.62099 7.95472C5.75338 7.52091 5.35 6.98637 5.35 6.5C5.35 6.01363 5.75338 5.47909 6.62099 5.04528C7.46767 4.62194 8.66184 4.35 10 4.35C11.3382 4.35 12.5323 4.62194 13.379 5.04528C14.2466 5.47909 14.65 6.01363 14.65 6.5Z",stroke:"black",strokeWidth:"0.7"}),e("path",{d:"M14.6875 6.83504V9.625C14.6875 9.625 13.0769 11.1875 10 11.1875C6.92308 11.1875 5.3125 9.625 5.3125 9.625V6.74392",stroke:"black",strokeWidth:"0.7"}),e("path",{d:"M14.6875 9.625V12.125C14.6875 12.125 13.0769 13.6875 10 13.6875C6.92308 13.6875 5.3125 12.125 5.3125 12.125V9.625",stroke:"black",strokeWidth:"0.7"}),e("path",{d:"M14.6875 12.125V14.625C14.6875 14.625 13.0769 16.1875 10 16.1875C6.92308 16.1875 5.3125 14.625 5.3125 14.625V12.125",stroke:"black",strokeWidth:"0.7"})]}),K5=()=>s("svg",{width:"20",height:"20",viewBox:"0 0 20 20",fill:"none",xmlns:"http://www.w3.org/2000/svg",children:[e("rect",{x:"0.5",y:"0.5",width:"19",height:"19",rx:"3.5",stroke:"currentColor"}),e("path",{d:"M4.5359 10L8 4L11.4641 10H4.5359Z",stroke:"currentColor"}),e("path",{d:"M8.5359 10L12 16L15.4641 10H8.5359Z",stroke:"currentColor"})]}),P5=()=>s("svg",{width:"20",height:"20",viewBox:"0 0 20 20",fill:"none",xmlns:"http://www.w3.org/2000/svg",children:[e("rect",{x:"0.5",y:"0.5",width:"19",height:"19",rx:"3.5",fill:"currentColor",stroke:"currentColor"}),e("path",{d:"M4.5359 10L8 4L11.4641 10H4.5359Z",stroke:"black"}),e("path",{d:"M8.5359 10L12 16L15.4641 10H8.5359Z",stroke:"black"})]}),V5=()=>s("svg",{width:"20",height:"20",viewBox:"0 0 20 20",fill:"none",xmlns:"http://www.w3.org/2000/svg",children:[e("rect",{x:"0.5",y:"0.5",width:"19",height:"19",rx:"3.5",stroke:"currentColor",strokeOpacity:"0.9"}),e("path",{fillRule:"evenodd",clipRule:"evenodd",d:"M10 15C12.7614 15 15 12.7614 15 10C15 7.23858 12.7614 5 10 5C7.23858 5 5 7.23858 5 10C5 12.7614 7.23858 15 10 15ZM10 16C13.3137 16 16 13.3137 16 10C16 6.68629 13.3137 4 10 4C6.68629 4 4 6.68629 4 10C4 13.3137 6.68629 16 10 16Z",fill:"currentColor",fillOpacity:"0.9"})]}),R5=()=>s("svg",{width:"20",height:"20",viewBox:"0 0 20 20",fill:"none",xmlns:"http://www.w3.org/2000/svg",children:[e("rect",{x:"0.5",y:"0.5",width:"19",height:"19",rx:"3.5",fill:"currentColor",stroke:"currentColor"}),e("path",{fillRule:"evenodd",clipRule:"evenodd",d:"M10 15C12.7614 15 15 12.7614 15 10C15 7.23858 12.7614 5 10 5C7.23858 5 5 7.23858 5 10C5 12.7614 7.23858 15 10 15ZM10 16C13.3137 16 16 13.3137 16 10C16 6.68629 13.3137 4 10 4C6.68629 4 4 6.68629 4 10C4 13.3137 6.68629 16 10 16Z",fill:"black"})]}),O5=()=>e("svg",{width:"20",height:"20",viewBox:"0 0 20 20",fill:"none",xmlns:"http://www.w3.org/2000/svg",children:e("rect",{x:"0.5",y:"0.5",width:"19",height:"19",rx:"3.5",stroke:"currentColor",strokeOpacity:"0.9"})}),N5=()=>e("svg",{width:"20",height:"20",viewBox:"0 0 20 20",fill:"none",xmlns:"http://www.w3.org/2000/svg",children:e("rect",{x:"0.5",y:"0.5",width:"19",height:"19",rx:"3.5",fill:"currentColor",stroke:"currentColor"})}),$5=()=>s("svg",{width:"20",height:"20",viewBox:"0 0 20 20",fill:"none",xmlns:"http://www.w3.org/2000/svg",children:[e("rect",{x:"0.5",y:"0.5",width:"19",height:"19",rx:"3.5",stroke:"currentColor"}),e("path",{d:"M14.4254 5.58523L15.744 6.87427L15.7249 6.89333L15.7043 6.91394L15.6837 6.93453L15.6631 6.95509L15.6425 6.97562L15.622 6.99612L15.6015 7.01659L15.581 7.03703L15.5606 7.05745L15.5402 7.07783L15.5198 7.09819L15.4995 7.11852L15.4791 7.13882L15.4588 7.15909L15.4386 7.17934L15.4183 7.19956L15.3981 7.21974L15.3779 7.23991L15.3578 7.26004L15.3377 7.28015L15.3176 7.30022L15.2975 7.32028L15.2774 7.3403L15.2574 7.3603L15.2374 7.38027L15.2175 7.40021L15.1975 7.42013L15.1776 7.44002L15.1577 7.45988L15.1379 7.47972L15.118 7.49953L15.0982 7.51931L15.0784 7.53907L15.0587 7.5588L15.0389 7.57851L15.0192 7.59819L14.9996 7.61785L14.9799 7.63748L14.9603 7.65708L14.9407 7.67666L14.9211 7.69621L14.9016 7.71574L14.882 7.73524L14.8625 7.75472L14.8431 7.77417L14.8236 7.7936L14.8042 7.81301L14.7848 7.83239L14.7654 7.85174L14.746 7.87107L14.7267 7.89038L14.7074 7.90966L14.6881 7.92892L14.6689 7.94815L14.6496 7.96736L14.6304 7.98655L14.6113 8.00571L14.5921 8.02485L14.573 8.04397L14.5538 8.06306L14.5347 8.08213L14.5157 8.10118L14.4966 8.1202L14.4776 8.1392L14.4586 8.15818L14.4396 8.17714L14.4207 8.19607L14.4017 8.21498L14.3828 8.23387L14.3639 8.25274L14.3451 8.27158L14.3262 8.2904L14.3074 8.3092L14.2886 8.32798L14.2698 8.34674L14.2511 8.36547L14.2323 8.38418L14.2136 8.40288L14.1949 8.42155L14.1763 8.4402L14.1576 8.45883L14.139 8.47743L14.1204 8.49602L14.1018 8.51459L14.0832 8.53313L14.0647 8.55166L14.0462 8.57016L14.0277 8.58864L14.0092 8.60711L13.9907 8.62555L13.9723 8.64397L13.9538 8.66238L13.9354 8.68076L13.917 8.69913L13.8987 8.71747L13.8803 8.73579L13.862 8.7541L13.8437 8.77239L13.8254 8.79065L13.8071 8.8089L13.7889 8.82713L13.7707 8.84534L13.7524 8.86353L13.7343 8.8817L13.7161 8.89986L13.6979 8.91799L13.6798 8.93611L13.6617 8.95421L13.6436 8.97229L13.6255 8.99036L13.6074 9.0084L13.5894 9.02643L13.5713 9.04444L13.5533 9.06243L13.5353 9.0804L13.5173 9.09836L13.4994 9.1163L13.4814 9.13422L13.4635 9.15213L13.4456 9.17002L13.4277 9.18789L13.4098 9.20574L13.392 9.22358L13.3741 9.2414L13.3563 9.25921L13.3385 9.277L13.3207 9.29477L13.3029 9.31253L13.2852 9.33027L13.2674 9.34799L13.2497 9.3657L13.232 9.38339L13.2143 9.40107L13.1966 9.41873L13.1789 9.43638L13.1613 9.45401L13.1436 9.47163L13.126 9.48923L13.1084 9.50681L13.0908 9.52438L13.0733 9.54194L13.0557 9.55948L13.0381 9.57701L13.0206 9.59452L13.0031 9.61202L12.9856 9.6295L12.9681 9.64697L12.9506 9.66443L12.9332 9.68187L12.9157 9.6993L12.8983 9.71671L12.8809 9.73412L12.8634 9.7515L12.8461 9.76888L12.8287 9.78624L12.8113 9.80358L12.794 9.82092L12.7766 9.83824L12.7593 9.85555L12.742 9.87284L12.7247 9.89013L12.7074 9.9074L12.6901 9.92466L12.6728 9.9419L12.6556 9.95913L12.6383 9.97636L12.6211 9.99356L12.6039 10.0108L12.5867 10.0279L12.5695 10.0451L12.5523 10.0623L12.5351 10.0794L12.518 10.0966L12.5008 10.1137L12.4837 10.1308L12.4666 10.1479L12.4495 10.165L12.4324 10.1821L12.4153 10.1992L12.3982 10.2162L12.3811 10.2333L12.364 10.2503L12.347 10.2674L12.33 10.2844L12.3129 10.3014L12.2959 10.3184L12.2789 10.3354L12.2619 10.3524L12.2449 10.3693L12.2279 10.3863L12.211 10.4032L12.194 10.4202L12.177 10.4371L12.1601 10.454L12.1432 10.471L12.1262 10.4879L12.1093 10.5048L12.0924 10.5216L12.0755 10.5385L12.0586 10.5554L12.0417 10.5723L12.0249 10.5891L12.008 10.606L11.9911 10.6228L11.9743 10.6396L11.9575 10.6565L11.9406 10.6733L11.9238 10.6901L11.907 10.7069L11.8902 10.7237L11.8734 10.7404L11.8566 10.7572L11.8398 10.774L11.823 10.7907L11.8062 10.8075L11.7895 10.8243L11.7727 10.841L11.7559 10.8577L11.7392 10.8745L11.7225 10.8912L11.7057 10.9079L11.689 10.9246L11.6723 10.9413L11.6556 10.958L11.6389 10.9747L11.6221 10.9914L11.6054 11.0081L11.5888 11.0247L11.5721 11.0414L11.5554 11.0581L11.5387 11.0747L11.522 11.0914L11.5054 11.108L11.4887 11.1247L11.4721 11.1413L11.4554 11.1579L11.4388 11.1746L11.4221 11.1912L11.4055 11.2078L11.3888 11.2244L11.3722 11.241L11.3556 11.2576L11.339 11.2742L11.3224 11.2908L11.3057 11.3074L11.2891 11.324L11.2725 11.3406L11.2559 11.3572L11.2393 11.3738L11.2227 11.3903L11.2061 11.4069L11.1895 11.4235L11.173 11.44L11.1564 11.4566L11.1398 11.4732L11.1232 11.4897L11.1066 11.5063L11.0901 11.5228L11.0735 11.5394L11.0569 11.5559L11.0404 11.5725L11.0238 11.589L11.0072 11.6056L10.9907 11.6221L10.9741 11.6386L10.9576 11.6552L10.941 11.6717L10.9245 11.6883L10.9079 11.7048L10.8914 11.7213L10.8748 11.7378L10.8583 11.7544L10.8417 11.7709L10.8252 11.7874L10.8086 11.804L10.7921 11.8205L10.7755 11.837L10.759 11.8535L10.7424 11.8701L10.7259 11.8866L10.7094 11.9031L10.6928 11.9196L10.6763 11.9362L10.6597 11.9527L10.6432 11.9692L10.6266 11.9857L10.6101 12.0023L10.5935 12.0188L10.577 12.0353L10.5604 12.0519L10.5439 12.0684L10.5273 12.0849L10.5108 12.1015L10.4942 12.118L10.4777 12.1345L10.4611 12.1511L10.4446 12.1676L10.428 12.1841L10.4114 12.2007L10.3949 12.2172L10.3783 12.2338L10.3618 12.2503L10.3452 12.2669L10.3286 12.2834L10.312 12.3L10.2955 12.3165L10.2789 12.3331L10.2623 12.3497L10.2457 12.3662L10.2291 12.3828L10.2125 12.3994L10.1959 12.4159L10.1793 12.4325L10.1627 12.4491L10.1461 12.4657L10.1295 12.4823L10.1129 12.4989L10.0963 12.5155L10.0797 12.5321L10.0631 12.5487L10.0464 12.5653L10.0298 12.5819L10.0132 12.5985L9.99652 12.6151L9.97987 12.6318L9.96322 12.6484L9.94657 12.665L9.92991 12.6817L9.91324 12.6983L9.89657 12.715L9.87989 12.7316L9.86321 12.7483L9.84653 12.7649L9.82984 12.7816L9.81314 12.7983L9.79644 12.815L9.77973 12.8317L9.76301 12.8484L9.74629 12.8651L9.72957 12.8818L9.71283 12.8985L9.69609 12.9152L9.67935 12.9319L9.6626 12.9487L9.64584 12.9654L9.62907 12.9822L9.6123 12.9989L9.59552 13.0157L9.57873 13.0324L9.56194 13.0492L9.54514 13.066L9.52833 13.0828L9.51151 13.0996L9.49469 13.1164L9.47786 13.1332L9.46102 13.15L9.44417 13.1668L9.42732 13.1837L9.41045 13.2005L9.39358 13.2174L9.3767 13.2342L9.35981 13.2511L9.34292 13.268L9.32601 13.2849L9.3091 13.3018L9.29217 13.3187L9.27524 13.3356L9.2583 13.3525L9.24135 13.3694L9.22439 13.3864L9.20742 13.4033L9.19044 13.4203L9.17345 13.4372L9.15645 13.4542L9.13945 13.4712L9.12243 13.4882L9.1054 13.5052L9.08836 13.5222L9.07131 13.5393L9.05426 13.5563L9.03719 13.5734L9.02011 13.5904L9.00302 13.6075L8.98592 13.6246L8.9688 13.6417L8.95168 13.6588L8.93455 13.6759L8.9174 13.693L8.90024 13.7101L8.88308 13.7273L8.8659 13.7444L8.84871 13.7616L8.8315 13.7788L8.81429 13.796L8.79706 13.8132L8.77983 13.8304L8.76257 13.8477L8.74531 13.8649L8.72804 13.8821L8.71075 13.8994L8.69345 13.9167L8.67614 13.934L8.65881 13.9513L8.64147 13.9686L8.62412 13.9859L8.60676 14.0033L8.58938 14.0206L8.57199 14.038L8.55458 14.0554L8.53716 14.0728L8.51973 14.0902L8.50229 14.1076L8.48483 14.1251L8.46736 14.1425L8.44987 14.16L8.43237 14.1775L8.41485 14.195L8.39732 14.2125L8.37978 14.23L8.36222 14.2475L8.34465 14.2651L8.32706 14.2827L8.30945 14.3002L8.29184 14.3178L8.2742 14.3355L8.25656 14.3531L8.23889 14.3707L8.22121 14.3884L8.20352 14.4061L8.18581 14.4238L8.16808 14.4415L8.15034 14.4592L8.13258 14.4769L8.11481 14.4947L8.09702 14.5124L8.07921 14.5302L8.06139 14.548L8.04355 14.5658L8.0257 14.5837L8.00783 14.6015L7.98994 14.6194L7.97203 14.6373L7.95411 14.6552L7.93617 14.6731L7.91821 14.691L7.90024 14.709L7.88225 14.727L7.86424 14.7449L7.84621 14.763L7.82817 14.781L7.81011 14.799L7.79203 14.8171L7.77393 14.8352L7.75581 14.8533L7.73768 14.8714L7.71952 14.8895L7.70135 14.9076L7.68316 14.9258L7.66495 14.944L7.64673 14.9622L7.62848 14.9804L7.61022 14.9987L7.59193 15.0169L7.57363 15.0352L7.55531 15.0535L7.53697 15.0718L7.5186 15.0902L7.50022 15.1085L7.48182 15.1269L7.4634 15.1453L7.44496 15.1637L7.4265 15.1822L7.40802 15.2006L7.38952 15.2191L7.371 15.2376L7.35246 15.2561L7.33389 15.2747L7.31531 15.2932L7.29671 15.3118L7.27808 15.3304L7.25944 15.3491L7.24077 15.3677L7.22208 15.3864L7.20337 15.4051L7.18464 15.4238L7.16589 15.4425L7.14712 15.4612L7.12832 15.48L7.10951 15.4988L7.09067 15.5176L7.07181 15.5365L7.05292 15.5553L7.03402 15.5742L7.01509 15.5931L6.99614 15.612C6.27167 16.3357 5.09652 16.3361 4.37259 15.613C3.64838 14.8896 3.64838 13.7168 4.37259 12.9935L13.1214 4.2547L14.4178 5.57764L14.4177 5.57772L14.4254 5.58523Z",stroke:"currentColor"}),e("path",{d:"M12.5299 10.2848L7.32791 15.5545C7.12956 15.7555 6.88934 15.9156 6.62689 16.0225C6.08679 16.2424 5.46752 16.2239 4.94171 15.972L4.77945 16.31L4.94171 15.972C4.6339 15.8246 4.36574 15.6007 4.16736 15.3245L4.02179 15.1219C3.60142 14.5367 3.60138 13.749 4.02169 13.1637C4.12291 13.0228 4.24539 12.8984 4.38476 12.7949L5.72374 11.8006L5.76816 11.7676L5.80115 11.7232L5.91056 11.576C6.30572 11.0443 6.96187 10.4244 7.58765 10.0864C7.90229 9.91646 8.17215 9.83813 8.37711 9.84461C8.55555 9.85025 8.69852 9.9179 8.81563 10.1071C8.88186 10.2141 8.92418 10.3701 8.97238 10.5823C8.97507 10.5942 8.9778 10.6063 8.98058 10.6186C9.00013 10.7052 9.02201 10.8022 9.04751 10.8896C9.07575 10.9865 9.11828 11.1086 9.19239 11.2146C9.29475 11.361 9.4504 11.4075 9.53763 11.4247C9.63768 11.4444 9.74477 11.4446 9.84616 11.436C10.0516 11.4187 10.299 11.3594 10.5607 11.2642C11.0498 11.0864 11.6345 10.7668 12.1516 10.2848L12.5299 10.2848Z",stroke:"currentColor",strokeWidth:"0.75"})]}),B5=()=>s("svg",{width:"20",height:"20",viewBox:"0 0 20 20",fill:"none",xmlns:"http://www.w3.org/2000/svg",children:[e("rect",{x:"0.5",y:"0.5",width:"19",height:"19",rx:"3.5",fill:"currentColor",stroke:"currentColor"}),e("path",{d:"M14.4254 5.58523L15.744 6.87427L15.7249 6.89333L15.7043 6.91394L15.6837 6.93453L15.6631 6.95509L15.6425 6.97562L15.622 6.99612L15.6015 7.01659L15.581 7.03703L15.5606 7.05745L15.5402 7.07783L15.5198 7.09819L15.4995 7.11852L15.4791 7.13882L15.4588 7.15909L15.4386 7.17934L15.4183 7.19956L15.3981 7.21974L15.3779 7.23991L15.3578 7.26004L15.3377 7.28015L15.3176 7.30022L15.2975 7.32028L15.2774 7.3403L15.2574 7.3603L15.2374 7.38027L15.2175 7.40021L15.1975 7.42013L15.1776 7.44002L15.1577 7.45988L15.1379 7.47972L15.118 7.49953L15.0982 7.51931L15.0784 7.53907L15.0587 7.5588L15.0389 7.57851L15.0192 7.59819L14.9996 7.61785L14.9799 7.63748L14.9603 7.65708L14.9407 7.67666L14.9211 7.69621L14.9016 7.71574L14.882 7.73524L14.8625 7.75472L14.8431 7.77417L14.8236 7.7936L14.8042 7.81301L14.7848 7.83239L14.7654 7.85174L14.746 7.87107L14.7267 7.89038L14.7074 7.90966L14.6881 7.92892L14.6689 7.94815L14.6496 7.96736L14.6304 7.98655L14.6113 8.00571L14.5921 8.02485L14.573 8.04397L14.5538 8.06306L14.5347 8.08213L14.5157 8.10118L14.4966 8.1202L14.4776 8.1392L14.4586 8.15818L14.4396 8.17714L14.4207 8.19607L14.4017 8.21498L14.3828 8.23387L14.3639 8.25274L14.3451 8.27158L14.3262 8.2904L14.3074 8.3092L14.2886 8.32798L14.2698 8.34674L14.2511 8.36547L14.2323 8.38418L14.2136 8.40288L14.1949 8.42155L14.1763 8.4402L14.1576 8.45883L14.139 8.47743L14.1204 8.49602L14.1018 8.51459L14.0832 8.53313L14.0647 8.55166L14.0462 8.57016L14.0277 8.58864L14.0092 8.60711L13.9907 8.62555L13.9723 8.64397L13.9538 8.66238L13.9354 8.68076L13.917 8.69913L13.8987 8.71747L13.8803 8.73579L13.862 8.7541L13.8437 8.77239L13.8254 8.79065L13.8071 8.8089L13.7889 8.82713L13.7707 8.84534L13.7524 8.86353L13.7343 8.8817L13.7161 8.89986L13.6979 8.91799L13.6798 8.93611L13.6617 8.95421L13.6436 8.97229L13.6255 8.99036L13.6074 9.0084L13.5894 9.02643L13.5713 9.04444L13.5533 9.06243L13.5353 9.0804L13.5173 9.09836L13.4994 9.1163L13.4814 9.13422L13.4635 9.15213L13.4456 9.17002L13.4277 9.18789L13.4098 9.20574L13.392 9.22358L13.3741 9.2414L13.3563 9.25921L13.3385 9.277L13.3207 9.29477L13.3029 9.31253L13.2852 9.33027L13.2674 9.34799L13.2497 9.3657L13.232 9.38339L13.2143 9.40107L13.1966 9.41873L13.1789 9.43638L13.1613 9.45401L13.1436 9.47163L13.126 9.48923L13.1084 9.50681L13.0908 9.52438L13.0733 9.54194L13.0557 9.55948L13.0381 9.57701L13.0206 9.59452L13.0031 9.61202L12.9856 9.6295L12.9681 9.64697L12.9506 9.66443L12.9332 9.68187L12.9157 9.6993L12.8983 9.71671L12.8809 9.73412L12.8634 9.7515L12.8461 9.76888L12.8287 9.78624L12.8113 9.80358L12.794 9.82092L12.7766 9.83824L12.7593 9.85555L12.742 9.87284L12.7247 9.89013L12.7074 9.9074L12.6901 9.92466L12.6728 9.9419L12.6556 9.95913L12.6383 9.97636L12.6211 9.99356L12.6039 10.0108L12.5867 10.0279L12.5695 10.0451L12.5523 10.0623L12.5351 10.0794L12.518 10.0966L12.5008 10.1137L12.4837 10.1308L12.4666 10.1479L12.4495 10.165L12.4324 10.1821L12.4153 10.1992L12.3982 10.2162L12.3811 10.2333L12.364 10.2503L12.347 10.2674L12.33 10.2844L12.3129 10.3014L12.2959 10.3184L12.2789 10.3354L12.2619 10.3524L12.2449 10.3693L12.2279 10.3863L12.211 10.4032L12.194 10.4202L12.177 10.4371L12.1601 10.454L12.1432 10.471L12.1262 10.4879L12.1093 10.5048L12.0924 10.5216L12.0755 10.5385L12.0586 10.5554L12.0417 10.5723L12.0249 10.5891L12.008 10.606L11.9911 10.6228L11.9743 10.6396L11.9575 10.6565L11.9406 10.6733L11.9238 10.6901L11.907 10.7069L11.8902 10.7237L11.8734 10.7404L11.8566 10.7572L11.8398 10.774L11.823 10.7907L11.8062 10.8075L11.7895 10.8243L11.7727 10.841L11.7559 10.8577L11.7392 10.8745L11.7225 10.8912L11.7057 10.9079L11.689 10.9246L11.6723 10.9413L11.6556 10.958L11.6389 10.9747L11.6221 10.9914L11.6054 11.0081L11.5888 11.0247L11.5721 11.0414L11.5554 11.0581L11.5387 11.0747L11.522 11.0914L11.5054 11.108L11.4887 11.1247L11.4721 11.1413L11.4554 11.1579L11.4388 11.1746L11.4221 11.1912L11.4055 11.2078L11.3888 11.2244L11.3722 11.241L11.3556 11.2576L11.339 11.2742L11.3224 11.2908L11.3057 11.3074L11.2891 11.324L11.2725 11.3406L11.2559 11.3572L11.2393 11.3738L11.2227 11.3903L11.2061 11.4069L11.1895 11.4235L11.173 11.44L11.1564 11.4566L11.1398 11.4732L11.1232 11.4897L11.1066 11.5063L11.0901 11.5228L11.0735 11.5394L11.0569 11.5559L11.0404 11.5725L11.0238 11.589L11.0072 11.6056L10.9907 11.6221L10.9741 11.6386L10.9576 11.6552L10.941 11.6717L10.9245 11.6883L10.9079 11.7048L10.8914 11.7213L10.8748 11.7378L10.8583 11.7544L10.8417 11.7709L10.8252 11.7874L10.8086 11.804L10.7921 11.8205L10.7755 11.837L10.759 11.8535L10.7424 11.8701L10.7259 11.8866L10.7094 11.9031L10.6928 11.9196L10.6763 11.9362L10.6597 11.9527L10.6432 11.9692L10.6266 11.9857L10.6101 12.0023L10.5935 12.0188L10.577 12.0353L10.5604 12.0519L10.5439 12.0684L10.5273 12.0849L10.5108 12.1015L10.4942 12.118L10.4777 12.1345L10.4611 12.1511L10.4446 12.1676L10.428 12.1841L10.4114 12.2007L10.3949 12.2172L10.3783 12.2338L10.3618 12.2503L10.3452 12.2669L10.3286 12.2834L10.312 12.3L10.2955 12.3165L10.2789 12.3331L10.2623 12.3497L10.2457 12.3662L10.2291 12.3828L10.2125 12.3994L10.1959 12.4159L10.1793 12.4325L10.1627 12.4491L10.1461 12.4657L10.1295 12.4823L10.1129 12.4989L10.0963 12.5155L10.0797 12.5321L10.0631 12.5487L10.0464 12.5653L10.0298 12.5819L10.0132 12.5985L9.99652 12.6151L9.97987 12.6318L9.96322 12.6484L9.94657 12.665L9.92991 12.6817L9.91324 12.6983L9.89657 12.715L9.87989 12.7316L9.86321 12.7483L9.84653 12.7649L9.82984 12.7816L9.81314 12.7983L9.79644 12.815L9.77973 12.8317L9.76301 12.8484L9.74629 12.8651L9.72957 12.8818L9.71283 12.8985L9.69609 12.9152L9.67935 12.9319L9.6626 12.9487L9.64584 12.9654L9.62907 12.9822L9.6123 12.9989L9.59552 13.0157L9.57873 13.0324L9.56194 13.0492L9.54514 13.066L9.52833 13.0828L9.51151 13.0996L9.49469 13.1164L9.47786 13.1332L9.46102 13.15L9.44417 13.1668L9.42732 13.1837L9.41045 13.2005L9.39358 13.2174L9.3767 13.2342L9.35981 13.2511L9.34292 13.268L9.32601 13.2849L9.3091 13.3018L9.29217 13.3187L9.27524 13.3356L9.2583 13.3525L9.24135 13.3694L9.22439 13.3864L9.20742 13.4033L9.19044 13.4203L9.17345 13.4372L9.15645 13.4542L9.13945 13.4712L9.12243 13.4882L9.1054 13.5052L9.08836 13.5222L9.07131 13.5393L9.05426 13.5563L9.03719 13.5734L9.02011 13.5904L9.00302 13.6075L8.98592 13.6246L8.9688 13.6417L8.95168 13.6588L8.93455 13.6759L8.9174 13.693L8.90024 13.7101L8.88308 13.7273L8.8659 13.7444L8.84871 13.7616L8.8315 13.7788L8.81429 13.796L8.79706 13.8132L8.77983 13.8304L8.76257 13.8477L8.74531 13.8649L8.72804 13.8821L8.71075 13.8994L8.69345 13.9167L8.67614 13.934L8.65881 13.9513L8.64147 13.9686L8.62412 13.9859L8.60676 14.0033L8.58938 14.0206L8.57199 14.038L8.55458 14.0554L8.53716 14.0728L8.51973 14.0902L8.50229 14.1076L8.48483 14.1251L8.46736 14.1425L8.44987 14.16L8.43237 14.1775L8.41485 14.195L8.39732 14.2125L8.37978 14.23L8.36222 14.2475L8.34465 14.2651L8.32706 14.2827L8.30945 14.3002L8.29184 14.3178L8.2742 14.3355L8.25656 14.3531L8.23889 14.3707L8.22121 14.3884L8.20352 14.4061L8.18581 14.4238L8.16808 14.4415L8.15034 14.4592L8.13258 14.4769L8.11481 14.4947L8.09702 14.5124L8.07921 14.5302L8.06139 14.548L8.04355 14.5658L8.0257 14.5837L8.00783 14.6015L7.98994 14.6194L7.97203 14.6373L7.95411 14.6552L7.93617 14.6731L7.91821 14.691L7.90024 14.709L7.88225 14.727L7.86424 14.7449L7.84621 14.763L7.82817 14.781L7.81011 14.799L7.79203 14.8171L7.77393 14.8352L7.75581 14.8533L7.73768 14.8714L7.71952 14.8895L7.70135 14.9076L7.68316 14.9258L7.66495 14.944L7.64673 14.9622L7.62848 14.9804L7.61022 14.9987L7.59193 15.0169L7.57363 15.0352L7.55531 15.0535L7.53697 15.0718L7.5186 15.0902L7.50022 15.1085L7.48182 15.1269L7.4634 15.1453L7.44496 15.1637L7.4265 15.1822L7.40802 15.2006L7.38952 15.2191L7.371 15.2376L7.35246 15.2561L7.33389 15.2747L7.31531 15.2932L7.29671 15.3118L7.27808 15.3304L7.25944 15.3491L7.24077 15.3677L7.22208 15.3864L7.20337 15.4051L7.18464 15.4238L7.16589 15.4425L7.14712 15.4612L7.12832 15.48L7.10951 15.4988L7.09067 15.5176L7.07181 15.5365L7.05292 15.5553L7.03402 15.5742L7.01509 15.5931L6.99614 15.612C6.27167 16.3357 5.09652 16.3361 4.37259 15.613C3.64838 14.8896 3.64838 13.7168 4.37259 12.9935L13.1214 4.2547L14.4178 5.57764L14.4177 5.57772L14.4254 5.58523Z",stroke:"black"}),e("path",{d:"M12.5299 10.2849L7.32791 15.5546C7.12956 15.7556 6.88934 15.9156 6.62689 16.0225C6.08679 16.2425 5.46752 16.224 4.94171 15.9721L4.77945 16.31L4.94171 15.9721C4.6339 15.8246 4.36574 15.6008 4.16736 15.3246L4.02179 15.122C3.60142 14.5368 3.60138 13.749 4.02169 13.1638C4.12291 13.0229 4.24539 12.8984 4.38476 12.795L5.72374 11.8006L5.76816 11.7677L5.80115 11.7233L5.91056 11.5761C6.30572 11.0444 6.96187 10.4244 7.58765 10.0865C7.90229 9.91653 8.17215 9.83821 8.37711 9.84469C8.55555 9.85033 8.69852 9.91798 8.81563 10.1072C8.88186 10.2142 8.92418 10.3701 8.97238 10.5824C8.97507 10.5942 8.9778 10.6063 8.98058 10.6187C9.00013 10.7053 9.02201 10.8022 9.04751 10.8897C9.07575 10.9866 9.11828 11.1087 9.19239 11.2147C9.29475 11.3611 9.4504 11.4075 9.53763 11.4247C9.63768 11.4445 9.74477 11.4447 9.84616 11.4361C10.0516 11.4187 10.299 11.3594 10.5607 11.2643C11.0498 11.0864 11.6345 10.7669 12.1516 10.2849L12.5299 10.2849Z",stroke:"black",strokeWidth:"0.75"})]}),H5=()=>s("svg",{width:"20",height:"20",viewBox:"0 0 20 20",fill:"none",xmlns:"http://www.w3.org/2000/svg",children:[e("rect",{x:"0.5",y:"0.5",width:"19",height:"19",rx:"3.5",stroke:"currentColor"}),e("path",{d:"M15.4237 6.90042C15.5191 6.92315 15.6152 6.94413 15.7074 6.96092C15.7135 7.05035 15.7162 7.16454 15.7138 7.30375C15.7056 7.77188 15.6408 8.43317 15.515 9.1653C15.2592 10.6537 14.774 12.3014 14.1 13.2C13.4011 14.1319 12.332 14.9694 11.4101 15.584C10.9538 15.8882 10.5429 16.1317 10.2465 16.2989C10.1617 16.3467 10.0865 16.3882 10.0224 16.423C9.97538 16.3925 9.92211 16.3576 9.86327 16.3183C9.61299 16.1515 9.26304 15.908 8.86735 15.6037C8.07099 14.9911 7.11105 14.148 6.4 13.2C5.71286 12.2838 5.10686 10.6159 4.73507 9.12872C4.55136 8.39389 4.4322 7.73262 4.38844 7.26582C4.37726 7.14653 4.37171 7.04688 4.37029 6.96627C4.68202 6.91822 5.07002 6.82212 5.46167 6.6997C6.04643 6.51692 6.71066 6.25305 7.25513 5.93001C7.78069 5.61819 8.40348 5.00685 8.92133 4.49851C8.96063 4.45994 8.99932 4.42196 9.03732 4.38474C9.32127 4.10667 9.57222 3.86458 9.78023 3.69195C9.86978 3.61763 9.94141 3.56465 9.99619 3.52986C10.0511 3.56629 10.1228 3.62162 10.2126 3.69902C10.4221 3.8796 10.6732 4.13028 10.9589 4.41605L10.9643 4.42138C11.2419 4.69905 11.5471 5.00425 11.8469 5.27159C12.1431 5.53579 12.4648 5.79139 12.7764 5.94721C13.307 6.2125 13.989 6.47149 14.5895 6.66369C14.8912 6.76025 15.179 6.8421 15.4237 6.90042ZM9.92522 3.48908C9.92521 3.48905 9.92594 3.48931 9.92744 3.48994C9.92598 3.48943 9.92523 3.48911 9.92522 3.48908Z",stroke:"currentColor"})]}),j5=()=>s("svg",{width:"20",height:"20",viewBox:"0 0 20 20",fill:"none",xmlns:"http://www.w3.org/2000/svg",children:[e("rect",{x:"0.5",y:"0.5",width:"19",height:"19",rx:"3.5",fill:"currentColor",stroke:"currentColor"}),e("path",{d:"M9.92516 3.4891C9.92515 3.48907 9.92588 3.48933 9.92738 3.48997C9.92592 3.48946 9.92517 3.48914 9.92516 3.4891ZM9.99613 3.52989C10.051 3.56631 10.1227 3.62164 10.2125 3.69904C10.422 3.87963 10.6731 4.1303 10.9589 4.41608L10.9642 4.4214C11.2419 4.69907 11.5471 5.00428 11.8468 5.27161C12.1431 5.53582 12.4647 5.79142 12.7763 5.94724C13.3069 6.21253 13.9889 6.47151 14.5894 6.66371C14.8911 6.76027 15.179 6.84213 15.4236 6.90044C15.519 6.92317 15.6151 6.94416 15.7074 6.96095C15.7134 7.05037 15.7162 7.16456 15.7137 7.30377C15.7056 7.7719 15.6407 8.4332 15.5149 9.16533C15.2592 10.6537 14.7739 12.3014 14.0999 13.2C13.401 14.1319 12.3319 14.9694 11.4101 15.584C10.9538 15.8882 10.5428 16.1317 10.2465 16.2989C10.1617 16.3467 10.0864 16.3882 10.0223 16.423C9.97532 16.3925 9.92205 16.3576 9.86321 16.3184C9.61293 16.1515 9.26298 15.9081 8.86729 15.6037C8.07092 14.9911 7.11099 14.1481 6.39994 13.2C5.7128 12.2838 5.10679 10.6159 4.73501 9.12874C4.5513 8.39391 4.43214 7.73264 4.38838 7.26584C4.3772 7.14656 4.37164 7.0469 4.37023 6.9663C4.68196 6.91824 5.06996 6.82215 5.46161 6.69972C6.04637 6.51694 6.7106 6.25307 7.25507 5.93003C7.78063 5.61822 8.40342 5.00687 8.92127 4.49853C8.96057 4.45996 8.99926 4.42198 9.03726 4.38477C9.32121 4.1067 9.57216 3.8646 9.78016 3.69197C9.86972 3.61765 9.94135 3.56467 9.99613 3.52989Z",stroke:"black"})]});function Z5({spanKind:n,variant:a="fill"}){const t=a==="fill";let l=t?e(N5,{}):e(O5,{});const i=wr({spanKind:n});switch(n){case"llm":l=t?e(I5,{}):e(A5,{});break;case"chain":l=t?e(R5,{}):e(V5,{});break;case"retriever":l=t?e(_5,{}):e(D5,{});break;case"embedding":l=t?e(E5,{}):e(F5,{});break;case"agent":l=t?e(M5,{}):e(z5,{});break;case"tool":l=t?e(T5,{}):e(x5,{});break;case"reranker":l=t?e(P5,{}):e(K5,{});break;case"evaluator":l=t?e(B5,{}):e($5,{});break;case"guardrail":l=t?e(j5,{}):e(H5,{});break}return e("div",{css:m`
        color: ${i};
        width: 20px;
        height: 20px;
      `,title:n,children:l})}const Sr=(function(){var n=[{defaultValue:null,kind:"LocalArgument",name:"nodeId"}],a=[{kind:"Variable",name:"id",variableName:"nodeId"}],t={alias:null,args:null,kind:"ScalarField",name:"__typename",storageKey:null},l={kind:"InlineFragment",selections:[{alias:null,args:null,concreteType:"TokenUsage",kind:"LinkedField",name:"tokenUsage",plural:!1,selections:[{alias:null,args:null,kind:"ScalarField",name:"prompt",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"completion",storageKey:null}],storageKey:null}],type:"ProjectSession",abstractKey:null};return{fragment:{argumentDefinitions:n,kind:"Fragment",metadata:null,name:"SessionTokenCountDetailsQuery",selections:[{alias:null,args:a,concreteType:null,kind:"LinkedField",name:"node",plural:!1,selections:[t,l],storageKey:null}],type:"Query",abstractKey:null},kind:"Request",operation:{argumentDefinitions:n,kind:"Operation",name:"SessionTokenCountDetailsQuery",selections:[{alias:null,args:a,concreteType:null,kind:"LinkedField",name:"node",plural:!1,selections:[t,l,{alias:null,args:null,kind:"ScalarField",name:"id",storageKey:null}],storageKey:null}]},params:{cacheID:"5df073c3f0f20378aed5118f6f0d2f4b",id:null,metadata:{},name:"SessionTokenCountDetailsQuery",operationKind:"query",text:`query SessionTokenCountDetailsQuery(
  $nodeId: ID!
) {
  node(id: $nodeId) {
    __typename
    ... on ProjectSession {
      tokenUsage {
        prompt
        completion
      }
    }
    id
  }
}
`}}})();Sr.hash="da1b954f5615c67f552ece1b8b3478b5";const U5=m`
  display: flex;
  flex-direction: column;
  gap: var(--ac-global-dimension-static-size-50);
`,G5=m`
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  gap: var(--ac-global-dimension-static-size-100);
`,Q5=m`
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: var(--ac-global-dimension-static-size-25);
`,W5=m`
  margin-top: var(--ac-global-dimension-static-size-100);
  margin-bottom: var(--ac-global-dimension-static-size-25);
`;function zn({label:n,count:a,isTotal:t=!1,isSubItem:l=!1}){const i=typeof a=="number"?On(a):"--";return s("div",{css:G5,children:[e(C,{size:l?"XS":"S",color:l?"text-500":t?"text-900":"text-700",weight:t?"heavy":"normal",children:n}),e("div",{css:Q5,children:s(C,{size:l?"XS":"S",color:"text-700",children:[i,"t"]})})]})}function Tl({children:n}){return e(C,{size:"XS",color:"text-700",weight:"heavy",css:W5,children:n})}function Xe({total:n,prompt:a,completion:t,promptDetails:l,completionDetails:i,label:r="Total"}){const o=l&&Object.entries(l).some(([,d])=>d!=null&&d>0),c=i&&Object.entries(i).some(([,d])=>d!=null&&d>0);return s("div",{css:U5,children:[n!=null&&e(zn,{label:r,count:n,isTotal:!0}),a!=null&&e(zn,{label:"Prompt",count:a}),t!=null&&e(zn,{label:"Completion",count:t}),o&&s(U,{children:[e(Tl,{children:"Prompt Details"}),l&&Object.entries(l).map(([d,u])=>u!=null&&u>0?e(zn,{label:d.charAt(0).toUpperCase()+d.slice(1),count:u,isSubItem:!0},`prompt-${d}`):null)]}),c&&s(U,{children:[e(Tl,{children:"Completion Details"}),i&&Object.entries(i).map(([d,u])=>u!=null&&u>0?e(zn,{label:d.charAt(0).toUpperCase()+d.slice(1),count:u,isSubItem:!0},`completion-${d}`):null)]})]})}function q5(n){const a=M.useLazyLoadQuery(Sr,{nodeId:n.sessionNodeId}),t=p.useMemo(()=>{if(a.node.__typename==="ProjectSession"){const l=a.node.tokenUsage.prompt,i=a.node.tokenUsage.completion;return{total:l+i,prompt:l,completion:i}}return{total:null,prompt:null,completion:null}},[a.node]);return e(Xe,{...t})}const X5=m`
  display: flex;
  flex-direction: row;
  gap: var(--ac-global-dimension-static-size-50);
  align-items: center;

  &[data-size="S"] {
    font-size: var(--ac-global-font-size-s);
  }
  &[data-size="M"] {
    font-size: var(--ac-global-font-size-m);
  }
`;function Y5(n,a){const{children:t,size:l="M",...i}=n,r=typeof t=="number"?On(t):"--";return s("div",{className:"token-count-item","data-size":l,css:X5,ref:a,...i,children:[e(T,{svg:e(e0,{}),css:m`
          color: var(--ac-global-text-color-900);
        `}),e(C,{size:n.size,fontFamily:"mono",children:r})]})}const ze=p.forwardRef(Y5);function Qm(n){return s(R,{children:[e(te,{children:e(ze,{size:n.size,role:"button",children:n.tokenCountTotal})}),s(ie,{children:[e(ae,{}),e(p.Suspense,{fallback:e(re,{}),children:e(q5,{sessionNodeId:n.nodeId})})]})]})}const xr=(function(){var n=[{defaultValue:null,kind:"LocalArgument",name:"nodeId"}],a=[{kind:"Variable",name:"id",variableName:"nodeId"}],t={alias:null,args:null,kind:"ScalarField",name:"__typename",storageKey:null},l={alias:null,args:null,kind:"ScalarField",name:"cumulativeTokenCountPrompt",storageKey:null},i={alias:null,args:null,kind:"ScalarField",name:"cumulativeTokenCountCompletion",storageKey:null},r={alias:null,args:null,kind:"ScalarField",name:"id",storageKey:null};return{fragment:{argumentDefinitions:n,kind:"Fragment",metadata:null,name:"TraceTokenCountDetailsQuery",selections:[{alias:null,args:a,concreteType:null,kind:"LinkedField",name:"node",plural:!1,selections:[t,{kind:"InlineFragment",selections:[{alias:null,args:null,concreteType:"Span",kind:"LinkedField",name:"rootSpan",plural:!1,selections:[l,i],storageKey:null}],type:"Trace",abstractKey:null}],storageKey:null}],type:"Query",abstractKey:null},kind:"Request",operation:{argumentDefinitions:n,kind:"Operation",name:"TraceTokenCountDetailsQuery",selections:[{alias:null,args:a,concreteType:null,kind:"LinkedField",name:"node",plural:!1,selections:[t,{kind:"InlineFragment",selections:[{alias:null,args:null,concreteType:"Span",kind:"LinkedField",name:"rootSpan",plural:!1,selections:[l,i,r],storageKey:null}],type:"Trace",abstractKey:null},r],storageKey:null}]},params:{cacheID:"e9131ab8a67b6b79dc9995bb3ce0cb55",id:null,metadata:{},name:"TraceTokenCountDetailsQuery",operationKind:"query",text:`query TraceTokenCountDetailsQuery(
  $nodeId: ID!
) {
  node(id: $nodeId) {
    __typename
    ... on Trace {
      rootSpan {
        cumulativeTokenCountPrompt
        cumulativeTokenCountCompletion
        id
      }
    }
    id
  }
}
`}}})();xr.hash="c0178c78b8c3bb146caa2579d6bc75c4";function J5(n){const a=M.useLazyLoadQuery(xr,{nodeId:n.traceNodeId}),t=p.useMemo(()=>{var l,i;if(a.node.__typename==="Trace"){const r=((l=a.node.rootSpan)==null?void 0:l.cumulativeTokenCountPrompt)??0,o=((i=a.node.rootSpan)==null?void 0:i.cumulativeTokenCountCompletion)??0;return{total:r+o,prompt:r,completion:o}}return{total:null,prompt:null,completion:null}},[a.node]);return e(Xe,{...t})}function Wm(n){return s(R,{children:[e(te,{children:e(ze,{size:n.size,role:"button",children:n.tokenCountTotal})}),s(ie,{children:[e(ae,{}),e(p.Suspense,{fallback:e(re,{}),children:e(J5,{traceNodeId:n.nodeId})})]})]})}const Tr=(function(){var n=[{defaultValue:null,kind:"LocalArgument",name:"nodeId"}],a=[{kind:"Variable",name:"id",variableName:"nodeId"}],t={alias:null,args:null,kind:"ScalarField",name:"__typename",storageKey:null},l={kind:"InlineFragment",selections:[{alias:null,args:null,kind:"ScalarField",name:"tokenCountTotal",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"tokenCountPrompt",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"tokenCountCompletion",storageKey:null},{alias:null,args:null,concreteType:"TokenCountPromptDetails",kind:"LinkedField",name:"tokenPromptDetails",plural:!1,selections:[{alias:null,args:null,kind:"ScalarField",name:"audio",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"cacheRead",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"cacheWrite",storageKey:null}],storageKey:null}],type:"Span",abstractKey:null};return{fragment:{argumentDefinitions:n,kind:"Fragment",metadata:null,name:"SpanTokenCountDetailsQuery",selections:[{alias:null,args:a,concreteType:null,kind:"LinkedField",name:"node",plural:!1,selections:[t,l],storageKey:null}],type:"Query",abstractKey:null},kind:"Request",operation:{argumentDefinitions:n,kind:"Operation",name:"SpanTokenCountDetailsQuery",selections:[{alias:null,args:a,concreteType:null,kind:"LinkedField",name:"node",plural:!1,selections:[t,l,{alias:null,args:null,kind:"ScalarField",name:"id",storageKey:null}],storageKey:null}]},params:{cacheID:"fc6d8104f9bf9481330b8b879b7c8e8e",id:null,metadata:{},name:"SpanTokenCountDetailsQuery",operationKind:"query",text:`query SpanTokenCountDetailsQuery(
  $nodeId: ID!
) {
  node(id: $nodeId) {
    __typename
    ... on Span {
      tokenCountTotal
      tokenCountPrompt
      tokenCountCompletion
      tokenPromptDetails {
        audio
        cacheRead
        cacheWrite
      }
    }
    id
  }
}
`}}})();Tr.hash="2f53943dbe7d189d4126be701a017818";function e4(n){const a=M.useLazyLoadQuery(Tr,{nodeId:n.spanNodeId}),t=p.useMemo(()=>{var l,i,r;if(a.node.__typename==="Span"){const o=a.node.tokenCountPrompt??0,c=a.node.tokenCountCompletion??0,d=a.node.tokenCountTotal??0,u={};return(l=a.node.tokenPromptDetails)!=null&&l.audio&&(u.audio=a.node.tokenPromptDetails.audio),(i=a.node.tokenPromptDetails)!=null&&i.cacheRead&&(u["cache read"]=a.node.tokenPromptDetails.cacheRead),(r=a.node.tokenPromptDetails)!=null&&r.cacheWrite&&(u["cache write"]=a.node.tokenPromptDetails.cacheWrite),{total:d,prompt:o,completion:c,promptDetails:Object.keys(u).length>0?u:void 0}}return{total:0,prompt:0,completion:0}},[a.node]);return e(Xe,{...t})}function n4(n){const a=p.useCallback(t=>{t.continuePropagation()},[]);return s(R,{children:[e(te,{onPress:a,children:e(ze,{size:n.size,role:"button",children:n.tokenCountTotal})}),s(ie,{children:[e(ae,{}),e(p.Suspense,{fallback:e(re,{}),children:e(e4,{spanNodeId:n.nodeId})})]})]})}const Ar=(function(){var n=[{defaultValue:null,kind:"LocalArgument",name:"nodeId"}],a=[{kind:"Variable",name:"id",variableName:"nodeId"}],t={alias:null,args:null,kind:"ScalarField",name:"__typename",storageKey:null},l={kind:"InlineFragment",selections:[{alias:null,args:null,kind:"ScalarField",name:"cumulativeTokenCountTotal",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"cumulativeTokenCountPrompt",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"cumulativeTokenCountCompletion",storageKey:null}],type:"Span",abstractKey:null};return{fragment:{argumentDefinitions:n,kind:"Fragment",metadata:null,name:"SpanCumulativeTokenCountDetailsQuery",selections:[{alias:null,args:a,concreteType:null,kind:"LinkedField",name:"node",plural:!1,selections:[t,l],storageKey:null}],type:"Query",abstractKey:null},kind:"Request",operation:{argumentDefinitions:n,kind:"Operation",name:"SpanCumulativeTokenCountDetailsQuery",selections:[{alias:null,args:a,concreteType:null,kind:"LinkedField",name:"node",plural:!1,selections:[t,l,{alias:null,args:null,kind:"ScalarField",name:"id",storageKey:null}],storageKey:null}]},params:{cacheID:"c1da825bac7aac7aafa07638290f6f1d",id:null,metadata:{},name:"SpanCumulativeTokenCountDetailsQuery",operationKind:"query",text:`query SpanCumulativeTokenCountDetailsQuery(
  $nodeId: ID!
) {
  node(id: $nodeId) {
    __typename
    ... on Span {
      cumulativeTokenCountTotal
      cumulativeTokenCountPrompt
      cumulativeTokenCountCompletion
    }
    id
  }
}
`}}})();Ar.hash="f7a968d87890a07d6e1dd6f06bad6b51";function a4(n){const a=M.useLazyLoadQuery(Ar,{nodeId:n.spanNodeId}),t=p.useMemo(()=>{if(a.node.__typename==="Span"){const l=a.node.cumulativeTokenCountPrompt??0,i=a.node.cumulativeTokenCountCompletion??0;return{total:a.node.cumulativeTokenCountTotal??0,prompt:l,completion:i}}return{total:null,prompt:null,completion:null}},[a.node]);return e(Xe,{...t})}function qm(n){return s(R,{children:[e(te,{children:e(ze,{size:n.size,role:"button",children:n.tokenCountTotal})}),s(ie,{children:[e(ae,{}),e(p.Suspense,{fallback:e(re,{}),children:e(a4,{spanNodeId:n.nodeId})})]})]})}const t4=m`
  display: flex;
  flex-direction: row;
  gap: var(--ac-global-dimension-static-size-50);
  align-items: center;

  &[data-size="S"] {
    font-size: var(--ac-global-font-size-s);
  }
  &[data-size="M"] {
    font-size: var(--ac-global-font-size-m);
  }
`;function l4(n,a){const{children:t,size:l="M",...i}=n,r=typeof t=="number"?dr(t):"--";return s("div",{className:"token-costs-item","data-size":l,css:t4,ref:a,...i,children:[e(T,{svg:e(Hc,{}),css:m`
          color: var(--ac-global-text-color-900);
        `}),e(C,{size:n.size,fontFamily:"mono",children:r})]})}const cn=p.forwardRef(l4),i4=m`
  display: flex;
  flex-direction: column;
  gap: var(--ac-global-dimension-static-size-100);
  min-width: 200px;
`,r4=m`
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  gap: var(--ac-global-dimension-static-size-200);

  &[data-is-total="true"] {
    font-weight: var(--ac-global-font-weight-heavy);
  }

  &[data-is-sub-item="true"] {
    margin-left: var(--ac-global-dimension-static-size-200);
    color: var(--ac-global-text-color-500);
    font-size: var(--ac-global-font-size-xs);
  }
`,o4=m`
  font-weight: var(--ac-global-font-weight-heavy);
  font-size: var(--ac-global-font-size-xs);
  color: var(--ac-global-text-color-700);
  margin-top: var(--ac-global-dimension-static-size-100);
`;function Mn({label:n,cost:a,isTotal:t,isSubItem:l}){return s("div",{css:r4,"data-is-total":t,"data-is-sub-item":l,children:[e(C,{size:l?"XS":"S",weight:t?"heavy":"normal",color:l?"text-500":t?"text-900":"text-700",children:n}),e(C,{size:l?"XS":"S",color:l?"text-500":"text-700",children:dr(a)})]})}function Al({children:n}){return e("div",{css:o4,children:e(C,{size:"XS",weight:"heavy",color:"text-700",children:n})})}function dn({total:n,prompt:a,completion:t,promptDetails:l,completionDetails:i,label:r="Total"}){const o=l&&Object.entries(l).some(([,d])=>d!=null&&d>0),c=i&&Object.entries(i).some(([,d])=>d!=null&&d>0);return s("div",{css:i4,children:[n!=null&&e(Mn,{label:r,cost:n,isTotal:!0}),a!=null&&e(Mn,{label:"Prompt",cost:a}),t!=null&&e(Mn,{label:"Completion",cost:t}),o&&s(U,{children:[e(Al,{children:"Prompt Details"}),l&&Object.entries(l).map(([d,u])=>u!=null&&u>0?e(Mn,{label:d.charAt(0).toUpperCase()+d.slice(1),cost:u,isSubItem:!0},`prompt-${d}`):null)]}),c&&s(U,{children:[e(Al,{children:"Completion Details"}),i&&Object.entries(i).map(([d,u])=>u!=null&&u>0?e(Mn,{label:d.charAt(0).toUpperCase()+d.slice(1),cost:u,isSubItem:!0},`completion-${d}`):null)]})]})}const Ir=(function(){var n=[{defaultValue:null,kind:"LocalArgument",name:"nodeId"}],a=[{kind:"Variable",name:"id",variableName:"nodeId"}],t={alias:null,args:null,kind:"ScalarField",name:"__typename",storageKey:null},l={alias:null,args:null,kind:"ScalarField",name:"cost",storageKey:null},i=[l],r={kind:"InlineFragment",selections:[{alias:null,args:null,concreteType:"SpanCostSummary",kind:"LinkedField",name:"costSummary",plural:!1,selections:[{alias:null,args:null,concreteType:"CostBreakdown",kind:"LinkedField",name:"total",plural:!1,selections:i,storageKey:null},{alias:null,args:null,concreteType:"CostBreakdown",kind:"LinkedField",name:"prompt",plural:!1,selections:i,storageKey:null},{alias:null,args:null,concreteType:"CostBreakdown",kind:"LinkedField",name:"completion",plural:!1,selections:i,storageKey:null}],storageKey:null},{alias:null,args:null,concreteType:"SpanCostDetailSummaryEntry",kind:"LinkedField",name:"costDetailSummaryEntries",plural:!0,selections:[{alias:null,args:null,kind:"ScalarField",name:"tokenType",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"isPrompt",storageKey:null},{alias:null,args:null,concreteType:"CostBreakdown",kind:"LinkedField",name:"value",plural:!1,selections:[l,{alias:null,args:null,kind:"ScalarField",name:"tokens",storageKey:null}],storageKey:null}],storageKey:null}],type:"Span",abstractKey:null};return{fragment:{argumentDefinitions:n,kind:"Fragment",metadata:null,name:"SpanTokenCostsDetailsQuery",selections:[{alias:null,args:a,concreteType:null,kind:"LinkedField",name:"node",plural:!1,selections:[t,r],storageKey:null}],type:"Query",abstractKey:null},kind:"Request",operation:{argumentDefinitions:n,kind:"Operation",name:"SpanTokenCostsDetailsQuery",selections:[{alias:null,args:a,concreteType:null,kind:"LinkedField",name:"node",plural:!1,selections:[t,r,{alias:null,args:null,kind:"ScalarField",name:"id",storageKey:null}],storageKey:null}]},params:{cacheID:"76a8269902195041de07d13cdf853e14",id:null,metadata:{},name:"SpanTokenCostsDetailsQuery",operationKind:"query",text:`query SpanTokenCostsDetailsQuery(
  $nodeId: ID!
) {
  node(id: $nodeId) {
    __typename
    ... on Span {
      costSummary {
        total {
          cost
        }
        prompt {
          cost
        }
        completion {
          cost
        }
      }
      costDetailSummaryEntries {
        tokenType
        isPrompt
        value {
          cost
          tokens
        }
      }
    }
    id
  }
}
`}}})();Ir.hash="2b8791832440bdad2d98eb3b3a168fd7";function s4(n){const a=M.useLazyLoadQuery(Ir,{nodeId:n.spanNodeId}),t=p.useMemo(()=>{var l,i,r,o,c,d;if(a.node.__typename==="Span"){const u=a.node.costDetailSummaryEntries;if(!u)return{total:null,prompt:null,completion:null,promptDetails:null,completionDetails:null};const g=u.filter(L=>L.isPrompt),h=u.filter(L=>!L.isPrompt),f=((i=(l=a.node.costSummary)==null?void 0:l.total)==null?void 0:i.cost)??0,b=((o=(r=a.node.costSummary)==null?void 0:r.prompt)==null?void 0:o.cost)??0,y=((d=(c=a.node.costSummary)==null?void 0:c.completion)==null?void 0:d.cost)??0,v={};g.forEach(L=>{L.value.cost!=null&&(v[L.tokenType]=L.value.cost)});const k={};return h.forEach(L=>{L.value.cost!=null&&(k[L.tokenType]=L.value.cost)}),{total:f,prompt:b,completion:y,promptDetails:Object.keys(v).length>0?v:null,completionDetails:Object.keys(k).length>0?k:null}}return{total:null,prompt:null,completion:null,promptDetails:null,completionDetails:null}},[a.node]);return e(dn,{...t})}function Xm(n){return s(R,{children:[e(te,{children:e(cn,{size:n.size,role:"button",children:n.totalCost})}),s(ie,{children:[e(ae,{}),e(p.Suspense,{fallback:e(re,{}),children:e(s4,{spanNodeId:n.spanNodeId})})]})]})}const zr=(function(){var n=[{defaultValue:null,kind:"LocalArgument",name:"nodeId"}],a=[{kind:"Variable",name:"id",variableName:"nodeId"}],t={alias:null,args:null,kind:"ScalarField",name:"__typename",storageKey:null},l={alias:null,args:null,kind:"ScalarField",name:"cost",storageKey:null},i=[l],r={kind:"InlineFragment",selections:[{alias:null,args:null,concreteType:"SpanCostSummary",kind:"LinkedField",name:"costSummary",plural:!1,selections:[{alias:null,args:null,concreteType:"CostBreakdown",kind:"LinkedField",name:"total",plural:!1,selections:i,storageKey:null},{alias:null,args:null,concreteType:"CostBreakdown",kind:"LinkedField",name:"prompt",plural:!1,selections:i,storageKey:null},{alias:null,args:null,concreteType:"CostBreakdown",kind:"LinkedField",name:"completion",plural:!1,selections:i,storageKey:null}],storageKey:null},{alias:null,args:null,concreteType:"SpanCostDetailSummaryEntry",kind:"LinkedField",name:"costDetailSummaryEntries",plural:!0,selections:[{alias:null,args:null,kind:"ScalarField",name:"tokenType",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"isPrompt",storageKey:null},{alias:null,args:null,concreteType:"CostBreakdown",kind:"LinkedField",name:"value",plural:!1,selections:[l,{alias:null,args:null,kind:"ScalarField",name:"tokens",storageKey:null}],storageKey:null}],storageKey:null}],type:"Trace",abstractKey:null};return{fragment:{argumentDefinitions:n,kind:"Fragment",metadata:null,name:"TraceTokenCostsDetailsQuery",selections:[{alias:null,args:a,concreteType:null,kind:"LinkedField",name:"node",plural:!1,selections:[t,r],storageKey:null}],type:"Query",abstractKey:null},kind:"Request",operation:{argumentDefinitions:n,kind:"Operation",name:"TraceTokenCostsDetailsQuery",selections:[{alias:null,args:a,concreteType:null,kind:"LinkedField",name:"node",plural:!1,selections:[t,r,{alias:null,args:null,kind:"ScalarField",name:"id",storageKey:null}],storageKey:null}]},params:{cacheID:"0aa2a06633664f6e538e638254144b69",id:null,metadata:{},name:"TraceTokenCostsDetailsQuery",operationKind:"query",text:`query TraceTokenCostsDetailsQuery(
  $nodeId: ID!
) {
  node(id: $nodeId) {
    __typename
    ... on Trace {
      costSummary {
        total {
          cost
        }
        prompt {
          cost
        }
        completion {
          cost
        }
      }
      costDetailSummaryEntries {
        tokenType
        isPrompt
        value {
          cost
          tokens
        }
      }
    }
    id
  }
}
`}}})();zr.hash="508fdb06371456b54b7317143a9fabf4";function c4(n){const a=M.useLazyLoadQuery(zr,{nodeId:n.traceNodeId}),t=p.useMemo(()=>{var l,i,r,o,c,d;if(a.node.__typename==="Trace"){const u=a.node.costDetailSummaryEntries;if(!u)return{total:null,prompt:null,completion:null,promptDetails:null,completionDetails:null};const g=u.filter(L=>L.isPrompt),h=u.filter(L=>!L.isPrompt),f=((i=(l=a.node.costSummary)==null?void 0:l.total)==null?void 0:i.cost)??0,b=((o=(r=a.node.costSummary)==null?void 0:r.prompt)==null?void 0:o.cost)??0,y=((d=(c=a.node.costSummary)==null?void 0:c.completion)==null?void 0:d.cost)??0,v={};g.forEach(L=>{L.value.cost!=null&&(v[L.tokenType]=L.value.cost)});const k={};return h.forEach(L=>{L.value.cost!=null&&(k[L.tokenType]=L.value.cost)}),{total:f,prompt:b,completion:y,promptDetails:Object.keys(v).length>0?v:null,completionDetails:Object.keys(k).length>0?k:null}}return{total:null,prompt:null,completion:null,promptDetails:null,completionDetails:null}},[a.node]);return e(dn,{...t})}function Ym(n){return s(R,{children:[e(te,{children:e(cn,{size:n.size,role:"button",children:n.totalCost})}),s(ie,{children:[e(ae,{}),e(p.Suspense,{fallback:e(re,{}),children:e(c4,{traceNodeId:n.nodeId})})]})]})}const Mr=(function(){var n=[{defaultValue:null,kind:"LocalArgument",name:"nodeId"}],a=[{kind:"Variable",name:"id",variableName:"nodeId"}],t={alias:null,args:null,kind:"ScalarField",name:"__typename",storageKey:null},l={kind:"InlineFragment",selections:[{alias:null,args:null,concreteType:"SpanCostDetailSummaryEntry",kind:"LinkedField",name:"costDetailSummaryEntries",plural:!0,selections:[{alias:null,args:null,kind:"ScalarField",name:"tokenType",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"isPrompt",storageKey:null},{alias:null,args:null,concreteType:"CostBreakdown",kind:"LinkedField",name:"value",plural:!1,selections:[{alias:null,args:null,kind:"ScalarField",name:"cost",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"tokens",storageKey:null}],storageKey:null}],storageKey:null}],type:"ProjectSession",abstractKey:null};return{fragment:{argumentDefinitions:n,kind:"Fragment",metadata:null,name:"SessionTokenCostsDetailsQuery",selections:[{alias:null,args:a,concreteType:null,kind:"LinkedField",name:"node",plural:!1,selections:[t,l],storageKey:null}],type:"Query",abstractKey:null},kind:"Request",operation:{argumentDefinitions:n,kind:"Operation",name:"SessionTokenCostsDetailsQuery",selections:[{alias:null,args:a,concreteType:null,kind:"LinkedField",name:"node",plural:!1,selections:[t,l,{alias:null,args:null,kind:"ScalarField",name:"id",storageKey:null}],storageKey:null}]},params:{cacheID:"5c5cd200597f3c5c5415851c9d8a52fd",id:null,metadata:{},name:"SessionTokenCostsDetailsQuery",operationKind:"query",text:`query SessionTokenCostsDetailsQuery(
  $nodeId: ID!
) {
  node(id: $nodeId) {
    __typename
    ... on ProjectSession {
      costDetailSummaryEntries {
        tokenType
        isPrompt
        value {
          cost
          tokens
        }
      }
    }
    id
  }
}
`}}})();Mr.hash="4ff1881d1c2662709204991c58108dcb";function d4(n){const a=M.useLazyLoadQuery(Mr,{nodeId:n.sessionNodeId}),t=p.useMemo(()=>{if(a.node.__typename==="ProjectSession"){const l=a.node.costDetailSummaryEntries;if(!l)return{total:null,prompt:null,completion:null,promptDetails:null,completionDetails:null};const i=l.filter(g=>g.isPrompt),r=l.filter(g=>!g.isPrompt),o=i.reduce((g,h)=>g+(h.value.cost||0),0),c=r.reduce((g,h)=>g+(h.value.cost||0),0),d={};i.forEach(g=>{g.value.cost!=null&&(d[g.tokenType]=g.value.cost)});const u={};return r.forEach(g=>{g.value.cost!=null&&(u[g.tokenType]=g.value.cost)}),{total:o+c,prompt:o>0?o:null,completion:c>0?c:null,promptDetails:Object.keys(d).length>0?d:null,completionDetails:Object.keys(u).length>0?u:null}}return{total:null,prompt:null,completion:null,promptDetails:null,completionDetails:null}},[a.node]);return e(dn,{...t})}function Jm(n){return s(R,{children:[e(te,{children:e(cn,{size:n.size,role:"button",children:n.totalCost})}),s(ie,{children:[e(ae,{}),e(p.Suspense,{fallback:e(re,{}),children:e(d4,{sessionNodeId:n.nodeId})})]})]})}function u4(n){switch(n){case"OK":return"success";case"ERROR":return"danger";case"UNSET":return"grey-500";default:P()}}function g4({statusCode:n,...a}){let t=e(ll,{});const l=u4(n);switch(n){case"OK":t=e(wi,{});break;case"ERROR":t=e(Lt,{});break;case"UNSET":t=e(ll,{});break;default:P()}return e(T,{svg:t,color:l,"aria-label":n,...a})}const m4=m`
  height: var(--ac-global-dimension-size-75);
  border-radius: 3px;
  background-color: var(--ac-global-color-grey-300);
  width: 100%;
  position: relative;
  overflow: hidden;
`,p4=m`
  position: absolute;
  top: 0;
  bottom: 0;
`;function h4({color:n,overallTimeRange:a,spanTimeRange:t,...l}){const[i,r]=p.useMemo(()=>{const o=a.end.valueOf()-a.start.valueOf(),c=(t.start.valueOf()-a.start.valueOf())/o*100,d=(t.end.valueOf()-a.start.valueOf())/o*100;return[c,d]},[a,t]);return e("div",{className:"timeline-bar timeline-bar__track",css:m4,title:`${a.start.toLocaleString()} - ${a.end.toLocaleString()}`,...l,children:e("div",{className:"timeline-bar__bar",css:p4,title:`${t.start.toLocaleString()} - ${t.end.toLocaleString()}`,"data-start-percentage":i,"data-end-percentage":r,style:{backgroundColor:n,left:`${i}%`,right:`${100-r}%`}})})}const Fr=p.createContext(null);function Er(){const n=p.useContext(Fr);if(n===null)throw new Error("useTraceTree must be used within a TraceTreeProvider");return n}function f4(n){const[a,t]=p.useState(!1),l=p.useCallback(i=>{p.startTransition(()=>{t(i)})},[]);return e(Fr.Provider,{value:{isCollapsed:a,setIsCollapsed:l},children:n.children})}function b4(n){const a=n.reduce((l,i)=>(l.set(i.spanId,{span:i,children:[]}),l),new Map),t=[];for(const l of n){const i=a.get(l.spanId);if(l.parentId===null||!a.has(l.parentId))t.push(i);else{const r=a.get(l.parentId);r&&r.children.push(i)}}for(const l of a.values())l.children.sort((i,r)=>new Date(i.span.startTime).valueOf()-new Date(r.span.startTime).valueOf());return t.sort((l,i)=>new Date(l.span.startTime).valueOf()-new Date(i.span.startTime).valueOf()),t}const Ht=25,Dr="300px",y4="500px",v4="800px";function ep(n){const{spans:a,onSpanClick:t,selectedSpanNodeId:l}=n,i=b4(a),r=i[0].span,o={start:new Date(r.startTime),end:r.endTime?new Date(r.endTime):new Date};return e(f4,{children:s("div",{css:m`
          display: flex;
          flex-direction: column;
          overflow: hidden;
          height: 100%;
          align-items: stretch;
          container-type: inline-size;
        `,children:[e(C4,{}),e("ul",{css:m`
            flex: 1 1 auto;
            display: flex;
            flex-direction: column;
            width: 100%;
            overflow: auto;
            --trace-tree-nesting-indent: ${Ht}px;
            @container (width < ${Dr}) {
              --trace-tree-nesting-indent: 0;
              // Hide the collapse button
              .span-controls,
              .latency-text,
              .token-count-item,
              .span-tree-edge-connector,
              .span-tree-edge,
              .span-tree-timing {
                display: none;
                visibility: hidden;
                width: 0;
              }
              .span-node-wrap {
                padding-left: var(--ac-global-dimension-static-size-200);
              }
            }
            @container (width < ${y4}) {
              .span-tree-timing {
                display: none;
                visibility: hidden;
                width: 0;
              }
            }
            @container (width > ${v4}) {
              .span-tree-timing {
                width: 33%;
              }
            }
          `,"data-testid":"trace-tree",children:i.map(c=>e(_r,{node:c,overallTimeRange:o,onSpanClick:t,selectedSpanNodeId:l},c.span.id))})]})})}function C4(){const n=Ge(i=>i.showMetricsInTraceTree),a=Ge(i=>i.setShowMetricsInTraceTree),{isCollapsed:t,setIsCollapsed:l}=Er();return e("div",{className:"trace-tree-toolbar",css:m`
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        box-sizing: border-box;
        width: 100%;
        align-items: center;
        padding: var(--ac-global-dimension-size-100);
        border-bottom: 1px solid var(--ac-global-color-grey-300);
        height: var(--ac-global-dimension-size-600);
        @container (width < ${Dr}) {
          button {
            display: none;
          }
        }
      `,children:s(S,{direction:"row",justifyContent:"space-between",alignItems:"center",flex:"none",gap:"size-100",width:"100%",children:[e(ne,{level:3,children:"Trace"}),s(S,{direction:"row",gap:"size-100",className:"trace-tree-controls",children:[s(R,{children:[e(z,{variant:"default",size:"S","aria-label":t?"Expand all":"Collapse all",onPress:()=>{l(!t)},leadingVisual:e(T,{svg:t?e(jc,{}):e(Zc,{})})}),s(ke,{offset:-5,children:[e(ae,{}),t?"Expand all nested spans":"Collapse all nested spans"]})]}),s(R,{children:[e(z,{size:"S","aria-label":n?"Hide metrics in trace tree":"Show metrics in trace tree",onPress:()=>{a(!n)},leadingVisual:e(T,{svg:n?e(Yc,{}):e(Jc,{})})}),s(ke,{offset:-5,children:[e(ae,{}),n?"Hide metrics in trace tree":"Show metrics in trace tree"]})]})]})]})})}const k4=m`
  font-weight: 500;
  color: var(--ac-global-text-color-900);
  display: inline-block;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
`;function _r(n){const{node:a,selectedSpanNodeId:t,onSpanClick:l,nestingLevel:i=0,overallTimeRange:r}=n,o=a.children,[c,d]=p.useState(!1),{isCollapsed:u}=Er(),g=o.length>0,h=Ge(E=>E.showMetricsInTraceTree),f=t===a.span.id,b=p.useRef(null);p.useEffect(()=>{f&&b.current&&b.current.scrollIntoView({behavior:"smooth",block:"nearest"})},[f]),p.useEffect(()=>{d(u)},[u]);const{name:y,latencyMs:v,statusCode:k,tokenCountTotal:L}=a.span;return s("div",{ref:b,children:[e("button",{className:"button--reset",css:m`
          width: 100%;
          overflow: hidden;
          cursor: pointer;
        `,onClick:()=>{p.startTransition(()=>{l&&l(a.span)})},children:s(L4,{isSelected:t===a.span.id,nestingLevel:i,children:[s(S,{direction:"row",gap:"size-100",justifyContent:"start",alignItems:"center",flex:"1 1 auto",minWidth:0,css:m`
              overflow: hidden;
            `,children:[e(Z5,{spanKind:a.span.spanKind}),e("span",{css:k4,title:y,children:y}),k==="ERROR"?e(g4,{statusCode:"ERROR",css:m`
                  font-size: var(--ac-global-font-size-m);
                `}):null,typeof L=="number"&&L>0&&h?e(n4,{tokenCountTotal:L,nodeId:a.span.id}):null]}),h?s("div",{css:T4,className:"span-tree-timing",children:[v!=null?e(w5,{latencyMs:v,showIcon:!1,size:"XS"}):null,e(z4,{spanKind:a.span.spanKind,overallTimeRange:r,spanTimeRange:{start:new Date(a.span.startTime),end:a.span.endTime?new Date(a.span.endTime):new Date}})]}):null,e("div",{css:x4,"data-testid":"span-controls",className:"span-controls",children:g?e(I4,{isCollapsed:c,onClick:()=>{d(!c)}}):null})]})}),o.length?e("ul",{css:m`
            display: ${c?"none":"flex"};
            flex-direction: column;
          `,children:o.map((E,O)=>{const F=o[O+1];return s("li",{css:m`
                  position: relative;
                `,children:[F?e(w4,{...F.span,nestingLevel:i}):null,e(S4,{...E.span,nestingLevel:i}),e(_r,{node:E,overallTimeRange:r,onSpanClick:l,selectedSpanNodeId:t,nestingLevel:i+1})]},E.span.spanId)})}):null]})}function L4(n){return e("div",{className:V("span-node-wrap",{"is-selected":n.isSelected}),css:m`
        width: 100%;
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        gap: var(--ac-global-dimension-static-size-100);
        padding-right: var(--ac-global-dimension-static-size-100);
        padding-top: var(--ac-global-dimension-static-size-100);
        padding-bottom: var(--ac-global-dimension-static-size-100);
        border-left: 4px solid transparent;
        box-sizing: border-box;
        &:hover {
          background-color: var(--ac-global-color-grey-200);
        }
        &.is-selected {
          background-color: var(--ac-global-color-primary-100);
          border-color: var(--ac-global-color-primary-200);
        }
        & > *:first-of-type {
          margin-left: calc(
            (${n.nestingLevel} * var(--trace-tree-nesting-indent)) + 16px
          );
        }
      `,children:n.children})}function w4({statusCode:n,nestingLevel:a}){const t=n==="ERROR";return e("div",{"aria-hidden":"true","data-testid":"span-tree-edge-connector",className:"span-tree-edge-connector","data-status-code":n,css:m`
        position: absolute;
        border-left: 1px solid
          ${t?"var(--ac-global-color-danger)":"var(--ac-global-color-grey-500)"};
        z-index: ${t?1:0};
        top: 0;
        left: ${a*Ht+29}px;
        width: 42px;
        bottom: 0;
        z-index: 1;
      `})}function S4({nestingLevel:n,statusCode:a}){const t=a==="ERROR",l=t?"var(--ac-global-color-danger)":"var(--ac-global-color-grey-500)";return e("div",{"aria-hidden":"true",className:"span-tree-edge",css:m`
        position: absolute;
        border-left: 1px solid ${l};
        border-bottom: 1px solid ${l};
        z-index: ${t?1:0};
        border-radius: 0 0 0 11px;
        top: -5px;
        left: ${n*Ht+29}px;
        width: 11px;
        height: 22px;
      `})}const x4=m`
  width: 20px;
  flex: none;
`,T4=m`
  gap: var(--ac-global-dimension-static-size-100);
  width: 150px;
  transition: all 0.2s ease-in-out;
  flex: none;
  display: flex;
  flex-direction: row;
  align-items: center;
  .latency-text {
    justify-content: end !important;
    min-width: 2.5rem;
    float: right;
  }
`,A4=m`
  display: flex;
  align-items: center;
  justify-content: center;
  width: 20px;
  height: 20px;
  border: none;
  background: none;
  cursor: pointer;
  color: var(--ac-global-text-color-900);
  border-radius: 4px;
  transition: transform 0.2s;
  transition: background-color 0.5s;
  flex: none;
  background-color: rgba(0, 0, 0, 0.1);
  &:hover {
    background-color: rgba(0, 0, 0, 0.3);
  }
  &.is-collapsed {
    transform: rotate(-90deg);
  }
`;function I4({isCollapsed:n,onClick:a}){return e("button",{onClick:t=>{t.stopPropagation(),t.preventDefault(),a()},className:V("button--reset collapse-toggle-button",{"is-collapsed":n}),css:A4,children:e(T,{svg:e(vi,{})})})}function z4({spanKind:n,...a}){const t=wr({spanKind:n});return e(h4,{color:t,...a})}const M4=m`
  width: 100%;
  display: flex;
  flex-direction: row;
  overflow: hidden;
  border-radius: 8px;
  gap: 2px;
`,F4=m`
  height: 100%;
  flex-shrink: 0;
  flex-grow: 0;
`,E4=({height:n=6,segments:a,totalValue:t})=>{const l=t??a.reduce((i,r)=>i+r.value,0);return e("div",{style:{height:`${n}px`},css:M4,children:a.map(i=>{const r=l>0?i.value/l*100:0,o=i.color;return e("div",{css:F4,style:{width:`${r}%`,backgroundColor:o}},i.name)})})};function np({valueLabel:n,totalValue:a,formatter:t,segments:l}){const i=q3(),r=l.map((o,c)=>({...o,color:o.color||X3(c,i)}));return s(S,{direction:"column",gap:"size-150",children:[s(S,{direction:"row",gap:"size-200",justifyContent:"space-between",children:[s(C,{weight:"heavy",children:["Total ",n]}),e(S,{direction:"row",gap:"size-400",children:e(C,{weight:"heavy",children:t(a)})})]}),e(E4,{height:6,totalValue:a,segments:r}),e(S,{direction:"column",gap:"size-100",children:r.map(o=>s(S,{direction:"row",gap:"size-200",justifyContent:"space-between",children:[s(S,{direction:"row",gap:"size-100",alignItems:"center",children:[e("div",{style:{backgroundColor:o.color,width:8,height:8,borderRadius:"100%"}}),e(C,{weight:"heavy",children:o.name})]}),e(S,{direction:"row",gap:"size-400",children:e(C,{weight:"heavy",children:t(o.value)})})]},o.name))})]})}function D4(n){return p.useMemo(()=>{try{const a=JSON.parse(n);return{text:JSON.stringify(a,null,2),textType:"json"}}catch{return{text:n,textType:"string"}}},[n])}function _4({children:n,preCSS:a}){const{text:t,textType:l}=D4(n);if(l==="string")return e("pre",{css:m`
          white-space: pre-wrap;
          text-wrap: wrap;
          overflow-wrap: anywhere;
          font-size: var(--ac-global-font-size-s);
          margin: 0;
          ${a}
        `,children:t});if(l==="json")return e(gr,{value:t});P()}const Kr=p.createContext(null);function Pr(){let n=p.useContext(Kr);return n===null&&(console.warn("useMarkdownMode must be used within a MarkdownDisplayProvider"),n={mode:"text",setMode:()=>{}}),n}function ap(n){const a=Ge(i=>i.markdownDisplayMode),t=Ge(i=>i.setMarkdownDisplayMode),l=p.useCallback(i=>{p.startTransition(()=>{t(i)})},[t]);return e(Kr.Provider,{value:{mode:a,setMode:l},children:n.children})}const K4=m`
  a {
    color: var(--ac-global-link-color);
    &:visited {
      color: var(--ac-global-link-color-visited);
    }
  }
  /* Remove the margin on the first and last paragraph */
  p:first-of-type {
    margin-top: 0;
  }
  p:last-of-type {
    margin-bottom: 0;
  }
  code {
    text-wrap: wrap;
  }
`;function P4({children:n,mode:a,margin:t="default"}){const l=t==="none"?m`
          margin: 0;
        `:m`
          margin: var(--ac-global-dimension-static-size-200);
        `;return a==="markdown"?e("div",{css:K4,children:e(D1,{remarkPlugins:[_1],css:l,children:n})}):e(_4,{preCSS:l,children:n})}function tp({children:n,margin:a="default"}){const{mode:t}=Pr();return e(P4,{mode:t,margin:a,children:n})}const V4=["text","markdown"];function R4(n){return typeof n=="string"&&V4.includes(n)}function O4({mode:n,onModeChange:a}){return s(Ne,{"aria-label":"Markdown Mode",selectedKey:n,css:m`
        button {
          width: 140px;
          min-width: 140px;
        }
      `,size:"S",onSelectionChange:t=>{if(R4(t))a(t);else throw new Error(`Unknown markdown mode: ${t}`)},children:[s(z,{children:[e(Oe,{}),e(Ae,{})]}),e(ue,{children:s(we,{children:[e(ee,{id:"text",children:"Text"},"text"),e(ee,{id:"markdown",children:"Markdown"},"markdown")]})})]})}function lp(){const{mode:n,setMode:a}=Pr();return e(O4,{mode:n,onModeChange:a})}function ip(n){const{spanKind:a,size:t="M"}=n,l=p.useMemo(()=>{let i="var(--ac-global-color-grey-300)";switch(a){case"llm":i="var(--ac-global-color-orange-500)";break;case"chain":i="var(--ac-global-color-blue-500)";break;case"retriever":i="var(--ac-global-color-seafoam-500)";break;case"reranker":i="var(--ac-global-color-celery-500)";break;case"embedding":i="var(--ac-global-color-indigo-500)";break;case"agent":i="var(--ac-global-color-grey-500)";break;case"tool":i="var(--ac-global-color-yellow-500)";break;case"evaluator":i="var(--ac-global-color-indigo-500)";break;case"guardrail":i="var(--ac-global-color-fuchsia-500)";break}return i},[a]);return e(je,{color:l,size:t,children:a})}const Vr=(function(){var n={alias:null,args:null,kind:"ScalarField",name:"id",storageKey:null},a={alias:null,args:null,kind:"ScalarField",name:"name",storageKey:null},t={alias:null,args:null,kind:"ScalarField",name:"label",storageKey:null},l={alias:null,args:null,kind:"ScalarField",name:"score",storageKey:null};return{argumentDefinitions:[],kind:"Fragment",metadata:null,name:"AnnotationSummaryGroup",selections:[{alias:null,args:null,concreteType:"Project",kind:"LinkedField",name:"project",plural:!1,selections:[n,{alias:null,args:null,concreteType:"AnnotationConfigConnection",kind:"LinkedField",name:"annotationConfigs",plural:!1,selections:[{alias:null,args:null,concreteType:"AnnotationConfigEdge",kind:"LinkedField",name:"edges",plural:!0,selections:[{alias:null,args:null,concreteType:null,kind:"LinkedField",name:"node",plural:!1,selections:[{kind:"InlineFragment",selections:[{alias:null,args:null,kind:"ScalarField",name:"annotationType",storageKey:null}],type:"AnnotationConfigBase",abstractKey:"__isAnnotationConfigBase"},{kind:"InlineFragment",selections:[n,a,{alias:null,args:null,kind:"ScalarField",name:"optimizationDirection",storageKey:null},{alias:null,args:null,concreteType:"CategoricalAnnotationValue",kind:"LinkedField",name:"values",plural:!0,selections:[t,l],storageKey:null}],type:"CategoricalAnnotationConfig",abstractKey:null}],storageKey:null}],storageKey:null}],storageKey:null}],storageKey:null},{alias:null,args:null,concreteType:"SpanAnnotation",kind:"LinkedField",name:"spanAnnotations",plural:!0,selections:[n,a,t,l,{alias:null,args:null,kind:"ScalarField",name:"annotatorKind",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"createdAt",storageKey:null},{alias:null,args:null,concreteType:"User",kind:"LinkedField",name:"user",plural:!1,selections:[{alias:null,args:null,kind:"ScalarField",name:"username",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"profilePictureUrl",storageKey:null}],storageKey:null}],storageKey:null},{alias:null,args:null,concreteType:"AnnotationSummary",kind:"LinkedField",name:"spanAnnotationSummaries",plural:!0,selections:[{alias:null,args:null,concreteType:"LabelFraction",kind:"LinkedField",name:"labelFractions",plural:!0,selections:[{alias:null,args:null,kind:"ScalarField",name:"fraction",storageKey:null},t],storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"meanScore",storageKey:null},a],storageKey:null}],type:"Span",abstractKey:null}})();Vr.hash="1bfa3a69e85bd44da68677f8f467150a";const N4=({value:n,fallback:a="--",...t})=>n==null||typeof n!="number"||isNaN(n)?e(C,{...t,fontFamily:"mono",children:a}):s(C,{...t,children:[e("span",{"aria-label":"mean score",children:"μ "}),e("span",{className:"font-mono",children:`${We(n)}`})]}),$4=m`
  & thead tr th {
    background-color: transparent;
  }
`;function B4({annotations:n,children:a,width:t,meanScore:l,showFilterActions:i}){const r=p.useMemo(()=>n.filter(c=>c.label!=null||c.score!=null),[n]),o=r[0];return o?s(_e,{children:[e(te,{children:e("span",{role:"button",children:a})}),e(hr,{children:s(ue,{shouldCloseOnInteractOutside:()=>!0,isKeyboardDismissDisabled:!1,style:{minWidth:t},children:[e(It,{}),e(be,{css:m`
              border-radius: var(--ac-global-radius-200);
            `,children:e(pa,{autoFocus:!0,contain:!0,restoreFocus:!0,children:e(w,{children:s(S,{direction:"column",children:[e(w,{borderBottomWidth:"thin",borderColor:"dark",paddingX:"size-200",paddingY:"size-100",children:s(S,{width:"100%",justifyContent:"space-between",children:[s(S,{direction:"row",gap:"size-100",alignItems:"center",children:[e(Nt,{size:"M",annotationName:o.name}),e(C,{weight:"heavy",title:o.name,size:"M",children:e(da,{maxWidth:"300px",children:o.name})})]}),s(R,{delay:0,children:[e(_i,{children:e(N4,{size:"L",value:l,fallback:null})}),s(ke,{placement:"top",children:[e(ae,{}),e(C,{children:"Mean Score"})]})]})]})}),e(w,{overflow:"auto",maxHeight:"300px",position:"relative",children:s("table",{css:m(Ot,$4),children:[e("thead",{children:s("tr",{children:[e("th",{children:"author"}),e("th",{children:"label"}),e("th",{children:"score"}),i?e("th",{children:"filters"}):null]})}),e("tbody",{children:r.map(c=>{var d,u,g;return s("tr",{css:m`
                              padding-left: var(ac-global-dimensions-size-200);
                            `,children:[e("td",{children:s(S,{wrap:"nowrap",gap:"size-100",alignItems:"center",children:[e(yr,{name:(d=c==null?void 0:c.user)==null?void 0:d.username,profilePictureUrl:(u=c==null?void 0:c.user)==null?void 0:u.profilePictureUrl,size:16}),e(C,{children:((g=c==null?void 0:c.user)==null?void 0:g.username)??"system"})]})}),e("td",{children:c.label?e(C,{title:c.label,children:e(da,{maxWidth:i?"150px":"200px",children:c.label})}):"--"}),e("td",{children:c.score!=null?We(c.score):"--"}),i?e("td",{children:e(S,{justifyContent:"end",flexGrow:1,children:e(ks,{annotation:c})})}):null]},c.id)})})]})})]})})})})]})})]}):null}const Rr=n=>{const a=M.useFragment(Vr,n),{spanAnnotations:t,spanAnnotationSummaries:l}=a,i=p.useMemo(()=>l.filter(c=>c.name!=="note").sort((c,d)=>c.name.localeCompare(d.name)),[l]),r=p.useMemo(()=>t.reduce((c,d)=>(d.label==null&&d.score==null||(c[d.name]?c[d.name]=[d,...c[d.name]].sort((u,g)=>new Date(g.createdAt).getTime()-new Date(u.createdAt).getTime()):c[d.name]=[d]),c),{}),[t]),o=p.useMemo(()=>a.project.annotationConfigs.edges.reduce((c,d)=>{const u=d.node.name;return u&&d.node.annotationType==="CATEGORICAL"&&(c[u]=d.node),c},{}),[a.project.annotationConfigs]);return{sortedSummariesByName:i,annotationsByName:r,categoricalAnnotationConfigsByName:o}},H4=m`
  min-height: 20px;
  align-items: center;
  justify-content: center;
  display: flex;
`,rp=({span:n,showFilterActions:a=!1,renderEmptyState:t})=>{const{sortedSummariesByName:l,annotationsByName:i,categoricalAnnotationConfigsByName:r}=Rr(n);return l.length===0&&t?t():e(S,{direction:"row",gap:"size-50",wrap:"wrap",children:l.map(o=>{var u;const c=(u=i[o.name])==null?void 0:u[0],d=o==null?void 0:o.meanScore;return c?e(B4,{annotations:i[o.name],width:"500px",meanScore:d,showFilterActions:a,children:e(ur,{annotation:c,annotationDisplayPreference:"none",css:H4,clickable:!0,children:d!=null?e(Ss,{name:c.name,meanScore:d,size:"S",disableAnimation:!0,annotationConfig:r[c.name]}):null})},c.id):null})})},op=({span:n,renderEmptyState:a})=>{const{sortedSummariesByName:t,annotationsByName:l,categoricalAnnotationConfigsByName:i}=Rr(n);return t.length===0&&a?a():e(S,{direction:"row",gap:"size-400",children:t.map(r=>{var c;const o=(c=l[r.name])==null?void 0:c[0];return o?e(Ls,{name:o.name,children:e(ws,{name:o.name,meanScore:r.meanScore,labelFractions:r.labelFractions,annotationConfig:i[o.name]})},o.id):null})})},j4=({hotkey:n,accept:a})=>{const t=K1();return P1(n,()=>{t==null||t.focusFirst({accept:a})},{preventDefault:!0}),null},Z4=p.forwardRef(({children:n,title:a,panelProps:t,panelResizeHandleProps:l,resizable:i=!1,bordered:r=!0,disabled:o},c)=>{const d=p.useRef(null);p.useImperativeHandle(c,()=>d.current);const[u,g]=p.useState(!1),h=()=>{const f=d.current;f!=null&&f.isCollapsed()?f==null||f.expand():f==null||f.collapse()};return s(U,{children:[i&&e(V1,{...l,"data-bordered":r,css:m(L5,m`
                border-radius: var(--ac-global-rounding-small);
                opacity: 1;
                background-color: unset;
                &[data-bordered="true"] {
                  background-color: var(--ac-global-border-color-default);
                }
                &[data-panel-group-direction="vertical"] {
                  height: 1px;
                }
                &:hover,
                &:focus,
                &:active,
                &:focus-visible {
                  // Make hover target bigger
                  background-color: var(--ac-global-color-primary);
                }
                &:not([data-resize-handle-state="drag"]) ~ [data-panel] {
                  // transition: flex 0.2s ease-in-out;
                }
              `)}),e(G4,{onClick:h,collapsed:u,bordered:r,disabled:o,children:a}),e(R1,{maxSize:100,...t,ref:d,collapsible:!0,onCollapse:()=>{var f;g(!0),(f=t==null?void 0:t.onCollapse)==null||f.call(t)},onExpand:()=>{var f;g(!1),(f=t==null?void 0:t.onExpand)==null||f.call(t)},children:n})]})});Z4.displayName="TitledPanel";const U4=m`
  all: unset;
  width: 100%;
  &:hover {
    cursor: pointer;
    background-color: var(--ac-global-input-field-background-color-active);
  }
  &:hover[disabled] {
    cursor: default;
    background-color: unset;
  }
  &[disabled] {
    opacity: var(--ac-opacity-disabled);
  }
  display: flex;
  align-items: center;
  gap: var(--ac-global-dimension-size-100);
  padding: var(--ac-global-dimension-size-100)
    var(--ac-global-dimension-size-50);
  font-weight: var(--px-font-weight-heavy);
  font-size: var(--ac-global-font-size-s);
  &[data-bordered="true"] {
    border-bottom: 1px solid var(--ac-global-border-color-default);
  }
  &[data-collapsed="true"] {
    border-bottom: none;
  }
`,G4=({children:n,collapsed:a,bordered:t,disabled:l,...i})=>s("button",{...i,type:"button","data-collapsed":a,"data-bordered":t,css:U4,disabled:a===void 0||l,children:[a!==void 0&&e(T,{"data-collapsed":a,svg:e(vi,{}),css:m`
            transition: transform 0.2s ease-in-out;
            &[data-collapsed="true"] {
              transform: rotate(-90deg);
            }
          `}),n]}),Or=(function(){var n={defaultValue:null,kind:"LocalArgument",name:"filterUserIds"},a={defaultValue:null,kind:"LocalArgument",name:"input"},t={defaultValue:null,kind:"LocalArgument",name:"name"},l={defaultValue:null,kind:"LocalArgument",name:"projectId"},i={defaultValue:null,kind:"LocalArgument",name:"spanId"},r={defaultValue:null,kind:"LocalArgument",name:"timeRange"},o=[{items:[{kind:"Variable",name:"input.0",variableName:"input"}],kind:"ListValue",name:"input"}],c=[{kind:"Variable",name:"id",variableName:"projectId"}],d=[{kind:"Variable",name:"annotationName",variableName:"name"},{kind:"Variable",name:"timeRange",variableName:"timeRange"}],u=[{kind:"Variable",name:"id",variableName:"spanId"}],g={alias:null,args:null,kind:"ScalarField",name:"__typename",storageKey:null},h={alias:null,args:null,kind:"ScalarField",name:"id",storageKey:null},f={alias:null,args:null,kind:"ScalarField",name:"annotationType",storageKey:null},b={kind:"InlineFragment",selections:[f],type:"AnnotationConfigBase",abstractKey:"__isAnnotationConfigBase"},y={alias:null,args:null,kind:"ScalarField",name:"optimizationDirection",storageKey:null},v={alias:null,args:null,kind:"ScalarField",name:"name",storageKey:null},k={alias:null,args:null,kind:"ScalarField",name:"label",storageKey:null},L={alias:null,args:null,kind:"ScalarField",name:"score",storageKey:null},E={alias:null,args:null,concreteType:"CategoricalAnnotationValue",kind:"LinkedField",name:"values",plural:!0,selections:[k,L],storageKey:null},O={kind:"InlineFragment",selections:[h],type:"Node",abstractKey:"__isNode"},F={alias:null,args:null,kind:"ScalarField",name:"fraction",storageKey:null},D={alias:null,args:null,kind:"ScalarField",name:"meanScore",storageKey:null},X={alias:null,args:null,kind:"ScalarField",name:"annotatorKind",storageKey:null},Y={alias:null,args:null,kind:"ScalarField",name:"createdAt",storageKey:null},_={alias:null,args:null,kind:"ScalarField",name:"explanation",storageKey:null};return{fragment:{argumentDefinitions:[n,a,t,l,i,r],kind:"Fragment",metadata:null,name:"SpanAnnotationsEditorCreateAnnotationMutation",selections:[{alias:null,args:o,concreteType:"SpanAnnotationMutationPayload",kind:"LinkedField",name:"createSpanAnnotations",plural:!1,selections:[{alias:null,args:null,concreteType:"Query",kind:"LinkedField",name:"query",plural:!1,selections:[{alias:"project",args:c,concreteType:null,kind:"LinkedField",name:"node",plural:!1,selections:[{kind:"InlineFragment",selections:[{args:d,kind:"FragmentSpread",name:"AnnotationSummaryValueFragment"}],type:"Project",abstractKey:null}],storageKey:null},{alias:null,args:u,concreteType:null,kind:"LinkedField",name:"node",plural:!1,selections:[{kind:"InlineFragment",selections:[{args:null,kind:"FragmentSpread",name:"AnnotationSummaryGroup"},{args:null,kind:"FragmentSpread",name:"TraceHeaderRootSpanAnnotationsFragment"},{args:[{kind:"Variable",name:"filterUserIds",variableName:"filterUserIds"}],kind:"FragmentSpread",name:"SpanAnnotationsEditor_spanAnnotations"},{args:null,kind:"FragmentSpread",name:"SpanAsideAnnotationList_span"},{args:null,kind:"FragmentSpread",name:"SpanFeedback_annotations"}],type:"Span",abstractKey:null}],storageKey:null}],storageKey:null}],storageKey:null}],type:"Mutation",abstractKey:null},kind:"Request",operation:{argumentDefinitions:[t,a,i,n,r,l],kind:"Operation",name:"SpanAnnotationsEditorCreateAnnotationMutation",selections:[{alias:null,args:o,concreteType:"SpanAnnotationMutationPayload",kind:"LinkedField",name:"createSpanAnnotations",plural:!1,selections:[{alias:null,args:null,concreteType:"Query",kind:"LinkedField",name:"query",plural:!1,selections:[{alias:"project",args:c,concreteType:null,kind:"LinkedField",name:"node",plural:!1,selections:[g,h,{kind:"InlineFragment",selections:[{alias:null,args:null,concreteType:"AnnotationConfigConnection",kind:"LinkedField",name:"annotationConfigs",plural:!1,selections:[{alias:null,args:null,concreteType:"AnnotationConfigEdge",kind:"LinkedField",name:"edges",plural:!0,selections:[{alias:null,args:null,concreteType:null,kind:"LinkedField",name:"node",plural:!1,selections:[g,b,{kind:"InlineFragment",selections:[f,h,y,v,E],type:"CategoricalAnnotationConfig",abstractKey:null},O],storageKey:null}],storageKey:null}],storageKey:null},{alias:null,args:d,concreteType:"AnnotationSummary",kind:"LinkedField",name:"spanAnnotationSummary",plural:!1,selections:[v,{alias:null,args:null,concreteType:"LabelFraction",kind:"LinkedField",name:"labelFractions",plural:!0,selections:[k,F],storageKey:null},D],storageKey:null}],type:"Project",abstractKey:null}],storageKey:null},{alias:null,args:u,concreteType:null,kind:"LinkedField",name:"node",plural:!1,selections:[g,h,{kind:"InlineFragment",selections:[{alias:null,args:null,concreteType:"Project",kind:"LinkedField",name:"project",plural:!1,selections:[h,{alias:null,args:null,concreteType:"AnnotationConfigConnection",kind:"LinkedField",name:"annotationConfigs",plural:!1,selections:[{alias:null,args:null,concreteType:"AnnotationConfigEdge",kind:"LinkedField",name:"edges",plural:!0,selections:[{alias:null,args:null,concreteType:null,kind:"LinkedField",name:"node",plural:!1,selections:[g,b,{kind:"InlineFragment",selections:[h,v,y,E],type:"CategoricalAnnotationConfig",abstractKey:null},O],storageKey:null}],storageKey:null},{alias:"configs",args:null,concreteType:"AnnotationConfigEdge",kind:"LinkedField",name:"edges",plural:!0,selections:[{alias:"config",args:null,concreteType:null,kind:"LinkedField",name:"node",plural:!1,selections:[g,O,{kind:"InlineFragment",selections:[v],type:"AnnotationConfigBase",abstractKey:"__isAnnotationConfigBase"}],storageKey:null}],storageKey:null}],storageKey:null}],storageKey:null},{alias:null,args:null,concreteType:"SpanAnnotation",kind:"LinkedField",name:"spanAnnotations",plural:!0,selections:[h,v,k,L,X,Y,{alias:null,args:null,concreteType:"User",kind:"LinkedField",name:"user",plural:!1,selections:[{alias:null,args:null,kind:"ScalarField",name:"username",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"profilePictureUrl",storageKey:null},h],storageKey:null},_,{alias:null,args:null,kind:"ScalarField",name:"metadata",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"identifier",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"source",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"updatedAt",storageKey:null}],storageKey:null},{alias:null,args:null,concreteType:"AnnotationSummary",kind:"LinkedField",name:"spanAnnotationSummaries",plural:!0,selections:[{alias:null,args:null,concreteType:"LabelFraction",kind:"LinkedField",name:"labelFractions",plural:!0,selections:[F,k],storageKey:null},D,v],storageKey:null},{alias:"filteredSpanAnnotations",args:[{fields:[{kind:"Literal",name:"exclude",value:{names:["note"]}},{fields:[{kind:"Variable",name:"userIds",variableName:"filterUserIds"}],kind:"ObjectValue",name:"include"}],kind:"ObjectValue",name:"filter"}],concreteType:"SpanAnnotation",kind:"LinkedField",name:"spanAnnotations",plural:!0,selections:[h,v,X,L,k,_,Y],storageKey:null}],type:"Span",abstractKey:null}],storageKey:null}],storageKey:null}],storageKey:null}]},params:{cacheID:"fe4bd60106516a1dd9a0d9b6b9d705cb",id:null,metadata:{},name:"SpanAnnotationsEditorCreateAnnotationMutation",operationKind:"mutation",text:`mutation SpanAnnotationsEditorCreateAnnotationMutation(
  $name: String!
  $input: CreateSpanAnnotationInput!
  $spanId: ID!
  $filterUserIds: [ID]
  $timeRange: TimeRange!
  $projectId: ID!
) {
  createSpanAnnotations(input: [$input]) {
    query {
      project: node(id: $projectId) {
        __typename
        ... on Project {
          ...AnnotationSummaryValueFragment_20r1YH
        }
        id
      }
      node(id: $spanId) {
        __typename
        ... on Span {
          ...AnnotationSummaryGroup
          ...TraceHeaderRootSpanAnnotationsFragment
          ...SpanAnnotationsEditor_spanAnnotations_3lpqY
          ...SpanAsideAnnotationList_span
          ...SpanFeedback_annotations
        }
        id
      }
    }
  }
}

fragment AnnotationSummaryGroup on Span {
  project {
    id
    annotationConfigs {
      edges {
        node {
          __typename
          ... on AnnotationConfigBase {
            __isAnnotationConfigBase: __typename
            annotationType
          }
          ... on CategoricalAnnotationConfig {
            id
            name
            optimizationDirection
            values {
              label
              score
            }
          }
          ... on Node {
            __isNode: __typename
            id
          }
        }
      }
    }
  }
  spanAnnotations {
    id
    name
    label
    score
    annotatorKind
    createdAt
    user {
      username
      profilePictureUrl
      id
    }
  }
  spanAnnotationSummaries {
    labelFractions {
      fraction
      label
    }
    meanScore
    name
  }
}

fragment AnnotationSummaryValueFragment_20r1YH on Project {
  annotationConfigs {
    edges {
      node {
        __typename
        ... on AnnotationConfigBase {
          __isAnnotationConfigBase: __typename
          annotationType
        }
        ... on CategoricalAnnotationConfig {
          annotationType
          id
          optimizationDirection
          name
          values {
            label
            score
          }
        }
        ... on Node {
          __isNode: __typename
          id
        }
      }
    }
  }
  spanAnnotationSummary(annotationName: $name, timeRange: $timeRange) {
    name
    labelFractions {
      label
      fraction
    }
    meanScore
  }
  id
}

fragment SpanAnnotationsEditor_spanAnnotations_3lpqY on Span {
  id
  filteredSpanAnnotations: spanAnnotations(filter: {exclude: {names: ["note"]}, include: {userIds: $filterUserIds}}) {
    id
    name
    annotatorKind
    score
    label
    explanation
    createdAt
  }
}

fragment SpanAsideAnnotationList_span on Span {
  project {
    id
    annotationConfigs {
      configs: edges {
        config: node {
          __typename
          ... on Node {
            __isNode: __typename
            id
          }
          ... on AnnotationConfigBase {
            __isAnnotationConfigBase: __typename
            name
          }
        }
      }
    }
  }
  spanAnnotations {
    id
  }
  ...AnnotationSummaryGroup
}

fragment SpanFeedback_annotations on Span {
  id
  spanAnnotations {
    id
    name
    label
    score
    explanation
    metadata
    annotatorKind
    identifier
    source
    createdAt
    updatedAt
    user {
      id
      username
      profilePictureUrl
    }
  }
}

fragment TraceHeaderRootSpanAnnotationsFragment on Span {
  ...AnnotationSummaryGroup
}
`}}})();Or.hash="470188a966012ed4819c3644e1463a4f";const Nr=(function(){var n={defaultValue:null,kind:"LocalArgument",name:"annotationId"},a={defaultValue:null,kind:"LocalArgument",name:"explanation"},t={defaultValue:null,kind:"LocalArgument",name:"filterUserIds"},l={defaultValue:null,kind:"LocalArgument",name:"label"},i={defaultValue:null,kind:"LocalArgument",name:"name"},r={defaultValue:null,kind:"LocalArgument",name:"projectId"},o={defaultValue:null,kind:"LocalArgument",name:"score"},c={defaultValue:null,kind:"LocalArgument",name:"spanId"},d={defaultValue:null,kind:"LocalArgument",name:"timeRange"},u=[{items:[{fields:[{kind:"Variable",name:"annotationId",variableName:"annotationId"},{kind:"Literal",name:"annotatorKind",value:"HUMAN"},{kind:"Variable",name:"explanation",variableName:"explanation"},{kind:"Variable",name:"label",variableName:"label"},{kind:"Variable",name:"name",variableName:"name"},{kind:"Variable",name:"score",variableName:"score"},{kind:"Literal",name:"source",value:"APP"}],kind:"ObjectValue",name:"input.0"}],kind:"ListValue",name:"input"}],g=[{kind:"Variable",name:"id",variableName:"projectId"}],h=[{kind:"Variable",name:"annotationName",variableName:"name"},{kind:"Variable",name:"timeRange",variableName:"timeRange"}],f=[{kind:"Variable",name:"id",variableName:"spanId"}],b={alias:null,args:null,kind:"ScalarField",name:"__typename",storageKey:null},y={alias:null,args:null,kind:"ScalarField",name:"id",storageKey:null},v={alias:null,args:null,kind:"ScalarField",name:"annotationType",storageKey:null},k={kind:"InlineFragment",selections:[v],type:"AnnotationConfigBase",abstractKey:"__isAnnotationConfigBase"},L={alias:null,args:null,kind:"ScalarField",name:"optimizationDirection",storageKey:null},E={alias:null,args:null,kind:"ScalarField",name:"name",storageKey:null},O={alias:null,args:null,kind:"ScalarField",name:"label",storageKey:null},F={alias:null,args:null,kind:"ScalarField",name:"score",storageKey:null},D={alias:null,args:null,concreteType:"CategoricalAnnotationValue",kind:"LinkedField",name:"values",plural:!0,selections:[O,F],storageKey:null},X={kind:"InlineFragment",selections:[y],type:"Node",abstractKey:"__isNode"},Y={alias:null,args:null,kind:"ScalarField",name:"fraction",storageKey:null},_={alias:null,args:null,kind:"ScalarField",name:"meanScore",storageKey:null},A={alias:null,args:null,kind:"ScalarField",name:"annotatorKind",storageKey:null},H={alias:null,args:null,kind:"ScalarField",name:"createdAt",storageKey:null},oe={alias:null,args:null,kind:"ScalarField",name:"explanation",storageKey:null};return{fragment:{argumentDefinitions:[n,a,t,l,i,r,o,c,d],kind:"Fragment",metadata:null,name:"SpanAnnotationsEditorEditAnnotationMutation",selections:[{alias:null,args:u,concreteType:"SpanAnnotationMutationPayload",kind:"LinkedField",name:"patchSpanAnnotations",plural:!1,selections:[{alias:null,args:null,concreteType:"Query",kind:"LinkedField",name:"query",plural:!1,selections:[{alias:"project",args:g,concreteType:null,kind:"LinkedField",name:"node",plural:!1,selections:[{kind:"InlineFragment",selections:[{args:h,kind:"FragmentSpread",name:"AnnotationSummaryValueFragment"}],type:"Project",abstractKey:null}],storageKey:null},{alias:null,args:f,concreteType:null,kind:"LinkedField",name:"node",plural:!1,selections:[{kind:"InlineFragment",selections:[{args:null,kind:"FragmentSpread",name:"AnnotationSummaryGroup"},{args:null,kind:"FragmentSpread",name:"TraceHeaderRootSpanAnnotationsFragment"},{args:[{kind:"Variable",name:"filterUserIds",variableName:"filterUserIds"}],kind:"FragmentSpread",name:"SpanAnnotationsEditor_spanAnnotations"},{args:null,kind:"FragmentSpread",name:"SpanAsideAnnotationList_span"},{args:null,kind:"FragmentSpread",name:"SpanFeedback_annotations"}],type:"Span",abstractKey:null}],storageKey:null}],storageKey:null}],storageKey:null}],type:"Mutation",abstractKey:null},kind:"Request",operation:{argumentDefinitions:[c,n,i,l,o,a,t,d,r],kind:"Operation",name:"SpanAnnotationsEditorEditAnnotationMutation",selections:[{alias:null,args:u,concreteType:"SpanAnnotationMutationPayload",kind:"LinkedField",name:"patchSpanAnnotations",plural:!1,selections:[{alias:null,args:null,concreteType:"Query",kind:"LinkedField",name:"query",plural:!1,selections:[{alias:"project",args:g,concreteType:null,kind:"LinkedField",name:"node",plural:!1,selections:[b,y,{kind:"InlineFragment",selections:[{alias:null,args:null,concreteType:"AnnotationConfigConnection",kind:"LinkedField",name:"annotationConfigs",plural:!1,selections:[{alias:null,args:null,concreteType:"AnnotationConfigEdge",kind:"LinkedField",name:"edges",plural:!0,selections:[{alias:null,args:null,concreteType:null,kind:"LinkedField",name:"node",plural:!1,selections:[b,k,{kind:"InlineFragment",selections:[v,y,L,E,D],type:"CategoricalAnnotationConfig",abstractKey:null},X],storageKey:null}],storageKey:null}],storageKey:null},{alias:null,args:h,concreteType:"AnnotationSummary",kind:"LinkedField",name:"spanAnnotationSummary",plural:!1,selections:[E,{alias:null,args:null,concreteType:"LabelFraction",kind:"LinkedField",name:"labelFractions",plural:!0,selections:[O,Y],storageKey:null},_],storageKey:null}],type:"Project",abstractKey:null}],storageKey:null},{alias:null,args:f,concreteType:null,kind:"LinkedField",name:"node",plural:!1,selections:[b,y,{kind:"InlineFragment",selections:[{alias:null,args:null,concreteType:"Project",kind:"LinkedField",name:"project",plural:!1,selections:[y,{alias:null,args:null,concreteType:"AnnotationConfigConnection",kind:"LinkedField",name:"annotationConfigs",plural:!1,selections:[{alias:null,args:null,concreteType:"AnnotationConfigEdge",kind:"LinkedField",name:"edges",plural:!0,selections:[{alias:null,args:null,concreteType:null,kind:"LinkedField",name:"node",plural:!1,selections:[b,k,{kind:"InlineFragment",selections:[y,E,L,D],type:"CategoricalAnnotationConfig",abstractKey:null},X],storageKey:null}],storageKey:null},{alias:"configs",args:null,concreteType:"AnnotationConfigEdge",kind:"LinkedField",name:"edges",plural:!0,selections:[{alias:"config",args:null,concreteType:null,kind:"LinkedField",name:"node",plural:!1,selections:[b,X,{kind:"InlineFragment",selections:[E],type:"AnnotationConfigBase",abstractKey:"__isAnnotationConfigBase"}],storageKey:null}],storageKey:null}],storageKey:null}],storageKey:null},{alias:null,args:null,concreteType:"SpanAnnotation",kind:"LinkedField",name:"spanAnnotations",plural:!0,selections:[y,E,O,F,A,H,{alias:null,args:null,concreteType:"User",kind:"LinkedField",name:"user",plural:!1,selections:[{alias:null,args:null,kind:"ScalarField",name:"username",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"profilePictureUrl",storageKey:null},y],storageKey:null},oe,{alias:null,args:null,kind:"ScalarField",name:"metadata",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"identifier",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"source",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"updatedAt",storageKey:null}],storageKey:null},{alias:null,args:null,concreteType:"AnnotationSummary",kind:"LinkedField",name:"spanAnnotationSummaries",plural:!0,selections:[{alias:null,args:null,concreteType:"LabelFraction",kind:"LinkedField",name:"labelFractions",plural:!0,selections:[Y,O],storageKey:null},_,E],storageKey:null},{alias:"filteredSpanAnnotations",args:[{fields:[{kind:"Literal",name:"exclude",value:{names:["note"]}},{fields:[{kind:"Variable",name:"userIds",variableName:"filterUserIds"}],kind:"ObjectValue",name:"include"}],kind:"ObjectValue",name:"filter"}],concreteType:"SpanAnnotation",kind:"LinkedField",name:"spanAnnotations",plural:!0,selections:[y,E,A,F,O,oe,H],storageKey:null}],type:"Span",abstractKey:null}],storageKey:null}],storageKey:null}],storageKey:null}]},params:{cacheID:"21f32f0823e2e9f883d1c332004c1559",id:null,metadata:{},name:"SpanAnnotationsEditorEditAnnotationMutation",operationKind:"mutation",text:`mutation SpanAnnotationsEditorEditAnnotationMutation(
  $spanId: ID!
  $annotationId: ID!
  $name: String!
  $label: String
  $score: Float
  $explanation: String
  $filterUserIds: [ID]
  $timeRange: TimeRange!
  $projectId: ID!
) {
  patchSpanAnnotations(input: [{annotationId: $annotationId, name: $name, label: $label, score: $score, explanation: $explanation, annotatorKind: HUMAN, source: APP}]) {
    query {
      project: node(id: $projectId) {
        __typename
        ... on Project {
          ...AnnotationSummaryValueFragment_20r1YH
        }
        id
      }
      node(id: $spanId) {
        __typename
        ... on Span {
          ...AnnotationSummaryGroup
          ...TraceHeaderRootSpanAnnotationsFragment
          ...SpanAnnotationsEditor_spanAnnotations_3lpqY
          ...SpanAsideAnnotationList_span
          ...SpanFeedback_annotations
        }
        id
      }
    }
  }
}

fragment AnnotationSummaryGroup on Span {
  project {
    id
    annotationConfigs {
      edges {
        node {
          __typename
          ... on AnnotationConfigBase {
            __isAnnotationConfigBase: __typename
            annotationType
          }
          ... on CategoricalAnnotationConfig {
            id
            name
            optimizationDirection
            values {
              label
              score
            }
          }
          ... on Node {
            __isNode: __typename
            id
          }
        }
      }
    }
  }
  spanAnnotations {
    id
    name
    label
    score
    annotatorKind
    createdAt
    user {
      username
      profilePictureUrl
      id
    }
  }
  spanAnnotationSummaries {
    labelFractions {
      fraction
      label
    }
    meanScore
    name
  }
}

fragment AnnotationSummaryValueFragment_20r1YH on Project {
  annotationConfigs {
    edges {
      node {
        __typename
        ... on AnnotationConfigBase {
          __isAnnotationConfigBase: __typename
          annotationType
        }
        ... on CategoricalAnnotationConfig {
          annotationType
          id
          optimizationDirection
          name
          values {
            label
            score
          }
        }
        ... on Node {
          __isNode: __typename
          id
        }
      }
    }
  }
  spanAnnotationSummary(annotationName: $name, timeRange: $timeRange) {
    name
    labelFractions {
      label
      fraction
    }
    meanScore
  }
  id
}

fragment SpanAnnotationsEditor_spanAnnotations_3lpqY on Span {
  id
  filteredSpanAnnotations: spanAnnotations(filter: {exclude: {names: ["note"]}, include: {userIds: $filterUserIds}}) {
    id
    name
    annotatorKind
    score
    label
    explanation
    createdAt
  }
}

fragment SpanAsideAnnotationList_span on Span {
  project {
    id
    annotationConfigs {
      configs: edges {
        config: node {
          __typename
          ... on Node {
            __isNode: __typename
            id
          }
          ... on AnnotationConfigBase {
            __isAnnotationConfigBase: __typename
            name
          }
        }
      }
    }
  }
  spanAnnotations {
    id
  }
  ...AnnotationSummaryGroup
}

fragment SpanFeedback_annotations on Span {
  id
  spanAnnotations {
    id
    name
    label
    score
    explanation
    metadata
    annotatorKind
    identifier
    source
    createdAt
    updatedAt
    user {
      id
      username
      profilePictureUrl
    }
  }
}

fragment TraceHeaderRootSpanAnnotationsFragment on Span {
  ...AnnotationSummaryGroup
}
`}}})();Nr.hash="2e32eb892ace0745b83b66da87e6e76e";const $r=(function(){var n={defaultValue:null,kind:"LocalArgument",name:"annotationIds"},a={defaultValue:null,kind:"LocalArgument",name:"filterUserIds"},t={defaultValue:null,kind:"LocalArgument",name:"projectId"},l={defaultValue:null,kind:"LocalArgument",name:"spanId"},i={defaultValue:null,kind:"LocalArgument",name:"timeRange"},r=[{fields:[{kind:"Variable",name:"annotationIds",variableName:"annotationIds"}],kind:"ObjectValue",name:"input"}],o=[{kind:"Variable",name:"id",variableName:"projectId"}],c=[{kind:"Variable",name:"id",variableName:"spanId"}],d={alias:null,args:null,kind:"ScalarField",name:"__typename",storageKey:null},u={alias:null,args:null,kind:"ScalarField",name:"id",storageKey:null},g={kind:"Variable",name:"timeRange",variableName:"timeRange"},h=[g],f=[{alias:null,args:null,kind:"ScalarField",name:"cost",storageKey:null}],b={alias:null,args:null,kind:"ScalarField",name:"name",storageKey:null},y={alias:null,args:null,kind:"ScalarField",name:"label",storageKey:null},v={alias:null,args:null,kind:"ScalarField",name:"score",storageKey:null},k={kind:"InlineFragment",selections:[u],type:"Node",abstractKey:"__isNode"},L={alias:null,args:null,kind:"ScalarField",name:"annotatorKind",storageKey:null},E={alias:null,args:null,kind:"ScalarField",name:"createdAt",storageKey:null},O={alias:null,args:null,kind:"ScalarField",name:"explanation",storageKey:null};return{fragment:{argumentDefinitions:[n,a,t,l,i],kind:"Fragment",metadata:null,name:"SpanAnnotationsEditorDeleteAnnotationMutation",selections:[{alias:null,args:r,concreteType:"SpanAnnotationMutationPayload",kind:"LinkedField",name:"deleteSpanAnnotations",plural:!1,selections:[{alias:null,args:null,concreteType:"Query",kind:"LinkedField",name:"query",plural:!1,selections:[{alias:"project",args:o,concreteType:null,kind:"LinkedField",name:"node",plural:!1,selections:[{kind:"InlineFragment",selections:[{args:null,kind:"FragmentSpread",name:"ProjectPageHeader_stats"}],type:"Project",abstractKey:null}],storageKey:null},{alias:null,args:c,concreteType:null,kind:"LinkedField",name:"node",plural:!1,selections:[{kind:"InlineFragment",selections:[{args:null,kind:"FragmentSpread",name:"AnnotationSummaryGroup"},{args:null,kind:"FragmentSpread",name:"TraceHeaderRootSpanAnnotationsFragment"},{args:[{kind:"Variable",name:"filterUserIds",variableName:"filterUserIds"}],kind:"FragmentSpread",name:"SpanAnnotationsEditor_spanAnnotations"},{args:null,kind:"FragmentSpread",name:"SpanAsideAnnotationList_span"},{args:null,kind:"FragmentSpread",name:"SpanFeedback_annotations"}],type:"Span",abstractKey:null}],storageKey:null}],storageKey:null}],storageKey:null}],type:"Mutation",abstractKey:null},kind:"Request",operation:{argumentDefinitions:[l,n,i,t,a],kind:"Operation",name:"SpanAnnotationsEditorDeleteAnnotationMutation",selections:[{alias:null,args:r,concreteType:"SpanAnnotationMutationPayload",kind:"LinkedField",name:"deleteSpanAnnotations",plural:!1,selections:[{alias:null,args:null,concreteType:"Query",kind:"LinkedField",name:"query",plural:!1,selections:[{alias:"project",args:o,concreteType:null,kind:"LinkedField",name:"node",plural:!1,selections:[d,u,{kind:"InlineFragment",selections:[{alias:null,args:h,kind:"ScalarField",name:"traceCount",storageKey:null},{alias:null,args:h,concreteType:"SpanCostSummary",kind:"LinkedField",name:"costSummary",plural:!1,selections:[{alias:null,args:null,concreteType:"CostBreakdown",kind:"LinkedField",name:"total",plural:!1,selections:f,storageKey:null},{alias:null,args:null,concreteType:"CostBreakdown",kind:"LinkedField",name:"prompt",plural:!1,selections:f,storageKey:null},{alias:null,args:null,concreteType:"CostBreakdown",kind:"LinkedField",name:"completion",plural:!1,selections:f,storageKey:null}],storageKey:null},{alias:"latencyMsP50",args:[{kind:"Literal",name:"probability",value:.5},g],kind:"ScalarField",name:"latencyMsQuantile",storageKey:null},{alias:"latencyMsP99",args:[{kind:"Literal",name:"probability",value:.99},g],kind:"ScalarField",name:"latencyMsQuantile",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"spanAnnotationNames",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"documentEvaluationNames",storageKey:null}],type:"Project",abstractKey:null}],storageKey:null},{alias:null,args:c,concreteType:null,kind:"LinkedField",name:"node",plural:!1,selections:[d,u,{kind:"InlineFragment",selections:[{alias:null,args:null,concreteType:"Project",kind:"LinkedField",name:"project",plural:!1,selections:[u,{alias:null,args:null,concreteType:"AnnotationConfigConnection",kind:"LinkedField",name:"annotationConfigs",plural:!1,selections:[{alias:null,args:null,concreteType:"AnnotationConfigEdge",kind:"LinkedField",name:"edges",plural:!0,selections:[{alias:null,args:null,concreteType:null,kind:"LinkedField",name:"node",plural:!1,selections:[d,{kind:"InlineFragment",selections:[{alias:null,args:null,kind:"ScalarField",name:"annotationType",storageKey:null}],type:"AnnotationConfigBase",abstractKey:"__isAnnotationConfigBase"},{kind:"InlineFragment",selections:[u,b,{alias:null,args:null,kind:"ScalarField",name:"optimizationDirection",storageKey:null},{alias:null,args:null,concreteType:"CategoricalAnnotationValue",kind:"LinkedField",name:"values",plural:!0,selections:[y,v],storageKey:null}],type:"CategoricalAnnotationConfig",abstractKey:null},k],storageKey:null}],storageKey:null},{alias:"configs",args:null,concreteType:"AnnotationConfigEdge",kind:"LinkedField",name:"edges",plural:!0,selections:[{alias:"config",args:null,concreteType:null,kind:"LinkedField",name:"node",plural:!1,selections:[d,k,{kind:"InlineFragment",selections:[b],type:"AnnotationConfigBase",abstractKey:"__isAnnotationConfigBase"}],storageKey:null}],storageKey:null}],storageKey:null}],storageKey:null},{alias:null,args:null,concreteType:"SpanAnnotation",kind:"LinkedField",name:"spanAnnotations",plural:!0,selections:[u,b,y,v,L,E,{alias:null,args:null,concreteType:"User",kind:"LinkedField",name:"user",plural:!1,selections:[{alias:null,args:null,kind:"ScalarField",name:"username",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"profilePictureUrl",storageKey:null},u],storageKey:null},O,{alias:null,args:null,kind:"ScalarField",name:"metadata",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"identifier",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"source",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"updatedAt",storageKey:null}],storageKey:null},{alias:null,args:null,concreteType:"AnnotationSummary",kind:"LinkedField",name:"spanAnnotationSummaries",plural:!0,selections:[{alias:null,args:null,concreteType:"LabelFraction",kind:"LinkedField",name:"labelFractions",plural:!0,selections:[{alias:null,args:null,kind:"ScalarField",name:"fraction",storageKey:null},y],storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"meanScore",storageKey:null},b],storageKey:null},{alias:"filteredSpanAnnotations",args:[{fields:[{kind:"Literal",name:"exclude",value:{names:["note"]}},{fields:[{kind:"Variable",name:"userIds",variableName:"filterUserIds"}],kind:"ObjectValue",name:"include"}],kind:"ObjectValue",name:"filter"}],concreteType:"SpanAnnotation",kind:"LinkedField",name:"spanAnnotations",plural:!0,selections:[u,b,L,v,y,O,E],storageKey:null}],type:"Span",abstractKey:null}],storageKey:null}],storageKey:null}],storageKey:null}]},params:{cacheID:"dee76f16722e918832123373a1155240",id:null,metadata:{},name:"SpanAnnotationsEditorDeleteAnnotationMutation",operationKind:"mutation",text:`mutation SpanAnnotationsEditorDeleteAnnotationMutation(
  $spanId: ID!
  $annotationIds: [ID!]!
  $timeRange: TimeRange!
  $projectId: ID!
  $filterUserIds: [ID]
) {
  deleteSpanAnnotations(input: {annotationIds: $annotationIds}) {
    query {
      project: node(id: $projectId) {
        __typename
        ... on Project {
          ...ProjectPageHeader_stats
        }
        id
      }
      node(id: $spanId) {
        __typename
        ... on Span {
          ...AnnotationSummaryGroup
          ...TraceHeaderRootSpanAnnotationsFragment
          ...SpanAnnotationsEditor_spanAnnotations_3lpqY
          ...SpanAsideAnnotationList_span
          ...SpanFeedback_annotations
        }
        id
      }
    }
  }
}

fragment AnnotationSummaryGroup on Span {
  project {
    id
    annotationConfigs {
      edges {
        node {
          __typename
          ... on AnnotationConfigBase {
            __isAnnotationConfigBase: __typename
            annotationType
          }
          ... on CategoricalAnnotationConfig {
            id
            name
            optimizationDirection
            values {
              label
              score
            }
          }
          ... on Node {
            __isNode: __typename
            id
          }
        }
      }
    }
  }
  spanAnnotations {
    id
    name
    label
    score
    annotatorKind
    createdAt
    user {
      username
      profilePictureUrl
      id
    }
  }
  spanAnnotationSummaries {
    labelFractions {
      fraction
      label
    }
    meanScore
    name
  }
}

fragment ProjectPageHeader_stats on Project {
  traceCount(timeRange: $timeRange)
  costSummary(timeRange: $timeRange) {
    total {
      cost
    }
    prompt {
      cost
    }
    completion {
      cost
    }
  }
  latencyMsP50: latencyMsQuantile(probability: 0.5, timeRange: $timeRange)
  latencyMsP99: latencyMsQuantile(probability: 0.99, timeRange: $timeRange)
  spanAnnotationNames
  documentEvaluationNames
  id
}

fragment SpanAnnotationsEditor_spanAnnotations_3lpqY on Span {
  id
  filteredSpanAnnotations: spanAnnotations(filter: {exclude: {names: ["note"]}, include: {userIds: $filterUserIds}}) {
    id
    name
    annotatorKind
    score
    label
    explanation
    createdAt
  }
}

fragment SpanAsideAnnotationList_span on Span {
  project {
    id
    annotationConfigs {
      configs: edges {
        config: node {
          __typename
          ... on Node {
            __isNode: __typename
            id
          }
          ... on AnnotationConfigBase {
            __isAnnotationConfigBase: __typename
            name
          }
        }
      }
    }
  }
  spanAnnotations {
    id
  }
  ...AnnotationSummaryGroup
}

fragment SpanFeedback_annotations on Span {
  id
  spanAnnotations {
    id
    name
    label
    score
    explanation
    metadata
    annotatorKind
    identifier
    source
    createdAt
    updatedAt
    user {
      id
      username
      profilePictureUrl
    }
  }
}

fragment TraceHeaderRootSpanAnnotationsFragment on Span {
  ...AnnotationSummaryGroup
}
`}}})();$r.hash="91b4801afce840fdac7250d2c84eff21";const Br=(function(){var n={alias:null,args:null,kind:"ScalarField",name:"id",storageKey:null};return{argumentDefinitions:[{defaultValue:null,kind:"LocalArgument",name:"filterUserIds"}],kind:"Fragment",metadata:null,name:"SpanAnnotationsEditor_spanAnnotations",selections:[n,{alias:"filteredSpanAnnotations",args:[{fields:[{kind:"Literal",name:"exclude",value:{names:["note"]}},{fields:[{kind:"Variable",name:"userIds",variableName:"filterUserIds"}],kind:"ObjectValue",name:"include"}],kind:"ObjectValue",name:"filter"}],concreteType:"SpanAnnotation",kind:"LinkedField",name:"spanAnnotations",plural:!0,selections:[n,{alias:null,args:null,kind:"ScalarField",name:"name",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"annotatorKind",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"score",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"label",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"explanation",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"createdAt",storageKey:null}],storageKey:null}],type:"Span",abstractKey:null}})();Br.hash="e1133bf8aec8eadedaa01c3c4170bfe9";const Hr=(function(){var n={defaultValue:null,kind:"LocalArgument",name:"filterUserIds"},a={defaultValue:null,kind:"LocalArgument",name:"projectId"},t={defaultValue:null,kind:"LocalArgument",name:"spanId"},l=[{kind:"Variable",name:"id",variableName:"projectId"}],i={alias:null,args:null,kind:"ScalarField",name:"id",storageKey:null},r={alias:null,args:null,kind:"ScalarField",name:"__typename",storageKey:null},o={alias:null,args:null,kind:"ScalarField",name:"name",storageKey:null},c={alias:null,args:null,kind:"ScalarField",name:"optimizationDirection",storageKey:null},d={alias:null,args:null,kind:"ScalarField",name:"label",storageKey:null},u={alias:null,args:null,kind:"ScalarField",name:"score",storageKey:null},g={kind:"InlineFragment",selections:[{alias:null,args:null,concreteType:"AnnotationConfigConnection",kind:"LinkedField",name:"annotationConfigs",plural:!1,selections:[{alias:"configs",args:null,concreteType:"AnnotationConfigEdge",kind:"LinkedField",name:"edges",plural:!0,selections:[{alias:"config",args:null,concreteType:null,kind:"LinkedField",name:"node",plural:!1,selections:[r,{kind:"InlineFragment",selections:[i],type:"Node",abstractKey:"__isNode"},{kind:"InlineFragment",selections:[o,{alias:null,args:null,kind:"ScalarField",name:"annotationType",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"description",storageKey:null}],type:"AnnotationConfigBase",abstractKey:"__isAnnotationConfigBase"},{kind:"InlineFragment",selections:[c,{alias:null,args:null,concreteType:"CategoricalAnnotationValue",kind:"LinkedField",name:"values",plural:!0,selections:[d,u],storageKey:null}],type:"CategoricalAnnotationConfig",abstractKey:null},{kind:"InlineFragment",selections:[{alias:null,args:null,kind:"ScalarField",name:"lowerBound",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"upperBound",storageKey:null},c],type:"ContinuousAnnotationConfig",abstractKey:null},{kind:"InlineFragment",selections:[o],type:"FreeformAnnotationConfig",abstractKey:null}],storageKey:null}],storageKey:null}],storageKey:null}],type:"Project",abstractKey:null},h=[{kind:"Variable",name:"id",variableName:"spanId"}];return{fragment:{argumentDefinitions:[n,a,t],kind:"Fragment",metadata:null,name:"SpanAnnotationsEditorSpanAnnotationsListQuery",selections:[{alias:"project",args:l,concreteType:null,kind:"LinkedField",name:"node",plural:!1,selections:[i,g],storageKey:null},{alias:"span",args:h,concreteType:null,kind:"LinkedField",name:"node",plural:!1,selections:[i,{kind:"InlineFragment",selections:[{args:[{kind:"Variable",name:"filterUserIds",variableName:"filterUserIds"}],kind:"FragmentSpread",name:"SpanAnnotationsEditor_spanAnnotations"}],type:"Span",abstractKey:null}],storageKey:null}],type:"Query",abstractKey:null},kind:"Request",operation:{argumentDefinitions:[a,t,n],kind:"Operation",name:"SpanAnnotationsEditorSpanAnnotationsListQuery",selections:[{alias:"project",args:l,concreteType:null,kind:"LinkedField",name:"node",plural:!1,selections:[r,i,g],storageKey:null},{alias:"span",args:h,concreteType:null,kind:"LinkedField",name:"node",plural:!1,selections:[r,i,{kind:"InlineFragment",selections:[{alias:"filteredSpanAnnotations",args:[{fields:[{kind:"Literal",name:"exclude",value:{names:["note"]}},{fields:[{kind:"Variable",name:"userIds",variableName:"filterUserIds"}],kind:"ObjectValue",name:"include"}],kind:"ObjectValue",name:"filter"}],concreteType:"SpanAnnotation",kind:"LinkedField",name:"spanAnnotations",plural:!0,selections:[i,o,{alias:null,args:null,kind:"ScalarField",name:"annotatorKind",storageKey:null},u,d,{alias:null,args:null,kind:"ScalarField",name:"explanation",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"createdAt",storageKey:null}],storageKey:null}],type:"Span",abstractKey:null}],storageKey:null}]},params:{cacheID:"c19b9cff9a85b67ea4db4f43b28d1fd3",id:null,metadata:{},name:"SpanAnnotationsEditorSpanAnnotationsListQuery",operationKind:"query",text:`query SpanAnnotationsEditorSpanAnnotationsListQuery(
  $projectId: ID!
  $spanId: ID!
  $filterUserIds: [ID]
) {
  project: node(id: $projectId) {
    __typename
    id
    ... on Project {
      annotationConfigs {
        configs: edges {
          config: node {
            __typename
            ... on Node {
              __isNode: __typename
              id
            }
            ... on AnnotationConfigBase {
              __isAnnotationConfigBase: __typename
              name
              annotationType
              description
            }
            ... on CategoricalAnnotationConfig {
              optimizationDirection
              values {
                label
                score
              }
            }
            ... on ContinuousAnnotationConfig {
              lowerBound
              upperBound
              optimizationDirection
            }
            ... on FreeformAnnotationConfig {
              name
            }
          }
        }
      }
    }
  }
  span: node(id: $spanId) {
    __typename
    id
    ... on Span {
      ...SpanAnnotationsEditor_spanAnnotations_3lpqY
    }
  }
}

fragment SpanAnnotationsEditor_spanAnnotations_3lpqY on Span {
  id
  filteredSpanAnnotations: spanAnnotations(filter: {exclude: {names: ["note"]}, include: {userIds: $filterUserIds}}) {
    id
    name
    annotatorKind
    score
    label
    explanation
    createdAt
  }
}
`}}})();Hr.hash="ab94a265160b38df3c4310317a5ca86b";const jr=(function(){var n={defaultValue:null,kind:"LocalArgument",name:"annotationConfigId"},a={defaultValue:null,kind:"LocalArgument",name:"filterUserIds"},t={defaultValue:null,kind:"LocalArgument",name:"projectId"},l={defaultValue:null,kind:"LocalArgument",name:"spanId"},i=[{fields:[{kind:"Variable",name:"annotationConfigId",variableName:"annotationConfigId"},{kind:"Variable",name:"projectId",variableName:"projectId"}],kind:"ObjectValue",name:"input"}],r=[{kind:"Variable",name:"id",variableName:"projectId"}],o={alias:null,args:null,kind:"ScalarField",name:"id",storageKey:null},c=[{kind:"Variable",name:"id",variableName:"spanId"}],d={alias:null,args:null,kind:"ScalarField",name:"__typename",storageKey:null},u={alias:null,args:null,kind:"ScalarField",name:"name",storageKey:null},g={alias:null,args:null,kind:"ScalarField",name:"label",storageKey:null},h={alias:null,args:null,kind:"ScalarField",name:"score",storageKey:null};return{fragment:{argumentDefinitions:[n,a,t,l],kind:"Fragment",metadata:null,name:"AnnotationConfigListRemoveAnnotationConfigFromProjectMutation",selections:[{alias:null,args:i,concreteType:"RemoveAnnotationConfigFromProjectPayload",kind:"LinkedField",name:"removeAnnotationConfigFromProject",plural:!1,selections:[{alias:null,args:null,concreteType:"Query",kind:"LinkedField",name:"query",plural:!1,selections:[{alias:"projectNode",args:r,concreteType:null,kind:"LinkedField",name:"node",plural:!1,selections:[{kind:"InlineFragment",selections:[o,{args:null,kind:"FragmentSpread",name:"AnnotationConfigListProjectAnnotationConfigFragment"}],type:"Project",abstractKey:null}],storageKey:null},{alias:null,args:c,concreteType:null,kind:"LinkedField",name:"node",plural:!1,selections:[{kind:"InlineFragment",selections:[o,{args:[{kind:"Variable",name:"filterUserIds",variableName:"filterUserIds"}],kind:"FragmentSpread",name:"SpanAnnotationsEditor_spanAnnotations"}],type:"Span",abstractKey:null}],storageKey:null}],storageKey:null}],storageKey:null}],type:"Mutation",abstractKey:null},kind:"Request",operation:{argumentDefinitions:[t,n,l,a],kind:"Operation",name:"AnnotationConfigListRemoveAnnotationConfigFromProjectMutation",selections:[{alias:null,args:i,concreteType:"RemoveAnnotationConfigFromProjectPayload",kind:"LinkedField",name:"removeAnnotationConfigFromProject",plural:!1,selections:[{alias:null,args:null,concreteType:"Query",kind:"LinkedField",name:"query",plural:!1,selections:[{alias:"projectNode",args:r,concreteType:null,kind:"LinkedField",name:"node",plural:!1,selections:[d,o,{kind:"InlineFragment",selections:[{alias:null,args:null,concreteType:"AnnotationConfigConnection",kind:"LinkedField",name:"annotationConfigs",plural:!1,selections:[{alias:null,args:null,concreteType:"AnnotationConfigEdge",kind:"LinkedField",name:"edges",plural:!0,selections:[{alias:null,args:null,concreteType:null,kind:"LinkedField",name:"node",plural:!1,selections:[d,{kind:"InlineFragment",selections:[o],type:"Node",abstractKey:"__isNode"},{kind:"InlineFragment",selections:[u,{alias:null,args:null,kind:"ScalarField",name:"annotationType",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"description",storageKey:null}],type:"AnnotationConfigBase",abstractKey:"__isAnnotationConfigBase"},{kind:"InlineFragment",selections:[{alias:null,args:null,concreteType:"CategoricalAnnotationValue",kind:"LinkedField",name:"values",plural:!0,selections:[g,h],storageKey:null}],type:"CategoricalAnnotationConfig",abstractKey:null},{kind:"InlineFragment",selections:[{alias:null,args:null,kind:"ScalarField",name:"lowerBound",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"upperBound",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"optimizationDirection",storageKey:null}],type:"ContinuousAnnotationConfig",abstractKey:null},{kind:"InlineFragment",selections:[u],type:"FreeformAnnotationConfig",abstractKey:null}],storageKey:null}],storageKey:null}],storageKey:null}],type:"Project",abstractKey:null}],storageKey:null},{alias:null,args:c,concreteType:null,kind:"LinkedField",name:"node",plural:!1,selections:[d,o,{kind:"InlineFragment",selections:[{alias:"filteredSpanAnnotations",args:[{fields:[{kind:"Literal",name:"exclude",value:{names:["note"]}},{fields:[{kind:"Variable",name:"userIds",variableName:"filterUserIds"}],kind:"ObjectValue",name:"include"}],kind:"ObjectValue",name:"filter"}],concreteType:"SpanAnnotation",kind:"LinkedField",name:"spanAnnotations",plural:!0,selections:[o,u,{alias:null,args:null,kind:"ScalarField",name:"annotatorKind",storageKey:null},h,g,{alias:null,args:null,kind:"ScalarField",name:"explanation",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"createdAt",storageKey:null}],storageKey:null}],type:"Span",abstractKey:null}],storageKey:null}],storageKey:null}],storageKey:null}]},params:{cacheID:"ac0ee63febc8956acc1d1b43505591c3",id:null,metadata:{},name:"AnnotationConfigListRemoveAnnotationConfigFromProjectMutation",operationKind:"mutation",text:`mutation AnnotationConfigListRemoveAnnotationConfigFromProjectMutation(
  $projectId: ID!
  $annotationConfigId: ID!
  $spanId: ID!
  $filterUserIds: [ID!]
) {
  removeAnnotationConfigFromProject(input: {projectId: $projectId, annotationConfigId: $annotationConfigId}) {
    query {
      projectNode: node(id: $projectId) {
        __typename
        ... on Project {
          id
          ...AnnotationConfigListProjectAnnotationConfigFragment
        }
        id
      }
      node(id: $spanId) {
        __typename
        ... on Span {
          id
          ...SpanAnnotationsEditor_spanAnnotations_3lpqY
        }
        id
      }
    }
  }
}

fragment AnnotationConfigListProjectAnnotationConfigFragment on Project {
  annotationConfigs {
    edges {
      node {
        __typename
        ... on Node {
          __isNode: __typename
          id
        }
        ... on AnnotationConfigBase {
          __isAnnotationConfigBase: __typename
          name
          annotationType
          description
        }
        ... on CategoricalAnnotationConfig {
          values {
            label
            score
          }
        }
        ... on ContinuousAnnotationConfig {
          lowerBound
          upperBound
          optimizationDirection
        }
        ... on FreeformAnnotationConfig {
          name
        }
      }
    }
  }
}

fragment SpanAnnotationsEditor_spanAnnotations_3lpqY on Span {
  id
  filteredSpanAnnotations: spanAnnotations(filter: {exclude: {names: ["note"]}, include: {userIds: $filterUserIds}}) {
    id
    name
    annotatorKind
    score
    label
    explanation
    createdAt
  }
}
`}}})();jr.hash="95e97ce45fd2d56bb67fbdb8fd683092";const Zr=(function(){var n={defaultValue:null,kind:"LocalArgument",name:"annotationConfigId"},a={defaultValue:null,kind:"LocalArgument",name:"filterUserIds"},t={defaultValue:null,kind:"LocalArgument",name:"projectId"},l={defaultValue:null,kind:"LocalArgument",name:"spanId"},i=[{fields:[{kind:"Variable",name:"annotationConfigId",variableName:"annotationConfigId"},{kind:"Variable",name:"projectId",variableName:"projectId"}],kind:"ObjectValue",name:"input"}],r=[{kind:"Variable",name:"id",variableName:"projectId"}],o={alias:null,args:null,kind:"ScalarField",name:"id",storageKey:null},c=[{kind:"Variable",name:"id",variableName:"spanId"}],d={alias:null,args:null,kind:"ScalarField",name:"__typename",storageKey:null},u={alias:null,args:null,kind:"ScalarField",name:"name",storageKey:null},g={alias:null,args:null,kind:"ScalarField",name:"label",storageKey:null},h={alias:null,args:null,kind:"ScalarField",name:"score",storageKey:null};return{fragment:{argumentDefinitions:[n,a,t,l],kind:"Fragment",metadata:null,name:"AnnotationConfigListAssociateAnnotationConfigWithProjectMutation",selections:[{alias:null,args:i,concreteType:"AddAnnotationConfigToProjectPayload",kind:"LinkedField",name:"addAnnotationConfigToProject",plural:!1,selections:[{alias:null,args:null,concreteType:"Query",kind:"LinkedField",name:"query",plural:!1,selections:[{alias:"projectNode",args:r,concreteType:null,kind:"LinkedField",name:"node",plural:!1,selections:[{kind:"InlineFragment",selections:[o,{args:null,kind:"FragmentSpread",name:"AnnotationConfigListProjectAnnotationConfigFragment"}],type:"Project",abstractKey:null}],storageKey:null},{alias:null,args:c,concreteType:null,kind:"LinkedField",name:"node",plural:!1,selections:[{kind:"InlineFragment",selections:[o,{args:[{kind:"Variable",name:"filterUserIds",variableName:"filterUserIds"}],kind:"FragmentSpread",name:"SpanAnnotationsEditor_spanAnnotations"}],type:"Span",abstractKey:null}],storageKey:null}],storageKey:null}],storageKey:null}],type:"Mutation",abstractKey:null},kind:"Request",operation:{argumentDefinitions:[t,n,l,a],kind:"Operation",name:"AnnotationConfigListAssociateAnnotationConfigWithProjectMutation",selections:[{alias:null,args:i,concreteType:"AddAnnotationConfigToProjectPayload",kind:"LinkedField",name:"addAnnotationConfigToProject",plural:!1,selections:[{alias:null,args:null,concreteType:"Query",kind:"LinkedField",name:"query",plural:!1,selections:[{alias:"projectNode",args:r,concreteType:null,kind:"LinkedField",name:"node",plural:!1,selections:[d,o,{kind:"InlineFragment",selections:[{alias:null,args:null,concreteType:"AnnotationConfigConnection",kind:"LinkedField",name:"annotationConfigs",plural:!1,selections:[{alias:null,args:null,concreteType:"AnnotationConfigEdge",kind:"LinkedField",name:"edges",plural:!0,selections:[{alias:null,args:null,concreteType:null,kind:"LinkedField",name:"node",plural:!1,selections:[d,{kind:"InlineFragment",selections:[o],type:"Node",abstractKey:"__isNode"},{kind:"InlineFragment",selections:[u,{alias:null,args:null,kind:"ScalarField",name:"annotationType",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"description",storageKey:null}],type:"AnnotationConfigBase",abstractKey:"__isAnnotationConfigBase"},{kind:"InlineFragment",selections:[{alias:null,args:null,concreteType:"CategoricalAnnotationValue",kind:"LinkedField",name:"values",plural:!0,selections:[g,h],storageKey:null}],type:"CategoricalAnnotationConfig",abstractKey:null},{kind:"InlineFragment",selections:[{alias:null,args:null,kind:"ScalarField",name:"lowerBound",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"upperBound",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"optimizationDirection",storageKey:null}],type:"ContinuousAnnotationConfig",abstractKey:null},{kind:"InlineFragment",selections:[u],type:"FreeformAnnotationConfig",abstractKey:null}],storageKey:null}],storageKey:null}],storageKey:null}],type:"Project",abstractKey:null}],storageKey:null},{alias:null,args:c,concreteType:null,kind:"LinkedField",name:"node",plural:!1,selections:[d,o,{kind:"InlineFragment",selections:[{alias:"filteredSpanAnnotations",args:[{fields:[{kind:"Literal",name:"exclude",value:{names:["note"]}},{fields:[{kind:"Variable",name:"userIds",variableName:"filterUserIds"}],kind:"ObjectValue",name:"include"}],kind:"ObjectValue",name:"filter"}],concreteType:"SpanAnnotation",kind:"LinkedField",name:"spanAnnotations",plural:!0,selections:[o,u,{alias:null,args:null,kind:"ScalarField",name:"annotatorKind",storageKey:null},h,g,{alias:null,args:null,kind:"ScalarField",name:"explanation",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"createdAt",storageKey:null}],storageKey:null}],type:"Span",abstractKey:null}],storageKey:null}],storageKey:null}],storageKey:null}]},params:{cacheID:"d50c07c47d622752dd477d5d58dcab08",id:null,metadata:{},name:"AnnotationConfigListAssociateAnnotationConfigWithProjectMutation",operationKind:"mutation",text:`mutation AnnotationConfigListAssociateAnnotationConfigWithProjectMutation(
  $projectId: ID!
  $annotationConfigId: ID!
  $spanId: ID!
  $filterUserIds: [ID!]
) {
  addAnnotationConfigToProject(input: {projectId: $projectId, annotationConfigId: $annotationConfigId}) {
    query {
      projectNode: node(id: $projectId) {
        __typename
        ... on Project {
          id
          ...AnnotationConfigListProjectAnnotationConfigFragment
        }
        id
      }
      node(id: $spanId) {
        __typename
        ... on Span {
          id
          ...SpanAnnotationsEditor_spanAnnotations_3lpqY
        }
        id
      }
    }
  }
}

fragment AnnotationConfigListProjectAnnotationConfigFragment on Project {
  annotationConfigs {
    edges {
      node {
        __typename
        ... on Node {
          __isNode: __typename
          id
        }
        ... on AnnotationConfigBase {
          __isAnnotationConfigBase: __typename
          name
          annotationType
          description
        }
        ... on CategoricalAnnotationConfig {
          values {
            label
            score
          }
        }
        ... on ContinuousAnnotationConfig {
          lowerBound
          upperBound
          optimizationDirection
        }
        ... on FreeformAnnotationConfig {
          name
        }
      }
    }
  }
}

fragment SpanAnnotationsEditor_spanAnnotations_3lpqY on Span {
  id
  filteredSpanAnnotations: spanAnnotations(filter: {exclude: {names: ["note"]}, include: {userIds: $filterUserIds}}) {
    id
    name
    annotatorKind
    score
    label
    explanation
    createdAt
  }
}
`}}})();Zr.hash="c0bef9fb6b65e0bb572ed9c7d42a0905";const Ur=(function(){var n={alias:null,args:null,kind:"ScalarField",name:"name",storageKey:null};return{argumentDefinitions:[],kind:"Fragment",metadata:null,name:"AnnotationConfigListProjectAnnotationConfigFragment",selections:[{alias:null,args:null,concreteType:"AnnotationConfigConnection",kind:"LinkedField",name:"annotationConfigs",plural:!1,selections:[{alias:null,args:null,concreteType:"AnnotationConfigEdge",kind:"LinkedField",name:"edges",plural:!0,selections:[{alias:null,args:null,concreteType:null,kind:"LinkedField",name:"node",plural:!1,selections:[{kind:"InlineFragment",selections:[{alias:null,args:null,kind:"ScalarField",name:"id",storageKey:null}],type:"Node",abstractKey:"__isNode"},{kind:"InlineFragment",selections:[n,{alias:null,args:null,kind:"ScalarField",name:"annotationType",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"description",storageKey:null}],type:"AnnotationConfigBase",abstractKey:"__isAnnotationConfigBase"},{kind:"InlineFragment",selections:[{alias:null,args:null,concreteType:"CategoricalAnnotationValue",kind:"LinkedField",name:"values",plural:!0,selections:[{alias:null,args:null,kind:"ScalarField",name:"label",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"score",storageKey:null}],storageKey:null}],type:"CategoricalAnnotationConfig",abstractKey:null},{kind:"InlineFragment",selections:[{alias:null,args:null,kind:"ScalarField",name:"lowerBound",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"upperBound",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"optimizationDirection",storageKey:null}],type:"ContinuousAnnotationConfig",abstractKey:null},{kind:"InlineFragment",selections:[n],type:"FreeformAnnotationConfig",abstractKey:null}],storageKey:null}],storageKey:null}],storageKey:null}],type:"Project",abstractKey:null}})();Ur.hash="7bed597e9a0dc874ed67506a8a4f870c";const Gr=(function(){var n=[{defaultValue:null,kind:"LocalArgument",name:"projectId"}],a=[{kind:"Variable",name:"id",variableName:"projectId"}],t={alias:null,args:null,kind:"ScalarField",name:"id",storageKey:null},l={kind:"InlineFragment",selections:[t],type:"Node",abstractKey:"__isNode"},i={alias:null,args:null,kind:"ScalarField",name:"name",storageKey:null},r={alias:null,args:null,kind:"ScalarField",name:"description",storageKey:null},o={alias:null,args:null,kind:"ScalarField",name:"annotationType",storageKey:null},c={kind:"InlineFragment",selections:[i,r,o],type:"AnnotationConfigBase",abstractKey:"__isAnnotationConfigBase"},d={kind:"InlineFragment",selections:[{alias:null,args:null,concreteType:"CategoricalAnnotationValue",kind:"LinkedField",name:"values",plural:!0,selections:[{alias:null,args:null,kind:"ScalarField",name:"label",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"score",storageKey:null}],storageKey:null}],type:"CategoricalAnnotationConfig",abstractKey:null},u={alias:null,args:null,kind:"ScalarField",name:"lowerBound",storageKey:null},g={alias:null,args:null,kind:"ScalarField",name:"upperBound",storageKey:null},h={kind:"InlineFragment",selections:[u,g],type:"ContinuousAnnotationConfig",abstractKey:null},f={alias:null,args:null,kind:"ScalarField",name:"__typename",storageKey:null};return{fragment:{argumentDefinitions:n,kind:"Fragment",metadata:null,name:"AnnotationConfigListQuery",selections:[{alias:"project",args:a,concreteType:null,kind:"LinkedField",name:"node",plural:!1,selections:[{kind:"InlineFragment",selections:[{args:null,kind:"FragmentSpread",name:"AnnotationConfigListProjectAnnotationConfigFragment"}],type:"Project",abstractKey:null}],storageKey:null},{alias:"allAnnotationConfigs",args:null,concreteType:"AnnotationConfigConnection",kind:"LinkedField",name:"annotationConfigs",plural:!1,selections:[{alias:null,args:null,concreteType:"AnnotationConfigEdge",kind:"LinkedField",name:"edges",plural:!0,selections:[{alias:null,args:null,concreteType:null,kind:"LinkedField",name:"node",plural:!1,selections:[l,c,d,h],storageKey:null}],storageKey:null}],storageKey:null}],type:"Query",abstractKey:null},kind:"Request",operation:{argumentDefinitions:n,kind:"Operation",name:"AnnotationConfigListQuery",selections:[{alias:"project",args:a,concreteType:null,kind:"LinkedField",name:"node",plural:!1,selections:[f,{kind:"InlineFragment",selections:[{alias:null,args:null,concreteType:"AnnotationConfigConnection",kind:"LinkedField",name:"annotationConfigs",plural:!1,selections:[{alias:null,args:null,concreteType:"AnnotationConfigEdge",kind:"LinkedField",name:"edges",plural:!0,selections:[{alias:null,args:null,concreteType:null,kind:"LinkedField",name:"node",plural:!1,selections:[f,l,{kind:"InlineFragment",selections:[i,o,r],type:"AnnotationConfigBase",abstractKey:"__isAnnotationConfigBase"},d,{kind:"InlineFragment",selections:[u,g,{alias:null,args:null,kind:"ScalarField",name:"optimizationDirection",storageKey:null}],type:"ContinuousAnnotationConfig",abstractKey:null},{kind:"InlineFragment",selections:[i],type:"FreeformAnnotationConfig",abstractKey:null}],storageKey:null}],storageKey:null}],storageKey:null}],type:"Project",abstractKey:null},t],storageKey:null},{alias:"allAnnotationConfigs",args:null,concreteType:"AnnotationConfigConnection",kind:"LinkedField",name:"annotationConfigs",plural:!1,selections:[{alias:null,args:null,concreteType:"AnnotationConfigEdge",kind:"LinkedField",name:"edges",plural:!0,selections:[{alias:null,args:null,concreteType:null,kind:"LinkedField",name:"node",plural:!1,selections:[f,l,c,d,h],storageKey:null}],storageKey:null}],storageKey:null}]},params:{cacheID:"1a712d6939eff6b3fc74c42fdf542bda",id:null,metadata:{},name:"AnnotationConfigListQuery",operationKind:"query",text:`query AnnotationConfigListQuery(
  $projectId: ID!
) {
  project: node(id: $projectId) {
    __typename
    ... on Project {
      ...AnnotationConfigListProjectAnnotationConfigFragment
    }
    id
  }
  allAnnotationConfigs: annotationConfigs {
    edges {
      node {
        __typename
        ... on Node {
          __isNode: __typename
          id
        }
        ... on AnnotationConfigBase {
          __isAnnotationConfigBase: __typename
          name
          description
          annotationType
        }
        ... on CategoricalAnnotationConfig {
          values {
            label
            score
          }
        }
        ... on ContinuousAnnotationConfig {
          lowerBound
          upperBound
        }
      }
    }
  }
}

fragment AnnotationConfigListProjectAnnotationConfigFragment on Project {
  annotationConfigs {
    edges {
      node {
        __typename
        ... on Node {
          __isNode: __typename
          id
        }
        ... on AnnotationConfigBase {
          __isAnnotationConfigBase: __typename
          name
          annotationType
          description
        }
        ... on CategoricalAnnotationConfig {
          values {
            label
            score
          }
        }
        ... on ContinuousAnnotationConfig {
          lowerBound
          upperBound
          optimizationDirection
        }
        ... on FreeformAnnotationConfig {
          name
        }
      }
    }
  }
}
`}}})();Gr.hash="17e291625e2df97c80e95916c0df269d";const Q4=m`
  padding: 0 var(--ac-global-dimension-size-100);
  max-height: 300px;
  min-width: 320px;
  min-height: 20px;
  overflow-y: auto;
  scrollbar-gutter: stable;
  .react-aria-ListBoxItem {
    padding: 0 var(--ac-global-dimension-size-100);

    label {
      border-radius: var(--ac-global-rounding-small);
      padding: var(--ac-global-dimension-size-50) 0;
      width: 100%;
      &:hover {
        background-color: var(--ac-global-color-grey-300);
      }
    }
  }
`,W4=m`
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  gap: var(--ac-global-dimension-size-100);
`,q4={CATEGORICAL:"Categorical",CONTINUOUS:"Continuous",FREEFORM:"Freeform"};function X4(n){var O;const a=ti(),{projectId:t,spanId:l}=n,[i,r]=p.useState(""),{viewer:o}=xn(),c=o==null?void 0:o.id,d=M.useLazyLoadQuery(Gr,{projectId:t}),u=M.useFragment(Ur,d.project),[g]=M.useMutation(Zr),[h]=M.useMutation(jr),f=p.useCallback(F=>{p.startTransition(()=>{g({variables:{projectId:t,annotationConfigId:F,spanId:l,filterUserIds:c?[c]:null}})})},[t,g,l,c]),b=p.useCallback(F=>{h({variables:{projectId:t,annotationConfigId:F,spanId:l,filterUserIds:c?[c]:null}})},[t,h,l,c]),y=d.allAnnotationConfigs.edges,v=(O=u.annotationConfigs)==null?void 0:O.edges,k=p.useMemo(()=>new Set(v==null?void 0:v.map(F=>F.node.id)),[v]),L=p.useMemo(()=>y.filter(F=>{var D;return(D=F.node.name)==null?void 0:D.toLowerCase().includes(i.toLowerCase())}),[y,i]),E=p.useCallback(F=>{k.has(F)?b(F):f(F)},[k,f,b]);return e(U,{children:e(w,{paddingTop:"size-100",maxWidth:320,children:e(pa,{autoFocus:!0,contain:!0,children:s(S,{direction:"column",gap:"size-100",children:[e(w,{paddingX:"size-100",paddingY:"size-100",children:s(S,{direction:"row",alignItems:"center",justifyContent:"space-between",gap:"size-100",children:[e(Q,{"aria-label":"Search annotation configs",value:i,onChange:F=>{r(F)},children:e(j,{placeholder:"Search annotation configs"})}),s(R,{children:[e(z,{"aria-label":"Create annotation config",onPress:()=>{a("/settings/annotations")},leadingVisual:e(T,{svg:e(xt,{})})}),s(ke,{placement:"bottom",children:[e(ae,{}),"Create new annotation config"]})]})]})}),e(we,{css:Q4,selectionMode:"single",selectionBehavior:"toggle","aria-label":"Annotation Configs",renderEmptyState:()=>e(w,{width:"100%",height:"100%",paddingBottom:"size-100",children:e(S,{direction:"column",alignItems:"center",justifyContent:"center",children:i?s(C,{style:{whiteSpace:"pre-wrap",textAlign:"center",padding:0},children:['No annotation configs found for "',i,'"']}):e(fa,{to:"/settings/annotations",children:"Configure Annotation Configs"})})}),onSelectionChange:F=>{if(F==="all"||F.size===0)return;const D=F.values().next().value;E(D)},children:L.map(F=>e(bn,{id:F.node.id,textValue:F.node.name,children:e(S,{direction:"row",alignItems:"center",children:s("label",{css:W4,children:[s(S,{direction:"row",alignItems:"center",gap:"size-100",children:[e("input",{type:"checkbox",checked:k.has(F.node.id),readOnly:!0}),e(ur,{annotation:{name:F.node.name||""},annotationDisplayPreference:"none",css:m`
                            width: fit-content;
                          `},F.node.name)]}),e("span",{children:q4[F.node.annotationType]||F.node.annotationType})]})})},F.node.id))})]})})})})}const Y4=({annotation:n,annotationConfig:a,currentAnnotationIDs:t,onCreate:l,onUpdate:i,onDelete:r,children:o,onSuccess:c,onError:d})=>{const u=a.name;pt(u);const g=a.annotationType,h=p.useMemo(()=>n||{name:u,label:null,score:null,explanation:null},[n,u]),f=Re({defaultValues:{[u]:h}}),b=f.setError,y=p.useCallback(async F=>{const D={...F[u],id:n==null?void 0:n.id};if(!D)return;let X;D.id&&g!=="FREEFORM"&&D.score==null&&!D.label||D.id&&g!=="FREEFORM"&&isNaN(D.score)&&!D.label||D.id&&g==="FREEFORM"&&!D.explanation?X="delete":D.id&&t.has(D.id)?X="update":X="create";let Y;switch(X){case"create":{Y=await l(D);break}case"update":{Y=await i(D);break}case"delete":{Y=await r(D);break}}Y.success?c==null||c(D):(b("root",{message:Y.error}),d==null||d(D,Y.error))},[n,u,g,t,b,l,r,d,c,i]),v=f.handleSubmit,k=p.useMemo(()=>ai.debounce(v(y),500),[v,y]),L=p.useRef(k);p.useEffect(()=>{L.current=k},[k]);const E=p.useRef(null),O=O1({control:f.control,name:u,exact:!0});return p.useEffect(()=>{if(!E.current){E.current=O;return}O!==E.current&&(E.current=O,L.current())},[O]),e(N1,{...f,children:o})},Qr="44px",J4=`calc(100% - ${Qr})`,Wr=({annotation:n,onSubmit:a})=>{const t=n!=null&&n.name?`${n.name}.explanation`:"explanation";return s(_e,{children:[e(Ln,{excludeFromTabOrder:!0,type:"button",isDisabled:!(n!=null&&n.id),className:"annotation-input-explanation",css:m`
          position: absolute;
          top: 6px;
          right: 0;
          width: ${Qr};
          font-size: var(--ac-global-dimension-static-font-size-75);
          background: none;
          border: none;
          padding: 0 !important;
          line-height: unset;
          color: var(--ac-global-link-color);
          &:disabled {
            cursor: default;
            opacity: var(--ac-opacity-disabled);
            color: var(--ac-global-text-color-900);
          }
          &:hover:not(:disabled) {
            text-decoration: underline;
            cursor: pointer;
            background: none;
          }
        `,children:"explain"}),s(ue,{placement:"bottom end",children:[e(It,{}),e(be,{children:({close:l})=>e(pa,{autoFocus:!0,contain:!0,restoreFocus:!0,children:e(w,{padding:"size-100",children:e("form",{onSubmit:i=>{i.preventDefault();const o=new FormData(i.target).get(t);typeof o=="string"&&(a==null||a(o)),l()},children:s(S,{direction:"column",gap:"size-100",children:[s(Q,{name:t,defaultValue:(n==null?void 0:n.explanation)??"",css:{minWidth:"300px"},children:[e(K,{children:"Explanation"}),e(j,{}),e(C,{slot:"description",children:"Why did you give this score?"})]}),e(z,{type:"submit",variant:"primary",size:"S",children:"Save"})]})})})})})]})]})},jt=n=>e(K,{className:V("react-aria-Label",n.className),css:m`
        max-width: ${J4};
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
      `,...n}),qr=p.forwardRef(({annotationConfig:n,annotation:a,onSubmitExplanation:t,...l},i)=>{var r;return s(S,{gap:"size-50",alignItems:"center",position:"relative",children:[e(Wr,{annotation:a,onSubmit:t}),s(Ne,{id:n.id,name:n.name,defaultSelectedKey:(a==null?void 0:a.label)??void 0,size:"S",...l,css:m`
          width: 100%;
        `,children:[e(jt,{children:n.name}),s(z,{ref:i,children:[e(Oe,{}),e(Ae,{})]}),e(C,{slot:"description",children:n.description}),e(ue,{children:e(we,{style:{minHeight:"auto"},children:(r=n.values)==null?void 0:r.map(o=>e(ee,{id:o.label,children:o.label},o.label))})})]})]})});qr.displayName="CategoricalAnnotationInput";const Xr=p.forwardRef(({annotationConfig:n,annotation:a,onSubmitExplanation:t,...l},i)=>s(S,{gap:"size-50",alignItems:"center",position:"relative",children:[e(Wr,{annotation:a,onSubmit:t}),s(Mi,{defaultValue:(a==null?void 0:a.score)??void 0,...l,ref:i,minValue:(n==null?void 0:n.lowerBound)??0,maxValue:(n==null?void 0:n.upperBound)??1,css:{width:"100%"},children:[e(jt,{children:n.name}),e(j,{placeholder:(n==null?void 0:n.optimizationDirection)==="MAXIMIZE"?`e.g. ${n.upperBound}`:`e.g. ${n.lowerBound}`}),s(C,{slot:"description",children:["from ",n.lowerBound," to ",n.upperBound]})]})]}));Xr.displayName="ContinuousAnnotationInput";const Yr=p.forwardRef(({annotationConfig:n,annotation:a,...t},l)=>e(S,{gap:"size-50",alignItems:"center",position:"relative",children:s(Q,{id:n.id,name:n.name,defaultValue:(a==null?void 0:a.explanation)??void 0,...t,ref:l,css:{width:"100%"},children:[e(jt,{children:n.name}),e(ma,{}),e(C,{slot:"description",children:n.description})]})}));Yr.displayName="FreeformAnnotationInput";function e9(n){const{annotationConfig:a,annotation:t}=n,{control:l}=$1();return s("div",{children:[a.annotationType==="CATEGORICAL"&&e($,{control:l,name:a.name,render:({field:{value:i,...r}})=>e(qr,{annotationConfig:a,annotation:t,...r,selectedKey:i==null?void 0:i.label,onSubmitExplanation:o=>{t!=null&&t.id&&r.onChange({...t,name:a.name,explanation:o})},onSelectionChange:o=>{var d,u;let c=o;if(c===(i==null?void 0:i.label)&&(c=null),typeof c=="string"&&c!=null){const g={...t,id:t==null?void 0:t.id,name:a.name,label:c,score:((u=(d=a.values)==null?void 0:d.find(h=>h.label===c))==null?void 0:u.score)??null};r.onChange(g)}else r.onChange({...t,id:t==null?void 0:t.id,name:a.name,label:null,score:null})}})}),a.annotationType==="CONTINUOUS"&&e($,{control:l,name:a.name,render:({field:{value:i,...r}})=>e(Xr,{annotationConfig:a,annotation:t,...r,onSubmitExplanation:o=>{t!=null&&t.id&&r.onChange({...t,name:a.name,explanation:o})},value:(i==null?void 0:i.score)??void 0,onChange:o=>{r.onChange({...t,id:t==null?void 0:t.id,name:a.name,score:o})}})}),a.annotationType==="FREEFORM"&&e($,{control:l,name:a.name,render:({field:{value:i,...r}})=>e(Yr,{annotationConfig:a,annotation:t,...r,value:(i==null?void 0:i.explanation)??"",onChange:o=>{r.onChange({...t,id:t==null?void 0:t.id,name:a.name,explanation:o})}})})]})}const n9="e";function a9(n){const{projectId:a,spanNodeId:t}=n,[l,i]=p.useState(null);return e(w,{height:"100%",maxHeight:"100%",overflow:"auto",children:s(S,{direction:"column",height:"100%",children:[e(w,{paddingY:"size-100",paddingX:"size-100",borderBottomWidth:"thin",borderColor:"dark",width:"100%",flex:"none",children:e(S,{direction:"row",alignItems:"center",justifyContent:"end",width:"100%",children:e(t9,{projectId:a,spanNodeId:t,disabled:l!==null,onAnnotationNameSelect:i})})}),e(p.Suspense,{children:e(r9,{spanId:t,projectId:a})})]})})}function t9(n){const{projectId:a,disabled:t=!1,spanNodeId:l,onAnnotationNameSelect:i}=n;return e(U,{children:s(_e,{children:[e(z,{variant:t?"default":"primary",isDisabled:t,size:"S",leadingVisual:e(T,{svg:e(xt,{})}),children:"Add Annotation"}),e(ue,{style:{border:"none"},placement:"bottom end",children:e(be,{children:({close:r})=>e(l9,{projectId:a,spanNodeId:l,onAnnotationNameSelect:o=>{i(o)},onClose:r})})})]})})}function l9(n){const{projectId:a,spanNodeId:t,onClose:l}=n;return e(Pi,{title:"Add Annotation from Config",backgroundColor:"light",borderColor:"light",children:e(p.Suspense,{children:e(o9,{projectId:a,spanId:t,onClose:l})})})}const i9=n=>!n.matches("button.annotation-input-explanation");function r9(n){var Y,_;const{spanId:a,projectId:t,extraAnnotationCards:l}=n,{viewer:i}=xn(),r=Ni(),o=p.useMemo(()=>i?[i.id]:[null],[i]),c=M.useLazyLoadQuery(Hr,{projectId:t,spanId:a,filterUserIds:o}),d=M.useFragment(Br,c.span),u=c.span.id,g=d.filteredSpanAnnotations,h=p.useMemo(()=>xs(g),[g]),f=p.useMemo(()=>new Set(h.map(A=>A.id)),[h]),b=(_=(Y=c.project)==null?void 0:Y.annotationConfigs)==null?void 0:_.configs,y=(b==null?void 0:b.length)??0,v=Di(),k=v==null?void 0:v.timeRange,[L]=M.useMutation($r),E=p.useCallback(A=>new Promise(H=>{var oe,Se;A.id?L({variables:{spanId:u,annotationIds:[A.id],timeRange:{start:(oe=k==null?void 0:k.start)==null?void 0:oe.toISOString(),end:(Se=k==null?void 0:k.end)==null?void 0:Se.toISOString()},projectId:t,filterUserIds:o},onCompleted:()=>{H({success:!0})},onError:$e=>{H({success:!1,error:$e.message}),r({title:"Error deleting annotation",message:$e.message})}}):H({success:!0})}),[L,u,k,t,r,o]),[O]=M.useMutation(Nr),F=p.useCallback(A=>new Promise(H=>{const oe=A.id;oe&&p.startTransition(()=>{var Se,$e;O({variables:{annotationId:oe,spanId:u,name:A.name,label:A.label,score:A.score,explanation:A.explanation||null,filterUserIds:o,timeRange:{start:(Se=k==null?void 0:k.start)==null?void 0:Se.toISOString(),end:($e=k==null?void 0:k.end)==null?void 0:$e.toISOString()},projectId:t},onCompleted:()=>{H({success:!0})},onError:Qt=>{H({success:!1,error:Qt.message}),r({title:"Error editing annotation",message:Qt.message})}})})}),[O,u,o,k,t,r]),[D]=M.useMutation(Or),X=p.useCallback(A=>new Promise(H=>{var oe,Se;D({variables:{input:{...A,spanId:u,annotatorKind:"HUMAN",explanation:A.explanation||null,source:"APP"},name:A.name,spanId:u,filterUserIds:o,timeRange:{start:(oe=k==null?void 0:k.start)==null?void 0:oe.toISOString(),end:(Se=k==null?void 0:k.end)==null?void 0:Se.toISOString()},projectId:t},onCompleted:()=>{H({success:!0})},onError:$e=>{H({success:!1,error:$e.message}),r({title:"Error creating annotation",message:$e.message})}})}),[D,u,k,t,r,o]);return s(w,{height:"100%",maxHeight:"100%",overflow:"auto",width:"100%",padding:"size-200",children:[!y&&!l&&s(S,{direction:"column",alignItems:"center",justifyContent:"center",height:"100%",children:[e(pc,{message:"No annotation configurations for this project"}),e(fa,{to:"/settings/annotations",children:"Configure Annotation Configs"})]}),!!y&&s(pa,{children:[e(j4,{hotkey:n9,accept:i9}),b==null?void 0:b.map((A,H)=>{const oe=h.find(Se=>Se.name===A.config.name);return e(Y4,{annotationConfig:A.config,currentAnnotationIDs:f,annotation:oe,onCreate:X,onUpdate:F,onDelete:E,children:e(e9,{annotation:oe,annotationConfig:A.config})},`${H}_${A.config.name}_form`)})]})]})}function o9(n){const{projectId:a,spanId:t}=n;return e(w,{minWidth:320,children:e(p.Suspense,{fallback:e(re,{}),children:e(S,{direction:"column",gap:"size-100",children:e(X4,{projectId:a,spanId:t})})})})}const Jr=m`
  display: flex;
  flex-direction: column;
  gap: var(--ac-global-dimension-size-50);
  width: 100%;
  &[data-outgoing="true"] {
    align-self: flex-end;
  }
  &[data-outgoing="false"] {
    align-self: flex-start;
  }
`,eo=m`
  display: flex;
  gap: var(--ac-global-dimension-size-100);
  width: 80%;
  align-items: flex-end;
  &[data-outgoing="true"] {
    flex-direction: row-reverse;
    align-self: flex-end;
  }
`,dt=24,s9=m`
  padding: var(--ac-global-dimension-size-100)
    var(--ac-global-dimension-size-150);
  font-size: var(--ac-global-font-size-s);
  line-height: var(--ac-global-line-height-s);
  word-wrap: break-word;
  &[data-outgoing="true"] {
    background-color: var(--ac-global-color-primary);
    color: var(--ac-global-color-grey-50);
    border-radius: var(--ac-global-rounding-large)
      var(--ac-global-rounding-large) 0 var(--ac-global-rounding-large);
  }
  &[data-outgoing="false"] {
    background-color: var(--ac-global-background-color-light);
    color: var(--ac-global-text-color-900);
    border-radius: var(--ac-global-rounding-large)
      var(--ac-global-rounding-large) var(--ac-global-rounding-large) 0;
  }
`,c9=m`
  font-size: var(--ac-global-font-size-xs);
  color: var(--ac-global-text-color-500);
  padding-left: calc(
    ${dt}px + var(--ac-global-dimension-size-100)
  );
  &[data-outgoing="true"] {
    text-align: right;
    padding-left: 0;
    padding-right: calc(
      ${dt}px + var(--ac-global-dimension-size-100)
    );
  }
`;function sp({text:n,timestamp:a,isOutgoing:t=!1,userName:l,userPicture:i=null}){return s("div",{css:Jr,"data-outgoing":t,children:[s("div",{css:eo,"data-outgoing":t,children:[e(yr,{name:l,profilePictureUrl:i,size:dt}),e("div",{css:s9,"data-outgoing":t,children:n})]}),e("div",{css:c9,"data-outgoing":t,children:e("time",{dateTime:a.toISOString(),children:Y0(a)})})]})}function cp({onSendMessage:n,isSending:a=!1,placeholder:t="Type a message"}){const[l,i]=p.useState(""),r=()=>{l.trim()&&(n&&n(l.trim()),i(""))};return e(w,{padding:"size-100",width:"100%",flex:"none",children:s(S,{direction:"row",gap:"size-100",children:[e(Q,{size:"M",value:l,onChange:i,onKeyDown:c=>{c.key==="Enter"&&!c.shiftKey&&(c.preventDefault(),r())},"aria-label":"Message input",isDisabled:a,children:e(j,{placeholder:t})}),e(z,{size:"M",variant:"primary",isDisabled:!l.trim()||a,onPress:r,"aria-label":a?"Sending message...":"Send",leadingVisual:a?e(T,{svg:e(Ai,{})}):e(T,{svg:e($c,{})})})]})})}const Il=24,d9=m`
  flex: none;
`,u9=m`
  width: 100%;
`,g9=m`
  width: 100%;
`,m9=m`
  &[data-outgoing="true"] {
    border-radius: var(--ac-global-rounding-large)
      var(--ac-global-rounding-large) 0 var(--ac-global-rounding-large);
  }
  &[data-outgoing="false"] {
    border-radius: var(--ac-global-rounding-large)
      var(--ac-global-rounding-large) var(--ac-global-rounding-large) 0;
  }
`;function dp({isOutgoing:n=!1,height:a=80}){return e("div",{css:m(Jr,g9),"data-outgoing":n,"data-testid":"message-container",children:s("div",{css:m(eo,u9),"data-outgoing":n,children:[e(fn,{width:Il,height:Il,borderRadius:"circle",animation:"pulse",css:d9}),e(fn,{"data-outgoing":n,height:a,animation:"wave","data-testid":"message-bubble-skeleton",css:m9})]})})}function up(n){const{kind:a}=n;return e(je,{size:"S",color:a==="HUMAN"?"var(--ac-global-color-blue-500)":"var(--ac-global-color-orange-500)",children:a})}const no=(function(){var n=[{defaultValue:null,kind:"LocalArgument",name:"annotationId"},{defaultValue:null,kind:"LocalArgument",name:"spanId"}],a=[{fields:[{items:[{kind:"Variable",name:"annotationIds.0",variableName:"annotationId"}],kind:"ListValue",name:"annotationIds"}],kind:"ObjectValue",name:"input"}],t=[{kind:"Variable",name:"id",variableName:"spanId"}],l={alias:null,args:null,kind:"ScalarField",name:"id",storageKey:null},i={alias:null,args:null,kind:"ScalarField",name:"name",storageKey:null},r={alias:null,args:null,kind:"ScalarField",name:"annotatorKind",storageKey:null},o={alias:null,args:null,kind:"ScalarField",name:"score",storageKey:null},c={alias:null,args:null,kind:"ScalarField",name:"label",storageKey:null},d={alias:null,args:null,kind:"ScalarField",name:"explanation",storageKey:null},u={alias:null,args:null,kind:"ScalarField",name:"createdAt",storageKey:null};return{fragment:{argumentDefinitions:n,kind:"Fragment",metadata:null,name:"SpanAnnotationActionMenuDeleteMutation",selections:[{alias:null,args:a,concreteType:"SpanAnnotationMutationPayload",kind:"LinkedField",name:"deleteSpanAnnotations",plural:!1,selections:[{alias:null,args:null,concreteType:"Query",kind:"LinkedField",name:"query",plural:!1,selections:[{alias:null,args:t,concreteType:null,kind:"LinkedField",name:"node",plural:!1,selections:[{kind:"InlineFragment",selections:[{args:null,kind:"FragmentSpread",name:"SpanAnnotationsEditor_spanAnnotations"},{args:null,kind:"FragmentSpread",name:"SpanFeedback_annotations"}],type:"Span",abstractKey:null}],storageKey:null}],storageKey:null}],storageKey:null}],type:"Mutation",abstractKey:null},kind:"Request",operation:{argumentDefinitions:n,kind:"Operation",name:"SpanAnnotationActionMenuDeleteMutation",selections:[{alias:null,args:a,concreteType:"SpanAnnotationMutationPayload",kind:"LinkedField",name:"deleteSpanAnnotations",plural:!1,selections:[{alias:null,args:null,concreteType:"Query",kind:"LinkedField",name:"query",plural:!1,selections:[{alias:null,args:t,concreteType:null,kind:"LinkedField",name:"node",plural:!1,selections:[{alias:null,args:null,kind:"ScalarField",name:"__typename",storageKey:null},l,{kind:"InlineFragment",selections:[{alias:"filteredSpanAnnotations",args:[{fields:[{kind:"Literal",name:"exclude",value:{names:["note"]}},{fields:[{kind:"Literal",name:"userIds",value:null}],kind:"ObjectValue",name:"include"}],kind:"ObjectValue",name:"filter"}],concreteType:"SpanAnnotation",kind:"LinkedField",name:"spanAnnotations",plural:!0,selections:[l,i,r,o,c,d,u],storageKey:'spanAnnotations(filter:{"exclude":{"names":["note"]},"include":{"userIds":null}})'},{alias:null,args:null,concreteType:"SpanAnnotation",kind:"LinkedField",name:"spanAnnotations",plural:!0,selections:[l,i,c,o,d,{alias:null,args:null,kind:"ScalarField",name:"metadata",storageKey:null},r,{alias:null,args:null,kind:"ScalarField",name:"identifier",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"source",storageKey:null},u,{alias:null,args:null,kind:"ScalarField",name:"updatedAt",storageKey:null},{alias:null,args:null,concreteType:"User",kind:"LinkedField",name:"user",plural:!1,selections:[l,{alias:null,args:null,kind:"ScalarField",name:"username",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"profilePictureUrl",storageKey:null}],storageKey:null}],storageKey:null}],type:"Span",abstractKey:null}],storageKey:null}],storageKey:null}],storageKey:null}]},params:{cacheID:"bcdc8dccf3bfa49b8aa7960710a4deed",id:null,metadata:{},name:"SpanAnnotationActionMenuDeleteMutation",operationKind:"mutation",text:`mutation SpanAnnotationActionMenuDeleteMutation(
  $annotationId: ID!
  $spanId: ID!
) {
  deleteSpanAnnotations(input: {annotationIds: [$annotationId]}) {
    query {
      node(id: $spanId) {
        __typename
        ... on Span {
          ...SpanAnnotationsEditor_spanAnnotations
          ...SpanFeedback_annotations
        }
        id
      }
    }
  }
}

fragment SpanAnnotationsEditor_spanAnnotations on Span {
  id
  filteredSpanAnnotations: spanAnnotations(filter: {exclude: {names: ["note"]}, include: {}}) {
    id
    name
    annotatorKind
    score
    label
    explanation
    createdAt
  }
}

fragment SpanFeedback_annotations on Span {
  id
  spanAnnotations {
    id
    name
    label
    score
    explanation
    metadata
    annotatorKind
    identifier
    source
    createdAt
    updatedAt
    user {
      id
      username
      profilePictureUrl
    }
  }
}
`}}})();no.hash="436457e2120f7750037b024a1b96e214";function gp(n){const{annotationId:a,spanNodeId:t,annotationName:l,onSpanAnnotationActionSuccess:i,onSpanAnnotationActionError:r,buttonVariant:o,buttonSize:c}=n,[d]=M.useMutation(no),u=p.useCallback(()=>{p.startTransition(()=>{d({variables:{annotationId:a,spanId:t},onCompleted:()=>{i({title:"Annotation Deleted",message:`Annotation ${l} has been deleted.`}),f(!1)},onError:b=>{r(b)}})})},[d,a,t,i,l,r]),g=p.useRef(null),[h,f]=p.useState(!1);return s(U,{children:[s(_e,{children:[e(z,{ref:g,size:c,variant:o,leadingVisual:e(T,{svg:e(Oc,{})})}),e(ue,{children:e(be,{children:({close:b})=>e(we,{style:{minHeight:"auto"},children:e(bn,{id:"deleteAnnotation",onAction:()=>{f(!0),b()},children:s(S,{direction:"row",gap:"size-75",justifyContent:"start",alignItems:"center",children:[e(T,{svg:e(Tt,{})}),e(C,{children:"Delete"})]})})})})})]}),e(_e,{isOpen:h,onOpenChange:f,children:e(Cn,{children:e(vn,{children:e(be,{children:({close:b})=>s(Ke,{children:[e(Pe,{children:e(Ve,{children:"Delete Annotation"})}),e(w,{padding:"size-200",children:e(C,{color:"danger",children:`Are you sure you want to delete annotation ${l}? This cannot be undone.`})}),e(w,{paddingEnd:"size-200",paddingTop:"size-100",paddingBottom:"size-100",borderTopColor:"light",borderTopWidth:"thin",children:s(S,{direction:"row",justifyContent:"end",gap:"size-200",children:[e(hr,{children:e(z,{onPress:b,children:"Cancel"})}),e(z,{variant:"danger",onPress:()=>{u()},children:"Delete Annotation"})]})})]})})})})})]})}const ao=(function(){var n={defaultValue:null,kind:"LocalArgument",name:"description"},a={defaultValue:null,kind:"LocalArgument",name:"metadata"},t={defaultValue:null,kind:"LocalArgument",name:"name"},l=[{alias:null,args:[{fields:[{kind:"Variable",name:"description",variableName:"description"},{kind:"Variable",name:"metadata",variableName:"metadata"},{kind:"Variable",name:"name",variableName:"name"}],kind:"ObjectValue",name:"input"}],concreteType:"DatasetMutationPayload",kind:"LinkedField",name:"createDataset",plural:!1,selections:[{alias:null,args:null,concreteType:"Dataset",kind:"LinkedField",name:"dataset",plural:!1,selections:[{alias:null,args:null,kind:"ScalarField",name:"id",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"name",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"description",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"metadata",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"createdAt",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"exampleCount",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"experimentCount",storageKey:null}],storageKey:null}],storageKey:null}];return{fragment:{argumentDefinitions:[n,a,t],kind:"Fragment",metadata:null,name:"CreateDatasetFormMutation",selections:l,type:"Mutation",abstractKey:null},kind:"Request",operation:{argumentDefinitions:[t,n,a],kind:"Operation",name:"CreateDatasetFormMutation",selections:l},params:{cacheID:"6aa615e27e1ccaa5431ba481842b43d0",id:null,metadata:{},name:"CreateDatasetFormMutation",operationKind:"mutation",text:`mutation CreateDatasetFormMutation(
  $name: String!
  $description: String = null
  $metadata: JSON = null
) {
  createDataset(input: {name: $name, description: $description, metadata: $metadata}) {
    dataset {
      id
      name
      description
      metadata
      createdAt
      exampleCount
      experimentCount
    }
  }
}
`}}})();ao.hash="5921369d33cc0fb1dffb5d943469a378";function to({datasetName:n,datasetDescription:a,datasetMetadata:t,onSubmit:l,isSubmitting:i,submitButtonText:r,formMode:o}){const{control:c,handleSubmit:d,formState:{isDirty:u}}=Re({defaultValues:{name:n??"Dataset "+new Date().toISOString(),description:a??"",metadata:JSON.stringify(t,null,2)??"{}"}});return s(on,{children:[s(w,{padding:"size-200",children:[e($,{name:"name",control:c,rules:{required:"Dataset name is required"},render:({field:{onChange:g,onBlur:h,value:f},fieldState:{invalid:b,error:y}})=>s(Q,{isInvalid:b,onChange:g,onBlur:h,value:f.toString(),children:[e(K,{children:"Dataset Name"}),e(j,{placeholder:"e.x. Golden Dataset"}),y!=null&&y.message?e(W,{children:y.message}):e(C,{slot:"description",children:"The name of the dataset"})]})}),e($,{name:"description",control:c,render:({field:{onChange:g,onBlur:h,value:f},fieldState:{invalid:b,error:y}})=>s(Q,{isInvalid:b,onChange:g,onBlur:h,value:f.toString(),children:[e(K,{children:"Description"}),e(ma,{placeholder:"e.x. A golden dataset for structured data extraction"}),y!=null&&y.message?e(W,{children:y.message}):e(C,{slot:"description",children:"The description of the dataset"})]})}),e($,{name:"metadata",control:c,rules:{validate:g=>du(g)?!0:"metadata must be a valid JSON object"},render:({field:{onChange:g,onBlur:h,value:f},fieldState:{invalid:b,error:y}})=>e(x3,{validationState:b?"invalid":"valid",label:"metadata",errorMessage:y==null?void 0:y.message,description:"A JSON object containing metadata for the dataset",children:e(k3,{value:f,onChange:g,onBlur:h})})})]}),e(w,{paddingEnd:"size-200",paddingTop:"size-100",paddingBottom:"size-100",borderTopColor:"light",borderTopWidth:"thin",children:e(S,{direction:"row",justifyContent:"end",children:e(z,{isDisabled:(o==="edit"?!u:!1)||i,variant:u?"primary":"default",size:"S",onPress:()=>{d(l)()},children:r})})})]})}function p9(n){const{onDatasetCreated:a,onDatasetCreateError:t}=n,[l,i]=M.useMutation(ao),r=p.useCallback(o=>{l({variables:{...o,metadata:JSON.parse(o.metadata)},onCompleted:c=>{a(c.createDataset.dataset)},updater:c=>{const d=M.ConnectionHandler.getConnectionID("client:root","DatasetPicker__datasets"),g=c.getRootField("createDataset").getLinkedRecord("dataset"),h=c.get(d);if(h&&g){const f=M.ConnectionHandler.createEdge(c,h,g,"DatasetEdge");M.ConnectionHandler.insertEdgeAfter(h,f)}},onError:c=>{t(c)}})},[l,a,t]);return e(to,{isSubmitting:i,onSubmit:r,submitButtonText:i?"Creating...":"Create Dataset",formMode:"create"})}const lo=(function(){var n={defaultValue:null,kind:"LocalArgument",name:"datasetId"},a={defaultValue:null,kind:"LocalArgument",name:"description"},t={defaultValue:null,kind:"LocalArgument",name:"metadata"},l={defaultValue:null,kind:"LocalArgument",name:"name"},i=[{fields:[{kind:"Variable",name:"datasetId",variableName:"datasetId"},{kind:"Variable",name:"description",variableName:"description"},{kind:"Variable",name:"metadata",variableName:"metadata"},{kind:"Variable",name:"name",variableName:"name"}],kind:"ObjectValue",name:"input"}],r={alias:null,args:null,kind:"ScalarField",name:"name",storageKey:null},o={alias:null,args:null,kind:"ScalarField",name:"description",storageKey:null},c={alias:null,args:null,kind:"ScalarField",name:"metadata",storageKey:null};return{fragment:{argumentDefinitions:[n,a,t,l],kind:"Fragment",metadata:null,name:"EditDatasetFormMutation",selections:[{alias:null,args:i,concreteType:"DatasetMutationPayload",kind:"LinkedField",name:"patchDataset",plural:!1,selections:[{alias:null,args:null,concreteType:"Dataset",kind:"LinkedField",name:"dataset",plural:!1,selections:[r,o,c],storageKey:null}],storageKey:null}],type:"Mutation",abstractKey:null},kind:"Request",operation:{argumentDefinitions:[n,l,a,t],kind:"Operation",name:"EditDatasetFormMutation",selections:[{alias:null,args:i,concreteType:"DatasetMutationPayload",kind:"LinkedField",name:"patchDataset",plural:!1,selections:[{alias:null,args:null,concreteType:"Dataset",kind:"LinkedField",name:"dataset",plural:!1,selections:[r,o,c,{alias:null,args:null,kind:"ScalarField",name:"id",storageKey:null}],storageKey:null}],storageKey:null}]},params:{cacheID:"24675cd487da4f57f6aa04d850e65ad3",id:null,metadata:{},name:"EditDatasetFormMutation",operationKind:"mutation",text:`mutation EditDatasetFormMutation(
  $datasetId: ID!
  $name: String!
  $description: String = null
  $metadata: JSON = null
) {
  patchDataset(input: {datasetId: $datasetId, name: $name, description: $description, metadata: $metadata}) {
    dataset {
      name
      description
      metadata
      id
    }
  }
}
`}}})();lo.hash="e952d9cbc840dd6cd447b3024178aab4";function mp({datasetName:n,datasetId:a,datasetDescription:t,onDatasetEdited:l,onDatasetEditError:i,datasetMetadata:r}){const[o,c]=M.useMutation(lo);return e(to,{datasetName:n,datasetDescription:t,datasetMetadata:r,onSubmit:u=>{o({variables:{datasetId:a,...u,metadata:JSON.parse(u.metadata)},onCompleted:()=>{l()},onError:g=>{i(g)}})},isSubmitting:c,submitButtonText:c?"Saving...":"Save",formMode:"edit"})}const io=(function(){var n={alias:null,args:null,kind:"ScalarField",name:"id",storageKey:null},a={alias:"dataset",args:null,concreteType:"Dataset",kind:"LinkedField",name:"node",plural:!1,selections:[n,{alias:null,args:null,kind:"ScalarField",name:"name",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"exampleCount",storageKey:null}],storageKey:null},t={alias:null,args:null,kind:"ScalarField",name:"cursor",storageKey:null},l={alias:null,args:null,kind:"ScalarField",name:"__typename",storageKey:null},i={alias:null,args:null,concreteType:"PageInfo",kind:"LinkedField",name:"pageInfo",plural:!1,selections:[{alias:null,args:null,kind:"ScalarField",name:"endCursor",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"hasNextPage",storageKey:null}],storageKey:null},r=[{kind:"Literal",name:"first",value:100}];return{fragment:{argumentDefinitions:[],kind:"Fragment",metadata:null,name:"DatasetSelectQuery",selections:[{alias:"datasets",args:null,concreteType:"DatasetConnection",kind:"LinkedField",name:"__DatasetPicker__datasets_connection",plural:!1,selections:[{alias:null,args:null,concreteType:"DatasetEdge",kind:"LinkedField",name:"edges",plural:!0,selections:[a,t,{alias:null,args:null,concreteType:"Dataset",kind:"LinkedField",name:"node",plural:!1,selections:[l],storageKey:null}],storageKey:null},i],storageKey:null}],type:"Query",abstractKey:null},kind:"Request",operation:{argumentDefinitions:[],kind:"Operation",name:"DatasetSelectQuery",selections:[{alias:null,args:r,concreteType:"DatasetConnection",kind:"LinkedField",name:"datasets",plural:!1,selections:[{alias:null,args:null,concreteType:"DatasetEdge",kind:"LinkedField",name:"edges",plural:!0,selections:[a,t,{alias:null,args:null,concreteType:"Dataset",kind:"LinkedField",name:"node",plural:!1,selections:[l,n],storageKey:null}],storageKey:null},i],storageKey:"datasets(first:100)"},{alias:null,args:r,filters:null,handle:"connection",key:"DatasetPicker__datasets",kind:"LinkedHandle",name:"datasets"}]},params:{cacheID:"e6bd6ad78e045a4cc2a4dad99aeb6fe3",id:null,metadata:{connection:[{count:null,cursor:null,direction:"forward",path:["datasets"]}]},name:"DatasetSelectQuery",operationKind:"query",text:`query DatasetSelectQuery {
  datasets(first: 100) {
    edges {
      dataset: node {
        id
        name
        exampleCount
      }
      cursor
      node {
        __typename
        id
      }
    }
    pageInfo {
      endCursor
      hasNextPage
    }
  }
}
`}}})();io.hash="8125ffe6752f16b2629b9773330a0a70";function pp(n){const a=M.useLazyLoadQuery(io,{},{fetchPolicy:"store-and-network"});return s(Ne,{"data-testid":"dataset-picker",size:n.size,className:"dataset-picker","aria-label":"select a dataset",onSelectionChange:t=>{var l;t&&((l=n.onSelectionChange)==null||l.call(n,t.toString()))},placeholder:n.placeholder??"Select a dataset",onBlur:n.onBlur,isRequired:n.isRequired,selectedKey:n.selectedKey,children:[n.label&&e(K,{children:n.label}),s(z,{className:"dataset-picker-button",children:[e(Oe,{}),e(Ae,{})]}),n.errorMessage&&e(C,{slot:"errorMessage",children:n.errorMessage}),e(ue,{children:e(we,{css:m`
            min-height: auto;
          `,children:a.datasets.edges.map(({dataset:t})=>e(ee,{id:t.id,children:s(S,{direction:"row",alignItems:"center",gap:"size-200",justifyContent:"space-between",width:"100%",children:[e(C,{children:t.name}),s(C,{color:"text-700",size:"XS",children:[t.exampleCount," examples"]})]})},t.id))})})]})}function hp({onDatasetCreated:n}){const[a,t]=p.useState(null),[l,i]=p.useState(!1),r=zt();return s(_e,{isOpen:l,onOpenChange:o=>{t(null),i(o)},children:[e(z,{variant:"default",leadingVisual:e(T,{svg:e(xt,{})}),"aria-label":"Create a new dataset",onPress:()=>{t(null),i(!0)}}),e(ue,{placement:"bottom right",css:m`
          border: none;
        `,children:e(Pi,{title:"Create New Dataset",borderColor:"light",backgroundColor:"light",children:s(w,{width:"500px",children:[a?e(ya,{variant:"danger",children:a}):null,e(p9,{onDatasetCreateError:o=>{const c=$t(o);t((c==null?void 0:c[0])??o.message)},onDatasetCreated:({id:o,name:c})=>{t(null),i(!1),n&&n(o),r({title:"Dataset Created",message:`Dataset "${c}" created successfully`})}})]})})})]})}const fp=({buttonText:n,successText:a,tooltipText:t="Copy link to clipboard",preserveSearchParams:l=!1})=>{const i=B1(),r=zt();return s(R,{delay:200,children:[e(z,{size:"S",leadingVisual:e(T,{svg:e(Qc,{})}),onPress:()=>{const o=new URL(i.pathname,window.location.origin);l&&(o.search=i.search),navigator.clipboard.writeText(o.toString()),r({title:a??"Link copied to clipboard",expireMs:1e3})},children:n}),e(mt,{offset:10,children:e(w,{padding:"size-100",backgroundColor:"light",borderColor:"dark",borderWidth:"thin",borderRadius:"small",children:e(C,{children:t})})})]})};function bp(n){return s(be,{children:[s(Pe,{children:[e(Ve,{children:"Annotate"}),e(ln,{children:e(Qe,{slot:"close"})})]}),e(Ke,{children:e(a9,{...n})})]})}function h9({listeners:n,attributes:a},t){return e("button",{ref:t,...n,...a,"aria-roledescription":"draggable","aria-pressed":"false","aria-disabled":"false",className:"button--reset",css:m`
        cursor: grab;
        background-color: var(--ac-global-color-grey-200);
        border: 1px solid var(--ac-global-color-grey-400);
        color: var(--ac-global-text-color-900);
        display: flex;
        align-items: center;
        justify-content: center;
        padding: var(--ac-global-dimension-size-100)
          var(--ac-global-dimension-size-50);
        border-radius: var(--ac-global-rounding-small);
        overflow: hidden;
      `,children:e("svg",{viewBox:"0 0 20 20",width:"12",fill:"currentColor",children:e("path",{d:"M7 2a2 2 0 1 0 .001 4.001A2 2 0 0 0 7 2zm0 6a2 2 0 1 0 .001 4.001A2 2 0 0 0 7 8zm0 6a2 2 0 1 0 .001 4.001A2 2 0 0 0 7 14zm6-8a2 2 0 1 0-.001-4.001A2 2 0 0 0 13 6zm0 2a2 2 0 1 0 .001 4.001A2 2 0 0 0 13 8zm0 6a2 2 0 1 0 .001 4.001A2 2 0 0 0 13 14z"})})})}const yp=rn.forwardRef(h9);function vp({preInitializationMinHeight:n,children:a}){const[t,l]=p.useState(!1),[i,r]=p.useState(!1),o=p.useRef(null);return p.useEffect(()=>{const c=new IntersectionObserver(([u])=>{l(u.isIntersecting)});o.current&&c.observe(o.current);const d=o.current;return()=>{d&&c.unobserve(d)}},[]),p.useLayoutEffect(()=>{t&&!i&&r(!0)},[i,t]),e("div",{ref:o,css:m`
        min-height: ${i?"auto":`${n}px`};
      `,children:a})}function Cp(n){return Object.values(Ze).includes(n)}function kp(n){return s("div",{role:"toolbar",css:m`
        padding: var(--ac-global-dimension-static-size-50)
          var(--ac-global-dimension-static-size-200);
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        align-items: center;
        gap: var(--ac-global-dimension-static-size-100);
        border-bottom: 1px solid var(--ac-global-border-color-dark);
        flex: none;
        min-height: 29px;
        .toolbar__main {
          display: flex;
          flex-direction: row;
          gap: var(--ac-global-dimension-static-size-100);
        }
      `,children:[e("div",{"data-testid":"toolbar-main",className:"toolbar__main",children:n.children}),n.extra?e("div",{"data-testid":"toolbar-extra",children:n.extra}):null]})}const f9=m`
  /* Align with other toolbar components */
  .react-aria-Button {
    height: 30px;
    min-height: 30px;
  }

  .react-aria-Label {
    padding: 5px 0;
    display: inline-block;
    font-size: var(--ac-global-dimension-static-font-size-75);
    font-weight: var(--px-font-weight-heavy);
  }
`,b9=m`
  /* Target the button element specifically */
  button[aria-haspopup="listbox"] {
    border: 1.1px solid var(--ac-global-color-designation-turquoise) !important;
    border-radius: var(--ac-global-rounding-small) !important;

    &:hover {
      border-color: white !important;
    }
  }
`;function Lp(n){const{timeRange:a,timePreset:t,setTimePreset:l}=Ws(),{primaryInferences:{name:i}}=ha(),r=i.slice(0,10);return e("div",{css:b9,children:e(li,{color:"designationTurquoise",children:s(R,{children:[s(Ne,{selectedKey:t,"data-testid":"inferences-time-range","aria-label":"Time range for the primary inferences",onSelectionChange:o=>{o!==t&&l(o)},css:f9,children:[s(K,{children:[r," inferences"]}),s(z,{children:[e(Oe,{}),e(Ae,{})]}),e(C,{slot:"description",children:""}),e(ue,{children:s(we,{children:[e(ee,{id:J.all,children:"All"},J.all),e(ee,{id:J.last_hour,children:"Last Hour"},J.last_hour),e(ee,{id:J.last_day,children:"Last Day"},J.last_day),e(ee,{id:J.last_week,children:"Last Week"},J.last_week),e(ee,{id:J.last_month,children:"Last Month"},J.last_month),e(ee,{id:J.last_3_months,children:"Last 3 Months"},J.last_3_months),e(ee,{id:J.first_hour,children:"First Hour"},J.first_hour),e(ee,{id:J.first_day,children:"First Day"},J.first_day),e(ee,{id:J.first_week,children:"First Week"},J.first_week),e(ee,{id:J.first_month,children:"First Month"},J.first_month)]})})]}),e(ie,{children:s("section",{css:m`
                h4 {
                  margin-bottom: 0.5rem;
                }
              `,children:[e(ne,{level:4,children:"primary inferences time range"}),s("div",{children:["start: ",en(a.start)]}),s("div",{children:["end: ",en(a.end)]})]})})]})})})}const zl=Ie("%x %X");function wp({timeRange:n}){const{referenceInferences:a}=ha(),l=((a==null?void 0:a.name)??"reference").slice(0,10);return e("div",{css:m`
        .ac-textfield {
          min-width: 331px;
        }
      `,children:e(li,{color:"designationPurple",children:s(R,{children:[s(Q,{isReadOnly:!0,"aria-label":"reference inferences time range",value:`${zl(n.start)} - ${zl(n.end)}`,children:[e(K,{children:`${l} inferences`}),e(j,{})]}),s(ke,{children:[e(ae,{}),"The static time range of the reference inferences"]})]})})})}const ro=(function(){var n=[{defaultValue:50,kind:"LocalArgument",name:"count"},{defaultValue:null,kind:"LocalArgument",name:"cursor"},{defaultValue:null,kind:"LocalArgument",name:"endTime"},{defaultValue:null,kind:"LocalArgument",name:"startTime"}],a=[{kind:"Variable",name:"after",variableName:"cursor"},{kind:"Variable",name:"first",variableName:"count"}],t={alias:null,args:null,kind:"ScalarField",name:"id",storageKey:null},l={fields:[{kind:"Variable",name:"end",variableName:"endTime"},{kind:"Variable",name:"start",variableName:"startTime"}],kind:"ObjectValue",name:"timeRange"};return{fragment:{argumentDefinitions:n,kind:"Fragment",metadata:null,name:"ModelSchemaTableDimensionsQuery",selections:[{args:[{kind:"Variable",name:"count",variableName:"count"},{kind:"Variable",name:"cursor",variableName:"cursor"},{kind:"Variable",name:"endTime",variableName:"endTime"},{kind:"Variable",name:"startTime",variableName:"startTime"}],kind:"FragmentSpread",name:"ModelSchemaTable_dimensions"}],type:"Query",abstractKey:null},kind:"Request",operation:{argumentDefinitions:n,kind:"Operation",name:"ModelSchemaTableDimensionsQuery",selections:[{alias:null,args:null,concreteType:"InferenceModel",kind:"LinkedField",name:"model",plural:!1,selections:[{alias:null,args:a,concreteType:"DimensionConnection",kind:"LinkedField",name:"dimensions",plural:!1,selections:[{alias:null,args:null,concreteType:"DimensionEdge",kind:"LinkedField",name:"edges",plural:!0,selections:[{alias:"dimension",args:null,concreteType:"Dimension",kind:"LinkedField",name:"node",plural:!1,selections:[t,{alias:null,args:null,kind:"ScalarField",name:"name",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"type",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"dataType",storageKey:null},{alias:"cardinality",args:[{kind:"Literal",name:"metric",value:"cardinality"},l],kind:"ScalarField",name:"dataQualityMetric",storageKey:null},{alias:"percentEmpty",args:[{kind:"Literal",name:"metric",value:"percentEmpty"},l],kind:"ScalarField",name:"dataQualityMetric",storageKey:null},{alias:"min",args:[{kind:"Literal",name:"metric",value:"min"},l],kind:"ScalarField",name:"dataQualityMetric",storageKey:null},{alias:"mean",args:[{kind:"Literal",name:"metric",value:"mean"},l],kind:"ScalarField",name:"dataQualityMetric",storageKey:null},{alias:"max",args:[{kind:"Literal",name:"metric",value:"max"},l],kind:"ScalarField",name:"dataQualityMetric",storageKey:null},{alias:"psi",args:[{kind:"Literal",name:"metric",value:"psi"},l],kind:"ScalarField",name:"driftMetric",storageKey:null}],storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"cursor",storageKey:null},{alias:null,args:null,concreteType:"Dimension",kind:"LinkedField",name:"node",plural:!1,selections:[{alias:null,args:null,kind:"ScalarField",name:"__typename",storageKey:null},t],storageKey:null}],storageKey:null},{alias:null,args:null,concreteType:"PageInfo",kind:"LinkedField",name:"pageInfo",plural:!1,selections:[{alias:null,args:null,kind:"ScalarField",name:"endCursor",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"hasNextPage",storageKey:null}],storageKey:null}],storageKey:null},{alias:null,args:a,filters:null,handle:"connection",key:"ModelSchemaTable_dimensions",kind:"LinkedHandle",name:"dimensions"}],storageKey:null}]},params:{cacheID:"c622a7e3a3aa7a2463ab98779e6499a9",id:null,metadata:{},name:"ModelSchemaTableDimensionsQuery",operationKind:"query",text:`query ModelSchemaTableDimensionsQuery(
  $count: Int = 50
  $cursor: String = null
  $endTime: DateTime!
  $startTime: DateTime!
) {
  ...ModelSchemaTable_dimensions_4sIU9C
}

fragment ModelSchemaTable_dimensions_4sIU9C on Query {
  model {
    dimensions(first: $count, after: $cursor) {
      edges {
        dimension: node {
          id
          name
          type
          dataType
          cardinality: dataQualityMetric(metric: cardinality, timeRange: {start: $startTime, end: $endTime})
          percentEmpty: dataQualityMetric(metric: percentEmpty, timeRange: {start: $startTime, end: $endTime})
          min: dataQualityMetric(metric: min, timeRange: {start: $startTime, end: $endTime})
          mean: dataQualityMetric(metric: mean, timeRange: {start: $startTime, end: $endTime})
          max: dataQualityMetric(metric: max, timeRange: {start: $startTime, end: $endTime})
          psi: driftMetric(metric: psi, timeRange: {start: $startTime, end: $endTime})
        }
        cursor
        node {
          __typename
          id
        }
      }
      pageInfo {
        endCursor
        hasNextPage
      }
    }
  }
}
`}}})();ro.hash="fb4c57e0ea77548c4e96ceb418e06614";const oo=(function(){var n=["model","dimensions"],a={fields:[{kind:"Variable",name:"end",variableName:"endTime"},{kind:"Variable",name:"start",variableName:"startTime"}],kind:"ObjectValue",name:"timeRange"};return{argumentDefinitions:[{defaultValue:50,kind:"LocalArgument",name:"count"},{defaultValue:null,kind:"LocalArgument",name:"cursor"},{defaultValue:null,kind:"LocalArgument",name:"endTime"},{defaultValue:null,kind:"LocalArgument",name:"startTime"}],kind:"Fragment",metadata:{connection:[{count:"count",cursor:"cursor",direction:"forward",path:n}],refetch:{connection:{forward:{count:"count",cursor:"cursor"},backward:null,path:n},fragmentPathInResult:[],operation:ro}},name:"ModelSchemaTable_dimensions",selections:[{alias:null,args:null,concreteType:"InferenceModel",kind:"LinkedField",name:"model",plural:!1,selections:[{alias:"dimensions",args:null,concreteType:"DimensionConnection",kind:"LinkedField",name:"__ModelSchemaTable_dimensions_connection",plural:!1,selections:[{alias:null,args:null,concreteType:"DimensionEdge",kind:"LinkedField",name:"edges",plural:!0,selections:[{alias:"dimension",args:null,concreteType:"Dimension",kind:"LinkedField",name:"node",plural:!1,selections:[{alias:null,args:null,kind:"ScalarField",name:"id",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"name",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"type",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"dataType",storageKey:null},{alias:"cardinality",args:[{kind:"Literal",name:"metric",value:"cardinality"},a],kind:"ScalarField",name:"dataQualityMetric",storageKey:null},{alias:"percentEmpty",args:[{kind:"Literal",name:"metric",value:"percentEmpty"},a],kind:"ScalarField",name:"dataQualityMetric",storageKey:null},{alias:"min",args:[{kind:"Literal",name:"metric",value:"min"},a],kind:"ScalarField",name:"dataQualityMetric",storageKey:null},{alias:"mean",args:[{kind:"Literal",name:"metric",value:"mean"},a],kind:"ScalarField",name:"dataQualityMetric",storageKey:null},{alias:"max",args:[{kind:"Literal",name:"metric",value:"max"},a],kind:"ScalarField",name:"dataQualityMetric",storageKey:null},{alias:"psi",args:[{kind:"Literal",name:"metric",value:"psi"},a],kind:"ScalarField",name:"driftMetric",storageKey:null}],storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"cursor",storageKey:null},{alias:null,args:null,concreteType:"Dimension",kind:"LinkedField",name:"node",plural:!1,selections:[{alias:null,args:null,kind:"ScalarField",name:"__typename",storageKey:null}],storageKey:null}],storageKey:null},{alias:null,args:null,concreteType:"PageInfo",kind:"LinkedField",name:"pageInfo",plural:!1,selections:[{alias:null,args:null,kind:"ScalarField",name:"endCursor",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"hasNextPage",storageKey:null}],storageKey:null}],storageKey:null}],storageKey:null}],type:"Query",abstractKey:null}})();oo.hash="fb4c57e0ea77548c4e96ceb418e06614";function Sp(n){const{data:a}=M.usePaginationFragment(oo,n.model),t=p.useMemo(()=>a.model.dimensions.edges.map(({dimension:i})=>({...i})),[a]),l=rn.useMemo(()=>[{header:"name",accessorKey:"name",cell:r=>e(fa,{to:`dimensions/${r.row.original.id}`,children:r.renderValue()})},{header:"type",accessorKey:"type"},{header:"data type",accessorKey:"dataType"},{header:"cardinality",accessorKey:"cardinality",cell:F3},{header:"% empty",accessorKey:"percentEmpty",cell:E3},{header:"min",accessorKey:"min",cell:Kn},{header:"mean",accessorKey:"mean",cell:Kn},{header:"max",accessorKey:"max",cell:Kn},{header:"PSI",accessorKey:"psi",cell:Kn}],[]);return e(fr,{columns:l,data:t})}const so=(function(){var n=[{defaultValue:50,kind:"LocalArgument",name:"count"},{defaultValue:null,kind:"LocalArgument",name:"cursor"},{defaultValue:null,kind:"LocalArgument",name:"endTime"},{defaultValue:null,kind:"LocalArgument",name:"startTime"}],a=[{kind:"Variable",name:"after",variableName:"cursor"},{kind:"Variable",name:"first",variableName:"count"}],t={alias:null,args:null,kind:"ScalarField",name:"id",storageKey:null};return{fragment:{argumentDefinitions:n,kind:"Fragment",metadata:null,name:"ModelEmbeddingsTableEmbeddingDimensionsQuery",selections:[{args:[{kind:"Variable",name:"count",variableName:"count"},{kind:"Variable",name:"cursor",variableName:"cursor"},{kind:"Variable",name:"endTime",variableName:"endTime"},{kind:"Variable",name:"startTime",variableName:"startTime"}],kind:"FragmentSpread",name:"ModelEmbeddingsTable_embeddingDimensions"}],type:"Query",abstractKey:null},kind:"Request",operation:{argumentDefinitions:n,kind:"Operation",name:"ModelEmbeddingsTableEmbeddingDimensionsQuery",selections:[{alias:null,args:null,concreteType:"InferenceModel",kind:"LinkedField",name:"model",plural:!1,selections:[{alias:null,args:a,concreteType:"EmbeddingDimensionConnection",kind:"LinkedField",name:"embeddingDimensions",plural:!1,selections:[{alias:null,args:null,concreteType:"EmbeddingDimensionEdge",kind:"LinkedField",name:"edges",plural:!0,selections:[{alias:"embedding",args:null,concreteType:"EmbeddingDimension",kind:"LinkedField",name:"node",plural:!1,selections:[t,{alias:null,args:null,kind:"ScalarField",name:"name",storageKey:null},{alias:"euclideanDistance",args:[{kind:"Literal",name:"metric",value:"euclideanDistance"},{fields:[{kind:"Variable",name:"end",variableName:"endTime"},{kind:"Variable",name:"start",variableName:"startTime"}],kind:"ObjectValue",name:"timeRange"}],kind:"ScalarField",name:"driftMetric",storageKey:null}],storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"cursor",storageKey:null},{alias:null,args:null,concreteType:"EmbeddingDimension",kind:"LinkedField",name:"node",plural:!1,selections:[{alias:null,args:null,kind:"ScalarField",name:"__typename",storageKey:null},t],storageKey:null}],storageKey:null},{alias:null,args:null,concreteType:"PageInfo",kind:"LinkedField",name:"pageInfo",plural:!1,selections:[{alias:null,args:null,kind:"ScalarField",name:"endCursor",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"hasNextPage",storageKey:null}],storageKey:null}],storageKey:null},{alias:null,args:a,filters:null,handle:"connection",key:"ModelEmbeddingsTable_embeddingDimensions",kind:"LinkedHandle",name:"embeddingDimensions"}],storageKey:null}]},params:{cacheID:"fd1226f3c603a0c90b1c1657a894e691",id:null,metadata:{},name:"ModelEmbeddingsTableEmbeddingDimensionsQuery",operationKind:"query",text:`query ModelEmbeddingsTableEmbeddingDimensionsQuery(
  $count: Int = 50
  $cursor: String = null
  $endTime: DateTime!
  $startTime: DateTime!
) {
  ...ModelEmbeddingsTable_embeddingDimensions_4sIU9C
}

fragment ModelEmbeddingsTable_embeddingDimensions_4sIU9C on Query {
  model {
    embeddingDimensions(first: $count, after: $cursor) {
      edges {
        embedding: node {
          id
          name
          euclideanDistance: driftMetric(metric: euclideanDistance, timeRange: {start: $startTime, end: $endTime})
        }
        cursor
        node {
          __typename
          id
        }
      }
      pageInfo {
        endCursor
        hasNextPage
      }
    }
  }
}
`}}})();so.hash="fb7f125f75d1d33a555c16e198dbcbf8";const co=(function(){var n=["model","embeddingDimensions"];return{argumentDefinitions:[{defaultValue:50,kind:"LocalArgument",name:"count"},{defaultValue:null,kind:"LocalArgument",name:"cursor"},{defaultValue:null,kind:"LocalArgument",name:"endTime"},{defaultValue:null,kind:"LocalArgument",name:"startTime"}],kind:"Fragment",metadata:{connection:[{count:"count",cursor:"cursor",direction:"forward",path:n}],refetch:{connection:{forward:{count:"count",cursor:"cursor"},backward:null,path:n},fragmentPathInResult:[],operation:so}},name:"ModelEmbeddingsTable_embeddingDimensions",selections:[{alias:null,args:null,concreteType:"InferenceModel",kind:"LinkedField",name:"model",plural:!1,selections:[{alias:"embeddingDimensions",args:null,concreteType:"EmbeddingDimensionConnection",kind:"LinkedField",name:"__ModelEmbeddingsTable_embeddingDimensions_connection",plural:!1,selections:[{alias:null,args:null,concreteType:"EmbeddingDimensionEdge",kind:"LinkedField",name:"edges",plural:!0,selections:[{alias:"embedding",args:null,concreteType:"EmbeddingDimension",kind:"LinkedField",name:"node",plural:!1,selections:[{alias:null,args:null,kind:"ScalarField",name:"id",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"name",storageKey:null},{alias:"euclideanDistance",args:[{kind:"Literal",name:"metric",value:"euclideanDistance"},{fields:[{kind:"Variable",name:"end",variableName:"endTime"},{kind:"Variable",name:"start",variableName:"startTime"}],kind:"ObjectValue",name:"timeRange"}],kind:"ScalarField",name:"driftMetric",storageKey:null}],storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"cursor",storageKey:null},{alias:null,args:null,concreteType:"EmbeddingDimension",kind:"LinkedField",name:"node",plural:!1,selections:[{alias:null,args:null,kind:"ScalarField",name:"__typename",storageKey:null}],storageKey:null}],storageKey:null},{alias:null,args:null,concreteType:"PageInfo",kind:"LinkedField",name:"pageInfo",plural:!1,selections:[{alias:null,args:null,kind:"ScalarField",name:"endCursor",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"hasNextPage",storageKey:null}],storageKey:null}],storageKey:null}],storageKey:null}],type:"Query",abstractKey:null}})();co.hash="fb7f125f75d1d33a555c16e198dbcbf8";function xp(n){const{data:a}=M.usePaginationFragment(co,n.model),t=p.useMemo(()=>a.model.embeddingDimensions.edges.map(({embedding:i})=>({...i})),[a]),l=rn.useMemo(()=>[{header:"name",accessorKey:"name",cell:({row:r,renderValue:o})=>e(fa,{to:`embeddings/${r.original.id}`,children:o()})},{header:"euclidean distance",accessorKey:"euclideanDistance",cell:Kn}],[]);return e(fr,{columns:l,data:t})}const uo=p.createContext(null),y9=()=>{const n=p.useContext(uo);if(n===null)throw new Error("useTimeSlice must be used within a TimeSliceProvider");return n},Tp=({initialTimestamp:n,children:a})=>{const[t,l]=p.useState(n),i=r=>{p.startTransition(()=>{l(r)})};return e(uo.Provider,{value:{selectedTimestamp:t,setSelectedTimestamp:i},children:a})};function v9(){const n=I(t=>t.setPointSizeScale),a=I(t=>t.pointSizeScale);return s(ds,{placement:"bottom left",children:[e(is,{variant:"default",size:"compact",icon:e(ts,{svg:e(ls.OptionsOutline,{})}),"aria-label":"Display Settings"}),e(cs,{children:e(rs,{padding:"size-100",children:e(os,{direction:"column",gap:"size-100",children:e(ss,{label:"Point Scale",minValue:0,maxValue:3,step:.1,value:a,onChange:n})})})})]})}const Ml=m`
  display: flex;
  flex-direction: row;
  gap: var(--ac-global-dimension-static-size-50);
  align-items: center;
`;function C9(n){return typeof n=="string"&&n in kn}function k9(n){return s(Gn,{selectedKeys:[n.mode],"aria-label":"Canvas Mode",size:"S",onSelectionChange:a=>{if(a.size===0)return;const t=a.keys().next().value;if(C9(t))n.onChange(t);else throw new Error(`Unknown canvas mode: ${a}`)},children:[s(R,{delay:0,children:[e(Ce,{"aria-label":"Move",id:kn.move,children:s("div",{css:Ml,children:[e(T,{svg:e(Nc,{})})," Move"]})}),e(ke,{placement:"top",offset:10,children:"Move around the canvas using orbital controls"})]}),s(R,{delay:0,children:[e(Ce,{"aria-label":"Select",id:kn.select,children:s("div",{css:Ml,children:[e(T,{svg:e(Vc,{})})," Select"]})}),e(ke,{placement:"top",offset:10,children:"Select points using the lasso tool"})]})]})}function L9({radius:n}){const a=I(d=>d.eventIdToDataMap),t=I(d=>d.highlightedClusterId),l=I(d=>d.selectedClusterId),i=I(d=>d.clusters),{theme:r}=le(),o=I(d=>d.clusterColorMode),c=p.useMemo(()=>i.map(d=>{const{eventIds:u}=d,g=u.map(h=>{var b;return{position:(b=a.get(h))==null?void 0:b.position}}).filter(h=>h.position!==null);return{...d,data:g}}).filter(d=>d.data.length>0),[i,a]);return e(U,{children:c.map((d,u)=>{const g=S9({selected:d.id===l,highlighted:d.id===t,clusterColorMode:o});return e(H1,{data:d.data,opacity:g,wireframe:!0,pointRadius:n,color:w9({theme:r,clusterColorMode:o,index:u,clusterCount:c.length})},`${d.id}__opacity_${String(g)}`)})})}function w9({theme:n,clusterColorMode:a,index:t,clusterCount:l}){return a===Et.default?n==="dark"?"#999999":"#bbbbbb":ei(t/l)}function S9({selected:n,highlighted:a,clusterColorMode:t}){return t===Et.highlight?1:n?.7:a?.5:0}const x9=2;function T9({pointRadius:n}){const a=I(u=>u.hoveredEventId),t=I(u=>u.pointSizeScale),l=I(u=>u.eventIdToDataMap),i=I(u=>u.pointGroupColors),r=I(u=>u.eventIdToGroup);if(a==null||l==null)return null;const o=l.get(a),c=r[a],d=i[c];return o==null?null:e(j1,{position:o.position,args:[n*x9],scale:[t,t,t],children:e("meshMatcapMaterial",{color:d,opacity:.7,transparent:!0})})}const Fl=1;function A9(){const n=I(i=>i.hoveredEventId),a=I(i=>i.eventIdToDataMap),t=p.useRef(null);Z1((i,r)=>{t.current&&t.current.children.forEach(o=>o.children[0].material.uniforms.dashOffset.value-=r*5)});const l=p.useMemo(()=>{if(n==null)return[];const i=a.get(n);if(i==null)return[];const r=i.retrievals??[];return(r==null?void 0:r.length)===0?[]:r.map(c=>{const d=a.get(c.documentId);return d==null?null:[i.position,d.position]}).filter(c=>c!=null)},[a,n]);return e("group",{ref:t,children:l.map((i,r)=>s("group",{children:[e(Yt,{start:i[0],end:i[1],color:16777215,opacity:1,transparent:!0,dashed:!0,dashScale:50,gapSize:20,linewidth:Fl}),e(Yt,{start:i[0],end:i[1],color:16777215,linewidth:Fl/2,transparent:!0,opacity:.8})]},r))})}const I9=.5,z9=.5,M9=100,El=1.7;function Dl(n,a){return typeof a=="function"?a(n):a}function F9({primaryData:n,referenceData:a,corpusData:t,color:l,radius:i}){const r=I(_=>_.inferencesVisibility),o=I(_=>_.coloringStrategy),{theme:c}=le(),d=I(_=>_.setSelectedEventIds),u=I(_=>_.selectedEventIds),g=I(_=>_.setSelectedClusterId),h=I(_=>_.setHoveredEventId),f=I(_=>_.pointSizeScale),b=p.useMemo(()=>Hl(h,M9),[h]),y=p.useMemo(()=>o!==B.inferences?"cube":"sphere",[o]),v=p.useMemo(()=>o!==B.inferences?"octahedron":"sphere",[o]),k=p.useMemo(()=>c==="dark"?U1(I9):ni(z9),[c]),L=p.useMemo(()=>typeof l=="function"?_=>k(l(_)):k(l),[l,k]),E=p.useCallback(_=>!u.has(_.metaData.id)&&u.size>0?Dl(_,L):Dl(_,l),[u,l,L]),O=r.reference&&a,F=r.corpus&&t,D=p.useCallback(_=>{p.startTransition(()=>{d(new Set([_.metaData.id])),g(null)})},[g,d]),X=p.useCallback(_=>{_==null||_.metaData==null||b(_.metaData.id)},[b]),Y=p.useCallback(()=>{b(null)},[b]);return s(U,{children:[r.primary?e(Ea,{data:n,pointProps:{color:E,radius:i,scale:f},onPointClicked:D,onPointHovered:X,onPointerLeave:Y}):null,O?e(Ea,{data:a,pointProps:{color:E,radius:i,size:i?i*El:void 0,scale:f},onPointHovered:X,onPointerLeave:Y,pointShape:y,onPointClicked:D}):null,F?e(Ea,{data:t,pointProps:{color:E,radius:i,size:i?i*El:void 0,scale:f},onPointHovered:X,onPointerLeave:Y,pointShape:v,onPointClicked:D}):null]})}const E9=/\.(mp4|mov|webm|ogg)(\?|$)/i,D9=/\.(mp3|wav)(\?|$)/i;function _9(n){return E9.test(n)}function K9(n){return D9.test(n)}var nn=(n=>(n.square="square",n.circle="circle",n.diamond="diamond",n))(nn||{});const P9=()=>e("svg",{width:"12px",height:"12px",viewBox:"0 0 12 12",fill:"none",xmlns:"http://www.w3.org/2000/svg",children:e("rect",{width:"12",height:"12",rx:"1",fill:"currentColor"})}),V9=()=>e("svg",{width:"12px",height:"12px",viewBox:"0 0 12 12",fill:"none",xmlns:"http://www.w3.org/2000/svg",children:e("circle",{cx:"6",cy:"6",r:"6",fill:"currentColor"})}),R9=()=>e("svg",{width:"12px",height:"12px",viewBox:"0 0 12 12",fill:"none",xmlns:"http://www.w3.org/2000/svg",children:e("path",{d:"M6 0L12 6L6 12L0 6L6 0Z",fill:"currentColor"})});function go(n){const{shape:a,color:t}=n,l=p.useMemo(()=>{switch(a){case"square":return e(P9,{});case"circle":return e(V9,{});case"diamond":return e(R9,{});default:P()}},[a]);return e("i",{className:"shape-icon",style:{color:t},css:m`
        display: flex;
        flex-direction: row;
        align-items: center;
      `,"aria-hidden":!0,children:l})}function O9(n){const{rawData:a,linkToData:t,promptAndResponse:l,documentText:i}=n;return i!=null?"document":l!=null?"prompt_response":t!=null?_9(t)?"video":K9(t)?"audio":"image":a!=null?"raw":"event_metadata"}function N9(n,a){const{rawData:t}=a;switch(n){case"document":return null;case"prompt_response":return null;case"image":return t!=null?"raw":null;case"video":return t!=null?"raw":null;case"audio":return t!=null?"raw":null;case"raw":return"event_metadata";case"event_metadata":return null;default:P()}}function $9(n){const{onClick:a,onMouseOver:t,onMouseOut:l,color:i,size:r,inferencesName:o,group:c}=n,d=O9(n),u=r==="large"?N9(d,n):null;return s("div",{"data-testid":"event-item",role:"button","data-size":r,css:m`
        width: 100%;
        height: 100%;
        box-sizing: border-box;
        border-style: solid;
        border-radius: 4px;
        overflow: hidden;

        display: flex;
        flex-direction: column;
        cursor: pointer;
        overflow: hidden;

        border-width: 1px;
        border-color: ${i};
        border-radius: var(--ac-global-rounding-medium);
        transition: border-color 0.2s ease-in-out;
        transition: transform 0.2s ease-in-out;
        &:hover {
          transform: scale(1.04);
        }
        &[data-size="small"] {
          border-width: 2px;
        }
      `,onClick:a,onMouseOver:t,onMouseOut:l,children:[s("div",{className:"event-item__preview-wrap","data-size":r,css:m`
          display: flex;
          flex-direction: row;
          flex: 1 1 auto;
          overflow: hidden;
          & > *:nth-child(1) {
            flex: 1 1 auto;
            overflow: hidden;
          }
          & > *:nth-child(2) {
            flex: none;
            width: 43%;
          }
          &[data-size="large"] {
            & > *:nth-child(1) {
              margin: var(--ac-global-dimension-static-size-100);
              border-radius: 8px;
            }
          }
        `,children:[e(_l,{previewType:d,...n}),u!=null&&e(_l,{previewType:u,...n})]}),r!=="small"&&e(W9,{color:i,group:c,inferencesName:o,showInferences:r==="large"})]})}function _l(n){const{previewType:a}=n;let t=null;switch(a){case"document":{t=e(U9,{...n});break}case"prompt_response":{t=e(Z9,{...n});break}case"image":{t=e(B9,{...n});break}case"video":{t=e(H9,{...n});break}case"audio":{t=e(j9,{...n});break}case"raw":{t=e(G9,{...n});break}case"event_metadata":{t=e(Q9,{...n});break}default:P()}return t}function B9(n){return e("img",{src:n.linkToData||"[error] unexpected missing url",css:m`
        min-height: 0;
        // Maintain aspect ratio while having normalized height
        object-fit: contain;
        transition: background-color 0.2s ease-in-out;
        background-color: ${ht(.85,n.color)};
      `})}function H9(n){return e("video",{src:n.linkToData||"[error] unexpected missing url",css:m`
        min-height: 0;
        // Maintain aspect ratio while having normalized height
        object-fit: contain;
        transition: background-color 0.2s ease-in-out;
        background-color: ${ht(.85,n.color)};
      `})}function j9(n){return e("audio",{src:n.linkToData||"[error] unexpected missing url",autoPlay:n.autoPlay,controls:!0})}function Z9(n){var a,t;return s("div",{"data-size":n.size,css:m`
        --prompt-response-preview-background-color: var(
          --ac-global-color-grey-200
        );
        background-color: var(--prompt-response-preview-background-color);
        &[data-size="small"] {
          display: flex;
          flex-direction: column;
          padding: var(--ac-global-dimension-static-size-50);
          font-size: var(--ac-global-dimension-static-font-size-75);
          section {
            flex: 1 1 0;
            overflow: hidden;
            header {
              display: none;
            }
          }
        }
        &[data-size="medium"] {
          display: flex;
          flex-direction: column;
          gap: var(--ac-global-dimension-static-size-50);
          padding: var(--ac-global-dimension-static-size-100);
          section {
            flex: 1 1 0;
            overflow: hidden;
          }
        }
        &[data-size="large"] {
          display: flex;
          flex-direction: row;
          section {
            padding: var(--ac-global-dimension-static-size-50);
            flex: 1 1 0;
          }
        }
        & > section {
          position: relative;

          header {
            font-weight: bold;
            margin-bottom: var(--ac-global-dimension-static-size-50);
          }
          &:before {
            content: "";
            width: 100%;
            height: 100%;
            position: absolute;
            left: 0;
            top: 0;
            background: linear-gradient(
              transparent 80%,
              var(--prompt-response-preview-background-color) 100%
            );
          }
        }
      `,children:[s("section",{children:[e("header",{children:"prompt"}),(a=n.promptAndResponse)==null?void 0:a.prompt]}),s("section",{children:[e("header",{children:"response"}),(t=n.promptAndResponse)==null?void 0:t.response]})]})}function U9(n){return e("p",{"data-size":n.size,css:m`
        flex: 1 1 auto;
        padding: var(--ac-global-dimension-static-size-100);
        margin-block-start: 0;
        margin-block-end: 0;
        position: relative;
        --text-preview-background-color: var(--ac-global-color-grey-100);
        background-color: var(--text-preview-background-color);

        &[data-size="small"] {
          padding: var(--ac-global-dimension-static-size-50);
          box-sizing: border-box;
        }
        &:before {
          content: "";
          width: 100%;
          height: 100%;
          position: absolute;
          left: 0;
          top: 0;
          background: linear-gradient(
            transparent 90%,
            var(--text-preview-background-color) 98%,
            var(--text-preview-background-color) 100%
          );
        }
      `,children:n.documentText})}function G9(n){return e("p",{"data-size":n.size,css:m`
        flex: 1 1 auto;
        padding: var(--ac-global-dimension-static-size-100);
        margin-block-start: 0;
        margin-block-end: 0;
        position: relative;
        --text-preview-background-color: var(--ac-background-color-light);
        background-color: var(--text-preview-background-color);

        &[data-size="small"] {
          padding: var(--ac-global-dimension-static-size-50);
          font-size: var(--ac-global-color-gray-600);
          box-sizing: border-box;
        }
        &:before {
          content: "";
          width: 100%;
          height: 100%;
          position: absolute;
          left: 0;
          top: 0;
          background: linear-gradient(
            transparent 90%,
            var(--text-preview-background-color) 98%,
            var(--text-preview-background-color) 100%
          );
        }
      `,children:n.rawData})}function Q9(n){return s("dl",{css:m`
        margin: 0;
        padding: var(--ac-global-dimension-static-size-200);
        display: flex;
        flex-direction: column;
        justify-content: center;
        gap: var(--ac-global-dimension-static-size-100);

        dt {
          font-weight: bold;
        }
        dd {
          margin-inline-start: var(--ac-global-dimension-static-size-100);
        }
      `,children:[s("div",{children:[e("dt",{children:"prediction label"}),e("dd",{children:n.predictionLabel||"--"})]}),s("div",{children:[e("dt",{children:"actual label"}),e("dd",{children:n.actualLabel||"--"})]})]})}function W9({color:n,group:a,showInferences:t,inferencesName:l}){return s("footer",{css:m`
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        padding: var(--ac-global-dimension-static-size-50)
          var(--ac-global-dimension-static-size-100)
          var(--ac-global-dimension-static-size-50) 7px;
        border-top: 1px solid var(--ac-global-border-color-dark);
      `,children:[s("div",{css:m`
          display: flex;
          flex-direction: row;
          align-items: center;
          gap: var(--ac-global-dimension-static-size-50);
        `,children:[e(go,{shape:nn.circle,color:n}),a]}),t?e("div",{title:"the inferences the point belongs to",children:l}):null]})}const Fn=200,na=10,q9=new Ps,X9=()=>{const{getInferencesNameByRole:n}=ha(),a=I(f=>f.hoveredEventId),t=I(f=>f.eventIdToDataMap),l=I(f=>f.pointData),i=I(f=>f.pointGroupColors),r=I(f=>f.eventIdToGroup);if(a==null||l==null||l==null)return null;const o=t.get(a),c=l[a];if(o==null||c==null)return null;const d=r[a],u=i[r[a]],g=qi(a),h=n(g);return e(G1,{position:o.position,pointerEvents:"none",zIndexRange:[0,1],calculatePosition:(f,b,y)=>{const v=q9.setFromMatrixPosition(f.matrixWorld);v.project(b);const k=y.width/2,L=y.height/2;return[Math.min(y.width-Fn-na,Math.max(0,v.x*k+k+na)),Math.min(y.height-Fn-na,Math.max(0,-(v.y*L)+L+na))]},children:e("div",{css:m`
          --grid-item-min-width: ${Fn}px;
          width: ${Fn}px;
          height: ${Fn}px;
          background-color: var(--ac-global-background-color-dark);
          border-radius: var(--ac-global-rounding-medium);
        `,children:e($9,{rawData:o.embeddingMetadata.rawData,linkToData:o.embeddingMetadata.linkToData,predictionLabel:o.eventMetadata.predictionLabel,actualLabel:o.eventMetadata.actualLabel,promptAndResponse:c.promptAndResponse,documentText:c.documentText,inferencesName:h,group:d,color:u,size:"medium",autoPlay:!0})})})},Y9=300,J9=3,e6=.2,n6=function(){const{selectedTimestamp:a}=y9(),t=I(d=>d.points),l=I(d=>d.hdbscanParameters),i=I(d=>d.umapParameters),[r,o,c]=p.useMemo(()=>{const{primaryEventIds:d,referenceEventIds:u,corpusEventIds:g}=Ft(t.map(h=>h.eventId));return[d.length,u.length,g.length]},[t]);return a?s("section",{css:m`
        width: 300px;
      `,children:[e(ne,{level:2,weight:"heavy",style:{marginBottom:8},children:"Point Cloud Summary"}),s("dl",{css:Qa,children:[s("div",{children:[e("dt",{children:"Timestamp"}),e("dd",{children:en(a)})]}),s("div",{children:[e("dt",{children:"primary points"}),e("dd",{children:r})]}),o>0?s("div",{children:[e("dt",{children:"reference points"}),e("dd",{children:o})]}):null,c>0?s("div",{children:[e("dt",{children:"corpus points"}),e("dd",{children:c})]}):null]}),e("br",{}),e(ne,{level:4,weight:"heavy",children:"Clustering Parameters"}),s("dl",{css:Qa,children:[s("div",{children:[e("dt",{children:"min cluster size"}),e("dd",{children:l.minClusterSize})]}),s("div",{children:[e("dt",{children:"cluster min samples"}),e("dd",{children:l.clusterMinSamples})]}),s("div",{children:[e("dt",{children:"cluster selection epsilon"}),e("dd",{children:l.clusterSelectionEpsilon})]})]}),e("br",{}),e(ne,{level:4,weight:"heavy",children:"UMAP Parameters"}),s("dl",{css:Qa,children:[s("div",{children:[e("dt",{children:"min distance"}),e("dd",{children:i.minDist})]}),s("div",{children:[e("dt",{children:"n neighbors"}),e("dd",{children:i.nNeighbors})]}),s("div",{children:[e("dt",{children:"n samples per inferences"}),e("dd",{children:i.nSamples})]})]})]}):null},Qa=m`
  margin: 0;
  padding: 0;
  div {
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
    gap: var(--ac-global-dimension-static-size-50);
  }
`;function a6(){const n=I(t=>t.canvasMode),a=I(t=>t.setCanvasMode);return s("div",{css:m`
        position: absolute;
        left: var(--ac-global-dimension-static-size-100);
        top: var(--ac-global-dimension-static-size-100);
        z-index: 1;
        display: flex;
        flex-direction: row;
        align-items: center;
        gap: var(--ac-global-dimension-static-size-100);
      `,children:[e(k9,{mode:n,onChange:a}),e(v9,{}),e(t6,{})]})}function t6(){return s(R,{delay:0,children:[e(z,{size:"S",leadingVisual:e(T,{svg:e(St,{})}),"aria-label":"Information bout the point-cloud display"}),e(ie,{placement:"bottom left",children:e(n6,{})})]})}function l6({children:n}){const{theme:a}=le();return e("div",{css:m`
        flex: 1 1 auto;
        height: 100%;
        position: relative;
        &[data-theme="dark"] {
          background: linear-gradient(
            rgb(21, 25, 31) 11.4%,
            rgb(11, 12, 14) 70.2%
          );
        }
        &[data-theme="light"] {
          background: linear-gradient(#f2f6fd 0%, #dbe6fc 74%);
        }
      `,"data-theme":a,children:n})}function Ap(){return s(l6,{children:[e(a6,{},"canvas-tools"),e(i6,{},"projection")]})}const i6=p.memo(function(){const a=I(A=>A.points),t=I(A=>A.canvasMode),l=I(A=>A.setSelectedEventIds),i=I(A=>A.setSelectedClusterId),r=I(A=>A.pointGroupColors),o=I(A=>A.pointGroupVisibility),{theme:c}=le(),d=I(A=>A.inferencesVisibility),[u,g]=p.useState(!0),h=p.useMemo(()=>Q1(a.map(A=>A.position)),[a]),f=(h.maxX-h.minX+(h.maxY-h.minY))/2/Y9,b=f*J9,y=t===kn.move,v=I(A=>A.eventIdToGroup),k=p.useCallback(A=>{const H=v[A.metaData.id]||"unknown";return r[H]||gn},[r,v]),L=p.useMemo(()=>a.filter(A=>A.eventId.includes("PRIMARY")),[a]),E=p.useMemo(()=>a.filter(A=>A.eventId.includes("REFERENCE")),[a]),O=p.useMemo(()=>a.filter(A=>A.eventId.includes("CORPUS")),[a]),F=p.useMemo(()=>L.filter(A=>{const H=v[A.eventId];return o[H]}),[L,v,o]),D=p.useMemo(()=>!E||E.length===0?null:E.filter(A=>{const H=v[A.eventId];return o[H]}),[E,v,o]),X=p.useMemo(()=>O.filter(A=>{const H=v[A.eventId];return o[H]}),[O,v,o]),Y=p.useMemo(()=>{const A=d.primary?F:[],H=d.reference?D:[],oe=d.corpus?X:[];return[...A,...H||[],...oe||[]]},[F,D,X,d]),_=W1(vt,yt,ns,Mt);return e(es,{camera:{position:[3,3,3]},children:s(_,{children:[e(q1,{autoRotate:u,autoRotateSpeed:2,enableRotate:y,enablePan:y,onEnd:()=>{g(!1)}}),s(X1,{bounds:h,boundsZoomPaddingFactor:e6,children:[e(Y1,{points:Y,onChange:A=>{l(new Set(A.map(H=>H.metaData.id))),i(null)},enabled:t===kn.select}),e(J1,{size:(h.maxX-h.minX)/4,color:c=="dark"?"#fff":"#505050"}),e(F9,{primaryData:F,referenceData:D,corpusData:X,color:k,radius:f}),e(L9,{radius:b}),e(X9,{}),e(T9,{pointRadius:f}),e(A9,{})]})]})})}),mo=(function(){var n=[{alias:null,args:null,concreteType:"InferenceModel",kind:"LinkedField",name:"model",plural:!1,selections:[{alias:null,args:null,concreteType:"DimensionConnection",kind:"LinkedField",name:"dimensions",plural:!1,selections:[{alias:null,args:null,concreteType:"DimensionEdge",kind:"LinkedField",name:"edges",plural:!0,selections:[{alias:null,args:null,concreteType:"Dimension",kind:"LinkedField",name:"node",plural:!1,selections:[{alias:null,args:null,kind:"ScalarField",name:"id",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"name",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"type",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"dataType",storageKey:null}],storageKey:null}],storageKey:null}],storageKey:null}],storageKey:null}];return{fragment:{argumentDefinitions:[],kind:"Fragment",metadata:null,name:"DimensionPickerQuery",selections:n,type:"Query",abstractKey:null},kind:"Request",operation:{argumentDefinitions:[],kind:"Operation",name:"DimensionPickerQuery",selections:n},params:{cacheID:"56e356d226d322dabfd9db8010884e4f",id:null,metadata:{},name:"DimensionPickerQuery",operationKind:"query",text:`query DimensionPickerQuery {
  model {
    dimensions {
      edges {
        node {
          id
          name
          type
          dataType
        }
      }
    }
  }
}
`}}})();mo.hash="747256fac1de97803ae6f96e3cb58d98";function r6(n){const{type:a}=n;let t="gray",l="";switch(a){case"feature":t="blue",l="FEA";break;case"tag":t="purple",l="TAG";break;case"prediction":t="white",l="PRE";break;case"actual":t="orange",l="ACT";break;default:P()}return e(je,{color:t,"aria-Token":a,title:"type",children:l})}const o6=s(gs,{children:[e(ne,{weight:"heavy",level:4,children:"Model Dimension"}),e(us,{children:e(C,{children:"A dimension is a feature, tag, prediction, or actual value that is associated with a model inference. Features represent inputs, tags represent metadata, predictions represent outputs, and actuals represent ground truth."})})]});function s6(n){const{selectedDimension:a,dimensions:t,onChange:l,isLoading:i}=n;return s("div",{children:[s(S,{direction:"row",alignItems:"center",gap:"size-25",children:[e(K,{children:"Dimension"}),o6]}),s(Ne,{defaultSelectedKey:a?a.name:void 0,"aria-label":"Select a dimension",onSelectionChange:r=>{const o=t.find(c=>c.name===r);o&&p.startTransition(()=>l(o))},isDisabled:i,"data-testid":"dimension-picker",children:[s(z,{children:[e(Oe,{}),e(Ae,{})]}),e(ue,{children:e(we,{children:t.map(r=>e(ee,{id:r.name,children:s(S,{direction:"row",alignItems:"center",gap:"size-100",children:[e(r6,{type:r.type}),r.name]})},r.name))})})]})]})}function c6(n){const[a,t]=p.useState([]),[l,i]=p.useState(!0),{selectedDimension:r,onChange:o}=n;return p.useEffect(()=>{M.fetchQuery(Qn,mo,{},{fetchPolicy:"store-or-network"}).toPromise().then(c=>{const d=(c==null?void 0:c.model.dimensions.edges.map(u=>u.node))??[];t(d),i(!1)})},[]),e(s6,{onChange:o,dimensions:a,selectedDimension:r,isLoading:l})}function d6(n){return typeof n=="string"&&n in B}const u6=Object.values(B);function g6(n){const{strategy:a,onChange:t}=n;return s(Ne,{defaultSelectedKey:a,"aria-label":"Coloring strategy",onSelectionChange:l=>{d6(l)&&t(l)},children:[e(K,{children:"Color By"}),s(z,{children:[e(Oe,{}),e(Ae,{})]}),e(C,{slot:"description",children:""}),e(ue,{children:e(we,{children:u6.map(l=>e(ee,{id:l,children:l},l))})})]})}const m6=m`
  display: flex;
  flex-direction: row;
  gap: var(--ac-global-dimension-size-50);
  align-items: center;
`;function aa(n){const{name:a,checked:t,onChange:l,color:i,iconShape:r=nn.circle}=n;return s("label",{css:m6,children:[e("input",{type:"checkbox",checked:t,name:a,onChange:l}),e(go,{shape:r,color:i}),a]},a)}function p6({hasReference:n,hasCorpus:a}){const t=I(f=>f.inferencesVisibility),l=I(f=>f.setInferencesVisibility),i=I(f=>f.coloringStrategy),r=p.useCallback(f=>{const{name:b,checked:y}=f.target;l({...t,[b]:y})},[t,l]),o=Ts(),c=p.useMemo(()=>{switch(i){case B.inferences:return o[0];case B.correctness:case B.dimension:return He;default:P()}},[i,o]),d=p.useMemo(()=>{switch(i){case B.inferences:return o[1];case B.correctness:case B.dimension:return He;default:P()}},[i,o]),u=He,g=i===B.inferences?nn.circle:nn.square,h=i===B.inferences?nn.circle:nn.diamond;return s("form",{css:m`
        display: flex;
        flex-direction: column;
        padding: var(--ac-global-dimension-static-size-100);
      `,children:[e(aa,{checked:t.primary,name:"primary",color:c,onChange:r}),n?e(aa,{checked:t.reference,name:"reference",onChange:r,color:d,iconShape:g}):null,a?e(aa,{checked:t.corpus,name:"corpus",onChange:r,color:u,iconShape:h}):null]})}function h6(){const n=I(r=>r.pointGroupVisibility),a=I(r=>r.setPointGroupVisibility),t=I(r=>r.pointGroupColors),l=p.useMemo(()=>Object.keys(n),[n]),i=p.useCallback(r=>{const{name:o,checked:c}=r.target;a({...n,[o]:c})},[n,a]);return s("form",{css:m`
        display: flex;
        flex-direction: column;
      `,children:[e(f6,{}),e("div",{css:m`
          padding: var(--ac-global-dimension-static-size-100);
        `,children:l.map(r=>{const o=n[r],c=t[r];return e(aa,{name:r,checked:o,color:c,onChange:i},r)})})]})}function f6(){const n=I(r=>r.pointGroupVisibility),a=I(r=>r.setPointGroupVisibility),t=I(r=>r.coloringStrategy),l=p.useMemo(()=>Object.values(n).every(r=>!r),[n]),i=p.useCallback(r=>{const{checked:o}=r.target,c=Object.keys(n).reduce((d,u)=>(d[u]=o,d),{});a(c)},[n,a]);return s("label",{css:()=>m`
        display: flex;
        flex-direction: row;
        gap: var(--ac-global-dimension-size-50);
        padding: var(--ac-global-dimension-static-size-50)
          var(--ac-global-dimension-static-size-100);
        background-color: var(--ac-global-background-color-light);
      `,children:[e("input",{type:"checkbox",checked:!l,onChange:i}),`${t}`]})}function Ip(){const{referenceInferences:n,corpusInferences:a}=ha(),t=I(h=>h.coloringStrategy),l=I(h=>h.setColoringStrategy),i=I(h=>h.dimension),r=I(h=>h.dimensionMetadata),o=I(h=>h.setDimension),c=n!=null||a!=null,d=t===B.dimension&&i==null,u=t===B.dimension&&i!=null&&r==null,g=t!==B.inferences&&!d&&!u;return s("section",{css:m`
        & > .ac-form {
          padding: var(--ac-global-dimension-static-size-100)
            var(--ac-global-dimension-static-size-100) 0
            var(--ac-global-dimension-static-size-100);
        }
        & > .ac-alert {
          margin: var(--ac-global-dimension-static-size-100);
        }
      `,children:[e(ms,{children:s(U,{children:[e(g6,{strategy:t,onChange:l}),t===B.dimension?e(c6,{selectedDimension:null,onChange:h=>{o(h)}}):null]})}),c?e(p6,{hasReference:n!=null,hasCorpus:a!=null}):null,g?e(h6,{}):null,d?e(ya,{variant:"info",showIcon:!1,children:"Please select a dimension to color the point cloud by"}):null,u?e("div",{css:m`
            padding: var(--ac-global-dimension-static-size-100);
            min-height: 100px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
          `,children:e(re,{message:"Calculating point colors"})}):null]})}function b6(n){return typeof n=="string"&&n in yn}function zp(n){return s(Gn,{selectedKeys:[n.mode],size:"S",onSelectionChange:a=>{if(a.size===0)return;const t=a.keys().next().value;if(b6(t))n.onChange(t);else throw new Error(`Unknown view mode: ${t}`)},children:[e(Ce,{"aria-label":"List",id:yn.list,children:e(T,{svg:e(Ti,{})})}),e(Ce,{"aria-label":"Grid",id:yn.gallery,children:e(T,{svg:e(xi,{})})})]})}function Mp(n){const{driftRatio:a,primaryToCorpusRatio:t,clusterId:l,isSelected:i,onClick:r,onMouseEnter:o,onMouseLeave:c,metricName:d,primaryMetricValue:u,referenceMetricValue:g,hideReference:h}=n,{percentage:f,comparisonInferencesRole:b}=p.useMemo(()=>typeof t=="number"?{percentage:(t+1)/2*100,comparisonInferencesRole:Te.corpus}:typeof a=="number"?{percentage:(a+1)/2*100,comparisonInferencesRole:Te.reference}:{percentage:100,comparisonInferencesRole:null},[a,t]);return s("div",{css:m`
        border: 1px solid var(--ac-global-border-color-light);
        border-radius: var(--ac-global-rounding-medium);
        overflow: hidden;
        transition: background-color 0.2s ease-in-out;
        cursor: pointer;
        &:hover {
          background-color: var(--ac-global-color-primary-700);
          border-color: var(--ac-global-color-primary);
        }
        &.is-selected {
          border-color: var(--ac-global-color-primary);
          background-color: var(--ac-global-color-primary-700);
        }
      `,className:i?"is-selected":"",role:"button",onClick:r,onMouseEnter:o,onMouseLeave:c,children:[s("div",{css:m`
          padding: var(--ac-global-dimension-static-size-100);
          display: flex;
          flex-direction: row;
          justify-content: space-between;
          align-items: center;
        `,children:[e(S,{"data-testid":"cluster-description",direction:"column",gap:"size-50",alignItems:"start",children:s(S,{direction:"column",alignItems:"start",children:[e(ne,{level:3,children:`Cluster ${l}`}),e(C,{color:"text-700",size:"XS",children:`${n.numPoints} points`})]})}),s("div",{"data-testid":"cluster-metric",css:m`
            display: flex;
            flex-direction: column;
            align-items: end;
          `,children:[e(C,{color:"text-700",size:"XS",children:d}),e(C,{color:"text-900",size:"S",children:Ll(u)}),h?null:e(C,{color:"purple-800",size:"XS",children:Ll(g)})]})]}),e(y6,{primaryPercentage:f,comparisonInferencesRole:b})]})}function y6({primaryPercentage:n,comparisonInferencesRole:a}){return s("div",{"data-testid":"inferences-distribution",css:m`
        display: flex;
        flex-direction: row;
      `,children:[e("div",{"data-testid":"primary-distribution",css:m`
          background-image: linear-gradient(
            to right,
            var(--px-primary-color--transparent) 0%,
            var(--px-primary-color)
          );
          height: var(--px-gradient-bar-height);
          width: ${n}%;
        `}),e("div",{"data-testid":"reference-distribution","data-reference-inferences-role":`${a??"none"}`,css:m`
          &[data-reference-inferences-role="reference"] {
            background-image: linear-gradient(
              to right,
              var(--px-reference-color) 0%,
              var(--px-reference-color--transparent)
            );
          }
          &[data-reference-inferences-role="corpus"] {
            background-image: linear-gradient(
              to right,
              var(--px-corpus-color) 0%,
              var(--px-corpus-color--transparent)
            );
          }

          height: var(--px-gradient-bar-height);
          width: ${100-n}%;
        `})]})}function Fp(){const n=I(d=>d.umapParameters),a=I(d=>d.setUMAPParameters),{handleSubmit:t,control:l,setError:i,formState:{isDirty:r,isValid:o}}=Re({reValidateMode:"onChange",defaultValues:n}),c=p.useCallback(d=>{const u=parseFloat(d.minDist);if(u<Ka||u>Pa){i("minDist",{message:`must be between ${Ka} and ${Pa}`});return}a({minDist:u,nNeighbors:parseInt(d.nNeighbors,10),nSamples:parseInt(d.nSamples,10)})},[a,i]);return e("section",{css:m`
        & > .ac-form {
          padding: var(--ac-global-dimension-static-size-100)
            var(--ac-global-dimension-static-size-100) 0
            var(--ac-global-dimension-static-size-100);
        }
      `,children:e(on,{onSubmit:t(c),children:s(w,{padding:"size-100",children:[e($,{name:"minDist",control:l,rules:{required:"field is required"},render:({field:{onChange:d,onBlur:u,value:g},fieldState:{invalid:h,error:f}})=>s(Q,{type:"number",isInvalid:h,onChange:b=>d(parseFloat(b)),onBlur:u,value:g.toString(),size:"S",children:[e(K,{children:"min distance"}),e(j,{step:.01,min:Ka,max:Pa}),f?e(W,{children:f.message}):e(C,{slot:"description",children:"how tightly to pack points"})]})}),e($,{name:"nNeighbors",control:l,rules:{required:"n neighbors is required",min:{value:Da,message:`greater than or equal to ${Da}`},max:{value:_a,message:`less than or equal to ${_a}`}},render:({field:d,fieldState:{invalid:u,error:g}})=>s(Q,{type:"number",isInvalid:u,...d,value:d.value,size:"S",children:[e(K,{children:"n neighbors"}),e(j,{step:.01,min:Da,max:_a}),g?e(W,{children:g.message}):e(C,{slot:"description",children:"Balances local versus global structure"})]})}),e($,{name:"nSamples",control:l,rules:{required:"n samples is required",max:{value:nl,message:`must be below ${nl}`},min:{value:el,message:`must be above ${el}`}},render:({field:{onChange:d,onBlur:u,value:g},fieldState:{invalid:h,error:f}})=>s(Q,{type:"number",isInvalid:h,onChange:b=>d(parseInt(b,10)),onBlur:u,value:g.toString(),size:"S",children:[e(K,{children:"n samples"}),e(j,{}),f?e(W,{children:f.message}):e(C,{slot:"description",children:"number of points to use per inferences"})]})}),e(z,{variant:r?"primary":"default",type:"submit",isDisabled:!o,css:m`
              width: 100%;
              margin-top: var(--ac-global-dimension-static-size-100);
            `,children:"Apply UMAP Parameters"})]})})})}function Ep(){const n=I(u=>u.hdbscanParameters),a=I(u=>u.setHDBSCANParameters),t=I(u=>u.clustersLoading),{control:l,handleSubmit:i,formState:{isDirty:r,isValid:o},reset:c}=Re({defaultValues:n}),d=p.useCallback(u=>{const g={minClusterSize:parseInt(u.minClusterSize,10),clusterMinSamples:parseInt(u.clusterMinSamples,10),clusterSelectionEpsilon:parseFloat(u.clusterSelectionEpsilon)};a(g),c(g)},[a,c]);return e("section",{css:m`
        & > .ac-form {
          padding: var(--ac-global-dimension-static-size-100)
            var(--ac-global-dimension-static-size-100) 0
            var(--ac-global-dimension-static-size-100);
        }
      `,children:e(on,{onSubmit:i(d),children:s(w,{padding:"size-100",children:[e($,{name:"minClusterSize",control:l,rules:{required:"field is required",min:{value:$s,message:"must be greater than 1"},max:{value:Ga,message:"must be less than 2,147,483,647"}},render:({field:{onChange:u,onBlur:g,value:h},fieldState:{invalid:f,error:b}})=>s(Q,{type:"number",isInvalid:f,onChange:y=>u(parseInt(y,10)),onBlur:g,value:h.toString(),size:"S",children:[e(K,{children:"Min Cluster Size"}),e(j,{}),b?e(W,{children:b.message}):e(C,{slot:"description",children:"The smallest size for a cluster."})]})}),e($,{name:"clusterMinSamples",control:l,rules:{required:"field is required",min:{value:al,message:`must be greater than ${al}`},max:{value:Ga,message:"must be less than 2,147,483,647"}},render:({field:{onBlur:u,onChange:g,value:h},fieldState:{invalid:f,error:b}})=>s(Q,{type:"number",isInvalid:f,onChange:y=>g(parseInt(y,10)),onBlur:u,value:h.toString(),size:"S",children:[e(K,{children:"Cluster Minimum Samples"}),e(j,{}),b?e(W,{children:b.message}):e(C,{slot:"description",children:"Determines if a point is a core point"})]})}),e($,{name:"clusterSelectionEpsilon",control:l,rules:{required:"field is required",min:{value:0,message:"must be a non-negative number"},max:{value:Ga,message:"must be less than 2,147,483,647"}},render:({field:{onBlur:u,onChange:g,value:h},fieldState:{invalid:f,error:b}})=>s(Q,{type:"number",isInvalid:f,onChange:y=>g(parseInt(y,10)),onBlur:u,value:h.toString(),size:"S",children:[e(K,{children:"Cluster Selection Epsilon"}),e(j,{}),b?e(W,{children:b.message}):e(C,{slot:"description",children:"A distance threshold"})]})}),e(z,{variant:r?"primary":"default",type:"submit",isDisabled:!o||t,css:m`
              width: 100%;
              margin-top: var(--ac-global-dimension-static-size-100);
            `,children:t?"Applying...":"Apply Clustering Config"})]})})})}function v6(n){return typeof n=="string"&&n in hn}function Dp(n){return s(Gn,{selectedKeys:[n.size],size:"S","aria-label":"Selection Grid Size",onSelectionChange:a=>{if(a.size===0)return;const t=a.keys().next().value;if(v6(t))n.onChange(t);else throw new Error(`Unknown grid size: ${t}`)},children:[e(Ce,{"aria-label":"Small",id:hn.small,children:"S"}),e(Ce,{"aria-label":"Medium",id:hn.medium,children:"M"}),e(Ce,{"aria-label":"Large",id:hn.large,children:"L"})]})}function C6(n){const{value:a}=n;return s("div",{className:"typescript-code-block",css:mr,children:[e(Ct,{text:a}),e(w3,{value:a})]})}const Zt="https://app.phoenix.arize.com",k6="https://llamatrace.com",L6=[Zt,k6],po=L6.includes(Tn),ut=()=>s("svg",{width:"32",height:"32",viewBox:"0 0 32 32",fill:"none",xmlns:"http://www.w3.org/2000/svg",children:[e("rect",{x:"0.25",y:"0.25",width:"31.5",height:"31.5"}),e("g",{mask:"url(#mask0_1112_37116)",children:e("path",{d:"M26.2795 13.8229C26.824 12.1886 26.6365 10.3984 25.7657 8.91186C24.4562 6.63186 21.8237 5.45886 19.2527 6.01086C18.109 4.72236 16.4657 3.98961 14.743 4.00011C12.115 3.99411 9.78324 5.68611 8.97474 8.18661C7.28649 8.53236 5.82924 9.58911 4.97649 11.0869C3.65724 13.3609 3.95799 16.2274 5.72049 18.1774C5.17599 19.8116 5.36349 21.6019 6.23424 23.0884C7.54374 25.3684 10.1762 26.5414 12.7472 25.9894C13.8902 27.2779 15.5342 28.0106 17.257 27.9994C19.8865 28.0061 22.219 26.3126 23.0275 23.8099C24.7157 23.4641 26.173 22.4074 27.0257 20.9096C28.3435 18.6356 28.042 15.7714 26.2802 13.8214L26.2795 13.8229ZM17.2585 26.4311C16.2062 26.4326 15.187 26.0644 14.3792 25.3901C14.416 25.3706 14.4797 25.3354 14.521 25.3099L19.3 22.5499C19.5445 22.4111 19.6945 22.1509 19.693 21.8696V15.1324L21.7127 16.2986C21.7345 16.3091 21.7487 16.3301 21.7517 16.3541V21.9334C21.7487 24.4144 19.7395 26.4259 17.2585 26.4311ZM7.59549 22.3039C7.06824 21.3934 6.87849 20.3261 7.05924 19.2904C7.09449 19.3114 7.15674 19.3496 7.20099 19.3751L11.98 22.1351C12.2222 22.2769 12.5222 22.2769 12.7652 22.1351L18.5995 18.7661V21.0986C18.601 21.1226 18.5897 21.1459 18.571 21.1609L13.7402 23.9501C11.5885 25.1891 8.84049 24.4526 7.59624 22.3039H7.59549ZM6.33774 11.8721C6.86274 10.9601 7.69149 10.2626 8.67849 9.90036C8.67849 9.94161 8.67624 10.0144 8.67624 10.0654V15.5861C8.67474 15.8666 8.82474 16.1269 9.06849 16.2656L14.9027 19.6339L12.883 20.8001C12.8627 20.8136 12.8372 20.8159 12.8147 20.8061L7.98324 18.0146C5.83599 16.7711 5.09949 14.0239 6.33699 11.8729L6.33774 11.8721ZM22.9322 15.7339L17.098 12.3649L19.1177 11.1994C19.138 11.1859 19.1635 11.1836 19.186 11.1934L24.0175 13.9826C26.1685 15.2254 26.9057 17.9771 25.663 20.1281C25.1372 21.0386 24.3092 21.7361 23.323 22.0991V16.4134C23.3252 16.1329 23.176 15.8734 22.933 15.7339H22.9322ZM24.9422 12.7084C24.907 12.6866 24.8447 12.6491 24.8005 12.6236L20.0215 9.86361C19.7792 9.72186 19.4792 9.72186 19.2362 9.86361L13.402 13.2326V10.9001C13.4005 10.8761 13.4117 10.8529 13.4305 10.8379L18.2612 8.05086C20.413 6.80961 23.164 7.54836 24.4045 9.70086C24.9287 10.6099 25.1185 11.6741 24.9407 12.7084H24.9422ZM12.304 16.8656L10.2835 15.6994C10.2617 15.6889 10.2475 15.6679 10.2445 15.6439V10.0646C10.246 7.58061 12.2612 5.56761 14.7452 5.56911C15.796 5.56911 16.813 5.93811 17.6207 6.61011C17.584 6.62961 17.521 6.66486 17.479 6.69036L12.7 9.45036C12.4555 9.58911 12.3055 9.84861 12.307 10.1299L12.304 16.8641V16.8656ZM13.4012 14.5001L16 12.9994L18.5987 14.4994V17.5001L16 19.0001L13.4012 17.5001V14.5001Z",fill:"var(--ac-global-text-color-900)"})})]}),w6=()=>s("svg",{width:"32",height:"32",viewBox:"0 0 32 32",fill:"none",xmlns:"http://www.w3.org/2000/svg",children:[e("path",{d:"M24.3968 1.6001H7.60314C4.28768 1.6001 1.59998 4.28781 1.59998 7.60326V24.3969C1.59998 27.7124 4.28768 30.4001 7.60314 30.4001H24.3968C27.7123 30.4001 30.4 27.7124 30.4 24.3969V7.60326C30.4 4.28781 27.7123 1.6001 24.3968 1.6001Z",fill:"black"}),e("path",{d:"M20.4595 22.9326C20.3942 22.8597 20.3287 22.7869 20.2634 22.7142C19.8027 22.2107 19.5742 21.6292 19.7557 20.8584C18.0112 21.4241 16.3359 21.5521 14.6059 21.1564C14.5605 21.6739 14.5424 22.1469 14.4722 22.6121C14.3864 23.1814 14.2552 23.7437 14.1477 24.3097C14.1102 24.5069 14.069 24.7054 14.0567 24.9049C14.02 25.4989 14.0332 26.0987 13.9532 26.6862C13.912 26.9884 13.7144 27.2694 13.5982 27.535H12.303L12.31 27.5189C12.3792 27.3307 12.4482 27.1426 12.5174 26.9544L12.5139 26.9589C12.5839 26.8887 12.6537 26.8184 12.7237 26.7482L12.7192 26.7527C12.7545 26.7172 12.7899 26.6819 12.8252 26.6464L13.0159 26.6244C13.0344 26.3096 13.0315 26.4252 13.0344 26.3096C13.0482 25.7476 13.04 25.184 13.0099 24.6227C12.9987 24.4167 12.9055 24.215 12.8499 24.0114C12.8112 24.0124 12.7725 24.0134 12.7339 24.0144C12.5274 24.7594 12.3209 25.5046 12.1144 26.2496L12.1235 26.2456C11.9757 26.5136 11.7677 27.0334 11.6199 27.3014C11.436 27.318 10.9177 27.2861 10.4885 27.2886C10.5235 26.9346 10.6549 26.7491 10.878 26.5487C11.3579 26.118 11.487 25.4862 11.4852 24.8812C11.4827 24.0362 11.3699 23.1917 11.3042 22.3469C11.3974 22.1771 11.4514 21.9604 11.5899 21.8451C12.5272 21.0642 13.2919 20.1312 14.0057 19.1537C14.6967 18.2074 15.3922 17.2629 16.0434 16.2891C16.7605 15.2164 17.5035 14.1457 17.668 12.8106C18.8827 12.9386 20.0424 13.2344 21.131 13.8176C21.4637 13.9957 21.8812 14.0157 22.2597 14.1082C22.4 14.2166 22.608 14.2959 22.6692 14.4382C22.9775 15.1554 23.2792 15.8786 23.523 16.6194C23.8229 17.5306 23.903 18.4651 23.748 19.4289C23.5624 20.5829 23.0542 21.576 22.3997 22.5182C22.2909 22.675 22.2555 22.8829 22.1862 23.0672L22.1887 23.0642C22.075 23.1445 21.9549 23.2172 21.849 23.3065C21.5627 23.548 21.4935 24.0167 21.0379 24.0824C21.0317 24.0576 21.0287 24.0326 21.0292 24.0069C21.0052 23.9615 20.9814 23.9164 20.9574 23.8711C20.7914 23.5582 20.6252 23.2456 20.4592 22.9327L20.4595 22.9326ZM8.62136 9.51022C8.44703 9.50288 8.26653 9.63839 8.08886 9.70789C8.08886 9.70789 7.92619 11.0549 7.92619 11.7327C7.92619 12.4106 8.15803 12.9852 8.19736 13.6229C8.22536 14.0771 8.24753 14.5626 8.42353 14.9684C8.63486 15.4552 8.7267 15.9257 8.70036 16.4434C8.62736 17.8817 9.37319 18.8549 10.5164 19.5961C11.0305 19.0374 11.5887 18.5127 12.0495 17.9131C12.9719 16.7127 13.7595 15.4267 14.1932 13.9569C14.2835 13.6507 14.343 13.3357 14.4312 12.9639C14.4792 12.9149 14.5777 12.8141 14.6762 12.7132L12.3105 12.7066C12.2757 12.6751 12.2514 12.6529 12.2165 12.6214L11.9172 9.70205C10.8187 9.63455 9.72053 9.55639 8.62103 9.51005L8.62136 9.51022ZM11.0974 6.03072C10.7014 5.23139 10.1199 4.61372 9.23886 4.26172C9.22486 4.50289 9.21353 4.69605 9.2012 4.90972C8.90686 4.69755 8.64653 4.51005 8.31036 4.26772C8.35336 4.70072 8.39503 5.00289 8.41103 5.30655C8.44253 5.90689 8.18469 6.20839 7.58003 6.29239C7.46219 6.30872 7.33986 6.29239 7.22136 6.30622C6.86669 6.34722 6.67719 6.54672 6.62953 6.90005C6.56719 7.36139 6.80303 7.66355 7.18053 7.84722C7.57336 8.03839 7.99219 8.17639 8.47136 8.36605C8.40119 8.60255 8.32986 8.83639 8.26286 9.07139C8.20253 9.28289 8.14703 9.49572 8.08936 9.70805C8.26703 9.63855 8.44736 9.50305 8.62186 9.51039C9.72136 9.55672 10.8195 9.63472 11.918 9.70238C11.856 8.43122 11.6695 7.18522 11.0977 6.03105L11.0974 6.03072ZM22.7327 23.7432C22.7654 23.7774 22.7979 23.8114 22.8305 23.8456C22.8647 23.8799 22.8989 23.9142 22.933 23.9484C22.967 23.9811 23.0009 24.0137 23.0349 24.0464C23.1599 24.1296 23.2849 24.2129 23.4097 24.2961C23.4704 23.9702 23.8405 23.5016 24.1502 23.2742C24.278 23.1804 24.3344 22.9924 24.4334 22.8546C24.4887 22.7776 24.5649 22.7156 24.6317 22.6469C24.6047 22.4296 24.5622 22.2131 24.5539 21.9951C24.53 21.3696 24.5692 20.7522 24.3732 20.1277C24.1377 19.3777 24.2292 18.5857 24.2729 17.7916C24.9915 17.6471 25.2974 17.1784 25.3377 16.5476C25.3864 15.7856 25.2435 15.0506 24.7662 14.4271C24.424 13.9802 23.9605 13.7294 23.3855 13.8199C23.0047 13.8797 22.6349 14.0094 22.26 14.1079C22.4004 14.2162 22.6084 14.2956 22.6695 14.4379C22.9779 15.1551 23.2795 15.8782 23.5234 16.6191C23.8232 17.5302 23.9034 18.4647 23.7484 19.4286C23.5627 20.5826 23.0545 21.5757 22.4 22.5179C22.2912 22.6747 22.2559 22.8826 22.1865 23.0669C22.3687 23.2924 22.5507 23.5177 22.7329 23.7432H22.7327ZM16.429 12.7566C16.3242 14.1091 15.68 15.2467 14.965 16.3461C14.3355 17.3139 13.7025 18.2844 12.9959 19.1956C12.4884 19.8499 11.857 20.4084 11.2809 21.0096C11.2887 21.4552 11.2965 21.9011 11.3044 22.3467C11.3975 22.1769 11.4515 21.9602 11.59 21.8449C12.5274 21.0641 13.292 20.1311 14.0059 19.1536C14.6969 18.2072 15.3924 17.2627 16.0435 16.2889C16.7607 15.2162 17.5037 14.1456 17.6682 12.8104C17.2552 12.7924 16.8422 12.7746 16.4292 12.7566H16.429ZM11.0757 19.9797C11.6089 19.3922 12.2085 18.8511 12.6599 18.2062C13.3574 17.2101 13.9809 16.1586 14.582 15.1002C14.923 14.5001 15.171 13.8462 15.203 13.1314C15.2087 13.0027 15.3402 12.8799 15.4135 12.7542C15.3532 12.7559 15.293 12.7576 15.2327 12.7592C15.1554 12.7434 15.078 12.7274 15.0009 12.7116C14.8927 12.7122 14.7847 12.7127 14.6765 12.7134C14.578 12.8142 14.4794 12.9151 14.4315 12.9641C14.3434 13.3357 14.2837 13.6509 14.1935 13.9571C13.7599 15.4269 12.9722 16.7129 12.0499 17.9132C11.589 18.5129 11.0309 19.0376 10.5167 19.5962C10.703 19.7241 10.8894 19.8519 11.0757 19.9799V19.9797ZM15.712 12.7541C15.752 13.8777 15.2507 14.8322 14.7135 15.7546C14.1947 16.6451 13.6115 17.5002 13.0197 18.3452C12.6715 18.8424 12.2557 19.2926 11.8627 19.7576C11.6777 19.9764 11.4749 20.1802 11.28 20.3907C11.2804 20.5971 11.2805 20.8032 11.2809 21.0096C11.857 20.4084 12.4884 19.8499 12.9959 19.1956C13.7025 18.2846 14.3357 17.3141 14.965 16.3461C15.68 15.2467 16.3242 14.1091 16.429 12.7566C16.19 12.7557 15.951 12.7549 15.7119 12.7541H15.712ZM23.4289 24.3776C23.5199 24.5641 23.6867 24.7499 23.6879 24.9369C23.692 25.6002 23.6439 26.2644 23.6017 26.9272C23.598 26.9859 23.4942 27.0382 23.4369 27.0935C23.3985 27.1222 23.36 27.1509 23.3217 27.1796C23.2885 27.2149 23.2554 27.2502 23.2222 27.2854C23.186 27.3172 23.1497 27.3489 23.1135 27.3807C23.1704 27.4447 23.2244 27.5609 23.2844 27.564C23.6212 27.582 23.9594 27.5727 24.3122 27.5727C24.6089 26.8482 24.7105 26.1406 24.6009 25.4002C24.5792 25.2536 24.5384 25.0701 24.6017 24.9571C25.0337 24.1864 24.9189 23.4202 24.6317 22.6467C24.5649 22.7154 24.4887 22.7774 24.4334 22.8544C24.3344 22.9922 24.278 23.1802 24.1502 23.2741C23.8405 23.5014 23.4704 23.9701 23.4097 24.2959C23.4145 24.3234 23.4209 24.3505 23.4289 24.3774V24.3776ZM15.4137 12.7541C15.3404 12.8796 15.2089 13.0026 15.2032 13.1312C15.1712 13.8461 14.9232 14.4999 14.5822 15.1001C13.9809 16.1586 13.3575 17.2101 12.66 18.2061C12.2085 18.8509 11.609 19.3919 11.0759 19.9796C11.144 20.1166 11.212 20.2536 11.2802 20.3906C11.475 20.1799 11.6779 19.9762 11.8629 19.7574C12.2559 19.2926 12.6717 18.8422 13.0199 18.345C13.6115 17.5001 14.1949 16.6449 14.7137 15.7544C15.2509 14.8321 15.7522 13.8776 15.7122 12.7539C15.6127 12.7539 15.5134 12.7539 15.4139 12.7539L15.4137 12.7541ZM15.0009 12.7114C15.0782 12.7272 15.1555 12.7432 15.2327 12.7591C15.1554 12.7432 15.078 12.7272 15.0009 12.7114ZM12.2212 12.6641C12.251 12.6782 12.281 12.6924 12.3109 12.7066C12.2842 12.6857 12.2542 12.6716 12.2212 12.6641ZM20.2559 26.4779C20.1152 26.5756 19.9745 26.6732 19.8339 26.7709C19.8065 26.9284 19.7792 27.0859 19.7505 27.2509H20.9545C20.9545 27.0077 20.9384 26.7889 20.9602 26.5741C20.9747 26.4314 21.0054 26.2596 21.0949 26.1604C21.8912 25.2774 22.2055 24.2307 22.189 23.064C22.0754 23.1444 21.9552 23.2171 21.8494 23.3064C21.563 23.5479 21.4939 24.0166 21.0382 24.0822C21.0512 24.9702 20.7829 25.7662 20.256 26.4779H20.2559Z",fill:"url(#paint0_linear_1119_37286)"}),e("defs",{children:s("linearGradient",{id:"paint0_linear_1119_37286",x1:"3.72803",y1:"12.2264",x2:"26.5747",y2:"25.3626",gradientUnits:"userSpaceOnUse",children:[e("stop",{stopColor:"#F6DDD7"}),e("stop",{offset:"0.25",stopColor:"#FCABE6"}),e("stop",{offset:"0.3",stopColor:"#F3ADE6"}),e("stop",{offset:"0.38",stopColor:"#DDB3E8"}),e("stop",{offset:"0.48",stopColor:"#B8BCEC"}),e("stop",{offset:"0.59",stopColor:"#85CAF1"}),e("stop",{offset:"0.7",stopColor:"#50D8F6"}),e("stop",{offset:"0.76",stopColor:"#50D8F6"}),e("stop",{offset:"0.86",stopColor:"#B58FE8"})]})})]}),ho=()=>s("svg",{width:"32",height:"32",viewBox:"0 0 32 32",fill:"none",xmlns:"http://www.w3.org/2000/svg",children:[e("rect",{x:"0.25",y:"0.25",width:"31.5",height:"31.5"}),e("path",{d:"M24.0371 13.2112C24.5781 13.7522 24.5781 14.6325 24.0371 15.1734L22.8253 16.3657L22.813 16.2974C22.7245 15.8074 22.4915 15.3627 22.1398 15.011C21.875 14.7467 21.5619 14.5513 21.2091 14.4303C20.9902 14.6504 20.8698 14.9388 20.8698 15.2423C20.8698 15.3039 20.8754 15.3678 20.8866 15.4316C21.0809 15.5016 21.2528 15.6097 21.3973 15.7542C21.9382 16.2951 21.9382 17.1754 21.3973 17.7164L20.3422 18.7714C20.0718 19.0419 19.7167 19.1769 19.3611 19.1769C19.0055 19.1769 18.6505 19.0419 18.38 18.7714C17.839 18.2305 17.839 17.3502 18.38 16.8092L19.5918 15.6175L19.6042 15.6858C19.6921 16.1747 19.925 16.6194 20.2778 16.9716C20.5433 17.237 20.8373 17.4134 21.1895 17.5338L21.2545 17.4689C21.4516 17.2718 21.5597 17.0097 21.5597 16.7302C21.5597 16.6681 21.5541 16.6059 21.5434 16.5449C21.3402 16.4777 21.1727 16.3819 21.0204 16.2296C20.8009 16.0101 20.6642 15.7295 20.6262 15.4187C20.6234 15.3963 20.6217 15.3745 20.6194 15.3521C20.5892 14.9472 20.7354 14.5518 21.0204 14.2674L22.0754 13.2123C22.337 12.9508 22.6853 12.8063 23.0566 12.8063C23.4278 12.8063 23.7762 12.9502 24.0377 13.2123L24.0371 13.2112ZM29.5464 16C29.5464 19.8601 26.4059 23 22.5464 23H9C5.14048 23 2 19.8601 2 16C2 12.1399 5.14048 9 9 9H22.5464C26.4065 9 29.5464 12.1405 29.5464 16ZM15.4904 19.5106C15.6007 19.3768 15.0911 18.9999 14.987 18.8616C14.7753 18.632 14.7742 18.3016 14.6314 18.0334C14.2819 17.2236 13.8804 16.42 13.3187 15.7346C12.7251 14.9847 11.9926 14.3642 11.3492 13.6603C10.8715 13.1692 10.7438 12.4698 10.3222 11.9417C9.74088 11.0832 7.90296 10.8491 7.6336 12.0615C7.63472 12.0996 7.62296 12.1237 7.58992 12.1478C7.44096 12.2558 7.30824 12.3796 7.1968 12.5291C6.92408 12.9088 6.88208 13.5528 7.22256 13.8938C7.23376 13.7141 7.23992 13.5444 7.38216 13.4156C7.64536 13.6413 8.04296 13.7214 8.34816 13.5528C9.0224 14.5154 8.8544 15.8471 9.38976 16.8842C9.5376 17.1295 9.68656 17.3798 9.8764 17.5949C10.0304 17.8346 10.5624 18.1174 10.5938 18.3391C10.5994 18.7199 10.5546 19.136 10.8043 19.4546C10.9219 19.6932 10.633 19.9329 10.4 19.9032C10.0976 19.9446 9.72856 19.6999 9.46368 19.8506C9.37016 19.9519 9.18704 19.8399 9.1064 19.9805C9.0784 20.0533 8.9272 20.1558 9.01736 20.2258C9.1176 20.1496 9.21056 20.0701 9.34552 20.1154C9.32536 20.2252 9.41216 20.2409 9.48104 20.2728C9.4788 20.3473 9.43512 20.4234 9.49224 20.4867C9.55888 20.4195 9.59864 20.3243 9.70448 20.2963C10.0562 20.765 10.414 19.822 11.175 20.2465C11.0205 20.2386 10.8833 20.2582 10.7791 20.3854C10.7534 20.4139 10.7315 20.4475 10.7769 20.4845C11.1874 20.2196 11.1851 20.5752 11.4517 20.466C11.6566 20.359 11.8605 20.2252 12.1041 20.2633C11.8672 20.3316 11.8577 20.522 11.7188 20.6827C11.6953 20.7074 11.6841 20.7354 11.7115 20.7762C12.2032 20.7348 12.2435 20.5713 12.6406 20.3708C12.9368 20.1899 13.2319 20.6284 13.4884 20.3786C13.545 20.3243 13.6222 20.3428 13.6922 20.3355C13.6026 19.8578 12.6176 20.4229 12.6333 19.7822C12.9502 19.5666 12.8774 19.1539 12.8987 18.8207C13.2633 19.0229 13.6687 19.1405 14.026 19.3337C14.2063 19.6249 14.4891 20.0096 14.866 19.9844C14.8761 19.9553 14.885 19.9295 14.8957 19.8998C15.0099 19.9194 15.1566 19.995 15.2194 19.8506C15.3902 20.0292 15.641 20.0202 15.8645 19.9743C16.0297 19.8399 15.5537 19.6484 15.4898 19.5101L15.4904 19.5106ZM25.4926 14.1923C25.4926 13.5405 25.2394 12.9284 24.7797 12.4686C24.3199 12.0089 23.7078 11.7558 23.0554 11.7558C22.403 11.7558 21.791 12.0089 21.3312 12.4686L20.2762 13.5237C20.0298 13.7701 19.8427 14.0596 19.7201 14.3838L19.7128 14.4023L19.6938 14.4079C19.3107 14.5261 18.973 14.7288 18.6902 15.0116L17.6352 16.0666C16.6849 17.0175 16.6849 18.5642 17.6352 19.5146C18.095 19.9743 18.707 20.2274 19.3589 20.2274C20.0107 20.2274 20.6234 19.9743 21.0831 19.5146L22.1382 18.4595C22.3834 18.2142 22.5694 17.9258 22.692 17.6022L22.6993 17.5837L22.7183 17.5775C23.0946 17.4622 23.4418 17.2527 23.7235 16.9716L24.7786 15.9166C25.2383 15.4568 25.4914 14.8447 25.4914 14.1923H25.4926ZM11.6533 18.7216C11.5626 19.0755 11.5329 19.6786 11.0726 19.696C11.0345 19.9004 11.2142 19.9771 11.3772 19.9116C11.539 19.8371 11.6158 19.9704 11.6701 20.1031C11.9198 20.1395 12.2894 20.0197 12.3034 19.724C11.9305 19.509 11.8151 19.1002 11.6527 18.7216H11.6533Z",fill:"var(--ac-global-text-color-900)"})]}),S6=()=>s("svg",{width:"32",height:"32",viewBox:"0 0 32 32",fill:"none",xmlns:"http://www.w3.org/2000/svg",children:[e("path",{d:"M29.5341 0H2.46593C1.10403 0 0 1.10403 0 2.46593V29.5341C0 30.896 1.10403 32 2.46593 32H29.5341C30.896 32 32 30.896 32 29.5341V2.46593C32 1.10403 30.896 0 29.5341 0Z",fill:"#0EAF9C"}),e("path",{d:"M24.1471 21.3058C24.1471 21.4934 23.9942 21.6447 23.806 21.6447C22.1086 21.6447 20.7328 20.2777 20.7328 18.5913V13.1026C20.7328 10.6667 18.7453 8.69255 16.2944 8.69255C13.8435 8.69255 11.9651 10.6674 11.9651 13.1026V15.1358C11.9611 15.3197 12.1082 15.4716 12.2925 15.4749C12.2951 15.4749 12.2971 15.4749 12.2997 15.4749H14.2389C14.4271 15.4787 14.5833 15.33 14.5872 15.1424C14.5872 15.1398 14.5872 15.1378 14.5872 15.1352V13.0201C14.5872 12.083 15.3513 11.3239 16.2944 11.3239C17.2375 11.3239 18.0016 12.083 18.0016 13.0201V25.7697C17.9976 25.9606 17.8388 26.1126 17.6466 26.1086C15.9571 26.1086 14.5872 24.7475 14.5872 23.0689C14.5872 23.0643 14.5872 23.0597 14.5872 23.0552V18.9842C14.5833 18.7958 14.4284 18.6451 14.2389 18.6451H12.2997C12.1147 18.6451 11.9651 18.7939 11.9651 18.9776C11.9651 18.9802 11.9651 18.9822 11.9651 18.9848V20.342C11.9651 22.0285 10.4801 23.3955 8.78276 23.3955C8.59391 23.3955 8.44165 23.2436 8.44165 23.0565V13.1033C8.44165 8.79386 11.9572 5.30078 16.2944 5.30078C20.6315 5.30078 24.1471 8.79386 24.1471 13.1033V21.3058Z",fill:"white"})]}),x6=()=>s("svg",{width:"32",height:"32",viewBox:"0 0 32 32",fill:"none",xmlns:"http://www.w3.org/2000/svg",children:[s("g",{clipPath:"url(#clip0_1112_37203)",children:[e("path",{d:"M29.0909 0H23.2727V6.39251H29.0909V0Z",fill:"black"}),e("path",{d:"M32 0H26.1818V6.39251H32V0Z",fill:"#F7D046"}),e("path",{d:"M5.81818 0H0V6.39251H5.81818V0Z",fill:"black"}),e("path",{d:"M5.81818 6.39258H0V12.7851H5.81818V6.39258Z",fill:"black"}),e("path",{d:"M5.81818 12.7852H0V19.1777H5.81818V12.7852Z",fill:"black"}),e("path",{d:"M5.81818 19.1777H0V25.5702H5.81818V19.1777Z",fill:"black"}),e("path",{d:"M5.81818 25.5698H0V31.9623H5.81818V25.5698Z",fill:"black"}),e("path",{d:"M8.7273 0H2.90912V6.39251H8.7273V0Z",fill:"#F7D046"}),e("path",{d:"M32 6.39258H26.1818V12.7851H32V6.39258Z",fill:"#F2A73B"}),e("path",{d:"M8.7273 6.39258H2.90912V12.7851H8.7273V6.39258Z",fill:"#F2A73B"}),e("path",{d:"M23.2727 6.39258H17.4545V12.7851H23.2727V6.39258Z",fill:"black"}),e("path",{d:"M26.1818 6.39258H20.3636V12.7851H26.1818V6.39258Z",fill:"#F2A73B"}),e("path",{d:"M14.5455 6.39258H8.72729V12.7851H14.5455V6.39258Z",fill:"#F2A73B"}),e("path",{d:"M20.3637 12.7852H14.5455V19.1777H20.3637V12.7852Z",fill:"#EE792F"}),e("path",{d:"M26.1818 12.7852H20.3636V19.1777H26.1818V12.7852Z",fill:"#EE792F"}),e("path",{d:"M14.5455 12.7852H8.72729V19.1777H14.5455V12.7852Z",fill:"#EE792F"}),e("path",{d:"M17.4545 19.1777H11.6364V25.5702H17.4545V19.1777Z",fill:"black"}),e("path",{d:"M20.3637 19.1777H14.5455V25.5702H20.3637V19.1777Z",fill:"#EB5829"}),e("path",{d:"M32 12.7852H26.1818V19.1777H32V12.7852Z",fill:"#EE792F"}),e("path",{d:"M8.7273 12.7852H2.90912V19.1777H8.7273V12.7852Z",fill:"#EE792F"}),e("path",{d:"M29.0909 19.1777H23.2727V25.5702H29.0909V19.1777Z",fill:"black"}),e("path",{d:"M32 19.1777H26.1818V25.5702H32V19.1777Z",fill:"#EB5829"}),e("path",{d:"M29.0909 25.5698H23.2727V31.9623H29.0909V25.5698Z",fill:"black"}),e("path",{d:"M8.7273 19.1777H2.90912V25.5702H8.7273V19.1777Z",fill:"#EB5829"}),e("path",{d:"M32 25.5698H26.1818V31.9623H32V25.5698Z",fill:"#EA3326"}),e("path",{d:"M8.7273 25.5698H2.90912V31.9623H8.7273V25.5698Z",fill:"#EA3326"})]}),e("defs",{children:e("clipPath",{id:"clip0_1112_37203",children:e("rect",{width:"32",height:"32",fill:"white"})})})]}),T6=()=>s("svg",{width:"32",height:"32",viewBox:"0 0 32 32",fill:"none",xmlns:"http://www.w3.org/2000/svg",children:[e("path",{d:"M26.6667 18.52C26.5078 18.3292 26.2852 18.2025 26.04 18.1633C25.7949 18.1241 25.5438 18.175 25.3333 18.3067L16 25.16V25.4533C16.1347 25.4374 16.2712 25.4501 16.4005 25.4908C16.5299 25.5314 16.6492 25.5989 16.7506 25.689C16.852 25.7791 16.9331 25.8896 16.9887 26.0133C17.0442 26.137 17.0729 26.2711 17.0729 26.4067C17.0729 26.5423 17.0442 26.6763 16.9887 26.8C16.9331 26.9237 16.852 27.0342 16.7506 27.1243C16.6492 27.2144 16.5299 27.2819 16.4005 27.3226C16.2712 27.3632 16.1347 27.3759 16 27.36C16.2165 27.361 16.4274 27.2907 16.6 27.16L26.48 19.8667C26.6725 19.7053 26.7982 19.4781 26.8327 19.2293C26.8672 18.9804 26.808 18.7277 26.6667 18.52Z",fill:"#669DF6"}),e("path",{d:"M16 27.3598C15.7666 27.3322 15.5514 27.2198 15.3953 27.0441C15.2392 26.8684 15.153 26.6415 15.153 26.4065C15.153 26.1714 15.2392 25.9446 15.3953 25.7689C15.5514 25.5931 15.7666 25.4808 16 25.4532V25.1598L6.66669 18.3065C6.45707 18.172 6.20525 18.1194 5.95931 18.1587C5.71337 18.1981 5.49054 18.3266 5.33335 18.5198C5.19277 18.7276 5.13659 18.981 5.17621 19.2287C5.21584 19.4764 5.34831 19.6997 5.54669 19.8532L15.4267 27.1465C15.5952 27.2753 15.8012 27.3455 16.0134 27.3465L16 27.3598Z",fill:"#AECBFA"}),e("path",{d:"M16 24.4531C15.6123 24.4531 15.2334 24.5681 14.9111 24.7834C14.5887 24.9988 14.3375 25.3049 14.1892 25.6631C14.0408 26.0212 14.002 26.4153 14.0776 26.7955C14.1533 27.1757 14.3399 27.5249 14.614 27.7991C14.8882 28.0732 15.2374 28.2598 15.6176 28.3355C15.9978 28.4111 16.3919 28.3723 16.75 28.2239C17.1082 28.0756 17.4143 27.8244 17.6297 27.502C17.845 27.1797 17.96 26.8008 17.96 26.4131C17.96 25.8933 17.7535 25.3948 17.3859 25.0272C17.0183 24.6596 16.5198 24.4531 16 24.4531ZM16 27.3598C15.8095 27.3598 15.6234 27.3031 15.4653 27.197C15.3071 27.0909 15.1841 26.9402 15.1119 26.764C15.0396 26.5878 15.0214 26.3941 15.0595 26.2075C15.0977 26.021 15.1904 25.85 15.326 25.7162C15.4616 25.5825 15.6339 25.4922 15.821 25.4566C16.0081 25.4211 16.2015 25.442 16.3767 25.5168C16.5519 25.5915 16.7008 25.7166 16.8047 25.8762C16.9086 26.0358 16.9626 26.2227 16.96 26.4131C16.96 26.5386 16.9351 26.6628 16.8867 26.7785C16.8383 26.8942 16.7673 26.9992 16.678 27.0873C16.5887 27.1754 16.4827 27.2448 16.3663 27.2916C16.25 27.3384 16.1254 27.3616 16 27.3598Z",fill:"#4285F4"}),e("path",{d:"M8.00001 8.14679C7.73587 8.14333 7.48352 8.03687 7.29673 7.85008C7.10993 7.66328 7.00347 7.41093 7.00001 7.14679V4.64012C6.98365 4.4982 6.99749 4.35441 7.04061 4.21821C7.08373 4.08201 7.15517 3.95647 7.25023 3.84982C7.34529 3.74317 7.46183 3.65782 7.5922 3.59939C7.72256 3.54095 7.86382 3.51074 8.00668 3.51074C8.14955 3.51074 8.2908 3.54095 8.42117 3.59939C8.55153 3.65782 8.66807 3.74317 8.76313 3.84982C8.85819 3.95647 8.92963 4.08201 8.97275 4.21821C9.01587 4.35441 9.02971 4.4982 9.01335 4.64012V7.14679C9.00984 7.41322 8.90153 7.66756 8.71188 7.85472C8.52222 8.04188 8.26647 8.14681 8.00001 8.14679Z",fill:"#AECBFA"}),e("path",{d:"M7.97336 17.0135C8.533 17.0135 8.98669 16.5598 8.98669 16.0002C8.98669 15.4405 8.533 14.9868 7.97336 14.9868C7.41371 14.9868 6.96002 15.4405 6.96002 16.0002C6.96002 16.5598 7.41371 17.0135 7.97336 17.0135Z",fill:"#AECBFA"}),e("path",{d:"M7.97336 14.0667C8.533 14.0667 8.98669 13.613 8.98669 13.0534C8.98669 12.4937 8.533 12.04 7.97336 12.04C7.41371 12.04 6.96002 12.4937 6.96002 13.0534C6.96002 13.613 7.41371 14.0667 7.97336 14.0667Z",fill:"#AECBFA"}),e("path",{d:"M7.97336 11.1067C8.533 11.1067 8.98669 10.6531 8.98669 10.0934C8.98669 9.53376 8.533 9.08008 7.97336 9.08008C7.41371 9.08008 6.96002 9.53376 6.96002 10.0934C6.96002 10.6531 7.41371 11.1067 7.97336 11.1067Z",fill:"#AECBFA"}),e("path",{d:"M24 11.0801C23.7336 11.0766 23.4792 10.9682 23.2921 10.7786C23.1049 10.5889 23 10.3332 23 10.0667V7.56006C23 7.29484 23.1054 7.04049 23.2929 6.85295C23.4804 6.66542 23.7348 6.56006 24 6.56006C24.2652 6.56006 24.5196 6.66542 24.7071 6.85295C24.8946 7.04049 25 7.29484 25 7.56006V10.0667C25.0018 10.1992 24.9772 10.3306 24.9277 10.4535C24.8783 10.5764 24.8049 10.6882 24.7119 10.7825C24.6188 10.8767 24.508 10.9516 24.3858 11.0027C24.2636 11.0538 24.1325 11.0801 24 11.0801Z",fill:"#4285F4"}),e("path",{d:"M24.0266 17.0267C24.5863 17.0267 25.04 16.573 25.04 16.0133C25.04 15.4537 24.5863 15 24.0266 15C23.467 15 23.0133 15.4537 23.0133 16.0133C23.0133 16.573 23.467 17.0267 24.0266 17.0267Z",fill:"#4285F4"}),e("path",{d:"M24.0266 14.0267C24.5863 14.0267 25.04 13.573 25.04 13.0133C25.04 12.4537 24.5863 12 24.0266 12C23.467 12 23.0133 12.4537 23.0133 13.0133C23.0133 13.573 23.467 14.0267 24.0266 14.0267Z",fill:"#4285F4"}),e("path",{d:"M24.0266 5.65313C24.5863 5.65313 25.04 5.19945 25.04 4.6398C25.04 4.08015 24.5863 3.62646 24.0266 3.62646C23.467 3.62646 23.0133 4.08015 23.0133 4.6398C23.0133 5.19945 23.467 5.65313 24.0266 5.65313Z",fill:"#4285F4"}),e("path",{d:"M16 20.0001C15.7359 19.9967 15.4835 19.8902 15.2967 19.7034C15.1099 19.5166 15.0035 19.2642 15 19.0001V16.4534C15.0285 16.2064 15.1468 15.9785 15.3324 15.813C15.518 15.6476 15.758 15.5562 16.0067 15.5562C16.2553 15.5562 16.4953 15.6476 16.6809 15.813C16.8665 15.9785 16.9849 16.2064 17.0133 16.4534V18.9734C17.0151 19.1076 16.9902 19.2408 16.9401 19.3653C16.8899 19.4898 16.8156 19.6031 16.7213 19.6986C16.627 19.7941 16.5147 19.87 16.3909 19.9217C16.2671 19.9735 16.1342 20.0001 16 20.0001Z",fill:"#669DF6"}),e("path",{d:"M16 22.9466C16.5597 22.9466 17.0134 22.4929 17.0134 21.9333C17.0134 21.3736 16.5597 20.9199 16 20.9199C15.4404 20.9199 14.9867 21.3736 14.9867 21.9333C14.9867 22.4929 15.4404 22.9466 16 22.9466Z",fill:"#669DF6"}),e("path",{d:"M16 14.5335C16.5597 14.5335 17.0134 14.0798 17.0134 13.5202C17.0134 12.9605 16.5597 12.5068 16 12.5068C15.4404 12.5068 14.9867 12.9605 14.9867 13.5202C14.9867 14.0798 15.4404 14.5335 16 14.5335Z",fill:"#669DF6"}),e("path",{d:"M16 11.5735C16.5597 11.5735 17.0134 11.1199 17.0134 10.5602C17.0134 10.0006 16.5597 9.54688 16 9.54688C15.4404 9.54688 14.9867 10.0006 14.9867 10.5602C14.9867 11.1199 15.4404 11.5735 16 11.5735Z",fill:"#669DF6"}),e("path",{d:"M20 14.0535C19.7359 14.0501 19.4835 13.9436 19.2967 13.7568C19.1099 13.57 19.0035 13.3177 19 13.0535V10.5469C18.9837 10.4049 18.9975 10.2612 19.0406 10.125C19.0837 9.98875 19.1552 9.8632 19.2502 9.75655C19.3453 9.64991 19.4618 9.56456 19.5922 9.50613C19.7226 9.44769 19.8638 9.41748 20.0067 9.41748C20.1495 9.41748 20.2908 9.44769 20.4212 9.50613C20.5515 9.56456 20.6681 9.64991 20.7631 9.75655C20.8582 9.8632 20.9296 9.98875 20.9728 10.125C21.0159 10.2612 21.0297 10.4049 21.0133 10.5469V13.0535C21.0098 13.32 20.9015 13.5743 20.7119 13.7615C20.5222 13.9486 20.2665 14.0535 20 14.0535Z",fill:"#4285F4"}),e("path",{d:"M20.0133 8.59991C20.573 8.59991 21.0267 8.14622 21.0267 7.58658C21.0267 7.02693 20.573 6.57324 20.0133 6.57324C19.4537 6.57324 19 7.02693 19 7.58658C19 8.14622 19.4537 8.59991 20.0133 8.59991Z",fill:"#4285F4"}),e("path",{d:"M20.0133 19.9334C20.573 19.9334 21.0267 19.4797 21.0267 18.9201C21.0267 18.3604 20.573 17.9067 20.0133 17.9067C19.4537 17.9067 19 18.3604 19 18.9201C19 19.4797 19.4537 19.9334 20.0133 19.9334Z",fill:"#4285F4"}),e("path",{d:"M20.0133 16.9734C20.573 16.9734 21.0267 16.5198 21.0267 15.9601C21.0267 15.4005 20.573 14.9468 20.0133 14.9468C19.4537 14.9468 19 15.4005 19 15.9601C19 16.5198 19.4537 16.9734 20.0133 16.9734Z",fill:"#4285F4"}),e("path",{d:"M11.9867 19.9334C12.5463 19.9334 13 19.4797 13 18.9201C13 18.3604 12.5463 17.9067 11.9867 17.9067C11.427 17.9067 10.9733 18.3604 10.9733 18.9201C10.9733 19.4797 11.427 19.9334 11.9867 19.9334Z",fill:"#AECBFA"}),e("path",{d:"M11.9867 11.5735C12.5463 11.5735 13 11.1199 13 10.5602C13 10.0006 12.5463 9.54688 11.9867 9.54688C11.427 9.54688 10.9733 10.0006 10.9733 10.5602C10.9733 11.1199 11.427 11.5735 11.9867 11.5735Z",fill:"#AECBFA"}),e("path",{d:"M11.9867 8.59991C12.5463 8.59991 13 8.14622 13 7.58658C13 7.02693 12.5463 6.57324 11.9867 6.57324C11.427 6.57324 10.9733 7.02693 10.9733 7.58658C10.9733 8.14622 11.427 8.59991 11.9867 8.59991Z",fill:"#AECBFA"}),e("path",{d:"M12 16.9735C11.7381 16.9737 11.4862 16.8724 11.2973 16.6909C11.1083 16.5095 10.997 16.2619 10.9867 16.0001V13.4668C10.9867 13.2016 11.0921 12.9472 11.2796 12.7597C11.4671 12.5722 11.7215 12.4668 11.9867 12.4668C12.2519 12.4668 12.5063 12.5722 12.6938 12.7597C12.8813 12.9472 12.9867 13.2016 12.9867 13.4668V16.0001C12.9798 16.2584 12.8733 16.504 12.6893 16.6854C12.5054 16.8669 12.2584 16.9701 12 16.9735Z",fill:"#AECBFA"})]}),A6=()=>s("svg",{width:"32",height:"32",viewBox:"0 0 32 32",fill:"none",xmlns:"http://www.w3.org/2000/svg",children:[e("g",{clipPath:"url(#clip0_1148_5989)",children:e("path",{d:"M1.96742 0.421623C1.1852 0.496042 0.711124 0.64488 0.616309 0.868135C0.379272 1.5379 0.189642 30.6108 0.42668 30.9829C0.592605 31.2309 1.75409 31.3798 4.64594 31.5286C9.88446 31.8511 30.9571 31.7022 31.2652 31.3798C31.4074 31.2309 31.5259 25.7239 31.5733 16.1736C31.6445 2.15806 31.6208 1.19061 31.2415 0.892941C31.0045 0.719297 29.9852 0.496042 28.9896 0.421623C27.1171 0.24798 4.21927 0.272786 1.96742 0.421623ZM15.7867 2.10844C15.8815 2.3317 15.8578 3.10069 15.763 3.84488C15.6208 5.18441 15.5971 5.20922 14.8385 5.20922C11.6148 5.20922 11.5674 11.386 14.7911 11.4852C15.2652 11.51 15.6445 11.6092 15.6445 11.7332C15.6445 11.8325 15.5259 12.7255 15.36 13.6929L15.0993 15.4294L14.0089 15.2805C10.8326 14.8092 10.2874 14.8092 9.86075 15.2557C9.60001 15.5286 9.5052 15.9007 9.57631 16.2232C10.1452 18.2573 9.83705 18.8526 8.29631 18.8526C6.58964 18.8526 6.3052 18.4061 6.92149 16.6201C7.15853 15.8759 7.13483 15.7519 6.63705 15.3301C6.21038 14.9581 5.6889 14.8836 3.84001 14.8836H1.58816L1.73038 12.8247C1.8252 11.7084 1.89631 8.80612 1.89631 6.39992V2.00922L2.56001 1.91C2.91557 1.86038 5.99705 1.78596 9.43409 1.76116C14.7911 1.73635 15.6682 1.78596 15.7867 2.10844ZM30.0326 2.05883C30.1985 2.23248 30.1985 15.3798 30.0326 15.5286C30.0089 15.5534 29.1556 15.6278 28.1363 15.6774L26.2874 15.8015L26.4296 15.2061C26.643 14.2387 26.1215 12.9488 25.363 12.527C24.4859 12.0557 22.5185 12.0557 21.4519 12.5022C20.4326 12.9488 20.0771 13.6681 20.1956 15.0325L20.2667 16.0991L19.2 15.9751C16.6163 15.6774 16.5452 15.6526 16.6874 15.0325C16.7585 14.71 16.9482 13.5937 17.0904 12.5519C17.3274 10.865 17.3274 10.5922 16.9719 10.1953C16.6637 9.82317 16.3556 9.74875 15.6208 9.84798C14.4593 10.0216 13.9852 9.62472 13.9852 8.50844C13.9852 7.04488 14.3171 6.67279 15.5971 6.7472C16.5452 6.82162 16.7111 6.7472 16.9956 6.20147C17.1615 5.85418 17.3037 4.7379 17.3037 3.64643V1.68674L23.5615 1.78596C26.9985 1.81077 29.9141 1.95961 30.0326 2.05883ZM24.4385 13.9162C24.8415 14.1395 24.8889 14.3875 24.8415 15.7022L24.7704 17.2402L27.4963 17.1906L30.2222 17.1658L30.1985 18.679C30.1748 19.5224 30.1511 22.4743 30.1274 25.2278L30.1037 30.2635H23.2296H16.3556V28.527V26.8154L17.5408 26.9643C18.6548 27.0883 18.7496 27.0635 19.5793 26.1953C20.4326 25.3022 20.4326 25.2774 20.3378 23.541C20.2667 21.9534 20.1719 21.7053 19.5556 21.1596C18.963 20.6139 18.7022 20.5395 17.4696 20.6387L16.0711 20.7379L16.2133 20.0185C16.2845 19.6216 16.3556 18.8278 16.3556 18.2325V17.1906L17.4933 17.3891C18.1096 17.4883 19.2711 17.5875 20.0533 17.5875C21.9259 17.6123 22.2104 17.3146 21.8311 15.7519C21.6889 15.1069 21.6178 14.4867 21.7126 14.3627C22.0919 13.7177 23.6563 13.4697 24.4385 13.9162ZM5.09631 17.6371C5.12001 19.1751 5.6889 19.9937 6.92149 20.341C8.34372 20.7627 9.88446 20.4402 10.7141 19.5968C11.2593 19.0263 11.3778 18.679 11.3778 17.7115V16.5457L12.4682 16.7193C13.0845 16.7937 13.8193 16.8681 14.1274 16.8681C14.6963 16.8681 14.6963 16.9177 14.6963 19.3488C14.6963 21.4573 14.7674 21.9038 15.1467 22.3007C15.5971 22.772 15.6682 22.772 16.7822 22.3999C17.4222 22.1767 18.1096 22.0774 18.323 22.1519C18.7971 22.3255 19.0341 23.8387 18.7259 24.6821C18.4889 25.3022 18.3941 25.3519 17.4696 25.2278C16.9245 25.1782 16.3082 25.0294 16.1185 24.955C15.9052 24.8557 15.5496 24.955 15.2889 25.1534C14.8859 25.4511 14.7911 25.8728 14.7437 27.8821L14.6489 30.2635H11.7571C10.1452 30.2635 7.22964 30.1891 5.26224 30.0898L1.65927 29.941V23.1441V16.3472L3.38964 16.4216L5.09631 16.496V17.6371Z",fill:"#EF4036"})}),e("defs",{children:e("clipPath",{id:"clip0_1148_5989",children:e("rect",{width:"32",height:"32",fill:"transparent"})})})]}),I6=()=>s("svg",{width:"32",height:"32",viewBox:"0 0 32 32",fill:"none",xmlns:"http://www.w3.org/2000/svg",children:[e("path",{d:"M18.2835 6L26.4963 26.5994H31L22.7873 6H18.2835Z",fill:"var(--ac-global-text-color-900)"}),e("path",{d:"M8.75587 18.4479L11.566 11.2087L14.3762 18.4479H8.75587ZM9.21147 6L1 26.5994H5.59136L7.27074 22.2735H15.8616L17.5407 26.5994H22.132L13.9206 6H9.21147Z",fill:"var(--ac-global-text-color-900)"})]}),z6=()=>s("svg",{width:"32",height:"32",viewBox:"0 0 32 32",fill:"none",xmlns:"http://www.w3.org/2000/svg",children:[e("path",{d:"M18.9623 11.0195C16.8877 11.0195 15.208 12.6992 15.208 14.7739C15.208 16.8485 16.8877 18.5282 18.9623 18.5282C21.037 18.5282 22.7167 16.8485 22.7167 14.7739C22.7167 12.6992 21.0332 11.0195 18.9623 11.0195ZM18.9623 17.1208C17.6662 17.1208 16.6154 16.07 16.6154 14.7739C16.6154 13.4777 17.6662 12.4269 18.9623 12.4269C20.2585 12.4269 21.3093 13.4777 21.3093 14.7739C21.3093 16.07 20.2585 17.1208 18.9623 17.1208Z",fill:"var(--ac-global-text-color-900)"}),e("path",{d:"M13.7781 11.0308C13.6515 11.0155 13.5212 11.0078 13.3908 11.0078C13.3256 11.0078 13.2642 11.0078 13.2029 11.0078C13.1415 11.0078 13.0763 11.0155 13.015 11.0193C12.7619 11.0385 12.5126 11.0807 12.2672 11.1459C11.7648 11.2801 11.2969 11.514 10.8904 11.84C10.4763 12.1736 10.1426 12.5954 9.91639 13.0786C9.80518 13.3202 9.72081 13.5733 9.67096 13.8341C9.64411 13.9607 9.62494 14.091 9.61343 14.2214C9.6096 14.2866 9.60193 14.348 9.60193 14.417V14.5129V14.6011V15.8589L9.6096 17.1167L9.61727 18.3746H11.0247L11.0323 17.1167V15.8589L11.04 14.6011V14.4707C11.04 14.4323 11.0477 14.3902 11.0515 14.3518C11.0592 14.2751 11.0707 14.1946 11.086 14.1179C11.1167 13.9683 11.1666 13.8188 11.2317 13.6807C11.3621 13.4008 11.5539 13.1553 11.7955 12.9598C12.0486 12.7603 12.3362 12.6108 12.6468 12.5264C12.8079 12.4842 12.9689 12.4536 13.1377 12.4382C13.1798 12.4382 13.222 12.4305 13.2642 12.4305C13.3064 12.4305 13.3486 12.4305 13.3908 12.4305C13.4713 12.4305 13.5518 12.4344 13.6324 12.442C13.9545 12.4727 14.2651 12.5724 14.5451 12.7297L15.2468 11.5102C14.7982 11.2494 14.2996 11.0845 13.7858 11.027L13.7781 11.0308Z",fill:"var(--ac-global-text-color-900)"}),e("path",{d:"M4.789 11.0002C2.71434 10.981 1.01934 12.6453 1.00016 14.72C0.98099 16.7946 2.64532 18.4896 4.71997 18.5088H6.02383V17.1014H4.789C3.49282 17.1168 2.43057 16.0775 2.41523 14.7813C2.39989 13.4852 3.43913 12.4229 4.73531 12.4076H4.789C6.08518 12.4076 7.13593 13.4583 7.13977 14.7545V18.2135C7.13977 19.4982 6.09285 20.5451 4.81201 20.5605C4.19843 20.5566 3.6117 20.3074 3.17836 19.874L2.1813 20.8711C2.87157 21.5652 3.80728 21.9602 4.78517 21.9717H4.83502C6.88283 21.941 8.52799 20.2805 8.53949 18.2327V14.6663C8.48964 12.6261 6.82531 11.0002 4.789 11.0002Z",fill:"var(--ac-global-text-color-900)"}),e("path",{d:"M27.2533 11.0195C25.1787 11.0195 23.499 12.6992 23.499 14.7739C23.499 16.8485 25.1787 18.5282 27.2533 18.5282H28.538V17.1208H27.2533C25.9572 17.1208 24.9064 16.07 24.9064 14.7739C24.9064 13.4777 25.9572 12.4269 27.2533 12.4269C28.469 12.4269 29.4852 13.3588 29.5926 14.5706V21.7801H31V14.7739C30.9962 12.703 29.3242 11.0195 27.2533 11.0195Z",fill:"var(--ac-global-text-color-900)"})]}),M6=()=>e("svg",{version:"1.1",id:"Layer_1",xmlns:"http://www.w3.org/2000/svg",x:"0px",y:"0px",width:"32",height:"32",viewBox:"0 0 400 400",enableBackground:"new 0 0 400 400",xmlSpace:"preserve",children:e("path",{fill:"var(--ac-global-text-color-900)",stroke:"none",d:`
M108.357758,374.748016
	C68.931068,356.066071 45.775341,325.019348 36.873970,283.154297
	C30.389435,252.656082 33.336266,222.467133 42.685719,193.016541
	C58.768898,142.354813 85.827126,98.280418 124.748680,61.938580
	C145.764755,42.315449 169.544373,26.902735 197.551865,18.696321
	C233.877899,8.052515 266.357330,15.785578 295.642151,38.813885
	C311.787628,51.509991 325.734741,66.145889 333.571045,85.621201
	C340.671906,103.268669 340.516388,121.362411 336.592682,139.643417
	C333.681305,153.207916 328.341309,165.942825 322.998566,178.398621
	C323.824585,180.318497 325.412994,180.144730 326.588379,180.303497
	C348.189026,183.221146 362.405640,201.825790 365.324188,224.059479
	C369.047516,252.424057 359.334717,276.863831 342.760071,298.986633
	C309.078064,343.943359 264.191742,371.643372 209.528900,383.468353
	C175.162979,390.902557 141.349426,389.043335 108.357758,374.748016
M271.080261,209.564880
	C276.822632,194.262497 283.971436,179.601944 291.199829,164.964279
	C296.215637,154.807129 300.561798,144.335480 303.180573,133.260727
	C307.179047,116.351280 306.355347,100.337906 294.874695,86.023811
	C283.959991,72.415321 271.036224,61.444416 255.257523,53.889622
	C243.448471,48.235489 231.098053,46.722847 218.275681,48.963493
	C190.663696,53.788551 168.189636,68.463501 148.031158,86.866074
	C121.336411,111.235603 101.638069,140.797668 86.485901,173.465500
	C72.204773,204.255356 64.520126,236.334229 69.392883,270.412170
	C73.207108,297.087158 84.966972,319.501312 107.685608,335.065063
	C135.185516,353.904266 165.862350,356.662231 197.639496,351.232513
	C226.848587,346.241608 253.160049,333.984497 277.058044,316.581299
	C297.531555,301.671906 314.873077,283.874969 325.936218,260.777405
	C331.523773,249.111649 333.769897,236.736618 330.307495,223.889450
	C329.156708,219.619415 327.376648,215.425262 322.397522,214.499054
	C317.326202,213.555649 314.021484,216.935379 310.871582,220.215073
	C310.074585,221.044922 309.510468,222.103455 308.867737,223.075668
	C300.009247,236.475174 289.673126,248.552429 277.708557,259.333801
	C249.653473,284.614502 216.635345,296.440063 179.132095,296.318329
	C161.393463,296.260742 149.833130,287.682251 145.810806,270.539856
	C140.823715,249.285797 142.451172,227.976303 150.218277,207.764145
	C164.287735,171.151611 185.422729,138.726166 211.975861,109.887596
	C218.737091,102.544426 225.840866,95.432785 234.904358,90.815033
	C237.647705,89.417328 240.608063,87.398354 243.710663,89.989059
	C247.025345,92.756889 246.760300,96.405632 245.685867,100.093086
	C244.092072,105.562981 241.271606,110.502014 238.899857,115.639061
	C231.912460,130.773315 225.552048,146.141083 222.041946,162.530533
	C217.079269,185.702393 230.538971,209.662094 252.994049,217.609100
	C261.908478,220.763977 266.484222,218.869110 271.080261,209.564880
z`})}),F6=()=>e("svg",{fill:"var(--ac-global-text-color-900)",width:"32",height:"32",viewBox:"0 0 32 32",xmlns:"http://www.w3.org/2000/svg",children:e("path",{d:"M 15.994141 3 C 15.629141 3 15.264219 3.0895313 14.949219 3.2695312 L 5.0390625 8.9902344 C 4.3990625 9.3602344 4 10.060781 4 10.800781 L 4 21.179688 C 4 21.929688 4.3990625 22.620234 5.0390625 22.990234 L 7.640625 24.490234 C 8.900625 25.110234 9.3499219 25.109375 9.9199219 25.109375 C 11.789922 25.109375 12.859375 23.979531 12.859375 22.019531 L 12.859375 11.310547 C 12.859375 11.150547 12.730312 11.019531 12.570312 11.019531 L 11.320312 11.019531 C 11.150313 11.019531 11.029297 11.150547 11.029297 11.310547 L 11.029297 22.009766 C 11.029297 22.889766 10.120391 23.749531 8.6503906 23.019531 L 5.9296875 21.449219 C 5.8296875 21.399219 5.7695313 21.289687 5.7695312 21.179688 L 5.7695312 10.810547 C 5.7695312 10.690547 5.8296875 10.589297 5.9296875 10.529297 L 15.839844 4.8105469 C 15.929844 4.7505469 16.050391 4.7505469 16.150391 4.8105469 L 26.060547 10.529297 C 26.160547 10.589297 26.220703 10.690781 26.220703 10.800781 L 26.220703 21.179688 C 26.220703 21.289687 26.160313 21.399219 26.070312 21.449219 L 16.150391 27.179688 C 16.060391 27.229688 15.929844 27.229688 15.839844 27.179688 L 13.289062 25.669922 C 13.219062 25.619922 13.120781 25.610391 13.050781 25.650391 C 12.340781 26.050391 12.210781 26.100078 11.550781 26.330078 C 11.390781 26.380078 11.140625 26.479766 11.640625 26.759766 L 14.949219 28.720703 C 15.269219 28.900703 15.630234 29 15.990234 29 C 16.360234 29 16.719062 28.900703 17.039062 28.720703 L 26.960938 22.990234 C 27.600938 22.620234 28 21.929688 28 21.179688 L 28 10.810547 C 28 10.060547 27.600938 9.37 26.960938 9 L 17.039062 3.2695312 C 16.724063 3.0895313 16.359141 3 15.994141 3 z M 18.660156 11.005859 C 15.830156 11.005859 14.140625 12.205078 14.140625 14.205078 C 14.140625 16.375078 15.819062 16.974141 18.539062 17.244141 C 21.789062 17.564141 22.039062 18.045547 22.039062 18.685547 C 22.039062 19.785547 21.150547 20.255859 19.060547 20.255859 C 16.430547 20.255859 15.850156 19.594922 15.660156 18.294922 C 15.640156 18.154922 15.520859 18.054688 15.380859 18.054688 L 14.089844 18.054688 C 13.929844 18.054688 13.810547 18.185938 13.810547 18.335938 C 13.810547 20.005937 14.720547 21.994141 19.060547 21.994141 C 22.200547 21.994141 24 20.755703 24 18.595703 C 24 16.455703 22.549766 15.884609 19.509766 15.474609 C 16.419766 15.074609 16.109375 14.864531 16.109375 14.144531 C 16.109375 13.544531 16.380156 12.755859 18.660156 12.755859 C 20.690156 12.755859 21.449766 13.194453 21.759766 14.564453 C 21.789766 14.694453 21.899062 14.794922 22.039062 14.794922 L 23.330078 14.794922 C 23.410078 14.794922 23.479063 14.755313 23.539062 14.695312 C 23.589062 14.645313 23.619375 14.564609 23.609375 14.474609 C 23.409375 12.114609 21.840156 11.005859 18.660156 11.005859 z"})}),fo=()=>e("svg",{width:"32",height:"32",viewBox:"0 0 32 32",fill:"none",xmlns:"http://www.w3.org/2000/svg",children:e("path",{d:"M15.357 4L26.714 27H4L15.357 4Z",fill:"var(--ac-global-text-color-900)"})}),E6=()=>e("svg",{width:"32",height:"32",viewBox:"0 0 40 40",version:"1.1",xmlns:"http://www.w3.org/2000/svg",children:s("g",{stroke:"none",strokeWidth:"1",fill:"none",fillRule:"evenodd",children:[e("g",{id:"Icon-Architecture-BG/32/Machine-Learning",fill:"#01A88D",children:e("rect",{id:"Rectangle",x:"0",y:"0",width:"40",height:"40"})}),e("g",{id:"Icon-Service/32/Amazon-Bedrock_32",transform:"translate(6.000000, 6.000000)",fill:"#FFFFFF",children:e("path",{d:"M10.516,26.9332116 L8.293,25.6632116 L11.724,23.9472116 L11.277,23.0532116 L7.277,25.0532116 L7.297,25.0942116 L4,23.2102116 L4,19.8092116 L7.724,17.9472116 L7.277,17.0532116 L3.536,18.9232116 L1,17.2322116 L1,14.8092116 L4.724,12.9472116 L4.277,12.0532116 L1,13.6912116 L1,10.7672116 L3.523,9.08621158 L7,11.0382116 L7,14.1912116 L5.277,15.0532116 L5.724,15.9472116 L7.5,15.0592116 L9.277,15.9472116 L9.724,15.0532116 L8,14.1912116 L8,10.7672116 L10.778,8.91621158 C10.916,8.82321158 11,8.66721158 11,8.50021158 L11,5.00021158 L10,5.00021158 L10,8.23221158 L7.278,10.0472116 L4,8.20721158 L4,4.03521158 L7,2.65721158 L7,7.00021158 L8,7.00021158 L8,2.19821158 L10.492,1.05421158 L14,2.80921158 L14,17.1912116 L6.277,21.0532116 L6.724,21.9472116 L14,18.3092116 L14,25.1912116 L10.516,26.9332116 Z M25.5,19.5002116 C25.5,20.0512116 25.052,20.5002116 24.5,20.5002116 C23.949,20.5002116 23.5,20.0512116 23.5,19.5002116 C23.5,18.9492116 23.949,18.5002116 24.5,18.5002116 C25.052,18.5002116 25.5,18.9492116 25.5,19.5002116 L25.5,19.5002116 Z M20.5,24.0002116 C20.5,24.5512116 20.052,25.0002116 19.5,25.0002116 C18.949,25.0002116 18.5,24.5512116 18.5,24.0002116 C18.5,23.4492116 18.949,23.0002116 19.5,23.0002116 C20.052,23.0002116 20.5,23.4492116 20.5,24.0002116 L20.5,24.0002116 Z M19.5,4.00021158 C19.5,3.44921158 19.949,3.00021158 20.5,3.00021158 C21.052,3.00021158 21.5,3.44921158 21.5,4.00021158 C21.5,4.55121158 21.052,5.00021158 20.5,5.00021158 C19.949,5.00021158 19.5,4.55121158 19.5,4.00021158 L19.5,4.00021158 Z M26,11.5002116 C26.552,11.5002116 27,11.9492116 27,12.5002116 C27,13.0512116 26.552,13.5002116 26,13.5002116 C25.449,13.5002116 25,13.0512116 25,12.5002116 C25,11.9492116 25.449,11.5002116 26,11.5002116 L26,11.5002116 Z M24.071,13.0002116 C24.295,13.8602116 25.071,14.5002116 26,14.5002116 C27.103,14.5002116 28,13.6032116 28,12.5002116 C28,11.3972116 27.103,10.5002116 26,10.5002116 C25.071,10.5002116 24.295,11.1402116 24.071,12.0002116 L15,12.0002116 L15,9.00021158 L20.5,9.00021158 C20.777,9.00021158 21,8.77621158 21,8.50021158 L21,5.92921158 C21.86,5.70521158 22.5,4.92921158 22.5,4.00021158 C22.5,2.89721158 21.603,2.00021158 20.5,2.00021158 C19.398,2.00021158 18.5,2.89721158 18.5,4.00021158 C18.5,4.92921158 19.14,5.70521158 20,5.92921158 L20,8.00021158 L15,8.00021158 L15,2.50021158 C15,2.31021158 14.893,2.13821158 14.724,2.05321158 L10.724,0.0532115843 C10.588,-0.0147884157 10.43,-0.0177884157 10.291,0.0452115843 L3.291,3.26021158 C3.115,3.34121158 3,3.51921158 3,3.71421158 L3,8.23221158 L0.223,10.0842116 C0.084,10.1772116 0,10.3332116 0,10.5002116 L0,17.5002116 C0,17.6672116 0.084,17.8232116 0.223,17.9162116 L3,19.7672116 L3,23.5002116 C3,23.6792116 3.096,23.8452116 3.252,23.9342116 L10.252,27.9342116 C10.329,27.9782116 10.414,28.0002116 10.5,28.0002116 C10.577,28.0002116 10.654,27.9822116 10.724,27.9472116 L14.724,25.9472116 C14.893,25.8622116 15,25.6892116 15,25.5002116 L15,21.0002116 L19,21.0002116 L19,22.0712116 C18.14,22.2952116 17.5,23.0712116 17.5,24.0002116 C17.5,25.1032116 18.398,26.0002116 19.5,26.0002116 C20.603,26.0002116 21.5,25.1032116 21.5,24.0002116 C21.5,23.0712116 20.86,22.2952116 20,22.0712116 L20,20.5002116 C20,20.2242116 19.777,20.0002116 19.5,20.0002116 L15,20.0002116 L15,17.0002116 L21.293,17.0002116 L22.784,18.4902116 C22.608,18.7882116 22.5,19.1302116 22.5,19.5002116 C22.5,20.6032116 23.398,21.5002116 24.5,21.5002116 C25.603,21.5002116 26.5,20.6032116 26.5,19.5002116 C26.5,18.3972116 25.603,17.5002116 24.5,17.5002116 C24.131,17.5002116 23.788,17.6082116 23.491,17.7832116 L21.854,16.1462116 C21.76,16.0532116 21.633,16.0002116 21.5,16.0002116 L15,16.0002116 L15,13.0002116 L24.071,13.0002116 Z",id:"Fill-5"})})]})}),D6=()=>s("svg",{width:"32",height:"32",style:{flex:"none",lineHeight:"1"},viewBox:"0 0 24 24",xmlns:"http://www.w3.org/2000/svg",children:[e("title",{children:"HuggingFace"}),s("g",{fill:"none",fillRule:"nonzero",children:[e("path",{d:"M2.25 11.535c0-3.407 1.847-6.554 4.844-8.258a9.822 9.822 0 019.687 0c2.997 1.704 4.844 4.851 4.844 8.258 0 5.266-4.337 9.535-9.687 9.535S2.25 16.8 2.25 11.535z",fill:"#FF9D0B"}),e("path",{d:"M11.938 20.086c4.797 0 8.687-3.829 8.687-8.551 0-4.722-3.89-8.55-8.687-8.55-4.798 0-8.688 3.828-8.688 8.55 0 4.722 3.89 8.55 8.688 8.55z",fill:"#FFD21E"}),e("path",{d:"M11.875 15.113c2.457 0 3.25-2.156 3.25-3.263 0-.576-.393-.394-1.023-.089-.582.283-1.365.675-2.224.675-1.798 0-3.25-1.693-3.25-.586 0 1.107.79 3.263 3.25 3.263h-.003z",fill:"#FF323D"}),e("path",{d:"M14.76 9.21c.32.108.445.753.767.585.447-.233.707-.708.659-1.204a1.235 1.235 0 00-.879-1.059 1.262 1.262 0 00-1.33.394c-.322.384-.377.92-.14 1.36.153.283.638-.177.925-.079l-.002.003zm-5.887 0c-.32.108-.448.753-.768.585a1.226 1.226 0 01-.658-1.204c.048-.495.395-.913.878-1.059a1.262 1.262 0 011.33.394c.322.384.377.92.14 1.36-.152.283-.64-.177-.925-.079l.003.003zm1.12 5.34a2.166 2.166 0 011.325-1.106c.07-.02.144.06.219.171l.192.306c.069.1.139.175.209.175.074 0 .15-.074.223-.172l.205-.302c.08-.11.157-.188.234-.165.537.168.986.536 1.25 1.026.932-.724 1.275-1.905 1.275-2.633 0-.508-.306-.426-.81-.19l-.616.296c-.52.24-1.148.48-1.824.48-.676 0-1.302-.24-1.823-.48l-.589-.283c-.52-.248-.838-.342-.838.177 0 .703.32 1.831 1.187 2.56l.18.14z",fill:"#3A3B45"}),e("path",{d:"M17.812 10.366a.806.806 0 00.813-.8c0-.441-.364-.8-.813-.8a.806.806 0 00-.812.8c0 .442.364.8.812.8zm-11.624 0a.806.806 0 00.812-.8c0-.441-.364-.8-.812-.8a.806.806 0 00-.813.8c0 .442.364.8.813.8zM4.515 13.073c-.405 0-.765.162-1.017.46a1.455 1.455 0 00-.333.925 1.801 1.801 0 00-.485-.074c-.387 0-.737.146-.985.409a1.41 1.41 0 00-.2 1.722 1.302 1.302 0 00-.447.694c-.06.222-.12.69.2 1.166a1.267 1.267 0 00-.093 1.236c.238.533.81.958 1.89 1.405l.24.096c.768.3 1.473.492 1.478.494.89.243 1.808.375 2.732.394 1.465 0 2.513-.443 3.115-1.314.93-1.342.842-2.575-.274-3.763l-.151-.154c-.692-.684-1.155-1.69-1.25-1.912-.195-.655-.71-1.383-1.562-1.383-.46.007-.889.233-1.15.605-.25-.31-.495-.553-.715-.694a1.87 1.87 0 00-.993-.312zm14.97 0c.405 0 .767.162 1.017.46.216.262.333.588.333.925.158-.047.322-.071.487-.074.388 0 .738.146.985.409a1.41 1.41 0 01.2 1.722c.22.178.377.422.445.694.06.222.12.69-.2 1.166.244.37.279.836.093 1.236-.238.533-.81.958-1.889 1.405l-.239.096c-.77.3-1.475.492-1.48.494-.89.243-1.808.375-2.732.394-1.465 0-2.513-.443-3.115-1.314-.93-1.342-.842-2.575.274-3.763l.151-.154c.695-.684 1.157-1.69 1.252-1.912.195-.655.708-1.383 1.56-1.383.46.007.889.233 1.15.605.25-.31.495-.553.718-.694.244-.162.523-.265.814-.3l.176-.012z",fill:"#FF9D0B"}),e("path",{d:"M9.785 20.132c.688-.994.638-1.74-.305-2.667-.945-.928-1.495-2.288-1.495-2.288s-.205-.788-.672-.714c-.468.074-.81 1.25.17 1.971.977.721-.195 1.21-.573.534-.375-.677-1.405-2.416-1.94-2.751-.532-.332-.907-.148-.782.541.125.687 2.357 2.35 2.14 2.707-.218.362-.983-.42-.983-.42S2.953 14.9 2.43 15.46c-.52.558.398 1.026 1.7 1.803 1.308.778 1.41.985 1.225 1.28-.187.295-3.07-2.1-3.34-1.083-.27 1.011 2.943 1.304 2.745 2.006-.2.7-2.265-1.324-2.685-.537-.425.79 2.913 1.718 2.94 1.725 1.075.276 3.813.859 4.77-.522zm4.432 0c-.687-.994-.64-1.74.305-2.667.943-.928 1.493-2.288 1.493-2.288s.205-.788.675-.714c.465.074.807 1.25-.17 1.971-.98.721.195 1.21.57.534.377-.677 1.407-2.416 1.94-2.751.532-.332.91-.148.782.541-.125.687-2.355 2.35-2.137 2.707.215.362.98-.42.98-.42S21.05 14.9 21.57 15.46c.52.558-.395 1.026-1.7 1.803-1.308.778-1.408.985-1.225 1.28.187.295 3.07-2.1 3.34-1.083.27 1.011-2.94 1.304-2.743 2.006.2.7 2.263-1.324 2.685-.537.423.79-2.912 1.718-2.94 1.725-1.077.276-3.815.859-4.77-.522z",fill:"#FFD21E"})]})]}),_6=()=>e("svg",{width:"32",height:"32",viewBox:"0 0 27.82 27.83",fill:"var(--ac-global-text-color-900)",xmlns:"http://www.w3.org/2000/svg",children:e("g",{id:"icons",children:s("g",{children:[e("path",{d:"m16.02,27.83h0c-1.48,0-2.97-.57-4.1-1.7-2.26-2.26-2.26-5.94,0-8.2l9.9-9.9v14c0,1.6-.65,3.05-1.7,4.1h0c-.56.56-1.2.98-1.88,1.26-.68.28-1.43.44-2.22.44Z"}),e("path",{d:"m5.8,17.61c-1.48,0-2.97-.57-4.1-1.7C.57,14.78,0,13.3,0,11.82h0c0-.76.15-1.49.42-2.16.28-.71.71-1.37,1.28-1.94h0c1.05-1.05,2.5-1.7,4.1-1.7h14s-9.9,9.89-9.9,9.89c-1.13,1.13-2.61,1.7-4.1,1.7Z"}),e("path",{d:"m24.41,8.44c-.78-.78-.78-2.05,0-2.83s2.05-.78,2.83,0,.78,2.05,0,2.83-2.05.78-2.83,0Z"}),e("path",{d:"m19.39,3.42c-.78-.78-.78-2.05,0-2.83s2.05-.78,2.83,0,.78,2.05,0,2.83-2.05.78-2.83,0Z"})]})})}),Kl=()=>e("svg",{width:"32",height:"32",viewBox:"0 0 32 32",fill:"none",xmlns:"http://www.w3.org/2000/svg",children:e("path",{fillRule:"evenodd",clipRule:"evenodd",d:"M19.2593 6.61905C19.0126 7.16696 18.7815 8.04669 18.5292 9.00706C18.4235 9.40941 18.3141 9.82591 18.1982 10.2381H23.1482C23.7004 10.2381 24.1482 10.6858 24.1482 11.2381V17.0307C24.5195 16.902 24.8948 16.7804 25.2572 16.663C26.122 16.383 26.9141 16.1264 27.4074 15.8525C29.0175 14.9587 30.6667 17.4728 30.6667 19.4716C30.6667 21.4703 29.0371 23.9954 27.4074 23.0906C26.914 22.8166 26.1217 22.56 25.2569 22.2799L25.2568 22.2799C24.8945 22.1625 24.5194 22.041 24.1482 21.9124V27.3333C24.1482 27.8856 23.7004 28.3333 23.1482 28.3333H8.85186C8.29957 28.3333 7.85186 27.8856 7.85186 27.3333V21.9159C7.48052 22.0446 7.10529 22.1662 6.74283 22.2836C5.8781 22.5636 5.086 22.8202 4.59263 23.0941C2.98259 23.9879 1.33337 21.4738 1.33337 19.475C1.33337 17.4763 2.963 14.9511 4.59263 15.856C5.08608 16.13 5.87835 16.3866 6.74324 16.6667C7.10558 16.7841 7.48066 16.9056 7.85186 17.0342V11.2381C7.85186 10.6858 8.29957 10.2381 8.85186 10.2381H13.8018C13.686 9.82578 13.5765 9.40914 13.4708 9.00667L13.4708 9.00661L13.4708 9.00659L13.4707 9.00657L13.4707 9.00656C13.2185 8.04639 12.9875 7.16687 12.7408 6.61905C11.9359 4.83128 14.2 3 16.0001 3C17.8001 3 20.0742 4.80952 19.2593 6.61905ZM12.2564 21.0247C11.9603 21.3049 11.5203 21.259 11.2731 20.9233C11.0258 20.5877 11.0663 20.0881 11.3625 19.8087L15.5529 15.8503C15.5746 15.8294 15.5991 15.8157 15.6237 15.8019C15.6363 15.7949 15.6489 15.7879 15.6611 15.7799C15.6701 15.7739 15.6788 15.7676 15.6874 15.7614C15.7062 15.7477 15.7248 15.7342 15.7464 15.7245C15.8281 15.688 15.9133 15.6667 15.9999 15.6667C16.0865 15.6667 16.1717 15.688 16.2534 15.7245C16.275 15.7342 16.2936 15.7478 16.3124 15.7614C16.321 15.7676 16.3296 15.7739 16.3386 15.7799C16.3509 15.7879 16.3635 15.7949 16.376 15.8019C16.4006 15.8157 16.4251 15.8294 16.4469 15.8503L20.6373 19.8087C20.9341 20.0881 20.9739 20.5877 20.7267 20.9233C20.4801 21.259 20.0402 21.3049 19.7433 21.0247L16.6983 18.1485V28.3333H15.9999H15.1852L15.3015 18.1485L12.2564 21.0247Z",fill:"var(--ac-global-text-color-900)"})}),K6=()=>s("svg",{width:"32",height:"32",viewBox:"0 0 16 16",fill:"none",xmlns:"http://www.w3.org/2000/svg",children:[e("g",{clipPath:"url(#clip0_2815_4632)",children:e("path",{fillRule:"evenodd",clipRule:"evenodd",d:"M15.7469 1.84196C16.0957 2.52647 16.0957 3.42256 16.0957 5.21473V10.9752C16.0957 12.7674 16.0957 13.6634 15.7469 14.348C15.4401 14.9501 14.9506 15.4396 14.3485 15.7464C13.6639 16.0952 12.7679 16.0952 10.9757 16.0952H5.21522C3.42305 16.0952 2.52696 16.0952 1.84245 15.7464C1.24033 15.4396 0.750789 14.9501 0.443994 14.348C0.0952148 13.6634 0.0952148 12.7674 0.0952148 10.9752V5.21473C0.0952148 3.42256 0.0952148 2.52647 0.443994 1.84196C0.750789 1.23984 1.24033 0.7503 1.84245 0.443506C2.52696 0.0947266 3.42305 0.0947266 5.21521 0.0947266H10.9757C12.7678 0.0947266 13.6639 0.0947266 14.3485 0.443506C14.9506 0.7503 15.4401 1.23984 15.7469 1.84196ZM5.27398 3.77524H9.3046L12.594 12.0905H10.9168L8.32056 5.18973H5.27398V3.77524ZM2.99402 10.676H7.12113V12.0905H2.99402V10.676Z",fill:"#FF4017"})}),e("defs",{children:e("clipPath",{id:"clip0_2815_4632",children:e("rect",{width:"16",height:"16",fill:"white"})})})]}),bo=()=>s("svg",{width:"32",height:"32",fill:"currentColor",fillRule:"evenodd",viewBox:"0 0 24 24",xmlns:"http://www.w3.org/2000/svg",children:[e("title",{children:"ModelContextProtocol"}),e("path",{d:"M15.688 2.343a2.588 2.588 0 00-3.61 0l-9.626 9.44a.863.863 0 01-1.203 0 .823.823 0 010-1.18l9.626-9.44a4.313 4.313 0 016.016 0 4.116 4.116 0 011.204 3.54 4.3 4.3 0 013.609 1.18l.05.05a4.115 4.115 0 010 5.9l-8.706 8.537a.274.274 0 000 .393l1.788 1.754a.823.823 0 010 1.18.863.863 0 01-1.203 0l-1.788-1.753a1.92 1.92 0 010-2.754l8.706-8.538a2.47 2.47 0 000-3.54l-.05-.049a2.588 2.588 0 00-3.607-.003l-7.172 7.034-.002.002-.098.097a.863.863 0 01-1.204 0 .823.823 0 010-1.18l7.273-7.133a2.47 2.47 0 00-.003-3.537z"}),e("path",{d:"M14.485 4.703a.823.823 0 000-1.18.863.863 0 00-1.204 0l-7.119 6.982a4.115 4.115 0 000 5.9 4.314 4.314 0 006.016 0l7.12-6.982a.823.823 0 000-1.18.863.863 0 00-1.204 0l-7.119 6.982a2.588 2.588 0 01-3.61 0 2.47 2.47 0 010-3.54l7.12-6.982z"})]}),P6=()=>s("svg",{width:"32",height:"32",viewBox:"0 0 24 24",xmlns:"http://www.w3.org/2000/svg",children:[e("title",{children:"Gemini"}),e("defs",{children:s("linearGradient",{id:"lobe-icons-gemini-fill",x1:"0%",x2:"68.73%",y1:"100%",y2:"30.395%",children:[e("stop",{offset:"0%",stopColor:"#1C7DFF"}),e("stop",{offset:"52.021%",stopColor:"#1C69FF"}),e("stop",{offset:"100%",stopColor:"#F0DCD6"})]})}),e("path",{d:"M12 24A14.304 14.304 0 000 12 14.304 14.304 0 0012 0a14.305 14.305 0 0012 12 14.305 14.305 0 00-12 12",fill:"url(#lobe-icons-gemini-fill)",fillRule:"nonzero"})]}),V6=()=>s("svg",{width:"32",height:"32",viewBox:"0 0 115 115",xmlns:"http://www.w3.org/2000/svg","aria-hidden":"true",focusable:"false",children:[e("path",{fill:"#FFBDDB",d:"M62.3737 105.707C59.5781 109.547 53.8509 109.547 51.0553 105.707L27.7796 73.7344C25.0105 69.9307 26.7073 64.5329 31.1546 62.9977L54.4303 54.9628C55.9102 54.4519 57.5187 54.4519 58.9987 54.9628L82.2744 62.9977C86.7217 64.533 88.4184 69.9307 85.6494 73.7344L62.3737 105.707ZM56.7145 99.8879L78.3862 70.1187L56.7145 62.6375L35.0428 70.1187L56.7145 99.8879Z"}),e("path",{fill:"#FFBDDB",d:"M110.86 62.2624C113.648 66.1079 111.878 71.5547 107.362 73.0268L69.7621 85.2833C65.2889 86.7414 60.6796 83.4597 60.5938 78.7556L60.1447 54.1362C60.1162 52.5708 60.6132 51.0411 61.5564 49.7914L76.3907 30.1379C79.2251 26.3826 84.883 26.4369 87.6448 30.2459L110.86 62.2624ZM103.577 65.8465L81.9617 36.0363L68.1497 54.3355L68.5678 77.2583L103.577 65.8465Z"}),e("path",{fill:"#FFBDDB",d:"M84.5326 2.75877C89.0515 1.29523 93.6849 4.66159 93.6894 9.41158L93.7269 48.9589C93.7314 53.6638 89.1859 57.0333 84.6856 55.6613L61.1323 48.4806C59.6347 48.024 58.3334 47.0786 57.4364 45.7954L43.3288 25.6139C40.6333 21.7577 42.4333 16.3935 46.9092 14.9439L84.5326 2.75877ZM85.6907 10.7928L50.6601 22.1382L63.7955 40.929L85.7256 47.6148L85.6907 10.7928Z"}),e("path",{fill:"#FFBDDB",d:"M28.9346 2.77586C24.4156 1.31232 19.7823 4.67868 19.7778 9.42867L19.7402 48.976C19.7358 53.6809 24.2812 57.0504 28.7816 55.6784L52.3348 48.4977C53.8324 48.0411 55.1337 47.0957 56.0307 45.8125L70.1383 25.6309C72.8339 21.7748 71.0339 16.4106 66.5579 14.961L28.9346 2.77586ZM27.7765 10.8099L62.8071 22.1553L49.6717 40.9461L27.7415 47.6319L27.7765 10.8099Z"}),e("path",{fill:"#FFBDDB",d:"M2.58066 62.2555C-0.20768 66.101 1.56213 71.5479 6.07825 73.02L43.6784 85.2765C48.1516 86.7346 52.7608 83.4529 52.8467 78.7488L53.2958 54.1294C53.3243 52.564 52.8273 51.0342 51.8841 49.7846L37.0498 30.131C34.2154 26.3758 28.5575 26.4301 25.7956 30.239L2.58066 62.2555ZM9.8636 65.8396L31.4788 36.0294L45.2908 54.3286L44.8726 77.2515L9.8636 65.8396Z"}),e("path",{fill:"white",d:"M79.5687 82.0867L85.6488 73.7348C86.1993 72.9787 86.5733 72.1596 86.7842 71.3204L74.626 75.2836L67.1038 85.6164C67.9705 85.6767 68.8689 85.5745 69.7619 85.2835L79.5687 82.0867Z"}),e("path",{fill:"white",d:"M60.167 55.3667L60.3224 63.8836L68.3744 66.6632L68.219 58.1463L60.167 55.3667Z"}),e("path",{fill:"white",d:"M93.7166 38.62L87.6446 30.2459C87.0975 29.4914 86.4368 28.8842 85.7069 28.4248L85.7191 41.2186L93.2279 51.5742C93.5492 50.7726 93.7273 49.8919 93.7264 48.9587L93.7166 38.62Z"}),e("path",{fill:"white",d:"M70.4293 51.3149L62.2812 48.8308L67.413 42.0318L75.5611 44.5159L70.4293 51.3149Z"}),e("path",{fill:"white",d:"M56.7395 44.7982L61.6199 37.8166L56.7395 30.8349L51.859 37.8166L56.7395 44.7982Z"}),e("path",{fill:"white",d:"M44.5547 16.2438C45.2222 15.6823 46.012 15.2344 46.9092 14.9438L56.7071 11.7705L66.5577 14.9608C67.4418 15.2472 68.2215 15.6862 68.8828 16.2363L56.7071 20.1796L44.5547 16.2438Z"}),e("path",{fill:"white",d:"M51.1787 48.8499L46.0469 42.0509L37.8988 44.535L43.0306 51.334L51.1787 48.8499Z"}),e("path",{fill:"white",d:"M20.2233 51.5523L27.7476 41.1752L27.7598 28.4014C27.0194 28.8627 26.3494 29.4754 25.7957 30.239L19.7501 38.5767L19.7402 48.9757C19.7394 49.8938 19.9118 50.7611 20.2233 51.5523Z"}),e("path",{fill:"white",d:"M53.2727 55.3623L45.2207 58.1419L45.0653 66.6588L53.1174 63.8792L53.2727 55.3623Z"}),e("path",{fill:"white",d:"M46.3199 85.6104L38.7916 75.2693L26.6406 71.3084C26.8511 72.1518 27.226 72.9749 27.779 73.7346L33.8488 82.0724L43.6778 85.2763C44.5653 85.5656 45.4581 85.6683 46.3199 85.6104Z"})]}),R6=()=>s("svg",{width:"32",height:"32",viewBox:"0 0 16 16",fill:"none",xmlns:"http://www.w3.org/2000/svg",children:[s("g",{clipPath:"url(#clip0_756_3354)",children:[e("path",{fillRule:"evenodd",clipRule:"evenodd",d:"M8.69139 10.1458C8.89799 10.3937 8.8645 10.7622 8.61657 10.9688L7.07351 12.2547L8.61657 13.5406C8.8645 13.7472 8.89799 14.1157 8.69139 14.3636C8.48478 14.6115 8.11631 14.645 7.86838 14.4384L5.82029 12.7317C5.52243 12.4834 5.52242 12.026 5.82029 11.7777L7.86838 10.071C8.11631 9.86438 8.48478 9.89788 8.69139 10.1458Z",fill:"#EA4335"}),e("path",{fillRule:"evenodd",clipRule:"evenodd",d:"M11.4459 10.1458C11.2393 10.3937 11.2728 10.7622 11.5207 10.9688L13.0638 12.2547L11.5207 13.5406C11.2728 13.7472 11.2393 14.1157 11.4459 14.3636C11.6525 14.6115 12.021 14.645 12.2689 14.4384L14.317 12.7317C14.6149 12.4834 14.6149 12.026 14.317 11.7777L12.2689 10.071C12.021 9.86438 11.6525 9.89788 11.4459 10.1458Z",fill:"#EA4335"}),e("path",{fillRule:"evenodd",clipRule:"evenodd",d:"M5.94165 2.19288C4.44903 2.19288 3.23902 3.40289 3.23902 4.89551C3.23902 6.38813 4.44903 7.59814 5.94165 7.59814H8.60776V8.76685H5.94165C3.80357 8.76685 2.07031 7.03359 2.07031 4.89551C2.07031 2.75743 3.80357 1.02417 5.94165 1.02417H9.73995C10.0627 1.02417 10.3243 1.28579 10.3243 1.60852C10.3243 1.93125 10.0627 2.19288 9.73995 2.19288H5.94165Z",fill:"#4285F4"}),e("path",{fillRule:"evenodd",clipRule:"evenodd",d:"M10.6895 2.19288C12.1821 2.19288 13.3922 3.40289 13.3922 4.89551C13.3922 6.38813 12.1821 7.59814 10.6895 7.59814H6.89123C6.5685 7.59814 6.30687 7.85977 6.30687 8.1825C6.30687 8.50523 6.5685 8.76685 6.89123 8.76685H10.6895C12.8276 8.76685 14.5609 7.03359 14.5609 4.89551C14.5609 2.75743 12.8276 1.02417 10.6895 1.02417H6.89123C6.5685 1.02417 6.30687 1.28579 6.30687 1.60852C6.30687 1.93125 6.5685 2.19288 6.89123 2.19288H10.6895Z",fill:"#34A853"}),e("path",{fillRule:"evenodd",clipRule:"evenodd",d:"M3.23902 10.739H4.18859C4.51132 10.739 4.77295 10.4774 4.77295 10.1547C4.77295 9.83196 4.51132 9.57033 4.18859 9.57033H3.01989C2.49545 9.57033 2.07031 9.99547 2.07031 10.5199V14.026C2.07031 14.5505 2.49545 14.9756 3.01989 14.9756H4.18859C4.51132 14.9756 4.77295 14.714 4.77295 14.3912C4.77295 14.0685 4.51132 13.8069 4.18859 13.8069H3.23902V10.739Z",fill:"#FBBC04"}),e("path",{fillRule:"evenodd",clipRule:"evenodd",d:"M10.9452 8.1825C10.9452 7.85977 10.6836 7.59814 10.3608 7.59814H6.89123C6.5685 7.59814 6.30687 7.85977 6.30687 8.1825C6.30687 8.50523 6.5685 8.76685 6.89123 8.76685H10.3608C10.6836 8.76685 10.9452 8.50523 10.9452 8.1825Z",fill:"#4285F4"}),e("path",{d:"M6.74514 4.89551C6.74514 5.25858 6.45081 5.55291 6.08774 5.55291C5.72467 5.55291 5.43034 5.25858 5.43034 4.89551C5.43034 4.53244 5.72467 4.23811 6.08774 4.23811C6.45081 4.23811 6.74514 4.53244 6.74514 4.89551Z",fill:"#4285F4"}),e("path",{d:"M11.2739 4.89551C11.2739 5.25858 10.9795 5.55291 10.6165 5.55291C10.2534 5.55291 9.95908 5.25858 9.95908 4.89551C9.95908 4.53244 10.2534 4.23811 10.6165 4.23811C10.9795 4.23811 11.2739 4.53244 11.2739 4.89551Z",fill:"#4285F4"})]}),e("defs",{children:e("clipPath",{id:"clip0_756_3354",children:e("rect",{width:"12.6294",height:"14",fill:"white",transform:"translate(2 1)"})})})]}),O6=()=>s("svg",{width:"32",height:"32",viewBox:"0 0 34 34",fill:"none",xmlns:"http://www.w3.org/2000/svg",children:[e("circle",{cx:"16.6532",cy:"16.9999",r:"14.0966",stroke:"currentColor",strokeWidth:"1.16026"}),e("ellipse",{cx:"16.6533",cy:"17",rx:"14.0966",ry:"9.45478",transform:"rotate(45 16.6533 17)",stroke:"currentColor",strokeWidth:"1.16026"}),e("path",{d:"M10.8984 17.0508H22.483",stroke:"currentColor",strokeWidth:"1.16026"}),e("path",{d:"M13.748 19.9932L19.6339 14.1074",stroke:"currentColor",strokeWidth:"1.16026"}),e("path",{d:"M19.6328 19.9932L13.747 14.1074",stroke:"currentColor",strokeWidth:"1.16026"}),e("path",{fillRule:"evenodd",clipRule:"evenodd",d:"M7.00863 10.796C4.56184 12.4371 3.13683 14.6416 3.13683 16.9998C3.13683 19.3579 4.56184 21.5624 7.00863 23.2035C9.45169 24.8421 12.8599 25.8744 16.6533 25.8744C20.4467 25.8744 23.8548 24.8421 26.2979 23.2035C28.7447 21.5624 30.1697 19.3579 30.1697 16.9998C30.1697 14.6416 28.7447 12.4371 26.2979 10.796C23.8548 9.15742 20.4467 8.12511 16.6533 8.12511C12.8599 8.12511 9.45169 9.15742 7.00863 10.796ZM6.36234 9.83242C9.02124 8.04906 12.6613 6.96484 16.6533 6.96484C20.6452 6.96484 24.2853 8.04906 26.9442 9.83242C29.5994 11.6133 31.33 14.1362 31.33 16.9998C31.33 19.8633 29.5994 22.3862 26.9442 24.1671C24.2853 25.9505 20.6452 27.0347 16.6533 27.0347C12.6613 27.0347 9.02124 25.9505 6.36234 24.1671C3.70718 22.3862 1.97656 19.8633 1.97656 16.9998C1.97656 14.1362 3.70718 11.6133 6.36234 9.83242Z",fill:"currentColor"})]}),N6=m`
  border-radius: var(--ac-global-rounding-medium);
  border: 1px solid var(--ac-global-color-grey-400);
  padding: var(--ac-global-dimension-size-100)
    var(--ac-global-dimension-size-150);
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  gap: var(--ac-global-dimension-size-100);
  transition:
    background-color 0.2s ease-in-out,
    border-color 0.2s ease-in-out;
  &:hover {
    background-color: var(--ac-global-color-grey-100);
    border-color: var(--ac-global-color-primary);
  }
  min-width: 230px;
  .integration__main-link {
    flex: 1 1 auto;
    color: var(--ac-global-text-color-900);
    text-decoration: none;
    display: flex;
    flex-direction: row;
    align-items: center;
    gap: var(--ac-global-dimension-size-150);
  }
  .integration__github-link {
    color: var(--ac-global-color-grey-500);
    transition: color 0.2s ease-in-out;
    display: flex;
    align-items: center;
    &:hover {
      color: var(--ac-global-color-grey-700);
    }
  }
`;function Ut({docsHref:n,githubHref:a,icon:t,name:l}){return s("div",{css:N6,children:[s("a",{href:n,className:"integration__main-link",target:"_blank",rel:"noreferrer",children:[t,l]}),e("div",{children:e("a",{href:a,target:"_blank",rel:"noreferrer",className:"integration__github-link","aria-label":"GitHub link",children:e(G6,{})})})]})}const $6=[{name:"OpenAI",docsHref:"https://arize.com/docs/phoenix/tracing/integrations-tracing/openai",githubHref:"https://github.com/Arize-ai/openinference/tree/main/python/instrumentation/openinference-instrumentation-openai",icon:e(ut,{})},{name:"LlamaIndex",githubHref:"https://github.com/Arize-ai/openinference/tree/main/python/instrumentation/openinference-instrumentation-llama-index",docsHref:"https://arize.com/docs/phoenix/tracing/integrations-tracing/llamaindex",icon:e(w6,{})},{name:"LangChain",docsHref:"https://arize.com/docs/phoenix/tracing/integrations-tracing/langchain",githubHref:"https://github.com/Arize-ai/openinference/tree/main/python/instrumentation/openinference-instrumentation-langchain",icon:e(ho,{})},{name:"Haystack",docsHref:"https://arize.com/docs/phoenix/tracing/integrations-tracing/haystack",githubHref:"https://github.com/Arize-ai/openinference/tree/main/python/instrumentation/openinference-instrumentation-haystack",icon:e(S6,{})},{name:"Vertex AI",docsHref:"https://arize.com/docs/phoenix/tracing/integrations-tracing/vertex",githubHref:"https://github.com/Arize-ai/openinference/tree/main/python/instrumentation/openinference-instrumentation-vertexai",icon:e(T6,{})},{name:"Mistral AI",docsHref:"https://arize.com/docs/phoenix/tracing/integrations-tracing/mistralai",githubHref:"https://github.com/Arize-ai/openinference/tree/main/python/instrumentation/openinference-instrumentation-mistralai",icon:e(x6,{})},{name:"DSPy",docsHref:"https://arize.com/docs/phoenix/tracing/integrations-tracing/dspy",githubHref:"https://github.com/Arize-ai/openinference/tree/main/python/instrumentation/openinference-instrumentation-dspy",icon:e(A6,{})},{name:"Anthropic",docsHref:"https://arize.com/docs/phoenix/tracing/integrations-tracing/anthropic",githubHref:"https://github.com/Arize-ai/openinference/tree/main/python/instrumentation/openinference-instrumentation-anthropic",icon:e(I6,{})},{name:"Smolagents",docsHref:"https://arize.com/docs/phoenix/tracing/integrations-tracing/hfsmolagents",githubHref:"https://github.com/Arize-ai/openinference/tree/main/python/instrumentation/openinference-instrumentation-smolagents",icon:e(D6,{})},{name:"OpenAI Agents",docsHref:"https://arize.com/docs/phoenix/tracing/integrations-tracing/openai-agents-sdk",githubHref:"https://github.com/Arize-ai/openinference/tree/main/python/instrumentation/openinference-instrumentation-openai-agents",icon:e(ut,{})},{name:"Agno",docsHref:"https://arize.com/docs/phoenix/tracing/integrations-tracing/agno",githubHref:"https://github.com/Arize-ai/openinference/tree/main/python/instrumentation/openinference-instrumentation-agno",icon:e(K6,{})},{name:"Bedrock",docsHref:"https://arize.com/docs/phoenix/tracing/integrations-tracing/bedrock",githubHref:"https://github.com/Arize-ai/openinference/tree/main/python/instrumentation/openinference-instrumentation-bedrock",icon:e(E6,{})},{name:"Google GenAI",docsHref:"https://arize.com/docs/phoenix/tracing/integrations-tracing/google-genai",githubHref:"https://github.com/Arize-ai/openinference/tree/main/python/instrumentation/openinference-instrumentation-google-genai",icon:e(P6,{})},{name:"Google ADK",docsHref:"https://arize.com/docs/phoenix/integrations/llm-providers/google-gen-ai/google-adk-tracing",githubHref:"https://github.com/Arize-ai/openinference/tree/main/python/instrumentation/openinference-instrumentation-google-adk",icon:e(R6,{})},{name:"Groq",docsHref:"https://arize.com/docs/phoenix/tracing/integrations-tracing/groq",githubHref:"https://github.com/Arize-ai/openinference/tree/main/python/instrumentation/openinference-instrumentation-groq",icon:e(z6,{})},{name:"CrewAI",docsHref:"https://arize.com/docs/phoenix/tracing/integrations-tracing/crewai",githubHref:"https://github.com/Arize-ai/openinference/tree/main/python/instrumentation/openinference-instrumentation-crewai",icon:e(M6,{})},{name:"Pydantic AI",docsHref:"https://arize.com/docs/phoenix/integrations/pydantic/pydantic-tracing",githubHref:"https://github.com/Arize-ai/openinference/tree/main/python/instrumentation/openinference-instrumentation-pydantic-ai",icon:e(V6,{})},{name:"LiteLLM",docsHref:"https://arize.com/docs/phoenix/integrations/llm-providers/litellm",githubHref:"https://github.com/Arize-ai/openinference/tree/main/python/instrumentation/openinference-instrumentation-litellm",icon:e(Kl,{})},{name:"PortKey",docsHref:"https://arize.com/docs/phoenix/integrations/portkey",githubHref:"https://github.com/Arize-ai/openinference/tree/main/python/instrumentation/openinference-instrumentation-portkey",icon:e(Kl,{})},{name:"MCP",docsHref:"https://arize.com/docs/phoenix/integrations/model-context-protocol/mcp-tracing",githubHref:"https://github.com/Arize-ai/openinference/tree/main/python/instrumentation/openinference-instrumentation-mcp",icon:e(bo,{})}],Gt=m`
  width: 100%;
  display: flex;
  flex-direction: row;
  gap: var(--ac-global-dimension-size-100);
  flex-wrap: wrap;
`;function B6(){return e("ul",{css:Gt,children:$6.map(n=>e("li",{children:e(Ut,{...n},n.name)},n.name))})}const H6=[{name:"Node",docsHref:"https://opentelemetry.io/docs/languages/js/getting-started/nodejs/",githubHref:"https://github.com/open-telemetry/opentelemetry-js",icon:e(F6,{})},{name:"Vercel",docsHref:"https://vercel.com/docs/observability/otel-overview",githubHref:"https://github.com/vercel/otel",icon:e(fo,{})}];function j6(){return e("ul",{css:Gt,children:H6.map(n=>e("li",{children:e(Ut,{...n},n.name)},n.name))})}const Z6=[{name:"OpenAI NodeJS SDK",docsHref:"https://arize.com/docs/phoenix/tracing/integrations-tracing/openai-node-sdk",githubHref:"https://github.com/Arize-ai/openinference/tree/main/js/packages/openinference-vercel",icon:e(ut,{})},{name:"LangChain.js",docsHref:"https://arize.com/docs/phoenix/tracing/integrations-tracing/langchain.js",githubHref:"https://github.com/Arize-ai/openinference/tree/main/js/packages/openinference-instrumentation-langchain",icon:e(ho,{})},{name:"Vercel AI SDK",docsHref:"https://arize.com/docs/phoenix/tracing/integrations-tracing/vercel-ai-sdk",githubHref:"https://github.com/Arize-ai/openinference/tree/main/js/packages/openinference-vercel",icon:e(fo,{})},{name:"Mastra",docsHref:"https://arize.com/docs/phoenix/integrations/mastra/mastra-tracing",githubHref:"https://github.com/Arize-ai/openinference/tree/main/js/packages/openinference-mastra",icon:e(O6,{})},{name:"BeeAI",docsHref:"https://arize.com/docs/phoenix/tracing/integrations-tracing/beeai",githubHref:"https://github.com/Arize-ai/openinference/tree/main/js/packages/openinference-instrumentation-beeai",icon:e(_6,{})},{name:"MCP",docsHref:"https://arize.com/docs/phoenix/tracing/integrations-tracing/model-context-protocol-mcp",githubHref:"https://github.com/Arize-ai/openinference/tree/main/js/packages/openinference-instrumentation-mcp",icon:e(bo,{})}];function U6(){return e("ul",{css:Gt,children:Z6.map(n=>e("li",{children:e(Ut,{...n},n.name)},n.name))})}const G6=()=>e("svg",{xmlns:"http://www.w3.org/2000/svg",width:"20",height:"20",viewBox:"0 0 24 24",children:s("g",{"data-name":"Layer 2",children:[e("rect",{width:"24",height:"24",transform:"rotate(180 12 12)",opacity:"0"}),e("path",{d:"M12 1A10.89 10.89 0 0 0 1 11.77 10.79 10.79 0 0 0 8.52 22c.55.1.75-.23.75-.52v-1.83c-3.06.65-3.71-1.44-3.71-1.44a2.86 2.86 0 0 0-1.22-1.58c-1-.66.08-.65.08-.65a2.31 2.31 0 0 1 1.68 1.11 2.37 2.37 0 0 0 3.2.89 2.33 2.33 0 0 1 .7-1.44c-2.44-.27-5-1.19-5-5.32a4.15 4.15 0 0 1 1.11-2.91 3.78 3.78 0 0 1 .11-2.84s.93-.29 3 1.1a10.68 10.68 0 0 1 5.5 0c2.1-1.39 3-1.1 3-1.1a3.78 3.78 0 0 1 .11 2.84A4.15 4.15 0 0 1 19 11.2c0 4.14-2.58 5.05-5 5.32a2.5 2.5 0 0 1 .75 2v2.95c0 .35.2.63.75.52A10.8 10.8 0 0 0 23 11.77 10.89 10.89 0 0 0 12 1","data-name":"github",fill:"currentColor"})]})}),Q6="https://arize.com/docs/phoenix/tracing/how-to-tracing/setup-tracing",W6="https://arize.com/docs/phoenix/tracing/how-to-tracing/setup-tracing/setup-tracing-python/using-otel-python-directly",q6="https://arize.com/docs/phoenix/setup/configuration",X6="pip install arize-phoenix-otel",Y6="pip install openinference-instrumentation-openai openai";function J6({isAuthEnabled:n,isHosted:a}){return a?`PHOENIX_CLIENT_HEADERS='api_key=<your-api-key>'
PHOENIX_COLLECTOR_ENDPOINT='${Zt}'`:n?"PHOENIX_API_KEY='<your-api-key>'":`PHOENIX_COLLECTOR_ENDPOINT='${Tn}'`}const e7=`from openinference.instrumentation.openai import OpenAIInstrumentor

OpenAIInstrumentor().instrument(tracer_provider=tracer_provider)`,n7=`import os
from openai import OpenAI

client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "Say this is a test",
        }
    ],
    model="gpt-3.5-turbo",
)`,a7=({isHosted:n,projectName:a})=>`from phoenix.otel import register

tracer_provider = register(
  project_name="${a}",
  endpoint="${(n?Zt:Tn)+"/v1/traces"}",
  auto_instrument=True
)`;function _p(n){const a=po,t=window.Config.authenticationEnabled,l=J6({isAuthEnabled:t,isHosted:a}),i=n.projectName||"your-next-llm-project";return s("div",{children:[e(w,{paddingTop:"size-200",paddingBottom:"size-100",children:e(ne,{level:2,weight:"heavy",children:"Install Dependencies"})}),e(w,{paddingBottom:"size-100",children:s(C,{children:["Use the Phoenix OTEL or"," ",e(de,{href:W6,children:"OpenTelemetry"})," to configure your application to send traces to Phoenix."]})}),e(ve,{children:e(xe,{value:X6})}),e(w,{paddingTop:"size-200",paddingBottom:"size-100",children:e(ne,{level:2,weight:"heavy",children:"Setup your Environment"})}),e(w,{paddingBottom:"size-100",children:s(C,{children:[e("b",{children:"arize-phoenix-otel"})," automatically picks up your configuration from"," ",e(de,{href:q6,children:"environment variables"})]})}),e(ve,{children:e(xe,{value:l})}),t?e(w,{paddingBottom:"size-100",paddingTop:"size-100",children:e(pr,{fallback:s(C,{children:["Personal API keys can be created and managed on your"," ",e(de,{href:"/profile",children:"Profile"})]}),children:s(C,{children:["System API keys can be created and managed in"," ",e(de,{href:"/settings/general",children:"Settings"})]})})}):null,e(w,{paddingTop:"size-200",paddingBottom:"size-100",children:e(ne,{level:2,weight:"heavy",children:"Setup OpenTelemetry"})}),e(w,{paddingBottom:"size-100",children:s(C,{children:["Register your application to send traces to this project. The code below should be added ",e("b",{children:"BEFORE"})," any code execution."]})}),e(w,{paddingBottom:"size-100",children:e(ve,{children:e(xe,{value:a7({projectName:i,isHosted:a})})})}),a?null:e(w,{paddingBottom:"size-100",children:s(C,{children:["To configure gRPC and batching, see our"," ",e(de,{href:Q6,children:"setup guide"}),"."]})}),e(w,{paddingTop:"size-200",paddingBottom:"size-100",children:e(ne,{level:2,weight:"heavy",children:"Setup Instrumentation"})}),e(w,{paddingBottom:"size-100",children:e(C,{children:"Add instrumentation to your application so that your application code is traces."})}),e(ps,{variant:"compact",children:s(Ad,{children:[s(zd,{children:[e(dl,{id:"instrumentation",children:"Instrumentation"}),e(dl,{id:"openai-example",children:"OpenAI Example"})]}),e(lt,{id:"instrumentation",children:s(w,{padding:"size-200",children:[s(C,{children:["Trace your application using"," ",e(de,{href:"https://github.com/Arize-ai/openinference",children:"OpenInference"})," ","instrumentation and OpenTelemetry"]}),e(w,{paddingTop:"size-200",paddingBottom:"size-200",children:e(B6,{})}),s(C,{children:["For more integrations, checkout our"," ",e(de,{href:"https://arize.com/docs/phoenix/tracing/integrations-tracing",children:"comprehensive guide"})]})]})}),e(lt,{id:"openai-example",children:s(w,{padding:"size-200",children:[s("p",{children:["Install"," ",e(de,{href:"https://github.com/Arize-ai/openinference",children:"OpenInference"})," ","instrumentation as well as ",e("b",{children:"openai"})]}),e(ve,{children:e(xe,{value:Y6})}),s("p",{children:["Instrument ",e("b",{children:"openai"})," at the beginning of your code"]}),e(w,{paddingBottom:"size-50",children:e(ve,{children:e(xe,{value:e7})})}),s("p",{children:["Use ",e("b",{children:"openai"})," as you normally and traces will be sent to Phoenix"]}),e(w,{paddingBottom:"size-50",children:e(ve,{children:e(xe,{value:n7})})})]})})]})})]})}const t7="https://arize.com/docs/phoenix/tracing/how-to-tracing/setup-tracing",l7=n=>`import { Resource } from '@opentelemetry/resources';
import { SEMRESATTRS_PROJECT_NAME } from '@arizeai/openinference-semantic-conventions';

resource: new Resource({
    [SEMRESATTRS_PROJECT_NAME]: "${n}",
});`,i7=["# HTTP endpoint. Can use gRPC if available. See documentation",`OTEL_EXPORTER_OTLP_TRACES_ENDPOINT="${Tn}/v1/traces"`].join(`
`);function Kp(n){const a=po,l=n.projectName||"your-next-llm-project";return s("div",{children:[e(w,{paddingTop:"size-200",paddingBottom:"size-100",children:e(ne,{level:2,weight:"heavy",children:"Setup OpenTelemetry"})}),e(w,{paddingBottom:"size-100",children:s(C,{children:["Configure"," ",e(de,{href:t7,children:"OpenTelemetry"})," ","to send traces to Phoenix."]})}),e(w,{paddingTop:"size-200",paddingBottom:"size-100",children:e(j6,{})}),e(w,{paddingTop:"size-200",paddingBottom:"size-100",children:e(ne,{level:2,weight:"heavy",children:"Setup your Environment"})}),e(w,{paddingBottom:"size-100",children:s(C,{children:["Set the authentication headers in the environment variable"," ",e("b",{children:"OTEL_EXPORTER_OTLP_HEADERS"}),". See"," ",e(de,{href:"https://opentelemetry.io/docs/languages/sdk-configuration/otlp-exporter/#otel_exporter_otlp_traces_headers",children:"environment variables"})]})}),e(ve,{children:e(xe,{value:[a?"OTEL_EXPORTER_OTLP_HEADERS='<auth-headers>'":"OTEL_EXPORTER_OTLP_HEADERS='Authorization=Bearer <your-api-key>'",i7].join(`
`)})}),e(I3,{children:e(w,{paddingBottom:"size-100",paddingTop:"size-100",children:e(pr,{fallback:s(C,{children:["Your personal API keys can be created and managed on your"," ",e(de,{href:"/profile",children:"Profile"})]}),children:s(C,{children:["System API keys can be created and managed in"," ",e(de,{href:"/settings/general",children:"Settings"})]})})})}),e(w,{paddingTop:"size-200",paddingBottom:"size-100",children:e(ne,{level:2,weight:"heavy",children:"Set the Project Name"})}),e(w,{paddingBottom:"size-100",children:s(C,{children:["Set the project name for your app in the ",e("b",{children:"Resource Attributes"}),"."]})}),e(w,{paddingBottom:"size-100",children:e(ve,{children:e(xe,{value:"npm install @arizeai/openinference-semantic-conventions --save"})})}),e(w,{paddingBottom:"size-100",children:e(ve,{children:e(C6,{value:l7(l)})})}),e(w,{paddingBottom:"size-100",children:s(C,{children:["Add the resources to the NodeJS SDK or Vercel OTEL registration. See"," ",e(de,{href:"https://opentelemetry.io/docs/languages/js/resources/",children:"resources"})," ","for details."]})}),e(w,{paddingTop:"size-200",paddingBottom:"size-100",children:e(ne,{level:2,weight:"heavy",children:"Setup Instrumentation"})}),e(w,{paddingBottom:"size-100",children:e(C,{children:"Add instrumentation to your application so that your application code is traces."})}),e(w,{paddingBottom:"size-100",children:e(U6,{})})]})}function Pp(n){return e("button",{className:"button--reset",onClick:a=>{a.stopPropagation(),n.onClick(a)},"aria-label":n["aria-label"],css:m`
        color: var(--ac-global-text-color-white-900);
        .ac-icon-wrap {
          font-size: 1.2rem;
        }

        &:hover {
          color: var(--ac-global-color-primary);
        }
      `,children:e(T,{svg:n.isExpanded?e(Ic,{}):e(Tc,{})})})}function r7({gradientStartColor:n,gradientEndColor:a,size:t=32}){return e("div",{css:m`
        border-radius: 50%;
        width: ${t}px;
        height: ${t}px;
        background: linear-gradient(
          136.27deg,
          ${n} 14.03%,
          ${a} 84.38%
        );
        flex-shrink: 0;
      `})}const o7=m`
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--ac-global-dimension-size-50);
  padding: var(--ac-global-dimension-size-100);
  border: 2px solid transparent;
  border-radius: var(--ac-global-rounding-medium);
  cursor: pointer;
  transition: all 200ms ease;
  position: relative;
  background: transparent;

  /* Hover state */
  &[data-hovered]:not([data-disabled]):not([data-selected]) {
    border-color: var(--ac-global-color-grey-200);
  }

  /* Selected state */
  &[data-selected] {
    background-color: var(--ac-global-color-primary-50);
    border-color: var(--ac-global-color-primary);
  }

  /* Pressed state */
  &[data-pressed] {
    transform: scale(0.98);
  }

  /* Focus visible state */
  &[data-focus-visible] {
    outline: 2px solid var(--ac-global-color-primary);
    outline-offset: 2px;
  }

  /* Disabled state */
  &[data-disabled] {
    opacity: 0.5;
    cursor: not-allowed;
  }

  /* Label text styling */
  .gradient-circle-radio__label {
    font-size: var(--ac-global-dimension-static-font-size-75);
    color: var(--ac-global-text-color-700);
    text-align: center;
    font-weight: 500;
  }

  &[data-selected] .gradient-circle-radio__label {
    color: var(--ac-global-color-primary);
    font-weight: 600;
  }
`;function Vp({gradientStartColor:n,gradientEndColor:a,label:t,size:l=32,className:i,css:r,...o}){return s(Gl,{className:V("gradient-circle-radio",i),css:m(o7,r),...o,children:[e(r7,{gradientStartColor:n,gradientEndColor:a,size:l}),t&&e("span",{className:"gradient-circle-radio__label",children:t})]})}const s7=m`
  position: relative;
  display: flex;
  flex-direction: row;
  align-items: center;
  width: fit-content;
  gap: var(--ac-global-dimension-size-100);
  font-size: var(--ac-global-dimension-static-font-size-100);

  &[data-direction="row"] {
    flex-direction: row;
    flex-wrap: wrap;

    .react-aria-Label {
      flex-basis: 100%;
      margin-bottom: var(--ac-global-dimension-size-100);
    }

    [slot="description"] {
      flex-basis: 100%;
      margin-top: var(--ac-global-dimension-size-50);
    }
  }

  &[data-direction="column"] {
    flex-direction: column;
    align-items: flex-start;
  }

  &[data-disabled] {
    opacity: 0.5;
  }

  &[data-readonly] {
    .gradient-circle-radio {
      opacity: 0.7;
      cursor: default;
    }
  }

  &:has(.gradient-circle-radio[data-focus-visible]) {
    border-radius: var(--ac-global-rounding-small);
    outline: 1px solid var(--ac-global-color-primary);
    outline-offset: var(--ac-global-dimension-size-50);
  }
`;function Rp({css:n,className:a,direction:t="row",...l}){return e(Ul,{"data-direction":t,className:V("gradient-circle-radio-group",a),css:m(Le,s7,n),...l})}function Op({sequenceNumber:n}){return s(je,{color:"var(--ac-global-color-yellow-500)",size:"S",children:["#",n]})}function Np(){const n=a5();return{getExperimentColor:p.useCallback(t=>{const l=Object.values(n),i=l.length;return l[t%i]},[n]),baseExperimentColor:"var(--ac-global-color-grey-500)"}}const yo=(function(){var n=[{defaultValue:null,kind:"LocalArgument",name:"nodeId"}],a=[{kind:"Variable",name:"id",variableName:"nodeId"}],t={alias:null,args:null,kind:"ScalarField",name:"__typename",storageKey:null},l=[{alias:null,args:null,kind:"ScalarField",name:"tokens",storageKey:null}],i={kind:"InlineFragment",selections:[{alias:null,args:null,concreteType:"SpanCostSummary",kind:"LinkedField",name:"costSummary",plural:!1,selections:[{alias:null,args:null,concreteType:"CostBreakdown",kind:"LinkedField",name:"total",plural:!1,selections:l,storageKey:null},{alias:null,args:null,concreteType:"CostBreakdown",kind:"LinkedField",name:"prompt",plural:!1,selections:l,storageKey:null},{alias:null,args:null,concreteType:"CostBreakdown",kind:"LinkedField",name:"completion",plural:!1,selections:l,storageKey:null}],storageKey:null}],type:"ExperimentRun",abstractKey:null};return{fragment:{argumentDefinitions:n,kind:"Fragment",metadata:null,name:"ExperimentRunTokenCountDetailsQuery",selections:[{alias:null,args:a,concreteType:null,kind:"LinkedField",name:"node",plural:!1,selections:[t,i],storageKey:null}],type:"Query",abstractKey:null},kind:"Request",operation:{argumentDefinitions:n,kind:"Operation",name:"ExperimentRunTokenCountDetailsQuery",selections:[{alias:null,args:a,concreteType:null,kind:"LinkedField",name:"node",plural:!1,selections:[t,i,{alias:null,args:null,kind:"ScalarField",name:"id",storageKey:null}],storageKey:null}]},params:{cacheID:"bb25f38a892f4b257794b8e43b04f835",id:null,metadata:{},name:"ExperimentRunTokenCountDetailsQuery",operationKind:"query",text:`query ExperimentRunTokenCountDetailsQuery(
  $nodeId: ID!
) {
  node(id: $nodeId) {
    __typename
    ... on ExperimentRun {
      costSummary {
        total {
          tokens
        }
        prompt {
          tokens
        }
        completion {
          tokens
        }
      }
    }
    id
  }
}
`}}})();yo.hash="0de1caa674a484b1e5d1449743805823";function c7(n){const a=M.useLazyLoadQuery(yo,{nodeId:n.experimentRunId}),t=p.useMemo(()=>{var l,i,r,o,c,d;if(a.node.__typename==="ExperimentRun"){const u=((i=(l=a.node.costSummary)==null?void 0:l.prompt)==null?void 0:i.tokens)??0,g=((o=(r=a.node.costSummary)==null?void 0:r.completion)==null?void 0:o.tokens)??0;return{total:((d=(c=a.node.costSummary)==null?void 0:c.total)==null?void 0:d.tokens)??0,prompt:u,completion:g}}return{total:null,prompt:null,completion:null}},[a.node]);return e(Xe,{...t})}function $p(n){return s(R,{isDisabled:n.tokenCountTotal==null,children:[e(te,{children:e(ze,{size:n.size,role:"button",children:n.tokenCountTotal})}),s(ie,{children:[e(ae,{}),e(p.Suspense,{fallback:e(re,{}),children:e(c7,{experimentRunId:n.experimentRunId})})]})]})}const vo=(function(){var n=[{defaultValue:null,kind:"LocalArgument",name:"nodeId"}],a=[{kind:"Variable",name:"id",variableName:"nodeId"}],t={alias:null,args:null,kind:"ScalarField",name:"__typename",storageKey:null},l=[{alias:null,args:null,kind:"ScalarField",name:"cost",storageKey:null}],i={kind:"InlineFragment",selections:[{alias:null,args:null,concreteType:"SpanCostSummary",kind:"LinkedField",name:"costSummary",plural:!1,selections:[{alias:null,args:null,concreteType:"CostBreakdown",kind:"LinkedField",name:"total",plural:!1,selections:l,storageKey:null},{alias:null,args:null,concreteType:"CostBreakdown",kind:"LinkedField",name:"prompt",plural:!1,selections:l,storageKey:null},{alias:null,args:null,concreteType:"CostBreakdown",kind:"LinkedField",name:"completion",plural:!1,selections:l,storageKey:null}],storageKey:null}],type:"ExperimentRun",abstractKey:null};return{fragment:{argumentDefinitions:n,kind:"Fragment",metadata:null,name:"ExperimentRunTokenCostsDetailsQuery",selections:[{alias:null,args:a,concreteType:null,kind:"LinkedField",name:"node",plural:!1,selections:[t,i],storageKey:null}],type:"Query",abstractKey:null},kind:"Request",operation:{argumentDefinitions:n,kind:"Operation",name:"ExperimentRunTokenCostsDetailsQuery",selections:[{alias:null,args:a,concreteType:null,kind:"LinkedField",name:"node",plural:!1,selections:[t,i,{alias:null,args:null,kind:"ScalarField",name:"id",storageKey:null}],storageKey:null}]},params:{cacheID:"56ebff6ade8d9718931af681ea77b06a",id:null,metadata:{},name:"ExperimentRunTokenCostsDetailsQuery",operationKind:"query",text:`query ExperimentRunTokenCostsDetailsQuery(
  $nodeId: ID!
) {
  node(id: $nodeId) {
    __typename
    ... on ExperimentRun {
      costSummary {
        total {
          cost
        }
        prompt {
          cost
        }
        completion {
          cost
        }
      }
    }
    id
  }
}
`}}})();vo.hash="f99884bcc09d854081aeba2247d70dde";function d7(n){const a=M.useLazyLoadQuery(vo,{nodeId:n.experimentRunId}),t=p.useMemo(()=>{var l,i,r,o,c,d;if(a.node.__typename==="ExperimentRun"){const u=((i=(l=a.node.costSummary)==null?void 0:l.prompt)==null?void 0:i.cost)??0,g=((o=(r=a.node.costSummary)==null?void 0:r.completion)==null?void 0:o.cost)??0;return{total:((d=(c=a.node.costSummary)==null?void 0:c.total)==null?void 0:d.cost)??0,prompt:u,completion:g}}return{total:null,prompt:null,completion:null}},[a.node]);return e(dn,{...t})}function Bp(n){return s(R,{isDisabled:n.costTotal==null,children:[e(te,{children:e(cn,{size:n.size,"aria-role":"button",children:n.costTotal})}),s(ie,{children:[e(ae,{}),e(p.Suspense,{fallback:e(re,{}),children:e(d7,{experimentRunId:n.experimentRunId})})]})]})}const Co=(function(){var n=[{defaultValue:null,kind:"LocalArgument",name:"nodeId"}],a=[{kind:"Variable",name:"id",variableName:"nodeId"}],t={alias:null,args:null,kind:"ScalarField",name:"__typename",storageKey:null},l=[{alias:null,args:null,kind:"ScalarField",name:"tokens",storageKey:null}],i={kind:"InlineFragment",selections:[{alias:null,args:null,concreteType:"SpanCostSummary",kind:"LinkedField",name:"costSummary",plural:!1,selections:[{alias:null,args:null,concreteType:"CostBreakdown",kind:"LinkedField",name:"total",plural:!1,selections:l,storageKey:null},{alias:null,args:null,concreteType:"CostBreakdown",kind:"LinkedField",name:"prompt",plural:!1,selections:l,storageKey:null},{alias:null,args:null,concreteType:"CostBreakdown",kind:"LinkedField",name:"completion",plural:!1,selections:l,storageKey:null}],storageKey:null}],type:"Experiment",abstractKey:null};return{fragment:{argumentDefinitions:n,kind:"Fragment",metadata:null,name:"ExperimentTokenCountDetailsQuery",selections:[{alias:null,args:a,concreteType:null,kind:"LinkedField",name:"node",plural:!1,selections:[t,i],storageKey:null}],type:"Query",abstractKey:null},kind:"Request",operation:{argumentDefinitions:n,kind:"Operation",name:"ExperimentTokenCountDetailsQuery",selections:[{alias:null,args:a,concreteType:null,kind:"LinkedField",name:"node",plural:!1,selections:[t,i,{alias:null,args:null,kind:"ScalarField",name:"id",storageKey:null}],storageKey:null}]},params:{cacheID:"3b40ee1d5d53511d1e5a6ff31b52cd01",id:null,metadata:{},name:"ExperimentTokenCountDetailsQuery",operationKind:"query",text:`query ExperimentTokenCountDetailsQuery(
  $nodeId: ID!
) {
  node(id: $nodeId) {
    __typename
    ... on Experiment {
      costSummary {
        total {
          tokens
        }
        prompt {
          tokens
        }
        completion {
          tokens
        }
      }
    }
    id
  }
}
`}}})();Co.hash="0946f26e471401c182db5b8107b9c3dd";function u7(n){const a=M.useLazyLoadQuery(Co,{nodeId:n.experimentId}),t=p.useMemo(()=>{var l,i,r,o,c,d;if(a.node.__typename==="Experiment"){const u=((i=(l=a.node.costSummary)==null?void 0:l.prompt)==null?void 0:i.tokens)??0,g=((o=(r=a.node.costSummary)==null?void 0:r.completion)==null?void 0:o.tokens)??0;return{total:((d=(c=a.node.costSummary)==null?void 0:c.total)==null?void 0:d.tokens)??0,prompt:u,completion:g}}return{total:null,prompt:null,completion:null}},[a.node]);return e(Xe,{...t})}function Hp(n){return n.tokenCountTotal==null?e(ze,{size:n.size,children:null}):s(R,{children:[e(te,{children:e(ze,{size:n.size,role:"button",children:n.tokenCountTotal})}),s(ie,{children:[e(ae,{}),e(p.Suspense,{fallback:e(re,{}),children:e(u7,{experimentId:n.experimentId})})]})]})}const ko=(function(){var n=[{defaultValue:null,kind:"LocalArgument",name:"experimentId"}],a=[{kind:"Variable",name:"id",variableName:"experimentId"}],t={alias:null,args:null,kind:"ScalarField",name:"__typename",storageKey:null},l={alias:null,args:null,kind:"ScalarField",name:"cost",storageKey:null},i=[l],r={kind:"InlineFragment",selections:[{alias:null,args:null,concreteType:"SpanCostSummary",kind:"LinkedField",name:"costSummary",plural:!1,selections:[{alias:null,args:null,concreteType:"CostBreakdown",kind:"LinkedField",name:"total",plural:!1,selections:i,storageKey:null},{alias:null,args:null,concreteType:"CostBreakdown",kind:"LinkedField",name:"prompt",plural:!1,selections:i,storageKey:null},{alias:null,args:null,concreteType:"CostBreakdown",kind:"LinkedField",name:"completion",plural:!1,selections:i,storageKey:null}],storageKey:null},{alias:null,args:null,concreteType:"SpanCostDetailSummaryEntry",kind:"LinkedField",name:"costDetailSummaryEntries",plural:!0,selections:[{alias:null,args:null,kind:"ScalarField",name:"tokenType",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"isPrompt",storageKey:null},{alias:null,args:null,concreteType:"CostBreakdown",kind:"LinkedField",name:"value",plural:!1,selections:[l,{alias:null,args:null,kind:"ScalarField",name:"tokens",storageKey:null}],storageKey:null}],storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"runCount",storageKey:null}],type:"Experiment",abstractKey:null};return{fragment:{argumentDefinitions:n,kind:"Fragment",metadata:null,name:"ExperimentAverageRunTokenCostsDetailsQuery",selections:[{alias:"experiment",args:a,concreteType:null,kind:"LinkedField",name:"node",plural:!1,selections:[t,r],storageKey:null}],type:"Query",abstractKey:null},kind:"Request",operation:{argumentDefinitions:n,kind:"Operation",name:"ExperimentAverageRunTokenCostsDetailsQuery",selections:[{alias:"experiment",args:a,concreteType:null,kind:"LinkedField",name:"node",plural:!1,selections:[t,r,{alias:null,args:null,kind:"ScalarField",name:"id",storageKey:null}],storageKey:null}]},params:{cacheID:"84d979fc0c4a2f43c63f82ffdb4d77be",id:null,metadata:{},name:"ExperimentAverageRunTokenCostsDetailsQuery",operationKind:"query",text:`query ExperimentAverageRunTokenCostsDetailsQuery(
  $experimentId: ID!
) {
  experiment: node(id: $experimentId) {
    __typename
    ... on Experiment {
      costSummary {
        total {
          cost
        }
        prompt {
          cost
        }
        completion {
          cost
        }
      }
      costDetailSummaryEntries {
        tokenType
        isPrompt
        value {
          cost
          tokens
        }
      }
      runCount
    }
    id
  }
}
`}}})();ko.hash="77037c928e3745c36b74597c172eb5ee";function g7({experimentId:n}){const a=M.useLazyLoadQuery(ko,{experimentId:n}),t=p.useMemo(()=>{if(a.experiment.__typename==="Experiment"){const l=a.experiment.costDetailSummaryEntries;if(!l)return{total:null,prompt:null,completion:null,promptDetails:null,completionDetails:null};const i=l.filter(v=>v.isPrompt),r=l.filter(v=>!v.isPrompt),o=a.experiment.costSummary.total.cost,c=a.experiment.costSummary.prompt.cost,d=a.experiment.costSummary.completion.cost,u=a.experiment.runCount,g=o==null||u==0?null:o/u,h=c==null||u==0?null:c/u,f=d==null||u==0?null:d/u,b={};i.forEach(v=>{v.value.cost!=null&&(b[v.tokenType]=v.value.cost)});const y={};return r.forEach(v=>{v.value.cost!=null&&(y[v.tokenType]=v.value.cost)}),{total:g,prompt:h,completion:f,promptDetails:Object.keys(b).length>0?b:null,completionDetails:Object.keys(y).length>0?y:null}}return{total:null,prompt:null,completion:null,promptDetails:null,completionDetails:null}},[a.experiment]);return e(dn,{...t,label:"Average"})}function jp(n){return s(R,{children:[e(te,{children:e(cn,{size:n.size,role:"button",children:n.averageRunCostTotal})}),s(ie,{children:[e(ae,{}),e(p.Suspense,{fallback:e(re,{}),children:e(g7,{experimentId:n.experimentId})})]})]})}const Lo=(function(){var n=[{defaultValue:null,kind:"LocalArgument",name:"input"}],a=[{alias:null,args:[{kind:"Variable",name:"input",variableName:"input"}],concreteType:"ExperimentMutationPayload",kind:"LinkedField",name:"deleteExperiments",plural:!1,selections:[{alias:null,args:null,kind:"ScalarField",name:"__typename",storageKey:null}],storageKey:null}];return{fragment:{argumentDefinitions:n,kind:"Fragment",metadata:null,name:"ExperimentActionMenuDeleteExperimentMutation",selections:a,type:"Mutation",abstractKey:null},kind:"Request",operation:{argumentDefinitions:n,kind:"Operation",name:"ExperimentActionMenuDeleteExperimentMutation",selections:a},params:{cacheID:"7fcd7830853f4b8f55b104d75dc5312b",id:null,metadata:{},name:"ExperimentActionMenuDeleteExperimentMutation",operationKind:"mutation",text:`mutation ExperimentActionMenuDeleteExperimentMutation(
  $input: DeleteExperimentsInput!
) {
  deleteExperiments(input: $input) {
    __typename
  }
}
`}}})();Lo.hash="c7f4f68f0256356c77264cc16b83e638";function Zp(n){const[a,t]=M.useMutation(Lo),{projectId:l,isQuiet:i=!1}=n,r=ti(),[o,c]=p.useState(!1),[d,u]=p.useState(!1),g=zt(),h=Ni(),f=n.onExperimentDeleted,b=p.useCallback(v=>{a({variables:{input:{experimentIds:[v]}},onCompleted:()=>{g({title:"Experiment deleted",message:"The experiment has been deleted."})},onError:k=>{const L=$t(k);h({title:"An error occurred",message:`Failed to delete experiment: ${(L==null?void 0:L[0])??k.message}`})}}),f==null||f(),c(!1)},[a,g,h,f]),y=[e(Jn,{children:s(S,{direction:"row",gap:"size-75",justifyContent:"start",alignItems:"center",children:[e(T,{svg:e(n0,{})}),e(C,{children:"View run traces"})]})},"GO_TO_EXPERIMENT_RUN_TRACES"),e(Jn,{children:s(S,{direction:"row",gap:"size-75",justifyContent:"start",alignItems:"center",children:[e(T,{svg:e(St,{})}),e(C,{children:"View metadata"})]})},"VIEW_METADATA"),e(Jn,{children:s(S,{direction:"row",gap:"size-75",justifyContent:"start",alignItems:"center",children:[e(T,{svg:e(Si,{})}),e(C,{children:"Copy experiment ID"})]})},"COPY_EXPERIMENT_ID")];return n.canDeleteExperiment&&y.push(e(Jn,{children:s(S,{direction:"row",gap:"size-75",justifyContent:"start",alignItems:"center",children:[e(T,{svg:e(Tt,{})}),e(C,{children:t?"Deleting...":"Delete"})]})},"DELETE_EXPERIMENT")),s(U,{children:[e("div",{onClick:v=>{v.preventDefault(),v.stopPropagation()},children:e(hs,{buttonSize:"compact",align:"end",isQuiet:i,disabledKeys:l?[]:["GO_TO_EXPERIMENT_RUN_TRACES"],onAction:v=>{switch(v){case"GO_TO_EXPERIMENT_RUN_TRACES":return r(`/projects/${l}`);case"VIEW_METADATA":{u(!0);break}case"COPY_EXPERIMENT_ID":{Pl(n.experimentId),g({title:"Copied",message:"The experiment ID has been copied to your clipboard"});break}case"DELETE_EXPERIMENT":{c(!0);break}default:P()}},children:y})}),e(Cn,{isDismissable:!0,isOpen:o,onOpenChange:c,children:e(vn,{size:"S",children:e(be,{children:s(Ke,{children:[s(Pe,{children:[e(Ve,{children:"Delete Experiment"}),e(ln,{children:e(Qe,{slot:"close"})})]}),e(w,{padding:"size-200",children:e(C,{color:"danger",children:"Are you sure you want to delete this experiment and its annotations and traces?"})}),e(w,{paddingEnd:"size-200",paddingTop:"size-100",paddingBottom:"size-100",borderTopColor:"light",borderTopWidth:"thin",children:s(S,{direction:"row",justifyContent:"end",gap:"size-100",children:[e(z,{size:"S",onPress:()=>c(!1),children:"Cancel"}),e(z,{variant:"danger",size:"S",onPress:()=>b(n.experimentId),children:"Delete Experiment"})]})})]})})})}),e(Cn,{isDismissable:!0,isOpen:d,onOpenChange:u,children:e(vn,{size:"S",children:e(be,{children:s(Ke,{children:[s(Pe,{children:[e(Ve,{children:"Metadata"}),e(ln,{children:e(Qe,{slot:"close"})})]}),e(gr,{value:JSON.stringify(n.metadata,null,2)})]})})})})]})}const wo=(function(){var n=[{defaultValue:null,kind:"LocalArgument",name:"experimentId"}],a=[{kind:"Variable",name:"id",variableName:"experimentId"}],t={alias:null,args:null,kind:"ScalarField",name:"__typename",storageKey:null},l={alias:null,args:null,kind:"ScalarField",name:"cost",storageKey:null},i=[l],r={kind:"InlineFragment",selections:[{alias:null,args:null,concreteType:"SpanCostSummary",kind:"LinkedField",name:"costSummary",plural:!1,selections:[{alias:null,args:null,concreteType:"CostBreakdown",kind:"LinkedField",name:"total",plural:!1,selections:i,storageKey:null},{alias:null,args:null,concreteType:"CostBreakdown",kind:"LinkedField",name:"prompt",plural:!1,selections:i,storageKey:null},{alias:null,args:null,concreteType:"CostBreakdown",kind:"LinkedField",name:"completion",plural:!1,selections:i,storageKey:null}],storageKey:null},{alias:null,args:null,concreteType:"SpanCostDetailSummaryEntry",kind:"LinkedField",name:"costDetailSummaryEntries",plural:!0,selections:[{alias:null,args:null,kind:"ScalarField",name:"tokenType",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"isPrompt",storageKey:null},{alias:null,args:null,concreteType:"CostBreakdown",kind:"LinkedField",name:"value",plural:!1,selections:[l,{alias:null,args:null,kind:"ScalarField",name:"tokens",storageKey:null}],storageKey:null}],storageKey:null}],type:"Experiment",abstractKey:null};return{fragment:{argumentDefinitions:n,kind:"Fragment",metadata:null,name:"ExperimentTokenCostsDetailsQuery",selections:[{alias:"experiment",args:a,concreteType:null,kind:"LinkedField",name:"node",plural:!1,selections:[t,r],storageKey:null}],type:"Query",abstractKey:null},kind:"Request",operation:{argumentDefinitions:n,kind:"Operation",name:"ExperimentTokenCostsDetailsQuery",selections:[{alias:"experiment",args:a,concreteType:null,kind:"LinkedField",name:"node",plural:!1,selections:[t,r,{alias:null,args:null,kind:"ScalarField",name:"id",storageKey:null}],storageKey:null}]},params:{cacheID:"3b4a585ebf1e46fed5f48bb8d74eec68",id:null,metadata:{},name:"ExperimentTokenCostsDetailsQuery",operationKind:"query",text:`query ExperimentTokenCostsDetailsQuery(
  $experimentId: ID!
) {
  experiment: node(id: $experimentId) {
    __typename
    ... on Experiment {
      costSummary {
        total {
          cost
        }
        prompt {
          cost
        }
        completion {
          cost
        }
      }
      costDetailSummaryEntries {
        tokenType
        isPrompt
        value {
          cost
          tokens
        }
      }
    }
    id
  }
}
`}}})();wo.hash="2101043bf625b3499039a269191c9269";function m7({experimentId:n}){const a=M.useLazyLoadQuery(wo,{experimentId:n}),t=p.useMemo(()=>{var l,i,r,o,c,d;if(a.experiment.__typename==="Experiment"){const u=a.experiment.costDetailSummaryEntries;if(!u)return{total:null,prompt:null,completion:null,promptDetails:null,completionDetails:null};const g=u.filter(L=>L.isPrompt),h=u.filter(L=>!L.isPrompt),f=((i=(l=a.experiment.costSummary)==null?void 0:l.total)==null?void 0:i.cost)??0,b=((o=(r=a.experiment.costSummary)==null?void 0:r.prompt)==null?void 0:o.cost)??0,y=((d=(c=a.experiment.costSummary)==null?void 0:c.completion)==null?void 0:d.cost)??0,v={};g.forEach(L=>{L.value.cost!=null&&(v[L.tokenType]=L.value.cost)});const k={};return h.forEach(L=>{L.value.cost!=null&&(k[L.tokenType]=L.value.cost)}),{total:f,prompt:b,completion:y,promptDetails:Object.keys(v).length>0?v:null,completionDetails:Object.keys(k).length>0?k:null}}return{total:null,prompt:null,completion:null,promptDetails:null,completionDetails:null}},[a.experiment]);return e(dn,{...t})}function Up(n){return s(R,{children:[e(te,{children:e(cn,{size:n.size,role:"button",children:n.totalCost})}),s(ie,{children:[e(ae,{}),e(p.Suspense,{fallback:e(re,{}),children:e(m7,{experimentId:n.experimentId})})]})]})}function p7(n){return typeof n=="string"&&["grid","list","metrics"].includes(n)}function Gp({viewMode:n,onViewModeChange:a}){return s(Gn,{selectedKeys:[n],selectionMode:"single",onSelectionChange:t=>{if(t.size===0)return;const l=t.keys().next().value;p7(l)?a(l):a("grid")},size:"S",children:[e(Ce,{id:"grid",leadingVisual:e(T,{svg:e(xi,{})}),children:"Grid"}),e(Ce,{id:"list",leadingVisual:e(T,{svg:e(Ti,{})}),children:"List"}),e(Ce,{id:"metrics",leadingVisual:e(T,{svg:e(kc,{})}),children:"Metrics"})]})}const So=(function(){var n=[{defaultValue:null,kind:"LocalArgument",name:"experimentId"}],a=[{kind:"Variable",name:"id",variableName:"experimentId"}],t={alias:null,args:null,kind:"ScalarField",name:"__typename",storageKey:null},l=[{alias:null,args:null,kind:"ScalarField",name:"tokens",storageKey:null}],i={kind:"InlineFragment",selections:[{alias:null,args:null,kind:"ScalarField",name:"runCount",storageKey:null},{alias:null,args:null,concreteType:"SpanCostSummary",kind:"LinkedField",name:"costSummary",plural:!1,selections:[{alias:null,args:null,concreteType:"CostBreakdown",kind:"LinkedField",name:"total",plural:!1,selections:l,storageKey:null},{alias:null,args:null,concreteType:"CostBreakdown",kind:"LinkedField",name:"prompt",plural:!1,selections:l,storageKey:null},{alias:null,args:null,concreteType:"CostBreakdown",kind:"LinkedField",name:"completion",plural:!1,selections:l,storageKey:null}],storageKey:null}],type:"Experiment",abstractKey:null};return{fragment:{argumentDefinitions:n,kind:"Fragment",metadata:null,name:"ExperimentAverageRunTokenCountDetailsQuery",selections:[{alias:"experiment",args:a,concreteType:null,kind:"LinkedField",name:"node",plural:!1,selections:[t,i],storageKey:null}],type:"Query",abstractKey:null},kind:"Request",operation:{argumentDefinitions:n,kind:"Operation",name:"ExperimentAverageRunTokenCountDetailsQuery",selections:[{alias:"experiment",args:a,concreteType:null,kind:"LinkedField",name:"node",plural:!1,selections:[t,i,{alias:null,args:null,kind:"ScalarField",name:"id",storageKey:null}],storageKey:null}]},params:{cacheID:"0e70281a4361949908af5866b8aa6c4e",id:null,metadata:{},name:"ExperimentAverageRunTokenCountDetailsQuery",operationKind:"query",text:`query ExperimentAverageRunTokenCountDetailsQuery(
  $experimentId: ID!
) {
  experiment: node(id: $experimentId) {
    __typename
    ... on Experiment {
      runCount
      costSummary {
        total {
          tokens
        }
        prompt {
          tokens
        }
        completion {
          tokens
        }
      }
    }
    id
  }
}
`}}})();So.hash="7772e95d9d4cf1f8435cb8fcf8e77081";function h7({experimentId:n}){const a=M.useLazyLoadQuery(So,{experimentId:n}),t=p.useMemo(()=>{if(a.experiment.__typename==="Experiment"){const l=a.experiment.costSummary.prompt.tokens,i=a.experiment.costSummary.completion.tokens,r=a.experiment.costSummary.total.tokens,o=a.experiment.runCount,c=r==null||o==0?null:r/o,d=l==null||o==0?null:l/o,u=i==null||o==0?null:i/o;return{total:c,prompt:d,completion:u}}return{total:null,prompt:null,completion:null}},[a.experiment]);return e(Xe,{...t,label:"Average"})}function Qp(n){return n.averageRunTokenCountTotal==null?e(ze,{size:n.size,children:null}):s(R,{children:[e(te,{children:e(ze,{size:n.size,role:"button",children:n.averageRunTokenCountTotal})}),s(ie,{children:[e(ae,{}),e(p.Suspense,{fallback:e(re,{}),children:e(h7,{experimentId:n.experimentId})})]})]})}const f7=n=>m`
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: ${n};
  overflow: hidden;
`;function Wp({children:n,lines:a}){return e("div",{css:f7(a),children:n})}const xo=(function(){var n=[{defaultValue:null,kind:"LocalArgument",name:"nodeId"}],a=[{kind:"Variable",name:"id",variableName:"nodeId"}],t={alias:null,args:null,kind:"ScalarField",name:"__typename",storageKey:null},l=[{alias:null,args:null,kind:"ScalarField",name:"cost",storageKey:null}],i={kind:"InlineFragment",selections:[{alias:null,args:null,concreteType:"SpanCostSummary",kind:"LinkedField",name:"costSummary",plural:!1,selections:[{alias:null,args:null,concreteType:"CostBreakdown",kind:"LinkedField",name:"total",plural:!1,selections:l,storageKey:null},{alias:null,args:null,concreteType:"CostBreakdown",kind:"LinkedField",name:"prompt",plural:!1,selections:l,storageKey:null},{alias:null,args:null,concreteType:"CostBreakdown",kind:"LinkedField",name:"completion",plural:!1,selections:l,storageKey:null}],storageKey:null}],type:"ExperimentRepeatedRunGroup",abstractKey:null};return{fragment:{argumentDefinitions:n,kind:"Fragment",metadata:null,name:"ExperimentRepeatedRunGroupTokenCostDetailsQuery",selections:[{alias:null,args:a,concreteType:null,kind:"LinkedField",name:"node",plural:!1,selections:[t,i],storageKey:null}],type:"Query",abstractKey:null},kind:"Request",operation:{argumentDefinitions:n,kind:"Operation",name:"ExperimentRepeatedRunGroupTokenCostDetailsQuery",selections:[{alias:null,args:a,concreteType:null,kind:"LinkedField",name:"node",plural:!1,selections:[t,i,{alias:null,args:null,kind:"ScalarField",name:"id",storageKey:null}],storageKey:null}]},params:{cacheID:"43099aa66474f4d3fa7cd9dc3f04ccf2",id:null,metadata:{},name:"ExperimentRepeatedRunGroupTokenCostDetailsQuery",operationKind:"query",text:`query ExperimentRepeatedRunGroupTokenCostDetailsQuery(
  $nodeId: ID!
) {
  node(id: $nodeId) {
    __typename
    ... on ExperimentRepeatedRunGroup {
      costSummary {
        total {
          cost
        }
        prompt {
          cost
        }
        completion {
          cost
        }
      }
    }
    id
  }
}
`}}})();xo.hash="125a71d4c6f856ce5da6d344cac839e8";function b7(n){const a=M.useLazyLoadQuery(xo,{nodeId:n.experimentRepeatedRunGroupId}),t=p.useMemo(()=>{if(a.node.__typename==="ExperimentRepeatedRunGroup"){const l=a.node.costSummary.prompt.cost,i=a.node.costSummary.completion.cost;return{total:a.node.costSummary.total.cost,prompt:l,completion:i}}return{total:null,prompt:null,completion:null}},[a.node]);return e(dn,{...t})}function qp(n){return s(R,{isDisabled:n.costTotal==null,children:[e(te,{children:e(cn,{size:n.size,"aria-role":"button",children:n.costTotal})}),s(ie,{children:[e(ae,{}),e(p.Suspense,{fallback:e(re,{}),children:e(b7,{experimentRepeatedRunGroupId:n.experimentRepeatedRunGroupId})})]})]})}const To=(function(){var n=[{defaultValue:null,kind:"LocalArgument",name:"nodeId"}],a=[{kind:"Variable",name:"id",variableName:"nodeId"}],t={alias:null,args:null,kind:"ScalarField",name:"__typename",storageKey:null},l=[{alias:null,args:null,kind:"ScalarField",name:"tokens",storageKey:null}],i={kind:"InlineFragment",selections:[{alias:null,args:null,concreteType:"SpanCostSummary",kind:"LinkedField",name:"costSummary",plural:!1,selections:[{alias:null,args:null,concreteType:"CostBreakdown",kind:"LinkedField",name:"total",plural:!1,selections:l,storageKey:null},{alias:null,args:null,concreteType:"CostBreakdown",kind:"LinkedField",name:"prompt",plural:!1,selections:l,storageKey:null},{alias:null,args:null,concreteType:"CostBreakdown",kind:"LinkedField",name:"completion",plural:!1,selections:l,storageKey:null}],storageKey:null}],type:"ExperimentRepeatedRunGroup",abstractKey:null};return{fragment:{argumentDefinitions:n,kind:"Fragment",metadata:null,name:"ExperimentRepeatedRunGroupTokenCountDetailsQuery",selections:[{alias:null,args:a,concreteType:null,kind:"LinkedField",name:"node",plural:!1,selections:[t,i],storageKey:null}],type:"Query",abstractKey:null},kind:"Request",operation:{argumentDefinitions:n,kind:"Operation",name:"ExperimentRepeatedRunGroupTokenCountDetailsQuery",selections:[{alias:null,args:a,concreteType:null,kind:"LinkedField",name:"node",plural:!1,selections:[t,i,{alias:null,args:null,kind:"ScalarField",name:"id",storageKey:null}],storageKey:null}]},params:{cacheID:"17535680d5a7af6fa77466bf5134c3e0",id:null,metadata:{},name:"ExperimentRepeatedRunGroupTokenCountDetailsQuery",operationKind:"query",text:`query ExperimentRepeatedRunGroupTokenCountDetailsQuery(
  $nodeId: ID!
) {
  node(id: $nodeId) {
    __typename
    ... on ExperimentRepeatedRunGroup {
      costSummary {
        total {
          tokens
        }
        prompt {
          tokens
        }
        completion {
          tokens
        }
      }
    }
    id
  }
}
`}}})();To.hash="fc023fee63f29794e61517820b6c9313";function y7(n){const a=M.useLazyLoadQuery(To,{nodeId:n.experimentRepeatedRunGroupId}),t=p.useMemo(()=>{if(a.node.__typename==="ExperimentRepeatedRunGroup"){const l=a.node.costSummary.prompt.tokens,i=a.node.costSummary.completion.tokens;return{total:a.node.costSummary.total.tokens,prompt:l,completion:i}}return{total:null,prompt:null,completion:null}},[a.node]);return e(Xe,{...t})}function Xp(n){return s(R,{isDisabled:n.tokenCountTotal==null,children:[e(te,{children:e(ze,{size:n.size,role:"button",children:n.tokenCountTotal})}),s(ie,{children:[e(ae,{}),e(p.Suspense,{fallback:e(re,{}),children:e(y7,{experimentRepeatedRunGroupId:n.experimentRepeatedRunGroupId})})]})]})}function Yp(){const[n,a]=p.useState(!1);return s(_e,{children:[e(z,{size:"S",variant:"primary",leadingVisual:e(T,{svg:e(Bc,{})}),onPress:()=>a(!0),children:"New Label"}),e(Cn,{isOpen:n,onOpenChange:a,children:e(vn,{size:"S",children:e(y5,{onCompleted:()=>a(!1)})})})]})}export{Mi as $,Ve as A,ln as B,rg as C,er as D,Qe as E,w as F,Cn as G,Kg as H,S as I,C as J,Ou as K,z as L,T as M,e8 as N,Ot as O,it as P,Pi as Q,I8 as R,A8 as S,Ze as T,Qn as U,Ni as V,zt as W,Q as X,_8 as Y,K8 as Z,vn as _,xa as a,ee as a$,Tt as a0,Bc as a1,$7 as a2,R7 as a3,f3 as a4,Wg as a5,ur as a6,da as a7,je as a8,_i as a9,t5 as aA,xn as aB,yr as aC,l5 as aD,br as aE,Tn as aF,q8 as aG,pr as aH,Ct as aI,S8 as aJ,w8 as aK,Mg as aL,Fg as aM,Mm as aN,zm as aO,tt as aP,ya as aQ,J7 as aR,Rg as aS,Oc as aT,v0 as aU,ie as aV,dr as aW,j3 as aX,Ne as aY,Ae as aZ,we as a_,ke as aa,ae as ab,$t as ac,ne as ad,re as ae,Ai as af,hr as ag,T2 as ah,fa as ai,nm as aj,am as ak,om as al,em as am,xt as an,Xg as ao,Jg as ap,zd as aq,dl as ar,R8 as as,Ad as at,c3 as au,cm as av,sm as aw,Am as ax,Im as ay,il as az,tr as b,zg as b$,ue as b0,Km as b1,$m as b2,Nm as b3,Ge as b4,X8 as b5,_m as b6,Vm as b7,Q7 as b8,i8 as b9,L8 as bA,lg as bB,k8 as bC,C8 as bD,gr as bE,hg as bF,pg as bG,E7 as bH,v8 as bI,Sg as bJ,xg as bK,Tg as bL,jm as bM,Hm as bN,kg as bO,qn as bP,Ta as bQ,Aa as bR,mu as bS,bu as bT,Yg as bU,w3 as bV,L3 as bW,n8 as bX,xd as bY,Pu as bZ,G2 as b_,X7 as ba,u8 as bb,s8 as bc,U7 as bd,Em as be,h8 as bf,Fm as bg,r8 as bh,Dm as bi,d8 as bj,Om as bk,Rm as bl,o8 as bm,Pm as bn,O8 as bo,Bm as bp,Q8 as bq,G8 as br,It as bs,y5 as bt,z8 as bu,x8 as bv,me as bw,Mc as bx,H8 as by,B8 as bz,Kt as c,N7 as c$,du as c0,p8 as c1,k3 as c2,Vg as c3,w5 as c4,Qg as c5,St as c6,n0 as c7,Um as c8,pc as c9,rp as cA,T8 as cB,tm as cC,up as cD,K3 as cE,gp as cF,q7 as cG,a8 as cH,pp as cI,hp as cJ,Ce as cK,gc as cL,D7 as cM,L5 as cN,le as cO,vc as cP,S7 as cQ,ap as cR,lp as cS,tp as cT,Ll as cU,l8 as cV,Z5 as cW,op as cX,ep as cY,u4 as cZ,np as c_,de as ca,Lt as cb,M7 as cc,E8 as cd,We as ce,g3 as cf,ip as cg,g4 as ch,en as ci,n4 as cj,Xm as ck,Si as cl,N4 as cm,i3 as cn,dm as co,q3 as cp,or as cq,X0 as cr,sp as cs,j4 as ct,cp as cu,dp as cv,n9 as cw,a9 as cx,K7 as cy,Z4 as cz,x7 as d,go as d$,O7 as d0,fp as d1,bp as d2,Ci as d3,qm as d4,Ym as d5,Qm as d6,vu as d7,rm as d8,Gm as d9,Zm as dA,Hc as dB,Tm as dC,ha as dD,Ws as dE,kp as dF,Lp as dG,wp as dH,xp as dI,Sp as dJ,Zs as dK,js as dL,I as dM,y9 as dN,vm as dO,Cm as dP,km as dQ,um as dR,gm as dS,mm as dT,_9 as dU,K9 as dV,Y7 as dW,qi as dX,$9 as dY,Kn as dZ,nn as d_,Pg as da,qg as db,t8 as dc,ba as dd,ve as de,zu as df,F7 as dg,V8 as dh,P8 as di,ig as dj,cu as dk,vg as dl,Cg as dm,yg as dn,Gn as dp,Ig as dq,vp as dr,dg as ds,cg as dt,sg as du,Au as dv,Dg as dw,_g as dx,yp as dy,Cp as dz,fg as e,xi as e$,lt as e0,yn as e1,M0 as e2,Dp as e3,zp as e4,Et as e5,Mp as e6,Ep as e7,ng as e8,eg as e9,Z7 as eA,T0 as eB,p9 as eC,b2 as eD,j8 as eE,im as eF,b4 as eG,Pp as eH,Wm as eI,hm as eJ,fm as eK,bm as eL,ym as eM,Ng as eN,$g as eO,Bg as eP,Hg as eQ,jg as eR,Lm as eS,xm as eT,wm as eU,Zg as eV,Ug as eW,Og as eX,I7 as eY,T7 as eZ,F8 as e_,ag as ea,A7 as eb,Tp as ec,z7 as ed,Ip as ee,Fp as ef,Ap as eg,s3 as eh,pm as ei,Sm as ej,cr as ek,a5 as el,_7 as em,D8 as en,tg as eo,Uc as ep,W7 as eq,xe as er,C6 as es,F3 as et,Jm as eu,bg as ev,c8 as ew,_p as ex,Kp as ey,j7 as ez,Vu as f,Ti as f0,r7 as f1,Le as f2,Rp as f3,Vp as f4,fn as f5,R3 as f6,mp as f7,N8 as f8,Lc as f9,g8 as fA,C2 as fB,Gg as fC,zc as fD,e0 as fE,b8 as fF,y8 as fG,Li as fH,Rd as fI,p7 as fJ,Gp as fK,Yp as fL,Pc as fM,J8 as fN,Y8 as fO,P7 as fP,W8 as fQ,B7 as fR,Kc as fS,f8 as fT,U8 as fU,M8 as fV,Z8 as fW,m8 as fa,lm as fb,h3 as fc,I3 as fd,n3 as fe,Op as ff,H7 as fg,V7 as fh,Nt as fi,$8 as fj,Up as fk,Hp as fl,Zp as fm,u3 as fn,$p as fo,ze as fp,Bp as fq,Np as fr,Wp as fs,xc as ft,p3 as fu,Xp as fv,qp as fw,Qp as fx,jp as fy,G7 as fz,oa as g,Ag as h,fe as i,ra as j,Q2 as k,yu as l,P as m,og as n,Tu as o,Lg as p,wg as q,ug as r,Qs as s,mg as t,gg as u,su as v,Eg as w,be as x,Ke as y,Pe as z};
