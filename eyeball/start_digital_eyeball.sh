PROJ_PATH="/home/resources/Projects/digital-eyeball-v2"
CAMURL1="rtsp://admin:Singapore2019@192.168.3.230:554/cam/realmonitor?channel=1&subtype=0"
CAMURL2="http://root:admin@169.254.137.125/axis-cgi/mjpg/video.cgi"

echo "connecting to venv..."
source "$PROJ_PATH/eyeballenv/bin/activate"
echo "starting digital eyeball with camera 1"
python "$PROJ_PATH/eyeball/run_one_camera.py" --camera-id "L0001" --camera-uri $CAMURL1 &
echo "starting digital eyeball with camera 2"
python "$PROJ_PATH/eyeball/run_one_camera.py" --camera-id "L0002" --camera-uri $CAMURL2 &


