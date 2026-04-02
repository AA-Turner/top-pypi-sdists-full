/* global afatSettings, _afatBootstrapTooltip, _manageModal, _removeSearchFromColumnControl, _removeColumnControl, DataTable */

$(document).ready(() => {
    'use strict';

    // Variables
    const hasPermissions = afatSettings.permissions.addFatLink || afatSettings.permissions.manageAfat;
    const linkListTable = $('#link-list');
    const RELOAD_INTERVAL = 60000;
    let expectedReloadTime = Date.now() + RELOAD_INTERVAL;
    let dt = null;

    // Column definitions based on permissions
    const linkListTableColumnDefs = [
        {
            target: 4,
            columnControl: _removeSearchFromColumnControl(),
        },
        {
            target: 5,
            columnControl: _removeColumnControl(),
            orderable: false
        },
    ];

    if (hasPermissions) {
        linkListTableColumnDefs.splice(1, 0, {
            target: 6,
            createdCell: (td) => {
                $(td).addClass('text-end');
            },
            columnControl: _removeColumnControl(),
            orderable: false,
            width: 125
        });
    }

    /**
     * Link list DataTable initialization complete handler
     *
     * @private
     */
    const _linkListTableInitComplete = () => {
        _afatBootstrapTooltip({selector: '#link-list'});
    };

    /**
     * Initialize the link list DataTable
     */
    const initializeDataTable = () => {
        dt = new DataTable(linkListTable, {
            ...afatSettings.dataTables,
            columnDefs: linkListTableColumnDefs,
            order: [[4, 'desc']],
            initComplete: () => {
                _linkListTableInitComplete();
                dt.on('draw.dt', () => _linkListTableInitComplete());
            }
        });

        setTimeout(reloadDataTable, RELOAD_INTERVAL);
    };

    /**
     * Reload the link list DataTable
     */
    const reloadDataTable = () => {
        const drift = Date.now() - expectedReloadTime;

        if (drift > RELOAD_INTERVAL) {
            const currentPath = window.location.pathname + window.location.search + window.location.hash;

            if (currentPath.startsWith('/')) {
                window.location.replace(currentPath);

                return;
            }

            console.error('Invalid redirect URL');
        }

        dt.ajax.reload(() => {
            _linkListTableInitComplete();
        }, false);

        expectedReloadTime += RELOAD_INTERVAL;

        setTimeout(reloadDataTable, Math.max(0, RELOAD_INTERVAL - drift));
    };

    // Initialize table and auto-reload
    initializeDataTable();

    // Initialize modals
    [
        afatSettings.modal.cancelEsiFleetModal.element,
        afatSettings.modal.deleteFatLinkModal.element,
    ].forEach((modalElement) => {
        _manageModal($(modalElement));
    });
});
