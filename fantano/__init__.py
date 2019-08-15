# filename: __init__.py
"""Testing hug."""
import hug

@hug.get('/test')
def test(thing):
    """Tests hug."""
    return 'This is a {thing} test'.format(**locals())
