from connector.cli import run_integration

from okta.integration import integration


def main():
    run_integration(integration)


if __name__ == "__main__":
    main()
