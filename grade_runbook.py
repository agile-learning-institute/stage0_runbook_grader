from datetime import datetime
import os
import json
import yaml


import logging
logger = logging.getLogger(__name__)

# Utils import
from stage0_py_utils import Evaluator, Loader, Config
config = Config()

class Runbook:
    """
    Processor class for testing a grading prompt using a grading key
    """
    def __init__(self):
        # Read runbook configuration and load prompts and keys
        with open(os.path.join(config.CONFIG_FOLDER, "grade_config.yaml"), "r", encoding="utf-8") as file:
            self.runbook_config = yaml.safe_load(file) or {}
        
        self.loader = Loader(input_folder=config.INPUT_FOLDER)
        self.grade_prompt = self.loader.load_messages(files=self.runbook_config["prompt_files"])
        self.grade_keys = self.loader.load_messages(files=self.runbook_config["key_files"])
        self.evaluator = Evaluator(
            name="Grader", 
            grade_model=self.runbook_config["grade_model"],
            grade_prompt_files=self.runbook_config["prompt_files"],
            grade_prompt=self.grade_prompt
        )
        logger.info(f"Evaluator model: {self.runbook_config["grade_model"]}, prompt files: {self.runbook_config["prompt_files"]}, key files: {self.runbook_config["key_files"]}")
        
    def run(self):
        """Process Grader Configuration"""
        start = datetime.now()
        logger.info(f"Starting {len(self.grade_keys)} tests at {str(start)}")
        passing = 0
        outcomes = [{
            "started_at": str(start),
            "model": self.runbook_config["grade_model"], 
            "prompt_files": self.runbook_config["prompt_files"], 
            "key_files": self.runbook_config["key_files"]
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
        file_path = os.path.join(config.OUTPUT_FOLDER, filename)
        os.makedirs(config.OUTPUT_FOLDER, exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(outcomes, file, indent=4)  

        logger.info(f"Final Grade: {round(passing / len(self.grade_keys) * 100)}% in {end-start} Saved To: {file_path}")
    
def main():
    logger.info("============================ Grader Pipeline Starting ==============================")
    
    try:
        runner = Runbook()
        runner.run()
    except Exception as e:
        logger.error(f"Error Reported {str(e)}", exc_info=True)
        
    logger.info("======================== Grader Pipeline Completed Successfully =====================")

if __name__ == "__main__":
    main()