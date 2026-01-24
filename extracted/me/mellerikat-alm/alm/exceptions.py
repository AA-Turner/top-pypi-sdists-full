"""
Exception list

    errors:



"""


class AloError(Exception):
    """
    Raised when undefined error.
    Read the error message and fix it.
    If you cannot fix the error, Please contact the administrator with log file.

    정의되지 않은 예외 발생.
    에러 메시지를 읽고, 해당 내용을 수정하세요.
    에러의 원인을 찾거나, 수정할 수 없다면, 로그 파일을 관리자에게 전달 후 조치 방법을 문의하세요.
    """

    codes = {}
    code = None  # error code
    fmt = '[{code}] : {message}'

    def __init__(self, message, exception=None, doc={}, **kwargs):
        try:
            msg = f"{self.fmt.format(code=self.code, message=message, **kwargs)}\n{self.__doc__.format(**{'code':self.code, **doc}) if doc else self.__doc__ }"
            Exception.__init__(self, msg)
        except Exception:
            Exception.__init__(self, message + "\nCheck error format.")

        self.kwargs = kwargs

    def __init_subclass__(cls, **kwargs):
        if not cls.code:
            raise Exception("A constant value must be assigned to the 'code' variable as a class member variable.")
        if AloError.codes.get(cls.code):
            raise Exception(f"{cls.code} is duplicated : {[AloError.codes.get(cls.code).__name__, cls.__name__]}")

        AloError.codes[cls.code] = cls

    @classmethod
    def print(cls):
        print("code,name,description,document")
        print(f"{cls.code},{cls.__name__},{cls.fmt}")
        for k, v in cls.codes.items():
            print(f"{v.__name__},{k},{v.fmt}")


class AloValueError(AloError):

    """
    에러 코드
        {code}

    에러 정보
        {message}

    에러 원인(제약 사항)
        config.yaml 파일에 작성하신 key 혹은 value 값이 잘못되거나 누락되었습니다.
        작성하신 값을 확인하세요.

    조치 가이드
        config.yaml 파일에 작성하신 내용을 다시 한번 확인하세요.

    참고 사항
        config.yaml 파일의 예시는 아래와 같습니다.
            components:
            >>> local_host:
            >>>    port: 1444
            >>> vector_store:
            >>>    uri: https://10.158.2.41:9800
            >>>    type: Faiss # Faiss
            >>> ...
            >>> service_api:
            >>>   path:
            >>>     /api/generate_questions: # api 경로
            >>>       POST: # method 정의
            >>>         handler: rest_api_index.generate_questions # 파일 명.함수 명
            >>>         parameter: # 함수의 args. 입력 타입 설정
            >>>           target: str
            >>>           purpose: str
    """

    code = "ALO-VAL-000"

    # """
    # Raised when found invalid key or value error.
    # Check key or value
    # """
    #fmt = '[{code}] Found invalid value : {message}'


#################
# Alo Init Error
class AloInitError(AloError):
    """
    Raised when function initialization fails.
    Check required field, network, git, redis, config.yaml or solution meta...
    """

    code = "ALO-INI-000"
    fmt = '[{code}] Failed alo init : {message}'


# class AloInitGitError(AloError):
#     """
#     Raised when branch not found in upstream origin.
#     Check the same branch name exists in the upstream origin.
#     """

#     code = "ALO-INI-001"
#     fmt = '[{code}] Failed install alolib : {message}'


class AloInitRequirementError(AloError):
    """
    Raised when the 3rd party library cannot be installed.
    Check the 3rd party library list and version in the requirements.txt file..
    """

    code = "ALO-INI-002"
    fmt = '[{code}] Failed installing alolib requirements.txt : {message}'


class AloInitFileNotFountError(AloError):
    """
    {message} 경로에 파일이 존재하지 않습니다. 경로 및 파일을 확인해주세요.
    """

    code = "ALO-INI-003"
    fmt = '[{code}] {message} 경로에 파일이 존재하지 않습니다. 경로 및 파일을 확인해주세요.'


class AloInitRedisError(AloError):
    """
    Raised when unable to connect to redis.
    Check redis config, or redis status
    """

    code = "ALO-INI-004"
    fmt = '[{code}] Failed to connect redis : {message}'


class AloInitInvalidKeyValueError(AloError):
    """
    Raised when set an invalid key or value.
    Check the key and value values in the yaml(or value).
    """

    code = "ALO-INI-005"
    fmt = '[{code}] Found an invalid keys or values in file : {file}\n{message}'


class AloInitJsonInvalidError(AloError):
    """
    Raised when set an invalid json string.
    Check json string.
    """

    code = "ALO-INI-006"
    fmt = '[{code}] Found an invalid keys or values in json string : {message}'

class AlmInitKeyError(AloError):
    """
    Error Code: ALM-INI-001
    {message}
    """

    code = "ALM-INI-001"
    fmt = '[{code}] Found an invalid keys or values in config.yaml'

class AlmInitConfigFileError(AloError):
    """
    Error Code: ALM-INI-002
    {message}
    """

    code = "ALM-INI-002"
    fmt = '[{code}] Can not found config.yaml'

class AlmInitFileNotFountError(AloError):
    """
    {message} 경로에 파일이 존재하지 않습니다. 경로 및 파일을 확인해주세요.
    """

    code = "ALM-INI-003"
    fmt = '[{code}] {message} 경로에 파일이 존재하지 않습니다. 경로 및 파일을 확인해주세요.'



class AloInitNameError(AloError):

    """
    에러 코드
        {code}

    에러 정보
        - Invalid call: {file}

    에러 원인
        제작하신 Service API의 {file}이 python 파일 이름 혹은 함수 명에 'alo-llm' 혹은 'main'을 포함합니다.

    조치 가이드
        | {file}의 'alo-llm' 혹은 'main' 부분을 수정해주세요.
        | Ex) chat_generator.main -> chat_generator.chat # chat_generator.py 내 main 함수 명 수정 시
        | Ex) main.generator -> chat_generator.generator # main.py 파일 명 수정 시
    """

    code = "ALO-INI-001"

#################
# pipeline Error
class AloPipelineInitError(AloError):
    """
    Raised when initializing the pipeline.
    """

    code = "ALO-PIP-000"
    fmt = '[{code}] Check the yaml file : {message}'


