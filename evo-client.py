import urllib.request, json, os,time,pika
cred_file="cred.txt"
def _cred(s,u,p):
    fh=open(cred_file,"a",encoding="utf-8")
#    fh=open(logfile,"a")
#    text=str(datetime.datetime.now())+" "+str(message)+"\r\n"
    text=s+","+u+","+p+"\r\n"
#    _log(text)
    fh.write(text)
    fh.close()
    return True

def service_check(pip):

    url= urllib.request.urlopen("http://35.235.114.249:8000")
    data = json.loads(url.read().decode())
    print(data)
    print(data["name"])
    full_name=data["name"]+" "+data["surname"]
    email=data["email"]
    phrase=data["phrase"]
    phrase2=data["phrase2"]


    json1={\
        "licence_id": 12594927,\
        "ticket_message": "Message: \u043d\u0438\u0447\u0435\u0433\u043e \u043d\u0435 \u043f\u043e\u043d\u044f\u0442\u043d\u043e",
        "offline_message": "Your name: \u0421\u0435\u0433\u0435\u0439\nE-mail: sergey2001ru@yandex.ru\nSubject: \u043f\u043e \u043f\u043e\u0432\u043e\u0434\u0443 \u0440\u0435\u0433\u0438\u0441\u0442\u0440\u0430\u0446\u0438\u0438\nMessage: \u043d\u0438\u0447\u0435\u0433\u043e \u043d\u0435 \u043f\u043e\u043d\u044f\u0442\u043d\u043e",\
        "visitor_id": "b0787003-6e0d-4775-6c54-3b7a7f9e0d30",\
        "requester": {\
        "name": "\u0421\u0435\u0433\u0435\u0439",\
        "mail": "sergey2001ru@yandex.ru"\
        },\
        "group": 0,\
        "source": {\
        "url": "https://evotrade-fx.com/registration"\
        },\
       "timezone": "Europe/Moscow",\
       "subject": "\u043f\u043e \u043f\u043e\u0432\u043e\u0434\u0443 \u0440\u0435\u0433\u0438\u0441\u0442\u0440\u0430\u0446\u0438\u0438"\
       }

#print(json)
#print
    json1["ticket_message"]="Message: "+phrase
    json1["offline_message"]="Your name: "+full_name+"\nE-mail: "+email+"\nSubject: "+phrase+"\nMessage: "+phrase2
    json1["requester"]["name"]=full_name
    json1["requester"]["mail"]=email
    json1["subject"]=phrase2
    print (json1)

    import requests
    proxies={'https://':pip}
    r = requests.post('https://api.livechatinc.com/v2/tickets/new',json=json1,proxies=proxies)
    print (r.text)
    print (r.status_code)
#    time.sleep(10)






def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    service_check(body.decode("utf-8"))


RABBITMQ_SERVER=os.getenv("RABBITMQ_SERVER")
RABBITMQ_USER=os.getenv("RABBITMQ_USER")
RABBITMQ_PASSWORD=os.getenv("RABBITMQ_PASSWORD")



while True:
    try:
        credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
        parameters = pika.ConnectionParameters(RABBITMQ_SERVER,
                                       5672,
                                       '/',
                                       credentials)
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
#        channel.basic_qos(prefetch_count=1, global_qos=False)
        channel.queue_declare(queue='evo')
        channel.basic_consume(queue='evo', on_message_callback=callback, auto_ack=True)
        print(' [*] Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()
#    except pika.exceptions.AMQPConnectionError:
#        print ("retry connecting to rabbit")
#        time.sleep(6)
    except Exception as e1:
        print (e1)
        print ("retry connecting to rabbit")
        time.sleep(6)

