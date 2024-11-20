from typing import Any

from src.poc.model import Base


def base_to_dict(base: Base, include_nones: bool = False) -> dict[str, Any]:
    """
    Transforms a Base model into a dictionary

    Args:
        base: entity
        include_nones (bool): if True, set nullable attributes

    Returns:
        dict[str, Any]: model dictionary
    """
    return {
        column.name: getattr(base, column.name)
        for column in base.__table__.columns
        if include_nones or getattr(base, column.name) is not None
    }
