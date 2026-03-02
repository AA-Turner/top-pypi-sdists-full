import os
import sys
import cv2
import json
import importlib
import argparse
from ultralytics import YOLO
from src.matrice_analytics.post_processing.core.base import ProcessingContext


class UseCaseTestProcessor:
    """
    A flexible YOLO-based video processor for testing different post-processing use cases.
    """

    def __init__(self, file_name, config_name, usecase_name, model_path, video_path, post_process=None, max_frames=None):
        self.file_name = file_name
        self.config_name = config_name
        self.usecase_name = usecase_name
        self.model_path = model_path
        self.video_path = video_path
        self.post_process = post_process
        self.max_frames = max_frames
        self.json_dir = "jsons"

        self._setup_environment()
        self.ConfigClass, self.UsecaseClass = self._load_usecase()
        self.config = self._initialize_config()
        self.processor = self.UsecaseClass()
        self.model = YOLO(self.model_path)
        os.makedirs(self.json_dir, exist_ok=True)

    def _setup_environment(self):
        """Ensure project root is added to sys.path."""
        project_root = os.path.abspath("/content/py_analytics")
        if project_root not in sys.path:
            sys.path.append(project_root)

    def _load_usecase(self):
        """Dynamically import config and usecase classes."""
        module_path = f"src.matrice_analytics.post_processing.usecases.{self.file_name}"
        module = importlib.import_module(module_path)
        return getattr(module, self.config_name), getattr(module, self.usecase_name)

    def _initialize_config(self):
        """Initialize config object, applying overrides if provided."""
        if self.post_process:
            return self.ConfigClass(**self.post_process)
        return self.ConfigClass()

    def _serialize_result(self, result):
        """Convert result object into JSON-serializable dict."""
        def to_serializable(obj):
            if hasattr(obj, "to_dict"):
                return obj.to_dict()
            if hasattr(obj, "__dict__"):
                return obj.__dict__
            return str(obj)
        return json.loads(json.dumps(result, default=to_serializable))


    def process_video(self):
        """Run YOLO inference on video and post-process frame by frame."""
        cap = cv2.VideoCapture(self.video_path)
        if not cap.isOpened():
            raise ValueError(f"Failed to open video at {self.video_path}")

        frame_idx = 0
        stream_info = {
            'input_settings': {
                'start_frame': 0,
                'original_fps': cap.get(cv2.CAP_PROP_FPS),
                'camera_info': {'id': 'cam1', 'name': 'Test Camera'}
            }
        }

        print(f"\nStarting video processing: {self.video_path}")
        print(f"Model: {self.model_path}")
        print(f"Output directory: {self.json_dir}\n")

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.model(frame_rgb)

            detections = []
            for xyxy, conf, cls in zip(results[0].boxes.xyxy, results[0].boxes.conf, results[0].boxes.cls):
                x1, y1, x2, y2 = xyxy.tolist()
                detections.append({
                    'category_id': int(cls),
                    'confidence': conf.item(),
                    'bounding_box': {
                        'xmin': int(x1),
                        'ymin': int(y1),
                        'xmax': int(x2),
                        'ymax': int(y2)
                    }
                })

            success, encoded_image = cv2.imencode(".jpg", frame)
            input_bytes = encoded_image.tobytes() if success else None

            try:
                result = self.processor.process(
                    detections, self.config, input_bytes, ProcessingContext(), stream_info
                )
            except TypeError:
                result = self.processor.process(
                    detections, self.config, ProcessingContext(), stream_info
                )

            json_path = os.path.join(self.json_dir, f"frame_{frame_idx:04d}.json")
            with open(json_path, "w") as f:
                json.dump(self._serialize_result(result), f, indent=2)

            print(f"Frame {frame_idx} processed — detections: {len(detections)} — saved: {json_path}")

            frame_idx += 1
            stream_info['input_settings']['start_frame'] += 1

            if self.max_frames and frame_idx >= self.max_frames:
                print(f"\nMax frame limit ({self.max_frames}) reached.")
                break

        cap.release()
        print(f"\nProcessing complete. JSON outputs saved in: {self.json_dir}")


def main():
    parser = argparse.ArgumentParser(description="YOLO Use Case Test Processor")

    parser.add_argument("--file_name", type=str, required=True,
                        help="Usecase file name under src/matrice_analytics/post_processing/usecases/")
    parser.add_argument("--config_name", type=str, required=True,
                        help="Config class name (e.g., PeopleCountingConfig)")
    parser.add_argument("--usecase_name", type=str, required=True,
                        help="Use case class name (e.g., PeopleCountingUseCase)")
    parser.add_argument("--model_path", type=str, required=True,
                        help="Path to YOLO model file (.pt)")
    parser.add_argument("--video_path", type=str, required=True,
                        help="Path to input video")
    parser.add_argument("--post_process", type=json.loads, default=None,
                        help="JSON string for config overrides, e.g. '{\"min_confidence\": 0.5}'")
    parser.add_argument("--max_frames", type=int, default=None,
                        help="Limit number of frames processed")

    args = parser.parse_args()

    processor = UseCaseTestProcessor(
        file_name=args.file_name,
        config_name=args.config_name,
        usecase_name=args.usecase_name,
        model_path=args.model_path,
        video_path=args.video_path,
        post_process=args.post_process,
        max_frames=args.max_frames
    )
    processor.process_video()


if __name__ == "__main__":
    main()
