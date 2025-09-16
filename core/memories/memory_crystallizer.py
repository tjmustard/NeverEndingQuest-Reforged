#!/usr/bin/env python3
"""
Memory Crystallizer for Companion Memory Core
Detects when emotional velocity exceeds threshold to form permanent memories.
"""

import json
import math
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime

from .emotional_vectors import EmotionalVector, CASCADE_TYPES
from .action_parser import ParsedAction

@dataclass
class CoreMemory:
    """Represents a crystallized memory"""
    id: str
    timestamp: str
    location: str
    npc_name: str
    trigger_actions: List[str]  # Readable action names
    emotional_vector: Dict[str, float]
    emotional_velocity: float
    journal_excerpt: str
    context: str
    mass: float  # For gravitational calculations
    decay_resistance: float  # How well memory resists fading
    cascade_type: Optional[str] = None
    interaction_number: int = 0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CoreMemory':
        """Create from dictionary"""
        return cls(**data)

class MemoryCrystallizer:
    """Crystallizes high-velocity emotional moments into permanent memories"""
    
    def __init__(self, crystallization_threshold: float = 0.35):
        """Initialize with configurable threshold"""
        self.crystallization_threshold = crystallization_threshold
        self.memory_counter = 0
        self.npc_interaction_counts = {}
    
    def check_crystallization(self, 
                            actions: List[ParsedAction],
                            npc_name: str,
                            location: str,
                            timestamp: str,
                            journal_excerpt: str,
                            current_emotional_state: Optional[EmotionalVector] = None,
                            existing_memories: Optional[List[CoreMemory]] = None) -> Optional[CoreMemory]:
        """Check if actions create enough emotional velocity to crystallize"""
        
        if not actions:
            return None
        
        # Track interaction count
        if npc_name not in self.npc_interaction_counts:
            self.npc_interaction_counts[npc_name] = 0
        self.npc_interaction_counts[npc_name] += 1
        
        # Calculate emotional delta from actions
        emotional_delta = EmotionalVector()
        for action in actions:
            for emotion, value in action.emotional_impact.items():
                emotional_delta.add(emotion, value)
        
        # Calculate velocity (magnitude of change)
        velocity = emotional_delta.magnitude()
        
        # Check if velocity exceeds threshold
        if velocity < self.crystallization_threshold:
            return None
        
        # Detect cascade type if we have existing memories
        cascade_type = None
        if existing_memories and current_emotional_state:
            cascade_type = self._detect_cascade(
                emotional_delta, 
                existing_memories,
                current_emotional_state
            )
        
        # Calculate memory properties
        mass = self._calculate_mass(velocity, cascade_type)
        decay_resistance = self._calculate_decay_resistance(
            velocity, 
            len(actions),
            cascade_type
        )
        
        # Create readable action list
        trigger_actions = list(set([
            action.get_readable_action() for action in actions
        ]))
        
        # Generate memory ID
        self.memory_counter += 1
        memory_id = f"{npc_name.lower().replace(' ', '_')}_mem_{self.memory_counter:03d}"
        
        # Build context string
        context = self._build_context(actions, location)
        
        # Create the memory
        memory = CoreMemory(
            id=memory_id,
            timestamp=timestamp,
            location=location,
            npc_name=npc_name,
            trigger_actions=trigger_actions,
            emotional_vector=emotional_delta.to_dict(),
            emotional_velocity=round(velocity, 2),
            journal_excerpt=journal_excerpt[:200],  # Limit excerpt length
            context=context,
            mass=round(mass, 2),
            decay_resistance=round(decay_resistance, 2),
            cascade_type=cascade_type,
            interaction_number=self.npc_interaction_counts[npc_name]
        )
        
        return memory
    
    def _calculate_mass(self, velocity: float, cascade_type: Optional[str]) -> float:
        """Calculate memory mass for gravitational system"""
        base_mass = velocity
        
        # Cascades create heavier memories
        if cascade_type == 'REVERSAL':
            base_mass *= 1.5  # Betrayals are heavy
        elif cascade_type == 'CONFIRMATION':
            base_mass *= 1.2  # Reinforcement adds weight
        elif cascade_type == 'COMPLEXITY':
            base_mass *= 1.3  # Unexpected dimensions are significant
        
        return base_mass
    
    def _calculate_decay_resistance(self, velocity: float, 
                                   action_count: int,
                                   cascade_type: Optional[str]) -> float:
        """Calculate how well memory resists decay over time"""
        # Base resistance from emotional intensity
        resistance = min(1.0, velocity * 1.5)
        
        # Multiple actions make memory more persistent
        resistance += min(0.2, action_count * 0.05)
        
        # Cascades are harder to forget
        if cascade_type in ['REVERSAL', 'COMPLEXITY']:
            resistance += 0.2
        
        return min(1.0, resistance)  # Cap at 1.0
    
    def _detect_cascade(self, new_emotion: EmotionalVector,
                       existing_memories: List[CoreMemory],
                       current_state: EmotionalVector) -> Optional[str]:
        """Detect emotional cascade patterns"""
        
        if not existing_memories:
            return None
        
        # Look at recent memories (last 3)
        recent_memories = existing_memories[-3:]
        
        for memory in recent_memories:
            # Reconstruct emotional vector from memory
            memory_vector = EmotionalVector(memory.emotional_vector)
            similarity = new_emotion.cosine_similarity(memory_vector)
            
            # Check for reversal (opposite emotions)
            if similarity < -0.7:
                return 'REVERSAL'
            # Check for confirmation (same direction)
            elif similarity > 0.8:
                return 'CONFIRMATION'
            # Check for complexity (perpendicular)
            elif abs(similarity) < 0.2 and new_emotion.magnitude() > 0.3:
                return 'COMPLEXITY'
        
        return None
    
    def _build_context(self, actions: List[ParsedAction], location: str) -> str:
        """Build a context description from actions"""
        positive_actions = [a for a in actions if a.action_type == 'positive']
        negative_actions = [a for a in actions if a.action_type == 'negative']
        
        if positive_actions and negative_actions:
            return f"Mixed interactions at {location}"
        elif positive_actions:
            return f"Positive interaction at {location}"
        elif negative_actions:
            return f"Negative encounter at {location}"
        else:
            return f"Interaction at {location}"
    
    def prune_memories(self, memories: List[CoreMemory], max_count: int = 5) -> List[CoreMemory]:
        """Keep only the strongest memories"""
        if len(memories) <= max_count:
            return memories
        
        # Sort by importance (velocity * decay_resistance)
        sorted_memories = sorted(
            memories,
            key=lambda m: m.emotional_velocity * m.decay_resistance,
            reverse=True
        )
        
        return sorted_memories[:max_count]
    
    def get_crystallization_stats(self) -> Dict[str, Any]:
        """Get statistics about crystallization process"""
        return {
            'threshold': self.crystallization_threshold,
            'total_memories_created': self.memory_counter,
            'npc_interaction_counts': self.npc_interaction_counts.copy()
        }