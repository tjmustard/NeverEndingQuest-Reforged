#!/usr/bin/env python3
"""
Memory Gravity System for Companion Memory Core
Implements gravitational retrieval where memories pull relevant experiences.
"""

import math
from typing import List, Dict, Optional, Tuple
from datetime import datetime, timedelta

from .emotional_vectors import EmotionalVector
from .memory_crystallizer import CoreMemory

class MemoryGravity:
    """Represents gravitational properties of a memory"""
    
    def __init__(self, memory: CoreMemory):
        """Initialize gravity from a core memory"""
        self.memory = memory
        self.mass = memory.mass
        self.signature = EmotionalVector(memory.emotional_vector)
        self.decay_resistance = memory.decay_resistance
        self.timestamp = memory.timestamp
        self.location = memory.location
    
    def calculate_pull(self, 
                      current_situation: Dict[str, any],
                      current_time: Optional[datetime] = None) -> float:
        """Calculate gravitational pull on current situation"""
        
        # Extract emotional context from situation
        situation_vector = self._extract_situation_vector(current_situation)
        
        # Calculate emotional similarity (resonance)
        emotional_similarity = self.signature.cosine_similarity(situation_vector)
        
        # Calculate temporal weight (older memories have more gravity)
        temporal_weight = self._calculate_temporal_weight(current_time)
        
        # Calculate location relevance
        location_bonus = self._calculate_location_bonus(current_situation)
        
        # Calculate contextual relevance
        context_multiplier = self._calculate_context_multiplier(current_situation)
        
        # Combined gravitational pull
        pull = (self.mass * 
               max(0, emotional_similarity) * 
               temporal_weight * 
               (1 + location_bonus) * 
               context_multiplier)
        
        return pull
    
    def _extract_situation_vector(self, situation: Dict[str, any]) -> EmotionalVector:
        """Extract emotional vector from current situation"""
        vector = EmotionalVector()
        
        # Check for emotional keywords in situation
        if 'emotions' in situation:
            vector.from_dict(situation['emotions'])
        
        # Analyze action type if present
        if 'action_type' in situation:
            action = situation['action_type'].lower()
            if 'heal' in action or 'help' in action:
                vector.add('trust', 0.3)
                vector.add('intimacy', 0.1)
            elif 'fight' in action or 'combat' in action:
                vector.add('trust', 0.2)
                vector.add('respect', 0.2)
            elif 'talk' in action or 'convers' in action:
                vector.add('intimacy', 0.2)
            elif 'threat' in action or 'danger' in action:
                vector.add('fear', 0.3)
                vector.add('trust', 0.2)
        
        # Check for danger level
        if situation.get('danger_level', 0) > 0.5:
            vector.add('fear', 0.2)
            vector.add('trust', 0.1)
        
        # Check for social context
        if situation.get('social_context', False):
            vector.add('intimacy', 0.1)
            vector.add('respect', 0.1)
        
        return vector
    
    def _calculate_temporal_weight(self, current_time: Optional[datetime]) -> float:
        """Calculate weight based on memory age"""
        if not current_time:
            # Default weight if no current time
            return 1.0
        
        try:
            # Parse memory timestamp
            memory_time = self._parse_game_timestamp(self.timestamp)
            if not memory_time:
                return 1.0
            
            # Calculate days elapsed
            time_diff = current_time - memory_time
            days_old = max(0, time_diff.days)
            
            # Logarithmic growth - older memories have more weight
            # But with decay resistance factored in
            weight = math.log(days_old + 1) * self.decay_resistance
            
            return max(0.5, min(2.0, weight))  # Clamp between 0.5 and 2.0
            
        except Exception:
            # On any parsing error, return default weight
            return 1.0
    
    def _parse_game_timestamp(self, timestamp: str) -> Optional[datetime]:
        """Parse game timestamp format"""
        try:
            # Expected format: "1492 Springmonth 1 10:36:00"
            parts = timestamp.split()
            if len(parts) >= 4:
                # Simple conversion - treat as days since campaign start
                year = int(parts[0]) if parts[0].isdigit() else 1492
                day = int(parts[2]) if len(parts) > 2 and parts[2].isdigit() else 1
                
                # Create a relative datetime
                base_date = datetime(2024, 1, 1)  # Arbitrary base
                return base_date + timedelta(days=(year - 1492) * 365 + day)
        except:
            pass
        return None
    
    def _calculate_location_bonus(self, situation: Dict[str, any]) -> float:
        """Calculate bonus for memories from same/similar locations"""
        current_location = situation.get('location', '')
        
        if not current_location:
            return 0.0
        
        # Exact location match
        if current_location.lower() == self.location.lower():
            return 0.5
        
        # Partial location match (same area type)
        location_types = ['dungeon', 'tavern', 'town', 'forest', 'cave', 'catacomb']
        for loc_type in location_types:
            if loc_type in current_location.lower() and loc_type in self.location.lower():
                return 0.2
        
        return 0.0
    
    def _calculate_context_multiplier(self, situation: Dict[str, any]) -> float:
        """Calculate multiplier based on contextual relevance"""
        multiplier = 1.0
        
        # Combat context
        if situation.get('in_combat', False) and 'combat' in str(self.memory.context).lower():
            multiplier *= 1.3
        
        # Cascade memories are more relevant in emotional situations
        if self.memory.cascade_type and situation.get('emotional_intensity', 0) > 0.5:
            multiplier *= 1.4
        
        # Recent memories are more relevant
        if self.memory.interaction_number > 0:
            recency_factor = 1 + (0.01 * min(10, self.memory.interaction_number))
            multiplier *= recency_factor
        
        return multiplier

