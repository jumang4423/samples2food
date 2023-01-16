import sys
import os
from os.path import exists
import json
import random
from PIL import Image
from itertools import product
from tqdm import tqdm
from pathlib import Path
from util.get_backend import get_backend
from riffusion.audio2img import audio_to_image

tile_size = 512

# devide one img which n x 512px into 512 x 512 imgs
def tile(filename, dir_out, tmp_png_path):
    name = Path(filename).stem
    img = Image.open(tmp_png_path)
    w, h = img.size
    fileNames = []
    if w < tile_size:
        print("audio file too short, must longer than 6s")
        print("filename: ", filename)
    for i, j in product(range(0, w, tile_size), range(0, h, tile_size)):
        tile = img.crop((i, j, i + tile_size, j + tile_size))
        tileId = int((i/512) + 1)
        if tileId != int(w / 512) + 1:
            # ex: futuristic_dreamy_1.png
            tileIdStr = "_" + str(tileId)
            tile.save(os.path.join(dir_out, name + tileIdStr + ".png"))
            fileNames.append(os.path.join(dir_out, name + tileIdStr + ".png"))

    return fileNames

def folder_valid(img_out, sound_dir, cap_out):
    # if img output dir doesnt exist
    if not os.path.exists(img_out):
        os.makedirs(img_out)
    # if caption output dir doesnt exist
    if not os.path.exists(cap_out):
        os.makedirs(cap_out)
    # if sound_dir doesnt exist
    if not os.path.exists(sound_dir):
        print("sound_dir doesnt exist")
        exit(1)
        return

def soundfile_name_validation(sound_dir):
    # accept .wav or .mp3
    # replace _ with , in text then rename
    for file in os.listdir(sound_dir):
        if file.endswith(".wav") or file.endswith(".mp3"):
            # replace _ with , in text then rename
            new_file_name = file.replace("_", ", ").replace(" ", "-")
            os.rename(os.path.join(sound_dir, file), os.path.join(sound_dir, new_file_name))


def get_sound_file_paths(sound_dir):
    sound_file_paths = []
    for root, dirs, files in os.walk(sound_dir):
        for file in files:
            if file.endswith(".wav") or file.endswith(".mp3"):
                sound_file_paths.append(os.path.join(root, file))
    return sound_file_paths

# create json object then save to out_dir + arr_r
def write_jsonl_metadata(arr_r, out_dir):
    jsonl_file_path = os.path.join(out_dir, "metadata.jsonl")

    # if metadata.jsonl already exists, delete once
    if exists(jsonl_file_path):
        os.remove(jsonl_file_path)

    data = []
    for line in arr_r:
        image_file_path = Path(line).stem + ".png"
        data.append(
            {
                "image_file_path": image_file_path,
                "text": "_".join(Path(line).stem.split("_")[:-1]).replace("_", ", ").replace("-", " "),
            }
        )
    with open(jsonl_file_path, "w") as metadata_file:
        for line in data:
            metadata_file.write(json.dumps(line) + "\n")

    return data

def write_captions(jsonl_obj, caption_out):
    for json_dict in jsonl_obj:
        with open(os.path.join(caption_out, json_dict["image_file_path"].replace(".png", ".txt")), "w") as f:
            f.write(json_dict["text"])

# clean up tempo fl
def rm_tempo_img(tmp_file_path):
    os.remove(tmp_file_path)

def samples2food(sound_file_paths, img_out, caption_out):
    bar = tqdm(total=len(sound_file_paths))
    fileNames = []
    for sound_file_path in sound_file_paths:
        # gen long png as tmp.png from audio file
        temp_image_path = "./tmp.png"
        audio_to_image(sound_file_path, temp_image_path, device=get_backend())
        _file_names = tile(sound_file_path, img_out, temp_image_path)
        fileNames.extend(_file_names)
        bar.update(1)

    # write metadata.jsonl
    jsonl_obj = write_jsonl_metadata(fileNames, img_out)

    # remove tmp.png
    rm_tempo_img(temp_image_path)

    # write captions
    write_captions(jsonl_obj, caption_out)
