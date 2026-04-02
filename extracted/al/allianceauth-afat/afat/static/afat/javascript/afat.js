/* global afatJsSettingsOverride, afatJsSettingsDefaults, bootstrap, objectDeepMerge, moment */

/* jshint -W097 */
'use strict';

// Build the settings object
const afatSettings = typeof afatJsSettingsOverride !== 'undefined'
    ? objectDeepMerge(afatJsSettingsDefaults, afatJsSettingsOverride) // jshint ignore: line
    : afatJsSettingsDefaults;

/**
 * Convert a string to a slug
 * @param {string} text
 * @returns {string}
 */
const _convertStringToSlug = (text) => { // eslint-disable-line no-unused-vars
    return text.toLowerCase()
        .replace(/[^\w ]+/g, '')
        .replace(/ +/g, '-');
};

/**
 * Sorting a table by its first columns alphabetically
 * @param {element} table
 * @param {string} order
 */
const _sortTable = (table, order) => { // eslint-disable-line no-unused-vars
    const asc = order === 'asc';
    const tbody = table.find('tbody');

    tbody.find('tr').sort((a, b) => {
        if (asc) {
            return $('td:first', a).text().localeCompare($('td:first', b).text());
        } else {
            return $('td:first', b).text().localeCompare($('td:first', a).text());
        }
    }).appendTo(tbody);
};

/**
 * Manage a modal window
 *
 * @param {element} modalElement The modal element
 */
const _manageModal = (modalElement) => { // eslint-disable-line no-unused-vars
    /**
     * Update modal elements
     *
     * @param {string} bodyText Modal body text
     * @param {string} confirmButtonText Text for the confirm action button
     * @param {string} cancelButtonText Text for the cancel action button
     * @param {string} confirmActionUrl URL for the confirm action button
     */
    const updateModal = ({bodyText, confirmButtonText, cancelButtonText, confirmActionUrl}) => {
        modalElement.find('#confirm-action').text(confirmButtonText).attr('href', confirmActionUrl);
        modalElement.find('#cancel-action').text(cancelButtonText);
        modalElement.find('.modal-body').html(bodyText);
    };

    /**
     * Clear modal elements
     */
    const clearModal = () => {
        modalElement.find('#confirm-action').text('').attr('href', '');
        modalElement.find('#cancel-action').text('');
        modalElement.find('.modal-body').html('');
    };

    modalElement.on('show.bs.modal', (event) => {
        const button = $(event.relatedTarget);
        const url = button.data('url');
        const bodyText = button.data('body-text');
        const confirmButtonText = button.data('confirm-text') || modalElement.find('#confirmButtonDefaultText').text();
        const cancelButtonText = button.data('cancel-text') || modalElement.find('#cancelButtonDefaultText').text();

        updateModal({
            bodyText: bodyText,
            confirmButtonText: confirmButtonText,
            cancelButtonText: cancelButtonText,
            confirmActionUrl: url
        });
    }).on('hide.bs.modal', () => {
        clearModal();
    });
};

/**
 * Bootstrap tooltip
 *
 * @param {string} [selector=.allianceauth-afat] Selector for the tooltip elements, defaults to 'body'
 *                                 to apply to all elements with the data-bs-tooltip attribute.
 *                                 Example: 'body', '.my-tooltip-class', '#my-tooltip-id'
 *                                 If you want to apply it to a specific element, use that element's selector.
 *                                 If you want to apply it to all elements with the data-bs-tooltip attribute,
 *                                 use 'body' or leave it empty.
 * @param {string} [namespace=afat] Namespace for the tooltip
 * @returns {void}
 */
const _afatBootstrapTooltip = ({selector = '.allianceauth-afat', namespace = 'afat'}) => { // eslint-disable-line no-unused-vars
    document.querySelectorAll(`${selector} [data-bs-tooltip="${namespace}"]`)
        .forEach((tooltipTriggerEl) => {
            // Dispose existing tooltip instance if it exists
            const existing = bootstrap.Tooltip.getInstance(tooltipTriggerEl);
            if (existing) {
                existing.dispose();
            }

            // Remove any leftover tooltip elements
            $('.bs-tooltip-auto').remove();

            // Create new tooltip instance
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
};

/**
 * Remove search control from column control
 *
 * @return {(*|{content: *[]}|{target: number, content: [string]}|{target: number, content: [string]})[]}
 * @private
 */
const _removeSearchFromColumnControl = () => { // eslint-disable-line no-unused-vars
    return afatSettings.dataTables.columnControl.map((control, index) => index === 1 ? { ...control, content: [] } : control);
};

/**
 * Remove all controls from column control
 *
 * @return {(*&{content: []})[]}
 * @private
 */
const _removeColumnControl = () => { // eslint-disable-line no-unused-vars
    return afatSettings.dataTables.columnControl.map((control) => ({ ...control, content: [] }));
};

/**
 * Render date in AFAT format
 *
 * @param {Date} date Date to render
 * @return {*} Formatted date string
 * @private
 */
const _dateRender = (date) => { // eslint-disable-line no-unused-vars
    return moment(date).utc().format(afatSettings.datetimeFormat);
};
