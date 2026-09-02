

class AdminSearchPlusMixin:
    """
    Admin mixin that limits searches to specified field
    """
    admin_search_plus = True
    show_full_result_count = False
    show_result_count = False

    def lookup_allowed(self, lookup, value, *args, **kwargs):
        if lookup.replace('__contains', '') in self.search_fields:
            return True

        return super().lookup_allowed(lookup, value, *args, **kwargs)
