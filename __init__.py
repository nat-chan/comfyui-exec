import re
from abc import ABCMeta

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
                "CATEGORY": "Eval",
            },
        )
        NODE_CLASS_MAPPINGS[name] = new_class
        NODE_DISPLAY_NAME_MAPPINGS[name] = format_class_name(name) + "💻"
        return new_class


class AnyType(str):
    def __ne__(self, __value: object) -> bool:
        return False
any = AnyType("*")

N = 5

class EvalNode(metaclass=CustomNodeMeta):
    OUTPUT_NODE = True
    RETURN_TYPES = tuple([any]*N)
    RETURN_NAMES = tuple([f"b{i}" for i in range(N)])
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required" : {
                "code": ("STRING", {"multiline": True, "default": ""}),
                "seed": ("INT:seed", {}),
            },
            "optional" : {
                f"a{i}" : ("*", {})
                for i in range(N)
            }
        }
    def run(
        self,
        code: str,
        seed: int,
        **kwargs,
    ) -> tuple[str]:
        kwargs.update({f"b{i}": None for i in range(N)})
        exec(code, None, kwargs)
        return tuple(kwargs.get(f"b{i}", None) for i in range(N))


# --- node }}}