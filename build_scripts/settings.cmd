@pushd %~dp0..
@set DIR_BUILD="%CD%\build"
@set DIR_SRC="%CD%\src"
@set DIR_INSTALL="%CD%\distribution"

@set CMAKE=cmake
@set CMAKE_GENERATOR="Visual Studio 16 2019"
@set CMAKE_ARCHITECTURE="x64"

@popd