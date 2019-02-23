
import pygame
import time
def showlrc(lrcfile,song_path):
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



    tempTime = 0
    pygame.mixer.init()
    pygame.mixer.music.load(song_path)
    for key in dictLrc.keys():
        tempTime = key - tempTime
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.play()
        time.sleep(tempTime)
        print(dictLrc[key])
        tempTime = key

lrcfile = 'final_lyrics.txt'
song_path = 'accompany.wav'
showlrc(lrcfile,song_path)