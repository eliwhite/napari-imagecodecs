import imagecodecs
import numpy as np

from napari_imagecodecs import napari_get_reader


# tmp_path is a pytest fixture
def test_reader(tmp_path):
    """An example of how you might test your plugin."""

    # write some fake data using your supported file format
    my_test_file = str(tmp_path / "myfile.npy")
    original_data = np.random.rand(20, 20)
    np.save(my_test_file, original_data)

    # try to read it back in
    reader = napari_get_reader(my_test_file)
    assert callable(reader)

    # make sure we're delivering the right format
    layer_data_list = reader(my_test_file)
    assert isinstance(layer_data_list, list) and len(layer_data_list) > 0
    layer_data_tuple = layer_data_list[0]
    assert isinstance(layer_data_tuple, tuple) and len(layer_data_tuple) > 0

    # make sure it's the same as it started
    np.testing.assert_allclose(original_data, layer_data_tuple[0])


def test_get_reader_pass():
    reader = napari_get_reader("fake.file")
    assert reader is None


def test_reader_jls(tmp_path):
    """Test reading JLS files."""
    # Create test data
    my_test_file = str(tmp_path / "myfile.jls")
    original_data = np.random.randint(0, 255, (20, 20), dtype=np.uint8)

    # Encode and save as JLS
    encoded_data = imagecodecs.jpegls_encode(original_data)
    with open(my_test_file, "wb") as f:
        f.write(encoded_data)

    # Try to read it back
    reader = napari_get_reader(my_test_file)
    assert callable(reader)

    # Make sure we're delivering the right format
    layer_data_list = reader(my_test_file)
    assert isinstance(layer_data_list, list) and len(layer_data_list) > 0
    layer_data_tuple = layer_data_list[0]
    assert isinstance(layer_data_tuple, tuple) and len(layer_data_tuple) > 0

    # Make sure it's the same as it started
    np.testing.assert_allclose(original_data, layer_data_tuple[0])


def test_reader_jxl(tmp_path):
    """Test reading JXL files."""
    # Create test data
    my_test_file = str(tmp_path / "myfile.jxl")
    original_data = np.random.randint(0, 255, (20, 20), dtype=np.uint8)

    # Encode and save as JXL
    encoded_data = imagecodecs.jpegxl_encode(original_data)
    with open(my_test_file, "wb") as f:
        f.write(encoded_data)

    # Try to read it back
    reader = napari_get_reader(my_test_file)
    assert callable(reader)

    # Make sure we're delivering the right format
    layer_data_list = reader(my_test_file)
    assert isinstance(layer_data_list, list) and len(layer_data_list) > 0
    layer_data_tuple = layer_data_list[0]
    assert isinstance(layer_data_tuple, tuple) and len(layer_data_tuple) > 0

    # Make sure it's the same as it started
    np.testing.assert_allclose(original_data, layer_data_tuple[0])


def test_get_reader_unsupported():
    """Test that unsupported file formats return None."""
    reader = napari_get_reader("fake.file")
    assert reader is None

    reader = napari_get_reader("test.txt")
    assert reader is None


def test_reader_directory(tmp_path):
    """Test reading a directory containing JLS and JXL files."""
    # Create test directory with multiple files
    test_dir = tmp_path / "test_images"
    test_dir.mkdir()

    # Create some test JLS files
    for i in range(3):
        file_path = test_dir / f"image_{i:03d}.jls"
        original_data = np.random.randint(0, 255, (20, 20), dtype=np.uint8)
        encoded_data = imagecodecs.jpegls_encode(original_data)
        with open(file_path, "wb") as f:
            f.write(encoded_data)

    # Create some test JXL files
    for i in range(2):
        file_path = test_dir / f"image_{i+3:03d}.jxl"
        original_data = np.random.randint(0, 255, (20, 20), dtype=np.uint8)
        encoded_data = imagecodecs.jpegxl_encode(original_data)
        with open(file_path, "wb") as f:
            f.write(encoded_data)

    # Test reading the directory
    reader = napari_get_reader(str(test_dir))
    assert callable(reader)

    # Read the data
    layer_data_list = reader(str(test_dir))
    assert isinstance(layer_data_list, list) and len(layer_data_list) > 0
    layer_data_tuple = layer_data_list[0]
    assert isinstance(layer_data_tuple, tuple) and len(layer_data_tuple) > 0

    # Check that we got a stacked array (5 images stacked)
    data = layer_data_tuple[0]
    assert data.shape[0] == 5  # 3 JLS + 2 JXL files


def test_reader_directory_empty(tmp_path):
    """Test reading an empty directory returns None."""
    empty_dir = tmp_path / "empty"
    empty_dir.mkdir()

    reader = napari_get_reader(str(empty_dir))
    assert reader is None


def test_reader_directory_mixed(tmp_path):
    """Test reading a directory with mixed supported and unsupported files."""
    test_dir = tmp_path / "mixed"
    test_dir.mkdir()

    # Create a JLS file
    jls_file = test_dir / "image.jls"
    original_data = np.random.randint(0, 255, (20, 20), dtype=np.uint8)
    encoded_data = imagecodecs.jpegls_encode(original_data)
    with open(jls_file, "wb") as f:
        f.write(encoded_data)

    # Create an unsupported file
    txt_file = test_dir / "readme.txt"
    with open(txt_file, "w") as f:
        f.write("This is a text file")

    # Should still work because there's at least one supported file
    reader = napari_get_reader(str(test_dir))
    assert callable(reader)

    # Read the data
    layer_data_list = reader(str(test_dir))
    assert isinstance(layer_data_list, list) and len(layer_data_list) > 0
    layer_data_tuple = layer_data_list[0]
    assert isinstance(layer_data_tuple, tuple) and len(layer_data_tuple) > 0

    # Should only load the JLS file
    data = layer_data_tuple[0]
    assert data.shape == (20, 20)  # Single image, not stacked
