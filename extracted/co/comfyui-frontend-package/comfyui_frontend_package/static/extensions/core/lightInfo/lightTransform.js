// Shim for extensions/core/lightInfo/lightTransform.ts
console.warn('[ComfyUI Notice] "extensions/core/lightInfo/lightTransform.js" is an internal module, not part of the public API. Future updates may break this import.');
export const orbitPosition = window.comfyAPI.lightTransform.orbitPosition;
export const orbitAnglesFor = window.comfyAPI.lightTransform.orbitAnglesFor;
export const orbitHandleState = window.comfyAPI.lightTransform.orbitHandleState;
