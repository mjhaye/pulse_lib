
import logging
from dataclasses import dataclass

from qcodes.instrument.base import Instrument
from typing import List

class MemoryManager:
    def __init__(self):
        self._free_slots = [i for i in range(50)]
        self._used_slots = {}

    def allocate(self, size):
        slot = self._free_slots.pop(0)
        self._used_slots[slot] = size
        logging.info(f'allocated {slot}: {size}')
        return slot

    def free(self, slot):
        size = self._used_slots.pop(slot)
        self._free_slots.append(slot)
        logging.info(f'freed {slot}: {size}')

@dataclass
class WaveformReference:
    wave_number: int
    size: int
    memory_manager: MemoryManager
    waveform: List

    def release(self):
        self.memory_manager.free(self.wave_number)
        self.waveform = None


# mock for M3202A / SD_AWG_Async
class MockM3202A(Instrument):

    def __init__(self, name, chassis, slot):
        super().__init__(name)
        self._slot_number = slot
        self._chassis_numnber = chassis
        self.memory_manager = MemoryManager()
        self.channel_data = {}
        self.channel_prescaler = {}
        self.amplitudes = {}
        for i in range(4):
            self.channel_data[i+1] = []
            self.channel_prescaler[i+1] = []

        self.chassis = chassis
        self.slot = slot

    def slot_number(self):
        return self._slot_number

    def chassis_number(self):
        return self._chassis_numnber

    def upload_waveform(self, wave) -> WaveformReference:
        size = len(wave)
        slot = self.memory_manager.allocate(size)
        logging.info(f'{self.name}.upload_waveform({slot}, {size})')
        return WaveformReference(slot, size, self.memory_manager, wave)

    def set_channel_amplitude(self, amplitude, channel):
        logging.info(f'{self.name}.set_channel_amplitude({amplitude}, {channel})')
        self.amplitudes[channel] = amplitude

    def set_channel_offset(self, offset, channel):
        logging.info(f'{self.name}.set_channel_offset({offset}, {channel})')

    def awg_flush(self, channel):
        logging.info(f'{self.name}.awg_flush({channel})')
        self.channel_data[channel] = []

    def awg_stop(self, channel):
        logging.info(f'{self.name}.awg_stop({channel})')

    def awg_queue_waveform(self, channel, waveform_ref, trigger_mode, start_delay, cycles, prescaler):
        logging.info(f'{self.name}.awg_queue_waveform({channel}, {waveform_ref.wave_number}, {trigger_mode}, {start_delay}, {cycles}, {prescaler})')
        self.channel_data[channel].append(waveform_ref.waveform * self.amplitudes[channel])
        self.channel_prescaler[channel].append(prescaler)

    def awg_is_running(self, channel):
        return False

    def get_data(self, channel):
        return self.channel_data[channel]

    def get_data_prescaler(self, channel):
        return self.channel_data[channel], self.channel_prescaler[channel]

    @staticmethod
    def convert_sample_rate_to_prescaler(sample_rate):
        """
        Args:
            sample_rate (float) : sample rate
        Returns:
            prescaler (int) : prescaler set to the awg.
        """
        # 0 = 1000e6, 1 = 200e6, 2 = 100e6, 3=66.7e6
        prescaler = int(200e6/sample_rate)

        return prescaler


    @staticmethod
    def convert_prescaler_to_sample_rate(prescaler):
        """
        Args:
            prescaler (int) : prescaler set to the awg.

        Returns:
            sample_rate (float) : effective sample rate the AWG will be running
        """
        # 0 = 1000e6, 1 = 200e6, 2 = 100e6, 3=66.7e6
        if prescaler == 0:
            return 1e9
        else:
            return 200e6/prescaler
