from spik2py_reflex_plugin import compute_outcome_measures
from spik2py_reflex_plugin import utlis
from dataclasses import dataclass
from spik2py_reflex_plugin.Graph import Base_Graph
from spik2py_reflex_plugin.Grouped_Graph import Grouped_Graph
import numpy as np
import pickle

from tqdm import tqdm
@dataclass
class SinglePulse:
    name:str
    waveform: list
    startindex:int
    endindex:int
    relativeonset:int
    onset:float
    peak_to_peak: float
    area: float
    rms:float
    intensity:float
    triggerindex:int

@dataclass
class PairedPulse:
    name:str
    pulse1:SinglePulse
    pulse2:SinglePulse
    peak_to_peak_ratio:float
    area_ratio:float
    intensity:any
    entirewaveform:any

@dataclass
class SingleTransPulse:
    name:str
    waveform: list
    startindex:int
    endindex:int
    relativeonset:int
    onset:float
    peak_to_peak: float
    area: float
    rms:float
    intensity:float
    triggerindex:int
    

class Parse:
    """Class for pulse parsing

    Parameters
    ----------
    self.single_pre: int
        time to include before the trigger in ms 

    self.single_post
        time to include after the trigger in ms 
    self.double_pre
        time to include after the fist trigger in ms 
    self.double_post
        time to include after the second trigger in ms

    self.trains_pre
        time to include after the trigger in ms 
    self.trains_post
        time to include after the trigger in ms 

    

    Attributes
    ----------

    Output
    ----------
    A list of dataclass objects 
    
    """
    def __init__(self,settings,trial,mode):
       
        self.single_pre=settings.presingle
        self.single_post=settings.postsingle
        self.double_pre=settings.predouble
        self.double_post= settings.postdouble
        self.trains_pre= settings.pretrains
        self.trains_post=settings.posttrains
        self.trial=trial
        self.mode=mode
        
    
    def parsesingle(self,trigger):
        
        
        
        

        target = trigger[1]
        
        left = target - self.single_pre/ 1000
        right = self.single_post / 1000 + target
        times = self.trial.Fdi.times

        start_index = np.searchsorted(times, left)
        trigger_index = np.searchsorted(times, target)
        end_index = np.searchsorted(times, right)

        intensity_index = np.searchsorted(self.trial.Stim.times, target)

        # find artifact start time
        ARTIFACT_TIME_MS=0.005
        skip_artifact_start_time = self.trial.Fdi.times[trigger_index] + ARTIFACT_TIME_MS
        artifact_start_index = np.searchsorted(times[trigger_index:end_index], skip_artifact_start_time) + trigger_index
        artifact_end_index = np.searchsorted(times[trigger_index:end_index], skip_artifact_start_time + 0.09) + trigger_index

        # compute baseline SD and average
        tkeo_array = utlis.TEOCONVERT(self.trial.Fdi.values)
        baseline_values = tkeo_array[artifact_start_index:artifact_end_index]
        baseline_sd = np.std(np.abs(baseline_values))
        baseline_avg = np.mean(np.abs(baseline_values))
        
        peak_to_peak, area=compute_outcome_measures.compute_peak2peak_area(self.trial.Fdi.values[artifact_start_index:end_index])

        # compute peak-to-peak and area
       
        # find onset time
        if self.mode =="single":
            onset_index = compute_outcome_measures.findonset(tkeo_array[trigger_index:end_index], baseline_sd, baseline_avg, artifact_start_index - trigger_index)
        elif self.mode=="double":
            baseline_values = self.trial.Fdi.values[artifact_start_index:artifact_end_index]
            baseline_sd = np.std(np.abs(baseline_values))
            baseline_avg = np.mean(np.abs(baseline_values))
            onset_index = compute_outcome_measures.findonset(self.trial.Fdi.values[trigger_index:end_index], baseline_sd, baseline_avg, artifact_start_index - trigger_index)
        else:

            onset_index = compute_outcome_measures.findonset(tkeo_array[trigger_index:end_index], baseline_sd, baseline_avg, artifact_start_index - trigger_index)

        if onset_index is not None:
            onset_time = self.trial.Fdi.times[onset_index + trigger_index]
            relative_time = onset_time - self.trial.Fdi.times[trigger_index]
        else:
            onset_time = None
            relative_time = None

        # create SinglePulse object
        data = SinglePulse(
            "singlepulse",
            self.trial.Fdi.values[start_index:end_index],
            start_index,
            end_index,
            relative_time,
            onset_time,
            peak_to_peak,
            area,
            0,
            self.trial.Stim.values[intensity_index],
            trigger_index
        )

        return data


    def parsetrans(self,trigger):
        import numpy as np
        
        
        
        pulse=self.parsesingle(trigger)
      
        
      
       
       
        data = SingleTransPulse(
        "single_trans_pulse",
        pulse.waveform,
        pulse.startindex,
        pulse.endindex,
        pulse.relativeonset,
        pulse.onset,
        pulse.peak_to_peak,
        pulse.area,
        0,
        pulse.intensity,
        pulse.triggerindex
    )

        
        return data
    
    def parsedouble(self,trigger):
        
       
        trigger1=("double",trigger[1])
        trigger2=("double",trigger[2])
        
        pulse1=self.parsesingle(trigger1)
        pulse2=self.parsesingle(trigger2)
        
        p2pratio=pulse1.peak_to_peak/ pulse2.peak_to_peak
        arearatio= pulse1.area/pulse2.area
        intensity=pulse1.intensity
        entirewaveform=self.trial.Fdi.values[pulse1.startindex:pulse2.endindex]
        
        
        data=PairedPulse(

            "pairedpulse",
            pulse1,
            pulse2,
            p2pratio,
            arearatio,
            intensity,
            entirewaveform



        )
        
        return data
        

