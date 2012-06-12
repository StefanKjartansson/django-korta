from paver.easy import * # noqa


PYCOMPILE_CACHES = ["*.pyc", "*$py.class"]

PROJECT = 'djkorta'


@task
@cmdopts([
    ("noerror", "E", "Ignore errors"),
])
def flake8(options):
    noerror = getattr(options, "noerror", False)
    sh("flake8 %s --ignore=E501" % PROJECT, ignore_error=noerror)


@task
def removepyc(options):
    sh("find %s -type f -a \\( %s \\) | xargs rm" % (PROJECT,
        " -o ".join("-name '%s'" % (pat, )
            for pat in PYCOMPILE_CACHES), ))
