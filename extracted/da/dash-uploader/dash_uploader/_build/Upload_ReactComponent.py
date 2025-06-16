# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Upload_ReactComponent(Component):
    """An Upload_ReactComponent component.
The Upload component

Keyword arguments:

- id (string; default 'default-dash-uploader-id'):
    User supplied id of this component.

- cancelButton (boolean; default True):
    Whether or not to have a cancel button.

- chunkSize (number; default 1024 * 1024):
    Size of file chunks to send to server.

- className (string; default 'dash-uploader-default'):
    Class to add to the upload component by default.

- completeClass (string; default 'dash-uploader-complete'):
    Class to add to the upload component when it is complete.

- completeStyle (dict; optional):
    Style when upload is completed (upload finished).

- completedMessage (string; default 'Complete! '):
    Message to display when upload completed.

- defaultStyle (dict; optional):
    Style attributes to add to the upload component.

- disableDragAndDrop (boolean; default False):
    Whether or not to allow file drag and drop.

- disabled (boolean; default False):
    Whether or not to allow file uploading.

- disabledClass (string; default 'dash-uploader-disabled'):
    Class to add to the upload component when it is disabled.

- disabledMessage (string; default 'The uploader is disabled.'):
    Message to display when upload disabled.

- disabledStyle (dict; optional):
    Style when upload is disabled.

- fileNames (list of strings; optional):
    The names of the files uploaded.

- filetypes (list of strings; default undefined):
    List of allowed file types, e.g. ['jpg', 'png'].

- hoveredClass (string; default 'dash-uploader-hovered'):
    Class to add to the upload component when it is hovered.

- isCompleted (boolean; default False):
    The boolean flag telling if upload is completed.

- maxFileSize (number; default 1024 * 1024 * 10):
    Maximum size per file in bytes.

- maxFiles (number; default 1):
    Maximum number of files that can be uploaded in one session.

- pauseButton (boolean; default True):
    Whether or not to have a pause button.

- pausedClass (string; default 'dash-uploader-paused'):
    Class to add to the upload component when it is paused.

- service (string; default '/API/dash-uploader'):
    The service to send the files to.

- simultaneousUploads (number; optional):
    Number of simultaneous uploads to select.

- simultaneuosUploads (number; default 1):
    Number of simulaneous uploads.

- startButton (boolean; default True):
    Whether or not to have a start button.

- textLabel (string; default 'Click Here to Select a File'):
    The string to display in the upload component.

- upload_id (string; default ''):
    The ID for the upload event (for example, session ID).

- uploadingClass (string; default 'dash-uploader-uploading'):
    Class to add to the upload component when it is uploading.

- uploadingStyle (dict; optional):
    Style when upload is in progress."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_uploader'
    _type = 'Upload_ReactComponent'
    @_explicitize_args
    def __init__(self, maxFiles=Component.UNDEFINED, maxFileSize=Component.UNDEFINED, chunkSize=Component.UNDEFINED, simultaneousUploads=Component.UNDEFINED, service=Component.UNDEFINED, className=Component.UNDEFINED, hoveredClass=Component.UNDEFINED, disabledClass=Component.UNDEFINED, pausedClass=Component.UNDEFINED, completeClass=Component.UNDEFINED, uploadingClass=Component.UNDEFINED, defaultStyle=Component.UNDEFINED, disabledStyle=Component.UNDEFINED, uploadingStyle=Component.UNDEFINED, completeStyle=Component.UNDEFINED, textLabel=Component.UNDEFINED, disabledMessage=Component.UNDEFINED, completedMessage=Component.UNDEFINED, fileNames=Component.UNDEFINED, filetypes=Component.UNDEFINED, startButton=Component.UNDEFINED, pauseButton=Component.UNDEFINED, cancelButton=Component.UNDEFINED, disabled=Component.UNDEFINED, disableDragAndDrop=Component.UNDEFINED, id=Component.UNDEFINED, isCompleted=Component.UNDEFINED, upload_id=Component.UNDEFINED, simultaneuosUploads=Component.UNDEFINED, onUploadErrorCallback=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'cancelButton', 'chunkSize', 'className', 'completeClass', 'completeStyle', 'completedMessage', 'defaultStyle', 'disableDragAndDrop', 'disabled', 'disabledClass', 'disabledMessage', 'disabledStyle', 'fileNames', 'filetypes', 'hoveredClass', 'isCompleted', 'maxFileSize', 'maxFiles', 'pauseButton', 'pausedClass', 'service', 'simultaneousUploads', 'simultaneuosUploads', 'startButton', 'textLabel', 'upload_id', 'uploadingClass', 'uploadingStyle']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'cancelButton', 'chunkSize', 'className', 'completeClass', 'completeStyle', 'completedMessage', 'defaultStyle', 'disableDragAndDrop', 'disabled', 'disabledClass', 'disabledMessage', 'disabledStyle', 'fileNames', 'filetypes', 'hoveredClass', 'isCompleted', 'maxFileSize', 'maxFiles', 'pauseButton', 'pausedClass', 'service', 'simultaneousUploads', 'simultaneuosUploads', 'startButton', 'textLabel', 'upload_id', 'uploadingClass', 'uploadingStyle']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(Upload_ReactComponent, self).__init__(**args)
