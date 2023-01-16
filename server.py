import sys

def main():
    if len(sys.argv) < 2:
        print("Usage: python server.py <sound_dir>")
        exit(1)
    sound_dir = sys.argv[1]
    img_out = sound_dir + "/img_out"
    cap_out = sound_dir + "/cap_out"
    # load lib for samples2food
    from samples2food import samples2food, folder_valid, get_sound_file_paths, soundfile_name_validation
    soundfile_name_validation(sound_dir)
    folder_valid(cap_out, sound_dir, img_out)
    sound_file_paths = get_sound_file_paths(sound_dir)
    # samples2food
    print("🍎 samples2food started")
    samples2food(sound_file_paths, img_out, cap_out)
    print("🍎 samples2food finished")

if __name__ == "__main__":
    main()
