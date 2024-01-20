find_package(Gemmi REQUIRED)
add_executable(gemmi_write gemmi_write_struct.cpp)
target_link_libraries(gemmi_write Gemmi::headers)