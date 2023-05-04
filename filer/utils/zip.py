from zipfile import ZipFile

from django.core.files.uploadedfile import SimpleUploadedFile


def unzip(file_obj):
    """
    Take a path to a zipfile and checks if it is a valid zip file
    and returns...
    """
    files = []
    # TODO: implement try-except here
    zip = ZipFile(file_obj)
    if bad_file := zip.testzip():
        raise Exception(f'"{bad_file}" in the .zip archive is corrupt.')
    infolist = zip.infolist()
    for zipinfo in infolist:
        if zipinfo.filename.startswith('__'):  # do not process meta files
            continue
        file_obj = SimpleUploadedFile(name=zipinfo.filename, content=zip.read(zipinfo))
        files.append((file_obj, zipinfo.filename))
    zip.close()
    return files
