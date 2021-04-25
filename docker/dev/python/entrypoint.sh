#!/bin/bash

USER_ID=$(stat -c "%u" $PWD)

PYTHON_RUN_UID=${PYTHON_RUN_UID:=${USER_ID}}
PYTHON_RUN_USER=${PYTHON_RUN_USER:=user}
PYTHON_RUN_GROUP=${PYTHON_RUN_GROUP:=user}

PYTHON_RUN_USER_TEST=$(grep "[a-zA-Z0-9\-\_]*:[a-zA-Z]:${PYTHON_RUN_UID}:" /etc/passwd)

if [ -n "${PYTHON_RUN_USER_TEST}" ]; then
  echo "Update user '$PYTHON_RUN_USER'"

  usermod -l ${PYTHON_RUN_USER} $(id -un ${PYTHON_RUN_UID})
  usermod -u $PYTHON_RUN_UID -g $PYTHON_RUN_GROUP $PYTHON_RUN_USER

else
  echo "Create user '$PYTHON_RUN_USER'"

  mkdir /home/$PYTHON_RUN_USER
  groupadd $PYTHON_RUN_GROUP
  useradd -u $PYTHON_RUN_UID -g $PYTHON_RUN_GROUP -d /home/$PYTHON_RUN_USER $PYTHON_RUN_USER
  chown $PYTHON_RUN_USER:$PYTHON_RUN_GROUP /home/$PYTHON_RUN_USER
fi

export HOME=/home/$PYTHON_RUN_USER

echo "Running command '$*'"
exec su -p ${PYTHON_RUN_USER} -s /bin/bash -c "$*"
