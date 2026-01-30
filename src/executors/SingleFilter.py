from sdks.novavision.src.base.component import Component
from ..models.PackageModel import (
    SingleFilterExecutorRequest, 
    SingleFilterExecutorResponse, 
    SingleFilterExecutorOutputs, 
    OutputImageOne
)
import cv2
import numpy as np

class SingleFilter(Component):
    def run(self, request: SingleFilterExecutorRequest) -> SingleFilterExecutorResponse:
        #Get Input Image
        input_data = request.inputs.inputImageOne.value
        
        
        img = input_data.data if hasattr(input_data, 'data') else input_data

        #Get Configuration
        config_wrapper = request.configs.configFilterType
        selected_option = config_wrapper.value

        
        processed_img = img.copy()

        
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
            
        
            processed_img = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

    
        output_image_one = OutputImageOne(value=processed_img)
        
        outputs_container = SingleFilterExecutorOutputs(
            outputImageOne=output_image_one
        )
        
        return SingleFilterExecutorResponse(outputs=outputs_container)
