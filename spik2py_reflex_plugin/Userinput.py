#this is the userinput class 
from typing import List
import numpy as np

class user_specified_data:
    """Class for user specified data from trial object provided by spike2by library

    Parameters
    ----------
    spike2py_trial_object : Trial Object
        See :class:`spike2py.trial.Trial` parameters for details.

    triggerchannel : List[float]
        Mmax.times if the condition is MMAX or DS8.times 
        This is a list containing time values of the trigger of interest 
    
    range : Dict
        A dictionary containing two fields , user specified starttime (s) and end time (s)
        e.g:
        "userstarttime": 23,
        "userendtime": 50,


    khz_clean: int
        Values representing khz frequency, this will be used to remove khz 

   

    Attributes
    ----------
    event_data : object
        Spike2Py trial object.
    channel : list[float]
        List of trigger times.
    starttime : float
        User-specified start time.
    endtime : float
        User-specified end time.
    khz_rate : float
        Rate used for kHz noise removal.
    khz_fq : int
        Value representing kHz frequency.

    
    """
   
    def __init__(self, spike2py_trial_object,triggerchannel,range,khz_clean):
        self.event_data = spike2py_trial_object
        self.channel=triggerchannel
        self.starttime=range["userstarttime"]
        self.endtime=range["userendtime"]
        self.khz_rate=1 / (khz_clean * 1000) + 0.00005
        self.khz_fq=khz_clean
        self.unclean=[]
    
    
    def extract(self)->List[int]:
        """
        Extracts trigger times within the specified range and removes kHz noise.

        Returns
        -------
        list[int]
            List of trigger times with kHz noise removed.

        """
        
        triggeruncleaned = self.channel[np.where((self.channel >self.starttime) & (self.channel <self.endtime))]
        self.unclean=triggeruncleaned
        return self.remove_khz()
    
    
    def remove_khz(self)->List[int]:
        """
        Removes kHz noise from the trigger times.

        Returns
        -------
        list[int]
            List of trigger times with kHz noise removed.

        """
        
        i = 0
        triggercleaned = []
        while i < len(self.unclean):

            if self.isKhz(i):
                triggercleaned.append(self.unclean[i])
                i += self.khz_fq
                continue
            i+=1


           
        return self.unclean if len(triggercleaned) == 0 else triggercleaned

            
    def isKhz(self,i)->bool:
        try:
            rightdiff = self.unclean[i + 1] - self.unclean[i]
            return True if rightdiff < self.khz_rate else False

        except:
            return False
        
                    
