# Employee Leave Management System

A Django-based web application to manage employee leaves, approvals, and balances with role-based access for Employees and Managers.

---

## 📌 Features Implemented
1. **User Authentication**
   - Secure login for Employees and Managers.
   - Role-based permissions (Employees submit leave requests, Managers approve/reject).

2. **Leave Request Submission**
   - Employees submit requests with leave type, start date, end date, and reason.
   - Input validation ensures dates are valid and all fields are filled.

3. **Leave Approval Workflow**
   - Managers can approve or reject requests.
   - Option for managers while approving/rejecting.

4. **Leave Balances**
   - Tracks available leave days for each employee.
   - Automatically updates balances on approval or rejection.

5. **Leave Calendar**
   - Displays approved leaves in a calendar view.
   - Highlights dates when employees are on leave.

---

## ⚠️ User Registration Rules
- **Employees cannot register themselves.**
- **Managers cannot register themselves.**
- Only the **superuser (admin)** can create Managers and Employees from the Django admin panel.

---

## 🛠 How to Run the Project Locally

### 1️⃣ Clone or Unzip the Project
Unzip the provided folder and open a terminal inside the project folder.

### 2️⃣ Create a Virtual Environment
```bash
python -m venv env
env\Scripts\activate       # On Windows
source env/bin/activate    # On Mac/Linux


3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Apply Migrations
python manage.py migrate

5️⃣ Create a Superuser (Admin)
python manage.py createsuperuser


This admin account will be used to:

Log in to the Django admin panel (/admin)

Create Managers

Create Employees

6️⃣ Run the Development Server
python manage.py runserver

7️⃣ Access the Application

Main Site: http://127.0.0.1:8000

Admin Panel: http://127.0.0.1:8000/admin

🧑‍💼 Workflow

Admin logs in → Creates Managers .

Employee logs in → Submits leave request.

Manager logs in → Reviews leave request → Approves or rejects.

Leave balances update automatically and calendar view updates.

📌 Default Roles in System

Superuser/Admin → Full access, can create users.

Manager → Approves/rejects leaves for their department’s employees.

Employee → Submits leave requests.