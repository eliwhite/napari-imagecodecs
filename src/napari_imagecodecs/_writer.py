"""
This module provides imagecodecs-based writers for napari.

It implements the Writer specification for various image formats supported by imagecodecs.
see: https://napari.org/stable/plugins/building_a_plugin/guides.html#writers
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING, Any, Union

import imagecodecs
import numpy as np

if TYPE_CHECKING:
    DataType = Union[Any, Sequence[Any]]
    FullLayerData = tuple[DataType, dict, str]


def write_single_image(path: str, data: Any, meta: dict) -> list[str]:
    """Writes a single image layer.

    Parameters
    ----------
    path : str
        A string path indicating where to save the image file.
    data : The layer data
        The `.data` attribute from the napari layer.
    meta : dict
        A dictionary containing all other attributes from the napari layer
        (excluding the `.data` layer attribute).

    Returns
    -------
    [path] : A list containing the string path to the saved file.
    """
    # Convert data to numpy array if it isn't already
    if not isinstance(data, np.ndarray):
        data = np.asarray(data)

    # Determine file format and write accordingly
    if path.lower().endswith(".npy"):
        np.save(path, data)
    elif path.lower().endswith(".jls"):
        # Convert to uint8 if needed for JPEG-LS
        if data.dtype != np.uint8:
            data = data.astype(np.uint8)
        encoded_data = imagecodecs.jpegls_encode(data)
        with open(path, "wb") as f:
            f.write(encoded_data)
    elif path.lower().endswith(".jxl"):
        # Convert to uint8 if needed for JPEG XL
        if data.dtype != np.uint8:
            data = data.astype(np.uint8)
        encoded_data = imagecodecs.jpegxl_encode(data)
        with open(path, "wb") as f:
            f.write(encoded_data)
    else:
        # Default to numpy format for unsupported extensions
        np.save(path, data)

    # return path to any file(s) that were successfully written
    return [path]


def write_multiple(path: str, data: list[FullLayerData]) -> list[str]:
    """Writes multiple layers of different types.

    Parameters
    ----------
    path : str
        A string path indicating where to save the data file(s).
    data : A list of layer tuples.
        Tuples contain three elements: (data, meta, layer_type)
        `data` is the layer data
        `meta` is a dictionary containing all other metadata attributes
        from the napari layer (excluding the `.data` layer attribute).
        `layer_type` is a string, eg: "image", "labels", "surface", etc.

    Returns
    -------
    [path] : A list containing (potentially multiple) string paths to the saved file(s).
    """
    saved_paths = []

    # For multiple layers, we'll save each as a separate file
    # with a suffix indicating the layer index
    base_path = path
    if "." in base_path:
        base_name, ext = base_path.rsplit(".", 1)
    else:
        base_name = base_path
        ext = "npy"  # default extension

    for i, (layer_data, _meta, _layer_type) in enumerate(data):
        layer_path = path if len(data) == 1 else f"{base_name}_layer_{i}.{ext}"

        # Convert data to numpy array if it isn't already
        if not isinstance(layer_data, np.ndarray):
            layer_data = np.asarray(layer_data)

        # Write the layer data
        if layer_path.lower().endswith(".npy"):
            np.save(layer_path, layer_data)
        elif layer_path.lower().endswith(".jls"):
            # Convert to uint8 if needed for JPEG-LS
            if layer_data.dtype != np.uint8:
                layer_data = layer_data.astype(np.uint8)
            encoded_data = imagecodecs.jpegls_encode(layer_data)
            with open(layer_path, "wb") as f:
                f.write(encoded_data)
        elif layer_path.lower().endswith(".jxl"):
            # Convert to uint8 if needed for JPEG XL
            if layer_data.dtype != np.uint8:
                layer_data = layer_data.astype(np.uint8)
            encoded_data = imagecodecs.jpegxl_encode(layer_data)
            with open(layer_path, "wb") as f:
                f.write(encoded_data)
        else:
            # Default to numpy format for unsupported extensions
            layer_path = f"{base_name}_layer_{i}.npy"
            np.save(layer_path, layer_data)

        saved_paths.append(layer_path)

    # return path to any file(s) that were successfully written
    return saved_paths
