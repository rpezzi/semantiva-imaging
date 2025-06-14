"""Domain-specific single-channel data types."""

import numpy as np
from typing import Iterator
from semantiva.data_types import BaseDataType, DataCollectionType


_ALLOWED_DTYPES = (np.uint8, np.float32, np.float64)


class SingleChannelImage(BaseDataType):
    """
    A class representing a 2D single-channel image.
    This class inherits from `BaseDataType` and is designed to handle 2D single-channel images.
    It validates the input data to ensure it is a 2D NumPy array and supports automatic casting
    of certain data types to `float32` if specified.
    """

    def __init__(self, data: np.ndarray, auto_cast: bool = True, *args, **kwargs):
        """
        Initializes the SingleChannelImage instance.

        Parameters:
            data (numpy.ndarray): The image data to be stored and validated.
            auto_cast (bool): If True, automatically casts uint16 and int16 data types to float32.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Raises:
            AssertionError: If the input data is not of an allowed dtype and auto_cast is True.
        """
        assert data.ndim == 2, f"SingleChannelImage expects 2-D, got ndim={data.ndim}"
        if data.dtype in (np.uint16, np.int16) and auto_cast:
            data = data.astype(np.float32)
        if auto_cast:
            assert (
                data.dtype in _ALLOWED_DTYPES
            ), f"Unsupported dtype {data.dtype}; allowed {_ALLOWED_DTYPES}"
        super().__init__(
            data,
        )

    def validate(self, data: np.ndarray):
        """
        Validates that the input data is a 2D NumPy array.

        Parameters:
            data (numpy.ndarray): The data to validate.

        Raises:
            AssertionError: If the input data is not a NumPy array.
            AssertionError: If the input data is not a 2D array.
        """
        assert isinstance(
            data, np.ndarray
        ), f"Data must be a numpy ndarray, got {type(data)}."
        assert data.ndim == 2, "Data must be a 2D array."
        return data

    def __str__(self):
        return f"SingleChannelImage: {self.data.shape}"


class SingleChannelImageStack(DataCollectionType[SingleChannelImage, np.ndarray]):
    """
    A class representing a 2D image.
    """

    def __init__(self, data: np.ndarray, auto_cast: bool = True, *args, **kwargs):
        assert (
            data.ndim == 3
        ), f"SingleChannelImageStack expects 3-D, got ndim={data.ndim}"
        if data.dtype in (np.uint16, np.int16) and auto_cast:
            data = data.astype(np.float32)
        if auto_cast:
            assert (
                data.dtype in _ALLOWED_DTYPES
            ), f"Unsupported --- dtype {data.dtype}; allowed {_ALLOWED_DTYPES}"
        super().__init__(data, *args, **kwargs)

    def validate(self, data: np.ndarray):
        """
        Validates that the input data is an 3-dimensional NumPy array.

        Parameters:
            data (numpy.ndarray): The data to validate.

        Raises:
            AssertionError: If the input data is not a NumPy array.
        """
        assert isinstance(data, np.ndarray), "Data must be a numpy ndarray."
        assert data.ndim == 3, "Data must be a 3D array (stack of 2D images)"

    def __iter__(self) -> Iterator[SingleChannelImage]:
        """Iterates through the 3D NumPy array, treating each 2D slice as an SingleChannelImage."""
        for i in range(self._data.shape[0]):
            yield SingleChannelImage(self._data[i])

    def append(self, item: SingleChannelImage) -> None:
        """
        Appends a 2D image to the image stack.

        This method takes an `SingleChannelImage` instance and adds its underlying 2D NumPy array
        to the existing 3D NumPy stack. If the stack is empty, it initializes it with the new image.

        Args:
            item (SingleChannelImage): The 2D image to append.

        Raises:
            TypeError: If the item is not an instance of `SingleChannelImage`.
            ValueError: If the image dimensions do not match the existing stack.
        """
        if not isinstance(item, SingleChannelImage):
            raise TypeError(f"Expected SingleChannelImage, got {type(item)}")

        new_image = item.data  # Extract the 2D NumPy array

        if not isinstance(new_image, np.ndarray) or new_image.ndim != 2:
            raise ValueError(f"Expected a 2D NumPy array, got shape {new_image.shape}")

        # If the stack is empty, initialize with the first image
        if self._data.size == 0:
            self._data = np.expand_dims(
                new_image, axis=0
            )  # Convert 2D to 3D with shape (1, H, W)
        else:
            # Ensure the new image has the same dimensions as existing ones
            if new_image.shape != self._data.shape[1:]:
                raise ValueError(
                    f"Image dimensions {new_image.shape} do not match existing stack {self._data.shape[1:]}"
                )

            # Append along the first axis (stack dimension)
            self._data = np.concatenate(
                (self._data, np.expand_dims(new_image, axis=0)), axis=0
            )

    @classmethod
    def _initialize_empty(cls) -> np.ndarray:
        """
        Returns an empty 3D NumPy array for initializing an empty ImageStackDataType.
        """
        return np.empty((0, 0, 0))  # Empty 3D array

    def __len__(self) -> int:
        """
        Returns the number of images in the stack.

        This method returns the number of 2D images stored along the first axis of
        the 3D NumPy array.

        Returns:
            int: The number of images in the stack.
        """
        return self._data.shape[0]

    def __str__(self):
        return f"ImageStackDataType: {self._data.shape}"
