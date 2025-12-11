import requests, tempfile, os
def fetch(url):
    try:
        r = requests.get(url, timeout=15)
        tf = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
        tf.write(r.content)
        tf.flush()
        tf.close()
        return tf.name
    except:
        return None
def cleanup(path):
    try:
        if os.path.exists(path):
            os.remove(path)
    except:
        pass
