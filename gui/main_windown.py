from PyQt6.QtWidgets import QApplication, QWidget, QPushButton , QVBoxLayout
import sys
from PyQt6.QtCore import QThread, QObject, pyqtSignal
import time




#CLASS FOR MAIN WINDOW OF UI

class mainWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.focus_thread : QThread | None = None
        self.focus_worker : QObject | None = None

        
        self.setWindowTitle("Blank Window")
        self.resize(800, 601)
        layout = QVBoxLayout()
        self.start_button = QPushButton("Start Focus Session")
        
        layout.addWidget(self.start_button)
        self.setLayout(layout)

        self.start_button.clicked.connect(self.start_session)



    def start_session(self):
            if self.focus_thread is not None and self.focus_thread.isRunning():
                return

            self.start_button.setEnabled(False)
            self.focus_thread  = QThread()
            self.focus_worker = focus_session_worker(duration_seconds= 5)

            self.focus_worker.moveToThread(self.focus_thread)

            self.focus_thread.started.connect(self.focus_worker.run)

            self.focus_worker.progess.connect(self.updated_countdown_label)
        

            self.focus_worker.finished.connect(self.focus_thread.quit)
            self.focus_worker.finished.connect(self.focus_worker.deleteLater)
            self.focus_thread.finished.connect(self.focus_thread.deleteLater)
            self.focus_worker.finished.connect(self.on_session_complete)
        
            self.focus_thread.start()


    def updated_countdown_label(self, remaining):
        mins, secs = divmod(remaining, 60)
        print(f"{mins:02d}:{secs:02d} remaining")

    def on_session_complete(self):
        print("25:00 mins")
        self.start_button.setEnabled(True)
        self.focus_thread.quit()
        self.focus_thread.wait()
        
        self.focus_thread = None
        self.focus_worker = None



#CLASS WHICH STARTS THE SESSION IN DIFFERENT THREAD THAN MAIN UI THREAD

class focus_session_worker(QObject):
    progess = pyqtSignal(int)
    finished = pyqtSignal()

    
    
    
    def __init__(self, duration_seconds: int = 1500):
        super().__init__()
        self.duration_seconds = duration_seconds
        self.is_running = True
       


    def run(self):
        for remaining in range(self.duration_seconds, 0 , -1):
            if not self.is_running:
                break
            self.progess.emit(remaining)
            time.sleep(1)
        self.finished.emit()

    def stop(self):
        self.is_running = False
    
    




#MAIN FUNCTION

def main():

    app = QApplication(sys.argv)

    main_win = mainWindow()

    main_win.show()
    sys.exit(app.exec())


if __name__=="__main__":
    main()
