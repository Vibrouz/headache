import sys
if sys.argv<2:
    print("The file format should be main.py <filename>")

with open(sys.argv[1],"rb") as file:
    magic_string= file.read(16)

with open("COnfig-file", "r") as config_file:
    if config_file.get(magic_string):
       print("your Extension is : ${config_file.get(magic_string)}")
     
