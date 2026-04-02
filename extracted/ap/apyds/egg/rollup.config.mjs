import terser from "@rollup/plugin-terser";
import typescript from "@rollup/plugin-typescript";
import { dts } from "rollup-plugin-dts";

export default [
    {
        input: "atsds_egg/index.mts",
        output: [
            {
                file: "dist/index.mjs",
                format: "es",
            },
        ],
        external: ["atsds"],
        plugins: [typescript(), terser()],
    },
    {
        input: "atsds_egg/index.mts",
        output: [
            {
                file: "dist/index.d.mts",
                format: "es",
            },
        ],
        plugins: [dts()],
    },
];
