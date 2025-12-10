from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QTextEdit, QMessageBox, QFormLayout, QHBoxLayout
from PyQt6.QtCore import Qt, pyqtSignal

class DetailPage(QWidget):
    back_to_list = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout()

        page_title = QLabel("게시글 상세 보기")
        page_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        page_title.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(page_title)

        # 상세 내용
        self.form = QFormLayout()
        self.form.setFormAlignment(Qt.AlignmentFlag.AlignTop)

        # set_detail에서 값 채워넣음
        self.title_view = QLabel()
        self.author_view = QLabel()
        self.created_view = QLabel()
        self.updated_view = QLabel()
        self.content_view = QTextEdit()

        # ReadOnly
        self.content_view.setReadOnly(True)

        self.form.addRow("제목", self.title_view)
        self.form.addRow("작성자", self.author_view)
        self.form.addRow("작성일자", self.created_view)
        self.form.addRow("수정일자", self.updated_view)

        # btn
        button_row = QHBoxLayout()
        update_btn = QPushButton("수정")
        # TODO: 수정 logic
        delete_btn = QPushButton("삭제")
        # TODO: 삭제 logic

        button_row.addWidget(update_btn)
        button_row.addWidget(delete_btn)
        button_row.setAlignment(Qt.AlignmentFlag.AlignRight)

        back_btn = QPushButton("목록으로")
        back_btn.clicked.connect(self.back_to_list.emit)

        layout.addLayout(button_row)
        layout.addLayout(self.form)
        layout.addWidget(QLabel("내용"))
        layout.addWidget(self.content_view)
        layout.addWidget(back_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        self.setLayout(layout)

    def set_detail(self, post):
        if not post:
            QMessageBox.warning(self, "Error", "존재하지 않는 게시글입니다.")
            return

        self.title_view.setText(post["title"])
        self.author_view.setText(post["author"])
        self.created_view.setText(post["created_at"])
        self.content_view.setPlainText(post["content"])

        if post["updated_at"]:
            self.updated_view.setText(post["updated_at"])
            self.updated_view.setStyleSheet("")
        else:
            self.updated_view.setText("-")
            self.updated_view.setStyleSheet("color: gray;")