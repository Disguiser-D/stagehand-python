# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the Python implementation of Stagehand, an AI browser automation framework that enables developers to combine traditional browser automation code with natural language AI instructions. It provides a Python SDK for browser automation with support for both local and remote (Browserbase) environments.

## Development Commands

### Code Quality and Formatting
- Format code and apply lints: `./format.sh` or `bash format.sh`
  - Runs Black formatting on `stagehand/` directory
  - Applies Ruff autofixes including import sorting
  - Checks for remaining Ruff issues
- Check types: `mypy stagehand/` (if mypy is installed)
- Manual linting: `ruff check stagehand/`

### Testing
- Run all tests with coverage: `./run_tests.sh` or `python -m pytest tests/ -v --cov=stagehand --cov-report=term --cov-report=html`
- Run specific test categories using markers:
  - Unit tests: `pytest -m unit`
  - Integration tests: `pytest -m integration`
  - E2E tests: `pytest -m e2e`
  - Local tests: `pytest -m local`
  - API tests: `pytest -m api`
  - Regression tests: `pytest -m regression`
- Run single test file: `pytest tests/path/to/test_file.py -v`
- Run with specific verbosity: `pytest tests/ -v -s`

### Package Management
- Install in development mode: `pip install -r requirements.txt` (uses editable install `-e .[dev]`)
- Check if package is installed: `pip list | grep stagehand`

## Core Architecture

### Main Components

1. **Stagehand Class** (`stagehand/main.py`): Main entry point and orchestrator
   - Manages browser connections (local/remote)
   - Handles LLM client initialization
   - Provides the `page` property via LivePageProxy for multi-tab support
   - Supports both API and local execution modes

2. **StagehandPage** (`stagehand/page.py`): Core browser page interface
   - Provides `act()`, `extract()`, and `observe()` methods
   - Handles DOM manipulation and element interaction
   - Integrates with handler classes for operation execution

3. **Handlers** (`stagehand/handlers/`): Process-specific operation handlers
   - `ActHandler`: Executes browser actions (click, type, etc.)
   - `ExtractHandler`: Extracts structured data using Pydantic schemas
   - `ObserveHandler`: Observes page elements and returns selectors
   - `CUAHandler`: Computer Use Agent handler for vision-based interactions

4. **Agent** (`stagehand/agent/`): Autonomous task execution
   - Supports OpenAI and Anthropic computer use agents
   - Handles multi-step workflows with provider-specific implementations

5. **LLM Integration** (`stagehand/llm/`): Language model client management
   - Uses litellm for multi-provider support
   - Handles model-specific prompt formatting and responses
   - Tracks token usage and inference metrics

### Environment Support

- **BROWSERBASE**: Remote browser execution via Browserbase API
- **LOCAL**: Local browser automation using Playwright

### Configuration System

Configuration is managed through `StagehandConfig` class with support for:
- Environment variables (`.env` file support)
- Runtime overrides via constructor parameters
- Model-specific settings (API keys, client options)
- Browser launch options for local execution

## Testing Structure

- **Unit tests** (`tests/unit/`): Test individual components in isolation
- **Integration tests** (`tests/integration/`): Test component interactions
- **E2E tests** (`tests/e2e/`): Full workflow testing
- **Regression tests** (`tests/regression/`): Prevent known issues from reoccurring
- **Mocks** (`tests/mocks/`): Mock implementations for testing

## Key Dependencies

- **playwright**: Browser automation engine
- **pydantic**: Data validation and schema definition
- **httpx**: Async HTTP client for API communication
- **litellm**: Multi-provider LLM client
- **browserbase**: Remote browser service integration
- **rich**: Enhanced terminal formatting for logs