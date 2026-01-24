/*
 * Trigger a new revision deployment and wait for it to complete
 * This ensures the benchmark instance is running the latest code
 */

// LangSmith API endpoints and credentials
// Prod jdr-benchmark: a23f03ff-6d4d-4efd-8149-bb5a7f3b95cf
// Staging jdr-benchmark: 8ced7b1a-275f-48f3-88bf-ae08fdc4b414
const DEPLOYMENT_ID = process.env.DEPLOYMENT_ID || '8ced7b1a-275f-48f3-88bf-ae08fdc4b414'; // jdr-benchmark deployment id
const LANGSMITH_API_KEY = process.env.LANGSMITH_API_KEY;
const API_BASE = 'https://beta.api.host.langchain.com/v1';

// Deployment configuration
const REVISION_CONFIG = {
    repo_path: "langgraph.json",
    env_vars: [
        {
            name: "N_JOBS_PER_WORKER",
            value: "100",
            type: "secret"
        },
        {
            name: "FF_LOG_DROPPED_EVENTS",
            value: "true",
            type: "secret"
        }
    ],
    shareable: false
};

// Expected deployment statuses in order
const EXPECTED_STATUSES = ['CREATED', 'AWAITING_BUILD', 'BUILDING', 'AWAITING_DEPLOY', 'DEPLOYING', 'DEPLOYED', 'QUEUED'];
const FINAL_STATUS = 'DEPLOYED';
const POLL_INTERVAL = 10000; // 10 seconds
const MAX_WAIT_TIME = 30 * 60 * 1000; // 30 minutes

async function updateRevision() {
    if (!LANGSMITH_API_KEY) {
        console.error('LANGSMITH_API_KEY environment variable is required');
        process.exit(1);
    }

    const headers = {
        'Content-Type': 'application/json',
        'x-api-key': LANGSMITH_API_KEY
    };

    const createUrl = `${API_BASE}/projects/${DEPLOYMENT_ID}/revisions`;
    const pollUrl = `${API_BASE}/projects/${DEPLOYMENT_ID}/revisions?limit=1&offset=0`;

    try {
        console.log('Triggering new revision deployment...');

        // Step 1: Create new revision
        const createResponse = await fetch(createUrl, {
            method: 'POST',
            headers,
            body: JSON.stringify(REVISION_CONFIG)
        });

        if (createResponse.status === 409) {
            console.log('⚠️  A new revision is already in progress. Continuing to poll existing deployment...');
        } else if (!createResponse.ok) {
            console.log(createResponse);
            throw new Error(`Failed to create revision: ${createResponse.status} ${createResponse.statusText}`);
        } else {
            const newRevision = await createResponse.json();
            const revisionId = newRevision.resource.latest_revision.hosted_langserve_revision_id;
            console.log(`✓ New revision created: ${revisionId}`);
            console.log(`Initial status: ${newRevision.status}`);
        }

        // Step 2: Poll until deployment is complete
        console.log('\nPolling deployment status...');
        const startTime = Date.now();
        let lastStatus = null;

        while (true) {
            let pollResponse;
            try {
                pollResponse = await fetch(pollUrl, {
                    method: 'GET',
                    headers
                });

                if (!pollResponse.ok) {
                    throw new Error(`Failed to poll revisions: ${pollResponse.status} ${pollResponse.statusText}`);
                }
            } catch (pollError) {
                console.error('Error calling poll endpoint (will retry):', pollError.message);
                // Wait before next poll and continue
                await new Promise(resolve => setTimeout(resolve, POLL_INTERVAL));
                continue;
            }

            // Parse response and handle deployment logic (these errors should still be thrown)
            const revisions = await pollResponse.json();

            if (!revisions || revisions.length === 0) {
                throw new Error('No revisions found');
            }

            const latestRevision = revisions[0];
            const currentStatus = latestRevision.status;

            // Log status changes
            if (currentStatus !== lastStatus) {
                const timestamp = new Date().toISOString();
                console.log(`[${timestamp}] Status: ${currentStatus}`);

                if (latestRevision.status_message) {
                    console.log(`  Message: ${latestRevision.status_message}`);
                }

                lastStatus = currentStatus;
            }

            // Check if deployment is complete
            if (currentStatus === FINAL_STATUS) {
                console.log(`\n✓ Deployment completed successfully!`);
                console.log(`Revision ID: ${latestRevision.id}`);
                console.log(`Total time: ${Math.round((Date.now() - startTime) / 1000)}s`);
                break;
            }

            // Check for failure statuses
            if (!EXPECTED_STATUSES.includes(currentStatus)) {
                throw new Error(`Deployment failed with status: ${currentStatus}${latestRevision.status_message ? ` - ${latestRevision.status_message}` : ''}`);
            }

            // Check timeout
            if (Date.now() - startTime > MAX_WAIT_TIME) {
                throw new Error(`Deployment timeout after ${MAX_WAIT_TIME / 60000} minutes. Last status: ${currentStatus}`);
            }

            // Wait before next poll
            await new Promise(resolve => setTimeout(resolve, POLL_INTERVAL));
        }

    } catch (error) {
        console.error('Fatal error during revision update:', error.message);
        process.exit(1);
    }
}

updateRevision().catch(error => {
    console.error('Unhandled error:', error.message);
    process.exit(1);
});
