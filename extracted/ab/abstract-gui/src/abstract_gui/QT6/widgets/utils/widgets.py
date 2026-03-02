from .kwargs_utils import *
from PyQt6.QtWidgets import QVBoxLayout
def getWidget(parent_layout: QVBoxLayout, **wkwargs):
    """Add either (label + widget) or a nested layout into parent_layout."""
    label = wkwargs['label']
    widget = wkwargs['widget']
    nested = wkwargs['nested_layout']
    stretch = wkwargs['stretch']

    if nested is not None:
        parent_layout.addLayout(nested, stretch)
    else:
        if label:
            parent_layout.addWidget(QLabel(label), stretch)  # stretch must be positional
        parent_layout.addWidget(widget, stretch)

def getListBox(*triplets, layout=None):
    layout = layout or QVBoxLayout()
    for t in triplets:
        wkwargs = createWidgetKwargs(*t)
        getWidget(layout, **wkwargs)
    return layout
def getQHBox(*triplets, label=None,layout=None):
    layout = layout or QHBoxLayout()
    label= label or 'QHBOX'
    layout.addStretch(1)
    layout.addWidget(QLabel(label))
    for t in triplets:
        layout.addWidget( t)
    return layout
def getRow(*columns, layout=None):
    layout = layout or QHBoxLayout()
    for col in columns:
        layout.addLayout(col, 1)
    return layout
def getRadioButton(self,label,group,checked=True,func = None):
    label=label or "radio"
    rbutton = QRadioButton(label)
    group.addButton(rbutton)
    self.rbutton.setChecked(checked)
    group = QButtonGroup(self)
    self.rbutton.toggled.connect(func)
    return self.rbutton
