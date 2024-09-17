from flask import Flask,render_template,request,url_for,redirect,Response
from serpapi import GoogleSearch
import gspread
import cv2

item=["Blue Shirt","Red Shirt","Black Pants","Watch"]


app = Flask(__name__)

camera = cv2.VideoCapture(0)

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
    combin=list(zip(item,img_url,dis))
    print(combin)
    return render_template("index.html",name=web_name,item=item,img_url=img_url,combin=combin)


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/admin")
def webcam():
    return render_template("webcam.html")

@app.route('/video_feed')
def video_feed():
    # Returns the generated frames as a video stream
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/checkout/<product>/")
def checkout(product):
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