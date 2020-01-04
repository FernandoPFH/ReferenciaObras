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
			mydb = mysql.connector.connect(host="mysqlsrv-users", user="guest", passwd="guest", database="users.db")
			break
		except:
			time.sleep(5)

	mycursor = mydb.cursor()

	comand = "SELECT * FROM users WHERE user =%s"
	user = (body["userinfo"]["user"],)

	try:
		mycursor.execute(comand, user)
		myresult = mycursor.fetchall()

		for linha in myresult:
			if linha[1] == body["userinfo"]["user"] and linha[2] == body["userinfo"]["password"]:
				newuser = (body["newuserinfo"]["user"],)
				try:
					mycursor.execute(comand, newuser)
					myresult1 = mycursor.fetchall()
					for linha1 in myresult1:
						if linha1[1] == body["newuserinfo"]:
							resposta = {"boo":False}
							break
						else:
							comand_insert = "INSERT INTO users (user, password) VALUES (%s, %s)"
							input = (body["newuserinfo"]["user"],body["newuserinfo"]["password"])
							mycursor.execute(comand_insert,input)
							mydb.commit()
				except:
					comand_insert = "INSERT INTO users (user, password) VALUES (%s, %s)"
					input = (body["newuserinfo"]["user"],body["newuserinfo"]["password"])
					mycursor.execute(comand_insert,input)
					mydb.commit()
			else:
				resposta = {"boo":False}
	except:
		resposta = {"boo":False}

	ch.basic_publish(exchange='',routing_key=properties.reply_to,properties=pika.BasicProperties(correlation_id = \
														properties.correlation_id),body=resposta)
	ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue="newlogin", on_message_callback=on_request)

channel.start_consuming()