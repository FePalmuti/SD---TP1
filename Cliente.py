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
	print("Ping: " + str(intervalo_de_tempo.seconds) + "." + str(intervalo_de_tempo.microseconds).zfill(6))
