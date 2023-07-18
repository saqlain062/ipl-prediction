from ipl import *
import DataBase 
from PyQt6.QtGui import QPixmap
import sys
from PyQt6.QtWidgets import (QWidget,QMainWindow,QComboBox,QMessageBox, QPushButton,
 QApplication, QLabel, QFormLayout,QSpinBox, QLineEdit, QSplashScreen, QSpinBox )
from PyQt6.QtGui import QFont,QPixmap,QAction
from PyQt6.QtCore import Qt,QTimer
import matplotlib
matplotlib.use('QtAgg')
from PyQt6 import QtWidgets,QtGui
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)
    # plt.figure(figsize=(18,8))
    # plt.plot(temp_df['end_of_over'],temp_df['wickets_in_over'],color='yellow',linewidth=3)
    # plt.plot(temp_df['end_of_over'],temp_df['win'],color='#00a65a',linewidth=4)
    # plt.plot(temp_df['end_of_over'],temp_df['lose'],color='red',linewidth=4)
    # plt.bar(temp_df['end_of_over'],temp_df['runs_after_over'])
    # plt.title('Target-' + str(target))
    # #plt.show()

class AnotherWindow(QWidget):
    def __init__(self,):
        super().__init__()
        form = QWidget()
        self.setWindowTitle("IPL PREDICTION")
        self.layout = QFormLayout(form)

        self.batting_team = QComboBox()
        self.batting_team.addItems(['Rajasthan Royals','Kolkata Knight Riders','Delhi Daredevils',
        'Royal Challengers Bangalore','Deccan Chargers','Mumbai Indians',
        'Kings XI Punjab','Chennai Super Kings','Pune Warriors','Gujarat Lions',
        'Sunrisers Hyderabad','Rising Pune Supergiant','Delhi Capitals',
        'Kochi Tuskers Kerala','Rising Pune Supergiants'])
        self.bowling_team = QComboBox()
        self.bowling_team.addItems(['Kings XI Punjab','Royal Challengers Bangalore','Rajasthan Royals',
        'Kochi Tuskers Kerala','Deccan Chargers','Chennai Super Kings',
        'Pune Warriors','Kolkata Knight Riders','Sunrisers Hyderabad',
        'Mumbai Indians','Delhi Daredevils','Rising Pune Supergiants',
        'Gujarat Lions','Delhi Capitals','Rising Pune Supergiant'])
        self.city = QComboBox()
        self.city.addItems(['Chennai','East London','Delhi','Kolkata','Chandigarh','Mohali',
        'Bengaluru','Ranchi','Jaipur','Durban','Mumbai','Hyderabad','Raipur',
        'Rajkot','Johannesburg','Bangalore','Ahmedabad','Centurion','Kimberley',
        'Kochi','Cuttack','Visakhapatnam','Pune', 'Nagpur','Abu Dhabi','Cape Town',
        'Indore','Kanpur','Bloemfontein','Dharamsala','Port Elizabeth','Sharjah'])
        
        # self.target = QLineEdit()
        self.target = QSpinBox(form,minimum=50, maximum =250)
        # self.target.setPlaceholderText("target")
        #self.score = QLineEdit()
        self.score = QSpinBox(form,minimum=1, maximum=200)
        self.over = QSpinBox(form,minimum=1, maximum=20)
        self.wickets = QSpinBox(form,minimum=0, maximum=10)
        self.w =QLabel()
        self.l = QLabel()
        self.w.setText("")
        self.l.setText("")
        self.w.setFont(QFont("Arial",20))
        self.l.setFont(QFont("Arial",20))

        self.layout.addWidget(self.batting_team)
        self.layout.addWidget(self.bowling_team)
        self.layout.addWidget(self.city)
        self.layout.addRow("Target",self.target)
        self.layout.addRow("Score",self.score)
        self.layout.addRow("Over",self.over)
        self.layout.addRow("Wickets",self.wickets)
        self.layout.addRow(self.w)
        self.layout.addRow(self.l)

        self.button = QPushButton("Predict Proboability")
        self.button.move(10,10)
        self.layout.addWidget(self.button)
        self.button1 = QPushButton("Clear Input")
        self.button1.move(20,20)
        self.layout.addWidget(self.button1)
        self.button.clicked.connect(self.Data)
        self.button1.clicked.connect(self.reset)
        self.setLayout(self.layout)


    def Data(self):
        tar = self.target.text() 
        scr = self.score.text()
        ovr = self.over.text()
        wik = self.wickets.text()
        bat = self.batting_team.currentText()
        bol = self.bowling_team.currentText()
        cit = self.city.currentText()
        # print(cit)
        runs_l = int(tar) - int(scr)
        ball_l = 120 - (int(ovr)*6)
        wick = 10 - int(wik)
        crr = int(scr)/int(ovr)
        rrr = (int(runs_l)*6)/int(ball_l)
        input_df = pd.DataFrame({'batting_team':[bat],'bowling_team':[bol],'city':[cit],'runs_left':[runs_l],
                                'balls_left':[ball_l],'wickets':[wick],'total_runs_x':[tar],'crr':[crr],'rrr':[rrr]})
        # print(input_df)
        # self.table.setHorizontalHeaderLabels(input_df[0].keys())
        # self.table.setRowCount(len(input_df))
        r = pipe.predict_proba(input_df)
        # print(r)
        loss = r[0][0]
        print(loss)
        win = r[0][1]
        print(win)
        lr = "Lining Rate "+bat+"="+str(round(win*100))+"%"
        wr = "Wining Rate "+bol+'='+str(round(loss*100))+'%'
        print(lr)
        print(wr)
        self.w.setText(f"<b>{wr}</b>")
        self.l.setText(f"<b>{lr}</b>")
        
        # print("lossing Rate",bat+'-'+str(round(win*100))+"%")
        # print("Wining Rate",bol+'-'+str(round(loss*100))+ '%')

    def delete(self):
        current_row = self.table.currentRow()
        if current_row < 0:
            return QMessageBox.warning(self, 'Warning','Please select a record to delete')

        button = QMessageBox.question(
            self,
            'Confirmation',
            'Are you sure that you want to delete the selected row?',
            QMessageBox.StandardButton.Yes |
            QMessageBox.StandardButton.No
        )
        if button == QMessageBox.StandardButton.Yes:
            self.table.removeRow(current_row)
    def valid(self):
        first_name = self.first_name.text().strip()
        last_name = self.last_name.text().strip()

        
        if not first_name:
            QMessageBox.critical(self, 'Error', 'Please enter the first name')
            self.first_name.setFocus()
            return False

        if not last_name:
            QMessageBox.critical(self, 'Error', 'Please enter the last name')
            self.last_name.setFocus()
            return False

        try:
            age = int(self.age.text().strip())
        except ValueError:
            QMessageBox.critical(self, 'Error', 'Please enter a valid age')
            self.age.setFocus()
            return False

        if age <= 0 or age >= 67:
            QMessageBox.critical(
                self, 'Error', 'The valid age is between 1 and 67')
            return False

        return True
    def reset(self):
        self.target.clear() 
        self.score.clear()
        self.over.clear()
        self.wickets.clear()
        self.l.clear()

        self.w.clear()

class MWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MWindow, self).__init__(*args, **kwargs)

        # Create the maptlotlib FigureCanvas object,
        # which defines a single set of axes as self.axes.
        sc = MplCanvas(self, width=5, height=4, dpi=100)
        sc.axes.plot(temp_df['end_of_over'],temp_df['wickets_in_over'],color='yellow',linewidth=3)
        sc.axes.plot(temp_df['end_of_over'],temp_df['win'],color='#00a65a',linewidth=4)
        sc.axes.plot(temp_df['end_of_over'],temp_df['lose'],color='red',linewidth=4)
        sc.axes.bar(temp_df['end_of_over'],temp_df['runs_after_over'])
        sc.axes.set_title("Target+"+str(target))
        # Create toolbar, passing canvas as first parament, parent (self, the MainWindow) as second.
        toolbar = NavigationToolbar(sc, self)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(toolbar)
        layout.addWidget(sc)

        # Create a placeholder widget to hold our toolbar and canvas.
        widget = QtWidgets.QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.show()
class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Window")
        self.setGeometry(200,200,200,200)



        font = QtGui.QFont()
        font.setFamily('Times')
        font.setBold(True)
        font.setPointSize(40)
        
        self.label = QLabel(self)
        self.setCentralWidget(self.label)
        filepath = "image1.jpg"
        pixmap = QPixmap(filepath)
        self.label.setPixmap(pixmap)
        self.label.setScaledContents(True)
        
        
        # add other widgets to the window
        # self.label = QLabel("Welcome to my application!", self)
        # self.label.setFont(font)
        # self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        menubar = self.menuBar()

        file1 = menubar.addMenu("File")
        file2 = menubar.addMenu("Data")

        view = QAction("View",self)
        new = QAction("Prediction",self)
        gr = QAction("Graph",self)
        data = QAction("Data Insertion",self)
        
        # file1.addAction(view)
        file1.addAction(new)
        file1.addAction(gr)
        file2.addAction(data)

        data.triggered.connect(self.viewData)
        new.triggered.connect(self.show_new_window)
        gr.triggered.connect(self.showGraph)
    

    def show_new_window(self, checked):
            self.w = AnotherWindow()
            self.w.show()
            #self.w.close()
    def showGraph(self):
        self.w1 = MWindow()
        # self.w.show()

    def viewData(self):
        self.w2 = DataBase.MainWindow()
        self.w2.show()

app = QApplication([])
app1 = QtWidgets.QApplication(sys.argv)
# Create the splash screen
# pixmap = QPixmap("image2.png")
# splash = QSplashScreen(pixmap, Qt.WindowStaysOnTopHint)
# splash.show()


window = MainWindow()
# window.splash = splash
window.show()
sys.exit(app.exec())


