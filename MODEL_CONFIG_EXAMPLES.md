# ============================================================================

# MODEL CONFIGURATION EXAMPLES

# ============================================================================

#

# This file shows examples of how to quickly switch between different

# LLM providers by changing just two lines in model_config.py

#

# ============================================================================

# Example 1: OpenAI GPT-4.1 (Default - Recommended)

# ----------------------------------------------------------------------------

# FULL_MODEL = "gpt-4.1-2025-04-14"

# FAST_MODEL = "gpt-4.1-mini-2025-04-14"

#

# Best for: Production use, highest quality responses

# Cost: Moderate to high

# Speed: Fast

# Requirements: OPENAI_API_KEY in config.py

# Example 2: Google Gemini

# ----------------------------------------------------------------------------

# FULL_MODEL = "gemini-exp-1206"

# FAST_MODEL = "gemini-2.0-flash-exp"

#

# Best for: Cost optimization, comparable quality

# Cost: Lower than OpenAI

# Speed: Very fast (especially flash model)

# Requirements

# - GEMINI_API_KEY in config.py

# - LLM_PROVIDER = "gemini" in config.py

# Example 3: Ollama Local Models (Full Power)

# ----------------------------------------------------------------------------

# FULL_MODEL = "llama3.1:70b"

# FAST_MODEL = "llama3.1:8b"

#

# Best for: Privacy, no API costs, local development

# Cost: Free (hardware costs only)

# Speed: Depends on hardware

# Requirements

# - Ollama installed and running locally

# - Models downloaded: `ollama pull llama3.1:70b` and `ollama pull llama3.1:8b`

# - LLM_PROVIDER = "ollama" in config.py

# - OLLAMA_BASE_URL = "<http://localhost:11434>" in config.py

# Example 4: Ollama Local Models (Balanced)

# ----------------------------------------------------------------------------

# FULL_MODEL = "qwen2.5:32b"

# FAST_MODEL = "llama3.1:8b"

#

# Best for: Balance between quality and speed on local hardware

# Cost: Free (hardware costs only)

# Speed: Faster than 70b models

# Requirements: Same as Example 3

# Example 5: Ollama Local Models (Fast)

# ----------------------------------------------------------------------------

# FULL_MODEL = "llama3.1:8b"

# FAST_MODEL = "mistral:7b"

#

# Best for: Testing, rapid prototyping, low-end hardware

# Cost: Free

# Speed: Very fast on consumer hardware

# Requirements: Same as Example 3

# Example 6: Mixed Provider Strategy

# ----------------------------------------------------------------------------

# You can also use different providers for different tasks

#

# In config.py, set: LLM_PROVIDER = "openai"  # or "gemini" or "ollama"

#

# Then in model_config.py, you can mix models

# FULL_MODEL = "gpt-4.1-2025-04-14"    # OpenAI for complex tasks

# FAST_MODEL = "gemini-2.0-flash-exp"  # Gemini for summaries

#

# Note: This requires the provider to support both models

# so it's better to stick with one provider per deployment

# Example 7: GPT-5 Experimental

# ----------------------------------------------------------------------------

# For testing new GPT-5 models

# FULL_MODEL = "gpt-5-2025-08-07"

# FAST_MODEL = "gpt-5-mini-2025-08-07"

# USE_GPT5_MODELS = True  # Enable GPT-5 specific features

#

# Best for: Experimental testing only

# Requirements: GPT-5 API access

# ============================================================================

# HOW TO SWITCH PROVIDERS

# ============================================================================

#

# 1. Open model_config.py

# 2. Change FULL_MODEL and FAST_MODEL to your desired models

# 3. Open config.py

# 4. Set LLM_PROVIDER to match your choice ("openai", "gemini", or "ollama")

# 5. Ensure the appropriate API key / configuration is set

# 6. Restart the application

#

# That's it! All 20+ model configurations will automatically use your

# selected models

#

# ============================================================================
