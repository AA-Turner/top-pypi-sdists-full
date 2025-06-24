"use strict";(globalThis.webpackChunksuperset=globalThis.webpackChunksuperset||[]).push([[4943],{4943:(e,t,a)=>{a.r(t),a.d(t,{default:()=>se});var s=a(7240),i=a(96453),o=a(5556),n=a.n(o),r=a(7350),l=a.n(r),c=a(20249),h=a.n(c),m=a(24143),p=a.n(m),u=a(74353),d=a.n(u),y=a(83826),x=a.n(y),g=a(71111),b=a.n(g),f=a(7349),v=a(58928),A=a(94963),w=a(93641),k=a(32142),L=a(95579),T=a(53682),M=a(13270),$=a(36673);function C(e){return Object.keys(e).reduce(((e,t)=>{const a=e;return a[t]=t,a}),{})}const E=C({FORMULA:{value:"FORMULA",label:(0,L.t)("Formula")},EVENT:{value:"EVENT",label:(0,L.t)("Event"),supportNativeSource:!0},INTERVAL:{value:"INTERVAL",label:(0,L.t)("Interval"),supportNativeSource:!0},TIME_SERIES:{value:"TIME_SERIES",label:(0,L.t)("Time Series")}}),N=(E.FORMULA,C({NATIVE:{value:"NATIVE",label:"Superset annotation"}})),O={descriptionColumns:["long_descr"],intervalEndColumn:"end_dttm",timeColumn:"start_dttm",titleColumn:"short_descr"};function F(e){return e.sourceType===N.NATIVE?{...e,...O}:e}const D=E;var S=a(84338),I=a(17171);const B=n().oneOfType([n().number,n().oneOf(["auto"])]),R=n().oneOfType([n().string,n().shape({label:n().string})]),Y=n().shape({r:n().number.isRequired,g:n().number.isRequired,b:n().number.isRequired}),_=n().shape({x:n().number,y:n().number}),z=n().shape({x:n().string,y:n().number}),P=n().shape({outliers:n().arrayOf(n().number),Q1:n().number,Q2:n().number,Q3:n().number,whisker_high:n().number,whisker_low:n().number}),V=n().shape({markerLabels:n().arrayOf(n().string),markerLineLabels:n().arrayOf(n().string),markerLines:n().arrayOf(n().number),markers:n().arrayOf(n().number),measures:n().arrayOf(n().number),rangeLabels:n().arrayOf(n().string),ranges:n().arrayOf(n().number)}),U=n().shape({annotationType:n().oneOf(Object.keys(E)),color:n().string,hideLine:n().bool,name:n().string,opacity:n().string,show:n().bool,showMarkers:n().bool,sourceType:n().string,style:n().string,value:n().oneOfType([n().number,n().string]),width:n().number}),G=[{text:"No data",dy:"-.75em",class:"header"},{text:"Adjust filters or check the Datasource.",dy:".75em",class:"body"}];d().extend(x());const W=(0,f.mo)(v.M);b().utils.noData=function(e,t){const a=e.options().margin(),s=b().utils.availableHeight(null,t,a),i=b().utils.availableWidth(null,t,a),o=a.left+i/2,n=a.top+s/2;t.selectAll("g").remove();const r=t.selectAll(".nv-noData").data(G);r.enter().append("text").attr("class",(e=>`nvd3 nv-noData ${e.class}`)).attr("dy",(e=>e.dy)).style("text-anchor","middle"),r.attr("x",o).attr("y",n).text((e=>e.text))};const{getColor:j,getScale:q}=A,H=[w.Y.Compare,w.Y.TimePivot],Q={data:n().oneOfType([n().arrayOf(n().oneOfType([z,n().shape({key:n().string,values:n().arrayOf(z)}),n().shape({key:n().arrayOf(n().string),values:n().arrayOf(_)}),n().shape({classed:n().string,key:n().string,type:n().string,values:n().arrayOf(_),yAxis:n().number}),n().shape({label:n().string,values:n().arrayOf(P)}),n().shape({key:n().string,values:n().arrayOf(n().object)})])),V]),width:n().number,height:n().number,annotationData:n().object,annotationLayers:n().arrayOf(U),bottomMargin:B,colorScheme:n().string,comparisonType:n().string,contribution:n().bool,leftMargin:B,onError:n().func,showLegend:n().bool,showMarkers:n().bool,vizType:n().oneOf([w.Y.BoxPlot,"bubble",w.Y.Bullet,w.Y.Compare,"column",w.Y.TimePivot,"pie"]),xAxisFormat:n().string,numberFormat:n().string,xAxisLabel:n().string,xAxisShowMinMax:n().bool,xIsLogScale:n().bool,xTicksLayout:n().oneOf(["auto","staggered","45°"]),yAxisFormat:n().string,yAxisBounds:n().arrayOf(n().number),yAxisLabel:n().string,yAxisShowMinMax:n().bool,yIsLogScale:n().bool,isBarStacked:n().bool,showBarValue:n().bool,showBrush:n().oneOf([!0,"yes",!1,"no","auto"]),onBrushEnd:n().func,yAxis2Format:n().string,lineInterpolation:n().string,isDonut:n().bool,isPieLabelOutside:n().bool,pieLabelType:n().oneOf(["key","value","percent","key_value","key_percent","key_value_percent"]),showLabels:n().bool,entity:n().string,maxBubbleSize:n().number,xField:R,yField:R,sizeField:R,baseColor:Y},X=()=>{},J=(0,k.gV)();function K(e,t){const{data:a,width:s,height:i,annotationData:o,annotationLayers:n=[],baseColor:r,bottomMargin:c,colorScheme:m,comparisonType:u,contribution:y,entity:x,isBarStacked:g,isDonut:v,isPieLabelOutside:A,leftMargin:C,lineInterpolation:E="linear",markerLabels:N,markerLines:O,markerLineLabels:B,markers:R,maxBubbleSize:Y,onBrushEnd:_=X,onError:z=X,pieLabelType:P,rangeLabels:V,ranges:U,showBarValue:G,showBrush:Q,showLabels:K,showLegend:Z,showMarkers:ee,sizeField:te,vizType:ae,xAxisFormat:se,numberFormat:ie,xAxisLabel:oe,xAxisShowMinMax:ne=!1,xField:re,xIsLogScale:le,xTicksLayout:ce,yAxisFormat:he,yAxisBounds:me,yAxisLabel:pe,yAxisShowMinMax:ue=!1,yAxis2ShowMinMax:de=!1,yField:ye,yIsLogScale:xe,sliceId:ge}=t,be=null!==document.querySelector("#explorer-container"),fe=e;fe.innerHTML="";const ve=n.filter((e=>e.show));let Ae,we=fe,ke=null;for(;we.parentElement;){if(we.parentElement.id.startsWith("chart-id-")){ke=we.parentElement.id;break}we=we.parentElement}const Le=s;let Te="key";function Me(e){return e.includes(ae)}fe.style.width=`${s}px`,fe.style.height=`${i}px`,ke?(0,I.G0)(ke):(0,I.$v)(!0),b().addGraph((function(){const t=p().select(e);t.classed("superset-legacy-chart-nvd3",!0),t.classed(`superset-legacy-chart-nvd3-${h()(ae)}`,!0);let n=t.select("svg");n.empty()&&(n=t.append("svg"));const fe=ae===w.Y.Bullet?Math.min(i,50):i,we=Me(H),$e="staggered"===ce,Ce="45°"===ce?45:0;if(45===Ce&&(0,S.A)(Q))return z((0,L.t)("You cannot use 45° tick layout along with the time range filter")),null;const Ee=(0,S.A)(Q)||"auto"===Q&&i>=480&&"45°"!==ce,Ne=(0,k.gV)(ie);switch(ae){case w.Y.TimePivot:Ae=b().models.lineChart(),Ae.xScale(p().time.scale.utc()),Ae.interpolate(E);break;case w.Y.Pie:if(Ae=b().models.pieChart(),Te="x",Ae.valueFormat(Ne),v&&Ae.donut(!0),Ae.showLabels(K),Ae.labelsOutside(A),Ae.labelThreshold(.05),Ae.cornerRadius(!0),["key","value","percent"].includes(P))Ae.labelType(P);else if("key_value"===P)Ae.labelType((e=>`${e.data.x}: ${Ne(e.data.y)}`));else{const e=p().sum(a,(e=>e.y)),t=(0,k.gV)(T.A.PERCENT_2_POINT);"key_percent"===P?(Ae.tooltip.valueFormatter((e=>t(e))),Ae.labelType((a=>`${a.data.x}: ${t(a.data.y/e)}`))):(Ae.tooltip.valueFormatter((a=>`${Ne(a)} (${t(a/e)})`)),Ae.labelType((a=>`${a.data.x}: ${Ne(a.data.y)} (${t(a.data.y/e)})`)))}Ae.margin({top:0});break;case"column":Ae=b().models.multiBarChart().reduceXTicks(!1);break;case w.Y.Compare:Ae=b().models.cumulativeLineChart(),Ae.xScale(p().time.scale.utc()),Ae.useInteractiveGuideline(!0),Ae.xAxis.showMaxMin(!1);break;case w.Y.LegacyBubble:Ae=b().models.scatterChart(),Ae.showDistX(!1),Ae.showDistY(!1),Ae.tooltip.contentGenerator((e=>(0,I.oh)({point:e.point,entity:x,xField:re,yField:ye,sizeField:te,xFormatter:(0,I.wn)(se),yFormatter:(0,I.wn)(he),sizeFormatter:J}))),Ae.pointRange([5,Y**2]),Ae.pointDomain([0,p().max(a,(e=>p().max(e.values,(e=>e.size))))]);break;case w.Y.BoxPlot:Te="label",Ae=b().models.boxPlotChart(),Ae.x((e=>e.label)),Ae.maxBoxWidth(75);break;case w.Y.Bullet:Ae=b().models.bulletChart(),a.rangeLabels=V,a.ranges=U,a.markerLabels=N,a.markerLines=O,a.markerLineLabels=B,a.markers=R;break;default:throw new Error(`Unrecognized visualization for nvd3${ae}`)}let Oe;Ae.margin({left:0,bottom:0}),G&&((0,I.C$)(n,a,g,he),Ae.dispatch.on("stateChange.drawBarValues",(()=>{(0,I.C$)(n,a,g,he)}))),Ee&&_!==X&&Ae.focus&&Ae.focus.dispatch.on("brush",(e=>{const t=(0,I.EF)(e.extent);t&&e.brush.on("brushend",(()=>{_(t)}))})),Ae.xAxis&&Ae.xAxis.staggerLabels&&Ae.xAxis.staggerLabels($e),Ae.xAxis&&Ae.xAxis.rotateLabels&&Ae.xAxis.rotateLabels(Ce),Ae.x2Axis&&Ae.x2Axis.staggerLabels&&Ae.x2Axis.staggerLabels($e),Ae.x2Axis&&Ae.x2Axis.rotateLabels&&Ae.x2Axis.rotateLabels(Ce),"showLegend"in Ae&&void 0!==Z&&(Le<340&&ae!==w.Y.Pie?Ae.showLegend(!1):Ae.showLegend(Z)),xe&&Ae.yScale(p().scale.log()),le&&Ae.xScale(p().scale.log()),we?(Oe=(0,f.mo)(se),Ae.interactiveLayer.tooltip.headerFormatter(W)):Oe=(0,I.wn)(se),Ae.x2Axis&&Ae.x2Axis.tickFormat&&Ae.x2Axis.tickFormat(Oe),Ae.xAxis&&Ae.xAxis.tickFormat&&(Me([w.Y.BoxPlot])?Ae.xAxis.tickFormat((e=>e.length>40?`${e.slice(0,Math.max(0,40))}…`:e)):Ae.xAxis.tickFormat(Oe));let Fe=(0,I.wn)(he);if(Ae.yAxis&&Ae.yAxis.tickFormat&&(!y&&"percentage"!==u||he&&he!==T.A.SMART_NUMBER&&he!==T.A.SMART_NUMBER_SIGNED||(Fe=(0,k.gV)(T.A.PERCENT_1_POINT)),Ae.yAxis.tickFormat(Fe)),Ae.y2Axis&&Ae.y2Axis.tickFormat&&Ae.y2Axis.tickFormat(Fe),Ae.yAxis&&Ae.yAxis.ticks(5),Ae.y2Axis&&Ae.y2Axis.ticks(5),(0,I.dw)(Ae.xAxis,ne),(0,I.dw)(Ae.x2Axis,ne),(0,I.dw)(Ae.yAxis,ue),(0,I.dw)(Ae.y2Axis,de||ue),ae===w.Y.TimePivot){if(r){const{r:e,g:t,b:a}=r;Ae.color((s=>{const i=s.rank>0?.5*s.perc:1;return`rgba(${e}, ${t}, ${a}, ${i})`}))}Ae.useInteractiveGuideline(!0),Ae.interactiveLayer.tooltip.contentGenerator((e=>(0,I.qY)(e,Oe,Fe)))}else if(ae!==w.Y.Bullet){const e=q(m);Ae.color((t=>t.color||e((0,I.n0)(t[Te]),ge)))}Me([w.Y.Compare])&&Ae.interactiveLayer.tooltip.contentGenerator((e=>(0,I.Jy)(e,Fe))),Ae.width(Le),Ae.height(fe),n.datum(a).transition().duration(500).attr("height",fe).attr("width",Le).call(Ae),xe&&Ae.yAxis.tickFormat((e=>0!==e&&Math.log10(e)%1==0?Fe(e):"")),Ce>0&&n.select(".nv-x.nv-axis > g").selectAll("g").selectAll("text").attr("dx",-6.5);const De=()=>{if(Ae.yDomain&&Array.isArray(me)&&2===me.length){const[e,t]=me,s=(0,M.A)(e)&&!Number.isNaN(e),i=(0,M.A)(t)&&!Number.isNaN(t);if(s&&i)Ae.yDomain([e,t]),Ae.clipEdge(!0);else if(s||i){const[o,n]=(0,I.B2)(a),r=s?e:o,l=i?t:n;Ae.yDomain([r,l]),Ae.clipEdge(!0)}}};if(De(),Ae.dispatch&&Ae.dispatch.stateChange&&Ae.dispatch.on("stateChange.applyYAxisBounds",De),ee&&(n.selectAll(".nv-point").style("stroke-opacity",1).style("fill-opacity",1),Ae.dispatch.on("stateChange.showMarkers",(()=>{setTimeout((()=>{n.selectAll(".nv-point").style("stroke-opacity",1).style("fill-opacity",1)}),10)}))),void 0!==Ae.yAxis||void 0!==Ae.yAxis2){const t=Math.ceil(Math.min(s*(be?.01:.03),30)),i=Ae.margin();Ae.xAxis&&(i.bottom=28);const r=(0,I.cm)(n,Ae.yAxis2?"nv-y1":"nv-y"),h=(0,I.cm)(n,"nv-x");if(i.left=r+t,pe&&""!==pe&&(i.left+=25),G&&(i.top+=24),ne&&(i.right=Math.max(20,h/2)+t),45===Ce?(i.bottom=h*Math.sin(Math.PI*Ce/180)+t+30,i.right=h*Math.cos(Math.PI*Ce/180)+t):$e&&(i.bottom=40),c&&"auto"!==c&&(i.bottom=parseInt(c,10)),C&&"auto"!==C&&(i.left=C),oe&&""!==oe&&Ae.xAxis){i.bottom+=25;let e=0;i.bottom&&!Number.isNaN(i.bottom)&&(e=i.bottom-45),Ae.xAxis.axisLabel(oe).axisLabelDistance(e)}if(pe&&""!==pe&&Ae.yAxis){let e=0;i.left&&!Number.isNaN(i.left)&&(e=i.left-70),Ae.yAxis.axisLabel(pe).axisLabelDistance(e)}if(we&&o&&ve.length>0){const e=ve.filter((e=>e.annotationType===D.TIME_SERIES)).reduce(((e,t)=>e.concat((o[t.name]||[]).map((e=>{if(!e)return{};const a=Array.isArray(e.key)?`${t.name}, ${e.key.join(", ")}`:`${t.name}, ${e.key}`;return{...e,key:a,color:t.color,strokeWidth:t.width,classed:`${t.opacity} ${t.style} nv-timeseries-annotation-layer showMarkers${t.showMarkers} hideLine${t.hideLine}`}})))),[]);a.push(...e)}if(ke&&(Ae&&Ae.interactiveLayer&&Ae.interactiveLayer.tooltip&&Ae.interactiveLayer.tooltip.classes([(0,I.Ir)(ke)]),Ae&&Ae.tooltip&&Ae.tooltip.classes([(0,I.Ir)(ke)])),Ae.margin(i),n.datum(a).transition().duration(500).attr("width",Le).attr("height",fe).call(Ae),window.addEventListener("scroll",l()((()=>(0,I.$v)(!1)),250)),we&&ve.length>0){const t=ve.filter((e=>e.annotationType===D.FORMULA)),s=Ae.xAxis.scale().domain()[1].valueOf(),i=Ae.xAxis.scale().domain()[0].valueOf();let r;if(r=Ae.xScale?Ae.xScale():Ae.xAxis.scale?Ae.xAxis.scale():p().scale.linear(),r&&r.clamp&&r.clamp(!0),t.length>0){const e=[];let o=Math.min(...a.map((e=>Math.min(...e.values.slice(1).map(((t,a)=>t.x-e.values[a].x))))));const n=(s-i)/(o||1);o=n<100?(s-i)/100:o,o=n>500?(s-i)/500:o,e.push(i);for(let t=i;t<s;t+=o)e.push(t);e.push(s);const r=t.map((t=>{const{value:a}=t;return{key:t.name,values:e.map((e=>({x:e,y:(0,$.p)(a,e)}))),color:t.color,strokeWidth:t.width,classed:`${t.opacity} ${t.style}`}}));a.push(...r)}const l=Ae.xAxis1?Ae.xAxis1:Ae.xAxis,c=Ae.yAxis1?Ae.yAxis1:Ae.yAxis,h=l.scale().range()[1],u=c.scale().range()[0];o&&(ve.filter((e=>e.annotationType===D.EVENT&&o&&o[e.name])).forEach(((t,a)=>{const s=F(t),i=p().select(e).select(".nv-wrap").append("g").attr("class",`nv-event-annotation-layer-${a}`),n=s.color||j((0,I.n0)(s.name),m),l=(0,I.AN)({...s,annotationTipClass:`arrow-down nv-event-annotation-layer-${t.sourceType}`}),c=(o[s.name].records||[]).map((e=>{const t=new Date(d().utc(e[s.timeColumn]));return{...e,[s.timeColumn]:t}})).filter((e=>!Number.isNaN(e[s.timeColumn].getMilliseconds())));c.length>0&&i.selectAll("line").data(c).enter().append("line").attr({x1:e=>r(new Date(e[s.timeColumn])),y1:0,x2:e=>r(new Date(e[s.timeColumn])),y2:u}).attr("class",`${s.opacity} ${s.style}`).style("stroke",n).style("stroke-width",s.width).on("mouseover",l.show).on("mouseout",l.hide).call(l),Ae.focus&&Ae.focus.dispatch.on("onBrush.event-annotation",(()=>{i.selectAll("line").data(c).attr({x1:e=>r(new Date(e[s.timeColumn])),y1:0,x2:e=>r(new Date(e[s.timeColumn])),y2:u,opacity:e=>{const t=r(new Date(e[s.timeColumn]));return t>0&&t<h?1:0}})}))})),ve.filter((e=>e.annotationType===D.INTERVAL&&o&&o[e.name])).forEach(((t,a)=>{const s=F(t),i=p().select(e).select(".nv-wrap").append("g").attr("class",`nv-interval-annotation-layer-${a}`),n=s.color||j((0,I.n0)(s.name),m),l=(0,I.AN)(s),c=(o[s.name].records||[]).map((e=>{const t=new Date(d().utc(e[s.timeColumn])),a=new Date(d().utc(e[s.intervalEndColumn]));return{...e,[s.timeColumn]:t,[s.intervalEndColumn]:a}})).filter((e=>!Number.isNaN(e[s.timeColumn].getMilliseconds())&&!Number.isNaN(e[s.intervalEndColumn].getMilliseconds())));c.length>0&&i.selectAll("rect").data(c).enter().append("rect").attr({x:e=>Math.min(r(new Date(e[s.timeColumn])),r(new Date(e[s.intervalEndColumn]))),y:0,width:e=>Math.max(Math.abs(r(new Date(e[s.intervalEndColumn]))-r(new Date(e[s.timeColumn]))),1),height:u}).attr("class",`${s.opacity} ${s.style}`).style("stroke-width",s.width).style("stroke",n).style("fill",n).style("fill-opacity",.2).on("mouseover",l.show).on("mouseout",l.hide).call(l),Ae.focus&&Ae.focus.dispatch.on("onBrush.interval-annotation",(()=>{i.selectAll("rect").data(c).attr({x:e=>r(new Date(e[s.timeColumn])),width:e=>{const t=r(new Date(e[s.timeColumn]));return r(new Date(e[s.intervalEndColumn]))-t}})}))}))),n.datum(a).attr("height",fe).attr("width",Le).call(Ae),Ae.dispatch.on("renderEnd.timeseries-annotation",(()=>{p().selectAll(".slice_container .nv-timeseries-annotation-layer.showMarkerstrue .nv-point").style("stroke-opacity",1).style("fill-opacity",1),p().selectAll(".slice_container .nv-timeseries-annotation-layer.hideLinetrue").style("stroke-width",0)}))}}return(0,I.OK)(Ae),Ae}))}K.displayName="NVD3",K.propTypes=Q;const Z=K;var ee=a(2445);const te=(0,s.A)(Z,{componentWillUnmount:function(){const{id:e}=this.props;null!=e?(0,I.G0)(e):(0,I.$v)(!0)}}),ae=({className:e,...t})=>(0,ee.Y)("div",{className:e,children:(0,ee.Y)(te,{...t})});ae.propTypes={className:n().string.isRequired};const se=(0,i.I4)(ae)`
  .superset-legacy-chart-nvd3-dist-bar,
  .superset-legacy-chart-nvd3-bar {
    overflow-x: auto !important;
    svg {
      &.nvd3-svg {
        width: auto;
        font-size: ${({theme:e})=>e.typography.sizes.m};
      }
    }
  }
  .superset-legacy-chart-nvd3 {
    nv-x text {
      font-size: ${({theme:e})=>e.typography.sizes.m};
    }
    g.superset path {
      stroke-dasharray: 5, 5;
    }
    .nvtooltip tr.highlight td {
      font-weight: ${({theme:e})=>e.typography.weights.bold};
      font-size: ${({theme:e})=>e.typography.sizes.m}px !important;
    }
    text.nv-axislabel {
      font-size: ${({theme:e})=>e.typography.sizes.m} !important;
    }
    g.solid path,
    line.solid {
      stroke-dasharray: unset;
    }
    g.dashed path,
    line.dashed {
      stroke-dasharray: 5, 5;
    }
    g.longDashed path,
    line.dotted {
      stroke-dasharray: 1, 1;
    }

    g.opacityLow path,
    line.opacityLow {
      stroke-opacity: 0.2;
    }

    g.opacityMedium path,
    line.opacityMedium {
      stroke-opacity: 0.5;
    }
    g.opacityHigh path,
    line.opacityHigh {
      stroke-opacity: 0.8;
    }
    g.time-shift-0 path,
    line.time-shift-0 {
      stroke-dasharray: 5, 5;
    }
    g.time-shift-1 path,
    line.time-shift-1 {
      stroke-dasharray: 1, 5;
    }
    g.time-shift-2 path,
    line.time-shift-3 {
      stroke-dasharray: 5, 1;
    }
    g.time-shift-3 path,
    line.time-shift-3 {
      stroke-dasharray: 5, 1;
    }
    g.time-shift-4 path,
    line.time-shift-4 {
      stroke-dasharray: 5, 10;
    }
    g.time-shift-5 path,
    line.time-shift-5 {
      stroke-dasharray: 0.9;
    }
    g.time-shift-6 path,
    line.time-shift-6 {
      stroke-dasharray: 15, 10, 5;
    }
    g.time-shift-7 path,
    line.time-shift-7 {
      stroke-dasharray: 15, 10, 5, 10;
    }
    g.time-shift-8 path,
    line.time-shift-8 {
      stroke-dasharray: 15, 10, 5, 10, 15;
    }
    g.time-shift-9 path,
    line.time-shift-9 {
      stroke-dasharray: 5, 5, 1, 5;
    }
    .nv-noData.body {
      font-size: ${({theme:e})=>e.typography.sizes.m};
      font-weight: ${({theme:e})=>e.typography.weights.normal};
    }
  }
  .superset-legacy-chart-nvd3-tr-highlight {
    border-top: 1px solid;
    border-bottom: 1px solid;
    font-weight: ${({theme:e})=>e.typography.weights.bold};
  }
  .superset-legacy-chart-nvd3-tr-total {
    font-weight: ${({theme:e})=>e.typography.weights.bold};
  }
  .nvtooltip {
    .tooltip-header {
      white-space: nowrap;
      font-weight: ${({theme:e})=>e.typography.weights.bold};
    }
    tbody tr:not(.tooltip-header) td:nth-of-type(2) {
      word-break: break-word;
    }
  }
  .d3-tip.nv-event-annotation-layer-table,
  .d3-tip.nv-event-annotation-layer-NATIVE {
    width: 200px;
    border-radius: 2px;
    background-color: ${({theme:e})=>e.colors.grayscale.base};
    fill-opacity: 0.6;
    margin: ${({theme:e})=>2*e.gridUnit}px;
    padding: ${({theme:e})=>2*e.gridUnit}px;
    color: ${({theme:e})=>e.colors.grayscale.light5};
    &:after {
      content: '\\25BC';
      font-size: ${({theme:e})=>e.typography.sizes.m};
      color: ${({theme:e})=>e.colors.grayscale.base};
      position: absolute;
      bottom: -14px;
      left: 94px;
    }
  }
`},7240:(e,t,a)=>{a.d(t,{A:()=>o});var s=a(96540),i=a(2445);function o(e,t){class a extends s.Component{constructor(e){super(e),this.container=void 0,this.setContainerRef=this.setContainerRef.bind(this)}componentDidMount(){this.execute()}componentDidUpdate(){this.execute()}componentWillUnmount(){this.container=void 0,null!=t&&t.componentWillUnmount&&t.componentWillUnmount.bind(this)()}setContainerRef(e){this.container=e}execute(){this.container&&e(this.container,this.props)}render(){const{id:e,className:t}=this.props;return(0,i.Y)("div",{ref:this.setContainerRef,id:e,className:t})}}const o=a;return e.displayName&&(o.displayName=e.displayName),e.propTypes&&(o.propTypes={...o.propTypes,...e.propTypes}),e.defaultProps&&(o.defaultProps=e.defaultProps),a}}}]);