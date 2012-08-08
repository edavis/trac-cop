from fabric.api import *

env.hosts = ["transparentnevada.com:4789"]
env.user = "eric"

def pack(commit="HEAD"):
    """
    Create an archive from the given commit.
    """
    local("git archive --format=tar.gz --prefix=trac-cop/ -o /tmp/trac-cop.tar.gz %(commit)s" %
          dict(commit=commit))

def deploy(commit="HEAD"):
    pack(commit)
    put("/tmp/trac-cop.tar.gz", "/tmp")
    with cd("/srv/environments/trac"):
        run("tar xf /tmp/trac-cop.tar.gz")
        run("bin/pip install -U --no-deps ./trac-cop/")
    run("rm -rf trac-cop")
    run("rm -f /tmp/trac-cop.tar.gz")
