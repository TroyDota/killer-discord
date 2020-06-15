from datetime import datetime


def datetime_from_iso(iso):
    try:
        return datetime.strptime(iso, "%Y-%m-%dT%H:%M:%S.%f%z")
    except:
        return datetime.strptime(iso, "%Y-%m-%dT%H:%M:%S%z")
