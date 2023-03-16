from srt import Subtitle
from faker import Faker
from datetime import timedelta

fake = Faker()


def subtitle_factory(index: int, start: int = None, end: int = None):
    if isinstance(start, (int, float)):
        start = timedelta(seconds=start)
    if isinstance(end, (int, float)):
        end = timedelta(seconds=end)

    if start == None:
        start = fake.random_digit_not_null()
        start = timedelta(seconds=start)

    if end == None:
        end = start + timedelta(seconds=fake.random_digit_not_null())
    return Subtitle(
        index=index, start=start, end=end, content=fake.sentence(nb_words=7)
    )
