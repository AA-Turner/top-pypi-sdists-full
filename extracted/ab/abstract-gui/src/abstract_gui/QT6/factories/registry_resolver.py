from ..imports import inspect,PyQt6,QtWidgets,QtCore,inspect
def get_func():
    # list all classes in QtWidgets
    all_widgets = [
        getattr(QtWidgets, name)
        for name in dir(QtWidgets)
        if inspect.isclass(getattr(QtWidgets, name))
    ]
    #values["mapping"][attr]
    mapping = {'PyQt6':{"module":PyQt6,"mapping":{}}}
    cls = QtWidgets
    for key,values in mapping.items():
        module = values.get('module')
        module_mapping = values.get('mapping')
        attributes = dir(module)
        attrs =  [n for n in dir(module) if getattr(module, n, None)]
        for attr in attrs:
             attr_values = dir(getattr(module, attr))
             values["mapping"][attr]={}
             obj = getattr(module, attr)
             for attr_value in dir(obj):
                sub_attr_values = dir(getattr(obj, attr_value, None))
                values["mapping"][attr][attr_value] = sub_attr_values
                input(values["mapping"][attr][attr_value])        

    print("\nCallable methods:")
    print([n for n in dir(cls) if callable(getattr(cls, n, None))])

    print("\nInit signature:")
    print(inspect.signature(cls))