class GravitationalRetrieval:
    """System for retrieving memories based on gravitational pull"""
    
    def __init__(self):
        """Initialize the retrieval system"""
        self.pull_threshold = 0.1  # Minimum pull to be considered relevant
    
    def retrieve_memories(self,
                         memories: List[CoreMemory],
                         current_situation: Dict[str, any],
                         max_memories: int = 3) -> List[Tuple[CoreMemory, float]]:
        """Retrieve most relevant memories for current situation"""
        
        if not memories:
            return []
        
        # Calculate pull for each memory
        memory_pulls = []
        for memory in memories:
            gravity = MemoryGravity(memory)
            pull = gravity.calculate_pull(current_situation)
            
            if pull > self.pull_threshold:
                memory_pulls.append((memory, pull))
        
        # Sort by pull strength
        memory_pulls.sort(key=lambda x: x[1], reverse=True)
        
        # Return top memories
        return memory_pulls[:max_memories]
    
    def find_resonant_memories(self,
                              memories: List[CoreMemory],
                              emotional_state: EmotionalVector,
                              threshold: float = 0.6) -> List[CoreMemory]:
        """Find memories that resonate with current emotional state"""
        
        resonant = []
        
        for memory in memories:
            memory_vector = EmotionalVector(memory.emotional_vector)
            similarity = emotional_state.cosine_similarity(memory_vector)
            
            if similarity > threshold:
                resonant.append(memory)
        
        return resonant
    
    def detect_memory_chains(self,
                           memories: List[CoreMemory],
                           max_chain_length: int = 3) -> List[List[CoreMemory]]:
        """Detect chains of related memories"""
        
        chains = []
        used_memories = set()
        
        for i, memory in enumerate(memories):
            if memory.id in used_memories:
                continue
            
            chain = [memory]
            used_memories.add(memory.id)
            current_vector = EmotionalVector(memory.emotional_vector)
            
            # Look for memories that follow emotionally
            for j, other in enumerate(memories[i+1:], i+1):
                if other.id in used_memories:
                    continue
                
                other_vector = EmotionalVector(other.emotional_vector)
                similarity = current_vector.cosine_similarity(other_vector)
                
                # Add to chain if similar enough
                if similarity > 0.5:
                    chain.append(other)
                    used_memories.add(other.id)
                    current_vector = other_vector
                    
                    if len(chain) >= max_chain_length:
                        break
            
            if len(chain) > 1:
                chains.append(chain)
        
        return chains