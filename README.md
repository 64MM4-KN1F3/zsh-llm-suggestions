# Zsh LLM Suggestions: UV, MLX & Ollama Edition

This is an enhanced fork of `zsh-llm-suggestions` that brings the power of local and cloud-based Large Language Models (LLMs) directly to your Zsh prompt. Get command suggestions and explanations instantly.

> This project is forked from [stefanheule/zsh-llm-suggestions](https://github.com/stefanheule/zsh-llm-suggestions).

---

## ✨ Key Features

This fork introduces several key enhancements for modern, efficient workflows:

- **UV Support**: Uses [UV](https://docs.astral.sh/uv/) for incredibly fast and self-contained Python dependency management.
    
- **MLX Support**: Run local models on Apple Silicon Macs via the [MLX LM](https://github.com/ml-explore/mlx-lm) library.
    
- **Ollama Support**: Run cross-platform local models using the [Ollama](https://ollama.com/) Python library.
    
- **CI/CD**: Basic quality-of-life improvements for the repository.
    

> **Note**: This has been primarily tested on macOS. Minor adjustments may be needed for other operating systems. <sup>*</sup>MLX is Mac Silicon only

---

## 🚀 How It Works
![Demo of zsh-llm-suggestions](https://github.com/64MM4-KN1F3/zsh-llm-suggestions/blob/master/zsh-suggestions.gif?raw=true)

`zsh-llm-suggestions` eliminates the need to remember complex commands.

- **Generate Commands**: Type a description of what you want to do (e.g., "find all files in my home directory larger than 1GB"), use a hotkey combo, and the LLM will replace your text with the corresponding shell command.
    
- **Explain Commands**: For any shell command you would like explianed, use a separate hotkey combo, and the LLM will provide a clear explanation.
    

---

## 🛠️ Installation

Follow these steps to get set up.

### Step 1: Clone the Repository

Clone this repository to a location of your choice. A common convention is a hidden directory in your home folder.

Shell

```
git clone https://github.com/64MM4-KN1F3/zsh-llm-suggestions.git ~/.zsh-plugins/zsh-llm-suggestions
```


### Step 2: Install Dependencies

This project uses `uv` by default for a seamless setup. You can also install packages manually with `pip`.

#### Option A: Install UV (Recommended)

[UV](https://docs.astral.sh/uv/getting-started/installation/) is an extremely fast Python package installer and resolver. Follow the [official instructions](https://docs.astral.sh/uv/getting-started/installation/) to install it. 
Once `uv` is installed, confiture the zsh-llm-suggestion envrironment from the installation directory with
- Create virtual environemt: `uv venv`
- sync the packages you required (mlx_option, ollama_option and/or openai_option)
Eg. If you only need Ollama:
  `uv sync --extra ollama_option`
Eg. If you need MLX, Ollama and OpenAI: 
  `uv sync --extra ollama_option --extra openai_option --extra mlx_option`

#### Option B: Manual Pip Installation

If you prefer not to use `uv`, you must install the required Python packages manually.

- **For Ollama**: `pip install ollama pygments`
    
- **For MLX**: `pip install mlx-lm pygments`
    
- **For OpenAI**: `pip install openai pygments`
    
- **For GitHub Copilot**: See the official guide for [installing GitHub Copilot in the CLI](https://docs.github.com/en/copilot/how-tos/set-up/install-copilot-in-the-cli).
    

### Step 3: Configure Your `.zshrc`

Add the following configuration to your `~/.zshrc` file.

1. **Source the Plugin**:
    
    Shell
    
    ```
    source ~/.zsh-plugins/zsh-llm-suggestions/zsh-llm-suggestions.zsh
    ```
    
2. **Set Environment Variables**: Configure the plugin's behavior with these variables. Place them **before** the `source`line.
    

|Variable|Description|Default|Example|
|---|---|---|---|
|`ZSH_LLM_SUGGESTIONS_USE_UV`|Set to `true` to use `uv`.|`false`|`export ZSH_LLM_SUGGESTIONS_USE_UV=true`|
|`OPENAI_API_KEY`|Your OpenAI API key.||`export OPENAI_API_KEY="sk-..."`|
|`ZSH_LLM_SUGGESTIONS_MLX_MODEL`|The MLX model to use from Hugging Face.||`export ZSH_LLM_SUGGESTIONS_MLX_MODEL="mlx-community/Phi-3-mini-4k-instruct-8bit"`|
|`ZSH_LLM_SUGGESTIONS_OLLAMA_MODEL`|The Ollama model to use.||`export ZSH_LLM_SUGGESTIONS_OLLAMA_MODEL="llama3"`|
|`ZSH_LLM_SUGGESTIONS_OPENAI_MODEL`|The OpenAI model to use.||`export ZSH_LLM_SUGGESTIONS_OPENAI_MODEL="gpt-4o-mini"`|


3. **Bind Hotkeys**: Use `bindkey` to map the functions to your desired keyboard shortcuts in .zshrc.
    
    > **Tip**: To find the character sequence for a key combination, press `Ctrl+V` in your terminal, then press the key combination.
    
    - `bindkey '^L' zsh_llm_suggestions_mlx`
        
    - `bindkey '^P' zsh_llm_suggestions_mlx_explain`
        
    - `bindkey '^K' zsh_llm_suggestions_ollama`
        
    - `bindkey '^O' zsh_llm_suggestions_ollama_explain`
        

### Step 4: Reload Your Shell

Apply the changes by restarting your terminal or running:

Shell

```
exec zsh
```

---

## ⚙️ Zsh Configuration Example

Here is a complete example of what you might add to your `.zshrc` file, configured for local models with MLX and Ollama.

Shell

```
# Zsh LLM Suggestions Configuration

# --- Environment Variables ---
# Use UV for automatic dependency management
export ZSH_LLM_SUGGESTIONS_USE_UV=true

# Specify the local models to use
export ZSH_LLM_SUGGESTIONS_MLX_MODEL="mlx-community/Qwen2.5-Coder-7B-Instruct-bf16"
export ZSH_LLM_SUGGESTIONS_OLLAMA_MODEL="qwen2.5-coder:7b-instruct-q5_K_M"

# --- Source the Plugin ---
source ~/.zsh-plugins/zsh-llm-suggestions/zsh-llm-suggestions.zsh

# --- Keybindings ---
# Ctrl + L: Suggest command using MLX
bindkey '^L' zsh_llm_suggestions_mlx
# Ctrl + P: Explain command using MLX
bindkey '^P' zsh_llm_suggestions_mlx_explain

# Ctrl + K: Suggest command using Ollama
bindkey '^K' zsh_llm_suggestions_ollama
# Ctrl + O: Explain command using Ollama
bindkey '^O' zsh_llm_suggestions_ollama_explain
```

---

## ⚠️ Important Considerations

1. **Trust But Verify**: LLMs can make mistakes or suggest destructive commands. **Always review a command before executing it.**
    
2. **API Costs**: Using cloud-based providers like OpenAI or GitHub Copilot may incur costs. Monitor your usage.
    

---

## 🙏 Credit

This project is a fork of the original `zsh-llm-suggestions` created by [stefanheule](https://github.com/stefanheule). All credit for the original idea and implementation goes to them.