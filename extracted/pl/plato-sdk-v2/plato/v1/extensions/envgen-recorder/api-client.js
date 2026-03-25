// Real Plato API Client using bundled SDK
class PlatoApiClient {
  constructor(apiKey) {
    this.apiKey = apiKey;
    this.baseUrl = 'https://plato.so/api';
    this.sdk = null;
  }

  init() {
    if (!window.PlatoSDK) {
      throw new Error('Plato SDK not loaded');
    }
    this.sdk = new window.PlatoSDK.Plato(this.apiKey, this.baseUrl);
  }

  /**
   * Create environment and return session object
   */
  async createEnvironment(simulatorName, artifactId = null) {
    if (!this.sdk) this.init();

    // Call SDK makeEnvironment
    const env = await this.sdk.makeEnvironment(
      simulatorName,
      false,  // openPageOnStart
      false,  // recordActions
      false,  // keepalive
      undefined, // alias
      false,  // fast
      artifactId || undefined,
      "browser" // interfaceType
    );

    // Wait for ready
    await env.waitForReady(120000);

    // Get the actual public URL
    const environmentUrl = env.getPublicUrl();

    return {
      environmentId: env.id,
      environmentUrl: environmentUrl,
      environment: env
    };
  }

  /**
   * Get simulator info
   */
  async getSimulator(simulatorName) {
    const response = await fetch(`${this.baseUrl}/simulator/${simulatorName}`, {
      headers: { 'X-API-Key': this.apiKey }
    });

    if (!response.ok) {
      throw new Error(`Simulator not found: ${response.statusText}`);
    }

    return await response.json();
  }

  /**
   * Submit review using the proper review + status API endpoints
   */
  async submitReview(simulatorName, review) {
    // Get simulator info
    const simulator = await this.getSimulator(simulatorName);
    const simulatorId = simulator.id;
    const currentConfig = simulator.config || {};
    const currentStatus = currentConfig.status || 'not_started';

    if (currentStatus != 'data_review_requested') {
      throw new Error(
        `Cannot submit review: Simulator is in wrong state "${currentStatus}". ` +
        `Must be in a data review state: data_review_requested`
      );
    }

    let newStatus;

    if (review.outcome === 'pass') {
      newStatus = 'ready';
    } else if (review.outcome === 'reject') {
      newStatus = 'data_in_progress';
    } else {
      return { success: true, message: 'Skipped' };
    }

    // Extract video and events paths from recordings array (should only have one recording)
    const recording = review.recordings && review.recordings.length > 0 ? review.recordings[0] : null;
    if (!recording || !recording.video_s3_path || !recording.events_s3_path) {
      throw new Error('Recording paths are required for review submission');
    }

    // 1. Submit review first (so we don't leave status changed without a review record)
    const reviewBody = {
      review_type: 'data',
      outcome: review.outcome,
      artifact_id: review.artifactId,
      video_s3_path: recording.video_s3_path,
      events_s3_path: recording.events_s3_path,
      sim_comments: review.comments ? [{ comment: review.comments }] : [],
    };

    const reviewResponse = await fetch(`${this.baseUrl}/v1/simulator/${simulatorId}/reviews`, {
      method: 'POST',
      headers: {
        'X-API-Key': this.apiKey,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(reviewBody)
    });

    if (!reviewResponse.ok) {
      const errorText = await reviewResponse.text().catch(() => reviewResponse.statusText);
      throw new Error(`Failed to submit review: ${errorText}`);
    }

    // 2. Update status after review is recorded
    const statusResponse = await fetch(`${this.baseUrl}/v1/simulator/${simulatorId}/status`, {
      method: 'POST',
      headers: {
        'X-API-Key': this.apiKey,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ status: newStatus })
    });

    if (!statusResponse.ok) {
      const errorText = await statusResponse.text().catch(() => statusResponse.statusText);
      throw new Error(`Failed to update status: ${errorText}`);
    }

    return { success: true, newStatus };
  }

  /**
   * Tag artifact as prod-latest
   */
  async tagArtifact(simulatorName, artifactId) {
    const response = await fetch(`${this.baseUrl}/simulator/update-tag`, {
      method: 'POST',
      headers: {
        'X-API-Key': this.apiKey,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        simulator_name: simulatorName,
        artifact_id: artifactId,
        tag_name: 'prod-latest',
        dataset: 'base'
      })
    });

    if (!response.ok) {
      throw new Error(`Failed to tag artifact: ${response.statusText}`);
    }

    return await response.json();
  }
}

window.PlatoApiClient = PlatoApiClient;
