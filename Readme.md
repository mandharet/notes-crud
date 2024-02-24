
#### [User Authentication APIs 🔗](https://github.com/mandharet/notes-crud/tree/DEVELOPMENT/apps/authapp#user-authentication-apis)

#### [Notes CRUD APIs 🔗](https://github.com/mandharet/notes-crud/tree/DEVELOPMENT/apps/notes#note-apis)

**Python: 3.9.5**

 ## Setting Up Local Development Environment

### 1. Setting Up using venv
### 2. Setting Up using docker

---
 
<details>

<summary>Setting Up using venv</summary>


### 1. Clone the Repository

```bash
git clone https://github.com/mandharet/notes-crud
cd ./notes-crud
```

### 2. Create a Virtual Environment (Optional but Recommended)

```bash
# Install virtualenv if not already installed
pip install virtualenv

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows
venv\Scripts\activate
# On Unix or MacOS
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

This command installs all the required Python packages specified in the `requirements.txt` file.

### 4. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

This command applies any pending database migrations.

### 5. Create a Superuser (Optional)

```bash
python manage.py createsuperuser
```

This command creates a superuser account for administrative access to the Django admin interface.

### 6. Run the Development Server

```bash
python manage.py runserver
```

This command starts the development server. You can access the Django development server at `http://127.0.0.1:8000/`.

### 7. Explore the API

Explore the API using tools like [Postman](https://www.postman.com/) or by visiting the provided Django admin interface at `http://127.0.0.1:8000/admin/` (login with superuser credentials).

</details>

---

<details>
<summary>Setting Up using docker</summary>

- [ ] TODO:create Dockerfile

</details>


---
