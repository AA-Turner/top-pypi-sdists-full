import cv2


def get_video_duration(video_path):
    cap = cv2.VideoCapture(video_path)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_rate = int(cap.get(cv2.CAP_PROP_FPS))
    duration = frame_count / frame_rate
    return duration


video_path = "example.mp3"
duration = get_video_duration(video_path)
print("视频时长：{}秒".format(duration))