import numpy as np
from spik2py_reflex_plugin.Trains_processing import Train_preprocessing
class Event:
    '''Takes in a number n, returns the square of n'''

    def __init__(self,trigger, triggertimes):       
        self.trigger= trigger
        self.unclassified_trigger = triggertimes       
    def meet_condition(self):
        '''Takes in a number n, returns the square of n'''

        return False

class Difference_Calculator:
    '''Takes in a number n, returns the square of n'''
    def __init__(self,trigger, triggertimes):
        self.alltriggers = triggertimes
        self.trigger= trigger   
        self.index=np.where(triggertimes >= trigger)[0][0]
    def leftdiff(self):
        '''Takes in a number n, returns the square of n'''
        index = self.index
        if index==0:
            return None
        try:
            
            leftdiff = self.alltriggers[index]-self.alltriggers[index - 1] 
            return leftdiff
        except IndexError:
            return None
        
    def rightdiff(self):
        '''Takes in a number n, returns the square of n'''
        index = self.index
        if self.alltriggers[index]== self.alltriggers[-1]:
            return None
        try:
            rightdiff = self.alltriggers[index + 1] -self.alltriggers[index]
            return rightdiff
        except IndexError:
            return None
    def leftdiff2(self):
        '''Takes in a number n, returns the square of n'''
        index = self.index
        if index==0:
            return None
        try:
            
            leftdiff = self.alltriggers[index-1]-self.alltriggers[index - 2] 
            return leftdiff
        except IndexError:
            return None
        
    def rightdiff2(self):
        '''Takes in a number n, returns the square of n'''
        index = self.index
        if self.alltriggers[index]== self.alltriggers[-1]:
            return None
        try:
            rightdiff = self.alltriggers[index + 2] -self.alltriggers[index+1]
            return rightdiff
        except IndexError:
            return None
    def rightdiff5(self):
        '''Takes in a number n, returns the square of n'''
        index = self.index
        if self.alltriggers[index]== self.alltriggers[-1]:
            return None
        try:
            rightdiff = self.alltriggers[index + 4] -self.alltriggers[index]
            return rightdiff
        except IndexError:
            return None
        
    def leftdiff5(self):
        '''Takes in a number n, returns the square of n'''
        index = self.index
        if index==0 or index==1 or index==2 or index==3  :
            return None
        try:
            leftdiff = self.alltriggers[index] -self.alltriggers[index-4]
            return leftdiff
        except IndexError:
            return None
    
    
    

class Single_Pulse(Event):
    name="Single_Pulse"
    def __init__(self, triggertimes, trigger, param):
        super().__init__(triggertimes, trigger)
        self.name="Single_Pulse"
        self.index = None
        self.left_diff=Difference_Calculator(self.unclassified_trigger,self.trigger).leftdiff()
        self.right_diff=Difference_Calculator(self.unclassified_trigger,self.trigger).rightdiff()
        self.paired_pulse_isi=param["paired_pulse_isi"]

    
    def meet_condition(self):
  
        if self.left_diff is None and self.right_diff is None:
            return self.name,True
        
        elif self.left_diff is None:
            if self.right_diff > 1 and self.right_diff > self.paired_pulse_isi:
                return self.name , True
            else:
                return self.name ,False
        
        elif self.right_diff is None:
            if self.left_diff > 1 and self.left_diff > self.paired_pulse_isi:
                return self.name , True
            else:
                return self.name ,False

        else:
            if self.right_diff > 1 and self.left_diff>1 and self.right_diff > self.paired_pulse_isi:
                return self.name , True
            else:
                return self.name ,False


class Paired_Pulse(Event):
    name="Paired_Pulse"
    def __init__(self, triggertimes, trigger, param):
        super().__init__(triggertimes, trigger)
        self.name="Paired_Pulse"
        self.index = None
        self.left_diff=Difference_Calculator(self.unclassified_trigger,self.trigger).leftdiff()
        self.right_diff=Difference_Calculator(self.unclassified_trigger,self.trigger).rightdiff()
        self.right_2_diff= Difference_Calculator(self.unclassified_trigger,self.trigger).rightdiff2()
        self.left_2_diff= Difference_Calculator(self.unclassified_trigger,self.trigger).leftdiff2()
        self.paired_pulse_isi=param["paired_pulse_isi"]

    
    def meet_condition(self):
        #edge case , first index of the list 
        def left_verify():
            if self.left_diff>self.paired_pulse_isi:
                return True

        def right_verify():
            if self.right_diff < self.paired_pulse_isi and self.right_2_diff > self.paired_pulse_isi:
                return True
        conditions = {
        "first_index": {
            "condition": self.left_diff is None,
            "action": lambda:right_verify()
        },
        "last_index": {
            "condition": self.right_diff is None,
            "action": lambda: False
        },
        "second_last_index": {
            "condition": self.right_2_diff is None,
            "action": lambda: (self.right_diff < self.paired_pulse_isi and left_verify())
        },
        "default": {
            "condition": True,
            "action": lambda: (right_verify() and left_verify())
        }
    }

        for condition_name, condition_info in conditions.items():
            if condition_info["condition"]:
                result = condition_info["action"]()
                return self.name, result
            
            
     