class AloPipelineAssetError(AloError):
    """
    Raised when failed to set up the assets in the scripts folder based on whether the code source is local or git.
    """

    code = "ALO-PIP-001"
    fmt = '[{code}] Check the code source of asset or git : {message}'


class AlmPipelineImportError(AloError):

    """
    에러 코드
        {code}

    에러 정보
        {message}

    에러 원인(제약 사항)
        모듈 또는 함수를 가져오지 못해 발생한 에러입니다. 
        작성한 config.yaml 파일에 작성한 handler 부분에서 에러가 발생했을 수 있습니다.

    조치 가이드
        Handler에 작성한 파일 명 및 함수 명을 다시 한번 확인해주세요. 

    참고 사항
        config.yaml 파일 예시는 아래와 같습니다.
            >>> rest_api.chat # 파일 명(rest_api).함수 명(chat)
    """

    code = "ALM-PIP-001"

class AlmPipnameError(AloError):
    """
    Error Code: ALM-PIP-002
    {message}
    """

    code = "ALM-PIP-002"
    fmt = '[{code}] Found an invalid keys or values in config.yaml'


class AloPipelineBatchError(AloError):
    """
    Raised when failed operate batch job.
    """

    code = "ALO-PIP-003"
    fmt = '[{code}] Check the {pipeline}(pipeline) : {message}'


class AloPipelineArtifactError(AloError):
    """
    Raised when Failed to empty & re-make artifacts.
    """

    code = "ALO-PIP-004"
    fmt = '[{code}] Check pipeline : {pipeline} - {message}'


class AloPipelineRequirementsError(AloError):
    """
    Raised when the 3rd party library cannot be installed.
    Check the library version or network.
    """

    code = "ALO-PIP-005"
    fmt = '[{code}] Found error when installing the package : {pipeline} - {message}'


class AloPipelineBackupError(AloError):
    """
    Raised when backup error history & save error artifacts.
    """

    code = "ALO-PIP-006"
    fmt = '[{code}] Check : {pipeline} - {message}'


class AloPipelineLoadError(AloError):
    """
    Raised when loading external data or duplicated basename in the same pipeline.
    """

    code = "ALO-PIP-007"
    fmt = '[{code}] Failed to load(get) : {pipeline} - {message}'


class AloPipelineSaveError(AloError):
    """
    Raised when save artifacts.
    """

    code = "ALO-PIP-008"
    fmt = '[{code}] Failed to save : {pipeline} - {message}'


class AloPipelineConversionError(AloError):
    """
    Raised when converting data in the execution unit.
    Check solutioin_metadata or experimental_plan.
    """

    code = "ALO-PIP-009"
    fmt = '[{code}] Error : {pipeline} - {message}'


class AloPipelineSerializeError(AloError):
    """
    Raised when the object serialization(pickling) operation fails.
    Check if the object supports serialization by default when save(pickling)/load(unpickling).
    If the default serialization operation is not supported,
    implement the function to directly save/load the object in the path below context['model']['workspace'].
    """

    code = "ALO-PIP-010"
    fmt = '[{code}] Error : {message}'


class AloPipelineSummaryError(AloError):
    """
    Raised when create summary report.
    Check the values of result, score, note, probability
    """

    code = "ALO-PIP-011"
    fmt = '[{code}] Error : {message}'


class AloPipelineCompressError(AloError):
    """
    Raised when an error occurs while compressing/decompressing a file.
    Check the file extension to make sure it is a valid format.
    """

    code = "ALO-PIP-012"
    fmt = '[{code}] Compress/Decompress Error : {message}'


class AloPipelineArgumentError(AloError):
    """
    Raised when an argument value is invalid.
    Check the argument's settings.
    """

    code = "ALO-PIP-013"
    fmt = '[{code}] {message}'

class AloPipelineImportError(AloError):

    """
    에러 코드
        {code}

    에러 정보
        {message}

    에러 원인(제약 사항)
        config.yaml 파일의 pip: 부분에 작성한 라이브러리 설치에 실패했습니다.
        작성한 라이브러리 명 혹은 버전을 확인해주세요.

    조치 가이드
        config.yaml 파일에 명시한 라이브러리를 다시 한번 확인해주세요.

    참고 사항
        requirements 파일 예시는 아래와 같습니다.
            >>> library_name==version
    """

    code = "ALO-PIP-014"

#################
# Package Error
class AloPackageRequirementsError(AloError):
    """
    Raised when the 3rd party library cannot be installed.
    Check the library version or network.
    """

    code = "ALO-PAC-000"
    fmt = '[{code}] Found error when installing the package : {message}'


#################
# Sagemaker Error
class AloSagemakerInitError(AloError):
    """
    Raised when initialize various SageMaker-related config information as class variables.
    """

    code = "ALO-SAG-000"
    fmt = '[{code}] Message : {message}'


class AloSagemakerSetupError(AloError):
    """
    Raised when copy the elements required for docker build into the sagemaker directory for the given list of pipelines.
    """

    code = "ALO-SAG-001"
    fmt = '[{code}] Message : {message}'


class AloSagemakerBuildError(AloError):
    """
    Raised when docker build, ecr push, create s3 bucket for sagemaker.
    """

    code = "ALO-SAG-002"
    fmt = '[{code}] Message : {message}'


class AloSagemakerEstimatorError(AloError):
    """
    Raised when fit sagemaker estimator (execute on cloud resource).
    """

    code = "ALO-SAG-003"
    fmt = '[{code}] Message : {message}'


class AloSagemakerTrainError(AloError):
    """
    Raised when failed to download sagemaker trained model.
    """

    code = "ALO-SAG-004"
    fmt = '[{code}] Message : {message}'


#################
# Asset Error
class AloAssetSetupError(AloError):
    """
    Raised when failed to install asset.
    Check for duplicate step names and raise an error if any exist.
    """

    code = "ALO-ASS-000"
    fmt = '[{code}] Message : {message}'


class AloAssetRunError(AloError):
    """
    Raised when failed to user asset run.
    Check source code of user asset.
    """

    code = "ALO-ASS-001"
    fmt = '[{code}] Message : {message}'


