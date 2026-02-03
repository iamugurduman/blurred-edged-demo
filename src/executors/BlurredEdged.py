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
from components.BlurredEdgedTest.src.utils.response import build_response
from components.BlurredEdgedTest.src.models.PackageModel import PackageModel


class BlurredEdged(Component):
    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)
        self.request.model = PackageModel(**(self.request.data))
        
        self.image = self.request.get_param("inputImageOne")
        self.filterType = self.request.get_param("configFilterType")  # Returns "Blur" or "Edge"
        
   
        if self.filterType == "Blur":
            self.blurKernelSize = self.request.get_param("BlurKernelSize")
            self.blurSigma = self.request.get_param("BlurSigma")
        elif self.filterType == "Edge":
            self.edgeThreshold = self.request.get_param("EdgeThreshold")

    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}

    def apply_filter(self, img):
        if img is None:
            return None
        
        if self.filterType == "Blur":
            k_size = int(self.blurKernelSize)
            sigma = float(self.blurSigma)
            # Ensure odd kernel size
            if k_size % 2 == 0:
                k_size += 1
            return cv2.GaussianBlur(img, (k_size, k_size), sigma)

        elif self.filterType == "Edge":
            threshold = int(self.edgeThreshold)
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
