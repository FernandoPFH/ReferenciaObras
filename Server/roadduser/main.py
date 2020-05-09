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

channel.queue_declare(queue="newlogin")

def on_request(ch, method, properties, body):
	while True:
		try:
			mydb = mysql.connector.connect(host="db", user="fernando", passwd="fernando", database="data.db")
			break
		except:
			time.sleep(5)

	mycursor = mydb.cursor()

	Body = body.decode("utf-8").split("!@!")

	comand = "SELECT * FROM Users WHERE User =%s"
	user = (Body[0],)

	resposta ="False"

	#try:
	if True:
		mycursor.execute(comand, user)
		myresult = mycursor.fetchall()

		for linha in myresult:
			if linha[0].decode("utf-8") == Body[0] and linha[1].decode("utf-8") == Body[1]:
				newuser = (Body[2],)
				try:
					mycursor.execute(comand, newuser)
					myresult1 = mycursor.fetchall()
					for linha1 in myresult1:
						if linha1[0].decode("utf-8") == Body[2]:
							resposta = "False"
							break
						else:
							comand_insert = "INSERT INTO Users (User, Password) VALUES (%s, %s)"
							input_ = (Body[2],Body[3])
							mycursor.execute(comand_insert,input_)
							mydb.commit()
							resposta = "True"
				except:
					comand_insert = "INSERT INTO Users (User, Password) VALUES (%s, %s)"
					input_ = (Body[2],Body[3])
					mycursor.execute(comand_insert,input_)
					mydb.commit()
					resposta = "True"
			else:
				resposta = "False"
	#except:
	#	resposta = "False"

	ch.basic_publish(exchange='',routing_key=properties.reply_to,properties=pika.BasicProperties(correlation_id = \
														properties.correlation_id),body=resposta)
	ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue="newlogin", on_message_callback=on_request)

channel.start_consuming()