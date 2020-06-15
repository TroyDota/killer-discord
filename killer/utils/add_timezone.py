from datetime import timezone


def add_utc(datetime):
    return datetime.replace(tzinfo=timezone.utc)


def to_utc(datetime):
    return datetime.astimezone(timezone.utc)
