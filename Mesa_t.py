import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtGui import QIcon, QMouseEvent, QPixmap, QFont

class TitleBar(QWidget):
    def __init__(self, parent=None):
        super(TitleBar, self).__init__(parent)

        self.setAutoFillBackground(True)
        self.setStyleSheet("background-color: #1E1E1E;")  # Цвет фона заголовка

        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(10, 0, 0, 0)  # Убираем отступы
        self.layout.setSpacing(0)  # Убираем промежутки между кнопками

        # Иконка приложения
        app_icon = QLabel()
        app_icon.setPixmap(QPixmap("G:Загрузки\Беапорваапоз имени(12)(3).png"))  # Замените на вашу иконку
        app_icon.setFixedSize(30, 30)
        self.layout.addWidget(app_icon)

        # Название приложения
        title = QLabel(" Mesa Browser")
        title.setFont(QFont("Arial", 11))  # Устанавливаем шрифт Unbounded
        title.setStyleSheet("color: white;")
        self.layout.addWidget(title)

        # Добавляем пространство, чтобы сдвинуть кнопки вправо
        spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.layout.addItem(spacer)

        # Кнопка минимизации
        minimize_button = QPushButton("🗕")  # Символ для кнопки минимизации
        minimize_button.setFixedSize(30, 30)  # Устанавливаем фиксированный размер
        minimize_button.setStyleSheet("background-color: #1E1E1E; color: white; border: none;")  # Убираем фон и рамку
        minimize_button.clicked.connect(self.show_minimized)
        self.layout.addWidget(minimize_button)

        # Кнопка развертывания
        maximize_button = QPushButton("🗖")  # Символ для кнопки развертывания
        maximize_button.setFixedSize(30, 30)  # Устанавливаем фиксированный размер
        maximize_button.setStyleSheet("background-color: #1E1E1E; color: white; border: none;")  # Убираем фон и рамку
        maximize_button.clicked.connect(self.toggle_maximize)
        self.layout.addWidget(maximize_button)

        # Кнопка закрытия
        close_button = QPushButton("✖")  # Символ для кнопки закрытия
        close_button.setFixedSize(30, 30)  # Устанавливаем фиксированный размер
        close_button.setStyleSheet("background-color: #1E1E1E; color: white; border: none;")  # Убираем фон и рамку
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

        # Устанавливаем иконку приложения (плейсхолдер)
        self.setWindowIcon(QIcon("G:Загрузки\Беапорваапоз имени(12)(1).png"))  # Плейсхолдер для иконки приложения

        # Устанавливаем темную тему
        self.setStyleSheet("""
    QMainWindow {
        background-color: #1E1E1E; /* Цвет фона окна */
        color: #FFFFFF; /* Цвет текста */
    }
    QTabWidget::pane {
        background-color: #1E1E1E; /* Цвет фона вкладок */
        border: none; /* Убираем рамку панели вкладок */
        border-radius: 10px; /* Скругленные углы панели вкладок */
    }
    QTabBar::tab {
        background: #1E1E1E; /* Цвет фона вкладки */
        color: #FFFFFF; /* Цвет текста вкладки */
        padding: 3px;
        border: 1px solid #444; /* Цвет рамки вкладки */
        border-top-left-radius: 10px; /* Скругление верхних углов */
        border-top-right-radius: 10px; /* Скругление верхних углов */
        margin-left: 5px; /* Отступ между вкладками */
        margin-right: 5px;
    }
    QTabBar::tab:selected {
        background: #2A2A2A; /* Цвет фона выделенной вкладки */
    }
    QToolBar {
        background-color: #1E1E1E; /* Цвет фона панели инструментов */
        border: 1px solid #444; /* Цвет рамки панели инструментов */
        margin: 5px; /* Отступы вокруг панели инструментов */
    }
    QLineEdit {
        background-color: #2A2A2A; /* Цвет фона строки ввода URL */
        color: #FFFFFF; /* Цвет текста в строке ввода */
        border-radius: 15px; /* Скругленные углы строки ввода URL */
        border: 1px solid #444; /* Цвет рамки строки ввода */
        margin: 5px; /* Отступы вокруг строки ввода URL */
        height: 30px; /* Увеличиваем высоту, чтобы скругление было заметно */
    }
    QPushButton {
        background-color: #1E1E1E; /* Цвет фона кнопок */
        color: #FFFFFF; /* Цвет текста кнопок */
        border: none; /* Убираем рамку у кнопок */
    }
""")

        # Удаляем системную рамку
        self.setWindowFlags(Qt.FramelessWindowHint)

        # Заголовок окна
        self.title_bar = TitleBar(self)
        self.setMenuWidget(self.title_bar)

        # Создаем виджет с вкладками
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.tabBarDoubleClicked.connect(self.open_new_tab)
        self.tabs.currentChanged.connect(self.current_tab_changed)
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_current_tab)

        self.setCentralWidget(self.tabs)

        # Добавляем панель инструментов
        navbar = QToolBar()
        self.addToolBar(navbar)

        # Кнопки навигации с плейсхолдерами
        back_btn = QAction(QIcon("G:Загрузки\icons8-sort-right-64(1).png"), "Назад", self)
        back_btn.triggered.connect(lambda: self.tabs.currentWidget().back())
        navbar.addAction(back_btn)

        forward_btn = QAction(QIcon("G:Загрузки\icons8-sort-right-64.png"), "Вперед", self)
        forward_btn.triggered.connect(lambda: self.tabs.currentWidget().forward())
        navbar.addAction(forward_btn)

        reload_btn = QAction(QIcon("G:Загрузки\icons8-synchronize-64.png"), "Перезагрузить", self)
        reload_btn.triggered.connect(lambda: self.tabs.currentWidget().reload())
        navbar.addAction(reload_btn)

        home_btn = QAction(QIcon("G:Загрузки\icons8-home-64.png"), "Домой", self)
        home_btn.triggered.connect(self.navigate_home)
        navbar.addAction(home_btn)

        # Строка для ввода URL
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        navbar.addWidget(self.url_bar)

        # Кнопка для открытия новой вкладки с плейсхолдером
        new_tab_btn = QAction(QIcon("G:Загрузки\icons8-plus-64.png"), "Новая вкладка", self)
        new_tab_btn.triggered.connect(self.open_new_tab)
        navbar.addAction(new_tab_btn)

        # Открываем первую вкладку
        self.add_new_tab(QUrl("http://www.google.com"), "Новая вкладка")

        # Отображаем окно
        self.showMaximized()

    def add_new_tab(self, qurl=None, label="Новая вкладка"):
        # Если URL не задан, используем Google
        if qurl is None:
            qurl = QUrl("http://www.google.com")

        # Создаем новый браузер
        browser = QWebEngineView()
        browser.setUrl(qurl)

        # Добавляем вкладку и делаем ее активной
        i = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(i)

        # Устанавливаем иконку закрытия для новой вкладки
        close_button = QPushButton()
        close_button.setFixedSize(20, 20)
        close_button.setIcon(QIcon("G:Загрузки\icons8-close-64.png"))  # Замените на вашу иконку для закрытия
        close_button.setIconSize(QSize(20, 20))
        close_button.setStyleSheet("background: transparent; border: none; color: white;")
        close_button.clicked.connect(lambda: self.close_current_tab(i))
        self.tabs.tabBar().setTabButton(i, QTabBar.RightSide, close_button)

        # Подключаем сигналы для обновления URL и заголовка вкладки
        browser.urlChanged.connect(lambda qurl, browser=browser: self.update_tab_title(browser))
        browser.iconChanged.connect(lambda icon, browser=browser: self.update_tab_icon(browser, icon))
        browser.urlChanged.connect(self.update_url)

    def open_new_tab(self, i=None):
        # Открываем новую вкладку при двойном клике или по кнопке
        self.add_new_tab()

    def close_current_tab(self, i):
        # Закрываем вкладку, если она не единственная
        if self.tabs.count() < 2:
            return

        self.tabs.removeTab(i)

    def update_tab_title(self, browser):
        # Обновление заголовка вкладки
        index = self.tabs.indexOf(browser)
        if index >= 0:
            self.tabs.setTabText(index, browser.page().title())

    def update_tab_icon(self, browser, icon):
        # Обновление иконки вкладки
        index = self.tabs.indexOf(browser)
        if index >= 0:
            self.tabs.setTabIcon(index, icon)

    def current_tab_changed(self, i):
        # Обновление строки URL при смене вкладки
        qurl = self.tabs.currentWidget().url()
        self.url_bar.setText(qurl.toString())

    def navigate_home(self):
        # Навигация на домашнюю страницу
        self.tabs.currentWidget().setUrl(QUrl("http://www.google.com"))

    def navigate_to_url(self):
        # Переход по введенному URL
        url = self.url_bar.text()
        self.tabs.currentWidget().setUrl(QUrl(url))

    def update_url(self, q):
        # Обновление строки URL при смене страницы
        self.url_bar.setText(q.toString())

# Запуск приложения
app = QApplication(sys.argv)
QApplication.setApplicationName("Mesa Browser")
app.setFont(QFont("Arial"))  # Устанавливаем шрифт приложения
window = Browser()
window.setWindowTitle("Mesa Browser")  # Название окна
window.show()  # Отображаем окно
app.exec_()
