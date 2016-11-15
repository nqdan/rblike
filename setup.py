#remove this import or we can meet unicode issue when build and deploy
#from __future__ import unicode_literals

from reviewboard.extensions.packaging import setup


PACKAGE = "rblike"
VERSION = "0.1"

setup(
    name=PACKAGE,
    version=VERSION,
    description="Extension rblike",
    author="SystemExec",
    packages=["rblike"],
    entry_points={
        'reviewboard.extensions':
            '%s = rblike.extension:RBLike' % PACKAGE,
    },
    package_data={
        b'rblike': [
            'templates/rblike/*.txt',
            'templates/rblike/*.html',
        ],
    }
)