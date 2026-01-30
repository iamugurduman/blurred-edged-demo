from sdks.novavision.src.base.component import Component
from ..models.models import (
    SingleFilterExecutorRequest, 
    SingleFilterExecutorResponse, 
    SingleFilterExecutorOutputs, 
    OutputImageOne
)
import cv2
import numpy as np

class SingleFilter(Component):
    def run(self, request: SingleFilterExecutorRequest) -> SingleFilterExecutorResponse:
        # 1. Get Input Image
        input_data = request.inputs.inputImageOne.value
        
        # MOCK SDK BEHAVIOR: Assuming input_data has a 'data' array
        img = input_data.data if hasattr(input_data, 'data') else input_data

        # 2. Get Configuration
        config_wrapper = request.configs.configFilterType
        selected_option = config_wrapper.value
        
        processed_img = img.copy()

        # 3. Switch Logic based on Type
        if selected_option.name == "Blur":
            # Extract Blur Parameters
            k_size = selected_option.blurKernelSize.value
            sigma = selected_option.blurSigma.value
            
            # Kernel size must be odd
            if k_size % 2 == 0:
                k_size += 1
            
            # Apply Gaussian Blur
            processed_img = cv2.GaussianBlur(img, (k_size, k_size), sigma)
            
        elif selected_option.name == "Edge":
            # Extract Edge Parameters
            threshold = selected_option.edgeThreshold.value
            
            # Canny Edge Detection
            edges = cv2.Canny(img, threshold / 2, threshold)
            
            # Convert single channel edge to 3-channel for consistency (Blue Edges on Black)
            processed_img = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

        # 4. Prepare Output with Strict Instantiation
        output_image_one = OutputImageOne(value=processed_img)
        
        outputs_container = SingleFilterExecutorOutputs(
            outputImageOne=output_image_one
        )
        
        return SingleFilterExecutorResponse(outputs=outputs_container)
