# Lumos Example Okta Connector

## About
This repo contains an Okta connector built using the [Lumos Connector SDK](https://pypi.org/project/connector-py/#description)

## Getting Started

After cloning this repo, create a new python environment

`python -m venv .venv`

Activate the environment

`source .venv/bin/activate`

Install the Lumos Connector SDK with development dependencies

`pip install "connector-py[dev]"`

Install the connector

`cd okta && pip install -e ".[all]"`

At this point you should be able to run a command like

`okta info` and see a command output in the console.

## Using this project

This project can be used as an example of how to build a connector or to experiment with a working connector. 
See the [Developer Docs](https://developers.lumos.com/docs/connector-sdk-1) for more information about building
and using connectors.

To run this connector within an agent, ensure you have docker installed on your system. Then run

`./scripts/run_compile_in_docker.sh`

Then run 

`docker build -f test-agent.Dockerfile . --progress=plain --platform linux/amd64 -t test-agent` 

This will build a docker image based on the lumos agent docker image that includes the test okta custom connector. To run the image, run

`docker run -e LUMOS_ON_PREMISE_AGENT_API_KEY={your_api_key} test-agent`