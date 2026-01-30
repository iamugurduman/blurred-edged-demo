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
        # Ayarları al
        self.config_wrapper = self.request.get_param("configMixType")
        self.image = self.request.get_param("inputImageOne")
        self.image_two = self.request.get_param("inputImageTwo")

    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}

    def apply_dual_filter(self, img1, img2):
        # ... İşlem mantığı (Blend/Concat) ...
        if img1 is None or img2 is None:
            return img1
            
        rows, cols, _ = img1.shape
        img2_resized = cv2.resize(img2, (cols, rows))
        
        selected_option = self.config_wrapper.value
        result_img = None
        
        if selected_option.name == "Blend":
            alpha = selected_option.blendAlpha.value
            beta = 1.0 - alpha
            result_img = cv2.addWeighted(img1, alpha, img2_resized, beta, 0.0)
            
        elif selected_option.name == "Concat":
            axis = selected_option.concatAxis.value
            if axis == 1:
                result_img = cv2.hconcat([img1, img2_resized])
            else:
                result_img = cv2.vconcat([img1, img2_resized])
        
        return result_img

    def run(self):
        # 1. Redis'ten resimleri çek (YENİ YAPI)
        img1 = Image.get_frame(img=self.image, redis_db=self.redis_db)
        img2 = Image.get_frame(img=self.image_two, redis_db=self.redis_db)
        
        # 2. İşle
        if img1 is not None and img2 is not None:
             result_val = self.apply_dual_filter(img1.value, img2.value)
             img1.value = result_val
        
        # 3. Sonucu Redis'e yaz
        self.image = Image.set_frame(img=img1, package_uID=self.uID, redis_db=self.redis_db)
        
        # 4. Response oluştur
        packageModel = build_response(context=self)
        return packageModel


if "__main__" == __name__:
    Executor(sys.argv[1]).run()
