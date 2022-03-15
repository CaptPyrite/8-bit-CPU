import os
import subprocess
import sys
import time

def delete_file(filename):
  os.remove(filename)

def rm_all_keys(x):
  return x.replace("[","").replace("]","").replace(" ","").replace("\n","")

def string2bin(string):
  return ''.join(bin(ord(c)) for c in string).replace('b','')

def assemble(filename):
  machine_exe_code = open("m.py","w")
  machine_exe_code.write("import CPU\n")
  machine_exe_code.write("adder = CPU.ADDER()\n")
  machine_exe_code.write("ram = CPU.RAM()\n")


  with open(filename,"r") as file:
    for i in file:
      if "RSTR:" in i:
        data = rm_all_keys(i).partition(":")[2].split(",")[0]
        location = rm_all_keys(i).partition(":")[2].split(",")[1].replace("$","")
        
        
        if "b" in data:
          data = string2bin(i.partition(":")[2].split(",")[0].replace("[","").replace("]","").partition("b")[2].replace('"',""))
          machine_exe_code.write("ram.write('{1}','{0}', 1)\n".format(data,location))
          
        else:
          machine_exe_code.write("CPU.CORE.cpu_ram(['{1}','{0}'])\n".format(bin(int(data))[2:].zfill(8)[::-1],location))
          
      elif "STR:" in i:
        data = rm_all_keys(i).partition(":")[2].split(",")[0]
        location = rm_all_keys(i).partition(":")[2].split(",")[1]
        machine_exe_code.write("CPU.CORE.cpu_ram(['{1}','{0}'])\n".format(bin(int(data))[2:].zfill(8)[::-1],location))
          
      elif "ADD:" in i:
        loc1 = rm_all_keys(i).partition(":")[2].split(",")[0]
        loc2 = rm_all_keys(i).partition(":")[2].split(",")[1]
        RAM_loc = rm_all_keys(i).partition("$")[2]
        code = """mem_{0} = adder.ALU([int(x) for x in list(str(CPU.CORE.get_rdata()['{1}']))],
                      [int(y) for y in list(str(CPU.CORE.get_rdata()['{2}']))],0)
  ram.write('{0}',mem_{0},1)\n""".format(RAM_loc,loc1,loc2[:loc2.index("$")])
        machine_exe_code.write(code)

      elif "SUB:" in i:
        loc1 = rm_all_keys(i).partition(":")[2].split(",")[0]
        loc2 = rm_all_keys(i).partition(":")[2].split(",")[1]
        RAM_loc = rm_all_keys(i).partition("$")[2]
        code = """mem_{0} = adder.ALU([int(x) for x in list(str(CPU.CORE.get_rdata()['{1}']))],
                      [int(y) for y in list(str(CPU.CORE.get_rdata()['{2}']))],1)
  ram.write('{0}',mem_{0},1)\n""".format(RAM_loc,loc1,loc2[:loc2.index("$")])
        machine_exe_code.write(code)
        
      elif "PRNT:" in i:
        loc1 = rm_all_keys(i).partition(":")[2].split(",")[0]
        loc2 = rm_all_keys(i).partition(":")[2].split(",")[1]
        if "add" in loc2:
          machine_exe_code.write("print(''.join('%s' % v for v in ram.read('{0}')['output'][::-1]))\n".format(loc1))
        elif "sub" in loc2:
          machine_exe_code.write("print(''.join('%s' % v for v in ram.read('{0}')['output'][::-1]))\n".format(loc1))
        elif "ptr" in loc2:
          machine_exe_code.write("print(ram.read('{0}'))\n".format(loc1.replace("$", "")))
          
        elif "ascii" in loc2:
          if ":" in loc1:
            missing_locs = [str(hex(i)) for i in range(int(loc1.split(":")[0],0),int(loc1.split(":")[1],0)+1)]
            machine_exe_code.write("printing_ascii_from_ram = []\n")
            for i in missing_locs:
              machine_exe_code.write("printing_ascii_from_ram.append(ram.read('{0}'))\n".format(i))
            machine_exe_code.write("print(''.join([chr(int(i, 2)) for i in printing_ascii_from_ram]))\n")
            machine_exe_code.write("del printing_ascii_from_ram")
          
          else:
            #
            machine_exe_code.write("print(chr(int(ram.read('{0}'),2)))\n".format(loc1.replace("$","")))
            
      elif "MOVL:" in i:
        loc1 = rm_all_keys(i).rpartition(":")[2].split(",")[0]
        loc2 = rm_all_keys(i).rpartition(":")[2].split(",")[1]
        machine_exe_code.write("CPU.CORE.cpu_ram(['{0}',CPU.CORE.get_rdata()['{1}']])\n".format(loc2,loc1))
        machine_exe_code.write("CPU.CORE.drain_cpu_ram('{0}')\n".format(loc1))
        
      elif "MOV:" in i:
        loc1 = rm_all_keys(i).rpartition(":")[2].split(",")[0].replace("$","")
        loc2 = rm_all_keys(i).rpartition(":")[2].split(",")[1].replace("$","")
        machine_exe_code.write("read_loc_{0} = ram.read('{0}')\n".format(loc1))
        machine_exe_code.write("ram.write('{0}',read_loc_{1},1)\n".format(loc2,loc1))
        machine_exe_code.write("ram.drain('{0}',1)\n".format(loc1))

      elif "LDA:" in i:
        loc1 = rm_all_keys(i).rpartition(":")[2].split(",")[0].replace("$","")
        loc2 = rm_all_keys(i).rpartition(":")[2].split(",")[1]
        machine_exe_code.write("CPU.CORE.cpu_ram(['{0}',ram.read('{1}')])\n".format(loc2,loc1))
      
  machine_exe_code.close()
     
'''
if __name__ == "__main__":
  assemble(sys.argv[1][2:])
  subprocess.call(["python", "m.py"])
  
  try:
    if sys.argv[2][1:] == "-kf":
      pass
    else:
      delete_file("m.py")
  except IndexError:
    delete_file("m.py") 
'''
assemble("hello_world.lasm")
subprocess.call(["python", "m.py"])
delete_file("m.py") 