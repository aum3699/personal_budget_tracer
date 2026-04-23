# Personal Budget Tracker

A comprehensive web-based personal budget tracker built with Flask, SQLite, and Bootstrap.

## Features
- **User Authentication**: Secure login/registration system with Flask-Login
- **CRUD Operations**: Add, edit, delete, and view incomes and expenses
- **Monthly Filtering**: Filter transactions by month and year
- **CSV Export**: Export filtered transactions to CSV format
- **User Data Isolation**: Each user sees only their own transactions
- **Real-time Summaries**: View total balance, income, and expenses
- **Modern UI**: Clean, responsive Bootstrap interface
- **Admin Panel**: Complete admin interface for user and transaction management

## Project Structure
```
personal_budget_tracker/
│
├── app/
│   ├── __init__.py
│   ├── routes.py
│   ├── auth.py
│   ├── admin.py
│   ├── models.py
│   ├── forms.py
│   ├── templates/
│   │   ├── index.html
│   │   ├── edit_transaction.html
│   │   ├── login.html
│   │   ├── register.html
│   │   └── admin/
│   │       ├── dashboard.html
│   │       └── users.html
│   └── static/
│
├── run.py
├── make_admin.py
├── requirements.txt
└── README.md
```

## Setup
1. **Create a virtual environment:**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # On Windows
   # or
   source venv/bin/activate  # On Mac/Linux
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the app:**
   ```bash
   python run.py
   ```

4. **Visit:** [http://127.0.0.1:5000](http://127.0.0.1:5000)

## Usage
1. **Register/Login**: Create an account or log in to access your budget
2. **Add Transactions**: Use the form to add income or expense entries
3. **Filter by Month**: Select month/year to view specific periods
4. **Edit/Delete**: Use action buttons to modify or remove transactions
5. **Export Data**: Download filtered transactions as CSV files

## Admin Panel Setup
1. **Register your first account** at `/register`
2. **Make yourself an admin** by running:
   ```bash
   python make_admin.py
   ```
3. **Access admin panel** by clicking "🔧 Admin Panel" in the navigation (only visible to admins)

## Admin Panel Features
- **Dashboard**: Overview of all users, transactions, and system statistics
- **User Management**: View all users, make/remove admins, delete users
- **Transaction Overview**: View all transactions across all users
- **User Details**: Detailed view of individual user's transactions and statistics

## Security Features
- Password hashing with Werkzeug
- User session management
- Data isolation between users
- CSRF protection with Flask-WTF
- Admin-only access to admin panel

## Future Enhancements
- Transaction categories management
- Budget goals and alerts
- Data visualization (charts/graphs)
- Multi-currency support
- Mobile app integration 
