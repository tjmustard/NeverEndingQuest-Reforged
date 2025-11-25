# SPDX-FileCopyrightText: 2024 MoonlightByte
# SPDX-License-Identifier: Fair-Source-1.0
# License: See LICENSE file in the repository root

"""
LLM Client Abstraction Layer
"""

import os
from abc import ABC, abstractmethod
import openai
import google.generativeai as genai
import ollama
import config
from utils.enhanced_logger import debug, info, warning, error

class LLMClient(ABC):
    @abstractmethod
    def chat_completion(self, model, messages, temperature=0.7, **kwargs):
        pass

class OpenAIClient(LLMClient):
    def __init__(self):
        # Use LLM_API_KEY if available, fallback to OPENAI_API_KEY for backwards compatibility
        api_key = getattr(config, 'LLM_API_KEY', None) or getattr(config, 'OPENAI_API_KEY', None)
        self.client = openai.OpenAI(api_key=api_key)
        # Expose the same interface as OpenAI
        self.chat = self.client.chat
        self.completions = self.client.completions
        self.embeddings = self.client.embeddings

    def chat_completion(self, model, messages, temperature=0.7, **kwargs):
        return self.client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            **kwargs
        )

class GeminiClient(LLMClient):
    def __init__(self):
        genai.configure(api_key=config.GEMINI_API_KEY)
        # Create nested structure to mimic OpenAI interface
        self.chat = GeminiChatNamespace(self)

    def chat_completion(self, model, messages, temperature=0.7, **kwargs):
        # Map OpenAI messages to Gemini format
        gemini_messages = []
        system_instruction = None
        
        for msg in messages:
            role = msg["role"]
            content = msg["content"]
            if role == "system":
                system_instruction = content
            elif role == "user":
                gemini_messages.append({"role": "user", "parts": [content]})
            elif role == "assistant":
                gemini_messages.append({"role": "model", "parts": [content]})

        # If no messages after filtering, create a default user message
        if not gemini_messages:
            gemini_messages = [{"role": "user", "parts": ["Hello"]}]

        generation_config = {
            "temperature": temperature,
        }
        
        # Configure safety settings to be less restrictive
        safety_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
        ]
        
        try:
            model_instance = genai.GenerativeModel(
                model_name=model, 
                system_instruction=system_instruction,
                safety_settings=safety_settings
            )
            
            response = model_instance.generate_content(
                gemini_messages,
                generation_config=generation_config
            )
            
            # Check if response has text
            if not hasattr(response, 'text') or not response.text:
                # If blocked by safety, try to get the response anyway
                if hasattr(response, 'candidates') and response.candidates:
                    # Use the first candidate even if it was blocked
                    candidate = response.candidates[0]
                    if hasattr(candidate, 'content') and hasattr(candidate.content, 'parts'):
                        text_parts = [part.text for part in candidate.content.parts if hasattr(part, 'text')]
                        if text_parts:
                            class MockResponse:
                                def __init__(self, text):
                                    self.text = text
                            response = MockResponse(' '.join(text_parts))
                        else:
                            raise ValueError("Gemini returned empty response - possibly blocked by safety filters")
                    else:
                        raise ValueError("Gemini returned empty response - possibly blocked by safety filters")
                else:
                    raise ValueError("Gemini returned empty response")
            
            # Wrap response to mimic OpenAI response structure
            return GeminiResponseWrapper(response)
        except Exception as e:
            error(f"Gemini API error: {e}")
            raise
        # Note: Gemini model names might need mapping or prefix adjustment
        # For now, assuming the config model name is compatible or mapped elsewhere
        # If using standard OpenAI model names in config, we might need a mapper here.
        # But for this implementation, we assume the user sets the correct model name in config for the provider.
        
        # Simple mapper for common OpenAI names to Gemini equivalents if needed, 
        # but ideally config should hold the correct model name.
        # Let's assume the passed 'model' is correct for the provider for now.
        generation_config = {
            "temperature": temperature,
        }
        
        model_instance = genai.GenerativeModel(model_name=model, system_instruction=system_instruction)
        
        response = model_instance.generate_content(
            gemini_messages,
            generation_config=generation_config
        )
        
        # Wrap response to mimic OpenAI response structure for compatibility
        return GeminiResponseWrapper(response)

class GeminiChatNamespace:
    """Mimics OpenAI's client.chat namespace"""
    def __init__(self, parent_client):
        self.parent = parent_client
        self.completions = GeminiCompletionsNamespace(parent_client)

class GeminiCompletionsNamespace:
    """Mimics OpenAI's client.chat.completions namespace"""
    def __init__(self, parent_client):
        self.parent = parent_client
    
    def create(self, model, messages, temperature=0.7, **kwargs):
        return self.parent.chat_completion(model, messages, temperature, **kwargs)

class GeminiResponseWrapper:
    def __init__(self, response):
        self.response = response
        self.choices = [GeminiChoice(response)]

class GeminiChoice:
    def __init__(self, response):
        self.message = GeminiMessage(response)

class GeminiMessage:
    def __init__(self, response):
        # Clean up Gemini's response - it sometimes wraps JSON in markdown code blocks
        content = response.text if hasattr(response, 'text') else str(response)
        
        # Remove markdown code block formatting if present
        if content.startswith('```'):
            # Remove opening code fence
            lines = content.split('\n')
            if lines[0].startswith('```'):
                lines = lines[1:]  # Remove first line (```json or ```)
            if lines and lines[-1].strip() == '```':
                lines = lines[:-1]  # Remove last line (```)
            content = '\n'.join(lines)
        
        self.content = content.strip()

class OllamaClient(LLMClient):
    def __init__(self):
        self.base_url = getattr(config, 'OLLAMA_BASE_URL', 'http://localhost:11434')
        self.client = ollama.Client(host=self.base_url)
        # Create nested structure to mimic OpenAI interface
        self.chat = OllamaChatNamespace(self)

    def chat_completion(self, model, messages, temperature=0.7, **kwargs):
        response = self.client.chat(
            model=model,
            messages=messages,
            options={'temperature': temperature}
        )
        
        # Wrap response to mimic OpenAI response structure
        return OllamaResponseWrapper(response)

class OllamaChatNamespace:
    """Mimics OpenAI's client.chat namespace"""
    def __init__(self, parent_client):
        self.parent = parent_client
        self.completions = OllamaCompletionsNamespace(parent_client)

class OllamaCompletionsNamespace:
    """Mimics OpenAI's client.chat.completions namespace"""
    def __init__(self, parent_client):
        self.parent = parent_client
    
    def create(self, model, messages, temperature=0.7, **kwargs):
        return self.parent.chat_completion(model, messages, temperature, **kwargs)

class OllamaResponseWrapper:
    def __init__(self, response):
        self.choices = [OllamaChoice(response)]

class OllamaChoice:
    def __init__(self, response):
        self.message = OllamaMessage(response)

class OllamaMessage:
    def __init__(self, response):
        self.content = response['message']['content']

def get_llm_client():
    provider = getattr(config, 'LLM_PROVIDER', 'openai').lower()
    
    if provider == 'gemini':
        return GeminiClient()
    elif provider == 'ollama':
        return OllamaClient()
    else:
        return OpenAIClient()
