from typing import Tuple, Optional, Union, List
from dataclasses import dataclass


@dataclass
class awg_channel:
    name: str
    awg_name: str
    channel_number: int
    amplitude: Optional[float] = None
    delay: float = 0 # ns
    attenuation: float = 1.0
    compensation_limits: Tuple[float, float] = (0,0)
    bias_T_RC_time: Optional[float] = None

@dataclass
class marker_channel:
    name: str
    module_name: str # could be AWG or digitizer
    channel_number: Union[int,Tuple[int,int]]
    '''
    Keysight: 0 = trigger out channel, 1...4 = analogue channel
    Tektronix: tuple = (channel,marker number), int = analogue channel
    '''
    setup_ns: float
    hold_ns: float
    amplitude: float = 1000
    invert: bool = False
    delay: float = 0 # ns

@dataclass
class digitizer_channel:
    name: str
    module_name: str
    channel_number: int
    input_range: Optional[float] = None

@dataclass
class digitizer_channel_iq:
    name: str
    module_name: str
    channel_numbers: List[int]
    phase : Optional[float] = None
    frequency : Optional[float] = None
    input_range: Optional[float] = None

