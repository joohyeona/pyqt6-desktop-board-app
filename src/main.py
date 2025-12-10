import sys
from pathlib import Path

from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QMessageBox

from pages import ListPage, CreatePage, DetailPage
from db.db_manager import DBManager

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("DDE Desktop Board")
        self.setMinimumSize(800, 600)

        # DB 연결
        base_dir = Path(__file__).resolve().parent
        db_path = base_dir / "board.sqlite3"
        self.db = DBManager(db_path)


        # QStackedWidget으로 페이지 전환
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # 페이지 인덱스
        self.PAGE_INDEX_LIST = 0
        self.PAGE_INDEX_CREATE = 1
        self.PAGE_INDEX_DETAIL = 2

        # 페이지 인스턴스
        self.list_page = ListPage()
        self.create_page = CreatePage()
        self.detail_page = DetailPage()

        # signal-slot 연결 =====================================================
        self.list_page.request_create.connect(self.show_create_page)    # list page -> create btn
        self.list_page.request_detail.connect(self.show_detail_page)    # list page -> 행 클릭 -> detail

        self.create_page.finished.connect(self.handle_cancel_btn)       # create page -> 취소 btn
        self.create_page.saved.connect(self.handle_post_saved)          # create page -> 저장 btn -> list

        self.detail_page.back_to_list.connect(self.show_list_page)      # detail page -> 목록으로 btn -> list
        self.detail_page.request_update.connect(self.show_create_page)  # detail page -> 수정 -> create(id)
        self.detail_page.deleted.connect(self.handle_post_deleted)      # detail page -> 삭제

        # QStackedWidget에 페이지 등록
        self.stacked_widget.addWidget(self.list_page)   # index 0
        self.stacked_widget.addWidget(self.create_page) # index 1
        self.stacked_widget.addWidget(self.detail_page) # 2

        # 첫 페이지
        self.show_list_page()


    def show_list_page(self):
        # 게시글 목록 페이지
        posts = self.db.get_list()
        self.list_page.load_posts(posts)
        self.stacked_widget.setCurrentIndex(self.PAGE_INDEX_LIST)

    def show_create_page(self, post_id: int | None = None):
        if post_id:
            # 수정 모드
            post = self.db.get_post(post_id)
            if not post:
                QMessageBox.warning(self, "Error", "수정 정보를 찾을 수 없습니다.")
                return
            self.create_page.set_detail(post)
        else:
            # 신규 게시글 작성
            self.create_page.set_new()
        self.stacked_widget.setCurrentIndex(self.PAGE_INDEX_CREATE)

    def show_detail_page(self, post_id: int):
        post = self.db.get_post(post_id)
        self.detail_page.set_detail(post)
        self.stacked_widget.setCurrentIndex(self.PAGE_INDEX_DETAIL)

    def handle_post_saved(self, data: dict):
        # 수정 mode
        if "id" in data:
            self.db.update_post(
                data["id"],
                data["title"],
                data["author"],
                data["content"]
            )
            QMessageBox.information(self, "저장 완료", "게시글이 수정되었습니다.")
            post_id = data["id"]

        else:
            # 신규 게시글 등록
            post_id = self.db.create_post(
                data["title"],
                data["author"],
                data["content"],
            )
            QMessageBox.information(self, "저장 완료", "게시글이 등록되었습니다.")

        self.show_detail_page(post_id)

    def handle_post_deleted(self, post_id: int):
        self.db.delete_post(post_id)
        QMessageBox.information(self, "삭제 완료", "게시글이 삭제되었습니다.")
        self.show_list_page()

    def handle_cancel_btn(self):
        if self.create_page._post_id is not None:
            self.show_detail_page(self.create_page._post_id) # 수정 취소 -> 상세 페이지
        else:
            self.show_list_page() # 신규 작성 취소 -> 목록


    def closeEvent(self, event):
        # 창 닫힐 때 DB Manager close
        if hasattr(self, "db"):
            self.db.close()

        super().closeEvent(event)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()