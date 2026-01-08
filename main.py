"""
My Start Page - FastAPI 백엔드
링크 관리를 위한 CRUD API 제공
"""
import json
import os
import uuid
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, Request, HTTPException, Header
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel


app = FastAPI()
templates = Jinja2Templates(directory="templates")

# 설정
LINKS_FILE = Path("links.json")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "1234")  # 기본값, 운영시 환경변수로 변경


class LinkCreate(BaseModel):
    """링크 생성 요청 모델"""
    section_id: str
    name: str
    url: str


class LinkDelete(BaseModel):
    """링크 삭제 요청 모델"""
    section_id: str
    link_id: str


def load_links() -> dict:
    """links.json 파일에서 링크 데이터 로드"""
    if not LINKS_FILE.exists():
        return {"sections": []}
    with open(LINKS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_links(data: dict) -> None:
    """링크 데이터를 links.json 파일에 저장"""
    with open(LINKS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def verify_password(password: Optional[str]) -> bool:
    """비밀번호 검증"""
    return password == ADMIN_PASSWORD


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """메인 페이지 렌더링"""
    data = load_links()
    return templates.TemplateResponse("index.html", {
        "request": request,
        "title": "My Start Page",
        "sections": data.get("sections", [])
    })


@app.get("/api/links")
async def get_links():
    """전체 링크 데이터 조회"""
    return load_links()


@app.post("/api/links")
async def add_link(link: LinkCreate, x_password: Optional[str] = Header(None)):
    """새 링크 추가 (비밀번호 필요)"""
    if not verify_password(x_password):
        raise HTTPException(status_code=401, detail="비밀번호가 올바르지 않습니다")
    
    data = load_links()
    
    # 해당 섹션 찾기
    section_found = False
    for section in data["sections"]:
        if section["id"] == link.section_id:
            new_link = {
                "id": str(uuid.uuid4())[:8],
                "name": link.name,
                "url": link.url
            }
            section["links"].append(new_link)
            section_found = True
            break
    
    if not section_found:
        raise HTTPException(status_code=404, detail="섹션을 찾을 수 없습니다")
    
    save_links(data)
    return {"success": True, "link": new_link}


@app.delete("/api/links/{section_id}/{link_id}")
async def delete_link(
    section_id: str, 
    link_id: str, 
    x_password: Optional[str] = Header(None)
):
    """링크 삭제 (비밀번호 필요)"""
    if not verify_password(x_password):
        raise HTTPException(status_code=401, detail="비밀번호가 올바르지 않습니다")
    
    data = load_links()
    
    # 해당 섹션에서 링크 찾아서 삭제
    for section in data["sections"]:
        if section["id"] == section_id:
            original_length = len(section["links"])
            section["links"] = [l for l in section["links"] if l["id"] != link_id]
            if len(section["links"]) < original_length:
                save_links(data)
                return {"success": True}
            raise HTTPException(status_code=404, detail="링크를 찾을 수 없습니다")
    
    raise HTTPException(status_code=404, detail="섹션을 찾을 수 없습니다")


@app.post("/api/sections")
async def add_section(
    request: Request,
    x_password: Optional[str] = Header(None)
):
    """새 섹션 추가 (비밀번호 필요)"""
    if not verify_password(x_password):
        raise HTTPException(status_code=401, detail="비밀번호가 올바르지 않습니다")
    
    body = await request.json()
    title = body.get("title", "")
    color = body.get("color", "blue")
    
    if not title:
        raise HTTPException(status_code=400, detail="섹션 제목이 필요합니다")
    
    data = load_links()
    new_section = {
        "id": str(uuid.uuid4())[:8],
        "title": title,
        "color": color,
        "links": []
    }
    data["sections"].append(new_section)
    save_links(data)
    
    return {"success": True, "section": new_section}


@app.delete("/api/sections/{section_id}")
async def delete_section(section_id: str, x_password: Optional[str] = Header(None)):
    """섹션 삭제 (비밀번호 필요)"""
    if not verify_password(x_password):
        raise HTTPException(status_code=401, detail="비밀번호가 올바르지 않습니다")
    
    data = load_links()
    original_length = len(data["sections"])
    data["sections"] = [s for s in data["sections"] if s["id"] != section_id]
    
    if len(data["sections"]) < original_length:
        save_links(data)
        return {"success": True}
    
    raise HTTPException(status_code=404, detail="섹션을 찾을 수 없습니다")
