import os

from django.utils.encoding import force_str
from django.utils.timezone import now

from .files import get_valid_filename


def by_date(instance, filename):
    datepart = force_str(now().strftime("%Y/%m/%d"))
    return os.path.join(datepart, get_valid_filename(filename))


def randomized(instance, filename):
    import uuid
    uuid_str = str(uuid.uuid4())
    return os.path.join(
        uuid_str[:2], uuid_str[2:4], uuid_str, get_valid_filename(filename)
    )


class prefixed_factory:
    def __init__(self, upload_to, prefix):
        self.upload_to = upload_to
        self.prefix = prefix

    def __call__(self, instance, filename):
        if callable(self.upload_to):
            upload_to_str = self.upload_to(instance, filename)
        else:
            upload_to_str = self.upload_to
        return (
            os.path.join(self.prefix, upload_to_str)
            if self.prefix
            else upload_to_str
        )
