locations = {"R1":0,
             "R2":0,
             "R3":0,
             "R4":0}

def not_gate(BIN):
  return(not BIN)

def and_gate(BIN1,BIN2):
    if BIN1 == 1 and BIN2 == 1:
        return(1)
    else:
        return(0)
      
def or_gate(BIN1,BIN2):
    if BIN1 == 1 or BIN2 ==1:
        return(1)
    else:
        return(0)

def xor_gate(BIN1,BIN2):
    if BIN1 != BIN2:
        return 1
    else:
        return 0
  
  
class ADDER:
  def __init__(self):
    self.ASM = 0
  
  def simple_adder(self,i1,i2,i3):
    xor1 = xor_gate(i1,i2)
    and1 = and_gate(i1,i2)
    xor2 = xor_gate(xor1,i3)
    and2 = and_gate(xor1,i3)
    or1 = or_gate(and1,and2)
    #      sum  carry
    return(xor2,or1)
    
  def Bit_8_adder(self,i1,i2,i3,i4,i5,i6,i7,i8, x1,x2,x3,x4,x5,x6,x7,x8, r):
      Adder1 = self.simple_adder(i1,x1,r)
      Adder2 = self.simple_adder(i2,x2,Adder1[1])
      Adder3 = self.simple_adder(i3,x3,Adder2[1])
      Adder4 = self.simple_adder(i4,x4,Adder3[1])
      Adder5 = self.simple_adder(i5,x5,Adder4[1])
      Adder6 = self.simple_adder(i6,x6,Adder5[1])
      Adder7 = self.simple_adder(i7,x7,Adder6[1])
      Adder8 = self.simple_adder(i8,x8,Adder7[1])
      
      return(Adder1[0],
             Adder2[0],
             Adder3[0],
             Adder4[0],
             Adder5[0],
             Adder6[0],
             Adder7[0],
             Adder8[0],
             Adder8[1])
  
  def ALU(self,state1,state2,SUB):
    l1_input1 = state1[0]
    l1_input2 = state1[1]
    l1_input3 = state1[2]
    l1_input4 = state1[3]
    l1_input5 = state1[4]
    l1_input6 = state1[5]
    l1_input7 = state1[6]
    l1_input8 = state1[7]
    l2_input1 = xor_gate(state2[0],SUB)
    l2_input2 = xor_gate(state2[1],SUB)
    l2_input3 = xor_gate(state2[2],SUB)
    l2_input4 = xor_gate(state2[3],SUB)
    l2_input5 = xor_gate(state2[4],SUB)
    l2_input6 = xor_gate(state2[5],SUB)
    l2_input7 = xor_gate(state2[6],SUB)
    l2_input8 = xor_gate(state2[7],SUB)
    
    BIT_8 = self.Bit_8_adder(l1_input1,l1_input2,l1_input3,l1_input4,
                        l1_input5,l1_input6,l1_input7,l1_input8,
                        l2_input1,l2_input2,l2_input3,l2_input4,
                        l2_input5,l2_input6,l2_input7,l2_input8,SUB)
    
    
    
    return({"output":BIT_8,"flags":(BIT_8[8],BIT_8[0],int(sum(BIT_8)==0))})
    
class RAM:
  def __init__(self):
    self.o = {}
    self.registers = self.multiplexed_register()

  def latch(self,state, set):
    if set == 1:
      if state == 1:
        return(1)
        
      elif state == 0:
        return(0)
      
    elif set == 0:
      return(0)
  
  def latch_8_bit(self,state1,state2,state3,state4,state5,state6,state7,state8,set):
    latch1 = self.latch(state1,set)
    latch2 = self.latch(state2,set)
    latch3 = self.latch(state3,set)
    latch4 = self.latch(state4,set)
    latch5 = self.latch(state5,set)
    latch6 = self.latch(state6,set)
    latch7 = self.latch(state7,set)
    latch8 = self.latch(state8,set)
    
    return(latch1,latch2,latch3,latch4,latch5,latch6,latch7,latch8)
   
  def multiplexed_register(self):
    for i in range(1600):
      self.o[hex(i)] = (0,0,0,0,0,0,0,0,0)
    
    
  def write(self,ADRESS,DATA,CLOCK):
    if CLOCK == 1:
      self.o[ADRESS]=DATA
    else:
        self.o[ADRESS]=(0,0,0,0,0,0,0,0)
  
  def read(self,ADRESS):
    return self.o[ADRESS]
  
  def drain(self,ADRESS,CLOCK):
    if CLOCK == 1:
      self.registers[ADRESS]=(0,0,0,0,0,0,0,0)
    else:
      pass
    
class CORE:  
  global locations
  def cpu_ram(loc_val):
    global locations
    if loc_val[0] in locations:
      locations[loc_val[0]] = loc_val[1]
      return 1
    else:
      return 0
  
  def get_rdata():
    global locations
    return locations

  def drain_cpu_ram(loc):
    global locations
    locations[loc] = 0