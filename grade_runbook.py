from datetime import datetime
import os
import json
import yaml
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

# Suppress noisy http loggers
logging.getLogger("httpcore").setLevel(logging.WARNING)  
logging.getLogger("httpx").setLevel(logging.WARNING)  

# Utils import
from stage0_py_utils import Evaluator, Loader

class Runbook:
    """
    Processor class for testing a grading prompt using a grading key
    """
    def __init__(self, config_folder="./config", input_folder="./input", output_folder="./output"):
        self.config_folder = config_folder
        self.input_folder = input_folder
        self.output_folder = output_folder

        # Read config and load prompts and keys
        with open(os.path.join(config_folder, "grade_config.yaml"), "r", encoding="utf-8") as file:
            self.config = yaml.safe_load(file) or {}
        
        self.loader = Loader(input_folder=input_folder)
        self.grade_prompt = self.loader.load_messages(files=self.config["prompt_files"])
        self.grade_keys = self.loader.load_messages(files=self.config["key_files"])
        self.evaluator = Evaluator(
            name="Grader", 
            grade_model=self.config["grade_model"],
            grade_prompt_files=self.config["prompt_files"],
            grade_prompt=self.grade_prompt
        )
        logger.info(f"Evaluator model: {self.config["grade_model"]}, prompt files: {self.config["prompt_files"]}, key files: {self.config["key_files"]}")
        
    def run(self):
        """Process Grader Configuration"""
        start = datetime.now()
        logger.info(f"Starting {len(self.grade_keys)} tests at {str(start)}")
        passing = 0
        outcomes = [{
            "started_at": str(start),
            "model": self.config["grade_model"], 
            "prompt_files": self.config["prompt_files"], 
            "key_files": self.config["key_files"]
        }]
        for line in self.grade_keys:
            given = line["given"]
            expected = line["expected"]
            min_value = float(line["min_value"])
            max_value = float(line["max_value"])
            before = datetime.now()
            grade = self.evaluator.grade_reply(expected=expected, given=given)
            latency = str(datetime.now() - before)
            outcomes.append({
                "given": given, 
                "expected": expected, 
                "grade": grade, 
                "min": min_value, 
                "max": max_value,
                "latency": latency
            })
            is_passing_score = isinstance(grade, float) and min_value <= grade <= max_value
            logger.info(f"Latency: {latency} Grade: {grade}, Min: {min_value} Max: {max_value} Pass: {is_passing_score}")
            if is_passing_score:
                passing += 1
                
        # Write output
        end = datetime.now()
        outcomes[0]["ended_at"] = str(end)
        timestamp = end.strftime("%Y.%m.%dT%H:%M:%S")
        filename = f"{timestamp}-grades.json"
        file_path = os.path.join(self.output_folder, filename)
        os.makedirs(self.output_folder, exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(outcomes, file, indent=4)  

        logger.info(f"Final Grade: {round(passing / len(self.grade_keys) * 100)}% in {end-start} Saved To: {file_path}")
    
def main():
    logger.info("============================ Grader Pipeline Starting ==============================")
    logger.info(f"Initialized, Input: {INPUT_FOLDER}, Output: {OUTPUT_FOLDER}, Config: {CONFIG_FOLDER} Logging Level {LOGGING_LEVEL}")
    
    try:
        runner = Runbook(config_folder=CONFIG_FOLDER, input_folder=INPUT_FOLDER, output_folder=OUTPUT_FOLDER)
        runner.run()
    except Exception as e:
        logger.error(f"Error Reported {str(e)}", exc_info=True)
        
    logger.info("======================== Grader Pipeline Completed Successfully =====================")

if __name__ == "__main__":
    main()