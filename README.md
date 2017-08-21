[OpenFisca](https://doc.openfisca.org/) helps you turn fiscal and social law into software.

`OpenFisca-Core` is the computation engine that is used by country packages to model tax and benefit systems.

### [More information](https://openfisca.org)

### [Documentation](https://doc.openfisca.org/)

### [Explore a full model](https://legislation.openfisca.fr)

### [Bootstrap a new country package template](https://github.com/openfisca/country-template)


## Environment

This package requires Python 2.7

## Installation

**If you're developing your own country package, you don't need to explicitly install `OpenFisca-Core`.** It just needs to appear [in your package dependencies](https://github.com/openfisca/openfisca-france/blob/18.2.1/setup.py#L53). Installing `OpenFisca-Core` is only needed if you want to contribute changes to the _core computation engine_, not a model of a specific country.

If you want to contribute to OpenFisca-Core itself, welcome! To install it locally in development mode:

```bash
git clone https://github.com/openfisca/openfisca-core.git
cd openfisca-core
pip install --editable ".[test]"
```

## Testing

```sh
make test
```

## Serving the API

OpenFisca-Core provides a Web-API. To run it with the mock country package `openfisca_country_template`, run:

```sh
COUNTRY_PACKAGE=openfisca_country_template gunicorn "openfisca_web_api_preview.app:create_app()" --bind localhost:5000 --workers 3
```

The `--workers k` (with `k >= 3`) option is necessary to avoid [this issue](http://stackoverflow.com/questions/11150343/slow-requests-on-local-flask-server). Without it, AJAX requests from Chrome sometimes take more than 20s to process.

### Tracker

The OpenFisca Web API comes with an [optional tracker](https://github.com/openfisca/tracker) which allows you to measure the usage of the API.
