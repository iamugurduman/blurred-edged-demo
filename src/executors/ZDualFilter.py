"""
    Dual Filter Executor: Blend or Concatenate two images
"""
import os
import cv2
import sys
import numpy as np

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../'))

from sdks.novavision.src.media.image import Image
from sdks.novavision.src.base.component import Component
from sdks.novavision.src.helper.executor import Executor
from ..response import build_response
from ..models.PackageModel import PackageModel


class DualFilter(Component):
    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)
        self.request.model = PackageModel(**(self.request.data))
        # Retrieve config object
        self.config_wrapper = self.request.get_param("configMixType")
        self.image = self.request.get_param("inputImageOne")
        self.image_two = self.request.get_param("inputImageTwo")

    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}

    def apply_dual_filter(self, img1, img2):
        if img1 is None or img2 is None:
            return img1
            
        rows, cols, _ = img1.shape
        # Resize img2 to match img1 for simple blending/stacking
        img2_resized = cv2.resize(img2, (cols, rows))
        
        selected_option = self.config_wrapper.value
        result_img = None
        
        if selected_option.name == "Blend":
            alpha = selected_option.blendAlpha.value
            beta = 1.0 - alpha
            # Gamma is usually 0
            result_img = cv2.addWeighted(img1, alpha, img2_resized, beta, 0.0)
            
        elif selected_option.name == "Concat":
            axis = int(selected_option.concatAxis.value)
            if axis == 1:
                # Horizontal
                result_img = cv2.hconcat([img1, img2_resized])
            else:
                # Vertical
                result_img = cv2.vconcat([img1, img2_resized])
        
        return result_img

    def run(self):
        # 1. Get Frames from Redis
        img1 = Image.get_frame(img=self.image, redis_db=self.redis_db)
        img2 = Image.get_frame(img=self.image_two, redis_db=self.redis_db)
        
        # 2. Process
        if img1 is not None and img2 is not None:
             result_val = self.apply_dual_filter(img1.value, img2.value)
             img1.value = result_val
        
        # 3. Set Frame back to Redis (Updating Image One with the result)
        self.image = Image.set_frame(img=img1, package_uID=self.uID, redis_db=self.redis_db)
        
        # Note: image_two remains unchanged in Redis, but exists in context for build_response logic
        
        # 4. Build Response
        packageModel = build_response(context=self)
        return packageModel


if "__main__" == __name__:
    Executor(sys.argv[1]).run()
