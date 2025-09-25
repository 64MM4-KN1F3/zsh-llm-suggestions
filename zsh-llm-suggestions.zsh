
zsh_llm_suggestions_spinner() {
    local pid=$1
    local delay=0.1
    local spinstr='|/-\'

    cleanup() {
      kill $pid
      echo -ne "\e[?25h"
    }
    trap cleanup SIGINT
    
    echo -ne "\e[?25l"
    while [ "$(ps a | awk '{print $1}' | grep $pid)" ]; do
        local temp=${spinstr#?}
        printf " [%c]" "$spinstr"
        local spinstr=$temp${spinstr%"$temp"}
        sleep $delay
        printf "\b\b\b\b"
    done
    printf "    \b\b\b\b"

    echo -ne "\e[?25h"
    trap - SIGINT
}

zsh_llm_suggestions_run_query() {
  local llm="$1"
  local query="$2"
  local result_file="$3"
  local mode="$4"
  echo -n "$query" | eval "$llm $mode" > "$result_file"
}

zsh_llm_completion() {
  local llm="$1"
  local mode="$2"
  local query=${BUFFER}

  # Empty prompt, nothing to do
  if [[ "$query" == "" ]]; then
    return
  fi

  # If the prompt is the last suggestions, just get another suggestion for the same query
  if [[ "$mode" == "generate" ]]; then
    if [[ "$query" == "$ZSH_LLM_SUGGESTIONS_LAST_RESULT" ]]; then
      query=$ZSH_LLM_SUGGESTIONS_LAST_QUERY
    else
      ZSH_LLM_SUGGESTIONS_LAST_QUERY="$query"
    fi
  fi

  # Temporary file to store the result of the background process
  local result_file="/tmp/zsh-llm-suggestions-result"
  # Run the actual query in the background (since it's long-running, and so that we can show a spinner)
  read < <( zsh_llm_suggestions_run_query $llm $query $result_file $mode & echo $! )
  # Get the PID of the background process
  local pid=$REPLY
  # Call the spinner function and pass the PID
  zsh_llm_suggestions_spinner $pid
  
  if [[ "$mode" == "generate" ]]; then
    # Place the query in the history first
    print -s $query
    # Replace the current buffer with the result
    ZSH_LLM_SUGGESTIONS_LAST_RESULT=$(cat $result_file)
    BUFFER="${ZSH_LLM_SUGGESTIONS_LAST_RESULT}"
    CURSOR=${#ZSH_LLM_SUGGESTIONS_LAST_RESULT}
  fi
  if [[ "$mode" == "explain" ]]; then
    echo ""
    eval "cat $result_file"
    echo ""
    zle reset-prompt
  fi
}

SCRIPT_DIR=$( cd -- "$( dirname -- "$0" )" &> /dev/null && pwd )
if [[ -z "$SCRIPT_DIR" ]]; then
  SCRIPT_DIR="./"
fi

zsh_llm_suggestions_openai() {
  local command
  if [[ "$ZSH_LLM_SUGGESTIONS_USE_UV" == "true" ]]; then
    command="uv run -q -w openai_option $SCRIPT_DIR/zsh-llm-suggestions-openai.py"
  else
    command="python3 $SCRIPT_DIR/zsh-llm-suggestions-openai.py"
  fi
  zsh_llm_completion "$command" "generate"
}

zsh_llm_suggestions_openai_explain() {
  local command
  if [[ "$ZSH_LLM_SUGGESTIONS_USE_UV" == "true" ]]; then
    command="uv run -q -w openai_option $SCRIPT_DIR/zsh-llm-suggestions-openai.py"
  else
    command="python3 $SCRIPT_DIR/zsh-llm-suggestions-openai.py"
  fi
  zsh_llm_completion "$command" "explain"
}

zsh_llm_suggestions_github_copilot() {
  local command
  if [[ "$ZSH_LLM_SUGGESTIONS_USE_UV" == "true" ]]; then
    command="uv run -q -w pygments $SCRIPT_DIR/zsh-llm-suggestions-github-copilot.py"
  else
    command="python3 $SCRIPT_DIR/zsh-llm-suggestions-github-copilot.py"
  fi
  zsh_llm_completion "$command" "generate"
}

zsh_llm_suggestions_github_copilot_explain() {
  local command
  if [[ "$ZSH_LLM_SUGGESTIONS_USE_UV" == "true" ]]; then
    command="uv run -q -w pygments $SCRIPT_DIR/zsh-llm-suggestions-github-copilot.py"
  else
    command="python3 $SCRIPT_DIR/zsh-llm-suggestions-github-copilot.py"
  fi
  zsh_llm_completion "$command" "explain"
}

zsh_llm_suggestions_mlx() {
  local command
  if [[ "$ZSH_LLM_SUGGESTIONS_USE_UV" == "true" ]]; then
    command="uv run -q --isolated -w mlx_option $SCRIPT_DIR/zsh-llm-suggestions-mlx.py"
  else
    command="python3 $SCRIPT_DIR/zsh-llm-suggestions-mlx.py"
  fi
  zsh_llm_completion "$command" "generate"
}

zsh_llm_suggestions_mlx_explain() {
  local command
  if [[ "$ZSH_LLM_SUGGESTIONS_USE_UV" == "true" ]]; then
    command="uv run -q --isolated -w mlx_option $SCRIPT_DIR/zsh-llm-suggestions-mlx.py"
  else
    command="python3 $SCRIPT_DIR/zsh-llm-suggestions-mlx.py"
  fi
  zsh_llm_completion "$command" "explain"
}

zsh_llm_suggestions_ollama() {
  local command
  if [[ "$ZSH_LLM_SUGGESTIONS_USE_UV" == "true" ]]; then
    command="uv run -q -w pygments -w ollama_option $SCRIPT_DIR/zsh-llm-suggestions-ollama.py"
  else
    command="python3 $SCRIPT_DIR/zsh-llm-suggestions-ollama.py"
  fi
  zsh_llm_completion "$command" "generate"
}

zsh_llm_suggestions_ollama_explain() {
  local command
  if [[ "$ZSH_LLM_SUGGESTIONS_USE_UV" == "true" ]]; then
    command="uv run -q -w pygments -w ollama_option $SCRIPT_DIR/zsh-llm-suggestions-ollama.py"
  else
    command="python3 $SCRIPT_DIR/zsh-llm-suggestions-ollama.py"
  fi
  zsh_llm_completion "$command" "explain"
}

zle -N zsh_llm_suggestions_ollama
zle -N zsh_llm_suggestions_ollama_explain
zle -N zsh_llm_suggestions_openai
zle -N zsh_llm_suggestions_openai_explain
zle -N zsh_llm_suggestions_github_copilot
zle -N zsh_llm_suggestions_github_copilot_explain
zle -N zsh_llm_suggestions_mlx
zle -N zsh_llm_suggestions_mlx_explain