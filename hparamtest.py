import random
from protopost import protopost_client as ppcl

HPARAMS = lambda experiment, id, params, metrics: ppcl(f"http://127.0.0.1:8080/hparams/{experiment}/{id}", {"params":params, "metrics":metrics})

apples = [1, 2, 3]
bananas = [2, 3, 4]

EXPERIMENT_NAME = "fruits"
id = 0
def get_id(a, b):
  global id
  id += 1
  return id


for i in range(1000):
  a = random.choice(apples)
  b = random.choice(bananas)
  HPARAMS(EXPERIMENT_NAME, get_id(a, b), {"apples":a, "bananas":b}, {"fruitiness":a*b})
