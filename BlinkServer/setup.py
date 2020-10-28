from setuptools import setup, find_packages

setup(
  name = 'BlinkServer',
  version = '1.0.0',
  description = 'Serves blinks to the BlinkUI',
  packages = find_packages(),
  entry_points = {
    'console_scripts': 'blink-server = blink.blink:main'
  },
  install_requires = [
    'scipy',
    'numpy',
    'imutils',
    'dlib',
    'opencv-python'
  ]
)