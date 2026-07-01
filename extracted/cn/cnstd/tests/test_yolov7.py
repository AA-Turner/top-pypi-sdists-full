import torch

from cnstd.yolov7.general import box_iou


def test_iou():
    box1 = torch.tensor([0, 0, 10, 10]).unsqueeze(0)
    shift = 8
    box2 = box1 + shift
    # box2 = torch.tensor([5, 5, 15, 15]).unsqueeze(0)
    res = box_iou(box1, box2).squeeze()
    print(float(res))
