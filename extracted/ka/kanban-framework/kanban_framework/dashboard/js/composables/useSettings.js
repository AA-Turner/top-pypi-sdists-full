import { ref, readonly } from 'vue';
import { api } from '../utils/api.js';

export function useSettings() {
  const config = ref(null);
  const workflow = ref(null);
  const knowledgeHealth = ref(null);
  const loading = ref(false);
  const saveStatus = ref('idle');
  const error = ref(null);

  async function loadConfig() {
    try {
      loading.value = true;
      config.value = await api.getConfig();
    } catch (e) {
      error.value = e.message;
    } finally {
      loading.value = false;
    }
  }

  async function loadWorkflow() {
    try {
      loading.value = true;
      workflow.value = await api.getWorkflow();
    } catch (e) {
      error.value = e.message;
    } finally {
      loading.value = false;
    }
  }

  async function saveConfig(data) {
    try {
      saveStatus.value = 'saving';
      const result = await api.saveConfig(data);
      config.value = result.data;
      saveStatus.value = 'saved';
      setTimeout(() => { if (saveStatus.value === 'saved') saveStatus.value = 'idle'; }, 2000);
      return result;
    } catch (e) {
      saveStatus.value = 'error';
      error.value = e.message;
      throw e;
    }
  }

  async function saveWorkflow(data) {
    try {
      saveStatus.value = 'saving';
      const result = await api.saveWorkflow(data);
      workflow.value = result.data;
      saveStatus.value = 'saved';
      setTimeout(() => { if (saveStatus.value === 'saved') saveStatus.value = 'idle'; }, 2000);
      return result;
    } catch (e) {
      saveStatus.value = 'error';
      error.value = e.message;
      throw e;
    }
  }

  async function loadKnowledgeHealth() {
    try {
      const result = await api.getKnowledgeHealth();
      knowledgeHealth.value = result;
    } catch (e) {
      knowledgeHealth.value = { success: false, error: e.message };
    }
  }

  return {
    config: readonly(config),
    workflow: readonly(workflow),
    knowledgeHealth: readonly(knowledgeHealth),
    loading: readonly(loading),
    saveStatus: readonly(saveStatus),
    error: readonly(error),
    loadConfig, loadWorkflow, saveConfig, saveWorkflow, loadKnowledgeHealth,
  };
}
