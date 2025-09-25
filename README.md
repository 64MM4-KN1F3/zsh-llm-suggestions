# Local + Cloud LLM-generated command suggestions for Zsh

![Demo of zsh-llm-suggestions](https://github.com/stefanheule/zsh-llm-suggestions/blob/master/zsh-llm-suggestions.gif?raw=true)

---
***Forked from https://github.com/stefanheule/zsh-llm-suggestions
**Key updates include:**
- **[UV](https://docs.astral.sh/uv/) Support for faster/better python project encapsulation + package management**
- **[MLX](https://opensource.apple.com/projects/mlx/) Support for local models on Mac Silicon devices via the [MLX_LM Python library](https://github.com/ml-explore/mlx-lm)**
- **[Ollama](https://ollama.com) Support for cross-platform local models via the [Ollama Python library](https://github.com/ollama/ollama-python)**
- **Basic CI/CD QoL improvements for repo**
---
`zsh` commands can be difficult to remember, but LLMs are great at turning human descriptions of what to do into a command. 

Enter `zsh-llm-suggestions`:
You describe what you would like to do directly in your prompt, you hit a keyboard shortcut of your choosing, and the LLM replaces your request with the command.

Similarly, if you have a command that you don't understand, `zsh-llm-suggestions` can query the LLM for you to explain that command. You can combine these, by first generating a command from a human description, and then asking the LLM to explain the command.
## Installation

### Clone the repository
```shell
git clone https://github.com/64MM4-KN1F3/zsh-llm-suggestions.git ~/zsh/zsh-llm-suggestions
```
### Install supporting packages

#### Install UV (recommended & easier)
See the following for uv installation:
https://docs.astral.sh/uv/getting-started/installation/
Once **uv** is installed, see the [[#Configure Zsh]] section and you're done 🙂
#### Install supporting packages manually via pip
Although not recommended, if you don't want to use **uv** you will have to manually install packages via pip
Eg. `pip3 install ollama pygments

Ollama will need: ollama, pygments
MLX will need: mlx_lm, pygments
OpenAI will need: openai, pygments
Github CoPilot: See [Installing GitHub Copilot in the CLI](https://docs.github.com/en/copilot/how-tos/set-up/install-copilot-in-the-cli)

### Configure Zsh
Source the script and configure the hotkey in `.zshrc`:
- `source ~/zsh/zsh-llm-suggestions/zsh-llm-suggestions.zsh`
Set environment variables
- If using **uv**: `ZSH_LLM_SUGGESTIONS_USE_UV=true`
- Specify models as needed using the following env vars:
	- `ZSH_LLM_SUGGESTIONS_MLX_MODEL`
	- `ZSH_LLM_SUGGESTIONS_OLLAMA_MODEL`
	- `ZSH_LLM_SUGGESTIONS_OPENAI_MODEL`
- For OpenAI, supply your API key in:
	- `OPENAI_API_KEY`
Bind your hotkeys - See examples below
- **Tip** - To check key combo output use Control-V in your terminal followed by the key combination you're considering to bind.

**Important** - To test your configuration, reload your Zsh shell using `exec zsh` (or similarly `source ~/.zshrc`)
#### MLX and Ollama .zshrc excerpt example

```shell
# ZSH MLX autosuggest
export ZSH_LLM_SUGGESTIONS_USE_UV=true
export ZSH_LLM_SUGGESTIONS_MLX_MODEL="mlx-community/Qwen2.5-Coder-7B-Instruct-bf16"
export ZSH_LLM_SUGGESTIONS_OLLAMA_MODEL="qwen2.5-coder:7b-instruct-q5_K_M"

source ~/zsh/zsh-llm-suggestions/zsh-llm-suggestions.zsh

bindkey '^L' zsh_llm_suggestions_mlx # Ctrl + L to have MLX model suggest a command given a English description
bindkey '^P' zsh_llm_suggestions_mlx_explain # Ctrl + P to have MLX model explain a command
bindkey '^K' zsh_llm_suggestions_ollama # Ctrl + K to have Ollama model suggest a command given a English description
bindkey '^O' zsh_llm_suggestions_ollama_explain # Ctrl + O to have Ollama model explain a command
```

#### OpenAI & CoPilot .zshrc excerpt example
```shell
export ZSH_LLM_SUGGESTIONS_USE_UV=true
export OPENAI_API_KEY="abcd-1234-efgh-5678-ijkl-9101"
export ZSH_LLM_SUGGESTIONS_OPENAI_MODEL="gpt-5-mini-2025-08-07"

source ~/zsh/zsh-llm-suggestions/zsh-llm-suggestions.zsh

bindkey '^o' zsh_llm_suggestions_openai # Ctrl + O to have OpenAI suggest a command given a English description
bindkey '^[^o' zsh_llm_suggestions_openai_explain # Ctrl + alt + O to have OpenAI explain a command
bindkey '^p' zsh_llm_suggestions_github_copilot # Ctrl + P to have GitHub Copilot suggest a command given a English description
bindkey '^[^p' zsh_llm_suggestions_github_copilot_explain # Ctrl + alt + P to have GitHub Copilot explain a command
```
## Usage
### LLM suggested commands
Type out what you'd like to do in a Zsh terminal , then hit ctrl+P or ctrl+O (or whatever hotkey you configured). `zsh-llm-suggestions` will then query the configured LLM and replace the query with the command suggested.
### Explain commands using LLM
If you typed a command (or maybe the LLM generated one) that you don't understand, use the bound key combination to have the configured LLM explain it.
## Warning
There are some risks using `zsh-llm-suggestions`:
1. LLMs can suggest bad commands, it is up to you to make sure you are okay executing the commands.
2. Most cloud-based LLMs are not free, so you might incur a cost when using `zsh-llm-suggestions`.
### Credit

This project is a fork of the original `zsh-llm-suggestions` created by [stefanheule](https://github.com/stefanheule/zsh-llm-suggestions). All credit for the original idea and implementation goes to them.