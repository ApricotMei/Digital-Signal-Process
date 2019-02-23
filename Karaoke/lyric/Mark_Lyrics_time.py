# -*- coding: utf-8 -*-
filename='accompany.wav'
bg1='1.png'
bg2='2.png'
bg3='3.png'
b='4.png'

import sys
import os
import pygame
from pygame.locals import *


# def formattime(t):
#   if t/10 == 0:
#     return '0'+str(int(t))

#   else:
#     return str(int(t))

def ms2time(t):
  m = t/60000
  s = t/1000
  minsec = '00'+':'+str(s)
  # +'.'+str(t)
  return minsec


def playmusic():
  rect=(0,0)
  n=0
  m=3
  pygame.init()
  screen = pygame.display.set_mode((300, 360), 0, 32)

  #new window
  pygame.display.set_caption("Transform")#title
  background = pygame.transform.scale(pygame.image.load(bg1), (300, 360))
  icon = pygame.image.load(b)
  pygame.display.set_icon(icon)
  #pygame.mixer.init()
  pygame.mixer.music.load(filename)
  pygame.mixer.music.play()
  while True:#sds
      for event in pygame.event.get():     
          if event.type ==QUIT:                            
              pygame.quit()
              sys.exit()
          pressed_keys = pygame.key.get_pressed()        
          if event.type == pygame.MOUSEBUTTONDOWN:
              n+=1
              if n%m==0:                  
                 background = pygame.transform.scale(pygame.image.load(bg1), (300, 360))
                 rect = background.get_rect()
                 screen = pygame.display.set_mode((rect.width, rect.height))                   
              if n%m==1:
                 background = pygame.transform.scale(pygame.image.load(bg2), (300, 360))
                 rect = background.get_rect()
                 screen = pygame.display.set_mode((rect.width, rect.height))
              if n%m==2:
                 background = pygame.transform.scale(pygame.image.load(bg3), (300, 360))
                 rect = background.get_rect()
                 screen = pygame.display.set_mode((rect.width, rect.height))
              t = pygame.mixer.music.get_pos()   #return ms
              minsec = ms2time(t)
              with open('time.txt', 'a+') as f:
                  f.write('['+minsec+']'+'\n')
      screen.blit(background,rect)         
      pygame.display.update() 

if __name__ == "__main__":  
    playmusic() 