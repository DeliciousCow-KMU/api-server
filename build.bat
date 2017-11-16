@echo off

set LAMBDA_NAME=%1

cd %LAMBDA_NAME%
del %LAMBDA_NAME%.zip

mkdir build
cd build

copy ..\lambda.py lambda.py
pip install -r ..\requirements.txt -t .
bandizip c %LAMBDA_NAME%.zip .
cd ..
move build\%LAMBDA_NAME%.zip %LAMBDA_NAME%.zip
rd /s/q build