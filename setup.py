from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="angel-live-data",
    version="1.0.0",
    author="Keshav D Kaushik",
    author_email="kdkaushik@gmail.com",
    description="Real-time market data streaming for Angel Broking SmartAPI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/angel-live-data",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Financial and Insurance Industry",
        "Topic :: Office/Business :: Financial :: Investment",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "flask>=2.0.0",
        "flask-socketio>=5.0.0",
        "mysql-connector-python>=8.0.0",
        "smartapi-python>=1.0.0",
        "pyotp>=2.6.0",
        "logzero>=1.7.0",
    ],
    keywords="angel broking, smartapi, market data, real-time, websocket, nifty, options",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/angel-live-data/issues",
        "Source": "https://github.com/yourusername/angel-live-data",
        "Documentation": "https://github.com/yourusername/angel-live-data#readme",
    },
)