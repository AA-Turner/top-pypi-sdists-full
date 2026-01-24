import nodeResolve from "@rollup/plugin-node-resolve";
import terser from "@rollup/plugin-terser";
import copy from "rollup-plugin-copy";

export default [
    {
        input: "atsds_bnf/index.mjs",
        output: {
            file: "dist/index.mjs",
            format: "es",
        },
        plugins: [
            nodeResolve({
                browser: true,
            }),
            terser(),
            copy({
                targets: [{ src: "atsds_bnf/index.d.mts", dest: "dist" }],
            }),
        ],
    },
];
