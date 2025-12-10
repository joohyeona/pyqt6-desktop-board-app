from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt, pyqtSignal

# 리스트, 게시글 작성 버튼
class ListPage(QWidget):
    # signal-slot
    request_create = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout()

        ## 요소
        # 1. 제목
        title_label = QLabel("게시글 목록")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 20px; font-weight: bold;")

        # 2. TODO: 목록

        # 3. 게시글 작성 버튼 -> main에 signal
        create_btn = QPushButton("게시글 작성")
        create_btn.clicked.connect(self.request_create.emit)


        # widget 배치
        layout.addWidget(title_label)
        layout.addWidget(create_btn, alignment=Qt.AlignmentFlag.AlignRight)

        self.setLayout(layout)