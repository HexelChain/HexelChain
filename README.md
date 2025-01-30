
# Hexel Chain: Autonomous Intellig![github-banner](https://github.com/user-attachments/assets/0208e4bc-92af-478b-ba40-89738695aed2)
ence Framework  

Hexel Chain serves as an advanced framework for AI-driven agents, seamlessly integrating large language models (LLMs) into an operational environment. It streamlines the creation and execution of LLM-powered agents by tackling key challenges such as task coordination, context management, memory allocation, data handling, tool integration, and SDK support. By enhancing the overall ecosystem for both developers and users, Hexel Chain simplifies the deployment of intelligent agents. The system consists of a core module responsible for essential operations and a dedicated SDK for extended functionality. Additionally, it offers both a web-based interface and a terminal-based UI for versatile interaction.

## 🏠 Structure of Hexel Chain  
### Overview

Hexel Chain consists of two primary components: the Hexel Chain core system and the Hexel Chain SDK.  
The core system functions as a management layer over the underlying operating environment, handling critical resources needed by AI-driven agents, including LLM integration, memory allocation, storage coordination, and tool access.  
The Hexel Chain SDK is built for both developers and users, providing the necessary framework to create and execute intelligent agent applications by interfacing with the core system.  
The core system is maintained within this repository, while the SDK is housed separately.

### Components and Interactions  
The diagram below illustrates how agents engage with the Hexel Chain SDK to communicate with the core system. It also outlines how the core system processes agent requests by orchestrating a sequence of system calls, which are managed and executed across various operational modules.  

## Various Deployment Configurations of Hexel Chain  

Before diving into the different deployment strategies, it's important to understand the core components involved:  

- **AHM (Agent Hub Machine)**: A centralized server that functions as a repository and marketplace for agents, allowing users to upload, access, and distribute agent-related assets.  
- **AUM (Agent UI Machine)**: A client-side interface enabling users to interact with agents. This can range from mobile devices to desktop systems that support visualization and agent control.  
- **ADM (Agent Development Machine)**: A dedicated environment for building, testing, and debugging agents, equipped with essential development tools and frameworks.  
- **ARM (Agent Running Machine)**: The execution layer where agents operate, requiring sufficient computational power to handle real-time tasks.  

The next sections outline the available deployment approaches. **Currently, Hexel Chain supports the first two modes, while additional configurations with enhanced capabilities are in active development.**  

### Mode 1 (Local Core Mode)  

- **Capabilities:**  
  - **For users:** Agents can be acquired from a central repository on Machine B and executed locally on Machine A.  
  - **For developers:** Agents can be created and tested on Machine A, then uploaded to the repository on Machine B.  

### Mode 2 (Remote Core Mode)  

- **Capabilities:**  
  - **Remote access to agents:** Users and developers can interact with agents hosted on Machine B, separate from the system where development and execution occur (Machine A).  
  - **Ideal for:** Users working on devices with limited computational resources, such as mobile or edge devices.  

### Mode 2.5 (Remote Development Mode)  

- **Capabilities:**  
  - **Remote agent creation:** Developers can build agents on Machine B while executing and testing them on Machine A.  
  - **Optimized for:** Development workflows on resource-limited devices.  
- **Key Implementation:**  
  - Efficient packaging and transmission of agents between machines to enable distributed development and testing.  

### Mode 3 (Personal Remote Core Mode)  

- **Upcoming Features:**  
  - Users and developers will have dedicated instances of Hexel Chain, complete with persistent data, accessible through a registered account.  
  - Data will sync seamlessly across multiple devices under the same account.  
- **Key Implementation:**  
  - Secure user account registration and authentication.  
  - Long-term storage for user-specific configurations and data.  
  - Cross-device synchronization of Hexel Chain instances.  
  - Privacy mechanisms for safeguarding user data.  

### Mode 4 (Personal Remote Virtual Core Mode)  

- **Upcoming Features:**  
  - Multiple instances of Hexel Chain can run independently on the same physical machine through virtualization.  
- **Key Implementation:**  
  - Virtualization of distinct Hexel Chain core environments within a single system.  
  - Dynamic resource scheduling and allocation for optimal performance of multiple virtual instances.

 ### Installation  

