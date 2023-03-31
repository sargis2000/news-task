# Django News Portal
This is a simple news portal built with Django framework that allows administrators to create and manage news articles
through the admin panel. The portal also allows visitors to browse and filter news articles by category and creation
date.
## Docker installation
#### Step1: Clone the repository:
```bash
git clone https://github.com/sargis2000/django-news-portal.git
```
#### Step2: Move to Root directory of project and run commands below
***Warning:***   Do not forget change env variables

```bash
sudo docker build -t django-news-portal .
sudo docker run -p 8000:8000 -e SECRET_KEY=my-strong-secret-key -e DEPLOY_MOD=True django-news-portal
```

## Manual installation
#### Step1: Clone the repository:

```bash
git clone https://github.com/sargis2000/django-news-portal.git
```
#### Step2: Create a virtual environment:
```bash
cd django-news-portal
python3 -m venv venv
source venv/bin/activate
```

#### Step3: Install dependencies:
```bash
pip install -r requirements.txt
```
#### Step4: Environment Variables:

To run this project, you will need to add the following environment variables to your .env file

`SECRET_KEY` any string \
`DEPLOY_MOD` if `True` DEBUG is off, otherwise on
```bash
export SECRET_KEY="my strong secret key"
export DEPLOY_MOD="True"
```

#### Step5: Run migrations:
```bash
python manage.py migrate
```
#### Step6: Create superuser:
```bash
python manage.py createsuperuser
```
### Step7: Run the server:
```bash
python manage.py runserver
```
Access the admin panel at http://localhost:8000/admin/ and log in with the superuser credentials.
# Run tests
```bash
 python manage.py test
 ```
# Usage
## Admin panel
##### The admin panel allows administrators to create and manage news articles and categories. To create a new article, follow these steps:

1) Log in to the admin panel.
2) Click on "News" to open the news list.
3) Click on "Add News" to create a new article.
4) Fill in the title and content of the article.
5) Select the categories that the article belongs to.
6) Select the main category of the article.
7) Click on "Save" to create the article.

##### To edit an existing article, follow these steps:

1) Log in to the admin panel.
2) Click on "News" to open the news list.
3) Click on the title of the article to open the editing form.
4) Edit the title, content, categories and main category as needed.
5) Click on "Save" to update the article.
##### To create a new category, follow these steps:

1) Log in to the admin panel.
2) Click on "Categories" to open the category list.
3) Click on "Add Category" to create a new category.
4) Fill in the name and slug  of the category.
5) Click on "Save" to create the category.
##### To edit an existing category, follow these steps:

1) Log in to the admin panel.
2) Click on "Categories" to open the category list.
3) Click on the name or slug  of the category to open the editing form.
4) Edit the name or slug of the category as needed.
5) Click on "Save" to update the category.
