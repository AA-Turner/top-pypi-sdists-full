/* global afatSettings, _convertStringToSlug, _sortTable, ClipboardJS, _manageModal, fetchGet, DataTable, _removeColumnControl */

$(document).ready(() => {
    'use strict';

    // const dtLanguage = afatSettings.dataTables.language;
    const fatListTable = $('#fleet-edit-fat-list');
    const shipTypeOverviewTable = $('#fleet-edit-ship-types');

    /**
     * Update ship type counts in the overview table
     *
     * @param {Object} data Object of FAT link data
     * @private
     */
    const _updateShipTypeCounts = (data) => {
        console.log('Updating ship type counts...', data);
        const shipTypeCounts = {};

        // Count ship types
        data.forEach((item) => {
            shipTypeCounts[item.ship_type] = (shipTypeCounts[item.ship_type] || 0) + 1;
        });

        // Clear and rebuild ship type overview
        shipTypeOverviewTable.find('tbody').empty();

        Object.entries(shipTypeCounts).forEach(([shipType, count]) => {
            const shipTypeSlug = _convertStringToSlug(shipType);

            shipTypeOverviewTable.append(
                `<tr class="shiptype-${shipTypeSlug}"><td class="ship-type">${shipType}</td><td class="ship-type-count text-end">${count}</td></tr>`
            );
        });

        _sortTable(shipTypeOverviewTable, 'asc');
    };

    /**
     * Initialize the FAT list DataTable
     *
     * @param {Object} data Object of FAT link data
     * @private
     */
    const _initializeDataTable = (data) => {
        const dt = new DataTable(fatListTable, { // eslint-disable-line no-unused-vars
            ...afatSettings.dataTables,
            data: data,
            columns: [
                {data: 'character_name'},
                {data: 'system'},
                {data: 'ship_type'},
                {data: 'actions'}
            ],
            columnDefs: [
                {
                    target: 3,
                    columnControl: _removeColumnControl(),
                    createdCell: (td) => {
                        $(td).addClass('text-end');
                    },
                    orderable: false,
                    width: 50
                }
            ],
            order: [[0, 'asc']],
            initComplete: () => {
                _updateShipTypeCounts(data);
            }
        });
    };

    // Load initial data
    fetchGet({url: afatSettings.url})
        .then(_initializeDataTable)
        .catch((error) => {
            console.error('Error fetching FAT list:', error);
        });

    // Auto-reload functionality
    if (afatSettings.reloadDatatable === true) {
        const intervalReloadDatatable = 15000;
        let expectedReloadTime = Date.now() + intervalReloadDatatable;

        const reloadDataTable = () => {
            const drift = Date.now() - expectedReloadTime;

            if (drift > intervalReloadDatatable) {
                const currentPath = window.location.pathname + window.location.search + window.location.hash;

                if (currentPath.startsWith('/')) {
                    window.location.replace(currentPath);

                    return;
                } else {
                    console.error('Invalid redirect URL');
                }
            }

            fetchGet({url: afatSettings.url})
                .then((newData) => {
                    const dataTable = fatListTable.DataTable();

                    dataTable.clear().rows.add(newData).draw();
                    _updateShipTypeCounts(newData);
                })
                .catch((error) => {
                    console.error('Error reloading data:', error);
                });

            expectedReloadTime += intervalReloadDatatable;

            setTimeout(reloadDataTable, Math.max(0, intervalReloadDatatable - drift));
        };

        setTimeout(reloadDataTable, intervalReloadDatatable);
    }

    // Initialize clipboard and modals
    const clipboard = new ClipboardJS('.copy-btn');
    clipboard.on('success', () => {
        $('.copy-btn').tooltip('show');
    });

    [
        afatSettings.modal.cancelEsiFleetModal.element,
        afatSettings.modal.deleteFatModal.element,
        afatSettings.modal.reopenFatLinkModal.element
    ].forEach((modalElement) => {
        _manageModal($(modalElement));
    });
});
