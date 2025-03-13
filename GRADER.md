# Grader Pipeline Runbook

This runbook accepts as parameters the grading prompts, and key files to use in evaluating the grader. Key files consist of input Given and Expected values along with human assigned grade min/max values. The provided values are presented to the grading prompt, and their given grade is noted in the output.

## Using this in your project. 
Adjust this command to use appropriate values for your Echo Bot project. Your input folder should contain ``grader`` folders with the csv files with your grader and keys. TODO: Still in development
```bash
docker run --rm /
    -v ./bot_name:/opt/input
    -v ./bot_name:/opt/output
    -e GRADE_PROMPTS=["prompt1.csv","prompt2.csv"]
    -e GRADE_KEYS=["keys1.csv", "keys2.csv"]
    ghcr.io/agile-learning-institute/stage0-echo-grader:latest
```
# Contributing

## Prerequisites

Ensure the following tools are installed:
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [Python](https://www.python.org/downloads/)
- [Pipenv](https://pipenv.pypa.io/en/latest/installation.html)

## Testing

## Install Dependencies
```bash
pipenv install
```

### Clear out the ./test/output folder
```bash
pipenv run clean
```

### Run Grader Runbook locally.
```bash
pipenv run grade
```
Note: This does clean then runs the code locally

### Debug Grader Runbook locally
```bash
pipenv run debug_grader
```
Runs locally with logging level set to DEBUG

### Build the Grader Runbook container
```bash
pipenv run build_grader
```

### Build, and run the Grader Runbook container
```bash
pipenv run grader_container
```
Note: Will use ./test folders

