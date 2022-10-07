from glob import glob
from re import A
from pyparsing import col
from scipy.fftpack import shift
import data_load_and_preprocessing
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
now_subject=0



FPS=4
WHITE=(255,255,255)
GREEN=(0,255,0)
BLACK=(0,0,0)
YELLOW=(255,255,0)
second_per_epoch=5

channel_list=["F3","C3","P3","Fz","Cz","Pz","F4","C4","P4"]
column_list=["delta band","theta band","alpha band","beta band","gamma band"]
now_band=2
music_name=""
music_index=0

epoch_leng=40


#reshaped_avg_spec_per_epoch=2*8*5*9*epoch_leng
band_name=["alpha","beta","delta","gamma","theta"]
def print_result():
  for a in range(5):
    print(f"show {band_name[a]} band result when listening {band_name[music_index]}.mp3 v.s. listening white_noise.mp3")
    table=np.zeros((8,9))
    subject_record=np.zeros(len(reshaped_avg_spec_per_epoch[music_index]))
    for i in range(len(reshaped_avg_spec_per_epoch[music_index])):  #8
      count_channel=0
      for j in range(len(reshaped_avg_spec_per_epoch[music_index][i][a])):#9 
        count_epoch=0
        for k in range(len(reshaped_avg_spec_per_epoch[music_index][i][a][j])):  #epoch_leng
          if(reshaped_avg_spec_per_epoch[music_index][i][a][j][k]>reshaped_avg_spec_per_epoch[5][i][a][j][k]):
            count_epoch+=1
        if count_epoch>round(epoch_leng/2):
          count_channel+=1
        table[i][j]=count_epoch
      if count_channel>4:
        subject_record[i]=1

    print(subject_record)  
    print(table)
    if(sum(subject_record[0:7])>=4.0):
      print(f"In {band_name[a]}_band,when subjects listened to {band_name[music_index]}.mp3 brainwave music, they generally induced stronger brainwaves than when they listened to white noise.")
    print("\n\n")


def return_color(spec):
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

def return_percentile(spec):
  if spec<=percentile_256[0]:
    return [spec,0]
  else:
    for i in range(len(percentile_256)-1):
      if percentile_256[i]<spec<=percentile_256[i+1]:
        return [spec,i+1]


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

def draw_all_channel():
  for i in range(len(channel_obj_list[0])):#8
    for j in range(len(channel_obj_list[0][i])):#9
      pos_x=channel_obj_list[0][i][j].x
      pos_y=channel_obj_list[0][i][j].y
      draw_text(screen,channel_list[j],18,pos_x+10,pos_y-7,BLACK)
def demarcation(): #分隔線
  for i in range(9):
    draw_line(screen,BLACK,(0+WIDTH*i/8,0),(0+WIDTH*i/8,LENGTH),2)
  # for i in range(3):
  #   draw_line(screen,BLACK,(0,0+LENGTH*i/2),(WIDTH,0+LENGTH*i/2),4)

#reshaped_avg_sppec_per_epoch =2*8*5*9*53
def create_object():
  list1=[]
  for i in range(8):
    tmp_list=[]
    for j in range(9):
      x=i*150
      y=3+15+j*(15+30+2+30)
      tp=[]
      for k in range(5):
        tp.append(reshaped_avg_spec_per_epoch[music_index][i][k][j])
      channel=channel_list[j]
      music=music_name
      spec_list=tp
      spec=0.0
      channel=Channel(x,y,spec,spec_list,channel,music)

      all_sprites.add(channel)
      tmp_list.append(channel)
    list1.append(tmp_list)

  list2=[]
  for i in range(8):
    tmp_list=[]
    for j in range(9):
      x=i*150
      y=3+(15+30+2)+j*(15+30+2+30)
      tp=[]
      for k in range(5):
        tp.append(reshaped_avg_spec_per_epoch[5][i][k][j])
      channel=channel_list[j]
      music="white_noise"
      spec_list=tp
      spec=0.0
      channel=Channel(x,y,spec,spec_list,channel,music)
      all_sprites.add(channel)
      tmp_list.append(channel)
    list2.append(tmp_list)
  channel_obj_list.append(list1)
  channel_obj_list.append(list2)


