import { ref, reactive, watch, onMounted, computed } from 'vue';
import { api } from '../utils/api.js';

const PHASE_ORDER = ['plan', 'plan_review', 'qa_spec', 'spec_review', 'execute', 'evaluate', 'retrospective', 'user_decision', 'archive'];
const PHASE_LABELS = {
  plan: '规划', plan_review: 'Plan 评审', qa_spec: '测试规格', spec_review: '规格评审',
  execute: '执行', evaluate: '评估', retrospective: '复盘', user_decision: '用户决策', archive: '归档',
};

function newStep(phase = 'execute', source = 'extension') {
  const tempId = '_new_' + Date.now();
  return {
    phase,
    insert_after: '',
    source,
    step: {
      id: tempId,
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
    const pendingDelete = ref(null);  // { step, index, timer } — soft delete with undo
    const showPalette = ref(false);  // toggle builtin step palette for reuse
    const paletteSearch = ref('');   // search filter within palette
    const selectedIndex = ref(null); // currently selected step for detail panel
    const detailTab = ref('basic');   // 'basic' | 'prompt' | 'advanced'

    // Critical steps that keep the workflow functional if not removed
    const _CRITICAL = new Set([
      'plan.plan_B',
      'execute.spawn', 'execute.verify',
      'evaluate.spawn', 'evaluate.collect_score', 'evaluate.collect_scores',
      'archive.guard',
    ]);
    function isCriticalStep(stepId) { return _CRITICAL.has(stepId); }

    function selectStep(globalIndex) {
      selectedIndex.value = globalIndex;
      detailTab.value = 'basic';
    }

    function closeDetail() {
      selectedIndex.value = null;
    }

    function initSteps(phasesArr, ext, defs) {
      steps.splice(0, steps.length);
      const hasPhases = phasesArr && Array.isArray(phasesArr) && phasesArr.length > 0;
      if (hasPhases) {
        // Phases are configured (may have empty steps) — show them directly
        for (const p of phasesArr) {
          if (p.steps && Array.isArray(p.steps)) {
            for (const s of p.steps) {
              steps.push({ phase: p.id, insert_after: '', source: 'builtin',
                step: { ...s } });
            }
          }
        }
      } else if (defs && typeof defs === 'object') {
        // No phases configured — load built-in defs for builtin modes
        const BUILTIN_MODES = new Set(['full', 'lightweight', 'quick']);
        const isBuiltinMode = props.modeName && BUILTIN_MODES.has(props.modeName);
        if (isBuiltinMode) {
          // Builtin mode: show all built-in steps
          for (const [key, val] of Object.entries(defs)) {
            if (typeof val === 'object' && val !== null && !val.description) {
              if (!modePhases.has(key)) continue;
              for (const [stepId, info] of Object.entries(val)) {
                if (!info || typeof info.description !== 'string') continue;
                steps.push({
                  phase: key, insert_after: '', source: 'builtin',
                  step: { id: stepId, description: info.description || '',
                          agent_type: info.agent_type || '' },
                });
              }
            } else if (val && typeof val === 'object' && typeof val.description === 'string') {
              const dotIdx = key.indexOf('.');
              const phaseId = dotIdx > 0 ? key.substring(0, dotIdx) : '';
              if (!phaseId || !modePhases.has(phaseId)) continue;
              steps.push({
                phase: phaseId, insert_after: '', source: 'builtin',
                step: { id: key, description: val.description || '',
                        agent_type: val.agent_type || '' },
              });
            }
          }
        }
        // Custom mode: stay empty, user picks from builtin palette
      }
      // Load extension steps
      const raw = (ext && ext.add_steps) || [];
      for (const item of raw) {
        steps.push(JSON.parse(JSON.stringify({ ...item, source: 'extension' })));
      }
    }

    onMounted(async () => {
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
      initSteps(props.phases, props.extensions, stepDefs.value);
    });

    watch(() => [props.phases, props.extensions], () => {
      initSteps(props.phases, props.extensions, stepDefs.value);
    }, { deep: true });

    const phaseList = computed(() => {
      // Phases relevant to the current editing context
      if (props.phases && props.phases.length > 0) {
        return props.phases.map(p => p.id || p).filter(Boolean);
      }
      return PHASE_ORDER;
    });

    const filteredSteps = computed(() => {
      let list = steps.map((s, i) => ({ step: s, index: i }));
      if (viewMode.value === 'builtin') list = list.filter(({ step }) => step.source === 'builtin');
      else if (viewMode.value === 'extension') list = list.filter(({ step }) => step.source === 'extension');
      if (filterPhase.value !== 'all') list = list.filter(({ step }) => step.phase === filterPhase.value);
      return list;
    });

    // Builtin step palette: reusable system steps for custom modes
    const builtinPalette = computed(() => {
      const defs = stepDefs.value;
      if (!defs || typeof defs !== 'object') return [];
      const existing = new Set(steps.map(s => s.step.id));
      const phaseOrder = (props.phases || []).map(p => p.id || p);
      const modePhases = new Set(phaseOrder.length > 0 ? phaseOrder : []);
      const result = [];
      for (const [key, val] of Object.entries(defs)) {
        if (typeof val === 'object' && val !== null && !val.description) {
          if (modePhases.size > 0 && !modePhases.has(key)) continue;
          if (filterPhase.value !== 'all' && key !== filterPhase.value) continue;
          for (const [stepId, info] of Object.entries(val)) {
            if (!existing.has(stepId) && info && typeof info.description === 'string') {
              result.push({ id: stepId, phase: key, description: info.description });
            }
          }
        } else if (val && typeof val === 'object' && typeof val.description === 'string') {
          const dotIdx = key.indexOf('.');
          const phaseId = dotIdx > 0 ? key.substring(0, dotIdx) : '';
          if (modePhases.size > 0 && !modePhases.has(phaseId)) continue;
          if (filterPhase.value !== 'all' && phaseId !== filterPhase.value) continue;
          if (!existing.has(key)) {
            result.push({ id: key, phase: phaseId, description: val.description });
          }
        }
      }
      // Apply search filter
      if (paletteSearch.value.trim()) {
        const q = paletteSearch.value.trim().toLowerCase();
        return result.filter(item =>
          item.id.toLowerCase().includes(q) ||
          item.description.toLowerCase().includes(q)
        );
      }
      return result;
    });

    function cloneBuiltinStep(stepId, phase) {
      const defs = stepDefs.value;
      const dotted = stepId.includes('.') ? stepId : `${phase}.${stepId}`;
      let info = null;
      // Try nested then flat
      if (defs[phase] && defs[phase] && defs[phase][stepId]) {
        info = defs[phase][stepId];
      } else if (defs[stepId]) {
        info = defs[stepId];
      } else if (defs[dotted]) {
        info = defs[dotted];
      }
      const stepData = {
        id: stepId,
        description: (info && info.description) || '',
        agent_type: (info && info.agent_type) || '',
      };
      if (info && info.spawn_prompt) stepData.spawn_prompt = info.spawn_prompt;
      if (info && info.actions) stepData.actions = [...info.actions];
      if (info && info.after) stepData.after = [...info.after];
      if (info && info.type) stepData.type = info.type;
      if (info && info.parallel) stepData.parallel = true;
      if (info && info.user_action) stepData.user_action = true;
      if (info && info.interactive) stepData.interactive = true;
      if (info && info.guard) stepData.guard = { ...info.guard };
      if (info && info.required_artifacts) stepData.required_artifacts = [...info.required_artifacts];
      steps.push({ phase, insert_after: '', source: 'builtin', step: stepData });
      showPalette.value = false;
      emitAll();
    }

    function addStep(source) {
      // Pick phase: current filter, or first phase in the mode, or 'execute'
      let phase = filterPhase.value !== 'all' ? filterPhase.value : 'execute';
      if (filterPhase.value === 'all') {
        const phasesWithSteps = new Set(steps.map(s => s.phase));
        // Try to use the first phase from the mode's phase_order
        for (const p of (props.phases || [])) {
          const pid = p.id || p;
          if (pid && pid !== 'all') { phase = pid; break; }
        }
      }
      steps.push(newStep(phase, source));
      emitAll();
    }

    function removeStep(globalIndex) {
      const step = steps[globalIndex];
      if (!step) return;
      // Soft-delete with 5s undo window
      if (pendingDelete.value) {
        clearTimeout(pendingDelete.value.timer);
        commitDelete();
      }
      steps.splice(globalIndex, 1);
      pendingDelete.value = { step, index: globalIndex, timer: setTimeout(() => {
        pendingDelete.value = null;
        emitAll();
      }, 5000) };
      emitAll();
    }

    function undoDelete() {
      if (!pendingDelete.value) return;
      clearTimeout(pendingDelete.value.timer);
      steps.splice(pendingDelete.value.index, 0, pendingDelete.value.step);
      pendingDelete.value = null;
      emitAll();
    }

    function commitDelete() {
      pendingDelete.value = null;
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
      steps, stepDefs, agentTypes, filterPhase, viewMode, tagInput, phaseList,
      filteredSteps, builtinCount, extCount,
      addStep, removeStep, moveStep, getAfterOptions, undoDelete, pendingDelete,
      addArtifact, removeArtifact, emitAll, showAdvanced, builtinPalette, showPalette, paletteSearch, cloneBuiltinStep,
      selectedIndex, selectStep, closeDetail, detailTab, isCriticalStep,
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
          <button class="btn btn-primary btn-sm" @click="addStep(viewMode === 'extension' ? 'extension' : 'builtin')">+ 新建步骤</button>
          <div class="step-palette-dropdown" v-if="builtinPalette.length > 0">
            <button class="btn btn-secondary btn-sm" @click="showPalette = !showPalette; paletteSearch = ''">📋 复用内置步骤 ({{ builtinPalette.length }})</button>
            <div class="step-palette-menu" v-if="showPalette">
              <div class="step-palette-search">
                <input type="text" v-model="paletteSearch" placeholder="搜索步骤名称或描述..."
                       class="field-input" style="width:100%;margin-bottom:6px;font-size:0.8rem" />
              </div>
              <button v-for="item in builtinPalette" :key="item.id"
                      class="step-palette-item"
                      @click="cloneBuiltinStep(item.id, item.phase); showPalette = false">
                <span class="step-palette-id">{{ item.id }}</span>
                <span class="step-palette-desc">{{ item.description }}</span>
              </button>
            </div>
          </div>
        </div>
      </div>

      <div class="step-phase-tabs">
        <a class="step-phase-tab" :class="{ active: filterPhase === 'all' }"
           @click="filterPhase = 'all'">全部 ({{ steps.length }})</a>
        <a v-for="pid in phaseList" :key="pid"
           class="step-phase-tab" :class="{ active: filterPhase === pid }"
           @click="filterPhase = pid">
          {{ PHASE_LABELS[pid] || pid }}
          ({{ steps.filter(s => s.phase === pid).length }})
        </a>
      </div>

      <div v-if="pendingDelete" class="step-undo-toast">
        已删除步骤 {{ pendingDelete.step.step.id }}
        <button class="btn btn-sm btn-primary" @click="undoDelete">撤销</button>
      </div>
      <div v-if="filteredSteps.length === 0" class="step-empty">
        <span v-if="steps.length === 0">暂无步骤，点击上方按钮添加</span>
        <span v-else>该阶段下暂无步骤</span>
      </div>

      <div class="step-editor-split" :class="{ 'has-detail': selectedIndex !== null }">
        <!-- Left: compact step list -->
        <div class="step-list-panel">
          <div class="step-list">
            <div v-for="{ step: item, index } in filteredSteps" :key="index"
                 class="step-row" :class="{ 'step-row-active': selectedIndex === index, 'step-row-builtin': item.source === 'builtin', 'step-row-critical': isCriticalStep(item.step.id) }"
                 @click="selectStep(index)">
              <span class="step-row-id">{{ item.step.id || '未命名' }}</span>
              <span class="step-row-critical-badge" v-if="isCriticalStep(item.step.id)" title="关键步骤，建议保留">⚷</span>
              <span class="step-row-phase">{{ PHASE_LABELS[item.phase] || item.phase }}</span>
              <span class="step-row-desc">{{ item.step.description }}</span>
              <span class="step-row-source" :class="'source-' + item.source">
                {{ item.source === 'builtin' ? '内置' : '扩展' }}
              </span>
              <button class="btn btn-icon btn-sm" @click.stop="moveStep(index, -1)" title="上移">↑</button>
              <button class="btn btn-icon btn-sm" @click.stop="moveStep(index, 1)" title="下移">↓</button>
              <button class="btn btn-icon btn-danger btn-sm" @click.stop="removeStep(index)" title="删除">×</button>
            </div>
          </div>
        </div>

        <!-- Right: detail editor or placeholder -->
        <div class="step-detail-panel" v-if="selectedIndex !== null">
          <div class="step-detail-header">
            <div class="step-detail-tabs">
              <button class="step-detail-tab" :class="{ active: detailTab === 'basic' }" @click="detailTab = 'basic'">基础</button>
              <button class="step-detail-tab" :class="{ active: detailTab === 'prompt' }" @click="detailTab = 'prompt'">Prompt</button>
              <button class="step-detail-tab" :class="{ active: detailTab === 'advanced' }" @click="detailTab = 'advanced'">高级</button>
            </div>
            <button class="btn btn-icon btn-sm" @click="closeDetail" title="关闭">×</button>
          </div>
          <template v-if="steps[selectedIndex]">
          <!-- BASIC TAB -->
          <div class="step-detail-body" v-show="detailTab === 'basic'">
            <div class="detail-field">
              <label class="detail-label">ID</label>
              <input type="text" v-model="steps[selectedIndex].step.id" placeholder="步骤 ID"
                     class="field-input step-id-input" @input="emitAll" />
            </div>
            <div class="detail-field">
              <label class="detail-label">描述</label>
              <input type="text" v-model="steps[selectedIndex].step.description" placeholder="步骤描述"
                     class="field-input" @input="emitAll" />
            </div>
            <div class="detail-row">
              <div class="detail-field detail-half">
                <label class="detail-label">阶段</label>
                <select v-model="steps[selectedIndex].phase" class="field-select" @change="emitAll">
                  <option v-for="pid in phaseList" :key="pid" :value="pid">{{ PHASE_LABELS[pid] || pid }}</option>
                </select>
              </div>
              <div class="detail-field detail-half">
                <label class="detail-label">Agent</label>
                <select v-model="steps[selectedIndex].step.agent_type" class="field-select" @change="emitAll">
                  <option value="">无</option>
                  <option v-for="at in agentTypes" :key="at" :value="at">{{ at }}</option>
                  <option value="__custom__">自定义...</option>
                </select>
                <input v-if="steps[selectedIndex].step.agent_type === '__custom__'" type="text"
                       v-model="steps[selectedIndex].step.agent_type" placeholder="自定义"
                       class="field-input" style="margin-top:4px" @input="emitAll" />
              </div>
            </div>
            <div class="detail-field" v-if="steps[selectedIndex].source === 'extension'">
              <label class="detail-label">插入位置</label>
              <select v-model="steps[selectedIndex].insert_after" class="field-select" @change="emitAll">
                <option v-for="opt in getAfterOptions(steps[selectedIndex].phase)" :key="opt.value" :value="opt.value">{{ opt.label }}</option>
              </select>
            </div>
            <div class="detail-field" v-if="steps[selectedIndex].step.actions && steps[selectedIndex].step.actions.length">
              <label class="detail-label">Actions <span class="detail-count">{{ steps[selectedIndex].step.actions.length }}</span></label>
              <div class="detail-code-block">
                <div v-for="(act, ai) in steps[selectedIndex].step.actions" :key="ai" class="detail-code-line">
                  <span class="detail-code-num">{{ ai + 1 }}</span><code>{{ act }}</code>
                </div>
              </div>
            </div>
          </div>
          <!-- PROMPT TAB -->
          <div class="step-detail-body" v-show="detailTab === 'prompt'">
            <div class="detail-field">
              <label class="detail-label">spawn_prompt</label>
              <textarea v-model="steps[selectedIndex].step.spawn_prompt" placeholder="告诉 Agent 要做什么..."
                        class="detail-prompt-area" rows="10" @input="emitAll"></textarea>
            </div>
          </div>
          <!-- ADVANCED TAB -->
          <div class="step-detail-body" v-show="detailTab === 'advanced'">
            <div class="detail-field">
              <label class="detail-label">依赖 (after)</label>
              <input type="text" :value="(steps[selectedIndex].step.after || []).join(', ')"
                     placeholder="step_id, ... (逗号分隔)" class="field-input"
                     @input="steps[selectedIndex].step.after = $event.target.value.split(',').map(s=>s.trim()).filter(Boolean); emitAll()" />
            </div>
            <div class="detail-toggles">
              <label class="detail-toggle">
                <input type="checkbox" v-model="steps[selectedIndex].step.parallel" @change="emitAll" />
                <span class="detail-toggle-mark"></span>
                并行执行
              </label>
              <label class="detail-toggle">
                <input type="checkbox" v-model="steps[selectedIndex].step.user_action" @change="emitAll" />
                <span class="detail-toggle-mark"></span>
                需用户操作
              </label>
              <label class="detail-toggle">
                <input type="checkbox" v-model="steps[selectedIndex].step.interactive" @change="emitAll" />
                <span class="detail-toggle-mark"></span>
                交互式
              </label>
            </div>
            <div class="detail-field">
              <label class="detail-label">产物验证</label>
              <div class="tag-input-group">
                <div class="tag-list">
                  <span v-for="(art, ai) in (steps[selectedIndex].step.required_artifacts || [])" :key="ai" class="tag">{{ art }}<button class="tag-remove" @click="removeArtifact(selectedIndex, ai)">×</button></span>
                </div>
                <div class="tag-input-row">
                  <input type="text" v-model="tagInput[selectedIndex]" placeholder="文件名 (如 report.json)"
                         class="field-input tag-field" @keydown.enter.prevent="addArtifact(selectedIndex)" />
                  <button class="btn btn-secondary btn-sm" @click="addArtifact(selectedIndex)">添加</button>
                </div>
              </div>
            </div>
          </div>
          </template>
          <div v-else class="step-empty">步骤不存在</div>
        </div>
        <div class="step-detail-panel step-detail-placeholder" v-else-if="steps.length > 0">
          <div class="step-empty">← 点击左侧步骤查看和编辑详细配置</div>
        </div>
      </div>
    </div>
  `,
};
