import json
from fastapi import APIRouter, HTTPException, File, UploadFile, Request, Query, Form
from fastapi import File, UploadFile
from pydantic import BaseModel
import os
import inspect
import sys
from typing import Any, Dict
import yaml
import aiofiles
from pathlib import Path
from fastapi.responses import JSONResponse
import boto3
##
def load_yaml_file(filepath: str) -> Dict[str, Any]:
    with open(filepath, 'r', encoding='utf-8') as file:
        data = yaml.safe_load(file)
    return data

# 현재 작업 디렉토리 얻기
current_directory = os.getcwd()
# 현재 작업 디렉토리와 'config.yaml'을 합쳐서 절대 경로 생성
config_path = os.path.join(current_directory, 'config.yaml')
config = load_yaml_file(config_path)

class UpdateAPI:
    def __init__(self, settings):
        self.router = APIRouter(prefix="/api/v1")
        self.settings = settings
        self.setup_routes()

    def setup_routes(self):
        @self.router.post("/get_s3_path")
        async def upload_file_and_get_s3_path(file: UploadFile = File(...), unique_id: str = Query(None, description="Unique identifier to append to the URI")):
            try:
                # 파일 업로드 처리
                upload_directory = os.path.join(self.settings.workspace, unique_id)
                os.makedirs(upload_directory, exist_ok=True)

                file_location = os.path.join(upload_directory, file.filename)

                with open(file_location, "wb") as buffer:
                    buffer.write(await file.read())

                # activate_info.json 파일에서 train_artifact_uri 읽기
                info_file_path = os.path.join(self.settings.workspace, "activate_info.json")

                if not os.path.exists(info_file_path):
                    raise HTTPException(status_code=404, detail="File not found: activate_info.json")

                try:
                    with open(info_file_path, "r", encoding="utf-8") as info_file:
                        data = json.load(info_file)

                    train_artifact_uri = data.get("stream_history_info", {}).get("train_artifact_uri")

                    if train_artifact_uri is None:
                        raise HTTPException(status_code=404, detail="train_artifact_uri not found in activate_info.json")

                    if unique_id:
                        train_artifact_uri = os.path.join(train_artifact_uri, unique_id)


                    # Boto3를 사용하여 S3에 파일 업로드
                    try:
                        aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
                        aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
                        if aws_access_key_id and aws_secret_access_key:
                            s3_client = boto3.client(
                                's3',
                                aws_access_key_id=aws_access_key_id,
                                aws_secret_access_key=aws_secret_access_key
                            )
                        else:
                            s3_client = boto3.client('s3')

                        try:
                            s3_client.upload_file(file_location, train_artifact_uri, file.filename)
                        except Exception as e:
                            raise HTTPException(status_code=500, detail=f"Failed to upload file to S3: {str(e)}")

                        return {
                            "file_path": file_location,
                            "train_artifact_uri": train_artifact_uri,
                        }
                    except Exception as e:
                        raise HTTPException(status_code=500, detail=f"Failed to initialize S3 client: {str(e)}")

                    return {
                        "file_path": file_location,
                        "train_artifact_uri": train_artifact_uri
                    }
                except json.JSONDecodeError:
                    raise HTTPException(status_code=500, detail="Error decoding JSON from activate_info.json")
                except Exception as e:
                    raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

            except Exception as e:
                raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

    # def setup_routes(self):

    #     @self.router.post("/uploadfile/")
    #     async def upload_file(file: UploadFile = File(...), id: str = Form(...)):
    #         try:
    #             environment = os.getenv('env_flag')
    #             if not environment:
    #                 print("Local Test 환경")
    #                 try:
    #                     directory = f".workspace/{id}"
    #                     file_location = f"{directory}/{file.filename}"

    #                     # 폴더가 없으면 생성
    #                     if not os.path.exists(directory):
    #                         os.makedirs(directory)

    #                     async with aiofiles.open(file_location, "wb") as out_file:
    #                         content = await file.read()
    #                         await out_file.write(content)

    #                     return {"info": f"file '{file.filename}' saved at '{file_location}'"}
    #                 except Exception as e:
    #                     return {"error": str(e)}

    #             elif environment == 'AWS':
    #                 try: 
    #                     import boto3
    #                     ald_s3_client = boto3.client('s3')
    #                     ald_s3_path = os.getenv('ald_s3_path')
    #                     if not ald_s3_path:
    #                         return JSONResponse(status_code=400, content={"error": "s3_path가 제공되지 않았습니다."})

    #                     if ald_s3_path.startswith("S3://"):
    #                         ald_s3_path = ald_s3_path[len("S3://"):]
    #                     path_parts = ald_s3_path.split("/", 1)

    #                     if len(path_parts) != 2:
    #                         return JSONResponse(status_code=400, content={"error": "s3_path 형식이 올바르지 않습니다. '버킷이름/경로' 형식이어야 합니다."})
                        
    #                     bucket_name, object_key = path_parts
    #                     ald_stream_id = os.getenv('stram_id')
    #                     ald_stream_history = os.getenv('stream_history')
    #                     object_key = f"{object_key}/{ald_stream_id}/{ald_stream_history}/{id}/"
    #                     ald_s3_client.upload_file(file.file, bucket_name, object_key)
    #                     return JSONResponse(status_code=200, content={"message": f"File uploaded to {ald_s3_client} successfully"})
                    
    #                 except Exception as e:
    #                     return JSONResponse(status_code=500, content={"error": str(e)})
                    
    #             elif environment == 'GCP':
    #                 print("GCP TBD")
    #             elif environment == 'LOCAL':
    #                 print("LOCAL TBD")
    #             else:
    #                 print('Not Supported')

    #         except Exception as e:
    #             return {"error": str(e)}

    #     @self.router.post("/downloadfile/")
    #     async def download_file(file: UploadFile = File(...), id: str = Form(...)):
    #         try:
    #             environment = os.getenv('env_flag')
    #             if not environment:
    #                 print("Local Test 환경")
    #                 directory = f".workspace/{id}"
    #                 file_location = f"{directory}/{file.filename}"

    #                 # 폴더가 없으면 생성
    #                 if not os.path.exists(directory):
    #                     os.makedirs(directory)

    #                 if not os.path.exists(file_location):
    #                     raise HTTPException(status_code=404, detail="File not found")
                    
    #                 return file_location

    #             elif environment == 'AWS':
    #                 try: 
    #                     import boto3
    #                     ald_s3_client = boto3.client('s3')

    #                     download_path = f".workspace/{id}"
    #                     # 폴더가 없으면 생성합니다.
    #                     if not os.path.exists(download_path):
    #                         os.makedirs(download_path)

    #                     ald_s3_path = os.getenv('ald_s3_path')
    #                     if not ald_s3_path:
    #                         return JSONResponse(status_code=400, content={"error": "s3_path가 제공되지 않았습니다."})

    #                     if ald_s3_path.startswith("S3://"):
    #                         ald_s3_path = ald_s3_path[len("S3://"):]
    #                     path_parts = ald_s3_path.split("/", 1)

    #                     if len(path_parts) != 2:
    #                         return JSONResponse(status_code=400, content={"error": "s3_path 형식이 올바르지 않습니다. '버킷이름/경로' 형식이어야 합니다."})
                        
    #                     bucket_name, object_key = path_parts
    #                     ald_stream_id = os.getenv('stram_id')
    #                     ald_stream_history = os.getenv('stream_history')

    #                     folder_name = f"{object_key}/{ald_stream_id}/{ald_stream_history}/{id}/"

    #                     objects = ald_s3_client.list_objects_v2(Bucket=bucket_name, Prefix=folder_name)


    #                     if 'Contents' not in objects:
    #                         print(f"No objects found in {bucket_name}/{folder_name}")
    #                         return

    #                     for obj in objects['Contents']:
    #                         object_key = obj['Key']
    #                         file_name = os.path.basename(object_key)
    #                         local_file_path = os.path.join(download_path, file_name)

    #                         try:
    #                             ald_s3_client.download_file(bucket_name, object_key, local_file_path)
    #                             print(f'{object_key} has been downloaded to {local_file_path}')
    #                         except Exception as e:
    #                             print(f'Error downloading {object_key}: {e}')

    #                     return JSONResponse(status_code=200, content={"message": f"File uploaded to {ald_s3_client} successfully"})
                    
    #                 except Exception as e:
    #                     return JSONResponse(status_code=500, content={"error": str(e)})
                    
    #             elif environment == 'GCP':
    #                 print("GCP TBD")
    #             elif environment == 'LOCAL':
    #                 print("LOCAL TBD")
    #             else:
    #                 print('Not Supported')

    #         except Exception as e:
    #             return {"error": str(e)}


    #     @self.router.get("/log_files")
    #     def get_logs_in_workspace_logs_folder():
    #         workspace_log_dir = Path(".workspace/logs")
    #         if not workspace_log_dir.exists():
    #             raise HTTPException(status_code=404, detail="Workspace 'logs' directory not found.")

    #         current_dir_files = [f.name for f in workspace_log_dir.iterdir() if f.is_file()]
    #         return {"folders": current_dir_files}
        
    #     @self.router.get("/read_logs")
    #     async def read_log_file(file_path: str):
    #         log_file_path = os.path.join(".workspace/logs", file_path)
    #         log_file_path = Path(log_file_path)
    #         if not log_file_path.exists():
    #             raise HTTPException(status_code=404, detail=f"Log file not found: {file_path}")

    #         try:
    #             with log_file_path.open("r", encoding="utf-8") as file:
    #                 content = file.read()
    #             return {"content": content}
    #         except Exception as e:
    #             raise HTTPException(status_code=500, detail=f"An error occurred while reading the log file: {str(e)}")

    def get_router(self):
        """라우터 반환 메서드 추가"""
        return self.router