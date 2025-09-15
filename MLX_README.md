# Zsh LLM Suggestions - MLX

This document provides instructions for setting up, configuring, and using `zsh-llm-suggestions-mlx.py` as a `uv` tool.

## Introduction

`zsh-llm-suggestions-mlx.py` is a proof-of-concept Zsh widget that uses a local LLM to provide command-line suggestions and explanations directly in your terminal. It leverages Apple's MLX framework for running models on Apple Silicon.

## Prerequisites

Before you begin, ensure you have the following software installed:

*   **uv**: A fast Python package installer and resolver.
*   **mlx-lm**: A library for running language models with MLX.
*   **pygments**: A syntax highlighting library.

## Installation

### 1. Install `uv`

If you don't have `uv` installed, you can install it with the following command:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Install Python Dependencies

Use `uv` to install `mlx-lm` and `pygments`:

```bash
uv pip install mlx-lm pygments
```

## Configuration

### Selecting a Model

You need to choose a model from the Hugging Face Hub that is compatible with `mlx-lm`. For this guide, we'll use `mlx-community/Phi-3-mini-4k-instruct-8bit`.

You can set the model using the `ZSH_LLM_SUGGESTIONS_MLX_MODEL` environment variable. Add the following line to your `.zshrc` file:

```bash
export ZSH_LLM_SUGGESTIONS_MLX_MODEL="mlx-community/Phi-3-mini-4k-instruct-8bit"
```

## Usage

You can use the script in two modes: `generate` for command suggestions and `explain` for command explanations.

### Generate Mode

To get a command suggestion, use the `generate` mode. The script will take the content of your command line buffer as input.

**Example:**

```bash
uvx zsh-llm-suggestions-mlx.py generate "list all files in the current directory"
```

### Explain Mode

To get an explanation for a command, use the `explain` mode.

**Example:**

```bash
uvx zsh-llm-suggestions-mlx.py explain "ls -la"
```

## Troubleshooting

### Common Issues

*   **Model Not Found**: Ensure the `MLX_LM_MODEL` environment variable is set correctly and the model exists on the Hugging Face Hub.
*   **Performance Issues**: Running a local LLM can be resource-intensive. If you experience slowdowns, consider using a smaller model or closing other applications.
*   **Errors during installation**: Make sure you have a compatible version of Python and that `uv` is installed correctly.