from ..imports import *
from .utils import *
def getKwargs(default=None, key=None, **kwargs):
    key = key or ''
    val = kwargs.pop(key, default)
    return val, kwargs

def getLayoutKwargs(layout=None, **kwargs):
    return getKwargs(layout, 'layout', **kwargs)

def getStretchKwargs(stretch=None, **kwargs):
    return getKwargs(0 if stretch is None else stretch, 'stretch', **kwargs)

def getLabelKwargs(label=None, **kwargs):
    return getKwargs('' if label is None else label, 'label', **kwargs)

def getWidgetKwargs(widget=None, **kwargs):
    # IMPORTANT: do NOT create a default QListWidget() here
    # We require the *actual* instance to be passed in.
    return getKwargs(widget, 'widget', **kwargs)


def createWidgetKwargs(*args, **kwargs):
    """
    Accepts (QWidget|QLayout, label: str, stretch: int) in any order.
    Returns {'widget': QWidget|None, 'nested_layout': QLayout|None, 'label': str, 'stretch': int}
    """
    widget = None
    nested_layout = None
    label = 'widget'
    stretch = 1

    for arg in args:
        if isinstance(arg, QWidget):
            widget = arg
        elif isinstance(arg, QLayout):
            nested_layout = arg
        elif isinstance(arg, str):
            label = arg
        elif isinstance(arg, int):
            stretch = arg

    # keyword overrides
    widget = kwargs.pop('widget', widget)
    nested_layout = kwargs.pop('nested_layout', nested_layout)
    label = kwargs.pop('label', label)
    stretch = kwargs.pop('stretch', stretch)

    if widget is None and nested_layout is None:
        raise ValueError("Pass a QWidget or QLayout.")

    return {'widget': widget, 'nested_layout': nested_layout, 'label': label, 'stretch': stretch}
def createWidgetKwargs(*args,**kwargs):
    og_widget = findTheWidget(*args,**kwargs)
    defaults = {
        "widget":{"value":QListWidget(),"type":type(QListWidget())},
        "label":{"value":'widget',"type":str},
        "stretch":{"value":1,"type":int},
        "nested_layout":{"value":None,"type":set()},
        }
    def get_dvalue(key):
        dvalues = defaults.get(key,{})
        value = dvalues.get('value')
        return value
    def get_dtype(key):
        dvalues = defaults.get(key)
        typ = dvalues.get('type')
        return typ
    def default_type_eval(key,arg):
        dtype = get_dtype(key)
        if dtype:
            return isinstance(arg,dtype)
        return False
    def default_widget_type_eval(key,arg):
        return value_is_widget(key,arg)
    widget_js = {
        "widget":None,
        "label":None,
        "stretch":None,
        "nested_layout":None
        }
    def get_widgVal(key,widgetJs={}):
        inwidget = widgetJs.get('widget')
        dvalue = get_dvalue(key)
        widgetJs= widgetJs or widget_js
        widgVal =  widgetJs.get(key,dvalue)
        #print(f"key == {key}\nvalues == {values}\ndefValue == {dvalue}\nwidgVal == {widgVal}")
        widgetJs[key] = widgVal if widgVal != None else dvalue
        outwidget = widgetJs.get('widget')
        return widgetJs
    nuKwargs={}
    for arg in args:
        
            for key,values in defaults.items():
               kvalue = kwargs.get(key)
               if kvalue == None and default_type_eval(key,arg) or default_widget_type_eval(key,arg):
                     nuKwargs[key]=arg

    kwargs.update(nuKwargs)
    og_widget
    for key,values in defaults.items():
        kwargs = get_widgVal(key,widgetJs=kwargs)
    return kwargs
