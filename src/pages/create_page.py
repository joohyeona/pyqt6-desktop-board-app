from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt, pyqtSignal

# 리스트, 게시글 작성 버튼
class CreatePage(QWidget):
    finished = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout()

        ## 요소
        title_label = QLabel("게시글 작성하기")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 20px; font-weight: bold;")

        # 1. TODO: 제목

        # 2. TODO: 내용, 작성자 작성란

        # 3. TODO: 저장 버튼 -> DB 저장, message -> finished

        # 4. 취소 버튼 -> TODO:message -> finished
        cancel_btn = QPushButton("취소")
        cancel_btn.clicked.connect(self.finished.emit)


        # add Widget
        layout.addWidget(title_label)
        layout.addWidget(cancel_btn)

        self.setLayout(layout)

    # TODO: save logic


        layout.addWidget(title_label)

        self.setLayout(layout)