class Channel(pygame.sprite.Sprite):
  def __init__(self,x,y,spec,spec_list,channel,music):
    pygame.sprite.Sprite.__init__(self)
    self.channel=channel
    self.music=music
    self.image=pygame.Surface((1,1))
    self.rect=self.image.get_rect()
    self.rect.x=x
    self.rect.y=y
    self.x=self.rect.x
    self.y=self.rect.y
    self.now_spec=spec
    self.image.fill(return_color(self.now_spec))
    self.spec_list=spec_list
    self.now_spec_list=self.spec_list[now_band]
    #print(return_color(self.now_spec),self.x,self.y,round(return_percentile(self.now_spec)[1]/2),30)
    pygame.draw.rect(screen,return_color(self.now_spec),[self.x,self.y,round(return_percentile(self.now_spec)[1]/2),30],0)
    draw_text(screen,str(round(return_percentile(self.now_spec)[0],3)),18,self.x+round(return_percentile(self.now_spec)[1]/2),self.y+7,BLACK)
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
    # self.image.fill(return_color(self.now_spec))
    # pygame.draw.rect(screen,return_color(self.now_spec),[self.x,self.y,round(return_percentile(self.now_spec)[1]/2),30],0)
    # draw_text(screen,str(round(return_percentile(self.now_spec)[0],3)),18,self.x+round(return_percentile(self.now_spec)[1]/2),self.y+7,BLACK)
  def object_display(self):
    self.image.fill(return_color(self.now_spec))
    if self.music!="white_noise":
      draw_text(screen,self.channel,25,20,self.y+22,BLACK)
    pygame.draw.rect(screen,return_color(self.now_spec),[150,self.y,return_percentile(self.now_spec)[1]*4,30],0)
    draw_text(screen,str(round(return_percentile(self.now_spec)[0],3)),18,150+(return_percentile(self.now_spec)[1]*4),self.y+7,BLACK)
    draw_text(screen,self.music,18,100,self.y+7,BLACK)
  def object_display_all(self):
    self.image.fill(return_color(self.now_spec))
    pygame.draw.rect(screen,return_color(self.now_spec),[self.x,self.y,round(return_percentile(self.now_spec)[1]/2),30],0)
    draw_text(screen,str(round(return_percentile(self.now_spec)[0],3)),18,self.x+round(return_percentile(self.now_spec)[1]/2),self.y+7,BLACK)
  def change_band(self):
    self.now_spec_list=self.spec_list[now_band]
    self.now_spec=self.now_spec_list[self.epoch_count-1]
    self.next_spec=self.now_spec_list[self.epoch_count]
def gradientRect( screen, left_colour, right_colour, target_rect ):
  """ Draw a horizontal-gradient filled rectangle covering <target_rect> """
  colour_rect = pygame.Surface( ( 2, 2 ) )                                   # tiny! 2x2 bitmap
  pygame.draw.line( colour_rect, left_colour,  ( 0,0 ), ( 1,0 ) )            # left colour line
  pygame.draw.line( colour_rect, right_colour, ( 0,1 ), ( 1,1 ) )            # right colour line
  colour_rect = pygame.transform.smoothscale( colour_rect, ( target_rect.width, target_rect.height ) )  # stretch!
  screen.blit( colour_rect, target_rect )         
