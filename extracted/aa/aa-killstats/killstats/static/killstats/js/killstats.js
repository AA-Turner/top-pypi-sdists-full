/* global killstatssettings, handleDropdownClick */

const entityPk = killstatssettings.entity_pk;
const entityType = killstatssettings.entity_type;

const yearDropdown = document.getElementById('yearDropdown');
const monthDropdown = document.getElementById('monthDropdown');

// Current date
const currentDate = new Date();
const state = {
    selectedYear: currentDate.getFullYear(),
    selectedMonth: currentDate.getMonth() + 1,
    translations: window.translations,
};

var halls, stats;
var urls, urlHalls, urlKills, urlLosses, urlTop10, urlStats;

var killsTable, lossesTable;

function generateUrl(type, entity, entityPk, selectedMonth, selectedYear) {
    return `/killstats/api/${type}/month/${selectedMonth}/year/${selectedYear}/${entity}/${entityPk}/`;
}

function getUrls(entity, entityPk, selectedMonth, selectedYear) {
    return {
        urlHalls: generateUrl('halls', entity, entityPk, selectedMonth, selectedYear),

        urlKills: generateUrl('killmail', entity, entityPk, selectedMonth, selectedYear) + 'kills/',
        urlLosses: generateUrl('killmail', entity, entityPk, selectedMonth, selectedYear) + 'losses/',

        urlTop10: generateUrl('stats/top/10', entity, entityPk, selectedMonth, selectedYear),
        urlStats: generateUrl('stats/all', entity, entityPk, selectedMonth, selectedYear),
    };
}

// Funktion zum Setzen des aktiven Tabs
function setActiveTab(tab) {
    if (tab === 'shame') {
        $('#shame-nav').addClass('active');
        $('#fame-nav').removeClass('active');
        $('#tab-shame').addClass('active show');
        $('#tab-fame').removeClass('active show');
    } else if (tab === 'fame') {
        $('#fame-nav').addClass('active');
        $('#shame-nav').removeClass('active');
        $('#tab-fame').addClass('active show');
        $('#tab-shame').removeClass('active show');
    }
}

// Funktion zum Ermitteln des aktiven Tabs
function getActiveTab() {
    if ($('#shame-nav').hasClass('active')) {
        return 'shame';
    } else if ($('#fame-nav').hasClass('active')) {
        return 'fame';
    }
    return null;
}

function loadStats(url) {
    stats = $.ajax({
        url: url,
        method: 'GET',
        dataType: 'json',
        success: function (data) {
            $('#killboard').show();
            $('#loadingIndicator').addClass('d-none');

            // Überprüfen, ob die Statistikdaten vorhanden sind
            if (data.stats) {
                // Füge die Statistikdaten in den Container ein
                updateStats(data.stats, $('#stats'));
            }
        }
    });
}

function updateStats(stats, container) {
    // Entferne alle vorhandenen Inhalte im Container
    container.empty();

    // Definiere die Kategorien und ihre Titel
    const categories = [
        { key: 'alltime_killer', title: 'All-Time Killer' },
        { key: 'top_killer', title: 'Top Killer' },
        { key: 'top_ship', title: 'Top Ship' },
        { key: 'highest_kill', title: 'Highest Kill' },
        { key: 'alltime_victim', title: 'All-Time Victim' },
        { key: 'top_victim', title: 'Top Victim' },
        { key: 'top_victim_ship', title: 'Top Victim Ship' },
        { key: 'highest_loss', title: 'Highest Loss' }
    ];

    // Iteriere über die Kategorien und erstelle Klone
    categories.forEach(category => {
        const stat = stats[category.key];
        if (!stat) return; // Überspringe, wenn keine Daten vorhanden sind

        const template = $('#stat-template').clone().removeAttr('id').removeClass('d-none');

        // Setze den Titel
        template.find('.stat-title').text(category.title);

        // Setze die spezifischen Daten basierend auf der Kategorie
        if (category.key === 'alltime_killer' || category.key === 'top_killer') {
            template.find('.stat-info').text(`${stat.character__name}: ${stat.alltime_killer || stat.top_killer} Kills`);
            template.find('.stat-portrait').attr('src', `https://images.evetech.net/characters/${stat.character_id}/portrait`);
            template.find('.stat-link').attr('href', `https://zkillboard.com/character/${stat.character_id}`);
        } else if (category.key === 'alltime_victim' || category.key === 'top_victim') {
            template.find('.stat-info').text(`${stat.victim__name}: ${stat.alltime_victim || stat.top_victim} Deaths`);
            template.find('.stat-portrait').attr('src', `https://images.evetech.net/characters/${stat.victim_id}/portrait`);
            template.find('.stat-link').attr('href', `https://zkillboard.com/character/${stat.victim_id}`);
        } else if (category.key === 'top_ship' || category.key === 'top_victim_ship') {
            template.find('.stat-info').text(`${stat.ship__name || stat.victim_ship__name}: ${stat.count || stat.top_victim_ship}`);
            template.find('.stat-portrait').attr('src', `https://images.evetech.net/Render/${stat.ship__id || stat.victim_ship_id}_64.png`);
            template.find('.stat-link').removeAttr('href'); // Kein Link für Schiffe
            template.find('.card-img-zoom').removeClass('card-img-zoom');
        } else if (category.key === 'highest_kill') {
            template.find('.stat-info').text(`Value: ${stat.killmail__victim_total_value.toLocaleString()} ISK`);
            template.find('.stat-portrait').attr('src', `https://images.evetech.net/Render/${stat.killmail__victim_ship__id}_64.png`);
            template.find('.stat-link').attr('href', `https://zkillboard.com/kill/${stat.killmail_id}`);
        } else if (category.key === 'highest_loss') {
            template.find('.stat-info').text(`Value: ${stat.victim_total_value.toLocaleString()} ISK`);
            template.find('.stat-portrait').attr('src', `https://images.evetech.net/Render/${stat.victim_ship__id}_64.png`);
            template.find('.stat-link').attr('href', `https://zkillboard.com/kill/${stat.killmail_id}`);
        }

        // Füge den Klon in den Container ein
        container.append(template);
    });

    // Zeige den Container an
    container.removeClass('d-none');
}

