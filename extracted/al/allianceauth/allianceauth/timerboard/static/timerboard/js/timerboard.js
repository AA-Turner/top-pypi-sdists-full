$(document).ready(() => {
    'use strict';

    const inputAbsoluteTime = $('input#id_absolute_time');
    const inputCountdown = $('#id_days_left, #id_hours_left, #id_minutes_left');

    inputAbsoluteTime.parent().hide();
    inputAbsoluteTime.parent().prev('label').hide();
    inputCountdown.prop('required', true);

    $('input#id_absolute_checkbox').change((event) => {
        if ($(event.target).prop('checked')) {
            // Checkbox is checked
            inputAbsoluteTime.parent().show();
            inputAbsoluteTime.parent().prev('label').show();
            inputCountdown.parent().hide();
            inputCountdown.parent().prev('label').hide();
            inputAbsoluteTime.prop('required', true);
            inputCountdown.prop('required', false);
        } else {
            // Checkbox is not checked
            inputAbsoluteTime.parent().hide();
            inputAbsoluteTime.parent().prev('label').hide();
            inputCountdown.parent().show();
            inputCountdown.parent().prev('label').show();
            inputAbsoluteTime.prop('required', false);
            inputCountdown.prop('required', true);
        }
    });

    addEventListener('paste', (event) => {
        const data = (event.clipboardData || window.clipboardData).getData('text').split(/\r?\n/);
        const dt_re =  /(\d{4}.\d{2}.\d{2}) (\d{2}.\d{2}.\d{2})/;

        if (data.length === 3 && data[2].match(dt_re)) {
            const system = document.getElementById('id_system');
            const absolute_time = document.getElementById('id_absolute_time');
            const details = document.getElementById('id_details');
            const absolute_checkbox = document.getElementById('id_absolute_checkbox');
            const structure_type = document.getElementById('id_structure');
            const planet_moon = document.getElementById('id_planet_moon');

            absolute_checkbox.checked = true;
            absolute_checkbox.dispatchEvent(new Event('change')); // toggle visible fields

            const system_and_structure_name = data[0];
            details.value = system_and_structure_name;

            const skyhook_re = /\(([\w\-]+) ([IXV]+)\) \[.+]/;
            if (system_and_structure_name.match(skyhook_re)) {
                const location = system_and_structure_name.match(skyhook_re);
                system.value = location[1];
                planet_moon.value = location[2];
                structure_type.value = 'Orbital Skyhook';
            }
            else {
                let system_name = system_and_structure_name.split(' - ')[0];
                if (system_name.match(/ » /)) {
                    system_name = system_name.split(' » ')[0];
                    structure_type.value = 'Ansiblex Jump Gate';
                }
                system.value = system_name;
            }
            const datetime = data[2].match(dt_re);
            const date = datetime[1].replace(/\D/g, '.');
            const time = datetime[2].replace(/\D/g, ':');
            const dt = new Date(date + ' ' + time + 'Z'); // force UTC
            absolute_time.value = dt.toISOString();
        }
    });
});
