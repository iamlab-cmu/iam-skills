from distutils.core import setup
  

setup(name='iam_skills',
      version='0.1.0',
      install_requires=[
            'pillar_state',
            'pillar_skills'
      ],
      description='Skill Utilities for IAM Lab',
      author='Jacky Liang',
      author_email='jackyliang@cmu.edu',
      packages=['iam_skills']
     )