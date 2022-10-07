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
# avg_spec_per_epoch,percentile_256,epoch_leng,music_list=data_load_and_preprocessing.get_avg()
# avg_spec_per_epoch=avg_spec_per_epoch[0].tolist()



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
interval=260  #表格字體跟圓形的間隔
display_mode=0 ##0:table  1:bar_plot
leng=40*5
total_leng=leng

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
  if spec<=percentile_256[0]:
    return [spec,0]
  else:
    for i in range(len(percentile_256)-1):
      if percentile_256[i]<spec<=percentile_256[i+1]:
        return [spec,i+1]

def draw_circle(reshaped_avg_spec_per_epoch,percentile_256):
  R=WIDTH/10
  for i in range(5):
    big_circle_center_x=i*(WIDTH/5)+(WIDTH/10)
    big_circle_center_y=120
    pygame.draw.circle(screen,(193, 225, 193),(big_circle_center_x,big_circle_center_y),R,0)
    divider=2.3
    shift_x=((R*(1/2))+(int(R/divider)))
    shift_y=((R*(1/2))+(int(R/divider)))
    cnt=0
    tmp_list=[]
    for j in range(3):
      for k in range(3):
        x=big_circle_center_x+((R*(1/2))+(j*int(R/divider)))-shift_x
        y=big_circle_center_y+((R*(1/2))+(k*int(R/divider)))-shift_y
        text_x=x   #channel name X座標
        text_y=y-25   #channel name Y座標
        r=int(R/7)
        tp=[]
        for a in range(max_subject_index):
          tp.append(reshaped_avg_spec_per_epoch[a][i][cnt])
        spec_list=tp
        spec=0.0
        channel=Channel(x,y,r,spec,spec_list,percentile_256)
        all_sprites.add(channel)
        tmp_list.append(channel)
        cnt+=1
    channel_obj_list.append(tmp_list)

def gradientRect( screen, left_colour, right_colour, target_rect ):
  """ Draw a horizontal-gradient filled rectangle covering <target_rect> """
  colour_rect = pygame.Surface( ( 2, 2 ) )                                   # tiny! 2x2 bitmap
  pygame.draw.line( colour_rect, left_colour,  ( 0,0 ), ( 1,0 ) )            # left colour line
  pygame.draw.line( colour_rect, right_colour, ( 0,1 ), ( 1,1 ) )            # right colour line
  colour_rect = pygame.transform.smoothscale( colour_rect, ( target_rect.width, target_rect.height ) )  # stretch!
  screen.blit( colour_rect, target_rect )                                    # paint it

def draw_rect_loop(percentile_256):
  # pygame.draw.rect(screen,WHITE,[1275,20,50,256],0) # 畫能量表示圖
  # gradientRect( screen, (0, 255, 0), (0, 100, 0), pygame.Rect( 100,100, 100, 50 ) )
  gradientRect( screen, (255, 0, 0), (0, 0, 255), pygame.Rect( 1250, 20, 50, 200 ) )
  draw_text(screen, str(round(percentile_256[0],2))+"(μV^2)", 16, 1350, 220, BLACK)
  draw_text(screen, str(round(percentile_256[-1],2))+"(μV^2)", 16, 1350, 20, BLACK)
  # draw_text(screen, "(μV^2)", 18, 1368, 20, WHITE)
  # draw_text(screen, "(μV^2)", 18, 1368, 220, WHITE)
  
def draw_circle_loop():
  R=WIDTH/10
  for i in range(5):
    big_circle_center_x=i*(WIDTH/5)+(WIDTH/10)
    big_circle_center_y=120
    pygame.draw.circle(screen,(193, 225, 193),(big_circle_center_x,big_circle_center_y),R-10,0)

def draw_text(surf, text, size, x, y, color):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.centery = y
    surf.blit(text_surface, text_rect)
def draw_line(surf,linecolor,start,end,width):
  pygame.draw.line(surf,linecolor,start,end,width)
def draw_dataframe():
  for k in range(5):
      draw_text(screen, column_list[k], 18, 120+240*k, 295, BLACK)
  for i in range(6):
      draw_line(screen,BLACK,(0+240*i,280),(0+240*i,580),2)
  for i in range(5):
      draw_line(screen,BLACK,(40+240*i,280+30),(40+240*i,580),1)
  for j in range(11):
      draw_line(screen,BLACK,(0,280+30*j),(1200,280+30*j),2)
def draw_circleframe():
  for i in range(2):
    draw_line(screen, BLACK, (0,0+240*i),(1200,0+240*i),2)
  for j in range(6):
    draw_line(screen, BLACK, (0+240*j,0),(0+240*j,240),2)



