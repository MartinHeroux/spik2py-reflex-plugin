import pickle
from tqdm import tqdm
from spik2py_reflex_plugin.Userinput import user_specified_data
from spik2py_reflex_plugin.Signal_Classifier import Pulse_Classifier
from spik2py_reflex_plugin.Parse_Signals import Parse
from spik2py_reflex_plugin.Graph import Base_Graph, Grouped_Graph
from spik2py_reflex_plugin import utlis
from spik2py_reflex_plugin.utlis import ParseSettings

def extract_evoked_responses(data,triggerchannel,range,khz_clean,filepath):
    """documentation"""
   
    user_data= user_specified_data(data,triggerchannel,range,khz_clean).extract().remove_khz()
    
    post_trains_entire_classified_list= Pulse_Classifier(data,triggerchannel,user_data,50 / 1000 + 0.01,1/25).classify()

    parsesettings= ParseSettings(200,100,15,40,5,25).get()

    lookup_table = {
        "Single_Pulse": Parse(parsesettings,data,"single").parsesingle,
        "Single_Trains_pulse":Parse(parsesettings,data,"trains").parsetrans,
        "Paired_Pulse": Parse(parsesettings,data,"double").parsedouble
    }
    single_pulse_result=[]
    double_pulse_result=[]
    trains_pulse_result=[]
    

    for trigger in tqdm(post_trains_entire_classified_list):
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

    
    masterresult=single_pulse_result+double_pulse_result+trains_pulse_result
    #Generate overview graph
    grouped_masterresult={}
    
    
    Base_Graph(data,masterresult,user_data,triggerchannel,range,filepath).generate_individual_graph(0.05)
    
    groupedsingle=utlis.Group_Individual_Pulses(single_pulse_result)
    #row= length of grouped single
    if len(groupedsingle)!=0:
        grouped_masterresult["single"]=Grouped_Graph(filepath,groupedsingle,parsesettings).generate_group_graph("single")
    
    groupedpaired=utlis.Group_Individual_Pulses(double_pulse_result)
    if len(groupedpaired)!=0:
        grouped_masterresult["paired"]=Grouped_Graph(filepath,groupedpaired,parsesettings).generate_paired_graph()

    groupedtraains=utlis.Group_Individual_Pulses(trains_pulse_result)
    if len(groupedtraains)!=0:
        grouped_masterresult["trains"]=Grouped_Graph(filepath,groupedtraains,parsesettings).generate_group_graph("trains")
    individualpickled=groupedsingle+groupedpaired+groupedtraains
    groupedpickled=grouped_masterresult
    

    with open(f"{filepath}_data.pickle", "wb") as file:
        pickle.dump({"individual":individualpickled,"grouped":groupedpickled}, file)
    