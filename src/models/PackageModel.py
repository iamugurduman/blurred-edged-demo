from pydantic import Field, validator
from typing import List, Optional, Union, Literal
from sdks.novavision.src.base.model import Package, Image, Inputs, Configs, Outputs, Response, Request, Output, Input, \
    Config


# Inputs
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
        title = "Image Input 1"


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
        title = "Image Input 2"


# Outputs
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
        title = "Output Image 1"


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


# --- Single Filter Configuration ---

class BlurKernelSize(Config):
    name: Literal["BlurKernelSize"] = "BlurKernelSize"
    value: int = Field(default=5)
    type: Literal["integer"] = "integer"
    field: Literal["textInput"] = "textInput"

    class Config:
        title = "Kernel Size"


class BlurSigma(Config):
    name: Literal["BlurSigma"] = "BlurSigma"
    value: float = Field(default=0.0)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"

    class Config:
        title = "Sigma X"


class OptionBlur(Config):
    blurKernelSize: BlurKernelSize
    blurSigma: BlurSigma
    name: Literal["Blur"] = "Blur"
    value: Literal["Blur"] = "Blur"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Gaussian Blur"


class EdgeThreshold(Config):
    name: Literal["EdgeThreshold"] = "EdgeThreshold"
    value: int = Field(default=100)
    type: Literal["integer"] = "integer"
    field: Literal["textInput"] = "textInput"

    class Config:
        title = "Edge Threshold"


class OptionEdge(Config):
    edgeThreshold: EdgeThreshold
    name: Literal["Edge"] = "Edge"
    value: Literal["Edge"] = "Edge"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Canny Edge"


class ConfigFilterType(Config):
    """
    Select whether to Blur or detect Edges.
    """
    name: Literal["configFilterType"] = "configFilterType"
    value: Union[OptionBlur, OptionEdge]
    type: Literal["object"] = "object"
    # Using dependentDropdownlist to show sub-options based on selection
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"

    class Config:
        title = "Operation"
        json_schema_extra = {
            "shortDescription": "Filter Mode"
        }


# --- Dual Filter Configuration ---

class BlendAlpha(Config):
    """Mixing factor (0.0 - 1.0)"""
    name: Literal["BlendAlpha"] = "BlendAlpha"
    value: float = Field(default=0.5)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"

    class Config:
        title = "Alpha"


class OptionBlend(Config):
    blendAlpha: BlendAlpha
    name: Literal["Blend"] = "Blend"
    value: Literal["Blend"] = "Blend"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Blend Images"


class ConcatAxis(Config):
    """0 for Vertical, 1 for Horizontal"""
    name: Literal["ConcatAxis"] = "ConcatAxis"
    value: int = Field(default=1)
    type: Literal["integer"] = "integer"
    field: Literal["textInput"] = "textInput"

    class Config:
        title = "Axis"


class OptionConcat(Config):
    concatAxis: ConcatAxis
    name: Literal["Concat"] = "Concat"
    value: Literal["Concat"] = "Concat"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Concatenate"


class ConfigMixType(Config):
    """
    Select how to combine the two images.
    """
    name: Literal["configMixType"] = "configMixType"
    value: Union[OptionBlend, OptionConcat]
    type: Literal["object"] = "object"
    # Using dependentDropdownlist to show sub-options based on selection
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"

    class Config:
        title = "Mix Mode"
        json_schema_extra = {
            "shortDescription": "Mixing Logic"
        }


# --- Inputs Groups ---

class SingleFilterExecutorInputs(Inputs):
    inputImageOne: InputImageOne


class DualFilterExecutorInputs(Inputs):
    inputImageOne: InputImageOne
    inputImageTwo: InputImageTwo


# --- Configs Groups ---

class SingleFilterExecutorConfigs(Configs):
    configFilterType: ConfigFilterType


class DualFilterExecutorConfigs(Configs):
    configMixType: ConfigMixType


# --- Outputs Groups ---

class SingleFilterExecutorOutputs(Outputs):
    outputImageOne: OutputImageOne


class DualFilterExecutorOutputs(Outputs):
    outputImageOne: OutputImageOne
    outputImageTwo: OutputImageTwo


# --- Requests ---

class SingleFilterExecutorRequest(Request):
    inputs: Optional[SingleFilterExecutorInputs]
    configs: SingleFilterExecutorConfigs

    class Config:
        json_schema_extra = {
            "target": "configs"
        }


class DualFilterExecutorRequest(Request):
    inputs: Optional[DualFilterExecutorInputs]
    configs: DualFilterExecutorConfigs

    class Config:
        json_schema_extra = {
            "target": "configs"
        }


# --- Responses ---

class SingleFilterExecutorResponse(Response):
    outputs: SingleFilterExecutorOutputs


class DualFilterExecutorResponse(Response):
    outputs: DualFilterExecutorOutputs


# --- Executors ---

class SingleFilterExecutor(Config):
    name: Literal["SingleFilterExecutor"] = "SingleFilterExecutor"
    value: Union[SingleFilterExecutorRequest, SingleFilterExecutorResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "Single Filter Executor"
        json_schema_extra = {
            "target": {
                "value": 0 # Points to SingleFilter.py (First alphabetically)
            }
        }


class DualFilterExecutor(Config):
    name: Literal["DualFilterExecutor"] = "DualFilterExecutor"
    value: Union[DualFilterExecutorRequest, DualFilterExecutorResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "Dual Filter Executor"
        json_schema_extra = {
            "target": {
                "value": 1 # Points to ZDualFilter.py (Second alphabetically)
            }
        }


# --- Main Package ---

class ConfigExecutor(Config):
    name: Literal["ConfigExecutor"] = "ConfigExecutor"
    value: Union[SingleFilterExecutor, DualFilterExecutor]
    type: Literal["executor"] = "executor"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"
    restart: Literal[True] = True

    class Config:
        title = "Task"


class PackageConfigs(Configs):
    executor: ConfigExecutor


class PackageModel(Package):
    name: Literal["BlurredEdgedDemo"] = "BlurredEdgedDemo"
    configs: PackageConfigs
    type: Literal["component"] = "component"
