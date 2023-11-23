run python server

open Folder in wsl
wsl

create environment
python3 -m venv nameofenvironment

activate environment
source nameofenvironment/bin/activate

install packages
pip install -r requirements.txt

activate python server
python app.py

celery jobs
celery -A app.celery worker -l info

celery periodic jobs 
celery -A app.celery beat -l info

mailhog 
open directory in which MailHog present
cd $HOME/go/bin
type ./MailHog

running frontend server

open templates folder

add node_modules folder into the templates folder

run server using 
npm run serve

