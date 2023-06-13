from spik2py_reflex_plugin import compute_outcome_measures
from spik2py_reflex_plugin import utlis
from dataclasses import dataclass


import numpy as np

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

