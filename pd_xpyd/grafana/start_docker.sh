#!/bin/bash

export DOCKER_IMAGE=${DOCKER_IMAGES:-ubuntu:22.04}
export CONTAINER_NAME=${CONTAINER_NAME:-ds-r1-pd-dashboard}

docker run -td --ulimit memlock=-1:-1 --ipc=host --net=host                \
     	--env http_proxy=${http_proxy} 			  \
        --env https_proxy=${https_proxy} 		  \
        --env no_proxy=${no_proxy} 			  \
        --device=/dev:/dev -v /dev:/dev                                    \
        --volume `pwd`:/workspace                                          \
        --env WORKSPACE_ROOT=/workspace                                    \
        --name ${CONTAINER_NAME}                                           \
        ${DOCKER_IMAGE}

docker exec $CONTAINER_NAME bash -c "sed -i 's/^#Port 22/Port ${SSH_PORT}/' /etc/ssh/sshd_config"
docker exec $CONTAINER_NAME bash -c "sed -i 's/^#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config"
docker exec $CONTAINER_NAME bash -c "service ssh start"
docker exec $CONTAINER_NAME bash -c "mkdir ~/.ssh; printf 'Host *\n    StrictHostKeyChecking no\nPort ${SSH_PORT}' >> ~/.ssh/config"
docker exec $CONTAINER_NAME bash -c "ssh-keygen -t rsa -b 4096 -N '' -f ~/.ssh/id_rsa -q"
docker exec $CONTAINER_NAME bash -c "cat ~/.ssh/id_rsa.pub >>  ~/.ssh/authorized_keys; chmod 600 ~/.ssh/authorized_keys"
docker exec $CONTAINER_NAME bash -c "ln -s /workspace ~/workspace"
docker exec ${CONTAINER_NAME} bash -c "cd \${WORKSPACE_ROOT}; ./setup.sh"
docker exec -it ${CONTAINER_NAME} bash
