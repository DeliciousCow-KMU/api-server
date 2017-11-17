var request = require("cow-ktisAuth/sample/request/request");

var options = { method: 'POST',
  url: 'https://1zi1pnd5vb.execute-api.ap-northeast-2.amazonaws.com/dev/auth',
  headers: { 'content-type': 'application/json' },
  body: { user_id: 'user_id', passwd: 'password' },
  json: true };

request(options, function (error, response, body) {
  if (error) throw new Error(error);

  console.log(body);
});
