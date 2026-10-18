# lc1_script
Custom script for using Behringer CMD LC-1 with Ableton

## Instalace
Zkopíruj složku `CMD_LC1` do `User Library/Remote Scripts/` (Win: `Documents\Ableton\User Library\Remote Scripts`, Mac: `~/Music/Ableton/User Library/Remote Scripts`).
V Live: Preferences > Link/Tempo/MIDI > Control Surface = `CMD_LC1`, Input/Output = LC-1.

Knob (CC 1, kanál 1 – nastavíš v `CMD_LC1/CMD_LC1.py`) ovládá poslední použitý parametr.
Pokud knob posílá relativní hodnoty, nastav `RELATIVE = True`.
