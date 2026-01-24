from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def embedded_view_example(request: HttpRequest) -> HttpResponse:
    return render(request, "example_app/embedded_view.html")
