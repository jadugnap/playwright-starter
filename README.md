# Python Playwright BDD Gherkin Test Suite

A starter repository for running Behavior-Driven Development (BDD) UI tests using **Python**, **Behave** (Gherkin syntax), and **Playwright**, integrated with **CircleCI** for continuous integration.

## Repository Structure

```
├── .circleci/
│   └── config.yml          # CircleCI workflow configuration
├── features/
│   ├── environment.py      # Playwright browser lifecycle hooks
│   ├── search.feature      # Gherkin BDD feature files
│   └── steps/
│       └── web_steps.py    # BDD step definitions utilizing Playwright
├── requirements.txt        # Python project dependencies
└── README.md               # Setup and usage guide
```

---

## Local Setup

### 1. Prerequisites
Ensure you have **Python 3.8+** installed.

### 2. Create a Virtual Environment (with pyenv-virtualenv)
```bash
# Create the virtualenv
pyenv virtualenv 3.11.0 playwright-bdd

# Activate the virtualenv
pyenv activate playwright-bdd
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Install Playwright Browsers
Download the required Playwright browser binaries:
```bash
playwright install chromium
```

---

## Running Tests

Run all BDD scenarios using Behave:
```bash
behave
```

### Environment Variables
You can configure test behavior using environment variables:

- **`PLAYWRIGHT_HEADLESS`**: Run browser in headless or headed mode. Defaults to `true`.
  ```bash
  PLAYWRIGHT_HEADLESS=false behave
  ```
- **`BROWSER`**: Specify the browser engine (`chromium`, `firefox`, or `webkit`). Defaults to `chromium`.
  ```bash
  BROWSER=firefox behave
  ```

---

## CircleCI Integration

This repository includes a pre-configured `.circleci/config.yml` that:
1. Provisions a Python environment.
2. Caches dependencies for faster build times.
3. Installs Playwright browser binaries and system OS dependencies (`playwright install --with-deps chromium`).
4. Executes the BDD test suite.
5. Captures and uploads failure screenshots as CircleCI build artifacts if any scenario fails.
