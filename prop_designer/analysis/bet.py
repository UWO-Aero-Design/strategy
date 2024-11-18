import numpy as np
import pandas as pd
from typing import Tuple
from prop_designer.types.prop import Propeller, BladeSection

def calculate_bet(prop: Propeller, rpm: float, free_stream_velocity: float) -> Tuple[float, float, pd.DataFrame]:
    """Calculate thrust and torque using Blade Element Theory
    
    Args:
        prop (Propeller): Propeller object
        rpm (float): Propeller rotational speed (RPM)
        free_stream_velocity (float): Incoming airspeed (m/s)
        
    Returns:
        tuple: (thrust_total, torque_total, section_results_df)
    """
    # Initialize lists to store section data
    section_data = {
        'radius': [],
        'r/R': [],
        'alpha_deg': [],
        'phi_deg': [],
        'chord': [],
        'twist': [],
        'cl': [],
        'cd': [],
        'dL': [],
        'dD': [],
        'velocity': [],
        'thrust': [],
        'torque': []
    }
    
    thrust_forces = []
    torque_forces = []
    
    section_width = (prop.diameter / 2) / len(prop.sections)
    omega = rpm * (2 * np.pi / 60)
    
    for blade in prop.sections:
        # Tangential velocity at this radius
        tangential_velocity = omega * blade.radius
        
        # Calculate velocity triangle
        resultant_velocity = np.sqrt(tangential_velocity**2 + free_stream_velocity**2)
        phi = np.arctan2(free_stream_velocity, tangential_velocity)
        
        # Calculate effective angle of attack
        alpha = np.radians(blade.twist) - phi
        alpha_deg = np.degrees(alpha)
        
        # Interpolate coefficients
        try:
            cl = np.interp(x=alpha_deg, xp=blade.cl_alpha[0], fp=blade.cl_alpha[1])
        except ValueError as e:
            print(f"Alpha {alpha_deg:.1f}° out of range for Cl interpolation: {e}")
            cl = 0    

        try:
            cd = np.interp(x=alpha_deg, xp=blade.cd_alpha[0], fp=blade.cd_alpha[1])
        except ValueError as e:
            print(f"Alpha {alpha_deg:.1f}° out of range for Cd interpolation: {e}")
            cd = 0    

        # Calculate sectional forces
        q = 0.5 * 1.225 * resultant_velocity**2
        dL = cl * q * blade.chord * section_width
        dD = cd * q * blade.chord * section_width
        
        # Transform forces to thrust and torque
        dT = dL * np.cos(phi) - dD * np.sin(phi)
        dQ = (dL * np.sin(phi) + dD * np.cos(phi)) * blade.radius
        
        # Store section data
        section_data['radius'].append(blade.radius)
        section_data['r/R'].append(blade.radius / (prop.diameter/2))
        section_data['alpha_deg'].append(alpha_deg)
        section_data['phi_deg'].append(np.degrees(phi))
        section_data['chord'].append(blade.chord)
        section_data['twist'].append(blade.twist)
        section_data['cl'].append(cl)
        section_data['cd'].append(cd)
        section_data['dL'].append(dL)
        section_data['dD'].append(dD)
        section_data['velocity'].append(resultant_velocity)
        section_data['thrust'].append(dT)
        section_data['torque'].append(dQ)
        
        thrust_forces.append(dT)
        torque_forces.append(dQ)

    # Calculate totals
    thrust_total = sum(thrust_forces) * prop.num_blades
    torque_total = sum(torque_forces) * prop.num_blades
    
    # Create DataFrame
    df = pd.DataFrame(section_data)
        
    # Add total values as attributes to the DataFrame
    df.attrs['thrust_total'] = thrust_total
    df.attrs['torque_total'] = torque_total
    df.attrs['rpm'] = rpm
    df.attrs['velocity'] = free_stream_velocity

    return thrust_total, torque_total, df