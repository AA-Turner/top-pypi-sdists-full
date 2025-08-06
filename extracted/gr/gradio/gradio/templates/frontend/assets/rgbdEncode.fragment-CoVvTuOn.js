import{j as r}from"./index-CUnH0zOt.js";import"./helperFunctions-za1q-UWN.js";import"./index-CE5Dq9Ft.js";import"./svelte/svelte.js";const e="rgbdEncodePixelShader",t=`varying vUV: vec2f;var textureSamplerSampler: sampler;var textureSampler: texture_2d<f32>;
#include<helperFunctions>
#define CUSTOM_FRAGMENT_DEFINITIONS
@fragment
fn main(input: FragmentInputs)->FragmentOutputs {fragmentOutputs.color=toRGBD(textureSample(textureSampler,textureSamplerSampler,input.vUV).rgb);}`;r.ShadersStoreWGSL[e]||(r.ShadersStoreWGSL[e]=t);const p={name:e,shader:t};export{p as rgbdEncodePixelShaderWGSL};
//# sourceMappingURL=rgbdEncode.fragment-CoVvTuOn.js.map
