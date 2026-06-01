import { ref, onMounted } from 'vue';
import { useSettings } from '../composables/useSettings.js';
import { ConfigPanel } from './ConfigPanel.js';
import { WorkflowPanel } from './WorkflowPanel.js';
import { KnowledgePanel } from './KnowledgePanel.js';

const SUB_TABS = [
  { id: 'config', label: '项目配置', icon: '⚙' },
  { id: 'workflow', label: '工作流配置', icon: '🔄' },
  { id: 'knowledge', label: '知识库管理', icon: '📚' },
];

export const SettingsPanel = {
  components: { ConfigPanel, WorkflowPanel, KnowledgePanel },
  setup() {
    const activeTab = ref('config');
    const {
      config, workflow, knowledgeHealth,
      saveStatus, error,
      loadConfig, loadWorkflow, saveConfig, saveWorkflow, loadKnowledgeHealth,
    } = useSettings();

    onMounted(async () => {
      await Promise.all([loadConfig(), loadWorkflow()]);
    });

    function handleSaveConfig(data) {
      return saveConfig(data);
    }

    function handleSaveWorkflow(data) {
      return saveWorkflow(data);
    }

    function handleRefreshHealth() {
      loadKnowledgeHealth();
    }

    return {
      SUB_TABS, activeTab,
      config, workflow, knowledgeHealth,
      saveStatus, error,
      handleSaveConfig, handleSaveWorkflow, handleRefreshHealth,
    };
  },
  template: `
    <div class="settings-panel">
      <div class="settings-tabs">
        <button v-for="tab in SUB_TABS" :key="tab.id"
                class="settings-tab" :class="{ active: activeTab === tab.id }"
                @click="activeTab = tab.id">
          <span class="settings-tab-icon">{{ tab.icon }}</span>
          {{ tab.label }}
        </button>
      </div>
      <div class="settings-body">
        <div v-if="error" class="settings-error">{{ error }}</div>
        <ConfigPanel v-if="activeTab === 'config'"
                     :initial-config="config"
                     :save-status="saveStatus"
                     @save="handleSaveConfig" />
        <WorkflowPanel v-if="activeTab === 'workflow'"
                       :initial-workflow="workflow"
                       :save-status="saveStatus"
                       @save="handleSaveWorkflow" />
        <KnowledgePanel v-if="activeTab === 'knowledge'"
                        :initial-config="config"
                        :knowledge-health="knowledgeHealth"
                        :save-status="saveStatus"
                        @save="handleSaveConfig"
                        @refresh-health="handleRefreshHealth" />
      </div>
    </div>
  `,
};
