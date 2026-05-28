import{S as r}from"./index-D2m8kTvy.js";import"./index-D-jIsajj.js";const e="passPixelShader",a=`varying vec2 vUV;uniform sampler2D textureSampler;
#define CUSTOM_FRAGMENT_DEFINITIONS
void main(void) 
{gl_FragColor=texture2D(textureSampler,vUV);}`;r.ShadersStore[e]||(r.ShadersStore[e]=a);const S={name:e,shader:a};export{S as passPixelShader};
