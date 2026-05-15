from setuptools import setup, find_packages

setup(
    name="chronocli",
    version="1.0.3",
    author="Your Name",
    description="AI-powered time tracking CLI",
    packages=find_packages(),
    install_requires=[
        "typer[all]",
        "rich",
        "textual",
        "openai",
        "python-dotenv",
        "matplotlib",
        "reportlab",
        "pandas",
        "sqlmodel",
        "pendulum",
        "gitpython",
        "psutil"
    ],
    entry_points={
        "console_scripts": [
            "chronocli=chronocli.main:app"
        ]
    },
)
