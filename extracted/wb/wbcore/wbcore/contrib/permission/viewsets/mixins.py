from wbcore.contrib.permission.filters import ObjectPermissionsFilter
from wbcore.viewsets.mixins import FilterMixin


class ObjectPermissionFilterMixin(FilterMixin):
    filter_backends = (ObjectPermissionsFilter, *FilterMixin.filter_backends)
