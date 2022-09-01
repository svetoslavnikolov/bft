cmake_minimum_required(VERSION 2.8)

project(BeamformingToolbox)

set(BeamformingToolbox_VERSION_MAJOR 1)
set(BeamformingToolbox_VERSION_MINOR 5)
set(BeamformingToolbox_VERSION_PATCH 0) 


set(
    BASESRC
    c/beamform.c
    c/focus.c
    c/geometry.c
    c/if_bft.c
    c/motion.c
    c/msgprint.c
    c/transducer.c
    )


set(
    BASEHDR
    h/beamform.h
    h/error.h
    h/focus.h
    h/geometry.h
    h/if_bft.h
    h/motion.h
    h/msgprint.h
    h/sys_params.h
    h/transducer.h
    h/types.h
    )


add_definitions(-Wall -DBFT_DLL -D_CRT_SECURE_NO_WARNINGS)
include_directories(${CMAKE_CURRENT_SOURCE_DIR}/h)

add_library(bft SHARED ${BASESRC} ${BASEHDR})

add_custom_command(TARGET bft POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E echo "This: " ${PYTHON_LIBRARIES}

    COMMAND ${CMAKE_COMMAND} -E copy $<TARGET_FILE:bft> ${CMAKE_CURRENT_SOURCE_DIR}/pybft
    #COMMAND ${CMAKE_COMMAND} -E copy ${CMAKE_CURRENT_BINARY_DIR}/ultrasound.py ${CMAKE_CURRENT_SOURCE_DIR}/python
)