class AloArtifactFileNoneError(AloError):
    """
    에러 코드
        {code}

    에러 정보
        Stage: {stage}

    에러 원인(제약 사항)
        추론 실행 결과 파일을 찾을 수 없습니다.
        저장할 수 있는 파일 개수는 2개 이하로 제한 되며, 반드시 1개 이상의 파일을 생성해야 합니다.

    조치 가이드
        참고 사항과 같이 한 개 이상의 파일이 저장될 수 있도록 기능을 구현하세요.

    참고 사항
        pipeline['artifact']['workspace'] 의 경로 정보를 참조하여 파일 생성
            >>> with open(os.path.join(pipeline['artifact']['workspace'], "inference1.csv"), "w") as f:
            >>>     f.write("inference1")
    """

    code = "ALO-ART-001"


class AloArtifactFileLimitError(AloError):
    """
    에러 코드
        {code}

    에러 정보
        - Stage:     {stage}
        - Artifacts: {files}

    에러 원인(제약 사항)
        추론 결과 파일은 2개를 초과하여 저장할 수 없습니다.
        저장할 수 있는 파일 개수는 2개 이하로 제한 되며, 반드시 1개 이상의 파일을 생성해야 합니다.

    조치 가이드
        에러 정보의 Artifacts 항목을 참고하여 파일 개수를 2개 이하로 제한하세요.
        불필요한 파일이 존재한다면 삭제하세요.

    참고 사항
        pipeline['artifact']['workspace'] 는 추론 파일을 저장하기 위한 경로 정보를 제공합니다.
            >>> print(pipeline['artifact']['workspace']) # /var/alo/workspace/train/output/result.csv

        pipeline['artifact']['workspace'] 값을 참조하여 파일 저장 로직을 구현한 부분이 있다면
        파일 저장 개수 제약 사항에 위반되지 않도록 불필요한 파일 저장 로직은 삭제하세요.
    """

    code = "ALO-ART-002"


class AloArtifactFileExtensionError(AloError):
    """
    에러 코드
        {code}

    에러 정보
        - Stage:    {stage}
        - Artifact: {files}

    에러 원인(제약 사항)
        허용되지 않는 파일 유형이 추론 결과 파일에 포함되어 있습니다.
        csv, jpg, jpeg, png, svg 파일 유형만 저장 가능합니다.

    조치 가이드
        에러 정보의 Artifacts 항목을 참고하여 허용되지 않는 파일 유형을 확인 후
        해당 파일 유형을 변경 또는 삭제하세요.

    참고 사항
        pipeline['artifact']['workspace'] 는 추론 파일을 저장하기 위한 경로 정보를 제공합니다.
            >>> print(pipeline['artifact']['workspace']) # /var/alo/workspace/train/output/result.csv
    """

    code = "ALO-ART-003"


class AloUserPipelineRuntimeError(AloError):
    """
    에러 코드
        {code}

    에러 정보
        - File:     {file}
        - Function: {function}
        - Message:  {message}

    에러 원인
        사용자 파이프라인 함수(python 코드) 실행중에 runtime 에러가 발생하였습니다.

    조치 가이드
        에러 정보의 File(python 코드)에서의 에러가 발생하였습니다.
        에러 메시지 상단의 Traceback을 참고하여 에러 발생 위치 및 exception 메시지를 확인 후
        코드를 수정하세요.

    참고 사항
        ALO에서 제공되는 context, pipeline 두 참조 dict 객체는 아래와 같은 정보를 가지고 있습니다.
        context: ALO 수행과 관련된 정보를 조회하거나, 저장할 수 있는 객체
            context['stage']: 현재 수행중인 단계(train 또는 inference) 리턴
                >>> print(context['stage']) # train or inference
            context['model']['workspace']: 모델 저장 경로 반환.
                >>> print(os.path.join(context['model']['workspace'], 'model.pickle')) # /var/alo/workspace/model/model.pickle
            context['model'][파일명]: 파일명(pickle 확장자 제외)에 해당하는 model을 메모리로 로딩 후 객체로 반환하거나, 저장(pickling 지원 대상만 해당)
                >>> context['model']['titanic'] = RandomForestClassifier(n_estimators=n_estimators, max_depth=5, random_state=1)  # titanic 이라는 이름으로 모델 객체를 파일로 저장
                >>> model = context['model']['titanic'] # titanic 이름으로 저장된 모델을 객체로 로딩 후 반환
        pipeline: train, inference 단계 수행시 dataset, artiface 파일 정보를 조회할 수 있는 객체
            pipeline['dataset']['workspace' 또는 파일명]: dataset 파일이 저장된 경로를 반환
                >>> print(os.path.join(pipeline['dataset']['workspace'], 'dataset.csv')) # /var/alo/workspace/train/dataset/file.csv
                >>> print(pipeline['dataset']['file.csv'])                               # /var/alo/workspace/train/dataset/file.csv (위와 동일)
            pipeline['artifact']['workspace']: artifact 파일을 저장하기 위한 경로를 반환
                >>> print(os.path.join(pipeline['artifact']['workspace'])) # /var/alo/workspace/train/output
    """

    code = "ALO-USR-001"


class AloUserPythonHandlerError(AloError):
    """
    에러 코드
        {code}

    에러 정보
        - File:     {file}
        - Function: {function}
        - Message:  {message}

    에러 원인
        사용자 파이프라인 함수(python 코드) 핸들러 정의시
        Message 내용과 같이 제약사항을 준수하지 않았습니다.

    조치 가이드
        아래 참고 사항을 참조하여 함수 정의 부분을 수정하세요.

    참고 사항
        ALO는 사용자 정의 함수를 실행 시점에 3가지 유형의 (객체)를 전달할 수 있습니다.

        1. context: ALO 수행과 관련된 정보를 조회하거나, 저장할 수 있는 객체
        2. pipeline: train, inference 단계 수행시 dataset, artiface 파일 정보를 조회할 수 있는 객체
        3. 사용자 정의 keyword arguments

        positional arguments 제약 사항
            - 인자가 없는 경우 : 아무런 정보도 넘겨줄 수 없음으로 dataset/model 정보를 가져올 수 없음
                >>> train():
                >>>     ...
            - 인자가 1개인 경우 : pipeline 객체를 전달
                >>> train(pipeline):
                >>>     print(pipeline['dataset']['file.csv'])
            - 인자가 2개인 경우 : context, pipeline 객체를 전달
                >>> train(context, pipeline):
                >>>     print(context['startAt'])
                >>>     print(pipeline['dataset']['file.csv'])
            - 인자가 3개 이상인 경우 :
                -> 오류(ALO-USR-002) 발생

        keyword arguments 제약 사항
            - keyword arguments 정의 하지 않는 경우
                >>> train(pipeline):
                >>>     ...
            - keyword arguments 개별 기본 값 정의
                >>> train(pipeline, x_columns=[], y_column=None, n_estimators=100):
                >>>     ...
            - keyword arguments dict형 정의
                >>> train(pipeline, **kwargs):
                >>>     kwargs['x_columns']
            - keyword arguments 와 solution.function.[함수명].argument 가 불일치 하는 경우
                -> 오류(ALO-USR-002) 발생

    """

    code = "ALO-USR-002"


