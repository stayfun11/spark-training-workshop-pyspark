# https://www.gnu.org/software/make/manual/make.html

## ENVS

# Default environment
## - use: make ENV=prod [target]
ENV ?= local
$(info [Makefile] Loading variables from env/base.env and env/$(ENV).env files ...)
## VARS

include env/base.env
include env/$(ENV).env


isset-%: ## Test if variable % is set or exit with error
	# @: $(if $(value $*),,$(error Variable $* is not set))

## HELP

.DEFAULT_GOAL:=help

help: ## Display the help menu.
	@grep -h "\#\#" $(MAKEFILE_LIST)

## INITIALIZERS
git-init:  ## Init the local git repo, create the distant github repo and pushed the initial project files.
	git init
	gh auth login --hostname=github.com
	gh repo create --private --source=. dktunited/$(GITHUB_REPOSITORY)
	git add .
	git commit -m "initial commit"
	git branch -M main
	git push -u origin main
	@echo "\nAdded, commit and pushed initial project files to branch 'main' of 'dktunited/$(GITHUB_REPOSITORY)'"

create-sonarcloud-project:  ## Create a SonarCloud project. Requires``SONARCLOUD_REPOSITORY`` and ``SONARCLOUD_TOKEN`` env variables.
	@curl -X POST "https://$(SONARCLOUD_TOKEN)@sonarcloud.io/api/projects/create" \
	  --data "organization=dktunited&name=$(SONARCLOUD_REPOSITORY)&project=dktunited_$(SONARCLOUD_REPOSITORY)"

# NOTE: to be done after gh-pages branch is created by Github Actions
gh-pages-init: ## Init the gh-pages branch.
	gh api -X "POST" "/repos/dktunited/$(GITHUB_REPOSITORY)/pages" --input=.github/gh-pages/config.json

sphinx-url-init:
	$(eval SPHINX_DOCUMENTATION_URL=$(shell gh api "/repos/dktunited/$(PROJECT_NAME)/pages" --jq '.html_url'))
	sed -i.bak "s?SPHINX_DOCUMENTATION_URL?$(SPHINX_DOCUMENTATION_URL)?" README.md && rm README.md.bak

## BUILDERS
build-%: ## Build package for format %.
	poetry build --format=$*

builders: build-wheel ## Run all the builders.

## CLEANERS

clean-docs: ## Clean the documentations.
	rm -rf docs/build/
	rm -rf docs/source/_api/

clean-caches: ## Clean the project caches.
	rm -f .coverage
	rm -rf .hypothesis/
	rm -rf .mypy_cache/
	rm -rf .pytest_cache/

clean-python: ## Clean the Python caches.
	find . -type f -name '*.py[co]' -delete
	find . -type d -name __pycache__ -delete

clean-package: ## Clean the project package.
	rm -rf dist/

clean-install: ## Clean the project installation.
	rm -rf .venv/

clean-reports: ## Clean the project generated reports.
	rm -rf reports/*.*

cleaners: clean-docs clean-caches clean-python clean-package clean-install clean-reports ## Run all the cleaners.

## INSTALLERS

install-dev: ## Install the project in dev mode.
	poetry install --all-extras

install-prod: ## Install the project in prod mode.
	poetry install --without=dev

## BUMPERS

## - Poetry

bump-poetry-githubactions: isset-POETRY_VERSION ## Bump the poetry version of GitHub Workflow Actions.
	sed -i.bak 's/^  poetry-version: { default: ".*", \(.*\) }/  poetry-version: { default: "$(POETRY_VERSION)", \1 }/' .github/actions/install-project/action.yml && rm .github/actions/install-project/action.yml.bak

## - Python

bump-python-project: isset-PYTHON_VERSION ## Bump the python version of the project.
	sed -i.bak 's/^python = .*/python = "^$(PYTHON_VERSION)"/' pyproject.toml && rm pyproject.toml.bak

bump-python-sonarcloud: isset-PYTHON_VERSION ## Bump the python version of Sonar Cloud properties.
	sed -i.bak 's/^sonar.python.version=.*/sonar.python.version=$(PYTHON_VERSION)/' sonar-project.properties && rm sonar-project.properties.bak

