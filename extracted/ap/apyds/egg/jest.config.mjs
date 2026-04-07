export default {
    testMatch: ["<rootDir>/tests/test_*.mjs"],
    collectCoverage: true,
    extensionsToTreatAsEsm: [".mts"],
    transform: {
        "^.+\\.m?tsx?$": [
            "@swc/jest",
            {
                jsc: {
                    parser: {
                        syntax: "typescript",
                    },
                    target: "es2022",
                },
                module: {
                    type: "es6",
                },
            },
        ],
    },
};
