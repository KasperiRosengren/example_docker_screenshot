### Build command
```
sudo docker build -t gui-test-app .
```

### Run container
#### Without interactive session
```
sudo docker run -v <PATH_FOR_VOLUME_ON_YOUR_PC>:/app/screenshots --name test gui-test-app
```
#### With interactive session
```
sudo docker run -it -v <PATH_FOR_VOLUME_ON_YOUR_PC>:/app/screenshots --name test gui-test-app sh
```