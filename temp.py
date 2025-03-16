import os
import logging

CONFIG_FOLDER = os.getenv("CONFIG_FOLDER", "./config") 
INPUT_FOLDER = os.getenv("INPUT_FOLDER", "./input")
OUTPUT_FOLDER = os.getenv("OUTPUT_FOLDER", "./output")
LOGGING_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
LOGGING_LEVEL = getattr(logging, LOGGING_LEVEL, logging.INFO)

# Reset logging handlers
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

# Configure logging
logging.basicConfig(
    level=LOGGING_LEVEL,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

logger = logging.getLogger(__name__)

# 🔹 Suppress noisy third-party loggers
# logging.getLogger("httpcore").setLevel(logging.WARNING)  
# logging.getLogger("httpx").setLevel(logging.WARNING)  
# logging.getLogger("stage0_py_utils.evaluator").setLevel(LOGGING_LEVEL)

logger.info("Logging successfully configured!")

# Import utils
from stage0_py_utils import ConversationServices, Evaluator

class Runbook:
    """Processor class for testing a grading prompt using a grading key"""
    def __init__(self):
        logger.info(f"Runbook initialized with Config: {CONFIG_FOLDER}, Input: {INPUT_FOLDER}, Output: {OUTPUT_FOLDER}")

    def run(self):
        logger.info("Running the Runbook...")
        # Your processing logic here

def main():
    logger.info("============================ Grader Pipeline Starting ==============================")
    logger.info(f"Initialized, Input: {INPUT_FOLDER}, Output: {OUTPUT_FOLDER}, Config: {CONFIG_FOLDER}, Logging Level {LOGGING_LEVEL}")
    
    try:
        runner = Runbook()
        runner.run()
    except Exception as e:
        logger.error(f"Error Reported {str(e)}", exc_info=True)

    logger.info("===================== Grader Pipeline Completed Successfully =======================")

if __name__ == "__main__":
    main()