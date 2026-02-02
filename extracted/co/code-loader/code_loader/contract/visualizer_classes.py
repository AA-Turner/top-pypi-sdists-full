from typing import List, Any, Tuple, Union, Optional

import numpy as np
import numpy.typing as npt
from dataclasses import dataclass

from code_loader.contract.enums import LeapDataType
from code_loader.contract.responsedataclasses import BoundingBox


class LeapValidationError(Exception):
    pass


def validate_type(actual: Any, expected: Any, prefix_message: str = '') -> None:
    if not isinstance(expected, list):
        expected = [expected]
    if actual not in expected:
        if len(expected) == 1:
            raise LeapValidationError(
                f'{prefix_message}.\n'
                f'visualizer returned unexpected type. got {actual}, instead of {expected[0]}')
        else:
            raise LeapValidationError(
                f'{prefix_message}.\n'
                f'visualizer returned unexpected type. got {actual}, allowed is one of {expected}')


@dataclass
class LeapImage:
    """
    Visualizer representing an image for Tensorleap.

    Attributes:
    data (npt.NDArray[np.float32] | npt.NDArray[np.uint8]): The image data.
    type (LeapDataType): The data type, default is LeapDataType.Image.
    compress: Optional[bool]: Whether to compress the image (.jpg) or not (.png)

    Example:
        image_data = np.random.rand(100, 100, 3).astype(np.float32)
        leap_image = LeapImage(data=image_data)
    """
    data: Union[npt.NDArray[np.float32], npt.NDArray[np.uint8]]
    type: LeapDataType = LeapDataType.Image
    compress: Optional[bool] = True

    def __post_init__(self) -> None:
        validate_type(self.type, LeapDataType.Image)
        validate_type(type(self.data), np.ndarray)
        validate_type(self.data.dtype, [np.uint8, np.float32])
        validate_type(len(self.data.shape), 3, 'Image must be of shape 3')
        validate_type(self.data.shape[2], [1, 3], 'Image channel must be either 3(rgb) or 1(gray)')
        validate_type(type(self.compress), bool, 'compress flag must be a boolean')


@dataclass
class LeapVideo:
    """
    Visualizer representing a video for Tensorleap.

    Attributes:
    data (npt.NDArray[np.float32] | npt.NDArray[np.uint8]): The video data, shaped [T, H, W, C], where T is the number of frames.
    type (LeapDataType): The data type, default is LeapDataType.Video.

    Example:
        video_data = np.random.rand(10, 100, 100, 3).astype(np.float32)
        leap_video = LeapVideo(data=video_data)
    """
    data: Union[npt.NDArray[np.float32], npt.NDArray[np.uint8]]
    type: LeapDataType = LeapDataType.Video

    def __post_init__(self) -> None:
        validate_type(self.type, LeapDataType.Video)
        validate_type(type(self.data), np.ndarray)
        validate_type(self.data.dtype, [np.uint8, np.float32])
        validate_type(len(self.data.shape), 4, 'Video must be of shape 4')
        validate_type(self.data.shape[3], [1, 3], 'Video channel must be either 3(rgb) or 1(gray)')


@dataclass
class LeapImageWithBBox:
    """
    Visualizer representing an image with bounding boxes for Tensorleap, used for object detection tasks.

    Attributes:
    data (npt.NDArray[np.float32] | npt.NDArray[np.uint8]): The image data, shaped [H, W, 3] or [H, W, 1].
    bounding_boxes (List[BoundingBox]): List of Tensorleap bounding boxes objects in relative size to image size.
    type (LeapDataType): The data type, default is LeapDataType.ImageWithBBox.

    Example:
        image_data = np.random.rand(100, 100, 3).astype(np.float32)
        bbox = BoundingBox(x=0.5, y=0.5, width=0.2, height=0.2, confidence=0.9, label="object")
        leap_image_with_bbox = LeapImageWithBBox(data=image_data, bounding_boxes=[bbox])
    """
    data: Union[npt.NDArray[np.float32], npt.NDArray[np.uint8]]
    bounding_boxes: List[BoundingBox]
    type: LeapDataType = LeapDataType.ImageWithBBox

    def __post_init__(self) -> None:
        validate_type(self.type, LeapDataType.ImageWithBBox)
        validate_type(type(self.data), np.ndarray)
        validate_type(self.data.dtype, [np.uint8, np.float32])
        validate_type(len(self.data.shape), 3, 'Image must be of shape 3')
        validate_type(self.data.shape[2], [1, 3], 'Image channel must be either 3(rgb) or 1(gray)')


