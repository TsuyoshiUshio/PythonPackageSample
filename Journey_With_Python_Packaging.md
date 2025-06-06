# Adventures in Python Packaging: Understanding Namespace Collisions

*June 6, 2025*

Python packaging is one of those topics that seems straightforward until you run into edge cases. In this post, I'll share my journey exploring Python packaging concepts, particularly focusing on namespace collisions. This is a common issue that can be confusing for developers working with multiple related packages.

## The Goal

I wanted to deeply understand Python packaging, specifically:

- How to properly manage Python packages
- Local development workflows
- Package naming conventions and structure
- Configuration options with pyproject.toml
- Handling duplicate namespaces
- Working with hyphens in package names
- Package references and dependencies

## The Setup: A Tale of Two Packages

To explore these concepts, I created a simple experimental setup with two packages that share the same namespace:

1. `azure-functions-agent-durable`
2. `azure-functions-agent-framework`

Both packages use the same namespace: `azurefunctions.agents`. This deliberate collision allows us to explore what happens when Python tries to import from packages with overlapping namespaces.

### Package 1: azure-functions-agent-durable

This package uses a more traditional approach to Python packaging:

```
azure-functions-agent-durable/
├── pyproject.toml
└── azurefunctions/
    ├── __init__.py
    └── agents/
        ├── __init__.py
        └── durable/
            ├── __init__.py
            └── durable.py
```

The core implementation is very simple:

```python
# filepath: azurefunctions/agents/durable/durable.py
def start_durable_task():
    return "Durable task started"
```

And the module exports this function:

```python
# filepath: azurefunctions/agents/durable/__init__.py
from .durable import start_durable_task
```

The package is configured with:

```toml
# pyproject.toml
[project]
name = "azure-functions-agent-durable"
version = "0.1.0"
description = "A minimal durable agent for Azure Functions."
authors = [{ name = "Tsuyoshi Ushio", email = "you@example.com" }]
license = { text = "MIT" }
readme = "README.md"
requires-python = ">=3.7"

[tool.setuptools.packages.find]
exclude = [
    'azurefunctions.agents',
    'azurefunctions', 'tests', 'samples'
    ]
```

### Package 2: azure-functions-agent-framework

This package uses a more modern approach:

```
azure-functions-agent-framework/
├── pyproject.toml
└── azurefunctions/
    └── agents/
        └── framework/
            ├── __init__.py
            └── client.py
```

Notice the lack of `__init__.py` files in the top-level directories.

Simple implementation:

```python
# filepath: azurefunctions/agents/framework/client.py
import helloworld

def start_agent():
    return "Agent started"
```

With module export:

```python
# filepath: azurefunctions/agents/framework/__init__.py
from .client import start_agent
```

And the package configuration:

```toml
# pyproject.toml
[project]
name = "azure-functions-agent-framework"
version = "0.1.0"
description = "A minimal agent framework for Azure Functions."
authors = [{ name = "Tsuyoshi Ushio", email = "you@example.com" }]
license = { text = "MIT" }
readme = "README.md"
requires-python = ">=3.7"

dependencies = [
    "example-helloworld"
]

[tool.setuptools.packages.find]
exclude = [
    'azurefunctions', 'tests', 'samples'
    ]
include = [
    'azurefunctions.agents.framework'
    ]
```

### The Sample Project

I created a simple project that tries to use both packages:

```python
# filepath: sample_project/sample_project/main.py
from azurefunctions.agents.durable import start_durable_task
from azurefunctions.agents.framework import start_agent

def main():
    print(start_durable_task())
    print(start_agent())

if __name__ == "__main__":
    main()
```

## The Problem: Running Into a Wall

When I tried to run the sample project, I hit an error:

```
$ python sample_project/main.py 
Traceback (most recent call last):
  File "/workspaces/packaging/sample_project/sample_project/main.py", line 2, in <module>
    from azurefunctions.agents.framework import start_agent
ImportError: cannot import name 'start_agent' from 'azurefunctions.agents' 
    (/workspaces/packaging/azure-functions-agent-durable/azurefunctions/agents/__init__.py)
```

The error is clear: Python could find the first package (`azure-functions-agent-durable`), but then when I tried to import from the second one (`azure-functions-agent-framework`), it was still looking in the first package's namespace.

## The Learning Journey

### Key Discovery #1: Two Approaches to Namespace Management

I discovered that there are two main approaches to handle namespaces in Python:

1. **Traditional approach** (used in `azure-functions-agent-durable`):
   - Uses `__init__.py` in every directory
   - Creates a traditional package structure

2. **Modern approach with namespace packages** (attempted in `azure-functions-agent-framework`):
   - Uses PEP 420 namespace packages
   - No `__init__.py` files in the shared namespace directories
   - Requires proper configuration with setuptools

### Key Discovery #2: The Role of pyproject.toml

The `pyproject.toml` file is crucial for modern Python packaging:

```toml
# Package dependencies
dependencies = [
    "example-helloworld"
]

# Package discovery configuration
[tool.setuptools.packages.find]
exclude = [
    'azurefunctions', 'tests', 'samples'
    ]
include = [
    'azurefunctions.agents.framework'
    ]
```

The `include` directive is especially important with namespace packages, as it tells setuptools exactly which packages to include.

### Key Discovery #3: Package Installation and Development Mode

After changing package structure, you need to reinstall in development mode:

```bash
pip install -e azure-functions-agent-durable/
pip install -e azure-functions-agent-framework/
```

This ensures that Python's import system sees the most up-to-date structure of your packages.

## Solutions to Namespace Collisions

Based on my experiments, I found several ways to solve the namespace collision problem:

### Solution 1: Use Different Namespaces

The simplest approach is to avoid sharing namespaces in the first place:

```
# Instead of azurefunctions.agents for both
azurefunctions_durable.agents
azurefunctions_framework.agents
```

### Solution 2: Proper Namespace Package Implementation

For intentionally shared namespaces, follow [PEP 420](https://www.python.org/dev/peps/pep-0420/) strictly:

- Remove `__init__.py` from shared namespace directories
- Configure setuptools correctly in all packages that share the namespace

### Solution 3: Package Consolidation

If the packages are closely related, consider consolidating them under a single package with clear submodules.

## Final Thoughts

Python packaging can be complex, but understanding the fundamentals helps you create clean, maintainable package structures. The main lessons I learned:

1. **Be consistent**: Choose one approach to namespace handling and stick with it
2. **Use modern tools**: `pyproject.toml` provides a clean way to define package metadata and dependencies
3. **Understand imports**: The Python import system has specific rules about how it resolves namespaces
4. **Test locally**: Development mode installation (`-e`) is essential for iterative development

By explicitly configuring which modules belong to which packages, we can avoid namespace collisions and create more robust Python libraries.

Have you run into similar Python packaging challenges? I'd love to hear about your experiences in the comments!

---

*This blog post is based on a practical exploration of Python packaging concepts. All code examples are available in the [GitHub repository](https://github.com/username/python-packaging-example).*
