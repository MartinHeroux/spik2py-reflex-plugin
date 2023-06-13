import pickle
from tqdm import tqdm
import pickle
from spik2py_reflex_plugin.Userinput import user_specified_data
from spik2py_reflex_plugin.Signal_Classifier import Pulse_Classifier,Classifier_info
from spik2py_reflex_plugin.Parse_Signals import Parse_All_Pulses
from spik2py_reflex_plugin.utlis import ParseSettings

def extract_evoked_responses(data,triggerchannel,range,khz_clean,filepath):
    """documentation"""
    PAIRED_PULSE_ISI=50 / 1000 + 0.01
    PER_S_TRAIN=1/25
    user_data= user_specified_data(data,triggerchannel,range,khz_clean).extract()
    
    settings=Classifier_info(data,user_data,triggerchannel, PAIRED_PULSE_ISI,PER_S_TRAIN)
    classified_list= Pulse_Classifier(settings).classify()
    #if you want to classify pulse with keyboard channel, jsut call the keyboard classifier class 
    #instead 
    #e.g classified list = Keyboard_Classifier(settings).classify()
    
   
    parse_setting_object = {
    "presingle_ms": 200,
    "postsingle_ms": 100,
    "predouble_ms": 15,
    "postdouble_ms": 40,
    "pretrain_ms": 5,
    "posttrain_ms": 25
}
    graphsettings={
        "settings":settings,
        "range":range,
        "filepath":filepath
    }
    
    parsesettings= ParseSettings(**parse_setting_object)
    masterresults=Parse_All_Pulses(data,classified_list,parsesettings,graphsettings).parse_all()
    individual_pickled_results=masterresults.plot_individual()
    group_pickled_results=masterresults.plot_group()
    with open(f"{filepath}_data.pickle", "wb") as file:
        pickle.dump({"individual":individual_pickled_results,"grouped":group_pickled_results}, file)
