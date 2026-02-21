from typing import Dict, Any
from .node import Node


class DataProcessingNode(Node):
    """
    Implementation of a node that processes data and provides feedback.

    Attributes:
        processing_interval (float): Time interval in seconds between processing cycles.
        data_processor (callable): Function to process the data.
    """

    def __init__(self, node_id: str, processing_interval: float = 1.0) -> None:
        super().__init__(node_id)
        self.processing_interval = processing_interval
        self.data_processor = self._default_data_processor
        self.log = logging.getLogger(f"AFDIN.Node.{node_id}.DataProcessor")

    def _default_data_processor(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Default data processing algorithm.

        Args:
            data (Dict[str, Any]): Input data to process.

        Returns:
            Dict[str, Any]: Processed data with an average value.
        """
        try:
            values = [d['value'] for d in data.get('data_points', [])]
            avg = sum(values) / len(values) if values else 0.0
            return {'timestamp': datetime.now().isoformat(), 'average_value': avg}
        except Exception as e:
            self.log.error(f"Data processing failed: {str(e)}")
            return {'error': str(e)}

    def start(self) -> None:
        """
        Starts the data processing loop.
        """
        self.active = True
        self.log.info("Starting data processing node.")
        try:
            while self.active:
                self.process_data({'data_points': [{'value': i} for i in range(5)]})
                import time
                time.sleep(self.processing_interval)
        except Exception as e:
            self.log.error(f"Node encountered an error: {str(e)}")
            self.stop()

    def stop(self) -> None:
        """
        Stops the data processing node gracefully.
        """
        self.active = False
        self.log.info("Stopping data processing node.")

    def process_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Processes incoming data and returns feedback.

        Args:
            data (Dict[str, Any]): Input data to be processed.

        Returns:
            Dict[str, Any]: Processed data/feedback.
        """
        self._log_event(f"Processing data: {data}")
        result = self.data_processor(data)
        self.send_feedback(result)
        return result

    def send_feedback(self, feedback: Dict[str, Any]) -> None:
        """
        Sends feedback to the knowledge base or dashboard.

        Args:
            feedback (Dict[str, Any]): Feedback data to be sent.
        """
        # Simulated integration with higher-level modules
        try:
            if 'knowledge_base' in globals():
                knowledge_base = globals()['knowledge_base']
                knowledge_base.update_with_feedback(feedback)
            elif 'dashboard' in globals():
                dashboard = globals()['dashboard']
                dashboard.log_activity(feedback)
        except Exception as e:
            self.log.error(f"Failed to send feedback: {str(e)}")