from flask import Flask, render_template, request, redirect, url_for, send_from_directory, session, jsonify, flash, make_response, render_template_string
import sqlite3
from datetime import datetime

app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.secret_key = "secret_key"

def render_webPage(navBarContent=None, webPageContent=None):
    navBarContent = navBarContent or '/MainNavBar/'
    webPageContent = webPageContent or 'home.html'   
    return render_template('index.html',navbar = navBarContent,iframeSrc=webPageContent)

@app.route("/", methods=['GET'])
def index():
    return render_webPage()

@app.route('/AdminNavBar/',methods=['GET'])
def AdminNavBar():
    return render_template('AdminNavBar.html')

@app.route("/MainNavBar/",methods=['GET','POST'])
def MainNavBar():
    return render_template('MainNavBar.html')

@app.route("/CustomerNavBar/",methods=['GET','POST'])
def CustomerNavBar():
    return render_template('CustomerNavBar.html')

@app.route("/ProfessionalNavBar/",methods=['GET','POST'])
def ProfessionalNavBar():
    return render_template('ProfessionalNavBar.html')

@app.route('/home',methods=['GET'])
def home():
    return render_webPage(webPageContent='home.html')

@app.route("/home.html", methods=['GET'])
def homeredirect():    
    return render_template('home.html')

@app.route('/contact',methods=['GET'])
def contact():
    return render_webPage(webPageContent='Contact.html')

@app.route('/Contact.html',methods=['GET','POST'])
def CONTACT():
    return render_template('Contact.html')

@app.route('/about',methods=['GET'])
def about():
    return render_webPage(webPageContent='AboutUs.html')

@app.route('/AboutUs.html',methods=['GET'])
def ABOUT():
    return render_template('AboutUs.html')

@app.route('/privacyPolicy',methods=['GET'])
def privacyPolicy():
    return render_webPage(webPageContent='PrivacyPolicy.html')

@app.route('/PrivacyPolicy.html',methods=['GET'])
def PRIVACYPOLICY():
    return render_template('PrivacyPolicy.html')

@app.route('/faq',methods=['GET'])
def faq():
    return render_webPage(webPageContent='Faq.html')

@app.route('/Faq.html',methods=['GET'])
def FAQ():
    return render_template('Faq.html')

@app.route('/toc',methods=['GET'])
def toc():
    return render_webPage(webPageContent='toc.html')

@app.route('/toc.html',methods=['GET'])
def TOC():
    return render_template('toc.html')

@app.route('/signUpCustomer', methods=['GET']) 
def signupCustomer():
    return render_webPage(webPageContent='Signup_Customer.html')

@app.route('/Signup_Customer.html',methods=['GET','POST'])
def SIGNUPCUSTOMER():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']
        postalCode = request.form['postalCode']
        password = request.form['password']
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO Customers (Name, Email, Phone, Address, PostalCode, Password) VALUES (?, ?, ?, ?, ?, ?)", (name, email, phone, address, postalCode, password))
            cursor.execute("INSERT INTO user_credentials (email, password, user_type) VALUES (?, ?, ?)", (email, password, "Customer"))
            conn.commit()
            print('Customer registered successfully!')
        except sqlite3.IntegrityError:
            print('Email already exists. Please use a different email.')
            flash('Email already exists. Please use a different email.', 'error') 
        except Exception as e:
            print(f'An error occurred: {e}')
            flash(f'An error occurred: {e}', 'error') 
        finally:
            conn.close()
        return redirect(url_for('login'))
    return render_template('Signup_Customer.html')

@app.route('/login',methods=['GET'])
def login():
    return render_webPage(webPageContent='Login.html')

