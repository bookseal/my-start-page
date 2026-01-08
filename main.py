"""
My Start Page - FastAPI Backend
CRUD API for link management
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

# Configuration
LINKS_FILE = Path("links.json")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "1234")


class LinkCreate(BaseModel):
    """Link creation request model"""
    section_id: str
    name: str
    url: str


class LinkDelete(BaseModel):
    """Link deletion request model"""
    section_id: str
    link_id: str


def load_links() -> dict:
    """Load link data from links.json file"""
    if not LINKS_FILE.exists():
        return {"sections": []}
    with open(LINKS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_links(data: dict) -> None:
    """Save link data to links.json file"""
    with open(LINKS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def verify_password(password: Optional[str]) -> bool:
    """Verify admin password"""
    return password == ADMIN_PASSWORD


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Render main page"""
    data = load_links()
    return templates.TemplateResponse("index.html", {
        "request": request,
        "title": "My Start Page",
        "sections": data.get("sections", [])
    })


@app.get("/api/links")
async def get_links():
    """Get all link data"""
    return load_links()


@app.post("/api/links")
async def add_link(link: LinkCreate, x_password: Optional[str] = Header(None)):
    """Add new link (password required)"""
    if not verify_password(x_password):
        raise HTTPException(status_code=401, detail="Invalid password")
    
    data = load_links()
    
    # Find the section
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
        raise HTTPException(status_code=404, detail="Section not found")
    
    save_links(data)
    return {"success": True, "link": new_link}


@app.delete("/api/links/{section_id}/{link_id}")
async def delete_link(
    section_id: str, 
    link_id: str, 
    x_password: Optional[str] = Header(None)
):
    """Delete link (password required)"""
    if not verify_password(x_password):
        raise HTTPException(status_code=401, detail="Invalid password")
    
    data = load_links()
    
    # Find and delete link from section
    for section in data["sections"]:
        if section["id"] == section_id:
            original_length = len(section["links"])
            section["links"] = [l for l in section["links"] if l["id"] != link_id]
            if len(section["links"]) < original_length:
                save_links(data)
                return {"success": True}
            raise HTTPException(status_code=404, detail="Link not found")
    
    raise HTTPException(status_code=404, detail="Section not found")


@app.post("/api/sections")
async def add_section(
    request: Request,
    x_password: Optional[str] = Header(None)
):
    """Add new section (password required)"""
    if not verify_password(x_password):
        raise HTTPException(status_code=401, detail="Invalid password")
    
    body = await request.json()
    title = body.get("title", "")
    color = body.get("color", "blue")
    
    if not title:
        raise HTTPException(status_code=400, detail="Section title is required")
    
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
    """Delete section (password required)"""
    if not verify_password(x_password):
        raise HTTPException(status_code=401, detail="Invalid password")
    
    data = load_links()
    original_length = len(data["sections"])
    data["sections"] = [s for s in data["sections"] if s["id"] != section_id]
    
    if len(data["sections"]) < original_length:
        save_links(data)
        return {"success": True}
    
    raise HTTPException(status_code=404, detail="Section not found")


@app.post("/api/links/{section_id}/{link_id}/move")
async def move_link(
    section_id: str,
    link_id: str,
    request: Request,
    x_password: Optional[str] = Header(None)
):
    """Move link up or down (password required)"""
    if not verify_password(x_password):
        raise HTTPException(status_code=401, detail="Invalid password")
    
    body = await request.json()
    direction = body.get("direction", "")  # "up" or "down"
    
    if direction not in ["up", "down"]:
        raise HTTPException(status_code=400, detail="Invalid direction")
    
    data = load_links()
    
    for section in data["sections"]:
        if section["id"] == section_id:
            links = section["links"]
            # Find link index
            idx = next((i for i, l in enumerate(links) if l["id"] == link_id), None)
            if idx is None:
                raise HTTPException(status_code=404, detail="Link not found")
            
            # Move link
            if direction == "up" and idx > 0:
                links[idx], links[idx - 1] = links[idx - 1], links[idx]
            elif direction == "down" and idx < len(links) - 1:
                links[idx], links[idx + 1] = links[idx + 1], links[idx]
            
            save_links(data)
            return {"success": True}
    
    raise HTTPException(status_code=404, detail="Section not found")
