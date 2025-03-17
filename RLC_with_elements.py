#!/usr/bin/env python3
#
#  RLC_with_elements.py
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
#  
# this code uses the calsses defined elements.py
# it calculates the transferfunction of a RLC circuit
# prints the values and generates a plot using matplotlib

import math
import cmath
import matplotlib.pyplot as plt
from elements import *


s = """
 The circuit:
  
o----- R1 ------o-------------o       
                |           
                |           R1 = 100kOhm
            ---------       R2 = 1 Ohm
            |       |       L1 = 500uH
            |       R2      C1 = 5nF
            C1      |
            |       L1
            |       |
            ---------
                |
                |
o---------------o--------------o                
        """
    
print(s)

# define the components using the objects from the electric elements class
R1 = Resistance("100k")
R2 = Resistance(1)
L1 = Inductance("500uH")
C1 = Capacitance("5nF")

# define the transferfucntion using the objects from the electric elements class
def transferfunction( f ): 
    Zrl = R2 + L1.getimpedance( f )
    Zparallel = Zrl.parallelwith( C1.getimpedance( f ) )
    return( Zparallel / ( R1 + Zparallel ) )
    
# prepare a list with frequency values
f = [ freq for freq in range(90000,110000,150) ] 

# apply the transferfunction to the frequencies using map()
H = list( map( transferfunction, f ) )

# real and imag values to polar
Hmagnitude, Hphase = list( zip( * map( cmath.polar, H) ))
Hphasedeg = list( map( math.degrees, Hphase ) )

# print the values
print("Transferfunction")
print("f  magnitude  phase")
for freq, mag, phase in zip(f, Hmagnitude, Hphasedeg):
    print( f"{freq}Hz  {mag:.2f}  {phase:.1f}°" )
    
# plot the values using matplotlib
plt.subplot(2, 1, 1)
plt.xscale("log")
plt.yscale("log")
plt.plot(f, Hmagnitude )
plt.xlabel("frequency (Hz)")
plt.ylabel("Transfer function, magnitude")
plt.subplot(2, 1, 2)
plt.xscale("log")
plt.plot(f, Hphasedeg )
plt.xlabel("frequency (Hz)")
plt.ylabel("Phase shift, degrees")
plt.grid()
plt.show()