def draw_bar_chart(now_list,now_list_pos,percentile_256):
  draw_line(screen,BLACK,(0,750),(1200,750),2)
  for i in range(6):
    draw_line(screen,BLACK,(0+i*240,750),(0+i*240,750-1.5*256),2)
  for i in range(5):
      draw_text(screen, column_list[i], 18, 120+240*i, 250, BLACK)
      pygame.draw.rect(screen,return_color(now_list[i][0],percentile_256),[70+240*i,750-round(now_list[i][1]*1.5),100,round(now_list[i][1]*1.5)],0)
      draw_text(screen,str(round(now_list[i][0],3))+"(μV^2)",18,120+240*i,750-round(now_list[i][1]*1.5)-20,BLACK)
      draw_line(screen,BLACK,(now_list_pos[i][0]-20,now_list_pos[i][1]-20),(now_list_pos[i][0]-45,now_list_pos[i][1]-45),2)
      draw_line(screen,BLACK,(now_list_pos[i][0]-20,now_list_pos[i][1]-20),(now_list_pos[i][0]-32,now_list_pos[i][1]-20),2)
      draw_line(screen,BLACK,(now_list_pos[i][0]-20,now_list_pos[i][1]-20),(now_list_pos[i][0]-20,now_list_pos[i][1]-32),2)
  draw_text(screen,"Now Channel: "+channel_list[now_channel_index],30,120+240*2,300,BLACK)


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
    self.percentile_256=percentile_256
    self.image.fill(return_color(self.now_spec,self.percentile_256))
    self.spec_list=spec_list
    self.now_spec_list=self.spec_list[now_subject_index]
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
  def change(self):
    self.now_spec_list=self.spec_list[now_subject_index]
    self.now_spec=self.now_spec_list[self.epoch_count-1]
    self.next_spec=self.now_spec_list[self.epoch_count]

def force_exit():
  pygame.quit()

