import numpy as np
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, field
import cv2
import requests
from scipy.special import softmax
try:
    from transformers import CLIPProcessor
    from PIL import Image
    import onnxruntime as ort
except:
    print("Unable to import onnxruntime/transformers/scipy/PIL")

def load_model_from_checkpoint(checkpoint_path,local_path):
    """
    Load a model from checkpoint URL
    """
    try:
        print(f"Loading model from checkpoint: {checkpoint_path}")
        
        # Check if checkpoint is a URL
        if checkpoint_path.startswith(('http://', 'https://')):
            # Download checkpoint from URL
            response = requests.get(checkpoint_path, timeout = (30,200))
            if response.status_code == 200:
                with open(local_path, 'wb') as f:
                    f.write(response.content)
                checkpoint_path = local_path
                print(f"Downloaded checkpoint to {local_path}")
            else:
                print(f"Failed to download checkpoint from {checkpoint_path}")
                return None
        
        # Load the model from the checkpoint
        model = ort.InferenceSession(checkpoint_path, providers=["CUDAExecutionProvider"])
        print(f"{local_path} Model loaded successfully from checkpoint")
        return model
        
    except Exception as e:
        print(f"Error loading model from checkpoint: {e}")
        return None



class ClipProcessor:
    def __init__(self,
                 image_model_path: str = 'https://s3.us-west-2.amazonaws.com/testing.resources/datasets/clip_image.onnx',
                 text_model_path: str = 'https://s3.us-west-2.amazonaws.com/testing.resources/datasets/clip_text.onnx',
                 processor_dir: str = './clip_processor',
                 providers: Optional[List[str]] = None):
        #test
        self.color_category: List[str] = ["black", "white", "yellow", "gray", "red", "blue", "light blue",
        "green", "brown"]

        self.image_url: str = image_model_path
        self.text_url: str = text_model_path
        self.processor_path: str = processor_dir

        self.image_sess = load_model_from_checkpoint(self.image_url,"clip_image.onnx")
        self.text_sess = load_model_from_checkpoint(self.text_url,"clip_text.onnx")

        self.processor = CLIPProcessor.from_pretrained(self.processor_path)

        tok = self.processor.tokenizer(self.color_category, padding=True, return_tensors="np")
        ort_inputs_text = {
            "input_ids": tok["input_ids"].astype(np.int64),
            "attention_mask": tok["attention_mask"].astype(np.int64)
        }
        text_out = self.text_sess.run(["text_embeds"], ort_inputs_text)[0].astype(np.float32)
        self.text_embeds = text_out / np.linalg.norm(text_out, axis=-1, keepdims=True)

        sample = self.processor(images=np.zeros((224, 224, 3), dtype=np.uint8), return_tensors="np")
        self.pixel_template = sample["pixel_values"].astype(np.float32)
        self.min_box_size = 32
        self.max_batch = 32
        self.frame_skip = 2
        self.batch_pixels = np.zeros((self.max_batch, *self.pixel_template.shape[1:]), dtype=np.float32)

        self.records: Dict[int, Dict[str, float]] = {}
        self.frame_idx = 0
        self.processed_frames = 0


    def process_color_in_frame(self, detections, input_bytes, zones: Optional[Dict[str, List[List[float]]]], stream_info):
        boxes = []
        tracked_ids: List[int] = []
        frame_number: Optional[int] = None
        # print(detections)
        self.frame_idx+=1
        nparr = np.frombuffer(input_bytes, np.uint8)        # convert bytes to numpy array
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)      # decode image

            # Step 2: Convert PIL → NumPy array
        frame = np.array(image)
        if stream_info:
            input_settings = stream_info.get("input_settings", {})
            start_frame = input_settings.get("start_frame")
            end_frame = input_settings.get("end_frame")
            if start_frame is not None and end_frame is not None and start_frame == end_frame:
                frame_number = start_frame

        for det in detections:
            bbox = det.get('bounding_box')
            tid = det.get('track_id')
            zones = zones if zones else {}
            for z_name, zone_polygon in zones.items():
                if self._is_in_zone(bbox, zone_polygon):
                    w = bbox['xmax'] - bbox['xmin']
                    h =  bbox['ymax'] - bbox['ymin']
                    if w >= self.min_box_size and h >= self.max_batch:
                        boxes.append(bbox)
                        tracked_ids.append(tid)
        # print(boxes)
        # print(tracked_ids)
        if not boxes:
          print(f"Frame {self.frame_idx}: No cars in zone")
          self.processed_frames += 1
          # print(f"Frame {frame_idx} processedms\n")
          return

        # print(boxes)
        # print(tracked_ids)
        crops_for_model = []
        map_trackidx_to_cropidx = []
        for i,(bbox, tid) in enumerate(zip(boxes, tracked_ids)):
            last_rec = self.records.get(tid)
            should_classify = False
            if last_rec is None:
                should_classify = True
            else:
                if (self.frame_idx - last_rec.get("last_classified_frame", -999)) >= self.frame_skip:
                    should_classify = True
            if should_classify:
                x1, y1, x2, y2 = bbox['xmin'], bbox['ymin'], bbox['xmax'], bbox['ymax']
                # crop safely
                y1c, y2c = max(0, y1), min(frame.shape[0], y2)
                x1c, x2c = max(0, x1), min(frame.shape[1], x2)
                if y2c - y1c <= 0 or x2c - x1c <= 0:
                    continue
                crop = cv2.cvtColor(frame[y1c:y2c, x1c:x2c], cv2.COLOR_BGR2RGB)
                pil_img = Image.fromarray(crop).resize((224, 224))
                map_trackidx_to_cropidx.append((tid, len(crops_for_model)))
                crops_for_model.append(pil_img)
        # print(crops_for_model)
        # print(map_trackidx_to_cropidx)

        if crops_for_model:
            record = {}
            img_embeds = self.run_image_onnx_on_crops(crops_for_model)  # [N, D]
            # compute similarity with text_embeds (shape [num_labels, D])
            sims = img_embeds @ self.text_embeds.T  # [N, num_labels]
            # convert to probs
            probs = np.exp(sims) / np.exp(sims).sum(axis=-1, keepdims=True)  # softmax numerically simple
            # print(probs)

            # assign back to corresponding tracks
            for (tid, crop_idx) in map_trackidx_to_cropidx:
                prob = probs[crop_idx]
                # print(prob)
                best_idx = int(np.argmax(prob))
                best_label = self.color_category[best_idx]
                # print(best_label)
                best_score = float(prob[best_idx])
                # print(best_score)

                rec = self.records.get(tid)
                # if rec is None:
                record[tid] = {
                    "frame": self.frame_idx,
                    "color": best_label,
                    "confidence": best_score,
                    "track_id": tid,
                    "last_classified_frame": self.frame_idx,
                }
                # else:
                #     # update only if confidence improves
                #     if best_score > rec["confidence"]:
                #         rec["color"] = best_label
                #         rec["confidence"] = best_score
                #         rec["frame"] = self.frame_idx
                #     rec["last_classified_frame"] = self.frame_idx


        return record


    def run_image_onnx_on_crops(self, crops):
        valid_crops = []
        for i, crop in enumerate(crops):
            if isinstance(crop, Image.Image):  # PIL.Image
                crop = np.array(crop)
            if not isinstance(crop, np.ndarray):
                print(f"Skipping crop {i}: not a numpy array ({type(crop)})")
                continue
            if crop.size == 0:
                print(f"Skipping crop {i}: empty array")
                continue

            try:
                crop_resized = cv2.resize(crop, (224, 224), interpolation=cv2.INTER_LINEAR)
                valid_crops.append(crop_resized)
            except Exception as e:
                print(f"Skipping crop {i}: resize failed ({e})")

        if not valid_crops:
            print("⚠️ No valid crops to process")
            return np.zeros((0, self.text_embeds.shape[-1]), dtype=np.float32)

        # Convert all valid crops at once
        pixel_values = self.processor(images=valid_crops, return_tensors="np")["pixel_values"]
        n = pixel_values.shape[0]
        self.batch_pixels[:n] = pixel_values

        ort_inputs = {"pixel_values": self.batch_pixels[:n]}
        img_out = self.image_sess.run(["image_embeds"], ort_inputs)[0].astype(np.float32)

        return img_out / np.linalg.norm(img_out, axis=-1, keepdims=True)


    def _is_in_zone(self, bbox, polygon: List[List[float]]) -> bool:
        if not polygon:
            return False
        # print(bbox)
        x1, y1, x2, y2 = bbox['xmin'], bbox['ymin'], bbox['xmax'], bbox['ymax']
        # print(x1,x2,y1,y2)
        # print(type(x1))
        # print(polygon)
        cx, cy = int((x1 + x2) / 2), int((y1 + y2) / 2)
        polygon = np.array(polygon, dtype=np.int32)
        return cv2.pointPolygonTest(polygon, (cx, cy), False) >= 0


