from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import os
from HAKKA_Backend.sql.mysql import execute_query  # 기존 SQL 실행 함수 사용
from fastapi.middleware.cors import CORSMiddleware
from HAKKA_Backend.map import insertMyPlace
from map.selectMyPlace import router as select_my_place_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React 프론트엔드 주소만 허용 (배포 시 변경 가능)
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메서드 허용 (GET, POST, PUT, DELETE 등)
    allow_headers=["*"],  # 모든 헤더 허용
)

app.include_router(insertMyPlace.router)

app.include_router(select_my_place_router)

@app.get("/")
def root():
    return {"message": "FastAPI 서버 실행 중!"}

# **3️⃣ 기본 API 엔드포인트**
@app.get("/")
def root():
    return {"message": "FastAPI Mokkoji Service Running!"}
