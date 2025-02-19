# mysql.py
import pymysql
from dotenv import load_dotenv
import os

env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(env_path)
load_dotenv()

def execute_query(query, params=None, multiple=False):
    # MySQL 서버 연결
    # 환경 변수 사용
    db_host = os.getenv('DB_HOST')
    db_user = os.getenv('DB_USER')
    db_pass = os.getenv('DB_PASS')
    db_name = os.getenv('DB_NAME')

    conn = pymysql.connect(
        host=db_host,
        user=db_user,
        passwd=db_pass,
        db=db_name
    )
    try:
        cursor = conn.cursor()
        
        if multiple:
            cursor.executemany(query, params)  # 여러 개의 데이터 한 번에 삽입
        else:
            cursor.execute(query, params)

        if query.strip().lower().startswith("select"):
            columns = [desc[0] for desc in cursor.description]  # 컬럼명 가져오기
            rows = cursor.fetchall()  # 데이터 가져오기
            print(f" SELECT 실행 결과: {rows}")  # 결과 확인
            return columns, rows  # 튜플 반환 (columns, rows)

        else:
            conn.commit()
            return cursor.rowcount
    finally:
        cursor.close()
        conn.close()
        