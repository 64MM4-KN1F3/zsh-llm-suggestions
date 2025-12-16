#!/usr/bin/env python3

import sys
import os
import subprocess
import json

MISSING_PREREQUISITES = "zsh-llm-suggestions missing prerequisites:"

def highlight_explanation(explanation):
  try:
    import pygments
    from pygments.lexers import MarkdownLexer
    from pygments.formatters import TerminalFormatter
    return pygments.highlight(explanation, MarkdownLexer(), TerminalFormatter(style='material'))
  except ImportError:
    return explanation

def ensure_lms_server_running():
    try:
        # Check server status
        # User requested: lms server status --json | jq .running
        result = subprocess.run(['lms', 'server', 'status', '--json'], capture_output=True, text=True)
        if result.returncode == 0:
            try:
                status = json.loads(result.stdout)
                if not status.get('running', False):
                    print("LM Studio server is not running. Starting it...", file=sys.stderr)
                    subprocess.run(['lms', 'server', 'start'], check=True)
            except json.JSONDecodeError:
                pass
    except FileNotFoundError:
        # lms command likely not found, proceed and let the SDK handle connection errors
        pass
    except Exception as e:
        # Print warning to stderr so it doesn't interfere with command substitution output
        print(f"Warning: Failed to check/start LM Studio server: {e}", file=sys.stderr)

def main():

  model_name = os.environ.get('ZSH_LLM_SUGGESTIONS_MODEL', 'devstral-small-2-24b-instruct-2512')
  mode = sys.argv[1]
  if mode != 'generate' and mode != 'explain':
    print("ERROR: something went wrong in zsh-llm-suggestions, please report a bug. Got unknown mode: " + mode)
    return

  try:
    import lmstudio as lm
  except ImportError:
    print(f'echo "{MISSING_PREREQUISITES} Install LM Studio Python SDK." && pip3 install lmstudio')
    return

    return

  try:
      # Try to connect to the model first (Optimistic check)
      model = lm.llm(model_name)
  except Exception:
      # If connection fails, ensure server is running and try again
      ensure_lms_server_running()
      try:
          model = lm.llm(model_name)
      except Exception as e:
          print(f"ERROR: Could not connect to LM Studio. Ensure LM Studio is running and a model is loaded. Details: {e}")
          return

  buffer = sys.stdin.read()
  
  system_message = "You are a zsh shell expert, please write a ZSH command that solves my problem. You should only output the completed command, no need to include any other explanation."
  
  if mode == 'explain':
    system_message = "You are a zsh shell expert, please briefly explain how the given command works. Be as concise as possible. Use Markdown syntax for formatting."

  # Construct the full prompt as the SDK might rely on a single string or handle history differently.
  # Based on search results, .respond() is the method. 
  # We will try to use a constructed prompt or list of messages if supported.
  # Assuming .respond() takes a string prompt or list of messages. 
  # For safety with a new SDK, simple string concatenation is often safest for a "completion" style, 
  # but for chat models (which LM Studio serves), a chat format is better.
  # Let's try to pass the system message + user message.
  
  full_prompt = f"{system_message}\n\nUser: {buffer}"
  
  try:
      # Using .respond() as found in search results
      result = model.respond(full_prompt).content
  except Exception as e:
      print(f"ERROR: Failed to get response from LM Studio. Details: {e}")
      return

  if mode == 'generate':
    result = result.replace('```zsh', '').replace('```', '').strip()
    print(result)
  
  if mode == 'explain':
    print(highlight_explanation(result))

if __name__ == '__main__':
  main()
