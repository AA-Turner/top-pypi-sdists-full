
import gradio as gr
from app import demo as app
import os

_docs = {'RangeSlider': {'description': 'A slider component that allows the user to select a range of values.', 'members': {'__init__': {'minimum': {'type': 'float', 'default': '0', 'description': 'minimum value for slider.'}, 'maximum': {'type': 'float', 'default': '100', 'description': 'maximum value for slider.'}, 'value': {'type': 'typing.Union[\n    typing.Tuple[float, float], typing.Callable, NoneType\n][typing.Tuple[float, float][float, float], Callable, None]', 'default': 'None', 'description': 'default value. If callable, the function will be called whenever the app loads to set the initial value of the component. Ignored if randomized=True.'}, 'step': {'type': 'float | None', 'default': 'None', 'description': 'increment between slider values.'}, 'label': {'type': 'str | None', 'default': 'None', 'description': 'The label for this component. Appears above the component and is also used as the header if there are a table of examples for this component. If None and used in a `gr.Interface`, the label will be the name of the parameter this component is assigned to.'}, 'info': {'type': 'str | None', 'default': 'None', 'description': 'additional component description.'}, 'every': {'type': 'float | None', 'default': 'None', 'description': "If `value` is a callable, run the function 'every' number of seconds while the client connection is open. Has no effect otherwise. The event can be accessed (e.g. to cancel it) via this component's .load_event attribute."}, 'show_label': {'type': 'bool | None', 'default': 'None', 'description': 'if True, will display label.'}, 'container': {'type': 'bool', 'default': 'True', 'description': 'If True, will place the component in a container - providing some extra padding around the border.'}, 'scale': {'type': 'int | None', 'default': 'None', 'description': 'relative size compared to adjacent Components. For example if Components A and B are in a Row, and A has scale=2, and B has scale=1, A will be twice as wide as B. Should be an integer. scale applies in Rows, and to top-level Components in Blocks where fill_height=True.'}, 'min_width': {'type': 'int', 'default': '160', 'description': 'minimum pixel width, will wrap if not sufficient screen space to satisfy this value. If a certain scale value results in this Component being narrower than min_width, the min_width parameter will be respected first.'}, 'interactive': {'type': 'bool | None', 'default': 'None', 'description': 'if True, slider will be adjustable; if False, adjusting will be disabled. If not provided, this is inferred based on whether the component is used as an input or output.'}, 'visible': {'type': 'bool', 'default': 'True', 'description': 'If False, component will be hidden.'}, 'elem_id': {'type': 'str | None', 'default': 'None', 'description': 'An optional string that is assigned as the id of this component in the HTML DOM. Can be used for targeting CSS styles.'}, 'elem_classes': {'type': 'list[str] | str | None', 'default': 'None', 'description': 'An optional list of strings that are assigned as the classes of this component in the HTML DOM. Can be used for targeting CSS styles.'}, 'render': {'type': 'bool', 'default': 'True', 'description': 'If False, component will not render be rendered in the Blocks context. Should be used if the intention is to assign event listeners now but render the component later.'}}, 'postprocess': {'value': {'type': 'typing.Optional[typing.Tuple[float, float]][\n    typing.Tuple[float, float][float, float], None\n]', 'description': 'Expects an {int} or {float} returned from function and sets slider value to it as long as it is within range (otherwise, sets to minimum value).'}}, 'preprocess': {'return': {'type': 'typing.Tuple[float, float][float, float]', 'description': 'Passes slider value as a {float} into the function.'}, 'value': None}}, 'events': {'change': {'type': None, 'default': None, 'description': 'Triggered when the value of the RangeSlider changes either because of user input (e.g. a user types in a textbox) OR because of a function update (e.g. an image receives a value from the output of an event trigger). See `.input()` for a listener that is only triggered by user input.'}, 'input': {'type': None, 'default': None, 'description': 'This listener is triggered when the user changes the value of the RangeSlider.'}, 'release': {'type': None, 'default': None, 'description': 'This listener is triggered when the user releases the mouse on this RangeSlider.'}}}, '__meta__': {'additional_interfaces': {}, 'user_fn_refs': {'RangeSlider': []}}}

abs_path = os.path.join(os.path.dirname(__file__), "css.css")

