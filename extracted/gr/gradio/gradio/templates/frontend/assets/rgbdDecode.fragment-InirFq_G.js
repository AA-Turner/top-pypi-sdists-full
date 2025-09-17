import{j as r}from"./index-Dv-qqpVD.js";import"./helperFunctions-CebNiqpC.js";import"./index-BxT30XTY.js";import"./svelte/svelte.js";const e="rgbdDecodePixelShader",t=`varying vUV: vec2f;var textureSamplerSampler: sampler;var textureSampler: texture_2d<f32>;
#include<helperFunctions>
#define CUSTOM_FRAGMENT_DEFINITIONS
@fragment
fn main(input: FragmentInputs)->FragmentOutputs {fragmentOutputs.color=vec4f(fromRGBD(textureSample(textureSampler,textureSamplerSampler,input.vUV)),1.0);}`;r.ShadersStoreWGSL[e]||(r.ShadersStoreWGSL[e]=t);const n={name:e,shader:t};export{n as rgbdDecodePixelShaderWGSL};
//# sourceMappingURL=rgbdDecode.fragment-InirFq_G.js.map
