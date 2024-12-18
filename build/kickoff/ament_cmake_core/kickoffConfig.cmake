# generated from ament/cmake/core/templates/nameConfig.cmake.in

# prevent multiple inclusion
if(_kickoff_CONFIG_INCLUDED)
  # ensure to keep the found flag the same
  if(NOT DEFINED kickoff_FOUND)
    # explicitly set it to FALSE, otherwise CMake will set it to TRUE
    set(kickoff_FOUND FALSE)
  elseif(NOT kickoff_FOUND)
    # use separate condition to avoid uninitialized variable warning
    set(kickoff_FOUND FALSE)
  endif()
  return()
endif()
set(_kickoff_CONFIG_INCLUDED TRUE)

# output package information
if(NOT kickoff_FIND_QUIETLY)
  message(STATUS "Found kickoff: 0.0.0 (${kickoff_DIR})")
endif()

# warn when using a deprecated package
if(NOT "" STREQUAL "")
  set(_msg "Package 'kickoff' is deprecated")
  # append custom deprecation text if available
  if(NOT "" STREQUAL "TRUE")
    set(_msg "${_msg} ()")
  endif()
  # optionally quiet the deprecation message
  if(NOT kickoff_DEPRECATED_QUIET)
    message(DEPRECATION "${_msg}")
  endif()
endif()

# flag package as ament-based to distinguish it after being find_package()-ed
set(kickoff_FOUND_AMENT_PACKAGE TRUE)

# include all config extra files
set(_extras "")
foreach(_extra ${_extras})
  include("${kickoff_DIR}/${_extra}")
endforeach()
