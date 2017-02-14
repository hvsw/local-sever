LOGS_PATH="/home/pi/420bits/logs"
SCRIPTS_PATH="/home/pi/420bits/local-sever"
RESTART="0"
STOP="0"

for i in "$@"
do
case $i in
    -r|--restart)
    RESTART="1"
    ;;

    -s|--stop)
    STOP="1"
    ;;

    -l=*|--lib=*)
    DIR="${i#*=}"
    ;;

    --default)
    DEFAULT=YES
    ;;

    *)
    ;;
esac
done

declare -a scripts=("420bits-service.py" "420bits-webserver.py")
for script in "${scripts[@]}"
do
   	if [ "$RESTART" == "1" ] || [ "$STOP" == "1" ]; then
   		PID=`ps -eaf | grep $script | grep -v grep | awk '{print $2}'`
		if [[ "" !=  "$PID" ]]; then
		  echo "Killing $PID - Script: $script"
		  kill -9 $PID
		fi
   	fi

    if [ "$STOP" == "0" ]; then
        if (( $(ps -aux | grep -v grep | grep "$script" | wc -l) > 0 ))
        then
        echo "$script is already running"
        else
        echo "Will start $script"
        /usr/bin/python "$SCRIPTS_PATH/$script" > "$LOGS_PATH/$script.log" 2>&1 &
        echo "Did start $script"
        fi
    fi
done