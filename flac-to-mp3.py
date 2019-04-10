#!/usr/bin/env python3

"""
Create MP3 derivatives from FLAC files.
Uses pydub to wrap ffmpeg.  See http://pydub.com/
"""

import argparse
from os import walk, makedirs
from os.path import join, splitext, isdir, isfile, exists
from shutil import copy2
from pydub import AudioSegment
import errno


def create_directory(d):
    """Create directories in destination if they don't already exist"""
    try:
        makedirs(d, exist_ok=True)
    except FileExistsError as exc:
        if exc.errno == errno.EEXIST and isdir(d):
            print("Already exists: {}".format(d))
            pass
        else:
            raise


def convert(r, f, p, fn):
    """Convert flac to mp3 using ffmpeg if the derivative doesn't already exist"""
    sourcefile = join(r, f)
    destfile = p.replace(".flac", ".mp3")
    if not isfile(destfile):
        flac_audio = AudioSegment.from_file(sourcefile, "flac")
        flac_audio.export(destfile, format="mp3")
        print("Converting {}".format(destfile))
    else:
        print("Already exists {}".format(destfile))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create MP3s from FLAC files")
    parser.add_argument("-s", '--source', help="Path to flac directory", required=True)
    parser.add_argument("-d", '--destination', help="Path to MP3 directory", required=True)
    args = vars(parser.parse_args())
    source = args["source"]
    destination = args["destination"]
    for root, dirs, files in walk(source, topdown=True):
        for directory in dirs:
            path = join(root, directory).replace(source, destination)
            create_directory(path)
        for file in files:
            newname = file.strip()
            path = join(root, newname).replace(source, destination)
            fname, extension = splitext(file)
            if extension == '.jpg' or extension == '.mp3':
                dest = join(root, file).replace(source, destination)
                if not exists(dest):
                    copy2(join(root, file), dest)
            elif extension == '.flac':
                convert(root, file, path, fname)
