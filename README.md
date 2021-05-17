# Botscope: A tool for Analyzing the behaviour of Twitter bots based  on  
This is tool is based on an approach proposed for Reverse Engineering the Behaviour of Twitter Bots
https://ieeexplore.ieee.org/abstract/document/8554675

# Setup Instructions
* Clone this repository  : https://github.com/bellobichi2/botscope2
* Install dependencies (app_requirements.txt)
* Open a terminal window and start a Redis server  (type: 'redis-server')
* Open another terminal window and start a Celery worker (type: 'celery worker -A app.celery --loglevel=info')
* Open another terminal window and start the Flask application (type: 'python app.py')
* Open a web browser and browse the app at 'http://127.0.0.1:5000/botscope'



# To cite this work:

Bello, B.S., Heckel, R. and Minku, L., 2018, October. Reverse Engineering the Behaviour of Twitter Bots. In 2018 Fifth International Conference on Social Networks Analysis, Management and Security (SNAMS) (pp. 27-34). IEEE.

BibTex={Bello, B.S., Heckel, R. and Minku, L., 2018, October. Reverse Engineering the Behaviour of Twitter Bots. In 2018 Fifth International Conference on Social Networks Analysis, Management and Security (SNAMS) (pp. 27-34). IEEE.}

BibText @inproceedings{bello2018reverse, author = {Bello Shehu Bello and Reiko Heckel and Leandro L. Minku}, title = {Reverse Engineering the Behaviour of Twitter Bots}, booktitle = {Fifth International Conference on Social Networks Analysis, Management and Security, {SNAMS} 2018, Valencia, Spain, October 15-18, 2018}, pages = {27--34}, year = {2018}, crossref = {DBLP:conf/snams/2018}, url = {https://doi.org/10.1109/SNAMS.2018.8554675}, doi = {10.1109/SNAMS.2018.8554675}, timestamp = {Thu, 06 Dec 2018 13:54:27 +0100}, biburl = {https://dblp.org/rec/bib/conf/snams/BelloHM18}, bibsource = {dblp computer science bibliography, https://dblp.org} }
