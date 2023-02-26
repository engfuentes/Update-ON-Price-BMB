import sys
import logging
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QTextEdit, QVBoxLayout
from PyQt6.QtCore import QObject, pyqtSignal, QThread
from PyQt6.QtGui import QIcon
import main

logging.basicConfig(
        #filename="logs.log",
        encoding="utf-8",
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )

logger = logging.getLogger('app')
logger.info(f"Starting the app")

class ConsoleWindowLogHandler(logging.Handler, QObject):
    sigLog = pyqtSignal(str)

    def __init__(self):
        logging.Handler.__init__(self)
        QObject.__init__(self)

    def emit(self, logRecord):
        msg = str(logRecord.getMessage())
        self.sigLog.emit(msg)


class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        
        # Window Properties
        self.setWindowTitle("ONs Price Updater")
        self.setWindowIcon(QIcon('icon.ico'))
        self.resize(600, 600) # width, height

        # Widgets
        self.button = QPushButton('&Update Google Sheet')
        logTextBox = QTextEdit()
        logTextBox.setReadOnly(True)
        
        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.button)
        layout.addWidget(logTextBox)
        self.setLayout(layout)

        # Connect button
        self.button.clicked.connect(self.buttonPressed)

        # Thread
        self.bee = Worker(self.runScript,())
        self.bee.finished.connect(self.restoreUi)
        self.bee.terminate()
    
        # Console handler
        consoleHandler = ConsoleWindowLogHandler()
        consoleHandler.sigLog.connect(logTextBox.append)
        logger.addHandler(consoleHandler)
    
    def buttonPressed(self):
        self.button.setEnabled(False)
        self.bee.start()
        
    def restoreUi(self):
        self.button.setEnabled(True)

    def runScript(self):
        main.main()

class Worker(QThread):
    def __init__(self, func, args):
        super(Worker, self).__init__()
        self.func = func
        self.args = args

    def run(self):
        self.func(*self.args)

app = QApplication(sys.argv) # If we use arguments in the command line
app.setStyleSheet('''
    QWidget {
        font-size: 20px;
    }
    
    QPushButton {
        font-size: 20px;
    }''') # Apply css 


window = MyApp()
window. show()

sys.exit(app.exec())