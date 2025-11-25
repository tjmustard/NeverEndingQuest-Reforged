# SPDX-FileCopyrightText: 2024 MoonlightByte
# SPDX-License-Identifier: Fair-Source-1.0
# License: See LICENSE file in the repository root
# This software is subject to the terms of the Fair Source License.

# ============================================================================
# CONFIG_TEMPLATE.PY - SYSTEM CONFIGURATION TEMPLATE
# ============================================================================
# 
# ARCHITECTURE ROLE: Configuration Management - Central System Settings Template
# 
# This template provides the structure for config.py including API keys, model
# selections, file paths, and operational parameters. It implements our
# "Configurable AI Strategy" by allowing model selection per use case.
# 
# KEY RESPONSIBILITIES:
# - API key and authentication management template
# - AI model configuration for different use cases
# - File system path configuration
# - System operational parameters
# - Environment-specific settings
# 
# CONFIGURATION CATEGORIES:
# - AI Models: Different models for DM, combat, validation, generation
# - File Paths: Module directories and schema locations
# - API Settings: Keys, timeouts, and retry parameters
# - System Parameters: Debug modes, logging levels, validation settings
# 
# SECURITY CONSIDERATIONS:
# - API keys should be moved to environment variables in production
# - Sensitive configuration should not be committed to version control
# - Copy this template to config.py and add your actual API key
# 
# ARCHITECTURAL INTEGRATION:
# - Used by all modules requiring AI model access
# - Provides centralized model selection strategy
# - Enables easy switching between different AI configurations
# - Supports our multi-model AI architecture
# 
# This module enables our flexible, multi-model AI strategy while
# maintaining centralized configuration management.
# ============================================================================

# Import model configuration settings
from model_config import *

# WARNING: Replace with your actual API key and move to environment variables in production
# Provider-specific API Keys
OPENAI_API_KEY = "your-api-key-here"
GEMINI_API_KEY = "your-gemini-api-key-here"

# Ollama Configuration
OLLAMA_BASE_URL = "http://localhost:11434"

# LLM Provider Selection
# Options: "openai", "gemini", "ollama"
LLM_PROVIDER = "openai"

# Automatic API Key Selection
# LLM_API_KEY automatically points to the correct key based on LLM_PROVIDER
# This makes it easier to switch providers without changing code
if LLM_PROVIDER == "openai":
    LLM_API_KEY = OPENAI_API_KEY
elif LLM_PROVIDER == "gemini":
    LLM_API_KEY = GEMINI_API_KEY
elif LLM_PROVIDER == "ollama":
    LLM_API_KEY = None  # Ollama doesn't require an API key
else:
    LLM_API_KEY = OPENAI_API_KEY  # Default to OpenAI

# --- Module folder structure ---
MODULES_DIR = "modules"
DEFAULT_MODULE = "The_Thornwood_Watch"

# Note: All model configurations are now imported from model_config.py above

# --- Web Interface Configuration ---
WEB_PORT = 8357                                         # Port for the web interface (changed from 5000 for security)

# --- END OF FILE config_template.py ---