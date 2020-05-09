import pika
import time
import json
import mysql.connector

while True:
	try:
		connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq-server'))
		channel = connection.channel()
		break
	except:
		time.sleep(5)

channel.queue_declare(queue="setobras")

def on_request(ch, method, properties, body):
	while True:
		try:
			mydb = mysql.connector.connect(host="db", user="fernando", passwd="fernando", database="data.db")
			break
		except:
			time.sleep(5)

	body = body.decode("utf-8")

	Uso = body.split("!@!")[0]
	Obra = json.loads(body.split("!@!")[1])

	if Uso == "remover":
		try:
			mycursor = mydb.cursor()
			comand = "DELETE FROM Obras WHERE id = %i"
			val = (Obra["id"],)
			mycursor.execute(comand,val)
			mydb.commit()
			resposta = "True"+ "!@!" +"remover"
		except:
			resposta = "False"+ "!@!" +"remover"
	elif Uso == "adicionar":
		try:
			mycursor = mydb.cursor()
			comand = "INSERT INTO Obras (Nome, Info) VALUES (%s, %s)"
			val = (Obra["Nome"],json.dumps(Obra["Info"]))
			mycursor.execute(comand,val)
			mydb.commit()
			resposta = "True"+ "!@!" +"adicionar" 
		except:
			resposta = "False"+ "!@!" +"adicionar"
	elif Uso == "mudar":
		try:
			mycursor = mydb.cursor()
			comand = "UPDATE Obras SET (Nome, Info) = (%s,%s) WHERE id = %i"
			val = (Obra["Nome"],json.dumps(Obra["Info"]),Obra["id"])
			mycursor.execute(comand,val)
			mydb.commit()
			resposta = "True"+ "!@!" +"mudar" 
		except:
			resposta = "False"+ "!@!" +"mudar" 

	ch.basic_publish(exchange='',routing_key=properties.reply_to,properties=pika.BasicProperties(correlation_id = \
														properties.correlation_id),body=resposta)
	ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue="setobras", on_message_callback=on_request)

channel.start_consuming()
