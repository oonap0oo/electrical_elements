#!/usr/bin/env python3
#
#  test_elements.py
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
# this code performs tests on the classes defined in the module elements.py

import math
import cmath

# import module to test
from elements import *
print("Test of module elements.py\n")
print("defining various objects invoking their methods\n")
print("and performing calculations with them\n")
print("*"*40)
print("\n    R E S I S T A N C E\n")

print("Define Resistance objects")
print("-"*30)
r1 = Resistance(1200.0)
print("r1 = Resistance(1200.0) -> r1 :", r1)
r2 = Resistance('1.5E3')
print("r2 = Resistance('1.5E3') -> r2 :", r2)
r3 = Resistance('5k6')
print("r3 = Resistance('5k6') -> r3 : ", r3)

print("\nCalculations using Resistance objects")
print("-"*30)
print("-r2 -> ", -r2)
print("r1 + r2 -> ", r1 + r2)
print("r2 - r1 -> ", r2 - r1)
print("r3 * 2 -> ", r3 * 2)
print("2 * r3 ->  ", 2 * r3)
print("r1 * r2 this should give an number -> ", r1 * r2)
print("r3 / 2 ->  ", r3 / 2)
print("2 / r3 this should give an number -> ", 2 / r3)
print("r1 / r2 this should give an number -> ", r1 / r2)
print("\nCalculating parallel resistance using an instance method")
print("r1.parallelwith( r2, r3) -> ", r1.parallelwith( r2, r3))
print("\nCalculating parallel resistance using an static method")
print("Resistance.parallel(r1, r2, r3) -> ", Resistance.parallel(r1, r2, r3))

print("\nFormatting a Resistance object to") 
print("representation with metric prefix")
print("such as k for kilo")
print("-"*30)
print("r2:", r2, "r3:", r3)
print("r2.tometricprefix() -> ", r2.tometricprefix())
print("r3 / 3 -> ", (r3 / 3))
print("(r3 / 3).tometricprefix() -> ", (r3 / 3).tometricprefix())
print("(r3 / 3).tometricprefix(precision = 6) -> ", (r3 / 3).tometricprefix(precision = 6))

print("\n    I M P E D A N C E\n")

print("Define Impedance objects")
print("-"*30)
z1 = Impedance( 100 + 200j )
print("z1 = Impedance( 100 + 200j ) -> z1: ",z1)
z2 = Impedance( complex( 50, -300 ) )
print("z2 = Impedance( complex( 50, -300 ) ) -> z2:",z2)

print("\nPolar representation")
print("-"*30)
print("z1 :", z1)
print("z1.topolar() -> ", z1.topolar() )
print("z1.topolardeg() -> ", z1.topolardeg() )
print("z2 :", z2)
print("z2.topolar() -> ", z2.topolar() )
print("z2.topolardeg() -> ", z2.topolardeg() )

print("\nCalculations using Impedance objects")
print("-"*30)
print("z1 :", z1)
print("z2 :", z2)
print("z1 + z2 -> ", z1 + z2)
print("z1 - z2 -> ", z1 - z2)
print("3 * z1 + z2 / 2 -> ", 3 * z1 + z2 / 2 )

print("\nCalculating parallel impedance using an instance method")
print("z1.parallelwith( z2 ) -> ", z1.parallelwith( z2 ) )
print("\nCalculating parallel impedance using an static method")
print("Impedance.parallel( z1, z2 ) -> ", Impedance.parallel( z1, z2 ) )

print("\nMixed calculations using Resistance and Impedance objects")
print("-"*30)
print("z1 :", z1)
print("r1 :", r1)    
print("z1 + r1:", z1 + r1)
print("z1.parallelwith( r1 ) -> ", z1.parallelwith( r1 ) )

print("\n    C A P A C I T A N C E\n")

print("Defining Capacitance object")
print("-"*30)
c1 = Capacitance(1.5E-6)
print("c1 = Capacitance(1.5E-6) -> c1:", c1 )
c2 = Capacitance('470nF')
print("c2 = Capacitance('470nF') -> c2:", c2 )

print("\nCalculations using Capacitance objects")
print("-"*30)
c3 = c2 * 3 + c1 / 4
print("c3 = c2 * 3 + c1 / 4 -> c3:", c3)
print("c3.tometricprefix() -> ", c3.tometricprefix())
print("c2.serieswith(c1) -> ", c2.serieswith(c1) )
print("c2.serieswith(c1).tometricprefix() -> ", c2.serieswith(c1).tometricprefix() )

print("\nGetting the impedance of a Capacitance object")
print("-"*30)
print("c1.tometricprefix() : ",c1.tometricprefix())
z4 = c1.getimpedance(frequency = 1000.0)
print("z4 = c1.getimpedance(frequency = 1000.0) -> z4:", z4)
print("z4.topolardeg() -> ", z4.topolardeg())
print("c2.tometricprefix() : ",c2.tometricprefix())
z5 = c2.getimpedance(50.0)
print("z5 = c2.getimpedance(50.0) -> z5:", z5)
print("z5.topolardeg() -> ", z5.topolardeg())

print("\nCalculations using impedance of Capacitance objects and resistance")
print("-"*30)
s = """ 
        |       f = 1kHz
        r1      r1 = r2 = 10kOhm
        |       c1 = c2 = 100nF
        c1
        |
    ---------
    |       |
    r2      c2
    |       |
    ---------
        |
    """
