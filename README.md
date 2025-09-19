# napari-imagecodecs

[![License MIT](https://img.shields.io/pypi/l/napari-imagecodecs.svg?color=green)](https://github.com/eliwhite/napari-imagecodecs/raw/main/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/napari-imagecodecs.svg?color=green)](https://pypi.org/project/napari-imagecodecs)
[![Python Version](https://img.shields.io/pypi/pyversions/napari-imagecodecs.svg?color=green)](https://python.org)
[![tests](https://github.com/eliwhite/napari-imagecodecs/workflows/tests/badge.svg)](https://github.com/eliwhite/napari-imagecodecs/actions)
[![codecov](https://codecov.io/gh/eliwhite/napari-imagecodecs/branch/main/graph/badge.svg)](https://codecov.io/gh/eliwhite/napari-imagecodecs)
[![napari hub](https://img.shields.io/endpoint?url=https://api.napari-hub.org/shields/napari-imagecodecs)](https://napari-hub.org/plugins/napari-imagecodecs)
[![npe2](https://img.shields.io/badge/plugin-npe2-blue?link=https://napari.org/stable/plugins/index.html)](https://napari.org/stable/plugins/index.html)
[![Copier](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/copier-org/copier/master/img/badge/badge-grayscale-inverted-border-purple.json)](https://github.com/copier-org/copier)

JPEG-LS & JPEG XL Reader for napari

This plugin adds support for loading JPEG-LS (.jls) and JPEG XL (.jxl) images directly into napari, using the high-performance imagecodecs library. It's designed for researchers and imaging scientists who work with microscopy, tomography, or other large-scale imaging datasets stored in modern compressed formats.

## Features

- **File Support**: Read .jls (JPEG-LS) and .jxl (JPEG XL) images
- **Folder Support**: Load entire directories of compressed images as stacked volumes
- **Lazy Loading**: Efficient loading of large datasets using dask
- **Integration**: Automatically registers as a napari reader plugin
- **Performance**: Uses imagecodecs backend for fast decoding
- **Data Types**: Supports grayscale and RGB images, including high-bit-depth scientific data

## Installation

You can install `napari-imagecodecs` via [pip]:

```
pip install napari-imagecodecs
```

If napari is not already installed, you can install `napari-imagecodecs` with napari and Qt via:

```
pip install "napari-imagecodecs[all]"
```


To install latest development version :

```
pip install git+https://github.com/eliwhite/napari-imagecodecs.git
```

## Usage

### Opening Files
Simply drag and drop your .jls or .jxl files into napari, or use File → Open.

### Opening Folders
To load entire directories of compressed images:
1. Use File → Open Folder
2. Select a directory containing .jls or .jxl files
3. All images will be loaded as a stacked volume

### Supported Formats
- **JPEG-LS (.jls)**: Lossless compression, ideal for scientific imaging
- **JPEG XL (.jxl)**: Advanced compression for high-bit-depth images
- **Mixed folders**: Can handle directories with both formats

## Example Use Cases

- Load JPEG-LS compressed microscopy data directly in napari for annotation
- Preview JPEG XL volumes from tissue imaging without converting to TIFF
- Integrate compressed datasets into napari workflows for visualization, segmentation, or registration

## Contributing

Contributions are very welcome. Tests can be run with [tox], please ensure
the coverage at least stays the same before you submit a pull request.

## License

Distributed under the terms of the [MIT] license,
"napari-imagecodecs" is free and open source software

## Issues

If you encounter any problems, please [file an issue] along with a detailed description.

[napari]: https://github.com/napari/napari
[copier]: https://copier.readthedocs.io/en/stable/
[@napari]: https://github.com/napari
[MIT]: http://opensource.org/licenses/MIT
[BSD-3]: http://opensource.org/licenses/BSD-3-Clause
[GNU GPL v3.0]: http://www.gnu.org/licenses/gpl-3.0.txt
[GNU LGPL v3.0]: http://www.gnu.org/licenses/lgpl-3.0.txt
[Apache Software License 2.0]: http://www.apache.org/licenses/LICENSE-2.0
[Mozilla Public License 2.0]: https://www.mozilla.org/media/MPL/2.0/index.txt
[napari-plugin-template]: https://github.com/napari/napari-plugin-template

[file an issue]: https://github.com/eliwhite/napari-imagecodecs/issues

[napari]: https://github.com/napari/napari
[tox]: https://tox.readthedocs.io/en/latest/
[pip]: https://pypi.org/project/pip/
[PyPI]: https://pypi.org/
