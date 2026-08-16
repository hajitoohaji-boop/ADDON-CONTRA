@echo off
setlocal EnableExtensions

set "PROJECT_DIR=%~dp0"
set "BUILDER_EXE="

for /f "delims=" %%F in ('where /r "%PROJECT_DIR%.." generalsmodbuilder.exe 2^>nul') do (
    set "BUILDER_EXE=%%F"
    goto :found
)

for /f "delims=" %%F in ('where /r "%USERPROFILE%\Desktop" generalsmodbuilder.exe 2^>nul') do (
    set "BUILDER_EXE=%%F"
    goto :found
)

:found
if not defined BUILDER_EXE (
    echo.
    echo ERROR: generalsmodbuilder.exe was not found.
    echo.
    echo Put the extracted GeneralsModBuilder v2.3 folder beside ADDON-CONTRA,
    echo or place it somewhere under the Desktop, then run this file again.
    echo.
    pause
    exit /b 1
)

echo Using ModBuilder:
echo %BUILDER_EXE%
echo.

echo Building ZZZ_ContraBossAddon.big ...
"%BUILDER_EXE%" --build --verbose-logging --config-list "%PROJECT_DIR%ModBundleItems.json" "%PROJECT_DIR%ModBundlePacks.json"
set "RC=%ERRORLEVEL%"

echo.
if not "%RC%"=="0" (
    echo BUILD FAILED. Error code: %RC%
    echo Keep this window open and send me the complete error text.
    pause
    exit /b %RC%
)

echo BUILD COMPLETED.
echo Check the project output for ZZZ_ContraBossAddon.big.
echo.
pause
exit /b 0
