"""
This module provides imagecodecs-based readers for napari.

It implements the Reader specification for various image formats supported by imagecodecs.
see: https://napari.org/stable/plugins/building_a_plugin/guides.html#readers
"""

import glob
import os

import dask.array as da
import imagecodecs
import numpy as np
from dask import delayed


def napari_get_reader(path):
    """A Reader contribution for imagecodecs-supported formats.

    Parameters
    ----------
    path : str or list of str
        Path to file, or list of paths.

    Returns
    -------
    function or None
        If the path is a recognized format, return a function that accepts the
        same path or list of paths, and returns a list of layer data tuples.
    """
    if isinstance(path, list):
        # reader plugins may be handed single path, or a list of paths.
        # if it is a list, it is assumed to be an image stack...
        # so we are only going to look at the first file.
        path = path[0]

    # Check if it's a directory
    if os.path.isdir(path):
        # Check if directory contains supported files
        supported_extensions = (".npy", ".jls", ".jxl")
        found_files = []
        for ext in supported_extensions:
            found_files.extend(glob.glob(os.path.join(path, f"*{ext}")))

        if not found_files:
            return None
        # Return the reader function for directory loading
        return reader_function

    # Check if the file extension is supported by imagecodecs
    supported_extensions = (".npy", ".jls", ".jxl")
    if not any(path.lower().endswith(ext) for ext in supported_extensions):
        return None

    # otherwise we return the *function* that can read ``path``.
    return reader_function


def reader_function(path):
    """Take a path or list of paths and return a list of LayerData tuples.

    Readers are expected to return data as a list of tuples, where each tuple
    is (data, [add_kwargs, [layer_type]]), "add_kwargs" and "layer_type" are
    both optional.

    Parameters
    ----------
    path : str or list of str
        Path to file, or list of paths.

    Returns
    -------
    layer_data : list of tuples
        A list of LayerData tuples where each tuple in the list contains
        (data, metadata, layer_type), where data is a numpy array, metadata is
        a dict of keyword arguments for the corresponding viewer.add_* method
        in napari, and layer_type is a lower-case string naming the type of
        layer. Both "meta", and "layer_type" are optional. napari will
        default to layer_type=="image" if not provided
    """
    # handle both a string and a list of strings
    paths = [path] if isinstance(path, str) else path

    # If it's a directory, find all supported files
    if len(paths) == 1 and os.path.isdir(paths[0]):
        directory = paths[0]
        supported_extensions = (".npy", ".jls", ".jxl")
        found_files = []
        for ext in supported_extensions:
            found_files.extend(glob.glob(os.path.join(directory, f"*{ext}")))

        if not found_files:
            raise ValueError(
                f"No supported files found in directory: {directory}"
            )

        # Sort files for consistent ordering
        found_files.sort()
        paths = found_files

    # Implement lazy loading using dask
    def load_single_file(file_path):
        """Load a single file and return its data."""
        if file_path.lower().endswith(".npy"):
            # Handle numpy files
            return np.load(file_path)
        elif file_path.lower().endswith(".jls"):
            # Handle JPEG-LS files
            with open(file_path, "rb") as f:
                data = f.read()
            return imagecodecs.jpegls_decode(data)
        elif file_path.lower().endswith(".jxl"):
            # Handle JPEG XL files
            with open(file_path, "rb") as f:
                data = f.read()
            return imagecodecs.jpegxl_decode(data)
        else:
            raise ValueError(f"Unsupported file format: {file_path}")

    # For single files, load immediately
    if len(paths) == 1 and not os.path.isdir(paths[0]):
        data = load_single_file(paths[0])
    else:
        # For multiple files or directories, use dask for lazy loading
        # First, load one file to get the shape and dtype
        sample_data = load_single_file(paths[0])
        shape = sample_data.shape
        dtype = sample_data.dtype

        # Create dask array with lazy loading
        lazy_arrays = []
        for i, file_path in enumerate(paths):
            # Create a delayed function that loads the file when needed
            delayed_load = delayed(load_single_file)(file_path)
            # Create a dask array from the delayed computation
            lazy_array = da.from_delayed(
                delayed_load, shape=shape, dtype=dtype, name=f"load_{i}"
            )
            lazy_arrays.append(lazy_array)

        # Stack the lazy arrays
        data = da.squeeze(da.stack(lazy_arrays))

    # optional kwargs for the corresponding viewer.add_* method
    add_kwargs = {}

    layer_type = "image"  # optional, default is "image"
    return [(data, add_kwargs, layer_type)]
