# stage0_runbook_grader
Grade the Grader runbook

# Grade Runbook
This runbook reads a [configuration.yaml](./test_data/config/grade_config.yaml) file, loads the referenced data files from the [input](./test_data/input/) folder, and then grades a model's responses to prompts that produce a grade when provided given and expected values. Grades are written to the [output](./test_data/output/) folder as yyyy.mm.ddThh:mm:ss-grades.json

## Expected Directory Structure
When you run the utility you will specify folders to mount for ``/config``, ``/input`` and ``/output``
```text
/📁 config
├── 📝 grade_config.yaml                # Grade Configuration
/📁 input
│── 📁 grader                           # Simple LLM message list with grading prompts and keys
│   ├── ✏️ grader1.csv                  # grade prompts
│   ├── ✏️ grader_key.csv               # grading keys (given, expected, min, max)
/📁 output
│   ├── 📀 yyyy-mm-ddThh:mm:ss-grades.json  # Grades from running the evaluation
```

## Using this in your project. 
Adjust the command below to use appropriate values for your Echo Bot project, and add it to your pipenv scripts. See the [test_data] folder for sample files. Grades will be written to a file called ``{datetime}-grades.json`` in the output folder when you run the tool. 

```bash
docker run --rm /
    -v ./my_model/input:/input
    -v ./my_model/config:/config
    -v ./my_model/output:/output
    ghcr.io/agile-learning-institute/stage0-echo-grade:latest
```

# Contributing

## Prerequisites

Ensure the following tools are installed:
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [Python](https://www.python.org/downloads/)
- [Pipenv](https://pipenv.pypa.io/en/latest/installation.html)

## Testing
All testing uses config/input/output folders in ./test_data.

## Install Dependencies
```bash
pipenv install
```

### Run Evaluate Runbook locally.
```bash
pipenv run grade
```

### Debug Evaluate Runbook locally
```bash
pipenv run debug
```
Runs locally with logging level set to DEBUG

### Build the Gary the Grader model
See Gary.modelfile - from llama3.2:latest, turns the temperature all the way down to 0
```bash
pipenv run model
```

### Build the Evaluate Runbook container
```bash
pipenv run build
```

### Build, and run the Evaluate Runbook container
```bash
pipenv run container
```