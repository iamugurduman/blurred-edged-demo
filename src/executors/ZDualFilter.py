from sdks.novavision.src.base.component import Component
from ..models.PackageModel import (
    DualFilterExecutorRequest, 
    DualFilterExecutorResponse, 
    DualFilterExecutorOutputs, 
    OutputImageOne, 
    OutputImageTwo
)
import cv2
import numpy as np


class DualFilter(Component):
    def run(self, request: DualFilterExecutorRequest) -> DualFilterExecutorResponse:
        # 1. Get Inputs
        img1 = request.inputs.inputImageOne.value
        img2 = request.inputs.inputImageTwo.value

        img1_data = img1.data if hasattr(img1, 'data') else img1
        img2_data = img2.data if hasattr(img2, 'data') else img2

        rows, cols, _ = img1_data.shape
        img2_resized = cv2.resize(img2_data, (cols, rows))

        # 2. Get Configuration
        config_wrapper = request.configs.configMixType
        selected_option = config_wrapper.value

        result_img = None
        mask_img = np.zeros_like(img1_data)  # Placeholder mask

        # 3. Switch Logic
        if selected_option.name == "Blend":
            # Access Blend Parameters
            alpha = selected_option.blendAlpha.value
            gamma = 0  # Simple gamma, could be param

            beta = 1.0 - alpha
            result_img = cv2.addWeighted(img1_data, alpha, img2_resized, beta, gamma)

            mask_img[:] = int(alpha * 255)

        elif selected_option.name == "Concat":
            # Access Concat Parameters
            axis = selected_option.concatAxis.value  # 0=Vertical, 1=Horizontal

            if axis == 1:
                # Horizontal
                result_img = cv2.hconcat([img1_data, img2_resized])
            else:
                # Vertical
                result_img = cv2.vconcat([img1_data, img2_resized])

            # Mask indicates the join line (simple line in middle)
            if axis == 1:
                cv2.line(mask_img, (cols, 0), (cols, rows), (255, 255, 255), 5)
            else:
                cv2.line(mask_img, (0, rows), (cols, rows), (255, 255, 255), 5)

        # 4. Prepare Outputs
        output_mixed = OutputImageOne(value=result_img)
        output_mask = OutputImageTwo(value=mask_img)

        return DualFilterExecutorResponse(outputs={
            "outputImageOne": output_mixed,
            "outputImageTwo": output_mask
        })
