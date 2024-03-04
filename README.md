File transfer programs using TCP and UDP, for each protocol. Reliable file transfer program have been implemented. 

For UDP, Selective Repeat algorithm have been implemented in order to prevent data loss. 



## RUN containers using docker compose plugin

You can test the program using seperate Docker containers for server and client. 

You can generate sample object files in order to test the program by running `generateobjects.sh` in server container.

To start server and client containers:
```
docker compose up -d
```

To stop server and client containers:
```
docker compose down
```

Note that, if you orchestrate your containers using docker compose, the containers will have hostnames ("client" and "server") and DNS will be able to resolve them...

In one terminal, attach to the server container
```
docker exec -it server bash
```
In another terminal, attach to the client container
```
docker exec -it client bash
```

In the server container: you should execute tcpserver.py or udpserver.py

In the client container: you should execute tcpclient.py or udpclient.py

After connection is established, in the client terminal you can enter the filenumber to transfer the files from server to client.


The local "code" folder is mapped to the "/app" folder in containers and the local "examples" folder is mapped to the "/examples" folder in the container. You can develop your code on your local folders on your own host machine, they will be immediately synchronized with the "/app" folder on containers. The volumes are created in read-write mode, so changes can be made both on the host or on the containers. You can run your code on the containers...