@dataclass
class LeapGraph:
    """
    Visualizer representing a line chart data for Tensorleap.

    Attributes:
    data (npt.NDArray[np.float32]): The array data, shaped [M, N] where M is the number of data points and N is the number of variables.
    type (LeapDataType): The data type, default is LeapDataType.Graph.
    x_label (Optional[str]): The x-axis label.
    y_label (Optional[str]): The y-axis label.
    x_range (Optional[Tuple[float, float]]): The range of x-axis. mapping the index to the range.

    Example:
        graph_data = np.random.rand(100, 3).astype(np.float32)
        x_label = 'Frequency [Seconds]'
        y_label = 'Amplitude [Voltage]'
        x_range = (0.1, 3.0)
        legend = ['experiment1', 'experiment2', 'experiment3']
        leap_graph = LeapGraph(data=graph_data, x_label=x_label, y_label=y_label, x_range=x_range, legend=legend)
    """
    data: npt.NDArray[np.float32]
    type: LeapDataType = LeapDataType.Graph
    x_label: Optional[str] = None
    y_label: Optional[str] = None
    x_range: Optional[Tuple[float,float]] = None
    legend: Optional[List[str]] = None

    def __post_init__(self) -> None:
        validate_type(self.type, LeapDataType.Graph)
        validate_type(type(self.data), np.ndarray)
        validate_type(self.data.dtype, np.float32)
        validate_type(len(self.data.shape), 2, f'Graph must be of shape 2')
        if self.legend:
            validate_type(self.data.shape[1], len(self.legend), 'Number of labels supplied should equal the number of graphs')
        validate_type(type(self.x_label), [str, type(None)], 'x_label must be a string or None')
        validate_type(type(self.y_label), [str, type(None)], 'y_label must be a string or None')
        validate_type(type(self.x_range), [tuple, type(None)], 'x_range must be a tuple or None')
        if self.x_range is not None:
            if len(self.x_range) != 2:
                raise LeapValidationError('x_range must be a tuple of length 2')
            validate_type(type(self.x_range[0]), [float, int] , 'x_range must be a tuple of floats or integers')
            validate_type(type(self.x_range[1]), [float, int], 'x_range must be a tuple of floats or integers')


@dataclass
class LeapText:
    """
    Visualizer representing text data for Tensorleap.

    Attributes:
    data (List[str]): The text data, consisting of a list of text tokens. If the model requires fixed-length inputs,
    it is recommended to maintain the fixed length, using empty strings ('') instead of padding tokens ('PAD') e.g., ['I', 'ate', 'a', 'banana', '', '', '', ...]
    type (LeapDataType): The data type, default is LeapDataType.Text.

    Example:
        text_data = ['I', 'ate', 'a', 'banana', '', '', '']
        heatmap = [0.1, 0.3, 0.2, 0.9, 0.0, 0.0, 0.0]
        leap_text = LeapText(data=text_data heatmap=heatmap)  # Create LeapText object
    """
    data: List[str]
    type: LeapDataType = LeapDataType.Text
    heatmap: Optional[List[float]] = None

    def __post_init__(self) -> None:
        validate_type(self.type, LeapDataType.Text)
        validate_type(type(self.data), list)
        for value in self.data:
            validate_type(type(value), str)

        if self.heatmap is not None:
            validate_type(type(self.heatmap), list)
            for v in self.heatmap:
                validate_type(type(v), float)
            if len(self.heatmap) != len(self.data):
                raise LeapValidationError(
                    f"Heatmap length ({len(self.heatmap)}) must match the number of tokens in `data` ({len(self.data)})."
                )


