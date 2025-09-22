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

  mode = sys.argv[1] if len(sys.argv) > 1 else "unknown"
  if mode != 'generate' and mode != 'explain':
    if mode != "generate" and mode != "explain":
      print(f"ERROR: something went wrong in zsh-llm-suggestions, please report a bug. Got unknown mode: {mode}")
      return
    return

  try:
    from mlx_lm import load, generate
  except ImportError:
    print(f'echo "{MISSING_PREREQUISITES} Install mlx-lm." && uv pip install mlx-lm')
    return

  try:
    import pygments
  except ImportError:
    print(f'echo "{MISSING_PREREQUISITES} Install pygments." && uv pip install pygments')
    return

  model_name = os.environ.get('ZSH_LLM_SUGGESTIONS_MLX_MODEL', 'mlx-community/Phi-3-mini-4k-instruct-8bit')
  
  model, tokenizer = load(model_name)

  buffer = sys.stdin.read()
  
  system_message = "You are a zsh shell expert, please write a ZSH command that solves my problem. You should only output the completed command, no need to include any other explanation."
  if mode == 'explain':
    system_message = "You are a zsh shell expert, please briefly explain how the given command works. Be as concise as possible. Use Markdown syntax for formatting."

  prompt = tokenizer.apply_chat_template([
      {"role": "system", "content": system_message},
      {"role": "user", "content": buffer},
  ], tokenize=False, add_generation_prompt=True)

  response = generate(model, tokenizer, prompt=prompt, verbose=False, max_tokens=100)
  
  result = response.strip()
  if mode == 'generate':
    result = result.replace('```zsh', '').replace('```', '').strip()
    print(result)
  if mode == 'explain':
    print(highlight_explanation(result))


if __name__ == '__main__':
  main()