@app.route('/Login.html',methods=['GET','POST'])
def loginPage():
    print("works")
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user_credentials WHERE email=? AND password =?", (email, password))
        user = cursor.fetchone()
        if not user:
            flash('Invalid email or password. Please try again.', 'error')
            return redirect(url_for('login'))
        if user[3] == "Admin":
            session['user_type'] = "admin"
            session['user_iignup_Customer.htmld'] = user[0]
            return redirect(url_for('admin_dashboard'))
        elif user[3] == "Customer":
            session['user_type'] = "customer"
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute("SELECT CustomerID FROM Customers WHERE email=?", (email,))
            id = cursor.fetchone()
            session['customer_id'] = id[0]
            print(session['customer_id'])
            return redirect(url_for('customer_homepage'))
        elif user[3] == "Professional":
            session['user_type'] = "professional"
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute("SELECT ProfessionalID,Approved FROM Professionals WHERE email=?", (email,))
            id = cursor.fetchone()
            session['professional_id'] = id[0]
            print(session['professional_id'])
            approved = id[1]
            if(approved):
                return redirect(url_for('professional_dashboard'))
            else:
                flash("Please wait for Admin Approval")
                return redirect(url_for('login'))
        conn.close()
    else:
        return render_template('Login.html')

@app.route('/signupProfessional', methods=['GET', 'POST'])
def signupProfessional():
    return render_webPage(webPageContent='Signup_Professional.html')

@app.route('/Signup_Professional.html',methods=['GET','POST'])
def SIGNUPPROFESSIONAL():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        experience = request.form['experience']
        skills = request.form['skills']
        address = request.form['address']
        certification = request.files['certification']
        postalCode = request.form['postalCode']
        password = request.form['password']

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO Professionals (Name, Email, Experience, Skills, Address, PostalCode, Password) VALUES (?, ?, ?, ?, ?, ?, ?)", (name, email, experience, skills, address, postalCode, password))
            cursor.execute("INSERT INTO user_credentials (email, password, user_type) VALUES (?, ?, ?)", (email, password, "Professional"))
            conn.commit()
            print('Professional registered successfully!')
        except sqlite3.IntegrityError:
            print('Email already exists. Please use a different email.')
            flash('Email already exists. Please use a different email.', 'error') 
        except Exception as e:
            print(f'An error occurred: {e}')
            flash(f'An error occurred: {e}', 'error') 
        finally:
            conn.close()
        return redirect(url_for('login'))
    return render_template('Signup_Professional.html')

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('../static', path)

@app.route('/admin',methods=['GET'])
def admin_dashboard():
    return render_webPage(navBarContent='/AdminNavBar/',webPageContent='Admin_Dashboard.html')

@app.route('/Admin_Dashboard.html', methods=['GET', 'POST'])
def admin():
    if 'user_type' not in session or session['user_type'] != 'admin':
        return redirect(url_for('login'))
    return render_template('Admin_Dashboard.html',escape_iframe=True)

@app.route('/customer',methods=['GET'])
def customer_homepage():
    return render_webPage(navBarContent='/CustomerNavBar/',webPageContent='Customer_Homepage.html')

@app.route('/Customer_Homepage.html')
def customer():
    if 'user_type' not in session or session['user_type'] != 'customer':
        return redirect(url_for('login'))
    return render_template('Customer_Homepage.html')

@app.route('/professional',methods=['GET'])
def professional_dashboard():
    return render_webPage(navBarContent='/ProfessionalNavBar/',webPageContent='Professional_Dashboard.html')

@app.route('/Professional_Dashboard.html')
def professional():
    if 'user_type' not in session or session['user_type'] != 'professional':
        return redirect(url_for('login'))
    return render_template('Professional_Dashboard.html')

@app.route('/adminManageServices',methods=['GET'])
def admin_manage_services():
    return render_webPage(navBarContent='/AdminNavBar/',webPageContent='Admin_Manage_Services.html')

