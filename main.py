import sys
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWidgets import *


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.lastPos = None
        self.title = ""

        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # Create the QWebEngineView and set the URL to load
        self.browser = QWebEngineView()
        self.browser.load(QUrl("https://e621.net"))

        # Apply a dark theme to the web page
        self.browser.setStyleSheet("background-color: #1f1f1f; color: #fff;")

        # Set the browser as the central widget of the main window
        self.setCentralWidget(self.browser)

        # Set the window properties
        self.setWindowTitle("e621")
        self.showMaximized()


        # Create the navigation toolbar and add the buttons
        navbar = QToolBar()
        navbar.setMovable(False)
        navbar.setFloatable(False)
        navbar.setStyleSheet("""
            QToolBar {
                margin-top: -1px;
                background-color: #1f1f1f;
                padding: 10px;
                text-align: center;
            }

            QToolButton {
                font-family: 'Baloo', sans-serif;
                font-size: 16px;
                background-color: #1f1f1f;
                margin-left: 5px;
                padding: 5px;
                margin-top: 2px;
                margin-bottom: 2px;
                color: #fff;
                transition: 0.2s;
                line-height: 20px;
            }

            QToolButton:hover {
                color: #fff;
                background-color: #2f2f2f;
                padding: 5px;
                line-height: 20px;
            }

            /* Add custom styles for the close and minimize buttons */
            #close_button, #minimize_button {
                background-color: transparent;
                border: none;
                font-size: 20px;
                width: 28px;
                height: 28px;
                margin-right: 10px;
                line-height: 20px;
            }
            #close_button:hover, #minimize_button:hover {
                background-color: #3f3f3f;
            }
        """)
        self.addToolBar(navbar)

        back_btn = QAction("Back", self)
        back_btn.triggered.connect(self.browser.back)
        navbar.addAction(back_btn)

        forward_btn = QAction("Forward", self)
        forward_btn.triggered.connect(self.browser.forward)
        navbar.addAction(forward_btn)

        reload_btn = QAction("Reload", self)
        reload_btn.triggered.connect(self.browser.reload)
        navbar.addAction(reload_btn)

        home_btn = QAction("Home", self)
        home_btn.triggered.connect(self.navigate_home)
        navbar.addAction(home_btn)

        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        navbar.addWidget(spacer)

        # Create the minimize button and add it to the toolbar
        minimize_btn = QToolButton()
        minimize_btn.setObjectName("minimize_button")
        minimize_btn.setText("−")
        minimize_btn.clicked.connect(self.showMinimized)
        navbar.addWidget(minimize_btn)

        screen_btn = QToolButton()
        screen_btn.setObjectName("minimize_button")
        screen_btn.setText("◻")
        screen_btn.clicked.connect(self.toggle_maximized)
        navbar.addWidget(screen_btn)

        close_btn = QToolButton()
        close_btn.setObjectName("close_button")
        close_btn.setText("×")
        close_btn.clicked.connect(self.close)
        navbar.addWidget(close_btn)

        self.setMouseTracking(True)
        navbar.setMouseTracking(True)
        navbar.mouseMoveEvent = self.mouseMoveEvent



    def navigate_home(self):
        self.browser.load(QUrl("https://www.e621.net"))

    def toggle_maximized(self):
        if self.isMaximized():
            self.showNormal()  # restore the window
        else:
            self.showMaximized()  # maximize the window

    def FullscreenRequest(self, request):
        request.accept()
        if request.toggleOn():
            self.browser.setParent(None)
            self.browser.showFullScreen()
        else:
            self.setCentralWidget(self.browser)
            self.browser.showNormal()

    def mousePressEvent(self, event):
        self.oldPosition = event.globalPos()

    def mouseMoveEvent(self, e):
        if self.isMaximized() == False:
            if e.buttons() == Qt.LeftButton:
                self.move(self.pos() + e.globalPos() - self.oldPosition)
                self.oldPosition = e.globalPos()
                e.accept()


app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())
