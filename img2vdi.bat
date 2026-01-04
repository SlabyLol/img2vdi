@echo off
setlocal

REM Prüfen ob Parameter übergeben wurde
if "%~1"=="" (
    echo Nutzung: img2vdi.bat datei.img
    pause
    exit /b
)

REM Dateinamen setzen
set INPUT=%~1
set OUTPUT=%~dpn1.vdi

REM VirtualBox Pfad (anpassen falls nötig)
set VBOX="C:\Program Files\Oracle\VirtualBox\VBoxManage.exe"

REM Prüfen ob VBoxManage existiert
if not exist %VBOX% (
    echo Fehler: VBoxManage nicht gefunden!
    pause
    exit /b
)

echo Konvertiere:
echo %INPUT%  -->  %OUTPUT%
echo.

%VBOX% convertfromraw "%INPUT%" "%OUTPUT%" --format VDI

if %ERRORLEVEL%==0 (
    echo.
    echo Fertig! VDI erstellt.
) else (
    echo.
    echo Fehler bei der Konvertierung!
)

pause