class Parse_Avg:
    def __init__(self):
        self=self

    def Parse_Single(self,arr,arrtimes,intensity):
        skip_artifact_start_time = 0.005
        artifact_start_index = np.searchsorted(arrtimes, skip_artifact_start_time)
        artifact_end_index = np.searchsorted(arrtimes, skip_artifact_start_time + 0.09) 

        # compute baseline SD and average
        tkeo_array = utlis.TEOCONVERT(arr)
        baseline_values = tkeo_array[artifact_start_index:artifact_end_index]
        baseline_sd = np.std(np.abs(baseline_values))
        baseline_avg = np.mean(np.abs(baseline_values))
        peak_to_peak, area=compute_outcome_measures.compute_peak2peak_area(arr)
        onset_index = compute_outcome_measures.findonset(tkeo_array, baseline_sd, baseline_avg, artifact_start_index )
        relativeonset=arrtimes[onset_index]
        data = SinglePulse(
            "grouped",
            arr,
            0,
            0,
            relativeonset,
            onset_index,
            peak_to_peak,
            area,
            0,
            intensity,
            0
        )

        return data

    def Parse_Trains_Single(self,arr,arrtimes,intensity):
        pulse=self.Parse_Single(arr,arrtimes,intensity)
  
        data = SingleTransPulse(
        "single_trans_pulse",
        pulse.waveform,
        pulse.startindex,
        pulse.endindex,
        pulse.relativeonset,
        pulse.onset,
        pulse.peak_to_peak,
        pulse.area,
        0,
        pulse.intensity,
        pulse.triggerindex
    )

        
        return data
        
    def Parse_Double(self,arr1,arr2,arrtimes1,arrtimes2,intensity,entirewaveform):
        pulse1=self.Parse_Single(arr1,arrtimes1,intensity)
        pulse2=self.Parse_Single(arr2,arrtimes2,intensity)
        p2pratio=pulse1.peak_to_peak/ pulse2.peak_to_peak
        arearatio= pulse1.area/pulse2.area
        intensity=pulse1.intensity
        entirewaveform=entirewaveform

        
        
        data=PairedPulse(

            "pairedpulse",
            pulse1,
            pulse2,
            p2pratio,
            arearatio,
            intensity,
            entirewaveform



        )
        return data


