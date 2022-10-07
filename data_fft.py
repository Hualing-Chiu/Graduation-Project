# encoding:utf-8
import sys
sys.getdefaultencoding()
import numpy as np 
from scipy.fftpack import fft,ifft 
import matplotlib.pyplot as plt 
from matplotlib.pylab import mpl 
#mpl.rcParams['font.sans-serif'] = ['SimHei'] #顯示中文 
mpl.rcParams['axes.unicode_minus']=False #顯示負號 
def do_fft(sampling_rate,time_window,y):
	x=np.linspace(0,time_window,sampling_rate*time_window) 
	fft_y=fft(y) #快速傅立葉變換 
	N= sampling_rate*time_window
	x = np.arange(N) # 頻率個數 
	half_x = x[range(int(N/2))] #取一半區間 
	abs_y=np.abs(fft_y) # 取複數的絕對值，即複數的模(雙邊頻譜) 
	angle_y=np.angle(fft_y) #取複數的角度 
	normalization_y=abs_y/N #歸一化處理（雙邊頻譜） 
	normalization_half_y = normalization_y[range(int(N/2))] #由於對稱性，只取一半區間（單邊頻譜） 

	five_band=[]
	five_band.append(round(sum(normalization_half_y[0:4])/len(normalization_half_y[0:4]),3)) #delta_band
	five_band.append(round(sum(normalization_half_y[4:9])/len(normalization_half_y[4:9]),3)) #theta_band
	five_band.append(round(sum(normalization_half_y[8:13])/len(normalization_half_y[8:13]),3)) #alpha_band
	five_band.append(round(sum(normalization_half_y[12:31])/len(normalization_half_y[12:31]),3)) #beta_band
	five_band.append(round(sum(normalization_half_y[30:51])/len(normalization_half_y[30:51]),3)) #gamma_band

	return five_band
