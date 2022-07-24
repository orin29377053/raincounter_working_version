containerName=raincointer_server
port_out=15566
port_in=15566
imageName=raincointer_server
PWD=$(pwd)
raincounter_db_ip=$raincounter_db_ip
CI_COMMIT_SHA=$CI_COMMIT_SHA

echo 'Try to get container ID which name is '$containerName

containerID=$(docker ps -a --filter "NAME=$containerName" --format "{{.ID}}")
if ["$containerID" = ""]
then
    echo "Can't find container: $containerName"
else
    echo "container ID: "$containerID
    echo "Stop server..."
    docker rm -f $containerID
    echo "Stop server DONE"
fi

echo "Try to run server..."
echo 'PWD: '$PWD
echo 'raincounter_db_ip: '$raincounter_db_ip
echo 'CI_COMMIT_SHA: '$CI_COMMIT_SHA
# python3 ./Rain-Counter/logSaver.py --Command "docker run -d -v $PWD:/app --name $containerName -e raincounter_db_ip=$raincounter_db_ip -p $port_out:$port_in -u 1002:1003 $imageName python ./Rain-Counter/manage.py runserver 0:15566"
docker run -d -v $PWD:/app --name $containerName -e raincounter_db_ip=$raincounter_db_ip -e CI_COMMIT_SHA=$CI_COMMIT_SHA -p $port_out:$port_in -u 1002:1003 $imageName python ./Rain-Counter/manage.py runserver 0:15566
# docker run -d -v $PWD:/app --name $containerName -e raincounter_db_ip=$raincounter_db_ip -p $port_out:$port_in -u 1002:1003 $imageName python ./Rain-Counter/logSaver.py --Command "python ./Rain-Counter/manage.py runserver 0:15566"
# docker run -d -v $PWD:/app --name $containerName -e raincounter_db_ip=$raincounter_db_ip -p $port_out:$port_in -u 1002:1003 $imageName python ./Rain-Counter/logSaver.py --Command "python --version"

NewServerContainerID=$(docker inspect --format="{{.Id}}" raincointer_server)
echo "Run server DONE! New container id: "$NewServerContainerID

echo "Run container log upload function START"
python3 $PWD/DockerContainerLogUploader/runScript.py --ID $NewServerContainerID &
echo "Run container log upload function DONE"

exit 0