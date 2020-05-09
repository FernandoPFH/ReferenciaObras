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
			mydb = mysql.connector.connect(host="rabbitmq-server", user="main", passwd="main", database="data.db")
			break
		except:
			time.sleep(5)

	print(body)

	mycursor = mydb.cursor()
	comand = "SELECT * FROM 'Users' WHERE 'User' =%s"
	user = (body["user"],)

	try:
		mycursor.execute(comand, user)
		myresult = mycursor.fetchall()

		for linha in myresult:
			if linha[2] == body["password"]:
				resposta = {"boo": True, "code":"QS2BP7G39nzhdu4suPdy8cGkPVymvxzr"}
				break
			else:
				resposta = {"boo":False}
	except:
		resposta = {"boo":False}

	ch.basic_publish(exchange='',routing_key=properties.reply_to,properties=pika.BasicProperties(correlation_id = \
														properties.correlation_id),body=resposta)
	ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue="trylogin", on_message_callback=on_request)

channel.start_consuming()
