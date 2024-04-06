import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="santhi12",
    database="homeserviceapp"
)
mycursor = mydb.cursor(buffered=True)


# Newuser register
def newuser_register():
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    mobile_no = input("Enter your Mobile No: ")
    address = input("Enter your Address: ")
    mycursor.execute("INSERT INTO User (UserName, Password, MobileNo, Address) VALUES (%s, %s, %s, %s)",
                     (username, password, mobile_no, address))
    mydb.commit()
    print("Registration successful. Welcome to Home Service App")

# NewService register
def newservice_register():
    servicename = input("Enter your servicename: ")
    cost= input("Cost of the service: ")
    Description = input("Description: ")
    mycursor.execute("INSERT INTO Services (ServiceName,Cost,Description) VALUES (%s, %s, %s)",
                     (servicename,cost,Description))
    mydb.commit()
    print("-----------------Service Registration successful----------------------------")


# register service provider
def register_service_provider(service_id):
    name = input("Enter service provider name: ")
    location = input("Enter service provider location: ")
    rating = float(input("Enter service provider rating (0-5): "))
    mycursor.execute("INSERT INTO ServiceProvider (ProviderName, Location, Rating, ServiceID) VALUES (%s, %s, %s, %s)",
                     (name, location, rating, service_id))
    mydb.commit()

    mycursor.execute("SELECT ProviderID FROM ServiceProvider WHERE ProviderName=%s AND Location=%s AND ServiceID=%s",
                     (name, location, service_id))
    provider_id = mycursor.fetchone()
    provider=provider_id[0]

    address = input(f"Enter {name} location address in {location}: ")
    rating = input("Enter location rating (0-5): ")
    mycursor.execute("INSERT INTO Locations (LocationName, Address, Rating,ProviderID) VALUES (%s, %s, %s,%s)",
                     (location, address, rating,provider))
    mydb.commit()
    print(f"--------------{name} registered successfully--------------------")

    print("______________________Register worker details_____________________")

    mycursor.execute("SELECT LocationID FROM Locations WHERE LocationName=%s AND Address=%s",
                     (location,address))
    location_id = mycursor.fetchone()
    if location_id:
        locationID = location_id[0]

    workername = input("Enter worker name: ")
    workermobileno=input("Enter worker Mobile No: ")
    rating = input("Enter worker rating (0-5): ")
    mycursor.execute("INSERT INTO Workers (WorkerName,WorkerMobileNo,LocationID, Rating) VALUES (%s, %s, %s,%s)",
                     (workername,workermobileno,locationID,rating))
    mydb.commit()
    print(f"--------------------Worker registered in {name } successfully----------------------------------")


# user login
def user_login(username, password):
    mycursor.execute("SELECT * FROM User WHERE UserName = %s AND Password = %s", (username, password))
    data = mycursor.fetchall()
    return bool(data)

# Available Services
def Available_services():
    mycursor.execute("SELECT * FROM Services")
    service_type = mycursor.fetchall()
    print("_______________________Available Services_______________________:")
    for service in service_type:
        print(f"ServiceID: {service[0]} - ServiceName: {service[1]} - Cost:{service[2]} - Discription: {service[3]}")


# Only for service provider
def display_servicename_serviceprovider():
    mycursor.execute("SELECT * FROM Services")
    service_type = mycursor.fetchall()
    print("_______________________Available Services_______________________:")
    for service in service_type:
        print(f"ServiceID: {service[0]} - ServiceName: {service[1]}")


# display service providers
def display_service_providers(service_id,locationname):
    mycursor.execute("SELECT * FROM ServiceProvider where ServiceID=%s AND Location=%s",(service_id,locationname,))
    providers = mycursor.fetchall()
    if providers:
        print("____________________Service Providers list_________________________")
        for provider in providers:
            print(f"ProviderID: {provider[0]} - ProviderName: {provider[1]} - Location: {provider[2]} - Rating: {provider[3]}")
    else:
        print("No service providers found.")


# display provider branch locations
def display_locations(service_id,provider_id):
    mycursor.execute("SELECT providerName FROM ServiceProvider where ServiceID=%s", (service_id,))
    providers = mycursor.fetchall()
    providername=providers[0]

    mycursor.execute("SELECT * FROM Locations where ProviderID=%s",(provider_id,))
    locations = mycursor.fetchall()
    if locations:
        print("___________________Provider branch Location________________")
        for location in locations:
            print(f"LocationID: {location[0]}, ProviderName: {providername}, Address: {location[2]}, Rating: {location[3]}")
    else:
        print("No locations found.")


