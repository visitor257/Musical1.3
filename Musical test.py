import sys
import time

from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtMultimedia import QSound
import ctypes
import os
import media_tool
from pydub import AudioSegment
import shutil


class Tray(QSystemTrayIcon, QMainWindow):
    def __init__(self):
        super().__init__()
        self.chenum = 0
        self.setup()
        self.show()

    def setup(self):
        print("1")
        self.mutime=0
        QMessageBox.about(self, "Musical", "Welcome to use Musical\n(Press [OK] to continue)")
        self.timetowait = 1000 * 3
        if self.chenum == 0:
            self.num4 = 0
        else:
            self.num4 = 1
        self.show1 = ""
        self.menulist = []
        self.word = "▶    Play"
        self.add_music()
        # self.index=0
        # self.tips=['M','Mu','Mus','Musi',"Music"]
        self.icon = QIcon("icons/1.png")
        self.setIcon(self.icon)
        self.setToolTip("Musical\nNow playing: %s" % self.musicname[0])
        self.activated.connect(self.process)
        # self.s=QSound("sound1.wav")
        # self.s2=QSound("sound2.wav")
        # self.ic=QIcon("icons/stand.png")
        self.mu = QSound(self.musicl[0])
        self.ic1 = QIcon("icons/1.png")
        self.num = 0
        self.num2 = 1
        self.num3 = 0
        # print(self.musicl)
        self.add_menu()
        self.changeicon()

    def add_music(self):
        #print("2")
        files = os.listdir(os.path.join(os.getcwd(), "Music"))
        self.musicl = []
        self.musicname = []
        for x in files:
            x2 = x.split(".")[-1]
            if x2 == "wav":
                # shutil.copy('Music/%s' % x,"finm/%s" % x)
                # os.system("copy Music/%s finm/%s" % (x,x))
                self.musicl.append("Music/%s" % x)
                self.musicname.append(x.split(".")[0:-1][0])
                # print(x)
            elif x2 == "mp3":
                s = AudioSegment.from_file("Music/%s" % x, format="mp3")
                n = "finm/%s.wav" % x.split(".")[0]
                mn = x.split(".")[0]
                s.export(n, format="wav")
                self.musicl.append(n)
                self.musicname.append(mn)
        # self.musicl=os.listdir("finm")
        # for x in os.listdir("finm"):
        print(self.musicname)
        print(self.musicl)

    def numpm(self):
        #print("3")
        if self.num < 0:
            self.num = len(self.musicl) - 1
        elif self.num == len(self.musicl):
            self.num = 0

    def process(self, key):
        #print("4")
        if key == self.Trigger:
            self.next_music()
            # self.previous_music()

        # elif key==self.Context:

        #     self.next_music()
        elif key == self.MiddleClick:
            self.stop_and_play()

    def add_menu(self):
        #print("5")
        self.menu = QMenu()
        # self.action = QAction("Now playing: %s" % self.musicname[self.num], self)
        # self.menu.addAction(self.action)
        # self.actiona = QAction("(Left mouse click to play next music)", self)
        # self.menu.addAction(self.actiona)
        # self.action2 = QAction("Previous music", self, triggered=self.previous_music)
        # self.menu.addAction(self.action2)
        # self.action3 = QAction(self.word, self, triggered=self.stop_and_play)
        # self.menu.addAction(self.action3)
        # self.action4 = QAction("Next music", self, triggered=self.next_music)
        # self.menu.addAction(self.action4)
        # self.action5 = QAction("Quit Musical", self, triggered=self.quit)
        # self.menu.addAction(self.action5)
        # self.setContextMenu(self.menu)
        # self.menulist = [self.action, self.actiona,self.actionb,self.action2, self.action3, self.action4, self.action5]
        self.reflash_menu()

    def previous_music(self):
        #print("6")
        self.num4 = 1
        self.mu.stop()
        if self.num3 == 1:
            self.num3 = 0
            self.num -= 1

        else:
            self.num -= 1
        self.numpm()
        self.reflash_menu()
        self.mu = QSound(self.musicl[self.num])
        self.num2 = 0
        self.mu.play()
        self.setIcon(self.ic1)
        self.setToolTip("Musical\nNow playing: %s" % self.musicname[self.num])

        self.num2 = 0
        self.word = "||    Stop playing"
        self.reflash_menu()

        self.changeicon()

    def next_music(self):
        #print("7")
        self.num4 = 1
        self.mu.stop()
        if self.num3 == 1:
            self.num3 = 0
            self.num += 1

        else:
            self.num += 1
        self.numpm()
        self.reflash_menu()
        self.mu = QSound(self.musicl[self.num])
        self.num2 = 0
        self.mu.play()
        self.setIcon(self.ic1)
        self.setToolTip("Musical\nNow playing: %s" % self.musicname[self.num])

        self.num2 = 0
        self.word = "||    Stop playing"
        self.reflash_menu()

        self.changeicon()

    def reflash_menu(self):
        #print("7")
        try:
            for i in self.menulist:
                self.menu.removeAction(i)
        except:
            pass
        if self.num3 == 0:
            self.action = QAction("Now playing: %s" % self.musicname[self.num], self)
            self.menu.addAction(self.action)
        elif self.num3 == 1:
            self.action = QAction("Now playing: %s" % self.show1, self)
            self.menu.addAction(self.action)
        self.actiona = QAction("(Left mouse click to play next music)", self)
        self.menu.addAction(self.actiona)
        self.actionb = QAction("Reflash", self, triggered=self.reflash_music)
        self.menu.addAction(self.actionb)
        self.action2 = QAction("|◀   Previous music", self, triggered=self.previous_music)
        self.menu.addAction(self.action2)
        self.action3 = QAction(self.word, self, triggered=self.stop_and_play)
        self.menu.addAction(self.action3)
        self.action4 = QAction("▶|   Next music", self, triggered=self.next_music)
        self.menu.addAction(self.action4)
        self.actionc = QAction("▼ Other music ▼", self)
        self.menu.addAction(self.actionc)
        self.actiond = QAction("Minecraft", self, triggered=self.play_music_minecraft, font="minecraft")
        self.menu.addAction(self.actiond)
        self.actione = QAction("Pacific Rim", self, triggered=self.play_music_pacific_rim)
        self.menu.addAction(self.actione)
        self.action5 = QAction("→] Exit", self, triggered=self.quit)
        self.menu.addAction(self.action5)
        self.setContextMenu(self.menu)
        self.menulist = [self.action, self.actiona, self.actionb, self.actione, self.actionc, self.actiond,
                         self.action2, self.action3, self.action4, self.action5]

    def stop_and_play(self):
        #print("8")
        self.num4 = 1
        if self.num2 == 0:
            self.mu.stop()
            self.timen=time.time()
            self.tim=(self.timen-self.timst)*1000
            self.mutime+=self.tim
            print(self.mutime)
            self.num2 = 1
            self.word = "▶    Play"
            self.reflash_menu()
            # self.action3 = QAction(self.word, self, triggered=self.stop_and_play)
            # self.menu.removeAction(self.action3)
            # self.setContextMenu(self.menu)
        elif self.num2 == 1:
            self.playready()
            print("a")
            self.mu=QSound("umpots/p.wav")
            print("b")
            self.mu.play()
            self.timst=time.time()
            self.num2 = 0
            self.word = "||    Stop playing"
            self.reflash_menu()
            # self.action3 = QAction(self.word, self, triggered=self.stop_and_play)
            # self.menu.addAction(self.action3)
            # self.setContextMenu(self.menu)
        self.changeicon()
    def playready(self):
        #print("9")
        makmu=AudioSegment.from_wav(self.musicl[self.num])
        temmu=AudioSegment.empty()
        temmu+=makmu[self.mutime:len(makmu)]
        temmu.export("umpots/p.wav",format="wav")
    def quit(self):
        #print("10")
        self.hide()
        for x in os.listdir("finm"):
            os.remove("finm/%s" % x)
        sys.exit()
        # self.setToolTip(self.tips[self.index%len(self.tips)])
        # self.index+=1

    # def mousePressEvent(self,event):
    #     if event.key()==Qt.Key_RightClick:
    #         print("a")
    def reflash_music(self):
        #print("11")
        self.mu.stop()
        self.chenum = 1
        self.setup()

    def play_music_minecraft(self):
        #print("12")
        self.num4 = 1
        self.num2 = 0
        self.num3 = 1
        self.show1 = "Minecraft"
        self.word = "||    Stop playing"
        self.mu.stop()
        self.reflash_menu()
        self.mu = QSound("other music/Minecraft.wav")
        self.mu.play()
        self.setToolTip("Musical\nNow playing: Minecraft")
        self.changeicon()

    def play_music_pacific_rim(self):
        #print("13")
        self.num4 = 1
        self.num2 = 0
        self.num3 = 1
        self.show1 = "Pacific Rim"
        self.word = "||    Stop playing"
        self.mu.stop()
        self.reflash_menu()
        self.mu = QSound("other music/Pacific Rim.wav")
        self.mu.play()
        self.setToolTip("Musical\nNow playing: Pacific Rim")
        self.changeicon()

    def changeicon(self):
        #print("14")
        if self.num4 == 1:
            self.timer = QTimer()
            # self.timer.singleShot(3000)
            if self.num2 == 1:
                # self.setIcon("playing.png")
                self.timer.singleShot(self.timetowait, self.icon2)
                # self.timer.singleShot(msec=3000)
            elif self.num2 == 0:
                # self.setIcon("stop.png")
                self.timer.singleShot(3000, self.icon1)

    def icon1(self):
        #print("15")
        self.setIcon(QIcon("icons/playing.png"))
        self.changeicon2()

    def icon2(self):
        #print("16")
        self.setIcon(QIcon("icons/stop.png"))
        self.changeicon2()

    def icon3(self):
        #print("17")
        self.setIcon(self.icon)
        self.changeicon()

    def changeicon2(self):
        #print("18")
        self.timer.singleShot(3000, self.icon3)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myappid = 'mycompany.myproduct.subproduct.version'  # arbitrary string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    app.setWindowIcon(QIcon("icons/1.png"))
    tray = Tray()
    sys.exit(app.exec_())
