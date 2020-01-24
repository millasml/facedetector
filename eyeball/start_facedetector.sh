PROJ_PATH="PUT PROJ PATH HERE"
CAMURL1="PUT CAMERA URI HERE"
CAMURL2="PUT CAMERA URI HERE"

echo "connecting to venv..."
source "$PROJ_PATH/facedetectorenv/bin/activate"
echo "starting facedetector with camera 1"
python "$PROJ_PATH/eyeball/run_one_camera.py" --camera-id "L0001" --camera-uri $CAMURL1 &
echo "starting facedetector with camera 2"
python "$PROJ_PATH/eyeball/run_one_camera.py" --camera-id "L0002" --camera-uri $CAMURL2 &


