# encoding: utf-8

from ..window.loading import LoadingWindow


def start_loading(parent,
                  wait_func):

    loading = LoadingWindow(wait_func=wait_func,
                            parent_geometry=parent.winfo_toplevel().winfo_geometry())

    loading.transient(parent)
    loading.grab_set()
    parent.wait_window(loading)