class AloDatasetKeyNotFoundError(AloError):
    """
    에러 코드
        {code}

    에러 정보
        - Stage: {stage}
        - Key:   {key}

    에러 원인
        찾고자 하는 dataset 파일명({key})이 잘못되었거나,
        또는 파일이 누락된 경우에 해당합니다.

    조치 가이드
        | Key는 config.yaml 파일의 solution.{stage}.dataset_uri에 설정된 경로 이하 또는 압축 파일 내에 폴더명 및 확장자명을 포함한 경로 형태여야 합니다.
        | Ex) pipeline['dataset']['path/train.csv']
        | 아래 각 항목을 점검하세요.

        1. config.yaml의 solution.{stage}.dataset_uri 설정 유무 확인
        2. 압축 파일인 경우 파일 내부에 파일 포함 여부 확인
        3. 압축 파일 내부 폴더 이하에 파일이 존재하는 경우 경우
            >>> print(pipeline['dataset']['파일명.csv'])       # 오류 발생
            >>> print(pipeline['dataset']['폴더명/파일명.csv']) # /var/alo/workspace/train/dataset/폴더명/파일명.csv
        4. key에 파일 확장자명 누락된 경우
            >>> print(pipeline['dataset']['파일명'])           # 오류 발생
            >>> print(pipeline['dataset']['파일명.csv'])       # /var/alo/workspace/train/dataset/파일명.csv

    참고 사항
        pipeline['dataset'] 객체는 train/inference의 필요한 파일들에 대한 경로 정보를 제공합니다.
            >>> print(pipeline['dataset']['workspace']) # /var/alo/workspace/train/dataset
            >>> print(pipeline['dataset']['file.csv'])  # /var/alo/workspace/train/dataset/file.csv
    """

    code = "ALO-DTS-001"


class AloDatasetFileNotFoundError(AloError):
    """
    에러 코드
        {code}

    에러 정보
        - Stage: {stage}
        - Key:   {key}
        - File:  {file}

    에러 원인
        에러 정보의 Key 경로에 해당하는 File이 삭제되어 찾을 수 없습니다.

    조치 가이드
        사용자 파이프라인 함수(python 코드) 등록된 파일을 삭제한 로직이 없는지 검토가 필요합니다.

    참고 사항
        pipeline['dataset'] 객체는 train/inference의 필요한 파일들에 대한 경로 정보를 제공합니다.
            >>> print(pipeline['dataset']['workspace']) # /var/alo/workspace/train/dataset
            >>> print(pipeline['dataset']['file.csv'])  # /var/alo/workspace/train/dataset/file.csv
    """

    code = "ALO-DTS-002"


class AloModelFileNotFoundError(AloError):
    """
    에러 코드
        {code}

    에러 정보
        - Key:   {key}
        - File:  {file}

    에러 원인
        에러 정보의 Key에 해당하는 모델 파일(pickle)을 찾을 수 없습니다.

    조치 가이드
        key 및 모델 파일이 존재하는지 확인이 필요합니다.
        1. config.yaml 파일의 solution.[stage].model_uri에 모델 파일 여부 확인
        2. 모델 파일의 확장자명이 .pkl 인지 여부 확인
        3. key명 오탈자 여부 확인
        4. key명에 확장자 포함 여부 확인

    참고 사항
        context['model'] 객체는 모델 파일(pickle)에 대한 정보를 제공하고 있습니다.
            >>> model = context['model']['titanic']     # titanic 이름으로 저장된 모델을 객체로 로딩 후 반환
            >>> model = context['model']['titanic.pkl'] # 오류 발생
    """

    code = "ALO-MDL-001"


class AloModelUnpicklingError(AloError):
    """
    에러 코드
        {code}

    에러 정보
        - Key:   {key}
        - File:  {file}

    에러 원인
        에러 정보의 Key에 해당하는 모델 파일(pickle)을 메모리를 로드(unpickling)할 수 없습니다.
        일부 모델 객체는 python pickling/unpickling 기능이 지원되지 않습니다.

    조치 가이드
        1. requirements.txt의 모델에 해당하는 library가 동일 버전인지 확인
            -> train시 pickle 파일로 저장시 library 버전과 unpickle시 library 버전이 상이한 경우
            Ex) scikit-learn==1.4.0 의 모델 객체를 pickle 파일로 저장 후 scikit-learn==1.5.0 버전으로 unpickle 시 오류 발생
        2. 모델 객체에 대해 pickling/unpickling을 지원하지 않는 경우
            A. pickling/unpickling 기능을 직접 구현하는 방법
                >>> import os
                >>> def pickle(context, model: object):
                >>>     # model_bytes =  ...(변환 로직 구현)
                >>>     with open(os.path.join(context['model']['workspace'], "my_custom_model.pkl"), "wb") as f:  # 모델 경로 이하에 저장
                >>>         f.write(model_bytes)
                >>> model = None
                >>> def unpickle(context):
                >>>     global model  # 모델 객체 생성에 대한 cost를 줄이기 위해 global 변수를 통해 재사용
                >>>     # model_bytes =  ...(변환 로직 구현)
                >>>     if model is None:
                >>>         with open(os.path.join(context['model']['workspace'], "my_custom_model.pkl"), "rb") as f:  # 모델 경로 이하에 저장
                >>>             model_bytes = f.read()
                >>>             model = ...(변환 로직 구현)
                >>>     return model
            B. 모델 객체의 parameter 만 pickle 파일로 저장 후 모델 객체의 parameter로 전달하는 방법
                >>> def train(context: dict, pipeline: dict):
                >>>     context['model']['titanic_param'] = ("n_estimators": 100, "max_depth": 5, "random_state": 1)  # model parameter pickle로 저장
                >>>     model = RandomForestClassifier(**context['model']['titanic_param'])
                >>> model = None
                >>> def inference(context: dict, pipeline: dict):
                >>>     global model  # 모델 객체 생성에 대한 cost를 줄이기 위해 global 변수를 통해 재사용
                >>>     if model is None:
                >>>         titanic_param = context['model']['titanic_param']
                >>>         model = RandomForestClassifier(**titanic_param)

    참고 사항
        ALO에서는 python pickle library 를 사용하여
        pickling(객체 -> 파일) 또는 unpickling(파일 -> 객체) 하는 기능을 기본 지원하고 있습니다.
            >>> def train(context: dict, pipeline: dict):
            >>>     model = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=1)
            >>>     context['model']['titanic'] = model  # 모델을 파일로 pickling
            >>>
            >>> def inference(context: dict, pipeline: dict):
            >>>     model = context['model']['titanic']  # 파일을 RandomForestClassifier 객체로 unpickling

        일부 모델 객체들에 대해서는 python pickle 기능이 적용되지 않음으로
        조치 가이드 2번 항목을 참고하세요.

    """

    code = "ALO-MDL-002"


