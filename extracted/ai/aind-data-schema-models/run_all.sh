for file in src/aind_data_schema_models/_generators/templates/*.txt; do
    # Extract the filename without the directory and extension
    type_name=$(basename "$file" .txt)

    # If harp_type, run the update script
    if [ "$type_name" == "harp_types" ]; then
        python src/aind_data_schema_models/_generators/update_harp_types.py
    fi
    
    # Call the Python script with the --type parameter
    python src/aind_data_schema_models/_generators/generator.py --type "$type_name"
done