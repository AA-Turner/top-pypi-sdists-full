/* global afatSettings, _afatBootstrapTooltip, Chart, fetchGet, _removeSearchFromColumnControl, _removeColumnControl, DataTable */

const elementBody = document.querySelector('body');
const elementBodyCss = getComputedStyle(elementBody);

Chart.defaults.color = elementBodyCss.color;

/**
 * Draw a chart on the given element with the given data and options using Chart.js
 *
 * @param {HTMLElement} element The element to draw the chart on
 * @param {string} chartType The type of chart to draw
 * @param {object} data The data to draw
 * @param {object} options The options to draw the chart with
 */
const drawChart = (element, chartType, data, options) => { // eslint-disable-line no-unused-vars
    'use strict';

    const chart = new Chart(element, { // eslint-disable-line no-unused-vars
        type: chartType,
        data: data,
        options: options
    });
};

$(document).ready(() => {
    'use strict';

    /**
     * Toggle element visibility
     *
     * @param {string} selector Element selector
     * @param {boolean} show True to show, false to hide
     */
    const toggleElement = (selector, show) => {
        $(selector).toggleClass('d-none', !show);
    };

    /**
     * Toggle multiple elements at once
     *
     * @param {string[]} selectors Array of selectors
     * @param {boolean} show True to show, false to hide
     */
    const toggleElements = (selectors, show) => {
        selectors.forEach(selector => toggleElement(selector, show));
    };

    /**
     * Handle character details button click
     *
     * @param {Event} event Click event
     */
    const handleCharacterDetailsClick = (event) => {
        const btn = $(event.currentTarget);
        const characterName = btn.data('character-name');
        const url = btn.data('url');

        // Hide loading/data elements initially
        toggleElements([
            '#col-character-alt-characters .afat-character-alt-characters .afat-no-data',
            '#col-character-alt-characters .afat-character-alt-characters .afat-character-alt-characters-table'
        ], false);

        // Show container and loading spinner
        toggleElements([
            '#col-character-alt-characters',
            '#col-character-alt-characters .afat-character-alt-characters .afat-loading-character-data'
        ], true);

        // Set character name
        $('#afat-corp-stats-main-character-name').text(characterName);

        // Fetch and display data
        fetchGet({url})
            .then(handleTableData)
            .catch((error) => {
                console.error(`Error: ${error.message}`);
            });
    };

    /**
     * Handle table data response
     *
     * @param {Object} tableData Array of table data objects
     */
    const handleTableData = (tableData) => {
        const table = $('#character-alt-characters');

        // Hide loading spinner
        toggleElement('#col-character-alt-characters .afat-character-alt-characters .afat-loading-character-data', false);

        if (!tableData || Object.keys(tableData).length === 0) {
            toggleElement('#col-character-alt-characters .afat-character-alt-characters .afat-no-data', true);

            return;
        }

        // Show table and initialize DataTable
        toggleElement('#col-character-alt-characters .afat-character-alt-characters .afat-character-alt-characters-table', true);

        // Destroy existing table if present
        if ($.fn.DataTable.isDataTable(table)) {
            table.DataTable().destroy();
        }

        // Create new DataTable
        const dt = new DataTable(table, { // eslint-disable-line no-unused-vars
            ...afatSettings.dataTables,
            data: tableData,
            columns: [
                { data: 'character_name' },
                { data: 'fat_count' },
                { data: 'show_details_button' },
                { data: 'in_main_corp' }
            ],
            order: [
                [3, 'desc'],
                [1, 'desc'],
                [0, 'asc']
            ],
            columnDefs: [
                {
                    targets: 1,
                    columnControl: _removeSearchFromColumnControl(),
                },
                {
                    target: 2,
                    createdCell: (td) => {
                        $(td).addClass('text-end');
                    },
                    columnControl: _removeColumnControl(),
                    width: 50
                },
                {
                    targets: 3,
                    visible: false
                }
            ],
            initComplete: () => {
                _afatBootstrapTooltip({selector: '#character-alt-characters'});
            }
        });
    };

    $('.btn-afat-corp-stats-view-character').on('click', handleCharacterDetailsClick);
});
