from setuptools import setup



setup(
    name='zeitfluss',
    version='1.0',
    py_modules=['zeitfluss'],
    install_requires=[
        'click',
        'parsedatetime',
    ],
    entry_points='''
        [console_scripts]
        zeitfluss=zeitfluss:cli
    '''
)
