import socket

ip = ""
porta = 7000

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((ip, porta))
sock.listen(1)
conexao, ip_cliente = sock.accept()

while True:
	conexao.recv(1024)
	print("Chegou!")
	resposta = "Respondendo ao teste"
	conexao.send(resposta.encode())
#
