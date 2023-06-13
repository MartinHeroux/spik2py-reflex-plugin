from typing import Dict, List , Union

# Define the type for a single pulse result
single_pulse_result = List

# Define the type for a double pulse result
double_pulse_result = List

# Define the type for a trains pulse result
trains_pulse_result = List

# Define the type for the overall object
pulse_result_type = Dict[str, List[Union[single_pulse_result, double_pulse_result, trains_pulse_result]]]
