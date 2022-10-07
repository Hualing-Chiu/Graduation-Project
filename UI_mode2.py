from re import A
from pyparsing import col
from scipy.fftpack import shift
# import data_average
import random
import math
import pygame
import matplotlib.pyplot as plt
import pandas as pd
import statistics as stat
import warnings
import numpy as np
import sys
import os
import threading
from matplotlib.pylab import mpl 





reshaped_avg_spec_per_epoch=[]
channel_obj_list=[]



FPS=8
WHITE=(255,255,255)
GREEN=(0,255,0)
BLACK=(0,0,0)
YELLOW=(255,255,0)
second_per_epoch=5
now_subject_index=0
max_subject_index=8
now_channel_index=0
max_channel_index=9
channel_list=["F3","C3","P3","Fz","Cz","Pz","F4","C4","P4"]
column_list=["delta band","theta band","alpha band","beta band","gamma band"]
now_band=0
now_subject_group=0
max_band=5
leng=40*5
total_leng=leng
all_sprites=pygame.sprite.Group()
def return_color(spec,percentile_256):
  color=(255,0,0)
  if(spec==0):
    return color
  if(spec==percentile_256[0]):
    color=[0,0,256]
  else:
    for i in range(len(percentile_256)-1):
      if percentile_256[i]<spec<=percentile_256[i+1]:
        color=[((i+1)*1),0,(256-(i+1)*1)]
        break
  for i in range(len(color)):
    if color[i]==256:
      color[i]=255
  return (color[0],color[1],color[2])

def return_percentile(spec,percentile_256):
  if spec==percentile_256[0]:
    return [spec,0+1]
  else:
    for i in range(len(percentile_256)-1):
      if percentile_256[i]<spec<=percentile_256[i+1]:
        return [spec,i+1]



#reshaped_avg_sppec_per_epoch =8*5*9*53
def draw_circle(reshaped_avg_spec_per_epoch,percentile_256):
  R=WIDTH/10
  outer_cnt=0
  for i in range(2):
    for j in range(2):
      outer_cnt+=1
      big_circle_center_x=i*((WIDTH+200)/2)+(WIDTH/10)
      big_circle_center_y=175+350*j
      pygame.draw.circle(screen,(193, 225, 193),(big_circle_center_x,big_circle_center_y),R,0)
      divider=2.3
      shift_x=((R*(1/2))+(int(R/divider)))
      shift_y=((R*(1/2))+(int(R/divider)))
      inner_cnt=0
      tmp_list=[]
      for k in range(3):
        for L in range(3):
          inner_cnt+=1
          x=big_circle_center_x+((R*(1/2))+(k*int(R/divider)))-shift_x
          y=big_circle_center_y+((R*(1/2))+(L*int(R/divider)))-shift_y
          text_x=x   #channel name X座標
          text_y=y-25   #channel name Y座標
          r=int(R/7)
          tp=[]                                          #1         2   2 6    3   3 7    4    4 8
          for a in range(max_subject_index):
            tp1=[]
            if(a+1==outer_cnt or a+1==outer_cnt+4):
              
              for b in range(5):
                tp1.append(reshaped_avg_spec_per_epoch[a][b][inner_cnt-1])
              tp.append(tp1)
          spec_list=tp
          spec=reshaped_avg_spec_per_epoch[now_subject_group][now_band][inner_cnt-1][0]
          channel=Channel(x,y,r,spec,spec_list,percentile_256)
          all_sprites.add(channel)  
          tmp_list.append(channel)
      channel_obj_list.append(tmp_list)

def draw_circle_loop():
  R=WIDTH/10
  cnt=0
  for i in range(2):
    for j in range(2):
      cnt+=1
      big_circle_center_x=2+i*((WIDTH+200)/2)+(WIDTH/10)
      big_circle_center_y=175+350*j
      pygame.draw.circle(screen,(193, 225, 193),(big_circle_center_x,big_circle_center_y),R,0)
      
font_name = pygame.font.match_font('arial')
def draw_text(surf, text, size, x, y, color):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.centery = y
    surf.blit(text_surface, text_rect)
def draw_line(surf,linecolor,start,end,width):
  pygame.draw.line(surf,linecolor,start,end,width)
def demarcation(): #分隔線
  draw_line(screen,BLACK,(0,350),(1400,350),2)
  draw_line(screen,BLACK,(700,0),(700,700),2)
