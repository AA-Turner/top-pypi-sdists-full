import { BenchmarkRunner } from './benchmark-runner.js';
import http from 'k6/http';
import { check } from 'k6';

export class WaitWrite extends BenchmarkRunner {
    static run(baseUrl, requestParams, benchmarkGraphOptions) {
        let url = `${baseUrl}/runs/wait`;

        // Create a payload with the LangGraph agent configuration
        // recursion_limit needs to account for both expand (fan-out) and steps (loop iterations)
        const expand = benchmarkGraphOptions.input.expand || 1;
        const steps = benchmarkGraphOptions.input.steps || 1;
        const payload = JSON.stringify({
            assistant_id: benchmarkGraphOptions.graph_id,
            input: benchmarkGraphOptions.input,
            config: {
                recursion_limit: Math.max(expand, steps) + 2,
            },
        });

        // If the request is stateful, create a thread first and use it in the url
        if (benchmarkGraphOptions.stateful) {
            const thread = http.post(`${baseUrl}/threads`, "{}", requestParams);
            const threadId = thread.json().thread_id;
            url = `${baseUrl}/threads/${threadId}/runs/wait`;
        }

        // Make a single request to the wait endpoint
        const result = http.post(url, payload, requestParams);

        return result;
    }

    static validate(result, errorMetrics, benchmarkGraphOptions) {
        const expected_length = benchmarkGraphOptions.input.mode === 'single' ? 1 : benchmarkGraphOptions.input.expand + 1;
        let success = false;

        try {
            let json = null;
            if (result.status === 200) {
                try {
                    json = result.json();
                } catch (e) {
                    // JSON parse failed
                    console.error('JSON response parsing failed')
                }
            }

            const checks = {
                'Run completed successfully': () => {
                    if (result.status !== 200) {
                        console.log(`WaitWrite VU ${__VU}: FAIL - HTTP status ${result.status}`);
                        return false;
                    }
                    if (!json) {
                        console.log(`WaitWrite VU ${__VU}: FAIL - JSON parse failed or empty response`);
                        return false;
                    }
                    if (json.__error__ !== undefined) {
                        console.log(`WaitWrite VU ${__VU}: FAIL - API error: ${JSON.stringify(json.__error__)}`);
                        return false;
                    }
                    // always check for expand field
                    if (json.expand === undefined) {
                        console.log(`WaitWrite VU ${__VU}: FAIL - No expand field. Response keys: [${Object.keys(json).join(', ')}]`);
                        return false;
                    }
                    // Only add message validation if the response actually contains a messages field
                    if (json.messages !== undefined && json.messages.length !== expected_length) {
                        console.log(`WaitWrite VU ${__VU}: FAIL - Wrong message count: got ${json.messages.length}, expected ${expected_length}`);
                        return false;
                    }
                    return true;
                },
            };

            success = check(result, checks);
        } catch (error) {
            console.log(`WaitWrite VU ${__VU}: Unknown error checking result: ${error.message}`);
        }

        if (!success) {
            try {
                const hasApiError = json && json.__error__;

                if (result.status >= 500) {
                    errorMetrics.server_errors.add(1);
                } else if (result.status === 408 || result.error?.includes('timeout')) {
                    errorMetrics.timeout_errors.add(1);
                } else if (hasApiError) {
                    errorMetrics.api_errors.add(1);
                } else if (result.status === 200 && json && (json.messages === undefined || json.messages?.length !== expected_length)) {
                    errorMetrics.missing_message_errors.add(1);
                } else {
                    errorMetrics.other_errors.add(1);
                }
            } catch (classifyError) {
                errorMetrics.other_errors.add(1);
            }
        }
        return success;
    }

    static toString() {
        return 'wait_write';
    }
}
