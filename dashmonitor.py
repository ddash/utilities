from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt
import os

class Window(QtGui.QWidget):
    
    def __init__(self):
	self.ext_mon = ""
	self.main_mon = ""
	self.main_res = ""
	self.ext_res = ""
	self.main_present = 0
	self.ext_present = 0

        QtGui.QWidget.__init__(self)
        
        self.b1_auto = QtGui.QPushButton('Auto (reset)', self)
        self.b2_ext = QtGui.QPushButton('Ext only', self)
        self.b3_left = QtGui.QPushButton('EXT - MAIN', self)
        self.b4_right = QtGui.QPushButton('MAIN - EXT', self)
        self.b1_auto.clicked.connect(self.setauto)
        self.b2_ext.clicked.connect(self.setext)
        self.b3_left.clicked.connect(self.setleft)
        self.b4_right.clicked.connect(self.setright)
        
        self.setGeometry(300, 300, 280, 200)
        self.setWindowTitle("Setup Displays")
        self.refresh_mon()
        
        layout = QtGui.QVBoxLayout(self)
        layout.addWidget(self.b1_auto)
        layout.addWidget(self.b2_ext)
        layout.addWidget(self.b3_left)
        layout.addWidget(self.b4_right)

    def refresh_mon(self):
        lines = os.popen("xrandr -q").readlines()
        outputs = {}
        curr = ""
        for line in lines:
            if " connected" in line: # monitor
                curr = line.split()[0]
                outputs[curr] = []
            elif line.startswith(" " * 3): # resolution
                outputs[curr].append(line.split()[0])

        for item in outputs:
            if item == "eDP1":
                self.main_mon = item
                self.main_res = outputs[item][0]
                self.main_present = 1
            else:
                self.ext_mon = item
                self.ext_res = outputs[item][0]
                self.ext_present = 1

        if self.main_present == 0:
            os.system('notify-send "DISPLAY" "ERROR: No internal monitor found!!!"')
            sys.exit(1)
        #elif self.main_present == 1 and self.ext_present ==0: # reset only when no ext mon is connected
        else: # reset by default
            os.system("xrandr --auto")

    def setauto(self):
	os.system('notify-send "DISPLAY" "Automatic setup"')
        os.system("xrandr --output {0} --auto --output {1} --auto".format(self.main_mon, self.ext_mon))
        os.system("xrandr --output {0} --brightness 0.7".format(self.main_mon))

    def setext(self):
	os.system('notify-send "DISPLAY" "Enabling only external monitor"')
        os.system("xrandr --output {0} --off".format(self.main_mon))
        os.system("xrandr --output {0} --mode {1}".format(self.ext_mon, self.ext_res))
	
    def setleft(self):
	os.system('notify-send "DISPLAY" "EXT <-> MAIN"')
        os.system("xrandr --output {0} --mode {1} --output {2} --mode {3}".format(self.ext_mon, self.ext_res, self.main_mon, self.main_res))
        os.system("xrandr --output {0} --left-of {1}".format(self.ext_mon, self.main_mon))
        os.system("xrandr --output {0} --brightness 0.7".format(self.main_mon))
	
    def setright(self):
	os.system('notify-send "DISPLAY" "MAIN <-> EXT"')
        os.system("xrandr --output {0} --mode {1} --output {2} --mode {3}".format(self.ext_mon, self.ext_res, self.main_mon, self.main_res))
        os.system("xrandr --output {0} --right-of {1}".format(self.ext_mon, self.main_mon))
        os.system("xrandr --output {0} --brightness 0.7".format(self.main_mon))
	
if __name__ == '__main__':

    import sys
    app = QtGui.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
