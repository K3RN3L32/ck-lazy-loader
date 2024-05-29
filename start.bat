@echo off
if "%1" == "elevated" goto start

:: Get the current directory of the batch file
set "batch_dir=%~dp0"

:: Start the batch file with elevated privileges and change directory
powershell -command "Start-Process cmd -ArgumentList '/c cd /d %batch_dir% && %~nx0 elevated' -Verb runas"
goto :EOF

:start
rem Run the Python script
py main.py
exit
