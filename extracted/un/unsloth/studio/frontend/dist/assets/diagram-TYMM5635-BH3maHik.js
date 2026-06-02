import{Dr as e,Er as t,Hr as n,Qt as r,Vr as i,dr as a,fr as o,gr as s,kn as c,kr as l,lr as u,mr as d,or as f,pr as p}from"./index-CsXMiQwf.js";import{t as m}from"./chunk-4BX2VUAB-BC0Dbbgo.js";import{t as h}from"./mermaid-parser.core-BHilnCTB.js";var g=a.packet,_=class{constructor(){this.packet=[],this.setAccTitle=e,this.getAccTitle=p,this.setDiagramTitle=l,this.getDiagramTitle=s,this.getAccDescription=o,this.setAccDescription=t}static{i(this,`PacketDB`)}getConfig(){let e=r({...g,...d().packet});return e.showBits&&(e.paddingY+=10),e}getPacket(){return this.packet}pushWord(e){e.length>0&&this.packet.push(e)}clear(){f(),this.packet=[]}},v=1e4,y=i((e,t)=>{m(e,t);let r=-1,i=[],a=1,{bitsPerRow:o}=t.getConfig();for(let{start:s,end:c,bits:l,label:u}of e.blocks){if(s!==void 0&&c!==void 0&&c<s)throw Error(`Packet block ${s} - ${c} is invalid. End must be greater than start.`);if(s??=r+1,s!==r+1)throw Error(`Packet block ${s} - ${c??s} is not contiguous. It should start from ${r+1}.`);if(l===0)throw Error(`Packet block ${s} is invalid. Cannot have a zero bit field.`);for(c??=s+(l??1)-1,l??=c-s+1,r=c,n.debug(`Packet block ${s} - ${r} with label ${u}`);i.length<=o+1&&t.getPacket().length<v;){let[e,n]=b({start:s,end:c,bits:l,label:u},a,o);if(i.push(e),e.end+1===a*o&&(t.pushWord(i),i=[],a++),!n)break;({start:s,end:c,bits:l,label:u}=n)}}t.pushWord(i)},`populate`),b=i((e,t,n)=>{if(e.start===void 0)throw Error(`start should have been set during first phase`);if(e.end===void 0)throw Error(`end should have been set during first phase`);if(e.start>e.end)throw Error(`Block start ${e.start} is greater than block end ${e.end}.`);if(e.end+1<=t*n)return[e,void 0];let r=t*n-1,i=t*n;return[{start:e.start,end:r,label:e.label,bits:r-e.start},{start:i,end:e.end,label:e.label,bits:e.end-i}]},`getNextFittingBlock`),x={parser:{yy:void 0},parse:i(async e=>{let t=await h(`packet`,e),r=x.parser?.yy;if(!(r instanceof _))throw Error(`parser.parser?.yy was not a PacketDB. This is due to a bug within Mermaid, please report this issue at https://github.com/mermaid-js/mermaid/issues.`);n.debug(t),y(t,r)},`parse`)},S=i((e,t,n,r)=>{let i=r.db,a=i.getConfig(),{rowHeight:o,paddingY:s,bitWidth:l,bitsPerRow:d}=a,f=i.getPacket(),p=i.getDiagramTitle(),m=o+s,h=m*(f.length+1)-(p?0:o),g=l*d+2,_=c(t);_.attr(`viewBox`,`0 0 ${g} ${h}`),u(_,h,g,a.useMaxWidth);for(let[e,t]of f.entries())C(_,t,e,a);_.append(`text`).text(p).attr(`x`,g/2).attr(`y`,h-m/2).attr(`dominant-baseline`,`middle`).attr(`text-anchor`,`middle`).attr(`class`,`packetTitle`)},`draw`),C=i((e,t,n,{rowHeight:r,paddingX:i,paddingY:a,bitWidth:o,bitsPerRow:s,showBits:c})=>{let l=e.append(`g`),u=n*(r+a)+a;for(let e of t){let t=e.start%s*o+1,n=(e.end-e.start+1)*o-i;if(l.append(`rect`).attr(`x`,t).attr(`y`,u).attr(`width`,n).attr(`height`,r).attr(`class`,`packetBlock`),l.append(`text`).attr(`x`,t+n/2).attr(`y`,u+r/2).attr(`class`,`packetLabel`).attr(`dominant-baseline`,`middle`).attr(`text-anchor`,`middle`).text(e.label),!c)continue;let a=e.end===e.start,d=u-2;l.append(`text`).attr(`x`,t+(a?n/2:0)).attr(`y`,d).attr(`class`,`packetByte start`).attr(`dominant-baseline`,`auto`).attr(`text-anchor`,a?`middle`:`start`).text(e.start),a||l.append(`text`).attr(`x`,t+n).attr(`y`,d).attr(`class`,`packetByte end`).attr(`dominant-baseline`,`auto`).attr(`text-anchor`,`end`).text(e.end)}},`drawWord`),w={draw:S},T={byteFontSize:`10px`,startByteColor:`black`,endByteColor:`black`,labelColor:`black`,labelFontSize:`12px`,titleColor:`black`,titleFontSize:`14px`,blockStrokeColor:`black`,blockStrokeWidth:`1`,blockFillColor:`#efefef`},E={parser:x,get db(){return new _},renderer:w,styles:i(({packet:e}={})=>{let t=r(T,e);return`
	.packetByte {
		font-size: ${t.byteFontSize};
	}
	.packetByte.start {
		fill: ${t.startByteColor};
	}
	.packetByte.end {
		fill: ${t.endByteColor};
	}
	.packetLabel {
		fill: ${t.labelColor};
		font-size: ${t.labelFontSize};
	}
	.packetTitle {
		fill: ${t.titleColor};
		font-size: ${t.titleFontSize};
	}
	.packetBlock {
		stroke: ${t.blockStrokeColor};
		stroke-width: ${t.blockStrokeWidth};
		fill: ${t.blockFillColor};
	}
	`},`styles`)};export{E as diagram};