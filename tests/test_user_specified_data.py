import pytest
from pytest import approx
import numpy as np
from spike2py.trial import TrialInfo, Trial

from spik2py_reflex_plugin import Userinput


def test_extract():
    data =Trial(TrialInfo(file=f"C:/Users/wanho/Downloads/matfiles/10_DATA000_C_M.mat",channels=["MMax","FDI","Ds8","stim"]))
    #point this to the mat folder you shared with me on dropbox 
    
    range={
    "userstarttime": 0,
    "userendtime": 20,
    }
    
    #check whether this fucntion returns a list of integers 
    #check whether it can be used to parse the whole trial and whether it is fine 
    #parsing only part of it.
    result = Userinput.user_specified_data(data,data.Ds8.times,range,10).extract()
    
    assert isinstance(result, np.ndarray), "Variable is not a numpy.ndarray"