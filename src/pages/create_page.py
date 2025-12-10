from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QTextEdit, QHBoxLayout, QMessageBox
from PyQt6.QtCore import Qt, pyqtSignal

# 리스트, 게시글 작성 버튼
class CreatePage(QWidget):
    finished = pyqtSignal()
    saved = pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout()

        ## 요소
        title_label = QLabel("게시글 작성하기")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 20px; font-weight: bold;")

        # 1. 제목, 내용, 작성자 입력란
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("제목을 입력하세요")
        self.author_input = QLineEdit()
        self.author_input.setPlaceholderText("작성자를 입력하세요")
        self.content_input = QTextEdit()
        self.content_input.setPlaceholderText("내용을 입력하세요")

        # 2. 버튼 영역
        button_row = QHBoxLayout()

        # 2-1. 취소 버튼 -> TODO:message -> finished
        cancel_btn = QPushButton("취소")
        cancel_btn.clicked.connect(self.finished.emit)

        # 2-2. TODO: 저장 버튼 -> DB 저장, message -> finished
        save_btn = QPushButton("저장")
        save_btn.clicked.connect(self.save_post)

        button_row.addWidget(cancel_btn)
        button_row.addWidget(save_btn)


        # add Widget
        layout.addWidget(title_label)

        layout.addWidget(QLabel("제목"))
        layout.addWidget(self.title_input)

        layout.addWidget(QLabel("작성자"))
        layout.addWidget(self.author_input)

        layout.addWidget(QLabel("내용"))
        layout.addWidget(self.content_input)

        layout.addLayout(button_row)

        self.setLayout(layout)

    def save_post(self):
        title = self.title_input.text().strip()
        author = self.author_input.text().strip()
        content = self.content_input.toPlainText().strip()

        # 유효성 검사
        if not title:
            QMessageBox.warning(self, "입력 오류", "제목을 입력해 주세요.")
            return
        if len(title) > 100:
            QMessageBox.warning(self, "입력 오류", "제목은 100자 이내로 입력해 주세요.")
            return

        if not author:
            QMessageBox.warning(self, "입력 오류", "작성자를 입력해 주세요.")
            return
        if len(author) > 20:
            QMessageBox.warning(self, "입력 오류", "작성자명은 20자 이내로 입력해 주세요.")
            return

        if not content:
            QMessageBox.warning(self, "입력 오류", "내용을 입력해 주세요.")
            return

        data = {
            "title": title,
            "author": author,
            "content": content
        }
        self.saved.emit(data)

        self.title_input.clear()
        self.author_input.clear()
        self.content_input.clear()