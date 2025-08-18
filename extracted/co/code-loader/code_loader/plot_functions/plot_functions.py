# mypy: ignore-errors


import os

from code_loader.inner_leap_binder.leapbinder import mapping_runtime_mode_env_var_mame

if not os.environ.get(mapping_runtime_mode_env_var_mame):
    try:
        import matplotlib.pyplot as plt  # type: ignore
    except ImportError:
        raise ImportError(
            "Matplotlib is not installed. Please install it using 'pip install matplotlib' to visualize Leap data."
        )


import numpy as np
from code_loader.contract.enums import LeapDataType
from textwrap import wrap
import math

from code_loader.contract.visualizer_classes import LeapImage, LeapImageWithBBox, LeapGraph, LeapText, \
    LeapHorizontalBar, LeapImageMask, LeapTextMask, LeapImageWithHeatmap

def run_only_on_non_mapping_mode():
    """
    Decorator to ensure that the function is only run when not in mapping mode.
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            if os.environ.get(mapping_runtime_mode_env_var_mame):
                print(f"Skipping {func.__name__} in mapping mode.")
                return
            return func(*args, **kwargs)
        return wrapper
    return decorator


@run_only_on_non_mapping_mode()
def plot_image_with_b_box(leap_data: LeapImageWithBBox, title: str) -> None:
    """
    Plot an image with overlaid bounding boxes.

    Returns:
        None

    Example:
        image_data = np.random.rand(100, 100, 3).astype(np.float32)
        bbox = BoundingBox(x=0.5, y=0.5, width=0.2, height=0.2, confidence=0.9, label="object")
        leap_image_with_bbox = LeapImageWithBBox(data=image_data, bounding_boxes=[bbox])
        title = "Image With bbox"
        visualize(leap_image_with_bbox, title)
    """

    image = leap_data.data
    bounding_boxes = leap_data.bounding_boxes

    # Create figure and axes
    fig, ax = plt.subplots(1)
    fig.patch.set_facecolor('black')
    ax.set_facecolor('black')

    # Display the image
    ax.imshow(image)
    ax.set_title(title, color='white')

    # Draw bounding boxes on the image
    for bbox in bounding_boxes:
        x, y, width, height = bbox.x, bbox.y, bbox.width, bbox.height
        confidence, label = bbox.confidence, bbox.label

        # Convert relative coordinates to absolute coordinates
        abs_x = x * image.shape[1]
        abs_y = y * image.shape[0]
        abs_width = width * image.shape[1]
        abs_height = height * image.shape[0]

        # Create a rectangle patch
        rect = plt.Rectangle(
            (abs_x - abs_width / 2, abs_y - abs_height / 2),
            abs_width, abs_height,
            linewidth=3, edgecolor='r', facecolor='none'
        )

        # Add the rectangle to the axes
        ax.add_patch(rect)

        # Display label and confidence
        ax.text(abs_x - abs_width / 2, abs_y - abs_height / 2 - 5,
                f"{label} {confidence:.2f}", color='r', fontsize=8,
                bbox=dict(facecolor='white', alpha=0.7, edgecolor='none', boxstyle='round,pad=0.3'))

    # Show the image with bounding boxes
    plt.show()


@run_only_on_non_mapping_mode()
def plot_image(leap_data: LeapImage, title: str) -> None:
    """
    Display the image contained in the LeapImage object.

    Returns:
        None

    Example:
        image_data = np.random.rand(100, 100, 3).astype(np.float32)
        leap_image = LeapImage(data=image_data)
        title = "Image"
        visualize(leap_image, title)
    """
    image_data = leap_data.data

    # If the image has one channel, convert it to a 3-channel image for display
    if image_data.shape[2] == 1:
        image_data = np.repeat(image_data, 3, axis=2)

    fig, ax = plt.subplots()
    fig.patch.set_facecolor('black')
    ax.set_facecolor('black')

    ax.imshow(image_data)

    plt.axis('off')
    plt.title(title, color='white')
    plt.show()


@run_only_on_non_mapping_mode()
def plot_graph(leap_data: LeapGraph, title: str) -> None:
    """
        Display the line chart contained in the LeapGraph object.

        Returns:
            None

        Example:
            graph_data = np.random.rand(100, 3).astype(np.float32)
            leap_graph = LeapGraph(data=graph_data)
            title = "Graph"
            visualize(leap_graph, title)
        """
    graph_data = leap_data.data
    num_variables = graph_data.shape[1]

    fig, ax = plt.subplots(figsize=(10, 6))

    # Set the background color to black
    fig.patch.set_facecolor('black')
    ax.set_facecolor('black')

    for i in range(num_variables):
        plt.plot(graph_data[:, i], label=f'Variable {i + 1}')

    ax.set_xlabel('Data Points', color='white')
    ax.set_ylabel('Values', color='white')
    ax.set_title(title, color='white')
    ax.legend()
    ax.grid(True, color='white')

    # Change the color of the tick labels to white
    ax.tick_params(colors='white')

    plt.show()


@run_only_on_non_mapping_mode()
def plot_text_with_heatmap(leap_data: LeapText, title: str) -> None:
    """
    Display the text contained in the LeapText object with a heatmap overlay.

    Args:
        leap_data (LeapData): The LeapText object containing text tokens and an optional heatmap.
        title (str): The title of the visualization.

    Returns:
        None

    Example:
        text_data = ['I', 'ate', 'a', 'banana', '', '', '']
        heatmap = [0.1, 0.3, 0.2, 0.9, 0.0, 0.0, 0.0]
        leap_text = LeapText(data=text_data, heatmap=heatmap)  # Create LeapText object
        title = "Text with Heatmap"
        visualize(leap_text, title)
    """
    text_data = leap_data.data
    heatmap = leap_data.heatmap

    text_data = [s for s in text_data if s != "[PAD]"]

    fig, ax = plt.subplots(figsize=(12, 5))
    fig.patch.set_facecolor('black')
    ax.set_facecolor('black')
    ax.axis('off')  # Hide axes

    font_size = 20

    if heatmap is not None:
        heatmap = heatmap[:len(text_data)]
        if len(heatmap) != len(text_data):
            raise ValueError(
                f"Heatmap length ({len(heatmap)}) must match the number of tokens in `data` ({len(text_data)}).")

        max_tokens_per_row = 10
        num_rows = math.ceil(len(text_data) / max_tokens_per_row)

        fig.set_size_inches(12, num_rows * 1.2)
        for idx, (token, value) in enumerate(zip(text_data, heatmap)):
            if token:
                row = idx // max_tokens_per_row
                col = idx % max_tokens_per_row

                x_pos = col / max_tokens_per_row + 0.03
                y_pos = 1 - (row + 0.5) / num_rows
                color = plt.cm.jet(value)
                ax.text(
                    x_pos,
                    y_pos,
                    token,
                    fontsize=font_size,
                    color=color,
                    ha="left",
                    va="center"
                )
    else:
        display_text = ' '.join([token for token in text_data if token])
        wrapped_text = "\n".join(wrap(display_text, width=80))
        font_color = 'white'
        ax.text(0.5, 0.5, wrapped_text, color=font_color, fontsize=font_size, ha='center', va='center')

    ax.set_title(title, color='white', fontsize=16)

    plt.tight_layout()
    plt.show()

@run_only_on_non_mapping_mode()
def plot_hbar(leap_data: LeapHorizontalBar, title: str) -> None:
    """
        Display the horizontal bar chart contained in the LeapHorizontalBar object.

        Returns:
            None

        Example:
            body_data = np.random.rand(5).astype(np.float32)
            gt_data = np.random.rand(5).astype(np.float32)
            labels = ['Class A', 'Class B', 'Class C', 'Class D', 'Class E']
            leap_horizontal_bar = LeapHorizontalBar(body=body_data, gt=gt_data, labels=labels)
            title = "Horizontal Bar"
            visualize(leap_horizontal_bar, title)
    """
    body_data = leap_data.body
    labels = leap_data.labels

    # Check if 'gt' attribute exists and is not None
    gt_data = getattr(leap_data, 'gt', None)

    fig, ax = plt.subplots()

    fig.patch.set_facecolor('black')
    ax.set_facecolor('black')

    # Adjust positions for side-by-side bars
    y_positions = range(len(labels))
    bar_width = 0.4

    # Plot horizontal bar chart
    if gt_data is not None:
        ax.barh([y - bar_width / 2 for y in y_positions], body_data, color='green', height=bar_width, label='Prediction')
        ax.barh([y + bar_width / 2 for y in y_positions], gt_data, color='orange', height=bar_width, label='GT')
    else:
        ax.barh(y_positions, body_data, color='green', label='Body Data')

    # Set the y-ticks to align with the center of the bars
    ax.set_yticks(y_positions)
    ax.set_yticklabels(labels, color='white')

    # Set the color of the labels and title to white
    ax.set_xlabel('Scores', color='white')
    ax.set_title(title, color='white')

    # Set the color of the ticks to white
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')

    # Add legend if gt is present
    if gt_data is not None:
        ax.legend(loc='best', facecolor='black', edgecolor='white', labelcolor='white')

    plt.show()

@run_only_on_non_mapping_mode()
def plot_image_mask(leap_data: LeapImageMask, title: str) -> None:
    """
        Plots an image with overlaid masks given a LeapImageMask visualizer object.

        Returns:
            None


        Example:
            image_data = np.random.rand(100, 100, 3).astype(np.float32)
            mask_data = np.random.randint(0, 2, (100, 100)).astype(np.uint8)
            labels = ["background", "object"]
            leap_image_mask = LeapImageMask(image=image_data, mask=mask_data, labels=labels)
            title = "Image Mask"
            visualize(leap_image_mask, title)
        """

    image = leap_data.image
    mask = leap_data.mask
    labels = leap_data.labels

    # Create a color map for each label
    colors = plt.cm.jet(np.linspace(0, 1, len(labels)))
    if image.dtype == np.uint8:
        colors = colors * 255

    # Make a copy of the image to draw on
    overlayed_image = image.copy()

    # Iterate through the unique values in the mask (excluding 0)
    for i, label in enumerate(labels):
        # Extract binary mask for the current instance
        instance_mask = (mask == (i + 1))

        # fill the instance mask with a translucent color
        overlayed_image[instance_mask] = (
                overlayed_image[instance_mask] * (1 - 0.5) + np.array(colors[i][:image.shape[-1]], dtype=np.uint8) * 0.5)

    # Display the result using matplotlib
    fig, ax = plt.subplots(1)
    fig.patch.set_facecolor('black')  # Set the figure background to black
    ax.set_facecolor('black')  # Set the axis background to black

    ax.imshow(overlayed_image)
    ax.set_title(title, color='white')
    plt.axis('off')  # Hide the axis
    plt.show()

@run_only_on_non_mapping_mode()
def plot_text_mask(leap_data: LeapTextMask, title: str) -> None:
    """
        Plots text with overlaid masks given a LeapTextMask visualizer object.

        Returns:
            None

        Example:
            text_data = ['I', 'ate', 'a', 'banana', '', '', '']
            mask_data = np.array([0, 0, 0, 1, 0, 0, 0]).astype(np.uint8)
            labels = ["object"]
            leap_text_mask = LeapTextMask(text=text_data, mask=mask_data, labels=labels)
            title = "Text Mask"
            visualize(leap_text_mask, title)
        """

    text_data = leap_data.text
    mask_data = leap_data.mask
    labels = leap_data.labels

    # Create a color map for each label
    colors = plt.cm.jet(np.linspace(0, 1, len(labels)))

    # Create a figure and axis
    fig, ax = plt.subplots()

    # Set background to black
    fig.patch.set_facecolor('black')
    ax.set_facecolor('black')
    ax.set_title(title, color='white')
    ax.axis('off')

    # Set initial position
    x_pos, y_pos = 0.01, 0.5  # Adjusted initial position for better visibility

    # Display the text with colors
    for token, mask_value in zip(text_data, mask_data):
        if mask_value > 0:
            color = colors[mask_value % len(colors)]
            bbox = dict(facecolor=color, edgecolor='none',
                        boxstyle='round,pad=0.3')  # Background color for masked tokens
        else:
            bbox = None

        ax.text(x_pos, y_pos, token, fontsize=12, color='white', ha='left', va='center', bbox=bbox)

        # Update the x position for the next token
        x_pos += len(token) * 0.03 + 0.02  # Adjust the spacing between tokens

    plt.show()

@run_only_on_non_mapping_mode()
def plot_image_with_heatmap(leap_data: LeapImageWithHeatmap, title: str) -> None:
    """
        Display the image with overlaid heatmaps contained in the LeapImageWithHeatmap object.

        Returns:
            None

        Example:
            image_data = np.random.rand(100, 100, 3).astype(np.float32)
            heatmaps = np.random.rand(3, 100, 100).astype(np.float32)
            labels = ["heatmap1", "heatmap2", "heatmap3"]
            leap_image_with_heatmap = LeapImageWithHeatmap(image=image_data, heatmaps=heatmaps, labels=labels)
            title = "Image With Heatmap"
            visualize(leap_image_with_heatmap, title)
        """
    image = leap_data.image
    heatmaps = leap_data.heatmaps
    labels = leap_data.labels

    # Plot the base image
    fig, ax = plt.subplots()
    fig.patch.set_facecolor('black')  # Set the figure background to black
    ax.set_facecolor('black')  # Set the axis background to black
    ax.imshow(image, cmap='gray')

    # Overlay each heatmap with some transparency
    for i in range(len(labels)):
        heatmap = heatmaps[i]
        ax.imshow(heatmap, cmap='jet', alpha=0.5)  # Adjust alpha for transparency
        ax.set_title(f'Heatmap: {labels[i]}', color='white')

        # Display a colorbar for the heatmap
        cbar = plt.colorbar(ax.imshow(heatmap, cmap='jet', alpha=0.5))
        cbar.set_label(labels[i], color='white')
        cbar.ax.yaxis.set_tick_params(color='white')  # Set color for the colorbar ticks
        plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color='white')  # Set color for the colorbar labels

    plt.axis('off')
    plt.title(title, color='white')
    plt.show()



plot_switch = {
    LeapDataType.Image: plot_image,
    LeapDataType.Text: plot_text_with_heatmap,
    LeapDataType.Graph: plot_graph,
    LeapDataType.HorizontalBar: plot_hbar,
    LeapDataType.ImageMask: plot_image_mask,
    LeapDataType.TextMask: plot_text_mask,
    LeapDataType.ImageWithHeatmap: plot_image_with_heatmap,
    LeapDataType.ImageWithBBox: plot_image_with_b_box,
}
