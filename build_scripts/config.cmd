@setlocal
@echo off
set DIR_MINE=%~dp0

pushd %DIR_MINE%

IF EXIST "%DIR_MINE%settings.cmd" (
    call "%DIR_MINE%settings.cmd"
)


IF EXIST "%DIR_MINE%settings_local.cmd" (
    call "%DIR_MINE%settings_local.cmd"
)


%CMAKE%^
    -G %CMAKE_GENERATOR%^
    -A %CMAKE_ARCHITECTURE%^
    -D CMAKE_INSTALL_PREFIX=%DIR_INSTALL%^
    -B %DIR_BUILD%^
    -S %DIR_SRC%


echo.**************************************************************************
echo.*
echo.*  All parameters from 'settings.cmd' can be overridden in
echo.*  %DIR_MINE%settings_local.cmd
echo.*
echo.*
echo.* CMAKE=%CMAKE%
echo.* CMAKE_GENERATOR=%CMAKE_GENERATOR%
echo.* CMAKE_ARCHITECTURE=%CMAKE_ARCHITECTURE%
echo.* CMAKE_INSTALL_PREFIX=%DIR_INSTALL%
echo.*
echo.**************************************************************************

popd
@echo on
@endlocal