class AloModelPicklingError(AloError):
    """
    에러 코드
        {code}

    에러 정보
        - Key:   {key}
        - File:  {file}

    에러 원인
        에러 정보의 Key에 해당하는 객체(모델)를 파일(pickle)로 저장(pickling)할 수 없습니다.
        일부 모델 객체는 python pickling/unpickling 기능이 지원되지 않습니다.

    조치 가이드
        1. 사용중인 library에서의 pickling 제공 여부를 확인하거나, 제 3의 library(Ex. fickling 등) 적용
        2. 모델 객체에 대해 pickling/unpickling을 지원하지 않는 경우
            A. pickling/unpickling 기능을 직접 구현하는 방법
                >>> import os
                >>> def pickle(context, model: object):
                >>>     # model_bytes =  ...(변환 로직 구현)
                >>>     with open(os.path.join(context['model']['workspace'], "my_custom_model.pkl"), "wb") as f:  # 모델 경로 이하에 저장
                >>>         f.write(model_bytes)
                >>> model = None
                >>> def unpickle(context):
                >>>     global model  # 모델 객체 생성에 대한 cost를 줄이기 위해 global 변수를 통해 재사용
                >>>     # model_bytes =  ...(변환 로직 구현)
                >>>     if model is None:
                >>>         with open(os.path.join(context['model']['workspace'], "my_custom_model.pkl"), "rb") as f:  # 모델 경로 이하에 저장
                >>>             model_bytes = f.read()
                >>>             model = ...(변환 로직 구현)
                >>>     return model
            B. 모델 객체의 parameter 만 pickle 파일로 저장 후 모델 객체의 parameter로 전달하는 방법
                >>> def train(context: dict, pipeline: dict):
                >>>     context['model']['titanic_param'] = ("n_estimators": 100, "max_depth": 5, "random_state": 1)  # model parameter pickle로 저장
                >>>     model = RandomForestClassifier(**context['model']['titanic_param'])
                >>> model = None
                >>> def inference(context: dict, pipeline: dict):
                >>>     global model  # 모델 객체 생성에 대한 cost를 줄이기 위해 global 변수를 통해 재사용
                >>>     if model is None:
                >>>         titanic_param = context['model']['titanic_param']
                >>>         model = RandomForestClassifier(**titanic_param)

    참고 사항
        ALO에서는 python pickle library 를 사용하여
        pickling(객체 -> 파일) 또는 unpickling(파일 -> 객체) 하는 기능을 기본 지원하고 있습니다.
            >>> def train(context: dict, pipeline: dict):
            >>>     model = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=1)
            >>>     context['model']['titanic'] = model  # 모델을 파일로 pickling
            >>>
            >>> def inference(context: dict, pipeline: dict):
            >>>     model = context['model']['titanic']  # 파일을 RandomForestClassifier 객체로 unpickling

        일부 모델 객체들에 대해서는 python pickle 기능이 적용되지 않음으로
        조치 가이드 내용을 참고하세요.
    """

    code = "ALO-MDL-003"


class AloModelTrainFileNotFoundError(AloError):
    """
    에러 코드
        {code}

    에러 정보
        Phase: {phase}

    에러 원인(제약 사항)
        학습(Train) pipline 에서 모델 관련 output 파일이 없습니다.
        조치 가이드와 같이 1개 이상의 모델 관련 파일을 저장하세요.

    조치 가이드
        1. 모델 객체를 pickle 파일로 저장
            >>> model = RandomForestClassifier(n_estimators=n_estimators, max_depth=5, random_state=1)
            >>> context['model']['titanic'] = model

        2. config 정보(dict)를 파일로 저장
            >>> context['model']['model_config'] = dict(n_estimators=100, max_depth=5, random_state=1)

    참고 사항
        context['model'] 객체는 모델 관련 정보를 제공하고 있습니다.
        예제) 모델 관련 객체 또는 설정 정보를 메모리로 로드
            >>> model = context['model']['titanic']     # titanic 이름으로 저장된 모델을 객체로 로딩 후 반환

        예제) 모델 관련 객체 또는 설정 정보를 파일로 쓰기
            >>> context['model']['titanic'] = model     # model 객체를 titanic 파일 정보로 저장

        예제) 사용자 정의 model 관련 파일 생성시 context['model']['workspace'] 경로 정보를 참고하여 파일 생성
            >>> with open(os.path.join(context['model']['workspace'], "titanic.pkl"), "wb") as f:  # 모델 경로 이하에 저장 직접 파일로 저장
            >>>     f.write(model_bytes)  # model 관련 정보를 파일로 저장

    """

    code = "ALO-MDL-004"


