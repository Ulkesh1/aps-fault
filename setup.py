from setuptools import setup,find_packages
from typing import List

def get_requirements()->List[str]:
    '''
    This function will retrun list of requirments
    '''
    requirements_list=[]
    with open ('requirements.txt','r') as req:
        requirements_list=[line.strip() for line in req.readlines() if line not in ['\n','-e .']]
        
    return requirements_list

setup(
    name="sensor",
    version="0.0.1",
    author="ulkesh",
    author_email="ulkesh13@gmail.com",
    url="https://github.com/Ulkesh1/SENSOR-FAULT-PREDICTION",
    packages=find_packages(),
    install_requires=get_requirements(),
)
