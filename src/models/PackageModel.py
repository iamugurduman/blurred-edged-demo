from pydantic import Field, validator
from typing import List, Optional, Union, Literal
from sdks.novavision.src.base.model import Package, Image, Inputs, Configs, Outputs, Response, Request, Output, Input, Config


#Inputs

class InputImageOne(Input):
    name: Literal["inputImageOne"] = "inputImageOne"
    value: Union[List[Image], Image]
    type: str = "object"

    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, value, values):
        value = values.get('value')
        if isinstance(value, Image):
            return "object"
        elif isinstance(value, list):
            return "list"

    class Config:
        title = "Image"


class InputImageTwo(Input):
    name: Literal["inputImageTwo"] = "inputImageTwo"
    value: Union[List[Image], Image]
    type: str = "object"

    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, value, values):
        value = values.get('value')
        if isinstance(value, Image):
            return "object"
        elif isinstance(value, list):
            return "list"

    class Config:
        title = "Image"


#Outputs

class OutputImageOne(Output):
    name: Literal["outputImageOne"] = "outputImageOne"
    value: Union[List[Image], Image]
    type: str = "object"

    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, value, values):
        value = values.get('value')
        if isinstance(value, Image):
            return "object"
        elif isinstance(value, list):
            return "list"

    class Config:
        title = "Output Image"


class OutputImageTwo(Output):
    name: Literal["outputImageTwo"] = "outputImageTwo"
    value: Union[List[Image], Image]
    type: str = "object"

    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, value, values):
        value = values.get('value')
        if isinstance(value, Image):
            return "object"
        elif isinstance(value, list):
            return "list"

    class Config:
        title = "Output Image 2"


# ========================================


#configs
class BlurKernelSize(Config):
    """Kernel size for Gaussian blur (must be odd)"""
    name: Literal["BlurKernelSize"] = "BlurKernelSize"
    value: int = Field(default=5)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"

    class Config:
        title = "Kernel Size"
        json_schema_extra = {
            "shortDescription": "Blur Kernel"
        }


class BlurSigma(Config):
    """Sigma X for Gaussian blur"""
    name: Literal["BlurSigma"] = "BlurSigma"
    value: float = Field(default=0.0)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"

    class Config:
        title = "Sigma X"
        json_schema_extra = {
            "shortDescription": "Blur Sigma"
        }

class EdgeThreshold(Config):
    """Threshold for Canny edge detection"""
    name: Literal["EdgeThreshold"] = "EdgeThreshold"
    value: int = Field(default=100)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"

    class Config:
        title = "Threshold"
        json_schema_extra = {
            "shortDescription": "Edge Threshold"
        }


class OptionBlur(Config):
    blurKernelSize: BlurKernelSize
    blurSigma: BlurSigma
    name: Literal["Blur"] = "Blur"
    value: Literal["Blur"] = "Blur"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Gaussian Blur"


class OptionEdge(Config):
    edgeThreshold: EdgeThreshold
    name: Literal["Edge"] = "Edge"
    value: Literal["Edge"] = "Edge"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Canny Edge"


class BlendAlpha(Config):
    """Alpha value for blending (0.0 to 1.0)"""
    name: Literal["BlendAlpha"] = "BlendAlpha"
    value: float = Field(default=0.5)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"

    class Config:
        title = "Alpha"
        json_schema_extra = {
            "shortDescription": "Blend Alpha"
        }



class ConcatAxis(Config):
    """Axis for concatenation: 0=Vertical, 1=Horizontal"""
    name: Literal["ConcatAxis"] = "ConcatAxis"
    value: int = Field(default=1)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"

    class Config:
        title = "Axis"
        json_schema_extra = {
            "shortDescription": "Concat Axis"
        }
class OptionBlend(Config):
    blendAlpha: BlendAlpha
    name: Literal["Blend"] = "Blend"
    value: Literal["Blend"] = "Blend"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Blend Images"



class OptionConcat(Config):
    concatAxis: ConcatAxis
    name: Literal["Concat"] = "Concat"
    value: Literal["Concat"] = "Concat"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Concatenate"


class BlurredEdged(Config):
    """Select filter operation: Blur or Edge detection"""
    name: Literal["configFilterType"] = "configFilterType"
    value: Union[OptionBlur, OptionEdge]
    type: Literal["object"] = "object"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"
    restart: Literal[True] = True

    class Config:
        title = "Filter Type"
        json_schema_extra = {
            "shortDescription": "Filter Operation"
        }



class BlendedConcat(Config):
    """Select how to combine two images"""
    name: Literal["configMixType"] = "configMixType"
    value: Union[OptionBlend, OptionConcat]
    type: Literal["object"] = "object"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"
    restart: Literal[True] = True

    class Config:
        title = "Combine Mode"
        json_schema_extra = {
            "shortDescription": "Combine Method"
        }



#Inputs
class BlurredEdgedExecutorInputs(Inputs):
    inputImageOne: InputImageOne


class BlendedConcatExecutorInputs(Inputs):
    inputImageOne: InputImageOne
    inputImageTwo: InputImageTwo



#Configs
class BlurredEdgedConfigs(Configs):
    configFilterType: BlurredEdged

class BlendedConcatConfigs(Configs):
    configMixType: BlendedConcat

#Outputs
class BlurredEdgedOutputs(Outputs):
    outputImageOne: OutputImageOne


class BlendedConcatOutputs(Outputs):
    outputImageOne: OutputImageOne
    outputImageTwo: OutputImageTwo

#Requests
class BlurredEdgedExecutorRequest(Request):
    inputs: Optional[BlurredEdgedExecutorInputs]
    configs: BlurredEdgedConfigs

    class Config:
        json_schema_extra = {
            "target": "configs"
        }

class BlendedConcatExecutorRequest(Request):
    inputs: Optional[BlendedConcatExecutorInputs]
    configs: BlendedConcatConfigs

    class Config:
        json_schema_extra = {
            "target": "configs"
        }

#Responses
class BlurredEdgedResponse(Response):
    outputs: BlurredEdgedOutputs

class BlendedConcatExecutorResponse(Response):
    outputs: BlendedConcatOutputs


#Executors
class BlurredEdgedExecutor(Config):
    name: Literal["BlurredEdged"] = "BlurredEdged"
    value: Union[BlurredEdgedExecutorRequest, BlurredEdgedResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "Blurred Edged"
        json_schema_extra = {
            "target": {
                "value": 0
            }
        }



class BlendedConcatExecutor(Config):
    name: Literal["BlendedConcat"] = "BlendedConcat"
    value: Union[BlendedConcatExecutorRequest, BlendedConcatExecutorResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "Blended Concat"
        json_schema_extra = {
            "target": {
                "value": 0
            }
        }


#Main Package

class ConfigExecutor(Config):

    name: Literal["ConfigExecutor"] = "ConfigExecutor"
    value: Union[BlurredEdgedExecutor, BlendedConcatExecutor]
    type: Literal["executor"] = "executor"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"
    restart: Literal[True] = True

    class Config:
        title = "Task"



class PackageConfigs(Configs):
    executor: ConfigExecutor


class PackageModel(Package):
    name: Literal["BlurredEdgedTest"] = "BlurredEdgedTest"
    configs: PackageConfigs
    type: Literal["component"] = "component"
