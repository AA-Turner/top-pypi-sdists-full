import PySimpleGUI as sg

class RightClickManager:
    from abstract_utilities import HistoryManager
    def __init__(self):
        self.keys=[]
        self.default_combo_values = []

        self.multi_text=''
        # Create an instance of HistoryManager
        self.history_mgr = HistoryManager()
        self.right_click_keys = ['Right','Redo', 'Undo', 'Cut', 'Copy', 'Paste', 'Delete', 'Select All', 'Key Term Search', 'Text Parsing']
    def get_right_click(self, key):
        self.keys.append(key)
        click = [key, []]
        for each in self.right_click_keys[1:]:
            click[1].append(f'{each}::{key}')
        return click
    def right_click_event(self,values,event,window):
        if '::' in event:
            action, component_key = event.split('::')
        if action in self.right_click_keys:
            if component_key not in self.history_mgr.history_names:
                history_manager.add_history_name(component_key, values[component_key])
        if action == 'delim':
            delim = values['delim']
            blocks = multi_text.split(delim)
            slice_it_up(blocks,window,delimiter=delim)
        if action == 'Undo':
            last_data = self.history_mgr.undo(component_key)
            window[component_key].update(last_data)
        elif action == 'Redo':
            last_data = self.history_mgr.redo(component_key)
            window[component_key].update(last_data)    
        elif action == 'Cut':
            window[component_key].Widget.event_generate('<<Cut>>')
        elif action ==  'Copy':
            window[component_key].Widget.event_generate('<<Copy>>')
        elif action ==  'Paste':
            window[component_key].Widget.event_generate('<<Paste>>')
        elif action ==  'Delete':
            window[component_key].Widget.event_generate('<<Clear>>')
        elif action ==  'Select All':
            window[component_key].Widget.event_generate('<<SelectAll>>') 
        elif action == 'Key Term Search' or action == 'Text Parsing':
            drop_down_selection = event  # Do what you want with the selection    
      

# Create an instance of MultilineSlider
history_manager = HistoryManager()
multiline_slider = MultilineSlider(history_manager)

# Define the GUI layout
layout = [
    [sg.Multiline(size=(40, 10), key='-MULTI-', right_click_menu=multiline_slider.get_right_click('-MULTI-'))],
    [sg.Button('Submit')]
]

# Create the window
window = sg.Window('Multiline with Right Click', layout)

# Event loop
while True:
    event, values = window.read()
    multiline_slider.right_click_event(values, event, window)
 

window.close()
