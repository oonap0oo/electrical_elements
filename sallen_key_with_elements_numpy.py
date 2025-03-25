#!/usr/bin/env python3
#
#  sallen_key_with_elements_numpy.py
#  
#  Copyright 2025 Nap0
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#  *****************************************
#  Sallen - Key VCVS Low Pass filter
#  using classes contained in elements.py
#  and Numpy + Matplotlib
# ******************************************
import math
import cmath
import matplotlib.pyplot as plt
import numpy as np
from elements import * # module containing classes for Resistance, Capacitance, ..

circuit = """
            Sallen – Key VCVS Circuit
     
              o----------------Z3----------------o
              |                                  |
              |                   | -            |
              |                   |    -         |
Vin o----Z1---o---Z2---o----------|+      -      | 
                       |          |          ----o--o Vout
                       |      o---|-      -      |
                       Z4     |   |    -         |
                       |      |   | -            |
                       |      |                  |
0V o-------------------o      o------------------o
                       

 Vout                   Z3 * Z4
______  =  ____________________________________  

 Vin        Z1 * Z2 + Z3 * (Z1 + Z2) + Z3 * Z4    

"""
# define cicuit elements for a low pass filter
R1 = Resistance("10k") # Z1 is a resistor for a low pass
R2 = Resistance("10k") # Z2 is a resistor for a low pass
C3 = Capacitance("1nF") # Z3 is a capacitor for a low pass
C4 = Capacitance("1nF") # Z4 is a capacitor for a low pass

#define transferfunction
def Vout_divby_Vin( freq ):
    Z1 = R1 # for resistors the impedance is the resistance
    Z2 = R2
    Z3 = C3.getimpedance( freq ) # for capacitors the impedance depends on frequency
    Z4 = C4.getimpedance( freq )
    numerator = Z3 * Z4 # calculate with the impedance objects
    denominator = Z1 * Z2 + Z3 * (Z1 + Z2) + Z3 * Z4 
    return( numerator / denominator )

# prepare a list with frequency values to be evenly spaced on a logaritmic scale
f = np.round( np.geomspace(500, 200000, num=30), 0)

# apply the transferfunction to the frequencies using numpy.vectorize
Vec_Vout_divby_Vin = np.vectorize( Vout_divby_Vin )
H = Vec_Vout_divby_Vin( f )

# real and imag values to polar
Hmagnitude = np.abs( H )
Hphase = np.angle( H )
# magnitude values to decibel
Hmagnitude_dB = 20 * np.log10( Hmagnitude )
# phase values to degrees
Hphasedeg = np.rad2deg( Hphase )

# print the circuit, coponent values and transferfunction
print(circuit)
print(f"Z1 is a resistor of {R1.tometricprefix()}")
print(f"Z2 is a resistor of {R2.tometricprefix()}")
print(f"Z3 is a capacitor of {C3.tometricprefix()}")
print(f"Z4 is a capacitor of {C4.tometricprefix()}")
print("\nTransferfunction\n")
print("-"*60)
print( f"{'frequency':>15}Hz |  {'magnitude':>15} dB |  {'phase':>15}° |" )
print("-"*60)
for freq, mag, phase in zip(f, Hmagnitude_dB, Hphasedeg):
    print( f"{freq:>15}Hz |  {mag:>15.2f} dB |  {phase:>15.1f}° |" )

input("Hit ENTER key for plot")

# plot the values using matplotlib
plt.figure(figsize=(15, 10), num="Sallen Key low pass filter")
plt.subplot(2, 1, 1)
plt.xscale("log")
plt.plot(f, Hmagnitude_dB, linewidth = 2, marker="o")
plt.xlabel("frequency (Hz)", fontsize=15)
plt.ylabel("magnitude (dB)", fontsize=15)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.grid()
plt.subplot(2, 1, 2)
plt.xscale("log")
plt.plot(f, Hphasedeg, linewidth = 2)
plt.xlabel("frequency (Hz)", fontsize=15)
plt.ylabel("Phase shift, degrees", fontsize=15)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.grid()
plt.show()

