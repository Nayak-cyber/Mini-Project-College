from flask import Flask,render_template,request,url_for,redirect,Response
from serpapi import GoogleSearch
import gspread
import cv2
import os
import pymongo

item=["Blue Shirt","Red Shirt","Black Pants","Watch"]

myclient=pymongo.MongoClient("mongodb://localhost:27017/")

mydb=myclient["orders"]

mycol=mydb["order"]

li=[]

for x in mycol.find():
  li.append(x)


app = Flask(__name__)

camera = cv2.VideoCapture(0)

detected_face_name=""

reference_images_dir = 'Gugs'

# Load all reference images and their names
reference_images = []
reference_names = []

for filename in os.listdir(reference_images_dir):
    if filename.endswith('.jpg') or filename.endswith('.png') or filename.endswith('.jpeg'):
        image_path = os.path.join(reference_images_dir, filename)
        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        image = cv2.resize(image, (100, 100))  # Resize for better performance
        reference_images.append(image)
        reference_names.append(os.path.splitext(filename)[0])

# Create a Haar cascade for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Flask route
def admin_access():
    global detected_face_name
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        exit()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Convert the frame to grayscale (since you're using template matching with grayscale images)
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the frame
        faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        # Initialize a variable to store the detected face name
        face_name = "Unknown"

        for (x, y, w, h) in faces:
            # Extract the face region from the frame
            face_region = gray_frame[y:y+h, x:x+w]
            best_match_name = "Unknown"
            best_match_value = 0

            # Compare the face region with all reference images
            for ref_image, name in zip(reference_images, reference_names):
                face_region_resized = cv2.resize(face_region, (ref_image.shape[1], ref_image.shape[0]))  # Resize the face region to match reference image size
                
                # Perform template matching
                result = cv2.matchTemplate(face_region_resized, ref_image, cv2.TM_CCOEFF_NORMED)
                _, max_val, _, _ = cv2.minMaxLoc(result)

                # Update the best match if this one is better
                if max_val > best_match_value:
                    best_match_value = max_val
                    best_match_name = name

            # Set the face name based on the best match
            face_name = best_match_name if best_match_value > 0.2 else "Unknown"
            detected_face_name = face_name  # This is the name of the detected face

            # Draw a rectangle around the detected face
            color = (0, 255, 0) if face_name != "Unknown" else (0, 0, 255)
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            cv2.putText(frame, face_name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

        print(detected_face_name)  # Print the detected face name in the console

        # Encode frame in JPEG format
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        # Yield the output frame in byte format
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()

def generate_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def update_google_sheet(name, email, message):
    client = gspread.service_account(filename="key.json")
    sheet = client.open("Mini Project Contact Form").sheet1  # Open the first sheet

    # Find the next available row
    next_row = len(sheet.get_all_values()) + 1

    # Update the sheet with new data
    sheet.update(f'A{next_row}:C{next_row}', [[name, email, message]])


web_name="Shopsmart"

dis=[]

order_item=""



def get_title(ite):
    params = {
    "engine": "walmart",
    "query": ite,
    "api_key": "f920b8404f9a0de2279ac3d8097f9c87af3b632cae57c969cd5043aa701a63c2"
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    organic_results = results["organic_results"][2]["title"]
    return organic_results

def fetch_image(query):
    params = {
        "engine": "google_images",
        "q": query,
        "location": "Austin, TX, Texas, United States",
        "api_key": "f920b8404f9a0de2279ac3d8097f9c87af3b632cae57c969cd5043aa701a63c2"
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    
    # Extract the URL of the first image
    if "images_results" in results and len(results["images_results"]) > 0:
        return results["images_results"][0].get("thumbnail")  # or use "original" if you need the full-sized image
    return None

one_image_per_query = {}

# for query in item:
#     # print(f"Fetching image for: {query}")
#     one_image_per_query[query] = fetch_image(query)
#     dis.append(get_title(query))

# img_url=[]

# # Print the collected image URLs
# for query, image_url in one_image_per_query.items():
#     if image_url:
#         img_url.append(image_url)
#         # print(f"\nImage for query '{query}': {image_url}")
#     else:
#         print(f"\nNo image found for query '{query}'")

# @app.route("/")
# def hello_world():
# #     return render_template("index.html",web_name=web_name)
# print("It worked correctly")
# print(image_url[1])
# https://rukminim2.flixcart.com/image/850/1000/xif0q/shirt/y/s/9/xxl-sh-55-getchi-original-imahfft2hpfenkx8.jpeg?q=90&crop=false

img_url=["https://rukminim2.flixcart.com/image/850/1000/xif0q/shirt/y/s/9/xxl-sh-55-getchi-original-imahfft2hpfenkx8.jpeg?q=90&crop=false",
         "https://rukminim2.flixcart.com/image/850/1000/shirt/h/w/h/12001red-english-navy-42-original-imaezh48h3gfnczr.jpeg?q=20&crop=false",
         "https://www.beyours.in/cdn/shop/files/eveeryday-pant--black-1.jpg?v=1688369505",
         "https://m.media-amazon.com/images/I/6166QQmf+YL._AC_UY1000_.jpg"]

dis=["Stylish blue shirt with a modern fit for casual wear.",
     "Bold red shirt, perfect for making a statement.",
     "Sleek black pants offering comfort and versatility for any occasion.",
     "Elegant wristwatch featuring a minimalist design for everyday use."]

@app.route("/")
def index():
    global detected_face_name
    combin=list(zip(item,img_url,dis))

    print(combin)
    print(detected_face_name)
    return render_template("index.html",name=web_name,item=item,img_url=img_url,combin=combin)


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/admin")
def webcam():
    detected_face_name
    return render_template("adminlog.html",name=detected_face_name)

@app.route("/panel")
def admin_panel():
    if detected_face_name=="Nayak" or detected_face_name=="Gugan":
        return render_template("panel.html",li=li)
    else:
        return render_template("not_panel.html")

# @app.route("/testing")
# def testing():
#     return render_template("adminlog.html")

# @app.route('/video_feed')
# def video_feed():
#     # Returns the generated frames as a video stream
#     return Response(generate_frames(),
#                     mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/face_recog')
def face_recog():
    return Response(admin_access(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/checkout/<product>/")
def checkout(product):
    global order_item
    order_item=product
    return render_template("checkout.html",product=product)



@app.route("/login",methods=['GET','POST'])
def login():
    if request.method == "POST":
       # getting input with name = fname in HTML form
       email=request.form.get("email")
       text=request.form.get("text")
       message=request.form.get("message")
       print(text+"\n"+email+"\n"+message)
       update_google_sheet(email,text,message)
       return redirect("/thanks")
    return render_template("contact.html")

@app.route('/checkout/confirmation', methods=['POST'])
def checkout_confirmation():
    global order_item  # Ensure order_item is set globally before this function is called
    print(order_item)
    global li
    name = request.form.get('name')
    email = request.form.get('email')
    address = request.form.get('address')
    city = request.form.get('city')
    zip_code = request.form.get('zip')
    payment_method = request.form.get('payment_method')
    password = request.form.get('password')  # New password field

    # Check if email already exists in the MongoDB collection
    existing_user = mycol.find_one({"email": email})
    if existing_user:
        # If email exists, check if password matches
        if existing_user['password'] != password:
            return render_template('password_mismatch.html')  # Password mismatch error page

    # Include order_item in the data to be saved
    mydict = {
        "name": name,
        "email": email,
        "address": address,
        "city": city,
        "zip_code": zip_code,
        "payment_method": payment_method,
        "password": password,  # Store password (consider hashing for security)
        "order_item": order_item  # Add the order item
    }

    x = mycol.insert_one(mydict)
    li.append(mydict)
    print(f"Order ID: {x.inserted_id} has been successfully placed!")

    # Pass order_item to the template
    return render_template(
        'confirmation.html', 
        name=name, 
        email=email, 
        address=address, 
        city=city, 
        zip=zip_code, 
        payment_method=payment_method,
        order_item=order_item  # Add order item to the template
    )



@app.route('/userlogin', methods=['GET', 'POST'])
def userlogin():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Check if the email and password match a record in MongoDB
        user = mycol.find_one({"email": email, "password": password})
        
        if user:
            # Fetch orders for the logged-in user
            orders = mycol.find({"email": email})
            return render_template('user_dashboard.html', orders=orders, user=user)
        else:
            error = "Invalid email or password. Please try again."
            return render_template('userlogin.html', error=error)
    
    # Render login page for GET request
    return render_template('userlogin.html')



@app.route("/thanks")
def feed():
    return render_template("thanks_feed.html")

@app.route("/thanksbye")
def bought():
    return render_template("bought.html")


@app.route("/about")
def about():
    return render_template("about.html")


def contact():
    return render_template("contact.html")

if __name__=="__main__":
    app.run(debug=True)