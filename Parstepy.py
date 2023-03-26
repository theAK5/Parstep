import sys,os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks 
from matplotlib.widgets import Slider,Button

#Reading data
filename = sys.argv[1]
path = os.getcwd()
file = os.path.join(path,filename)
# df = pd.read_csv(r'~/Dropbox/Test/test.txt',sep='\t')
ch = int(input('Channel number:'))
df = pd.read_csv(file,sep='\t')
n = len(df)
D = [df['data{}'.format(ch)][i] for i in range(n)]
time = [df['t'][i] for i in range(n)] 


#Some postprocessing
mean_int= []
std_mean_int= []
dif = 5 
for i in range(dif,n-dif):
    mean_int.append(np.mean(D[i-dif:i+dif]))
for i in range(dif,n-dif):
     std_mean_int.append(np.std(mean_int[i-dif:i+dif]))

n_datapts = int(input('Enter data window size:')) 

#Finding the peaks(separators)
spike_data = np.array(std_mean_int)
data = np.array(D)
spike_time = np.array(time[dif:n-dif])
np_time = np.array(time)
cmax_index,_ = find_peaks(spike_data,height= 30,distance = 70)
windows = []
datapoints = []
#Slicing of signal
def slice(cmax_index):
    windows.clear() 
    datapoints.clear()
    for i in range(len(cmax_index)):
        try: 
            mid = (int((cmax_index[i]+cmax_index[i+1])/2))+ dif
        except:
            mid = (int((cmax_index[i]+n)/2))+ dif
        ext = int(n_datapts/2)
        if(mid+ext<n):
            windows.extend(range(mid-ext,mid+ext))
            datapoints.append(range(mid-ext,mid+ext))
#Functions for sliders and the buttons
def plot(): 
    main_ax.clear()
    main_ax.plot(time,D)
    main_ax.plot(time[dif:n-dif],std_mean_int)
    main_ax.plot(spike_time[cmax_index], spike_data[cmax_index],'b.')
    main_ax.plot(np_time[windows],data[windows],'r.')

def update_d(val):
    global cmax_index
    cmax_index,_ = find_peaks(spike_data,height= slider_h.val,distance = val)
    slice(cmax_index)
    plot()

def update_h(val):
    global cmax_index
    cmax_index,_ = find_peaks(spike_data,height= val,distance = slider_d.val)
    slice(cmax_index)
    plot()

def save_it(val):
    results_mean = [np.mean(data[d]) for d in datapoints]
    results_SD = [np.std(data[d]) for d in datapoints]
    results = {'Mean':results_mean,'SD':results_SD}
    result_df = pd.DataFrame(results)
    result_df.to_excel('{}_CH{}_parsed.xlsx'.format(filename.split(".")[0],ch),index= False)     
    print('Saved in {}_CH{}_parsed.xlsx!'.format(filename.split(".")[0],ch))
#Setting up interactive plot
fig = plt.figure(figsize=(9,7))
main_ax = plt.axes()
fig.subplots_adjust(bottom=0.25)
sliderh_ax  = fig.add_axes([0.1,0.10,0.8,0.05])
sliderd_ax  = fig.add_axes([0.1,0.05,0.8,0.05])
save_button_ax = fig.add_axes([0.8, 0.01, 0.1, 0.04])

#Setting up slider and button
slider_h= Slider(sliderh_ax, 'Height', 0,1000, valinit=30,valstep=1)
slider_d= Slider(sliderd_ax, 'Distance', 0,100, valinit=70,valstep=1)
slider_h.on_changed(update_h)
slider_d.on_changed(update_d)
save_button_ax = fig.add_axes([0.8, 0.01, 0.1, 0.04])
save_button = Button(save_button_ax, 'Save')
save_button.on_clicked(save_it)

#Plotting
slice(cmax_index)
plot()
plt.show()