# display all location for Particular provider
def all_locations(providername):
    mycursor.execute("SELECT ProviderName,Location FROM ServiceProvider Where ProviderName=%s",(providername,))
    locations = mycursor.fetchall()
    if locations:
        print("________Provider Location____________________")
        for location in locations:
            print(f"ProviderName: {location[0]}  location: {location[1]}")
            print("----------------------------------------------")
    else:
        print("No locations found.")


# Display bookingservice requests
def bookingservice_requests(username):
   mycursor.execute("SELECT * FROM bookinghistory where WorkerName=%s",(username,))
   booking_records = mycursor.fetchall()

   if booking_records:
       print("_________________Booking Service list______________________")
       for record in booking_records:
           print("UserName:", record[1])
           user=record[1]
           mycursor.execute("SELECT MobileNo,Address FROM User where UserName=%s", (user,))
           userno = mycursor.fetchone()
           usermobile = userno[0]
           useraddress=userno[1]
           print("UserMobileNO:",usermobile)
           print("UserAddress:", useraddress)
           print("Booking ServiceName:", record[2])
           print("Booking Date:", record[7])
           print("Booking Status:",record[9])
           print("---------------------------------")
           print()
   else:
        print("booking service not found.")


# Display all workers details at location
def display_workers(location):
    mycursor.execute("SELECT * from Workers WHERE LocationID = %s", (location,))
    workers = mycursor.fetchall()
    if workers:
        print("_____________________Worker availble in this location________________")
        for worker in workers:
            print(f"WorkerID: {worker[0]}, Name: {worker[1]}, Rating: {worker[4]}")
    else:
        print("No workers found.")


# Display selected worker details
def workers_selection(worker_id):
    mycursor.execute("SELECT * from Workers WHERE WorkerID = %s", (worker_id,))
    select_worker= mycursor.fetchone()
    if select_worker:
        print("___________Selected Worker_________________")
        print(f"WorkerName: {select_worker[1]} - WokerMobileNo: {select_worker[2]} ")
    else:
        print("No workers found.")


# display all worker details at particular Provider
def display_All_Workers(providername):
    mycursor.execute("SELECT ProviderID,Location FROM ServiceProvider WHERE ProviderName=%s ",(providername,))
    provider = mycursor.fetchone()
    if provider:
        provider_id = provider[0]
        provider_location = provider[1]
    mycursor.execute("SELECT LocationID,Address FROM Locations WHERE ProviderID=%s AND LocationName=%s ",
                     (provider_id,provider_location,))
    location_id = mycursor.fetchone()
    if location_id:
        locationID = location_id[0]
        Address=location_id[1]

    mycursor.execute("SELECT * from Workers WHERE LocationID=%s",(locationID,))
    all_worker= mycursor.fetchall()
    if all_worker:
        print("---------All Worker List-------------")
        for workers in all_worker:
            print(f"WorkerName: {workers[1]} - WorkerMobileNo: {workers[2]} -WorkingAddress: {Address}")
    else:
        print("No workers found.")


# Booking the service
def bookingservice(username,service_id,location_id,worker_id):
    BookingStatus = input("Went to book this service -> Typing scheduled:")

    BookingDate = input("Enter booking date: ")

    mycursor.execute("select Cost from Services where ServiceID= %s", (service_id,))
    serviceprice = mycursor.fetchone()
    servicecost = serviceprice[0]
    mycursor.execute("select Discount from Offer where ServiceID= %s", (service_id,))
    discount = mycursor.fetchone()
    servicediscount = discount[0]
    DiscountedPrice=servicecost-(servicecost*(servicediscount/100))
    print("________________________Payment your service____________________________")
    print(f"Your Total PaymentAmount with discount:{DiscountedPrice}")
    TotalPayment=float(input("Send your Service TotalAmount:"))
    if(TotalPayment==DiscountedPrice):
        print("---------------------Payment Is Successful--------------------")

    mycursor.execute("select ServiceName from Services where ServiceID= %s", (service_id,))
    service = mycursor.fetchone()
    servicename = service[0]

    mycursor.execute("select providerName from ServiceProvider where ServiceID= %s", (service_id,))
    provider = mycursor.fetchone()
    providername = provider[0]

    mycursor.execute("SELECT Address FROM locations WHERE LocationID = %s", (location_id,))
    location = mycursor.fetchone()
    locationname = location[0]

    mycursor.execute("select WorkerName,WorkerMobileNo from Workers where WorkerID= %s", (worker_id,))
    worker = mycursor.fetchone()
    workername = worker[0]
    workermobile=worker[1]

    mycursor.execute("INSERT INTO bookinghistory (UserName,ServiceName,ProviderName,BranchAddress,WorkerName,WorkerMobileNo,TotalCost,BookingDate,BookingStatus) VALUES (%s, %s, %s,%s,%s,%s,%s,%s,%s)",
                     (username,servicename,providername,locationname,workername,workermobile,DiscountedPrice,BookingDate,BookingStatus))
    mydb.commit()
    print(f"-----------------------------{servicename} is booked successfully-------------------------------------")