@dataclass
class LeapHorizontalBar:
    """
    Visualizer representing horizontal bar data for Tensorleap.
    For example, this can be used to visualize the model's prediction scores in a classification problem.

    Attributes:
    body (npt.NDArray[np.float32]): The data for the bar, shaped [C], where C is the number of data points.
    labels (List[str]): Labels for the horizontal bar; e.g., when visualizing the model's classification output, labels are the class names.
    Length of `body` should match the length of `labels`, C.
    type (LeapDataType): The data type, default is LeapDataType.HorizontalBar.

    Example:
        body_data = np.random.rand(5).astype(np.float32)
        labels = ['Class A', 'Class B', 'Class C', 'Class D', 'Class E']
        gt_data = np.array([0.1, 0.2, 0.3, 0.4, 0.5]).astype(np.float32)
        leap_horizontal_bar = LeapHorizontalBar(body=body_data, labels=labels, gt=gt_data)
    """
    body: npt.NDArray[np.float32]
    labels: List[str]
    gt: Optional[npt.NDArray[np.float32]] = None
    type: LeapDataType = LeapDataType.HorizontalBar


    def __post_init__(self) -> None:
        validate_type(self.type, LeapDataType.HorizontalBar)
        validate_type(type(self.body), np.ndarray)
        validate_type(self.body.dtype, np.float32)
        validate_type(len(self.body.shape), 1, 'HorizontalBar body must be of shape 1')
        validate_type(type(self.gt), [np.ndarray, type(None)],
                      'Provided HorizontalBar GT data should be a numpy array')
        if self.gt is not None:
            validate_type(len(self.gt.shape), 1, 'HorizontalBar GT must be of shape 1')

        validate_type(type(self.labels), list)
        for label in self.labels:
            validate_type(type(label), str)


@dataclass
class LeapImageMask:
    """
    Visualizer representing an image with a mask for Tensorleap.
    This can be used for tasks such as segmentation, and other applications where it is important to highlight specific regions within an image.

    Attributes:
    mask (npt.NDArray[np.uint8]): The mask data, shaped [H, W].
    image (npt.NDArray[np.float32] | npt.NDArray[np.uint8]): The image data, shaped [H, W, 3] or shaped [H, W, 1].
    labels (List[str]): Labels associated with the mask regions; e.g., class names for segmented objects. The length of `labels` should match the number of unique values in `mask`.
    type (LeapDataType): The data type, default is LeapDataType.ImageMask.

    Example:
        image_data = np.random.rand(100, 100, 3).astype(np.float32)
        mask_data = np.random.randint(0, 2, (100, 100)).astype(np.uint8)
        labels = ["background", "object"]
        leap_image_mask = LeapImageMask(image=image_data, mask=mask_data, labels=labels)
    """
    mask: npt.NDArray[np.uint8]
    image: Union[npt.NDArray[np.float32], npt.NDArray[np.uint8]]
    labels: List[str]
    type: LeapDataType = LeapDataType.ImageMask

    def __post_init__(self) -> None:
        validate_type(self.type, LeapDataType.ImageMask)
        validate_type(type(self.mask), np.ndarray)
        validate_type(self.mask.dtype, np.uint8)
        validate_type(len(self.mask.shape), 2, 'image mask must be of shape 2')
        validate_type(type(self.image), np.ndarray)
        validate_type(self.image.dtype, [np.uint8, np.float32])
        validate_type(len(self.image.shape), 3, 'Image must be of shape 3')
        validate_type(self.image.shape[2], [1, 3], 'Image channel must be either 3(rgb) or 1(gray)')
        validate_type(type(self.labels), list)
        for label in self.labels:
            validate_type(type(label), str)