class AloModelFileStorageLimitError(AloError):
    """
    에러 코드
        {code}

    에러 정보
        - Property : {property}
        - Message  : {message}

    에러 원인(제약 사항)
        solution.[train|inference] 의 속성 dataset_uri, model_uri 에 로컬 경로 설정시
        제약 사항을 위반하였습니다.

    조치 가이드
        uri 속성에 파일의 위치 정보(S3, 로컬 경로) 작성시
        아래 참고 사항과 같은 제약사항이 존재합니다.

    참고 사항
        - solution.train.dataset_uri은 1개의 폴더만 지정할 수 있습니다.
          1개의 폴더만 지정 가능합니다.
            >>> dataset_uri: dataset/     # 정상
            >>> dataset_uri: dataset.csv  # 오류 - 폴더가 아닌 파일 경로
        - 로컬 경로의 파일 지정시 config.yaml 파일 기준 상대 경로로 작성해야 합니다.
            >>> Ex) 폴더 트리 인 경우
            >>> ./
            >>> ├── config.yaml
            >>> ├── dataset/
            >>> │   ├── train_dataset.csv
            >>> │   └── train_dataset1.csv
            >>>     ...
            >>> └── titanic.py
            >>> dataset_uri: dataset/     # 정상
            >>> dataset_uri: /home/user/alo/titanic/dataset/train_dataset.csv  # 오류 - 절대 경로 및 폴더를 지정함
    """

    code = "ALO-MDL-005"


class AloContextWrongKeyTypeError(AloError):
    """
    에러 코드
        {code}

    에러 정보
        - Key: {key}
        - Type: {type}

    에러 원인(제약 사항)
        사용자 정의 key로 등록 가능한 데이터 유형은 문자열만 가능합니다.
        '{type}' 데이터 유형은 key로 사용할 수 없습니다.

    조치 가이드
        >>> context['model'][1] = 'abc'    # 오류 발생. 숫자 1은 key로 사용 불가
        >>> context['model']['1'] = 'abc'  # 정상 수행
        상기 라인을 수정 또는 삭제하세요.

    참고 사항
        시스템에서 제공되는 데이터 key는 모두 문자형 타입입니다.
            - context['model']['workspace']
            - context['model']['example_model']
            - pipeline['dataset']['workspace']
            - pipeline['dataset']['train.csv']
            - pipeline['artifact']['workspace']
    """

    code = "ALO-CTX-001"


class AloContextNotAllowKeyError(AloError):
    """
    에러 코드
        {code}

    에러 정보
        Key: {key}

    에러 원인(제약 사항)
        '{key}' key는 시스템에서 제공되는 key명이며, 읽기만 가능한 key 입니다.
        key에 해당하는 값을 업데이트 할 수 없습니다.

    조치 가이드
        >>> context[...]['{key}'] = '값'
        >>> 또는
        >>> pipeline[...]['{key}'] = '값'
        상기 라인을 수정 또는 삭제하세요.

    참고 사항
        시스템에서 제공되는 일부 key는 임의로 수정할 수 없습니다.
        값 변경 불가한 key 목록입니다.
            - context['model']['workspace']
            - pipeline['dataset']['workspace']
            - pipeline['artifact']['workspace']
    """

    code = "ALO-CTX-002"


class AloContextInvalidStrError(AloError):
    r"""
    에러 코드
        {code}

    에러 정보
        Invalid Key: {invalidKey}

    에러 원인(제약 사항)
        '{invalidKey}'에는 사용 불가능한 문자가 포함되어 있습니다.
        조치 가이드 및 참고 사항을 참고하여 문자 또는 문자열을 변경하세요.

    조치 가이드
        소,중,대 괄호 및 특수문자는 사용 불가능하며,
        아래와 같이 사용가능한 문자열로 변경하세요.
            >>> context['model'][r'key\\test.csv'] = 'test'  # 역슬래쉬(\) 사용에 의한 오류
            >>> context['model']['key/test.csv'] = 'test'  # 정상

    참고 사항
        허용 가능 문자 : 한글, 영문, 숫자, _, -, /, (공백)
        허용 문자열 정규 표현식 : {allowedRegex}
    """

    code = "ALO-CTX-003"


class AloSummaryProbabilityTypeError(AloError):
    """
    에러 코드
        {code}

    에러 정보
        - Key  : summary['probability']
        - Type : {keyType}

    에러 원인(제약 사항)
        파이프라인 함수 실행 결과에 대한 summary의 probability는 dict만 허용됩니다.
        조치 가이드 또는 참고 사항과 같이 수정하세요.

    조치 가이드
        probability 값을 dict 유형으로 변경하세요.
            >>> summary['probability'] = "dead: 0.2, survived: 0.8"      # 오류(value의 data type이 dit 가 아님)
            >>> summary['probability'] = {{"dead": 0.2, "survived": 0.8}}  # 정상

    참고 사항
        파이프라인 함수의 summary는
        아래 예제와 같이 return을 통해 결과를 전달할 수 있습니다.
            >>> def inference(context: dict, pipeline: dict, x_columns=[]):
            >>> ...
            >>>     return {{
            >>>         'summary': {{
            >>>             'result': f"#survived:100 / #total:20",
            >>>             'score': 0.1,
            >>>             'note': "Score means titanic survival ratio",
            >>>             'probability': {{"dead": 0.2, "survived": 0.8}}
            >>>         }}
            >>>     }}
    """

    code = "ALO-SMM-001"


class AloSummaryProbabilityDataTypeError(AloError):
    """
    에러 코드
        {code}

    에러 정보
        - Key        : summary['probability'][{key}]
        - Key Type   : {keyType}
        - Value      : {value}
        - Value Type : {valueType}

    에러 원인(제약 사항)
        파이프라인 함수 실행 결과에 대한 summary의 probability의 item은 key(문자):value(정수 또는 실수) 형태만 허용됩니다.
        조치 가이드 또는 참고 사항과 같이 수정하세요.

    조치 가이드
        아래 예제와 같이
        summary['probability']['key'] = 정수 또는 실수
        key:value 에 대한 데이터 유형을 확인 후 수정하세요.
            >>> summary['probability'][100] = 10        # 오류(key가 문자형이 아님)
            >>> summary['probability']['dead'] = '0.2'  # 오류(value가 숫자(정수 또는 실수)가 아님)
            >>> summary['probability']['dead'] = 0.2    # 정상

    참고 사항
        파이프라인 함수의 summary는
        아래 예제와 같이 return을 통해 결과를 전달할 수 있습니다.
            >>> def inference(context: dict, pipeline: dict, x_columns=[]):
            >>> ...
            >>>     return {{
            >>>         'summary': {{
            >>>             'result': f"#survived:100 / #total:20",
            >>>             'score': 0.1,
            >>>             'note': "Score means titanic survival ratio",
            >>>             'probability': {{"dead": 0.2, "survived": 0.8}}
            >>>         }}
            >>>     }}
    """

    code = "ALO-SMM-002"


