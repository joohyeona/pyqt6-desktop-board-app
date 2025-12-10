from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QAbstractItemView
from PyQt6.QtCore import Qt, pyqtSignal

# 리스트, 게시글 작성 버튼
class ListPage(QWidget):
    request_create = pyqtSignal()    # signal-slot main으로
    request_detail = pyqtSignal(int) # detail page 요청

    def __init__(self, parent=None):
        super().__init__(parent)
        self.post_ids: list[int] = []   # 행별 post_id 저장
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout()

        ## 요소
        # 1. 제목
        title_label = QLabel("게시판")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 20px; font-weight: bold;")

        # 2. 목록 table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["No.", "제목", "작성자", "작성일자"])
        self.table.horizontalHeader().setStretchLastSection(True)

        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)         # edit block
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)  # 행 단위 선택
        self.table.cellClicked.connect(self.click_row)   # 행 클릭 -> 상세 페이지

        # 3. 게시글 작성 버튼 -> main에 signal
        create_btn = QPushButton("게시글 작성")
        create_btn.clicked.connect(self.request_create.emit)


        # widget 배치
        layout.addWidget(title_label)
        layout.addWidget(self.table)
        layout.addWidget(create_btn, alignment=Qt.AlignmentFlag.AlignRight)

        self.setLayout(layout)

    def load_posts(self, posts: list):
        self.table.setRowCount(len(posts))

        for row_idx, post in enumerate(posts):
            self.post_ids.append(post["id"])

            num_col = QTableWidgetItem(str(row_idx + 1))
            title_col = QTableWidgetItem(post["title"])
            author_col = QTableWidgetItem(post["author"])
            date_col = QTableWidgetItem(post["created_at"])

            # 정렬
            num_col.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            author_col.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            date_col.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            self.table.setItem(row_idx, 0, num_col)
            self.table.setItem(row_idx, 1, title_col)
            self.table.setItem(row_idx, 2, author_col)
            self.table.setItem(row_idx, 3, date_col)

    def click_row(self, row:int, column: int):
        post_id = self.post_ids[row]
        self.request_detail.emit(post_id)