def draw_rect_loop():
  # pygame.draw.rect(screen,WHITE,[1275,20,50,256],0) # 畫能量表示圖
  # gradientRect( screen, (0, 255, 0), (0, 100, 0), pygame.Rect( 100,100, 100, 50 ) )
  gradientRect( screen, (255, 0, 0), (0, 0, 255), pygame.Rect( 1250, 20, 50, 200 ) )
  draw_text(screen, str(round(percentile_256[0],2))+"(μV^2)", 16, 1350, 220, BLACK)
  draw_text(screen, str(round(percentile_256[-1],2))+"(μV^2)", 16, 1350, 20, BLACK)
  # draw_text(screen, "(μV^2)", 18, 1368, 20, WHITE)
  # draw_text(screen, "(μV^2)", 18, 1368, 220, WHITE)



def draw_now_band():
    draw_text(screen,"Now Band : "+column_list[now_band],20,1300,530,BLACK)

def show_subject():
  for i in range(len(channel_obj_list)):#2
    for j in range(len(channel_obj_list[i])):#8
      for k in  range(len(channel_obj_list[i][j])):#9
        if j==now_subject:
          channel_obj_list[i][j][k].object_display()
def show_all_subject():
  demarcation()
  draw_all_channel()
  for i in range(len(channel_obj_list)):#2
    for j in range(len(channel_obj_list[i])):#8
      for k in  range(len(channel_obj_list[i][j])):#9
        channel_obj_list[i][j][k].object_display_all()

def force_exit():
  pygame.quit()

