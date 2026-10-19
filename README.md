# lc1_script
Custom script for using Behringer CMD LC-1 with Ableton

## Instalace
Zkopíruj složku `CMD_LC1` do `User Library/Remote Scripts/` (Win: `Documents\Ableton\User Library\Remote Scripts`, Mac: `~/Music/Ableton/User Library/Remote Scripts`).
V Live: Preferences > Link/Tempo/MIDI > Control Surface = `CMD_LC1`, Input/Output = LC-1.

Enkodér na kanálu 5 ovládá poslední použitý parametr. Posílá CC 16; hodnota
65 znamená otáčení doprava a 63 doleva. Nastavení najdeš v
`CMD_LC1/CMD_LC1.py`. Každý krok změní parametr o `1/127` jeho rozsahu.
