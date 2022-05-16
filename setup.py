from setuptools import setup

setup(name='escm',
      version='0.1',
      description='ELOG Socket Comunication Manager server',
      url='',
      author='Oiggart',
      author_email='andrea.a.raggio@jyu.fi',
      license='GPL-3.0',
      packages=['escm_server','escm_client'],
      install_requires=[
          'zmq',
          'subprocess',
      ],
      zip_safe=False,
)

# setup(name='escm_client',
#       version='0.1',
#       description='ELOG Socket Comunication Manager client',
#       url='',
#       author='Oiggart',
#       author_email='andrea.a.raggio@jyu.fi',
#       license='GPL-3.0',
#       packages=['escm_client'],
#       install_requires=[
#           'zmq',
#       ],
#       zip_safe=False,
# )