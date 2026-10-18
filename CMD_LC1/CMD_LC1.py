"""Minimal MIDI Remote Script: one LC-1 encoder controls the last touched
(selected) parameter in Ableton Live."""
import Live
from _Framework.ControlSurface import ControlSurface

# --- Configuration (adjust to your LC-1 preset) ---
MIDI_CHANNEL = 0        # 0-based (0 = channel 1)
ENCODER_CC = 1          # CC number sent by the knob
RELATIVE = False        # False = absolute 0-127 (default), True = relative
RELATIVE_STEP = 1.0 / 127.0  # parameter range fraction per encoder tick
# Relative encoding: 1..63 = increase, 65..127 = decrease (two's complement style)


class CMD_LC1(ControlSurface):
    def __init__(self, c_instance):
        super(CMD_LC1, self).__init__(c_instance)
        self.show_message("CMD LC-1 script loaded")

    def build_midi_map(self, midi_map_handle):
        super(CMD_LC1, self).build_midi_map(midi_map_handle)
        # Forward the CC to this script and stop Live from mapping it itself
        Live.MidiMap.forward_midi_cc(
            self.handle(), midi_map_handle, MIDI_CHANNEL, ENCODER_CC)

    def receive_midi(self, midi_bytes):
        if len(midi_bytes) == 3 and midi_bytes[0] == 0xB0 + MIDI_CHANNEL \
                and midi_bytes[1] == ENCODER_CC:
            self._on_encoder(midi_bytes[2])
            return
        super(CMD_LC1, self).receive_midi(midi_bytes)

    def _on_encoder(self, value):
        param = self.song().view.selected_parameter  # last touched parameter
        if param is None or not param.is_enabled or param.is_quantized:
            return
        span = param.max - param.min
        if RELATIVE:
            delta = value if value < 64 else value - 128
            new = param.value + delta * RELATIVE_STEP * span
        else:
            new = param.min + (value / 127.0) * span
        param.value = max(param.min, min(param.max, new))
