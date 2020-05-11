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

channel.queue_declare(queue="getreferencia")

def on_request(ch, method, properties, body):
	while True:
		try:
			mydb = mysql.connector.connect(host="db", user="fernando", passwd="fernando", database="data.db")
			break
		except:
			time.sleep(5)

	mycursor = mydb.cursor()

	comand = "SELECT * FROM Referencia"

	try:
		mycursor.execute(comand)
		myresult = mycursor.fetchall()

		answer = ""

		for linha in myresult:
			try:
				answer += " !!@!! ".join(linha)
			except:
				answer += str(linha)
			
			if myresult.index(linha) != len(myresult) - 1:
				answer += " !!!@!!! "

		resposta = "True" + " !@! " + answer
	except:
		resposta = "False"

	ch.basic_publish(exchange='',routing_key=properties.reply_to,properties=pika.BasicProperties(correlation_id = \
														properties.correlation_id),body=resposta)
	ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue="getreferencia", on_message_callback=on_request)

channel.start_consuming()
