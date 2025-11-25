# ============================================================================
# MODEL CONFIGURATION - CENTRALIZED MODEL TIER DEFINITIONS
# ============================================================================
# 
# This file uses a centralized model tier system for easy provider switching.
# Change FULL_MODEL and FAST_MODEL below to switch all models at once.
#
# AVAILABLE MODEL OPTIONS:
#
# OpenAI:
#   - gpt-4.1-2025-04-14         (Full, most capable)
#   - gpt-4.1-mini-2025-04-14    (Fast, cost-effective)
#   - gpt-5-mini-2025-08-07      (GPT-5 fast, experimental)
#   - gpt-5-2025-08-07           (GPT-5 full, experimental)
#
# Gemini:
#   - gemini-2.5-flash           (Fast, cost-effective)
#   - gemini-2.5-pro             (Full, most capable)
#   - gemini-2.0-flash-exp       (Fast, cost-effective, experimental)
#   - gemini-exp-1206            (Full, most capable, experimental)
#   - gemini-2.0-flash-thinking-exp (Reasoning, experimental)
#
# Ollama (Local):
#   - llama3.1:8b                (Fast, 8B parameters)
#   - llama3.1:70b               (Full, 70B parameters)
#   - qwen2.5:32b                (Balanced, 32B parameters)
#   - mistral:7b                 (Fast, 7B parameters)
#
# ============================================================================

# --- CENTRALIZED MODEL TIER CONFIGURATION ---
# Change these two settings to switch all models at once
FULL_MODEL = "gemini-2.5-pro"           # For complex tasks, JSON operations, validation
FAST_MODEL = "gemini-2.5-flash"      # For summaries, simple operations, compression

# --- Main Game Logic Models (used in main.py) ---
DM_MAIN_MODEL = FULL_MODEL
DM_SUMMARIZATION_MODEL = FAST_MODEL
DM_VALIDATION_MODEL = FULL_MODEL

# --- Action Prediction Model (used in action_predictor.py) ---
ACTION_PREDICTION_MODEL = FULL_MODEL  # Use full model for accurate action prediction

# --- Combat Simulation Models (used in combat_manager.py) ---
COMBAT_MAIN_MODEL = FULL_MODEL
# COMBAT_SCHEMA_UPDATER_MODEL - This was defined but not directly used.
# If needed for update_player_info, update_npc_info, update_encounter called from combat_sim,
# those modules will use their own specific models defined below.
COMBAT_DIALOGUE_SUMMARY_MODEL = FAST_MODEL

# --- Utility and Builder Models ---
NPC_BUILDER_MODEL = FULL_MODEL                # Used in npc_builder.py
ADVENTURE_SUMMARY_MODEL = FAST_MODEL
CHARACTER_VALIDATOR_MODEL = FULL_MODEL        # Used in adv_summary.py
PLOT_UPDATE_MODEL = FAST_MODEL                # Used in plot_update.py
PLAYER_INFO_UPDATE_MODEL = FAST_MODEL         # Used in update_player_info.py
NPC_INFO_UPDATE_MODEL = FAST_MODEL            # Used in update_npc_info.py
MONSTER_BUILDER_MODEL = FULL_MODEL
ENCOUNTER_UPDATE_MODEL = FAST_MODEL
LEVEL_UP_MODEL = FULL_MODEL                   # Used in level_up.py

# --- Transition Validation Model ---
TRANSITION_VALIDATOR_MODEL = FAST_MODEL       # Used in transition_validator.py
TRANSITION_VALIDATOR_TEMPERATURE = 0.3        # Low temp for analytical reasoning

# --- Token Optimization Models ---
DM_MINI_MODEL = FAST_MODEL                    # Used for simple conversations and plot-only updates
DM_FULL_MODEL = FULL_MODEL                    # Used for complex actions requiring JSON operations

# --- Model Routing Settings ---
ENABLE_INTELLIGENT_ROUTING = True             # Enable/disable action-based model routing
MAX_VALIDATION_RETRIES = 1                    # Retry with full model after this many validation failures

# --- GPT-5 Model Configuration ---
GPT5_MINI_MODEL = "gpt-5-mini-2025-08-07"     # GPT-5 mini model for testing
GPT5_FULL_MODEL = "gpt-5-2025-08-07"          # GPT-5 full model (kept for compatibility, not used)
USE_GPT5_MODELS = False                       # Toggle for GPT-5 models (default: GPT-4.1)
GPT5_USE_HIGH_REASONING_ON_RETRY = True       # Use high reasoning effort after first failure (instead of model switch)

# --- Combat System Settings ---
USE_COMPRESSED_COMBAT = True                  # Toggle for compressed combat AND validation prompts (False = original prompts)

# --- Conversation Compression Settings ---
# Enable/disable compression types before API calls
COMPRESSION_ENABLED = True                    # Master switch for all compression
COMPRESS_LOCATION_ENCOUNTERS = True           # Compress location encounter data using dynamic compressor
COMPRESS_LOCATION_SUMMARIES = True            # Compress location summaries (now implemented)

# --- Compression Model Configuration ---
# Models used for compressing conversation history and location data
NARRATIVE_COMPRESSION_MODEL = FAST_MODEL      # For general narrative compression
LOCATION_COMPRESSION_MODEL = FULL_MODEL       # For location encounter compression
COMPRESSION_MAX_WORKERS = 4                   # Number of parallel workers for compression