# Changelog
All notable changes to Pulselib will be documented in this file.

## \[1.3.0] - not yet released
### Added
- IQ correction of phase, amplitude and offset:
  add_channel_offset, set_qubit_correction_phase, set_qubit_correction_gain
- New interface from hardware class to pulselib: set_channel_attenuations and add_virtual_matrix
- Virtual matrix on top of virtual gates
- Added hw schedule for UHFLI with Tektronix

### Removed
- pulse.add_channel_compenstation_limit. Correct method is add_channel_compensation_limit

### Fixed
- loops with t_measurement in HVI variable.
- release_awg_memory() for Keysight

## \[1.2.0] - 2021-11-11
First labeled release. Start of dev branch and change logging.