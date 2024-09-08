# from serpapi import GoogleSearch

# # Define your list of search queries
# search_queries = ["Red Shirt", "Blue Jeans", "Black Shoes"]

# # Define a function to fetch one image for a given query
# def fetch_image(query):
#     params = {
#         "engine": "google_images",
#         "q": query,
#         "location": "Austin, TX, Texas, United States",
#         "api_key": "f920b8404f9a0de2279ac3d8097f9c87af3b632cae57c969cd5043aa701a63c2"
#     }
#     search = GoogleSearch(params)
#     results = search.get_dict()
    
#     # Extract the URL of the first image
#     if "images_results" in results and len(results["images_results"]) > 0:
#         return results["images_results"][0].get("thumbnail")  # or use "original" if you need the full-sized image
#     return None

# # Dictionary to store one image for each query
# one_image_per_query = {}

# # Fetch one image for each query
# for query in search_queries:
#     # print(f"Fetching image for: {query}")
#     one_image_per_query[query] = fetch_image(query)

# img_link=[]

# # Print the collected image URLs
# for query, image_url in one_image_per_query.items():
#     if image_url:
#         img_link.append(image_url)
#         print(f"\nImage for query '{query}': {image_url}")
#     else:
#         print(f"\nNo image found for query '{query}'")

# print(img_link)

# from serpapi import GoogleSearch

# def get_product_descriptions(api_key, product_names):
#     product_descriptions = {}

#     for product in product_names:
#         search = GoogleSearch({
#             "q": product,
#             "tbm": "shop",
#             "api_key": api_key
#         })
#         results = search.get_dict()

#         if "shopping_results" in results:
#             # Get the first result's description
#             description = results['shopping_results'][0].get('description', 'No description found')
#         else:
#             description = "No results found"

#         product_descriptions[product] = description

#     return product_descriptions

# # Replace with your actual SerpApi key
# api_key = "YOUR_SERPAPI_API_KEY"

# # List of product names
# product_names = ["iPhone 14", "Samsung Galaxy S23", "Sony WH-1000XM5"]

# descriptions = get_product_descriptions(api_key, product_names)

# for product, description in descriptions.items():
#     print(f"{product}: {description}")

# from serpapi import GoogleSearch

# def get_title(ite):
#     params = {
#     "engine": "walmart",
#     "query": ite,
#     "api_key": "f920b8404f9a0de2279ac3d8097f9c87af3b632cae57c969cd5043aa701a63c2"
#     }

#     search = GoogleSearch(params)
#     results = search.get_dict()
#     organic_results = results["organic_results"][2]["title"]
#     return organic_results

# item=["black shirt","red shirt"]

# dis=[]

# for i in item:
#     dis.append(get_title(i))

# for i in dis:
#     print(i)


# import requests

# r = requests.get('https://serpapi.com/search.json?engine=google&q=Coffee', auth=('user', 'pass'))

# file=r.json()
# print(file)

# import gspread

# # Authenticate using the service account
# client = gspread.service_account(filename="key.json")

# # Open the spreadsheet by name
# spreadsheet = client.open("Mini Project Contact Form")

# # Select the first sheet (worksheet)
# worksheet = spreadsheet.sheet1  # Or use .worksheet("Sheet1") if you know the sheet's name

# # Define the three variables you want to write
# var1 = "Value1"
# var2 = "Value2"
# var3 = "Value3"

# # Find the next empty row
# next_row = len(worksheet.get_all_values()) + 1

# # Update the next row with the three variables
# worksheet.update(f'A{next_row}:C{next_row}', [[var1, var2, var3]])

# print(f"Values written to row {next_row}: {var1}, {var2}, {var3}")
# app.py
from flask import Flask, Response, render_template
import cv2

app = Flask(__name__)

# Initialize the webcam
camera = cv2.VideoCapture(0)  # 0 is the default camera

def generate_frames():
    while True:
        # Capture frame-by-frame
        success, frame = camera.read()
        if not success:
            break
        else:
            # Encode the frame in JPEG format
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            # Concatenate frame one by one and show result
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('test.html')

@app.route('/video_feed')
def video_feed():
    # Returns the generated frames as a video stream
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True)

