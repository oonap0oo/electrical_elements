#!/usr/bin/env python3
#
#  elements.py
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
# class definitions for electrical elements
# this module defines:
#
# class Electricalelement
# class Impedance(Electricalelement)
# class Resistance(Impedance)
# class Capacitance(Electricalelement)
# class Inductance(Electricalelement)
# class Voltage(Electricalelement)
# class Current(Electricalelement)

import math
import cmath

# ----------------------------------------------------------
# generic class for actual electric elements to inherit from
# ----------------------------------------------------------
class Electricalelement:
    
    # initialising the Electricalelement using a number or string as parameter
    def __init__(self, value = 0, unit = ""):        
        if  isinstance(value, (float, int, complex)):
            self.value = value
        elif isinstance(value, str):
            self.value = Electricalelement.metricprefixtofloat(value)
        else:
            raise TypeError(f"Cannot initialise Electricalelement using a {type(value)}")
        self.unit = unit
    
    # return a machine readable representation of an Electricalelement
    def __repr__(self):
        return( f"Electricalelement({self.value},'{self.unit}')" )  
    
    # string representation of an Electricalelement
    def __str__(self):
        if self.value.imag == 0:
            return( f"{self.value.real} {self.unit}" ) 
        else:
            return( f"{self.value} {self.unit}" )  
    
            
    # instance method, return a string representing a value with metric prefix
    def tometricprefix(self, precision=3):
        if isinstance(self.value, (int, float) ):
            return( Electricalelement.floattometricprefix( self.value, self.unit, precision ) )
        elif isinstance(self.value, complex ):
            if self.value.imag == 0:
                return( Electricalelement.floattometricprefix( self.value.real, self.unit, precision ) )
            else:
                realstr = Electricalelement.floattometricprefix( self.value.real, self.unit, precision )
                imagstr = Electricalelement.floattometricprefix( abs( self.value.imag ), self.unit, precision )
                if self.value.imag < 0:
                    return( f"({realstr})-({imagstr})j" )
                else:
                    return( f"({realstr})+({imagstr})j" )
        else:
            raise TypeError(f"Cannot convert {type(self)} to metric prefix")
            
    
    def topolar(self, phaseprecision=3):
        modulus, phase =  cmath.polar( self.value )
        phase = round(phase, phaseprecision)
        return( f"{modulus} {self.unit} {chr(0x2220)} {phase} radians" )
    
    def topolardeg(self, phaseprecision=3):
        modulus, phase =  cmath.polar( self.value )
        phasedeg = math.degrees( phase )
        phasedeg = round(phasedeg, phaseprecision)
        return( f"{modulus} {self.unit} {chr(0x2220)} {phasedeg}°" )

            
    
    # static method, convert a string with metric prefix to float return nan if not valid
    @staticmethod
    def metricprefixtofloat( expression ): 
        #print("--- expression",expression,end=" ---> ")
        expression = expression.strip()
        units = ("V", "A", "Ohm", "F","Farad" ,"H" ,"Henry")
        for unit in units:
            if unit in expression:
                expression = expression.replace(unit, "")        
        #print("expression",expression)
        dictprefixinv = {'T': 12, 'G': 9, 'M': 6, 'k': 3, 'm': -3, 'µ': -6, 'u': -6, \
            'n': -9, 'p': -12, 'f': -15}
        value=None
        for prefix in dictprefixinv:
            if prefix in expression:
                mantissastr,*otherstr=expression.split(prefix)
                if otherstr[0].isnumeric():
                    mantissastr=f"{mantissastr}.{otherstr[0]}"
                exponent=dictprefixinv[prefix]
                try:
                    value=float(mantissastr) * 10 ** exponent
                except ValueError:
                    value=math.nan
                finally:
                    break
        if value is None: # no metric prefix was encountered
            try:
                value=float(expression) # see if it is a regular valid float 
            except ValueError:
                value=math.nan
        return value
        
        
    # static method, convert a float to string with metric prefix
    @staticmethod
    def floattometricprefix( x , unit="", precision=3 ):   
        dictprefix = {12:"T",9:"G",6:"M",3:"k",-3:"m",-6:"µ",-9:"n",-12:"p",-15:"f"} 
        sci = f"{x:e}"
        mantissastr,exponentstr = sci.split("e")
        newexponent = int(exponentstr) // 3 * 3
        factormantissa=10 ** (int(exponentstr) % 3)
        newmantissa = float(mantissastr) * factormantissa
        newmantissa = round(newmantissa, precision)
        prefix = dictprefix.get(newexponent)
        if prefix is None:
            if newexponent != 0:
                engstr = f"{newmantissa}E{newexponent:+03d} {unit}"  
            else:
                engstr = f"{newmantissa} {unit}"
        else:        
            engstr = f"{newmantissa} {prefix}{unit}"
        return engstr
    


    


