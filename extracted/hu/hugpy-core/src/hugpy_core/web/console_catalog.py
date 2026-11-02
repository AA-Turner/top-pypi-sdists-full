"""Compact model list for the browser; evidence stays in the model database."""


def console_catalog_rows(rows: list) -> list:
    bulky = {'worker_assignments', 'quants', 'copies', 'weights', 'hugpy_json'}
    result = []
    for row in rows:
        summary = {key: value for key, value in row.items() if key not in bulky}
        # Copy locations/status are useful in the list; embedded discovery
        # manifests duplicate the full model evidence and dominate page size.
        if isinstance(summary.get('central_copies'), list):
            summary['central_copies'] = [
                {key: value for key, value in copy.items() if key != 'details'}
                if isinstance(copy, dict) else copy
                for copy in summary['central_copies']]
        result.append(summary)
    return result