def run(avg_spec_per_epoch,percentile_256,epoch_leng,music_name):
  force_exit()
  pygame.init()
  pygame.mixer.init()
  global WIDTH
  global LENGTH
  WIDTH,LENGTH=1400-200,700
  AREA=(WIDTH+200,LENGTH+100)
  global screen
  screen=pygame.display.set_mode(AREA)
  global all_sprites
  all_sprites=pygame.sprite.Group()

  global font_name
  font_name = pygame.font.match_font('arial')
  soundwav=pygame.mixer.Sound(f"./{music_name}/{music_name}.mp3")
  WIDTH,LENGTH=1400-200,700
  AREA=(WIDTH+200,LENGTH+100)
  screen=pygame.display.set_mode(AREA)
  pygame.display.set_caption("UI_mode1")
  clock=pygame.time.Clock()
  FPS=8
  WHITE=(255,255,255)
  GREEN=(0,255,0)
  BLACK=(0,0,0)
  YELLOW=(255,255,0)
  second_per_epoch=5
  global now_subject_index
  now_subject_index=0
  max_subject_index=8
  global now_channel_index
  now_channel_index=0
  max_channel_index=9
  channel_list=["F3","C3","P3","Fz","Cz","Pz","F4","C4","P4"]
  column_list=["delta band","theta band","alpha band","beta band","gamma band"]
  interval=260  #表格字體跟圓形的間隔
  display_mode=0 ##0:table  1:bar_plot
  leng=epoch_leng*second_per_epoch
  total_leng=leng
  soundwav.play()
  # all_sprites=pygame.sprite.Group()
  global channel_obj_list
  global reshaped_avg_spec_per_epoch
  channel_obj_list=[]
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
  reshaped_avg_spec_per_epoch=np.array(reshaped_avg_spec_per_epoch)



  # channel_obj_list=[]

  font_name = pygame.font.match_font('arial')


  flag=True 
  screen.fill(WHITE)
  draw_circle(reshaped_avg_spec_per_epoch,percentile_256)
  running=True
  cnt=0
  while running:
    now_channel_list=[]
    position_list=[]
    clock.tick(FPS)
    screen.fill(WHITE)
    if flag:
      draw_rect_loop(percentile_256)
      draw_circle_loop()
      draw_circleframe()
      pygame.mixer.unpause()
      cnt+=1
      if(cnt==FPS):
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
          elif event.key== pygame.K_SPACE:
            flag=False
          elif event.key== pygame.K_RIGHT:
            now_subject_index+=1
            now_subject_index%=8
            for i in range(len(channel_obj_list)):#5
              for j in range(len(channel_obj_list[i])):#9
                channel_obj_list[i][j].change()
          elif event.key== pygame.K_LEFT:
            now_subject_index-=1
            if now_subject_index<0:
              now_subject_index=max_subject_index+now_subject_index
            for i in range(len(channel_obj_list)):#5
              for j in range(len(channel_obj_list[i])):#9
                channel_obj_list[i][j].change()
          elif event.key== pygame.K_DOWN:
            now_channel_index+=1
            now_channel_index%=9

          elif event.key==pygame.K_UP:
            now_channel_index-=1
            if now_channel_index<0:
              now_channel_index=max_channel_index+now_channel_index


          elif event.key==pygame.K_0:
            display_mode=0
          elif event.key==pygame.K_1:
            display_mode=1
      
      
      for i in range(len(channel_obj_list)):#5
        for j in range(len(channel_obj_list[i])):#9
          draw_text(screen, channel_list[j], 16, channel_obj_list[i][j].x, channel_obj_list[i][j].y-25, BLACK)  #印channel name
          if j==now_channel_index:
            now_channel_list.append(return_percentile(channel_obj_list[i][j].now_spec,percentile_256))
            position_list.append([channel_obj_list[i][j].x,channel_obj_list[i][j].y])

          if display_mode==0:
            draw_text(screen, str(round(channel_obj_list[i][j].now_spec_list[channel_obj_list[i][j].epoch_count],3)), 18, 120+i*240, 60+265+j*30, BLACK)
            draw_text(screen,str(channel_list[j]),16,20+240*i,280+30*j+45,BLACK)
      if now_subject_index!=7:
        draw_text(screen, "subject number:"+str(now_subject_index+1), 25, 1300, 740, BLACK)
      else:
        draw_text(screen, "all subject's average", 25, 1300, 740, BLACK)
      draw_text(screen, "RUN", 25, 1360, 770, BLACK)
      draw_text(screen, "Music time(s):", 20, 1280, 710, BLACK)
      draw_text(screen, str(total_leng-leng)+"/"+str(total_leng)+" s", 20, 1360, 710, BLACK)
      if display_mode==0:
        draw_dataframe()
        draw_text(screen,"Spectrum Table",25,600,770,BLACK)
      else:
        draw_bar_chart(now_channel_list,position_list,percentile_256)
        draw_text(screen,"Spectrum Bar Chart",25,600,770,BLACK)
      all_sprites.update()

    else:
      draw_rect_loop(percentile_256)
      draw_circle_loop()
      draw_circleframe()
      pygame.mixer.pause()
      for event in pygame.event.get():
        if event.type==pygame.QUIT:
          running=False
        elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False
                elif event.key==pygame.K_SPACE:
                    flag=True
                elif event.key== pygame.K_RIGHT:
                  now_subject_index+=1
                  now_subject_index%=8
                  for i in range(len(channel_obj_list)):#5
                    for j in range(len(channel_obj_list[i])):#9
                      channel_obj_list[i][j].change()
                elif event.key== pygame.K_LEFT:
                  now_subject_index-=1
                  if now_subject_index<0:
                    now_subject_index=max_subject_index+now_subject_index
                  for i in range(len(channel_obj_list)):#5
                    for j in range(len(channel_obj_list[i])):#9
                      channel_obj_list[i][j].change()
                elif event.key== pygame.K_DOWN:
                  now_channel_index+=1
                  now_channel_index%=9
                  # for i in range(len(channel_obj_list)):#5
                  #   for j in range(len(channel_obj_list[i])):#9
                  #     channel_obj_list[i][j].change()
                elif event.key==pygame.K_UP:
                  now_channel_index-=1
                  if now_channel_index<0:
                    now_channel_index=max_channel_index+now_channel_index
                  # for i in range(len(channel_obj_list)):#5
                  #   for j in range(len(channel_obj_list[i])):#9
                  #     channel_obj_list[i][j].change()
                elif event.key==pygame.K_0:
                  display_mode=0
                elif event.key==pygame.K_1:
                  display_mode=1
      draw_text(screen, "Music time(s):", 20, 1280, 710, BLACK)
      draw_text(screen, str(total_leng-leng)+"/"+str(total_leng)+" s", 20, 1360, 710, BLACK)
      if now_subject_index!=7:
        draw_text(screen, "subject number:"+str(now_subject_index+1), 25, 1300, 740, BLACK)
      else:
        draw_text(screen, "all subject's average", 25, 1300, 740, BLACK)
      draw_text(screen, "PAUSE", 25, 1360, 770, BLACK)
      for i in range(len(channel_obj_list)):#5
        for j in range(len(channel_obj_list[i])):#9
          if j==now_channel_index:
            now_channel_list.append(return_percentile(channel_obj_list[i][j].now_spec,percentile_256))
            position_list.append([channel_obj_list[i][j].x,channel_obj_list[i][j].y])
          draw_text(screen, channel_list[j], 16, channel_obj_list[i][j].x, channel_obj_list[i][j].y-25, BLACK)  #印channel name
          pygame.draw.circle(screen,return_color(channel_obj_list[i][j].now_spec,percentile_256),(channel_obj_list[i][j].x,channel_obj_list[i][j].y),channel_obj_list[i][j].r,0)
          if display_mode==0:
            draw_text(screen, str(round(channel_obj_list[i][j].now_spec_list[channel_obj_list[i][j].epoch_count],3)), 18, 120+i*240, 265+j*30+60, BLACK)
            draw_text(screen,str(channel_list[j]),16,20+240*i,280+30*j+45,BLACK)
      if display_mode==0:
        draw_dataframe()
        draw_text(screen,"Spectrum Table",25,600,770,BLACK)
      else:
        draw_bar_chart(now_channel_list,position_list,percentile_256)
        draw_text(screen,"Spectrum Bar Chart",25,600,770,BLACK)

    
    all_sprites.draw(screen)

    pygame.display.update()

  pygame.mixer.music.stop()
  pygame.quit()

# return 0

# print(channel_obj_list[0][0].epoch_count)

