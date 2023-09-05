# Fill the Gaps

I am a tiny tool that fills gaps in subtitles.

## Usage

With default values: Replace any gaps in a subtitle that are longer than 0.5 second with a '.' and save the new subtitle file to "./filled.srt". If a gap is longer than 2 seconds, segment it into parts which are at most 2 seconds and at least 0.5 seconds long.

    python3 ./fill-the-gaps.py subtitles.srt


