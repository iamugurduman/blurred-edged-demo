from sdks.novavision.src.helper.package import PackageHelper
from src.novavision.novafilters.models.models import (
    PackageModel, 
    PackageConfigs, 
    ConfigExecutor, 
    SingleFilterExecutor, 
    SingleFilterResponse, 
    SingleFilterOutputs, 
    OutputImageOne,
   
    DualFilterExecutor,
    DualFilterResponse,
    DualFilterOutputs,
    OutputImageTwo
)


def build_response_single(context):
    output_image = OutputImageOne(value=context.image)
    outputs_container = SingleFilterOutputs(outputImageOne=output_image)
    executor_response = SingleFilterResponse(outputs=outputs_container)
    single_filter_executor = SingleFilterExecutor(value=executor_response)
    config_executor = ConfigExecutor(value=single_filter_executor)
    package_configs = PackageConfigs(executor=config_executor)
    package = PackageHelper(packageModel=PackageModel, packageConfigs=package_configs)
    package_model = package.build_model(context)
    return package_model


def build_response_dual(context):
    outputImage = OutputImageOne(value=context.image)

    img2_val = getattr(context, 'image_two', None)
    outputImage2 = OutputImageTwo(value=img2_val if img2_val is not None else context.image) 
    
    dualOutputs = DualFilterOutputs(outputImageOne=outputImage, outputImageTwo=outputImage2)
    dualResponse = DualFilterResponse(outputs=dualOutputs)
    dualExecutor = DualFilterExecutor(value=dualResponse)
    
    executor = ConfigExecutor(value=dualExecutor)
    package_configs = PackageConfigs(executor=executor)
    package = PackageHelper(packageModel=PackageModel, packageConfigs=package_configs)
    package_model = package.build_model(context)
    return package_model


def build_response(context):
    if hasattr(context, 'image_two') and context.image_two is not None:
        return build_response_dual(context)
    elif hasattr(context, 'executor') and 'Dual' in str(context.executor):
        return build_response_dual(context)
    else:
        return build_response_single(context)
