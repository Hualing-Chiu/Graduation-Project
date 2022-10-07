from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox
from Brainwave_UI_MainWindow import Ui_MainWindow
from PyQt5.QtCore import QCoreApplication
import sys
import data_load_and_preprocessing
import UI_mode1
import UI_mode2
import UI_mode3
# from PyQt5 import QMessageBox
class MainWindow(QtWidgets.QMainWindow):
  def __init__(self,all_data,percentile_256,epoch_leng,music_list):
    # in python3, super(Class, self).xxx = super().xxx
    super(MainWindow, self).__init__()
    self.ui = Ui_MainWindow()
    self.ui.setupUi(self)
    self.all_data=all_data
    self.percentile_256=percentile_256
    self.epoch_leng=epoch_leng
    self.music_list=music_list
    self.band_list=['alpha','beta','delta','gamma','theta']
    self.setup_control()
  def setup_control(self):
    # TODO

    self.ui.pushButton.clicked.connect(self.start_click)
    self.ui.pushButton_2.clicked.connect(self.help_click)
    self.now_music = self.ui.comboBox.currentText()
    self.ui.comboBox.currentIndexChanged.connect(self.change_music_combobox)

    self.now_UI_mode=self.ui.comboBox_2.currentText()
    self.ui.comboBox_2.currentIndexChanged.connect(self.change_UI_mode_combobox)

    return

  def start_click(self):
    # print(self.now_UI_mode)
    if self.now_UI_mode=="Mode 1":
      music_string_lst=self.now_music.split(".")
      music_string=music_string_lst[0]
      idx=self.band_list.index(music_string)
      UI_mode1.run(self.all_data[idx],self.percentile_256,self.epoch_leng,music_string)
    elif self.now_UI_mode=="Mode 2":
      music_string_lst=self.now_music.split(".")
      music_string=music_string_lst[0]
      idx=self.band_list.index(music_string)
      UI_mode2.run(self.all_data[idx],self.percentile_256,self.epoch_leng,music_string)
    elif self.now_UI_mode=="Mode 3":
      music_string_lst=self.now_music.split(".")
      music_string=music_string_lst[0]
      idx=self.band_list.index(music_string)
      UI_mode3.run(self.all_data,self.percentile_256,self.epoch_leng,music_string,idx)


      return

  def help_click(self):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle('User\'s guide')
        msg_box.setText(f"Welcome to \"Brainwave UI\".\nThere are three display modes for you to choose from.")
        user_guide_msg=f"全部模式都可按空白鍵暫停，按q退出介面\n\nMode1:\n按0進入子模式0(預設子模式)，左右鍵切換欲觀察的受試者\n按1進入子模式1，左右鍵同子模式0，上下鍵可切換欲觀察的通道\n\n"
        user_guide_msg+=f"Mode2:\n上下鍵切換不同組受試者\n左右鍵切換欲觀察的band\n\n"
        user_guide_msg+=f"Mode3:\n預設模式:上下鍵切換欲觀察的受試者\n左右鍵切換欲觀察的band\n按A進入觀察所有人的子觀察模式\n在這個子模式中左右鍵作用同預設模式\n上下鍵切回預設模式\n\n"
        msg_box.setInformativeText(user_guide_msg)

                 
        # msg_box.setDetailedText(
        #     'Follow our Bucketing page, and learn more'
        #     'about PySide2, Java, Design pattern!\n'
        #     'Enjoy!')
        msg_box.setStyleSheet("min-width:800 px;min-height:200 px; font-size: 20px; font-size:30px; background-color: rgb(0,0,0);color: rgb(255,255,255);")
        msg_box.addButton('OK',QMessageBox.AcceptRole)
        msg_box.show()


  def change_music_combobox(self):
    self.now_music = self.ui.comboBox.currentText()
    

  def change_UI_mode_combobox(self):
    self.now_UI_mode=self.ui.comboBox_2.currentText()


if __name__ == '__main__':
  app = QtWidgets.QApplication(sys.argv)
  all_data,percentile_256,epoch_leng,music_list=data_load_and_preprocessing.get_avg()
  window = MainWindow(all_data,percentile_256,epoch_leng,music_list)
  window.show()
  sys.exit(app.exec_())