import subprocess
import re
# TEST
first = input("Enter the start of the IP range: ")
last = input("Enter the end of the IP range: ")

def get_host(x):
    dot_counter = 0
    pos_counter = 0
    for i in x:
        if i == ".":
            dot_counter = dot_counter + 1
        if dot_counter == 3:
            return (x[0:pos_counter+1], x[pos_counter+1:])
        pos_counter += 1
        
network, first_host = get_host(first)
network, last_host = get_host(last)

print("Network: ", network)
print("Start: ", first_host)
print("End", last_host)

empty_string = ""
counter = 0

for i in range(int(first_host), int(last_host)):
    process = subprocess.getoutput(f"ping -n 1 {network+str(i)}")
    empty_string += process
    string_needed = re.compile(r"TTL=")
    mo = string_needed.search(empty_string)
    try:
        if mo.group() == "TTL=":
            print("HOST IS UP")
    except:
        print("HOST IS DOWN")
    
    empty_string = ""
print("completed")
