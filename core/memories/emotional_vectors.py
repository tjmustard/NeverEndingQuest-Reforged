#!/usr/bin/env python3
"""
Emotional Vector System for Companion Memory Core
Implements 5-dimensional emotional space for memory crystallization.
"""

import math
from typing import Dict, Optional
from dataclasses import dataclass, field

@dataclass
class EmotionalDimensions:
    """Constants for emotional dimension bounds"""
    TRUST_MIN: float = -1.0
    TRUST_MAX: float = 1.0
    POWER_MIN: float = -1.0
    POWER_MAX: float = 1.0
    INTIMACY_MIN: float = 0.0
    INTIMACY_MAX: float = 1.0
    FEAR_MIN: float = 0.0
    FEAR_MAX: float = 1.0
    RESPECT_MIN: float = -1.0
    RESPECT_MAX: float = 1.0

class EmotionalVector:
    """Represents a 5-dimensional emotional state with physics-based properties"""
    
    def __init__(self, initial_values: Optional[Dict[str, float]] = None):
        """Initialize emotional vector with optional starting values"""
        self.dimensions = EmotionalDimensions()
        self.emotions = {
            'trust': 0.0,    # betrayal <-> loyalty
            'power': 0.0,    # submission <-> dominance  
            'intimacy': 0.0, # stranger -> lover
            'fear': 0.0,     # safety -> terror
            'respect': 0.0   # contempt <-> admiration
        }
        
        if initial_values:
            for emotion, value in initial_values.items():
                if emotion in self.emotions:
                    self.add(emotion, value)
    
    def add(self, emotion: str, value: float) -> None:
        """Add to emotional dimension with proper clamping"""
        if emotion not in self.emotions:
            return
            
        self.emotions[emotion] += value
        
        # Apply bounds based on emotion type
        if emotion == 'trust':
            self.emotions[emotion] = max(self.dimensions.TRUST_MIN, 
                                        min(self.dimensions.TRUST_MAX, 
                                            self.emotions[emotion]))
        elif emotion == 'power':
            self.emotions[emotion] = max(self.dimensions.POWER_MIN,
                                        min(self.dimensions.POWER_MAX,
                                            self.emotions[emotion]))
        elif emotion == 'intimacy':
            self.emotions[emotion] = max(self.dimensions.INTIMACY_MIN,
                                        min(self.dimensions.INTIMACY_MAX,
                                            self.emotions[emotion]))
        elif emotion == 'fear':
            self.emotions[emotion] = max(self.dimensions.FEAR_MIN,
                                        min(self.dimensions.FEAR_MAX,
                                            self.emotions[emotion]))
        elif emotion == 'respect':
            self.emotions[emotion] = max(self.dimensions.RESPECT_MIN,
                                        min(self.dimensions.RESPECT_MAX,
                                            self.emotions[emotion]))
    
    def set(self, emotion: str, value: float) -> None:
        """Set emotional dimension to specific value"""
        if emotion in self.emotions:
            self.emotions[emotion] = 0  # Reset first
            self.add(emotion, value)    # Then add with clamping
    
    def magnitude(self) -> float:
        """Calculate the magnitude (velocity) of the emotional vector"""
        return math.sqrt(sum(v**2 for v in self.emotions.values()))
    
    def normalize(self) -> 'EmotionalVector':
        """Return normalized version of this vector"""
        mag = self.magnitude()
        if mag == 0:
            return EmotionalVector()
        
        normalized = EmotionalVector()
        for emotion, value in self.emotions.items():
            normalized.emotions[emotion] = value / mag
        return normalized
    
    def dot_product(self, other: 'EmotionalVector') -> float:
        """Calculate dot product with another emotional vector"""
        return sum(self.emotions[e] * other.emotions[e] 
                  for e in self.emotions.keys())
    
    def cosine_similarity(self, other: 'EmotionalVector') -> float:
        """Calculate cosine similarity with another emotional vector"""
        mag_self = self.magnitude()
        mag_other = other.magnitude()
        
        if mag_self == 0 or mag_other == 0:
            return 0.0
            
        return self.dot_product(other) / (mag_self * mag_other)
    
    def distance(self, other: 'EmotionalVector') -> float:
        """Calculate Euclidean distance to another emotional vector"""
        return math.sqrt(sum((self.emotions[e] - other.emotions[e])**2 
                            for e in self.emotions.keys()))
    
    def copy(self) -> 'EmotionalVector':
        """Create a deep copy of this emotional vector"""
        return EmotionalVector(initial_values=self.emotions.copy())
    
    def to_dict(self) -> Dict[str, float]:
        """Convert to dictionary representation"""
        return self.emotions.copy()
    
    def from_dict(self, data: Dict[str, float]) -> None:
        """Load from dictionary representation"""
        for emotion in self.emotions.keys():
            if emotion in data:
                self.set(emotion, data[emotion])
    
    def get_dominant_emotion(self) -> tuple[str, float]:
        """Get the strongest emotional dimension"""
        if not any(abs(v) > 0.01 for v in self.emotions.values()):
            return ('neutral', 0.0)
            
        dominant = max(self.emotions.items(), key=lambda x: abs(x[1]))
        return dominant
    
    def get_emotional_signature(self) -> str:
        """Get a string signature of significant emotions"""
        significant = [(k, v) for k, v in self.emotions.items() 
                      if abs(v) > 0.1]
        significant.sort(key=lambda x: abs(x[1]), reverse=True)
        
        if not significant:
            return "neutral"
            
        return ", ".join(f"{k}: {v:+.2f}" for k, v in significant[:3])
    
    def __str__(self) -> str:
        """String representation showing non-zero emotions"""
        non_zero = [(k, v) for k, v in self.emotions.items() 
                   if abs(v) > 0.01]
        if not non_zero:
            return "EmotionalVector(neutral)"
        return "EmotionalVector(" + ", ".join(f"{k}={v:.2f}" 
                                              for k, v in non_zero) + ")"
    
    def __repr__(self) -> str:
        """Detailed representation"""
        return f"EmotionalVector({self.emotions})"
    
    def __add__(self, other: 'EmotionalVector') -> 'EmotionalVector':
        """Add two emotional vectors"""
        result = EmotionalVector()
        for emotion in self.emotions.keys():
            result.emotions[emotion] = self.emotions[emotion] + other.emotions[emotion]
            # Apply clamping
            result.add(emotion, 0)  # This triggers clamping without adding
        return result
    
    def __sub__(self, other: 'EmotionalVector') -> 'EmotionalVector':
        """Subtract two emotional vectors"""
        result = EmotionalVector()
        for emotion in self.emotions.keys():
            result.emotions[emotion] = self.emotions[emotion] - other.emotions[emotion]
            # Apply clamping
            result.add(emotion, 0)  # This triggers clamping without adding
        return result
    
    def __mul__(self, scalar: float) -> 'EmotionalVector':
        """Multiply emotional vector by scalar"""
        result = EmotionalVector()
        for emotion, value in self.emotions.items():
            result.set(emotion, value * scalar)
        return result
    
    def __rmul__(self, scalar: float) -> 'EmotionalVector':
        """Right multiply for scalar * vector"""
        return self.__mul__(scalar)

# Behavioral eigenvectors for pattern analysis
BEHAVIORAL_EIGENVECTORS = [
    'protector_vs_exploiter',    # Do they protect or use the NPC?
    'consistent_vs_chaotic',      # Are actions predictable?
    'generous_vs_greedy',         # Do they share resources?
    'truthful_vs_deceptive',      # Do they keep promises?
    'violent_vs_peaceful'         # Do they resort to violence?
]

# Cascade detection types
CASCADE_TYPES = {
    'REVERSAL': 'Same emotion, opposite sign (betrayal after trust)',
    'CONFIRMATION': 'Amplification of existing pattern', 
    'COMPLEXITY': 'Orthogonal emotion (unexpected dimension)',
    'NEUTRAL': 'No significant pattern'
}