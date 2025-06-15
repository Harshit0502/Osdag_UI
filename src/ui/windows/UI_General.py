# -*- coding: utf-8 -*-
"""General UI window for Osdag
This implements the main layout with sidebar, header, connection tabs,
design cards and footer. It follows the specification provided in the
prompt and uses PySide6 widgets directly.
"""

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QPushButton, QLabel, QSplitter, QFrame, QSizePolicy, QApplication, QButtonGroup
)
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtGui import QFont, QPixmap, QColor, QPainter, QIcon, QCursor
from PySide6.QtCore import Qt, QSize, QMetaObject

import resources.resources_rc  # ensure resource import


class OsdagGeneralUI(object):
    """Setup class to build the main window."""

    sidebar_buttons = [
        ("Home", ":/vectors/Osdag_logo.svg"),
        ("Tension Member", ":/vectors/Osdag_logo.svg"),
        ("Compression Member", ":/vectors/Osdag_logo.svg"),
        ("Flexure Member", ":/vectors/Osdag_logo.svg"),
        ("Beam-Column", ":/vectors/Osdag_logo.svg"),
        ("Plate Girder", ":/vectors/Osdag_logo.svg"),
        ("Truss", ":/vectors/Osdag_logo.svg"),
        ("2D Frame", ":/vectors/Osdag_logo.svg"),
        ("3D Frame", ":/vectors/Osdag_logo.svg"),
        ("Group Design", ":/vectors/Osdag_logo.svg"),
    ]

    connection_tabs = [
        "Shear Connection",
        "Moment Connection",
        "Base Plate",
        "Truss Connection",
    ]

    def setupUi(self, MainWindow: QMainWindow):
        MainWindow.setObjectName("Osdag_MainWindow")
        MainWindow.setMinimumSize(1100, 700)
        MainWindow.setStyleSheet("background-color: white;")
        self.centralwidget = QWidget(MainWindow)
        self.main_layout = QHBoxLayout(self.centralwidget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.splitter = QSplitter(Qt.Horizontal, self.centralwidget)
        self.main_layout.addWidget(self.splitter)

        # Sidebar
        self.sidebar_widget = QWidget()
        self.sidebar_layout = QVBoxLayout(self.sidebar_widget)
        self.sidebar_layout.setContentsMargins(5, 5, 5, 5)
        self.sidebar_layout.setSpacing(2)

        self.button_group = QButtonGroup(self.sidebar_widget)
        self.button_group.setExclusive(True)
        for text, icon_path in self.sidebar_buttons:
            btn = QPushButton(text)
            btn.setCheckable(True)
            btn.setIcon(QIcon(icon_path))
            btn.setIconSize(QSize(24, 24))
            btn.setStyleSheet(self._sidebar_button_style(False))
            btn.clicked.connect(self._sidebar_button_clicked)
            self.sidebar_layout.addWidget(btn)
            self.button_group.addButton(btn)

        self.sidebar_layout.addStretch(1)
        self.iitb_logo = QSvgWidget(":/vectors/IITB_logo.svg")
        self.iitb_logo.setFixedSize(60, 60)
        self.sidebar_layout.addWidget(self.iitb_logo, 0, Qt.AlignHCenter)
        self.splitter.addWidget(self.sidebar_widget)

        # Right panel
        self.right_panel = QWidget()
        self.right_layout = QVBoxLayout(self.right_panel)
        self.right_layout.setContentsMargins(10, 10, 10, 10)
        self.right_layout.setSpacing(10)

        # Header
        self.header_widget = QWidget()
        self.header_layout = QHBoxLayout(self.header_widget)
        self.header_layout.setContentsMargins(0, 0, 0, 0)
        self.osdag_logo = QSvgWidget(":/vectors/Osdag_logo.svg")
        self.osdag_logo.setFixedSize(60, 60)
        self.header_layout.addWidget(self.osdag_logo, 0, Qt.AlignLeft | Qt.AlignVCenter)

        self.header_label = QLabel("Osdag® Open steel design and graphics")
        font = QFont("Calibri", 20)
        font.setBold(True)
        self.header_label.setFont(font)
        self.header_label.setStyleSheet("color: black;")
        self.header_layout.addWidget(self.header_label, 1, Qt.AlignLeft | Qt.AlignVCenter)
        self.right_layout.addWidget(self.header_widget)

        # Connection tabs
        self.tab_widget = QWidget()
        self.tab_layout = QHBoxLayout(self.tab_widget)
        self.tab_layout.setSpacing(4)
        self.tab_layout.setContentsMargins(0, 0, 0, 0)
        self.tab_buttons = []
        for tab in self.connection_tabs:
            t_btn = QPushButton(tab)
            t_btn.setCheckable(True)
            t_btn.clicked.connect(self._tab_clicked)
            t_btn.setStyleSheet(self._tab_button_style(False))
            self.tab_layout.addWidget(t_btn)
            self.tab_buttons.append(t_btn)
        self.right_layout.addWidget(self.tab_widget)

        # Sub options area
        self.sub_option_widget = QWidget()
        self.sub_option_layout = QHBoxLayout(self.sub_option_widget)
        self.sub_option_layout.setContentsMargins(0, 0, 0, 0)
        self.right_layout.addWidget(self.sub_option_widget)

        # Design cards section
        self.card_container = QWidget()
        self.card_layout = QGridLayout(self.card_container)
        self.card_layout.setSpacing(20)
        self.card_layout.setContentsMargins(0, 0, 0, 0)
        # example cards
        for i in range(6):
            card = QFrame()
            card.setFrameShape(QFrame.StyledPanel)
            card.setStyleSheet(self._card_style())
            c_layout = QVBoxLayout(card)
            img = QLabel()
            img.setPixmap(QPixmap(":/vectors/Osdag_logo.svg"))
            img.setAlignment(Qt.AlignCenter)
            title = QLabel(f"Design {i+1}")
            title.setAlignment(Qt.AlignCenter)
            title.setFont(QFont("Calibri", 12))
            c_layout.addWidget(img)
            c_layout.addWidget(title)
            row = i // 3
            col = i % 3
            self.card_layout.addWidget(card, row, col)
            card.mousePressEvent = lambda e, n=i+1: print(f"Selected design {n}")
        self.right_layout.addWidget(self.card_container, 1)

        # Footer
        self.footer_widget = QWidget()
        self.footer_layout = QHBoxLayout(self.footer_widget)
        self.footer_layout.setContentsMargins(0, 0, 0, 0)
        self.footer_layout.setSpacing(20)
        self.version_label = QLabel("Version 1.0.0")
        self.version_label.setStyleSheet("color: gray;")
        self.footer_layout.addWidget(self.version_label)
        self.footer_layout.addStretch(1)
        logos = [":/vectors/FOSSEE_logo.svg", ":/vectors/MOS_logo.svg",
                 ":/vectors/ConstructSteel_logo.svg", ":/vectors/IITB_logo.svg"]
        for l in logos:
            w = QSvgWidget(l)
            w.setFixedSize(80, 40)
            self.footer_layout.addWidget(w)
        self.right_layout.addWidget(self.footer_widget)

        self.splitter.addWidget(self.right_panel)
        self.splitter.setSizes([150, 950])

        MainWindow.setCentralWidget(self.centralwidget)
        QMetaObject.connectSlotsByName(MainWindow)

        # activate default selections
        if self.button_group.buttons():
            self.button_group.buttons()[0].setChecked(True)
            self._update_sidebar_styles()
        if self.tab_buttons:
            self.tab_buttons[0].setChecked(True)
            self._update_tab_styles()
            self._populate_sub_options(0)

    # -------- style helpers ----------
    def _sidebar_button_style(self, checked: bool) -> str:
        if checked:
            return "background-color: #90af13; color: white; text-align: left; padding: 5px;"
        return "background-color: white; color: black; text-align: left; padding: 5px;"

    def _tab_button_style(self, checked: bool) -> str:
        if checked:
            return "background-color: #90af13; color: white; padding: 4px 8px;"
        return "background-color: white; color: black; padding: 4px 8px;"

    def _card_style(self) -> str:
        return (
            "QFrame {border: 1px solid #ddd; border-radius: 4px;"\
            "background: #fefefe;}"
        )

    # --------- interaction handlers ---------
    def _sidebar_button_clicked(self):
        self._update_sidebar_styles()

    def _tab_clicked(self):
        self._update_tab_styles()
        index = self.tab_buttons.index(self.sender())
        self._populate_sub_options(index)

    def _update_sidebar_styles(self):
        for btn in self.button_group.buttons():
            btn.setStyleSheet(self._sidebar_button_style(btn.isChecked()))

    def _update_tab_styles(self):
        for btn in self.tab_buttons:
            btn.setStyleSheet(self._tab_button_style(btn.isChecked()))

    def _populate_sub_options(self, tab_index: int):
        # Clear current sub options
        while self.sub_option_layout.count():
            item = self.sub_option_layout.takeAt(0)
            w = item.widget()
            if w is not None:
                w.deleteLater()
        # Placeholder sub options
        options = [
            ["Beam to Beam Splice", "Beam to Column Splice", "PEB"],
            ["End Plate", "Flange Plate"],
            ["Base Plate"],
            ["Truss"],
        ]
        if tab_index < len(options):
            for opt in options[tab_index]:
                b = QPushButton(opt)
                b.setStyleSheet(
                    "background-color: white; border: 1px solid #ccc; padding: 4px;"
                )
                self.sub_option_layout.addWidget(b)
        self.sub_option_layout.addStretch(1)


if __name__ == "__main__":
    app = QApplication([])
    w = QMainWindow()
    ui = OsdagGeneralUI()
    ui.setupUi(w)
    w.show()
    app.exec()
