FROM public.ecr.aws/g3l5j2q0/lumos/on-prem-agent-base:latest AS build-agent

COPY ./okta ./okta

RUN pip3 install "connector-py[dev]"

RUN cd okta && pip3 install -e ".[all]"

RUN pip3 install botocore

ENTRYPOINT ["connector", "compile-on-prem", "--connector-root-module-dir", "./okta/okta", "--app-id", "okta", "--output-directory", "./build/compiled/okta"]