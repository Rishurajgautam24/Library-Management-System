# Library Management System

## Final Project Report

### AUTHOR
- **Name**: Rishu Raj Gautam
- **About Me**: I leverage data to drive impactful applications and strategic decisions. Combining a background in Mathematics & Computer Applications with a passion for coding, I'm adept at Python, web development frameworks, and machine learning. I'm also enthusiastic about education, creating content to empower others.

### DESCRIPTION OF PROJECT
A library may operate more efficiently by managing books, users, transactions, and comments with the use of a Library Management System, a comprehensive software solution. With tools for managing user accounts, cataloguing books, processing loan and return procedures, gathering feedback, and more, this system meets the demands of users, librarians, and administrators.

### TECHNOLOGIES USED
- **Flask**: Backend framework for building the web application.
- **SQLAlchemy**: ORM (Object-Relational Mapping) tool for database interactions.
- **SQLite**: Database management system for storing application data.
- **HTML/CSS/JavaScript**: Frontend technologies for user interface design and interactivity.
- **Flask-Login**: Extension for managing user sessions and authentication.
- **Datetime**: Python library for handling date and time operations.

### ARCHITECTURE
The main code to run the web app is contained in the `Main.py` file. `LMS` (Library Management System) is a module that contains all the files for the app. Here's a description of files inside `LMS`:
- `Api.py`: Contains UserAPI, SectionAPI, BookAPI.
- `Auth.py`: Contains Authorization logic like login, signup.
- `Graphs.py`: Contains logic for generating graphs for the dashboard.
- `Librarian.py`: Contains all functionalities related to Librarian.
- `Models.py`: Contains DB Classes.
- `User.py`: Contains all functionalities related to User.
- `Validation.py`: Contains error handling logic for API.
- `Views.py`: Contains Normal view for guest user.
- `Templates`: Contains all HTML templates for User, Librarian, authorization.
- `Static`: Contains CSS and image files.

### FEATURES
#### User Management:
- Registration and authentication for users (librarians and regular users).
- User roles (librarian or regular user) to control access and permissions.
- User profile management including personal details like name, email, contact number, etc.

#### Book Management:
- Cataloging and indexing of books with details such as title, author, ISBN, content, availability status, etc.
- Classification of books into sections for easy navigation and organization.
- Ability to add, edit, and delete books from the system.

#### Transaction Management:
- Tracking of book transactions including borrowing and returning activities.
- Automatic updates to book availability status upon transactions.
- Due date management and reminders for users to return borrowed books on time.

#### Borrow Request Management:
- Facility for users to request book borrowings.
- Approval workflow for librarian review and processing of borrow requests.
- Monitoring and updating the status of borrow requests (e.g., pending, approved, rejected).

#### Feedback System:
- Collection of user feedback on borrowed books.

#### Download Access Control:
- Provision for users to download digital copies of books (if available).
- Permission-based access control to regulate downloading privileges.

### DB SCHEMA DESIGN
The database schema consists of tables for users, sections, books, transactions, borrow requests, downloads, and feedback. Relationships are established between these tables to track user activities such as borrowing, requesting, downloading, and providing feedback on books. Each table contains relevant fields such as user details, book information, transaction dates, request statuses, and feedback text, ensuring comprehensive data management within the library system.

### FUTURE ENHANCEMENTS
- Implementing a reservation system for requested books.
- Adding advanced search and filtering options for books.
- Enhancing the user interface for better user experience.
- Integrating email notifications for overdue books, approved requests, etc.

### VIDEO LINK
Video demonstration of my project is available [here](https://youtu.be/F5NynPbNYl0).

### THANK YOU
Thank you for viewing my project! Feel free to reach out if you have any questions or feedback.
