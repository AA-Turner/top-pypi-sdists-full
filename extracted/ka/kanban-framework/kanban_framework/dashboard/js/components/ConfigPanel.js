import { ref, reactive, watch, onMounted } from 'vue';

const FIELD_GROUPS = [
  {
    title: '基础配置',
    fields: [
      { key: 'project', label: '项目名称', type: 'text', default: '', tooltip: '项目名称，用于 dashboard 展示和归档记录' },
      { key: 'trunk', label: '主干分支', type: 'text', default: 'main', tooltip: '归档时 worktree 代码合并到此分支' },
      { key: 'output_dir', label: '产出目录', type: 'text', default: 'src', tooltip: '产出代码的根目录名，已有代码库建议设为空' },
      { key: 'python_bin', label: 'Python 解释器', type: 'text', default: 'venv/bin/python', tooltip: 'Python 解释器路径，支持相对路径和绝对路径' },
      { key: 'task_id_base', label: '任务编号基数', type: 'number', default: 0, tooltip: '设置后任务 ID 从 base*1000+1 开始' },
    ],
  },
  {
    title: '知识库',
    fields: [
      { key: 'knowledge.backend', label: '后端引擎', type: 'select', default: 'builtin', options: ['builtin', 'chromadb'], tooltip: 'builtin (SQLite FTS5) / chromadb (向量检索)' },
      { key: 'knowledge.scope', label: '个人标识 (scope)', type: 'text', default: '', tooltip: '设置后 DB 文件自动隔离为 knowledge-{scope}.db', pattern: '^[a-z0-9][a-z0-9-]{1,15}$' },
    ],
  },
  {
    title: '超时控制',
    fields: [
      { key: 'timeout.plan_seconds', label: 'Plan 阶段 (秒)', type: 'slider', default: 300, min: 60, max: 600, step: 30, tooltip: 'Plan 全阶段总超时' },
      { key: 'timeout.execute_seconds', label: 'Execute 阶段 (秒)', type: 'slider', default: 600, min: 60, max: 1800, step: 60, tooltip: 'Execute 阶段总超时，复杂任务建议调大' },
      { key: 'timeout.evaluate_seconds', label: 'Evaluate 阶段 (秒)', type: 'slider', default: 300, min: 60, max: 600, step: 30, tooltip: 'Evaluate 阶段总超时' },
      { key: 'timeout.single_agent_seconds', label: '单 Agent (秒)', type: 'slider', default: 180, min: 30, max: 600, step: 30, tooltip: '单个 Agent 调用的超时' },
    ],
  },
  {
    title: 'Token 预算',
    fields: [
      { key: 'budget.per_task', label: '单任务预算', type: 'number', default: 500000, tooltip: '单个任务的总 token 预算上限' },
      { key: 'budget.per_phase.plan', label: 'Plan 阶段', type: 'number', default: 50000, tooltip: 'Plan 阶段 token 预算' },
      { key: 'budget.per_phase.execute', label: 'Execute 阶段', type: 'number', default: 200000, tooltip: 'Execute 阶段 token 预算' },
      { key: 'budget.per_phase.evaluate', label: 'Evaluate 阶段', type: 'number', default: 150000, tooltip: 'Evaluate 阶段 token 预算' },
      { key: 'budget.warning_threshold', label: '告警阈值', type: 'slider', default: 0.8, min: 0.5, max: 1.0, step: 0.05, tooltip: '消耗超过 预算×阈值 时触发 warning' },
      { key: 'budget.hard_limit', label: '硬性限制', type: 'switch', default: true, tooltip: '超预算时是否强制阻断新 Agent 调用' },
    ],
  },
  {
    title: '调度策略',
    fields: [
      { key: 'scheduler.max_parallel', label: '最大并行数', type: 'slider', default: 3, min: 1, max: 5, step: 1, tooltip: '同一批次最多并行启动的 Agent 数量' },
      { key: 'scheduler.poll_interval_seconds', label: '轮询间隔 (秒)', type: 'slider', default: 30, min: 10, max: 120, step: 5, tooltip: '后台 Agent 完成状态的检查间隔' },
      { key: 'scheduler.conflict_strategy', label: '冲突策略', type: 'readonly', default: 'serialize', tooltip: '当前仅支持 serialize（串行化）' },
    ],
  },
];

function getNestedValue(obj, key) {
  return key.split('.').reduce((o, k) => o && o[k], obj);
}

