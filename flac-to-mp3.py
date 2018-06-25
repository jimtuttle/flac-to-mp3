#!/usr/bin/env python3
from optparse import OptionParser
from os import walk, listdir, makedirs
from os.path import join, splitext, isdir, exists
from shutil import copy2
from pydub import AudioSegment
from subprocess import run
import errno


def makedir(d):
    """Create directories in destination if they don't already exist"""
    try:
        makedirs(d)
    except FileExistsError as exc:
        if exc.errno == errno.EEXIST and isdir(d):
            pass
        else:
            raise


def convert(r, f, d, p, fn):
    """Convert flac to mp3 using ffmpeg if the derivative doesn't already exist"""
    sourcefile = join(r, f)
    destfile = join(d, fn + '.mp3')
    if not exists(destfile):
        flac_audio = AudioSegment.from_file(sourcefile, "flac")
        flac_audio.export(destfile, format="mp3")
        print("Converting {}".format(destfile))
    else:
        print("Already exists ".format(destfile))


parser = OptionParser()
parser.add_option("-s", "--source", dest="source",
                  help="path to directory containing FLAC files", metavar="FILE")
parser.add_option("-d", "--destination", dest="destination",
                  help="path to directory containing FLAC files", metavar="FILE")
(options, args) = parser.parse_args()


for root, dirs, files in walk(source):
    for file in files:
        path = root.replace(source, '')  # file path minus source path
        destdir = join(destination, path)  # path to new derivative directory
        makedir(destdir)
        fname, extension = splitext(file)
        if extension == '.jpg' or extension == '.mp3':
            if not exists(join(destdir, file)):
                copy2(join(root, file), join(destdir, file))
        elif extension == '.flac':
            convert(root, file, destdir, path, fname)
