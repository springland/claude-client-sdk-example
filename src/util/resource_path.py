from pathlib import Path


def get_resource_path(subdir: str | None = None) -> Path:
    """Return the project's resources directory or an optional subdirectory."""
    project_root = Path(__file__).resolve().parents[2]
    resources_path = project_root / "resources"
    return resources_path / subdir if subdir is not None else resources_path
