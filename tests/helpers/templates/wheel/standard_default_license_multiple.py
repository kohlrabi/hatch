from hatch.template import File
from hatch.utils.fs import Path
from hatchling.__about__ import __version__
from hatchling.metadata.utils import DEFAULT_METADATA_VERSION

from ..new.licenses_multiple import get_files as get_template_files
from .utils import update_record_file_contents


def get_files(**kwargs):
    metadata_directory = kwargs.get('metadata_directory', '')

    files = []
    for f in get_template_files(**kwargs):
        first_part = f.path.parts[0]

        if first_part == 'LICENSES':
            files.append(File(Path(metadata_directory, 'license_files', 'LICENSES', f.path.parts[1]), f.contents))

        if first_part != kwargs['package_name']:
            continue

        files.append(f)

    files.append(File(Path(metadata_directory, 'entry_points.txt'), ''))
    files.append(
        File(
            Path(metadata_directory, 'WHEEL'),
            f"""\
Wheel-Version: 1.0
Generator: hatch {__version__}
Root-Is-Purelib: true
Tag: py2-none-any
Tag: py3-none-any
""",
        )
    )
    files.append(
        File(
            Path(metadata_directory, 'METADATA'),
            f"""\
Metadata-Version: {DEFAULT_METADATA_VERSION}
Name: {kwargs['project_name_normalized']}
Version: 0.0.1
""",
        )
    )

    record_file = File(Path(metadata_directory, 'RECORD'), '')
    update_record_file_contents(record_file, files)
    files.append(record_file)

    return files
