-- Drop and recreate the Professionals table to add the Phone column with a unique constraint
DROP TABLE IF EXISTS Professionals;

CREATE TABLE Professionals (
    ProfessionalID INTEGER PRIMARY KEY,
    Email VARCHAR(255) UNIQUE NOT NULL,
    Password VARCHAR(255) NOT NULL,
    Name VARCHAR(255) NOT NULL,
    Experience VARCHAR(255),
    Skills TEXT,
    Address VARCHAR(255),
    CertificationFile VARCHAR(255),
    PostalCode VARCHAR(10),
    Phone TEXT UNIQUE
);
