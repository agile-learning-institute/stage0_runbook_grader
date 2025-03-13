import json
import yaml
import os
from datetime import datetime
from stage0_py_utils import Evaluator, Loader

import logging
logger = logging.getLogger(__name__)

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
        
    def run(self):
        """Process Grader Configuration"""
        outcomes = []
        passing = 0
        for line in self.grade_keys:
            given = line["given"]
            expected = line["expected"]
            min_value = float(line["min_value"])
            max_value = float(line["max_value"])
            grade = self.evaluator.grade_reply(expected=expected, given=given)
            outcomes.append({
                "given": given, 
                "expected": expected, 
                "grade": grade, 
                "min": min_value, 
                "max": max_value
            })
            logger.info(f"Grade: {grade}, Min: {min_value} Max: {max_value}")
            if grade and min_value <= grade <= max_value:
                passing += 1
                
        # Write output
        timestamp = datetime.now().strftime("%Y.%m.%dT%H:%M:%S")
        filename = f"{timestamp}-grades.json"
        file_path = os.path.join(self.output_folder, filename)
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(outcomes, file, indent=4)  

        print(f"Final Grade: {passing / len(outcomes)}")
    
def main():
    config_folder = os.getenv("CONFIG_FOLDER", "/config") 
    input_folder = os.getenv("INPUT_FOLDER", "./input")
    output_folder = os.getenv("OUTPUT_FOLDER", "./output")
    logging_level = os.getenv("LOG_LEVEL", logging.INFO)

    # Configure root logger
    logging.basicConfig(level=logging_level)

    # Suppress excessive DEBUG logs from `httpcore`
    logging.getLogger("httpcore").setLevel(logging_level)  
    logging.getLogger("httpx").setLevel(logging.WARNING)  # suppress `httpx` logs
    logging.getLogger("stage0_py_utils.evaluator").setLevel(logging_level)
    
    logger.info(f"============================ Grader Pipeline Starting ==============================")
    logger.info(f"Initialized, Input: {input_folder}, Output: {output_folder}, Config: {config_folder} Logging Level {logging_level}")
    
    try:
        runner = Runbook(config_folder=config_folder, input_folder=input_folder, output_folder=output_folder)
        runner.run()
    except Exception as e:
        logger.error(f"Error Reported {str(e)}", exc_info=True)
    logger.info(f"===================== Grader Pipeline Completed Successfully =======================")

if __name__ == "__main__":
    main()