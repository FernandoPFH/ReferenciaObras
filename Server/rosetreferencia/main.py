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

channel.queue_declare(queue="setreferencia")

def on_request(ch, method, properties, body):
	while True:
		try:
			mydb = mysql.connector.connect(host="db", user="fernando", passwd="fernando", database="data.db")
			break
		except:
			time.sleep(5)

	ref = body.decode("utf-8").split("!!@!!")
	num = len(ref) / 3

	#try:
	if True:
		for i in range(0,num):
			mycursor = mydb.cursor()
			comand = "UPDATE Referencia SET (Preco,Tempo) = (%f,%i) WHERE Nome = %s"
			val = (ref[3*i+1],ref[3*i+2],ref[3*i])
			mycursor.execute(comand,val)
			mydb.commit()

		resposta = "True"
	#except:
	#	resposta = "False"

	ch.basic_publish(exchange='',routing_key=properties.reply_to,properties=pika.BasicProperties(correlation_id = \
														properties.correlation_id),body=resposta)
	ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue="setreferencia", on_message_callback=on_request)

channel.start_consuming()
