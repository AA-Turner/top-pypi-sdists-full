/* global updateData */

function setupModal(modalId, ajaxDataAttr, contentId, loaderId) {
    $(modalId).on('show.bs.modal', function (event) {
        const button = $(event.relatedTarget);
        let ajaxUrl = button.data(ajaxDataAttr);
        const modal = $(this);

        // reactive loader
        modal.find(contentId).hide();
        modal.find(loaderId).show();

        modal.find(contentId).load(
            ajaxUrl,
            function(response, status, xhr) {
                modal.find(loaderId).hide();
                modal.find(contentId).show();

                if ([403, 404, 500].includes(xhr.status)) {
                    modal.find(contentId).html(response);
                    modal.find('.modal-title').html('Error');
                    return;
                }

                // Extract and set the modal title
                const title = modal.find(contentId).find('#modal-title').html();
                modal.find('.modal-title').html(title);
                modal.find('.modal-title').removeClass('d-none');
                modal.find(contentId).find('#modal-title').hide();
            }
        );
    }).on('hidden.bs.modal', function () {
        // Clear the modal content when it is hidden
        $(this).find(contentId).html('');
    });
}

function getMonthName(monthNumber, translations) {
    const months = translations.months;
    return months[monthNumber - 1]; // Array ist 0-basiert, daher -1
}


function handleDropdownClick(event, dropdownType, state) {
    if (event.target && event.target.matches('a.dropdown-item')) {
        const items = event.currentTarget.querySelectorAll('a.dropdown-item');
        items.forEach(item => item.classList.remove('active'));
        event.target.classList.add('active');

        if (dropdownType === 'year') {
            $('#yearDropDownButton').text(event.target.textContent);
            state.selectedYear = event.target.dataset.bsYearId;
            state.selectedviewMode = 'month';
        } else if (dropdownType === 'month') {
            $('#monthDropDownButton').text(event.target.textContent);
            state.selectedMonth = event.target.dataset.bsMonthId;
            state.selectedviewMode = 'month';
        }

        updateData(state.selectedMonth, state.selectedYear);
    }
}
