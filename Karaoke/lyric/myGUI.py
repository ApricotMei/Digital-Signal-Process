import pygame

import tkinter as Tk
# import winsound
import time

#load lyric
lrcfile = 'final_lyrics.txt'
#read file
f = open(lrcfile)
strLrc = f.read()
dictLrc = {}
# split lyrics
lineListLrc = strLrc.splitlines()
for lineLrc in lineListLrc:
    # split time and text
    listLrc = lineLrc.split("]")
    timeLrc = listLrc[0][1:].split(':')
    times = float(timeLrc[0]) * 60 + float(timeLrc[1])
    dictLrc[times] = listLrc[1]
# tempTime = 0

music = Tk.Tk()
music.title('music player')
#music.geometry('460x600+500+100')

pygame.mixer.init()

def lrc(tempTime=0):
    for key in dictLrc.keys():
        tempTime = key - tempTime
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.play()
        time.sleep(tempTime)
        print(dictLrc[key])
        tempTime = key

def m1():
    #import winsound
    #winsound.PlaySound('1.wav', winsound.SND_FILENAME|winsound.SND_ASYNC)
    song_path= 'Rolling in the Deep.wav'
    pygame.mixer.init()
    pygame.mixer.music.load(song_path)
    lrc()
def m2():
	track2 = pygame.mixer.Sound('accompany.wav')
	track2.play()

def pause():
	pygame.mixer.pause()

def unpause():
	pygame.mixer.unpause()

def open():
	sing= Tk.Toplevel()
	sing.title('sing')
	a2 = Tk.Button(sing, text = 'test', command = m1)
	a2.pack()



a1 = Tk.Label(music,font = ("Courier", 28, "bold"), text = 'test')
b1 = Tk.Button(music, text = 'play music1',font = ('Courier New bold',14), width = 16 , command = m1)
b2 = Tk.Button(music, text = 'play music2', width = 8, command = m2)
c1 = Tk.Button(music, text = 'pause', width = 8, command = pause)
d1 = Tk.Button(music, text = 'play', width = 8, command = unpause)
e1 = Tk.Button(music, text = 'sing', command = open)
f1 = Tk.Label(music, font = ("Courier", 15, "bold"),text = 'lyrics')

a1.pack()
b1.pack()
b2.pack()
c1.pack()
d1.pack()
e1.pack()
f1.pack()


music.mainloop()