@app.route('/Admin_Manage_Services.html', methods=['GET', 'POST'])
def adminManageServices():
    if 'user_type' not in session or session['user_type'] != 'admin':
        return redirect(url_for('login'))
    if request.method == 'POST':
        action = request.form.get('action')
        service_id = request.form.get('service_id')
        if action == 'add':
            service_name = request.form['service_name']
            base_price = request.form['base_price']
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Services (ServiceName, BasePrice) VALUES (?, ?)", (service_name, base_price))
            conn.commit()
            conn.close()
            print('Service added successfully!')
        elif action == 'update':
            service_name = request.form['service_name']
            base_price = request.form['base_price']
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute("UPDATE Services SET ServiceName = ?, BasePrice = ? WHERE ServiceID = ?", (service_name, base_price, service_id))
            conn.commit()
            conn.close()
            print('Service updated successfully!')
        elif action == 'delete':
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Services WHERE ServiceID = ?", (service_id,))
            conn.commit()
            conn.close()
            print('Service deleted successfully!')
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Services")
    services = cursor.fetchall()
    conn.close()
    return render_template('Admin_Manage_Services.html', services=services)

@app.route('/adminManageProfessionals',methods=['GET'])
def admin_manage_professionals():
    return render_webPage(navBarContent='/AdminNavBar/',webPageContent='Admin_Manage_Professionals.html')

@app.route('/Admin_Manage_Professionals.html', methods=['GET', 'POST'])
def ADMINMANAGEPROFESSIONALS():
    if 'user_type' not in session or session['user_type'] != 'admin':
        return redirect(url_for('login'))
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Professionals WHERE ProfessionalID != 8")
    professionals = cursor.fetchall()
    conn.close()
    if request.method == 'POST':
        action = request.form.get('action')
        professional_id = request.form.get('professional_id')
        print(professional_id)
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        if action == 'approve':
            cursor.execute("UPDATE Professionals SET Approved = 1 WHERE ProfessionalID = ?", (professional_id,))
            conn.commit()
            print('Professional approved successfully!')
        elif action == 'disapprove':
            cursor.execute("UPDATE Professionals SET Approved = 0 WHERE ProfessionalID = ?", (professional_id,))
            conn.commit()
            print('Professional disapproved successfully!')
        print(action)
        if action == 'reject':
            try:
                professional_id = int(professional_id)
                cursor.execute("DELETE FROM Professionals WHERE ProfessionalID = ?", (professional_id,))
                conn.commit()
                print('Professional rejected successfully!')
            except ValueError:
                print('Invalid professional ID.')
            except Exception as e:
                print(f'An error occurred while rejecting the professional: {e}')
        conn.close()
        return redirect(url_for('admin_manage_professionals'))
    return render_template('Admin_Manage_Professionals.html', professionals=professionals)
@app.route('/adminManageRequests',methods=['GET'])
def admin_manage_requests():
    return render_webPage(navBarContent='/AdminNavBar/',webPageContent='Admin_Manage_Requests.html')

@app.route('/Admin_Manage_Requests.html')
def ADMINMANAGEREQUESTS():
    if 'user_type' not in session or session['user_type'] != 'admin':
        return redirect(url_for('login'))
    if request.method == 'POST':
        action = request.form.get('action')
        service_id = request.form.get('service_id')
        if action == 'add':
            service_name = request.form['service_name']
            base_price = request.form['base_price']
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Services (ServiceName, BasePrice) VALUES (?, ?)", (service_name, base_price))
            conn.commit()
            conn.close()
            print('Service added successfully!')
        elif action == 'update':
            service_name = request.form['service_name']
            base_price = request.form['base_price']
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute("UPDATE Services SET ServiceName = ?, BasePrice = ? WHERE ServiceID = ?", (service_name, base_price, service_id))
            conn.commit()
            conn.close()
            print('Service updated successfully!')
        elif action == 'delete':
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Services WHERE ServiceID = ?", (service_id,))
            conn.commit()
            conn.close()
            print('Service deleted successfully!')
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ServiceRequests")
    services = cursor.fetchall()
    conn.close()
    return render_template('Admin_Manage_Requests.html', services=services)
@app.route('/customerSearch',methods=['GET'])
def customer_search():
    return render_webPage(navBarContent='/CustomerNavBar/',webPageContent='Customer_Search.html')

