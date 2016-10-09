from setuptools import setup

setup (name='BusinessParser',
      version='0.1.0',
      packages=['src'],
      entry_points={
          'console_scripts': [
              'src = src.__main__:main'
          ]
      },
)