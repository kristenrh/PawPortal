 CREATE TABLE Animal (

AnimalName VARCHAR(25),

AnimalSpecies VARCHAR(100),

AnimalID SERIAL PRIMARY KEY,

AnimalLocation VARCHAR(5),

LastFed TIMESTAMP,

LastWalk TIMESTAMP,

AnimalAge SMALLINT,

BehaviorType VARCHAR(25)

);

INSERT INTO Animal(

AnimalName,

AnimalSpecies,

AnimalLocation,

LastFed,

LastWalk,

AnimalAge,

BehaviorType

)

VALUES

('Ruby','Mixed Breed','A01','2026-02-19 9:30','2026-02-19 14:30',5,'Aggressive'),

('Mozart', 'Cavalier King Charles Spaniel', 'B01','2026-02-19 9:30', '2026-02-19 14:30',6, 'Energetic'),

('Willow', 'Beagle', 'C01', '2026-02-19 9:30', '2026-02-19 14:30', 12, 'Loner'),

('Jack', 'Cavalier King Charles Spaniel', 'D01', '2026-02-19 9:30', '2026-02-19 14:30', 10, 'Playful'),

('Mini Mae', 'Toy Shih Tzu','E01', '2026-02-19 9:30', '2026-02-19 14:30', 14, 'Vocal');


CREATE TABLE Person(

PersonKey SERIAL PRIMARY KEY,

FirstName VARCHAR(25),

LastName VARCHAR(25),

person_role VARCHAR(10) CHECK(Pers IN ('Staff', 'Volunteer', 'Adopter')),

Status VARCHAR(10)

);


INSERT INTO Person

(FirstName, LastName, PersonRole)

VALUES

('Firstname', 'lastname', 'Volunteer'),

('Firstname', 'lastname', 'Staff'),

('Firstname', 'lastname', 'Volunteer'),

('Firstname', 'lastname', 'Staff'); 
