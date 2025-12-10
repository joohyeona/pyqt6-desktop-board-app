from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QTextEdit, QHBoxLayout, QMessageBox
from PyQt6.QtCore import Qt, pyqtSignal

# 리스트, 게시글 작성 버튼
class CreatePage(QWidget):
    finished = pyqtSignal()
    saved = pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._post_id: int | None = None  # 수정 | 신규 mode
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

        # 2-1. 취소 btn
        cancel_btn = QPushButton("취소")
        cancel_btn.clicked.connect(self.on_cancel)

        # 2-2. 저장 btn
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

    # 신규 작성 mode
    def set_new(self):
        self._post_id = None
        self.title_input.clear()
        self.author_input.clear()
        self.content_input.clear()

        # 원본 상태 저장 - 취소 시 비교
        self._original = {
            "title": "",
            "author": "",
            "content": ""
        }

    # 수정 mode
    def set_detail(self, post):
        if not post:
            QMessageBox.warning(self, "Error", "수정 내용을 불러올 수 없습니다.")

        self._post_id = post["id"]
        self.title_input.setText(post["title"])
        self.author_input.setText(post["author"])
        self.content_input.setPlainText(post["content"])

        # 원본 상태 저장 - 취소 시 비교
        self._original = {
            "title": post["title"],
            "author": post["author"],
            "content": post["content"]
        }


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
        if self._post_id is not None:
            data["id"] = self._post_id

        self.saved.emit(data)

        self.title_input.clear()
        self.author_input.clear()
        self.content_input.clear()

    def on_cancel(self):
        current = {
            "title": self.title_input.text(),
            "author": self.author_input.text(),
            "content": self.content_input.toPlainText()
        }

        # 변경 내용 있을 시 alert
        if current != self._original:
            reply = QMessageBox.question(
                self,
                "Alert",
                "변경 내용이 저장되지 않았습니다. 취소하시겠습니까?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.No:
                return

        self.finished.emit()