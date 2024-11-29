import sys
import json
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLineEdit, QPushButton, QStyle, QTabWidget, QHBoxLayout, QSplitter, QMenu, QAction, QFileDialog, QCheckBox, QListWidget, QDialog
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEnginePage, QWebEngineDownloadItem
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtCore import QUrl, Qt, QFile, QSize, QObject, QEvent, QEventLoop, QRect, QCoreApplication, QPropertyAnimation
from PyQt5 import QtCore

class SimpleBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NV Browser")
        self.setGeometry(300, 300, 1000, 600)

        self.central_widget = QTabWidget()
        self.setCentralWidget(self.central_widget)

        self.main_layout = QHBoxLayout(self.central_widget)

        self.tabs = QTabWidget()
        self.tabs.setTabPosition(QTabWidget.West)
        self.tabs.setMovable(True)
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_current_tab)

        new_tab_button = QPushButton("+")
        new_tab_button.setObjectName("new_tab_button")  # Set object name for styling
        new_tab_button.clicked.connect(self.open_new_tab)
        new_tab_button.setFixedSize(25, 25)
        self.tabs.setCornerWidget(new_tab_button, Qt.TopLeftCorner)
        
        self.splitter = QSplitter(Qt.Horizontal)
        self.splitter.addWidget(self.tabs)

        self.main_layout.addWidget(self.splitter)

        self.load_tabs()

        self.apply_styles()

    def handle_download(self, download_item):
        filename, _ = QFileDialog.getSaveFileName(self, "Save File", "./Downloads", download_item.path())
        if filename:
            download_item.setPath(filename)
            download_item.accept()  # Accept the download request
            print(f"Downloaded: {filename}")

    def add_new_tab(self, qurl=None, lable="OpenTab"):
        if qurl is None:
            qurl = QUrl("https://www.google.com")

        browser = QWebEngineView()
        browser.setUrl(qurl)

        # Connect the downloadRequested signal to the handle_download method
        browser.page().profile().downloadRequested.connect(self.handle_download)

        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        nav_container = QWidget()
        nav_container.setFixedHeight(30)
        nav_layout = QHBoxLayout(nav_container)
        nav_layout.setContentsMargins(1, 1, 1, 1)
        nav_layout.setSpacing(1)

        back_button = QPushButton("<")
        back_button.clicked.connect(browser.back)
        back_button.setFixedSize(30, 25)

        forward_button = QPushButton(">")
        forward_button.clicked.connect(browser.forward)
        forward_button.setFixedSize(30, 25)

        refresh_button = QPushButton("⟳")
        refresh_button.clicked.connect(browser.reload)
        refresh_button.setFixedSize(30, 25)

        stop_button = QPushButton("⨯")
        stop_button.clicked.connect(browser.stop)
        stop_button.setFixedSize(30, 25)

        home_button = QPushButton("[-]")
        home_button.clicked.connect(lambda: browser.setUrl(QUrl("https://www.google.com")))
        home_button.setFixedSize(30, 25)

        url_bar = QLineEdit()
        url_bar.setPlaceholderText("Enter URL...")
        url_bar.returnPressed.connect(lambda: self.navigate_to_url(browser, url_bar))

        go_button = QPushButton("Go!")
        go_button.clicked.connect(lambda: self.navigate_to_url(browser, url_bar))
        go_button.setFixedSize(30, 25)

        nav_layout.addWidget(back_button)
        nav_layout.addWidget(forward_button)
        nav_layout.addWidget(url_bar, 1)
        nav_layout.addWidget(go_button)
        nav_layout.addWidget(refresh_button)
        nav_layout.addWidget(stop_button)
        nav_layout.addWidget(home_button)

        layout.addWidget(nav_container)
        layout.addWidget(browser, 1)

        i = self.tabs.addTab(container, lable)
        self.tabs.setCurrentIndex(i)

        browser.urlChanged.connect(lambda qurl, browser=browser: self.update_url_bar(qurl, browser))

    def navigate_to_url(self, browser, url_bar):
        url = url_bar.text()
        if not url.startswith("https://"):
            url = "https://" + url
        browser.setUrl(QUrl(url))

    def update_url_bar(self, q, browser=None):
        if browser != self.tabs.currentWidget().findChild(QWebEngineView):
            return
        url_bar = self.tabs.currentWidget().findChild(QLineEdit)
        if url_bar:
            url_bar.setText(q.toString())
            url_bar.setCursorPosition(0)

    def close_current_tab(self, index):
        if self.tabs.count() > 1:
            self.tabs.removeTab(index)

    def open_new_tab(self):
        self.add_new_tab(QUrl("https://www.google.com"), "New Tab")

    def apply_styles(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #b1b3b5;
                border-radius: 10px;
            }
            QLineEdit {
                padding: 2px 4px;
                font-size: 16px;
                border: 3px solid #9c27cf;
                border-radius: 10px;
                margin: px;
            }
            
            QPushButton {
                padding: 2px 4px;
                font-size: 12px;
                background-color: #9c27cf;
                color: white;
                border: none;
                border-radius: 10px;
                margin: 0px;
            }
                           
            QPushButton:hover {
                background-color: #b1b3b5;
            }
                           
            QTabWidet::pane{
                border: 1px #9c27cf;
                background: white;        
            }
            
            QTabWidget::tab-bar:left {
                left: 0px;
                top: 12px;
            }
                           
            QTabBar::tab {
                background: #d1d3d5;
                border: 2px solid #9c27cf;
                padding: 5px;
                min-width: 20px;
                max-width: 150px;
                border-radius: 10px;
            }

            QTabBar::tab:selected {
                background: white;
            }

            QPushButton#new_tab_button {
                background-color: transparent;
                border: none;
                color: #9c27cf;
                font-weight: bold;
                font-size: 20px;
                padding: 0px;
                margin: 0px;
                left: 10px;
                top: 10px;
            }
            QPushButton#new_tab_button:hover {
            color: #b1b3b5;
            }
        """)

    def closeEvent(self, event):
        self.save_tabs()
        event.accept()

    def save_tabs(self):
        urls = []
        for i in range(self.tabs.count()):
            container = self.tabs.widget(i)
            browser = container.findChild(QWebEngineView)
            if browser:
                urls.append(browser.url().toString())
        with open("tabs.json", "w") as file:
            json.dump(urls, file)

    def load_tabs(self):
        try:
            with open("tabs.json", "r") as file:
                urls = json.load(file)
                for url in urls:
                    self.add_new_tab(QUrl(url), "Restored Tab")
        except FileNotFoundError:
            self.add_new_tab(QUrl("https://www.google.com"), "New Tab")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    browser = SimpleBrowser()
    browser.show()
    sys.exit(app.exec_())