import re

TAG_VALIDATION_REGEX = re.compile(r"\A[\w][\w.\-]{0,127}\Z")
NAME_VALIDATION_REGEX = re.compile(r"\A[a-z0-9\-_\/]+\Z")


class ImageLogos:
    KERAS = "keras"
    TENSORFLOW = "tensorflow"
    SKLEARN = "sklearn"
    PYTHON = "python"
    R = "r"
    XGBOOST = "xgboost"
    BASH = "bash"
    S3 = "s3"
    SPARK = "spark"
    OPENCV = "opencv"
    PYTORCH = "pytorch"
    VGG = "vgg"
    CNVRG = "cnvrg"
    MXNET = "mxnet"
    TENSOR_RT = "tensor_rt"
    RAPIDS = "rapids"
    INTEL = "intel"
    NVIDIA = "nvidia"

    @classmethod
    def validate_icon(cls, icon_name):
        if icon_name is None or icon_name == "":
            return True

        icon_types = [cls.__dict__[var] for var in vars(cls) if not var.startswith("__")]
        return icon_name in icon_types