print(s)
f = 1E3
print("f = 1E3 -> f:", f)
r1 = Resistance('10k')
print("r1 = Resistance('10k') -> r1:", r1)
r2 = r1
print("r2=r1")
c1 = Capacitance('100n')
print("c1 = Capacitance('100n') -> c1:", c1)
c2 = c1
print("c2 = c1")
ztotal = r1 + c1.getimpedance(f) + Impedance.parallel( c2.getimpedance(f), r2 )
print("ztotal = r1 + c1.getimpedance(f) + Impedance.parallel( c2.getimpedance(f), r2 )")
print(" -> ztotal:", ztotal)
print("ztotal.tometricprefix() ->", ztotal.tometricprefix())
print("ztotal.topolar() -> ", ztotal.topolar())
print("ztotal.topolardeg() -> ", ztotal.topolardeg())


print("\n    I N D U C T A N C E \n")    


print("Defining Inductance object")
print("-"*30)
l1 = Inductance(2E-3)
print("l1 = Inductance(2E-3) -> l1:", l1 )
l2 = Inductance('500µh')
print("l2 = Inductance('500µh') -> l2:", l2 )


print("\nCalculations using Inductance objects")
print("-"*30)
l3 = l2 / 5 + l1 * 3
print("l3 = 2 / 5 + l1 * 3 -> l3:", l3)
print("l3.tometricprefix() -> ", l3.tometricprefix())
print("l2.parallelwith(l1) -> ", l2.parallelwith(l1) )
print("l2.parallelwith(l1).tometricprefix() -> ", l2.parallelwith(l1).tometricprefix() )

print("\nGetting the impedance of a Inductance object")
print("-"*30)
print("l1.tometricprefix() : ",l1.tometricprefix())
z4 = l1.getimpedance(frequency = 1000.0)
print("z4 = l1.getimpedance(frequency = 1000.0) -> z4:", z4)
print("z4.topolardeg() -> ", z4.topolardeg())
print("l2.tometricprefix() : ",l2.tometricprefix())
z5 = l2.getimpedance(1E6)
print("z5 = l2.getimpedance(1E6) -> z5:", z5)
print("z5.topolardeg() -> ", z5.topolardeg())

print("\nCalculations using Resistance and impedance of Capacitance and Inductance objects")
print("-"*30)
s = """ 
        |       f = 19.59kHz (close to resonance)
        |       r1 = 3 Ohm
        |       l1 = 300µH
    ---------   c1 = 220nF
    |       |
    |       r1
    c1      |
    |       l1
    |       |
    ---------
        |
        |
    """
    
print(s)    
f = 19.59E3
print("f = 19.6E3 -> ", f)
r1 = Resistance(3)
print("r1 = Resistance(5) -> r1:", r1)
l1 = Inductance('300µH')
print("l1 = Inductance('300µH') -> l1:", l1)
c1 = Capacitance('220nF')
print("c1 = Capacitance('220nF') -> c1:", c1)
Zrl = r1 + l1.getimpedance( f )
print("Zrl = r1 + l1.getimpedance( f ) -> Zrl:", Zrl)
Zc1 = c1.getimpedance( f )
print("Zc1 = c1.getimpedance( f ) -> Zc1:", Zc1)
Ztotal = Impedance.parallel( Zrl, Zc1 )
print("Ztotal = Impedance.parallel( Zrl, c1.getimpedance( f ) ) -> Ztotal:", Ztotal)
print("Ztotal.topolar():", Ztotal.topolar())
print("Ztotal.topolardeg():", Ztotal.topolardeg())

print("\n    V O L T A G E \n")    


print("Defining Voltage object")
print("-"*30)
v1 = Voltage('0.23kV')
print("v1 = Voltage('0.23kV') -> v1:", v1 )
v2 = Voltage( cmath.rect(230, 2 * math.pi / 3) )
print("v2 = Voltage( cmath.rect(230, math.pi / 2) ) -> v2:", v2 )
print("v2.topolardeg() -> ", v2.topolardeg())

print("\nCalculations using Voltage objects")
print("-"*30)
v3 = v1 + v2
print("v3 = v1 + v2 -> v3:", v3)
print("v3.topolardeg() -> ", v3.topolardeg())
v4 = v3 / v2
print("dividing 2 voltages returns a complex number")
print("v4 = v3 / v2 -> v4:", v4)
print("type( v4 ) -> ", type( v4 ))
print("abs( v4 ) -> ", abs( v4 ))
print("math.degrees( cmath.phase( v4 ) ) -> ", math.degrees( cmath.phase( v4 ) ))

print("\nCalculations using Voltage, Current and Impedance objects")
print("-"*30)
v1 = Voltage('230V')
print("v1 = Voltage('230V') -> v1:", v1)
c1 = Capacitance('1µ2')
print("c1 = Capacitance('1µ2') -> c1:", c1)
r1 = Resistance('0.1kOhm')
print("r1 = Resistance('0.1kOhm') -> r1:", r1)
f = 50
print("f = 50")
i1 = v1 / ( r1 + c1.getimpedance( f ) )
print("i1 = v1 / ( r1 + c1.getimpedance( f ) ) -> i1:", i1)
print("type( i1 ) -> ", type( i1 ) )
print("i1.topolardeg()", i1.topolardeg())

print("\n ****** END ********************************************")
