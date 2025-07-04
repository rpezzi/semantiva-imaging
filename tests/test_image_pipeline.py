# Copyright 2025 Semantiva authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pytest
from semantiva.logger import Logger
from semantiva.context_processors.context_types import ContextType
from semantiva.specializations import load_specializations
from semantiva_imaging.data_types import (
    SingleChannelImage,
)
from semantiva.payload_operations import Pipeline
from semantiva_imaging.data_io.loaders_savers import (
    ImageDataRandomGenerator,
    SingleChannelImageStackRandomGenerator,
)
from semantiva.tools import PipelineInspector


@pytest.fixture
def image_stack_data():
    """
    Pytest fixture for providing an SingleChannelImageStack instance using the dummy generator.
    """
    generator = SingleChannelImageStackRandomGenerator()
    return generator.get_data((10, 256, 256))


@pytest.fixture
def random_image1():
    """
    Pytest fixture for providing a random 2D SingleChannelImage instance using the dummy generator.
    """
    generator = ImageDataRandomGenerator()
    return generator.get_data((256, 256))


@pytest.fixture
def random_image2():
    """
    Pytest fixture for providing another random 2D SingleChannelImage instance using the dummy generator.
    """
    generator = ImageDataRandomGenerator()
    return generator.get_data((256, 256))


def test_image_pipeline_execution(image_stack_data, random_image1, random_image2):
    """
    Test the execution of a pipeline with multiple image operations.

    The pipeline consists of:
    1. StackToImageMeanProjector: Flattens the image stack to a 2D image.
    2. ImageAddition: Adds a random image to the flattened image.
    3. ImageSubtraction: Subtracts another random image from the result.
    4. ImageCropper: Clips the final image to a specific region.
    """

    load_specializations("imaging")
    # Define node configurations
    node_configurations = [
        {
            "processor": "StackToImageMeanProjector",
            "parameters": {},
        },
        {
            "processor": "ImageAddition",
            "parameters": {"image_to_add": random_image1},
        },
        {
            "processor": "ImageSubtraction",
            "parameters": {"image_to_subtract": random_image2},
        },
        {
            "processor": "ImageCropper",
            "parameters": {"x_start": 50, "x_end": 200, "y_start": 50, "y_end": 200},
        },
    ]

    # Initialize logger
    logger = Logger()
    logger.set_verbose_level("DEBUG")
    logger.set_console_output()
    # Initialize the pipeline
    pipeline = Pipeline(node_configurations, logger)

    # Initialize the context and process the data
    context = ContextType()
    output_data, output_context = pipeline.process(image_stack_data, context)

    # Validate the output
    assert isinstance(output_data, SingleChannelImage)
    assert isinstance(output_context, ContextType)
    # Expected result validation skipped due to dynamic random inputs

    # Inspect the pipeline
    print("\n")
    print(
        "==============================Pipeline inspection=============================="
    )
    print(PipelineInspector.inspect_pipeline(pipeline))

    # Check timers
    print(
        "================================Pipeline timers================================"
    )
    print(pipeline.get_timers())
    print(
        "==============================================================================="
    )
