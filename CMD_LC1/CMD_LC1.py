"""Minimal MIDI Remote Script: one LC-1 encoder controls the last touched
(selected) parameter in Ableton Live."""
from _Framework.ControlSurface import ControlSurface
from _Framework.ButtonElement import ButtonElement
from _Framework.InputControlElement import MIDI_CC_TYPE

# --- Configuration (adjust to your LC-1 preset) ---
MIDI_CHANNEL = 4             # 0-based (4 = channel 5)
ENCODER_CC = 16              # CC number sent by the encoder
ENCODER_CW_VALUE = 65        # CC value sent when turning clockwise
ENCODER_CCW_VALUE = 63       # CC value sent when turning counterclockwise
ENCODER_STEP = 1.0 / 127.0   # parameter range fraction per encoder tick


class CMD_LC1(ControlSurface):
    def __init__(self, c_instance):
        super(CMD_LC1, self).__init__(c_instance)
        with self._control_surface_injector:
            self._encoder = ButtonElement(
                is_momentary=True,
                msg_type=MIDI_CC_TYPE,
                channel=MIDI_CHANNEL,
                identifier=ENCODER_CC,
                name="Encoder")
        self._encoder.add_value_listener(self._on_encoder_value)
        self.show_message("CMD LC-1 script loaded")

    def build_midi_map(self, midi_map_handle):
        super(CMD_LC1, self).build_midi_map(midi_map_handle)
        self.log_message(
            "CMD_LC1: MIDI map built for channel %d, CC %d"
            % (MIDI_CHANNEL + 1, ENCODER_CC))

    def receive_midi(self, midi_bytes):
        if len(midi_bytes) == 3 and midi_bytes[0] & 0xF0 == 0xB0:
            self.log_message(
                "CMD_LC1: raw CC status 0x%02X, CC %d, value %d"
                % (midi_bytes[0], midi_bytes[1], midi_bytes[2]))
        super(CMD_LC1, self).receive_midi(midi_bytes)

    def _on_encoder_value(self, value):
        if value == ENCODER_CW_VALUE:
            self._on_encoder(1, value)
        elif value == ENCODER_CCW_VALUE:
            self._on_encoder(-1, value)
        else:
            self.log_message("CMD_LC1: ignored unrecognized CC value %d" % value)

    def _on_encoder(self, direction, value):
        message = "CMD_LC1: encoder callback channel %d CC %d value %d" \
            % (MIDI_CHANNEL + 1, ENCODER_CC, value)
        self.log_message(message)
        self.show_message(message)
        param = self.song().view.selected_parameter  # last touched parameter
        if param is None:
            self.show_message("CMD LC-1: MIDI received, no selected parameter")
            return
        if not param.is_enabled or param.is_quantized:
            self.show_message("CMD LC-1: selected parameter cannot be changed")
            return
        span = param.max - param.min
        new = param.value + direction * ENCODER_STEP * span
        param.value = max(param.min, min(param.max, new))
        self.show_message("CMD LC-1: selected parameter updated")
