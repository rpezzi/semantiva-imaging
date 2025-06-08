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
import numpy as np
from semantiva_imaging.data_types import SingleChannelImageStack
from semantiva_imaging.visualization.viewers import SingleChannelImageStackAnimator


# Sample test data
@pytest.fixture
def test_image_stack():
    """Fixture to provide test image stack data."""
    return SingleChannelImageStack(np.random.rand(10, 256, 256))


def test_display_animation(test_image_stack):
    """Test that the animation is correctly displayed."""
    SingleChannelImageStackAnimator.view(test_image_stack)
