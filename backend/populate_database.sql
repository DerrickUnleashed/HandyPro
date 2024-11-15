-- Insert data into Customers table
INSERT INTO Customers (CustomerID, Email, Password, Name, Phone, Address, PostalCode) VALUES
(1, 'customer1@example.com', 'password123', 'John Doe', '555-1234', '123 Main St', '12345'),
(2, 'customer2@example.com', 'password456', 'Jane Smith', '555-5678', '456 Oak Ave', '67890');

-- Insert data into Professionals table
INSERT INTO Professionals (ProfessionalID, Email, Password, Name, Experience, Skills, Address, CertificationFile, PostalCode) VALUES
(1, 'professional1@example.com', 'password789', 'Peter Jones', '5 years', 'Plumbing, Electrical', '789 Pine Ln', 'certificate1.pdf', '13579'),
(2, 'professional2@example.com', 'password012', 'Mary Brown', '10 years', 'Carpentry, Painting', '1011 Birch Rd', 'certificate2.pdf', '24680');

-- Insert data into Admins table
INSERT INTO Admins (AdminID, Email, Password, Name) VALUES
(1, 'admin@example.com', 'adminpass', 'Admin User');

-- Insert data into Services table
INSERT INTO Services (ServiceID, ServiceName, Description, BasePrice) VALUES
(1, 'Plumbing Repair', 'Repairing leaky pipes and faucets', 75.00),
(2, 'Electrical Work', 'Installing and repairing electrical systems', 100.00),
(3, 'Painting', 'Interior and exterior painting services', 150.00);

-- Insert data into ServiceRequests table
INSERT INTO ServiceRequests (RequestID, CustomerID, ServiceID, Status) VALUES
(1, 1, 1, 'Completed'),
(2, 2, 3, 'Pending');

-- Insert data into ServiceHistory table
INSERT INTO ServiceHistory (HistoryID, CustomerID, ProfessionalID, ServiceID, Status, CompletionDate) VALUES
(1, 1, 1, 1, 'Completed', '2024-11-02 10:00:00');

-- Insert data into ProfessionalStats table
INSERT INTO ProfessionalStats (ProfessionalID, CompletedRequests, TotalEarnings, AverageRating) VALUES
(1, 1, 75.00, 5.0),
(2, 0, 0.00, 0.0);

-- Insert data into CustomerStats table
INSERT INTO CustomerStats (CustomerID, TotalRequests, AverageRating) VALUES
(1, 1, 5.0),
(2, 1, 0.0);
