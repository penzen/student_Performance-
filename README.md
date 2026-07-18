# California Housing MLOps Project — Section Report

## 1. What this section was about

In this section, we moved from simple notebook-style machine learning code into a more production-style MLOps project structure.

The project uses the California housing dataset:

```text
https://raw.githubusercontent.com/ageron/handson-ml2/master/datasets/housing/housing.tgz
```

The basic ML goal is:

```text
Given information about housing districts, predict median_house_value.
```

So this is a **regression problem**, because the target value is numerical.

The broader MLOps goal is not only to train a model, but to build a structured pipeline:

```text
Data ingestion
→ Data validation
→ Data transformation
→ Model training
→ Model saving
→ Later: model evaluation, serving, Docker, CI/CD, etc.
```

---

## 2. Why the project felt confusing

This section was confusing because the project changed from:

```text
One notebook / one Python script
```

to:

```text
A modular project with many folders and files
```

That is normal. In a real MLOps project, code is separated into different parts so it becomes easier to maintain, test, debug, and deploy.

A simple notebook may contain everything in one place:

```text
load data
clean data
train model
save model
```

But a production-style project separates this into:

```text
config/
src/
components/
pipelines/
entity/
constants/
utils/
artifacts/
main.py
```

This is why many import errors and path errors appeared. The logic itself was often correct, but once the code was split across files, Python needed the correct package paths, working directory, and virtual environment.

---

## 3. Project structure we worked with

The project structure looked roughly like this:

```text
student_Performance_p1/
│
├── config/
│   └── config.yaml
│
├── src/
│   └── student_Performance_p1/
│       ├── __init__.py
│       ├── components/
│       │   ├── data_ingestion.py
│       │   ├── data_validation.py
│       │   ├── data_transformation.py
│       │   └── model_trainer.py
│       │
│       ├── config/
│       │   └── configuration.py
│       │
│       ├── constants/
│       │   └── __init__.py
│       │
│       ├── entity/
│       │   └── config_entity.py
│       │
│       ├── pipelines/
│       │   └── data_ingestion_pipeline.py
│       │
│       └── utils/
│           └── common.py
│
├── schema.yaml
├── params.yaml
├── main.py
├── requirements.txt
└── artifacts/
```

The important idea:

```text
config.yaml stores paths/settings
schema.yaml stores expected data columns and target column
params.yaml stores model hyperparameters
config_entity.py stores dataclasses
configuration.py reads YAML and builds config objects
components/ contains actual ML logic
pipelines/ connects components
main.py runs the pipeline stages
artifacts/ stores generated files
```

---

## 4. Data ingestion stage

### Goal

The data ingestion stage downloads the dataset and extracts it.

Input:

```text
housing.tgz
```

Output:

```text
artifacts/data_ingestion/housing.tgz
artifacts/data_ingestion/housing.csv
```

### Important lesson: `.tgz` is not `.zip`

At first, the code used:

```python
import zipfile
```

and tried:

```python
with zipfile.ZipFile(self.config.local_data_file, "r") as zip_ref:
    zip_ref.extractall(self.config.unzip_dir)
```

That was wrong because the dataset file is:

```text
housing.tgz
```

A `.tgz` file should be extracted using `tarfile`, not `zipfile`.

Correct code:

```python
import tarfile

with tarfile.open(self.config.local_data_file, "r:gz") as tar_ref:
    tar_ref.extractall(path=self.config.unzip_dir)
```

### Data ingestion config

In `config.yaml`, the ingestion section became:

```yaml
data_ingestion:
  root_dir: artifacts/data_ingestion
  source_URL: https://raw.githubusercontent.com/ageron/handson-ml2/master/datasets/housing/housing.tgz
  local_data_file: artifacts/data_ingestion/housing.tgz
  unzip_dir: artifacts/data_ingestion
```

### Final successful result

The stage successfully produced:

```text
Data downloaded successfully to: artifacts/data_ingestion/housing.tgz
Data extracted successfully to: artifacts/data_ingestion
```

So the ingestion stage worked.

---

## 5. YAML and ConfigBox issues

### Problem 1: `Cannot extrapolate Box from string`

We saw this error:

```text
Cannot extrapolate Box from string
```

This happened because one YAML file had plain text or invalid YAML structure.

For example, this is bad:

```yaml
params
```

because it is just a string.

This is valid:

```yaml
{}
```

or:

```yaml
ElasticNet:
  alpha: 0.2
  l1_ratio: 0.1
```

### Fix for `params.yaml`

