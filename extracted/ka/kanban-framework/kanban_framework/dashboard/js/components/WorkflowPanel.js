import { ref, reactive, watch, onMounted, computed } from 'vue';
import { StepEditor } from './StepEditor.js';
import { GuardEditor } from './GuardEditor.js';
import { ModeEditor } from './ModeEditor.js';

export const WorkflowPanel = {
  props: {
    initialWorkflow: { type: Object, default: () => ({}) },
    saveStatus: { type: String, default: 'idle' },
  },
  emits: ['save'],
  setup(props, { emit }) {
    const globalTab = ref('modes');
    const workflow = reactive({});
    const dirty = ref(false);

    function initWorkflow(data) {
      Object.keys(workflow).forEach(k => delete workflow[k]);
      Object.assign(workflow, JSON.parse(JSON.stringify(data || {})));
      if (!workflow.phases) workflow.phases = [];
      if (!workflow.self_improve) workflow.self_improve = {};
      if (!workflow.user_decision) workflow.user_decision = {};
      dirty.value = false;
    }

    onMounted(() => { if (props.initialWorkflow) initWorkflow(props.initialWorkflow); });
    watch(() => props.initialWorkflow, (v) => { if (v) initWorkflow(v); });
    watch(workflow, () => { dirty.value = true; }, { deep: true });

    const globalPassThreshold = computed({
      get: () => workflow.pass_threshold ?? 8.5,
      set: (v) => { workflow.pass_threshold = Number(v); },
    });

    const maxIterations = computed({
      get: () => workflow.max_iterations ?? 6,
      set: (v) => { workflow.max_iterations = Number(v); },
    });

    function selectGlobal(tab) {
      globalTab.value = tab;
      selectedMode.value = null;
    }

    function handleSave() {
      emit('save', JSON.parse(JSON.stringify(workflow)));
      dirty.value = false;
    }

    function handleExtensionsUpdate(updatedSteps) {
      if (!workflow.extensions) workflow.extensions = {};
      if (!workflow.extensions.modes || !Array.isArray(workflow.extensions.modes) || workflow.extensions.modes.length === 0) {
        workflow.extensions.modes = ['full'];
      }
      workflow.extensions.add_steps = updatedSteps;
      dirty.value = true;
    }

    function handleStepsUpdate(updatedPhases) {
      if (selectedMode.value) {
        if (!workflow.modes) workflow.modes = {};
        if (!workflow.modes[selectedMode.value]) workflow.modes[selectedMode.value] = {};
        const mode = workflow.modes[selectedMode.value];
        if (!mode.phases) mode.phases = [];
        for (const up of updatedPhases) {
          let existing = mode.phases.find(p => p.id === up.id);
          if (!existing) {
            existing = { id: up.id };
            mode.phases.push(existing);
          }
          existing.steps = up.steps;
        }
      } else {
        if (!workflow.phases) workflow.phases = [];
        for (const up of updatedPhases) {
          let existing = workflow.phases.find(p => p.id === up.id);
          if (!existing) {
            existing = { id: up.id };
            workflow.phases.push(existing);
          }
          existing.steps = up.steps;
        }
      }
      dirty.value = true;
    }

    function handleGuardUpdate({ phaseId, guard }) {
      if (selectedMode.value) {
        // Write to mode-specific phases
        if (!workflow.modes) workflow.modes = {};
        if (!workflow.modes[selectedMode.value]) workflow.modes[selectedMode.value] = {};
        const mode = workflow.modes[selectedMode.value];
        if (!mode.phases) mode.phases = [];
        let existing = mode.phases.find(p => p.id === phaseId);
        if (!existing) {
          existing = { id: phaseId };
          mode.phases.push(existing);
        }
        existing.guard = guard;
      } else {
        // Write to top-level phases
        if (!workflow.phases) workflow.phases = [];
        let existing = workflow.phases.find(p => p.id === phaseId);
        if (!existing) {
          existing = { id: phaseId };
          workflow.phases.push(existing);
        }
        existing.guard = guard;
      }
      dirty.value = true;
    }

    const selectedMode = ref(null);

    function handleModesUpdate(updatedModes) {
      workflow.modes = updatedModes;
      dirty.value = true;
    }

    function handleEditModeSteps(modeName) {
      selectedMode.value = modeName;
      globalTab.value = 'extensions';
    }

    function getModePhases(modeName) {
      if (!modeName || !workflow.modes || !workflow.modes[modeName]) return [];
      const mode = workflow.modes[modeName];
      const order = (mode && mode.phase_order) || [];
      const existing = (mode && mode.phases) || [];
      const result = [];
      const byId = {};
      for (const p of existing) { byId[p.id] = p; }
      for (const pid of order) {
        result.push(byId[pid] || { id: pid, steps: [] });
      }
      return result.length > 0 ? result : existing;
    }

    return {
      globalTab, workflow, dirty,
      globalPassThreshold, maxIterations,
      selectGlobal, handleSave,
      handleExtensionsUpdate, handleStepsUpdate, handleGuardUpdate, handleModesUpdate,
      selectedMode, handleEditModeSteps, getModePhases,
    };
  },
  components: { StepEditor, GuardEditor, ModeEditor },
  template: `
    <div class="workflow-panel">
      <div class="workflow-layout">
        <div class="workflow-nav">
          <div class="workflow-nav-section">工作流配置</div>
          <a class="workflow-nav-item" :class="{ active: globalTab === 'settings' }" @click="selectGlobal('settings')">
            <span class="phase-label">全局设置</span>
          </a>
          <a class="workflow-nav-item" :class="{ active: globalTab === 'extensions' }" @click="selectGlobal('extensions')">
            <span class="phase-label">步骤编辑</span>
          </a>
          <a class="workflow-nav-item" :class="{ active: globalTab === 'guard' }" @click="selectGlobal('guard')">
            <span class="phase-label">Guard 检查</span>
          </a>
          <a class="workflow-nav-item" :class="{ active: globalTab === 'modes' }" @click="selectGlobal('modes')">
            <span class="phase-label">模式编辑</span>
          </a>
        </div>

        <div class="workflow-content">
          <div class="settings-status-bar">
            <span class="save-status" :class="saveStatus">
              {{ saveStatus === 'saving' ? '保存中...' : saveStatus === 'saved' ? '已保存' : saveStatus === 'error' ? '保存失败' : '' }}
            </span>
            <button class="btn btn-primary" @click="handleSave" :disabled="!dirty || saveStatus === 'saving'">保存</button>
          </div>

          <div v-if="globalTab === 'settings'" class="phase-editor">
            <h3>全局设置</h3>
            <div class="field-row">
              <label class="field-label">全局通过阈值</label>
              <div class="slider-control">
                <input type="range" v-model.number="globalPassThreshold" min="7" max="10" step="0.5" class="field-slider" />
                <span class="slider-value">{{ globalPassThreshold }}</span>
              </div>
            </div>
            <div class="field-row">
              <label class="field-label">最大迭代次数</label>
              <input type="number" v-model.number="maxIterations" min="1" max="10" class="field-input field-input-number" />
            </div>
            <div class="field-row">
              <label class="field-label" title="评分全部通过时立即退出迭代">全部通过即退出</label>
              <label class="switch">
                <input type="checkbox" v-model="workflow.self_improve.exit_all_pass" />
                <span class="switch-slider"></span>
              </label>
            </div>
            <div class="field-row">
              <label class="field-label">默认回退起点</label>
              <select v-model="workflow.self_improve.default_restart_from" class="field-select">
                <option value="plan">plan</option>
                <option value="execute">execute</option>
              </select>
            </div>
            <div class="field-row">
              <label class="field-label">用户决策触发条件</label>
              <input type="text" v-model="workflow.user_decision.trigger" class="field-input"
                     placeholder="all_pass OR max_iterations_reached" />
            </div>
          </div>

          <div v-if="globalTab === 'extensions'" class="phase-editor">
            <div v-if="selectedMode" class="step-editor-mode-banner">
              正在编辑模式: <strong>{{ selectedMode }}</strong>
              <button class="btn btn-sm btn-secondary" @click="selectedMode = null">切换到全局步骤</button>
            </div>
            <StepEditor
              :phases="selectedMode ? getModePhases(selectedMode) : (workflow.phases || [])"
              :extensions="workflow.extensions || {}"
              :mode-name="selectedMode"
              @update:steps="handleStepsUpdate"
              @update:extensions="handleExtensionsUpdate"
            />
          </div>
          <div v-if="globalTab === 'guard'" class="phase-editor">
            <div v-if="selectedMode" class="step-editor-mode-banner">
              正在编辑模式: <strong>{{ selectedMode }}</strong> — Guard 检查
              <button class="btn btn-sm btn-secondary" @click="selectedMode = null">切换到全局 Guard</button>
            </div>
            <GuardEditor
              :phases="selectedMode ? getModePhases(selectedMode) : (workflow.phases || [])"
              :mode-name="selectedMode"
              @update:guard="handleGuardUpdate"
            />
          </div>
          <div v-if="globalTab === 'modes'" class="phase-editor">
            <ModeEditor
              :modes="workflow.modes || {}"
              @update:modes="handleModesUpdate"
              @edit-steps="handleEditModeSteps"
            />
          </div>
        </div>
      </div>
    </div>
  `,
};
