import json
import traceback
import requests
from bs4 import BeautifulSoup


class Response(dict):
    def __init__(self, resp, status=200):
        super().__init__()
        self.update({
            'statusCode': status,
            'body': json.dumps(resp),
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
        })


class KtisSession:
    KTIS_SECURE_URL = "https://ktis.kookmin.ac.kr/"

    def __init__(self, user_id, passwd):
        self.req_session = requests.Session()
        self.req_session.get(self.KTIS_SECURE_URL)
        login_request = self.req_session.post("{0}kmu/com.Login.do?".format(self.KTIS_SECURE_URL),
                                              data={'txt_user_id': user_id, 'txt_passwd': passwd})
        self.account = user_id
        self.is_valid = "frameset" in login_request.text

    def get_info(self):
        if self.is_valid:
            info_request = self.req_session.post("{0}kmu/usa.Usa0215qAGet01.do".format(self.KTIS_SECURE_URL),
                                                 data={'nfkey': None, 'pFolder': "%C7%D0%C0%FB%BD%C3%BD%BA%C5%DB",
                                                       'ServiceID': self.account})
            info_list = []
            for info_item in BeautifulSoup(info_request.text, 'html.parser').select("td.table_bg_white"):
                info_list.append(info_item.string)
            return {
                'user_id': info_list[0].strip(),
                'name': info_list[1].strip(),
                'college': info_list[3].strip(),
                'department': info_list[4].strip()
            }
        else:
            return None


def lambda_handler(event, context):
    try:
        query = json.loads(event["body"])
        query = (query.get("user_id"), query.get("passwd"))
        if query[0] and query[1]:
            session = KtisSession(*query)
            if session.is_valid:
                return Response({'data': session.get_info()})
            else:
                return Response({'err': "Authenticate failed"}, 401)
        else:
            return Response({'err': "Missing field"}, 400)
    except (json.JSONDecodeError, TypeError):
        return Response({'err': "Invalid request format"}, 400)
    except Exception as e:
        print("Unknown Error at lambda_handler: %s" % str(e))
        traceback.print_exc()
        return Response({'err': "unknown"}, 500)