#### System Requirements  

##### Python  
- Compatible Versions: **Python 3.10 - 3.11**  

#### Configuring API Keys  

To enable various AI services such as OpenAI, Anthropic, Groq, and HuggingFace, API keys are required. The recommended approach for setting them up is by modifying the `hexel/config/config.yaml` file directly.  

> [!NOTE]  
> It is highly advised to configure API keys via `hexel/config/config.yaml`. This method ensures a streamlined setup process and minimizes potential synchronization conflicts that may arise with environment variables.  

Below is a sample configuration for defining API keys within `hexel/config/config.yaml`:  

```yaml
openai: "your-openai-key"
gemini: "your-gemini-key"
groq: "your-groq-key"
anthropic: "your-anthropic-key"
huggingface:
  auth_token: "your-huggingface-token"
  home: "optional-path"

To acquire these API keys, refer to the respective provider platforms:

- **OpenAI API:** Visit OpenAI's API Key Page  
- **Google Gemini API:** Access via Google's API Portal  
- **Groq API:** Retrieve from Groq's Developer Console  
- **HuggingFace Token:** Generate from HuggingFace's Settings  
- **Anthropic API:** Available via Anthropic's API Dashboard  

**Use ollama Models:** If you would like to use ollama, you need to download ollama from from https://ollama.com/.
Then pull the available models you would like to use from https://ollama.com/library
```bash
ollama pull llama3:8b # use llama3:8b for example
```
Then you need to start the ollama server either from ollama app
or using the following command in the terminal
```bash
ollama serve
```
> [!TIP]
> ollama can support both CPU-only and GPU environment, details of how to use ollama can be found at [here](https://github.com/ollama/ollama)

**Utilizing HuggingFace Models:**  
Certain models from HuggingFace require authentication. To access all available models, you must configure an authentication token. This can be generated from HuggingFace’s token settings page and should be set as an environment variable using the following command:  

By default, HuggingFace downloads models to the `~/.cache` directory. If you wish to specify a different location for storing model files, you can define the directory path in the `hexel/config/config.yaml` file.  

To accelerate model inference, you can leverage vLLM as the backend.  

> [!NOTE]  
> vLLM is currently compatible only with Linux-based systems and requires a GPU-enabled environment. If your system does not meet these requirements, alternative solutions must be considered.  

Since vLLM does not natively support specifying GPU IDs, you will need to manually configure the environment variable as shown below:  

```bash
export CUDA_VISIBLE_DEVICES="0" # Replace with the desired GPU IDs

```
##### Detailed Setup Instructions  

For an in-depth guide on configuring API keys and environment settings, refer to the official documentation.  

Alternatively, environment variables can be set manually using the following commands:  

```bash
# Display current environment variables or available API keys if none are set  
hexel env list  

# Configure new environment variables or modify existing ones  
hexel env set  

# Refresh Hexel Chain’s configuration without restarting the system  
hexel refresh  

# When environment variables are not configured, the system will prompt for the following API keys:  
export OPENAI_API_KEY="your-openai-key"  
export GEMINI_API_KEY="your-gemini-key"  
export GROQ_API_KEY="your-groq-key"  
export HF_AUTH_TOKEN="your-huggingface-token"  
export HF_HOME="optional-path-to-store-huggingface-models"  

# Installation from Source  
# Clone the Hexel Chain repository  
git clone https://github.com/agiresearch/HexelChain.git  
cd HexelChain && git checkout v0.2.0.beta  

# Set up a virtual environment (recommended)  
python3.x -m venv venv  # Supports Python 3.10 and 3.11  
source venv/bin/activate  

# Alternatively, create a Conda environment  
conda create -n venv python=3.x  # Supports Python 3.10 and 3.11  
conda activate venv  

# Install dependencies based on system configuration  
# For GPU-enabled environments:  
pip install -r requirements-cuda.txt  

# For CPU-only environments:  
pip install -r requirements.txt  

# Quickstart - Launch Hexel Chain  
# Start the Hexel Chain core system  
bash runtime/launch_kernel.sh  

# If a specific Python version needs to be set explicitly  
python3.x -m uvicorn runtime.kernel:app --host 0.0.0.0  

