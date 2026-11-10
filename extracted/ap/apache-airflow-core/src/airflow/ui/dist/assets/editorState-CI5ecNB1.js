import{$c as e,$s as t,Ac as n,Bs as r,Cs as i,Du as a,Fc as o,Ff as s,Gs as c,If as l,Kf as u,Mu as ee,Oc as d,Oo as te,Rf as f,Sc as p,Ss as ne,_c as m,ac as h,ad as g,bc as _,bo as re,gc as v,gp as y,ic as b,if as x,np as ie,oo as S,tc as C,uc as w,vf as T,xc as ae,zs as E}from"./textModel-DszL-kTz.js";import{M as D,_t as O,at as oe}from"./actionbar-DaUIy8yJ.js";var k=r,se=class extends l{constructor(e){super(),this.containerDomNode=document.createElement(`div`),this.containerDomNode.className=`monaco-hover`,this.containerDomNode.classList.toggle(`fade-in`,!!e),this.containerDomNode.tabIndex=0,this.containerDomNode.setAttribute(`role`,`tooltip`),this.contentsDomNode=document.createElement(`div`),this.contentsDomNode.className=`monaco-hover-content`,this.scrollbar=this._register(new oe(this.contentsDomNode,{consumeMouseWheelIfScrollbarIsNeeded:!0})),this.containerDomNode.appendChild(this.scrollbar.getDomNode())}onContentsChanged(){this.scrollbar.scanDomNode()}},ce=class e extends l{static render(t,n,r){return new e(t,n,r)}constructor(e,t,n){super(),this.actionLabel=t.label,this.actionKeybindingLabel=n,this.actionContainer=b(e,k(`div.action-container`)),this.actionContainer.setAttribute(`tabindex`,`0`),this.action=b(this.actionContainer,k(`a.action`)),this.action.setAttribute(`role`,`button`),t.iconClass&&b(this.action,k(`span.icon`)).classList.add(...t.iconClass.split(` `)),this.actionRenderedLabel=n?`${t.label} (${n})`:t.label;let r=b(this.action,k(`span`));r.textContent=this.actionRenderedLabel,this._store.add(new A(this.actionContainer,t.run)),this._store.add(new j(this.actionContainer,t.run,[3,10])),this.setEnabled(!0)}setEnabled(e){e?(this.actionContainer.classList.remove(`disabled`),this.actionContainer.removeAttribute(`aria-disabled`)):(this.actionContainer.classList.add(`disabled`),this.actionContainer.setAttribute(`aria-disabled`,`true`))}};function le(e,t){return e&&t?y(7,`Inspect this in the accessible view with {0}.`,t):e?y(8,`Inspect this in the accessible view via the command Open Accessible View which is currently not triggerable via keybinding.`):``}var A=class extends l{constructor(e,n){super(),this._register(t(e,c.CLICK,t=>{t.stopPropagation(),t.preventDefault(),n(e)}))}},j=class extends l{constructor(e,n,r){super(),this._register(t(e,c.KEY_DOWN,t=>{let i=new a(t);r.some(e=>i.equals(e))&&(t.stopPropagation(),t.preventDefault(),n(e))}))}},M=E(`openerService`),N=`default`;function P(e,t){return e.with({fragment:`${t.startLineNumber},${t.startColumn}${t.endLineNumber?`-${t.endLineNumber}${t.endColumn?`,${t.endColumn}`:``}`:``}`})}function F(e){let t,n=/^L?(\d+)(?:,(\d+))?(-L?(\d+)(?:,(\d+))?)?/.exec(e.fragment);return n&&(t={startLineNumber:parseInt(n[1]),startColumn:n[2]?parseInt(n[2]):1,endLineNumber:n[4]?parseInt(n[4]):void 0,endColumn:n[4]?n[5]?parseInt(n[5]):1:void 0},e=e.with({fragment:``})),{selection:t,uri:e}}var I;(function(e){e[e.AVOID=0]=`AVOID`,e[e.ALIGN=1]=`ALIGN`})(I||={});function L(e,t,n){let r=n.mode===I.ALIGN?n.offset:n.offset+n.size,i=n.mode===I.ALIGN?n.offset+n.size:n.offset;return n.position===0?t<=e-r?{position:r,result:`ok`}:t<=i?{position:i-t,result:`flipped`}:{position:Math.max(e-t,0),result:`overlap`}:t<=i?{position:i-t,result:`ok`}:t<=e-r&&i<t/2?{position:r,result:`flipped`}:{position:0,result:`overlap`}}function R(e,t,n,r){let i=r?.anchorAlignment??0,a=r?.anchorPosition??0,o=r?.anchorAxisAlignment??0,s,c;if(o===0){let r={offset:n.top-e.top,size:n.height,position:a===0?0:1},o={offset:n.left,size:n.width,position:i===0?0:1,mode:I.ALIGN},l=L(e.height,t.height,r);s=l.position+e.top,l.result===`flipped`&&(a=+(a===0)),D.intersects({start:s,end:s+t.height},{start:r.offset,end:r.offset+r.size})&&(o.mode=I.AVOID);let u=L(e.width,t.width,o);c=u.position,u.result===`flipped`&&(i=+(i===0))}else{let r={offset:n.left,size:n.width,position:i===0?0:1},o={offset:n.top,size:n.height,position:a===0?0:1,mode:I.ALIGN},l=L(e.width,t.width,r);c=l.position,l.result===`flipped`&&(i=+(i===0)),D.intersects({start:c,end:c+t.width},{start:r.offset,end:r.offset+r.size})&&(o.mode=I.AVOID);let u=L(e.height,t.height,o);s=u.position+e.top,u.result===`flipped`&&(a=+(a===0))}let l=e.width-(c+t.width),u=e.height-(s+t.height);return{top:s,left:c,bottom:u,right:l,anchorAlignment:i,anchorPosition:a}}function z(e){let t=e;return!!t&&typeof t.x==`number`&&typeof t.y==`number`}var B=`context-view-menu-motion`,V=`context-view-menu-motion-closing`,H=[`modern-ui`,`monaco-enable-motion`],U=`--vscode-context-view-close-animation-duration`,W=`--vscode-context-view-menu-motion-shadow`,G=`--vscode-context-view-menu-motion-close-start-opacity`,K=`--vscode-context-view-menu-motion-close-start-transform`,ue=250,q=`cubic-bezier(0.22, 1, 0.36, 1)`,de={className:V,duration:150,requiredAncestorClasses:H};function J(e){return`
	${e} .context-view.${B} {
		animation: none;
		box-shadow: none;
		overflow: visible;
	}

	${e} .context-view.${B} > .monaco-scrollable-element {
		animation: context-view-menu-motion-open ${ue}ms ${q} backwards;
		box-shadow: var(${W});
		transform-origin: top left;
		will-change: opacity;
	}

	${e} .context-view.${B}.right > .monaco-scrollable-element {
		transform-origin: top right;
	}

	${e} .context-view.${B}.top > .monaco-scrollable-element {
		transform-origin: bottom left;
	}

	${e} .context-view.${B}.top.right > .monaco-scrollable-element {
		transform-origin: bottom right;
	}

	${e} .context-view.${B}.${V} > .monaco-scrollable-element {
		animation: context-view-menu-motion-close var(${U}) ${q} both;
		pointer-events: none;
	}

	@keyframes context-view-menu-motion-open {
		0% {
			opacity: 0;
			transform: scale(0.97);
		}

		100% {
			opacity: 1;
			transform: scale(1);
		}
	}

	@keyframes context-view-menu-motion-close {
		0% {
			opacity: var(${G}, 1);
			transform: var(${K}, scale(1));
		}

		100% {
			opacity: 0;
			transform: scale(0.99);
		}
	}`}var fe;function pe(){fe||=O(void 0,e=>{e.textContent=J(`.modern-ui.monaco-enable-motion`)})}function Y(e){if(o(e)){let t=v(e),n=m(e);return{top:t.top*n,left:t.left*n,width:t.width*n,height:t.height*n}}return z(e)?{top:e.y,left:e.x,width:e.width||1,height:e.height||2}:{top:e.posy,left:e.posx,width:2,height:2}}var me=class t extends l{static{this.BUBBLE_UP_EVENTS=[`click`,`keydown`,`focus`,`blur`]}static{this.BUBBLE_DOWN_EVENTS=[`click`]}constructor(e,t){super(),this.container=null,this.useFixedPosition=!1,this.useShadowDOM=!1,this.delegate=null,this.toDisposeOnClean=l.None,this.toDisposeOnSetContainer=l.None,this.shadowRoot=null,this.shadowRootHostElement=null,pe(),this.view=r(`.context-view`),d(this.view),this.setContainer(e,t),this._register(u(()=>this.setContainer(null,1)))}setContainer(e,n){this.useFixedPosition=n!==1;let i=this.useShadowDOM;if(this.useShadowDOM=n===3,(e!==this.container||i!==this.useShadowDOM)&&(this.container&&=(this.toDisposeOnSetContainer.dispose(),this.view.remove(),this.shadowRoot&&(this.shadowRoot=null,this.shadowRootHostElement?.remove(),this.shadowRootHostElement=null),null),e)){if(this.container=e,this.useShadowDOM){this.shadowRootHostElement=r(`.shadow-root-host`),Object.assign(this.shadowRootHostElement.style,{position:`fixed`,top:`0`,left:`0`,width:`0`,height:`0`}),this.container.appendChild(this.shadowRootHostElement),this.shadowRoot=this.shadowRootHostElement.attachShadow({mode:`open`});let e=document.createElement(`style`);e.textContent=he,this.shadowRoot.appendChild(e),this.shadowRoot.appendChild(this.view),this.shadowRoot.appendChild(r(`slot`))}else this.container.appendChild(this.view);let n=new f;t.BUBBLE_UP_EVENTS.forEach(e=>{n.add(C(this.container,e,e=>{this.onDOMEvent(e,!1)}))}),t.BUBBLE_DOWN_EVENTS.forEach(e=>{n.add(C(this.container,e,e=>{this.onDOMEvent(e,!0)},!0))}),this.toDisposeOnSetContainer=n}}show(t){this.completeHideAnimation(),this.isVisible()&&this.hide(void 0,!0),h(this.view),this.view.className=`context-view monaco-component`,this.view.style.top=`0px`,this.view.style.left=`0px`;let n=`${2575+(t.layer??0)}`;this.view.style.zIndex=n,this.shadowRootHostElement&&(this.shadowRootHostElement.style.zIndex=n),this.view.style.position=this.useFixedPosition?`fixed`:`absolute`,e(this.view),this.toDisposeOnClean=t.render(this.view)||l.None,this.delegate=t,this.doLayout(),this.delegate.focus?.()}getViewElement(){return this.view}layout(){this.isVisible()&&(this.delegate.canRelayout===!1&&!(ie&&ee.pointerEvents)?this.hide():(this.delegate?.layout?.(),this.doLayout()))}doLayout(){if(!this.isVisible())return;let e=Y(this.delegate.getAnchor()),t=this.container?p(this.container):w(),n={top:t.pageYOffset,left:t.pageXOffset,width:t.innerWidth,height:t.innerHeight};this.view.classList.toggle(`fixed`,this.useFixedPosition),this.view.style.top=`0px`,this.view.style.left=`0px`;let r=v(this.view),i={width:ae(this.view),height:_(this.view)},a=this.delegate.anchorPosition,o=this.delegate.anchorAlignment,s=this.delegate.anchorAxisAlignment,c=R(n,i,e,{anchorAlignment:o,anchorPosition:a,anchorAxisAlignment:s}),{top:l,left:u}=c;this.view.classList.remove(`top`,`bottom`,`left`,`right`),this.view.classList.add(c.anchorPosition===0?`bottom`:`top`),this.view.classList.add(c.anchorAlignment===0?`left`:`right`),this.view.style.top=`${l-r.top}px`,this.view.style.left=`${u-r.left}px`,this.view.style.width=`initial`}hide(e,t=!1){if(this.hidingContextView){t&&this.completeHideAnimation();return}let n=this.delegate;if(this.delegate=null,!n)return;let r=this.toDisposeOnClean;this.toDisposeOnClean=l.None,n.onHide?.(e);let i=n.closeAnimation;if(!t&&i&&i.duration>0&&this.hasRequiredAncestorClasses(i.requiredAncestorClasses)){this.view.style.setProperty(U,`${i.duration}ms`),this.prepareMenuCloseAnimation(),this.view.inert=!0,this.view.classList.add(i.className);let e=setTimeout(()=>this.completeHideAnimation(),i.duration);this.hidingContextView={disposable:u(()=>clearTimeout(e)),toDispose:r,className:i.className}}else r.dispose(),d(this.view)}isVisible(){return!!this.delegate}completeHideAnimation(){let e=this.hidingContextView;e&&(this.hidingContextView=void 0,e.disposable.dispose(),this.view.classList.remove(e.className),this.view.style.removeProperty(U),this.view.style.removeProperty(G),this.view.style.removeProperty(K),e.toDispose.dispose(),d(this.view),this.view.inert=!1)}prepareMenuCloseAnimation(){if(!this.view.classList.contains(`context-view-menu-motion`))return;let e=Array.from(this.view.children).find(e=>o(e)&&e.classList.contains(`monaco-scrollable-element`));if(!o(e))return;let t=p(e).getComputedStyle(e);this.view.style.setProperty(G,t.opacity),this.view.style.setProperty(K,t.transform)}hasRequiredAncestorClasses(e){if(!e?.length)return!0;for(let t=this.view;t;){let n=t;if(e.every(e=>n.classList.contains(e)))return!0;if(n.parentElement)t=n.parentElement;else{let e=n.getRootNode();t=e instanceof ShadowRoot&&o(e.host)?e.host:null}}return!1}onDOMEvent(e,t){this.delegate&&(this.delegate.onDOMEvent?this.delegate.onDOMEvent(e,p(e).document.activeElement):t&&!n(e.target,this.container)&&this.hide())}dispose(){this.hide(),this.completeHideAnimation(),super.dispose()}},he=`
	:host {
		all: initial; /* 1st rule so subsequent properties are reset. */
	}

	.codicon[class*='codicon-'] {
		font: normal normal normal 16px/1 codicon;
		display: inline-block;
		text-decoration: none;
		text-rendering: auto;
		text-align: center;
		-webkit-font-smoothing: antialiased;
		-moz-osx-font-smoothing: grayscale;
		user-select: none;
		-webkit-user-select: none;
		-ms-user-select: none;
	}

	:host {
		font-family: -apple-system, BlinkMacSystemFont, "Segoe WPC", "Segoe UI", "HelveticaNeue-Light", system-ui, "Ubuntu", "Droid Sans", sans-serif;
	}

	:host-context(.mac) { font-family: -apple-system, BlinkMacSystemFont, sans-serif; }
	:host-context(.mac:lang(zh-Hans)) { font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Hiragino Sans GB", sans-serif; }
	:host-context(.mac:lang(zh-Hant)) { font-family: -apple-system, BlinkMacSystemFont, "PingFang TC", sans-serif; }
	:host-context(.mac:lang(ja)) { font-family: -apple-system, BlinkMacSystemFont, "Hiragino Kaku Gothic Pro", sans-serif; }
	:host-context(.mac:lang(ko)) { font-family: -apple-system, BlinkMacSystemFont, "Apple SD Gothic Neo", "Nanum Gothic", "AppleGothic", sans-serif; }

	:host-context(.windows) { font-family: "Segoe WPC", "Segoe UI", sans-serif; }
	:host-context(.windows:lang(zh-Hans)) { font-family: "Segoe WPC", "Segoe UI", "Microsoft YaHei", sans-serif; }
	:host-context(.windows:lang(zh-Hant)) { font-family: "Segoe WPC", "Segoe UI", "Microsoft Jhenghei", sans-serif; }
	:host-context(.windows:lang(ja)) { font-family: "Segoe WPC", "Segoe UI", "Yu Gothic UI", "Meiryo UI", sans-serif; }
	:host-context(.windows:lang(ko)) { font-family: "Segoe WPC", "Segoe UI", "Malgun Gothic", "Dotom", sans-serif; }

	:host-context(.linux) { font-family: system-ui, "Ubuntu", "Droid Sans", sans-serif; }
	:host-context(.linux:lang(zh-Hans)) { font-family: system-ui, "Ubuntu", "Droid Sans", "Source Han Sans SC", "Source Han Sans CN", "Source Han Sans", sans-serif; }
	:host-context(.linux:lang(zh-Hant)) { font-family: system-ui, "Ubuntu", "Droid Sans", "Source Han Sans TC", "Source Han Sans TW", "Source Han Sans", sans-serif; }
	:host-context(.linux:lang(ja)) { font-family: system-ui, "Ubuntu", "Droid Sans", "Source Han Sans J", "Source Han Sans JP", "Source Han Sans", sans-serif; }
	:host-context(.linux:lang(ko)) { font-family: system-ui, "Ubuntu", "Droid Sans", "Source Han Sans K", "Source Han Sans JR", "Source Han Sans", "UnDotum", "FBaekmuk Gulim", sans-serif; }
	${J(`:host-context(.modern-ui.monaco-enable-motion)`)}
`,X=class{constructor(e,t,n=t){this.modifierLabels=[null],this.modifierLabels[2]=e,this.modifierLabels[1]=t,this.modifierLabels[3]=n}toLabel(e,t,n){if(t.length===0)return null;let r=[];for(let i=0,a=t.length;i<a;i++){let a=t[i],o=n(a);if(o===null)return null;r[i]=ye(a,o,this.modifierLabels[e])}return r.join(` `)}},Z=new X({ctrlKey:`⌃`,shiftKey:`⇧`,altKey:`⌥`,metaKey:`⌘`,separator:``},{ctrlKey:y(39,`Ctrl`),shiftKey:y(40,`Shift`),altKey:y(41,`Alt`),metaKey:y(42,`Windows`),separator:`+`},{ctrlKey:y(43,`Ctrl`),shiftKey:y(44,`Shift`),altKey:y(45,`Alt`),metaKey:y(46,`Super`),separator:`+`}),ge=new X({ctrlKey:y(47,`Control`),shiftKey:y(48,`Shift`),altKey:y(49,`Option`),metaKey:y(50,`Command`),separator:`+`},{ctrlKey:y(51,`Control`),shiftKey:y(52,`Shift`),altKey:y(53,`Alt`),metaKey:y(54,`Windows`),separator:`+`},{ctrlKey:y(55,`Control`),shiftKey:y(56,`Shift`),altKey:y(57,`Alt`),metaKey:y(58,`Super`),separator:`+`}),_e=new X({ctrlKey:`Ctrl`,shiftKey:`Shift`,altKey:`Alt`,metaKey:`Cmd`,separator:`+`},{ctrlKey:`Ctrl`,shiftKey:`Shift`,altKey:`Alt`,metaKey:`Super`,separator:`+`}),ve=new X({ctrlKey:`ctrl`,shiftKey:`shift`,altKey:`alt`,metaKey:`cmd`,separator:`+`},{ctrlKey:`ctrl`,shiftKey:`shift`,altKey:`alt`,metaKey:`win`,separator:`+`},{ctrlKey:`ctrl`,shiftKey:`shift`,altKey:`alt`,metaKey:`meta`,separator:`+`});function ye(e,t,n){if(t===null)return``;let r=[];return e.ctrlKey&&r.push(n.ctrlKey),e.shiftKey&&r.push(n.shiftKey),e.altKey&&r.push(n.altKey),e.metaKey&&r.push(n.metaKey),t!==``&&r.push(t),r.join(n.separator)}var Q=E(`IEditorCancelService`),$=new i(`cancellableOperation`,!1,y(993,`Whether the editor runs a cancellable operation, e.g. like 'Peek References'`));S(Q,class{constructor(){this._tokens=new WeakMap}add(e,t){let n=this._tokens.get(e);n||(n=e.invokeWithinContext(e=>({key:$.bindTo(e.get(ne)),tokens:new s})),this._tokens.set(e,n));let r;return n.key.set(!0),r=n.tokens.push(t),()=>{r&&=(r(),n.key.set(!n.tokens.isEmpty()),void 0)}}cancel(e){let t=this._tokens.get(e);if(!t)return;let n=t.tokens.pop();n&&(n.cancel(),t.key.set(!t.tokens.isEmpty()))}},1);var be=class extends T{constructor(e,t){super(t),this.editor=e,this._unregister=e.invokeWithinContext(t=>t.get(Q).add(e,this))}dispose(){this._unregister(),super.dispose()}};te(new class extends re{constructor(){super({id:`editor.cancelOperation`,kbOpts:{weight:100,primary:9},precondition:$})}runEditorCommand(e,t){e.get(Q).cancel(t)}});var xe=class e{constructor(e,t){if(this.flags=t,this.flags&1){let t=e.getModel();this.modelVersionId=t?g(`{0}#{1}`,t.uri.toString(),t.getVersionId()):null}else this.modelVersionId=null;this.position=this.flags&4?e.getPosition():null,this.selection=this.flags&2?e.getSelection():null,this.flags&8?(this.scrollLeft=e.getScrollLeft(),this.scrollTop=e.getScrollTop()):(this.scrollLeft=-1,this.scrollTop=-1)}_equals(t){if(!(t instanceof e))return!1;let n=t;return!(this.modelVersionId!==n.modelVersionId||this.scrollLeft!==n.scrollLeft||this.scrollTop!==n.scrollTop||!this.position&&n.position||this.position&&!n.position||this.position&&n.position&&!this.position.equals(n.position)||!this.selection&&n.selection||this.selection&&!n.selection||this.selection&&n.selection&&!this.selection.equalsRange(n.selection))}validate(t){return this._equals(new e(t,this.flags))}},Se=class extends be{constructor(e,t,n,r){super(e,r),this._listener=new f,t&4&&this._listener.add(e.onDidChangeCursorPosition(e=>{n&&x.containsPosition(n,e.position)||this.cancel()})),t&2&&this._listener.add(e.onDidChangeCursorSelection(e=>{n&&x.containsRange(n,e.selection)||this.cancel()})),t&8&&this._listener.add(e.onDidScrollChange(e=>this.cancel())),t&1&&(this._listener.add(e.onDidChangeModel(e=>this.cancel())),this._listener.add(e.onDidChangeModelContent(e=>this.cancel())))}dispose(){this._listener.dispose(),super.dispose()}},Ce=class extends T{constructor(e,t){super(t),this._listener=e.onDidChangeContent(()=>this.cancel())}dispose(){this._listener.dispose(),super.dispose()}};export{le as C,j as S,F as _,_e as a,ce as b,B as c,de as d,Y as f,N as g,M as h,ge as i,W as l,R as m,Se as n,Z as o,L as p,Ce as r,ve as s,xe as t,me as u,P as v,se as x,A as y};