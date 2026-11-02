cmake_minimum_required(VERSION 2.8)
PROJECT(iit-walkman-ros-pkg)




add_custom_target(  acm
                    COMMAND ${CMAKE_SOURCE_DIR}/walkman_urdf/script/create_acm.sh walkman)

add_custom_target(	remove_old_walkman_urdf_gazebo ALL
    				COMMAND ${CMAKE_COMMAND} -E remove_directory 
        			"~/.gazebo/models/walkman_urdf/")

add_custom_target(  remove_old_walkman_gazebo ALL
                    COMMAND ${CMAKE_COMMAND} -E remove_directory 
                    "~/.gazebo/models/walkman/")

add_custom_target(  compile_urdf_sdf ALL
                    COMMAND ${CMAKE_SOURCE_DIR}/walkman_urdf/script/create_urdf_srdf_sdf.sh walkman)

if(CMAKE_INSTALL_PREFIX_INITIALIZED_TO_DEFAULT)
    add_custom_target(	copy_walkman_gazebo ALL
        				COMMAND ${CMAKE_COMMAND} -E copy_directory 
            			"${PROJECT_SOURCE_DIR}/walkman_gazebo/sdf/" 
            			"~/.gazebo/models/walkman/"
            			DEPENDS remove_old_walkman_gazebo)
endif()

# install urdf and srdf folders in the correct path
install(DIRECTORY walkman_urdf/urdf/ DESTINATION "${CMAKE_INSTALL_PREFIX}/share/robots/walkman/urdf") #FILES_MATCHING PATTERN "*.urdf / .srdf"
install(DIRECTORY walkman_srdf/srdf/ DESTINATION "${CMAKE_INSTALL_PREFIX}/share/robots/walkman/srdf") #FILES_MATCHING PATTERN "*.urdf / .srdf"
