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
  ## TODO remove filename from sys.argv[0] here and reset where the prompt caches live dynamically
  script_dir= os.path.dirname(sys.argv[0])
  if mode != 'generate' and mode != 'explain':
    if mode != "generate" and mode != "explain":
      print(f"ERROR: something went wrong in zsh-llm-suggestions, please report a bug. Got unknown mode: {mode}")
      return
    return
  match mode:
    case 'generate':
        prompt_cache_file_path = os.path.join(script_dir, '.zsh_llm_suggestions_mlx_prompt_cache_generate.safetensors')
    case 'explain':
        prompt_cache_file_path = os.path.join(script_dir, '.zsh_llm_suggestions_mlx_prompt_cache_explain.safetensors')


  try:
    from mlx_lm import load, generate
    from mlx_lm.models.cache import load_prompt_cache, make_prompt_cache, save_prompt_cache
  except ImportError:
    print("{MISSING_PREREQUISITES} Install mlx-lm.")
    return

  try:
    import pygments
  except ImportError:
    print("{MISSING_PREREQUISITES} Install pygments.")
    return
  
  try:
    import re
  except ImportError:
    print("{MISSING_PREREQUISITES} Install re.")
    return

  model_name = os.environ.get('ZSH_LLM_SUGGESTIONS_MLX_MODEL', 'mlx-community/Phi-3-mini-4k-instruct-8bit')
  
  original_stderr = sys.stderr
  sys.stderr = open(os.devnull, 'w')
  try:
    model, tokenizer = load(model_name)
  finally:
    sys.stderr.close()
    sys.stderr = original_stderr

  buffer = sys.stdin.read()
  
  system_message = "You are a zsh shell expert, please write a ZSH command that solves my problem. You should only output the completed command, no need to include any other explanation."
  if mode == 'explain':
    system_message = "You are a zsh shell expert, please briefly explain how the given command works. Be as concise as possible. Use Markdown syntax for formatting."

  prompt = tokenizer.apply_chat_template([
      {"role": "system", "content": system_message},
      {"role": "user", "content": buffer},
  ], tokenize=False, add_generation_prompt=True)

  prompt_cache = None
  if os.path.exists(prompt_cache_file_path):
      try:
          prompt_cache = load_prompt_cache(prompt_cache_file_path)
      except Exception as e:
          print(f"Error loading prompt cache: {e}. Deleting old cache and regenerating.")
          if os.path.exists(prompt_cache_file_path):
              os.remove(prompt_cache_file_path)
          prompt_cache = None
  
  if prompt_cache is None:
      print("creating " + mode + " prompt cache")
      prompt_cache = make_prompt_cache(model)

  try:
      response = generate(
          model,
          tokenizer,
          prompt=prompt,
          verbose=False,
          max_tokens=100,
          prompt_cache=prompt_cache,
      )
  except ValueError as e:
      print(f"Error during generation with prompt cache: {e}. Deleting old cache and regenerating.")
      if os.path.exists(prompt_cache_file_path):
          os.remove(prompt_cache_file_path)
      prompt_cache = make_prompt_cache(model)
      response = generate(
          model,
          tokenizer,
          prompt=prompt,
          verbose=False,
          max_tokens=100,
          prompt_cache=prompt_cache,
      )

  save_prompt_cache(prompt_cache_file_path, prompt_cache)
  
  regex_pattern_to_remove=r'<\|\w+\|>'

  result = re.sub(regex_pattern_to_remove, '', response.strip())
  if mode == 'generate':
    result = result.replace('```zsh', '').replace('```', '').strip()

    print(result)
  if mode == 'explain':
    print(highlight_explanation(result))


if __name__ == '__main__':
  main()