Since the project was not using parameters yet at that point, we made `params.yaml` valid by using:

```yaml
{}
```

Later, for model training, it should contain:

```yaml
ElasticNet:
  alpha: 0.2
  l1_ratio: 0.1
```

### Problem 2: `schema.yaml` structure

The schema needed to be a dictionary-like YAML structure, not just plain text.

Correct `schema.yaml`:

```yaml
COLUMNS:
  longitude: float64
  latitude: float64
  housing_median_age: float64
  total_rooms: float64
  total_bedrooms: float64
  population: float64
  households: float64
  median_income: float64
  ocean_proximity: object
  median_house_value: float64

TARGET_COLUMN:
  name: median_house_value
```

### Important lesson

`ConfigBox` follows the YAML structure exactly.

So if the YAML is:

```yaml
TARGET_COLUMN:
  name: median_house_value
```

then Python must access it like this:

```python
self.schema.TARGET_COLUMN.name
```

not:

```python
self.schema.name
```

---

## 6. `Path` import problem in `common.py`

### Mistake

In `common.py`, this was used:

```python
from anyio import Path
```

That was wrong for this project.

### Fix

Use Python’s built-in `pathlib`:

```python
from pathlib import Path
```

### Why it mattered

Your constants were using `pathlib.Path`, for example:

```python
CONFIG_FILE_PATH = Path("config/config.yaml")
```

But `read_yaml()` was expecting `anyio.Path`, which caused type-checking problems with `ensure_annotations`.

Correct import:

```python
from pathlib import Path
```

---

## 7. `ensure_annotations` problem

We saw an error like:

```text
isinstance() arg 2 must be a type, a tuple of types, or a union
```

This happened around functions using:

```python
@ensure_annotations
```

especially on functions returning `None`, like:

```python
@ensure_annotations
def create_directories(path_to_directories: list) -> None:
```

### Fix

We removed `@ensure_annotations` from `create_directories()`.

Correct version:

```python
def create_directories(path_to_directories: list):
    try:
        for path in path_to_directories:
            os.makedirs(path, exist_ok=True)

        logger.info(f"Directories created successfully: {path_to_directories}")

    except Exception as e:
        logger.error(f"Error while creating directories: {e}")
        raise ValueError(f"Error while creating directories: {e}")
```

### Lesson

`ensure_annotations` can be helpful, but it can also create confusing errors, especially with newer Python versions and return type `None`.

---

## 8. Virtual environment problem

A major issue was that the terminal showed:

```text
(.venv)
```

but Python was still using base Python.

The real check is not the prompt. The real check is:

```cmd
where python
python -c "import sys; print(sys.executable)"
python -m pip --version
```

Correct result should be:

```text
C:\Users\penze\Desktop\MLdev_ops\.venv\Scripts\python.exe
```

Wrong result was:

```text
C:\Users\penze\AppData\Local\Programs\Python\Python313\python.exe
```

### Safe way to run the project

Use the full virtual environment Python path:

```cmd
C:\Users\penze\Desktop\MLdev_ops\.venv\Scripts\python.exe main.py
```

from inside the project folder:

```cmd
cd C:\Users\penze\Desktop\MLdev_ops\student_Performance_p1
```

### Safe install command

Install packages into the real `.venv` with:

```cmd
C:\Users\penze\Desktop\MLdev_ops\.venv\Scripts\python.exe -m pip install package_name
```

For example:

```cmd
C:\Users\penze\Desktop\MLdev_ops\.venv\Scripts\python.exe -m pip install python-box
```

### Important lesson

This is not enough:

```text
(.venv)
```

Always trust:

```cmd
python -c "import sys; print(sys.executable)"
```

---

## 9. `python-box` vs `box` package problem

We saw this error:

```text
ImportError: cannot import name 'ConfigBox' from 'box'
```

This happened because the wrong package or wrong environment was being used.

Correct import:

```python
from box import ConfigBox
```

Correct package to install:

```cmd
pip install python-box
```

Not:

```cmd
pip install box
```

### Safe fix

```cmd
C:\Users\penze\Desktop\MLdev_ops\.venv\Scripts\python.exe -m pip uninstall box -y
C:\Users\penze\Desktop\MLdev_ops\.venv\Scripts\python.exe -m pip install python-box
```

Then test:

```cmd
C:\Users\penze\Desktop\MLdev_ops\.venv\Scripts\python.exe -c "from box import ConfigBox; print('ConfigBox works')"
```

---

## 10. Notebook vs project file issues

The code worked in the notebook because everything was in one place.

In a notebook, you can define:

