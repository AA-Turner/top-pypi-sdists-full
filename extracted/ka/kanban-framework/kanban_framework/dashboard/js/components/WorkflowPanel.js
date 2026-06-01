import { ref, reactive, watch, onMounted, computed } from 'vue';
import { StepEditor } from './StepEditor.js';
import { GuardEditor } from './GuardEditor.js';
import { ModeEditor } from './ModeEditor.js';

const PHASE_ORDER = ['plan', 'plan_review', 'qa_spec', 'spec_review', 'execute', 'evaluate', 'retrospective', 'archive'];
const PHASE_LABELS = {
  plan: '规划', plan_review: 'Plan 评审', qa_spec: '测试规格', spec_review: '规格评审',
  execute: '执行', evaluate: '评估', retrospective: '复盘', archive: '归档',
};
const DEFAULT_AGENT_ROLES = ['code_reviewer', 'qa', 'pm', 'designer', 'plan_reviewer'];

function getPhaseConfig(phases, phaseId) {
  if (!Array.isArray(phases)) return null;
  return phases.find(p => p.id === phaseId) || null;
}

function ensurePhase(phases, phaseId) {
  let phase = getPhaseConfig(phases, phaseId);
  if (!phase) {
    phase = { id: phaseId };
    phases.push(phase);
  }
  return phase;
}

