/*!
 * DataTables - filterDropDown plugin (modernized fork by Peter Pfeufer)
 *
 * @version 0.0.3
 * @author Peter Pfeufer
 * @license GPL-3.0 or later
 * @link https://github.com/ppfeufer/datatables-filterdropdown
 *
 * Description: This plugin adds a filter dropdown to DataTables columns,
 *              allowing users to filter the table based on unique values in each column.
 *              It supports both client-side and server-side processing, and is
 *              compatible with different versions of DataTables.
 *
 * Original Plugin:
 * Author: Erik Kalkoken
 * Created: 08/28/2017
 * GitHub: https://github.com/ErikKalkoken/filterDropDown
 **/

/* global define */

/*
 * datatables-filterdropdown
 * DataTables extension wrapper (compatible with DataTables 2/3 and jQuery integration)
 * This file exports a factory that registers the extension and also attaches it to the
 * global DataTable object when available so it can be used as a normal DataTables
 * plugin (both in ES module environments and classic script includes).
 */

// UMD / module wrapper: support ESM, CommonJS and browser globals
((factory) => {
    'use strict';

    if (typeof define === 'function' && define.amd) {
        // AMD
        define(['datatables.net'], (dt) => {
            return factory(window, document, dt);
        });
    } else if (typeof exports === 'object') {
        // CommonJS
        const cjsRequires = (root) => {
            if (!root.DataTable) {
                require('datatables.net')(root);
            }
        };

        if (typeof window === 'undefined') {
            module.exports = (root) => {
                if (!root) {
                    // CommonJS environments without a window global must pass a
                    // root. This will give an error otherwise
                    root = window;
                }

                cjsRequires(root);

                return factory(root, root.document, root.DataTable);
            };
        } else {
            cjsRequires(window);

            module.exports = factory(window, window.document, window.DataTable);
        }
    } else {
        // Browser
        factory(window, document, window.DataTable);
    }
})((window, document, DataTable) => { // jshint ignore:line
    'use strict';

    const version = '0.0.3';

    /**
     * Default settings for the filterDropDown plugin.
     * These defaults can be overridden by providing a custom initialization object when initializing the DataTable.
     *
     * @type {function(): {filterDef: {ajax: null, bootstrapVersion: number, columns: [], labelFilter: string}, columnDef: {labelDropdownAll: string, maxWidth: null, title: null}}}
     * @private
     */
    const _defaults = () => {
        return {
            filterDef: {
                ajax: null,
                bootstrapVersion: 5,
                columns: [],
                labelFilter: 'Filter by' // Please set this explicitly, so it can be translated
            },
            columnDef: {
                labelDropdownAll: 'All', // Please set this explicitly, so it can be translated
                maxWidth: null,
                title: null
            }
        };
    };

    /**
     * DataTables compatibility helpers
     * Provides a unified way to access DataTables API and utilities, supporting both jQuery and global DataTable usage patterns, as well as version checks.
     *
     * @type {{apiFromSettings: function(*): (*|null), escapeRegex: function(*): (*), version: function(): (*|null), isV2: function(): (null|*)}}
     */
    const dtCompat = (() => {
        const hasJQueryDT = typeof jQuery !== 'undefined' && jQuery.fn && jQuery.fn.dataTable;
        const hasGlobalDT = typeof DataTable !== 'undefined' && DataTable;

        return {
            /**
             * Get the DataTables API instance from the settings object, supporting both jQuery and global DataTable usage patterns.
             *
             * @param settings
             * @returns {*|null}
             */
            apiFromSettings: (settings) => {
                // Global/Native DataTables API
                if (hasGlobalDT && DataTable.Api) {
                    return new DataTable.Api(settings);
                }

                // jQuery DataTables API
                if (hasJQueryDT && jQuery.fn.dataTable.Api) {
                    return new jQuery.fn.dataTable.Api(settings);
                }

                console.warn('DataTables not found or unsupported API.'); // graceful fallback

                return null;
            },

            /**
             * Escape a string for use in a regular expression, supporting both jQuery and global DataTable usage patterns.
             *
             * @param str
             * @returns {string|*|string|string}
             */
            escapeRegex: (str) => {
                if (hasGlobalDT && DataTable.util && DataTable.util.escapeRegex) {
                    return DataTable.util.escapeRegex(str);
                }

                if (hasJQueryDT && jQuery.fn.dataTable && jQuery.fn.dataTable.util && jQuery.fn.dataTable.util.escapeRegex) {
                    return jQuery.fn.dataTable.util.escapeRegex(str);
                }

                // Fallback: simple escape (not full DataTables behavior but safer than nothing)
                return str ? String(str).replace(/[-/\\^$*+?.()|[\]{}]/g, '\\$&') : '';
            },

            /**
             * Get the version of DataTables, supporting both jQuery and global DataTable usage patterns.
             *
             * @returns {*|null|string}
             */
            version: () => {
                if (hasJQueryDT && jQuery.fn.dataTable && jQuery.fn.dataTable.version) {
                    return jQuery.fn.dataTable.version;
                }

                if (hasGlobalDT && DataTable && DataTable.version) {
                    return DataTable.version;
                }

                return null;
            },

            /**
             * Check if the DataTables version is 2 or higher, supporting both jQuery and global DataTable usage patterns.
             *
             * @returns {boolean|null}
             */
            isV2: () => {
                const v = (typeof DataTable !== 'undefined' && DataTable && DataTable.version) || (typeof jQuery !== 'undefined' && jQuery.fn && jQuery.fn.dataTable && jQuery.fn.dataTable.version);

                if (!v) {
                    return null;
                }

                const major = parseInt(String(v).split('.')[0], 10);

                return !isNaN(major) && major >= 2;
            }
        };
    })();

    /**
     * Set the select UI from the column's current search (handles stateSave restore)
     *
     * @param select
     * @param column
     */
    const setSelectFromColumnSearch = (select, column) => {
        if (!select || !column) {
            return;
        }

        const $select = $(select);
        const currentSearch = column.search(); // may be '' or a regex string like ^value$

        if (!currentSearch) {
            // nothing to restore
            return;
        }

        // Try to find a matching option by comparing DataTables escaped option -> ^escaped$
        const options = $select.find('option').map((_, option) => {
            void _; // Void unused variable

            return $(option).val();
        }).get();

        for (let i = 0; i < options.length; i++) {
            const opt = options[i];

            if (opt === '') {
                continue;
            }

            const escaped = dtCompat.escapeRegex(opt);

            if (`^${escaped}$` === currentSearch || opt === currentSearch) {
                $select.val(opt);

                return;
            }
        }

        // If not found among options, try to extract a raw value from a pattern like ^...$
        const m = currentSearch.match(/^\^(.*)\$$/);
        const raw = m ? m[1].replace(/\\(.)/g, '$1') : currentSearch.replace(/\\(.)/g, '$1');

        if (raw) {
            // append the missing option so UI reflects saved state
            $select.append(`<option value="${raw}">${raw}</option>`);
            $select.val(raw);
        }
    };

    /**
     * Parse initialization array and returns filterDef array to faster and easy use,
     * also sets defaults for properties that are not set
     *
     * @param initArray
     * @returns {{columns: Array, columnsIdxList: Array, bootstrapVersion: number,ajax: null, labelFilter: string}}
     */
    const parseInitArray = (initArray) => {
        // Start with a copy of the default filter definition
        const filterDef = {
            ..._defaults().filterDef,
            columnsIdxList: [] // Initialize columnsIdxList as an empty array
        };

        // Set filter properties if they have been defined otherwise the defaults will be used
        if ('bootstrapVersion' in initArray && typeof initArray.bootstrapVersion === 'number') {
            filterDef.bootstrapVersion = initArray.bootstrapVersion;
        }

        if ('ajax' in initArray && typeof initArray.ajax === 'string') {
            filterDef.ajax = initArray.ajax;
        }

        if ('labelFilter' in initArray && typeof initArray.labelFilter === 'string') {
            filterDef.labelFilter = initArray.labelFilter;
        }

        // Add definition for each column
        if ('columns' in initArray) {
            initArray.columns.forEach((initColumn) => {
                if ('idx' in initColumn && typeof initColumn.idx === 'number') {
                    // Initialize column
                    const idx = initColumn.idx;

                    // Start with a copy of the default column definition
                    filterDef.columns[idx] = {..._defaults().columnDef};

                    // Add to a list of indices in the same order they appear in the init array
                    filterDef.columnsIdxList.push(idx);

                    // Set column properties if they have been defined otherwise the defaults will be used
                    if ('title' in initColumn && typeof initColumn.title === 'string') {
                        filterDef.columns[idx].title = initColumn.title;
                    }

                    if ('maxWidth' in initColumn && typeof initColumn.maxWidth === 'string') {
                        filterDef.columns[idx].maxWidth = initColumn.maxWidth;
                    }

                    if ('labelDropdownAll' in initColumn && typeof initColumn.labelDropdownAll === 'string') {
                        filterDef.columns[idx].labelDropdownAll = initColumn.labelDropdownAll;
                    }
                }
            });
        }

        return filterDef;
    };

    /**
     * Add option d to the given select object
     *
     * @param select
     * @param d
     */
    const addOption = (select, d) => {
        if (d !== '') {
            select.append(`<option value="${d}">${d}</option>`);
        }
    };

    /**
     * Initialize the select element for given column and apply event to react to changes
     *
     * @param id
     * @param column
     * @returns {*|jQuery|HTMLElement}
     */
    const initSelectForColumn = (id, column) => {
        const select = $(`#${id}_filterSelect${column.index()}`);

        $(select).change(() => {
            const val = dtCompat.escapeRegex($(select).val());

            column.search(val ? `^${val}$` : '', true, false).draw();
        });

        return select;
    };

    // Add filterDropDown container div, draw select elements with default options.
    // Use preInit so that elements are created and correctly shown before data is loaded
    $(document).on('preInit.dt', (e, settings) => {
        if (e.namespace !== 'dt') {
            return;
        }

        // Get the api object for the current dt table
        const api = dtCompat.apiFromSettings(settings);

        if (!api) {
            return;
        }

        // Get the id of the current table
        const id = api.table().node().id;

        // Get the initialization object for the current table to retrieve custom settings
        const initObj = api.init();

        // Only proceed if the filter has been defined in the current table,
        // otherwise don't do anything.
        if (!('filterDropDown' in initObj)) {
            return;
        }

        // Get the current filter definition from the init array
        const filterDef = parseInitArray(initObj.filterDropDown);

        // only proceed if there are any columns defined
        if (filterDef.columns.length === 0) {
            return;
        }

        // Get container div for the current data table to add new elements to
        const container = api.table().container();

        // Add filter elements to DOM
        const filterWrapperId = `${id}_filterWrapper`;

        // Set CSS classes for the filter wrapper div
        let filterWrapperCssClasses = `${filterWrapperId} align-items-center d-flex flex-wrap gap-3 mb-3`;

        // Override for a potentially different Bootstrap version in the future
        // if (filterDef.bootstrapVersion === 5) {
        //     filterWrapperCssClasses = `${filterWrapperId} align-items-center d-flex flex-wrap gap-3 mb-3`;
        // }

        $(container).prepend(`<div class="row justify-content-between"><p class="mb-1 fw-bold">${filterDef.labelFilter}:</p><div id="${filterWrapperId}" class="${filterWrapperCssClasses}"></div></div>`);

        api.columns(filterDef.columnsIdxList).indexes().each((idx) => {
            const column = api.column(idx);
            const colIndex = column.index();

            // Set title of current column
            const columnHeader = $(column.header()).find('.dt-column-title').html() || $(column.header()).html();
            let colName = filterDef.columns[colIndex].title !== null ? filterDef.columns[colIndex].title : columnHeader;

            if (colName === '') {
                colName = `column ${colIndex + 1}`;
            }

            // Adding the select element for current column to container
            const selectId = `${id}_filterSelect${colIndex}`;

            // Set markup for select element with label, the label is needed to make
            // clear which column is filtered and also to make the filter accessible
            // for screen readers, the select element will be initialized with default
            // option and options will be added after filtering the table
            let selectMarkup = `<div><label for="${selectId}" class="col-auto">${colName}</label><select id="${selectId}" class="form-select form-select-sm w-auto ${id}_filterSelect"></select></div>`;

            // Override for a potentially different Bootstrap version in the future
            // if (filterDef.bootstrapVersion === 5) {
            //     selectMarkup = `<div><label for="${selectId}" class="col-auto">${colName}</label><select id="${selectId}" class="form-select form-select-sm w-auto ${id}_filterSelect"></select></div>`;
            // }

            $(`#${filterWrapperId}`).append(selectMarkup);

            // Initializing select for current column and applying event to react to changes
            $(`#${selectId}`).empty().append(`<option value="">${filterDef.columns[colIndex].labelDropdownAll}</option>`);
        });
    });

    // Filter table and add available options to dropDowns
    $(document).on('init.dt', (e, settings) => {
        if (e.namespace !== 'dt') {
            return;
        }

        // Get api object for current dt table
        const api = dtCompat.apiFromSettings(settings);

        if (!api) {
            return;
        }

        // Get id of current table
        const id = api.table().node().id;

        // Get the initialization object for current table to retrieve custom settings
        const initObj = api.init();

        // Only proceed if a filter has been defined in the current table, otherwise don't do anything.
        if (!('filterDropDown' in initObj)) {
            return;
        }

        // Get current filter definition
        const filterDef = parseInitArray(initObj.filterDropDown);

        if (filterDef.ajax === null) {
            api.columns(filterDef.columnsIdxList).indexes().each((idx) => {
                const column = api.column(idx);
                const select = initSelectForColumn(id, column);

                column.data().unique().sort().each((d) => addOption(select, d));

                setSelectFromColumnSearch(select, column);
            });
        } else {
            // Fetch column options from server for server side processing
            const columnsQuery = `columns=${encodeURIComponent(api.columns(filterDef.columnsIdxList).dataSrc().join())}`;

            $.getJSON(`${filterDef.ajax}?${columnsQuery}`, (columnsOptions) => {
                api.columns(filterDef.columnsIdxList).indexes().each((idx) => {
                    const column = api.column(idx);
                    const select = initSelectForColumn(id, column);
                    const columnName = column.dataSrc();

                    if (columnName in columnsOptions) {
                        columnsOptions[columnName].forEach((d) => addOption(select, d));

                        setSelectFromColumnSearch(select, column);
                    } else {
                        console.warn(`Missing column '${columnName}' in ajax response.`);
                    }
                });
            });
        }
    });

    // Sync selects after state is loaded (extra robustness)
    $(document).on('stateLoaded.dt', (e, settings, data) => {
        void data;

        if (e.namespace !== 'dt') {
            return;
        }

        const api = dtCompat.apiFromSettings(settings);

        if (!api) {
            return;
        }

        const initObj = api.init();

        if (!('filterDropDown' in initObj)) {
            return;
        }

        const filterDef = parseInitArray(initObj.filterDropDown);

        api.columns(filterDef.columnsIdxList).indexes().each((idx) => {
            const column = api.column(idx);
            const select = $(`#${api.table().node().id}_filterSelect${column.index()}`);

            setSelectFromColumnSearch(select, column);
        });
    });

    // Attach a convenience method/namespace to DataTable global (if present)
    if (typeof DataTable !== 'undefined') {
        DataTable.filterDropDown = DataTable.filterDropDown || {};
        DataTable.filterDropDown.version = version;
        DataTable.filterDropDown.register = () => {
            // No-op: the plugin registers itself via DataTables events when included
            return true;
        };
    }

    // Expose a minimal API for module consumers
    return {
        version: version,
        register: () => {
            return true;
        }
    };
});
