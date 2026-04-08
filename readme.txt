Add your backend folder here
to start django backend locally -
1. Open the project folder “chroma-branding-vault” then → cd backend
2. inside “backend” folder, there will be a venv folder
3. To activate venv, run → source venv/Scripts/activate
4. now → cd dev and run → python manage.py runserver
p.s -  if any error occurs, try both of these commands →
         First → python manage.py makemigrations
         Then → python manage.py migrate
         Lastly → python manage.py runserver

3. command didn’t work. The following worked instead:
.\venv\Scripts\Activate.ps1