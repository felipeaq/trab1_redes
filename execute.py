import os
os.system ('sudo rm result.txt')
for i in range (0,380000,5000):
    os.system ('sudo python testes.py {}'.format(i))