# view user booking history
def view_booking_history(username,service_id):
    mycursor.execute("SELECT ServiceName FROM Services where ServiceID=%s", (service_id,))
    servicename = mycursor.fetchone()
    service = servicename[0]

    mycursor.execute("SELECT * FROM bookinghistory where UserName=%s", (username,))
    booking_records = mycursor.fetchall()
    if booking_records:
        print("--------Booking Details-------------")
        for record in booking_records:
            print("ServiceName:",service)
            print("ProviderName:", record[3])
            print("ProviderBranch Address:", record[4])
            print("WorkerName:", record[5])
            print("WorkerMobileNo:", record[6])
            print("Booking Date:", record[7])
            print("Total Cost:", record[8])
            print("---------------------------------")
            print()
    else:

        print("No booking history found.")


# show all booking history
def display_booking_history(username):
   mycursor.execute("SELECT * FROM bookinghistory where UserName=%s",(username,))
   booking_records = mycursor.fetchall()
   if booking_records:
       print("__________________Booking History________________________")
       for record in booking_records:
           print("UserName:", record[1])
           print("ServiceName:", record[2])
           print("ProviderName:", record[3])
           print("Location:", record[4])
           print("WorkerName:", record[5])
           print("WorkerMobileNo:", record[6])
           print("Booking Date:", record[7])
           print("Total Cost:", record[8])
           print("---------------------------------")
           print()
   else:

        print("No booking history found.")


# User Update the booking status
def update_booking_status(username):
    mycursor.execute("SELECT ServiceName FROM bookinghistory where UserName=%s", (username,))
    booking_servicename = mycursor.fetchall()
    print("________________Booked Service Name______________")
    print(booking_servicename)
    servicename=input("Choose the upadate service name: ")
    add_status = input("Booking service-> Cancel or Postponed: ").lower()

    if(add_status=="postponed"):
        postponed_date=input("Enter your postponed Date: ")
        mycursor.execute("UPDATE bookinghistory SET BookingStatus = %s, BookingDate=%s WHERE UserName = %s AND ServiceName=%s ",
                         (add_status,postponed_date,username, servicename))
        mydb.commit()
    elif(add_status=="cancel"):
        mycursor.execute("DELETE FROM bookinghistory WHERE UserName = %s AND ServiceName = %s", (username, servicename))
        mydb.commit()

    print(f"--------------------Booking Status {add_status} successfully-----------------------")


# User give feedback
def give_feedback(username,service_id):
    mycursor.execute("SELECT UserID FROM User WHERE UserName = %s", (username,))
    user = mycursor.fetchone()
    user_id = user[0]

    mycursor.execute("select * from Services where ServiceID= %s", (service_id,))
    service = mycursor.fetchone()
    service_id=service[0]

    comments = input("Enter your Comments: ")
    Rating = input("Enter the Rating(0-5): ")

    mycursor.execute("INSERT INTO Feedback (UserID, ServiceID,Rating,Comment) VALUES (%s, %s, %s,%s)",
                     (user_id,service_id,Rating,comments))
    mydb.commit()
    print("Feedback submitted successfully!")


# display feedback
def display_feedbacks():
    mycursor.execute("SELECT * FROM Feedback")
    feedbacks = mycursor.fetchall()
    if feedbacks:
        print("Feedbacks:")
        for feedback in feedbacks:
            print(f"User ID: {feedback[1]}, ServiceID: {feedback[2]} ,Comments:{feedback[3]},Rating: {feedback[4]}")
    else:
        print("No feedbacks found.")