```python
ConfigurationManager
DataIngestor
DataValidation
DataTransformation
ModelTrainer
```

all in one session.

But when moving code into files, Python imports become important.

For example:

```text
main.py
  ↓ imports
pipeline file
  ↓ imports
component file
  ↓ imports
config entity file
```

If one import path is wrong, the whole project fails.

### Main lesson

Notebook code working does not automatically mean modular project code will work.

When converting notebook code to files, check:

```text
imports
working directory
virtual environment
YAML path names
dataclass field names
```

---

## 11. Import path mistakes

Several errors came from mixing import styles.

Wrong examples:

```python
from student_Performance_p1.src.student_Performance_p1.entity.config_entity import DataIngestConfig
```

This is wrong because it repeats the project structure too much.

For the current setup, we used:

```python
from src.student_Performance_p1.entity.config_entity import DataIngestConfig
```

The important rule:

```text
Use one import style consistently.
```

For now:

```python
from src.student_Performance_p1...
```

Later, after proper editable installation:

```cmd
python -m pip install -e .
```

the cleaner professional import style would be:

```python
from student_Performance_p1...
```

But mixing both styles causes errors.

---

## 12. VS Code play button issue

The VS Code play button can use a different:

```text
Python interpreter
working directory
```

So it may run with the correct `.venv`, but from the wrong folder.

That breaks relative paths like:

```python
Path("config/config.yaml")
```

because those depend on the current working directory.

### Correct project working directory

For this project, we want:

```text
C:\Users\penze\Desktop\MLdev_ops\student_Performance_p1
```

If VS Code runs from:

```text
C:\Users\penze\Desktop\MLdev_ops
```

then this path:

```text
config/config.yaml
```

will be searched in the wrong place.

### Debug command

Use:

```python
import sys, os
print(sys.executable)
print(os.getcwd())
```

Expected:

```text
C:\Users\penze\Desktop\MLdev_ops\.venv\Scripts\python.exe
C:\Users\penze\Desktop\MLdev_ops\student_Performance_p1
```

---

## 13. Data validation stage

### Goal

The validation stage checks whether the dataset columns match the expected schema.

Actual dataset columns come from:

```python
data.columns
```

Expected columns come from:

```python
schema.yaml
```

### First validation issue

We got:

```text
'ConfigBox' object has no attribute 'columns'
```

because code used:

```python
self.schema.columns
```

but the schema file had:

```yaml
COLUMNS:
```

Correct access:

```python
self.schema.COLUMNS
```

### Second validation issue

We got:

```text
DataValidationConfig object has no attribute STATUS_FILE
```

because the dataclass had:

```python
status_file
```

but the code used:

```python
self.config.STATUS_FILE
```

Correct code:

```python
self.config.status_file
```

### Third validation issue

Validation returned:

```text
False
```

because the code accidentally passed the whole schema:

```python
all_schema=self.schema
```

Instead of only the column dictionary:

```python
all_schema=self.schema.COLUMNS
```

Correct mapping:

```python
data_validation_config = DataValidationConfig(
    root_dir=config.root_dir,
    status_file=config.status_file,
    unzipped_data_dir=config.unzipped_data_dir,
    all_schema=self.schema.COLUMNS
)
```

### Important lesson

When using YAML + dataclasses, names must match exactly:

```text
status_file != STATUS_FILE
COLUMNS != columns
```

Python is case-sensitive.

---

## 14. Missing values in the dataset

We checked:

```python
data.isnull().sum()
```

Result:

```text
longitude               0
latitude                0
housing_median_age      0
total_rooms             0
total_bedrooms        207
population              0
households              0
median_income           0
median_house_value      0
ocean_proximity         0
```

This means only `total_bedrooms` has missing values.

### What we learned

ML models generally cannot train with missing values.

Later, this should be handled during data transformation using imputation.

Example:

```python
from sklearn.impute import SimpleImputer

imputer = SimpleImputer(strategy="median")
```

For this project, the important finding was:

```text
total_bedrooms has 207 missing values
```

---

## 15. Data transformation stage

### Goal

The transformation stage split the full dataset into train and test files.

Input:

```text
artifacts/data_ingestion/housing.csv
```

Output:

```text
artifacts/data_transformation/transformed_train_data.csv
artifacts/data_transformation/transformed_test_data.csv
```

### Config section

The `config.yaml` section became:

```yaml
data_transformation:
  root_dir: artifacts/data_transformation
  data_path: artifacts/data_ingestion/housing.csv
  transformed_train_data: artifacts/data_transformation/transformed_train_data.csv
  transformed_test_data: artifacts/data_transformation/transformed_test_data.csv
```

