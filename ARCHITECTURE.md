# Star Wars Crawler - Project Architecture

## Project Structure

This project follows a modular architecture with clear separation of concerns and adherence to Python development best practices.

### Core Structure

```
star_war_crawler/
├── src/                    # Main source code
│   ├── star_wars_generator/  # Core video generation logic
│   │   ├── core.py           # Main generator class
│   │   ├── cli.py            # Command-line interface
│   │   ├── main.py           # Entry point
│   │   └── test_core.py      # Unit tests
│   └── utils/              # Shared utilities
│       ├── __init__.py
│       └── moviepy_config.py # MoviePy configuration
├── tests/                  # Integration tests
├── scripts/                # Automation scripts
├── examples/               # Usage examples and configs
├── experiments/            # Experimental/prototype code
├── archive/                # Archived files and reports
├── docs/                   # Documentation
├── output/                 # Generated video files
└── logs/                   # Application logs
```

### Module Responsibilities

#### `src/star_wars_generator/`
- **Purpose**: Core video generation functionality
- **Key Components**:
  - `core.py`: Main `Fixed3DStarWarsGeneratorV2` class with 3D text rendering
  - `cli.py`: Command-line interface for user interaction
  - `main.py`: Application entry point
  - `test_core.py`: Unit tests for core functionality

#### `src/utils/`
- **Purpose**: Shared utilities and configurations
- **Key Components**:
  - `moviepy_config.py`: ImageMagick integration setup

#### `tests/`
- **Purpose**: Integration and system-level tests
- **Components**: End-to-end testing scenarios

#### `scripts/`
- **Purpose**: Development and maintenance automation
- **Components**: Cleanup, validation, and audit scripts

#### `experiments/`
- **Purpose**: Prototype and experimental code
- **Rule**: Code here is not production-ready and may be incomplete

#### `examples/`
- **Purpose**: Configuration templates and usage examples
- **Components**: JSON configs, demo scripts

### Design Principles

#### 1. **Separation of Concerns**
- Video generation logic isolated in `core.py`
- UI/CLI logic separate in `cli.py`
- Configuration management centralized

#### 2. **Type Safety**
- Full type annotations on all public functions
- Strict mypy compliance in core modules

#### 3. **Error Handling**
- Specific exception types (no bare `except Exception`)
- Graceful degradation with meaningful error messages

#### 4. **Code Quality**
- Ruff enforcement with comprehensive rules
- Pre-commit hooks for automatic formatting
- Magic numbers replaced with named constants

### Key Conventions

#### **File Naming**
- Test files: `test_*.py` or `*_test.py`
- Config files: `*.json` in `examples/configs/`
- Scripts: Descriptive names in `scripts/`

#### **Prohibited Practices**
- ❌ No temporary files in `src/`
- ❌ No experimental code in production modules
- ❌ No hardcoded magic numbers
- ❌ No broad exception handling
- ❌ No missing type annotations in public APIs

#### **Required Practices**
- ✅ All functions must have docstrings
- ✅ Type annotations on public functions
- ✅ Tests alongside implementation
- ✅ Configuration through JSON files
- ✅ Logging for debugging and monitoring

### Dependencies

#### **Core Dependencies**
- `moviepy`: Video processing and generation
- `pillow`: Image manipulation
- `numpy`: Mathematical operations
- `opencv-python`: Computer vision operations

#### **Development Dependencies**
- `ruff`: Linting and formatting
- `pytest`: Testing framework
- `pre-commit`: Git hooks

### Configuration

#### **Video Generation**
- Default resolution: 1280x720
- Frame rate: 24 FPS
- 3D perspective with configurable tilt angles
- Star field background generation

#### **Code Quality**
- Line length: 88 characters
- Quote style: Double quotes
- Import sorting: isort compatible
- Target Python version: 3.12+

### Maintenance

#### **Regular Tasks**
- Monthly dead code audit: `ruff check --select F401,F841 src/`
- Dependency updates: Check for outdated packages
- Documentation updates: Keep this file current
- Test coverage: Maintain >80% coverage

#### **Before Releases**
- Full test suite execution
- Code quality validation
- Documentation review
- Performance benchmarking

### Extension Points

#### **Adding New Features**
1. Create module in `src/star_wars_generator/`
2. Add corresponding tests
3. Update CLI if user-facing
4. Document in this file

#### **Adding New Generators**
1. Inherit from base generator pattern
2. Implement required methods
3. Add configuration schema
4. Include usage examples

---

**Last Updated**: July 4, 2025
**Maintainer**: Development Team
**Review Frequency**: Monthly
