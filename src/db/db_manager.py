import sqlite3
from pathlib import Path
from typing import List, Optional

class DBManager:
    def __init__(self, db_path: Path):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row # row로 호출되게
        self._create_tables()

    def _create_tables(self) -> None:
        # 테이블 없으면 생성
        cursor = self.conn.cursor()
        cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title VARCHAR(100) NOT NULL,
                author VARCHAR(20) NOT NULL,
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT NULL,
                deleted_at TIMESTAMP DEFAULT NULL,
                is_deleted BOOLEAN DEFAULT 0
            )
            '''
        )
        self.conn.commit()

    def get_post(self, post_id: int) -> Optional[sqlite3.Row]:
        # 상세 페이지 get
        cursor = self.conn.cursor()
        cursor.execute(
            """
            SELECT * FROM posts
            WHERE id = ?
            """,
            (post_id,),
        )
        row = cursor.fetchone()
        return row

    def get_list(self) -> list[sqlite3.Row]:
        cursor = self.conn.cursor()
        # TODO: 목록에 보여줄 것만 가져오기
        cursor.execute(
            """
            SELECT * FROM posts
            ORDER BY created_at DESC
            """
        )
        rows = cursor.fetchall()
        return rows

    def update_post(self, post_id: int, title: str, author: str, content: str) -> None:
        cursor = self.conn.cursor()
        cursor.execute(
            """
            UPDATE posts
            SET title = ?, author = ?, content = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """,
            (title, author, content,post_id),
        )
        self.conn.commit()

    def delete_post(self, post_id: int):
        # soft delete
        cursor = self.conn.cursor()
        cursor.execute(
            "UPDATE posts SET is_deleted = 1, deleted_at = CURRENT_TIMESTAMP WHERE id = ?",
            (post_id,)
        )
        self.conn.commit()

    def close(self) -> None:
        # 앱 종료 시 connect close
        if self.conn:
            self.conn.close()