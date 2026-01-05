import contextvars
import logging
import sys

# Creating a variable which can be provides
nodeId = contextvars.ContextVar("node_id", default="0")


def setNodeId(node_id: str) -> None:
    nodeId.set(node_id)


def getNodeId() -> str:
    return nodeId.get()


class NodeIdFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        record.node_id = getNodeId()
        return True


logger = logging.getLogger("Bitcoin")
logger.setLevel(logging.INFO)

# CONSOLE HANDLER
# NOTE: This particular handler handles the logging for showing to the output
# You can add more handlers and write it to file if  you need
console = logging.StreamHandler(sys.stdout)
console.setLevel(logging.INFO)

# FORMAT
fmt = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - Node=%(node_id)s - %(message)s"
)
logger.addFilter(NodeIdFilter())
console.setFormatter(fmt)
logger.addHandler(console)
