from typing import Dict, Any
from .node_impl import DataProcessingNode


def main() -> None:
    """
    Example usage of the DataProcessingNode.
    """
    # Initialize logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    node_id = "DPN_001"
    processing_interval = 2.0

    try:
        node = DataProcessingNode(node_id, processing_interval)
        node.start()
    except Exception as e:
        print(f"Failed to initialize or start node: {str(e)}")