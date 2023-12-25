# coding = utf-8
 
from PyQt5 import QtCore,QtGui,QtWidgets
import sys
 
class MainUi(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainUi,self).__init__()
        self.init_ui()
 
    def init_ui(self):
        # 创建一个窗口 基础大小为960x700，最小大小为200x200，最大大小为1800x1400，网格布局
        self.setFixedSize(200,200)
        self.setMinimumSize(200, 200)
        self.setMaximumSize(200, 200)
        self.main_widget = QtWidgets.QWidget()  # 创建窗口主部件

        self.main_layout = QtWidgets.QGridLayout()  # 创建主部件的网格布局

        self.main_widget.setLayout(self.main_layout)  # 设置窗口主部件布局为网格布局

        
        self.setCentralWidget(self.main_widget) # 设置窗口主部件
 
def main():
    app = QtWidgets.QApplication(sys.argv)
    gui = MainUi()
    gui.show()
    sys.exit(app.exec_())
 
if __name__ == '__main__':
    main()