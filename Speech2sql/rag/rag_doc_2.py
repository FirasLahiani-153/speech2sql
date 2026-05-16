from langchain_core.documents import Document


def get_rag():
    schema_docs = [
    Document(page_content="""
TABLE: airline
COLUMNS: airline_id, iata, airlinename, base_airport
DESCRIPTION: Stores airline master data, including airline code, airline name, and the airline's base airport.
PRIMARY KEY: airline_id
""", metadata={"type": "schema"}),

    Document(page_content="""
TABLE: airplane
COLUMNS: airplane_id, capacity, type_id, airline_id
DESCRIPTION: Stores individual airplanes operated by airlines, including seating capacity and aircraft type.
PRIMARY KEY: airplane_id
""", metadata={"type": "schema"}),

    Document(page_content="""
TABLE: airplane_type
COLUMNS: type_id, identifier, description
DESCRIPTION: Stores aircraft model or type information, such as identifier and textual description.
PRIMARY KEY: type_id
""", metadata={"type": "schema"}),

    Document(page_content="""
TABLE: airport
COLUMNS: airport_id, iata, icao, name
DESCRIPTION: Stores airport reference information, including IATA code, ICAO code, and airport name.
PRIMARY KEY: airport_id
""", metadata={"type": "schema"}),

    Document(page_content="""
TABLE: airport_geo
COLUMNS: airport_id, name, city, country, latitude, longitude, geolocation
DESCRIPTION: Stores detailed geographic information for airports, including city, country, coordinates, and geolocation point.
PRIMARY KEY: airport_id
""", metadata={"type": "schema"}),

    Document(page_content="""
TABLE: airport_reachable
COLUMNS: airport_id, hops
DESCRIPTION: Stores airport reachability information, indicating the number of hops associated with an airport.
PRIMARY KEY: airport_id
""", metadata={"type": "schema"}),

    Document(page_content="""
TABLE: booking
COLUMNS: booking_id, flight_id, seat, passenger_id, price
DESCRIPTION: Stores passenger bookings for flights, including assigned seat and booking price.
PRIMARY KEY: booking_id
""", metadata={"type": "schema"}),

    Document(page_content="""
TABLE: employee
COLUMNS: employee_id, firstname, lastname, birthdate, sex, street, city, zip, country, emailaddress, telephoneno, salary, department, username, password
DESCRIPTION: Stores employee information, including personal details, contact information, department, salary, and login credentials.
PRIMARY KEY: employee_id
""", metadata={"type": "schema"}),

    Document(page_content="""
TABLE: flight
COLUMNS: flight_id, flightno, from, to, departure, arrival, airline_id, airplane_id
DESCRIPTION: Stores actual flight records, including departure and arrival airports, timing, airline, and assigned airplane.
PRIMARY KEY: flight_id
""", metadata={"type": "schema"}),

    Document(page_content="""
TABLE: flight_log
COLUMNS: flight_log_id, log_date, user, flight_id, flightno_old, flightno_new, from_old, to_old, from_new, to_new, departure_old, arrival_old, departure_new, arrival_new, airplane_id_old, airplane_id_new, airline_id_old, airline_id_new, comment
DESCRIPTION: Stores audit history of flight changes, capturing old and new values for flight details and a comment about the update.
PRIMARY KEY: flight_log_id
""", metadata={"type": "schema"}),

    Document(page_content="""
TABLE: flightschedule
COLUMNS: flightno, from, to, departure, arrival, airline_id, monday, tuesday, wednesday, thursday, friday, saturday, sunday
DESCRIPTION: Stores recurring or scheduled flight information, including route, times, airline, and operating days of the week.
PRIMARY KEY: flightno
""", metadata={"type": "schema"}),

    Document(page_content="""
TABLE: passenger
COLUMNS: passenger_id, passportno, firstname, lastname
DESCRIPTION: Stores basic passenger identity information, including passport number and passenger name.
PRIMARY KEY: passenger_id
""", metadata={"type": "schema"}),

    Document(page_content="""
TABLE: passengerdetails
COLUMNS: passenger_id, birthdate, sex, street, city, zip, country, emailaddress, telephoneno
DESCRIPTION: Stores additional passenger profile and contact details associated with a passenger.
PRIMARY KEY: passenger_id
""", metadata={"type": "schema"}),

    Document(page_content="""
TABLE: weatherdata
COLUMNS: log_date, time, station, temp, humidity, airpressure, wind, weather, winddirection
DESCRIPTION: Stores weather observations for stations at specific dates and times, including temperature, humidity, pressure, wind, and weather condition.
PRIMARY KEY: log_date, time, station
""", metadata={"type": "schema"}),
    ]
    
    relationship_docs = [
    Document(page_content="""
SOURCE TABLE: airline
SOURCE COLUMN: base_airport
TARGET TABLE: airport
TARGET COLUMN: airport_id
DESCRIPTION: Each airline is associated with one base airport.
""", metadata={"type": "relationship"}),

    Document(page_content="""
SOURCE TABLE: airplane
SOURCE COLUMN: type_id
TARGET TABLE: airplane_type
TARGET COLUMN: type_id
DESCRIPTION: Each airplane is associated with one airplane type.
""", metadata={"type": "relationship"}),

    Document(page_content="""
SOURCE TABLE: airplane
SOURCE COLUMN: airline_id
TARGET TABLE: airline
TARGET COLUMN: airline_id
DESCRIPTION: Each airplane is operated by one airline.
""", metadata={"type": "relationship"}),

    Document(page_content="""
SOURCE TABLE: airport_geo
SOURCE COLUMN: airport_id
TARGET TABLE: airport
TARGET COLUMN: airport_id
DESCRIPTION: Each airport_geo record extends one airport with geographic information.
""", metadata={"type": "relationship"}),

    Document(page_content="""
SOURCE TABLE: airport_reachable
SOURCE COLUMN: airport_id
TARGET TABLE: airport
TARGET COLUMN: airport_id
DESCRIPTION: Each airport_reachable record is linked to one airport.
""", metadata={"type": "relationship"}),

    Document(page_content="""
SOURCE TABLE: booking
SOURCE COLUMN: flight_id
TARGET TABLE: flight
TARGET COLUMN: flight_id
DESCRIPTION: Each booking is associated with one flight.
""", metadata={"type": "relationship"}),

    Document(page_content="""
SOURCE TABLE: booking
SOURCE COLUMN: passenger_id
TARGET TABLE: passenger
TARGET COLUMN: passenger_id
DESCRIPTION: Each booking is associated with one passenger.
""", metadata={"type": "relationship"}),

    Document(page_content="""
SOURCE TABLE: flight
SOURCE COLUMN: airline_id
TARGET TABLE: airline
TARGET COLUMN: airline_id
DESCRIPTION: Each flight is operated by one airline.
""", metadata={"type": "relationship"}),

    Document(page_content="""
SOURCE TABLE: flight
SOURCE COLUMN: airplane_id
TARGET TABLE: airplane
TARGET COLUMN: airplane_id
DESCRIPTION: Each flight uses one airplane.
""", metadata={"type": "relationship"}),

    Document(page_content="""
SOURCE TABLE: flight
SOURCE COLUMN: flightno
TARGET TABLE: flightschedule
TARGET COLUMN: flightno
DESCRIPTION: Each flight is linked to a scheduled flight definition through flight number.
""", metadata={"type": "relationship"}),

    Document(page_content="""
SOURCE TABLE: flight
SOURCE COLUMN: from
TARGET TABLE: airport
TARGET COLUMN: airport_id
DESCRIPTION: Each flight departs from one airport.
""", metadata={"type": "relationship"}),

    Document(page_content="""
SOURCE TABLE: flight
SOURCE COLUMN: to
TARGET TABLE: airport
TARGET COLUMN: airport_id
DESCRIPTION: Each flight arrives at one airport.
""", metadata={"type": "relationship"}),

    Document(page_content="""
SOURCE TABLE: flight_log
SOURCE COLUMN: flight_id
TARGET TABLE: flight
TARGET COLUMN: flight_id
DESCRIPTION: Each flight_log entry refers to one flight.
""", metadata={"type": "relationship"}),

    Document(page_content="""
SOURCE TABLE: flightschedule
SOURCE COLUMN: airline_id
TARGET TABLE: airline
TARGET COLUMN: airline_id
DESCRIPTION: Each scheduled flight is operated by one airline.
""", metadata={"type": "relationship"}),

    Document(page_content="""
SOURCE TABLE: flightschedule
SOURCE COLUMN: from
TARGET TABLE: airport
TARGET COLUMN: airport_id
DESCRIPTION: Each scheduled flight departs from one airport.
""", metadata={"type": "relationship"}),

    Document(page_content="""
SOURCE TABLE: flightschedule
SOURCE COLUMN: to
TARGET TABLE: airport
TARGET COLUMN: airport_id
DESCRIPTION: Each scheduled flight arrives at one airport.
""", metadata={"type": "relationship"}),

    Document(page_content="""
SOURCE TABLE: passengerdetails
SOURCE COLUMN: passenger_id
TARGET TABLE: passenger
TARGET COLUMN: passenger_id
DESCRIPTION: Each passengerdetails record extends one passenger with additional personal information.
""", metadata={"type": "relationship"}),
    ]
    join_hints = [
    "booking.flight_id = flight.flight_id",
    "booking.passenger_id = passenger.passenger_id",
    "passengerdetails.passenger_id = passenger.passenger_id",
    "flight.airline_id = airline.airline_id",
    "flight.airplane_id = airplane.airplane_id",
    "flight.flightno = flightschedule.flightno",
    "flight.from = airport.airport_id",
    "flight.to = airport.airport_id",
    "flightschedule.airline_id = airline.airline_id",
    "flightschedule.from = airport.airport_id",
    "flightschedule.to = airport.airport_id",
    "airline.base_airport = airport.airport_id",
    "airplane.type_id = airplane_type.type_id",
    "airplane.airline_id = airline.airline_id",
    "airport_geo.airport_id = airport.airport_id",
    "airport_reachable.airport_id = airport.airport_id",
    "flight_log.flight_id = flight.flight_id",
    ]

    examples = [
 

    Document(page_content="""
QUESTION: List all airlines.
SQL: SELECT * FROM airline;
""", metadata={"type": "example"}),
 
    Document(page_content="""
QUESTION: Show me the names and IATA codes of all airports.
SQL: SELECT iata, name FROM airport;
""", metadata={"type": "example"}),
 
    Document(page_content="""
QUESTION: What countries have airports?
SQL: SELECT DISTINCT country FROM airport_geo;
""", metadata={"type": "example"}),
 
    Document(page_content="""
QUESTION: Show all employees and their departments.
SQL: SELECT firstname, lastname, department FROM employee;
""", metadata={"type": "example"}),
 

    Document(page_content="""
QUESTION: Which airlines are based at airport 1?
SQL: SELECT airlinename FROM airline WHERE base_airport = 1;
""", metadata={"type": "example"}),
 
    Document(page_content="""
QUESTION: Show all flights departing from airport 10.
SQL: SELECT flight_id, flightno, departure FROM flight WHERE `from` = 10;
""", metadata={"type": "example"}),
 
    Document(page_content="""
QUESTION: Find employees who earn more than 5000.
SQL: SELECT firstname, lastname, salary FROM employee WHERE salary > 5000;
""", metadata={"type": "example"}),
 
    Document(page_content="""
QUESTION: Which scheduled flights operate on Monday?
SQL: SELECT flightno, `from`, `to` FROM flightschedule WHERE monday = 1;
""", metadata={"type": "example"}),
 

    Document(page_content="""
QUESTION: List all flights with their airline names.
SQL: SELECT f.flightno, a.airlinename FROM flight f JOIN airline a ON f.airline_id = a.airline_id;
""", metadata={"type": "example"}),
 
    Document(page_content="""
QUESTION: Show all bookings with passenger names.
SQL: SELECT b.booking_id, p.firstname, p.lastname, b.price FROM booking b JOIN passenger p ON b.passenger_id = p.passenger_id;
""", metadata={"type": "example"}),
 
    Document(page_content="""
QUESTION: Show flight numbers with departure and arrival airport names.
SQL: SELECT f.flightno, dep.name AS departure_airport, arr.name AS arrival_airport FROM flight f JOIN airport dep ON f.`from` = dep.airport_id JOIN airport arr ON f.`to` = arr.airport_id;
""", metadata={"type": "example"}),
 
    Document(page_content="""
QUESTION: Show airline names with their base airport names.
SQL: SELECT a.airlinename, ap.name AS base_airport_name FROM airline a JOIN airport ap ON a.base_airport = ap.airport_id;
""", metadata={"type": "example"}),
 
    Document(page_content="""
QUESTION: Show passengers with their contact details.
SQL: SELECT p.firstname, p.lastname, pd.emailaddress, pd.telephoneno, pd.city, pd.country FROM passenger p JOIN passengerdetails pd ON p.passenger_id = pd.passenger_id;
""", metadata={"type": "example"}),
 
    Document(page_content="""
QUESTION: Show all airplanes with their type descriptions and airline names.
SQL: SELECT ap.airplane_id, apt.identifier, apt.description, al.airlinename FROM airplane ap JOIN airplane_type apt ON ap.type_id = apt.type_id JOIN airline al ON ap.airline_id = al.airline_id;
""", metadata={"type": "example"}),

    Document(page_content="""
QUESTION: How many flights are there in total?
SQL: SELECT COUNT(*) AS total_flights FROM flight;
""", metadata={"type": "example"}),
 
    Document(page_content="""
QUESTION: What is the average booking price?
SQL: SELECT AVG(price) AS avg_price FROM booking;
""", metadata={"type": "example"}),
 
    Document(page_content="""
QUESTION: What is the total revenue from all bookings?
SQL: SELECT SUM(price) AS total_revenue FROM booking;
""", metadata={"type": "example"}),
 
    Document(page_content="""
QUESTION: What is the most expensive booking?
SQL: SELECT MAX(price) AS max_price FROM booking;
""", metadata={"type": "example"}),
 

    Document(page_content="""
QUESTION: How many flights does each airline operate?
SQL: SELECT a.airlinename, COUNT(f.flight_id) AS flight_count FROM airline a JOIN flight f ON a.airline_id = f.airline_id GROUP BY a.airlinename;
""", metadata={"type": "example"}),
 
    Document(page_content="""
QUESTION: Which airlines operate more than 5 flights?
SQL: SELECT a.airlinename, COUNT(f.flight_id) AS flight_count FROM airline a JOIN flight f ON a.airline_id = f.airline_id GROUP BY a.airlinename HAVING COUNT(f.flight_id) > 5;
""", metadata={"type": "example"}),
 
    Document(page_content="""
QUESTION: How many airports are in each country?
SQL: SELECT country, COUNT(*) AS airport_count FROM airport_geo GROUP BY country;
""", metadata={"type": "example"}),
 
    Document(page_content="""
QUESTION: Total revenue per airline from bookings.
SQL: SELECT al.airlinename, SUM(b.price) AS total_revenue FROM booking b JOIN flight f ON b.flight_id = f.flight_id JOIN airline al ON f.airline_id = al.airline_id GROUP BY al.airlinename;
""", metadata={"type": "example"}),
 

    Document(page_content="""
QUESTION: What are the 5 most expensive bookings?
SQL: SELECT booking_id, flight_id, passenger_id, price FROM booking ORDER BY price DESC LIMIT 5;
""", metadata={"type": "example"}),
 
    Document(page_content="""
QUESTION: Show the top 3 highest-paid employees.
SQL: SELECT firstname, lastname, salary FROM employee ORDER BY salary DESC LIMIT 3;
""", metadata={"type": "example"}),
 
    Document(page_content="""
QUESTION: List the 5 passengers who spent the most on bookings.
SQL: SELECT p.firstname, p.lastname, SUM(b.price) AS total_spent FROM passenger p JOIN booking b ON p.passenger_id = b.passenger_id GROUP BY p.passenger_id, p.firstname, p.lastname ORDER BY total_spent DESC LIMIT 5;
""", metadata={"type": "example"}),

    Document(page_content="""
QUESTION: Which passengers have booked the most expensive flight?
SQL: SELECT p.firstname, p.lastname FROM passenger p JOIN booking b ON p.passenger_id = b.passenger_id WHERE b.price = (SELECT MAX(price) FROM booking);
""", metadata={"type": "example"}),
 
    Document(page_content="""
QUESTION: Find passengers who have never booked a flight.
SQL: SELECT firstname, lastname FROM passenger WHERE passenger_id NOT IN (SELECT DISTINCT passenger_id FROM booking);
""", metadata={"type": "example"}),
 
    Document(page_content="""
QUESTION: Which employees earn more than the average salary?
SQL: SELECT firstname, lastname, salary FROM employee WHERE salary > (SELECT AVG(salary) FROM employee);
""", metadata={"type": "example"}),
 
    Document(page_content="""
QUESTION: Find airports that are not a base for any airline.
SQL: SELECT name FROM airport WHERE airport_id NOT IN (SELECT base_airport FROM airline);
""", metadata={"type": "example"}),

    Document(page_content="""
QUESTION: Which flights depart after 18:00?
SQL: SELECT flightno, departure FROM flight WHERE TIME(departure) > '18:00:00';
""", metadata={"type": "example"}),
 
    Document(page_content="""
QUESTION: How many flights departed each month?
SQL: SELECT MONTH(departure) AS month, COUNT(*) AS flight_count FROM flight GROUP BY MONTH(departure) ORDER BY month;
""", metadata={"type": "example"}),
 
    Document(page_content="""
QUESTION: Which flights have a duration longer than 5 hours?
SQL: SELECT flightno, departure, arrival, TIMESTAMPDIFF(HOUR, departure, arrival) AS duration_hours FROM flight WHERE TIMESTAMPDIFF(HOUR, departure, arrival) > 5;
""", metadata={"type": "example"}),

    Document(page_content="""
QUESTION: Find all airports with 'International' in their name.
SQL: SELECT name, iata FROM airport WHERE name LIKE '%International%';
""", metadata={"type": "example"}),
 
    Document(page_content="""
QUESTION: Which passengers have a last name starting with 'S'?
SQL: SELECT firstname, lastname FROM passenger WHERE lastname LIKE 'S%';
""", metadata={"type": "example"}),
 
    Document(page_content="""
QUESTION: Show airports in Germany, France, or Italy.
SQL: SELECT a.name, ag.country FROM airport a JOIN airport_geo ag ON a.airport_id = ag.airport_id WHERE ag.country IN ('Germany', 'France', 'Italy');
""", metadata={"type": "example"}),
 
    Document(page_content="""
QUESTION: Show flights departing from Germany.
SQL: SELECT f.flightno, f.departure FROM flight f JOIN airport dep ON f.`from` = dep.airport_id JOIN airport_geo dep_geo ON dep.airport_id = dep_geo.airport_id WHERE dep_geo.country = 'Germany';
""", metadata={"type": "example"}),

Document(page_content="""
QUESTION: Show flights from Germany to France.
SQL: SELECT f.flightno, f.departure FROM flight f JOIN airport dep ON f.`from` = dep.airport_id JOIN airport_geo dep_geo ON dep.airport_id = dep_geo.airport_id JOIN airport arr ON f.`to` = arr.airport_id JOIN airport_geo arr_geo ON arr.airport_id = arr_geo.airport_id WHERE dep_geo.country = 'Germany' AND arr_geo.country = 'France';
""", metadata={"type": "example"}),
    Document(page_content="""
QUESTION: Show the busiest route with the most bookings.
SQL: SELECT dep.name AS from_airport, arr.name AS to_airport, COUNT(b.booking_id) AS booking_count FROM booking b JOIN flight f ON b.flight_id = f.flight_id JOIN airport dep ON f.`from` = dep.airport_id JOIN airport arr ON f.`to` = arr.airport_id GROUP BY f.`from`, f.`to`, dep.name, arr.name ORDER BY booking_count DESC LIMIT 1;
""", metadata={"type": "example"}),
 
    Document(page_content="""
QUESTION: Show passengers who have flown on more than one airline.
SQL: SELECT p.firstname, p.lastname, COUNT(DISTINCT f.airline_id) AS airline_count FROM passenger p JOIN booking b ON p.passenger_id = b.passenger_id JOIN flight f ON b.flight_id = f.flight_id GROUP BY p.passenger_id, p.firstname, p.lastname HAVING COUNT(DISTINCT f.airline_id) > 1;
""", metadata={"type": "example"}),
 
    Document(page_content="""
QUESTION: Show airports with no outgoing flights.
SQL: SELECT a.name FROM airport a LEFT JOIN flight f ON a.airport_id = f.`from` WHERE f.flight_id IS NULL;
""", metadata={"type": "example"}),
 
    Document(page_content="""
QUESTION: Which scheduled flights run every day of the week?
SQL: SELECT flightno FROM flightschedule WHERE monday = 1 AND tuesday = 1 AND wednesday = 1 AND thursday = 1 AND friday = 1 AND saturday = 1 AND sunday = 1;
""", metadata={"type": "example"}),

    Document(page_content="""
QUESTION: What is the average humidity per station?
SQL: SELECT station, AVG(humidity) AS avg_humidity FROM weatherdata GROUP BY station;
""", metadata={"type": "example"}),
 
    Document(page_content="""
QUESTION: Find days where the temperature dropped below 0.
SQL: SELECT DISTINCT log_date, station, temp FROM weatherdata WHERE temp < 0;
""", metadata={"type": "example"}),
 

    Document(page_content="""
QUESTION: Which flights had their departure airport changed?
SQL: SELECT flight_id, from_old, from_new, comment FROM flight_log WHERE from_old != from_new;
""", metadata={"type": "example"}),
 
    Document(page_content="""
QUESTION: How many changes were made per flight?
SQL: SELECT flight_id, COUNT(*) AS change_count FROM flight_log GROUP BY flight_id ORDER BY change_count DESC;
""", metadata={"type": "example"}),
    ]



    return schema_docs + relationship_docs +join_hints+ examples