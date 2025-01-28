# test.py
import MySQLdb
import os

from sql.mysql import execute_query

# 사용자로부터 입력받는 함수
def get_mokkoji_info():
    mokkoji_uuid = input("mokkoji_uuid를 입력하세요: ")
    mokkoji_name = input("mokkoji_name을 입력하세요: ")
    mokkoji_des = input("mokkoji_des를 입력하세요: ")
    reg_id = input("reg_id를 입력하세요: ")
    chg_id = input("chg_id를 입력하세요: ")
    use_yn = input("use_yn을 입력하세요 (1/0): ")
    
    return (mokkoji_uuid, mokkoji_name, mokkoji_des, reg_id, chg_id, use_yn)


# 실행할 SQL 쿼리
def get_query_from_file(file_path, query_tag):
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()
    
    # 태그를 기준으로 분리
    queries = content.split('-- Query: ')
    
    # 각 쿼리를 검사
    for query in queries:
        if query_tag in query:
            # 태그를 제외한 쿼리만 반환
            return query.split('\n', 1)[1].strip()
    
    raise ValueError(f"Tag '{query_tag}'에 해당하는 쿼리를 찾을 수 없습니다.")


# SQL 파일 경로
current_dir = os.path.dirname(os.path.abspath(__file__))
query_file = os.path.join(current_dir, "sql", "query.sql")  # sql 폴더에 있는 queries.sql

# 실행할 쿼리 태그
#query_tag = "select mokkoji_info & mokkoji_user"  # 여기에서 태그를 변경해서 다른 쿼리 실행 가능
query_tag = "insert mokkoji_info"  # 여기에서 태그를 변경해서 다른 쿼리 실행 가능
# 파일에서 쿼리 가져오기
try:
    sql_query = get_query_from_file(query_file, query_tag)
except ValueError as e:
    print(f"쿼리 로드 에러: {e}")
    exit()

result = None

# 사용자 입력 받기
data = get_mokkoji_info()

# 직접 데이터 삽입
"""
data = (
    '1',
    'admin',
    'admin',
    'admin123@',
    'admin',
    '',
    '1'
)
"""
# 쿼리 실행 (컬럼명과 결과 반환)
try:
    if sql_query.strip().lower().startswith("select"):
        # SELECT 쿼리는 데이터를 전달하지 않음
        result = execute_query(sql_query)
    else:
        # INSERT/UPDATE/DELETE 쿼리는 데이터를 전달
        result = execute_query(sql_query, data)
        
    if isinstance(result, tuple):  # SELECT 쿼리
        columns, rows = result
    else:  # INSERT/UPDATE/DELETE 쿼리
        print(f"쿼리 실행 성공! 영향을 받은 행의 수: {result}")
except MySQLdb.Error as e:
    print(f"MySQL 실행 에러: {e}")
except Exception as e:
    print(f"일반 에러: {e}")    

# 결과 출력
if isinstance(result, tuple):  # SELECT 쿼리인 경우
    columns, rows = result
    print("\n결과:")
    for row in rows:
        print(row)
        print(row[columns.index('mokkoji_name')])
else:  # INSERT/UPDATE/DELETE 쿼리인 경우
    print(f"쿼리 실행 성공! 영향을 받은 행의 수: {result}")