# -----------------------------------------------------------------       
# Class for an impedance to be used with resistance, capacitance and inductance
# -----------------------------------------------------------------       
class Impedance(Electricalelement):
    
    # value is the impedance value in Ohm
    def __init__(self, value = 0):
        if isinstance( value, complex ):
            super().__init__( value, "Ohm" )
        elif isinstance( value, (int, float) ):
            super().__init__( complex(value), "Ohm" )
        elif isinstance(value, str):
            floatvalue = Electricalelement.metricprefixtofloat(value)
            super().__init__( complex(floatvalue), "Ohm" )
        else:
            raise TypeError(f"Not able to initialise Impedance using a {type(value)}")
    
    # return a machine readable representation of a Impedance
    def __repr__(self):
        return( f"Impedance({self.value})" )  
        
    # negation of an Impedance   
    # returns a Impedance object
    def __neg__(self):
        return( Impedance( -self.value ) )
    
    # adding two Impedance    
    # returns a Impedance object
    def __add__(self, other):
        thistype = type(self)
        return( Impedance( self.value + other.value ) )
    
    # subtracting two Impedance  
    # returns a Impedance object
    def __sub__(self, other):
        return( Impedance( self.value - other.value ) ) 
        
    # multiplication of an Impedance times number returns an Impedance
    # multiplication of an Impedance times another Impedance returns a float
    def __mul__(self,other):
        if isinstance(other, ( float, int )): 
            return( Impedance( self.value * other) )
        elif isinstance(other, Impedance):
            return( self.value * other.value )
        else:
            raise TypeError(f"Cannot multiply {type(self)} with {type(other)}")
    
    # multiplication in reverse order
    __rmul__ = __mul__
    
    # division of an Impedance by number returns an Impedance
    # division of an Impedance by another Impedance returns a float
    def __truediv__(self,other):
        if isinstance(other, ( float, int )): 
            return( Impedance( self.value / other ) )
        elif isinstance(other, Impedance):
            return( self.value / other.value )
        else:
            raise TypeError(f"Cannot divide {type(self)} by {type(other)}")
    
    # division in reverse order returns a float
    def __rtruediv__(self,other):
        if isinstance(other, ( float, int )): 
            return( other / self.value )
        elif isinstance(other, Impedance):
            return( other.value / self.value )
        else:
            raise TypeError(f"Cannot divide {type(other)} by {type(self)}")
        
        
        
        
    # instance method to calculate parallel Impedance of this instance with n other Impedances
    def parallelwith(self, *impedances):
        return( Impedance.parallel( self, *impedances ) ) 
                  
    
    # static method to calculate equivalent impedances of n parallel impedances
    @staticmethod
    def parallel(*impedances): 
        sumofinverse = sum( [ 1 / z.value for z in impedances] )
        return( Impedance( complex( 1 / sumofinverse ) ) )




# -------------------------------------------------------        
# class for a resistance inherits from Impedance as a special case
# -------------------------------------------------------
class Resistance(Impedance):
    
    # value is the resistance value in Ohm
    def __init__(self, value = 0):
        super().__init__( value )
        
    # return a machine readable representation of a Resistance
    def __repr__(self):
        return( f"Resistance({self.value})" )  
        
     

