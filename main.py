# main.py
import sys
import os
import subprocess
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl,pyqtSlot, QObject,pyqtSignal
from PyQt5.QtWebChannel import QWebChannel

class Backend(QObject):
    sendMessageToJS = pyqtSignal(str)
    @pyqtSlot(float, float)
    def receiveCenter(self, lon, lat):
        print(f"Map center is at Longitude: {lon}, Latitude: {lat}")
        self.sendMessageToJS.emit(f"New center coordinates: Longitude {lon}, Latitude {lat}")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('OpenLayers in PyQt')
        self.setGeometry(100, 100, 800, 600)

        self.browser = QWebEngineView()

        # Start the local server
        self.server_process = subprocess.Popen([sys.executable, 'run_server.py'], cwd=os.path.dirname(os.path.abspath(__file__)))

        # Set the URL to load the map
        self.browser.setUrl(QUrl("http://localhost:8000/map/map.html"))
        self.setCentralWidget(self.browser)

        self.channel = QWebChannel()
        self.backend = Backend()
        self.channel.registerObject('pyjs', self.backend)
        self.browser.page().setWebChannel(self.channel)

    def closeEvent(self, event):
        # Kill the server process when closing the application
        self.server_process.terminate()
        self.server_process.wait()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
