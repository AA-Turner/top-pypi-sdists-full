/*
 * Trigger a new revision deployment and wait for it to complete.
 * Uses Host v2 deployment APIs.
 */

import { createRevision, requireApiKey } from './host-v2.js';

const DEPLOYMENT_ID =
  process.env.DEPLOYMENT_ID || '03b7336a-73dd-4ee5-8b5e-da19c48a6cdc';

async function updateRevision() {
  const apiKey = requireApiKey();
  await createRevision(DEPLOYMENT_ID, apiKey);
  console.log('\n✓ Deployment completed successfully!');
}

updateRevision().catch((error) => {
  console.error('Fatal error during revision update:', error.message);
  process.exit(1);
});
