"""
    Single Filter Executor: Blur or Edge Detection
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


class BlurredEdged(Component):
    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)
        self.request.model = PackageModel(**(self.request.data))
        
        self.config_wrapper = self.request.get_param("configFilterType")
        self.image = self.request.get_param("inputImageOne")

    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}

    def apply_filter(self, img):
        if img is None:
            return None
            
        selected_option = self.config_wrapper.value
        
        if selected_option.name == "Blur":
            k_size = selected_option.blurKernelSize.value
            sigma = selected_option.blurSigma.value
            # Ensure odd kernel size
            k_size = int(k_size)
            if k_size % 2 == 0:
                k_size += 1
            return cv2.GaussianBlur(img, (k_size, k_size), sigma)

        elif selected_option.name == "Edge":
            threshold = selected_option.edgeThreshold.value
            edges = cv2.Canny(img, threshold / 2, threshold)
            return cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

        else:
            return img

    def run(self):
        #Get Frame from Redis
        img = Image.get_frame(img=self.image, redis_db=self.redis_db)
        
        #Process
        img.value = self.apply_filter(img.value)
        
        #Set Frame back to Redis
        self.image = Image.set_frame(img=img, package_uID=self.uID, redis_db=self.redis_db)
        
        #Build Response
        packageModel = build_response(context=self)
        return packageModel


if "__main__" == __name__:
    Executor(sys.argv[1]).run()
