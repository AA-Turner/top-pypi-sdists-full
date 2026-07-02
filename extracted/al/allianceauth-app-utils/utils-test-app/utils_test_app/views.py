from django.shortcuts import render


def index(request):
    """Start page with ability to login"""
    return render(request, "utils_test_app/index.html")
