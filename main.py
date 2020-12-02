import os

from flask import Flask, request
from flask_restful import Resource, Api
from tensorboardX import SummaryWriter

PORT = os.getenv("PORT", 80)
LOGDIR = os.getenv("LOGDIR", "./runs/")
FLUSH_SECS = os.getenv("FLUSH_SECS", 10)

runs = {}

#/run_name/group/tag

class Scalar(Resource):
    def post(self, run_name, group, tag):
        #data = request.get_json(force=True)
        value = request.data
        value = float(value)#parse float.... ew should use json but w/e

        #create run if not exist
        if run_name not in runs:
            runs[run_name] = {
                "writer": SummaryWriter(LOGDIR + run_name, flush_secs=FLUSH_SECS),
                "step": 0
            }

        run = runs[run_name]
        #write and increment step
        run["writer"].add_scalar(group + "/" + tag, value, run["step"])
        run["step"] += 1

app = Flask(__name__)
api = Api(app)

api.add_resource(Scalar, '/<run_name>/<group>/<tag>')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=PORT)
