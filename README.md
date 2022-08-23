# Trial Balloon

[*Trial Balloon*](https://en.wikipedia.org/wiki/Trial_balloon) is a Python helper library for easily generating and validating response data and documentation for Democracy Club APIs.

## Layout

This repository contains [Pydantic](https://pydantic-docs.helpmanual.io/) models in the `trial_balloon/models` directory that are the ultimate source of truth. These define the format and structure of the API responses. The `trial_balloon/schemas/` directory contains [JSON Schema](https://json-schema.org/) documentation generated from these models, and in `trial_balloon/examples/` you will find static JSON output, also generated with the help of these models and validated against them.

The `trial_balloon/fixtures/` directory contains the Python objects that produce these examples, but they can also be imported and used directly.

## Usage

Trial Balloon can be installed as a Python package and the models and fixtures can be imported and used directly in Python software or tests. Alternatively, for non-Python projects, the static JSON examples can be used directly. To make it easier to keep the examples current, maintainers may want to add this repository as a [git submodule](https://github.blog/2016-02-01-working-with-submodules/) to their own project, or regularly update as part of a continuous integration pipeline.

### As a Python package

Install via pip (or [`poetry add`](https://python-poetry.org/docs/basic-usage/#specifying-dependencies))
```bash
pip install -i https://test.pypi.org/simple/ trial-balloon
```

Then you can import fixtures and use them directly in tests. `FIXTURES_BY_NAME` is provided for convenience.


```python
import pytest
from trial_balloon.fixtures import FIXTURES_BY_NAME

from sample_client import client

@patch('sample_client.requests')
def test_call_api(fake_requests):
    fake_requests.get().json() = FIXTURES_BY_NAME['westminster'].dict()
    resp = client.get_postcode()
    assert resp['dates'] == []
```

If using a web framework that supports integration with Pydantic (such as [FastAPI](https://fastapi.tiangolo.com/) or Django via [Django-Ninja](https://django-ninja.rest-framework.com/)) you could also use these models directly in the application:

```python
from ninja import NinjaAPI
from trial_balloon.models.postcode_search import RootModel as PostcodeSearchResults

from polling_station.models import PostcodeDetails

api = NinjaAPI()

@api.get("/postcodes/{postcode}", response=PostcodeSearchResults)
def get_by_postcode(request, postcode: str):
    details = PostcodeDetails.objects.get(postcode==postcode)
    return details

```

### As static JSON files

You can download the example JSON files directly from Github, either individually or [in a bundle as a tagged archive](https://github.com/DemocracyClub/interview-test-brendan/tags), 

```bash
curl https://github.com/DemocracyClub/interview-test-brendan/archive/refs/tags/v0.1.0a.tar.gz | tar -zx interview-test-brendan-0.1.0a/trial_balloon/examples/ --strip-components=2
```

You could also clone the entire repository, or even add it as [a git submodule](https://git-scm.com/book/en/v2/Git-Tools-Submodules) inside your own project's repository

```bash
git submodule add git@github.com:DemocracyClub/interview-test-brendan.git trial_balloon
```

## Development

### Setup

Trial Balloon uses [Poetry](https://python-poetry.org/) for packaging and dependency management. Once you already have [Poetry itself installed](https://python-poetry.org/docs/#installation), you can run...

```bash
poetry install
```

...to install all required Python dependencies inside a [virtualenv](https://docs.python.org/3/library/venv.html), isolated from your system Python.

If your system has `make` available, there is a Makefile in the root of the repository with several helpful commands, but these are optional.

### Workflow

**To add a new field**

Find the model you need to update in `trial_balloon/models/` edit and make the changes there. Refer to the [Pydantic usage docs](https://pydantic-docs.helpmanual.io/usage/models/), if needed. Once you're satisfied, in the project root you can run:

```bash
make schemas   # To update schemas
make examples  # To update examples
make all       # To update both
```

**To add or change a fixture**

Find the fixture you want to edit (or create a new one) in `trial_balloon/fixtures/`. Once you've made the changes, you can run...

```bash
make examples
```

to re-generate the JSON examples, including your own new one.

**Tidy up**

Review your changes with `git diff`, you can also run

```bash
make format # To automatically format your Python code.
make lint   # To run static analysis tools and check your code for glitches.
make test   # To run tests using your models/fixtures against a sample client app.
```

*Note that the local test suite passing, doesn't guarantee your changes are non-breaking for all possible consumers of this library.* Be sure to tag and version any breaking changes appropriately (see below).

Once you're happy with the changes, make sure to commit both the modified Python code and the static JSON folders.

### Publish

#### Prerequisites

You'll need to register an accont and generate an API token for PyPI or [Test PyPI](https://test.pypi.org/manage/account/#api-tokens) (the steps below show test PyPI, adapted from [this SO answer](https://stackoverflow.com/q/68882603/845210)) to configure your local environment:

```bash
poetry config repositories.testpypi https://test.pypi.org/legacy/
poetry config pypi-token.testpypi pypi-TOKEN...
```

#### Creating a release

Update the version string in `pyproject.toml` Please follow [semantic versioning](https://semver.org/): if you have made breaking changes, increment the major version number. Add a git tag for the new verson:

```bash
git tag 'v0.1.1'
git push origin --tags
```

Then, run

```bash
make dist
poetry publish -r testpypi
```

to publish the new version to PyPI.

