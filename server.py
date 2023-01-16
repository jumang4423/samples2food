import sys

def main():
    if len(sys.argv) < 3:
        print("Usage: python server.py <sound_dir> <output_dir>")
        exit(1)
    sound_dir = sys.argv[1]
    dir_out = sys.argv[2]
    # load lib for samples2food
    from samples2food import samples2food, folder_valid, get_sound_file_paths, soundfile_name_validation
    soundfile_name_validation(sound_dir)
    folder_valid(dir_out, sound_dir)
    sound_file_paths = get_sound_file_paths(sound_dir)
    # samples2food
    print("🍎 samples2food started")
    samples2food(sound_file_paths, dir_out)
    print("🍎 samples2food finished")

if __name__ == "__main__":
    main()
