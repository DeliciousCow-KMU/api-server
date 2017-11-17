#!/bin/sh

curl --request POST \
  --url https://1zi1pnd5vb.execute-api.ap-northeast-2.amazonaws.com/dev/auth \
  --header 'content-type: application/json' \
  --data '{
	"user_id": "user_id",
	"passwd": "password"
}'