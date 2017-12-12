import json
import os
import traceback

import pymysql
import pymysql.cursors


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


def lambda_handler(event, context):
    try:
        query = json.loads(event["body"])
        db_conn = pymysql.connect(host=os.environ['DB_HOST'],
                                  user=os.environ['DB_USER'],
                                  password=os.environ['DB_PASSWD'],
                                  db=os.environ['CRAWL_DB_NAME'],
                                  charset='utf8',
                                  cursorclass=pymysql.cursors.DictCursor)

        if query.get("api_id") == 1:
            print("[API] getNotice")
            if not query.get("department"):
                return Response({'err': "Missing field"}, 400)
            with db_conn.cursor() as db_cur:
                sql_query = "SELECT `title`, `url` FROM `post` WHERE `department`=%s"
                db_cur.execute(sql_query, (query["department"],))

                articles = []
                for elem in db_cur.fetchall():
                    articles.append({
                        "title": elem['title'],
                        "url": elem["url"]
                    })

            return Response({'data': articles}, 200)

        return Response({'err': "api not found"}, 404)

    except (json.JSONDecodeError, TypeError):
        print("[Invalid format]")
        return Response({'err': "Invalid request format"}, 400)
    except Exception as e:
        print("Unknown Error at lambda_handler: %s" % str(e))
        traceback.print_exc()
        return Response({'err': "unknown"}, 500)