@app.route('/Customer_Search.html', methods=['GET'])
def CUSTOMER_SEARCH():
    search_query = request.args.get('searchQuery')
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    if search_query:
        cursor.execute("SELECT * FROM Services WHERE ServiceName LIKE ?", ('%' + search_query + '%',))
        search_results = cursor.fetchall()
    else:
        cursor.execute("SELECT * FROM Services")
        search_results = cursor.fetchall()
    conn.close()
    return render_template('Customer_Search.html', search_results=search_results)

@app.route('/Admin_Search.html', methods=['GET', 'POST'])
def admin_search():
    if 'user_type' not in session or session['user_type'] != 'admin':
        return redirect(url_for('login'))
    if request.method == 'POST':
        search_query = request.form['searchQuery']
        search_type = request.form['searchType']
        search_results = []
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        if search_type == 'serviceId':
            cursor.execute("SELECT * FROM Services WHERE ServiceID = ?", (search_query,))
        elif search_type == 'professionalID':
            cursor.execute("SELECT * FROM Professionals WHERE ProfessionalID = ?", (search_query,))
        elif search_type == 'customerID':
            cursor.execute("SELECT * FROM Customers WHERE CustomerID = ?", (search_query,))
        elif search_type == 'serviceName':
            cursor.execute("SELECT * FROM Services WHERE ServiceName LIKE ?", ('%' + search_query + '%',))
        search_results = cursor.fetchall()
        conn.close()
        return render_template('Admin_Search.html', search_results=search_results, search_type=search_type)
    return render_template('Admin_Search.html')

@app.route('/customerServiceHistory',methods=['GET'])
def customer_service_history():
    return render_webPage(navBarContent='/CustomerNavBar/',webPageContent='Customer_Service_History.html')

