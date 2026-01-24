datamodel-codegen --input ../src/ogmios/model/cardano.json --input-file-type jsonschema --output-model-type pydantic.BaseModel --output ../src/ogmios/model/cardano_model.py
datamodel-codegen --input ../src/ogmios/model/ogmios.json --input-file-type jsonschema --output-model-type pydantic.BaseModel --output ../src/ogmios/model/ogmios_model.py
