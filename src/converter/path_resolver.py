import pathlib
from pathlib import PosixPath


def resolve_output_dir_path(
    input_path: PosixPath,
    input_root_dir: PosixPath,
    output_root_dir: PosixPath,
) -> PosixPath:
    input_root_dir_path = pathlib.Path(input_root_dir)
    relative = input_path.relative_to(input_root_dir_path)
    return pathlib.Path(output_root_dir) / relative