@app.route('/Customer_Service_History.html', methods=['POST','GET'])
def CUSTOMERSERVICEHISTORY():
    customer_id = session.get('customer_id')
    if not customer_id:
        print("Please log in to view your service history.")
        return redirect(url_for('login'))
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            RequestID, Name, Email, ServiceName, RequestDate, Status, Rating, Review 
        FROM ServiceRequests sr 
        JOIN Services s ON sr.ServiceID = s.ServiceID 
        JOIN Professionals p ON p.ProfessionalID = sr.ProfessionalID 
        WHERE CustomerID = ?
    """, (customer_id,))
    service_history = cursor.fetchall()
    if request.method == 'POST':
        # Handle request cancellation
        if 'cancel_request_id' in request.form:
            request_id = request.form.get('cancel_request_id')
            try:
                cursor.execute("""
                    UPDATE ServiceRequests 
                    SET Status = 'Cancelled' 
                    WHERE RequestID = ? AND CustomerID = ? AND Status = 'Requested'
                """, (request_id, customer_id))
                conn.commit()
                conn.close()
                return redirect(url_for('CUSTOMERSERVICEHISTORY'))
            except Exception as e:
                print(f"Error cancelling request: {e}")
                conn.close()
                return redirect(url_for('CUSTOMERSERVICEHISTORY'))
        request_id = request.form.get('request_id')
        rating = request.form.get('rating')
        review = request.form.get('review')
        
        if all([request_id, rating, review]):
            try:
                cursor.execute("""
                    UPDATE ServiceRequests 
                    SET Rating = ?, Review = ?, Status = 'Closed' 
                    WHERE RequestID = ? AND CustomerID = ? AND Status = 'Accepted'
                """, (rating, review, request_id, customer_id))
                conn.commit()
                print(f"Review and rating submitted for request {request_id}")
            except Exception as e:
                print(f"Error updating review and rating: {e}")
            finally:
                conn.close()
            return redirect(url_for('CUSTOMERSERVICEHISTORY'))
    conn.close()
    if service_history:
        return render_template('Customer_Service_History.html', service_history=service_history)
    else:
        print(f'No service history found for customer ID {customer_id}')
        return render_template('Customer_Service_History.html')

@app.route('/addService',methods=['GET'])
def ADDSERVICE():
    return render_webPage(navBarContent='/AdminNavBar/',webPageContent='Add_Service.html')

@app.route('/Add_Service.html', methods=['GET', 'POST'])
def add_service():
    if request.method == 'POST':
        service_name = request.form['serviceName']
        description = request.form['description']
        base_price = request.form['basePrice']
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO Services (ServiceName, Description, BasePrice) VALUES (?, ?, ?)", (service_name, description, base_price))
            conn.commit()
            print('Service added successfully!')
        except Exception as e:
            print(f'An error occurred: {e}')
        finally:
            conn.close()
        return redirect(url_for('admin_manage_services'))
    return render_template('Add_Service.html')

@app.route('/Professional_Search.html', methods=['GET'])
def professional_search():
    return render_template('Professional_Search.html')

@app.route('/adminSummary',methods=['GET'])
def ADMINSUMMARY():
    return render_webPage(navBarContent='/AdminNavBar/',webPageContent='Admin_Summary.html')

@app.route('/Admin_Summary.html')
def admin_summary():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("SELECT Rating , COUNT(Rating) FROM ServiceRequests GROUP BY Rating HAVING Rating NOT NULL")
    customer_data = cur.fetchall()
    print(customer_data)
    ratings = {}
    for i in customer_data:
        ratings[str(i[0])] = i[1]
    return render_template('Admin_Summary.html',ratings=jsonify(ratings))
@app.route('/customerSummary',methods=['GET'])
def customer_summary():
    return render_webPage(navBarContent='/CustomerNavBar/',webPageContent='Customer_Summary.html')
@app.route('/Customer_Summary.html')
def CUSTOMERSUMMARY():
    customer_id = session.get('customer_id')
    if not customer_id:
        return redirect(url_for('login'))

    # Get customer data from the database
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM Customers WHERE CustomerID = ?", (customer_id,))
    customer_data = cur.fetchone()
    cur.execute("""
        SELECT s.ServiceName, sr.Status
        FROM ServiceRequests sr
        JOIN Services s ON sr.serviceId = s.ServiceID
        WHERE sr.CustomerID = ?
    """, (customer_id,))
    service_history = cur.fetchall()
    cur.execute("""
        SELECT Rating
        FROM ServiceRequests
        WHERE CustomerID = ?
    """, (customer_id,))
    rating = cur.fetchall()
    try:
        average_rating = sum(r[0] for r in rating if r[0] is not None) / len(list(r[0] for r in rating if r[0] is not None)) if rating else None
    except ZeroDivisionError:
        average_rating = None
    return render_template('Customer_Summary.html', customer=customer_data, service_history=service_history, average_rating=average_rating, rating = rating)


@app.route('/Review_Submission.html', methods=['GET', 'POST'])
def review_submission():
    return render_template('Review_Submission.html')

@app.route('/Service_Request.html')
def service_request():
    return render_template('Service_Request.html')

@app.route('/add_service_request', methods=['POST'])
def add_service_request():
    try:
        service_id = request.form['serviceId']
        customer_id = session.get('customer_id')

        if not customer_id:
            print("Please log in to book a service.")
            return redirect(url_for('login'))

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        time = str(datetime.now())[:-7]
        cursor.execute("INSERT INTO ServiceRequests (serviceID, professionalID,customerID,RequestDate) VALUES (?, ?,?,?)", (service_id, 8, customer_id,time))
        conn.commit()
        conn.close()
        print('Service request submitted successfully!')
        return redirect(url_for('customer_search'))
    except Exception as e:
        print(f'An error occurred: {e}')
        return redirect(url_for('customer_search'))
@app.route('/professionalServiceToday',methods=['GET'])
def professional_services_today():
    return render_webPage(navBarContent='/ProfessionalNavBar/',webPageContent='Professional_Services_Today.html')

@app.route('/Professional_Services_Today.html', methods=['GET', 'POST'])
def PROFESSIONALSERVICESTODAY():
    professional_id = session.get('professional_id')
    if not professional_id:
        print("Please log in as a professional.")
        return redirect(url_for('login'))

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT Name,Phone,Address,PostalCode,RequestID,ServiceName 
                   FROM ServiceRequests sr JOIN Customers c ON c.CustomerID = sr.CustomerID JOIN Services s ON s.ServiceID = sr.ServiceID
                   WHERE Status = ? AND ProfessionalID = ?''', ('Accepted', professional_id))
    requests = cursor.fetchall()
    print(requests)
    conn.close()

    

    return render_template('Professional_Services_Today.html', requests=requests)


@app.route('/logout')
def logout():
    session.pop('user_type', None)
    session.pop('id', None)
    return redirect(url_for('index'))

@app.route('/serviceDetails',methods=['GET'])
def service_details():
    service_id = request.args.get('service_id')
    s = 'Service_Details.html?service_id='+service_id
    return render_webPage(navBarContent='/AdminNavBar/',webPageContent=s)

@app.route('/Service_Details.html')
def SERVICEDETAILS():
    service_id = request.args.get('service_id')
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT ServiceName, Description, BasePrice FROM Services WHERE ServiceID = ?", (service_id,))
    service_data = cursor.fetchone()
    conn.close()
    return render_template('Service_Details.html', service=service_data)
@app.route('/professionalProfile',methods=['GET'])
def professional_profile():
    professional_id = request.args.get('professional_id')
    s = 'Professional_Profile.html?professional_id='+professional_id
    return render_webPage(navBarContent='/AdminNavBar/',webPageContent=s)

@app.route('/Professional_Profile.html')
def PROFESSIONALPROFILE():
    professional_id = request.args.get('professional_id')
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Professionals WHERE ProfessionalID = ?", (professional_id,))
    professional = cursor.fetchone()
    conn.close()
    return render_template('Professional_Profile.html', professional=professional)

@app.route('/professionalServiceHistory',methods=['GET'])
def professional_service_history():
    return render_webPage(navBarContent='/ProfessionalNavBar/',webPageContent='Professional_Service_History.html')

@app.route('/Professional_Service_History.html', methods=['GET'])
def PROFESSIONALSERVICEHISTORY():
    professional_id = session.get('professional_id')
    if not professional_id:
        return redirect(url_for('login'))

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT RequestID,Rating,Review,ServiceName
        FROM ServiceRequests sr JOIN Services s ON sr.serviceID = s.ServiceID
        WHERE ProfessionalID = ? AND Status = 'Closed'
    """, (professional_id,))
    service_history = cursor.fetchall()
    conn.close()
    print(service_history)
    return render_template('Professional_Service_History.html', service_history=service_history)