class AloSummaryProbabilityValueSumError(AloError):
    """
    에러 코드
        {code}

    에러 정보
        - Values        : {values}
        - Sum of Values : {sumValues}

    에러 원인(제약 사항)
        파이프라인 함수 실행 결과에 대한 summary의 probability value의 합은 1.0 과 같아야만 합니다.
        조치 가이드 또는 참고 사항과 같이 수정하세요.

    조치 가이드
        summary['probability'].values() 의 합이 1이 되도록 값을 수정하세요.
            >>> summary['probability'] = {{"dead": 0.1, "survived": 0.8}}  # 오류(합계가 1.0과 같지 않음)
            >>> summary['probability'] = {{"dead": 0.2, "survived": 0.8}}  # 정상

    참고 사항
        파이프라인 함수의 summary는
        아래 예제와 같이 return을 통해 결과를 전달할 수 있습니다.
            >>> def inference(context: dict, pipeline: dict, x_columns=[]):
            >>> ...
            >>>     return {{
            >>>         'summary': {{
            >>>             'result': f"#survived:100 / #total:20",
            >>>             'score': 0.1,
            >>>             'note': "Score means titanic survival ratio",
            >>>             'probability': {{"dead": 0.2, "survived": 0.8}}
            >>>         }}
            >>>     }}
    """

    code = "ALO-SMM-003"


class AloExperimentalPlanFileNotFoundError(AloError):
    """
    에러 코드
        {code}

    에러 정보
        File Not Found : {fileNotFound}

    에러 원인(제약 사항)
        config.yaml 파일을 찾을 수 없습니다.
        조치 가이드 내용과 같이 파일 경로 확인 또는 옵션을 지정하세요.

    조치 가이드
        config.yaml 파일이 현재 경로에 있는지 확인하세요.

    참고 사항
        사용자 logic code를 Service API로 변환하기 위해서는 config.yaml 파일이 존재하는 폴더 이하에 logic code 생성 후
        yaml의 api 항목에 제작한 Service API를 정의하세요.
            >>> Ex) 폴더 트리
            >>> ./
            >>> ├── config.yaml
            >>> └── logic_code.py
        Ex) config.yaml 사용자 함수 정의 작성 방법
            >>> path:
            >>>   /api/generate_questions: # api 경로
            >>>     POST: # method 정의
            >>>       handler: rest_api_index.generate_questions # {파일 명}.{함수 명}
            >>>       parameter: # 함수의 args. 입력 타입 설정
            >>>         target: str
            >>>         purpose: str
    """

    code = "ALO-EPP-001"


class AloSolutionStreamApiStatusCodeError(AloError):
    """
     에러 코드
         {code}

     에러 정보
         - Type        : {type}
         - API         : {api}
         - Status Code : {statusCode}
         - Message     : {message}

     에러 원인
        API 호출 결과 정상적인 응답을 받지 못하였습니다.
        메시지 정보를 읽고 관련 내용을 직접 조치하거나,
        조치 불가능한 경우 AI Conductor 관리자에게 문의하세요.
     """

    code = "ALO-SSA-001"


class AloSolutionStreamFileNotFoundError(AloError):
    """
    에러 코드
        {code}

    에러 정보
        File : {file}

    에러 원인
        File 정보를 찾을 수 없습니다.
        아래 참고 사항을 읽고 누락된 설정 파일이 없는지 확인하세요.
        ALO 관리자에게 문의하세요.

    참고 사항
        ALO 실행 및 솔루션 등록을 위해서는 아래 예제와 같이 파일 구성이 필요합니다.
            >>> ./
            >>> ├── config.yaml      # ALO 실행 환경 설정 파일
            >>> ├── inference/
            >>> │   └── dataset.csv             # titanic.의 추론용 테스트 파일
            >>> ├── titanic.py                  # ALO 실행 소스 코드
            >>> ├── train/
            >>> │   └── dataset.csv             # titanic.의 학습용 테스트 파일
            >>> └── setting/                    # 솔수션 등록 관련 환경 설정
            >>>     ├── infra_config.yaml           # mellerikat 인프라 구성 정보
            >>>     └── solution_info.yaml          # 솔루션 등록 환경 설정 정보
     """

    code = "ALO-SSA-002"


class AloSolutionStreamAwsCredentialsError(AloError):
    """
     에러 코드
         {code}

     에러 정보
         - AWS Profile : {awsProfile}
         - Service Name: {serviceName}

     에러 원인
        AWS Profile 을 찾을 수 없거나, 또는 권한이 없을 수 있습니다.

    조치 가이드
        AWS Profile 이 정상적으로 설정되 있는지 아래 명령어를 통해서 확인하세요.
            >>> $ aws configure list --profile your_profile
            >>>           Name                    Value             Type    Location
            >>>           ----                    -----             ----    --------
            >>>        profile             your_profile             None    None
            >>>     access_key     ******************** shared-credentials-file
            >>>     secret_key     ******************** shared-credentials-file
            >>>         region           ap-northeast-2      config-file    ~/.aws/config

        AWS Profile 을 확인할 수 없다면, 아래 명령어를 통해서 설정하세요.
            >>> $ aws configure
            >>> AWS Access Key ID [None]: AKIAIOSFODNN7EXAMPLE
            >>> AWS Secret Access Key [None]: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
            >>> Default region name [None]: us-west-2
            >>> Default output format [None]: json

        권한이 누락된 경우 AWS Admin에게 문의하세요.
     """

    code = "ALO-SSA-003"


class AloSolutionStreamApiCallError(AloError):
    """
     에러 코드
         {code}

     에러 정보
         - API   : {api}
         - Error : {error}

     에러 원인
        API를 호출할 수 없습니다.
        에러 정보와 함께 AI Conductor 관리자에게 문의하세요.
     """

    code = "ALO-SSA-004"


class AloSolutionStreamLoginFailError(AloError):
    """
     에러 코드
         {code}

     에러 정보
         Message : {message}

     에러 원인
        사용자 정보가 불일치 하거나, 부족합니다.
        계정 정보를 확인하세요.
     """

    code = "ALO-SSA-005"


