from operator import delitem
import os
import sys
import math
import pygame
import data_fft
import scipy.io as sio
import matplotlib.pyplot as plt
import pandas as pd
import statistics as stat
import data_fft
import numpy as np
original_name=['alpha','beta','delta','gamma','theta','white_noise']
data_path=[]
music_path=[]
for i in range(6):
  temp=[]
  for j in range(7):
    temp.append('./'+original_name[i]+'/'+original_name[i]+'_subject'+str(j+1))
  data_path.append(temp)
  music_path.append(f"./{original_name[i]}/{original_name[i]}.mp3")
# print(data_path)
# print(music_path)

def return_spec_time_sequential_per_epoch(fi):
  data1=sio.loadmat(fi)
  data=data1['EEG'].tolist()
  time_sequential_with_every_channel_dB=[]
  for i in range(len(data[0][0][15])):
    channel=[]
    for j in range(len(data[0][0][15][0][0])):
      epoch=[]
      for k in range(len(data[0][0][15][0])):
        epoch.append(data[0][0][15][i][k][j])
      channel.append(epoch)
    time_sequential_with_every_channel_dB.append(channel)



  time_sequential_per_epoch_with_every_channel_dB=[]
  for i in range(len(time_sequential_with_every_channel_dB)):  #9
    tmp=[]
    for j in range(len(time_sequential_with_every_channel_dB[0])):##48 or 53 or 54
      ttmp=data_fft.do_fft(1000,5,time_sequential_with_every_channel_dB[i][j][1000:])

      
      tmp.append(ttmp)
    time_sequential_per_epoch_with_every_channel_dB.append(tmp)




  

  return time_sequential_per_epoch_with_every_channel_dB

def get_avg():
  # all_data=[]
  # epoch_leng=40
  # for i in range(len(data_path)):  ## 6 music
  #   temp=[]
  #   print(f"\nLoad data:listening {original_name[i]} music...")
  #   for j in range(len(data_path[i])):  ## 7 subject
  #     temp.append(return_spec_time_sequential_per_epoch(data_path[i][j]))
  #     print('done! ('+str(i+1)+'/'+str(len(data_path))+')'+':'+'('+str(j+1)+'/'+str(len(data_path[i]))+')')
  #   all_data.append(temp)



  # for i in range(len(all_data)):
  #   for j in range(len(all_data[i])):
  #     for k in range(len(all_data[i][j])):
  #       del all_data[i][j][k][epoch_leng:]
  

  # all_subject=[]
  # for k in range(len(all_data)):
  #   all_subject_music=[]
  #   for i in range(len(all_data[k])):
    
  #     tmp=[]
  #     for j in range(len(all_data[k][i])):
  #       tmp.append(all_data[k][i][j])
  #     all_subject_music.append(tmp)
    
  #   subject_avg=[]

  #   for x in range(len(all_data[k][0])): #9
  #     temp=[]
  #     for y in range(len(all_data[k][0][x])):#53
  #       tmp=[]
  #       for z in range(len(all_data[k][0][x][y])): #5
  #         sum=0.0
  #         for w in range(len(all_data[k])):
  #           sum+=all_data[k][w][x][y][z]
  #         tmp.append(round(sum/len(all_data[k]),3))
          

  #       temp.append(tmp)
  #     subject_avg.append(temp)
  #   all_subject_music.append(subject_avg)
  #   all_subject.append(all_subject_music)
  percentile=256
  percentile_256=[]
  # all_data=np.array(all_subject)
  # with open('all_data.txt','w') as outfile:
  #   for slice_4d in all_data:
  #     for slice_3d in slice_4d:
  #       for slice_2d in slice_3d:
  #         np.savetxt(outfile,slice_2d,fmt='%f',delimiter=',')
  all_data=np.loadtxt('all_data.txt',delimiter=',').reshape((6,8,9,40,5))
  for i in range(0,percentile+1):
    percentile_256.append(np.percentile(all_data,i*(100/percentile)))
  return all_data,percentile_256,40,music_path
      
        

