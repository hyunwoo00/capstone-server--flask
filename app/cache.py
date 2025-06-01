import redis
from dotenv import load_dotenv
from app.db import get_connection
import os
import json

load_dotenv()

host = os.getenv('REDIS_HOST', 'redis')
port = os.getenv('REDIS_PORT', 6379)

# 로컬 Redis 연결
# host = 'redis' 도커 환경 내에서 host는 docker-compose.yml 내에서 정의한 redis의 이름.
# db = 0, 0번 db 사용.
# decode_responses=True // redis에서 가져온 데이터를 문자열로 자동 디코딩
r = redis.Redis(host=host, port=port, db=0, decode_responses=True)

# 초기 캐싱 함수
def init_cache():
    #db 연결
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            #labels 테이블 값 fetching.
            cursor.execute("SET NAMES utf8mb4;")
            cursor.execute("SELECT * FROM yamnet_labels;")
            rows = cursor.fetchall()
            for row in rows:
                #key, value 할당.
                key = f"display_name:{row['display_name']}"
                value = {
                    'display_name_kor': row['display_name_kor'],
                    'label_category': row['label_category']
                }
                print(row['display_name_kor'])
                #redis 저장. ensure_ascii=False를 통해 한국어가 깨지는것을 막음.
                r.set(key, json.dumps(value, ensure_ascii=False))
                print(f"[CACHE] {key} → {value}")
    finally:
        #db 연결해제.
        conn.close()

def get_label_infos(display_name):
    key = f"display_name:{display_name}"
    value = r.get(key)

    if value is None:
        return None
    
    # JSON 문자열을 파이썬 딕셔너리로 변환
    return json.loads(value)      # str → dict