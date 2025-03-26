FROM public.ecr.aws/g3l5j2q0/lumos/on-premise-agent-no-connectors:latest

COPY ./compiled/compiled/okta/bundled/okta-0.1.0.tar.gz ./agent/connectors/

COPY ./settings.toml ./agent/settings.toml