from protopost import protopost_client as ppcl

run_name = "foo"
name = "bar"

HPARAMS = lambda params, metrics: ppcl("http://127.0.0.1/hparams/run_name/name", {"params":params, "metrics":metrics})