bump-python-githubactions: isset-PYTHON_VERSION ## Bump the python version of GitHub Workflow Actions.
	sed -i.bak 's/^  python-version: { default: ".*", \(.*\) }/  python-version: { default: "$(PYTHON_VERSION)", \1 }/' .github/actions/install-project/action.yml && rm .github/actions/install-project/action.yml.bak

## - Package

bump-package-env: ## Bump the PACKAGE_VERSION environment variable.
	$(eval PACKAGE_VERSION=$(shell cat VERSION))
	sed -i.bak 's/^PACKAGE_VERSION=.*/PACKAGE_VERSION=$(PACKAGE_VERSION)/' env/base.env && rm env/base.env.bak

bump-package-project: ## Bump the package version of the project.
	sed -i.bak 's/^version = .*/version = "$(shell cat VERSION)"/' pyproject.toml && rm pyproject.toml.bak

bump-package-sphinxdocs: ## Bump the package version of the documentation.
	sed -i.bak 's/^version = .*/version = "$(shell cat VERSION)"/' docs/source/conf.py && rm docs/source/conf.py.bak

bump-package-sonarcloud: ## Bump the package version of Sonar Cloud properties.
	sed -i.bak 's/^sonar.projectVersion=.*/sonar.projectVersion=$(shell cat VERSION)/' sonar-project.properties && rm sonar-project.properties.bak

# - Bumpers

bump-poetry: bump-poetry-githubactions ## Run all the poetry bumpers

bump-python: bump-python-project bump-python-sonarcloud bump-python-githubactions ## Run all the python bumpers

bump-package: bump-package-env bump-package-project bump-package-sphinxdocs bump-package-sonarcloud ## Run all the package bumpers

## CHECKERS

check-types: ## Check the project code types with mypy.
	poetry run mypy src/

check-tests: ## Check the project unit tests with pytest.
	poetry run pytest -n auto src/tests/

check-format: ## Check the project code format with isort and black.
	poetry run isort --check src/
	poetry run black --check src/

check-poetry: ## Check the project pyproject.toml with poetry.
	poetry check

check-quality: ## Check the project code quality with pylint.
	poetry run pylint src/

check-coverage: ## Check the project test coverage with coverage.
	poetry run pytest -n auto --cov=. src/tests/

checkers: check-types check-format check-poetry check-quality check-coverage ## Run all the checkers.

## REPORTERS

report-tests: ## Generate the project unit test report.
	poetry run pytest -n auto --junitxml=reports/pytest.xml src/tests/

report-quality: ## Generate the project quality report.
	poetry run pylint --output-format=parseable src/ | tee reports/pylint.txt

report-coverage: ## Generate the project test coverage report.
	poetry run pytest -n auto --cov=. --cov-report=xml:reports/coverage.xml src/tests/

report-dependencies: ## Generate the project dependencies report.
	poetry export --without-hashes --output=reports/requirements.txt

reporters: report-tests report-quality report-coverage report-dependencies ## Run all the reporters.

## FORMATTERS

format-imports: ## Format the project imports with isort.
	poetry run isort src/

format-sources: ## Format the project sources with black.
	poetry run black src/

formatters: format-imports format-sources ## Run all the formatters.

# DOCUMENTERS

document-api: ## Document the project API.
	poetry run sphinx-apidoc -o docs/source/_api src/$(PROJECT_NAME_UNDERSCORES)/

document-%: ## Document the project in format %.
	poetry run sphinx-build -b $* docs/source docs/build

documenters: bump-package clean-docs document-api document-html ## Run all the documenters.

# PUBLISHERS

## - Configurations (S3)

publish-s3-data: isset-S3_WORKSPACE ## Push the configurations to the S3 bucket.
	aws s3 sync data/inputs/ $(S3_DATA_DIR)

publish-s3-conf: isset-S3_WORKSPACE ## Push the configurations to the S3 bucket.
	aws s3 sync confs/base/ $(S3_CONFS_DIR)/$(PACKAGE_VERSION)/base/
	aws s3 sync confs/$(ENV)/ $(S3_CONFS_DIR)/$(PACKAGE_VERSION)/$(ENV)/

## - Jobs (entrypoint for spark-submit)
publish-s3-jobs: isset-S3_WORKSPACE
	aws s3 sync src/$(PROJECT_NAME_UNDERSCORES)/jobs/ $(S3_JOBS_DIR)/$(PACKAGE_VERSION)