# -------------------------------------------------------        
# class for a capacitance inherits from Electricalelement
# -------------------------------------------------------
class Capacitance(Electricalelement):
    
    # value is the capacitance value in Farad
    def __init__(self, value = 0):
        super().__init__( value, "F" )
        
    # return a machine readable representation of a Capacitance
    def __repr__(self):
        return( f"Capacitance({self.value})" )  
        
    # negation of an Capacitance   
    # returns a Capacitance object
    def __neg__(self):
        return( Capacitance( -self.value) )
    
    # adding two Capacitance    
    # returns a Capacitance object
    def __add__(self, other):
        return( Capacitance( self.value + other.value) )
    
    # subtracting two Capacitance  
    # returns a Capacitance object
    def __sub__(self, other):
        return( Capacitance( self.value - other.value) ) 
        
    # multiplication of an Capacitance times number returns an Capacitance
    # multiplication of an Capacitance times another Capacitance returns a float
    def __mul__(self,other):
        if isinstance(other, ( float, int )): 
            return( Capacitance( self.value * other) )
        elif isinstance(other, Capacitance):
            return( self.value * other.value )
        else:
            raise TypeError(f"Cannot multiply {type(self)} with {type(other)}")
    
    # multiplication in reverse order
    __rmul__ = __mul__
    
    # division of an Capacitance by number returns an Capacitance
    # division of an Capacitance by another Capacitance returns a float
    def __truediv__(self,other):
        if isinstance(other, ( float, int )): 
            return( Capacitance( self.value / other) )
        elif isinstance(other, Capacitance):
            return( self.value / other.value )
        else:
            raise TypeError(f"Cannot divide {type(self)} by {type(other)}")
    
    # division in reverse order returns a float
    def __rtruediv__(self,other):
        if isinstance(other, ( float, int )): 
            return( other / self.value )
        elif isinstance(other, Capacitance):
            return( other.value / self.value )
        else:
            raise TypeError(f"Cannot divide {type(other)} by {type(self)}")
        
    
    
    # return an Impedance object representing the frequency dependant impedance        
    def getimpedance(self, frequency):
        Xc = 1 / ( 2.0 * math.pi * frequency * self.value )
        Zc = complex( 0, -Xc )
        return( Impedance( Zc ) )
       

    # instance method to calculate series capacitance of this instance with n other Capacitance
    def serieswith(self, *capacitances):
        return( Capacitance.series( self, *capacitances ) ) 
          
    
    # static method to calculate equivalent capacitance of n parallel Capacitance
    @staticmethod
    def series(*capacitances): 
        sumofinverse = math.fsum( [ 1 / c.value for c in capacitances] )
        return( Capacitance( 1 / sumofinverse ) )


# -------------------------------------------------------        
# class for a inductance inherits from Electricalelement
# -------------------------------------------------------
class Inductance(Electricalelement):
    
    # value is the Inductance value in Henry
    def __init__(self, value = 0):
        super().__init__( value, "H" )
        
    # return a machine readable representation of a Inductance
    def __repr__(self):
        return( f"Inductance({self.value})" )  
        
    # negation of an Inductance   
    # returns a Inductance object
    def __neg__(self):
        return( Inductance( -self.value) )
    
    # adding two Inductance    
    # returns a Inductance object
    def __add__(self, other):
        return( Inductance( self.value + other.value) )
    
    # subtracting two Inductance  
    # returns a Inductance object
    def __sub__(self, other):
        return( Inductance( self.value - other.value) ) 
        
    # multiplication of an Inductance times number returns an Inductance
    # multiplication of an Inductance times another Inductance returns a float
    def __mul__(self,other):
        if isinstance(other, ( float, int )): 
            return( Inductance( self.value * other) )
        elif isinstance(other, Inductance):
            return( self.value * other.value )
        else:
            raise TypeError(f"Cannot multiply {type(self)} with {type(other)}")
    
    # multiplication in reverse order
    __rmul__ = __mul__
    
    # division of an Inductance by number returns an Inductance
    # division of an Inductance by another Inductance returns a float
    def __truediv__(self,other):
        if isinstance(other, ( float, int )): 
            return( Inductance( self.value / other) )
        elif isinstance(other, Inductance):
            return( self.value / other.value )
        else:
            raise TypeError(f"Cannot divide {type(self)} by {type(other)}")
    
    # division in reverse order returns a float
    def __rtruediv__(self,other):
        if isinstance(other, ( float, int )): 
            return( other / self.value )
        elif isinstance(other, Inductance):
            return( other.value / self.value )
        else:
            raise TypeError(f"Cannot divide {type(other)} by {type(self)}")
        
    
    
    # return an Impedance object representing the frequency dependant impedance        
    def getimpedance(self, frequency):
        Xl = 2.0 * math.pi * frequency * self.value 
        Zc = complex( 0, Xl )
        return( Impedance( Zc ) )
       

    # instance method to calculate parallel Inductance of this instance with n other Inductance
    def parallelwith(self, *inductances):
        return( Inductance.parallel( self, *inductances ) ) 
          
    
    # static method to calculate equivalent Inductance of n parallel Inductance
    @staticmethod
    def parallel(*inductances): 
        sumofinverse = math.fsum( [ 1 / c.value for c in inductances] )
        return( Inductance( 1 / sumofinverse ) )


