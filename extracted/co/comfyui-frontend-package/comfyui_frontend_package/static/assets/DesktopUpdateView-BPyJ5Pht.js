var __defProp = Object.defineProperty;
var __name = (target, value) => __defProp(target, "name", { value, configurable: true });
import { defineComponent, ref, onUnmounted, openBlock, createBlock, withCtx, createBaseVNode, toDisplayString, unref, createVNode } from "./vendor-vue-DbSbNqzX.js";
import { script$29 as script, script$2 as script$1, script$53 as script$2 } from "./vendor-primevue-CGMNnJS3.js";
import { _sfc_main as _sfc_main$1 } from "./TerminalOutputDrawer-D_4Y-clR.js";
import { t, electronAPI, _export_sfc } from "./index-Bm0FjBLW.js";
import { _sfc_main as _sfc_main$2 } from "./BaseViewTemplate-Cc7ATWEZ.js";
import "./vendor-vue-i18n-IV1BVZMP.js";
const _hoisted_1 = { class: "h-screen w-screen grid items-center justify-around overflow-y-auto" };
const _hoisted_2 = { class: "relative m-8 text-center" };
const _hoisted_3 = { class: "download-bg pi-download text-4xl font-bold" };
const _hoisted_4 = { class: "m-8" };
const _sfc_main = /* @__PURE__ */ defineComponent({
  __name: "DesktopUpdateView",
  setup(__props) {
    const electron = electronAPI();
    const terminalVisible = ref(false);
    const toggleConsoleDrawer = /* @__PURE__ */ __name(() => {
      terminalVisible.value = !terminalVisible.value;
    }, "toggleConsoleDrawer");
    onUnmounted(() => electron.Validation.dispose());
    return (_ctx, _cache) => {
      return openBlock(), createBlock(_sfc_main$2, { dark: "" }, {
        default: withCtx(() => [
          createBaseVNode("div", _hoisted_1, [
            createBaseVNode("div", _hoisted_2, [
              createBaseVNode("h1", _hoisted_3, toDisplayString(unref(t)("desktopUpdate.title")), 1),
              createBaseVNode("div", _hoisted_4, [
                createBaseVNode("span", null, toDisplayString(unref(t)("desktopUpdate.description")), 1)
              ]),
              createVNode(unref(script), { class: "m-8 w-48 h-48" }),
              createVNode(unref(script$1), {
                style: { "transform": "translateX(-50%)" },
                class: "fixed bottom-0 left-1/2 my-8",
                label: unref(t)("maintenance.consoleLogs"),
                icon: "pi pi-desktop",
                "icon-pos": "left",
                severity: "secondary",
                onClick: toggleConsoleDrawer
              }, null, 8, ["label"]),
              createVNode(_sfc_main$1, {
                modelValue: terminalVisible.value,
                "onUpdate:modelValue": _cache[0] || (_cache[0] = ($event) => terminalVisible.value = $event),
                header: unref(t)("g.terminal"),
                "default-message": unref(t)("desktopUpdate.terminalDefaultMessage")
              }, null, 8, ["modelValue", "header", "default-message"])
            ])
          ]),
          createVNode(unref(script$2))
        ]),
        _: 1
      });
    };
  }
});
const DesktopUpdateView = /* @__PURE__ */ _export_sfc(_sfc_main, [["__scopeId", "data-v-8d77828d"]]);
export {
  DesktopUpdateView as default
};
//# sourceMappingURL=DesktopUpdateView-BPyJ5Pht.js.map
