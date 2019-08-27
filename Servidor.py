import socket

ip = ""
porta = 7000

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((ip, porta))

while True:
	mensagem, endereco = sock.recvfrom(1024)
	print("Chegou!")
	sock.sendto(bytearray("Resposta ao teste", "utf-8"), (endereco))
