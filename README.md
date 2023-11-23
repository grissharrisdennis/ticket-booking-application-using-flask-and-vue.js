run python server

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
npm install -g @vue/cli
vue create my-vue-app  # Replace 'my-vue-app' with your project name
cd my-vue-app

(this instruction is for others who deleted their node modules like me
add node modules using 
npm install
i have'nt uploaded the node modules along with the folder ,above command reads the package.json to install the necessary packages if you need it.)

run server using 
npm run serve

