import matplotlib.pyplot as plt
import numpy as np



class Base_Graph:
    def __init__(self,settings,parsedresults,range,filepath):
        
        self.trial=settings.trial_object
        self.results= parsedresults
        self.triggercleaned=settings.user_data
        self.triggeruncleaned=settings.triggerchannel
        self.userstarttime= range["userstarttime"]
        self.userendtime= range["userendtime"]
        self.filepath=filepath


        
    def generate_individual_graph(self,pretriggertime_ms,post_ms):
    
        fig, (ax1, ax2,ax5,ax4) = plt.subplots(4, 1, sharex=True,figsize=(10, 6))
        ax1.eventplot(self.triggercleaned, orientation='horizontal', colors='g')
        ax2.eventplot(self.triggeruncleaned, orientation='horizontal', colors='r')
        
        
        ax4.plot(self.trial.Fdi.times,self.trial.Fdi.values)
        
        ax5.plot(self.trial.Stim.times,self.trial.Stim.values)
        #plot the grey intervals and the trigger times
    
        plt.xlim(self.userstarttime, self.userendtime)
        
        plt.ylim(-1,1)
        
        masteronset=[]
        for i,x in enumerate(self.results):
            if x.name=="pairedpulse":
                ax4.axvspan(self.trial.Fdi.times[x.pulse1.startindex], self.trial.Fdi.times[x.pulse2.endindex], alpha=0.2, color='gray')
                ax4.axvspan(self.trial.Fdi.times[x.pulse1.startindex], self.trial.Fdi.times[x.pulse2.endindex], alpha=0.2, color='gray')
                masteronset.append(self.trial.Fdi.times[x.pulse1.triggerindex])
                masteronset.append(self.trial.Fdi.times[x.pulse2.triggerindex])
            else:
                ax4.axvspan(self.trial.Fdi.times[x.startindex], self.trial.Fdi.times[x.endindex], alpha=0.2, color='gray')
                masteronset.append(self.trial.Fdi.times[x.triggerindex])
        ax4.vlines(x=list(filter(lambda x: x is not None, masteronset)), ymin=ax4.get_ylim()[0], ymax=ax4.get_ylim()[1], colors='red', ls=':', lw=1, label='vline_single - full height')
                
        
        plt.savefig(self.filepath,dpi = 300,orientation='landscape')
        
       
        gg=fig.text(0.5, 0.95, f"hi", ha='center', va='top')
        gg.remove()

        for i , x in enumerate(self.results):
            if  x.name=="singlepulse":
                ymax= np.max(np.array(self.trial.Fdi.values[x.triggerindex:x.endindex]))
                ymin= np.min(np.array(self.trial.Fdi.values[x.triggerindex:x.endindex]))
                y_range = ymax - ymin
               
                plt.xlim([self.trial.Fdi.times[x.triggerindex]-pretriggertime_ms,  self.trial.Fdi.times[x.endindex]+post_ms])
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
                plt.xlim([self.trial.Fdi.times[x.pulse1.triggerindex]-pretriggertime_ms,  self.trial.Fdi.times[x.pulse2.endindex]+post_ms])
                
                plt.ylim([ymin - 0.1*y_range,ymax +0.1*y_range])
                text1 = fig.text(0.5, 0.95, f"", ha='center', va='top')
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
      
                