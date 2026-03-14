# ✨ My Start Page

<div align="center">

![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)

**개인 맞춤형 브라우저 시작 페이지** 🚀

*빠른 접근, 깔끔한 시작*

</div>

---

## 🎨 Features

| Feature | Description |
|---------|-------------|
| 🔗 **링크 관리** | 섹션별 북마크 추가/삭제/정렬 |
| 🎨 **Glassmorphism UI** | 모던하고 세련된 디자인 |
| 🔍 **통합 검색** | Naver, YouTube 바로 검색 |
| 🎨 **테마 컬러** | 섹션별 6가지 네온 컬러 |
| 🔐 **심플 인증** | 비밀번호 기반 관리자 기능 |
| 📱 **반응형** | 모바일/태블릿/데스크톱 지원 |

## 🖼️ Preview

```
┌─────────────────────────────────────────────────────┐
│           ✨ My Start Page ✨                       │
│                                                     │
│  ┌──────────────┐  ┌──────────────┐                │
│  │ 🔍 Naver     │  │ ▶️ YouTube   │                │
│  │ [Search...] │  │ [Search...] │                │
│  └──────────────┘  └──────────────┘                │
│                                                     │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐            │
│  │ Dev 🔵  │  │ Cloud ☁️│  │ Tools🔧│            │
│  │ • GitHub │  │ • AWS   │  │ • Notion│            │
│  │ • GitLab │  │ • GCP   │  │ • Slack │            │
│  │ • ...    │  │ • ...   │  │ • ...   │            │
│  └─────────┘  └─────────┘  └─────────┘            │
└─────────────────────────────────────────────────────┘
```

## 🚀 Quick Start

### 로컬 실행

```bash
# 저장소 클론
git clone https://github.com/yourusername/my-start-page.git
cd my-start-page

# 가상환경 생성 및 활성화
python3 -m venv venv
source venv/bin/activate

# 의존성 설치
pip install -r requirements.txt

# 서버 실행
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Docker 실행

```bash
# 빌드 & 실행
docker build -t my-start-page .
docker run -d -p 8000:8000 -e ADMIN_PASSWORD=yourpassword my-start-page
```

## ⚙️ Configuration

| 환경변수 | 설명 | 기본값 |
|----------|------|--------|
| `ADMIN_PASSWORD` | 관리자 비밀번호 | `1234` |
| `LINKS_FILE` | 링크 데이터 파일 경로 | `links.json` |

## 📁 Project Structure

```
my-start-page/
├── main.py              # FastAPI 백엔드
├── requirements.txt     # Python 의존성
├── Dockerfile           # Docker 이미지 설정
├── links.json           # 링크 데이터
├── data/
│   └── links.json       # 영구 데이터 저장
└── templates/
    └── index.html       # 프론트엔드 (Jinja2 + Tailwind)
```

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | 메인 페이지 렌더링 |
| `GET` | `/api/links` | 모든 링크 조회 |
| `POST` | `/api/links` | 링크 추가 🔐 |
| `DELETE` | `/api/links/{section_id}/{link_id}` | 링크 삭제 🔐 |
| `POST` | `/api/links/{section_id}/{link_id}/move` | 링크 순서 변경 🔐 |
| `POST` | `/api/sections` | 섹션 추가 🔐 |
| `DELETE` | `/api/sections/{section_id}` | 섹션 삭제 🔐 |

> 🔐 = 비밀번호 필요 (`X-Password` 헤더)

## 🎨 Theme Colors

```
🔵 Blue    #00d4ff    🟣 Purple  #b94dff
🟢 Green   #00ff9d    🔴 Red     #ff4d6d
🟡 Yellow  #ffd700    🟠 Orange  #ff8c00
```

## 🛠️ Tech Stack

- **Backend**: FastAPI + Uvicorn
- **Frontend**: Jinja2 + Tailwind CSS
- **Storage**: JSON file (no database required)
- **Deploy**: Docker ready

---

<div align="center">

Made with 💜 by [bit-habit.com](https://bit-habit.com)

</div>
