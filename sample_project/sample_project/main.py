from azurefunctions.agents.durable import start_durable_task
from azurefunctions.agents.framework import start_agent


def main():
    print(start_durable_task())
    print(start_agent())

if __name__ == "__main__":
    main()