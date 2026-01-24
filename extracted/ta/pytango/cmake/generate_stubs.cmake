install(CODE "
    message(\"Generating .pyi stub files.\")
")

# Temporarily copy _tango extension to source dir
install(CODE "
    file(COPY \"$<TARGET_FILE:pytango_tango>\" DESTINATION \"${CMAKE_CURRENT_SOURCE_DIR}/tango\")
    file(RENAME \"${CMAKE_CURRENT_SOURCE_DIR}/tango/$<TARGET_FILE_NAME:pytango_tango>\" \"${CMAKE_CURRENT_SOURCE_DIR}/tango/$<TARGET_FILE_PREFIX:pytango_tango>$<TARGET_FILE_BASE_NAME:pytango_tango>$<TARGET_FILE_SUFFIX:pytango_tango>\")
")

# Trick to get the PYTHONPATH from isolated environment
install(CODE "
    execute_process(
        COMMAND python -c \"import os; print(os.environ.get('PYTHONPATH', ''))\"
        OUTPUT_VARIABLE ISOLATED_PYTHONPATH
        OUTPUT_STRIP_TRAILING_WHITESPACE
        ECHO_OUTPUT_VARIABLE
    )
")

# Determine system path separator sign
# Convert source path according to platform
if(WIN32)
    set(PATH_SEPARATOR ";")
    install(CODE "string(REPLACE \"/\" \"\\\\\" PYTANGO_SOURCE_DIR \"${CMAKE_CURRENT_SOURCE_DIR}\")")
else()
    set(PATH_SEPARATOR ":")
    install(CODE "set(PYTANGO_SOURCE_DIR \"\${CMAKE_CURRENT_SOURCE_DIR}\")")
endif()

# Generate the .pyi stubs
# Appending tango source code directory to ISOLATED_PYTHONPATH
if(WIN32)
    install(CODE "
        execute_process(
            COMMAND ${CMAKE_COMMAND} -E env \"PYTHONPATH=\${PYTANGO_SOURCE_DIR}${PATH_SEPARATOR}\${ISOLATED_PYTHONPATH}\"
            cmake\\\\gen_stubs.bat
            RESULT_VARIABLE TRY_TO_INSTALL_STUBS
        )
    ")
else()
    install(CODE "
        execute_process(
            COMMAND ${CMAKE_COMMAND} -E env \"PYTHONPATH=\${PYTANGO_SOURCE_DIR}${PATH_SEPARATOR}\${ISOLATED_PYTHONPATH}\"
            cmake/gen_stubs.sh tango --ignore-all-errors --enum-class-locations=DevState|AttrWriteType|LevelLevel|ErrSeverity:tango
            RESULT_VARIABLE TRY_TO_INSTALL_STUBS
        )
    ")
endif()

# Copy generated .pyi stubs
install(CODE "
  if(\${TRY_TO_INSTALL_STUBS} EQUAL 0)
    configure_file(
        \"\${CMAKE_CURRENT_SOURCE_DIR}/stubs/tango/__init__.pyi\"
        \"\${CMAKE_CURRENT_SOURCE_DIR}/tango/__init__.pyi\"
        COPYONLY
    )
    configure_file(
        \"\${CMAKE_CURRENT_SOURCE_DIR}/stubs/tango/_tango/__init__.pyi\"
        \"\${CMAKE_CURRENT_SOURCE_DIR}/tango/_tango.pyi\"
        COPYONLY
    )
    message(STATUS \"Stub files installed into \${CMAKE_CURRENT_SOURCE_DIR}/tango/\")
  else()
    message(WARNING \"Stub generation failed; skipping copy of .pyi files.\")
  endif()
")


# Clean _tango extension from source dir and remove stubs folder
install(CODE "
    file(REMOVE \"${CMAKE_CURRENT_SOURCE_DIR}/tango/$<TARGET_FILE_PREFIX:pytango_tango>$<TARGET_FILE_BASE_NAME:pytango_tango>$<TARGET_FILE_SUFFIX:pytango_tango>\")
    file(REMOVE_RECURSE \"${CMAKE_CURRENT_SOURCE_DIR}/stubs\")
")
