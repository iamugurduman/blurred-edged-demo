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
from components.BlurredEdgedTest.src.utils.response import build_response
from components.BlurredEdgedTest.src.models.PackageModel import PackageModel


class BlendedConcat(Component):
    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)
        self.request.model = PackageModel(**(self.request.data))
       
        self.mixType = self.request.get_param("configMixType")
        # Use defaults if nested params are not accessible via get_param
        self.blendAlpha = self.request.get_param("blendAlpha") or 0.5
        self.concatAxis = self.request.get_param("concatAxis") or 1
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
        
        result_img = None
        
        if self.mixType == "Blend":
            alpha = float(self.blendAlpha)
            beta = 1.0 - alpha
            # Gamma is usually 0
            result_img = cv2.addWeighted(img1, alpha, img2_resized, beta, 0.0)
            
        elif self.mixType == "Concat":
            axis = int(self.concatAxis)
            if axis == 1:
                # Horizontal
                result_img = cv2.hconcat([img1, img2_resized])
            else:
                # Vertical
                result_img = cv2.vconcat([img1, img2_resized])
        
        return result_img

    def run(self):
        #Get Frames from Redis
        img1 = Image.get_frame(img=self.image, redis_db=self.redis_db)
        img2 = Image.get_frame(img=self.image_two, redis_db=self.redis_db)
        
        #Process
        if img1 is not None and img2 is not None:
             result_val = self.apply_dual_filter(img1.value, img2.value)
             img1.value = result_val
        
        #Set Frame back to Redis (Updating Image One with the result)
        self.image = Image.set_frame(img=img1, package_uID=self.uID, redis_db=self.redis_db)
        
        
        #Build Response
        packageModel = build_response(context=self)
        return packageModel


if "__main__" == __name__:
    Executor(sys.argv[1]).run()
