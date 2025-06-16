import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLineEdit, QPushButton,
    QVBoxLayout, QWidget, QHBoxLayout, QSizePolicy,
    QTabBar, QLabel, QToolButton, QMenu,
    QDialog, QInputDialog, QTextEdit, QMessageBox,
    QShortcut, QSlider
)
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, Qt, QPoint, QEvent
from PyQt5.QtGui import QKeySequence, QMovie, QIntValidator, QFont, QIcon

class MemonBrowser(QMainWindow):
    MAX_TABS = 25

    def __init__(self):
        super().__init__()

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("background-color: white;")
        self.setWindowTitle("Memon Browser")
        self.showMaximized()

        # --- Web view ---
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("https://www.google.com"))
        self.browser.loadStarted.connect(self.start_loading)
        self.browser.loadFinished.connect(self.stop_loading)
        self.browser.titleChanged.connect(self.update_tab_title)
        self.browser.setZoomFactor(0.85)

        # --- Search Box ---
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Enter URL or search query")
        self.search_box.returnPressed.connect(self.load_url)
        self.search_box.setFixedSize(600, 30)
        self.search_box.setStyleSheet("""
            QLineEdit {
                border-radius: 10px;
                padding-left: 35px;  /* space for spinner */
                font-size: 14px;
                border: 1px solid #ccc;
            }
        """)

        # --- Loading spinner label ---
        self.spinner_label = QLabel(self.search_box)
        self.spinner_label.setFixedSize(20, 20)
        self.spinner_label.move(7, 5)  # inside search box
        # self.spinner_label.hide()

        # Use your own spinner.gif here or comment these lines to disable spinner
        self.spinner_movie = QMovie("spinner.gif")
        self.spinner_label.setMovie(self.spinner_movie)

        # --- Back and Forward Buttons ---
        self.back_button = QPushButton("◀")
        self.back_button.setFixedSize(30, 30)
        self.back_button.clicked.connect(self.browser.back)
        self.forward_button = QPushButton("▶")
        self.forward_button.setFixedSize(30, 30)
        self.forward_button.clicked.connect(self.browser.forward)

        # --- Custom Window Control Buttons ---
        self.min_button = QPushButton("➖")
        self.max_button = QPushButton("⬜")
        self.close_button = QPushButton("❌")

        for btn in [self.min_button, self.max_button, self.close_button]:
            btn.setFixedSize(30, 30)
            btn.setStyleSheet("""
                QPushButton {
                    border: none;
                    background-color: #eee;
                    border-radius: 10px;
                    font-size: 14px;
                }
                QPushButton:hover {
                    background-color: #ccc;
                }
            """)

        self.min_button.clicked.connect(self.showMinimized)
        self.max_button.clicked.connect(self.toggle_max_restore)
        self.close_button.clicked.connect(self.close)

        # Track URLs for tabs
        self.tabs = ["https://www.google.com"]
        self.current_tab_index = 0

        # --- Tab bar with manual add button ---
        self.tab_bar = QTabBar()
        self.tab_bar.setExpanding(False)
        self.tab_bar.setTabsClosable(True)
        self.tab_bar.tabCloseRequested.connect(self.close_tab)
        self.tab_bar.currentChanged.connect(self.switch_tab)

        # Start with exactly one tab
        self.tab_bar.addTab("Tab 1")
        self.load_tab(0)

        # "New Tab" button next to tab bar
        self.new_tab_btn = QToolButton()
        self.new_tab_btn.setText("+")
        self.new_tab_btn.setFixedSize(30, 30)
        self.new_tab_btn.clicked.connect(self.add_new_tab)
        self.new_tab_btn.setStyleSheet("""
            QToolButton {
                font-size: 18px;
                background-color: #ddd;
                border-radius: 5px;
            }
            QToolButton:hover {
                background-color: #bbb;
            }
        """)

        # --- Settings button to the left of tabs ---
        self.settings_button = QToolButton()
        self.settings_button.setText("☰")
        self.settings_button.setFixedSize(30, 30)
        self.settings_button.setToolTip("Settings")
        self.settings_button.setStyleSheet("""
            QToolButton {
                font-size: 18px;
                background-color: #ddd;
                border-radius: 5px;
                border: none;
            }
            QToolButton:hover {
                background-color: #bbb;
            }
        """)
        self.settings_button.setPopupMode(QToolButton.InstantPopup)  # Show menu on click

        # Create the settings menu
        self.settings_menu = QMenu()
        self.settings_menu.addAction("Zoom", self.open_zoom_menu)
        self.settings_menu.addSeparator()
        self.settings_menu.addAction("Find on Page", self.show_find_dialog)
        self.settings_menu.addAction("Bookmarks List", self.show_bookmarks_list)
        self.settings_menu.addAction("Settings", self.show_settings_page)
        self.settings_menu.addAction("About", self.show_about_dialog)
        self.settings_button.setMenu(self.settings_menu)
        self.settings_button.clicked.connect(self.open_zoom_menu)

        # --- Layout for tabs + settings + new tab button ---
        tab_layout = QHBoxLayout()
        tab_layout.setContentsMargins(0, 0, 0, 0)
        tab_layout.addWidget(self.settings_button)
        tab_layout.addStretch()              # push tabs to center
        tab_layout.addWidget(self.tab_bar)
        tab_layout.addStretch()              # push new tab button right
        tab_layout.addWidget(self.new_tab_btn)

        tab_container = QWidget()
        tab_container.setLayout(tab_layout)
        tab_container.setFixedHeight(35)

        # --- Layout for window controls (right) ---
        window_controls_layout = QHBoxLayout()
        window_controls_layout.setSpacing(5)
        window_controls_layout.addWidget(self.min_button)
        window_controls_layout.addWidget(self.max_button)
        window_controls_layout.addWidget(self.close_button)

        # --- Layout for navigation buttons (left) ---
        nav_buttons_layout = QHBoxLayout()
        nav_buttons_layout.setSpacing(5)
        nav_buttons_layout.addWidget(self.back_button)
        nav_buttons_layout.addWidget(self.forward_button)

        # Spacers for centering search box
        left_spacer = QWidget()
        left_spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        right_spacer = QWidget()
        right_spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        # Bookmarks stored as a set for quick lookup
        self.bookmarks = set()

        # Bookmark button setup (unchanged except for initial icon)
        self.bookmark_button = QPushButton("☆")  # Start unfilled star
        self.bookmark_button.setFixedSize(30, 30)
        self.bookmark_button.setToolTip("Bookmark this page")
        self.bookmark_button.setStyleSheet("""
            QPushButton {
                font-size: 18px;
                background-color: #ddd;
                border-radius: 5px;
                border: none;
            }
            QPushButton:hover {
                background-color: #bbb;
            }
        """)
        self.bookmark_button.clicked.connect(self.toggle_bookmark)
        # Also update bookmark icon whenever URL changes
        self.browser.urlChanged.connect(self.update_bookmark_icon)

        # --- Top bar layout ---
        top_bar_layout = QHBoxLayout()
        top_bar_layout.setContentsMargins(10, 10, 10, 10)
        top_bar_layout.setSpacing(15)
        top_bar_layout.addLayout(nav_buttons_layout)
        top_bar_layout.addWidget(left_spacer)
        top_bar_layout.addWidget(self.search_box)
        top_bar_layout.addWidget(self.bookmark_button)  # This is the line you need to add
        top_bar_layout.addWidget(right_spacer)
        top_bar_layout.addLayout(window_controls_layout)

        # Top bar container
        top_bar_container = QWidget()
        top_bar_container.setLayout(top_bar_layout)
        top_bar_container.setStyleSheet("""
            background-color: #f0f0f0;
            border-radius: 10px;
        """)
        top_bar_container.setFixedHeight(50)

        # --- Main layout ---
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(5)
        main_layout.addWidget(top_bar_container)
        main_layout.addWidget(self.browser)
        main_layout.addWidget(tab_container)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # --- For dragging window ---
        self.oldPos = self.pos()
        top_bar_container.mousePressEvent = self.mouse_press_event
        top_bar_container.mouseMoveEvent = self.mouse_move_event

        self.is_maximized = True

        # Zoom factor default
        self.zoom_factor = 1.0

        # Shortcut for closing tab: Ctrl+W
        self.close_tab_shortcut = QShortcut(QKeySequence("Ctrl+W"), self)
        self.close_tab_shortcut.activated.connect(self.close_current_tab)

    # Call this when bookmark button clicked
    def toggle_bookmark(self):
        url = self.search_box.text().strip()
        if url in self.bookmarks:
            self.bookmarks.remove(url)
            self.bookmark_button.setText("☆")
            print(f"Removed bookmark: {url}")
        else:
            self.bookmarks.add(url)
            self.bookmark_button.setText("★")
            print(f"Added bookmark: {url}")

    # Update star icon depending on whether current URL is bookmarked
    def update_bookmark_icon(self):
        url = self.browser.url().toString()
        self.search_box.setText(url)  # keep search box updated

        if url in self.bookmarks:
            self.bookmark_button.setText("★")
        else:
            self.bookmark_button.setText("☆")

    def open_zoom_menu(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Zoom")
        dialog.setFixedSize(300, 90)
        dialog.setWindowFlags(dialog.windowFlags() & ~Qt.WindowContextHelpButtonHint)  # Remove '?'

        # 🔍 Set the Zoom-In icon (update the path as needed)
        dialog.setWindowIcon(QIcon("zoom-in.png"))

        font = QFont("Calibri", 12, QFont.Bold)

        layout = QVBoxLayout()

        zoom_label = QLabel()
        zoom_label.setFont(font)

        zoom_slider = QSlider(Qt.Horizontal)
        zoom_slider.setRange(25, 500)
        zoom_slider.setValue(int(self.browser.zoomFactor() * 100))
        zoom_slider.setTickPosition(QSlider.TicksBelow)
        zoom_slider.setTickInterval(25)
        zoom_slider.setFont(font)

        def update_zoom_label_and_apply(value):
            zoom_label.setText(f"Zoom: {value}%")
            self.browser.setZoomFactor(value / 100)  # Apply zoom live

        zoom_slider.valueChanged.connect(update_zoom_label_and_apply)
        update_zoom_label_and_apply(zoom_slider.value())  # Set initial label text and zoom

        layout.addWidget(zoom_label)
        layout.addWidget(zoom_slider)

        dialog.setLayout(layout)
        dialog.exec_()

    def close_current_tab(self):
        index = self.tab_bar.currentIndex()
        if index != -1:
            self.close_tab(index)

    # Update the current tab text to the new title
    def update_tab_title(self, title):
        current_index = self.tab_bar.currentIndex()
        if current_index >= 0:
            self.tab_bar.setTabText(current_index, title)

    def load_url(self):
        text = self.search_box.text().strip()
        if "." in text or text.startswith("http"):
            url = text if text.startswith("http") else "http://" + text
        else:
            url = f"https://www.google.com/search?q={text}"
        self.browser.setUrl(QUrl(url))
        self.tabs[self.current_tab_index] = url

    def toggle_max_restore(self):
        if self.is_maximized:
            self.showNormal()
            self.is_maximized = False
        else:
            self.showMaximized()
            self.is_maximized = True

    def mouse_press_event(self, event):
        self.oldPos = event.globalPos()

    def mouse_move_event(self, event):
        delta = QPoint(event.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()

    def add_new_tab(self):
        if self.tab_bar.count() >= self.MAX_TABS:
            msg_box = QMessageBox(self)
            # msg_box.setIcon(QMessageBox.Warning)
            msg_box.setWindowTitle("Tab Limit Reached")
            msg_box.setText(f"Maximum of {self.MAX_TABS} tabs reached!")

            msg_box.setWindowIcon(QIcon("warning.png"))
            # Set custom font for the whole message box
            msg_font = QFont("Calibri", 12)
            msg_box.setFont(msg_font)

            # Add custom OK button
            ok_button = msg_box.addButton(QMessageBox.Ok)
            ok_button.setFont(QFont("Calibri", 12, QFont.Bold))
            ok_button.setFlat(True)
            ok_button.setStyleSheet("""
                QPushButton {
                    background-color: #0078d7;
                    color: white;
                    border: none;
                    border-radius: 12px;
                    padding: 6px 12px;
                }
                QPushButton:hover {
                    background-color: #005a9e;
                }
            """)

            msg_box.exec_()
            return

        new_index = self.tab_bar.addTab(f"Tab {self.tab_bar.count() + 1}")
        self.tabs.append("https://www.google.com")
        self.tab_bar.setCurrentIndex(new_index)

    def close_tab(self, index):
        self.tab_bar.removeTab(index)
        del self.tabs[index]

        if self.tab_bar.count() == 0:
            self.close()  # Close the whole browser if no tabs left
            return

        if self.current_tab_index >= self.tab_bar.count():
            self.current_tab_index = self.tab_bar.count() - 1

        self.load_tab(self.current_tab_index)

    def switch_tab(self, index):
        if index < 0 or index >= len(self.tabs):
            return
        self.current_tab_index = index
        self.load_tab(index)

    def load_tab(self, index):
        url = self.tabs[index]
        self.browser.setUrl(QUrl(url))
        self.search_box.setText(url)

    def start_loading(self):
        self.spinner_label.show()
        self.spinner_movie.start()

    def stop_loading(self, ok):
        self.spinner_movie.stop()
        self.spinner_label.hide()

    # --- Settings menu actions ---
    def set_zoom(self, factor):
        factor = max(0.25, min(factor, 5.0))
        self.zoom_factor = factor
        self.browser.setZoomFactor(factor)

    def show_find_dialog(self):
        text, ok = QInputDialog.getText(self, "Find on Page", "Enter text to find:")
        if ok and text:
            self.browser.findText("", QWebEngineView.FindFlag(0))  # clear previous highlights
            self.browser.findText(text)

    def show_bookmarks_list(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Bookmarks List")
        dialog.setMinimumSize(400, 300)

        text_edit = QTextEdit()
        text_edit.setReadOnly(True)
        if self.bookmarks:
            text_edit.setPlainText("\n".join(sorted(self.bookmarks)))
        else:
            text_edit.setPlainText("No bookmarks yet.")

        layout = QVBoxLayout()
        layout.addWidget(text_edit)
        dialog.setLayout(layout)
        dialog.exec_()

    def show_settings_page(self):
        QMessageBox.information(self, "Settings", "Settings page is under construction.")

    def show_about_dialog(self):
        about_box = QMessageBox(self)
        about_box.setWindowTitle("About")
        about_box.setIcon(QMessageBox.Information)

        # Set custom font and formatting
        font = QFont("Calibri", 13)
        about_box.setFont(font)

        # Set styled, centered text with Safari-like line spacing
        about_box.setTextFormat(Qt.RichText)
        about_box.setText(
            "<div style='text-align: center;'>"
            "<h2 style='margin-bottom: 4px;'>Memon Browser</h2>"
            "<p style='margin: 0; font-size: 12pt;'>Version 1.0</p>"
            "<p style='margin: 10px 0;'>A simple PyQt5-based browser.</p>"
            "<p style='font-size: 11pt;'>Developed with ❤️ by you!</p>"
            "</div>"
        )

        # Add custom OK button
        ok_button = about_box.addButton(QMessageBox.Ok)
        ok_button.setFont(QFont("Calibri", 13, QFont.Bold))
        ok_button.setFlat(True)
        ok_button.setStyleSheet("""
            QPushButton {
                background-color: #0078d7;
                color: white;
                border: none;
                border-radius: 12px;
                padding: 6px 16px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #005a9e;
            }
        """)

        # Optional: Set window icon if you have one
        # about_box.setWindowIcon(QIcon("icons/browser_icon.png"))

        about_box.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MemonBrowser()
    window.show()
    sys.exit(app.exec_())