@echo off
set PYTHON_SCRIPT=text_processor_final.py
set APP_NAME=TextFormatterPro

pyinstaller --noconsole ^
            --onefile ^
            --name "%APP_NAME%" ^
            %PYTHON_SCRIPT%