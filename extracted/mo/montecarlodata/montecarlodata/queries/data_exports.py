# Queries related to Data Exports

GET_DATA_EXPORT_URL = """
    query getDataExportUrl($dataExportName: DataExportNames!) {
        getDataExportUrl(dataExportName: $dataExportName) {
            url
        }
    }
"""