# Display offers
def all_display_offers():
    mycursor.execute("SELECT * FROM Offer")
    offers = mycursor.fetchall()
    if offers:
        print("_________All service Offers___________")
        for offer in offers:
            mycursor.execute("select ServiceName from Services where ServiceID= %s", (offer[1],))
            service = mycursor.fetchall()
            servicename = service[0]
            print("ServiceName:",servicename )
            print("Discount:", offer[2])
            print("Expiry Date:", offer[3])
            print("_______________________________________")
    else:
        print("No offers found.")


# Display offer for selected service
def view_offers(service_id):
    mycursor.execute("select Discount from Offer where ServiceID= %s", (service_id,))
    Discount = mycursor.fetchall()
    if Discount:
        print("_____________Offer for your service_______________")
        for offer in Discount:
            print(f"Discount for this service : {offer[0]}%")
    else:
        print("No offer found.")



# Main function
def main():
    print("--------------- Welcome to Home Service App ---------------")
    while True:
        destination = input(
    "Are you a => user,newuser,Worker, newserviceprovider and serviceprovider and exit option?Type your destination: ").lower()

        if destination == "newuser":
            newuser_register()

        elif destination == "user":
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            if user_login(username, password):
                print("____________Login Successfully______________")
                while True:
                    print("_________________________________________________")
                    print("1:Booking the service ")
                    print("2:View Booking History")
                    print("3:Canceling or Postponing a Booking service")
                    print("4:Display offers")
                    print("5:Give feed back")
                    print("6:Exit")
                    print("___________________________________________________")
                    choice = int(input("Enter your option: "))
                    if choice == 1:
                        Available_services()

                        service_id = input("Enter Booking service ID: ")
                        print("-------your ServiceName is selected successfully-------")
                        view_offers(service_id)

                        locationname = input("Enter your location name: ")
                        display_service_providers(service_id, locationname)

                        provider_id = input('Choose the ServiceProvideName: ')
                        print("-------your ServiceProvider is selected successfully-------")
                        display_locations(service_id, provider_id)

                        location_id = input("Choose the Provider Branch locationID: ")
                        print("-------your ServiceProvider location is selected successfully-------")
                        display_workers(location_id)

                        worker_id = input("Choose the WorkerID: ")
                        workers_selection(worker_id)
                        print("-------Worker is selected successfully-------")
                        bookingservice(username, service_id, location_id, worker_id)

                        view_booking_history(username, service_id)
                    elif choice == 2:
                        display_booking_history(username)
                    elif choice == 3:
                        update_booking_status(username)
                    elif choice == 4:
                        all_display_offers()
                    elif choice == 5:
                        give_feedback(username, service_id)
                    elif choice == 6:
                        print("Exiting Home Service App. Thank you!")
                        exit()
                    else:
                        print("Invalid choice")
            else:
                print("User does not exist")

        elif destination == "worker":
            username = input("Enter your name: ")
            while True:
                print("1:View Booking services")
                print("2: Exit")
                choice = int(input("Enter your option: "))
                if choice == 1:
                    bookingservice_requests(username)
                elif choice ==2:
                    print("Exiting Home Service App. Thank you!")
                    exit()
                else:
                    print("Invalid choice")

        elif destination == "newserviceprovider":
            display_servicename_serviceprovider()
            service_id = input("Choose the serviceID: ")
            register_service_provider(service_id)

        elif destination == "serviceprovider":
            providername = input("Enter your provider name: ")
            while True:
                print("1: View your provider location")
                print("2: Display Workers")
                choice = int(input("Enter your option: "))
                if choice == 1:
                    all_locations(providername)
                elif choice == 2:
                    display_All_Workers(providername)
                else:
                    print("Invalid choice")

        elif destination == "admin":
            while True:
                print("1: Register New Service: ")
                print("2: Exit")
                choice = int(input("Enter your option: "))
                if choice == 1:
                    newservice_register()
                elif choice == 2:
                    exit()
                else:
                    print("Invalid choice")

        elif destination == "exit":
            print("Exiting Home Service App. Thank you!")

        else:
            print("Invalid destination")

    mycursor.close()
    mydb.close()
    print("App closed.")


if __name__ == "__main__":
    main()
