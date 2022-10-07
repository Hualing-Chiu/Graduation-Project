clc
clear all;
close all;

folder = dir('*');
folder = folder(3:end);

for i = 1:length(folder)
    if folder(i).isdir == 1
        cd( folder(i).name )
        disp(folder(i).name)
        folder(i).name
        [rjfile, EEGband,spec] = EEGproceV1_7();
        if isempty(rjfile)~=1
            filename = [folder(i).name 'RJ.xlsx'];
            writecell(rjfile, filename);
        end
         if isempty(EEGband)~=1
            filename = [folder(i).name 'band.mat'];
            
            spec_table = array2table(EEGband, 'VariableNames' ,...
            {'Filename', ' Delta 1-4Hz', 'Theta 5-7Hz', 'Alpha 8-12Hz', 'Low-beta 13-16Hz', 'Mid-Beta 17-20Hz', 'High-bata 21-28Hz'...
             , 'All-bata', 'Low Gama 30-50Hz '});
            save(filename, 'spec_table','spec');
        end
        cd .. ;
    else 
        continue
    end
end

function [rjfile, EEGband,spec] = EEGproceV1_7()
    file = dir('*.cnt'); % 找資料夾內所有.cnt 檔案
     rjfile = {}; ;
     EEGband = {};
     spec=0;
    for i = 1:length(file)
       [ALLEEG EEG CURRENTSET ALLCOM] = eeglab;
       file(i).name          
%        EEG = pop_loadcnt([file(i).folder '\'  file(i).name] , 'dataformat', 'auto', 'keystroke', 'on', 'memmapfile', '');
       EEG = pop_loadcnt([file(i).folder '\'  file(i).name] , 'dataformat', 'auto', 'memmapfile', '');
       %D:\NCKUCSIE\grade3\grade3-2\Project\Brainwave_project_ui\Brainwave_Analysis_project
       EEG=pop_chanedit(EEG, 'lookup','D:\\NCKUCSIE\\grade3\\grade3-2\\Project\\Brainwave_project_ui\\Brainwave_Analysis_project\\eeglab_resource\\eeglab14_1_2b\\plugins\\dipfit2.3\\standard_BESA\\standard-10-5-cap385.elp');
       EEG = pop_select( EEG,'channel',{'Cz' 'F3' 'C3' 'P3' 'F4' 'C4' 'P4' 'Pz' 'Fz'}); %%這邊很重要請寫你有採用的通道, 或著你不改也可以
       EEG = pop_eegfiltnew(EEG, 0.5,65,6600,0,[],0);
       time_point = [];
       time_point(:,2) = 5:5:(floor(EEG.xmax)-5); %%這邊是取開始錄製前5秒->錄製結束前5秒進行處理, 每5秒做一個區間間格標記, 這邊你們能自己決定不建議少於2秒
       if length( time_point(:,2)) <= 24
           continue
           index = size(rjfile,1);
           rjfile{index+1,1} = file(i).name(1:end-4);
           rjfile{index+1,2} = 0
           rjfile{index+1,3} = 0
           rjfile{index+1,4} = 0
       end
       EEG.event = [];
       EEG = pop_importevent( EEG, 'append','no','event', [time_point] ,'fields',{'type' 'latency'},'timeunit',1);
       EEG = pop_epoch( EEG, {  }, [-1  5], 'newname', 'CNT file epochs', 'epochinfo', 'yes'); %%取每個事件前1秒與事件後5秒進行前處理
       epoch_num = size(EEG.epoch, 2);
       EEG = pop_rmbase( EEG, [-1000    0]);%%取每個事件前1秒訊號進行校正
%        EEG = pop_eegthresh(EEG,1, [1:8] ,-110,110,0,4.999,0,1);%%標記振幅超過+-75uv
%        [EEG, rj_index] = pop_rejspec( EEG, 1,'elecrange',[1:8] ,'method','multitaper','threshold',[-40 40] ,'freqlimits',[1 50], 'eegplotreject',1); %%使用頻譜能量進行造訊移除這邊定義 40dB
       
        %%頻譜過濾範圍1-50Hz
       rj_index=0;
       if  size(EEG.epoch, 2) >= 24 %%檢查可用的 epoch 數超過24個也就是2分鐘, 你們要自己修改福和你們的範圍
           filename = [file(i).name(1:end-4) '.set'];
           EEG =  pop_saveset( EEG, filename);
           [spec, freq] = eegspecplot(EEG);
   
           %%頻譜能量 dB 轉 uv 
           spec = db2pow(spec);
           filename = [file(i).name(1:end-4) 'CRT.mat'];
           save(filename, 'spec', 'freq', 'rj_index', 'epoch_num');
           
           %%這邊取能量帶寬的平均值
           index_s = size(EEGband,1);
           EEGband{index_s+1,1} = file(i).name(1:end-4);
           EEGband{index_s+1,2} = mean(spec(:, 2:5) ,  2);
           EEGband{index_s+1,3} = mean(spec(:, 6:8) ,  2);
           EEGband{index_s+1,4} = mean(spec(:, 9:13) ,  2);
           EEGband{index_s+1,5} = mean(spec(:, 14:17) ,  2);
           EEGband{index_s+1,6} = mean(spec(:, 18:21) ,  2);
           EEGband{index_s+1,7} = mean(spec(:, 22:29) ,  2);
           EEGband{index_s+1,8} = mean(spec(:, 14:29) ,  2);
           EEGband{index_s+1,9} = mean(spec(:, 31:51) ,  2);
       else
           index = size(rjfile,1);
           rjfile{index+1,1} = file(i).name(1:end-4);
           rjfile{index+1,2} = length(rj_index);
           rjfile{index+1,3} = epoch_num;
           rjfile{index+1,4} = length(rj_index)/ epoch_num;
       end
       close all;
       clear EEG;
    end
end

function [spec, freq] = eegspecplot(EEG) 
    if isempty(EEG.event)~=1
        [spec, freq] =  pop_spectopo(EEG, 1, [-1000  4999], 'EEG' , 'percent', 100, 'freqrange',[1 50],'electrodes','on' ,'plot' ,'on');
        filename = [EEG.filename(1:end-3) '.bmp']
        saveas(gcf,filename)
    end
end