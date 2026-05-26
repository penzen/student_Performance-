# End to End Data Science Project

### Workflows--ML Pipeline

1. Data Ingestion
2. Data Validation
3. Data Transformation-- Feature Engineering,Data Preprocessing
4. Model Trainer
5. Model Evaluation- MLFLOW,Dagshub

## Workflows

1. Update config.yaml # important congifuration that we need for Data Ingestion
2. Update schema.yaml # used for Data validation, check the schema of the input we are getting 
3. Update params.yaml # Used for spefici conditons where there are spcific parameters that we need 
4. Update the entity # 
5. Update the configuration manager in src config 
6. Update the components
7. Update the pipeline # training pipline and batch prediction pipline 
8. Update the main.py


## Basically the important files in this project 
Notebook = testing/experimenting
components = actual reusable ML steps
config/entity/constants = settings and paths
pipeline = connects the steps
main.py = runs the project
Docker/GitHub Actions = deployment/automation later