RequisitionPro - Inventory Management System
RequisitionPro is a comprehensive inventory management system built with Django that streamlines the product requisition process for organizations. With role-based access, intuitive workflows, and real-time inventory tracking, RequisitionPro simplifies procurement operations from request to fulfillment.
Key Features
🔐 User Authentication & Management
•	Role-based access (Employee and Manager)
•	Registration with department assignment
•	Profile management with photo upload
•	Password reset via OTP email verification
📦 Product Catalog
•	Product listings with search and filtering
•	Detailed product views with stock indicators
•	Related product suggestions
•	Category-based organization
📝 Requisition Workflow
•	Employee requisition creation and management
•	Manager approval/rejection system
•	Priority-based requisition handling
•	Requisition tracking with status updates
📊 Dashboards
•	Employee dashboard for tracking personal requisitions
•	Manager dashboard for departmental approvals
•	Role-specific navigation
Technology Stack
Backend
•	Django (Python web framework)
•	Database: SQLite (default, can be configured for PostgreSQL/MySQL)
•	Authentication: Custom user model extending AbstractUser
•	Email: SMTP for OTP-based password resets
Frontend
•	Bootstrap 5 (Responsive UI framework)
•	Font Awesome (Icons)
•	JavaScript (Dynamic interactions)
Models
# accounts/models.py
class User(AbstractUser):
    EMPLOYEE = 'Employee'
    MANAGER = 'Manager'
    ROLE_CHOICES = [
        (EMPLOYEE, 'Employee'),
        (MANAGER, 'Manager'),
    ]
    # ... additional fields ...

# catalog/models.py
class Product(models.Model):
    sku = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=200)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    current_stock = models.PositiveIntegerField(default=0)

# requisitions/models.py
class Requisition(models.Model):
    PENDING = 'PENDING'
    APPROVED = 'APPROVED'
    REJECTED = 'REJECTED'
    STATUS_CHOICES = [...]
    # ... fields and methods ...
Prerequisites
•	Python 3.8+
•	Django 4.0+
•	Pillow (for image handling)
Setup Instructions
1.	Clone the repository:
git clone https://github.com/yourusername/requisitionpro.git
cd requisitionpro
2.	Create virtual environment:
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
3.	Install dependencies:
pip install -r requirements.txt
4.	Apply migrations:
python manage.py migrate
5.	Create superuser:
python manage.py createsuperuser
6.	Run development server:
python manage.py runserver
7.	Access the application at http://localhost:8000
Usage Guide
Roles and Permissions
•	Employee:
o	Create/edit/cancel requisitions
o	View personal requisition history
o	Update personal profile
•	Manager:
o	Approve/reject requisitions from their department
o	View all requisitions in their department
o	Add comments to approvals/rejections
Key Functionality
1.	Registration & Login
o	Custom registration form with role selection
o	Secure login with password reset functionality
2.	Product Catalog
o	Browse products with search and filtering
o	View product details and stock levels
o	Request products directly from catalog
3.	Requisition Management
o	Create requisitions with multiple items
o	Set priority levels (Low/Medium/High)
o	Track requisition status through workflow
4.	Approval Process
o	Managers receive pending requisitions
o	Approval with optional comments
o	Rejection requires justification
Contributing
Contributions are welcome! Please follow these steps:
1.	Fork the repository
2.	Create your feature branch (git checkout -b feature/AmazingFeature)
3.	Commit your changes (git commit -m 'Add some AmazingFeature')
4.	Push to the branch (git push origin feature/AmazingFeature)
5.	Open a pull request
License
Distributed under the MIT License. See LICENSE for more information.

