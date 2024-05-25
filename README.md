# comfyui-exec⚠️

![image](https://github.com/nat-chan/comfyui-exec/assets/18454066/3daed333-12a3-4c7f-a359-a1918005f877)

> [!WARNING]
> This custom node has the danger of allowing users to execute arbitrary code, e.g. `rm -rf /`, on the server. It should not be used in a production environment.

This custom node executes the Python code entered in the text field.
It can have any number of outputs for any number of inputs.
There are no restrictions on input and output types.

## Installation

```
cd ComfyUI/custom_nodes
git clone https://github.com/nat-chan/comfyui-exec
```

## Nodes

### Exec Code Runner 

**input**

- `CODE`
  - Python code to be executed. It must be of type STRING and is intended to be connected to a `Text Multiline` node, etc.

- `a`,`b`…`z`
  - Connecting any node you wish to the `a` node will cause the next `b` node to appear, and so on, allowing any number of inputs. The input flowing to each node is assigned to the alphabet of the node's label.

**output**

- `RESULT`
  - It must be connected to the `Exec Result Retriever` node.

### Exec Result Retriever 

**input**

- `RESULT`
  - - It must be connected to the `Exec Code Runner` node.

- `variable_name`
  - Describe the process in the CODE and fill in the name of the variable you want to retrieve. It can be connected to any type of node.
