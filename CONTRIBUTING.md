# Contributing to Claude Connect

Thank you for your interest in contributing to Claude Connect! This document provides guidelines and instructions for contributing to this project.

## Code of Conduct

Please read and follow our [Code of Conduct](CODE_OF_CONDUCT.md) to foster an open and welcoming environment.

## Getting Started

1. **Fork the repository** on GitHub.
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR-USERNAME/claude-connect.git
   cd claude-connect
   ```
3. **Set up the development environment**:
   ```bash
   # Create and activate a virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   
   # Install dependencies
   pip install -r requirements.txt
   ```
4. **Create a branch** for your changes:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Workflow

1. **Make your changes** in your feature branch.
2. **Write or update tests** for your changes.
3. **Run tests** to ensure they pass:
   ```bash
   pytest
   ```
4. **Format your code** using appropriate tools (e.g., black, isort).
5. **Commit your changes** with a clear commit message:
   ```bash
   git commit -m "Add feature: your feature description"
   ```
6. **Push your branch** to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```
7. **Create a Pull Request** from your fork to the main repository.

## Pull Request Guidelines

* Ensure your PR addresses a specific issue. If an issue doesn't exist, create one first.
* Include a clear description of the changes and their purpose.
* Make sure all tests pass.
* Update documentation if necessary.
* Keep PRs focused on a single topic to make review easier.

## Adding New Features

### Adding a New Resource Type

1. Define the resource type in `resources.json`.
2. Implement the handler function in `main.py`.
3. Add tests for the new resource type.

### Adding a New Tool

1. Implement the tool handler function in `main.py`.
2. Add the tool to the capabilities list in the `capabilities_list_handler` function.
3. Add tests for the new tool.

### Adding a New Prompt Template

1. Add the prompt template to `prompts.json`.
2. Add tests for the new prompt template.

## Code Style

* Follow PEP 8 guidelines for Python code.
* Use type hints where appropriate.
* Write clear docstrings for functions and classes.
* Keep functions focused on a single responsibility.

## Testing

* Write tests for all new features and bug fixes.
* Ensure existing tests continue to pass.
* Use pytest fixtures for common test setup.

## Documentation

* Update the README.md if your changes affect the user experience.
* Document new features, configuration options, or API changes.
* Include examples where appropriate.

## License

By contributing to Claude Connect, you agree that your contributions will be licensed under the project's [MIT License](LICENSE).

## Questions?

If you have any questions or need help, please open an issue or reach out to the maintainers.

Thank you for contributing to Claude Connect!
