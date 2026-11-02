import{d as y,C as k,c as u,bG as _,a as h,l as t,e as c,F as b,b3 as g,b as f,ch as M,a1 as p,w as x,aH as N,b7 as C,t as w,ck as T,bU as z,A as s,_ as I}from"./index-Dkn7ZTWz.js";import{c as n}from"./createLucideIcon-BB5siJz0.js";import{M as S}from"./message-square-text-3hZ7FHum.js";/**
 * @license @lucide/vue v1.23.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const V=[["path",{d:"M5 21v-6",key:"1hz6c0"}],["path",{d:"M12 21V9",key:"uvy0l4"}],["path",{d:"M19 21V3",key:"11j9sm"}]],q=n("chart-no-axes-column-increasing",V);/**
 * @license @lucide/vue v1.23.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const B=[["path",{d:"M3 5h1",key:"1mv5vm"}],["path",{d:"M3 12h1",key:"lp3yf2"}],["path",{d:"M3 19h1",key:"w6f3n9"}],["path",{d:"M8 5h1",key:"1nxr5w"}],["path",{d:"M8 12h1",key:"1con00"}],["path",{d:"M8 19h1",key:"k7p10e"}],["path",{d:"M13 5h8",key:"a7qcls"}],["path",{d:"M13 12h8",key:"h98zly"}],["path",{d:"M13 19h8",key:"c3s6r1"}]],D=n("logs",B);/**
 * @license @lucide/vue v1.23.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const L=[["path",{d:"m10.586 5.414-5.172 5.172",key:"4mc350"}],["path",{d:"m18.586 13.414-5.172 5.172",key:"8c96vv"}],["path",{d:"M6 12h12",key:"8npq4p"}],["circle",{cx:"12",cy:"20",r:"2",key:"144qzu"}],["circle",{cx:"12",cy:"4",r:"2",key:"muu5ef"}],["circle",{cx:"20",cy:"12",r:"2",key:"1xzzfp"}],["circle",{cx:"4",cy:"12",r:"2",key:"1hvhnz"}]],R=n("waypoints",L),A={class:"data-workspace"},F={class:"data-tabs-scroll"},P=["aria-label"],$=["href","aria-selected","onClick"],j=y({__name:"DataPage",setup(E){const{t:e}=k(),r=z(),i=u(()=>[{value:"statistics",label:e("core.navigation.dataTabs.statistics"),routeName:"Stats",icon:q},{value:"conversations",label:e("core.navigation.dataTabs.conversations"),routeName:"Conversation",icon:S},{value:"logs",label:e("core.navigation.dataTabs.logs"),routeName:"Console",icon:D},{value:"trace",label:e("core.navigation.dataTabs.trace"),routeName:"Trace",icon:R}]),l=u(()=>String(r.meta.dataTab||"statistics"));return _(()=>r.meta.dataTab,d=>{const o=i.value.find(a=>a.value===d);o&&localStorage.setItem("data_last_tab",o.routeName)},{immediate:!0}),(d,o)=>(s(),h("div",A,[t("div",F,[t("nav",{class:"data-tabs",role:"tablist","aria-label":c(e)("core.navigation.data")},[(s(!0),h(b,null,g(i.value,a=>(s(),p(c(T),{key:a.value,custom:"",to:{name:a.routeName}},{default:x(({href:m,navigate:v})=>[t("a",{href:m,class:N(["data-tab",{"data-tab--active":l.value===a.value}]),role:"tab","aria-selected":l.value===a.value,onClick:v},[(s(),p(C(a.icon),{size:16,"stroke-width":1.8,"aria-hidden":"true"})),t("span",null,w(a.label),1)],10,$)]),_:2},1032,["to"]))),128))],8,P)]),f(c(M))]))}}),W=I(j,[["__scopeId","data-v-f162a78a"]]);export{W as default};
