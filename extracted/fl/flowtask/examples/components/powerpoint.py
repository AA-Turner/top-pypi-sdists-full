from pathlib import Path
from pptx.util import Inches
from flowtask.interfaces.powerpoint import PowerPointClient

# Instantiate the handler
handler = PowerPointClient()

# # Create slide contents using the create_slide method
# slide1 = handler.create_slide(
#     text_content='Slide 1 Text',
#     image_path='image1.png',
#     image_size=(1, 2, 5),  # left=1 inch, top=2 inches, width=5 inches
#     font_size=24,
#     font_color='FF0000',
#     font_name='Arial',
#     layout_index=2  # Use layout index 2 for this slide
# )

# slide2 = handler.create_slide(
#     text_content='Slide 2 Text',
#     font_size=18,
#     font_color='0000FF',
#     font_name='Verdana'
# )

# Define slide contents with specific master, layout, and placeholder mappings
slide1 = {
    'master_index': 0,  # Select master slide 1
    'layout_index': 1,  # Different layout
    'text_content': [
        {'Title 1': {"text": "Store Overview"}},
        {'Subtitle 2': {"text": "Customer Insights"}}
    ]
}

slide2 = {
    'master_index': 0,  # Select master slide 0
    'layout_index': 1,  # Layout index within the master
    'text_content': [
        {'Title 1': {"text": "Best Buy | ", "font_name": "Arial", "font_size": 32, "font_color": '000079', "bold": True}},
        {'Title 1': {"text": "#BBY1013, Glen Allen, VA", "font_name": "Arial", "font_size": 32, "font_color": '808080', "new_paragraph": False}},
        {"Text Placeholder 3": {"text": "Ink Wall", "font_name": "Arial", "font_size": 32, "font_color": '808080', "bold": True, "new_paragraph": True}}
    ],
    'image': {
        'path': 'image1.png',
        'placeholder_id': 'Picture Placeholder 2',
        'top': 'center',
        'left': 'center',
        'scale_factor': 0.38
    }
}

# Prepare the slide contents iterator
slide_contents = [slide2]

# Create a presentation from a template
template_path = Path('epson-template4.pptx')
handler.list_placeholder_ids(template_path)

output_file_path = Path('presentation_from_template.pptx')

handler.create_presentation_from_template(
    template_path,
    slide_contents,
    output_file_path,
    default_layout_index=1  # Default layout index to use if not specified per slide
)
