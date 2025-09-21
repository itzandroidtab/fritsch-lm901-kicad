# Kicad to Fritsch LM901 converter
This python script is for the LM901 semi automatic pick and place machine [advanced version of this machine](https://www.fritsch-smt.de/en/manual-pick-place/lm901). To create a new placement file you need to manually go to each position with the tool head to register it. KiCad can automaticly generate this data. This python script converts a KiCad placement file to a file accepted by the LM901 DOS appliation (yes it runs on DOS. 86Box works as well with serial port emulation).

This was made during my rev efforts of the DOS program as a intermediate solution to improve my workflow.

## Usage
To run the script you need the following:
* Kicad position file
* Reference for board location detection (1 or 3 are supported in the LM901 DOS program)

```bash
python kicad_lm901_converter.py -i <input_file.pos> -o <output_file.smd> -ref <"X,Y"> [-ref1 <"X,Y">] [-ref2 <"X,Y">] [-r <rotation>] 
```

- `-i <input_file.pos>`: Input KiCad POS file (required)
- `-o <output_file.smd>`: Output SMD file (required)
- `-ref <X,Y>`: Reference 0 coordinate (required, e.g. "77.75,341.75")
- `-ref1 <X,Y>`: Reference 1 coordinate (optional)
- `-ref2 <X,Y>`: Reference 2 coordinate (optional, required if ref1 is present. Ref 1 is not used if Ref 2 is not present)
- `-r <rotation>`: Rotation angle in degrees (optional, e.g. 90, 180, 270)

Example:
```bash
python kicad_lm901_converter.py -i pinball_playfield-top.pos -o pinball_top.smd -ref "77.75,341.75" -ref1 "129.5,345.25" -ref2 "181.25,53" -r 90 
```
