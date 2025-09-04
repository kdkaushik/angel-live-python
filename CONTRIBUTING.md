# Contributing to Angel Live Data Stream

Thank you for your interest in contributing to this project! 

## How to Contribute

### Reporting Bugs
- Use the GitHub issue tracker
- Include detailed steps to reproduce
- Provide system information (OS, Python version, etc.)

### Suggesting Features
- Open an issue with the "enhancement" label
- Describe the feature and its benefits
- Include implementation ideas if possible

### Code Contributions

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes**
   - Follow existing code style
   - Add comments for complex logic
   - Update documentation if needed
4. **Test your changes**
   - Ensure the application runs without errors
   - Test with real market data if possible
5. **Commit your changes**
   ```bash
   git commit -m "Add: your feature description"
   ```
6. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```
7. **Create a Pull Request**

## Development Setup

1. Clone your fork
2. Create virtual environment
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```
4. Set up configuration
   ```bash
   cp config.example.py config.py
   # Edit config.py with your credentials
   ```

## Code Style

- Follow PEP 8 guidelines
- Use meaningful variable names
- Add docstrings to functions
- Keep functions focused and small

## Questions?

Contact: kdkaushik@gmail.com