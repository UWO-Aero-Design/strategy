from pydantic import BaseModel, Field
from typing import List, Callable, Tuple
import numpy as np

class BladeSection(BaseModel):
    "A single blade section of a propeller"
    # Geometric properties
    radius: float = Field(..., description="Radial position from the hub center (m)")
    chord: float = Field(..., description="Chord length (m)")
    twist: float = Field(..., description="Geometric twist (degree)")
    
    # Aerodynamic properties - these come from airfoil choice
    cl_alpha: Tuple[List[float], List[float]] = Field(..., description="Lift curve slope (degree)")
    cd_alpha: Tuple[List[float], List[float]] = Field(..., description="Drag curve slope (degree)")

class Propeller(BaseModel):
    "A complete propeller"
    num_blades: int = Field(..., description="Number of blades")
    diameter: float = Field(..., description="Propeller diameter (m)")
    hub_radius: float = Field(..., description="Hub radius (m)")
    sections: List[BladeSection] = Field(..., description="List of blade sections")


def create_prop(
        num_blades: int, 
        diameter: float, 
        hub_radius: float, 
        num_sections: int,
        chord_range: tuple[float, float], # start cord length, and end cord length as percentage of diameter
        twist_range: tuple[float, float], # start and end twist angle
        cl_alpha: Tuple[List[float], List[float]], # cl/alpha curve.
        cd_alpha: Tuple[List[float], List[float]], # cl/alpha curve.
        ):
    
    radius = diameter / 2
    r_positions = np.linspace(hub_radius, radius, num_sections)
    chord_lengths = np.linspace(chord_range[0], chord_range[1], num_sections)
    twist_angles = np.linspace(twist_range[0], twist_range[1], num_sections)

    sections = []

    for radius, chord, twist_angle, in zip(r_positions, chord_lengths, twist_angles):
        blade = BladeSection(
            radius=radius, 
            chord=chord, 
            twist=twist_angle,
            cl_alpha=cl_alpha,
            cd_alpha=cd_alpha)
        
        sections.append(blade)
        
    prop = Propeller(
        num_blades=num_blades,
        diameter=diameter,
        hub_radius=hub_radius,
        sections=sections
        )
    
    return prop