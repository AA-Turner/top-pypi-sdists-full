/*
 * Delete all threads and runs from the last benchmark run for consistent tests
 * The default benchmark server has a thread TTL of one hour that should clean things up too so this doesn't run too long.
 */

// URL of your LangGraph server
const BASE_URL = process.env.BASE_URL || 'http://localhost:9123';
// LangSmith API key only needed with a custom server endpoint
const LANGSMITH_API_KEY = process.env.LANGSMITH_API_KEY;

async function clean() {
    const headers = { 'Content-Type': 'application/json' };
    if (LANGSMITH_API_KEY) {
        headers['x-api-key'] = LANGSMITH_API_KEY;
    }

    const searchUrl = `${BASE_URL}/threads/search`;
    let totalDeleted = 0;

    try {
        console.log('Starting thread cleanup...');
        
        while (true) {
            try {
                // Get the next page of threads
                console.log('Searching for threads...');
                const searchResponse = await fetch(searchUrl, {
                    method: 'POST',
                    headers,
                    body: JSON.stringify({
                        limit: 1000
                    })
                });

                if (!searchResponse.ok) {
                    throw new Error(`Search request failed: ${searchResponse.status} ${searchResponse.statusText}`);
                }

                const threads = await searchResponse.json();
                
                // If no threads found, we're done
                if (!threads || threads.length === 0) {
                    console.log('No more threads found.');
                    break;
                }

                console.log(`Found ${threads.length} threads to delete`);

                // Delete each thread
                for (const thread of threads) {
                    try {
                        const deleteUrl = `${BASE_URL}/threads/${thread.thread_id}`;
                        const deleteResponse = await fetch(deleteUrl, {
                            method: 'DELETE',
                            headers
                        });

                        if (!deleteResponse.ok) {
                            console.error(`Failed to delete thread ${thread.thread_id}: ${deleteResponse.status} ${deleteResponse.statusText}`);
                        } else {
                            totalDeleted++;
                        }
                    } catch (deleteError) {
                        console.error(`Error deleting thread ${thread.thread_id}:`, deleteError.message);
                    }
                }

                console.log(`Deleted ${threads.length} threads in this batch`);

            } catch (batchError) {
                console.error('Error in batch processing:', batchError.message);
                break;
            }
        }

        console.log(`Cleanup completed. Total threads deleted: ${totalDeleted}`);

    } catch (error) {
        console.error('Fatal error during cleanup:', error.message);
        process.exit(1);
    }
}

clean().catch(error => {
    console.error('Unhandled error:', error.message);
    process.exit(1);
});