publish-s3: publish-s3-conf publish-s3-jobs

## - AWS Code Artifact (CA)

publish-ca-token: isset-AWS_ACCOUNT ## Get an authorization token from Code Artifact
	$(eval CA_TOKEN=$(shell aws codeartifact get-authorization-token --region=$(AWS_REGION) \
		--domain=$(CA_DOMAIN) --domain-owner=$(CA_OWNER) --query authorizationToken \
		--output text --duration-seconds 900)) # minimum duration for the CI/CD

publish-ca-package: isset-AWS_ACCOUNT publish-ca-token ## Publish the package to Code Artifact.
	@poetry run twine upload --repository-url=$(CA_URL) --username=$(CA_USER) --password=$(CA_TOKEN) dist/*


delete-ca-package: isset-AWS_ACCOUNT publish-ca-token ## Delete the current version of package from Code Artifact, if it exists.
	@if aws codeartifact list-packages \
			--domain $(CA_DOMAIN) \
			--domain-owner $(AWS_ACCOUNT) \
			--repository $(CA_REPOSITORY) \
			--format pypi 2>/dev/null | grep -q "$(PACKAGE_NAME)" ; then \
  		aws codeartifact delete-package-versions --no-cli-pager \
		--domain $(CA_DOMAIN) \
		--domain-owner $(AWS_ACCOUNT) \
		--repository $(CA_REPOSITORY) \
		--format pypi \
		--package $(PACKAGE_NAME) \
		--versions $(PACKAGE_VERSION); \
	else \
	  echo "Package $(PACKAGE_NAME) does not exist on $(CA_REPOSITORY). Skipping deletion step."; \
	fi

add-ca-repository: publish-ca-token ## Configure poetry to install dependencies from Code Artifact repository.
	poetry source add --priority=supplemental $(CA_DOMAIN)  $(CA_URL)/simple
	poetry config http-basic.$(CA_DOMAIN) $(CA_USER) $(CA_TOKEN)

## AWS Elastic Container Registry (ECR)

publish-ecr-login: isset-AWS_ACCOUNT ## Login with Docker CLI to Elastic Container Registry.
	aws ecr get-login-password --region $(AWS_REGION) | docker login --username $(ECR_USER) --password-stdin $(ECR_HOST)

publish-ecr-config: isset-AWS_ACCOUNT publish-ca-token ## Configure the docker image to work with Code Artifact.
	cp docker/netrc.in docker/.netrc # don't commit!
	sed -i.bak 's/MACHINE/$(CA_HOST)/' docker/.netrc && rm docker/.netrc.bak
	sed -i.bak 's/LOGIN/$(CA_USER)/' docker/.netrc && rm docker/.netrc.bak
	@sed -i.bak 's/PASSWORD/$(CA_TOKEN)/' docker/.netrc && rm docker/.netrc.bak

publish-ecr-build: isset-AWS_ACCOUNT publish-ecr-config ## Build the docker image locally using Code Artifact package.
	docker buildx build \
		-t $(DOCKER_IMAGE) \
		--platform=$(DOCKER_BUILD_PLATFORMS) \
		--build-arg INDEX_URL=$(CA_URL_SIMPLE) \
		--build-arg PACKAGE_VERSION=$(PACKAGE_VERSION) \
		docker/

publish-ecr-image: isset-AWS_ACCOUNT publish-ecr-login ## Publish the docker image with a tag to Elastic Container Registry. NOT to be run on Github Actions, since on GA git is not configured.
	$(eval GIT_SHORT_SHA=$(shell git rev-parse --short HEAD))
	docker tag $(DOCKER_IMAGE) $(ECR_IMAGE_NAME):$(GIT_SHORT_SHA)
	docker tag $(DOCKER_IMAGE) $(ECR_IMAGE_NAME):$(PACKAGE_VERSION)
	docker tag $(DOCKER_IMAGE) $(ECR_IMAGE_NAME):latest
	docker push $(ECR_IMAGE_NAME) --all-tags


publishers-summary:
	$(eval GIT_SHORT_SHA=$(shell git rev-parse --short HEAD))
	@echo "PUBLISHERS SUMMARY"
	@echo "* Docker image URIs:"
	@echo "\t* $(ECR_IMAGE_NAME):$(PACKAGE_VERSION)"
	@echo "\t* $(ECR_IMAGE_NAME):$(GIT_SHORT_SHA)"
	@echo "\t* $(ECR_IMAGE_NAME):latest"
	@echo "* S3 confs dir: $(S3_CONFS_DIR)/$(PACKAGE_VERSION)"
	@echo "\t* base confs dir: $(S3_CONFS_DIR)/$(PACKAGE_VERSION)/base"
	@echo "\t* env confs dir: $(S3_CONFS_DIR)/$(PACKAGE_VERSION)/$(ENV)"
	@echo "* S3 jobs dir: $(S3_JOBS_DIR)/$(PACKAGE_VERSION)"

publishers: bump-package delete-ca-package clean-package build-wheel publish-ca-package publish-ecr-build publish-ecr-image publish-s3-conf publish-s3-jobs publishers-summary ## Run all the publishers.

# DEPLOYMENT

# EMR Deployment

deploy-on-emr: isset-AWS_ACCOUNT  ## Deploy the job on EMR - variables EMR_CLUSTER_ID and JOB_FILE must be passed at run time (e.g. make deploy-on-emr ENV=dev EMR_CLUSTER_ID=j-2X3X4X5X6X7X8 JOB_FILE=my_job.py)
	$(eval STEPS=$(shell echo '\
	Type=CUSTOM_JAR,\
	Name=\"$(PROJECT_NAME)\",\
	Jar=\"command-runner.jar\",\
	ActionOnFailure=CONTINUE,\
	Args=[\
	\"spark-submit\",\"--deploy-mode\",\"cluster\",\
	\"--conf\",\"spark.executorEnv.YARN_CONTAINER_RUNTIME_TYPE=docker\",\
	\"--conf\",\"spark.executorEnv.YARN_CONTAINER_RUNTIME_DOCKER_IMAGE=$(ECR_IMAGE_NAME):$(PACKAGE_VERSION)\",\
	\"--conf\",\"spark.yarn.appMasterEnv.YARN_CONTAINER_RUNTIME_TYPE=docker\",\
	\"--conf\",\"spark.yarn.appMasterEnv.YARN_CONTAINER_RUNTIME_DOCKER_IMAGE=$(ECR_IMAGE_NAME):$(PACKAGE_VERSION)\",\
	\"$(S3_JOBS_DIR)/$(PACKAGE_VERSION)/$(JOB_FILE)\",\
	\"--confs-dir=$(S3_CONFS_DIR)/$(PACKAGE_VERSION)\",\
	\"--env=$(ENV)\",\
	\"--spark-master=yarn\"]' | tr -d '[:space:]'))
	aws emr add-steps --no-cli-pager \
		--cluster-id $(EMR_CLUSTER_ID) \
		--steps $(STEPS)


## DBX
dbx-sync:
	poetry run dbx sync repo \
	  --source=. \
	  --include=src/ \
	  --include=notebooks/ \
	  --include=confs/ \
	  --profile=$(DATABRICKS_USER) \
	  --dest-repo=$(DATABRICKS_REPOSITORY)

dbx-execute: isset-DATABRICKS_CLUSTER ## Run a workflow on Databricks. Needs to pass a `WORKFLOW` variable (e.g. make dbx-execute WORKFLOW=my_workflow)
	poetry run dbx execute \
		--deployment-file depl/dbx-workflows.yml \
		--cluster-name=$(DATABRICKS_CLUSTER) \
		$(WORKFLOW)

dbx-configure:  ## Configure Databricks profile and environment.
	poetry run dbx configure --profile $(DATABRICKS_USER) --environment default

dbx-login: isset-DATABRICKS_INSTANCE ## Login to Databricks. You will need to pass your token.
	poetry run databricks configure --host=https://$(DATABRICKS_INSTANCE) --profile $(DATABRICKS_USER) --token

dbx-create-repo: isset-DATABRICKS_USER isset-DATABRICKS_REPOSITORY ## Create a Databricks repo.
	poetry run databricks repos create \
	  --url=$(GITHUB_FULL_URL) \
	  --provider=github \
	  --path="/Repos/$(DATABRICKS_USER)/$(DATABRICKS_REPOSITORY)" \
	  --profile=$(DATABRICKS_USER)

dbx-setup: dbx-configure dbx-login dbx-create-repo ## Setup Databricks repo.