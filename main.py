import os
import json
from flask import Flask, request
from flask_restful import Resource, Api
from tensorboardX import SummaryWriter
from nd_to_json import nd_to_json, json_to_nd

import sys
import signal
signal.signal(signal.SIGTERM, lambda: sys.exit(0))

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

PORT = os.getenv("PORT", 80)
LOGDIR = os.getenv("LOGDIR", "./runs/")
FLUSH_SECS = os.getenv("FLUSH_SECS", 10)

runs = {}

#type/run_name/group/tag

def resolve_run(run_name):
    #create run if not exist
    if run_name not in runs:
        runs[run_name] = {
            "writer": SummaryWriter(LOGDIR + run_name, flush_secs=FLUSH_SECS),
            "steps": {}
        }

    run = runs[run_name]
    return run

def get_step(run_name, p):
    if p not in runs[run_name]["steps"]:
        runs[run_name]["steps"][p] = 0

    return runs[run_name]["steps"][p]

def increment_step(run_name, p):
    runs[run_name]["steps"][p] += 1

class Scalar(Resource):
    def post(self, run_name, group, tag):
        #data = request.get_json(force=True)
        value = request.data
        value = float(value)#parse float.... ew should use json but w/e

        run = resolve_run(run_name)
        tag_name = group + "/" + tag
        p = "scalar/" + tag_name
        #write and increment step
        run["writer"].add_scalar(tag_name, value, get_step(run_name, p))
        increment_step(run_name, p)

class Histogram(Resource):
    def post(self, run_name, group, tag):
        x = json_to_nd(request.json)
        run = resolve_run(run_name)
        tag_name = group + "/" + tag
        p = "histogram/" + tag_name

        run["writer"].add_histogram(tag_name, x, get_step(run_name, p))
        increment_step(run_name, p)

class Audio(Resource):
    def post(self, run_name, group, tag, samplerate=44100):
        x = json_to_nd(request.json)
        run = resolve_run(run_name)
        samplerate = int(samplerate)
        tag_name = group + "/" + tag
        p = "audio/" + tag_name
        #write and increment step
        run["writer"].add_audio(tag_name, x, get_step(run_name, p), sample_rate=samplerate)
        increment_step(run_name, p)

class Image(Resource):
    def post(self, run_name, group, tag, format="hwc"):
        x = json_to_nd(request.json)
        run = resolve_run(run_name)
        format = format.upper()
        tag_name = group + "/" + tag
        p = "image/" + tag_name
        #write and increment step
        run["writer"].add_image(tag_name, x, get_step(run_name, p), dataformats=format)
        increment_step(run_name, p)

class Video(Resource):
    def post(self, run_name, group, tag, fps=15):
        x = json_to_nd(request.json)
        run = resolve_run(run_name)
        format = format.upper()
        fps = int(fps)
        tag_name = group + "/" + tag
        p = "video/" + tag_name
        #write and increment step
        run["writer"].add_image(tag_name, x, get_step(run_name, p), fps=fps)
        increment_step(run_name, p)

class HParams(Resource):
    def post(self, run_name, name):
        data = request.get_json(force=True)
        params = data["params"]
        metrics = data["metrics"]

        run = resolve_run(run_name)
        p = "hparams/" + name
        #write and increment step
        run["writer"].add_hparams(params, metrics, name, get_step(run_name, p))
        increment_step(run_name, p)

#TODO: mesh?

app = Flask(__name__)
api = Api(app)

api.add_resource(Scalar, '/scalar/<run_name>/<group>/<tag>')
api.add_resource(Histogram, '/histogram/<run_name>/<group>/<tag>')
api.add_resource(Audio, '/audio/<run_name>/<group>/<tag>/<samplerate>')
#api.add_resource(Audio, '/audio/<run_name>/<group>/<tag>')
api.add_resource(Image, '/image/<run_name>/<group>/<tag>/<format>')
#api.add_resource(Image, '/image/<run_name>/<group>/<tag>')
api.add_resource(Video, '/video/<run_name>/<group>/<tag>/<fps>')
#api.add_resource(Video, '/video/<run_name>/<group>/<tag>')
api.add_resource(HParams, '/hparams/<run_name>/<name>')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=PORT)
