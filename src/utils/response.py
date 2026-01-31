from sdks.novavision.src.helper.package import PackageHelper
from ..models.PackageModel import (
    PackageModel, 
    PackageConfigs, 
    ConfigExecutor, 
    BlurredEdgedExecutor, 
    BlurredEdgedResponse, 
    BlurredEdgedOutputs, 
    OutputImageOne,
   
    BlendedConcatExecutor,
    BlendedConcatExecutorResponse,
    BlendedConcatOutputs,
    OutputImageTwo
)


def build_response_blurrededged(context):
    output_image = OutputImageOne(value=context.image)
   
    outputs_container = BlurredEdgedOutputs(outputImage=output_image) 
    executor_response = BlurredEdgedResponse(outputs=outputs_container)
    single_filter_executor = BlurredEdgedExecutor(value=executor_response)
    config_executor = ConfigExecutor(value=single_filter_executor)
    package_configs = PackageConfigs(executor=config_executor)
    package = PackageHelper(packageModel=PackageModel, packageConfigs=package_configs)
    package_model = package.build_model(context)
    return package_model


def build_response_blendedconcat(context):
    outputImage = OutputImageOne(value=context.image)

    img2_val = getattr(context, 'image_two', None)
    outputImage2 = OutputImageTwo(value=img2_val if img2_val is not None else context.image) 
    
    dualOutputs = BlendedConcatOutputs(outputImageOne=outputImage, outputImageTwo=outputImage2)
    dualResponse = BlendedConcatExecutorResponse(outputs=dualOutputs)
    dualExecutor = BlendedConcatExecutor(value=dualResponse)
    
    executor = ConfigExecutor(value=dualExecutor)
    package_configs = PackageConfigs(executor=executor)
    package = PackageHelper(packageModel=PackageModel, packageConfigs=package_configs)
    package_model = package.build_model(context)
    return package_model


def build_response(context):
    if hasattr(context, 'image_two') and context.image_two is not None:
        return build_response_blendedconcat(context)
    elif hasattr(context, 'executor') and 'Merged' in str(type(context)) or 'Blended' in str(type(context)): # Check class name loosely
         return build_response_blendedconcat(context)
    else:
        return build_response_blurrededged(context)
