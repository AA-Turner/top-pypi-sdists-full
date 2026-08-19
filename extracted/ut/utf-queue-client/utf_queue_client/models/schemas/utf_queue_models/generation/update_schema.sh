#!/bin/bash

success() {
  echo ===========================================================================
  echo All Operations completed successfully!
  echo ===========================================================================
  exit 0
}

error() {
  echo
  echo ===========================================================================
  echo $1
  echo ===========================================================================
  echo

  exit 1
}

# TODO: check for unzip and java

# get the directory of this script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
pushd "$SCRIPT_DIR" > /dev/null

if [ ! -d venv ]; then
    echo ===========================================================================
    echo Creating Python Virtual Environment
    python3 -m venv venv
    echo ===========================================================================
    # echo a blank line
    echo
fi

source venv/bin/activate
echo ===========================================================================
echo Installing python requirements
python -m pip install wheel pip -U > /dev/null
pip install -r requirements.txt > /tmp/pip-output.txt 2>&1
if [ $? -ne 0 ]; then
    echo Python requirements installation failed!
    cat /tmp/pip-output.txt
    exit 1
fi
rm -f /tmp/pip-output.txt
echo ===========================================================================
echo

echo ===========================================================================
echo Generating schema/queue_message.json from schema/queue_message.ts
# generate queue_message.json schema from queue_message.ts
rm -rf ../schema/elements
python update_schema.py --schema ../schema/queue_message.ts --output ../schema/queue_message.json --output_element_dir ../schema/elements
if [ $? -ne 0 ]; then
    error "JSON schema generation failed!"
fi
echo ===========================================================================
echo

echo ===========================================================================
echo Generating python models
datamodel-codegen --output-model-type pydantic.BaseModel --base-class utf_queue_client.models.base_model.BaseModel --target-python-version 3.8 --enum-field-as-literal all --input ../schema/queue_message.json --input-file-type jsonschema --output ../models/python/generated_models_pydantic_v1.py
datamodel-codegen --output-model-type pydantic_v2.BaseModel --base-class utf_queue_client.models.base_model.BaseModel --target-python-version 3.8 --enum-field-as-literal all --input ../schema/queue_message.json --input-file-type jsonschema --output ../models/python/generated_models_pydantic_v2.py
black ../models/python
if [ $? -ne 0 ]; then
    error "Python model generation failed"
fi
echo ===========================================================================
echo

# C# model generation is currently not working on MacOS/Linux
#echo ===========================================================================
#echo Generating CSharp models
#mono CSharpModelGenerator/CSharpModelGenerator.exe ../schema/queue_message.json ../models/csharp/GeneratedModels.cs
#if [ $? -ne 0 ]; then
#    error "CSharp model generation failed"
#fi
#echo ===========================================================================
#echo

echo ===========================================================================
echo Generating Java models
rm -rf ../models/java

if [ ! -f JavaModelGenerator/jsonschema2pojo-1.1.1/bin/jsonschema2pojo ]; then
    echo Downloading jsonschema2pojo
    mkdir -p JavaModelGenerator
    curl -s -f -k https://artifactory.silabs.net/artifactory/infrasw-generic/utf/tools/jsonschema2pojo-1.1.1.zip -o JavaModelGenerator/jsonschema2pojo.zip
    unzip JavaModelGenerator/jsonschema2pojo.zip -d JavaModelGenerator
    chmod +x JavaModelGenerator/jsonschema2pojo-1.1.1/bin/jsonschema2pojo
    if [ $? -ne 0 ]; then
        error "Unable to download jsonschema2pojo tool"
    fi
    rm -f JavaModelGenerator/jsonschema2pojo.zip
fi

# -a GSON -sl -b
./JavaModelGenerator/jsonschema2pojo-1.1.1/bin/jsonschema2pojo -s ../schema/elements -303 -b -p com.silabs.utf.QueueModels  --target ../models/java
if [ $? -ne 0 ]; then
    error "Java model generation failed"
fi
echo ===========================================================================
# patch models
echo Patching models
python patch_models.py
if [ $? -ne 0 ]; then
    error "Patching models failed"
fi
black ../models/python
echo
success
