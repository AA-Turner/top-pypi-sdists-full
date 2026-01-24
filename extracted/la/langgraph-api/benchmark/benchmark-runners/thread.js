import { BenchmarkRunner } from './benchmark-runner.js';
import http from 'k6/http';
import { check } from 'k6';
// Uses crypto which is globally available in k6: https://grafana.com/docs/k6/latest/javascript-api/#crypto

export class Thread extends BenchmarkRunner {
    /**
     * Create a thread, search for it, get it, patch it, get it again, count the number of threads, delete the thread
     */
    static run(baseUrl, requestParams) {
        let metadata = { description: `Test benchmark thread ${crypto.randomUUID()}`};

        // Create a thread
        const createPayload = JSON.stringify({ metadata });
        const createResponse = http.post(`${baseUrl}/threads`, createPayload, requestParams);
        const threadId = createResponse.json().thread_id;

        // Search for the thread
        const searchPayload = JSON.stringify({ metadata, limit: 1 });
        const searchResponse = http.post(`${baseUrl}/threads/search`, searchPayload, requestParams);

        // Get the thread
        const getResponse = http.get(`${baseUrl}/threads/${threadId}`, requestParams);

        // Patch the thread
        metadata = { description: `Test benchmark thread ${crypto.randomUUID()}` };
        const patchPayload = JSON.stringify({ metadata });
        const patchResponse = http.patch(`${baseUrl}/threads/${threadId}`, patchPayload, requestParams);

        // Get the thread again
        const getResponse2 = http.get(`${baseUrl}/threads/${threadId}`, requestParams);

        // Count the number of threads
        const countPayload = JSON.stringify({ metadata });
        const countResponse = http.post(`${baseUrl}/threads/count`, countPayload, requestParams);

        // Delete the thread
        const deleteResponse = http.del(`${baseUrl}/threads/${threadId}`, "{}", requestParams);

        return {
            threadId,
            searchResponse,
            getResponse,
            patchResponse,
            getResponse2,
            countResponse,
            deleteResponse,
        };
    }

    static validate(result, errorMetrics, benchmarkGraphOptions) {
        let success = false;
        try {
            success = check(result, {
                'Search response contains a single thread': (r) => r.searchResponse.json().length === 1,
                'Search response contains the correct thread': (r) => r.searchResponse.json()[0].thread_id === result.threadId,
                'Get response contains the correct thread': (r) => r.getResponse.json().thread_id === result.threadId,
                'Patch response contains the correct thread': (r) => r.patchResponse.json().thread_id === result.threadId,
                'Get response 2 contains the correct thread': (r) => r.getResponse2.json().thread_id === result.threadId,
                'Get response 2 contains the new description': (r) => r.getResponse2.json().metadata.description != result.getResponse.json().metadata.description && result.getResponse2.json().metadata.description === result.patchResponse.json().metadata.description,
                'Count response contains the correct number of threads': (r) => parseInt(r.countResponse.json()) === 1,
                'Delete response is successful': (r) => r.deleteResponse.status === 204,
            });
        } catch (error) {
            console.log(`Unknown error checking response: ${error.message}`);
        }

        if (!success) {
            if (result.searchResponse.status == 502 || result.getResponse.status == 502 || result.patchResponse.status == 502 || result.getResponse2.status == 502 || result.countResponse.status == 502 || result.deleteResponse.status == 502) {
                errorMetrics.server_errors.add(1);
                console.log(`Server error: ${result.searchResponse.status}, ${result.getResponse.status}, ${result.patchResponse.status}, ${result.getResponse2.status}, ${result.countResponse.status}, ${result.deleteResponse.status}`);
            } else if (result.searchResponse.status === 408 || result.getResponse.status === 408 || result.patchResponse.status === 408 || result.getResponse2.status === 408 || result.countResponse.status === 408 || result.deleteResponse.status === 408) {
                errorMetrics.timeout_errors.add(1);
                console.log(`Timeout error: ${result.searchResponse.error}, ${result.getResponse.error}, ${result.patchResponse.error}, ${result.getResponse2.error}, ${result.countResponse.error}, ${result.deleteResponse.error}`);
            } else {
                errorMetrics.other_errors.add(1);
                console.log(`Other error: ${result.searchResponse.body}, ${result.getResponse.body}, ${result.patchResponse.body}, ${result.getResponse2.body}, ${result.countResponse.body}, ${result.deleteResponse.body}`);
            }
        }
        return success;
    }

    static toString() {
        return 'threads';
    }
}

