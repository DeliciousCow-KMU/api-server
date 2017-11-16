#!/bin/bash

LAMBDA_NAME=$1

cd ${LAMBDA_NAME}
rm ${LAMBDA_NAME}.zip

mkdir build
cd build

cp ../lambda.py ./lambda.py
pip install -r ../requirements.txt -t .
zip -r ${LAMBDA_NAME}.zip .
cd ..
mv ./build/${LAMBDA_NAME}.zip ./${LAMBDA_NAME}.zip
rm -rf ./build