import terser from "@rollup/plugin-terser";
import typescript from "@rollup/plugin-typescript";
import nodeResolve from "@rollup/plugin-node-resolve";
import { dts } from "rollup-plugin-dts";

export default [
    {
        input: {
            index: "atsds/index.mts",
            example: "examples/main.mjs",
        },
        output: {
            dir: "dist",
            format: "es",
            entryFileNames: "[name].mjs",
        },
        plugins: [terser(), typescript(), nodeResolve()],
    },
    {
        input: {
            index: "atsds/index.mts",
        },
        output: {
            dir: "dist",
            format: "es",
            entryFileNames: "[name].d.mts",
        },
        plugins: [dts()],
    },
];
