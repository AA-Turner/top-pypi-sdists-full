from django.urls import path, re_path
from django.views.generic import TemplateView
from .views import SpreadsheetMigrator

"""
It is important that the path to the root should be after the child paths.
"""
urlpatterns = [
    re_path('report/*', TemplateView.as_view(template_name='spreadsheet_migrator_index.html'),
         name='spreadsheet-migrator-index'),
    path('', TemplateView.as_view(template_name='spreadsheet_migrator_index.html'), name='spreadsheet-migrator-index'),
    path('migrate/', SpreadsheetMigrator.as_view()),
]
