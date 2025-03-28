import cv2
import numpy as np
import base_object
import json
import subprocess

file = base_object.file
current_values = {}
skipped = 0

FRAMES = 6545
WIDTH, HEIGHT = (24, 18)

# Takes longer to load but is higher resolution
#WIDTH, HEIGHT = (32, 24)
OUT_PATH = "../P5REssentials/CPK/APPLE.CPK/EVENT/E100/E100"

def initial_setup():
    print(WIDTH * HEIGHT)
    file["Duration"] = FRAMES + 50
    for i in range(WIDTH * HEIGHT):
        x = i % WIDTH
        y = (i - x) / WIDTH
        id = get_id(x, y)
        obj = {
            "Id": id,
            "Type": "Item",
            "Field08": 1,
            "Field0C": i + 1,
            "ResourceMajorId": 151,
            "ResourceSubId": 0,
            "ResourceMinorId": 175,
            "Field1C": 0,
            "AnimationMajorId": 174,
            "AnimationMinorId": -1,
            "AnimationSubId": -1,
            "Field28": 0,
            "Field2C": 0
        }
        file["Objects"].append(obj)

        set_data = {
            "Type": "MSD_",
            "Field04": 1,
            "Field06": 0,
            "ObjectId": id,
            "Field0C": 0,
            "Frame": 1,
            "Duration": 1,
            "DataSize": 64,
            "EvtFlagType": "None",
            "EvtFlagId": 0,
            "EvtFlagValue": 0,
            "EvtFlagConditionalType": "FlagValue_Equals_FlagIdResult",
            "Data": {
                "Position": {
                    "X": (x - WIDTH / 2) * 30,
                    "Y": (y - HEIGHT / 2) * 30,
                    "Z": 0
                },
                    "Rotation": {
                    "X": 0,
                    "Y": 0,
                    "Z": 0.0
                },
                "Field18": 1143042887,
                "Field1C": 0.0,
                "Field20": -1020883212,
                "Field24": 0.0,
                "Field28": 0,
                "Field2C": 0,
                "Field30": 0,
                "Field34": 0,
                "Field38": 0,
                "Field3C": 0
            }
        }
        file["Commands"].append(set_data)
        change_alpha(id, 10, False)

def change_alpha(id: int, frame: int, show: bool):
    alpha = {
        "Type": "MAlp",
        "Field04": 0,
        "Field06": 0,
        "ObjectId": id,
        "Field0C": 0,
        "Frame": frame + 20,
        "Duration": 1,
        "DataSize": 16,
        "EvtFlagType": "None",
        "EvtFlagId": 0,
        "EvtFlagValue": 0,
        "EvtFlagConditionalType": "FlagValue_Equals_FlagIdResult",
        "Data": {
            "Field00": 0,
            "AlphaLevel": -16777216 if show else 0,
            "Field08": 4354,
            "Field0C": 16777216
        }
    }
    file["Commands"].append(alpha)

def get_id(x: int, y: int):
    return int(y * WIDTH + x + 3)

def frame_parse(frame: int, img):
    global skipped
    img = cv2.resize(img, (WIDTH, HEIGHT), interpolation=cv2.INTER_NEAREST)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.flip(img, 0)

    on = set(zip(*np.where(img > 200)))    # White pixels
    off = set(zip(*np.where(img <= 200)))     # Black pixels
    # on = np.where(np.all(img == [255, 255, 255], 2))
    # off = np.where(np.all(img == [0, 0, 0], 2))

    for y, x in on:
        state = current_values.get(f"{y},{x}")
        if state == None or state == False:
            current_values[f"{y},{x}"] = True
            change_alpha(get_id(x, y), frame, True)
        else:
            skipped += 1

    for y, x in off:
        state = current_values.get(f"{y},{x}")
        if state == None or state == True:
            current_values[f"{y},{x}"] = False
            change_alpha(get_id(x, y), frame, False)
        else:
            skipped += 1


vid = cv2.VideoCapture("badapple.mp4")
if not vid.isOpened():
    raise Exception("Couldn't load the video. Is it named badapple.mp4?")


initial_setup()

for i in range(FRAMES):
    ret, frame = vid.read()
    if not ret:
        print(f"Stopped early at frame {i} (ran out of frames to process)")
        file["Duration"] = i + 50
        break
    frame_parse(i + 1, frame)
    if i % 200 == 0:
        print(f"Frame {i} complete")

vid.release()
print(f"All frames calculated. Optimization saved {skipped} frames! Saving now...")

with open(f"{OUT_PATH}/E100_000.evt.json", "w") as f:
    print("saving")
    json.dump(file, f, indent=2)
    print("Saved. converting...")


subprocess.run(["EvtTool/EvtTool.exe", f"{OUT_PATH}/E100_000.evt.json"])
print("Done!")