### Dataclass mistake

We first had:

```python
@dataclass
class DataTransformationConfig:
    root_dir: Path
    data_path: Path
    ingested_test_path: Path
```

But the code was creating:

```python
DataTransformationConfig(
    root_dir=config.root_dir,
    data_path=config.data_path,
    train_data_path=config.transformed_train_data,
    test_data_path=config.transformed_test_data
)
```

This caused:

```text
unexpected keyword argument 'train_data_path'
```

### Fix

The dataclass needed to match the arguments:

```python
@dataclass
class DataTransformationConfig:
    root_dir: Path
    data_path: Path
    train_data_path: Path
    test_data_path: Path
```

### Data saving mistake

Wrong:

```python
train_set.to_csv(self.config.ingested_train_path, "train.csv", index=False)
```

The second argument in `to_csv()` is not the file name. It is treated as a separator.

Correct:

```python
train_set.to_csv(self.config.train_data_path, index=False)
test_set.to_csv(self.config.test_data_path, index=False)
```

### Lesson

Dataclass fields, config keys, and class attributes must align:

```text
config.yaml → ConfigurationManager → dataclass → component class
```

---

## 16. Model trainer stage

### Goal

Train an ElasticNet regression model and save it.

Input:

```text
artifacts/data_transformation/transformed_train_data.csv
artifacts/data_transformation/transformed_test_data.csv
```

Output:

```text
artifacts/model_trainer/model.joblib
```

### Config section

```yaml
model_trainer:
  root_dir: artifacts/model_trainer
  train_data_path: artifacts/data_transformation/transformed_train_data.csv
  test_data_path: artifacts/data_transformation/transformed_test_data.csv
  model_path: artifacts/model_trainer/model.joblib
```

### Mistake 1: wrong config keys

The code tried:

```python
config.transformed_train_data
config.transformed_test_data
```

But inside the `model_trainer` section, the keys were:

```yaml
train_data_path
test_data_path
```

Correct:

```python
train_data_path=config.train_data_path
test_data_path=config.test_data_path
```

### Mistake 2: `model_name` vs `model_path`

The YAML had:

```yaml
model_path: artifacts/model_trainer/model.joblib
```

But the code tried:

```python
config.model_name
```

This caused:

```text
'ConfigBox' object has no attribute 'model_name'
```

### Fix

Use:

```python
model_path=config.model_path
```

### Mistake 3: target column path

The code tried:

```python
target_column=self.schema.name
```

But schema was:

```yaml
TARGET_COLUMN:
  name: median_house_value
```

Correct:

```python
target_column=self.schema.TARGET_COLUMN.name
```

### Mistake 4: categorical column error

ElasticNet failed with:

```text
could not convert string to float: 'NEAR OCEAN'
```

because the column:

```text
ocean_proximity
```

contains text categories.

ElasticNet only accepts numeric features.

Quick fix:

```python
x_train = train_data.drop(columns=[self.config.target_column, "ocean_proximity"], axis=1)
y_train = train_data[self.config.target_column]

x_test = test_data.drop(columns=[self.config.target_column, "ocean_proximity"], axis=1)
y_test = test_data[self.config.target_column]
```

Better future fix:

```text
Use OneHotEncoder for ocean_proximity in the transformation stage.
```

### Mistake 5: duplicated model save path

The code tried to save to:

```text
artifacts/model_trainer\artifacts/model_trainer/model.joblib
```

because it joined:

```python
os.path.join(self.config.root_dir, self.config.model_name)
```

while `model_name` already contained the full path.

Correct:

```python
joblib.dump(model, self.config.model_path)
```

### Lesson

Use one of these approaches:

If YAML has only file name:

```yaml
model_name: model.joblib
```

then save with:

```python
os.path.join(self.config.root_dir, self.config.model_name)
```

If YAML has full path:

```yaml
model_path: artifacts/model_trainer/model.joblib
```

then save with:

```python
joblib.dump(model, self.config.model_path)
```

In this project, we used the second approach.

---

## 17. Important pattern we learned

Every stage follows the same pattern:

```text
1. Add paths/settings in config.yaml
2. Create a dataclass in config_entity.py
3. Add a get_stage_config() method in configuration.py
4. Build the component class in components/
5. Build the pipeline class in pipelines/
6. Call the pipeline from main.py
```

Example:

