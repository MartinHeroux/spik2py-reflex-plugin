import matplotlib.pyplot as plt
import numpy as np


from spik2py_reflex_plugin.Parse_Avg import Parse_Avg
class Grouped_Graph:
    def __init__(self,filepath,list,parsesettings):
        self.list=list
        self.filepath=filepath
        self.parsesettings=parsesettings

    def generate_paired_graph(self):
        grouped_data=[]
        fig2paried, ax2 = plt.subplots(nrows=len(self.list) if len(self.list) > 0 else 1, ncols=2,sharey=True,sharex=True)
        for ppindex,pp in enumerate(self.list):
            allwaveform1=[]
            allwaveform2=[]
            allbaselinewaveform=[]
            for wave in pp:

                timeaxis = np.linspace(0,self.parsesettings.predouble+self.parsesettings.postdouble, num=len(wave.pulse1.waveform))
                timeaxis2=np.linspace(0, self.parsesettings.predouble+self.parsesettings.postdouble, num=len(wave.pulse2.waveform))
              
                
                allwaveform1.append(wave.pulse1.waveform)
                allwaveform2.append(wave.pulse2.waveform)
                allbaselinewaveform.append(wave.entirewaveform)
                try:
                    if ppindex==0:
                        ppindex=ppindex
                    else:
                        ppindex=ppindex*2
                        
                    ax2[ppindex].plot(timeaxis,wave.pulse1.waveform,color=(0.8, 0.8, 0.8))
                    ax2[ppindex+1].plot(timeaxis2,wave.pulse2.waveform,color=(0.8, 0.8, 0.8))
                    #ax2[ppindex][0].plot(x_new,TKEOarray,color="green")
                    ax2[ppindex].text(0.95, 0.95, f" {wave.intensity}", transform=ax2[ppindex].transAxes, ha='right', va='top')
                except:
                    pass

                
            max_len_first_array = max(len(arr) for arr in allwaveform1)
            max_len_second_array = max(len(arr) for arr in allwaveform2)
            max_len_entire_array = max(len(arr) for arr in allbaselinewaveform)
            
            # Resize the arrays to have the same shape
            
            resized_list_1 = [np.resize(arr, (max_len_first_array,)) for arr in allwaveform1]
            resized_list_2 = [np.resize(arr, (max_len_second_array,)) for arr in allwaveform2]
            resized_entirewaveform=[np.resize(arr, (max_len_entire_array)) for arr in allbaselinewaveform]
            avg_arr_1 = np.mean(resized_list_1, axis=0)
            avg_arr_2 = np.mean(resized_list_2, axis=0)
            avg_entirewaveform=np.mean(resized_entirewaveform,axis=0)

            avg_timeaxis_1 = np.linspace(0,  self.parsesettings.predouble+self.parsesettings.postdouble, num=len(avg_arr_1))
            avg_timeaxis_2 = np.linspace(0,  self.parsesettings.predouble+self.parsesettings.postdouble, num=len(avg_arr_2))
           
            ax2[ppindex].plot(avg_timeaxis_1,avg_arr_1,color='red') 
            ax2[ppindex+1].plot(avg_timeaxis_2,avg_arr_2,color='red') 
            # Resize the arrays to have the same shape

           
            data=Parse_Avg().Parse_Double(avg_arr_1,avg_arr_2,avg_timeaxis_1,avg_timeaxis_2,pp[0].intensity,avg_entirewaveform)
            grouped_data.append({"intensity":pp[0].intensity,"data":data})
        plt.savefig(f"{self.filepath}_grouped_paired.png",dpi = 300,orientation='landscape')
        plt.close()
        return grouped_data

    

    def generate_group_graph(self,name):
        fig1single, ax1 = plt.subplots(nrows=len(self.list) if len(self.list) > 0 else 1, ncols=1,sharey=True,sharex=True)
        grouped_data=[]
    
        time_elapsed:any
        if self.list[0][0].name=="single_trans_pulse":
            time_elapsed=self.parsesettings.pretrains+self.parsesettings.posttrains
        elif  self.list[0][0].name=="singlepulse":
            time_elapsed=self.parsesettings.presingle+self.parsesettings.postsingle


        for ppindex,pp in enumerate(self.list):
            allwaveforms=[]
            subgraph:any
            try:
                subgraph=ax1[ppindex]
            except:
                subgraph=ax1
                
                
            for wave in pp:
                timeaxis = np.linspace(0, time_elapsed, num=len(wave.waveform))
                x_new = timeaxis
                print(wave)
                allwaveforms.append(wave.waveform)

                
                subgraph.plot(x_new,wave.waveform,color=(0.8, 0.8, 0.8))
            max_len = max(len(arr) for arr in allwaveforms)
           
            # Resize the arrays to have the same shape
            
            resized_list = [np.resize(arr, (max_len,)) for arr in allwaveforms]
            avg_arr = np.mean(resized_list, axis=0)
            avg_timeaxis = np.linspace(0,  time_elapsed, num=len(avg_arr))
           
            subgraph.plot(avg_timeaxis,avg_arr,color='red')
            subgraph.text(0.95, 0.95, f" {pp[0].intensity}", transform=subgraph.transAxes, ha='right', va='top')
            if pp[0].name=="single_trans_pulse":
            
                data=Parse_Avg().Parse_Trains_Single(avg_arr,avg_timeaxis,pp[0].intensity)
                grouped_data.append({"intensity":pp[0].intensity,"data":data})
            else:
                data=Parse_Avg().Parse_Single(avg_arr,avg_timeaxis,pp[0].intensity)
                grouped_data.append({"intensity":pp[0].intensity,"data":data})

        
        plt.savefig(f"{self.filepath}_grouped_{name}_.png",dpi = 300,orientation='landscape')
        plt.close()
        return grouped_data

          