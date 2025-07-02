import{s,k as i,r as m,j as e}from"./index.CW9dTClp.js";import{P as c,R as l}from"./RenderInPortalIfExists.D95lvcfx.js";const p=""+new URL("../media/flake-0.DgWaVvm5.png",import.meta.url).href,d=""+new URL("../media/flake-1.B2r5AHMK.png",import.meta.url).href,f=""+new URL("../media/flake-2.BnWSExPC.png",import.meta.url).href,o=150,g=150,E=10,S=90,u=4e3,n=(t,a=0)=>Math.random()*(t-a)+a,x=()=>i(`from{transform:translateY(0)
      rotateX(`,n(360),`deg)
      rotateY(`,n(360),`deg)
      rotateZ(`,n(360),"deg);}to{transform:translateY(calc(100vh + ",o,`px))
      rotateX(0)
      rotateY(0)
      rotateZ(0);}`),_=s("img",{target:"es7rdur0"})(({theme:t})=>({position:"fixed",top:"-150px",marginLeft:`${-150/2}px`,zIndex:t.zIndices.balloons,left:`${n(S,E)}vw`,animationDelay:`${n(u)}ms`,height:`${o}px`,width:`${g}px`,pointerEvents:"none",animationDuration:"3000ms",animationName:x(),animationTimingFunction:"ease-in",animationDirection:"normal",animationIterationCount:1,opacity:1})),w=100,r=[p,d,f],I=r.length,M=({particleType:t})=>e(_,{src:r[t]}),h=function({scriptRunId:a}){return e(l,{children:e(c,{className:"stSnow","data-testid":"stSnow",scriptRunId:a,numParticleTypes:I,numParticles:w,ParticleComponent:M})})},P=m.memo(h);export{w as NUM_FLAKES,P as default};
