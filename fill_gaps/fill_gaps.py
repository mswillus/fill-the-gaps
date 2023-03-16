from srt import Subtitle
import srt
import math

from datetime import timedelta


def has_gap(subtitles: list[Subtitle]) -> bool:
    gap_detected = False
    subtitles = list(srt.sort_and_reindex(subtitles))
    for subtitle_position in range(len(subtitles) - 1):
        if subtitles[subtitle_position].end < subtitles[subtitle_position + 1].start:
            gap_detected = True
    return gap_detected


def fill_gaps(
    subtitles: list[Subtitle],
    threshold: timedelta = timedelta(0),
    placeholder: str = ".",
    split: timedelta = timedelta(0),
) -> list[Subtitle]:
    if has_gap(subtitles):
        subtitles = list(srt.sort_and_reindex(subtitles))
        number_of_subtitles = len(subtitles)
        index_of_last_subtitle = number_of_subtitles
        for subtitle_position in range(number_of_subtitles - 1):
            before_gap = subtitles[subtitle_position]
            after_gap = subtitles[subtitle_position + 1]
            gap_duration = after_gap.start - before_gap.end
            if gap_duration > threshold:
                gap = Subtitle(
                    index_of_last_subtitle + 1,
                    before_gap.end,
                    after_gap.start,
                    content=placeholder,
                )
                if gap_duration > split and split > timedelta(0):
                    split_gap = split_subtitle(gap, split, threshold)
                    for sub in split_gap:
                        subtitles.append(sub)
                else:
                    subtitles.append(gap)
    return subtitles


def split_subtitle(
    subtitle: Subtitle, max_duration: timedelta, threshold: timedelta = timedelta(0)
) -> list[Subtitle]:
    subtitles = []
    duration = subtitle.end - subtitle.start
    number_of_parts = int(
        math.ceil(duration.total_seconds() / max_duration.total_seconds())
    )
    for part in range(number_of_parts):
        start = part * max_duration + subtitle.start
        end = start + max_duration
        if end > subtitle.end:
            end = subtitle.end
            if end - start < threshold:
                subtitles[part - 1].end = end
        else:
            subtitle_part = Subtitle(part + 1, start, end, subtitle.content)
            subtitles.append(subtitle_part)

    return subtitles