class Parse_All_Pulses:
    """Class for organisning the parsed results.

    Parameters
    ----------
    data : Spike2py trail object 
        See Trial.trial for more info.
    post_trains_entire_classified_list: List[tuples()]
        this consists of the output from the classifer class , for single pulses, it 
        should containa named tuple like this (("single_pulse),(34)), where the first item 
        is the name of the classified pusle and the second the trigger time of that pulse as 
        appeared in the mat file and orginal channel. 
        For double pulse, it will be something like (("double"),(firsttriigger),(secondtrigger))
    parsesettings:
        
    graphsettings:

    the values for parsesettings and graphsettings are ambiguous and could be refactored into
    something more readable 

    Attributes
    ----------
    
    """

    def __init__(self,data,post_trains_entire_classified_list,parsesettings,graphsettings):
        self.data=data
        self.post_trains_entire_classified_list=post_trains_entire_classified_list
        self.parsesettings=parsesettings
        self.graphsettings=graphsettings
        self.single=None
        self.double=None
        self.trains=None
        self.master=None
        self.group_single=None
        self.group_double=None
        self.group_trains=None
        

        
    
    def parse_all(self):
        
        lookup_table = {
        "Single_Pulse": Parse(self.parsesettings,self.data,"single").parsesingle,
        "Single_Trains_pulse":Parse(self.parsesettings,self.data,"trains").parsetrans,
        "Paired_Pulse": Parse(self.parsesettings,self.data,"double").parsedouble
        }
        single_pulse_result=[]
        double_pulse_result=[]
        trains_pulse_result=[]
    

        for trigger in tqdm(self.post_trains_entire_classified_list):
            try:
                result=lookup_table[trigger[0]](trigger)
                if result.name=="single_trans_pulse":
                    trains_pulse_result.append(result)
                elif result.name=="singlepulse":
                    single_pulse_result.append(result)
                elif result.name=="pairedpulse":
                    double_pulse_result.append(result)
            except Exception as error:
                print(str(error))
                break

        
        
        self.single=single_pulse_result
        self.double=double_pulse_result
        self.trains=trains_pulse_result
        self.master=single_pulse_result+double_pulse_result+trains_pulse_result
      
        
        
        return self.group_pulses()

    def group_pulses(self):
        self.single=utlis.Group_Individual_Pulses(self.single)
        self.double=utlis.Group_Individual_Pulses(self.double)
        self.trains=utlis.Group_Individual_Pulses(self.trains)
        
        return self

    
    def plot_individual(self):
        
       
        Base_Graph(self.graphsettings["settings"],self.master,self.graphsettings["range"],self.graphsettings["filepath"]).generate_individual_graph(0.25,0.25)
        return self.single+self.double+self.trains
    
    def plot_group(self):
        
        #row= length of grouped single
        group_single=[]
        group_double=[]
        group_trains=[]
        
        if len( self.single)!=0:
            group_single=Grouped_Graph(self.graphsettings["filepath"],self.single,self.parsesettings).generate_group_graph("single")
        
        
        if len(self.double)!=0:
            group_double=Grouped_Graph(self.graphsettings["filepath"],self.double,self.parsesettings).generate_paired_graph()

        
        if len(self.trains)!=0:
            group_trains=Grouped_Graph(self.graphsettings["filepath"],self.trains,self.parsesettings).generate_group_graph("trains")
        
        #groupedpickled=grouped_masterresult

        return group_single+group_double+group_trains

    def pickle(self):
        filepath=self.graphsettings["filepath"]
        self.plot_group()
        with open(f"{filepath}_data.pickle", "wb") as file:
            pickle.dump({"individual":self.single+self.double+self.trains,"grouped":self.group_single+self.group_double+self.group_trains}, file)
        return