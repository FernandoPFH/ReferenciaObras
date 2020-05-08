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

channel.queue_declare(queue="setobras")

def on_request(ch, method, properties, body):
	while True:
		try:
			mydb = mysql.connector.connect(host="mysqlsrv-obras", user="guest", passwd="guest", database="data.db")
			break
		except:
			time.sleep(5)

	if body["uso"] == "remover":
		try:
			mycursor = mydb.cursor()
			comand = "DELETE FROM obras WHERE id = %s"
			val = (body["obra"]["id"],)
			mycursor.execute(comand,val)
			mydb.commit()
			resposta = {"boo":True, "uso":"remover"} 
		except:
			resposta = {"boo":False, "uso":"remover"}
	elif body["uso"] == "adicionar":
		try:
			#TODO adicionar obra
			mycursor = mydb.cursor()
			comand = ""
			resposta = {"boo":True, "uso":"adicionar"} 
		except:
			resposta = {"boo":False, "uso":"adicionar"}
	elif body["uso"] == "mudar":
		try:
			mycursor = mydb.cursor()
			comand = "UPDATE obras SET obra = %s WHERE id = %s"
			val = (body["obra"]["obra"],body["obra"]["id"])
			mycursor.execute(comand,val)
			mydb.commit()
			mycursor = mydb.cursor()
			comand = ""
			resposta = {"boo":True, "uso":"mudar"} 
		except:
			resposta = {"boo":False, "uso":"mudar"}

	ch.basic_publish(exchange='',routing_key=properties.reply_to,properties=pika.BasicProperties(correlation_id = \
														properties.correlation_id),body=resposta)
	ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue="setobras", on_message_callback=on_request)

channel.start_consuming()
