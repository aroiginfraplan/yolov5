#/usr/bin/python3
ENVNAME=".env"

if [ -d $ENVNAME ]; then

    . $ENVNAME/bin/activate

else

    virtualenv $ENVNAME --python=python3
    . $ENVNAME/bin/activate
    pip install -r requirements.txt

fi
