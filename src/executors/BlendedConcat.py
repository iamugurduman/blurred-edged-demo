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
       
        self.image = self.request.get_param("inputImageOne")
        self.image_two = self.request.get_param("inputImageTwo")
        self.mixType = self.request.get_param("configMixType")  # Returns "Blend" or "Concat"
        
        # For storing results
        self.image_result_one = None
        self.image_result_two = None
        
        if self.mixType == "Blend":
            self.blendAlpha = self.request.get_param("BlendAlpha")

    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}

    def apply_dual_filter(self, img1, img2):
        if img1 is None or img2 is None:
            return img1, img1
        
        # Resize img2 to match img1
        img2_resized = cv2.resize(img2, (img1.shape[1], img1.shape[0]))
        
        if self.mixType == "Blend":
            alpha = float(self.blendAlpha)
            result = cv2.addWeighted(img1, alpha, img2_resized, 1.0 - alpha, 0)
            return result, result  # Same result for both outputs
            
        elif self.mixType == "Concat":
            horizontal = cv2.hconcat([img1, img2_resized])
            vertical = cv2.vconcat([img1, img2_resized])
            return horizontal, vertical  # Different results for each output
        
        return img1, img1

    def run(self):
        #Get Frames from Redis
        img1 = Image.get_frame(img=self.image, redis_db=self.redis_db)
        img2 = Image.get_frame(img=self.image_two, redis_db=self.redis_db)
        
        #Process
        if img1 is not None and img2 is not None:
            result_one, result_two = self.apply_dual_filter(img1.value, img2.value)
            img1.value = result_one
            img2.value = result_two
        
        #Set Frames back to Redis
        self.image_result_one = Image.set_frame(img=img1, package_uID=self.uID, redis_db=self.redis_db)
        self.image_result_two = Image.set_frame(img=img2, package_uID=self.uID, redis_db=self.redis_db)
        
        #Build Response
        packageModel = build_response(context=self)
        return packageModel


if "__main__" == __name__:
    Executor(sys.argv[1]).run()