class Trains(Event):
    name=""
    def __init__(self, triggertimes, trigger, param):
        super().__init__(triggertimes, trigger)
        self.name="Trains"
        self.index = None
        self.left_diff=Difference_Calculator(self.unclassified_trigger,self.trigger).leftdiff()
        self.right_diff=Difference_Calculator(self.unclassified_trigger,self.trigger).rightdiff()
        self.right_diff_5=Difference_Calculator(self.unclassified_trigger,self.trigger).rightdiff5()
        self.left_diff_5=Difference_Calculator(self.unclassified_trigger,self.trigger).leftdiff5()
       
        self.right_2_diff= Difference_Calculator(self.unclassified_trigger,self.trigger).rightdiff2()
        self.left_2_diff= Difference_Calculator(self.unclassified_trigger,self.trigger).leftdiff2()
        self.per_s_train=param["per_s_train"]
        
    

    def meet_condition(self):  
        def left_verify():
            if self.left_diff_5 / 5 < self.per_s_train:
                return True

        def right_verify():
            if self.right_diff_5 / 5 < self.per_s_train:
                return True
     
    
            
        if self.left_diff is None :
            
            if right_verify():
                self.name="Trains_Start"
                return self.name , True
            else:
                return self.name ,False
        
        elif self.right_diff is None:
            if left_verify():
                self.name="Trains_End"
                return self.name , True
            else:
                return self.name ,False

        else:
            try:
                if right_verify() and self.left_diff> self.per_s_train:
                    self.name="Trains_Start"
                    return self.name , True
                elif left_verify() and self.right_diff> self.per_s_train:
                    self.name="Trains_End"
                    return self.name , True
                else:
                    return self.name,False
            except:
                return self.name , False
            
            
        



        

class Classifier_info:
    """Class for containing infomration needed for the classifier class.

    Parameters
    ----------
    trial_object : Trial Object
        See :class:`spike2py.trial.Trial` parameters for details.

    triggerchannel : List[float]
        Mmax.times if the condition is MMAX or DS8.times 
        This is a list containing time values of the trigger of interest 
    
    paried_pulse_isi : float 
        Inter-stimulus interval for paired pulse in s + error of 0.01s, or any error specified
        example:interval in s + error in s
        example:50 / 1000 + 0.01
    per_s_train : int
        Inter-stimulus interval for trains pulse
        This will used to determine if a pulse is classified as trains or not
        If the difference between two pulse is smaller than per_s_train, then the pulse is 
        classified as a trains pulse
        example: 1s/ number of individual trains pulse in a second 
        example: 1/25

    Attributes
    ----------
    Same as parameters as described above

    """
    def __init__(self, trial_object,user_data,triggerchannel,paried_pulse_isi,per_s_train):
        self.trial_object = trial_object
        self.user_data=user_data
        self.triggerchannel=triggerchannel
        self.paired_pulse_isi=paried_pulse_isi
        self.per_s_train=per_s_train
    def get_variables(self):
        return self
        

class Pulse_Classifier:
    """Class for pulse classification by analysing the time difference between pulses.
    If you wanted to classify data with different methods, e.g keyboard, 
    you can create a new class e.g with its own classify function and logic
    as long as the output is a list of tuples with name of the pulse and the trigger time
    KeyStroke_Classifier class 

    Parameters
    ----------
    setting : Classifier_info
        See Signal_Classifier.Classifier_info for more info.

    Attributes
    ----------
    Similar to parameters

    """

    def __init__(self, setting):
        self.unclassified_trigger = setting.user_data
        self.classified_trigger:list=[]
        self.triggerchanel=setting.triggerchannel
        self.paired_pulse_isi=setting.paired_pulse_isi
        self.per_s_train=setting.per_s_train
        self.data=setting.trial_object
        


        

    def classify(self):
        """Main Function to classify pulses withint the Pulse_Classifier Class

        Parameters
        ----------
        

       
        
        """
        param={
            "paired_pulse_isi":self.paired_pulse_isi,
            "per_s_train":self.per_s_train
        }
        skip_next = False
        for index,trigger in enumerate(self.unclassified_trigger):
            if skip_next:
                skip_next = False
                continue # skip
            for subclass in Event.__subclasses__():
                name,boolval=subclass(self.unclassified_trigger,trigger,param).meet_condition()
                if boolval is True:
                    if subclass.__name__=="Paired_Pulse":
                        self.classified_trigger.append((name,trigger,self.unclassified_trigger[index+1]))
                        skip_next = True
                        break

                    else:
                            
                        self.classified_trigger.append((name,trigger))
                        break
                else:
                    pass
        classified_pulses=Train_preprocessing(self.data,self.classified_trigger,self.triggerchanel).extract_trains_period()
        return classified_pulses
