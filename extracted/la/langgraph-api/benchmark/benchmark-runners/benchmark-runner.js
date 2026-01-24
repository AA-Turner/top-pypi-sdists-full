/**
 * Abstract class for running a benchmark type.
 */
export class BenchmarkRunner {
    /**
     * Run the benchmark type.
     * @param {string} baseUrl - The base URL of the Agent Server.
     * @param {any} requestParams - The parameters to use for the request. Includes headers and other config like timeout.
     * @param {any} benchmarkGraphOptions - The options for the benchmark graph.
     * @returns {any} - The result of the benchmark type. This format will vary by benchmark type.
     */
    static run(baseUrl, requestParams, benchmarkGraphOptions) {
        throw new Error('Not implemented');
    }

    /**
     * Convert the benchmark name to a string.
     * @returns {string} - A string representation of the benchmark name.
     */
    static toString() {
        throw new Error('Not implemented');
    }

    /**
     * Validate the result of the benchmark run.
     * @param {any} result - The result of the benchmark run. This format will vary by benchmark type.
     * @param {any} errorMetrics - A dictionary of error metrics that can be used to more granularly track errors.
     * @param {any} benchmarkGraphOptions - The options for the benchmark graph.
     * @returns {boolean} - True if the benchmark run was successful, false otherwise.
     */
    static validate(result, errorMetrics, benchmarkGraphOptions) {
        throw new Error('Not implemented');
    }
}