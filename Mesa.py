import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtGui import QIcon, QMouseEvent


class TitleBar(QWidget):
    def __init__(self, parent=None):
        super(TitleBar, self).__init__(parent)

        self.setAutoFillBackground(True)
        self.setStyleSheet("background-color: #1E1E1E;")

        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.layout.addItem(spacer)

        minimize_button = QPushButton("🗕")
        minimize_button.setFixedSize(30, 30)
        minimize_button.setStyleSheet("background-color: #1E1E1E; color: white; border: none;")
        minimize_button.clicked.connect(self.show_minimized)
        self.layout.addWidget(minimize_button)

        maximize_button = QPushButton("🗖")
        maximize_button.setFixedSize(30, 30)
        maximize_button.setStyleSheet("background-color: #1E1E1E; color: white; border: none;")
        maximize_button.clicked.connect(self.toggle_maximize)
        self.layout.addWidget(maximize_button)

        close_button = QPushButton("✖")
        close_button.setFixedSize(30, 30)
        close_button.setStyleSheet("background-color: #1E1E1E; color: white; border: none;")
        close_button.clicked.connect(self.close_window)
        self.layout.addWidget(close_button)

        self.setLayout(self.layout)

        self.mousePressPos = None
        self.mouseMovePos = None

    def close_window(self):
        self.parent().close()

    def toggle_maximize(self):
        if self.parent().isMaximized():
            self.parent().showNormal()
        else:
            self.parent().showMaximized()

    def show_minimized(self):
        self.parent().showMinimized()

    def mousePressEvent(self, event: QMouseEvent):
        self.mousePressPos = event.globalPos() - self.parent().frameGeometry().topLeft()
        event.accept()

    def mouseMoveEvent(self, event: QMouseEvent):
        if event.buttons() == Qt.LeftButton:
            self.parent().move(event.globalPos() - self.mousePressPos)
        event.accept()


class Browser(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowIcon(QIcon("G:/Загрузки/your_icon.png"))

        self.setStyleSheet("""
            QMainWindow {
                background-color: #1E1E1E;
                color: #FFFFFF;
            }
            QTabWidget {
                background-color: #1E1E1E;
                color: #FFFFFF;
            }
            QTabBar::tab {
                background: #1E1E1E;
                color: #FFFFFF;
                padding: 10px;
                border: 1px solid #444;
            }
            QTabBar::tab:selected {
                background: #2A2A2A;
            }
            QToolBar {
                background-color: #1E1E1E;
                border: 1px solid #444;
            }
            QLineEdit {
                background-color: #2A2A2A;
                color: #FFFFFF;
                padding: 5px;
                border: 1px solid #444;
            }
            QPushButton {
                background-color: #1E1E1E;
                color: #FFFFFF;
                padding: 5px;
                border: none;
            }
        """)

        self.setWindowFlags(Qt.FramelessWindowHint)

        self.title_bar = TitleBar(self)
        self.setMenuWidget(self.title_bar)

        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.tabBarDoubleClicked.connect(self.open_new_tab)
        self.tabs.currentChanged.connect(self.current_tab_changed)
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_current_tab)

        self.tabs.setStyleSheet("""
            QTabBar::close-button {
                image: url(G:/Загрузки/your_close_icon.png);
                subcontrol-position: right;
            }
            QTabBar::close-button:hover {
                image: url(G:/Загрузки/your_close_icon_hover.png);
            }
        """)

        self.setCentralWidget(self.tabs)

        navbar = QToolBar()
        self.addToolBar(navbar)

        back_btn = QAction(QIcon("G:/Загрузки/icons8-sort-right-64(1).png"), "Назад", self)
        back_btn.triggered.connect(lambda: self.tabs.currentWidget().back())
        navbar.addAction(back_btn)

        forward_btn = QAction(QIcon("G:/Загрузки/icons8-sort-right-64.png"), "Вперед", self)
        forward_btn.triggered.connect(lambda: self.tabs.currentWidget().forward())
        navbar.addAction(forward_btn)

        reload_btn = QAction(QIcon("G:/Загрузки/icons8-synchronize-64.png"), "Перезагрузить", self)
        reload_btn.triggered.connect(lambda: self.tabs.currentWidget().reload())
        navbar.addAction(reload_btn)

        home_btn = QAction(QIcon("G:/Загрузки/icons8-home-64.png"), "Домой", self)
        home_btn.triggered.connect(self.navigate_home)
        navbar.addAction(home_btn)

        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        navbar.addWidget(self.url_bar)

        new_tab_btn = QAction(QIcon("G:/Загрузки/icons8-plus-64.png"), "Новая вкладка", self)
        new_tab_btn.triggered.connect(self.open_new_tab)
        navbar.addAction(new_tab_btn)

        self.add_new_tab(QUrl("http://www.google.com"), "Новая вкладка")

        self.showMaximized()

    def add_new_tab(self, qurl=None, label="Новая вкладка"):
        if qurl is None:
            qurl = QUrl("http://www.google.com")

        browser = QWebEngineView()
        browser.setUrl(qurl)

        i = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(i)

        browser.urlChanged.connect(lambda qurl, browser=browser: self.update_tab_title(browser))
        browser.iconChanged.connect(lambda icon, browser=browser: self.update_tab_icon(browser, icon))
        browser.urlChanged.connect(self.update_url)

    def open_new_tab(self, i=None):
        self.add_new_tab()

    def close_current_tab(self, i):
        if self.tabs.count() > 1:
            self.tabs.removeTab(i)

    def update_tab_title(self, browser):
        index = self.tabs.indexOf(browser)
        if index >= 0:
            self.tabs.setTabText(index, browser.page().title())

    def update_tab_icon(self, browser, icon):
        index = self.tabs.indexOf(browser)
        if index >= 0:
            self.tabs.setTabIcon(index, icon)

    def current_tab_changed(self, i):
        qurl = self.tabs.currentWidget().url()
        self.url_bar.setText(qurl.toString())

    def navigate_home(self):
        self.tabs.currentWidget().setUrl(QUrl("http://www.google.com"))

    def navigate_to_url(self):
        url = self.url_bar.text()
        self.tabs.currentWidget().setUrl(QUrl(url))

    def update_url(self, q):
        self.url_bar.setText(q.toString())


app = QApplication(sys.argv)
QApplication.setApplicationName("Mesa Browser")
window = Browser()
window.setWindowTitle("Mesa Browser")
window.show()
app.exec_()
