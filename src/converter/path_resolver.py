import pathlib
from pathlib import Path


def resolve_output_dir_path(
    input_path: Path,
    input_root_dir: Path,
    output_root_dir: Path,
) -> Path:
    input_root_dir_path = pathlib.Path(input_root_dir)
    relative = input_path.relative_to(input_root_dir_path)
    return pathlib.Path(output_root_dir) / relative
