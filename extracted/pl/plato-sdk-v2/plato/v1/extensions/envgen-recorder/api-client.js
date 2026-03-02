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
   * Submit review
   */
  async submitReview(simulatorName, review) {
    // Get simulator info
    const simulator = await this.getSimulator(simulatorName);
    const simulatorId = simulator.id;
    const currentConfig = simulator.config || {};
    const existingReviews = currentConfig.reviews || [];
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

    // Build review object matching SimReview model
    const reviewObject = {
      review_type: 'data', // Environment recording reviews are always 'env'
      outcome: review.outcome,
      artifact_id: review.artifactId,
      video_s3_path: recording.video_s3_path,
      events_s3_path: recording.events_s3_path,
      comments: review.comments || null,
      timestamp_iso: new Date().toISOString()
    };

    // Submit
    const response = await fetch(`${this.baseUrl}/env/simulators/${simulatorId}`, {
      method: 'PUT',
      headers: {
        'X-API-Key': this.apiKey,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        config: {
          ...currentConfig,
          status: newStatus,
          reviews: [...existingReviews, reviewObject]
        }
      })
    });

    if (!response.ok) {
      const errorText = await response.text().catch(() => response.statusText);
      throw new Error(`Failed to submit review: ${errorText}`);
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