# ----------------------------------------------------------
# generic class for a voltage
# ----------------------------------------------------------
class Voltage(Electricalelement):
    
    # value is the voltage value in Volt
    def __init__(self, value = 0):
        if isinstance( value, complex ):
            super().__init__( value, "V" )
        elif isinstance( value, (int, float) ):
            super().__init__( complex(value), "V" )
        elif isinstance(value, str):
            floatvalue = Electricalelement.metricprefixtofloat(value)
            super().__init__( complex(floatvalue), "V" )
        else:
            raise TypeError(f"Not able to initialise Voltage using a {type(value)}")
        
    # return a machine readable representation of a Capacitance
    def __repr__(self):
        return( f"Voltage({self.value})" )  
        
    # negation of an Voltage   
    # returns a Voltage object
    def __neg__(self):
        return( Voltage( -self.value ) )
    
    # adding two Voltage    
    # returns a Voltage object
    def __add__(self, other):
        thistype = type(self)
        return( Voltage( self.value + other.value ) )
    
    # subtracting two Voltage  
    # returns a Voltage object
    def __sub__(self, other):
        return( Voltage( self.value - other.value ) ) 

    # multiplication of an Voltage times number returns an Voltage
    # multiplication of an Voltage times another Voltage returns a Complex
    def __mul__(self,other):
        if isinstance(other, ( float, int )): 
            return( Voltage( self.value * other) )
        elif isinstance(other, Voltage):
            return( self.value * other.value )
        else:
            raise TypeError(f"Cannot multiply {type(self)} with {type(other)}")
    
    # multiplication in reverse order
    __rmul__ = __mul__
    
    # division of an Voltage by number returns an Voltage
    # division of an Voltage by another Voltage returns a Complex
    def __truediv__(self,other):
        if isinstance(other, ( float, int )): 
            return( Voltage( self.value / other ) )
        elif isinstance(other, Voltage):
            return( self.value / other.value )
        elif isinstance(other, Impedance):
            return( Current( self.value / other.value ) )
        elif isinstance(other, Current):
            return( Impedance( self.value / other.value ) )
        else:
            raise TypeError(f"Cannot divide {type(self)} by {type(other)}")
    
    # division in reverse order returns a Complex
    def __rtruediv__(self,other):
        if isinstance(other, ( float, int )): 
            return( other / self.value )
        elif isinstance(other, Voltage):
            return( other.value / self.value )
        else:
            raise TypeError(f"Cannot divide {type(other)} by {type(self)}")


# ----------------------------------------------------------
# generic class for a current
# ----------------------------------------------------------
class Current(Electricalelement):
    
    # value is the current value in Volt
    def __init__(self, value = 0):
        if isinstance( value, complex ):
            super().__init__( value, "A" )
        elif isinstance( value, (int, float) ):
            super().__init__( complex(value), "A" )
        elif isinstance(value, str):
            floatvalue = Electricalelement.metricprefixtofloat(value)
            super().__init__( complex(floatvalue), "A" )
        else:
            raise TypeError(f"Not able to initialise Current using a {type(value)}")
        
    # return a machine readable representation of a Current
    def __repr__(self):
        return( f"Current({self.value})" )  
        
    # negation of an Current   
    # returns a Current object
    def __neg__(self):
        return( Current( -self.value ) )
    
    # adding two Current    
    # returns a Current object
    def __add__(self, other):
        thistype = type(self)
        return( Current( self.value + other.value ) )
    
    # subtracting two Current  
    # returns a Current object
    def __sub__(self, other):
        return( Current( self.value - other.value ) ) 

    # multiplication of an Current times number returns an Current
    # multiplication of an Current times another Current returns a Complex
    # multiplication of an Current times a Impedance returns a Voltage
    def __mul__(self,other):
        if isinstance(other, ( float, int )): 
            return( Current( self.value * other) )
        elif isinstance(other, Current):
            return( self.value * other.value )
        elif isinstance(other, Impedance ):
            return( Voltage( self.value * other.value ) )
        else:
            raise TypeError(f"Cannot multiply {type(self)} with {type(other)}")
    
    # multiplication in reverse order
    __rmul__ = __mul__
    
    # division of an Current by number returns an Current
    # division of an Current by another Current returns a Complex
    def __truediv__(self,other):
        if isinstance(other, ( float, int )): 
            return( Current( self.value / other ) )
        elif isinstance(other, Current):
            return( self.value / other.value )
        else:
            raise TypeError(f"Cannot divide {type(self)} by {type(other)}")
    
    # division in reverse order returns a Complex
    # division of a Voltage by a Current returns an Impedance
    def __rtruediv__(self,other):
        if isinstance(other, ( float, int )): 
            return( other / self.value )
        elif isinstance(other, Voltage):
            return( Impedance ( other.value / self.value ) )
        else:
            raise TypeError(f"Cannot divide {type(other)} by {type(self)}")


# --- tests --------------------------        
if __name__ == "__main__":
    import test_elements
