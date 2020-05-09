import pika
import uuid
from flask import Flask,request
import json
app = Flask(__name__)

class Mensagem(object):
	def __init__(self, queue):
		self.queue = queue
		self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq-server'))
		self.channel = self.connection.channel()
		result = self.channel.queue_declare(queue='', exclusive=True)
		self.callback_queue = result.method.queue
		self.channel.basic_consume(queue=self.callback_queue,on_message_callback=self.on_response,auto_ack=True)

	def on_response(self, ch, method, props, body):
		if self.corr_id == props.correlation_id:
			self.response = body.decode("utf-8")

	def call(self, mensagem):
		self.response = None
		self.corr_id = str(uuid.uuid4())
		self.channel.basic_publish(exchange='',routing_key=self.queue,properties=pika.BasicProperties(reply_to=self.callback_queue,correlation_id=self.corr_id),body=mensagem)
		while self.response is None:
			self.connection.process_data_events()
		return self.response

@app.route('/',methods = ['GET'])
def main_page():
	return 'Hello!!!'

@app.route('/login/',methods = ['POST', 'GET'])
def login():
	if request.method == 'GET':
		User = request.args.get('user') + "!@!" + request.args.get('password')
		mensagem = Mensagem(queue="trylogin")
		response = mensagem.call(mensagem=User).split("!@!")
		if response[0] == "True":
			return response[1]
		elif response[0] == "False":
			return "Login Negado"

	elif request.method == 'POST':
		User = request.args.get('user') + "!@!" + request.args.get('password')
		NewUser = request.args.get('newuser') + "!@!" + request.args.get('newpassword')
		mensagem = Mensagem(queue="newlogin")
		response = mensagem.call(mensagem=User+"!@!"+NewUser)
		if response == "True":
			return "Novo usuario registrado com sucesso"
		elif response == "False":
			return "Erro ao registrar novo usuario"

@app.route('/QS2BP7G39nzhdu4suPdy8cGkPVymvxzr/obras/', methods = ['POST', 'GET'])
def obras():
	if request.method == 'GET':
		mensagem = Mensagem(queue="getobras")
		response = mensagem.call(mensagem="getobras")
		if response["boo"] == True:
			return response["obras"]
		elif response["boo"] == False:
			return "Erro ao tentar acessar as obras"

	elif request.method == 'POST':
		dados = {"uso":request.args.get('uso'), "obra":json.loads(request.args.get('obra'))}
		mensagem = Mensagem(queue="setobras")
		response = mensagem.call(mensagem=dados)
		if response["boo"] == True:
			if response["uso"] == "remover":
				return "Obra removida com sucesso"
			elif response["uso"] == "adicionar":
				return "Obra adicionada com sucesso"
			elif response["uso"] == "mudar":
				return "Obra alterada com sucesso"
		elif response["boo"] == False:
			if response["uso"] == "remover":
				return "Erro ao tentar remover obra"
			elif response["uso"] == "adicionar":
				return "Erro ao tentar adicionar obra"
			elif response["uso"] == "mudar":
				return "Erro ao tentar alterar obra"

@app.route('/QS2BP7G39nzhdu4suPdy8cGkPVymvxzr/referencia/', methods = ['POST', 'GET'])
def referencia():
	if request.method == 'GET':
		mensagem = Mensagem(queue="getreferencia")
		response = mensagem.call(mensagem="getreferencia")
		if response["boo"] == True:
			return response["referencia"]
		elif response["boo"] == False:
			return "Erro ao tentar acessar a referencia"

	elif request.method == 'POST':
		dados = {"referencia":json.loads(request.args.get('referencia'))}
		mensagem = Mensagem(queue="setreferencia")
		response = mensagem.call(mensagem=dados)
		if response["boo"] == True:
			return "Referencia mudada com sucesso"
		elif response["boo"] == False:
			return "Erro ao tentar mudar referencia"

if __name__ == '__main__':
	app.run(host='0.0.0.0')