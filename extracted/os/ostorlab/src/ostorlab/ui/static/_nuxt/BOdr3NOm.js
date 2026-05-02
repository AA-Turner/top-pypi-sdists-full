import{R as d,g as a}from"./EcQIca6j.js";class u{constructor(e={}){this.t=e,this.g=new(typeof TextDecoder<"u"?TextDecoder:require("util").TextDecoder)}decode(e){const t=new Uint8Array(e),s=new DataView(t.buffer);return this.D={array:t,view:s},this.S=0,this.C()}C(e=this.m(!1)){switch(e){case"Z":return null;case"N":return;case"T":return!0;case"F":return!1;case"i":return this.F((({view:t},s)=>t.getInt8(s)),1);case"U":return this.F((({view:t},s)=>t.getUint8(s)),1);case"I":return this.F((({view:t},s)=>t.getInt16(s)),2);case"l":return this.F((({view:t},s)=>t.getInt32(s)),4);case"L":return this.N(8,this.t.int64Handling,!0);case"d":return this.F((({view:t},s)=>t.getFloat32(s)),4);case"D":return this.F((({view:t},s)=>t.getFloat64(s)),8);case"H":return this.N(this.V(),this.t.highPrecisionNumberHandling,!1);case"C":return String.fromCharCode(this.C("i"));case"S":return this.j(this.V());case"[":return this.M();case"{":return this.O()}throw Error("Unexpected type")}Z(){let e,t;switch(this.m(!0)){case"$":if(this.q(),e=this.m(!1),this.m(!0)!=="#")throw Error("Expected count marker");case"#":this.q(),t=this.V()}return{type:e,count:t}}M(){const{type:e,count:t}=this.Z();if("ZTF".indexOf(e)!==-1)return Array(t).fill(this.C(e));if(this.t.useTypedArrays)switch(e){case"i":return this.B(t);case"U":return this.L(t);case"I":return Int16Array.from({length:t},(()=>this.C(e)));case"l":return Int32Array.from({length:t},(()=>this.C(e)));case"d":return Float32Array.from({length:t},(()=>this.C(e)));case"D":return Float64Array.from({length:t},(()=>this.C(e)))}if(t!=null){const s=Array(t);for(let r=0;r<t;r++)s[r]=this.C(e);return s}{const s=[];for(;this.m(!0)!=="]";)s.push(this.C());return this.q(),s}}O(){const{type:e,count:t}=this.Z(),s={};if(t!=null)for(let r=0;r<t;r++)s[this.C("S")]=this.C(e);else{for(;this.m(!0)!=="}";)s[this.C("S")]=this.C();this.q()}return s}V(){const e=this.C();if(Number.isInteger(e)&&e>=0)return e;throw Error("Invalid length/count")}N(e,t,s){if(typeof t=="function")return this.F(t,e);switch(t){case"skip":return void this.q(e);case"raw":return s?this.L(e):this.j(e)}throw Error("Unsuported type")}L(e){return this.F((({array:t},s)=>new Uint8Array(t.buffer,s,e)),e)}B(e){return this.F((({array:t},s)=>new Int8Array(t.buffer,s,e)),e)}j(e){return this.F((({array:t},s)=>this.g.decode(new DataView(t.buffer,s,e))),e)}q(e=1){this.R(e),this.S+=e}m(e){const{array:t,view:s}=this.D;let r="N";for(;r==="N"&&this.S<t.byteLength;)r=String.fromCharCode(s.getInt8(this.S++));return e&&this.S--,r}F(e,t){this.R(t);const s=e(this.D,this.S,t);return this.S+=t,s}R(e){if(this.S+e>this.D.array.byteLength)throw Error("Unexpected EOF")}}function h(o,e){return new u(e).decode(o)}class l{downloadArrayBuffer(e,t){const s=new Blob([new Uint8Array(t).buffer]),r=window.URL.createObjectURL(s),n=document.createElement("a");n.href=r,n.download=e,document.body.appendChild(n),n.click(),n.remove(),window.URL.revokeObjectURL(r)}}const p=a`query scans($scanIds: [Int], $page: Int, $numberElements: Int, $orderBy: OxoScanOrderByEnum, $sort: SortEnum) {
  scans(scanIds: $scanIds, page: $page, numberElements: $numberElements, orderBy: $orderBy, sort: $sort) {
    pageInfo {
      count
      numPages
    }
    scans {
      id
      title
      createdTime
      progress
      riskRating
      assets {
        __typename
        ... on OxoAndroidFileAssetType {
          id
          packageName
          path
        }
        ... on OxoIOSFileAssetType {
          id
          bundleId
          path
        }
        ... on OxoAndroidStoreAssetType {
          id
          packageName
          applicationName
        }
        ... on OxoIOSStoreAssetType {
          id
          bundleId
          applicationName
        }
        ... on OxoUrlsAssetType {
          id
          links {
            url
            method
          }
        }
        ... on OxoNetworkAssetType {
          id
          networks {
            host
            mask
          }
        }
        ... on OxoDomainNameAssetsType {
          id
          domainNames {
            name
          }
        }
      }
    }
  }
}
`,m=a`
query Scan($scanId: Int!) {
  scan(scanId: $scanId) {
      id
      title
      createdTime
      messageStatus
      progress
  }
}
`,f=a`mutation DeleteScans ($scanIds: [Int]!){
  deleteScans (scanIds: $scanIds) {
    result
  }
}
`,y=a`mutation stopScans($scanIds: [Int]!) {
  stopScans(scanIds: $scanIds) {
    scans {
      id
    }
  }
}`,S=a`mutation ImportScan($file: Upload!, $scanId: Int) {
  importScan(file: $file, scanId: $scanId) {
    message
  }
}`,w=a`
  mutation RunScan ($scan: OxoAgentScanInputType!) {
    runScan (scan: $scan) {
      scan {
        id
      }
    }
  }
`,I=a`
  mutation ExportScan($scanId: Int!) {
    exportScan(scanId: $scanId) {
      content
    }
  }
`;class A{requestor;totalScans;constructor(e){this.requestor=new d(e),this.totalScans=0}async getScans(e,t){t={...t},t.numberElements===-1&&(t.numberElements=void 0,t.page=void 0);const s=await this.requestor.post(e,{query:p,variables:t}),r=s?.data?.data.scans.scans||[];return this.totalScans=s?.data?.data?.scans?.pageInfo?.count||r.length,r}async getScan(e,t){return(await this.requestor.post(e,{query:m,variables:{scanId:t}}))?.data?.data?.scan||{}}async stopScans(e,t){return(await this.requestor.post(e,{query:y,variables:{scanIds:t}}))?.data?.stopScan?.result||!1}async deleteScans(e,t){return(await this.requestor.post(e,{query:f,variables:{scanIds:t}}))?.data?.deleteScans?.result||!1}async exportScan(e,t){const s=await this.requestor.$axios.post(e.endpoint,{query:I,variables:{scanId:t}},{responseType:"arraybuffer",headers:{Accept:"application/ubjson","X-Api-Key":e.apiKey}}),n=h(s?.data)?.data?.exportScan?.content;n!=null&&new l().downloadArrayBuffer("exported_scan.zip",n)}async importScan(e,t,s){const r=new FormData,n=S,c={scanId:s,file:null};r.append("operations",JSON.stringify({query:n,variables:c,app:t,maps:{app:["variables.file"]}})),r.append("0",t),r.append("map",JSON.stringify({0:["variables.file"]}));const i=await this.requestor.$axios.post(e.endpoint,r,{headers:{"Content-Type":"multipart/form-data","X-Api-Key":e.apiKey}});if((i?.data?.errors||[]).length>0)throw new Error(i?.data?.errors[0]?.message);return i?.data?.importScan?.result||!1}async runScan(e,t){const s=await this.requestor.post(e,{query:w,variables:{scan:t}});if((s?.data?.errors||[]).length>0)throw new Error(s?.data?.errors[0]?.message);if(s?.data?.data?.runScan===null||s?.data?.data?.runScan===void 0)throw new Error("An error occurred while creating the scan");return s?.data?.data?.runScan?.scan?.id}}export{A as S};
