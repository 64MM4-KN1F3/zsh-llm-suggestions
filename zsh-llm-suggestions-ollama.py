#!/usr/bin/env python3

import sys
import os

MISSING_PREREQUISITES = "zsh-llm-suggestions missing prerequisites:"

def highlight_explanation(explanation):
  try:
    import pygments
    from pygments.lexers import MarkdownLexer
    from pygments.formatters import TerminalFormatter
    return pygments.highlight(explanation, MarkdownLexer(), TerminalFormatter(style='material'))
  except ImportError:
    return explanation

def main():

  mode = sys.argv
  if mode != 'generate' and mode != 'explain':
    print("ERROR: something went wrong in zsh-llm-suggestions, please report a bug. Got unknown mode: " + mode)
    return

  try:
    import ollama
  except ImportError:
    print(f'echo "{MISSING_PREREQUISITES} Install Ollama Python API." && uv pip install ollama')
    return

  try:
    import pygments
  except ImportError:
    print(f'echo "{MISSING_PREREQUISITES} Install pygments." && uv pip install pygments')
    return

  model_name = os.environ.get('ZSH_LLM_SUGGESTIONS_OLLAMA_MODEL', 'llama3') # Default to 'llama3'

  client = ollama.Client()

  buffer = sys.stdin.read()
  system_message="""You are a zsh shell expert, please write a ZSH command that solves my problem.
You should only output the completed command, no need to include any other explanation."""
  if mode == 'explain':
    system_message="""You are a zsh shell expert, please briefly explain how the given command works. Be as concise as possible. Use Markdown syntax for formatting."""
  
  messages=[
    {
      "role":'system',
      "content": system_message,
    },
    {"role": "user", "content": buffer}
  ]
  
  response = client.chat(
    model=model_name,
    messages=messages,
    options={
        'temperature': 0.2,
        'num_predict': 1000,
    }
  )
  
  result = response['message']['content'].strip()
  if mode == 'generate':
    result = result.replace('```zsh', '').replace('```', '').strip()
    print(result)
  if mode == 'explain':
    print(highlight_explanation(result))


if __name__ == '__main__':
  main()