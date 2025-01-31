# mysql.py
import pymysql
from dotenv import load_dotenv
import os

load_dotenv()

def execute_query(query, params=None):
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
        if params:
            cursor.execute(query, params)  # 파라미터 바인딩
        else:
            cursor.execute(query)
            
        if query.strip().lower().startswith("select"):
            # SELECT 쿼리의 경우
            columns = [desc[0] for desc in cursor.description]
            result = cursor.fetchall()
            return columns, result
        else:
            # INSERT/UPDATE/DELETE 쿼리의 경우
            conn.commit()  # 트랜잭션 커밋
            return cursor.rowcount  # 영향을 받은 행의 수 반환
    except pymysql.Error as e:
        # MySQL 관련 에러 처리
        print(f"MySQL 에러 발생: {e}")
        raise  # 에러를 다시 호출자에게 전달
    except Exception as e:
        # 일반 에러 처리
        print(f"알 수 없는 에러 발생: {e}")
        raise
    finally:
        cursor.close()
        conn.close()