with gr.Blocks(
    css=abs_path,
    theme=gr.themes.Default(
        font_mono=[
            gr.themes.GoogleFont("Inconsolata"),
            "monospace",
        ],
    ),
) as demo:
    gr.Markdown(
"""
# `gradio_rangeslider`

<div style="display: flex; gap: 7px;">
<a href="https://pypi.org/project/gradio_rangeslider/" target="_blank"><img alt="PyPI - Version" src="https://img.shields.io/pypi/v/gradio_rangeslider"></a> <a href="https://github.com/freddyaboulton/gradio-range-slider/issues" target="_blank"><img alt="Static Badge" src="https://img.shields.io/badge/Issues-white?logo=github&logoColor=black"></a> <a href="https://huggingface.co/spaces/freddyaboulton/gradio_rangeslider/discussions" target="_blank"><img alt="Static Badge" src="https://img.shields.io/badge/%F0%9F%A4%97%20Discuss-%23097EFF?style=flat&logoColor=black"></a>
</div>

🛝 Slider component for selecting a range of values
""", elem_classes=["md-custom"], header_links=True)
    app.render()
    gr.Markdown(
"""
## Installation

```bash
pip install gradio_rangeslider
```

## Usage

```python

import gradio as gr
from gradio_rangeslider import RangeSlider
from pathlib import Path

text = "## The range is: {min} to {max}"

docs = Path(__file__).parent / "docs.md"

with gr.Blocks() as demo:
    with gr.Tabs():
        with gr.Tab("Demo"):
            gr.Markdown(\"\"\"## 🛝 RangeSlider

            ## Drag either end and see the selected endpoints update in real-time.
            \"\"\") 
            range_slider = RangeSlider(minimum=0, maximum=100, value=(0, 100))
            range_ = gr.Markdown(value=text.format(min=0, max=100))
            range_slider.change(lambda s: text.format(min=s[0], max=s[1]), range_slider, range_,
                                show_progress="hide", trigger_mode="always_last")
            gr.Slider(label="Normal slider", minimum=0, maximum=100, value=50, interactive=True)
            gr.Examples([(20, 30), (40, 80)], inputs=[range_slider])
        with gr.Tab("Docs"):
            gr.Markdown(docs.read_text())


if __name__ == "__main__":
    demo.launch()

```
""", elem_classes=["md-custom"], header_links=True)


    gr.Markdown("""
## `RangeSlider`

### Initialization
""", elem_classes=["md-custom"], header_links=True)

    gr.ParamViewer(value=_docs["RangeSlider"]["members"]["__init__"], linkify=[])


    gr.Markdown("### Events")
    gr.ParamViewer(value=_docs["RangeSlider"]["events"], linkify=['Event'])




    gr.Markdown("""

### User function

The impact on the users predict function varies depending on whether the component is used as an input or output for an event (or both).

- When used as an Input, the component only impacts the input signature of the user function.
- When used as an output, the component only impacts the return signature of the user function.

The code snippet below is accurate in cases where the component is used as both an input and an output.

- **As input:** Is passed, passes slider value as a {float} into the function.
- **As output:** Should return, expects an {int} or {float} returned from function and sets slider value to it as long as it is within range (otherwise, sets to minimum value).

 ```python
def predict(
    value: typing.Tuple[float, float][float, float]
) -> typing.Optional[typing.Tuple[float, float]][
    typing.Tuple[float, float][float, float], None
]:
    return value
```
""", elem_classes=["md-custom", "RangeSlider-user-fn"], header_links=True)




    demo.load(None, js=r"""function() {
    const refs = {};
    const user_fn_refs = {
          RangeSlider: [], };
    requestAnimationFrame(() => {

        Object.entries(user_fn_refs).forEach(([key, refs]) => {
            if (refs.length > 0) {
                const el = document.querySelector(`.${key}-user-fn`);
                if (!el) return;
                refs.forEach(ref => {
                    el.innerHTML = el.innerHTML.replace(
                        new RegExp("\\b"+ref+"\\b", "g"),
                        `<a href="#h-${ref.toLowerCase()}">${ref}</a>`
                    );
                })
            }
        })

        Object.entries(refs).forEach(([key, refs]) => {
            if (refs.length > 0) {
                const el = document.querySelector(`.${key}`);
                if (!el) return;
                refs.forEach(ref => {
                    el.innerHTML = el.innerHTML.replace(
                        new RegExp("\\b"+ref+"\\b", "g"),
                        `<a href="#h-${ref.toLowerCase()}">${ref}</a>`
                    );
                })
            }
        })
    })
}

""")

demo.launch()
