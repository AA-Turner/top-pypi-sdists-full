import { BenchmarkRunner } from './benchmark-runner.js';
import { check } from 'k6';
import http from 'k6/http';

function parseSSE(text) {
    const events = [];
    const lines = text.split('\r\n');
    let currentEvent = { event: '', data: '' };
    
    for (const line of lines) {
        if (line.startsWith('event:')) {
            currentEvent.event = line.substring(6).trim();
        } else if (line.startsWith('data:')) {
            const dataContent = line.substring(5).trim();
            currentEvent.data = dataContent;
        } else if (line === '') {
            // Empty line marks end of event
            if (currentEvent.data) {
                try {
                    events.push({
                        event: currentEvent.event,
                        data: JSON.parse(currentEvent.data)
                    });
                } catch (e) {
                    // Some events might not be JSON
                    events.push(currentEvent);
                }
            }
            currentEvent = { event: '', data: '' };
        }
    }
    
    return events;
}

export class StreamWrite extends BenchmarkRunner {
    static run(baseUrl, requestParams, benchmarkGraphOptions) {
        let url = `${baseUrl}/runs/stream`;

        // Create a payload with the LangGraph agent configuration
        const payload = JSON.stringify({
            assistant_id: benchmarkGraphOptions.graph_id,
            input: benchmarkGraphOptions.input,
            config: {
                recursion_limit: benchmarkGraphOptions.input.expand + 2,
            },
        });

        // If the request is stateful, create a thread first and use it in the url
        if (benchmarkGraphOptions.stateful) {
            const thread = http.post(`${baseUrl}/threads`, "{}", requestParams);
            const threadId = thread.json().thread_id;
            url = `${baseUrl}/threads/${threadId}/runs/stream`;
        }

        const response = http.post(url, payload, requestParams);
        const events = parseSSE(response.body);
        return { events, response };
    }

    static validate(result, errorMetrics, benchmarkGraphOptions) {
        const expected_messages = benchmarkGraphOptions.input.mode === 'single' ? 1 : benchmarkGraphOptions.input.expand + 1;
        const expected_events = expected_messages + 2; // +2 for the metadata and initial values event
        let success = false;
        try {
            success = check(result, {
                'Run completed successfully': (r) => r.response.status === 200,
                'Response contains expected number of events': (r) => r.events.length === expected_events,
                'Response contains metadata event': (r) => r.events[0].event === 'metadata',
                'Response contains expected number of messages': (r) => r.events[expected_events - 1].data.messages.length === expected_messages,
            });
        } catch (error) {
            console.log(`Unknown error checking result: ${error.message}`);
        }

        if (!success) {
            // Classify error based on status code or response
            if (result.response.status >= 500) {
                errorMetrics.server_errors.add(1);
                console.log(`Server error: ${result.response.status}`);
            } else if (result.response.status === 408 || result.response.error?.includes('timeout')) {
                errorMetrics.timeout_errors.add(1);
                console.log(`Timeout error: ${result.response.error}`);
            } else if (result.response.status === 200 && result.events[expected_events - 1].data.messages.length !== expected_messages) {
                errorMetrics.missing_message_errors.add(1);
                console.log(`Missing message error: Status ${result.response.status}, ${JSON.stringify(result.response.body)}, ${result.response.headers?.['Content-Location']}`);
            } else {
                errorMetrics.other_errors.add(1);
                console.log(`Other error: Status ${result.response.status}, ${JSON.stringify(result.response.body)}, ${result.events}`);
            }
        }
        return success;
    }

    static toString() {
        return 'stream_write';
    }
}