import { ref, reactive, watch, computed } from 'vue';
import { api } from '../utils/api.js';

const PHASE_ORDER = ['plan', 'plan_review', 'qa_spec', 'spec_review', 'execute', 'evaluate', 'retrospective', 'user_decision', 'archive'];
const PHASE_LABELS = {
  plan: '规划', plan_review: 'Plan 评审', qa_spec: '测试规格', spec_review: '规格评审',
  execute: '执行', evaluate: '评估', retrospective: '复盘', user_decision: '用户决策', archive: '归档',
};
const BUILTIN_NAMES = ['full', 'lightweight', 'quick'];
const BUILTIN_ORDERS = {
  full:        ['plan', 'plan_review', 'qa_spec', 'spec_review', 'execute', 'evaluate', 'retrospective', 'user_decision', 'archive'],
  lightweight: ['plan', 'execute', 'evaluate', 'user_decision', 'archive'],
  quick:       ['execute', 'user_decision', 'archive'],
};

export const ModeEditor = {
  props: {
    modes: { type: Object, default: () => ({}) },
  },
  emits: ['update:modes', 'edit-steps'],
  setup(props, { emit }) {
    const customModes = reactive({});
    const editName = ref('');
    const editPhases = reactive([]);

    function initModes(m) {
      Object.keys(customModes).forEach(k => delete customModes[k]);
      if (m && typeof m === 'object') {
        for (const [name, cfg] of Object.entries(m)) {
          if (!BUILTIN_NAMES.includes(name)) {
            const phases = cfg.phase_order || [];
            customModes[name] = reactive({ phase_order: [...phases] });
          }
        }
      }
    }

    initModes(props.modes);
    watch(() => props.modes, v => initModes(v));

    const customNames = computed(() => Object.keys(customModes));
    const editTemplate = ref('');
    const isNewMode = computed(() => !editName.value || !customModes[editName.value]);

    const availableTemplates = computed(() => {
      const names = [...BUILTIN_NAMES];
      if (props.modes && typeof props.modes === 'object') {
        for (const [n, cfg] of Object.entries(props.modes)) {
          if (cfg && cfg.phase_order && !names.includes(n)) names.push(n);
        }
      }
      return names;
    });

    function startAdd() {
      editName.value = '';
      editTemplate.value = 'lightweight';  // sensible default
      // Apply lightweight template immediately
      editPhases.splice(0, editPhases.length, ...BUILTIN_ORDERS['lightweight']);
    }

    function applyTemplate(templateName) {
      if (!templateName) {
        editPhases.splice(0, editPhases.length);
        return;
      }
      editTemplate.value = templateName;
      // Copy phase_order from the template mode
      const modes = props.modes || {};
      const cfg = modes[templateName];
      if (cfg && cfg.phase_order) {
        editPhases.splice(0, editPhases.length, ...cfg.phase_order);
      } else if (BUILTIN_ORDERS[templateName]) {
        editPhases.splice(0, editPhases.length, ...BUILTIN_ORDERS[templateName]);
      }
    }

    function startEdit(name) {
      editName.value = name;
      editTemplate.value = '';
      editPhases.splice(0, editPhases.length, ...(customModes[name].phase_order || []));
    }

    function cancelEdit() {
      editName.value = '';
      editTemplate.value = '';
      editPhases.splice(0, editPhases.length);
    }

    function togglePhase(phaseId) {
      const idx = editPhases.indexOf(phaseId);
      if (idx >= 0) editPhases.splice(idx, 1);
      else editPhases.push(phaseId);
    }

    function movePhase(index, dir) {
      const t = index + dir;
      if (t < 0 || t >= editPhases.length) return;
      const tmp = editPhases[index];
      editPhases[index] = editPhases[t];
      editPhases[t] = tmp;
    }

    async function saveMode() {
      if (!editName.value.trim()) return;
      const name = editName.value.trim();
      const modeData = { phase_order: [...editPhases] };
      // Copy phases (steps) from template if selected
      if (editTemplate.value) {
        let tplPhases = null;
        const tplCfg = (props.modes || {})[editTemplate.value];
        if (tplCfg && tplCfg.phases && tplCfg.phases.length > 0) {
          tplPhases = tplCfg.phases;
        } else {
          // Fallback: fetch step definitions from API and build phases
          try {
            const data = await api.getStepDefinitions();
            const defs = (data && data.steps) || {};
            tplPhases = [];
            for (const pid of editPhases) {
              const phaseSteps = defs[pid];
              if (phaseSteps && typeof phaseSteps === 'object') {
                const steps = Object.entries(phaseSteps).map(([stepId, info]) => ({
                  id: stepId,
                  description: info.description || '',
                  agent_type: info.agent_type || '',
                  spawn_prompt: info.spawn_prompt || '',
                  actions: info.actions || [],
                  ...(info.after ? { after: info.after } : {}),
                  ...(info.parallel ? { parallel: true } : {}),
                  ...(info.user_action ? { user_action: true } : {}),
                  ...(info.interactive ? { interactive: true } : {}),
                  ...(info.type && info.type !== 'action' ? { type: info.type } : {}),
                }));
                tplPhases.push({ id: pid, steps });
              }
            }
          } catch (_) {
            tplPhases = [];
          }
        }
        if (tplPhases && tplPhases.length > 0) {
          modeData.phases = JSON.parse(JSON.stringify(tplPhases));
        }
      }
      customModes[name] = reactive(modeData);
      cancelEdit();
      emitModes();
    }

    function deleteMode(name) {
      delete customModes[name];
      emitModes();
    }

    function editSteps(modeName) {
      emit('edit-steps', modeName);
    }

    function emitModes() {
      const out = {};
      for (const n of BUILTIN_NAMES) {
        out[n] = { phase_order: [...BUILTIN_ORDERS[n]] };
        // Preserve any phases/steps configured via StepEditor
        if (props.modes && props.modes[n] && props.modes[n].phases) {
          out[n].phases = props.modes[n].phases;
        }
      }
      for (const [n, cfg] of Object.entries(customModes)) {
        out[n] = { phase_order: [...cfg.phase_order] };
        // Preserve phases from customModes (e.g. from template), then from existing workflow
        if (cfg.phases && cfg.phases.length > 0) {
          out[n].phases = cfg.phases;
        } else if (props.modes && props.modes[n] && props.modes[n].phases) {
          out[n].phases = props.modes[n].phases;
        }
      }
      emit('update:modes', out);
    }

    return {
      PHASE_ORDER, PHASE_LABELS, BUILTIN_NAMES, BUILTIN_ORDERS,
      customModes, customNames, editName, editPhases, editTemplate, availableTemplates, isNewMode,
      startAdd, startEdit, cancelEdit, togglePhase, movePhase, applyTemplate, saveMode, deleteMode, editSteps,
    };
  },
  template: `
    <div class="mode-editor">
      <div class="mode-editor-header">
        <h3>模式编辑器</h3>
        <button v-if="!editName && editPhases.length === 0" class="btn btn-primary btn-sm" @click="startAdd">+ 添加模式</button>
      </div>
      <p class="step-editor-hint">
        内置模式（full/lightweight/quick）始终可用，不可删除。自定义模式通过 <code>kanban run --mode &lt;name&gt;</code> 使用。
      </p>

      <!-- Edit form -->
      <div v-if="editPhases.length > 0 || editName !== '' || editTemplate" class="mode-edit-form">
        <div class="field-row">
          <label class="field-label">模式名称</label>
          <input type="text" v-model="editName" placeholder="如 review_only"
                 class="field-input" :disabled="!!customModes[editName]" />
        </div>
        <div class="field-row" v-if="!editTemplate && isNewMode">
          <label class="field-label">基于模板创建 (可选)</label>
          <select v-model="editTemplate" class="field-select" @change="applyTemplate(editTemplate)">
            <option value="">空白创建</option>
            <option v-for="tpl in availableTemplates" :key="tpl" :value="tpl">{{ tpl }}</option>
          </select>
        </div>
        <div class="field-row" v-if="editTemplate">
          <label class="field-label">模板</label>
          <span class="mode-template-badge">{{ editTemplate }}</span>
          <button class="btn btn-sm btn-secondary" @click="editTemplate = ''; editPhases.splice(0, editPhases.length)">✕ 取消模板</button>
        </div>
        <div class="field-row" v-if="editPhases.length > 0">
          <label class="field-label">阶段序列</label>
          <div class="mode-phase-order">
            <div v-for="(pid, idx) in editPhases" :key="pid" class="mode-phase-chip">
              <span>{{ PHASE_LABELS[pid] || pid }}</span>
              <button class="btn btn-icon btn-sm" @click="movePhase(idx, -1)" :disabled="idx === 0">↑</button>
              <button class="btn btn-icon btn-sm" @click="movePhase(idx, 1)" :disabled="idx === editPhases.length - 1">↓</button>
              <button class="btn btn-icon btn-danger btn-sm" @click="togglePhase(pid)">×</button>
            </div>
          </div>
        </div>
        <div class="field-row">
          <label class="field-label">可选阶段</label>
          <div class="mode-available-phases">
            <button v-for="pid in PHASE_ORDER" :key="pid"
                    class="btn btn-sm" :class="editPhases.includes(pid) ? 'btn-primary' : 'btn-secondary'"
                    :disabled="editPhases.includes(pid)"
                    @click="togglePhase(pid)">
              {{ PHASE_LABELS[pid] || pid }}
            </button>
          </div>
        </div>
        <div class="mode-edit-actions">
          <button class="btn btn-primary btn-sm" @click="saveMode" :disabled="!editName.trim() || editPhases.length === 0">保存模式</button>
          <button class="btn btn-secondary btn-sm" @click="cancelEdit">取消</button>
        </div>
      </div>

      <!-- Builtin modes (read-only) -->
      <div class="mode-list">
        <div v-for="name in BUILTIN_NAMES" :key="name" class="mode-card mode-card-builtin">
          <div class="mode-card-header">
            <span class="mode-card-name">{{ name }}</span>
            <span class="step-card-source-badge source-builtin">内置</span>
            <button class="btn btn-secondary btn-sm" @click="editSteps(name)" title="编辑步骤">⚙ 步骤</button>
          </div>
          <div class="mode-card-order">
            <span v-for="(pid, i) in BUILTIN_ORDERS[name]" :key="pid" class="mode-phase-label">
              {{ PHASE_LABELS[pid] || pid }}<span v-if="i < BUILTIN_ORDERS[name].length - 1"> →</span>
            </span>
          </div>
        </div>

        <!-- Custom modes -->
        <div v-for="name in customNames" :key="name" class="mode-card mode-card-custom">
          <div class="mode-card-header">
            <span class="mode-card-name">{{ name }}</span>
            <span class="step-card-source-badge source-extension">自定义</span>
            <button class="btn btn-secondary btn-sm" @click="editSteps(name)" title="编辑步骤">⚙ 步骤</button>
            <button class="btn btn-icon btn-sm" @click="startEdit(name)" title="编辑">✎</button>
            <button class="btn btn-icon btn-danger btn-sm" @click="deleteMode(name)" title="删除">×</button>
          </div>
          <div class="mode-card-order">
            <span v-for="(pid, i) in (customModes[name] && customModes[name].phase_order || [])" :key="pid" class="mode-phase-label">
              {{ PHASE_LABELS[pid] || pid }}<span v-if="i < (customModes[name]?.phase_order?.length || 0) - 1"> →</span>
            </span>
          </div>
        </div>
      </div>

      <div v-if="customNames.length === 0 && editPhases.length === 0" class="step-empty">
        暂无自定义模式，点击上方按钮添加
      </div>
    </div>
  `,
};
