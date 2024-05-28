import re
from abc import ABCMeta
from pathlib import Path

NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}
WEB_DIRECTORY = "./js"
__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS", "WEB_DIRECTORY"]

"""
https://zenn.dev/4kk11/articles/4e36fc68293bd2
https://github.com/chrisgoringe/Comfy-Custom-Node-How-To/wiki/api
"""


# {{{ node ---
def format_class_name(class_name: str) -> str:
    """先頭以外の大文字の前に空白を挟む"""
    formatted_name = re.sub(r"(?<!^)(?=[A-Z])", " ", class_name)
    return formatted_name


class CustomNodeMeta(ABCMeta):
    def __new__(
        cls,
        name: str,
        bases: list,
        attrs: dict,
    ) -> "CustomNodeMeta":
        global NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS
        new_class = super().__new__(
            cls,
            name,
            bases,
            attrs
            | {
                "FUNCTION": "run",
                "CATEGORY": "Exec" + "⚠️",
            },
        )
        NODE_CLASS_MAPPINGS[name] = new_class
        NODE_DISPLAY_NAME_MAPPINGS[name] = format_class_name(name) + "⚠️"
        return new_class


class AnyType(str):
    def __ne__(self, __value: object) -> bool:
        return False
any = AnyType("*")

class ExecCodeRunner(metaclass=CustomNodeMeta):
    OUTPUT_NODE = True
    RETURN_TYPES = ("RESULT",)
    RETURN_NAMES = ("RESULT",)
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required" : {
                "CODE": ("STRING", {"forceInput": True}),
                "seed": ("INT:seed", {}),
            },
        }
    def run(self, CODE: str, seed: int, **kwargs) -> tuple[dict]:
        exec(CODE, {}, kwargs)
        return (kwargs,)

class ExecResultRetriever(metaclass=CustomNodeMeta):
    OUTPUT_NODE = True
    RETURN_TYPES = (any,)
    RETURN_NAMES = ("*",)
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required" : {
                "RESULT" : ("RESULT", {"forceInput": True}),
                "variable_name": ("STRING", {"multiline": False, "default": "z"}),
                "seed": ("INT:seed", {}),
            }
        }
    def run(self, RESULT: dict, variable_name: str, seed: int) -> tuple:
        return (RESULT[variable_name],)

class ExecCodeReader(metaclass=CustomNodeMeta):
    OUTPUT_NODE = True
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("CODE",)
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required" : {
                "file_path": ("STRING", {"multiline": False, "default": "~/code.py"}),
                "seed": ("INT:seed", {}),
            }
        }
    def run(self, file_path: str, seed: int) -> tuple:
        p = Path(file_path).expanduser()
        txt = p.read_text()
        return (txt,)


# --- node }}}