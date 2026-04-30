docker build --no-cache \
  --build-arg CUDA_MAJOR=13 \
  --build-arg CUDA_MINOR=0 \
  --build-arg BUILD_METAPACKAGE=false \
  --build-arg BUILD_COMMON=true \
  --build-arg BUILD_PYTORCH=false \
  --build-arg BUILD_JAX=false \
  -t "aarch_wheel3" -f build_tools/wheel_utils/Dockerfile.aarch .
docker run --runtime=nvidia --gpus=all --ipc=host "aarch_wheel3"
