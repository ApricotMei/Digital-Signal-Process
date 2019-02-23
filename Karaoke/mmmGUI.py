from tkinter import *
from tkinter.font import Font
from PIL import Image, ImageTk
import os, pygame, time
from datetime import datetime
from threading import Thread

# from myfunctions import record

class Window:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        # 创建tkinter顶层窗口
        self.master = Tk()
        self.master.title('Let\'s sing' )  # 窗口的标题

        left = (self.master.winfo_screenwidth() - width) // 2
        top = (self.master.winfo_screenheight() - height) // 2

        self.master.geometry('{0}x{1}+{2}+{3}'.format(width, height, left, top))


class ButtonsFrame(Frame):  # 播放按钮组的页面
    from myfunctions import record


    def __init__(self, master, musicListFrame, musicFrame):
        super(ButtonsFrame, self).__init__(master)
        self.musicListFrame = musicListFrame  # 列表界面
        self.musicFrame = musicFrame  # 显示歌曲信息

        frame = Frame(self)  # 临时使用，作为按钮组不见的直接父窗口
        self.singBtn = Button(frame, text='SING', width=20, bg='rosybrown', padx=4,  font=("Courier",10),command=self.sing)
        self.playBtn = Button(frame, text='ORIGINAL SONG', width=20, bg='rosybrown', padx=4,  font=("Courier",10), command=self.play)
        self.pauseBtn = Button(frame, text='PAUSE/CONTINUE', width=20, bg='rosybrown', padx=4,  font=("Courier",10),command=self.pause)
        self.stopBtn = Button(frame, text='STOP', width=20, bg='rosybrown', padx=4,  font=("Courier",10),command=self.stop)
        self.hahaBtn = Button(frame, text = 'LAUGH', width = 20, bg = 'rosybrown', padx = 3,  font=("Courier",10),command = self.haha)
        self.booBtn = Button(frame, text = 'BOOING', width = 20, bg = 'rosybrown', padx= 3, font=("Courier",10),command = self.boo)        
        self.appBtn = Button(frame, text = 'APPLAUD', width = 20, bg = 'rosybrown', padx = 3, font=("Courier",10),command = self.applaud)
        # 以表格布局方式将按钮添加到frame界面中
        self.singBtn.grid(row=0, column=1)
        self.playBtn.grid(row=0, column=2)
        self.pauseBtn.grid(row=1, column=1)
        self.stopBtn.grid(row=1, column=2)
        self.hahaBtn.grid(row=3, column=1)
        self.booBtn.grid(row=3, column=2)
        self.appBtn.grid(row=3, column=3)
        frame.pack(side=BOTTOM)  # 将按钮组躲在的界面放在窗口的底部位置

        self.playing = False  # 播放中
        self.musicPosition = 0 # 播放到哪一行


    def play(self):
        #print('--play--')
        playMusicName, musicPath = self.musicListFrame.getSelectMusic()  # 获取选择的音乐
        if playMusicName:
            self.musicFrame.musicName.set(playMusicName)
            print(playMusicName)

            # 加载歌词
            self.loadLyric(playMusicName)

            self.toPlay(musicPath)

        else:
            print('--请选择歌曲--')

    def haha(self):
        pygame.mixer.init()
        track1 = pygame.mixer.Sound('23333.wav')
        track1.play()
    def boo(self):
        pygame.mixer.init()
        track2 = pygame.mixer.Sound('boo.wav')
        track2.play()
    def applaud(self):
        pygame.mixer.init()
        track3 = pygame.mixer.Sound('applaud.wav')
        track3.play()
    def loadLyric(self, musicName):
        lyricPath = os.path.join('./lyric', musicName+'.txt')
        if os.path.exists(lyricPath):
            self.times = []  # 每一行歌词播放的时间
            self.contents = []  # 每一行歌词
            self.timesdelta = []  # 时间差

            with open(lyricPath, encoding='gbk') as f:
                for line in f.readlines():
                    self.times.append(datetime.strptime(line.split(']')[0][1:],'%M:%S.%f'))
                    self.contents.append(line.split(']')[1].strip())

            for i in range(len(self.times)-1):
                t1 = self.times[i]
                t2 = self.times[i+1]
                td = t2 - t1
                td = round(float('{0}.{1}'.format(td.seconds,td.microseconds)))
                self.timesdelta.append(td)

        else:
            print('{0} 不存在！'.format(lyricPath))

    def toShowLyric(self):
        # 显示第一行的歌词
        self.musicFrame.musicLyric.set(self.contents[self.musicPosition])
        for i in range(self.musicPosition, len(self.timesdelta)):
            if not self.playing:
                self.musicPosition = i+1
                break
            # 等待下一行歌词显示
            time.sleep(self.timesdelta[i])
            if not self.playing:
                self.musicPosition = i+1
                break

            self.musicFrame.musicLyric.set(self.contents[i+1])


    def toPlay(self, mpath):
        # 播放音乐
        pygame.mixer.init()
        pygame.mixer.music.load(mpath)
        pygame.mixer.music.play()
        self.playing = True
        self.musicPosition = 0  # 新歌从第一行开始
        self.lt = Thread(target=self.toShowLyric)  #显示歌词
        self.lt.start()  # 启动子线程，显示歌词

    def record_Play(self, mpath):
        # 播放音乐
        pygame.mixer.init()
        pygame.mixer.music.load(mpath)
        pygame.mixer.music.play()
        self.playing = True
        self.musicPosition = 0  # 新歌从第一行开始
        self.lt = Thread(target=self.toShowLyric)  #显示歌词
        self.lt.start()  # 启动子线程，显示歌词
        self.re = Thread(target=self.record) 
        self.re.start() 
        #root = Tk()
        #scorelabel = Label(root, text = 'your score')
        #scorelabel.pack()
        #root.mainloop()

    def pause(self):
        print('--pause--')
        if self.playing:
            pygame.mixer.music.pause()
            self.playing = False
            time.sleep(1)
            self.lt.join()  # 等待子线程结束
        else:
            pygame.mixer.music.unpause()
            self.playing = True
            self.lt = Thread(target=self.toShowLyric)  # 显示歌词
            self.lt.start()  # 启动子线程，显示歌词

    def stop(self):
        print('--stop--')
        if self.playing:
            pygame.mixer.music.stop()
            self.playing = False

    def sing(self):
        playMusicName,x = self.musicListFrame.getSelectMusic() # 获取选择的音乐
        musicPath = './music_accompany/'+ playMusicName +'.wav'
        if playMusicName:
            self.musicFrame.musicName.set(playMusicName)
            print(playMusicName)

            # 加载歌词
            self.loadLyric(playMusicName)

            self.record_Play(musicPath)


