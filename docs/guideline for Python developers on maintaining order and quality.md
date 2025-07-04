## 1\. Project Initialization

Always start your projects with a structured approach to ensure consistency and maintainability from day one.

  * **Initialize with Rye:** Use `rye init` to set up the standard project structure.

    ```
    my_project/
    ├── src/          # Package code
    ├── tests/        # Tests
    ├── .gitignore
    └── pyproject.toml  # Dependency configuration
    ```

  * **Use UV for Installations:** Replace `pip` with `uv` for significantly faster dependency management.

    ```bash
    uv pip install -r requirements.txt # Up to 100x faster than pip
    ```

-----

## 2\. Code Organization

Organize your codebase logically to enhance readability and navigability for all developers.

  * **Group by Functionality (Scope-based):** Structure your `src/` directory by functional modules.

    ```
    src/
    ├── payments/   # All payment logic
    │   ├── service.py
    │   └── models.py
    ├── search/     # Search module
    └── utils/      # Common utilities
    ```

  * **Prohibit "Junk" Files:** Ensure your `.gitignore` file includes common temporary and experimental files to keep your repository clean.

    `.gitignore` should include entries like `*.tmp`, `*.bak`, `_experimental_*`.

-----

## 3\. Automated Code Checks

Automate code quality checks using Ruff and pre-commit hooks to catch issues early in the development cycle.

  * **Configure Ruff in `pyproject.toml`:** Set up Ruff to enforce comprehensive linting and formatting rules.

    ```toml
    [tool.ruff]
    lint.select = ["ALL"]       # Check all rules
    lint.unused-imports = true  # Detect unused imports
    format.quote-style = "double"
    ```

  * **Implement Pre-commit Hook:** Integrate Ruff into your pre-commit hooks to automatically format and lint code before commits.

    ```yaml
    # .pre-commit-config.yaml
    repos:
      - repo: [https://github.com/astral-sh/ruff-pre-commit](https://github.com/astral-sh/ruff-pre-commit)
        rev: v0.4.7
        hooks:
          - id: ruff
            args: [--fix, --exit-non-zero-on-fix]
    ```

-----

## 4\. Dependency Management

Efficiently manage project dependencies with `uv` to ensure a clean and up-to-date environment.

  * **Automated Dependency Cleanup:** `uv` provides commands for seamless installation, uninstallation, and automatic removal of unused packages.

    ```bash
    uv pip install package     # Install a package
    uv pip uninstall package   # Uninstall a package
    uv pip autoremove          # Remove unused packages
    ```

  * **Weekly Update Checks:** Regularly check for outdated packages to maintain security and leverage the latest features.

    ```bash
    uv pip list --outdated
    ```

-----

## 5\. Identifying Dead Code

Periodically identify and remove unused code to reduce technical debt and improve code clarity.

  * **Run During Refactoring:** Use Ruff to find unused variables and imports during refactoring efforts.

    ```bash
    ruff check --select F841   # Unused variables
    ruff check --select F401   # Unused imports
    ```

  * **Integrate into CI:** Include dead code checks as part of your Continuous Integration (CI) pipeline.

    ```yaml
    # GitHub Actions example
    - name: Dead Code Check
      run: ruff check --select F401,F841 src/
    ```

-----

## 6\. Handling Experimental Code

Isolate experimental features to prevent them from polluting the main codebase and to ensure proper cleanup.

  * **Isolate in Branches:** Create dedicated feature branches for experimental work.

    ```bash
    git checkout -b experiment/optimize-algo
    ```

  * **Automate Cleanup of Old Branches:** Implement a script to automatically delete old `experiment/` branches after a set period (e.g., 30 days).

    ```bash
    # Script: cleanup_old_branches.sh
    git branch --merged main | grep 'experiment/' | xargs git branch -d
    ```

-----

## 7\. Backup Procedures

Perform backups before making significant, widespread changes to your codebase.

  * **Before Mass Changes:** Create a backup directory of the affected modules.

    ```bash
    BACKUP_DIR="backup_$(date +%Y%m%d)"
    cp -r src/module $BACKUP_DIR
    ```

-----

## 8\. Test Coverage

Ensure comprehensive test coverage by placing tests logically alongside their respective code.

  * **Tests Alongside Code:** Store tests in the same directory as the code they cover.

    ```
    src/
    ├── payments/
    │   ├── service.py
    │   └── test_service.py  # Test in the same directory
    ```

-----

## 9\. Project Structure Documentation

Maintain a `ARCHITECTURE.md` file at the root of your project to document the logical structure and any key conventions.

  * **`ARCHITECTURE.md` in Root:** Clearly describe the purpose of each top-level directory and any specific rules (e.g., prohibited file types).

    ```markdown
    ## Structure
    - `src/payments/` — Payment logic
    - `src/search/` — Search algorithms

    **Prohibited:** Storing temporary files in `src/`
    ```

-----

## 10\. Regular Audit

Perform regular audits of your project's health, including dead code checks and dependency cleanup.

  * **Monthly Audit:** Schedule a monthly "dead code audit" that combines Ruff checks and `uv pip autoremove`. Define this as a custom Rye command in your `pyproject.toml`.

    ```toml
    # pyproject.toml
    [tool.rye]
    scripts.dead-code-audit = "ruff check --select F401,F841 src/ && uv pip autoremove"
    ```

    Then run:

    ```bash
    rye run dead-code-audit
    ```

-----

## Quick Daily Checklist:

Incorporate these checks into your daily development routine:

  * **Before committing:**
      * `ruff format .` (Formatting)
      * `ruff check .` (Error checking)
      * `uv pip autoremove` (Dependency cleanup)
  * **When creating a new file:**
      * Does it conform to the `src/<module>/` structure?
      * Are there any naming duplicates?
  * **After merging branches:**
      * Run `ruff check --select F401` (Search for "dead" imports)
  * **Once a month:**
      * Conduct a `dead-code-audit`
      * Update `ARCHITECTURE.md`