@dataclass
class LeapTextMask:
    """
    Visualizer representing text data with a mask for Tensorleap.
    This can be used for tasks such as named entity recognition (NER), sentiment analysis, and other applications where it is important to highlight specific tokens or parts of the text.

    Attributes:
    mask (npt.NDArray[np.uint8]): The mask data, shaped [L].
    text (List[str]): The text data, consisting of a list of text tokens, length of L.
    labels (List[str]): Labels associated with the masked tokens; e.g., named entities or sentiment categories. The length of `labels` should match the number of unique values in `mask`.
    type (LeapDataType): The data type, default is LeapDataType.TextMask.

    Example:
        text_data = ['I', 'ate', 'a', 'banana', '', '', '']
        mask_data = np.array([0, 0, 0, 1, 0, 0, 0]).astype(np.uint8)
        labels = ["object"]
        leap_text_mask = LeapTextMask(text=text_data, mask=mask_data, labels=labels)
        leap_text_mask.plot_visualizer()
    """
    mask: npt.NDArray[np.uint8]
    text: List[str]
    labels: List[str]
    type: LeapDataType = LeapDataType.TextMask

    def __post_init__(self) -> None:
        validate_type(self.type, LeapDataType.TextMask)
        validate_type(type(self.mask), np.ndarray)
        validate_type(self.mask.dtype, np.uint8)
        validate_type(len(self.mask.shape), 1, 'text mask must be of shape 1')
        validate_type(type(self.text), list)
        for t in self.text:
            validate_type(type(t), str)
        validate_type(type(self.labels), list)
        for label in self.labels:
            validate_type(type(label), str)


@dataclass
class LeapImageWithHeatmap:
    """
    Visualizer representing an image with heatmaps for Tensorleap.
    This can be used for tasks such as highlighting important regions in an image, visualizing attention maps, and other applications where it is important to overlay heatmaps on images.

    Attributes:
    image (npt.NDArray[np.float32]): The image data, shaped [H, W, C], where C is the number of channels.
    heatmaps (npt.NDArray[np.float32]): The heatmap data, shaped [N, H, W], where N is the number of heatmaps.
    labels (List[str]): Labels associated with the heatmaps; e.g., feature names or attention regions. The length of `labels` should match the number of heatmaps, N.
    type (LeapDataType): The data type, default is LeapDataType.ImageWithHeatmap.

    Example:
        image_data = np.random.rand(100, 100, 3).astype(np.float32)
        heatmaps = np.random.rand(3, 100, 100).astype(np.float32)
        labels = ["heatmap1", "heatmap2", "heatmap3"]
        leap_image_with_heatmap = LeapImageWithHeatmap(image=image_data, heatmaps=heatmaps, labels=labels)
    """
    image: npt.NDArray[np.float32]
    heatmaps: npt.NDArray[np.float32]
    labels: List[str]
    type: LeapDataType = LeapDataType.ImageWithHeatmap

    def __post_init__(self) -> None:
        validate_type(self.type, LeapDataType.ImageWithHeatmap)
        validate_type(type(self.heatmaps), np.ndarray)
        validate_type(self.heatmaps.dtype, np.float32)
        validate_type(type(self.image), np.ndarray)
        validate_type(self.image.dtype, np.float32)
        validate_type(type(self.labels), list)
        for label in self.labels:
            validate_type(type(label), str)
        if self.heatmaps.shape[0] != len(self.labels):
            raise LeapValidationError(
                'Number of heatmaps and labels must be equal')


map_leap_data_type_to_visualizer_class = {
    LeapDataType.Image.value: LeapImage,
    LeapDataType.Graph.value: LeapGraph,
    LeapDataType.Video.value: LeapVideo,
    LeapDataType.Text.value: LeapText,
    LeapDataType.HorizontalBar.value: LeapHorizontalBar,
    LeapDataType.ImageMask.value: LeapImageMask,
    LeapDataType.TextMask.value: LeapTextMask,
    LeapDataType.ImageWithBBox.value: LeapImageWithBBox,
    LeapDataType.ImageWithHeatmap.value: LeapImageWithHeatmap
}
