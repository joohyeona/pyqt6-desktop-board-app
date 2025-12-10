import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget

from pages import ListPage, CreatePage # init으로 import

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("DDE Desktop Board")
        self.setMinimumSize(800, 600)

        # QStackedWidget으로 페이지 전환
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # 페이지 인덱스
        self.PAGE_INDEX_LIST = 0
        self.PAGE_INDEX_CREATE = 1

        # 페이지 인스턴스
        self.list_page = ListPage()
        self.create_page = CreatePage()

        # signal-slot 연결
        # list page -> create 버튼 -> show_create_page
        self.list_page.request_create.connect(self.show_create_page)
        # create page -> finished 요청 -> list
        self.create_page.finished.connect(self.show_list_page)

        # QStackedWidget에 페이지 등록
        self.stacked_widget.addWidget(self.list_page)   # index 0
        self.stacked_widget.addWidget(self.create_page) # index 1

        # 첫 페이지
        self.show_list_page()


    def show_list_page(self):
        # 게시글 목록 페이지
        self.stacked_widget.setCurrentIndex(self.PAGE_INDEX_LIST)

    def show_create_page(self):
        # 게시글 작성 페이지
        self.stacked_widget.setCurrentIndex(self.PAGE_INDEX_CREATE)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()