# Brainwave_Analysis_project
> ### 指導教授：梁勝富
> ### 專題成員：莊上緣、江柏諺、邱華苓、洪誼臻
> ### 作者:成功大學資訊工程學系 112級 莊上緣

## 簡介
> #### &emsp;&emsp;腦波與人類的心理狀態，包括專注力、心理壓力與意識活動的關聯性，在生醫與腦科學領域一直以來都是令人十分感興趣的主題之一，而新聞或研究指出：腦波可受音樂調整或促進，因此我們對此議題進行探討與分析。
> #### &emsp;&emsp;而腦波種類依頻率大致分為alpha波（8～12Hz，放鬆與冥想）、beta波（12～30Hz，警覺、思考與心情緊張）、delta波（0.1～3Hz，深層睡眠），gamma波（＞30Hz，感官協調）、theta波（4～8Hz，潛意識、長期記憶）。
> #### &emsp;&emsp;我們利用網路上標榜能增強上述特定腦波的音樂，蒐集受試者聆聽音樂時的腦波，並使用短時距傅立葉分析搭配EEGLAB套件環境，生成並顯示對應的腦波分析結果。將這些結果與受試者聆聽白噪音時的常態腦波進行比較，觀察各種腦波音樂對於誘發出特定腦波的效果。
> #### &emsp;&emsp;為了方便實驗觀察與資料顯示，我們設計了一套動態視覺化UI介面，將腦波的原始檔案經EEGLAB進行依些前處理後就匯入此套介面。這套介面設計之初並沒有進行模組化，因此每個介面要執行時必須個別在命令列打入不同的執行指令，且無法讓使用者自由切換想觀測的音樂以及想使用的UI模式，因此我就應用了類似於MVC架構的理念，用pyQt5的Qt Designer設計了一個主控台，並將原本的四種UI模式模組化後統整成3個模式並各自包裝成副程式，所以目前的介面可以讓使用者由主控台自由選擇音樂與UI模式。
----------------------------------------------------
## 系統架構圖(總覽)
![](https://i.imgur.com/szZyy0u.png)
----------------------------------------------------
## MATLAB與EEGLAB資料前處理操作DEMO影片連結:
> #### [https://youtu.be/ChDR9dAhYYc](https://youtu.be/ChDR9dAhYYc)
-----------------------------------------------------------

## 系統架構圖(動態介面)
![](https://i.imgur.com/7q3t3Ng.png)

## 環境與python package
### 測試環境:Windows 10
### 軟體工具:MATLAB R2021A,Visual Studio Code,Qt Designer,Python 3.8.0

-------------------------------------
### 以下為相關package版本
Package                  Version
------------------------ ---------
MarkupSafe               2.0.1
------------------------ ---------
matplotlib               3.5.1
------------------------ ---------
matplotlib-inline        0.1.3
------------------------ ---------
numpy                    1.21.5
------------------------ ---------
pygame                   2.1.2
------------------------ ---------
PyQt5                    5.15.6
------------------------ ---------
PyQt5-Qt5                5.15.2
------------------------ ---------
PyQt5-sip                12.9.0
------------------------ ---------
PySide2                  5.15.2.1
------------------------ ---------
scipy                    1.4.1
------------------------ ---------
shiboken2                5.15.2.1
------------------------ ---------
statistics               1.0.3.5
------------------------ ---------

## 執行方式
### 前往這份repo的對應路徑:
> #### \Brainwave_Analysis_project\UI_with_pyQt
### 接著在命列列輸入以下指令即可
> #### python Brainwave_UI_MainWindow_main_controller.py
### 在主控台即可選擇欲觀察之音樂及UI模式，也可以按HELP查看User's Guide
### 選擇好音樂及UI模式後即可按START開始執行對應的UI模式
![](https://i.imgur.com/PFcOGhe.png)


## 本次專題之簡介檔案連結:
> #### [https://drive.google.com/file/d/144-oSXoARIjn0BuPaMUIhiROfzyBg0qp/view?usp=sharing](https://drive.google.com/file/d/144-oSXoARIjn0BuPaMUIhiROfzyBg0qp/view?usp=sharing)
## 本次專題之簡報連結:
> #### [https://drive.google.com/file/d/1jUJ94tHr-l9WM6fm2UHJCmLpE8bmM7Pn/view?usp=sharing](https://drive.google.com/file/d/1jUJ94tHr-l9WM6fm2UHJCmLpE8bmM7Pn/view?usp=sharing)

## 本次專題之專題展參展影片連結:

> #### [https://youtu.be/n02rIqxe-KI](https://youtu.be/n02rIqxe-KI)

## 動態介面DEMO影片連結:
> #### [https://youtu.be/epRa3JlG6rw](https://youtu.be/epRa3JlG6rw)

## 本次專題的受試者腦波原始檔、經過前處理後的腦波檔、腦波音樂以及eeglab的相關函式庫之雲端連結:
> #### [https://drive.google.com/drive/folders/1ZraqQW24qmIm9BV0siA5MPDQMfYdX3FX?usp=sharing](https://drive.google.com/drive/folders/1ZraqQW24qmIm9BV0siA5MPDQMfYdX3FX?usp=sharing)

## 與專題相關的一些整理之hackmd紀錄:
> #### [https://hackmd.io/@shangyuan191/H1PbWZI7q](https://hackmd.io/@shangyuan191/H1PbWZI7q)

#### 陽明交通大學 盧家鋒教授的生醫訊號分析相關概念與實作、MATLAB與EEGLAB教學網址:
> #### [https://www.ym.edu.tw/~cflu/CFLu_course_matlabsig.html](https://www.ym.edu.tw/~cflu/CFLu_course_matlabsig.html)
 