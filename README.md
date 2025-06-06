# Python Packaging Example

This repository demonstrates common Python packaging concepts and potential issues, particularly focusing on namespace package collisions.

📝 **[Read the detailed blog post: "Adventures in Python Packaging: Understanding Namespace Collisions"](Journey_With_Python_Packaging.md)**

## Project Structure

```
packaging/
├── azure-functions-agent-durable/     # Package 1
│   ├── pyproject.toml
│   └── azurefunctions/
│       └── agents/
│           └── durable/
│               ├── __init__.py
│               └── durable.py
│
├── azure-functions-agent-framework/   # Package 2
│   ├── pyproject.toml
│   └── azurefunctions/
│       └── agents/
│           └── framework/
│               ├── __init__.py
│               └── client.py
│
└── sample_project/                    # Example consumer project
    ├── pyproject.toml
    └── sample_project/
        ├── __init__.py
        └── main.py
```

## The Namespace Collision Problem

This project demonstrates a common issue with Python packaging: **namespace collisions**. The two packages `azure-functions-agent-durable` and `azure-functions-agent-framework` both use the same namespace: `azurefunctions.agents`.

When Python tries to import modules from these packages:
1. It can only resolve one package for a given namespace path
2. This can lead to import errors when trying to access functions that exist in one package from the namespace loaded from another package

## How to Run

The sample project attempts to import modules from both packages:

```python
# From sample_project/main.py
from azurefunctions.agents.durable import start_durable_task
from azurefunctions.agents.framework import start_agent
```

Running this code demonstrates the namespace collision:

```bash
$ python sample_project/main.py
# Results in an ImportError
```

## Solutions to Namespace Collisions

### Option 1: Use Different Namespaces

Modify the packages to use separate, non-overlapping namespaces:

```
azurefunctions_durable.agents
azurefunctions_framework.agents
```

### Option 2: Use Proper Namespace Packages

If sharing namespaces is intentional, follow [PEP 420](https://www.python.org/dev/peps/pep-0420/) to create proper namespace packages:
- Remove `__init__.py` from the shared namespace directories
- Use appropriate setup tools configuration

### Option 3: Merge Related Packages

If the packages are closely related, consider combining them under a single package with clear submodule organization.

## Learning Objectives

This repository helps you understand:
- How Python package namespaces work
- Common issues with namespace collisions
- Package distribution and importing mechanisms
- Best practices for organizing related Python packages

For a detailed walkthrough of what I learned during this project, see the [Journey with Python Packaging](Journey_With_Python_Packaging.md) blog post.

## Development Setup

1. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install the packages in development mode:
   ```bash
   pip install -e azure-functions-agent-durable/
   pip install -e azure-functions-agent-framework/
   pip install -e sample_project/
   ```

## License

[MIT](LICENSE)
