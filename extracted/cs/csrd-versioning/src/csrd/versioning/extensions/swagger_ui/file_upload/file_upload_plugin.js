// ── File Upload Examples Plugin ──
// Swagger UI omits the examples dropdown for multipart/form-data request
// bodies. This plugin wraps the RequestBody component to render an example
// selector dropdown, descriptions, and a read-only preview (pre-click) or
// editable form (post-click) — all within React's render cycle so state
// survives re-renders without MutationObserver hacks.

function FileUploadExamplesPlugin() {
  // Per-operation state survives React unmount/remount via closure.
  // Keyed by specPath so each request body gets independent tracking.
  const _state = {};
  function _getState(key) {
    if (!_state[key]) _state[key] = { selected: null, modifiedSnapshot: null };
    return _state[key];
  }

  const toJS = (v) => v && typeof v.toJS === 'function' ? v.toJS() : v;

  function sortedValue(ex) {
    const raw = typeof ex.value === 'object' ? Object.values(ex.value)[0] : ex.value;
    try {
      const parsed = JSON.parse(typeof raw === 'string' ? raw : JSON.stringify(raw));
      const sortKeys = (obj) => {
        if (Array.isArray(obj)) return obj.map(sortKeys);
        if (obj && typeof obj === 'object') {
          return Object.fromEntries(
            Object.entries(obj).sort(([a], [b]) => a.localeCompare(b)).map(([k, v]) => [k, sortKeys(v)])
          );
        }
        return obj;
      };
      return JSON.stringify(sortKeys(parsed), null, 2);
    } catch {
      return typeof raw === 'string' ? raw : JSON.stringify(raw, null, 2);
    }
  }

  return {
    wrapComponents: {
      // Swagger UI 5.x only renders <input type="file"> for format:binary,
      // but OpenAPI 3.1 (FastAPI) uses contentMediaType instead.  This
      // wrapper bridges the gap so file inputs render without patching
      // the schema (which would show "($binary)" in the type annotation).
      JsonSchema_string: (Original, system) => {
        const React = system.React;
        const h = React.createElement;
        return function ContentMediaTypeFileInput(props) {
          const { schema, getComponent, errors, onChange } = props;
          const contentMediaType = schema && schema.get ? schema.get('contentMediaType') : null;
          const type = schema && schema.get ? schema.get('type') : null;
          const format = schema && schema.get ? schema.get('format') : null;
          if (type === 'string' && contentMediaType === 'application/octet-stream' && !format) {
            const Input = getComponent('Input');
            return h(Input, {
              type: 'file',
              className: errors && errors.length ? 'invalid' : '',
              title: errors && errors.length ? errors : '',
              onChange: (e) => onChange(e.target.files[0]),
              disabled: props.isDisabled
            });
          }
          return h(Original, props);
        };
      },
      RequestBody: (Original, system) => {
        const React = system.React;
        const h = React.createElement;

        return function MultipartRequestBody(props) {
          const { requestBody, contentType, isExecute, specPath } = props;

          // ── Guard: only enhance multipart/form-data with examples ──
          let examples = null;
          let schemaName = null;
          let inlineSchema = null;

          // Helper: find the JSON body property (the non-file property with a $ref)
          const findBodyProp = (properties) => {
            if (!properties) return null;
            for (const [key, val] of Object.entries(properties)) {
              if (key === 'file') continue;
              if (val?.$ref || val?.allOf) return val;
            }
            return null;
          };

          // Helper: try to resolve the requestBody schema name from the multipart schema
          const resolveSchema = (mp, specJson) => {
            const schemaRef = mp.schema?.$ref;
            if (schemaRef) {
              const bodySchemaName = schemaRef.split('/').pop();
              const bodySchema = specJson?.components?.schemas?.[bodySchemaName];
              const rbProp = findBodyProp(bodySchema?.properties);
              if (rbProp?.$ref) return rbProp.$ref.split('/').pop();
            }
            // Resolved/inlined: schema.properties may have $ref or allOf
            const rbProp = findBodyProp(mp.schema?.properties);
            if (rbProp?.$ref) return rbProp.$ref.split('/').pop();
            if (rbProp?.allOf) {
              const ref = rbProp.allOf.find(a => a.$ref);
              if (ref) return ref.$ref.split('/').pop();
            }
            return null;
          };

          if (contentType === 'multipart/form-data' && requestBody) {
            const rb = toJS(requestBody);
            const mp = rb?.content?.['multipart/form-data'];
            if (mp?.examples && Object.keys(mp.examples).length > 0) {
              examples = mp.examples;
              const specJson = toJS(system.specSelectors.specJson());
              schemaName = resolveSchema(mp, specJson);
              // Resolved requestBody has $refs inlined — try raw spec path instead
              if (!schemaName) {
                const sp = toJS(specPath);
                if (sp && specJson) {
                  let node = specJson;
                  for (const key of sp) { node = node?.[key]; }
                  const rawMp = node?.content?.['multipart/form-data'];
                  if (rawMp) schemaName = resolveSchema(rawMp, specJson);
                }
              }
              // If we still can't find a named schema, capture the inline body schema
              if (!schemaName && findBodyProp(mp.schema?.properties)) {
                inlineSchema = findBodyProp(mp.schema.properties);
              }
            }
          }

          // Fallback: read from raw spec if resolved spec lacks examples
          if (!examples && contentType === 'multipart/form-data') {
            const specJson = toJS(system.specSelectors.specJson());
            const sp = toJS(specPath);
            if (sp && specJson) {
              let node = specJson;
              for (const key of sp) { node = node?.[key]; }
              const mp = node?.content?.['multipart/form-data'];
              if (mp?.examples && Object.keys(mp.examples).length > 0) {
                examples = mp.examples;
                schemaName = resolveSchema(mp, specJson);
                if (!schemaName && findBodyProp(mp.schema?.properties)) {
                  inlineSchema = findBodyProp(mp.schema.properties);
                }
              }
            }
          }

          if (!examples) return h(Original, props);

          // ── State ──
          const sp = toJS(specPath);
          const stateKey = Array.isArray(sp) ? sp.join('/') : String(sp);
          const opState = _getState(stateKey);
          const exampleNames = Object.keys(examples);

          const [selected, setSelected] = React.useState(
            () => {
              if (opState.selected && (opState.selected === '__modified' || examples[opState.selected])) {
                return opState.selected;
              }
              return exampleNames[0];
            }
          );
          const [activeTab, setActiveTab] = React.useState('example');
          const settingRef = React.useRef(false);
          const lastTaRef = React.useRef(null);
          const wrapperRef = React.useRef(null);
          const prevExecuteRef = React.useRef(isExecute);

          // Memoize the Original component so dropdown state changes don't
          // trigger a re-render of the textarea (which loses cursor position).
          const originalElement = React.useMemo(
            () => h(Original, props),
            [isExecute, requestBody, contentType, specPath]
          );

          // Sync to persistent closure state
          React.useEffect(() => { opState.selected = selected; }, [selected]);

          // Reset state when leaving "Try it out" mode (Cancel click)
          React.useEffect(() => {
            const wasExecute = prevExecuteRef.current;
            prevExecuteRef.current = isExecute;
            if (wasExecute && !isExecute) {
              opState.modifiedSnapshot = null;
              opState.selected = null;
              lastTaRef.current = null;
              setSelected(exampleNames[0]);
            }
          }, [isExecute]);

          // ── Post-click: detect textarea value changes instantly ──
          // Uses MutationObserver (catches React-driven changes like Reset)
          // plus native input listener (catches user keystrokes).
          React.useEffect(() => {
            if (!isExecute || !wrapperRef.current) return;
            let lastSeenValue = null;
            const cleanups = [];

            // Eagerly apply CSS restructuring as soon as the textarea appears,
            // independent of settingRef so it is never blocked.
            const applyFormClass = () => {
              const ta = wrapperRef.current?.querySelector('textarea');
              if (ta && ta !== lastTaRef.current) {
                lastTaRef.current = ta;
                const tc = ta.closest('.table-container');
                if (tc) tc.classList.add('multipart-form-table');
                const onInput = () => syncValue();
                ta.addEventListener('input', onInput);
                cleanups.push(() => ta.removeEventListener('input', onInput));
              }
              // Fix file input type annotations to match schema nullability
              const allRows = wrapperRef.current?.querySelectorAll('tr') || [];
              for (const row of allRows) {
                const nameEl = row.querySelector('.parameters-col_name label');
                const typeEl = row.querySelector('.parameter__type');
                if (nameEl && typeEl) {
                  const fieldName = nameEl.textContent.replace(/[*\s]|required/g, '').trim();
                  const info = fileFields.find(f => f.name === fieldName);
                  if (info && typeEl.textContent !== info.typeLabel) {
                    typeEl.textContent = info.typeLabel;
                  }
                }
              }
              return ta;
            };

            const syncValue = () => {
              const ta = applyFormClass();
              if (!ta || settingRef.current) return;

              if (ta.value === lastSeenValue) return;
              lastSeenValue = ta.value;

              // Check if the value exactly matches a known example's formatted output
              for (const [name, ex] of Object.entries(examples)) {
                if (ta.value === sortedValue(ex)) {
                  opState.modifiedSnapshot = null;
                  setSelected(name);
                  return;
                }
              }
              opState.modifiedSnapshot = ta.value;
              if (opState.selected !== '__modified') setSelected('__modified');
            };

            // On remount, restore modified textarea value before sync detection
            // so syncValue doesn't see the default example and wipe the snapshot.
            if (opState.modifiedSnapshot != null) {
              const ta = applyFormClass();
              if (ta) {
                settingRef.current = true;
                const nativeSet = Object.getOwnPropertyDescriptor(
                  window.HTMLTextAreaElement.prototype, 'value'
                ).set;
                nativeSet.call(ta, opState.modifiedSnapshot);
                ta.dispatchEvent(new Event('input', { bubbles: true }));
                setTimeout(() => { settingRef.current = false; }, 0);
              }
            }
            // On entering execute mode, if a non-default example was selected
            // pre-click, set the textarea to that example so the selection persists.
            else if (opState.selected && opState.selected !== '__modified' && examples[opState.selected]) {
              const ta = applyFormClass();
              const ex = examples[opState.selected];
              if (ta && ex) {
                const desired = sortedValue(ex);
                if (ta.value !== desired) {
                  settingRef.current = true;
                  const nativeSet = Object.getOwnPropertyDescriptor(
                    window.HTMLTextAreaElement.prototype, 'value'
                  ).set;
                  nativeSet.call(ta, desired);
                  ta.dispatchEvent(new Event('input', { bubbles: true }));
                  setTimeout(() => { settingRef.current = false; }, 0);
                }
              }
            }

            syncValue();

            // MutationObserver catches React-driven value changes (Reset, etc.)
            // and also applies the form class eagerly if the textarea appears late.
            const observer = new MutationObserver(() => {
              applyFormClass();
              syncValue();
            });
            const target = wrapperRef.current.querySelector('.opblock-section-request-body')
                        || wrapperRef.current;
            observer.observe(target, { childList: true, subtree: true, characterData: true });
            cleanups.push(() => observer.disconnect());

            return () => cleanups.forEach(fn => fn());
          }, [isExecute]);

          // Fix file type annotations after every render cycle.
          // React may overwrite DOM changes from the MutationObserver,
          // so we re-apply after React commits using requestAnimationFrame.
          React.useEffect(() => {
            if (!isExecute || !wrapperRef.current || fileFields.length === 0) return;
            const rafId = requestAnimationFrame(() => {
              const allRows = wrapperRef.current?.querySelectorAll('tr') || [];
              for (const row of allRows) {
                const nameEl = row.querySelector('.parameters-col_name label');
                const typeEl = row.querySelector('.parameter__type');
                if (nameEl && typeEl) {
                  const fieldName = nameEl.textContent.replace(/[*\s]|required/g, '').trim();
                  const info = fileFields.find(f => f.name === fieldName);
                  if (info && typeEl.textContent !== info.typeLabel) {
                    typeEl.textContent = info.typeLabel;
                  }
                }
              }
            });
            return () => cancelAnimationFrame(rafId);
          });

          // ── Dropdown change handler ──
          const handleChange = (e) => {
            const name = e.target.value;
            setSelected(name);
            if (!isExecute) return;

            if (name === '__modified') {
              const ta = wrapperRef.current?.querySelector('textarea');
              if (ta && opState.modifiedSnapshot != null) {
                settingRef.current = true;
                const nativeSet = Object.getOwnPropertyDescriptor(
                  window.HTMLTextAreaElement.prototype, 'value'
                ).set;
                nativeSet.call(ta, opState.modifiedSnapshot);
                ta.dispatchEvent(new Event('input', { bubbles: true }));
                setTimeout(() => { settingRef.current = false; }, 0);
              }
              return;
            }

            const ex = examples[name];
            if (!ex?.value) return;

            // User explicitly chose a known example — clear modified state
            opState.modifiedSnapshot = null;

            const fileInput = wrapperRef.current?.querySelector('input[type="file"]');
            if (fileInput) fileInput.value = '';

            const ta = wrapperRef.current?.querySelector('textarea');
            if (ta) {
              settingRef.current = true;
              const nativeSet = Object.getOwnPropertyDescriptor(
                window.HTMLTextAreaElement.prototype, 'value'
              ).set;
              nativeSet.call(ta, sortedValue(ex));
              ta.dispatchEvent(new Event('input', { bubbles: true }));
              setTimeout(() => { settingRef.current = false; }, 0);
            }
          };

          // ── Derived render data ──
          const selectedEx = selected === '__modified' ? null : examples[selected];
          const displayEx = selectedEx || Object.values(examples)[0];

          const options = [];
          if (opState.modifiedSnapshot != null) {
            options.push(h('option', { key: '__modified', value: '__modified' }, '[Modified Value]'));
          }
          for (const name of exampleNames) {
            options.push(h('option', { key: name, value: name }, examples[name].summary || name));
          }

          const dropdown = h('div', { className: 'examples-select' },
            h('span', { className: 'examples-select__section-label' }, 'Examples: '),
            h('select', { className: 'examples-select-element', value: selected, onChange: handleChange },
              ...options
            )
          );

          const description = displayEx?.description
            ? h('div', { className: 'example__section multipart-preview-description' },
                h('div', { className: 'example__section-header' }, 'Example Description'),
                h('p', null, displayEx.description)
              )
            : null;

          // ── Derive file field info from schema (shared by both modes) ──
          const fileFields = [];
          const rb = toJS(requestBody);
          let mpSchema = rb?.content?.['multipart/form-data']?.schema;
          // Resolve $ref if the multipart schema is a reference
          if (mpSchema?.$ref && !mpSchema.properties) {
            const refName = mpSchema.$ref.split('/').pop();
            const specJson = toJS(system.specSelectors.specJson());
            mpSchema = specJson?.components?.schemas?.[refName] || mpSchema;
          }
          if (mpSchema?.properties) {
            for (const [name, prop] of Object.entries(mpSchema.properties)) {
              const isFile = prop.format === 'binary'
                || prop.contentMediaType === 'application/octet-stream'
                || prop.type === 'file';
              const anyOfFile = prop.anyOf?.some(a =>
                a.format === 'binary' || a.contentMediaType === 'application/octet-stream'
              );
              if (isFile || anyOfFile) {
                const isRequired = mpSchema.required?.includes(name);
                const isNullable = anyOfFile || (Array.isArray(prop.type) && prop.type.includes('null'));
                const typeLabel = isNullable ? 'string | (string | null)' : 'string';
                fileFields.push({ name, typeLabel, isRequired });
              }
            }
          }
          if (fileFields.length === 0) {
            fileFields.push({ name: 'file', typeLabel: 'string', isRequired: true });
          }

          // ── Shared tab bar (used by both modes) ──
          const tabBar = h('div', { className: 'tab' },
            h('li', {
              className: 'tabitem' + (activeTab === 'example' ? ' active' : ''),
              onClick: () => setActiveTab('example'),
              style: { cursor: 'pointer' }
            }, 'Example Value'),
            h('li', {
              className: 'tabitem' + (activeTab === 'schema' ? ' active' : ''),
              onClick: () => setActiveTab('schema'),
              style: { cursor: 'pointer' }
            }, 'Schema')
          );

          // ── Schema pane (shared by both modes when Schema tab active) ──
          let schemaPane = null;
          if (activeTab === 'schema') {
            let schemaContent;
            const ModelComponent = system.getComponent('Model');

            if (ModelComponent && schemaName && system.Im) {
              const schemaDef = system.specSelectors.findDefinition(schemaName);
              if (schemaDef) {
                const schemaSpecPath = system.Im.List(['components', 'schemas', schemaName]);
                schemaContent = h('div', { className: 'model-box' },
                  h(ModelComponent, {
                    schema: schemaDef,
                    name: schemaName,
                    isRef: true,
                    getComponent: system.getComponent,
                    specSelectors: system.specSelectors,
                    getConfigs: system.getConfigs,
                    specPath: schemaSpecPath,
                    depth: 1,
                    expandDepth: 2,
                    includeReadOnly: true,
                    includeWriteOnly: true,
                  })
                );
              }
            }

            if (!schemaContent) {
              let schemaObj = null;
              if (schemaName) {
                const specJson = toJS(system.specSelectors.specJson());
                schemaObj = specJson?.components?.schemas?.[schemaName];
              }
              if (!schemaObj && inlineSchema) {
                schemaObj = inlineSchema;
              }
              schemaContent = schemaObj
                ? h('div', { className: 'highlight-code' },
                    h('pre', {
                      className: 'microlight',
                      style: { display: 'block', overflow: 'auto', padding: '10px' }
                    }, JSON.stringify(schemaObj, null, 2))
                  )
                : 'Schema not available';
            }
            schemaPane = h('div', { className: 'multipart-schema-pane' }, schemaContent);
          }

          // ═══════════════════════════════════════
          // POST-CLICK: dropdown → tabs → form/schema → description → file → execute
          // ═══════════════════════════════════════
          if (isExecute) {
            // "Example Value" tab shows the editable form; "Schema" tab shows schema
            const contentSlot = activeTab === 'example' ? originalElement : schemaPane;
            return h('div', { ref: wrapperRef, className: 'multipart-examples-wrapper' },
              h('div', { className: 'multipart-postclick-controls' }, dropdown, tabBar),
              contentSlot,
              h('div', { className: 'multipart-postclick-description' }, description)
            );
          }

          // ═══════════════════════════════════════
          // PRE-CLICK: dropdown → tabs → content/schema → description → file row
          // ═══════════════════════════════════════
          let contentPane;
          if (activeTab === 'example') {
            contentPane = h('div', null,
              h('div', { className: 'highlight-code' },
                h('pre', {
                  className: 'microlight',
                  style: { display: 'block', overflow: 'auto', padding: '10px' }
                }, sortedValue(displayEx))
              )
            );
          } else {
            contentPane = schemaPane;
          }

          const fileRow = fileFields.map(f =>
            h('div', { key: f.name, className: 'multipart-preview-file' },
              h('div', { className: 'parameter__name' },
                f.name,
                f.isRequired ? h('span', { className: 'multipart-required-tag' }, h('span', { className: 'multipart-required-star' }, ' *'), ' required') : null
              ),
              h('div', { className: 'parameter__type' }, f.typeLabel)
            )
          );

          return h('div', { ref: wrapperRef, className: 'multipart-body-preview' },
            dropdown,
            tabBar,
            contentPane,
            description,
            ...fileRow
          );
        };
      }
    }
  };
}
