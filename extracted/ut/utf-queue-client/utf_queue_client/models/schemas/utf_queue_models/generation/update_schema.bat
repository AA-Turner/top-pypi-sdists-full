@echo off
setlocal

python --version | findstr /C:"Python 3" > NUL 2>&1
if %errorlevel% neq 0 (
    set "ERROR_MESSAGE=Python 3 is required to run this script"
    goto ERROR
)
set "SEVENZIP=%ProgramFiles%\7-zip\7z.exe"
if not exist "%SEVENZIP%" (
    set "ERROR_MESSAGE=7-Zip required to run this script"
    goto ERROR
)
set JAVA=java
where %JAVA% > NUL 2>&1
if %errorlevel% neq 0 (
    if exist %JAVA_HOME%\bin\java.exe (
        set "PATH=%PATH%;%JAVA_HOME%\bin"
    ) else (
        set "ERROR_MESSAGE=Java is required to run this script"
        goto ERROR
    )
)

echo.

if not exist %~dp0venv (
   echo ===========================================================================
   echo Creating Python Virtual Environment
   python -m venv %~dp0venv
   echo ===========================================================================
   echo.
)
call %~dp0venv\scripts\activate.bat
echo ===========================================================================
echo Installing python requirements
python -m pip install wheel pip -U
pip install -r %~dp0requirements.txt > %TEMP%\pip-output.txt 2>&1
if %errorlevel% neq 0 (
    type %TEMP%\pip-output.txt
    set "ERROR_MESSAGE=Python requirements installation failed!"
    goto ERROR
)
del %TEMP%\pip-output.txt
echo ===========================================================================
echo. 

echo ===========================================================================
echo Generating schema/queue_message.json from schema/queue_message.ts
:: generate queue_message.json schema from queue_message.ts
if exist %~dp0..\schema\elements (
    rd /s /q %~dp0..\schema\elements
)
python %~dp0update_schema.py --schema %~dp0..\schema\queue_message.ts --output %~dp0..\schema\queue_message.json --output_element_dir %~dp0..\schema\elements
if %errorlevel% neq 0 (
    set "ERROR_MESSAGE=JSON schema generation failed!"
    goto ERROR
)
echo ===========================================================================
echo. 

echo ===========================================================================
echo Generating python models
datamodel-codegen --output-model-type pydantic.BaseModel --base-class utf_queue_client.models.base_model.BaseModel --target-python-version 3.8 --enum-field-as-literal all --input %~dp0..\schema\queue_message.json --input-file-type jsonschema --output %~dp0..\models\python\generated_models_pydantic_v1.py
datamodel-codegen --output-model-type pydantic_v2.BaseModel --base-class utf_queue_client.models.base_model.BaseModel --target-python-version 3.8 --enum-field-as-literal all --input %~dp0..\schema\queue_message.json --input-file-type jsonschema --output %~dp0..\models\python\generated_models_pydantic_v2.py
black %~dp0..\models\python
if %errorlevel% neq 0 (
    set "ERROR_MESSAGE=Python model generation failed"
    goto ERROR
)
echo ===========================================================================
echo.

echo ===========================================================================
echo Generating CSharp models
CSharpModelGenerator\CSharpModelGenerator.exe %~dp0..\schema\queue_message.json %~dp0..\models\csharp\GeneratedModels.cs
if %errorlevel% neq 0 (
    set "ERROR_MESSAGE=CSharp model generation failed"
    goto ERROR
)
echo ===========================================================================
echo.

echo ===========================================================================
echo Generating Java models
if exist %~dp0..\models\java (
    rd /s /q %~dp0..\models\java
)
if not exist JavaModelGenerator\jsonschema2pojo-1.1.1\bin\jsonschema2pojo.bat (
    echo Downloading jsonschema2pojo
    mkdir JavaModelGenerator > NUL
    curl -s -f -k https://artifactory.silabs.net/artifactory/infrasw-generic/utf/tools/jsonschema2pojo-1.1.1.zip -o JavaModelGenerator\jsonschema2pojo.zip
    "%SEVENZIP%" x -oJavaModelGenerator JavaModelGenerator\jsonschema2pojo.zip
    if %errorlevel% neq 0 (
        set "ERROR_MESSAGE=Unable to download jsonschema2pojo tool"
        goto ERROR
    )
    del /Q JavaModelGenerator\jsonschema2pojo.zip
)
:: -a GSON -sl -b
call JavaModelGenerator\jsonschema2pojo-1.1.1\bin\jsonschema2pojo.bat -s %~dp0..\schema\elements -303 -b -p com.silabs.utf.QueueModels  --target %~dp0..\models\java
if %errorlevel% neq 0 (
    set "ERROR_MESSAGE=Java model generation failed"
    goto ERROR
)
echo ===========================================================================
echo Patching models
python %~dp0patch_models.py
black %~dp0..\models\python

echo ===========================================================================
echo.

:SUCCESS
echo ===========================================================================
echo All Operations completed successfully!
echo ===========================================================================
echo.
exit /b 0

:ERROR
echo.
echo ===========================================================================
echo %ERROR_MESSAGE%
echo ===========================================================================
echo.
pause
exit /b 1


::pause

