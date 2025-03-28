# P5R Bad Apple EVT Generator
Tool for creating a bad apple EVT for P5R. Could reasonably be expanded to do other videos as well.

## To install:
```bash
cd <PATH_TO_RELOADED_MODS_FOLDER>
git clone https://github.com/bobbythecatfish/p5r-bad-apple.git
```

## To create the EVT:
1) Download the bad apple video and move it to the folder `<PATH_TO_RELOADED_MODS_FOLDER>/p5r-bad-apple/CreationTool`.
2) Name the video `badapple.mp4`
3) Run the following command
```bash
cd p5r-bad-apple/CreationTool
pip install -r requirements.txt
python badapple.py
```

## To view in game
I'm working on a way to get this to play naturally, but it can currently be called with [Mod Menu](https://github.com/ShrineFox/Persona-5-Mod-Menu). Go to mod menu, call, event, and enter in 100 000.