### Language Model Settings

#### Model Selection
```bash Terminal
interpreter --model "gpt-3.5-turbo"
```
```python Python
interpreter.llm.model = "gpt-3.5-turbo"
```
```yaml Profile
llm:
  model: gpt-3.5-turbo
```

#### Temperature
```bash Terminal
interpreter --temperature 0.7
```
```python Python
interpreter.llm.temperature = 0.7
```
```yaml Profile
llm:
  temperature: 0.7
```

#### Context Window
```bash Terminal
interpreter --context_window 16000
```
```python Python
interpreter.llm.context_window = 16000
```
```yaml Profile
llm:
  context_window: 16000
```

#### Max Tokens
```bash Terminal
interpreter --max_tokens 100
```
```python Python
interpreter.llm.max_tokens = 100
```
```yaml Profile
llm:
  max_tokens: 100
```

#### Max Output
```bash Terminal
interpreter --max_output 1000
```
```python Python
interpreter.llm.max_output = 1000
```
```yaml Profile
llm:
  max_output: 1000
```

#### API Base
```bash Terminal
interpreter --api_base "https://api.example.com"
```
```python Python
interpreter.llm.api_base = "https://api.example.com"
```
```yaml Profile
llm:
  api_base: https://api.example.com
```

#### API Key
```bash Terminal
interpreter --api_key "your_api_key_here"
```
```python Python
interpreter.llm.api_key = "your_api_key_here"
```
```yaml Profile
llm:
  api_key: your_api_key_here
```

#### API Version
```bash Terminal
interpreter --api_version 2.0.2
```
```python Python
interpreter.llm.api_version = '2.0.2'
```
```yaml Profile
llm:
  api_version: 2.0.2
```

#### LLM Supports Functions
```bash Terminal
interpreter --llm_supports_functions
```
```python Python
interpreter.llm.supports_functions = True
```
```yaml Profile
llm:
  supports_functions: true
```

#### LLM Does Not Support Functions
```bash Terminal
interpreter --no-llm_supports_functions
```
```python Python
interpreter.llm.supports_functions = False
```
```yaml Profile
llm:
  supports_functions: false
```

#### Execution Instructions
```python Python
interpreter.llm.execution_instructions = "To execute code on the user's machine, write a markdown code block. Specify the language after the ```. You will receive the output. Use any programming language."
```

#### LLM Supports Vision
```bash Terminal
interpreter --llm_supports_vision
```
```python Python
interpreter.llm.supports_vision = True
```
```yaml Profile
llm:
  supports_vision: true
```

---

### Interpreter Settings

#### Vision Mode
```bash Terminal
interpreter --vision
```
```python Python
interpreter.llm.model = "gpt-4o"
interpreter.llm.supports_vision = True
interpreter.llm.supports_functions = True
```

#### OS Mode
```bash Terminal
interpreter --os
```
```yaml Profile
os: true
```

#### Version
```bash Terminal
interpreter --version
```

#### Open Local Models Directory
```bash Terminal
interpreter --local_models
```

#### Open Profiles Directory
```bash Terminal
interpreter --profiles
```

#### Select Profile
```bash Terminal
interpreter --profile local.yaml
```

#### Help
```bash Terminal
interpreter --help
```

#### Loop (Force Task Completion)
```bash Terminal
interpreter --loop
```
```python Python
interpreter.loop = True
```
```yaml Profile
loop: true
```

#### Verbose
```bash Terminal
interpreter --verbose
```
```python Python
interpreter.verbose = True
```
```yaml Profile
verbose: true
```

#### Safe Mode
```bash Terminal
interpreter --safe_mode ask
```
```python Python
interpreter.safe_mode = 'ask'
```
```yaml Profile
safe_mode: ask
```

#### Auto Run
```bash Terminal
interpreter --auto_run
```
```python Python
interpreter.auto_run = True
```
```yaml Profile
auto_run: true
```

#### Max Budget
```bash Terminal
interpreter --max_budget 0.01
```
```python Python
interpreter.max_budget = 0.01
```
```yaml Profile
max_budget: 0.01
```

#### Local Mode
```bash Terminal
interpreter --local
```
```python Python
interpreter.offline = True
interpreter.llm.model = "openai/x"
interpreter.llm.api_key = "fake_key"
interpreter.llm.api_base = "http://localhost:1234/v1"
```

#### Fast Mode
```bash Terminal
interpreter --fast
```
```yaml Profile
fast: true
```

#### Custom Instructions
```bash Terminal
interpreter --custom_instructions "This is a custom instruction."
```
```python Python
interpreter.custom_instructions = "This is a custom instruction."
```
```yaml Profile
custom_instructions: "This is a custom instruction."
```

#### System Message
```bash Terminal
interpreter --system_message "You are Open Interpreter..."
```
```python Python
interpreter.system_message = "You are Open Interpreter..."
```
```yaml Profile
system_message: "You are Open Interpreter..."
```

#### Disable Telemetry
```bash Terminal
interpreter --disable_telemetry
```
```python Python
interpreter.anonymized_telemetry = False
```
```yaml Profile
disable_telemetry: true
```

#### Offline
```python Python
interpreter.offline = True
```
```bash Terminal
interpreter --offline true
```
```yaml Profile
offline: true
```

#### Messages
```python Python
interpreter.messages = messages
```

#### User Message Template
```python Python
interpreter.user_message_template = "{content} Please send me some code that would be able to answer my question, in the form of ```python\n... the code ...\n``` or ```shell\n... the code ...\n```"
```

#### Always Apply User Message Template
```python Python
interpreter.always_apply_user_message_template = False
```

#### Code Message Template
```python Python
interpreter.code_output_template = "Code output: {content}\nWhat does this output mean / what's next (if anything, or are we done)?"
```

#### Empty Code Message Template
```python Python
interpreter.empty_code_output_template = "The code above was executed on my machine. It produced no text output. what's next (if anything, or are we done?)"
```

#### Code Output Sender
```python Python
interpreter.code_output_sender = "user"
```

---

### Computer Settings

#### Offline
```python Python
interpreter.computer.offline = True
```
```yaml Profile
computer.offline: True
```

#### Verbose
```python Python
interpreter.computer.verbose = True
```
```yaml Profile
computer.verbose: True
```

#### Emit Images
```python Python
interpreter.computer.emit_images = True
```
```yaml Profile
computer.emit_images: True
```

#### Import Computer API
```python Python
interpreter.computer.import_computer_api = True
```
```yaml Profile
computer.import_computer_api: True
```