function setNestedValue(obj, key, value) {
  const parts = key.split('.');
  let current = obj;
  for (let i = 0; i < parts.length - 1; i++) {
    if (!current[parts[i]]) current[parts[i]] = {};
    current = current[parts[i]];
  }
  current[parts[parts.length - 1]] = value;
}

export const ConfigPanel = {
  props: {
    initialConfig: { type: Object, default: () => ({}) },
    saveStatus: { type: String, default: 'idle' },
  },
  emits: ['save'],
  setup(props, { emit }) {
    const form = reactive({});
    const collapsed = reactive({});
    const dirty = ref(false);

    function initForm(config) {
      for (const group of FIELD_GROUPS) {
        collapsed[group.title] = false;
        for (const field of group.fields) {
          const val = getNestedValue(config, field.key);
          form[field.key] = val !== undefined ? val : field.default;
        }
      }
      dirty.value = false;
    }

    onMounted(() => {
      if (props.initialConfig) initForm(props.initialConfig);
    });

    watch(() => props.initialConfig, (newConfig) => {
      if (newConfig) initForm(newConfig);
    });

    watch(form, () => { dirty.value = true; }, { deep: true });

    function buildPayload() {
      const payload = {};
      for (const group of FIELD_GROUPS) {
        for (const field of group.fields) {
          setNestedValue(payload, field.key, form[field.key]);
        }
      }
      return payload;
    }

    function handleSave() {
      emit('save', buildPayload());
      dirty.value = false;
    }

    function handleReset() {
      if (!confirm('确定要重置为默认值吗？当前修改将丢失。')) return;
      for (const group of FIELD_GROUPS) {
        for (const field of group.fields) {
          form[field.key] = field.default;
        }
      }
      dirty.value = true;
    }

    function toggleGroup(title) {
      collapsed[title] = !collapsed[title];
    }

    function validateField(field) {
      if (field.pattern && form[field.key]) {
        return new RegExp(field.pattern).test(form[field.key]);
      }
      return true;
    }

    return {
      FIELD_GROUPS, form, collapsed, dirty,
      handleSave, handleReset, toggleGroup, validateField,
    };
  },
  template: `
    <div class="config-panel">
      <div class="settings-status-bar">
        <span class="save-status" :class="saveStatus">
          {{ saveStatus === 'saving' ? '保存中...' : saveStatus === 'saved' ? '已保存' : saveStatus === 'error' ? '保存失败' : '' }}
        </span>
        <div class="status-actions">
          <button class="btn btn-secondary" @click="handleReset" :disabled="!dirty">重置默认值</button>
          <button class="btn btn-primary" @click="handleSave" :disabled="!dirty || saveStatus === 'saving'">
            {{ saveStatus === 'saving' ? '保存中...' : '保存' }}
          </button>
        </div>
      </div>

      <div v-for="group in FIELD_GROUPS" :key="group.title" class="field-group">
        <div class="field-group-header" @click="toggleGroup(group.title)">
          <span>{{ group.title }}</span>
          <span class="collapse-icon" :class="{ collapsed: collapsed[group.title] }">▾</span>
        </div>
        <div class="field-group-body" v-show="!collapsed[group.title]">
          <div v-for="field in group.fields" :key="field.key" class="field-row">
            <label class="field-label" :title="field.tooltip">
              {{ field.label }}
              <span class="tooltip-icon" :title="field.tooltip">ⓘ</span>
            </label>
            <div class="field-control">
              <input v-if="field.type === 'text'"
                     v-model="form[field.key]"
                     class="field-input"
                     :class="{ 'field-error': !validateField(field) }"
                     :placeholder="field.default" />
              <input v-else-if="field.type === 'number'"
                     v-model.number="form[field.key]"
                     type="number"
                     class="field-input field-input-number" />
              <div v-else-if="field.type === 'slider'" class="slider-control">
                <input type="range"
                       v-model.number="form[field.key]"
                       :min="field.min" :max="field.max" :step="field.step"
                       class="field-slider" />
                <span class="slider-value">{{ form[field.key] }}</span>
              </div>
              <label v-else-if="field.type === 'switch'" class="switch">
                <input type="checkbox" v-model="form[field.key]" />
                <span class="switch-slider"></span>
              </label>
              <select v-else-if="field.type === 'select'"
                      v-model="form[field.key]"
                      class="field-select">
                <option v-for="opt in field.options" :key="opt" :value="opt">{{ opt }}</option>
              </select>
              <span v-else-if="field.type === 'readonly'" class="field-readonly">{{ form[field.key] }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  `,
};
