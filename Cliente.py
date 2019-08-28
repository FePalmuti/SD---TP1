import socket
from datetime import datetime

ip = "127.0.0.1"
porta = 7000
timeout = 200 #Microsegundos

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
	qnt_pacotes_perdidos = 0
	somatorio_rtt = 0
	somatorio_vazao = 0

	input("Digite \"enter\" para pingar.")

	for i in range(100):
		tempo_inicial = datetime.now()
		sock.sendto(bytearray("Testando ping", "UTF-8"), (ip, porta))
		sock.recvfrom(1024)
		tempo_final = datetime.now()
		intervalo_de_tempo = tempo_final - tempo_inicial

		#O intervalo de tempo passa a ser em microsegundos
		intervalo_de_tempo = intervalo_de_tempo.microseconds
		if(intervalo_de_tempo > timeout):
			#Contabiliza o pacote perdido
			qnt_pacotes_perdidos += 1
		else:
			#Contabiliza o RTT
			somatorio_rtt += intervalo_de_tempo
			#Conversao de microsegundos para segundos
			intervalo_de_tempo = intervalo_de_tempo/1000000
			#Calculo da vazao
			vazao = 1024/intervalo_de_tempo
			#Conversao de B/s para MB/s
			vazao = vazao/1048576
			#Contabiliza a vazao
			somatorio_vazao += vazao

	rtt_medio = somatorio_rtt / (100 - qnt_pacotes_perdidos)
	print("RTT medio: " + str(int(rtt_medio)) + " microsegundos.")
	vazao_media = somatorio_vazao / (100 - qnt_pacotes_perdidos)
	print("Vazao: " + str(round(vazao_media, 2)) + " MB/s.")
	print("Taxa de perda: " + str(qnt_pacotes_perdidos) + "%\n")
