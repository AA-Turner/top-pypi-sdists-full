import { ref, reactive, watch, computed } from 'vue';

const PHASE_ORDER = ['plan', 'plan_review', 'qa_spec', 'spec_review', 'execute', 'evaluate', 'retrospective', 'archive'];
const PHASE_LABELS = {
  plan: '规划', plan_review: 'Plan 评审', qa_spec: '测试规格', spec_review: '规格评审',
  execute: '执行', evaluate: '评估', retrospective: '复盘', archive: '归档',
};

const ALL_CHECKS = [
  { id: 'knowledge_references', label: '知识引用检查', desc: '检查产物中是否有 K-NNN 格式的知识库引用' },
  { id: 'test_files', label: '测试文件检查', desc: '验证工作树中存在测试文件' },
  { id: 'tdd_evidence', label: 'TDD 证据检查', desc: '验证 execution_summary.md 的 TDD 证据表' },
  { id: 'test_spec_coverage', label: '测试规格覆盖率', desc: '检查 test_spec.md 中 UT-xxx 的实现覆盖率' },
  { id: 'knowledge_artifact', label: '知识产物检查', desc: '检查阶段知识产物（pitfalls / knowledge_extracted）' },
  { id: 'quick_scope', label: 'Quick 模式范围', desc: 'Quick 模式下的变更范围限制检查' },
];

const PHASE_DEFAULT_CHECKS = {
  plan: ['knowledge_references'],
  execute: ['test_files', 'tdd_evidence', 'test_spec_coverage', 'knowledge_artifact'],
  retrospective: ['knowledge_artifact'],
};

export const GuardEditor = {
  props: {
    phases: { type: Array, default: () => [] },
  },
  emits: ['update:guard'],
  setup(props, { emit }) {
    const phaseGuards = reactive({});

    function initGuards(phasesArr) {
      for (const pid of PHASE_ORDER) {
        let guard = { checks: [], quick_limits: {}, test_spec_coverage_threshold: 0.5 };
        if (phasesArr && Array.isArray(phasesArr)) {
          const p = phasesArr.find(ph => ph.id === pid);
          if (p && p.guard) {
            guard.checks = p.guard.checks || [];
            guard.quick_limits = { ...(p.guard.quick_limits || {}) };
            guard.test_spec_coverage_threshold = p.guard.test_spec_coverage_threshold ?? 0.5;
          }
        }
        if (guard.checks.length === 0 && PHASE_DEFAULT_CHECKS[pid]) {
          guard.checks = [...PHASE_DEFAULT_CHECKS[pid]];
        }
        phaseGuards[pid] = reactive(guard);
      }
    }

    initGuards(props.phases);
    watch(() => props.phases, (v) => initGuards(v), { deep: true });

    const phaseList = computed(() => {
      if (props.phases && props.phases.length > 0) {
        return props.phases.map(p => p.id || p).filter(Boolean);
      }
      return PHASE_ORDER;
    });

    function toggleCheck(phaseId, checkId) {
      const g = phaseGuards[phaseId];
      const idx = g.checks.indexOf(checkId);
      if (idx >= 0) g.checks.splice(idx, 1);
      else g.checks.push(checkId);
      emitGuard(phaseId);
    }

    function emitGuard(phaseId) {
      const g = phaseGuards[phaseId];
      const out = { checks: [...g.checks] };
      if (g.quick_limits && Object.values(g.quick_limits).some(v => v)) {
        out.quick_limits = { ...g.quick_limits };
      }
      if (g.test_spec_coverage_threshold !== 0.5) {
        out.test_spec_coverage_threshold = g.test_spec_coverage_threshold;
      }
      emit('update:guard', { phaseId, guard: out });
    }

    function onLimitChange(phaseId) {
      emitGuard(phaseId);
    }

    return {
      PHASE_ORDER, PHASE_LABELS, ALL_CHECKS,
      phaseGuards, phaseList,
      toggleCheck, onLimitChange, emitGuard,
    };
  },
  template: `
    <div class="guard-editor">
      <div class="guard-editor-header">
        <h3>Guard 检查配置</h3>
      </div>
      <p class="step-editor-hint">
        配置各阶段的 Guard 检查项。取消勾选可禁用某项检查，空列表则只做 artifact 文件存在性验证。
      </p>

      <div class="guard-list">
        <div v-for="pid in phaseList" :key="pid" class="guard-phase-card">
          <div class="guard-phase-header">
            <span class="guard-phase-title">{{ PHASE_LABELS[pid] || pid }}</span>
            <span class="guard-phase-badge">{{ pid }}</span>
            <span v-if="phaseGuards[pid]" class="guard-check-count">
              {{ phaseGuards[pid].checks.length }} checks
            </span>
          </div>
          <div class="guard-checks" v-if="phaseGuards[pid]">
            <label v-for="chk in ALL_CHECKS" :key="chk.id" class="guard-check-item"
                   :title="chk.desc">
              <input type="checkbox"
                     :checked="phaseGuards[pid].checks.includes(chk.id)"
                     @change="toggleCheck(pid, chk.id)" />
              <span class="guard-check-label">{{ chk.label }}</span>
            </label>
          </div>
          <div class="guard-params" v-if="pid === 'execute' && phaseGuards[pid]">
            <div class="field-row">
              <label class="field-label">Quick 文件上限</label>
              <input type="number" v-model.number="phaseGuards[pid].quick_limits.max_files"
                     min="1" max="20" class="field-input field-input-number" @change="onLimitChange(pid)" />
            </div>
            <div class="field-row">
              <label class="field-label">Quick 行数上限</label>
              <input type="number" v-model.number="phaseGuards[pid].quick_limits.max_total_lines"
                     min="10" max="200" class="field-input field-input-number" @change="onLimitChange(pid)" />
            </div>
            <div class="field-row">
              <label class="field-label">Quick 新增行上限</label>
              <input type="number" v-model.number="phaseGuards[pid].quick_limits.max_added_lines"
                     min="5" max="100" class="field-input field-input-number" @change="onLimitChange(pid)" />
            </div>
            <div class="field-row">
              <label class="field-label">覆盖率阈值</label>
              <div class="slider-control">
                <input type="range" v-model.number="phaseGuards[pid].test_spec_coverage_threshold"
                       min="0" max="1" step="0.1" class="field-slider" @input="onLimitChange(pid)" />
                <span class="slider-value">{{ (phaseGuards[pid].test_spec_coverage_threshold * 100).toFixed(0) }}%</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  `,
};
