import requests

HOST = "http://127.0.0.1"

def send(host, run_name, group, tag, value):
    requests.post("{}/{}/{}/{}".format(host, run_name, group, tag), json=value)

run_name = "foo"
group = "bar"
tag = "baz"
for i in range(100):
    send(HOST, run_name, group, tag, i)

run_name = "foo"
group = "bar2"
tag = "baz"
for i in range(100):
    send(HOST, run_name, group, tag, i)

run_name = "foo"
group = "bar"
tag = "qux"
for i in range(100):
    send(HOST, run_name, group, tag, -i)

run_name = "foo2"
group = "bar"
tag = "baz"
for i in range(100):
    send(HOST, run_name, group, tag, i * 2)
