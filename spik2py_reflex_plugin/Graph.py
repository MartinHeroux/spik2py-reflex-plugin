import matplotlib.pyplot as plt
import numpy as np
from spik2py_reflex_plugin import compute_outcome_measures
from spik2py_reflex_plugin.Parse_Signals import Parse_Avg

class Base_Graph:
    def __init__(self,trial,parsedresults,triggercleaned,triggeruncleaned,range,filepath):
        self.trial=trial
        self.results= parsedresults
        self.triggercleaned=triggercleaned
        self.triggeruncleaned=triggeruncleaned
        self.userstarttime= range["userstarttime"]
        self.userendtime= range["userendtime"]
        self.filepath=filepath


        
    def generate_individual_graph(self):
    
        fig, (ax1, ax2,ax5,ax4) = plt.subplots(4, 1, sharex=True,figsize=(10, 6))
        ax1.eventplot(self.triggercleaned, orientation='horizontal', colors='g')
        ax2.eventplot(self.triggeruncleaned, orientation='horizontal', colors='r')
        
        
        ax4.plot(self.trial.Fdi.times,self.trial.Fdi.values)
        
        ax5.plot(self.trial.Stim.times,self.trial.Stim.values)
        
    
        plt.xlim(self.userstarttime, self.userendtime)
        
        plt.ylim(-1,1)
        
        
        plt.savefig(self.filepath,dpi = 300,orientation='landscape')
        
       
        gg=fig.text(0.5, 0.95, f"hi", ha='center', va='top')
        gg.remove()

        for i , x in enumerate(self.results):
            if  x.name=="singlepulse":
                ymax= np.max(np.array(self.trial.Fdi.values[x.triggerindex:x.endindex]))
                ymin= np.min(np.array(self.trial.Fdi.values[x.triggerindex:x.endindex]))
                y_range = ymax - ymin
               
                plt.xlim([self.trial.Fdi.times[x.triggerindex],  self.trial.Fdi.times[x.endindex]])
                text1 = fig.text(0.5, 0.95, f"hi", ha='center', va='top')
                text2 = fig.text(0.9, 0.90, f"Onset:{round(x.relativeonset, 2)}" if x.onset is not None else "", ha='center', va='top')
                text3 = fig.text(0.9, 0.80, f"Area:{round(x.area, 2)}" if x.area is not None else "", ha='center', va='top')
                text4 = fig.text(0.9, 0.70, f"peak to peak:{round(x.peak_to_peak, 2)}" if x.peak_to_peak is not None else "", ha='center', va='top')

                
                plt.ylim([ymin - 0.1*y_range,ymax +0.1*y_range])
                fig.text(0.5, 0.95, "hi", ha='center', va='top')
                
                
                
                plt.savefig(f"{self.filepath}_{i}.png",dpi = 300,orientation='landscape')
                text_objects = [text1, text2,text3, text4]

        # remove the text objects
                for text_obj in text_objects:
                    text_obj.remove()

                

            elif x.name=="single_trans_pulse":
                #disabling the generation of trains_graph
                """
                ymax= np.max(np.array(yy1[x.triggerindex:x.endindex]))
                ymin= np.min(np.array(yy1[x.triggerindex:x.endindex]))
                y_range = ymax - ymin
                print(ymax)
                print(ymin)
                plt.xlim([xx1[x.triggerindex]-0.01,  parseddata.Fdi.times[x.endindex]+0.001])
                
                
                plt.ylim([ymin - 0.1*y_range,ymax +0.1*y_range])
                text1 = fig.text(0.5, 0.95, f"{filedataname}", ha='center', va='top')
                text2 = fig.text(0.9, 0.90, f"Onset:{round(x.relativeonset, 2)}" if x.onset is not None else "", ha='center', va='top')
                text3 = fig.text(0.9, 0.80, f"Area:{round(x.area, 2)}" if x.area is not None else "", ha='center', va='top')
                text4 = fig.text(0.9, 0.70, f"peak to peak:{round(x.peak_to_peak, 2)}" if x.peak_to_peak is not None else "", ha='center', va='top')
                    
                plt.savefig(f"{file_path}_{i}.png",dpi = 300,orientation='landscape')
                text_objects = [text1, text2,text3, text4]

                # remove the text objects
                for text_obj in text_objects:
                    text_obj.remove()
                """


            elif x.name=="pairedpulse":
                
                
                ymax= np.max(np.array(self.trial.Fdi.values[x.pulse1.triggerindex:x.pulse2.endindex]))
                ymin= np.min(np.array(self.trial.Fdi.values[x.pulse1.triggerindex:x.pulse2.endindex]))
                print(ymax)
                print(ymin)
                y_range = ymax - ymin
                plt.xlim([self.trial.Fdi.times[x.pulse1.triggerindex],  self.trial.Fdi.times[x.pulse2.endindex]])
                
                plt.ylim([ymin - 0.1*y_range,ymax +0.1*y_range])
                text1 = fig.text(0.5, 0.95, f"hi", ha='center', va='top')
                text2 = fig.text(0.5, 0.90, f"Onset1: {round(x.pulse1.relativeonset, 2) if x.pulse1.onset is not None else ''}", ha='center', va='top')
                text3 = fig.text(0.5, 0.80, f"Onset2: {round(x.pulse2.relativeonset, 2) if x.pulse2.onset is not None else ''}", ha='center', va='top')
                text4 = fig.text(0.9, 0.90, f"Area1: {round(x.pulse1.area, 2) if x.pulse1.area is not None else ''}", ha='center', va='top')
                text5 = fig.text(0.9, 0.80, f"Area2: {round(x.pulse2.area, 2) if x.pulse2.area is not None else ''}", ha='center', va='top')
                text6 = fig.text(0.9, 0.70, f"Peak to peak1: {round(x.pulse1.peak_to_peak, 2) if x.pulse1.peak_to_peak is not None else ''}", ha='center', va='top')
                text7 = fig.text(0.9, 0.60, f"Peak to peak2: {round(x.pulse2.peak_to_peak, 2) if x.pulse2.peak_to_peak is not None else ''}", ha='center', va='top')
                text8 = fig.text(0.9, 0.50, f"Peak to peak ratio: {round(x.peak_to_peak_ratio, 2) if x.peak_to_peak_ratio is not None else ''}", ha='center', va='top')
                text9 = fig.text(0.9, 0.40, f"area ratio: {round(x.area_ratio, 2) if x.area_ratio is not None else ''}", ha='center', va='top')

                
                plt.savefig(f"{self.filepath}_{i}_paired.png",dpi = 300,orientation='landscape')
                
                text_objects = [text1, text2,text3, text4,text5,text6,text7,text8,text9]
                
                
                # remove the text objects
                for text_obj in text_objects:
                    text_obj.remove()
            
            
            
            #ax4.vlines(x=list(filter(lambda x: x is not None, masteronset)), ymin=ax4.get_ylim()[0], ymax=ax4.get_ylim()[1], colors='red', ls=':', lw=1, label='vline_single - full height')
        
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

            avg_timeaxis_1 = np.linspace(0,  200, num=len(avg_arr_1))
            avg_timeaxis_2 = np.linspace(0,  200, num=len(avg_arr_2))
           
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
            for wave in pp:
                timeaxis = np.linspace(0, time_elapsed, num=len(wave.waveform))
                x_new = timeaxis
                print(wave)
                allwaveforms.append(wave.waveform)

                
                ax1[ppindex].plot(x_new,wave.waveform,color=(0.8, 0.8, 0.8))
            max_len = max(len(arr) for arr in allwaveforms)
            print(max_len)
            # Resize the arrays to have the same shape
            
            resized_list = [np.resize(arr, (max_len,)) for arr in allwaveforms]
            avg_arr = np.mean(resized_list, axis=0)
            avg_timeaxis = np.linspace(0,  time_elapsed, num=len(avg_arr))
           
            ax1[ppindex].plot(avg_timeaxis,avg_arr,color='red')
            ax1[ppindex].text(0.95, 0.95, f" {pp[0].intensity}", transform=ax1[ppindex].transAxes, ha='right', va='top')
            if pp[0].name=="single_trans_pulse":
            
                data=Parse_Avg().Parse_Trains_Single(avg_arr,avg_timeaxis,pp[0].intensity)
                grouped_data.append({"intensity":pp[0].intensity,"data":data})
            else:
                data=Parse_Avg().Parse_Single(avg_arr,avg_timeaxis,pp[0].intensity)
                grouped_data.append({"intensity":pp[0].intensity,"data":data})

        
        plt.savefig(f"{self.filepath}_grouped_{name}_.png",dpi = 300,orientation='landscape')
        plt.close()
        return grouped_data

                
                