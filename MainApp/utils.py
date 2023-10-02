import os
from datetime import date
from mimetypes import guess_type

from django.core.serializers.json import DjangoJSONEncoder

from .models import FileTypes, FileExtensions

def custom_guess_type(filename):
    EXTENSION_MIME_MAP = {
        '.dwg': 'application/acad',
        '.skp': 'application/vnd.sketchup.skp',
        '.3ds': 'image/x-3ds',
    }

    mimetype = guess_type(filename)[0]
    if mimetype is None:
        _, ext = os.path.splitext(filename)
        ext = ext.lower()
        mimetype = EXTENSION_MIME_MAP.get(ext)

    return mimetype
def get_or_create_file_type(file_mimetype):
    # This function checks if a FileType exists for the given MIME type, and if not, creates one.
    file_type, created = FileTypes.objects.get_or_create(file_type=file_mimetype)
    return file_type

def get_or_create_file_extension(file_name):
    # This function checks if a FileExtension exists for the given file name, and if not, creates one.
    _, ext = os.path.splitext(file_name)
    file_extension, created = FileExtensions.objects.get_or_create(extension=ext)
    return file_extension

class ExtendedEncoder(DjangoJSONEncoder):
    def default(self, o):
        if isinstance(o, date):
            return o.isoformat()
        return super().default(o)