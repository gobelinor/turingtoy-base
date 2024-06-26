from typing import (
    Dict,
    List,
    Optional,
    Tuple,
)

import poetry_version

__version__ = poetry_version.extract(source_file=__file__)


def run_turing_machine(
    machine: Dict,
    input_: str,
    steps: Optional[int] = None,
) -> Tuple[str, List, bool]:
    
    accepted = False
    
    state = machine["start state"]
    blank = machine["blank"]
    table = machine["table"]
    input_ = blank + input_
    i = 1 
    
    execution_history = []
    
    while state not in machine["final states"]:
        
        #reading
        
        if i < 0 or i >= len(input_): 
            reading = blank
        else:
            reading = input_[i]
        
        #making moves

        #for history execution
        execution = {"state": state, "reading": reading, "position": i, "memory": input_}

        #action to take
        action = table[state][reading]
        
        #just moving
        if action == "L":
            i -= 1
        elif action == "R":
            i += 1

        #writing
        if isinstance(action, dict) and "write" in action.keys():
            if i<0:
                input_ = action["write"] + input_
            else:
                input_ = input_[:i] + action["write"] + input_[i+1:]
        
        #moving and changing state
        if isinstance(action, dict) and "R" in action.keys():
            i+=1
            state = action["R"]
        elif isinstance(action, dict) and "L" in action.keys():
            i-=1
            state = action["L"]  
        
        #logging history execution
        execution["transition"] = state
        execution_history.append(execution)
    
    accepted = True
    input_ = input_.strip(blank)
    return input_, execution_history, accepted

