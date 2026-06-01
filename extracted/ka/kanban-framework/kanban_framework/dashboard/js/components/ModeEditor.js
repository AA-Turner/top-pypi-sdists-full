import { ref, reactive, watch, computed } from 'vue';

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

    function startAdd() {
      editName.value = '';
      editPhases.splice(0, editPhases.length, ...['execute']);
    }

    function startEdit(name) {
      editName.value = name;
      editPhases.splice(0, editPhases.length, ...(customModes[name].phase_order || []));
    }

    function cancelEdit() {
      editName.value = '';
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

    function saveMode() {
      if (!editName.value.trim()) return;
      const name = editName.value.trim();
      customModes[name] = reactive({ phase_order: [...editPhases] });
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
      }
      for (const [n, cfg] of Object.entries(customModes)) {
        out[n] = { phase_order: [...cfg.phase_order] };
      }
      emit('update:modes', out);
    }

    return {
      PHASE_ORDER, PHASE_LABELS, BUILTIN_NAMES, BUILTIN_ORDERS,
      customModes, customNames, editName, editPhases,
      startAdd, startEdit, cancelEdit, togglePhase, movePhase, saveMode, deleteMode, editSteps,
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
      <div v-if="editPhases.length > 0" class="mode-edit-form">
        <div class="field-row">
          <label class="field-label">模式名称</label>
          <input type="text" v-model="editName" placeholder="如 review_only"
                 class="field-input" :disabled="!!customModes[editName]" />
        </div>
        <div class="field-row">
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
