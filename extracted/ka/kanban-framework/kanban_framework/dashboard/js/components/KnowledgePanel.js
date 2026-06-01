import { ref, onMounted } from 'vue';

const SCOPE_PATTERN = /^[a-z0-9][a-z0-9-]{1,15}$/;
const BACKEND_OPTIONS = ['builtin', 'chromadb'];

export const KnowledgePanel = {
  props: {
    initialConfig: { type: Object, default: () => ({}) },
    knowledgeHealth: { type: Object, default: () => null },
  },
  emits: ['save', 'refreshHealth'],
  setup(props, { emit }) {
    const backend = ref('builtin');
    const scope = ref('');
    const scopeValid = ref(true);
    const shareEnabled = ref(false);
    const sharePath = ref('');
    const dirty = ref(false);
    const confirmBackendSwitch = ref(false);
    const pendingBackend = ref('');

    function initFromConfig(config) {
      backend.value = config.knowledge?.backend || 'builtin';
      scope.value = config.knowledge?.scope || '';
      shareEnabled.value = config.knowledge?.share?.enabled || false;
      sharePath.value = config.knowledge?.share?.path || '';
      scopeValid.value = !scope.value || SCOPE_PATTERN.test(scope.value);
      dirty.value = false;
    }

    onMounted(() => { if (props.initialConfig) initFromConfig(props.initialConfig); });

    function validateScope(val) {
      scope.value = val;
      scopeValid.value = !val || SCOPE_PATTERN.test(val);
      dirty.value = true;
    }

    function requestBackendSwitch(newBackend) {
      if (newBackend !== backend.value) {
        pendingBackend.value = newBackend;
        confirmBackendSwitch.value = true;
      }
    }

    function confirmSwitch() {
      backend.value = pendingBackend.value;
      confirmBackendSwitch.value = false;
      dirty.value = true;
    }

    function cancelSwitch() {
      confirmBackendSwitch.value = false;
      pendingBackend.value = '';
    }

    function handleSave() {
      const payload = {
        knowledge: {
          backend: backend.value,
          scope: scope.value,
          share: {
            enabled: shareEnabled.value,
            path: sharePath.value,
          },
        },
      };
      emit('save', payload);
      dirty.value = false;
    }

    return {
      BACKEND_OPTIONS, backend, scope, scopeValid,
      shareEnabled, sharePath, dirty,
      confirmBackendSwitch, pendingBackend,
      validateScope, requestBackendSwitch, confirmSwitch, cancelSwitch, handleSave,
    };
  },
  template: `
    <div class="knowledge-panel">
      <div class="field-group">
        <div class="field-group-header">后端配置</div>
        <div class="field-group-body">
          <div class="field-row">
            <label class="field-label">当前后端
              <span class="tooltip-icon" title="切换后端不影响已有数据，搜索自动路由">ⓘ</span>
            </label>
            <select v-model="backend" class="field-select" @change="requestBackendSwitch($event.target.value)">
              <option v-for="opt in BACKEND_OPTIONS" :key="opt" :value="opt">{{ opt }}</option>
            </select>
          </div>
        </div>
      </div>

      <div v-if="confirmBackendSwitch" class="confirm-dialog">
        <p>确定要切换后端到 <strong>{{ pendingBackend }}</strong> 吗？</p>
        <div class="confirm-actions">
          <button class="btn btn-secondary" @click="cancelSwitch">取消</button>
          <button class="btn btn-primary" @click="confirmSwitch">确认切换</button>
        </div>
      </div>

      <div class="field-group">
        <div class="field-group-header">个人标识 (scope)</div>
        <div class="field-group-body">
          <div class="field-row">
            <label class="field-label">Scope
              <span class="tooltip-icon" title="设置后 DB 文件自动隔离为 knowledge-{scope}.db">ⓘ</span>
            </label>
            <input type="text" :value="scope" @input="validateScope($event.target.value)"
                   class="field-input" :class="{ 'field-error': !scopeValid }"
                   placeholder="例: alice" />
            <span v-if="!scopeValid" class="field-error-msg">格式: 小写字母数字开头, 2-16位</span>
          </div>
        </div>
      </div>

      <div class="field-group">
        <div class="field-group-header">共享知识库</div>
        <div class="field-group-body">
          <div class="field-row">
            <label class="field-label">启用共享</label>
            <label class="switch">
              <input type="checkbox" v-model="shareEnabled" @change="dirty = true" />
              <span class="switch-slider"></span>
            </label>
          </div>
          <div v-if="shareEnabled" class="field-row">
            <label class="field-label">共享库路径</label>
            <input type="text" v-model="sharePath" @input="dirty = true" class="field-input"
                   placeholder="/shared/team/knowledge.db" />
          </div>
        </div>
      </div>

      <div class="field-group">
        <div class="field-group-header">
          健康状态
          <button class="btn btn-secondary btn-sm" @click="$emit('refreshHealth')">刷新</button>
        </div>
        <div class="field-group-body">
          <div v-if="knowledgeHealth && knowledgeHealth.success" class="health-card">
            <div class="health-grid">
              <div class="health-item">
                <span class="health-label">条目总数</span>
                <span class="health-value">{{ knowledgeHealth.data?.total_entries ?? '-' }}</span>
              </div>
              <div class="health-item">
                <span class="health-label">覆盖领域</span>
                <span class="health-value">{{ knowledgeHealth.data?.domains?.length ?? '-' }}</span>
              </div>
              <div class="health-item">
                <span class="health-label">过期条目</span>
                <span class="health-value">{{ knowledgeHealth.data?.expired ?? '-' }}</span>
              </div>
              <div class="health-item">
                <span class="health-label">重复嫌疑</span>
                <span class="health-value">{{ knowledgeHealth.data?.duplicates ?? '-' }}</span>
              </div>
            </div>
          </div>
          <div v-else-if="knowledgeHealth" class="health-card health-error">
            <span>{{ knowledgeHealth.error || '无法获取健康状态' }}</span>
          </div>
          <div v-else class="health-card">
            <span>点击「刷新」获取知识库健康状态</span>
          </div>
        </div>
      </div>

      <div class="settings-status-bar">
        <button class="btn btn-primary" @click="handleSave" :disabled="!dirty || !scopeValid">保存</button>
      </div>
    </div>
  `,
};
