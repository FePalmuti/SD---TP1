import socket
from datetime import datetime

ip = "127.0.0.1"
porta = 7000

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
	input("Digite \"enter\" para pingar.")

	tempo_inicial = datetime.now()
	sock.sendto(bytearray("Testando ping", "utf-8"), (ip, porta))
	sock.recvfrom(1024)
	tempo_final = datetime.now()
	intervalo_de_tempo = tempo_final - tempo_inicial

	#Conversao de datetime para float
	intervalo_de_tempo = intervalo_de_tempo.microseconds
	print("Ping: " + str(intervalo_de_tempo) + " microsegundos.")
	#Conversao de microsegundos para segundos
	intervalo_de_tempo = intervalo_de_tempo/1000000

	vazao = 1024/intervalo_de_tempo
	#Conversao de B/s para MB/s
	vazao = vazao/1048576
	print("Vazao: " + str(round(vazao, 2)) + " MB/s.\n")
