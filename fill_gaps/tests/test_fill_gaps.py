import srt
from datetime import timedelta

from ..fill_gaps import *
from .factories import subtitle_factory


def test_fill_gaps_detects_gap():
    subtitle_1 = subtitle_factory(1)
    subtitle_2 = subtitle_factory(2, start=subtitle_1.end + timedelta(seconds=3))
    assert has_gap([subtitle_1, subtitle_2])


def test_fill_gaps_detects_when_there_is_no_gap():
    subtitle_1 = subtitle_factory(1)
    subtitle_2 = subtitle_factory(2, subtitle_1.end)

    assert has_gap([subtitle_1, subtitle_2]) == False


def test_fill_gaps_detects_gap_when_order_is_incorrect():
    subtitle_1 = subtitle_factory(1, 5, 6)
    subtitle_2 = subtitle_factory(2, 2, 3)

    assert has_gap([subtitle_1, subtitle_2])


def test_fill_gaps_will_fill_a_gap_for_me():
    subtitle_1 = subtitle_factory(1, 5, 6)
    subtitle_2 = subtitle_factory(2, 2, 3)

    assert has_gap([subtitle_1, subtitle_2])

    subtitles = fill_gaps([subtitle_1, subtitle_2])

    assert has_gap(subtitles) == False


def test_fill_gaps_ignores_gaps_shorter_than_threshold():
    subtitle_1 = subtitle_factory(1, 5, 6)
    subtitle_2 = subtitle_factory(2, 2, 3)

    assert has_gap([subtitle_1, subtitle_2])

    subtitles = fill_gaps([subtitle_1, subtitle_2], threshold=timedelta(seconds=2))

    assert has_gap(subtitles)


def test_fill_gaps_removes_gaps_longer_than_threshold():
    subtitle_1 = subtitle_factory(1, 5, 6)
    subtitle_2 = subtitle_factory(2, 2, 3)

    assert has_gap([subtitle_1, subtitle_2])

    subtitles = fill_gaps([subtitle_1, subtitle_2], threshold=timedelta(seconds=0.5))

    assert has_gap(subtitles) is False


def test_fill_gaps_fills_gaps_with_placeholder():
    subtitle_1 = subtitle_factory(1, 5, 6)
    subtitle_2 = subtitle_factory(2, 2, 3)

    subtitles = srt.sort_and_reindex(
        fill_gaps([subtitle_1, subtitle_2], placeholder="GAP")
    )
    assert list(subtitles)[1].content == "GAP"


def test_fill_gaps_splits_entries():
    subtitle_1 = subtitle_factory(1, 0, 2)
    subtitle_2 = subtitle_factory(2, 8, 10)

    # split in 2 second intervals
    subtitles = list(
        fill_gaps(
            [subtitle_1, subtitle_2], split=timedelta(seconds=2), placeholder="gap"
        )
    )

    assert len(subtitles) == 5
    assert subtitles[4].content == "gap"
    assert subtitles[3].content == "gap"
    assert subtitles[2].content == "gap"


def test_fill_gaps_splits_entries_with_threshold():
    subtitle_1 = subtitle_factory(1, 0, 2)
    subtitle_2 = subtitle_factory(2, 8.4, 9.6)

    # split in 2 second intervals
    subtitles = list(
        fill_gaps(
            [subtitle_1, subtitle_2],
            threshold=timedelta(seconds=1),
            split=timedelta(seconds=2),
            placeholder="gap",
        )
    )

    subtitles = list(srt.sort_and_reindex(subtitles))

    assert len(subtitles) == 5
    assert subtitles[3].content == "gap"
    assert subtitles[3].end == timedelta(seconds=8.4)
    assert subtitles[2].content == "gap"
    assert subtitles[1].content == "gap"


def test_split_subtitle_splits_subtitle():
    subtitle = subtitle_factory(1, 0, 10)
    subtitles = split_subtitle(subtitle, timedelta(seconds=2))

    assert len(subtitles) == 5


def test_split_subtitle_takes_theshold_into_account():
    subtitle = subtitle_factory(1, 0, 10.4)
    subtitles = split_subtitle(subtitle, timedelta(seconds=2), timedelta(seconds=0.5))

    assert len(subtitles) == 5
