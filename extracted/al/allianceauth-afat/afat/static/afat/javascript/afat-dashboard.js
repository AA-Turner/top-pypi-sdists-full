/* global afatSettings, characters, _dateRender, _manageModal, fetchGet, DataTable */

$(document).ready(() => {
    'use strict';

    const dtLanguage = afatSettings.dataTables.language;

    const _createDataTable = ({table, url, columns, columnDefs, order, columnControl}) => {
        fetchGet({url})
            .then((data) => {
                const dt = new DataTable(table, { // eslint-disable-line no-unused-vars
                    ...afatSettings.dataTables,
                    data: data,
                    columns: columns,
                    order: order,
                    ordering: {
                        indicators: false,
                        handler: false
                    },
                    columnDefs: columnDefs || [],
                    columnControl: columnControl || afatSettings.dataTables.columnControl
                });
            })
            .catch((error) => console.error(`Error fetching data for ${table}:`, error));
    };

    /**
     * Initialize character FAT tables
     */
    const initCharacterFatTables = () => {
        const characterTableColumns = [
            {data: 'fleet_name'},
            {data: 'fleet_type'},
            {data: 'doctrine'},
            {data: 'system'},
            {data: 'ship_type'},
            {
                data: {
                    display: (data) => _dateRender(data.fleet_time.time),
                    sort: (data) => data.fleet_time.timestamp
                },
            }
        ];

        characters.forEach((character) => {
            const table = $('#recent-fats-character-' + character.charId);
            const url = afatSettings.url.characterFats.replace('0', character.charId);

            _createDataTable({
                table: table,
                url: url,
                columns: characterTableColumns,
                columnControl: [],
                order: [[5, 'desc']]
            });
        });
    };

    /**
     * Initialize recent FAT links table
     */
    const initRecentFatLinksTable = () => {
        const columns = [
            {data: 'fleet_name'},
            {data: 'fleet_type'},
            {data: 'doctrine'},
            {data: 'creator_name'},
            {
                data: {
                    display: (data) => _dateRender(data.fleet_time.time),
                    sort: (data) => data.fleet_time.timestamp
                },
            }
        ];

        const columnDefs = [];
        const hasPermissions = afatSettings.permissions.addFatLink || afatSettings.permissions.manageAfat;

        if (hasPermissions) {
            columns.push({
                data: 'actions'
            });

            columnDefs.push({
                target: 5,
                orderable: false,
                createdCell: (td) => $(td).addClass('text-end'),
                width: 125
            });
        }

        dtLanguage.emptyTable = `<div class="aa-callout aa-callout-warning" role="alert">
            <p>${afatSettings.translation.dataTable.noFatlinksWarning}</p>
        </div>`;

        _createDataTable({
            table: $('#dashboard-recent-fatlinks'),
            url: afatSettings.url.recentFatLinks,
            columns: columns,
            columnDefs: columnDefs,
            columnControl: [],
            order: [[4, 'desc']]
        });
    };

    /**
     * Initialize modals
     */
    const initModals = () => {
        const modals = [
            afatSettings.modal.cancelEsiFleetModal.element,
            afatSettings.modal.deleteFatLinkModal.element
        ];

        modals.forEach(modalElement => {
            _manageModal($(modalElement));
        });
    };

    // Initialize components
    if (characters.length > 0) {
        initCharacterFatTables();
    }

    initRecentFatLinksTable();
    initModals();
});