def run(avg_spec_per_epoch,percentile_256_outer,epoch_leng_outer,music_name_outer,music_index_outer):
  force_exit()
  pygame.init()
  global all_sprites
  all_sprites=pygame.sprite.Group()
  pygame.mixer.init()
  global WIDTH
  global LENGTH
  global AREA
  global screen
  WIDTH,LENGTH=1400-200,700
  AREA=(WIDTH+200,LENGTH)
  screen=pygame.display.set_mode(AREA)
  global music_name
  global music_index
  global epoch_leng
  epoch_leng=epoch_leng_outer
  music_index=music_index_outer
  music_name=music_name_outer
  soundwav=pygame.mixer.Sound(f"./{music_name}/{music_name}.mp3")
  WIDTH,LENGTH=1400-200,700
  AREA=(WIDTH+200,LENGTH)
  screen=pygame.display.set_mode(AREA)
  pygame.display.set_caption("UI_mode3")
  clock=pygame.time.Clock()
  FPS=4
  WHITE=(255,255,255)
  GREEN=(0,255,0)
  BLACK=(0,0,0)
  YELLOW=(255,255,0)
  second_per_epoch=5
  global reshaped_avg_spec_per_epoch
  global channel_obj_list
  global percentile_256
  global now_band
  global now_subject
  reshaped_avg_spec_per_epoch=[]
  channel_obj_list=[]
  percentile_256=[]
  percentile_256=percentile_256_outer
  channel_list=["F3","C3","P3","Fz","Cz","Pz","F4","C4","P4"]
  column_list=["delta band","theta band","alpha band","beta band","gamma band"]
  now_band=0
  max_band=5
  leng=epoch_leng*second_per_epoch
  total_leng=leng

  time_point=np.zeros(total_leng)
  for x in range(len(avg_spec_per_epoch)):
    tmptmptmp=[]
    for a in range(len(avg_spec_per_epoch[x])):
      tmptmp=[]
      for i in range(len(avg_spec_per_epoch[x][0][0][0])):
        temp=[]
        for j in range(len(avg_spec_per_epoch[x][0])):
          tmp=[]
          for k in range(len(avg_spec_per_epoch[x][0][0])):
            tmp.append(avg_spec_per_epoch[x][a][j][k][i])
          temp.append(tmp)
        tmptmp.append(temp)
      tmptmptmp.append(tmptmp)
    reshaped_avg_spec_per_epoch.append(tmptmptmp)

  running=True
  flag=True
  cnt=0
  cnt_per_fps=0
  cnt_per_second=0
  create_object()
  show_init=True
  show_subject_mode=0
  soundwav.play()
  pygame.mixer.pause()
  while running:
    cnt_per_fps=0
    clock.tick(FPS)
    if show_init==True:
      screen.fill(BLACK)
      draw_text(screen,"press SPACE to start!",50,700,350,WHITE)
      for event in pygame.event.get():
          if event.type==pygame.QUIT:
            running=False
          elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
              running = False
            elif event.key== pygame.K_SPACE:
              show_init=False
    else:
      pygame.mixer.unpause()
      screen.fill(WHITE)
      draw_now_band()
      draw_rect_loop()
      if flag:
        pygame.mixer.unpause()
        cnt+=1
        if(cnt==FPS):
          if cnt_per_second>=2:
            time_point[total_leng-leng]=1
          cnt_per_second=0
          leng-=1
          cnt=0
        if(leng==0):
          running=False
        for event in pygame.event.get():
          if event.type==pygame.QUIT:
            running=False
          elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
              running = False
            elif event.key==pygame.K_SPACE:
                flag=False
            elif event.key== pygame.K_RIGHT:
              now_band+=1
              now_band%=max_band
              for i in range(len(channel_obj_list)):#2
                for j in range(len(channel_obj_list[i])):#8
                  for k in  range(len(channel_obj_list[i][j])):#9
                    channel_obj_list[i][j][k].change_band()
            elif event.key== pygame.K_LEFT:
              now_band-=1
              if now_band<0:
                now_band=max_band+now_band
              for i in range(len(channel_obj_list)):#2
                for j in range(len(channel_obj_list[i])):#8
                  for k in  range(len(channel_obj_list[i][j])):#9
                    channel_obj_list[i][j][k].change_band()
            elif event.key==pygame.K_DOWN:
              show_subject_mode=0
              now_subject+=1
              now_subject%=8
            elif event.key==pygame.K_UP:
              show_subject_mode=0
              now_subject-=1
              if now_subject<0:
                now_subject+=8
            elif event.key==pygame.K_a:
              show_subject_mode=1
              


          

          
        if show_subject_mode==0:
          show_subject()
          draw_text(screen, "Now subject number:"+str(now_subject+1), 20, 1300, 550, BLACK)
        else:
          show_all_subject()
        draw_text(screen, "RUN", 25, 1360, 670, BLACK)
        draw_text(screen, "Music time(s):"+str(total_leng-leng)+"/"+str(total_leng)+" s", 20, 1300, 610, BLACK)
        # draw_text(screen, str(total_leng-leng)+"/"+str(total_leng)+" s", 20, 1360, 610, BLACK)
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
              for i in range(len(channel_obj_list)):#2
                for j in range(len(channel_obj_list[i])):#8
                  for k in  range(len(channel_obj_list[i][j])):#9
                    channel_obj_list[i][j][k].change_band()
            elif event.key== pygame.K_LEFT:
              now_band-=1
              if now_band<0:
                now_band=max_band+now_band
              for i in range(len(channel_obj_list)):#2
                for j in range(len(channel_obj_list[i])):#8
                  for k in  range(len(channel_obj_list[i][j])):#9
                    channel_obj_list[i][j][k].change_band()
            elif event.key==pygame.K_DOWN:
              show_subject_mode=0
              now_subject+=1
              now_subject%=8
            elif event.key==pygame.K_UP:
              show_subject_mode=0
              now_subject-=1
              if now_subject<0:
                now_subject+=8
            elif event.key==pygame.K_a:
              show_subject_mode=1
              


          

          
        if show_subject_mode==0:
          show_subject()
          draw_text(screen, "Now subject number:"+str(now_subject+1), 20, 1300, 550, BLACK)
        else:
          show_all_subject()
        draw_text(screen, "PAUSE", 25, 1360, 670, BLACK)
        draw_text(screen, "Music time(s):"+str(total_leng-leng)+"/"+str(total_leng)+" s", 20, 1300, 610, BLACK)
        # draw_text(screen, str(total_leng-leng)+"/"+str(total_leng)+" s", 20, 1360, 610, BLACK)


      all_sprites.draw(screen)
    pygame.display.update()
  pygame.quit()
  print_result()