```text
Data ingestion:
  DataIngestConfig
  get_data_ingest_config()
  DataIngestor
  DataIngestionPipeline

Data validation:
  DataValidationConfig
  get_data_validation_config()
  DataValidation
  DataValidationPipeline

Data transformation:
  DataTransformationConfig
  get_data_transformation_config()
  DataTransformation
  DataTransformationPipeline

Model trainer:
  ModelTrainerConfig
  get_model_trainer_config()
  ModelTrainer
  ModelTrainerPipeline
```

This is the general production-style MLOps structure.

---

## 18. Most common mistakes from this section

### Mistake 1: Trusting `(.venv)` too much

`(.venv)` in the terminal is not proof that Python is using the venv.

Always check:

```cmd
python -c "import sys; print(sys.executable)"
```

### Mistake 2: Installing packages into base Python

If `python` points to base Python, then:

```cmd
python -m pip install package
```

installs into base Python.

Safe command:

```cmd
C:\Users\penze\Desktop\MLdev_ops\.venv\Scripts\python.exe -m pip install package
```

### Mistake 3: Mixing import styles

Bad:

```python
from student_Performance_p1.src.student_Performance_p1...
```

Use one style consistently:

```python
from src.student_Performance_p1...
```

### Mistake 4: YAML key mismatch

Examples:

```text
status_file != STATUS_FILE
COLUMNS != columns
model_path != model_name
train_data_path != transformed_train_data
```

### Mistake 5: Dataclass field mismatch

If dataclass has:

```python
ingested_test_path
```

but code passes:

```python
train_data_path
```

it fails.

### Mistake 6: Using wrong config class

We accidentally used `DataIngestionConfig` for data transformation.

Each stage needs its own config class.

### Mistake 7: Categorical text in ML model

ElasticNet cannot use:

```text
NEAR OCEAN
```

directly.

Text categories must be encoded or dropped.

### Mistake 8: Duplicate path joining

If YAML already has full path:

```yaml
model_path: artifacts/model_trainer/model.joblib
```

do not join it again with `root_dir`.

---

## 19. What we successfully completed

By the end of this section, we successfully got several pipeline pieces working.

### Completed

```text
Project structure created
YAML config loading fixed
Virtual environment issue understood
Data ingestion completed
Data validation logic debugged
Data transformation completed
Model trainer reached training stage
ElasticNet trained after dropping text column
Model saving path issue identified and fixed
```

### Generated artifacts

```text
artifacts/data_ingestion/housing.tgz
artifacts/data_ingestion/housing.csv

artifacts/data_validation/status.txt

artifacts/data_transformation/transformed_train_data.csv
artifacts/data_transformation/transformed_test_data.csv

artifacts/model_trainer/model.joblib
```

---

## 20. Key MLOps lessons

This section taught more than just ML. It taught real MLOps debugging.

The key lessons were:

```text
1. Production ML projects are mostly about structure and reliability.
2. YAML configs make paths/settings reusable, but names must match exactly.
3. Dataclasses are useful, but they are strict about field names.
4. Notebook code and modular project code behave differently.
5. Virtual environments must be verified, not assumed.
6. Relative paths depend on the working directory.
7. Data validation catches schema problems.
8. Data transformation prepares data for training.
9. Model training requires numeric input.
10. Saving models requires clean path handling.
```

---

## 21. Clean final command to run project

From the project folder:

```cmd
cd C:\Users\penze\Desktop\MLdev_ops\student_Performance_p1
```

Run with the real virtual environment Python:

```cmd
C:\Users\penze\Desktop\MLdev_ops\.venv\Scripts\python.exe main.py
```

To confirm environment and directory:

```cmd
C:\Users\penze\Desktop\MLdev_ops\.venv\Scripts\python.exe -c "import sys, os; print(sys.executable); print(os.getcwd())"
```

Expected:

```text
C:\Users\penze\Desktop\MLdev_ops\.venv\Scripts\python.exe
C:\Users\penze\Desktop\MLdev_ops\student_Performance_p1
```

---

## 22. Final reflection

The confusion in this section was completely normal.

This was not just a simple ML lesson. It involved:

```text
Python package imports
virtual environments
Jupyter notebook behavior
YAML files
ConfigBox
dataclasses
project structure
relative paths
data validation
data transformation
model training
model saving
```

That is a lot of moving pieces.

The important achievement is that each error taught something practical:

```text
Import errors taught package structure.
YAML errors taught config design.
Dataclass errors taught strict object construction.
Model errors taught preprocessing.
Path errors taught artifact management.
Environment errors taught reproducibility.
```

This is exactly the kind of debugging that happens in real MLOps work.
