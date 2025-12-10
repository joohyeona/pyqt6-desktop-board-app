import sys
from pathlib import Path

from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QMessageBox

from pages import ListPage, CreatePage
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
        print("db연결됨:", len(self.db.get_list()))

        # QStackedWidget으로 페이지 전환
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # 페이지 인덱스
        self.PAGE_INDEX_LIST = 0
        self.PAGE_INDEX_CREATE = 1

        # 페이지 인스턴스
        self.list_page = ListPage()
        self.create_page = CreatePage()

        # signal-slot 연결 =====================================================
        self.list_page.request_create.connect(self.show_create_page)    # list page -> create btn
        self.create_page.finished.connect(self.show_list_page)          # create page -> 취소 btn -> list
        self.create_page.saved.connect(self.handle_post_saved)          # create page -> 저장 btn -> list

        # QStackedWidget에 페이지 등록
        self.stacked_widget.addWidget(self.list_page)   # index 0
        self.stacked_widget.addWidget(self.create_page) # index 1

        # 첫 페이지
        self.show_list_page()


    def show_list_page(self):
        # 게시글 목록 페이지
        posts = self.db.get_list()
        self.list_page.load_posts(posts)
        self.stacked_widget.setCurrentIndex(self.PAGE_INDEX_LIST)

    def show_create_page(self):
        # 게시글 작성 페이지
        self.stacked_widget.setCurrentIndex(self.PAGE_INDEX_CREATE)

    def handle_post_saved(self, data: dict):
        # DB에 post 저장
        post_id = self.db.create_post(
            data["title"],
            data["author"],
            data["content"],
        )
        QMessageBox.information(self, "저장 완료", "게시글이 저장되었습니다.")
        self.show_list_page()   #TODO: 상세 페이지로 이동

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