
      cmake_minimum_required(VERSION 3.27.7)
      project(link_flags C)

      include_directories(/Users/blowekamp/src/SimpleITKPythonPackage/_skbuild/macosx-12.0-arm64-3.8/cmake-build/sitk-sb/CMakeTmp/link_flags/gnu_ld_ignore/MODULE/SHARED/src)

      add_library(number SHARED number.c)
      add_library(counter MODULE counter.c)
    
        set_target_properties(counter PROPERTIES PREFIX "")
      
        set_target_properties(counter PROPERTIES LINK_FLAGS "-Wl,--unresolved-symbols=ignore-all")
      
      add_executable(main main.c)
    
        target_link_libraries(main number)
      
        target_link_libraries(main "")
      