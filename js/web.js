import { app } from "../../scripts/app.js";

app.registerExtension({
  name: "comfyui-exec",
  async beforeRegisterNodeDef(nodeType, nodeData, app) {
    if (
        nodeData.name === "ExecCodeRunner" || 
        nodeData.name === "ExecResultRetriever" ||
        nodeData.name === "ExecCodeReader"
      ) {
      const origOnNodeCreated = nodeType.prototype.onNodeCreated;
      nodeType.prototype.onNodeCreated = function () {
        const r = origOnNodeCreated ? origOnNodeCreated.apply(this) : undefined;
        for (const w of this.widgets) {
          if (w.name === "seed") {
            w.type = "converted-widget";
            if (!w.linkedWidgets) continue;
            for (const lw of w.linkedWidgets) {
              lw.type = "converted-widget";
            }
          }
        }
        return r;
      }
      nodeType.prototype.color = LGraphCanvas.node_colors.cyan.color;
      nodeType.prototype.bgcolor = LGraphCanvas.node_colors.cyan.bgcolor;
    }
    if (nodeData.name === "ExecCodeRunner") {
      nodeType.prototype.onConnectionsChange = function (type, index, connected, linkInfo, ioSlot) {
        if (!linkInfo) return;
        if (type !== 1) return;
        if (connected) {
          const cnt = this.inputs.filter(input => input.link === null).length;
          if (cnt < 1) {
            this.addInput("abcdefghijklmnopqrstuvwxyz"[this.inputs.length-1], "*");
          }
        } else {
          const cnt = this.inputs.filter(input => input.link === null).length;
          if (cnt > 1) {
            this.removeInput(this.inputs.length-1);
          }
        }
      }
    }
  },
});