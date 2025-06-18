import{j as r}from"./index-CeRq0YVE.js";import"./index-BegVNm_t.js";import"./svelte/svelte.js";const e="passPixelShader",a=`varying vec2 vUV;uniform sampler2D textureSampler;
#define CUSTOM_FRAGMENT_DEFINITIONS
void main(void) 
{gl_FragColor=texture2D(textureSampler,vUV);}`;r.ShadersStore[e]||(r.ShadersStore[e]=a);const s={name:e,shader:a};export{s as passPixelShader};
//# sourceMappingURL=pass.fragment-C35v02bc.js.map
