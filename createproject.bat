@echo off

set /p name="Enter project name: " %=%

python "%~dp0createproject.py" "%name%"

for %%x in (%cmdcmdline%) do if /i "%%~x"=="/c" set DOUBLECLICKED=1
if defined DOUBLECLICKED pause