def draw_bar_chart(now_list,percentile_256):
  for i in range(2): #上面y軸
    draw_line(screen,BLACK,(270+700*i,40),(270+700*i,310),2)
    draw_text(screen,"subject_"+str(i+1+now_subject_group*4),25,120+700*i,30,BLACK)
    for j in range(9):
      draw_text(screen, channel_list[j], 20, 252+700*i, 52+30*j, BLACK)
      pygame.draw.rect(screen,return_color(now_list[i][j][0],percentile_256),[270+700*i,40+j*30,round(now_list[i][j][1]),30],0)
      draw_text(screen,str(round(now_list[i][j][0],3)),18,275+700*i+round(now_list[i][j][1]),52+30*j,BLACK)
  for i in range(2): #下面y軸
    draw_line(screen,BLACK,(270+700*i,40+350),(270+700*i,310+350),2)
    draw_text(screen,"subject_"+str(i+2+1+now_subject_group*4),25,120+700*i,320+350,BLACK)
    for j in range(9):
      draw_text(screen, channel_list[j], 20, 252+700*i, 350+52+30*j, BLACK)
      pygame.draw.rect(screen,return_color(now_list[i+2][j][0],percentile_256),[270+700*i,350+40+j*30,round(now_list[i+2][j][1]),30],0)
      draw_text(screen,str(round(now_list[i+2][j][0],3)),18,275+700*i+round(now_list[i+2][j][1]),350+52+30*j,BLACK)


def draw_now_band():
    draw_text(screen,"Now Band : "+column_list[now_band],20,700,350,BLACK)
class Channel(pygame.sprite.Sprite):
  def __init__(self,x,y,r,spec,spec_list,percentile_256):
    pygame.sprite.Sprite.__init__(self)
    self.image=pygame.Surface((1,1))
    self.rect=self.image.get_rect()
    self.rect.centerx=x
    self.rect.centery=y
    self.x=self.rect.centerx
    self.y=self.rect.centery
    self.r=r
    self.now_spec=spec
    self.image.fill(return_color(self.now_spec,percentile_256))
    self.spec_list=spec_list
    self.now_spec_list=self.spec_list[now_subject_group][now_band]
    self.percentile_256=percentile_256
    pygame.draw.circle(screen,return_color(self.now_spec,self.percentile_256),(self.x,self.y),self.r,0)
    self.now_fps=0
    self.epoch_count=0
    self.next_spec=self.now_spec_list[self.epoch_count]
  def update(self):
    self.now_fps+=1
    if(self.now_fps==FPS*second_per_epoch):
      self.now_fps=0
      self.epoch_count+=1
    self.next_spec=self.now_spec_list[self.epoch_count]
    self.now_spec+=((self.next_spec-self.now_spec)/(FPS*second_per_epoch))
    self.image.fill(return_color(self.now_spec,self.percentile_256))
    pygame.draw.circle(screen,return_color(self.now_spec,self.percentile_256),(self.x,self.y),self.r,0)
  def change_band(self):
    self.now_spec_list=self.spec_list[now_subject_group][now_band]
    self.now_spec=self.now_spec_list[self.epoch_count-1]
    self.next_spec=self.now_spec_list[self.epoch_count]
  def change_group(self):
    self.now_spec_list=self.spec_list[now_subject_group][now_band]
    self.now_spec=self.now_spec_list[self.epoch_count-1]
    self.next_spec=self.now_spec_list[self.epoch_count]
# reshaped_avg_spec_per_epoch=np.array(reshaped_avg_spec_per_epoch)
def force_exit():
  pygame.quit()