export const WorkflowPanel = {
  props: {
    initialWorkflow: { type: Object, default: () => ({}) },
    saveStatus: { type: String, default: 'idle' },
  },
  emits: ['save'],
  setup(props, { emit }) {
    const selectedPhase = ref('evaluate');
    const globalTab = ref(null);
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

    const currentPhase = computed(() => getPhaseConfig(workflow.phases, selectedPhase.value));

    const globalPassThreshold = computed({
      get: () => workflow.pass_threshold ?? 8.5,
      set: (v) => { workflow.pass_threshold = Number(v); },
    });

    const maxIterations = computed({
      get: () => workflow.max_iterations ?? 6,
      set: (v) => { workflow.max_iterations = Number(v); },
    });

    const dimensionWeightSum = computed(() => {
      const phase = currentPhase.value;
      if (!phase || !phase.quality_gate || !phase.quality_gate.dimensions) return 0;
      return phase.quality_gate.dimensions.reduce((s, d) => s + (d.weight || 0), 0);
    });

    function selectPhase(phaseId) {
      selectedPhase.value = phaseId;
      globalTab.value = null;
    }

    function selectGlobal(tab) {
      globalTab.value = tab;
      selectedPhase.value = '';
      selectedMode.value = null;  // Clear mode context when navigating via global nav
    }

    function toggleQualityGate(phaseId) {
      const phase = ensurePhase(workflow.phases, phaseId);
      if (!phase.quality_gate) {
        phase.quality_gate = { enabled: true, pass_threshold: 8.5, max_rounds: 3, dimensions: [] };
      } else {
        phase.quality_gate.enabled = !phase.quality_gate.enabled;
      }
      dirty.value = true;
    }

    function addDimension(phaseId) {
      const phase = ensurePhase(workflow.phases, phaseId);
      if (!phase.quality_gate) phase.quality_gate = { enabled: true, dimensions: [] };
      if (!phase.quality_gate.dimensions) phase.quality_gate.dimensions = [];
      phase.quality_gate.dimensions.push({ id: `dim_${Date.now()}`, name: '', weight: 0.2 });
      dirty.value = true;
    }

    function removeDimension(phaseId, index) {
      const phase = getPhaseConfig(workflow.phases, phaseId);
      if (phase && phase.quality_gate && phase.quality_gate.dimensions) {
        phase.quality_gate.dimensions.splice(index, 1);
        dirty.value = true;
      }
    }

    function addAgent(phaseId) {
      const phase = ensurePhase(workflow.phases, phaseId);
      if (!phase.agents) phase.agents = [];
      phase.agents.push({ role: '', required: true, parallel: false });
      dirty.value = true;
    }

    function removeAgent(phaseId, index) {
      const phase = getPhaseConfig(workflow.phases, phaseId);
      if (phase && phase.agents) {
        phase.agents.splice(index, 1);
        dirty.value = true;
      }
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
        // Write to modes.<name>.phases[]
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
        // Write to top-level phases[]
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
      if (!workflow.phases) workflow.phases = [];
      let existing = workflow.phases.find(p => p.id === phaseId);
      if (!existing) {
        existing = { id: phaseId };
        workflow.phases.push(existing);
      }
      existing.guard = guard;
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
      return (mode && mode.phases) || [];
    }

    return {
      PHASE_ORDER, PHASE_LABELS, DEFAULT_AGENT_ROLES,
      selectedPhase, globalTab, workflow, dirty,
      currentPhase, globalPassThreshold, maxIterations, dimensionWeightSum,
      selectPhase, selectGlobal, toggleQualityGate,
      addDimension, removeDimension, addAgent, removeAgent, handleSave,
      handleExtensionsUpdate, handleStepsUpdate, handleGuardUpdate, handleModesUpdate,
      selectedMode, handleEditModeSteps, getModePhases,
    };
  },
  components: { StepEditor, GuardEditor, ModeEditor },
  template: `
    <div class="workflow-panel">
      <div class="workflow-layout">
        <div class="workflow-nav">
          <div class="workflow-nav-section">阶段</div>
          <a v-for="pid in PHASE_ORDER" :key="pid"
             class="workflow-nav-item" :class="{ active: selectedPhase === pid }"
             @click="selectPhase(pid)">
            <span class="phase-id">{{ pid }}</span>
            <span class="phase-label">{{ PHASE_LABELS[pid] || pid }}</span>
          </a>
          <div class="workflow-nav-divider"></div>
          <div class="workflow-nav-section">全局设置</div>
          <a class="workflow-nav-item" :class="{ active: globalTab === 'self_improve' }" @click="selectGlobal('self_improve')">
            <span class="phase-label">自迭代策略</span>
          </a>
          <a class="workflow-nav-item" :class="{ active: globalTab === 'user_decision' }" @click="selectGlobal('user_decision')">
            <span class="phase-label">用户决策门控</span>
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

          <div v-if="globalTab === 'self_improve'" class="phase-editor">
            <h3>自迭代策略</h3>
            <div class="field-row">
              <label class="field-label">最大迭代次数</label>
              <input type="number" v-model.number="maxIterations" min="1" max="10" class="field-input field-input-number" />
            </div>
            <div class="field-row">
              <label class="field-label">全局通过阈值</label>
              <div class="slider-control">
                <input type="range" v-model.number="globalPassThreshold" min="7" max="10" step="0.5" class="field-slider" />
                <span class="slider-value">{{ globalPassThreshold }}</span>
              </div>
            </div>
            <div class="field-row">
              <label class="field-label" title="评分全部通过时立即退出迭代">全部通过即退出 ⓘ</label>
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
          </div>

          <div v-if="globalTab === 'user_decision'" class="phase-editor">
            <h3>用户决策门控</h3>
            <div class="field-row">
              <label class="field-label">触发条件</label>
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
            <GuardEditor
              :phases="workflow.phases || []"
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
          <div v-if="currentPhase && !globalTab" class="phase-editor">
            <h3>{{ PHASE_LABELS[currentPhase.id] || currentPhase.id }} 阶段</h3>

            <div v-if="currentPhase.id === 'evaluate'" class="field-row">
              <label class="field-label" style="font-weight:600">评估通过阈值</label>
              <div class="slider-control">
                <input type="range" v-model.number="currentPhase.pass_threshold" min="7" max="10" step="0.5" class="field-slider" />
                <span class="slider-value">{{ currentPhase.pass_threshold || 9.0 }}</span>
              </div>
            </div>

            <div class="field-group">
              <div class="field-group-header">
                质量门禁
                <label class="switch switch-inline">
                  <input type="checkbox"
                         :checked="currentPhase.quality_gate && currentPhase.quality_gate.enabled"
                         @change="toggleQualityGate(currentPhase.id)" />
                  <span class="switch-slider"></span>
                </label>
              </div>
              <div class="field-group-body" v-if="currentPhase.quality_gate && currentPhase.quality_gate.enabled">
                <div class="field-row">
                  <label class="field-label">通过阈值</label>
                  <div class="slider-control">
                    <input type="range" v-model.number="currentPhase.quality_gate.pass_threshold" min="7" max="10" step="0.5" class="field-slider" />
                    <span class="slider-value">{{ currentPhase.quality_gate.pass_threshold || 8.5 }}</span>
                  </div>
                </div>
                <div class="field-row">
                  <label class="field-label">最大审核轮数</label>
                  <input type="number" v-model.number="currentPhase.quality_gate.max_rounds" min="1" max="5" class="field-input field-input-number" />
                </div>

                <div v-if="currentPhase.quality_gate.dimensions && currentPhase.quality_gate.dimensions.length" class="dimensions-list">
                  <div class="dim-header">
                    <span>评审维度</span>
                    <span class="dim-weight-hint" :class="{ 'weight-ok': Math.abs(dimensionWeightSum - 1) < 0.01, 'weight-bad': Math.abs(dimensionWeightSum - 1) >= 0.01 }">
                      权重总和: {{ dimensionWeightSum.toFixed(2) }}
                    </span>
                  </div>
                  <div v-for="(dim, idx) in currentPhase.quality_gate.dimensions" :key="idx" class="dim-row">
                    <input type="text" v-model="dim.name" placeholder="维度名称" class="field-input dim-name" />
                    <input type="number" v-model.number="dim.weight" min="0" max="1" step="0.05" class="field-input field-input-number dim-weight" />
                    <button class="btn btn-icon btn-danger" @click="removeDimension(currentPhase.id, idx)" title="删除">×</button>
                  </div>
                </div>
                <button class="btn btn-secondary btn-sm" @click="addDimension(currentPhase.id)">+ 添加维度</button>
              </div>
            </div>

            <div class="field-group">
              <div class="field-group-header">Agent 配置</div>
              <div class="field-group-body">
                <div v-if="currentPhase.agents && currentPhase.agents.length" class="agents-list">
                  <div v-for="(agent, idx) in currentPhase.agents" :key="idx" class="agent-row">
                    <input type="text" v-model="agent.role" placeholder="role" class="field-input agent-role"
                           list="agent-roles" />
                    <label class="switch switch-inline" title="必需">
                      <input type="checkbox" v-model="agent.required" />
                      <span class="switch-slider"></span>
                    </label>
                    <span class="agent-toggle-label">必需</span>
                    <label class="switch switch-inline" title="并行">
                      <input type="checkbox" v-model="agent.parallel" />
                      <span class="switch-slider"></span>
                    </label>
                    <span class="agent-toggle-label">并行</span>
                    <button class="btn btn-icon btn-danger" @click="removeAgent(currentPhase.id, idx)" title="删除">×</button>
                  </div>
                </div>
                <button class="btn btn-secondary btn-sm" @click="addAgent(currentPhase.id)">+ 添加 Agent</button>
                <datalist id="agent-roles">
                  <option v-for="r in DEFAULT_AGENT_ROLES" :key="r" :value="r" />
                </datalist>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  `,
};
