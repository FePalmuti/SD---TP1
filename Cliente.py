import socket
import time

class Cliente:
	ip = "127.0.0.1"
	porta = 7000
	timeout = 0.7 #Segundos
	qnt_pacotes = 10

	def __init__(self):
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.sock.settimeout(self.timeout)
		self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 1024)

		op = self.perguntar_opcao_ao_usuario()
		while op != "x":
			self.qnt_pacotes_retornados = 0
			self.qnt_pacotes_perdidos = 0
			self.lista_rtts = []

			for id in range(self.qnt_pacotes):
				tempo_inicial = time.time()
				self.sock.sendto(str(id).encode(), (self.ip, self.porta))

				try:
					id_incorrespondente = True
					while id_incorrespondente:
						mensagem, endereco = self.sock.recvfrom(1024)
						id_recebido = int(mensagem.decode())
						if id_recebido == id:
							tempo_final = time.time()
							intervalo_de_tempo = tempo_final - tempo_inicial
							self.lista_rtts.append(intervalo_de_tempo)
							# O valor eh mostrado em milisegundos
							print("Pacote", str(id + 1), "retornou em",\
									round(intervalo_de_tempo * 1000, 2), "ms.")
							self.qnt_pacotes_retornados += 1
							id_incorrespondente = False

				except socket.timeout:
					print("Pacote", str(id + 1), "perdido!")
					self.qnt_pacotes_perdidos += 1

			self.gerar_relatorio()
			op = self.perguntar_opcao_ao_usuario()
		self.sock.close()

	def perguntar_opcao_ao_usuario(self):
		return input("Digite \"enter\" para pingar ou \"x\" para sair.\n")

	def calcular_rtt_medio(self):
		if self.qnt_pacotes_retornados != 0:
			somatorio_rtts = 0
			for tempo in self.lista_rtts:
				somatorio_rtts += tempo
			rtt_medio = somatorio_rtts / self.qnt_pacotes_retornados
		else:
			rtt_medio = 0
		# O valor eh mostrado em milisegundos
		print("RTT medio:", round(rtt_medio * 1000, 2), "ms")
		return rtt_medio

	def calcular_vazao(self, rtt_medio):
		if rtt_medio != 0:
			vazao = (1024 * 8) / (rtt_medio * 1048576)
		else:
			vazao = 0
		# O valor eh mostrado em Mb/s
		print("Vazao:", round(vazao, 4), "Mb/s")

	def calcular_taxa_perda(self):
		proporcao_perda = self.qnt_pacotes_perdidos / self.qnt_pacotes
		percentual_perda = proporcao_perda * 100
		percentual_perda = round(percentual_perda, 2)
		print("Taxa de perda:", percentual_perda, "%")

	def gerar_relatorio(self):
		print("---------------------------------------------------------------")
		rtt_medio = self.calcular_rtt_medio()
		self.calcular_vazao(rtt_medio)
		self.calcular_taxa_perda()
		print()


Cliente()
#
