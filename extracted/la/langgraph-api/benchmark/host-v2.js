/**
 * LangSmith Host v2 API helpers for benchmark tooling.
 */

export const STAGING_TENANT_ID = '8f32dc68-61a1-439c-81d3-33511ef55527';
export const HOST_V2_BASE =
  process.env.HOST_API_V2_BASE || 'https://beta.api.host.langchain.com/v2';

export const REVISION_CONFIG = {
  source_revision_config: {
    langgraph_config_path: 'langgraph.json',
  },
};

export const EXPECTED_REVISION_STATUSES = new Set([
  'CREATING',
  'QUEUED',
  'AWAITING_BUILD',
  'BUILDING',
  'AWAITING_DEPLOY',
  'DEPLOYING',
  'DEPLOYED',
]);

export const FINAL_REVISION_STATUS = 'DEPLOYED';
// Overridable so tests can drive the poll loops without real-time waits.
export const POLL_INTERVAL_MS = Number(
  process.env.HOST_POLL_INTERVAL_MS || 10_000,
);
export const MAX_WAIT_MS = 30 * 60 * 1000;
// Consecutive successful /ok responses required before a deployment counts as
// ready. At POLL_INTERVAL_MS this is a 60s sustained-health window.
export const HEALTH_CONSECUTIVE_OK = Number(
  process.env.HOST_HEALTH_CONSECUTIVE_OK || 6,
);

export function requireApiKey() {
  const apiKey = process.env.LANGSMITH_API_KEY;
  if (!apiKey) {
    throw new Error('LANGSMITH_API_KEY environment variable is required');
  }
  return apiKey;
}

export function hostHeaders(apiKey) {
  return {
    'Content-Type': 'application/json',
    'x-api-key': apiKey,
    'X-Tenant-Id': STAGING_TENANT_ID,
    'X-Organization-Id': STAGING_TENANT_ID,
  };
}

async function readErrorDetail(response) {
  try {
    return await response.text();
  } catch {
    return response.statusText;
  }
}

export async function hostRequest(method, path, apiKey, body) {
  const response = await fetch(`${HOST_V2_BASE}${path}`, {
    method,
    headers: hostHeaders(apiKey),
    body: body === undefined ? undefined : JSON.stringify(body),
  });
  if (!response.ok) {
    const detail = await readErrorDetail(response);
    throw new Error(`${method} ${path} failed: ${response.status} ${detail}`);
  }
  if (response.status === 204) {
    return null;
  }
  return response.json();
}

export async function listLatestRevision(deploymentId, apiKey) {
  const result = await hostRequest(
    'GET',
    `/deployments/${deploymentId}/revisions?limit=1&offset=0`,
    apiKey,
  );
  const revisions = result?.resources ?? [];
  if (revisions.length === 0) {
    throw new Error(`No revisions found for deployment ${deploymentId}`);
  }
  return revisions[0];
}

/**
 * Poll until a revision reaches DEPLOYED.
 *
 * Pass `revisionId` whenever a mutation just returned one. Without it the first
 * poll can observe the *previous* revision, which is already DEPLOYED, and
 * return immediately - so the benchmark would run against the old
 * configuration while the new one was still rolling, and file the result under
 * the new tier's name. Both mutating endpoints hand the id back, so this is
 * normally known rather than discovered.
 */
export async function pollRevisionDeployed(
  deploymentId,
  apiKey,
  { revisionId = null } = {},
) {
  const startTime = Date.now();
  let lastStatus = null;

  while (true) {
    let revision;
    try {
      revision = await listLatestRevision(deploymentId, apiKey);
    } catch (error) {
      if (Date.now() - startTime > MAX_WAIT_MS) {
        throw new Error(
          `Deployment timeout after ${MAX_WAIT_MS / 60000} minutes. Last error: ${error.message}`,
        );
      }
      console.error('Error polling revision (will retry):', error.message);
      await sleep(POLL_INTERVAL_MS);
      continue;
    }

    if (revisionId !== null && revision.id !== revisionId) {
      // Ours has not surfaced yet; the one being reported is the previous
      // revision, which is already DEPLOYED.
      if (Date.now() - startTime > MAX_WAIT_MS) {
        throw new Error(
          `Revision ${revisionId} never became the latest revision after ${MAX_WAIT_MS / 60000} minutes`,
        );
      }
      await sleep(POLL_INTERVAL_MS);
      continue;
    }

    const currentStatus = revision.status;
    if (currentStatus !== lastStatus) {
      console.log(`[${new Date().toISOString()}] revision status: ${currentStatus}`);
      lastStatus = currentStatus;
    }

    if (currentStatus === FINAL_REVISION_STATUS) {
      console.log('  revision deployed');
      return revision;
    }

    if (!EXPECTED_REVISION_STATUSES.has(currentStatus)) {
      throw new Error(`Deployment failed with status: ${currentStatus}`);
    }

    if (Date.now() - startTime > MAX_WAIT_MS) {
      throw new Error(
        `Deployment timeout after ${MAX_WAIT_MS / 60000} minutes. Last status: ${currentStatus}`,
      );
    }

    await sleep(POLL_INTERVAL_MS);
  }
}

