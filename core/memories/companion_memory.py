#!/usr/bin/env python3
"""
Companion Memory Manager - Main orchestrator for the memory system
Manages memory creation, retrieval, and persistence for companion NPCs.
"""

import json
import os
from typing import Dict, List, Optional, Any
from pathlib import Path
from collections import defaultdict

from .emotional_vectors import EmotionalVector, BEHAVIORAL_EIGENVECTORS
from .action_parser import ActionParser
from .memory_crystallizer import MemoryCrystallizer, CoreMemory
from .memory_gravity import GravitationalRetrieval
from utils.encoding_utils import safe_json_load, safe_json_dump
from utils.enhanced_logger import debug, info, warning, error

class CompanionMemoryManager:
    """Manages the complete memory system for companion NPCs"""
    
    def __init__(self):
        """Initialize the memory management system"""
        self.data_dir = Path('data/companion_memories')
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # Core components
        self.action_parser = ActionParser()
        self.crystallizer = MemoryCrystallizer(crystallization_threshold=0.35)
        self.retrieval_system = GravitationalRetrieval()
        
        # Memory storage
        self.npc_memories: Dict[str, List[CoreMemory]] = defaultdict(list)
        self.npc_emotional_states: Dict[str, EmotionalVector] = defaultdict(EmotionalVector)
        self.npc_behavioral_models: Dict[str, Dict[str, float]] = defaultdict(self._init_behavioral_model)
        self.interaction_counts: Dict[str, int] = defaultdict(int)
        
        # Configuration
        self.config_file = self.data_dir / 'memory_config.json'
        self.load_configuration()
        
        # Load existing memories
        self.load_all_memories()
        
        debug("CompanionMemoryManager", "Initialized Companion Memory System")
    
    def _init_behavioral_model(self) -> Dict[str, float]:
        """Initialize behavioral eigenvector model"""
        return {
            'protector_vs_exploiter': 0.0,
            'consistent_vs_chaotic': 0.0, 
            'generous_vs_greedy': 0.0,
            'truthful_vs_deceptive': 0.0,
            'violent_vs_peaceful': 0.0
        }
    
    def process_journal_entry(self, 
                            journal_entry: Dict[str, Any],
                            party_npcs: Optional[List[str]] = None) -> Dict[str, CoreMemory]:
        """Process a journal entry for memory extraction"""
        
        # Extract key information
        location = journal_entry.get('location', 'Unknown')
        timestamp = f"{journal_entry.get('date', '')} {journal_entry.get('time', '')}"
        summary = journal_entry.get('summary', '')
        
        if not summary:
            return {}
        
        # Get list of NPCs to track
        if not party_npcs:
            party_npcs = ['Kira', 'Elen', 'Thane', 'Vera', 'Brann']
        
        memories_created = {}
        
        # Process each NPC
        for npc_name in party_npcs:
            # Skip if NPC not mentioned
            if npc_name.lower() not in summary.lower():
                continue
            
            # Track interaction
            self.interaction_counts[npc_name] += 1
            
            # Parse actions from journal
            actions = self.action_parser.parse_entry(summary, npc_name)
            
            if not actions:
                continue
            
            # Extract relevant excerpt
            excerpt = self._extract_excerpt(summary, npc_name)
            
            # Check for memory crystallization
            memory = self.crystallizer.check_crystallization(
                actions=actions,
                npc_name=npc_name,
                location=location,
                timestamp=timestamp,
                journal_excerpt=excerpt,
                current_emotional_state=self.npc_emotional_states[npc_name],
                existing_memories=self.npc_memories[npc_name]
            )
            
            if memory:
                # Update emotional state
                for emotion, value in memory.emotional_vector.items():
                    self.npc_emotional_states[npc_name].add(emotion, value)
                
                # Update behavioral model
                self._update_behavioral_model(npc_name, actions)
                
                # Store memory
                self.npc_memories[npc_name].append(memory)
                
                # Prune if needed (keep top 5)
                self.npc_memories[npc_name] = self.crystallizer.prune_memories(
                    self.npc_memories[npc_name], max_count=5
                )
                
                memories_created[npc_name] = memory
                
                info("CompanionMemory", 
                     f"Crystallized memory for {npc_name}: {memory.trigger_actions} (velocity: {memory.emotional_velocity})")
        
        # Save if any memories were created
        if memories_created:
            self.save_all_memories()
        
        return memories_created
    
    def _extract_excerpt(self, text: str, npc_name: str, context_chars: int = 100) -> str:
        """Extract relevant excerpt mentioning NPC"""
        import re
        
        match = re.search(rf'\b{npc_name}\b', text, re.IGNORECASE)
        if match:
            start = max(0, match.start() - context_chars)
            end = min(len(text), match.end() + context_chars)
            excerpt = text[start:end].strip()
            
            # Add ellipsis if truncated
            if start > 0:
                excerpt = '...' + excerpt
            if end < len(text):
                excerpt = excerpt + '...'
            
            return excerpt
        return text[:200] + '...' if len(text) > 200 else text
    
    def _update_behavioral_model(self, npc_name: str, actions: List[Any]) -> None:
        """Update behavioral eigenvector model based on actions"""
        model = self.npc_behavioral_models[npc_name]
        
        for action in actions:
            # Analyze action for behavioral patterns
            action_text = action.get_readable_action().lower()
            
            # Protector vs Exploiter
            if any(word in action_text for word in ['protect', 'defend', 'heal', 'rescue']):
                model['protector_vs_exploiter'] += 0.1
            elif any(word in action_text for word in ['abandon', 'betray', 'exploit']):
                model['protector_vs_exploiter'] -= 0.2
            
            # Consistent vs Chaotic
            if any(word in action_text for word in ['trust', 'promise', 'reliable']):
                model['consistent_vs_chaotic'] += 0.1
            elif any(word in action_text for word in ['betray', 'unpredictable']):
                model['consistent_vs_chaotic'] -= 0.2
            
            # Generous vs Greedy
            if any(word in action_text for word in ['share', 'give', 'generous']):
                model['generous_vs_greedy'] += 0.1
            elif any(word in action_text for word in ['steal', 'hoard', 'greedy']):
                model['generous_vs_greedy'] -= 0.2
            
            # Truthful vs Deceptive
            if any(word in action_text for word in ['honest', 'truth', 'confide']):
                model['truthful_vs_deceptive'] += 0.1
            elif any(word in action_text for word in ['lie', 'deceive', 'mislead']):
                model['truthful_vs_deceptive'] -= 0.2
            
            # Violent vs Peaceful
            if any(word in action_text for word in ['peaceful', 'calm', 'gentle']):
                model['violent_vs_peaceful'] += 0.1
            elif any(word in action_text for word in ['violent', 'aggressive', 'cruel']):
                model['violent_vs_peaceful'] -= 0.2
        
        # Clamp values
        for key in model:
            model[key] = max(-1.0, min(1.0, model[key]))
    
    def get_relevant_memories(self,
                             npc_name: str,
                             current_situation: Dict[str, Any],
                             max_memories: int = 3) -> List[CoreMemory]:
        """Retrieve most relevant memories for current situation"""
        
        if npc_name not in self.npc_memories:
            return []
        
        memories = self.npc_memories[npc_name]
        if not memories:
            return []
        
        # Use gravitational retrieval
        relevant = self.retrieval_system.retrieve_memories(
            memories, current_situation, max_memories
        )
        
        # Return just the memories (not the pull values)
        return [memory for memory, pull in relevant]
    
    def get_npc_profile(self, npc_name: str) -> Dict[str, Any]:
        """Get complete emotional and behavioral profile for an NPC"""
        
        profile = {
            'name': npc_name,
            'total_interactions': self.interaction_counts.get(npc_name, 0),
            'core_memories': len(self.npc_memories.get(npc_name, [])),
            'emotional_state': self.npc_emotional_states[npc_name].to_dict() if npc_name in self.npc_emotional_states else {},
            'behavioral_model': self.npc_behavioral_models.get(npc_name, {}),
            'relationship_status': self._determine_relationship(npc_name),
            'strongest_memory': None
        }
        
        # Add strongest memory if exists
        if npc_name in self.npc_memories and self.npc_memories[npc_name]:
            strongest = max(self.npc_memories[npc_name], 
                          key=lambda m: m.emotional_velocity)
            profile['strongest_memory'] = strongest.to_dict()
        
        return profile
    
    def _determine_relationship(self, npc_name: str) -> List[str]:
        """Determine relationship status based on emotional state"""
        
        if npc_name not in self.npc_emotional_states:
            return ['Acquaintance']
        
        state = self.npc_emotional_states[npc_name]
        relationships = []
        
        if state.emotions['trust'] > 0.5:
            relationships.append('Trusted Ally')
        elif state.emotions['trust'] > 0.3:
            relationships.append('Friend')
        elif state.emotions['trust'] < -0.3:
            relationships.append('Distrusted')
        
        if state.emotions['respect'] > 0.4:
            relationships.append('Respected')
        elif state.emotions['respect'] < -0.3:
            relationships.append('Disrespected')
        
        if state.emotions['intimacy'] > 0.5:
            relationships.append('Close Bond')
        elif state.emotions['intimacy'] > 0.3:
            relationships.append('Growing Closeness')
        
        if state.emotions['fear'] > 0.4:
            relationships.append('Feared')
        
        if state.emotions['power'] > 0.4:
            relationships.append('Leader')
        elif state.emotions['power'] < -0.4:
            relationships.append('Follower')
        
        return relationships if relationships else ['Neutral']
    
    def save_all_memories(self) -> None:
        """Save all memories to disk"""
        
        for npc_name in self.npc_memories:
            self.save_npc_memories(npc_name)
        
        # Save configuration
        self.save_configuration()
    
    def save_npc_memories(self, npc_name: str) -> None:
        """Save memories for a specific NPC"""
        
        filename = self.data_dir / f"{npc_name.lower().replace(' ', '_')}_memories.json"
        
        data = {
            'npc_name': npc_name,
            'core_memories': [m.to_dict() for m in self.npc_memories.get(npc_name, [])],
            'current_emotional_state': self.npc_emotional_states[npc_name].to_dict() if npc_name in self.npc_emotional_states else {},
            'behavioral_model': self.npc_behavioral_models.get(npc_name, {}),
            'total_interactions': self.interaction_counts.get(npc_name, 0)
        }
        
        safe_json_dump(data, filename)
        debug("CompanionMemory", f"Saved memories for {npc_name}")
    
    def load_all_memories(self) -> None:
        """Load all memories from disk"""
        
        for filepath in self.data_dir.glob('*_memories.json'):
            if filepath.name != 'memory_config.json':
                self.load_npc_memories(filepath)
    
    def load_npc_memories(self, filepath: Path) -> None:
        """Load memories for a specific NPC"""
        
        data = safe_json_load(filepath)
        if not data:
            return
        
        npc_name = data.get('npc_name')
        if not npc_name:
            return
        
        # Load memories
        self.npc_memories[npc_name] = [
            CoreMemory.from_dict(m) for m in data.get('core_memories', [])
        ]
        
        # Load emotional state
        if 'current_emotional_state' in data:
            self.npc_emotional_states[npc_name].from_dict(data['current_emotional_state'])
        
        # Load behavioral model
        if 'behavioral_model' in data:
            self.npc_behavioral_models[npc_name] = data['behavioral_model']
        
        # Load interaction count
        self.interaction_counts[npc_name] = data.get('total_interactions', 0)
        
        debug("CompanionMemory", f"Loaded {len(self.npc_memories[npc_name])} memories for {npc_name}")
    
    def save_configuration(self) -> None:
        """Save system configuration"""
        
        config = {
            'crystallization_threshold': self.crystallizer.crystallization_threshold,
            'max_memories_per_npc': 5,
            'retrieval_pull_threshold': self.retrieval_system.pull_threshold,
            'total_memories_created': self.crystallizer.memory_counter,
            'npc_interaction_counts': dict(self.interaction_counts)
        }
        
        safe_json_dump(config, self.config_file)
    
    def load_configuration(self) -> None:
        """Load system configuration"""
        
        if not self.config_file.exists():
            return
        
        config = safe_json_load(self.config_file)
        if not config:
            return
        
        # Apply configuration
        if 'crystallization_threshold' in config:
            self.crystallizer.crystallization_threshold = config['crystallization_threshold']
        
        if 'retrieval_pull_threshold' in config:
            self.retrieval_system.pull_threshold = config['retrieval_pull_threshold']
        
        if 'total_memories_created' in config:
            self.crystallizer.memory_counter = config['total_memories_created']
        
        if 'npc_interaction_counts' in config:
            self.interaction_counts.update(config['npc_interaction_counts'])
    
    def clear_npc_memories(self, npc_name: str) -> None:
        """Clear all memories for a specific NPC"""
        
        if npc_name in self.npc_memories:
            del self.npc_memories[npc_name]
        
        if npc_name in self.npc_emotional_states:
            del self.npc_emotional_states[npc_name]
        
        if npc_name in self.npc_behavioral_models:
            del self.npc_behavioral_models[npc_name]
        
        if npc_name in self.interaction_counts:
            del self.interaction_counts[npc_name]
        
        # Delete file
        filename = self.data_dir / f"{npc_name.lower().replace(' ', '_')}_memories.json"
        if filename.exists():
            filename.unlink()
        
        info("CompanionMemory", f"Cleared all memories for {npc_name}")