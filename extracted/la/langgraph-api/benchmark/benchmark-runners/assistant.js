import { BenchmarkRunner } from './benchmark-runner.js';
import http from 'k6/http';
import { check } from 'k6';
// Uses crypto which is globally available in k6: https://grafana.com/docs/k6/latest/javascript-api/#crypto

export class Assistant extends BenchmarkRunner {
    /**
     * Create an assistant, search for it, get it, patch it, get it again, count the number of assistants, delete the assistant
     */
    static run(baseUrl, requestParams) {
        const graph_id = 'benchmark';
        let metadata = { description: `Test benchmark assistant ${crypto.randomUUID()}`, created_by: 'benchmark' };

        // Create an assistant
        const createPayload = JSON.stringify({ graph_id, metadata });
        const createResponse = http.post(`${baseUrl}/assistants`, createPayload, requestParams);
        const assistantId = createResponse.json().assistant_id;

        // Search for the assistant
        const searchPayload = JSON.stringify({ graph_id, metadata, limit: 1 });
        const searchResponse = http.post(`${baseUrl}/assistants/search`, searchPayload, requestParams);

        // Get the assistant
        const getResponse = http.get(`${baseUrl}/assistants/${assistantId}`, requestParams);

        // Patch the assistant
        metadata = { description: `Test benchmark assistant ${crypto.randomUUID()}` };
        const patchPayload = JSON.stringify({ metadata });
        const patchResponse = http.patch(`${baseUrl}/assistants/${assistantId}`, patchPayload, requestParams);

        // Get the assistant again
        const getResponse2 = http.get(`${baseUrl}/assistants/${assistantId}`, requestParams);

        // Count the number of assistants
        const countPayload = JSON.stringify({ graph_id, metadata });
        const countResponse = http.post(`${baseUrl}/assistants/count`, countPayload, requestParams);

        // Delete the assistant
        const deleteResponse = http.del(`${baseUrl}/assistants/${assistantId}`, "{}", requestParams);

        return {
            assistantId,
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
                'Search response contains a single assistant': (r) => r.searchResponse.json().length === 1,
                'Search response contains the correct assistant': (r) => r.searchResponse.json()[0].assistant_id === result.assistantId,
                'Get response contains the correct assistant': (r) => r.getResponse.json().assistant_id === result.assistantId,
                'Patch response contains the correct assistant': (r) => r.patchResponse.json().assistant_id === result.assistantId,
                'Get response 2 contains the correct assistant': (r) => r.getResponse2.json().assistant_id === result.assistantId,
                'Get response 2 contains the new description': (r) => r.getResponse2.json().metadata.description != result.getResponse.json().metadata.description && result.getResponse2.json().metadata.description === result.patchResponse.json().metadata.description,
                'Get response 2 contains the correct created_by': (r) => r.getResponse2.json().metadata.created_by === 'benchmark',
                'Count response contains the correct number of assistants': (r) => parseInt(r.countResponse.json()) === 1,
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
        return 'assistants';
    }
}