@app.route('/professionalRequests',methods=['GET'])
def professional_requests():
    return render_webPage(navBarContent='/ProfessionalNavBar/',webPageContent='Professional_Requests.html')

@app.route('/Professional_Requests.html', methods=['GET','POST'])
def PROFESSIONALREQUESTS():
    professional_id = session.get('professional_id')
    if not professional_id:
        return redirect(url_for('login'))
    request_id = request.form.get('request_id')
    if request.method =='POST':
        print(request_id,professional_id)
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE ServiceRequests SET Status = 'Accepted',ProfessionalID = ? WHERE RequestID = ?", (professional_id,request_id))
        conn.commit()
        conn.close()
        return redirect(url_for('professional_requests'))

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT RequestID,ServiceName,RequestDate,Description,BasePrice
        FROM ServiceRequests sr JOIN Services s ON sr.serviceID = s.ServiceID
        WHERE Status = 'Requested'
    """)
    service_history = cursor.fetchall()
    conn.close()
    service_history = [list(i) for i in service_history]
    for i in service_history:
        i[3] = i[3].split('.')[0]
    return render_template('Professional_Requests.html', service_history=service_history)

@app.route('/professionalSummary',methods=['GET'])
def professional_summary():
    return render_webPage(navBarContent='/ProfessionalNavBar/',webPageContent='Professional_Summary.html')

@app.route('/Professional_Summary.html')
def PROFESSIONALSUMMARY():
    requested_count = 10  # Replace with your actual data retrieval
    accepted_count = 5
    closed_count = 3
    average_rating = 4.5
    return render_template('Professional_Summary.html', requested_count=requested_count, accepted_count=accepted_count, closed_count=closed_count, average_rating=average_rating)

@app.route('/customerProfile',methods=['GET'])
def customer_profile():
    return render_webPage(navBarContent='/CustomerNavBar/',webPageContent='Customer_Profile.html')

@app.route('/Customer_Profile.html', methods=['GET', 'POST'])
def CUSTOMERPROFILE():
    customer_id = session.get('customer_id')
    if not customer_id:
        return redirect(url_for('login'))
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Customers WHERE CustomerID = ?", (customer_id,))
    customer = cursor.fetchone()
    conn.close()
    if request.method == 'POST':
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT email FROM Customers WHERE CustomerID = ?",(customer_id,))
        oemail = cursor.fetchone()[0]
        cursor.execute("SELECT id FROM user_credentials WHERE email=?",(oemail,))
        id = cursor.fetchone()[0]
        name = request.form.get("name")
        email = request.form.get("email")
        address = request.form.get("address")
        phone = request.form.get("phone")
        password = request.form.get("password")
        postalcode = request.form.get("postal_code")
        updated_data = (name, email, address, phone, password, postalcode, customer_id)
        cursor.execute("UPDATE user_credentials SET email = ? WHERE id = ?",(email,id))
        conn.commit()
        cursor.execute("""
            UPDATE Customers
            SET Name = ?, Email = ?, Address = ?, Phone = ?, Password = ?, PostalCode = ?
            WHERE CustomerID = ?
        """, updated_data)  
        conn.commit()
        conn.close()
        return redirect(url_for('customer_profile')) 
    return render_template('Customer_Profile.html',customer=customer)

@app.route('/professionalProfileEdit',methods=['GET'])
def professional_profile_edit():
    return render_webPage(navBarContent='/ProfessionalNavBar/',webPageContent='Professional_Profile_Edit.html')

@app.route('/Professional_Profile_Edit.html', methods=['GET', 'POST'])
def PROFESSIONALPROFILEEDIT():
    professional_id = session.get('customer_id')
    if not professional_id:
        return redirect(url_for('login'))
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Professionals WHERE ProfessionalID = ?", (professional_id,))
    customer = cursor.fetchone()
    conn.close()
    if request.method == 'POST':
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT email FROM Professionals WHERE ProfessionalID = ?",(professional_id,))
        oemail = cursor.fetchone()[0]
        cursor.execute("SELECT id FROM user_credentials WHERE email=?",(oemail,))
        id = cursor.fetchone()[0]
        name = request.form.get("name")
        email = request.form.get("email")
        address = request.form.get("address")
        phone = request.form.get("phone")
        password = request.form.get("password")
        postalcode = request.form.get("postal_code")
        experience = request.form.get("experience")
        skills = request.form.get("skills")
        updated_data = (name, email, address, phone, password, postalcode, experience, skills, professional_id)
        cursor.execute("UPDATE user_credentials SET email = ? WHERE id = ?",(email,id))
        conn.commit()
        cursor.execute("""
            UPDATE Professionals
            SET Name = ?, Email = ?, Address = ?, Phone = ?, Password = ?, PostalCode = ?,experience = ?,skills = ?
            WHERE ProfessionalID = ?
        """, updated_data)
        conn.commit()
        conn.close()
        return redirect(url_for('professional_profile_edit')) 
    return render_template('Professional_Profile_Edit.html',customer=customer)

@app.route('/Signup_Customer.html', methods=['GET', 'POST'])
def signup_customer_html():
    return signupCustomer()

if __name__ == '__main__':
    app.run(debug=True)