function initializeDataTable(tableId, url, totalValueId) {
    return $(tableId).DataTable({
        'processing': true,
        'serverSide': true,
        'ajax': {
            'url': url,
            'dataSrc': function(json) {
                $(totalValueId).text(json.totalvalue.toLocaleString());
                return json.data;
            }
        },
        'columns': [
            {
                'data': 'killmail_id',
                'render': function(data, type, row) {
                    return '<a href="https://zkillboard.com/kill/' + data + '" target="_blank">' +
                        '<img class="card-img zoom" src="https://imageserver.eveonline.com/types/' + row.victim_ship.id + '/icon/?size=64" height="64" width="64"/>' +
                        '</a>';
                }
            },
            {
                'data': 'victim_ship',
                'render': function(data, type, row) {
                    return row.victim_ship.name;
                }
            },
            {
                'data': 'victim',
                'render': function (data, type, row) {
                    var imageUrl = 'https://imageserver.eveonline.com/';
                    if (data && data.id !== row.victim_alliance_id && data.id !== row.victim_corporation_id) {
                        imageUrl += 'characters/' + data.id + '/portrait/?size=64';
                    } else if (row.victim_alliance_id && data.id === row.victim_alliance_id) {
                        imageUrl += 'alliances/' + row.victim_alliance_id + '/logo/?size=64';
                    } else if (row.victim_corporation_id && data.id === row.victim_corporation_id) {
                        imageUrl += 'corporations/' + row.victim_corporation_id + '/logo/?size=64';
                    } else {
                        // Fallback image URL if no valid ID is available
                        imageUrl += 'icons/no-image.png'; // Beispiel für ein Platzhalterbild
                    }

                    var imageHTML = '<a href="https://zkillboard.com/';
                    if (data && data.id !== row.victim_alliance_id && data.id !== row.victim_corporation_id) {
                        imageHTML += 'character/' + data.id;
                    } else if (row.victim_alliance_id && data.id === row.victim_alliance_id) {
                        imageHTML += 'alliance/' + row.victim_alliance_id;
                    } else if (row.victim_corporation_id && data.id === row.victim_corporation_id) {
                        imageHTML += 'corporation/' + row.victim_corporation_id;
                    }

                    imageHTML += '" target="_blank"> <img class="card-img zoom" src="' + imageUrl + '" height="64" width="64"/></a>';

                    return imageHTML;
                }
            },
            { 'data': 'victim.name'},
            {
                'data': 'victim_total_value',
                'render': function (data, type, row) {
                    // Rückgabe des formatierten Strings mit Farbe und Einheit
                    if (type === 'display') {
                        return data.toLocaleString() + ' ISK';
                    }
                    return data;
                }
            },
            {
                'data': 'killmail_date',
                'render': function (data, type, row) {
                    return moment(data).format('YYYY-MM-DD HH:mm'); // eslint-disable-line no-undef
                }
            },
        ],
        'order': [[5, 'desc']],
        'pageLength': 25,
        'autoWidth': false,
        'columnDefs': [
            { 'sortable': false, 'targets': [0, 2] },
        ],
    });
}