export async function createRevision(deploymentId, apiKey) {
  console.log(`Triggering new revision for deployment ${deploymentId}...`);
  let revisionId = null;
  const response = await fetch(`${HOST_V2_BASE}/deployments/${deploymentId}/revisions`, {
    method: 'POST',
    headers: hostHeaders(apiKey),
    body: JSON.stringify(REVISION_CONFIG),
  });
  if (response.status === 409) {
    console.log('  revision already in progress; polling existing deployment...');
  } else if (!response.ok) {
    const detail = await readErrorDetail(response);
    throw new Error(
      `POST /deployments/${deploymentId}/revisions failed: ${response.status} ${detail}`,
    );
  } else {
    const revision = await response.json();
    revisionId = revision.id ?? null;
    console.log(`  revision created: ${revision.id} (${revision.status})`);
  }
  // 409 means one was already in progress and we were given no id, so fall back
  // to waiting on whatever the latest revision turns out to be.
  return pollRevisionDeployed(deploymentId, apiKey, { revisionId });
}

/**
 * Wait until the deployment answers /ok successfully `consecutive` times in a
 * row, resetting the streak on any failure.
 *
 * A single 200 is not readiness. After a tier change the control plane reports
 * DEPLOYED while pods are still rolling and the database is still resizing;
 * /ok?check_db=1 passes on one connection and has been observed answering
 * 248ms after DEPLOYED, with the deployment then failing under load with
 * "cannot create run: failed to begin transaction". Requiring a sustained
 * streak turns that into a wait instead of a corrupted measurement.
 */
export async function pollDeploymentHealthy(
  baseUrl,
  apiKey,
  { checkDb = true, consecutive = HEALTH_CONSECUTIVE_OK } = {},
) {
  const url = new URL('ok', baseUrl.endsWith('/') ? baseUrl : `${baseUrl}/`);
  if (checkDb) {
    url.searchParams.set('check_db', '1');
  }

  const startTime = Date.now();
  let lastError = 'unknown';
  let streak = 0;

  console.log(
    `Polling deployment health at ${url} (need ${consecutive} consecutive)...`,
  );

  while (true) {
    try {
      const headers = { Accept: 'application/json' };
      if (apiKey) {
        headers['x-api-key'] = apiKey;
      }
      const response = await fetch(url, { headers });
      if (response.ok) {
        const body = await response.json();
        if (body?.ok === true) {
          streak += 1;
          if (streak >= consecutive) {
            console.log(`  deployment health check passed (${streak}x)`);
            return;
          }
          await sleep(POLL_INTERVAL_MS);
          continue;
        }
        lastError = `unexpected body: ${JSON.stringify(body)}`;
      } else {
        const detail = await readErrorDetail(response);
        lastError = `HTTP ${response.status} ${detail}`;
      }
    } catch (error) {
      lastError = error.message;
    }

    if (streak > 0) {
      console.log(`  health streak broken at ${streak} (${lastError})`);
      streak = 0;
    }

    if (Date.now() - startTime > MAX_WAIT_MS) {
      throw new Error(
        `Health check timeout after ${MAX_WAIT_MS / 60000} minutes. Last error: ${lastError}`,
      );
    }

    console.log(`  health check pending (${lastError})`);
    await sleep(POLL_INTERVAL_MS);
  }
}

export async function setResourceTiers(
  deploymentId,
  computeTier,
  databaseTier,
  apiKey,
  baseUrl,
) {
  /** @type {{ compute_tier?: string, database_tier?: string }} */
  const body = {};
  if (computeTier != null) {
    body.compute_tier = computeTier;
  }
  if (databaseTier != null) {
    body.database_tier = databaseTier;
  }
  if (Object.keys(body).length === 0) {
    throw new Error('At least one of computeTier or databaseTier is required');
  }
  console.log(
    `Setting resource tiers for deployment ${deploymentId}: ${JSON.stringify(body)}`,
  );
  // The response is the updated Deployment, and it already carries the id of
  // the revision the resize just created.
  const deployment = await hostRequest(
    'PATCH',
    `/deployments/${deploymentId}/resource-tiers`,
    apiKey,
    body,
  );
  await pollRevisionDeployed(deploymentId, apiKey, {
    revisionId: deployment?.latest_revision_id ?? null,
  });
  if (baseUrl) {
    await pollDeploymentHealthy(baseUrl, apiKey, { checkDb: true });
  }
}

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}
