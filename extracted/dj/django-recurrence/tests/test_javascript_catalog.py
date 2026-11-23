import pytest
from django.urls import include, path
from django.views.i18n import JavaScriptCatalog, JSONCatalog

from recurrence import forms


class URLconf:
    def __init__(self, urlpatterns):
        self.urlpatterns = urlpatterns


def use_urlpatterns(settings, monkeypatch, urlpatterns):
    monkeypatch.setattr(forms, '_recurrence_javascript_catalog_view', None)
    settings.ROOT_URLCONF = URLconf(urlpatterns)


@pytest.mark.parametrize('urlpatterns', [
    # the catalog of django-recurrence, as in the installation docs
    [path('jsi18n/', JavaScriptCatalog.as_view(packages=['recurrence']), name='javascript-catalog')],
    # without a name
    [path('jsi18n/', JavaScriptCatalog.as_view(packages=['recurrence']))],
    # without packages the view serves every installed application
    [path('jsi18n/', JavaScriptCatalog.as_view())],
    # other catalogs are skipped
    [
        path('admin-jsi18n/', JavaScriptCatalog.as_view(packages=['django.contrib.admin'])),
        path('jsi18n.json', JSONCatalog.as_view(packages=['recurrence'])),
        path('jsi18n/', JavaScriptCatalog.as_view(packages=['django.contrib.admin', 'recurrence'])),
    ],
])
def test_catalog_is_found(settings, monkeypatch, urlpatterns):
    use_urlpatterns(settings, monkeypatch, urlpatterns)

    assert forms.find_recurrence_i18n_js_catalog() == '/jsi18n/'
    # the catalog has to be loaded before the widget scripts
    assert forms.RecurrenceWidget().media._js[0] == '/jsi18n/'


def test_catalog_is_found_in_a_namespace(settings, monkeypatch):
    catalog = path('jsi18n/', JavaScriptCatalog.as_view(packages=['recurrence']), name='catalog')
    use_urlpatterns(settings, monkeypatch, [
        path('calendar/', include(([catalog], 'calendar'))),
    ])

    assert forms.find_recurrence_i18n_js_catalog() == '/calendar/jsi18n/'


@pytest.mark.parametrize('urlpatterns', [
    [],
    [path('jsi18n/', JavaScriptCatalog.as_view(packages=['django.contrib.admin']))],
    [path('jsi18n.json', JSONCatalog.as_view(packages=['recurrence']))],
])
def test_media_without_a_catalog(settings, monkeypatch, urlpatterns):
    use_urlpatterns(settings, monkeypatch, urlpatterns)

    assert forms.find_recurrence_i18n_js_catalog() is None
    assert forms.RecurrenceWidget().media._js == [
        'admin/js/vendor/jquery/jquery.min.js',
        'admin/js/jquery.init.js',
        '/fakestatictrees/recurrence/js/recurrence.js',
        '/fakestatictrees/recurrence/js/recurrence-widget.js',
        '/fakestatictrees/recurrence/js/recurrence-widget.init.js',
    ]


def test_url_set_by_the_project_is_used(settings, monkeypatch):
    use_urlpatterns(settings, monkeypatch, [])
    monkeypatch.setattr(forms, '_recurrence_javascript_catalog_url', '/custom/jsi18n/')

    assert forms.find_recurrence_i18n_js_catalog() == '/custom/jsi18n/'
