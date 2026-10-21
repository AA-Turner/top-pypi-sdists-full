// Shim for extensions/core/load3d/SceneModelManager.ts
console.warn('[ComfyUI Notice] "extensions/core/load3d/SceneModelManager.js" is an internal module, not part of the public API. Future updates may break this import.');
export const disposeObject3D = window.comfyAPI.SceneModelManager.disposeObject3D;
export const cloneObject3DResources = window.comfyAPI.SceneModelManager.cloneObject3DResources;
export const SceneModelManager = window.comfyAPI.SceneModelManager.SceneModelManager;
