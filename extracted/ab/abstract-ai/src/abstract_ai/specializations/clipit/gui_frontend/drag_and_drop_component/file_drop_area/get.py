import inspect
from PyQt5 import QtWidgets, QtCore

# 1) Constructor signature(s)
print(inspect.signature(QtWidgets.QListWidgetItem.__init__))
# e.g. __init__(self, *args, **kwargs)  # overloaded under the hood

# 2) All public members (methods, signals, properties, …)
all_members = [m for m in dir(QtWidgets.QListWidgetItem) if not m.startswith('_')]
print("All members:", all_members)

# 3) Which of those are callables?
methods = [m for m in all_members
           if callable(getattr(QtWidgets.QListWidgetItem, m))]
print("Methods & signals:", methods)

# 4) Which are non-callable properties?
props = [m for m in all_members
         if not callable(getattr(QtWidgets.QListWidgetItem, m))]
print("Attributes/properties:", props)

# 5) If you want to know what “roles” you can pass to item.data()/setData():

roles = [(name, getattr(QtCore.Qt, name))
         for name in dir(QtCore.Qt)
         if name.endswith('Role')]
print("Available data‐roles (name, int):\n", roles)