// Funktion zum Aktualisieren der Shame-Daten
function updateShame(shameData) {
    // Entferne alte Inhalte im Container
    $('.shame').empty();

    // Prüfe, ob shame Daten enthält und zeige den entsprechenden Container an oder aus
    if (shameData && shameData.length > 0) {
        $('#hall').removeClass('d-none'); // Container für Hall of Shame anzeigen
        $('#shame-nav').removeClass('d-none'); // Container für Hall of Shame anzeigen
    } else {
        $('#shame-nav').addClass('d-none'); // Container für Hall of Shame ausblenden
        $('#shame-nav').removeClass('active');
    }

    if (shameData) {
        shameData.forEach(function (kill) {
            const shameTemplate = $('#hall-template').clone().removeAttr('id').removeClass('d-none');

            // Header
            shameTemplate.find('.card-header').text(kill.character_name);

            // Body
            shameTemplate.find('.hall-character-link').attr('href', kill.zkb_link);
            shameTemplate.find('.hall-portrait').attr('src', kill.portrait);
            shameTemplate.find('.zkb-link').attr('href', 'https://zkillboard.com/kill/' + kill.killmail_id);
            shameTemplate.find('.ship-logo-img').attr('src', 'https://images.evetech.net/Render/' + kill.ship + '_64.png');

            // Footer
            shameTemplate.find('.total-value').text(kill.totalValue.toLocaleString());
            shameTemplate.find('.ship-name').text(kill.ship_name);
            shameTemplate.find('.zkb-button-link').attr('href', 'https://zkillboard.com/kill/' + kill.killmail_id).attr('target', '_blank');

            // Add the template to the fame container
            $('.shame').append(shameTemplate);
        });
    }
}

// Funktion zum Aktualisieren der Fame-Daten
function updateFame(fameData) {
    // Entferne alte Inhalte im Container
    $('.fame').empty();

    // Prüfe, ob fame Daten enthält und zeige den entsprechenden Container an oder aus
    if (fameData && fameData.length > 0) {
        $('#hall').removeClass('d-none'); // Container für Hall of Fame anzeigen
        $('#fame-nav').removeClass('d-none'); // Container für Hall of Fame anzeigen
    } else {
        $('#fame-nav').addClass('d-none'); // Container für Hall of Fame ausblenden
        $('#fame-nav').removeClass('active');
    }

    if (fameData) {
        fameData.forEach(function (kill) {
            const fameTemplate = $('#hall-template').clone().removeAttr('id').removeClass('d-none');

            // Header
            fameTemplate.find('.card-header').text(kill.character_name);

            // Body
            fameTemplate.find('.hall-character-link').attr('href', kill.zkb_link);
            fameTemplate.find('.hall-portrait').attr('src', kill.portrait);
            fameTemplate.find('.zkb-link').attr('href', 'https://zkillboard.com/kill/' + kill.killmail_id);
            fameTemplate.find('.ship-logo-img').attr('src', 'https://images.evetech.net/Render/' + kill.ship + '_64.png');

            // Footer
            fameTemplate.find('.total-value').text(kill.totalValue.toLocaleString());
            fameTemplate.find('.ship-name').text(kill.ship_name);
            fameTemplate.find('.zkb-button-link').attr('href', 'https://zkillboard.com/kill/' + kill.killmail_id).attr('target', '_blank');

            // Add the template to the fame container
            $('.fame').append(fameTemplate);
        });
    }
    // Setze den aktiven Tab
    setActiveTab();
}

function updateData(selectedMonth, selectedYear) {
    var urls;
    var activeTab = getActiveTab();

    urls = getUrls(entityType, entityPk, selectedMonth, selectedYear);

    const { urlHalls, urlKills, urlLosses, urlTop10, urlStats } = urls;

    $('#killboard').addClass('d-none');
    $('#hall').addClass('d-none');
    $('#loadingIndicator').removeClass('d-none');

    // Initialisiere die DataTables nur, wenn sie noch nicht initialisiert sind
    if (!$.fn.DataTable.isDataTable('#kills')) {
        killsTable = initializeDataTable('#kills', urlKills, '#total-value-kills');
    } else {
        killsTable.ajax.url(urlKills).load();
    }

    if (!$.fn.DataTable.isDataTable('#losses')) {
        lossesTable = initializeDataTable('#losses', urlLosses, '#total-value-losses');
    } else {
        lossesTable.ajax.url(urlLosses).load();
    }

    // AJAX-Anfrage für Halls
    halls = $.ajax({
        url: urlHalls,
        method: 'GET',
        dataType: 'json',
        success: function (data) {
            $('#killboard').removeClass('d-none');
            $('#loadingIndicator').addClass('d-none');
            updateShame(data[0].shame);
            updateFame(data[0].fame);
            setActiveTab(activeTab);
        }
    });

    loadStats(urlStats);

    $('#top10').html('<button type="button" class="btn btn-secondary" data-bs-toggle="modal" data-bs-target="#modalViewTop10KillerContainer" data-ajax_url="' + urlTop10 + '">Top 10</button>');
}

document.addEventListener('DOMContentLoaded', function () {
    yearDropdown.addEventListener('click', event => handleDropdownClick(event, 'year', state));
    monthDropdown.addEventListener('click', event => handleDropdownClick(event, 'month', state));
    var activeTab = getActiveTab();
    updateData(state.selectedMonth, state.selectedYear);
});
