// UI string catalog for the web IDE. Mirrors bingo/tui/i18n.py keys.
window.I18N = {
  en: {
    explorer: "EXPLORER", welcome: "Open a file, or ask the assistant.",
    tagline: "AI pentest workbench",
    q_explain: "Explain this project", q_script: "Write a helper script",
    q_scan: "Scan a target URL",
    tab_dev: "DEV", tab_pentest: "PENTEST", send: "Send", stop: "Stop",
    placeholder: "Ask, or paste a target URL…",
    ready: "ready", busy: "working…",
    scan: "Full scan", waf: "WAF test", copied: "Transcript copied.",
    empty_copy: "Nothing to copy.",
    settings: "Settings", commands: "Commands ( / )",
    set_model: "AI model", set_lang: "Language", set_mode: "Default mode",
    set_root: "Workspace", quit_hint: "Close the browser tab to quit.",
    saved_models: "Saved models", add_model: "Add model", add_model_btn: "Add",
    delete: "Delete", model_added: "Model added.",
    ph_api_key: "API key", ph_base_url: "Base URL (optional)",
    ph_model_name: "Model name (optional)", ph_alias: "Alias (optional)",
  },
  ko: {
    explorer: "탐색기", welcome: "파일을 열거나 어시스턴트에게 물어보세요.",
    tagline: "AI 침투 테스트 워크벤치",
    q_explain: "이 프로젝트 설명해줘", q_script: "헬퍼 스크립트 작성",
    q_scan: "대상 URL 스캔",
    tab_dev: "개발", tab_pentest: "침투", send: "전송", stop: "중지",
    placeholder: "질문하거나 대상 URL을 붙여넣으세요…",
    ready: "준비됨", busy: "처리 중…",
    scan: "전체 스캔", waf: "WAF 테스트", copied: "대화가 복사됐습니다.",
    empty_copy: "복사할 내용이 없습니다.",
    settings: "설정", commands: "명령 ( / )",
    set_model: "AI 모델", set_lang: "언어", set_mode: "기본 모드",
    set_root: "작업 폴더", quit_hint: "종료하려면 브라우저 탭을 닫으세요.",
    saved_models: "저장된 모델", add_model: "모델 추가", add_model_btn: "추가",
    delete: "삭제", model_added: "모델이 추가됐습니다.",
    ph_api_key: "API 키", ph_base_url: "Base URL (선택)",
    ph_model_name: "모델 이름 (선택)", ph_alias: "별칭 (선택)",
  },
  zh: {
    explorer: "资源管理器", welcome: "打开文件，或向助手提问。",
    tagline: "AI 渗透测试工作台",
    q_explain: "解释这个项目", q_script: "编写辅助脚本",
    q_scan: "扫描目标 URL",
    tab_dev: "开发", tab_pentest: "渗透", send: "发送", stop: "停止",
    placeholder: "提问，或粘贴目标 URL…",
    ready: "就绪", busy: "处理中…",
    scan: "全量扫描", waf: "WAF 测试", copied: "对话已复制。",
    empty_copy: "没有可复制的内容。",
    settings: "设置", commands: "命令 ( / )",
    set_model: "AI 模型", set_lang: "语言", set_mode: "默认模式",
    set_root: "工作目录", quit_hint: "关闭浏览器标签页即可退出。",
    saved_models: "已保存模型", add_model: "添加模型", add_model_btn: "添加",
    delete: "删除", model_added: "模型已添加。",
    ph_api_key: "API 密钥", ph_base_url: "Base URL (可选)",
    ph_model_name: "模型名称 (可选)", ph_alias: "别名 (可选)",
  },
};

window.t = function (key, lang) {
  lang = lang || (window.__BINGO__ && window.__BINGO__.lang) || "en";
  var tbl = window.I18N[lang] || window.I18N.en;
  return tbl[key] || window.I18N.en[key] || key;
};

window.applyI18n = function (lang) {
  document.querySelectorAll("[data-i18n]").forEach(function (el) {
    el.textContent = window.t(el.getAttribute("data-i18n"), lang);
  });
  document.querySelectorAll("[data-i18n-ph]").forEach(function (el) {
    el.setAttribute("placeholder", window.t(el.getAttribute("data-i18n-ph"), lang));
  });
  document.querySelectorAll("[data-i18n-title]").forEach(function (el) {
    el.setAttribute("title", window.t(el.getAttribute("data-i18n-title"), lang));
  });
};
