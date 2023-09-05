from logging import info, debug, error
import logging
import argparse
import os
import srt
from datetime import timedelta

from fill_gaps.fill_gaps import fill_gaps

logging.basicConfig(level=logging.INFO)

parser = argparse.ArgumentParser(
    prog="Subtitle gap filler",
    description="Looks for gaps in your subtitle and fills them",
)

parser.add_argument("filename", help="srt file")
args = parser.parse_args()

if not os.path.exists("./" + args.filename):
    error("The file you specified does not exist")
    exit()

elif not args.filename.endswith(".srt"):
    error("You did not specify a srt file")
    exit()

srt_file = open(args.filename, "r")

srt_file_content = srt_file.read()
subtitles = list(srt.parse(srt_file_content))

threshold = 0.5
split = 2
placeholder = "."
info(f"Inserting \"{placeholder}\" where gapps of at least {threshold} seconds appear.")
info(f"Inserted gapps will be split into blocks of {split} seconds, if the gap is bigger then {split+threshold}")

subtitles = srt.sort_and_reindex(
    fill_gaps(subtitles, threshold=timedelta(seconds=threshold), split=timedelta(seconds=split))
)

subtitles_srt = srt.compose(subtitles)

info("Writing new subtitle file to ./filled.srt")
modified_file = open("./filled.srt", "x")
modified_file.writelines(subtitles_srt)
