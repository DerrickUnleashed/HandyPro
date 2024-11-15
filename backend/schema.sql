-- SQLite Script to create the database schema

CREATE TABLE Customers (
    CustomerID INTEGER PRIMARY KEY,
    Email VARCHAR(255) UNIQUE NOT NULL,
    Password VARCHAR(255) NOT NULL,
    Name VARCHAR(255) NOT NULL,
    Phone VARCHAR(20),
    Address VARCHAR(255),
    PostalCode VARCHAR(10)
);

CREATE TABLE Professionals (
    ProfessionalID INTEGER PRIMARY KEY,
    Email VARCHAR(255) UNIQUE NOT NULL,
    Password VARCHAR(255) NOT NULL,
    Name VARCHAR(255) NOT NULL,
    Experience VARCHAR(255),
    Skills TEXT,
    Address VARCHAR(255),
    CertificationFile VARCHAR(255),
    PostalCode VARCHAR(10)
);

CREATE TABLE Admins (
    AdminID INTEGER PRIMARY KEY,
    Email VARCHAR(255) UNIQUE NOT NULL,
    Password VARCHAR(255) NOT NULL,
    Name VARCHAR(255) NOT NULL
);

CREATE TABLE Services (
    ServiceID INTEGER PRIMARY KEY,
    ServiceName VARCHAR(255) NOT NULL,
    Description TEXT,
    BasePrice DECIMAL(10, 2) NOT NULL
);

CREATE TABLE ServiceRequests (
    RequestID INTEGER PRIMARY KEY,
    CustomerID INTEGER NOT NULL,
    ProfessionalID INTEGER,
    ServiceID INTEGER NOT NULL,
    RequestDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    Status TEXT NOT NULL DEFAULT 'Pending',
    Rating INTEGER,
    Review TEXT,
    FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID),
    FOREIGN KEY (ProfessionalID) REFERENCES Professionals(ProfessionalID),
    FOREIGN KEY (ServiceID) REFERENCES Services(ServiceID)
);

CREATE TABLE ServiceHistory (
    HistoryID INTEGER PRIMARY KEY,
    CustomerID INTEGER NOT NULL,
    ProfessionalID INTEGER NOT NULL,
    ServiceID INTEGER NOT NULL,
    Status TEXT NOT NULL,
    CompletionDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID),
    FOREIGN KEY (ProfessionalID) REFERENCES Professionals(ProfessionalID),
    FOREIGN KEY (ServiceID) REFERENCES Services(ServiceID)
);

CREATE TABLE ProfessionalStats (
    ProfessionalID INTEGER PRIMARY KEY,
    CompletedRequests INTEGER DEFAULT 0,
    TotalEarnings DECIMAL(10, 2) DEFAULT 0,
    AverageRating REAL DEFAULT 0,
    FOREIGN KEY (ProfessionalID) REFERENCES Professionals(ProfessionalID)
);

CREATE TABLE CustomerStats (
    CustomerID INTEGER PRIMARY KEY,
    TotalRequests INTEGER DEFAULT 0,
    AverageRating REAL DEFAULT 0,
    FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID)
);