class MusicInfoFrame(Frame):
    def __init__(self, master):
        super(MusicInfoFrame, self).__init__(master)

        img = Image.open('1.jpg')
        photoImg = img.resize((320, 320), Image.ANTIALIAS)
        self.photo = ImageTk.PhotoImage(photoImg)  # 转成Tk控件可以显示的图片对象

        frame = Frame(self, width=400, height=400, bg = "LightSlateGray")

        self.musicName = StringVar(value='Let\'s sing!')
        font = Font(size=18, family='bold')
        self.musicNameLabel = Label(frame, textvariable=self.musicName, font=("Courier",30,"bold"), fg='LightSlateGray', width=30, height=3)

        self.musicImgLabel = Label(frame, image=self.photo, text='show picture')
        self.musicLyric = StringVar(value='Lyric')
        lyricLabel = Label(frame, textvariable=self.musicLyric, font= ("Courier",15,"bold"), fg='green', width=50, height=10, )

        self.musicNameLabel.pack(side=TOP)
        self.musicImgLabel.pack(after=self.musicNameLabel)  # before兄弟控件的前面，after兄弟控件的后面
        lyricLabel.pack(after=self.musicImgLabel)

        frame.pack(side=TOP)


class MusicListFrame(Frame):
    def __init__(self, master):
        super(MusicListFrame, self).__init__(master)
        self.musicList = []  #歌曲列表（MP3文件的完整路径）

        titleLabel = Label(self, text='Choose Music to Sing', fg='LightSlateGray', font=('Courier',20,"bold"), width=20)
        self.musicListbox = Listbox(self, bd=1, selectmode=SINGLE,height=30)
        self.loadMusic('./music')


        titleLabel.pack(side=TOP)
        self.musicListbox.pack(after=titleLabel)


    def getSelectMusic(self):
        musicName = self.musicListbox.selection_get()
        for mpath in self.musicList:
            if musicName == os.path.split(mpath)[1]:
                return os.path.splitext(musicName)[0],mpath

        print('Choose music to sing')

    def loadMusic(self, path):
        # load all music in path
        for fileName in os.listdir(path):
            if 'wav' in fileName:
                self.musicListbox.insert(END,fileName)
                self.musicList.append(os.path.join(path,fileName))


if __name__ == '__main__':
    win = Window(900, 600)
    musicListFrame = MusicListFrame(win.master)
    musicListFrame.pack(side=LEFT)

    musicFrame = MusicInfoFrame(win.master)


    btnsFrame = ButtonsFrame(win.master, musicListFrame, musicFrame)
    btnsFrame.pack(side=BOTTOM)
    musicFrame.pack(side=TOP)  # 这个要放到最后面

    mainloop()  # 主界面一直显示