# To run the system in the background  
python3.x -m uvicorn runtime.kernel:app --host 0.0.0.0 & 2>&1 > MYLOGFILE.txt  

# To keep the process running after closing the shell  
nohup python3.x -m uvicorn runtime.kernel:app --host 0.0.0.0 &  

### Supported LLM Cores
| Provider 🏢 | Model Name 🤖 | Open Source 🔓 | Model String ⌨️ | Backend ⚙️ | Required API Key |
|:------------|:-------------|:---------------|:---------------|:---------------|:----------------|
| Anthropic | Claude 3.5 Sonnet | ❌ | claude-3-5-sonnet-20241022 |anthropic | ANTHROPIC_API_KEY |
| Anthropic | Claude 3.5 Haiku | ❌ | claude-3-5-haiku-20241022 |anthropic | ANTHROPIC_API_KEY |
| Anthropic | Claude 3 Opus | ❌ | claude-3-opus-20240229 |anthropic | ANTHROPIC_API_KEY |
| Anthropic | Claude 3 Sonnet | ❌ | claude-3-sonnet-20240229 |anthropic | ANTHROPIC_API_KEY |
| Anthropic | Claude 3 Haiku | ❌ | claude-3-haiku-20240307 |anthropic | ANTHROPIC_API_KEY |
| OpenAI | GPT-4 | ❌ | gpt-4 |openai| OPENAI_API_KEY |
| OpenAI | GPT-4 Turbo | ❌ | gpt-4-turbo |openai| OPENAI_API_KEY |
| OpenAI | GPT-4o | ❌ | gpt-4o |openai| OPENAI_API_KEY |
| OpenAI | GPT-4o mini | ❌ | gpt-4o-mini |openai| OPENAI_API_KEY |
| OpenAI | GPT-3.5 Turbo | ❌ | gpt-3.5-turbo |openai| OPENAI_API_KEY |
| Google | Gemini 1.5 Flash | ❌ | gemini-1.5-flash |google| GEMINI_API_KEY |
| Google | Gemini 1.5 Flash-8B | ❌ | gemini-1.5-flash-8b |google| GEMINI_API_KEY |
| Google | Gemini 1.5 Pro | ❌ | gemini-1.5-pro |google| GEMINI_API_KEY |
| Google | Gemini 1.0 Pro | ❌ | gemini-1.0-pro |google| GEMINI_API_KEY |
| Groq | Llama 3.2 90B Vision | ✅ | llama-3.2-90b-vision-preview |groq| GROQ_API_KEY |
| Groq | Llama 3.2 11B Vision | ✅ | llama-3.2-11b-vision-preview |groq| GROQ_API_KEY |
| Groq | Llama 3.1 70B | ✅ | llama-3.1-70b-versatile |groq| GROQ_API_KEY |
| Groq | Llama Guard 3 8B | ✅ | llama-guard-3-8b |groq| GROQ_API_KEY |
| Groq | Llama 3 70B | ✅ | llama3-70b-8192 |groq| GROQ_API_KEY |
| Groq | Llama 3 8B | ✅ | llama3-8b-8192 |groq| GROQ_API_KEY |
| Groq | Mixtral 8x7B | ✅ | mixtral-8x7b-32768 |groq| GROQ_API_KEY |
| Groq | Gemma 7B | ✅ | gemma-7b-it |groq| GROQ_API_KEY |
| Groq | Gemma 2B | ✅ | gemma2-9b-it |groq| GROQ_API_KEY |
| Groq | Llama3 Groq 70B | ✅ | llama3-groq-70b-8192-tool-use-preview |groq| GROQ_API_KEY |
| Groq | Llama3 Groq 8B | ✅ | llama3-groq-8b-8192-tool-use-preview |groq| GROQ_API_KEY |
| ollama | [All Models](https://ollama.com/search) | ✅ | model-name |ollama| - |
| vLLM | [All Models](https://docs.vllm.ai/en/latest/) | ✅ | model-name |vllm| - |
| HuggingFace | [All Models](https://huggingface.co/models/) | ✅ | model-name |huggingface| HF_HOME |