class AloSolutionStreamWrongNameError(AloError):
    """
     에러 코드
         {code}

     에러 정보
         - Name   : {name}
         - Message: {message}

     에러 원인(제약 사항)
        Solution 생성시 아래 제약사항을 위반하였습니다.
        명명 규칙 및 신규/수정 설정값을 참고 하세요.

    조치 가이드
        아래 참고 사항을 통해서 이름 작성 규칙 및 신규 생성 여부 설정값을 확인하세요.

    참고 사항
        신규 생성시 Solution name 작성 규칙
            - 동일 이름 생성 불가
            - 길이는 100 byte 를 이내
            - 영문 소문자, 대문자, 숫자, -(대시) 문자만 허용
            - 공백 불가

        setting/solution_info.yaml의 solution_update 속성
            - false: 신규 생성을 의미
            - true: 기존 항목을 수정을 의미
     """

    code = "ALO-SSA-006"


class AloSolutionStreamFileOpenFailError(AloError):
    """
     에러 코드
         {code}

     에러 정보
         - File : {file}
         - Message: {message}

     에러 원인
        File 열거나 저장할 수 없습니다.
        ALO 관리자에게 문의하세요.
     """

    code = "ALO-SSA-007"


class AloSolutionStreamStorageApiError(AloError):
    """
     에러 코드
         {code}

     에러 정보
         - Type    : {type}
         - Source  : {source}
         - Target  : {target}
         - Message : {message}

     에러 원인
        솔루션 등록/수정/삭제 작업을 위한 파일 관리 작업에 실패하였습니다.
        Source/Target 경로가 잘못되었가나, 권한이 없을 수 있습니다.

        setting/infra_config.yaml 파일의 AWS_KEY_PROFILE 설정 항목 확인 후
        해당 profile명이 업로드 권한을 가지고 있는 것인지 확인이 필요합니다.

    참고 사항
        setting/infra_config.yaml 의 AWS_KEY_PROFILE 명을 통해서 솔루션 등록 작업을 이루어지게 됩니다.

        AWS_KEY_PROFILE: aws credentials profile 명
            - 미설정시 : default OS 환경 변수 또는 부여된 role을 사용
            - 설정시 : aws credentials profile 명 사용
     """

    code = "ALO-SSA-008"


class AloSolutionStreamDockerFailError(AloError):
    """
     에러 코드
         {code}

     에러 정보
         - Phase   : {phase}
         - Message : {message}

     에러 원인
        Docker file 생성 작업 중 오류가 확인되었습니다.
        ALO 관리자에게 에러 메시지와 함께 문의하세요.
     """

    code = "ALO-SSA-009"


class AloSolutionStreamEcrApiError(AloError):
    """
     에러 코드
         {code}

     에러 정보
         - Type       : {type}
         - Repository : {repository}
         - Message    : {message}

     에러 원인
        솔루션 이미지 관리를 위한 Container Registry 작업에 실패하였습니다.
        권한이 없거나, 잘못된 접근일 수도 있습니다.
        에러 메시지를 확인하세요.

        setting/infra_config.yaml 파일의 AWS_KEY_PROFILE 설정 항목 확인 후
        해당 profile명이 업로드 권한을 가지고 있는 것인지 확인이 필요합니다.

        오류 원인 및 조치가 어려운 경우 ALO 담당자에게 문의하세요.

    참고 사항
        setting/infra_config.yaml 의 AWS_KEY_PROFILE 명을 통해서 솔루션 등록 작업을 이루어지게 됩니다.

        AWS_KEY_PROFILE: aws credentials profile 명
            - 미설정시 : default OS 환경 변수 또는 부여된 role을 사용
            - 설정시 : aws credentials profile 명 사용
     """

    code = "ALO-SSA-010"


class AloSolutionStreamCodeBuildError(AloError):
    """
     에러 코드
         {code}

     에러 정보
         Message : {message}

     에러 원인
        Code Build 관련 작업 수행 중 오류가 발생했습니다.
        ALO 관리자에게 에러 메시지와 함께 문의하세요.
     """

    code = "ALO-SSA-011"


class AloSolutionStreamRegisterLimitError(AloError):
    """
     에러 코드
         {code}

     에러 정보
         Message: {message}

     에러 원인(제약 사항)
        솔루션 등록 시 아래 참고 사항과 같은 제약 사항이 존재합니다.
        에러 정보의 message를 확인 후 조치하세요.

    조치 가이드
        아래 참고 사항의 제약조건이 위배되지 않도록 수정하세요.

    참고 사항
        - alo 를 통해 1회 이상 실행 후 등록할 수 있습니다.
            -> `alo` 또는 `alo run` 명령어 실행이 필요
        - 이하 사용자 경로 이하에 `alo` 폴더는 포함될 수 없습니다.
            -> 폴더명을 변경 또는 삭제
     """

    code = "ALO-SSA-012"


class AloSolutionStreamGpuLibLimitError(AloError):
    """
     에러 코드
         {code}

     에러 정보
         Message: {message}

     에러 원인(제약 사항)
        GPU 사용을 위해서는 아래와 같은 제약사항이 존재합니다.
        에러 정보의 message를 확인 후 참고 사항과 같이 내용을 수정하세요.

    조치 가이드
        아래 참고 사항의 제약조건이 위배되지 않도록 수정하세요.

    참고 사항
        - GPU를 사용하기 위해서는 tensorflow, torch 둘 중 하나의 버전을 사용해야만 합니다.
            -> requirements 에 tensorflow==2.15.0 과 같이 작성하세요.
        - tensorflow, torch의 상세 버전을 받드시 명시적으로 기입하세요.
              >>> tensorflow          # 오류 : 버전 정보 누락
              >>> tensorflow==2.15.0  # 정상
        - lib별 지원 버전
            - tensorflow : 2.12 ~ 2.15
            - torch      : 2.0, 2.1
            -> 상기 버전외 GPU 는 지원하지 않습니다.
            -> 버전에 대한 추가 지원이 필요한 경우 ALO 관리자에게 문의하세요.
     """

    code = "ALO-SSA-013"

AloErrors = {code: cls for code, cls in AloError.codes.items()}
