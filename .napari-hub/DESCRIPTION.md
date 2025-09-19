JPEG-LS & JPEG XL Reader for napari

Summary

This plugin adds support for loading JPEG-LS (.jls) and JPEG XL (.jxl) images directly into napari, using the high-performance imagecodecs library.

It is designed for researchers and imaging scientists who work with microscopy, tomography, or other large-scale imaging datasets stored in modern compressed formats. JPEG-LS offers efficient, lossless compression for grayscale and scientific images, while JPEG XL provides advanced compression for high-bit-depth and photographic data.

With this plugin, you can seamlessly open these files in napari alongside other formats, without needing manual conversion steps.

⸻

Features
	•	File support: Read .jls (JPEG-LS) and .jxl (JPEG XL) images.
	•	Integration: Automatically registers as a napari reader plugin — just drag and drop files into napari.
	•	Performance: Uses the imagecodecs backend for fast decoding of high-bit-depth, large-scale images.
	•	Data types: Supports grayscale and RGB images, including 8-bit, 12-bit, and 16-bit scientific image stacks.

⸻

Quick Start
	1.	Install the plugin from napari-hub or pip.
	2.	Launch napari.
	3.	Drag and drop your .jls or .jxl files into the viewer.

That’s it — your images will load and can be explored, processed, or overlaid like any other napari layer.

⸻

Example Use Case
	•	Load JPEG-LS compressed microscopy data directly in napari for annotation.
	•	Preview JPEG XL volumes from tissue imaging without converting to TIFF.
	•	Integrate compressed datasets into napari workflows for visualization, segmentation, or registration.

⸻

Keywords

JPEG-LS · JPEG XL · compressed images · scientific imaging · microscopy · tomography · high bit depth
