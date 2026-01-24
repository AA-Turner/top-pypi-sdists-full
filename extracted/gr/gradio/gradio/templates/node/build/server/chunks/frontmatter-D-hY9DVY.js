import { ai as Cu, a8 as yc, a3 as Wc, a5 as Pu, aq as mt, v } from './Code.svelte_svelte_type_style_lang-UrlqsTby.js';
import { yaml as a } from './yaml-6088L0kW.js';
import './2-B89dC7Mi.js';
import './index5-BoOEKc6P.js';
import './dev-fallback-Bc5Ork7Y.js';
import './async-Mo2Ia14K.js';
import './index-D1Ptw7Az.js';
import 'path';
import 'url';
import 'fs';
import './spring-DE8vsW2o.js';

const n=/^---\s*$/m,F={defineNodes:[{name:"Frontmatter",block:true},"FrontmatterMark"],props:[yc({Frontmatter:[v.documentMeta,v.monospace],FrontmatterMark:v.processingInstruction}),Wc.add({Frontmatter:Pu,FrontmatterMark:()=>null})],wrap:Cu(t=>{const{parser:e}=mt.define(a);return t.type.name==="Frontmatter"?{parser:e,overlay:[{from:t.from+4,to:t.to-4}]}:null}),parseBlock:[{name:"Frontmatter",before:"HorizontalRule",parse:(t,e)=>{let r;const a=new Array;if(t.lineStart===0&&n.test(e.text)){for(a.push(t.elt("FrontmatterMark",0,4));t.nextLine();)if(n.test(e.text)){r=t.lineStart+4;break}return r!==void 0&&(a.push(t.elt("FrontmatterMark",r-4,r)),t.addElement(t.elt("Frontmatter",0,r,a))),true}return  false}}]};

export { F as frontmatter };
//# sourceMappingURL=frontmatter-D-hY9DVY.js.map
