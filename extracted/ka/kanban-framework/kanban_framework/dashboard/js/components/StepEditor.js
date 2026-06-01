import { ref, reactive, watch, onMounted, computed } from 'vue';
import { api } from '../utils/api.js';

const PHASE_ORDER = ['plan', 'plan_review', 'qa_spec', 'spec_review', 'execute', 'evaluate', 'retrospective', 'archive'];
const PHASE_LABELS = {
  plan: '规划', plan_review: 'Plan 评审', qa_spec: '测试规格', spec_review: '规格评审',
  execute: '执行', evaluate: '评估', retrospective: '复盘', archive: '归档',
};

function newStep(phase = 'execute', source = 'extension') {
  return {
    phase,
    insert_after: '',
    source,
    step: {
      id: '',
      description: '',
      agent_type: '',
      parallel: false,
      user_action: false,
      interactive: false,
      spawn_prompt: '',
      required_artifacts: [],
    },
  };
}

export const StepEditor = {
  props: {
    phases: { type: Array, default: () => [] },
    extensions: { type: Object, default: () => ({}) },
    modeName: { type: String, default: null },
  },
  emits: ['update:steps', 'update:extensions'],
  setup(props, { emit }) {
    const steps = reactive([]);
    const stepDefs = ref({});
    const agentTypes = ref([]);
    const filterPhase = ref('all');
    const viewMode = ref('all'); // 'all' | 'builtin' | 'extension'
    const showAdvanced = ref(false);
    const tagInput = reactive({});

    function initSteps(phasesArr, ext) {
      steps.splice(0, steps.length);
      // Load built-in steps from phases
      if (phasesArr && Array.isArray(phasesArr)) {
        for (const p of phasesArr) {
          if (p.steps && Array.isArray(p.steps)) {
            for (const s of p.steps) {
              steps.push({ phase: p.id, insert_after: '', source: 'builtin',
                step: { ...s } });
            }
          }
        }
      }
      // Load extension steps
      const raw = (ext && ext.add_steps) || [];
      for (const item of raw) {
        steps.push(JSON.parse(JSON.stringify({ ...item, source: 'extension' })));
      }
    }

    onMounted(async () => {
      initSteps(props.phases, props.extensions);
      try {
        const data = await api.getStepDefinitions();
        stepDefs.value = data.steps || {};
        agentTypes.value = data.agent_types || [];
      } catch (_) {
        agentTypes.value = [
          'kanban-planner', 'kanban-plan-reviewer', 'kanban-qa',
          'kanban-test-spec-reviewer', 'kanban-executor', 'kanban-code-reviewer',
          'kanban-knowledge-manager', 'kanban-researcher', 'kanban-designer',
          'kanban-pm', 'kanban-knowledge-capture',
        ];
      }
    });

    watch(() => [props.phases, props.extensions], () => {
      initSteps(props.phases, props.extensions);
    }, { deep: true });

    const filteredSteps = computed(() => {
      let list = steps.map((s, i) => ({ step: s, index: i }));
      if (viewMode.value === 'builtin') list = list.filter(({ step }) => step.source === 'builtin');
      else if (viewMode.value === 'extension') list = list.filter(({ step }) => step.source === 'extension');
      if (filterPhase.value !== 'all') list = list.filter(({ step }) => step.phase === filterPhase.value);
      return list;
    });

    function addStep(source) {
      const phase = filterPhase.value === 'all' ? 'execute' : filterPhase.value;
      steps.push(newStep(phase, source));
      emitAll();
    }

    function removeStep(index) {
      steps.splice(index, 1);
      emitAll();
    }

    function moveStep(index, dir) {
      const target = index + dir;
      if (target < 0 || target >= steps.length) return;
      const tmp = steps[index];
      steps[index] = steps[target];
      steps[target] = tmp;
      emitAll();
    }

    function getAfterOptions(phaseId) {
      if (!phaseId) return [];
      const opts = [{ value: '', label: '末尾追加' }];
      const builtIn = Object.entries(stepDefs.value)
        .filter(([id]) => id.startsWith(phaseId + '.'))
        .map(([id, def]) => ({ value: id, label: `${id} (${def.description || id})` }));
      opts.push(...builtIn);
      for (const s of steps) {
        const sid = s.step && s.step.id;
        if (sid && s.phase === phaseId) {
          const fullId = sid.includes('.') ? sid : `${phaseId}.${sid}`;
          if (!opts.some(o => o.value === fullId)) {
            opts.push({ value: fullId, label: fullId });
          }
        }
      }
      return opts;
    }

    function addArtifact(index) {
      const input = tagInput[index];
      if (!input || !input.trim()) return;
      const s = steps[index];
      if (!s.step.required_artifacts) s.step.required_artifacts = [];
      if (!s.step.required_artifacts.includes(input.trim())) {
        s.step.required_artifacts.push(input.trim());
      }
      tagInput[index] = '';
      emitAll();
    }

    function removeArtifact(index, artIdx) {
      const s = steps[index];
      if (s.step.required_artifacts) {
        s.step.required_artifacts.splice(artIdx, 1);
        emitAll();
      }
    }

    function emitAll() {
      // Emit built-in steps as phases
      const phaseMap = {};
      for (const p of (props.phases || [])) {
        phaseMap[p.id] = { ...p, steps: undefined };
      }
      for (const s of steps) {
        if (s.source !== 'builtin' || !s.step.id || !s.step.id.trim()) continue;
        const pid = s.phase;
        if (!phaseMap[pid]) phaseMap[pid] = { id: pid };
        if (!phaseMap[pid].steps) phaseMap[pid].steps = [];
        const out = { ...s.step };
        if (!out.agent_type) delete out.agent_type;
        if (!out.spawn_prompt) delete out.spawn_prompt;
        if (!out.required_artifacts || out.required_artifacts.length === 0) delete out.required_artifacts;
        if (out.parallel === false) delete out.parallel;
        if (out.user_action === false) delete out.user_action;
        if (out.interactive === false) delete out.interactive;
        phaseMap[pid].steps.push(out);
      }
      emit('update:steps', Object.values(phaseMap).filter(p => p.steps));

      // Emit extension steps
      const extSteps = [];
      for (const s of steps) {
        if (s.source !== 'extension' || !s.step.id || !s.step.id.trim()) continue;
        const out = { phase: s.phase, step: { ...s.step } };
        if (s.insert_after) out.insert_after = s.insert_after;
        if (!out.step.agent_type) delete out.step.agent_type;
        if (!out.step.spawn_prompt) delete out.step.spawn_prompt;
        if (!out.step.required_artifacts || out.step.required_artifacts.length === 0) delete out.step.required_artifacts;
        if (out.step.parallel === false) delete out.step.parallel;
        if (out.step.user_action === false) delete out.step.user_action;
        if (out.step.interactive === false) delete out.step.interactive;
        extSteps.push(out);
      }
      emit('update:extensions', extSteps);
    }

    const builtinCount = computed(() => steps.filter(s => s.source === 'builtin').length);
    const extCount = computed(() => steps.filter(s => s.source === 'extension').length);

    return {
      PHASE_ORDER, PHASE_LABELS,
      steps, stepDefs, agentTypes, filterPhase, viewMode, tagInput,
      filteredSteps, builtinCount, extCount,
      addStep, removeStep, moveStep, getAfterOptions,
      addArtifact, removeArtifact, emitAll, showAdvanced,
    };
  },
  template: `
    <div class="step-editor">
      <div class="step-editor-header">
        <h3>步骤编辑器</h3>
        <div class="step-editor-actions">
          <select v-model="viewMode" class="field-select" style="width:auto;margin-right:8px">
            <option value="all">全部 ({{ steps.length }})</option>
            <option value="builtin">内置步骤 ({{ builtinCount }})</option>
            <option value="extension">扩展步骤 ({{ extCount }})</option>
          </select>
          <button class="btn btn-primary btn-sm" @click="addStep(viewMode === 'extension' ? 'extension' : 'builtin')">+ 添加步骤</button>
        </div>
      </div>

      <div class="step-phase-tabs">
        <a class="step-phase-tab" :class="{ active: filterPhase === 'all' }"
           @click="filterPhase = 'all'">全部 ({{ steps.length }})</a>
        <a v-for="pid in PHASE_ORDER" :key="pid"
           class="step-phase-tab" :class="{ active: filterPhase === pid }"
           @click="filterPhase = pid"
           v-show="steps.filter(s => s.phase === pid).length > 0">
          {{ PHASE_LABELS[pid] || pid }}
          ({{ steps.filter(s => s.phase === pid).length }})
        </a>
      </div>

      <div v-if="filteredSteps.length === 0" class="step-empty">
        <span v-if="steps.length === 0">暂无步骤，点击上方按钮添加</span>
        <span v-else>该阶段下暂无步骤</span>
      </div>

      <div class="step-list">
        <div v-for="{ step: item, index } in filteredSteps" :key="index"
             class="step-card" :class="{ 'step-card-builtin': item.source === 'builtin' }">
          <div class="step-card-header">
            <input type="text" v-model="item.step.id" placeholder="步骤 ID (如 knowledge_search)"
                   class="field-input step-id-input" @input="emitAll" />
            <span class="step-card-phase-badge">{{ item.phase }}</span>
            <span class="step-card-source-badge" :class="'source-' + item.source">
              {{ item.source === 'builtin' ? '内置' : '扩展' }}
            </span>
            <button class="btn btn-icon btn-sm" @click="moveStep(index, -1)" title="上移">↑</button>
            <button class="btn btn-icon btn-sm" @click="moveStep(index, 1)" title="下移">↓</button>
            <button class="btn btn-icon btn-danger btn-sm" @click="removeStep(index)" title="删除">×</button>
          </div>
          <div class="step-card-body">
            <div class="field-row">
              <label class="field-label">描述</label>
              <input type="text" v-model="item.step.description" placeholder="步骤描述"
                     class="field-input" @input="emitAll" />
            </div>
            <div class="field-row">
              <label class="field-label">目标阶段</label>
              <select v-model="item.phase" class="field-select" @change="emitAll">
                <option v-for="pid in PHASE_ORDER" :key="pid" :value="pid">
                  {{ PHASE_LABELS[pid] || pid }}
                </option>
              </select>
            </div>
            <div class="field-row" v-if="item.source === 'extension'">
              <label class="field-label">插入位置</label>
              <select v-model="item.insert_after" class="field-select" @change="emitAll">
                <option v-for="opt in getAfterOptions(item.phase)" :key="opt.value"
                        :value="opt.value">{{ opt.label }}</option>
              </select>
            </div>
            <div class="field-row">
              <label class="field-label">Agent 类型</label>
              <div class="agent-type-input">
                <select v-model="item.step.agent_type" class="field-select agent-type-select" @change="emitAll">
                  <option value="">无 (纯动作)</option>
                  <option v-for="at in agentTypes" :key="at" :value="at">{{ at }}</option>
                  <option value="__custom__">自定义...</option>
                </select>
                <input v-if="item.step.agent_type === '__custom__'" type="text"
                       v-model="item.step.agent_type" placeholder="自定义 agent_type"
                       class="field-input agent-type-custom" @input="emitAll" />
              </div>
            </div>
            <div class="field-row">
              <label class="field-label">spawn_prompt</label>
              <textarea v-model="item.step.spawn_prompt" placeholder="告诉 Agent 要做什么..."
                        class="field-textarea" rows="3" @input="emitAll"></textarea>
            </div>
            <div class="field-row">
              <a class="step-phase-tab" @click="showAdvanced = !showAdvanced" style="cursor:pointer;font-size:12px">
                {{ showAdvanced ? '▾ 收起高级选项' : '▸ 高级选项 (依赖/并行/门禁/知识检索)' }}
              </a>
            </div>
            <template v-if="showAdvanced">
            <div class="field-row" v-if="item.source === 'extension'">
              <label class="field-label">依赖 (after)</label>
              <input type="text" :value="(item.step.after || []).join(', ')"
                     placeholder="step_id, ... (逗号分隔)" class="field-input"
                     @input="item.step.after = $event.target.value.split(',').map(s=>s.trim()).filter(Boolean); emitAll()" />
            </div>
            <div class="field-row step-toggles">
              <label class="switch switch-inline" title="并行执行">
                <input type="checkbox" v-model="item.step.parallel" @change="emitAll" />
                <span class="switch-slider"></span>
              </label>
              <span class="agent-toggle-label">并行</span>
              <label class="switch switch-inline" title="需用户操作">
                <input type="checkbox" v-model="item.step.user_action" @change="emitAll" />
                <span class="switch-slider"></span>
              </label>
              <span class="agent-toggle-label">用户操作</span>
              <label class="switch switch-inline" title="交互式">
                <input type="checkbox" v-model="item.step.interactive" @change="emitAll" />
                <span class="switch-slider"></span>
              </label>
              <span class="agent-toggle-label">交互式</span>
            </div>
            <div class="field-row">
              <label class="field-label">产物验证</label>
              <div class="tag-input-group">
                <div class="tag-list">
                  <span v-for="(art, ai) in (item.step.required_artifacts || [])" :key="ai" class="tag">
                    {{ art }}
                    <button class="tag-remove" @click="removeArtifact(index, ai)">×</button>
                  </span>
                </div>
                <div class="tag-input-row">
                  <input type="text" v-model="tagInput[index]" placeholder="文件名 (如 report.json)"
                         class="field-input tag-field" @keydown.enter.prevent="addArtifact(index)" />
                  <button class="btn btn-secondary btn-sm" @click="addArtifact(index)">添加</button>
                </div>
              </div>
            </div>
            </template>
          </div>
        </div>
      </div>
    </div>
  `,
};
