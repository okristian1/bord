#readme


Purpouse

Keep a updatable list of every table in every restaurant. 

Problem. A restaurant responds with only booked tables when api is queried, not empty tables.
This makes it impossible to know if a restaurant has a free table or not.

Solution. Check the booking for the restaurant every day for a year. That should give a pretty
accurate overview of what tables the restaurant has with an acceptable error rate. If a new table
is found. Update list of tables for that restaurant with table number and number of guests for an
estimation for number of seats a table can have. 

Things to watch out for. Tables being temporarily connected. Divide guests by number of tables or 
even ignore such anomalies. Update table seats if number of seats for a booking is higher than 
previous. Consider ignoring certain unrealistic number increases.

Consider that some tables might be unused for periods of time or even most of the year. Examples
can be outside areas, VIP tables, rooms being fixed or even just not open during low season. 


Pick shorter timeperiod than a year for testing.



Then just match the empty tables against the occupied once 


Check for official bookatable api?
