import pika
import time
import mysql.connector

while True:
	try:
		connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq-server'))
		channel = connection.channel()
		break
	except:
		time.sleep(5)
channel.queue_declare(queue="trylogin")

def on_request(ch, method, properties, body):
	while True:
		try:
			print("Tentando")
			mydb = mysql.connector.connect(host="db", user="fernando", passwd="fernando", database="data.db")
			break
		except:
			time.sleep(5)

	mycursor = mydb.cursor()
	comand = "SELECT * FROM Users WHERE User =%s"
	Body = body.decode("utf-8").split("!@!")
	user = (Body[0],)

	mycursor.execute(comand, user)
	myresult = mycursor.fetchall()

	try:
		mycursor.execute(comand, user)
		myresult = mycursor.fetchall()

		for linha in myresult:
			if linha[1].decode("utf-8") == Body[1]:
				resposta = "True!@!QS2BP7G39nzhdu4suPdy8cGkPVymvxzr"
				break
			else:
				resposta = "False"
	except:
		resposta = "False"

	ch.basic_publish(exchange='',routing_key=properties.reply_to,properties=pika.BasicProperties(correlation_id = \
														properties.correlation_id),body=resposta)
	ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue="trylogin", on_message_callback=on_request)

channel.start_consuming()
