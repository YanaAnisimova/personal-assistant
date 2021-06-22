from setuptools import setup, find_namespace_packages

setup(
      name='personal_assistant',
      version='1.0',
      description='Console bot for contact book managing',
      url='https://github.com/47codemonkey/personal-assistant',
      author='Udarniki truda',
      entry_points={'console_scripts': ['assistant = personal_assistant.assistant:main']},
      packages=['personal_assistant']
      )