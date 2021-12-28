# Aegis TensorBoard Logger

## Environment
- `LOGDIR` - TensorBoard log directory (defaults to `./runs/`, which would be `/app/runs` in the container)
- `FLUSH_SECS` - Flush logs every this many seconds (defaults to 10)
- `PORT` - the port to listen on (defaults to 80)

## Routes
* `/scalar/<run_name>/<group>/<tag>` to log scalars
* `/histogram/<run_name>/<group>/<tag>` to log histograms
* Similar routes exist for audio, images, and video but uh... they're untested.

That's all it does. :)

## TODO
* Support/test other types of TensorBoard logs (image, video, text?)
* Add ability to create new timestamped logs
* Add ability to delete old logs (or at least close the logger so the files can be deleted)
* create docker-compose.yml example
