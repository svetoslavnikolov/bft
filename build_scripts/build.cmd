@setlocal
@echo off

set DIR_MINE=%~dp0

IF EXIST "%DIR_MINE%settings.cmd" (
    call "%DIR_MINE%settings.cmd"
)

IF EXIST "%DIR_MINE%settings_local.cmd" (
    call "%DIR_MINE%settings_local.cmd"
)

%CMAKE% --build^
    %DIR_BUILD%^
    --clean-first^
    --config Release^
    --target INSTALL
@endlocal