def run(avg_spec_per_epoch,percentile_256,epoch_leng,music_name):
  pygame.init()
  pygame.mixer.init()
  soundwav=pygame.mixer.Sound(f"./{music_name}/{music_name}.mp3")
  global WIDTH
  global LENGTH
  global AREA
  global screen
  WIDTH,LENGTH=1400-200,700
  AREA=(WIDTH+200,LENGTH)
  screen=pygame.display.set_mode(AREA)
  pygame.display.set_caption("UI_mode2")
  clock=pygame.time.Clock()
  FPS=8
  WHITE=(255,255,255)
  GREEN=(0,255,0)
  BLACK=(0,0,0)
  YELLOW=(255,255,0)
  second_per_epoch=5
  now_subject_index=0
  max_subject_index=8
  now_channel_index=0
  max_channel_index=9
  channel_list=["F3","C3","P3","Fz","Cz","Pz","F4","C4","P4"]
  column_list=["delta band","theta band","alpha band","beta band","gamma band"]
  global now_band
  global now_subject_group
  now_band=0
  now_subject_group=0
  max_band=5
  leng=epoch_leng*second_per_epoch
  total_leng=leng
  soundwav.play()
  reshaped_avg_spec_per_epoch=[]
  for a in range(len(avg_spec_per_epoch)):
    tmptmp=[]
    for i in range(len(avg_spec_per_epoch[0][0][0])):
      temp=[]
      for j in range(len(avg_spec_per_epoch[0])):
        tmp=[]
        for k in range(len(avg_spec_per_epoch[0][0])):
          tmp.append(avg_spec_per_epoch[a][j][k][i])
        temp.append(tmp)
      tmptmp.append(temp)
    reshaped_avg_spec_per_epoch.append(tmptmp)

  draw_circle(reshaped_avg_spec_per_epoch,percentile_256)
  running=True
  flag=True
  cnt=0
  while running:
    now_channel_list=[]
    clock.tick(FPS)
    screen.fill(WHITE)
    demarcation()
    pygame.draw.rect(screen,(230, 230, 230),[580,305,240,90],0)
    draw_circle_loop()
    if flag:
      cnt+=1
      if(cnt==FPS):
        leng-=1
        cnt=0
      if(leng==0):
        running=False
      pygame.mixer.unpause()
      for event in pygame.event.get():
        if event.type==pygame.QUIT:
          running=False
        elif event.type == pygame.KEYDOWN:
          if event.key == pygame.K_q:
            running = False
          elif event.key== pygame.K_SPACE:
            flag=False
          elif event.key== pygame.K_RIGHT:
            now_band+=1
            now_band%=max_band
            for i in range(len(channel_obj_list)):#4
              for j in range(len(channel_obj_list[i])):#9
                channel_obj_list[i][j].change_band()
          elif event.key== pygame.K_LEFT:
            now_band-=1
            if now_band<0:
              now_band=max_band+now_band
            for i in range(len(channel_obj_list)):#4
              for j in range(len(channel_obj_list[i])):#9
                channel_obj_list[i][j].change_band()
          elif event.key== pygame.K_DOWN:
            now_subject_group+=1
            now_subject_group%=2
            for i in range(len(channel_obj_list)):#4
              for j in range(len(channel_obj_list[i])):#9
                channel_obj_list[i][j].change_group()
          elif event.key==pygame.K_UP:
            now_subject_group-=1
            if now_subject_group<0:
              now_subject_group=1
            for i in range(len(channel_obj_list)):#4
              for j in range(len(channel_obj_list[i])):#9
                channel_obj_list[i][j].change_group()
      draw_text(screen, "RUN", 20, 700, 325, BLACK)
      draw_text(screen, "Music time(s) : ", 20, 667, 375, BLACK)
      draw_text(screen, str(total_leng-leng)+"/"+str(total_leng)+" s", 20, 762, 375, BLACK)
      all_sprites.update()
    else:
      pygame.mixer.pause()
      for event in pygame.event.get():
        if event.type==pygame.QUIT:
          running=False
        elif event.type == pygame.KEYDOWN:
          if event.key == pygame.K_q:
            running = False
          elif event.key== pygame.K_SPACE:
            flag=True
          elif event.key== pygame.K_RIGHT:
            now_band+=1
            now_band%=max_band
            for i in range(len(channel_obj_list)):#4
              for j in range(len(channel_obj_list[i])):#9
                channel_obj_list[i][j].change_band()
          elif event.key== pygame.K_LEFT:
            now_band-=1
            if now_band<0:
              now_band=max_band+now_band
            for i in range(len(channel_obj_list)):#4
              for j in range(len(channel_obj_list[i])):#9
                channel_obj_list[i][j].change_band()
          elif event.key== pygame.K_DOWN:
            now_subject_group+=1
            now_subject_group%=2
            for i in range(len(channel_obj_list)):#4
              for j in range(len(channel_obj_list[i])):#9
                channel_obj_list[i][j].change_group()
          elif event.key==pygame.K_UP:
            now_subject_group-=1
            if now_subject_group<0:
              now_subject_group=1
            for i in range(len(channel_obj_list)):#4
              for j in range(len(channel_obj_list[i])):#9
                channel_obj_list[i][j].change_group()
      draw_text(screen, "PAUSE", 20, 700, 325, BLACK)
      draw_text(screen, "Music time(s) : ", 20, 667, 375, BLACK)
      draw_text(screen, str(total_leng-leng)+"/"+str(total_leng)+" s", 20, 762, 375, BLACK)
    outer_list=[]
    for i in (0,2,1,3):#4
      inner_list=[]
      for j in range(len(channel_obj_list[i])):#9
          inner_list.append(return_percentile(channel_obj_list[i][j].now_spec,percentile_256))
          pygame.draw.circle(screen,return_color(channel_obj_list[i][j].now_spec,percentile_256),(channel_obj_list[i][j].x,channel_obj_list[i][j].y),channel_obj_list[i][j].r,0)
      # print()
      outer_list.append(inner_list)
    draw_bar_chart(outer_list,percentile_256)
    draw_now_band()
    all_sprites.draw(screen)
    pygame.display.update()
  pygame.quit()
  