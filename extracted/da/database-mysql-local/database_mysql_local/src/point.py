from database_infrastructure_local.point import Point

# ! this fiel is for backward compatibility
# ! a lot of backeages import point from database_mysql_local,
# ! update them to import from database_infrastructure_local instead then this file can be removed/ deleted
__all__ = ["Point"]
