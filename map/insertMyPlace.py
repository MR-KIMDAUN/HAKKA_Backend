import MySQLdb
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from sql.mysql import execute_query
from map.myPlace import scrape_my_place
from uuidSetting import create_uuid

router = APIRouter()

class InsertMyPlaceRequest(BaseModel):
    url: str

# SQL 파일 로드 함수
def get_query_from_file(file_path, query_tag):
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()
    
    queries = content.split('-- Query: ')
    
    for query in queries:
        if query_tag in query:
            return query.split('\n', 1)[1].strip()
    
    raise ValueError(f"Tag '{query_tag}'에 해당하는 쿼리를 찾을 수 없습니다.")

# SQL 파일 경로 설정
current_dir = os.path.dirname(os.path.abspath(__file__))  # 현재 파일 경로
backend_dir = os.path.dirname(current_dir)  # HAKKA_Backend 폴더로 이동
query_file = os.path.join(backend_dir, "sql", "query.sql")  # sql 폴더 지정

@router.post("/insert_my_place")
def insert_my_place(request: InsertMyPlaceRequest):
    
    data = scrape_my_place(request.url)
    
    if not data:
        raise HTTPException(status_code=400, detail="데이터 추출 실패 또는 데이터 없음!")

    # SQL 쿼리 가져오기
    query_tag = "insert Place_info"
    
    try:
        sql_query = get_query_from_file(query_file, query_tag)
    except ValueError as e:
        raise HTTPException(status_code=500, detail=f"쿼리 로드 에러: {e}")

    # 데이터 저장
    inserted_places = []
    
    for place in data:
        new_uuid = create_uuid()
        
        inserted_places.append((
            new_uuid,
            '1',
            '1',
            place['title'],
            place['address'],
            '테스트설명',
            place['image'],  
            "1",  
            "admin",  
            "admin",  
            request.url
        ))

    try:
        result = execute_query(sql_query, inserted_places, multiple=True)
        return {"message": "데이터 저장 완료", "rows_inserted": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DB 저장 실패: {e}")
