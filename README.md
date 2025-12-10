# PyQT6 기반의 Desktop 게시판 프로그램

PyQt6와 SQLite를 사용하여 구현한 데스크탑 기반의 게시판 프로그램입니다.  
CRUD 기능을 제공하며, 각 화면은 QStackedWidget으로 라우팅되고 Signal-Slot 패턴을 통해 페이지 간 이벤트를 처리합니다.  

---

## Features

- 게시글 CRUD(Create/Read/Update/Delete) 기능 제공
- SQLite Local Database 사용
- QStackedWidget 기반 페이지 전환
-  Signal-Slot 방식으로 페이지 간 이벤트 처리
- 입력 폼 변경 감지 후 취소 시 Confirm Dialog 출력

---

## Installation & Run
### 1. git clone 및 프로젝트 폴더로 이동
```bash
git clone https://github.com/joohyeona/pyqt6-desktop-board-app.git
cd <project folder>
```

### 2. venv(가상환경) 실행
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate
```

### 3. root 경로에서 requirements 설치
```pip install -r requirements.txt```

### 4. root경로에서 main.py 실행
```bash
python src/main.py
```

---

## Project Structure

```shell
root/
├─ src/
│  ├─ pages/
│  │  ├─ create_page.py  # 게시글 작성/수정 화면
│  │  ├─ detail_page.py  # 게시글 상세 페이지
│  │  └─ list_page.py    # 게시글 목록 페이지
│  │
│  ├─ db/
│  │  └─ db_manager.py   # SQLite 연결 및 CRUD 기능 제공
│  │ 
│  ├─ board.sqlite3      # Local DB 파일
│  └─ main.py            # Application Entry Point
│
├─ README.md
└─ requirements.txt
```

---

### TODO

- 게시글 검색 기능(제목/내용/작성자 기준)
- Pagination 또는 Infinite Scroll 적용
- UI Style 개선 (QSS 적용, 테마 변경 등)