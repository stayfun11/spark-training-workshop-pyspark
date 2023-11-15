**spark-training - workshop**

- **Team**: spark-training <spark-training@decathlon.com>
- **Template**: [DPS Python template](https://github.com/dktunited/dps-python-template)
- **Description**: training

# Table of Content
- [Table of Content](#table-of-content)
- [Resources](#resources)
  * [Github](#github)
  * [AWS Account](#aws-account)
  * [Project Documentation](#project-documentation)
  * [SonarCloud Code Quality](#sonarcloud-code-quality)
- [Installation](#installation)
  * [Git Repository](#git-repository)
  * [Dependencies](#dependencies)
- [How-To](#how-to)
  * [Publish artifacts on snapshot environment](#publish-artifacts-on-snapshot-environment)
  * [Publish artifacts on release environment](#publish-artifacts-on-release-environment)
  * [Install dependencies from CodeArtifact](#install-dependencies-from-codeartifact)
  * [Deploy images manually on industrialization environment (EMR / Databricks)](#deploy-images-manually-on-industrialization-environment--emr---databricks-)
    + [On databricks](#on-databricks)
    + [On EMR](#on-emr)
      - [Create a fixed dev EMR cluster](#create-a-fixed-dev-emr-cluster)
        * [Run jobs on the EMR cluster](#run-jobs-on-the-emr-cluster)
  * [Deploy images via Airflow](#deploy-images-via-airflow)
  * [Update the project version](#update-the-project-version)
  * [Use the data catalog](#use-the-data-catalog)
    + [Some examples](#some-examples)
  * [Setup Open Lineage](#setup-open-lineage)
  * [Add a new project environment](#add-a-new-project-environment)
  * [Include new dependencies in the project](#include-new-dependencies-in-the-project)
  * [Get the list of tasks supported by this project](#get-the-list-of-tasks-supported-by-this-project)
  * [Clean the project repository for reverting its state](#clean-the-project-repository-for-reverting-its-state)
  * [Build the Python package used in the publication stage](#build-the-python-package-used-in-the-publication-stage)
  * [Execute the package script locally from the command-line](#execute-the-package-script-locally-from-the-command-line)
  * [Use the configuration files in this project (in `confs/`)](#use-the-configuration-files-in-this-project--in--confs---)
  * [Use DBX to sync your local code or ship your job on databricks ?](#use-dbx-to-sync-your-local-code-or-ship-your-job-on-databricks--)
    + [What is DBX ?](#what-is-dbx--)
    + [How do we use it in this template ?](#how-do-we-use-it-in-this-template--)
    + [Setup DBX](#setup-dbx)
    + [Sync your local code with your databricks repo](#sync-your-local-code-with-your-databricks-repo)
    + [Run your jobs on databricks.](#run-your-jobs-on-databricks)
  * [Change the version number of Poetry, Python, Package, ...](#change-the-version-number-of-poetry--python--package--)
  * [Check that the quality of the code fits the standard of Decathlon](#check-that-the-quality-of-the-code-fits-the-standard-of-decathlon)
  * [Report the code quality of my project to SonarCloud](#report-the-code-quality-of-my-project-to-sonarcloud)
  * [Format the code automatically to fit to Decathlon standard](#format-the-code-automatically-to-fit-to-decathlon-standard)
  * [Generate and deploy the documentation of the project on Github Pages](#generate-and-deploy-the-documentation-of-the-project-on-github-pages)

# Resources

This section enumerates the resources available to support the project development.

## Github

- **[Github Repository](https://github.com/dktunited/spark-training-workshop-pyspark)**: Storage and versionning of the project source code.
- **[Github Workflows](https://github.com/dktunited/spark-training-workshop-pyspark/actions)**: Automation of repetitive task (e.g., publication of code artifacts).
  
## AWS Account

- **[AWS S3 Bucket (S3)](https://s3.console.aws.amazon.com/s3/buckets/dev-dct-wksp-spark-training?prefix=spark-training-workshop-pyspark%2F&region=eu-west-1&showversions=false#)**: Storage of the datasets and configurations during development.
  - Note: you should NOT store code artifacts there. Use resources below for that purpose.
- **[AWS Code Artifact (CA)](https://eu-west-1.console.aws.amazon.com/codesuite/codeartifact/d/614303399241/dataplatform-dev/r/dataplatform-dev-store-pypi/p/pypi/spark-training-workshop-pyspark/versions?region=eu-west-1)**: Storage and versionning for Python packages (i.e., wheel files).
- **[AWS Elastic Container Registry (ECR)](https://eu-west-1.console.aws.amazon.com/ecr/repositories/private/614303399241/spark-training-workshop-pyspark-dev?region=eu-west-1)**: Storage and versionning of Docker image/containers.

## Project Documentation

- **[Sphinx Documentation](SPHINX_DOCUMENTATION_URL)**: Documentation of the project, hosted on Github Pages.

## SonarCloud Code Quality

- **[SonarCloud Dashboard](https://sonarcloud.io/project/overview?id=dktunited_spark-training-workshop-pyspark)**: Report and visualize the code quality of an internal project.

# Installation

This section explains the steps required to start developing for the project.

## Git Repository

**[Clone the remote Git repository to your local computer](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository).**

```bash
# With SSH (recommended)
git clone ssh@git@github.com:dktunited/spark-training-workshop-pyspark.git
# With HTTPS
git clone https://github.com/dktunited/spark-training-workshop-pyspark.git
```

## Dependencies

**Install the project dependencies in a [Python Virtual Environment](https://docs.python.org/3/library/venv.html).**

```bash
make install-dev
```

# How-To
## Publish artifacts on snapshot environment 
To publish snapshot artifacts on the "snapshot" environment, *i.e.* 
* the "snapshot" CodeArtifact registry "dataplatform-dev-store-pypi", hosted on the preprod account
* the "dev" ECR registry "614303399241.dkr.ecr.eu-west-1.amazonaws.com/spark-training-workshop-pyspark-dev", hosted on the preprod account

You can either run the following target:

```commandline
make publishers ENV=dev
```

or you can trigger publication process with github actions.

To do so, go on the "Actions" tab of your github project, select "Publish artifacts on dev" workflow, and
click on the "Run workflow" button.

## Publish artifacts on release environment 
To publish snapshot artifacts on the "release" environment, *i.e.* 
* the "release" CodeArtifact registry "dataplatform-store-pypi", hosted on the prod account
* the "preprod" ECR registry "614303399241.dkr.ecr.eu-west-1.amazonaws.com/spark-training-workshop-pyspark", hosted on the preprod account
* the "prod" ECR registry "614303399241.dkr.ecr.eu-west-1.amazonaws.com/spark-training-workshop-pyspark", hosted on the prod account

You can either manually run the "Publish artifacts on ppd & prd" github actions workflow, or you can create 
a release on github. The creation of the release will trigger the "Publish artifacts on ppd & prd" workflow.


## Install dependencies from CodeArtifact

1. Add a custom repo to the poetry configuration file with the following command:

```
make add-ca-repository
```

This will add the following lines to the `myproject.toml` file:

```
[[tool.poetry.source]]
name = "repo-name"
url = "repo-url"
priority = "supplemental"
```

2. Now you can install your dependencies by adding the following line to the `dependencies` section of the `myproject.toml` file:

```
your-python-dep = {version = "^1.0.0", source = "repo-name"}
```

For example, to install the `requests` package from CodeArtifact, you would add the following line to the `dependencies` section:

```
requests = {version = "^2.26.0", source = "repo-name"}
```

Once you have added the custom repo and the dependency to the `myproject.toml` file, you can install the dependencies by running the following command:

```
poetry install
```

This will install the dependencies from the CodeArtifact repository.

**Here are some additional notes:**

* The `repo-name` and `repo-url` values should be the name and URL of the CodeArtifact repository that you want to use.
* The `priority` value can be set to `required`, `recommended`, `optional`, or `supplemental`. The default value is `supplemental`.
* The `version` value should be the version of the dependency that you want to install.



## Deploy images manually on industrialization environment (EMR / Databricks)
This section explains how you can fire-up a test industrialization infrastructure 
(EMR or Databricks) and run your spark docker image on it. 

You can use both EMR or Databricks. We recommend using Databricks, for its simplicity, 
its better interface and the fact that it is easier to access logs. 
However, you are free to use the service of your choice, so we describe both approaches. 

### On databricks
This is the **recommended approach**

* First, go on 
[Databricks exploration workspace](https://decathlon-dataplatform-exploration.cloud.databricks.com/login.html)

* In the "workflow" tab, click on "create job"

* For 'Type', choose 'Spark Submit'

* Click on the "edit" button next to cluster -> it opens a "Configure Cluster" window:
  * choose the policy corresponding to your team (*e.g.*: 'Dps-jobs' for DPS team)  
  * In 'Docker' tab of 'advanced' section, click "Use your own Docker container" and 
  fill the URI of your docker image on ECR, which should be something like 
  `614303399241.dkr.ecr.eu-west-1.amazonaws.com/dps-my-project-pyspark:1.0.0.dev0`

then click on "Create" (leave the other fields as is)

* Add the args for spark-submit, an example of valid args for the example jobs are
  
```bash
["--packages=io.openlineage:openlineage-spark:0.18.0",
"s3://dev-dct-wksp-dps/dps-my-project-pyspark/jobs/1.0.0.dev0/example_job.py",
"--env=dev",
"--confs-dir=s3://dev-dct-wksp-dps/dps-my-project-pyspark/confs/1.0.0.dev0",
"--log-level=INFO"]
```

* Then click on "Create"

* Then, click on "Run now"

* You can them follow the execution of your job and checks the logs in the 
  job run page. To see how to do it, please refer to 
  [How to read the production logs on Databricks](#on-databricks)

### On EMR
#### Create a fixed dev EMR cluster
We recommend using the jenkins service to create fixed EMR cluster. 

* go to the [jenkins](https://dataplatform-jenkins.dktapp.cloud/job/EMR/job/EMR_Create_Cluster/job/AWS-EMR-create-dev-cluster/)
  page (don't forget to enable zscaler)
* choose AWS-EMR-create-dev-cluster > build with parameters
* Choose EMR version: 6.9.0 (**IMPORTANT**, The run of docker images raises an error with EMR 6.10.0, so please use 6.9.0)
* choose the following options:
  * app: your team name (eg: tuk-dev)
  * name of cluster: whatever (note that a prefix will be added to your cluster name)
  * instace type master: r5.xlarge (this is recommended to change the default setting to avoid RAM saturation)
  * nbr core spots (for master): 2 (we invert the spots vs on demand to decrease the cost)
  * nbr core on demand (for master): 0
  * use docker : yes
  * enable glue: yes
  * other options set to default
* click on build, then wait for the cluster to be created.
* Get the cluster-id that should look like j-3CT52HIZ9BTM6

##### Run jobs on the EMR cluster

**IMPORTANT NOTE - EMR 6.10 **: As of today (june 5th 2023), there is currently a bug on EMR 6.10 which prevents
from running docker images. So **please use EMR 6.9.0** (or lower versions) for now (since this project use
docker container as artefacts)

You can then run directly the 'add-steps' command from your terminal with the following
makefile target 
```bash 
make deploy-on-emr EMR_CLUSTER_ID=<YOUR-EMR-CLUSTER-ID> JOB_FILE=<PYTHON-JOB-FILE>
```
where 
* EMR_CLUSTER_ID is the cluster id you got when creating the cluster with Jenkins
* JOB_FILE is the python file you want to run on the cluster (it should be in the `jobs` folder)

For instance
makefile target 
```bash 
make deploy-on-emr EMR_CLUSTER_ID=j-3CT52HIZ9BTM6 JOB_FILE=example_job.py
```

You can then go the EMR interface on AWS console to check out the logs of your application. 
For more details on how to do that, please check the 
[How to read the production logs](#how-to-read-the-production-logs) section. 

## Deploy images via Airflow
To see how to deploy your dockerized jobs on EMR or databricks via Airflow, please
refer to the section "Executing Spark jobs" of the 
[DPS Airflow template](https://github.com/dktunited/dps-airflow-template) documentation. 

## Update the project version
The source of truth for the project version is the version defined in the `VERSION` file, at the root of the project.
To update the version, you must : 
* update the version in `VERSION` file
* propagate the version to the `version` variable in other files (`pyproject.toml` and `env/base.env`)
  by running the following target `make bump-package`

Please note that the `bump-package` target will be automatically executed when 
* you run the global `make publishers` target
* you trigger the `publication-dev` GA workflow

## Use the data catalog
This module `conf.config` will also load the `catalog.yml` files. 
These files contain the **job data catalog** which is the configuration to read and write your data.

This configuration is given as an input of the `Dataset` object in the `io.core` module. The `Dataset` object
is a simplified layer given to the Data Engineer to easily and generically read or write data. Not extra code is needed, 
just add your data in the `catalog.yml` file.

**Important note**: 
* The data catalog lets you specify data sources either as data files (e.g. csv, parquet, etc.) 
or as tables (implemented with Glue Catalog).
* We highly recommend **using glue tables** when possible, as it ensures strong typing oy your dataset, as
well as the completeness of our data-lake's metastore.

The `catalog.yml` file as a specific schema to follow:
```yml
<job_name>: # Name of the job, you will define in it all the data needed for this job
  inputs: # The input data e.g. the data you will read
    <dataset>: # name of your dataset
      path: 'path/to/your/data' # the path to your data
      # OR
      table: 'database.table_name' # the database and the table name of your data
      schema: 'project_name.io.schemas.dataset.SCHEMA' # optional: the schema of your data
      read_args: # Read options
        format: csv # mandatory: the data format
        header: true # optional: other read options available in Spark
  outputs: # The output data e.g. the data you will write
    <dataset>: # name of your dataset
      path: 'path/to/your/data' # the path to your data
      # OR
      table: 'database.table_name' # the database and the table name of your data
      schema: 'project_name.io.schemas.dataset.SCHEMA' # optional: the schema of your data
      write_args: # Write options
        format: parquet # mandatory: the data format
        mode: overwrite # optional: writing mode (overwrite or append)
```

In the read_args and write_args you can specify all the options available in Spark for your file format 
(e.g. you can add the `header` option for the CSV file format).

### Some examples
In this example, we will read CSV files with a header and write our output data in parquet. We want to rewrite the data
every time the job is executed.

It will give this `catalog.yml` file:
```yaml
example_job:
  inputs:
    flights:
      path: 'data/inputs/flights/*'
      read_args:
        format: csv
        header: true
  outputs:
    aggregated_flights:
      path: 'data/outputs/aggregated_flights/'
      write_args:
        format: parquet
        mode: overwrite
```
With the `ConfigLoader`, you can load the job data catalog and use it to read and write your data:
```python
# Load the config and catalog files
config_loader = ConfigLoader("local")
catalog = config_loader["catalog"]["example_job"]
inputs = catalog["inputs"]
outputs = catalog["outputs"]

# Read the inputs data
flights = Dataset(
    spark=spark,
    config=inputs["flights"]
).read()

aggregated_flights = transform_data(flights) # Transform the input data

# Write results in outputs dir
Dataset(
    spark=spark,
    config=outputs["aggregated_flights"],
).write(aggregated_flights)
```
And that's it ! The `Dataset` object will read the config from the `catalog.yml` file under `inputs` under `flights`, 
and read the `flights` data. The output of the `read` method is a `DataFrame` containing your data.

Then, when you write the `aggregated_flights` data, the `Dataset` object will write the `DataFrame` given as input, 
to the location and format given in the `catalog.yml` under `outputs` under `aggregated_flights`.

**Add the schemas**

We can add schemas to our data. To do so, we have to add the schemas in the `io.schemas` module.
Each schema must be in a dedicated file.

Here is an example of the schema files:
```python
# io.schemas.flights.py file
from pyspark.sql.types import (
    StringType,
    StructField,
    StructType,
    LongType
)


SCHEMA = StructType(
    [
        StructField('DEST_COUNTRY_NAME', StringType(), True),
        StructField('ORIGIN_COUNTRY_NAME', StringType(), True),
        StructField('count', LongType(), True)
    ]
)

# io.schemas.aggregated_flights.py file
from pyspark.sql.types import (
    StringType,
    StructField,
    StructType,
    LongType
)


SCHEMA = StructType(
    [
        StructField('DEST_COUNTRY_NAME', StringType(), True),
        StructField('TOTAL_COUNT', LongType(), True)
    ]
)
```

Than you have to add the path to the schemas in the `catalog.yml` files:
```yaml
example_job:
  inputs:
    flights:
      path: 'data/inputs/flights/*'
      schema: 'project_name.io.schemas.flights.SCHEMA'
      read_args:
        format: csv
        header: true
  outputs:
    aggregated_flights:
      path: 'data/outputs/aggregated_flights/'
      schema: 'project_name.io.schemas.aggregated_flights.SCHEMA'
      write_args:
        format: parquet
        mode: overwrite
```
You can relaunch your job and the schemas will be taken into account. Easy, right ?

**Write your data as a table in AWS Glue**

You can also read and write your data as a table in AWS Glue. You do not have to touch the python code, just the `catalog.yml`, like this:
```yml
example_job:
  inputs:
    flights:
      table: 'database_name.flights'
      schema: 'project_name.io.schemas.flights.SCHEMA'
      read_args:
        format: parquet
  outputs:
    aggregated_flights:
      table: 'database_name.aggregated_flights'
      schema: 'project_name.io.schemas.aggregated_flights.SCHEMA'
      write_args:
        format: parquet
        mode: overwrite
```
We still define the file format because when we write as a table, the table structure and metadata will be written in AWS Glue 
but the files will be written in an S3 bucket in the specified file format. You can only use Parquet or Delta.

## Setup Open Lineage
[Open Lineage](https://openlineage.io/) is a standard for metadata collection and sharing. 
It allows to track data lineage and data quality.

To run a job with Open Lineage, you need to pass the following parameters to your spark-submit command:

```bash
spark-submit \
--packages io.openlineage:openlineage-spark:0.18.0 \
--conf spark.extraListeners=io.openlineage.spark.agent.OpenLineageSparkListener \
--conf spark.openlineage.url=<OPENLINEAGE-URL> \
# other spark confs ...
path/to/your/job.py
# other job parameters ...
```

The open lineage urls to use depending on the environment : 
- dev: https://ol-dev.dktapp.cloud/api/v1/namespaces/pyspark/
- preprod: https://ol-preprod.dktapp.cloud/api/v1/namespaces/pyspark/
- prod: https://ol.dktapp.cloud/api/v1/namespaces/pyspark/

For instance, for a databricks jobs on dev environment, your task will look like this:

```bash
["--packages=io.openlineage:openlineage-spark:0.18.0",
"--conf","spark.extraListeners=io.openlineage.spark.agent.OpenLineageSparkListener",
"--conf","spark.openlineage.url=https://ol-dev.dktapp.cloud/api/v1/namespaces/pyspark/",
"s3://dev-dct-wksp-dps/dps-my-project-pyspark/jobs/1.0.0.dev0/example_job.py",
"--confs-dir","s3://dev-dct-wksp-dps/dps-my-project-pyspark/confs/1.0.0.dev0",
"--env","dev"]
```

## Add a new project environment
The `env` directory contains two kind of files
* `base.env` file contains the project level variables (project name, version, etc):
  * Variables in this file are always loaded when you execute a makefile target. 
* The env files, e€.g.* `{dev/ppd/prd/local}.env` contain environment-specific variables (CA repository, ECR registry, etc).
  * To load variables in this file in environment-specific targets, add `ENV=<env>` in the command, *e.g.*: `make publisers ENV=dev`
  
You might need to update the values of variables in this environment files. 
You might also want to create a new environment file in `env/` if you want to operate your project 
on another account (e.g., dedicated account).

Important note: you should review the information carefully to ensure the values are compatible with your environment and avoid copy-paste errors.

## Include new dependencies in the project

Dependencies are managed by [Poetry](https://python-poetry.org/) and its CLI to update the `pyproject.toml` file.

You can add production dependencies under the `[tool.poetry.dependencies]` with this command:

```bash
poetry add <PACKAGE>
```

If your dependency is only useful during development, you can add it under `[tool.poetry.group.dev.dependencies]` with this command:

```bash
poetry add -G dev <PACKAGE>
```



## Get the list of tasks supported by this project

You can read the Makefile of the project or use the following command:

```bash
make help
```

## Clean the project repository for reverting its state

There are various make tasks prefixed with 'clean-' to clean the project:
- **clean-docs**: Clean the documentation.
- **clean-caches**: Clean the projet caches.
- **clean-python**: Clean the Python caches.
- **clean-package**: Clean the project packages.
- **clean-install**: Clean the project installation.
- **clean-reports**: Clean the project generated reports.
- **cleaners**: Run all the cleaners

## Build the Python package used in the publication stage

We support the following package format: wheel (recommended) and sdist.

You can execute the following make tasks to build the package:
- **build-wheel**: Build the wheel package.
- **builders**: Run all the builders.

## Execute the package script locally from the command-line

The package script should be executed using Poetry with any configurations:

```bash
poetry run <PACKAGE_NAME> 
```

## Use the configuration files in this project (in `confs/`)

This project includ a `config.py` module, which contains a `ConfigLoader` class. 

This class provides a method for loading configuration files from a directory
using the OmegaConf library. 
It supports any path format supported by the `cloudpathlib` library.
The class support using a "base" environment. The configuration files from this environment will 
be shared by all other environments.

Here are 2 examples on how to use it 

**Example 1: Load from local dir**
To load  configuration files named 'config.yaml' located in directories:
* '/path/to/configs/base'
* '/path/to/configs/local'

use the following code:
```python
>>> from spark_training_workshop_pyspark.config import ConfigLoader
>>> loader = ConfigLoader(confs_dir='/path/to/configs', env='local', base_env='base')  
>>> config = loader.get('config.yaml')
```
Please note:
* that `config` will be a dictionary built by merging the dictionarry mapping 
  '/path/to/configs/base/config.yaml' and '/path/to/configs/local/config.yaml' files 
  (the latter overwriting the former in case of conflict).
* base_env is optional, it defaults to 'base'

**Example 2: Load from s3**
To load a configuration file named 'config.yaml' located in s3 path 's3://my-bucket/path/to/configs/dev',
without using a 'base' environment, use the following code:
```python
use the following code:
```python
>>> from spark_training_workshop_pyspark.config import ConfigLoader
>>> loader = ConfigLoader(confs_dir='s3://my-bucket/path/to/configs', env='dev')
>>> config = loader.get('config.yaml')
```

The returned `config` object is a merge of dictionnaries mapping 

## Use DBX to sync your local code or ship your job on databricks ?
### What is DBX ? 
[DBX](https://docs.databricks.com/dev-tools/dbx.html) is an extension of the databricks 
command line interface (CLI), which comes with a variety of functionalities for development, jobs run
and deployment. 

### How do we use it in this template ? 
In this template, we mainly use DBX to 
* sync your local src code with the corresponding github repositories loaded on databricks. 
* run your job directly on databricks with dbx workflows 
  (without passing by a docker image (to test your job before its publication).

### Setup DBX
To setup  databricks for the first time, run the following commands 
(You will need to pass a databricks token):
```bash 
dbx-setup
```

This target actually runs the following sub-targets:
* **dbx-configure**: 
  * Configures Databricks profile and environment.
  * Creates a profile named after the `DATABRICKS_USER` variable in `env/local.env` file.
  * `DATABRICKS_USER` must be your decathlon email (*e.g.* john.doe@decathlon.com)
* **dbx-login**:
  * Logs in to Databricks using the profile created in the previous step.
  * You will need to pass your databricks token (accessible from the "Settings" tab of your databricks workspace)
* **dbx-create-repo**:
  * Creates a repository on the databricks workspace for the current user, and links it to the project's github repository 
    (defined by the `GITHUB_FULL_URL` variable in `env/base.env` file

OK ! You're all set !
Now you can either sync your local code with your databricks repo, or run your job directly on databricks.

### Sync your local code with your databricks repo
This section explains how you can sync your local code with your databricks repo.
When your local code is sync with your databricks repo, all your local modifications (*e.g.* you add a new function)
will be automatically accessible from your databricks repo.

Please check the `notebooks/example_job.py` notebook to see how to load the modified code.

To sync your local modifications with your databricks repo, please run : 

```bash
make dbx-sync
```
Now you can edit your local code and see your changes in the remote databricks repo in realtime.
You can find an example on how to load the modified code in the `notebooks/example_job.py` notebook. 

**Best practices for dbx-sync**
If you work on databricks, you will have two git repositories (your local, and your databricks repo). 
You can trigger git commands (commit, push) from either of those two repos. 
To avoid git conflicts on files modified both on local and databricks, we *strongly recommend* the following approach:
* for all your files except notebooks: do and commit your modification from your local environment
* for your notebooks, do and commit your modifications from your databricks repo. 

### Run your jobs on databricks. 
This session explains how you can use dbx workflows to run your jobs on databricks, and tests it before its publication.

**IMPORTANT**: For the example job to run, don't forget to copy your inputs data to s3 with `make publish-s3-data ENV=dev`. 

You can launch your job execution directly from your local machine using dbx workflows.
To do that just edit the file `depl/dbx-workflows.yml` and add your job with a convenient params like the example bellow
```yml
build:
   python: "pip"
environments:
  default:
    workflows:
      - name: "example-job"
        spark_python_task:
          python_file: "file://src/dps-my-project-pyspark/jobs/example_job.py"
          parameters: ["--env", "dev", "--conf", "file:fuse://confs/"]
```

To run for instance the "example-job" workflow, just run the following command:

```bash
make dbx-execute WORKFLOW=example-job
```


## Change the version number of Poetry, Python, Package, ...

We provide several make tasks prefixed with 'bump-' in the Makefile:
- **bump-poetry**: change the version of Poetry in all the associated files.
- **bump-python**: change the version of Python in all the associated files.
- **bump-package**: change the version of the project package in all the associated files.

We recommend to pass the new version in the command-line to avoid stalled version numbers stored in files:

```bash
make bump-package PACKAGE_VERSION=3.2.1
```

## Check that the quality of the code fits the standard of Decathlon

Decathlon recommends to check the quality of your code to improve its maintenance and robustness.

You have access to several code checkers as make tasks prefixed with 'check-':
- **check-types**: Check the project types with mypy.
- **check-tests**: Check the project tests with pytest.
- **check-format**: Check the project code format with black and isort.
- **check-poetry**: Check the project pyproject.toml with poetry.
- **check-quality**: Check the project code quality with pylint.
- **check-coverage**: Check the project test coverage with coverage.
- **checkers**: Run all the checkers

Note: checkers are run automatically after each code push in the checkers GitHub workflow: `.github/workflows/checkers.yml`.

## Report the code quality of my project to SonarCloud

The project include a SonarCloud GitHub workflow to report the code quality: `.github/workflows/sonarcloud.yml`.

This GitHub workflow runs the make tasks prefixed with 'report-' after each code push to generate its reports:
- **report-tests**: Generate the project unit test reports.
- **report-quality**: Generate the project quality reports.
- **report-coverage**: Generate the project test coverage reports.
- **report-dependencies**: Generate the project dependencies reports.
- **reporters**: Run all the reporters.

By default, you must **trigger this workflow manually** (`on: workflow_dispatch`). \
If you want to trigger it automatically, you must update the workflow file to use another trigger (*e.g.*: `on: push`).

## Format the code automatically to fit to Decathlon standard

Decathlon is using [isort](https://pycqa.github.io/isort/) and [black](https://black.readthedocs.io/en/stable/) to format its import and source code respectively.

In VS Code, you can open the code-workspace workspace to configure your IDE automatically.

You can also run the following command before each commit:
- **format-imports**: Format the project imports with isort.
- **format-sources**: Format the project sources with black.
- **formaters**: Run all the formaters.

## Generate and deploy the documentation of the project on Github Pages

The project includes a GitHub workflow to build and publish Sphinx Documentation on Github Pages: `.github/workflows/sphinx.yml`.

You can run the make tasks prefixed with 'document-' to generate and preview the docs on your computer:
- **document-api**: Document the project API.
- **document-html**: Document the project in HTML.
- **documenters**: Run all the documenters.

You can edit your documentation either as [ReStructuredText](https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html) or in [Markdown](https://www.markdownguide.org/) (recommended).
