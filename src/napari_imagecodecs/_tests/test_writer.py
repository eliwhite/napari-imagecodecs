import imagecodecs
import numpy as np

from napari_imagecodecs import write_multiple, write_single_image


def test_write_single_image_npy(tmp_path):
    """Test writing single image as NPY."""
    my_test_file = str(tmp_path / "myfile.npy")
    original_data = np.random.rand(20, 20)

    # Write the data
    result = write_single_image(my_test_file, original_data, {})
    assert result == [my_test_file]

    # Read it back and verify
    loaded_data = np.load(my_test_file)
    np.testing.assert_allclose(original_data, loaded_data)


def test_write_single_image_jls(tmp_path):
    """Test writing single image as JLS."""
    my_test_file = str(tmp_path / "myfile.jls")
    original_data = np.random.randint(0, 255, (20, 20), dtype=np.uint8)

    # Write the data
    result = write_single_image(my_test_file, original_data, {})
    assert result == [my_test_file]

    # Read it back and verify
    with open(my_test_file, "rb") as f:
        encoded_data = f.read()
    loaded_data = imagecodecs.jpegls_decode(encoded_data)
    np.testing.assert_allclose(original_data, loaded_data)


def test_write_single_image_jxl(tmp_path):
    """Test writing single image as JXL."""
    my_test_file = str(tmp_path / "myfile.jxl")
    original_data = np.random.randint(0, 255, (20, 20), dtype=np.uint8)

    # Write the data
    result = write_single_image(my_test_file, original_data, {})
    assert result == [my_test_file]

    # Read it back and verify
    with open(my_test_file, "rb") as f:
        encoded_data = f.read()
    loaded_data = imagecodecs.jpegxl_decode(encoded_data)
    np.testing.assert_allclose(original_data, loaded_data)


def test_write_multiple(tmp_path):
    """Test writing multiple layers."""
    my_test_file = str(tmp_path / "myfile.npy")
    original_data1 = np.random.rand(20, 20)
    original_data2 = np.random.rand(20, 20)

    # Create layer data
    layer_data = [(original_data1, {}, "image"), (original_data2, {}, "image")]

    # Write the data
    result = write_multiple(my_test_file, layer_data)
    assert len(result) == 2

    # Read back and verify
    for i, path in enumerate(result):
        loaded_data = np.load(path)
        if i == 0:
            np.testing.assert_allclose(original_data1, loaded_data)
        else:
            np.testing.assert_allclose(original_data2, loaded_data)
