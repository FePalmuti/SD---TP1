import socket
import time

class Cliente:
	ip = "127.0.0.1"
	porta = 7000
	timeout = 0.7 #Segundos
	qnt_pacotes = 10
	lista_rtts = []

	def __init__(self):
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.sock.settimeout(self.timeout)

		op = self.perguntar_opcao_ao_usuario()
		while op != "x":
			self.qnt_pacotes_retornados = 0
			self.qnt_pacotes_perdidos = 0

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
							print("Pacote", str(id + 1), "retornou em", intervalo_de_tempo, "s.")
							self.qnt_pacotes_retornados += 1
							id_incorrespondente = False

				except socket.timeout:
					print("Pacote", str(id + 1), "perdido!")
					self.qnt_pacotes_perdidos += 1

			self.gerar_relatorio()
			op = self.perguntar_opcao_ao_usuario()

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
		print("RTT medio:", rtt_medio, "s")
		return rtt_medio

	def calcular_vazao(self, rtt_medio):
		if rtt_medio != 0:
			vazao = 1024 / rtt_medio
		else:
			vazao = 0
		print("Vazao:", vazao, "B/s")

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
